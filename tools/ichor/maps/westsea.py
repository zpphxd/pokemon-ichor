#!/usr/bin/env python3
"""Build Route 33, the western sea (post-game, batch 1): layout, border, events,
and Halia's hut.

Route 33 runs west from Cape Tainaron along the Mani's foot, round the corner,
and north up the Ionian side to Ithaka and Kerkyra (design/AETHOS_MAP.md: cells
(8,14) to (2,4)). It is one 64x80 map on gTileset_Aethos + gTileset_Westsea:

  - the south leg (rows 48-79): Tainaron's cape at the east edge, its landing
    and sea cave; a reef fence across the leg at x = 40 with two gaps, each
    watched by a diver, and the westward current's run through it closed by
    loose rock until the bronze ram breaks it (then the current is a fast lane
    from the cape to the fog); west of the fence the current splits the leg in
    two (a wall north-south): the corner's lane north, and the wreck's lane
    south; the cove behind more loose rock; Kymon becalmed on his raft;
  - the corner (rows 40-56): Halia's islet with her hut, jetty and nets (Route
    33's own landing for the ship), Poseidon's altar on its stack, and the fog
    bank toward the Pillars and Atlantis in the south-west (Labor 10 opens it);
  - the north leg (rows 0-39): the Echinades, a reef across the strait whose
    one gap is a whirlpool Triton's Conch calms; past it a southward current
    splits the basin; Ithaka with Phorkys's cove, the birds' rock, the lagoon
    behind a second whirlpool, and Kerkyra's harbor with the stone ship at its
    mouth.

The ground plan is drawn below with shape helpers, then auto-tiled: rock
coasts and shoals take one of westsea's thirteen shapes by their neighbours;
islands take aethos's sand edges, sand-into-grass rims, olives, cypresses and
pines. Set pieces go on top in code. westsea_review.py checks and renders it;
westsea_hut.py builds Halia's hut.

Writes data/layouts/Route33_WesternSea/{map,border}.bin, its layouts.json
entry and data/maps/Route33_WesternSea/map.json (events and header).

Westsea ids come from build/westsea/catalog.json; make it with
  /usr/bin/python3 tools/ichor/art/westsea_build.py

Usage: /usr/bin/python3 tools/ichor/maps/westsea.py [--render DIR] [--no-check] [--plan]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/westsea/catalog.json"
LAYOUTS = ROOT / "data/layouts/layouts.json"
NAME = "Route33_WesternSea"
LAYOUT_ID = "LAYOUT_ROUTE33_WESTERN_SEA"
W, H = 64, 80

# ---------------------------------------------------------------------------
# aethos ids (design/phase1/TILES_aethos.md)
# ---------------------------------------------------------------------------
SEA = 0x170
GRASS = 0x001
FLOWERS = 0x004
OLIVE_TOP = (0x1D4, 0x1D5)
OLIVE_BOT = (0x1E4, 0x1E5)
OLIVE_BOT_TIP = (0x1DC, 0x1DD)
OLIVE_TIP_GRASS = (0x1CE, 0x1CF)
CYPRESS_TOP = 0x00E
CYPRESS_BOT = 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))
SAND = {"tl": 0x11B, "t": 0x11C, "tr": 0x11D, "l": 0x123, "c": 0x124, "r": 0x125,
        "bl": 0x12B, "b": 0x12C, "br": 0x12D,
        "in_nw": 0x13D, "in_ne": 0x13E, "in_sw": 0x145, "in_se": 0x146}
SAND_GRASS = {"tl": 0x118, "t": 0x119, "tr": 0x11A, "l": 0x120, "c": 0x121, "r": 0x122,
              "bl": 0x128, "b": 0x129, "br": 0x12A}

SURF_BEHAVIORS = {"MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER",
                  "MB_SOOTOPOLIS_DEEP_WATER", "MB_EASTWARD_CURRENT", "MB_WESTWARD_CURRENT",
                  "MB_NORTHWARD_CURRENT", "MB_SOUTHWARD_CURRENT"}
CURRENTS = {"MB_EASTWARD_CURRENT": (1, 0), "MB_WESTWARD_CURRENT": (-1, 0),
            "MB_NORTHWARD_CURRENT": (0, -1), "MB_SOUTHWARD_CURRENT": (0, 1)}
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
WESTSEA_ATTR = np.fromfile(ROOT / "data/tilesets/secondary/westsea/porytiles_bin/metatile_attributes.bin", "<u2")


def behavior(mid):
    a = AETHOS_ATTR[mid] if mid < 0x200 else WESTSEA_ATTR[mid - 0x200]
    return MB.get(int(a) & 0xFF, "?")


def hashed(x, y, salt=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) % 1000 / 1000


def interp(points, t):
    ks = sorted(points)
    if t <= ks[0]:
        return points[ks[0]]
    if t >= ks[-1]:
        return points[ks[-1]]
    for a, b in zip(ks, ks[1:]):
        if a <= t <= b:
            return points[a] + (points[b] - points[a]) * (t - a) / (b - a)


# ---------------------------------------------------------------------------
# Where things are (cells). The plan, the pieces, the events and the checks read these.
# ---------------------------------------------------------------------------
WHIRL_ECHINADES = (14, 38)        # 2x2, the Echinades' gap, in the reef's two rows
WHIRL_LAGOON = (33, 11)           # 2x2, the lagoon's mouth
LAGOON = (38, 12)
COVE = (42, 48)
ROCKS_COVE = [(42, 51), (43, 51)]
BARRIER_X = 40                    # the reef fence across the south leg
GAPS = {"north": (56, 57), "south": (76, 77)}
CURRENT_ROWS = (66, 67)
ROCKS_CURRENT = [(BARRIER_X, 66), (BARRIER_X, 67)]
WRECK = (29, 74)                  # 4x3
STONE_SHIP = (10, 5)              # 5x2, off the mouth of Kerkyra's harbor
BIRDS_ROCK = (26, 15)             # 2x2
ALTAR = (5, 41)                   # 2x3
ISLET = (11, 41)                  # Halia's islet's plan origin
HUT = (13, 42)                    # 3x3, door at (14, 44)
HUT_DOOR = (HUT[0] + 1, HUT[1] + 2)
JETTY = [(20, 47), (21, 47), (22, 47)]
RAFT_AT_SEA = (47, 57)            # 2x1; Kymon on the left cell
RAFT_HOME = (21, 48)              # 2x1, moored below the jetty
RAFT_GLAUKON = (51, 63)
PHORKYS_OLIVE = (2, 25)           # 2x2, at the head of Phorkys's cove on Ithaka
FOG_EDGE = 10                     # the fog bank's wall runs x < FOG_EDGE
FOG_GATE = [(FOG_EDGE, 66), (FOG_EDGE, 67)]
FOG_ON_X, FOG_OFF_X = 13, 15
CAVE = (60, 69)                   # Tainaron's sea cave, in the cape's south face
STELE = (18, 44)                  # the route's stele on Halia's islet

# Rock islets (westsea's crag pieces): (piece, x, y). Each is solid all over.
ISLETS = [
    # the north basin
    ("islet_b", 16, 2), ("islet_d", 26, 27), ("islet_b", 13, 18), ("islet_a", 10, 30),
    ("islet_d", 23, 21),
    # the Echinades, strung along the reef (Ovid's nymphs who forgot the river)
    ("islet_b", 3, 37), ("islet_d", 8, 38), ("islet_b", 19, 37), ("islet_d", 24, 38),
    ("islet_b", 28, 37),
    # the corner and the south leg
    ("islet_c", 23, 52), ("islet_a", 44, 59), ("islet_b", 33, 58), ("islet_c", 23, 60),
    ("islet_b", 50, 70), ("islet_a", 19, 72), ("islet_d", 40, 72), ("islet_d", 40, 61),
]

LANDINGS = {
    # name: (water tile, port id for EventScript_IchorLand, what's there)
    "TAINARON": ((57, 66), "VOYAGE_CAPE_TAINARON", "Cape Tainaron"),
    "ITHAKA": ((5, 25), "VOYAGE_ITHAKA", "Ithaka"),
    "KERKYRA": ((4, 4), "VOYAGE_KERKYRA", "Kerkyra"),
    "ROUTE33": ((23, 47), "VOYAGE_ROUTE33", "Halia's jetty"),
}
# A mooring post beside each landing that has no jetty
POSTS = [(57, 65), (6, 26), (5, 5)]

# ---------------------------------------------------------------------------
# The ground plan
# ---------------------------------------------------------------------------
#   ~ open sea     : shoal (lighter water over sand)     # rock: coast and islets
#   s sand         g grass         T woods on grass (olives, pines, cypresses)
#   J jetty        > < ^ v  currents (east, west, north, south)
#   R reef awash   F fog bank (a wall)    f fog (passable mist)
#   @ a set piece's cells (placed in code; sea under it)

# The mainland: land is x >= WEST_COAST(y) and y <= SOUTH_COAST(x).
WEST_COAST = {0: 30, 3: 29, 6: 31, 9: 33, 15: 33, 18: 31, 22: 30, 25: 28, 28: 29, 31: 31, 35: 32,
              40: 33, 45: 31, 50: 30, 53: 31}
SOUTH_COAST = {28: 55, 31: 53, 34: 52, 37: 51, 40: 51, 45: 51, 49: 49, 53: 48, 55: 49, 56: 55,
               57: 61, 58: 65, 59: 67, 60: 69, 63: 68}


class Plan:
    def __init__(self):
        self.c = [["~"] * W for _ in range(H)]
        self.keep = set()              # cells smoothing must not touch

    def get(self, x, y, out="~"):
        return self.c[y][x] if 0 <= x < W and 0 <= y < H else out

    def set(self, x, y, ch):
        if 0 <= x < W and 0 <= y < H:
            self.c[y][x] = ch

    def rect(self, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, ch)

    def ellipse(self, cx, cy, rx, ry, ch, only=None):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x - cx) / (rx + 0.01)) ** 2 + ((y - cy) / (ry + 0.01)) ** 2 <= 1.0:
                    if only is None or self.get(x, y) in only:
                        self.set(x, y, ch)

    def rows(self, x0, y0, rows):
        """Paint ASCII rows at (x0, y0); spaces leave the plan alone."""
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch != " ":
                    self.set(x0 + i, y0 + j, ch)

    def text(self):
        return "\n".join(f"{y:2d} " + "".join(r) for y, r in enumerate(self.c))


def mainland(p):
    for y in range(H):
        xw = round(interp(WEST_COAST, y)) + (1 if hashed(0, y // 2, 3) < 0.3 else 0)
        for x in range(26, W):
            ys = round(interp(SOUTH_COAST, x)) - (1 if hashed(x // 2, 0, 4) < 0.3 and x < 55 else 0)
            if x >= xw and y <= ys:
                p.set(x, y, "#")


SIZES = {"islet_a": (3, 2), "islet_b": (2, 2), "islet_c": (3, 3), "islet_d": (2, 1)}


def mark_islets(p, islets):
    for (key, x, y) in islets:
        w, h = SIZES[key]
        p.rect(x, y, x + w - 1, y + h - 1, "@")


def compose_plan():
    p = Plan()
    mainland(p)

    # ---- the north lagoon: a bay in the mainland, its mouth a whirlpool ----------
    lx, ly = LAGOON
    p.ellipse(lx, ly, 2.4, 2.0, "~")
    p.ellipse(lx + 0.4, ly + 0.2, 1.2, 0.9, ":")
    wx, wy = WHIRL_LAGOON
    p.rect(wx - 2, wy, lx - 2, wy + 1, "~")       # the channel in
    p.rect(wx, wy, wx + 1, wy + 1, "@")

    # ---- the cove behind the loose rock, in the south coast -----------------------
    cx, cy = COVE
    p.ellipse(cx + 0.5, cy, 1.8, 1.5, "~")
    p.rect(cx, cy + 1, cx + 1, ROCKS_COVE[0][1] + 1, "~")
    for (x, y) in ROCKS_COVE:
        p.set(x, y, "@")

    # ---- Kerkyra: green, its harbor a sandy bay on the east side ----------------
    p.rows(0, 0, [
        "TTTTggTss",
        "TTTggggss",
        "TTTgggss~",
        "TTggss~~~",
        "TTgs~~~~~",
        "TTggs~~~~",
        "TTTggss~~",
        "TTTTggss~",
        "TTTgggs~~",
        "TTggggss~",
        "TTTgggs~~",
        "TTgggss~~",
        "Tggsss~~~",
        "gsss~~~~~",
        "ss~~~~~~~",
    ])
    # ---- Ithaka: Phorkys's cove opens east, an olive at its head -------------------
    p.rows(0, 18, [
        "ss~~~~~~",
        "Tss~~~~~",
        "TTgs~~~~",
        "TTTgs~~~",
        "TTTggs~~",
        "TTTggss~",
        "TTggss~~",
        "TTggs~~~",
        "TTggs~~~",
        "TTTggss~",
        "TTTTgss~",
        "TTTggss~",
        "TTggss~~",
        "TTTgs~~~",
        "Tgss~~~~",
        "gss~~~~~",
        "ss~~~~~~",
    ])

    # ---- the Echinades: a reef across the strait, its gap the whirlpool ------------
    wx, wy = WHIRL_ECHINADES
    for x in range(0, 34):
        if p.get(x, 38) == "#":
            break
        if x in (wx, wx + 1):
            continue
        y = 38 + (1 if hashed(x, 38, 9) < 0.3 else 0)
        p.set(x, y, "R")
        if hashed(x, 39, 2) < 0.35:
            p.set(x, 77 - y, "R")
    p.rect(wx, wy, wx + 1, wy + 1, "@")
    for y in (wy, wy + 1):                         # the gap's walls: no way round the whirlpool
        p.set(wx - 1, y, "R")
        p.set(wx + 2, y, "R")
    mark_islets(p, [i for i in ISLETS if 35 <= i[2] <= 40])
    for y in range(35, 42):
        for x in range(0, 34):
            if p.get(x, y) == "~" and any(p.get(x + dx, y + dy) in "R#@" for dx in (-1, 0, 1)
                                          for dy in (-1, 0, 1)) and hashed(x, y, 5) < 0.75:
                p.set(x, y, ":")

    # ---- the north basin: a southward current down its middle ----------------------
    for y in range(5, 32):
        p.set(20, y, "v")
        p.set(21, y, "v")

    # ---- the birds' rock and its shoal, east of the current -----------------------
    bx, by = BIRDS_ROCK
    p.ellipse(bx + 1, by + 1, 3.5, 2.6, ":", only="~")
    p.rect(bx, by, bx + 1, by + 1, "@")
    # ---- rock islets in the north basin, a shoal round the larger ones --------------
    for (key, x, y) in ISLETS:
        if y < 35 and key == "islet_a":
            w, h = SIZES[key]
            p.ellipse(x + w / 2 - 0.5, y + h / 2 - 0.5, w / 2 + 1.6, h / 2 + 1.3, ":", only="~")
    mark_islets(p, [i for i in ISLETS if i[2] < 35])

    # ---- Halia's islet ---------------------------------------------------------------
    p.ellipse(16.5, 46, 8, 6.2, ":", only="~")
    p.rows(ISLET[0], ISLET[1], [
        "  sss       ",
        " sgggss     ",
        "sggggggs    ",
        "sgggggggs   ",
        "sgggggggs   ",
        "sggggggsss  ",
        "ssggggsssJJJ",
        " sssssssss  ",
        " ssssssss   ",
        "  ssssss    ",
        "   sss      ",
    ])
    # ---- Poseidon's stack, west of the islet ----------------------------------------
    p.rect(ALTAR[0], ALTAR[1], ALTAR[0] + 1, ALTAR[1] + 2, "@")
    # ---- the corner: a broad rock islet off the mainland's foot ---------------------
    p.ellipse(24.5, 53, 3.6, 2.6, ":", only="~")

    # ---- the south leg: the reef fence across it, at x = BARRIER_X --------------------
    for y in range(44, H):
        if p.get(BARRIER_X, y) == "#" or y in GAPS["north"] + GAPS["south"] + CURRENT_ROWS:
            continue
        jog = hashed(BARRIER_X, y, 17) < 0.3 and y not in (55, 58, 65, 68, 75, 78)
        p.set(BARRIER_X + (1 if jog else 0), y, "R")
    # the westward current: from the cape's lee to the fog bank's approach
    for x in range(17, 56):
        for y in CURRENT_ROWS:
            if p.get(x, y) == "~":
                p.set(x, y, "<")
    for (x, y) in ROCKS_CURRENT:
        p.set(x, y, "@")
    for (x, y) in POSTS:
        p.set(x, y, "@")
    # its eddy: a pocket on the north side, where an amphora turns
    p.ellipse(16, 64.5, 1.6, 1.3, ":", only="~")
    # the wreck on her shoal, a sandbar, rock islets along the lanes
    wx, wy = WRECK
    p.ellipse(wx + 2, wy + 1, 6.2, 3.6, ":", only="~")
    p.rect(wx, wy, wx + 3, wy + 2, "@")
    p.ellipse(50, 76.5, 3.6, 2.2, ":", only="~")
    p.rows(48, 76, [" ss ", "ssss"])
    for (key, x, y) in ISLETS:
        if y > 50 and key == "islet_c":
            w, h = SIZES[key]
            p.ellipse(x + w / 2 - 0.5, y + h / 2 - 0.5, w / 2 + 1.5, h / 2 + 1.2, ":", only="~")
    mark_islets(p, [i for i in ISLETS if i[2] > 50])
    # Glaukon's raft, Kymon's raft
    p.rect(RAFT_GLAUKON[0], RAFT_GLAUKON[1], RAFT_GLAUKON[0] + 1, RAFT_GLAUKON[1], "@")
    p.rect(RAFT_AT_SEA[0], RAFT_AT_SEA[1], RAFT_AT_SEA[0] + 1, RAFT_AT_SEA[1], "@")

    # ---- the fog bank toward the Pillars (south-west) -----------------------------------
    for y in range(55, H):
        edge = FOG_EDGE - (1 if hashed(0, y, 13) < 0.35 else 0)
        for x in range(0, edge):
            p.set(x, y, "F")
        for x in range(edge, FOG_EDGE + 1):
            p.set(x, y, "f")
    for y in (FOG_GATE[0][1], FOG_GATE[1][1]):
        for x in range(0, FOG_EDGE + 1):
            p.set(x, y, "f")                         # the way through, kept open; objects close it
    # inshore shoals along the mainland's feet
    for (cx, cy, rx, ry) in ((47, 53, 4.5, 1.8), (35, 55.5, 3.5, 1.6), (30.5, 25.5, 1.6, 3),
                             (31.5, 4, 1.6, 2.5), (52, 57, 2.4, 3)):
        p.ellipse(cx, cy, rx, ry, ":", only="~")
    return p


# ---------------------------------------------------------------------------
# Auto-tiling
# ---------------------------------------------------------------------------

def shape_of(inside):
    """inside(dx, dy) -> bool. The canonical shape, or None if the cell's
    neighbourhood isn't one of the thirteen."""
    n, s, w, e = (not inside(0, -1)), (not inside(0, 1)), (not inside(-1, 0)), (not inside(1, 0))
    nw, ne, sw, se = (not inside(-1, -1)), (not inside(1, -1)), (not inside(-1, 1)), (not inside(1, 1))
    if (n and s) or (w and e):
        return None
    if n or s or w or e:
        key = ("t" if n else "b" if s else "") + ("l" if w else "r" if e else "")
        need = {"t": (sw, se), "b": (nw, ne), "l": (ne, se), "r": (nw, sw),
                "tl": (se,), "tr": (sw,), "bl": (ne,), "br": (nw,)}[key]
        return None if any(need) else key
    diag = [d for d, v in (("in_nw", nw), ("in_ne", ne), ("in_sw", sw), ("in_se", se)) if v]
    if not diag:
        return "c"
    return diag[0] if len(diag) == 1 else None


