"""Eleusa's fields: standing wheat (tall grass with soft edges), harvested
stubble, sheaves and stooks, and Demeter's poppies.

The wheat and the stubble are painted per shape from agros's soft-ground engine
(agros_ground.visible): the region is the union of the cell and its
neighbors, opened with a rounded brush and wobbled by a 16 px periodic noise,
so every piece meets every other seamlessly and their 8x8 quarters repeat.
Both come as all 47 blob shapes (agros_ground.blob_keys), named by shape key,
so the map team can draw any field outline.

Wheat keeps MB_TALL_GRASS: it is Eleusa's tall grass. Light comes from the top
left: ears lean out over the field's north edge, the south edge shows dark
stalk bases, and the field casts a shadow on the grass to its south and east.
"""
from __future__ import annotations

import numpy as np

import agros_ground as AG
from eleusa_lib import GRASS, Layer, Struct, grass, put, struct

SEC = "fields"

# --------------------------------------------------------------------------
# Textures, 16 px periodic
# --------------------------------------------------------------------------

EAR = [
    "4..",
    ".4.",
    "434",
    "433",
    "332",
    "322",
    "221",
    ".1K",
]
EAR_LEGEND = {"4": "wh4", "3": "wh3", "2": "wh2", "1": "wh1", "K": "wk"}
# Ears in a staggered lattice; (x, y) of each ear's top-left, wrapping at 16.
EARS = [(0, 0), (4, 4), (8, 1), (12, 5), (0, 8), (4, 12), (8, 9), (12, 13)]
EARS_B = [(1, 2), (5, 6), (9, 0), (13, 4), (1, 10), (5, 14), (9, 8), (13, 12)]


def wheat_texture(poppies=0, variant=0):
    """16x16 wheat: slim golden ears with their awns, on stalks, dark between."""
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            # stalks in shade, with dark furrows between the plants
            c = "wh1"
            if x % 4 == 3 and (y + x) % 3:
                c = "wk"
            elif x % 4 == 1:
                c = "wh2"
            L.px(x, y, c)
    for ex, ey in (EARS if variant == 0 else EARS_B):
        for j, row in enumerate(EAR):
            for i, ch in enumerate(row):
                if ch == ".":
                    continue
                L.px((ex + i) % 16, (ey + j) % 16, EAR_LEGEND[ch])
    for k in range(poppies):
        px, py = [(6, 5), (13, 13), (2, 12)][k]
        put(L, px - 1, py - 1, [".2.", "211", ".1K"], {"2": "pp2", "1": "pp1", "K": "pp0"})
        L.px(px, py + 2, "gd")
    return L


def stubble_texture():
    """16x16 cut field: short straw stubs in rows over dry, pale ground, each
    stub lit on top with a shadow below it, and a little fallen straw."""
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            L.px(x, y, "sb3")
    for row in range(4):
        y = row * 4
        for k in range(4):
            x = (k * 4 + (row % 2) * 2 + (k * 3 + row) % 2) % 16
            L.px(x, y, "wh4")
            L.px(x, (y + 1) % 16, "sb2")
            L.px((x + 1) % 16, (y + 1) % 16, "sb1")
            L.px(x, (y + 2) % 16, "sb2")
    # fallen straws and the odd clod
    for x, y, c in ((6, 2, "wh2"), (7, 2, "wh3"), (13, 10, "wh2"), (14, 10, "wh3"), (2, 13, "sb2"),
                    (10, 6, "sb2"), (3, 7, "wh3")):
        L.px(x, y, c)
    return L


_WHEAT = None
_STUBBLE = None


def _tex(name):
    global _WHEAT, _STUBBLE
    if name == "wheat":
        if _WHEAT is None:
            _WHEAT = wheat_texture()
        return _WHEAT
    if _STUBBLE is None:
        _STUBBLE = stubble_texture()
    return _STUBBLE


def paint_tex(L, tex, ox, oy, mask):
    for y, x in np.argwhere(mask):
        L.a[oy + y, ox + x] = tex.a[(oy + y) % 16, (ox + x) % 16]


