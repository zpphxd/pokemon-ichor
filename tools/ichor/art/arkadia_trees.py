"""Arkadia's trees: the town's cypresses in four shapes, the lamp-trees (unlit and
lit), the canopy (a soft mass of crowns: the town's edges, the Cypress Wood, the
Pool's glade), the great trunks and the white poplars.

A town cypress is 2x4 metatiles on aethos grass: the two top rows are drawn over
the player (T, the top layer), the two bottom rows block (X, the middle layer).
"""
from __future__ import annotations

import numpy as np

import arkadia_lib as L

TREE_WALK = ["TT", "TT", "XX", "XX"]


def _tree(key, title, notes, paint):
    s = L.struct(key, title, 2, 4, "trees", walk=list(TREE_WALK), notes=notes, on="grass",
                 names={"tl": (0, 0), "tr": (1, 0), "ul": (0, 1), "ur": (1, 1),
                        "ml": (0, 2), "mr": (1, 2), "bl": (0, 3), "br": (1, 3)})
    art = L.Layer(32, 64)
    # the shadow first, on a grass-colored scratch layer, then the tree over it
    g = L.Layer(32, 64)
    for y in range(64):
        for x in range(32):
            g.px(x, y, L.grass_px(x, y))
    paint(art, g)
    # split: rows 0-1 to the top layer, rows 2-3 to the middle layer; the shadow
    # pixels (grass darkened under the tree) go with the art
    for y in range(64):
        for x in range(32):
            a = art.a[y, x]
            if a[3]:
                dst = s.T if y < 32 else s.M
                dst.a[y, x] = a
            elif g.get(x, y) != L.grass_px(x, y):
                dst = s.T if y < 32 else s.M
                dst.a[y, x] = g.a[y, x]
    return s


def _cypress(cx, top, base, hw, belly=0.66, lean=0.0, seed=1, trunk_h=3):
    def paint(art, g):
        L.grass_shadow(g, int(cx) + 2, base + 1, int(hw) + 2, 3)
        m = L.cypress_mask(32, 64, cx, top, base - trunk_h + 1, hw, belly=belly, lean=lean,
                           seed=seed)
        L.trunk(art, int(round(cx)), base - trunk_h, base)
        L.paint_foliage(art, m, cx=cx, seed=seed)
    return paint


def spire():
    return _tree("cypress_spire", "Cypress: the tall spire",
                 "A tall, slim cypress, 2x4: the town's commonest. Rows 0-1 draw over the "
                 "player (walk behind it); rows 2-3 block.",
                 _cypress(15.5, 1, 61, 8.5, belly=0.7, seed=2))


def broad():
    return _tree("cypress_broad", "Cypress: the broad flame",
                 "A fuller cypress, its crown rounded into a flame.",
                 _cypress(15.5, 4, 61, 12.5, belly=0.58, seed=5))


def twin():
    def paint(art, g):
        L.grass_shadow(g, 13, 62, 13, 3)
        m1 = L.cypress_mask(32, 64, 10.5, 2, 58, 7.0, belly=0.72, seed=7)
        m2 = L.cypress_mask(32, 64, 21.5, 13, 59, 7.5, belly=0.7, seed=3)
        L.trunk(art, 22, 56, 61)
        L.paint_foliage(art, m2, cx=21.5, seed=3)
        L.trunk(art, 10, 56, 61)
        L.paint_foliage(art, m1, cx=10.5, seed=7)
    return _tree("cypress_twin", "Cypress: the twins",
                 "Two slim cypresses grown together, one a head taller.", paint)


def old():
    def paint(art, g):
        L.grass_shadow(g, 17, 62, 12, 3)
        m = L.cypress_mask(32, 64, 15.0, 3, 54, 11.0, belly=0.62, lean=4.0, seed=11)
        # a split crown: a notch in the top third
        for y in range(3, 22):
            for x in range(17, 20):
                if y < 6 + (x - 17) * 4:
                    m[y, x] = False
        # a gnarled trunk with a root
        for y in range(52, 62):
            for x in (13, 14, 15, 16):
                art.px(x, y, "k1" if x in (14, 15) else "ink")
        art.blit(["k  k", "kk.kk"], {"k": "ink", ".": "k1"}, 11, 60)
        L.paint_foliage(art, m, cx=15.0, seed=11)
    return _tree("cypress_old", "Cypress: the old one",
                 "A gnarled old cypress, leaning, its crown split by a lightning stroke long "
                 "ago, its trunk showing.", paint)


