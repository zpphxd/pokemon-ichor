"""Skiron ground: the old paved road and tall grass, both with soft edges.

Both are drawn per cell from the cell's 3x3 neighborhood, keyed like agros's
soft ground (agros_ground.py): the cell's state then its neighbors' in the
order N NE E SE S SW W NW, "1" in the region and "0" not, a diagonal counting
only when both its sides are in. The road is paved inside its cells: a wobbly
grass verge, a dirt line, a course of long kerbstones, then polygonal
flagstones in a pattern that repeats every 16 px, so every piece meets every
other. The tall grass is agros's barley painter.

(The diolkos is in gTileset_Isthmos, the director's set.)
"""
from __future__ import annotations

import numpy as np

import agros_ground as AG
from skiron_lib import GRASS, Struct

SEC = "ground"

# --------------------------------------------------------------------------
# Shape keys
# --------------------------------------------------------------------------

DIRS = AG.DIRS


def canon(center, neigh):
    """Shape key with diagonals cleared unless both their sides are set."""
    b = list(neigh)
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] == "1" and b[c] == "1"):
            b[d] = "0"
    return center + "|" + "".join(b)


# The road and meadow shapes every map is likely to need: the straight edges,
# outer and inner corners. Maps add the rest through skiron_shapes.json.
BASE_SHAPES = {
    "N": "1|00111110", "S": "1|11100011", "W": "1|11111000", "E": "1|10001111",
    "NW": "1|00111000", "NE": "1|00001110", "SW": "1|11100000", "SE": "1|10000011",
    "iNE": "1|10111111", "iSE": "1|11101111", "iSW": "1|11111011", "iNW": "1|11111110",
}
FULL = "1|11111111"


# --------------------------------------------------------------------------
# The paved road
# --------------------------------------------------------------------------

SEEDS = [(3.0, 3.5), (11.5, 2.0), (7.0, 9.5), (14.5, 10.5), (0.5, 12.5)]


def _stone_map():
    """16x16 periodic map of flagstone ids: polygonal slabs, the Voronoi cells
    of a few seeds on a torus, a little wider than tall."""
    ids = np.zeros((16, 16), int)
    for y in range(16):
        for x in range(16):
            best, bi = 1e9, 0
            for i, (sx, sy) in enumerate(SEEDS):
                dx = min(abs(x - sx), 16 - abs(x - sx)) * 0.8
                dy = min(abs(y - sy), 16 - abs(y - sy))
                d = dx * dx + dy * dy
                if d < best:
                    best, bi = d, i
            ids[y, x] = bi
    return ids


STONES = _stone_map()
# body color per slab: weathered limestone, some grey, some buff
STONE_TONE = {0: "k3", 1: "p1", 2: "p1", 3: "k3", 4: "p2"}
LIGHTER = {"p2": "p3", "p1": "p2", "k3": "p2", "l1": "p1"}
DARKER = {"p2": "p1", "p1": "l1", "k3": "k2", "l1": "l0"}


def paving(x, y, variant="mid"):
    """Color of the flagstone floor at cell pixel (x, y): slabs lit on their
    top left, joints dark on their bottom right."""
    x %= 16
    y %= 16
    sid = STONES[y, x]
    right = STONES[y, (x + 1) % 16]
    below = STONES[(y + 1) % 16, x]
    left = STONES[y, (x - 1) % 16]
    above = STONES[(y - 1) % 16, x]
    if right != sid or below != sid:
        c = "k2" if (x * 5 + y * 3) % 4 else "l0"
        if variant == "mid2" and (x * 3 + y) % 5 == 0:
            c = "gd"                                    # weeds in the joints
        return c
    body = STONE_TONE[sid]
    if variant == "mid2" and sid == 2:
        body = "l1"                                     # a worn, dished slab
    if left != sid or above != sid:
        return LIGHTER[body] if (x + y) % 3 else body
    if (x * 7 + y * 11) % 13 == 0 or (x * 5 + y * 9) % 17 == 0:
        return DARKER[body]                             # pitting
    return body


def _variant_marks(L, ox, oy, variant):
    if variant == "mid3":
        # a crack across a slab, and a corner broken out and filled with earth
        for (x, y) in ((8, 6), (9, 7), (9, 8), (10, 9), (11, 9), (12, 10)):
            L.px(ox + x, oy + y, "k2")
        for (x, y) in ((8, 7), (10, 10), (11, 10)):
            L.px(ox + x, oy + y, "p2")
        for (x, y) in ((1, 1), (2, 1), (1, 2), (2, 2), (3, 2), (2, 3)):
            L.px(ox + x, oy + y, "l1")
        L.px(ox + 2, oy + 2, "l0")
        L.px(ox + 1, oy + 1, "gd")
    if variant == "mid2":
        L.px(ox + 6, oy + 12, "g1")
        L.px(ox + 7, oy + 12, "gd")
        L.px(ox + 13, oy + 4, "g1")


