"""Gytheion and the strait off Malea: the quay's purple-stained steps and
stains, murex shell heaps, the dye-works shed and its steaming lead vats, the
stall under its purple awning, racks of drying nets, the causeway to Kranai and
its whitewashed shrine, the little theater cut into the hill and its
stage-building (the Asclepeion), Cape Malea's sea cliffs, the Malea current,
and the drowned town off Elaphonisos.

Gytheion is the color only kings can afford, and nobody here can afford it:
purple in every crack of the quay, gray murex heaps like snow.
"""
from __future__ import annotations

import math

import numpy as np

import lakonia_lib as L
from lakonia_lib import ground, put, struct

SEC = "harbor"
hp, mx = L.hp, L.mx


def stain(M, X, Y, x, y, strength=1.0):
    """A purple stain on limestone: the darker the deeper."""
    k = hp(x, y, 141)
    if k % 5 == 0 and strength < 1.0:
        return
    M.px(X, Y, "pu2" if k % 3 else ("pu1" if strength > 0.7 else "pu3"))


# --------------------------------------------------------------------------
# The quay: purple-stained steps, stains, shell heaps
# --------------------------------------------------------------------------

def quayside():
    names = {"steps_S": (0, 0), "steps_E": (1, 0), "steps_W": (2, 0), "stain": (3, 0),
             "stain_b": (4, 0), "drain": (5, 0), "heap_TL": (0, 1), "heap_TR": (1, 1),
             "heap_BL": (0, 2), "heap_BR": (1, 2), "shells": (2, 1), "shells_sand": (3, 1),
             "heap_small": (4, 1), "pebbles": (2, 2), "pebbles_b": (3, 2), "mooring": (5, 1),
             "bucket": (4, 2), "basket": (5, 2), "steps_SL": (6, 0), "steps_SR": (6, 1),
             "amphorae": (6, 2)}
    s = struct("quayside", "The purple quay: steps, stains, murex heaps", 7, 3, SEC,
               walk=["...X...", "XX.XXX.", "XX..XXX"], names=names,
               notes="Gytheion's quay is aethos's limestone path with Skandeia's quay edges "
                     "(the `quay` kit); these finish it in purple. `steps_S` `steps_E` "
                     "`steps_W`: steps down into the sea (borrowed), stained purple where the "
                     "dyers rinse their arms (walkable); `steps_SL` `steps_SR` are a stair two "
                     "cells wide. `amphorae`: jars of brine for the shells (impassable). On borrowed path: `stain` `stain_b` "
                     "(walkable), `drain` (a gutter running purple to the sea, impassable), "
                     "`mooring` (a bollard, impassable), `bucket` (the fisherman's bronze "
                     "helmet, bailing water; impassable), `basket` (a basket of live murex). "
                     "Murex shell heaps behind the dye-works, gray like snow: `heap_*` (2 x 2) "
                     "and `heap_small` (impassable); `shells` on path and `shells_sand` on "
                     "sand (walkable, crushed shell). On the shingle beach (borrowed sand): "
                     "`pebbles` `pebbles_b`, stained purple (walkable).")
    M = s.M
    ground(s, "sea", [(0, 0), (1, 0), (2, 0), (6, 0), (6, 1)])
    ground(s, "path", [(6, 2)])
    ground(s, "path", [(3, 0), (4, 0), (5, 0), (2, 1), (4, 1), (5, 1), (4, 2), (5, 2),
                       (0, 1), (1, 1), (0, 2), (1, 2)])
    ground(s, "sand", [(3, 1), (2, 2), (3, 2)])
    # steps down into the sea: south, east and west. The quay's wall runs on
    # either side; between, three steps go down, wetter and more purple
    # toward the water, which laps the last one.
    for nm in ("steps_S", "steps_E", "steps_W", "steps_SL", "steps_SR"):
        cx, cy = names[nm]
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, cy * 16 + y
                if nm in ("steps_S", "steps_SL", "steps_SR"):
                    t_, u = y, x
                elif nm == "steps_E":
                    t_, u = x, y
                else:
                    t_, u = 15 - x, y
                side = (u <= 1 and nm != "steps_SR") or (u >= 14 and nm != "steps_SL")
                if side:
                    # the quay wall's coping and face either side of the stair
                    if t_ < 6:
                        c = "p3" if t_ == 5 else "p2"
                    elif t_ < 7:
                        c = "p3"
                    elif t_ < 13:
                        c = "p1" if (u + t_) % 4 else "kr1"
                        if t_ == 12:
                            c = "kr0"
                    else:
                        continue
                    if u in (1, 14):
                        c = "kr0" if t_ >= 6 else c
                    M.px(X, Y, c)
                    continue
                if t_ >= 13:
                    if t_ == 13 and u % 2 == 0:
                        M.px(X, Y, "w0")
                    continue
                st = min(2, t_ // 4)
                ph = t_ % 4
                c = ("p3", "p2", "p1", "kr0")[ph]
                if st == 2:
                    c = ("p2", "p1", "kr1", "kr0")[ph]
                # the dye pooled on each tread, broader and darker lower down
                wide = 2.5 + st * 2.0 + 0.8 * math.sin(u * 1.7 + st)
                mid = {"steps_SL": 15.5, "steps_SR": -0.5}.get(nm, 7.5)
                if nm in ("steps_SL", "steps_SR"):
                    wide += 3
                if abs(u - mid) < wide and ph in (0, 1):
                    c = ("pu4", "pu3", "pu2")[st] if ph == 0 else ("pu3", "pu2", "pu1")[st]
                elif abs(u - mid) < wide - 1 and ph == 2:
                    c = "pu1" if st else "pu2"
                M.px(X, Y, c)
    # stains on the paving
    for nm, seed in (("stain", 0), ("stain_b", 7)):
        cx, cy = names[nm]
        for y in range(16):
            for x in range(16):
                d = math.hypot((x - 7.5) / (6.5 if seed else 5.5), (y - 8) / (4.5 if seed else 5.5))
                d += 0.25 * math.sin(x * 1.3 + y * 0.7 + seed)
                if d < 1:
                    stain(M, cx * 16 + x, cy * 16 + y, x, y, 1.0 - d)
                elif d < 1.3 and hp(x, y, 3 + seed) % 3 == 0:
                    M.px(cx * 16 + x, cy * 16 + y, "pu4")
    cx, cy = names["drain"]
    for y in range(16):
        for x in range(5, 11):
            c = "kr0" if x in (5, 10) else ("pu1" if (y + x) % 3 else "pu2")
            M.px(cx * 16 + x, y, c)
    # murex heaps: spiky gray shells, white where the sun catches them
    def shell_heap(ox, oy, w, h_, seed):
        m = np.zeros((h_, w), bool)
        for y in range(h_):
            for x in range(w):
                a = math.atan2(y - h_ * 0.6, x - w / 2)
                if math.hypot((x - w / 2 + 0.5) / (w / 2 - 1), (y - h_ * 0.62) / (h_ * 0.55)) \
                        < 1 + 0.08 * math.sin(a * 9 + seed):
                    m[y, x] = True
        for y in range(h_):
            for x in range(w):
                if not m[y, x]:
                    if y > 0 and m[y - 1, x] and (x + y) % 2 and y > h_ * 0.6:
                        M.px(ox + x, oy + y, "kr0")
                    continue
                k = hp(x % 16, y % 16, 161 + seed)
                up = y == 0 or not m[y - 1, x]
                lit = -(x - w / 2) / w - (y - h_ / 2) / h_
                c = "kr2" if lit > 0 else "kr1"
                if k % 4 == 0:
                    c = "kr3" if lit > -0.2 else "kr2"
                if k % 7 == 0:
                    c = "kr0"
                if k % 23 == 0:
                    c = "pu3"
                if up:
                    c = "kr3" if k % 2 else "w0"
                M.px(ox + x, oy + y, c)
    shell_heap(0, 16, 32, 32, 1)
    shell_heap(64, 16 + 3, 16, 13, 4)
    for nm in ("shells", "shells_sand"):
        cx, cy = names[nm]
        for (sx, sy) in ((2, 3), (9, 2), (5, 8), (12, 7), (3, 12), (10, 12), (7, 5)):
            put(M, cx * 16 + sx, cy * 16 + sy, ["32", "21"], {"3": "kr3", "2": "kr2", "1": "kr1"})
    for nm, seed in (("pebbles", 0), ("pebbles_b", 5)):
        cx, cy = names[nm]
        for y in range(16):
            for x in range(16):
                k = hp(x, y, 171 + seed)
                if k % 4 == 0:
                    M.px(cx * 16 + x, cy * 16 + y, "kr2" if k % 3 else "kr1")
                elif k % 9 == 1:
                    M.px(cx * 16 + x, cy * 16 + y, "pu3" if k % 2 else "pu2")
    # a bollard
    cx, cy = names["mooring"]
    put(M, cx * 16 + 4, cy * 16 + 3, [
        "..3333..",
        ".322221.",
        ".322221.",
        "..3221..",
        "..3221..",
        ".322221.",
        "32222221",
        "11111111",
        ".kkkkkk.",
    ], {"3": "kr2", "2": "kr1", "1": "kr0", "k": "p1"})
    # the helmet bucket: Kleon's closed bronze helmet, upturned, full of seawater
    # (on the top layer, in Kythera's timber-and-terracotta palette: old bronze)
    cx, cy = names["bucket"]
    put(s.T, cx * 16 + 3, cy * 16 + 4, [
        "..00000000..",
        ".0bbbbbbbb0.",
        "0bwbbbbbbbb0",
        "0bbbbbbbbbb0",
        "033333333330",
        "03223003232.",
        ".032200322..",
        "..03323302..",
        "...000000...",
        "....1111....",
    ], {"0": "wd0", "b": "b2", "w": "b1", "3": "wd3", "2": "tc2", "1": "wd1"})
    # amphorae of brine, leaning together
    cx, cy = names["amphorae"]
    for (ax, ay) in ((2, 2), (8, 1), (5, 5)):
        put(M, cx * 16 + ax, cy * 16 + ay, [
            ".11.",
            ".22.",
            "1221",
            "2332",
            "2332",
            "2222",
            "1221",
            ".22.",
            ".11.",
        ], {"1": "kr0", "2": "p1", "3": "p3"})
    # a basket of murex
    cx, cy = names["basket"]
    put(M, cx * 16 + 2, cy * 16 + 3, [
        "..3232323232..",
        ".323232323232.",
        "0111111111110.",
        "0p1p1p1p1p1p0",
        "01p1p1p1p1p10",
        "0p1p1p1p1p1p0",
        ".000000000000",
        "..p.p.p.p.p..",
    ], {"3": "kr3", "2": "kr2", "1": "p1", "p": "p2", "0": "kr0"})
    return s


# --------------------------------------------------------------------------
# The dye-works, its vats, the stall, the nets
# --------------------------------------------------------------------------

def dyeworks():
    names = {"roof_L": (0, 0), "roof": (1, 0), "roof_b": (2, 0), "roof_open": (3, 0),
             "roof_R": (4, 0), "wall_L": (0, 1), "skeins": (1, 1), "door": (2, 1),
             "open": (3, 1), "open_R": (4, 1)}
    s = struct("dyeworks", "The dye-works", 5, 2, SEC, walk=["XXXXX", "XXDXX"],
               names=names,
               notes="Porphyris's dye-works on the shore: a long rough-stone shed under a "
                     "clay-tile roof, its walls stained purple to the eaves, skeins of wool "
                     "drying on a pole by the door, and its east end open to the sea, the lead "
                     "vats glowing purple in the dark (`open`, `open_R`). `door` is "
                     "`MB_NON_ANIMATED_DOOR`. Impassable otherwise. The heaps of shell go "
                     "behind it.")
    B, T = s.B, s.T
    import lakonia_town as Tn
    W = 80
    Tn.tile_roof(B, 0, 0, W, rows=13)
    for x in range(W):
        for y, c in zip(range(13, 16), ("sn3", "sn2", "sn1")):
            B.px(x, y, c)
    for y in range(16):
        B.px(0, y, "sn1")
        B.px(W - 1, y, "sn1")
    # walls of rough stone with purple splashes (stains on the top layer)
    for y in range(16, 32):
        for x in range(W):
            c = L.stone_course_px(x % 16, y, 16, ramp=("sn3", "sn2", "sn2", "sn1"), course=4, brick=7)
            if y == 16:
                c = "sn1"
            if x in (0,):
                c = "sn1"
            B.px(x, y, c)
    for x in range(W - 32):
        for y in range(16, 32):
            yy = y - 16
            k = hp(x % 16, yy, 181)
            if yy > 6 and k % (3 + (15 - yy) // 3) == 0:
                T.px(x, y, "pu2" if k % 2 else "pu1")
            if yy > 12 and k % 2 == 0:
                T.px(x, y, "pu1")
    # the door
    put(B, 32 + 3, 17, [
        "1111111111",
        "1iiiiiiii1",
        "1i22i22ii1",
        "1i22i22ii1",
        "1i22i22ii1",
        "1i22i22ii1",
        "1i22i22ii1",
        "1i22i22ii1",
        "1i22i22ii1",
        "1i22i22ii1",
        "1i22i22ii1",
        "1iiiiiiii1",
        "3333333333",
        "1111111111",
    ], {"1": "ro1", "i": "ink", "2": "ro2", "3": "sn3"})
    # skeins on a pole: from pink to near-black (top layer: purple group)
    for x in range(16 + 1, 16 + 15):
        T.px(x, 18, "ink")
    for i, (sx, c1, c2) in enumerate(((2, "pu4", "pu3"), (5, "pu3", "pu2"), (8, "pu2", "pu1"),
                                       (11, "pu1", "pu0"))):
        for y in range(19, 28 + (i % 2)):
            T.px(16 + sx, y, c1)
            T.px(16 + sx + 1, y, c2 if y % 3 else c1)
    # the open end: dark shed, two vats glowing, a low wall
    for y in range(16, 32):
        for x in range(48, W):
            yy = y - 16
            c = "sn0" if yy < 12 else "sn1"
            if x == W - 1:
                c = "sn1"
            if x in (48, 49):
                c = "sn2" if x == 48 else "sn1"
            B.px(x, y, c)
    for vx in (52, 66):
        put(T, vx, 22, [
            ".0000000000.",
            "0322222222k0",
            "0kppppppppk0",
            "0kpqqpppppk0",
            "0kppppqqppk0",
            "0kkkkkkkkkk0",
            ".0kkkkkkkk0.",
            "..00000000..",
        ], {"0": "ink", "3": "kr3", "2": "kr2", "k": "kr0", "p": "pu1", "q": "pu2"})
    return s


def vats():
    names = {"vat": (0, 0), "vat_b": (1, 0), "skein_rack": (2, 0), "nets_L": (3, 0),
             "nets_R": (4, 0)}
    s = struct("vats", "Lead vats, a skein rack, nets drying", 5, 1, SEC, walk=["XXXXX"],
               names=names,
               notes="On borrowed path. `vat` `vat_b`: a great lead vat of purple steaming over "
                     "its fire (animated steam), outside the dye-works. `skein_rack`: dyed "
                     "wool drying on a frame. `nets_L` `nets_R`: nets hung to dry on poles, the "
                     "stall's racks and the fishers'. All impassable.")
    ground(s, "path")
    M, T = s.M, s.T
    for ox in (0, 16):
        put(M, ox + 1, 3, [
            ".00000000000.",
            "0322222222220",
            "0k3ppqpppp2k0",
            "0kpppppqqppk0",
            "0kppqqppppkk0",
            "0kkkkkkkkkkk0",
            "0kkkkkkkkkkk0",
            ".0kkkkkkkkk0.",
            "..k0000000k..",
            "..k.w.w.w.k..",
            "..kkkkkkkkk..",
            "...........",
        ], {"0": "ink", "3": "kr3", "2": "kr2", "k": "kr0", "p": "pu1", "q": "pu2",
            "w": "pu4"})
    frames = L.anim_layer(s, "steam", 3, layer="middle")
    puffs = [((4, 1), (9, 0)), ((5, 0), (8, 1)), ((3, 0), (10, 1))]
    for fi, F in enumerate([M] + frames):
        for ox in (0, 16):
            for (px_, py_) in puffs[(fi + ox // 16) % 3]:
                put(F, ox + px_, py_, [".w.", "www"], {"w": "w0" if fi % 2 else "kr3"})
    L.settle(s, "steam", [(0, 0), (1, 0)])
    # skein rack (purple group): a frame with hanks of wool
    put(M, 32 + 1, 1, [
        "00000000000000",
        "0............0",
        "0.43.32.21.10.",
        "0.43.32.21.10.",
        "0.43.32.21.10.",
        "0.43.32.21.10.",
        "0.4..3..2..1..",
        "0............0",
        "0............0",
        "0............0",
        "0............0",
        "0............0",
        "kk..........kk",
    ], {"0": "ink", "4": "pu4", "3": "pu3", "2": "pu2", "1": "pu1", "k": "kr0"})
    # nets on poles (wood group)
    for ox in (48, 64):
        for y in range(1, 15):
            if ox == 48:
                M.px(ox + 2, y, "wd1")
                M.px(ox + 3, y, "wd0")
            else:
                M.px(ox + 12, y, "wd1")
                M.px(ox + 13, y, "wd0")
        for x in range(16):
            M.px(ox + x, 2, "wd2")
        for y in range(3, 13):
            for x in range(16):
                if ox == 48 and x < 4 or ox == 64 and x > 11:
                    continue
                sag = round(2 * math.sin(math.pi * ((x + (ox - 48)) / 32)))
                if y < 4 + sag:
                    continue
                if (x + y) % 3 == 0 or (x - y) % 3 == 0:
                    M.px(ox + x, y, "wd3" if y < 9 else "wd2")
        for x in range(16):
            if (x + ox) % 5 == 0:
                M.px(ox + x, 13, "re3")
    return s


def stall():
    names = {"awning_L": (0, 0), "awning": (1, 0), "awning_R": (2, 0), "counter_L": (0, 1),
             "counter": (1, 1), "counter_R": (2, 1)}
    s = struct("stall", "The stall under the purple awning", 3, 2, SEC, walk=["TTT", "XXX"],
               names=names,
               notes="Gytheion's one shop (the hamlet's Agora): a stall on the quay under a "
                     "striped purple awning (drawn over the player), its counter of planks "
                     "with stock on racks of drying nets. Talk to the stallkeeper across the "
                     "counter. On borrowed path.")
    ground(s, "path")
    T, M = s.T, s.M
    for y in range(16):
        for x in range(48):
            if y < 2:
                continue
            stripe = (x // 4) % 2
            c = ("pu2", "w0")[stripe] if y < 11 else None
            if y == 2:
                c = "pu1"
            if y in (11, 12):
                # scalloped edge
                if (x % 4) in (1, 2) or y == 11:
                    c = ("pu1", "kr2")[stripe] if y == 11 else ("pu1" if stripe == 0 else "kr2")
                else:
                    c = None
            if x in (0, 47) and y < 13:
                c = "ink"
            if c:
                T.px(x, y, c)
    # counter and wares (wood group): planks, a scale, amphorae, a net
    for y in range(16, 32):
        for x in range(48):
            yy = y - 16
            if yy < 2:
                if x in (2, 3, 44, 45):
                    M.px(x, y, "wd1")
                continue
            if yy < 9:
                c = "wd3" if yy in (2, 3) else ("wd2" if (x + yy) % 8 else "wd1")
                if x in (2, 3, 44, 45):
                    c = "wd1"
                M.px(x, y, c)
            elif yy < 12:
                M.px(x, y, "wd1" if yy < 11 else "wd0")
    put(M, 6, 18, ["..00..", ".0110.", "011110", ".0110."], {"0": "wd0", "1": "tc2"})
    put(M, 20, 18, [".1.1.", "11111", ".111.", "..1.."], {"1": "re3"})
    put(M, 32, 17, ["..00..", ".0220.", "022220", "022220", ".0220."], {"0": "wd0", "2": "tc1"})
    return s


# --------------------------------------------------------------------------
# Kranai: the causeway and the shrine
# --------------------------------------------------------------------------

def causeway():
    names = {"H": (0, 0), "H_b": (1, 0), "H_W": (2, 0), "H_E": (3, 0),
             "V": (0, 1), "V_b": (1, 1), "V_N": (2, 1), "V_S": (3, 1)}
    s = struct("kranai_way", "The causeway to Kranai", 4, 2, SEC,
               walk=["....", "...."], names=names,
               notes="The low stone causeway from Gytheion's beach out to the islet of Kranai, "
                     "a cell wide, over the borrowed sea, rough blocks with the sea foaming "
                     "against them: east-west `H` (`H_b`; `H_W` `H_E` meet sand), north-south "
                     "`V` (`V_b`; `V_N` `V_S` meet sand). Walkable.")
    ground(s, "sea")
    M = s.M

    def block(X, Y, vertical):
        u, v = (Y % 16, X % 16) if vertical else (X % 16, Y % 16)
        k = hp(u, v, 191)
        joint = (u + (4 if (v // 5) % 2 else 0)) % 8 == 0 or v % 5 == 4
        c = "kr1" if joint else ("kr2" if k % 3 else "kr3")
        return c

    for cx in range(4):
        for vertical, oy in ((False, 0), (True, 16)):
            for y in range(16):
                for x in range(16):
                    X, Y = cx * 16 + x, oy + y
                    a, b = (x, y) if vertical else (y, x)   # a: across, b: along
                    if 3 <= a <= 12:
                        c = block(X, Y, vertical)
                        if a == 3:
                            c = "kr3"
                        if a == 12:
                            c = "kr0"
                        if a == 11 and not vertical:
                            c = "kr1"
                        M.px(X, Y, c)
                    elif a in (2, 13) and (b + cx) % 3:
                        M.px(X, Y, "w0")
                    elif a in (1, 14) and (b + cx) % 4 == 0:
                        M.px(X, Y, "w0")
            # ends: the causeway runs onto sand (sand drawn up to the waterline)
            if cx >= 2:
                for y in range(16):
                    for x in range(16):
                        X, Y = cx * 16 + x, oy + y
                        a, b = (x, y) if vertical else (y, x)
                        land = (b < 6) if cx == 2 else (b > 9)
                        if land and not (3 <= a <= 12):
                            M.px(X, Y, L.sand_px(X, Y))
                        elif (b == 6 if cx == 2 else b == 9) and not (3 <= a <= 12):
                            M.px(X, Y, "w0")
    return s


def shrine():
    names = {"roof_L": (0, 0), "roof": (1, 0), "roof_R": (2, 0), "wall_L": (0, 1),
             "door": (1, 1), "wall_R": (2, 1)}
    s = struct("kranai_shrine", "The shrine on Kranai", 3, 2, SEC, walk=["XXX", "XDX"],
               names=names,
               notes="Klymene's little whitewashed shrine on Kranai, where Paris and Helen "
                     "spent their first night: a gabled roof of gray slabs, whitewash gone "
                     "pink at the foot with old purple, a dark doorway (`door`, "
                     "`MB_NON_ANIMATED_DOOR`). The roof row stands on borrowed sand.")
    ground(s, "sand", [(0, 0), (2, 0)])
    B, M = s.B, s.M
    for y in range(16):
        for x in range(48):
            a = abs(x - 23.5)
            ridge = 1 + a * 0.4
            if y < ridge:
                continue
            c = "kr2" if (x + 2 * y) % 5 else "kr1"
            if y < ridge + 1.2:
                c = "kr3" if x < 24 else "kr1"
            if y >= 13:
                c = ("kr0", "kr1", "w0")[y - 13]
            (B if 16 <= x < 32 else M).px(x, y, c)
    for y in range(16):
        for x in range(16, 32):
            if B.get(x, y) is None:
                B.px(x, y, L.sand_px(x, y))
    for y in range(16, 32):
        for x in range(48):
            yy = y - 16
            c = "w0" if (x + y) % 9 else "kr3"
            if yy > 11:
                c = "pu4" if (x + yy) % 3 else "kr3"
            if yy == 15:
                c = "kr1"
            if x in (0, 47):
                c = "kr2"
            B.px(x, y, c)
    put(B, 18, 17, [
        "00000000000",
        "0iiiiiiiii0",
        "0iiiiiiiii0",
        "0iiiiiiiii0",
        "0iiiiiiiii0",
        "0iiiiiiiii0",
        "0iiiiiiiii0",
        "0iiiiiiiii0",
        "0iiiiiiiii0",
        "0iiiiiiiii0",
        "0iiiiiiiii0",
        "22222222222",
    ], {"0": "kr1", "i": "ink", "2": "kr2"})
    put(B, 21, 21, ["..1..", ".121.", "12221"], {"1": "pu2", "2": "pu3"})
    return s


# --------------------------------------------------------------------------
# The theater and its stage-building (the Asclepeion)
# --------------------------------------------------------------------------

def theater():
    n = 7
    W, H = n * 16, 4 * 16
    c0 = W / 2 - 0.5
    cy0 = H + 6.0
    s = struct("theater", "The little theater on the hill", n, 4, SEC,
               walk=["XXXXXXX", "X.....X", "X.....X", "X.....X"],
               names={"top": (3, 0), "seat": (3, 2), "orchestra": (3, 3), "west": (0, 3),
                      "east": (6, 3)},
               notes="Gytheion's theater, cut into the hill behind the hamlet: curved rows of "
                     "stone seats climbing the slope round the half-moon of the orchestra, 7 x "
                     "4, the hill's grass above (mirror-symmetric, so it costs half). Walk the "
                     "rows (the patients sit in the sun in the front ones); the outer cells "
                     "and the top are impassable. The stage-building, the Asclepeion, stands "
                     "across its open south side: `skene`.")
    B = s.B
    for y in range(H):
        for x in range(W):
            u = min(x, W - 1 - x)
            r = math.hypot(x - c0, (y - cy0) * 1.25)
            c = None
            if r < 26:
                # orchestra: beaten earth with a stone ring
                c = "pw1" if (u + y) % 7 else "sn3"
                if 24 < r < 26:
                    c = "sn2"
            elif r < 74:
                row = int((r - 26) // 6)
                t = (r - 26) % 6
                c = "sn3" if t < 2 else ("sn2" if t < 4 else "sn1")
                if t < 1:
                    c = "sn4"
                # aisles, like the spokes of a wheel
                ang = math.atan2(abs(x - c0), cy0 - y)
                if abs((ang * 180 / math.pi) % 30 - 15) < 1.6 and ang < 1.45:
                    c = "sn2" if t < 3 else "sn1"
                if row % 2 and t >= 4:
                    c = "sn1"
            elif r < 77:
                c = "sn1" if r < 75.5 else "gd"
            else:
                c = L.grass_px(x, y)
                c = "g2" if c == "g3" else c
            B.px(x, y, c)
    return s


def skene():
    names = {"roof_L": (0, 0), "roof": (1, 0), "roof_R": (5, 0), "wall_L": (0, 1),
             "pinax": (1, 1), "wall": (2, 1), "door": (3, 1), "rod": (4, 1), "wall_R": (5, 1)}
    s = struct("skene", "The stage-building: Gytheion's Asclepeion", 6, 2, SEC,
               walk=["XXXXXX", "XXXDXX"], names=names,
               notes="The theater's stage-building, its back to the town, which is Gytheion's "
                     "Asclepeion: a long low building of plastered stone under a flat roof, "
                     "a painted panel (`pinax`) and the rod of Asclepius (`rod`) beside the "
                     "door (`door`, `MB_NON_ANIMATED_DOOR`; Fly lands outside it). Place it "
                     "across the theater's open side. Impassable but the door.")
    B, T = s.B, s.T
    import lakonia_town as Tn
    W = 96
    for y in range(16):
        for x in range(W):
            c = Tn.roof_px(x, y)
            if y <= 1:
                c = "pw2" if y == 0 else "pw1"
            if y >= 11:
                c = ("pw2", "pw1", "sn3", "sn2", "sn1")[y - 11]
            if x <= 1:
                c = "pw2" if x == 0 else "pw1"
            if x >= W - 2:
                c = "pw1" if x == W - 2 else "sn2"
            B.px(x, y, c)
    for y in range(16, 32):
        for x in range(W):
            c = Tn.socle(x, y, 27) or Tn.plaster(x, y)
            if y == 16:
                c = "sn1"
            if x in (0, W - 1):
                c = "sn1"
            B.px(x, y, c)
    put(B, 48 + 3, 16, [
        "1111111111",
        "1i222122i1",
        "1i222122i1",
        "1i222122i1",
        "1i2221s2i1",
        "1i222122i1",
        "1i222122i1",
        "1i222122i1",
        "1i222122i1",
        "1i222122i1",
        "1iiiiiiii1",
        "3333333333",
    ], {"1": "ro1", "i": "ink", "2": "lr2", "s": "sn1", "3": "sn3"})
    # the pinax: a painted sea and palace, faded
    put(B, 16 + 2, 18, [
        "111111111111",
        "1pppppppppp1",
        "1pp22pp22pp1",
        "1p2222222pp1",
        "1pp1111ppp11",
        "1rrrrrrrrrr1",
        "1rr11rrrrrr1",
        "111111111111",
    ], {"1": "ro1", "p": "pw2", "2": "sn3", "r": "lr1"})
    # the rod of Asclepius: a staff with a serpent, bronze on the top layer
    put(T, 64 + 5, 17, [
        "..3...",
        ".323..",
        "..3...",
        ".v3...",
        "..3v..",
        ".v3...",
        "..3v..",
        ".v3...",
        "..3v..",
        "..3...",
    ], {"3": "wd2", "v": "tc1"})
    return s


# --------------------------------------------------------------------------
# The strait: Malea's current, the drowned town
# --------------------------------------------------------------------------

def current():
    names = {"current": (0, 0), "current_b": (1, 0)}
    s = struct("current", "The Malea current", 2, 1, SEC, walk=["WW"], names=names,
               notes="The fast current under Cape Malea's cliffs that carries surfers west "
                     "(`MB_WESTWARD_CURRENT`): streaks of foam on the borrowed sea, racing "
                     "west (animated). Lay a band of `current` `current_b` along the cliffs.")
    ground(s, "sea")
    M = s.M
    streaks = [(2, 2, 6), (10, 5, 4), (5, 9, 7), (13, 12, 5), (1, 14, 3)]

    def draw(F, f):
        for cx in range(2):
            for (sx, sy, ln) in streaks:
                for i in range(ln):
                    x = (sx - 4 * f + i + cx * 7) % 16
                    c = "w0" if i == 0 else ("b4" if i < ln - 1 else "b3")
                    F.px(cx * 16 + x, sy + (cx * 3) % 2, c)
    draw(M, 0)
    frames = L.anim_layer(s, "current", 4, layer="middle")
    for fi, F in enumerate(frames, start=1):
        F.a[:] = 0
        draw(F, fi)
    for x in range(2):
        s.behaviors[(x, 0)] = "MB_WESTWARD_CURRENT"
    return s


def drowned():
    names = {"wall_H": (0, 0), "wall_V": (1, 0), "NW": (2, 0), "NE": (3, 0),
             "SW": (0, 1), "SE": (1, 1), "door_H": (2, 1), "well": (3, 1),
             "street": (0, 2), "square": (1, 2), "column": (2, 2), "rubble": (3, 2)}
    s = struct("drowned", "The drowned town off Elaphonisos", 4, 3, SEC,
               walk=["WWWW", "WWWW", "WWWW"], names=names,
               notes="Under the clear turquoise shallows off Elaphonisos's north shore: "
                     "streets, house walls and a square with a well in it, seen through the "
                     "water (the post-game's Nereid Pearl dives here). Lay them over borrowed "
                     "shallows like a plan of a town: `wall_H`, `wall_V`, corners `NW` `NE` "
                     "`SW` `SE` (named for the corner of the house they make), `door_H` (a "
                     "wall with a doorway), `well`, `street` and `square` (paving), `column` "
                     "(a stump), `rubble`. Every cell is surfable sea (`MB_OCEAN_WATER`).")
    ground(s, "shallow")
    M = s.M
    for nm, (cx, cy) in names.items():
        ox, oy = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, oy + y
                ver = 6 <= x <= 9
                hor = 6 <= y <= 9
                arms = {"wall_H": hor, "wall_V": ver, "door_H": hor and not 4 <= x <= 11,
                        "NW": (hor and x >= 6) or (ver and y >= 6),
                        "NE": (hor and x <= 9) or (ver and y >= 6),
                        "SW": (hor and x >= 6) or (ver and y <= 9),
                        "SE": (hor and x <= 9) or (ver and y <= 9)}.get(nm)
                if arms:
                    lit = (y == 6 and hor) or (x == 6 and ver)
                    c = "dt3" if lit else ("dt2" if (x + y) % 5 else "dt1")
                    if (hor and y == 9) or (ver and x == 9):
                        c = "dt1"
                    M.px(X, Y, c)
                elif arms is not None and (x + y) % 7 == 0:
                    M.px(X, Y, "dt2")
        if nm in ("street", "square"):
            for y in range(16):
                for x in range(16):
                    k = hp(x, y, 201 + (nm == "square"))
                    if (x % 4 == 0 or y % 4 == 0) and k % 3:
                        M.px(ox + x, oy + y, "dt2")
                    elif nm == "square" and k % 11 == 0:
                        M.px(ox + x, oy + y, "dt3")
        if nm == "well":
            for y in range(16):
                for x in range(16):
                    r = math.hypot(x - 7.5, y - 7.5)
                    if 3.5 < r < 6.2:
                        M.px(ox + x, oy + y, "dt3" if y < 7 else "dt1")
                    elif r <= 3.5:
                        M.px(ox + x, oy + y, "b1")
        if nm == "column":
            for y in range(16):
                for x in range(16):
                    r = math.hypot(x - 7.5, y - 7.5)
                    if r < 4.5:
                        M.px(ox + x, oy + y, "dt3" if x + y < 15 else "dt2")
                    elif r < 5.5:
                        M.px(ox + x, oy + y, "dt1")
        if nm == "rubble":
            for (rx, ry) in ((3, 3), (9, 2), (6, 8), (12, 10), (2, 12), (10, 6)):
                put(M, ox + rx, oy + ry, ["32", "21"], {"3": "dt3", "2": "dt2", "1": "dt1"})
    for y in range(3):
        for x in range(4):
            s.behaviors[(x, y)] = "MB_OCEAN_WATER"
    return s


def build():
    return [quayside(), dyeworks(), vats(), stall(), causeway(), shrine(), theater(), skene(),
            current(), drowned()]
