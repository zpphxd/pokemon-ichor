#!/usr/bin/env python3
"""Build Akti Town: the harbor's outdoor layout and its three interiors.

Writes:
  data/layouts/AktiTown/map.bin, border.bin           (28x28, aethos + akti)
  data/layouts/AktiTown_Asclepeion/map.bin, border.bin  (rooms/akti_asclepeion.bin)
  data/layouts/AktiTown_Agora/map.bin, border.bin       (rooms/akti_agora.bin)
  data/layouts/AktiTown_FishersHouse/map.bin, border.bin (rooms/fishers_house.bin)

Then it checks every Akti map.json against its blockdata: warps sit on doors or
exit mats, NPCs and coord triggers on walkable ground, bg events are readable
from a walkable tile, and the south seam is open exactly at x=10..13.

Akti metatile ids come from build/akti/catalog.json (see TILES_akti.md). Make it with
  /usr/bin/python3 tools/ichor/art/akti_build.py --no-compile

Usage: /usr/bin/python3 tools/ichor/maps/akti.py [--render DIR]
  --render writes akti_town.png (2x), akti_town_walk.png (collision overlay),
  screen-sized crops along the slice's route, and the interiors' renders into DIR.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/akti/catalog.json"
W, H = 28, 28
SEAM = range(10, 14)  # the walkable columns on the Route 1 seam

# ---------------------------------------------------------------------------
# aethos ids (General's numbering; see TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS = 0x001
GRASS_SHADE = 0x01C
REEDS = 0x015
TILLED = {"tl": 0x103, "t": 0x104, "tr": 0x105, "l": 0x10B, "c": 0x10C, "r": 0x10D,
          "bl": 0x113, "b": 0x114, "br": 0x115}
FLOWERS = 0x004
SEA = 0x170
STELE = 0x003            # town sign
HERM = 0x01B
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))   # an umbrella pine, 2x2
WALL = {"l": 0x148, "run": 0x149, "r": 0x14A, "w": 0x132, "e": 0x133}   # dry-stone walls
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
# sand set into grass (General's sand pit): its rim fades the beach into the meadow
SAND_GRASS = {"tl": 0x118, "t": 0x119, "tr": 0x11A, "l": 0x120, "c": 0x121, "r": 0x122,
              "bl": 0x128, "b": 0x129, "br": 0x12A}
SAND = {"tl": 0x11B, "t": 0x11C, "tr": 0x11D, "l": 0x123, "c": 0x124, "r": 0x125,
        "bl": 0x12B, "b": 0x12C, "br": 0x12D,
        "in_nw": 0x13D, "in_ne": 0x13E, "in_sw": 0x145, "in_se": 0x146}
ASCLEPEION = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
              [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
AGORA = [[0x028, 0x029, 0x029, 0x02B], [0x030, 0x031, 0x032, 0x033],
         [0x038, 0x039, 0x03A, 0x03B], [0x060, 0x041, 0x042, 0x043]]

SURF_BEHAVIORS = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
                  "MB_SOOTOPOLIS_DEEP_WATER"}
DOOR_BEHAVIORS = {"MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR", "MB_SOUTH_ARROW_WARP"}


def behavior_names():
    txt = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    out, v = {}, 0
    for name, val in re.findall(r"^\s*(MB_\w+)\s*(?:=\s*(\w+))?\s*,", txt, re.M):
        if val:
            v = int(val, 0)
        out[v] = name
        v += 1
    return out


MB = behavior_names()


def attrs(path):
    return np.fromfile(ROOT / path, "<u2")


AETHOS_ATTR = attrs("data/tilesets/primary/aethos/porytiles_bin/metatile_attributes.bin")
TILESET_ATTR = {
    "akti": attrs("data/tilesets/secondary/akti/porytiles_bin/metatile_attributes.bin"),
    "civic": attrs("data/tilesets/secondary/civic/porytiles_bin/metatile_attributes.bin"),
    "oikia": attrs("data/tilesets/secondary/oikia/porytiles_bin/metatile_attributes.bin"),
}


def behavior(mid, secondary="akti"):
    a = AETHOS_ATTR[mid] if mid < 0x200 else TILESET_ATTR[secondary][mid - 0x200]
    return MB.get(int(a) & 0xFF, "?")


def hashed(x, y, salt=0):
    """A stable pseudo-random number in [0, 1) for a map cell."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


