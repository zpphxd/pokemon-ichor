#!/usr/bin/env python3
"""Draw Ichor's map-name popups as carved stones and painted plaques.

A popup is a 96x40 stone: an 80x24 face behind the name (theme.png) and a
one-tile border (theme_outline.png, 30 tiles in the order DrawMapNamePopUpFrame
in src/map_name_popup.c draws them: 12 along the top, then left/right pairs
for the three middle rows, then 12 along the bottom). The name prints in
palette 14 with color 2 and shadow 3, so each theme sets those two:

  wood slot        STELE   a marble stele with a low pediment and incised
                           letters (dark cut, lit lower edge): villages,
                           towns and routes, Kalliste's included
  marble slot      TEMPLE  white marble, gilded pediment and gilt letters:
                           cities and sanctuaries
  stone slot       CAVE    a rough basalt slab with chiseled light letters
  brick slot       CLAY    a terracotta plaque with a black-figure meander
                           and ink letters
  underwater slot  SEA     an Aegean-blue fresco tile edged with the
                           running wave, letters in lime-white
  stone2 slot      DEEP    sunken sea-green marble with barnacles, for the
                           sea floor (and underwater.pal, used whenever the
                           weather is underwater bubbles)

The enum and file names stay Emerald's so upstream merges stay easy; the
theme table in map_name_popup.c maps each map section to one of them.

Usage: python3 tools/ichor/art/ui_menus_popup.py
"""
import numpy as np

from ui_menus_lib import *

OUT = ROOT / "graphics/map_popup"
IMG = ROOT / "design/phase1/img"

W, H = 96, 40

# Every theme uses the same index roles, so one painter draws them all:
# 1 outline, 2 text, 3 text shadow, 4 face light, 5 face, 6 face shade,
# 7 edge dark, 8 deep, 9-13 accents.
T_OUT, T_TXT, T_SH, F_HI, F_MID, F_LO, E_DK, E_DEEP, A1, A2, A3, A4, A5 = range(1, 14)

