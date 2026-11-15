#!/usr/bin/env python3
"""The Pokedex, drawn as a codex: parchment leaves inset in a terracotta board
with bronze corner caps, the family look of the pottery menus.

Writes, in graphics/pokedex/:
  menu.png                      the shared BG tiles (list, entry, cry, size,
                                select bars, the list's slide-up menu)
  list.bin, list_underlay.bin   the list screen (BG1 masks, BG3 base)
  info_screen.bin, cry_screen.bin, size_screen.bin
  screen_select_bar_main.bin, screen_select_bar_submenu.bin
  start_menu_main.bin, start_menu_search_results.bin
  bg_hoenn.pal (the AETHOS codex), bg_national.pal (ALL: black glaze),
  search_results_bg.pal (search results: olive)
  interface.png                 list sprites (counts, buttons, arrows)
  caught_ball.png, size_silhouette.pal, cry_meter*.png, cry_screen_bg.png,
  area_glow.png, area_marker.png

How the engine uses them (src/pokedex.c), which the art follows:
  - Every screen prints in BG palette 0: color 15 with shadow 3. The area
    labels fill with 7 and print 1 with shadow 5.
  - The interface sprites are colored with bg_hoenn.pal's palette 0.
  - The select bar's four tabs (7 tiles each, from column 1) are recolored by
    the code: palette 2 when selected, 4 when not. In the submenu bar the
    fourth (CANCEL) is always palette 2.
  - Palette 3 is the entry page's "owned" glow: for a Pokemon not caught the
    code copies palette 0 over it, and the caught page flickers colors 1-7
    between the two. Only the band between entry and description uses it.
  - Palette 5 color 13 is the cry page's play arrow, set by the code.
  - The cry waveform window sits under BG3 (rows 12-18), so those tiles are
    left transparent.
  - The list's names scroll on BG2 between BG1 and BG3: BG1 covers rows 0-1
    and 18-19 so names never show outside the list leaf.
"""
import numpy as np

from ui_codex_lib import *  # noqa: F401,F403

OUT = ROOT / "graphics/pokedex"
IMG = ROOT / "design/phase1/img"
W, H = 256, 160  # tilemaps are 32 tiles wide; the screen shows 30

# --- Palettes -----------------------------------------------------------------
# One index layout for all six BG palettes.
PL, PA, PS, PD, CD, FI, IK, FR, FZ, BL, BR, BD, GO, GP, TX = range(1, 16)

FIELDS = {
    # name: (field, ring)
    "aethos": (CLAY, RING),                    # terracotta: the Aethos codex
    "national": (GLAZE, (48, 32, 24)),         # black glaze: every Pokemon
    "search": (OLIVE_DARK, (40, 56, 24)),      # olive: a search's results
}


def palettes(variant):
    field, ring = FIELDS[variant]
    p0 = [TRANSPARENT, PARCH_LIGHT, PARCHMENT, PARCH_SHADE, PARCH_DARK, CLAY_DARK,
          field, INK, ring, CLAY, BRONZE_LIGHT, BRONZE, BRONZE_DARK, GOLD, GOLD_PALE, INK_TEXT]
    p1 = list(p0)
    p2 = list(p0)   # a selected tab, and the list's slide-up menu
    p2[BL], p2[BR], p2[BD], p2[GO], p2[GP] = GOLD_PALE, GOLD, GOLD_DARK, INK, GOLD_DARK
    p3 = list(p0)   # the owned glow on the entry page
    p3[PD], p3[CD] = GOLD, GOLD_DARK
    p4 = list(p0)   # an unselected tab
    p4[BL], p4[BR], p4[BD], p4[GO], p4[GP] = CLAY, CLAY_DARK, INK, PARCHMENT, INK
    p5 = list(p0)   # the play arrow (color 13, set by the code)
    p5[GO] = GOLD_DARK
    return [p0, p1, p2, p3, p4, p5]


def v(pal, idx):
    return pal * 16 + idx


# Canvas values in palette 0.
C_PL, C_PA, C_PS, C_PD, C_CD, C_FI, C_IK, C_FR, C_FZ, C_BL, C_BR, C_BD, C_GO, C_GP, C_TX = range(1, 16)


# --- Shared painters -------------------------------------------------------------
def repal(c, tx, ty, tw, th, pal):
    """Move every painted pixel of a block of tiles into palette pal."""
    sub = c.a[ty * 8:(ty + th) * 8, tx * 8:(tx + tw) * 8]
    m = (sub & 15) != 0
    sub[m] = (sub[m] & 15) | (pal << 4)


def board(c, x=0, y=0, w=W, h=H):
    clay_field(c, x, y, w, h, C_FI, C_FR)


def corner_key(pal=0):
    return {"o": v(pal, IK), "d": v(pal, BD), "b": v(pal, BR), "l": v(pal, BL),
            "g": v(pal, GP), "r": v(pal, BD)}


def caps(c, x, y, w, h, pal=0):
    """Bronze corner caps on the four corners of a w x h rectangle."""
    k = corner_key(pal)
    bronze_corner(c, x, y, k)
    bronze_corner(c, x + w - 8, y, k, flip_h=True)
    bronze_corner(c, x, y + h - 8, k, flip_v=True)
    bronze_corner(c, x + w - 8, y + h - 8, k, flip_h=True, flip_v=True)


