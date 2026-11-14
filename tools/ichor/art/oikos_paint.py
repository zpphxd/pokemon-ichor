#!/usr/bin/env python3
"""Paint oikos, Ichor's Greek interior primary, from vanilla Building.

Building, the vanilla interior primary, holds only 8 metatiles: the void
(0x000-0x001), the TV (0x002-0x003), the PC (0x004-0x005) and the exit mat
(0x006-0x007). Floors, walls and furniture all live in the Hoenn secondaries,
which also point at about 20 of Building's tiles by index. So oikos does two
things, both without moving anything a secondary uses:

1. Repaints in place, at the same tile indices: the TV becomes Mom's loom, the
   PC becomes the Pithos, the exit mat a woven rush mat, and primary palettes
   0, 1 and 5 move to the master palette (design/phase1/PLAN.md).
2. Adds a Greek interior kit as new primary metatiles from 0x008, drawn only
   into tile slots and palettes (2-4) that no secondary uses: terracotta and
   marble floors, lime-plastered walls with a meander frieze and red dado,
   beams, shuttered windows, doorways, stairs, kline, klismos, tables, shelves,
   amphorae, pithoi, a loom, the hearth, lamps, a brazier, a Doric column and
   more. Free-standing pieces repeat at id + 0x40 on the other floor. Interiors
   redrawn later can be built from these directly; design/phase1/TILES_oikos.md
   lists every id.

Every tile is drawn below as a character grid, one character per pixel, with a
legend per palette. The script writes the Porymap assets in
data/tilesets/primary/oikos/porytiles_bin, then runs `porytiles
decompile-tileset` so Porytiles' own sources match, and a `compile-tileset`
that must change nothing (porytiles/tilesets/gTileset_Oikos/config.yaml keeps
tiles in patch mode and palettes locked). Finally it checks that every tile a
Hoenn secondary uses is unchanged unless it is one of the repaints above.

Usage: /usr/bin/python3 tools/ichor/art/oikos_paint.py [--no-porytiles]
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
VANILLA = ROOT / "data/tilesets/primary/building"
OUT = ROOT / "data/tilesets/primary/oikos/porytiles_bin"
TILESET = "gTileset_Oikos"

MB_NORMAL = 0x00
MB_SOUTH_ARROW_WARP = 0x65
MB_PC = 0x83
MB_TELEVISION = 0x86
NORMAL, COVERED = 0, 1   # metatile layer types

# --- Palettes ----------------------------------------------------------------
# Master palette families (PLAN.md); every value is a multiple of 8.
INK = (32, 24, 24)
TERRA_D, TERRA, TERRA_L, TERRA_P = (120, 48, 24), (184, 88, 48), (224, 136, 88), (240, 184, 136)
MARBLE_D, MARBLE, MARBLE_L = (168, 160, 152), (216, 208, 192), (248, 248, 240)
AEGEAN_D, AEGEAN, AEGEAN_L, AEGEAN_P = (24, 56, 120), (48, 104, 176), (112, 168, 224), (176, 216, 240)
GOLD_D, GOLD = (200, 144, 40), (240, 192, 64)
LIME_D, LIME, LIME_L = (176, 144, 96), (208, 184, 136), (232, 216, 176)
OLIVE_D, OLIVE, OLIVE_L = (56, 72, 32), (96, 112, 48), (144, 160, 72)
WOOD_D, WOOD, WOOD_L = (72, 48, 32), (128, 88, 48), (176, 128, 72)
BLACK = (0, 0, 0)

# Palette 0 keeps vanilla's roles: 0 is the backdrop, 1-4 the outline and the
# light-to-white ramp that the secondaries' object caps use, 10-12 glass, 13
# brass. 5-9, 14 and 15 only colored Building's own TV and PC, now redrawn.
PAL0 = [BLACK, INK, (136, 120, 104), (200, 192, 176), MARBLE_L, TERRA_D, TERRA,
        LIME, LIME_L, TERRA_L, AEGEAN_D, AEGEAN, AEGEAN_L, GOLD, WOOD, WOOD_D]
KEY0 = {".": 0, "#": 1, "s": 2, "m": 3, "P": 4, "R": 5, "r": 6, "l": 7, "c": 8,
        "o": 9, "B": 10, "b": 11, "a": 12, "y": 13, "w": 14, "W": 15}

# Palette 1: the exit mat (and Frontier pieces that keep vanilla's roles:
# outline, gray ramp, orange ramp). 5-8 and 13-15 were unused red filler.
PAL1 = [BLACK, INK, WOOD, LIME_D, LIME_L, BLACK, BLACK, BLACK, BLACK,
        TERRA_D, TERRA, TERRA_L, LIME, BLACK, BLACK, BLACK]
KEY1 = {".": 0, "#": 1, "w": 2, "v": 3, "u": 4, "R": 9, "r": 10, "o": 11, "l": 12}

# Palette 2, clay and wood: terracotta floors, furniture, pots, plants, cloth.
PAL2 = [BLACK, INK, TERRA_D, TERRA, TERRA_L, TERRA_P, WOOD_D, WOOD, WOOD_L,
        AEGEAN_D, OLIVE_D, OLIVE, OLIVE_L, GOLD, LIME_L, AEGEAN]
KEY2 = {".": 0, "#": 1, "R": 2, "r": 3, "o": 4, "p": 5, "W": 6, "w": 7, "v": 8,
        "B": 9, "G": 10, "g": 11, "l": 12, "y": 13, "c": 14, "b": 15}

# Palette 3, lime plaster and fresco: walls, beams, windows, doorways, stairs.
PAL3 = [BLACK, INK, (184, 168, 144), (224, 216, 192), (248, 240, 224), TERRA_D,
        TERRA, GOLD_D, AEGEAN_D, AEGEAN, AEGEAN_L, AEGEAN_P, WOOD_D, WOOD,
        WOOD_L, (96, 80, 64)]
KEY3 = {".": 0, "#": 1, "s": 2, "m": 3, "P": 4, "R": 5, "r": 6, "y": 7, "B": 8,
        "b": 9, "a": 10, "k": 11, "W": 12, "w": 13, "v": 14, "d": 15}

# Palette 4, marble, bronze and fire: marble floors, columns, statue, braziers,
# lamps, the hearth.
PAL4 = [BLACK, INK, MARBLE_D, MARBLE, MARBLE_L, (128, 120, 112), WOOD_D,
        (168, 112, 48), GOLD_D, TERRA, TERRA_L, GOLD, (248, 240, 200), AEGEAN,
        AEGEAN_D, OLIVE]
KEY4 = {".": 0, "#": 1, "M": 2, "m": 3, "P": 4, "n": 5, "Z": 6, "z": 7, "x": 8,
        "f": 9, "F": 10, "y": 11, "e": 12, "b": 13, "B": 14, "g": 15}

# Palette 5 keeps vanilla's roles (white, sky blues, sand, and black in 15 for
# the void fill) for the secondaries that use it; shades move to the master
# palette.
PAL5 = [(24, 40, 80), MARBLE_L, (232, 232, 224), AEGEAN_P, AEGEAN_L, MARBLE_D,
        (104, 96, 96), (56, 48, 48), AEGEAN_D, (136, 192, 232), (80, 136, 200),
        LIME_L, LIME, LIME_D, GOLD_D, BLACK]

PALETTES = {0: PAL0, 1: PAL1, 2: PAL2, 3: PAL3, 4: PAL4, 5: PAL5}
KEYS = {0: KEY0, 1: KEY1, 2: KEY2, 3: KEY3, 4: KEY4}


# --- Drawing helpers -----------------------------------------------------------

def grid(rows, pal, w=16, h=16):
    """Character rows -> index array, checked against size and legend."""
    key = KEYS[pal]
    assert len(rows) == h, f"{len(rows)} rows, want {h}: {rows[:2]}"
    for r in rows:
        assert len(r) == w, f"row {r!r} is {len(r)} wide, want {w}"
        bad = set(r) - set(key)
        assert not bad, f"row {r!r}: {bad} not in palette {pal}"
    return np.array([[key[c] for c in r] for r in rows], np.uint8)


class Canvas:
    """A character grid for objects bigger than one metatile."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [["."] * w for _ in range(h)]

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def stamp(self, x0, y0, rows):
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c != ".":
                    self.px(x0 + x, y0 + y, c)

    def rows(self):
        return ["".join(r) for r in self.g]


def tile8(rows):
    assert len(rows) == 8 and all(len(r) == 8 for r in rows), rows
    return rows


