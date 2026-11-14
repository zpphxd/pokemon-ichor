#!/usr/bin/env python3
"""Paint the stage of Daphne's new-game speech: the Akademia's laurel grove
at dawn, painted like a vase.

A meander frieze runs along the top. Under a night of black glaze the dawn
comes up behind the grove: rose, then terracotta, then gold at the horizon,
with the laurels standing against it in black-figure. Daphne, Smoliv and the
hero stand on the dark ground in a pool of sunlight, which grows from its
centre when someone steps onto it and shrinks away when they leave.

How the engine draws it (src/main_menu.c, the Birch speech; unchanged):
  BG1  this picture: shadow.png's tiles, map.bin (32x20), palettes 0 and 1
       from bg0.pal and bg1.pal. It slides 60 px right while the hero is
       chosen, so the picture wraps round its 256 px width.
  The pool of light is palette 0's colors 1-8, centre to rim. The engine
  loads them from bg2.pal at an offset that steps 8 -> 0 to light it and
  0 -> 8 to put it out: entries 0-7 are the lit pool, 8-15 the bare ground.

Writes graphics/birch_speech/: shadow.png, map.bin, bg0.pal, bg1.pal, bg2.pal;
and design/phase1/img/ui_speech_bg.png.

Usage: python3 tools/ichor/art/ui_speech_bg.py
"""
import math

import numpy as np

from ui_menus_lib import (ROOT, INK, CLAY_DARK, CLAY, CLAY_LIGHT, GOLD, GOLD_PALE, PARCHMENT,
                          MEANDER, TileSet, compile_map, write_tiles_png, write_jasc,
                          render_map, save_rgb, pal16)

OUT = ROOT / "graphics/birch_speech"
IMG = ROOT / "design/phase1/img"
W, H = 256, 160

EARTH = (64, 40, 32)
LIGHT = [   # the pool of sunlight, centre to rim
    (248, 232, 176), (248, 216, 136), (240, 192, 96), (232, 168, 80),
    (216, 136, 72), (184, 104, 56), (144, 72, 48), (104, 56, 40),
]
GRADIENT = LIGHT + [EARTH] * 8

P0 = pal16([
    (32, 24, 24),        # 0  backdrop
    *LIGHT,              # 1-8 the pool (rewritten at run time from bg2.pal)
    EARTH,               # 9  the ground
    INK,                 # 10
    CLAY_DARK,           # 11
    CLAY,                # 12
    CLAY_LIGHT,          # 13
    GOLD,                # 14
    (88, 56, 40),        # 15 the ground, lit along the horizon
])
P1 = pal16([
    (32, 24, 24),        # 0
    INK,                 # 1  the laurels, black-figure
    (40, 24, 40),        # 2  night
    (64, 32, 56),        # 3
    (104, 48, 64),       # 4  rose
    (152, 64, 56),       # 5
    CLAY,                # 6  terracotta
    CLAY_LIGHT,          # 7
    (240, 168, 80),      # 8
    GOLD,                # 9
    GOLD_PALE,           # 10 the horizon's brightest
    PARCHMENT,           # 11 stars
    CLAY_DARK,           # 12 the frieze's shade
    (64, 40, 32),        # 13 earth (the trees' feet)
])
A = dict(ink=16 + 1, night=16 + 2, n2=16 + 3, rose=16 + 4, r2=16 + 5, clay=16 + 6,
         clay_lt=16 + 7, amber=16 + 8, gold=16 + 9, gold_pale=16 + 10, star=16 + 11,
         clay_dk=16 + 12, earth=16 + 13)
G = dict(earth=9, ink=10, clay_dk=11, clay=12, clay_lt=13, gold=14, earth_lt=15)

HORIZON = 80          # on a tile boundary: the sky is palette 1, the ground palette 0
POOL_X, POOL_Y, POOL_RX, POOL_RY = 120, 95, 66, 13   # where the vanilla spotlight was


def sky(a):
    """Night above, dawn toward the horizon, in dithered bands."""
    bands = [(10, "night"), (36, "n2"), (48, "rose"), (58, "r2"), (66, "clay"), (72, "clay_lt"),
             (76, "amber"), (79, "gold"), (HORIZON, "gold_pale")]
    for y in range(10, HORIZON):
        for x in range(W):
            for i, (y1, c) in enumerate(bands):
                if y < y1:
                    break
            prev = bands[i - 1][1] if i > 0 else c
            # a two-row checker where one band meets the next
            if y >= y1 - 2 and (x + y) % 2 == 0 and i + 1 < len(bands):
                c = bands[i + 1][1]
            a[y, x] = A[c]
    # a few stars still out in the west of the sky
    for (x, y) in [(20, 18), (52, 26), (90, 14), (150, 22), (186, 31), (232, 16), (122, 34), (70, 36)]:
        a[y, x] = A["star"]


