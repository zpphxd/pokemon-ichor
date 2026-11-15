"""Shared toolkit for Thyrsa's theater: gTileset_Theater (the outdoor theater, on
the aethos primary) and gTileset_Skene (the stage building's backstage and prop
room, on oikos).

The theater is the set piece of Act II's first stretch (design/phase3/SCRIPT.md,
beats 32-34 and Part 2). Its map is drawn in the GBA's oblique view, so the
stage building stands at the top of the map with its painted front facing the
camera, and the cavea fans out below the orchestra: the audience sits with its
back to us, facing the stage, as it would in Thyrsa.

This module holds:

  - the colors and palette groups of both tilesets. Every 8x8 tile of every
    layer takes all its colors from one group (eleusa_lib.validate checks it);
  - the cavea's geometry, shared by the art (theater_cavea.py) and the map
    builder (tools/ichor/maps/theater.py), so the seats drawn are the seats
    placed;
  - the seated people, as small ASCII sprites.

The cavea is an octagon of concentric tiers around the orchestra, built so its
art repeats every cell: the straight south tiers are rows of the map, the
straight west and east tiers are columns, and the 45-degree tiers between them
run on diagonals. Every facet's corner falls on a cell edge, so every cell of
seats is one facet's pattern, and a whole facet is one repeating cell.
All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
from agros_lib import Layer, Struct  # noqa: E402,F401

ROOT = A.ROOT

# --------------------------------------------------------------------------
# Colors. Names are prefixed q (the theater) and k (the skene) so they never
# clash with another tileset's in agros_lib's shared table.
# --------------------------------------------------------------------------

NEW = {
    # the cavea's seat stone: Thyrsa's warm limestone, in the crowd's palette
    "qs0": (96, 80, 56), "qs1": (152, 128, 96), "qs2": (200, 176, 136), "qs3": (232, 216, 184),
    # the crowd: skin, hair, festival clothes
    "qk1": (176, 112, 72), "qk2": (232, 176, 128), "qh1": (96, 56, 32), "qh2": (176, 168, 152),
    "qcw": (240, 232, 216), "qcr": (184, 48, 40), "qcb": (64, 96, 160), "qcy": (224, 168, 48),
    "qcp": (128, 64, 136),
    # paving, stairs and kerbs: the same limestone, one step bluer, so stone
    # without people never lands in the crowd's palette
    "qp0": (96, 80, 64), "qp1": (152, 128, 104), "qp2": (200, 176, 144), "qp3": (232, 216, 192),
    # marble, bronze, flame, ivy
    "qm1": (248, 240, 224), "qm2": (208, 200, 184), "qb0": (112, 72, 32), "qb1": (184, 136, 64),
    "qf0": (208, 64, 24), "qf1": (248, 152, 40), "qf2": (248, 232, 144),
    "qi0": (40, 80, 40), "qi1": (96, 144, 56),
    # the orchestra's beaten earth and the stage's planks
    "qe0": (136, 104, 64), "qe1": (176, 136, 88), "qe2": (208, 176, 120),
    "qw0": (80, 48, 32), "qw1": (128, 88, 48), "qw2": (176, 136, 80),
    # the skene's front: painted plaster, roof tiles, gold, the doors' paint
    "qa1": (176, 152, 120), "qa2": (216, 192, 152), "qa3": (240, 224, 192),
    "qr0": (104, 40, 32), "qr1": (160, 64, 40), "qr2": (208, 112, 72),
    "qg1": (192, 144, 40), "qg2": (248, 208, 88), "qd1": (136, 40, 56),
    # the god-machine, rope, garlands, the hill's rock
    "qo1": (160, 128, 80), "qo2": (216, 184, 128), "qx1": (112, 104, 96), "qx2": (160, 152, 136),
    "qn": (216, 72, 56),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GRASS4 = ["g1", "g2", "g3", "gd"]

# gTileset_Theater's four groups. Porytiles gets them as packing hints and
# fills four palettes; the build copies the crowd's palette into the three
# spare slots, one per pair of blocks, so the six blocks of seats pulse in
# three pairs and each pair can stop on its own (theater_build.py). Seat
# stone and stair stone never share an 8x8 tile: where a stair, a walkway or
# the aisle cuts a seat cell, the seats are the bottom layer and the stone
# lies over them in the middle layer.
GROUPS = {
    # the seats and the people in them
    "crowd": ["ink", "qs0", "qs1", "qs2", "qs3", "qk1", "qk2", "qh1", "qh2",
              "qcw", "qcr", "qcb", "qcy", "qcp", "qi1"],
    # stairs, walkways, the aisle, the orchestra, the stage floor, the terrace
    "earth": GRASS4 + ["ink", "qe0", "qe1", "qe2", "qp0", "qp1", "qp2", "qp3",
                       "qw0", "qw1", "qw2"],
    # the skene's painted front and roof
    "skene": ["ink", "qa1", "qa2", "qa3", "qw0", "qw1", "qw2", "qr0", "qr1", "qr2",
              "qg1", "qg2", "qi0", "qi1", "qd1"],
    # the crane, ropes, garlands, torches and the thymele, on grass or stone
    "props": GRASS4 + ["ink", "qw1", "qo1", "qo2", "qb1", "qi1", "qn", "qm1", "qp2",
                       "qf1", "qf2"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(C[n] for n in _names)) == len(_names), _g
    for _n in _names:
        assert _n in C, _n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# The crowd's palette is copied into two spare slots; its seats are drawn three
# times, once per pair of blocks (theater_build.py patches the copies).
PAIRS = ("low", "mid", "top")

# --------------------------------------------------------------------------
# The map and the cavea's geometry (pixels; cell = 16 px)
# --------------------------------------------------------------------------

W, H = 40, 34
OX, OY = 320, 208          # the orchestra's center (the thymele)
OR = 64                    # the orchestra's radius
YS = 288                   # the south tiers: tier 0 is row 18
XS = 272                   # ... and runs from column 17 to the stair; tier k from XS - 8k
XW = 240                   # the west tiers: tier 0 is column 14 (east tiers mirrored)
CUT = 160                  # the cavea's north ends: the side tiers stop at row 10
CORNER_W = XW + 16         # tier 0's west column turns into the diagonal at row 16; tier k at +8k
TIERS = 15                 # tiers 0..14: seats, the diazoma, seats, the promenade
DIAZOMA = (6, 7)           # the walkway halfway up
PROMENADE = (13, 14)       # the walkway round the top
STAIR_C = (304, 336)       # the central stair, columns 19-20
STAIR_D = (504, 536)       # the diagonal stairs: px + py in this band (cells x+y = 31, 32)
STAIR_W = (208, 224)       # the side stairs: row 13, through the orchestra's center
STAGE_ROW = 6              # the stage floor, rows 6-7
PROSKENION_ROW = 8         # the stage front
FRONT_ROW = 0              # tier 0: the front row (prohedria)


def mirror_px(px):
    """Left-half coordinates for any pixel column (the cavea is symmetric)."""
    return px if px < OX else 2 * OX - 1 - px


def tier_coord(px, py):
    """The continuous tier coordinate of a pixel, and which facet it lies on.
    floor() of it is the tier; its fraction runs 0 at a tier's inner (stage)
    edge to 1 at its outer edge."""
    x = mirror_px(px) + 0.5
    y = py + 0.5
    ts = (y - YS) / 16.0
    tw = (XW - x) / 16.0
    # The diagonal tier k's inner edge runs through the south facet's corner,
    # which moves half a cell out per tier: (XS - 8k, YS + 16k), so
    # y - x = YS - XS + 24k. The west corner moves the same way, (XW - 16k,
    # CORNER_W + 8k). Every facet grows, as a regular octagon's would, and a
    # diagonal tier is 17 px thick, near the straight tiers' 16.
    td = (y - x - (YS - XS)) / 24.0
    t, facet = ts, "S"
    if tw > t:
        t, facet = tw, "W"
    if td > t:
        t, facet = td, "D"
    return t, facet


def facet_of_cell(cx, cy):
    """Every seat cell lies on one facet: 'S' (a south row), 'W' (a west or
    east column) or 'D' (a diagonal). Cells inside tier 0 return 'I'."""
    t, f = tier_coord(cx * 16 + 8, cy * 16 + 8)
    return f if t >= 0 else "I"


def cell_tier(cx, cy):
    t, _ = tier_coord(cx * 16 + 8, cy * 16 + 8)
    return int(np.floor(t))


def in_cavea_rows(cy):
    return cy * 16 >= CUT


def is_left(cx):
    return cx * 16 < OX


def stair_at(px, py):
    """Which stair a pixel is on, if any: 'C' central, 'D' diagonal, 'W' side."""
    x = mirror_px(px)
    t, facet = tier_coord(px, py)
    if facet == "S" and STAIR_C[0] <= px < STAIR_C[1]:
        return "C"
    if facet == "D" and STAIR_D[0] <= x + py + 1 < STAIR_D[1]:
        return "D"
    if facet == "W" and STAIR_W[0] <= py < STAIR_W[1]:
        return "W"
    return None


def stair_cell(cx, cy):
    """The stair cells the player walks: the central stair's two columns, the
    side stairs' row, and each diagonal stair's two-cell staircase."""
    if cy * 16 < CUT:
        return None
    t = cell_tier(cx, cy)
    if t < 0 or t >= PROMENADE[0] or t in DIAZOMA:
        return None
    f = facet_of_cell(cx, cy)
    x = cx if is_left(cx) else W - 1 - cx
    if f == "S" and cx in (19, 20):
        return "C"
    if f == "W" and cy == 13:
        return "W"
    if f == "D" and x + cy in (31, 32):
        return "D"
    return None


def walkway_cell(cx, cy):
    """A cell of the diazoma or the promenade the player can stand on: its
    center is on the walkway. On the diagonals that makes a two- or three-cell
    staircase, which the player walks like any stair."""
    if cy * 16 < CUT and facet_of_cell(cx, cy) == "W":
        return False
    t = cell_tier(cx, cy)
    return t in DIAZOMA or t in PROMENADE


def walk_cell(cx, cy):
    """Where the player may walk in the cavea: its stairs and walkways, and
    everything inside tier 0 (the aisle and the orchestra)."""
    if stair_cell(cx, cy) or walkway_cell(cx, cy):
        return True
    t, f = tier_coord(cx * 16 + 8, cy * 16 + 8)
    return t < 0


def block_of_cell(cx, cy):
    """The block of seats a cell belongs to (1-6, west to east), or 0. The
    stairs divide them: the side stair, the diagonal stair, the central
    stair. Pairs: blocks 1 and 6 are 'low' (their ends come down to the
    parodoi), 2 and 5 'mid', 3 and 4 'top' (the back of the cavea)."""
    t = cell_tier(cx, cy)
    if cy * 16 < CUT or t < 0 or t >= PROMENADE[0] or t in DIAZOMA or stair_cell(cx, cy):
        return 0
    f = facet_of_cell(cx, cy)
    x = cx if is_left(cx) else W - 1 - cx
    if f == "W":
        b = 1 if cy < 13 else 2
    elif f == "D":
        b = 2 if x + cy < 31 else 3
    else:
        b = 3
    return b if is_left(cx) else 7 - b


def pair_of_block(b):
    return {1: "low", 6: "low", 2: "mid", 5: "mid", 3: "top", 4: "top"}.get(b)


# --------------------------------------------------------------------------
# Seated people, seen from the stage side's back: ASCII sprites
#   H hair   S skin   T tunic   t tunic shade (ink)   o ink outline
# --------------------------------------------------------------------------

# From behind (the south tiers face north, to the stage): 7 x 9.
BACK = [
    "..ooo..",
    ".oHHHo.",
    ".oHHHo.",
    "..SHS..",
    ".oTTTo.",
    "oTTTTTo",
    "oTTTTTo",
    "oTTTTTo",
    ".ooooo.",
]
# In profile, facing east (the west tiers face the orchestra): 7 x 9.
PROFILE = [
    "..ooo..",
    ".oHHSo.",
    ".oHHSSo",
    "..oSSo.",
    ".oTTTo.",
    "oTTTTTo",
    "oTTTTSo",
    "oTTTTTo",
    ".ooooo.",
]
# Three-quarter back view, facing north-east (the south-west diagonal): 7 x 9.
THREEQ = [
    "..ooo..",
    ".oHHHo.",
    ".oHHSo.",
    "..SSo..",
    ".oTTTo.",
    "oTTTTTo",
    "oTTTTTo",
    "oTTTTTo",
    ".ooooo.",
]
SPRITES = {"S": BACK, "W": PROFILE, "D": THREEQ}

HAIRS = ["qh1", "ink", "qh1", "qh2", "qcy", "ink"]
TUNICS = ["qcw", "qcr", "qcb", "qcy", "qcp", "qcw", "qi1", "qcr"]


def person(L, x, y, facet, hair, tunic, flip=False):
    """Paint one seated person with its top-left at (x, y)."""
    rows = SPRITES[facet]
    legend = {"H": hair, "S": "qk2", "T": tunic, "o": "ink"}
    for j, row in enumerate(rows):
        r = row[::-1] if flip else row
        for i, ch in enumerate(r):
            if ch in legend:
                L.px(x + i, y + j, legend[ch])