def join_tiles(tl, tr, bl, br):
    return [a + b for a, b in zip(tl, tr)] + [a + b for a, b in zip(bl, br)]


def recolor(rows, mapping, where=lambda x, y: True):
    return ["".join(mapping.get(c, c) if where(x, y) else c for x, c in enumerate(r))
            for y, r in enumerate(rows)]


def hflip(rows):
    return [r[::-1] for r in rows]


MEANDER = [  # the same running key as the pottery UI (ui_frames.py)
    "#####.##",
    "....#.#.",
    ".####.#.",
    ".#....#.",
    ".######.",
]


def band(motif, ink, ground, reps=2):
    return ["".join(ground if c == "." else ink for c in row) * reps for row in motif]


# --- 1. Vanilla repaints (same tile indices) ------------------------------------

# 0x002 TV (off) -> Mom's warp-weighted loom: cloth beam, woven Aegean cloth with
# a gold-and-red band, the shed rod, warp threads and clay loom weights.
LOOM = grid([
    "#W#WWWWWWWWWW#W#",
    "#w" + "l" * 12 + "w#",
    "#wWWWWWWWWWWWWw#",
    "#wBBBBBBBBBBBBw#",
    "#wbbbbbbbbbbbbw#",
    "#wyRyRyRyRyRyRw#",
    "#wbbbbbbbbbbbbw#",
    "#wbabbbabbbabbw#",
    "#wbbbbbbbbbbbbw#",
    "#wccccccccccccw#",
    "#wWWWWWWWWWWWWw#",
    "#wcscscscscscsw#",
    "#wcscscscscscsw#",
    "#woosoosoosoosw#",
    "#wrrsrrsrrsrrsw#",
    "#WRRsRRsRRsRRsW#",
], 0)

# 0x003 TV (on) -> the loom mid-weave: more cloth, a fresh red stripe at the
# fell and the gold shuttle in the shed. (Oikos has no tile animation.)
LOOM_ON = grid([
    "#W#WWWWWWWWWW#W#",
    "#w" + "l" * 12 + "w#",
    "#wWWWWWWWWWWWWw#",
    "#wBBBBBBBBBBBBw#",
    "#wbbbbbbbbbbbbw#",
    "#wyRyRyRyRyRyRw#",
    "#wbbbbbbbbbbbbw#",
    "#wbabbbabbbabbw#",
    "#wbbbbbbbbbbbbw#",
    "#w" + "o" * 12 + "w#",
    "#wccccccccccccw#",
    "#wWyyyyWscscscw#",
    "#wcscscscscscsw#",
    "#woosoosoosoosw#",
    "#wrrsrrsrrsrrsw#",
    "#WRRsRRsRRsRRsW#",
], 0)

# 0x004 PC (off) -> the Pithos: a great storage jar against the plastered wall,
# rope-pattern bands, the lid sealed with gold wax.
PITHOS = grid([
    "mmmm########mmmm",
    "mmm#RRRyyRRR#mmm",
    "mmm#ooooorrR#mmm",
    "mmmm#RRRRRR#mmmm",
    "mm#oorrrrrrrR#mm",
    "m#oRoRoRoRoRRR#m",
    "m#cooorrrrrrRR#m",
    "m#coorrrrrrrRR#m",
    "m#oorrrrrrrrRR#m",
    "m#oRoRoRoRoRRR#m",
    "m#oorrrrrrrrRR#m",
    "m#oorrrrrrrRRR#m",
    "mm#orrrrrrrRR#mm",
    "sss#rrrrrrRR#sss",
    "ssss#RRRRRR#ssss",
    "sssss######sssss",
], 0)

# 0x005 PC (on) shares the jar's lower half; its upper half is the jar opened,
# the seal lifted and light rising from the mouth.
PITHOS_ON_TOP = grid([
    "mmmmmmmcmmmcmmmm",
    "mmmmmcmycyPcmmmm",
    "mmm#yyPPPPyy#mmm",
    "mmmm#RyyyyR#mmmm",
    "mm#oorrrrrrrR#mm",
    "m#oRoRoRoRoRRR#m",
    "m#cooorrrrrrRR#m",
    "m#coorrrrrrrRR#m",
], 0, h=8)

# 0x006-0x007 exit mat (tiles 9 and 10, drawn mirrored into a 32x16 mat):
# a woven rush mat with a terracotta border.
MAT_END = grid(tile8([
    "RRRRRRRR",
    "Rrrrrrrr",
    "RrRRRRRR",
    "RrRuulul",
    "RrRwvvwv",
    "RrRulluu",
    "RrRvwvvw",
    "RrRuulul",
]), 1, 8, 8)
MAT_MID = grid(tile8([
    "RRRRRRRR",
    "rrrrrrrr",
    "RRRRRRRR",
    "uuluuulu",
    "vwvvwvvw",
    "luulluul",
    "wvvwvvwv",
    "uuluuulu",
]), 1, 8, 8)


# --- 2. The kit ------------------------------------------------------------------
# Backgrounds first. Floors tile in every direction; walls tile left to right.

# Terracotta: long 16x8 tiles laid in running bond, so the floor reads as
# clay tiling without a busy grid. The lower course is offset by half a tile.
FLOOR_TERRA = [
    "pppppppppppppoor",
    "poooooooooooooor",
    "poooooooooooooor",
    "ooooooooooooooor",
    "ooooopooooooooor",
    "ooooooooooooooor",
    "oooooooooooooorr",
    "rrrrrrrrrrrrrrrR",
    "pppppoorpppppppp",
    "ooooooorpooooooo",
    "ooooooorpooooooo",
    "oooooooroooooooo",
    "oopooooroooooooo",
    "oooooooroooooooo",
    "oooooorroooooooo",
    "rrrrrrrRrrrrrrrr",
]

FLOOR_TERRA_WORN = [  # a cracked tile and a chipped edge
    "pppppppppppppoor",
    "poooooooooooooor",
    "pooRooooooooooor",
    "oooorRooooooooor",
    "oooooorRoooopoor",
    "oooooooorRooooor",
    "ooooooooooRroorr",
    "rrrrrrrrrrrrrrrR",
    "pppppoorpppppppp",
    "ooooooorpooooooo",
    "ooooooorpooooooo",
    "rooooooroooooooo",
    "RroooooroooRoooo",
    "ooooooorooooRooo",
    "oooooorroooooRoo",
    "rrrrrrrRrrrrrrrr",
]

DARKER = {"p": "o", "o": "r", "r": "R"}
# Floor right under a wall: the wall's cast shadow, dithered out.
FLOOR_TERRA_SHADOW = recolor(recolor(FLOOR_TERRA, DARKER, lambda x, y: y < 2),
                             DARKER, lambda x, y: y == 2 and x % 2 == 0)

FLOOR_MARBLE = [
    "PPPPPPPPPPPPPPPM",
    "PmmmmmmmmmmmmmmM",
    "PmmmmmmPmmmmmmmM",
    "PmmmmmmmMmmmmmmM",
    "PmmmmmmmmMmmmmmM",
    "PmmmmmmmmmMMmmmM",
    "PmmPmmmmmmmmMmmM",
    "PmmmPPmmmmmmmMmM",
    "PmmmmmPmmmmmmmmM",
    "PmmmmmmPmmmmmmmM",
    "PMmmmmmmmmmmmmmM",
    "PmMMmmmmmmmmmmmM",
    "PmmmMmmmmmmmPmmM",
    "PmmmmMmmmmmmmPmM",
    "PmmmmmmmmmmmmmmM",
    "MMMMMMMMMMMMMMMn",
]

FLOOR_MARBLE_INLAY = [  # opus sectile: an Aegean lozenge set in the slab
    "PPPPPPPPPPPPPPPM",
    "PmmmmmmmmmmmmmmM",
    "PmmmmmmBBmmmmmmM",
    "PmmmmmBbbBmmmmmM",
    "PmmmmBbbbbBmmmmM",
    "PmmmBbbPPbbBmmmM",
    "PmmBbbPmmPbbBmmM",
    "PmBbbPmMMmPbbBmM",
    "PmBbbPmMMmPbbBmM",
    "PmmBbbPmmPbbBmmM",
    "PmmmBbbPPbbBmmmM",
    "PmmmmBbbbbBmmmmM",
    "PmmmmmBbbBmmmmmM",
    "PmmmmmmBBmmmmmmM",
    "PmmmmmmmmmmmmmmM",
    "MMMMMMMMMMMMMMMn",
]

FLOOR_MARBLE_SHADOW = recolor(recolor(FLOOR_MARBLE, {"P": "m", "m": "M", "M": "n"}, lambda x, y: y < 2),
                              {"P": "m", "m": "M"}, lambda x, y: y == 2 and x % 2 == 0)

