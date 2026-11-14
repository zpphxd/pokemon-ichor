#!/usr/bin/env python3
"""Paint the battle text box and menus as the pottery dialogue box.

The battle message box is built from exactly the dialogue box's tiles
(tools/ichor/art/ui_frames.py): a terracotta band with the black-figure key,
saltire squares at the corners and a parchment field. The FIGHT/BAG menu and
the move list already draw the player's chosen menu frame (frame 1 is the
pottery frame); this script gives their text the same parchment field and
ink, and retunes the PP warning colors so they read on parchment.

It also redraws the "press A" arrow as a plain downward triangle: the old
blunt shield read as a red heart at 1x, in battle and in the field alike.

Writes:
  graphics/battle_interface/textbox.png, textbox_map.bin, textbox_0.pal,
    textbox_1.pal   BG0 of the battle: tiles, the three box layouts, palettes
  graphics/battle_interface/text.pal       BG palette 5: menu and move text
  graphics/battle_interface/text_pp.pal    PP colors by how much is left
  graphics/battle_interface/level_up_banner.png  the level-up plaque
  graphics/fonts/down_arrow.png, down_arrow_alt.png  the continue arrow

Usage: python3 tools/ichor/art/ui_battle_textbox.py
"""
import struct

from ui_battle_lib import (
    BI, CLAY, CLAY_DARK, CLAY_LIGHT, GOLD, INK, PARCHMENT, PARCH_SHADE, RED, ROOT,
    IdxCanvas, write_jasc,
)
from ui_frames import CORNER, FIELD, FRAME_PAL, LEFT, TOP

TEXT_INK = (56, 40, 32)   # the dialogue box's text color

# BG palette 0 in battle (also the evolution, egg hatch and trade scenes,
# which reuse the battle text box). Battle messages print with fg 1, shadow 6
# on fill 15; the egg hatch prints fg 5. Battle and evolution messages draw
# the dark continue arrow (down_arrow_alt.png: edge 1, fill 2), so it comes
# out ink-edged red like the field's; the plain arrow (edge 2, fill 4) is all
# red here.
TEXTBOX_PAL = [
    (0, 0, 0),       # 0  transparent
    TEXT_INK,        # 1  message text, dark arrow edge
    RED,             # 2  dark arrow fill, plain arrow edge
    PARCH_SHADE,     # 3
    RED,             # 4  plain arrow fill
    TEXT_INK,        # 5  egg hatch text
    PARCH_SHADE,     # 6  text shadow
    (0, 0, 0), (0, 0, 0), (0, 0, 0),
    INK,             # 10 the key
    CLAY_DARK,       # 11 incised line
    CLAY,            # 12 clay band
    CLAY_LIGHT,      # 13
    (0, 0, 0),
    PARCHMENT,       # 15 field
]
KEY = {" ": 0, "p": 15, "#": 10, "d": 11, ".": 12, "l": 13, "o": 12}

# Tiles of textbox.png. Tiles 1-2 are the menu cursor (action menu, move list,
# YES/NO): the game draws them with this palette 0, on the menus' parchment.
T_BLANK, T_CURSOR_TOP, T_CURSOR_BOTTOM, T_CORNER, T_TOP, T_SIDE, T_FIELD = range(7)
HFLIP, VFLIP = 0x400, 0x800

CURSOR = [
    "........", "........", "........", "........",
    ".#......", ".##.....", ".###....", ".####...",
    ".#####..", ".####...", ".###....", ".##.....",
    ".#......", "........", "........", "........",
]


def textbox_png():
    c = IdxCanvas(128, 8)
    c.blit(8 * T_CURSOR_TOP, 0, CURSOR[:8], {".": 15, "#": 1})
    c.blit(8 * T_CURSOR_BOTTOM, 0, CURSOR[8:], {".": 15, "#": 1})
    for i, t in ((T_CORNER, CORNER), (T_TOP, TOP), (T_SIDE, LEFT), (T_FIELD, FIELD)):
        c.blit(8 * i, 0, t, KEY)
    return c


def box(entries, top, left, right, close_right=True):
    """Lay a framed box on the 32-wide map: rows top..top+5, cols left..right."""
    def put(r, col, tile, flags=0):
        entries[r * 32 + col] = tile | flags
    bottom = top + 5
    put(top, left, T_CORNER)
    put(bottom, left, T_CORNER, VFLIP)
    last = right - 1 if close_right else right
    for col in range(left + 1, last + 1):
        put(top, col, T_TOP)
        put(bottom, col, T_TOP, VFLIP)
    for r in range(top + 1, bottom):
        put(r, left, T_SIDE)
        for col in range(left + 1, last + 1):
            put(r, col, T_FIELD)
    if close_right:
        put(top, right, T_CORNER, HFLIP)
        put(bottom, right, T_CORNER, HFLIP | VFLIP)
        for r in range(top + 1, bottom):
            put(r, right, T_SIDE, HFLIP)


