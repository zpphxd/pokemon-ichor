"""The plain of Troy for gTileset_Troas: wheat, reeds, river banks, burial
mounds, Ida's pines, oaks and elms, and the small things in the grass.

Wheat and the river banks are soft-edged sets of fourteen pieces (a nine-patch,
four inner corners and a lone clump), shaped by agros_ground's rounded-brush
engine so every piece meets its neighbors seamlessly. Wheat is the Troad's tall
grass (MB_TALL_GRASS). Bank pieces are water cells (MB_OCEAN_WATER) on aethos's
animated sea with a lip of turf and earth drawn over the land side.

Light comes from the top left everywhere.
"""
from __future__ import annotations

import numpy as np

from agros_ground import halo, ring, visible
from troas_lib import blob, finish, mirror_x, outline_mask, struct

# The fourteen shapes: a cell's key lists its 8 neighbors N NE E SE S SW W NW,
# 1 inside the region. Map builders choose the piece by the same rule.
SHAPES = {
    "c": "1|11111111", "n": "1|00111110", "s": "1|11100011", "w": "1|11111000",
    "e": "1|10001111", "nw": "1|00111000", "ne": "1|00001110", "sw": "1|11100000",
    "se": "1|10000011", "in_nw": "1|11111110", "in_ne": "1|10111111", "in_sw": "1|11111011",
    "in_se": "1|11101111", "one": "1|00000000",
}
ORDER = ["nw", "n", "ne", "in_nw", "in_ne", "c", "one", "c2",
         "w", "e", "sw", "s", "se", "in_sw", "in_se"]


def shape_struct(key, title, painter, walk, mb, notes, ground):
    """One structure holding every shape, 8 to a row; names map shape -> cell."""
    w, h = 8, 2
    s = struct(key, title, w, h, walk=[walk * w] * h, notes=notes, ground=ground)
    for i, name in enumerate(ORDER):
        cx, cy = i % w, i // w
        s.names[name] = (cx, cy)
        painter(s.M, cx * 16, cy * 16, SHAPES.get(name, SHAPES["c"]), variant=name == "c2")
        if mb:
            s.behaviors[(cx, cy)] = mb
    # the unused 16th cell repeats the plain middle
    painter(s.M, 7 * 16, 16, SHAPES["c"], variant=True)
    if mb:
        s.behaviors[(7, 1)] = mb
    s.names["c3"] = (7, 1)
    return finish(s)


# --------------------------------------------------------------------------
# Wheat
# --------------------------------------------------------------------------

EAR = ["4..", ".4.", "434", "433", "332", "322", "221", ".1K"]
EAR_KEY = {"4": "tw4", "3": "tw3", "2": "tw2", "1": "tw1", "K": "tw0"}
EARS = [(0, 0), (4, 4), (8, 1), (12, 5), (0, 8), (4, 12), (8, 9), (12, 13)]
EARS_B = [(2, 2), (6, 6), (10, 0), (14, 4), (2, 10), (6, 14), (10, 8), (14, 12)]


def wheat_texture(variant=False):
    t = np.empty((16, 16), object)
    for y in range(16):
        for x in range(16):
            c = "tw1"
            if x % 4 == 3 and (y + x) % 3:
                c = "tw0"
            elif x % 4 == 1:
                c = "tw2"
            t[y, x] = c
    for ex, ey in (EARS_B if variant else EARS):
        for j, row in enumerate(EAR):
            for i, ch in enumerate(row):
                if ch != ".":
                    t[(ey + j) % 16, (ex + i) % 16] = EAR_KEY[ch]
    if variant:
        # cornflowers among the corn
        for (x, y) in ((5, 3), (12, 10), (1, 13)):
            t[y, x] = "b2"
            t[y + 1, x] = "rg1"
    return t


