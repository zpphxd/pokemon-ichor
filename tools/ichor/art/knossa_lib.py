"""Shared toolkit for Act III's Knossa secondaries (LABYRINTH.md §2, §3, §11).

Knossa is Minoan Crete above ground: Amnisos's harbor with a hive on every
roof, the Bull Road's vine and olive terraces, the Bronze Heel's giant foot on
its beach, the Palace of Minos on its hill, Mount Ida's holm oaks and its
caves. LABYRINTH.md §11 planned one `knossa` secondary; it holds far more
distinct pieces than 504 tiles, so it is split by map, as the Kythera family
is (see knossa_build.py), and every piece is painted here or in the knossa_*
painters and placed by name.

It builds on kythera_lib (and so agros_lib): the same Layer and Struct, walk
codes, borrowed aethos ground (grass, path, sand, sea, shallows, fall),
animations, validation, near-duplicate merging and previews. It adds:

  - Knossa's colors. The Minoan red, ochre, gypsum and black, and the fresco
    blues, whites and saffrons, are the labyrinth tileset's own
    (labyrinth_art.NEW, same names and values), so the palace's columns and
    frescoes and the Labyrinth's meet at the Grand Staircase in one red and
    one blue. Cretan limestone (`cs*`) is the Kythera rose-stone ramp
    re-toned grey-ochre, so Kythera's cliff and terrace painters can be
    recolored into it (recolor()).
  - The palette groups. Every 8x8 tile of every layer and animation frame
    draws from one group; each tileset takes at most seven (slots 6-12).
    Shared groups (minoan, fresco, stone, foam, green, bronze, terra) are the
    same in every Knossa tileset that carries them, so a piece two tilesets
    share looks the same in both.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_lib as K  # noqa: E402
from kythera_lib import (Layer, Struct, anim_layer, copy_struct, fill, ground,  # noqa: E402,F401
                         h, hp, pick, put, settle, struct)

A = K.A
C = K.C
ROOT = K.ROOT

NEW = {
    # --- Minoan red, ochre, gypsum, black, terracotta: labyrinth_art's "minoan"
    "mr0": (104, 24, 24), "mr1": (160, 40, 32), "mr2": (208, 72, 48), "mr3": (232, 128, 96),
    "mo0": (160, 104, 40), "mo1": (216, 160, 64), "mo2": (240, 216, 144),
    "mg0": (184, 176, 160), "mg1": (224, 216, 200), "mg2": (248, 240, 224),
    "mb": (56, 48, 48),
    "mt0": (128, 64, 40), "mt1": (184, 104, 64), "mt2": (224, 152, 104),
    # --- fresco blue, white, saffron, skin: labyrinth_art's "fresco"
    "fw": (248, 248, 240),
    "fb0": (24, 48, 104), "fb1": (40, 88, 168), "fb2": (96, 152, 216), "fb3": (168, 208, 240),
    "fy0": (216, 152, 40), "fy1": (248, 208, 96), "fr": (192, 56, 40), "fs": (168, 88, 56),
    "fg0": (56, 104, 64), "fg1": (120, 168, 96), "fq": (120, 128, 168), "fcr": (232, 216, 184),
    "fp": (232, 160, 152),
    # --- Cretan limestone: Kythera's rose ramp (rm0-rm5, mw2, mw3) re-toned
    "cs0": (64, 56, 56), "cs1": (112, 96, 88), "cs2": (160, 144, 120), "cs3": (200, 184, 152),
    "cs4": (232, 216, 184), "cs5": (248, 240, 224), "csw2": (216, 208, 192),
    "csw3": (152, 144, 136),
    # --- vines and grapes; thyme flowers come from agros (th2)
    "gp0": (72, 40, 88), "gp1": (128, 72, 136),
    # --- bronze gone green: Talos's foot, old nails and shields
    "vg0": (32, 80, 72),
    # --- the cave: Ida's and Eileithyia's dark limestone, and a polished stone's shine
    "ck0": (16, 16, 24), "ck1": (40, 40, 48), "ck2": (64, 64, 72), "ck3": (96, 88, 96),
    "ck4": (128, 120, 120), "ck5": (168, 160, 152), "ck6": (208, 200, 184),
    "cm0": (80, 72, 48), "cm1": (120, 104, 72),
    # --- Titan slate and gold (the West Magazines' camp)
    "ts0": (40, 32, 56), "ts1": (80, 72, 104), "ts2": (128, 120, 152), "tgd": (232, 184, 64),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in C or C[_n] == _c, f"color name clash: {_n}"
    C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)

GRASS4 = ["g1", "g2", "g3", "gd"]

GROUPS = {
    # labyrinth_art.GROUPS["minoan"], verbatim: red columns and black capitals,
    # gypsum, ochre plaster, horns of consecration, labrys marks, pithoi, the
    # houses of Amnisos (plaster, timber, red frames), hives of clay and straw
    "minoan": ["ink", "mr0", "mr1", "mr2", "mr3", "mo0", "mo1", "mo2", "mg0", "mg1", "mg2",
               "mb", "mt0", "mt1", "mt2"],
    # labyrinth_art.GROUPS["fresco"], verbatim: blue grounds, dolphins, lilies,
    # saffron, bull-leapers, blue monkeys, griffins
    "fresco": ["ink", "fw", "fb0", "fb1", "fb2", "fb3", "fy0", "fy1", "fr", "fs", "fg0", "fg1",
               "fq", "fcr", "fp"],
    # Cretan limestone on aethos grass: cliffs, terraces, the town wall, tide
    # shelves above the water; kythera_lib's "rose" group, re-toned
    "stone": ["cs0", "cs1", "cs2", "cs3", "cs4", "cs5", "w0", "csw2", "csw3", "cv0", "my1",
              "my2", "my3", "g1", "g2"],
    # kythera_lib's "foam", verbatim: surf, lace, wet rock, the quay's edges
    "foam": ["b3", "b4", "w0", "kq1", "kq2", "kr0", "kr1", "kr2", "kr3", "ks1", "ks2", "p1",
             "p2", "p3", "l1"],
    # vines and grapes, holm oak, phrygana and thyme, on aethos grass
    "green": GRASS4 + ["t0", "my1", "my2", "my3", "my4", "kt1", "kt2", "gp0", "gp1", "th2",
                       "w0"],
    # bronze and verdigris (Talos's foot, the Kouretes' shields, labrys door
    # fittings), and Kythera's marble herm (cw*), which Knossa reuses
    "bronze": ["bz0", "bz1", "bz2", "bz3", "vg0", "vg1", "vg2", "w0", "cw1", "cw2", "cw3",
               "ink", "mr", "pl", "ks1"],
    # kythera_lib's "terra", verbatim: boats, the triremes, timber, nets, ladders
    "terra": ["tc0", "tc1", "tc2", "tc3", "wd0", "wd1", "wd2", "wd3", "w0", "ink", "b1", "b2",
              "kr1", "kr2", "rs1"],
    # the caves of Ida and Eileithyia: dark limestone, the worn floor, the
    # polished stone
    "cave": ["ck0", "ck1", "ck2", "ck3", "ck4", "ck5", "ck6", "cm0", "cm1", "cs3", "cs4",
             "cs5", "mt1", "mo1", "fw"],
    # Titan slate and gold, with timber and canvas, for the West Magazines' camp
    "titan": ["ink", "ts0", "ts1", "ts2", "tgd", "bz1", "bz2", "wd0", "wd1", "wd2", "wd3",
              "tc3", "kr1", "kr2", "w0"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(C[n] for n in _names)) == len(_names), _g
    for _n in _names:
        assert _n in C, _n


def groups(*names):
    """The ordered group dict for a tileset carrying these groups."""
    assert len(names) <= 7, names
    return {n: GROUPS[n] for n in names}


def group_rgb(gr):
    return {g: {C[n] for n in names} for g, names in gr.items()}


# --------------------------------------------------------------------------
# Recoloring Kythera's painters into Knossa's groups
# --------------------------------------------------------------------------

ROSE_TO_STONE = {"rm0": "cs0", "rm1": "cs1", "rm2": "cs2", "rm3": "cs3", "rm4": "cs4",
                 "rm5": "cs5", "mw2": "csw2", "mw3": "csw3"}


def recolor(s, mapping):
    """Map color names to others in every layer and animation frame of s."""
    rgb = {C[a]: C[b] for a, b in mapping.items()}
    arrays = [L.a for L in s.layers.values()]
    for an in s.anims.values():
        arrays += [f.a for f in an["frames"]]
    for a in arrays:
        m = a[..., 3] > 0
        flat = a[..., :3]
        for src, dst in rgb.items():
            sel = m & (flat[..., 0] == src[0]) & (flat[..., 1] == src[1]) & (flat[..., 2] == src[2])
            flat[sel] = dst
    return s


def nearest(s, names, layers=("bottom", "middle", "top")):
    """Snap every pixel of the given layers to the nearest of `names`."""
    pal = np.array([C[n] for n in names], np.int32)
    for ln in layers:
        a = s.layers[ln].a
        m = a[..., 3] > 0
        px = a[..., :3][m].astype(np.int32)
        if not len(px):
            continue
        d = ((px[:, None, :] - pal[None, :, :]) ** 2 * np.array([3, 4, 2])).sum(-1)
        a[..., :3][m] = pal[d.argmin(1)].astype(np.uint8)
    return s


# --------------------------------------------------------------------------
# Small painting helpers
# --------------------------------------------------------------------------

def grid(L, ox, oy, rows, legend, flip=False):
    """put() with a legend that may map a char to None (transparent: erase)."""
    for j, row in enumerate(rows):
        if flip:
            row = row[::-1]
        for i, ch in enumerate(row):
            if ch == " " or ch not in legend:
                continue
            L.px(ox + i, oy + j, legend[ch])


def mirror_cells(L, x0, y0, w, h_):
    """Make a box left-right symmetric: copy its left half onto the right."""
    for y in range(y0, y0 + h_):
        for x in range(w // 2):
            L.a[y, x0 + w - 1 - x] = L.a[y, x0 + x]


def tex16(L, ox, oy, w, h_, fn, mask=None):
    """Fill a box with fn(x mod 16, y mod 16) so the texture tiles."""
    for y in range(oy, oy + h_):
        for x in range(ox, ox + w):
            if mask is not None and not mask(x - ox, y - oy):
                continue
            c = fn(x % 16, y % 16)
            if c:
                L.px(x, y, c)
