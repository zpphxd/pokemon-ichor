#!/usr/bin/env python3
"""Paint the Aethos region map: a black-figure map on terracotta.

The land is reserved clay with an incised ink coast; the sea is black glaze
with wine-purple wave strokes (Homer's wine-dark sea); roads are ink dots,
trireme lanes gold dashes; each place has a small painted glyph; a meander
border runs round the edge, the same key as the dialogue box. The geography
and the map-section grid are documented in design/AETHOS_MAP.md.

The map is one 240x160 picture, cut into 8x8 tiles:
  - the Fly map and the wall map (src/region_map.c) show it on an affine BG:
    8bpp, at most 256 tiles, no flips, a 64x64 byte tilemap
  - the Pokedex area view shows it on a text BG: 8bpp, 32x32 u16 tilemap
Both load the palette at BG palette 7 (colors 112-159), so the PNG indices are
offset by 112 and at most 48 colors are used.

The grid: section cell (gx, gy) is screen tile (gx + 1, gy + 2), the region
map's MAPCURSOR_X_MIN / MAPCURSOR_Y_MIN.

Writes:
  graphics/pokenav/region_map/map.png, map.bin, map.pal   (Fly and wall map)
  graphics/pokedex/region_map.png, region_map.bin, region_map.pal (dex area)
  design/phase1/img/ui_world_map*.png                      (previews)

Usage: python3 tools/ichor/art/ui_world_map.py
"""
import numpy as np
from PIL import Image, ImageDraw

from ui_menus_lib import (ROOT, Canvas, INK, CLAY_DARK, CLAY, CLAY_LIGHT, CLAY_PALE,
                          PARCHMENT, MARBLE, MARBLE_DARK, MARBLE_LIGHT, GOLD, GOLD_DARK,
                          GOLD_PALE, OLIVE, OLIVE_DARK, AEGEAN_LIGHT, save_rgb, write_jasc)

IMG = ROOT / "design/phase1/img"
W, H = 240, 160
PAL_BASE = 112   # BG palette 7, where both screens load the map palette

# --- Palette ---------------------------------------------------------------
COLORS = [
    ("glaze", (40, 24, 32)),        # the sea: black glaze with a wine cast
    ("wine_dk", (72, 32, 56)),      # wave strokes
    ("wine", (104, 48, 72)),        # surf along the coast, lit strokes
    ("wine_lt", (152, 88, 104)),    # foam, lanes' shadow side
    ("ink", INK),                   # coast, roads, glyph outlines
    ("clay_dk", CLAY_DARK),         # incised hatching, mountain shade
    ("clay", CLAY),                 # the land
    ("clay_lt", CLAY_LIGHT),        # lit coast, plains
    ("clay_pale", CLAY_PALE),       # highlights
    ("parch", PARCHMENT),           # snow shade, foam
    ("white", MARBLE_LIGHT),        # added white: temples, snow, clouds
    ("marble", MARBLE),
    ("marble_dk", MARBLE_DARK),
    ("gold", GOLD),                 # temples' pediments, lanes
    ("gold_dk", GOLD_DARK),
    ("gold_pale", GOLD_PALE),
    ("olive", OLIVE),               # olive and cypress crowns
    ("olive_dk", OLIVE_DARK),
    ("lava", (240, 88, 40)),        # Kaldera's forge
    ("lava_dk", (176, 40, 24)),
    ("pool", AEGEAN_LIGHT),         # sacred pools and lakes
    ("ghost", (152, 72, 48)),       # unrevealed places: a shade under the clay
    ("ghost_sea", (88, 48, 72)),    # unrevealed in the sea
]
C = {name: i for i, (name, _) in enumerate(COLORS)}
RGB = [rgb for _, rgb in COLORS]
assert len(RGB) <= 48


def cell_px(gx, gy):
    """Top-left pixel of map-section cell (gx, gy)."""
    return (gx + 1) * 8, (gy + 2) * 8


