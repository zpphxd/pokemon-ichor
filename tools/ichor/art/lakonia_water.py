"""Lakonia's fresh water: the Eurotas and its banks, reeds and oleander, the
stone ford and the fisher's rock, the plain bridge and the Platanistas's
footbridges with their statues; Lake Stymphalia's black water, its reed
grass, reed curtains, the roosting reeds and the reed wall that grows back,
the causeway on piles, the boardwalks and Akanthis's stilt hut.

Water is lakonia_lib.water(): an animated texture in the bottom layer, the
same few tiles under every water cell; banks, reeds, planks and stone are
drawn on the middle layer over it.
"""
from __future__ import annotations

import math

import numpy as np

import lakonia_lib as L
from lakonia_lib import ground, put, struct

SEC = "water"
hp, mx = L.hp, L.mx

# --------------------------------------------------------------------------
# Reeds
# --------------------------------------------------------------------------

TOPS = [2, 5, 0, 4, 1, 6, 3, 7]


def reed_px(X, Y, ramp=("re4", "re3", "re2", "re1"), sparse=False):
    """Reeds seen from the south: two staggered rows of plumed blades per
    cell, each cell mirror-symmetric. ramp: plume, lit stem, stem, base."""
    x, y = mx(X), Y % 16
    for t0 in (TOPS[x], TOPS[x] + 8):
        dy = (y - t0) % 16
        if dy < 8:
            break
    if dy == 0:
        return ramp[0]
    if dy == 1:
        return ramp[0] if x % 3 == 0 else ramp[1]
    if dy < 5:
        return ramp[1] if x % 2 == 0 else ramp[2]
    if sparse:
        return None
    return ramp[2] if dy < 6 and x % 2 == 0 else ramp[3]


def grass_bank(X, Y):
    c = L.grass_px(X, Y)
    return "g2" if c == "g3" else c


# --------------------------------------------------------------------------
# The Eurotas
# --------------------------------------------------------------------------

def river():
    def paint(s, X, Y, d):
        u, v = mx(X), Y % 16
        if d > 1.5:
            # a fringe of reeds standing in the water along every bank
            if d < 3.5 and u in (2, 3) and v % 8 < 5:
                c = reed_px(X, Y, sparse=True)
                if c:
                    s.M.px(X, Y, c)
            return
        if d > 0.5:
            if (u + v) % 4 == 0:
                s.M.px(X, Y, "ew2")
            return
        if d > -0.6:
            s.M.px(X, Y, "re1")
        elif d > -1.6:
            s.M.px(X, Y, "re2" if (u + v) % 3 else "re1")
        elif d > -2.5:
            s.M.px(X, Y, "gd" if (u + v) % 2 else "g1")
        else:
            s.M.px(X, Y, grass_bank(X, Y))

    def fisher_rock(s, ox, oy):
        put(s.M, ox + 2, oy + 3, [
            "...444444...",
            ".4433333332.",
            "433333333322",
            "433333333322",
            "333333333221",
            ".2222222221.",
            "..e1111111..",
            "...eeeeee...",
        ], {"4": "re4", "3": "re3", "2": "re2", "1": "re1", "e": "ew0"})

    def ford(s, ox, oy):
        for (sx, sy) in ((2, 1), (8, 4), (3, 8), (9, 11)):
            put(s.M, ox + sx, oy + sy, [".444.", "43332", "33322", ".e11.", "..e.."],
                {"4": "re4", "3": "re3", "2": "re2", "1": "re1", "e": "ew0"})

    def tuft(s, ox, oy):
        for y in range(16):
            for x in range(16):
                if math.hypot((x - 7.5) / 6.5, (y - 8.5) / 6.8) < 1:
                    c = reed_px(ox + x, oy + y)
                    if c:
                        s.M.px(ox + x, oy + y, c)

    s = L.autotile("river", "The Eurotas: green water, soft banks", SEC, paint, walk_code="P",
                   seed=1.0, e=4.0, r=4.0,
                   extra=[("rock", "1|11111111", fisher_rock), ("ford", "1|11111111", ford),
                          ("tuft", "1|11111111", tuft)],
                   notes="The Eurotas, the Platanistas's moat and every stream: slow green water "
                         "(animated) between soft grass banks with a fringe of reeds, as all 47 "
                         "soft-edge shapes; kythera_lib.blob_key gives a cell's key from a water "
                         "mask, and `1|11111111` is open water. Every cell is fresh water "
                         "(`MB_POND_WATER`, surfable; fish from the bank). Extra open-water cells: "
                         "`rock`, a flat rock the fisher stands on (impassable); `ford`, stepping "
                         "stones across a side stream (walkable: lay a line of them); `tuft`, a "
                         "clump of reeds in midstream (impassable).")
    L.water(s, "eurotas")
    rows = [list(r) for r in s.walk]
    for nm, wc, beh in (("rock", "X", None), ("ford", ".", "MB_NORMAL"), ("tuft", "X", None)):
        x, y = s.names[nm]
        rows[y][x] = wc
        s.behaviors.pop((x, y), None)
    s.walk = ["".join(r) for r in rows]
    return s


