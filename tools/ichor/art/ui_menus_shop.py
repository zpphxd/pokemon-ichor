#!/usr/bin/env python3
"""Draw Ichor's Agora: the buy menu as a market stall.

The item list is the stall: a striped awning with a scalloped valance over a
papyrus price board, between two wooden posts, on a counter plank with a
meander painted along its front. The description and the item icon sit on
papyrus panels, matching the bag. The top left stays open on the Agora map,
as the Hoenn mart did, with the money box framed like every menu.

The engine loads these tiles at 0x3E3 on BG1 (BuyMenuDecompressBgGraphics
in src/shop.c), so there is room for 29 tiles and no more; a tilemap entry
of 0 leaves the map showing. The list and description text print in palette
15 (the dialogue box's): ink on PARCHMENT, which the description fills
behind each line, so its panel is exactly that color.

Writes, in graphics/shop/: menu.png (palette 12), menu.bin, money.png.

Usage: python3 tools/ichor/art/ui_menus_shop.py
"""
import numpy as np

from ui_menus_lib import *

OUT = ROOT / "graphics/shop"
IMG = ROOT / "design/phase1/img"

ROW_ALT = (224, 200, 152)
WOOD_DARK = (88, 48, 24)
WOOD = (136, 88, 48)
WOOD_LIGHT = (184, 128, 72)

PAL = pal16([
    TRANSPARENT,   # 0
    INK,           # 1
    CLAY_DARK,     # 2
    CLAY,          # 3
    CLAY_LIGHT,    # 4
    PARCHMENT,     # 5  papyrus; equals the text fill
    PARCH_SHADE,   # 6
    PARCH_DARK,    # 7
    WOOD_DARK,     # 8
    WOOD,          # 9
    WOOD_LIGHT,    # 10
    GOLD,          # 11
    GOLD_DARK,     # 12
    ROW_ALT,       # 13 alternate list rows
    (96, 64, 40),  # 14 shade under the awning
    GOLD_PALE,     # 15 MONEY label, lit
])
K_INK, K_LINE, K_CLAY, K_HI, K_P, K_PS, K_PD, K_W0, K_W1, K_W2, K_G, K_GD, K_ALT, K_SH = range(1, 15)

W, H = 240, 160


