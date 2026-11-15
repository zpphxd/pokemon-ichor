"""Kirrha, Delphoi's harbor (MAP_KIRRHA, 36x30, aethos + kirrha). See harbors.py.

The plan, west to east:
  x 0-2    the gulf's west arm and a strip of shore under the cliffs (a dead end:
           a Hyper Potion where it stops)
  x 3-9    Apollo's plain, fenced, wild olives; the fence-watcher and the beggar
           lean on its east fence
  x 0-10   above it all the Phaidriades: the west cliff, the cleft with the sacred
           road's steps climbing to Delphoi's roofs and the Kastalian falls, the
           pilgrims' gate and its two guards, the east cliff
  x 11-19  Parnassos's grey crags (rows 6-9) under the olive slope
  x 20-24  Strophios's inn (warp 0) by the road down from the Split Road
  x 26-29  the road from Route 9 (columns 26-29 at the seam, verges 26 and 29)
  x 11-22  the muleteer's house and stable (warp 2) and the old sweeper's (warp 3)
           either side of the street (x 17-18)
  y 18-24  the quay: the fish market under the fig, the Kronist's crate, the
           Agora's shed (warp 1), the pilgrims, Panopeus's ferry at the east end
  x 28-35  a beach under the eastern hill (a Net Ball at its end)
  y 25-29  the gulf: the kaiki, a rowing boat, the rock in the bay (Big Pearl,
           with the Conch)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harbors as H  # noqa: E402
from harbors import (BOULDER, FALLS, FALLS_FOAM, FLOWERS, GRASS, SAND, SEA, STELE, Grid,  # noqa: E402
                     hashed, hidden, item_ball, obj, sign, trigger)

NAME, LAYOUT = "Kirrha", "LAYOUT_KIRRHA"
W, HGT = 36, 30
SEAM_ROWS = 6
SEAM_FROM_X = 11       # fieldmap.c copies Kirrha's columns 11+ across the Route 9 seam
NORTH_ROAD = range(26, 30)
S = "Kirrha_EventScript_"

# doors (fixed warp ids, BUILD.md): 0 inn, 1 Agora stall, 2 muleteer, 3 sweeper
INN_DOOR = (23, 9)
STALL_DOOR = (21, 20)
MULETEER_DOOR = (15, 15)
SWEEPER_DOOR = (21, 15)

# where scripted people stand
GUARDS = ((5, 9), (6, 9))
PANOPEUS = (23, 23)
ALETHEA = (16, 22)
ARRIVAL_TRIGGERS = tuple((x, 2) for x in range(26, 30))   # across the road from Route 9


def plan():
    """Ground plan: 'w' sea, 's' sand, 'r' road, 'q' quay, 'g' grass, 'o' trees,
    'p' Apollo's plain, 'B' a structure's footprint (placed afterwards)."""
    P = [["g"] * W for _ in range(HGT)]

    def box(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                P[y][x] = c
    box(11, 0, 25, 5, "o")          # the olive slope under Parnassos (aethos: the seam)
    box(30, 0, 35, 13, "o")         # the eastern hill
    box(26, 0, 26, 5, "g")
    box(29, 0, 29, 5, "g")
    box(27, 0, 28, 9, "r")          # the road from the Split Road
    box(2, 10, 28, 11, "r")         # the road along the foot of the crags
    box(5, 9, 6, 9, "r")            # the sacred road below the gate
    box(17, 12, 18, 20, "r")        # the street down to the quay
    box(13, 16, 16, 16, "r")        # the muleteer's doorstep path
    box(19, 16, 21, 16, "r")        # the sweeper's
    box(4, 13, 8, 19, "p")          # Apollo's plain
    box(0, 9, 0, 29, "w")           # the gulf's west arm
    box(1, 9, 1, 20, "w")
    box(2, 10, 2, 19, "s")          # the shore path under the plain
    box(3, 21, 27, 23, "q")         # the quay
    box(1, 21, 2, 29, "w")
    box(1, 24, 35, 29, "w")         # the gulf
    box(29, 16, 34, 21, "s")        # the beach
    box(28, 22, 35, 23, "w")
    box(35, 15, 35, 23, "w")
    box(28, 16, 28, 21, "g")
    return P


def compose():
    g = Grid("kirrha", W, HGT)
    P = plan()
    sea = {(x, y) for y in range(HGT) for x in range(W) if P[y][x] == "w"}
    # --- ground ---------------------------------------------------------
    roads = {(x, y) for y in range(HGT) for x in range(W) if P[y][x] == "r"}
    for (x, y) in sea:
        g.set(x, y, SEA, False, built=False)
    H.lay_path(g, roads)
    for y in range(HGT):
        for x in range(W):
            if P[y][x] == "s":
                g.set(x, y, SAND, False, built=False)
    # the sand's rim: the water cells round the beach and the shore path show its edge
    rim = {}
    for y in range(16, 22):
        rim[(35, y)] = "r"
    for x in range(29, 35):
        rim[(x, 22)] = "b"
    rim[(28, 22)] = "bl"
    rim[(35, 22)] = "br"
    rim[(35, 15)] = "tr"
    for y in range(10, 20):
        rim[(1, y)] = "l"
    rim[(1, 20)] = "bl"
    rim[(1, 9)] = "tl"
    H.sand_rim(g, rim)
    H.lay_quay(g, {(x, y) for y in range(HGT) for x in range(W) if P[y][x] == "q"}, sea)

    # --- the Phaidriades (columns 0-10, which Route 9 never draws) ----------
    # the west cliff runs on above the map; its east flank faces the cleft
    for y in range(0, 8):
        xr = 3 if y < 2 or y == 7 else 4
        for x in range(0, xr + 1):
            col = "r" if x == xr else ("m0" if x % 2 == 0 else "m1")
            g.put_part("cliff", f"{'faceA' if y % 2 == 0 else 'faceB'}_{col}", x, y)
    for x in range(0, 4):
        g.put_part("cliff", f"footB_{'r' if x == 3 else ('m0' if x % 2 == 0 else 'm1')}", x, 8)
    g.put("delphoi", 4, 0)
    for y in range(2, 7):
        for i in range(2):
            g.cell("cleft", i, (y - 2) % 2, 5 + i, y)
    for y in range(0, 6):
        g.set(7, y, FALLS, False)
    g.set(7, 6, FALLS_FOAM, False)
    for y in range(0, 7):          # the falls can't be climbed or surfed from the gate side
        g.solid[y, 7] = True
    g.put("gate", 4, 7)
    # the east cliff: its west flank to the falls, its east flank to the olive slope
    for y in range(0, 9):
        for x in range(8, 11):
            if x == 8:
                col = "l"
            elif x == 10 and y < 6:
                col = "r"
            else:
                col = "m0" if x % 2 == 0 else "m1"
            if y == 8 and x < 10:
                g.put_part("cliff", f"footB_{col}", x, y)
            else:
                g.put_part("cliff", f"{'faceA' if y % 2 == 0 else 'faceB'}_{col}", x, y)
    g.put_part("cliff", "footA_m0", 10, 9)
    # Parnassos's crags along the road, below the seam rows: higher where they
    # join the east cliff, stepping down eastward, scrub and olives on the steps
    for x in range(11, 20):
        col = "r" if x == 19 else ("m0" if x % 2 == 0 else "m1")
        if x <= 15:
            col = "r" if x == 15 else col
            g.put_part("cliff", f"rim_{col}" if x > 10 else f"faceB_{col}", x, 6)
            g.put_part("cliff", f"faceB_{col}", x, 7)
            g.put_part("cliff", f"faceA_{col}", x, 8)
            g.put_part("cliff", f"footA_{col}", x, 9)
        else:
            col = "l" if x == 16 else col
            g.put_part("cliff", f"rim_{col}", x, 7)
            g.put_part("cliff", f"faceA_{col}", x, 8)
            g.put_part("cliff", f"footA_{col}", x, 9)
    # rocks either side of the guards, so the gate is met head on
    g.set(4, 9, BOULDER, True)
    g.set(7, 9, BOULDER, True)
    g.set(8, 9, STELE, True)                 # the gate's notice
    g.set(9, 9, GRASS, False)
    g.set(2, 20, BOULDER, True)              # the shore path ends at a rock

    # --- the inn and the road down from Route 9 -------------------------------
    sys.path.insert(0, str(H.ROOT / "tools/ichor/art"))
    import kirrha_town as R
    g.recipe(R.RECIPES["inn"], 20, 6)
    g.put("laurel", 25, 7)
    g.set(26, 9, STELE, True)                # the town's sign by the road
    g.set(17, 6, FLOWERS, False)             # anemones on the crags' lower step

    # --- the households ---------------------------------------------------
    g.put("stable", 11, 14)
    g.recipe(R.RECIPES["muleteer"], 13, 13)
    g.recipe(R.RECIPES["sweeper"], 20, 13)
    g.put("laurel", 25, 12)
    # the sweeper's kitchen garden, and the boatyard by the beach
    for i, m in enumerate((0x103, 0x104, 0x105)):
        g.set(23 + i, 14, m, False)
    for i, m in enumerate((0x113, 0x114, 0x115)):
        g.set(23 + i, 15, m, False)
    g.put("upturned", 26, 17)
    # the beach: nets drying on poles, a boat hauled up, a rock
    g.put("net_poles", 30, 16)
    g.put("beached", 32, 19)
    g.set(29, 20, H.BOULDER_SAND, True)
    # the town's well at the head of the street
    g.put("well", 19, 12)
    # the quay's back: low dry-stone walls where it meets the town's grass
    for x0, x1 in ((10, 13), (23, 27)):
        for x in range(x0, x1 + 1):
            g.set(x, 20, 0x148 if x == x0 else (0x14A if x == x1 else 0x149), True)
    # sea rocks off the beach and in the bay
    g.set(32, 25, 0x18C, True)
    g.set(2, 26, 0x18C, True)
    g.set(17, 28, 0x18C, True)

    # --- Apollo's plain behind its fence ------------------------------------
    fence = lambda name, x, y: g.cell("fence", {"w": 0, "run": 1, "e": 2, "ns": 3, "sw": 4}[name], 0, x, y)
    for x in range(3, 10):
        fence("run", x, 12)
        fence("run", x, 20)
    for y in range(13, 20):
        fence("ns", 3, y)
        fence("ns", 9, y)
    fence("w", 3, 12)
    fence("e", 9, 12)
    fence("w", 3, 20)
    fence("e", 9, 20)
    for (x, y) in ((4, 13), (6, 14), (4, 16), (7, 17), (5, 18), (7, 13)):
        if g.free(x, y, 2, 2):
            g.olive(x, y)
    for y in range(13, 20):
        for x in range(4, 9):
            if g.free(x, y):
                g.set(x, y, FLOWERS if hashed(x, y, 3) < 0.25 else GRASS, False)  # fenced off

    # --- the waterfront ---------------------------------------------------
    g.put("fish_market", 14, 18)
    g.put("stall", 20, 18)
    g.put("kronist_crate", 19, 21)
    goods = lambda cx, cy, x, y: g.cell("quay_goods", cx, cy, x, y)
    goods(0, 0, 4, 21)                       # the net rack
    goods(1, 0, 5, 21)
    goods(3, 0, 7, 21)                       # the net heap
    goods(4, 0, 11, 21)                      # crates
    goods(5, 0, 12, 21)                      # rope
    goods(2, 1, 8, 21)                       # the octopus line
    goods(3, 1, 9, 21)
    goods(0, 1, 25, 21)                      # amphorae for the ferry
    goods(1, 1, 26, 21)
    goods(4, 1, 7, 22)                       # pilgrims' bundles
    goods(5, 1, 13, 22)
    g.cell("quay_steps", 1, 0, 10, 23)       # steps down into the gulf
    g.cell("quay_steps", 4, 0, 25, 22)       # the ferry's notice board
    g.put("ferry", 21, 24)
    g.put("kaiki", 4, 24)
    g.put("rowboat", 13, 24)
    g.put("bay_rock", 9, 26)

    # --- trees ------------------------------------------------------------
    zone = [(x, y) for y in range(HGT) for x in range(W) if P[y][x] == "o"]
    H.fill_trees(g, zone, salt=21)
    for (x, y) in ((23, 15), (24, 15), (25, 15)):
        pass
    # the north edge is shut but for the road and its verges: a gap in the olives
    # becomes a cypress or a rock
    for x in range(11, W):
        if x in NORTH_ROAD or g.solid[0, x]:
            continue
        if g.free(x, 0, 1, 2):
            g.cypress(x, 0)
        else:
            g.set(x, 0, BOULDER, True)
    g.put("laurel", 31, 14) if g.free(31, 14, 2, 2) else None
    for (x, y) in ((24, 16), (26, 13), (27, 13), (23, 17), (25, 11)):
        if g.free(x, y) and P[y][x] == "g":
            g.set(x, y, FLOWERS)
    for y in range(12, 21):
        for x in range(10, 35):
            if P[y][x] == "g" and g.free(x, y) and hashed(x, y, 13) < 0.12:
                g.set(x, y, FLOWERS)
    return g, P


def border():
    return [SEA, SEA, SEA, SEA]


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

def events():
    objects = [
        obj("LOCALID_KIRRHA_ALETHEA", "OBJ_EVENT_GFX_ICHOR_ALETHEA", *ALETHEA, S + "Alethea",
            flag="FLAG_ICHOR_HIDE_ALETHEA_KIRRHA", move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_KIRRHA_ALETHEA_GATE", "OBJ_EVENT_GFX_ICHOR_ALETHEA", 4, 11, S + "Alethea",
            flag="FLAG_TEMP_2", move="MOVEMENT_TYPE_FACE_UP"),
        obj("LOCALID_KIRRHA_ALETHEA_ROAD", "OBJ_EVENT_GFX_ICHOR_ALETHEA", 26, 3, S + "Alethea",
            flag="FLAG_TEMP_3", move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_KIRRHA_GUARD_1", "OBJ_EVENT_GFX_ICHOR_TEMPLE_GUARD", *GUARDS[0], S + "TempleGuard"),
        obj("LOCALID_KIRRHA_GUARD_2", "OBJ_EVENT_GFX_ICHOR_TEMPLE_GUARD", *GUARDS[1], S + "TempleGuard"),
        obj("LOCALID_KIRRHA_KRONIST", "OBJ_EVENT_GFX_ICHOR_KRONIST", 20, 21, S + "Kronist",
            move="MOVEMENT_TYPE_FACE_LEFT"),
        obj("LOCALID_KIRRHA_PANOPEUS", "OBJ_EVENT_GFX_ICHOR_PANOPEUS", *PANOPEUS, S + "Panopeus",
            move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_KIRRHA_PILGRIM_1", "OBJ_EVENT_GFX_ICHOR_PILGRIM_BLANKET", 6, 22, S + "Pilgrim1",
            move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_KIRRHA_PILGRIM_2", "OBJ_EVENT_GFX_ICHOR_PILGRIM_BLANKET_2", 12, 22, S + "Pilgrim2",
            move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_KIRRHA_PILGRIM_3", "OBJ_EVENT_GFX_ICHOR_PILGRIM_BLANKET_3", 19, 22, S + "Pilgrim3",
            move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_KIRRHA_FISHWIFE", "OBJ_EVENT_GFX_ICHOR_WOMAN", 16, 21, S + "Fishwife",
            move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_KIRRHA_BEGGAR", "OBJ_EVENT_GFX_ICHOR_ELDER_M", 10, 19, S + "Beggar",
            move="MOVEMENT_TYPE_FACE_RIGHT"),
        obj("LOCALID_KIRRHA_FENCE_WATCHER", "OBJ_EVENT_GFX_ICHOR_ELDER_M", 10, 16, S + "FenceWatcher",
            move="MOVEMENT_TYPE_FACE_LEFT"),
        item_ball("LOCALID_KIRRHA_ITEM_BIG_PEARL", 9, 26, "ITEM_BIG_PEARL",
                  "FLAG_ICHOR_ITEM_KIRRHA_BIG_PEARL"),
        item_ball("LOCALID_KIRRHA_ITEM_HYPER_POTION", 2, 19, "ITEM_HYPER_POTION",
                  "FLAG_ICHOR_ITEM_KIRRHA_HYPER_POTION"),
        item_ball("LOCALID_KIRRHA_ITEM_NET_BALL", 34, 16, "ITEM_NET_BALL",
                  "FLAG_ICHOR_ITEM_KIRRHA_NET_BALL"),
    ]
    warps = [("MAP_KIRRHA_INN", INN_DOOR), ("MAP_KIRRHA_AGORA", STALL_DOOR),
             ("MAP_KIRRHA_MULETEERS_HOUSE", MULETEER_DOOR), ("MAP_KIRRHA_SWEEPERS_HOUSE", SWEEPER_DOOR)]
    warp_events = [{"x": x, "y": y, "elevation": 0, "dest_map": m, "dest_warp_id": "0"}
                   for m, (x, y) in warps]
    coords = [trigger(x, y, "VAR_TEMP_1", 0, S + "Arrival") for (x, y) in ARRIVAL_TRIGGERS]
    bgs = [
        sign(26, 9, S + "TownSign"),
        sign(8, 9, S + "GateSign"),
        sign(9, 15, S + "FenceSign"),
        sign(25, 22, S + "FerrySign"),
        sign(10, 13, S + "DigFence"),           # ICHOR_STUB_DIG: the daily spot by the fence


        hidden(7, 9, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_KIRRHA_BRONZE_OBOL"),
        hidden(15, 19, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_KIRRHA_PEARL"),
        hidden(3, 23, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_KIRRHA_HEART_SCALE"),
    ]
    return objects, warp_events, coords, bgs


HEADER = {
    "layout": LAYOUT,
    # ICHOR_STUB_MUSIC: Part 9 gives Kirrha the road theme (630) until a town cue exists
    "music": "MUS_ICHOR_ROAD",
    "map_type": "MAP_TYPE_TOWN",
    "weather": "WEATHER_SUNNY",
    "allow_cycling": True, "allow_escaping": False, "allow_running": True,
    "show_map_name": True,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
    "connections": [{"map": "MAP_ROUTE9_SCHISTE", "offset": 18, "direction": "up"}],
}


def build():
    g, P = compose()
    H.write_layout(NAME, LAYOUT, g, border(), "gTileset_Kirrha")
    H.write_map_json(NAME, HEADER, *events())
    return g


SCREENS = {
    "1_north_road": (27, 4), "2_inn": (24, 9), "3_gate": (6, 6), "4_street": (17, 14),
    "5_quay_west": (8, 23), "6_quay_east": (21, 23), "7_plain": (6, 15), "8_beach": (30, 19),
}


def render(out_dir):
    return H.render(NAME, LAYOUT, out_dir, "kirrha", SCREENS)


def check(g):
    errors, reach, blocks = H.common_checks(
        g, NAME, (27, 0),
        unreachable_ok=("LOCALID_KIRRHA_ITEM_BIG_PEARL", "LOCALID_KIRRHA_ALETHEA_GATE",
                        "LOCALID_KIRRHA_ALETHEA_ROAD"),
        solid_ok=())
    # the seam: aethos only in the six rows nearest Route 9, from column 11 east
    for y in range(SEAM_ROWS):
        for x in range(SEAM_FROM_X, W):
            mid = int(blocks[y, x]) & 0x3FF
            if mid >= 0x200:
                errors.append(f"Kirrha: ({x},{y}) is kirrha metatile 0x{mid:03X} inside the seam strip")
    for x in range(W):
        open_ = H.walkable(blocks, x, 0)
        if open_ != (x in NORTH_ROAD):
            errors.append(f"Kirrha: north edge column {x} is {'open' if open_ else 'shut'}")
    # the gate holds: nothing north of the guards is reachable
    for y in range(0, 9):
        for x in range(0, 11):
            if (x, y) in reach:
                errors.append(f"Kirrha: ({x},{y}) behind the pilgrims' gate is reachable")
    # the Big Pearl's rock is reached only from the water
    if (9, 26) in reach:
        errors.append("Kirrha: the bay rock is reachable on foot")
    # the guards stand in the road's only two cells; the player meets them from below
    for (x, y) in GUARDS:
        if not H.walkable(blocks, x, y + 1):
            errors.append(f"Kirrha: no cell below the guard at ({x},{y})")
    for (x, y) in ((4, 9), (7, 9)):
        if H.walkable(blocks, x, y):
            errors.append(f"Kirrha: ({x},{y}) beside the guards is open")
    for (x, y) in ((4, 10), (4, 11), (7, 10), (7, 11)):
        if not H.walkable(blocks, x, y):
            errors.append(f"Kirrha: Alethea's way to the gate crosses solid ({x},{y})")
    # Alethea's walk on the quay
    for x in range(ALETHEA[0], ALETHEA[0] + 4):
        if not H.walkable(blocks, x, ALETHEA[1]):
            errors.append(f"Kirrha: Alethea's walk on the quay crosses solid ({x},{ALETHEA[1]})")
    return errors
