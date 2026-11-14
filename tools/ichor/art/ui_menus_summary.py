#!/usr/bin/env python3
"""Draw Ichor's Pokemon summary screen: papyrus pages unrolled from a scroll
rod, on the terracotta field the other menus share.

The header is the scroll's rod, black with gold knobs, carrying the page
title and the page dots; a papyrus tag at its end holds the button prompt.
Each page's sections open with a meander band and an ink cartouche lettered
in parchment (PROFILE, ABILITY, STATS ...). Labels the code prints in light
text sit on terracotta inlays; values and descriptions sit on papyrus.

The summary code draws many tiles by number, so this script pins them:
  0x00          transparent           0x01  field (the status band's blank)
  0x1A          field, flipped        0x2C  Pokerus-cured mark
  0x39-0x3D     contest ivy leaves    0x40-0x4C, 0x50-0x5C  page dots
  0x62-0x6A     EXP bar fills         0xA9-0xAC  STATS cartouche
  0xD9          band, mirrored        0xDA-0xDF  EVS / IVS (iv_ev_tiles.png)
(see DrawPagination, DrawExperienceProgressBar, DrawContestMoveHearts,
DrawPokerusCuredSymbol and ChangeStatLabel in src/pokemon_summary_screen.c).

Palettes: 0-4 are one art palette (the code addresses the same art through
palettes 1-4 in places), 5 is palette 0 with a gilded portrait backdrop for
shiny Pokemon, 6 and 7 hold the text colors.

Writes, in graphics/summary_screen/:
  tiles.png, iv_ev_tiles.png
  page_info.bin, page_info_egg.bin, page_skills.bin,
  page_battle_moves.bin, page_contest_moves.bin
  status_tilemap.bin, effect_battle.bin, effect_contest.bin, effect_cancel.bin
  move_select.png, markings.pal, a_button.png, b_button.png

Usage: python3 tools/ichor/art/ui_menus_summary.py
"""
import numpy as np

from ui_menus_lib import *

OUT = ROOT / "graphics/summary_screen"
IMG = ROOT / "design/phase1/img"

RING = (160, 72, 40)
ROD = (72, 56, 48)          # the rod's lit edge
FIBER = (224, 200, 152)     # papyrus fibers behind the portrait

ART = pal16([
    TRANSPARENT,   # 0
    INK,           # 1
    CLAY_DARK,     # 2
    CLAY,          # 3
    CLAY_LIGHT,    # 4
    RING,          # 5  throwing rings
    PARCHMENT,     # 6  papyrus
    PARCH_SHADE,   # 7
    PARCH_DARK,    # 8
    GOLD,          # 9
    GOLD_DARK,     # 10
    (240, 232, 208),  # 11 portrait backdrop, light   (shiny: gilded)
    FIBER,         # 12 portrait backdrop, fibers     (shiny: gilded)
    AEGEAN_LIGHT,  # 13 EXP fill
    AEGEAN,        # 14 EXP fill, shade
    ROD,           # 15 rod highlight
])
SHINY = list(ART)
SHINY[11] = (248, 232, 160)
SHINY[12] = (232, 192, 96)
K_INK, K_LINE, K_CLAY, K_HI, K_RING, K_P, K_PS, K_PD, K_G, K_GD, K_BG, K_FIB, K_EXP, K_EXPD, K_ROD = range(1, 16)

