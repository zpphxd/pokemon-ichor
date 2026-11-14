#!/usr/bin/env python3
"""Draw Ichor's trainer card: a kylix, the Greek drinking cup, seen from above.

Front: the cup's white-ground bowl, with your portrait in the tondo at its
centre, your name inscribed above it and your money, Pokedex, time and ID
painted either side in red labels over ink figures. Back: the cup turned over.
A victory wreath circles its foot, around your name, and gains one gold leaf
per Laurel, each leaf carrying its god's emblem.

The card gets finer as you earn stars (the engine's count: the Hall of Heroes,
a complete Aethos Dex, and two Hoenn feats that Ichor cuts): its lip and
handles go from black glaze to bronze, coral red, silver and gold. Theo's card
lies on Aegean blue, Ianthe's on violet, her name's flower (ion + anthos).

How the engine draws it (src/trainer_card.c, where the Ichor edits are):
  BG2  the screen behind the cup (bg.bin)
  BG0  the cup, front.bin or back.bin; it is squashed by a scanline effect to flip
  BG3  the portrait window, the stars (tile 143, palette 4) and the laurels
       (badges.png at tile 192, palette 3), drawn by code
  BG1  the text, palette 15 (the dialogue box's ink and red)
All three tilemaps share tiles.png (at most 192 tiles) and palettes 0-2:
  0  the cup: one palette per star count (green, bronze, copper, silver, gold.pal)
  1  the background: Theo's in those files, Ianthe's in female_bg.pal
  2  the wreath's twigs and the back's details
Tiles 140, 141, 156 and 157 are Hoenn's back-of-card stat marks, drawn by
DrawCardBackStats on the Emerald card only for link and contest stats; they
are left blank. Tile 143 is the star.

Writes graphics/trainer_card/: tiles.png, bg.bin, front.bin, front_link.bin,
back.bin, green/bronze/copper/silver/gold.pal, female_bg.pal, star.pal,
badges.png; and previews in design/phase1/img/ui_card_*.png.

Usage: python3 tools/ichor/art/ui_trainer_card.py
"""
import math

import numpy as np

from ui_menus_lib import (ROOT, INK, CLAY_DARK, CLAY, CLAY_LIGHT, CLAY_PALE, PARCHMENT,
                          PARCH_SHADE, PARCH_DARK, GOLD, GOLD_DARK, GOLD_PALE, MARBLE_LIGHT,
                          OLIVE, OLIVE_DARK, SILVER_LEAF, AEGEAN_DARK, AEGEAN, AEGEAN_LIGHT,
                          AEGEAN_PALE, TRANSPARENT, MEANDER, pal16, write_tiles_png,
                          write_indexed_png, write_jasc, render_map, save_rgb)
from ui_menus_summary import GLYPHS, letter

OUT = ROOT / "graphics/trainer_card"
IMG = ROOT / "design/phase1/img"
W, H = 240, 160
CX, CY = 119.5, 79.5          # the cup's centre, between pixels so the quadrants mirror
RX, RY = 100, 72              # the bowl's outer edge
LIP = 5                       # the black-glaze lip's width

GLAZE = (56, 40, 40)

# --- Palettes ---------------------------------------------------------------
# Palette 0, the cup. Slots 3-5 and 11 change with the star count.
P0_BASE = [
    TRANSPARENT,   # 0
    INK,           # 1  outline
    GLAZE,         # 2  black glaze: the lip, the tondo's band
    None,          # 3  lip, lit   (tier)
    None,          # 4  lip, mid   (tier)
    None,          # 5  lip, shade (tier)
    PARCHMENT,     # 6  the white-ground bowl; the same as the text field
    PARCH_SHADE,   # 7  the bowl's wall in shadow
    CLAY_DARK,     # 8  the tondo's ground line; the underside's shade
    CLAY,          # 9  the underside
    CLAY_LIGHT,    # 10 the tondo's ground
    None,          # 11 the tondo band's dots (tier)
    CLAY_PALE,     # 12 the underside, lit
    PARCH_DARK,    # 13 incised lines in the bowl
    GOLD,          # 14 the rosettes on the lip
    MARBLE_LIGHT,  # 15 a glint on the lip
]
TIERS = {   # (lit, mid, shade, band dots)
    "green": [(136, 104, 96), (80, 56, 56), (48, 32, 32), (224, 136, 88)],     # black glaze, plain
    "bronze": [(232, 176, 104), (176, 112, 48), (112, 64, 32), (208, 152, 72)],
    "copper": [(248, 160, 120), (208, 80, 48), (136, 40, 24), (240, 136, 96)],  # Exekias's coral red
    "silver": [(248, 248, 248), (192, 192, 200), (120, 120, 136), (216, 216, 224)],
    "gold": [(248, 232, 152), (240, 192, 64), (176, 120, 32), (248, 224, 136)],
}