# ---------------------------------------------------------------------------
# the grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.mid = np.full((h, w), GRASS, np.uint16)
        self.solid = np.zeros((h, w), bool)
        self.cat = {s["key"]: s for s in json.loads(CAT.read_text())}

    def set(self, x, y, mid, solid=False):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.mid[y, x] = mid
            self.solid[y, x] = solid

    def k(self, key, cx=0, cy=0):
        return self.cat[key]["ids"][cy][cx]

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        """Place an akti structure (or part of one); collision follows its walk grid."""
        s = self.cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                self.set(x + i, y + j, s["ids"][cy + j][cx + i], s["walk"][cy + j][cx + i] == "X")

    def block(self, rows, x, y, solid=True):
        for j, r in enumerate(rows):
            for i, m in enumerate(r):
                if m is not None:
                    self.set(x + i, y + j, m, solid)

    def olive(self, x, y):
        """A 2x2 olive. Its crown pokes into the row above, drawn over the player;
        stacked olives use the bottom-with-tip piece, as TILES_aethos.md says."""
        below = y + 2 < self.h and self.mid[y + 2, x] == OLIVE_TOP[0]
        self.block([OLIVE_TOP, OLIVE_BOT_TIP if below else OLIVE_BOT], x, y)
        if y > 0:
            above = (int(self.mid[y - 1, x]), int(self.mid[y - 1, x + 1]))
            if above == OLIVE_BOT:
                self.block([OLIVE_BOT_TIP], x, y - 1)
            elif all(m in (GRASS, GRASS_SHADE, FLOWERS) for m in above):
                self.block([OLIVE_TIP_GRASS], x, y - 1, solid=bool(self.solid[y - 1, x]))

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True)
        self.set(x, y + 1, CYPRESS_BOT, True)

    def pine(self, x, y):
        self.block(PINE, x, y)

    def free(self, x, y, w=1, h=1):
        """True if every cell is plain open grass."""
        return all(0 <= x + i < self.w and 0 <= y + j < self.h
                   and self.mid[y + j, x + i] in (GRASS, GRASS_SHADE) and not self.solid[y + j, x + i]
                   for j in range(h) for i in range(w))


def edge_key(n, s_, w_, e, nw, ne, sw, se):
    """Which edge piece a region cell needs, from which neighbours lie outside it."""
    if n and w_:
        return "tl"
    if n and e:
        return "tr"
    if s_ and w_:
        return "bl"
    if s_ and e:
        return "br"
    if n:
        return "t"
    if s_:
        return "b"
    if w_:
        return "l"
    if e:
        return "r"
    if nw:
        return "in_nw"
    if ne:
        return "in_ne"
    if sw:
        return "in_sw"
    if se:
        return "in_se"
    return "c"


def neighbours(plan, x, y, outside):
    h, w = len(plan), len(plan[0])

    def out(dx, dy):
        x2, y2 = x + dx, y + dy
        if not (0 <= x2 < w and 0 <= y2 < h):
            return False
        return plan[y2][x2] in outside
    return (out(0, -1), out(0, 1), out(-1, 0), out(1, 0), out(-1, -1), out(1, -1), out(-1, 1), out(1, 1))


# ---------------------------------------------------------------------------
# Akti Town
# ---------------------------------------------------------------------------
#
# The town is laid out from this plan, then the buildings and props go on top.
#   ~ open sea     q quay stone (harbor, mole, pier)     s sand     g grass
#   p limestone path     f the plaza's warm paving     t tilled earth (gardens)
#   B a building's footprint: the ground under it doesn't matter, and paving and
#     paths run flush against it instead of drawing a kerb or a grass rim
#
# The road climbs from the south gate to the plaza, where the krene stands
# against the Agora's terrace and the Temple of Hestia rises on its podium to the
# right. The harbor street runs on north to the quay. The trireme lies in the
# basin behind the mole, which runs out from the west headland; the beach curves
# round to Poseidon's shrine on the point. The lower town is gardens: the
# Asclepeion's herb beds, Diktys's boat by the gate, a shuttered house with its
# fig, washing and goat pen, and olive terraces at the edges.

