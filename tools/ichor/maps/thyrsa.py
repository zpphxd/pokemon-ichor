#!/usr/bin/env python3
"""Build Thyrsa City: the layout (56x48, aethos + thyrsa), its events, and the checks.

Writes:
  data/layouts/ThyrsaCity/map.bin, border.bin
  data/maps/ThyrsaCity/map.json         (events: people, warps, triggers, signs)

Thyrsa is a walled city on a long hill (SCRIPT.md Part 2, "Thyrsa City"). The
Cyclopean walls stand inside the seam strips, so every map edge is aethos's
hillside: the Elektran Gate on the south wall faces the road up from Route 7,
the Neistan Gate (west, to Route 8) and the Proitid Gate (east, to Euboia) open
through the side walls, and four gates are bricked up. Inside, five districts:
the lower town inside the Elektran Gate (the Asclepeion and the fountain of
Dirke on the left of the gate road, the Agora on the right, the Kantharos,
Pindaros and Eudora in the lanes east); the vineyards along the west wall; the
east hill, with the theater's high gate on its upper terrace and Polos and
Euthykles on the terrace below; the Agora square at the city's heart; and the
Kadmeia on the hill's top, up a broad stair, with Semele's chamber, Chthonia's
house, Manto's house on the citadel's edge and the Temple of Dionysus at the
head of the main street, framed by it all the way from the gate.

Thyrsa metatile ids come from build/thyrsa/catalog.json (TILES_thyrsa.md). Make it
with  /usr/bin/python3 tools/ichor/art/thyrsa_build.py

Usage: /usr/bin/python3 tools/ichor/maps/thyrsa.py [--render DIR] [--no-check]
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
CAT = ROOT / "build/thyrsa/catalog.json"
W, H = 56, 48
SEAM_ROWS, SEAM_COLS = 6, 8
SOUTH_SEAM = range(26, 30)       # the Elektran road at Route 7's columns 20-23, offset +6
WEST_ROAD = (23, 24)             # the Neistan road's rows at the west edge (Route 8, batch 2)
EAST_ROAD = (30, 31)             # the Proitid road's rows at the east edge (Euboia, batch 7)
MAPDIR = ROOT / "data/maps/ThyrsaCity"
LAYDIR = ROOT / "data/layouts/ThyrsaCity"

# ---------------------------------------------------------------------------
# aethos ids (TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS = 0x001
FLOWERS = 0x004
STELE_GRASS = 0x003
HERM = 0x01B
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))
BOULDER = 0x0E0
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}
LEDGE = {"s": 0x087, "w": 0x085, "e": 0x086, "sw": 0x08D, "se": 0x08E}

SURF_BEHAVIORS = {"MB_POND_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER"}
DOOR_BEHAVIORS = {"MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR"}


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
AETHOS_ATTR = np.fromfile(ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatile_attributes.bin", "<u2")


def thyrsa_attr():
    return np.fromfile(ROOT / "data/tilesets/secondary/thyrsa/porytiles_bin/metatile_attributes.bin", "<u2")


def behavior(mid, attr=None):
    if mid < 0x200:
        return MB.get(int(AETHOS_ATTR[mid]) & 0xFF, "?")
    attr = thyrsa_attr() if attr is None else attr
    return MB.get(int(attr[mid - 0x200]) & 0xFF, "?")


def hashed(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


# ---------------------------------------------------------------------------
# the grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self):
        self.mid = np.full((H, W), GRASS, np.uint16)
        self.solid = np.zeros((H, W), bool)
        self.built = np.zeros((H, W), bool)     # a structure's cell: no kerb, no shade logic
        self.cat = {s["key"]: s for s in json.loads(CAT.read_text())}

    def set(self, x, y, mid, solid=False, built=False):
        if 0 <= x < W and 0 <= y < H:
            self.mid[y, x] = mid
            self.solid[y, x] = solid
            if built:
                self.built[y, x] = True

    def part(self, key, name):
        s = self.cat[key]
        cx, cy = s["names"][name]
        return s["ids"][cy][cx], s["walk"][cy][cx]

    def put_part(self, key, name, x, y):
        mid, walk = self.part(key, name)
        self.set(x, y, mid, walk == "X", built=True)

    def put(self, key, x, y, cx=0, cy=0, w=None, h=None):
        s = self.cat[key]
        w = s["w"] - cx if w is None else w
        h = s["h"] - cy if h is None else h
        for j in range(h):
            for i in range(w):
                self.set(x + i, y + j, s["ids"][cy + j][cx + i], s["walk"][cy + j][cx + i] == "X",
                         built=True)

    def olive(self, x, y):
        below = y + 2 < H and self.mid[y + 2, x] == OLIVE_TOP[0]
        for i in range(2):
            self.set(x + i, y, OLIVE_TOP[i], True, built=True)
            self.set(x + i, y + 1, (OLIVE_BOT_TIP if below else OLIVE_BOT)[i], True, built=True)
        if y > 0:
            above = (int(self.mid[y - 1, x]), int(self.mid[y - 1, x + 1]))
            if above == OLIVE_BOT:
                for i in range(2):
                    self.set(x + i, y - 1, OLIVE_BOT_TIP[i], True, built=True)
            elif all(m in (GRASS, FLOWERS) for m in above) and not self.built[y - 1, x] \
                    and not self.built[y - 1, x + 1]:
                for i in range(2):
                    self.set(x + i, y - 1, OLIVE_TIP_GRASS[i], bool(self.solid[y - 1, x + i]))

    def cypress(self, x, y):
        self.set(x, y, CYPRESS_TOP, True, built=True)
        self.set(x, y + 1, CYPRESS_BOT, True, built=True)

    def free(self, x, y, w=1, h=1):
        return all(0 <= x + i < W and 0 <= y + j < H and self.mid[y + j, x + i] in (GRASS, FLOWERS)
                   and not self.solid[y + j, x + i] and not self.built[y + j, x + i]
                   for j in range(h) for i in range(w))


def edge_key(n, s_, w_, e, nw, ne, sw, se):
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


# ---------------------------------------------------------------------------
# The ground plan
# ---------------------------------------------------------------------------
#   o outside hillside (aethos grass; trees fill it)   r the road outside (aethos path)
#   c a clearing outside (open aethos grass)
#   p the street flags     g grass inside     a an earth lane (aethos path)
#   v vine rows (tall grass)    B a structure's footprint (walls, buildings)

def plan():
    P = [["o"] * W for _ in range(H)]

    def box(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                P[y][x] = c
    # inside the walls: the flags, then the gardens, lanes and footprints over them
    box(10, 3, 45, 37, "p")
    # the Kadmeia: gardens either side of the paved forecourt, a lane to Semele's
    # chamber, Manto's doorstep along the wall walk; the parapet and its stair
    box(10, 3, 21, 11, "g")
    box(34, 3, 45, 11, "g")
    box(13, 8, 21, 9, "a")
    box(19, 7, 19, 7, "a")
    box(34, 11, 41, 11, "a")
    box(10, 12, 45, 13, "B")
    box(26, 12, 29, 13, "p")
    # the vineyards along the west wall: two blocks of vines, the lane to the
    # Neistan Gate between them, the old terrace wall, a path along their east side
    box(10, 14, 20, 37, "g")
    box(11, 19, 18, 22, "v")
    box(19, 18, 19, 26, "a")
    box(10, 23, 20, 24, "a")
    box(18, 25, 20, 26, "a")
    box(10, 26, 17, 26, "B")
    box(11, 27, 18, 33, "v")
    box(19, 32, 20, 37, "p")
    # gardens in the square's corners and the theater's grove on the east hill
    box(21, 15, 23, 17, "g")
    box(32, 15, 34, 16, "g")
    box(35, 14, 45, 16, "g")
    box(34, 19, 45, 19, "B")
    # the Asclepeion's grove, the garden behind the Agora
    box(21, 25, 24, 27, "g")
    box(31, 26, 35, 27, "g")
    # footprints: the Asclepeion, the Agora, the Kantharos and Pindaros, Eudora and
    # her yard, Dirke, the gate's towers
    box(19, 28, 23, 31, "B")
    box(31, 28, 35, 31, "B")
    box(36, 26, 45, 29, "B")
    box(37, 33, 40, 35, "B")
    box(41, 32, 45, 35, "B")
    box(22, 33, 24, 34, "B")
    box(24, 36, 25, 37, "B")
    box(30, 36, 31, 37, "B")
    # the walls (strips, battlements and faces)
    box(8, 0, 9, 38, "B")
    box(46, 0, 47, 38, "B")
    box(10, 0, 45, 2, "B")
    box(8, 38, 47, 40, "B")
    # outside: the road up to the Elektran Gate, the Neistan and Proitid roads,
    # and the clearings by their gates
    box(26, 41, 29, 47, "r")
    box(25, 41, 30, 42, "r")
    box(14, 41, 24, 43, "c")
    box(31, 41, 41, 43, "c")
    box(4, 21, 7, 26, "c")
    box(0, 23, 7, 24, "r")
    box(48, 28, 51, 33, "c")
    box(48, 30, 55, 31, "r")
    return P


# ---------------------------------------------------------------------------
# composing the city
# ---------------------------------------------------------------------------

def ground(g, P):
    pv = lambda name: g.part("paving", name)[0]
    kb = lambda name: g.part("kerb", name)[0]
    KERB = {"tl": "NW", "t": "N", "tr": "NE", "l": "W", "r": "E", "bl": "SW", "b": "S", "br": "SE",
            "in_nw": "inNW", "in_ne": "inNE", "in_sw": "inSW", "in_se": "inSE"}
    vines = lambda name: g.part("vines", name)[0]
    for y in range(H):
        for x in range(W):
            c = P[y][x]
            if c in "ocg":
                g.set(x, y, GRASS)
            elif c in "ra":
                outside = "ocgv"
                n, s_, w_, e = [(0 <= yy < H and 0 <= xx < W and P[yy][xx] in outside)
                                for (xx, yy) in ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))]
                key = "c" if (n and s_) or (w_ and e) else edge_key(n, s_, w_, e, *[False] * 4)
                g.set(x, y, PATH.get(key, PATH["c"]))
            elif c == "v":
                west = x - 1 < 0 or P[y][x - 1] != "v"
                east = x + 1 >= W or P[y][x + 1] != "v"
                m = vines("W") if west else vines("E") if east else \
                    vines("grapes") if hashed(x, y, 3) < 0.3 else vines("row")
                g.set(x, y, m)
            elif c == "p":
                def out(dx, dy):
                    xx, yy = x + dx, y + dy
                    return 0 <= xx < W and 0 <= yy < H and P[yy][xx] in "gvaoc"
                key = edge_key(out(0, -1), out(0, 1), out(-1, 0), out(1, 0),
                               out(-1, -1), out(1, -1), out(-1, 1), out(1, 1))
                if key != "c":
                    g.set(x, y, kb(KERB[key]))
                else:
                    g.set(x, y, pv("crack") if hashed(x, y, 7) < 0.05 else pv("flag"))
            else:
                g.set(x, y, pv("flag"))


def shade(g, P):
    """The street flags in the shadow of a wall or a house to their north or west."""
    pv = lambda name: g.part("paving", name)[0]
    plain = {pv("flag"), pv("crack")}
    attr = thyrsa_attr()

    def caster(x, y):
        m = int(g.mid[y, x])
        if not g.built[y, x] or m < 0x200:
            return False
        return bool(g.solid[y, x]) or behavior(m, attr) in DOOR_BEHAVIORS
    for y in range(1, H):
        for x in range(1, W):
            if int(g.mid[y, x]) not in plain or g.built[y, x]:
                continue
            n = caster(x, y - 1)
            w_ = caster(x - 1, y)
            if n and w_:
                g.set(x, y, pv("shade_nw"))
            elif n:
                g.set(x, y, pv("shade_n"))
            elif w_:
                g.set(x, y, pv("shade_w"))


def walls(g):
    # --- the west and east strips, with their gates -------------------------
    for y in range(0, 38):
        g.put_part("strip", "run", 8, y)
        g.put_part("strip", "run_in", 9, y)
        g.put_part("strip_e", "run_in", 46, y)
        g.put_part("strip_e", "run", 47, y)
    g.put("side_gate", 8, 22)                 # the Neistan Gate: passage at (8-9, 24)
    g.put("side_gate_e", 46, 29)              # the Proitid Gate: passage at (46-47, 31)
    g.put_part("strip", "end", 8, 38)
    g.put_part("strip", "end_in", 9, 38)
    g.put_part("strip_e", "end_in", 46, 38)
    g.put_part("strip_e", "end", 47, 38)
    # --- the north wall, its face toward the Kadmeia -------------------------
    for x in range(10, 46):
        g.put("wall", x, 0, cx=1 + x % 2, w=1)
    # --- the south wall, its face toward the road --------------------------------
    for x in range(10, 46):
        g.put("wall", x, 38, cx=1 + x % 2, w=1, h=1)
    for x in range(8, 48):
        g.put("wall", x, 39, cx=1 + x % 2, cy=1, w=1, h=2)
    g.put("wall", 8, 39, cx=0, cy=1, w=1, h=2)
    g.put("wall", 47, 39, cx=3, cy=1, w=1, h=2)
    # ivy pouring over the battlements (even columns)
    for x in (16, 22, 34, 38):
        g.put("wall_ivy", x, 0)
    for x in (18, 36, 44):
        g.put("wall_ivy", x, 38)
    # the four bricked-up gates: two in the north wall, two in the south
    for (x, y) in ((12, 2), (42, 2), (14, 40), (40, 40)):
        g.put("arch_bricked", x, y)
    # the Elektran Gate
    g.put("elektran", 24, 36)


def kadmeia(g):
    # the parapet along the citadel's edge, and the broad stair through it
    for x in list(range(10, 26)) + list(range(30, 46)):
        g.put_part("parapet", "run", x, 12)
        g.put("terrace", x, 13, cx=1 + x % 2, w=1)
    g.put_part("parapet", "E", 25, 12)
    g.put_part("parapet", "W", 30, 12)
    g.put_part("parapet", "seat", 35, 12)
    g.put_part("terrace", "E", 25, 13)
    g.put_part("terrace", "W", 30, 13)
    stair(g, 26, 12, 4)
    # the temple at the head of the main street, its steps below it
    g.put("temple", 24, 4)
    stair(g, 24, 8, 8)
    # Semele's chamber, Chthonia's house of rough stones
    g.put("semele", 14, 6)
    g.put("sown_house", 18, 4)
    # Manto's house on the citadel's edge: limewashed, doves on the ridge
    DOORS["manto"] = house(g, 37, 8, lime=True, ridge=["doves", "run", "doves"],
                           eaves=[None, "eaves_mask", None], uppers=[],
                           lower=["window", "door", "window"])
    # the sacred grove: olives and cypresses
    g.olive(16, 3)
    g.olive(40, 4)
    g.olive(34, 4)
    for (x, y) in ((10, 5), (10, 9), (21, 4), (11, 9), (44, 3), (44, 7), (45, 5), (36, 6),
                   (43, 9)):
        if g.free(x, y, 1, 2):
            g.cypress(x, y)


def stair(g, x, y, w):
    for row, (wn, rn, en) in enumerate((("W", "run", "E"), ("W2", "run2", "E2"))):
        g.put_part("steps", wn, x, y + row)
        for i in range(1, w - 1):
            g.put_part("steps", rn, x + i, y + row)
        g.put_part("steps", en, x + w - 1, y + row)


def house(g, x, y, lime=False, ridge=(), eaves=None, uppers=(), lower=()):
    """A house from the kit: ridge and eaves rows, any upper storeys, the ground
    storey. Parts are named as in the catalog; 'x:<sign>' takes a trade sign."""
    up, ex, lo = ("upper_lime", "upper2_lime", "lower_lime") if lime else ("upper", "upper2", "lower")
    n = len(lower)
    eaves = eaves or [None] * n
    rows = [[("roof", "W")] + [("roof", r or "run") for r in ridge] + [("roof", "E")],
            [("roof", "eaves_W")] + [("roof", e or "eaves_run") for e in eaves] + [("roof", "eaves_E")]]
    for u in uppers:
        rows.append([(up, "W")] + [((ex, p[2:]) if p.startswith("x:") else (up, p)) for p in u]
                    + [(up, "E")])
    rows.append([(lo, "W")] + [(lo, p) for p in lower] + [(lo, "E")])
    for j, row in enumerate(rows):
        assert len(row) == n + 2, (x, y, j)
        for i, (k, p) in enumerate(row):
            g.put_part(k, p, x + i, y + j)
    door = [i for i, p in enumerate(lower) if p in ("door", "door_arched", "shop")]
    return (x + 1 + door[0], y + len(rows) - 1)


DOORS = {}


def town(g):
    # ---- the vineyards' head: Staphylos the vintner, his press -----------------
    DOORS["vintner"] = house(g, 11, 14, lime=True, ridge=[None, "chimney", None],
                             uppers=[["shutters", "x:vintner", "grille"]],
                             lower=["window", "door", "bench"])
    g.put("press", 17, 15)
    # the old terrace wall across the vineyards, its marked ivy by the city wall
    g.put("ivy_mark", 10, 26)
    for x in range(11, 17):
        g.put("terrace", x, 26, cx=1 + x % 2, w=1)
    g.put_part("terrace", "E", 17, 26)
    g.put("old_trellis", 11, 34)
    # ---- the east hill: the theater's gate on the upper terrace ------------------
    g.put("theater_gate", 42, 14)
    g.put_part("terrace", "W", 34, 19)
    for x in range(35, 45):
        g.put("terrace", x, 19, cx=1 + x % 2, w=1)
    g.put_part("terrace", "E", 45, 19)
    # Polos the old actor, and Euthykles the mask-maker, on the terrace below
    DOORS["actor"] = house(g, 35, 20, ridge=[None, None, "chimney"],
                           uppers=[["arched", "mask_tragic", "shutters"]],
                           lower=["bench", "door_arched", "window"])
    DOORS["masks"] = house(g, 40, 20, lime=True, ridge=["chimney", None, None],
                           uppers=[["grille", "x:mask_maker", "arched"]],
                           lower=["window", "shop", "wall"])
    # ---- the lanes east of the Agora: the Kantharos, Pindaros, Eudora ------------
    DOORS["tavern"] = house(g, 36, 26, ridge=[None, "chimney", None],
                            uppers=[["arched", "x:tavern", "shutters"]],
                            lower=["window", "door", "bench"])
    DOORS["pindaros"] = house(g, 41, 26, lime=True, ridge=[None, None, "chimney"],
                              uppers=[["shutters", "x:poet", "arched"]],
                              lower=["bench", "door", "window"])
    g.put("jars", 36, 30)
    DOORS["eudora"] = house(g, 37, 33, ridge=["chimney", None], eaves=[None, "eaves_mask"],
                            uppers=[], lower=["window", "door_arched"])
    # her walled yard, an old tree over it
    for y in (32, 35):
        g.put_part("court_wall", "W", 41, y)
        for x in range(42, 45):
            g.put_part("court_wall", "run", x, y)
        g.put_part("court_wall", "E", 45, y)
    for y in (33, 34):
        for x in range(41, 46):
            g.set(x, y, GRASS, True, built=True)
    g.olive(42, 33)
    # ---- the lower town: the Asclepeion and Dirke, the Agora -------------------
    g.put("asclepeion", 19, 28)
    g.put("dirke", 22, 33)
    g.put("agora", 31, 28)
    # ---- the square: a wine stall, garlands across the main street --------------
    g.put("stall_wine", 22, 19)
    g.put("statue", 32, 18)                    # the god in bronze
    for y in (21, 33):
        g.put_part("garland", "post_W", 25, y)
        for x in range(26, 30):
            g.put_part("garland", "swag", x, y)
        g.put_part("garland", "post_E", 30, y)
    # ---- signs ---------------------------------------------------------------------
    for (x, y) in SIGNS.values():
        g.put_part("stele", "sign", x, y)


# Signs on the flags (stele cells); their bg events are written with the events.
SIGNS = {
    "town": (32, 35),          # inside the Elektran Gate
    "kadmeia": (25, 14),       # at the foot of the Kadmeia stair
    "theater": (41, 17),       # on the theater terrace, beside the gate
    "neistan": (13, 25),       # by the Neistan Gate
    "proitid": (45, 30),       # by the Proitid Gate
}


def outside(g, P):
    """The hillside outside the walls: olives, pines and cypresses mixed in uneven
    depth, a few rocks; open only along the roads and in the clearings by the
    gates. Graves and a herm line the road up to the Elektran Gate."""
    def zone(x, y):
        return 0 <= x < W and 0 <= y < H and P[y][x] == "o"
    # the road's furniture first
    g.set(22, 42, STELE_GRASS, True, built=True)       # an old grave by the road
    g.set(33, 42, STELE_GRASS, True, built=True)
    g.set(31, 44, HERM, True, built=True)              # the herm at the city's approach
    cands = [(x, y) for y in range(H) for x in range(W) if zone(x, y)]
    cands.sort(key=lambda c: hashed(c[0], c[1], 21))
    for (x, y) in cands:
        r = hashed(x, y, 23)
        two = all(zone(x + i, y + j) for i in (0, 1) for j in (0, 1)) and g.free(x, y, 2, 2)
        if r < 0.62 and two:
            g.olive(x, y)
        elif r < 0.74 and two:
            g.set(x, y, PINE[0][0], True, built=True)
            g.set(x + 1, y, PINE[0][1], True, built=True)
            g.set(x, y + 1, PINE[1][0], True, built=True)
            g.set(x + 1, y + 1, PINE[1][1], True, built=True)
    for (x, y) in cands:
        if zone(x, y + 1) and g.free(x, y, 1, 2) and hashed(x, y, 5) < 0.8:
            g.cypress(x, y)
    # what's left of the hillside is scrub and rock: closed, so the hill reads as one
    for (x, y) in cands:
        if g.free(x, y):
            g.set(x, y, BOULDER if hashed(x, y, 9) < 0.35 else GRASS, True, built=True)
        else:
            g.solid[y, x] = True
    # flowers in the clearings
    for y in range(H):
        for x in range(W):
            if P[y][x] == "c" and g.free(x, y) and hashed(x, y, 13) < 0.16:
                g.set(x, y, FLOWERS)


def inside_greenery(g):
    """Trees and flowers in the city's gardens: the Kadmeia's sacred grove is in
    kadmeia(); here the square's plots, the Asclepeion's grove, the garden behind
    the Agora, the theater's grove and the vineyards' south end."""
    g.olive(22, 16)                       # the square's west plot
    for (x, y) in ((32, 15), (34, 15),    # the square's east plot
                   (21, 25), (24, 25),    # the Asclepeion's grove
                   (32, 26), (34, 26),    # behind the Agora
                   (35, 14), (39, 14), (41, 14), (45, 14),   # the theater's grove
                   (10, 14), (16, 17), (20, 14)):            # the vineyards' head
        if g.free(x, y, 1, 2):
            g.cypress(x, y)
    g.olive(37, 15)
    g.olive(15, 35)
    g.olive(18, 35)
    for y in range(H):
        for x in range(W):
            if g.free(x, y) and 10 <= x < 46 and 3 <= y < 38 and hashed(x, y, 17) < 0.14:
                g.set(x, y, FLOWERS)


def compose():
    g = Grid()
    P = plan()
    ground(g, P)
    walls(g)
    kadmeia(g)
    town(g)
    inside_greenery(g)
    outside(g, P)
    shade(g, P)
    return g, P


def border():
    return np.array([OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]], np.uint16)


def encode(g):
    attr = thyrsa_attr()
    out = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            mid = int(g.mid[y, x])
            water = behavior(mid, attr) in SURF_BEHAVIORS
            out[y, x] = mid | (int(g.solid[y, x]) << 10) | ((1 if water else 3) << 12)
    return out


# ---------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------

def obj(local_id, gfx, x, y, script, flag="0", move="MOVEMENT_TYPE_FACE_DOWN", trainer=False,
        sight=0, rx=0, ry=0, item=None):
    return {
        "local_id": local_id,
        "graphics_id": gfx,
        "x": x, "y": y, "elevation": 3,
        "movement_type": move,
        "movement_range_x": rx, "movement_range_y": ry,
        "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": item if item else str(sight),
        "script": script,
        "flag": flag,
    }


def item_ball(local_id, x, y, item, flag):
    d = obj(local_id, "OBJ_EVENT_GFX_ITEM_BALL", x, y, "Common_EventScript_FindItem", flag=flag,
            item=item)
    return d


S = "ThyrsaCity_EventScript_"


def events():
    objects = [
        obj("LOCALID_THYRSA_GATEKEEPER", "OBJ_EVENT_GFX_ICHOR_ELDER_M", 23, 37, S + "Gatekeeper",
            move="MOVEMENT_TYPE_FACE_RIGHT"),
        obj("LOCALID_THYRSA_MANTO", "OBJ_EVENT_GFX_ICHOR_MANTO", 35, 11, S + "Manto"),
        obj("LOCALID_THYRSA_ALETHEA", "OBJ_EVENT_GFX_ICHOR_ALETHEA_KNEEL", 17, 7, S + "Alethea",
            flag="FLAG_ICHOR_HIDE_ALETHEA_THYRSA", move="MOVEMENT_TYPE_FACE_LEFT"),
        obj("LOCALID_THYRSA_ALETHEA_GATE", "OBJ_EVENT_GFX_ICHOR_ALETHEA", 16, 24, S + "AletheaGate",
            flag="FLAG_TEMP_12", move="MOVEMENT_TYPE_FACE_LEFT"),
        obj("LOCALID_THYRSA_KRONIST", "OBJ_EVENT_GFX_ICHOR_KRONIST", 30, 27, S + "Kronist",
            move="MOVEMENT_TYPE_FACE_LEFT"),
        obj("LOCALID_THYRSA_HERALD", "OBJ_EVENT_GFX_ICHOR_HERALD", 28, 18, S + "Herald",
            flag="FLAG_ICHOR_DIONYSIA_DONE"),
        obj("LOCALID_THYRSA_NEISTAN_GUARD", "OBJ_EVENT_GFX_ICHOR_HOPLITE", 9, 24, S + "NeistanGuard",
            flag="FLAG_ICHOR_HIDE_NEISTAN_GUARDS", move="MOVEMENT_TYPE_FACE_RIGHT"),
        obj("LOCALID_THYRSA_NEISTAN_GUARD_B", "OBJ_EVENT_GFX_ICHOR_HOPLITE", 10, 25, S + "NeistanGuard",
            move="MOVEMENT_TYPE_FACE_UP"),
        obj("LOCALID_THYRSA_NEISTAN_GUARD_ASIDE", "OBJ_EVENT_GFX_ICHOR_HOPLITE", 11, 22,
            S + "NeistanGuard", flag="FLAG_TEMP_11", move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_THYRSA_NEISTAN_DRUM", "OBJ_EVENT_GFX_PUSHABLE_BOULDER", 9, 24, S + "NeistanDrum",
            flag="FLAG_ICHOR_HIDE_NEISTAN_DRUM"),
        obj("LOCALID_THYRSA_PROITID_GUARD", "OBJ_EVENT_GFX_ICHOR_HOPLITE", 46, 31, S + "ProitidGuard",
            move="MOVEMENT_TYPE_FACE_LEFT"),
        obj("LOCALID_THYRSA_THEATER_KEEPER", "OBJ_EVENT_GFX_ICHOR_HARVESTER_THYRSA", 44, 18, S + "TheaterKeeper",
            move="MOVEMENT_TYPE_FACE_LEFT"),
        obj("LOCALID_THYRSA_BEGGAR", "OBJ_EVENT_GFX_ICHOR_ELDER_M", 21, 34, S + "Beggar",
            move="MOVEMENT_TYPE_FACE_RIGHT"),
        obj("LOCALID_THYRSA_CITIZEN_MASKS", "OBJ_EVENT_GFX_ICHOR_WOMAN_THYRSA", 33, 20, S + "CitizenMasks",
            move="MOVEMENT_TYPE_FACE_LEFT"),
        obj("LOCALID_THYRSA_CITIZEN_SEER", "OBJ_EVENT_GFX_ICHOR_MERCHANT_THYRSA", 39, 25, S + "CitizenSeer",
            move="MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT", rx=2),
        obj("LOCALID_THYRSA_CITIZEN_KADMOS", "OBJ_EVENT_GFX_ICHOR_ELDER_F", 23, 24,
            S + "CitizenKadmos", move="MOVEMENT_TYPE_FACE_DOWN"),
        obj("LOCALID_THYRSA_CITIZEN_IVY", "OBJ_EVENT_GFX_ICHOR_MOM_THYRSA", 34, 36, S + "CitizenIvy",
            move="MOVEMENT_TYPE_FACE_UP"),
        obj("LOCALID_THYRSA_CITIZEN_CUSHION", "OBJ_EVENT_GFX_ICHOR_YOUTH_M", 21, 20,
            S + "CitizenCushion", move="MOVEMENT_TYPE_WANDER_UP_AND_DOWN", ry=1),
        obj("LOCALID_THYRSA_CHILD_1", "OBJ_EVENT_GFX_ICHOR_KID_M_THYRSA", 24, 15, S + "Child",
            move="MOVEMENT_TYPE_FACE_RIGHT"),
        obj("LOCALID_THYRSA_CHILD_2", "OBJ_EVENT_GFX_ICHOR_KID_F", 30, 15, S + "Child2",
            move="MOVEMENT_TYPE_FACE_LEFT"),
        obj("LOCALID_THYRSA_OINOPION", "OBJ_EVENT_GFX_ICHOR_VINTNER", 13, 22, S + "Oinopion",
            trainer=True, sight=3),
        obj("LOCALID_THYRSA_LENAIA", "OBJ_EVENT_GFX_ICHOR_MAENAD_THYRSA", 11, 30, S + "Lenaia",
            trainer=True, sight=2, move="MOVEMENT_TYPE_FACE_LEFT"),
        obj("LOCALID_THYRSA_HEGELOCHOS", "OBJ_EVENT_GFX_ICHOR_ACTOR", 38, 18, S + "Hegelochos",
            trainer=True, sight=2, move="MOVEMENT_TYPE_WALK_LEFT_AND_RIGHT", rx=2),
        # Manto's crows (Part 2, Manto's house): a flock over the road outside the
        # Elektran Gate, shown only for their scene (FLAG_TEMP_13, set on load)
        obj("LOCALID_THYRSA_CROWS", "OBJ_EVENT_GFX_ICHOR_CROWS", 27, 41, S + "Crows",
            flag="FLAG_TEMP_13"),
        obj("LOCALID_THYRSA_THYRSIVY", "OBJ_EVENT_GFX_SPECIES(THYRSIVY)", 13, 35, S + "Thyrsivy",
            flag="FLAG_ICHOR_HIDE_OMEN_THYRSIVY"),
        item_ball("LOCALID_THYRSA_ITEM_BLACK_SLUDGE", 19, 16, "ITEM_BLACK_SLUDGE",
                  "FLAG_ICHOR_ITEM_THYRSA_BLACK_SLUDGE"),
        item_ball("LOCALID_THYRSA_ITEM_SUPER_POTION", 18, 33, "ITEM_SUPER_POTION",
                  "FLAG_ICHOR_ITEM_THYRSA_SUPER_POTION"),
        item_ball("LOCALID_THYRSA_ITEM_BIG_NUGGET", 9, 28, "ITEM_BIG_NUGGET",
                  "FLAG_ICHOR_ITEM_THYRSA_BIG_NUGGET"),
    ]
    warps = [
        ("MAP_THYRSA_CITY_ASCLEPEION", (21, 31)),
        ("MAP_THYRSA_CITY_AGORA", (33, 31)),
        ("MAP_THYRSA_CITY_TAVERN", DOORS["tavern"]),
        ("MAP_THYRSA_CITY_TEMPLE_OF_DIONYSUS", (27, 7)),
        ("MAP_THYRSA_CITY_MASK_WORKSHOP", DOORS["masks"]),
        ("MAP_THYRSA_CITY_ACTOR_HOUSE", DOORS["actor"]),
        ("MAP_THYRSA_CITY_EUDORA_HOUSE", DOORS["eudora"]),
        ("MAP_THYRSA_CITY_MANTO_HOUSE", DOORS["manto"]),
        ("MAP_THYRSA_CITY_PINDAROS_HOUSE", DOORS["pindaros"]),
        ("MAP_THYRSA_CITY_SOWN_HOUSE", (19, 6)),
        ("MAP_THYRSA_CITY_VINTNER_HOUSE", DOORS["vintner"]),
        ("MAP_THYRSA_THEATER", (43, 17)),
        # the temple's palace door is two cells wide: its east leaf leads in too
        ("MAP_THYRSA_CITY_TEMPLE_OF_DIONYSUS", (28, 7)),
    ]
    warp_events = [{"x": x, "y": y, "elevation": 0, "dest_map": m, "dest_warp_id": "0"}
                   for m, (x, y) in warps]
    coord = []
    for x in SOUTH_SEAM:
        coord.append({"type": "trigger", "x": x, "y": 37, "elevation": 3, "var": "VAR_TEMP_1",
                      "var_value": "0", "script": f"{S}ArrivalX{x}"})
    # Manto's crows, from the inside of the Elektran Gate, in the evening or at night
    for x in SOUTH_SEAM:
        coord.append({"type": "trigger", "x": x, "y": 37, "elevation": 3, "var": "VAR_TEMP_3",
                      "var_value": "0", "script": S + "Crows"})
    coord.append({"type": "trigger", "x": 43, "y": 18, "elevation": 3, "var": "VAR_TEMP_2",
                  "var_value": "0", "script": S + "TheaterKeeperStop"})
    signs = [
        (SIGNS["town"], "TownSign"), (SIGNS["kadmeia"], "KadmeiaSign"),
        (SIGNS["theater"], "TheaterSign"), (SIGNS["neistan"], "NeistanSign"),
        (SIGNS["proitid"], "ProitidSign"),
        # (16,7), (22,34) and (12,2) are kept free for the hidden items (BUILD.md, Thyrsa)
        ((14, 7), "SemeleChamber"), ((15, 7), "SemeleCrack"),
        ((13, 2), "BrickedGate"), ((42, 2), "BrickedGate"),
        ((43, 2), "BrickedGate"), ((14, 40), "BrickedGate"), ((15, 40), "BrickedGate"),
        ((40, 40), "BrickedGate"), ((41, 40), "BrickedGate"),
        ((10, 26), "MarkedIvy"), ((23, 34), "Dirke"), ((17, 16), "WinePress"),
        ((18, 16), "WinePress"),
        ((13, 7), "DigSemele"), ((10, 33), "DigVineyard"),
        ((27, 4), "TempleFront"), ((28, 4), "TempleFront"),
        ((22, 42), "Grave"), ((33, 42), "Grave"), ((31, 44), "Herm"), ((32, 19), "Statue"),
    ]
    bg = [{"type": "sign", "x": x, "y": y, "elevation": 0,
           "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": S + name}
          for (x, y), name in signs]
    return objects, warp_events, coord, bg


def write_map_json():
    objects, warps, coord, bg = events()
    path = MAPDIR / "map.json"
    d = json.loads(path.read_text())
    d.update({
        "layout": "LAYOUT_THYRSA_CITY",
        # ICHOR_STUB_MUSIC: MUS_ICHOR_THYRSA (SCRIPT.md Part 9, cue 16) isn't composed yet
        "music": "MUS_ICHOR_EMPORION",
        "map_type": "MAP_TYPE_CITY",
        "weather": "WEATHER_SUNNY",
        "allow_cycling": True, "allow_escaping": False, "allow_running": True,
        "show_map_name": True,
        "connections": [{"map": "MAP_ROUTE7_KRONIA_GROUNDS", "offset": 6, "direction": "down"}],
        "object_events": objects, "warp_events": warps, "coord_events": coord, "bg_events": bg,
    })
    path.write_text(json.dumps(d, indent=2) + "\n")


def write_layout():
    g, P = compose()
    LAYDIR.mkdir(parents=True, exist_ok=True)
    encode(g).astype("<u2").tofile(LAYDIR / "map.bin")
    border().astype("<u2").tofile(LAYDIR / "border.bin")
    lj = ROOT / "data/layouts/layouts.json"
    t = lj.read_text()
    new = ('"id": "LAYOUT_THYRSA_CITY",\n      "name": "ThyrsaCity_Layout",\n      "width": 56,\n'
           '      "height": 48,\n      "primary_tileset": "gTileset_Aethos",\n'
           '      "secondary_tileset": "gTileset_Thyrsa",')
    t2 = re.sub(r'"id": "LAYOUT_THYRSA_CITY",\s*"name": "ThyrsaCity_Layout",\s*"width": \d+,\s*'
                r'"height": \d+,\s*"primary_tileset": "\w+",\s*"secondary_tileset": "\w+",', new, t)
    assert '"secondary_tileset": "gTileset_Thyrsa"' in t2
    if t2 != t:
        lj.write_text(t2)
    return g, P


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------

SCREENS = {
    "1_road": (27, 44), "2_gate": (27, 36), "3_lower_town": (24, 32), "4_square": (27, 22),
    "5_stair": (27, 15), "6_temple": (27, 10), "7_semele": (16, 9), "8_manto": (38, 11),
    "9_vineyards": (15, 24), "10_neistan": (9, 24), "11_terrace": (40, 18), "12_lanes": (40, 31),
    "13_proitid": (47, 31), "14_vines_south": (14, 32),
}


def render(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rm = [sys.executable, str(ROOT / "tools/ichor/render_map.py")]
    png = out_dir / "ThyrsaCity.png"
    subprocess.run(rm + ["LAYOUT_THYRSA_CITY", "--scale", "2", "-o", str(png)], check=True,
                   stdout=subprocess.DEVNULL)
    with_people(png, out_dir / "ThyrsaCity_events.png")
    overlay(png, out_dir / "ThyrsaCity_walk.png", 2)
    screens(out_dir)
    return png


def with_people(png, out):
    """Mark where people stand on the render (a small figure per object)."""
    from PIL import Image, ImageDraw
    im = Image.open(png).convert("RGBA")
    d = ImageDraw.Draw(im)
    ev = json.loads((MAPDIR / "map.json").read_text())
    c = 32
    for o in ev["object_events"]:
        x, y = o["x"] * c, o["y"] * c
        col = (250, 210, 60, 255) if "ITEM" in o["graphics_id"] else \
            (230, 80, 80, 255) if o["trainer_type"] != "TRAINER_TYPE_NONE" else (90, 170, 255, 255)
        d.ellipse([x + 8, y + 2, x + 23, y + 13], fill=col, outline=(20, 20, 20, 255))
        d.rectangle([x + 10, y + 13, x + 21, y + 29], fill=col, outline=(20, 20, 20, 255))
    im.save(out)


def screens(out_dir, margin=8):
    from PIL import Image
    blocks = np.fromfile(LAYDIR / "map.bin", "<u2").reshape(H, W)
    bord = np.fromfile(LAYDIR / "border.bin", "<u2").reshape(2, 2)
    big = np.empty((H + 2 * margin, W + 2 * margin), np.uint16)
    for y in range(big.shape[0]):
        for x in range(big.shape[1]):
            big[y, x] = bord[y % 2, x % 2]
    big[margin:margin + H, margin:margin + W] = blocks
    tmp = out_dir / "padded.bin"
    big.astype("<u2").tofile(tmp)
    png = out_dir / "padded.png"
    subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata", str(tmp),
                    "--width", str(big.shape[1]), "--primary", "aethos", "--secondary", "thyrsa",
                    "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png)
    c = 32
    crops = []
    for name, (px, py) in SCREENS.items():
        x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
        crop = im.crop((x0, y0, x0 + 15 * c, y0 + 10 * c))
        crops.append(crop)
    cols = 2
    sheet = Image.new("RGB", (cols * 15 * c + (cols - 1) * 8, -(-len(crops) // cols) * (10 * c + 8) - 8),
                      (24, 24, 32))
    for i, crop in enumerate(crops):
        sheet.paste(crop, ((i % cols) * (15 * c + 8), (i // cols) * (10 * c + 8)))
    sheet.save(out_dir / "ThyrsaCity_screens.png")
    tmp.unlink()
    png.unlink()


def overlay(png, out, scale):
    from PIL import Image, ImageDraw
    im = Image.open(png).convert("RGBA")
    blocks = np.fromfile(LAYDIR / "map.bin", "<u2").reshape(H, W)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = 16 * scale
    for y, row in enumerate(blocks):
        for x, b in enumerate(row):
            if b >> 10 & 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 70))
    ev = json.loads((MAPDIR / "map.json").read_text())
    for o in ev["object_events"]:
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5],
                  outline=(255, 255, 0, 255), width=2)
    for w_ in ev["warp_events"]:
        d.rectangle([w_["x"] * c + 2, w_["y"] * c + 2, w_["x"] * c + c - 3, w_["y"] * c + c - 3],
                    outline=(0, 255, 255, 255), width=2)
    for t in ev["coord_events"]:
        d.rectangle([t["x"] * c + 6, t["y"] * c + 6, t["x"] * c + c - 7, t["y"] * c + c - 7],
                    fill=(255, 0, 255, 160))
    for b in ev["bg_events"]:
        d.line([b["x"] * c + 3, b["y"] * c + 3, b["x"] * c + c - 4, b["y"] * c + c - 4],
               fill=(255, 255, 255, 255), width=2)
        d.line([b["x"] * c + c - 4, b["y"] * c + 3, b["x"] * c + 3, b["y"] * c + c - 4],
               fill=(255, 255, 255, 255), width=2)
    Image.alpha_composite(im, lay).save(out)


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def walkable(blocks, x, y):
    h, w = blocks.shape
    return 0 <= x < w and 0 <= y < h and not (blocks[y, x] >> 10 & 3) and blocks[y, x] >> 12 != 1


def reachable(blocks, start, blocked=()):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p not in seen and p not in blocked and walkable(blocks, *p):
                seen.add(p)
                q.append(p)
    return seen


# Cells the scenes walk people across, which must stay open.
SCRIPTED_PATHS = {
    # from (23,37) up to row 35, along it, and down to stand north of the player
    "Gatekeeper": [(23, 37), (23, 36)] + [(x, 35) for x in range(23, 30)]
                  + [(x, 36) for x in range(26, 30)],
    "Alethea at the gate": [(x, 24) for x in range(7, 17)] + [(10, 23)],
}


def check():
    errors = []
    blocks = np.fromfile(LAYDIR / "map.bin", "<u2").reshape(H, W)
    ev = json.loads((MAPDIR / "map.json").read_text())
    attr = thyrsa_attr()
    start = (27, H - 1)
    gates_shut = {(9, 24), (8, 24), (46, 31), (47, 31)}
    reach = reachable(blocks, start)
    objects = {(o["x"], o["y"]) for o in ev["object_events"]}
    for w_ in ev["warp_events"]:
        x, y = w_["x"], w_["y"]
        b = behavior(int(blocks[y, x]) & 0x3FF, attr)
        if b not in DOOR_BEHAVIORS:
            errors.append(f"warp at ({x},{y}) to {w_['dest_map']} is on {b}, not a door")
        if (x, y + 1) not in reach:
            errors.append(f"warp at ({x},{y}) to {w_['dest_map']} can't be reached from its doorstep")
    for o in ev["object_events"]:
        x, y = o["x"], o["y"]
        if o["local_id"] in ("LOCALID_THYRSA_ITEM_BIG_NUGGET",):
            continue                 # on the wall-walk, seen and not reached (the Thyrsus)
        if not walkable(blocks, x, y):
            errors.append(f"object {o['local_id']} at ({x},{y}) stands on a solid cell")
        elif (x, y) not in reach and o["local_id"] not in ("LOCALID_THYRSA_PROITID_GUARD",):
            errors.append(f"object {o['local_id']} at ({x},{y}) is unreachable")
    for t in ev["coord_events"]:
        if (t["x"], t["y"]) not in reach:
            errors.append(f"coord event at ({t['x']},{t['y']}) is unreachable")
    for b in ev["bg_events"]:
        x, y = b["x"], b["y"]
        fronts = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
        if not any(p in reach and p not in objects for p in fronts):
            errors.append(f"bg event {b['script']} at ({x},{y}) can't be read from a walkable tile")
    # the seams: aethos only, and open exactly where the roads run
    for y in range(H):
        for x in range(W):
            mid = int(blocks[y, x]) & 0x3FF
            if mid >= 0x200 and (y >= H - SEAM_ROWS or x < SEAM_COLS or x >= W - SEAM_COLS):
                errors.append(f"({x},{y}) is thyrsa metatile 0x{mid:03X} inside a seam strip")
    for x in range(W):
        if walkable(blocks, x, H - 1) != (x in SOUTH_SEAM):
            errors.append(f"south edge column {x} is {'open' if walkable(blocks, x, H - 1) else 'shut'}")
    for y in range(H):
        if walkable(blocks, 0, y) != (y in WEST_ROAD):
            errors.append(f"west edge row {y} is {'open' if walkable(blocks, 0, y) else 'shut'}")
        if walkable(blocks, W - 1, y) != (y in EAST_ROAD):
            errors.append(f"east edge row {y} is {'open' if walkable(blocks, W - 1, y) else 'shut'}")
    # with the side gates shut, the road from Route 7 must not reach the west or east roads
    shut = reachable(blocks, start, blocked=gates_shut)
    for y in WEST_ROAD:
        if (0, y) in shut:
            errors.append("the Neistan road can be reached from Route 7 without the gate")
    for y in EAST_ROAD:
        if (W - 1, y) in shut:
            errors.append("the Proitid road can be reached from Route 7 without the gate")
    for who, cells in SCRIPTED_PATHS.items():
        for (x, y) in cells:
            if not walkable(blocks, x, y) and (x, y) not in gates_shut:
                errors.append(f"{who}'s path crosses solid ({x},{y})")
    # trainers: Oinopion's sight must cross the lane
    if not all(walkable(blocks, 13, y) for y in (23, 24)):
        errors.append("Oinopion's lane is blocked")
    # the north edge: nothing walkable on row 0 (the border would show)
    if any(walkable(blocks, x, 0) for x in range(W)):
        errors.append("row 0 is walkable")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR", help="also render the map into DIR")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run tools/ichor/art/thyrsa_build.py first")
    write_layout()
    write_map_json()
    if args.render:
        print(render(args.render))
    if not args.no_check:
        errors = check()
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("thyrsa: layout and events written, checks pass")


if __name__ == "__main__":
    main()
