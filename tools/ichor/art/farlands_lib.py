"""Shared toolkit for the far lands' secondaries: the steppe family (steppe,
steppe_town, steppe_camp) and the far-west family (far_west, hesperides).

These are the edges of the known world: Thrace, the Thermodon and the
Scythian steppe to the north-east; Erytheia, the Pillars, the Garden of the
Hesperides and the Atlas range at the sunset end. Labors 8-11 (LABORS.md) and
the Oikoumene's lands (OIKOUMENE.md 4.3, 4.4, 4.8) both build on them.

The machinery is world-act3's kythera_lib (Kythera and Melos), ported here so
these sets own their copy:

  - A palette plan per tileset: seven groups for the secondary's palettes
    6-12 (GROUPS[tileset]). Every 8x8 tile of every layer, and of every
    animation frame, takes all its colors from one group; validate() enforces
    it, and the groups go to Porytiles as packing hints.
  - Borrowed ground. A cell can sit on aethos's grass, limestone path, sand,
    sea, turquoise shallows or falling water. Its bottom layer stays empty in
    the sources; after Porytiles compiles, farlands_build.py points the cell's
    bottom tiles at aethos's own ground metatile (GROUND_METATILE). This is how
    every piece here meets aethos ground without a seam, and why the seam
    strips MAP_DESIGN 5 asks for are easy: everything fades onto aethos.
  - Animations: a structure carries extra frames of one layer
    (Struct.anims[name]); every 8x8 tile that changes becomes a Porytiles
    animated tile.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
from agros_lib import Layer, Struct, aethos  # noqa: E402,F401

ROOT = A.ROOT

# --------------------------------------------------------------------------
# Colors: agros's names (aethos ground, sea, grass...), plus the far lands'
# --------------------------------------------------------------------------

NEW = {
    # aethos's sand and turquoise shallows, exactly
    "ks1": (200, 168, 104), "ks2": (232, 208, 144), "kq1": (88, 176, 200),
    # --- the steppe ---
    # straw gold: the long steppe grass, thatch, dry tussocks
    "sg0": (104, 72, 32), "sg1": (160, 112, 40), "sg2": (208, 160, 64), "sg3": (232, 200, 104),
    "sg4": (248, 232, 168),
    # short dry turf, grazed down
    "dt1": (168, 152, 80), "dt2": (200, 176, 96), "dt3": (224, 208, 136),
    # meadow flowers: poppy, cornflower
    "pp": (216, 48, 40), "cf": (88, 104, 200),
    # dirt road and mud
    "rd0": (88, 64, 40), "rd3": (208, 176, 128),
    "md0": (64, 48, 32), "md1": (104, 80, 56), "md2": (144, 120, 88),
    # reeds and cattails
    "rg1": (48, 80, 40), "rg2": (88, 128, 56), "rg3": (152, 168, 88),
    "rb1": (120, 72, 40), "rb2": (168, 112, 64),
    # grey field stone (babas, kerbs, markers), lichen
    "sn0": (64, 64, 72), "sn1": (104, 104, 112), "sn2": (152, 152, 152), "sn3": (200, 200, 192),
    "lc": (200, 192, 88),
    # the Arimaspian heights: brown-grey rock, gold in the veins, old bone
    "hr0": (72, 56, 48), "hr1": (112, 96, 80), "hr2": (160, 144, 120), "hr3": (200, 184, 160),
    "hr4": (232, 224, 200), "au1": (200, 152, 40), "au2": (248, 216, 80),
    "bn1": (200, 192, 168), "bn2": (240, 232, 208),
    # willow and poplar
    "wl1": (40, 72, 48), "wl2": (72, 112, 64), "wl3": (120, 152, 88), "wl4": (168, 184, 120),
    # timber, from the tarred post to the sun-bleached plank
    "tb0": (56, 40, 32), "tb1": (96, 64, 40), "tb2": (136, 96, 56), "tb3": (176, 136, 88),
    "tb4": (216, 184, 136),
    # mud-brick and daub
    "mb1": (152, 112, 72), "mb2": (192, 152, 104), "mb3": (224, 192, 144),
    # felt: Scythian red, undyed cream, a blue appliqué
    "fr0": (80, 24, 24), "fr1": (144, 40, 32), "fr2": (192, 64, 40), "fr3": (224, 112, 72),
    "fc0": (152, 136, 104), "fc1": (208, 192, 152), "fc2": (240, 232, 200), "fb": (48, 72, 136),
    # Thracian bronze and verdigris, fire and ash
    "bz0": (72, 48, 32), "bz1": (136, 96, 48), "bz2": (200, 152, 72), "bz3": (240, 208, 128),
    "vg1": (64, 128, 112),
    "fi1": (248, 224, 112), "fi2": (240, 144, 48), "fi3": (192, 64, 32), "as1": (96, 88, 88),
    # --- the far west ---
    # red earth
    "re0": (80, 32, 32), "re1": (128, 56, 40), "re2": (168, 80, 48), "re3": (200, 112, 64),
    "re4": (224, 152, 96),
    # sunset-lit grass
    "dg0": (72, 48, 40), "dg1": (128, 88, 48), "dg2": (184, 128, 56), "dg3": (224, 168, 72),
    "dg4": (248, 208, 112),
    # evening: violet shadow, pink and gold light
    "ev0": (48, 40, 72), "ev1": (88, 72, 112), "ev2": (136, 112, 152), "ev3": (184, 160, 192),
    "pk1": (216, 112, 112), "pk2": (240, 168, 152), "gl": (248, 232, 144),
    # red rock lit by the sunset
    "rr0": (64, 32, 32), "rr1": (112, 56, 48), "rr2": (160, 88, 64), "rr3": (200, 128, 88),
    "rr4": (232, 176, 128),
    # maquis: lentisk, dwarf palm, broom
    "mq0": (32, 48, 32), "mq1": (56, 80, 48), "mq2": (88, 112, 56), "mq3": (136, 144, 72),
    # marble in evening light
    "ml0": (104, 88, 96), "ml1": (152, 136, 136), "ml2": (200, 184, 176), "ml3": (232, 224, 208),
    # slag and mine spoil
    "sl0": (24, 24, 32), "sl1": (48, 48, 64), "sl2": (88, 80, 96),
    # the night sky past the edge of the world
    "ns0": (16, 16, 48), "ns1": (32, 40, 88), "ns2": (64, 72, 136),
    # --- the Garden and Atlas ---
    # the garden's evening greens
    "hg0": (32, 64, 56), "hg1": (56, 104, 72), "hg2": (96, 144, 88), "hg3": (152, 184, 104),
    "hg4": (200, 216, 136),
    # golden apples
    "ap0": (136, 80, 24), "ap1": (200, 136, 32), "ap2": (240, 192, 56), "ap3": (248, 232, 136),
    # Ladon's scales
    "ld0": (24, 56, 56), "ld1": (40, 96, 88), "ld2": (72, 144, 112), "ld3": (136, 192, 136),
    # cold high rock and the snowline
    "cr0": (48, 48, 64), "cr1": (88, 88, 104), "cr2": (136, 128, 144), "cr3": (184, 176, 184),
    "sw1": (168, 176, 208), "sw2": (216, 224, 240),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C
_dups = {}
for _n, _c in C.items():
    _dups.setdefault(_c, []).append(_n)

# aethos ground a cell can borrow (its bottom-layer tiles)
GROUND_METATILE = {"grass": 0x001, "path": 0x1D9, "sand": 0x124, "sea": 0x170,
                   "shallow": 0x0D1, "fall": 0x0B3}

# walk codes -> metatile behaviors
WALK_BEHAVIOR = {
    "G": "MB_TALL_GRASS", "L": "MB_LONG_GRASS", "J": "MB_JUMP_SOUTH", "<": "MB_JUMP_WEST",
    ">": "MB_JUMP_EAST", "^": "MB_JUMP_NORTH", "D": "MB_NON_ANIMATED_DOOR",
    "W": "MB_OCEAN_WATER", "P": "MB_POND_WATER", "H": "MB_SHALLOW_WATER", "F": "MB_WATERFALL",
    "S": "MB_SAND", "M": "MB_PUDDLE",
}
WALK_CODES = {
    "X": "Impassable: set collision 1.",
    ".": "Passable.",
    "T": "Passable, drawn over the player, who walks behind it.",
    "G": "Tall grass: `MB_TALL_GRASS`, wild encounters. Passable.",
    "L": "Long grass or reeds: `MB_LONG_GRASS`, wild encounters. Passable.",
    "D": "Door: `MB_NON_ANIMATED_DOOR`. Put the warp here.",
    "W": "Sea: `MB_OCEAN_WATER`, surfable (collision 0).",
    "P": "Fresh water: `MB_POND_WATER`, surfable.",
    "H": "Shallow water: `MB_SHALLOW_WATER`, walkable, splashes.",
    "M": "Mud or a puddle: `MB_PUDDLE`, walkable.",
    "F": "Waterfall: `MB_WATERFALL`.",
    "J": "Ledge: `MB_JUMP_SOUTH`.",
    "<": "Ledge: `MB_JUMP_WEST`.",
    ">": "Ledge: `MB_JUMP_EAST`.",
    "S": "Sand: `MB_SAND`.",
}

# --------------------------------------------------------------------------
# Structures
# --------------------------------------------------------------------------


def struct(key, title, w, h, section, walk=None, notes="", names=None, on=None, oik=False):
    """A Struct whose walk codes set its behaviors, optionally on borrowed
    ground everywhere ('grass', 'sand', 'sea'...). oik=True marks a piece
    drawn for the Oikoumene's lands (the catalogs flag it)."""
    s = Struct(key, title, w, h, section, walk=walk, notes=notes, names=names)
    s.behaviors = {}
    for cy, row in enumerate(s.walk):
        for cx, ch in enumerate(row):
            if ch in WALK_BEHAVIOR:
                s.behaviors[(cx, cy)] = WALK_BEHAVIOR[ch]
    s.anims = {}
    s.ground = {}
    s.oik = oik
    if on:
        ground(s, on)
    return s


