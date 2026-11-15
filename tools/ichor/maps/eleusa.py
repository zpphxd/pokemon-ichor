#!/usr/bin/env python3
"""Build Eleusa Village: layout, events, checks and review renders.

Eleusa is a farming village round the sanctuary of the Mysteries
(design/phase2/SCRIPT.md, "Eleusa Village"; design/AETHOS_MAP.md). Gold wheat
and dark doors: the Sacred Way comes in from Route 5 on the west, runs through
the village to the well-yard, and climbs through the Propylaia to the court of
the Telesterion, the crown of the village, with the Ploutonion's cave mouth in
the rock beside it. Fields lie south and west; the Eleutherai road (Route 6)
leaves north and the road of the Mysteries (Route 15, shut in Act I) east.

Pieces come by key and name from build/eleusa/catalog.json (TILES_eleusa.md;
make it with /usr/bin/python3 tools/ichor/art/eleusa_build.py --no-compile).

Writes:
  data/layouts/EleusaVillage/map.bin, border.bin   (50x40, aethos + eleusa)
  data/maps/EleusaVillage/map.json                 its events, from the tables below
  data/maps/EleusaVillage/scripts.pory             the generated block between the markers
  the placeholder interiors' return warps (data/maps/EleusaVillage_*/map.json,
  data/maps/EleusaSanctum_B1F/map.json), so every door resolves both ways

Checks: every warp on a door and reachable; people on open ground and
reachable; every sign readable; no walkable pocket cut off from the west
gate; the seams open where BUILD.md says and only aethos metatiles within 8
columns of the west and east seams and 6 rows of the north one.

Usage: /usr/bin/python3 tools/ichor/maps/eleusa.py [--render DIR] [--walk]
  --render DIR  writes eleusa_village.png (2x, with people), eleusa_village_walk.png
                (collision overlay), screen views along the route and a contact sheet
  --walk        prints the walk map (# solid, . reachable, ? cut off)
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
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor"))
import eleusa_lib as E  # noqa: E402

CAT = ROOT / "build/eleusa/catalog.json"
NAME = "EleusaVillage"
LAYOUT_ID = "LAYOUT_ELEUSA_VILLAGE"
MAP_DIR = ROOT / "data/maps" / NAME
LAYOUT_DIR = ROOT / "data/layouts" / NAME
W, H = 50, 40

# ---------------------------------------------------------------------------
# The seams (BUILD.md's connections table). None of the three neighbours exists
# yet, so map.json carries no connections; the openings are built and checked.
# ---------------------------------------------------------------------------
WEST_SEAM = range(24, 28)     # rows open on x = 0: Route 5, the Skironian cliffs
NORTH_SEAM = range(44, 48)    # columns open on y = 0: Route 6, the Eleutherai road
EAST_SEAM = range(24, 28)     # rows open on x = 49: Route 15, shut in Act I
STRIP_COLS = 8                # aethos only within 8 columns of a left/right seam
STRIP_ROWS = 6                # and within 6 rows of an up/down one (MAP_DESIGN.md §5)

# ---------------------------------------------------------------------------
# aethos ids (TILES_aethos.md)
# ---------------------------------------------------------------------------
GRASS = 0x001
SHADE = 0x01C
TALL = 0x00D                  # barley tufts: the poppy meadow's tall grass
FLOWERS = 0x004
STELE = 0x003
SKEP = 0x0E0                  # tan boulder on grass: stands in for a straw beehive (as in Elaia)
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
OLIVE_TIP_TALL = (0x1C6, 0x1C7)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
CYPRESS_TOP_OVER_OLIVE = (0x1EC, 0x1ED)
CYPRESS_BOT_UNDER_TIP = (0x1F4, 0x1F5)
PINE = ((0x01E, 0x01F), (0x026, 0x027))
WALL = {"l": 0x148, "run": 0x149, "r": 0x14A, "w": 0x132, "e": 0x133}
PATH = {"tl": 0x1D0, "t": 0x1D1, "tr": 0x1D2, "l": 0x1D8, "c": 0x1D9, "r": 0x1DA,
        "bl": 0x1E0, "b": 0x1E1, "br": 0x1E2}

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
AETHOS_ATTR = np.fromfile(ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatile_attributes.bin", "<u2")
ELEUSA_ATTR = np.fromfile(ROOT / "data/tilesets/secondary/eleusa/porytiles_bin/metatile_attributes.bin", "<u2")


def behavior(mid):
    a = AETHOS_ATTR[mid] if mid < 0x200 else ELEUSA_ATTR[mid - 0x200]
    return MB.get(int(a) & 0xFF, "?")


def noise(x, y, salt=0):
    """A stable 0..99 per cell."""
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 100


# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------

class Grid:
    def __init__(self):
        cat = json.loads(CAT.read_text())
        self.s = {d["key"]: d for d in cat["structures"]}
        self.fronts = cat["fronts"]
        self.mt = np.full((H, W), GRASS, np.int32)
        self.solid = np.zeros((H, W), bool)
        self.kind = np.full((H, W), "grass", object)

    def set(self, x, y, mid, solid, kind=None):
        if 0 <= x < W and 0 <= y < H:
            self.mt[y, x] = mid
            self.solid[y, x] = solid
            if kind:
                self.kind[y, x] = kind

    def ids(self, key, name):
        d = self.s[key]
        cx, cy = d["names"][name]
        return d["ids"][cy][cx], d["walk"][cy][cx]

    def put(self, key, x, y, cells=None, kind=None):
        """An Eleusa structure with its top-left at (x, y); collision follows its
        walk grid (X blocks; . T G D are open)."""
        d = self.s[key]
        for j in range(d["h"]):
            for i in range(d["w"]):
                if cells is not None and (i, j) not in cells:
                    continue
                self.set(x + i, y + j, d["ids"][j][i], d["walk"][j][i] == "X", kind or key)

    def piece(self, key, name, x, y, kind=None):
        mid, walk = self.ids(key, name)
        self.set(x, y, mid, walk == "X", kind or key)

    def front(self, key, x, y):
        """A house front from the kit: every cell blocks but its doors."""
        for j, row in enumerate(self.fronts[key]["ids"]):
            for i, mid in enumerate(row):
                if mid is not None:
                    door = behavior(mid) in DOOR_BEHAVIORS
                    self.set(x + i, y + j, mid, not door, "door" if door else "house")

    def doors(self, x0, y0, x1, y1):
        return [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
                if behavior(int(self.mt[y, x])) in DOOR_BEHAVIORS]

    # --- trees (aethos) --------------------------------------------------------
    def olive(self, x, y):
        for i in range(2):
            self.set(x + i, y, OLIVE_TOP[i], True, "olive_top")
            self.set(x + i, y + 1, OLIVE_BOT[i], True, "olive_bot")
        if y == 0:
            return
        for i in range(2):
            k = self.kind[y - 1, x + i]
            if k == "olive_bot":
                self.mt[y - 1, x + i] = OLIVE_BOT_TIP[i]
            elif k == "cypress_bot":
                self.mt[y - 1, x + i] = CYPRESS_BOT_UNDER_TIP[i]
            elif k == "grass":
                self.set(x + i, y - 1, OLIVE_TIP_GRASS[i], self.solid[y - 1, x + i], "tip")
            elif k == "meadow":
                self.set(x + i, y - 1, OLIVE_TIP_TALL[i], self.solid[y - 1, x + i], "tip_tall")

    def cypress(self, x, y):
        if self.kind[y, x] == "olive_bot":
            half = 0 if self.mt[y, x] in (OLIVE_BOT[0], OLIVE_BOT_TIP[0]) else 1
            self.set(x, y, CYPRESS_TOP_OVER_OLIVE[half], True, "cypress_top")
        else:
            self.set(x, y, CYPRESS_TOP, True, "cypress_top")
        self.set(x, y + 1, CYPRESS_BOT, True, "cypress_bot")

    def pine(self, x, y):
        for j in range(2):
            for i in range(2):
                self.set(x + i, y + j, PINE[j][i], True, "pine")

    def free(self, x, y, w=1, h=1, kinds=("grass",)):
        return all(0 <= x + i < W and 0 <= y + j < H and self.kind[y + j, x + i] in kinds
                   and not self.solid[y + j, x + i] for j in range(h) for i in range(w))


# ---------------------------------------------------------------------------
# The plan: ground kinds per cell, before any structure goes on top
#   F forest (2x2 blocks on the border's phase)   g grass   p limestone path
#   s the Sacred Way's slabs   w standing wheat   u stubble   m the poppy meadow
#   r the Rharian field's wheat   B a building's footprint
# ---------------------------------------------------------------------------

# The forest, as 2x2 blocks: block (bx, by) covers x 2bx..2bx+1, y 2by..2by+1, the
# border's phase, so the edge olives run on into the border's. F forest, . open.
FOREST = [
    #  bx: 0123456789012345678901234
    "FFFFFFFFFFFFFFFFFFFFFF..F",   # y 0-1    the Eleutherai road leaves north at x 44-47
    "FFFFFFFFFFFFFFFFFFFFFF..F",   # y 2-3
    "FFFFFFFFFFFFFFFFFFFFFF..F",   # y 4-5
    "FFFFF.............FFFF..F",   # y 6-7    the NW wheat, the sanctuary, the NE grove
    "FFFF..............FFFF..F",   # y 8-9
    "FFFF..............FFFF..F",   # y 10-11
    "FFFFF.............FFFF..F",   # y 12-13
    "FFFF..............FFFF..F",   # y 14-15
    "FFFF.................F..F",   # y 16-17  pomegranates along the grove's foot
    "FFFF.................F..F",   # y 18-19  the house of Keleos
    "FF......................F",   # y 20-21  Krokis's verge at the west gate
    "FF......................F",   # y 22-23
    ".........................",   # y 24-25  the Sacred Way: Route 5 in on the west, Route 15 out east
    ".........................",   # y 26-27
    "FFFF.................FFFF",   # y 28-29  the fields
    "FFF..................FFFF",   # y 30-31
    "FFFF.................FFFF",   # y 32-33
    "FFFF.................FFFF",   # y 34-35
    "FFFF.................FFFF",   # y 36-37
    "FFFFFFFFFFFFFFFFFFFFFFFFF",   # y 38-39
]


def forest_mask():
    m = np.zeros((H, W), bool)
    for by, row in enumerate(FOREST):
        for bx, c in enumerate(row[:25]):
            if c == "F":
                m[2 * by:2 * by + 2, 2 * bx:2 * bx + 2] = True
    return m


def rect(plan, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            plan[y][x] = c


def mask_rows(plan, rows, ox, oy, c):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch == "#":
                plan[oy + j][ox + i] = c


def make_plan():
    fm = forest_mask()
    plan = [["F" if fm[y, x] else "g" for x in range(W)] for y in range(H)]
    # the Sacred Way: aethos path in the seam strips, the slabs between them
    rect(plan, 0, 24, W - 1, 27, "p")
    rect(plan, STRIP_COLS, 24, W - 1 - STRIP_COLS, 26, "s")
    # the Eleutherai road north, and its verge
    rect(plan, 44, 0, 47, 23, "g")
    rect(plan, 45, 0, 46, 23, "p")
    # the sanctuary: its court, and the well-yard before the Propylaia
    rect(plan, 21, 10, 33, 19, "s")
    rect(plan, 30, 9, 33, 9, "s")
    rect(plan, 30, 11, 31, 12, "g")         # a pomegranate's bed in the court
    rect(plan, 21, 21, 29, 23, "s")
    # the granary yard behind the Asclepeion and the Agora, and the lane up to it
    rect(plan, 13, 19, 14, 23, "p")
    rect(plan, 9, 18, 19, 18, "p")
    # the north-west wheat, and a reaped plot beside the granary
    mask_rows(plan, ["..######.....",
                     ".#########...",
                     "###########..",
                     "###########..",
                     ".#########...",
                     "..#####......"], 8, 7, "w")
    mask_rows(plan, ["####.",
                     "#####",
                     "####."], 8, 13, "u")
    # a grass verge between the Sacred Way and the fields
    rect(plan, STRIP_COLS, 27, W - 1 - STRIP_COLS, 27, "g")
    # the lane to the fields, past Euphorion's porch, and on to the Rharian field
    rect(plan, 20, 27, 21, 31, "p")
    rect(plan, 20, 31, 36, 31, "p")
    # the south-west wheat, the big field, round the threshing floor
    mask_rows(plan, ["..#####.....",
                     ".######.....",
                     "#######.....",
                     "########....",
                     "##########..",
                     "##########..",
                     ".#########..",
                     "..#######...",
                     "...####....."], 8, 29, "w")
    # stubble: a reaped strip along the field's west side
    mask_rows(plan, ["###.",
                     "####",
                     "####",
                     "####",
                     "##.."], 8, 32, "u")
    # south of the lane: wheat down to the trees
    mask_rows(plan, ["..######.",
                     ".########",
                     "#########",
                     "#########",
                     ".#######.",
                     "..####..."], 19, 32, "w")
    # the Rharian field: wheat behind Dysaules's fence
    rect(plan, 30, 33, 35, 35, "r")
    # the poppy meadow, east of the farmhouse
    mask_rows(plan, [".####",
                     "#####",
                     "#####",
                     "#####",
                     "#####",
                     ".###.",
                     "..#.."], 37, 29, "m")
    return plan


# ---------------------------------------------------------------------------
# Ground
# ---------------------------------------------------------------------------

def edge_key(n, s, w, e):
    if n and w:
        return "tl"
    if n and e:
        return "tr"
    if s and w:
        return "bl"
    if s and e:
        return "br"
    return "t" if n else "b" if s else "l" if w else "r" if e else "c"


def ground(g, plan):
    def at(x, y):
        if not (0 <= x < W and 0 <= y < H):
            return "#"                      # off the map: the ground runs on
        return plan[y][x]

    for kind, key in (("w", "wheat"), ("u", "stubble"), ("r", "wheat")):
        region = [[plan[y][x] == kind for x in range(W)] for y in range(H)]
        d = g.s[key]
        for y in range(H):
            for x in range(W):
                if plan[y][x] != kind:
                    continue
                k = E.blob_key(region, x, y)
                cx, cy = d["names"][k]
                g.set(x, y, d["ids"][cy][cx], False, {"w": "wheat", "u": "stubble", "r": "rharian"}[kind])
                if kind == "w" and k == "1|11111111" and noise(x, y, 7) < 9:
                    g.put("wheat_poppies", x, y, kind="wheat")
    for y in range(H):
        for x in range(W):
            c = plan[y][x]
            if c == "p":
                # paths fade into grass; against slabs, buildings and the map edge they run on
                soft = "gFwumr"
                n = at(x, y - 1) in soft
                s = at(x, y + 1) in soft
                w = at(x - 1, y) in soft
                e = at(x + 1, y) in soft
                key = "c" if (n and s) or (w and e) else edge_key(n, s, w, e)
                g.set(x, y, PATH[key], False, "path")
            elif c == "s":
                soft = "gFwumr"
                n = at(x, y - 1) in soft
                s = at(x, y + 1) in soft
                w = at(x - 1, y) in soft
                e = at(x + 1, y) in soft
                name = ("N" if n else "S" if s else "") + ("W" if w else "E" if e else "")
                if not name:
                    name = "C_ruts" if y == 25 and noise(x, y, 3) < 55 else "C"
                g.piece("sacred_way", name, x, y, kind="slab")
            elif c == "m":
                g.set(x, y, TALL, False, "meadow")
            elif c == "g":
                g.set(x, y, GRASS, False, "grass")


def forest(g, plan):
    """Olives mostly, with stone pines and pairs of cypresses breaking them up,
    placed top down so each crown tips into the tree above it."""
    blocks = sorted({(x // 2, y // 2) for y in range(H) for x in range(W) if plan[y][x] == "F"},
                    key=lambda b: (b[1], b[0]))
    bset = set(blocks)
    kinds = {}
    for bx, by in blocks:
        buried = all((bx + dx, by + dy) in bset or not (0 <= 2 * (bx + dx) < W and 0 <= 2 * (by + dy) < H)
                     for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        n = noise(bx, by, 11)
        edge = bx == 0 or by == 0 or 2 * bx + 2 >= W or 2 * by + 2 >= H
        if edge and n < 85:
            kinds[(bx, by)] = "olive"
        elif buried and n < 50:
            kinds[(bx, by)] = "olive"
        else:
            kinds[(bx, by)] = "pine" if n < 30 else "cypress" if n < 62 else "olive"
    for (bx, by) in blocks:
        if kinds[(bx, by)] == "pine" and (kinds.get((bx, by + 1)) == "olive" or kinds.get((bx, by - 1)) == "pine"):
            kinds[(bx, by)] = "cypress"
    for (bx, by) in blocks:
        x, y = 2 * bx, 2 * by
        k = kinds[(bx, by)]
        if k == "olive":
            g.olive(x, y)
        elif k == "pine":
            g.pine(x, y)
        else:
            g.cypress(x, y)
            g.cypress(x + 1, y)


# ---------------------------------------------------------------------------
# The places
# ---------------------------------------------------------------------------

# Where things stand (top-left of each piece); the events below refer to these.
TELESTERION = (21, 6)         # 9x7, door at +4,+5
PLOUTONION = (30, 6)          # 4x3, doors at +1,+2 and +2,+2
PROPYLAIA = (22, 16)          # 7x6, walk through the middle column (+3), steps on row +5
KALLICHORON = (31, 21)        # 3x3, the curb at +1,+1
ASCLEPEION = (8, 20)          # 5x4, door +2,+3
AGORA = (15, 20)              # 5x4, door +2,+3
KELEOS = (37, 18)             # gable_tower, 5x6, door +1,+5
GRANARY = (14, 14)            # granary, 4x4, barn doors +1,+3 and +2,+3
EUPHORION = (22, 27)          # porch_house, 4x4, door +2,+3
DYSAULES = (29, 27)           # longhouse, 5x4, barn doors +2,+3 and +3,+3
ALONIA = (15, 28)             # the threshing floor, 4x4 (its middle at +1..+2)
SANCT_W, SANCT_E, SANCT_S = 20, 34, 20   # the sanctuary's walls


def torch(g, x, y):
    """A procession torch, its head at (x, y) and its foot below, on grass or paving."""
    key = "torch_post_path" if g.kind[y + 1, x] == "slab" else "torch_post"
    g.piece(key, "top_cold", x, y)
    g.piece(key, "foot", x, y + 1)


def wall_ew(g, x0, x1, y, kind="wall"):
    for x in range(x0, x1 + 1):
        g.set(x, y, WALL["l"] if x == x0 else WALL["r"] if x == x1 else WALL["run"], True, kind)


def wall_ns(g, x, y0, y1, side, kind="wall"):
    for y in range(y0, y1 + 1):
        g.set(x, y, WALL[side], True, kind)


def sanctuary(g):
    tx, ty = TELESTERION
    g.put("telesterion", tx, ty)
    px, py = PLOUTONION
    g.put("plutonion", px, py)
    # the walls: west and east down to the south wall, which the Propylaia stands in
    wall_ns(g, SANCT_W, 6, SANCT_S - 1, "w")
    wall_ns(g, SANCT_E, 6, SANCT_S - 1, "e")
    ax, ay = PROPYLAIA
    wall_ew(g, SANCT_W, ax - 1, SANCT_S)
    wall_ew(g, ax + 7, SANCT_E, SANCT_S)
    g.put("propylaea", ax, ay)
    # the court: torches on the axis from the gate to the hall, the sanctuary's own
    # grain jars, a shrine of Demeter, Persephone's pomegranates in the grove
    for x in (ax + 1, ax + 5):
        torch(g, x, 13)
    for x in (30, 31, 32, 33):
        g.put("pithos_path", x, 17)
    g.put("pithos_path", 21, 18)
    g.put("pomegranate", 30, 11)
    g.put("grain_shrine_path", 33, 10)
    g.put("sheaf_path", 33, 14)
    g.put("sheaf_path", 21, 14)
    # hedges of cypresses outside the west and east walls
    for y in range(6, 18, 2):
        g.cypress(SANCT_E + 1, y)
    for y in range(6, 14, 2):
        g.cypress(SANCT_W - 1, y)


def village(g):
    # the Asclepeion and the Agora face the Sacred Way at the west gate
    g.put("asclepeion", *ASCLEPEION)
    g.put("agora", *AGORA)
    # the well-yard: the Maiden's Well, its bench, the "fig" (a pomegranate), torches
    g.put("kallichoron", *KALLICHORON)
    kx, ky = KALLICHORON
    g.put("seat_stone", kx + 4, ky + 1)               # the worn bench
    g.put("pomegranate", 35, 18)                      # the dry fig of the well (Persephone's tree stands in)
    for x in (21, 29):
        torch(g, x, 21)
    # the house of Keleos, the oldest in Eleusa, on the well-yard; a pomegranate and
    # a cypress behind its gable
    g.front("gable_tower", *KELEOS)
    g.put("pomegranate", KELEOS[0], KELEOS[1])
    g.cypress(KELEOS[0] + 2, KELEOS[1])
    # pomegranates along the grove's foot
    for x in (36, 38, 40):
        g.put("pomegranate", x, 16)
    # the granary yard: Sitokles's granary by the sanctuary's west wall, the threshing
    # floor's sacks, the oven and the jars
    g.front("granary", *GRANARY)
    gx, gy = GRANARY
    for x in (gx - 1, gx + 4):
        g.put("pithos", x, gy + 2)
    g.put("oven", 18, 14)
    g.put("winnowing", 9, 17)
    g.put("pithos", 12, 16)
    for (x, y) in ((9, 14), (10, 14)):
        g.put("stook", x, y)
    g.put("sheaf_grass", gx + 4, gy + 1)
    # the lane to the fields: Euphorion's porch, Dysaules's long farmhouse
    g.front("porch_house", *EUPHORION)
    g.front("longhouse", *DYSAULES)


def fields(g):
    # the threshing floor at the big field's edge, at threshing time
    ax, ay = ALONIA
    g.put("alonia", ax, ay)
    g.put("alonia_work", ax + 1, ay + 1)
    g.put("winnowing", ax + 1, ay + 4)
    g.put("sheaf_grass", ax + 4, ay + 1)
    # stooks and the reaper's basket on the stubble
    for (x, y) in ((9, 33), (10, 34)):
        g.put("stook", x, y)
    g.put("reaper", 9, 35)
    # Demeter's field shrine at the corner of the wheat
    g.put("grain_shrine", 18, 33)
    # the Rharian field's fence (aethos dry stone), with Dysaules's stele
    wall_ew(g, 29, 36, 32, "fence")
    wall_ew(g, 29, 36, 36, "fence")
    wall_ns(g, 29, 33, 35, "w", "fence")
    wall_ns(g, 36, 33, 35, "e", "fence")
    g.set(28, 32, STELE, True, "sign")
    # beehives in the meadow
    for (x, y) in ((41, 31), (39, 34)):
        g.set(x, y, SKEP, True, "skep")
    # sheaves at the north-west field's margin
    for (x, y) in ((20 - 2, 9), (9, 12)):
        if g.kind[y, x] == "grass":
            g.put("sheaf_grass", x, y)
    # poppies round the meadow and the wheat
    for (x, y) in ((36, 30), (36, 33), (40, 29), (42, 33), (37, 36), (19, 33), (8, 28),
                   (17, 37), (28, 37), (24, 33), (10, 6), (17, 7), (8, 10), (19, 12), (13, 13)):
        if g.kind[y, x] == "grass":
            g.piece("poppies", "scattered" if noise(x, y, 4) < 60 else "dense", x, y, kind="poppies")


def edges(g):
    # the village sign at the west gate, and the road north's stele
    g.set(7, 23, STELE, True, "sign")
    g.set(43, 21, STELE, True, "sign")
    # cypresses stood along the verges, so the forest's face steps forward, and
    # along the Eleutherai road
    for (x, y) in ((6, 22), (8, 28), (44, 4), (47, 7), (44, 11), (47, 15), (44, 18)):
        if g.free(x, y, 1, 2):
            g.cypress(x, y)
    g.set(47, 11, SKEP, True, "boulder")                     # a boulder on the verge
    # procession torches along the Sacred Way's south verge (cold until the night
    # of the Mysteries)
    for x in (11, 17, 27, 35, 40):
        if g.free(x, 27, 1, 2, kinds=("grass", "flowers")):
            torch(g, x, 27)
    # the road of the Mysteries, shut: a wall across it, the hoplite in its gap
    for y in (24, 26, 27):
        g.set(48, y, WALL["w"], True, "wall")
    # anemones in the grass by the roads
    for (x, y) in ((5, 23), (4, 21), (7, 30), (47, 22), (44, 9), (47, 3), (44, 15), (13, 28),
                   (25, 32), (16, 19), (8, 19)):
        if g.kind[y, x] == "grass" and not g.solid[y, x]:
            g.set(x, y, FLOWERS, False, "flowers")


def compose():
    g = Grid()
    plan = make_plan()
    ground(g, plan)
    forest(g, plan)
    sanctuary(g)
    village(g)
    fields(g)
    edges(g)
    return g, plan


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
GFX = "OBJ_EVENT_GFX_ICHOR_"
PX = "EleusaVillage_EventScript_"
PROCESSION = "FLAG_ICHOR_HIDE_PROCESSION_ELEUSA"     # shown from the Harvest Laurel to the Mysteries
# local id, graphics, x, y, facing, script, hide flag[, trainer sight]
OBJECTS = [
    ("KROKIS", GFX + "ELDER_F", 8, 27, "UP", "Krokis", "0"),
    ("WATER_CARRIER", GFX + "WOMAN", 30, 22, "RIGHT", "WaterCarrier", "0"),
    ("KID", GFX + "KID_M", 33, 21, "LEFT", "Kid", "0"),
    ("KOPROS", "OBJ_EVENT_GFX_SPECIES(KAPLET)", 32, 21, "DOWN", "Kopros", "0"),
    ("DYSAULES", GFX + "HARVESTER", 28, 34, "RIGHT", "Dysaules", "0"),
    # a swineherd, optional: he watches the threshing floor (SCRIPT.md Part 3)
    ("EUBOULEUS", GFX + "GOATHERD", 14, 28, "RIGHT", "Eubouleus", "0", 3),
    ("HOPLITE", GFX + "HOPLITE", 48, 25, "LEFT", "Hoplite", "0"),
    # beat 20: Kleon in the square, waiting for the procession (gone once the Mysteries begin)
    ("KLEON", GFX + "KLEON", 24, 23, "DOWN", "Kleon", "FLAG_ICHOR_HIDE_KLEON_ELEUSA"),
    # beat 22: the procession, in the sanctuary's court and the square. Alethea comes up to
    # the Telesterion's steps (25, 12) as the player walks out with the Harvest Laurel, and
    # Kerykos stands on them with his staff. ICHOR_STUB_SPRITE: the initiates are drawn
    # as pilgrims and youths until the Initiate walker exists; Eudemos as an elder.
    ("ALETHEA", GFX + "ALETHEA", 24, 14, "UP", "Alethea", PROCESSION),
    ("KERYKOS", GFX + "KERYKOS", 27, 12, "LEFT", "Kerykos", PROCESSION),
    ("EUDEMOS", GFX + "ELDER_M", 30, 14, "LEFT", "Eudemos", PROCESSION),
    ("INITIATE_1", GFX + "PILGRIM", 22, 14, "UP", "Initiate1", PROCESSION),
    ("INITIATE_2", GFX + "YOUTH_F", 28, 13, "UP", "Initiate2", PROCESSION),
    ("INITIATE_3", GFX + "YOUTH_M", 31, 13, "LEFT", "Initiate3", PROCESSION),
    ("INITIATE_4", GFX + "PILGRIM", 32, 15, "UP", "Initiate4", PROCESSION),
    ("INITIATE_5", GFX + "YOUTH_M", 23, 22, "DOWN", "Initiate5", PROCESSION),
    ("INITIATE_6", GFX + "YOUTH_F", 26, 23, "LEFT", "Initiate6", PROCESSION),
]
# Krokis's gate (beat 19): a coord trigger across the Sacred Way just inside the west
# entrance, two steps short of her stool. It plays once (VAR_TEMP_8 is 1 once the
# saffron thread is tied; the map's ON_TRANSITION sets it from FLAG_ICHOR_SAFFRON_THREAD).
KROKIS_GATE = [(6, y) for y in WEST_SEAM]
ITEMS = [
    ("ITEM_SUPER_POTION", 18, 30, "FLAG_ICHOR_ITEM_ELEUSA_SUPER_POTION"),
    ("ITEM_AWAKENING", 39, 32, "FLAG_ICHOR_ITEM_ELEUSA_AWAKENING"),
]
HIDDEN = [
    ("ITEM_HONEY", 39, 34, "FLAG_ICHOR_HIDDEN_ELEUSA_HONEY"),
    ("ITEM_POMEG_BERRY", 35, 20, "FLAG_ICHOR_HIDDEN_ELEUSA_POMEG_BERRY"),
    # the Bronze Obol: ITEM_RELIC_COPPER stands in, as at Elaia's well
    ("ITEM_RELIC_COPPER", 32, 22, "FLAG_ICHOR_HIDDEN_ELEUSA_BRONZE_OBOL"),
]
# x, y, facing, script
SIGNS = [
    (7, 23, "ANY", "VillageSign"),
    (43, 21, "ANY", "NorthRoadSign"),
    (24, 20, "NORTH", "SanctuarySign"),
    (24, 11, "NORTH", "TempleSign"),
    (30, 8, "NORTH", "PloutonionSign"),
    (28, 32, "ANY", "RharianSign"),
    (35, 22, "ANY", "WellBench"),
    (18, 34, "ANY", "FieldShrine"),             # ICHOR_STUB_RITES: Demeter's field altar
    (41, 31, "ANY", "Beehives"),
]
# The road of the Mysteries is shut in Act I: a hoplite at (47,25) turns the player
# back from the line x = 46. (The story batch opens it in Act II.)
EAST_GUARD_LINE = []
DIG = [(9, 36), (38, 35)]                       # ICHOR_STUB_DIG: the fields' two daily dig spots


def warps(g):
    """(x, y, destination map, its warp id), in warp-id order. Each placeholder
    room's warp 0 is its door mat, so the village doors point at 0, and the rooms
    point back at the first of a door's ids."""
    out = []
    def door(where, w, h, dest):
        x, y = where
        for (dx, dy) in g.doors(x, y, x + w - 1, y + h - 1):
            out.append((dx, dy, dest, 0))
    door(ASCLEPEION, 5, 4, "MAP_ELEUSA_VILLAGE_ASCLEPEION")
    door(AGORA, 5, 4, "MAP_ELEUSA_VILLAGE_AGORA")
    door(KELEOS, 5, 6, "MAP_ELEUSA_VILLAGE_HOUSE_OF_KELEOS")
    door(GRANARY, 4, 4, "MAP_ELEUSA_VILLAGE_GRANARY_HOUSE")
    door(EUPHORION, 4, 4, "MAP_ELEUSA_VILLAGE_POETS_HOUSE")
    door(DYSAULES, 5, 4, "MAP_ELEUSA_VILLAGE_FARMHOUSE")
    door(TELESTERION, 9, 7, "MAP_ELEUSA_VILLAGE_TEMPLE_OF_DEMETER")
    door(PLOUTONION, 4, 3, "MAP_ELEUSA_SANCTUM_B1F")
    return out


