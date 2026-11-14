"""Soft-edged ground for Agros: tall grass, the limestone path, goat tracks.

Each piece is drawn from a cell's 3x3 neighborhood. The region (tall grass,
path...) is the union of its cells at pixel level, plus a triangle for a path
"half cell" that cuts a stair-step corner on the diagonal. The visible shape is
that region opened with a rounded brush: shrunk by a margin, then grown back by
a corner radius, its edge wobbled by a 16 px periodic noise. Because every
piece is cut from the same field and the field only reaches a few pixels, the
pieces meet seamlessly in any arrangement, and their 8x8 quarters repeat, so
the whole set costs few tiles.

Shape keys (used by map builders): the cell and its neighbors N NE E SE S SW W
NW, each one character: "1" region, "0" not region, and for paths "/" or "\\"
for half cells, named by where their path triangle sits ("a" NE, "b" SE, "c"
SW, "d" NW), e.g. "1|1a011101".
"""
from __future__ import annotations

import math

import numpy as np

from agros_lib import GRASS, PATH, TALL, Struct

DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]  # N NE E SE S SW W NW
HALF = {"a": "NE", "b": "SE", "c": "SW", "d": "NW"}


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


def canon(center, neigh):
    """Shape key for a cell: center state and its 8 neighbor states."""
    return center + "|" + "".join(neigh)


def _triangle(where):
    """16x16 mask of a half cell's path triangle."""
    y, x = np.mgrid[0:16, 0:16]
    return {"NE": x >= y, "SE": x + y >= 15, "SW": x <= y, "NW": x + y <= 15}[where]


def region_canvas(key):
    """48x48 bool canvas of the region around a cell."""
    center, neigh = key.split("|")
    states = [center] + list(neigh)
    offsets = [(0, 0)] + DIRS
    R = np.zeros((48, 48), bool)
    for st, (dx, dy) in zip(states, offsets):
        x0, y0 = 16 + dx * 16, 16 + dy * 16
        if st == "1":
            R[y0:y0 + 16, x0:x0 + 16] = True
        elif st in HALF:
            R[y0:y0 + 16, x0:x0 + 16] |= _triangle(HALF[st])
    return R


def wobble(seed, amp, jag=0.0):
    """A 16 px periodic noise field in about [-amp-jag, amp+jag]: a slow swell,
    plus `jag`, a fine 4 px saw that reads as blade tips along an edge."""
    y, x = np.mgrid[0:48, 0:48].astype(float)
    t = 2 * math.pi / 16
    f = (np.sin(t * 2 * x + seed) + np.sin(t * 2 * y + 1.7 * seed)
         + np.sin(t * (x + y) + 2.3 * seed) + 0.6 * np.sin(t * 3 * (x - y) + seed)) / 3.6
    saw = (((x.astype(int) * 3 + y.astype(int) * 5) % 4) / 1.5 - 1.0)
    return amp * f + jag * saw


def visible(key, margin, radius, amp, seed, jag=0.0):
    """Center cell's 16x16 visible mask: the region opened by a rounded brush."""
    R = region_canvas(key)
    pts = np.argwhere(np.ones((48, 48), bool)).astype(np.float32)          # (y, x) of every pixel
    outside = np.argwhere(~R).astype(np.float32)
    if len(outside) == 0:
        return np.ones((16, 16), bool), R
    d_in = np.sqrt(((pts[:, None, :] - outside[None, :, :]) ** 2).sum(-1)).min(1).reshape(48, 48)
    d_in[~R] = 0
    core = np.argwhere(d_in > margin + radius).astype(np.float32)
    center = np.argwhere(np.ones((16, 16), bool)).astype(np.float32) + 16
    if len(core) == 0:
        return np.zeros((16, 16), bool), R
    d_core = np.sqrt(((center[:, None, :] - core[None, :, :]) ** 2).sum(-1)).min(1).reshape(16, 16)
    n = wobble(seed, amp, jag)[16:32, 16:32]
    vis = (d_core <= radius + n) & R[16:32, 16:32]
    return vis, R


def ring(mask):
    """Pixels of `mask` that touch a pixel outside it (4-neighborhood)."""
    p = np.pad(mask, 1, constant_values=True)
    inner = p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return mask & ~inner


def halo(mask):
    """Pixels outside `mask` that touch it."""
    p = np.pad(mask, 1, constant_values=False)
    near = p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    return near & ~mask


# --------------------------------------------------------------------------
# Painters for one 16x16 cell
# --------------------------------------------------------------------------

def paint_tall(L, ox, oy, key):
    """Barley meeting grass: the clump keeps a dark rim, and a few awns lean out."""
    vis, _ = visible(key, margin=1.0, radius=3.0, amp=1.4, seed=1.1, jag=1.2)
    L.texture(GRASS, ox, oy, 16, 16)
    L.texture(TALL, ox, oy, 16, 16, vis)
    for y, x in np.argwhere(ring(vis)):
        # keep the barley's own dark shading where it already is, darken the rest
        if tuple(L.a[oy + y, ox + x, :3]) not in ((40, 56, 32),):
            L.px(ox + x, oy + y, "t1")
    # awns: short stems poking up out of the clump's top edge
    for y, x in np.argwhere(halo(vis)):
        if y + 1 < 16 and vis[y + 1, x] and (x * 5 + y * 3) % 7 == 0:
            L.px(ox + x, oy + y, "t3")
            if y - 1 >= 0 and not vis[y - 1, x] and (x + y) % 2 == 0:
                L.px(ox + x, oy + y - 1, "tg")


def paint_path(L, ox, oy, key):
    """The limestone road: grass margins scalloped, a worn darker lip on the stone."""
    vis, _ = visible(key, margin=3.0, radius=2.0, amp=1.2, seed=2.3)
    L.texture(GRASS, ox, oy, 16, 16)
    L.texture(PATH, ox, oy, 16, 16, vis)
    for y, x in np.argwhere(ring(vis)):
        L.px(ox + x, oy + y, "p1")
    for y, x in np.argwhere(halo(vis)):
        if (x + 2 * y) % 3:
            L.px(ox + x, oy + y, "g2")


def paint_track(L, ox, oy, key):
    """A goat track: a narrow worn line of bare earth through the grass."""
    vis, _ = visible(key, margin=4.5, radius=1.5, amp=0.8, seed=3.7)
    L.texture(GRASS, ox, oy, 16, 16)
    for y, x in np.argwhere(vis):
        h = (x * 7 + y * 13) % 11
        L.px(ox + x, oy + y, "l1" if h > 2 else ("p1" if h == 2 else "l0"))
    for y, x in np.argwhere(ring(vis)):
        if (x + y) % 2:
            L.px(ox + x, oy + y, "gd")


def shape_set(key, title, keys, painter, walk_code, section, notes):
    """A Struct holding one piece per shape key, 8 per row; names map key -> cell."""
    w = 8
    h = (len(keys) + w - 1) // w
    walk = []
    names = {}
    for j in range(h):
        row = ""
        for i in range(w):
            n = j * w + i
            row += walk_code if n < len(keys) else walk_code
            if n < len(keys):
                names[keys[n]] = (i, j)
        walk.append(row)
    s = Struct(key, title, w, h, section, walk=walk, notes=notes, names=names)
    for k, (i, j) in names.items():
        painter(s.B, i * 16, j * 16, k)
    # unused tail cells repeat the last piece so the sheet has no holes
    last = keys[-1]
    for n in range(len(keys), w * h):
        painter(s.B, (n % w) * 16, (n // w) * 16, last)
    return s