# --- Geography (screen pixels; see design/AETHOS_MAP.md) ---------------------
# The north: Thessaly, Boeotia and Attica, from the Ionian shore round to Sounion
MAINLAND = [
    (30, 8), (102, 8), (99, 15), (98, 22), (103, 28), (110, 30), (114, 36), (109, 39),
    (111, 43), (107, 46), (112, 49), (119, 53), (126, 57), (133, 62), (136, 70),
    (131, 74), (125, 69), (116, 66), (107, 65), (100, 66), (95, 66), (92, 61), (88, 55),
    (82, 51), (72, 50), (60, 51), (48, 52), (40, 56), (34, 53), (32, 42), (28, 32),
    (30, 22), (27, 14),
]
# The Peloponnese, joined to the north at the Isthmus
PELOPONNESE = [
    (84, 58), (91, 60), (97, 65), (98, 73), (104, 75), (112, 79), (114, 85), (107, 88),
    (100, 84), (98, 91), (102, 99), (100, 107), (96, 112), (92, 109), (88, 100), (84, 103),
    (80, 111), (76, 118), (72, 121), (68, 117), (66, 108), (62, 104), (58, 109),
    (54, 115), (50, 111), (46, 101), (42, 92), (38, 81), (36, 70), (40, 62), (48, 60),
    (60, 60), (74, 59),
]
EUBOEA = [(113, 41), (121, 41), (131, 46), (141, 51), (139, 55), (129, 52), (118, 48)]
CRETE = [
    (103, 125), (113, 120), (127, 119), (143, 118), (156, 119), (167, 117), (181, 118),
    (196, 116), (209, 119), (213, 124), (205, 130), (189, 133), (173, 136), (157, 138),
    (139, 138), (123, 136), (110, 133), (103, 129),
]
KALLISTE = [(142, 70), (150, 67), (154, 71), (156, 79), (154, 87), (156, 93), (150, 98),
            (144, 96), (142, 88), (140, 79)]
KYTHERA = [(88, 113), (95, 113), (97, 118), (92, 122), (87, 119)]
ISLANDS = [
    [(17, 15), (22, 13), (25, 18), (22, 27), (18, 23)],          # Kerkyra (the Odyssey's west)
    [(21, 52), (28, 51), (30, 57), (25, 61), (22, 58)],          # Kephallenia
    [(25, 70), (31, 69), (32, 75), (27, 77)],                    # Zakynthos
    [(110, 72), (115, 71), (116, 76), (111, 77)],                # Aigina, in the Saronic
    [(135, 77), (139, 76), (139, 82), (135, 82)],                # Keos
    [(144, 51), (151, 53), (153, 59), (147, 60), (144, 56)],     # Andros
    [(157, 60), (162, 61), (161, 65), (157, 64)],                # Tenos
    [(166, 66), (172, 67), (171, 71), (166, 71)],                # Mykonos
    [(131, 86), (137, 85), (138, 91), (132, 92)],                # Paros, Kalliste's neighbor
    [(121, 101), (128, 100), (129, 105), (122, 106)],            # Melos
    [(157, 103), (162, 103), (161, 107), (157, 107)],            # Ios
    [(171, 90), (180, 91), (179, 95), (171, 94)],                # Amorgos
    [(214, 48), (222, 47), (224, 52), (216, 54)],                # Samos
    [(217, 98), (225, 96), (228, 104), (220, 108)],              # Rhodes
]
# Kaldera: the caldera ring of Thera, open to the west, with the burning islet
KALDERA_RING = [(163, 102), (169, 103), (171, 108), (168, 113), (162, 114), (165, 110),
                (167, 107), (165, 105)]
KALDERA_SOUTH = [(158, 112), (162, 111), (162, 114), (158, 114)]


def land_mask():
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    for poly in [MAINLAND, PELOPONNESE, EUBOEA, CRETE, KALLISTE, KYTHERA, KALDERA_RING,
                 KALDERA_SOUTH] + ISLANDS:
        d.polygon(poly, fill=1)
    m = np.array(im, bool)
    m[:8, :] = m[8:9, :]   # the north runs on past the border
    return m


