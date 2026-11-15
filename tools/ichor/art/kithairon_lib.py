"""Shared toolkit for gTileset_Kithairon, the Kithairon crossing's secondary.

One secondary for all four outdoor maps of the crossing (Route 6, Eleutherai,
Mt. Kithairon, Route 7 and the Kronia grounds) and Antiope's cave, so their
shared seams need no aethos-only strip. It pairs with the aethos primary.

It draws with agros_lib's layers and structures and eleusa_lib's borrowed
ground, validation and tile merging, and adds:

  - Kithairon's palette plan: seven groups for the secondary's slots 6-12.
    Every 8x8 tile of every layer takes all its colors from one group.
  - A soft-shape engine for whole regions (tall grass, the road, crags with a
    south face, water with grassy banks), after agros_ground: a cell's piece is
    chosen by its blob key (eleusa_lib.blob_key), and pieces are cut from one
    continuous field, so any outline meets itself seamlessly.

All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
import eleusa_lib as E  # noqa: E402  (registers Eleusa's colors: lf*, pl*, rf*...)
from agros_lib import GRASS, PATH, SEA, TALL, Layer, Struct, aethos  # noqa: E402,F401

ROOT = A.ROOT

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # Kithairon's rock: a cool grey limestone, from crevice to sunlit edge
    "rk0": (40, 40, 48), "rk1": (80, 80, 88), "rk2": (120, 120, 120), "rk3": (160, 160, 152),
    "rk4": (200, 200, 184), "rk5": (232, 232, 216),
    # ivy, and the marked ivy of the Thyrsus walls (gold berries)
    "iv0": (32, 64, 40), "iv1": (64, 104, 48), "iv2": (112, 152, 64), "mk": (216, 176, 56),
    # black firs, from the shadow under the boughs to the lit tips
    "fr0": (16, 32, 32), "fr1": (32, 56, 48), "fr2": (56, 88, 64), "fr3": (96, 128, 80),
    # scrub oak and wild pear leaves
    "oa1": (64, 96, 40), "oa2": (104, 136, 56), "oa3": (152, 176, 80),
    # grapes
    "gp0": (56, 24, 64), "gp1": (104, 48, 112), "gp2": (160, 96, 168),
    # Cyclopean stone: huge warm grey blocks
    "cy0": (56, 48, 40), "cy1": (96, 88, 72), "cy2": (136, 128, 104), "cy3": (176, 168, 144),
    "cy4": (216, 208, 184),
    # the Kronia: red-and-cream awnings, canvas, gold cloth, figs
    "rd0": (136, 32, 40), "rd1": (200, 56, 48), "cn0": (152, 136, 104), "cn1": (240, 232, 208),
    "cn2": (200, 184, 152), "au0": (152, 96, 16), "au1": (216, 160, 40), "au2": (248, 216, 96),
    "pu1": (120, 56, 128),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

GRASS4 = ["g1", "g2", "g3", "gd"]

GROUPS = {
    # soft tall grass and road edges, river banks, the dancing floor, drums
    "field": GRASS4 + ["t0", "t1", "t3", "tg", "p1", "p2", "p3", "l0", "l1", "wd1", "ink"],
    # crags, rocks, ivy, the cave, shrines and boundary stones
    "rock": GRASS4 + ["rk0", "rk1", "rk2", "rk3", "rk4", "rk5", "iv0", "iv1", "iv2", "mk", "ink"],
    # firs, oaks, wild pears
    "tree": GRASS4 + ["fr0", "fr1", "fr2", "fr3", "oa1", "oa2", "oa3", "k1", "k2", "w0", "ink"],
    # vine trellises, the old vines across the road, the wine-cart's jars
    "vine": GRASS4 + ["lf0", "lf1", "lf2", "gp0", "gp1", "gp2", "wd1", "wd2", "tc1", "tc2", "ink"],
    # Eleusa's house kit, verbatim (plaster, roof tiles, timber, ox-blood, socle)
    "house": list(E.GROUPS["house"]),
    # Cyclopean walls, the old temple, the wine press, troughs, the fold
    "stone": GRASS4 + ["cy0", "cy1", "cy2", "cy3", "cy4", "p2", "p3", "gp0", "gp1", "l0", "ink"],
    # the Kronia's awnings, tables, tents, stage, banner and oven; braziers
    "camp": ["rd0", "rd1", "cn0", "cn1", "cn2", "au0", "au1", "au2", "pu1", "wd1", "wd2", "tc1",
             "g1", "gd", "ink"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# Borrowed ground: a cell's bottom layer pointed at aethos's own metatile.
GROUND_METATILE = {"grass": 0x001, "path": 0x1D9, "sea": 0x170, "tall": 0x00D, "shade": 0x01C}
E.GROUND_METATILE.update(GROUND_METATILE)    # E.composite/preview read it


def struct(key, title, w, h, section, walk=None, notes="", names=None, on=None):
    return E.struct(key, title, w, h, section, walk=walk, notes=notes, names=names, on=on)


ground = E.ground
put = E.put
validate = lambda structs: E.validate(structs, GROUP_RGB)  # noqa: E731
merge_near_duplicates = E.merge_near_duplicates
tiles_of = E.tiles_of
preview = E.preview
composite = E.composite
blob_key = E.blob_key


def hsh(x, y, k=0):
    h = (x * 374761393 + y * 668265263 + k * 2147483647) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h ^ (h >> 16)) & 0xFFFF


# --------------------------------------------------------------------------
# The soft-shape engine (after agros_ground): one 48 x 48 field per key
# --------------------------------------------------------------------------

DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]   # N NE E SE S SW W NW


def blob_keys():
    """The 47 shapes of a binary region cell (diagonals count only when both
    neighboring sides are in the region)."""
    keys = set()
    for bits in range(256):
        b = [(bits >> i) & 1 for i in range(8)]
        for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
            if not (b[a] and b[c]):
                b[d] = 0
        keys.add("1|" + "".join(str(v) for v in b))
    return sorted(keys)


def region(key):
    """48 x 48 bool canvas of the region around a cell (the cell in the middle)."""
    neigh = key.split("|")[1]
    R = np.zeros((48, 48), bool)
    R[16:32, 16:32] = True
    for st, (dx, dy) in zip(neigh, DIRS):
        if st == "1":
            R[16 + dy * 16:32 + dy * 16, 16 + dx * 16:32 + dx * 16] = True
    return R


def wobble(seed, amp, jag=0.0):
    y, x = np.mgrid[0:48, 0:48].astype(float)
    t = 2 * math.pi / 16
    f = (np.sin(t * 2 * x + seed) + np.sin(t * 2 * y + 1.7 * seed)
         + np.sin(t * (x + y) + 2.3 * seed) + 0.6 * np.sin(t * 3 * (x - y) + seed)) / 3.6
    saw = (((x.astype(int) * 3 + y.astype(int) * 5) % 4) / 1.5 - 1.0)
    return amp * f + jag * saw


def soft(key, margin, radius, amp, seed, jag=0.0):
    """The region opened by a rounded brush, over the whole 48 x 48 canvas.
    Only the middle cell and the parts of its neighbors within a few pixels of
    it are exact (the field reaches margin + radius + amp pixels)."""
    R = region(key)
    ys, xs = np.nonzero(~R)
    if len(ys) == 0:
        return np.ones((48, 48), bool)
    out = np.stack([ys, xs], 1).astype(np.float32)
    pts = np.argwhere(np.ones((48, 48), bool)).astype(np.float32)
    d_in = np.sqrt(((pts[:, None, :] - out[None, :, :]) ** 2).sum(-1)).min(1).reshape(48, 48)
    d_in[~R] = 0
    core = np.argwhere(d_in > margin + radius).astype(np.float32)
    if len(core) == 0:
        return np.zeros((48, 48), bool)
    d_core = np.sqrt(((pts[:, None, :] - core[None, :, :]) ** 2).sum(-1)).min(1).reshape(48, 48)
    return (d_core <= radius + wobble(seed, amp, jag)) & R


def ring(mask):
    p = np.pad(mask, 1, constant_values=True)
    inner = p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return mask & ~inner


def halo(mask):
    p = np.pad(mask, 1, constant_values=False)
    near = p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    return near & ~mask


def shape_set(key, title, section, keys, painter, walk_code, notes, on=None, behavior=None):
    """A Struct holding one piece per shape key, 8 per row; names map key -> cell.
    painter(struct, ox, oy, key) paints one 16 x 16 cell."""
    w = 8
    h = max(1, (len(keys) + w - 1) // w)
    names = {k: (i % w, i // w) for i, k in enumerate(keys)}
    s = struct(key, title, w, h, section, walk=[walk_code * w] * h, notes=notes, names=names)
    cells = [(i % w, i // w) for i in range(w * h)]
    if on:
        ground(s, on)
    for n, (cx, cy) in enumerate(cells):
        k = keys[min(n, len(keys) - 1)]       # the tail repeats the last piece
        painter(s, cx * 16, cy * 16, k)
        if behavior:
            s.behaviors[(cx, cy)] = behavior
    return s


# --------------------------------------------------------------------------
# Small drawing helpers
# --------------------------------------------------------------------------

def fill(L, x0, y0, w, h, fn):
    """Fill a box with fn(x, y) -> color name or None (absolute coordinates)."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            c = fn(x, y)
            if c:
                L.px(x, y, c)


