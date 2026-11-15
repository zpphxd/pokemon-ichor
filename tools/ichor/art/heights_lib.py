"""Shared toolkit for gTileset_ArkadiaHeights, the Arkadian climb's secondary,
and gTileset_MaiaCave, the Cave of Maia's.

The climb from Aigion to Arkadia (Route 11, Styx Falls, Route 12) is one set
on the aethos primary, so its own seams need no aethos-only strip. It draws
with agros_lib's layers and structures, eleusa_lib's borrowed ground,
validation and tile merging, and kithairon_lib's soft-shape engine, and adds:

  - the climb's palette plan: seven groups for the secondary's slots 6-12.
    Every 8x8 tile of every layer takes all its colors from one group.
  - borrowed ground for falling water: a cell can sit on aethos's animated
    waterfall (0x0B3), so the Styx's thread moves behind a slit in the cliff.

All colors are multiples of 8 (exact BGR555). New color names start with "q",
so they never clash with another set's.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
import eleusa_lib as E  # noqa: E402
import kithairon_lib as K  # noqa: E402  (the soft-shape engine, the firs' colors)
from agros_lib import GRASS, PATH, SEA, TALL, Layer, Struct, aethos  # noqa: E402,F401

ROOT = A.ROOT

NEW = {
    # Arkadian limestone: a warm, ochre-tinged grey, from crevice to sunlit lip
    "qr0": (48, 40, 40), "qr1": (88, 80, 72), "qr2": (128, 120, 104), "qr3": (168, 160, 136),
    "qr4": (208, 200, 176), "qr5": (240, 232, 208),
    # fern and moss on the cliffs
    "qv1": (64, 104, 56), "qv2": (112, 152, 72),
    # the Styx's black rock, black water, the obols, the thread of white water
    "qb0": (16, 16, 24), "qb1": (40, 40, 48), "qb2": (64, 64, 72), "qb3": (96, 96, 104),
    "qb4": (136, 136, 144), "qk0": (0, 8, 16), "qk1": (24, 32, 48),
    "qa1": (184, 144, 56), "qa2": (232, 200, 96), "qm0": (200, 216, 224), "qm1": (240, 248, 248),
    # Kyllene's wind-combed meadow grass, gentians and crocus
    "qg0": (48, 88, 64), "qg1": (88, 128, 80), "qg2": (136, 168, 104), "qg3": (184, 200, 144),
    "qf1": (88, 112, 200), "qf2": (152, 176, 232), "qy": (232, 200, 72),
    # white water: foam and its shadow over the river
    "qs0": (96, 152, 192), "qs1": (176, 216, 232),
    # the fallen temple's marble, the kiln's clay, a bronze crescent
    "qm2": (232, 224, 200), "qm3": (192, 184, 160), "qm4": (144, 136, 120), "qm5": (96, 88, 80),
    "qc1": (176, 96, 56), "qc2": (216, 144, 96), "qz": (200, 168, 96),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GRASS4 = ["g1", "g2", "g3", "gd"]

GROUPS = {
    # tall barley grass and the road (agros's painters, verbatim)
    "field": list(A.GROUPS["field"]),
    # Kyllene's meadow grass, its flowers
    "meadow": GRASS4 + ["qg0", "qg1", "qg2", "qg3", "qf1", "qf2", "qy", "w0", "th1", "th2", "ink"],
    # the gorge's limestone: cliffs, rims, ledges, boulders, Nonakris's houses, nests
    "rock": GRASS4 + ["qr0", "qr1", "qr2", "qr3", "qr4", "qr5", "qv1", "qv2", "wd1", "k1", "ink"],
    # the Styx: black rock, black water, obols, the white thread
    "black": GRASS4 + ["qb0", "qb1", "qb2", "qb3", "qb4", "qk0", "qk1", "qa1", "qa2", "qm0", "qm1"],
    # firs, kermes oak, cypresses (kithairon's tree group, so its painters work here)
    "tree": GRASS4 + ["fr0", "fr1", "fr2", "fr3", "oa1", "oa2", "oa3", "k1", "k2", "w0", "ink"],
    # the river's white water and gravel banks, runnels, springs
    "water": GRASS4 + ["qr1", "qr2", "qr3", "qr4", "qs0", "qs1", "qm1", "qv1", "qv2", "ink"],
    # the fallen temple, drums, the kiln and its smoke, shrines, herms, the bridge
    "stone": GRASS4 + ["qm2", "qm3", "qm4", "qm5", "qc1", "qc2", "wd1", "wd2", "qz", "qr1", "ink"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# The Cave of Maia's own set: the cave's rock and floor, the god's things.
CAVE_NEW = {
    "qd0": (24, 16, 16), "qd1": (56, 48, 40), "qd2": (96, 80, 64), "qd3": (136, 112, 88),
    "qd4": (176, 152, 112), "qd5": (208, 184, 136), "qe1": (160, 128, 88), "qe2": (192, 160, 112),
    "qe3": (224, 200, 152),
}
for _n, _c in CAVE_NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)

CAVE_GROUPS = {
    # walls and floor: the cave's warm brown rock, its sandy floor
    "cave": ["qd0", "qd1", "qd2", "qd3", "qd4", "qd5", "qe1", "qe2", "qe3", "ink"],
    # the god's things: the lyre's shell, gut strings, swaddling, the lamp's flame
    "relic": ["qd0", "qd1", "qd2", "qd4", "qe1", "qe2", "qe3", "qm2", "qc1", "qc2", "qy", "wd1",
              "wd2", "ink"],
    # the altar and the herm's face: marble on the cave floor
    "altar": ["qd1", "qd2", "qd3", "qe1", "qe2", "qe3", "qm2", "qm3", "qm4", "qm5", "qz", "qv1",
              "qv2", "qc1", "ink"],
}
for g, names in CAVE_GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
CAVE_GROUP_RGB = {g: {C[n] for n in names} for g, names in CAVE_GROUPS.items()}

# Borrowed ground: a cell's bottom layer pointed at aethos's own metatile.
GROUND_METATILE = {"grass": 0x001, "path": 0x1D9, "sea": 0x170, "tall": 0x00D, "shade": 0x01C,
                   "fall": 0x0B3}
E.GROUND_METATILE.update(GROUND_METATILE)    # E.composite/preview read it

struct = K.struct
ground = E.ground
put = E.put
merge_near_duplicates = E.merge_near_duplicates
tiles_of = E.tiles_of
composite = E.composite
preview = E.preview
blob_key = E.blob_key
hsh = K.hsh
soft = K.soft
ring = K.ring
halo = K.halo
shape_set = K.shape_set
crop = K.crop
ellipse_mask = K.ellipse_mask


def validate(structs, cave=False):
    return E.validate(structs, CAVE_GROUP_RGB if cave else GROUP_RGB)


def name_of(rgb):
    return A.RGB2NAME[tuple(int(v) for v in rgb)]


def grass_px(x, y):
    """aethos grass at (x, y), phase-locked to the 16 px grid, by color name."""
    return name_of(aethos(GRASS)[y % 16, x % 16])


def shade(c, steps=1, ramp=("qr0", "qr1", "qr2", "qr3", "qr4", "qr5")):
    """Move a color along a ramp: steps < 0 darker, > 0 lighter."""
    if c not in ramp:
        return c
    i = max(0, min(len(ramp) - 1, ramp.index(c) + steps))
    return ramp[i]