FLOOR_MARBLE_MEANDER = (["PPPPPPPPPPPPPPPP", "mmmmmmmmmmmmmmmm", "MMMMMMMMMMMMMMMM",
                         "mmmmmmmmmmmmmmmm"]
                        + band(MEANDER, "B", "m")
                        + ["mmmmmmmmmmmmmmmm", "MMMMMMMMMMMMMMMM", "PPPPPPPPPPPPPPPP",
                           "mmmmmmmmmmmmmmmm", "mmmmmmmmmmmmmmmm", "mmmmmmmmmmmmmmmm",
                           "MMMMMMMMMMMMMMMM"])

_H = ["cccc", "vvvv", "cccc", "wwww"]
_V = ["cvcw"] * 4
FLOOR_RUSH = ["".join((_H if (bx + by) % 2 == 0 else _V)[y % 4] for bx in range(4))
              for by in range(4) for y in range(4)]

# Walls (palette 3). Upper course: a squared ceiling beam over lime plaster.
PLASTER = [
    "mmmmmmmmmmmmmmmm",
    "mmmmPmmmmmmmmmmm",
    "mmmmmmmmmmmsmmmm",
    "mmmmmmmmmmmmmmmm",
    "mPmmmmmmmmmmmmPm",
    "mmmmmmmmsmmmmmmm",
    "mmmmmmmmmmmmmmmm",
    "mmmmmmPmmmmmmmmm",
    "mmmmmmmmmmmmmmmm",
    "mmmsmmmmmmmmmmmm",
    "mmmmmmmmmmmmPmmm",
    "mmmmmmmmmmmmmmmm",
    "mmmmmPmmmmmmmmmm",
    "mmmmmmmmmmmmmsmm",
    "mmmmmmmmmmmmmmmm",
    "mmmmmmmmmmPmmmmm",
]

BEAM = [
    "WWWWWWWWWWWWWWWW",
    "vvvvvvvwvvvvvvvv",
    "wwwvwwwwwwwwvwww",
    "wwwwwwWwwwwwwwww",
    "WWWWWWWWWWWWWWWW",
    "ssssssssssssssss",
    "msmsmsmsmsmsmsms",
]
WALL_UPPER_BEAM = BEAM + PLASTER[7:]
WALL_UPPER = PLASTER

# Lower course: plaster, a black-on-ochre meander frieze between oxblood
# lines, a red dado and a dark skirting.
DADO = ["rrrrrrrrrrrrrrrr", "rrrrrrrrrrrrrrrr", "rrrrrrrrrrrrrrrr",
        "rRrrrrrrrRrrrrrr", "RRRRRRRRRRRRRRRR", "dddddddddddddddd"]
WALL_LOWER_FRIEZE = PLASTER[:4] + ["RRRRRRRRRRRRRRRR"] + band(MEANDER, "#", "y") + \
    ["RRRRRRRRRRRRRRRR"] + DADO[1:]
WALL_LOWER = PLASTER[:9] + ["RRRRRRRRRRRRRRRR"] + DADO[:4] + DADO[4:]

# Fresco panel: a running wave in Aegean on the plaster.
WAVE = [  # running wave (Vitruvian scroll): crests curl over to the right
    "kkkkBBkk",
    "kkkBbbBk",
    "kkBbkkbB",
    "kBbbBkbB",
    "Bbbbbbbb",
    "bbbbbbbb",
]
WALL_UPPER_FRESCO = PLASTER[:5] + ["B" * 16] + [r * 2 for r in WAVE] + ["B" * 16] + PLASTER[13:]

# A lamp niche cut into the plaster; the lamp itself is a separate layer.
WALL_NICHE = [
    "mmmmmmmmmmmmmmmm",
    "mmmmmPmmmmmmmmmm",
    "mmmmmmssssmmmmmm",
    "mmmmmsddddsmmmmm",
    "mmmmsddddddPmmmm",
    "mmmsddddddddPmmm",
    "mmmsddddddddPmmm",
    "mmmsddddddddPmmm",
    "mmmsddddddddPmmm",
    "mmmsddddddddPmmm",
    "mmmsddddddddPmmm",
    "mmmsddddddddPmmm",
    "mmmPPPPPPPPPPmmm",
    "mmmssssssssssmmm",
    "mmmmmmmmmmmmmmmm",
    "mmmmmmmmsmmmmmmm",
]
NICHE_LAMP = [  # palette 4: a clay oil lamp, flame at the nozzle
    "................",
    "................",
    "................",
    "................",
    "................",
    "..........e.....",
    ".........yey....",
    ".........FyF....",
    "..........f.....",
    "....#####.#.....",
    "...#FFFFF#f#....",
    "...#fFFfffff#...",
    "....#########...",
    "................",
    "................",
    "................",
]

WINDOW_SHUT = [  # Cycladic blue shutters, latched
    "mmmmmmmmmmmmmmmm",
    "mWWWWWWWWWWWWWWm",
    "mWwvwwwwwwwwwwWm",
    "mmsBBBBBBBBBBPmm",
    "mmsBaaaBBaaaBPmm",
    "mmsBbbbBBbbbBPmm",
    "mmsBaaaBBaaaBPmm",
    "mmsBbbbBBbbbBPmm",
    "mmsBaaayyaaaBPmm",
    "mmsBbbbBBbbbBPmm",
    "mmsBaaaBBaaaBPmm",
    "mmsBbbbBBbbbBPmm",
    "mmsBBBBBBBBBBPmm",
    "mPPPPPPPPPPPPPPm",
    "mssssssssssssssm",
    "mmmmmmmmmmmmmmmm",
]

WINDOW_OPEN = [  # shutters folded back: sky, a cloud, the sea and an island
    "mmmmmmmmmmmmmmmm",
    "mWWWWWWWWWWWWWWm",
    "mWwvwwwwwwwwwwWm",
    "BbskkkkkkkkkkPbB",
    "BaskkkkkkkkkkPaB",
    "BbskkkkkPkkkkPbB",
    "BaskkkkPPPkkkPaB",
    "BbskkkkkkkkkkPbB",
    "BaskkkkkkkkkkPaB",
    "BbsaaaaayyaaaPbB",
    "BasaaaaaaaaaaPaB",
    "BbsbbbbbbbbbbPbB",
    "BasbbbbbbbbbbPaB",
    "BbPPPPPPPPPPPPbB",
    "BBssssssssssssBB",
    "mmmmmmmmmmmmmmmm",
]

DOORWAY_TOP = [  # timber lintel over a dark opening
    "mmmmmmmmmmmmmmmm",
    "mmmmPmmmmmmmmmmm",
    "mWWWWWWWWWWWWWWm",
    "mWvvvvvvvvvvvvWm",
    "mWwwwwwwwwwwwwWm",
    "mWWWWWWWWWWWWWWm",
    "mms##########Pmm",
    "mms##########Pmm",
    "mms##########Pmm",
    "mms#WWWWWWWW#Pmm",
    "mms#WWWWWWWW#Pmm",
    "mms#WWWWWWWW#Pmm",
    "mms#WWWWWWWW#Pmm",
    "mms#WWWWWWWW#Pmm",
    "mms#WWWWWWWW#Pmm",
    "mms#WWWWWWWW#Pmm",
]
def lower_opening(mid):
    """A lower-course cell with an opening: the frieze and dado run up to the
    jambs, and the opening ends in a lit stone sill."""
    sill = ["PPPPPPPPPPPP", "mmmmmmmmmmmm", "ssssssssssss"]
    return [WALL_LOWER_FRIEZE[y][:2] + (mid[y] if y < 13 else sill[y - 13]) + WALL_LOWER_FRIEZE[y][14:]
            for y in range(16)]


DOORWAY_BOTTOM = lower_opening(["s#WWWWWWWW#P"] * 13)

_STEPS = [  # treads (lit) and risers, darker the higher they climb
    "##########", "##########", "WWWWWWWWWW", "##########", "wwwwwwwwww",
    "WWWWWWWWWW", "##########", "vvvvvvvvvv", "wwwwwwwwww", "WWWWWWWWWW",
    "##########", "vvvvvvvvvv", "vvvvvvvvvv", "wwwwwwwwww", "WWWWWWWWWW",
    "##########", "vvvvvvvvvv", "vvvvvvvvvv", "wwwwwwwwww", "wwwwwwwwww",
    "WWWWWWWWWW", "##########", "vvvvvvvvvv",
]
STAIRS_UP_TOP = DOORWAY_TOP[:6] + ["mms" + s + "Pmm" for s in _STEPS[:10]]
STAIRS_UP_BOTTOM = lower_opening(["s" + s + "P" for s in _STEPS[10:23]])

