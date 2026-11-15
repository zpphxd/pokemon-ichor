"""Eleusa's farmyards: threshing floors, the winnowing, pithoi, the bread oven,
the vine pergola, the plough and the field wall.

The alonia (threshing floor) and the field wall are agros's own pieces, adopted
pixel for pixel (agros_rock.alonia, agros_rock.walls), so a threshing floor or
a wall looks the same on Route 2 and in the village. Eleusa adds a working
alonia centre (a grain heap and the threshing sledge) that drops into the
floor's middle 2 x 2.

Light from the top left; objects outlined in ink; small props stand on
borrowed aethos grass, so they cost no ground tiles.
"""
from __future__ import annotations

import numpy as np

import agros_rock
from eleusa_lib import Layer, grass, on_other_ground, put, struct

SEC = "farm"


def _adopt(a, key=None, title=None):
    """Re-home an agros Struct in an Eleusa section (pixels, walk, names, notes)."""
    s = struct(key or a.key, title or a.title, a.w, a.h, SEC, walk=a.walk, notes=a.notes,
               names=dict(a.names))
    for ln in ("bottom", "middle", "top"):
        s.layers[ln].a[:] = a.layers[ln].a
    s.behaviors = dict(a.behaviors)
    return s


def alonia():
    s = _adopt(agros_rock.alonia(), title="Alonia: the round threshing floor (agros)")
    s.notes = ("Agros's threshing floor, pixel for pixel: flagstones in a ring of upright "
               "stones, open to walk on. For harvest time, swap its middle 2 x 2 for "
               "`alonia_work` (the grain heap and the sledge).")
    return s


