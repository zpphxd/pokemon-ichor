#!/usr/bin/env python3
"""Build Aigina's interior: the Aphaia Road, the Temple of Aphaia and Mount Oros.

Three Act II maps on gTileset_Aethos + gTileset_Aegina (design/phase2/BUILD.md,
batch 1; SCRIPT.md, "Aegina's interior: an optional detour"). World-act2 scripts
their people and story; this builds the places, their seams, items and event
spots, ready to script.

The island, north of Aigina Town's gate:

    MAP_AEGINA_MOUNT_OROS (16x16)    MAP_AEGINA_TEMPLE_OF_APHAIA (24x20)
    the peak and Zeus's altar   bay  Aphaia's Doric temple on its pine hill
    ---------------------------------------------------------------------
    MAP_AEGINA_APHAIA_ROAD (40x24): pistachios, ant hills, a band of golden
    grass through the scrub, the great herm at the fork
    ---------------------------------------------------------------------
                 MAP_AEGINA_TOWN (30x24), its gate at columns 24-25

All four share the aegina secondary, so no seam needs an aethos-only strip
(MAP_DESIGN.md section 5). The three maps are drawn below as ASCII plans in one
world frame (the road's top-left is (0,0)), auto-tiled as one piece so every
seam matches, then cut apart. Every edge without a connection is coast: the
border is the sea all round, as it is for the town.

Plan legend (one character per metatile):
  ~  sea            r  rocks awash         s  sand (surf or soft edges, chosen)
  .  grass          *  red anemones        ,  tall grass (aethos, green)
  d  dry grass (soft edges onto the green)  ;  golden tall grass (on dry ground)
  o  scrub cushion (solid, on dry)          A  ant hill (solid)   t  ant trail
  p  limestone path (soft edges)            ^  marble steps
  _  terrace lip: a ledge, jump south       b  boulder            S  stele (sign)
  H  the great herm   k  a worn foundation block (walkable, on dry)
  %  woods: Aleppo pines, umbrella pines and cypresses, packed by the builder
  Q  pistachio (2x2)  Y  Aleppo pine (2x3)  U  umbrella pine (2x2)  C  cypress (1x2)
  K  a fallen column drum (2x1)             #  a set piece placed in code

It writes data/layouts/<Map>/map.bin and border.bin, the three layouts' entries
in data/layouts/layouts.json, and each map.json's events and connections (and
the town's connection north), then checks the rules MAP_DESIGN.md sets for a
route: seams that match, no trap, a forced band on the way to each end, the
mandatory trainers' lines across the only path, and every person, item and
readable thing reachable.

The aegina catalog must exist:  /usr/bin/python3 tools/ichor/art/aegina_build.py --no-compile

Usage: /usr/bin/python3 tools/ichor/maps/aegina_detour.py [--render DIR]
  --render DIR writes, into DIR: aigina_aphaia_road.png, aigina_temple_of_aphaia.png
  and aigina_mount_oros.png (2x) with _walk.png collision overlays,
  aigina_island.png (the four maps stitched) and aigina_interior_screens.png
  (every 15x10 view along the walk); each view also goes to build/aigina_interior/.
  The renders in design/phase2/img/ come from --render design/phase2/img.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aegina as town  # noqa: E402  the town's helpers, plan and gate

ROOT = town.ROOT
LAYOUTS = ROOT / "data/layouts/layouts.json"
SEA, GRASS, FLOWERS, TALL = town.SEA, town.GRASS, town.FLOWERS, town.TALL
LEDGE_SHADOW = 0x002                        # grass under a ledge's lip
STELE, HERM, BOULDER = town.STELE, town.HERM, town.BOULDER
LEDGE = {"run": 0x087, "w_end": 0x0D5, "e_end": 0x0D6}
STEPS = 0x0AF                               # aethos's marble steps
TRIPOD = (0x130, 0x131)                     # bronze tripod (top layer) on its marble plinth
CYPRESS = (town.CYPRESS_TOP, town.CYPRESS_BOT)

# ---------------------------------------------------------------------------
# The world frame
# ---------------------------------------------------------------------------

# The road's column over the town's gate column 24: the town's connection north
# has offset 24 - GATE (BUILD.md), and the road's south one GATE - 24.
GATE = 20
TOWN_X, TOWN_Y = GATE - town.GATE_COLS[0], 24          # the town's (0,0) in world cells
XMIN, XMAX, YMIN, YMAX = TOWN_X, 40, -20, TOWN_Y + 6    # the frame auto-tiling sees


class Map:
    def __init__(self, key, map_id, folder, layout, x, y, w, h, png):
        self.key, self.id, self.folder, self.layout = key, map_id, folder, layout
        self.x, self.y, self.w, self.h, self.png = x, y, w, h, png

    def contains(self, wx, wy):
        return self.x <= wx < self.x + self.w and self.y <= wy < self.y + self.h


ROAD = Map("road", "MAP_AEGINA_APHAIA_ROAD", "AeginaAphaiaRoad", "LAYOUT_AEGINA_APHAIA_ROAD",
           0, 0, 40, 24, "aigina_aphaia_road")
OROS = Map("oros", "MAP_AEGINA_MOUNT_OROS", "AeginaMountOros", "LAYOUT_AEGINA_MOUNT_OROS",
           0, -16, 16, 16, "aigina_mount_oros")
TEMPLE = Map("temple", "MAP_AEGINA_TEMPLE_OF_APHAIA", "AeginaTempleOfAphaia", "LAYOUT_AEGINA_TEMPLE_OF_APHAIA",
             16, -20, 24, 20, "aigina_temple_of_aphaia")
MAPS = (ROAD, OROS, TEMPLE)
TOWN_ID = "MAP_AEGINA_TOWN"

# Each seam: (map, direction, neighbour, offset), both ways (map.json connections).
CONNECTIONS = {
    ROAD: [("down", TOWN_ID, TOWN_X), ("up", OROS.id, OROS.x - ROAD.x), ("up", TEMPLE.id, TEMPLE.x - ROAD.x)],
    OROS: [("down", ROAD.id, ROAD.x - OROS.x)],
    TEMPLE: [("down", ROAD.id, ROAD.x - TEMPLE.x)],
}
TOWN_CONNECTION = ("up", ROAD.id, ROAD.x - TOWN_X)          # in the town's map.json

# ---------------------------------------------------------------------------
# The plans
# ---------------------------------------------------------------------------
#
# The Aphaia Road climbs from the town's gate in a switchback: north through the
# pistachios, west along the lower terrace, north past Myrmex at the ant hills'
# corner, east along the upper terrace, then north through the band of golden
# grass past Sostratos to the great herm on the bay. There it forks: west and
# north through the pines to Mount Oros, east and up the marble steps (Euthymia
# keeps them) to the temple. Terraces east of the road drop back down to the
# orchard: the quick way home.
#
# The route standard (MAP_DESIGN.md section 8; Act II's middle band) wants 8 or
# more forced grass cells between every pair of ends, so each leg of the walk
# has its own band: two on the trunk (the golden grass Myrmex watches at the
# ant hills' corner, 4 deep, and the band under Sostratos, 4 deep), one on
# each branch past the fork (the pine glade on the Oros path and the golden
# grass between the herm and the temple steps, 4 each). Town to either end is
# then 12 and Oros to the temple 8, both ways: tall grass above the terrace wall
# west of the steps (24-26, 1) charges the hop down into the temple-side band
# the cell it skips. The rest of the grass is optional: the west meadow under
# the Oros ledge, the pistachio and meadow terraces on the way home, golden
# grass on the east plateau, and tall grass under the orchard's pistachios by
# the gate.

ROAD_PLAN = [
    # 0         1         2         3
    # 0123456789012345678901234567890123456789
    "~s%%%%%%;;%s~~~~~~~~s%%%...pp...%%%%%s~~",  # 0   seams: Oros (0-15), the temple (16-39)
    "~s%%%%%;;;%%s~~r~~~s%%%%,,,pp.S.%%%%%s~~",  # 1   the pine glade on the Oros path
    "~ss%%%%;;;d%%s~~~~s%%%%%___^^___%%%%%s~~",  # 2   Marilades; the temple steps
    "~~s%%%%%;;SddsssssssS.H;;;dppddo;;dUUs~~",  # 3   the bay's beach; the herm; Euthymia
    "~~s%%%%%ppppppppppppppp;;;;ppdd;;;SUUs~~",  # 4   the fork; the horos on the hill
    "~~s%%%%%pppppdod;;;ddp;;;odppd;;;ddd.s~~",  # 5
    "~~s%%%dod;;dd%%%%ooodpp%%%%ddddoo;d..s~~",  # 6   Sostratos; Nikasia over the way home
    "~s%%%________%%%%%o;;;,,o%%_______%%%%s~",  # 7   the band
    "rs%%%.,,*.,,.%%%%%o;;;;,,%%QQ....QQ,,.s~",  # 8
    "~s%%%d;;ddd,.%%%%%o;;;;;,%%QQ....QQ,,,s~",  # 9
    "~s%%%%%%%%%ppppppppo;;;;o%%...QQ.,,,.s~~",  # 10  the upper terrace
    "~~s%%%%%%%%pppppppppppp%%%%...QQ..,,,s~~",  # 11
    "~~s%%%%%%%%;;__________%%%%_______%%%s~r",  # 12
    "r~s%%%%%%%%;;AtAd;;Ad;d%,..,,dddAUU..s~~",  # 13  the ant hills; Myrmex
    "~~s%%%%%%%%;;ddtd;;tA;;%,,,.dAtddUU..s~~",  # 14
    "~~~s%%%%%%%;;odAdd;dd;o%.,,,,dddd...s~r~",  # 15
    "~~~s%%%%%%%ppppppppppp%%.....,,,...s~~~~",  # 16  the lower terrace
    "~~~~s%%%%%%ppppppppppp%%%%______%%s~~~~~",  # 17
    "~~~~~~~s...QQ.,QQ..dpp.QQ..*..%%s~~~~~~~",  # 18
    "~~~~~~~~~s.QQ,,QQ..dpp.QQ,,,..s~~~~~~~~~",  # 19  Opora
    "~~~~~~~~~~~s.QQ....Sppd.,,,..s~~~~~~~~~~",  # 20  the south sign
    "~~~~~~~~~~~~sQQ..YYoppoYY..s~~~~~~~~~~~~",  # 21
    "~~~~~~~~~~~~~~sssYYoppoYYss~~~~~~~~~~~~~",  # 22
    "~~~~~~~~~~~~~~~~~YYoppoYY~~~~~~~~~~~~~~~",  # 23  the seam with the town's gate
]

# Mount Oros: the island's peak. The path switchbacks up from the road through
# pines, then dry grass and scrub, to Zeus's altar on the summit; the sea is on
# every side but the south.
OROS_PLAN = [
    # 0123456789012345
    "~~~~~~~~~~~~~~~~",  # 0
    "~~~~~rssr~~~~~~~",  # 1
    "~~~~ssddss~~~~~~",  # 2
    "~~~sod##dds~~~~~",  # 3   Zeus's altar
    "~~sodd##dods~~~~",  # 4
    "~~sod;dppd;os~~~",  # 5   the summit
    "~~sod;;ppd;os~~~",  # 6
    "~~s%pppppdos~~~~",  # 7
    "~s%%ppppp,%%s~~~",  # 8
    "~~s%;;____%%%s~~",  # 9   a band of golden grass on the climb
    "~~s%;;dddd,%%sr~",  # 10
    "~s%%pppppp.%s~~~",  # 11
    "~ss%pppppp%s~r~~",  # 12
    "~~s%%%%%pp%s~~~~",  # 13
    "~~s%%%%%pp%s~~~~",  # 14
    "~s%%%%%%pp%s~~~~",  # 15  the seam with the road
]

# The Temple of Aphaia on its hilltop: the Doric front facing south down the
# path from the road, pines crowding the hill behind, Artemis's altar before it,
# and the old temple's foundations to the west where the earth is turned.
TEMPLE_PLAN = [
    # 0         1         2
    # 012345678901234567890123
    "~~~~~~~~~~~~~~~~~~~~~~~~",  # 0
    "~~~~~~~~~r~ssss~~~~r~~~~",  # 1
    "~~~~~~~sss%%%%%sss~~~~~~",  # 2
    "~~~~~ss%%%%%%%%%%%ss~~~~",  # 3
    "~~~~s%%%%%%%%%%%%%%%%s~~",  # 4
    "~~~~s%%%%######%%%%%%s~~",  # 5   the temple
    "~~~~s%%%%######%%%%%%%s~",  # 6
    "~~~s%%%%%######%%%%%%%s~",  # 7
    "~~r~s%%%%######%%%%%%s~~",  # 8
    "~~~s%%%dd######ddkkkk%s~",  # 9   its steps; the old temple's foundations
    "~~~s%%%ddddppdd#dkddk%s~",  # 10  Artemis's altar
    "~~~s%%oddddppdd#dkddks~~",  # 11
    "~~~~sooddddppddddkKKk%sr",  # 12
    "~~~s%%_____^^____kkkk%s~",  # 13  the terrace and its steps
    "~r~s%%%...CppC...%%%%%s~",  # 14
    "~~~~s%,,,.CppC.,,%%%%%s~",  # 15
    "~~~s%%,*..CppC..,%%%%s~~",  # 16
    "~~~s%%%...CppC..%%%%%s~~",  # 17
    "~~~~s%%%...pp...%%%%%s~~",  # 18
    "~~~~s%%%...pp...%%%%%s~~",  # 19  the seam with the road
]

PLANS = {ROAD: ROAD_PLAN, OROS: OROS_PLAN, TEMPLE: TEMPLE_PLAN}

# Set pieces, in each map's own cells: (catalog key or special, x, y)
TEMPLE_FRONT = (9, 5)                     # temple_aphaia's top-left; its steps are row 9
ALTAR_ZEUS = (6, 3)                       # altar_zeus's top-left on Mount Oros
ALTAR_ARTEMIS = (15, 10)                  # the tripod's top cell; its plinth below
SET_PIECES = {
    TEMPLE: [("temple_aphaia", *TEMPLE_FRONT), ("tripod", *ALTAR_ARTEMIS)],
    OROS: [("altar_zeus", *ALTAR_ZEUS)],
    ROAD: [],
}

# ---------------------------------------------------------------------------
# People, items and readable things (each map's own cells)
# ---------------------------------------------------------------------------
#
# The trainers and the priestess are world-act2's: they stand here with a
# placeholder line (ICHOR_ACT2) and no battle. Their trainer_type stays NONE
# until world-act2 registers the parties and writes trainerbattle scripts (the
# sight check reads the trainer id from the script, so a placeholder can't be a
# sighted trainer). TRAINERS gives the facing and sight each is placed for, and
# whether its line must cut the only path; the checks prove it does.
#
# Eight of them (world-act2's batch 4 registers all eight at Astyra levels): the
# first three are Phase 2's; Opora, Marilades and Nikasia on the road, Myrto at
# the temple and Aigon on Oros were added for the route standard. Each one's
# scripts.pory comment suggests a class, a name and a party.

FACING = {"MOVEMENT_TYPE_FACE_UP": (0, -1), "MOVEMENT_TYPE_FACE_DOWN": (0, 1),
          "MOVEMENT_TYPE_FACE_LEFT": (-1, 0), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0)}

# name: (map, x, y, facing, sight, mandatory on the walk to, gfx)
TRAINERS = {
    # the orchard by the gate: the road's first, in plain view across the way up
    "Opora": (ROAD, 18, 19, "MOVEMENT_TYPE_FACE_RIGHT", 3, (), "OBJ_EVENT_GFX_ICHOR_HARVESTER"),
    "Myrmex": (ROAD, 13, 14, "MOVEMENT_TYPE_FACE_LEFT", 3, ("oros", "temple"), "OBJ_EVENT_GFX_ICHOR_HOPLITE"),
    "Sostratos": (ROAD, 20, 6, "MOVEMENT_TYPE_FACE_RIGHT", 3, ("oros", "temple"), "OBJ_EVENT_GFX_ICHOR_MERCHANT"),
    "Euthymia": (ROAD, 26, 3, "MOVEMENT_TYPE_FACE_RIGHT", 3, ("temple",), "OBJ_EVENT_GFX_ICHOR_PILGRIM"),
    # the pine glade on the Oros path, stepping out of the trees across it
    "Marilades": (ROAD, 10, 2, "MOVEMENT_TYPE_FACE_LEFT", 3, ("oros",), "OBJ_EVENT_GFX_ICHOR_MAN"),
    # the top of the east terraces, watching the hop down: the quick way home
    "Nikasia": (ROAD, 28, 6, "MOVEMENT_TYPE_FACE_RIGHT", 2, (), "OBJ_EVENT_GFX_ICHOR_YOUTH_F"),
    # the top of the temple's marble steps
    "Myrto": (TEMPLE, 10, 12, "MOVEMENT_TYPE_FACE_RIGHT", 3, ("temple",), "OBJ_EVENT_GFX_ICHOR_ACOLYTE_F"),
    # Oros's golden band, the only way up to the summit
    "Aigon": (OROS, 6, 10, "MOVEMENT_TYPE_FACE_LEFT", 2, ("oros",), "OBJ_EVENT_GFX_ICHOR_GOATHERD"),
}
PRIESTESS = (TEMPLE, 11, 9, "MOVEMENT_TYPE_FACE_DOWN")
LOCALID_PREFIX = {ROAD: "APHAIA", TEMPLE: "APHAIA", OROS: "OROS"}

# (map, x, y, item, amount, flag, note)
ITEMS = [
    (ROAD, 22, 13, "ITEM_SILVER_POWDER", 1, "FLAG_ICHOR_ITEM_APHAIA_SILVER_POWDER", "on the ant hills"),
    (ROAD, 12, 3, "ITEM_SUPER_POTION", 1, "FLAG_ICHOR_ITEM_APHAIA_SUPER_POTION", "at the Oros fork"),
    (ROAD, 5, 9, "ITEM_HYPER_POTION", 1, "FLAG_ICHOR_ITEM_APHAIA_HYPER_POTION", "the west meadow's end"),
    (ROAD, 37, 8, "ITEM_LEAF_STONE", 1, "FLAG_ICHOR_ITEM_APHAIA_LEAF_STONE", "the pistachio terrace's far corner"),
    (TEMPLE, 14, 9, "ITEM_PRETTY_FEATHER", 2, "FLAG_ICHOR_ITEM_APHAIA_PRETTY_FEATHER", "on the temple steps"),
    (TEMPLE, 16, 14, "ITEM_GREAT_BALL", 1, "FLAG_ICHOR_ITEM_APHAIA_GREAT_BALL", "the cypress nook east of the way"),
    # ICHOR_STUB_OFFERINGS: Wine is an engine item still to come; Berry Juice stands in
    (OROS, 8, 4, "ITEM_BERRY_JUICE", 1, "FLAG_ICHOR_ITEM_OROS_WINE", "by Zeus's altar"),
]

# Hidden items (map, x, y, item, flag, note). Their flags are vanilla ones, at or
# above FLAG_HIDDEN_ITEMS_START, which bg_hidden_item_event needs.
HIDDEN = [
    (ROAD, 13, 3, "ITEM_BIG_PEARL", "FLAG_ICHOR_HIDDEN_APHAIA_BIG_PEARL", "the west end of the bay's beach"),
    (ROAD, 15, 21, "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_APHAIA_REVIVE", "under the pines at the orchard's foot"),
    (ROAD, 36, 13, "ITEM_NUGGET", "FLAG_ICHOR_HIDDEN_APHAIA_NUGGET", "behind the umbrella pine, meadow terrace"),
    (ROAD, 36, 6, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_HIDDEN_APHAIA_PRETTY_FEATHER", "past the horos, at the cliff"),
    (TEMPLE, 7, 14, "ITEM_MOON_STONE", "FLAG_ICHOR_HIDDEN_APHAIA_MOON_STONE", "the cypress nook west of the way"),
    (TEMPLE, 20, 13, "ITEM_ETHER", "FLAG_ICHOR_HIDDEN_APHAIA_ETHER", "the old foundations' far corner"),
    (OROS, 7, 2, "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_OROS_STAR_PIECE", "behind Zeus's altar"),
    (OROS, 10, 4, "ITEM_THUNDER_STONE", "FLAG_ICHOR_HIDDEN_OROS_THUNDER_STONE", "the summit's east lip"),
]

# Temple and Oros are one-floor landmarks off the road, not routes: the route
# standard judges them as dungeons (MAP_DESIGN.md section 8.4).
ICHOR_KIND = {TEMPLE: "dungeon", OROS: "dungeon"}

# (map, x, y, script suffix, read from) -- read from: the tile the player stands
# on to read it, which the checks make sure is reachable
BG = [
    (ROAD, 22, 3, "GreatHerm", (22, 4)),
    (ROAD, 20, 3, "ForkSign", (20, 4)),
    (ROAD, 19, 20, "SouthSign", (20, 20)),
    (ROAD, 30, 1, "TempleSign", (29, 1)),
    (ROAD, 10, 3, "OrosSign", (10, 4)),
    (ROAD, 34, 4, "Horos", (34, 5)),
    (OROS, ALTAR_ZEUS[0], ALTAR_ZEUS[1] + 1, "AltarOfZeus", (ALTAR_ZEUS[0], ALTAR_ZEUS[1] + 2)),
    (TEMPLE, ALTAR_ARTEMIS[0], ALTAR_ARTEMIS[1] + 1, "AltarOfArtemis", (ALTAR_ARTEMIS[0], ALTAR_ARTEMIS[1] + 2)),
    (TEMPLE, 18, 11, "DigSpot", (19, 11)),
]

# Where the walks go: into the road from the town's gate, and the two ends.
ROAD_START = [(GATE, 23), (GATE + 1, 23)]
GOALS = {"oros": (OROS, ALTAR_ZEUS[0], ALTAR_ZEUS[1] + 2),
         "temple": (TEMPLE, PRIESTESS[1], PRIESTESS[2] + 1)}

# ---------------------------------------------------------------------------
# The world grid
# ---------------------------------------------------------------------------

GREEN_SET = set(".*,_%bHSQYUC#^")
DRY_SET = set("d;oAtk K".replace(" ", ""))
SEA_SET = set("~r")


def family(c):
    if c in SEA_SET:
        return "sea"
    if c == "s":
        return "sand"
    if c == "p":
        return "path"
    if c in DRY_SET:
        return "dry"
    return "green"


class World:
    def __init__(self):
        self.w, self.h = XMAX - XMIN, YMAX - YMIN
        self.ch = [["~"] * self.w for _ in range(self.h)]
        self.mid = np.full((self.h, self.w), SEA, np.uint16)
        self.solid = np.zeros((self.h, self.w), bool)
        self.done = np.zeros((self.h, self.w), bool)       # cells a piece already drew
        self.cat = {s["key"]: s for s in json.loads(town.CAT.read_text())}
        # the town's top rows, so the road's bottom rows tile against them
        tr = {"g": ".", "q": ".", "B": "."}
        for ty, row in enumerate(town.PLAN[:YMAX - TOWN_Y]):
            for tx, c in enumerate(row):
                self.setch(TOWN_X + tx, TOWN_Y + ty, tr.get(c, c))
        for m in MAPS:
            plan = PLANS[m]
            assert len(plan) == m.h, f"{m.key}: plan has {len(plan)} rows, want {m.h}"
            for y, row in enumerate(plan):
                assert len(row) == m.w, f"{m.key}: plan row {y} is {len(row)} wide, want {m.w}"
                for x, c in enumerate(row):
                    self.setch(m.x + x, m.y + y, c)

    # world-cell access ----------------------------------------------------------
    def inside(self, x, y):
        return XMIN <= x < XMAX and YMIN <= y < YMAX

    def setch(self, x, y, c):
        if self.inside(x, y):
            self.ch[y - YMIN][x - XMIN] = c

    def c(self, x, y):
        return self.ch[y - YMIN][x - XMIN] if self.inside(x, y) else "~"

    def set(self, x, y, mid, solid=False):
        if self.inside(x, y):
            self.mid[y - YMIN, x - XMIN] = mid
            self.solid[y - YMIN, x - XMIN] = solid
            self.done[y - YMIN, x - XMIN] = True

    def get(self, x, y):
        return int(self.mid[y - YMIN, x - XMIN]), bool(self.solid[y - YMIN, x - XMIN])

    def k(self, key, cx=0, cy=0):
        return self.cat[key]["ids"][cy][cx]

    def put(self, key, x, y, solid_all=True):
        """An aegina structure; '-' cells keep their ground. Walk-behind ('T') cells
        are solid too unless solid_all is False."""
        s = self.cat[key]
        for j in range(s["h"]):
            for i in range(s["w"]):
                wk = s["walk"][j][i]
                if wk == "-":
                    continue
                self.set(x + i, y + j, s["ids"][j][i], wk == "X" or (wk == "T" and solid_all))

    # the plan's neighbourhood ------------------------------------------------------
    def nb(self, x, y, pred):
        """(n, s, w, e, nw, ne, sw, se): which neighbours satisfy pred(char)."""
        return tuple(pred(self.c(x + dx, y + dy)) for dx, dy in
                     ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)))


def ground(wd):
    """Every cell's ground, with soft edges where sand, dry grass and the path meet
    the meadow, and the surf where sand meets the sea."""
    dg = lambda cx, cy: wd.k("dry_grass", cx, cy)
    dry = {"tl": dg(0, 0), "t": dg(1, 0), "tr": dg(2, 0), "l": dg(0, 1), "c": dg(1, 1),
           "r": dg(2, 1), "bl": dg(0, 2), "b": dg(1, 2), "br": dg(2, 2),
           "in_nw": dg(3, 0), "in_ne": dg(4, 0), "in_sw": dg(3, 1), "in_se": dg(4, 1)}
    for y in range(YMIN, YMAX):
        for x in range(XMIN, XMAX):
            c = wd.c(x, y)
            f = family(c)
            if f == "sea":
                wd.mid[y - YMIN, x - XMIN] = SEA
            elif f == "sand":
                key = town.edge_key(*wd.nb(x, y, lambda q: family(q) == "sea"))
                if key == "c":
                    n, s_, w_, e, *_ = wd.nb(x, y, lambda q: family(q) not in ("sand", "sea"))
                    soft = town.edge_key(n, s_, w_, e)
                    mid = town.SAND_GRASS[soft] if soft != "c" else town.SAND["c"]
                else:
                    mid = town.SAND[key]
                wd.mid[y - YMIN, x - XMIN] = mid
            elif f == "dry":
                key = town.edge_key(*wd.nb(x, y, lambda q: family(q) != "dry"))
                if key == "c" and town.hashed(x, y, 3) < 0.15:
                    mid = dg(3 + (x % 2), 2)                 # a pebble
                else:
                    mid = dry[key]
                wd.mid[y - YMIN, x - XMIN] = mid
            elif f == "path":
                n, s_, w_, e, *_ = wd.nb(x, y, lambda q: q not in "p^")
                key = "c" if (n and s_) or (w_ and e) else town.edge_key(n, s_, w_, e)
                wd.mid[y - YMIN, x - XMIN] = town.PATH.get(key, town.PATH["c"])
            else:
                wd.mid[y - YMIN, x - XMIN] = GRASS


def features(wd):
    """The plan's one-cell features: grass, flowers, ledges, scrub, ants, signs."""
    for y in range(YMIN, YMAX):
        for x in range(XMIN, XMAX):
            c = wd.c(x, y)
            if c == ".":
                wd.set(x, y, LEDGE_SHADOW if wd.c(x, y - 1) == "_" else GRASS)
            elif c == "*":
                wd.set(x, y, FLOWERS)
            elif c == ",":
                wd.set(x, y, TALL)
            elif c == ";":
                wd.set(x, y, wd.k("dry_tall_grass"))
            elif c == "A":
                wd.set(x, y, wd.k("anthills", 0, 0), True)
            elif c == "t":
                wd.set(x, y, wd.k("anthills", 1, 0))
            elif c == "k":
                wd.set(x, y, wd.k("kolona", 0 if town.hashed(x, y, 5) < 0.5 else 2, 4))
            elif c == "^":
                wd.set(x, y, STEPS)
            elif c == "H":
                wd.set(x, y, HERM, True)
            elif c == "S":
                wd.set(x, y, STELE, True)
            elif c == "b":
                wd.set(x, y, BOULDER, True)
            elif c == "r":
                wd.set(x, y, wd.k("sea_rocks"), True)
            elif c == "_":
                left, right = wd.c(x - 1, y), wd.c(x + 1, y)
                open_ = lambda q: q in ".*,dp;tk"
                piece = "w_end" if open_(left) else "e_end" if open_(right) else "run"
                wd.set(x, y, LEDGE[piece], True)
            elif c == "o":
                # scrub comes in pairs: left cushion, right cushion along a run
                run = 0
                while wd.c(x - run - 1, y) == "o":
                    run += 1
                wd.set(x, y, wd.k("scrub", run % 2, 0), True)


