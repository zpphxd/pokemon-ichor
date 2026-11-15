"""Shared toolkit for gTileset_Trophonios, Trophonios's cave under Lebadeia.

A self-contained secondary on the aethos primary for the two dark floors of
the oracle's cave (SCRIPT.md Part 5 and Part 10). It started from batch 1's
Antiope's cave (gTileset_KithaironCave: the crag rock as cave walls, the floor,
the bronze brazier) and was redrawn for a deeper, worked cave: walls with a
dark cap and a tall ochre limestone face, a damp clay floor, the underground
Herkyna, the priests' paved chamber with the throne of Mnemosyne, the
pilgrims' chalk handprints, the snake's cleft, the black pool and the
bread-oven hole.

It draws with agros_lib's Layer and Struct and eleusa_lib's validation and
tile merging, and adds its own palette plan: six groups for the secondary's
slots 6-12. Every 8x8 tile of every layer takes all its colors from one group.
Walls, props and furniture sit in the middle layer over the plain floor's
bottom tiles, so the floor is stored once and every group stays pure.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
import eleusa_lib as E  # noqa: E402
import kithairon_lib as K  # noqa: E402  (its soft-shape engine is generic)
from agros_lib import Layer, Struct  # noqa: E402,F401

ROOT = A.ROOT

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    "tink": (16, 8, 8),
    # the rock's cap, seen from above: near-black umber with lumps
    "cp0": (24, 16, 16), "cp1": (40, 32, 32), "cp2": (64, 48, 48),
    # the face: warm ochre limestone, from the base's shadow to the lip
    "fc0": (56, 40, 32), "fc1": (88, 64, 48), "fc2": (120, 96, 72), "fc3": (160, 128, 96),
    "fc4": (200, 168, 128), "fc5": (232, 208, 168),
    # the pilgrims' chalk: faint in torchlight; the glow copy lights only these
    "ch1": (184, 184, 168), "ch2": (232, 232, 216),
    # damp: seeps on the face, wet floor
    "dm0": (48, 64, 56), "dm1": (80, 104, 88),
    # the floor: cool grey-brown clay, pebbles
    "fl0": (48, 40, 40), "fl1": (72, 64, 56), "fl2": (96, 80, 72), "fl3": (120, 104, 88),
    "fl4": (152, 136, 112), "fl5": (184, 168, 136),
    "dp0": (40, 48, 48), "dp1": (64, 72, 64), "cs0": (32, 24, 24),
    # the priests' paving
    "pv1": (176, 160, 128), "pv2": (208, 192, 160),
    # the underground Herkyna and the black pool
    "wa0": (8, 16, 24), "wa1": (16, 32, 48), "wa2": (32, 56, 72), "wa3": (56, 88, 104),
    "wa4": (104, 144, 152), "fm": (192, 216, 208), "bk": (8, 8, 8),
    # bronze, fire, ash, bread and honey
    "bz0": (96, 56, 16), "bz1": (160, 104, 40), "bz2": (216, 160, 72),
    "fx0": (184, 48, 24), "fx1": (232, 112, 32), "fx2": (248, 184, 56), "fx3": (248, 240, 200),
    "as0": (64, 56, 56), "as1": (112, 104, 96),
    "br0": (120, 72, 32), "br1": (176, 120, 64), "br2": (224, 192, 136), "hn": (232, 152, 24),
    # the throne's marble, wood and rope, daylight through the grille
    "mb0": (96, 96, 104), "mb1": (144, 144, 152), "mb2": (192, 192, 192), "mb3": (232, 232, 224),
    "wo0": (64, 40, 24), "wo1": (104, 72, 40), "wo2": (152, 112, 64),
    "rp0": (168, 136, 88), "rp1": (208, 184, 136),
    "dl0": (184, 200, 208), "dl1": (240, 248, 248),
    # the snake, the webs, old bones
    "sn0": (24, 32, 24), "sn1": (48, 64, 40), "sn2": (80, 96, 56), "sn3": (128, 136, 80),
    "sn4": (176, 168, 112), "wb0": (152, 152, 160), "wb1": (216, 216, 224),
    "bn0": (200, 192, 168), "bn1": (144, 136, 120),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GROUPS = {
    # walls: the cap, the face, chalk prints and seeps on the face
    "rock": ["tink", "cp0", "cp1", "cp2", "fc0", "fc1", "fc2", "fc3", "fc4", "fc5", "ch1", "ch2",
             "dm0", "dm1"],
    # the floor, damp, contact shadow, chalk on the floor, the priests' paving
    "floor": ["tink", "fl0", "fl1", "fl2", "fl3", "fl4", "fl5", "dp0", "dp1", "cs0", "ch1", "ch2",
              "pv1", "pv2"],
    # the stream, its banks, the spring, the black pool and its rim
    "water": ["tink", "wa0", "wa1", "wa2", "wa3", "wa4", "fm", "bk", "fl1", "fl2", "fl3", "fc1",
              "fc2", "fc3"],
    # bronze braziers, flame, ash, bread offerings and honey cakes
    "fire": ["tink", "bz0", "bz1", "bz2", "fx0", "fx1", "fx2", "fx3", "as0", "as1", "br0", "br1",
             "br2", "hn"],
    # the throne of Mnemosyne, the grille, the ladder, the votive tablets
    "stone": ["tink", "mb0", "mb1", "mb2", "mb3", "wo0", "wo1", "wo2", "rp0", "rp1", "bz1", "bz2",
              "dl0", "dl1"],
    # the snake's coils, cobwebs, old bones
    "life": ["tink", "sn0", "sn1", "sn2", "sn3", "sn4", "cp0", "cp1", "wb0", "wb1", "bn0", "bn1"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}
GLOW = ("ch1", "ch2")   # the glow copy keeps only these (SYSTEMS.md section 2)


def struct(key, title, w, h, section, walk=None, notes="", names=None):
    return E.struct(key, title, w, h, section, walk=walk, notes=notes, names=names)


put = E.put
validate = lambda structs: E.validate(structs, GROUP_RGB)  # noqa: E731
merge_near_duplicates = E.merge_near_duplicates
tiles_of = E.tiles_of
composite = E.composite
soft = K.soft
ring = K.ring
halo = K.halo
ellipse_mask = K.ellipse_mask


def hsh(x, y, k=0):
    h = (x * 374761393 + y * 668265263 + k * 2147483647) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h ^ (h >> 16)) & 0xFFFF



# --------------------------------------------------------------------------
# Textures (16 px periodic, so neighbors tile seamlessly)
# --------------------------------------------------------------------------

def _pnoise(v, salt):
    """A smooth 16 x 16 field in about [-1, 1], periodic in both directions."""
    y, x = np.mgrid[0:16, 0:16].astype(float)
    t = 2 * math.pi / 16
    f = np.zeros((16, 16))
    for i, (kx, ky, a) in enumerate(((1, 0, 1.0), (0, 1, 1.0), (1, 1, 0.7), (1, -1, 0.7),
                                     (2, 1, 0.45), (1, 2, 0.45), (3, -1, 0.3), (2, -3, 0.25))):
        ph = (hsh(i, v, salt) % 628) / 100.0
        f += a * np.sin(t * (kx * x + ky * y) + ph)
    return f / 2.6


_FLOOR = {}


def floor_px(x, y, variant=0):
    """The cave floor: packed grey-brown clay, softly mottled (a few variants)."""
    v = variant % 4
    if v not in _FLOOR:
        f = _pnoise(v, 31)
        g = np.full((16, 16), "fl2", object)
        for yy in range(16):
            for xx in range(16):
                n = f[yy, xx] + ((xx + yy) % 2) * 0.12
                if n < -0.78:
                    g[yy, xx] = "fl1"
                elif n > 0.72:
                    g[yy, xx] = "fl3"
                h = hsh(xx, yy, 40 + v) % 100
                if h < 4:
                    g[yy, xx] = "fl1"
                elif h > 97:
                    g[yy, xx] = "fl3"
        _FLOOR[v] = g
    return _FLOOR[v][y % 16, x % 16]


def pebble(L, x, y, big=False):
    L.px(x, y, "fl4")
    L.px(x + 1, y, "fl3")
    L.px(x, y + 1, "fl3")
    L.px(x + 1, y + 1, "fl1")
    if big:
        L.px(x + 2, y, "fl3")
        L.px(x + 2, y + 1, "fl1")
        L.px(x, y + 2, "fl0")
        L.px(x + 1, y + 2, "fl0")
        L.px(x - 1, y, "fl5")


def floor_cell(L, ox, oy, variant=0):
    base = {0: 0, 1: 1, 2: 2, 3: 3, 4: 1, 5: 0, 6: 2, 7: 3}.get(variant, 0)
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, floor_px(x, y, base))
    if variant == 1:        # pebbles
        for (px, py, big) in ((3, 4, True), (11, 2, False), (7, 11, True), (13, 13, False), (1, 13, False)):
            pebble(L, ox + px, oy + py, big)
    elif variant == 2:      # a hairline crack
        for (px, py) in ((1, 4), (2, 5), (3, 5), (4, 6), (5, 6), (6, 7), (7, 7), (8, 8), (9, 8),
                         (10, 8), (11, 9), (12, 10), (13, 10), (14, 11)):
            L.px(ox + px, oy + py, "fl0")
            L.px(ox + px, oy + py + 1, "fl3")
        L.px(ox + 9, oy + 9, "fl0")
    elif variant == 3:      # damp: a dark wet sheen in an irregular patch
        f = _pnoise(9, 77)
        for y in range(16):
            for x in range(16):
                r = math.hypot((x - 7.5) / 7.5, (y - 8) / 6)
                if r + 0.25 * f[y, x] < 0.85:
                    L.px(ox + x, oy + y, "fl1" if (x + 2 * y) % 5 else "fl0")
                elif r + 0.25 * f[y, x] < 1.0 and (x + y) % 2:
                    L.px(ox + x, oy + y, "fl1")
        for (px, py) in ((5, 6), (10, 9), (7, 11)):
            L.px(ox + px, oy + py, "fl4")
    elif variant == 4:      # gravel: a drift of small stones
        for (px, py) in ((2, 3), (5, 2), (9, 4), (12, 3), (4, 7), (8, 8), (13, 8), (2, 11),
                         (6, 12), (10, 13), (14, 12)):
            L.px(ox + px, oy + py, "fl4" if (px + py) % 3 else "fl3")
            L.px(ox + px + 1, oy + py + 1, "fl1")
    elif variant == 5:      # plain, with one big flat stone set in the clay
        m = ellipse_mask(16, 16, 8.5, 8, 5.2, 3.8)
        for yy, xx in np.argwhere(m):
            u = (xx - 8.5) / 5.2 + (yy - 8) / 3.8
            L.px(ox + xx, oy + yy, "fl4" if u < -0.6 else ("fl3" if u < 0.7 else "fl2"))
        for yy, xx in np.argwhere(ring(m)):
            if yy >= 8:
                L.px(ox + xx, oy + yy, "fl0")


_CAP = {}


def cap_px(x, y, variant=0):
    """The rock's cap from above: near-black umber, with low lumps lit from the
    top left. A few variants, so a big mass of rock never reads as a grid."""
    v = variant % 3
    if v not in _CAP:
        f = _pnoise(v, 5) + 0.35 * _pnoise(v + 7, 13)
        lump = f > 0.62
        g = np.full((16, 16), "cp0", object)
        for yy in range(16):
            for xx in range(16):
                if lump[yy, xx]:
                    up = lump[(yy - 1) % 16, xx] and lump[yy, (xx - 1) % 16]
                    g[yy, xx] = "cp1" if up or (xx + yy) % 2 else "cp2"
                elif hsh(xx, yy, 50 + v) % 17 == 0:
                    g[yy, xx] = "cp1"
        _CAP[v] = g
    return _CAP[v][y % 16, x % 16]


def _wob(x, seed):
    """A small periodic wobble (16 px), for strata lines that meet across cells."""
    t = 2 * math.pi / 16
    return int(round(1.2 * math.sin(t * x + seed) + 0.6 * math.sin(2 * t * x + 2 * seed)))


def face_px(x, y, row, rows, seed=0, variant=0):
    """The limestone face: wandering strata over a light-to-dark fall, a few
    vertical joints, speckle. row is this cell's row in the face (0 = top),
    rows the face's height; variants differ in their joints and speckle only,
    so strata meet across neighboring cells."""
    yy = row * 16 + y
    total = rows * 16
    t = yy / max(total - 1, 1)
    shade = 4 - int(t * 3.2 + 0.25)                 # 4 at the lip, 1 at the base
    phase = (yy + _wob(x, 1.3 + 0.7 * (yy // 6))) % 6
    if phase == 0:
        shade -= 1                                   # a bedding line
    elif phase == 1:
        shade += 1 if t < 0.8 else 0                 # the ledge of rock above it
    # vertical joints: a dark line down part of the cell
    for jx, j0, j1 in (((3, 0, 9), (11, 5, 16)), ((7, 2, 14),), ((2, 6, 16), (13, 0, 7)))[variant % 3]:
        if x == jx and j0 <= y < j1:
            shade = min(shade, 1)
        elif x == jx + 1 and j0 <= y < j1:
            shade += 1
    h = hsh(x, yy, 60 + variant) % 100
    if h < 5:
        shade -= 1
    elif h > 96:
        shade += 1
    shade = max(0, min(5, shade))
    return f"fc{shade}"


def paint_face(L, ox, oy, row, rows, seed=0, mask=None, variant=0):
    for y in range(16):
        for x in range(16):
            if mask is None or mask[y, x]:
                L.px(ox + x, oy + y, face_px(x, y, row, rows, seed, variant))


def chalk_hand(L, ox, oy, kind, bright="ch1", dim="ch1"):
    """A small chalk hand, fingers pointing `kind` (N, E, S, W), or a flat
    palm print ('one'), drawn 8-10 px across at (ox, oy)."""
    hands = {
        "N": [
            ".2.2.2..",
            ".2.2.2.2",
            ".2.2.2.2",
            ".1222221",
            "2222222.",
            ".222222.",
            "..2222..",
            "..1221..",
        ],
        "one": [
            "..2.2.2.",
            "..2.2.2.",
            "2.2.2.2.",
            ".2222222",
            ".222222.",
            "..2222..",
            "..2222..",
            "...11...",
        ],
    }
    if kind in ("N", "one"):
        rows = hands[kind]
    elif kind == "S":
        rows = [r[::-1] for r in hands["N"][::-1]]
    elif kind == "E":
        n = hands["N"]
        rows = ["".join(n[7 - x][y] for x in range(8)) for y in range(8)]
    elif kind == "W":
        n = hands["N"]
        rows = ["".join(n[x][7 - y] for x in range(8)) for y in range(8)]
    else:
        raise ValueError(kind)
    put(L, ox, oy, rows, {"2": bright, "1": dim})