def frieze(a):
    a[0:10, :] = A["clay"]
    a[0, :] = A["ink"]
    for j, row in enumerate(MEANDER):
        for x in range(W):
            if row[x % 8] == "#":
                a[2 + j, x] = A["ink"]
    a[8, :] = A["clay_dk"]
    a[9, :] = A["ink"]


def laurel(a, x0, h, spread):
    """A laurel tree in black-figure: a trunk and a crown of leafy masses."""
    base = HORIZON
    for y in range(base - h // 2, base):
        for x in range(x0 - 1, x0 + 2):
            a[y, x % W] = A["ink"]
    rnd = np.random.RandomState(x0 * 7 + h)
    for k in range(9):
        cx = x0 + int(rnd.randint(-spread, spread + 1))
        cy = base - h + int(rnd.randint(0, h // 2))
        rx, ry = rnd.randint(6, 11), rnd.randint(4, 7)
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 and y < base:
                    a[y, x % W] = A["ink"]
    # leaves breaking the crown's edge, so it reads as foliage, not a cloud
    for k in range(60):
        x = x0 + int(rnd.randint(-spread - 10, spread + 11))
        y = base - h + int(rnd.randint(-3, h // 2 + 6))
        near = any(0 <= y + dy < H and a[y + dy, (x + dx) % W] == A["ink"]
                   for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)))
        if 10 < y < base and a[y, x % W] != A["ink"] and near:
            for (dx, dy) in [(0, 0), (1, 0), (0, 1)]:
                if 10 < y + dy < base:
                    a[y + dy, (x + dx) % W] = A["ink"]


def ground(a):
    for y in range(HORIZON, H):
        for x in range(W):
            a[y, x] = G["earth"]
    a[HORIZON, :] = G["ink"]
    a[HORIZON + 1, :] = G["earth_lt"]
    # the exergue under the scene: a clay band with the meander, as on a vase
    for y in range(108, 118):
        a[y, :] = G["clay"]
    a[108, :] = G["ink"]
    for j, row in enumerate(MEANDER):
        for x in range(W):
            if row[x % 8] == "#":
                a[110 + j, x] = G["ink"]
    a[117, :] = G["ink"]
    # the pool of sunlight: palette 0's colors 1 (centre) to 8 (rim)
    for y in range(POOL_Y - POOL_RY - 1, POOL_Y + POOL_RY + 2):
        for x in range(POOL_X - POOL_RX - 1, POOL_X + POOL_RX + 2):
            e = math.sqrt(((x - POOL_X + 0.5) / POOL_RX) ** 2 + ((y - POOL_Y + 0.5) / POOL_RY) ** 2)
            if e <= 1 and HORIZON + 1 < y < 108:
                ring = 1 if e < 0.55 else min(8, 2 + int((e - 0.55) / 0.065))
                a[y, x] = ring


def paint():
    a = np.zeros((H, W), np.uint8)
    sky(a)
    for (x, h, s) in [(18, 58, 14), (236, 50, 12), (96, 30, 8), (176, 36, 9)]:
        laurel(a, x, h, s)
    frieze(a)
    ground(a)
    return a


def write():
    a = paint()
    ts = TileSet(reserved=1)

    class Cv:
        def __init__(self, a):
            self.a, self.w, self.h = a, a.shape[1], a.shape[0]
    m = compile_map(Cv(a), ts, 32, 20, region=(0, 0, 32, 20))
    n = len(ts.tiles)
    assert n <= 448, n
    print(f"speech background: {n} tiles")
    write_tiles_png(OUT / "shadow.png", ts.tiles, [P0, P1], tiles_wide=16)
    (OUT / "map.bin").write_bytes(m.astype("<u2").tobytes())
    print("wrote graphics/birch_speech/map.bin")
    write_jasc(OUT / "bg0.pal", P0)
    write_jasc(OUT / "bg1.pal", P1)
    write_jasc(OUT / "bg2.pal", GRADIENT)
    # previews: the pool lit, half lit, and dark
    shots = []
    for i in (0, 4, 8):
        p0 = list(P0)
        p0[1:9] = GRADIENT[i:i + 8]
        shots.append(render_map(m, ts.tiles, [p0, P1], 30, 20))
    save_rgb(IMG / "ui_speech_bg.png", np.hstack(shots), 2)


if __name__ == "__main__":
    write()