# --- Sections: (MAPSEC, name, cells) ---------------------------------------
# Story order first; see design/AETHOS_MAP.md for the route through them.
SECTIONS = [
    ("MAPSEC_ELAIA_VILLAGE", "ELAIA VILLAGE", [(17, 9)]),
    ("MAPSEC_KALLISTE_ROUTE_1", "ROUTE 1", [(17, 8)]),
    ("MAPSEC_AKTI_TOWN", "AKTI TOWN", [(17, 7)]),
    ("MAPSEC_EMPORION_CITY", "EMPORION CITY", [(10, 6)]),
    ("MAPSEC_AETHOS_ROUTE_2", "ROUTE 2", [(11, 5)]),
    ("MAPSEC_ELEUSA_VILLAGE", "ELEUSA VILLAGE", [(12, 5)]),
    ("MAPSEC_AETHOS_ROUTE_3", "ROUTE 3", [(12, 4)]),
    ("MAPSEC_THYRSA_CITY", "THYRSA CITY", [(12, 3)]),
    ("MAPSEC_AETHOS_ROUTE_4", "ROUTE 4", [(11, 3), (10, 3)]),
    ("MAPSEC_DELPHOI", "DELPHOI", [(9, 3)]),
    ("MAPSEC_AETHOS_ROUTE_15", "ROUTE 15", [(8, 4), (7, 4), (6, 4), (5, 4), (4, 4)]),
    ("MAPSEC_AETHOS_ROUTE_5", "ROUTE 5", [(7, 5), (7, 6)]),
    ("MAPSEC_ARKADIA", "ARKADIA", [(7, 7)]),
    ("MAPSEC_AETHOS_ROUTE_6", "ROUTE 6", [(8, 7), (9, 6)]),
    ("MAPSEC_AETHOS_ROUTE_7", "ROUTE 7", [(13, 5)]),
    ("MAPSEC_ASTYRA", "ASTYRA", [(14, 5), (15, 5)]),
    ("MAPSEC_AETHOS_ROUTE_11", "ROUTE 11", [(16, 7), (15, 7), (14, 7), (13, 7)]),
    ("MAPSEC_AETHOS_ROUTE_12", "ROUTE 12", [(16, 9), (16, 10), (17, 10), (18, 10)]),
    ("MAPSEC_KALDERA", "KALDERA", [(19, 11)]),
    ("MAPSEC_AETHOS_ROUTE_13", "ROUTE 13", [(11, 12), (12, 12), (13, 12), (14, 12), (15, 12),
                                           (16, 12), (17, 12), (18, 12)]),
    ("MAPSEC_KYTHERA_ISLE", "KYTHERA ISLE", [(10, 12)]),
    ("MAPSEC_KNOSSA_ISLE", "KNOSSA ISLE", [(17, 13)]),
    ("MAPSEC_AETHOS_ROUTE_14", "ROUTE 14", [(10, 11), (9, 10)]),
    ("MAPSEC_AETHOS_ROUTE_8", "ROUTE 8", [(7, 8)]),
    ("MAPSEC_LAKONIA", "LAKONIA", [(8, 9)]),
    ("MAPSEC_THE_ASCENT", "THE ASCENT", [(9, 2), (9, 1)]),
    ("MAPSEC_MOUNT_OLYMPUS", "MT. OLYMPUS", [(8, 0), (9, 0)]),
    # Post-game: hidden on the map until the game is cleared (region_map.c)
    ("MAPSEC_AETHOS_ROUTE_9", "ROUTE 9", [(8, 10), (7, 11)]),
    ("MAPSEC_CAPE_TAINARON", "CAPE TAINARON", [(7, 12)]),
    ("MAPSEC_AETHOS_ROUTE_10", "ROUTE 10", [(6, 7), (5, 7)]),
    ("MAPSEC_OLYMPIA", "OLYMPIA", [(4, 7)]),
    ("MAPSEC_ATLANTIS", "ATLANTIS", [(1, 11)]),
]
POSTGAME = {"MAPSEC_AETHOS_ROUTE_9", "MAPSEC_CAPE_TAINARON", "MAPSEC_AETHOS_ROUTE_10",
            "MAPSEC_OLYMPIA", "MAPSEC_ATLANTIS"}


def center(cell):
    x, y = cell_px(*cell)
    return x + 4, y + 4


# --- Glyphs ---------------------------------------------------------------
# Keys: # ink, d clay_dk, c clay, l clay_lt, p clay_pale, w white, m marble,
# M marble_dk, g gold, G gold_dk, y gold_pale, o olive, O olive_dk, r lava,
# R lava_dk, b pool, h ghost, s ghost_sea, ~ wine, ' parch; space = leave.
KEY = {"#": "ink", "d": "clay_dk", "c": "clay", "l": "clay_lt", "p": "clay_pale",
       "w": "white", "m": "marble", "M": "marble_dk", "g": "gold", "G": "gold_dk",
       "y": "gold_pale", "o": "olive", "O": "olive_dk", "r": "lava", "R": "lava_dk",
       "b": "pool", "h": "ghost", "s": "ghost_sea", "~": "wine", "'": "parch",
       "k": "glaze", "v": "wine_lt"}

