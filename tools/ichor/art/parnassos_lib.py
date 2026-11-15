"""Shared toolkit for gTileset_Parnassos: Lebadeia and Route 9, the Split Road.

One secondary on the aethos primary for both maps, so their shared seam needs
no aethos-only strip. It draws with kithairon_lib's soft-shape engine, layers
and borrowed ground (which come from agros_lib and eleusa_lib), and adds
Parnassos's palette plan: seven groups for the secondary's slots 6-12, where
every 8x8 tile of every layer takes all its colors from one group.

  field  tall grass, the road, timber (the broken bridge)
  rock   Parnassos's pale limestone crags, scrub, the river's banks, the bronze
         grille and the spout in the rock face
  tree   laurels, wild olives, plane trees
  stone  worked limestone on grass: paving, the herm, the boundary stone,
         altars, the treasury's ruin, column drums, steps, bridges, benches
  water  the springs of Lethe and Mnemosyne and their rims
  house  Eleusa's house kit, verbatim
  far    the far side of the ravine: the Phaidriades, Delphoi's roofs, the
         Kastalian falls, the ravine's dark

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kithairon_lib as K  # noqa: E402  (registers rk*, iv*, fr*, ... and Eleusa's colors)
from kithairon_lib import (GRASS, PATH, SEA, TALL, Layer, Struct, aethos, blob_key,  # noqa: E402,F401
                           blob_keys, crop, ellipse_mask, fill, halo, hsh, ring, soft)

A = K.A
E = K.E
ROOT = K.ROOT

NEW = {
    # Parnassos's limestone: paler and warmer than Kithairon's, from crevice to sun
    "pk0": (48, 40, 40), "pk1": (96, 88, 80), "pk2": (136, 128, 112), "pk3": (176, 168, 152),
    "pk4": (208, 200, 184), "pk5": (240, 232, 216),
    # bronze (the grille, the herm's garland boss)
    "bz1": (168, 104, 48),
    # laurel: the bay tree's dark glossy leaves, to the lit tips
    "lr0": (24, 48, 32), "lr1": (40, 80, 48), "lr2": (72, 120, 64), "lr3": (128, 168, 88),
    # worked limestone and marble, shadow to highlight
    "mb0": (64, 56, 48), "mb1": (112, 104, 88), "mb2": (160, 152, 136), "mb3": (200, 192, 176),
    "mb4": (232, 224, 208), "mb5": (248, 248, 240),
    # Lethe's black water
    "lt0": (16, 24, 32), "lt1": (32, 48, 64), "lt2": (64, 88, 104),
    # the far side: hazy rock, the ravine's dark and its mist
    "hz0": (120, 128, 152), "hz1": (152, 160, 176), "hz2": (184, 192, 200), "hz3": (216, 216, 224),
    "dk0": (24, 24, 40), "dk1": (56, 56, 80),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GRASS4 = ["g1", "g2", "g3", "gd"]

GROUPS = {
    "field": GRASS4 + ["t0", "t1", "t3", "tg", "p1", "p2", "p3", "l0", "l1", "wd1", "ink"],
    "rock": GRASS4 + ["pk0", "pk1", "pk2", "pk3", "pk4", "pk5", "iv0", "iv1", "iv2", "bz1", "b3"],
    "tree": GRASS4 + ["lr0", "lr1", "lr2", "lr3", "o4", "o5", "k1", "k2", "k3", "w1", "ink"],
    "stone": GRASS4 + ["mb0", "mb1", "mb2", "mb3", "mb4", "mb5", "lr1", "tc1", "p1", "p2", "ink"],
    "water": ["b1", "b2", "b3", "b4", "w0", "lt0", "lt1", "lt2", "mb0", "mb1", "mb2", "mb3", "mb4",
              "lr1", "ink"],
    "house": list(E.GROUPS["house"]),
    "far": ["hz0", "hz1", "hz2", "hz3", "pk0", "dk1", "tc1", "tc2", "w0", "w1", "b4", "lr1", "lr2",
            "pk2", "ink"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# Borrowed ground: a cell's bottom layer pointed at aethos's own metatile.
GROUND_METATILE = {"grass": 0x001, "path": 0x1D9, "sea": 0x170, "tall": 0x00D, "shade": 0x01C}
E.GROUND_METATILE.update(GROUND_METATILE)

struct = K.struct
ground = E.ground
put = E.put
validate = lambda structs: E.validate(structs, GROUP_RGB)  # noqa: E731
merge_near_duplicates = E.merge_near_duplicates
tiles_of = E.tiles_of
preview = E.preview
composite = E.composite
shape_set = K.shape_set
on_other_ground = E.on_other_ground

# Kithairon's painters draw with its own rock and ivy names; Parnassos's rock is
# warmer and paler, so their output is recolored by name.
KITH_TO_PARN = {"rk0": "pk0", "rk1": "pk1", "rk2": "pk2", "rk3": "pk3", "rk4": "pk4", "rk5": "pk5",
                "mk": "bz1"}


def recolor(L, mapping):
    """Swap colors on a layer by name (in place)."""
    a = L.a
    for src, dst in mapping.items():
        r, g, b = C[src]
        m = (a[..., 3] > 0) & (a[..., 0] == r) & (a[..., 1] == g) & (a[..., 2] == b)
        a[m, 0], a[m, 1], a[m, 2] = C[dst]


def recolor_struct(s, mapping=KITH_TO_PARN):
    for L in s.layers.values():
        recolor(L, mapping)
    return s


def grass_name(x, y):
    g = aethos(GRASS)
    return A.RGB2NAME[tuple(int(v) for v in g[y % 16, x % 16])]


def grass_fill(L, x0, y0, w, h):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            L.px(x, y, grass_name(x, y))


def shadow_dither(L, cx, cy, rx, ry, x0, y0, x1, y1):
    """A soft cast shadow on grass already painted on L (an ellipse, dithered)."""
    for y in range(y0, y1):
        for x in range(x0, x1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1:
                continue
            c = L.get(x, y)
            if c in ("g2", "g3") and (x + y) % 2 == 0:
                L.px(x, y, "g1")
            elif c == "g1" and (x + y) % 2 == 0:
                L.px(x, y, "gd")


def shadow_alpha(L, cx, cy, rx, ry, x0, y0, x1, y1):
    """A dithered shadow painted as 'gd' on empty pixels of an upper layer (for
    pieces on borrowed grass, whose own layer can't read the grass)."""
    for y in range(y0, y1):
        for x in range(x0, x1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1:
                continue
            if not L.a[y, x, 3] and (x + y) % 2 == 0:
                L.px(x, y, "gd")


def blobs_crown(L, ox, oy, w, h, blobs, ramp, rim, speck=None):
    """A broadleaf crown from overlapping round blobs, lit from the top left.
    ramp: [shadow, mid, light, (highlight)]; returns the mask."""
    m = np.zeros((h, w), bool)
    for (cx, cy, rx, ry) in blobs:
        m |= ellipse_mask(w, h, cx, cy, rx, ry)
    for y in range(h):
        for x in range(w):
            if not m[y, x]:
                continue
            best = min(blobs, key=lambda b: ((x - b[0]) / b[2]) ** 2 + ((y - b[1]) / b[3]) ** 2)
            u = (x - best[0]) / best[2] + (y - best[1]) / best[3]
            if u > 0.7:
                c = ramp[0]
            elif u > -0.15:
                c = ramp[1]
            elif u > -0.9 or len(ramp) < 4:
                c = ramp[2]
            else:
                c = ramp[3]
            if speck and (x * 7 + y * 5) % 11 == 0 and -0.6 < u < 0.5:
                c = speck
            L.px(ox + x, oy + y, c)
    pad = np.pad(m, 1)
    edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in np.argwhere(edge):
        L.px(ox + x, oy + y, rim)
    return m
