#!/usr/bin/env python3
"""The naming screen as a writing tablet: the name is written on a parchment
strip in a wooden frame with a bronze stylus beside it, and the keyboard is
a wax tablet (pinax) whose letters are cut light into the wax. Each keyboard
page is its own wax: dark (UPPER), red (lower) and olive (others).

Writes, in graphics/naming_screen/:
  menu.png             the BG tiles (the engine copies 48 tiles, 0x600 bytes)
  background.bin       the desk and the name strip (BG3)
  keyboard_upper.bin, keyboard_lower.bin, keyboard_symbols.bin   the tablets
                       (BG1/BG2), the same tiles in palettes 1, 2 and 3
  menu.pal             BG palette 0 (and the jar icon's sprite palette)
  page_swap_upper/lower/others.pal   the tablets' wood and wax rims
  keyboard.pal         BG palette 10: the name strip's ink, the key letters,
                       the three waxes (window fills 13, 14, 15)
  banner.pal           BG palette 11 for the controls banner (ink band)
  buttons.pal, cursor.pal            the BACK/OK keys, page tags, cursor
  pc_icon_off.png, pc_icon_on.png    "sent to the Pithos": a small jar

src/naming_screen.c loads banner.pal for the banner instead of the shared
text_pal2 (an Ichor edit), so the blue Hoenn bar becomes an ink band.
"""
import numpy as np

from ui_codex_lib import *  # noqa: F401,F403

OUT = ROOT / "graphics/naming_screen"

# BG palette 0.
PL, PA, PS, PD, IK, CD, CL, CLL, RG, BD, BR, BL, GO, GP, TX = range(1, 16)
MENU = pal16([INK, PARCH_LIGHT, PARCHMENT, PARCH_SHADE, PARCH_DARK, INK, CLAY_DARK, CLAY,
              CLAY_LIGHT, RING, BRONZE_DARK, BRONZE, BRONZE_LIGHT, GOLD, GOLD_PALE, INK_TEXT])

WAX = {"upper": GLAZE, "lower": (136, 48, 32), "others": (72, 80, 40)}
WAX_DARK = {"upper": (40, 24, 24), "lower": (96, 32, 24), "others": (48, 56, 24)}

