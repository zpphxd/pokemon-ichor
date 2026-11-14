#!/usr/bin/env python3
"""The Augur's Eye (the expansion's DexNav), painted as an augur's tablet.

START > AUGURY opens src/dexnav.c's screen: the Pokemon of the current map by
where they live (sea, land, hidden), and the chosen one's species, type, search
level, hidden ability and chain. Emerald-expansion's art was a red and blue
gadget. Here it is the pottery family of UI_menus.md and UI_codex.md:

  - a black-glaze band along the top, where the engine prints "R TO REGISTER"
    and the map's name in parchment, with an R key cap on the left
  - three parchment leaves in clay frames on the terracotta field, one per
    habitat, each with an ink cartouche lettered SEA, LAND or HIDDEN and an
    incised socket where each Pokemon's icon stands
  - on the right, the augur's reading: a parchment leaf ruled into five
    entries, each headed by an ink band, under a gold-rimmed SEEK plaque with
    the A coin

The geometry is the engine's (include/dexnav.h): icon centres, the info
window at tile (21, 5) whose values print at y 5, 29, 53, 77 and 101, the
register window across rows 0-1 from tile 4. The screen is one 16-color BG
palette (gui.pal; its color 0 is the backdrop) and BG1 charbase 3, which has
room for 384 tiles before the tilemap at screen base 30.

Also recolors the sprites the screen loads with its own palette: the selection
cursor (a gold ring) and the "caught them all" mark (a black-figure ball).

Writes graphics/dexnav/gui_tiles.png, gui_tilemap.bin, gui.pal, cursor.png and
captured_all.png; and design/phase1/img/ui_augury.png.

Usage: /usr/bin/python3 tools/ichor/art/ui_augury.py
"""
import numpy as np
from PIL import Image

from ui_codex_lib import *  # noqa: F401,F403

OUT = ROOT / "graphics/dexnav"
IMG = ROOT / "design/phase1/img"

# One palette. Index 0 is the backdrop the engine shows through every
# transparent pixel, so it is the black glaze.
PAL = [GLAZE, INK, GLAZE, CLAY_DARK, CLAY, RING, CLAY_LIGHT, PARCHMENT, PARCH_SHADE,
       PARCH_DARK, PARCH_LIGHT, GOLD, GOLD_DARK, GOLD_PALE, BRONZE, INK_TEXT]
(K, G, CD, CL, RG, CLL, PA, PS, PD, PL, GO, GD, GP, BZ, TX) = range(1, 16)

# The engine's places (include/dexnav.h).
WATER_X, WATER_Y = 30, 35
LAND_X, LAND_TOP_Y, LAND_BOT_Y = 20, 72, 100
HIDDEN_X, HIDDEN_Y = 52, 138
INFO_X, INFO_Y = 21 * 8, 5 * 8
INFO_ROWS = [5, 29, 53, 77, 101]           # value y within the info window
LABELS = ["SPECIES", "TYPE", "SEARCH LEVEL", "HIDDEN ABILITY", "CURRENT CHAIN"]


def leaf(c, x, y, w, h):
    """A parchment leaf in a clay frame with an ink outline, lit from the top left."""
    c.frame(x, y, w, h, K)
    c.rect(x + 1, y + 1, w - 2, h - 2, CL)
    c.hline(x + 1, y + 1, w - 2, CLL)
    c.vline(x + 1, y + 1, h - 2, CLL)
    c.hline(x + 1, y + h - 2, w - 2, CD)
    c.vline(x + w - 2, y + 1, h - 2, CD)
    c.frame(x + 3, y + 3, w - 6, h - 6, K)
    c.rect(x + 4, y + 4, w - 8, h - 8, PA)
    c.hline(x + 4, y + 4, w - 8, PL)
    c.hline(x + 4, y + h - 5, w - 8, PS)


def socket(c, cx, cy):
    """An incised oval where a Pokemon's icon stands (its feet sit near cy + 8)."""
    for dx in range(-8, 9):
        for dy in range(-3, 4):
            if (dx / 8.5) ** 2 + (dy / 3.5) ** 2 <= 1.0:
                c.px(cx + dx, cy + 9 + dy, PS)
    for dx in range(-7, 8):
        c.px(cx + dx, cy + 6 if abs(dx) < 4 else cy + 7, PD)