LIGHT_TEXT = (248, 240, 216)
LIGHT_SHADOW = (104, 40, 24)
# Text palette 6 (sTextColors): 1/2 dark text on papyrus; 3/4 light text on
# terracotta; 5/6 the memo's highlighted words; 7/8 male and 9/10 female
# symbols (on terracotta); 11/12 and 13/14 a male or female OT's name.
TEXT6 = pal16([
    TRANSPARENT, INK_TEXT, PARCH_SHADE, LIGHT_TEXT, LIGHT_SHADOW,
    (176, 40, 24), (232, 176, 136),
    AEGEAN_PALE, LIGHT_SHADOW, (248, 192, 176), LIGHT_SHADOW,
    AEGEAN_PALE, LIGHT_SHADOW, (248, 192, 176), LIGHT_SHADOW, LIGHT_TEXT,
])
# Text palette 7: the prompt (dark, on the papyrus tag) and the dex number
# (light, or 7/8 gold for colorId 7); 13-15 paint the A and B coins.
TEXT7 = pal16([
    TRANSPARENT, INK_TEXT, PARCH_SHADE, LIGHT_TEXT, LIGHT_SHADOW,
    (176, 40, 24), (232, 176, 136), GOLD, CLAY_DARK, (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
    GOLD, GOLD_DARK, INK,
])
PALETTES = [ART, ART, ART, ART, ART, SHINY, TEXT6, TEXT7]

W, H = 256, 160

# --- Lettering ---------------------------------------------------------------
# Square capitals in the manner of an inscription, 5 px tall.
GLYPHS = {
    "A": [".#.", "#.#", "###", "#.#", "#.#"], "B": ["##.", "#.#", "##.", "#.#", "##."],
    "C": [".##", "#..", "#..", "#..", ".##"], "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"], "F": ["###", "#..", "##.", "#..", "#.."],
    "G": [".##", "#..", "#.#", "#.#", ".##"], "H": ["#.#", "#.#", "###", "#.#", "#.#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"], "J": ["..#", "..#", "..#", "#.#", ".#."],
    "K": ["#.#", "#.#", "##.", "#.#", "#.#"], "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#...#", "##.##", "#.#.#", "#...#", "#...#"], "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "O": [".#.", "#.#", "#.#", "#.#", ".#."], "P": ["##.", "#.#", "##.", "#..", "#.."],
    "R": ["##.", "#.#", "##.", "#.#", "#.#"], "S": [".##", "#..", ".#.", "..#", "##."],
    "T": ["###", ".#.", ".#.", ".#.", ".#."], "U": ["#.#", "#.#", "#.#", "#.#", ".#."],
    "V": ["#.#", "#.#", "#.#", ".#.", ".#."], "W": ["#...#", "#...#", "#.#.#", "##.##", "#...#"],
    "X": ["#.#", "#.#", ".#.", "#.#", "#.#"], "Y": ["#.#", "#.#", ".#.", ".#.", ".#."],
    ".": ["", "", "", "", "#"], " ": ["..", "..", "..", "..", ".."],
}


def text_width(s):
    return sum(len(GLYPHS[ch][0]) if GLYPHS[ch][0] else 1 for ch in s) + len(s) - 1


def letter(c, x, y, s, color):
    for ch in s:
        g = GLYPHS[ch]
        w = len(g[0]) if g[0] else 1
        for j, row in enumerate(g):
            for i, v in enumerate(row):
                if v == "#":
                    c.px(x + i, y + j, color)
        x += w + 1
    return x


# --- Shared pieces --------------------------------------------------------------
def field(c, x, y, w, h):
    c.rect(x, y, w, h, K_CLAY)
    for yy in range(y, y + h):
        if yy % 8 == 7:
            c.hline(x, yy, w, K_RING)


def band(c, x, y, w):
    """A section band, 8 px: ink rules round an ink meander on clay."""
    c.hline(x, y, w, K_INK)
    c.rect(x, y + 1, w, 6, K_CLAY)
    c.meander(x, y + 1, w, K_INK)
    c.hline(x, y + 6, w, K_CLAY)
    c.hline(x, y + 7, w, K_INK)


def cartouche(c, x, y, label):
    """An ink cartouche lettered in parchment, laid over a band at row y."""
    w = text_width(label) + 6
    c.rect(x, y, w, 8, K_INK)
    c.px(x, y, K_CLAY)
    c.px(x + w - 1, y, K_CLAY)
    c.px(x, y + 7, K_CLAY)
    c.px(x + w - 1, y + 7, K_CLAY)
    letter(c, x + 3, y + 2, label, K_P)
    return x + w