def p0(tier):
    pal = list(P0_BASE)
    pal[3], pal[4], pal[5], pal[11] = TIERS[tier]
    return pal16(pal)


def p1(dark, mid, light, pale):
    """Palette 1, the screen behind the cup: a woven cloth with a meander border."""
    return pal16([TRANSPARENT, INK, dark, mid, light, pale, CLAY_DARK, CLAY, CLAY_LIGHT, PARCHMENT])


P1_THEO = p1(AEGEAN_DARK, AEGEAN, AEGEAN_LIGHT, AEGEAN_PALE)
P1_IANTHE = p1((56, 32, 88), (104, 64, 144), (160, 120, 200), (208, 184, 232))

P2 = pal16([TRANSPARENT, INK, OLIVE_DARK, OLIVE, SILVER_LEAF, CLAY_DARK, CLAY, CLAY_LIGHT,
            CLAY_PALE, GOLD_DARK, GOLD, PARCHMENT, GLAZE])
# palette-coded pixel values (palette * 16 + index)
K = dict(ink=1, glaze=2, lit=3, mid=4, shade=5, cream=6, cream_sh=7, clay_dk=8, clay=9,
         clay_lt=10, dots=11, clay_pale=12, incise=13, gold=14, glint=15)
B = dict(ink=16 + 1, dk=16 + 2, mid=16 + 3, lt=16 + 4, pale=16 + 5, clay_dk=16 + 6,
         clay=16 + 7, clay_lt=16 + 8, parch=16 + 9)
T = dict(ink=32 + 1, olive_dk=32 + 2, olive=32 + 3, silver=32 + 4, clay_dk=32 + 5,
         clay=32 + 6, clay_lt=32 + 7, clay_pale=32 + 8, gold_dk=32 + 9, gold=32 + 10,
         parch=32 + 11, glaze=32 + 12)

# Palette 3, the laurels; palette 4, the star.
P3 = pal16([TRANSPARENT, INK, GOLD_DARK, GOLD, GOLD_PALE, MARBLE_LIGHT, (152, 96, 32), OLIVE_DARK])
P4 = pal16([TRANSPARENT, INK, GOLD_DARK, GOLD, GOLD_PALE, MARBLE_LIGHT])

STAR_TILE = 143
BLANK_TILES = (140, 141, 156, 157)
MAX_TILES = 192


def ell(x, y, rx, ry, cx=CX, cy=CY):
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2


# --- Shared: the cup's silhouette (lip and handles), the same on both faces ---
def cup_outline(a, inside):
    """Paint the lip and handles; call inside(x, y) for the bowl's interior."""
    for y in range(H):
        for x in range(W):
            e = ell(x, y, RX, RY)
            if e > 1:
                continue
            ei = ell(x, y, RX - LIP, RY - LIP)
            if ell(x, y, RX - 1, RY - 1) > 1:
                a[y, x] = K["ink"]
            elif ei > 1:
                # the lip: lit along the top, shaded toward the foot. The light
                # is from above rather than the top left, so the cup's two halves
                # mirror and share their tiles.
                # A band of metal (or glaze, at no stars) with a lit outer
                # edge, the same all round so the cup's quarters share tiles.
                if ell(x, y, RX - 2, RY - 2) > 1:
                    a[y, x] = K["lit"]
                elif ell(x, y, RX - 4, RY - 4) > 1:
                    a[y, x] = K["mid"]
                else:
                    a[y, x] = K["shade"]
            elif ell(x, y, RX - LIP - 1, RY - LIP - 1) > 1:
                a[y, x] = K["ink"]
            else:
                a[y, x] = inside(x, y)
    # rosettes on the lip, at the four quarters and the four diagonals
    for k in range(8):
        t = k * math.pi / 4 + math.pi / 8
        x, y = CX + (RX - 2.5) * math.cos(t), CY + (RY - 2.5) * math.sin(t)
        xi, yi = int(round(x - 0.5)), int(round(y - 0.5))
        for (dx, dy) in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            a[yi + dy, xi + dx] = K["gold"]
    handles(a)


