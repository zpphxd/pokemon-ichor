#!/usr/bin/env python3
"""Fold staged Act II parties into src/data/trainers.party and opponents.h.

  python3 tools/ichor/act2/fold_parties.py design/phase3/parties/*.party

Each staged file holds `=== TRAINER_ICHOR_<NAME> ===` blocks in the .party
syntax (design/phase3/SCRIPT.md Part 3). This script:
  - drops `Ability:` lines while the Aethos species are stand-ins (ICHOR_STUB_AETHOS_DEX);
  - maps classes and pics that don't exist yet to stand-ins (ICHOR_STUB_TRAINER_ART),
    keeping the intended one in a comment, until the sprites agent adds them;
  - assigns each new name the next free id in its block (design/phase3/BUILD.md's
    ranges) and rewrites the world-act2 block of include/constants/opponents.h;
  - rewrites the /* Ichor: world-act2 */ section of src/data/trainers.party.
Run it again after any staged file changes: it rebuilds both sections whole.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PARTY = ROOT / "src/data/trainers.party"
OPP = ROOT / "include/constants/opponents.h"
ORDER = ROOT / "design/phase3/parties/ORDER.txt"   # one id name per line, in id order (160 up)

def known(kind):
    """Classes and pics trainerproc can resolve today."""
    src = (ROOT / "include/constants/trainers.h").read_text()
    pre = {'Class': 'TRAINER_CLASS_', 'Pic': 'TRAINER_PIC_', 'Music': 'TRAINER_ENCOUNTER_MUSIC_'}[kind]
    return set(m.group(1) for m in re.finditer(r'\b' + pre + r'([A-Z0-9_]+)\b', src))

def norm(s):
    return re.sub(r'[^A-Z0-9]+', '_', s.upper()).strip('_')

CLASS_STANDIN = {'MAENAD': 'Harvester', 'SATYR': 'Goatherd', 'ACTOR': 'Acolyte', 'VINTNER': 'Harvester',
                 'FOWLER': 'Shepherd', 'HUNTRESS': 'Hoplite', 'CHARCOALER': 'Shepherd', 'HEALER': 'Acolyte',
                 'ATHLETE': 'Hoplite', 'PHILOSOPHER': 'Augur', 'ARCHER': 'Hoplite', 'SMITH': 'Shepherd',
                 'DIVER': 'Shepherd', 'PILGRIM': 'Shepherd', 'RUNNER': 'Hoplite', 'MERCHANT': 'Shepherd',
                 'FISHER': 'Shepherd', 'SAILOR': 'Shepherd', 'SCHOLAR': 'Augur', 'TITAN_ADMIN': 'Titanborn',
                 'JESTER': 'Goatherd', 'INITIATE': 'Acolyte', 'POTTER': 'Shepherd', 'BEEKEEPER': 'Harvester',
                 'SWINEHERD': 'Shepherd'}
PIC_STANDIN = {'Class': None}

def main(files):
    classes, pics, music = known('Class'), known('Pic'), known('Music')
    blocks = []
    for f in files:
        txt = Path(f).read_text()
        for m in re.finditer(r'^=== (TRAINER_ICHOR_[A-Z0-9_]+) ===\n(.*?)(?=^=== |\Z)', txt, re.S | re.M):
            blocks.append((m.group(1), m.group(2).rstrip() + '\n'))
    order = [l.strip() for l in ORDER.read_text().split('\n') if l.strip() and not l.startswith('#')]
    names = [b[0] for b in blocks]
    for n in names:
        if n not in order:
            sys.exit(f'{n} is not in {ORDER.relative_to(ROOT)}: add it to its agent\'s range')
    out = ['/* Ichor: world-act2 (ids 160-319) */', '']
    for name, body in sorted(blocks, key=lambda b: order.index(b[0])):
        lines = []
        for line in body.split('\n'):
            if line.startswith('Ability:'):
                continue  # ICHOR_STUB_AETHOS_DEX
            mm = re.match(r'^Music: (.+)$', line)
            if mm and norm(mm.group(1)) not in music:
                line = 'Music: Male'  # ICHOR_STUB_MUSIC
            m = re.match(r'^(Class|Pic): (.+)$', line)
            if m:
                kind, val = m.groups()
                have = classes if kind == 'Class' else pics
                if norm(val) not in have:
                    stand = CLASS_STANDIN.get(norm(val)) if kind == 'Class' else None
                    if kind == 'Pic':
                        # a new person's portrait: borrow the class's stand-in pic
                        stand = {'HIEROPHANT': 'Hierophant Ione'}.get(norm(val).split('_')[0], 'Shepherd')
                    line = f'{kind}: {stand or "Shepherd"}'
            lines.append(line)
        out.append(f'=== {name} ===')
        out.extend(l for l in lines if l is not None)
    party = PARTY.read_text()
    a = party.index('/* Ichor: world-act2 (ids 160-319) */')
    b = party.index('/* Ichor: world-act3')
    PARTY.write_text(party[:a] + '\n'.join(out).rstrip() + '\n\n\n' + party[b:])
    opp = OPP.read_text()
    # Act II's ids: 160-319, then 820-849 from the shared reserve (tools/ichor/claim_ranges.md).
    blocks_ids = list(range(160, 320)) + list(range(820, 850))
    if len(order) > len(blocks_ids):
        sys.exit(f'{len(order)} trainers, but Act II has {len(blocks_ids)} ids (160-319, 820-849): ask the director for more')
    defs = [f'#define {n:<37} {blocks_ids[i]}' for i, n in enumerate(order)]
    end = blocks_ids[len(order) - 1] + 1 if order else 0
    new = ('// world-act2, ids 160-319: Thyrsa, Arkadia, Astyra, Kaldera.\n' + '\n'.join(defs)
           + ('\n' if defs else '') + f'#define TRAINERS_END_ACT2                     {end}\n')
    opp = re.sub(r'// world-act2, ids 160-319:.*?#define TRAINERS_END_ACT2\s+\d+\n', new, opp, flags=re.S)
    OPP.write_text(opp)
    print(f'{len(blocks)} parties, {len(order)} ids, the last {end - 1}')

if __name__ == '__main__':
    main(sys.argv[1:])