PLAN = [
    #         1111111111222222222
    # 234567890123456789012345678
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~",  # 0
    "~~~~~~~~~~~~~~~~~~sssss~~~~~",  # 1
    "~~~~~~~~~~~~~~~~~~sssss~~~~~",  # 2
    "~~qqqqqqqqqq~~~~~~sssss~~~~~",  # 3
    "~~qqqqqqqqqq~~~~~~sssss~~~ss",  # 4
    "BBqqqqqqqqqq~~qq~~sssss~~sss",  # 5
    "BBqq~~~~~~~~~~qq~~~~~~~sssss",  # 6
    "BBqq~~~~~~~~~~qq~~~~~~ssssss",  # 7
    "ggqq~~~~~~~~~~qq~~~~~sssssss",  # 8
    "ggqqqqqqqqqqqqqqqqqqssssssss",  # 9
    "ggqqqqqqqqqqqqqqqqqqssssssss",  # 10
    "ggqqqqqqqqqqqqqqqqqqssssssss",  # 11
    "ggBBBBBBBBBpppggBBBBBBBggggg",  # 12
    "ggBBBBBBBBgpppggBBBBBBBggggg",  # 13
    "ggBBBBBBBBgpppggBBBBBBBggggg",  # 14
    "gggppgBBBBgpppggBBBBBBBggggg",  # 15
    "gggppgBBBBgpppggBBBBBBBggggg",  # 16
    "gggppBBBBBBBppggBBBBBBBggggg",  # 17
    "gggppffffffffffBBBBBBBBBgggg",  # 18
    "ggBBBBfffffffffffffffffggggg",  # 19
    "ggBBBBfffffffffffffffffggggg",  # 20
    "ggBBBBgffffffffffffggggggggg",  # 21
    "ggBBBBggggppppgggggggggggggg",  # 22
    "gggppppppppppppggggggggggggg",  # 23
    "gggppppppppppppggggggggggggg",  # 24
    "ggttttggggppppttgggggggggggg",  # 25
    "ggttttggggppppttgggggggggggg",  # 26
    "ggggggggggppppgggggggggggggg",  # 27
]
assert len(PLAN) == H
WATERISH = "~"


