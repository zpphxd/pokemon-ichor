"""Taygetos and the Skiritis: the dark mountain wall behind Lakonia, the rock
walls of the hill routes, Cape Malea's sea cliffs, scree and boulders.

The rock is a blue-violet limestone gone dark with weather, cut by vertical
fissures, lit from the top left; black pines cling to its ledges and pale
scree fans out at its foot onto the grass. Everything is in the `mount` group.
"""
from __future__ import annotations

import math

import numpy as np

import lakonia_lib as L
from lakonia_lib import ground, put, struct

SEC = "mount"

# --------------------------------------------------------------------------
# Rock textures
# --------------------------------------------------------------------------


def _facets(X, Y, period=32, sx=1.0, sy=1.0, seed=0):
    """Nearest jittered point on a periodic grid: (id, dx, dy, d1, d2)."""
    n = 4
    cl = period / n
    x, y = (X % period), (Y % period)
    best = []
    gx, gy = int(x // cl), int(y // cl)
    for j in range(gy - 1, gy + 2):
        for i in range(gx - 1, gx + 2):
            hh = L.h(i % n, j % n, seed)
            px_ = (i + 0.2 + (hh % 7) / 10) * cl
            py_ = (j + 0.2 + ((hh // 7) % 7) / 10) * cl
            d = math.hypot((x - px_) * sx, (y - py_) * sy)
            best.append((d, (i % n) + 4 * (j % n), x - px_, y - py_))
    best.sort()
    d1, fid, dx, dy = best[0]
    return fid, dx, dy, d1, best[1][0]


RIDGES = [(0, 6), (6, 4), (10, 7), (17, 5), (22, 6), (28, 4)]


def face_px(X, Y, seed=0):
    """The cliff face: vertical ridges of rock (32 px periodic across, 16
    down), each lit on its left, shaded on its right, a dark crevice between,
    broken into blocks by sloping joints."""
    x = (X + seed * 13) % 32
    for i, (x0, w) in enumerate(RIDGES):
        if x0 <= x < x0 + w:
            break
    lx = x - x0
    off = (i * 7 + seed * 3) % 16
    slope = 1 if i % 2 else -1
    brk = (Y + off - (lx * slope) // 2) % 16
    if lx == w - 1:
        return "ty0"
    if brk == 0:
        return "ty0"
    if brk == 1:
        return "ty3" if lx < w - 2 else "ty2"
    if lx == 0:
        return "ty3" if brk % 5 else "ty2"
    if lx == 1:
        return "ty2"
    if lx >= w - 2:
        return "ty1" if brk % 6 else "ty0"
    k = L.hp(X, Y, seed + 7, 32)
    if k % 13 == 0:
        return "ty0"
    return "ty2" if (lx < w // 2 and k % 3) else "ty1"


def pn(X, Y, period, seed):
    """Smooth periodic noise in about [-1, 1]."""
    t = 2 * math.pi / period
    v = 0.0
    for i, (a, b) in enumerate(((1, 0), (0, 1), (1, 1), (2, -1), (1, 2), (3, 1))):
        v += math.sin(t * (a * X + b * Y) + seed * 1.7 + i * 2.1) / (1 + 0.35 * i)
    return v / 2.6


SCRUB = [(6, 7, 4.2, 3.4), (22, 4, 3.2, 2.6), (14, 21, 4.8, 3.8), (28, 23, 3.0, 2.6),
         (3, 27, 2.6, 2.2)]


def _scrub(X, Y):
    """(depth, lit) of the nearest pine-scrub clump, 32 px periodic."""
    x, y = X % 32, Y % 32
    for (cx, cy, rx, ry) in SCRUB:
        for ox in (-32, 0, 32):
            for oy in (-32, 0, 32):
                dx, dy = (x - cx - ox) / rx, (y - cy - oy) / ry
                a = math.atan2(dy, dx)
                r = math.hypot(dx, dy) - 0.12 * math.sin(a * 5 + cx)
                if r < 1:
                    return r, -(dx + dy)
    return None


def mass_px(X, Y, seed=0):
    """The massif seen from above: stepped rock plates lit top-left, with
    clumps of dark pine scrub; 32 px periodic."""
    sc = _scrub(X, Y)
    if sc is not None:
        r, lit = sc
        if r > 0.82 and lit < 0.3:
            return "ty0"
        k = L.hp(X, Y, 5, 32)
        if lit > 0.6:
            return "c3" if k % 3 == 0 else "c2"
        if lit > -0.2:
            return "c2" if k % 3 else "c1"
        return "c1"
    sh = _scrub(X - 2, Y - 2)
    if sh is not None and sh[0] < 0.95:
        return "ty0" if (X + Y) % 2 else "ty1"
    v = pn(X, Y, 32, seed + 5)
    lv = math.floor((v + 1) * 2.5)
    lv_ul = math.floor((pn(X - 1, Y - 1, 32, seed + 5) + 1) * 2.5)
    lv_dr = math.floor((pn(X + 1, Y + 1, 32, seed + 5) + 1) * 2.5)
    if lv > lv_ul:
        return "ty3" if lv >= 3 else "ty2"
    if lv < lv_ul or lv > lv_dr + 0:
        if lv_dr < lv:
            return "ty0"
    if lv_dr < lv:
        return "ty0"
    if lv >= 4:
        return "ty3" if L.hp(X, Y, 9, 32) % 4 == 0 else "ty2"
    return ("ty1", "ty1", "ty2", "ty1", "ty2")[lv % 5] if L.hp(X, Y, 3, 32) % 7 else "ty0"


def scree_px(X, Y):
    """Loose pale scree: pebbles with dark undersides."""
    x, y = X % 16, Y % 16
    k = L.hp(x, y, 41)
    if (x * 5 + y * 7) % 11 < 2:
        return "ty2"
    if k % 7 == 0:
        return "ty5"
    return "ty4" if (x + y * 3) % 5 else "ty3"


def pine(Lr, ox, oy, w=12, hgt=14, seed=0, lean=0.0):
    """A black pine clinging to rock: three tiers of dark needles, lit on the
    top left, with a dark outline and a crooked trunk."""
    sub = L.Layer(Lr.w, Lr.h)
    m = np.zeros((Lr.h, Lr.w), bool)
    tiers = 3
    th = hgt / tiers
    for t in range(tiers):
        ty_ = oy + t * th
        half = (t + 1.6) * w / (2 * (tiers + 0.6))
        cxp = ox + w / 2 + lean * (tiers - t)
        for y in range(int(ty_), int(ty_ + th + 2)):
            for x in range(int(cxp - half - 2), int(cxp + half + 3)):
                f = (y - ty_) / (th + 1)
                if abs(x - cxp) <= half * (0.35 + 0.75 * f) + 0.7 * math.sin(x * 1.9 + y + seed) \
                        and 0 <= y < Lr.h and 0 <= x < Lr.w:
                    m[y, x] = True
    for y in range(int(oy + hgt), int(oy + hgt + 3)):
        Lr.px(int(ox + w / 2), y, "ty1")
        Lr.px(int(ox + w / 2) + 1, y, "ty0")
    ys, xs = np.nonzero(m)
    for y, x in zip(ys, xs):
        up = y == 0 or not m[y - 1, x]
        left = x == 0 or not m[y, x - 1]
        down = y + 1 >= Lr.h or not m[y + 1, x]
        k = L.h(int(x), int(y), seed)
        c = "c1"
        if up or (left and k % 2):
            c = "c3" if k % 3 else "c2"
        elif not down and k % 4 == 0:
            c = "c2"
        sub.px(int(x), int(y), c)
    sub.outline("ty0")
    for y, x in zip(*np.nonzero(sub.a[..., 3] > 0)):
        Lr.px(int(x), int(y), sub.get(int(x), int(y)))


# --------------------------------------------------------------------------
# The wall kit
# --------------------------------------------------------------------------

def taygetos():
    names = {
        "mass_00": (0, 0), "mass_10": (1, 0), "mass_01": (0, 1), "mass_11": (1, 1),
        "lip_L": (2, 0), "lip": (3, 0), "lip_b": (4, 0), "lip_R": (5, 0),
        "face_L": (2, 1), "face": (3, 1), "face_b": (4, 1), "face_R": (5, 1),
        "foot_L": (2, 2), "foot": (3, 2), "foot_b": (4, 2), "foot_R": (5, 2),
        "side_E": (6, 0), "side_W": (7, 0), "side_E_foot": (6, 1), "side_W_foot": (7, 1),
        "back_NW": (6, 2), "back": (7, 2), "back_NE": (0, 2), "pine_face": (1, 2),
        "in_E": (0, 3), "in_W": (1, 3), "mass_pine": (2, 3), "gully": (3, 3), "gully_foot": (4, 3),
        "boulder": (5, 3), "boulders": (6, 3), "scree": (7, 3),
    }
    walk = ["XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "XXXXXXX."]
    s = struct("taygetos", "Taygetos: the dark wall", 8, 4, SEC, walk=walk, names=names,
               notes="The mountain wall behind Lakonia, and the rock walls of the hill routes. "
                     "Fill the mountain's body with `mass_00` `mass_10` / `mass_01` `mass_11`, "
                     "a 2 x 2 block that tiles (put `mass_XY` at x % 2, y % 2; `mass_pine` breaks "
                     "it up). A south-facing wall is `lip` over `face` over `foot`, the foot "
                     "standing on grass (`_b` are variants to break a long run; `_L` `_R` end "
                     "one); `pine_face` is a face with a black pine on a ledge. `side_E` / "
                     "`side_W` run north-south down the mountain's east or west flank (with "
                     "`side_E_foot` / `side_W_foot` where a flank meets a south face's foot "
                     "row); `back` and `back_NW` `back_NE` finish a free-standing rock's north "
                     "edge onto grass. `in_E` `in_W` turn a south face's lip into a flank. "
                     "`gully` and `gully_foot` are a dry watercourse down the face. Loose "
                     "pieces on grass: `boulder`, `boulders` (impassable), `scree` (walkable). "
                     "All impassable except `scree`.")
    B, M = s.B, s.M
    # the massif's body, 32 px periodic
    for (cx, cy) in ((0, 0), (1, 0), (0, 1), (1, 1), (2, 3)):
        for y in range(16):
            for x in range(16):
                B.px(cx * 16 + x, cy * 16 + y, mass_px(cx * 16 + x, cy * 16 + y))
    pine(B, 2 * 16 + 2, 3 * 16 + 1, w=12, hgt=12, seed=3)
    # the lip: massif above, a lit rim, then the face's first pixels
    for i, cx in enumerate((2, 3, 4, 5)):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, y
                rim = 9 + round(1.2 * math.sin(2 * math.pi * X / 32) + 0.6 * math.sin(2 * math.pi * X / 8))
                if y < rim:
                    c = mass_px(X, Y + 16, seed=0)
                elif y == rim:
                    c = "ty4" if X % 5 else "ty3"
                elif y == rim + 1:
                    c = "ty3"
                else:
                    c = face_px(X, Y, seed=0)
                    if y == rim + 2:
                        c = "ty0" if X % 3 == 0 else "ty1"
                B.px(X, Y, c)
    # the face
    for i, cx in enumerate((2, 3, 4, 5)):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, 16 + y
                B.px(X, Y, face_px(X, Y, seed=0))
    # foot: face down to scree, scree to grass (borrowed)
    ground(s, "grass", [(2, 2), (3, 2), (4, 2), (5, 2), (6, 1), (7, 1), (6, 2), (7, 2), (0, 2),
                        (5, 3), (6, 3), (7, 3), (4, 3)])
    for i, cx in enumerate((2, 3, 4, 5)):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, 32 + y
                base = 7 + round(1.4 * math.sin(2 * math.pi * X / 32 + 1) + 0.7 * math.sin(2 * math.pi * X / 8))
                fan = base + 4 + round(1.5 * math.sin(2 * math.pi * X / 16 + 2))
                if y < base:
                    M.px(X, Y, face_px(X, Y, seed=0))
                elif y == base:
                    M.px(X, Y, "ty0")
                elif y < fan:
                    M.px(X, Y, scree_px(X, Y))
                elif y == fan and (X + i) % 2 == 0:
                    M.px(X, Y, "gd")
                elif y == fan + 1 and X % 3 == 0:
                    M.px(X, Y, "gd")
    # end pieces: round the run's ends off (L: rock only east of a slope line)
    for cx, side in ((2, -1), (5, 1)):
        for cy in (0, 1, 2):
            layer = B if cy < 2 else M
            for y in range(16):
                for x in range(16):
                    X, Y = cx * 16 + x, cy * 16 + y
                    edge = 3 + cy * 1.5 + y * 0.12
                    inside = (x >= edge) if side < 0 else (x <= 15 - edge)
                    near = (abs(x - edge) < 1.0) if side < 0 else (abs((15 - x) - edge) < 1.0)
                    if cy < 2 and not inside:
                        # beyond the end: the massif continues above the lip, grass below
                        if cy == 0 and y < 9:
                            continue
                        layer.px(X, Y, L.grass_px(X, Y))
                    elif near and cy < 2:
                        layer.px(X, Y, "ty0" if side > 0 else "ty3")
                    elif cy == 2 and not inside:
                        layer.px(X, Y, None)
    # flanks: a strip of face down the mountain's east / west side
    for cx, side in ((6, 1), (7, -1)):
        for cy in (0,):
            for y in range(16):
                for x in range(16):
                    X, Y = cx * 16 + x, cy * 16 + y
                    lx = x if side > 0 else 15 - x       # 0 at the mountain side
                    wob = round(0.8 * math.sin(2 * math.pi * Y / 16))
                    if lx < 6 + wob:
                        B.px(X, Y, mass_px(X, Y))
                    elif lx < 7 + wob:
                        B.px(X, Y, "ty4" if side < 0 else "ty3")
                    elif lx < 11 + wob:
                        B.px(X, Y, face_px(X + 5, Y))
                    elif lx < 12 + wob:
                        B.px(X, Y, "ty0")
                    elif lx < 13 + wob:
                        B.px(X, Y, scree_px(X, Y))
                    else:
                        B.px(X, Y, L.grass_px(X, Y))
        # the flank's foot: the strip ending in scree on grass (borrowed)
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, 16 + y
                lx = x if side > 0 else 15 - x
                wob = round(0.8 * math.sin(2 * math.pi * Y / 16))
                endy = 9 + lx * 0.3
                if y < endy:
                    if lx < 6 + wob:
                        M.px(X, Y, mass_px(X, Y))
                    elif lx < 11 + wob:
                        M.px(X, Y, face_px(X + 5, Y))
                    elif lx < 12 + wob:
                        M.px(X, Y, "ty0")
                    elif lx < 13 + wob:
                        M.px(X, Y, scree_px(X, Y))
                elif y < endy + 1:
                    M.px(X, Y, "ty0" if lx < 12 else None)
                elif y < endy + 4 and lx < 12 + (y - endy) * 0.6:
                    M.px(X, Y, scree_px(X, Y))
    # back edges: the rock's north rim onto grass (grass north, rock south)
    for cx, kind in ((6, "NW"), (7, "N"), (0, "NE")):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, 32 + y
                rim = 6 + round(0.9 * math.sin(2 * math.pi * X / 16))
                if kind == "NW":
                    d = min(y - rim, x - 5)
                elif kind == "NE":
                    d = min(y - rim, 10 - x)
                else:
                    d = y - rim
                if d > 1:
                    M.px(X, Y, mass_px(X, Y))
                elif d > 0:
                    M.px(X, Y, "ty4")
                elif d > -1 and (X + Y) % 2:
                    M.px(X, Y, "gd")
    # a pine on a ledge of the face
    for y in range(16):
        for x in range(16):
            B.px(16 + x, 32 + y, face_px(16 + x, 32 + y))
    s.ground.pop((1, 2), None)
    for x in range(16 + 1, 16 + 15):
        B.px(x, 32 + 13, "ty3" if x % 4 else "ty4")
        B.px(x, 32 + 14, "ty0")
    pine(B, 16 + 1, 32 + 1, w=14, hgt=12, seed=7, lean=0.4)
    B.rect(32, 32, 16, 16, None)          # keep the pine inside its cell
    # inner corners: a south face's lip turning into a flank (face to the west/east)
    for cx, side in ((0, 1), (1, -1)):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, 48 + y
                lx = x if side > 0 else 15 - x
                rim = 9 + round(1.2 * math.sin(2 * math.pi * X / 32))
                if y < rim or lx < 6:
                    c = mass_px(X, Y)
                elif y == rim or lx == 6:
                    c = "ty4"
                else:
                    c = face_px(X, Y)
                B.px(X, Y, c)
    # a gully: a dry watercourse cut into the face, its bed of fallen stone
    for cx, foot in ((3, False), (4, True)):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, 48 + y
                g = x - 7.5 - 1.2 * math.sin(Y / 3.0)
                inbed = abs(g) < 3.0
                if foot and y > 8 and abs(g) > 2.5 + (y - 8) * 0.7:
                    continue
                if inbed:
                    k = L.hp(X, Y, 61)
                    c = "ty1" if (X * 2 + Y * 5) % 7 < 3 else ("ty2" if k % 3 else "ty3")
                    if g < -2.0:
                        c = "ty0"
                    elif g > 2.0:
                        c = "ty2"
                elif abs(g) < 4.0:
                    c = "ty3" if g < 0 else "ty0"
                else:
                    c = face_px(X, Y)
                if foot and y > 8:
                    c = scree_px(X, Y) if inbed or abs(g) < 6 else c
                (M if foot else B).px(X, Y, c)
    # boulders and scree on grass
    for (cx, pts) in ((5, [(8, 9, 5.5, 4.5)]), (6, [(5, 10, 4.0, 3.2), (11, 6, 3.5, 2.8),
                                                   (11, 12, 2.6, 2.2)])):
        for (bx, by, rx, ry) in pts:
            for y in range(16):
                for x in range(16):
                    X, Y = cx * 16 + x, 48 + y
                    d = math.hypot((x - bx) / rx, (y - by) / ry)
                    if d < 1:
                        lit = -(x - bx) / rx - (y - by) / ry
                        c = "ty4" if lit > 0.7 else ("ty3" if lit > -0.1 else "ty2")
                        if d > 0.85:
                            c = "ty1" if lit < 0.5 else "ty3"
                        M.px(X, Y, c)
                    elif d < 1.25 and y > by and M.get(X, Y) is None:
                        M.px(X, Y, "gd" if (X + Y) % 2 else "g1")
    # scree: a loose fan of pebbles on the grass (walkable)
    for y in range(16):
        for x in range(16):
            X, Y = 7 * 16 + x, 48 + y
            d = math.hypot((x - 8) / 7.0, (y - 8.5) / 5.5) + 0.15 * math.sin(x * 1.3 + y)
            if d < 1 and (L.hp(x, y, 51) % 3 or d < 0.6):
                M.px(X, Y, scree_px(X, Y))
            elif d < 1.15 and (x + y) % 3 == 0:
                M.px(X, Y, "ty3")
    return s


def build():
    return [taygetos()]