TEMPLE = [          # a Doric temple front: gold pediment, white columns
    "   ##   ",
    "  #gg#  ",
    " #gGGg# ",
    "########",
    " w w w  ",
    " w w w  ",
    "########",
    "        ",
]
AKROPOLIS = [       # the Parthenon on its rock, 16x8
    "                ",
    "     ######     ",
    "    #gggggg#    ",
    "   ##########   ",
    "    w w w w w   ",
    "  ############  ",
    " #ddddddddddddd#",
    "#dddcddddcdddddd",
]
THEATER = [
    "  ####  ",
    " #wmmw# ",
    "#wm##mw#",
    "#m#cc#m#",
    "#w#cc#w#",
    " ##cc## ",
    " #####  ",
    "        ",
]
OMPHALOS = [        # Delphoi: the navel stone in its net, under Apollo's sun
    "   g    ",
    " g g g  ",
    "  ###   ",
    " #wMw#  ",
    "#wMwMw# ",
    "#MwMwM# ",
    "########",
    "        ",
]
MOON_GROVE = [
    "  yy    ",
    " y      ",
    " y    # ",
    "  yy #O#",
    "   #  #O",
    " #O# #O#",
    " #O#  # ",
    "  #     ",
]
WHEAT = [           # Eleusa: Demeter's sheaf
    " g g g  ",
    " gGgGg  ",
    "  gGg   ",
    "   #    ",
    "  #g#   ",
    "   #    ",
    "  # #   ",
    "        ",
]
SHIELD = [          # Lakonia: a hoplite shield blazoned with lambda
    "  ####  ",
    " #gggg# ",
    "#gg#ggg#",
    "#g#G#gg#",
    "#g#gG#g#",
    " #gggg# ",
    "  ####  ",
    "        ",
]
SHELL = [           # Kythera: Aphrodite's scallop, born of the foam
    "        ",
    "  ####  ",
    " #w'w'# ",
    "#'w'w'w#",
    "#w'w'w'#",
    " #'w'w# ",
    "  #ww#  ",
    "   ##   ",
]
LABYRINTH = [       # Knossa: the Labyrinth, as on Knossian coins
    "########",
    "#pppppp#",
    "#p####p#",
    "#p#pp#p#",
    "#p#p##p#",
    "#p#pppp#",
    "#p######",
    "########",
]
OLIVE_TREE = [      # Elaia: the village olive
    "  oooo  ",
    " ooOooo ",
    "oOooOoo ",
    " oooOoo ",
    "  o##o  ",
    "   #    ",
    "   #    ",
    "  ###   ",
]
HARBOR = [          # Akti: Hestia's temple over the harbor mole
    "   ##   ",
    "  #gg#  ",
    " #gGGg# ",
    "########",
    " w w w  ",
    " w w w  ",
    "########",
    "        ",
]
CAVE_GHOST = [      # Tainaron, unrevealed: the gate is only a shadow
    "        ",
    "  hhhh  ",
    " hhhhhh ",
    " hh  hh ",
    " hh  hh ",
    "        ",
    "        ",
    "        ",
]
STADIUM_GHOST = [   # Olympia, unrevealed: the stadium's faint oval
    "        ",
    " hhhhhh ",
    "h      h",
    "h      h",
    " hhhhhh ",
    "        ",
    "        ",
    "        ",
]
ATLANTIS_GHOST = [  # Atlantis, sunken: Plato's rings of land and water
    "  ssss  ",
    " s    s ",
    "s  ss  s",
    "s s  s s",
    "s s  s s",
    "s  ss  s",
    " s    s ",
    "  ssss  ",
]
MOUNTAIN = [        # black-figure peak, lit on the left
    "   #    ",
    "  #l#   ",
    "  #ld#  ",
    " #lcdd# ",
    " #lcdd# ",
    "#lccddd#",
    "########",
    "        ",
]
SMALL_PEAK = [
    "        ",
    "        ",
    "   #    ",
    "  #l#   ",
    " #lcd#  ",
    "#lccdd# ",
    "####### ",
    "        ",
]
CYPRESS = [
    "  #     ",
    " #O#    ",
    " #O# #  ",
    "#OO##O# ",
    "#OO##O# ",
    " ## #O# ",
    "  #  #  ",
    "        ",
]
VINES = [           # Thyrsa's vineyards
    "        ",
    " o  o  o",
    "#o##o##o",
    " #  #  #",
    "        ",
    " o  o  o",
    "#o##o##o",
    " #  #  #",
]
FIELDS = [          # Eleusa's wheat plain
    "        ",
    " g g g g",
    " G G G G",
    "        ",
    "g g g g ",
    "G G G G ",
    "        ",
    "        ",
]
OLIVES = [          # Kalliste's groves
    "        ",
    " oo     ",
    "oOoo    ",
    " ##  oo ",
    "    oOoo",
    "     ## ",
    "        ",
    "        ",
]
def olympus(c, px, py):
    """The mountain of the gods: a lit west face, a shaded east face, snow on
    the summit, a cloud bank about its waist and a gold glint, the Pantheon,
    at the very top. (px, py) is the peak."""
    h = 20
    for r in range(h):
        half = r * 7 // 8
        y = py + r
        for x in range(px - half - 1, px + half + 2):
            edge = x in (px - half - 1, px + half + 1)
            if edge or r == h - 1:
                col = "ink"
            elif r < 6:
                col = "white" if x <= px + (r // 3) else "parch"
            else:
                col = "clay_lt" if x < px - half // 2 else ("clay" if x <= px else "clay_dk")
            c.px(x, y, C[col])
    for (cx, cy, rx) in [(px - 9, py + 9, 6), (px + 9, py + 10, 7), (px - 2, py + 11, 5),
                         (px + 3, py + 8, 4)]:
        for x in range(cx - rx, cx + rx + 1):
            c.px(x, cy, C["white"])
            if abs(x - cx) < rx - 1:
                c.px(x, cy - 1, C["white"])
            if abs(x - cx) < rx:
                c.px(x, cy + 1, C["marble"])
    c.px(px, py + 1, C["gold"])
    c.px(px, py, C["gold_pale"])




DOLPHIN = [         # black-figure dolphins leap in the empty sea, painted in clay
    "     d          ",
    "    dcc         ",
    "  ccllcc     c  ",
    " cllcccccc  cc  ",
    "c#cc    ccccccc ",
    " cc        c  c ",
    "                ",
    "                ",
]


def stamp(c, glyph, x, y):
    for j, row in enumerate(glyph):
        for i, ch in enumerate(row):
            if ch != " ":
                c.px(x + i, y + j, C[KEY[ch]])


# --- Painting -----------------------------------------------------------------
def paint():
    land = land_mask()
    c = Canvas(W, H, C["glaze"])

    # The sea: wine strokes scattered on a 16x16 repeat, so open sea costs four tiles.
    for y in range(H):
        for x in range(W):
            if land[y, x]:
                continue
            u, v = x % 16, y % 16
            if (v == 3 and 2 <= u <= 5) or (v == 2 and u in (6, 7)) or (v == 4 and u == 1):
                c.px(x, y, C["wine_dk"])
            if (v == 11 and 10 <= u <= 13) or (v == 10 and u in (14, 15)) or (v == 12 and u == 9):
                c.px(x, y, C["wine_dk"])

    # The land: reserved clay with an incised ink coast, lit on its top-left edges.
    for y in range(H):
        for x in range(W):
            if land[y, x]:
                c.px(x, y, C["clay"])
    for y in range(H):
        for x in range(W):
            if not land[y, x]:
                continue
            n = [land[y + dy, x + dx] if 0 <= y + dy < H and 0 <= x + dx < W else True
                 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if not all(n):
                c.px(x, y, C["ink"])
            elif (x > 0 and not land[y, x - 2 if x > 1 else 0]) or (y > 1 and not land[y - 2, x]):
                c.px(x, y, C["clay_lt"])
    # surf: one wine pixel of foam outside every coast
    for y in range(H):
        for x in range(W):
            if land[y, x]:
                continue
            if any(0 <= y + dy < H and 0 <= x + dx < W and land[y + dy, x + dx]
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                c.px(x, y, C["wine"])

    # Landscape: the ranges, forests and fields that make each region itself.
    # Each sits in a whole cell of plain land, so repeats cost no new tiles.
    def cellstamp(glyph, cells):
        for (tx, ty) in cells:
            stamp(c, glyph, tx * 8, ty * 8)

    cellstamp(MOUNTAIN, [(5, 3), (6, 4), (5, 5), (7, 3), (8, 5), (6, 2)])     # Pindos
    cellstamp(MOUNTAIN, [(9, 4)])                                              # Parnassos
    cellstamp(SMALL_PEAK, [(12, 6)])                                           # Kithairon
    cellstamp(MOUNTAIN, [(8, 12), (8, 13)])                                    # Taygetos
    cellstamp(SMALL_PEAK, [(11, 11)])                                          # Parnon
    cellstamp(SMALL_PEAK, [(6, 8), (10, 10), (6, 10)])                         # Arkadian hills
    cellstamp(CYPRESS, [(7, 9), (8, 10), (7, 8)])                              # Arkadia's cypresses
    cellstamp(MOUNTAIN, [(16, 15)])                                            # Ida, on Knossa
    cellstamp(SMALL_PEAK, [(23, 15), (21, 15)])
    cellstamp(SMALL_PEAK, [(13, 3)])                                           # Pelion
    cellstamp(OLIVES, [(18, 10)])                                              # Kalliste's groves
    olympus(c, 80, 8)
    for (x, y, flip) in [(196, 80, False), (176, 40, True), (12, 120, False)]:  # dolphins
        stamp(c, [r[::-1] for r in DOLPHIN] if flip else DOLPHIN, x, y)

    # Roads: ink dots, one every other pixel, centre to centre.
    def road(points, color="ink", step=2, faint=False):
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0))
            for k in range(0, n + 1):
                if k % step:
                    continue
                x = round(x0 + (x1 - x0) * k / n)
                y = round(y0 + (y1 - y0) * k / n)
                if land[y, x]:
                    c.px(x, y, C[color])

    def lane(points):
        """A trireme lane: gold dashes over the sea, 3 on and 2 off."""
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0))
            for k in range(0, n + 1):
                if k % 5 >= 3:
                    continue
                x = round(x0 + (x1 - x0) * k / n)
                y = round(y0 + (y1 - y0) * k / n)
                if not land[y, x]:
                    c.px(x, y, C["gold_dk"])

    ctr = {s[0]: [center(cell) for cell in s[2]] for s in SECTIONS}
    road([ctr["MAPSEC_ELAIA_VILLAGE"][0], ctr["MAPSEC_AKTI_TOWN"][0]])
    road([ctr["MAPSEC_EMPORION_CITY"][0], ctr["MAPSEC_AETHOS_ROUTE_2"][0], ctr["MAPSEC_ELEUSA_VILLAGE"][0]])
    road([ctr["MAPSEC_ELEUSA_VILLAGE"][0], ctr["MAPSEC_THYRSA_CITY"][0]])
    road([ctr["MAPSEC_THYRSA_CITY"][0], ctr["MAPSEC_DELPHOI"][0]])
    road([ctr["MAPSEC_ELEUSA_VILLAGE"][0], ctr["MAPSEC_ASTYRA"][0]])
    road([(68, 61), ctr["MAPSEC_ARKADIA"][0]])                                   # Aigion to Arkadia
    road([ctr["MAPSEC_ARKADIA"][0], (76, 76), (84, 68), ctr["MAPSEC_EMPORION_CITY"][0]])
    road([ctr["MAPSEC_ARKADIA"][0], (68, 84), ctr["MAPSEC_LAKONIA"][0]])
    road([ctr["MAPSEC_LAKONIA"][0], (84, 100)])                                  # down to Gytheion
    road([ctr["MAPSEC_DELPHOI"][0], (84, 28), (84, 22)])                         # the Ascent
    road([ctr["MAPSEC_DELPHOI"][0], (82, 50)])                                   # down to Kirrha
    # post-game roads, unrevealed: sparse ghost dots
    road([ctr["MAPSEC_LAKONIA"][0], (76, 100), (68, 108), (69, 115)], color="ghost", step=3)
    road([ctr["MAPSEC_ARKADIA"][0], (52, 76), (45, 76)], color="ghost", step=3)

    # Trireme lanes
    lane([(149, 71), (141, 76), (130, 78), (120, 77), (106, 70), (97, 67)])      # Akti to Emporion
    lane([(82, 51), (70, 58)])                                                    # the Gulf ferry
    lane([(124, 70), (132, 84), (141, 94), (156, 101), (161, 106)])              # Astyra to Kaldera
    lane([(160, 110), (140, 113), (110, 115), (98, 116)])                         # Kaldera to Kythera
    lane([(140, 113), (146, 119)])                                                # ... and to Knossa
    lane([(92, 112), (86, 104)])                                                  # Kythera to Gytheion

    # Place glyphs, drawn last so they sit on top
    def at(sec, glyph, dx=0, dy=0, i=0):
        x, y = cell_px(*[s for s in SECTIONS if s[0] == sec][0][2][i])
        stamp(c, glyph, x + dx, y + dy)

    at("MAPSEC_ELAIA_VILLAGE", OLIVE_TREE)
    at("MAPSEC_AKTI_TOWN", HARBOR)
    at("MAPSEC_EMPORION_CITY", TEMPLE)
    at("MAPSEC_ELEUSA_VILLAGE", TEMPLE)
    at("MAPSEC_THYRSA_CITY", THEATER)
    at("MAPSEC_DELPHOI", OMPHALOS)
    at("MAPSEC_ARKADIA", MOON_GROVE)
    at("MAPSEC_ASTYRA", AKROPOLIS)
    at("MAPSEC_KYTHERA_ISLE", SHELL)
    at("MAPSEC_KNOSSA_ISLE", LABYRINTH)
    at("MAPSEC_LAKONIA", SHIELD)
    at("MAPSEC_CAPE_TAINARON", CAVE_GHOST)
    at("MAPSEC_OLYMPIA", STADIUM_GHOST)
    at("MAPSEC_ATLANTIS", ATLANTIS_GHOST)
    # Kaldera's forge burns in the caldera
    kx, ky = cell_px(19, 11)
    for (x, y, col) in [(kx + 3, ky + 3, "lava"), (kx + 4, ky + 3, "lava_dk"),
                        (kx + 3, ky + 4, "lava_dk"), (kx + 4, ky + 2, "lava")]:
        c.px(x, y, C[col])

    border(c)
    return c, land