def blocks(wd):
    """Trees and drums drawn as blocks in the plan ('QQ/QQ' a pistachio), and the
    woods ('%') packed with a staggered mix of pines and cypresses."""
    sizes = {"Q": ("pistachio", 2, 2), "Y": ("pine", 2, 3), "U": ("upine", 2, 2), "C": ("cypress", 1, 2),
             "K": ("kolona_ruins", 2, 1)}
    taken = set()
    for y in range(YMIN, YMAX):
        for x in range(XMIN, XMAX):
            c = wd.c(x, y)
            if c not in sizes or (x, y) in taken:
                continue
            kind, bw, bh = sizes[c]
            cells = [(x + i, y + j) for j in range(bh) for i in range(bw)]
            bad = [p for p in cells if wd.c(*p) != c or p in taken]
            assert not bad, f"a {kind} at world ({x},{y}) doesn't fit its plan block: {bad}"
            taken.update(cells)
            tree(wd, kind, x, y)
    woods(wd)


def tree(wd, kind, x, y):
    if kind == "upine":
        wd.set(x, y, town.UPINE[0][0], True)
        wd.set(x + 1, y, town.UPINE[0][1], True)
        wd.set(x, y + 1, town.UPINE[1][0], True)
        wd.set(x + 1, y + 1, town.UPINE[1][1], True)
    elif kind == "cypress":
        wd.set(x, y, CYPRESS[0], True)
        wd.set(x, y + 1, CYPRESS[1], True)
    else:
        wd.put(kind, x, y)


