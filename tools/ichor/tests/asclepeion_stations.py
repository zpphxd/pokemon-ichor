#!/usr/bin/env python3
"""Check every civic Asclepeion uses the standard healer's station and Pithos.

FldEff_PokecenterHeal draws the Poke Balls at fixed screen offsets from the
player, so they only land in the spring basin when the basin sits exactly
where civic_rooms.station_cells puts it relative to the healer. This reads each
Asclepeion's map.json (the healer, the Pithos bg events) and its map.bin, and
fails on any cell that differs from the standard pieces.

  /usr/bin/python3 tools/ichor/tests/asclepeion_stations.py

Arkadia's Asclepeion is drawn from its own tileset (ArkadiaRooms) and is
checked by eye: its spring fountain and marked Pithos sit in the same places.
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import civic_tiles as ct  # noqa: E402
import civic_rooms as CR  # noqa: E402

CIVIC = ("gTileset_Civic", "gTileset_CivicKythera")
# Paphia's counter ends at the fountain's wall: its station stops at the
# healer's right-hand cell (no votives); the basin, relief and staff are the
# standard piece.
SHORT = {"KytheraPaphia_Asclepeion": {(1, -1), (2, -1), (1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (3, 1)}}


def main():
    ct.define()
    name_of = {ct.FIRST_ID + i: m["name"] for i, m in enumerate(ct.METATILES)}
    layouts = {l["id"]: l for l in json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"] if "id" in l}
    bad, seen = [], 0
    for mj in sorted(ROOT.glob("data/maps/*Asclepeion*/map.json")):
        m = json.loads(mj.read_text())
        lay = layouts[m["layout"]]
        if lay["secondary_tileset"] not in CIVIC:
            continue
        w, h = lay["width"], lay["height"]
        blocks = np.fromfile(ROOT / lay["blockdata_filepath"], "<u2").reshape(h, w) & 0x3FF
        mapname = mj.parent.name
        healers = [o for o in m["object_events"]
                   if o["script"].endswith(("_EventScript_Healer", "_EventScript_Phaedon"))]
        if len(healers) != 1:
            bad.append(f"{mapname}: {len(healers)} healers")
            continue
        hx, hy = healers[0]["x"], healers[0]["y"]
        skip = SHORT.get(mapname, set())
        for x, y, want in CR.station_cells(hx, hy):
            if (x - hx, y - hy) in skip:
                continue
            got = name_of.get(int(blocks[y, x]), hex(int(blocks[y, x])))
            if got != want:
                bad.append(f"{mapname}: ({x},{y}) is {got}, want {want}")
        pithos = sorted({(b["x"], b["y"]) for b in m["bg_events"] if b["script"].endswith("_Pithos")})
        if not pithos:
            bad.append(f"{mapname}: no Pithos bg event")
            continue
        px = pithos[0][0]
        for x, y, want in CR.pithos_cells(px):
            got = name_of.get(int(blocks[y, x]), hex(int(blocks[y, x])))
            if got != want:
                bad.append(f"{mapname}: Pithos ({x},{y}) is {got}, want {want}")
        if any(p[1] != 2 for p in pithos):
            bad.append(f"{mapname}: Pithos bg events {pithos} are not on its foot (row 2)")
        jars = [(x, y) for y in range(h) for x in range(w) if name_of.get(int(blocks[y, x]), "").startswith("asc_jar")]
        if jars:
            bad.append(f"{mapname}: small jars at {jars} can be taken for the Pithos")
        seen += 1
    for b in bad:
        print("STATIONS FAIL:", b)
    if bad or not seen:
        sys.exit(1)
    print(f"STATIONS PASS: {seen} civic Asclepeions use the standard station and Pithos")


if __name__ == "__main__":
    main()
