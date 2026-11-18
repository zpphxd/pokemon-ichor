"""Kythera's fresh water: the Neraida falls (lip, foot, the thin falls, the cliff
beside a fall), mossy pink-stone kerbs for pools and the river, the Spring of
Kallirhoe's round pool, stepping stones, a plank bridge, weirs, the water-mill
with its turning wheel (and the still, broken wheels of the idle mills), the
Foam Road's spring basin, the Minoan vault door, and the rock stair down to
Echo's caves.

The water is aethos's: falling water borrows its waterfall (0x0B3), pools and
the river its turquoise shallows (0x0D1), both animated. These pieces draw only
the stone, the foam and the wood over it.
"""
from __future__ import annotations

import math

import numpy as np

import kythera_lib as K
from kythera_lib import anim_layer, ground, put, struct
from kythera_coast import bubbles, foam_ring, stone_px, wob

SEC = "water"
GRASS = 0x001


def grass_px(X, Y):
    rgb = tuple(int(v) for v in K.aethos(GRASS)[Y % 16, X % 16])
    n = K.A.RGB2NAME[rgb]
    return "g2" if n == "g3" else n


def mossy_stone(L, ox, oy, pts, seed=0, moss=True):
    """A rounded pink stone (a polygon), lit top-left, moss on its crown."""
    sub = K.Layer(L.w, L.h)
    sub.poly([(ox + x, oy + y) for x, y in pts], "rm3")
    ys, xs = np.nonzero(sub.a[..., 3] > 0)
    if not len(xs):
        return sub
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    for y, x in zip(ys, xs):
        u = (x - x0) / max(1, x1 - x0)
        v = (y - y0) / max(1, y1 - y0)
        k = K.h(int(x), int(y), seed)
        if u + v < 0.6:
            c = "rm4" if k % 4 else "rm5"
        elif u + v < 1.2:
            c = "rm3"
        elif u + v < 1.6:
            c = "rm2"
        else:
            c = "rm1"
        if moss and v < 0.35 and k % 3 == 0:
            c = "my2" if k % 2 else "my3"
        L.px(int(x), int(y), c)
    sub.outline("rm0")
    for y, x in zip(*np.nonzero(sub.a[..., 3] > 0)):
        if sub.get(int(x), int(y)) == "rm0":
            L.px(int(x), int(y), "rm0")
    return sub


# --------------------------------------------------------------------------
# Falls
# --------------------------------------------------------------------------

