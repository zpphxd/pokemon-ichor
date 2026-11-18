#!/usr/bin/env python3
"""Delphoi's wild tables (design/phase4/SCRIPT.md Part 4, "Delphoi's tables"):
Route 28's Sacred Olives and Kastalian Gorge, and Delphoi's laurel terraces and
pools, each with morning, day, evening and night tables. Levels are BALANCE's
Delphoi row (wild 48-52). Writes them into src/data/wild_encounters.json,
replacing any earlier copy.

  /usr/bin/python3 tools/ichor/maps/delphoi_encounters.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "src/data/wild_encounters.json"


def land(rate, slots):
    return {"encounter_rate": rate, "mons": [{"min_level": a, "max_level": b, "species": "SPECIES_" + s}
                                             for (s, a, b) in slots]}


# 12 slots: 20/20/10/10/10/10/5/5/4/4/1/1
OLIVES = {
    "Morning": [("MELIBEE", 48, 50), ("GALENYON", 48, 50), ("BASILOPS", 49, 51), ("MELISSEER", 49, 51),
                ("ELAPLING", 48, 50), ("GELASABLE", 49, 51), ("CAIRNOLITH", 49, 51), ("GALENYON", 50, 51),
                ("MELIBEE", 50, 51), ("BASILOPS", 50, 51), ("ENIGMAW", 51, 51), ("HIEROLIVE", 51, 51)],
    "Day": [("MELIBEE", 48, 50), ("BASILOPS", 48, 50), ("GALENYON", 49, 51), ("MELISSEER", 49, 51),
            ("ELAPLING", 48, 50), ("CAIRNOLITH", 49, 51), ("HARPELLE", 49, 51), ("MELIBEE", 50, 51),
            ("GALENYON", 50, 51), ("BASILOPS", 50, 51), ("ENIGMAW", 51, 51), ("HIEROLIVE", 51, 51)],
    "Evening": [("GELASABLE", 48, 50), ("MELIBEE", 48, 50), ("ELEKTEAR", 49, 51), ("SOPHOWL", 49, 51),
                ("ELAPLING", 48, 50), ("BASILOPS", 49, 51), ("CAIRNOLITH", 49, 51), ("GELASABLE", 50, 51),
                ("ELEKTEAR", 50, 51), ("SOPHOWL", 50, 51), ("ENIGMAW", 51, 51), ("HIEROLIVE", 51, 51)],
    "Night": [("GELASABLE", 48, 50), ("SOPHOWL", 48, 50), ("GELASABLE", 49, 51), ("CAIRNOLITH", 49, 51),
              ("ELAPLING", 48, 50), ("SOPHOWL", 49, 51), ("LYKANAX", 49, 51), ("GELASABLE", 50, 51),
              ("CAIRNOLITH", 50, 51), ("SOPHOWL", 50, 51), ("ELEKTEAR", 51, 51), ("HIEROLIVE", 51, 51)],
}
GORGE = {
    "Morning": [("MELIBEE", 48, 50), ("CAIRNOLITH", 48, 50), ("PYTHOROS", 49, 51), ("MELISSEER", 49, 51),
                ("BASILOPS", 49, 51), ("GALENYON", 49, 51), ("PYTHOROS", 50, 52), ("HYMNARIA", 50, 52),
                ("MELIBEE", 51, 52), ("CAIRNOLITH", 51, 52), ("ENIGMAW", 52, 52), ("ENIGMAW", 52, 52)],
    "Day": [("CAIRNOLITH", 48, 50), ("MELIBEE", 48, 50), ("BASILOPS", 49, 51), ("PYTHOROS", 49, 51),
            ("HARPELLE", 49, 51), ("MELISSEER", 49, 51), ("HYMNARIA", 50, 52), ("PYTHOROS", 50, 52),
            ("CAIRNOLITH", 51, 52), ("GALENYON", 51, 52), ("ENIGMAW", 52, 52), ("TAURIVET", 52, 52)],
    "Evening": [("MELIBEE", 48, 50), ("CAIRNOLITH", 48, 50), ("ELEKTEAR", 49, 51), ("SOPHOWL", 49, 51),
                ("PYTHOROS", 49, 51), ("GELASABLE", 49, 51), ("ELEKTEAR", 50, 52), ("HYMNARIA", 50, 52),
                ("CAIRNOLITH", 51, 52), ("GELASABLE", 51, 52), ("ENIGMAW", 52, 52), ("LYKANAX", 52, 52)],
    "Night": [("GELASABLE", 48, 50), ("CAIRNOLITH", 48, 50), ("SOPHOWL", 49, 51), ("ELEKTEAR", 49, 51),
              ("GELASABLE", 49, 51), ("LYKANAX", 49, 51), ("SOPHOWL", 50, 52), ("ELEKTEAR", 50, 52),
              ("CAIRNOLITH", 51, 52), ("HYMNARIA", 51, 52), ("PYTHOROS", 52, 52), ("LYKANAX", 52, 52)],
}
DELPHOI = {
    "Morning": [("MELIBEE", 48, 50), ("MELISSEER", 48, 50), ("HYMNARIA", 49, 51), ("BASILOPS", 49, 51),
                ("CAIRNOLITH", 49, 51), ("GALENYON", 49, 51), ("HYMNARIA", 50, 52), ("MELISSEER", 51, 52),
                ("MELIBEE", 51, 52), ("CAIRNOLITH", 51, 52), ("ENIGMAW", 52, 52), ("PYTHOROS", 52, 52)],
    "Day": [("MELISSEER", 48, 50), ("MELIBEE", 48, 50), ("BASILOPS", 49, 51), ("HYMNARIA", 49, 51),
            ("GALENYON", 49, 51), ("HARPELLE", 49, 51), ("MELISSEER", 50, 52), ("HYMNARIA", 51, 52),
            ("CAIRNOLITH", 51, 52), ("MELIBEE", 51, 52), ("ENIGMAW", 52, 52), ("CHELYRA", 52, 52)],
    "Evening": [("MELIBEE", 48, 50), ("ELEKTEAR", 48, 50), ("HYMNARIA", 49, 51), ("SOPHOWL", 49, 51),
                ("MELISSEER", 49, 51), ("GELASABLE", 49, 51), ("ELEKTEAR", 50, 52), ("MANTIPOD", 51, 52),
                ("MELIBEE", 51, 52), ("CAIRNOLITH", 51, 52), ("ENIGMAW", 52, 52), ("PYTHOROS", 52, 52)],
    "Night": [("MANTIPOD", 48, 50), ("SOPHOWL", 48, 50), ("MANTIPOD", 49, 51), ("GELASABLE", 49, 51),
              ("ELEKTEAR", 49, 51), ("CAIRNOLITH", 49, 51), ("MANTIPOD", 50, 52), ("SOPHOWL", 51, 52),
              ("GELASABLE", 51, 52), ("MANTIPOD", 51, 52), ("ELEKTEAR", 52, 52), ("PYRAPOD", 52, 52)],
}
# surfing the pools (5 slots: 60/30/5/4/1) and fishing (old 2, good 3, super 5)
SURF = [("HYMNARIA", 48, 51), ("GALENYON", 48, 51), ("HYMNARIA", 50, 52), ("GALENYON", 50, 52),
        ("KYNOKETOS", 52, 52)]
SURF_NIGHT = [("HYMNARIA", 48, 51), ("GALENYON", 48, 51), ("ELEKTEAR", 50, 52), ("HYMNARIA", 50, 52),
              ("KYNOKETOS", 52, 52)]
FISH = [("KETOFRY", 15, 19), ("KARKITOX", 20, 24), ("KETOFRY", 15, 19), ("KARKITOX", 48, 50),
        ("GALENYON", 48, 50), ("KARKITOX", 49, 52), ("KYNOKETOS", 50, 52), ("KARKITOX", 49, 52),
        ("KYNOKETOS", 50, 52), ("KYNOKETOS", 52, 52)]
FISH_NIGHT = [("KETOFRY", 15, 19), ("KARKITOX", 20, 24), ("KETOFRY", 15, 19), ("KARKITOX", 48, 50),
              ("ELEKTEAR", 48, 50), ("KARKITOX", 49, 52), ("KYNOKETOS", 50, 52), ("KARKITOX", 49, 52),
              ("KYNOKETOS", 50, 52), ("KYNOKETOS", 52, 52)]


def entries():
    out = []
    for (mapid, label, table, rate, water) in (
            ("MAP_ROUTE28_SACRED_OLIVES", "gRoute28SacredOlives", OLIVES, 20, False),
            ("MAP_ROUTE28_KASTALIAN_GORGE", "gRoute28KastalianGorge", GORGE, 20, True),
            ("MAP_DELPHOI", "gDelphoi", DELPHOI, 15, True)):
        for tod, slots in table.items():
            e = {"map": mapid, "base_label": f"{label}_{tod}", "land_mons": land(rate, slots)}
            if mapid == "MAP_ROUTE28_KASTALIAN_GORGE":
                e["rock_smash_mons"] = land(20, [("CAIRNOLITH", 48, 50), ("CAIRNOLITH", 49, 51),
                                                 ("ENIGMAW", 50, 52), ("PYTHOROS", 50, 52), ("TELKANVIL", 51, 52)])
            if water:
                night = tod == "Night"
                e["water_mons"] = land(4, SURF_NIGHT if night else SURF)
                e["fishing_mons"] = land(20, FISH_NIGHT if night else FISH)
            out.append(e)
    return out


def main():
    d = json.loads(P.read_text())
    group = next(g for g in d["wild_encounter_groups"] if g.get("for_maps"))
    mine = {"MAP_ROUTE28_SACRED_OLIVES", "MAP_ROUTE28_KASTALIAN_GORGE", "MAP_DELPHOI"}
    group["encounters"] = [e for e in group["encounters"] if e.get("map") not in mine] + entries()
    P.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
