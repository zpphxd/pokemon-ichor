"""Mount Ida and the caves (LABYRINTH §2; SCRIPT.md Part 2, Part 10): holm oaks
and goat pastures on the Ida path; the cradle shrine, the Idaean Cave's
walled forecourt with the Kouretes' bronze shields nailed to the rock and a
stone cradle-altar; and a cave kit shared by the Idaean Cave and the Cave of
Eileithyia, with Amalthea's horn, Epimenides's ledge, and the birth-stone
polished by hands inside its little wall, clay offerings round it.

The caves' rock is the Cretan limestone cliff's own texture (kythera_coast's
stone_px) in the dark `cave` ramp, so a cave reads as the same stone as the
mountain outside, without the sun.
"""
from __future__ import annotations

import math

import numpy as np

import knossa_lib as N
from knossa_land import face_fill, stone
from knossa_lib import ground, grid, struct

SEC_IDA = "ida"
SEC_CAVE = "cave"

ROSE_TO_CAVE = {"rm0": "ck1", "rm1": "ck2", "rm2": "ck3", "rm3": "ck4", "rm4": "ck5",
                "rm5": "ck5", "cv0": "ck0"}


def rock_px(X, Y, dark=0):
    import kythera_coast as Co
    return ROSE_TO_CAVE.get(Co.stone_px(X, Y, dark), "ck0")


def foliage(L, mask, ramp, seed=0, outline="t0", clump=4.0, flowers=None, fl_rate=0,
            periodic=False):
    import kythera_land as KL
    KL.foliage(L, mask, ramp, seed=seed, outline=outline, clump=clump, flowers=flowers,
               fl_rate=fl_rate, periodic=periodic)


# --------------------------------------------------------------------------
# The Ida path: holm oaks, boulders
# --------------------------------------------------------------------------

