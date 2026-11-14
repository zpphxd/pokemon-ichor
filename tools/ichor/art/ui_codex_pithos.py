#!/usr/bin/env python3
"""The Pithos (the storage system) around its jars: the PKMN DATA panel, the
YOUR PARTY tray, the lid button, the scrolling clay behind, the menus, and the
hand that reaches into the jar. The jars themselves are ui_codex_jars.py.

Writes, in graphics/pokemon_storage/:
  menu.png, interface.pal, party_menu.pal, pkmn_data_gray.pal
  display_menu.bin   the left panel (BG1, tiles from 0x100)
  pkmn_data.bin      its label: lit (palette 0) and dimmed (palette 2)
  party_menu.bin     the party tray; its last two rows are the YOUR PARTY tab
  party_slot_filled.bin, party_slot_empty.bin, close_box_button.bin
  scrolling_bg.png/.bin/.pal, scrolling_bg_move_items.pal
  text_windows.pal   the menus and messages: ink on parchment
  hand_cursor.png    the hand (its palette is the gold hand of auto-action
                     and the jar picker), waveform.png (the oil lamps beside
                     PKMN DATA; its palette is the everyday hand's)

How the engine uses them (src/pokemon_storage_system.c):
  - BG1 loads menu.png at tile 0x100; maps add 0x100 to every index.
  - The info window under the portrait (cols 0-8, rows 11-17) prints in BG
    palette 3 (scrolling_bg.pal): fill 1, text 2 shadow 3, male 4/5, female
    6/7. The scrolling clay uses 8-10 of the same palette.
  - The party tray slides down from above; its rows 20-21 are the tab seen
    at the top. Slots: the lead at (1,7), the rest at (7, 1+3k), 4x3 tiles.
  - The lid button's rows 0-1 are its normal state, rows 2-3 its flash.
"""
import numpy as np

from ui_codex_lib import *  # noqa: F401,F403

OUT = ROOT / "graphics/pokemon_storage"
IMG = ROOT / "design/phase1/img"

# BG palette 0 (interface.pal); the party tray's palette 1 is the same.
IK, CD, CL, CLL, PL, PA, PS, PD, BD, BR, BL, GO, GP, RG, GZ = range(1, 16)
INTERFACE = pal16([INK, INK, CLAY_DARK, CLAY, CLAY_LIGHT, PARCH_LIGHT, PARCHMENT,
                   PARCH_SHADE, PARCH_DARK, BRONZE_DARK, BRONZE, BRONZE_LIGHT, GOLD, GOLD_PALE,
                   RING, GLAZE])
# Palette 2 dims the PKMN DATA label when no Pokemon is shown: its gold
# lettering (GP) goes to dull bronze.
DIMMED = list(INTERFACE)
DIMMED[GP] = BRONZE_DARK
DIMMED[GO] = BRONZE_DARK


def board(c, x, y, w, h):
    clay_field(c, x, y, w, h, CL, RG)


def plate(c, x, y, w, h, face=CD, light=CL, shade=IK, outline=IK):
    """A clay plate with clipped corners."""
    c.rect(x + 1, y, w - 2, h, outline)
    c.rect(x, y + 1, w, h - 2, outline)
    c.rect(x + 1, y + 1, w - 2, h - 2, face)
    c.hline(x + 2, y + 1, w - 4, light)
    c.hline(x + 2, y + h - 2, w - 4, shade if shade != outline else face)


