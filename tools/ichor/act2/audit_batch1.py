#!/usr/bin/env python3
"""Static checks across batch 1's maps, where one agent's map meets another's.

  python3 tools/ichor/act2/audit_batch1.py

Each agent tested its own maps; this checks the joins between them, from the
map.json files alone:
  - every warp leads to a map that exists and to a warp that exists there, and
    that warp leads back (doors are two-way);
  - every connection has its partner on the other map, opposite and with the
    negated offset (connections to maps not on this branch are listed, not failed);
  - no batch 1 map warps to, or respawns at, a Hoenn or FRLG map (BUILD.md:
    the Hoenn cut deletes them);
  - HEAL_LOCATION_THYRSA_CITY stands on the tile below a door into the Asclepeion;
  - every trainer id the batch's scripts battle is defined and has a party.
Prints one line per problem and exits 1 if there are any.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAPS = ROOT / "data/maps"
BATCH1 = [
    "Route6_EleutheraiRoad", "Route6_AntiopesCave", "Eleutherai", "Eleutherai_WatchHouse",
    "Eleutherai_OinoeHouse", "Eleutherai_LysidikeHouse", "MtKithairon", "Route7_KroniaGrounds",
    "ThyrsaCity", "ThyrsaCity_Asclepeion", "ThyrsaCity_Agora", "ThyrsaCity_Tavern",
    "ThyrsaCity_TempleOfDionysus", "ThyrsaCity_MaskWorkshop", "ThyrsaCity_ActorHouse",
    "ThyrsaCity_EudoraHouse", "ThyrsaCity_MantoHouse", "ThyrsaCity_PindarosHouse",
    "ThyrsaCity_SownHouse", "ThyrsaCity_VintnerHouse", "ThyrsaTheater", "ThyrsaTheater_Skene",
]
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}


def load(name):
    return json.loads((MAPS / name / "map.json").read_text())


def main():
    problems, notes = [], []
    by_id = {}
    for p in MAPS.glob("*/map.json"):
        d = json.loads(p.read_text())
        by_id[d["id"]] = (p.parent.name, d)
    ichor = set(json.loads((MAPS / "map_groups.json").read_text()).get("gMapGroup_IndoorThyrsa", []))
    ichor |= set(BATCH1)
    batch_ids = {load(n)["id"] for n in BATCH1}

    for name in BATCH1:
        d = load(name)
        for i, w in enumerate(d["warp_events"]):
            dest = w["dest_map"]
            where = f"{name} warp {i} ({w['x']},{w['y']})"
            if dest not in by_id:
                problems.append(f"{where}: {dest} doesn't exist")
                continue
            dname, dd = by_id[dest]
            if dest not in batch_ids and not dname.startswith(("Eleusa", "Elaia", "Akti", "Kalliste")):
                problems.append(f"{where}: leads out of the batch, to {dest} ({dname}): a Hoenn or FRLG map?")
            k = int(w["dest_warp_id"]) if str(w["dest_warp_id"]).isdigit() else None
            if k is None:
                notes.append(f"{where}: dynamic destination {w['dest_warp_id']}")
                continue
            if k >= len(dd["warp_events"]):
                problems.append(f"{where}: {dest} has no warp {k}")
                continue
            back = dd["warp_events"][k]["dest_map"]
            if back != d["id"]:
                problems.append(f"{where}: {dest} warp {k} leads to {back}, not back here")
        for c in d.get("connections") or []:
            other = c["map"]
            if other not in by_id:
                notes.append(f"{name}: connection {c['direction']} to {other}, not on this branch")
                continue
            oname, od = by_id[other]
            partner = [x for x in (od.get("connections") or [])
                       if x["map"] == d["id"] and x["direction"] == OPPOSITE[c["direction"]]]
            if not partner:
                problems.append(f"{name}: connection {c['direction']} to {other} has no partner on {oname}")
            elif int(partner[0]["offset"]) != -int(c["offset"]):
                problems.append(f"{name}: connection {c['direction']} to {other} offset {c['offset']}, "
                                f"but {oname}'s is {partner[0]['offset']} (should be {-int(c['offset'])})")

    heal = json.loads((ROOT / "src/data/heal_locations.json").read_text())
    entries = heal.get("heal_locations", heal) if isinstance(heal, dict) else heal
    thyrsa = [h for h in entries if h.get("id") == "HEAL_LOCATION_THYRSA_CITY"]
    if not thyrsa:
        problems.append("HEAL_LOCATION_THYRSA_CITY is missing")
    else:
        h = thyrsa[0]
        city = load("ThyrsaCity")
        doors = [w for w in city["warp_events"] if w["dest_map"] == "MAP_THYRSA_CITY_ASCLEPEION"]
        if h.get("map") != "MAP_THYRSA_CITY" or not any(w["x"] == h["x"] and w["y"] + 1 == h["y"] for w in doors):
            problems.append(f"HEAL_LOCATION_THYRSA_CITY at {h.get('map')} ({h.get('x')},{h.get('y')}) "
                            f"isn't below an Asclepeion door ({[(w['x'], w['y']) for w in doors]})")

    opp = (ROOT / "include/constants/opponents.h").read_text()
    party = (ROOT / "src/data/trainers.party").read_text()
    used = set()
    for name in BATCH1:
        used |= set(re.findall(r"TRAINER_ICHOR_[A-Z0-9_]+", (MAPS / name / "scripts.pory").read_text()))
    for t in sorted(used):
        if not re.search(rf"#define {t}\b", opp):
            problems.append(f"{t} is battled but not defined in opponents.h")
        elif f"=== {t} ===" not in party:
            problems.append(f"{t} has no party in src/data/trainers.party")

    for n in notes:
        print("NOTE", n)
    for p in problems:
        print("AUDIT FAIL:", p)
    if problems:
        sys.exit(1)
    print(f"AUDIT ok: {len(BATCH1)} maps, their warps and connections join up; {len(used)} trainers have parties")


if __name__ == "__main__":
    main()
