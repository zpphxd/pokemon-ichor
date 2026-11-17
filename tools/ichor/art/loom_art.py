"""gTileset_Loom: the Loom under the Omphalos and the Stair of Hours
(design/phase4/SCRIPT.md beats III-9 to III-11, Part 10 "Tileset: loom";
design/maps/TheLoom.md and design/maps/StairOfHours.md).

Both maps are one-off set pieces, so this tileset is drawn the other way round
from a biome set: each map is **painted whole, as a scene, at map scale**, in
every state the story needs, and the scenes are sliced into 16x16 cells. Every
distinct cell (its pixels, layers and behavior) becomes one metatile, and the
builder writes the layout from the same grid, so the map is exactly the
painting. Repeating ground (warp threads, floor, chasm, sky, paving) is painted
with patterns locked to the 16 px grid, so it costs a handful of metatiles; the
set pieces (the cloth, the chains, the dials, the numerals) are drawn once.

The scenes:
  loom_before   the Loom on the night of the Omphalos: the warp, the cloth, the
                three chains to the posts and the beam, the chasm below
  loom_after    after the cut: the chains broken and coiled on the spurs, the roof
                torn open on the sky at the west end, the foot of the Stair of
                Hours climbing the west wall
  stair         the Stair of Hours, all flights solid
  stair_ghost   the three gated flights (to landings 1, 5 and 9) still unformed:
                pale outlines of steps that won't take your weight
  stair_fallen  every flight gone to sky (the crumble, III-11C): the hour-stones
                hang alone

Palette plan (secondary slots 6-12; six used):
  rock   Parnassos limestone of the cavern: roof, walls, the shelf floor, the
         spurs, the pillars, the chasm's black
  loom   timber and bronze: the posts, the cloth beam, the pegs
  warp   the warp and the cloth: the dark behind the threads, white thread, the
         red knots, the red-brown wool of the woven band and its black-figure
         pictures, and the clay loom-weights
  chain  black adamant (middle layer only, over whatever it crosses)
  stone  the Stair: cyclopean dark stone, cut limestone, white marble, gold,
         the bronze dials
  sky    the stopped dawn: the sky, the cloud sea, the unformed steps

Every 8x8 tile of every layer draws from one group (validate() checks it), every
bottom layer is opaque, and no metatile uses three layers.
"""
from __future__ import annotations

import math

import numpy as np

import emporion_lib as E
import kalliste_lib as K
from kalliste_lib import Layer, tile_colors

# --------------------------------------------------------------------------
# Colors and groups
# --------------------------------------------------------------------------

NEW = {
    # rock: the cavern's limestone, cool and dark, with the chasm's black
    "lr0": (8, 8, 16), "lr1": (32, 24, 32), "lr2": (56, 48, 56), "lr3": (80, 72, 80),
    "lr4": (112, 104, 104), "lr5": (144, 136, 128), "lr6": (176, 168, 152), "lr7": (208, 200, 184),
    "lro0": (104, 80, 56), "lro1": (152, 120, 80),
    # loom: timber and bronze
    "lt0": (40, 24, 24), "lt1": (72, 48, 32), "lt2": (112, 72, 40), "lt3": (152, 104, 56),
    "lt4": (192, 144, 88), "lb0": (120, 80, 32), "lb1": (184, 136, 48), "lb2": (240, 200, 104),
    # warp: the dark, the thread, the knots, the wool
    "lw0": (8, 8, 16), "lw1": (24, 24, 40), "lw2": (48, 48, 64),
    "lw3": (144, 136, 136), "lw4": (200, 192, 184), "lw5": (240, 232, 224),
    "lk0": (120, 24, 32), "lk1": (192, 48, 48), "lk2": (240, 112, 96),
    "lc0": (96, 40, 32), "lc1": (160, 80, 40), "lc2": (208, 136, 80), "lc3": (232, 216, 176),
    # chain: black adamant
    "la0": (16, 16, 24), "la1": (48, 48, 64), "la2": (96, 96, 120), "la3": (160, 160, 192),
    "la4": (224, 224, 248),
    # stone: the Stair
    "ls0": (32, 32, 40), "ls1": (64, 64, 72), "ls2": (96, 88, 96), "ls3": (128, 120, 120),
    "ls4": (160, 152, 144), "ls5": (192, 184, 168), "ls6": (224, 216, 200), "ls7": (248, 240, 224),
    "lsl0": (168, 144, 104), "lsl1": (208, 184, 136), "lsg0": (176, 128, 40), "lsg1": (232, 184, 64),
    # sky: the stopped dawn
    "lk_hi": (136, 152, 200), "lk_md": (160, 176, 216), "lk_lo": (184, 192, 224),
    "lcl0": (160, 144, 176), "lcl1": (208, 168, 176), "lcl2": (240, 208, 200), "lcl3": (248, 240, 232),
    "lcg": (248, 216, 160), "lgh0": (176, 184, 216), "lgh1": (216, 224, 240),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    "rock": ["lr0", "lr1", "lr2", "lr3", "lr4", "lr5", "lr6", "lr7", "lro0", "lro1"],
    "loom": ["lr0", "lt0", "lt1", "lt2", "lt3", "lt4", "lb0", "lb1", "lb2", "lr1", "lr2"],
    "warp": ["lw0", "lw1", "lw2", "lw3", "lw4", "lw5", "lk0", "lk1", "lk2",
             "lc0", "lc1", "lc2", "lc3"],
    "chain": ["la0", "la1", "la2", "la3", "la4"],
    "stone": ["ls0", "ls1", "ls2", "ls3", "ls4", "ls5", "ls6", "ls7", "lsl0", "lsl1",
              "lsg0", "lsg1"],
    "sky": ["lk_hi", "lk_md", "lk_lo", "lcl0", "lcl1", "lcl2", "lcl3", "lcg", "lgh0", "lgh1"],
}
# lr0 and lw0 are one color (the chasm's black is the dark behind the warp)
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(C[n] for n in _names)) == len(_names), _g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}


def h32(x, y, salt=0):
    v = (x * 374761393 + y * 668265263 + salt * 2246822519) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return (v ^ (v >> 16)) & 0xFFFF


# --------------------------------------------------------------------------
# A scene: two layers at map scale, and a walk grid
# --------------------------------------------------------------------------

class Scene:
    """A map painted whole. walk[y][x]: '.' walkable, 'X' blocked. beh: (x, y) -> MB_*."""

    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.B = Layer(w * 16, h * 16)
        self.M = Layer(w * 16, h * 16)
        self.walk = [["X"] * w for _ in range(h)]
        self.beh = {}

    def walkable(self, x0, y0, x1, y1, on=True):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < self.w and 0 <= y < self.h:
                    self.walk[y][x] = "." if on else "X"

    def copy(self, name):
        s = Scene(name, self.w, self.h)
        s.B.a = self.B.a.copy()
        s.M.a = self.M.a.copy()
        s.walk = [r[:] for r in self.walk]
        s.beh = dict(self.beh)
        return s

    def fill(self, L, cx0, cy0, cx1, cy1, fn):
        """fn(x, y) -> color name or None, over cells cx0..cx1, cy0..cy1 (map pixels)."""
        for y in range(cy0 * 16, (cy1 + 1) * 16):
            for x in range(cx0 * 16, (cx1 + 1) * 16):
                c = fn(x, y)
                if c:
                    L.px(x, y, c)

    def clear(self, L, cx0, cy0, cx1, cy1):
        L.a[cy0 * 16:(cy1 + 1) * 16, cx0 * 16:(cx1 + 1) * 16] = 0

    def cell(self, cx, cy):
        sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        return self.B.a[sl], self.M.a[sl]


