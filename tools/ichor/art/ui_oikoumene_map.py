#!/usr/bin/env python3
"""Paint the Oikoumene chart: the post-game's second region map.

Hecataeus drew the world as a round shield: three lands round one sea, and a
river running round the rim. This is that shield in the Aethos chart's
black-figure family (tools/ichor/art/ui_world_map.py): the land is reserved
clay with an incised ink coast, the inner seas are black glaze with
wine-purple strokes, and Okeanos is a band of wine-dark water round the rim
with a current drawn along it, the Shield of Achilles's own device (Iliad
18.607-608). The corners outside the disc are darker terracotta, and the same
meander border as the dialogue box runs round the edge. Aethos sits in the
middle as an inlay: the Aethos chart itself, in miniature, in a gilt ring
round the Omphalos. design/OIKOUMENE.md section 3 is the plan; this script is
the one place its cells live.

The chart takes Kanto's slot in gRegionMapInfos (REGION_OIKOUMENE is
REGION_KANTO, include/constants/regions.h), so it writes Kanto's files:

  graphics/pokenav/region_map/map_kanto.png, .bin, .pal  (Fly and wall map:
      an affine BG, 8bpp, no flips, at most 256 tiles)
  graphics/pokedex/region_map_kanto.png, .bin, .pal      (Pokedex area view:
      a text BG, at most 232 tiles)
  src/data/region_map/region_map_layout_kanto.h           (the section grid)
  src/data/region_map/region_map_sections.json            (every Oikoumene
      section's x, y, width and height; tools/ichor/oikoumene_sections.py
      owns the ids and names)
  design/oikoumene/img/chart.png, chart_grid.png           (previews)

Art and grid come from one table, GRID, so they can't disagree. Each cell is
two characters: a section code from SECTIONS, '::' unnamed land, '--' unnamed
sea, '~~' Okeanos (the band), '<>' the Aethos inlay, '..' the corners
outside the disc. Cell (gx, gy) is screen tile (gx + 1, gy + 2).

The coast is drawn as the Aethos chart's is: land and sea are sampled on a
4-pixel lattice and joined by bilinear interpolation, so a stretch of coast
repeats a few shapes. Here the lattice comes from the cells themselves (a
cell's center takes its own terrain, edges and corners the mix of their
neighbours', with a little fixed jitter so the coasts don't read as a grid),
plus the two ellipses of Okeanos. The script stops if the tiles pass 232.

Usage: python3 tools/ichor/art/ui_oikoumene_map.py
"""
import json
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ui_menus_lib import (ROOT, Canvas, INK, CLAY_DARK, CLAY, CLAY_LIGHT, CLAY_PALE, PARCHMENT, MARBLE,
                          MARBLE_DARK, MARBLE_LIGHT, GOLD, GOLD_DARK, GOLD_PALE, OLIVE, OLIVE_DARK, OLIVE_LIGHT,
                          AEGEAN_LIGHT, AEGEAN_PALE, BRONZE, save_rgb, write_jasc)
import ui_world_map as aethos

inside = aethos.inside

IMG = ROOT / "design/oikoumene/img"
W, H = 240, 160
PAL_BASE = 112          # BG palette 7, where both screens load the map palette
GRID_W, GRID_H = 28, 15
DEX_TILE_LIMIT = 232    # the Pokedex area view; the Fly map's affine BG allows 256

# --- Palette ---------------------------------------------------------------
COLORS = [
    ("glaze", (40, 24, 32)),        # the inner seas: black glaze
    ("wine_dk", (72, 32, 56)),      # wave strokes
    ("wine", (104, 48, 72)),        # surf along the coasts
    ("wine_lt", (152, 88, 104)),    # Okeanos's current, foam
    ("ocean", (88, 32, 64)),        # Okeanos, the wine-dark river round the rim
    ("ink", INK),
    ("clay_dk", CLAY_DARK),         # incised hatching, mountain shade
    ("clay", CLAY),                 # the land
    ("clay_lt", CLAY_LIGHT),        # lit coast
    ("clay_pale", CLAY_PALE),       # roads, highlights, sand
    ("corner", (144, 64, 32)),      # the terracotta outside the disc
    ("parch", PARCHMENT),
    ("white", MARBLE_LIGHT),
    ("marble", MARBLE),
    ("marble_dk", MARBLE_DARK),
    ("gold", GOLD),
    ("gold_dk", GOLD_DARK),
    ("gold_pale", GOLD_PALE),
    ("olive", OLIVE),
    ("olive_dk", OLIVE_DARK),
    ("olive_lt", OLIVE_LIGHT),
    ("lava", (240, 88, 40)),
    ("lava_dk", (176, 40, 24)),
    ("pool", AEGEAN_LIGHT),         # rivers, lakes, springs
    ("ice", AEGEAN_PALE),           # the Rhipaean ice
    ("bronze", BRONZE),             # Colchis
    ("mist", (152, 136, 160)),      # the Cimmerian mist
    ("mist_dk", (104, 88, 120)),
    ("rose", (232, 120, 128)),      # rosy-fingered dawn
    ("ghost", (152, 72, 48)),       # (the Aethos glyphs' keys)
    ("ghost_sea", (88, 48, 72)),
]
C = {name: i for i, (name, _) in enumerate(COLORS)}
RGB = [rgb for _, rgb in COLORS]
assert len(RGB) <= 48

KEY = dict(aethos.KEY)
KEY.update({"n": "ocean", "e": "mist", "E": "mist_dk", "i": "ice", "z": "bronze", "x": "rose",
            "L": "olive_lt", "t": "corner"})


def cell_px(gx, gy):
    """Top-left pixel of map-section cell (gx, gy)."""
    return (gx + 1) * 8, (gy + 2) * 8


# --- The grid ------------------------------------------------------------------
# OIKOUMENE.md section 3's sketch, with every one of the 107 sections given a
# cell. The Black Sea is up and right, Egypt down and right, Libya along the
# bottom, the Pillars at the left, and the north and far west squeezed against
# the rim, as on the old maps. Aethos's inlay is the center (cols 9-11, rows 6-8).
GRID = [
    #0 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
    ".. .. .. .. .. .. .. .. ~~ ~~ ~~ ~~ ~~ SV SV ~~ ~~ ~~ ~~ ~~ .. .. .. .. .. .. .. ..",  # 0
    ".. .. .. .. .. ~~ CI CI ~~ :: :: :: :: HY :: :: :: :: :: ~~ ~~ ~~ ~~ .. .. .. .. ..",  # 1
    ".. .. .. LD ~~ ~~ :: :: :: :: :: :: :: CB RP FW :: AH :: :: :: :: ~~ ~~ ~~ .. .. ..",  # 2
    ".. .. GS ~~ :: :: :: :: :: :: :: :: :: :: OL SR SR :: :: LM :: :: :: :: ~~ ~~ .. ..",  # 3
    ".. ~~ ~~ :: :: :: :: :: :: :: :: :: :: :: -- LE -- -- -- -- -- :: CC CC :: ~~ ~~ ..",  # 4
    "~~ ~~ :: -- AA FL -- -- :: :: BP AB HB SA BO PC PC PC IA -- -- PH AI FA :: :: ~~ ~~",  # 5
    "BL AS :: -- -- CU :: -- OS <> <> <> HE SE BO :: :: :: :: TH CH :: :: GA :: :: :: ~~",  # 6
    "BL :: TA -- AL SI EL KR WD <> <> <> SK IL ID :: PS RR GO TR :: :: :: :: :: :: :: ~~",  # 7
    "~~ GD :: -- -- -- -- :: WD <> <> <> CR WL GP MS SD RR CG :: :: :: :: :: :: :: :: ~~",  # 8
    "ER OC PI OG -- CY TK SS WD -- -- -- -- MI LA MA TM HP :: :: :: :: :: :: :: :: ~~ ~~",  # 9
    ".. HS AR AG :: :: :: LO -- -- KY -- -- -- PX -- -- -- :: :: :: :: :: :: :: DW ~~ ..",  # 10
    ".. .. GR ~~ AT :: :: TT SY AN SP :: :: :: :: NK DR HL :: NY TS MM PG :: ~~ ~~ .. ..",  # 11
    ".. .. .. GG ~~ ~~ :: :: :: SL :: AM SN :: GY PD ME NI HK EP CT MR ~~ ~~ ~~ .. .. ..",  # 12
    ".. .. .. .. .. ~~ SO ~~ ~~ GT :: :: GC :: :: MO :: AY VT ~~ ~~ ~~ ~~ .. .. .. .. ..",  # 13
    ".. .. .. .. .. .. .. .. ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ .. .. .. .. .. .. .. ..",  # 14
]