def label(c, x, y, w, s, fg, shadow, font="narrow"):
    tw = text_width(s, font)
    draw_text(c, x + (w - tw) // 2, y, s, fg, shadow, font=font)


def socket(c, x, y, w, h, filled):
    """A party slot: a parchment seat when filled, an incised socket when not."""
    if filled:
        c.frame(x, y, w, h, IK)
        c.rect(x + 1, y + 1, w - 2, h - 2, PA)
        c.hline(x + 1, y + 1, w - 2, PL)
        c.vline(x + 1, y + 1, h - 2, PL)
        c.hline(x + 1, y + h - 2, w - 2, PS)
        c.vline(x + w - 2, y + 2, h - 3, PS)
    else:
        c.rect(x, y, w, h, CD)
        c.hline(x, y, w, IK)
        c.vline(x, y, h, IK)
        c.hline(x + 1, y + h - 1, w - 1, CLL)
        c.vline(x + w - 1, y + 1, h - 1, CLL)


# --- The left panel ------------------------------------------------------------
def paint_display():
    c = Canvas(256, 160)
    board(c, 0, 0, 80, 160)
    c.vline(79, 0, 160, IK)
    c.vline(78, 0, 160, CD)
    # Header: an ink cartouche for PKMN DATA, flanked by the lamps (sprites).
    pkmn_data_label(c, GP)
    # Portrait: a parchment niche in a bronze frame (rows 2-10).
    c.frame(4, 18, 70, 70, IK)
    bevel_rect(c, 5, 19, 68, 68, BR, BL, BD)
    c.frame(8, 22, 62, 62, IK)
    c.rect(9, 23, 60, 60, PS)
    c.hline(9, 23, 60, PD)
    c.vline(9, 23, 60, PD)
    for (x, y) in [(5, 19), (70, 19), (5, 84), (70, 84)]:
        c.rect(x, y, 3, 3, GO)
        c.px(x, y, GP)
    # Info panel (window cols 0-8, rows 11-17): its frame on col 9 and row 18.
    c.rect(0, 88, 78, 64, IK)
    c.rect(1, 89, 76, 62, PA)       # behind the window; the window paints over it
    c.vline(73, 88, 64, IK)
    c.rect(74, 88, 4, 64, CD)
    c.hline(0, 144, 78, IK)
    # Row 18-19: the markings sit on a parchment strip.
    c.rect(1, 145, 72, 14, PA)
    c.hline(1, 145, 72, PL)
    c.hline(0, 159, 78, IK)
    return c


def pkmn_data_label(c, letters):
    cartouche(c, 6, 1, 66, 14, IK)
    c.hline(8, 2, 62, GZ)
    label(c, 6, 0, 66, "PKMN DATA", letters, BD)


def paint_pkmn_data():
    """The label alone, 8x2 tiles at (1,0): palette 0 lit, palette 2 dimmed."""
    c = Canvas(64, 32)
    sub = Canvas(80, 16)
    board(sub, 0, 0, 80, 16)
    pkmn_data_label(sub, GP)
    c.paste(sub.a[:, 8:72], 0, 0)
    c.paste(sub.a[:, 8:72], 0, 16)
    m = c.a[16:32] != 0
    c.a[16:32][m] = (c.a[16:32][m] & 15) | 0x20
    return c


# --- Top buttons -----------------------------------------------------------------
def paint_close_button():
    """CLOSE THE LID, 72x16 at (21,0); rows 2-3 are the flash."""
    c = Canvas(72, 32)
    for i, (face, light, fg, sh) in enumerate([(CD, CL, PL, IK), (GO, GP, IK, BD)]):
        y = 16 * i
        board(c, 0, y, 72, 16)
        plate(c, 0, y + 1, 72, 14, face, light)
        label(c, 0, y, 72, "CLOSE THE LID", fg, sh)
    return c


# --- The party tray --------------------------------------------------------------
def paint_party():
    """12x22 tiles: the tray (rows 0-19) and its YOUR PARTY tab (rows 20-21)."""
    c = Canvas(96, 176)
    # The tray: a clay board edged in ink, a meander along its foot.
    board(c, 0, 0, 96, 160)
    c.vline(0, 0, 160, IK)
    c.vline(95, 0, 160, IK)
    c.vline(1, 0, 160, CLL)
    c.vline(94, 0, 160, CD)
    meander_band(c, 1, 152, 94, IK, CD)
    # The lead's slot and the five beside it (filled; the code swaps in the
    # empty socket where a slot has no Pokemon).
    socket(c, 8, 56, 32, 24, True)
    for k in range(5):
        socket(c, 56, 8 + 24 * k, 32, 24, True)
    # CANCEL at rows 17-18, columns 7-10.
    plate(c, 54, 137, 36, 14, CD, CL)
    label(c, 54, 136, 36, "CANCEL", PL, IK)
    # The tab.
    board(c, 0, 160, 96, 16)
    plate(c, 0, 161, 72, 14, CD, CL)
    label(c, 0, 160, 72, "YOUR PARTY", PL, IK)
    c.rect(72, 160, 24, 16, 0)
    return c


def paint_slots():
    c = Canvas(64, 24)
    board(c, 0, 0, 64, 24)
    socket(c, 0, 0, 32, 24, True)
    socket(c, 32, 0, 32, 24, False)
    return c


# --- Scrolling clay behind the jars ------------------------------------------------
def scrolling_bg():
    """A 32x16 repeat: Corinthian filler rosettes on ringed clay (palette 3,
    colors 8-10). The code scrolls it diagonally."""
    c = Canvas(32, 16)
    c.rect(0, 0, 32, 16, 8)
    c.hline(0, 7, 32, 9)
    c.hline(0, 15, 32, 9)
    for (x, y) in [(8, 3), (24, 11)]:
        for (dx, dy) in [(0, -2), (-2, 0), (2, 0), (0, 2)]:
            c.px(x + dx, y + dy, 10)
        c.px(x, y, 10)
    return c


def write_scrolling():
    c = scrolling_bg()
    ts = TileSet(reserved=0, flips=False)
    tiles = [ts.add(t)[0] for t in tiles_of(c.a)]
    m = np.zeros((32, 32), np.uint16)
    for ty in range(32):
        for tx in range(32):
            m[ty, tx] = tiles[(ty % 2) * 4 + tx % 4] | (3 << 12)
    base = [TRANSPARENT, PARCHMENT, INK_TEXT, PARCH_SHADE, AEGEAN, AEGEAN_PALE,
            (192, 48, 32), (240, 176, 152)]
    clay = base + [CLAY, RING, CLAY_DARK]
    olive = base + [OLIVE, OLIVE_DARK, (40, 56, 24)]
    write_tiles_png(OUT / "scrolling_bg.png", ts.tiles, [pal16(clay)], tiles_wide=4)
    write_tilemap(OUT / "scrolling_bg.bin", m)
    write_jasc(OUT / "scrolling_bg.pal", pal16(clay))
    write_jasc(OUT / "scrolling_bg_move_items.pal", pal16(olive))


# --- Sprites: the hand and the lamps -------------------------------------------------
# The hand keeps Emerald's four poses (bounce, bounce, open, grip) and their
# fingertip positions, recolored red-figure: clay skin outlined in ink. Pixel
# roles: 1 outline, 2 dark, 3 skin, 11 mid, 12 shade. The shadow uses 8 and 15.
HAND_EVERYDAY = {1: INK, 2: CLAY_DARK, 3: CLAY_LIGHT, 11: CLAY, 12: (152, 64, 32),
                 8: GLAZE, 15: INK}
HAND_GOLD = {1: INK, 2: GOLD_DARK, 3: GOLD_PALE, 11: GOLD, 12: BRONZE,
             4: PARCHMENT, 5: PARCH_LIGHT, 6: CLAY, 7: INK}   # 4-7: the jar picker


def lamp(c, x, flip, lit, phase):
    """An oil lamp (lychnos), 16x8, nozzle toward the label."""
    rows = [
        "                ",
        "                ",
        "                ",
        "    oooooo      ",
        "  oo777777ooo   ",
        " o77777777777o  ",
        "  oo888888ooo   ",
        "    oooooo      ",
    ]
    if flip:
        rows = [r[::-1] for r in rows]
    c.grid(x, 0, rows, {"o": 1, "7": 7, "8": 8})
    if lit:
        fx = x + (13 if not flip else 2)
        flame = [[".4.", "454", "565"], ["4..", "45.", "565"], [".4.", ".45", "565"]][phase]
        for j, row in enumerate(flame):
            for i, ch in enumerate(row):
                if ch != ".":
                    c.px(fx - 1 + i, 1 + j, int(ch))


def write_sprites():
    hand = np.array(Image.open(OUT / "hand_cursor.png"))
    write_indexed_png(OUT / "hand_cursor.png", hand, [pal16([TRANSPARENT] + [HAND_GOLD.get(i, (0, 0, 0)) for i in range(1, 16)])])
    shadow = np.array(Image.open(OUT / "hand_cursor_shadow.png"))
    everyday = pal16([TRANSPARENT] + [HAND_EVERYDAY.get(i, (0, 0, 0)) for i in range(1, 16)])
    everyday[4], everyday[5], everyday[6], everyday[7] = GOLD_PALE, GOLD, (232, 120, 40), BRONZE
    write_indexed_png(OUT / "hand_cursor_shadow.png", shadow, [everyday])
    # Lamps: frames 0 (left, unlit), 2/4/6 (left, flickering), 8 (right,
    # unlit), 10/12 (right, flickering). Each frame is 16x8 (two tiles).
    c = Canvas(16, 56)
    frames = [(False, False, 0), (False, True, 0), (False, True, 1), (False, True, 2),
              (True, False, 0), (True, True, 1), (True, True, 2)]
    for i, (flip, lit, ph) in enumerate(frames):
        sub = Canvas(16, 8)
        lamp(sub, 0, flip, lit, ph)
        c.paste(sub, 0, 8 * i)
    write_indexed_png(OUT / "waveform.png", c.a, [everyday])
    # The box picker shares the gold hand's palette; keep its own .pal in step.
    write_jasc(OUT / "box_selection_popup.pal", pal16([TRANSPARENT] + [HAND_GOLD.get(i, (0, 0, 0)) for i in range(1, 16)]))
    for name in ("box_selection_popup_center.png", "box_selection_popup_sides.png"):
        a = np.array(Image.open(OUT / name))
        write_indexed_png(OUT / name, a, [pal16([TRANSPARENT] + [HAND_GOLD.get(i, (0, 0, 0)) for i in range(1, 16)])])


# --- Compile ----------------------------------------------------------------------
def with_base(m):
    """BG1 maps index menu.png from tile 0x100."""
    out = m.copy()
    out = (out & 0xFC00) | ((out & 0x3FF) + 0x100)
    return out


def write_all():
    ts = TileSet(reserved=1)
    disp = compile_map(paint_display(), ts, 32, 20)
    disp[:, 10:] = 0
    data = compile_map(paint_pkmn_data(), ts, 8, 4)
    party = compile_map(paint_party(), ts, 12, 22, palette_of=lambda x, y: 1)
    slots = compile_map(paint_slots(), ts, 8, 3, palette_of=lambda x, y: 1)
    close = compile_map(paint_close_button(), ts, 9, 4)
    check_tiles(len(ts), 256, "graphics/pokemon_storage/menu.png")
    write_tiles_png(OUT / "menu.png", ts.tiles, [INTERFACE], tiles_wide=16)
    write_tilemap(OUT / "display_menu.bin", with_base(disp))
    write_tilemap(OUT / "pkmn_data.bin", with_base(data))
    write_tilemap(OUT / "party_menu.bin", with_base(party))
    write_tilemap(OUT / "party_slot_filled.bin", with_base(slots[:, 0:4]))
    write_tilemap(OUT / "party_slot_empty.bin", with_base(slots[:, 4:8]))
    write_tilemap(OUT / "close_box_button.bin", with_base(close))
    write_jasc(OUT / "interface.pal", INTERFACE)
    write_jasc(OUT / "party_menu.pal", INTERFACE)
    write_jasc(OUT / "pkmn_data_gray.pal", pal16(DIMMED))
    write_jasc(OUT / "display_menu.pal", INTERFACE)
    # Menus and messages print fill 1, text 2, shadow 3.
    write_jasc(OUT / "text_windows.pal", pal16([TRANSPARENT, PARCHMENT, INK_TEXT, PARCH_SHADE]))
    write_scrolling()
    write_sprites()
    return ts


if __name__ == "__main__":
    write_all()