def ground(g):
    q = lambda cx, cy: g.k("quay", cx, cy)
    quay_pieces = {"tl": q(0, 0), "t": q(1, 0), "tr": q(2, 0), "l": q(0, 1), "r": q(2, 1),
                   "bl": q(0, 2), "b": q(1, 2), "br": q(2, 2),
                   "in_nw": q(3, 0), "in_ne": q(4, 0), "in_sw": q(3, 1), "in_se": q(4, 1)}
    pv = lambda cx, cy: g.k("plaza", cx, cy)
    paving_pieces = {"tl": pv(0, 0), "t": pv(1, 0), "tr": pv(2, 0), "l": pv(0, 1), "r": pv(2, 1),
                     "bl": pv(0, 2), "b": pv(1, 2), "br": pv(2, 2)}
    for y, row in enumerate(PLAN):
        assert len(row) == W, f"plan row {y} is {len(row)} wide"
        for x, c in enumerate(row):
            if c in WATERISH:
                g.set(x, y, SEA)
            elif c == "q":
                key = edge_key(*neighbours(PLAN, x, y, WATERISH))
                if key == "c":
                    # plain ashlar, with the two alternates scattered so long runs don't tile
                    r = hashed(x, y, 1)
                    m = q(3, 2) if r < 0.18 else q(4, 2) if r < 0.34 else q(1, 1)
                else:
                    m = quay_pieces[key]
                g.set(x, y, m)
            elif c == "s":
                key = edge_key(*neighbours(PLAN, x, y, WATERISH))
                if key == "c":
                    n, s_, w_, e, *_ = neighbours(PLAN, x, y, "g")
                    soft = edge_key(n, s_, w_, e, *[False] * 4)
                    g.set(x, y, SAND_GRASS[soft] if soft != "c" else SAND["c"])
                else:
                    g.set(x, y, SAND[key])
            elif c == "p":
                # paths fade into grass on every side; against paving, buildings or the
                # map edge they run on
                n, s_, w_, e, *_ = neighbours(PLAN, x, y, "gt")
                key = "c" if (n and s_) or (w_ and e) else edge_key(n, s_, w_, e, *[False] * 4)
                g.set(x, y, PATH.get(key, PATH["c"]))
            elif c == "f":
                n, s_, w_, e, *_ = neighbours(PLAN, x, y, "gtpqs")
                key = edge_key(n, s_, w_, e, False, False, False, False)
                if key == "c":
                    # the interior pair lays the marble flags on a two-cell repeat; a few
                    # plain limestone cells break it up
                    r = hashed(x, y, 2)
                    m = pv(3 + x % 2, 2) if r < 0.12 else pv(3 + x % 2, y % 2)
                else:
                    m = paving_pieces[key]
                g.set(x, y, m)
            elif c == "t":
                n, s_, w_, e, *_ = neighbours(PLAN, x, y, "gpsB")
                g.set(x, y, TILLED[edge_key(n, s_, w_, e, *[False] * 4)])
            else:
                g.set(x, y, GRASS)


def wall_run(g, x0, x1, y):
    """A west-east dry-stone wall from x0 to x1 inclusive."""
    for x in range(x0, x1 + 1):
        g.set(x, y, WALL["l"] if x == x0 else WALL["r"] if x == x1 else WALL["run"], True)


def terrace_run(g, x0, x1, y, steps=()):
    """Akti's retaining wall from x0 to x1, lower ground to the south, with steps."""
    t = lambda cx: g.k("terrace", cx, 0)
    for x in range(x0, x1 + 1):
        if x in steps:
            g.set(x, y, t(3), False)
        else:
            g.set(x, y, t(0) if x == x0 else t(4) if x == x1 else t(1 + (x - x0) % 2), True)


def headland(g, x, y0, y1):
    """The west headland from row y0 (its tip) to row y1 (its south face on grass),
    repeating its solid middle row for length."""
    rows = [0, 1] + [2] * (y1 - y0 - 2) + [3]
    for j, cy in enumerate(rows):
        g.put("headland", x, y0 + j, cy=cy, h=1)