# Tablet palettes 1-3: 11 outline, 12-14 wood, 15 the wax showing at the rim.
# 1-3 are the input arrow's and underscore's colors on the name strip.
def tablet_pal(page):
    return pal16([TRANSPARENT, PARCH_LIGHT, INK_TEXT, PARCH_DARK, (0, 0, 0), (0, 0, 0), (0, 0, 0),
                  (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                  INK, BRONZE_DARK, BRONZE, BRONZE_LIGHT, WAX[page]])


T_IK, T_WD, T_W, T_WL, T_WAX = 11, 12, 13, 14, 15


def paint_background():
    c = Canvas(256, 160)
    clay_field(c, 0, 0, 256, 160, CL, RG)
    meander_band(c, 0, 17, 240, IK, CL)
    rays_band(c, 0, 152, 240, IK, CL)
    # The name strip: parchment in a wooden frame, cols 4-25, rows 3-8.
    x, y, w, h = 32, 24, 176, 48
    c.rect(x + 2, y + 2, w - 4, h - 4, IK)
    c.rect(x + 3, y + 3, w - 6, h - 6, BR)
    c.hline(x + 3, y + 3, w - 6, BL)
    c.vline(x + 3, y + 3, h - 6, BL)
    c.hline(x + 3, y + h - 4, w - 6, BD)
    c.vline(x + w - 4, y + 3, h - 6, BD)
    c.rect(x + 6, y + 6, w - 12, h - 12, IK)
    c.rect(x + 7, y + 7, w - 14, h - 14, PL)
    # Where the writer stands (the icon at 48-63, 29-52): a shadow on the strip.
    for yy in range(50, 54):
        half = [5, 7, 7, 5][yy - 50]
        c.hline(56 - half, yy, 2 * half, PS)
    # The stylus, bronze with a bone point, leaning beside the strip.
    for i in range(34):
        x0, y0 = 214 + i // 3, 26 + i
        c.px(x0, y0, IK)
        c.px(x0 + 1, y0, BL if i < 28 else PL)
        c.px(x0 + 2, y0, BR if i < 28 else PS)
        c.px(x0 + 3, y0, IK)
    c.rect(214, 24, 4, 3, BD)
    c.hline(214, 23, 4, IK)
    return c


def paint_tablet():
    """The wax tablet's wooden frame: cols 2-22, rows 9-18, with a handle lug
    at the top right (cols 22-23, rows 9-12). The window covers cols 3-21,
    rows 10-17 with the wax."""
    c = Canvas(256, 160)
    P = 16
    x0, y0, x1, y1 = 16, 72, 184, 152  # outer box (exclusive right/bottom)
    c.rect(x0, y0, x1 - x0, y1 - y0, P + T_IK)
    c.rect(x0 + 1, y0 + 1, x1 - x0 - 2, y1 - y0 - 2, P + T_W)
    c.hline(x0 + 1, y0 + 1, x1 - x0 - 2, P + T_WL)
    c.vline(x0 + 1, y0 + 1, y1 - y0 - 2, P + T_WL)
    c.hline(x0 + 1, y1 - 2, x1 - x0 - 2, P + T_WD)
    c.vline(x1 - 2, y0 + 1, y1 - y0 - 2, P + T_WD)
    # The wax well, sunk into the wood: its rim shows the page's wax.
    c.rect(22, 78, 156, 68, P + T_IK)
    c.rect(23, 79, 154, 66, P + T_WAX)
    # The handle lug with its cord hole.
    lx, ly = 184, 72
    c.rect(lx - 1, ly, 13, 30, P + T_IK)
    c.rect(lx - 1, ly + 1, 12, 28, P + T_W)
    c.hline(lx - 1, ly + 1, 12, P + T_WL)
    c.vline(lx + 10, ly + 1, 28, P + T_WD)
    c.hline(lx - 1, ly + 28, 12, P + T_WD)
    c.rect(lx + 3, ly + 10, 4, 4, P + T_IK)
    return c


def write_bg():
    ts = TileSet(reserved=1)
    bg = compile_map(paint_background(), ts, 32, 20)
    tab = compile_map(paint_tablet(), ts, 32, 20)
    check_tiles(len(ts), 48, "graphics/naming_screen/menu.png")
    write_tiles_png(OUT / "menu.png", ts.tiles + [np.zeros((8, 8), np.uint8)] * (48 - len(ts.tiles)),
                    [MENU], tiles_wide=3)
    write_tilemap(OUT / "background.bin", bg)
    for name, pal in [("keyboard_upper", 1), ("keyboard_lower", 2), ("keyboard_symbols", 3)]:
        m = tab.copy()
        nz = (m & 0x3FF) != 0
        m[nz] = (m[nz] & 0x0FFF) | (pal << 12)
        write_tilemap(OUT / f"{name}.bin", m)


def write_palettes():
    write_jasc(OUT / "menu.pal", MENU)
    for page in ("upper", "lower", "others"):
        write_jasc(OUT / f"page_swap_{page}.pal", tablet_pal(page))
    # keyboard.pal: the name strip prints 2 on 1 with shadow 3; keys print 1
    # with shadow 2 on the page's wax (13 UPPER, 14 lower, 15 others); the
    # gender mark uses 4/5 (female) and 8/9 (male).
    write_jasc(OUT / "keyboard.pal", pal16([
        PARCH_LIGHT, PARCH_LIGHT, INK_TEXT, PARCH_SHADE,
        (192, 48, 32), (232, 152, 136), (56, 120, 32), (176, 200, 120),
        AEGEAN, AEGEAN_LIGHT, (0, 0, 0), (0, 0, 0), (0, 0, 0),
        WAX["upper"], WAX["lower"], WAX["others"]]))
    # The controls banner prints 1 with shadow 2 on 15.
    write_jasc(OUT / "banner.pal", pal16([TRANSPARENT, PARCH_LIGHT, CLAY_DARK, PARCH_SHADE] + [(0, 0, 0)] * 11 + [INK]))
    # Buttons and page tags: clay plates lettered in parchment (1, 3, 4), the
    # three waxes for the page tags (6/7, 8/9, 10/11), gold BACK and OK keys
    # (12 letters, 13 face); 14 is the flash the code animates.
    write_jasc(OUT / "buttons.pal", pal16([
        TRANSPARENT, PARCH_LIGHT, INK, CLAY_DARK, CLAY, PARCH_LIGHT,
        WAX_DARK["upper"], WAX["upper"], WAX_DARK["lower"], WAX["lower"],
        WAX_DARK["others"], WAX["others"], BRONZE_DARK, GOLD, INK, INK]))
    # The key cursor: sun-gold.
    write_jasc(OUT / "cursor.pal", pal16([TRANSPARENT, GOLD, GOLD_DARK, GOLD_DARK] + [(0, 0, 0)] * 8 +
                                         [PARCH_LIGHT, (0, 0, 0), PARCH_LIGHT, (0, 0, 0)]))


JAR = [
    "                ",
    "     oooooo     ",
    "    o333333o    ",
    "     oddddo     ",
    "    o333333o    ",
    "   o33333333o   ",
    "  o3llll33333o  ",
    "  o3lkkkkkk33o  ",
    " o3lk3k33k3k33o ",
    " o3lkkkkkkkk33o ",
    " o3l333333333do ",
    " o3l333333333do ",
    " o3lkkkkkkkkk3do",
    " o33k3k3k3k3kddo",
    "  o3kkkkkkkk3do ",
    "  o33333333ddo  ",
    "   o333333ddo   ",
    "    o33333do    ",
    "     o3ddo      ",
    "     oooooo     ",
    "    o333333o    ",
    "    oooooooo    ",
    "                ",
    "                ",
]


def write_pc_icons():
    """'Sent to the Pithos': a little pithos instead of a PC (menu.pal)."""
    for name, glint in [("pc_icon_off.png", False), ("pc_icon_on.png", True)]:
        c = Canvas(16, 24)
        c.grid(0, 0, JAR, {"o": IK, "3": CL, "d": CD, "l": CLL, "k": IK})
        if glint:
            c.grid(0, 0, JAR, {"o": IK, "3": CLL, "d": CL, "l": GP, "k": IK})
        write_indexed_png(OUT / name, c.a, [MENU])


def recolor_sprites():
    """Keep the shapes of the cursor, buttons, tags, arrow and underscore and
    give their PNGs the new palettes (the game reads the .pal files)."""
    for name, pal in [("back_button.png", "buttons.pal"), ("ok_button.png", "buttons.pal"),
                      ("page_swap_frame.png", "buttons.pal"), ("page_swap_button.png", "buttons.pal"),
                      ("page_swap_upper.png", "buttons.pal"), ("page_swap_lower.png", "buttons.pal"),
                      ("page_swap_others.png", "buttons.pal"), ("cursor.png", "cursor.pal"),
                      ("cursor_filled.png", "cursor.pal"), ("cursor_squished.png", "cursor.pal"),
                      ("input_arrow.png", "page_swap_others.pal"), ("underscore.png", "page_swap_others.pal")]:
        a = np.array(Image.open(OUT / name))
        write_indexed_png(OUT / name, a, [read_jasc(OUT / pal)])


if __name__ == "__main__":
    write_palettes()
    write_bg()
    write_pc_icons()
    recolor_sprites()