def woods(wd):
    """Pack '%' cells with trees. Pines go down first in a stable pseudo-random
    order, so the crowns stagger instead of lining up in rows; Aleppo pines (2x3)
    and umbrella pines (2x2) take most of it, cypresses fill the 1x2 slots left,
    and a last lone cell gets a young cypress (the spire's crown alone, which reads
    as a juniper) or, now and then, a boulder."""
    def free(x, y, w, h):
        return all(wd.c(x + i, y + j) == "%" and not wd.done[y + j - YMIN, x + i - XMIN]
                   for j in range(h) for i in range(w))
    cells = [(x, y) for y in range(YMIN, YMAX) for x in range(XMIN, XMAX) if wd.c(x, y) == "%"]
    for x, y in sorted(cells, key=lambda p: town.hashed(p[0], p[1], 17)):
        r = town.hashed(x, y, 11)
        if r < 0.5 and free(x, y, 2, 3):
            tree(wd, "pine", x, y)
        elif free(x, y, 2, 2):
            tree(wd, "upine", x, y)
    for x, y in cells:                                  # then the gaps, top-down
        if free(x, y, 2, 2):
            tree(wd, "upine", x, y)
        elif free(x, y, 1, 2):
            tree(wd, "cypress", x, y)
    for x, y in cells:
        if free(x, y, 1, 1):
            wd.set(x, y, BOULDER if town.hashed(x, y, 23) < 0.12 else CYPRESS[0], True)


