#!/usr/bin/env python3
"""Draw Ichor's bag screen: a traveler's satchel on a pottery field.

The screen is one painted vase panel: a meander frieze along the top, a row of
black-figure rays along the foot, a terracotta field with throwing rings, and
parchment panels framed like the dialogue box. The pocket name sits on a
parchment label under the frieze, beside a silver drachma (the old Poke Ball
sticker, which spins when the pocket changes).

Writes, in graphics/bag/:
  menu.png, menu.bin            BG2 tiles and tilemap (<= 53 tiles, see graphics.c)
  menu_male.pal, menu_female.pal  BG palettes 0 (art) and 1 (list text)
  rotating_ball.png             the drachma sprite that spins on a pocket switch
  hm.png, select_button.png     list badges, repainted black-figure
The satchel itself is drawn by ui_menus_satchel.py.

Usage: python3 tools/ichor/art/ui_menus_bag.py
"""
import numpy as np

from ui_frames import CORNER, TOP, LEFT
from ui_menus_lib import *

OUT = ROOT / "graphics/bag"
IMG = ROOT / "design/phase1/img"

# Palette 0: the painted screen.
BG = pal16([
    TRANSPARENT,   # 0
    INK,           # 1  black-figure ink, outlines
    CLAY_DARK,     # 2  incised lines
    CLAY,          # 3  the field
    CLAY_LIGHT,    # 4  clay highlight
    (160, 72, 40), # 5  throwing rings in the field
    PARCHMENT,     # 6  panels
    PARCH_SHADE,   # 7
    PARCH_DARK,    # 8
    GOLD_DARK,     # 9
    GOLD,          # 10
    MARBLE,        # 11 the drachma
    MARBLE_DARK,   # 12
    MARBLE_LIGHT,  # 13
    (96, 88, 88),  # 14 drachma shadow
    (0, 0, 0),     # 15 unused
])
I_INK, I_LINE, I_CLAY, I_HI, I_RING, I_P, I_PS, I_PD, I_GD, I_G, I_M, I_MD, I_ML, I_MS = range(1, 15)

# Palette 1: the text windows draw with it (sFontColorTable in item_menu.c):
# item names in 1 with shadow 3, the pocket name in 1 with shadow 4, a moving
# item in 3 with shadow 6. The HM badge and SELECT tag use 1, 5, 10, 11, 15,
# and the pocket dots (tiles 0x17 and 0x2B, drawn by DrawPocketIndicatorSquare)
# are painted in 2 and 7-9 and 12-13 so they sit on the field.
TEXT = pal16([
    TRANSPARENT,   # 0
    INK_TEXT,      # 1  text
    INK,           # 2  dot outline
    PARCH_SHADE,   # 3  text shadow
    CLAY_LIGHT,    # 4  pocket name shadow
    GOLD,          # 5  SELECT tag
    PARCH_DARK,    # 6  shadow of an item being moved
    CLAY,          # 7  field (dots)
    (160, 72, 40), # 8  field rings (dots)
    CLAY_DARK,     # 9  empty dot
    PARCHMENT,     # 10 list panel, behind the badges
    GOLD_DARK,     # 11 HM letters, shade
    GOLD_DARK,     # 12 full dot, shade
    GOLD,          # 13 full dot
    GOLD_PALE,     # 14 full dot, glint
    GOLD,          # 15 HM letters
])

W, H = 240, 160
FIELD_RING_PERIOD = 8


def field(c, x, y, w, h):
    """Terracotta with a throwing ring on the last row of every tile."""
    c.rect(x, y, w, h, I_CLAY)
    for yy in range(y, y + h):
        if yy % FIELD_RING_PERIOD == FIELD_RING_PERIOD - 1:
            c.hline(x, yy, w, I_RING)


# Frame tiles from the dialogue box, keyed into palette 0. On the field the
# frame's outer outline is ink, so a panel reads as painted onto the clay.
FRAME_KEY = {"o": I_INK, "#": I_INK, "d": I_LINE, ".": I_CLAY, "l": I_HI, "p": I_P}


def stamp_tile(c, tx, ty, t, key, under=None):
    for y, row in enumerate(t):
        for x, ch in enumerate(row):
            if ch == " ":
                if under is not None:
                    c.px(tx * 8 + x, ty * 8 + y, under(tx * 8 + x, ty * 8 + y))
                continue
            c.px(tx * 8 + x, ty * 8 + y, key[ch])