def panel(c, x, y, w, h, fill=K_P):
    """A papyrus panel: ink outline, incised clay line, papyrus inside."""
    c.rect(x, y, w, h, fill)
    c.frame(x, y, w, h, K_INK)
    c.frame(x + 1, y + 1, w - 2, h - 2, K_LINE)


def inlay(c, x, y, w, h):
    """A terracotta inlay for light lettering, lit at the top."""
    c.rect(x, y, w, h, K_CLAY)
    c.hline(x, y, w, K_HI)
    c.hline(x, y + h - 1, w, K_LINE)


def section(c, tx0, tx1, ty, label, rows):
    """A framed section: band at tile row ty, then rows of (kind, height in
    tiles) where kind is 'p' papyrus or 'c' terracotta inlay."""
    x0, x1 = tx0 * 8, tx1 * 8 + 8
    band(c, x0, ty * 8, x1 - x0)
    cartouche(c, x0 + 12, ty * 8, label)
    y = ty * 8 + 8
    total = sum(h for _, h in rows) * 8
    panel(c, x0, y - 1, x1 - x0, total + 1)
    for kind, h in rows:
        if kind == "c":
            inlay(c, x0 + 2, y, x1 - x0 - 4, h * 8)
        y += h * 8
    # re-ink the band's foot over the panel's top edge
    c.hline(x0, ty * 8 + 7, x1 - x0, K_INK)
    return y


# --- Header: the scroll rod ------------------------------------------------------
def rod(c, x, w):
    """Rows 0-1: a black rod, lit along its top."""
    c.rect(x, 0, w, 16, K_INK)
    c.hline(x, 1, w, K_ROD)
    c.hline(x, 2, w, K_ROD)
    c.hline(x, 14, w, K_LINE)


def knob(c, x):
    """A gold knob (the scroll's cornu), 6 px wide, at the rod's left end."""
    for j in range(16):
        r = [0, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 0][j]
        for i in range(-r, r + 1):
            c.px(x + 3 + i, j, K_G)
        c.px(x + 3 - r, j, K_GD if j > 8 else K_G)
        c.px(x + 3 + r, j, K_GD)
    c.px(x + 2, 4, K_P)
    c.px(x + 2, 5, K_P)


def tag(c, x0, x1):
    """The papyrus tag at the rod's end, holding the button prompt."""
    c.rect(x0, 0, x1 - x0, 16, K_P)
    c.hline(x0, 0, x1 - x0, K_PS)
    c.hline(x0, 15, x1 - x0, K_PD)
    c.hline(x0, 14, x1 - x0, K_PS)


def dot_tiles():
    """16x16 page dots on the rod, as (top-left, top-right, bottom-left,
    bottom-right) tiles, keyed by DrawPagination's states."""
    def base(end=False):
        c = Canvas(16, 16)
        rod(c, 0, 16)
        if end:
            # the rod ends in a gold knob, then the tag begins
            tag(c, 10, 16)
            knob(c, 9)
        return c

    def disc(c, kind, cx=6):
        cy = 8
        pts = [(x, y) for y in range(16) for x in range(16) if (x - cx + 0.5) ** 2 + (y - cy + 0.5) ** 2 <= 12.5]
        if kind == "now":
            for x, y in pts:
                c.px(x, y, K_G)
            for x, y in pts:
                if (x - cx + 1.5) ** 2 + (y - cy + 1.5) ** 2 > 12.5:
                    c.px(x, y, K_GD)
            c.px(cx - 2, cy - 2, K_P)
        elif kind == "seen":
            for x, y in pts:
                c.px(x, y, K_CLAY)
            for x, y in pts:
                if (x - cx + 1.5) ** 2 + (y - cy + 1.5) ** 2 > 12.5:
                    c.px(x, y, K_LINE)
        else:  # ahead: a clay ring
            for x, y in pts:
                if (x - cx + 0.5) ** 2 + (y - cy + 0.5) ** 2 > 5:
                    c.px(x, y, K_CLAY)

    out = {}
    for name, kind, end in [("now", "now", False), ("now_last", "now", True), ("seen", "seen", False),
                            ("ahead", "ahead", False), ("ahead_last", "ahead", True)]:
        c = base(end)
        disc(c, kind, 5 if end else 8)
        out[name] = c.a
    out["before"] = base().a
    t = Canvas(16, 16)
    tag(t, 0, 16)
    out["after"] = t.a
    return out