def handles(a):
    """Two horizontal loop handles, glaze, lit on top, the cloth showing through."""
    for side in (-1, 1):
        hx = CX + side * (RX + 6)
        for y in range(int(CY) - 12, int(CY) + 14):
            for x in range(W):
                if side * (x - CX) < RX - 6:
                    continue
                e_out = ell(x, y, 15, 10, hx, CY)
                e_in = ell(x, y, 9, 4.5, hx, CY)
                if e_out <= 1 and e_in > 1 and ell(x, y, RX - 1, RY - 1) > 1:
                    edge = ell(x, y, 14, 9, hx, CY) > 1 or ell(x, y, 10, 5.5, hx, CY) <= 1
                    if edge:
                        a[y, x] = K["ink"]
                    else:
                        a[y, x] = K["lit"] if y < CY - 3 else (K["mid"] if y < CY + 4 else K["shade"])


# --- Front: the bowl, the tondo ----------------------------------------------
TX, TY = 38, 35               # the tondo's outer radii; its band is 5 px


def front():
    a = np.zeros((H, W), np.uint8)

    def inside(x, y):
        et = ell(x, y, TX, TY)
        if et <= 1:
            if ell(x, y, TX - 1, TY - 1) > 1 or (ell(x, y, TX - 5, TY - 5) > 1 and ell(x, y, TX - 6, TY - 6) <= 1):
                return K["ink"]
            if ell(x, y, TX - 5, TY - 5) > 1:
                return K["glaze"]
            # the tondo's ground: light clay over a dark ground line
            if y > CY + 22:
                return K["clay_dk"] if y > CY + 23 else K["ink"]
            return K["clay_lt"]
        # the bowl's wall: shadowed near the lip on its top-left
        ei = ell(x, y, RX - LIP - 1, RY - LIP - 1)
        nx, ny = (x - CX) / RX, (y - CY) / RY
        if ei > 0.9:
            return K["cream_sh"]
        return K["cream"]

    cup_outline(a, inside)
    # the tondo band: clay dots set round it, mirrored in all four quarters
    for k in range(10):
        t = (k + 0.5) * (math.pi / 2) / 10
        dx, dy = (TX - 2.5) * math.cos(t), (TY - 2.5) * math.sin(t)
        for sx in (-1, 1):
            for sy in (-1, 1):
                x, y = CX + sx * dx, CY + sy * dy
                xi, yi = int(math.floor(x)), int(math.floor(y))
                a[yi, xi] = K["dots"]
    # an incised line framing the inscriptions either side, like a cup's frieze
    for x in range(34, 82):
        if x % 2 == 0:
            a[78, x] = K["incise"]
    mirror(a)
    return a