WALL_POST_UPPER = [r[:6] + "WvwW" + r[10:] for r in WALL_UPPER_BEAM]
WALL_POST_LOWER = [r[:6] + "WvwW" + r[10:] for r in WALL_LOWER_FRIEZE[:15]] + ["ddddddWWWWdddddd"]

STAIRS_DOWN = [  # palette 2: a stair opening in the terracotta floor
    "pppppppppppppppr",
    "pRRRRRRRRRRRRRRr",
    "pR############Rr",
    "pR#cccccccccc#Rr",
    "pR#vvvvvvvvvv#Rr",
    "pR#WWWWWWWWWW#Rr",
    "pR#cccccccccc#Rr",
    "pR#vvvvvvvvvv#Rr",
    "pR#WWWWWWWWWW#Rr",
    "pR#wwwwwwwwww#Rr",
    "pR#WWWWWWWWWW#Rr",
    "pR############Rr",
    "pR#WWWWWWWWWW#Rr",
    "pR############Rr",
    "pRRRRRRRRRRRRRRr",
    "rrrrrrrrrrrrrrrR",
]

THRESHOLD = [  # palette 4: a worn marble door-step, the room's exit
    "nnnnnnnnnnnnnnnn",
    "MMMMMMMMMMMMMMMM",
    "PPPPPPPPPPPPPPPP",
    "PmmmmmmmmmmmmmmM",
    "PmmmmmPPPmmmmmmM",
    "PmmmmPPmPPmmmmmM",
    "PmmmmmPPPmmmmmmM",
    "PmmmmmmmmmmmmmmM",
    "PmmmmmmmmmmmmmmM",
    "MMMMMMMMMMMMMMMM",
    "MmmmmmmmmmmmmmMn",
    "MMMMMMMMMMMMMMMn",
    "nnnnnnnnnnnnnnnn",
    "################",
    "................",
    "................",
]

# --- Furniture (object layers; '.' shows the floor or wall underneath) -------------

def kline():
    """Couch-bed, 2x2: raised head end with a gold medallion, cushion, Aegean
    cover, linen throw at the foot, painted rail and turned legs."""
    c = Canvas(32, 32)
    c.rect(4, 27, 29, 28, "r")                        # shadow on the floor
    leg = [".#W#.", "#vwW#", ".#w#.", ".#v#.", "#vwW#", ".#w#.", ".###."]
    c.stamp(2, 22, leg)
    c.stamp(25, 22, leg)
    c.rect(1, 18, 30, 18, "#")                         # front rail
    c.rect(1, 19, 30, 22, "w")
    c.rect(2, 19, 29, 19, "v")
    c.rect(1, 22, 30, 22, "W")
    c.rect(1, 23, 30, 23, "#")
    c.px(0, 19, "#"), c.px(0, 20, "#"), c.px(0, 21, "#"), c.px(0, 22, "#")
    c.px(31, 19, "#"), c.px(31, 20, "#"), c.px(31, 21, "#"), c.px(31, 22, "#")
    for x in range(4, 29, 4):
        c.px(x, 20, "y")
        c.px(x + 1, 21, "R")
    c.rect(4, 7, 29, 7, "#")                           # back rail
    c.rect(4, 8, 29, 9, "w")
    c.rect(4, 8, 29, 8, "v")
    c.rect(4, 10, 30, 17, "b")                         # mattress cover
    c.rect(4, 10, 30, 10, "B")
    c.rect(29, 10, 30, 17, "B")
    c.rect(4, 16, 30, 17, "B")
    for x in range(5, 30, 2):
        c.px(x, 17, "y")                               # fringe
    c.rect(22, 10, 28, 15, "c")                        # folded linen throw
    c.rect(22, 15, 28, 15, "R")
    c.rect(22, 12, 28, 12, "R")
    c.rect(28, 10, 28, 15, "R")
    c.stamp(5, 8, [                                    # striped linen cushion
        "..#####..",
        ".#ccycc#.",
        "#cccyccv#",
        "#cccycvv#",
        "#ccvyvvv#",
        ".#vvyvv#.",
        "..#####..",
    ])
    c.stamp(0, 3, [                                    # head end
        ".####.",
        "#vvvv#",
        "#vyyw#",
        "#vyyw#",
        "#vwwW#",
        "#vwW#.",
        "#vwW#.",
        "#vwW#.",
        "#vwW#.",
        "#vwW#.",
        "#vwW#.",
        "#vwW#.",
        "#vwW#.",
        "#vwW#.",
        "#vwW#.",
        "#####.",
    ])
    c.stamp(29, 6, ["###", "#v#", "#w#", "#w#", "#w#", "#w#", "#w#", "#w#",
                    "#w#", "#w#", "#w#", "#w#", "#W#"])  # foot post
    return c.rows()


def shelf():
    """Scroll shelf, 2x2, against the wall: pigeonholes of scroll ends, with
    two small jars on top."""
    c = Canvas(32, 32)
    c.stamp(5, 0, [".##.", "#oo#", "#or#", ".##."])
    c.stamp(23, 0, ["..##..", ".#oo#.", "#cBBo#", "#oorR#", ".####."])
    c.rect(1, 4, 30, 31, "#")
    c.rect(2, 5, 29, 6, "v")
    c.rect(2, 7, 29, 7, "W")
    for row_y in (8, 18):
        c.rect(2, row_y, 29, row_y + 8, "W")
        for col in range(4):
            x0 = 3 + col * 7
            c.rect(x0, row_y, x0 + 5, row_y + 7, "#")
            for sx, sy in ((0, 1), (3, 1), (1, 4), (4, 4)):
                c.stamp(x0 + sx, row_y + sy, ["cc", "cv"])
        c.rect(2, row_y + 8, 29, row_y + 8, "v")
        c.rect(2, row_y + 9, 29, row_y + 9, "w")
    c.rect(2, 28, 29, 29, "w")
    c.rect(2, 28, 29, 28, "v")
    c.rect(2, 30, 3, 31, "W"), c.rect(28, 30, 29, 31, "W")
    for x in (1, 30):
        c.rect(x, 4, x, 31, "#")
    c.rect(2, 8, 2, 29, "w"), c.rect(29, 8, 29, 29, "W")
    return c.rows()


def amphora_rack():
    """Wine rack, 2x2: three amphorae standing in a pierced board."""
    c = Canvas(32, 32)
    amph = [  # transport amphora: loop handles, black bands, a pointed toe
        "...####...",
        "..#oppo#..",
        "...#or#...",
        ".###or###.",
        ".#.#or#.#.",
        ".#.#or#.#.",
        ".#ooorrR#.",
        "#poorrrrR#",
        "#ooorrrrR#",
        "##########",
        "#ooorrrrR#",
        "##########",
        "#ooorrrrR#",
        "#ooorrrRR#",
        ".#oorrrR#.",
        ".#oorrRR#.",
        "..#orrR#..",
        "..#orRR#..",
        "...#rR#...",
        "...#RR#...",
        "....##....",
    ]
    for i, x in enumerate((1, 11, 21)):
        c.stamp(x, 2 + (i % 2), amph)
    c.rect(0, 16, 31, 16, "#")                          # pierced board
    c.rect(0, 17, 31, 18, "v")
    c.rect(0, 19, 31, 19, "W")
    c.rect(0, 20, 31, 20, "#")
    for x in (5, 15, 25):
        c.rect(x, 17, x + 1, 18, "R")
    for x in (1, 29):                                   # legs
        c.rect(x, 21, x + 1, 31, "w")
        c.px(x - 1 if x > 1 else x + 2, 21, "#")
    c.stamp(1, 21, ["#w#", "#w#", "#w#", "#w#", "#w#", "#w#", "#w#", "#w#", "#w#", "#W#", "###"])
    c.stamp(28, 21, ["#w#", "#w#", "#w#", "#w#", "#w#", "#w#", "#w#", "#w#", "#w#", "#W#", "###"])
    c.rect(4, 26, 27, 27, "W")                          # lower stretcher
    c.rect(4, 25, 27, 25, "#"), c.rect(4, 28, 27, 28, "#")
    return c.rows()