# --------------------------------------------------------------------------
# Soft-edged painters (one 16x16 cell from its shape key)
# --------------------------------------------------------------------------

def paint_wheat(L, ox, oy, key):
    """Wheat meeting grass. The field's edge keeps a few px of margin so the
    soft outline shows; ears poke above the north edge, stalk bases darken the
    south edge, and grass to the south and east lies in the field's shadow."""
    vis, _ = AG.visible(key, margin=2.0, radius=4.5, amp=1.5, seed=0.7, jag=1.0)
    grass(L, ox, oy, 16, 16)
    paint_tex(L, _tex("wheat"), ox, oy, vis)
    ring = AG.ring(vis)
    halo = AG.halo(vis)
    for y, x in np.argwhere(ring):
        below = y + 1 >= 16 or not vis[y + 1, x]
        above = y - 1 < 0 or not vis[y - 1, x]
        right = x + 1 >= 16 or not vis[y, x + 1]
        if below:
            L.px(ox + x, oy + y, "wk")
        elif right:
            L.px(ox + x, oy + y, "wh1")
        elif above:
            L.px(ox + x, oy + y, "wh3" if (x + y) % 3 else "wh4")
    for y, x in np.argwhere(halo):
        # shadow on the grass south and east of the wheat
        if (y - 1 >= 0 and vis[y - 1, x]) or (x - 1 >= 0 and vis[y, x - 1]):
            L.px(ox + x, oy + y, "g1" if (x + y) % 2 else "gd")
        # ears leaning out over the north edge
        if y + 1 < 16 and vis[y + 1, x] and (x * 5 + y * 3) % 5 == 0:
            L.px(ox + x, oy + y, "wh3")
            if y - 1 >= 0 and not vis[y - 1, x]:
                L.px(ox + x, oy + y - 1, "wh4")


def paint_stubble(L, ox, oy, key):
    """Harvested stubble meeting grass: a cleaner edge, a little straw strewn
    on the grass beside it."""
    vis, _ = AG.visible(key, margin=2.0, radius=3.5, amp=1.2, seed=4.1)
    grass(L, ox, oy, 16, 16)
    paint_tex(L, _tex("stubble"), ox, oy, vis)
    for y, x in np.argwhere(AG.ring(vis)):
        below = y + 1 >= 16 or not vis[y + 1, x]
        L.px(ox + x, oy + y, "sb1" if below else "sb2")
    for y, x in np.argwhere(AG.halo(vis)):
        if (x * 3 + y * 5) % 7 == 0:
            L.px(ox + x, oy + y, "sb3")


def soft_set(key, title, painter, code, notes):
    keys = AG.blob_keys()
    s = AG.shape_set(key, title, keys, painter, code, SEC, notes)
    return s


# --------------------------------------------------------------------------
# Field pieces
# --------------------------------------------------------------------------

def wheat_centers():
    """Extra wheat interiors: a second ear pattern and poppies in the corn."""
    s = struct("wheat_poppies", "Poppies in the corn", 1, 1, SEC, walk=["G"],
               notes="Tall grass for the inside of a field (where the shape key is "
                     "`1|11111111`): wheat with Demeter's poppies through it. Scatter it to "
                     "break up a large field.")
    s.B.a[0:16, 0:16] = wheat_texture(poppies=3).a
    return s


SHEAF = [
    "...4.4.4...",
    "..4343434..",
    ".434333323.",
    ".33332332K.",
    "..322322K..",
    "...21221...",
    "...KWWWK...",
    "...12121...",
    "...12121...",
    "..1121211..",
    "..21212121.",
    "..K11111K..",
]
SHEAF_LEGEND = {"4": "wh4", "3": "wh3", "2": "wh2", "1": "wh1", "K": "wk", "W": "sb1"}


