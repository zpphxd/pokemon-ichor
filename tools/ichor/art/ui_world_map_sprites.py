#!/usr/bin/env python3
"""The sprites and frame that sit on the Aethos region map.

  cursor_small.png, cursor.pal  the map cursor: gold brackets that breathe
  cursor_large.png              the same, for the zoomed view (PokeNav only)
  fly_target_icons.png          fly marks: gold corner ticks round a glyph
                                you can fly to; nothing on one you can't, so
                                the painted glyph always shows
  brendan_icon.png, may_icon.png  "you are here": Theo's and Ianthe's heads
                                under the petasos, in their battle colors
  frame.png, frame.bin          the Fly map's BG1 frame, now empty: the
                                meander border is painted into the map itself

Usage: python3 tools/ichor/art/ui_world_map_sprites.py
"""
import numpy as np

from ui_menus_lib import (ROOT, INK, GOLD, GOLD_DARK, GOLD_PALE, MARBLE_LIGHT, TRANSPARENT,
                          write_indexed_png, write_jasc, save_rgb)

OUT = ROOT / "graphics/pokenav/region_map"
IMG = ROOT / "design/phase1/img"


def grid(rows, key):
    a = np.zeros((len(rows), len(rows[0])), np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            a[y, x] = key[ch]
    return a


# --- Cursor --------------------------------------------------------------------
# 16x16, centred on the 8x8 cell. Frame 0: brackets one pixel off the cell;
# frame 1: pulled in to touch it. The anim swaps them every 20 frames.
CURSOR_PAL = [TRANSPARENT, INK, GOLD, GOLD_PALE, MARBLE_LIGHT, GOLD_DARK] + [(0, 0, 0)] * 10
CK = {" ": 0, "#": 1, "g": 2, "y": 3, "w": 4, "G": 5}


def bracket_frame(size, inset):
    """Four gold L-brackets with an ink keyline, in a size x size frame."""
    a = np.zeros((size, size), np.uint8)
    lo, hi = inset, size - 1 - inset
    arm = max(3, (hi - lo) // 3)
    for (cx, cy, dx, dy) in [(lo, lo, 1, 1), (hi, lo, -1, 1), (lo, hi, 1, -1), (hi, hi, -1, -1)]:
        for k in range(arm + 1):
            for (x, y) in [(cx + dx * k, cy), (cx, cy + dy * k)]:
                a[y, x] = CK["y"] if k == 0 else CK["g"]
                # ink keyline on the outside of each arm
                ox, oy = (x, y - dy) if y == cy else (x - dx, y)
                if 0 <= ox < size and 0 <= oy < size and a[oy, ox] == 0:
                    a[oy, ox] = CK["#"]
        a[cy - dy if 0 <= cy - dy < size else cy, cx - dx if 0 <= cx - dx < size else cx] = CK["#"]
    return a


def cursors():
    small = np.vstack([bracket_frame(16, 1), bracket_frame(16, 2)])
    write_indexed_png(OUT / "cursor_small.png", small, [CURSOR_PAL])
    large = np.vstack([bracket_frame(32, 2), bracket_frame(32, 3), bracket_frame(32, 4)])
    write_indexed_png(OUT / "cursor_large.png", large, [CURSOR_PAL])
    write_jasc(OUT / "cursor.pal", CURSOR_PAL)
    return small


# --- Fly marks -------------------------------------------------------------------
# Frames (tile numbers): 0 8x8 can fly; 1-2 16x8; 3-4 8x16; 5 8x8 can't;
# 6-7 16x8 can't; 8-9 8x16 can't; 10-13 the Frontier's 16x16 outline (unused).
# The sheet is 16 px wide, so tile n sits at ((n % 2) * 8, (n // 2) * 8).
FLY_PAL = [TRANSPARENT, INK, GOLD, GOLD_PALE] + [(0, 0, 0)] * 12


def ticks(w, h):
    """Gold corner ticks round a w x h glyph, keylined in ink."""
    a = np.zeros((h, w), np.uint8)
    for (x, y) in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        a[y, x] = 3
        a[y, x + (1 if x == 0 else -1)] = 2
        a[y + (1 if y == 0 else -1), x] = 2
    return a


def fly_icons():
    sheet = np.zeros((56, 16), np.uint8)

    def put(tile, block):
        y, x = (tile // 2) * 8, (tile % 2) * 8
        sheet[y:y + 8, x:x + 8] = block

    t88 = ticks(8, 8)
    t168 = ticks(16, 8)
    t816 = ticks(8, 16)
    put(0, t88)
    put(1, t168[:, :8]), put(2, t168[:, 8:])
    put(3, t816[:8]), put(4, t816[8:])
    # 5-9: can't fly yet: left empty so the painted glyph shows clean
    t1616 = ticks(16, 16)
    for n, (yy, xx) in zip(range(10, 14), [(0, 0), (0, 8), (8, 0), (8, 8)]):
        put(n, t1616[yy:yy + 8, xx:xx + 8])
    write_indexed_png(OUT / "fly_target_icons.png", sheet, [FLY_PAL])


# --- "You are here": the hero's head under the petasos --------------------------
# Colors from graphics/trainers/palettes/{brendan,may}.pal (sprites_player.py).
SKIN_L, SKIN_M, SKIN_D = (248, 208, 168), (224, 160, 112), (168, 104, 72)
GOLD_D, GOLD_M, GOLD_L = (152, 96, 32), (208, 152, 48), (240, 200, 88)
BLUE_D, BLUE_M = (24, 56, 120), (48, 104, 176)
CREAM = (248, 240, 216)
HEAD_KEY = {" ": 0, "#": 1, "L": 2, "S": 3, "d": 4, "h": 5, "H": 6, "G": 7, "M": 8,
            "D": 9, "B": 10, "U": 11, "W": 12}

THEO = [
    "                ",
    "      ####      ",
    "     #GGMM#     ",
    "  ###GGMMMD###  ",
    " #GGGGMMMMMDDD# ",
    "  ############  ",
    "   #hhhhhhhh#   ",
    "   #hLLLLLLh#   ",
    "   #L#LLL#LS#   ",
    "   #LLLLLLLS#   ",
    "    #LLddLS#    ",
    "    #SLLLLS#    ",
    "   ##B#SS#B##   ",
    "  #BBBU##UBBB#  ",
    "  #UUUUUUUUUU#  ",
    "   ##########   ",
]
IANTHE = [
    "                ",
    "      ####      ",
    "     #GGMM#     ",
    "  ###GGMMMD###  ",
    " #GGGGMMMMMDDD# ",
    "  ############  ",
    "   #hhhhhhhh#   ",
    "   #hLLLLLLhh#  ",
    "   #L#LLL#LSH#  ",
    "   #LLLLLLLSh#  ",
    "    #LLddLSHh#  ",
    "    #SLLLLS#H#  ",
    "   ##B#SS#BHh#  ",
    "  #BBBU##UBHh#  ",
    "  #UUUUUUUUU##  ",
    "   ##########   ",
]


def head(rows, hair, sheen, name):
    pal = [TRANSPARENT, INK, SKIN_L, SKIN_M, SKIN_D, hair, sheen, GOLD_L, GOLD_M, GOLD_D,
           (112, 168, 224), BLUE_M, CREAM] + [(0, 0, 0)] * 3
    a = grid(rows, HEAD_KEY)
    write_indexed_png(OUT / f"{name}.png", a, [pal])
    return a, pal


# --- The Fly map's frame -----------------------------------------------------------
# The map paints its own meander border, so BG1 only frames the "FLY to where?"
# prompt at the bottom left (window 1,18 14x2, which runs off the screen's foot
# like Emerald's). It is the menu frame's own tiles and palette (ui_frames.py),
# so it matches the name window the engine frames beside it.
def frame():
    import ui_frames as uf
    pal = list(uf.FRAME_PAL)
    key = uf.FRAME_KEY

    def tile(rows):
        return grid(rows, key)

    tiles = [np.zeros((8, 8), np.uint8), tile(uf.CORNER), tile(uf.TOP), tile(uf.LEFT), tile(uf.FIELD)]
    sheet = np.zeros((16, 24), np.uint8)
    for i, t in enumerate(tiles):
        sheet[(i // 3) * 8:(i // 3) * 8 + 8, (i % 3) * 8:(i % 3) * 8 + 8] = t
    write_indexed_png(OUT / "frame.png", sheet, [[tuple(v - v % 8 for v in c) for c in pal]])
    HF, PAL1 = 0x400, 1 << 12
    m = np.zeros((20, 32), np.uint16)
    m[17, 0] = 1 | PAL1
    m[17, 1:15] = 2 | PAL1
    m[17, 15] = 1 | HF | PAL1
    m[18:20, 0] = 3 | PAL1
    m[18:20, 1:15] = 4 | PAL1
    m[18:20, 15] = 3 | HF | PAL1
    (OUT / "frame.bin").write_bytes(m.astype("<u2").tobytes())
    print("wrote graphics/pokenav/region_map/frame.bin")


def preview(small, theo, ianthe):
    tiles = []
    for a, pal in [(small[:16], CURSOR_PAL), (small[16:], CURSOR_PAL), theo, ianthe]:
        p = np.array(pal, np.uint8)
        rgb = p[a]
        rgb[a == 0] = (40, 24, 32)
        tiles.append(rgb)
    save_rgb(IMG / "ui_world_map_sprites.png", np.hstack(tiles), 6)


if __name__ == "__main__":
    s = cursors()
    fly_icons()
    t = head(THEO, (32, 24, 24), (72, 72, 104), "brendan_icon")
    i = head(IANTHE, (96, 56, 40), (152, 96, 64), "may_icon")
    frame()
    preview(s, t, i)
