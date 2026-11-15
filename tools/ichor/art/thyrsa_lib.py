"""Shared toolkit for gTileset_Thyrsa, Thyrsa City's secondary tileset.

Thyrsa is Thebes renamed: the god's own city, walled on a long hill, older and
greyer than Corinth. Its walls are Cyclopean (huge polygonal blocks, dark joints,
ivy in every crack), its streets are flagged in the same grey-buff stone, its
houses are ochre or limewashed under terracotta with doors and shutters painted
wine-purple or vine-green, and masks hang over its doors for the festival.

It draws with emporion_lib's Struct, finish and painters (which use
kalliste_lib's Layer and the 8-wide sheet packing) and adds:

  - Thyrsa's palette plan: seven groups for the secondary's slots 6-12. Every
    8x8 tile of every layer takes all its colors from one group; validate()
    enforces it.
  - "clay" (ochre stucco, wine paint) and "clay2" (limewash, vine-green paint)
    are parallel slot for slot, so a lime house part is the ochre part's own
    tile in another palette and costs nothing.
  - Ground per cell, as Emporion's: borrowed aethos ground ("grass", "path"),
    Thyrsa's own street flags ("pave"), the vineyards' tilled earth ("earth"),
    or "none" (the art fills the cell).
  - Painters for the city: Cyclopean masonry, flagstones, ivy, masks and
    festival garlands.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion_lib as E  # noqa: E402
import kalliste_lib as K  # noqa: E402
from kalliste_lib import Layer, tile_colors  # noqa: E402,F401

ROOT = K.ROOT

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # Theban stone: a cool grey-buff, older than Corinth's marble
    "cg0": (64, 56, 56), "cg1": (96, 88, 80), "cg2": (128, 120, 104), "cg3": (160, 152, 128),
    "cg4": (192, 184, 160), "cg5": (224, 216, 192), "cb": (168, 136, 96),
    # ivy, the god's plant, on everything
    "iv0": (24, 48, 32), "iv1": (40, 80, 40), "iv2": (72, 120, 48), "iv3": (128, 168, 72),
    # wine-purple paint, and its parallel, vine-green
    "wn0": (72, 24, 48), "wn1": (128, 48, 80),
    "gp0": (56, 96, 80), "gp1": (120, 152, 104),
    # limewash, the parallel of ochre stucco
    "lm0": (152, 144, 136), "lm1": (192, 184, 176), "lm2": (232, 224, 216), "lm3": (248, 240, 232),
    # the festival's purples and a deep red
    "vp0": (56, 24, 56), "vp1": (104, 40, 96), "vp2": (160, 88, 152), "rd0": (120, 32, 32),
    # the vineyards' earth
    "e0": (112, 72, 48),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    # Cyclopean walls, gates, towers, the street flags and kerbs, steps, terrace
    # walls, Semele's chamber, Chthonia's house; ivy and its smoke.
    "stone": ["ink", "cg0", "cg1", "cg2", "cg3", "cg4", "cg5", "cb", "w0", "iv0", "iv1", "iv2",
              "iv3", "e1", "e2"],
    # Terracotta roofs, ochre stucco, wine-purple doors and shutters, ivy on walls.
    "clay": ["ink", "tc0", "tc1", "tc2", "tc3", "oc0", "oc1", "oc2", "oc3", "wn0", "wn1", "w0",
             "w2", "iv1", "iv2"],
    # The same, slot for slot, with limewash and vine-green paint.
    "clay2": ["ink", "tc0", "tc1", "tc2", "tc3", "lm0", "lm1", "lm2", "lm3", "gp0", "gp1", "w0",
              "w2", "iv1", "iv2"],
    # Marble, gold, painted blue and red: the temple, the Asclepeion, the fountain.
    "marble": ["ink", "w0", "m1", "m2", "m3", "m4", "m5", "g0", "g1", "br", "b0", "b1", "b2",
               "rd", "rd0"],
    # The festival: masks, garlands, ribbons, awnings, banners.
    "fest": ["ink", "w0", "rd", "rd0", "vp0", "vp1", "vp2", "g0", "g1", "iv1", "iv2", "iv3",
             "wd0", "wd1", "wd2"],
    # The vineyards: vines, grapes, trellis timber, tilled earth.
    "vine": ["ink", "wd0", "wd1", "wd2", "wd3", "iv0", "iv1", "iv2", "iv3", "vp0", "vp1", "vp2",
             "e0", "e1", "e2"],
    # Timber, warm limestone and terracotta: the press, jars, barrels, gates' leaves.
    "wood": ["ink", "wd0", "wd1", "wd2", "wd3", "s1", "s2", "s3", "s4", "tc0", "tc1", "tc2",
             "tc3", "w0", "rp"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# clay -> clay2: a limewashed house is the ochre house, slot for slot
LIME = dict(zip(GROUPS["clay"], GROUPS["clay2"]))

# The ground kinds. "pave" and "earth" are drawn by this tileset; "grass" and
# "path" are borrowed from aethos (emporion_lib.GROUND_METATILE).
E.DRAWN.add("earth")
Struct = E.Struct


def struct(key, title, w, h, walk=None, notes="", ground="pave", section="streets"):
    return Struct(key, title, w, h, walk=walk, notes=notes, ground=ground, section=section)


# --------------------------------------------------------------------------
# Cyclopean masonry and flagstones: Voronoi blocks on a torus, so the texture
# repeats every `period` px and long walls cost few tiles.
# --------------------------------------------------------------------------

def _voronoi(period, n, seed, sx=0.85, sy=1.05):
    """Seeds on a jittered grid over a period x period torus; returns the label
    of the nearest seed, the distances to the nearest and second-nearest, and
    each pixel's offset from its own seed (for shading the block's bulge)."""
    rnd = random.Random(seed)
    pts = []
    k = int(math.ceil(math.sqrt(n)))
    cell = period / k
    for j in range(k):
        for i in range(k):
            if len(pts) >= n:
                break
            pts.append(((i + 0.15 + 0.7 * rnd.random()) * cell, (j + 0.15 + 0.7 * rnd.random()) * cell))
    yy, xx = np.mgrid[0:period, 0:period]
    best = np.full((period, period), 1e9)
    second = np.full((period, period), 1e9)
    lab = np.zeros((period, period), int)
    offx = np.zeros((period, period))
    offy = np.zeros((period, period))
    for idx, (px, py) in enumerate(pts):
        for ox in (-period, 0, period):
            for oy in (-period, 0, period):
                dx, dy = xx - px - ox, yy - py - oy
                d = np.hypot(dx * sx, dy * sy)
                upd = d < best
                second = np.where(upd, best, np.minimum(second, d))
                best = np.where(upd, d, best)
                lab = np.where(upd, idx, lab)
                offx = np.where(upd, dx, offx)
                offy = np.where(upd, dy, offy)
    return lab, best, second, offx, offy


_TEX = {}
FLAG_SEED = 9
WALL_SEED = 29

TEXTURES = {
    # kind: (period, blocks, seed attr, ramp, per-block base index, joint width, joint color)
    "wall": (32, 6, "WALL_SEED", ("cg1", "cg2", "cg3", "cg4", "cg5"), (2, 2, 3, 1, 2, 3), 1.0, "cg0"),
    "flag": (16, 3, "FLAG_SEED", ("cg2", "cg3", "cg4", "cg5", "cg5"), (2, 2, 2), 0.9, "cg2"),
    "rough": (32, 4, None, ("cg1", "cg2", "cg3", "cg4", "cg5"), (2, 1, 3, 2), 1.2, "cg0"),
}


def masonry(kind):
    """A period x period array of color names for a texture.

    kind: "wall" (Cyclopean face: big polygonal blocks with bulging, shaded faces
          and thin dark joints), "flag" (the street flags: lighter, flatter),
          "rough" (Chthonia's house: bigger, rougher)."""
    if kind in _TEX:
        return _TEX[kind]
    period, n, seed_attr, ramp, bases, jw, jc = TEXTURES[kind]
    seed = globals()[seed_attr] if seed_attr else 23
    lab, d1, d2, offx, offy = _voronoi(period, n, seed)
    gap = d2 - d1
    out = np.empty((period, period), object)
    radius = period / math.sqrt(n) / 2
    for y in range(period):
        for x in range(period):
            b = lab[y, x]
            if gap[y, x] < jw:
                out[y, x] = jc
                continue
            i = bases[b % len(bases)]
            # the block's bulge: lit toward the top left, shaded toward the bottom
            # right, strongest near its edges
            t = (offx[y, x] + offy[y, x] * 1.2) / (radius * 1.6)
            edge = gap[y, x] < jw + 1.3
            if edge and t < -0.1:
                i += 2 if kind != "flag" else 1
            elif t < -0.55:
                i += 1
            elif edge and t > 0.15:
                i -= 2 if kind != "flag" else 1
            elif t > 0.6:
                i -= 1
            else:
                h = (x * 7 + y * 13 + b * 5) % 29
                if h == 0:
                    i -= 1
            out[y, x] = ramp[max(0, min(4, i))]
    _TEX[kind] = out
    return out


def fill_masonry(L, x0, y0, w, h, kind="wall", ox=0, oy=0):
    """Paint the texture into the box, phase-locked to (ox, oy) so that a cell at
    map column c meets its neighbors when ox = -16 * (c % 2)."""
    tex = masonry(kind)
    p = tex.shape[0]
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            L.px(x, y, tex[(y - oy) % p][(x - ox) % p])


# --------------------------------------------------------------------------
# Ivy
# --------------------------------------------------------------------------

def ivy_leaf(L, x, y, lit=False):
    """A single ivy leaf, 3x3, pointing down: the god's plant."""
    L.blit(["1k1" if not lit else "2k2", "212" if not lit else "323", " 1 "],
           {"k": "iv0", "1": "iv1", "2": "iv2", "3": "iv3"}, x, y)


def ivy_patch(L, x0, y0, w, h, density=0.55, seed=1, lit=True, mask=None, dark="iv0"):
    """A mat of ivy over the box: overlapping leaves, darker at the bottom, with a
    few sunlit leaves on top. mask(x, y) -> bool limits where leaves fall."""
    rnd = random.Random(seed)
    spots = []
    for yy in range(y0, y0 + h, 2):
        for xx in range(x0, x0 + w, 2):
            if rnd.random() < density and (mask is None or mask(xx, yy)):
                spots.append((xx + rnd.randint(-1, 1), yy))
    for (xx, yy) in spots:
        L.blit(["kk", "11"] if rnd.random() < 0.5 else ["k1", "12"],
               {"k": dark, "1": "iv1", "2": "iv2"}, xx, yy)
    if lit:
        for (xx, yy) in spots[::3]:
            L.px(xx + 1, yy, "iv2")
            if rnd.random() < 0.4:
                L.px(xx, yy, "iv3")


def ivy_drape(L, x0, y0, w, length, seed=3, top_full=4):
    """Ivy falling from a wall top: a full mat for top_full px, then strands of
    uneven length hanging down. Returns nothing; draws into L."""
    rnd = random.Random(seed)
    ivy_patch(L, x0, y0, w, top_full, density=0.9, seed=seed)
    x = x0
    while x < x0 + w:
        ln = rnd.randint(length // 3, length)
        for yy in range(y0 + top_full, y0 + top_full + ln):
            c = "iv1" if (yy - y0) % 3 else "iv2"
            L.px(x, yy, c)
            if (yy - y0) % 3 == 0:
                L.px(x - 1 if rnd.random() < 0.5 else x + 1, yy, "iv1")
                L.px(x, yy + 1, "iv0")
        L.px(x, y0 + top_full + ln, "iv0")
        x += rnd.randint(2, 4)


# --------------------------------------------------------------------------
# Masks
# --------------------------------------------------------------------------

MASK_COMIC = [
    " kkkkkk ",
    "kwwwwwwk",
    "kwkwwkwk",
    "kwwwwwwk",
    "kwrrrrwk",
    " krkkrk ",
    "  kkkk  ",
]
MASK_TRAGIC = [
    " kkkkkk ",
    "kwwwwwwk",
    "kkwwwwkk",
    "kwkwwkwk",
    "kwwkkwwk",
    " kwwwwk ",
    "  kkkk  ",
]
MASK_SATYR = [
    "k      k",
    "kk kkkkk",
    " kgggggk",
    "kgkggkgk",
    "kggggggk",
    " kgrrgk ",
    "  kggk  ",
    "   kk   ",
]
MASK_KEY = {"k": "ink", "w": "w0", "r": "rd", "g": "g0"}


def mask(L, x, y, kind="comic", hair=None):
    rows = {"comic": MASK_COMIC, "tragic": MASK_TRAGIC, "satyr": MASK_SATYR}[kind]
    L.blit(rows, MASK_KEY, x, y)
    if hair:
        # an ivy wreath over the brow
        for i in range(0, 8, 2):
            L.px(x + i, y, "iv2")
            L.px(x + i + 1, y, "iv1")


# --------------------------------------------------------------------------
# Validation (emporion_lib's, against Thyrsa's groups)
# --------------------------------------------------------------------------

def validate(structs):
    problems = []
    for s in structs:
        gr = s.borrowed
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    cols = tile_colors(layer, tx, ty)
                    if not cols:
                        continue
                    if not any(cols <= g for g in GROUP_RGB.values()):
                        names = sorted(K.RGB2NAME.get(c, str(c)) for c in cols)
                        problems.append(f"{s.key} {ln} tile ({tx},{ty}) mixes groups: {names}")
        for cy in range(s.h):
            for cx in range(s.w):
                sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                n = sum(1 for layer in s.layers.values() if (layer.a[sl][..., 3] > 0).any())
                if n == 3:
                    problems.append(f"{s.key} metatile ({cx},{cy}) has three layers")
                if (cx, cy) in gr:
                    if (s.B.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground draws a bottom")
                    if (s.T.a[sl][..., 3] > 0).any() and (s.M.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground uses both upper layers")
                    continue
                lower = np.maximum(s.B.a[sl][..., 3], s.M.a[sl][..., 3])
                if n and not (lower > 0).all():
                    problems.append(f"{s.key} ({cx},{cy}) has holes below the sprites layer")
    return problems


# --------------------------------------------------------------------------
# Ground and finishing
# --------------------------------------------------------------------------

def paving(L, x0, y0, w, h, ox=0, oy=0):
    """Thyrsa's street flags: irregular grey-buff slabs, thin joints. Repeats every
    32 px (two cells), so a street costs at most four cells' tiles."""
    fill_masonry(L, x0, y0, w, h, "flag", ox, oy)


def earth(L, x0, y0, w, h, ox=0, oy=0):
    """The vineyards' tilled earth, furrowed west-east. Repeats every 16 px."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - ox) % 16, (y - oy) % 16
            c = "e1"
            if Y in (4, 12):
                c = "e0"
            elif Y in (5, 13):
                c = "e2" if X % 5 else "e1"
            elif (X * 3 + Y * 7) % 19 == 0:
                c = "e0"
            L.px(x, y, c)


def finish(s, phase=(0, 0)):
    """Paint drawn ground under the art (paving phase-locked to the cell's map
    parity given by phase, in cells), then resolve layers as emporion_lib does."""
    B, M, T = s.B, s.M, s.T
    px, py = phase
    for (cx, cy), kind in s.ground.items():
        sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        if kind in ("pave", "earth"):
            g = Layer(16, 16)
            if kind == "pave":
                paving(g, 0, 0, 16, 16, ox=-16 * ((cx + px) % 2), oy=-16 * ((cy + py) % 2))
            else:
                earth(g, 0, 0, 16, 16)
            # the art drawn in the bottom layer moves up a layer, so the ground's
            # tiles stay pure and shared: a prop on the flags costs only its own
            art = B.a[sl].copy()
            if (art[..., 3] > 0).any():
                up = M.a[sl].copy()
                m = up[..., 3] > 0
                art[m] = up[m]
                M.a[sl] = art
            B.a[sl] = g.a
        if kind in E.BORROWED:
            continue
        hasM = (M.a[sl][..., 3] > 0).any()
        hasT = (T.a[sl][..., 3] > 0).any()
        if hasM and hasT:
            src = M.a[sl]
            m = src[..., 3] > 0
            B.a[sl][m] = src[m]
            M.a[sl] = 0
    return s


def recolor(s, mapping, key=None, title=None, notes=None):
    t = E.recolor(s, mapping, key=key, title=title, notes=notes)
    t.names = dict(getattr(s, "names", {}))
    return t


mirror = E.mirror
mirror_half = E.mirror_half
outline_rect = E.outline_rect


# Porytiles sorts each palette's colors by value, so a limewashed part is the
# ochre part's own 4bpp tile only if the two groups sort in step, slot for slot.
_clay = sorted(GROUPS["clay"], key=lambda n: C[n])
_lime = sorted(GROUPS["clay2"], key=lambda n: C[n])
assert [LIME[n] for n in _clay] == _lime, list(zip(_clay, _lime))
