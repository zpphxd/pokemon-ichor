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
  graphics/interface/main_menu_bg.pal, main_menu_text.pal   The title's
      main menu: a terracotta backdrop and sun-gold plates lettered in ink
      (main_menu.c reads these colors instead of hardcoding Emerald's).
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


def write_main_menu():
    """The title's main menu (NEW GAME, CONTINUE, OPTION) on terracotta.
    main_menu_bg.pal's color 0 is the backdrop. main_menu.c reads its window
    colors from main_menu_text.pal: fill 10, headers 11 with shadow 12, the
    Continue panel's details in 1 (Theo) or 13 (Ianthe), 14 spare. The fill is
    sun-gold: the selected plate shows it as it is, and the code lightens the
    others towards parchment."""
    write_jasc(OUT / "main_menu_bg.pal", pal16([CLAY, CLAY_DARK, CLAY_LIGHT, RING]))
    pal = [gba(c) for c in MESSAGE_BOX[:16]]
    pal[1] = AEGEAN_DARK            # Theo's details
    pal[10] = GOLD_PALE             # the plate
    pal[11] = INK_TEXT              # NEW GAME, CONTINUE, OPTION
    pal[12] = GOLD                  # their shadow
    pal[13] = (168, 32, 64)         # Ianthe's details
    pal[14] = INK
    write_jasc(OUT / "main_menu_text.pal", pal)


if __name__ == "__main__":
    write_std_menu()
    write_option_text()
    write_main_menu()
