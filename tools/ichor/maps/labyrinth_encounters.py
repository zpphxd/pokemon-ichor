#!/usr/bin/env python3
"""Wild tables for the Labyrinth's upper rings (design/phase4/SCRIPT.md, "The
Labyrinth's rings"; LABYRINTH_MAZE.md §5: the wild things live in the cave, the
built corridors stay quiet, so only the cave's earth (MB_CAVE) and its stream
call these). Writes them into src/data/wild_encounters.json, replacing any
earlier entry for the same map and label.

  /usr/bin/python3 tools/ichor/maps/labyrinth_encounters.py
"""
import json
from pathlib import Path
import plan_hook  # noqa: E402  (tools/ichor/wild_plan.py)

ROOT = Path(__file__).resolve().parents[3]
J = ROOT / "src/data/wild_encounters.json"


def land(rows, rate=8):
    return {"encounter_rate": rate,
            "mons": [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + s.upper()} for s, lo, hi in rows]}


R1 = [("Mitoclew", 44, 46), ("Cairnolith", 44, 46), ("Kalyptor", 44, 46), ("Kolossette", 44, 46),
      ("Plouteras", 44, 46), ("Mitoclew", 44, 46), ("Cairnolith", 45, 46), ("Kalyptor", 45, 46),
      ("Kolossette", 45, 46), ("Plouteras", 45, 46), ("Kolossard", 46, 46), ("Kourodin", 46, 46)]
R2 = [("Mitoclew", 44, 46), ("Kalyptor", 44, 46), ("Cairnolith", 44, 46), ("Hyphantis", 44, 46),
      ("Kolossette", 44, 46), ("Plouteras", 44, 46), ("Mitoclew", 45, 46), ("Kalyptor", 45, 46),
      ("Cairnolith", 45, 46), ("Hyphantis", 45, 46), ("Taurivet", 46, 46), ("Kolossard", 46, 46)]
R2N = [("Mitoclew", 44, 46), ("Kalyptor", 44, 46), ("Cairnolith", 44, 46), ("Hyphantis", 44, 46),
       ("Kolossette", 44, 46), ("Plouteras", 44, 46), ("Amnoze", 45, 46), ("Kalyptor", 45, 46),
       ("Mitoclew", 45, 46), ("Hyphantis", 45, 46), ("Amnoze", 46, 46), ("Taurivet", 46, 46)]
R3 = [("Hyphantis", 45, 47), ("Kalyptor", 45, 47), ("Persenyx", 45, 47), ("Mitoclew", 45, 47),
      ("Plouteras", 45, 47), ("Hyphantis", 45, 47), ("Kalyptor", 46, 47), ("Persenyx", 46, 47),
      ("Mitoclew", 46, 47), ("Plouteras", 46, 47), ("Kolossette", 47, 47), ("Kolossard", 47, 47)]
R4 = [("Cairnolith", 45, 47), ("Plouteras", 45, 47), ("Kolossette", 45, 47), ("Mitoclew", 45, 47),
      ("Cairnolith", 45, 47), ("Plouteras", 45, 47), ("Kolossette", 46, 47), ("Mitoclew", 46, 47),
      ("Cairnolith", 46, 47), ("Plouteras", 46, 47), ("Kaprodon", 47, 47), ("Geogrip", 47, 47)]
# the underground stream (Rings II-IV): what lives in cold dark water
WATER = [("Kalyptor", 44, 47), ("Mitoclew", 44, 47), ("Plouteras", 45, 47), ("Kalyptor", 46, 47),
         ("Persenyx", 47, 47)]
FISH = [("Plouteras", 40, 44), ("Mitoclew", 40, 44), ("Plouteras", 42, 45), ("Kalyptor", 44, 46),
        ("Persenyx", 44, 46), ("Plouteras", 45, 47), ("Kalyptor", 45, 47), ("Mitoclew", 46, 47),
        ("Persenyx", 46, 47), ("Kolossette", 47, 47)]

# rubble the Hammer breaks: what hides in fallen masonry
ROCK = [("Cairnolith", 44, 47), ("Mitoclew", 44, 47), ("Cairnolith", 45, 47), ("Kolossette", 46, 47),
        ("Geogrip", 47, 47)]
TOMB = [("Kalyptor", 46, 48), ("Mitoclew", 46, 48), ("Persenyx", 46, 48), ("Kalyptor", 47, 48),
        ("Mitoclew", 47, 48), ("Persenyx", 47, 48), ("Kalyptor", 48, 48), ("Lykanax", 47, 48),
        ("Persenyx", 48, 48), ("Mitoclew", 48, 48), ("Lykanax", 48, 48), ("Kolossard", 48, 48)]