def reeds():
    def paint(s, X, Y, d):
        if d > 1.0:
            c = reed_px(X, Y)
        elif d > -1.5:
            c = reed_px(X, Y, sparse=True)
        else:
            c = None
        if c:
            s.M.px(X, Y, c)

    s = L.autotile("reeds", "Eurotas reed beds in the shallows (tall grass)", SEC, paint,
                   walk_code="G", seed=3.0, e=3.0, r=4.0, amp=1.2,
                   notes="The reed beds the agoge's boys cut barehanded for their beds: dense "
                         "reeds standing in the river's green water, as all 47 soft-edge shapes "
                         "(the region is the reeds; open water round it is `river`'s "
                         "`1|11111111`). `MB_TALL_GRASS`: walk in, knee-deep, and meet "
                         "Pokémon. Also the Sickle's reed thicket on Route 25, and Orthia's "
                         "marshy bank.")
    L.water(s, "eurotas", walk=None, behavior=None)
    for y in range(s.h):
        for x in range(s.w):
            s.behaviors[(x, y)] = "MB_TALL_GRASS"
    return s


def oleander():
    s = struct("oleander", "Oleander", 3, 1, SEC, walk=["XXX"],
               names={"bush": (0, 0), "thicket_L": (1, 0), "thicket_R": (2, 0)},
               notes="Pink oleander, the riverbank shrub: `bush`, and a two-cell thicket "
                     "`thicket_L` `thicket_R`. Impassable, on borrowed grass. Poisonous; the "
                     "goats know.")
    ground(s, "grass")
    M = s.M
    m = np.zeros((16, 48), bool)
    for y in range(16):
        for x in range(48):
            a = math.atan2(y - 8, x - 7.5)
            if math.hypot((x - 7.5) / 7.2, (y - 7.5) / 6.6) < 1 + 0.08 * math.sin(a * 6) and y < 14:
                m[y, x] = True
            if math.hypot((x - 32) / 15.2, (y - 7.5) / 6.6) < 1 + 0.06 * math.sin(a * 9) and y < 14:
                m[y, x] = True
    sh = np.zeros_like(m)
    sh[2:, 1:] = m[:-2, :-1]
    for y, x in zip(*np.nonzero(sh & ~m)):
        if y >= 9:
            M.px(int(x), int(y), "gd" if (x + y) % 2 == 0 else "g1")
    for y, x in zip(*np.nonzero(m)):
        x, y = int(x), int(y)
        k = hp(x % 16, y, 121)
        up = y == 0 or not m[y - 1, x]
        dn = y == 15 or not m[y + 1, x]
        # narrow leaves in spiky clusters, lit from the top left
        c = "re1" if (x + 2 * y) % 5 < 2 else "gd"
        if up or (x % 16 < 8 and y < 7 and k % 3 == 0):
            c = "g1" if k % 2 else "re2"
        if dn:
            c = "re1"
        M.px(x, y, c)
    for (bx, by) in ((3, 3), (8, 2), (11, 6), (5, 8), (9, 10), (18, 3), (24, 5), (30, 2),
                     (36, 4), (42, 6), (27, 9), (20, 8), (38, 9), (33, 7)):
        put(M, bx, by, [".a.", "aba", ".a."], {"a": "op2", "b": "op1"})
    m2 = np.zeros_like(m)
    return s


# --------------------------------------------------------------------------
# Bridges, the ford's statues
# --------------------------------------------------------------------------

