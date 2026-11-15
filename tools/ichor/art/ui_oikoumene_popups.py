#!/usr/bin/env python3
"""Draw the Oikoumene's three map-name popups, in ui_menus_popup.py's style.

Each land the first batch builds gets a stone of its own, a 96x40 face and
frame cut the same way as the six Aethos ones (see ui_menus_popup.py for the
layout and the palette roles):

  troad    ILION'S WALLS  pale limestone ashlar with merlons along the top and
                          a sloping batter at the foot: the Troad and its plain
  papyrus  PAPYRUS        a papyrus sheet between its two rolled ends, edged
                          with a tomb-painting band of lapis, malachite and
                          ochre: Egypt
  pontos   COLCHIAN       a bronze plaque riveted at the corners, with the dark
           BRONZE         green Euxine running along its foot: the Black Sea

src/map_name_popup.c's MAPPOPUP_THEME_TROAD, _PAPYRUS and _PONTOS load them,
and its tables give each Oikoumene section a theme.

Usage: python3 tools/ichor/art/ui_oikoumene_popups.py
"""
import numpy as np

from ui_menus_lib import *
from ui_menus_popup import (W, H, T_OUT, T_TXT, T_SH, F_HI, F_MID, F_LO, E_DK, E_DEEP, A1, A2, A3, A4, A5,
                            shaded_slab)

OUT = ROOT / "graphics/map_popup"
IMG = ROOT / "design/oikoumene/img"

THEMES = {
    "troad": dict(
        pal=[TRANSPARENT, (64, 48, 32), (72, 56, 40), (240, 232, 200), (224, 208, 168), (200, 184, 144),
             (176, 160, 120), (136, 120, 88), (96, 80, 56), GOLD, GOLD_DARK, (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        kind="walls"),
    "papyrus": dict(
        pal=[TRANSPARENT, (56, 40, 24), (40, 32, 24), (248, 240, 200), (232, 216, 160), (216, 192, 128),
             (184, 152, 96), (136, 104, 56), (96, 72, 40), (40, 72, 160), (56, 144, 104), (200, 120, 40),
             (24, 40, 96), (0, 0, 0)],
        kind="papyrus"),
    "pontos": dict(
        pal=[TRANSPARENT, (48, 32, 16), (56, 32, 16), (240, 200, 120), (208, 152, 72), (176, 112, 48),
             (136, 80, 32), (96, 56, 24), (64, 40, 16), (40, 88, 72), (24, 56, 48), (248, 224, 160),
             (0, 0, 0), (0, 0, 0)],
        kind="bronze"),
}


def paint(kind):
    c = Canvas(W, H, 0)
    if kind == "walls":
        # the wall's face, its courses of ashlar, merlons on top, a batter below
        shaded_slab(c, 3, 7, 90, 27)
        for x in range(3, 93, 10):              # merlons along the top
            c.rect(x, 3, 6, 4, F_MID)
            c.hline(x, 3, 6, F_HI)
            c.vline(x + 5, 3, 4, F_LO)
            c.frame(x - 1, 2, 8, 6, T_OUT)
        c.hline(3, 7, 90, F_HI)
        for y in (13, 19, 25):                   # coursing joints, staggered
            c.hline(4, y, 88, F_LO)
        for k, y in enumerate((8, 14, 20, 26)):
            for x in range(10 + (k % 2) * 6, 90, 14):
                if y + 4 < 33:
                    c.vline(x, y, 5, F_LO)
        # the batter: the wall slopes out at its foot
        c.rect(1, 34, 94, 4, F_LO)
        c.hline(1, 34, 94, F_MID)
        c.frame(0, 33, 96, 6, T_OUT)
        c.rect(0, 39, 96, 1, 0)
        # a gold band of wheat at the base, the plain's
        for x in range(5, 91, 4):
            c.px(x, 35, A1)
            c.px(x + 1, 36, A2)
    elif kind == "papyrus":
        # the sheet, its fibres, the two rolled ends
        shaded_slab(c, 9, 4, 78, 32)
        rng = np.random.default_rng(11)
        for y in range(9, 31, 3):
            x = 11 + int(rng.integers(0, 6))
            while x < 84:
                n = int(rng.integers(4, 12))
                c.hline(x, y, min(n, 84 - x), F_LO)
                x += n + int(rng.integers(5, 12))
        for x0 in (2, 87):                       # the rolls
            c.rect(x0, 2, 7, 36, F_MID)
            c.vline(x0 + 1, 2, 36, F_HI)
            c.vline(x0 + 5, 2, 36, E_DK)
            c.frame(x0 - 1, 1, 9, 38, T_OUT)
            for y in (6, 18, 30):
                c.hline(x0, y, 7, E_DK)
        # a painted band top and bottom: lapis, malachite, ochre blocks
        for y0 in (5, 32):
            for k, x in enumerate(range(10, 86, 6)):
                col = (A1, A2, A3)[k % 3]
                c.rect(x, y0, 5, 2, col)
            c.hline(10, y0 - 1 if y0 == 5 else y0 + 2, 76, A4)
    elif kind == "bronze":
        shaded_slab(c, 3, 3, 90, 34)
        # hammered bronze: a few lighter strokes, then rivets in the corners
        for (x, y, n) in [(10, 9, 6), (70, 11, 7), (20, 28, 5), (60, 26, 4), (82, 20, 4)]:
            c.hline(x, y, n, F_HI)
        for (x, y) in [(6, 6), (89, 6), (6, 33), (89, 33)]:
            c.rect(x - 1, y - 1, 3, 3, E_DK)
            c.px(x - 1, y - 1, A3)
            c.px(x, y, F_HI)
        # the Euxine along the foot: dark green, a running wave in its crest
        c.rect(4, 30, 88, 6, A1)
        wave = ["..##....", ".#..#...", "#....#.#"]
        for x0 in range(4, 92, 8):
            for j, row in enumerate(wave):
                for i, ch in enumerate(row):
                    if ch == "#" and x0 + i < 92:
                        c.px(x0 + i, 31 + j, A2)
        c.hline(4, 29, 88, E_DEEP)
    return c


def write():
    sheets = []
    for name, th in THEMES.items():
        pal = pal16(th["pal"])
        c = paint(th["kind"])
        a = c.a
        write_indexed_png(OUT / f"{name}.png", a[8:32, 8:88], [pal])
        tiles = [a[0:8, x:x + 8] for x in range(0, 96, 8)]
        for ty in range(1, 4):
            tiles.append(a[ty * 8:ty * 8 + 8, 0:8])
            tiles.append(a[ty * 8:ty * 8 + 8, 88:96])
        tiles += [a[32:40, x:x + 8] for x in range(0, 96, 8)]
        write_tiles_png(OUT / f"{name}_outline.png", tiles, [pal], tiles_wide=10, min_tiles=30)
        sheets.append(canvas_rgb(c, [pal]))
    rows = []
    for rgb in sheets:
        bg = np.zeros((H + 8, W + 8, 3), np.uint8)
        bg[:] = (120, 152, 80)
        m = (rgb != np.array(TRANSPARENT, np.uint8)).any(axis=2)
        sub = bg[4:4 + H, 4:4 + W]
        sub[m] = rgb[m]
        rows.append(bg)
    IMG.mkdir(parents=True, exist_ok=True)
    save_rgb(IMG / "popups.png", np.hstack(rows), 3)


if __name__ == "__main__":
    write()
