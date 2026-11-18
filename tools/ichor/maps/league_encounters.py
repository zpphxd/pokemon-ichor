#!/usr/bin/env python3
"""Write the Ascent's wild tables into src/data/wild_encounters.json.

BALANCE.md's League row, raised in the endgame upgrade (2026-11-17): wild
54-64, each floor's band at most five levels wide and climbing with the
mountain. The tables turn colder floor by floor (design/IDEAS.md, the Ascent
of Olympus): Niflake and Kryopuff in the Icefall's caves, Chionyad and
Borapteryx on the ice, Krystolos in the crystal caves, Pagoshard on the
glacier (its first wild home), Stygiad in the coldest dark, and their evolved
forms commonest near the peak. First stages sit in the rare slots
(BALANCE.md: late areas show final forms, first stages only in rare spots).

Twelve land slots, Emerald's odds: 20 20 10 10 10 10 5 5 4 4 1 1.

Usage: python3 tools/ichor/maps/league_encounters.py
"""
import json
from pathlib import Path

import water_tables as W

ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "src/data/wild_encounters.json"

TABLES = {
    "MAP_ASCENT_1F": dict(label="gAscent_1F", band=(54, 58), rate=12,
        Morning=["LYKANAX", "NEMELEON", "LAOLITH", "BASILOPS", "HOPLEKTOR", "KERASTORM",
                 "LYKANAX", "NEMELEON", "LAOLITH", "BASILOPS", "HOPLEKTOR", "KERASTORM"],
        Night=["LYKANAX", "HARPELLE", "STARKOS", "KAPRODON", "LAOLITH", "NEMELEON",
               "LYKANAX", "HARPELLE", "STARKOS", "KAPRODON", "LAOLITH", "NEMELEON"]),
    "MAP_ASCENT_2F": dict(label="gAscent_2F", band=(55, 59), rate=12,
        Morning=["BORAPTERYX", "CHIONYAD", "LAOLITH", "KOLOSSARD", "GEOGRIP", "HOPLEKTOR",
                 "BORAPTERYX", "CHIONYAD", "LAOLITH", "KOLOSSARD", "KRYOPUFF", "NIFLAKE"],
        Night=["BORAPTERYX", "STYGIAD", "HARPELLE", "KOLOSSARD", "GEOGRIP", "STARKOS",
               "BORAPTERYX", "STYGIAD", "HARPELLE", "KOLOSSARD", "NIFLAKE", "KRYOPUFF"],
        rock=["LAOLITH", "KOLOSSARD", "GEOGRIP", "LAOLITH", "KOLOSSARD"]),
    "MAP_ASCENT_ICEFALL": dict(label="gAscent_Icefall", band=(57, 61), rate=7,
        Morning=["BORAPTERYX", "CHIONYAD", "KOLOSSARD", "CHIONYAD", "BORAPTERYX", "LAOLITH",
                 "KRYSTOLOS", "GEOGRIP", "NIFLAKE", "KRYOPUFF", "NIFLAKE", "KRYOPUFF"],
        Night=["STYGIAD", "CHIONYAD", "BORAPTERYX", "KOLOSSARD", "STYGIAD", "CHIONYAD",
               "KRYSTOLOS", "HARPELLE", "NIFLAKE", "KRYOPUFF", "NIFLAKE", "KRYOPUFF"],
        rock=["KRYSTOLOS", "PAGOSHARD", "LAOLITH", "GEOGRIP", "PAGOSHARD"]),
    "MAP_ASCENT_ICEFALL_DEEP": dict(label="gAscent_IcefallDeep", band=(59, 63), rate=8,
        Morning=["STYGIAD", "STYGIAD", "KRYSTOLOS", "CHIONYAD", "STYGIAD", "KOLOSSARD",
                 "KRYSTOLOS", "PERSENYX", "NIFLAKE", "STYGIAD", "KRYOPUFF", "NIFLAKE"],
        Night=["STYGIAD", "STYGIAD", "KRYSTOLOS", "PERSENYX", "STYGIAD", "CHIONYAD",
               "KRYSTOLOS", "HARPELLE", "NIFLAKE", "STYGIAD", "KRYOPUFF", "NIFLAKE"]),
    "MAP_ASCENT_CRYSTAL_VAULT": dict(label="gAscent_CrystalVault", band=(60, 63), rate=5,
        Morning=["KRYSTOLOS", "CHIONYAD", "KRYSTOLOS", "PAGOSHARD", "CHIONYAD", "KRYSTOLOS",
                 "PAGOSHARD", "STYGIAD", "NIFLAKE", "PAGOSHARD", "KRYOPUFF", "NIFLAKE"],
        Night=["KRYSTOLOS", "STYGIAD", "KRYSTOLOS", "PAGOSHARD", "CHIONYAD", "STYGIAD",
               "PAGOSHARD", "KRYSTOLOS", "NIFLAKE", "PAGOSHARD", "KRYOPUFF", "NIFLAKE"]),
    "MAP_ASCENT_GLACIER": dict(label="gAscent_Glacier", band=(58, 62), rate=8,
        Morning=["CHIONYAD", "BORAPTERYX", "PAGOSHARD", "KRYSTOLOS", "BORAPTERYX", "CHIONYAD",
                 "KERASTORM", "KOLOSSARD", "PAGOSHARD", "KRYOPUFF", "PAGOSHARD", "NIFLAKE"],
        Night=["STYGIAD", "BORAPTERYX", "CHIONYAD", "KRYSTOLOS", "PAGOSHARD", "STYGIAD",
               "HARPELLE", "KOLOSSARD", "PAGOSHARD", "NIFLAKE", "PAGOSHARD", "KRYOPUFF"]),
    "MAP_ASCENT_3F": dict(label="gAscent_3F", band=(60, 64), rate=6,
        Morning=["KRYSTOLOS", "BORAPTERYX", "CHIONYAD", "KERASTORM", "HOPLEKTOR", "BORAPTERYX",
                 "KRYSTOLOS", "CHIONYAD", "BORAPTERYX", "KRYSTOLOS", "AETARCH", "CHIONYAD"],
        Night=["STYGIAD", "KRYSTOLOS", "CHIONYAD", "BORAPTERYX", "HARPELLE", "KRYSTOLOS",
               "STYGIAD", "CHIONYAD", "BORAPTERYX", "STARKOS", "KRYSTOLOS", "STYGIAD"]),
}


