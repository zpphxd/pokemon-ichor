#!/usr/bin/env python3
"""Turn a SCRIPT.md Part 4 section into wild_encounters.json entries.

  python3 tools/ichor/act2/encounters_from_script.py PART4.md > design/phase3/encounters/<agent>.json

Reads each "`MAP_X`, land `encounter_rate: N`" heading and the 12-slot table under it
(Slot | Rate | _Morning | Levels | _Night | Levels) and writes one entry per time of day:
gX_Morning, and gX_Night where the night column differs. Species names are the Aethos
names (SPECIES_<NAME>), which the stand-in headers resolve (ICHOR_STUB_AETHOS_DEX).
Fishing and surfing tables are read when headed "`MAP_X` fishing" / "`MAP_X` water".
"""
import json, re, sys

def label(map_const):
    words = map_const[4:].split('_')
    return 'g' + ''.join(w.capitalize() if not w.isdigit() else w for w in words)

def parse(txt):
    out = []
    for m in re.finditer(r'`(MAP_[A-Z0-9_]+)`, land `encounter_rate: (\d+)`(.*?)(?=\n`MAP_|\n## |\Z)', txt, re.S):
        mp, rate, body = m.group(1), int(m.group(2)), m.group(3)
        rows = [r for r in body.split('\n') if re.match(r'^\|\s*\d+\s*\|', r)]
        if len(rows) < 12: continue
        day, night = [], []
        for r in rows[:12]:
            c = [x.strip() for x in r.strip('|').split('|')]
            def mon(name, lv):
                name = re.sub(r'[†*]', '', name).strip()
                a, b = (re.split(r'[–-]', lv) + [lv])[:2]
                return {'min_level': int(a), 'max_level': int(b), 'species': 'SPECIES_' + name.upper()}
            day.append(mon(c[2], c[3])); night.append(mon(c[4], c[5]))
        base = label(mp)
        out.append({'map': mp, 'base_label': base + '_Morning', 'land_mons': {'encounter_rate': rate, 'mons': day}})
        if night != day:
            out.append({'map': mp, 'base_label': base + '_Night', 'land_mons': {'encounter_rate': rate, 'mons': night}})
    return out

if __name__ == '__main__':
    json.dump(parse(open(sys.argv[1]).read()), sys.stdout, indent=2)
    print()