def set_walk(s, walk):
    """Replace a structure's walk codes and the behaviors they imply (keeping
    behaviors set by hand for cells whose code has none)."""
    s.walk = list(walk)
    keep = {k: v for k, v in s.behaviors.items() if s.walk[k[1]][k[0]] not in WALK_BEHAVIOR
            and s.walk[k[1]][k[0]] not in "X.T"}
    s.behaviors = keep
    for cy, row in enumerate(s.walk):
        for cx, ch in enumerate(row):
            if ch in WALK_BEHAVIOR:
                s.behaviors[(cx, cy)] = WALK_BEHAVIOR[ch]


def ground(s, kind, cells=None):
    """Put cells (default: all) on borrowed aethos ground. Their bottom layer
    stays empty: the build supplies aethos's ground there."""
    assert kind in GROUND_METATILE, kind
    cells = cells if cells is not None else [(x, y) for y in range(s.h) for x in range(s.w)]
    for (cx, cy) in cells:
        s.ground[(cx, cy)] = kind
        s.B.rect(cx * 16, cy * 16, 16, 16, None)


def anim_layer(s, name, n, layer="middle"):
    """Start an animation on one of s's layers: returns n-1 extra frame Layers,
    each a copy of the layer as it is now (frame 0 is the layer itself)."""
    src = s.layers[layer]
    frames = []
    for _ in range(n - 1):
        L = Layer(src.w, src.h)
        L.a[:] = src.a
        frames.append(L)
    s.anims[name] = {"layer": layer, "frames": frames}
    return frames