def glacial(L):
    """The mountain's cold water: the tarn under the Icefall, the glacier's melt
    pool. Kynoketos and Galenyon, Stygiad in the black water, Dakrock rare."""
    return W._table(
        [("KYNOKETOS", L, L + 2), ("STYGIAD", L, L + 2), ("GALENYON", L + 1, L + 3),
         ("STYGIAD", L + 2, L + 3), ("DAKROCK", L + 3, L + 4)],
        [("KYNOKETOS", L - 2, L), ("GALENYON", L - 2, L),
         ("KYNOKETOS", L, L + 2), ("GALENYON", L, L + 2), ("STYGIAD", L, L + 2),
         ("KYNOKETOS", L + 2, L + 4), ("GALENYON", L + 2, L + 4), ("STYGIAD", L + 2, L + 4),
         ("DAKROCK", L + 3, L + 4), ("DAKROCK", L + 4, L + 4)], fish_rate=20)


WATER = {"MAP_ASCENT_ICEFALL": glacial(57), "MAP_ASCENT_ICEFALL_DEEP": glacial(59),
         "MAP_ASCENT_GLACIER": glacial(58)}


def mons(species, band):
    lo, hi = band
    return [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + s} for s in species]


def main():
    data = json.loads(PATH.read_text())
    group = data["wild_encounter_groups"][0]
    enc = [e for e in group["encounters"] if e.get("map") not in TABLES]
    for mapid, t in TABLES.items():
        for tod in ("Morning", "Night"):
            e = {"map": mapid, "base_label": f"{t['label']}_{tod}",
                 "land_mons": {"encounter_rate": t["rate"], "mons": mons(t[tod], t["band"])}}
            if "rock" in t:
                e["rock_smash_mons"] = {"encounter_rate": 20, "mons": mons(t["rock"], t["band"])}
            if tod == "Morning" and mapid in WATER:
                e.update(json.loads(json.dumps(WATER[mapid])))
            enc.append(e)
    W.apply(enc, {"MAP_ASCENT_1F", "MAP_ASCENT_2F"})  # the springs
    group["encounters"] = enc
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