# Kinds: a TOWN has (or will have) an Asclepeion and a fly target; a WAY is a
# dungeon, sanctuary or landmark on land; a ROAD a land route; a LANE water
# (a sea lane, a strait, a river lane); an ISLE an island in the inner seas; a
# RIM a place in Okeanos itself; a LAKE a lake on land; a RIVER a river lane
# through the land (the Nile and its cataracts), drawn as a river.
TOWN, WAY, ROAD, LANE, ISLE, RIM, LAKE, RIVER = "town", "way", "road", "lane", "isle", "rim", "lake", "river"

# code: (MAPSEC suffix, kind)
SECTIONS = {
    "<>": ("AETHOS", "inlay"),
    # 4.1 Thrace and the Troad
    "SE": ("SESTOS", TOWN), "HE": ("HELLESPONT", LANE), "IL": ("ILION", TOWN),
    "SK": ("SKAMANDER_PLAIN", ROAD), "ID": ("IDA_ROAD", ROAD), "GP": ("GARGAROS_PEAK", WAY),
    "WL": ("WALLS_OF_LAOMEDON", WAY), "CR": ("CHRYSE", TOWN), "HB": ("HEBROS_SHORE", ROAD),
    "AB": ("ABDERA", TOWN), "BP": ("BISTONIAN_PLAIN", ROAD),
    # 4.5 Egypt
    "NK": ("NAUKRATIS", TOWN), "DR": ("DELTA_REEDS", ROAD), "PX": ("PHAROS", ISLE),
    "ME": ("MEMPHIS", TOWN), "PD": ("PYRAMID_FIELD", ROAD), "GY": ("GREAT_PYRAMID", WAY),
    "NI": ("NILE", RIVER), "HL": ("HELIOPOLIS", TOWN), "MO": ("LAKE_MOERIS", LAKE),
    "VT": ("VALLEY_OF_TOMBS", WAY), "HK": ("HEKATOMPYLOS", TOWN), "EP": ("ELEPHANTINE", TOWN),
    "AY": ("ABYDOS", WAY),
    # 4.3 The Black Sea
    "BO": ("BOSPORUS", LANE), "SA": ("SALMYDESSOS", TOWN), "PC": ("PONTIC_COAST", LANE),
    "TH": ("THEMISKYRA", TOWN), "TR": ("THERMODON_ROAD", ROAD), "AI": ("AIA", TOWN),
    "PH": ("PHASIS", ROAD), "FA": ("FIELD_OF_ARES", ROAD), "GA": ("GROVE_OF_ARES", WAY),
    "LE": ("LEUKE", ISLE), "IA": ("ISLE_OF_ARES", ISLE), "CC": ("CAUCASUS", WAY),
    "CH": ("CHALYBIA", TOWN),
    # 4.2 Lydia and Phrygia
    "RR": ("ROYAL_ROAD", ROAD), "SD": ("SARDIS", TOWN), "PS": ("PACTOLUS_SANDS", ROAD),
    "TM": ("MOUNT_TMOLUS", WAY), "HP": ("HYPAIPA", TOWN), "MA": ("MAEANDER", ROAD),
    "MI": ("MILETOS", TOWN), "LA": ("MOUNT_LATMOS", WAY), "CG": ("CHASM_OF_GYGES", WAY),
    "GO": ("GORDION", TOWN), "MS": ("MOUNT_SIPYLOS", WAY),
    # 4.7 Libya
    "AM": ("AMMONION", TOWN), "SN": ("SAND_SEA", ROAD), "KY": ("KYRENE", TOWN),
    "SP": ("SILPHIUM_PLATEAU", ROAD), "TT": ("TRITONIS", LAKE), "SY": ("SYRTIS", ROAD),
    "SL": ("SALT_RIDGE", ROAD), "AN": ("ANTAEUS_RING", WAY), "GT": ("GARAMANTES_TUNNELS", WAY),
    "GC": ("GLASS_CRATER", WAY),
    # 4.4 Scythia and Hyperborea
    "OL": ("OLBIA", TOWN), "SR": ("STEPPE_ROAD", ROAD), "LM": ("LAKE_MAEOTIS", LAKE),
    "FW": ("FEATHER_WASTES", ROAD), "AH": ("ARIMASPIAN_HEIGHTS", ROAD), "RP": ("RHIPAEAN_PASS", ROAD),
    "CB": ("CAVE_OF_BOREAS", WAY), "HY": ("HYPERBOREA", TOWN),
    # 4.6 Aithiopia
    "CT": ("CATARACTS", RIVER), "MR": ("MEROE", TOWN), "TS": ("TABLE_OF_THE_SUN", WAY),
    "NY": ("MOUNT_NYSA", WAY), "MM": ("MOUNTAINS_OF_THE_MOON", ROAD), "PG": ("PYGMY_MARSHES", ROAD),
    "DW": ("GATE_OF_DAWN", RIM),
    # 4.8 The Far West
    "PI": ("PILLARS", LANE), "OC": ("OCEAN_STREAM", RIM), "ER": ("ERYTHEIA", RIM),
    "HS": ("HESPERIDES", RIM), "AR": ("ATLAS_RIDGE", RIM), "GD": ("GADEIRA", TOWN),
    "TA": ("TARTESSOS", TOWN), "AT": ("ATARANTES", TOWN), "AS": ("ATLANTIC_SHORE", ROAD),
    "AG": ("ATLAS_RANGE", WAY),
    # 4.9 The Western Sea
    "WD": ("WINE_DARK_SEA", LANE), "OS": ("OUTER_SEA", LANE), "LO": ("LOTUS_ISLE", ISLE),
    "CY": ("CYCLOPS_ISLE", ISLE), "AL": ("AIOLIA", ISLE), "AA": ("AIAIA", ISLE),
    "SI": ("SIRENS_ROCKS", ISLE), "SS": ("SCYLLA_STRAIT", LANE), "TK": ("THRINAKIA", ISLE),
    "KR": ("KROTON", TOWN), "CU": ("CUMAE", TOWN), "EL": ("ELEA", TOWN),
    "FL": ("PHLEGRAEAN_FIELDS", ROAD), "OG": ("OGYGIA", ISLE),
    # 4.10 The Ring of Okeanos
    "~~": ("OKEANOS", RIM), "CI": ("CIMMERIAN_SHORE", RIM), "LD": ("LAND_OF_DREAMS", RIM),
    "GS": ("GATES_OF_THE_SUN", RIM), "BL": ("ISLES_OF_THE_BLESSED", RIM), "GG": ("GORGONS_ISLE", RIM),
    "GR": ("GRAIAI", RIM), "SO": ("SPRINGS_OF_OKEANOS", RIM), "SV": ("SELVAGE", RIM),
}
LAND_KINDS = {TOWN, WAY, ROAD, LAKE, RIVER}
WATER_KINDS = {LANE, ISLE}


def parse_grid():
    cells = {}
    for gy, row in enumerate(GRID):
        toks = row.split()
        assert len(toks) == GRID_W, (gy, len(toks))
        for gx, t in enumerate(toks):
            assert t in SECTIONS or t in ("::", "--", ".."), (gx, gy, t)
            cells[(gx, gy)] = t
    return cells


CELLS = parse_grid()
CELLS_OF = {}
for _cell, _code in sorted(CELLS.items(), key=lambda kv: (kv[0][1], kv[0][0])):
    if _code in SECTIONS:
        CELLS_OF.setdefault(_code, []).append(_cell)
assert set(CELLS_OF) == set(SECTIONS), set(SECTIONS) ^ set(CELLS_OF)
assert len(SECTIONS) == 107, len(SECTIONS)


def kind_of(code):
    return SECTIONS[code][1] if code in SECTIONS else None


def is_water_cell(code):
    """Inner-sea cells: unnamed sea, lanes, islands (an islet is pasted on
    water), and the water round the Aethos inlay."""
    return code == "--" or code == "<>" or kind_of(code) in WATER_KINDS


# --- Okeanos: the ring of cells round the rim --------------------------------------
def is_ring_cell(code):
    return code == "~~" or kind_of(code) == RIM


JITTER = 0.0
RING = {cell for cell, code in CELLS.items() if is_ring_cell(code)}


