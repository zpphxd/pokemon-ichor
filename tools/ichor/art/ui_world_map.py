#!/usr/bin/env python3
"""Paint the Aethos region map: a black-figure map on terracotta.

The land is reserved clay with an incised ink coast; the sea is black glaze
with wine-purple wave strokes (Homer's wine-dark sea). Land routes are worn
paths that wind cell by cell between the towns, sea routes are gold dashes,
and every town, waypoint and island has its own small glyph. A meander border
runs round the edge, the same key as the dialogue box. The geography, the
route network and the map-section grid are documented in design/AETHOS_MAP.md.

The map is one 240x160 picture, cut into 8x8 tiles:
  - the Fly map and the wall map (src/region_map.c) show it on an affine BG:
    8bpp, at most 256 tiles, no flips, a 64x64 byte tilemap
  - the Pokedex area view shows it on a text BG: 8bpp, 32x32 u16 tilemap,
    at most 232 tiles
Both load the palette at BG palette 7 (colors 112-159), so the PNG indices are
offset by 112 and at most 48 colors are used.

To keep inside the tile budget the coast is drawn by marching squares on a
4-pixel lattice, so a stretch of coast repeats the same few tiles; small
islands are drawn whole inside one tile; roads, lanes and stamps are drawn in
tile-local coordinates, so the same piece is always the same tile.

The grid: section cell (gx, gy) is screen tile (gx + 1, gy + 2), the region
map's MAPCURSOR_X_MIN / MAPCURSOR_Y_MIN.

Writes:
  graphics/pokenav/region_map/map.png, map.bin, map.pal   (Fly and wall map)
  graphics/pokedex/region_map.png, region_map.bin, region_map.pal (dex area)
  src/data/region_map/region_map_sections.json, region_map_layout.h
  include/constants/region_map_sections_ichor.h          (FRLG name aliases)
  design/phase1/img/ui_world_map*.png                      (previews)

Usage: python3 tools/ichor/art/ui_world_map.py
"""
import json

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ui_menus_lib import (ROOT, Canvas, INK, CLAY_DARK, CLAY, CLAY_LIGHT, CLAY_PALE,
                          PARCHMENT, MARBLE, MARBLE_DARK, MARBLE_LIGHT, GOLD, GOLD_DARK,
                          GOLD_PALE, OLIVE, OLIVE_DARK, AEGEAN_LIGHT, save_rgb, write_jasc)

IMG = ROOT / "design/phase1/img"
W, H = 240, 160
PAL_BASE = 112   # BG palette 7, where both screens load the map palette
GRID_W, GRID_H = 28, 15

# --- Palette ---------------------------------------------------------------
COLORS = [
    ("glaze", (40, 24, 32)),        # the sea: black glaze with a wine cast
    ("wine_dk", (72, 32, 56)),      # wave strokes
    ("wine", (104, 48, 72)),        # surf along the coast
    ("wine_lt", (152, 88, 104)),    # foam
    ("ink", INK),                   # coast, roads, glyph outlines
    ("clay_dk", CLAY_DARK),         # incised hatching, mountain shade
    ("clay", CLAY),                 # the land
    ("clay_lt", CLAY_LIGHT),        # lit coast
    ("clay_pale", CLAY_PALE),       # roads, highlights
    ("parch", PARCHMENT),           # snow shade, foam
    ("white", MARBLE_LIGHT),        # added white: temples, snow, clouds
    ("marble", MARBLE),
    ("marble_dk", MARBLE_DARK),
    ("gold", GOLD),                 # pediments, lanes
    ("gold_dk", GOLD_DARK),
    ("gold_pale", GOLD_PALE),
    ("olive", OLIVE),               # olive, laurel and cypress crowns
    ("olive_dk", OLIVE_DARK),
    ("lava", (240, 88, 40)),        # Kaldera's forge
    ("lava_dk", (176, 40, 24)),
    ("pool", AEGEAN_LIGHT),         # lakes, springs and rivers
    ("ghost", (152, 72, 48)),       # unrevealed places on land: a shade under the clay
    ("ghost_sea", (88, 48, 72)),    # unrevealed places at sea
    ("mist", (152, 136, 160)),      # the fog at the chart's edge, where the Oikoumene begins
]
C = {name: i for i, (name, _) in enumerate(COLORS)}
RGB = [rgb for _, rgb in COLORS]
assert len(RGB) <= 48


def cell_px(gx, gy):
    """Top-left pixel of map-section cell (gx, gy)."""
    return (gx + 1) * 8, (gy + 2) * 8


# --- Sections -----------------------------------------------------------------
# kinds: a town has an Asclepeion (a future fly target); a waypoint is a cave,
# a pass, a hamlet or a landmark between towns; a road is a land route; a sea
# route is open water; an isle is an island with no town on it. A crossing is
# the way off this chart onto the Oikoumene's: its id belongs to
# tools/ichor/oikoumene_sections.py, so only its cell is set here.
TOWN, WAY, ROAD, SEA, ISLE, CROSS = "town", "way", "road", "sea", "isle", "cross"


def route(n):
    return f"MAPSEC_AETHOS_ROUTE_{n}", f"ROUTE {n}"