def sheaves():
    out = []
    # a stook: four sheaves leaned together, on stubble
    s = struct("stook", "Stook of sheaves on the stubble", 1, 1, SEC, walk=["X"],
               notes="Four sheaves stood together to dry, on the stubble's middle.")
    paint_tex(s.B, _tex("stubble"), 0, 0, np.ones((16, 16), bool))
    for y in range(12, 16):
        for x in range(3, 14):
            if s.B.get(x, y) in ("sb3", "wh4"):
                s.B.px(x, y, "sb2")
    put(s.M, 0, 2, [r[1:] for r in SHEAF], SHEAF_LEGEND)
    put(s.M, 5, 2, SHEAF, SHEAF_LEGEND)
    put(s.M, 2, 4, SHEAF, SHEAF_LEGEND)
    out.append(s)
    # a single sheaf standing on grass, for yards and doorways
    s = struct("sheaf_grass", "A sheaf standing on grass", 1, 1, SEC, walk=["X"], on="grass",
               notes="On borrowed aethos grass: a sheaf by a door, a shrine or a gate.")
    put(s.M, 2, 3, SHEAF, SHEAF_LEGEND)
    out.append(s)
    # the reaper's basket and sickle
    s = struct("reaper", "The reaper's basket and sickle, on stubble", 1, 1, SEC, walk=["X"],
               notes="A wicker basket of cut ears with a bronze sickle laid across it.")
    paint_tex(s.B, _tex("stubble"), 0, 0, np.ones((16, 16), bool))
    put(s.M, 1, 3, [
        "....4.4..4....",
        "...434343434..",
        "..K33333233K..",
        ".K1222222221K.",
        ".K2121212121K.",
        ".K1212121212K.",
        "..K12121212K..",
        "..K21212121K..",
        "...KKKKKKKK...",
    ], {"4": "wh4", "3": "wh3", "2": "wh2", "1": "wh1", "K": "wk"})
    out.append(s)
    return out


def poppies():
    """Poppy meadow cells on grass: walkable, scatter them to make a field."""
    s = struct("poppies", "Poppies in the grass", 2, 1, SEC, walk=[".."],
               names={"scattered": (0, 0), "dense": (1, 0)},
               notes="Field poppies through aethos grass; walkable. Scatter `scattered` "
                     "round a field's edge and use `dense` for its heart. Poppies are "
                     "Demeter's flower: plant them by her shrines and in the corn.")
    flower = [".2.", "211", ".1K"]
    bud = ["1", "K"]
    leg = {"2": "pp2", "1": "pp1", "K": "pp0"}
    spots = [
        [(3, 3, 1), (11, 6, 1), (6, 11, 1), (13, 13, 0), (1, 9, 0)],
        [(2, 2, 1), (8, 1, 1), (13, 4, 1), (5, 7, 1), (11, 9, 1), (1, 12, 1), (7, 13, 1),
         (14, 13, 1), (10, 15, 0), (4, 15, 0)],
    ]
    for i, sp in enumerate(spots):
        grass(s.B, i * 16, 0, 16, 16)
        for (x, y, full) in sp:
            ox = i * 16
            # a stem and a leaf under each flower
            s.B.px(ox + x, (y + 2) % 16, "gd")
            s.B.px(ox + x - 1 if x else ox + x + 1, (y + 3) % 16, "gd")
            if full:
                for j, row in enumerate(flower):
                    for k, ch in enumerate(row):
                        if ch != ".":
                            s.B.px(ox + (x - 1 + k) % 16, (y - 1 + j) % 16, leg[ch])
            else:
                for j, row in enumerate(bud):
                    s.B.px(ox + x, (y + j) % 16, leg[row])
    return s


def build():
    wheat = soft_set("wheat", "Standing wheat with soft edges (tall grass)", paint_wheat, "G",
                     "Eleusa's tall grass: golden wheat. Every one of the 47 blob shapes, named "
                     "by its shape key (agros_ground.py), so a field can take any outline. "
                     "MB_TALL_GRASS throughout: wild encounters follow the cells while the "
                     "outline stays soft. The full interior is `1|11111111`.")
    stubble = soft_set("stubble", "Harvested stubble with soft edges", paint_stubble, ".",
                       "A reaped field: rows of cut straw over dry earth. Walkable. The same 47 "
                       "shapes as the wheat, so a field can be half reaped: put stubble cells "
                       "beside wheat cells and give each the shape it has on its own.")
    return [wheat, wheat_centers(), stubble, *sheaves(), poppies()]