def field_at(x, y):
    return I_RING if y % FIELD_RING_PERIOD == FIELD_RING_PERIOD - 1 else I_CLAY


def hflip(t):
    return [r[::-1] for r in t]


def vflip(t):
    return t[::-1]


def framed_panel(c, tx, ty, tw, th):
    """A dialogue-box frame (meander all round, saltire corners) of tw x th
    tiles, its inside left for the caller to fill."""
    for x in range(tx, tx + tw):
        for y in range(ty, ty + th):
            if (x, y) == (tx, ty):
                t = CORNER
            elif (x, y) == (tx + tw - 1, ty):
                t = hflip(CORNER)
            elif (x, y) == (tx, ty + th - 1):
                t = vflip(CORNER)
            elif (x, y) == (tx + tw - 1, ty + th - 1):
                t = vflip(hflip(CORNER))
            elif y == ty:
                t = TOP
            elif y == ty + th - 1:
                t = vflip(TOP)
            elif x == tx:
                t = LEFT
            elif x == tx + tw - 1:
                t = hflip(LEFT)
            else:
                continue
            stamp_tile(c, x, y, t, FRAME_KEY, field_at)


def frieze_top(c, y, w):
    """The shoulder frieze: ink rules round a meander on clay."""
    c.hline(0, y, w, I_LINE)
    c.hline(0, y + 1, w, I_INK)
    c.rect(0, y + 2, w, 5, I_CLAY)
    c.meander(0, y + 2, w, I_INK)  # rows y+2..y+6
    c.hline(0, y + 7, w, I_INK)


def frieze_rays(c, y, w):
    """The foot of the vase: black rays rising from an ink rule."""
    c.rect(0, y, w, 8, I_CLAY)
    c.hline(0, y, w, I_INK)
    for x0 in range(0, w, 8):
        # a slim black ray rising from the foot rule to a point
        for j, half in enumerate([0, 0, 1, 1, 2, 3]):
            c.hline(x0 + 4 - half, y + 2 + j, 2 * half + 1, I_INK)
    c.hline(0, y + 7, w, I_INK)


# The drachma: a silver coin struck with Athena's owl, 16x16, the owl in
# black-figure ink. The same picture is the BG sticker and the sprite that
# spins while the pocket changes.
COIN = [
    "                ",
    "     dddddd     ",
    "   dd333333dd   ",
    "  d33llllll33d  ",
    "  d3lkllllkl3d  ",
    " d3llkkkkkkll3d ",
    " d3lkwwkkwwkl3d ",
    " d3lkwpkkpwkl3d ",
    " d3lkkkggkkkl3d ",
    " d3llkk.kkkll3d ",
    " d3llkkkk.kll3d ",
    "  d3lkkkkkkl3d  ",
    "  d33lgllgl33d  ",
    "   dd333333dd   ",
    "     dddddd     ",
    "                ",
]


def paint_coin(c, x, y):
    key = {"d": I_MS, "3": I_MD, "l": I_ML, ".": I_M, "k": I_INK, "w": I_ML, "p": I_INK, "g": I_G}
    c.grid(x, y, COIN, key)


def rosette(c, x, y):
    """A black-figure filler rosette: five dots round a center."""
    for (dx, dy) in [(0, -2), (-2, -1), (2, -1), (-1, 2), (1, 2)]:
        c.px(x + dx, y + dy, I_INK)
    c.px(x, y, I_INK)