# (MAPSEC, name, kind, cells), in story order. A route's cells run in the
# direction you first walk or sail it.
SECTIONS = [
    # Prologue: Kalliste (Naxos). The slice's three maps.
    ("MAPSEC_ELAIA_VILLAGE", "ELAIA VILLAGE", TOWN, [(23, 9)]),
    ("MAPSEC_KALLISTE_ROUTE_1", "ROUTE 1", ROAD, [(23, 8)]),
    ("MAPSEC_AKTI_TOWN", "AKTI TOWN", TOWN, [(23, 7)]),
    # Act I: the crossing, then the mainland road
    (*route(2), SEA, [(22, 7), (21, 7), (21, 8), (20, 8), (20, 9)]),
    (*route(3), SEA, [(19, 9), (18, 9), (17, 9), (16, 9), (15, 9), (14, 9), (13, 9), (12, 9), (11, 9)]),
    ("MAPSEC_EMPORION_CITY", "EMPORION CITY", TOWN, [(10, 9)]),
    (*route(4), ROAD, [(10, 8), (11, 8)]),
    ("MAPSEC_HECATES_HOLLOW", "HECATE'S HOLLOW", WAY, [(12, 8)]),
    (*route(5), ROAD, [(13, 8), (13, 7)]),
    ("MAPSEC_ELEUSA_VILLAGE", "ELEUSA VILLAGE", TOWN, [(14, 7)]),
    (*route(6), ROAD, [(14, 6)]),
    ("MAPSEC_MT_KITHAIRON", "MT. KITHAIRON", WAY, [(14, 5)]),
    # Act II
    (*route(7), ROAD, [(13, 5), (13, 4)]),
    ("MAPSEC_THYRSA_CITY", "THYRSA CITY", TOWN, [(12, 4)]),
    (*route(8), ROAD, [(11, 4), (10, 4)]),
    ("MAPSEC_LEBADEIA", "LEBADEIA", WAY, [(9, 4)]),
    (*route(9), ROAD, [(9, 5), (8, 5)]),
    ("MAPSEC_KIRRHA", "KIRRHA", WAY, [(7, 5)]),
    (*route(10), SEA, [(7, 6), (6, 6), (5, 6)]),
    ("MAPSEC_AIGION", "AIGION", WAY, [(5, 7)]),
    (*route(11), ROAD, [(5, 8)]),
    ("MAPSEC_STYX_FALLS", "STYX FALLS", WAY, [(5, 9)]),
    (*route(12), ROAD, [(5, 10), (6, 10)]),
    ("MAPSEC_ARKADIA", "ARKADIA", TOWN, [(7, 10), (7, 11)]),
    (*route(13), ROAD, [(7, 9)]),
    ("MAPSEC_NEMEA", "NEMEA", WAY, [(8, 9)]),
    (*route(14), ROAD, [(9, 9)]),
    (*route(15), ROAD, [(15, 7), (16, 7)]),
    ("MAPSEC_DAPHNI", "DAPHNI", WAY, [(17, 7)]),
    (*route(16), ROAD, [(17, 6)]),
    ("MAPSEC_ASTYRA", "ASTYRA", TOWN, [(18, 6), (18, 7)]),
    (*route(17), ROAD, [(18, 5), (19, 5)]),
    ("MAPSEC_MARATHON", "MARATHON", WAY, [(20, 5)]),
    (*route(18), ROAD, [(19, 7)]),
    ("MAPSEC_CAPE_SOUNION", "CAPE SOUNION", WAY, [(19, 8)]),
    ("MAPSEC_EUBOIA", "EUBOIA", ISLE, [(12, 3), (13, 2), (14, 2), (15, 3), (16, 3), (17, 4)]),
    ("MAPSEC_AIGINA", "AIGINA", ISLE, [(14, 10)]),
    (*route(19), SEA, [(23, 10)]),
    ("MAPSEC_KALDERA", "KALDERA", TOWN, [(23, 11)]),
    (*route(20), SEA, [(21, 5), (21, 4), (21, 3), (21, 2), (21, 1), (21, 0)]),
    ("MAPSEC_SKYROS", "SKYROS", ISLE, [(22, 3)]),
    ("MAPSEC_LEMNOS", "LEMNOS", ISLE, [(20, 1)]),
    ("MAPSEC_SAMOTHRAKE", "SAMOTHRAKE", ISLE, [(22, 0)]),
    (*route(21), SEA, [(24, 7), (25, 7), (25, 6), (25, 5), (25, 4), (25, 3)]),
    ("MAPSEC_DELOS", "DELOS", ISLE, [(22, 6)]),
    ("MAPSEC_PAROS", "PAROS", ISLE, [(22, 10)]),
    ("MAPSEC_IKARIA", "IKARIA", ISLE, [(24, 6)]),
    ("MAPSEC_SAMOS", "SAMOS", ISLE, [(26, 7)]),
    ("MAPSEC_CHIOS", "CHIOS", ISLE, [(26, 5)]),
    ("MAPSEC_LESBOS", "LESBOS", ISLE, [(26, 3), (26, 2)]),
    # Act III
    (*route(22), SEA, [(22, 11), (21, 11), (20, 11), (19, 11), (18, 11), (17, 11), (16, 11),
                       (15, 11), (14, 11), (13, 11), (12, 11), (12, 12)]),
    ("MAPSEC_MELOS", "MELOS", ISLE, [(18, 10)]),
    ("MAPSEC_KYTHERA_ISLE", "KYTHERA ISLE", TOWN, [(12, 13)]),
    (*route(23), SEA, [(13, 13), (13, 12), (14, 12), (15, 12), (16, 12), (17, 12), (18, 12),
                       (19, 12), (20, 12), (21, 12)]),
    ("MAPSEC_AMNISOS", "AMNISOS", TOWN, [(21, 13)]),
    ("MAPSEC_BULL_ROAD", "BULL ROAD", ROAD, [(21, 14)]),
    ("MAPSEC_PALACE_OF_MINOS", "PALACE OF MINOS", WAY, [(20, 14)]),
    ("MAPSEC_MT_IDA", "MT. IDA", WAY, [(19, 14), (18, 14)]),
    (*route(24), SEA, [(11, 13)]),
    ("MAPSEC_GYTHEION", "GYTHEION", WAY, [(10, 13)]),
    (*route(25), ROAD, [(10, 12)]),
    ("MAPSEC_LAKONIA", "LAKONIA", TOWN, [(9, 12)]),
    (*route(26), ROAD, [(9, 11)]),
    ("MAPSEC_LAKE_STYMPHALIA", "LAKE STYMPHALIA", WAY, [(9, 10)]),
    (*route(27), ROAD, [(8, 10), (8, 11)]),
    (*route(28), ROAD, [(7, 4)]),
    ("MAPSEC_DELPHOI", "DELPHOI", TOWN, [(7, 3)]),
    # The League
    (*route(29), ROAD, [(7, 2), (8, 2)]),
    ("MAPSEC_THERMOPYLAI", "THERMOPYLAI", WAY, [(9, 2)]),
    (*route(30), ROAD, [(10, 2)]),
    ("MAPSEC_VALE_OF_TEMPE", "VALE OF TEMPE", WAY, [(10, 1)]),
    ("MAPSEC_THE_ASCENT", "THE ASCENT", ROAD, [(9, 1), (9, 0)]),
    ("MAPSEC_MOUNT_OLYMPUS", "MT. OLYMPUS", TOWN, [(8, 0), (7, 0)]),
    # Post-game: hidden on the map until the game is cleared (region_map.c)
    (*route(31), ROAD, [(9, 13)]),
    ("MAPSEC_CAPE_TAINARON", "CAPE TAINARON", TOWN, [(9, 14)]),
    (*route(32), ROAD, [(6, 11), (5, 11), (4, 11)]),
    ("MAPSEC_OLYMPIA", "OLYMPIA", TOWN, [(3, 11)]),
    (*route(33), SEA, [(8, 14), (7, 14), (6, 14), (5, 14), (4, 14), (3, 14), (2, 14), (2, 13),
                       (2, 12), (2, 11), (2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5), (2, 4)]),
    ("MAPSEC_ATLANTIS", "ATLANTIS", TOWN, [(1, 13)]),
    ("MAPSEC_ITHAKA", "ITHAKA", ISLE, [(1, 7)]),
    ("MAPSEC_KERKYRA", "KERKYRA", ISLE, [(1, 4)]),
    (*route(34), SEA, [(24, 11), (25, 11)]),
    ("MAPSEC_RHODOS", "RHODOS", ISLE, [(26, 11)]),
    # The Oikoumene: THE OIKOUMENE, in the fog at the chart's eastern edge, flies
    # you to your last Oikoumene port (design/OIKOUMENE.md section 2). Hidden
    # until you've crossed (region_map.c).
    ("MAPSEC_THE_OIKOUMENE", "THE OIKOUMENE", CROSS, [(27, 5)]),
]
POSTGAME = {"MAPSEC_AETHOS_ROUTE_31", "MAPSEC_CAPE_TAINARON", "MAPSEC_AETHOS_ROUTE_32",
            "MAPSEC_OLYMPIA", "MAPSEC_AETHOS_ROUTE_33", "MAPSEC_ATLANTIS", "MAPSEC_ITHAKA",
            "MAPSEC_KERKYRA", "MAPSEC_AETHOS_ROUTE_34", "MAPSEC_RHODOS"}
