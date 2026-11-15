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
from kithairon_lib import ROOT, Map, hidden, item_ball, obj, sign, trigger, warp  # noqa: E402

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

    # polish pass: the terraces' risers are dry stone, with rock ledges where the
    # road lets you hop home; the outcrops, the cave's crag and the cutting's
    # shoulders are tiers with real cliffs.
    for x in range(13, 32):
        m.ch[21][x] = "w"
    for x in range(32, 41):
        m.ch[21][x] = "^"
    for x in list(range(41, 45)) + list(range(47, 56)):
        m.ch[21][x] = "w"
    m.ch[21][45] = "v"                  # an old vine stock, too thick to cut, beside the gap
    m.ch[21][46] = "="                  # the thicket of young vines stands in the gap
    for x in range(15, 22):
        m.ch[12][x] = "^"
    for x in range(22, 37):
        m.ch[12][x] = "w"
    for x in range(37, 47):
        m.ch[12][x] = "^"
    for x in range(47, 56):
        m.ch[12][x] = "w"
    for y in range(13, 21):
        if m.ch[y][49] == "#":
            m.ch[y][49] = "w"
    # an outcrop in the vines on each terrace
    m.raise_(25, 12, 29, 14, 1)
    m.rect(25, 12, 29, 14, ".")
    m.raise_(27, 18, 31, 20, 1)
    m.rect(27, 18, 31, 20, ".")
    m.cells([(28, 18), (29, 18)], "#")
    # the cutting's two shoulders under Eleutherai
    m.raise_(21, 0, 30, 4, 1)
    m.rect(23, 3, 30, 4, ".")
    m.rect(21, 0, 26, 2, "F")
    m.rect(27, 0, 30, 2, "#")
    m.raise_(34, 0, 39, 3, 1)
    m.rect(34, 2, 37, 3, ".")
    m.rect(34, 0, 37, 1, "#")
    m.rect(38, 0, 39, 3, "F")
    # Antiope's crag, its cave mouth in the cliff
    m.raise_(48, 0, 55, 7, 1)
    m.rect(48, 6, 55, 7, ".")
    m.rect(48, 0, 55, 3, "F")
    m.rect(49, 4, 54, 5, "#")
    m.cells([(48, 4), (48, 5), (55, 4), (55, 5)], "F")
    m.face[(52, 7)] = ("cliff_mouth", "mouth")
    m.no_face_decor |= {(51, 6), (52, 6), (53, 6), (51, 7), (53, 7)}
    m.rect(53, 8, 55, 10, "F")
    # band 3: across the road under the cutting, Astylos just past it
    m.rect(31, 4, 33, 6, ",")
    m.rect(34, 4, 37, 5, "#")
    m.cells([(37, 4), (37, 5)], "F")
    # long grass between the vine rows on both terraces, with a reason to go in
    m.rect(32, 17, 43, 18, ",")
    m.cells([(32, 17), (43, 18), (38, 18)], ".")
    m.rect(9, 7, 12, 7, ",")
    # a clearing in the west woods: deadfall and a hidden find
    m.rect(3, 13, 8, 17, ".")
    m.rect(4, 14, 7, 16, ",")
    m.cells([(3, 13), (8, 17), (3, 17), (8, 13)], "F")
    m.cells([(5, 13), (6, 13)], "L")
    m.rect(9, 15, 12, 15, ".")

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
    m.stamp("barrier", 45, 18, names={(0, 0): "W", (1, 0): "E"}) if m.cat.has("barrier") else None
    m.stamp("press", 19, 18)
    m.stamp("cart", 24, 5)
    m.oak(28, 5)
    m.oak(35, 5)
    m.fir(40, 13)
    m.oak(50, 22 - 2) if False else None
    m.stamp("markers", 34, 6, names={(0, 0): "herm_top", (0, 1): "herm"})   # the fork's great herm
    m.named("markers", "dig", 50, 11)                     # a daily dig spot on the spur
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
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 8, 8, "EventScript_StrengthBoulder",
                "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_ROUTE6_DRUM", local_id="LOCALID_ROUTE6_DRUM"),
            # beat 26: the young vines across the road's gap (Demeter's Sickle)
            obj("OBJ_EVENT_GFX_CUTTABLE_TREE", 46, 21, "EventScript_CutTree", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_HIDE_ELEUTHERAI_VINES", local_id="LOCALID_ROUTE6_VINES"),
            item_ball(5, 8, "ITEM_MAX_ETHER", "FLAG_ICHOR_ITEM_ROUTE6_MAX_ETHER"),
            # the spur: Botrys in his vines, the Super Potion halfway
            obj(P + "HARVESTER", 43, 7, R6 + "Botrys", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=2),
            item_ball(44, 11, "ITEM_SUPER_POTION", "FLAG_ICHOR_ITEM_ROUTE6_SUPER_POTION"),
            # leg D: Astylos in the cutting
            obj(P + "YOUTH_M", 31, 3, R6 + "Astylos", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3),
        ],
        "warp_events": [warp(52, 7, "MAP_ROUTE6_ANTIOPES_CAVE", 0)],
        "coord_events": [trigger(45, 20, R6 + "HeraldScene"), trigger(46, 20, R6 + "HeraldScene"),
                         trigger(8, 8, R6 + "DrumMoved", "VAR_TEMP_2")],
        "bg_events": [
            sign(43, 25, R6 + "SignSouth"),
            sign(45, 21, R6 + "VineStock", "BG_EVENT_PLAYER_FACING_NORTH"),
            hidden(23, 6, "ITEM_WINE", "FLAG_ICHOR_HIDDEN_ROUTE6_WINE"),
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
    m = Map("Eleutherai", 32, 28, "kithairon")
    # Mt. Kithairon's seam (north) is on another set: core and aethos only
    m.core_rows = set(range(0, 6))
    # The road runs north past the foot of the fort's rock (x 10-11). The fort
    # stands on that rock (tier 1, its cliff on rows 14-15), entered by a stair
    # under its gate. The god's temple is west of the road, Oinoe's house below
    # it; Lysidike's house stands in its sheep pens to the south-east.
    m.raise_(14, 0, 31, 15, 1)
    m.rect(0, 0, 31, 27, ".")
    m.rect(0, 0, 7, 5, "F")
    m.rect(0, 6, 1, 9, "F")
    m.cells([(8, 0), (8, 1), (2, 6), (3, 6)], "F")
    m.rect(10, 0, 11, 27, "=")
    # the fort's rock: firs and boulders on its top, round the walls
    m.rect(14, 0, 31, 5, "F")
    m.rect(17, 2, 28, 4, "#")
    m.cells([(16, 3), (29, 3), (22, 1), (23, 1), (24, 1)], "#")
    m.rect(14, 6, 15, 13, "F")
    m.rect(30, 6, 31, 13, "F")
    m.cells([(14, 14), (15, 14), (14, 15), (15, 15), (30, 14), (31, 14), (30, 15), (31, 15)], "F")
    m.rect(17, 8, 28, 11, "c")          # the parade ground
    # the road to the gate, and its stair
    m.rect(12, 16, 23, 17, "=")
    m.stair(23, 14, 1)
    # the temple's paving, west of the road
    m.rect(2, 11, 8, 17, "p")
    m.pavelike |= {(2, 15), (2, 16), (8, 16), (4, 12), (6, 11), (5, 13), (4, 16), (2, 11), (8, 11)}
    # the spring
    m.cells([(12, 19), (12, 20)], ".")
    # the pens: dry stone round Lysidike's house, the gate on the south
    m.rect(16, 19, 30, 19, "w")
    m.rect(16, 26, 30, 26, "w")
    m.rect(16, 19, 16, 26, "w")
    m.rect(30, 19, 30, 26, "w")
    m.rect(22, 26, 24, 26, ".")
    m.rect(17, 20, 29, 25, ".")
    m.rect(0, 24, 3, 27, "F")
    m.rect(26, 27, 31, 27, "F")
    m.cells([(0, 22), (1, 22), (6, 27), (7, 27), (31, 16), (31, 17), (31, 18)], "F")

    # the fort, on its rock: the north wall with the watch-house door, side
    # walls, towers at the south corners, the south wall with the gate
    F0 = 4                               # the polish pass moved it 4 rows south
    for x in range(17, 30):
        side = "L" if x == 17 else ("R" if x == 29 else "M")
        m.named("fort", f"W0_{side}", x, 2 + F0)
        m.named("fort", f"W1_{side}", x, 3 + F0)
    m.named("fort", "slit", 20, 2 + F0)
    m.named("fort", "slit", 26, 2 + F0)
    m.named("fort", "door", 23, 3 + F0)
    for y in (4, 5, 6):
        m.named("fort", "side", 17, y + F0)
        m.named("fort", "side", 29, y + F0)
    for tx in (17, 28):
        for i, c in enumerate(("L", "R")):
            m.named("fort", f"T0_{c}", tx + i, 7 + F0)
            m.named("fort", f"T1_{c}", tx + i, 8 + F0)
            m.named("fort", f"T2_{c}", tx + i, 9 + F0)
    for x in range(19, 28):
        if 22 <= x <= 24:
            continue
        m.named("fort", "W0_M", x, 8 + F0)
        m.named("fort", "W1_M", x, 9 + F0)
    for i, c in enumerate("LMR"):
        m.named("fort", f"gate_{c}", 22 + i, 8 + F0)
        m.named("fort", f"gateF_{c}", 22 + i, 9 + F0)
    m.no_face_decor |= {(22, 14), (24, 14), (22, 15), (24, 15)}
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
    # houses: Oinoe's below the temple, Lysidike's in the pens
    oinoe = house(m, 1, 19, 4, 2, windows=((1, "shutters"),))
    lysi = house(m, 19, 19, 5, 2, windows=((1, "lattice"), (3, "shutters")))
    # the spring's trough by the road; signs; trees
    m.stamp("trough", 13, 19)
    m.put(12, 1, L.STELE)
    m.put(9, 14, L.STELE)
    m.oak(6, 24)
    m.oak(26, 23) if False else None
    m.cypress(9, 7)
    m.cypress(13, 10)
    m.cypress(13, 6)
    m.cypress(7, 19)
    m.cypress(15, 23)
    m.olive(26, 22)
    m.olive(3, 7)
    m.pine(28, 16) if False else None
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
            obj(P + "HOPLITE", 22, 16, EL + "Sentry", "MOVEMENT_TYPE_FACE_DOWN"),
            obj(P + "KID_M", 15, 20, EL + "ShepherdBoy", "MOVEMENT_TYPE_FACE_LEFT"),
            obj(P + "ELDER_M", 14, 20, EL + "OldMan", "MOVEMENT_TYPE_FACE_UP"),
            obj("OBJ_EVENT_GFX_SPECIES(WOOLOO)", 26, 24, EL + "Sheep", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
            obj("OBJ_EVENT_GFX_SPECIES(WOOLOO)", 28, 21, EL + "Sheep", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
            obj("OBJ_EVENT_GFX_SPECIES(WOOLOO)", 18, 24, EL + "Sheep", "MOVEMENT_TYPE_FACE_RIGHT"),
        ],
        "warp_events": [
            warp(23, 3 + F0, "MAP_ELEUTHERAI_WATCH_HOUSE", 0),
            warp(*oinoe, "MAP_ELEUTHERAI_OINOE_HOUSE", 0),
            warp(*lysi, "MAP_ELEUTHERAI_LYSIDIKE_HOUSE", 0),
        ],
        "coord_events": [],
        "bg_events": [
            sign(5, 13, EL + "Plinth"),
            sign(9, 14, EL + "SignPlinth"),
            sign(12, 1, EL + "SignNorth"),
            sign(13, 19, EL + "Trough"),
            hidden(14, 19, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_ELEUTHERAI_BRONZE_OBOL"),
            hidden(30, 0, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_ELEUTHERAI_STARDUST") if False else None,
        ],
    }
    E["bg_events"] = [b for b in E["bg_events"] if b]
    views = [(10, 26), (10, 18), (6, 15), (14, 21), (23, 16), (23, 10), (21, 24), (10, 6), (10, 1)]
    return m, E, views


# ===========================================================================
# Mt. Kithairon, the maenads' pass (40 x 56)
# ===========================================================================

def kithairon():
    m = Map("MtKithairon", 40, 56, "pass")
    # Eleutherai's seam (south) and Route 7's (north): core and aethos only
    m.core_rows = set(range(0, 6)) | set(range(50, 56))
    # The climb, in tiers: the foot (0), the glade (1), the fork (2), the high
    # meadow (3), and the two shoulders of the pass (4) with the shrine's ledge.
    # Each tier's two southmost rows are its cliff; firs hide the cliffs' ends.
    m.raise_(0, 0, 39, 19, 3)
    m.raise_(0, 20, 39, 31, 2)
    m.raise_(0, 32, 39, 43, 1)
    m.raise_(0, 0, 18, 7, 4)            # the west shoulder
    m.raise_(23, 0, 39, 5, 4)           # the east shoulder
    m.raise_(28, 6, 37, 11, 4)          # ... and its ledge, where the shrine is
    m.rect(0, 0, 39, 55, "F")

    # --- the foot: switchbacks under the first cliff (tier 0) ------------------
    m.rect(15, 48, 22, 55, ".")         # leg 1, up from Eleutherai
    m.rect(3, 48, 22, 52, ".")          # leg 2, west along the foot
    m.rect(3, 44, 9, 52, ".")           # leg 3, north
    m.rect(3, 42, 20, 45, ".")          # leg 4, east under the cliff
    m.rect(10, 46, 17, 48, ".")         # the hollow between the legs
    m.rect(18, 44, 22, 47, "#")
    m.rect(18, 49, 19, 55, "=")
    m.rect(6, 49, 19, 50, "=")
    m.rect(6, 44, 7, 50, "=")
    m.rect(6, 44, 15, 45, "=")
    m.stair(14, 42)
    m.rect(3, 46, 9, 48, ",")           # band 1: across leg 3, 3 deep
    m.rect(10, 46, 17, 46, "^")         # the ledge home, over the hollow
    m.cells([(3, 44), (3, 45), (20, 42), (20, 43), (3, 52), (22, 52), (15, 55), (15, 54)], "F")
    m.cells([(13, 48), (16, 48)], "s")
    m.cells([(10, 47), (11, 47)], "L")
    # a clearing east of leg 1: optional grass, a goat track in, a Hyper Potion
    m.rect(20, 52, 24, 53, ".")
    m.rect(23, 46, 33, 53, ".")
    m.rect(25, 47, 32, 51, ",")
    m.cells([(25, 47), (26, 47), (32, 51), (31, 51), (25, 51)], ".")
    m.cells([(33, 46), (33, 47), (23, 46), (23, 47), (24, 46)], "F")
    m.cells([(29, 52), (30, 52)], "L")
    m.cells([(28, 46), (33, 52), (23, 53)], "#")
    # a nook west of leg 2: deadfall and a hidden Ether
    m.rect(1, 53, 4, 55, ".")
    m.cells([(1, 53), (2, 53)], "L")

    # --- the glade (tier 1): the fir clearing's band, the dancing floor ---------
    m.rect(10, 37, 27, 41, ".")
    m.rect(14, 41, 15, 41, "=")
    m.rect(10, 37, 19, 40, ",")         # band 2: 4 deep, firs west, rock east
    m.rect(20, 37, 22, 40, "#")
    m.rect(23, 37, 27, 37, "^")         # a ledge back down from the glade
    m.cells([(26, 40), (27, 40), (27, 39)], "s")
    m.cells([(27, 41)], "F")
    m.rect(10, 30, 33, 36, ".")         # the glade, under the second cliff
    m.rect(14, 36, 15, 36, "=")
    for y in range(32, 36):
        for x in range(11, 21):
            if ((x - 15.5) / 4.3) ** 2 + ((y - 33.6) / 2.2) ** 2 <= 1:
                m.ch[y][x] = "t"        # the dancing floor, trampled bare
    m.rect(24, 32, 25, 34, "=")
    m.stair(24, 30)
    m.cells([(10, 36), (33, 36), (33, 35), (10, 30), (10, 31), (33, 30), (33, 31)], "F")
    m.rect(28, 32, 32, 33, ",")         # long grass at the glade's back, by Bromia
    m.cells([(32, 34), (31, 36), (30, 36)], "s")
    # west of the band: a hidden clearing in the firs, through a gap
    m.rect(3, 33, 8, 37, ".")
    m.rect(9, 34, 9, 34, ".")
    m.rect(4, 34, 7, 36, ",")
    m.cells([(3, 33), (8, 37), (3, 37)], "F")
    m.cells([(5, 33), (6, 33)], "L")

    # --- the fork (tier 2): the boundary stone, Pentheus's fir, the spring -----
    m.rect(19, 20, 31, 29, ".")
    m.rect(24, 20, 25, 29, "=")
    m.stair(24, 18)
    m.rect(19, 30, 33, 31, ".")         # the cliff over the glade shows here
    m.rect(14, 25, 18, 26, "#")
    m.rect(14, 27, 14, 29, "F")
    m.rect(18, 27, 18, 29, "F")
    m.rect(15, 27, 17, 29, ".")         # the Thyrsus's ledge, over the marked ivy
    m.rect(14, 30, 18, 31, ".")
    m.rect(19, 27, 22, 29, "#")
    m.cells([(19, 26), (19, 20), (19, 21), (20, 20)], "F")
    # the drum's path, west to a rocky shelf
    m.rect(9, 24, 23, 24, "=")
    m.rect(9, 23, 18, 23, "#")
    m.rect(9, 25, 13, 25, "#")
    m.rect(4, 21, 8, 27, ".")
    m.cells([(4, 21), (8, 27), (4, 27)], "F")
    m.cells([(5, 22), (7, 26)], "#")
    m.cells([(6, 27), (5, 27)], "s")
    # east: the spring path through long grass to Aktaion's spring
    m.rect(26, 26, 31, 26, "=")
    m.rect(27, 20, 38, 29, ".")
    m.rect(28, 23, 36, 27, ",")
    m.cells([(28, 23), (29, 23), (36, 27), (35, 27)], ".")
    m.rect(33, 21, 36, 22, "~")
    m.rect(26, 28, 31, 28, "^")         # a ledge down to the glade's stair
    m.cells([(38, 20), (38, 21), (27, 20), (27, 21), (38, 29), (37, 29)], "F")
    m.cells([(37, 22)], "s")

    # --- the high meadow (tier 3): the fold, band 3, the shrine's ledge --------
    m.rect(4, 8, 38, 17, ".")
    m.rect(19, 18, 30, 19, ".")         # the third cliff shows here
    m.rect(24, 13, 25, 17, "=")
    m.rect(20, 13, 25, 14, "=")
    m.rect(20, 0, 21, 14, "=")
    # the fold: a dry-stone pen with its gate east
    m.rect(5, 9, 15, 9, "w")
    m.rect(5, 16, 15, 16, "w")
    m.rect(5, 9, 5, 16, "w")
    m.rect(15, 9, 15, 16, "w")
    m.cells([(15, 13), (15, 14)], ".")
    m.rect(16, 8, 17, 11, "#")
    m.rect(23, 6, 27, 11, "#")
    m.cells([(23, 6), (24, 6), (25, 11)], "F")
    m.rect(18, 9, 24, 11, ",")          # band 3: 3 deep, the fold's wall to the shoulder
    m.rect(29, 13, 34, 15, ",")         # long grass on the open meadow
    m.cells([(29, 13), (34, 15)], ".")
    m.cells([(37, 16), (37, 17), (38, 17), (4, 8), (4, 17), (16, 17)], "F")
    m.cells([(31, 16), (36, 13), (27, 16), (18, 16)], "s")
    # the shrine's ledge (tier 4) and its stair
    m.rect(29, 6, 36, 9, ".")
    m.stair(34, 10, 1)
    # the pass between the shoulders
    m.rect(19, 0, 22, 7, ".")
    m.rect(20, 0, 21, 7, "=")
    m.rect(0, 0, 17, 5, "F")
    m.rect(9, 0, 15, 3, "#")
    m.rect(25, 0, 33, 2, "#")
    m.cells([(16, 4), (17, 4), (24, 3), (24, 2)], "#")
    m.rect(6, 6, 18, 7, ".")            # the west shoulder's face shows here
    m.rect(23, 4, 27, 5, ".")           # and the east one's

    # stamps
    m.stamp("pentheus_fir", 26, 20)
    m.stamp("trough", 7, 10)
    m.stamp("leanto", 12, 10)
    m.stamp("pear", 8, 13)
    m.named("markers", "boundary", 26, 27)
    m.named("shrine", "seat", 32, 22)
    m.named("markers", "dig", 31, 21)
    m.named("markers", "dig", 32, 15)
    m.stamp("fir", 37, 23)
    m.named("shrine", "drum", 18, 33)
    m.named("shrine", "drum_b", 12, 32)
    m.named("shrine", "drum", 19, 35)
    m.named("shrine", "shrine_bad_top", 31, 7)
    m.named("shrine", "shrine_bad", 31, 8)
    m.face[(16, 30)] = ("cliff_marked", "marked_u")
    m.face[(16, 31)] = ("cliff_marked", "marked_l")
    m.put(22, 3, L.STELE)
    m.put(17, 54, L.STELE)
    m.put(17, 12, L.STELE)
    E = {
        "connections": [
            {"map": "MAP_ELEUTHERAI", "offset": MK_SOUTH - EL_NORTH, "direction": "down"},
            {"map": "MAP_ROUTE7_KRONIA_GROUNDS", "offset": MK_NORTH - R7_SOUTH, "direction": "up"},
        ],
        "object_events": [
            obj(P + "GOATHERD", 10, 48, MK + "Lykidas", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2),
            obj(P + "MAENAD", 26, 32, MK + "Euia", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2,
                local_id="LOCALID_KITHAIRON_EUIA"),
            obj(P + "MAENAD", 31, 34, MK + "Bromia", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=3,
                local_id="LOCALID_KITHAIRON_BROMIA"),
            obj(P + "MAENAD", 14, 33, MK + "Maenad", "MOVEMENT_TYPE_FACE_RIGHT",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_MAENAD_1"),
            obj(P + "MAENAD", 16, 32, MK + "Maenad", "MOVEMENT_TYPE_FACE_DOWN",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_MAENAD_2"),
            obj(P + "MAENAD", 15, 35, MK + "Maenad", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_MAENAD_3"),
            obj("OBJ_EVENT_GFX_SPECIES(BOTRYKIT)", 13, 34, MK + "Botrykit", "MOVEMENT_TYPE_FACE_RIGHT",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_BOTRYKIT_1"),
            obj("OBJ_EVENT_GFX_SPECIES(BOTRYKIT)", 17, 34, MK + "Botrykit", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_ICHOR_SAW_MAENADS", local_id="LOCALID_KITHAIRON_BOTRYKIT_2"),
            item_ball(20, 32, "ITEM_REVIVE", "FLAG_ICHOR_ITEM_KITHAIRON_REVIVE"),
            item_ball(16, 28, "ITEM_MAX_ELIXIR", "FLAG_ICHOR_ITEM_KITHAIRON_MAX_ELIXIR"),
            obj(P + "HOPLITE", 23, 23, MK + "Arimnestos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=1),
            obj("OBJ_EVENT_GFX_PUSHABLE_BOULDER", 12, 24, "EventScript_StrengthBoulder",
                "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_ICHOR_HIDE_KITHAIRON_DRUM",
                local_id="LOCALID_KITHAIRON_DRUM"),
            item_ball(5, 24, "ITEM_MAX_REVIVE", "FLAG_ICHOR_ITEM_KITHAIRON_MAX_REVIVE"),
            # ICHOR_STUB_TMS: Venoshock has no TM number yet (SCRIPT.md region A, open question 17)
            item_ball(37, 27, "ITEM_TM_SLUDGE_BOMB", "FLAG_ICHOR_ITEM_KITHAIRON_TM_VENOSHOCK"),
            item_ball(31, 48, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_KITHAIRON_HYPER_POTION"),
            item_ball(5, 35, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_KITHAIRON_ULTRA_BALL"),
            obj(P + "SHEPHERD", 16, 13, MK + "Phorbas", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("OBJ_EVENT_GFX_SPECIES(WOOLOO)", 10, 14, MK + "Sheep", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1),
            obj("OBJ_EVENT_GFX_SPECIES(WOOLOO)", 7, 13, MK + "Sheep", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj(P + "TITAN_GRUNT", 33, 8, MK + "Ilys", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2),
        ],
        "warp_events": [],
        "coord_events": [trigger(x, 36, MK + "DancingFloor") for x in (14, 15)]
        + [trigger(12, 24, MK + "DrumMoved", "VAR_TEMP_2")],
        "bg_events": [
            sign(17, 54, MK + "SignSouth"),
            sign(16, 31, MK + "MarkedIvy"),
            sign(26, 27, MK + "BoundaryStone"),
            sign(27, 23, MK + "PentheusFir"),
            sign(32, 22, MK + "SpringSeat"),
            sign(34, 22, MK + "Spring"),
            sign(35, 22, MK + "Spring"),
            sign(37, 25, MK + "Arrow"),
            sign(31, 21, MK + "SpringDig"),
            sign(32, 15, MK + "DigSpot"),
            sign(17, 12, MK + "SignFold"),
            sign(31, 8, MK + "Shrine"),
            sign(22, 3, MK + "SignNorth"),
            hidden(36, 23, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_HIDDEN_KITHAIRON_PRETTY_FEATHER"),
            hidden(26, 23, "ITEM_HONEY", "FLAG_ICHOR_HIDDEN_KITHAIRON_HONEY"),
            hidden(2, 55, "ITEM_ETHER", "FLAG_ICHOR_HIDDEN_KITHAIRON_ETHER"),
            hidden(36, 6, "ITEM_RARE_CANDY", "FLAG_ICHOR_HIDDEN_KITHAIRON_RARE_CANDY"),
        ],
    }
    views = [(18, 54), (10, 50), (7, 46), (13, 44), (15, 39), (15, 35), (25, 33), (24, 25), (12, 24),
             (32, 24), (25, 16), (12, 12), (21, 10), (32, 8), (21, 3)]
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
    # pass 2: the Asopos narrower, its west bank wandering; the reed islet midstream;
    # band 2 fenced by scrub (firs) instead of walls
    bank = [0, 0, -1, -1, -1, 0, 0, 1, 1, 0, 0, -1, -2, -2, -1, -1, 0, 0, 0, 1, 1, 1, 0, 0, -1, -1, 0, 0]
    for y in range(6, 34):
        xw = 38 + bank[y - 6]
        for x in range(35, 44):
            if x >= xw:
                m.ch[y][x] = "~"
            elif m.ch[y][x] == "~":
                m.ch[y][x] = "," if 17 <= y <= 30 else "."
    m.rect(40, 19, 41, 20, ".")
    # polish pass: the north face redrawn. Two rock walls make the defile at the
    # mountain's lip (tier 1: their cliffs face you as you come over the pass);
    # the road winds down through Komos's band, west along the slope past
    # Hagnon, north through the west meadow's band beside a mountain brook, and
    # east into the camp. The brook feeds a pond at the camp's corner.
    m.rect(0, 17, 34, 39, "F")
    m.rect(35, 34, 43, 39, "F")
    m.raise_(11, 29, 18, 37, 1)          # the defile's west wall
    m.raise_(22, 29, 30, 37, 1)          # ... and its east wall
    m.rect(12, 30, 17, 35, "#")
    m.cells([(12, 30), (17, 33), (13, 33), (12, 34), (12, 35), (16, 31)], "F")
    m.rect(23, 30, 28, 35, "#")
    m.cells([(28, 30), (23, 33), (28, 33), (28, 34), (28, 35), (25, 31)], "F")
    m.rect(13, 36, 18, 37, ".")          # the walls' cliffs show here
    m.rect(22, 36, 28, 37, ".")
    m.rect(13, 38, 28, 39, ".")          # the defile's mouth, at the lip
    m.cells([(13, 38), (13, 39), (14, 39), (28, 38), (28, 39), (27, 39)], "F")
    m.cells([(15, 38), (25, 39)], "s")
    m.cells([(23, 38), (24, 38)], "L")
    m.rect(19, 29, 21, 37, ".")          # the defile itself, three wide
    # the slopes: leg A down to the bend, leg B west, the west meadow (leg C),
    # leg D east into the camp
    m.rect(18, 24, 22, 28, ".")
    m.rect(6, 23, 22, 26, ".")
    m.rect(14, 26, 17, 28, ".")          # the lost pilgrim's nook
    m.cells([(14, 28), (17, 28)], "F")
    m.rect(5, 17, 12, 28, ".")
    m.rect(11, 27, 13, 28, "F")
    m.rect(13, 19, 22, 22, "F")          # scrub between the legs
    m.rect(5, 17, 22, 18, ".")
    m.rect(3, 13, 4, 28, "~")            # the brook, off the mountain
    m.rect(1, 13, 4, 15, "~")            # ... into a pond at the camp's corner
    m.cells([(1, 13), (4, 13)], ".")
    m.rect(0, 17, 2, 28, "F")
    # the road
    m.rect(20, 24, 21, 39, "=")
    m.rect(9, 24, 21, 25, "=")
    m.rect(9, 17, 10, 25, "=")
    m.rect(9, 17, 21, 18, "=")
    # grass: the two bands, and long grass at the meadow's dead end
    m.rect(19, 29, 21, 32, ",")          # band 1: 4 deep, below Komos, walled by the rock
    m.rect(5, 19, 12, 21, ",")           # band 2: 3 deep, from the brook to the scrub
    m.rect(6, 26, 8, 28, ",")
    m.cells([(12, 22), (11, 22)], "s")
    # the riverside pasture, east, off the herm's side path: long grass, a rock
    # ledge down toward the beach
    m.rect(24, 17, 34, 23, ".")
    m.rect(28, 18, 34, 22, ",")
    m.rect(24, 20, 27, 20, "n")
    m.cells([(24, 23), (25, 23), (34, 23)], "F")
    m.cells([(26, 22)], "s")
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
    for (x, y) in ((11, 11), (14, 11), (33, 10), (10, 7), (17, 10), (34, 6)):
        m.stamp("tent", x, y)
    m.olive(11, 14)
    m.stamp("banner", 15, 13)
    m.named("camp_small", "board", 19, 15)
    m.named("camp_small", "hoop", 6, 15)
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
    m.put(18, 38, L.STELE)
    m.oak(7, 13) if False else None
    E = {
        "connections": [
            {"map": "MAP_MT_KITHAIRON", "offset": R7_SOUTH - MK_NORTH, "direction": "down"},
            {"map": "MAP_THYRSA_CITY", "offset": -6, "direction": "up"},
        ],
        "object_events": [
            # the north face
            obj(P + "SATYR", 19, 34, R7 + "Komos", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=2),
            obj(P + "YOUTH_F", 16, 27, R7 + "LostPilgrim", "MOVEMENT_TYPE_FACE_DOWN"),
            item_ball(5, 28, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_ROUTE7_FULL_HEAL"),
            obj(P + "MAN", 12, 26, R7 + "Hagnon", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=2),
            # beat 29: the greeter, Kleon and Alethea at the tables, the reader
            obj(P + "KRONIST", 23, 15, R7 + "Greeter", "MOVEMENT_TYPE_FACE_DOWN",
                local_id="LOCALID_ROUTE7_GREETER"),
            obj(P + "KLEON_FEAST", 26, 13, R7 + "Kleon", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_HIDE_KLEON_KRONIA", local_id="LOCALID_ROUTE7_KLEON"),
            obj(P + "ALETHEA", 28, 13, R7 + "Alethea", "MOVEMENT_TYPE_FACE_UP",
                flag="FLAG_ICHOR_HIDE_ALETHEA_KRONIA", local_id="LOCALID_ROUTE7_ALETHEA"),
            obj(P + "KRONIST", 31, 15, R7 + "Reader", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_TEMP_4", local_id="LOCALID_ROUTE7_READER"),
            obj(P + "KRONIST", 31, 15, R7 + "ReaderAfter", "MOVEMENT_TYPE_FACE_LEFT",
                flag="FLAG_TEMP_5", local_id="LOCALID_ROUTE7_READER_AFTER"),
            obj(P + "KRONIST", 26, 8, R7 + "StageKronist", "MOVEMENT_TYPE_FACE_DOWN"),
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
            item_ball(40, 19, "ITEM_BIG_PEARL", "FLAG_ICHOR_ITEM_ROUTE7_BIG_PEARL"),
        ],
        "warp_events": [],
        "coord_events": [trigger(x, 16, R7 + "GreeterScene") for x in (20, 21)]
        + [trigger(x, 12, R7 + "KleonScene", "VAR_TEMP_2") for x in (20, 21, 22, 23)],
        "bg_events": [
            sign(18, 38, R7 + "SignSouth"),
            hidden(37, 16, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_ROUTE7_BRONZE_OBOL"),
            hidden(14, 8, "ITEM_CHARCOAL", "FLAG_ICHOR_HIDDEN_ROUTE7_CHARCOAL"),
            hidden(36, 33, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_ROUTE7_PEARL"),
            sign(24, 15, R7 + "GreatHerm"),
            sign(19, 15, R7 + "SignKronia"),
            sign(16, 14, R7 + "Banner"),
            sign(29, 15, R7 + "ReaderTable"),
            sign(30, 15, R7 + "ReaderTable"),
            sign(31, 8, R7 + "StewardsTent"),
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

# Where the player enters each map, and what is meant to be out of reach on foot
# today (relic gates, the reed islet), for the reachability check below.
ENTRIES = {
    "route6": [(45, 27), (46, 27)],
    "cave": [(7, 11)],
    "eleutherai": [(10, 27), (11, 27)],
    "kithairon": [(18, 55), (19, 55)],
    "route7": [(20, 39), (21, 39)],
}
UNREACHABLE_OK = {
    "route6": {(5, 8)},                        # the Max Ether, behind the drum (the Girdle)
    "eleutherai": set(),
    "kithairon": {(5, 24), (16, 28)},          # the Max Revive (the Girdle), the Max Elixir (the Thyrsus)
    "route7": {(40, 19)},                      # the Big Pearl on the reed islet (the Conch)
    "cave": {(14, 3)},                         # the Star Piece on the ivy ledge (the Thyrsus)
}


# Cells scripts open: the vines and the barrier (and the herald, who leaves).
OPENS = {"route6": {(46, 21), (45, 18), (46, 18), (45, 17), (8, 8)},
         "kithairon": {(12, 24), (16, 32), (15, 35), (14, 33), (13, 34), (17, 34)}}


def check_reach(key):
    def run(m, E):
        # people stand on tiles: treat their tiles as blocked while walking
        people = {(o["x"], o["y"]) for o in E.get("object_events", [])}
        opens = OPENS.get(key, set())
        m.force_open |= opens
        seen = L.reach(m, ENTRIES[key], blocked_extra=people - opens)
        m.force_open -= opens
        bad = []
        targets = [(o["x"], o["y"], o["script"].split("_")[-1]) for o in E.get("object_events", [])]
        targets += [(b["x"], b["y"], b.get("script", b.get("flag", "?")).split("_")[-1])
                    for b in E.get("bg_events", [])]
        for (x, y, what) in targets:
            near = {(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))}
            if not (near & seen) and (x, y) not in UNREACHABLE_OK.get(key, ()):
                bad.append(f"{what}@{x},{y}")
        for e in E.get("coord_events", []) + E.get("warp_events", []):
            if (e["x"], e["y"]) not in seen and not ({(e["x"], e["y"] + 1), (e["x"], e["y"] - 1)} & seen):
                bad.append(f"event@{e['x']},{e['y']}")
        print(f"  {m.name}: {len(seen)} cells reachable" + (f"; OUT OF REACH: {', '.join(bad)}" if bad else ""))
        # forced grass (MAP_DESIGN section 1): the grass patches every walk from the
        # entry to the far exit must cross
        if key in EXITS:
            grass = L.grass_cells(m)
            parts, left = [], set(grass)
            while left:
                c = left.pop()
                part, todo = {c}, [c]
                while todo:
                    x, y = todo.pop()
                    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                        n = (x + dx, y + dy)
                        if n in left:
                            left.discard(n)
                            part.add(n)
                            todo.append(n)
                parts.append(part)
            m.force_open |= opens
            forced = []
            for part in parts:
                r = L.reach(m, ENTRIES[key], blocked_extra=(people - opens) | part)
                if not (set(EXITS[key]) & r):
                    xs = sorted({x for x, _ in part}); ys = sorted({y for _, y in part})
                    forced.append(f"x {xs[0]}-{xs[-1]}, y {ys[0]}-{ys[-1]}")
            m.force_open -= opens
            print(f"  {m.name}: forced grass bands: {'; '.join(forced) if forced else 'NONE'}")
    return run


# The far exit of each route, for the forced-grass check.
EXITS = {"route6": [(32, 0), (33, 0)], "kithairon": [(20, 0), (21, 0)], "route7": [(20, 0), (21, 0)]}


CHECKS = {k: check_reach(k) for k in ENTRIES}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapes", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    build(args.only.split(",") if args.only else None, args.shapes, args.tag)


if __name__ == "__main__":
    main()