def paint_wheat(L, ox, oy, key, variant=False):
    vis, _ = visible(key, margin=1.5, radius=4.0, amp=1.4, seed=0.9, jag=1.0)
    tex = wheat_texture(variant)
    for y, x in np.argwhere(vis):
        L.px(ox + x, oy + y, tex[y, x])
    for y, x in np.argwhere(ring(vis)):
        below = y + 1 >= 16 or not vis[y + 1, x]
        above = y - 1 < 0 or not vis[y - 1, x]
        right = x + 1 >= 16 or not vis[y, x + 1]
        if below:
            L.px(ox + x, oy + y, "tw0")
        elif right:
            L.px(ox + x, oy + y, "tw1")
        elif above:
            L.px(ox + x, oy + y, "tw3" if (x + y) % 3 else "tw4")
    for y, x in np.argwhere(halo(vis)):
        if (y - 1 >= 0 and vis[y - 1, x]) or (x - 1 >= 0 and vis[y, x - 1]):
            L.px(ox + x, oy + y, "gr1")      # the field's shadow on the grass
        if y + 1 < 16 and vis[y + 1, x] and (x * 5 + y * 3) % 5 == 0:
            L.px(ox + x, oy + y, "tw3")      # ears leaning out over the north edge
            if y - 1 >= 0 and not vis[y - 1, x]:
                L.px(ox + x, oy + y - 1, "tw4")


def wheat():
    return shape_struct(
        "wheat", "Wheat on the plain (tall grass)", paint_wheat, ".", "MB_TALL_GRASS",
        "The Troad's tall grass: standing wheat, gold against aethos's grass, in fourteen soft-"
        "edged shapes named by the side the grass is on (n, ne, ... in_se for an inner corner, "
        "one for a lone clump). c2 and c3 are middles with another ear pattern and "
        "cornflowers. Every cell is MB_TALL_GRASS.", "grass")


def wheat_crop():
    """The same wheat as a crop in a town's fields: impassable, no encounters.
    It shares every tile with the tall grass, so it costs metatiles only."""
    return shape_struct(
        "wheat_crop", "Wheat in a town field (impassable)", paint_wheat, "X", None,
        "A town's standing crop: the wheat's fourteen shapes, impassable and with no wild "
        "encounters, for fields inside a town (towns have no land tables). Same names as wheat.",
        "grass")


# --------------------------------------------------------------------------
# River banks
# --------------------------------------------------------------------------

def paint_bank(L, ox, oy, key, variant=False):
    """Water meeting land: the land side gets turf and a lip of wet earth; the
    north bank shows its earth face, the south bank only a wet line."""
    vis, _ = visible(key, margin=4.0, radius=4.0, amp=1.0, seed=2.7, jag=0.6)
    land = ~vis
    if not land.any():
        if variant:
            for (x, y) in ((3, 4), (11, 11)):
                L.px(ox + x, oy + y, "w0")
                L.px(ox + x + 1, oy + y, "w0")
        return
    water = vis
    # distance of each land pixel from the water, 4-neighbourhood
    d = np.full((16, 16), 99)
    d[water] = 0
    for _ in range(6):
        p = np.pad(d, 1, constant_values=99)
        d = np.minimum(d, np.minimum.reduce([p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]]) + 1)
    for y, x in np.argwhere(land):
        dist = d[y, x]
        water_below = any(y + k < 16 and water[y + k, x] for k in range(1, 5))
        if water_below and dist <= 4:
            c = ("tw0" if dist == 1 else "e1" if dist == 2 else "e2" if dist == 3 else "gr1")
        elif dist == 1:
            c = "e1"
        elif dist == 2:
            c = "gr1"
        else:
            c = "gr0" if (x * 3 + y * 7) % 11 else "gr2"
        L.px(ox + x, oy + y, c)
    # foam along the waterline, and a reed or two on the lip
    for y, x in np.argwhere(halo(land) & water):
        if (x * 5 + y * 3) % 4 == 0:
            L.px(ox + x, oy + y, "w0")
    for y, x in np.argwhere(land):
        if d[y, x] == 3 and (x * 7 + y * 5) % 9 == 0 and y >= 3:
            for k in range(3):
                L.px(ox + x, oy + y - k, "rg1" if k else "rg0")
            L.px(ox + x, oy + y - 3, "rg2")