def bridge():
    names = {"deck_W": (0, 0), "deck": (1, 0), "deck_E": (2, 0),
             "face_W": (0, 1), "arch": (1, 1), "face_E": (2, 1),
             "foot_V": (3, 0), "foot_H": (3, 1), "foot_V_N": (4, 0), "foot_V_S": (4, 1)}
    s = struct("bridge", "The plain stone bridge, and footbridges", 5, 2, SEC,
               walk=["....." , "XXX.."], names=names,
               notes="Lakonia's plain stone bridge over the Eurotas, east-west across a "
                     "north-south river: `deck_W` `deck` `deck_E` (repeat `deck`), low kerbs "
                     "either side, over `face_W` `arch` `face_E`, its south face standing in "
                     "the water. The deck's ends sit on the banks' grass. Footbridges of plank "
                     "on posts, one cell wide: `foot_V` runs north-south (end it with "
                     "`foot_V_N` `foot_V_S` on the banks), `foot_H` east-west. All decks "
                     "walkable; the face is impassable water.")
    B, M = s.B, s.M
    # stone deck: kerbs at top and bottom, flags between
    for cx in (0, 1, 2):
        for y in range(16):
            for x in range(16):
                X = cx * 16 + x
                c = "sn3" if (x + 5 * (y // 4)) % 8 else "sn2"
                if y % 4 == 3:
                    c = "sn2"
                if y in (0, 1):
                    c = ("sn4", "sn3")[y]
                elif y == 2:
                    c = "sn1"
                elif y in (13, 14):
                    c = ("sn4", "sn3")[y - 13]
                elif y == 15:
                    c = "sn1"
                B.px(X, y, c)
    # ends meet grass: a short ramp of grass on the outer side
    for cx, side in ((0, -1), (2, 1)):
        for y in range(16):
            for x in range(16):
                lx = x if side < 0 else 15 - x
                if lx < 3:
                    B.px(cx * 16 + x, y, grass_bank(cx * 16 + x, y))
                elif lx == 3:
                    B.px(cx * 16 + x, y, "sn1")
    # the south face over water (bottom water, middle stone)
    for cx in (0, 1, 2):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, 16 + y
                c = None
                if y < 5:
                    c = ("sn3", "sn2", "sn2", "sn3", "sn2")[y]
                    if y in (1, 3) and x % 8 == 0:
                        c = "sn1"
                elif cx == 1:
                    ax = abs(x - 7.5)
                    top = 5 + (ax / 7.5) ** 2 * 6
                    if y < top or ax > 6.5:
                        c = "sn2" if (x + y) % 5 else "sn1"
                        if y >= top - 1 and ax <= 6.5:
                            c = "sn1"
                    elif y < top + 2:
                        c = "sn0"
                else:
                    inner = x if cx == 2 else 15 - x
                    if inner > 5:
                        c = "sn2" if (x + y) % 5 else "sn1"
                        if y == 15:
                            c = "sn1"
                    elif inner > 4:
                        c = "sn1"
                if c:
                    M.px(X, Y, c)
    # plank footbridges over water
    ox = 48
    for y in range(16):
        for x in range(3, 13):
            c = "wd3" if y % 4 else "wd1"
            if x in (3, 12):
                c = "wd0"
            elif x in (4, 11):
                c = "wd1"
            M.px(ox + x, y, c)
        if y % 8 == 2:
            M.px(ox + 2, y, "wd0")
            M.px(ox + 13, y, "wd0")
    oy = 16
    for x in range(16):
        for y in range(3, 12):
            c = "wd3" if x % 4 else "wd1"
            if y == 3:
                c = "wd1"
            if y in (10, 11):
                c = ("wd1", "wd0")[y - 10]
            M.px(ox + x, oy + y, c)
        if x % 8 == 2:
            for y in (12, 13):
                M.px(ox + x, oy + y, "wd0")
    # bank landings for the north-south footbridge: planks onto grass
    for cy, north in ((0, True), (1, False)):
        oyy = cy * 16
        for y in range(16):
            for x in range(16):
                X, Y = 64 + x, oyy + y
                land = (y < 7) if north else (y > 8)
                if land:
                    M.px(X, Y, grass_bank(X, Y))
                    if 3 <= x <= 12 and (y >= 4 if north else y <= 11):
                        M.px(X, Y, "sn3" if (x + y) % 3 else "sn2")
                elif y == (7 if north else 8) and not 3 <= x <= 12:
                    M.px(X, Y, "gd")
                elif 3 <= x <= 12:
                    c = "sn3" if (x + 2 * (y // 3)) % 5 else "sn2"
                    if x in (3, 12) or y % 3 == 2:
                        c = "sn1" if x == 12 or y % 3 == 2 else "sn4"
                    M.px(X, Y, c)
    L.water(s, "eurotas", cells=[(0, 1), (1, 1), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1)],
            walk=None, behavior=None)
    s.walk = [".....", "XXX.."]
    s.behaviors = {}
    return s


def landing_fix(s):
    return s


def statues():
    s = struct("statues", "Herakles and Lykourgos at the Platanistas's bridges", 2, 2, SEC,
               walk=["TT", "XX"],
               names={"herakles": (0, 0), "herakles_base": (0, 1), "lykourgos": (1, 0),
                      "lykourgos_base": (1, 1)},
               notes="The Platanistas's two bridgeheads: Herakles in his lion skin with his "
                     "club, and Lykourgos the lawgiver, bearded, with his staff, in old "
                     "weathered marble (objects). Each is a head (drawn over the player) over "
                     "a base (impassable). On borrowed grass.")
    ground(s, "grass")
    T, M = s.T, s.M
    lk = {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1", "0": "sn0"}
    put(T, 2, 2, [
        "....3333....",
        "...344443...",
        "..34433443..",
        "..3433334321",
        "..340330432.",
        "...3333332..",
        "..33433332..",
        ".3344333321.",
        "334433333221",
        "344433333221",
        "344333332221",
        "34433333222.",
        "3443333322..",
        "3443333332..",
    ], lk)
    put(M, 2, 16, [
        "3443333332..",
        ".343333332..",
        ".333332222..",
        "..33.33221..",
        "..33.33221..",
        "..33.33221..",
        "..32.32211..",
        ".1111111111.",
        "444444444444",
        "433333333332",
        "433333333332",
        "222222222221",
        ".1111111111.",
    ], lk)
    for y in range(4, 16):
        T.px(2 + 11, y, "sn1")
    put(M, 13, 16, ["2", "1", "1"], lk)
    put(T, 18, 1, [
        "...3333.....1",
        "..344443....1",
        "..343433....1",
        "..3333332...1",
        "...34432....1",
        "..3344332...1",
        "..34444332..1",
        ".334444332..1",
        "3344444333221",
        "3443333333221",
        "3443333332221",
        "344333333222.",
        "34433333322.1",
        "344333333221.",
        ".44333333221.",
    ], lk)
    put(M, 18, 16, [
        ".44333333221.",
        ".43333333221.",
        ".43333333221.",
        ".43333332221.",
        ".43333332221.",
        ".43333332221.",
        ".2222222221..",
        ".1111111111..",
        "444444444444.",
        "4333333333321",
        "4333333333321",
        "2222222222221",
        ".11111111111.",
    ], lk)
    for (x, y) in ((22, 7), (24, 7)):
        T.px(x, y, "sn1")
    return s


# --------------------------------------------------------------------------
# Lake Stymphalia
# --------------------------------------------------------------------------

MARSH_REED = ("re3", "re2", "re1", "bw1")
CURTAIN = ("re2", "re1", "md1", "bw0")


def marsh():
    def paint(s, X, Y, d):
        u, v = mx(X), Y % 16
        if d > 1.0:
            return
        if d > 0.0:
            if (u + v) % 3 == 0:
                s.M.px(X, Y, "bw2")
            return
        if d > -1.0:
            s.M.px(X, Y, "md1")
        elif d > -2.2:
            s.M.px(X, Y, "md1" if (u + v) % 3 == 0 else "re1")
        elif d > -3.0:
            s.M.px(X, Y, "gd" if (u + v) % 2 else "g1")
        else:
            s.M.px(X, Y, grass_bank(X, Y))

    def rock(s, ox, oy):
        put(s.M, ox + 1, oy + 2, [
            "....1111......",
            "..11222111....",
            ".1223332211...",
            "12233332221111",
            "12333322221221",
            "12222222211221",
            ".1111111111111",
            "..0000000000..",
        ], {"3": "re3", "2": "re2", "1": "re1", "0": "bw0"})

    def stump(s, ox, oy):
        put(s.M, ox + 4, oy + 3, [
            "..1111..",
            ".122221.",
            "12322221",
            "12222221",
            "11222211",
            ".111111.",
            "00011000",
            ".0....0.",
        ], {"3": "re4", "2": "md1", "1": "re1", "0": "bw0"})

    s = L.autotile("marsh", "Lake Stymphalia: black water, muddy shores", SEC, paint,
                   walk_code="P", seed=2.0, e=4.0, r=4.0,
                   extra=[("rock", "1|11111111", rock), ("stump", "1|11111111", stump)],
                   notes="Lake Stymphalia's still black water (animated, barely) between muddy "
                         "grass shores, as all 47 soft-edge shapes; `1|11111111` is open water. "
                         "Fresh water (`MB_POND_WATER`, surfable). Extra open-water cells: "
                         "`rock`, a low rock in the water (the islets' rocks; the far rock with "
                         "the item), `stump`, a drowned stump. Both impassable.")
    L.water(s, "marsh")
    rows = [list(r) for r in s.walk]
    for nm in ("rock", "stump"):
        x, y = s.names[nm]
        rows[y][x] = "X"
        s.behaviors.pop((x, y), None)
    s.walk = ["".join(r) for r in rows]
    return s


def marsh_reeds():
    def paint(s, X, Y, d):
        if d > 1.0:
            c = reed_px(X, Y, ramp=MARSH_REED)
        elif d > -1.5:
            c = reed_px(X, Y, ramp=MARSH_REED, sparse=True)
        else:
            c = None
        if c:
            s.M.px(X, Y, c)

    s = L.autotile("marsh_reeds", "Stymphalia's reed grass in the shallows (tall grass)", SEC, paint,
                   walk_code="G", seed=5.0, e=3.0, r=4.0, amp=1.2,
                   notes="Reed grass standing in the black water, on the islets and across the "
                         "causeway (the forced band), as all 47 soft-edge shapes. "
                         "`MB_TALL_GRASS`.")
    L.water(s, "marsh", walk=None, behavior=None)
    for y in range(s.h):
        for x in range(s.w):
            s.behaviors[(x, y)] = "MB_TALL_GRASS"
    return s


def curtain():
    def paint(s, X, Y, d):
        u, v = mx(X), Y % 16
        if d > 0.5:
            c = reed_px(X, Y, ramp=CURTAIN)
            if c in ("md1", "bw0") and (u * 3 + v) % 7 == 0:
                c = "re1"
            s.M.px(X, Y, c)
        elif d > -1.5:
            c = reed_px(X, Y, ramp=CURTAIN, sparse=True)
            if c:
                s.M.px(X, Y, c)

    s = L.autotile("curtain", "Dense reed curtains", SEC, paint, walk_code="X", seed=7.0,
                   e=2.0, r=3.0, amp=1.0,
                   notes="Reeds too thick to walk through, standing in black water: the "
                         "curtain round the reed-bed nests (its gap is the way in) and the "
                         "lake's walls, as all 47 soft-edge shapes. Impassable.")
    L.water(s, "marsh", walk=None, behavior=None)
    return s


def roost():
    names = {"L": (0, 0), "M": (1, 0), "R": (2, 0), "M_b": (3, 0)}
    s = struct("roost", "The bronze birds' roost (the north bed)", 4, 1, SEC, walk=["XXXX"],
               names=names,
               notes="The north shore's reed bed where the Stymphalian birds roost so thick "
                     "nobody can walk in (LABORS's Stymphalian Reeds, Labor 6): a curtain of "
                     "reeds with bronze feathers glinting in it (`glint`, animated). Run `L` "
                     "`M` (`M_b`) `R` along the curtain's front. Impassable.")
    M = s.M
    for cx in range(4):
        for y in range(16):
            for x in range(16):
                X = cx * 16 + x
                c = reed_px(X, y, ramp=CURTAIN)
                if (cx == 0 and x < 3) or (cx == 2 and x > 12):
                    c = reed_px(X, y, ramp=CURTAIN, sparse=True)
                if c:
                    M.px(X, y, c)
    birds = [(4, 5), (10, 2), (13, 9), (20, 6), (27, 3), (24, 11), (36, 4), (41, 8), (52, 3),
             (58, 7), (49, 10)]
    for (bx, by) in birds:
        put(M, bx, by, [".33.", "3223", ".22."], {"3": "bz3", "2": "bz2"})
    L.water(s, "marsh", walk=None, behavior=None)
    frames = L.anim_layer(s, "glint", 3, layer="middle")
    for fi, F in enumerate(frames, start=1):
        for i, (bx, by) in enumerate(birds):
            if (i + fi) % 3 == 0:
                put(F, bx, by, [".33.", "3333", ".33."], {"3": "bz3"})
            elif (i + fi) % 3 == 1:
                put(F, bx, by, [".22.", "2332", ".22."], {"2": "bz2", "3": "bz3"})
    return s


def regrow():
    names = {"wall": (0, 0), "wall_b": (1, 0), "cut": (2, 0), "cut_b": (3, 0)}
    s = struct("regrow", "The reed wall that grows back (the south-east bed)", 4, 1, SEC,
               walk=["XX.."], names=names,
               notes="The south-east shore's reed wall that grows back as fast as Demeter's "
                     "Sickle cuts it (LABORS's Springs of Lerna, Labor 2): `wall` `wall_b` "
                     "(impassable, a tangle of green new shoots among the old reeds) and "
                     "`cut` `cut_b`, the same cells cut to stubble, which a script swaps in "
                     "and out. Behind it, draw the eight pools with `marsh`.")
    M = s.M
    for cx in range(4):
        for y in range(16):
            for x in range(16):
                X = cx * 16 + x
                if cx < 2:
                    c = reed_px(X, y, ramp=("my4" if False else "re3", "re2", "re1", "md1"))
                    if (mx(X) + y + cx) % 5 == 0 and y > 3:
                        c = "g1" if y % 2 else "gd"
                    M.px(X, y, c)
                else:
                    u = mx(X)
                    if y % 4 == 3 and u % 2 == (cx % 2):
                        M.px(X, y, "re3" if (u + y) % 3 else "re2")
                    elif y % 4 == 2 and u % 2 == (cx % 2):
                        M.px(X, y, "re1")
                    elif y % 4 == 3:
                        M.px(X, y, "md1")
    L.water(s, "marsh", walk=None, behavior=None)
    return s


# --------------------------------------------------------------------------
# The causeway, the boardwalks, the stilt hut
# --------------------------------------------------------------------------

def causeway():
    names = {"V": (0, 0), "V_b": (1, 0), "V_N": (2, 0), "V_S": (3, 0),
             "H": (0, 1), "H_W": (1, 1), "H_E": (2, 1), "turn": (3, 1),
             "face": (0, 2), "face_W": (1, 2), "face_E": (2, 2), "face_turn": (3, 2)}
    s = struct("causeway", "The old stone causeway on piles", 4, 3, SEC,
               walk=["....", "....", "XXXX"], names=names,
               notes="The causeway from Stymphalia's south shore: old paving on stone piles "
                     "over the black water, green with slime at the waterline. Two cells "
                     "of it: north-south `V` (`V_b` a variant; `V_N` `V_S` end it on a bank), "
                     "and east-west `H` (`H_W` `H_E` end it on a bank) with its south face "
                     "`face` (`face_W` `face_E`) in the row below: piers and dark water "
                     "between. `turn` joins a north-south run onto an east-west one (put "
                     "`face_turn` under it). Deck walkable; face impassable.")
    B, M = s.B, s.M

    def paving(X, Y):
        u, v = mx(X), Y % 16
        c = "sn3" if (u + 4 * (v // 5)) % 7 else "sn2"
        if v % 5 == 4:
            c = "sn2"
        if (u * 3 + v * 5) % 23 == 0:
            c = "sn4"
        return c

    # north-south: paving x 3..12, a curb, the piles' tops either side
    for cx in range(4):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, y
                if 3 <= x <= 12:
                    c = paving(X, Y)
                    if x in (3, 12):
                        c = "sn4" if x == 3 else "sn1"
                    if cx == 2 and y < 4 or cx == 3 and y > 11:
                        c = None
                    if c:
                        M.px(X, Y, c)
                elif x in (2, 13):
                    M.px(X, Y, "g1" if (y % 6 == 2) else "gd")
                if x in (1, 14) and y % 8 in (5, 6) and cx < 2:
                    M.px(X, Y, "sn2" if x == 1 else "sn1")
        if cx == 1:
            for (px_, py_) in ((6, 4), (9, 10)):
                M.px(X - 15 + px_, py_, "sn1")
    for cx, north in ((2, True), (3, False)):
        for y in range(16):
            for x in range(16):
                X = cx * 16 + x
                land = (y < 5) if north else (y > 10)
                if land:
                    M.px(X, y, grass_bank(X, y))
                    if 3 <= x <= 12:
                        M.px(X, y, paving(X, y))
                elif y in ((5,) if north else (10,)) and not (3 <= x <= 12):
                    M.px(X, y, "gd")
    # east-west deck and its south face
    for cx in range(4):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, 16 + y
                c = paving(X, Y)
                if y == 0:
                    c = "sn1"
                elif y == 1:
                    c = "sn4"
                elif y == 15:
                    c = "sn4"
                if cx == 1 and x < 3:
                    c = grass_bank(X, Y) if y > 1 else None
                if cx == 2 and x > 12:
                    c = grass_bank(X, Y) if y > 1 else None
                if cx == 3 and (x < 3 or x > 12) and y < 1:
                    c = None
                if cx == 3 and (x < 3 or x > 12) and y >= 1:
                    c = paving(X, Y) if y > 1 else "sn4"
                if c:
                    M.px(X, Y, c)
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, 32 + y
                pier = (x % 16) in range(5, 11)
                c = None
                if y < 4:
                    c = ("sn2", "sn1", "sn2", "sn1")[y] if not (y == 1 and x % 4 == 0) else "sn0"
                elif pier:
                    c = "sn2" if x % 16 in (5, 6) else "sn1"
                    if y > 10:
                        c = "g1" if (x + y) % 2 else "gd"
                    if y == 15:
                        c = "sn0"
                elif y < 6:
                    c = "sn0"
                if cx == 1 and x < 3 or cx == 2 and x > 12:
                    c = "gd" if y < 3 else None
                if c:
                    M.px(X, Y, c)
    L.water(s, "marsh", walk=None, behavior=None)
    s.walk = ["....", "....", "XXXX"]
    s.behaviors = {}
    return s


def boardwalk():
    names = {"V": (0, 0), "H": (1, 0), "cross": (2, 0), "end_N": (3, 0), "end_S": (4, 0),
             "end_W": (5, 0), "end_E": (6, 0), "V_sit": (7, 0),
             "T_E": (0, 1), "T_W": (1, 1), "T_N": (2, 1), "T_S": (3, 1),
             "NE": (4, 1), "NW": (5, 1), "SE": (6, 1), "SW": (7, 1)}
    s = struct("boardwalk", "Wooden boardwalks over the mud and water", 8, 2, SEC,
               walk=["........", "........"], names=names,
               notes="Boardwalks of gray old planks on posts, one cell wide, threading the "
                     "reed islets: `V` north-south, `H` east-west, `cross`, T-junctions "
                     "(`T_E` has a branch east, and so on), corners (`NE` joins north and "
                     "east, and so on) and ends (`end_N` is the north end of a run: its "
                     "last plank, the open water beyond). `V_sit` is a run with a gap at "
                     "its edge where Borboros sits with his legs over the side. Walkable; "
                     "the water round them shows through.")
    M = s.M
    arms = {"V": "NS", "H": "EW", "cross": "NSEW", "end_N": "S", "end_S": "N", "end_W": "E",
            "end_E": "W", "V_sit": "NS", "T_E": "NSE", "T_W": "NSW", "T_N": "EWN", "T_S": "EWS",
            "NE": "NE", "NW": "NW", "SE": "SE", "SW": "SW"}
    for nm, (cx, cy) in names.items():
        a = arms[nm]
        ox, oy = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                inV = 3 <= x <= 12 and (("N" in a and y <= 8) or ("S" in a and y >= 7))
                inH = 3 <= y <= 12 and (("W" in a and x <= 8) or ("E" in a and x >= 7))
                hub = 3 <= x <= 12 and 3 <= y <= 12 and len(a) > 1
                if nm.startswith("end_"):
                    if nm == "end_N":
                        inV = 3 <= x <= 12 and y >= 2
                    if nm == "end_S":
                        inV = 3 <= x <= 12 and y <= 13
                    if nm == "end_W":
                        inH = 3 <= y <= 12 and x >= 2
                    if nm == "end_E":
                        inH = 3 <= y <= 12 and x <= 13
                if not (inV or inH or hub):
                    continue
                if inV and not inH:
                    c = "wd3" if y % 4 else "wd1"
                    if x in (3, 12):
                        c = "wd1"
                    if (x + y * 3) % 11 == 0:
                        c = "wd2"
                elif inH and not inV:
                    c = "wd3" if x % 4 else "wd1"
                    if y == 3:
                        c = "wd2"
                    if y == 12:
                        c = "wd0"
                    if (y + x * 3) % 11 == 0:
                        c = "wd2"
                else:
                    c = "wd2" if (x + y) % 4 else "wd1"
                M.px(ox + x, oy + y, c)
        # posts at the corners of every run, shadows on the water east and south
        for (px_, py_) in ((2, 2), (13, 2), (2, 13), (13, 13)):
            if M.get(ox + px_ + (1 if px_ < 8 else -1), oy + py_) or \
                    M.get(ox + px_, oy + py_ + (1 if py_ < 8 else -1)):
                M.px(ox + px_, oy + py_, "wd0")
        for y in range(16):
            for x in range(16):
                if M.get(ox + x, oy + y) is None and x > 0 and y > 0 and \
                        M.get(ox + x - 1, oy + y - 1) in ("wd1", "wd2", "wd3"):
                    M.px(ox + x, oy + y, "bw0")
    # Borboros's gap: a missing plank at the run's east edge
    ox, oy = 7 * 16, 0
    for y in range(6, 10):
        for x in range(10, 13):
            M.px(ox + x, oy + y, "bw0" if y > 6 else "wd0")
    L.water(s, "marsh", walk=None, behavior=None)
    return s


def stilt_hut():
    names = {"roof_L": (0, 0), "roof": (1, 0), "roof_R": (2, 0), "wall_L": (0, 1),
             "door": (1, 1), "wall_R": (2, 1), "porch_L": (0, 2), "porch": (1, 2),
             "porch_R": (2, 2)}
    s = struct("stilt_hut", "Akanthis's stilt hut", 3, 3, SEC,
               walk=["XXX", "XDX", "..."], names=names,
               notes="The old fowler's hut on stilts beside the causeway (the rest point): a "
                     "reed-thatched roof, walls of woven reed on a timber frame, nets drying, "
                     "and a plank porch over the water where it meets the causeway. `door` "
                     "(`MB_NON_ANIMATED_DOOR`) opens off the porch; the porch is walkable. "
                     "The hidden item is under the hut.")
    B, M = s.B, s.M
    # thatch: domed, overhanging
    for y in range(26):
        for x in range(48):
            edge = abs(x - 23.5)
            topy = 3 + max(0, edge - 16) * 0.6
            if y < topy or edge > 23.5:
                continue
            course = int((y - topy) // 3)
            c = "re3" if (x + course * 3) % 4 else "re4"
            if (y - int(topy)) % 3 == 2:
                c = "re2"
            if y >= 23:
                c = ("re2", "wd1", "wd0")[y - 23]
            if edge > 22.5:
                c = "wd0"
            M.px(x, y, c)
    # walls of woven reed panels, a dark door
    for y in range(26, 32):
        for x in range(2, 46):
            c = "re2" if (x + y) % 3 else "re3"
            if x % 9 == 0:
                c = "wd1"
            M.px(x, y, c)
    for y in range(18, 32):
        for x in range(19, 29):
            if y < 23:
                continue
            c = "wd0" if x in (19, 28) else ("ink" if y > 23 else "wd1")
            M.px(x, y, c)
    put(M, 4, 26, ["w.w.w", ".w.w.", "w.w.w"], {"w": "wd3"})
    # porch planks and stilts
    for y in range(32, 48):
        for x in range(48):
            yy = y - 32
            if yy < 9:
                c = "wd3" if x % 4 else "wd1"
                if yy == 0:
                    c = "wd1"
                if yy == 8:
                    c = "wd0"
                M.px(x, y, c)
            elif x % 15 in (2, 3) and yy < 15:
                M.px(x, y, "wd1" if x % 15 == 2 else "wd0")
            elif yy < 11 and x > 0 and M.get(x - 1, y - 1) in ("wd0", "wd1", "wd3"):
                M.px(x, y, "bw0")
    # behind the roof: the water (the top cells' corners)
    L.water(s, "marsh", walk=None, behavior=None)
    s.walk = ["XXX", "XDX", "..."]
    s.behaviors = {(1, 1): "MB_NON_ANIMATED_DOOR"}
    return s


def build():
    return [river(), reeds(), oleander(), bridge(), statues(), marsh(), marsh_reeds(),
            curtain(), roost(), regrow(), causeway(), boardwalk(), stilt_hut()]
