#!/usr/bin/env python3
"""Knossa's wild tables above ground, from design/phase4/SCRIPT.md Part 4 ("Knossa's
wild tables", "Fishing and water"): the Bull Road, the vineyard terraces, the
Bronze Heel, and Amnisos's and the Heel's water. Writes them into
src/data/wild_encounters.json, replacing any earlier copy of the same maps.

    python3 tools/ichor/maps/knossa_encounters.py
"""
import json
from pathlib import Path
import plan_hook  # noqa: E402  (tools/ichor/wild_plan.py)

ROOT = Path(__file__).resolve().parents[3]


def land(rows):
    return {"encounter_rate": RATE, "mons": [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + s.upper()}
                                             for (s, lo, hi) in rows]}


def table(rate, rows):
    return {"encounter_rate": rate, "mons": [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + s.upper()}
                                             for (s, lo, hi) in rows]}


ROAD_DAY = [("Taurivet", 42, 44), ("Melibee", 42, 44), ("Onotis", 42, 44), ("Kerazap", 42, 44),
            ("Galenyon", 42, 44), ("Cairnolith", 43, 45), ("Melisseer", 43, 45), ("Taurivet", 44, 45),
            ("Onotis", 44, 45), ("Kerazap", 44, 45), ("Kolossard", 45, 45), ("Ikaroth", 45, 45)]
ROAD_NIGHT = [("Gelasable", 42, 44), ("Sophowl", 42, 44), ("Taurivet", 42, 44), ("Onotis", 42, 44),
              ("Kalyptor", 42, 44), ("Cairnolith", 43, 45), ("Gelasable", 44, 45), ("Sophowl", 44, 45),
              ("Kalyptor", 44, 45), ("Onotis", 44, 45), ("Amnoze", 45, 45), ("Midonos", 45, 45)]
VINE_DAY = [("Thyrsivy", 43, 45), ("Onotis", 43, 45), ("Melibee", 43, 45), ("Melisseer", 43, 45),
            ("Gelasable", 43, 45), ("Midonos", 43, 45), ("Thyrsivy", 44, 45), ("Onotis", 44, 45),
            ("Korantha", 44, 45), ("Melisseer", 44, 45), ("Korantha", 45, 45), ("Kerazap", 45, 45)]
VINE_NIGHT = [("Oinopard", 43, 45), ("Gelasable", 43, 45), ("Thyrsivy", 43, 45), ("Sophowl", 43, 45),
              ("Onotis", 43, 45), ("Midonos", 43, 45), ("Oinopard", 44, 45), ("Kalyptor", 44, 45),
              ("Persenyx", 44, 45), ("Thyrsivy", 44, 45), ("Persenyx", 45, 45), ("Amnoze", 45, 45)]
HEEL_DAY = [("Kolossette", 43, 45), ("Galenyon", 43, 45), ("Karkitox", 43, 45), ("Taurivet", 43, 45),
            ("Cairnolith", 43, 45), ("Onotis", 43, 45), ("Taurivet", 44, 45), ("Ikaroth", 44, 45),
            ("Kolossard", 44, 45), ("Galenyon", 44, 45), ("Kolossard", 45, 45), ("Telkanvil", 45, 45)]
HEEL_NIGHT = [("Kolossette", 43, 45), ("Karkitox", 43, 45), ("Gelasable", 43, 45), ("Kalyptor", 43, 45),
              ("Cairnolith", 43, 45), ("Sophowl", 43, 45), ("Karkitox", 44, 45), ("Kolossette", 44, 45),
              ("Gelasable", 44, 45), ("Cairnolith", 44, 45), ("Telkanvil", 45, 45), ("Kalyptor", 45, 45)]
WATER = [("Galenyon", 43, 45), ("Karkitox", 43, 45), ("Narkeray", 44, 45), ("Telkanvil", 45, 45),
         ("Kynoketos", 45, 45)]
FISH_AMNISOS = [("Ketofry", 42, 44), ("Karkitox", 42, 44), ("Karkitox", 43, 45), ("Narkeray", 43, 45),
                ("Ketofry", 43, 45), ("Narkeray", 44, 46), ("Telkanvil", 44, 46), ("Karkitox", 45, 46),
                ("Kynoketos", 46, 46), ("Kynoketos", 46, 46)]
FISH_HEEL = [("Ketofry", 42, 44), ("Karkitox", 42, 44), ("Narkeray", 43, 45), ("Karkitox", 43, 45),
             ("Ketofry", 43, 45), ("Telkanvil", 44, 46), ("Kynoketos", 45, 46), ("Narkeray", 44, 46),
             ("Kynoketos", 46, 46), ("Telkanvil", 46, 46)]

ENTRIES = [
    ("MAP_KNOSSA_AMNISOS", "gKnossaAmnisos", {"Morning": {"water_mons": table(4, WATER),
                                                           "fishing_mons": table(30, FISH_AMNISOS)}}),
    ("MAP_KNOSSA_BULL_ROAD", "gKnossaBullRoad", {"Morning": {"land_mons": table(20, ROAD_DAY)},
                                                  "Night": {"land_mons": table(20, ROAD_NIGHT)}}),
    ("MAP_KNOSSA_BULL_ROAD_VINEYARD", "gKnossaBullRoadVineyard",
     {"Morning": {"land_mons": table(25, VINE_DAY)}, "Night": {"land_mons": table(25, VINE_NIGHT)}}),
    ("MAP_KNOSSA_BRONZE_HEEL", "gKnossaBronzeHeel",
     {"Morning": {"land_mons": table(20, HEEL_DAY), "water_mons": table(4, WATER),
                  "fishing_mons": table(30, FISH_HEEL)},
      "Night": {"land_mons": table(20, HEEL_NIGHT), "water_mons": table(4, WATER),
                "fishing_mons": table(30, FISH_HEEL)}}),
]


def main():
    p = ROOT / "src/data/wild_encounters.json"
    w = json.loads(p.read_text())
    g = w["wild_encounter_groups"][0]
    ours = {e[0] for e in ENTRIES}
    g["encounters"] = [e for e in g["encounters"] if e.get("map") not in ours]
    for (mp, label, times) in ENTRIES:
        for t, fields in times.items():
            g["encounters"].append({"map": mp, "base_label": f"{label}_{t}", **fields})
    plan_hook.apply(g["encounters"])  # the distribution pass has the last word (design/DISTRIBUTION.md)
    p.write_text(json.dumps(w, indent=2, ensure_ascii=False) + "\n")
    print("wrote", sum(len(t) for (_, _, t) in ENTRIES), "tables")


if __name__ == "__main__":
    main()