# the heart (Rings V-VII; SCRIPT.md Part 4's tables, the Labyrinth II build)
R5 = [("Kalyptor", 46, 48), ("Mitoclew", 46, 48), ("Lykanax", 46, 48), ("Hyphantis", 46, 48),
      ("Plouteras", 46, 48), ("Kalyptor", 46, 48), ("Lykanax", 47, 48), ("Mitoclew", 47, 48),
      ("Hyphantis", 47, 48), ("Cairnolith", 47, 48), ("Kaprodon", 48, 48), ("Persenyx", 48, 48)]
R6 = [("Kolossette", 46, 48), ("Taurivet", 46, 48), ("Gigantomb", 46, 48), ("Cairnolith", 46, 48),
      ("Kolossette", 46, 48), ("Taurivet", 46, 48), ("Gigantomb", 47, 48), ("Kourodin", 47, 48),
      ("Kolossard", 47, 48), ("Kolossette", 47, 48), ("Kolossard", 48, 48), ("Gigantomb", 48, 48)]
R7 = [("Sophowl", 47, 49), ("Mitoclew", 47, 49), ("Psychora", 47, 49), ("Chelyra", 47, 49),
      ("Melisseer", 47, 49), ("Sophowl", 47, 49), ("Mitoclew", 48, 49), ("Psychora", 48, 49),
      ("Chelyra", 48, 49), ("Melisseer", 48, 49), ("Kerastorm", 49, 49), ("Amnoze", 49, 49)]
R7N = [("Sophowl", 47, 49), ("Mitoclew", 47, 49), ("Psychora", 47, 49), ("Chelyra", 47, 49),
       ("Amnoze", 47, 49), ("Sophowl", 47, 49), ("Mitoclew", 48, 49), ("Psychora", 48, 49),
       ("Chelyra", 48, 49), ("Amnoze", 48, 49), ("Amnoze", 49, 49), ("Kerastorm", 49, 49)]

TABLES = {
    ("MAP_LABYRINTH_RING1", "Morning"): {"rock_smash_mons": land(ROCK, 20), "land_mons": land(R1)},
    ("MAP_LABYRINTH_RING2", "Morning"): {"rock_smash_mons": land(ROCK, 20), "land_mons": land(R2), "water_mons": land(WATER, 4),
                                         "fishing_mons": land(FISH, 20)},
    ("MAP_LABYRINTH_RING2", "Night"): {"rock_smash_mons": land(ROCK, 20), "land_mons": land(R2N), "water_mons": land(WATER, 4),
                                       "fishing_mons": land(FISH, 20)},
    ("MAP_LABYRINTH_RING3", "Morning"): {"rock_smash_mons": land(ROCK, 20), "land_mons": land(R3, 10), "water_mons": land(WATER, 4),
                                         "fishing_mons": land(FISH, 20)},
    ("MAP_LABYRINTH_RING4", "Morning"): {"rock_smash_mons": land(ROCK, 20), "land_mons": land(R4, 6), "water_mons": land(WATER, 4),
                                         "fishing_mons": land(FISH, 20)},
    # Rings V and VI: the same stream fills the cisterns around the heart
    ("MAP_LABYRINTH_RING5", "Morning"): {"land_mons": land(R5, 10), "rock_smash_mons": land(ROCK, 20),
                                         "water_mons": land(WATER, 4), "fishing_mons": land(FISH, 20)},
    ("MAP_LABYRINTH_RING6", "Morning"): {"land_mons": land(R6, 8), "rock_smash_mons": land(ROCK, 20),
                                         "water_mons": land(WATER, 4), "fishing_mons": land(FISH, 20)},
    ("MAP_LABYRINTH_RING7", "Morning"): {"land_mons": land(R7, 10), "rock_smash_mons": land(ROCK, 20)},
    ("MAP_LABYRINTH_RING7", "Night"): {"land_mons": land(R7N, 10), "rock_smash_mons": land(ROCK, 20)},
    ("MAP_LABYRINTH_MINOS_TOMB", "Morning"): {"land_mons": land(TOMB, 4)},
    ("MAP_LABYRINTH_CELLARS", "Morning"): {"land_mons": land(TOMB, 6)},
}


def main(maps=None):
    d = json.loads(J.read_text())
    enc = d["wild_encounter_groups"][0]["encounters"]
    for (mp, when), t in TABLES.items():
        if maps and mp not in maps:
            continue
        name = "".join(w.capitalize() for w in mp[4:].split("_"))
        label = f"g{name}_{when}"
        enc[:] = [e for e in enc if e.get("base_label") != label]
        enc.append({"map": mp, "base_label": label, **t})
    plan_hook.apply(enc)  # the distribution pass has the last word (design/DISTRIBUTION.md)
    J.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    import sys
    main(sys.argv[1:] or None)
