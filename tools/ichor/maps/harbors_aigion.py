"""Aigion, the Achaean port across the gulf (MAP_AIGION, 28x24, aethos + aigion).
See harbors.py.

The plan, north to south:
  rows 0-2    the gulf: Helike's drowned roofs off the quay's west end, a kaiki,
              Panopeus's ferry alongside (shown once the gulf is crossed), a
              rowing boat
  rows 3-5    the quay; the fisher at its west end over the roofs
  rows 6-10   the street climbing south (x 12-14) past the old Achaean's narrow
              house (warp 0) and the goatherd's (warp 1), built against the grey
              crags of the hill; steps up onto the terrace
  rows 11-17  the grove of Zeus the Assembler: old planes in a ring round the
              altar, the grove-keeper (the healer) beside it
  rows 18-23  the road south into the Krathis gorge (Route 11, batch 3): columns
              12-15 at the seam (verges 12 and 15), aethos only
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harbors as H  # noqa: E402
from harbors import (BOULDER, FLOWERS, GRASS, SEA, STELE, Grid, hashed, hidden,  # noqa: E402
                     item_ball, obj, sign, trigger)

NAME, LAYOUT = "Aigion", "LAYOUT_AIGION"
W, HGT = 28, 24
SEAM_ROWS = 6
SOUTH_ROAD = range(12, 16)     # Route 11's road: 13-14, verges 12 and 15
S = "Aigion_EventScript_"

ACHAEAN_DOOR = (8, 9)
GOATHERD_DOOR = (19, 9)
ARRIVAL = (17, 4)              # the deck's landing warp puts the player here
PANOPEUS = (18, 3)
ALETHEA_QUAY = (16, 4)
ALETHEA_ROAD = (14, 22)
KEEPER = (12, 12)
ALTAR = (13, 13)


def plan():
    P = [["g"] * W for _ in range(HGT)]

    def box(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                P[y][x] = c
    box(0, 0, 27, 2, "w")
    box(0, 3, 0, 5, "w")
    box(27, 3, 27, 5, "w")
    box(1, 3, 26, 5, "q")
    box(12, 6, 14, 9, "r")          # the street
    box(8, 10, 11, 10, "r")         # the Achaean's doorstep path
    box(15, 10, 19, 10, "r")        # the goatherd's
    box(13, 18, 14, 23, "r")        # the road south
    box(12, 15, 15, 17, "r")        # the grove's floor south of the altar
    box(0, 6, 5, 23, "o")           # the hillsides
    box(22, 10, 27, 23, "o")
    box(6, 18, 11, 23, "o")
    box(16, 18, 21, 23, "o")
    box(12, 19, 12, 23, "g")
    box(15, 19, 15, 23, "g")
    return P


def compose():
    g = Grid("aigion", W, HGT)
    P = plan()
    sea = {(x, y) for y in range(HGT) for x in range(W) if P[y][x] == "w"}
    for (x, y) in sea:
        g.set(x, y, SEA, False, built=False)
    H.lay_path(g, {(x, y) for y in range(HGT) for x in range(W) if P[y][x] == "r"})
    H.lay_quay(g, {(x, y) for y in range(HGT) for x in range(W) if P[y][x] == "q"}, sea)
    # the gulf's furniture
    g.put("drowned", 3, 1)
    g.put("kaiki", 7, 1)
    g.put("ferry", 16, 0)
    g.put("rowboat", 23, 2)
    goods = lambda cx, cy, x, y: g.cell("quay_goods", cx, cy, x, y)
    goods(0, 0, 9, 5)                       # nets drying
    goods(1, 0, 10, 5)
    goods(4, 0, 22, 5)                      # crates
    goods(0, 1, 24, 5)                      # amphorae
    goods(1, 1, 25, 5)
    goods(5, 0, 26, 5)
    g.cell("quay_steps", 4, 0, 15, 5)       # the notice board
    g.cell("quay_steps", 2, 0, 5, 3)        # a bollard where the fisher stands
    # --- the households, and the hill the goatherd built against -----------
    sys.path.insert(0, str(H.ROOT / "tools/ichor/art"))
    import kirrha_town as R
    g.recipe(R.RECIPES["achaean"], 7, 6, kit="house_aigion", signs="house_signs_aigion")
    g.recipe(R.RECIPES["goatherd"], 17, 7, kit="house_aigion", signs="house_signs_aigion")
    for x in range(21, 27):
        col = "l" if x == 21 else ("r" if x == 26 else ("m0" if x % 2 == 0 else "m1"))
        g.put_part("cliff", f"rim_{col}", x, 6)
        g.put_part("cliff", f"faceA_{col}", x, 7)
        g.put_part("cliff", f"faceB_{col}", x, 8)
        g.put_part("cliff", f"footB_{col}", x, 9)
    g.put("rocks", 15, 7)
    # the terrace's lip: steps up from the street, a dry-stone wall either side
    for i, x in enumerate(range(12, 15)):
        g.cell("steps", i, 0, x, 10)
    for x in range(6, 12):
        if x not in (8, 9, 10, 11) or True:
            pass
    for x in list(range(6, 8)) + list(range(20, 22)):
        g.set(x, 10, 0x149, True)
    g.set(5, 10, 0x148, True)
    g.set(22, 10, 0x14A, True)
    # --- the grove of Zeus -------------------------------------------------
    g.put("plane", 8, 11)
    g.put("plane", 17, 11)
    g.put("plane", 6, 14)
    g.put("plane_hollow", 19, 14)
    g.put("plane", 9, 15) if g.free(9, 15, 3, 3) else None
    g.put("zeus_altar", *ALTAR)
    g.put("laurel", 16, 16) if g.free(16, 16, 2, 2) else None
    # --- the road south (seam rows: aethos only) ----------------------------
    g.set(16, 19, STELE, True)
    zone = [(x, y) for y in range(HGT) for x in range(W) if P[y][x] == "o"]
    H.fill_trees(g, zone, salt=33)
    for y in range(6, 18):
        for x in range(6, 22):
            if P[y][x] == "g" and g.free(x, y) and hashed(x, y, 17) < 0.14:
                g.set(x, y, FLOWERS)
    return g, P


def border():
    return [SEA, SEA, SEA, SEA]


def events():
    objects = [
        obj("LOCALID_AIGION_PANOPEUS", "OBJ_EVENT_GFX_ICHOR_PANOPEUS", *PANOPEUS, S + "Panopeus",
            flag="FLAG_TEMP_1", move="MOVEMENT_TYPE_FACE_UP"),
        obj("LOCALID_AIGION_ALETHEA_QUAY", "OBJ_EVENT_GFX_ICHOR_ALETHEA", *ALETHEA_QUAY, S + "AletheaRoad",
            flag="FLAG_TEMP_2", move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_AIGION_ALETHEA", "OBJ_EVENT_GFX_ICHOR_ALETHEA", *ALETHEA_ROAD, S + "AletheaRoad",
            flag="FLAG_ICHOR_HIDE_ALETHEA_AIGION", move="MOVEMENT_TYPE_FACE_UP"),
        obj("LOCALID_AIGION_GROVE_KEEPER", "OBJ_EVENT_GFX_ICHOR_PRIESTESS", *KEEPER, S + "GroveKeeper",
            move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_AIGION_FISHER", "OBJ_EVENT_GFX_ICHOR_FISHER", 4, 3, S + "Fisher",
            move="MOVEMENT_TYPE_FACE_UP"),
        obj("LOCALID_AIGION_CHILD", "OBJ_EVENT_GFX_ICHOR_KID_F", 13, 7, S + "Child",
            move="MOVEMENT_TYPE_WANDER_UP_AND_DOWN", ry=1),
    ]
    warps = [("MAP_AIGION_ACHAEANS_HOUSE", ACHAEAN_DOOR), ("MAP_AIGION_GOATHERDS_HOUSE", GOATHERD_DOOR)]
    warp_events = [{"x": x, "y": y, "elevation": 0, "dest_map": m, "dest_warp_id": "0"}
                   for m, (x, y) in warps]
    bgs = [
        sign(15, 5, S + "QuaySign"),
        sign(16, 19, S + "SouthSign"),
        sign(ALTAR[0], ALTAR[1] + 1, S + "Altar"),
        sign(ALTAR[0] + 1, ALTAR[1] + 1, S + "Altar"),
        sign(11, 16, S + "DigGrove"),            # ICHOR_STUB_DIG: the daily spot at the grove's edge
        hidden(20, 15, "ITEM_HONEY", "FLAG_ICHOR_HIDDEN_AIGION_HONEY"),
        hidden(1, 3, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_AIGION_PEARL"),
    ]
    return objects, warp_events, [], bgs


HEADER = {
    "layout": LAYOUT,
    # ICHOR_STUB_MUSIC: Part 9 gives Aigion the road theme (630) until a town cue exists
    "music": "MUS_ICHOR_ROAD",
    "map_type": "MAP_TYPE_TOWN",
    "weather": "WEATHER_SUNNY",
    "allow_cycling": True, "allow_escaping": False, "allow_running": True,
    "show_map_name": True,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
    "connections": None,     # Route 11 (batch 3) joins the south edge at columns 12-15
}


def build():
    g, P = compose()
    H.write_layout(NAME, LAYOUT, g, border(), "gTileset_Aigion")
    H.write_map_json(NAME, HEADER, *events())
    return g


SCREENS = {"1_quay": (13, 4), "2_street": (13, 8), "3_grove": (13, 14), "4_road_south": (13, 20),
           "5_drowned": (6, 4), "6_goatherd": (20, 9)}


def render(out_dir):
    return H.render(NAME, LAYOUT, out_dir, "aigion", SCREENS)


def check(g):
    errors, reach, blocks = H.common_checks(g, NAME, ARRIVAL)
    for y in range(HGT - SEAM_ROWS, HGT):
        for x in range(W):
            mid = int(blocks[y, x]) & 0x3FF
            if mid >= 0x200:
                errors.append(f"Aigion: ({x},{y}) is aigion metatile 0x{mid:03X} inside the seam strip")
    for x in range(W):
        open_ = H.walkable(blocks, x, HGT - 1)
        if open_ != (x in SOUTH_ROAD):
            errors.append(f"Aigion: south edge column {x} is {'open' if open_ else 'shut'}")
    if (KEEPER[0], KEEPER[1] + 1) not in reach:
        errors.append("Aigion: the heal tile in front of the grove-keeper can't be reached")
    return errors