# --- The meander border: the dialogue box's own key (ui_frames.py) -------------
MEANDER = ["#####.##", "....#.#.", ".####.#.", ".#....#.", ".######."]
TOP = ["oooooooo"] + MEANDER + ["dddddddd", "........"]
CORNER = [" ooooooo", "o#####..", "o##.##..", "o#.#.#..", "o##.##..", "o#####..",
          "o.....dd", "o.....d."]
BKEY = {" ": "glaze", "o": "clay_dk", "#": "ink", ".": "clay", "d": "clay_dk"}


def border(c):
    top = TOP
    left = ["".join(row[k] for row in TOP) for k in range(8)]
    tiles = {
        "tl": CORNER, "tr": [r[::-1] for r in CORNER], "bl": CORNER[::-1],
        "br": [r[::-1] for r in CORNER[::-1]], "t": top, "b": top[::-1],
        "l": left, "r": [r[::-1] for r in left],
    }

    def put(name, tx, ty):
        for j, row in enumerate(tiles[name]):
            for i, ch in enumerate(row):
                c.px(tx * 8 + i, ty * 8 + j, C[BKEY[ch]])

    for tx in range(1, 29):
        put("t", tx, 0)
        put("b", tx, 19)
    for ty in range(1, 19):
        put("l", 0, ty)
        put("r", 29, ty)
    put("tl", 0, 0), put("tr", 29, 0), put("bl", 0, 19), put("br", 29, 19)


