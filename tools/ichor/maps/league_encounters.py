#!/usr/bin/env python3
"""Write the Ascent's wild tables into src/data/wild_encounters.json.

BALANCE.md's League row: wild 52-58. Each floor's band is at most five levels
wide and climbs with the mountain. Only final forms appear (BALANCE.md's rule
for areas from Astyra on): the slopes' wolves and lions, the cloud's wind birds
and snow nymphs, the snowline's ghosts of the Styx's ice.

Usage: python3 tools/ichor/maps/league_encounters.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "src/data/wild_encounters.json"

TABLES = {
    "MAP_ASCENT_1F": dict(label="gAscent_1F", band=(52, 56), rate=12,
        Morning=["LYKANAX", "NEMELEON", "LAOLITH", "BASILOPS", "HOPLEKTOR", "KERASTORM"],
        Night=["LYKANAX", "HARPELLE", "STARKOS", "KAPRODON", "LAOLITH", "NEMELEON"]),
    "MAP_ASCENT_2F": dict(label="gAscent_2F", band=(54, 57), rate=12,
        Morning=["BORAPTERYX", "CHIONYAD", "LAOLITH", "KOLOSSARD", "GEOGRIP", "HOPLEKTOR"],
        Night=["BORAPTERYX", "STYGIAD", "HARPELLE", "KOLOSSARD", "GEOGRIP", "STARKOS"],
        rock=["LAOLITH", "KOLOSSARD", "GEOGRIP", "LAOLITH", "KOLOSSARD"]),
    "MAP_ASCENT_3F": dict(label="gAscent_3F", band=(55, 58), rate=12,
        Morning=["CHIONYAD", "BORAPTERYX", "KOLOSSARD", "LAOLITH", "KERASTORM", "HOPLEKTOR"],
        Night=["STYGIAD", "CHIONYAD", "BORAPTERYX", "HARPELLE", "KOLOSSARD", "STARKOS"],
        rock=["KOLOSSARD", "LAOLITH", "GEOGRIP", "KOLOSSARD", "LAOLITH"]),
}


def mons(species, band, n):
    lo, hi = band
    return [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + species[i % len(species)]} for i in range(n)]


def main():
    data = json.loads(PATH.read_text())
    group = data["wild_encounter_groups"][0]
    enc = [e for e in group["encounters"] if e.get("map") not in TABLES]
    for mapid, t in TABLES.items():
        for tod in ("Morning", "Night"):
            e = {"map": mapid, "base_label": f"{t['label']}_{tod}",
                 "land_mons": {"encounter_rate": t["rate"], "mons": mons(t[tod], t["band"], 12)}}
            if "rock" in t:
                e["rock_smash_mons"] = {"encounter_rate": 20, "mons": mons(t["rock"], t["band"], 5)}
            enc.append(e)
    group["encounters"] = enc
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