def leaf(c, x, y, w, h, face=C_PA):
    """A parchment leaf: ink outline, lit top and left edge, shaded foot."""
    c.frame(x, y, w, h, C_IK)
    c.rect(x + 1, y + 1, w - 2, h - 2, face)
    c.hline(x + 1, y + 1, w - 2, C_PL)
    c.vline(x + 1, y + 1, h - 2, C_PL)
    c.hline(x + 1, y + h - 2, w - 2, C_PS)
    c.vline(x + w - 2, y + 2, h - 3, C_PS)


def niche(c, x, y, w, h):
    """A recessed panel in a leaf: shaded top and left, lit bottom and right."""
    c.frame(x, y, w, h, C_PD)
    c.rect(x + 1, y + 1, w - 2, h - 2, C_PS)
    c.hline(x + 1, y + h - 1, w - 1, C_PL)
    c.vline(x + w - 1, y + 1, h - 1, C_PL)


def tooled_band(c, x, y, w):
    """The board's tooled edge: an ink meander between rules, 7 px."""
    meander_band(c, x, y, w, C_IK, C_FZ)


def owned_band(c, y):
    """The band between entry and description, a strap across the whole
    codex, in palette 3: a terracotta meander on sand that the code gilds
    once the Pokemon is caught. It fills tile row y // 8 alone, so no other
    palette shares those tiles."""
    c.hline(0, y, W, v(3, IK))
    c.rect(0, y + 1, W, 5, v(3, PD))
    c.meander(0, y + 1, W, v(3, CD))
    c.hline(0, y + 6, W, v(3, IK))
    c.hline(0, y + 7, W, v(3, IK))
    c.rect(5, y + 7, 230, 1, v(3, PA))
    c.px(5, y + 7, v(3, PL))
    c.px(234, y + 7, v(3, PS))


# --- The list screen ------------------------------------------------------------
LIST_X, LIST_W = 132, 106      # the list leaf (names print from x 136)
SEL_Y = 72                     # the code keeps the selected row at y 72-87