def settle(s, name, cells):
    """Declare every cell of s outside `cells` static for animation `name`."""
    an = s.anims[name]
    base = s.layers[an["layer"]].a
    cells = set(cells)
    for cy in range(s.h):
        for cx in range(s.w):
            if (cx, cy) in cells:
                continue
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            for f in an["frames"]:
                f.a[sl] = base[sl]


def pick(s, names, w=None, key=None, title=None, notes=None, section=None, oik=None):
    """A new structure holding only the named single cells of s, in rows of w."""
    names = list(names)
    w = w or len(names)
    hh = (len(names) + w - 1) // w
    cells = [s.names[n] for n in names]
    walk = []
    for j in range(hh):
        row = ""
        for i in range(w):
            k = j * w + i
            c = cells[k] if k < len(cells) else cells[-1]
            row += s.walk[c[1]][c[0]]
        walk.append(row)
    c = struct(key or s.key, title or s.title, w, hh, section or s.section, walk=walk,
               notes=notes if notes is not None else s.notes,
               names={n: (k % w, k // w) for k, n in enumerate(names)},
               oik=s.oik if oik is None else oik)
    srcs = dict(s.anims)
    frames = {an: [Layer(w * 16, hh * 16) for _ in v["frames"]] for an, v in srcs.items()}
    for k in range(w * hh):
        sx, sy = cells[min(k, len(cells) - 1)]
        dx, dy = k % w, k // w
        ssl = np.s_[sy * 16:sy * 16 + 16, sx * 16:sx * 16 + 16]
        dsl = np.s_[dy * 16:dy * 16 + 16, dx * 16:dx * 16 + 16]
        for ln in ("bottom", "middle", "top"):
            c.layers[ln].a[dsl] = s.layers[ln].a[ssl]
        if (sx, sy) in s.ground:
            c.ground[(dx, dy)] = s.ground[(sx, sy)]
        if (sx, sy) in s.behaviors:
            c.behaviors[(dx, dy)] = s.behaviors[(sx, sy)]
        for an, v in srcs.items():
            for fi, f in enumerate(v["frames"]):
                frames[an][fi].a[dsl] = f.a[ssl]
    for an, v in srcs.items():
        c.anims[an] = {"layer": v["layer"], "frames": frames[an]}
    return c


def copy_struct(s, key=None, title=None, notes=None, section=None, oik=None):
    c = struct(key or s.key, title or s.title, s.w, s.h, section or s.section, walk=list(s.walk),
               notes=notes if notes is not None else s.notes, names=dict(s.names),
               oik=s.oik if oik is None else oik)
    for ln in ("bottom", "middle", "top"):
        c.layers[ln].a[:] = s.layers[ln].a
    c.behaviors = dict(s.behaviors)
    c.ground = dict(s.ground)
    for name, an in s.anims.items():
        fr = []
        for f in an["frames"]:
            L = Layer(f.w, f.h)
            L.a[:] = f.a
            fr.append(L)
        c.anims[name] = {"layer": an["layer"], "frames": fr}
    return c


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def h(x, y, k=0):
    """A cheap hash of a pixel position, 0..96."""
    return (x * 73 + y * 151 + k * 37 + (x * y + k) % 7) % 97


def hp(x, y, k=0, period=16):
    """h() on 16 px periodic coordinates, so textures tile."""
    return h(x % period, y % period, k)


def put(L, x, y, rows, legend, hflip=False):
    """Blit an ASCII grid with a legend of color names; ' ' and '.' are skipped."""
    for j, row in enumerate(rows):
        if hflip:
            row = row[::-1]
        for i, ch in enumerate(row):
            if ch in " ." or ch not in legend:
                continue
            L.px(x + i, y + j, legend[ch])


def tex(L, mid, x, y, w, h_, mask=None):
    """Fill with an aethos metatile's pixels, locked to the 16 px grid."""
    L.texture(mid, x, y, w, h_, mask)


def aethos_px(mid, X, Y, remap=None):
    """aethos metatile `mid`'s color name at absolute pixel (X, Y)."""
    rgb = tuple(int(v) for v in aethos(mid)[Y % 16, X % 16])
    n = A.RGB2NAME[rgb]
    if remap and n in remap:
        n = remap[n]
    return n


def grass_px(X, Y, no_g3=False):
    return aethos_px(0x001, X, Y, {"g3": "g2"} if no_g3 else None)


def sand_px(X, Y):
    return aethos_px(0x124, X, Y)


def path_px(X, Y):
    return aethos_px(0x1D9, X, Y)


def tile_colors(layer, tx, ty):
    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
    m = t[..., 3] > 0
    return {tuple(int(v) for v in p) for p in t[m][:, :3]}


def mask_from(fn, w, h_):
    m = np.zeros((h_, w), bool)
    for y in range(h_):
        for x in range(w):
            m[y, x] = bool(fn(x, y))
    return m


def paint_mask(L, mask, fn, ox=0, oy=0):
    """For every True pixel of mask, paint fn(x, y) (local coords) at ox+x, oy+y."""
    ys, xs = np.nonzero(mask)
    for y, x in zip(ys, xs):
        c = fn(int(x), int(y))
        if c:
            L.px(ox + int(x), oy + int(y), c)


def edge_of(mask):
    """Pixels of mask that touch a pixel outside it (4-neighborhood)."""
    p = np.pad(mask, 1, constant_values=False)
    inner = p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return mask & ~inner


def halo_of(mask):
    p = np.pad(mask, 1, constant_values=False)
    near = p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    return near & ~mask


def shadow_below(L, mask, colors, dy=1, ox=0, oy=0, only_empty=True):
    """Paint a soft drop shadow below a mask: colors[0] nearest."""
    hh, ww = mask.shape
    for y in range(hh):
        for x in range(ww):
            if mask[y, x]:
                continue
            for i, c in enumerate(colors):
                yy = y - (i + dy)
                if 0 <= yy < hh and mask[yy, x]:
                    if not only_empty or L.get(ox + x, oy + y) is None:
                        L.px(ox + x, oy + y, c)
                    break


# --------------------------------------------------------------------------
# Foliage (kythera_land's), lit from the top left
# --------------------------------------------------------------------------

def foliage(L, mask, ramp, seed=0, outline=None, clump=4.0, flowers=None, fl_rate=0,
            periodic=True):
    """Shade a foliage mass as clumps of leaves lit from the top left. ramp is
    dark -> light (4 colors). flowers: colors dotted over the lit side."""
    hgt, wid = mask.shape
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return
    n = int(round(16 / clump))
    cl = 16 / n
    for y, x in zip(ys, xs):
        x, y = int(x), int(y)
        px_, py_ = (x % 16, y % 16) if periodic else (x, y)
        best, bd = None, 1e9
        gx, gy = int(px_ // cl), int(py_ // cl)
        for j in (gy - 1, gy, gy + 1):
            for i in (gx - 1, gx, gx + 1):
                hh = h(i % n if periodic else i, j % n if periodic else j, seed + 3)
                cx_ = (i + 0.25 + (hh % 6) / 10) * cl
                cy_ = (j + 0.25 + ((hh // 6) % 6) / 10) * cl
                d = (px_ - cx_) ** 2 + (py_ - cy_) ** 2
                if d < bd:
                    bd, best = d, (cx_, cy_)
        dx, dy = px_ - best[0], py_ - best[1]
        t = dx + dy
        lvl = 2 if t < -1.0 else (1 if t < 1.5 else 0)
        up = sum(1 for k in range(1, 4) if y - k < 0 or not mask[y - k, x])
        left = sum(1 for k in range(1, 3) if x - k < 0 or not mask[y, x - k])
        down = sum(1 for k in range(1, 4) if y + k >= hgt or not mask[y + k, x])
        if up >= 2 or (left >= 2 and up >= 1):
            lvl += 1
        if down >= 2:
            lvl -= 1
        lvl = max(0, min(3, lvl + 1 if lvl < 3 else 3))
        L.px(x, y, ramp[lvl])
        if flowers and lvl >= 2 and hp(x, y, seed + 9) % fl_rate == 0:
            L.px(x, y, flowers[hp(x, y, seed + 1) % len(flowers)])
    if outline:
        sub = Layer(wid, hgt)
        sub.mask_fill(mask, ramp[0])
        sub.outline(outline)
        for y, x in zip(*np.nonzero(sub.a[..., 3] > 0)):
            if sub.get(int(x), int(y)) == outline:
                L.px(int(x), int(y), outline)


def blob(cx, cy, rx, ry, w, h_, wobble=0.0, k=6, seed=0.0):
    """Bool mask (h_, w) of a wobbly ellipse."""
    y, x = np.mgrid[0:h_, 0:w].astype(float)
    ang = np.arctan2(y - cy, x - cx)
    r = np.hypot((x - cx) / rx, (y - cy) / ry)
    return r < 1 + wobble * np.sin(ang * k + seed)


# --------------------------------------------------------------------------
# Animation bookkeeping
# --------------------------------------------------------------------------

def anim_tiles(s):
    """{(layer name, tx, ty): anim name} for every tile that changes between frames."""
    out = {}
    for name, an in s.anims.items():
        base = s.layers[an["layer"]].a
        for f in an["frames"]:
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                    if not np.array_equal(base[sl], f.a[sl]):
                        out[(an["layer"], tx, ty)] = name
    return out


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def group_rgb(groups):
    return {g: {C[n] for n in names} for g, names in groups.items()}


def check_groups(groups, label):
    assert len(groups) <= 7, (label, len(groups))
    for g, names in groups.items():
        assert len(names) <= 15, (label, g, len(names))
        assert len(set(C[n] for n in names)) == len(names), (label, g, "duplicate colors")
        for n in names:
            assert n in C, (label, n)


def validate(structs, grgb):
    """Problems: a tile (over all its frames) whose colors fit no group, three
    layers in one cell, holes under the sprite layer, bad borrowed cells."""
    problems = []
    for s in structs:
        gr = s.ground
        at = anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    cols = tile_colors(layer, tx, ty)
                    if (ln, tx, ty) in at:
                        an = s.anims[at[(ln, tx, ty)]]
                        for f in an["frames"]:
                            cols |= tile_colors(f, tx, ty)
                    if cols and not any(cols <= g for g in grgb.values()):
                        names = sorted(A.RGB2NAME.get(c, str(c)) for c in cols)
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
                    problems.append(f"{s.key} metatile ({cx},{cy}) has holes below the sprites layer")
                if n == 0:
                    problems.append(f"{s.key} metatile ({cx},{cy}) is empty")
    return problems


def which_group(cols, grgb):
    for g, rgb in grgb.items():
        if cols <= rgb:
            return g
    return None


def tile_report(structs, grgb):
    """Which colors in a mixed tile fall outside the group that fits best."""
    out = []
    for s in structs:
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in s.ground:
                        continue
                    cols = tile_colors(layer, tx, ty)
                    if not cols or any(cols <= g for g in grgb.values()):
                        continue
                    best = max(grgb, key=lambda g: len(cols & grgb[g]))
                    extra = sorted(A.RGB2NAME.get(c, str(c)) for c in cols - grgb[best])
                    out.append(f"{s.key} {ln} ({tx},{ty}): best {best}, extra {extra}")
    return out


# --------------------------------------------------------------------------
# Previews with the real aethos ground
# --------------------------------------------------------------------------

def composite(s, frame=0):
    out = np.zeros((s.h * 16, s.w * 16, 3), np.uint8)
    out[:] = (255, 0, 255)
    gr = s.ground
    for ln in ("bottom", "middle", "top"):
        a = s.layers[ln].a
        for an in s.anims.values():
            if an["layer"] == ln and frame and frame - 1 < len(an["frames"]):
                a = an["frames"][frame - 1].a
        m = a[..., 3] > 0
        if ln == "bottom":
            m = m.copy()
            for (cx, cy), kind in gr.items():
                out[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = aethos(GROUND_METATILE[kind])
                m[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = False
        out[m] = a[..., :3][m]
    return out


def shelf_preview(structs, scale=2, width=1500, bg=(40, 40, 48), frame=0):
    """Pieces laid left to right in rows up to `width` px, labelled."""
    from PIL import Image, ImageDraw
    pad = 8
    imgs = [(s.key + (" *" if getattr(s, "oik", False) else ""),
             Image.fromarray(composite(s, frame)).resize((s.w * 16 * scale, s.h * 16 * scale),
                                                         Image.NEAREST)) for s in structs]
    rows, cur, cw = [], [], pad
    for k, i in imgs:
        w = max(i.width, len(k) * 6) + pad
        if cur and cw + w > width:
            rows.append(cur)
            cur, cw = [], pad
        cur.append((k, i))
        cw += w
    if cur:
        rows.append(cur)
    height = sum(max(i.height for _, i in r) + pad + 12 for r in rows) + pad
    out = Image.new("RGB", (width, height), bg)
    d = ImageDraw.Draw(out)
    y = pad
    for r in rows:
        x = pad
        for key, i in r:
            d.text((x, y), key, fill=(230, 230, 200))
            out.paste(i, (x, y + 12))
            x += max(i.width, len(key) * 6) + pad
        y += max(i.height for _, i in r) + pad + 12
    return out


# --------------------------------------------------------------------------
# Tile accounting, and near-duplicate merging (animated tiles excluded)
# --------------------------------------------------------------------------

def _flips(t):
    return (t, t[:, ::-1], t[::-1, :], t[::-1, ::-1])


def tiles_of(structs, include_anim=True):
    occ = {}
    for s in structs:
        gr = s.ground
        at = anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    if not include_anim and (ln, tx, ty) in at:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    occ.setdefault(min(v.tobytes() for v in _flips(t)), []).append((s.key, layer, tx, ty))
    return occ


def tile_cost(structs):
    """Distinct tiles per structure key (a tile shared by several counts for the first)."""
    seen, cost = set(), {}
    for s in structs:
        n = 0
        for k, occ in tiles_of([s]).items():
            if k not in seen:
                seen.add(k)
                n += 1
        cost[s.key] = n
    return cost


def merge_near_duplicates(structs, limit, grgb):
    occ = tiles_of(structs, include_anim=False)
    keys = list(occ)
    if not keys:
        return []
    arr = {k: np.frombuffer(k, np.uint8).reshape(8, 8, 4) for k in keys}

    def grp(k):
        a = arr[k]
        m = a[..., 3] > 0
        return which_group({tuple(int(v) for v in p) for p in a[m][:, :3]}, grgb)
    groups = {k: grp(k) for k in keys}
    flat = np.stack([arr[k].reshape(64, 4) for k in keys])
    pairs = []
    for i, k in enumerate(keys):
        best = None
        for v in _flips(arr[k]):
            d = (flat != v.reshape(1, 64, 4)).any(-1).sum(-1)
            best = d if best is None else np.minimum(best, d)
        for j in np.nonzero(best <= limit)[0]:
            if j > i:
                pairs.append((int(best[j]), i, int(j)))
    pairs.sort()
    dropped, kept, merges = set(), set(), []
    for d, i, j in pairs:
        a, b = keys[i], keys[j]
        if a in dropped or b in dropped or groups[a] != groups[b]:
            continue
        if ((arr[a][..., 3] > 0) != (arr[b][..., 3] > 0)).any() and \
                all(((v[..., 3] > 0) != (arr[a][..., 3] > 0)).any() for v in _flips(arr[b])):
            continue
        keep, drop = (a, b) if len(occ[a]) >= len(occ[b]) else (b, a)
        if drop in kept:
            keep, drop = drop, keep
            if drop in kept:
                continue
        for (_, layer, tx, ty) in occ[drop]:
            cur = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            best = min(_flips(arr[keep]), key=lambda v: int((cur != v).any(-1).sum()))
            if ((best[..., 3] > 0) != (cur[..., 3] > 0)).any():
                continue
            layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = best
        dropped.add(drop)
        kept.add(keep)
        merges.append(d)
    return merges


# --------------------------------------------------------------------------
# Shape keys for soft ground, from a region mask (map builders use this)
# --------------------------------------------------------------------------

NEIGHBORS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def blob_key(region, x, y):
    """The shape key of cell (x, y) in a boolean region grid [y][x]: '1|' then
    N NE E SE S SW W NW, a diagonal counting only when both of its sides are in
    the region. Cells off the grid count as in the region."""
    hh, ww = len(region), len(region[0])

    def at(i, j):
        if not (0 <= i < ww and 0 <= j < hh):
            return 1
        return 1 if region[j][i] else 0
    b = [at(x + dx, y + dy) for dx, dy in NEIGHBORS]
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] and b[c]):
            b[d] = 0
    return "1|" + "".join(str(v) for v in b)


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def dist(x0, y0, x1, y1):
    return math.hypot(x1 - x0, y1 - y0)
