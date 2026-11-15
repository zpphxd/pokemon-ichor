#!/usr/bin/env python3
"""Draw the evolution scene's background: a black-figure radiance.

Behind the evolving Pokemon, rays burst from the centre and nested frames of
meander ring it, all in black glaze; the engine's light runs through them as
terracotta and gold, the colors of the battle intro's pottery transitions.

How the engine animates it (src/evolution_scene.c, unchanged):
  - bg.png's tiles are drawn on two layers, bg_inner.bin on BG1 and
    bg_outer.bin on BG2, blended half and half, each circling 4 px out of phase.
  - Every pixel's index (1-13) is a step outward from the centre. The
    animation (sBgAnim_PalIndexes) lights the steps in a wave that runs out
    and back, through the ramp in bg_anim.pal: 0 dark ... 13 brightest.
So this script paints each layer as a field of steps: the inner layer's steps
are an eight-pointed star of rays, the outer layer's are square frames with a
meander in each, raised a step so the key lights a moment before its frame.

Writes graphics/evolution_scene/: bg.png, bg_inner.bin, bg_outer.bin,
bg_anim.pal; and design/phase1/img/ui_evolution_bg.png.

Usage: python3 tools/ichor/art/ui_evolution_bg.py
"""
import math

import numpy as np

from ui_menus_lib import ROOT, TileSet, write_tiles_png, write_jasc, save_rgb, MEANDER

OUT = ROOT / "graphics/evolution_scene"
IMG = ROOT / "design/phase1/img"
CX, CY = 128, 80       # the radiance's centre on the 256x256 map: the screen's (120, 64)
STEPS = 13

# The light ramp: black glaze through terracotta to pale gold.
RAMP = [
    (24, 16, 16), (40, 24, 24), (64, 32, 24), (88, 40, 24), (120, 48, 24), (152, 64, 32),
    (184, 88, 48), (208, 112, 64), (224, 136, 88), (232, 160, 80), (240, 184, 72),
    (240, 200, 96), (248, 216, 136), (248, 232, 184),
]
PAL = [(0, 0, 0)] + RAMP[1:] + [(0, 0, 0)] * 2   # index 0 is transparent in the tiles


def inner():
    """An eight-pointed star of rays: each step is the union of a square and a
    longer diamond, so four rays run along the axes and four between them.
    Its edges are straight lines at 0, 45 and 90 degrees, which repeat from
    tile to tile, so the whole star costs few tiles."""
    a = np.zeros((256, 256), np.uint8)
    for y in range(256):
        for x in range(256):
            dx, dy = abs(x - CX + 0.5), abs(y - CY + 0.5)
            d = min(max(dx, dy), (dx + dy) / 1.6)
            a[y, x] = min(STEPS, 1 + int(d / 9))
    return a


def outer():
    """Square frames, each carrying a meander that sits a step ahead of it."""
    a = np.zeros((256, 256), np.uint8)
    for y in range(256):
        for x in range(256):
            dx, dy = x - CX + 0.5, y - CY + 0.5
            d = max(abs(dx), abs(dy))
            step = int(d / 10)
            band = d - step * 10            # 0..10 across this frame
            v = 1 + step
            # the meander runs round the frame on its middle five pixels
            if 2.5 <= band < 7.5:
                along = int(abs(dx) if abs(dy) > abs(dx) else abs(dy))
                row = MEANDER[int(band - 2.5)]
                if row[along % 8] == "#":
                    v += 1
            a[y, x] = min(STEPS, v)
    return a


def write():
    ia, oa = inner(), outer()
    ts = TileSet(reserved=1)
    maps = []
    for a in (ia, oa):
        m = np.zeros((32, 32), np.uint16)
        for ty in range(32):
            for tx in range(32):
                i, f = ts.add(a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8])
                m[ty, tx] = i | f | (10 << 12)
        maps.append(m)
    n = len(ts.tiles)
    print(f"evolution background: {n} tiles")
    assert n <= 224, n
    write_tiles_png(OUT / "bg.png", ts.tiles, [PAL], tiles_wide=16, min_tiles=224)
    (OUT / "bg_inner.bin").write_bytes(maps[0].astype("<u2").tobytes())
    (OUT / "bg_outer.bin").write_bytes(maps[1].astype("<u2").tobytes())
    print("wrote graphics/evolution_scene/bg_inner.bin, bg_outer.bin")
    write_jasc(OUT / "bg_anim.pal", RAMP + [(0, 0, 0)] * (32 - len(RAMP)))
    preview(ia, oa)


def preview(ia, oa):
    """Three moments of the wave, both layers blended, at the screen's view."""
    frames = []
    for peak in (5, 9, 13):
        lit = []
        for a in (ia, oa):
            v = np.abs(a.astype(int) - peak)
            level = np.clip(13 - v * 2, 0, 13)
            lit.append(np.array(RAMP, np.int32)[level])
        rgb = ((lit[0] + lit[1]) // 2).astype(np.uint8)
        frames.append(rgb[16:176, 8:248])
    save_rgb(IMG / "ui_evolution_bg.png", np.hstack(frames), 2)


# The sparks that ring and rain on the evolving Pokemon (graphics/misc/evo_sparkle.png,
# src/evolution_graphics.c). Emerald's were plain white dots. Here each is a
# four-pointed gold spark, white-hot at the heart, with ink at its tips so it
# still reads once the light behind it turns gold. The engine shrinks it with
# affine matrices, so the heart stays at the tile's centre.
SPARK = [
    "...k....",
    "...o....",
    "..kgk...",
    "kogWgok.",
    "..kgk...",
    "...o....",
    "...k....",
    "........",
]
SPARK_PAL = [(0, 0, 0), (32, 24, 24), (200, 144, 40), (240, 192, 64), (248, 248, 216)] + [(0, 0, 0)] * 11


def write_sparkle():
    key = {".": 0, "k": 1, "o": 2, "g": 3, "W": 4}
    a = np.array([[key[ch] for ch in row] for row in SPARK], np.uint8)
    write_tiles_png(ROOT / "graphics/misc/evo_sparkle.png", [a], [SPARK_PAL], tiles_wide=1)


if __name__ == "__main__":
    write()
    write_sparkle()
