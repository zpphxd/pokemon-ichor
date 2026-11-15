#!/usr/bin/env python3
"""Halia's hut on Route 33, laid out from the oikia room catalog.

Every house is a home with a room of its own (design/MAP_DESIGN.md section 2).
Like Akti's homes (akti_homes.py, read it first), the room is composed with
tools/ichor/art/oikia_build.py's own composer from the pieces in oikia_art.py,
without recompiling gTileset_Oikia: every cell it uses must already be in the
tileset, and the build stops if one isn't.

  /usr/bin/python3 tools/ichor/maps/westsea_hut.py     # also run by westsea.py

Writes data/layouts/Route33_WesternSea_HaliasHut/{map,border}.bin, the layout's
size in layouts.json, the map's events in its map.json, and
design/postgame/img/route33_halias_hut.png (3x).
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))

import oikia_art as A  # noqa: E402
import oikia_build as B  # noqa: E402
import oikia_rooms as R  # noqa: E402

VOID = 0x0210   # oikia's near-black void, the room's border
LAYOUT = "Route33_WesternSea_HaliasHut"
LAYOUT_ID = "LAYOUT_ROUTE33_WESTERN_SEA_HALIAS_HUT"

# Halia is Kymon's grandmother, alone on her islet in the western sea. One low
# room under the thatch: the hearth in the middle of the back wall where she
# smokes fish, her nets and oars hung on the left, a model boat and the trident
# she was given on the right, her bed in the warm corner, and Kymon's pallet by
# the door. The back wall steps in on the left, where the roof comes down low.
HUT = {
    "title": "Halia's hut, Route 33",
    "map": "MAP_ROUTE33_WESTERN_SEA_HALIAS_HUT",
    "layout": LAYOUT,
    "floor": "boards",
    "wall": "blue",
    "grid": [
        "##WWWWWW",
        "WWWWWWWW",
        "WW......",
        "........",
        "........",
        "........",
        "........",
    ],
    "rugs": [("red", 3, 4, 2, 2)],
    "stamps": [
        ("nets", 0, 1),
        ("soot", 3, 0),
        ("hearth", 3, 2),
        ("boat", 5, 0),
        ("trident", 7, 0),
        ("fish_basket", 2, 2),
        ("pots", 6, 3),
        ("herbs", 2, 0),
        ("kline", 6, 4),
        ("pithos", 7, 2),
        ("amphora_plain", 1, 4),
        ("pots", 0, 6),
        ("kalathos", 2, 4),
        ("stool", 2, 5),
        ("mat", 3, 6),
    ],
    "spots": [
        ("warp", "door to Route 33 (south-arrow mat)", [(3, 6), (4, 6)]),
        ("npc", "Halia, at her hearth", (5, 3), "west"),
        ("npc", "Kymon, home (once towed)", (6, 6), "west"),
        ("bg", "the hearth: fish smoking over it", (3, 3), (3, 4, "north")),
        ("bg", "the model boat", (5, 1), (5, 2, "north")),
    ],
}


def build():
    base = dict(R.ROOMS)
    base.update(R.catalog(A.STAMPS))
    composed = {n: B.compose(s) for n, s in base.items()}
    order0, _ = B.collect(composed)
    hut = B.compose(HUT)
    composed["halias_hut"] = hut
    order, ids = B.collect(composed)
    if len(order) != len(order0):
        raise SystemExit(f"westsea_hut: the hut needs {len(order) - len(order0)} cells gTileset_Oikia "
                         "doesn't have; use pieces it has (oikia_rooms.catalog)")
    B.check_spots("halias_hut", HUT, hut)
    h, w = len(hut), len(hut[0])
    blocks = B.blockdata(hut, ids["halias_hut"])
    got = B.render_compiled(blocks, w, "gTileset_Aethos")
    if not np.array_equal(got, B.image_of(hut)):
        raise SystemExit("westsea_hut: the hut doesn't render from the compiled tileset as composed")
    d = ROOT / "data/layouts" / LAYOUT
    d.mkdir(parents=True, exist_ok=True)
    blocks.tofile(d / "map.bin")
    np.array([VOID] * 4, np.uint16).astype("<u2").tofile(d / "border.bin")
    layouts = ROOT / "data/layouts/layouts.json"
    data = json.loads(layouts.read_text())
    for lay in data["layouts"]:
        if lay.get("id") == LAYOUT_ID:
            lay.update({"width": w, "height": h, "primary_tileset": "gTileset_Aethos",
                        "secondary_tileset": "gTileset_Oikia"})
    layouts.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    out = ROOT / "design/postgame/img/route33_halias_hut.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    B.save_scaled(got, out, 3)
    write_events()
    print(f"westsea_hut: {w}x{h} -> data/layouts/{LAYOUT}, {out.relative_to(ROOT)}")


P = "Route33_WesternSea_HaliasHut_EventScript_"


def write_events():
    path = ROOT / "data/maps/Route33_WesternSea_HaliasHut/map.json"
    m = json.loads(path.read_text())

    def npc(gfx, x, y, script, facing, flag="0", local_id=None):
        o = {"graphics_id": gfx, "x": x, "y": y, "elevation": 3,
             "movement_type": f"MOVEMENT_TYPE_FACE_{facing.upper()}", "movement_range_x": 0,
             "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE",
             "trainer_sight_or_berry_tree_id": "0", "script": script, "flag": flag}
        return {"local_id": local_id, **o} if local_id else o

    def sign(x, y, script):
        return {"type": "sign", "x": x, "y": y, "elevation": 0,
                "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH", "script": script}

    m.update({
        "music": "MUS_ICHOR_TRIREME", "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_INDOOR",
        "show_map_name": False, "allow_cycling": False, "allow_running": True,
        "object_events": [
            npc("OBJ_EVENT_GFX_ICHOR_ELDER_F", 5, 3, P + "Halia", "left", local_id="LOCALID_HUT_HALIA"),
            # FLAG_TEMP_1 hides him until he's home (the map's ON_TRANSITION sets it)
            npc("OBJ_EVENT_GFX_ICHOR_FISHER", 6, 6, P + "Kymon", "left", flag="FLAG_TEMP_1",
                local_id="LOCALID_HUT_KYMON"),
        ],
        "warp_events": [
            {"x": 3, "y": 6, "elevation": 0, "dest_map": "MAP_ROUTE33_WESTERN_SEA", "dest_warp_id": "0"},
            {"x": 4, "y": 6, "elevation": 0, "dest_map": "MAP_ROUTE33_WESTERN_SEA", "dest_warp_id": "0"},
        ],
        "coord_events": [],
        "bg_events": [sign(3, 3, P + "Hearth"), sign(5, 1, P + "ModelBoat")],
    })
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    build()