def smooth_rock(p, rounds=8):
    """Make every rock cell one of the thirteen shapes. A cell one wide (water
    on opposite sides) turns to sea; a notch of sea that leaves a neighbour
    without a shape (a stray diagonal) is filled with rock. The map's edge
    counts as rock: the mainland runs on past it."""
    def inside(x, y):
        if not (0 <= x < W and 0 <= y < H):
            return True
        return p.c[y][x] == "#"
    for _ in range(rounds):
        changed = False
        for y in range(H):
            for x in range(W):
                if p.c[y][x] != "#":
                    continue
                f = lambda dx, dy: inside(x + dx, y + dy)
                if shape_of(f) is not None:
                    continue
                thin = (not f(0, -1) and not f(0, 1)) or (not f(-1, 0) and not f(1, 0))
                if thin:
                    p.c[y][x] = "~"
                else:
                    for dy in (-1, 1):
                        for dx in (-1, 1):
                            if not f(dx, dy) and p.get(x + dx, y + dy) in "~:":
                                p.c[y + dy][x + dx] = "#"
                changed = True
        if not changed:
            return
    bad = [(x, y) for y in range(H) for x in range(W) if p.c[y][x] == "#"
           and shape_of(lambda dx, dy: inside(x + dx, y + dy)) is None]
    if bad:
        sys.exit(f"westsea: rock cells still out of shape: {bad[:12]}")


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