# --- Tiles ----------------------------------------------------------------------
def cut(c):
    tiles, index, tmap = [], {}, np.zeros((20, 30), int)
    for ty in range(20):
        for tx in range(30):
            t = c.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            k = t.tobytes()
            if k not in index:
                index[k] = len(tiles)
                tiles.append(t.copy())
            tmap[ty, tx] = index[k]
    return tiles, tmap


def write_outputs(c):
    tiles, tmap = cut(c)
    n = len(tiles)
    print(f"region map: {n} unique tiles (the Fly map has room for 256, the dex area 232)")
    assert n <= 232, n
    pal = list(RGB) + [(0, 0, 0)] * (48 - len(RGB))
    full = [(0, 0, 0)] * 256
    for i, col in enumerate(pal):
        full[PAL_BASE + i] = col
    # tiles PNG: 16 tiles wide, 8bpp, indices offset into palette 7
    rows = (n + 15) // 16
    sheet = np.zeros((rows * 8, 128), np.uint8)
    for i, t in enumerate(tiles):
        y, x = (i // 16) * 8, (i % 16) * 8
        sheet[y:y + 8, x:x + 8] = t + PAL_BASE
    # pad the unused cells with tile 0 (sea), so no stray index-0 pixels exist
    for i in range(n, rows * 16):
        y, x = (i // 16) * 8, (i % 16) * 8
        sheet[y:y + 8, x:x + 8] = tiles[0] + PAL_BASE
    for out in [ROOT / "graphics/pokenav/region_map/map.png", ROOT / "graphics/pokedex/region_map.png"]:
        im = Image.fromarray(sheet, "P")
        im.putpalette([v for col in full for v in col])
        im.save(out)
        print(f"wrote {out.relative_to(ROOT)}")
    write_jasc(ROOT / "graphics/pokenav/region_map/map.pal", pal)
    write_jasc(ROOT / "graphics/pokedex/region_map.pal", pal)

    # Fly / wall map: an affine 64x64 byte map; off-screen cells are open sea.
    vals, counts = np.unique(tmap, return_counts=True)
    sea = vals[np.argmax(counts)]
    aff = np.full((64, 64), sea, np.uint8)
    aff[:20, :30] = tmap
    (ROOT / "graphics/pokenav/region_map/map.bin").write_bytes(aff.tobytes())
    print("wrote graphics/pokenav/region_map/map.bin")
    # Dex area: a 32x32 text map of u16 entries
    txt = np.full((32, 32), sea, np.uint16)
    txt[:20, :30] = tmap
    (ROOT / "graphics/pokedex/region_map.bin").write_bytes(txt.astype("<u2").tobytes())
    print("wrote graphics/pokedex/region_map.bin")
    return tiles, tmap


def rgb_of(c):
    return np.array(RGB + [(255, 0, 255)] * (256 - len(RGB)), np.uint8)[c.a]


def preview(c):
    rgb = rgb_of(c)
    save_rgb(IMG / "ui_world_map.png", rgb, 3)
    # The grid: every section's cells outlined, for design/AETHOS_MAP.md
    g = Image.fromarray(rgb).resize((W * 4, H * 4), Image.NEAREST)
    d = ImageDraw.Draw(g)
    for gx in range(28):
        for gy in range(15):
            x, y = cell_px(gx, gy)
            d.rectangle([x * 4, y * 4, x * 4 + 31, y * 4 + 31], outline=(90, 70, 70))
    for sec, name, cells in SECTIONS:
        col = (120, 120, 120) if sec in POSTGAME else ((240, 192, 64) if "ROUTE" not in sec else (112, 168, 224))
        for cell in cells:
            x, y = cell_px(*cell)
            d.rectangle([x * 4 + 1, y * 4 + 1, x * 4 + 30, y * 4 + 30], outline=col, width=2)
        x, y = cell_px(*cells[0])
        d.text((x * 4 + 2, y * 4 + 33 if "ROUTE" in sec else y * 4 - 11), name.title(), fill=col)
    g.save(IMG / "ui_world_map_grid.png")
    print("wrote design/phase1/img/ui_world_map_grid.png")


# --- Section data: one source for the art, the grid and the names -------------
def write_sections():
    """Update region_map_sections.json (names and grid boxes) and regenerate
    region_map_layout.h. New sections are appended, so existing MAPSEC
    values never move."""
    import json
    path = ROOT / "src/data/region_map/region_map_sections.json"
    data = json.loads(path.read_text())
    by_id = {e["id"]: e for e in data["map_sections"]}
    for sec, name, cells in SECTIONS:
        xs, ys = [x for x, _ in cells], [y for _, y in cells]
        entry = {"id": sec, "name": name, "x": min(xs), "y": min(ys),
                 "width": max(xs) - min(xs) + 1, "height": max(ys) - min(ys) + 1}
        if sec in by_id:
            by_id[sec].clear()
            by_id[sec].update(entry)
        else:
            data["map_sections"].append(entry)
    assert len(data["map_sections"]) < 0xFD, "MAPSEC_NONE must stay below the special met locations"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {path.relative_to(ROOT)}: {len(data['map_sections'])} sections")

    grid = [["MAPSEC_NONE"] * 28 for _ in range(15)]
    for sec, _, cells in SECTIONS:
        for (x, y) in cells:
            assert grid[y][x] == "MAPSEC_NONE", (sec, x, y)
            grid[y][x] = sec
    lines = [
        "// Ichor: the Aethos region map's section grid, 28x15 cells. Generated by",
        "// tools/ichor/art/ui_world_map.py from the same table that paints the map;",
        "// edit SECTIONS there and rerun it. design/AETHOS_MAP.md has the plan.",
        "static const mapsec_u8_t sRegionMap_MapSectionLayout[MAP_HEIGHT][MAP_WIDTH] = {",
    ]
    for row in grid:
        lines.append("    {" + ", ".join(row) + "},")
    lines.append("};")
    out = ROOT / "src/data/region_map/region_map_layout.h"
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    canvas, _ = paint()
    write_outputs(canvas)
    write_sections()
    preview(canvas)