LAMP_Y = 34       # the chains' top, in the tree's 64 px (row 2 of the tree)


def lamptree():
    base = _cypress(15.5, 4, 61, 12.5, belly=0.58, seed=5)

    def paint(art, g):
        base(art, g)
        L.lamp(art, 1, LAMP_Y, False)
        L.lamp(art, 26, LAMP_Y, False)
    s = _tree("lamptree", "The lamp-tree (unlit)",
              "The broad cypress hung with two clay lamps on chains: every cypress on the "
              "main path. The lamps are on row 2 (`ml`, `mr`); `lamps_lit` holds the same two "
              "cells with the lamps alight, which the dusk scene and the night swap in "
              "(metatile labels `Arkadia_LampUnlit_L/_R`, `Arkadia_LampLit_L/_R`).", paint)
    return s


def lamps_lit():
    base = _cypress(15.5, 4, 61, 12.5, belly=0.58, seed=5)
    full = L.Layer(32, 64)
    g = L.Layer(32, 64)
    for y in range(64):
        for x in range(32):
            g.px(x, y, L.grass_px(x, y))
    base(full, g)
    L.lamp(full, 1, LAMP_Y, True)
    L.lamp(full, 26, LAMP_Y, True)
    s = L.struct("lamps_lit", "The lamp-tree's lamps, alight", 2, 1, "trees", walk=["XX"],
                 on="grass", names={"L": (0, 0), "R": (1, 0)},
                 notes="Row 2 of `lamptree` with its lamps lit: swap these over `ml` and `mr`.")
    for y in range(16):
        for x in range(32):
            a = full.a[32 + y, x]
            if a[3]:
                s.M.a[y, x] = a
            elif g.get(x, 32 + y) != L.grass_px(x, 32 + y):
                s.M.a[y, x] = g.a[32 + y, x]
    return s


# --------------------------------------------------------------------------
# The canopy
# --------------------------------------------------------------------------

def town_canopy(keys):
    """The town's edges: a mass of crowns over aethos grass (borrowed)."""
    def painter(s, ox, oy, k):
        L.paint_canopy_cell(s.B, s.M, ox, oy, k, L.RAMP_TOWN, floor=None, bark="k1",
                            shadow="grass")
    s = L.K.shape_set("canopy", "The canopy: a mass of cypress crowns", "trees", keys, painter,
                      "X", "Cypress crowns so close they knit, over aethos grass: the forest "
                           "the town stands in. Spires along the north edge, trunks and shade "
                           "along the south. Impassable. Names are blob shape keys.",
                      on="grass")
    return s


def wood_canopy(keys, floor):
    """The Cypress Wood's walls: the canopy over the Wood's dark floor."""
    def painter(s, ox, oy, k):
        L.paint_canopy_cell(s.B, s.M, ox, oy, k, L.RAMP_WOOD, floor=floor, bark="wb0",
                            shadow="wc0", dark="wc0")
    return L.K.shape_set("canopy", "The Wood's canopy over its floor", "wood", keys, painter,
                         "X", "The Wood's close-knit cypresses on its floor in deep shade. "
                              "Impassable. Names are blob shape keys.")


def glade_canopy(keys):
    """The Pool's glade: the same dark crowns, over aethos grass."""
    def painter(s, ox, oy, k):
        L.paint_canopy_cell(s.B, s.M, ox, oy, k, L.RAMP_WOOD, floor=None, bark="wb0",
                            shadow="grass")
    return L.K.shape_set("canopy_grass", "The Wood's canopy round the Pool's glade", "glade",
                         keys, painter, "X",
                         "The Wood's dark cypresses standing round the glade, over aethos "
                         "grass. Impassable. Names are blob shape keys.", on="grass")