def ellipse_mask(w, h, cx, cy, rx, ry):
    y, x = np.mgrid[0:h, 0:w]
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0


def shade_grass(L, x0, y0, w, h, step=1):
    """Paint a cast shadow onto grass pixels already on L: g3/g2 -> g1, g1 -> gd."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            c = L.get(x, y)
            if c in ("g2", "g3"):
                L.px(x, y, "g1" if step == 1 or (x + y) % 2 else "g2")
            elif c == "g1" and step == 1:
                L.px(x, y, "gd")


def grass_under(L, x0, y0, w, h):
    """aethos grass, phase-locked to the 16 px grid."""
    L.texture(GRASS, x0, y0, w, h)


# --------------------------------------------------------------------------
# Mock compositions (painting previews before the maps exist)
# --------------------------------------------------------------------------

def mock(layers, w, h, base=None):
    """Compose an image from [(struct, {(x, y): name})] layers of shape-set or
    structure cells over aethos grass. Later layers draw over earlier ones
    (a cell keeps the last piece put on it)."""
    out = np.zeros((h * 16, w * 16, 3), np.uint8)
    g = aethos(base or GRASS)
    for y in range(h):
        for x in range(w):
            out[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = g
    for s, cells in layers:
        img = composite(s)
        for (x, y), name in cells.items():
            cx, cy = s.names[name] if isinstance(name, str) else name
            out[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = img[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
    return out


def shape_cells(rows, ch, x0=0, y0=0):
    """{(x, y): blob key} for the cells of `ch` in an ASCII grid."""
    reg = [[c == ch for c in r] for r in rows]
    return {(x0 + x, y0 + y): blob_key(reg, x, y)
            for y, r in enumerate(rows) for x, c in enumerate(r) if c == ch}


def crop(s, key, title, names, cols=8, notes=None):
    """A new structure holding some named cells of s, packed in rows of `cols`.
    Layers, walk codes, behaviors and borrowed ground come along."""
    order = list(names)
    w = min(cols, len(order))
    h = (len(order) + w - 1) // w
    walk = [["X"] * w for _ in range(h)]
    out = Struct(key, title, w, h, s.section, notes=notes if notes is not None else s.notes,
                 names={n: (i % w, i // w) for i, n in enumerate(order)})
    out.ground = {}
    gr = getattr(s, "ground", {})
    for i, n in enumerate(order):
        sx, sy = s.names[n]
        dx, dy = i % w, i // w
        for ln in ("bottom", "middle", "top"):
            out.layers[ln].a[dy * 16:dy * 16 + 16, dx * 16:dx * 16 + 16] = \
                s.layers[ln].a[sy * 16:sy * 16 + 16, sx * 16:sx * 16 + 16]
        walk[dy][dx] = s.walk[sy][sx]
        if (sx, sy) in s.behaviors:
            out.behaviors[(dx, dy)] = s.behaviors[(sx, sy)]
        if (sx, sy) in gr:
            out.ground[(dx, dy)] = gr[(sx, sy)]
    # pad a short last row by repeating the last cell (no holes in the sheet)
    last = len(order) - 1
    lx, ly = last % w, last // w
    for i in range(len(order), w * h):
        dx, dy = i % w, i // w
        for ln in ("bottom", "middle", "top"):
            out.layers[ln].a[dy * 16:dy * 16 + 16, dx * 16:dx * 16 + 16] = \
                out.layers[ln].a[ly * 16:ly * 16 + 16, lx * 16:lx * 16 + 16]
        walk[dy][dx] = walk[ly][lx]
        if (lx, ly) in out.ground:
            out.ground[(dx, dy)] = out.ground[(lx, ly)]
        if (lx, ly) in out.behaviors:
            out.behaviors[(dx, dy)] = out.behaviors[(lx, ly)]
    out.walk = ["".join(r) for r in walk]
    return out