def write_events(g):
    m = json.loads((MAP_DIR / "map.json").read_text())
    m["music"] = "MUS_ICHOR_ELEUSA"
    m["weather"] = "WEATHER_SUNNY"
    # Route 5 joins the west edge (its rows 21-24 meet ours 24-27); Routes 6 and
    # 15 (world-act2) add theirs on their own branch. BUILD.md has the seams.
    m["connections"] = [{"map": "MAP_ROUTE5_SKIRONIAN_CLIFFS", "offset": 3, "direction": "left"}]
    objs = []
    for lid, gfx, x, y, facing, script, flag, *sight in OBJECTS:
        objs.append({
            "local_id": f"LOCALID_ELEUSA_{lid}", "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": f"MOVEMENT_TYPE_FACE_{facing}", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL" if sight else "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": str(sight[0]) if sight else "0",
            "script": PX + script, "flag": flag})
    for item, x, y, flag in ITEMS:
        objs.append({
            "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": x, "y": y, "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_LOOK_AROUND", "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": item,
            "script": "Common_EventScript_FindItem", "flag": flag})
    m["object_events"] = objs
    m["warp_events"] = [{"x": x, "y": y, "elevation": 0, "dest_map": d, "dest_warp_id": str(i)}
                        for x, y, d, i in warps(g)]
    m["coord_events"] = [{"type": "trigger", "x": x, "y": y, "elevation": 0, "var": "VAR_TEMP_1",
                          "var_value": "0", "script": PX + "RoadShut"} for x, y in EAST_GUARD_LINE]
    m["coord_events"] += [{"type": "trigger", "x": x, "y": y, "elevation": 0, "var": "VAR_TEMP_8",
                           "var_value": "0", "script": PX + "KrokisGate"} for x, y in KROKIS_GATE]
    bgs = [{"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{f}", "script": PX + s} for x, y, f, s in SIGNS]
    bgs += [{"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
             "script": PX + "DigSpot"} for x, y in DIG]
    bgs += [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag,
             "quantity": 1, "underfoot": False} for item, x, y, flag in HIDDEN]
    m["bg_events"] = bgs
    (MAP_DIR / "map.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


ROOMS = {   # placeholder interiors: their mat warps back to the village
    "MAP_ELEUSA_VILLAGE_ASCLEPEION": "EleusaVillage_Asclepeion",
    "MAP_ELEUSA_VILLAGE_AGORA": "EleusaVillage_Agora",
    "MAP_ELEUSA_VILLAGE_HOUSE_OF_KELEOS": "EleusaVillage_HouseOfKeleos",
    "MAP_ELEUSA_VILLAGE_GRANARY_HOUSE": "EleusaVillage_GranaryHouse",
    "MAP_ELEUSA_VILLAGE_POETS_HOUSE": "EleusaVillage_PoetsHouse",
    "MAP_ELEUSA_VILLAGE_FARMHOUSE": "EleusaVillage_Farmhouse",
    "MAP_ELEUSA_SANCTUM_B1F": "EleusaSanctum_B1F",
}
MAT = [(4, 7), (5, 7)]   # the Fisher's house mat the placeholder rooms copy


def write_room_warps(g):
    """Point each room's way out at its village door (the first, for a double door).
    A room still on the placeholder (no warp back to the village yet) gets the Fisher's
    house mat; a room its own builder has drawn keeps its warps' places, and only their
    destination id is kept in step with the village's door list. The Temple of Demeter's
    own builder writes its stair warps."""
    first = {}
    for i, (x, y, dest, _) in enumerate(warps(g)):
        first.setdefault(dest, i)
    for dest, name in ROOMS.items():
        path = ROOT / "data/maps" / name / "map.json"
        m = json.loads(path.read_text())
        out = [w for w in m.get("warp_events") or [] if w.get("dest_map") == "MAP_ELEUSA_VILLAGE"]
        if out:
            for w in out:
                w["dest_warp_id"] = str(first[dest])
        else:
            m["warp_events"] = (m.get("warp_events") or []) + [
                {"x": x, "y": y, "elevation": 0, "dest_map": "MAP_ELEUSA_VILLAGE",
                 "dest_warp_id": str(first[dest])} for x, y in MAT]
        text = json.dumps(m, indent=2, ensure_ascii=False) + "\n"
        if text != path.read_text():
            path.write_text(text)
    return first


# ---------------------------------------------------------------------------
# The generated script block: the Ploutonion's bronze gate stays shut until
# beat 22 opens the sanctum (its door cells get collision on load).
# ---------------------------------------------------------------------------
SCRIPT_BEGIN = "// --- Generated by tools/ichor/maps/eleusa.py from the layout. Do not edit. ---"
SCRIPT_END = "// --- End of the generated block. ---"


def script_block(g):
    px, py = PLOUTONION
    cells = [(x, y) for (x, y) in g.doors(px, py, px + 3, py + 2)]
    out = [SCRIPT_BEGIN, "",
           "// The Ploutonion's bronze gate: shut (its two door cells block) until",
           "// FLAG_ICHOR_SANCTUM_OPEN (beat 22).",
           f"script {PX}ShutPloutonion {{"]
    for x, y in cells:
        out.append(f"    setmetatile({x}, {y}, 0x{int(g.mt[y, x]):03X}, TRUE)")
    out += ["    return", "}", "", SCRIPT_END]
    return "\n".join(out)


def splice_script(g):
    path = MAP_DIR / "scripts.pory"
    text = path.read_text()
    a, b = text.find(SCRIPT_BEGIN), text.find(SCRIPT_END)
    if a < 0 or b < 0:
        sys.exit(f"eleusa: {path} needs the markers:\n{SCRIPT_BEGIN}\n{SCRIPT_END}")
    new = text[:a] + script_block(g) + text[b + len(SCRIPT_END):]
    if new != text:
        path.write_text(new)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def blockdata(g):
    out = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            out[y, x] = (int(g.mt[y, x]) & 0x3FF) | (int(g.solid[y, x]) << 10) | (3 << 12)
    return out


def border():
    return np.array([OLIVE_TOP[0], OLIVE_TOP[1], OLIVE_BOT_TIP[0], OLIVE_BOT_TIP[1]], np.uint16)


def write_layout(g):
    LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
    blockdata(g).astype("<u2").tofile(LAYOUT_DIR / "map.bin")
    border().astype("<u2").tofile(LAYOUT_DIR / "border.bin")
    path = ROOT / "data/layouts/layouts.json"
    data = json.loads(path.read_text())
    for l in data["layouts"]:
        if l.get("id") == LAYOUT_ID and (l["width"], l["height"], l["secondary_tileset"]) != (W, H, "gTileset_Eleusa"):
            l["width"], l["height"] = W, H
            l["primary_tileset"], l["secondary_tileset"] = "gTileset_Aethos", "gTileset_Eleusa"
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def reach_from(g, start, blocked=frozenset()):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if (0 <= p[0] < W and 0 <= p[1] < H and p not in seen and not g.solid[p[1], p[0]]
                    and p not in blocked):
                seen.add(p)
                q.append(p)
    return seen


def check(g):
    problems = []
    m = json.loads((MAP_DIR / "map.json").read_text())
    start = (0, WEST_SEAM[1])
    people = {(o["x"], o["y"]) for o in m["object_events"]}
    reach = reach_from(g, start)
    # the seams
    for y in range(H):
        if (not g.solid[y, 0]) != (y in WEST_SEAM):
            problems.append(f"west seam: row {y} is {'open' if not g.solid[y, 0] else 'shut'}")
        if (not g.solid[y, W - 1]) != (y in EAST_SEAM):
            problems.append(f"east seam: row {y} is {'open' if not g.solid[y, W - 1] else 'shut'}")
    for x in range(W):
        if (not g.solid[0, x]) != (x in NORTH_SEAM):
            problems.append(f"north seam: column {x} is {'open' if not g.solid[0, x] else 'shut'}")
        if not g.solid[H - 1, x]:
            problems.append(f"south edge: column {x} is open")
    for y in range(H):
        for x in range(W):
            mid = int(g.mt[y, x])
            near = x < STRIP_COLS or x >= W - STRIP_COLS or y < STRIP_ROWS
            if near and mid >= 0x200:
                problems.append(f"Eleusa metatile 0x{mid:03X} at ({x},{y}), inside a seam strip: use aethos there")
    for p in list(NORTH_SEAM):
        if (p, 0) not in reach:
            problems.append(f"the north seam at ({p},0) can't be walked to")
    if (W - 1, EAST_SEAM[1]) not in reach:
        problems.append("the east seam can't be walked to")
    # warps
    for w in m["warp_events"]:
        x, y = w["x"], w["y"]
        if behavior(int(g.mt[y, x])) not in DOOR_BEHAVIORS:
            problems.append(f"warp ({x},{y}) is on {behavior(int(g.mt[y, x]))}, not a door")
        if (x, y + 1) not in reach:
            problems.append(f"warp ({x},{y}): its doorstep ({x},{y + 1}) is unreachable")
    # people and items stand on open ground the player can walk next to
    for o in m["object_events"]:
        x, y = o["x"], o["y"]
        who = o.get("local_id", o["graphics_id"] + f"@{x},{y}")
        if g.solid[y, x]:
            problems.append(f"{who} stands on a solid cell ({x},{y})")
        if (x, y) not in reach:
            problems.append(f"{who} at ({x},{y}) is cut off")
    still = reach_from(g, start, frozenset(people))
    for o in m["object_events"]:
        x, y = o["x"], o["y"]
        if not any((x + dx, y + dy) in still for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
            problems.append(f"{o.get('local_id', o['graphics_id'])} at ({x},{y}) can't be talked to past the others")
    for w in m["warp_events"]:
        if (w["x"], w["y"] + 1) not in still:
            problems.append(f"a person blocks the door ({w['x']},{w['y']})")
    # signs and hidden things are read from a walkable neighbour
    for b in m["bg_events"]:
        x, y = b["x"], b["y"]
        if b["type"] == "sign" and (x, y) in reach and not g.kind[y, x] in ("stubble", "meadow", "grass", "wheat"):
            problems.append(f"sign ({x},{y}) is on walkable ground")
        if not any((x + dx, y + dy) in still for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
            problems.append(f"bg event ({x},{y}) can't be read from anywhere")
    # no walkable pocket is cut off from the gate (the fenced Rharian field aside)
    pockets = [(x, y) for y in range(H) for x in range(W)
               if not g.solid[y, x] and (x, y) not in reach and g.kind[y, x] != "rharian"]
    if pockets:
        problems.append(f"walkable but cut off from the gate: {pockets[:12]}{' …' if len(pockets) > 12 else ''}")
    # every building's door must be reachable, and the doors are what map.json says
    if len(m["warp_events"]) != len(warps(g)):
        problems.append("map.json's warps differ from the layout's doors")
    # Krokis's gate spans the whole road in from Route 5, on open ground
    for (x, y) in KROKIS_GATE:
        if g.solid[y, x] or (x, y) not in reach:
            problems.append(f"Krokis's gate trigger ({x},{y}) isn't on the open road")
    if {y for _, y in KROKIS_GATE} != set(WEST_SEAM):
        problems.append("Krokis's gate doesn't span every row of the west road")
    return problems, reach


def walk_text(g, reach):
    rows = ["    " + "".join(str(x % 10) for x in range(W))]
    for y in range(H):
        rows.append(f"{y:3d} " + "".join("#" if g.solid[y, x] else "." if (x, y) in reach else "?"
                                         for x in range(W)))
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------

def renderer():
    import render_map as R
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    return R, R.Renderer(R.Tileset(R.resolve_tileset("aethos", syms)),
                         R.Tileset(R.resolve_tileset("gTileset_Eleusa", syms)))


FRAME = {"DOWN": 0, "UP": 1, "LEFT": 2, "RIGHT": 2}


def sprite(gfx, facing):
    from PIL import Image
    if gfx.startswith("OBJ_EVENT_GFX_SPECIES("):
        name = gfx[len("OBJ_EVENT_GFX_SPECIES("):-1]
        stub = (ROOT / "include/constants/ichor_species_stubs.h").read_text()
        mm = re.search(rf"SPECIES_{name}\s+SPECIES_(\w+)", stub)
        sp = (mm.group(1) if mm else name).lower()
        sheet = Image.open(ROOT / f"graphics/pokemon/{sp}/overworld.png")
        fw = sheet.height
        frame = {"DOWN": 0, "UP": 1, "LEFT": 2, "RIGHT": 2}[facing]
    elif gfx == "OBJ_EVENT_GFX_ITEM_BALL":
        p = ROOT / "graphics/object_events/pics/misc/item_ball.png"
        sheet = Image.open(p)
        fw, frame = 16, 0
    else:
        sheet = Image.open(ROOT / f"graphics/object_events/pics/people/ichor/{gfx[len(GFX):].lower()}.png")
        fw = 16
        frame = FRAME[facing]
    fh = sheet.height
    crop = sheet.crop((frame * fw, 0, frame * fw + fw, fh))
    spr = crop.convert("RGBA")
    if sheet.mode == "P":
        idx = crop.load()
        px = spr.load()
        for j in range(fh):
            for i in range(fw):
                if idx[i, j] == 0:
                    px[i, j] = (0, 0, 0, 0)
    if facing == "RIGHT":
        spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    return spr, fw, fh


def people(im, pad=0, everyone=False):
    for lid, gfx, x, y, facing, script, flag, *_ in OBJECTS:
        if flag != "0" and not everyone:
            continue                 # the story cast comes and goes; the renders show the everyday village
        try:
            spr, fw, fh = sprite(gfx, facing)
        except FileNotFoundError:
            continue
        im.paste(spr, ((x + pad) * 16 + 8 - fw // 2, (y + pad) * 16 + 16 - fh), spr)
    for item, x, y, flag in ITEMS:
        try:
            spr, fw, fh = sprite("OBJ_EVENT_GFX_ITEM_BALL", "DOWN")
            im.paste(spr, ((x + pad) * 16, (y + pad) * 16 + 16 - fh), spr)
        except FileNotFoundError:
            pass
    return im


# Where the player stands for each 15x10 review view, along the route.
VIEWS = [
    ("01_west_gate", 3, 25), ("02_asclepeion", 11, 25), ("03_well_yard", 26, 24),
    ("04_propylaia", 25, 18), ("05_court", 25, 13), ("06_ploutonion", 31, 11),
    ("07_granary_yard", 13, 17), ("08_nw_wheat", 12, 10), ("09_lane_fields", 21, 30),
    ("10_threshing", 13, 32), ("11_rharian", 30, 33), ("12_meadow", 39, 32),
    ("13_east_gate", 45, 25), ("14_north_road", 45, 9), ("15_keleos", 37, 25),
]


def render(out_dir):
    from PIL import Image, ImageDraw
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    R, r = renderer()
    blocks = np.fromfile(LAYOUT_DIR / "map.bin", "<u2")
    flat = R.render_blocks(r, blocks, W)
    whole = people(flat.convert("RGBA"))
    whole.convert("RGB").resize((W * 32, H * 32), Image.NEAREST).save(out_dir / "eleusa_village.png")
    # collision overlay with events
    m = json.loads((MAP_DIR / "map.json").read_text())
    im = flat.convert("RGBA").resize((W * 32, H * 32), Image.NEAREST)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    c = 32
    for y in range(H):
        for x in range(W):
            if blocks[y * W + x] >> 10 & 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 70))
            elif behavior(int(blocks[y * W + x]) & 0x3FF) == "MB_TALL_GRASS":
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 255, 0, 40))
    for o in m["object_events"]:
        d.ellipse([o["x"] * c + 4, o["y"] * c + 4, o["x"] * c + c - 5, o["y"] * c + c - 5], outline=(255, 255, 0, 255), width=3)
    for w_ in m["warp_events"]:
        d.rectangle([w_["x"] * c + 3, w_["y"] * c + 3, w_["x"] * c + c - 4, w_["y"] * c + c - 4], outline=(0, 255, 255, 255), width=3)
    for b in m["bg_events"]:
        col = (255, 120, 255, 255) if b["type"] == "hidden_item" else (255, 255, 255, 255)
        d.line([b["x"] * c + 4, b["y"] * c + 4, b["x"] * c + c - 5, b["y"] * c + c - 5], fill=col, width=3)
        d.line([b["x"] * c + c - 5, b["y"] * c + 4, b["x"] * c + 4, b["y"] * c + c - 5], fill=col, width=3)
    Image.alpha_composite(im, ov).convert("RGB").save(out_dir / "eleusa_village_walk.png")
    # GBA screen views, with the border past the edges
    pad = 8
    bw, bh = W + 2 * pad, H + 2 * pad
    bord = border()
    big = np.zeros((bh, bw), np.uint16)
    for y in range(bh):
        for x in range(bw):
            big[y, x] = bord[((x - pad) % 2) + 2 * ((y - pad) % 2)]
    big[pad:pad + H, pad:pad + W] = blocks.reshape(H, W)
    padded = people(R.render_blocks(r, big.reshape(-1), bw).convert("RGBA"), pad).convert("RGB")
    views = []
    for name, px, py in VIEWS:
        x0, y0 = (px - 7 + pad) * 16, (py - 4 + pad) * 16 - 8
        v = padded.crop((x0, y0, x0 + 240, y0 + 160))
        v.resize((480, 320), Image.NEAREST).save(out_dir / f"view_{name}.png")
        views.append((name, v))
    cols = 3
    rows = (len(views) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 248 + 8, rows * 178 + 8), (24, 24, 32))
    sd = ImageDraw.Draw(sheet)
    for i, (name, v) in enumerate(views):
        x, y = 8 + (i % cols) * 248, 8 + (i // cols) * 178
        sheet.paste(v, (x, y + 10))
        sd.text((x, y - 2), name, fill=(230, 230, 200))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out_dir / "eleusa_views.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--walk", action="store_true")
    args = ap.parse_args()
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run /usr/bin/python3 tools/ichor/art/eleusa_build.py --no-compile first")
    g, plan = compose()
    write_layout(g)
    write_events(g)
    write_room_warps(g)
    splice_script(g)
    problems, reach = check(g)
    if args.walk:
        print(walk_text(g, reach))
    if args.render:
        render(args.render)
    for p in problems:
        print("PROBLEM:", p)
    print(f"eleusa: {W}x{H}, {len(warps(g))} door warps, {len(OBJECTS)} people, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