THEMES = {
    "wood": dict(  # STELE
        pal=[TRANSPARENT, (56, 48, 48), (80, 72, 72), MARBLE_LIGHT, (240, 232, 224), MARBLE, (192, 184, 168),
             MARBLE_DARK, (120, 112, 104), (232, 224, 208), (176, 168, 152), GOLD, GOLD_DARK, (0, 0, 0)],
        kind="stele"),
    "marble": dict(  # TEMPLE
        pal=[TRANSPARENT, (72, 56, 40), (128, 80, 16), (248, 240, 200), MARBLE_LIGHT, (240, 232, 224), (216, 208, 192),
             MARBLE_DARK, (120, 112, 104), GOLD, GOLD_DARK, AEGEAN, CLAY, (0, 0, 0)],
        kind="temple"),
    "stone": dict(  # CAVE
        pal=[TRANSPARENT, (24, 24, 24), (224, 216, 200), (32, 32, 32), (136, 128, 120), (104, 96, 96), (80, 72, 72),
             (56, 48, 48), (40, 32, 32), (152, 144, 136), (72, 64, 64), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        kind="cave"),
    "brick": dict(  # CLAY
        pal=[TRANSPARENT, INK, INK, CLAY_LIGHT, CLAY_LIGHT, CLAY, (160, 72, 40),
             CLAY_DARK, (88, 32, 16), INK, PARCHMENT, (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        kind="clay"),
    "underwater": dict(  # SEA
        pal=[TRANSPARENT, AEGEAN_DARK, MARBLE_LIGHT, AEGEAN_DARK, AEGEAN_LIGHT, AEGEAN, (40, 88, 152),
             AEGEAN_DARK, (16, 40, 88), MARBLE_LIGHT, AEGEAN_PALE, (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        kind="sea"),
    "stone2": dict(  # DEEP
        pal=[TRANSPARENT, (16, 40, 48), (216, 240, 232), (16, 40, 48), (120, 176, 168), (88, 144, 144), (64, 112, 120),
             (40, 80, 88), (24, 56, 64), (168, 208, 192), (152, 112, 88), OLIVE_LIGHT, (0, 0, 0), (0, 0, 0)],
        kind="deep"),
}


def shaded_slab(c, x, y, w, h, outline=True):
    """A slab lit from the top left: highlight, face, shade and an outline."""
    c.rect(x, y, w, h, F_MID)
    c.hline(x, y, w, F_HI)
    c.vline(x, y, h, F_HI)
    c.hline(x, y + h - 1, w, F_LO)
    c.vline(x + w - 1, y, h, F_LO)
    if outline:
        c.frame(x - 1, y - 1, w + 2, h + 2, T_OUT)


def pediment(c, x0, x1, base, rise, fill=F_MID, edge=F_HI):
    """A low gable from x0 to x1 standing on row `base`."""
    mid = (x0 + x1) / 2
    half = (x1 - x0) / 2
    for x in range(x0, x1 + 1):
        top = base - round(rise * (1 - abs(x - mid) / half))
        c.vline(x, top, base - top + 1, fill)
        c.px(x, top, edge if x <= mid else F_LO)
        c.px(x, top - 1, T_OUT)


def paint(kind):
    c = Canvas(W, H, 0)
    if kind in ("stele", "temple"):
        gilt = kind == "temple"
        # the slab, its face behind the name (y 8-31)
        shaded_slab(c, 5, 8, 86, 27)
        # grain: faint veins across the marble
        for (x, y, n) in [(9, 30, 5), (80, 11, 5)]:  # two faint veins, clear of the name
            for i in range(n):
                c.px(x + i, y + (i // 4) % 2, A2 if kind == "stele" else F_LO)
        # a low pediment (y 1-5) on a cornice (y 5-7), with acroteria
        pediment(c, 4, 91, 5, 4, fill=A1 if gilt else F_MID, edge=F_HI)
        if gilt:
            # a tympanum disc, the sun, at the gable's center
            for (dx, dy) in [(0, 0), (-1, 0), (1, 0), (0, -1)]:
                c.px(47 + dx, 4 + dy, A2)
        c.hline(2, 5, 92, T_OUT)
        c.hline(2, 6, 92, F_HI)
        c.hline(2, 7, 92, E_DK)
        c.vline(1, 5, 3, T_OUT)
        c.vline(94, 5, 3, T_OUT)
        for ax in (3, 92):
            c.rect(ax - 1, 2, 3, 3, A1 if gilt else F_MID)
            c.px(ax, 2, F_HI)
            c.frame(ax - 2, 1, 5, 5, T_OUT)
        c.rect(46, 0, 3, 1, A1 if gilt else F_HI)
        c.hline(4, 7, 88, T_OUT)
        # plinth
        c.rect(1, 35, 94, 4, E_DK)
        c.hline(1, 35, 94, F_LO)
        c.frame(0, 34, 96, 6, T_OUT)
        if kind == "temple":
            # a gilded band under the cornice and gold rosettes in the corners
            c.hline(5, 9, 86, A1)
            c.hline(5, 10, 86, A2)
            for rx in (8, 87):
                for (dx, dy) in [(0, -1), (-1, 0), (1, 0), (0, 1), (0, 0)]:
                    c.px(rx + dx, 30 + dy, A1)
                c.px(rx, 30, A2)
    elif kind == "cave":
        rng = np.random.default_rng(7)
        shaded_slab(c, 3, 3, 90, 34)
        # a rough, chipped outline
        for x in range(2, 94):
            if rng.random() < 0.35:
                c.px(x, 3, 0)
                c.px(x, 2, 0)
                c.px(x, 4, T_OUT)
            if rng.random() < 0.35:
                c.px(x, 37, 0)
                c.px(x, 36, T_OUT)
        for y in range(3, 37):
            if rng.random() < 0.3:
                c.px(2, y, 0)
                c.px(3, y, T_OUT)
            if rng.random() < 0.3:
                c.px(93, y, 0)
                c.px(92, y, T_OUT)
        # speckle and cracks
        for _ in range(70):
            x, y = int(rng.integers(6, 90)), int(rng.integers(6, 34))
            c.px(x, y, A1 if rng.random() < 0.5 else A2)
        for (x, y) in [(14, 8), (15, 9), (15, 10), (16, 11), (78, 26), (79, 27), (79, 28), (80, 29), (81, 29)]:
            c.px(x, y, E_DEEP)
    elif kind == "clay":
        shaded_slab(c, 2, 2, 92, 36)
        # black-figure meander top and bottom, ink rules
        for y0 in (3, 32):
            c.hline(3, y0, 90, T_OUT)
            c.meander(4, y0 + 1, 88, T_OUT)
            c.hline(3, y0 + 6 if y0 == 3 else y0 - 1, 90, T_OUT)
        # rays down the sides
        for y in range(10, 31, 4):
            c.hline(3, y, 3, T_OUT)
            c.px(3, y + 1, T_OUT)
            c.hline(90, y, 3, T_OUT)
            c.px(92, y + 1, T_OUT)
    elif kind == "sea":
        shaded_slab(c, 2, 2, 92, 36)
        # the running wave along the foot and the head
        wave = [
            "..##....",
            ".#..#...",
            "#.##.#..",
            "#.#..#.#",
            ".#...##.",
        ]
        for x0 in range(3, 93, 8):
            for j, row in enumerate(wave):
                for i, ch in enumerate(row):
                    if ch == "#" and x0 + i < 93:
                        c.px(x0 + i, 32 + j, A1)
                        c.px(x0 + i, 3 + (4 - j), A2)
        c.hline(3, 31, 90, E_DEEP)
        c.hline(3, 8, 90, E_DEEP)
    elif kind == "deep":
        rng = np.random.default_rng(3)
        shaded_slab(c, 3, 4, 90, 32)
        c.rect(2, 1, 92, 4, F_HI)
        c.frame(1, 0, 94, 6, T_OUT)
        c.rect(2, 35, 92, 4, E_DK)
        c.frame(1, 34, 94, 6, T_OUT)
        # weathering, barnacles and a strand of weed
        for _ in range(40):
            x, y = int(rng.integers(5, 91)), int(rng.integers(7, 33))
            c.px(x, y, A1 if rng.random() < 0.6 else E_DK)
        for (x, y) in [(10, 30), (12, 31), (84, 9), (86, 10), (85, 28)]:
            c.px(x, y, A2)
            c.px(x + 1, y, A2)
        for y in range(6, 36):
            c.px(90 + (y // 3) % 2, y, A3)
    return c


def write():
    sheets = []
    for name, th in THEMES.items():
        pal = pal16(th["pal"])
        c = paint(th["kind"])
        a = c.a
        interior = a[8:32, 8:88]
        write_indexed_png(OUT / f"{name}.png", interior, [pal])
        # outline tiles, in DrawMapNamePopUpFrame's order
        tiles = [a[0:8, x:x + 8] for x in range(0, 96, 8)]
        for ty in range(1, 4):
            tiles.append(a[ty * 8:ty * 8 + 8, 0:8])
            tiles.append(a[ty * 8:ty * 8 + 8, 88:96])
        tiles += [a[32:40, x:x + 8] for x in range(0, 96, 8)]
        write_tiles_png(OUT / f"{name}_outline.png", tiles, [pal], tiles_wide=10, min_tiles=30)
        if name == "stone2":
            write_jasc(OUT / "underwater.pal", pal)
        sheets.append(canvas_rgb(c, [pal]))
    # Preview: each stone with a sample name, at 3x, on a grass stand-in.
    preview(sheets)


SAMPLES = ["ELAIA VILLAGE", "AKTI TOWN", "KRONION CAVE", "EMPORION", "ROUTE 2", "ATLANTIS"]


def preview(sheets):
    rows = []
    for rgb in sheets:
        bg = np.zeros((H + 8, W + 8, 3), np.uint8)
        bg[:] = (120, 152, 80)
        m = (rgb != np.array(TRANSPARENT, np.uint8)).any(axis=2)
        sub = bg[4:4 + H, 4:4 + W]
        sub[m] = rgb[m]
        rows.append(bg)
    sheet = np.vstack([np.hstack(rows[:3]), np.hstack(rows[3:])])
    save_rgb(IMG / "ui_popup_themes.png", sheet, 3)


if __name__ == "__main__":
    write()
