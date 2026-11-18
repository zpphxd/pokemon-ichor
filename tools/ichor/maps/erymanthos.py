#!/usr/bin/env python3
"""Build the Erymanthian Preserve, Artemis's hunting park on Mount Erymanthos beside
Arkadia: Ichor's Safari Zone (design/DISTRIBUTION.md §4, design/maps/ErymanthosPreserve.md).

This file owns the Preserve's six maps (their layouts, events, scripts and checks) and
writes the lodge's hut into Arkadia's west road. The wild tables are
tools/ichor/wild_plan.py's (the distribution pass); the engine is upstream's Safari Zone,
switched back on in include/config/ichor.h (ICHOR_SAFARI_PRESERVE).

The lodge (11x8, Arkadia's charcoal-hut room). *A hunters' hut dug into the hill at the
west road's end.* Melanippe, Artemis's keeper, takes the fee (¥500) and hands over 30 Pan
Balls; the hunt lasts 500 steps. The hut's wall carries the old drawing of the mountain.

The Oakwood (40x34). *Holm oaks and walnuts round glades of tall grass.* The keeper's bell
at the gate (ring it to leave), the long glade the road climbs through, Artemis's spring in
the west glade, the clearing of long grass, and two roads out: up to the High Meadow, east
to the river.

The High Meadow (40x30). *Above the trees, under the snowline.* Long grass wall to wall,
a limestone band with a stair cut through it, scree, the cold cave's mouth in a crag, and
in the top corner a gap the boar has choked with fallen oaks: the Thicket, after Labor 4.

The River (32x34). *The Erymanthos coming down off the mountain.* Reeds, a sand bar, a
ford, an angler's stilt hut and the far bank's long grass. Rods work from every bank; the
Conch takes you onto the water.

The Cold Cave (26x18, cave_dark). *A seep cave where the frost never leaves.* Pagoshard.

The Boar's Thicket (26x22, post-game). *Rooted-up oaks round the boar's wallow.* Sealed
until the Erymanthian Boar is caught (FLAG_ICHOR_ERYMANTHIAN_BOAR, LABORS.md Labor 4);
Atalanta's cairn.

Usage: /usr/bin/python3 tools/ichor/maps/erymanthos.py [--render DIR] [--walk] [--only STEMS]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import route5 as R5  # noqa: E402
import kopais as KP  # noqa: E402  (the Stymphalia painter, Spec, Walked, renders)
import stymphalia as ST  # noqa: E402  (its Grid, painter extras, Spec, checks)

noise = R5.noise
STYM = "gTileset_Stymphalia"
smid = KP.smid
SIGN = R5.SIGN

LODGE, OAK, MEADOW, RIVER, CAVE, THICKET = ("ErymanthosPreserve_Lodge", "ErymanthosPreserve_Oakwood",
                                            "ErymanthosPreserve_Meadow", "ErymanthosPreserve_River",
                                            "ErymanthosPreserve_Cave", "ErymanthosPreserve_Thicket")
MAP = {n: "MAP_" + KP.const(n) for n in (LODGE, OAK, MEADOW, RIVER, CAVE, THICKET)}

FEE = 500
ARRIVAL = (19, 30)                 # where the keeper leaves you in the Oakwood, facing north
LODGE_BACK = (5, 5)                # where the hunt ends, in the lodge (data/scripts/safari_zone.inc)
LODGE_HUT = (3, 33)                # the hut's 4x3 front on Arkadia's west road; its door is (5, 35)
FLAG_BOAR = "FLAG_ICHOR_ERYMANTHIAN_BOAR"

# ---------------------------------------------------------------------------
# Flags: claimed from world-act2's bank range (tools/ichor/claim_ranges.md)
# ---------------------------------------------------------------------------
BANK_RANGE = "0x500-0x63F"
POSTGAME_RANGE = "0x700-0x7FF"
FLAG_NOTES = {}


def flag(name, note, rng=BANK_RANGE):
    FLAG_NOTES[name] = (note, rng)
    return name


def claim_flags():
    text = (ROOT / "include/constants/flags.h").read_text()
    for name, (note, rng) in FLAG_NOTES.items():
        if re.search(rf"#define {name}\b", text):
            continue
        kind = "hiddenitem" if name.startswith("FLAG_ICHOR_HIDDEN_ITEM_") else "bankflag"
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/claim.py"), "--range", rng, kind, name,
                        "Erymanthian Preserve: " + note], check=True, capture_output=True)
        text = (ROOT / "include/constants/flags.h").read_text()


flag(FLAG_BOAR, "the Erymanthian Boar caught (Labor 4, LABORS.md); opens the Preserve's thicket", POSTGAME_RANGE)


def item_flag(what, note):
    return flag(f"FLAG_ICHOR_ITEM_ERYMANTHOS_{what}", note)


def hidden_flag(what, note):
    return flag(f"FLAG_ICHOR_HIDDEN_ITEM_ERYMANTHOS_{what}", note)


class Spec(ST.Spec):
    pass


def write_events(spec, music, map_type, header=None, extra=None):
    KP.write_events(spec, music, map_type, header=header, extra=extra)
    p = ROOT / f"data/maps/{spec.name}/scripts.pory"
    p.write_text(p.read_text().replace("tools/ichor/maps/kopais.py", "tools/ichor/maps/erymanthos.py"))


def canopy(g, salt):
    """Close the woods: holm oaks on a staggered 2x2 lattice, with walnuts and planes
    among them, before the painter fills what's left (pines, cypresses, scrub)."""
    T = "trees"
    holm = [("holm_TL", 0, 0), ("holm_TR", 1, 0), ("holm_BL", 0, 1), ("holm_BR", 1, 1)]
    for y in range(0, g.h - 1, 2):
        for x in range((y // 2) % 2, g.w - 1, 2):
            if not g.room(x, y, 2, 2, "#"):
                continue
            n = noise(x, y, salt)
            if n < 10 and g.room(x, y, 3, 3, "#"):
                g.spiece(T, x, y, [(f"walnut_{i}{j}", i, j) for i in range(3) for j in range(3)], True)
            elif n < 16 and g.room(x, y, 3, 3, "#"):
                g.spiece("plane", x, y, [(f"plane_{i}{j}", i, j) for i in range(3) for j in range(3)], True)
            elif n < 82:
                g.spiece(T, x, y, holm, True)


def outdoor(name, g, props, border, salt=0):
    g.pines = 42                   # more holm oak and walnut than pine: an oak wood

    def all_props(g):
        props(g)
        canopy(g, 140 + salt)
    ST.paint(g, all_props)
    blocks = g.blocks()
    KP.write_layout(name, blocks, [border | (1 << 10)] * 4, "gTileset_Aethos", STYM)
    return blocks


def bell(s, x, y):
    """The keeper's bell, on a post: ring it to end the hunt."""
    s.sign(x, y, "Bell")
    s.script("Bell", f'''    lockall
    msgbox(format("A bronze bell hangs from the post. Ring it, and the keeper comes to walk you out.\\p"
                  "Ring the bell and end the hunt?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        playse(SE_DING_DONG)
        waitse
        goto(SafariZone_EventScript_Exit)
    }}
    releaseall''')


EXTRA_ROUTE = {"ichor_kind": "safari", "show_map_name": False, "allow_cycling": False, "allow_running": True, "allow_escaping": False}

# ---------------------------------------------------------------------------
# The Oakwood (40x34). The High Meadow is north (our x 12-13 at the top = its 12-13);
# the River is east (our rows 12-13 at the edge = its rows 12-13).
# ---------------------------------------------------------------------------
OAK_W, OAK_H = 40, 34
OAK_SPRING = (5, 7)
OAK_SIGN = (17, 28)
OAK_BELL = (22, 31)
OAK_SIGN_E = (36, 11)


def plan_oak():
    W, H = OAK_W, OAK_H
    g = ST.Grid(OAK, W, H)
    g.rect("#", 0, 0, W - 1, H - 1)
    # --- the gate's glade (rows 26-32): the bell, the keeper's posts ----------------------
    g.blob(".", 19, 29, 6, 3, salt=1)
    g.rect(".", 16, 28, 26, 31)
    g.rect("#", 15, 32, 26, 33)                    # the oaks close behind the gate
    g.rect("p", 19, 26, 20, 32)
    g.put("k", OAK_SIGN, OAK_BELL, (18, 32), (21, 32), OAK_SIGN_E)
    # --- the long glade (rows 19-25): the road climbs through tall grass -----------------
    g.blob(",", 11, 22, 8, 3, salt=2)
    g.blob(",", 26, 23, 6, 3, salt=3)
    g.blob(",", 19, 22, 5, 2, salt=10)
    g.rect("p", 19, 19, 20, 25)
    g.blob(".", 4, 24, 2, 3, salt=11)
    g.blob(",", 7, 27, 3, 2, salt=4)              # a pocket off the glade's west end
    g.put(".", (3, 22), (4, 22))
    # --- the crossroads and the clearing of long grass (rows 10-18) ----------------------
    g.rect("p", 12, 17, 27, 18)
    g.blob(";", 19, 13, 7, 3, salt=5)
    g.blob(".", 15, 15, 2, 1, salt=12)
    # --- the west glade and Artemis's spring (rows 4-14) ---------------------------------
    g.blob(".", 6, 9, 4, 4, salt=6)
    g.blob(",", 5, 13, 3, 2, salt=13)
    g.put("k", OAK_SPRING, (OAK_SPRING[0] + 1, OAK_SPRING[1]), (OAK_SPRING[0], OAK_SPRING[1] + 1),
          (OAK_SPRING[0] + 1, OAK_SPRING[1] + 1))
    g.rect(".", 9, 9, 11, 10)
    g.blob(",", 10, 15, 1, 1, salt=14)
    g.rect(".", 10, 11, 11, 14)
    # --- the road north to the meadow (x 12-13), through a band of tall grass -------------
    g.rect("p", 12, 0, 13, 18)
    g.blob(",", 12, 4, 4, 2, salt=15)
    g.rect("p", 12, 0, 13, 2)
    # --- the east road to the river (rows 12-13) and the north-east glade ---------------
    g.rect("p", 26, 12, 27, 18)
    g.rect("p", 26, 12, W - 1, 13)
    g.blob(",", 32, 7, 5, 3, salt=7)
    g.blob(".", 31, 10, 2, 1, salt=16)
    g.blob(",", 33, 16, 4, 2, salt=8)
    # --- the south-east glade (rows 22-30), off the long glade ---------------------------
    g.blob(",", 32, 27, 5, 3, salt=9)
    g.put(".", (35, 28), (36, 28))
    return g


def props_oak(g):
    g.set(*OAK_SIGN, SIGN, True)
    g.set(*OAK_SIGN_E, SIGN, True)
    g.spiece("odds", *OAK_BELL, [("post", 0, 0)])
    g.spiece("odds", 18, 32, [("post", 0, 0)])
    g.spiece("odds", 21, 32, [("post", 0, 0)])
    g.spiece("spring", *OAK_SPRING)
    g.spiece("odds", 8, 6, [("stele", 0, 0)]) if g.at(8, 6) == "#" else None


def spec_oak():
    s = Spec(OAK)
    s.connections = [{"direction": "up", "map": MAP[MEADOW], "offset": 0},
                     {"direction": "right", "map": MAP[RIVER], "offset": 0}]
    s.sign(*OAK_SIGN, "Sign", text="THE ERYMANTHIAN PRESERVE\\nArtemis's own woods. Take only what she lets you catch.")
    bell(s, *OAK_BELL)
    s.sign(OAK_SPRING[0], OAK_SPRING[1] + 1, "Spring", "NORTH",
           text="A spring under the oaks, with a bow and a crescent cut in the stone above it. "
                "The water is very cold.")
    s.sign(OAK_SPRING[0] + 1, OAK_SPRING[1] + 1, "Spring", "NORTH")
    s.person("Huntress", "ACOLYTE_F", 24, 28, "LEFT")
    s.script("Huntress", '''    lock
    faceplayer
    msgbox(format("First hunt? Throw barley and it stays to eat, but it's harder to catch. Throw a stone "
                  "and it's easier to catch, and readier to run.\\p"
                  "Owls and wolves come out at night. The meadow's cold birds, up top. And the river...\\p"
                  "Fish the river at any hour. Somebody once pulled up something with more than one head."))
    release''')
    s.item("ITEM_BIG_MUSHROOM", 36, 28, item_flag("OAK_GLADE", "the Oakwood's south-east glade"))
    s.item("ITEM_TINY_MUSHROOM", 3, 22, item_flag("OAK_POCKET", "the long glade's west pocket"))
    s.hide("ITEM_MOON_STONE", 7, 9, hidden_flag("OAK_SPRING", "beside Artemis's spring"))
    s.hide("ITEM_ETHER", 33, 9, hidden_flag("OAK_NE", "the north-east glade"))
    s.sign(*OAK_SIGN_E, "SignRiver", text="TO THE RIVER\\nThe Erymanthos, and the swans' shallows.")
    return s


def build_oak():
    g = plan_oak()
    blocks = outdoor(OAK, g, props_oak, R5.CYPRESS_TOP, 1)
    s = spec_oak()
    write_events(s, "MUS_ICHOR_ROAD", "MAP_TYPE_ROUTE", extra=dict(EXTRA_ROUTE, weather="WEATHER_SUNNY"))
    m = ST.Walk(OAK, blocks, STYM, s, g)
    gate = [ARRIVAL]
    north = [(x, 0) for x in (12, 13)]
    east = [(OAK_W - 1, y) for y in (12, 13)]
    views = [("1 the gate and the bell", 20, 29), ("2 the long glade", 19, 22), ("3 the crossroads", 19, 17),
             ("4 the clearing", 19, 12), ("5 Artemis's spring", 6, 9), ("6 the road north", 12, 4),
             ("7 the east road", 33, 12), ("8 the north-east glade", 32, 7), ("9 the south-east glade", 32, 26)]
    return m, [("the gate to the meadow", gate, north), ("the gate to the river", gate, east)], views, "oakwood", set()


# ---------------------------------------------------------------------------
# The High Meadow (40x30). The Oakwood is south (our x 12-13 at the bottom); the
# Thicket is north (our x 6 at the top = its 6).
# ---------------------------------------------------------------------------
MEA_W, MEA_H = 40, 30
MEA_MOUTH = (31, 8)                # the cold cave's mouth, in the crag's foot; the warp is here
MEA_OAKS = (6, 2)                  # the fallen oaks across the thicket's gap
MEA_SIGN = (14, 25)
MEA_SIGN_TOP = (8, 4)


def plan_meadow():
    W, H = MEA_W, MEA_H
    g = ST.Grid(MEADOW, W, H)
    g.rect("#", 0, 0, W - 1, H - 1)
    # --- the lower meadow (rows 17-26): long grass, tall-grass hollows, open knolls -------
    g.rect(";", 2, 17, 37, 25)
    g.blob(";", 20, 22, 17, 4, salt=11)
    g.blob(",", 7, 21, 4, 3, salt=12)
    g.blob(",", 30, 20, 5, 2, salt=13)
    g.blob(",", 22, 24, 4, 1, salt=14)
    g.blob(".", 17, 19, 3, 1, salt=19)
    g.blob(".", 34, 24, 2, 1, salt=20)
    g.rect("#", 38, 17, W - 1, 26)
    for x in range(2, 38):                         # the trees' ragged upper edge
        if noise(x, 26, 15) < 40 and g.at(x, 26) == ";":
            g.put("#", (x, 26))
    g.blob(".", 12, 25, 3, 1, salt=21)
    g.rect("p", 12, 18, 13, H - 1)
    g.put("k", MEA_SIGN)
    # --- the limestone band (rows 12-16): a stair cut through, a ledge to hop back down ----
    for x in range(W):
        jag = x in range(2, 10) or x in range(15, 21) or x in range(33, 37)  # not by the stair or the ledge
        top = 12 + (1 if noise(x, 12, 90) < 30 and jag else 0)
        bot = 16 - (1 if noise(x, 16, 91) < 30 and jag else 0)
        g.rect("^", x, top, x, bot)
        if top > 12:
            g.put(";", (x, 12))
        if bot < 16:
            g.put(";", (x, 16))
        if noise(x, 14, 92) < 22 and jag:             # a cleft bites into the face
            g.put(";", (x, bot))
    g.rect("S", 12, 12, 12, 16)
    g.rect("v", 22, 16, 30, 16)
    g.rect(".", 22, 15, 30, 15)
    g.rect(";", 22, 13, 30, 14)
    g.rect(".", 22, 12, 30, 12)
    g.put("^", (22, 13), (30, 13), (22, 14), (30, 14))
    # --- the upper meadow (rows 2-11): long grass, scree, the cold birds' ground -----------
    g.rect(";", 2, 3, 36, 11)
    g.blob(",", 18, 6, 6, 2, salt=16)
    g.blob(".", 23, 10, 3, 1, salt=22)
    g.blob("q", 9, 8, 3, 2, salt=17)
    g.blob("q", 34, 10, 2, 1, salt=18)
    g.rect("p", 12, 9, 13, 11)
    g.blob(".", 6, 4, 3, 2, salt=23)
    g.put("k", MEA_SIGN_TOP)
    # --- the crag and the cold cave --------------------------------------------------------
    g.blob("^", 31, 4, 5, 3, salt=24)
    g.rect("^", 27, 3, 35, 8)
    g.rect(".", 29, 9, 33, 9)
    g.put("k", MEA_MOUTH, (MEA_MOUTH[0], MEA_MOUTH[1] - 1))
    g.rect("#", 37, 0, W - 1, 11)
    g.rect("#", 2, 0, 36, 1)
    # --- the thicket's gap: one cell wide, choked with fallen oaks -----------------------
    g.rect("p", MEA_OAKS[0], 0, MEA_OAKS[0], 3)
    return g


def props_meadow(g):
    g.set(*MEA_SIGN, SIGN, True)
    g.set(*MEA_SIGN_TOP, SIGN, True)
    g.set(MEA_MOUTH[0], MEA_MOUTH[1] - 1, R5.CAVE_TOP, True)
    g.set(*MEA_MOUTH, R5.CAVE_DOOR, False)
    for x, y in ((24, 9), (35, 21), (5, 24), (16, 4)):
        if g.at(x, y) in (";", ","):
            g.spiece("taygetos", x, y, [("boulder", 0, 0)])
    g.spiece("taygetos", 10, 7, [("boulders", 0, 0)])


def spec_meadow():
    s = Spec(MEADOW)
    s.connections = [{"direction": "down", "map": MAP[OAK], "offset": 0},
                     {"direction": "up", "map": MAP[THICKET], "offset": 0}]
    s.warps = [KP.warp(*MEA_MOUTH, CAVE, 0)]
    s.sign(*MEA_SIGN, "Sign", text="THE HIGH MEADOW\\nAbove the trees the wind comes off the snow. "
                                    "The cold birds nest here.")
    s.sign(*MEA_SIGN_TOP, "SignTop", text="KEEP OUT. THE BOAR'S GROUND.\\nBy order of the keeper. "
                                          "Nobody has caught it. Nobody should try.")
    s.person("FallenOaks", "OBJ_EVENT_GFX_CUTTABLE_TREE", *MEA_OAKS, "DOWN", FLAG_BOAR)
    s.script("FallenOaks", '''    lockall
    msgbox(format("Young oaks lie across the gap, torn up by the roots. Their bark is scored with tusks "
                  "as long as your arm.\\p"
                  "No blade will clear these. Something has to be done about whatever tore them up."))
    releaseall''')
    s.person("Herder", "GOATHERD", 16, 10, "DOWN")
    s.script("Herder", '''    lock
    faceplayer
    msgbox(format("I graze my goats up here in summer. Not by the gap. Never by the gap.\\p"
                  "The boar came down off Erymanthos the year my father was born. Herakles himself "
                  "dragged it off, they say. Then another came. There's always another."))
    release''')
    s.item("ITEM_NEVER_MELT_ICE", 34, 10, item_flag("MEADOW_SCREE", "the high meadow's east scree"))
    s.item("ITEM_REVIVE", 3, 23, item_flag("MEADOW_LOW", "the lower meadow's west corner"))
    s.hide("ITEM_STARDUST", 26, 12, hidden_flag("MEADOW_LEDGE", "the ledge over the band"))
    s.hide("ITEM_ICE_STONE", 9, 9, hidden_flag("MEADOW_SCREE_W", "the west scree"))
    return s


def build_meadow():
    g = plan_meadow()
    blocks = outdoor(MEADOW, g, props_meadow, R5.CYPRESS_TOP, 2)
    s = spec_meadow()
    write_events(s, "MUS_ICHOR_ROAD", "MAP_TYPE_ROUTE", extra=dict(EXTRA_ROUTE, weather="WEATHER_SUNNY"))
    m = ST.Walk(MEADOW, blocks, STYM, s, g)
    south = [(x, MEA_H - 1) for x in (12, 13)]
    views = [("1 from the oakwood", 12, 25), ("2 the lower meadow", 24, 21), ("3 the stair", 12, 14),
             ("4 the ledge", 26, 14), ("5 the upper meadow", 19, 7), ("6 the cold cave", 31, 9),
             ("7 the boar's gap", 7, 3), ("8 the east scree", 35, 5)]
    return m, [("the oakwood to the cave", south, [(MEA_MOUTH[0], MEA_MOUTH[1] + 1)]),
               ("the oakwood to the gap", south, [(MEA_OAKS[0], MEA_OAKS[1] + 1)])], views, "meadow", set()


# ---------------------------------------------------------------------------
# The River (32x34). The Oakwood is west (our rows 12-13 at the left edge).
# ---------------------------------------------------------------------------
RIV_W, RIV_H = 32, 34
RIV_HUT = (23, 5)                  # the angler's stilt hut, 3x3
RIV_SIGN = (4, 11)
RIV_FORD = (22, 23)


def river_x(y):
    """The river's west edge at row y: it swings east, then back."""
    return 12 + (0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                 0, 0, 0)[y]


def plan_river():
    W, H = RIV_W, RIV_H
    g = ST.Grid(RIVER, W, H)
    g.rect("#", 0, 0, W - 1, H - 1)
    # --- the west bank: the road in from the oakwood, down to the ford -----------------
    for y in range(3, 31):
        g.rect(".", 3 + (1 if noise(3, y, 28) < 30 else 0), y, river_x(y) - 1, y)
    g.blob(",", 6, 7, 3, 2, salt=21)
    g.blob(",", 6, 26, 3, 3, salt=22)
    g.blob(";", 6, 17, 3, 3, salt=29)
    g.rect("p", 0, 12, 10, 13)
    g.rect("p", 9, 12, 10, RIV_FORD[0] + 1)
    g.put("k", RIV_SIGN)
    # --- the river, its sand bar and the ford -------------------------------------------
    for y in range(H):
        x0 = river_x(y)
        g.rect("=", x0, y, x0 + 6, y)
    for y in range(4, 10):
        g.put("s", (river_x(y) - 1, y), (river_x(y) - 2, y))
    for y in range(RIV_FORD[0], RIV_FORD[1] + 1):   # stepping stones across the water only
        g.rect("p", 9, y, river_x(y) - 1, y)
        g.rect("f", river_x(y), y, river_x(y) + 6, y)
        g.rect("p", river_x(y) + 7, y, 23, y)
    # --- the far bank: long grass to the trees, the angler's hut, a reedy backwater ------
    for y in range(3, 31):
        g.rect(";", river_x(y) + 7, y, 29 - (1 if noise(29, y, 30) < 35 else 0), y)
    g.blob(",", 25, 13, 4, 4, salt=25)
    g.blob(".", 27, 20, 2, 2, salt=31)
    g.blob(",", 27, 5, 2, 2, salt=26)
    g.rect(".", 21, 6, 22, 10)
    g.put("k", *[(RIV_HUT[0] + i, RIV_HUT[1] + j) for i in range(3) for j in range(3)])
    g.rect(".", 23, 8, 25, 9)
    g.rect("p", 22, 9, 24, 22)
    g.rect("p", 22, 9, 24, 9)
    g.blob("~", 25, 27, 3, 2, salt=32)               # the backwater, in the reeds
    g.blob("r", 25, 27, 2, 1, salt=33)
    for x in range(21, 30):
        if noise(x, 30, 27) < 45 and g.at(x, 30) != "~":
            g.put("#", (x, 30))
    return g


def props_river(g):
    g.set(*RIV_SIGN, SIGN, True)
    g.spiece("stilt_hut", *RIV_HUT, solid=True)
    g.set(RIV_HUT[0] + 1, RIV_HUT[1] + 2, smid("stilt_hut", "door"), True)   # its door stays shut


def spec_river():
    s = Spec(RIVER)
    s.connections = [{"direction": "left", "map": MAP[OAK], "offset": 0}]
    s.sign(*RIV_SIGN, "Sign", text="THE ERYMANTHOS\\nThe river runs down off the mountain to the Alpheios. "
                                    "Mind the ford after rain.")
    s.person("Angler", "FISHER", 24, 10, "LEFT")
    s.script("Angler", '''    lock
    faceplayer
    msgbox(format("Rods work in the Preserve, same as anywhere. A bite here is still a hunt: you throw "
                  "Pan Balls at what you hook.\\p"
                  "Swans' cygnets in the shallows, the bronze birds' chicks in the reeds...\\p"
                  "And once, at night, a little thing with three heads that bit my line in three places."))
    release''')
    s.item("ITEM_MYSTIC_WATER", 28, 4, item_flag("RIVER_NE", "the far bank's north corner"))
    s.item("ITEM_NET_BALL", 5, 22, item_flag("RIVER_WEST", "the west bank, past the ford road"))
    s.hide("ITEM_PEARL", 11, 6, hidden_flag("RIVER_SANDBAR", "the river's sand bar"))
    s.hide("ITEM_HEART_SCALE", 4, 29, hidden_flag("RIVER_SW", "the west bank's south end"))
    return s


def build_river():
    g = plan_river()
    blocks = outdoor(RIVER, g, props_river, R5.CYPRESS_TOP, 3)
    s = spec_river()
    write_events(s, "MUS_ICHOR_ROAD", "MAP_TYPE_ROUTE", extra=dict(EXTRA_ROUTE, weather="WEATHER_SUNNY"))
    m = ST.Walk(RIVER, blocks, STYM, s, g)
    west = [(0, y) for y in (12, 13)]
    views = [("1 from the oakwood", 5, 12), ("2 the sand bar", 11, 7), ("3 the ford", 16, 23),
             ("4 the angler's hut", 24, 7), ("5 the far bank", 26, 14), ("6 the west bank's south end", 6, 27)]
    return m, [("the oakwood to the far bank", west, [(24, 15)])], views, "river", set()


# ---------------------------------------------------------------------------
# The Cold Cave (26x18, cave_dark, lit). Its mouth opens south onto the High Meadow.
# ---------------------------------------------------------------------------
CAVE_W, CAVE_H = 26, 18
CAVE_MOUTH = (5, 16)               # daylight_s; the warp is one row below


def plan_cave():
    W, H = CAVE_W, CAVE_H
    g = [["#"] * W for _ in range(H)]

    def rect(ch, x0, y0, x1, y1):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                g[y][x] = ch
    rect(".", 4, 11, 7, 16)                        # up from the mouth
    rect(".", 3, 6, 11, 11)                        # the first hall
    rect("#", 6, 8, 7, 9)
    rect(".", 11, 3, 20, 8)                        # the frost hall, under a crack of daylight
    rect(",", 14, 4, 16, 6)
    rect("#", 18, 3, 20, 4)
    rect(".", 20, 7, 23, 14)                       # down the east side to the seep
    rect("~", 14, 11, 19, 14)                      # the seep's pool
    rect(".", 12, 10, 13, 15)
    rect(".", 14, 15, 20, 15)
    rect(".", 8, 13, 11, 15)
    g[12][20] = "."
    return g


def build_cave():
    import cave_dark_kit as kit
    cat = json.loads((ROOT / "data/tilesets/secondary/cave_dark/catalog.json").read_text())
    pieces = {p["key"]: p["ids"] for p in cat["pieces"]}
    g = plan_cave()
    W, H = CAVE_W, CAVE_H
    tiles = kit.autotile(["".join(r) for r in g], cat, "wet")
    blocks = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            t = tiles[y][x] & 0x3FF
            blocks[y, x] = t | (0x400 if g[y][x] == "#" else 0x1000 if g[y][x] == "~" else 0x3000)

    def put(x, y, ids, solid=True):
        for j, row in enumerate(ids):
            for i, mid in enumerate(row):
                blocks[y + j, x + i] = mid | (0x400 if solid else 0x3000)
    put(*CAVE_MOUTH, pieces["daylight_s"], solid=False)
    put(22, 10, pieces["seep"])
    put(9, 7, pieces["stalagmites"])
    put(19, 6, pieces["column"])
    put(23, 13, pieces["stalagmite"])
    put(3, 6, pieces["stalagmite_tall"])
    put(10, 14, pieces["rock_pile"])
    put(13, 3, pieces["stele"])
    put(17, 7, pieces["pebbles"], solid=False)
    put(5, 12, pieces["pebbles"], solid=False)
    KP.write_layout(CAVE, blocks, [kit.kit_id(cat, "T|...", "wet") | 0x3400] * 4, "gTileset_Aethos",
                    "gTileset_CaveDark")
    s = Spec(CAVE)
    s.warps = [KP.warp(CAVE_MOUTH[0], CAVE_MOUTH[1] + 1, MEADOW, 0)]
    s.sign(13, 3, "Stele", text="Cut in the rock: a hunting dog, a deer and a crescent moon. "
                                "Under them, newer: THE COLD KEEPS. SO DO WE.")
    s.item("ITEM_ICE_STONE", 22, 7, item_flag("CAVE_EAST", "the cold cave's east side"))
    s.hide("ITEM_NEVER_MELT_ICE", 15, 5, hidden_flag("CAVE_FROST", "under the frost hall's crack"))
    s.hide("ITEM_ESCAPE_ROPE", 9, 14, hidden_flag("CAVE_PILE", "behind the rock pile"))
    write_events(s, "MUS_ICHOR_HOLLOW", "MAP_TYPE_UNDERGROUND",
                 extra={"ichor_kind": "safari", "requires_flash": False, "allow_cycling": False, "allow_escaping": False,
                        "allow_running": True, "show_map_name": False, "weather": "WEATHER_NONE"})
    m = ST.Walk(CAVE, blocks, "gTileset_CaveDark", s, ST.Grid(CAVE, W, H))
    return m, [("the mouth to the seep", [CAVE_MOUTH], [(21, 12)])], [
        ("1 the mouth", 5, 13), ("2 the first hall", 6, 8), ("3 the frost hall", 15, 5), ("4 the seep", 18, 12)], \
        "cave", set()


# ---------------------------------------------------------------------------
# The Boar's Thicket (26x22, post-game). The High Meadow is south (our x 6 at the bottom).
# ---------------------------------------------------------------------------
TH_W, TH_H = 26, 22
TH_CAIRN = (19, 5)
TH_SIGN = (7, 18)


def plan_thicket():
    W, H = TH_W, TH_H
    g = ST.Grid(THICKET, W, H)
    g.rect("#", 0, 0, W - 1, H - 1)
    g.rect("p", 6, 15, 6, H - 1)
    g.rect(".", 5, 15, 8, 17)
    g.blob(",", 8, 14, 3, 2, salt=31)
    g.rect(";", 7, 4, 21, 13)
    g.blob(";", 14, 8, 8, 5, salt=32)
    g.blob(",", 10, 6, 3, 2, salt=33)
    g.blob(",", 19, 11, 2, 2, salt=34)
    g.blob("q", 14, 8, 2, 1, salt=35)              # the boar's wallow, rooted to bare scree
    g.rect(".", 18, 4, 21, 6)
    g.put("k", TH_CAIRN, TH_SIGN)
    for x, y in ((12, 5), (17, 12), (9, 10)):       # oaks it has torn up and left
        g.put("#", (x, y))
    return g


def props_thicket(g):
    g.spiece("odds", *TH_CAIRN, [("stele", 0, 0)])
    g.set(*TH_SIGN, SIGN, True)
    g.spiece("odds", 15, 10, [("drag", 0, 0)], False) if g.at(15, 10) in (";", "q") else None


def spec_thicket():
    s = Spec(THICKET)
    s.connections = [{"direction": "down", "map": MAP[MEADOW], "offset": 0}]
    s.sign(*TH_CAIRN, "Cairn", text="A cairn of river stones, a hunter's mark. One stone is cut: "
                                     "ATALANTA WAS HERE. SO WAS THE BOAR. NOT FOR LONG.")
    s.item("ITEM_BIG_ROOT", 20, 12, item_flag("THICKET_ROOTS", "the thicket's torn-up roots"))
    s.hide("ITEM_RARE_CANDY", 14, 8, hidden_flag("THICKET_WALLOW", "in the boar's wallow"))
    s.item("ITEM_SITRUS_BERRY", 9, 15, item_flag("THICKET_GAP", "by the thicket's gap"))
    s.hide("ITEM_ETHER", 20, 5, hidden_flag("THICKET_CAIRN", "behind Atalanta's cairn"))
    s.sign(*TH_SIGN, "Sign", text="THE BOAR'S THICKET\\nThe oaks lie where it threw them.")
    return s


def build_thicket():
    g = plan_thicket()
    blocks = outdoor(THICKET, g, props_thicket, R5.CYPRESS_TOP, 4)
    s = spec_thicket()
    write_events(s, "MUS_ICHOR_ROAD_NIGHT", "MAP_TYPE_ROUTE", extra=dict(EXTRA_ROUTE, weather="WEATHER_SHADE"))
    m = ST.Walk(THICKET, blocks, STYM, s, g)
    south = [(6, TH_H - 1)]
    return m, [("the gap to the cairn", south, [(TH_CAIRN[0], TH_CAIRN[1] + 1)])], [
        ("1 the gap", 6, 17), ("2 the wallow", 14, 8), ("3 the cairn", 19, 6)], "thicket", set()


# ---------------------------------------------------------------------------
# The lodge (Arkadia's charcoal-hut room) and its hut on Arkadia's west road
# ---------------------------------------------------------------------------

def build_lodge():
    src = ROOT / "data/layouts/Arkadia_CharcoalHut"
    dst = ROOT / f"data/layouts/{LODGE}"
    for f in ("map.bin", "border.bin"):
        (dst / f).write_bytes((src / f).read_bytes())
    lay = np.fromfile(dst / "map.bin", "<u2").reshape(8, 11)
    FLOOR, STOOL = 0x260 | 0x3000, 0x263 | 0x0400
    lay[4, 0] = 0x25E | 0x3000           # the coal heaps swept out: bare wall foot and floor
    lay[3, 1] = FLOOR
    lay[5, 2] = STOOL                    # a stool for the keeper's visitors
    lay[6, 2:5] = [0x266 | 0x0400, 0x267 | 0x0400, 0x268 | 0x0400]   # a second stack of spear shafts
    lay.astype("<u2").tofile(dst / "map.bin")
    s = Spec(LODGE)
    ark_warp = arkadia_lodge()
    s.warps = [KP.warp(4, 7, "Arkadia", ark_warp), KP.warp(5, 7, "Arkadia", ark_warp)]
    s.person("Keeper", "PRIESTESS", 6, 3, "DOWN")
    s.sign(6, 1, "Drawing", "NORTH", text="An old drawing of the mountain burned onto a board: the oaks, "
                                           "the meadow, the river, and up in one corner, a boar.")
    s.sign(2, 2, "Sacks", "NORTH", text="Sacks of barley for the hunt, and a basket of throwing stones.")
    s.sign(4, 2, "Rake", "NORTH", text="Hunting spears, and a net with a tear in it the shape of a tusk.")
    s.scripts.append(f'''text {s.px}Name {{ "MELANIPPE" }}''')
    s.script("Keeper", f'''    lock
    faceplayer
    setspeaker({s.px}Name)
    msgbox(format("This is the Erymanthian Preserve, Artemis's own hunting ground. I keep it for her.\\p"
                  "For ¥{FEE} you may hunt it. You take {30} Pan Balls and no Pokémon of your own: "
                  "the goddess's animals are caught, not beaten.\\p"
                  "You have {500} steps before I ring you out."))
    showmoneybox(0, 0)
    msgbox(format("Will you hunt?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) != YES) {{
        hidemoneybox
        msgbox(format("Then go gently. She sees who comes and goes."))
        release
        end
    }}
    getpartysize
    if (var(VAR_RESULT) == PARTY_SIZE) {{
        specialvar(VAR_RESULT, ScriptCheckFreePokemonStorageSpace)
        if (var(VAR_RESULT) == FALSE) {{
            hidemoneybox
            msgbox(format("Your party's full and so is your Pithos. Where would you put a catch? "
                          "Make room first."))
            release
            end
        }}
    }}
    checkmoney({FEE})
    if (var(VAR_RESULT) == FALSE) {{
        hidemoneybox
        msgbox(format("That's not enough. The goddess doesn't haggle, and neither do I."))
        release
        end
    }}
    removemoney({FEE})
    updatemoneybox
    playse(SE_SHOP)
    msgbox(format("Here: {30} Pan Balls. Pan made the first nets for her, they say.\\p"
                  "Barley brings them close and slow. A stone makes them easier to take, and quicker to bolt.\\p"
                  "When you want to come back, ring the bell at the gate."))
    hidemoneybox
    special(EnterSafariMode)
    setvar(VAR_SAFARI_ZONE_STATE, 2)
    closemessage
    warp({MAP[OAK]}, {ARRIVAL[0]}, {ARRIVAL[1]})
    waitstate
    release''')
    s.script("Back", f'''    lockall
    applymovement(LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp)
    waitmovement(0)
    setspeaker({s.px}Name)
    msgbox(format("Back in one piece. Whatever you caught, treat it well. It was hers first."))
    setvar(VAR_SAFARI_ZONE_STATE, 0)
    releaseall''')
    header = f'''mapscripts {LODGE}_MapScripts {{
    MAP_SCRIPT_ON_FRAME_TABLE [
        VAR_SAFARI_ZONE_STATE, 1: {s.px}Back
    ]
}}'''
    write_events(s, "MUS_ICHOR_AKTI", "MAP_TYPE_INDOOR", header=header,
                 extra={"show_map_name": False, "weather": "WEATHER_NONE"})


def arkadia_lodge():
    """Copy Arkadia's charcoal hut front (its 4x3 at x 9-12, rows 19-21) onto the west
    road's end, with a warp to the lodge on its door; returns that warp's index."""
    lay = ROOT / "data/layouts/Arkadia/map.bin"
    b = np.fromfile(lay, "<u2").reshape(44, 50)
    hx, hy = LODGE_HUT
    front = b[19:22, 9:13].copy()
    b[hy:hy + 3, hx:hx + 4] = front
    b.astype("<u2").tofile(lay)
    door = (hx + 2, hy + 2)
    p = ROOT / "data/maps/Arkadia/map.json"
    m = json.loads(p.read_text())
    warps = m["warp_events"]
    for i, w in enumerate(warps):
        if w["dest_map"] == MAP[LODGE]:
            break
    else:
        warps.append({"x": door[0], "y": door[1], "elevation": 0, "dest_map": MAP[LODGE], "dest_warp_id": "0"})
        i = len(warps) - 1
    # the Alpheios sign beside the hut now names the Preserve too
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    return i


BUILDERS = [build_oak, build_meadow, build_river, build_cave, build_thicket]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--walk", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    bad = 0
    build_lodge()
    for b in BUILDERS:
        m, segs, views, stem, floats = b()
        if args.only and stem not in args.only.split(","):
            continue
        problems, mand, forced = ST.check(m, segs, 0, floats=floats)
        if args.walk:
            print(KP.walk_text(m))
        if args.render:
            KP.render(m, args.render, stem, views)
        for p in problems:
            print(f"PROBLEM {m.name}: {p}")
        print(f"{m.name}: {m.w}x{m.h}, grass on the way {forced}, {len(problems)} problems")
        bad += len(problems)
    claim_flags()
    import wild_plan
    data = json.loads(wild_plan.PATH.read_text())
    wild_plan.apply(wild_plan.ichor_entries(data))      # the Preserve's tables are the plan's
    wild_plan.PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