def alonia_work(base):
    """The alonia's middle 2 x 2 at threshing time: ears spread on the floor,
    a heap of grain in the centre, the sledge with its flint teeth, a fork."""
    s = struct("alonia_work", "Alonia at threshing time: middle 2 x 2", 2, 2, SEC,
               walk=["XX", "XX"],
               notes="Drop over the alonia's cells (1,1)-(2,2). The heap and the sledge "
                     "block; walk round them on the ring.")
    s.B.a[:] = base.B.a[16:48, 16:48]
    M = s.M
    # threshed ears spread across the flags
    for (x, y) in ((3, 3), (9, 2), (24, 4), (28, 9), (4, 25), (26, 27), (2, 14), (29, 20)):
        put(M, x, y, ["43", ".2"], {"4": "wh3", "3": "wh2", "2": "wh1"})
    # the heap of grain: a low gold mound lit from the top left
    for y in range(32):
        for x in range(32):
            d = ((x - 15.5) / 11.5) ** 2 + ((y - 17) / 8.5) ** 2
            if d <= 1:
                u = (x - 15.5) / 11.5 + (y - 17) / 8.5
                c = "wh3" if u < -0.5 else ("wh2" if u < 0.55 else "wh1")
                if (x * 7 + y * 3) % 11 == 0 and c != "wh1":
                    c = "p3"
                M.px(x, y, c)
            elif d <= 1.18 and y > 17:
                M.px(x, y, "l0")
    # the threshing sledge leaning on the heap's south side: a board with flints
    put(M, 4, 22, [
        "KKKKKKKKKKKKKKKKKKKKKKK",
        "KdwdwdwdwdwdwdwdwdwdwdK",
        "KwwwwwwwwwwwwwwwwwwwwwK",
        "KdKdKdKdKdKdKdKdKdKdKdK",
        ".KKKKKKKKKKKKKKKKKKKKK.",
    ], {"K": "ink", "w": "wd1", "d": "l0"})
    # a wooden fork stuck in the heap
    for i in range(9):
        M.px(21 + i // 3, 6 + i, "wd1")
    put(M, 18, 3, ["w.w.w", "wwwww"], {"w": "wd1"})
    return s


def winnowing():
    """The winnowing on borrowed grass: sacks of grain, the liknon with its
    grain, a heap of chaff the wind has blown aside."""
    s = struct("winnowing", "Winnowing: sacks, the liknon, the chaff", 3, 1, SEC, walk=["XXX"],
               on="grass", names={"sacks": (0, 0), "liknon": (1, 0), "chaff": (2, 0)},
               notes="Three props on aethos grass, to set beside a threshing floor. The "
                     "liknon is the winnowing basket the Mysteries carried, so it reappears "
                     "in the sanctum.")
    M = s.M
    # two linen sacks of grain, tied at the neck
    for ox, oy in ((1, 4), (7, 2)):
        put(M, ox, oy, [
            "..KKK...",
            "..K3K...",
            ".K232K..",
            "K33322K.",
            "K332221K",
            "K322211K",
            "K322111K",
            "K221111K",
            ".KK111K.",
            "...KKK..",
        ], {"K": "ink", "3": "p3", "2": "p2", "1": "p1"})
    put(M, 7, 3, ["...", "333"], {"3": "wh3"})
    # the liknon: a shovel-shaped wicker basket heaped with grain
    put(M, 17, 3, [
        "......KKKKK...",
        "....KK44434K..",
        "..KK4433332K..",
        ".K11333322211K",
        "K1212122221211K"[:14],
        "K21212121212K.",
        ".K212121212K..",
        "..KK2121KKK...",
        "....KKKK......",
    ], {"K": "ink", "4": "wh3", "3": "wh2", "2": "wh1", "1": "l1"})
    # chaff: a pale drift with a few husks blowing off east
    for y in range(16):
        for x in range(16):
            d = ((x - 7) / 6.5) ** 2 + ((y - 11) / 4) ** 2
            if d <= 1:
                M.px(32 + x, y, "p3" if (x + y) % 3 else "p2")
            elif d <= 1.25 and y >= 11:
                M.px(32 + x, y, "p1")
    for x, y in ((46, 6), (44, 4), (47, 9), (13 + 32, 8)):
        M.px(x, y, "p2")
    return s


PITHOS = [
    "....KKKKKK....",
    "...K334433K...",
    "...KK1111KK...",
    "..K32344432K..",
    ".K3343344331K.",
    "K334433443321K",
    "K334433443321K",
    "K3K4KK3KK4K21K",
    "K34K44K44K4K1K",
    "K334433443321K",
    "K334433443321K",
    "K334433433321K",
    "K334433433321K",
    "K334333333211K",
    "K33433333321K.",
    ".K3433333221K.",
    ".K3333333221K.",
    "..K33333221K..",
    "..K23332211K..",
    "...K322211K...",
    "...K222111K...",
    "....KK11KK....",
]


def pithoi():
    out = []
    s = struct("pithos", "A great pithos, taller than a man", 1, 2, SEC, walk=["T", "X"],
               on="grass",
               notes="The storage jar Pandora's box really was. Stand them in rows for a "
                     "granary yard. The rim draws over the player; the body blocks.")
    leg = {"K": "ink", "4": "rf3", "3": "tc2", "2": "tc1", "1": "tc0"}
    put(s.T, 1, 8, PITHOS[:8], leg)
    put(s.M, 1, 16, PITHOS[8:], leg)
    # its shadow on the grass, to the south east
    for x in range(9, 16):
        if x % 2 == 0:
            s.M.px(x, 30, "gd")
    out.append(s)
    s = struct("pithos_sunk", "Pithoi sunk to the shoulder", 2, 1, SEC, walk=["XX"], on="path",
               notes="A granary floor: two pithoi buried to the shoulder in beaten earth, one "
                     "with its stone lid on. On borrowed aethos path.")
    for ox, lid in ((1, True), (17, False)):
        put(s.M, ox, 2, [
            "...KKKKKKKK...",
            "..K33444433K..",
            ".K3KKKKKKKK3K.",
            "K34K111111K32K",
            "K33K111111K21K",
            "K332KKKKKK221K",
            ".K3322222221K.",
            "..KK1111111K..",
            "....KKKKKK....",
        ], {"K": "ink", "4": "rf3", "3": "tc2", "2": "tc1", "1": "wk"})
        if lid:
            put(s.M, ox + 2, 3, [
                ".KKKKKKKK.",
                "K33333332K",
                "K32222221K",
                ".KKKKKKKK.",
            ], {"K": "ink", "3": "p3", "2": "p2", "1": "p1"})
    out.append(s)
    return out


def oven():
    s = struct("oven", "The bread oven: a clay dome", 2, 2, SEC, walk=["XX", "XX"], on="grass",
               notes="A beehive oven of daub over a stone base, its mouth glowing, a peel "
                     "leaning on it. Barley loaves are Demeter's own bread.")
    M = s.M
    for y in range(32):
        for x in range(32):
            d = ((x - 15.5) / 13.5) ** 2 + ((y - 17) / 13) ** 2
            if d <= 1 and y < 27:
                u = (x - 15.5) / 13.5 + (y - 17) / 13
                c = "p3" if u < -0.7 else ("p2" if u < 0.1 else ("p1" if u < 0.7 else "l1"))
                M.px(x, y, c)
    M.outline("ink")
    # stone base
    for y in range(26, 31):
        for x in range(3, 29):
            M.px(x, y, "l1" if (x // 4 + y) % 2 else "l0")
    M.hline(3, 28, 31, "ink")
    M.vline(2, 26, 31, "ink")
    M.vline(29, 26, 31, "ink")
    M.hline(3, 28, 26, "p1")
    # the mouth, with embers
    put(M, 10, 17, [
        "..KKKKKKKKK..",
        ".KwwwwwwwwwK.",
        "KwhhhhhhhhhwK",
        "KwhhhwhhhhhwK",
        "Kw33w2w33hwwK",
        "Kw3w323w2w3wK",
        "KKKKKKKKKKKKK",
    ], {"K": "ink", "w": "wk", "h": "wk", "3": "wh3", "2": "wh2"})
    # smoke hole at the top
    put(M, 14, 3, ["KKK", "KwK"], {"K": "ink", "w": "wk"})
    # the peel leaning on the east side
    for i in range(14):
        M.px(27 + i // 5, 10 + i, "wh1")
    put(M, 24, 7, [".KK.", "K33K", "K33K", ".KK."], {"K": "ink", "3": "wh2"})
    # shadow on the grass
    for x in range(6, 32):
        if x % 2:
            M.px(x, 31, "l0")
    return s


def pergola():
    """A vine on a timber pergola: the canopy draws over the player, who walks
    beneath it; the two posts block."""
    s = struct("pergola", "Vine pergola", 3, 2, SEC, walk=["TTT", "X.X"], on="grass",
               notes="Timber posts under a grape vine. The top row is canopy drawn over the "
                     "player; walk between the posts. Set it before a door for a shaded "
                     "porch, or run it along a wall (repeat the middle column).")
    T, M = s.T, s.M
    # posts
    for px in (5, 42):
        for y in range(16, 30):
            M.px(px, y, "k1")
            M.px(px + 1, y, "k2")
            M.px(px + 2, y, "k1")
        M.hline(px - 1, px + 3, 30, "ink")
        for y in range(16, 30):
            M.px(px - 1, y, "ink")
            M.px(px + 3, y, "ink")
    # the canopy: vine leaves in clumps over a beam, with hanging bunches;
    # 16 px periodic, so the middle column repeats for a longer pergola
    LEAF = [
        "..1..2...1...2..",
        ".1121221.11.2212",
        "12221122111222111",
        "2211012211022110",
        "1100101100110010",
        "2112212211122122",
        "2211221112211221",
        "1100110011100110",
        "1221122012211220",
        "2211211112211211",
        "1110110011100110",
    ]
    for y, row in enumerate(LEAF):
        for x in range(48):
            ch = row[x % 16]
            if ch == ".":
                continue
            T.px(x, y, {"2": "lf2", "1": "lf1", "0": "lf0"}[ch])
    T.hline(0, 47, 11, "k2")
    T.hline(0, 47, 12, "k1")
    for gx in (5, 21, 37):
        put(T, gx, 12, ["K11K", "1221", "K11K", ".1K."], {"K": "ink", "1": "pp0", "2": "pp1"})
    T.outline("lf0")
    return s


def build():
    a = alonia()
    jars = pithoi()
    return [a, alonia_work(a), winnowing(), *jars, oven(),
            on_other_ground(jars[0], "pithos_path", "path", shadow="p1",
                            title="A great pithos, on beaten earth or paving")]