def oaks():
    names = {"oak_TL": (0, 0), "oak_TR": (1, 0), "oak_BL": (0, 1), "oak_BR": (1, 1),
             "young_top": (2, 0), "young": (2, 1), "boulder": (3, 0), "boulders": (3, 1),
             "acorns": (4, 0), "goat_track": (4, 1)}
    s = struct("oaks", "Holm oaks, boulders and the goat track", 5, 2, SEC_IDA,
               walk=["TTTX.", "XXXX."], names=names,
               notes="The Ida path's goat pastures (on borrowed grass). **The holm oak**, 2 x "
                     "2: `oak_TL` `oak_TR` (its dense evergreen crown, drawn over the player) "
                     "over `oak_BL` `oak_BR` (the crown's skirt and the grey trunk, "
                     "impassable). `young_top` over `young`, a young oak. `boulder` and "
                     "`boulders`, grey limestone on the grass (impassable). Walkable: "
                     "`acorns`, fallen acorns and leaves under an oak; `goat_track`, a narrow "
                     "track worn by hooves (lay it in a line).")
    ground(s, "grass")
    M, Tl = s.M, s.T
    # the holm oak: a broad dark crown, grey trunk, ground shadow
    W, H = 32, 32
    m = np.zeros((H, W), bool)
    for y in range(H):
        for x in range(W):
            d = math.hypot((x - 15.5) / 15.0, (y - 12.0) / 11.5)
            d += 0.08 * math.sin(math.atan2(y - 12, x - 15.5) * 6)
            m[y, x] = d < 1.0 and y < 25
    sub = N.Layer(W, H)
    # trunk and shadow first
    for y in range(20, 31):
        for x in range(13, 19):
            sub.px(x, y, "kt2" if x < 15 else ("kt1" if x < 18 else "t0"))
    for x in range(6, 27):
        for y in (30, 31):
            if sub.get(x, y) is None and abs(x - 16) < 10 - (y - 30) * 3:
                sub.px(x, y, "gd")
    crown = N.Layer(W, H)
    foliage(crown, m, ["my1", "my2", "my3", "my4"], seed=31, clump=4.0)
    for y in range(H):
        for x in range(W):
            if crown.a[y, x, 3]:
                sub.a[y, x] = crown.a[y, x]
    for y in range(H):
        for x in range(W):
            if sub.a[y, x, 3]:
                (Tl if y < 16 else M).a[y, x] = sub.a[y, x]
    # the young oak, 1 x 2
    m2 = np.zeros((32, 16), bool)
    for y in range(32):
        for x in range(16):
            m2[y, x] = math.hypot((x - 7.5) / 7.0, (y - 13.0) / 8.5) < 1.0
    sub2 = N.Layer(16, 32)
    for y in range(20, 30):
        sub2.px(7, y, "kt2")
        sub2.px(8, y, "kt1")
    for x in range(3, 13):
        sub2.px(x, 30, "gd")
    c2 = N.Layer(16, 32)
    foliage(c2, m2, ["my1", "my2", "my3", "my4"], seed=33, clump=3.5)
    for y in range(32):
        for x in range(16):
            if c2.a[y, x, 3]:
                sub2.a[y, x] = c2.a[y, x]
            if sub2.a[y, x, 3]:
                (Tl if y < 16 else M).a[y, 32 + x] = sub2.a[y, x]
    # boulders: grey limestone, lichen
    def boulder(ox, oy, cx_, cy_, rx, ry, seed):
        for y in range(16):
            for x in range(16):
                d = math.hypot((x - cx_) / rx, (y - cy_) / ry) + 0.06 * math.sin(x * 1.7 + seed)
                if d < 1.0:
                    lit = (cx_ - x) * 0.6 + (cy_ - y)
                    c = "cs5" if lit > 3 else ("cs4" if lit > 0 else ("cs3" if lit > -3 else "cs2"))
                    if d > 0.85:
                        c = "cs1"
                    if N.h(x, y, seed) % 17 == 0:
                        c = "my3"
                    M.px(ox + x, oy + y, c)
                elif d < 1.2 and y > cy_:
                    M.px(ox + x, oy + y, "g1")
    boulder(48, 0, 7.5, 8.5, 6.5, 5.5, 1)
    boulder(48, 16, 5, 9, 4.5, 4, 2)
    boulder(48, 16, 11, 10, 3.5, 3, 3)
    # acorns and leaf litter
    for (x, y) in ((3, 4), (9, 3), (12, 9), (5, 11), (8, 7), (2, 13), (13, 13)):
        grid(M, 64 + x, y, ["kk", "ok"], {"k": "kt1", "o": "my1"})
    # goat track: a worn line of bare earth, hoofprints
    for y in range(16):
        for x in range(5, 11):
            if (x in (5, 10) and (y + x) % 3 == 0):
                continue
            M.px(64 + x, 16 + y, "kt2" if (x + y) % 4 else "kt1")
    for (x, y) in ((6, 3), (9, 7), (6, 11), (9, 14)):
        M.px(64 + x, 16 + y, "t0")
    return s


# --------------------------------------------------------------------------
# The cradle shrine: shields on the rock, the cradle-altar
# --------------------------------------------------------------------------

def shield(L, ox, oy, r=6.0, seed=0):
    """A bronze shield nailed to the rock: a boss, concentric rings, a rim."""
    cx_, cy_ = ox + 7.5, oy + 7.5
    for y in range(oy, oy + 16):
        for x in range(ox, ox + 16):
            d = math.hypot(x - cx_, y - cy_)
            if d < r:
                lit = (cx_ - x) + (cy_ - y)
                if d < 1.6:
                    c = "bz3"
                elif abs(d - r * 0.55) < 0.6:
                    c = "bz1"
                elif d > r - 1.0:
                    c = "bz0"
                else:
                    c = "bz2" if lit > -1 else "bz1"
                    if lit > 4 and d < r * 0.5:
                        c = "bz3"
                if (seed and N.h(x, y, seed) % 7 == 0):
                    c = "vg1"
                L.px(x, y, c)
    L.px(int(cx_), int(cy_ - r + 1.5), "ink")     # the nail at the top


