#!/usr/bin/env python3
"""Write Route 4's wild encounter tables into src/data/wild_encounters.json.

The tables are SCRIPT.md Part 4's "Route 2, the Sacred Way" (levels 16-19, BALANCE.md's
Eleusa row), with the director's rulings applied (BUILD.md):
  - no early-evolved wild forms: Gelasable (from Galekit at 20) and Cairnolith (from
    Pebblith at 25) leave the night table for Galekit and Pebblith. Lophops (from Epopoi
    at 14) and Kerazap (friendship; the dex has it on the mainland's hill pastures) stay.
  - Obolorn at 1% at night among the roadside tombs.
Three times of day (the expansion's OW_TIME_OF_DAY_ENCOUNTERS; morning 6-10, day 10-19,
evening 19-20, night 20-6). Evening has no table of its own and falls back to _Morning,
so _Morning is dawn and dusk: the goats graze then, and the hoopoes call.
_Morning also carries the rock-smash table (marble rubble broken with the Bronze Hammer;
the dex: Pebblith "often tumbles out of rocks broken with the Bronze Hammer"); the other
times fall back to it.

Usage: /usr/bin/python3 tools/ichor/maps/route4_encounters.py   (idempotent)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JSON = ROOT / "src/data/wild_encounters.json"
MAP = "MAP_ROUTE4_ISTHMUS"


def mons(rows):
    return [{"min_level": lo, "max_level": hi, "species": f"SPECIES_{s}"} for s, lo, hi in rows]


# land slots 20/20/10/10/10/10/5/5/4/4/1/1
MORNING = [("EPOPOI", 16, 18), ("KERAZAP", 17, 19), ("LOPHOPS", 16, 18), ("ONOTIS", 16, 18),
           ("GALEKIT", 16, 18), ("CHELONET", 16, 18), ("ERGANT", 16, 18), ("ELALEAF", 16, 18),
           ("SPALUNK", 17, 19), ("HARPECK", 17, 19), ("NEMECUB", 18, 18), ("KERAZAP", 19, 19)]
DAY = [("LOPHOPS", 16, 18), ("ONOTIS", 16, 18), ("CHELONET", 16, 18), ("GALEKIT", 16, 18),
       ("KERAZAP", 17, 19), ("EPOPOI", 16, 18), ("ERGANT", 16, 18), ("ELALEAF", 16, 18),
       ("SPALUNK", 17, 19), ("HARPECK", 17, 19), ("NEMECUB", 18, 18), ("NEMECUB", 19, 19)]
NIGHT = [("GALEKIT", 16, 18), ("ONOTIS", 16, 18), ("GALEKIT", 17, 19), ("CHELONET", 16, 18),
         ("PEBBLITH", 17, 19), ("SPALUNK", 16, 18), ("PEBBLITH", 16, 18), ("KERAZAP", 17, 19),
         ("ERGANT", 17, 19), ("HARPECK", 18, 19), ("OBOLORN", 18, 18), ("NEMECUB", 18, 18)]
# rock smash slots 60/30/5/4/1
ROCKS = [("PEBBLITH", 16, 19), ("SPALUNK", 16, 18), ("PEBBLITH", 18, 19), ("CHELONET", 17, 19),
         ("PEBBLITH", 19, 19)]


def entries():
    return [
        {"map": MAP, "base_label": "gRoute4Isthmus_Morning",
         "land_mons": {"encounter_rate": 20, "mons": mons(MORNING)},
         "rock_smash_mons": {"encounter_rate": 20, "mons": mons(ROCKS)}},
        {"map": MAP, "base_label": "gRoute4Isthmus_Day",
         "land_mons": {"encounter_rate": 20, "mons": mons(DAY)}},
        {"map": MAP, "base_label": "gRoute4Isthmus_Night",
         "land_mons": {"encounter_rate": 20, "mons": mons(NIGHT)}},
    ]


def main():
    data = json.loads(JSON.read_text())
    group = next(g for g in data["wild_encounter_groups"] if g["label"] == "gWildMonHeaders")
    enc = group["encounters"]
    old = [i for i, e in enumerate(enc) if e.get("map") == MAP]
    at = old[0] if old else next((i + 1 for i in range(len(enc) - 1, -1, -1)
                                  if enc[i].get("map", "").startswith("MAP_ELEUSA")), len(enc))
    enc[:] = [e for e in enc if e.get("map") != MAP]
    enc[at:at] = entries()
    JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"{JSON}: {MAP} morning, day and night land tables, and rock smash")


if __name__ == "__main__":
    main()