def paint_screen():
    c = Canvas(W, H)
    field(c, 0, 0, W, H)

    # Shoulder frieze across the whole screen.
    frieze_top(c, 0, W)

    # The item list: a dialogue-box panel, cols 13-29, rows 1-18. Its inside
    # (cols 14-28, rows 2-17) must be the single plain tile 0x11, which
    # DrawItemListBgRow repaints row by row.
    framed_panel(c, 13, 1, 17, 18)
    c.rect(14 * 8, 2 * 8, 15 * 8, 16 * 8, I_P)

    # Pocket name label: parchment, cols 4-11 rows 1-2, hung under the frieze.
    lx, ly, lw, lh = 32, 8, 64, 16
    c.rect(lx, ly, lw, lh, I_P)
    c.frame(lx, ly, lw, lh, I_INK)
    c.hline(lx + 1, ly + 1, lw - 2, I_HI)          # lit top edge
    c.hline(lx + 1, ly + lh - 2, lw - 2, I_PS)     # shaded foot
    for (px, py) in [(lx, ly), (lx + lw - 1, ly), (lx, ly + lh - 1), (lx + lw - 1, ly + lh - 1)]:
        c.px(px, py, field_at(px, py))             # round the corners
    # small ink studs where the label hangs from the frieze
    for sx in (lx + 4, lx + lw - 5):
        c.px(sx, ly - 1, I_INK)

    # The drachma, where the Hoenn bag had its ball sticker.
    paint_coin(c, 8, 8)

    # Item icon plate: parchment, cols 1-4 rows 9-12 (the icon is 24x24 at 24,88).
    bx, by, bw, bh = 9, 73, 30, 29
    c.rect(bx, by, bw, bh, I_P)
    c.frame(bx, by, bw, bh, I_INK)
    c.frame(bx + 2, by + 2, bw - 4, bh - 4, I_PS)
    c.hline(bx + 1, by + 1, bw - 2, I_HI)
    c.vline(bx + 1, by + 1, bh - 2, I_HI)

    # The satchel (a 64x64 sprite at 36,34) stands on a short meander plinth,
    # the way figures on a vase stand on their ground line.
    px0, pw = 44, 56
    c.hline(px0, 92, pw, I_INK)
    c.rect(px0, 93, pw, 5, I_CLAY)
    c.meander(px0, 93, pw, I_INK)
    c.hline(px0, 98, pw, I_INK)
    c.hline(px0 + 1, 99, pw - 1, I_LINE)

    # Filler rosettes, as on Corinthian and early Attic ware.
    for (x, y) in [(17, 42), (26, 58), (12, 64)]:
        rosette(c, x, y)

    # Description: parchment running off the left edge, cols 0-12 rows 13-18.
    dx, dy, dw, dh = 0, 103, 104, 49
    c.rect(dx, dy, dw, dh, I_P)
    c.hline(dx, dy, dw, I_INK)
    c.hline(dx, dy + 1, dw - 1, I_LINE)
    c.vline(dx + dw - 1, dy, dh, I_INK)
    c.vline(dx + dw - 2, dy + 1, dh - 1, I_LINE)

    # Foot frieze.
    frieze_rays(c, 152, W)
    return c


def compile_bag(c):
    ts = TileSet(reserved=0)
    # Fixed tiles the code draws by number.
    plain = np.full((8, 8), I_P, np.uint8)
    dot_off, dot_on = pocket_dots()
    ts.place(0, np.zeros((8, 8), np.uint8))
    ts.place(0x11, plain)
    ts.place(0x17, dot_off)
    ts.place(0x2B, dot_on)
    # The tile slots between the fixed ones are filled as new tiles arrive.
    free = [i for i in range(1, 0x40) if i not in (0x11, 0x17, 0x2B)]
    entries = np.zeros((32, 32), np.uint16)
    for ty in range(20):
        for tx in range(30):
            cell = c.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            hit = ts.lookup.get((cell & 15).tobytes())
            if hit is None:
                idx = free.pop(0)
                ts.place(idx, cell)
                hit = (idx, 0)
            entries[ty, tx] = hit[0] | hit[1]
    # The dots row: the code repaints cols 5-9 of row 3 with palette 1.
    for tx in range(5, 10):
        entries[3, tx] = 0x17 | (1 << 12)
    used = max(int(e & 0x3FF) for e in entries.flat) + 1
    assert used <= 53, f"bag menu uses {used} tiles; graphics.c loads -num_tiles 53"
    return ts, entries


