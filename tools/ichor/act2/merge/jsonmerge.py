#!/usr/bin/env python3
"""Three-way merge of data/maps/map_groups.json or src/data/wild_encounters.json, mid-merge.
  python3 tools/ichor/act2/merge/jsonmerge.py THEIRS FILE   (from the repo root)
map_groups: each list keeps ours' order, drops what theirs removed, adds what theirs added
after its predecessor. wild_encounters: entries by base_label; theirs' changes win unless
ours changed the same entry too (listed as 'both changed', ours kept)."""
import json, subprocess, sys
THEIRS, f = sys.argv[1], sys.argv[2]
def git(*a): return subprocess.run(['git', *a], capture_output=True, text=True).stdout
base = git('merge-base', 'HEAD', THEIRS).strip()
B, O, T = (json.loads(git('show', f'{r}:{f}')) for r in (base, 'HEAD', THEIRS))
def mlist(b, o, t):
    b = b or []; out = [x for x in o if not (x in b and x not in t)]
    for i, x in enumerate(t):
        if x in out or x in b: continue
        prev = next((t[j] for j in range(i - 1, -1, -1) if t[j] in out), None)
        out.insert(out.index(prev) + 1 if prev is not None else len(out), x)
    return out
conf = []
if 'group_order' in O:
    R = {}
    for k in list(O) + [k for k in T if k not in O]:
        if k in B and k not in T: continue
        if k not in O and k in B: continue
        o, t, b = O.get(k, []), T.get(k, []), B.get(k)
        R[k] = mlist(b, o, t) if isinstance(o, list) else (t if o == b else o)
else:
    R = O
    for og in O['wild_encounter_groups']:
        tg = next(g for g in T['wild_encounter_groups'] if g['label'] == og['label'])
        bg = next((g for g in B['wild_encounter_groups'] if g['label'] == og['label']), {'encounters': []})
        key = lambda e: e.get('base_label') or (e.get('map'), json.dumps(e, sort_keys=True))
        bo = {key(e): e for e in bg['encounters']}; to = {key(e): e for e in tg['encounters']}
        enc = []
        for e in og['encounters']:
            k = key(e)
            if k in bo and k not in to: continue
            if k in to and to[k] != bo.get(k):
                if e != bo.get(k) and e != to[k]: conf.append(k); enc.append(e); continue
                e = to[k]
            enc.append(e)
        have = {key(e) for e in enc}
        enc += [e for k, e in to.items() if k not in have and k not in bo]
        og['encounters'] = enc
        if og.get('fields') != tg.get('fields') and og.get('fields') == bg.get('fields'): og['fields'] = tg['fields']
open(f, 'w').write(json.dumps(R, indent=2, ensure_ascii=False) + '\n')
print(f, 'merged; both changed:', conf)
