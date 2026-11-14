"""Agros farm and roadside props: the carter's cart, the bee wall with its
clay hives, the spring in its little nymphaion, and a roadside shrine.
"""
from __future__ import annotations

from agros_lib import GRASS, Struct
from agros_rock import stones

SEC = "props"


def grass_floor(s):
    s.B.texture(GRASS, 0, 0, s.w * 16, s.h * 16)


def cart():
    """A two-wheeled farm cart, side on, shafts resting on the ground to the
    west, loaded with amphorae and a sack."""
    s = Struct("cart", "The carter's cart, loaded", 3, 2, SEC, walk=["XXX", "XXX"],
               notes="Shafts to the west, where the Mudbray stands. Impassable.")
    grass_floor(s)
    B, M = s.B, s.M
    for x in range(6, 46):                       # its shadow
        for y in (28, 29, 30):
            if (x + y) % 2 == 0 and B.get(x, y) != "gd":
                B.px(x, y, "gd")
    # shafts, angling down to the ground at the west
    M.line(0, 25, 14, 17, "ink")
    M.line(0, 24, 14, 16, "wd2")
    M.line(1, 26, 14, 18, "wd1")
    # the bed
    M.rect(12, 14, 33, 3, "wd2")
    M.hline(12, 44, 13, "ink")
    M.hline(12, 44, 17, "ink")
    M.rect(12, 18, 33, 2, "wd1")
    M.hline(12, 44, 20, "ink")
    for x in range(14, 44, 6):
        M.vline(x, 14, 19, "wd1")
    M.vline(12, 13, 20, "ink")
    M.vline(44, 13, 20, "ink")
    # side rails
    for x in (13, 24, 34, 43):
        M.vline(x, 8, 13, "ink")
        M.vline(x + 1, 8, 13, "wd2")
    M.hline(13, 44, 8, "ink")
    M.hline(14, 43, 9, "wd2")
    # load: three amphorae and a sack, behind the rail
    for i, ax in enumerate((16, 22, 28)):
        M.blit([
            " kkk ",
            " kck ",
            "kbcck",
            "kcccc",
            "kbccc",
            "kcccc",
            " kck ",
            "  k  ",
        ], {"k": "ink", "c": "tc1", "b": "tc2"}, ax, 1 + (i % 2))
    M.ellipse(34, 2, 43, 11, "ink")
    M.ellipse(35, 3, 42, 10, "p1")
    M.ellipse(35, 3, 40, 7, "p2")
    M.line(38, 2, 40, 4, "l1")
    # rails drawn again in front of the load
    for x in (24, 34):
        M.vline(x, 8, 13, "ink")
        M.vline(x + 1, 9, 13, "wd2")
    M.hline(14, 43, 9, "wd2")
    # the wheel: spokes, rim, hub
    cx, cy, r = 29, 22, 8
    for y in range(cy - r - 1, cy + r + 2):
        for x in range(cx - r - 1, cx + r + 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if r - 1.5 <= d <= r + 0.5:
                M.px(x, y, "ink" if d > r - 0.3 else "wd1")
    for (dx, dy) in ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
        M.line(cx, cy, cx + dx * (r - 2), cy + dy * (r - 2), "wd2")
    M.ellipse(cx - 2, cy - 2, cx + 2, cy + 2, "ink")
    M.px(cx, cy, "tg")
    return s


def bee_wall():
    """A bee wall: a dry-stone wall with niches, each holding a horizontal clay
    hive, its mouth to the sun; bees drifting."""
    s = Struct("bee_wall", "Bee wall with three clay hives", 3, 2, SEC, walk=["XXX", "XXX"],
               notes="The Greek way of keeping bees: long clay hives laid in a stone wall. "
                     "Komatas's terraces. Impassable.")
    grass_floor(s)
    M = s.M
    stones(M, 0, 4, 48, 24, seed=5, ramp=["k1", "l1", "p1", "p2", "p2"], mortar="k1")
    M.hline(0, 47, 3, "k1")
    M.hline(0, 47, 4, "p2")
    for x in range(48):
        if x % 2 == 0:
            M.px(x, 28, "gd")
        M.px(x, 27, "k1")
    for i, hx in enumerate((3, 18, 33)):
        # the niche
        M.rect(hx, 10, 12, 11, "k1")
        # the hive: a clay cylinder seen end-on to the south, body going back
        M.ellipse(hx + 1, 11, hx + 11, 20, "ink")
        M.ellipse(hx + 2, 12, hx + 10, 19, "tc1")
        M.ellipse(hx + 2, 12, hx + 7, 16, "tc2")
        M.ellipse(hx + 4, 14, hx + 8, 17, "tc0")
        M.ellipse(hx + 5, 15, hx + 7, 16, "ink")       # the mouth
        M.hline(hx + 3, hx + 9, 20, "tc0")
    for (x, y) in ((9, 8), (12, 6), (25, 7), (28, 9), (40, 6), (44, 9), (16, 24), (31, 23), (21, 2)):
        M.px(x, y, "ink")
        M.px(x + 1, y, "tg")
    return s


def spring():
    """A spring house: water from a lion's mouth in a whitewashed niche, falling
    into a stone basin."""
    s = Struct("spring", "Spring in a little nymphaion", 3, 2, SEC, walk=["XXX", "XXX"],
               notes="A roadside spring: a whitewashed aedicule with a blue niche, water "
                     "running into a basin. Impassable.")
    grass_floor(s)
    M = s.M
    # aedicule: pediment, two pilasters, the niche
    M.poly([(10, 6), (24, 0), (38, 6)], "ink")
    M.poly([(12, 6), (24, 1), (36, 6)], "w0")
    M.hline(13, 35, 5, "w1")
    M.rect(10, 6, 29, 2, "w1")
    M.hline(10, 38, 6, "ink")
    M.rect(10, 8, 5, 14, "w0")
    M.rect(34, 8, 5, 14, "w0")
    M.vline(14, 8, 21, "w1")
    M.vline(38, 8, 21, "w1")
    M.vline(9, 6, 22, "ink")
    M.vline(39, 6, 22, "ink")
    M.rect(15, 8, 19, 14, "b1")
    M.ellipse(15, 4, 33, 14, "b1")
    M.rect(16, 9, 2, 12, "b2")
    # the lion's mouth and its stream
    M.ellipse(21, 10, 27, 15, "k3")
    M.ellipse(22, 11, 26, 14, "k2")
    M.px(24, 13, "ink")
    M.vline(24, 15, 24, "b4")
    M.vline(23, 16, 24, "b3")
    # the basin
    M.rect(6, 22, 37, 7, "k3")
    M.hline(6, 42, 22, "w1")
    M.rect(8, 24, 33, 4, "b2")
    M.hline(9, 39, 24, "b3")
    M.px(23, 25, "b4")
    M.px(25, 25, "b4")
    M.px(21, 26, "b4")
    M.rect(6, 29, 37, 2, "k2")
    M.hline(6, 42, 31, "ink")
    M.vline(5, 22, 31, "ink")
    M.vline(43, 22, 31, "ink")
    return s


def shrine():
    """A roadside shrine: a whitewashed naiskos on a step, its niche Aegean blue,
    a clay lamp burning low."""
    s = Struct("shrine", "Roadside shrine", 1, 2, SEC, walk=["X", "X"],
               notes="For a fork or a field gate. Impassable.")
    grass_floor(s)
    M = s.M
    M.poly([(1, 8), (8, 2), (15, 8)], "ink")
    M.poly([(3, 8), (8, 3), (13, 8)], "w0")
    M.hline(1, 14, 8, "ink")
    M.rect(2, 9, 12, 14, "w0")
    M.vline(13, 9, 22, "w1")
    M.vline(1, 8, 23, "ink")
    M.vline(14, 8, 23, "ink")
    M.rect(5, 11, 6, 8, "b1")
    M.ellipse(5, 9, 10, 14, "b1")
    M.rect(5, 15, 2, 4, "b2")
    M.blit([" kk ", "kllk", " kk "], {"k": "ink", "l": "l1"}, 6, 16)
    M.px(8, 15, "b4")
    M.rect(0, 23, 16, 3, "w1")
    M.hline(0, 15, 23, "w0")
    M.hline(0, 15, 26, "ink")
    M.vline(0, 23, 26, "ink")
    M.vline(15, 23, 26, "ink")
    for x in range(1, 16, 2):
        M.px(x, 27, "g1")
    return s


def build():
    return [cart(), bee_wall(), spring(), shrine()]