def jitter(i, j, salt=0):
    """A fixed pseudo-random number in [-1, 1) for lattice point (i, j)."""
    h = (i * 73856093) ^ (j * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((h >> 8) & 0xFFFF) / 32768.0 - 1.0


# Hand-placed lattice values (cell units -> land 1 / water 0) that shape what
# the cells alone can't: the straits, Italy's boot, the gulfs.
OVERRIDES = {}

# The inner seas, as coastlines in cell units: the lattice is water inside
# any of these. Every sea cell of GRID lies inside one and every land cell
# outside them all (check() proves it), so the art and the grid agree; the
# outlines give the seas their shape where cells alone would make them boxes.
SEAS = [
    # Our sea: the Mediterranean, from the Pillars round Italy and the Aegean
    # (the Aethos inlay sits in it) to the Levant and back along Libya
    [(1.3, 9.3), (2.6, 9.3), (3.15, 8.75),                                        # Calpe
     (3.25, 8.0), (2.85, 7.3), (3.2, 6.5), (2.9, 5.6), (3.1, 5.0),                # Iberia's east coast
     (3.8, 4.75), (4.5, 4.85),                                                     # Gaul
     (4.8, 5.3), (4.75, 6.1), (5.1, 6.9), (5.8, 7.05),                             # Latium, Campania
     (5.9, 7.7), (6.5, 8.2), (6.95, 8.6), (7.3, 9.0),                              # Lucania, the toe
     (7.95, 8.6), (8.05, 7.7), (7.6, 7.05), (7.05, 6.9),                           # Kroton, Taranto's gulf
     (6.95, 6.2), (6.2, 5.7), (6.05, 4.95),                                        # Italy's Adriatic shore
     (6.6, 4.75), (7.6, 4.8),                                                      # the Adriatic's head
     (7.9, 5.4), (8.3, 5.95), (9.2, 6.0),                                          # Illyria, Epirus
     (10.4, 5.95), (11.6, 6.0), (12.9, 5.95),                                      # Thrace's shore
     (12.95, 6.8),                                                                 # the Chersonese
     (12.1, 7.0), (12.0, 7.9), (12.15, 8.9),                                       # the Troad
     (12.95, 9.05), (13.05, 9.95),                                                 # Ionia
     (14.0, 10.0), (15.2, 9.95), (16.4, 10.05), (17.5, 9.95),                      # Lycia, Cilicia
     (18.05, 10.4), (17.9, 10.95),                                                 # the Levant
     (16.8, 11.0), (15.6, 10.95), (14.5, 11.0),                                    # the Delta's coast
     (13.4, 10.95), (12.2, 11.0), (11.1, 10.95),                                   # Marmarica
     (11.05, 10.3), (10.5, 9.95), (9.95, 10.3),                                    # Kyrene's bulge
     (9.9, 10.95), (8.9, 11.05), (8.1, 10.95), (7.0, 10.95),                       # the Syrtis gulfs
     (6.95, 10.0), (5.5, 10.05), (4.2, 9.95), (3.1, 10.05),                        # Libya's north coast
     (2.6, 9.75), (1.3, 9.75)],                                                    # Abila
    # the Hellespont, between Sestos and the Troad, and the Propontis
    [(12.5, 6.8), (14.1, 6.8), (14.1, 7.2), (12.5, 7.2)],
    [(14.05, 6.15), (14.95, 6.15), (14.95, 6.9), (14.05, 6.9)],
    # the Bosporus, narrow, up to the Black Sea
    [(14.3, 4.8), (14.7, 4.8), (14.7, 6.3), (14.3, 6.3)],
    # the Black Sea, with the Crimea and Colchis at its east end
    [(14.1, 4.4), (14.6, 3.95), (16.0, 3.9), (17.0, 3.95), (17.3, 4.35), (17.7, 4.3), (18.2, 3.95),
     (19.5, 3.95), (20.4, 4.1), (20.95, 4.6), (20.95, 5.5), (20.0, 5.95), (19.0, 5.95), (18.0, 6.0),
     (17.0, 5.9), (16.0, 6.0), (15.05, 5.9), (14.7, 5.0), (14.0, 4.9)],
]
LANDS = []


def lattice():
    """Three fields on the 4-pixel lattice, each from the cells touching a
    point: land against water inside the disc; the disc against the corners
    outside it; the world inside Okeanos against the ring. A point at a cell's
    centre takes that cell's value, a point on an edge or a corner the mean of
    the cells it touches, so the rim and the coasts follow the cells with
    rounded steps. A smooth ellipse would put a new tile at every step of its
    curve, far past the 232-tile budget; this way each straight run of the
    rim repeats one tile."""
    lx, ly = W // 4 + 1, H // 4 + 1
    land = np.zeros((ly, lx), float)
    inner = np.zeros((ly, lx), float)
    outer = np.zeros((ly, lx), float)
    for j in range(ly):
        for i in range(lx):
            x, y = i / 2 - 1, j / 2 - 2           # lattice point in cell units
            xs = [x - 0.5] if i % 2 else [x - 1, x]
            ys = [y - 0.5] if j % 2 else [y - 1, y]
            touching = [((int(cx), int(cy)), CELLS.get((int(cx), int(cy)), ".."))
                        for cx in xs for cy in ys]
            n = len(touching)
            outer[j, i] = sum(code != ".." for _, code in touching) / n
            inner[j, i] = sum(code != ".." and cell not in RING for cell, code in touching) / n
            if SEAS:
                v = 0.0 if any(inside(p, x, y) for p in SEAS) else 1.0
                if any(inside(p, x, y) for p in LANDS):
                    v = 1.0
            else:
                v = sum(0.0 if is_water_cell(code) else 1.0 for _, code in touching) / n
                if n > 1 and 0 < v < 1:
                    v += JITTER * jitter(i, j)      # wobble the inner coasts a little
            land[j, i] = v
            if (x, y) in OVERRIDES:
                land[j, i] = OVERRIDES[(x, y)]
    return land, inner, outer


def field(lat, step=4):
    """Bilinear interpolation of a lattice field to every pixel."""
    y = np.arange(H)
    x = np.arange(W)
    j, v = y // step, ((y % step) + 0.5) / step
    i, u = x // step, ((x % step) + 0.5) / step
    a = lat[j][:, i]
    b = lat[j][:, i + 1]
    c = lat[j + 1][:, i]
    d = lat[j + 1][:, i + 1]
    uu, vv = u[None, :], v[:, None]
    return a * (1 - uu) * (1 - vv) + b * uu * (1 - vv) + c * (1 - uu) * vv + d * uu * vv


# --- Islands: drawn whole inside their own cell, so each costs one tile -------
ISLETS = {
    "LE": ["        ", "        ", "  ###   ", " #####  ", " ###### ", "  ####  ", "        ", "        "],  # Leuke, the White Isle
    "IA": ["        ", "        ", "   ##   ", "  ####  ", "  ###   ", "        ", "        ", "        "],  # the Isle of Ares
    "AA": ["        ", "  ##    ", " ####   ", " #####  ", "  ###   ", "        ", "        ", "        "],  # Aiaia
    "AL": ["        ", "        ", "  ####  ", " ###### ", " ###### ", "  ####  ", "        ", "        "],  # Aiolia, bronze-walled
    "SI": ["        ", "        ", " ##  #  ", " #  ##  ", "    #   ", "        ", "        ", "        "],  # the Sirens' rocks
    "CY": ["        ", "        ", "  ###   ", " #####  ", "  ####  ", "   #    ", "        ", "        "],  # the Cyclops's island
    "OG": ["        ", "        ", "  ##    ", " ####   ", " #####  ", "  ###   ", "        ", "        "],  # Ogygia
    "LO": ["        ", "        ", "        ", "  ###   ", " #####  ", "  ##    ", "        ", "        "],  # the Lotus Isle
    "PX": ["        ", "        ", "        ", "        ", "  ####  ", " ###### ", "        ", "        "],  # Pharos
    "ER": ["        ", "  ##    ", " ####   ", " ###    ", "  ##    ", "        ", "        ", "        "],  # Erytheia
    "HS": ["        ", "        ", "   ##   ", "  ####  ", "  ###   ", "        ", "        ", "        "],  # the Hesperides
    "GG": ["        ", "        ", "  ###   ", "  ####  ", "   ##   ", "        ", "        ", "        "],  # the Gorgons' isle
    "GR": ["        ", "        ", "   ##   ", "  ###   ", "   #    ", "        ", "        ", "        "],  # the Graiai's rock
    "TK": ["        ", " ###### ", " #####  ", "  ####  ", "  ###   ", "   #    ", "        ", "        "],  # Thrinakia, three-cornered Sicily
    "BL": ["        ", "   ##   ", "  ####  ", "   ##   ", "        ", "  ###   ", " ####   ", "  ##    "],  # the Isles of the Blessed
}

# --- Glyphs (keys as ui_world_map.KEY, plus n ocean, e/E mist, i ice, z bronze,
# x rose, L olive_lt, t corner; a space leaves the ground) ----------------------
G = {}
G["tower"] = [          # Sestos: Hero's tower, the lamp lit
    "   y    ",
    "  #g#   ",
    "  #w#   ",
    "  #m#   ",
    "  #w#   ",
    " #wmw#  ",
    " #mmm#  ",
    " #####  ",
]
G["troy"] = [           # Ilion: the great sloping walls and the Skaian Gate
    " ##  ## ",
    " #w##w# ",
    "#wwwwwm#",
    "#www#wm#",
    "#ww#k#m#",
    "#ww#k#m#",
    "########",
    "        ",
]
G["walls"] = [          # the Walls of Laomedon, built by two gods for no pay
    "        ",
    "#w#w#w# ",
    "####### ",
    "#wmwwm# ",
    "#mwwmw# ",
    "####### ",
    "        ",
    "        ",
]
G["pyramids"] = [       # the Pyramid Field
    "        ",
    "  #     ",
    " #y#    ",
    " #yG#   ",
    "#yyG#y# ",
    "#yyGGyG#",
    "########",
    "        ",
]
G["great_pyramid"] = [
    "   ##   ",
    "  #yG#  ",
    "  #yG#  ",
    " #yyGG# ",
    " #yyGG# ",
    "#yyyGGG#",
    "########",
    "        ",
]
G["pylon"] = [          # Memphis: a temple pylon
    "        ",
    "###  ###",
    "#wm##wm#",
    "#wmggwm#",
    "#wm##wm#",
    "#wm##wm#",
    "########",
    "        ",
]
G["colossi"] = [        # Hekatompylos: Memnon's singing colossus and its twin
    "   y    ",
    " ##  ## ",
    "#dd##dd#",
    " #d# #d#",
    " #dd##dd",
    "#ddd#ddd",
    "########",
    "        ",
]
G["obelisk"] = [        # Heliopolis: the sun's city
    " g      ",
    "gyg  #  ",
    " g  #y# ",
    "    #y# ",
    "    #y# ",
    "    #y# ",
    "   #####",
    "        ",
]
G["tomb"] = [           # the Valley of Tombs
    "        ",
    "  ####  ",
    " #dddd# ",
    "#dd##dd#",
    "#d#kk#d#",
    "#d#kk#d#",
    "########",
    "        ",
]
G["mastaba"] = [        # Abydos: Osiris's tomb
    "        ",
    "        ",
    "  ####  ",
    " #pppp# ",
    "#pp##pp#",
    "#pp##pp#",
    "########",
    "        ",
]
G["reeds"] = [          # papyrus and reeds, standing in water
    "o  o  o ",
    "O  O oO ",
    "O oO OO ",
    "OoOO OO ",
    "bObbObbb",
    " bbbbbb ",
    "        ",
    "        ",
]
G["lighthouse"] = [     # Pharos (on its islet)
    "   r    ",
    "  #y#   ",
    "  #w#   ",
    "  #m#   ",
    "        ",
    "        ",
    "        ",
    "        ",
]
G["pelta"] = [          # Themiskyra: an Amazon's crescent shield
    "        ",
    "##    ##",
    "#g#  #g#",
    "#gg##gg#",
    " #gggg# ",
    "  #gg#  ",
    "   ##   ",
    "        ",
]
G["palace"] = [         # Aia: Aietes's bronze palace
    "   ##   ",
    "  #zz#  ",
    " #zggz# ",
    "########",
    " z z z  ",
    " z z z  ",
    "########",
    "        ",
]
G["fleece"] = [         # the Grove of Ares: the Golden Fleece on its oak
    " oooo   ",
    "oOooOo  ",
    " oO#oo  ",
    "  #gg   ",
    "  #ygg  ",
    "  #gg   ",
    "  #     ",
    " ###    ",
]
G["furrows"] = [        # the Field of Ares, ploughed with bronze bulls
    "        ",
    " dddddd ",
    "  z  z  ",
    " dddddd ",
    "        ",
    " dddddd ",
    "        ",
    "        ",
]
G["anvil"] = [          # Chalybia: the first iron
    "  r     ",
    " rR     ",
    "        ",
    " ###### ",
    "#mmmmmm#",
    " ##mm## ",
    "  #mm#  ",
    " ###### ",
]
G["coin"] = [           # Sardis: Croesus's gold, the first coins
    "  ####  ",
    " #gggg# ",
    "#gyggGg#",
    "#gGGggg#",
    "#gggGGg#",
    " #gGgg# ",
    "  ####  ",
    "        ",
]
G["knot"] = [           # Gordion: the Knot
    "        ",
    "  #gg#  ",
    " #g##g# ",
    "#g#gg#g#",
    " #g##g# ",
    "  #gg#  ",
    " #g  g# ",
    "        ",
]
G["meander"] = [        # the Maeander, which named the pattern
    "        ",
    "bbbbb b ",
    "    b b ",
    " bbbb b ",
    " b    b ",
    " bbbbbb ",
    "        ",
    "        ",
]
G["moon_peak"] = [      # Latmos (Endymion's moon), the Mountains of the Moon
    " yy     ",
    "y   #   ",
    "y  #l#  ",
    " yy#ld# ",
    "  #lcdd#",
    " #lccdd#",
    "########",
    "        ",
]
G["oasis"] = [          # Ammonion: palms and the Spring of the Sun
    " oo  oo ",
    "oOooOOoo",
    "  #  #  ",
    "  #  #  ",
    " bbbbbb ",
    "  bbbb  ",
    "        ",
    "        ",
]
G["dunes"] = [          # the Great Sand Sea
    "        ",
    "  ppd   ",
    " pccdd  ",
    "pp   ppd",
    "    pccd",
    " ppd    ",
    "pccdd   ",
    "        ",
]
G["silphium"] = [       # the Silphium Plateau
    " y y y  ",
    "  oLo   ",
    "   O    ",
    " L O L  ",
    "  oOo   ",
    "   O    ",
    "  OOO   ",
    "        ",
]
G["salt"] = [           # the salt hills
    "        ",
    "   ##   ",
    "  #ww#  ",
    " #wwmw# ",
    "#wwmmmw#",
    "########",
    "        ",
    "        ",
]
G["ring"] = [           # Antaeus's wrestling ring
    "        ",
    " ###### ",
    "#pppppp#",
    "#pp##pp#",
    "#pppppp#",
    " ###### ",
    "        ",
    "        ",
]
G["crater"] = [         # the Glass Crater
    "        ",
    " ###### ",
    "#ddddd##",
    "#dygyd# ",
    " #yyy#  ",
    "  ###   ",
    "        ",
    "        ",
]
G["cave"] = [           # a cave mouth
    "        ",
    "  ####  ",
    " #dddd# ",
    "#dd##dd#",
    "#d####d#",
    "#d####d#",
    "########",
    "        ",
]
G["feathers"] = [       # the Feather Wastes: the Scythians call snow feathers
    "w   w   ",
    "  w   w ",
    " w  w   ",
    "   w   w",
    "w    w  ",
    "  w  w  ",
    " w     w",
    "   w    ",
]
G["gold_peak"] = [      # the Arimaspian heights, where griffins guard the gold
    "   #    ",
    "  #l#   ",
    "  #lg#  ",
    " #lcdg# ",
    " #lgdd# ",
    "#lccgdd#",
    "########",
    "        ",
]
G["ice"] = [            # the Rhipaean ice walls
    "  #   # ",
    " #i# #i#",
    "#iiw#iiw",
    "#iwi#iwi",
    "#iiw#iiw",
    "########",
    "        ",
    "        ",
]
G["tholos"] = [         # Hyperborea: Apollo's round temple in a green meadow
    "   ##   ",
    "  #ww#  ",
    " ###### ",
    " w w w  ",
    " w w w  ",
    "########",
    "LoLoLoLo",
    "        ",
]
G["cataract"] = [       # the cataracts of the Nile
    "        ",
    "        ",
    "bwbbwbbw",
    "wbbwbbwb",
    "bbwbbwbb",
    "        ",
    "        ",
    "        ",
]
G["steep_pyramids"] = [  # Meroe: steep Nubian pyramids, gold fetters
    "  #  #  ",
    " #d##d# ",
    " #d##dd#",
    "#dd#ddd#",
    "#dd#ddd#",
    "########",
    "  g  g  ",
    "        ",
]
G["table"] = [          # the Table of the Sun
    "        ",
    "  r g y ",
    "########",
    "#gggggg#",
    " #    # ",
    " #    # ",
    "        ",
    "        ",
]
G["sunrise"] = [        # the Gate of Dawn, on Okeanos's eastern shore
    " x  y  x",
    "  x y x ",
    "   yyy  ",
    "  ygggy ",
    " yggggy ",
    "########",
    "        ",
    "        ",
]
G["pillars"] = [        # the Pillars: NE PLUS ULTRA
    " #    # ",
    "#w#  #w#",
    "#w#  #w#",
    "#w#  #w#",
    "#m#  #m#",
    "###  ###",
    "        ",
    "        ",
]
G["cup"] = [            # Helios's golden cup on the Ocean stream
    "        ",
    "        ",
    "#gggggg#",
    " #gyyg# ",
    "  #gg#  ",
    "   ##   ",
    "        ",
    "        ",
]
G["atlas"] = [          # Atlas's Ridge: the peak that holds up the sky
    "wwwwwww ",
    "  #l#   ",
    " #lcd#  ",
    " #lcd#  ",
    "#lccdd# ",
    "#lccdd# ",
    "####### ",
    "        ",
]
G["volcano"] = [        # the Burning Fields; Etna on Thrinakia
    "  r  R  ",
    " R r    ",
    "   ##   ",
    "  #rr#  ",
    " #lccd# ",
    "#lcccdd#",
    "########",
    "        ",
]
G["etna"] = [          # Etna on Thrinakia (on its islet)
    "   r    ",
    "   #    ",
    "  #l#   ",
    "        ",
    "        ",
    "        ",
    "        ",
    "        ",
]
G["cattle"] = [         # Thrinakia: Helios's cattle
    "        ",
    "        ",
    "  # #   ",
    " #pp#   ",
    "#pppp#  ",
    " #  #   ",
    "        ",
    "        ",
]
G["whirlpool"] = [      # Scylla and Charybdis
    "        ",
    " vvvvv  ",
    "v     v ",
    "v vvv v ",
    "v v v v ",
    "v vv  v ",
    " v   v  ",
    "  vvv   ",
]
G["mist"] = [           # the Cimmerian shore, in perpetual dusk
    "eeee    ",
    "  eeEEe ",
    " Eeee   ",
    "    eeee",
    "eeEe    ",
    "   eeEE ",
    "        ",
    "        ",
]
G["dream_gates"] = [    # the Land of Dreams: the gates of horn and of ivory
    "  #  #  ",
    " #p##w# ",
    " #p##w# ",
    " #p##w# ",
    " #p##w# ",
    " ###### ",
    "        ",
    "        ",
]
G["sun_gates"] = [      # the Gates of the Sun, where it goes in at evening
    "  yyy   ",
    " ygggy  ",
    "########",
    "#z#z#z##",
    "#z#z#z##",
    "########",
    "        ",
    "        ",
]
G["spring"] = [         # the Springs of Okeanos, where every river rises
    "   b    ",
    "  b b   ",
    " b  b   ",
    "  bbb   ",
    " bbbbb  ",
    "bbbbbbb ",
    "        ",
    "        ",
]
G["selvage"] = [        # the Selvage: Okeanos pours over the edge of the world
    "ww w ww ",
    "w ww w w",
    " w  w  w",
    "w  w  w ",
    "        ",
    "        ",
    "        ",
    "        ",
]
G["gorgon"] = [         # the Gorgons' isle (on its islet)
    "        ",
    "        ",
    "  ky    ",
    "  kk    ",
    "        ",
    "        ",
    "        ",
    "        ",
]
G["eye"] = [            # the Graiai and their one eye
    "        ",
    "        ",
    "   wk   ",
    "        ",
    "        ",
    "        ",
    "        ",
    "        ",
]
G["apples"] = [         # the Hesperides' golden apples
    "        ",
    "        ",
    "   oo   ",
    "  ogOo  ",
    "   g    ",
    "        ",
    "        ",
    "        ",
]
G["blessed"] = [        # the Isles of the Blessed: gold meadows, roses
    "        ",
    "   gx   ",
    "  LgxL  ",
    "   L    ",
    "        ",
    "  gxL   ",
    " LxgL   ",
    "        ",
]
G["red_isle"] = [       # Erytheia, Geryon's red island
    "        ",
    "  RR    ",
    " RrRR   ",
    " RRr    ",
    "  RR    ",
    "        ",
    "        ",
    "        ",
]
G["white_isle"] = [     # Leuke
    "        ",
    "        ",
    "  www   ",
    " wwmww  ",
    " wwmwmw ",
    "  mmmm  ",
    "        ",
    "        ",
]
G["bronze_isle"] = [    # Aiolia, walled in bronze
    "        ",
    "        ",
    "  zzzz  ",
    " zcccLz ",
    " zcLccz ",
    "  zzzz  ",
    "        ",
    "        ",
]
G["one_eye"] = [        # the Cyclops's island
    "        ",
    "        ",
    "        ",
    "   kw   ",
    "        ",
    "        ",
    "        ",
    "        ",
]
G["lotus"] = [
    "        ",
    "        ",
    "   w    ",
    "  wxw   ",
    "        ",
    "        ",
    "        ",
    "        ",
]
G["grove"] = [          # Aiaia and Ogygia: a wooded isle
    "        ",
    "  oo    ",
    " oOo    ",
    "  o#    ",
    "        ",
    "        ",
    "        ",
    "        ",
]
G["birds"] = [          # the Isle of Ares and its bronze-feathered birds
    " z   z  ",
    "z z z z ",
    "        ",
    "        ",
    "        ",
    "        ",
    "        ",
    "        ",
]
G["horse"] = [          # the Bistonian Plain: Diomedes's mares
    "        ",
    "    ##  ",
    "   #dd# ",
    "#ddddd# ",
    " #dddd  ",
    " #  #   ",
    " #  #   ",
    "        ",
]
G["tunnels"] = [        # the Garamantes' tunnels
    "        ",
    "        ",
    " ##  ## ",
    "#kk##kk#",
    "#kk##kk#",
    "########",
    "        ",
    "        ",
]
G["sibyl"] = [          # Cumae: the Sibyl's cave
    "   y    ",
    "  ####  ",
    " #dddd# ",
    "#dd##dd#",
    "#d#yk#d#",
    "#d####d#",
    "########",
    "        ",
]

# Which glyph marks each place. Routes and lanes are drawn as paths instead.
GLYPHS = {
    "SE": G["tower"], "IL": G["troy"], "WL": G["walls"], "GP": aethos.MOUNTAIN, "CR": aethos.TEMPLE,
    "AB": aethos.PORT, "BP": G["horse"], "HB": None,
    "NK": aethos.PORT, "DR": G["reeds"], "ME": G["pylon"], "PD": G["pyramids"], "GY": G["great_pyramid"],
    "HL": G["obelisk"], "MO": aethos.LAKE, "VT": G["tomb"], "HK": G["colossi"], "EP": aethos.HAMLET,
    "AY": G["mastaba"],
    "SA": aethos.HAMLET, "TH": G["pelta"], "AI": G["palace"], "FA": G["furrows"], "GA": G["fleece"],
    "CC": aethos.SNOW_PEAK, "CH": G["anvil"],
    "SD": G["coin"], "TM": aethos.KITHAIRON, "HP": aethos.HAMLET, "MA": G["meander"], "MI": aethos.PORT,
    "LA": G["moon_peak"], "CG": G["cave"], "GO": G["knot"], "MS": aethos.MOUNTAIN,
    "AM": G["oasis"], "SN": G["dunes"], "KY": aethos.TEMPLE, "SP": G["silphium"], "TT": aethos.LAKE,
    "SL": G["salt"], "AN": G["ring"], "GT": G["tunnels"], "GC": G["crater"],
    "OL": aethos.PORT, "SR": aethos.MOUND, "LM": aethos.LAKE, "FW": G["feathers"], "AH": G["gold_peak"],
    "RP": G["ice"], "CB": G["cave"], "HY": G["tholos"],
    "CT": G["cataract"], "MR": G["steep_pyramids"], "TS": G["table"], "NY": aethos.KITHAIRON,
    "MM": G["moon_peak"], "PG": G["reeds"], "DW": G["sunrise"],
    "PI": G["pillars"], "OC": G["cup"], "HS": G["apples"], "AR": G["atlas"], "GD": aethos.PORT,
    "TA": aethos.SOUNION, "AT": aethos.HAMLET, "AG": aethos.SNOW_PEAK,
    "TK": G["etna"], "KR": aethos.TEMPLE, "CU": G["sibyl"], "EL": aethos.HAMLET, "FL": G["volcano"],
    "SS": G["whirlpool"],
    "LE": G["white_isle"], "IA": G["birds"], "AA": G["grove"], "AL": G["bronze_isle"], "CY": G["one_eye"],
    "OG": G["grove"], "LO": G["lotus"], "PX": G["lighthouse"], "ER": G["red_isle"], "GG": G["gorgon"],
    "GR": G["eye"], "BL": G["blessed"],
    "CI": G["mist"], "LD": G["dream_gates"], "GS": G["sun_gates"], "SO": G["spring"], "SV": G["selvage"],
}

# The land between the places: ranges, forests, steppe and desert on whole
# cells, so the same stamp on clay is always the same tile.
LANDSCAPE = [
    (aethos.SNOW_PEAK, [(24, 4), (24, 5)]),                    # the Caucasus's east
    (aethos.MOUNTAIN, [(21, 4), (22, 7), (24, 7)]),            # Armenia, the Taurus
    (aethos.SMALL_PEAK, [(20, 7), (23, 8), (20, 3), (11, 3)]),
    (aethos.CYPRESS, [(5, 3), (7, 4), (9, 3)]),                # Europe's forests
    (aethos.MOUND, [(18, 3), (16, 2)]),                        # the steppe's barrows
    (G["dunes"], [(20, 9), (23, 10), (13, 11), (6, 12), (10, 13)]),  # Arabia, Libya
    (G["oasis"], [(22, 9)]),
    (aethos.OLIVES, [(15, 7), (2, 6)]),                        # Ionia; Iberia
    (aethos.SMALL_PEAK, [(5, 11), (11, 11)]),                  # the Atlas foothills; Libya's jebel
]

# --- Journeys -----------------------------------------------------------------
# Land routes, as chains of section codes or bare (x, y) cells; each link is
# drawn centre to centre in tile-local coordinates, so a straight piece is
# always the same tile (ui_world_map.py's method).
ROADS = [
    ["SK", "IL", "ID", "GP", "MS", "SD", "RR", "GO", "TR", "TH", "CH"],   # the Troad to the Royal Road
    ["MI", "LA", "MA", "TM", "SD", "PS"],
    ["TM", "HP"],
    ["BP", "AB", "HB", "SA"],                                             # the Thracian shore
    ["PH", "AI", "FA", "GA"],                                             # up the Phasis to the Fleece
    ["OL", "SR"], ["SR", "FW", "RP", "CB", "HY"], [(16, 3), (16, 2), "AH"],  # the steppe to Hyperborea
    ["NK", "DR", "ME", "PD", "GY"], ["DR", "HL"],                         # the delta
    ["KY", "SP", "AN", "SL"], ["SP", (10, 12), "AM", "SN", (13, 12), "GY"], ["TT", "SY", "AN"],
    ["EP", "NY", "TS", "MM", "PG", (23, 11), (23, 10), (24, 10)],        # Aithiopia to the Gate of Dawn
    ["MM", "MR"],
    ["AS", (1, 7), "GD"], [(1, 7), "TA"], ["AG", (4, 10), "AT"],          # the far west
    ["FL", "CU", (6, 6), "EL", "KR", (7, 8)],                             # Italy's road
]
# The Nile and the Phasis's mouth, drawn as rivers through the same cells.
RIVERS = [["DR", "ME", "NI", "HK", "EP", "CT", "MR"]]
# Sea lanes as polylines in cell units, gold dashes on water only.
LANES = [
    # the Hellespont, the Bosporus and the Pontic coast to Colchis
    [(11.9, 6.55), (12.6, 6.7), (13.5, 7.0), (14.5, 6.6), (14.5, 5.4), (15.5, 5.45), (17.5, 5.4),
     (19.6, 5.4), (20.8, 5.3)],
    # Pharos's waters: Kaldera's south-east sea to the delta
    [(11.6, 8.6), (12.6, 9.5), (13.6, 10.3), (14.6, 10.7), (15.2, 10.9)],
    # the wine-dark sea: Maleia's storm out to the Lotus Isle
    [(9.1, 8.9), (8.5, 9.4), (8.2, 10.2), (7.9, 10.5)],
    # the Outer Sea: from Ogygia home to Kerkyra
    [(3.8, 9.3), (4.5, 8.6), (6.6, 8.3), (7.6, 6.6), (8.6, 6.4), (9.05, 6.4)],
]


# --- Painting -------------------------------------------------------------------
def stamp(c, glyph, x, y):
    for j, row in enumerate(glyph):
        for i, ch in enumerate(row):
            if ch != " ":
                c.px(x + i, y + j, C[KEY[ch]])


# Okeanos: an ellipse round the grid, two 4-pixel blocks wide, drawn in whole
# 4x4 blocks. A smooth curve would need a new tile at nearly every step (about
# 120 tiles for the rim alone); in blocks it is a pixel-art ellipse that still
# reads as a round shield, and its steps repeat.
RIM_CX, RIM_CY, RIM_A, RIM_B = 120.0, 76.0, 112.5, 60.5
RIM_WIDTH = 8


def rim_blocks(offset=0):
    """Pixels whose 4x4 block's centre lies inside the ellipse shrunk by offset."""
    by, bx = np.mgrid[0:H // 4, 0:W // 4]
    cx, cy = bx * 4 + 2, by * 4 + 2
    inside = ((cx - RIM_CX) / (RIM_A - offset)) ** 2 + ((cy - RIM_CY) / (RIM_B - offset)) ** 2 <= 1
    return np.repeat(np.repeat(inside, 4, axis=0), 4, axis=1)


def classify():
    """Every pixel's terrain: 0 corner, 1 Okeanos, 2 sea, 3 land."""
    land_l, _, _ = lattice()
    outer = rim_blocks()
    inner = rim_blocks(RIM_WIDTH)
    land = (field(land_l) > 0.5) & inner
    for code, rows in ISLETS.items():
        for cell in CELLS_OF[code]:
            x0, y0 = cell_px(*cell)
            for r, row in enumerate(rows):
                for k, ch in enumerate(row):
                    if ch == "#":
                        land[y0 + r, x0 + k] = True
    t = np.zeros((H, W), np.uint8)
    t[outer] = 1
    t[outer & inner] = 2
    t[land] = 3
    # the inlay: water round the roundel, the roundel itself painted later
    x0, y0 = cell_px(9, 6)
    t[y0:y0 + 24, x0:x0 + 24] = np.where(t[y0:y0 + 24, x0:x0 + 24] == 3, 2, t[y0:y0 + 24, x0:x0 + 24])
    return t


def neighbours(mask):
    """For each pixel, whether any 4-neighbour is in mask (off-canvas counts as not)."""
    n = np.zeros_like(mask)
    n[1:, :] |= mask[:-1, :]
    n[:-1, :] |= mask[1:, :]
    n[:, 1:] |= mask[:, :-1]
    n[:, :-1] |= mask[:, 1:]
    return n


def paint_ground(c, t):
    fill = {0: "corner", 1: "ocean", 2: "glaze", 3: "clay"}
    for k, name in fill.items():
        c.a[t == k] = C[name]
    land = t == 3
    # the coast: an incised ink line, the top-left lit, surf outside
    edge = land & neighbours(~land)
    c.a[edge] = C["ink"]
    # lit and surf only on the inner seas: the rim keeps to its blocks
    sea = t == 2
    lit = np.zeros_like(land)
    lit[:, 2:] |= sea[:, :-2]
    lit[2:, :] |= sea[:-2, :]
    c.a[land & ~edge & lit] = C["clay_lt"]
    surf = sea & neighbours(land)
    c.a[surf] = C["wine"]
    # the rim: ink on both edges of the band where it meets the corners
    rim = (t == 1) & neighbours(t == 0)
    c.a[rim] = C["ink"]


def ring_loop():
    """The ring's cells in order round the rim. Each has exactly two ring
    neighbours, so the ring is one closed loop."""
    start = min(RING, key=lambda cell: (cell[1], cell[0]))
    loop, prev, cur = [start], None, start
    while True:
        nbrs = [(cur[0] + dx, cur[1] + dy) for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1))]
        nbrs = [n for n in nbrs if n in RING]
        assert len(nbrs) == 2, (cur, nbrs)
        nxt = nbrs[0] if nbrs[0] != prev else nbrs[1]
        if nxt == start:
            break
        loop.append(nxt)
        prev, cur = cur, nxt
    assert len(loop) == len(RING), (len(loop), len(RING))
    return loop