def compose():
    g = Grid(W, H)
    ground(g)
    k = g.k
    rocks = lambda x, y: g.put("sea_rocks", x, y)

    # ---- the sea: the west headland runs out north, a channel, then a stack;
    # tide rocks lie off the beach
    headland(g, 0, 3, 8)
    g.put("sea_stack", 0, 0)
    rocks(3, 1)
    rocks(24, 3)
    rocks(17, 4)
    rocks(20, 7)

    # ---- the relic gates (SYSTEMS.md §1, D10): seen now, opened later ----------
    # The Bronze Hammer: the tide rocks' spur, its grotto choked with marble rubble
    # (bg events on row 4). Poseidon's Conch: the islet and its white shrine, out
    # of reach across the water; gulls circle it (object events). The sand east of
    # the shrine, x = 21, rows 2-4, is left for the landing when Surf arrives.
    g.put("grotto", 26, 1)
    g.put("shrine_poseidon", 19, 2)

    # ---- the mole, built out from the headland --------------------------------
    # its seaward coping is a parapet (keeps the player off row 3, so the map's
    # border never shows above the harbor); harbor goods stand along its middle row
    for x in range(2, 12):
        g.solid[3, x] = True
    g.put("boat_kaiki", 5, 1)                      # a kaiki moored outside the mole
    g.put("bollard_line", 6, 3)
    g.put("amphora_stack", 3, 4)
    g.put("rope_coil", 7, 4)
    g.put("octopus_line", 9, 4)

    # ---- the basin: the trireme Euploia, her gangplank down to the quay --------
    g.put("trireme", 4, 6)
    g.put("quay_gangplank", 7, 9)
    g.put("bollard_line", 4, 9)                    # her stern and bow lines
    g.put("bollard_line", 11, 9)
    g.put("boat_kaiki", 12, 1)                     # fishing boats off the pier
    g.put("boat_kaiki_left", 16, 7)
    g.put("rope_coil", 13, 9)

    # ---- the quay ---------------------------------------------------------------
    g.put("fish_stall", 16, 9)                     # the fishwife stands at (19,10)
    g.put("amphora_stack", 2, 11)                  # goods for the trireme by the Fisher's door
    g.put("rope_coil", 4, 11)
    for y in (9, 10, 11):
        g.set(20, y, k("quay_edges", 1, 0))        # the quay's flags run out onto the sand
    g.set(15, 12, k("quay_edges", 0, 0))

    # ---- the beach: tide rocks under the grotto, the boats hauled up, nets drying
    g.put("rocks_sand", 24, 7)                     # Hydna's tide rocks; the Pearl is hidden here
    g.put("beach_shells", 25, 9)
    g.put("boat_beached", 22, 10)
    g.put("net_poles", 26, 10)

    # ---- the harbor street and the Agora ------------------------------------------
    g.put("house_small", 2, 12)                    # Glaukos the fisher, by the harbor
    g.block(AGORA, 6, 13)                          # up its steps where the street meets the plaza
    g.set(7, 16, AGORA[3][1], False)
    wall_run(g, 6, 10, 12)                         # its yard wall, on the quay side
    g.set(14, 12, HERM, True)                      # THE QUAY

    # ---- the temple on its podium -------------------------------------------------
    g.put("temple_hestia", 16, 12)

    # ---- the terraces: the Agora's retaining wall runs on west to the edge, and the
    # temple's podium east through the olives, so the upper town reads as one level
    # above the plaza and the gardens
    terrace_run(g, -1, 11, 17, steps=(3, 4, 7, 8))
    terrace_run(g, 15, 28, 18, steps=(19, 26))
    for (x, y) in ((15, 13), (15, 16), (23, 13), (23, 16)):
        g.cypress(x, y)                            # sacred cypresses flank the temple

    # ---- the plaza -----------------------------------------------------------------
    g.put("krene", 9, 18)                          # the fountain house against the terrace
    g.put("altar", 20, 19)                         # Hestia's altar before the temple stairs

    # ---- the lower town: the town wall, the gate, gardens and yards ----------------
    wall_run(g, -1, 9, 27)                         # the field wall, open at the gate
    wall_run(g, 14, 28, 27)
    g.block(ASCLEPEION, 2, 19)
    g.set(3, 22, ASCLEPEION[3][1], False)
    g.put("boat_upturned", 7, 25)                  # Diktys sits at (9,25)
    g.set(14, 24, STELE, True)                     # AKTI TOWN, by the gate
    g.put("house_shuttered", 16, 23)
    g.put("fig_tree", 20, 21)
    g.put("laundry", 19, 26)
    # the goat pen, its south side the field wall
    wall_run(g, 22, 26, 23)
    for y in range(24, 27):
        g.set(22, y, WALL["w"], True)
        g.set(26, y, WALL["e"], True)

    # ---- greenery: olives in uneven depth, cypress spires, umbrella pines, rocks and
    # scrub, so the edges never settle into a rhythm
    # upper town, west and east of the harbor street; then the lower town
    for (x, y) in ((0, 10), (24, 14), (26, 16), (0, 19), (24, 20), (0, 25)):
        g.olive(x, y)
    for (x, y) in ((0, 14), (26, 12), (0, 22)):
        if g.free(x, y, 2, 2):
            g.pine(x, y)
    for (x, y) in ((0, 12), (2, 15), (27, 19), (27, 23), (6, 25), (23, 21)):
        if g.free(x, y, 1, 2):
            g.cypress(x, y)
    for (key, x, y) in (("shrubs", 24, 12), ("shrubs", 0, 16), ("rock_grass", 24, 16),
                        ("rock_grass", 0, 21), ("shrubs", 6, 22), ("rock_grass", 25, 22),
                        ("rock_grass", 8, 26)):
        if g.free(x, y, 2, 1):
            g.put(key, x, y)
    for (x, y) in ((10, 13), (10, 15), (14, 14), (14, 16), (5, 15), (1, 13), (2, 18),
                   (23, 15), (25, 17), (22, 22), (19, 22), (15, 22), (26, 19), (27, 25),
                   (2, 23), (21, 24)):
        if g.mid[y, x] == GRASS and not g.solid[y, x]:
            g.set(x, y, FLOWERS)
    return g


