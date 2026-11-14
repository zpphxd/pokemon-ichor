#!/usr/bin/env python3
"""Draw Ichor's pottery UI: the dialogue box, the menu frame and the name box.

A terracotta band painted with a black-figure Greek key (meander), with a
saltire square at each corner and a dark incised line around a light-clay text
field. The tiles are drawn by hand below as 8x8 character grids; this script
only assembles them into the indexed PNGs the build converts.

Writes, in graphics/text_window/:
  message_box.png  field dialogue box (14 tiles) and BG palette 15 for text
  1.png            menu frame style 1, the default (optionsWindowFrameType 0)
  name_box.png     speaker name plaque that sits on the dialogue box
  signpost.png     marble stele frame for signs (text_pal1.pal, slots 10-15)
  2.png - 5.png    selectable variants: red-figure, white-ground, Aegean, bronze
  6.png - 20.png   vanilla frames, inner margin retinted to parchment

Usage: python3 tools/ichor/art/ui_frames.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "graphics/text_window"

# Master palette (design/phase1/PLAN.md). All values are multiples of 8.
INK = (32, 24, 24)            # black-figure ink
CLAY_DARK = (120, 48, 24)     # terracotta, dark
CLAY = (184, 88, 48)          # terracotta
CLAY_LIGHT = (224, 136, 88)   # terracotta, light
PARCHMENT = (232, 216, 176)   # limestone, light: the text field
PARCH_SHADE = (208, 184, 136) # limestone, mid: text shadow

# BG palette 15, shared by the dialogue box, every overworld text window and the
# name box. Indices 1-9 are the text printer's colors (TEXT_COLOR_WHITE is the
# field, DARK_GRAY the ink, LIGHT_GRAY its shadow); they are retuned so text
# stays high-contrast on parchment instead of white. 10-15 belong to the frame.
MSG_PAL = [
    (112, 200, 160),  # 0  transparent
    PARCHMENT,        # 1  TEXT_COLOR_WHITE: text field
    (56, 40, 32),     # 2  TEXT_COLOR_DARK_GRAY: ink text
    PARCH_SHADE,      # 3  TEXT_COLOR_LIGHT_GRAY: text shadow
    (192, 48, 32),    # 4  TEXT_COLOR_RED
    (224, 160, 120),  # 5  TEXT_COLOR_LIGHT_RED
    (56, 120, 32),    # 6  TEXT_COLOR_GREEN
    (176, 200, 120),  # 7  TEXT_COLOR_LIGHT_GREEN
    (40, 88, 176),    # 8  TEXT_COLOR_BLUE
    (168, 184, 208),  # 9  TEXT_COLOR_LIGHT_BLUE
    INK,              # 10 frame ink
    CLAY_DARK,        # 11 frame incised line
    CLAY,             # 12 frame clay
    CLAY_LIGHT,       # 13 frame clay highlight
    (248, 248, 240),  # 14 marble (spare)
    (240, 192, 64),   # 15 sun-gold (spare)
]
MSG_KEY = {" ": 0, "p": 1, "#": 10, "d": 11, ".": 12, "l": 13}

# BG palette for menu frame 1 (loaded to slot 14). The frame never relies on
# matching the window's fill color: its inner edge is the dark incised line, so
# it reads the same on parchment or on a screen whose text field is white.
# Index 15 stays the outermost outline as in every vanilla frame, because the
# DexNav search window redraws the frame with a palette that only lights 15.
FRAME_PAL = [
    (98, 197, 98),    # 0  transparent
    INK,              # 1  meander ink
    CLAY_DARK,        # 2  incised line
    CLAY,             # 3  clay
    CLAY_LIGHT,       # 4  clay highlight
] + [(0, 0, 0)] * 9 + [
    PARCHMENT,        # 14 field (centre tile)
    CLAY,             # 15 outline
]
FRAME_KEY = {" ": 0, "#": 1, "d": 2, ".": 3, "l": 4, "p": 14, "o": 15}

# --- The motif -------------------------------------------------------------
# One period of a running meander: a single 1 px line that hooks back on itself.
# It is 5 px tall and repeats every 8 px, so one tile holds exactly one unit.
# The tile is cut where only the top stroke crosses, so the band starts and
# stops on a stroke that leaves the corner cleanly instead of on a half hook.
MEANDER = [
    "#####.##",
    "....#.#.",
    ".####.#.",
    ".#....#.",
    ".######.",
]

# Top edge: outline, clay, meander, then the incised line that frames the text.
TOP = ["oooooooo"] + MEANDER + ["dddddddd", "pppppppp"]

# Left edge: the same meander turned to run down the side (rows of TOP become
# columns), so the key goes all the way round like a painted panel.
LEFT = ["o" + "".join(row[c] for row in MEANDER) + "dp" for c in range(8)]

# Top-left corner: a saltire square, the stop Attic painters set between
# runs of meander. The outer corner is clipped by a pixel to soften it.
CORNER = [
    " ooooooo",
    "o#####..",
    "o##.##..",
    "o#.#.#..",
    "o##.##..",
    "o#####..",
    "o.....dd",
    "o.....dp",
]

FIELD = ["pppppppp"] * 8
BLANK = ["        "] * 8


def hflip(t):
    return [r[::-1] for r in t]


def vflip(t):
    return t[::-1]


def check(t):
    assert len(t) == 8 and all(len(r) == 8 for r in t), t
    return t


def write_png(path, tiles_wide, tiles, palette, key, ink_is_outline):
    """tiles: list of 8x8 char grids, laid out row-major, tiles_wide per row."""
    rows = (len(tiles) + tiles_wide - 1) // tiles_wide
    im = Image.new("P", (tiles_wide * 8, rows * 8))
    px = im.load()
    for i, t in enumerate(tiles):
        check(t)
        ox, oy = (i % tiles_wide) * 8, (i // tiles_wide) * 8
        for y, row in enumerate(t):
            for x, ch in enumerate(row):
                if ch == "o":  # outline: frame index 15, or plain ink in palette 15
                    ch = "o" if ink_is_outline else "."
                px[ox + x, oy + y] = key[ch]
    flat = [v for c in palette for v in c]
    assert len(palette) == 16 and all(v % 8 == 0 for v in flat[3:]), "16 GBA-exact colors"
    im.putpalette(flat)
    im.save(path, bits=4)
    print(f"wrote {path.relative_to(ROOT)}")


def message_box():
    # Tile slots used by WindowFunc_DrawDialogueFrame (src/menu.c): 1 and 6 are
    # the corners, 3 and 5 sit beside them, 4 repeats along the top, 7 and 10
    # are the sides, 9 fills the column left of the text. The bottom row is the
    # top row flipped vertically. Slots 0, 2, 8, 11-13 are unused; keep them
    # blank.
    t = [BLANK] * 14
    t[1], t[3], t[4], t[5], t[6] = CORNER, TOP, TOP, TOP, hflip(CORNER)
    t[7], t[9], t[10] = LEFT, FIELD, hflip(LEFT)
    write_png(OUT / "message_box.png", 7, t, MSG_PAL, MSG_KEY, False)


def frame_1():
    # 3x3 tiles: corners, edges, and a centre the frame code never draws.
    t = [
        CORNER, TOP, hflip(CORNER),
        LEFT, FIELD, hflip(LEFT),
        vflip(CORNER), vflip(TOP), vflip(hflip(CORNER)),
    ]
    write_png(OUT / "1.png", 3, t, FRAME_PAL, FRAME_KEY, True)


def name_box():
    # 3x2 tiles (src/field_name_box.c): left cap, middle (tiled under the
    # name), right cap. The bottom row covers the dialogue box's top band, so
    # outside the plaque it repeats that band. Text is parchment (index 1) on an
    # ink plaque with a light-clay rim.
    body = [" ", "o", "l"] + ["#"] * 10 + ["l", "o", "p"]
    band = [" "] * 8 + TOP
    mid = ["".join(body[y] for _ in range(8)) for y in range(16)]
    cap = []
    for y in range(16):
        row = ""
        for x in range(8):
            if x < 4 or (x == 4 and y < 3) or (x == 5 and y < 2):
                row += band[y][x] if y >= 8 else " "
            elif x == 4 or (x == 5 and y < 3) or y in (1, 14):
                row += "o" if 1 <= y <= 14 else band[y][x]
            elif x == 5 or y in (2, 13):
                row += "l" if y < 15 else "p"
            else:
                row += body[y]
        cap.append(row)
    left, right = cap, [r[::-1] for r in cap]
    t = [left[:8], mid[:8], right[:8], left[8:], mid[8:], right[8:]]
    write_png(OUT / "name_box.png", 3, t, MSG_PAL, MSG_KEY, False)


# Sign frame: a marble stele with its key painted in Aegean blue, so signs read
# as stone beside the clay dialogue box. Same tiles as the dialogue box. Signs
# load std text palette 1 (text_pal1.pal); only its slots 10-15 are rewritten,
# so the white field and gray text it gives other screens are untouched.
SIGN_PAL_FRAME = {10: (248, 248, 240),   # marble, light (spare)
                  11: (216, 208, 192),   # marble: the band
                  12: (168, 160, 152),   # marble, dark: incised line
                  13: (48, 104, 176),    # Aegean blue: the key
                  14: (24, 56, 120),     # Aegean, dark (spare)
                  15: (168, 160, 152)}   # outer edge
SIGN_KEY = {" ": 0, "p": 1, ".": 11, "d": 12, "#": 13, "o": 15}


def signpost():
    pal_path = OUT / "text_pal1.pal"
    text = pal_path.read_bytes().decode()
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    for i, c in SIGN_PAL_FRAME.items():
        lines[3 + i] = "%d %d %d" % c
    pal_path.write_bytes(nl.join(lines).encode())
    pal = [tuple(map(int, l.split())) for l in lines[3:19]]
    # Slots used by WindowFunc_DrawSignFrame (src/menu.c): 0 corner, 1 top
    # beside it, 2 outer side, 3 inner side (the field column), 4 top edge.
    im_tiles = [CORNER, TOP, LEFT, FIELD, TOP]
    pal16 = [tuple(v - v % 8 for v in c) for c in pal]
    write_png(OUT / "signpost.png", 5, im_tiles, pal16, SIGN_KEY, True)


# Variants of frame 1: the same tiles, other pottery wares, as
# (ground, incised line, key). The outer edge takes the ground color: an edge
# in the key's color would fuse with the meander's outer stroke.
VARIANTS = {
    2: (INK, CLAY_DARK, CLAY),                               # red-figure: clay key on ink
    3: ((248, 248, 240), (168, 160, 152), INK),              # white-ground
    4: ((176, 216, 240), (48, 104, 176), (24, 56, 120)),     # Aegean
    5: ((240, 192, 64), (200, 144, 40), INK),                # bronze
}


def variants():
    t = [CORNER, TOP, hflip(CORNER), LEFT, FIELD, hflip(LEFT),
         vflip(CORNER), vflip(TOP), vflip(hflip(CORNER))]
    for n, (ground, line, key) in VARIANTS.items():
        pal = list(FRAME_PAL)
        pal[1], pal[2], pal[3], pal[4], pal[15] = key, line, ground, ground, ground
        write_png(OUT / f"{n}.png", 3, t, pal, FRAME_KEY, True)


def retint_vanilla_frames():
    # Frames 6-20 keep their Hoenn art for now, but their inner margin (index
    # 14, white in vanilla) is retinted to parchment so it meets the overworld
    # text field without a white ring.
    for n in range(6, 21):
        path = OUT / f"{n}.png"
        im = Image.open(path)
        pal = im.getpalette()[:48]
        pal[42:45] = PARCHMENT
        im.putpalette(pal)
        im.save(path, bits=4)
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    message_box()
    frame_1()
    name_box()
    signpost()
    variants()
    retint_vanilla_frames()