def mirror(a):
    """Copy the left half onto the right, so the halves share tiles (H-flip)."""
    a[:, W // 2:] = a[:, :W // 2][:, ::-1]


# --- Back: the cup's underside, the foot and the wreath ---------------------
WCX, WCY = 119.5, 63.5        # the wreath's centre
WRX, WRY = 60, 36             # the ring the leaves sit on
FRX, FRY = 30, 21             # the foot ring
PANEL_TOP, PANEL_BOTTOM = 104, 139   # the stats band (rows printed at y 105 and 121)
# The eight laurel slots, as 16x16 cells: the left branch rises from the tie
# at the foot of the wreath (1 Hearth ... 4 Mask), the right branch comes down
# (5 Moon ... 8 Sun). Angles are degrees on the wreath's ring, y down.
SLOT_ANGLES = [118, 152, 190, 228, 312, 350, 28, 62]


def slot_cells():
    """Each slot's top-left tile. The right branch mirrors the left exactly."""
    cells = []
    for deg in SLOT_ANGLES:
        left = 90 < deg < 270
        t = math.radians(deg if left else 180 - deg)
        x = WCX + WRX * math.cos(t)
        y = WCY + WRY * math.sin(t)
        cx, cy = int(round((x - 8) / 8)), int(round((y - 8) / 8))
        cells.append((cx if left else 28 - cx, cy))
    return cells


def back():
    a = np.zeros((H, W), np.uint8)

    def inside(x, y):
        # the underside: clay, lit top-left, shading toward the lip
        nx, ny = (x - CX) / RX, (y - CY) / RY
        ei = ell(x, y, RX - LIP - 1, RY - LIP - 1)
        if ei > 0.86:
            return K["clay_dk"]
        return K["clay"]

    cup_outline(a, inside)
    # a white-ground band below the wreath, where the stats are written: the
    # engine prints them in red and ink, which clay would swallow
    for y in range(PANEL_TOP, PANEL_BOTTOM + 1):
        for x in range(W):
            if ell(x, y, RX - LIP - 2, RY - LIP - 2) > 1:
                continue
            if y in (PANEL_TOP, PANEL_BOTTOM):
                a[y, x] = K["ink"]
            elif y == PANEL_TOP + 1:
                a[y, x] = K["cream_sh"]
            else:
                a[y, x] = K["cream"]
    paint_foot_and_wreath(a)
    mirror(a)
    inscribe_laurels(a)
    unify_palettes(a)
    return a


def unify_palettes(a):
    """A tile has one palette: any tile the wreath (palette 2) touches is
    repainted in palette 2's copies of the cup's colors."""
    to_p2 = {K["ink"]: T["ink"], K["glaze"]: T["glaze"], K["clay"]: T["clay"],
             K["clay_dk"]: T["clay_dk"], K["clay_pale"]: T["clay_pale"], K["clay_lt"]: T["clay_lt"],
             K["cream"]: T["parch"], K["gold"]: T["gold"]}
    for ty in range(20):
        for tx in range(30):
            cell = a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            if not ((cell >> 4) == 2).any():
                continue
            for k, v in to_p2.items():
                cell[cell == k] = v
            left = cell[(cell != 0) & ((cell >> 4) != 2)]
            assert left.size == 0, f"tile ({tx},{ty}) keeps palette-0 colors {set(left.tolist())}"


def paint_foot_and_wreath(a):
    # the foot: a raised ring in glaze, its centre reserved for the victor's name
    for y in range(H):
        for x in range(W):
            e = ell(x, y, FRX, FRY, WCX, WCY)
            if e <= 1:
                if ell(x, y, FRX - 1, FRY - 1, WCX, WCY) > 1:
                    a[y, x] = K["ink"]
                elif ell(x, y, FRX - 4, FRY - 4, WCX, WCY) > 1:
                    a[y, x] = K["glaze"]
                elif ell(x, y, FRX - 5, FRY - 5, WCX, WCY) > 1:
                    a[y, x] = K["ink"]
                else:
                    a[y, x] = K["cream"]
    wreath(a)


def wreath(a):
    """The bare wreath, in black-figure glaze: two laurel branches on the ring,
    tied at the foot, with a faint outline where each Laurel's leaf will go."""
    cells = slot_cells()
    # twigs: along the ring, from the tie (90 deg) round each side to the top
    for deg10 in range(900, 2700 + 1, 3):
        for side in (-1, 1):
            t = math.radians(deg10 / 10.0)
            x = WCX + side * WRX * math.cos(t)
            y = WCY + WRY * math.sin(t)
            if deg10 > 2460:      # the branches stop short of meeting at the top
                continue
            xi, yi = int(math.floor(x)), int(math.floor(y))
            a[yi, xi] = T["ink"]
            a[yi - 1, xi] = T["glaze"] if a[yi - 1, xi] != T["ink"] else a[yi - 1, xi]
    # laurel leaves along the twig between the slots, alternately inside and
    # outside, each pointing up the branch toward the crown
    for k, deg in enumerate(range(98, 246, 7)):
        if any(abs(deg - s) < 11 for s in SLOT_ANGLES):
            continue
        t = math.radians(deg)
        x, y = WCX + WRX * math.cos(t), WCY + WRY * math.sin(t)
        # tangent toward the top of the wreath (increasing angle), and the outward normal
        tx, ty = -WRX * math.sin(t), WRY * math.cos(t)
        n = math.hypot(tx, ty)
        tx, ty = tx / n, ty / n
        nx, ny = (x - WCX) / WRX, (y - WCY) / WRY
        n = math.hypot(nx, ny)
        nx, ny = nx / n, ny / n
        out = 1 if k % 2 == 0 else -1
        dx, dy = 0.75 * tx + 0.66 * out * nx, 0.75 * ty + 0.66 * out * ny
        for s in range(5):
            px, py = int(math.floor(x + dx * s)), int(math.floor(y + dy * s))
            a[py, px] = T["glaze"]
            if 1 <= s <= 2:
                qx, qy = int(math.floor(x + dx * s + tx)), int(math.floor(y + dy * s + ty))
                if a[qy, qx] != T["ink"]:
                    a[qy, qx] = T["glaze"]
    # the tie: a ribbon knot at the foot of the wreath
    tx, ty = int(WCX), int(WCY + WRY)
    for (dx, dy) in [(-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (-3, 2), (-2, 1),
                     (2, 1), (3, 2), (-3, 3), (3, 3), (-4, 4), (4, 4)]:
        a[ty + dy, tx + dx] = T["gold"]
    a[ty, tx] = T["gold_dk"]
    # ghost leaves where the Laurels go
    for (cx, cy), deg in zip(cells, SLOT_ANGLES):
        leaf_ghost(a, cx * 8, cy * 8, deg)


def inscribe_laurels(a):
    """LAURELS, inscribed in the gap at the top of the wreath."""
    s = "LAURELS"
    w = sum(len(GLYPHS[ch][0]) + 1 for ch in s) - 1
    x0 = int(WCX + 0.5) - w // 2
    y0 = int(WCY - WRY) - 7

    class C:
        def px(self, x, y, c):
            a[y, x] = c
    letter(C(), x0, y0, s, K["ink"])


def slot_leaf(deg):
    """The leaf for a slot: the right branch's leaves are the left's, mirrored,
    exactly as the wreath art is (mirror())."""
    if 90 < deg < 270:
        return leaf_mask(deg)
    return leaf_mask(180 - deg)[:, ::-1]


def leaf_mask(deg):
    """A laurel leaf in a 16x16 cell, laid along the wreath at this angle."""
    m = np.zeros((16, 16), np.uint8)
    t = math.radians(deg + 90)            # along the ring
    ux, uy = math.cos(t), math.sin(t)
    for y in range(16):
        for x in range(16):
            dx, dy = x - 7.5, y - 7.5
            along = dx * ux + dy * uy
            across = -dx * uy + dy * ux
            # a pointed oval, 15 long and 9 wide
            if (along / 7.4) ** 2 + (across / 4.6) ** 2 <= 1 - 0.25 * (along / 7.4):
                m[y, x] = 1
    return m


def leaf_ghost(a, x0, y0, deg):
    m = slot_leaf(deg)
    for y in range(16):
        for x in range(16):
            if not m[y, x]:
                continue
            edge = any(not (0 <= y + dy < 16 and 0 <= x + dx < 16 and m[y + dy, x + dx])
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                a[y0 + y, x0 + x] = K["clay_dk"]


# --- The laurels: badges.png, one gold leaf per temple --------------------------
EMBLEMS = {   # 7x7, ink on gold: each Laurel's god (design/TERMS.md)
    "hearth": [  # Hestia: the hearth flame
        "   #   ",
        "  ##   ",
        "  ### #",
        " #####",
        " ## ##",
        "#######",
        " ##### ",
    ],
    "herald": [  # Hermes: the kerykeion, its two serpents
        " #   # ",
        "  # #  ",
        "   #   ",
        "  # #  ",
        "   #   ",
        "   #   ",
        "   #   ",
    ],
    "harvest": [  # Demeter: an ear of wheat
        "  # #  ",
        "   #   ",
        "  # #  ",
        "   #   ",
        "  # #  ",
        "   #   ",
        "   #   ",
    ],
    "mask": [  # Dionysus: the theater mask
        " ##### ",
        "#######",
        "# ### #",
        "#######",
        "## # ##",
        " #   # ",
        "  ###  ",
    ],
    "moon": [  # Artemis: the crescent
        "  ###  ",
        " ##    ",
        "##     ",
        "##     ",
        "##     ",
        " ##    ",
        "  ###  ",
    ],
    "forge": [  # Hephaestus: the hammer
        "#####  ",
        "#####  ",
        "  #    ",
        "  #    ",
        "  #    ",
        "  #    ",
        "  #    ",
    ],
    "foam": [  # Aphrodite: the scallop
        "       ",
        " ##### ",
        "# # # #",
        "# # # #",
        " #####",
        "  ###  ",
        "   #   ",
    ],
    "sun": [  # Apollo: the sun
        "#  #  #",
        " #   # ",
        "  ###  ",
        "# ### #",
        "  ###  ",
        " #   # ",
        "#  #  #",
    ],
}
LAUREL_ORDER = ["hearth", "herald", "harvest", "mask", "moon", "forge", "foam", "sun"]


def laurel(deg, emblem):
    """A gold leaf along the wreath, outlined in ink, lit top-left, its god's
    emblem painted upright on it."""
    m = slot_leaf(deg)
    a = np.zeros((16, 16), np.uint8)
    for y in range(16):
        for x in range(16):
            if not m[y, x]:
                continue
            edge = any(not (0 <= y + dy < 16 and 0 <= x + dx < 16 and m[y + dy, x + dx])
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                a[y, x] = 1
            else:
                lit = (x - 7.5) + (y - 7.5)
                a[y, x] = 4 if lit < -6 else (3 if lit < 5 else 2)
    g = EMBLEMS[emblem]
    for j, row in enumerate(g):
        for i, ch in enumerate(row):
            if ch == "#":
                x, y = 4 + i, 4 + j
                if m[y, x]:
                    a[y, x] = 1
    return a


def badges():
    sheet = np.zeros((16, 128), np.uint8)
    for i, (deg, name) in enumerate(zip(SLOT_ANGLES, LAUREL_ORDER)):
        sheet[:, i * 16:i * 16 + 16] = laurel(deg, name)
    write_indexed_png(OUT / "badges.png", sheet, [P3])
    return sheet


def star_tile():
    rows = [
        "   ##   ",
        "  #yg#  ",
        " ##gg## ",
        "#ygwgGg#",
        " #gGgG# ",
        "  #gG#  ",
        "   ##   ",
        "        ",
    ]
    key = {" ": 0, "#": 1, "G": 2, "g": 3, "y": 4, "w": 5}
    return np.array([[key[c] for c in r] for r in rows], np.uint8)


# --- The screen behind the cup -------------------------------------------------
def background():
    """A woven cloth, its ground in the hero's color with a fine diamond twill,
    and a clay border with the meander along the top and foot."""
    a = np.zeros((H, W), np.uint8)
    for y in range(H):
        for x in range(W):
            u, v = x % 8, y % 8
            twill = (u + v) % 8 == 0 or (u - v) % 8 == 4
            a[y, x] = B["mid"] if twill else B["dk"]
    for y0, flip in ((0, False), (H - 8, True)):
        rows = MEANDER[::-1] if flip else MEANDER
        for y in range(8):
            for x in range(W):
                a[y0 + y, x] = B["clay"]
        for j, row in enumerate(rows):
            for x in range(W):
                if row[x % 8] == "#":
                    a[y0 + 1 + j, x] = B["ink"]
        a[y0 + (7 if not flip else 0), :] = B["clay_dk"]
    return a


# --- Compiling ------------------------------------------------------------------
def compile_all(faces):
    """Cut the three 30x20 faces into one deduplicated tileset (with flips),
    keeping the engine's fixed tiles at their numbers."""
    reserved = {0, STAR_TILE, *BLANK_TILES}
    tiles = {0: np.zeros((8, 8), np.uint8)}
    lookup = {}

    def index(t, i):
        for v, f in [(t, 0), (t[:, ::-1], 0x400), (t[::-1, :], 0x800), (t[::-1, ::-1], 0xC00)]:
            lookup.setdefault(v.tobytes(), (i, f))

    index(tiles[0], 0)
    for b in BLANK_TILES:
        tiles[b] = np.zeros((8, 8), np.uint8)
    tiles[STAR_TILE] = star_tile()
    nxt = [1]

    def add(t):
        hit = lookup.get(t.tobytes())
        if hit:
            return hit
        while nxt[0] in reserved:
            nxt[0] += 1
        i = nxt[0]
        nxt[0] += 1
        tiles[i] = t.copy()
        index(t, i)
        return i, 0

    maps = []
    for a in faces:
        m = np.zeros((20, 30), np.uint16)
        for ty in range(20):
            for tx in range(30):
                cell = a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                pals = set((cell[cell & 15 != 0] >> 4).tolist())
                assert len(pals) <= 1, f"tile ({tx},{ty}) mixes palettes {pals}"
                pal = pals.pop() if pals else 0
                i, f = add(cell & 15)
                m[ty, tx] = i | f | (pal << 12)
        maps.append(m)
    n = max(tiles) + 1
    assert n <= MAX_TILES, f"{n} tiles; the engine loads {MAX_TILES}"
    out = [tiles.get(i, np.zeros((8, 8), np.uint8)) for i in range(n)]
    return out, maps


def write():
    faces = [background(), front(), back()]
    tiles, (mbg, mfront, mback) = compile_all(faces)
    print(f"trainer card: {len(tiles)} tiles of {MAX_TILES}")
    pal_of = lambda i: 4 if i == STAR_TILE else 0
    write_tiles_png(OUT / "tiles.png", tiles, [p0("green"), P1_THEO, P2, P3, P4], tiles_wide=16,
                    min_tiles=160, pal_of_tile=pal_of)
    for name, m in [("bg", mbg), ("front", mfront), ("front_link", mfront), ("back", mback)]:
        (OUT / f"{name}.bin").write_bytes(m.astype("<u2").tobytes())
        print(f"wrote graphics/trainer_card/{name}.bin")
    for tier in TIERS:
        write_jasc(OUT / f"{tier}.pal", p0(tier) + P1_THEO + P2)
    write_jasc(OUT / "female_bg.pal", P1_IANTHE)
    write_jasc(OUT / "star.pal", P4)
    sheet = badges()
    preview(tiles, mbg, mfront, mback, sheet)


def preview(tiles, mbg, mfront, mback, sheet):
    out = []
    for tier, p1 in [("green", P1_THEO), ("gold", P1_IANTHE)]:
        pals = [p0(tier), p1, P2, P3, P4]
        bg = render_map(mbg, tiles, pals, 30, 20)
        for m in (mfront, mback):
            card = render_map(m, tiles, pals, 30, 20, transparent=(0, 0, 0))
            img = bg.copy()
            mask = np.zeros((160, 240), bool)
            for ty in range(20):
                for tx in range(30):
                    e = int(m[ty, tx])
                    idx, hf, vf = e & 0x3FF, e & 0x400, e & 0x800
                    t = np.asarray(tiles[idx]) & 15
                    if hf:
                        t = t[:, ::-1]
                    if vf:
                        t = t[::-1]
                    mask[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = t != 0
            img[mask] = card[mask]
            out.append(img)
    # laurels on the back, all eight, for the preview
    img = out[1].copy()
    p3 = np.array(P3, np.uint8)
    for i, (cx, cy) in enumerate(slot_cells()):
        leaf = sheet[:, i * 16:i * 16 + 16]
        sub = img[cy * 8:cy * 8 + 16, cx * 8:cx * 8 + 16]
        sub[leaf != 0] = p3[leaf[leaf != 0]]
    out.append(img)
    grid = np.vstack([np.hstack(out[0:2]), np.hstack([out[4], out[2]])])
    save_rgb(IMG / "ui_card_parts.png", grid, 2)


if __name__ == "__main__":
    write()