def pocket_dots():
    """Tiles 0x17 (other pocket) and 0x2B (this pocket), in palette 1 so
    the colors stay true on the field: a hollow clay ring and a gold disc."""
    F, R = 7, 8   # field, ring rows (palette 1)
    base = np.full((8, 8), F, np.uint8)
    base[7, :] = R
    off = base.copy()
    for (x, y) in [(3, 2), (4, 2), (2, 3), (5, 3), (2, 4), (5, 4), (3, 5), (4, 5)]:
        off[y, x] = 9
    on = base.copy()
    disc = [
        " 2222 ",
        "2edd22",
        "2dddc2",
        "2dccc2",
        " 2222 ",
    ]
    key = {"2": 2, "e": 14, "d": 13, "c": 12}
    for j, row in enumerate(disc):
        for i, ch in enumerate(row):
            if ch != " ":
                on[1 + j, 1 + i] = key[ch]
    return off, on


def write_bag_bg():
    c = paint_screen()
    ts, entries = compile_bag(c)
    n = max(int(e & 0x3FF) for e in entries.flat) + 1
    tiles = ts.tiles[:max(n, 0x2C)]
    write_tiles_png(OUT / "menu.png", tiles, [BG], tiles_wide=16, min_tiles=64)
    write_tilemap(OUT / "menu.bin", entries)
    write_jasc(OUT / "menu_male.pal", BG + TEXT)
    write_jasc(OUT / "menu_female.pal", BG + TEXT)
    print(f"bag menu: {n} tiles")
    return c, ts, entries


def write_coin_sprite():
    # rotating_ball.png: sprite palette of its own (index 0 transparent).
    key = {"d": 1, "3": 2, "l": 3, ".": 4, "k": 5, "w": 3, "p": 5, "g": 6}
    a = np.zeros((16, 16), np.uint8)
    for y, row in enumerate(COIN):
        for x, ch in enumerate(row):
            if ch != " ":
                a[y, x] = key[ch]
    pal = pal16([TRANSPARENT, (96, 88, 88), MARBLE_DARK, MARBLE_LIGHT, MARBLE, INK, GOLD])
    write_indexed_png(OUT / "rotating_ball.png", a, [pal])


def write_badges():
    # HM badge: gold letters on a black-figure ink tablet (palette 1 indices).
    hm = [
        "aaaaaaaaaaaaaaaa",
        "a11111111111111a",
        "1111111111111111",
        "1111111111111111",
        "1111111111111111",
        "11fb11fb1fb11fb1",
        "11fb11fb1ffbffb1",
        "11fffffb1fbfbfb1",
        "11fbbbfb1fbbbfb1",
        "11fb11fb1fb11fb1",
        "11bb11bb1bb11bb1",
        "1111111111111111",
        "1111111111111111",
        "1111111111111111",
        "a11111111111111a",
        "aaaaaaaaaaaaaaaa",
    ]
    key = {"a": 10, "1": 2, "f": 15, "b": 11}
    a = np.array([[key[ch] for ch in row] for row in hm], np.uint8)
    write_indexed_png(OUT / "hm.png", a, [TEXT])
    # SELECT tag: ink letters on a gold tab, as a stamped bronze label.
    sel = [
        "aaaaaaaaaaaaaaaaaaaaaaaa",
        "aaaaaaaaaaaaaaaaaaaaaaaa",
        "aaa111111111111111111aaa",
        "aa11555555555555555511aa",
        "a1155115115155551115511a",
        "a1555155155155511111551a",
        "a1555155155155111111151a",
        "a1555115115155111111151a",
        "a1555515155155111111151a",
        "a1555515155155511111551a",
        "a1155115115115551115511a",
        "aa11555555555555555511aa",
        "aaa111111111111111111aaa",
        "aaaaaaaaaaaaaaaaaaaaaaaa",
        "aaaaaaaaaaaaaaaaaaaaaaaa",
        "aaaaaaaaaaaaaaaaaaaaaaaa",
    ]
    key = {"a": 10, "1": 1, "5": 5}
    a = np.array([[key[ch] for ch in row] for row in sel], np.uint8)
    write_indexed_png(OUT / "select_button.png", a, [TEXT])


def preview(c, entries, ts):
    rgb = render_map(entries, ts.tiles, [BG, TEXT], 30, 20)
    save_rgb(IMG / "ui_bag_bg.png", rgb, 2)


# The berry tag screen (Bag > Berries > CHECK TAG) and its palettes are drawn by
# ui_berry_tag.py, which redrew Emerald's tag as a clay label.


if __name__ == "__main__":
    c, ts, entries = write_bag_bg()
    write_coin_sprite()
    write_badges()
    preview(c, entries, ts)