def falls():
    names = {"lip_L": (0, 0), "lip_R": (1, 0), "foot_L": (0, 1), "foot_R": (1, 1),
             "face_fall_L": (2, 0), "face_fall_R": (3, 0), "thin_fall": (4, 0), "thin_foot": (4, 1),
             "thin_sea": (5, 1), "basin": (5, 0), "foot_face_L": (2, 1), "foot_face_R": (3, 1)}
    s = struct("falls", "Waterfalls, and the Foam Road's spring basin", 6, 2, SEC,
               walk=["FFXXFX", "PPXXPW"], names=names,
               notes="Falling water is aethos's waterfall (0x0B3, `MB_WATERFALL`, animated): build a "
                     "fall's column from it, two wide for the Neraida falls. These finish it. "
                     "`lip_L` `lip_R` sit at the top, where the river curls over (borrowed waterfall). "
                     "`foot_L` `foot_R` at the bottom, the plunge churning white in turquoise water "
                     "(borrowed shallows, animated foam, `MB_POND_WATER`). The pink cliff beside a "
                     "fall: `face_fall_L` (the face to the fall's west, wet and mossy at its east "
                     "edge) and `face_fall_R`, and at their feet `foot_face_L` / `_R`. "
                     "`thin_fall` is a thin cascade, one cell wide, rock on either side of a "
                     "narrow stream (the spring's fall, and the Foam Road's Horn gate); "
                     "`thin_foot` its foot in a pool, `thin_sea` its foot in the sea (borrowed "
                     "sea). `basin` is the Foam Road's rest point: the freshwater spring's stone "
                     "basin under the cliff's `seep` (borrowed shallows; impassable, read it).")
    ground(s, "fall", [(0, 0), (1, 0), (4, 0)])
    ground(s, "shallow", [(0, 1), (1, 1), (4, 1), (5, 0)])
    ground(s, "sea", [(5, 1)])
    M, B = s.M, s.B
    frames = anim_layer(s, "surf", 3)
    allf = [M] + frames
    # lip: the river's edge curling over: a bright crest, streaks below
    for cx in (0, 1):
        ox = cx * 16
        for x in range(16):
            X = ox + x
            crest = 4 + int(round(wob(X, 0.5) * 0.6))
            for y in range(0, crest):
                M.px(X, y, "kq1" if (x + y) % 4 else "kq2")
            M.px(X, crest, "w0")
            M.px(X, crest + 1, "w0" if x % 3 else "kq2")
            M.px(X, crest + 2, "kq2" if x % 2 else "b4")
            if x % 4 == 1:
                M.px(X, crest + 3, "w0")
    # foot: churning foam in the plunge pool (animated)
    for cx in (0, 1):
        ox, oy = cx * 16, 16
        for f, L in enumerate(allf):
            for y in range(16):
                for x in range(16):
                    X, Y = ox + x, oy + y
                    d = y - (6 + (f - 1) + wob(X + 3 * f, 0.5))
                    if d < -4:
                        L.px(X, Y, "w0" if bubbles(X, Y, f) or y < 2 else "kq2")
                    elif d < 0:
                        L.px(X, Y, "w0" if bubbles(X, Y, f) else ("kq2" if (x + y) % 2 else None))
                    elif d < 3 and bubbles(X, Y, f + 1):
                        L.px(X, Y, "kq2")
    # the cliff beside a fall: pink stone, its edge on the fall's side wet
    for cx, side in ((2, "L"), (3, "R")):
        ox = cx * 16
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, y
                c = stone_px(X, Y)
                near = (15 - x) if side == "L" else x
                if near < 3:
                    c = "rm1" if (y + near) % 3 else "rm0"
                    if near == 0 and y % 4 == 1:
                        c = "w0"
                elif near < 5 and (x + y) % 3 == 0:
                    c = "my2"
                B.px(X, Y, c)
        # its foot: the face's base and spray on the pool's stones
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, 16 + y
                near = (15 - x) if side == "L" else x
                if y < 6:
                    c = stone_px(X, Y)
                    if y >= 4:
                        c = "rm1"
                    if near < 3:
                        c = "rm0" if y % 2 else "rm1"
                elif y < 9:
                    c = "rm2" if (x + y) % 3 else "my2"
                else:
                    c = grass_px(X, Y)
                    if near < 3 and (x + 2 * y) % 5 == 0:
                        c = "w0"
                B.px(X, Y, c)
    # thin fall: rock on both sides of a narrow stream
    ox = 64
    for y in range(16):
        l = 5 + int(round(wob(y, 0.4) * 0.5))
        r = 10 + int(round(wob(y + 7, 0.4) * 0.5))
        for x in range(16):
            if x < l or x > r:
                c = stone_px(ox + x, y)
                if x == l - 1 or x == r + 1:
                    c = "rm0"
                elif x == l - 2 or x == r + 2:
                    c = "my2" if y % 3 == 0 else "rm1"
                M.px(ox + x, y, c)
    # thin foot in a pool (animated foam ring) and in the sea
    for (cx, cy) in ((4, 1), (5, 1)):
        ox, oy = cx * 16, cy * 16
        sub = K.Layer(M.w, M.h)
        sub.rect(ox + 5, oy, 6, 3, "w0")
        for f, L in enumerate(allf):
            for y in range(0, 4):
                for x in range(5, 11):
                    L.px(ox + x, oy + y, "w0" if (x + y + f) % 3 else "kq2")
        foam_ring(allf, ox, oy, 16, 16, lambda X, Y, sub=sub: sub.get(X, Y) is not None,
                  width=(2, 3, 2))
    # basin: a stone trough under the seep, clear water in it
    ox, oy = 80, 0
    for y in range(16):
        for x in range(16):
            rim = x < 2 or x > 13 or y < 3 or y > 12
            if rim:
                c = "rm4" if (y < 3 or x < 2) else "rm2"
                if y == 0 or x == 0:
                    c = "rm5"
                if y > 13 or x > 14:
                    c = "rm1"
                if y == 15:
                    c = "rm0"
                M.px(ox + x, oy + y, c)
    for x in range(2, 14):
        M.px(ox + x, oy + 3, "rm1")
    put(M, ox + 6, oy + 4, ["w.w", ".w."], {"w": "w0"})
    K.settle(s, "surf", [(0, 1), (1, 1), (4, 1), (5, 1)])
    return s


