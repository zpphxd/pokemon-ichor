#!/usr/bin/env python3
"""Three-way merge of a JSON registry whose lists hold objects keyed by an id
(layouts.json by "id", wild_encounters.json by "base_label").

For each keyed list: entries ours and theirs share are taken from whichever
side changed them (ours wins when both did, and is reported); entries one side
removed stay removed; entries either side added are kept, ours first, then
theirs' in their own order. Builds from the merge's stages 1-3.

  python3 tools/ichor/merge/union_json_keyed.py FILE...
"""
import json
import subprocess
import sys

KEYS = ("id", "base_label", "label")


def stage(n, path):
    return json.loads(subprocess.run(["git", "show", f":{n}:{path}"], capture_output=True,
                                     text=True, check=True).stdout)


def key_of(lst):
    for k in KEYS:
        if lst and all(isinstance(e, dict) and k in e for e in lst):
            return k
    return None


def merge(b, o, t, where):
    if o == t:
        return o
    if o == b:
        return t
    if t == b:
        return o
    if isinstance(o, dict) and isinstance(t, dict):
        b = b if isinstance(b, dict) else {}
        out = {}
        for k in list(o) + [k for k in t if k not in o]:
            if k not in o:
                if k not in b:
                    out[k] = t[k]
                continue
            if k not in t:
                if k not in b:
                    out[k] = o[k]
                continue
            out[k] = merge(b.get(k), o[k], t[k], f"{where}.{k}")
        return out
    if isinstance(o, list) and isinstance(t, list):
        k = key_of(o) or key_of(t)
        if k:
            b = b if isinstance(b, list) else []
            bm = {e[k]: e for e in b}
            om = {e[k]: e for e in o}
            tm = {e[k]: e for e in t}
            out = []
            for e in o:
                if e[k] in tm:
                    out.append(merge(bm.get(e[k]), e, tm[e[k]], f"{where}[{e[k]}]"))
                elif e[k] not in bm:
                    out.append(e)  # ours added
            for e in t:
                if e[k] not in om and e[k] not in bm:
                    out.append(e)  # theirs added
            return out
    print(f"both changed {where}: kept ours")
    return o


for path in sys.argv[1:]:
    out = merge(stage(1, path), stage(2, path), stage(3, path), path)
    with open(path, "w") as f:
        f.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"resolved {path}")
