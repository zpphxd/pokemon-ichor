#!/usr/bin/env python3
"""The Gigas trainer portrait (TRAINER_PIC_ICHOR_GIGAS), 64x64, 15 colors.

    /usr/bin/python3 tools/ichor/art/portrait_gigas.py [--write] [--preview DIR]

The giants serve the Titans, and they are built like the Titanborn soldier,
only more so, so the portrait is made from the approved Titanborn portrait
(graphics/trainers/front_pics/titan_grunt.png, the model-led cast art) by a
fixed list of recolors and repaints, replayed every run (STYLE.md §3.4):

  * the crest turns black and stands one row taller, with a cool sheen on the
    lit side, the "tall black crest" of the gigas walker (walker_paint.py)
  * the blue tunic's upper half becomes a cuirass of bronze scales: a darker,
    greener bronze than the skin's ramp, so the chest can't read as bare,
    laid in offset rows with a lit top and a dark lower curve on each scale
  * the lower half becomes a kilt of dark leather strips (pteruges)

The blue ramp's three slots become the scale ramp, and the dark ink that
only the tunic used becomes the crest's sheen, so the palette stays at 15.
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
SRC = os.path.join(ROOT, "graphics/trainers/front_pics/titan_grunt.png")
OUT = os.path.join(ROOT, "graphics/trainers/front_pics/ichor_gigas.png")

# the source's slots: 1-3 inks, 4 5 7 the tunic's blue (dark, mid, light),
# 6 the darkest red, 8 9 leather, 10 the crest red, 11-15 bronze and skin
CREST_SHEEN, SCALE_D, SCALE_M, SCALE_L, CREST_D, CREST_M = 3, 4, 5, 7, 6, 10
NEW_COLORS = {
    CREST_SHEEN: (104, 104, 120),
    SCALE_D: (88, 64, 24),
    SCALE_M: (144, 104, 32),
    CREST_D: (32, 24, 32),
    SCALE_L: (200, 152, 56),
    CREST_M: (56, 56, 72),
}
BLUE = (4, 5, 7)
BELT_ROW = 29          # the tunic's belt line: scales above, leather strips below


def build():
    src = Image.open(SRC)
    a = np.array(src).astype(np.int32)
    pal = src.getpalette()[:48]
    pal = [tuple(pal[i * 3:i * 3 + 3]) for i in range(16)]
    blue = np.isin(a, BLUE)
    # the Titanborn's bronze sickle badge on the chest goes under the scales
    badge = np.zeros_like(blue)
    badge[22:28, 34:40] = True
    badge &= (a >= 11)
    a = a.copy()
    a[badge] = 5
    blue |= badge
    out = a.copy()
    out[a == 3] = 2            # the tunic's darkest ink merges into the next, freeing slot 3

    # the crest: everything red on the helmet's top, and the dark top edge and
    # bronze-lit tufts in its first rows
    H, W = a.shape
    for y in range(0, 13):
        for x in range(26, 46):
            v = a[y, x]
            if v == 10:
                out[y, x] = CREST_M
            elif y <= 6 and v in (8, 9):
                out[y, x] = CREST_D
            elif y <= 5 and v in (12, 13):
                out[y, x] = CREST_SHEEN
    # one row taller: a new dark top edge over the old one, which turns to sheen
    for x in range(32, 36):
        out[1, x] = CREST_D
        out[2, x] = CREST_SHEEN if x < 34 else CREST_M
    out[2, 31] = out[2, 36] = CREST_D

    # the cuirass of scales
    level = {4: 1, 5: 1, 7: 2, 3: 0}
    ramp = [2, SCALE_D, SCALE_M, SCALE_L]
    for y in range(H):
        for x in range(W):
            if not blue[y, x] and not (a[y, x] == 3 and y < BELT_ROW + 1):
                continue
            if y < BELT_ROW:
                lv = level[a[y, x]]
                cx = (x + 2 * ((y // 2) % 2)) % 4
                if y % 2 == 1 and cx in (0, 3):
                    lv -= 1                       # the lower curve of each scale
                elif y % 2 == 0 and cx == 1:
                    lv += 1                       # its lit top
                out[y, x] = ramp[max(0, min(3, lv))]
            elif y == BELT_ROW or y == BELT_ROW + 1:
                out[y, x] = 9 if a[y, x] == 7 else 8     # the leather belt
            elif blue[y, x]:
                lv = level[a[y, x]]
                if x % 3 == 0:
                    lv -= 1                       # the gaps between the strips
                out[y, x] = [2, 2, 6, 8][max(0, min(3, lv))]

    for i, c in NEW_COLORS.items():
        pal[i] = c
    assert all(v % 8 == 0 for c in pal for v in c), pal
    return out.astype(np.uint8), pal


def save(arr, pal, path):
    im = Image.fromarray(arr, "P")
    im.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    im.save(path, bits=4, transparency=0)


def rgba(arr, pal):
    out = np.zeros(arr.shape + (4,), np.uint8)
    m = arr != 0
    out[m, :3] = np.array(pal)[arr[m]]
    out[m, 3] = 255
    return Image.fromarray(out)


def preview(arr, pal, outdir):
    """Old (the Titanborn it is made from) and new, on the grass battle colors,
    at 1x and 4x."""
    os.makedirs(outdir, exist_ok=True)
    src = Image.open(SRC).convert("RGBA")
    row = Image.new("RGBA", (64 * 2 + 8, 64), (112, 160, 96, 255))
    row.alpha_composite(src, (0, 0))
    row.alpha_composite(rgba(arr, pal), (72, 0))
    row.save(os.path.join(outdir, "ichor_gigas_1x.png"))
    row.resize((row.width * 4, row.height * 4), Image.NEAREST).save(
        os.path.join(outdir, "ichor_gigas_4x.png"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--preview")
    args = ap.parse_args()
    arr, pal = build()
    if args.write:
        save(arr, pal, OUT)
        print("wrote", os.path.relpath(OUT, ROOT))
    if args.preview:
        preview(arr, pal, args.preview)


if __name__ == "__main__":
    sys.exit(main())