def title(c):
    """The header: tooled board and an ink cartouche lettered POKeDEX."""
    tooled_band(c, 0, 4, W)
    cartouche(c, 6, 1, 76, 14, C_IK)
    c.hline(8, 2, 72, C_BD)
    w = text_width("POKéDEX")
    draw_text(c, 6 + (76 - w) // 2, 0, "POKéDEX", C_GP, C_BD)


def paint_list():
    c = Canvas(W, H)
    board(c)
    title(c)
    # The foot of the board.
    rays_band(c, 0, 152, W, C_IK, C_FZ)

    # Tally leaf for the SEEN / OWN sprites (x 0-63, y 24-99).
    leaf(c, 2, 20, 58, 84)
    # Portrait leaf: the selected Pokemon stands at (96, 80).
    leaf(c, 62, 17, 68, 127)
    niche(c, 64, 20, 64, 120)
    # A pedestal line under the portrait.
    c.hline(70, 118, 52, C_PD)
    c.hline(72, 119, 48, C_PL)

    # The list leaf: visible rows 2-17 (y 16-143); BG1 masks the rest.
    leaf(c, LIST_X, 13, LIST_W, 133)
    # Scroll track on the leaf's right margin (the thumb sprite is at x 226-233).
    c.rect(LIST_X + LIST_W - 10, 16, 4, 128, C_PS)
    c.vline(LIST_X + LIST_W - 10, 16, 128, C_PD)
    c.vline(LIST_X + LIST_W - 7, 16, 128, C_PL)
    # The selected row: a gold-pale bar ruled in gold.
    sx, sw = LIST_X + 2, LIST_W - 13
    c.rect(sx, SEL_Y, sw, 16, C_GP)
    c.hline(sx, SEL_Y, sw, C_GO)
    c.hline(sx, SEL_Y + 15, sw, C_GO)
    # A bronze pointer from the portrait to the selected row.
    for j in range(7):
        half = 3 - abs(3 - j)
        c.hline(129, SEL_Y + 4 + j, half + 1, C_BR)
        c.px(129 + half + 1, SEL_Y + 4 + j, C_IK)
    c.vline(128, SEL_Y + 3, 9, C_IK)
    c.px(129, SEL_Y + 4, C_BL)
    c.px(129, SEL_Y + 5, C_BL)

    # Bronze caps on the board's corners.
    caps(c, 0, 0, 240, 160)
    return c


def paint_start_menu(entries):
    """The list's slide-up menu (BG0, map rows 20-31, columns 16-29). The
    cursor sprite sits at x 136; entries are 16 px apart from row 1."""
    rows = 2 * len(entries) + 2
    c = Canvas(W, 12 * 8)
    P = 2
    x0, w = 128, 112
    h = rows * 8
    # In palette 2 the bronze slots are gold, so the frame reads gilded.
    c.frame(x0, 0, w, h, v(P, IK))
    c.rect(x0 + 1, 1, w - 2, h - 2, v(P, PA))
    meander_band(c, x0 + 1, 1, w - 2, v(P, IK), v(P, BR))
    meander_band(c, x0 + 1, h - 8, w - 2, v(P, IK), v(P, BR))
    c.vline(x0 + 1, 8, h - 16, v(P, PL))
    c.vline(x0 + w - 2, 8, h - 16, v(P, PS))
    for i, s in enumerate(entries):
        draw_text(c, 144, 8 + 16 * i, s, v(P, TX), v(P, PS))
    return c


# --- Entry pages -----------------------------------------------------------------
def page_board():
    c = Canvas(W, H)
    board(c)
    return c


def paint_info():
    c = page_board()
    leaf(c, 4, 18, 232, 142)
    caps(c, 4, 18, 232, 142)
    # Portrait niche: the Pokemon stands at (48, 56).
    niche(c, 12, 22, 72, 64)
    # Rules: under the category, and under HT.
    for x in range(94, 190, 2):
        c.px(x, 55, C_PD)
        c.px(x, 71, C_PD)
    # Footprint medallion (window at tiles 25-26, 8-9).
    medallion(c, 207, 71)
    # The band that gilds when the Pokemon is caught.
    owned_band(c, 88)
    return c


def medallion(c, cx, cy):
    """A bronze-rimmed roundel; the footprint prints in ink on its face."""
    for y in range(cy - 12, cy + 14):
        for x in range(cx - 12, cx + 14):
            d = ((x - cx - 0.5) ** 2 + (y - cy - 0.5) ** 2) ** 0.5
            if d <= 12.6:
                if d > 11.6:
                    c.px(x, y, C_IK)
                elif d > 9.6:
                    lit = (x - cx) + (y - cy) < 0
                    c.px(x, y, C_BL if lit else C_BD)
                elif d > 8.6:
                    c.px(x, y, C_IK)
                else:
                    c.px(x, y, C_PL)


def paint_cry():
    c = page_board()
    leaf(c, 4, 18, 232, 142)
    niche(c, 12, 22, 72, 64)
    # The play button: an A coin and a play arrow (palette 5, color 13).
    coin(c, 89, 73, "A")
    c.rect(106, 73, 26, 14, C_IK)
    c.rect(107, 74, 24, 12, C_BD)
    for j in range(9):
        half = 4 - abs(4 - j)
        c.hline(115, 76 + j, half + 1, C_GO)
    repal(c, 13, 9, 4, 2, 5)  # the arrow's tiles take palette 5
    # The VU meter window (cols 18-27, rows 3-10) is the cry_meter art; seat it.
    c.frame(143, 23, 82, 66, C_IK)
    # Band under the entry.
    meander_band(c, 5, 88, 230, C_IK, C_PD)
    # Rows 12-18, columns 1-28: the waveform window shows through.
    c.rect(8, 96, 224, 56, 0)
    caps(c, 4, 18, 232, 142)
    return c


def coin(c, x, y, letter):
    """A gold coin struck with a button letter, 14x14."""
    rows = [
        "    oooooo    ",
        "  oo555555oo  ",
        " o5577777755o ",
        " o5777777775o ",
        "o577777777773o",
        "o577777777773o",
        "o577777777773o",
        "o577777777773o",
        "o577777777773o",
        "o577777777773o",
        " o5777777773o ",
        " o3377777733o ",
        "  oo333333oo  ",
        "    oooooo    ",
    ]
    c.grid(x, y, rows, {"o": C_IK, "5": C_GP, "7": C_GO, "3": C_BR})
    draw_text(c, x + 4, y - 1, letter, C_IK, None, font="small")


def paint_size():
    c = page_board()
    leaf(c, 4, 18, 232, 142)
    # The measuring wall: a lit stone with a height scale, cols 6-23.
    c.frame(47, 21, 146, 69, C_IK)
    c.rect(48, 22, 144, 67, C_PL)
    for y in range(26, 88, 4):
        c.hline(49, y, 4 if y % 16 == 10 else 2, C_PD)
        c.hline(187 if y % 16 != 10 else 185, y, 4 if y % 16 == 10 else 2, C_PD)
    c.hline(48, 87, 144, C_PD)
    c.hline(48, 88, 144, C_PS)
    meander_band(c, 5, 96, 230, C_IK, C_PD)
    meander_band(c, 5, 145, 230, C_IK, C_PD)
    caps(c, 4, 18, 232, 142)
    return c


# --- The select bar ----------------------------------------------------------------
def tab(c, x, label, pal):
    """A 56x16 tab. Its colors come from the slots palette 2 and 4 swap:
    face 11 lit 10, edge 12, letters 13 shadowed by 14."""
    w = 56
    c.rect(x + 2, 0, w - 4, 1, v(pal, IK))
    c.rect(x + 1, 1, w - 2, 15, v(pal, IK))
    c.rect(x + 2, 1, w - 4, 14, v(pal, BR))
    c.hline(x + 2, 1, w - 4, v(pal, BL))
    c.vline(x + 2, 1, 14, v(pal, BL))
    c.hline(x + 2, 14, w - 4, v(pal, BD))
    c.vline(x + w - 3, 2, 13, v(pal, BD))
    tw = text_width(label)
    draw_text(c, x + (w - tw) // 2, 0, label, v(pal, GO), v(pal, GP))


def paint_select_bar(submenu):
    c = Canvas(W, 24)
    labels = ["AREA", "CRY", "SIZE", "CANCEL"]
    for i, s in enumerate(labels):
        x = 8 + 56 * i
        if submenu and i == 3:
            # Always palette 2 here; drawn as a B coin and a label on the board.
            coin_on_bar(c, x + 2, 1)
            draw_text(c, x + 18, 0, "CANCEL", v(2, PL), v(2, IK))
        else:
            tab(c, x, s, 4)
    return c


def coin_on_bar(c, x, y):
    rows = [
        "    oooooo    ",
        "  oo555555oo  ",
        " o5577777755o ",
        " o5777777775o ",
        "o577777777773o",
        "o577777777773o",
        "o577777777773o",
        "o577777777773o",
        "o577777777773o",
        "o577777777773o",
        " o5777777773o ",
        " o3377777733o ",
        "  oo333333oo  ",
        "    oooooo    ",
    ]
    P = 2
    c.grid(x, y, rows, {"o": v(P, IK), "5": v(P, BL), "7": v(P, BR), "3": v(P, BD)})
    draw_text(c, x + 4, y - 1, "B", v(P, GO), None, font="small")


# --- Sprites -------------------------------------------------------------------------
# interface.png is a 1D sprite sheet (4 tiles a row in the PNG). Each sprite
# takes consecutive tiles from its frame number, row-major inside the sprite.
# Colored with bg_hoenn.pal's palette 0, so the same indices as the BG.
SPRITE_FRAMES = {
    # name: (first tile, w, h)
    "scroll_arrow": (1, 16, 8),
    "scroll_bar": (3, 8, 8),
    "menu_cursor": (4, 8, 16),
    "select_button": (32, 32, 16),
    "search_text": (40, 32, 16),
    "start_button": (48, 32, 16),
    "menu_text": (56, 32, 16),
    "seen_text": (64, 64, 32),
    "own_text": (96, 64, 32),
    "aethos_text": (160, 32, 16),
    "all_text": (168, 32, 16),
}


def spr_arrow():
    c = Canvas(16, 8)
    rows = [
        "       oo       ",
        "      o55o      ",
        "     o5775o     ",
        "    o577775o    ",
        "   o57777773o   ",
        "  o5777777773o  ",
        "  oooooooooooo  ",
    ]
    c.grid(0, 0, rows, {"o": IK, "5": GP, "7": GO, "3": BR})
    return c


def spr_thumb():
    c = Canvas(8, 8)
    rows = [
        " oooooo ",
        "oglllldo",
        "olbbbbdo",
        "olbbbbdo",
        "olbbbbdo",
        "olbbbbdo",
        "oddddddo",
        " oooooo ",
    ]
    c.grid(0, 0, rows, {"o": IK, "g": GP, "l": BL, "b": BR, "d": BD})
    return c


def spr_cursor():
    c = Canvas(8, 16)
    rows = [
        "o      ",
        "o5o    ",
        "o775o  ",
        "o77775o",
        "o7773o ",
        "o73o   ",
        "oo     ",
    ]
    c.grid(1, 4, rows, {"o": IK, "5": GP, "7": GO, "3": BR})
    return c


def spr_key(label):
    """A button cap: an ink capsule lettered in gold."""
    c = Canvas(32, 16)
    c.rect(1, 2, 30, 12, IK)
    c.rect(0, 3, 32, 10, IK)
    c.hline(2, 3, 28, BD)
    tw = text_width(label, "small")
    draw_text(c, (32 - tw) // 2 + 1, 0, label, GO, BD, font="small")
    return c


def spr_label(label, font="narrow"):
    """Light lettering on the board: parchment with an ink shadow."""
    c = Canvas(32, 16)
    draw_text(c, 1, 0, label, PL, IK, font=font)
    return c


def spr_heading(label):
    """SEEN / OWN: ink lettering and a rule, on the tally leaf."""
    c = Canvas(64, 32)
    tw = text_width(label)
    draw_text(c, (64 - tw) // 2, 0, label, TX, PS)
    c.hline(8, 14, 48, PD)
    c.hline(8, 15, 48, PL)
    return c


def spr_dexname(label):
    c = Canvas(32, 16)
    draw_text(c, 3, 1, label, TX, PS, font="small")
    return c


def spr_digit(d):
    c = Canvas(8, 16)
    draw_text(c, 1, 0, str(d), TX, PS)
    return c


def write_interface():
    old = np.array(Image.open(OUT / "interface.png"))
    sheet = [t & 15 for t in tiles_of(old)]       # 256 tiles, 4 a row
    for i in range(len(sheet)):
        if not 16 <= i < 32:                      # keep the rotating ball's OBJ window mask
            sheet[i] = np.zeros((8, 8), np.uint8)
    parts = {
        "scroll_arrow": spr_arrow(), "scroll_bar": spr_thumb(), "menu_cursor": spr_cursor(),
        "select_button": spr_key("SELECT"), "start_button": spr_key("START"),
        "search_text": spr_label("SEARCH"), "menu_text": spr_label("MENU"),
        "seen_text": spr_heading("SEEN"), "own_text": spr_heading("OWN"),
        "aethos_text": spr_dexname("AETHOS"), "all_text": spr_dexname("ALL"),
    }
    for name, c in parts.items():
        first, w, h = SPRITE_FRAMES[name]
        assert (c.w, c.h) == (w, h), name
        for k, t in enumerate(tiles_of(c.a)):
            sheet[first + k] = t
    for d in range(10):
        for base in (128, 176):
            for k, t in enumerate(tiles_of(spr_digit(d).a)):
                sheet[base + 2 * d + k] = t
    a = np.zeros((512, 32), np.uint8)
    for i, t in enumerate(sheet):
        a[(i // 4) * 8:(i // 4) * 8 + 8, (i % 4) * 8:(i % 4) * 8 + 8] = t
    write_indexed_png(OUT / "interface.png", a, [palettes("aethos")[0]])


def write_caught_ball():
    """The owned mark beside a list entry (8x16, printed in palette 0): the
    black-glazed ball of the party menu."""
    c = Canvas(8, 16)
    rows = [
        " oooo  ",
        "o7777o ",
        "o7oo7o ",
        "oo55oo ",
        "o5225o ",
        "o2222o ",
        " oooo  ",
    ]
    c.grid(0, 5, rows, {"o": IK, "7": BD, "5": GO, "2": PD})
    write_indexed_png(OUT / "caught_ball.png", c.a, [palettes("aethos")[0]])


def recolor_png(name, colors):
    """Keep a PNG's pixels and give it new colors (index -> RGB)."""
    path = OUT / name
    a = np.array(Image.open(path))
    pal = [TRANSPARENT] + [(0, 0, 0)] * 15
    for i, c in colors.items():
        pal[i] = c
    write_indexed_png(path, a, [pal])


def write_cry_assets():
    """The cry page: the waveform's papyrus, the dial, the needle."""
    # Waveform window (palette 8): a ruled papyrus tile; the wave grades from
    # ink at its spine (8) to light clay at its peaks (15).
    t = np.full((8, 8), 1, np.uint8)
    t[7, :] = 2
    wave = [INK, INK_TEXT, (88, 48, 32), CLAY_DARK, (152, 64, 32), CLAY, (208, 112, 64), CLAY_LIGHT]
    write_indexed_png(OUT / "cry_screen_bg.png", t, [[TRANSPARENT, PARCHMENT, PARCH_SHADE] + [(0, 0, 0)] * 5 + wave])

    # The dial: 80x64, the whole VU window (palette 9). The needle pivots at
    # its center (40, 32).
    pal = pal16([TRANSPARENT, INK, PARCH_LIGHT, PARCHMENT, PARCH_SHADE, PARCH_DARK,
                 BRONZE_DARK, BRONZE, BRONZE_LIGHT, BRONZE_GLINT, CLAY_DARK, CLAY, INK_TEXT])
    c = Canvas(80, 64, 3)
    cx, cy = 39.5, 31.5
    import math
    for y in range(64):
        for x in range(80):
            d = math.hypot(x - cx, y - cy)
            if d <= 31:
                lit = (x - cx) + (y - cy) < 0
                if d > 30:
                    c.px(x, y, 1)
                elif d > 27:
                    c.px(x, y, 8 if lit else 6)
                elif d > 26:
                    c.px(x, y, 1)
                else:
                    c.px(x, y, 2)
            elif d <= 32:
                c.px(x, y, 4)
    # Ticks on the upper arc, the loud end in red clay.
    for k in range(11):
        ang = math.radians(150 - 12 * k)
        r0, r1 = (18, 25) if k % 5 == 0 else (21, 25)
        col = 10 if k >= 8 else 1
        for r in range(r0, r1 + 1):
            c.px(int(round(cx + r * math.cos(ang))), int(round(cy - r * math.sin(ang))), col)
    for r in range(22, 26):
        for k in range(30):
            ang = math.radians(54 - k)
            c.px(int(round(cx + r * math.cos(ang))), int(round(cy - r * math.sin(ang))), 11 if r > 23 else 10)
    # A lyre mark on the lower face, the sign of a voice.
    lyre = [
        "1.....1",
        "1.....1",
        ".1...1.",
        ".11111.",
        ".1.1.1.",
        ".1.1.1.",
        ".11111.",
        "..111..",
    ]
    c.grid(36, 41, lyre, {"1": 12, ".": 2}, transparent=" ")
    write_indexed_png(OUT / "cry_meter.png", c.a, [pal])

    # The needle keeps its shape; ink with a clay tip.
    recolor_png("cry_meter_needle.png", {1: INK, 2: CLAY, 3: CLAY_DARK, 4: PARCH_LIGHT})


def write_search():
    """The search page keeps Emerald's tiles and the code's palette swaps
    (pokedex.c SetSearchRectHighlight: palette 0 selected, 1 idle, 2 and 3
    disabled) but wears the codex colors: idle labels are dark clay lettered
    in parchment, the selected one gold lettered in ink, disabled ones black
    glaze; the boxes are parchment and the field is ringed clay.
    Pixel roles in search_menu.png: 3 box fill, 4 label letters, 5 and 7 box
    edges, 6 outlines, 8/9 and 10/11 the two kinds of label (fill, letter
    shadow), 12/13 the field, 14 the selected box's ring. The window prints
    in palette 0 with color 15 and shadow 2."""
    path = OUT / "search_menu.png"
    a = np.array(Image.open(path))
    field = (a == 12) | (a == 13)
    rows = np.indices(a.shape)[0] % 8
    a[field] = np.where(rows[field] == 7, 13, 12)
    sel = [TRANSPARENT, INK, PARCH_SHADE, PARCHMENT, INK, PARCH_DARK, INK, BRONZE,
           GOLD, GOLD_DARK, GOLD, GOLD_DARK, CLAY, RING, GOLD, INK_TEXT]
    idle = [TRANSPARENT, INK, PARCH_SHADE, PARCHMENT, PARCHMENT, PARCH_DARK, INK, BRONZE,
            CLAY_DARK, INK, CLAY_DARK, INK, CLAY, RING, INK, INK_TEXT]
    off_sel = [TRANSPARENT, INK, PARCH_SHADE, PARCH_DARK, PARCH_DARK, BRONZE_DARK, INK, BRONZE,
               GLAZE, INK, GLAZE, INK, CLAY, RING, GOLD_DARK, INK_TEXT]
    off = list(off_sel)
    off[14] = INK
    write_indexed_png(path, a, [idle])
    write_jasc(OUT / "search_menu.pal", sel + idle + off_sel + off)


# The area glow's 48 tiles, in the order of src/data/pokedex_area_glow.h. Each
# names the neighbours that glow: an EDGE_L tile sits left of a glowing cell, so
# its glow is on its right; a CORNER_TL tile sits up-left of one, so its glow is
# in its bottom-right corner.
GLOW_TILES = [
    "", "R", "L", "L R", "B", "B R", "B L", "B L R", "T", "T R", "T L", "T L R",
    "T B", "T B R", "T B L", "T B L R", "FULL",
    "TL", "BL", "BL TL", "TR", "TR TL", "TR BL", "TR BL TL", "BR", "BR TL", "BR BL", "BR BL TL",
    "BR TR", "BR TR TL", "BR TR BL", "BR TR BL TL",
    "R TL", "R BL", "R BL TL", "L TR", "L BR", "L BR TR", "B TR", "B TL", "B TL TR",
    "T BR", "T BL", "T BL BR", "B L TR", "B R TL", "T R BL", "T L BR",
]
# Which neighbour (dx, dy) of the tile glows, for each flag.
GLOW_NEIGHBOUR = {
    "R": (-1, 0), "L": (1, 0), "B": (0, -1), "T": (0, 1),
    "TL": (1, 1), "TR": (-1, 1), "BL": (1, -1), "BR": (-1, -1),
}


def write_area_glow():
    """The glow over the places a Pokemon lives, as black-figure gilding.

    Emerald's glow was a solid wash with a two-pixel rim. Here a glowing cell is
    hatched with gold incisions at 45 degrees, so the map's glyphs read through
    it, inside a pale gold edge; one pixel out runs a gold rule, and beyond it a
    dotted gold line like the map's roads. The engine pulses the layer's alpha.
    The hatching repeats every 4 px, so it joins across tiles. Colors keep the
    indices the old recolor used: 1 gold, 2 deep gold, 3 pale gold, 4 dark gold.
    """
    a = np.zeros((96, 32), np.uint8)
    for i, spec in enumerate(GLOW_TILES):
        # A 3x3 block of cells with this tile in the middle.
        full = np.zeros((24, 24), bool)
        if spec == "FULL":
            full[8:16, 8:16] = True
        else:
            for flag in spec.split():
                dx, dy = GLOW_NEIGHBOUR[flag]
                full[8 + dy * 8:16 + dy * 8, 8 + dx * 8:16 + dx * 8] = True
        ys, xs = np.nonzero(full)
        tile = np.zeros((8, 8), np.uint8)
        for y in range(8):
            for x in range(8):
                px, py = x + 8, y + 8
                if full[py, px]:
                    # Inside: a pale edge, then gold hatching.
                    edge = any(not full[py + oy, px + ox]
                               for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1))
                               if 0 <= px + ox < 24 and 0 <= py + oy < 24)
                    if spec != "FULL" and edge:
                        tile[y, x] = 3
                    elif (x + y) % 4 == 0:
                        tile[y, x] = 1
                    elif (x + y) % 4 == 1:
                        tile[y, x] = 4
                    continue
                if len(xs) == 0:
                    continue
                d = np.sqrt(((xs - px) ** 2 + (ys - py) ** 2).min())
                if d <= 1.0:
                    tile[y, x] = 1          # the gold rule round the region
                elif d <= 2.3 and (px + py) % 2 == 0:
                    tile[y, x] = 2          # the dotted road beyond it
        a[(i // 4) * 8:(i // 4) * 8 + 8, (i % 4) * 8:(i % 4) * 8 + 8] = tile
    pal = [TRANSPARENT, GOLD, (232, 152, 48), GOLD_PALE, GOLD_DARK] + [(0, 0, 0)] * 11
    write_indexed_png(OUT / "area_glow.png", a, [pal])


def write_unknown_mon():
    """The unknown Pokemon: a clay roundel with a black-figure question mark.

    graphics/pokemon/question_mark/circled/ is the front and back pic of
    SPECIES_NONE: the codex list shows it for every unseen neighbour. Emerald's
    was a black-and-white "?" ring. Here it is a terracotta tondo, ringed in
    ink and dotted like the trainer card's cup, with the "?" painted in glaze
    and an incised highlight. The shiny palette gilds it."""
    S = 64
    cx, cy = 31.5, 33.5
    c = np.zeros((S, S), np.uint8)
    yy, xx = np.mgrid[0:S, 0:S]
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    ang = np.arctan2(yy - cy, xx - cx)
    # 1 ink, 2 clay dark, 3 clay, 4 clay light, 5 clay pale, 6 glaze, 7 parchment
    c[r <= 23.5] = 1
    c[r <= 22.5] = 3
    # Light from the top left: a lit crescent and a shaded one, cut by offset discs.
    r_lit = np.sqrt((xx - cx - 4) ** 2 + (yy - cy - 4) ** 2)
    r_shade = np.sqrt((xx - cx + 3) ** 2 + (yy - cy + 3) ** 2)
    c[(r <= 22.5) & (r_lit > 22.5)] = 4
    c[(r <= 22.5) & (r_lit > 24.5) & (r > 20.0)] = 5
    c[(r <= 22.5) & (r_shade > 22.5)] = 2
    # A band of parchment dots inside an ink ring, as on the kylix's tondo.
    c[(r > 17.5) & (r <= 18.5)] = 1
    step = np.round((ang + np.pi) / (2 * np.pi) * 28).astype(int) % 2 == 0
    c[step & (np.abs(r - 20.2) <= 0.75)] = 7
    QM = [
        ".....######.....",
        "...##########...",
        "..####....####..",
        ".####......####.",
        ".####......####.",
        "...........####.",
        "..........#####.",
        ".........#####..",
        "........#####...",
        ".......####.....",
        "......####......",
        "......####......",
        "................",
        "......####......",
        "......####......",
        "......####......",
    ]
    ox, oy = 24, 26
    for j, row in enumerate(QM):
        for i, ch in enumerate(row):
            if ch == "#":
                c[oy + j, ox + i] = 6
    # An incised highlight along the hook and the dot, like a scratch through the glaze.
    for j, i in [(1, 5), (1, 6), (1, 7), (2, 3), (3, 2), (4, 2), (13, 7)]:
        c[oy + j, ox + i] = 4
    pal = [TRANSPARENT, INK, CLAY_DARK, CLAY, CLAY_LIGHT, (240, 176, 128), INK, PARCHMENT] + [(0, 0, 0)] * 8
    pal[6] = (48, 32, 24)  # black glaze, a touch warmer than the ink ring
    shiny = list(pal)
    shiny[2], shiny[3], shiny[4], shiny[5] = GOLD_DARK, GOLD, GOLD_PALE, (248, 240, 200)
    qdir = ROOT / "graphics/pokemon/question_mark/circled"
    write_indexed_png(qdir / "anim_front.png", np.vstack([c, c]), [pal])
    write_indexed_png(qdir / "back.png", c, [pal])
    write_jasc(qdir / "normal.pal", pal)
    write_jasc(qdir / "shiny.pal", shiny)
    write_unknown_icon()


def write_unknown_icon():
    """The unknown Pokemon's icon (graphics/pokemon/question_mark/icon.png): the
    same clay roundel at icon size, which the Augur's Eye shows for a Pokemon
    not yet seen. Icons share six palettes, and this one is icon palette 0, so
    it is drawn in that palette's clay (6), orange (7), pink (11) and greys."""
    QM = [
        ".####.",
        "##..##",
        "....##",
        "...##.",
        "..##..",
        "......",
        "..##..",
    ]
    frames = []
    for lift in (0, 1):
        a = np.zeros((32, 32), np.uint8)
        cx, cy = 15.5, 20.5 - lift
        for y in range(32):
            for x in range(32):
                r = ((x + 0.5 - cx - 0.5) ** 2 + (y + 0.5 - cy - 0.5) ** 2) ** 0.5
                if r <= 10.5:
                    a[y, x] = 15
                if r <= 9.5:
                    a[y, x] = 6
                    if (x - cx) + (y - cy) < -6:
                        a[y, x] = 7
                    if (x - cx) + (y - cy) < -11:
                        a[y, x] = 11
        ox, oy = 13, int(cy) - 3
        for j, row in enumerate(QM):
            for i, ch in enumerate(row):
                if ch == "#":
                    a[oy + j, ox + i] = 15
        frames.append(a)
    icon_pal = [tuple(v) for v in read_jasc(ROOT / "graphics/pokemon/icon_palettes/pal0.pal")]
    write_indexed_png(ROOT / "graphics/pokemon/question_mark/icon.png", np.vstack(frames), [[gba(c) for c in icon_pal]])


def write_area_assets():
    # The glow over the places a Pokemon lives: gold hatching, pulsing over the map.
    write_area_glow()
    # Special-area markers: a gold seal ringed in ink.
    recolor_png("area_marker.png", {2: INK, 3: CLAY_DARK, 4: GOLD, 5: GOLD_PALE, 6: GOLD_PALE, 7: PARCH_LIGHT})
    # Size silhouettes: black-figure ink.
    write_jasc(OUT / "size_silhouette.pal", [TRANSPARENT] + [INK] * 15)


# --- Compile -------------------------------------------------------------------------
def compile_all():
    ts = TileSet(reserved=1)
    maps = {}

    lst = paint_list()
    full = compile_map(lst, ts, 32, 20)
    under = full.copy()
    over = np.zeros_like(full)
    over[0:2, :] = full[0:2, :]
    over[18:20, :] = full[18:20, :]
    maps["list"] = over
    maps["list_underlay"] = under

    for name, painter in [("info_screen", paint_info), ("cry_screen", paint_cry), ("size_screen", paint_size)]:
        maps[name] = compile_map(painter(), ts, 32, 20)
    # The waveform shows through rows 12-18 of the cry page.
    maps["cry_screen"][12:19, 1:29] = 0

    for name, sub in [("screen_select_bar_main", False), ("screen_select_bar_submenu", True)]:
        m = compile_map(paint_select_bar(sub), ts, 32, 3)
        m[2, :] = 0
        maps[name] = m

    main_entries = ["BACK TO LIST", "LIST TOP", "LIST BOTTOM", "CLOSE POKéDEX"]
    search_entries = ["BACK TO LIST", "LIST TOP", "LIST BOTTOM", "BACK TO POKéDEX", "CLOSE POKéDEX"]
    for name, entries in [("start_menu_main", main_entries), ("start_menu_search_results", search_entries)]:
        maps[name] = compile_map(paint_start_menu(entries), ts, 32, 12)
    return ts, maps, lst


# pokedex.c loads menu.png whole (an Ichor edit: it used to copy 256 tiles).
# The new-entry page puts it at charbase 1 under map base 14, so 384 is the cap.
MAX_TILES = 384


def write_all():
    ts, maps, lst = compile_all()
    check_tiles(len(ts), MAX_TILES, "graphics/pokedex/menu.png")
    pals = {k: palettes(k) for k in FIELDS}
    write_tiles_png(OUT / "menu.png", ts.tiles, [pals["aethos"][0]], tiles_wide=16)
    for name, m in maps.items():
        write_tilemap(OUT / f"{name}.bin", m)
    for variant, fname in [("aethos", "bg_hoenn.pal"), ("national", "bg_national.pal"),
                           ("search", "search_results_bg.pal")]:
        write_jasc(OUT / fname, [col for p in pals[variant] for col in p])
    write_interface()
    write_caught_ball()
    write_cry_assets()
    write_area_assets()
    write_unknown_mon()
    write_search()
    preview(ts, maps, pals, IMG / "ui_codex_dex_bg.png")
    return ts, maps, pals


def preview(ts, maps, pals, out):
    """A review sheet: every map rendered with its palettes."""
    tiles = ts.tiles
    shots = []
    for name, h, variant in [("list_underlay", 20, "aethos"), ("list", 20, "aethos"),
                             ("info_screen", 20, "aethos"), ("cry_screen", 20, "aethos"),
                             ("size_screen", 20, "aethos"), ("list_underlay", 20, "national"),
                             ("list_underlay", 20, "search")]:
        shots.append(render_map(maps[name], tiles, pals[variant], w=30, h=h, transparent=(0, 96, 96)))
    bar = render_map(maps["screen_select_bar_main"], tiles, pals["aethos"], w=30, h=3, transparent=(0, 96, 96))
    sub = render_map(maps["screen_select_bar_submenu"], tiles, pals["aethos"], w=30, h=3, transparent=(0, 96, 96))
    sm = render_map(maps["start_menu_main"], tiles, pals["aethos"], w=30, h=12, transparent=(0, 96, 96))
    sr = render_map(maps["start_menu_search_results"], tiles, pals["aethos"], w=30, h=12, transparent=(0, 96, 96))
    sheet = np.zeros((160 * 3 + 96 + 24 * 2, 240 * 3, 3), np.uint8)
    for i, s in enumerate(shots):
        sheet[(i // 3) * 160:(i // 3) * 160 + 160, (i % 3) * 240:(i % 3) * 240 + 240] = s
    y = 480
    sheet[y:y + 24, 0:240] = bar
    sheet[y:y + 24, 240:480] = sub
    sheet[y + 24:y + 120, 0:240] = sm
    sheet[y + 24:y + 120, 240:480] = sr
    save_rgb(out, sheet, 2)


if __name__ == "__main__":
    write_all()