# DrawPagination's tile numbers: (top-left, top-right), bottom row is +0x10.
DOT_SLOTS = {
    "before": (0x40, 0x40), "now": (0x41, 0x42), "ahead": (0x43, 0x44), "seen": (0x46, 0x47),
    "ahead_last": (0x48, 0x49), "after": (0x4A, 0x4A), "now_last": (0x4B, 0x4C),
}


# --- The portrait column ---------------------------------------------------------
def portrait_column(c):
    field(c, 0, 16, 80, 144)
    # a vertical divider between the column and the pages
    c.vline(78, 16, 144, K_LINE)
    c.vline(79, 16, 144, K_INK)
    # The portrait: cols 1-8 rows 4-11. Only colors 11 and 12 differ in the
    # shiny palette, so the frame stays put while the backdrop gilds.
    x, y, w, h = 8, 32, 64, 64
    c.rect(x, y, w, h, K_BG)
    for yy in range(y + 3, y + h - 3, 4):
        c.hline(x + 3, yy, w - 6, K_FIB)          # papyrus fibers
    for xx in ():  # fibers run one way only, so the backdrop never reads as bars
        c.vline(xx, y + 3, h - 6, K_FIB)
    c.frame(x, y, w, h, K_INK)
    c.frame(x + 1, y + 1, w - 2, h - 2, K_GD)
    c.frame(x + 2, y + 2, w - 4, h - 4, K_LINE)
    # an ink ground line for the Pokemon, as on a vase
    c.hline(x + 3, y + h - 6, w - 6, K_LINE)
    # a meander under the portrait, above the name
    c.rect(x, y + h + 1, w, 5, K_CLAY)
    c.meander(x, y + h + 1, w, K_INK)
    c.hline(x, y + h + 6, w, K_INK)


def status_band():
    """The STATUS band that slides in at rows 18-19, cols 0-9 (10x2 tiles):
    an ink band for the light label, and a papyrus seat for the status icon."""
    c = Canvas(80, 16)
    c.rect(0, 0, 80, 16, K_INK)
    c.hline(0, 0, 80, K_LINE)
    c.hline(0, 1, 80, K_ROD)
    c.rect(49, 3, 26, 11, K_P)
    c.frame(48, 2, 28, 13, K_GD)
    c.px(48, 2, K_INK)
    c.px(75, 2, K_INK)
    c.px(48, 14, K_INK)
    c.px(75, 14, K_INK)
    c.hline(0, 15, 80, K_LINE)
    return c


# --- Pages -------------------------------------------------------------------------
def page_info(egg=False):
    c = Canvas(W, H)
    field(c, 0, 0, W, H)
    rod(c, 0, 240)
    tag(c, 104 if egg else 152, 240)
    portrait_column(c)
    field(c, 80, 16, 160, 144)
    section(c, 10, 29, 3, "PROFILE", [("c", 2), ("p", 2)])
    if egg:
        section(c, 10, 29, 8, "STATE", [("p", 4)])
    else:
        section(c, 10, 29, 8, "ABILITY", [("c", 2), ("p", 2)])
    section(c, 10, 29, 13, "TRAINER MEMO", [("p", 6)])
    return c


