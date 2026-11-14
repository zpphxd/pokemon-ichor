"""Agros trees, shrubs and herbs: the ancient olive, a fig, broom, oleander,
thyme, field herbs, scattered stones and the soft shade under trees.

Light falls from the top left. Foliage is built from clusters, each lit on
its upper left and shaded on its lower right, with a dark rim; trunks are
grey olive bark. Everything stands on aethos grass painted into the bottom
layer, so a piece can sit anywhere in a meadow.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from agros_lib import GRASS, Struct

SEC = "flora"


def disc(w, h, cx, cy, rx, ry):
    m = Image.new("1", (w, h), 0)
    ImageDraw.Draw(m).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=1)
    return np.array(m, bool)


def foliage(L, clusters, ramp, rim, speck=None, region=None):
    """Paint leafy clusters [(cx, cy, rx, ry)] onto layer L.

    ramp: dark -> light colors. Each cluster is shaded by the angle to the
    light (top left) and outlined with `rim` where it meets the background or
    a cluster in front. Later clusters sit in front of earlier ones."""
    H, W = L.h, L.w
    owner = np.full((H, W), -1)
    for i, (cx, cy, rx, ry) in enumerate(clusters):
        owner[disc(W, H, cx, cy, rx, ry)] = i
    for y in range(H):
        for x in range(W):
            i = owner[y, x]
            if i < 0 or (region is not None and not region[y, x]):
                continue
            cx, cy, rx, ry = clusters[i]
            # position inside the cluster: -1 (lit, top left) .. +1 (shade)
            u = ((x - cx) / max(rx, 1) + (y - cy) / max(ry, 1)) / 2
            leaf = ((x * 5 + y * 3) % 7 == 0) or ((x * 3 + y * 7) % 11 == 0)
            k = 0.5 - 0.6 * u + (0.18 if leaf else 0)
            idx = int(max(0, min(len(ramp) - 1, round(k * (len(ramp) - 1)))))
            c = ramp[idx]
            if speck and leaf and k > 0.85:
                c = speck
            L.px(x, y, c)
    # rims: where a cluster meets the background or a later (front) cluster's
    # edge, so lobes read separately
    for y in range(H):
        for x in range(W):
            i = owner[y, x]
            if i < 0 or (region is not None and not region[y, x]):
                continue
            for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                j = owner[y + dy, x + dx] if 0 <= y + dy < H and 0 <= x + dx < W else -1
                if j < 0 or (j > i and (dx, dy) in ((1, 0), (0, 1))):
                    L.px(x, y, rim)
                    break


def grass_floor(s):
    s.B.texture(GRASS, 0, 0, s.w * 16, s.h * 16)


def shade(L, cx, cy, rx, ry):
    """A soft shadow on grass: solid core, dithered rim."""
    for y in range(L.h):
        for x in range(L.w):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 0.55 or (d <= 1.0 and (x + y) % 2 == 0):
                if L.get(x, y) in ("g2", "g3", "g1"):
                    L.px(x, y, "gd" if L.get(x, y) == "g1" else "g1")


# --------------------------------------------------------------------------

def big_olive():
    """The ancient olive of Route 1: a crown 4 cells wide over a twisted, hollow
    trunk splitting in three, roots gripping the ground."""
    s = Struct("big_olive", "The big olive: an ancient tree, 4 by 4", 4, 4, SEC,
               walk=["TTTT", "XXXX", "XXXX", "XXXX"],
               notes="Route 1's landmark. The top row is crown drawn over the player, who "
                     "can walk behind it; the rest is impassable. Its trunk is hollow at "
                     "the bottom middle, under the crown's shadow.")
    grass_floor(s)
    B, M, T = s.B, s.M, s.T
    shade(B, 33, 57, 28, 6)
    # The trunk: three twisted strands that part into limbs, plus two roots.
    strands = [
        [(21, 63, 5.0), (24, 55, 5.0), (21, 47, 4.0), (14, 38, 3.0), (9, 32, 2.0)],
        [(33, 63, 6.0), (31, 54, 5.5), (34, 46, 4.5), (33, 36, 3.5), (31, 28, 2.5)],
        [(44, 63, 5.0), (41, 55, 5.0), (45, 47, 4.0), (52, 39, 3.0), (57, 32, 2.0)],
        [(12, 63, 2.5), (20, 59, 3.0)],
        [(54, 63, 2.5), (45, 59, 3.0)],
    ]
    mask = np.zeros((64, 64), bool)
    side = np.zeros((64, 64))      # 0 = lit edge of a strand, 1 = shaded edge
    yy, xx = np.mgrid[0:64, 0:64]
    for pts in strands:
        for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
            for t in np.linspace(0, 1, 24):
                cx, cy, r = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r0 + (r1 - r0) * t
                d = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
                side[d & ~mask] = ((xx - cx + r) / (2 * r))[d & ~mask]
                mask |= d
    for y in range(64):
        for x in range(64):
            if not mask[y, x] or y < 26:
                continue
            u = side[y, x]
            c = "k3" if u < 0.3 else "k2" if u < 0.72 else "k1"
            if (y + int(u * 9)) % 6 == 0 and 0.15 < u < 0.9:
                c = "k1"           # bark furrows twisting up the strands
            M.px(x, y, c)
    # strands overlap: a dark seam where they meet
    for y in range(40, 62):
        for x in range(1, 63):
            if mask[y, x] and abs(side[y, x] - side[y, x - 1]) > 0.5 and mask[y, x - 1]:
                M.px(x, y, "k1")
    M.ellipse(28, 51, 35, 61, "ink")                   # the hollow at the foot
    M.ellipse(29, 53, 33, 61, "k1")
    M.ellipse(30, 55, 33, 61, "ink")
    M.outline("ink")
    # The crown: many small leaf clumps in a broad, uneven dome; the part in
    # row 0 goes to the top layer so the player can walk behind it.
    clusters = []
    rows = [(9, [(18, 5), (29, 4), (41, 5)]),
            (15, [(9, 5), (20, 6), (32, 6), (44, 6), (55, 5)]),
            (22, [(5, 5), (15, 6), (26, 6), (38, 6), (49, 6), (59, 5)]),
            (29, [(9, 6), (20, 6), (31, 5), (43, 6), (54, 6)]),
            (35, [(4, 4), (14, 5), (46, 5), (59, 4)])]
    for cy, row in rows:
        for cx, r in row:
            clusters.append((cx, cy, r + 1, r))
    crown = Struct("tmp", "", 4, 4, SEC).M
    foliage(crown, clusters, ["t0", "t1", "gd", "o4", "o5"], "t0", speck="o5")
    for y in range(64):
        for x in range(64):
            c = crown.get(x, y)
            if c:
                (T if y < 16 else M).px(x, y, c)
    return s


def fig():
    """A fig: broad lobed leaves, darker than an olive, on a pale smooth trunk."""
    s = Struct("fig", "Fig tree, 2 by 2", 2, 2, SEC, walk=["XX", "XX"],
               notes="A smaller tree for field corners and the spring.")
    grass_floor(s)
    shade(s.B, 17, 28, 13, 4)
    s.M.blit([
        "      kMk  kMk     ",
        "       kMk kMk     ",
        "        kMMMk      ",
        "        kMMMk      ",
        "        kMMMMk     ",
        "       kMMMMMMk    ",
        "      kk     kk    ",
    ], {"k": "ink", "M": "k3"}, 7, 22)
    clusters = [(9, 12, 8, 7), (23, 11, 8, 7), (16, 7, 9, 6), (12, 19, 8, 5), (21, 19, 8, 5)]
    foliage(s.M, clusters, ["c1", "c2", "c3", "gd"], "c1", speck="g3")
    return s


def shrub(key, title, clusters, ramp, rim, flowers, walk="X", notes=""):
    s = Struct(key, title, 1, 1, SEC, walk=[walk], notes=notes)
    grass_floor(s)
    shade(s.B, 8, 14, 7, 2)
    foliage(s.M, clusters, ramp, rim)
    for (x, y, c) in flowers:
        s.M.px(x, y, c)
    return s


def shrubs():
    out = []
    out.append(shrub("broom", "Broom in flower", [(5, 8, 5, 5), (11, 8, 5, 5), (8, 5, 6, 4)],
                     ["t0", "t1", "c2", "gd"], "t0",
                     [(x, y, "tg" if (x + y) % 3 else "y2") for (x, y) in
                      ((4, 4), (7, 3), (10, 4), (12, 6), (3, 7), (6, 6), (9, 7), (13, 9), (5, 10),
                       (8, 9), (11, 11), (2, 10))],
                     notes="Yellow broom, a low wild shrub. Impassable."))
    out.append(shrub("oleander", "Oleander in flower", [(5, 9, 5, 5), (11, 9, 5, 5), (8, 5, 6, 5)],
                     ["t0", "t1", "c2", "gd"], "t0",
                     [(x, y, c) for (x, y, c) in
                      ((5, 3, "op2"), (6, 3, "op3"), (6, 4, "op1"), (10, 4, "op2"), (11, 4, "op3"),
                       (11, 5, "op1"), (3, 8, "op2"), (4, 8, "op3"), (13, 8, "op2"), (12, 8, "op3"),
                       (8, 8, "op2"), (8, 7, "op3"), (9, 8, "op1"), (6, 11, "op2"), (10, 11, "op2"))],
                     notes="Pink oleander, the shrub of dry streambeds. Impassable."))
    # thyme: a low cushion the player walks over
    s = Struct("thyme", "Wild thyme", 1, 1, SEC, walk=["."],
               notes="A low cushion of thyme on grass; walkable.")
    grass_floor(s)
    s.B.blit([
        "                ",
        "                ",
        "                ",
        "      d  d      ",
        "    dTdddTd     ",
        "   dTttdtTtd    ",
        "  dttTtttttTd   ",
        "  dtttttTttttd  ",
        "   dddtttttdd   ",
        "      ddddd     ",
        "          d  d  ",
        "  d     dTdTdd  ",
        " dTd   dtttttd  ",
        " dtd    ddddd   ",
        "  d             ",
        "                ",
    ], {"d": "gd", "t": "th1", "T": "th2"}, 0, 0)
    out.append(s)
    # field herbs: sprigs with white chamomile heads
    s = Struct("herbs", "Field herbs and chamomile", 1, 1, SEC, walk=["."],
               notes="Sprigs and chamomile on grass; walkable.")
    grass_floor(s)
    s.B.blit([
        "                ",
        "   w            ",
        "  wyw     w     ",
        "   w     wyw    ",
        "   t      w     ",
        "  ttT     t     ",
        "   t     tTt    ",
        "          t     ",
        "       w        ",
        "      wyw    w  ",
        "       w    wyw ",
        "  t    t     w  ",
        " tTt  tTt    t  ",
        "  t    t    tTt ",
        "             t  ",
        "                ",
    ], {"w": "p3", "y": "tg", "t": "t1", "T": "t3"}, 0, 0)
    out.append(s)
    return out


def tree_shade():
    """Soft shade cast by an olive, for the two cells below its trunk."""
    s = Struct("tree_shade", "Soft shade under a tree", 2, 1, SEC, walk=[".."],
               notes="Put under a 2x2 olive's bottom row; walkable grass in shade.")
    grass_floor(s)
    shade(s.B, 17, 3, 15, 5)
    return s


def build():
    return [big_olive(), fig(), *shrubs(), tree_shade()]
