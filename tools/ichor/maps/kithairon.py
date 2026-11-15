#!/usr/bin/env python3
"""Build the Kithairon crossing: Route 6, Antiope's cave, Eleutherai, Mt. Kithairon
and Route 7 with the Kronia grounds (design/phase3/SCRIPT.md beats 26-29).

Each map is drawn below in code: a ground grid (tools/ichor/maps/kithairon_lib.py
has the legend) carved out of woods and rock, then stamped with the tilesets'
structures, then auto-tiled. It writes:

  data/layouts/<Map>/{map,border}.bin and the layouts' entries in layouts.json
  data/maps/<Map>/map.json: events, connections and music
  build/render/kithairon/<Map>.png, _review.png (collision and events) and
  _screens.png (15 x 10 GBA screens along the road)
  design/phase3/img/<Map>.png (2x), for the director

Usage:
  /usr/bin/python3 tools/ichor/maps/kithairon.py            # build every map
  /usr/bin/python3 tools/ichor/maps/kithairon.py --shapes   # list the soft-ground
      shapes the maps use in tools/ichor/art/kithairon_shapes.json; then rebuild the
      tilesets (tools/ichor/art/kithairon_build.py) and run this again
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kithairon_lib as L  # noqa: E402
from kithairon_lib import ROOT, Map, item_ball, obj, sign, trigger, warp  # noqa: E402

IMG = ROOT / "design/phase3/img"
P = "OBJ_EVENT_GFX_ICHOR_"
R6 = "Route6_EleutheraiRoad_EventScript_"
EL = "Eleutherai_EventScript_"
MK = "MtKithairon_EventScript_"
R7 = "Route7_KroniaGrounds_EventScript_"
AC = "Route6_AntiopesCave_EventScript_"
ROAD_MUSIC = "MUS_ICHOR_ROAD"   # ICHOR_STUB_MUSIC: MUS_ICHOR_KITHAIRON / _KRONIA aren't composed yet

# Seams (design/phase3/BUILD.md): x offsets between neighbors.
R6_NORTH = 32            # Route 6's road leaves its north edge at 32-33 (verges 31, 34)
EL_SOUTH = 10            # ... and enters Eleutherai's south edge at 10-11
EL_NORTH = 10            # Eleutherai's road leaves its north edge at 10-11
MK_SOUTH = 18            # ... and enters Mt. Kithairon's south edge at 18-19
MK_NORTH = 20            # Mt. Kithairon's road leaves its north edge at 20-21
R7_SOUTH = 20            # ... and enters Route 7's south edge at 20-21
R7_NORTH = 20            # Route 7's road leaves its north edge at 20-23 (Thyrsa: 26-29, offset -6)


def RL(text, width):
    """Expand run-length rows ("F27 #2 .3") into strings, checking each width."""
    rows = []
    for line in text.strip().splitlines():
        row = "".join(tok[0] * int(tok[1:]) for tok in line.split())
        assert len(row) == width, (len(row), line)
        rows.append(row)
    return rows


def fir_border(cat):
    """A 2 x 2 border that repeats as an endless fir wood: crown over stack."""
    return [cat.cell("fir", 0, 1)[0], cat.cell("fir", 1, 1)[0],
            cat.cell("fir_stack", 0, 0)[0], cat.cell("fir_stack", 1, 0)[0]]


# ===========================================================================
# Route 6, the Eleutherai Road (56 x 28)
# ===========================================================================

def route6():
    m = Map("Route6_EleutheraiRoad", 56, 28, "kithairon")
    m.aethos_rows = set(range(22, 28))      # Eleusa's seam: aethos only
    # Ground, row by row, as runs: "F27 #2 .3" is 27 woods, 2 crag, 3 grass.
    # The road zigzags up the terraces: north from Eleusa (x 45-46) through
    # the vines, west along the vine terrace (rows 15-16), up the stair at the
    # west end, east along terrace 2 (rows 8-9) past Pythodoros's gap, then
    # north through the cutting to Eleutherai (x 32-33); the spur runs east
    # from the fork to Antiope's cave.
    m.grid(RL("""
        F27 #2 .3 =2 .2 #2 F18
        F26 #3 .3 =2 .1 #3 F18
        F24 #8 =2 #4 F18
        F24 #7 .1 =2 #4 F12 #6
        F23 #8 .1 =2 #3 .1 F10 #8
        F15 w1 F7 .8 .1 =2 .4 #2 .8 #8
        F3 #6 F2 .2 =2 w1 F7 .8 .1 =2 .1 .3 #2 v7 .1 #8
        F3 #6 .4 =2 w1 .1 w6 .9 =2 .1 .3 #2 .8 #8
        F3 #1 s4 =1 =4 =2 =1 =1 ,4 =13 =4 .1 ,7 .3 =4 #3
        F3 #1 s4 #1 =4 =2 =1 =1 ,4 =13 =4 ,11 =4 #3
        F3 #6 F4 =2 w1 w7 .14 ,10 .2 .3 #4
        F13 =2 .7 v15 ,8 .4 .2 #5
        F13 =2 _7 #5 #5 #5 _10 #9
        F12 F1 =2 .7 v5 #5 v5 .8 .2 .2 #1 F6
        F13 =2 .12 w5 .13 .2 .2 #1 F6
        F13 =15 ,3 =16 .2 #1 F6
        F13 =15 ,3 =16 .2 #1 F6
        F13 .1 .13 w5 v12 .1 =2 .2 #1 F6
        F13 v5 .1 .3 .2 v3 #5 .12 .1 =2 .2 #1 F6
        F13 .5 .1 .3 .5 #5 v7 .2 v3 .1 =2 .2 #1 F6
        F13 ,6 .5 v3 #5 .12 .1 =2 .2 #1 F6
        F13 #19 _9 #4 .2 #9
        .45 =2 .9
        .45 =2 .9
        .45 =2 .9
        .45 =2 .9
        .45 =2 .9
        .45 =2 .9
    """, 56))
    # ragged woods' edges (natural edges, MAP_DESIGN section 7)
    m.cells([(12, 13), (12, 14), (11, 19), (12, 19), (12, 20), (11, 20), (10, 20)], ".")
    m.cells([(13, 18), (13, 19)], "F")
    m.cells([(22, 5), (21, 5), (22, 6)], ".")
    m.cells([(37, 5), (37, 4)], "#")
    m.pathlike |= {(44, 21), (47, 21), (44, 18), (47, 18), (8, 8)}

    # stamps --------------------------------------------------------------------
    for (x, y) in ((0, 22), (4, 23), (8, 22), (12, 24), (16, 22), (20, 23), (24, 22), (28, 24),
                   (2, 26), (6, 25), (10, 26), (14, 26), (18, 25), (22, 26), (26, 26)):
        if y + 1 <= 27:
            m.pine(x, y) if (x // 2) % 3 == 0 else m.olive(x, y)
    for (x, y) in ((31, 24), (35, 25), (39, 23)):
        m.olive(x, y)
    for (x, y) in ((42, 22), (49, 22), (52, 24), (49, 26), (54, 22)):
        m.cypress(x, y)
    for (x, y) in ((33, 26), (38, 26), (41, 25)):
        m.cypress(x, y)
    m.olive(51, 26) if False else None
    m.put(43, 25, L.STELE)                               # the south sign
    m.stamp("old_vines", 45, 21, names={(0, 0): "vines", (1, 0): "vines_b"})
    m.stamp("barrier", 45, 18, names={(0, 0): "W", (1, 0): "E"}) if m.cat.has("barrier") else None
    m.stamp("press", 19, 18)
    m.stamp("cart", 24, 5)
    m.oak(28, 5)
    m.oak(35, 5)
    m.fir(40, 13)
    m.oak(50, 22 - 2) if False else None
    m.stamp("markers", 34, 6, names={(0, 0): "herm_top", (0, 1): "herm"})   # the fork's great herm
    m.named("markers", "dig", 50, 11)                     # a daily dig spot on the spur
    m.named("crag_detail", "mouth", 52, 7)               # Antiope's cave
    m.put(34, 1, L.STELE)                                # the north sign
    m.named("markers", "boulder", 38, 11) if False else None

    E = {
        "connections": [
            {"map": "MAP_ELEUTHERAI", "offset": R6_NORTH - EL_SOUTH, "direction": "up"},
        ],
        "object_events": [
            # beat 26: Alethea by the vines, the herald behind his barrier
            obj(P + "ALETHEA", 47, 22, R6 + "Alethea", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_ICHOR_HIDE_ALETHEA_ROUTE6", local_id="LOCALID_ROUTE6_ALETHEA"),
            obj(P + "HERALD", 45, 17, R6 + "Herald", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_HIDE_HERALD_BARRIER", local_id="LOCALID_ROUTE6_HERALD"),
            # leg B: the vine-dresser, Ikarios, the pilgrims
            obj(P + "HARVESTER", 16, 17, R6 + "VineDresser", "MOVEMENT_TYPE_FACE_DOWN"),
            obj(P + "VINTNER", 38, 14, R6 + "Ikarios", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3),
            obj(P + "WOMAN", 34, 16, R6 + "Pilgrim", "MOVEMENT_TYPE_FACE_LEFT"),
            obj(P + "MAN", 23, 15, R6 + "PilgrimB", "MOVEMENT_TYPE_FACE_LEFT"),
            item_ball(11, 7, "ITEM_SUPER_REPEL", "FLAG_ICHOR_ITEM_ROUTE6_SUPER_REPEL"),
            # terrace 2: Pythodoros at the gap, the cart driver
            obj(P + "YOUTH_M", 16, 7, R6 + "Pythodoros", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2),
            obj(P + "MAN", 27, 7, R6 + "CartDriver", "MOVEMENT_TYPE_FACE_LEFT"),
            # the cellar nook: the drum (the Girdle) and the Max Ether
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 8, 8, R6 + "Drum", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_HIDE_ROUTE6_DRUM", local_id="LOCALID_ROUTE6_DRUM"),
            item_ball(5, 8, "ITEM_MAX_ETHER", "FLAG_ICHOR_ITEM_ROUTE6_MAX_ETHER"),
            # the spur: Botrys in his vines, the Super Potion halfway
            obj(P + "HARVESTER", 43, 7, R6 + "Botrys", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=2),
            item_ball(44, 11, "ITEM_SUPER_POTION", "FLAG_ICHOR_ITEM_ROUTE6_SUPER_POTION"),
            # leg D: Astylos in the cutting
            obj(P + "YOUTH_M", 31, 3, R6 + "Astylos", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3),
        ],
        "warp_events": [warp(52, 7, "MAP_ROUTE6_ANTIOPES_CAVE", 0)],
        "coord_events": [trigger(45, 20, R6 + "HeraldScene"), trigger(46, 20, R6 + "HeraldScene")],
        "bg_events": [
            sign(43, 25, R6 + "SignSouth"),
            sign(45, 21, R6 + "Vines", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(46, 21, R6 + "Vines", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(20, 19, R6 + "SignPress"),
            sign(34, 7, R6 + "GreatHerm"),
            sign(50, 11, R6 + "DigSpot"),
            sign(34, 1, R6 + "SignNorth"),
        ],
    }
    views = [(45, 26), (45, 21), (45, 17), (38, 16), (28, 16), (16, 15), (13, 10), (18, 9), (27, 8),
             (35, 9), (44, 9), (51, 9), (32, 5), (32, 2), (8, 9)]
    return m, E, views


# ===========================================================================
# Eleutherai, the free town (32 x 26)
# ===========================================================================

def house(m, x, y, w, door_dx, windows=(), door="plank"):
    """An Eleusa-kit house front, w wide, its roof's top-left at (x, y)."""
    for i in range(w):
        side = "L" if i == 0 else ("R" if i == w - 1 else "M")
        m.named("roof_tile", f"R0_{side}", x + i, y)
        m.named("roof_tile", f"R1_{side}", x + i, y + 1)
        m.named("wall", f"W0_{side}", x + i, y + 2)
        m.named("wall", f"W1_{side}", x + i, y + 3)
    for dx, kind in windows:
        m.named("windows", kind, x + dx, y + 2)
    m.named("doors", door, x + door_dx, y + 3)
    return (x + door_dx, y + 3)