def great_trunk(floor):
    """A great cypress trunk at the foot of the canopy: the narrow's two pillars."""
    s = L.struct("great_trunk", "A great trunk", 1, 1, "wood", walk=["X"],
                 notes="The foot of a huge cypress, roots spread on the floor; put it on the "
                       "canopy's south edge where a trunk should show (the narrow's pillars).")
    for y in range(16):
        for x in range(16):
            s.B.px(x, y, floor(x, y))
    for y in range(16):
        w = 4 if y < 11 else 4 + (y - 10)
        for x in range(8 - w, 8 + w):
            c = "wb0" if x < 8 else "wc0"
            if x == 8 - w or x == 8 + w - 1:
                c = "wc0"
            if (x * 3 + y) % 7 == 0 and x < 9:
                c = "wf3"
            s.M.px(x, y, c)
    return s


# --------------------------------------------------------------------------
# White poplars (the Pool's ring)
# --------------------------------------------------------------------------

def poplar(key="poplar", flip=False, seed=13):
    """A white poplar on grass, 2x3: silver-green crown over a white trunk."""
    s = L.struct(key, "A white poplar", 2, 3, "glade", walk=["TT", "XX", "XX"], on="grass",
                 names={"tl": (0, 0), "tr": (1, 0), "ml": (0, 1), "mr": (1, 1), "bl": (0, 2),
                        "br": (1, 2)},
                 notes="A white poplar, Mnemosyne's tree, 2x3 on grass: its top row draws "
                       "over the player.")
    art = L.Layer(32, 48)
    g = L.Layer(32, 48)
    for y in range(48):
        for x in range(32):
            g.px(x, y, L.grass_px(x, y))
    L.grass_shadow(g, 17, 45, 11, 3)
    # the trunk: white bark with dark lenticels
    for y in range(26, 46):
        for x in range(14, 18):
            c = "pw1" if x < 16 else "pw0"
            if (y * 5 + x * 3) % 9 == 0:
                c = "pk0"
            art.px(x, y, c)
        art.px(13, y, "pk0")
        art.px(18, y, "pk0")
    # the crown: a tall oval of shimmering leaves, silver beneath, green above
    rng = np.random.RandomState(seed)
    m = np.zeros((48, 32), bool)
    for y in range(1, 34):
        t = (y - 1) / 33
        r = 13 * (1 - (2 * t - 0.9) ** 2) ** 0.5 if abs(2 * t - 0.9) < 1 else 0
        for x in range(32):
            if abs(x - 15.5) <= r + 0.8 * np.sin(y * 1.3 + seed):
                m[y, x] = True
    for y, x in np.argwhere(m):
        u = (x - 3) / 26
        h = (x * 7 + y * 11 + seed) % 9
        if u < 0.35:
            c = "pg2" if h > 2 else "pw1"
        elif u < 0.7:
            c = "pg1" if h > 1 else "pg2"
        else:
            c = "pg0" if h > 3 else "pg1"
        if y > 26 and h < 3:
            c = "pg0"
        art.px(x, y, c)
    pad = np.pad(m, 1)
    edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in np.argwhere(edge):
        art.px(x, y, "pg0" if x > 12 else "pg1")
    # a few leaves flipped silver
    for _ in range(18):
        y, x = rng.randint(3, 30), rng.randint(5, 27)
        if m[y, x]:
            art.px(x, y, "pw1")
    if flip:
        art.a[:] = art.a[:, ::-1].copy()
        g.a[:] = g.a[:, ::-1].copy()
    for y in range(48):
        for x in range(32):
            a = art.a[y, x]
            dst = s.T if y < 16 else s.M
            if a[3]:
                dst.a[y, x] = a
            elif g.get(x, y) != L.grass_px(x, y):
                dst.a[y, x] = g.a[y, x]
    return s


def town(keys):
    return [spire(), broad(), twin(), old(), lamptree(), lamps_lit(), town_canopy(keys)]
