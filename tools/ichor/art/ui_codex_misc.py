#!/usr/bin/env python3
"""Palettes that put the remaining standard windows into the pottery family.

  graphics/interface/std_menu.pal         The standard menu palette. Every
      screen that loads it into a window palette (the move relearner, the
      whiteout and save-error screens, the clear-save screen, link and trade
      windows) now prints ink on parchment, exactly as the dialogue box does.
      It is the dialogue box's palette (graphics/text_window/message_box.png)
      with its frame colors, so a window looks the same on either.
  graphics/interface/option_menu_text.pal The options screen's text: labels
      in incised clay, choices in ink, the chosen one in the dialogue box's
      red, all on parchment. The code darkens every row but the current one.
"""
from ui_codex_lib import *  # noqa: F401,F403

OUT = ROOT / "graphics/interface"

# The dialogue box's palette, slot for slot (ui_frames.py MSG_PAL):
# 1 parchment, 2 ink text, 3 its shadow, 4/5 red and its shadow, 6/7 green,
# 8/9 blue, then the frame's ink, clays, marble and gold.
MESSAGE_BOX = png_palette(ROOT / "graphics/text_window/message_box.png")[:16]


def write_std_menu():
    write_jasc(OUT / "std_menu.pal", [MESSAGE_BOX[0]] + [gba(c) for c in MESSAGE_BOX[1:16]])


def write_option_text():
    # option_menu.c prints labels in 2 with shadow 3, choices in 6 with
    # shadow 7, and the chosen one in 4 with shadow 5, on fill 1.
    write_jasc(OUT / "option_menu_text.pal", pal16([
        (0, 0, 0),
        PARCHMENT,          # 1 fill
        CLAY_DARK,          # 2 labels and the OPTION header
        PARCH_SHADE,        # 3 their shadow
        (192, 48, 32),      # 4 the chosen value: the dialogue box's red
        (224, 160, 120),    # 5 its shadow
        INK_TEXT,           # 6 the other values
        PARCH_SHADE,        # 7 their shadow
    ]))


if __name__ == "__main__":
    write_std_menu()
    write_option_text()