# --------------------------------------------------------------------------
# Kerbs for pools and the river
# --------------------------------------------------------------------------

def kerb():
    """Mossy pink stones edging turquoise water. Directions name where the
    water is (as the surf's do)."""
    names = {"S": (0, 0), "N": (1, 0), "E": (2, 0), "W": (3, 0),
             "NW": (4, 0), "NE": (5, 0), "SW": (6, 0), "SE": (7, 0),
             "in_NW": (0, 1), "in_NE": (1, 1), "in_SW": (2, 1), "in_SE": (3, 1),
             "stones": (4, 1), "stones_b": (5, 1), "reeds": (6, 1), "lily": (7, 1)}
    s = struct("kerb", "Mossy stone kerbs for pools and the river", 8, 2, SEC,
               walk=["XXXXXXXX", "XXXX..PP"], names=names,
               notes="Rounded pink stones with moss on their crowns, edging aethos's turquoise "
                     "shallows (borrowed, animated): the plunge pools, the upper pool, the Neraida "
                     "river's banks. Edges are named by where the water is: `S` has grass to the "
                     "north and water to the south. Corners are named as the pool's corners: `NW` "
                     "is a pool's north-west corner (water to its south-east); `in_NW` is the "
                     "corner of a tongue of land reaching into the water (land only to the "
                     "north-west). "
                     "`stones` and `stones_b` are stepping stones (walkable, borrowed water round "
                     "them); `reeds` a clump of reeds in the shallows; `lily` lily pads. Kerb cells "
                     "are impassable.")
    ground(s, "shallow")
    M = s.M

    def edge(cx, cy, sd):
        """sd(x, y) > 0 on land. Grass on land, a band of stones at the edge,
        water (transparent) beyond."""
        ox, oy = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                d = sd(x, y)
                if d > 3.0:
                    M.px(ox + x, oy + y, grass_px(ox + x, oy + y))
        # stones along the band where -3 < d < 4
        rng = []
        for j in range(4):
            for i in range(4):
                hh = K.h(i + cx * 4, j + cy * 4, 31)
                px_ = i * 4 + 1 + hh % 2
                py_ = j * 4 + 1 + (hh // 2) % 2
                d = sd(px_, py_)
                if -3.5 < d < 3.5:
                    rng.append((px_, py_, 2.6 + (hh % 3) * 0.5, hh))
        for (px_, py_, r, hh) in rng:
            pts = [(px_ + r * math.cos(a) * (1 + 0.15 * math.sin(3 * a + hh)),
                    py_ + r * 0.85 * math.sin(a) * (1 + 0.15 * math.sin(2 * a + hh)))
                   for a in np.linspace(0, 2 * math.pi, 10, endpoint=False)]
            mossy_stone(M, ox, oy, pts, seed=hh)
        # the waterline: a dark lip under the stones on the water side
        for y in range(16):
            for x in range(16):
                d = sd(x, y)
                if -4.5 < d < -2.5 and M.get(ox + x, oy + y) is None and (x + y) % 2:
                    M.px(ox + x, oy + y, "rm1")

    S_ = lambda x, y: 7.5 - y
    N_ = lambda x, y: y - 8.5
    E_ = lambda x, y: 7.5 - x
    W_ = lambda x, y: x - 8.5

    def io(a, b, r=4.0):
        if a < r and b < r:
            return r - math.hypot(r - a, r - b)
        return min(a, b)

    def iu(a, b, r=4.0):
        return -io(-a, -b, r)

    edge(0, 0, S_)
    edge(1, 0, N_)
    edge(2, 0, E_)
    edge(3, 0, W_)
    # a pool's corners: land on two sides, water in the opposite quarter
    edge(4, 0, lambda x, y: iu(S_(x, y), E_(x, y)))      # NW: land north and west
    edge(5, 0, lambda x, y: iu(S_(x, y), W_(x, y)))      # NE
    edge(6, 0, lambda x, y: iu(N_(x, y), E_(x, y)))      # SW
    edge(7, 0, lambda x, y: iu(N_(x, y), W_(x, y)))      # SE
    # a tongue of land: land in one quarter only
    edge(0, 1, lambda x, y: io(S_(x, y), E_(x, y)))      # land NW
    edge(1, 1, lambda x, y: io(S_(x, y), W_(x, y)))      # land NE
    edge(2, 1, lambda x, y: io(N_(x, y), E_(x, y)))      # land SW
    edge(3, 1, lambda x, y: io(N_(x, y), W_(x, y)))      # land SE
    # stepping stones
    for (cx, pts_list) in ((4, [[(3, 4), (7, 2), (12, 4), (13, 9), (9, 12), (4, 11)]]),
                           (5, [[(1, 5), (5, 3), (8, 6), (7, 10), (3, 11)],
                                [(9, 8), (12, 6), (15, 9), (13, 13), (10, 13)]])):
        for pts in pts_list:
            st = mossy_stone(M, cx * 16, 16, pts, seed=cx, moss=False)
        for y in range(16, 32):
            for x in range(cx * 16, cx * 16 + 16):
                if M.get(x, y) is None and M.get(x, y - 1) in ("rm0",) and (x + y) % 2:
                    M.px(x, y, "rm1")
    # reeds and lilies
    for (rx, ry) in ((3, 2), (6, 1), (9, 3), (12, 2), (5, 6), (10, 7)):
        for k in range(6):
            M.px(96 + rx + (k // 3), 16 + ry + k, "my3" if k < 2 else "my2")
        M.px(96 + rx, 16 + ry - 1, "rm1")
    for (lx, ly) in ((2, 3), (9, 2), (5, 9), (11, 10)):
        put(M, 112 + lx, 16 + ly, [".mm.", "m33m", "mm3m", ".mm."], {"m": "my2", "3": "my3"})
    put(M, 112 + 7, 16 + 6, [".w.", "wrw", ".w."], {"w": "w0", "r": "rm3"})
    return s


# --------------------------------------------------------------------------
# The Spring of Kallirhoe: a round pool
# --------------------------------------------------------------------------

def spring_pool():
    s = struct("spring_pool", "The Spring of Kallirhoe's round pool", 4, 4, SEC,
               walk=["XXXX", "XPPX", "XPPX", "XXXX"], names={"north": (1, 0), "south": (1, 3)},
               notes="Kallirhoe's pool: a ring of worn, mossy stones round clear turquoise water "
                     "(borrowed shallows, animated), 4 x 4. The youth kneels on the grass just south "
                     "of it; put `falls.thin_fall` against its north side for the thin fall from "
                     "the rock lip, and ring it with `flowers.narcissus`. The water cells are "
                     "`MB_POND_WATER`; the rim is impassable.")
    ground(s, "shallow")
    M = s.M
    cx_, cy_ = 32, 32
    R0, R1 = 20.0, 27.5
    for y in range(64):
        for x in range(64):
            d = math.hypot(x + 0.5 - cx_, (y + 0.5 - cy_) * 1.05)
            if d >= R1:
                M.px(x, y, grass_px(x, y))
    # the ring of stones
    n = 22
    for i in range(n):
        a = 2 * math.pi * i / n + 0.1
        r = (R0 + R1) / 2
        sx = cx_ + r * math.cos(a)
        sy = cy_ + r * math.sin(a) / 1.05
        rr = 3.6 + 0.6 * ((i * 7) % 3)
        pts = [(sx + rr * math.cos(b) * (1 + 0.12 * math.sin(3 * b + i)),
                sy + rr * 0.85 * math.sin(b)) for b in np.linspace(0, 2 * math.pi, 10, endpoint=False)]
        mossy_stone(M, 0, 0, pts, seed=i)
    # grass filling gaps behind the stones
    for y in range(64):
        for x in range(64):
            d = math.hypot(x + 0.5 - cx_, (y + 0.5 - cy_) * 1.05)
            if R1 - 3.5 < d < R1 and M.get(x, y) is None:
                M.px(x, y, grass_px(x, y))
            elif R0 - 1.5 < d <= R0 + 0.5 and M.get(x, y) is None and (x + y) % 2:
                M.px(x, y, "rm1")
    # a slab where you kneel (south), a sunken step
    put(M, 26, 52, [
        "aaaaaaaaaaaa",
        "a5555555555b",
        "a4444444444b",
        "bbbbbbbbbbbb",
    ], {"a": "rm5", "5": "rm5", "4": "rm4", "b": "rm2"})
    return s


# --------------------------------------------------------------------------
# Bridge and weirs
# --------------------------------------------------------------------------

def bridge_weir():
    names = {"bridge_W": (0, 0), "bridge": (1, 0), "bridge_E": (2, 0), "bridge_N": (3, 0),
             "bridge_V": (3, 1), "bridge_S": (3, 2),
             "weir_W": (0, 1), "weir": (1, 1), "weir_E": (2, 1),
             "weir_low_W": (0, 2), "weir_low": (1, 2), "weir_low_E": (2, 2)}
    s = struct("bridge_weir", "A plank bridge and the weirs", 4, 3, SEC,
               walk=["....", "XPX.", "XPX."], names=names,
               notes="Over borrowed turquoise water. The plank bridge on posts: `bridge_W` `bridge` "
                     "`bridge_E` east-west, `bridge_N` `bridge_V` `bridge_S` north-south (all "
                     "walkable). The weirs: a low sill of pink stone across the river with water "
                     "spilling over it in foam (animated): `weir_W` `weir` `weir_E` (the sill's "
                     "bank ends are impassable, its middle is water) and `weir_low_*`, a lower, "
                     "broken one.")
    ground(s, "shallow")
    M = s.M
    frames = anim_layer(s, "surf", 3)
    allf = [M] + frames
    # horizontal bridge
    for cx, end in ((0, "W"), (1, None), (2, "E")):
        ox = cx * 16
        for y in range(3, 13):
            for x in range(16):
                if end == "W" and x < 2:
                    continue
                if end == "E" and x > 13:
                    continue
                c = "wd2" if y not in (3, 12) else ("wd3" if y == 3 else "wd0")
                if x % 4 == 0 and 3 < y < 12:
                    c = "wd1"
                if y == 11:
                    c = "wd1"
                M.px(ox + x, y, c)
        for px_ in ((2, 13) if end else (6,)):
            for y in range(12, 15):
                M.px(ox + px_, y, "wd0")
                M.px(ox + px_ + 1, y, "wd1")
        if end:
            # rope rails at the ends
            M.px(ox + (2 if end == "W" else 13), 2, "wd3")
            M.px(ox + (2 if end == "W" else 13), 1, "wd1")
    # vertical bridge
    for cy, end in ((0, "N"), (1, None), (2, "S")):
        ox, oy = 48, cy * 16
        for y in range(16):
            if end == "N" and y < 2:
                continue
            if end == "S" and y > 13:
                continue
            for x in range(3, 13):
                c = "wd2" if x not in (3, 12) else ("wd3" if x == 3 else "wd0")
                if y % 4 == 0 and 3 < x < 12:
                    c = "wd1"
                M.px(ox + x, oy + y, c)
        for y in range(16):
            if end != "N" or y > 2:
                pass
    # weirs: a sill across the river; foam spilling below it
    for row, (y0, broken) in ((1, (3, False)), (2, (5, True))):
        for cx, end in ((0, "W"), (1, None), (2, "E")):
            ox, oy = cx * 16, row * 16
            sub = K.Layer(M.w, M.h)
            for x in range(16):
                if broken and 5 <= x <= 9 and end is None:
                    continue
                top = y0 + (1 if (x // 5) % 2 else 0)
                for y in range(top, top + 4):
                    c = ("rm4", "rm3", "rm2", "rm1")[y - top]
                    if end == "W" and x < 4:
                        c = grass_px(ox + x, oy + y) if y - top < 2 else c
                    for L in allf:
                        L.px(ox + x, oy + y, c)
                    sub.px(ox + x, oy + y, "rm1")
                if end in ("W", "E"):
                    edge_land = x < 5 if end == "W" else x > 10
                    if edge_land:
                        for y in range(16):
                            if y < top or y >= top + 4:
                                c = grass_px(ox + x, oy + y)
                                if (end == "W" and x == 4) or (end == "E" and x == 11):
                                    c = "rm2"
                                for L in allf:
                                    L.px(ox + x, oy + y, c)
            # spill: white water just below the sill
            for f, L in enumerate(allf):
                for x in range(16):
                    if end == "W" and x < 5 or end == "E" and x > 10:
                        continue
                    top = y0 + (1 if (x // 5) % 2 else 0) + 4
                    for k in range(5 + f):
                        y = top + k
                        if y < 16:
                            if k < 2:
                                L.px(ox + x, oy + y, "w0")
                            elif bubbles(ox + x, oy + y, f):
                                L.px(ox + x, oy + y, "w0" if k < 4 else "mw2")
    K.settle(s, "surf", [(x, y) for x in range(3) for y in (1, 2)])
    return s


# --------------------------------------------------------------------------
# The water-mill
# --------------------------------------------------------------------------

def wheel_frame(L, ox, oy, phase, broken=False):
    """A paddle wheel, 32 x 32, spokes rotated by `phase` (radians)."""
    cx_, cy_ = ox + 15.5, oy + 15.5
    R = 13.0
    for y in range(oy, oy + 32):
        for x in range(ox, ox + 32):
            d = math.hypot(x - cx_, y - cy_)
            if R - 2 <= d <= R:
                L.px(x, y, "wd1" if d > R - 1 else "wd2")
    for k in range(8):
        a = phase + k * math.pi / 4
        if broken and k in (2, 5):
            continue
        for t in np.linspace(2, R - 1, 24):
            L.px(int(round(cx_ + t * math.cos(a))), int(round(cy_ + t * math.sin(a))), "wd2")
        # a paddle at the rim
        for t in np.linspace(R - 1, R + 2.5, 6):
            for w in (-1, 0, 1):
                px_ = cx_ + t * math.cos(a) - w * math.sin(a)
                py_ = cy_ + t * math.sin(a) + w * math.cos(a)
                L.px(int(round(px_)), int(round(py_)), "wd3" if w < 0 else "wd1")
    put(L, int(cx_) - 2, int(cy_) - 2, [".kk.", "k33k", "k33k", ".kk."], {"k": "wd0", "3": "wd3"})


def mill():
    s = struct("mill", "The water-mill", 5, 5, SEC,
               walk=["XXXXX", "XXXXX", "XDXPP", "...XX", "...PP"],
               names={"house": (0, 0), "door": (1, 2), "wheel": (3, 1), "wheel_still": (3, 3)},
               notes="Myles's mill: a whitewashed mill house under a terracotta roof (3 x 3), its "
                     "door at (1, 2), and a paddle wheel (2 x 2 at (3, 1)) on the river beside it, "
                     "turning (the `wheel` animation) in borrowed turquoise water. The idle mills "
                     "of the ravine use the same house with `wheel_still` (2 x 2 at (3, 3)), its "
                     "wheel stopped and missing paddles. The house and wheels are impassable; "
                     "the water at a wheel's foot is `MB_POND_WATER`.")
    s.behaviors[(1, 2)] = "MB_NON_ANIMATED_DOOR"
    ground(s, "shallow", [(3, 1), (4, 1), (3, 2), (4, 2), (3, 3), (4, 3), (3, 4), (4, 4)])
    ground(s, "grass", [(3, 0), (4, 0), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4)])
    B, M = s.B, s.M
    # the house: terracotta roof (row 0), white walls (rows 1-2), door
    for y in range(48):
        for x in range(48):
            if y < 14:
                c = ("tc2", "tc2", "tc1", "tc1")[x % 4] if y % 4 != 3 else "tc1"
                if y == 0:
                    c = "tc1"
                if y == 13:
                    c = "cw3"
            else:
                c = "w0" if (x * 3 + y) % 23 else "cw1"
                if y in (14, 15):
                    c = "cw2"
                if y >= 45:
                    c = ("cw1", "cw2", "cw3")[y - 45]
            if x == 0 or x == 47:
                c = "cw3" if y >= 14 else "tc1"
            elif x >= 45 and y >= 14:
                c = "cw2"
            B.px(x, y, c)
    # the door, a sack beside it, a window
    for y in range(33, 47):
        for x in range(20, 29):
            c = "b1" if x not in (20, 28) and y != 33 else "ab0"
            if (x - 21) % 3 == 2 and y > 34:
                c = "ab0"
            if y == 40 and x == 26:
                c = "ink"
            B.px(x, y, c)
    put(B, 6, 20, ["bb.kkkk.bb", "bAbkkkkbAb", "bAbkkkkbAb", "bb.cccc.bb"],
        {"b": "ab0", "A": "b1", "k": "ink", "c": "cw2"})
    put(B, 33, 37, [".ww.", "wwww", "wwcw", "wwww", ".cc."], {"w": "w0", "c": "cw2"})
    # the wheel turning (4 frames) and still
    for y in range(16, 48):
        for x in range(48, 80):
            pass
    fr = anim_layer(s, "wheel", 4)
    allw = [M] + fr
    for i, L in enumerate(allw):
        wheel_frame(L, 48, 16, phase=i * math.pi / 16)
        # the race: white water churning under the wheel
        for x in range(48, 80):
            for y in range(40, 47):
                if bubbles(x, y, i % 3) and (x + y + i) % 2:
                    L.px(x, y, "w0")
    wheel_frame(M, 48, 48, phase=0.31, broken=True)
    for (mx, my_) in ((52, 52), (70, 58), (60, 74)):
        put(M, mx, my_, ["gg", "g."], {"g": "kr2"})
    K.settle(s, "wheel", [(3, 1), (4, 1), (3, 2), (4, 2)])
    # a stone axle-bearing on the house side
    return s


# --------------------------------------------------------------------------
# The Minoan vault door, and the rock stair down to the caves
# --------------------------------------------------------------------------

def vault_cave():
    s = struct("vault_cave", "The Minoan vault door, the cave stair", 3, 2, SEC,
               walk=["XXX", "XDD"], names={"vault_TL": (0, 0), "vault_TR": (1, 0),
                                         "vault_BL": (0, 1), "vault_door": (1, 1),
                                         "cave_top": (2, 0), "cave_stair": (2, 1)},
               notes="Set into the pink cliff face. `vault_*` (2 x 2 at its top-left): the door cut "
                     "into the cliff behind the Neraida's upper pool, no handle, only a hollow "
                     "shaped like a double axe, and round its frame old Minoan paint flaking: blue "
                     "dolphins, red bulls. Its bottom-right cell (1, 1) is the door "
                     "(`MB_NON_ANIMATED_DOOR`; the script opens it with the Labrys). `cave_top` "
                     "over `cave_stair`: a rough arch in the pink rock and a rock stair going down "
                     "into the dark, the spring's way down to Echo's caves (the stair is the door).")
    B = s.B
    # vault: plaster frame with paint, a grey stone slab, the axe hollow
    for y in range(32):
        for x in range(32):
            frame = x < 6 or x > 25 or y < 5
            if frame:
                c = "pl"
                k = K.h(x, y, 7)
                if k % 9 == 0:
                    c = "cw2"            # flaked to the stone
                if x in (0, 31) or y == 0:
                    c = "bz1"
                B.px(x, y, c)
            else:
                c = "cw2" if (x + y) % 7 else "cw3"
                if x in (6, 25) or y == 5:
                    c = "cw3"
                B.px(x, y, c)
    # dolphins (blue) up the left jamb, bulls (red) up the right, a band over the lintel
    for (dx, dy) in ((1, 7), (1, 16), (1, 25)):
        put(B, dx, dy, [".bb..", "bbbbb", "..b.b"], {"b": "b1"})
    for (bx, by) in ((26, 8), (26, 18)):
        put(B, bx, by, ["r..r", "rrrr", "rrr.", "r.r."], {"r": "mr"})
    for x in range(2, 30, 4):
        put(B, x, 1, ["bb", "rr"], {"b": "b1", "r": "mr"})
    # the double-axe hollow in the slab
    put(B, 10, 12, [
        "kk......kk",
        "kkk.kk.kkk",
        "kkkkkkkkkk",
        "kkk.kk.kkk",
        "kk..kk..kk",
        "....kk....",
        "....kk....",
        "....kk....",
        "....kk....",
    ], {"k": "ink"})
    for x in range(6, 26):
        B.px(x, 31, "bz0")
    # the cave arch in the pink rock
    for y in range(32):
        for x in range(16):
            X, Y = 32 + x, y
            c = stone_px(X, Y)
            dx = abs(x - 7.5)
            inside = (y >= 6 and dx < 5.5 - max(0, 9 - y) * 0.45) or y >= 16 and dx < 5.5
            if inside:
                c = "cv0"
                if y >= 18:
                    step = (y - 18) // 4
                    yy = (y - 18) % 4
                    if dx < 5 - step * 0.3:
                        c = ("rm2", "rm1", "rm0", "cv0")[yy] if step < 3 else "cv0"
            elif dx < 6.8 - max(0, 9 - y) * 0.45 and y >= 5:
                c = "rm0"
            B.px(X, Y, c)
    s.behaviors = {(1, 1): "MB_NON_ANIMATED_DOOR", (2, 1): "MB_NON_ANIMATED_DOOR"}
    return s


def naiad_altar():
    s = struct("naiad_altar", "The Naiads' altar", 2, 1, SEC, walk=["XX"],
               names={"horn": (0, 0), "empty": (1, 0)},
               notes="The Naiads' shrine at the plunge pool (beat III-1H): a mossy marble altar with "
                     "the Horn of Achelous laid on it (`horn`), and the same once the horn is taken "
                     "(`empty`: swap it in when `FLAG_ICHOR_GOT_HORN_OF_ACHELOUS` is set). On "
                     "borrowed grass; impassable, read it.")
    ground(s, "grass")
    M = s.M
    for ox in (0, 16):
        put(M, ox + 1, 3, [
            "..kkkkkkkkkk..",
            ".k5555555555k.",
            "k555555555555k",
            "k444444444444k",
            "k4m4444444m43k",
            "k443333333333k",
            "k444444444433k",
            "k4m444444m4433",
            "k333333333333k",
            ".kkkkkkkkkkkk.",
            "..g.gggg.g.g..",
        ], {"k": "rm2", "5": "w0", "4": "rm5", "3": "rm4", "m": "my2", "g": "g1"})
    # the horn: a curving ivory horn spilling grain and fruit
    put(M, 3, 0, [
        "..........kk",
        "......kkkk5k",
        "...kkk55554k",
        ".kk55444kk..",
        "k5444kk.....",
        "krrk........",
    ], {"k": "rm2", "5": "w0", "4": "rm5", "r": "rm3"})
    return s


def build():
    return [falls(), kerb(), spring_pool(), bridge_weir(), mill(), vault_cave(), naiad_altar()]