BY_ID = {s[0]: s for s in SECTIONS}

# The journeys, as chains of sections: the roads and lanes are painted along
# them, from the last cell of one section to the first cell of the next.
PATHS = [
    ["MAPSEC_ELAIA_VILLAGE", "MAPSEC_KALLISTE_ROUTE_1", "MAPSEC_AKTI_TOWN", route(2)[0],
     route(3)[0], "MAPSEC_EMPORION_CITY", route(4)[0], "MAPSEC_HECATES_HOLLOW", route(5)[0],
     "MAPSEC_ELEUSA_VILLAGE", route(6)[0], "MAPSEC_MT_KITHAIRON", route(7)[0],
     "MAPSEC_THYRSA_CITY", route(8)[0], "MAPSEC_LEBADEIA", route(9)[0], "MAPSEC_KIRRHA",
     route(10)[0], "MAPSEC_AIGION", route(11)[0], "MAPSEC_STYX_FALLS", route(12)[0],
     "MAPSEC_ARKADIA", route(13)[0], "MAPSEC_NEMEA", route(14)[0], "MAPSEC_EMPORION_CITY"],
    ["MAPSEC_ELEUSA_VILLAGE", route(15)[0], "MAPSEC_DAPHNI", route(16)[0], "MAPSEC_ASTYRA",
     route(17)[0], "MAPSEC_MARATHON", route(20)[0]],
    ["MAPSEC_ASTYRA", route(18)[0], "MAPSEC_CAPE_SOUNION"],
    ["MAPSEC_ELAIA_VILLAGE", route(19)[0], "MAPSEC_KALDERA", route(22)[0],
     "MAPSEC_KYTHERA_ISLE", route(23)[0], "MAPSEC_AMNISOS", "MAPSEC_BULL_ROAD",
     "MAPSEC_PALACE_OF_MINOS", "MAPSEC_MT_IDA"],
    ["MAPSEC_AKTI_TOWN", route(21)[0]],
    ["MAPSEC_KYTHERA_ISLE", route(24)[0], "MAPSEC_GYTHEION", route(25)[0], "MAPSEC_LAKONIA",
     route(26)[0], "MAPSEC_LAKE_STYMPHALIA", route(27)[0], "MAPSEC_ARKADIA"],
    ["MAPSEC_KIRRHA", route(28)[0], "MAPSEC_DELPHOI", route(29)[0], "MAPSEC_THERMOPYLAI",
     route(30)[0], "MAPSEC_VALE_OF_TEMPE", "MAPSEC_THE_ASCENT", "MAPSEC_MOUNT_OLYMPUS"],
    ["MAPSEC_LAKONIA", route(31)[0], "MAPSEC_CAPE_TAINARON", route(33)[0]],
    ["MAPSEC_ARKADIA", route(32)[0], "MAPSEC_OLYMPIA"],
    ["MAPSEC_KALDERA", route(34)[0]],
]
DIRS = {(0, -1): "N", (1, 0): "E", (0, 1): "S", (-1, 0): "W"}


def links():
    """Every cell's connected neighbours along the journeys: {cell: set of dirs}."""
    out = {}

    def link(a, b):
        d = (b[0] - a[0], b[1] - a[1])
        assert d in DIRS, (a, b)
        out.setdefault(a, set()).add(DIRS[d])
        out.setdefault(b, set()).add(DIRS[(-d[0], -d[1])])

    for sec, _, kind, cells in SECTIONS:
        if kind in (ROAD, SEA):
            for a, b in zip(cells, cells[1:]):
                link(a, b)
    for chain in PATHS:
        for a, b in zip(chain, chain[1:]):
            ca, cb = BY_ID[a], BY_ID[b]
            ends = [ca[3][-1]] if ca[2] in (ROAD, SEA) else ca[3]
            starts = [cb[3][0]] if cb[2] in (ROAD, SEA) else cb[3]
            pair = [(x, y) for x in ends for y in starts if abs(x[0] - y[0]) + abs(x[1] - y[1]) == 1]
            assert pair, (a, b)
            link(*pair[0])
    return out


# --- Geography (cell units: cell (gx, gy) spans [gx, gx+1] x [gy, gy+1]) -----
# Greece, unfolded to fill the screen: the mainland runs west to east across
# the middle, the Gulf of Korinthos cuts it from the Peloponnese, the Cyclades
# and the islands of the east Aegean fill the right, and Knossa (Crete) runs
# along the bottom. North is up; places keep their real order.
MAINLAND = [
    # the north, beyond the top of the grid
    (1.6, -1.7), (11.2, -1.7),
    # Thessaly's coast: Pieria, Ossa, Pelion
    (11.3, -0.4), (10.95, 0.5), (11.35, 1.3), (11.05, 2.2),
    # the Malian gulf at Thermopylai
    (10.55, 2.75), (10.1, 2.85), (9.85, 3.25), (10.0, 3.75),
    # Boeotia's north shore, facing Euboia across the Euripus
    (10.9, 4.15), (11.8, 4.2), (12.6, 4.15), (13.4, 4.2), (13.85, 4.3), (13.85, 4.9),
    (14.3, 5.15), (15.2, 5.2), (16.1, 5.1), (17.0, 5.15), (17.9, 5.1), (18.8, 5.2),
    (19.7, 5.1), (20.4, 4.85), (20.95, 5.05),
    # east Attica, Marathon to Sounion
    (21.05, 5.8), (20.65, 6.3), (20.4, 6.9), (20.15, 7.6), (20.2, 8.25), (19.9, 8.85),
    (19.45, 9.15), (19.1, 8.6),
    # Attica's south shore: Phaleron, Piraeus, the bay of Eleusis
    (18.6, 8.2), (17.9, 8.15), (17.1, 8.25), (16.3, 8.15), (15.5, 8.2), (14.7, 8.15),
    (14.1, 8.25),
    # the Megarid and the Skironian cliffs, down to the Isthmus
    (13.95, 8.9), (13.2, 9.1), (12.4, 9.15), (11.6, 9.1), (11.15, 9.2),
    # the Argolid and Cape Malea
    (11.2, 9.95), (11.9, 10.15), (12.15, 10.8), (11.95, 11.55), (12.1, 12.3), (11.65, 12.95),
    (11.15, 12.85), (10.9, 13.3), (11.05, 13.9),
    # the Lakonian gulf, the Mani and Tainaron
    (10.4, 14.15), (10.15, 14.6), (9.9, 15.35), (9.35, 15.3), (9.05, 14.4), (8.9, 13.35),
    # the Messenian gulf, Messenia and the west coast
    (8.45, 13.15), (8.1, 13.4), (7.95, 13.95), (7.1, 14.15), (6.2, 13.9), (5.3, 14.15),
    (4.4, 13.9), (3.55, 14.05), (3.1, 13.5), (2.9, 12.7), (3.15, 11.9), (2.85, 11.1),
    (3.1, 10.2), (2.85, 9.3), (3.15, 8.45), (2.9, 7.6), (3.3, 7.3),
    # the gulf of Korinthos: the Peloponnese's north shore, east to the gulf's tip
    (4.2, 7.2), (5.1, 7.3), (6.0, 7.15), (7.0, 7.3), (8.0, 7.15), (8.95, 7.3),
    (9.1, 7.9), (8.9, 8.6), (9.3, 9.15), (9.9, 9.05),
    # ... and back along the north shore, past Kirrha
    (10.15, 8.3), (9.95, 7.5), (10.1, 6.65), (9.85, 5.95), (9.1, 5.75), (8.2, 5.85),
    (7.3, 5.7), (6.4, 5.85), (5.5, 5.7), (4.6, 5.85), (3.7, 5.7), (3.0, 5.85),
    # the Ionian coast, north to Epirus
    (2.85, 5.35), (3.15, 4.5), (2.85, 3.6), (3.1, 2.7), (2.75, 1.8), (2.65, 0.8),
    (2.3, -0.3),
]
EUBOIA = [(12.15, 3.75), (12.4, 3.05), (13.0, 2.4), (13.6, 1.85), (14.6, 1.85), (15.3, 2.35),
          (16.1, 2.65), (16.85, 2.9), (17.5, 3.4), (18.05, 4.0), (18.2, 4.75), (17.65, 4.8),
          (17.05, 4.25), (16.3, 3.85), (15.4, 3.8), (14.6, 3.15), (14.0, 2.9), (13.4, 3.15),
          (12.85, 3.8)]