def page_skills():
    c = Canvas(W, H)
    field(c, 80, 16, 160, 144)
    # ITEM and RIBBON side by side
    band(c, 80, 24, 160)
    cartouche(c, 92, 24, "ITEM")
    cartouche(c, 172, 24, "RIBBON")
    panel(c, 80, 31, 79, 17)
    panel(c, 161, 31, 79, 17)
    c.hline(80, 31, 160, K_INK)
    # STATS: labels on terracotta, values on papyrus
    band(c, 80, 48, 160)
    stats_cart = (96, 48)            # cols 12-15: STATS cartouche, tiles 0xA9-0xAC
    cartouche(c, stats_cart[0], stats_cart[1], "STATS")
    panel(c, 80, 55, 160, 49)
    inlay(c, 82, 56, 46, 47)         # HP / ATTACK / DEFENSE labels, cols 10-15
    inlay(c, 174, 56, 42, 47)        # SP.ATK / SP.DEF / SPEED labels, cols 22-26
    c.vline(128, 56, 47, K_LINE)
    c.vline(173, 56, 47, K_LINE)
    c.vline(216, 56, 47, K_LINE)
    c.hline(80, 55, 160, K_INK)
    # EXP.
    band(c, 80, 104, 160)
    cartouche(c, 92, 104, "EXP.")
    panel(c, 80, 111, 160, 49)
    inlay(c, 82, 112, 88, 32)        # EXP. POINTS / NEXT LV. labels
    c.vline(170, 112, 32, K_LINE)
    c.hline(80, 111, 160, K_INK)
    # the EXP bar row (row 18): label tile at col 20, bar at cols 21-28
    letter(c, 154, 147, "EXP", K_INK)
    exp_frame(c, 167, 144, 64)
    return c


def exp_frame(c, x, y, w):
    c.hline(x, y + 2, w + 2, K_INK)
    c.hline(x, y + 6, w + 2, K_INK)
    c.vline(x, y + 2, 5, K_INK)
    c.vline(x + w + 1, y + 2, 5, K_INK)
    c.rect(x + 1, y + 3, w, 3, K_PD)


def exp_tiles():
    """Tiles 0x62-0x69 (0-7 px filled) and 0x6A (full), for the 8 cells at
    row 18, cols 21-28: the bar's ink rails with an Aegean fill."""
    out = []
    for n in range(9):
        t = Canvas(8, 8, K_P)
        t.hline(0, 2, 8, K_INK)
        t.hline(0, 6, 8, K_INK)
        t.rect(0, 3, 8, 3, K_PD)
        t.rect(0, 3, n, 1, K_EXP)
        t.rect(0, 4, n, 2, K_EXPD)
        out.append(t.a)
    return out


def moves_panel(c, contest=False):
    """Rows as the code expects them: MOVES band at row 3, four moves in rows
    4-11 (a fifth, in the forget-a-move flow, extends the panel through row
    13), DESCRIPTION band at row 14 over rows 15-19."""
    field(c, 80, 16, 160, 144)
    band(c, 80, 24, 160)
    cartouche(c, 92, 24, "MOVES")
    panel(c, 80, 31, 160, 65)
    # type icon seats (papyrus), names on terracotta (cols 15-23), PP papyrus
    inlay(c, 120, 32, 72, 63)
    c.vline(119, 32, 63, K_LINE)
    c.vline(192, 32, 63, K_LINE)
    c.hline(80, 31, 160, K_INK)
    # DESCRIPTION
    band(c, 80, 112, 160)
    cartouche(c, 92, 112, "DESCRIPTION")
    panel(c, 80, 119, 160, 41)
    c.hline(80, 119, 160, K_INK)
    return c


def page_moves(contest=False):
    c = Canvas(W, H)
    moves_panel(c, contest)
    return c


def effect_box(contest=False):
    """The EFFECT box that slides in at cols 0-9, rows 13-19 (10x7 tiles):
    a field row, the band at row 14 (level with DESCRIPTION, clear of the
    nickname above), labels and values in rows 15-18, the panel's foot."""
    c = Canvas(80, 56)
    field(c, 0, 0, 80, 56)
    band(c, 0, 8, 80)
    cartouche(c, 8, 8, "EFFECT")
    panel(c, 0, 15, 80, 41)
    c.hline(0, 15, 80, K_INK)
    if contest:
        inlay(c, 2, 16, 44, 39)      # APPEAL / JAM labels
    else:
        inlay(c, 2, 16, 52, 39)      # POWER / ACCURACY labels
    return c