def border():
    return np.array([OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]], np.uint16)


def encode(g):
    out = np.zeros((g.h, g.w), np.uint16)
    for y in range(g.h):
        for x in range(g.w):
            mid = int(g.mid[y, x])
            water = behavior(mid) in SURF_BEHAVIORS
            elev = 1 if water else 3
            out[y, x] = mid | (int(g.solid[y, x]) << 10) | (elev << 12)
    return out


# ---------------------------------------------------------------------------
# interiors
# ---------------------------------------------------------------------------

ROOMS = {
    # layout dir: (room bin, width, void metatile for the border; see TILES_civic/oikia.md)
    "AktiTown_Asclepeion": ("akti_asclepeion", 15, 0x200),
    "AktiTown_Agora": ("akti_agora", 13, 0x200),
    "AktiTown_FishersHouse": ("fishers_house", 10, 0x210),
}

SOLID = 1 << 10
GROUND = 3 << 12


def asclepeion_without_stairs(blocks):
    """The slice has no upper floor, so paint the stairs at (0..1, 0..2) over with
    wall and shaded floor, as ROOMS_civic.md describes. Civic ids: asc_wall_top_l
    0x206, asc_wall_top 0x205, asc_wall 0x208, asc_floor_a_sh 0x203, asc_floor_b_sh
    0x204 (the checker is a where x+y is even)."""
    b = blocks.reshape(-1, 15)
    b[0, 0], b[0, 1] = 0x206 | SOLID, 0x205 | SOLID
    b[1, 0], b[1, 1] = 0x208 | SOLID, 0x208 | SOLID
    b[2, 0], b[2, 1] = 0x203 | GROUND, 0x204 | GROUND
    return b.reshape(-1)


def write_layouts():
    d = ROOT / "data/layouts/AktiTown"
    encode(compose()).astype("<u2").tofile(d / "map.bin")
    border().astype("<u2").tofile(d / "border.bin")
    for name, (room, _, void) in ROOMS.items():
        d = ROOT / "data/layouts" / name
        d.mkdir(parents=True, exist_ok=True)
        blocks = np.fromfile(ROOT / "design/phase1/rooms" / f"{room}.bin", "<u2")
        if name == "AktiTown_Asclepeion":
            blocks = asclepeion_without_stairs(blocks)
        blocks.astype("<u2").tofile(d / "map.bin")
        np.full(4, void, np.uint16).astype("<u2").tofile(d / "border.bin")


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