class Grid:
    def __init__(self, plan, cat):
        self.p = plan
        self.cat = cat
        self.mid = np.full((H, W), SEA, np.uint16)
        self.solid = np.zeros((H, W), bool)
        self.landish = np.zeros((H, W), bool)        # land: elevation 3, walkable unless solid

    def k(self, key, cx=0, cy=0):
        return self.cat[key]["ids"][cy][cx]

    def set(self, x, y, mid, solid=False, land=None):
        if 0 <= x < W and 0 <= y < H:
            self.mid[y, x] = mid
            self.solid[y, x] = solid
            if land is not None:
                self.landish[y, x] = land

    def put(self, key, x, y, solid=None, land=None):
        """Place a westsea piece; collision from its walk grid (X), unless given."""
        s = self.cat[key]
        for j in range(s["h"]):
            for i in range(s["w"]):
                walk = s["walk"][j][i]
                self.set(x + i, y + j, s["ids"][j][i], walk == "X" if solid is None else solid, land)


def tile(plan, cat):
    g = Grid(plan, cat)
    P = plan.c
    LAND = "sgTJ"

    def at(x, y, out):
        return P[y][x] if 0 <= x < W and 0 <= y < H else out

    for y in range(H):
        for x in range(W):
            ch = P[y][x]
            if ch == "#":
                sh = shape_of(lambda dx, dy: at(x + dx, y + dy, "#") == "#")
                key = "rock_" + sh
                if sh == "c":
                    key += {(0, 0): "", (1, 0): "_10", (0, 1): "_01", (1, 1): "_11"}[(x % 2, y % 2)]
                elif sh in ("t", "b") and x % 2:
                    key += "_10"
                elif sh in ("l", "r") and y % 2:
                    key += "_01"
                g.set(x, y, g.k(key), True)
            elif ch == ":":
                # a shoal runs right up to anything that isn't open sea
                sh = shape_of(lambda dx, dy: at(x + dx, y + dy, "~") not in "~<>^vFf") or "c"
                key = "shoal_" + sh
                if sh == "c":
                    key += {(0, 0): "", (1, 0): "_10", (0, 1): "_01", (1, 1): "_11"}[(x % 2, y % 2)]
                g.set(x, y, g.k(key))
            elif ch in "<>^v":
                d = {">": "e", "<": "w", "^": "n", "v": "s"}[ch]
                g.set(x, y, g.k(f"current_{d}{'a' if hashed(x, y, 23) < 0.7 else 'b'}"))
            elif ch == "R":
                # in a shoal, the reef keeps the shoal's water; in open sea, the sea's
                shoaly = any(at(x + dx, y + dy, "~") == ":" for dx in (-1, 0, 1) for dy in (-1, 0, 1))
                v = "abc"[int(hashed(x, y, 21) * 3)]
                g.set(x, y, g.k(("reef_" if shoaly else "reefs_") + v), True)
            elif ch == "F":
                g.set(x, y, g.k(f"fog_core_{x % 2}{y % 2}"), True)
            elif ch == "f":
                if at(x - 1, y, "~") == "F":
                    g.set(x, y, g.k(f"fog_edge_{y % 2}"))
                else:
                    g.set(x, y, g.k(f"fog_lane_{x % 2}"))
            elif ch in "sgT":
                water = [at(x + dx, y + dy, ch) not in LAND for dx, dy in
                         ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1))]
                key = edge_key(*water)
                if key != "c":
                    g.set(x, y, SAND[key], land=True)
                elif ch == "s":
                    grassy = [at(x + dx, y + dy, "s") in "gT" for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0))]
                    soft = edge_key(*grassy, False, False, False, False)
                    g.set(x, y, SAND_GRASS[soft] if soft != "c" else SAND["c"], land=True)
                else:
                    g.set(x, y, GRASS, land=True)
            elif ch == "J":
                g.set(x, y, SEA, land=True)
    # aethos's half-water sand edges are water (surfable), not land
    for y in range(H):
        for x in range(W):
            if g.landish[y, x] and behavior(int(g.mid[y, x])) in SURF_BEHAVIORS and P[y][x] != "J":
                g.landish[y, x] = False
    return g