def set_pieces(wd):
    for m, pieces in SET_PIECES.items():
        for key, x, y in pieces:
            wx, wy = m.x + x, m.y + y
            if key == "tripod":
                wd.set(wx, wy, TRIPOD[0], True)
                wd.set(wx, wy + 1, TRIPOD[1], True)
                continue
            s = wd.cat[key]
            for j in range(s["h"]):
                for i in range(s["w"]):
                    assert wd.c(wx + i, wy + j) == "#", f"{m.key}: {key} at ({x},{y}) is off its '#' footprint"
            wd.put(key, wx, wy)


def compose():
    wd = World()
    ground(wd)
    features(wd)
    set_pieces(wd)
    blocks(wd)
    return wd


# ---------------------------------------------------------------------------
# Layouts
# ---------------------------------------------------------------------------

def cut(wd, m):
    """A map's cells from the world: (metatile ids, solid) arrays."""
    ys, xs = slice(m.y - YMIN, m.y - YMIN + m.h), slice(m.x - XMIN, m.x - XMIN + m.w)
    return wd.mid[ys, xs].copy(), wd.solid[ys, xs].copy()


def encode(mid, solid):
    out = np.zeros(mid.shape, np.uint16)
    for y in range(mid.shape[0]):
        for x in range(mid.shape[1]):
            m = int(mid[y, x])
            elev = 1 if town.behavior(m) in town.SURF_BEHAVIORS else 3
            out[y, x] = m | (int(solid[y, x]) << 10) | (elev << 12)
    return out