def banks():
    return shape_struct(
        "bank", "River banks", paint_bank, ".", "MB_OCEAN_WATER",
        "For the Skamander: water cells on aethos's sea with turf and a lip of wet earth "
        "drawn over the land side, in the same fourteen shapes as the wheat (the region is "
        "the water: n means land to the north). Surfable; mark them as water (elevation 1).",
        "sea")


# --------------------------------------------------------------------------
# Reeds
# --------------------------------------------------------------------------

def reed(L, x, y, h, lean=0):
    for k in range(h):
        L.px(x + (lean if k > h - 3 else 0), y - k, "rg1" if k % 3 else "rg0")
    L.px(x + lean, y - h, "rg2")


def reeds():
    s = struct("reeds", "Reeds of the Skamander", 3, 1, walk=[".X."],
               notes="Cell 0: a reed bed on grass, tall grass (MB_TALL_GRASS). Cell 1: reeds "
                     "standing in the water at a bank, impassable, on aethos's sea. Cell 2: a "
                     "small reed tuft on grass, walkable decoration.",
               ground="grass")
    s.set_ground("sea", [(1, 0)])
    s.behaviors[(0, 0)] = "MB_TALL_GRASS"
    M = s.M
    for i, x in enumerate(range(1, 16, 2)):
        h = 9 + (i * 5) % 5
        reed(M, x, 15, h, lean=1 if i % 3 == 0 else 0)
        if i % 2:
            M.px(x, 15 - h - 1, "tw1")          # a brown seed head
            M.px(x, 15 - h - 2, "tw0")
    for x in range(0, 16):
        M.px(x, 15, "rg0" if x % 2 else "gr1")
    # in the water: a stand of reeds with their reflections broken by ripples
    for i, x in enumerate(range(18, 31, 2)):
        h = 8 + (i * 3) % 4
        reed(M, x, 12, h, lean=-1 if i % 2 else 0)
        M.px(x, 13, "w0" if i % 2 else "e1")
    M.hline(17, 30, 14, "w0")
    for x in range(17, 31, 3):
        M.px(x, 15, "w0")
    # a tuft
    for i, x in enumerate((37, 39, 40, 42, 44)):
        reed(M, x, 14, 4 + (i * 3) % 4, lean=1 if i == 4 else 0)
    M.hline(36, 44, 15, "gr1")
    return finish(s)


# --------------------------------------------------------------------------
# Burial mounds
# --------------------------------------------------------------------------

def mound():
    """A heroes' tumulus: a turfed dome ringed at its foot with a kerb of grey
    stones, a stele on the crown. Symmetric, so it costs half its tiles."""
    s = struct("mound", "A heroes' burial mound", 3, 2, walk=["XXX", "XXX"],
               notes="A tumulus on the plain (Achilles's and Patroclus's at Sigeion, "
                     "Protesilaos's across the strait, the heroes' mounds on the Skamander). "
                     "Impassable; dig spots in batch 2 go at its foot as hidden events.",
               ground="grass")
    M = s.M
    dome = blob(M, 23.5, 22, 22, 15, "ov2")
    yy, xx = np.mgrid[0:32, 0:48]
    m = dome & (yy > 7)
    # shading: lit crown at the top left, darker lower right, turf texture
    for y, x in np.argwhere(dome):
        nx, ny = (x - 23.5) / 22, (y - 22) / 15
        lit = -0.6 * nx - 0.8 * ny
        c = "ov3" if lit > 0.55 else "ov2" if lit > 0.05 else "ov1" if lit > -0.45 else "ov0"
        if c == "ov2" and (x * 7 + y * 3) % 13 == 0:
            c = "ov3"
        M.px(x, y, c)
    outline_mask(M, dome, 0, 0, "ink")
    # the kerb: a ring of stones along the foot
    for x in range(3, 45, 4):
        yb = 22 + int(15 * np.sqrt(max(0.0, 1 - ((x + 1.5 - 23.5) / 22) ** 2))) - 3
        yb = min(yb, 29)
        M.rect(x, yb, 3, 2, "tk1")
        M.hline(x, x + 2, yb, "tk2")
        M.px(x + 2, yb + 1, "tk0")
    # the stele on the crown
    M.rect(22, 2, 4, 8, "tk2")
    M.vline(25, 3, 9, "tk1")
    M.hline(22, 25, 2, "ink")
    M.vline(21, 2, 9, "ink")
    M.vline(26, 2, 9, "ink")
    M.hline(21, 26, 10, "ov0")
    mirror_x(M, 0, 48, 0, 32)
    del m
    return finish(s)