OLIVE_POT = [  # 1x2: an olive sapling in a black-figure pot (palette 2)
    "....##..###.....",
    "..##lc##llc#....",
    ".#lcllggllccl#..",
    "#llggllclggll#..",
    "#lgGglllgGgllc#.",
    ".#gGGgllggGgcl#.",
    "#lcgGggllgGGgl#.",
    "#llcggGggGggll#.",
    ".#lgGgg#wgGgll#.",
    "..#gg#.#w#GGg#..",
    "...##..#wW#g#...",
    "........#wW##...",
    ".......#wW#.....",
    ".......#ww#.....",
    "........#wW#....",
    "........#wW#....",
    # pot
    "....#########...",
    "...#RRRRRRRRR#..",
    "...#poooooorR#..",
    "....#ooooorR#...",
    "...#o#######R#..",
    "...#o#o#o#o#R#..",
    "...#o#######R#..",
    "...#ooooorrRR#..",
    "....#oooorrR#...",
    "....#ooorrRR#...",
    ".....#oorrR#....",
    ".....#orrRR#....",
    "......#####.....",
    ".....rrrrrrr....",
    "................",
    "................",
]

LAMPSTAND = [  # 1x2, palette 4: a bronze lampstand with a lit oil lamp
    "................",
    ".......e........",
    "......yey.......",
    "......yey.......",
    ".....yFeFy......",
    "......FyF.......",
    ".......f........",
    "...##########...",
    "..#xxxxxxxxzZ#..",
    "...#zzzzzzzZ#...",
    "....###xz###....",
    ".......xz.......",
    "......#xz#......",
    "......#xZ#......",
    "......#xZ#......",
    "......#xZ#......",
    "......#xZ#......",
    "......#xZ#......",
    ".....##xZ##.....",
    "....#xzzzZZ#....",
    ".....##xZ##.....",
    "......#xZ#......",
    "......#xZ#......",
    "......#xZ#......",
    "......#xZ#......",
    "......#xZ#......",
    ".....#xzzZ#.....",
    "....#xz##zZ#....",
    "...#xz#..#zZ#...",
    "..#xz#....#zZ#..",
    "..###......###..",
    "................",
]


def hearth():
    """The family hearth, 2x2 (palette 4): a ring of stones round banked
    embers, with a bronze pot on its tripod."""
    c = Canvas(32, 32)
    cx, cy, r_out, r_in = 15.5, 17.5, 14.5, 9.5
    for y in range(32):
        for x in range(32):
            d = ((x - cx) ** 2 + ((y - cy) * 1.25) ** 2) ** 0.5
            if d <= r_out:
                if d > r_in:
                    ang = np.arctan2(y - cy, x - cx)
                    seg = int((ang + np.pi) / (2 * np.pi) * 16)
                    if r_out - d < 1.2 or d - r_in < 1.0:
                        ch = "#"
                    elif seg % 2 == 0:
                        ch = "m" if y < cy else "M"
                    else:
                        ch = "P" if y < cy - 3 else ("m" if y < cy + 3 else "M")
                    if abs(((ang + np.pi) / (2 * np.pi) * 16) % 1) < 0.08:
                        ch = "n"
                else:
                    ch = "n"
                c.px(x, y, ch)
    embers = [
        "....f.F.f.....",
        "..fFfyFfFfF...",
        ".FyeyFfyFyFf..",
        "fFyeeyFyeyFf..",
        ".fFyyFfFyFf...",
        "..fnfFfnfFn...",
        "...n.nfn.n....",
    ]
    c.stamp(9, 15, embers)
    c.stamp(10, 7, [  # bronze pot on a tripod, steam rising
        "....P..P....",
        ".....P.P....",
        "...#######..",
        "..#xxxxxxzZ#",
        "..#xzzzzzzZ#",
        "...#zzzzzZ#.",
        "....#ZZZZ#..",
        "...#..#..#..",
        "..#...#...#.",
    ])
    return c.rows()


COLUMN = [  # 1x3, palette 4: Doric capital, fluted shaft, base on the floor
    "################",
    "#PPPPPPPPPPPPPM#",
    "#mmmmmmmmmmmmmM#",
    "################",
    ".#PPPPPPPPPPmM#.",
    "..#PPmmmmmmmM#..",
    "...##########...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
] + ["...#PmPmmMmM#..."] * 16 + [
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "...#PmPmmMmM#...",
    "..##PmPmmMmM##..",
    ".#PPPPPPPPPPmM#.",
    "#PPPPPPPPPPPPmM#",
    "#mmmmmmmmmmmmMM#",
    "################",
    "nnnnnnnnnnnnnnnn",
    "................",
]

STATUE = [  # 1x2, palette 4: Asclepius on a plinth, his snake round his staff
    "................",
    "......####......",
    ".....#PPPm#.....",
    ".....#PPmM#..#..",
    ".....#mMMn#..Z..",
    "......#Mn#...Z..",
    "...###mMMn###Z..",
    "..#PPPmmmmMn#Zg.",
    "..#PPmmmmmMnmZ#.",
    "..#PmmnmmmMn#Zg.",
    "..#PmmmnmmMngZ..",
    "..#PmmmmnmMn#Zg.",
    "..#PmmmmmnMngZ..",
    "..#PmmmmmmnM#Zg.",
    "..#PmmmmmmMngZ..",
    "..#PPmmmmmMn#Zg.",
    "..#PmmmmmmMngZ..",
    "..#PPmmmmmMn#Z..",
    "..#PmmmmmmMn#Z..",
    "..#PPmmmmmMM#Z..",
    "..#PmPmmmMMM#Z..",
    ".#PPmPmmmMMMn#Z.",
    ".##############.",
    ".#PPPPPPPPPPPPM#",
    ".#PmmmmmmmmmmMM#",
    ".#PmmmmmmmmmmMM#",
    ".#PmmmmmmmmmmMM#",
    ".#MMMMMMMMMMMMn#",
    ".##############.",
    "..nnnnnnnnnnnnn.",
    "................",
    "................",
]

PITHOS_TALL = [  # 1x2, palette 2: a storage jar taller than a child
    "................",
    "....########....",
    "...#RRRyyRRR#...",
    "...#pooooorR#...",
    "....#RRRRRR#....",
    "..##oorrrrrR##..",
    ".#ooorrrrrrrRR#.",
    "#oRoRoRoRoRoRRR#",
    "#poooorrrrrrrRR#",
    "#ppoorrrrrrrrRR#",
    "#pooorrrrrrrrRR#",
    "#ooorrrrrrrrrRR#",
    "#o###########RR#",
    "#o#o#o#o#o#o#RR#",
    "#o###########RR#",
    "#ooorrrrrrrrrRR#",
    "#ooorrrrrrrrRRR#",
    "#oRoRoRoRoRoRRR#",
    "#ooorrrrrrrrRRR#",
    "#ooorrrrrrrrRRR#",
    ".#oorrrrrrrRRR#.",
    ".#oorrrrrrrRRR#.",
    "..#orrrrrrRRR#..",
    "..#orrrrrrRRR#..",
    "...#rrrrrRRR#...",
    "....#rrrrRR#....",
    ".....#rrRR#.....",
    "....#WwwwwW#....",
    "....########....",
    "...rrrrrrrrrr...",
    "................",
    "................",
]

LOOM_TALL = [  # 1x2, palette 2: the standing loom, full height
    "#W#..........#W#",
    "#wW##########Ww#",
    "#wvvvvvvvvvvvvw#",
    "#wWWWWWWWWWWWWw#",
    "#wBBBBBBBBBBBBw#",
    "#wbbbbbbbbbbbbw#",
    "#wbbbbbbbbbbbbw#",
    "#wyRyRyRyRyRyRw#",
    "#wbbbbbbbbbbbbw#",
    "#wbbbbbbbbbbbbw#",
    "#wbcbbbcbbbcbbw#",
    "#wbbbbbbbbbbbbw#",
    "#wbbbbbbbbbbbbw#",
    "#wyRyRyRyRyRyRw#",
    "#wbbbbbbbbbbbbw#",
    "#wccccccccccccw#",
    "#wWWWWWWWWWWWWw#",
    "#wc.c.c.c.c.c.w#",
    "#wc.c.c.c.c.c.w#",
    "#wc.c.c.c.c.c.w#",
    "#wwwwwwwwwwwwww#",
    "#wWWWWWWWWWWWWw#",
    "#wc.c.c.c.c.c.w#",
    "#wc.c.c.c.c.c.w#",
    "#wc.c.c.c.c.c.w#",
    "#wro.ro.ro.ro.w#",
    "#wRr.Rr.Rr.Rr.w#",
    "#wRr.Rr.Rr.Rr.w#",
    "#w.R..R..R..R.w#",
    "#w............w#",
    "#W............W#",
    "##............##",
]