# --- Fixed small tiles --------------------------------------------------------------
def ivy(kind):
    """Contest ivy leaves (Greek art's heart): filled ink or an empty outline."""
    t = Canvas(8, 8, K_P)
    leaf = [
        ".##.##.",
        "#######",
        "#######",
        ".#####.",
        "..###..",
        "...#...",
    ]
    for j, row in enumerate(leaf):
        for i, ch in enumerate(row):
            if ch == "#":
                edge = (j == 0 or i in (0, 6) or j == 5 or row[max(i - 1, 0)] == "." or i + 1 >= len(row) or row[i + 1] == ".")
                if kind == "full":
                    t.px(i, j + 1, K_INK)
                elif edge or j >= 4:
                    t.px(i, j + 1, K_PD)
    if kind == "full":
        t.px(2, 2, K_CLAY)
    return t.a


def pokerus_mark():
    t = Canvas(8, 8)
    field(t, 0, 0, 8, 8)
    # a small gold star of healing on the field
    for (x, y) in [(3, 1), (3, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (3, 4), (2, 5), (4, 5)]:
        t.px(x, y, K_G)
    return t.a


# --- Compile ---------------------------------------------------------------------------
class Compiler:
    def __init__(self):
        self.ts = TileSet()
        self.ts.tiles = []
        self.reserved = set()
        self.next_free = 1

    def fix(self, idx, tile):
        self.ts.place(idx, tile)
        self.reserved.add(idx)

    def alloc(self, tile):
        hit = self.ts.lookup.get(np.asarray(tile, np.uint8).tobytes())
        if hit is not None:
            return hit
        while self.next_free in self.reserved or self.next_free < len(self.ts.tiles) and self.ts.tiles[self.next_free].any():
            self.next_free += 1
        i = self.next_free
        self.ts.place(i, tile)
        self.reserved.add(i)
        return i, 0

    def cut(self, c, region, pal_of=lambda tx, ty: 0, map_w=32):
        """Tilemap entries for region (tx, ty, w, h) of canvas c."""
        x0, y0, w, h = region
        out = np.zeros((h, w), np.uint16)
        for j in range(h):
            for i in range(w):
                tx, ty = x0 + i, y0 + j
                cell = c.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                if not cell.any():
                    out[j, i] = 0
                    continue
                idx, f = self.alloc(cell)
                out[j, i] = idx | f | (pal_of(tx, ty) << 12)
        return out


def build():
    comp = Compiler()
    zero = np.zeros((8, 8), np.uint8)
    comp.fix(0, zero)
    fieldt = Canvas(8, 8)
    field(fieldt, 0, 0, 8, 8)
    comp.fix(0x01, fieldt.a)
    comp.fix(0x1A, fieldt.a[::-1])            # drawn flipped at (3,17)
    comp.fix(0x2C, pokerus_mark())
    comp.fix(0x39, ivy("empty"))
    comp.fix(0x3A, ivy("full"))
    comp.fix(0x3C, ivy("full"))
    comp.fix(0x3D, ivy("empty"))
    dots = dot_tiles()
    for name, (a, b) in DOT_SLOTS.items():
        t = dots[name]
        comp.fix(a, t[0:8, 0:8])
        comp.fix(b, t[0:8, 8:16])
        comp.fix(a + 0x10, t[8:16, 0:8])
        comp.fix(b + 0x10, t[8:16, 8:16])
    for n, t in enumerate(exp_tiles()):
        comp.fix(0x62 + n, t)
    # skills page STATS cartouche: cols 12-15 of row 6 -> tiles 0xA9-0xAC
    skills = page_skills()
    for i in range(4):
        comp.fix(0xA9 + i, skills.a[48:56, 96 + i * 8:104 + i * 8])
    band_t = skills.a[48:56, 136:144]
    comp.fix(0xD9, band_t[:, ::-1])           # drawn h-flipped by ClearStatLabel
    for i in range(0xDA, 0xE0):
        comp.reserved.add(i)

    maps = {}
    info = page_info()
    egg = page_info(egg=True)

    def info_pal(tx, ty):
        return 4 if ty < 2 else 0

    def page_map(c, full):
        m = np.zeros((32, 32), np.uint16)
        if full:
            m[0:20, 0:30] = comp.cut(c, (0, 0, 30, 20), info_pal)
        else:
            m[2:20, 10:30] = comp.cut(c, (10, 2, 20, 18))
        return m

    maps["page_info"] = page_map(info, True)
    maps["page_info_egg"] = page_map(egg, True)
    # the header dots: the code rewrites cols 11-18 with fixed tiles, keeping
    # the palette, so plant the start state there without flips.
    for m, pages in ((maps["page_info"], ["now", "ahead", "ahead", "ahead_last"]),
                     (maps["page_info_egg"], ["now_last", "after", "after", "after"])):
        for k, name in enumerate(pages):
            a, b = DOT_SLOTS[name]
            m[0, 11 + 2 * k] = a | 0x4000
            m[0, 12 + 2 * k] = b | 0x4000
            m[1, 11 + 2 * k] = (a + 0x10) | 0x4000
            m[1, 12 + 2 * k] = (b + 0x10) | 0x4000
        m[17, 3] = 0x81A                     # Pokerus: no mark
    maps["page_skills"] = page_map(skills, False)
    # EXP bar starts empty
    for i in range(8):
        maps["page_skills"][18, 21 + i] = 0x2062
    # STATS cartouche pinned to its tiles
    for i in range(4):
        maps["page_skills"][6, 12 + i] = 0xA9 + i
    moves = page_moves()
    contest = page_moves(contest=True)
    maps["page_battle_moves"] = page_map(moves, False)
    maps["page_contest_moves"] = page_map(contest, False)

    # Status band (10x2), EFFECT boxes (10x8; row 7 is the blank row under them).
    sb = status_band()
    status = comp.cut(sb, (0, 0, 10, 2))
    eb = effect_box(False)
    ec = effect_box(True)
    eff_b = np.zeros((8, 10), np.uint16)
    eff_b[:7] = comp.cut(eb, (0, 0, 10, 7))
    eff_c = np.zeros((8, 10), np.uint16)
    eff_c[:7] = comp.cut(ec, (0, 0, 10, 7), pal_of=lambda tx, ty: 1)
    for j in range(2):
        for i in range(4):
            eff_c[2 + j, 6 + i] = 0x1039
            eff_c[4 + j, 6 + i] = 0x103D

    # The fifth-move rows (effect_cancel.bin): A = a moves-panel row, B = the
    # panel's foot, C = the field beneath, each 20 tiles (cols 10-29), cut
    # from the moves page's rows 10, 11 and 12.
    rowA = comp.cut(moves, (10, 10, 20, 1))[0]
    rowB = comp.cut(moves, (10, 11, 20, 1))[0]
    rowC = comp.cut(moves, (10, 12, 20, 1))[0]
    cancel = np.concatenate([rowA, rowB, rowC, np.zeros(4, np.uint16)])
    # (the code adds the palette to these entries, so they carry none)
    cancel &= 0x0FFF

    n = len(comp.ts.tiles)
    assert n <= 240, f"summary tiles: {n} > 240"
    return comp, maps, status, eff_b, eff_c, cancel, n


def write():
    comp, maps, status, eff_b, eff_c, cancel, n = build()
    tiles = comp.ts.tiles
    pal_of = lambda i: 0
    write_tiles_png(OUT / "tiles.png", tiles, PALETTES, tiles_wide=16, min_tiles=240, pal_of_tile=pal_of)
    # The IV/EV variant: the same tiles, with EVS at 0xDA-0xDC and IVS at
    # 0xDD-0xDF lettered like the STATS cartouche.
    alt = list(tiles) + [np.zeros((8, 8), np.uint8)] * max(0, 0xE0 - len(tiles))
    for base, label in ((0xDA, "EVS"), (0xDD, "IVS")):
        c = Canvas(24, 8)
        band(c, 0, 0, 24)
        cartouche(c, 0, 0, label)
        for i in range(3):
            alt[base + i] = c.a[:, i * 8:i * 8 + 8] & 15
    write_tiles_png(OUT / "iv_ev_tiles.png", alt, PALETTES, tiles_wide=16, min_tiles=240, pal_of_tile=pal_of)
    for name, m in maps.items():
        write_tilemap(OUT / f"{name}.bin", m)
    (OUT / "status_tilemap.bin").write_bytes(status.astype("<u2").tobytes())
    (OUT / "effect_battle.bin").write_bytes(eff_b.astype("<u2").tobytes())
    (OUT / "effect_contest.bin").write_bytes(eff_c.astype("<u2").tobytes())
    (OUT / "effect_cancel.bin").write_bytes(cancel.astype("<u2").tobytes())
    print(f"summary: {n} tiles")
    write_sprites()
    preview(comp, maps, status, eff_b)


def write_sprites():
    # The move selector: same shape, gold for the cursor, Aegean for the
    # second selector used when swapping moves.
    from PIL import Image
    im = Image.open(OUT / "move_select.png")
    a = np.array(im)
    pal = pal16([TRANSPARENT, GOLD, GOLD_DARK, AEGEAN_LIGHT, AEGEAN_DARK, (0, 0, 0), (0, 0, 0), (0, 0, 0),
                 (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), GOLD])  # 12: the cursor box
    write_indexed_png(OUT / "move_select.png", a, [pal])
    # A and B: gold coins struck with an ink letter, in text palette 7
    # (13 gold, 14 its shaded rim, 15 ink). They are blitted into the prompt
    # window, so they sit on the papyrus tag.
    coins = {
        "a_button.png": [
            "                ",
            "                ",
            "     dddddd     ",
            "    dddddddd    ",
            "   dddd**dddd   ",
            "   ddd*dd*ddd   ",
            "  dddd*dd*dddd  ",
            "  dddd****dddd  ",
            "  dddd*dd*dddd  ",
            "  dddd*dd*dddd  ",
            "   ddddddddde   ",
            "   dddddddde    ",
            "    eddddeee    ",
            "     eeeeee     ",
            "                ",
            "                ",
        ],
        "b_button.png": [
            "                ",
            "                ",
            "     dddddd     ",
            "    dddddddd    ",
            "   ddd***dddd   ",
            "   ddd*dd*ddd   ",
            "  dddd***ddddd  ",
            "  dddd*dd*dddd  ",
            "  dddd*dd*dddd  ",
            "  dddd***ddddd  ",
            "   ddddddddde   ",
            "   dddddddde    ",
            "    eddddeee    ",
            "     eeeeee     ",
            "                ",
            "                ",
        ],
    }
    key = {" ": 0, "d": 13, "e": 14, "*": 15}
    gray = [(i * 16, i * 16, i * 16) for i in range(16)]
    for name, rows in coins.items():
        g = np.array([[key[ch] for ch in row] for row in rows], np.uint8)
        write_indexed_png(OUT / name, g, [gray])
    # Markings (circle, square, triangle, heart; graphics/interface/
    # mon_markings.png): 1-2 an unset mark, faint on the clay; 3-4 a set one,
    # in gold.
    write_jasc(OUT / "markings.pal", pal16([TRANSPARENT, CLAY_LIGHT, (208, 112, 64), GOLD, GOLD_DARK]))


def preview(comp, maps, status, eff_b):
    imgs = []
    for name in ("page_info", "page_skills", "page_battle_moves", "page_info_egg"):
        base = render_map(maps["page_info"], comp.ts.tiles, PALETTES, 30, 20)
        top = render_map(maps[name], comp.ts.tiles, PALETTES, 30, 20)
        m = (maps[name][:20, :30] != 0).repeat(8, 0).repeat(8, 1)
        base[m] = top[m]
        imgs.append(base)
    sheet = np.vstack([np.hstack(imgs[:2]), np.hstack(imgs[2:])])
    save_rgb(IMG / "ui_summary_bg.png", sheet, 2)


if __name__ == "__main__":
    write()