def cradle_shrine():
    names = {"shields_L": (0, 0), "shields": (1, 0), "shields_R": (2, 0),
             "altar_L": (0, 1), "altar_R": (1, 1), "offerings": (2, 1), "shield_one": (3, 0),
             "lamp": (3, 1)}
    s = struct("cradle_shrine", "The cradle shrine: the Kouretes' shields, the cradle-altar",
               4, 2, SEC_IDA, walk=["XXXX", "XX.X"], names=names,
               notes="The Idaean Cave's mouth (`MAP_KNOSSA_CRADLE_SHRINE`, SCRIPT.md Part 2), "
                     "where the Kymbash clang: bronze shields nailed to the rock face, the "
                     "Kouretes' who clashed them so Kronos would never hear the baby cry. "
                     "`shields_L` `shields` `shields_R` are a row of the limestone cliff's "
                     "`face` hung with shields (lay them in a `face` row either side of the "
                     "cave's mouth, `shield_one` for a single one); the Throat Spray hides "
                     "behind them. `altar_L` `altar_R`: the stone cradle-altar, a low trough "
                     "of stone rocked on its base, honey cakes and flowers in it (impassable; "
                     "bg event). `offerings` (walkable): clay figures, a pot of honey, a "
                     "bronze pin on the ground before it. `lamp`: an oil lamp on a stone "
                     "(impassable). The altar row stands on borrowed path, the forecourt's beaten floor; its wall is the `terrace` kit.")
    B, M = s.B, s.M
    face_fill(B, 0, 0, 64, 16)
    for (cx, rs) in ((0, ((4, 3, 5.0), (12, 9, 4.5))), (1, ((6, 5, 6.0), (13, 11, 3.5))),
                     (2, ((3, 9, 4.5), (11, 4, 5.0))), (3, ((7.5, 7.5, 6.5),))):
        for (sx, sy, r) in rs:
            shield(M, cx * 16 + int(sx) - 7, int(sy) - 7, r=r, seed=cx + 2)
    # crop shields that spilled over cell edges into neighbours is fine: the
    # face is continuous. The altar: a stone cradle on a plinth, on grass.
    ground(s, "path", [(0, 1), (1, 1), (2, 1), (3, 1)])
    grid(M, 2, 16 + 3, [
        ".kkkkkkkkkkkkkkkkkkkkkkkkkk.",
        "k55555555555555555555555554k",
        "k5yyfyyyyfyyy4yyyfyyyyfyy43k",
        "k5yfyyfyy4yyfyyyyfyy4yyfy43k",
        "k54444444444444444444444433k",
        ".k333333333333333333333332k.",
        "..k3333333333333333333332k..",
        "...kkk22222222222222kkkk....",
        "....k1222222222222221k......",
        "....k1111111111111111k......",
        "....kkkkkkkkkkkkkkkkkk......",
    ], {"k": "cs0", "5": "cs5", "4": "cs4", "3": "cs3", "2": "cs2", "1": "cs1",
        "y": "cs4", "f": "my3"})
    # honey cakes in the cradle: drawn over in green-free stone tones
    # (the stone group carries no honey; the cakes are pale stone loaves)
    for (x, y) in ((6, 21), (14, 22), (22, 21)):
        grid(M, x, y, ["55", "44"], {"5": "cs5", "4": "cs3"})
    # offerings: clay figures, a honey pot, a pin (minoan group, middle layer)
    fig = [".k.k.", "k2.2k", ".k1k.", ".k1k.", "kk1kk"]
    for (fx, fy) in ((2, 5), (10, 7)):
        grid(M, 32 + fx, 16 + fy, fig, {"k": "mt0", "1": "mt1", "2": "mt2"})
    grid(M, 32 + 6, 16 + 9, [".kk.", "kmmk", "k11k", ".kk."], {"k": "mt0", "m": "mo1", "1": "mt1"})
    for x in range(3, 9):
        M.px(32 + x, 16 + 14, "mo1")
    M.px(32 + 9, 16 + 14, "mo0")
    # the lamp on a stone
    grid(M, 48 + 3, 16 + 3, [
        "....yy....",
        "...yYy....",
        ".kkkkkkk..",
        "k2111110k.",
        ".kkkkkkk..",
    ], {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0", "y": "mo1", "Y": "mo2"})
    grid(M, 48 + 2, 16 + 9, [
        ".kkkkkkkkk.",
        "k555544433k",
        "k444333322k",
        ".kkkkkkkkk.",
    ], {"k": "cs0", "5": "cs5", "4": "cs4", "3": "cs3", "2": "cs2"})
    return s


# --------------------------------------------------------------------------
# The caves
# --------------------------------------------------------------------------

FLOOR = [
    "................",
    "..o.......p.....",
    "......dd........",
    "............o...",
    ".p......d.......",
    "...........dd...",
    "....o...........",
    "..........p.....",
    ".dd.............",
    "......o.....d...",
    "..............o.",
    "...p....dd......",
    "................",
    "..........o.....",
    "....d...........",
    ".........p...o..",
]


def floor_px(x, y, seed=0):
    """The cave floor: packed earth, smooth, a few pebbles and dark hollows."""
    ch = FLOOR[(y + 5 * seed) % 16][(x + 3 * seed) % 16]
    return {"o": "ck3", "p": "ck4", "d": "cm0"}.get(ch, "cm1")


def cave_kit():
    names = {"rock": (0, 0), "face_L": (1, 0), "face": (2, 0), "face_b": (3, 0),
             "face_R": (4, 0), "side_W": (5, 0), "side_E": (6, 0), "dark": (7, 0),
             "floor": (0, 1), "floor_b": (1, 1), "path": (2, 1), "path_H": (3, 1),
             "in_NW": (4, 1), "in_NE": (5, 1), "out_SW": (6, 1), "out_SE": (7, 1),
             "stalagmite": (0, 2), "stalagmites": (1, 2), "col_top": (2, 2), "col": (2, 3),
             "pool_L": (3, 2), "pool_R": (4, 2), "ledge_L": (5, 2), "ledge_R": (6, 2),
             "rubble": (7, 2), "exit": (0, 3), "glow": (1, 3), "drip": (3, 3), "bones": (4, 3),
             "steps": (5, 3), "shelf": (6, 3), "crack": (7, 3)}
    s = struct("cave", "The cave kit: rock, faces, floors", 8, 4, SEC_CAVE,
               walk=["XXXXXXXX", "....XXXX", "XXXXXXXX", ".X.X.X.X"], names=names,
               notes="The Idaean Cave and the Cave of Eileithyia: Ida's limestone in the dark. "
                     "**Rock**: `rock` is the cave's mass seen from above (the border, and "
                     "every cell that is not cave); a wall facing you is a `face` row under "
                     "it (`face_b` breaks it up; `face_L` / `face_R` end it); `side_W` (rock "
                     "to the west) and `side_E` edge the floor; `in_NW` / `in_NE` turn a face "
                     "into a side, `out_SW` / `out_SE` finish a rock mass's foot. `dark`: a "
                     "passage on into the dark (impassable, or a warp). **Floor** (walkable): "
                     "`floor`, `floor_b`, and the path worn by pilgrims' feet, `path` (north-"
                     "south) and `path_H`; `steps` cut in the floor where it drops (walkable); "
                     "`glow`, daylight fallen in from the mouth; `drip`, a puddle under a "
                     "dripping stalactite; `bones`, old offerings' bones (walkable). "
                     "**Features** (impassable): `stalagmite`, `stalagmites`, `col_top` over "
                     "`col` (a column where stalactite met stalagmite, its top drawn over the "
                     "player), `pool_L` `pool_R` (a still black pool), `ledge_L` `ledge_R` "
                     "(a rock shelf: Epimenides sleeps on it), `rubble`, `shelf` (a low rock "
                     "shelf for offerings), `crack` (a narrow fissure). `exit`: the cave mouth "
                     "seen from inside, daylight beyond (`MB_SOUTH_ARROW_WARP`, the warp out).")
    B, M, Tl = s.B, s.M, s.T
    # rock mass from above: dark, mottled
    for y in range(16):
        for x in range(16):
            k = N.h(x, y, 4)
            B.px(x, y, "ck1" if k % 5 else ("ck0" if k % 2 else "ck2"))

    def face(ox, oy, end=None, b=0):
        for y in range(16):
            for x in range(16):
                if end == "L" and x < 5 - y // 4:
                    B.px(ox + x, oy + y, "ck1")
                    continue
                if end == "R" and x > 10 + y // 4:
                    B.px(ox + x, oy + y, "ck1")
                    continue
                if y < 2:
                    c = "ck1" if y == 0 else "ck3"
                elif y > 13:
                    c = floor_px(x, y) if y == 15 else "ck1"
                else:
                    c = rock_px(ox + x + 5 * b, oy + y)
                B.px(ox + x, oy + y, c)
    face(16, 0, "L")
    face(32, 0)
    face(48, 0, b=1)
    face(64, 0, "R")
    # sides: rock to one side, floor to the other
    for (ox, side) in ((80, "W"), (96, "E")):
        for y in range(16):
            for x in range(16):
                xx = x if side == "W" else 15 - x
                e = 4 + int(round(math.sin(y / 2.5) * 0.8))
                if xx < e:
                    c = "ck1"
                elif xx < e + 3:
                    c = rock_px(ox + x, y, 1 if side == "E" else 0)
                elif xx == e + 3:
                    c = "ck2"
                else:
                    c = floor_px(x, y)
                B.px(ox + x, y, c)
    # dark passage
    for y in range(16):
        for x in range(16):
            B.px(112 + x, y, "ck0" if 3 < x < 12 and y > 3 else rock_px(112 + x, y))
    # floors
    for (ox, seed) in ((0, 0), (16, 3)):
        for y in range(16):
            for x in range(16):
                B.px(ox + x, 16 + y, floor_px(x, y, seed))
    for (ox, vertical) in ((32, True), (48, False)):
        for y in range(16):
            for x in range(16):
                u = x if vertical else y
                c = floor_px(x, y)
                if 5 <= u <= 10:
                    # feet have worn the floor smooth and pale down the middle
                    c = "cs3" if (x + y) % 2 == 0 and 6 <= u <= 9 else "cm1"
                    if u in (5, 10):
                        c = "cm0" if (x + y) % 3 else "cm1"
                B.px(ox + x, 16 + y, c)
    # inner corners and outer feet
    for (ox, side) in ((64, "NW"), (80, "NE")):
        for y in range(16):
            for x in range(16):
                xx = x if side == "NW" else 15 - x
                if y < 14 and xx < 5:
                    c = "ck1"
                elif y < 14 and xx < 8:
                    c = rock_px(ox + x, 16 + y, 1)
                elif y < 2:
                    c = "ck1"
                elif y < 14:
                    c = rock_px(ox + x, 16 + y)
                else:
                    c = floor_px(x, y)
                B.px(ox + x, 16 + y, c)
    for (ox, side) in ((96, "SW"), (112, "SE")):
        for y in range(16):
            for x in range(16):
                xx = x if side == "SW" else 15 - x
                if xx < 5 and y < 6:
                    c = "ck1"
                elif xx < 5 and y < 14:
                    c = rock_px(ox + x, 16 + y)
                else:
                    c = floor_px(x, y)
                B.px(ox + x, 16 + y, c)
    # features on the floor
    for cx in range(8):
        for y in range(32, 64):
            for x in range(cx * 16, cx * 16 + 16):
                B.px(x, y, floor_px(x, y, cx))

    def mite(L, ox, oy, h_, w_, dx=0, foot=15):
        for y in range(h_):
            half = w_ * (y + 1) / h_ / 2
            for x in range(16):
                d = x + 0.5 - 8 - dx
                if abs(d) <= half:
                    c = "ck5" if d < -half / 3 else ("ck4" if d < half / 3 else "ck3")
                    L.px(ox + x, oy + foot - h_ + y, c)
                elif abs(d) <= half + 1 and y > 1:
                    L.px(ox + x, oy + foot - h_ + y, "ck2")
    mite(M, 0, 32, 12, 7)
    mite(M, 16, 32, 10, 5, dx=-1)
    mite(M, 16, 32, 6, 4, dx=-5, foot=14)
    mite(M, 16, 32, 5, 3, dx=4, foot=13)
    # the column, 1 x 2: a stalactite meeting a stalagmite
    for y in range(32):
        t = y / 31.0
        half = 2.2 + 3.2 * abs(t - 0.45) ** 1.4 * 2
        for x in range(16):
            d = x + 0.5 - 8
            if abs(d) <= half:
                c = "ck5" if d < -half / 3 else ("ck4" if d < half / 3 else "ck3")
                (Tl if y < 16 else M).px(32 + x, 32 + y, c)
            elif abs(d) <= half + 1:
                (Tl if y < 16 else M).px(32 + x, 32 + y, "ck1")
    # the pool, 2 x 1
    for y in range(16):
        for x in range(32):
            d = math.hypot((x - 15.5) / 14.0, (y - 8.0) / 6.0)
            if d < 0.82:
                c = "ck0" if (x + y) % 9 else "ck2"
                if d < 0.5 and (x - y) % 11 == 0:
                    c = "ck3"
                M.px(48 + x, 32 + y, c)
            elif d < 1.0:
                M.px(48 + x, 32 + y, "ck2" if y < 8 else "ck4")
    # the ledge, 2 x 1: a rock shelf a man could sleep on
    grid(M, 80, 32 + 2, [
        "..kkkkkkkkkkkkkkkkkkkkkkkkkkk...",
        ".k666666666666666666666666655k..",
        "k55555555555555555555555555544k.",
        "k55545555555555555555545555543k.",
        "k44444444444444444444444444433k.",
        ".k33333333333333333333333333322k",
        "..k2222222222222222222222222221k",
        "...kkkkkkkkkkkkkkkkkkkkkkkkkkkk.",
    ], {"k": "ck1", "6": "ck6", "5": "ck5", "4": "ck4", "3": "ck3", "2": "ck2"})
    # rubble
    for (rx, ry) in ((1, 5), (7, 2), (9, 9), (3, 10)):
        grid(M, 112 + rx, 32 + ry, [".kkk.", "k554k", "k432k", ".kkk."],
             {"k": "ck1", "5": "ck5", "4": "ck4", "3": "ck3", "2": "ck2"})
    # the exit: the mouth from inside, daylight
    for y in range(16):
        for x in range(16):
            d = abs(x - 7.5)
            if y < 10 and d < 5 - (9 - y) * 0.3:
                c = "fw" if d < 3 else "cs4"
            elif d < 6:
                c = "cs3" if y >= 10 else rock_px(x, 48 + y)
            else:
                c = rock_px(x, 48 + y)
            B.px(x, 48 + y, c)
    # glow: daylight on the floor
    for y in range(16):
        for x in range(16):
            c = B.get(16 + x, 48 + y)
            if y >= 11 or (y >= 6 and (x + y) % (12 - y if y < 11 else 1) == 0):
                c = {"cm0": "cm1", "cm1": "cs3", "ck3": "cs4", "ck4": "cs4"}.get(c, c)
            B.px(16 + x, 48 + y, c)
    # col's lower cell is (2, 3): already drawn. drip: a puddle
    for y in range(16):
        for x in range(16):
            d = math.hypot((x - 7.5) / 5.0, (y - 9) / 3.0)
            if d < 1.0:
                B.px(48 + x, 48 + y, "ck0" if d < 0.7 else "ck2")
    B.px(48 + 7, 48 + 3, "ck4")
    B.px(48 + 7, 48 + 5, "ck4")
    # bones: old offerings
    grid(B, 64 + 3, 48 + 5, ["5...5....", "54445..5.", "5...5.545", "......5.."],
         {"5": "ck6", "4": "ck5"})
    # steps cut in the floor
    for y in range(16):
        for x in range(16):
            k = y % 5
            B.px(80 + x, 48 + y, ("cs3", "cm1", "cm1", "cm0", "ck1")[k])
    # a low shelf of rock for offerings
    grid(M, 96 + 1, 48 + 4, [
        ".kkkkkkkkkkkk.",
        "k666665555554k",
        "k554444444443k",
        ".k3333333332k.",
        "..kkkkkkkkkk..",
    ], {"k": "ck1", "6": "ck6", "5": "ck5", "4": "ck4", "3": "ck3", "2": "ck2"})
    # a crack: a narrow dark fissure in the floor
    for y in range(16):
        x = int(7 + 2.5 * math.sin(y / 3.0))
        B.px(112 + x, 48 + y, "ck0")
        B.px(112 + x + 1, 48 + y, "ck0" if y % 3 else "ck1")
    s.walk = ["XXXXXXXX", "....XXXX", "XXXXXXXX", "...X..X."]
    s.walk[3] = "." + "." + "X" + "." + "." + "." + "X" + "X"
    s.behaviors = {(0, 3): "MB_SOUTH_ARROW_WARP"}
    return s


def cave_shrines():
    names = {"horn_TL": (0, 0), "horn_TR": (1, 0), "horn_BL": (0, 1), "horn_BR": (1, 1),
             "stone_TL": (2, 0), "stone_TR": (3, 0), "stone_BL": (2, 1), "stone_BR": (3, 1)}
    s = struct("cave_shrines", "Amalthea's horn, Eileithyia's birth-stone", 4, 2, SEC_CAVE,
               walk=["XXXX", "XXXX"], names=names,
               notes="On the cave floor, both 2 x 2 and impassable. **Amalthea's horn** "
                     "(`horn_*`), at the back of the Idaean Cave: a great goat's horn lying "
                     "on a rock, brimming with fruit that never rots (bg event: place "
                     "Capricornus). **The birth-stone** (`stone_*`), at the end of the Cave of "
                     "Eileithyia: a stalagmite polished smooth by hands inside its little "
                     "stone wall, tiny clay babies and honey cakes left round it (bg event: "
                     "Hera Favor; Gennaia stands by it).")
    B, M = s.B, s.M
    for y in range(32):
        for x in range(64):
            B.px(x, y, floor_px(x % 16, y % 16, x // 16))
    # the horn: a long curved ivory horn, fruit spilling from its mouth
    for t in np.linspace(0, 1, 160):
        cx_ = 6 + 22 * t
        cy_ = 20 - 12 * math.sin(t * math.pi * 0.85) + 4 * t
        r = 1.2 + 4.6 * t
        for y in range(int(cy_ - r) - 1, int(cy_ + r) + 2):
            for x in range(int(cx_ - r) - 1, int(cx_ + r) + 2):
                d = math.hypot(x - cx_, y - cy_)
                if d < r:
                    c = "ck6" if y < cy_ - r * 0.3 else ("cs4" if y < cy_ + r * 0.3 else "cs3")
                    if int(t * 20) % 3 == 0 and d > r * 0.7:
                        c = "cs3"
                    M.px(x, y, c)
    # its mouth, dark, and the fruit tumbling out
    for y in range(12, 26):
        for x in range(26, 32):
            if math.hypot((x - 29) / 2.5, (y - 18.5) / 5.5) < 1.0:
                M.px(x, y, "ck1")
    for (fx, fy, c) in ((28, 22, "mt1"), (24, 26, "mo1"), (20, 27, "mt1"), (16, 27, "mo1"),
                        (22, 24, "fw"), (12, 27, "mt1"), (26, 26, "fw")):
        grid(M, fx, fy, [".cc.", "cccc", ".cc."], {"c": c})
        M.px(fx + 1, fy, "ck6" if c != "fw" else "cs5")
    # outline the horn
    hn = N.Layer(64, 32)
    hn.a[:] = M.a
    for y in range(32):
        for x in range(32):
            if hn.a[y, x, 3] and hn.get(x, y) in ("ck6", "cs4", "cs3"):
                for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < 32 and 0 <= y + dy < 32 and not hn.a[y + dy, x + dx, 3]:
                        M.px(x, y, "ck2")
                        break
    # the birth-stone: a stalagmite polished smooth, its little wall, offerings
    ox = 32
    for y in range(32):
        for x in range(32):
            d = math.hypot((x - 15.5) / 13.5, (y - 21.0) / 8.5)
            if 0.82 < d < 1.0 and y > 13:
                c = "cs4" if y < 21 else "cs3"
                if (x + y) % 6 == 0:
                    c = "ck3"
                M.px(ox + x, y, c)
    for y in range(2, 26):
        t = (y - 2) / 24.0
        half = 1.5 + 5.0 * t ** 1.3
        for x in range(32):
            d = x + 0.5 - 16
            if abs(d) <= half:
                c = "ck6" if d < -half * 0.2 else ("ck5" if d < half * 0.5 else "ck4")
                if abs(d + half * 0.45) < 0.8 and y > 6:
                    c = "fw"                 # the shine of hands
                M.px(ox + x, y, c)
            elif abs(d) <= half + 1:
                M.px(ox + x, y, "ck2")
    for (fx, fy) in ((7, 18), (23, 19), (10, 24), (21, 25)):
        grid(M, ox + fx, fy, [".m.", "mmm", ".m."], {"m": "mt1"})
    for (fx, fy) in ((14, 27), (18, 27)):
        grid(M, ox + fx, fy, ["oo", "oo"], {"o": "mo1"})
    return s


def build():
    return [oaks(), cradle_shrine(), cave_kit(), cave_shrines()]