KLISMOS_FRONT = [
    "................",
    "................",
    "...##########...",
    "..#vvvvvvvvvv#..",
    "..#wwwwwwwwwW#..",
    "...##########...",
    "....#w#..#w#....",
    "..############..",
    "..#bbbbbbbbbB#..",
    "..#bbbbbbbbBB#..",
    "..#vvvvvvvvvv#..",
    "..#W#wwwwww#W#..",
    ".#W#.######.#W#.",
    ".#W#........#W#.",
    "#W#..........#W#",
    ".r............r.",
]

KLISMOS_SIDE = [  # facing right: the curved back on the left, saber legs
    "................",
    "..##............",
    ".#vw#...........",
    ".#vw#...........",
    "..#vw#..........",
    "..#vw#..........",
    "...#w#..........",
    "...#w#########..",
    "...#wbbbbbbbb#..",
    "...#vvvvvvvvvv#.",
    "...#W#wwwwww#W#.",
    "..#W#.......#W#.",
    "..#W#........#W#",
    ".#W#.........#W#",
    ".#W#.........#W#",
    ".rr...........rr",
]

TABLE = [  # trapeza: a three-legged table with bread and a kylix
    "................",
    "................",
    "....###...###...",
    "...#ppo#.#yyy#..",
    ".##############.",
    "#ccvvvvvvvvvvvv#",
    "#cvvvvvvvvvvvvw#",
    "#vvvvvvvvvvvvww#",
    "################",
    "#wwwwwwwwwwwwwW#",
    ".#W##########W#.",
    "..#w#..#w#..#w#.",
    "..#w#..#w#..#w#.",
    "..#v#..#v#..#v#.",
    ".#ww#.#ww#.#ww#.",
    ".rrr...rrr..rrr.",
]

STOOL = [  # diphros okladias: a folding stool with a cushion
    "................",
    "................",
    "................",
    "................",
    "................",
    "...##########...",
    "..#bbbbbbbbbB#..",
    "..#vvvvvvvvvv#..",
    "...##########...",
    "....#W#..#W#....",
    ".....#W##W#.....",
    "......#WW#......",
    ".....#W##W#.....",
    "....#W#..#W#....",
    "...#W#....#W#...",
    "...rr......rr...",
]

KIBOTOS = [  # wooden chest with a painted panel and brass fittings
    "................",
    "................",
    "................",
    "...##########...",
    "..#vvvvvvvvvv#..",
    ".#vvvvvvvvvvvw#.",
    ".#wwwwwwwwwwwW#.",
    ".######yy######.",
    ".#ww#rrrrrr#wW#.",
    ".#ww#rooooR#wW#.",
    ".#ww#roRRoR#wW#.",
    ".#ww#rrrrRR#wW#.",
    ".#yw########wy#.",
    ".##############.",
    "..#W#......#W#..",
    "..rrr......rrr..",
]

AMPHORA = [  # neck amphora: loop handles, a black belly band, black foot
    "......####......",
    ".....#oppo#.....",
    "......#or#......",
    "...####or####...",
    "...#..#or#..#...",
    "...#.#oorr#.#...",
    "...#oooorrrR#...",
    "..#poooorrrrR#..",
    "..#ooooorrrrR#..",
    "..############..",
    "..#oooooorrrR#..",
    "..############..",
    "...#oooorrrR#...",
    "....#oorrRR#....",
    "......####......",
    ".....rrrrrr.....",
]

KRATER = [  # column krater: dark mouth, loop handles, a meander round the body
    "................",
    "................",
    ".##############.",
    "#ppppppppppppoo#",
    "#oRRRRRRRRRRRRr#",
    "################",
    "##.#oooorrrR#.##",
    "#..##########..#",
    ".#.#oooo#o#o#.#.",
    "..##o####o#o##..",
    "...#o#oooo#o#...",
    "...#o######o#...",
    "....#oorrRR#....",
    ".....#orRR#.....",
    "......####......",
    ".....rrrrrr.....",
]

BRAZIER = [  # palette 4: a bronze tripod brazier, burning
    "......f.F.......",
    ".....FyfyF.f....",
    "....fyeeyFyF....",
    "...FyeeeeyyF....",
    "..fFyeeyyyFf....",
    "..############..",
    ".#xxxxxxxxxxzZ#.",
    "..#zzzzzzzzzZ#..",
    "...#ZzzzzzZZ#...",
    "....########....",
    "....#x#..#Z#....",
    "...#x#....#Z#...",
    "...#x#....#Z#...",
    "..#x#......#Z#..",
    "..##........##..",
    "..nn........nn..",
]

KLEPSYDRA = [  # palette 2: the water clock on its wall bracket
    "................",
    "...##########...",
    "...#RoooooorR#..",
    "....#oooorrR#...",
    ".....#orrRR#....",
    "......#rR#......",
    ".......#b.......",
    ".......bb.......",
    "........b.......",
    "...##########...",
    "...#bbbbbbbbB#..",
    "...#RoooooorR#..",
    "....#oooorrR#...",
    ".....#rrrRR#....",
    "..############..",
    "..#WwwwwwwwwW#..",
]

KNUCKLEBONES = [  # a low gaming table: knucklebones and a cup
    "................",
    "................",
    "................",
    "..#.......###...",
    ".#c#.#c#.#RRR#..",
    ".#cc##cc#.#R#...",
    ".############...",
    "#vvvvcvvvvvvvv#.",
    "#vcvvvvvvvvvcw#.",
    "#vvvvvvvvvvvww#.",
    "###############.",
    "#wwwwwwwwwwwwW#.",
    ".#W#.......#W#..",
    ".#W#.......#W#..",
    ".#W#.......#W#..",
    ".rr........rr...",
]

HERB_POT = [  # basil in a small clay pot
    "................",
    "................",
    "......##........",
    "....##lg##.#....",
    "...#lglgGl#g#...",
    "..#lgGlglgGlg#..",
    "..#glgGglGglG#..",
    "...#GgGglgGg#...",
    "....##GgGg##....",
    "....#RRRRRR#....",
    "...#poooorRR#...",
    "...#ooo#oRRR#...",
    "....#ooorRR#....",
    "....#oorrRR#....",
    ".....######.....",
    ".....rrrrrr.....",
]

def counter():
    """Market counter, 3x1 (palette 2): a scrubbed top over a front painted
    with a black-figure meander on terracotta."""
    c = Canvas(48, 16)
    c.rect(1, 2, 46, 2, "#")
    c.rect(0, 3, 47, 4, "v")
    c.rect(1, 3, 20, 3, "c")
    c.rect(0, 5, 47, 5, "#")
    c.rect(0, 6, 47, 14, "w")
    c.rect(46, 6, 46, 14, "W")
    c.rect(2, 7, 45, 13, "#")
    for y, row in enumerate(MEANDER):
        for x in range(3, 45):
            c.px(x, 8 + y, "#" if row[(x - 3) % 8] == "#" else "o")
    c.rect(0, 14, 47, 14, "W")
    for x in (0, 47):
        c.rect(x, 3, x, 14, "#")
    c.rect(0, 15, 47, 15, "#")
    return c.rows()


COUNTER = counter()

WALL_MAP = [  # 2x1, palette 3: a painted map of Aethos
    "................................",
    ".##############################.",
    ".#WWWWWWWWWWWWWWWWWWWWWWWWWWWW#.",
    ".#WbbbbbbbbbbbbbbbbbbbbbbbbbbW#.",
    ".#WbbbbbyyyybbbbbbbbbbbbbabbbW#.",
    ".#WbbbbyyyyyyybbbbbbbbbbbbbbbW#.",
    ".#WbbbyyyyyyyyybbbbbayybbbbbbW#.",
    ".#WbbbbyyyyyybbbbbbbyyyybbbbbW#.",
    ".#WbbbbbyyyybbbbbbbbbyybbbbbbW#.",
    ".#WbbbbbbbbbbbbbabbbbbbbbbbbbW#.",
    ".#WbbbabbbbbbbbbbbbbbbbbyybbbW#.",
    ".#WbbbbbbbbbbybbbbbbbbbbbybbbW#.",
    ".#WbbbbbbbbbbrbbbbbbbbbbbbbbbW#.",
    ".#WWWWWWWWWWWWWWWWWWWWWWWWWWWW#.",
    ".##############################.",
    "................................",
]