def paint_current(c, t):
    """Okeanos's current: a line of foam through the ring, cell to cell, the
    river running round the shield's rim. It steps as the ring steps, like
    the meander on the border, and each straight piece is one tile."""
    mid = rim_blocks(RIM_WIDTH // 2)
    line = mid & neighbours(~mid) & (t == 1) & (c.a == C["ocean"])
    c.a[line] = C["wine_lt"]
    return
    loop = ring_loop()
    dirs = {}
    for a, b in zip(loop, loop[1:] + loop[:1]):
        d = (b[0] - a[0], b[1] - a[1])
        name = {(0, -1): "N", (1, 0): "E", (0, 1): "S", (-1, 0): "W"}[d]
        back = {"N": "S", "S": "N", "E": "W", "W": "E"}[name]
        dirs.setdefault(a, set()).add(name)
        dirs.setdefault(b, set()).add(back)
    for cell, ds in dirs.items():
        x0, y0 = cell_px(*cell)
        for (i, j) in segments(ds):
            if t[y0 + j, x0 + i] == 1:
                c.px(x0 + i, y0 + j, C["wine_lt"])


def paint_waves(c):
    """Wine strokes on a 16x16 repeat, only on tiles of open sea or open
    Okeanos, so open water costs a few tiles and every coast stays clean."""
    for base, stroke in (("glaze", "wine_dk"), ("ocean", "wine")):
        for ty in range(20):
            for tx in range(30):
                tile = c.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                if not (tile == C[base]).all():
                    continue
                for j in range(8):
                    for i in range(8):
                        x, y = tx * 8 + i, ty * 8 + j
                        u, v = x % 16, y % 16
                        if ((v == 3 and 2 <= u <= 5) or (v == 2 and u in (6, 7)) or (v == 4 and u == 1)
                                or (v == 11 and 10 <= u <= 13) or (v == 10 and u in (14, 15))
                                or (v == 12 and u == 9)):
                            c.px(x, y, C[stroke])


def chain_cells(chain):
    """A chain of codes and cells, as a list of cells, each code entered at
    the cell nearest the previous one and left from its nearest to the next."""
    out = []
    for k, item in enumerate(chain):
        if isinstance(item, tuple):
            out.append(item)
            continue
        cells = CELLS_OF[item]
        if len(cells) == 1:
            out.append(cells[0])
            continue
        # a section of several cells: walk them in the order that joins up
        prev = out[-1] if out else None
        nxt = chain[k + 1] if k + 1 < len(chain) else None
        nxt_cell = (nxt if isinstance(nxt, tuple) else CELLS_OF[nxt][0]) if nxt else None
        order = sorted(cells, key=lambda c: (abs(c[0] - prev[0]) + abs(c[1] - prev[1])) if prev
                       else -(abs(c[0] - nxt_cell[0]) + abs(c[1] - nxt_cell[1])))
        out.extend(order)
    return out


def links(chains):
    out = {}
    dirs = {(0, -1): "N", (1, 0): "E", (0, 1): "S", (-1, 0): "W"}
    for chain in chains:
        cells = chain_cells(chain)
        for a, b in zip(cells, cells[1:]):
            d = (b[0] - a[0], b[1] - a[1])
            assert d in dirs, (chain, a, b)
            out.setdefault(a, set()).add(dirs[d])
            out.setdefault(b, set()).add(dirs[(-d[0], -d[1])])
    return out


def segments(dirs):
    pts = set()
    for d in dirs:
        if d == "N":
            pts |= {(3, j) for j in range(0, 5)}
        elif d == "S":
            pts |= {(3, j) for j in range(3, 8)}
        elif d == "W":
            pts |= {(i, 3) for i in range(0, 5)}
        elif d == "E":
            pts |= {(i, 3) for i in range(3, 8)}
    return pts


def paint_roads(c, t):
    for cell, dirs in links(ROADS).items():
        x0, y0 = cell_px(*cell)
        for (i, j) in sorted(segments(dirs)):
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                x, y = x0 + i + dx, y0 + j + dy
                if t[y, x] == 3 and c.a[y, x] != C["ink"]:
                    c.px(x, y, C["clay_pale"])


def paint_rivers(c, t):
    for cell, dirs in links(RIVERS).items():
        x0, y0 = cell_px(*cell)
        for (i, j) in sorted(segments(dirs)):
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                x, y = x0 + i + dx, y0 + j + dy
                if t[y, x] == 3:
                    c.px(x, y, C["pool"])
    # the delta's mouths, from the Delta Reeds to the sea
    x0, y0 = cell_px(16, 11)
    for y in range(y0 - 2, y0 + 4):
        if t[y, x0 + 3] == 3:
            c.px(x0 + 3, y, C["pool"])
            c.px(x0 + 4, y, C["pool"])
    for k in range(4):
        if t[y0 + 1 - k, x0 + 1 - k] == 3:
            c.px(x0 + 1 - k, y0 + 1 - k, C["pool"])


def paint_lanes(c, t):
    for poly in LANES:
        n = 0
        for (ax, ay), (bx, by) in zip(poly, poly[1:]):
            x0, y0 = (ax + 1) * 8, (ay + 2) * 8
            x1, y1 = (bx + 1) * 8, (by + 2) * 8
            steps = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
            for s in range(steps):
                x = round(x0 + (x1 - x0) * s / steps)
                y = round(y0 + (y1 - y0) * s / steps)
                n += 1
                if 0 <= x < W and 0 <= y < H and t[y, x] in (1, 2) and n % 4 < 2:
                    if c.a[y, x] in (C["glaze"], C["wine_dk"], C["ocean"]):
                        c.px(x, y, C["gold_dk"])


def paint_inlay(c):
    """Aethos at the centre: the Aethos chart itself in miniature, in a gilt
    ring round the Omphalos."""
    x0, y0 = cell_px(9, 6)
    cx, cy, r = x0 + 11.5, y0 + 11.5, 11.6
    small = aethos_miniature()
    for y in range(y0, y0 + 24):
        for x in range(x0, x0 + 24):
            d = math.hypot(x - cx, y - cy)
            if d > r + 0.5:
                continue
            if d > r - 1:
                c.px(x, y, C["ink"])
            elif d > r - 2:
                c.px(x, y, C["gold"] if (x + y) % 2 else C["gold_dk"])
            elif d > r - 3:
                c.px(x, y, C["ink"])
            else:
                c.px(x, y, C["glaze"])
    sh, sw = small.shape
    ox, oy = x0 + 12 - sw // 2, y0 + 12 - sh // 2
    for j in range(sh):
        for i in range(sw):
            if small[j, i] and math.hypot(ox + i - cx, oy + j - cy) < r - 3:
                c.px(ox + i, oy + j, C["clay"])
    # the coast of the miniature, in ink, and the Omphalos at Delphoi in gold
    for j in range(sh):
        for i in range(sw):
            if not small[j, i]:
                continue
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ii, jj = i + di, j + dj
                if not (0 <= ii < sw and 0 <= jj < sh) or not small[jj, ii]:
                    if math.hypot(ox + i - cx, oy + j - cy) < r - 3:
                        c.px(ox + i, oy + j, C["clay_dk"])
                    break
    dx, dy = AETHOS_OMPHALOS
    c.px(ox + dx, oy + dy, C["gold_pale"])
    c.px(ox + dx, oy + dy + 1, C["gold"])


AETHOS_OMPHALOS = (0, 0)


def aethos_miniature():
    """The Aethos chart's land, shrunk to fit the inlay: its grid (224x120
    pixels) to 20x11, by majority."""
    global AETHOS_OMPHALOS
    m = aethos.land_mask()[16:136, 8:232]
    sw, sh = 20, 11
    out = np.zeros((sh, sw), bool)
    for j in range(sh):
        for i in range(sw):
            blk = m[j * 120 // sh:(j + 1) * 120 // sh, i * 224 // sw:(i + 1) * 224 // sw]
            out[j, i] = blk.mean() > 0.45
    # Delphoi, cell (7, 3) of the Aethos grid
    AETHOS_OMPHALOS = (int((7.5 * 8) * sw / 224), int((3.5 * 8) * sh / 120))
    return out


def paint_glyphs(c, t, landscape=True):
    for glyph, cells in LANDSCAPE if landscape else []:
        for cell in cells:
            assert CELLS[cell] == "::", cell
            stamp(c, glyph, *cell_px(*cell))
    for code, glyph in GLYPHS.items():
        if glyph is None:
            continue
        for cell in CELLS_OF[code]:
            stamp(c, glyph, *cell_px(*cell))


# --- The meander border: the dialogue box's own key -------------------------------
def border(c):
    top = aethos.TOP
    left = ["".join(row[k] for row in top) for k in range(8)]
    tiles = {
        "tl": aethos.CORNER, "tr": [r[::-1] for r in aethos.CORNER], "bl": aethos.CORNER[::-1],
        "br": [r[::-1] for r in aethos.CORNER[::-1]], "t": top, "b": top[::-1],
        "l": left, "r": [r[::-1] for r in left],
    }
    bkey = {" ": "corner", "o": "clay_dk", "#": "ink", ".": "clay", "d": "clay_dk"}

    def put(name, tx, ty):
        for j, row in enumerate(tiles[name]):
            for i, ch in enumerate(row):
                c.px(tx * 8 + i, ty * 8 + j, C[bkey[ch]])

    for tx in range(1, 29):
        put("t", tx, 0)
        put("b", tx, 19)
    for ty in range(1, 19):
        put("l", 0, ty)
        put("r", 29, ty)
    put("tl", 0, 0), put("tr", 29, 0), put("bl", 0, 19), put("br", 29, 19)


def paint(lean=0):
    """The chart. lean > 0 leaves out decoration, a layer at a time, for a
    screen with a smaller tile budget: 1 the landscape stamps, 2 the sea
    lanes too, 3 the roads too. Every place keeps its glyph."""
    t = classify()
    c = Canvas(W, H, C["corner"])
    paint_ground(c, t)
    paint_current(c, t)
    paint_rivers(c, t)
    if lean < 3:
        paint_roads(c, t)
    paint_glyphs(c, t, landscape=lean < 1)
    paint_inlay(c)
    paint_waves(c)
    if lean < 2:
        paint_lanes(c, t)
    border(c)
    return c, t


def check(t):
    """Every land place stands on land, every lane and island on the inner
    seas, every rim place in Okeanos."""
    bad = []
    for code, cells in CELLS_OF.items():
        kind = SECTIONS[code][1]
        for (gx, gy) in cells:
            x, y = cell_px(gx, gy)
            centre = t[y + 3:y + 5, x + 3:x + 5]
            if kind in LAND_KINDS and not (centre == 3).any():
                bad.append((code, (gx, gy), "should be on land"))
            if kind == LANE and not ((centre == 2) | (centre == 1)).any():
                bad.append((code, (gx, gy), "should be on water"))
            if kind == ISLE and not (t[y:y + 8, x:x + 8] == 2).any():
                bad.append((code, (gx, gy), "an island should have sea round it"))
            if kind == RIM and not (t[y:y + 8, x:x + 8] == 1).any():
                bad.append((code, (gx, gy), "should be in Okeanos"))
    for b in bad:
        print("  !", *b)
    assert not bad


# --- Tiles ----------------------------------------------------------------------
def cut(c):
    tiles, index, tmap = [], {}, np.zeros((20, 30), int)
    for ty in range(20):
        for tx in range(30):
            tile = c.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            k = tile.tobytes()
            if k not in index:
                index[k] = len(tiles)
                tiles.append(tile.copy())
            tmap[ty, tx] = index[k]
    return tiles, tmap


FLY_TILE_LIMIT = 256    # the Fly and wall map: an affine BG, 8bpp, 256 tiles at char base 2
LEAN_NAMES = ["full", "no landscape stamps", "no landscape or sea lanes", "no landscape, lanes or roads"]


def write_sheet(path_png, path_pal, tiles):
    """The tiles as a 16-wide 8bpp sheet, indices offset into palette 7. It
    is always 256 cells, so region_map.c's "-num_tiles" cuts always fit; the
    unused cells are blank."""
    pal = list(RGB) + [(0, 0, 0)] * (48 - len(RGB))
    full = [(0, 0, 0)] * 256
    for i, col in enumerate(pal):
        full[PAL_BASE + i] = col
    sheet = np.zeros((16 * 8, 128), np.uint8)
    for i, tile in enumerate(tiles):
        y, x = (i // 16) * 8, (i % 16) * 8
        sheet[y:y + 8, x:x + 8] = tile + PAL_BASE
    im = Image.fromarray(sheet, "P")
    im.putpalette([v for col in full for v in col])
    im.save(path_png)
    write_jasc(path_pal, pal)
    print(f"wrote {path_png.relative_to(ROOT)}, {path_pal.name}")


def write_outputs():
    """The Fly and wall map get the full chart. The Pokedex area view has 24
    fewer tiles to spend, so it takes the leanest-needed version: the same
    chart and every place, less decoration a layer at a time (paint's lean)."""
    fly, _ = paint(0)
    tiles, tmap = cut(fly)
    print(f"Oikoumene chart, Fly map: {len(tiles)} unique tiles (room for {FLY_TILE_LIMIT})")
    if len(tiles) > FLY_TILE_LIMIT:
        raise SystemExit(f"{len(tiles)} tiles: over the Fly map's {FLY_TILE_LIMIT}")
    write_sheet(ROOT / "graphics/pokenav/region_map/map_kanto.png",
                ROOT / "graphics/pokenav/region_map/map_kanto.pal", tiles)
    corner = tmap[1, 1]     # off-screen cells: the terracotta outside the disc
    aff = np.full((64, 64), corner, np.uint8)
    aff[:20, :30] = tmap
    (ROOT / "graphics/pokenav/region_map/map_kanto.bin").write_bytes(aff.tobytes())
    print("wrote graphics/pokenav/region_map/map_kanto.bin")

    for lean in range(len(LEAN_NAMES)):
        dex, _ = paint(lean)
        dtiles, dmap = cut(dex)
        if len(dtiles) <= DEX_TILE_LIMIT:
            break
    print(f"Oikoumene chart, Pokedex area: {len(dtiles)} unique tiles (room for {DEX_TILE_LIMIT}), "
          f"{LEAN_NAMES[lean]}")
    if len(dtiles) > DEX_TILE_LIMIT:
        raise SystemExit(f"{len(dtiles)} tiles even at its leanest: over the Pokedex area's {DEX_TILE_LIMIT}")
    write_sheet(ROOT / "graphics/pokedex/region_map_kanto.png", ROOT / "graphics/pokedex/region_map_kanto.pal",
                dtiles)
    txt = np.full((32, 32), dmap[1, 1], np.uint16)
    txt[:20, :30] = dmap
    (ROOT / "graphics/pokedex/region_map_kanto.bin").write_bytes(txt.astype("<u2").tobytes())
    print("wrote graphics/pokedex/region_map_kanto.bin")
    return fly, dex, lean


def write_sections():
    """The grid header and every Oikoumene section's box in the json. The ids
    and names are tools/ichor/oikoumene_sections.py's."""
    grid = [["MAPSEC_NONE"] * GRID_W for _ in range(GRID_H)]
    for (gx, gy), code in CELLS.items():
        if code in SECTIONS:
            grid[gy][gx] = "MAPSEC_" + SECTIONS[code][0]
    lines = [
        "// Ichor: the Oikoumene chart's section grid, 28x15 cells, in Kanto's chart slot",
        "// (REGION_OIKOUMENE is REGION_KANTO). Generated by tools/ichor/art/ui_oikoumene_map.py",
        "// from the same table that paints the chart; edit GRID there and rerun it.",
        "// design/OIKOUMENE.md section 3 has the plan.",
        "static const mapsec_u8_t sRegionMapSections_Kanto[MAP_HEIGHT][MAP_WIDTH] = {",
    ]
    for row in grid:
        lines.append("    {" + ", ".join(row) + "},")
    lines.append("};")
    out = ROOT / "src/data/region_map/region_map_layout_kanto.h"
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out.relative_to(ROOT)}")

    path = ROOT / "src/data/region_map/region_map_sections.json"
    data = json.loads(path.read_text())
    by_id = {e["id"]: e for e in data["map_sections"]}
    for code, (suffix, _) in SECTIONS.items():
        sec = "MAPSEC_" + suffix
        if sec not in by_id:
            raise SystemExit(f"{sec} is not in region_map_sections.json: run tools/ichor/oikoumene_sections.py")
        cells = CELLS_OF[code]
        xs, ys = [x for x, _ in cells], [y for _, y in cells]
        e = by_id[sec]
        e["x"], e["y"] = min(xs), min(ys)
        e["width"], e["height"] = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {path.relative_to(ROOT)}: {len(SECTIONS)} Oikoumene sections placed")


# --- Previews -------------------------------------------------------------------
KIND_COLOR = {TOWN: (240, 192, 64), WAY: (120, 208, 120), ROAD: (112, 168, 224), LANE: (176, 136, 232),
              ISLE: (232, 232, 232), RIM: (232, 120, 160), LAKE: (112, 200, 232), RIVER: (112, 200, 232), "inlay": (255, 255, 255)}


def rgb_of(c):
    return np.array(RGB + [(255, 0, 255)] * (256 - len(RGB)), np.uint8)[c.a]


def names():
    data = json.loads((ROOT / "src/data/region_map/region_map_sections.json").read_text())
    return {e["id"]: e.get("name", "") for e in data["map_sections"]}


def preview(c):
    rgb = rgb_of(c)
    IMG.mkdir(parents=True, exist_ok=True)
    save_rgb(IMG / "chart.png", rgb, 2)
    S = 5
    g = Image.fromarray(rgb).resize((W * S, H * S), Image.NEAREST)
    pane = Image.new("RGB", (W * S + 520, H * S), (24, 18, 22))
    pane.paste(g, (0, 0))
    d = ImageDraw.Draw(pane)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)
        small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 11)
    except OSError:
        font = small = ImageFont.load_default()
    for gx in range(GRID_W):
        for gy in range(GRID_H):
            x, y = cell_px(gx, gy)
            d.rectangle([x * S, y * S, x * S + 8 * S - 1, y * S + 8 * S - 1], outline=(70, 56, 56))
    for (gx, gy), code in CELLS.items():
        if code not in SECTIONS or code in ("~~",):
            continue
        col = KIND_COLOR[SECTIONS[code][1]]
        x, y = cell_px(gx, gy)
        d.rectangle([x * S + 1, y * S + 1, x * S + 8 * S - 2, y * S + 8 * S - 2], outline=col, width=2)
        tw = d.textlength(code, font=font)
        bx, by = x * S + (8 * S - tw) / 2, y * S + 8 * S - 17
        d.rectangle([bx - 2, by - 1, bx + tw + 1, by + 14], fill=(16, 12, 14))
        d.text((bx, by), code, fill=col, font=font)
    nm = names()
    x0, y = W * S + 12, 8
    for code, (suffix, kind) in SECTIONS.items():
        d.text((x0, y), code, fill=KIND_COLOR[kind], font=font)
        d.text((x0 + 26, y), nm.get("MAPSEC_" + suffix, suffix).title(), fill=(220, 210, 196), font=small)
        y += 14
        if y > H * S - 20:
            x0, y = x0 + 172, 8
    pane.save(IMG / "chart_grid.png")
    print("wrote design/oikoumene/img/chart_grid.png")


if __name__ == "__main__":
    import sys
    canvas, terrain = paint()
    check(terrain)
    if "--dry" in sys.argv:     # paint, count and preview only
        for lean, name in enumerate(LEAN_NAMES):
            print(f"Oikoumene chart, {name}: {len(cut(paint(lean)[0])[0])} unique tiles")
    else:
        write_outputs()
        write_sections()
    preview(canvas)