def paint():
    c = Canvas(W, H, 0)

    # --- the stall, cols 13-29 --------------------------------------------
    x0, x1 = 104, 240
    # price board: papyrus rows, alternating every item (16 px) like the
    # Hoenn list, from row 2 to row 18
    for y in range(16, 152):
        c.hline(x0 + 8, y, x1 - x0 - 16, K_P if ((y - 16) // 16) % 2 == 0 else K_ALT)
    # the shade cast by the awning
    c.hline(x0 + 8, 16, x1 - x0 - 16, K_PD)
    c.hline(x0 + 8, 17, x1 - x0 - 16, K_PS)
    # wooden posts
    for px in (x0, x1 - 8):
        c.rect(px + 1, 8, 6, 144, K_W1)
        c.vline(px + 1, 8, 144, K_W2)
        c.vline(px + 2, 8, 144, K_W2)
        c.vline(px + 6, 8, 144, K_W0)
        c.vline(px, 8, 144, K_INK)
        c.vline(px + 7, 8, 144, K_INK)
    # awning: 8 px stripes, clay and papyrus, under an ink ridge
    for x in range(x0, x1):
        stripe = K_CLAY if ((x - x0) // 8) % 2 == 0 else K_P
        c.vline(x, 1, 9, stripe)
        if stripe == K_CLAY and (x - x0) % 8 == 0:
            c.vline(x, 1, 9, K_HI)
    c.hline(x0, 0, x1 - x0, K_INK)
    c.hline(x0, 1, x1 - x0, K_LINE)
    # scalloped valance: each 8 px stripe ends in a rounded tongue
    for x in range(x0, x1):
        k = (x - x0) % 8
        stripe = K_CLAY if ((x - x0) // 8) % 2 == 0 else K_P
        depth = [2, 4, 5, 6, 6, 5, 4, 2][k]
        for j in range(depth):
            c.px(x, 10 + j, stripe)
        c.px(x, 10 + depth, K_INK)
        for j in range(depth + 1, 8):
            if c.a[10 + j, x] == 0:
                c.px(x, 10 + j, K_SH if 112 <= x < 232 else 0)
    c.hline(x0, 9, x1 - x0, K_LINE)
    # counter plank across the foot, row 19, with a painted meander
    c.rect(x0, 152, x1 - x0, 8, K_W1)
    c.hline(x0, 152, x1 - x0, K_INK)
    c.hline(x0, 153, x1 - x0, K_W2)
    c.rect(x0, 154, x1 - x0, 5, K_W1)
    c.meander(x0, 154, x1 - x0, K_W0)
    c.hline(x0, 159, x1 - x0, K_INK)

    # --- item icon plate, as in the bag (the pic at ICON_PIC) ---------------
    check_icon_plate()
    bx, by, bw, bh = ICON_PLATE
    c.rect(bx, by, bw, bh, K_P)
    c.frame(bx, by, bw, bh, K_INK)
    c.frame(bx + 2, by + 2, bw - 4, bh - 4, K_PS)
    c.hline(bx + 1, by + 1, bw - 2, K_HI)
    c.vline(bx + 1, by + 1, bh - 2, K_HI)
    for (px, py) in [(bx, by), (bx + bw - 1, by), (bx, by + bh - 1), (bx + bw - 1, by + bh - 1)]:
        c.px(px, py, 0)

    # --- description, cols 0-12, rows 13-19 ----------------------------------
    dy = 103
    c.rect(0, dy, 104, H - dy, K_P)
    c.hline(0, dy, 104, K_INK)
    c.hline(0, dy + 1, 103, K_LINE)
    c.hline(0, dy + 2, 103, K_HI)
    c.vline(103, dy, H - dy, K_INK)
    return c


def compile_shop(c):
    ts = TileSet()
    ts.tiles = [np.zeros((8, 8), np.uint8)]
    ts.lookup = {}
    ts._index(ts.tiles[0], 0)
    entries = np.zeros((32, 32), np.uint16)
    for ty in range(20):
        for tx in range(30):
            cell = c.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            if not cell.any():
                continue
            i, f = ts.add(cell)
            assert i != 0 or f, (tx, ty)
            entries[ty, tx] = i | f
    n = len(ts.tiles)
    assert n <= 29, f"shop menu uses {n} tiles; the engine has room for 29 (0x3E3-0x3FF)"
    return ts, entries


def write():
    c = paint()
    ts, entries = compile_shop(c)
    write_tiles_png(OUT / "menu.png", ts.tiles, [PAL], tiles_wide=29, min_tiles=29)
    write_tilemap(OUT / "menu.bin", entries)
    print(f"shop menu: {len(ts.tiles)} tiles")
    write_money_label()
    preview(c)


# The MONEY label beside the amount, a 32x16 sprite. The engine colors it
# with this menu's palette (sSpritePalette_MoneyLabel in src/money.c uses
# gShopMenu_Pal), so it is drawn in those indices: gold letters, lit on top,
# outlined in ink, like the HM badge. The letterforms are Emerald's.
MONEY = [
    "                                ",
    "                                ",
    "                                ",
    "   111 11111111111111111111 111 ",
    "   1e111e11ee11e11d1eeed1e1 1d1 ",
    "   1ee1ee1e11d1ee1e1d1111e111e1 ",
    "   1c1e1d1c11c1c1cc1ccc111c1c11 ",
    "   1c111c1c11c1c11c1c111111c111 ",
    "   1d111d11dd11d11d1dddd111d11  ",
    "   111 111111111111111111 111   ",
]


def write_money_label():
    key = {" ": 0, "1": K_INK, "e": 15, "c": K_G, "d": K_GD}
    a = np.zeros((16, 32), np.uint8)
    for y, row in enumerate(MONEY):
        for x, ch in enumerate(row):
            a[y, x] = key[ch]
    write_indexed_png(OUT / "money.png", a, [PAL])


def preview(c):
    # The stall over a stand-in for the Agora floor, at 2x.
    rgb = canvas_rgb(c, [PAL])
    floor = np.zeros_like(rgb)
    floor[:] = (200, 176, 136)
    for y in range(0, H, 16):
        floor[y, :] = (168, 144, 104)
    m = c.a == 0
    rgb[m] = floor[m]
    save_rgb(IMG / "ui_shop_bg.png", rgb, 2)


if __name__ == "__main__":
    write()