def render(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rm = [sys.executable, str(ROOT / "tools/ichor/render_map.py")]
    png = out_dir / "akti_town.png"
    subprocess.run(rm + ["LAYOUT_AKTI_TOWN", "--scale", "2", "-o", str(png)], check=True,
                   stdout=subprocess.DEVNULL)
    overlay(png, ROOT / "data/layouts/AktiTown/map.bin", W, out_dir / "akti_town_walk.png", 2)
    screens(out_dir)
    for name in ROOMS:
        lid = "LAYOUT_" + re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()
        subprocess.run(rm + [lid, "--scale", "3", "-o", str(out_dir / f"{name.lower()}.png")], check=True,
                       stdout=subprocess.DEVNULL)


# Where the player stands for each screen-sized review crop, along the slice's route.
SCREENS = {
    "1_gate": (11, 26), "2_plaza": (12, 20), "3_temple": (19, 17), "4_street": (12, 14),
    "5_quay": (8, 10), "6_pier": (14, 6), "7_beach": (23, 8), "8_asclepeion": (4, 23),
    "9_mole": (5, 5), "10_garden": (19, 25),
}


def screens(out_dir, margin=8):
    """Crop GBA-screen views (15x10 tiles, the player on the 8th column and 5th row)
    from the map padded with its border, at 2x, and tile them into one sheet."""
    from PIL import Image
    blocks = np.fromfile(ROOT / "data/layouts/AktiTown/map.bin", "<u2").reshape(H, W)
    bord = np.fromfile(ROOT / "data/layouts/AktiTown/border.bin", "<u2").reshape(2, 2)
    big = np.empty((H + 2 * margin, W + 2 * margin), np.uint16)
    for y in range(big.shape[0]):
        for x in range(big.shape[1]):
            big[y, x] = bord[y % 2, x % 2]
    big[margin:margin + H, margin:margin + W] = blocks
    tmp = out_dir / "padded.bin"
    big.astype("<u2").tofile(tmp)
    png = out_dir / "padded.png"
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(tmp),
                    "--width", str(big.shape[1]), "--primary", "aethos", "--secondary", "akti",
                    "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png)
    c = 32
    crops = []
    for name, (px, py) in SCREENS.items():
        x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
        crop = im.crop((x0, y0, x0 + 15 * c, y0 + 10 * c))
        crop.save(out_dir / f"screen_{name}.png")
        crops.append(crop)
    cols = 2
    sheet = Image.new("RGB", (cols * 15 * c + (cols - 1) * 8, -(-len(crops) // cols) * (10 * c + 8) - 8),
                      (24, 24, 32))
    for i, crop in enumerate(crops):
        sheet.paste(crop, ((i % cols) * (15 * c + 8), (i // cols) * (10 * c + 8)))
    sheet.save(out_dir / "screens_sheet.png")
    tmp.unlink()


def overlay(png, bin_path, width, out, scale):
    """Tint impassable cells red and water blue, and draw the map's events."""
    from PIL import Image, ImageDraw
    im = Image.open(png).convert("RGBA")
    blocks = np.fromfile(bin_path, "<u2").reshape(-1, width)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = 16 * scale
    for y, row in enumerate(blocks):
        for x, b in enumerate(row):
            if b >> 10 & 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 70))
            elif b >> 12 == 1:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 80, 255, 50))
    ev = json.loads((ROOT / "data/maps/AktiTown/map.json").read_text())
    for o in ev["object_events"]:
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5], outline=(255, 255, 0, 255), width=2)
    for w_ in ev["warp_events"]:
        d.rectangle([w_["x"] * c + 2, w_["y"] * c + 2, w_["x"] * c + c - 3, w_["y"] * c + c - 3], outline=(0, 255, 255, 255), width=2)
    for t in ev["coord_events"]:
        d.rectangle([t["x"] * c + 6, t["y"] * c + 6, t["x"] * c + c - 7, t["y"] * c + c - 7], fill=(255, 0, 255, 160))
    for b in ev["bg_events"]:
        d.line([b["x"] * c + 3, b["y"] * c + 3, b["x"] * c + c - 4, b["y"] * c + c - 4], fill=(255, 255, 255, 255), width=2)
        d.line([b["x"] * c + c - 4, b["y"] * c + 3, b["x"] * c + 3, b["y"] * c + c - 4], fill=(255, 255, 255, 255), width=2)
    Image.alpha_composite(im, lay).save(out)


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def walkable(blocks, x, y):
    h, w = blocks.shape
    return 0 <= x < w and 0 <= y < h and not (blocks[y, x] >> 10 & 3) and blocks[y, x] >> 12 != 1


def reachable(blocks, start, extra_open=()):
    seen, q = {start}, deque([start])
    h, w = blocks.shape
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p not in seen and (walkable(blocks, *p) or p in extra_open):
                seen.add(p)
                q.append(p)
    return seen