# --------------------------------------------------------------------------
# Textures (all periodic on the 16 px grid, so repeated ground is one metatile)
# --------------------------------------------------------------------------

def blocky(period_x, period_y, salt, levels):
    """A periodic 2x2-pixel-block value field, quantized to `levels` names. The
    2 px blocks keep shading in clusters (STYLE.md §4.3: no salt-and-pepper)."""
    bx, by = period_x // 2, period_y // 2
    rng = np.random.default_rng(salt)
    base = rng.random((by, bx))
    # smooth it a little, wrapping, so values clump
    sm = (base + np.roll(base, 1, 0) + np.roll(base, 1, 1) + np.roll(base, -1, 0)
          + np.roll(base, -1, 1)) / 5
    lo, hi = sm.min(), sm.max()
    q = ((sm - lo) / (hi - lo + 1e-9) * len(levels)).astype(int).clip(0, len(levels) - 1)

    def f(x, y):
        return levels[q[(y // 2) % by, (x // 2) % bx]]
    return f


ROOF = blocky(32, 16, 7, ["lr1", "lr2", "lr2", "lr2", "lr3", "lr3", "lr4"])
WALL = blocky(32, 32, 11, ["lr1", "lr2", "lr2", "lr3", "lr3", "lr3", "lr4"])
FLOOR = blocky(32, 32, 5, ["lr3", "lr4", "lr4", "lr4", "lr4", "lr4", "lr5", "lr5"])


def floor_px(x, y):
    c = FLOOR(x, y)
    # the threads' faint light on the stone nearest the chasm, fading south
    row = y // 16
    if row == 11 and c == "lr4" and (y % 16) < 9:
        c = "lr5"
    elif row == 13 and c == "lr4" and (x // 2 + y // 2) % 3 == 0:
        c = "lr3"
    # a few long cracks in the bedrock, on a 64 px period
    xx, yy = x % 32, y % 32
    # slabs of bedrock: an irregular joint net on a 32 px period, each slab
    # catching the light on its upper left edge
    # a few natural cracks in the bedrock, each with a lit lip below it
    crack = (yy == 20 and 2 <= xx < 13) or (yy == 21 and 12 <= xx < 15) or \
            (xx == 25 and 6 <= yy < 12) or (xx == 26 and 11 <= yy < 15) or (yy == 30 and 18 <= xx < 22)
    if crack:
        return "lr2"
    lip = (yy == 21 and 2 <= xx < 12) or (yy == 22 and 12 <= xx < 15) or \
          (xx == 26 and 6 <= yy < 11) or (xx == 27 and 11 <= yy < 15)
    if lip:
        return "lr5"
    return c


# --------------------------------------------------------------------------
# The Loom (34 x 14)
# --------------------------------------------------------------------------

LOOM_W, LOOM_H = 34, 14
POST_X = (3, 30)
BEAM_Y = 2
CLOTH_Y = (3, 4)
WARP_Y = (5, 6, 7)
LAST_Y = 8
CHASM_Y = (9, 10)
FLOOR_Y = (11, 12, 13)
SPURS = {"spinner": 6, "measurer": 16, "cutter": 26}      # each spur is x..x+1
FATE_AT = {"spinner": (6, 9), "measurer": (16, 9), "cutter": (27, 9)}
EAST_DOOR = (33, 12)
BOULDERS = [(5, 13, "boulder"), (11, 13, "mite"), (19, 13, "boulder"), (20, 13, "mite"),
            (29, 13, "boulder"), (2, 13, "mite")]
ROCKS = {
    "boulder": ["................",
                "......2222......",
                "....22666522....",
                "...2676555532...",
                "..267655544332..",
                "..2765554443322.",
                ".27655544433322.",
                ".26555444333222.",
                ".25554443332221.",
                ".24444333322211.",
                "..233333222211..",
                "...1122222111...",
                "....11111111...."],
    "mite": ["................",
             ".......22.......",
             "......2652......",
             "......2653......",
             ".....26543......",
             ".....265432.....",
             "....2655432.....",
             "....2654432..2..",
             "...26554332.262.",
             "...26544332.2532",
             "..265443322.2432",
             "..2654433221.21.",
             ".265444333221...",
             ".2544433322211..",
             "..1112222211....",
             "................"],
}
WEST_STAIR = (1, 11)

# The woven band: the story so far, in black-figure on red-brown wool (k black
# figure, c cream incision). 32 x 18 each; they straddle rows 3 and 4.
MOTIFS = {
    "olive": [
        "................................",
        "...........kkk...kkkk...........",
        ".........kkkkkkkkkkkkkk.........",
        ".......kkkkkkkkkkkkkkkkkk.......",
        "......kkkkkckkkkkkkkckkkkk......",
        ".....kkkkkkkkkkkckkkkkkkkkk.....",
        "......kkkkckkkkkkkkkkkckkk......",
        "........kkkkkkkkkkkkkkkk........",
        "..........kkkk.kk.kkkk..........",
        "...............kk...............",
        "..............kkk...............",
        "..............kkk...............",
        ".............kkkk...............",
        "..............kkkk..............",
        "..............kkk...............",
        ".............kkkkk..............",
        "...........kkkkkkkkk............",
        "................................"],
    "ship": [
        "................................",
        "...............k................",
        "...............k................",
        "..........kkkkkkkkkkk...........",
        "..........kckkckkckkk...........",
        "..........kkkkkkkkkkk...........",
        "..........kckkckkckkk...........",
        "..........kkkkkkkkkkk...........",
        "k..............k...............k",
        "kk.............k..............kk",
        ".kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.",
        "..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..",
        "..kckckckckckckckckckckckckck...",
        "...kkkkkkkkkkkkkkkkkkkkkkkkkk...",
        "....k.k.k.k.k.k.k.k.k.k.k.k.....",
        "...k.k.k.k.k.k.k.k.k.k.k.k......",
        "................................",
        "................................"],
    "bull": [
        "................................",
        "...k............................",
        "....k...........................",
        "....kk..kkkkkkkkkkkkkkkkk.......",
        "...kkkkkkkkkkkkkkkkkkkkkkkk.....",
        "..kckkkkkkkkkkkkkkkkkkkkkkkk....",
        "..kkkkkkkkkkkkkkkkkkkkkkkkkkk...",
        "...kkkkkkkkkcckkkkkkkkkkkkkkkk..",
        "....kkkkkkkkkkkkkkkkkkkkkkkkk.k.",
        ".....kkkkkkkkkkkkkkkkkkkkkkk..k.",
        "......kkkkkkkkkkkkkkkkkkkkkk....",
        "......kk.kk...........kk.kk.....",
        "......kk..kk..........kk..kk....",
        ".....kk...kk.........kk...kk....",
        ".....k.....k.........k.....k....",
        "................................",
        "................................",
        "................................"],
    "fates": [
        "................................",
        "..kkkkkkkkkkkkkkkkkkkkkkkkkkkk..",
        "..k.c.c.c.c.c.c.c.c.c.c.c.c.ck..",
        "..k.c.c.c.c.c.c.c.c.c.c.c.c.ck..",
        "..k.c.c.c.c.c.c.c.c.c.c.c.c.ck..",
        "..k.........................k...",
        "..k..kk.......kk.......kk...k...",
        "..k.kkkk.....kkkk.....kkkk..k...",
        "..k..kk.......kk.......kk...k...",
        "..k.kkkk.....kkkk.....kkkk..k...",
        "..k.kkkkk...kkkkkk...kkkkk..k...",
        "..k.kkckk...kkckkk...kkckk..k...",
        "..k.kkkkkk..kkkkkk..kkkkkk..k...",
        "..k.kkkkkk..kkkkkk..kkkkkk..k...",
        "..k.kkkkkk..kkkkkk..kkkkkk..k...",
        "..k..k..k....k..k....k..k...k...",
        ".kkk.......................kkk..",
        "................................"],
    "sickle": [
        "................................",
        ".....................kkkk.......",
        "...................kkkkkkkk.....",
        ".................kkkk....kkkk...",
        "................kkk........kk...",
        "...............kkk..........k...",
        "...............kk.....c.........",
        "..............kkk...............",
        "..............kkk.........c.....",
        "..............kkk...............",
        "...............kkk.....c........",
        "................kkkk............",
        "..................kkkkk.........",
        "....................kkkkkk......",
        "......................kkkk......",
        ".......................kk.......",
        "......................kkk.......",
        ".....................kkk........"],
}
ROSETTE = [
    "................",
    "................",
    "................",
    "......k..k......",
    ".....kkkkkk.....",
    "....kkkckkkk....",
    "...kkkcccckk....",
    "....kkkckkkk....",
    ".....kkkkkk.....",
    "......k..k......",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................"]
# west to east, x = 4 .. 29: f = a rosette filler
FRIEZE = ["f", "olive", "f", "ship", "f", "bull", "f", "fates", "f", "ship~", "f",
          "bull~", "f", "olive~", "f", "sickle", "f", "f"]
MEANDER = ["cccccccc",
           "c.....c.",
           "c.ccc.c.",
           "c.c...c.",
           "c.ccccc."]


def paint_cloth(sc):
    L = sc.B
    y0 = CLOTH_Y[0] * 16
    x0 = 4 * 16
    x1 = 30 * 16
    for x in range(x0, x1):
        # rows 3-4: the woven band
        for y in range(y0, y0 + 32):
            yy = y - y0
            c = "lc1"
            if yy < 2:
                c = "lc0"
            elif yy < 7:
                ch = MEANDER[yy - 2][(x - x0) % 8]
                c = "lc3" if ch == "c" else "lc0"
            elif yy == 7:
                c = "lc0"
            elif yy == 25:
                c = "lc0"
            elif yy in (26, 27):
                c = "lc3" if (x // 2 + (yy == 27)) % 2 == 0 and (x % 4) < 2 else "lc0"
            elif yy == 28:
                c = "lc0"
            elif yy >= 29:
                # the fell: the cloth ends in a fringe where the open warp begins
                tx = (x - x0) % 4
                c = ("lw4" if tx == 1 else "lw3" if tx == 3 else "lw0") if yy > 29 else "lc0"
            L.px(x, y, c)
    # the pictures, in the band's rows 8-24 (18 px)
    cx = 4
    for m in FRIEZE:
        flip = m.endswith("~")
        name = m.rstrip("~")
        rows = ROSETTE if name == "f" else MOTIFS[name]
        L.blit(rows, {"k": "lw0", "c": "lc3"}, cx * 16, y0 + 7, hflip=flip)
        cx += 1 if name == "f" else 2
    assert cx == 30, cx


THREADS = {1: "lw5", 4: "lw4", 7: "lw5", 10: "lw3", 13: "lw4"}


def paint_warp(sc):
    """Rows 5-7: the open warp. Five threads a cell, bright and dim, on the dark."""
    L = sc.B
    for x in range(4 * 16, 30 * 16):
        tx = x % 16
        for y in range(WARP_Y[0] * 16, (WARP_Y[-1] + 1) * 16):
            c = "lw0"
            if tx in THREADS:
                c = THREADS[tx]
            elif tx in (2, 8, 14) and (y // 4) % 2:
                c = "lw1"     # threads further back, half lost in the dark
            L.px(x, y, c)
    # the last row: each pair or three of threads gathers in a red knot, then a
    # cord to a clay loom-weight, and under the weights the dark
    y0 = LAST_Y * 16
    for x in range(4 * 16, 30 * 16):
        for y in range(y0, y0 + 16):
            L.px(x, y, "lw0")
    for cx in range(4, 30):
        X = cx * 16
        # threads run down into the knots (rows 0-4)
        for t, c in THREADS.items():
            for y in range(0, 4):
                L.px(X + t, y0 + y, c)
        for t, k in ((1, 2), (4, 3), (7, 4), (10, 10), (13, 11)):
            L.px(X + (t + k) // 2, y0 + 4, THREADS[t])
        for kx in (3, 10):
            # the knot
            L.rect(X + kx, y0 + 5, 3, 2, "lk1")
            L.px(X + kx, y0 + 5, "lk2")
            L.px(X + kx + 2, y0 + 6, "lk0")
            # the cord and the weight: a little clay pyramid with a hole
            L.px(X + kx + 1, y0 + 7, "lw3")
            L.blit(["..c..", ".ccC.", ".cCC.", "ccCCd", "ccCdd", "ddddd"],
                   {"c": "lc2", "C": "lc1", "d": "lc0"}, X + kx - 1, y0 + 8)
            L.px(X + kx + 1, y0 + 10, "lw0")


def paint_beam_posts(sc, after=False):
    B, M = sc.B, sc.M
    y0 = BEAM_Y * 16
    # the cloth beam: a great squared timber, banded in bronze at the posts
    for x in range(4 * 16, 30 * 16):
        for y in range(y0, y0 + 16):
            yy = y - y0
            if yy < 2:
                c = "lr0"
            elif yy == 2:
                c = "lt3"
            elif yy == 3:
                c = "lt4" if (x // 6) % 3 else "lt3"
            elif yy < 9:
                c = "lt2" if ((x % 32) + yy * 3) % 23 else "lt1"
            elif yy == 9:
                c = "lt1"
            else:
                c = "lt0"
            B.px(x, y, c)
    # the cloth wraps round the beam's foot (warp group, middle layer)
    for x in range(4 * 16, 30 * 16):
        for y in range(y0 + 10, y0 + 16):
            M.px(x, y, "lc0" if y < y0 + 12 else "lc1")
        if x % 16 in (5, 6):
            M.px(x, y0 + 12, "lc0")   # the folds
    # bronze bands near the posts and pegs along the beam
    for bx in (4 * 16 + 2, 29 * 16 + 8):
        for x in range(bx, bx + 6):
            for y in range(y0 + 2, y0 + 10):
                B.px(x, y, "lb1" if x - bx in (1, 2) else "lb0")
            B.px(x, y0 + 2, "lb2")
    for px_ in range(5 * 16 + 8, 29 * 16, 32):
        B.px(px_, y0 + 5, "lb2")
        B.px(px_, y0 + 6, "lb1")
    # the posts: x = 3 and 30. Rows 2-8 are drawn whole into the bottom layer on
    # the dark (chains may cross them on the middle layer); the finial (row 1) and
    # the foot (row 9) stand on the middle layer over the rock.
    for i, cx in enumerate(POST_X):
        X = cx * 16
        flip = i == 1
        for y in range(2 * 16, 9 * 16):
            for xx in range(16):
                B.px(X + xx, y, "lr0")
        for y in range(1 * 16 + 4, 9 * 16 + 10):
            L = B if 2 * 16 <= y < 9 * 16 else M
            for xx in range(2, 14):
                X_ = 15 - xx if flip else xx
                if xx == 2 or xx == 13:
                    c = "lt0"
                elif xx in (3, 4):
                    c = "lt3"
                elif xx >= 11:
                    c = "lt1"
                else:
                    c = "lt2" if ((y % 16) * 7 + xx * 3) % 29 else "lt1"
                L.px(X + X_, y, c)
        # the finial
        M.blit(["..bbbb..", ".bBBBBb.", ".bBBBBb.", "..bbbb.."],
               {"b": "lb0", "B": "lb1"}, X + 4, 1 * 16)
        M.px(X + 6, 1 * 16 + 1, "lb2")
        # bronze collars where the beam rests, and at the foot
        for yy in (y0 + 1, y0 + 2, 9 * 16 + 8, 9 * 16 + 9):
            L = B if yy < 9 * 16 else M
            for xx in range(2, 14):
                L.px(X + xx, yy, "lb1" if yy in (y0 + 1, 9 * 16 + 8) else "lb0")
        # the beam's end sits in the post's notch
        for y in range(y0 + 3, y0 + 9):
            B.px(X + (13 if not flip else 2), y, "lt4")
    # the pillars the posts stand on, out of the chasm (rock, bottom layer)
    for cx in POST_X:
        X = cx * 16
        for y in range(9 * 16, 11 * 16):
            fade = (y - 9 * 16) / 32
            for xx in range(16):
                if xx < 1 or xx > 14:
                    c = "lr0"
                else:
                    ramp = ["lr6", "lr5", "lr4", "lr4", "lr3", "lr3", "lr3", "lr2", "lr2", "lr2",
                            "lr2", "lr1", "lr1", "lr1"]
                    c = ramp[xx - 1]
                    lvl = ["lr0", "lr1", "lr2", "lr3", "lr4", "lr5", "lr6"].index(c) if c in (
                        "lr0", "lr1", "lr2", "lr3", "lr4", "lr5", "lr6") else 3
                    lvl = max(0, lvl - int(fade * 5 + ((xx + y) % 3 == 0) * (fade > .5)))
                    c = ["lr0", "lr1", "lr2", "lr3", "lr4", "lr5", "lr6"][lvl]
                B.px(X + xx, y, c)


def paint_rock(sc):
    B = sc.B
    W = sc.w
    # the roof: rows 0-1, with a fringe of stalactites at row 1's foot, over the dark
    for x in range(0, W * 16):
        tip = 10 + [0, 4, 6, 3, 0, 1, 5, 2, 0, 0, 3, 5][(x % 32) // 3 % 12] if x % 32 < 30 else 10
        for y in range(0, 32):
            if y < 16 + tip:
                c = ROOF(x, y)
                if y == 16 + tip - 1:
                    c = "lr1"
                elif y > 16 + tip - 4 and c == "lr4":
                    c = "lr3"
            else:
                c = "lr0"
            B.px(x, y, c)
    # the side walls: x 0-2 and 31-33, rows 2-10
    for (cx0, cx1, west) in ((0, 2, True), (31, 33, False)):
        for y in range(32, 11 * 16):
            for x in range(cx0 * 16, (cx1 + 1) * 16):
                c = WALL(x, y)
                # the wall's face toward the hall is lit (west wall) or shadowed
                edge = (cx1 * 16 + 15 - x) if west else (x - cx0 * 16)
                if edge < 2:
                    c = "lr5" if west else "lr1"
                elif edge < 4 and west:
                    c = "lr4"
                B.px(x, y, c)
    # the floor: rows 11-13 (and its two end walls stay rock)
    for x in range(0, W * 16):
        for y in range(11 * 16, 14 * 16):
            B.px(x, y, floor_px(x, y))
    # the far walls at the ends of the shelf (x 0 and 33 on rows 11-13)
    for y in range(11 * 16, 14 * 16):
        for x in range(0, 16):
            B.px(x, y, WALL(x, y) if x < 13 else ("lr5" if x < 15 else "lr4"))
        for x in range(33 * 16, 34 * 16):
            B.px(x, y, WALL(x, y) if x > 33 * 16 + 2 else "lr1")
    # the chasm: rows 9-10, x 3..30, a far wall falling into black
    for x in range(3 * 16, 31 * 16):
        for y in range(9 * 16, 11 * 16):
            yy = y - 9 * 16
            if yy < 4:
                c = "lr2" if (x // 4 + yy) % 5 else "lr1"
            elif yy < 9:
                c = "lr1" if (x // 2 + yy) % 7 else "lr0"
            else:
                c = "lr0"
                if ((x % 32) // 2, (y % 32) // 2) in ((3, 12), (11, 13), (9, 15)):
                    c = "lr1"
            B.px(x, y, c)
    # the floor's lip at the chasm's edge (row 11's top)
    for x in range(1 * 16, 33 * 16):
        B.px(x, 11 * 16, "lr2")
        B.px(x, 11 * 16 + 1, "lr7")
        B.px(x, 11 * 16 + 2, "lr6")
    # the three spurs: tongues of floor out to the warp (x..x+1, rows 9-10)
    for name, sx in SPURS.items():
        X = sx * 16
        def inside(x, y, X=X):
            # a tongue of rock: a rounded tip 16 px wide at the warp, widening
            # to the full two cells where it leaves the shelf
            dx, yy = x - X, y - 9 * 16
            if not (0 <= dx < 32) or yy < 0:
                return False
            if yy >= 32:
                return True
            half = 8 + yy * 8 / 31 + (1 if (yy // 6) % 2 and yy > 8 else 0)
            if yy < 4:
                half -= [4, 2, 1, 0.5][yy]
            return abs(dx - 15.5) <= half
        for y in range(9 * 16, 11 * 16):
            for x in range(X, X + 32):
                if not inside(x, y):
                    continue
                c = floor_px(x, y)
                if not inside(x, y - 1) or not inside(x - 1, y):
                    c = "lr7"
                elif not inside(x - 2, y) or not inside(x, y - 2):
                    c = "lr6"
                elif not inside(x + 1, y) or not inside(x + 2, y):
                    c = "lr3"
                B.px(x, y, c)
    # fallen rock and a few stalagmites along the south of the shelf: they
    # frame the walk and break its long straight edge (blocked cells)
    for (bx, by, kind) in BOULDERS:
        rows = ROCKS[kind]
        B.blit(rows, {"1": "lr1", "2": "lr2", "3": "lr3", "4": "lr4", "5": "lr5", "6": "lr6",
                      "7": "lr7"}, bx * 16, by * 16 + 16 - len(rows))
    # floor cells under the spurs lose their lip
    for sx in SPURS.values():
        for x in range(sx * 16 + 2, sx * 16 + 30):
            for y in range(11 * 16, 11 * 16 + 3):
                B.px(x, y, floor_px(x, y))
    # the east door: a rough arch in the end wall, the Omphalos stair's last
    # steps coming down out of the dark into the hall (x 33, rows 11-12)
    dx_, dy_ = EAST_DOOR
    X, Y = dx_ * 16, (dy_ - 1) * 16
    for y in range(Y, Y + 32):
        for x in range(X, X + 16):
            yy, xx = y - Y, x - X
            arch = 1 + (abs(xx - 7.5) ** 2) / 9
            if yy < arch or xx < 1 or xx > 14:
                continue
            if xx in (1, 2) or yy < arch + 1:
                c = "lr6" if xx < 3 else "lr5"
            elif xx in (13, 14):
                c = "lr1"
            elif yy < 12:
                c = "lr0"
            else:
                step = (yy - 12) // 5
                c = ("lr2", "lr3", "lr4", "lr5")[min(step, 3)] if (yy - 12) % 5 else "lr6"
            B.px(x, y, c)
    sc.walkable(1, 11, 32, 13)
    for (bx, by, kind) in BOULDERS:
        sc.walkable(bx, by, bx, by, on=False)
    for sx in SPURS.values():
        sc.walkable(sx, 9, sx + 1, 10)
    sc.walkable(*EAST_DOOR, *EAST_DOOR)


# --- the chains -------------------------------------------------------------

def chain_line(M, x0, y0, x1, y1, start=0):
    """Links every 4 px along the line, alternately a ring seen flat and one seen
    edge-on, with a glint on the upper left. Returns the number of links."""
    n = max(1, int(math.hypot(x1 - x0, y1 - y0) // 5))
    ang = math.atan2(y1 - y0, x1 - x0)
    along_x = abs(math.cos(ang)) > abs(math.sin(ang))
    for i in range(n + 1):
        t = i / n
        x = round(x0 + (x1 - x0) * t)
        y = round(y0 + (y1 - y0) * t)
        if (i + start) % 2 == 0:
            # a heavy ring seen flat, a hole in the middle, a cold glint
            M.blit([".aaa.", "aA.Aa", "a...a", "aA.Aa", ".aaa."],
                   {"a": "la1", "A": "la0"}, x - 2, y - 2)
            M.px(x - 1, y - 2, "la4")
            M.px(x - 2, y - 1, "la3")
            M.px(x - 2, y, "la2")
        else:
            if along_x:
                M.blit(["aaaaa", "bbbbb", "AAAAA"], {"a": "la3", "b": "la2", "A": "la0"}, x - 2, y - 1)
                M.px(x - 1, y - 1, "la4")
            else:
                M.blit(["abA", "abA", "abA", "abA", "abA"], {"a": "la3", "b": "la2", "A": "la0"},
                       x - 1, y - 2)
                M.px(x - 1, y - 2, "la4")
    return n


def chain_anchors():
    p = {
        "spinner": ((3 * 16 + 14, 6 * 16 + 8), (6 * 16 + 9, 9 * 16 - 3)),
        "measurer": ((16 * 16 + 8, 3 * 16 + 2), (16 * 16 + 8, 9 * 16 - 4)),
        "cutter": ((30 * 16 + 1, 6 * 16 + 8), (27 * 16 + 7, 9 * 16 - 3)),
    }
    return p


def paint_chains(sc):
    for name, (a, b) in chain_anchors().items():
        chain_line(sc.M, a[0], a[1], b[0], b[1])
        # the shackle at the anchor: a bronze-black staple
        sc.M.blit(["aaa", "a.a"], {"a": "la1"}, a[0] - 1, a[1] - 2)


def paint_broken_chains(sc):
    for name, (a, b) in chain_anchors().items():
        # a stub hangs from the anchor, four links, then the clean bright cut
        ax = a[0] + (5 if name == "spinner" else -5 if name == "cutter" else 0)
        chain_line(sc.M, ax, a[1], ax, a[1] + 18)
        sc.M.blit(["c.c", ".c."], {"c": "la4"}, ax - 1, a[1] + 21)
        if name != "measurer":
            chain_line(sc.M, a[0], a[1], ax, a[1])
        # the rest lies coiled on the spur, where she stood
        fx, fy = FATE_AT[name]
        cx, cy = fx * 16 + 8, fy * 16 + 20
        for k in range(14):
            ang = k * 1.1
            r = 2 + k * 0.55
            x = int(cx + r * math.cos(ang))
            y = int(cy + r * math.sin(ang) * 0.6)
            sc.M.blit([".a.", "aAa", ".a."], {"a": "la1", "A": "la3" if k % 3 == 0 else "la0"}, x - 1, y - 1)
        sc.M.blit(["c.c", ".c."], {"c": "la4"}, cx + 8, cy - 1)


# --- after the cut: the torn roof and the foot of the Stair ----------------------

def paint_after(sc):
    B, M = sc.B, sc.M
    # the roof at the west end is torn open on the sky: sky below, rock edge above
    hole = set()
    for x in range(0, 3 * 16):
        top = 0
        bot = 29 + int(2 * math.sin(x / 4.0) + 1.5 * math.sin(x / 1.7)) - max(0, x - 30) // 2
        for y in range(max(0, top), max(top, bot)):
            hole.add((x, y))
    for cy in (0, 1):
        for cx in range(0, 3):
            cells = [(x, y) for x in range(cx * 16, cx * 16 + 16) for y in range(cy * 16, cy * 16 + 16)]
            if not any(p in hole for p in cells):
                continue
            for (x, y) in cells:
                rock = B.get(x, y)
                B.px(x, y, "lk_hi" if y < 8 else "lk_md" if y < 18 else "lk_lo")
                if (x, y) not in hole and rock:
                    M.px(x, y, rock)
            # the torn rim catches the gray light
            for (x, y) in cells:
                if (x, y) not in hole and ((x, y + 1) in hole or (x, y - 1) in hole):
                    M.px(x, y, "lr6")
    # the stair: pale steps climbing the west wall from the shelf to the hole,
    # x 1-2, rows 2-11 (stone, middle layer over the rock)
    for y in range(2 * 16, 12 * 16):
        for x in range(1 * 16 + 2, 3 * 16 - 2):
            yy = (12 * 16 - 1 - y)
            step = yy % 8
            c = "ls6" if step == 7 else "ls5" if step >= 5 else "ls4" if step >= 2 else "ls2"
            if x in (1 * 16 + 2, 3 * 16 - 3):
                c = "ls1"
            elif x == 1 * 16 + 3:
                c = "ls7" if step >= 5 else "ls5"
            M.px(x, y, c)
    sc.walkable(1, 11, 2, 11)
    sc.walkable(2, 11, 2, 13)


def loom_scenes():
    before = Scene("loom_before", LOOM_W, LOOM_H)
    paint_rock(before)
    paint_cloth(before)
    paint_warp(before)
    paint_beam_posts(before)
    paint_chains(before)
    after = Scene("loom_after", LOOM_W, LOOM_H)
    paint_rock(after)
    paint_cloth(after)
    paint_warp(after)
    paint_beam_posts(after, after=True)
    paint_broken_chains(after)
    paint_after(after)
    return [before, after]


# --------------------------------------------------------------------------
# The Stair of Hours (24 x 110)
# --------------------------------------------------------------------------

STAIR_W, STAIR_H = 24, 110


def landing_rect(k):
    """(x0, x1, top row, face row) of hour-stone k (1-12)."""
    if k == 12:
        return 5, 18, 11, 16
    t = 100 - 8 * (k - 1)
    x0, x1 = (2, 10) if k % 2 else (13, 21)
    return x0, x1, t, t + 4


def flight_cells(k):
    """The cells of the flight up to landing k (from landing k-1, or from the foot
    for k = 1): [(row, x0)], each 3 wide, bottom row first. The top row cuts
    through landing k's face."""
    if k == 1:
        return [(108, 5), (107, 5), (106, 5), (105, 5), (104, 5)]
    x0, x1, t, face = landing_rect(k - 1)
    up = t - 1
    if k == 12:
        return [(up, 8), (up - 1, 10), (up - 2, 11), (up - 3, 11)]
    if (k - 1) % 2:   # from a west landing to an east one
        return [(up, 8), (up - 1, 10), (up - 2, 12), (up - 3, 13)]
    return [(up, 13), (up - 1, 11), (up - 2, 9), (up - 3, 8)]


def dial_cell(k):
    """The top-left cell of hour-stone k's sundial (2 x 2)."""
    if k == 12:
        return 9, 13
    x0, x1, t, face = landing_rect(k)
    return (x0 + x1) // 2 - 1, t + 1


ERA = {k: ("cyclopean" if k <= 4 else "ashlar" if k <= 8 else "marble") for k in range(1, 12)}
ERA[12] = "gold"
SHADOW = (12, 11)     # the Lord of Time's shadow: 3 x 2 from here


def paving(era, x, y):
    """Each era's floor, on a 16 px period: the hours climb through time's strata."""
    xx, yy = x % 16, y % 16
    if era == "cyclopean":
        # two big polygonal blocks a cell, dark joints, a worn high spot
        if (xx == 9 - yy // 4 and yy < 9) or (yy == 8 and xx >= 6) or (xx == 13 and yy > 8) or yy == 15:
            return "ls1"
        if (xx, yy) in ((2, 2), (3, 2), (2, 3), (10, 11), (11, 11)):
            return "ls4"
        return "ls3" if (xx // 2 + yy // 2) % 5 else "ls2"
    if era == "ashlar":
        # cut limestone in a running bond, two courses a cell
        course = yy // 8
        if yy % 8 == 7 or (xx == (3 if course else 11)):
            return "ls3"
        if yy % 8 == 0 or xx == (4 if course else 12):
            return "lsl1"
        return "lsl0" if (xx + yy) % 11 == 0 else "lsl1" if yy % 8 < 2 else "lsl0"
    # marble: one slab a cell, a fine joint, a soft vein; gold on the twelfth
    if xx == 15 or yy == 15:
        return "ls4"
    if xx == 0 or yy == 0:
        return "ls7"
    if era == "gold" and ((x // 16 + y // 16) % 3 == 0) and xx + yy in (13, 14) and 2 < xx < 13:
        return "lsg1" if xx % 3 else "lsg0"
    if (xx - yy) in (3, 4) and 3 < xx < 13:
        return "ls5"
    return "ls6"


def kerb(x, y, rx, ry, w, top):
    """The hour-stone's rim: a plain raised kerb one cell wide round its top,
    era-blind, so every landing shares it. rx, ry: pixels into the stone."""
    W = w * 16
    ex = min(rx, W - 1 - rx)
    west = rx < W // 2
    if (top and ry == 0) or ex == 0:
        return "ls1"
    if (top and ry == 1) or (ex == 1 and west):
        return "ls7"
    if ex == 1:
        return "ls3"
    inner_y = top and ry >= 13
    inner_x = 13 <= ex <= 15 and (rx < 16 or rx >= W - 16)
    if (inner_y and ry == 15) or (inner_x and ex == 15 and not west):
        return "ls3"
    if (inner_y and ry == 15) or (inner_x and ex == 15):
        return "ls3"
    if (inner_y and ry == 14) or (inner_x and ex == 14):
        return "ls4"
    if (inner_y and ry == 13) or (inner_x and ex == 13):
        return "ls6"
    return "ls5" if (x * 3 + y * 5) % 23 else "ls4"


GREEK = {  # 5 x 7 glyphs
    "A": ["..x..", ".x.x.", ".x.x.", "x...x", "xxxxx", "x...x", "x...x"],
    "B": ["xxxx.", "x...x", "x...x", "xxxx.", "x...x", "x...x", "xxxx."],
    "G": ["xxxxx", "x....", "x....", "x....", "x....", "x....", "x...."],
    "D": ["..x..", "..x..", ".x.x.", ".x.x.", "x...x", "x...x", "xxxxx"],
    "E": ["xxxxx", "x....", "x....", "xxxx.", "x....", "x....", "xxxxx"],
    "S": ["xxxxx", "x....", ".x...", "..x..", ".x...", "x....", "xxxxx"],   # stigma, drawn as sigma
    "Z": ["xxxxx", "....x", "...x.", "..x..", ".x...", "x....", "xxxxx"],
    "H": ["x...x", "x...x", "x...x", "xxxxx", "x...x", "x...x", "x...x"],
    "Q": [".xxx.", "x...x", "x...x", "x.x.x", "x...x", "x...x", ".xxx."],   # theta
    "I": ["x", "x", "x", "x", "x", "x", "x"],
}
NUMERAL = {1: "A", 2: "B", 3: "G", 4: "D", 5: "E", 6: "S", 7: "Z", 8: "H", 9: "Q", 10: "I",
           11: "IA", 12: "IB"}


def numeral(L, cx, cy, text):
    """The hour inlaid in gold in the face, with a dark cut under each stroke."""
    glyphs = [GREEK[ch] for ch in text]
    w = sum(len(g[0]) for g in glyphs) + (len(glyphs) - 1) * 2
    x = cx * 16 + (16 - w) // 2
    y = cy * 16 + 3
    for g in glyphs:
        for j, row in enumerate(g):
            for i, ch in enumerate(row):
                if ch == "x":
                    L.px(x + i, y + j + 1, "ls0")
        for j, row in enumerate(g):
            for i, ch in enumerate(row):
                if ch == "x":
                    L.px(x + i, y + j, "lsg1" if j < 3 else "lsg0")
        x += len(g[0]) + 2


def paint_dial(L, cx, cy, hour):
    """A sundial set in the stone, 2 x 2 cells: a bronze rim, a marble face with
    twelve hour marks (the quarters in gold), the gnomon, and its long shadow
    stopped at `hour` (12 at the top)."""
    X, Y = cx * 16 + 16, cy * 16 + 16
    for y in range(cy * 16, cy * 16 + 32):
        for x in range(cx * 16, cx * 16 + 32):
            dx, dy = x + 0.5 - X, y + 0.5 - Y
            d = math.hypot(dx, dy)
            if d < 11.5:
                c = "ls7" if dx + dy < -6 else "ls6"
            elif d < 12.5:
                c = "ls4"
            elif d < 14:
                c = "lsg1" if dy < -2 else "lsg0"
            elif d < 15.2:
                c = "lsg0" if dy < 4 else "ls1"
            elif d < 16 and dy > 0:
                c = "ls1"     # the dial's own shadow on the floor
            else:
                continue
            L.px(x, y, c)
    for h in range(12):
        a = math.radians(h * 30 - 90)
        for r in ((9.5, 10.5) if h % 3 == 0 else (10.2,)):
            L.px(math.floor(X + r * math.cos(a)), math.floor(Y + r * math.sin(a)),
                 "lsg0" if h % 3 == 0 else "ls3")
    a = math.radians(hour * 30 - 90)
    for r in range(2, 10):
        L.px(math.floor(X + r * math.cos(a)), math.floor(Y + r * math.sin(a)), "ls2")
        if r < 8:
            L.px(math.floor(X + r * math.cos(a) + 0.7 * math.sin(a)),
                 math.floor(Y + r * math.sin(a) - 0.7 * math.cos(a)), "ls3")
    L.blit([".k.", "kgk", ".k."], {"k": "ls0", "g": "lsg1"}, X - 2, Y - 2)


# Cloud puffs and streaks, on the sky band they sit in (w white, p pink, s shade)
CLOUDS = {
    "puff": ["...................wwwww......................",
             ".................wwwwwwwww.....................",
             "..........www...wwwwwwwwwwww...................",
             "........wwwwwwwwwwwwwwwwwwwww..wwww............",
             ".......wwwwwwwwwwwwwwwwwwwwwwwwwwwwww..........",
             "......wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww........",
             "...wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww......",
             "..wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww....",
             ".wwwwwwwwwppwwwwwwwwwwwwwwwwwwppwwwwwwwwwwwww..",
             "wwwwwwwppppppwwwwwwwwwwwwwwwpppppwwwwwwwwwwwww.",
             ".wpppppppppppppppwwwwwwpppppppppppppppwwwwwppp.",
             "..ppppppppppppppppppppppppppppppppppppppppppp..",
             "...pppppssssspppppppppppppssssssppppppppssss...",
             ".....sssss...sssssppppsssss....ssssssssss......",
             "...................ssss........................"],
    "streak": ["................................",
               "..........wwwwww................",
               "......wwwwppppwwwwww............",
               "..wwwwpppppppppppppwwwww........",
               "...ppppppps....ppppppppwwwwww...",
               "........ssss............pppp....",
               "................................",
               "................................",
               "................................"],
}
CLOUD_AT = [("streak", 1, 3), ("puff", 17, 6), ("streak", 18, 26), ("puff", 0, 31),
            ("streak", 17, 46), ("puff", 1, 55), ("streak", 18, 68), ("puff", 17, 79),
            ("streak", 0, 86), ("puff", 18, 92)]
SKY_BANDS = [(0, "lk_hi"), (38, "lk_md"), (78, "lk_lo")]


def sky_color(x, y):
    """Three bands, each meeting the next over two rows of dither."""
    row = y // 16
    prev = SKY_BANDS[0][1]
    for start, col in SKY_BANDS[1:]:
        if row < start - 2:
            return prev
        if row < start:
            frac = 0.25 if row == start - 2 else 0.6
            return col if ((x // 2) * 7 + (y // 2) * 3) % 8 < frac * 8 else prev
        prev = col
    return prev


CLOUD_TOP = 97


def cloud_px(x, y):
    """The cloud sea below everything, on a 32 px period: billows lit gold on
    top, pink below, a shade line between rolls. None above its top edge."""
    xx = x % 32
    top = CLOUD_TOP * 16 + 6 + int(5 - 5 * math.sin(math.pi * xx / 32) ** 0.6)
    if y < top:
        return None
    yy = y - top
    if yy < 1:
        return "lcl3"
    if yy < 3:
        return "lcg"
    if yy < 7:
        return "lcl2"
    # deeper down: soft banks, a few long lit crests and shade lines, on a
    # 64 x 48 period so the eye doesn't find a lattice
    py = (y - CLOUD_TOP * 16) % 48
    px = x % 64
    crest = [(10, 6, 30), (26, 36, 60), (40, 2, 22)]
    for cy0, a, b in crest:
        if a <= px < b:
            arc = int(3 * math.sin(math.pi * (px - a) / (b - a)))
            if py == cy0 - arc:
                return "lcl3" if (px - a) < (b - a) // 2 else "lcl2"
            if py == cy0 - arc + 1:
                return "lcl2"
            if py == cy0 - arc - 1 and (px - a) % 6 < 4:
                return "lcl0"
    return "lcl1"


def paint_sky(sc):
    B = sc.B
    for y in range(0, STAIR_H * 16):
        for x in range(0, STAIR_W * 16):
            c = cloud_px(x, y) if y >= CLOUD_TOP * 16 else None
            B.px(x, y, c or sky_color(x, y))
    for name, wx, wy in CLOUD_AT:
        for j, r in enumerate(CLOUDS[name]):
            for i, ch in enumerate(r):
                col = {"w": "lcl3", "p": "lcl2", "s": "lcl1"}.get(ch)
                if col:
                    B.px(wx * 16 + i, wy * 16 + 3 + j, col)


def paint_landing(sc, k):
    B, M = sc.B, sc.M
    x0, x1, t, face = landing_rect(k)
    w = x1 - x0 + 1
    era = ERA[k]
    for y in range(t * 16, face * 16):
        for x in range(x0 * 16, (x1 + 1) * 16):
            rx, ry = x - x0 * 16, y - t * 16
            cx, cy = x // 16, y // 16
            ring = cx in (x0, x1) or cy == t
            if ring:
                if cy == t and cx in (x0, x1):
                    ex = rx if cx == x0 else (w * 16 - 1 - rx)
                    if ry < 3 and ex < [3, 1, 1][ry]:
                        continue
                c = kerb(x, y, rx, ry, w, top=(cy == t))
                (M if cy == t and cx in (x0, x1) else B).px(x, y, c)
            else:
                B.px(x, y, paving(era, x, y))
    # the face: era-blind stone with its numeral, rounded at the foot of its ends
    for y in range(face * 16, face * 16 + 16):
        for x in range(x0 * 16, (x1 + 1) * 16):
            yy = y - face * 16
            rx = x - x0 * 16
            ex = min(rx, w * 16 - 1 - rx)
            if yy >= 12 and ex < (yy - 11) * 2:
                continue
            if yy == 0:
                c = "ls4"
            elif yy == 1:
                c = "ls3"
            elif yy >= 13:
                c = "ls1"
            elif yy == 12:
                c = "ls1"
            else:
                c = "ls2" if ((x % 16) // 4 + yy // 3) % 4 else "ls1"
            if ex == 0:
                c = "ls1"
            elif ex == 1 and rx < 8:
                c = "ls4"
            M.px(x, y, c)
    numeral(M, (x0 + x1) // 2, face, NUMERAL[k])
    # the broken underside, a row deeper: rough rock tapering to a point
    for x in range(x0 * 16, (x1 + 1) * 16):
        rx = x - x0 * 16
        ex = min(rx, w * 16 - 1 - rx)
        depth = [12, 13, 13, 14, 15, 15, 14, 12, 11, 11, 12, 14, 16, 16, 15, 13][x % 16]
        depth = min(depth, max(0, ex // 2 - 1))
        for yy in range(depth):
            y = (face + 1) * 16 + yy
            c = "ls2" if yy < 2 else "ls1" if yy < depth - 1 else "ls0"
            if yy == 3 and (x % 16) in (3, 4, 11):
                c = "ls2"
            M.px(x, y, c)
    sc.walkable(x0, t, x1, face - 1)
    dx, dy = dial_cell(k)
    paint_dial(M, dx, dy, k % 12)
    sc.walkable(dx, dy, dx + 1, dy + 1, on=False)


def paint_flight(sc, k, ghost=False):
    """The flight up to landing k: steps 3 cells wide, fully drawn on the middle
    layer (over the sky, the underside or the face they cut through), so every
    flight shares the same few metatiles."""
    M = sc.M
    for (row, x0) in flight_cells(k):
        stony = {cx: bool((M.a[row * 16:row * 16 + 16, cx * 16:cx * 16 + 16, 3] > 0).any())
                 for cx in range(x0, x0 + 3)}
        if not ghost:
            sc.clear(M, x0, row, x0 + 2, row)
        for y in range(row * 16, row * 16 + 16):
            yy = y - row * 16
            for x in range(x0 * 16, x0 * 16 + 48):
                rx = x - x0 * 16
                if ghost:
                    # on the sky the unformed steps are pale outlines; where they
                    # cross a face they are scratched into the stone
                    stone = stony[x // 16]
                    if yy % 8 == 0 and 2 <= rx <= 45:
                        c = "ls6" if stone else "lgh1"
                    elif rx in (2, 45) or (yy % 8 == 1 and 3 <= rx <= 44 and (rx // 2) % 2):
                        c = "ls4" if stone else "lgh0"
                    else:
                        continue
                else:
                    tread = yy % 8
                    c = "ls6" if tread == 0 else "ls5" if tread < 4 else "ls3" if tread < 6 else "ls2"
                    if rx < 1 or rx > 46:
                        c = "ls0"
                    elif rx == 1:
                        c = "ls7" if tread < 4 else "ls4"
                    elif rx == 46:
                        c = "ls1"
                M.px(x, y, c)
        sc.walkable(x0, row, x0 + 2, row, on=not ghost)


def paint_foot(sc):
    """The foot: the top of the split Omphalos rising out of the cloud. The egg
    has broken in two along a jagged seam, its halves leaning apart in their net
    of knotted wool, and the stair comes up out of the crack between them. Row
    109 is the way back down (a south arrow warp)."""
    M = sc.M
    CX, CY, RX, RY = 6.5 * 16, 108.8 * 16, 5.6 * 16, 3.8 * 16
    for y in range(105 * 16, 110 * 16):
        for x in range(0, 13 * 16):
            dx, dy = (x + 0.5 - CX) / RX, (y + 0.5 - CY) / RY
            r2 = dx * dx + dy * dy
            if r2 > 1.0:
                continue
            # the crack: a jagged gap down the middle, wider at the top
            seam = 16 + 3 * math.sin(y / 5.0) + max(0, (106.5 * 16 - y)) * 0.25
            if abs(x + 0.5 - CX) < seam:
                continue
            west = x < CX
            c = "ls5" if dx < -0.45 else "ls4" if dx < 0.25 else "ls3"
            if dy < -0.75:
                c = "ls6" if west else "ls5"
            u, v = (x + y) % 10, (x - y) % 10
            if u == 0 or v == 0:
                c = "lsl0" if c in ("ls5", "ls6") else "ls2"
            if u == 0 and v == 0:
                c = "lsg1" if west else "lsg0"
            if r2 > 0.9 or abs(x + 0.5 - CX) < seam + 1.5:
                c = "ls1"
            M.px(x, y, c)
    # the crack below the first step: dark, going down
    for y in range(109 * 16, 110 * 16):
        for x in range(5 * 16, 8 * 16):
            M.px(x, y, "ls0" if (y - 109 * 16) > 3 or (x // 2) % 3 else "ls1")
    sc.walkable(5, 109, 7, 109)


def paint_shadow_block(sc):
    """The Lord of Time's shadow on the twelfth landing's top edge (3 x 2)."""
    sx, sy = SHADOW
    dark = {"ls7": "ls4", "ls6": "ls3", "ls5": "ls3", "ls4": "ls2", "ls3": "ls2", "ls2": "ls1",
            "lsg1": "lsg0", "lsg0": "ls2", "ls1": "ls0"}
    for y in range(sy * 16, (sy + 2) * 16):
        for x in range(sx * 16, (sx + 3) * 16):
            rx, ry = x - sx * 16, y - sy * 16
            if ((rx - 23.5) / 23) ** 2 + ((ry - 14) / 15) ** 2 > 1.0:
                continue
            base = sc.B.get(x, y)
            if base in dark:
                sc.B.px(x, y, dark[base])


def paint_gold_ring(sc):
    """The twelfth landing's dial sits in a ring of gold inlay (4 x 4 round it),
    twelve gold rays running out to it."""
    dx, dy = dial_cell(12)
    X, Y = dx * 16 + 16, dy * 16 + 16
    for y in range((dy - 1) * 16, (dy + 3) * 16):
        for x in range((dx - 1) * 16, (dx + 3) * 16):
            if dx <= x // 16 <= dx + 1 and dy <= y // 16 <= dy + 1:
                continue
            d = math.hypot(x + 0.5 - X, y + 0.5 - Y)
            if 27 < d < 29.5:
                sc.B.px(x, y, "lsg1" if y < Y else "lsg0")
            elif 29.5 <= d < 30.5:
                sc.B.px(x, y, "ls4")
            elif 17 < d <= 27:
                ang = math.degrees(math.atan2(y + 0.5 - Y, x + 0.5 - X)) % 30
                if ang < 1.6 or ang > 28.4:
                    sc.B.px(x, y, "lsg0")


def stair_scenes():
    base = Scene("stair", STAIR_W, STAIR_H)
    paint_sky(base)
    for k in range(1, 13):
        paint_landing(base, k)
    paint_gold_ring(base)
    paint_shadow_block(base)
    paint_foot(base)
    full = base.copy("stair")
    for k in range(1, 13):
        paint_flight(full, k)
    ghost = base.copy("stair_ghost")
    for k in range(1, 13):
        paint_flight(ghost, k, ghost=k in (1, 5, 9))
    fallen = base.copy("stair_fallen")
    paint_flight(fallen, 1)
    return [full, ghost, fallen]


def all_scenes():
    return loom_scenes() + stair_scenes()


# --------------------------------------------------------------------------
# Slicing into metatiles
# --------------------------------------------------------------------------

class Struct(E.Struct):
    def __init__(self, key, title, w, h, walk=None, notes="", section="cells"):
        super().__init__(key, title, w, h, walk=walk, notes=notes, ground="none", section=section)
        self.names = {}


def slice_scenes(scenes):
    """Every distinct cell (bottom, middle, behavior) across the scenes -> one
    1x1 Struct; returns (structs, {scene name: [[struct index]]})."""
    seen, structs, grids = {}, [], {}
    for sc in scenes:
        grid = []
        for cy in range(sc.h):
            row = []
            for cx in range(sc.w):
                b, m = sc.cell(cx, cy)
                beh = sc.beh.get((cx, cy), "")
                key = (b.tobytes(), m.tobytes(), beh)
                if key not in seen:
                    s = Struct(f"c{len(structs):03d}", f"{sc.name} ({cx},{cy})", 1, 1,
                               walk=["." if sc.walk[cy][cx] == "." else "X"])
                    s.B.a[:] = b
                    s.M.a[:] = m
                    if beh:
                        s.behaviors[(0, 0)] = beh
                    s.first = (sc.name, cx, cy)
                    seen[key] = len(structs)
                    structs.append(s)
                row.append(seen[key])
            grid.append(row)
        grids[sc.name] = grid
    return structs, grids


def validate(structs):
    problems = []
    for s in structs:
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    cols = tile_colors(layer, tx, ty)
                    if cols and not any(cols <= g for g in GROUP_RGB.values()):
                        names = sorted(K.RGB2NAME.get(c, str(c)) for c in cols)
                        problems.append(f"{s.key} {s.title} {ln} tile ({tx},{ty}) mixes groups: {names}")
        if not (s.B.a[..., 3] > 0).all():
            problems.append(f"{s.key} {s.title}: bottom layer isn't opaque")
    return problems


SHEET_ROWS = 64


def pack(structs):
    rows = 0
    for i, s in enumerate(structs):
        col, row = i % 8, i // 8
        s.origin = (col, row)
        s.ids = [[0x200 + row * 8 + col]]
        rows = row + 1
    assert rows <= SHEET_ROWS, f"{len(structs)} metatiles: more than a secondary holds"
    return rows