KALLISTE = [(23.15, 6.65), (23.9, 6.8), (24.2, 7.5), (24.05, 8.35), (24.2, 9.2), (23.85, 10.15),
            (23.1, 10.1), (22.85, 9.3), (23.05, 8.5), (22.8, 7.7), (22.95, 6.95)]
LESBOS = [(25.95, 1.85), (26.85, 1.9), (27.15, 2.6), (26.85, 3.45), (26.25, 4.15), (26.05, 3.3),
          (26.15, 2.55)]
CRETE = [(13.85, 13.45), (14.6, 13.2), (15.7, 13.3), (16.8, 13.15), (17.9, 13.3), (19.0, 13.15),
         (20.1, 13.3), (21.2, 13.15), (22.3, 13.3), (23.4, 13.15), (24.5, 13.3), (25.6, 13.35),
         (26.15, 13.75), (25.7, 14.35), (24.6, 14.65), (23.5, 14.95), (22.4, 15.15), (21.3, 15.05),
         (20.2, 15.25), (19.1, 15.05), (18.0, 15.15), (16.9, 14.95), (15.8, 14.85), (14.7, 14.65),
         (14.0, 14.15)]
LAND_POLYGONS = [MAINLAND, EUBOIA, KALLISTE, LESBOS, CRETE]

# Small islands, drawn whole inside their own cell so each costs one tile.
ISLETS = {
    (14, 10): ["        ", "   ##   ", "  ####  ", " #####  ", " ###### ", "  ##    ", "        ", "        "],   # Aigina
    (18, 10): ["        ", " ##  ## ", " ##  ## ", " ###### ", "  ####  ", "        ", "        ", "        "],   # Melos, round its bay
    (22, 6): ["        ", "        ", "   ##   ", "  ###   ", "   #    ", "  #     ", "        ", "        "],    # Delos and Rheneia
    (22, 10): ["        ", "  ###   ", " #####  ", " ###### ", "  ####  ", "   ##   ", "        ", "        "],   # Paros
    (24, 6): ["        ", "        ", " ###    ", " ###### ", "   #### ", "        ", "        ", "        "],    # Ikaria, long and thin
    (26, 7): ["        ", "  ##    ", " ###### ", "  ##### ", "    ##  ", "        ", "        ", "        "],    # Samos
    (26, 5): ["        ", "   ##   ", "  ###   ", "  ####  ", "  ###   ", "   ##   ", "        ", "        "],    # Chios
    (22, 3): ["        ", "  ##    ", " ####   ", "  ####  ", "   #### ", "    ##  ", "        ", "        "],    # Skyros
    (20, 1): ["        ", " ## ### ", " ###### ", "  ####  ", "  ##    ", "        ", "        ", "        "],    # Lemnos
    (22, 0): ["        ", "  ####  ", " ###### ", " ###### ", "  ####  ", "        ", "        ", "        "],    # Samothrake
    (12, 13): ["        ", "  ####  ", " ###### ", " ###### ", "  ####  ", "   ##   ", "        ", "        "],   # Kythera
    (23, 11): ["        ", "  ####  ", " ##  ## ", " #   ## ", "     ## ", " ##  ## ", "  ####  ", "        "],   # Thera's ring, open to the west
}
# Post-game islands: painted faint, a shade under the sea, until they open.
GHOST_ISLETS = {
    (1, 4): ["  ##    ", " ####   ", "  ###   ", "   ##   ", "   ###  ", "    ##  ", "        ", "        "],     # Kerkyra
    (1, 7): ["   ##   ", "  ###   ", "   #    ", "   ##   ", "  ###   ", "        ", "        ", "        "],     # Ithaka
    (26, 11): ["     ## ", "    ### ", "   #### ", "  ####  ", " ###    ", " ##     ", "        ", "        "],   # Rhodos
}


def inside(poly, x, y):
    """Point in polygon (even-odd)."""
    c = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            xc = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            if x < xc:
                c = not c
    return c


def land_mask():
    """The land, pixel by pixel. The polygons are sampled on a 4-pixel lattice
    and joined up by marching squares, so a coast is made of a few repeating
    shapes; the islets are pasted whole."""
    lx, ly = W // 4 + 1, H // 4 + 1
    lat = np.zeros((ly, lx), float)
    for j in range(ly):
        for i in range(lx):
            cx, cy = i / 2 - 1, j / 2 - 2      # lattice point in cell units
            if any(inside(p, cx, cy) for p in LAND_POLYGONS):
                lat[j, i] = 1
    m = np.zeros((H, W), bool)
    for y in range(H):
        j, v = y // 4, ((y % 4) + 0.5) / 4
        for x in range(W):
            i, u = x // 4, ((x % 4) + 0.5) / 4
            f = (lat[j, i] * (1 - u) * (1 - v) + lat[j, i + 1] * u * (1 - v)
                 + lat[j + 1, i] * (1 - u) * v + lat[j + 1, i + 1] * u * v)
            m[y, x] = f > 0.5
    for (gx, gy), rows in ISLETS.items():
        x0, y0 = cell_px(gx, gy)
        for r, row in enumerate(rows):
            for k, ch in enumerate(row):
                if ch == "#":
                    m[y0 + r, x0 + k] = True
    return m