def write_layouts(wd):
    data = json.loads(LAYOUTS.read_text())
    for m in MAPS:
        d = ROOT / "data/layouts" / m.folder
        d.mkdir(parents=True, exist_ok=True)
        encode(*cut(wd, m)).astype("<u2").tofile(d / "map.bin")
        np.full(4, SEA, np.uint16).astype("<u2").tofile(d / "border.bin")
        lay = next(l for l in data["layouts"] if l.get("id") == m.layout)
        lay.update({"width": m.w, "height": m.h, "primary_tileset": "gTileset_Aethos",
                    "secondary_tileset": "gTileset_Aegina"})
    LAYOUTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def blocks_of(m):
    return np.fromfile(ROOT / "data/layouts" / m.folder / "map.bin", "<u2").reshape(m.h, m.w)


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

def obj(gfx, x, y, movement, script, flag="0", local_id=None, sight="0", amount=0):
    o = {}
    if local_id:
        o["local_id"] = local_id
    o.update({"graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": movement,
              "movement_range_x": amount, "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE",
              "trainer_sight_or_berry_tree_id": sight, "script": script, "flag": flag})
    return o


def events_of(m):
    objects, bgs = [], []
    for name, (tm, x, y, facing, _sight, _must, gfx) in TRAINERS.items():
        if tm is m:
            objects.append(obj(gfx, x, y, facing, f"{m.folder}_EventScript_{name}",
                               local_id=f"LOCALID_{LOCALID_PREFIX[m]}_{name.upper()}"))
    if m is PRIESTESS[0]:
        _, x, y, facing = PRIESTESS
        objects.append(obj("OBJ_EVENT_GFX_ICHOR_PRIESTESS", x, y, facing, f"{m.folder}_EventScript_Priestess",
                           local_id="LOCALID_APHAIA_PRIESTESS"))
    for im, x, y, item, amount, flag, _note in ITEMS:
        if im is m:
            objects.append(obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, "MOVEMENT_TYPE_FACE_DOWN",
                               "Common_EventScript_FindItem", flag=flag, sight=item,
                               amount=amount if amount > 1 else 0))
    for bm, x, y, name, _front in BG:
        if bm is m:
            bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                        "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                        "script": f"{m.folder}_EventScript_{name}"})
    for hm, x, y, item, flag, _note in HIDDEN:
        if hm is m:
            bgs.append({"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag})
    conns =[{"map": nid, "offset": off, "direction": d} for d, nid, off in CONNECTIONS[m]]
    return {"connections": conns, "object_events": objects, "warp_events": [], "coord_events": [],
            "bg_events": bgs}


def write_events():
    for m in MAPS:
        path = ROOT / "data/maps" / m.folder / "map.json"
        data = json.loads(path.read_text())
        data.update({"music": "MUS_ICHOR_ROAD", "region_map_section": "MAPSEC_AIGINA",
                     "map_type": "MAP_TYPE_ROUTE", "weather": "WEATHER_SUNNY"})
        if m in ICHOR_KIND:
            data["ichor_kind"] = ICHOR_KIND[m]
        data.update(events_of(m))
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    path = ROOT / "data/maps/AeginaTown/map.json"
    data = json.loads(path.read_text())
    d, nid, off = TOWN_CONNECTION
    conns = [c for c in (data.get("connections") or []) if c["map"] != nid]
    data["connections"] = conns + [{"map": nid, "offset": off, "direction": d}]
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# The walk model: every built cell of the four maps in the world frame
# ---------------------------------------------------------------------------

STEPS4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Walk:
    """What the player can do on each built cell: 'solid', 'ledge' (jump south),
    'grass' (tall grass) or 'open'. People and item balls block their cells.
    Moving between two maps is allowed only across a connection."""

    def __init__(self, with_objects=True):
        self.kind, self.owner = {}, {}
        for key, (bl, ox, oy) in self.sources().items():
            h, w = bl.shape
            for y in range(h):
                for x in range(w):
                    v = int(bl[y, x])
                    b = town.behavior(v & 0x3FF)
                    if b == "MB_JUMP_SOUTH":
                        k = "ledge"
                    elif v >> 10 & 3 or v >> 12 != 3:
                        k = "solid"
                    elif b == "MB_TALL_GRASS":
                        k = "grass"
                    else:
                        k = "open"
                    self.kind[(ox + x, oy + y)] = k
                    self.owner[(ox + x, oy + y)] = key
        self.objects = set()
        if with_objects:
            for m in MAPS:
                for o in events_of(m)["object_events"]:
                    self.objects.add((m.x + o["x"], m.y + o["y"]))
        links = {(ROAD.key, "town"), (ROAD.key, OROS.key), (ROAD.key, TEMPLE.key)}
        self.links = links | {(b, a) for a, b in links}

    @staticmethod
    def sources():
        out = {m.key: (blocks_of(m), m.x, m.y) for m in MAPS}
        out["town"] = (np.fromfile(town.LAYOUT / "map.bin", "<u2").reshape(town.H, town.W), TOWN_X, TOWN_Y)
        return out

    def ok(self, c, avoid=()):
        return self.kind.get(c) in ("open", "grass") and c not in self.objects and c not in avoid

    def moves(self, c, avoid=()):
        """Where one step from c can end: a ledge south of c is hopped."""
        for dx, dy in STEPS4:
            n = (c[0] + dx, c[1] + dy)
            if self.kind.get(n) == "ledge" and (dx, dy) == (0, 1):
                n = (n[0], n[1] + 1)
            if n not in self.kind:
                continue
            a, b = self.owner[c], self.owner[n]
            if a != b and (a, b) not in self.links:
                continue
            if self.ok(n, avoid):
                yield n

    def reach(self, starts, avoid=()):
        seen = {s for s in starts if self.ok(s, avoid)}
        q = deque(seen)
        while q:
            c = q.popleft()
            for n in self.moves(c, avoid):
                if n not in seen:
                    seen.add(n)
                    q.append(n)
        return seen

    def cost(self, starts, goals, avoid=(), weight=None):
        """0-1 BFS: the least weight of the cells entered from a start to a goal
        (by default, tall-grass steps); None if no walk reaches a goal."""
        weight = weight or (lambda c: 1 if self.kind[c] == "grass" else 0)
        dist, dq = {}, deque()
        for s in starts:
            if self.ok(s, avoid):
                dist[s] = weight(s)
                dq.append(s)
        while dq:
            c = dq.popleft()
            for n in self.moves(c, avoid):
                w = weight(n)
                if n not in dist or dist[c] + w < dist[n]:
                    dist[n] = dist[c] + w
                    (dq.appendleft if w == 0 else dq.append)(n)
        best = [dist[g] for g in goals if g in dist]
        return min(best) if best else None

    def grass_parts(self):
        seen, parts = set(), []
        for c, k in self.kind.items():
            if k != "grass" or c in seen:
                continue
            part, todo = set(), [c]
            seen.add(c)
            while todo:
                x, y = todo.pop()
                part.add((x, y))
                for dx, dy in STEPS4:
                    n = (x + dx, y + dy)
                    if self.kind.get(n) == "grass" and n not in seen:
                        seen.add(n)
                        todo.append(n)
            parts.append(part)
        return parts

    def forced_bands(self, starts, goals):
        bands = []
        if self.cost(starts, goals) is None:
            return bands
        for part in self.grass_parts():
            if self.cost(starts, goals, avoid=part) is None:
                depth = self.cost(starts, goals, weight=lambda c, p=part: 1 if c in p else 0)
                bands.append((part, depth))
        return sorted(bands, key=lambda b: -max(y for _, y in b[0]))

    def sight(self, x, y, facing, reach):
        dx, dy = FACING[facing]
        cells = []
        for i in range(1, reach + 1):
            c = (x + dx * i, y + dy * i)
            if self.kind.get(c) not in ("open", "grass"):
                break
            cells.append(c)
        return cells


def world_xy(m, x, y):
    return (m.x + x, m.y + y)


def goal_cells(name):
    m, x, y = GOALS[name]
    return [world_xy(m, x, y)]


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check(wd, verbose=True):
    errors, notes = [], []
    say = print if verbose else (lambda *a: None)
    w = Walk()
    start = [world_xy(ROAD, *p) for p in ROAD_START]

    # 1. seams: every edge cell that can be walked on faces a connection, with
    #    walkable ground across; everything else on an edge is sea or solid
    for m in MAPS:
        bord = np.fromfile(ROOT / "data/layouts" / m.folder / "border.bin", "<u2")
        if any(int(b) & 0x3FF != SEA for b in bord):
            errors.append(f"{m.key}: the border should be open sea")
        sides = {d for d, _, _ in CONNECTIONS[m]}
        for y in range(m.h):
            for x in range(m.w):
                if not (x in (0, m.w - 1) or y in (0, m.h - 1)):
                    continue
                c = world_xy(m, x, y)
                if w.kind[c] not in ("open", "grass"):
                    continue
                across = []
                if y == 0:
                    across.append(("up", (c[0], c[1] - 1)))
                if y == m.h - 1:
                    across.append(("down", (c[0], c[1] + 1)))
                if x == 0:
                    across.append(("left", (c[0] - 1, c[1])))
                if x == m.w - 1:
                    across.append(("right", (c[0] + 1, c[1])))
                for d, n in across:
                    if d not in sides or n not in w.kind:
                        errors.append(f"{m.key} ({x},{y}): walkable on the {d} edge with no map beyond")
                    elif w.kind[n] not in ("open", "grass"):
                        errors.append(f"{m.key} ({x},{y}): walkable on the {d} seam, but blocked across it")
    for tx in town.GATE_COLS:
        if w.kind.get((TOWN_X + tx, TOWN_Y - 1)) not in ("open", "grass"):
            errors.append(f"the town's gate column {tx} meets a blocked road cell")

    # 2. both ends can be reached from the gate, and nothing is a trap
    reach = w.reach(start)
    for name in GOALS:
        if not any(g in reach for g in goal_cells(name)):
            errors.append(f"no walk from the town's gate to {name}")
    preds = {}
    for c in reach:
        for n in w.moves(c):
            preds.setdefault(n, set()).add(c)
    home = set(start) & reach
    q = deque(home)
    while q:
        c = q.popleft()
        for p in preds.get(c, ()):
            if p not in home:
                home.add(p)
                q.append(p)
    trapped = sorted(reach - home)
    if trapped:
        errors.append(f"cells a player can reach but never leave: {trapped[:8]}{' ...' if len(trapped) > 8 else ''}")

    # 3. a forced band of tall grass on the way to each end
    for name in GOALS:
        bands = w.forced_bands(start, goal_cells(name))
        for part, depth in bands:
            ys = sorted({y for _, y in part})
            say(f"  to {name}: forced band at world rows {ys[0]}..{ys[-1]}, {len(part)} cells, "
                f"no fewer than {depth} grass steps")
        if not bands:
            errors.append(f"the walk to {name} has no forced grass band")
        elif any(d < 2 for _, d in bands):
            errors.append(f"a forced band on the walk to {name} can be crossed in under 2 steps")

    # 4. the trainers: placed on open ground, and the mandatory ones can't be skirted
    for name, (m, x, y, facing, sight, must, _gfx) in TRAINERS.items():
        c = world_xy(m, x, y)
        if w.kind.get(c) not in ("open", "grass"):
            errors.append(f"{name} at ({x},{y}) stands on a {w.kind.get(c)} cell")
            continue
        line = w.sight(*c, facing, sight)
        if len(line) < 2:
            errors.append(f"{name} at ({x},{y}) sees only {line}")
        for goal in must:
            ok = w.cost(start, goal_cells(goal), avoid=set(line)) is None
            say(f"  {name} at ({x},{y}) {facing[19:].lower()} sees {[(a - m.x, b - m.y) for a, b in line]}: "
                f"{'covers the only path' if ok else 'CAN be skirted'} to {goal}")
            if not ok:
                errors.append(f"{name}'s line can be skirted on the walk to {goal}")

    # 5. people and items on open ground the player can reach; signs readable
    for m in MAPS:
        for o in events_of(m)["object_events"]:
            c = world_xy(m, o["x"], o["y"])
            if w.kind.get(c) not in ("open", "grass"):
                errors.append(f"{m.key}: object at ({o['x']},{o['y']}) stands on a {w.kind.get(c)} cell")
            if not any((c[0] + dx, c[1] + dy) in reach for dx, dy in STEPS4):
                errors.append(f"{m.key}: nobody can walk up to the object at ({o['x']},{o['y']})")
    for m, x, y, name, (fx, fy) in BG:
        c, f = world_xy(m, x, y), world_xy(m, fx, fy)
        if abs(c[0] - f[0]) + abs(c[1] - f[1]) != 1:
            errors.append(f"{name}: its reading tile ({fx},{fy}) isn't next to it")
        if f not in reach:
            errors.append(f"{name} at ({x},{y}): its reading tile ({fx},{fy}) can't be reached")
        if w.kind.get(c) != "solid" and name != "DigSpot":
            errors.append(f"{name} at ({x},{y}) should be on its solid sign, herm or altar")
    for m, x, y, item, _flag, note in HIDDEN:
        if not any((m.x + x + dx, m.y + y + dy) in reach for dx, dy in STEPS4):
            errors.append(f"{m.key}: nobody can stand next to the hidden {item} at ({x},{y}), {note}")
    hm, hx, hy = next((m, x, y) for m, x, y, n, _ in BG if n == "GreatHerm")
    if world_xy(hm, hx, hy + 1) not in reach:
        errors.append("the tile south of the great herm (the Wings' landing) can't be reached")

    # 6. dead ends: every walkable cell with one way out should have something there
    marks = set()
    for m in MAPS:
        ev = events_of(m)
        marks |= {world_xy(m, o["x"], o["y"]) for o in ev["object_events"]}
        marks |= {world_xy(m, b["x"], b["y"]) for b in ev["bg_events"]}
    for c in sorted(reach):
        if w.owner[c] == "town":
            continue
        exits = [n for n in ((c[0] + dx, c[1] + dy) for dx, dy in STEPS4) if w.ok(n) or n in w.objects]
        if len(exits) <= 1 and not any(abs(c[0] - a) + abs(c[1] - b) <= 2 for a, b in marks):
            m = next(mm for mm in MAPS if mm.contains(*c))
            notes.append(f"dead end with nothing in it: {m.key} ({c[0] - m.x},{c[1] - m.y})")

    # 7. dry-ground pieces should sit on dry ground: nothing green beside them
    for y in range(YMIN, YMAX):
        for x in range(XMIN, XMAX):
            if wd.c(x, y) in ";oAtk" and any(m.contains(x, y) for m in MAPS):
                for dx, dy in STEPS4:
                    q2 = wd.c(x + dx, y + dy)
                    if family(q2) == "green" and q2 not in "%QYUC#_,SH":
                        notes.append(f"'{wd.c(x, y)}' at world ({x},{y}) touches the meadow at ({x + dx},{y + dy})")
                        break
    return errors, notes


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def renderer():
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    return rm, rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)),
                           rm.Tileset(rm.resolve_tileset("gTileset_Aegina", syms)))