def _dist_inside(key):
    """Distance of each center-cell pixel to the nearest pixel outside the region."""
    R = AG.region_canvas(key)
    outside = np.argwhere(~R).astype(np.float32)
    if len(outside) == 0:
        return np.full((16, 16), 99.0)
    yy, xx = np.mgrid[16:32, 16:32]
    pts = np.stack([yy.ravel(), xx.ravel()], 1).astype(np.float32)
    d = np.sqrt(((pts[:, None, :] - outside[None, :, :]) ** 2).sum(-1)).min(1)
    return d.reshape(16, 16)


def paint_road(L, ox, oy, key, variant="mid"):
    """One cell of the paved road for a shape key."""
    d = _dist_inside(key)
    gy, gx = np.gradient(np.minimum(d, 20.0))
    n = AG.wobble(4.1, 1.1, 0.6)[16:32, 16:32]
    L.texture(GRASS, ox, oy, 16, 16)
    for y in range(16):
        for x in range(16):
            dd = d[y, x]
            verge = 2.0 + n[y, x]
            if dd < verge:
                continue                                  # grass
            if dd < 3.0:
                L.px(ox + x, oy + y, "l1" if (x + y) % 3 else "l0")
                continue
            if dd < 6.0:
                # kerbstones: long worn blocks flush with the road, a little paler
                k = dd - 3.0
                along = x if abs(gy[y, x]) >= abs(gx[y, x]) else y
                if along % 9 == 8:
                    c = "k2"
                elif k < 1.0:
                    c = "p2"
                elif (along * 3 + int(k)) % 7 == 0:
                    c = "k3"
                else:
                    c = "p1"
                L.px(ox + x, oy + y, c)
                continue
            if dd < 7.0:
                L.px(ox + x, oy + y, "k3" if (x + y) % 3 else "k2")
                continue
            L.px(ox + x, oy + y, paving(x, y, variant))
    if key == FULL:
        _variant_marks(L, ox, oy, variant)


def road_set(keys):
    """The road pieces: every shape key (named by key and by its BASE_SHAPES
    alias), plus the plain road and two worn variants of it."""
    keys = list(dict.fromkeys(keys))
    pieces = [("mid", FULL, "mid"), ("mid2", FULL, "mid2"), ("mid3", FULL, "mid3")]
    alias = {v: k for k, v in BASE_SHAPES.items()}
    for k in keys:
        if k != FULL:
            pieces.append((k, k, "mid"))
    w = 8
    h = (len(pieces) + w - 1) // w
    s = Struct("road", "The old paved road", w, h, SEC, walk=["." * w] * h,
               notes="Flagstones in long kerbs, a grass verge outside them. Pieces are named by "
                     "shape key (and N, S, E, W, NW, NE, SW, SE, iNE, iSE, iSW, iNW for the "
                     "straight edges and corners); `mid` is the open road, `mid2` and `mid3` "
                     "worn variants of it (weeds in the joints, a cracked stone). Walkable.")
    for i, (name, key, variant) in enumerate(pieces):
        cx, cy = i % w, i // w
        paint_road(s.B, cx * 16, cy * 16, key, variant)
        s.names[name] = (cx, cy)
        if key in alias and name == key:
            s.names[alias[key]] = (cx, cy)
    for i in range(len(pieces), w * h):
        paint_road(s.B, (i % w) * 16, (i // w) * 16, FULL, "mid")
    return s


# --------------------------------------------------------------------------
# Tall grass with soft edges (agros's barley painter)
# --------------------------------------------------------------------------

def tall_set(keys):
    keys = [k for k in dict.fromkeys(keys) if k != FULL]
    s = AG.shape_set("tall", "Tall grass with soft edges", keys, AG.paint_tall, "G", SEC,
                     "The aethos barley meadow (0x00D in the middle) with soft, wobbly edges. "
                     "Each piece is named by its shape key and keeps MB_TALL_GRASS, so "
                     "encounters follow the cells while the outline stays soft.")
    alias = {v: k for k, v in BASE_SHAPES.items()}
    for k, cell in list(s.names.items()):
        if k in alias:
            s.names[alias[k]] = cell
    return s


def tall_thyme():
    """The thyme meadow: barley grown through with wild thyme in flower."""
    from skiron_lib import TALL
    s = Struct("tall_thyme", "Tall grass with thyme in flower", 1, 1, SEC, walk=["G"],
               notes="The meadow cell for Route 5's thyme meadow: aethos barley threaded with "
                     "purple thyme. MB_TALL_GRASS. Mix it with plain 0x00D inside a meadow "
                     "whose edges are `tall` pieces.")
    s.B.texture(TALL, 0, 0, 16, 16)
    for (x, y) in ((2, 3), (9, 1), (12, 7), (5, 9), (1, 13), (10, 12), (14, 14), (7, 5)):
        s.B.px(x, y, "th2")
        s.B.px(x + 1, y, "th1")
        s.B.px(x, y + 1, "th1")
    return s


def build(shapes):
    road_keys = list(BASE_SHAPES.values()) + list(shapes.get("road", []))
    tall_keys = list(BASE_SHAPES.values()) + list(shapes.get("tall", []))
    return [road_set(road_keys), tall_set(tall_keys), tall_thyme()]
