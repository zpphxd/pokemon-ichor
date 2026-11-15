#!/usr/bin/env python3
"""Fold staged Act II wild tables into src/data/wild_encounters.json.

  python3 tools/ichor/act2/fold_encounters.py design/phase3/encounters/*.json

Each staged file is a list of wild_encounters.json entries ({"map", "base_label",
"land_mons" / "water_mons" / "fishing_mons" ...}). Each entry replaces the entry
with the same base_label in the land group, or is appended. Labels end in _Morning
(morning, day and evening) or _Night; a map with no _Night entry falls back to
_Morning at night (OW_TIME_OF_DAY_FALLBACK), so caves and fishing need only _Morning.
Run it again after any staged file changes.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WILD = ROOT / "src/data/wild_encounters.json"


def main(files):
    data = json.loads(WILD.read_text())
    group = data["wild_encounter_groups"][0]
    by_label = {e["base_label"]: i for i, e in enumerate(group["encounters"])}
    added = replaced = 0
    for f in files:
        for entry in json.loads(Path(f).read_text()):
            label = entry["base_label"]
            if not (label.endswith("_Morning") or label.endswith("_Night")):
                sys.exit(f"{f}: {label} needs a _Morning or _Night suffix")
            if label in by_label:
                group["encounters"][by_label[label]] = entry
                replaced += 1
            else:
                by_label[label] = len(group["encounters"])
                group["encounters"].append(entry)
                added += 1
    WILD.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"{added} added, {replaced} replaced; {len(group['encounters'])} entries in {group['label']}")


if __name__ == "__main__":
    main(sys.argv[1:])