# --- Glyphs ---------------------------------------------------------------
# Keys: # ink, d clay_dk, c clay, l clay_lt, p clay_pale, w white, m marble,
# M marble_dk, g gold, G gold_dk, y gold_pale, o olive, O olive_dk, r lava,
# R lava_dk, b pool, h ghost, s ghost_sea, ~ wine, ' parch, k glaze, v wine_lt;
# space = leave.
KEY = {"#": "ink", "d": "clay_dk", "c": "clay", "l": "clay_lt", "p": "clay_pale",
       "w": "white", "m": "marble", "M": "marble_dk", "g": "gold", "G": "gold_dk",
       "y": "gold_pale", "o": "olive", "O": "olive_dk", "r": "lava", "R": "lava_dk",
       "b": "pool", "h": "ghost", "s": "ghost_sea", "~": "wine", "'": "parch",
       "k": "glaze", "v": "wine_lt", "e": "mist"}

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
SOUNION = [         # Poseidon's temple on the cape, all white
    "   ##   ",
    "  #ww#  ",
    " #wmmw# ",
    "########",
    " w w w  ",
    " w w w  ",
    "########",
    "        ",
]
PARTHENON = [       # Astyra, upper cell: the Parthenon on the Akropolis rock
    "        ",
    "   ##   ",
    "  #gg#  ",
    " ###### ",
    " w w w  ",
    "########",
    "#dddddd#",
    "#dcddcdd",
]
CITY = [            # Astyra, lower cell: the city at the rock's foot
    "#dddddd#",
    " ###### ",
    "  #dd# #",
    " #dddd#d",
    " #w#w##w",
    "#dd#dddd",
    "#w##w#w#",
    "########",
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
MOON_GROVE = [      # Arkadia: Artemis's crescent over the cypresses
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
LABYRINTH = [       # the Palace of Minos: the Labyrinth, as on Knossian coins
    "########",
    "#pppppp#",
    "#p####p#",
    "#p#pp#p#",
    "#p#p##p#",
    "#p#pppp#",
    "#p######",
    "########",
]
BEEHIVE = [         # Amnisos: a skep, for the hives on every roof
    "   ##   ",
    "  #gg#  ",
    " #gGGg# ",
    " #gggg# ",
    "#gGGGGg#",
    "#gggggg#",
    "#gg##gg#",
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
HARBOR = [          # Akti: Hestia's temple over the harbor
    "   ##   ",
    "  #gg#  ",
    " #gGGg# ",
    "########",
    " w w w  ",
    " w w w  ",
    "########",
    "        ",
]
HOLLOW = [          # Hecate's Hollow: a cave mouth, and her torch
    "    g   ",
    "   gy   ",
    "  ####  ",
    " #dddd# ",
    "#dd##dd#",
    "#d####d#",
    "#d####d#",
    "########",
]
KITHAIRON = [       # Mt. Kithairon: the Bacchae's mountain, wreathed in ivy
    "   #    ",
    "  #l#   ",
    " #lcd#  ",
    " oOcdo# ",
    "#lOooOd#",
    "#lccddd#",
    "########",
    "        ",
]
HAMLET = [          # Lebadeia: a hamlet at the oracle cave of Trophonios
    "        ",
    "   ##   ",
    "  #dd#  ",
    " #dddd# ",
    " #wwww# ",
    " #w##w##",
    " ####### ",
    "        ",
]
PORT = [            # Kirrha, Aigion, Gytheion: a harbor hamlet and its boat
    "  ##    ",
    " #dd#   ",
    "#dddd#  ",
    "#w##w#  ",
    "######  ",
    "    #   ",
    "  #dddd#",
    "   #### ",
]
FALLS = [           # Styx Falls: the black water the gods swore by
    "########",
    "#dd##dd#",
    "#d#kk#d#",
    "#d#kk#d#",
    "#d#kk#d#",
    "#d#kk#d#",
    "##kkkk##",
    " kkkkkk ",
]
COLUMNS = [         # Nemea: the standing columns of Zeus's temple
    "        ",
    "####### ",
    " w w w  ",
    " w w w  ",
    " w w w  ",
    " w w w  ",
    "####### ",
    "        ",
]
LAUREL = [          # Daphni: Apollo's laurel grove on the road of the Mysteries
    "  oo    ",
    " oyoo oo",
    " ooOooyo",
    "  #oo oo",
    "  #  ## ",
    "  #   # ",
    "        ",
    "        ",
]
MOUND = [           # Marathon: the burial mound, and a spear
    "     #  ",
    "     #  ",
    "   g #  ",
    "  ####  ",
    " #dddd# ",
    "#dddddd#",
    "########",
    "        ",
]
LAKE = [            # Lake Stymphalia: reeds, still water and the birds
    " #   #  ",
    "# # # # ",
    "        ",
    "  bbbb  ",
    " bbbbbb ",
    "obbbbbbo",
    " obbbbo ",
    "  oooo  ",
]
TEMPE = [           # the Vale of Tempe: Daphne's laurel by the river
    "  oo    ",
    " oyooo  ",
    " ooOoo  ",
    "   #    ",
    "bb #  bb",
    " bbbbbb ",
    "  bbbb  ",
    "        ",
]
GATES = [           # Thermopylai: the hot gates, steam from the springs
    " w  w   ",
    "  w  w  ",
    "########",
    "#d#  #d#",
    "#d#  #d#",
    "#d#  #d#",
    "##    ##",
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
SNOW_PEAK = [       # Ida, snow on its summit
    "   #    ",
    "  #w#   ",
    "  #w'#  ",
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
OLIVES = [          # groves
    "        ",
    " oo     ",
    "oOoo    ",
    " ##  oo ",
    "    oOoo",
    "     ## ",
    "        ",
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

EDGE_FOG = [         # the fog bank at the eastern edge, and a sail going into it
    "   eeeee",
    " eee    ",
    "    eeee",
    "  eee   ",
    "eee  eee",
    "   ee   ",
    " eeee   ",
    "     eee",
    "   #    ",          # (27, 5): THE OIKOUMENE
    "  #w  ee",
    " ee#ww  ",
    "  #www  ",
    "  #w'w  ",
    " GgggG  ",
    "  GGG ee",
    "eee     ",
    "   eeee ",
    " ee     ",
    "    eee ",
    "eeee    ",
    "  e   ee",
    "     e  ",
    " ee     ",
    "        ",
]

# Which glyph marks each place (towns, waypoints and the post-game's ghosts)
GLYPHS = {
    "MAPSEC_ELAIA_VILLAGE": [OLIVE_TREE],
    "MAPSEC_AKTI_TOWN": [HARBOR],
    "MAPSEC_EMPORION_CITY": [TEMPLE],
    "MAPSEC_HECATES_HOLLOW": [HOLLOW],
    "MAPSEC_ELEUSA_VILLAGE": [WHEAT],
    "MAPSEC_MT_KITHAIRON": [KITHAIRON],
    "MAPSEC_THYRSA_CITY": [THEATER],
    "MAPSEC_LEBADEIA": [HAMLET],
    "MAPSEC_KIRRHA": [PORT],
    "MAPSEC_AIGION": [PORT],
    "MAPSEC_STYX_FALLS": [FALLS],
    "MAPSEC_ARKADIA": [MOON_GROVE, CYPRESS],
    "MAPSEC_NEMEA": [COLUMNS],
    "MAPSEC_DAPHNI": [LAUREL],
    "MAPSEC_ASTYRA": [PARTHENON, CITY],
    "MAPSEC_MARATHON": [MOUND],
    "MAPSEC_CAPE_SOUNION": [SOUNION],
    "MAPSEC_KYTHERA_ISLE": [SHELL],
    "MAPSEC_AMNISOS": [BEEHIVE],
    "MAPSEC_PALACE_OF_MINOS": [LABYRINTH],
    "MAPSEC_MT_IDA": [SNOW_PEAK, MOUNTAIN],
    "MAPSEC_GYTHEION": [PORT],
    "MAPSEC_LAKONIA": [SHIELD],
    "MAPSEC_LAKE_STYMPHALIA": [LAKE],
    "MAPSEC_DELPHOI": [OMPHALOS],
    "MAPSEC_THERMOPYLAI": [GATES],
    "MAPSEC_VALE_OF_TEMPE": [TEMPE],
    "MAPSEC_CAPE_TAINARON": [CAVE_GHOST],
    "MAPSEC_OLYMPIA": [STADIUM_GHOST],
    "MAPSEC_ATLANTIS": [ATLANTIS_GHOST],
}
# The land between the places: ranges, forests and fields on whole cells.
LANDSCAPE = [
    (MOUNTAIN, [(4, 1), (5, 3), (4, 4), (6, 1), (3, 2)]),      # the Pindos
    (SMALL_PEAK, [(5, 1), (6, 4), (4, 0)]),
    (MOUNTAIN, [(6, 3), (8, 3)]),                              # Parnassos, round Delphoi
    (SMALL_PEAK, [(10, 5)]),                                   # Helikon
    (VINES, [(11, 5), (12, 5)]),                               # Thyrsa's vineyards
    (SMALL_PEAK, [(16, 5), (11, 7)]),                          # Parnes; Geraneia, over the Hollow
    (SMALL_PEAK, [(10, 0)]),                                   # Ossa
    (MOUNTAIN, [(7, 8), (4, 9)]),                              # Kyllene; Erymanthos
    (SMALL_PEAK, [(6, 8), (4, 12), (11, 11)]),                 # Aroania; Lykaion; Parnon
    (CYPRESS, [(6, 9), (4, 10), (3, 9)]),                      # Arkadia's forests
    (MOUNTAIN, [(8, 12)]),                                     # Taygetos
    (OLIVES, [(5, 12), (6, 12), (6, 13)]),                     # Messenia's groves
    (SMALL_PEAK, [(15, 14), (23, 14), (17, 14)]),              # the White Mountains; Dikte
    (OLIVES, [(16, 13), (22, 13)]),                            # Knossa's terraces
]


def stamp(c, glyph, x, y, under=None):
    for j, row in enumerate(glyph):
        for i, ch in enumerate(row):
            if ch != " ":
                c.px(x + i, y + j, C[KEY[ch]])


def olympus(c, px, py):
    """The mountain of the gods: a lit west face, a shaded east face, snow on
    the summit, a cloud bank about its waist and a gold glint, the Pantheon,
    at the very top. (px, py) is the peak."""
    h = 17
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
    for (cx, cy, rx) in [(px - 8, py + 9, 5), (px + 8, py + 10, 6), (px - 2, py + 11, 4),
                         (px + 3, py + 8, 4)]:
        for x in range(cx - rx, cx + rx + 1):
            c.px(x, cy, C["white"])
            if abs(x - cx) < rx - 1:
                c.px(x, cy - 1, C["white"])
            if abs(x - cx) < rx:
                c.px(x, cy + 1, C["marble"])
    c.px(px, py + 1, C["gold"])
    c.px(px, py, C["gold_pale"])


# --- Painting -----------------------------------------------------------------
def coast(c, land, fill, edge, lit, surf):
    """Clay inside, an incised ink line on the coast, the top-left lit, and a
    line of surf outside."""
    for y in range(H):
        for x in range(W):
            if not land[y, x]:
                continue
            n = [land[y + dy, x + dx] if 0 <= y + dy < H and 0 <= x + dx < W else True
                 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if not all(n):
                c.px(x, y, C[edge])
            elif lit and ((x > 1 and not land[y, x - 2]) or (y > 1 and not land[y - 2, x])):
                c.px(x, y, C[lit])
            else:
                c.px(x, y, C[fill])
    if surf:
        for y in range(H):
            for x in range(W):
                if land[y, x]:
                    continue
                if any(0 <= y + dy < H and 0 <= x + dx < W and land[y + dy, x + dx]
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    c.px(x, y, C[surf])


def paint():
    land = land_mask()
    c = Canvas(W, H, C["glaze"])
    coast(c, land, "clay", "ink", "clay_lt", "wine")

    # the post-game's islands, a shade under the sea
    ghost = np.zeros((H, W), bool)
    for (gx, gy), rows in GHOST_ISLETS.items():
        x0, y0 = cell_px(gx, gy)
        for r, row in enumerate(rows):
            for k, ch in enumerate(row):
                if ch == "#":
                    ghost[y0 + r, x0 + k] = True
    for y in range(H):
        for x in range(W):
            if ghost[y, x]:
                c.px(x, y, C["ghost_sea"])

    for glyph, cells in LANDSCAPE:
        for (gx, gy) in cells:
            stamp(c, glyph, *cell_px(gx, gy))
    olympus(c, 68, 9)

    # Roads and lanes, centre to centre, in tile-local coordinates so every
    # straight piece is the same tile.
    kind_at = {}
    for sec, _, kind, cells in SECTIONS:
        for cell in cells:
            kind_at[cell] = (sec, kind)
    lk = links()
    for cell, dirs in lk.items():
        sec, kind = kind_at[cell]
        if kind not in (ROAD, SEA):
            continue
        x0, y0 = cell_px(*cell)
        post = sec in POSTGAME
        segs = []
        for d in dirs:
            if d == "N":
                segs.append([(3, j) for j in range(0, 5)])
            elif d == "S":
                segs.append([(3, j) for j in range(3, 8)])
            elif d == "W":
                segs.append([(i, 3) for i in range(0, 5)])
            elif d == "E":
                segs.append([(i, 3) for i in range(3, 8)])
        pts = {p for s in segs for p in s}
        for (i, j) in sorted(pts):
            x, y = x0 + i, y0 + j
            if kind == ROAD:
                # a worn path two pixels wide, its lower and right edge in shadow
                for (dx, dy, col) in ((0, 0, "clay_pale"), (1, 0, "clay_pale"), (0, 1, "clay_pale"),
                                      (1, 1, "clay_pale")):
                    if land[y + dy, x + dx]:
                        c.px(x + dx, y + dy, C["ghost" if post else col])
            else:
                # a trireme lane: gold dashes, two on and two off
                if not land[y, x] and ((i + j) % 4) < 2:
                    c.px(x, y, C["ghost_sea" if post else "gold_dk"])

    # Place glyphs, drawn last so they sit on top
    for sec, glyphs in GLYPHS.items():
        cells = BY_ID[sec][3]
        for cell, glyph in zip(cells, glyphs * len(cells)):
            stamp(c, glyph, *cell_px(*cell))
    # Kaldera's forge burns in the caldera; Kythera's shell is the island itself
    kx, ky = cell_px(23, 11)
    for (x, y, col) in [(kx + 3, ky + 3, "lava"), (kx + 4, ky + 3, "lava_dk"),
                        (kx + 3, ky + 4, "lava_dk"), (kx + 2, ky + 4, "lava")]:
        c.px(x, y, C[col])
    for (x, y, flip) in [(136, 8, False), (216, 88, True)]:  # dolphins in the empty sea
        stamp(c, [r[::-1] for r in DOLPHIN] if flip else DOLPHIN, x, y)
    stamp(c, EDGE_FOG, *cell_px(27, 4))    # THE OIKOUMENE, past the fog

    # The sea: wine strokes on a 16x16 repeat, only on open water, so open sea
    # costs four tiles and every coast tile stays clean.
    for ty in range(20):
        for tx in range(30):
            t = c.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            if not (t == C["glaze"]).all():
                continue
            for j in range(8):
                for i in range(8):
                    x, y = tx * 8 + i, ty * 8 + j
                    u, v = x % 16, y % 16
                    if ((v == 3 and 2 <= u <= 5) or (v == 2 and u in (6, 7)) or (v == 4 and u == 1)
                            or (v == 11 and 10 <= u <= 13) or (v == 10 and u in (14, 15))
                            or (v == 12 and u == 9)):
                        c.px(x, y, C["wine_dk"])

    border(c)
    return c, land


def check(land):
    """Every land section stands on land and every sea route on water."""
    bad = []
    for sec, _, kind, cells in SECTIONS:
        for (gx, gy) in cells:
            x, y = cell_px(gx, gy)
            on_land = land[y + 4, x + 4] or land[y + 3, x + 3]
            if kind == SEA and on_land:
                bad.append((sec, (gx, gy), "sea route on land"))
            if kind in (ROAD, TOWN, WAY, ISLE) and not on_land \
                    and sec not in ("MAPSEC_ATLANTIS", "MAPSEC_KALDERA") and (gx, gy) not in GHOST_ISLETS:
                bad.append((sec, (gx, gy), "on water"))
    for b in bad:
        print("  !", *b)
    assert not bad


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
    # tiles PNG: 16 tiles wide, 8bpp, indices offset into palette 7. The sheet
    # is always 256 cells, so region_map.c's "-num_tiles 233" and "232" always
    # fit; the unused cells are blank (index 0), which gbagfx expects past the
    # tiles it keeps.
    sheet = np.zeros((16 * 8, 128), np.uint8)
    for i, t in enumerate(tiles):
        y, x = (i // 16) * 8, (i % 16) * 8
        sheet[y:y + 8, x:x + 8] = t + PAL_BASE
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


# --- Previews -------------------------------------------------------------------
KIND_COLOR = {TOWN: (240, 192, 64), WAY: (120, 208, 120), ROAD: (112, 168, 224),
              SEA: (176, 136, 232), ISLE: (232, 232, 232), CROSS: (232, 120, 160)}
POST_COLOR = (150, 150, 150)


CODES = {
    "ELAIA_VILLAGE": "Ela", "AKTI_TOWN": "Akt", "EMPORION_CITY": "Emp", "HECATES_HOLLOW": "Hec",
    "ELEUSA_VILLAGE": "Ele", "MT_KITHAIRON": "Kit", "THYRSA_CITY": "Thy", "LEBADEIA": "Leb",
    "KIRRHA": "Kir", "AIGION": "Aig", "STYX_FALLS": "Styx", "ARKADIA": "Ark", "NEMEA": "Nem",
    "DAPHNI": "Dap", "ASTYRA": "Ast", "MARATHON": "Mar", "CAPE_SOUNION": "Sou", "EUBOIA": "Eub",
    "AIGINA": "Agn", "KALDERA": "Kal", "SKYROS": "Sky", "LEMNOS": "Lem", "SAMOTHRAKE": "Smt",
    "DELOS": "Del", "PAROS": "Par", "IKARIA": "Ika", "SAMOS": "Sam", "CHIOS": "Chi",
    "LESBOS": "Les", "MELOS": "Mel", "KYTHERA_ISLE": "Kyt", "AMNISOS": "Amn", "BULL_ROAD": "Bull",
    "PALACE_OF_MINOS": "Pal", "MT_IDA": "Ida", "GYTHEION": "Gyt", "LAKONIA": "Lak",
    "LAKE_STYMPHALIA": "Stm", "DELPHOI": "Dlp", "THERMOPYLAI": "Thm", "VALE_OF_TEMPE": "Tem",
    "THE_ASCENT": "Asc", "MOUNT_OLYMPUS": "Olym", "CAPE_TAINARON": "Tai", "OLYMPIA": "Olpa",
    "ATLANTIS": "Atl", "ITHAKA": "Ith", "KERKYRA": "Ker", "RHODOS": "Rho",
    "THE_OIKOUMENE": "Oik",
}


def short(sec, name):
    if name.startswith("ROUTE "):
        return name[6:]
    return CODES[sec[7:]]


def title(name):
    small = {"OF"}
    return " ".join(w.lower() if w in small else w.capitalize() for w in name.split())


def preview(c):
    rgb = rgb_of(c)
    save_rgb(IMG / "ui_world_map.png", rgb, 3)
    # The labelled grid, for design/AETHOS_MAP.md: every section's cells
    # outlined by kind, its code in the cell, and a key down the right.
    S = 5
    g = Image.fromarray(rgb).resize((W * S, H * S), Image.NEAREST)
    pane = Image.new("RGB", (W * S + 430, H * S), (24, 18, 22))
    pane.paste(g, (0, 0))
    d = ImageDraw.Draw(pane)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)
        small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 12)
    except OSError:
        font = small = ImageFont.load_default()
    for gx in range(GRID_W):
        for gy in range(GRID_H):
            x, y = cell_px(gx, gy)
            d.rectangle([x * S, y * S, x * S + 8 * S - 1, y * S + 8 * S - 1], outline=(70, 56, 56))
    for sec, name, kind, cells in SECTIONS:
        col = POST_COLOR if sec in POSTGAME else KIND_COLOR[kind]
        label = short(sec, name)
        for cell in cells:
            x, y = cell_px(*cell)
            d.rectangle([x * S + 1, y * S + 1, x * S + 8 * S - 2, y * S + 8 * S - 2], outline=col, width=2)
            tw = d.textlength(label, font=font)
            bx, by = x * S + (8 * S - tw) / 2, y * S + 8 * S - 17
            d.rectangle([bx - 2, by - 1, bx + tw + 1, by + 14], fill=(16, 12, 14))
            d.text((bx, by), label, fill=col, font=font)
    # the key
    x0, y = W * S + 12, 10
    d.text((x0, y), "Towns, waypoints and islands", fill=(240, 230, 210), font=font)
    y += 20
    for sec, name, kind, cells in SECTIONS:
        if kind in (ROAD, SEA) and sec not in ("MAPSEC_THE_ASCENT", "MAPSEC_BULL_ROAD"):
            continue
        col = POST_COLOR if sec in POSTGAME else KIND_COLOR[kind]
        d.text((x0, y), f"{short(sec, name):>4}", fill=col, font=font)
        d.text((x0 + 44, y), title(name) + ("  (post-game)" if sec in POSTGAME else ""),
               fill=(220, 210, 196), font=small)
        y += 15
        if y > H * S - 60:
            x0, y = x0 + 215, 30
    legend = [(TOWN, "town"), (WAY, "waypoint"), (ROAD, "land route"), (SEA, "sea route"),
              (ISLE, "island")]
    lx = W * S + 12
    ly = H * S - 40
    for k, label in legend:
        d.rectangle([lx, ly, lx + 12, ly + 12], outline=KIND_COLOR[k], width=2)
        d.text((lx + 16, ly - 1), label, fill=(220, 210, 196), font=small)
        lx += 80
    d.rectangle([W * S + 12, ly + 18, W * S + 24, ly + 30], outline=POST_COLOR, width=2)
    d.text((W * S + 28, ly + 17), "post-game, hidden until the game is cleared", fill=(220, 210, 196), font=small)
    pane.save(IMG / "ui_world_map_grid.png")
    print("wrote design/phase1/img/ui_world_map_grid.png")


# --- Section data: one source for the art, the grid and the names -------------
APPENDED_START = 212      # the first section after Kalliste's three
KANTO_FIRST, KANTO_LAST = 89, 191   # FRLG-only IDs, re-used for Aethos (design/AETHOS_MAP.md)
ALIASES = ROOT / "include/constants/region_map_sections_ichor.h"
FIXED = {"MAPSEC_ELAIA_VILLAGE", "MAPSEC_KALLISTE_ROUTE_1", "MAPSEC_AKTI_TOWN"}


def write_sections():
    """Rewrite region_map_sections.json, the FRLG alias header and
    region_map_layout.h from SECTIONS.

    Towns, waypoints and the post-game's places take the IDs after Kalliste's
    three (212 on), so the map-name pop-up can give each its own theme.
    Routes and islands take IDs from the Kanto block (89 to 191), which only an
    FRLG build uses; its old names stay defined as aliases, so upstream code
    that names them still compiles. MAPSEC_NONE must stay below 0xFD."""
    path = ROOT / "src/data/region_map/region_map_sections.json"
    data = json.loads(path.read_text())
    secs = data["map_sections"]

    # The FRLG name of every Kanto slot: the alias header remembers the ones
    # already re-keyed; the rest still carry their own.
    old = {}
    if ALIASES.exists():
        for line in ALIASES.read_text().splitlines():
            if line.startswith("#define MAPSEC_"):
                _, frlg, ichor = line.split()
                old[ichor] = frlg
    frlg_of = {i: old.get(secs[i]["id"], secs[i]["id"]) for i in range(KANTO_FIRST, KANTO_LAST + 1)}
    if not ALIASES.exists():
        upstream = {e["id"] for e in secs[KANTO_FIRST:KANTO_LAST + 1]}
        assert "MAPSEC_VIRIDIAN_CITY" in upstream, "the Kanto block has moved: check KANTO_FIRST"

    def entry(sec, name, cells):
        xs, ys = [x for x, _ in cells], [y for _, y in cells]
        return {"id": sec, "name": name, "x": min(xs), "y": min(ys),
                "width": max(xs) - min(xs) + 1, "height": max(ys) - min(ys) + 1}

    def upstream_entry(i):
        return {"id": frlg_of[i], "name": frlg_of[i][7:].replace("_", " ")}

    # restore every Kanto slot to its FRLG name first, then hand them out again
    kanto = [s for s in SECTIONS if s[2] in (ROAD, SEA, ISLE) and s[0] not in FIXED]
    places = [s for s in SECTIONS if s[2] not in (ROAD, SEA, ISLE, CROSS) and s[0] not in FIXED]
    assert len(kanto) <= KANTO_LAST - KANTO_FIRST + 1
    aliases = []
    for k, i in enumerate(range(KANTO_FIRST, KANTO_LAST + 1)):
        if k < len(kanto):
            sec, name, _, cells = kanto[k]
            secs[i] = entry(sec, name, cells)
            aliases.append((frlg_of[i], sec))
        elif secs[i]["id"] != frlg_of[i]:
            secs[i] = upstream_entry(i)
    for s in FIXED:
        i = next(k for k, e in enumerate(secs) if e["id"] == s)
        assert i < APPENDED_START
        secs[i] = entry(s, BY_ID[s][1], BY_ID[s][3])
    for sec, name, kind, cells in SECTIONS:
        if kind == CROSS:      # its id is the Oikoumene script's; just place it
            i = next(k for k, e in enumerate(secs) if e["id"] == sec)
            secs[i] = entry(sec, secs[i].get("name", name), cells)
    del secs[APPENDED_START:]
    for sec, name, _, cells in places:
        secs.append(entry(sec, name, cells))
    assert len(secs) < 0xFD, "MAPSEC_NONE must stay below the special met locations"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {path.relative_to(ROOT)}: {len(secs)} sections, "
          f"{len(kanto)} in the Kanto block, {len(places)} after Kalliste")

    lines = [
        "// Ichor: Aethos's routes and islands use the section IDs of the Kanto block,",
        "// which only an FRLG build needs (design/AETHOS_MAP.md). The Kanto names stay",
        "// defined as aliases so upstream code that names them still compiles; in this",
        "// build they mean the Aethos sections. Generated by tools/ichor/art/ui_world_map.py.",
        "#ifndef GUARD_CONSTANTS_REGION_MAP_SECTIONS_ICHOR_H",
        "#define GUARD_CONSTANTS_REGION_MAP_SECTIONS_ICHOR_H",
        "",
    ] + [f"#define {frlg} {ichor}" for frlg, ichor in aliases] + ["", "#endif", ""]
    ALIASES.write_text("\n".join(lines))
    print(f"wrote {ALIASES.relative_to(ROOT)}: {len(aliases)} aliases")

    grid = [["MAPSEC_NONE"] * GRID_W for _ in range(GRID_H)]
    for sec, _, _, cells in SECTIONS:
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
    canvas, land = paint()
    check(land)
    write_outputs(canvas)
    write_sections()
    preview(canvas)
