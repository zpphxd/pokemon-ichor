#!/usr/bin/env python3
"""Build Akti Town: the harbor's outdoor layout and its three interiors.

Writes:
  data/layouts/AktiTown/map.bin, border.bin           (28x26, aethos + kalliste)
  data/layouts/AktiTown_Asclepeion/map.bin, border.bin  (rooms/akti_asclepeion.bin)
  data/layouts/AktiTown_Agora/map.bin, border.bin       (rooms/akti_agora.bin)
  data/layouts/AktiTown_FishersHouse/map.bin, border.bin (rooms/fishers_house.bin)

Then it checks every Akti map.json against its blockdata: warps sit on doors or
exit mats, NPCs and coord triggers on walkable ground, bg events are readable
from a walkable tile, and the south seam is open exactly at x=10..13.

Kalliste metatile ids come from build/kalliste/catalog.json. Make it with
  /usr/bin/python3 tools/ichor/art/kalliste_build.py --no-compile

Usage: /usr/bin/python3 tools/ichor/maps/akti.py [--render DIR]
  --render writes akti_town.png (2x) and akti_town_walk.png (collision overlay)
  and the interiors' renders into DIR.
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
CAT = ROOT / "build/kalliste/catalog.json"
W, H = 28, 28
SEAM = range(10, 14)  # the walkable columns on the Route 1 seam

# ---------------------------------------------------------------------------
# aethos ids (General's numbering)
# ---------------------------------------------------------------------------
GRASS = 0x001
GRASS_SHADE = 0x01C
TILLED = (0x103, 0x104, 0x105, 0x10B, 0x10C, 0x10D, 0x113, 0x114, 0x115)  # TL T TR / L C R / BL B BR
TRIPOD_TOP, TRIPOD_BASE = 0x130, 0x131  # bronze tripod on a plinth (the temple's sign)
FLOWERS = 0x004
SEA = 0x170
STELE = 0x003            # town sign
HERM = 0x01B
BOULDER_SAND = 0x0E2
BOULDER_GRASS = 0x0E0
SEA_BOULDER = 0x18C                                # a rock in a foam ring, on deep water
SEA_ROCK_2X2 = ((0x150, 0x151), (0x158, 0x159))   # a rock across four cells, as on Route 115
SEA_STACK = ((0x175, 0x176), (0x17D, 0x17E))      # a rounded stack, 2x2
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
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
    "kalliste": attrs("data/tilesets/secondary/kalliste/porytiles_bin/metatile_attributes.bin"),
    "civic": attrs("data/tilesets/secondary/civic/porytiles_bin/metatile_attributes.bin"),
    "oikia": attrs("data/tilesets/secondary/oikia/porytiles_bin/metatile_attributes.bin"),
}


def behavior(mid, secondary="kalliste"):
    a = AETHOS_ATTR[mid] if mid < 0x200 else TILESET_ATTR[secondary][mid - 0x200]
    return MB.get(int(a) & 0xFF, "?")


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

    def k(self, key, cx, cy):
        return self.cat[key]["ids"][cy][cx]

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        """Place a kalliste structure (or part of one); collision follows its walk grid."""
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
            elif all(m in (GRASS, GRASS_SHADE) for m in above):
                self.block([OLIVE_TIP_GRASS], x, y - 1, solid=False)

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True)
        self.set(x, y + 1, CYPRESS_BOT, True)


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
# The town is laid out from this plan, then the buildings go on top.
#   ~ open sea     R rocks standing in the sea     q quay stone (harbor, mole, pier)
#   s sand         g grass                         p limestone path
#   f Cycladic flagstones (the plaza)              t tilled earth (the Asclepeion's herb bed)
#
# The eye from the south gate: the road climbs into the plaza, the Temple of Hestia
# stands over it on its podium to the right, and the main street runs on north to
# the quay, where the trireme lies in the basin behind the mole.

PLAN = [
    #         1111111111222222222
    # 234567890123456789012345678
    "RR~~~~~~~~~~~~~~~~~~~~~~~~RR",  # 0
    "RR~~~~~~~~~~~~~~~~~~~~R~~~RR",  # 1
    "R~~~~~~~~~~~~~~~~~~~~~~~~RRR",  # 2
    "R~~~~~~~~~~~~~~~~~~~~~~~~RRR",  # 3
    "RRqqqqqqqqqq~~~~~~~~~~~~~sss",  # 4
    "RRqqqqqqqqqq~~qq~~~~~~~sssss",  # 5
    "RRqqqqqqqqqq~~qq~~~~~~ssssss",  # 6
    "RRqq~~~~~~~~~~qq~~~~~sssssss",  # 7
    "RRqq~~~~~~~~~~qq~~~~ssssssss",  # 8
    "Rgqqqqqqqqqqqqqqqqqqssssssss",  # 9
    "ggqqqqqqqqqqqqqqqqqqssssssss",  # 10
    "ggqqqqqqqqqqqqqqqqqqssssssss",  # 11
    "gggggggggggpppgggggggggggggg",  # 12
    "gggggggggggpppgggggggggggggg",  # 13
    "gggggggggggpppgggggggggggggg",  # 14
    "ggpppggggggpppgggggggggggggg",  # 15
    "ggpppggggggpppgggggggggggggg",  # 16
    "ggpppggggggpppgggggggggggggg",  # 17
    "ggpppffffffffffggggggggggggg",  # 18
    "ggggggffffffffffffffffgggggg",  # 19
    "ggggggffffffffffffffffgggggg",  # 20
    "ggggggggggffffffgggggggggggg",  # 21
    "ggggggggggppppgggggggggggggg",  # 22
    "ggppppppppppppgggggggggggggg",  # 23
    "ggppppppppppppgggggggggggggg",  # 24
    "ggggggggggppppgggggggggggggg",  # 25
    "ggggggggggpppppppppggggggggg",  # 26
    "ggggggggggppppgggggggggggggg",  # 27
]
H = len(PLAN)
WATERISH = "~R"


def ground(g):
    q = lambda cx, cy: g.k("quay", cx, cy)
    quay_pieces = {"tl": q(0, 0), "t": q(1, 0), "tr": q(2, 0), "l": q(0, 1), "r": q(2, 1),
                   "bl": q(0, 2), "b": q(1, 2), "br": q(2, 2),
                   "in_nw": q(3, 0), "in_ne": q(4, 0), "in_sw": q(3, 1), "in_se": q(4, 1)}
    pv = lambda cx, cy: g.k("paving", cx, cy)
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
                    # plain paving, with the two alternates scattered so long runs don't tile
                    m = [q(1, 1), q(1, 1), q(3, 2), q(1, 1), q(4, 2), q(1, 1), q(1, 1)][(x * 3 + y * 5) % 7]
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
                # paths fade into grass on every side; against paving or the map edge they run on
                n, s_, w_, e, *_ = neighbours(PLAN, x, y, "gt")
                key = "c" if (n and s_) or (w_ and e) else edge_key(n, s_, w_, e, *[False] * 4)
                g.set(x, y, PATH.get(key, PATH["c"]))
            elif c == "f":
                n, s_, w_, e, *_ = neighbours(PLAN, x, y, "gtpqs")
                key = edge_key(n, s_, w_, e, False, False, False, False)
                if key == "c":
                    m = pv(1, 1) if (x * 7 + y * 3) % 5 == 0 else pv(3, (x + y) % 3)
                else:
                    m = paving_pieces[key]
                g.set(x, y, m)
            else:
                g.set(x, y, GRASS)


def compose():
    g = Grid(W, H)
    ground(g)
    k = lambda key, cx, cy: g.k(key, cx, cy)
    nets = lambda cx, cy: k("quay_nets", cx, cy)
    rock = lambda x, y: g.set(x, y, SEA_BOULDER, True)

    # ---- the sea's rocks ---------------------------------------------------------
    # the west headland breaks up into stacks and boulders beyond the mole
    g.block(SEA_STACK, 0, 0)
    g.block(SEA_ROCK_2X2, 0, 2)
    g.block(SEA_STACK, 0, 5)
    rock(1, 4)
    g.block(SEA_ROCK_2X2, 0, 7)
    rock(0, 9)
    rock(3, 2)
    # tide rocks off the beach point
    g.block(SEA_STACK, 26, 0)
    g.block(SEA_STACK, 24, 1)
    rock(22, 2)
    rock(23, 3)
    rock(24, 4)
    g.block(SEA_ROCK_2X2, 26, 2)
    rock(20, 0)

    # ---- the harbor ------------------------------------------------------------------
    # the mole, with bollards and a net drying near its head
    for x in (4, 9):
        g.set(x, 4, k("quay_steps", 2, 0), True)
    g.set(6, 5, nets(0, 0), True)
    g.set(7, 5, nets(1, 0), True)
    g.set(10, 5, nets(2, 0), True)
    # the trireme Euploia, alongside the quay: stern, three midships, bow
    kai = lambda cx, cy: k("boat_kaiki", cx, cy)
    for j in range(2):
        g.block([[kai(0, j), kai(1, j), kai(1, j), kai(1, j), kai(2, j)]], 5, 7 + j)
    g.set(7, 9, k("quay_steps", 0, 0))            # steps down to her side: the gangplank
    g.put("boat_kaiki", 16, 4)                     # fishing boats off the pier
    g.put("boat_kaiki_left", 17, 7)
    for x in (4, 11):
        g.set(x, 9, k("quay_steps", 2, 0), True)   # bollards on the quay's coping
    # cargo for the trireme, stacked against the Fisher's house
    g.set(2, 11, nets(0, 1), True)
    g.set(3, 11, nets(1, 1), True)
    g.set(4, 11, nets(2, 1), True)
    # the fish stall by the pier: crates of the catch and a jar of brine. The quay
    # runs past it to the beach on rows 9 and 11.
    g.set(17, 10, nets(2, 1), True)
    g.set(18, 10, nets(2, 1), True)
    g.set(19, 10, nets(3, 1), True)

    # ---- buildings -------------------------------------------------------------------
    g.put("house_small", 2, 12)                    # Glaukos the fisher, by the harbor
    # the Agora, up a flight of steps where the harbor street meets the plaza
    g.block(AGORA, 6, 13)
    g.set(7, 16, AGORA[3][1], False)
    g.set(5, 12, k("wall_drystone", 0, 0), True)   # its yard wall, on the quay side
    for x in range(6, 10):
        g.set(x, 12, k("wall_drystone", 1 + x % 2, 0), True)
    g.set(10, 12, k("wall_drystone", 3, 0), True)
    terrace = lambda cx: k("terrace", cx, 0)
    g.set(5, 17, terrace(0), True)
    for x in range(6, 10):
        g.set(x, 17, terrace(1 + x % 2), True)
    g.set(10, 17, terrace(4), True)
    g.set(7, 17, terrace(3), False)
    g.set(8, 17, terrace(3), False)
    # the Temple of Hestia on its podium, crowning the plaza
    g.put("temple_hestia", 16, 12)
    g.set(15, 18, terrace(0), True)
    for x in range(16, 23):
        g.set(x, 18, terrace(1 + x % 2), True)
    g.set(23, 18, terrace(4), True)
    g.set(19, 18, terrace(3), False)
    for (x, y) in ((15, 13), (15, 16), (23, 13), (23, 16)):
        g.cypress(x, y)                            # sacred cypresses flank the temple
    # the Asclepeion, set back in its garden off the plaza
    g.block(ASCLEPEION, 2, 19)
    g.set(3, 22, ASCLEPEION[3][1], False)
    g.block([[TILLED[0], TILLED[2]], [TILLED[6], TILLED[8]]], 6, 21, solid=False)  # its herb bed
    # a shut two-storey house below the plaza
    g.put("house_large", 17, 21)
    g.solid[25, 18] = True                         # no interior: its door is barred
    # Poseidon's shrine out on the beach point, looking over the cove
    g.put("shrine_poseidon", 25, 5)

    # ---- signs -------------------------------------------------------------------------
    g.set(14, 24, STELE, True)                     # AKTI TOWN, by the gate
    g.set(22, 19, TRIPOD_TOP, False)               # a bronze tripod beside the temple's altar
    g.set(22, 20, TRIPOD_BASE, True)
    g.set(14, 12, HERM, True)                      # THE QUAY
    # the south edge: a field wall below the shut house's lane
    for x in range(14, 20):
        g.set(x, 27, k("wall_drystone", 1 + x % 2, 0), True)

    # ---- Diktys's net yard by the gate --------------------------------------------------
    g.set(6, 25, nets(0, 0), True)
    g.set(7, 25, nets(1, 0), True)
    g.set(8, 25, nets(2, 0), True)

    # ---- the beach: boulders at its back, where the dunes meet the grass ----------------
    for (x, y) in ((21, 10), (22, 11), (27, 9), (27, 10), (22, 7), (25, 9)):
        g.set(x, y, BOULDER_SAND, True)
    # an altar before the temple stairs, with its fire lit (Elaia's marble altar, on paving)
    g.put("altar_square", 20, 19)

    # ---- trees: olives in staggered depth, cypress spires between ---------------------
    olives = [(0, 10), (0, 13), (1, 15), (0, 18), (0, 21), (0, 24), (0, 26), (2, 26), (5, 26),
              (8, 26), (24, 12), (26, 14), (24, 16), (26, 19), (24, 21), (26, 23), (23, 26),
              (25, 26), (20, 26)]
    for (x, y) in sorted(olives, key=lambda p: -p[1]):
        g.olive(x, y)
    for (x, y) in ((0, 12), (0, 16), (1, 17), (0, 20), (1, 23), (4, 26), (7, 26),
                   (2, 24), (9, 21), (16, 22), (22, 22), (27, 12), (27, 17), (22, 26),
                   (27, 21), (27, 26), (22, 24)):
        if not g.solid[y, x] and not g.solid[y + 1, x]:
            g.cypress(x, y)
    for (x, y) in ((4, 15), (4, 16), (5, 15), (8, 22), (14, 21), (15, 21), (20, 19), (21, 19),
                   (10, 13), (10, 14), (1, 19), (13, 20), (25, 18), (26, 18), (12, 25)):
        if g.mid[y, x] == GRASS:
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
    "9_mole": (5, 5),
}


def screens(out_dir, margin=8):
    """Crop GBA-screen views (15x10 tiles, the player on the 8th column and 5th row)
    from the map padded with its border, at 2x."""
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
                    "--width", str(big.shape[1]), "--primary", "aethos", "--secondary", "kalliste",
                    "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png)
    c = 32
    for name, (px, py) in SCREENS.items():
        x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
        im.crop((x0, y0, x0 + 15 * c, y0 + 10 * c)).save(out_dir / f"screen_{name}.png")
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


def check():
    errors = []
    maps = {
        "AktiTown": ("kalliste", W),
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
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR", help="also render the maps into DIR")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run tools/ichor/art/kalliste_build.py --no-compile first")
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