def spring():
    """The Asclepeion's marble basin of spring water, 2x1 (palette 4)."""
    c = Canvas(32, 16)
    c.rect(1, 1, 30, 1, "#")
    c.rect(0, 2, 31, 8, "#")
    c.rect(1, 2, 30, 7, "P")          # rim, lit
    c.rect(29, 2, 30, 7, "M")
    c.rect(3, 3, 28, 6, "b")          # water
    c.rect(3, 6, 28, 6, "B")
    c.rect(27, 3, 28, 6, "B")
    c.rect(3, 3, 26, 3, "B")          # the rim's shadow on the water
    for x, y in ((6, 4), (7, 4), (15, 5), (16, 5), (21, 4)):
        c.px(x, y, "e")
    c.rect(1, 8, 30, 8, "M")
    c.rect(0, 9, 31, 9, "#")
    c.rect(2, 10, 29, 12, "m")        # basin front, fluted
    for x in range(4, 28, 3):
        c.rect(x, 10, x, 12, "M")
    c.rect(2, 10, 2, 12, "P")
    c.rect(29, 10, 29, 12, "n")
    for x in (1, 30):
        c.rect(x, 10, x, 13, "#")
    c.rect(1, 13, 30, 13, "#")
    c.rect(2, 14, 29, 14, "n")
    return c.rows()


SPRING = spring()

LONG_TABLE = [  # 2x1, palette 2: a scholar's table with scrolls
    "................................",
    "...##....####.........###.......",
    "..#cc#..#cccc#.......#ccc#.#....",
    "..#cv#..#ccvv#..###..#cRc##c#...",
    ".##############################.",
    "#cvvvvvvvvvvvvvvvvvvvvvvvvvvvvw#",
    "#vvvvvvvvvvvvvvvvvvvvvvvvvvvvww#",
    "################################",
    "#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwW#",
    ".#W########################W##..",
    ".#w#......................#w#...",
    ".#w#......................#w#...",
    ".#w#......................#w#...",
    ".#v#......................#v#...",
    "#ww#......................#ww#..",
    "rrr.......................rrr...",
]


# --- The kit table ---------------------------------------------------------------
# (metatile id, name) -> layers. Furniture sits on an object layer over a floor
# or wall background, so its palette is free of the background's.

def cells(art, w, h):
    """Split a (16h x 16w) grid into per-metatile 16x16 grids, row-major."""
    assert len(art) == 16 * h, f"{len(art)} rows, want {16 * h}"
    for r in art:
        assert len(r) == 16 * w, f"row {r!r} is {len(r)} wide, want {16 * w}"
    out = []
    for cy in range(h):
        for cx in range(w):
            out.append([r[cx * 16:(cx + 1) * 16] for r in art[cy * 16:(cy + 1) * 16]])
    return out


KIT = []  # dicts: id, name, bottom (grid, pal), top (grid, pal) or None, layer, behavior


def put(mid, name, bottom, top=None, layer=NORMAL, behavior=MB_NORMAL):
    assert all(k["id"] != mid for k in KIT), hex(mid)
    KIT.append(dict(id=mid, name=name, bottom=bottom, top=top, layer=layer, behavior=behavior))


def obj(mid, name, art, pal, w, h, bgs, layers=None):
    """Place a w x h object at mid (a row of the sheet is 8 metatiles)."""
    for i, cell in enumerate(cells(art, w, h)):
        cx, cy = i % w, i // w
        layer = layers[i] if layers else COVERED
        put(mid + cy * 8 + cx, f"{name} {cx},{cy}" if w * h > 1 else name,
            bgs[i] if isinstance(bgs, list) else bgs, (cell, pal), layer)


T = (FLOOR_TERRA, 2)
M = (FLOOR_MARBLE, 4)
WU = (WALL_UPPER_BEAM, 3)
WL = (WALL_LOWER_FRIEZE, 3)


def build_kit():
    KIT.clear()
    # Row 1: floors
    put(0x008, "floor: terracotta", T)
    put(0x009, "floor: terracotta, worn", (FLOOR_TERRA_WORN, 2))
    put(0x00A, "floor: terracotta, wall shadow", (FLOOR_TERRA_SHADOW, 2))
    put(0x00B, "floor: marble", M)
    put(0x00C, "floor: marble, Aegean inlay", (FLOOR_MARBLE_INLAY, 4))
    put(0x00D, "floor: marble, wall shadow", (FLOOR_MARBLE_SHADOW, 4))
    put(0x00E, "floor: marble, meander border", (FLOOR_MARBLE_MEANDER, 4))
    put(0x00F, "floor: rush matting", (FLOOR_RUSH, 2))
    # Row 2: upper wall course
    put(0x010, "wall upper: ceiling beam", WU)
    put(0x011, "wall upper: plaster", (WALL_UPPER, 3))
    put(0x012, "wall upper: wave fresco", (WALL_UPPER_FRESCO, 3))
    put(0x013, "wall upper: lamp niche", (WALL_NICHE, 3), (NICHE_LAMP, 4), COVERED)
    put(0x014, "window: shutters closed", (WINDOW_SHUT, 3))
    put(0x015, "window: shutters open", (WINDOW_OPEN, 3))
    put(0x016, "doorway: lintel", (DOORWAY_TOP, 3))
    put(0x017, "stairs up: top", (STAIRS_UP_TOP, 3))
    # Row 3: lower wall course and floor openings
    put(0x018, "wall lower: meander frieze, dado", WL)
    put(0x019, "wall lower: plain dado", (WALL_LOWER, 3))
    put(0x01A, "wall upper: timber post", (WALL_POST_UPPER, 3))
    put(0x01B, "wall lower: timber post", (WALL_POST_LOWER, 3))
    put(0x01C, "threshold (exit, south warp)", (THRESHOLD, 4), behavior=MB_SOUTH_ARROW_WARP)
    put(0x01D, "stairs down", (STAIRS_DOWN, 2))
    put(0x01E, "doorway: opening", (DOORWAY_BOTTOM, 3))
    put(0x01F, "stairs up: bottom", (STAIRS_UP_BOTTOM, 3))
    # Rows 4-5: 2-tall pieces
    obj(0x020, "kline", kline(), 2, 2, 2, T)
    obj(0x022, "scroll shelf", shelf(), 2, 2, 2, [WU, WU, WL, WL])
    obj(0x024, "amphora rack", amphora_rack(), 2, 2, 2, [WU, WU, WL, WL])
    obj(0x026, "potted olive", OLIVE_POT, 2, 1, 2, T, [NORMAL, COVERED])
    obj(0x027, "lampstand", LAMPSTAND, 4, 1, 2, T, [NORMAL, COVERED])
    # Rows 6-7
    obj(0x030, "hearth", hearth(), 4, 2, 2, T)
    obj(0x032, "Doric column", COLUMN, 4, 1, 3, M, [NORMAL, NORMAL, COVERED])
    obj(0x033, "statue of Asclepius", STATUE, 4, 1, 2, M, [NORMAL, COVERED])
    obj(0x034, "pithos (tall)", PITHOS_TALL, 2, 1, 2, [WU, WL])
    obj(0x035, "loom (tall)", LOOM_TALL, 2, 1, 2, [WU, WL])
    obj(0x036, "klismos chair, facing down", KLISMOS_FRONT, 2, 1, 1, T)
    obj(0x037, "klismos chair, facing right", KLISMOS_SIDE, 2, 1, 1, T)
    obj(0x03E, "klismos chair, facing left", hflip(KLISMOS_SIDE), 2, 1, 1, T)
    obj(0x03F, "table (trapeza)", TABLE, 2, 1, 1, T)
    # Row 8 (0x042 is the column's base)
    obj(0x040, "stool (diphros)", STOOL, 2, 1, 1, T)
    obj(0x041, "chest (kibotos)", KIBOTOS, 2, 1, 1, T)
    obj(0x043, "amphora", AMPHORA, 2, 1, 1, T)
    obj(0x044, "krater", KRATER, 2, 1, 1, M)
    obj(0x045, "brazier", BRAZIER, 4, 1, 1, M)
    obj(0x046, "water clock (klepsydra)", KLEPSYDRA, 2, 1, 1, WU)
    obj(0x047, "knucklebones table", KNUCKLEBONES, 2, 1, 1, T)
    # Row 9
    obj(0x048, "counter", COUNTER, 2, 3, 1, T)
    obj(0x04B, "wall map of Aethos", WALL_MAP, 3, 2, 1, WU)
    obj(0x04D, "sacred spring basin", SPRING, 4, 2, 1, M)
    obj(0x04F, "herb pot", HERB_POT, 2, 1, 1, T)
    # Row 10
    obj(0x050, "scholar's table", LONG_TABLE, 2, 2, 1, T)
    # 0x060-0x09F: every free-standing piece again on the other floor, at its
    # id + 0x40 (terracotta <-> marble). The object layer's tiles are shared,
    # so these cost metatile ids only, no tiles.
    for k in [k for k in KIT if 0x020 <= k["id"] < 0x060]:
        if k["bottom"] is T or k["bottom"] is M:
            other = M if k["bottom"] is T else T
            put(k["id"] + 0x40, f"{k['name']}, on {'marble' if other is M else 'terracotta'}",
                other, k["top"], k["layer"], k["behavior"])
    KIT.sort(key=lambda k: k["id"])