# ---------------------------------------------------------------------------
# Woods on the islands
# ---------------------------------------------------------------------------

def free_grass(g, x, y, w=1, h=1):
    return all(0 <= x + i < W and 0 <= y + j < H and g.mid[y + j, x + i] == GRASS
               and not g.solid[y + j, x + i] and g.p.c[y + j][x + i] == "T"
               for j in range(h) for i in range(w))


def olive(g, x, y):
    below = y + 2 < H and g.mid[y + 2, x] == OLIVE_TOP[0]
    for i, m in enumerate(OLIVE_TOP):
        g.set(x + i, y, m, True)
    for i, m in enumerate(OLIVE_BOT_TIP if below else OLIVE_BOT):
        g.set(x + i, y + 1, m, True)
    if y > 0:
        above = (int(g.mid[y - 1, x]), int(g.mid[y - 1, x + 1]))
        if above == OLIVE_BOT:
            for i, m in enumerate(OLIVE_BOT_TIP):
                g.set(x + i, y - 1, m, True)
        elif all(m == GRASS for m in above):
            for i, m in enumerate(OLIVE_TIP_GRASS):
                g.set(x + i, y - 1, m, bool(g.solid[y - 1, x + i]))


def woods(g):
    """Fill each island's T cells: olives and stone pines where 2x2 fits, then
    cypresses, then flowering scrub (still solid: a gap in the woods is woods)."""
    for y in range(H - 1):
        for x in range(W - 1):
            if free_grass(g, x, y, 2, 2) and hashed(x, y, 30) < 0.72:
                if hashed(x, y, 31) < 0.35:
                    for j, row in enumerate(PINE):
                        for i, m in enumerate(row):
                            g.set(x + i, y + j, m, True)
                else:
                    olive(g, x, y)
    for y in range(H - 1):
        for x in range(W):
            if free_grass(g, x, y, 1, 2):
                g.set(x, y, CYPRESS_TOP, True)
                g.set(x, y + 1, CYPRESS_BOT, True)
    for y in range(H):
        for x in range(W):
            if g.p.c[y][x] == "T" and g.mid[y, x] == GRASS and not g.solid[y, x]:
                g.set(x, y, FLOWERS if hashed(x, y, 41) < 0.5 else GRASS, True)