def textbox_map():
    """Keep vanilla's three layouts (message, action, move list); repaint the
    message-box parts, which use palette 0. The menu boxes keep their
    palette-1 entries, tiles 0x12-0x1A, where the game loads the menu frame."""
    path = BI / "textbox_map.bin"
    entries = list(struct.unpack("<2048H", path.read_bytes()))
    for i, e in enumerate(entries):
        if e >> 12 == 0:
            entries[i] = 0
    box(entries, 14, 0, 29)                      # plain message box
    box(entries, 34, 0, 14, close_right=False)   # beside the action menu
    path.write_bytes(struct.pack("<2048H", *entries))
    print(f"wrote {path.relative_to(ROOT)}")


# BG palette 5: the action menu (fg 13, shadow 15, fill 14), the move names,
# the move type and PP (fg 12, shadow 11, rewritten from text_pp.pal).
def text_pal():
    vanilla = [(0, 0, 0), (248, 0, 0), (128, 0, 0), (248, 160, 96), (128, 80, 48)]
    return vanilla + [(0, 0, 0)] * 6 + [PARCH_SHADE, TEXT_INK, TEXT_INK, PARCHMENT, PARCH_SHADE]


# Pairs of (text, shadow) by PP state: half or less, a quarter or less, none,
# and plenty. Darker than vanilla's yellows so they read on parchment (and on
# the summary screen's white, which loads the same file).
PP_STATES = [
    ((152, 96, 0), GOLD),
    ((184, 72, 8), (240, 176, 128)),
    ((176, 32, 24), (232, 160, 136)),
    (TEXT_INK, PARCH_SHADE),
]


def text_pp_pal():
    pal = [c for pair in PP_STATES for c in pair]
    return pal + [(0, 0, 0)] * (16 - len(pal))


# --- Level-up plaque (BG palette 6; the window prints fg 1, shadow 2) --------
def level_up_banner():
    pal = [(0, 0, 0), TEXT_INK, PARCH_SHADE, INK, PARCHMENT, CLAY_LIGHT, CLAY,
           CLAY_DARK] + [(0, 0, 0)] * 8
    c = IdxCanvas(96, 24)
    c.rect(0, 0, 95, 23, 6)                 # clay rim
    c.rect(1, 1, 94, 22, 7)                 # incised line
    c.rect(2, 2, 93, 21, 4)                 # parchment field
    c.rect(2, 13, 93, 21, 5)                # lower band in light clay
    c.hline(2, 93, 12, 7)
    for x, y in ((0, 0), (95, 0), (0, 23), (95, 23)):
        c.set(x, y, 0)
    return c, pal


# --- The continue arrow -------------------------------------------------------
ARROW = [
    ".eeeeeee",
    ".efffffe",
    "..efffe.",
    "...efe..",
    "....e...",
]


def arrow_png(edge, fill, pal):
    """8x48: the arrow repeated every 16 rows (the game blits a 16-row
    window starting 0-2 rows down to make it bob)."""
    c = IdxCanvas(8, 48)
    for k in range(3):
        c.blit(0, 16 * k + 5, ARROW, {"e": edge, "f": fill})
    return c, pal


def main():
    textbox_png().save(BI / "textbox.png", TEXTBOX_PAL)
    textbox_map()
    write_jasc(BI / "textbox_0.pal", TEXTBOX_PAL)
    write_jasc(BI / "textbox_1.pal", FRAME_PAL)
    write_jasc(BI / "text.pal", text_pal())
    write_jasc(BI / "text_pp.pal", text_pp_pal())
    c, pal = level_up_banner()
    c.save(BI / "level_up_banner.png", pal)
    fonts = ROOT / "graphics/fonts"
    from ui_battle_lib import read_png_palette
    c, pal = arrow_png(2, 4, read_png_palette(fonts / "down_arrow.png"))
    c.save(fonts / "down_arrow.png", [tuple(v - v % 8 for v in p) for p in pal])
    c, pal = arrow_png(1, 2, read_png_palette(fonts / "down_arrow_alt.png"))
    c.save(fonts / "down_arrow_alt.png", [tuple(v - v % 8 for v in p) for p in pal])


if __name__ == "__main__":
    main()