# --- Assembly ---------------------------------------------------------------------

def read_pal(path):
    vals = [int(v) for v in path.read_text().split()[3:51]]
    return [tuple(vals[i:i + 3]) for i in range(0, 48, 3)]


def write_pal(path, colors):
    assert len(colors) == 16
    for c in colors:
        assert all(v % 8 == 0 for v in c), c
        assert c != (255, 0, 255), "Porytiles rejects magenta in palette slots"
    lines = ["JASC-PAL", "0100", "16"] + [f"{r} {g} {b}" for r, g, b in colors]
    path.write_bytes(("\r\n".join(lines) + "\r\n").encode())


def to_tiles(img):
    h, w = img.shape
    return img.reshape(h // 8, 8, w // 8, 8).swapaxes(1, 2).reshape(-1, 8, 8)


def from_tiles(tiles, cols=16):
    rows = len(tiles) // cols
    return tiles.reshape(rows, cols, 8, 8).swapaxes(1, 2).reshape(rows * 8, cols * 8)


def secondary_tile_refs():
    """Primary tile indices used by any secondary that pairs with Building or
    Oikos in data/layouts/layouts.json."""
    headers = (ROOT / "src/data/tilesets/headers.h").read_text()
    metas = dict(re.findall(r'(gMetatiles_\w+)\[\]\s*=\s*INCBIN_U16\("([^"]+)"',
                            (ROOT / "src/data/tilesets/metatiles.h").read_text()))
    bins = {}
    for name, body in re.findall(r'const struct Tileset (gTileset_\w+)\s*=\s*\{(.*?)\};', headers, re.S):
        f = dict(re.findall(r'\.(\w+)\s*=\s*(\w+)', body))
        if f.get("metatiles") in metas:
            bins[name] = ROOT / metas[f["metatiles"]]
    layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
    secs = {l["secondary_tileset"] for l in layouts
            if l.get("primary_tileset") in ("gTileset_Building", TILESET)}
    refs = set()
    for s in secs:
        m = np.fromfile(bins[s], "<u2") & 0x3FF
        refs |= {int(t) for t in m if t < 512}
    return refs


class Allocator:
    def __init__(self, tiles, free):
        self.tiles, self.free, self.seen = tiles, list(free), {}

    def entry(self, t, pal):
        if not t.any():
            return 0
        for hf in (0, 1):
            for vf in (0, 1):
                v = t[:, ::-1] if hf else t
                v = v[::-1, :] if vf else v
                k = v.tobytes()
                if k in self.seen:
                    return self.seen[k] | hf << 10 | vf << 11 | pal << 12
        assert self.free, "out of free primary tile slots"
        idx = self.free.pop(0)
        self.tiles[idx] = t
        self.seen[t.tobytes()] = idx
        return idx | pal << 12


def quarters(a):
    return [a[0:8, 0:8], a[0:8, 8:16], a[8:16, 0:8], a[8:16, 8:16]]


def layer_entries(alloc, layer):
    if layer is None:
        return [0, 0, 0, 0]
    rows, pal = layer
    return [alloc.entry(q, pal) for q in quarters(grid(rows, pal))]


REPAINTED = {9, 10, 19, 20, 35, 36, 496, 497, 498, 499, 21, 22, 37, 38, 500, 501}


def paint():
    build_kit()
    vt = Image.open(VANILLA / "tiles.png")
    tiles = to_tiles(np.array(vt) % 16).copy()
    assert len(tiles) == 512
    vanilla_tiles = tiles.copy()
    metatiles = np.fromfile(VANILLA / "metatiles.bin", "<u2").reshape(-1, 8).copy()
    attrs = np.fromfile(VANILLA / "metatile_attributes.bin", "<u2").copy()
    assert len(metatiles) == 8

    # 1. In-place repaints, at the tile indices Building's metatiles name.
    def put16(img, idxs):
        for q, i in zip(quarters(img), idxs):
            tiles[i] = q
    put16(LOOM, [19, 20, 35, 36])
    put16(LOOM_ON, [496, 497, 498, 499])
    put16(PITHOS, [21, 22, 37, 38])
    tiles[500], tiles[501] = PITHOS_ON_TOP[:, :8], PITHOS_ON_TOP[:, 8:]  # 0x005 reuses 37, 38
    tiles[9], tiles[10] = MAT_END, MAT_MID

    # 2. The kit, in slots nothing else uses.
    refs = secondary_tile_refs()
    free = [i for i in range(1, 512) if not vanilla_tiles[i].any() and i not in refs]
    alloc = Allocator(tiles, free)
    n = max(k["id"] for k in KIT) + 1
    meta = np.zeros((n, 8), np.uint16)
    attr = np.zeros(n, np.uint16)
    meta[:8], attr[:8] = metatiles, attrs
    for k in KIT:
        meta[k["id"]] = layer_entries(alloc, k["bottom"]) + layer_entries(alloc, k["top"])
        attr[k["id"]] = k["behavior"] | k["layer"] << 12
    used = 512 - len(alloc.free) - (512 - len(free))
    print(f"kit: {len(KIT)} metatiles, {used} new tiles, {len(alloc.free)} free slots left")

    # Write the Porymap assets.
    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.fromarray(from_tiles(tiles), "P")
    im.putpalette(vt.getpalette())
    im.save(OUT / "tiles.png")
    meta.tofile(OUT / "metatiles.bin")
    attr.tofile(OUT / "metatile_attributes.bin")
    (OUT / "palettes").mkdir(exist_ok=True)
    for i in range(16):
        if i in PALETTES:
            colors = PALETTES[i]
        else:  # secondary slots: never loaded from a primary; keep vanilla's
            colors = [c if c != (255, 0, 255) else BLACK for c in read_pal(VANILLA / f"palettes/{i:02d}.pal")]
        write_pal(OUT / f"palettes/{i:02d}.pal", colors)
    return tiles, vanilla_tiles, meta, refs


def porytiles(*args):
    exe = shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")
    r = subprocess.run([exe, *args], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"porytiles {' '.join(args)} failed:\n{r.stdout}\n{r.stderr}")


def snapshot():
    """What the game reads: tile indices, metatiles, attributes, palettes.
    (Porytiles re-encodes tiles.png's PNG palette and clears build outputs.)"""
    snap = {"tiles": (np.array(Image.open(OUT / "tiles.png")) % 16).tobytes()}
    for name in ("metatiles.bin", "metatile_attributes.bin"):
        snap[name] = (OUT / name).read_bytes()
    for i in range(16):
        snap[f"{i:02d}.pal"] = read_pal(OUT / f"palettes/{i:02d}.pal")
    return snap


def verify(tiles, vanilla_tiles, meta, refs):
    """Hoenn secondaries must still find their tiles; the kit must read back."""
    now = to_tiles(np.array(Image.open(OUT / "tiles.png")) % 16)
    moved = [i for i in sorted(refs) if i not in REPAINTED and not (now[i] == vanilla_tiles[i]).all()]
    assert not moved, f"tiles used by Hoenn secondaries changed: {moved}"
    assert (now == tiles).all(), "tiles.png differs from what was painted"
    got = np.fromfile(OUT / "metatiles.bin", "<u2").reshape(-1, 8)
    assert got.shape == meta.shape and (got == meta).all(), "metatiles.bin differs from what was painted"
    print(f"verified: {len(refs)} secondary-referenced tiles intact, kit reads back")


def main():
    tiles, vanilla_tiles, meta, refs = paint()
    if "--no-porytiles" not in sys.argv:
        before = snapshot()
        porytiles("decompile-tileset", TILESET, "--no-verify-checksums")
        porytiles("compile-tileset", TILESET)
        after = snapshot()
        changed = [str(p) for p in set(before) | set(after) if before.get(p) != after.get(p)]
        assert not changed, f"Porytiles recompile changed {changed}"
        print("porytiles: decompiled; a recompile changes nothing the game reads")
    verify(tiles, vanilla_tiles, meta, refs)


if __name__ == "__main__":
    main()