def label(c, x, y, text, font="small"):
    """An ink cartouche lettered in parchment, 9 px tall (small capitals are 7)."""
    w = text_width(text, font) + 8
    cartouche(c, x, y, w, 9, K)
    draw_text(c, x + 4, y - 3, text, PL, font=font)
    return w


def key_cap(c, x, y, letter):
    """A parchment key cap with an ink letter, as on the codex's foot."""
    bevel_rect(c, x, y, 15, 12, PA, PL, PS, outline=K)
    draw_text(c, x + 4, y - 1, letter, TX, font="normal")


def coin(c, x, y, letter):
    """A gold coin struck with an ink letter, 12 px."""
    for dy in range(12):
        for dx in range(12):
            r = ((dx - 5.5) ** 2 + (dy - 5.5) ** 2) ** 0.5
            if r <= 5.9:
                c.px(x + dx, y + dy, K)
            if r <= 4.9:
                lit = (dx - 5.5) + (dy - 5.5) < -2
                c.px(x + dx, y + dy, GP if lit else GO)
    draw_text(c, x + 3, y - 2, letter, K, font="small")


def paint():
    c = Canvas(256, 160, 0)
    clay_field(c, 0, 0, 256, 160, CL, RG)
    # The glaze band and its gold rule.
    c.rect(0, 0, 256, 14, G)
    c.hline(0, 14, 256, GD)
    c.hline(0, 15, 256, K)
    key_cap(c, 9, 1, "R")

    # The sea: five Pokemon in a row.
    leaf(c, 8, 18, 144, 36)
    label(c, 12, 15, "SEA")
    for i in range(5):
        socket(c, WATER_X + 24 * i, WATER_Y)
    # The land: two rows of six.
    leaf(c, 2, 58, 154, 60)
    label(c, 6, 55, "LAND")
    for i in range(6):
        socket(c, LAND_X + 24 * i, LAND_TOP_Y)
        socket(c, LAND_X + 24 * i, LAND_BOT_Y)
    # The hidden: three.
    leaf(c, 32, 124, 96, 34)
    label(c, 36, 121, "HIDDEN")
    for i in range(3):
        socket(c, HIDDEN_X + 24 * i, HIDDEN_Y)

    # The reading: the SEEK plaque, then a ruled leaf of five entries.
    bevel_rect(c, 166, 17, 70, 18, CL, CLL, CD, outline=K)
    c.frame(167, 18, 68, 16, GD)
    coin(c, 172, 20, "A")
    draw_text(c, 188, 18, "SEEK", PL, shadow=CD, font="normal")
    leaf(c, 160, 37, 80, 123)
    for i, (text, row) in enumerate(zip(LABELS, INFO_ROWS)):
        y = INFO_Y + row - 9
        c.rect(164, y, 72, 9, K)
        c.hline(164, y + 8, 72, CD)
        draw_text(c, 167, y - 3, text, PL, font="small")
    # A meander along the foot of the clay.
    meander_band(c, 0, 153, 32, K, CL)
    meander_band(c, 128, 153, 32, K, CL)
    return c


def write():
    c = paint()
    ts = TileSet(reserved=1)
    m = compile_map(c, ts, 32, 32, region=(0, 0, 32, 20))
    check_tiles(len(ts), 384, "graphics/dexnav/gui_tiles.png")
    write_tiles_png(OUT / "gui_tiles.png", ts.tiles, [PAL], tiles_wide=16)
    write_tilemap(OUT / "gui_tilemap.bin", m)
    write_jasc(OUT / "gui.pal", PAL)

    # The selection cursor: Emerald-expansion's red ring, now a gold one with an
    # ink edge. captured_all.png shares this palette: a black-figure ball.
    cur = np.array(Image.open(OUT / "cursor.png"))
    cpal = [(248, 0, 248), GOLD, PARCH_LIGHT, PARCHMENT, PARCH_DARK, CLAY, CLAY_DARK, INK] + [(0, 0, 0)] * 8
    write_indexed_png(OUT / "cursor.png", cur, [cpal])
    cap = np.array(Image.open(OUT / "captured_all.png"))
    write_indexed_png(OUT / "captured_all.png", cap, [cpal])

    rgb = render_map(m, ts.tiles, [PAL], w=30, h=20)
    save_rgb(IMG / "ui_augury.png", rgb, 3)


if __name__ == "__main__":
    write()