def eleutherai():
    m = Map("Eleutherai", 32, 26, "kithairon")
    # The road runs north past the foot of the fort's crag (x 10-11). The fort
    # (north-east) is stamped over the grass rows 2-9; its crag drops to the
    # stair at x 22-24. The temple's paving is west of the road; Lysidike's
    # house stands in its sheep pens to the south-east.
    m.grid(RL("""
        F8 .2 =2 .2 F18
        F8 .2 =2 .2 F18
        F8 .2 =2 .2 #3 .13 #2
        F8 .2 =2 .2 #3 .13 #2
        F8 .2 =2 .2 #3 .1 c11 .1 #2
        F8 .2 =2 .2 #3 .1 c11 .1 #2
        F8 .2 =2 .2 #3 .1 c11 .1 #2
        F8 .2 =2 .2 #3 .2 c9 .2 #2
        F7 .3 =2 .2 #3 .13 #2
        F6 .4 =2 .2 #3 .13 #2
        F1 .9 =2 .2 #8 =3 #7
        F1 .1 p7 .1 =2 .2 #8 =3 #7
        F1 .1 p7 .1 =2 =13 .7
        F1 .1 p7 .1 =2 =13 .7
        F1 .1 p7 .1 =2 .20
        F1 .1 p7 .1 =2 .3 .2 w13 .2
        F1 .1 p7 .1 =2 .5 w1 .11 w1 .2
        F1 .9 =2 .5 w1 .11 w1 .2
        .10 =2 .5 w1 .11 w1 .2
        .10 =2 .5 w1 .11 w1 .2
        .10 =2 .5 w1 .5 w6 w1 .2
        .10 =2 .5 w1 .5 w1 .5 w1 .2
        .10 =2 .5 w1 .5 w1 .5 w1 .2
        F5 .5 =2 .5 w5 .3 w5 .2
        F5 .4 .1 =2 .2 F3 .9 F6
        F5 .4 .1 =2 .2 F3 .9 F6
    """, 32))
    m.cells([(30, 12), (31, 12), (31, 13), (30, 14), (31, 14), (31, 15), (30, 16), (31, 16)], "F")
    m.cells([(0, 17), (0, 18)], "F")
    m.cells([(13, 24), (12, 24)], ".")
    m.pavelike |= {(2, 15), (2, 16), (8, 16), (4, 12), (6, 11), (5, 13), (4, 16), (2, 11), (8, 11)}
    m.pathlike |= {(22, 9), (23, 9), (24, 9)}

    # the fort -----------------------------------------------------------------
    for x in range(17, 30):
        side = "L" if x == 17 else ("R" if x == 29 else "M")
        m.named("fort", f"W0_{side}", x, 2)
        m.named("fort", f"W1_{side}", x, 3)
    m.named("fort", "slit", 20, 2)
    m.named("fort", "slit", 26, 2)
    m.named("fort", "door", 23, 3)
    for y in (4, 5, 6):
        m.named("fort", "side", 17, y)
        m.named("fort", "side", 29, y)
    for tx in (17, 28):
        for i, c in enumerate(("L", "R")):
            m.named("fort", f"T0_{c}", tx + i, 7)
            m.named("fort", f"T1_{c}", tx + i, 8)
            m.named("fort", f"T2_{c}", tx + i, 9)
    for x in range(19, 28):
        if 22 <= x <= 24:
            continue
        m.named("fort", "W0_M", x, 8)
        m.named("fort", "W1_M", x, 9)
    for i, c in enumerate("LMR"):
        m.named("fort", f"gate_{c}", 22 + i, 8)
        m.named("fort", f"gateF_{c}", 22 + i, 9)
    # the god's temple: columns, a stump, a fallen drum, the empty plinth
    for x in (2, 8):
        m.named("temple", "col_top_g", x, 10)
        m.named("temple", "col", x, 11)
    m.named("temple", "col_top", 2, 15)
    m.named("temple", "col", 2, 16)
    m.named("temple", "stump", 8, 16)
    m.named("temple", "drum", 4, 12)
    m.named("temple", "stump", 6, 11)
    m.named("temple", "plinth", 5, 13)
    m.named("temple", "broom", 4, 16)
    # houses: Oinoe's beside the temple, Lysidike's among the pens
    oinoe = house(m, 1, 18, 4, 2, windows=((1, "shutters"),))
    lysi = house(m, 19, 16, 5, 2, windows=((1, "lattice"), (3, "shutters")))
    # the spring with its trough, by the road; signs; trees
    m.stamp("trough", 13, 15)
    m.put(12, 1, L.STELE)
    m.put(9, 14, L.STELE)
    m.oak(13, 18)
    m.oak(6, 22)
    m.cypress(9, 8)
    m.cypress(13, 9)
    m.cypress(25, 12)
    E = {
        "connections": [
            {"map": "MAP_ROUTE6_ELEUTHERAI_ROAD", "offset": EL_SOUTH - R6_NORTH, "direction": "down"},
            {"map": "MAP_MT_KITHAIRON", "offset": EL_NORTH - MK_SOUTH, "direction": "up"},
        ],
        "object_events": [
            obj(P + "ALETHEA", 5, 14, EL + "Alethea", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_HIDE_ALETHEA_ELEUTHERAI", local_id="LOCALID_ELEUTHERAI_ALETHEA"),
            obj(P + "ELDER_F", 5, 17, EL + "Oinoe", "MOVEMENT_TYPE_FACE_UP",
                local_id="LOCALID_ELEUTHERAI_OINOE"),
            obj(P + "HOPLITE", 21, 12, EL + "Sentry", "MOVEMENT_TYPE_FACE_DOWN"),
            obj(P + "KID_M", 15, 16, EL + "ShepherdBoy", "MOVEMENT_TYPE_FACE_LEFT"),
            obj(P + "ELDER_M", 14, 16, EL + "OldMan", "MOVEMENT_TYPE_FACE_UP"),
            obj("OBJ_EVENT_GFX_SPECIES(WOOLOO)", 25, 21, EL + "Sheep", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
            obj("OBJ_EVENT_GFX_SPECIES(WOOLOO)", 27, 18, EL + "Sheep", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
            obj("OBJ_EVENT_GFX_SPECIES(WOOLOO)", 18, 21, EL + "Sheep", "MOVEMENT_TYPE_FACE_RIGHT"),
        ],
        "warp_events": [
            warp(23, 3, "MAP_ELEUTHERAI_WATCH_HOUSE", 0),
            warp(*oinoe, "MAP_ELEUTHERAI_OINOE_HOUSE", 0),
            warp(*lysi, "MAP_ELEUTHERAI_LYSIDIKE_HOUSE", 0),
        ],
        "coord_events": [],
        "bg_events": [
            sign(5, 13, EL + "Plinth"),
            sign(9, 14, EL + "SignPlinth"),
            sign(12, 1, EL + "SignNorth"),
            sign(13, 15, EL + "Trough"),
            sign(14, 15, EL + "Trough"),
        ],
    }
    views = [(10, 24), (10, 18), (6, 15), (14, 14), (23, 12), (23, 6), (21, 21), (10, 6), (10, 1)]
    return m, E, views


# ===========================================================================
# Mt. Kithairon, the maenads' pass (40 x 56)
# ===========================================================================

def kithairon():
    m = Map("MtKithairon", 40, 56, "kithairon")
    m.core_rows = set(range(0, 6))          # Route 7's seam: core and aethos only
    # South to north: the first switchbacks (Lykidas), the fir clearing's forced
    # band, the glade and the maenads' dancing floor (Euia at its only way
    # north), the pass fork (east: Aktaion's spring; west: the drum and the Max
    # Revive), Pentheus's fir, the fold and the high meadow, the ivy shrine's
    # side ledge, the north lip.
    m.grid(RL("""
        F16 #3 .1 =2 .1 F17
        F16 .4 =2 .2 F16
        F14 .6 =2 .1 #13 F4
        F14 #6 =2 .2 .11 #5
        F2 .4 F8 #6 =6 .9 #5
        F2 .6 F6 #6 =6 .9 #5
        F1 .1 ,4 .4 F4 #6 =2 .3 .10 #5
        F1 ,6 .3 .10 =2 .1 #17
        F1 ,5 .4 w8 .2 =2 .2 #16
        F1 .1 ,3 .5 w1 .6 w1 .2 =2 .2 #16
        F2 ,4 .4 w1 .6 w1 .2 =2 .2 #16
        F2 .8 w1 .6 w1 .2 =2 .2 #3 F13
        F3 .7 w1 .6 w1 .2 =2 .2 #3 F13
        F3 .7 w3 .2 w3 .2 =2 .2 #3 F13
        #9 F2 .7 .2 =2 .1 .3 .2 F8 F4
        #9 F2 .7 .2 =2 .1 .3 .2 F5 .6 F1
        #8 F3 .7 .2 =2 .1 .3 .2 F4 .3 ~3 .1 F1
        #8 F3 .7 .2 =2 .1 .3 .2 .1 F3 .3 ~3 .1 F1
        #7 F4 .7 .2 =2 .1 .3 ,6 .3 ~3 .1 F1
        #7 #7 .4 .2 =2 .2 ,9 .6 F1
        #7 #2 .4 #1 .4 .1 .1 =2 .1 .1 ,9 .6 F1
        #7 #2 .3 =8 =2 =4 ,6 =3 .4 F1
        #7 #2 .3 #2 =6 =2 =4 ,6 =3 .4 F1
        #20 =2 .2 ,8 .4 F4
        F8 #12 =2 #6 ,4 .3 F5
        F8 #8 .1 #3 =2 #6 .4 F8
        F8 #12 =2 .1 #5 F12
        F8 #6 #6 =2 #10 F8
        F14 .6 =2 .10 F8
        F14 .3 =12 .3 F8
        F14 .3 =12 .3 F8
        F14 .3 =12 .3 F8
        F14 .3 =12 .3 F8
        F14 .3 =12 .3 F8
        F14 .3 =12 .3 F8
        F14 .3 =12 .3 F8
        F15 .3 =10 .4 F8
        F16 .4 .4 =2 .6 F8
        F18 .6 =2 .2 ,4 F8
        F18 .6 =2 .2 ,4 F8
        F22 .2 =2 .2 ,4 F8
        F8 =2 F12 .2 =2 .3 ,3 F8
        F8 =6 ,4 =8 .3 ,3 F8
        F8 =6 ,4 =8 .3 ,3 F8
        F8 =2 #14 .2 .4 F10
        F2 .6 =2 .8 .2 #6 F14
        F2 .1 ,3 .2 =2 .8 .2 #6 F14
        F2 .1 ,4 .1 =2 .8 .2 F20
        F2 .1 ,4 .1 =2 .8 .2 F20
        F2 .5 .1 =12 .4 F16
        F2 .5 .1 =12 .4 F16
        F2 .4 .2 .2 _6 .2 =2 .2 F18
        F2 .4 .2 .2 .7 .1 =2 .3 F17
        F2 .4 .2 .2 .7 .1 =2 .3 F17
        F10 .7 .1 =2 .1 F19
        F10 .7 .1 =2 .1 F19
    """, 40))
    m.pathlike |= {(13, 21)}

    # stamps
    m.stamp("pentheus_fir", 23, 14)
    m.stamp("trough", 12, 9)
    m.named("markers", "boundary", 22, 20)
    m.named("markers", "seat", 34, 18)
    m.named("markers", "dig", 35, 23)
    m.named("markers", "dig", 6, 9)
    m.named("markers", "drum", 26, 31)
    m.named("markers", "drum_b", 27, 34)
    m.named("markers", "drum", 17, 33)
    m.stamp("markers", 31, 4, names={(0, 0): "shrine_bad_top", (0, 1): "shrine_bad"})
    m.named("crag_detail", "marked_face", 16, 27)
    m.named("crag_detail", "ivy_face", 15, 27)
    m.named("crag_detail", "ivy_face", 23, 27)
    m.put(22, 1, L.STELE)
    m.put(17, 54, L.STELE)
    m.put(18, 13, L.STELE)
    m.oak(14, 10)
    m.oak(26, 37)
    E = {
        "connections": [
            {"map": "MAP_ELEUTHERAI", "offset": MK_SOUTH - EL_NORTH, "direction": "down"},
            {"map": "MAP_ROUTE7_KRONIA_GROUNDS", "offset": MK_NORTH - R7_SOUTH, "direction": "up"},
        ],
        "object_events": [
            obj(P + "GOATHERD", 11, 47, MK + "Lykidas", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3),
            obj(P + "MAENAD", 22, 26, MK + "Euia", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=4,
                local_id="LOCALID_KITHAIRON_EUIA"),
            obj(P + "MAENAD", 30, 32, MK + "Bromia", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2,
                local_id="LOCALID_KITHAIRON_BROMIA"),
            obj(P + "MAENAD", 22, 31, MK + "Maenad", "MOVEMENT_TYPE_FACE_RIGHT",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_MAENAD_1"),
            obj(P + "MAENAD", 24, 30, MK + "Maenad", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_MAENAD_2"),
            obj(P + "MAENAD", 23, 34, MK + "Maenad", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_MAENAD_3"),
            obj("OBJ_EVENT_GFX_SPECIES(BOTRYKIT)", 21, 33, MK + "Botrykit", "MOVEMENT_TYPE_FACE_RIGHT",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_BOTRYKIT_1"),
            obj("OBJ_EVENT_GFX_SPECIES(BOTRYKIT)", 25, 33, MK + "Botrykit", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_BOTRYKIT_2"),
            item_ball(15, 30, "ITEM_REVIVE", "FLAG_ICHOR_ITEM_KITHAIRON_REVIVE"),
            item_ball(16, 25, "ITEM_MAX_ELIXIR", "FLAG_ICHOR_ITEM_KITHAIRON_MAX_ELIXIR"),
            obj(P + "HOPLITE", 19, 20, MK + "Arimnestos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2),
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 13, 21, MK + "Drum", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_HIDE_KITHAIRON_DRUM", local_id="LOCALID_KITHAIRON_DRUM"),
            item_ball(10, 21, "ITEM_MAX_REVIVE", "FLAG_ICHOR_ITEM_KITHAIRON_MAX_REVIVE"),
            # ICHOR_STUB_TM: Venoshock has no TM number yet (SCRIPT.md region A, open question 17)
            item_ball(37, 22, "ITEM_TM_SLUDGE_BOMB", "FLAG_ICHOR_ITEM_KITHAIRON_TM_VENOSHOCK"),
            obj(P + "SHEPHERD", 17, 11, MK + "Phorbas", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("OBJ_EVENT_GFX_SPECIES(WOOLOO)", 14, 12, MK + "Sheep", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
            obj(P + "TITAN_GRUNT", 30, 5, MK + "Ilys", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2),
        ],
        "warp_events": [],
        "coord_events": [trigger(x, 38, MK + "DancingFloor") for x in (24, 25)],
        "bg_events": [
            sign(17, 54, MK + "SignSouth"),
            sign(16, 27, MK + "MarkedIvy"),
            sign(22, 20, MK + "BoundaryStone"),
            sign(24, 17, MK + "PentheusFir"),
            sign(34, 18, MK + "SpringSeat"),
            sign(36, 17, MK + "Spring"),
            sign(37, 16, MK + "Spring"),
            sign(35, 23, MK + "DigSpot"),
            sign(6, 9, MK + "DigSpot"),
            sign(18, 13, MK + "SignFold"),
            sign(31, 5, MK + "Shrine"),
            sign(22, 1, MK + "SignNorth"),
        ],
    }
    views = [(18, 54), (12, 49), (9, 45), (16, 43), (24, 40), (23, 33), (20, 25), (28, 21), (35, 20),
             (14, 21), (21, 16), (14, 11), (26, 5), (20, 1)]
    return m, E, views


# ===========================================================================
# Route 7, the Kronia grounds (44 x 40)
# ===========================================================================

def route7():
    m = Map("Route7_KroniaGrounds", 44, 40, "kronia")
    m.aethos_rows = set(range(0, 6))         # Thyrsa's seam: aethos only
    m.core_rows = set(range(34, 40))         # Mt. Kithairon's seam: core and aethos only
    # The north face (south half) descends north: the defile and Komos, the
    # first forced band, the switchbacks (the lost pilgrim, the Full Heal),
    # Hagnon's bend and the second band in the pasture, the great herm. Then the
    # Kronia camp on the Asopos meadow, the road straight through it to the
    # Elektran Gate (Thyrsa's map, across the north seam), the river east.
    m.grid(RL("""
        .20 =4 .20
        .20 =4 .20
        .20 =4 .20
        .20 =4 .20
        .20 =4 .20
        .20 =4 .20
        .20 =4 .13 ~7
        .20 =4 .12 ~8
        .20 =4 .12 ~8
        .20 =4 .12 ~8
        .20 =4 .12 ~8
        .20 =4 .11 ~9
        .20 =4 .11 ~9
        .20 =4 .11 ~9
        .20 =4 .11 ~9
        .20 =4 .11 ~9
        .20 =4 =11 ~9
        F19 w1 ,2 w1 F7 ,5 ~9
        F19 w1 ,2 w1 F7 ,5 ~9
        F19 w1 ,2 w1 F7 ,5 ~4 .2 ~3
        F10 .9 w1 =2 w1 F7 ,5 ~4 .2 ~3
        F10 =12 F8 ,5 ~9
        F10 =12 F8 ,5 ~9
        F2 .1 ,4 .3 =2 .9 F9 ,5 ~9
        F2 .1 ,4 .3 =2 .9 F9 ,5 ~9
        F2 .7 .1 =2 .9 F9 ,5 ~9
        F2 .7 .1 =2 .9 F9 .5 ~9
        F2 .7 .1 =12 F8 .5 ~9
        F2 .7 .1 =12 F8 F5 ~9
        F17 #3 ,2 #3 F10 ~9
        F17 #3 ,2 #3 F10 ~9
        F17 #3 ,2 #3 F10 ~9
        F17 #3 ,2 #3 F10 ~9
        F12 #8 =2 #8 F5 ~9
        F12 #8 =2 #8 F14
        F12 #7 .1 =2 #8 F14
        F12 #8 =2 #8 F14
        F12 #8 =2 #8 F14
        F14 #6 =2 #6 F16
        F14 .5 .1 =2 .1 .4 F17
    """, 44))
    # stamps: the camp ------------------------------------------------------------
    def table(x, y, w, foods=("T_bread", "T_figs", "T_jars")):
        for i in range(w):
            c = "C_L" if i == 0 else ("C_R" if i == w - 1 else ("C_M", "C_M2", "C_M3")[i % 3])
            t = "T_L" if i == 0 else ("T_R" if i == w - 1 else foods[(i - 1) % len(foods)])
            b = "B_L" if i == 0 else ("B_R" if i == w - 1 else "B_M")
            m.named("feast_table", c, x + i, y)
            m.named("feast_table", t, x + i, y + 1)
            m.named("feast_table", b, x + i, y + 2)
    table(2, 6, 8)                                   # the long tables, west of the road
    table(2, 10, 7, ("T_figs", "T_jars", "T_bread"))
    table(25, 11, 6, ("T_jars", "T_bread", "T_figs"))  # Kleon's table
    m.stamp("oven", 13, 6)
    m.stamp("stage", 24, 6)
    m.stamp("big_tent", 30, 6)
    for (x, y) in ((11, 11), (14, 11), (33, 10)):
        m.stamp("tent", x, y)
    m.stamp("banner", 15, 13)
    m.named("camp_small", "board", 19, 15)
    m.named("camp_small", "hoop", 4, 14)
    m.named("camp_small", "hoop", 8, 15)
    m.named("camp_small", "reader_L", 29, 15)
    m.named("camp_small", "reader_R", 30, 15)
    m.stamp("markers", 24, 14, names={(0, 0): "herm_top", (0, 1): "herm"})
    m.named("markers", "dig", 33, 15)
    # the north band (aethos only): an avenue of cypresses and olives to the gate
    for (x, y) in ((18, 1), (25, 1), (18, 4), (25, 4)):
        m.cypress(x, y)
    for (x, y) in ((3, 2), (9, 1), (13, 3), (30, 2), (36, 1), (40, 3)):
        m.olive(x, y)
    m.put(19, 1, L.STELE)
    m.put(23, 39, L.STELE)
    m.oak(0, 14)
    m.oak(15, 24)
    E = {
        "connections": [
            {"map": "MAP_MT_KITHAIRON", "offset": R7_SOUTH - MK_NORTH, "direction": "down"},
            {"map": "MAP_THYRSA_CITY", "offset": -6, "direction": "up"},
        ],
        "object_events": [
            # the north face
            obj(P + "SATYR", 19, 35, R7 + "Komos", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=4),
            obj(P + "YOUTH_F", 17, 25, R7 + "LostPilgrim", "MOVEMENT_TYPE_FACE_DOWN"),
            item_ball(3, 24, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_ROUTE7_FULL_HEAL"),
            obj(P + "MAN", 14, 20, R7 + "Hagnon", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=4),
            # beat 29: the greeter, Kleon and Alethea at the tables, the reader
            obj(P + "KRONIST", 23, 15, R7 + "Greeter", "MOVEMENT_TYPE_FACE_DOWN",
                local_id="LOCALID_ROUTE7_GREETER"),
            obj(P + "KLEON_FEAST", 26, 13, R7 + "Kleon", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_HIDE_KLEON_KRONIA", local_id="LOCALID_ROUTE7_KLEON"),
            obj(P + "ALETHEA", 28, 13, R7 + "Alethea", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_HIDE_ALETHEA_KRONIA", local_id="LOCALID_ROUTE7_ALETHEA"),
            obj(P + "KRONIST", 31, 15, R7 + "Reader", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_ICHOR_KRONIA_READER_GONE", local_id="LOCALID_ROUTE7_READER"),
            obj(P + "KRONIST", 31, 15, R7 + "ReaderAfter", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_TEMP_5", local_id="LOCALID_ROUTE7_READER_AFTER"),
            obj(P + "KRONIST", 26, 7, R7 + "StageKronist", "MOVEMENT_TYPE_FACE_DOWN"),
            obj(P + "TITAN_GRUNT", 32, 9, R7 + "TentGuard", "MOVEMENT_TYPE_FACE_DOWN"),
            obj(P + "MAN", 16, 8, R7 + "Baker", "MOVEMENT_TYPE_FACE_LEFT"),
            obj(P + "ELDER_M", 5, 8, R7 + "Master", "MOVEMENT_TYPE_FACE_UP"),
            obj(P + "MAN", 6, 8, R7 + "Steward", "MOVEMENT_TYPE_FACE_UP"),
            obj(P + "WOMAN", 8, 8, R7 + "Mother", "MOVEMENT_TYPE_FACE_UP"),
            obj(P + "KID_F", 5, 15, R7 + "Child", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
            obj(P + "KID_M", 7, 14, R7 + "ChildB", "MOVEMENT_TYPE_FACE_LEFT"),
            # the Titanborn at the tables: they battle only if asked
            obj(P + "TITAN_GRUNT", 3, 8, R7 + "Argillos", "MOVEMENT_TYPE_FACE_UP"),
            obj(P + "TITAN_GRUNT", 4, 12, R7 + "Keramos", "MOVEMENT_TYPE_FACE_UP"),
            obj(P + "TITAN_GRUNT", 7, 12, R7 + "Plinthos", "MOVEMENT_TYPE_FACE_UP"),
            obj(P + "TITAN_GRUNT", 29, 13, R7 + "Gypsos", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_GYPSOS_WENT_HOME", local_id="LOCALID_ROUTE7_GYPSOS"),
            # the reed islet (the Conch)
            item_ball(39, 19, "ITEM_BIG_PEARL", "FLAG_ICHOR_ITEM_ROUTE7_BIG_PEARL"),
        ],
        "warp_events": [],
        "coord_events": [trigger(x, 16, R7 + "GreeterScene") for x in (20, 21)]
        + [trigger(x, 12, R7 + "KleonScene", "VAR_TEMP_2") for x in (20, 21, 22, 23)],
        "bg_events": [
            sign(23, 39, R7 + "SignSouth"),
            sign(24, 15, R7 + "GreatHerm"),
            sign(19, 15, R7 + "SignKronia"),
            sign(16, 14, R7 + "Banner"),
            sign(29, 15, R7 + "ReaderTable"),
            sign(30, 15, R7 + "ReaderTable"),
            sign(31, 8, R7 + "StewardsTent"),
            sign(32, 8, R7 + "StewardsTent"),
            sign(33, 15, R7 + "DigSpot"),
            sign(19, 1, R7 + "SignNorth"),
        ],
    }
    views = [(20, 38), (20, 35), (20, 30), (14, 27), (10, 23), (16, 21), (20, 18), (21, 15), (12, 11),
             (28, 10), (31, 16), (38, 20), (21, 5), (21, 1)]
    return m, E, views


# ===========================================================================
# Antiope's cave (16 x 12)
# ===========================================================================

def cave():
    m = Map("Route6_AntiopesCave", 16, 12, "cave")
    m.grid([
        "################",
        "################",
        "####kkkkkkkk####",
        "###kkkkkkkkkk#k#",
        "##kkkkkkkkkkk###",
        "##kkkkkkkkkkkkk#",
        "##kkkkkkkkkkkk##",
        "###kkkkkkkkkkk##",
        "###kkkkkkkkkk###",
        "####kkkkkkkkk###",
        "#####kkkkkk#####",
        "#######kk#######",
    ])
    m.named("cave_detail", "cave_carving_L", 7, 1)
    m.named("cave_detail", "cave_carving_R", 8, 1)
    m.named("cave_detail", "cave_crack", 10, 1)
    m.named("cave_detail", "cave_shelf", 12, 2)
    m.named("cave_detail", "cave_marked", 14, 4)
    m.named("cave_floor", "exit", 7, 11)
    m.named("cave_floor", "exit", 8, 11)
    m.named("dig_cave", "dig_cave", 4, 6)
    m.named("brazier", "cold_top", 4, 8)
    m.named("brazier", "cold", 4, 9)
    E = {
        "object_events": [
            item_ball(12, 2, "ITEM_PP_UP", "FLAG_ICHOR_ITEM_ANTIOPE_PP_UP"),
            item_ball(14, 3, "ITEM_STAR_PIECE", "FLAG_ICHOR_ITEM_ANTIOPE_STAR_PIECE"),
        ],
        "warp_events": [warp(7, 11, "MAP_ROUTE6_ELEUTHERAI_ROAD", 0), warp(8, 11, "MAP_ROUTE6_ELEUTHERAI_ROAD", 0)],
        "coord_events": [],
        "bg_events": [
            sign(7, 1, AC + "Carving"), sign(8, 1, AC + "Carving"),
            sign(4, 8, AC + "Brazier"), sign(4, 9, AC + "Brazier"),
            sign(4, 6, AC + "DigSpot"),
            sign(14, 4, AC + "MarkedIvy"),
        ],
    }
    return m, E, [(7, 10), (7, 4), (12, 4)]


# ===========================================================================
# Running the builds
# ===========================================================================

MAPS = {
    "route6": ("LAYOUT_ROUTE6_ELEUTHERAI_ROAD", "Route6_EleutheraiRoad", route6, ROAD_MUSIC, None),
    "cave": ("LAYOUT_ROUTE6_ANTIOPES_CAVE", "Route6_AntiopesCave", cave, "MUS_ICHOR_HOLLOW",
             {"requires_flash": True}),
    "eleutherai": ("LAYOUT_ELEUTHERAI", "Eleutherai", eleutherai, ROAD_MUSIC, None),
    "kithairon": ("LAYOUT_MT_KITHAIRON", "MtKithairon", kithairon, ROAD_MUSIC, None),
    "route7": ("LAYOUT_ROUTE7_KRONIA_GROUNDS", "Route7_KroniaGrounds", route7, ROAD_MUSIC, None),
}


def build(only=None, shapes_only=False, tag=""):
    missing = []
    built = {}
    for key, (layout, folder, fn, music, extra) in MAPS.items():
        if only and key not in only:
            continue
        m, E, views = fn()
        m.missing = missing
        m.autotile()
        built[key] = (m, E, views, layout, folder, music, extra)
    if shapes_only:
        data = json.loads(L.SHAPES.read_text()) if (L.SHAPES.exists() and only) else {}
        for kind in L.SHAPE_SETS:
            used = set(data.get(kind, []))
            for (m, *_rest) in built.values():
                used |= m.shapes_used[kind]
            data[kind] = sorted(used)
        L.SHAPES.write_text(json.dumps(data, indent=1) + "\n")
        print({k: len(v) for k, v in data.items()}, "->", L.SHAPES.relative_to(ROOT))
        return
    if missing:
        print(f"{len(missing)} shape cells drawn with stand-ins: run --shapes, rebuild the art")
    errs = []
    for key, (m, E, views, layout, folder, music, extra) in built.items():
        errs += m.check_seams()
    if errs:
        sys.exit("seam errors:\n  " + "\n  ".join(errs[:20]))
    for key, (m, E, views, layout, folder, music, extra) in built.items():
        border = BORDERS.get(key, lambda c: fir_border(c))(m.cat)
        L.write_layout(layout, folder, m, border)
        L.write_events(folder, E, music, extra)
        plain = L.render(m, E, border, views, tag)
        IMG.mkdir(parents=True, exist_ok=True)
        shutil.copy2(L.RENDER / f"{m.name}{tag}.png", IMG / f"{folder}.png")
        print(f"{folder}: {m.w}x{m.h} -> {(IMG / f'{folder}.png').relative_to(ROOT)}")
        CHECKS.get(key, lambda m, E: None)(m, E)
    return built


BORDERS = {"cave": lambda c: [c.named("cave", "1|11111111")[0]] * 4}
CHECKS = {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapes", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    build(args.only.split(",") if args.only else None, args.shapes, args.tag)


if __name__ == "__main__":
    main()