# --------------------------------------------------------------------------
# Trees
# --------------------------------------------------------------------------

def ida_pine():
    """A black pine of Ida: a tall dark cone of layered boughs on a red-brown
    trunk. 2 x 3, symmetric."""
    s = struct("ida_pine", "Black pine of Ida", 2, 3, walk=["XX", "XX", "XX"],
               notes="Ida's pine, 2 x 3. Stagger them 1-2 cells apart for a forest edge; "
                     "mix with aethos's stone pines and cypresses.",
               ground="grass")
    M = s.M
    # trunk
    M.rect(14, 38, 4, 9, "tk0")
    M.vline(14, 38, 46, "ink")
    M.vline(17, 38, 46, "ink")
    M.vline(15, 39, 45, "tk1")
    # boughs: five tiers, each a drooping fan wider than the one above
    tiers = [(2, 10, 5), (7, 13, 9), (13, 16, 13), (20, 20, 16), (28, 24, 18)]
    for (top, depth, half) in tiers:
        for y in range(top, top + depth):
            t = (y - top) / max(1, depth - 1)
            hw = int(round(half * (0.35 + 0.65 * t)))
            for x in range(16 - hw, 16 + hw):
                lit = (x < 16 - hw * 0.3) and y < top + depth - 3
                c = "pn2" if lit else "pn1"
                if y >= top + depth - 2 or x >= 16 + hw * 0.55:
                    c = "pn0"
                if (x + 2 * y) % 7 == 0 and c == "pn1":
                    c = "pn2"
                M.px(x, y, c)
        M.hline(16 - half, 16 + half - 1, top + depth - 1, "ink")
    # outline the crown and its tip
    crown = M.a[:, :, 3] > 0
    outline_mask(M, crown, 0, 0, "ink")
    M.px(15, 0, "pn1")
    M.px(16, 0, "pn1")
    M.px(15, 1, "pn2")
    M.px(16, 1, "pn1")
    mirror_x(M, 0, 32, 0, 37)
    return finish(s)


def young_pine():
    s = struct("young_pine", "Young pine", 1, 2, walk=["X", "X"],
               notes="A small pine of Ida, 1 x 2, for breaking up a tree line.", ground="grass")
    M = s.M
    M.rect(7, 26, 2, 5, "tk0")
    for (top, depth, half) in ((2, 8, 3), (7, 9, 5), (13, 10, 7), (20, 7, 7)):
        for y in range(top, top + depth):
            t = (y - top) / max(1, depth - 1)
            hw = max(1, int(round(half * (0.3 + 0.7 * t))))
            for x in range(8 - hw, 8 + hw):
                c = "pn2" if x < 8 - hw * 0.2 and y < top + depth - 2 else "pn1"
                if y >= top + depth - 1:
                    c = "pn0"
                M.px(x, y, c)
    outline_mask(M, M.a[:, :, 3] > 0, 0, 0, "ink")
    mirror_x(M, 0, 16, 0, 26)
    return finish(s)