FLYERS = ("WINGULL",)

# Cells the scenes walk people across: they must stay open.
SCRIPTED_PATHS = {
    # Diktys from (9,25) to meet the player on the road, and back
    "Diktys": [(x, 25) for x in range(9, 14)] + [(x, 26) for x in range(10, 14)],
    # Alethea: up the road from (12,27), across the plaza, up to (19,18); then back
    # across and up the harbor street to the quay
    "Alethea": [(12, y) for y in range(19, 28)] + [(x, 19) for x in range(12, 20)]
               + [(19, 18)] + [(13, y) for y in range(11, 20)],
    # Kleon from (5,10): down, east along the back of the quay, down the street
    "Kleon": [(5, 11)] + [(x, 11) for x in range(5, 12)] + [(11, y) for y in range(11, 17)],
    # the player drawn up to the group from the trigger at x = 10
    "Player": [(x, y) for x in (8, 9, 10) for y in (9, 10, 11) if (x, y) != (8, 9)],
}


def check():
    errors = []
    maps = {
        "AktiTown": ("akti", W),
        "AktiTown_Asclepeion": ("civic", 15),
        "AktiTown_Agora": ("civic", 13),
        "AktiTown_FishersHouse": ("oikia", 10),
    }
    for name, (sec, width) in maps.items():
        blocks = np.fromfile(ROOT / "data/layouts" / name / "map.bin", "<u2").reshape(-1, width)
        ev = json.loads((ROOT / "data/maps" / name / "map.json").read_text())
        warps = [(w_["x"], w_["y"]) for w_ in ev["warp_events"]]
        start = warps[0] if name != "AktiTown" else (11, H - 1)
        objects = {(o["x"], o["y"]) for o in ev["object_events"]}
        reach = reachable(blocks, start if walkable(blocks, *start) else (start[0], start[1] - 1),
                          extra_open=set(warps))
        for (x, y) in warps:
            b = behavior(int(blocks[y, x]) & 0x3FF, sec)
            if b not in DOOR_BEHAVIORS:
                errors.append(f"{name}: warp at ({x},{y}) is on {b}, not a door")
            if (x, y) not in reach:
                errors.append(f"{name}: warp at ({x},{y}) is unreachable")
        for o in ev["object_events"]:
            x, y = o["x"], o["y"]
            if any(f in o["graphics_id"] for f in FLYERS):
                continue                           # gulls may hang over the water
            if not walkable(blocks, x, y):
                errors.append(f"{name}: object {o.get('local_id', o['graphics_id'])} at ({x},{y}) stands on a solid cell")
        for t in ev["coord_events"]:
            if (t["x"], t["y"]) not in reach:
                errors.append(f"{name}: coord event at ({t['x']},{t['y']}) is unreachable")
        for b in ev["bg_events"]:
            x, y = b["x"], b["y"]
            if (x, y) in reach and b["type"] != "hidden_item":
                continue
            fronts = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
            if b["type"] == "hidden_item" and (x, y) in reach:
                continue
            if not any(p in reach and p not in objects for p in fronts):
                errors.append(f"{name}: bg event at ({x},{y}) can't be read from any walkable tile")
        if name == "AktiTown":
            for x in range(width):
                ok = walkable(blocks, x, H - 1)
                if ok != (x in SEAM):
                    errors.append(f"AktiTown: south seam column {x} is {'open' if ok else 'closed'}")
            top = min(y for (x, y) in reach if y < H - 1)
            if top < 4:
                errors.append(f"AktiTown: row {top} is walkable, so the border shows above the harbor")
            for who, cells in SCRIPTED_PATHS.items():
                for (x, y) in cells:
                    if not walkable(blocks, x, y):
                        errors.append(f"AktiTown: {who}'s scripted path crosses solid ({x},{y})")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR", help="also render the maps into DIR")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run tools/ichor/art/akti_build.py --no-compile first")
    write_layouts()
    if args.render:
        render(args.render)
    if not args.no_check:
        errors = check()
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("akti: layouts written, checks pass")


if __name__ == "__main__":
    main()
