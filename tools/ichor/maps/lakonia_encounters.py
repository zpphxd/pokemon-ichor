#!/usr/bin/env python3
"""Write Lakonia's wild tables (design/phase4/SCRIPT.md Part 4, "Lakonia's tables")
into src/data/wild_encounters.json: Gytheion's harbor, Route 25 and the
training fields. Rerunning replaces the entries it owns.

    python3 tools/ichor/maps/lakonia_encounters.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "src/data/wild_encounters.json"


def mons(rows):
    return [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + s.upper()} for (s, lo, hi) in rows]


HARBOR_SURF = [("Galenyon", 45, 48), ("Narkeray", 45, 48), ("Karkitox", 46, 49), ("Kynoketos", 47, 49),
               ("Telkanvil", 48, 49)]
HARBOR_FISH = [("Ketofry", 5, 10), ("Karkipool", 10, 15),
               ("Narkeray", 35, 40), ("Ketofry", 15, 19), ("Karkipool", 20, 27),
               ("Kynoketos", 45, 49), ("Narkeray", 45, 49), ("Karkitox", 45, 49), ("Telkanvil", 47, 49),
               ("Kynoketos", 49, 49)]
RIVER_FISH = [("Ketofry", 5, 10), ("Ketofry", 10, 14),
              ("Ketofry", 15, 19), ("Karkipool", 20, 27), ("Karkipool", 22, 27),
              ("Karkitox", 45, 49), ("Kynoketos", 45, 49), ("Karkitox", 46, 49), ("Kynoketos", 47, 49),
              ("Karkitox", 49, 49)]
RIVER_SURF = [("Karkitox", 46, 48), ("Galenyon", 46, 48), ("Karkitox", 47, 49), ("Kynoketos", 48, 50),
              ("Galenyon", 49, 50)]
R25_MORNING = [("Gelasable", 46, 48), ("Hoplomex", 46, 48), ("Kerazap", 46, 48), ("Chelonet", 46, 48),
               ("Cairnolith", 47, 49), ("Galenyon", 47, 49), ("Onotis", 47, 49), ("Kaplet", 47, 49),
               ("Elapling", 48, 50), ("Hoplomex", 49, 50), ("Nemeleon", 50, 50), ("Stachypter", 50, 50)]
R25_NIGHT = [("Gelasable", 46, 48), ("Cairnolith", 46, 48), ("Kerazap", 46, 48), ("Karkitox", 46, 48),
             ("Gelasable", 47, 49), ("Kaplet", 47, 49), ("Chelonet", 47, 49), ("Kalyptor", 47, 49),
             ("Cairnolith", 48, 50), ("Karkitox", 48, 50), ("Nemeleon", 50, 50), ("Kalyptor", 50, 50)]
LAK_MORNING = [("Dorydrake", 47, 49), ("Hoplomex", 47, 49), ("Gelasable", 47, 49), ("Kerazap", 47, 49),
               ("Hoplomex", 48, 50), ("Dorydrake", 48, 50), ("Cairnolith", 48, 50), ("Chelonet", 48, 50),
               ("Hoplektor", 49, 50), ("Gelasable", 49, 50), ("Nemeleon", 50, 50), ("Hoplektor", 50, 50)]
LAK_NIGHT = [("Gelasable", 47, 49), ("Dorydrake", 47, 49), ("Hoplomex", 47, 49), ("Cairnolith", 47, 49),
             ("Gelasable", 48, 50), ("Dorydrake", 48, 50), ("Kerazap", 48, 50), ("Cairnolith", 48, 50),
             ("Hoplomex", 49, 50), ("Gelasable", 49, 50), ("Nemeleon", 50, 50), ("Dorydrake", 50, 50)]

ENTRIES = []
for tod in ("Morning", "Night"):
    ENTRIES.append({"map": "MAP_GYTHEION", "base_label": f"gGytheion_{tod}",
                    "water_mons": {"encounter_rate": 4, "mons": mons(HARBOR_SURF)},
                    "fishing_mons": {"encounter_rate": 30, "mons": mons(HARBOR_FISH)}})
    ENTRIES.append({"map": "MAP_ROUTE25_EUROTAS", "base_label": f"gRoute25_Eurotas_{tod}",
                    "land_mons": {"encounter_rate": 20, "mons": mons(R25_MORNING if tod == "Morning" else R25_NIGHT)},
                    "water_mons": {"encounter_rate": 4, "mons": mons(RIVER_SURF)},
                    "fishing_mons": {"encounter_rate": 30, "mons": mons(RIVER_FISH)}})
    ENTRIES.append({"map": "MAP_LAKONIA", "base_label": f"gLakonia_{tod}",
                    "land_mons": {"encounter_rate": 15, "mons": mons(LAK_MORNING if tod == "Morning" else LAK_NIGHT)},
                    "water_mons": {"encounter_rate": 4, "mons": mons(RIVER_SURF)},
                    "fishing_mons": {"encounter_rate": 30, "mons": mons(RIVER_FISH)}})


def main():
    data = json.loads(PATH.read_text())
    group = data["wild_encounter_groups"][0]
    labels = {e["base_label"] for e in ENTRIES}
    group["encounters"] = [e for e in group["encounters"] if e["base_label"] not in labels] + ENTRIES
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(ENTRIES)} tables")


if __name__ == "__main__":
    main()