# ---------------------------------------------------------------------------
# Set pieces
# ---------------------------------------------------------------------------

def rock_distance(p):
    """For each mainland rock cell, how far (in cells) it is from anything that
    isn't rock: 1 on the coast, more inland."""
    dist = np.zeros((H, W), int)
    q = []
    for y in range(H):
        for x in range(W):
            if p.c[y][x] == "#":
                if any(0 <= x + dx < W and 0 <= y + dy < H and p.c[y + dy][x + dx] != "#"
                       for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                    dist[y, x] = 1
                    q.append((x, y))
    head = 0
    while head < len(q):
        x, y = q[head]
        head += 1
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and p.c[ny][nx] == "#" and dist[ny, nx] == 0:
                dist[ny, nx] = dist[y, x] + 1
                q.append((nx, ny))
    return dist


def scatter(g, events):
    """Rocks awash and floating timber where the sea would otherwise be empty:
    for each 9x7 block with nothing in it, one feature on open water, clear of
    every event, lane, gap and landing."""
    keep = set()
    for kind in ("object_events", "bg_events", "coord_events", "warp_events"):
        for e in events[kind]:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    keep.add((e["x"] + dx, e["y"] + dy))
    for (x, y), _, _ in LANDINGS.values():
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                keep.add((x + dx, y + dy))
    for y in range(H):
        for dx in range(-3, 4):
            keep.add((BARRIER_X + dx, y))
        for x in range(FOG_EDGE, FOG_ON_X + 4):
            keep.add((x, y))
    for x in range(W):
        for y in list(range(CURRENT_ROWS[0] - 2, CURRENT_ROWS[1] + 3)) + list(range(35, 43)):
            keep.add((x, y))
    for y in range(0, 34):
        for x in range(18, 24):
            keep.add((x, y))                         # either side of the north current

    def open_sea(x, y):
        return 0 <= x < W and 0 <= y < H and g.p.c[y][x] == "~" and not g.solid[y, x] \
            and int(g.mid[y, x]) == SEA

    BX, BY = 9, 7
    for by in range(0, H, BY):
        for bx in range(0, W, BX):
            cells = [(x, y) for y in range(by, min(H, by + BY)) for x in range(bx, min(W, bx + BX))]
            busy = sum(1 for (x, y) in cells if g.p.c[y][x] not in "~" or int(g.mid[y, x]) != SEA)
            if busy > 3:
                continue
            spots = [(x, y) for (x, y) in cells if (x, y) not in keep
                     and all(open_sea(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
            if not spots:
                continue
            x, y = spots[int(hashed(bx, by, 71) * len(spots))]
            r = hashed(bx, by, 72)
            if r < 0.45:
                g.set(x, y, g.k("reefs_" + "abc"[int(hashed(x, y, 73) * 3)]), True)
            elif r < 0.75:
                g.put("sea_rocks", x, y)
            else:
                g.set(x, y, g.k("debris_a" if x % 2 else "debris_b"))


def place(g):
    k = g.k
    # whirlpools: passable cells; invisible objects hold them till the Conch
    for (x, y) in (WHIRL_ECHINADES, WHIRL_LAGOON):
        g.put("whirlpool", x, y)
    for i, (x, y) in enumerate(ROCKS_COVE + ROCKS_CURRENT):
        g.set(x, y, k("ram_rock_a" if i % 2 == 0 else "ram_rock_b"), False)
    g.put("wreck", *WRECK)
    g.put("stone_ship", *STONE_SHIP)
    g.put("birds_rock", *BIRDS_ROCK)
    g.put("altar_stack", *ALTAR)
    for (key, x, y) in ISLETS:
        g.put(key, x, y)
    for (x, y) in POSTS:
        g.set(x, y, k("mooring_post"), True)
    # Halia's islet: the hut, the jetty, her boat, the nets, an olive by the door
    g.put("hut", *HUT, land=True)
    for (x, y), key in zip(JETTY, ("jetty_h", "jetty_h", "jetty_end_e")):
        g.set(x, y, k(key), False, land=True)
    g.put("boat_beached", 13, 48, land=True)
    g.put("net_poles", 16, 48, land=True)
    olive(g, 16, 45)
    g.set(*STELE, 0x003, True, land=True)          # aethos's marble stele: ROUTE 33
    olive(g, *PHORKYS_OLIVE)
    g.put("raft", *RAFT_GLAUKON)
    g.put("raft", *RAFT_AT_SEA)
    # sea stacks and rocks: the lanes' edges, and the lee for the floating finds
    for (key, x, y) in (("sea_stack", 23, 8), ("sea_rocks", 24, 13), ("sea_rocks", 9, 22),
                        ("sea_stack", 12, 25), ("sea_rocks", 7, 33), ("sea_rocks", 28, 22),
                        ("sea_stack", 2, 49), ("sea_rocks", 21, 57), ("sea_stack", 47, 61),
                        ("sea_rocks", 13, 71), ("sea_stack", 25, 77), ("sea_rocks", 54, 74),
                        ("sea_rocks", 36, 70), ("sea_stack", 17, 55), ("sea_rocks", 27, 33),
                        ("sea_rocks", 9, 14), ("sea_stack", 25, 2), ("sea_rocks", 30, 61),
                        ("sea_rocks", 45, 70), ("sea_rocks", 56, 79), ("sea_rocks", 14, 59),
                        ("sea_rocks", 34, 44), ("sea_rocks", 50, 66), ("sea_rocks", 18, 12)):
        if all(g.p.c[y + j][x + i] in "~:" for j in range(2 if key == "sea_stack" else 1)
               for i in range(2 if key == "sea_stack" else 1)):
            g.put(key, x, y)
    for (x, y) in ((35, 76), (36, 74), (24, 66), (28, 70)):
        g.set(x, y, k("debris_a" if x % 2 else "debris_b"))
    # the mainland: bare rock on the coast, scrub inland, stone pines and cypresses
    dist = rock_distance(g.p)
    taken = np.zeros((H, W), bool)
    for y in range(0, H - 1, 2):
        for x in range(0, W - 1, 2):
            cells = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if all(dist[cy, cx] >= 3 for cx, cy in cells) and hashed(x, y, 61) < 0.22:
                g.put("rock_pine", x, y)
                for cx, cy in cells:
                    taken[cy, cx] = True
    for y in range(0, H - 1, 2):
        for x in range(0, W, 2):
            if taken[y, x] or taken[y + 1, x]:
                continue
            if dist[y, x] >= 2 and dist[y + 1, x] >= 2 and hashed(x, y, 62) < 0.16:
                g.put("rock_cypress", x, y)
                taken[y, x] = taken[y + 1, x] = True
    for y in range(H):
        for x in range(W):
            if taken[y, x] or g.p.c[y][x] != "#" or int(g.mid[y, x]) not in (
                    k("rock_c"), k("rock_c_10"), k("rock_c_01"), k("rock_c_11")):
                continue
            d = dist[y, x]
            if (d >= 3 and hashed(x, y, 63) < 0.7) or (d == 2 and hashed(x, y, 64) < 0.35):
                g.set(x, y, k(f"rock_c_scrub_{x % 2}{y % 2}"), True)
    g.set(*CAVE, k("rock_b_cave"), True)


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

S = "Route33_WesternSea_EventScript_"
SWIMMER_M = "OBJ_EVENT_GFX_SWIMMER_M"     # ICHOR_STUB_PG_SPRITES: the Diver wants an Ichor swimmer
SWIMMER_F = "OBJ_EVENT_GFX_SWIMMER_F"
I = "OBJ_EVENT_GFX_ICHOR_"


def obj(gfx, x, y, script, move="MOVEMENT_TYPE_FACE_DOWN", trainer=False, sight=0, flag="0",
        local_id=None, elevation=1, rx=0, ry=0):
    o = {"graphics_id": gfx, "x": x, "y": y, "elevation": elevation, "movement_type": move,
         "movement_range_x": rx, "movement_range_y": ry,
         "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
         "trainer_sight_or_berry_tree_id": str(sight), "script": script, "flag": flag}
    if local_id:
        o = {"local_id": local_id, **o}
    return o


def item_ball(x, y, item, flag, elevation=1):
    # ICHOR_STUB_PG_SPRITES: a bobbing amphora wants its own object graphics
    return obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, "Common_EventScript_FindItem", sight=item, flag=flag,
               elevation=elevation)


def invisible(x, y, script, flag, local_id):
    return obj("OBJ_EVENT_GFX_ITEM_BALL", x, y, script, move="MOVEMENT_TYPE_INVISIBLE", flag=flag,
               local_id=local_id)


def sign(x, y, script, elevation=0):
    return {"type": "sign", "x": x, "y": y, "elevation": elevation,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": script}


def hidden(x, y, item, flag):
    return {"type": "hidden_item", "x": x, "y": y, "elevation": 0, "item": item, "flag": flag}


def trigger(x, y, script, var, value):
    return {"type": "trigger", "x": x, "y": y, "elevation": 0, "var": var, "var_value": value,
            "script": script}


# The trainers MAP_DESIGN calls checkpoints: the cells their lines must cover,
# which together close a crossing. westsea_review.check() proves it.
TRAINERS = {
    # name: (x, y, facing, sight, gfx, mandatory crossing)
    "Glaukon": (RAFT_GLAUKON[0], RAFT_GLAUKON[1], "left", 1, I + "SAILOR", None),
    "Pontia": (BARRIER_X, GAPS["north"][0] - 1, "down", 2, SWIMMER_F, "north"),
    "Aktaios": (BARRIER_X, GAPS["south"][0] - 1, "down", 2, SWIMMER_M, "south"),
    "Halieus": (WRECK[0] + 1, WRECK[1], "up", 1, I + "FISHER", None),
    "Nerites": (WHIRL_ECHINADES[0] - 1, WHIRL_ECHINADES[1] - 1, "right", 2, SWIMMER_M, "echinades"),
    "Damon": (STONE_SHIP[0] + 3, STONE_SHIP[1] + 1, "down", 1, I + "SAILOR", None),
}


def events():
    wx, wy = WHIRL_ECHINADES
    lx, ly = WHIRL_LAGOON
    objects = []
    for name, (x, y, facing, sight, gfx, _) in TRAINERS.items():
        objects.append(obj(gfx, x, y, S + name, f"MOVEMENT_TYPE_FACE_{facing.upper()}", trainer=True,
                           sight=sight, local_id=f"LOCALID_R33_{name.upper()}"))
    objects += [
        # Kymon, becalmed on his raft (at home in the hut once towed)
        obj(I + "FISHER", RAFT_AT_SEA[0], RAFT_AT_SEA[1], S + "KymonAtSea", "MOVEMENT_TYPE_FACE_LEFT",
            flag="FLAG_ICHOR_R33_KYMON_HOME", local_id="LOCALID_R33_KYMON"),
        # the whirlpools: four invisible cells each
        invisible(wx, wy, S + "WhirlpoolEchinades", "FLAG_ICHOR_R33_WHIRLPOOL_ECHINADES", "LOCALID_R33_WHIRL_E1"),
        invisible(wx + 1, wy, S + "WhirlpoolEchinades", "FLAG_ICHOR_R33_WHIRLPOOL_ECHINADES", "LOCALID_R33_WHIRL_E2"),
        invisible(wx, wy + 1, S + "WhirlpoolEchinades", "FLAG_ICHOR_R33_WHIRLPOOL_ECHINADES", "LOCALID_R33_WHIRL_E3"),
        invisible(wx + 1, wy + 1, S + "WhirlpoolEchinades", "FLAG_ICHOR_R33_WHIRLPOOL_ECHINADES", "LOCALID_R33_WHIRL_E4"),
        invisible(lx, ly, S + "WhirlpoolLagoon", "FLAG_ICHOR_R33_WHIRLPOOL_LAGOON", "LOCALID_R33_WHIRL_L1"),
        invisible(lx + 1, ly, S + "WhirlpoolLagoon", "FLAG_ICHOR_R33_WHIRLPOOL_LAGOON", "LOCALID_R33_WHIRL_L2"),
        invisible(lx, ly + 1, S + "WhirlpoolLagoon", "FLAG_ICHOR_R33_WHIRLPOOL_LAGOON", "LOCALID_R33_WHIRL_L3"),
        invisible(lx + 1, ly + 1, S + "WhirlpoolLagoon", "FLAG_ICHOR_R33_WHIRLPOOL_LAGOON", "LOCALID_R33_WHIRL_L4"),
        # the loose rock the ram breaks
        invisible(*ROCKS_COVE[0], S + "RocksCove", "FLAG_ICHOR_R33_ROCKS_COVE", "LOCALID_R33_ROCK_COVE1"),
        invisible(*ROCKS_COVE[1], S + "RocksCove", "FLAG_ICHOR_R33_ROCKS_COVE", "LOCALID_R33_ROCK_COVE2"),
        invisible(*ROCKS_CURRENT[0], S + "RocksCurrent", "FLAG_ICHOR_R33_ROCKS_CHANNEL", "LOCALID_R33_ROCK_CURRENT1"),
        invisible(*ROCKS_CURRENT[1], S + "RocksCurrent", "FLAG_ICHOR_R33_ROCKS_CHANNEL", "LOCALID_R33_ROCK_CURRENT2"),
        # the fog bank's way through: FLAG_TEMP_1 is set on load once Labor 10's Pillars stand
        invisible(*FOG_GATE[0], S + "FogBank", "FLAG_TEMP_1", "LOCALID_R33_FOG1"),
        invisible(*FOG_GATE[1], S + "FogBank", "FLAG_TEMP_1", "LOCALID_R33_FOG2"),
        # floating amphorae, and the cove's find
        item_ball(28, 17, "ITEM_MAX_ELIXIR", "FLAG_ICHOR_ITEM_R33_BIRDS_ROCK"),     # in the stack's lee
        item_ball(16, 64, "ITEM_MAX_REVIVE", "FLAG_ICHOR_ITEM_R33_CURRENT"),        # the current's eddy
        item_ball(COVE[0], COVE[1], "ITEM_ABILITY_CAPSULE", "FLAG_ICHOR_ITEM_R33_COVE"),
        item_ball(LAGOON[0] + 1, LAGOON[1], "ITEM_DAMP_ROCK", "FLAG_ICHOR_ITEM_R33_LAGOON"),
    ]
    bgs = [
        # landings (ICHOR_STUB_PG_LANDING until EventScript_IchorLand lands)
        sign(*LANDINGS["TAINARON"][0], S + "LandTainaron"),
        sign(*LANDINGS["ITHAKA"][0], S + "LandIthaka"),
        sign(*LANDINGS["KERKYRA"][0], S + "LandKerkyra"),
        sign(*LANDINGS["ROUTE33"][0], S + "LandJetty"),
        # the set pieces
        sign(STONE_SHIP[0] + 1, STONE_SHIP[1] + 1, S + "StoneShip"),
        sign(STONE_SHIP[0] + 4, STONE_SHIP[1] + 1, S + "StoneShip"),
        sign(ALTAR[0], ALTAR[1] + 2, S + "PoseidonsAltar"),
        sign(ALTAR[0] + 1, ALTAR[1] + 2, S + "PoseidonsAltar"),
        sign(*CAVE, S + "TainaronCave"),
        sign(8, 38, S + "Echinades"),
        sign(24, 38, S + "Echinades"),
        sign(PHORKYS_OLIVE[0] + 1, PHORKYS_OLIVE[1] + 1, S + "PhorkysOlive"),
        sign(*STELE, S + "SignIslet"),
        # hidden items
        hidden(WRECK[0] + 2, WRECK[1], "ITEM_BIG_NUGGET", "FLAG_ICHOR_HIDDEN_R33_WRECK"),
        hidden(STONE_SHIP[0] + 2, STONE_SHIP[1], "ITEM_STAR_PIECE", "FLAG_ICHOR_HIDDEN_R33_STONE_SHIP"),
        hidden(BIRDS_ROCK[0] + 1, BIRDS_ROCK[1] + 1, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_HIDDEN_R33_BIRDS_ROCK"),
        hidden(PHORKYS_OLIVE[0] + 1, PHORKYS_OLIVE[1], "ITEM_OLIVE_OIL", "FLAG_ICHOR_HIDDEN_R33_PHORKYS"),
        hidden(14, 51, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_R33_HALIA"),
        hidden(ALTAR[0] + 1, ALTAR[1] + 1, "ITEM_BIG_PEARL", "FLAG_ICHOR_HIDDEN_R33_ALTAR"),
    ]
    warps = [{"x": HUT_DOOR[0], "y": HUT_DOOR[1], "elevation": 3,
              "dest_map": "MAP_ROUTE33_WESTERN_SEA_HALIAS_HUT", "dest_warp_id": "0"}]
    coords = []
    # fog weather: on as you sail into the bank's approach, off as you leave it
    for y in range(52, H):
        coords.append(trigger(FOG_ON_X, y, S + "FogOn", "VAR_TEMP_2", "0"))
        coords.append(trigger(FOG_OFF_X, y, S + "FogOff", "VAR_TEMP_2", "1"))
    return {"object_events": objects, "warp_events": warps, "coord_events": coords, "bg_events": bgs}


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def encode(g):
    out = np.zeros((H, W), np.uint16)
    for y in range(H):
        for x in range(W):
            elev = 3 if g.landish[y, x] else 1
            out[y, x] = int(g.mid[y, x]) | (int(g.solid[y, x]) << 10) | (elev << 12)
    return out


def write(g, ev):
    d = ROOT / "data/layouts" / NAME
    d.mkdir(parents=True, exist_ok=True)
    encode(g).astype("<u2").tofile(d / "map.bin")
    np.array([SEA] * 4, np.uint16).astype("<u2").tofile(d / "border.bin")
    data = json.loads(LAYOUTS.read_text())
    for lay in data["layouts"]:
        if lay.get("id") == LAYOUT_ID:
            lay.update({"width": W, "height": H, "primary_tileset": "gTileset_Aethos",
                        "secondary_tileset": "gTileset_Westsea"})
            break
    else:
        sys.exit(f"no layout {LAYOUT_ID}")
    LAYOUTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    path = ROOT / "data/maps" / NAME / "map.json"
    m = json.loads(path.read_text())
    m.update({"music": "MUS_ICHOR_TRIREME", "weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_OCEAN_ROUTE",
              "allow_cycling": False, "allow_running": True, "show_map_name": True,
              "region_map_section": "MAPSEC_AETHOS_ROUTE_33", "connections": None})
    m.update(ev)
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    write_header(g)


HEADER = ROOT / "include/constants/ichor_postgame_sea.h"
BEGIN = "// Route 33's cells and metatiles: written by tools/ichor/maps/westsea.py. Don't edit by hand.\n"
END = "// End of Route 33's cells and metatiles.\n"


def write_header(g):
    """Route 33's coordinates and metatile ids for its map scripts, as #defines in
    include/constants/ichor_postgame_sea.h, between the generated markers."""
    k = g.k
    defs = [
        ("METATILE_R33_SEA", f"0x{SEA:03X}", "aethos's open sea"),
        ("METATILE_R33_CURRENT_W", f"0x{k('current_wa'):03X}", "westsea's westward current"),
        ("METATILE_R33_RAFT_L", f"0x{k('raft', 0, 0):03X}", "Kymon's raft, left cell"),
        ("METATILE_R33_RAFT_R", f"0x{k('raft', 1, 0):03X}", "Kymon's raft, right cell"),
        ("R33_WHIRL_ECHINADES_X", WHIRL_ECHINADES[0], "the Echinades' whirlpool, top-left (2x2)"),
        ("R33_WHIRL_ECHINADES_Y", WHIRL_ECHINADES[1], ""),
        ("R33_WHIRL_LAGOON_X", WHIRL_LAGOON[0], "the lagoon's whirlpool, top-left (2x2)"),
        ("R33_WHIRL_LAGOON_Y", WHIRL_LAGOON[1], ""),
        ("R33_ROCKS_COVE_X", ROCKS_COVE[0][0], "the cove's loose rock: two cells east-west"),
        ("R33_ROCKS_COVE_Y", ROCKS_COVE[0][1], ""),
        ("R33_ROCKS_CURRENT_X", ROCKS_CURRENT[0][0], "the current's loose rock: two cells north-south"),
        ("R33_ROCKS_CURRENT_Y", ROCKS_CURRENT[0][1], ""),
        ("R33_RAFT_SEA_X", RAFT_AT_SEA[0], "Kymon's raft, becalmed (2x1)"),
        ("R33_RAFT_SEA_Y", RAFT_AT_SEA[1], ""),
        ("R33_RAFT_HOME_X", RAFT_HOME[0], "Kymon's raft, moored at Halia's jetty (2x1)"),
        ("R33_RAFT_HOME_Y", RAFT_HOME[1], ""),
        ("R33_TOW_X", LANDINGS["ROUTE33"][0][0], "where the tow leaves you: the jetty's landing"),
        ("R33_TOW_Y", LANDINGS["ROUTE33"][0][1], ""),
        ("R33_FOG_ON_X", FOG_ON_X, "the fog's approach: weather on west of here"),
        ("R33_FOG_TOP_Y", 52, "and south of here"),
    ]
    lines = [BEGIN]
    for name, val, note in defs:
        lines.append(f"#define {name:<26} {val}" + (f"  // {note}" if note else "") + "\n")
    lines.append(END)
    text = HEADER.read_text()
    a, b = text.index(BEGIN), text.index(END) + len(END)
    HEADER.write_text(text[:a] + "".join(lines) + text[b:])


def build():
    if not CAT.exists():
        sys.exit(f"{CAT} is missing; run tools/ichor/art/westsea_build.py first")
    cat = {s["key"]: s for s in json.loads(CAT.read_text())}
    plan = compose_plan()
    smooth_rock(plan)
    g = tile(plan, cat)
    woods(g)
    place(g)
    ev = events()
    scatter(g, ev)
    return plan, g, ev


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--no-check", action="store_true")
    ap.add_argument("--plan", action="store_true", help="print the ground plan and stop")
    args = ap.parse_args()
    plan, g, ev = build()
    if args.plan:
        print(plan.text())
        return
    write(g, ev)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import westsea_hut
    westsea_hut.build()
    import westsea_review
    if args.render:
        westsea_review.render(args.render)
    if not args.no_check:
        errors = westsea_review.check()
        for e in errors:
            print("CHECK:", e)
        if errors:
            sys.exit(1)
        print("westsea: Route 33 written, checks pass")


if __name__ == "__main__":
    main()
