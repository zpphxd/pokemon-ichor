"""Shared toolkit for gTileset_Kopais, Route 8's secondary (the Kopais shore).

Lake Kopais's south shore: reed beds (the marsh's tall grass), shallow marsh
water and the open lake, mudflats, Mount Phikion's grey rock and scrub, the
Minyan dike with its sluice and fishing jetty, the Treasury of Minyas, the
walled islet of Gla, and the fowlers' and eel-men's gear. It pairs with the
aethos primary.

It draws with agros_lib's layers and structures, eleusa_lib's borrowed ground,
validation and tile merging, and kithairon_lib's soft-shape engine, and adds:

  - Kopais's palette plan: seven groups for the secondary's slots 6-12.
  - Class keys for soft ground that meets several kinds of neighbor. A key is
    '1|' then N NE E SE S SW W NW, one character each: '1' the region itself,
    or the neighbor's class (g grass and anything dry, w marsh water, m mud,
    r reeds). The visible shape comes from the binary key (kithairon_lib.soft);
    each pixel outside it is painted as the class of the neighbor cell it lies
    in, so reeds fade into water on one side and grass on another.
  - Phases. Animated pieces (the reeds' sway, the marsh water's glints) are
    painted once per phase; kopais_build.py turns phases 1-3 into tile frames.

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
import kithairon_lib as K  # noqa: E402  (registers Kithairon's colors: rk*, cy*, oa*...)
from agros_lib import GRASS, PATH, SEA, TALL, Struct, aethos  # noqa: E402,F401

ROOT = A.ROOT
PHASES = 4                # animation frames per animated piece (key frame = phase 0)

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # cattails and reed plumes
    "ct0": (80, 48, 32), "ct1": (136, 88, 48), "rpl": (208, 192, 144),
    # marsh mud, from the wet dark to the cracked dry crust
    "md0": (64, 56, 40), "md1": (104, 88, 64), "md2": (144, 128, 96), "md3": (184, 168, 128),
    # marsh water: murky green-teal shallows, and their glint
    "mw0": (48, 88, 88), "mw1": (72, 120, 112), "mw2": (112, 160, 144), "mw3": (184, 216, 200),
    # lily pads and duckweed
    "lp1": (72, 120, 48), "lp2": (128, 168, 72),
    # fowlers' and eel-men's gear: straw, cord, fire, smoke, eels
    "st1": (184, 152, 88), "st2": (224, 200, 136), "fi1": (224, 96, 32), "fi2": (248, 200, 72),
    "sm1": (168, 168, 160), "sm2": (216, 216, 208), "el": (56, 56, 40),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GRASS4 = ["g1", "g2", "g3", "gd"]
REED = ["t0", "t1", "gd", "t3", "ct0", "ct1", "rpl"]

GROUPS = {
    # reed beds on dry ground: reeds, cattails, grass, the mud at their feet
    "reed": REED + ["g1", "g2", "g3", "md0", "md1", "md2", "ink"],
    # reed beds standing in the water
    "reedw": REED + ["mw0", "mw1", "mw2", "mw3", "lp1", "lp2", "md0", "md1"],
    # marsh water, its mud banks and mudflats, lily pads, the lake's marshy rim
    "marsh": ["mw0", "mw1", "mw2", "mw3", "md0", "md1", "md2", "md3", "lp1", "lp2", "w0"]
             + GRASS4,
    # the road, barley on the spur, turned earth, the racing post
    "field": GRASS4 + ["t0", "t1", "t3", "tg", "p1", "p2", "p3", "l0", "l1", "wd1", "ink"],
    # Phikion's grey rock, its scrub and ledges, the Sphinx's ledge and feathers
    "rock": GRASS4 + ["rk0", "rk1", "rk2", "rk3", "rk4", "rk5", "oa1", "oa2", "oa3", "w0", "ink"],
    # Minyan stonework: the dike, the sluice, the Treasury, Gla's wall, the herm
    "stone": ["cy0", "cy1", "cy2", "cy3", "cy4", "l0", "l1", "p1", "p2", "p3"]
             + GRASS4 + ["ink"],
    # reed huts, nets, eel traps, the smoking rack and its fire, the reed boat
    "gear": ["wd1", "wd2", "st1", "st2", "k1", "fi1", "fi2", "sm1", "sm2", "el", "g1", "g2",
             "gd", "ink"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# Borrowed ground: a cell's bottom layer pointed at aethos's own metatile.
GROUND_METATILE = {"grass": 0x001, "path": 0x1D9, "sea": 0x170, "tall": 0x00D, "shade": 0x01C,
                   "deep": 0x14E, "longgrass": 0x015}
E.GROUND_METATILE.update(GROUND_METATILE)

struct = E.struct
ground = E.ground
put = E.put
validate = lambda structs: E.validate(structs, GROUP_RGB)  # noqa: E731
merge_near_duplicates = E.merge_near_duplicates
tiles_of = E.tiles_of
composite = E.composite
preview = E.preview
hsh = K.hsh
ring, halo, soft, crop = K.ring, K.halo, K.soft, K.crop
DIRS = K.DIRS


def which_group(cols):
    for g, rgb in GROUP_RGB.items():
        if cols <= rgb:
            return g
    return None


# --------------------------------------------------------------------------
# Class keys
# --------------------------------------------------------------------------

def binary(key, inside="1"):
    """The binary blob key of a class key: `inside` lists the classes that
    count as the region. Diagonals count only when both sides do."""
    neigh = key.split("|")[1]
    b = [1 if c in inside else 0 for c in neigh]
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] and b[c]):
            b[d] = 0
    return "1|" + "".join(str(v) for v in b)


def class_canvas(key, center="1"):
    """48 x 48 array of the class of each pixel's cell (the cell in the middle).
    A diagonal neighbor that doesn't count (one of its sides is another class)
    takes the class of its sides when they agree, so corners stay clean."""
    neigh = key.split("|")[1]
    cls = np.empty((48, 48), dtype="<U1")
    cls[16:32, 16:32] = center
    for i, (st, (dx, dy)) in enumerate(zip(neigh, DIRS)):
        cls[16 + dy * 16:32 + dy * 16, 16 + dx * 16:32 + dx * 16] = st
    # pixels of the region itself take the class of the nearest other cell, so
    # the margin a soft edge leaves inside the region is painted as what lies
    # beyond it
    own = cls == center
    if (~own).any():
        out = np.argwhere(~own).astype(np.float32)
        pts = np.argwhere(own).astype(np.float32)
        d = ((pts[:, None, :] - out[None, :, :]) ** 2).sum(-1)
        near = out[d.argmin(1)].astype(int)
        for (y, x), (ny, nx) in zip(pts.astype(int), near):
            cls[y, x] = cls[ny, nx]
    return cls


def outside_class(cls, y, x):
    """The class of an outside pixel (canvas coordinates)."""
    return cls[y, x]


def periodic(fn):
    """fn(x, y) on absolute pixels, made 16 px periodic."""
    return lambda x, y: fn(x % 16, y % 16)


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def grass_name(x, y):
    g = aethos(GRASS)
    return A.RGB2NAME[tuple(int(v) for v in g[y % 16, x % 16])]


def name_of(rgb):
    return A.RGB2NAME[tuple(int(v) for v in rgb)]


def sway(phase):
    """The reeds' sway, in pixels, for each phase: rest, lean east, rest, lean west."""
    return (0, 1, 0, -1)[phase % PHASES]


def wave(phase, x, y, k=0):
    """A slow drift for the marsh water's glints: 0..15."""
    return (x + 4 * phase + 3 * ((y + k) // 4)) % 16


def struct_anim(s, kind):
    s.anim = kind
    return s