def oak():
    """The Troad's valonia oak, broad and low: the oak by the Skaian Gate in the
    Iliad. A round crown of leaf clusters over a short gnarled trunk."""
    s = struct("oak", "Valonia oak", 2, 2, walk=["XX", "XX"],
               notes="2 x 2. The oak by the Skaian Gate (Iliad 6.237) and the plain's shade "
                     "trees.", ground="grass")
    M = s.M
    # trunk and roots
    M.rect(13, 20, 6, 10, "tk0")
    M.px(12, 29, "tk0")
    M.px(19, 29, "tk0")
    M.vline(14, 20, 29, "tk1")
    outline_mask(M, M.a[:, :, 3] > 0, 0, 0, "ink")
    # crown: overlapping leaf clusters, lit from the top left
    clusters = [(16, 9, 13, 8), (8, 12, 7, 6), (24, 12, 7, 6), (11, 6, 6, 5), (21, 6, 6, 5),
                (16, 15, 10, 5)]
    crown = np.zeros((32, 32), bool)
    for (cx, cy, rx, ry) in clusters:
        yy, xx = np.mgrid[0:32, 0:32]
        crown |= ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
    for y, x in np.argwhere(crown):
        lit = (x - 16) * -0.5 + (y - 10) * -0.8
        c = "ov3" if lit > 5 else "ov2" if lit > -1 else "ov1" if lit > -6 else "ov0"
        if (x * 5 + y * 7) % 11 == 0:
            c = {"ov3": "ov4", "ov2": "ov3", "ov1": "ov2", "ov0": "ov1"}[c]
        M.px(x, y, c)
    outline_mask(M, crown, 0, 0, "ink")
    # acorn cups catching the light
    for (x, y) in ((9, 9), (22, 14), (15, 4), (26, 9)):
        M.px(x, y, "tk2")
    return finish(s)


def elm():
    """An elm on Protesilaos's mound: green below, its crown dead and bare where
    it grew tall enough to see Troy (Philostratus, Heroikos 9)."""
    s = struct("elm_withered", "Elm with a withered crown", 1, 2, walk=["X", "X"],
               notes="Plant on and beside Protesilaos's mound on the strait's north shore.",
               ground="grass")
    M = s.M
    M.rect(7, 18, 2, 13, "tk0")
    M.vline(7, 18, 30, "tk1")
    # bare top: grey twigs
    for (x0, y0, x1, y1) in ((8, 12, 4, 2), (8, 12, 12, 1), (8, 9, 6, 5), (8, 10, 11, 6),
                             (8, 14, 3, 8)):
        M.line(x0, y0, x1, y1, "tk1")
    M.vline(8, 2, 18, "tk1")
    # green lower crown
    crown = np.zeros((32, 16), bool)
    yy, xx = np.mgrid[0:32, 0:16]
    crown |= ((xx - 8) / 7) ** 2 + ((yy - 19) / 5) ** 2 <= 1
    for y, x in np.argwhere(crown):
        c = "ov2" if x < 8 and y < 20 else "ov1" if y < 22 else "ov0"
        if (x * 3 + y * 5) % 7 == 0:
            c = "ov3"
        M.px(x, y, c)
    outline_mask(M, crown, 0, 0, "ink")
    M.rect(7, 24, 2, 7, "tk0")
    M.hline(6, 9, 30, "ink")
    return finish(s)


# --------------------------------------------------------------------------
# Small things in the grass
# --------------------------------------------------------------------------

def grass_bits():
    s = struct("grass_bits", "Flowers and stones in the grass", 3, 1, walk=["...", ],
               notes="Walkable scatter for varied ground: chamomile, a golden tuft of dry "
                     "grass, a few field stones (wheat's c2 has the cornflowers).",
               ground="grass")
    M = s.M
    for (x, y) in ((3, 4), (9, 2), (6, 10), (12, 8), (2, 13), (13, 13)):
        M.px(x, y + 1, "rg1")
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            M.px(x + dx, y + dy, "w0")
        M.px(x, y, "tw3")
    for i, x in enumerate(range(18, 30, 2)):
        h = 4 + (i * 3) % 4
        for k in range(h):
            M.px(x + (1 if k > h - 2 and i % 2 else 0), 13 - k, "tw2" if k > 1 else "tw1")
        M.px(x, 13 - h, "tw4")
    M.hline(17, 30, 14, "gr1")
    for (x, y, w) in ((34, 5, 4), (40, 10, 5), (36, 12, 3), (43, 3, 3)):
        M.rect(x, y, w, 2, "tk2")
        M.hline(x, x + w - 1, y + 2, "tk0")
        M.px(x, y, "ov4")
    s.names = {"chamomile": (0, 0), "dry_tuft": (1, 0), "stones": (2, 0)}
    return finish(s)


def build():
    return [wheat(), banks(), reeds(), mound(), ida_pine(), young_pine(), oak(), elm(), grass_bits(),
            wheat_crop()]