def render_world_blocks():
    """The four maps' built cells in one frame, sea where no map is."""
    srcs = Walk.sources()
    x0 = min(ox for _, ox, _ in srcs.values()) - 2
    y0 = min(oy for _, _, oy in srcs.values()) - 2
    x1 = max(ox + bl.shape[1] for bl, ox, _ in srcs.values()) + 2
    y1 = max(oy + bl.shape[0] for bl, _, oy in srcs.values()) + 2
    grid = np.full((y1 - y0, x1 - x0), SEA | (1 << 12), np.uint16)
    for bl, ox, oy in srcs.values():
        h, wdt = bl.shape
        grid[oy - y0:oy - y0 + h, ox - x0:ox - x0 + wdt] = bl
    return grid, x0, y0


def draw_overlay(img, kinds, scale, events, lines, bands, title=None):
    from PIL import Image, ImageDraw, ImageFont
    img = img.convert("RGBA")
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = 16 * scale
    for (x, y), k in kinds.items():
        bx, by = x * c, y * c
        box = [bx, by, bx + c - 1, by + c - 1]
        if k == "solid":
            d.rectangle(box, fill=(255, 0, 0, 70))
        elif k == "ledge":
            d.rectangle(box, fill=(40, 90, 255, 90))
            d.polygon([(bx + 8, by + 10), (bx + c - 8, by + 10), (bx + c // 2, by + c - 6)], fill=(255, 255, 255, 230))
        elif k == "grass":
            d.rectangle(box, fill=(0, 255, 0, 50))
    for (x, y) in bands:
        d.rectangle([x * c + 1, y * c + 1, x * c + c - 2, y * c + c - 2], outline=(255, 235, 0, 255), width=3)
    for (x, y) in lines:
        d.rectangle([x * c + 7, y * c + 7, x * c + c - 8, y * c + c - 8], fill=(255, 0, 255, 150))
    for kind, (x, y) in events:
        bx, by = x * c, y * c
        if kind == "object":
            d.ellipse([bx + 4, by + 4, bx + c - 5, by + c - 5], outline=(255, 255, 0, 255), width=3)
        elif kind == "item":
            d.ellipse([bx + 6, by + 6, bx + c - 7, by + c - 7], outline=(0, 255, 255, 255), width=3)
        else:
            d.line([bx + 4, by + 4, bx + c - 5, by + c - 5], fill=(255, 255, 255, 255), width=3)
            d.line([bx + c - 5, by + 4, bx + 4, by + c - 5], fill=(255, 255, 255, 255), width=3)
    out = Image.alpha_composite(img, lay)
    if title:
        font = ImageFont.load_default(size=14)
        cap = Image.new("RGBA", (out.width, 26), (24, 24, 32, 255))
        ImageDraw.Draw(cap).text((8, 5), title, fill=(255, 255, 255, 255), font=font)
        sheet = Image.new("RGBA", (out.width, out.height + cap.height))
        sheet.paste(cap, (0, 0))
        sheet.paste(out, (0, cap.height))
        out = sheet
    return out.convert("RGB")


def all_events():
    evs = []
    for m in MAPS:
        ev = events_of(m)
        for o in ev["object_events"]:
            kind = "item" if o["graphics_id"] == "OBJ_EVENT_GFX_ITEM_BALL" else "object"
            evs.append((kind, world_xy(m, o["x"], o["y"])))
        for b in ev["bg_events"]:
            evs.append(("bg", world_xy(m, b["x"], b["y"])))
    return evs


def all_lines(w):
    out = []
    for name, (m, x, y, facing, sight, _must, _gfx) in TRAINERS.items():
        out += w.sight(*world_xy(m, x, y), facing, sight)
    return out


# The views a player sees along the walk: (name, map, the cell they stand on).
SCREENS = [
    ("01_gate", ROAD, 20, 21), ("02_orchard", ROAD, 17, 18), ("03_lower_terrace", ROAD, 14, 17),
    ("04_myrmex", ROAD, 12, 15), ("05_ant_hills", ROAD, 17, 14), ("06_upper_terrace", ROAD, 17, 11),
    ("07_band", ROAD, 21, 9), ("08_fork", ROAD, 21, 5), ("09_bay", ROAD, 14, 4),
    ("10_oros_path", ROAD, 8, 2), ("11_oros_foot", OROS, 8, 13), ("12_oros_climb", OROS, 5, 10),
    ("13_oros_summit", OROS, 6, 5), ("14_temple_steps", ROAD, 27, 4), ("15_temple_slope", TEMPLE, 12, 16),
    ("16_temple_front", TEMPLE, 12, 11), ("17_foundations", TEMPLE, 17, 11), ("18_east_plateau", ROAD, 33, 5),
    ("19_east_terraces", ROAD, 30, 13), ("20_way_home", ROAD, 25, 19),
]


def render(out_dir):
    from PIL import Image
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rm, r = renderer()
    w = Walk()
    start = [world_xy(ROAD, *p) for p in ROAD_START]
    band_cells = set()
    for name in GOALS:
        for part, _ in w.forced_bands(start, goal_cells(name)):
            band_cells |= part
    lines, evs = all_lines(w), all_events()
    for m in MAPS:
        bl = blocks_of(m)
        img = rm.render_blocks(r, (bl & 0x3FF).ravel(), m.w)
        img = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
        img.save(out_dir / f"{m.png}.png")
        kinds = {(x, y): w.kind[world_xy(m, x, y)] for y in range(m.h) for x in range(m.w)}
        loc = lambda cells: [(a - m.x, b - m.y) for a, b in cells if m.contains(a, b)]
        mevs = [(k, (a - m.x, b - m.y)) for k, (a, b) in evs if m.contains(a, b)]
        draw_overlay(img, kinds, 2, mevs, loc(lines), loc(band_cells),
                     f"{m.id}: red solid, blue ledge (jumps south), green tall grass, yellow forced band, "
                     f"magenta sight").save(out_dir / f"{m.png}_walk.png")
    grid, x0, y0 = render_world_blocks()
    img = rm.render_blocks(r, (grid & 0x3FF).ravel(), grid.shape[1])
    img.resize((img.width * 2, img.height * 2), Image.NEAREST).save(out_dir / "aigina_island.png")
    screens(rm, r, grid, x0, y0, out_dir)


def screens(rm, r, grid, x0, y0, out_dir):
    """GBA-screen views (15x10, the player on the 8th column and 5th row) at 2x,
    cut from the stitched island, so a view near a seam shows its neighbour as
    the game draws it."""
    from PIL import Image
    big = rm.render_blocks(r, (grid & 0x3FF).ravel(), grid.shape[1])
    sea = rm.render_blocks(r, np.array([SEA]), 1)
    pad = Image.new("RGB", (big.width + 2 * 16 * 8, big.height + 2 * 16 * 8))
    for yy in range(0, pad.height, 16):
        for xx in range(0, pad.width, 16):
            pad.paste(sea, (xx, yy))
    pad.paste(big, (16 * 8, 16 * 8))
    crops_dir = ROOT / "build/aigina_interior"
    crops_dir.mkdir(parents=True, exist_ok=True)
    crops = []
    for name, m, px, py in SCREENS:
        wx, wy = m.x + px - x0 + 8, m.y + py - y0 + 8
        crop = pad.crop(((wx - 7) * 16, (wy - 4) * 16, (wx + 8) * 16, (wy + 6) * 16))
        crop = crop.resize((crop.width * 2, crop.height * 2), Image.NEAREST)
        crop.save(crops_dir / f"screen_{name}.png")
        crops.append(crop)
    cols, cw, ch = 4, 15 * 32, 10 * 32
    sheet = Image.new("RGB", (cols * cw + (cols - 1) * 8, -(-len(crops) // cols) * (ch + 8) - 8), (24, 24, 32))
    for i, crop in enumerate(crops):
        sheet.paste(crop, ((i % cols) * (cw + 8), (i // cols) * (ch + 8)))
    sheet.save(out_dir / "aigina_interior_screens.png")


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR", help="also render the maps into DIR")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()
    if not town.CAT.exists():
        sys.exit(f"{town.CAT} is missing; run tools/ichor/art/aegina_build.py --no-compile first")
    wd = compose()
    write_layouts(wd)
    write_events()
    if args.render:
        render(args.render)
    if not args.no_check:
        errors, notes = check(wd)
        for n in notes:
            print("NOTE:", n)
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("aegina_detour: layouts and events written, checks pass")


if __name__ == "__main__":
    main()
