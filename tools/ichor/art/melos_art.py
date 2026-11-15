"""Melos, the open sea of Routes 22 and 23, Antikythera's islet, and Echo's sea
caves: the pieces only the gTileset_Melos secondary carries.

  - The obsidian slope: black volcanic glass over the hillside, soft-edged
    (all 47 shapes), glinting now and then (the `glint` animation), with the
    old knapping pits and Theion's sacks.
  - Klima's boathouses at the waterline: whitewashed, with sea doors painted
    red, blue or green over a short slip, a land door at the side.
  - A well with its trough, vines on their trellis, grey tuff terrace walls
    with the niche where the armless goddess stands.
  - The sea: stakes marking the trireme lane, a sunken capital, Anydros's bare
    rock and its dead fig, the wreck's ribs on the Antikythera reef.
  - Echo's sea caves: dark pink rock walls and ceiling, a sandy floor, cave
    pools, the shaft of light from the Speaking Hall's roof crack, the low arch
    of the sea mouth, the stair up to the spring, a brazier cold and lit.
"""
from __future__ import annotations

import math

import numpy as np

import kythera_lib as K
from kythera_lib import anim_layer, ground, put, struct
from kythera_coast import bubbles, foam_ring, rock_blob, stone_px, wob

SEC_M = "melos"
SEC_S = "sea"
SEC_C = "cave"
GRASS = 0x001


def grass_px(X, Y):
    rgb = tuple(int(v) for v in K.aethos(GRASS)[Y % 16, X % 16])
    return K.A.RGB2NAME[rgb]


# --------------------------------------------------------------------------
# The obsidian slope
# --------------------------------------------------------------------------

def _obsidian_tex():
    """16x16 periodic: glassy black facets with conchoidal sheen lines."""
    t = {}
    for y in range(16):
        for x in range(16):
            # facets: angular cells shaded by a fake normal
            fx = (x + (y // 4) * 3) % 8
            fy = y % 4
            k = K.h(x // 4 + (y // 4) * 5, y // 4, 41)
            base = ("ob0", "ob1", "ob1", "ob2")[k % 4]
            if fy == 0 and fx < 6:
                base = "ob2" if base != "ob2" else "ob3"
            if fx == 7:
                base = "ob0"
            t[(x, y)] = base
    # curved sheen arcs (the glass's ripples)
    for (cx, cy, r) in ((5, 6, 4.5), (12, 13, 3.5)):
        for a in np.linspace(math.pi * 1.05, math.pi * 1.6, 9):
            x = int(round(cx + r * math.cos(a))) % 16
            y = int(round(cy + r * math.sin(a))) % 16
            t[(x, y)] = "ob3"
    return t


def obsidian():
    from agros_ground import blob_keys, halo, ring, visible
    keys = blob_keys()
    w = 8
    hh = (len(keys) + w - 1) // w
    names = {k: (i % w, i // w) for i, k in enumerate(keys)}
    s = struct("obsidian", "The obsidian slope, soft-edged", w, hh, SEC_M,
               walk=["." * w] * hh, names=names,
               notes="Melos's hillside of black volcanic glass, as all 47 soft-edge shapes on aethos "
                     "grass (kythera_lib.blob_key gives a cell's key from a mask), its edge broken "
                     "into scree. Walkable. The full interior is `1|11111111`; it glints now and "
                     "then in the sun (the `glint` animation).")
    B = s.B
    tex_ = _obsidian_tex()

    def paint(L, ox, oy, key):
        vis, _ = visible(key, margin=1.5, radius=2.5, amp=1.6, seed=7.7, jag=1.0)
        K.tex(L, GRASS, ox, oy, 16, 16)
        for y in range(16):
            for x in range(16):
                if vis[y, x]:
                    L.px(ox + x, oy + y, tex_[((ox + x) % 16, (oy + y) % 16)])
        for y, x in np.argwhere(ring(vis)):
            L.px(ox + x, oy + y, "l0" if (x + y) % 3 else "ob1")
        for y, x in np.argwhere(halo(vis)):
            if (x * 7 + y * 3) % 5 == 0:
                L.px(ox + x, oy + y, "ob1" if (x + y) % 2 else "l1")
    for k, (cx, cy) in names.items():
        paint(B, cx * 16, cy * 16, k)
    for i in range(len(keys), w * hh):
        paint(B, (i % w) * 16, (i // w) * 16, keys[-1])
    # glints on the full interior: a star of light, now and then
    fr = anim_layer(s, "glint", 3, layer="bottom")
    cx, cy = names["1|11111111"]
    for f, (gx, gy) in ((0, (4, 9)), (1, (11, 4))):
        L = fr[f]
        X, Y = cx * 16 + gx, cy * 16 + gy
        put(L, X - 1, Y - 1, [".w.", "wbw", ".w."] if f == 0 else ["..w..", ".bwb.", "wwbww", ".bwb.", "..w.."],
            {"w": "w0", "b": "b4"})
    K.settle(s, "glint", [(cx, cy)])
    return s


def obsidian_bits():
    names = {"pit": (0, 0), "pit_b": (1, 0), "flakes": (2, 0), "sacks": (3, 0), "core": (4, 0)}
    s = struct("obsidian_bits", "Knapping pits, flakes and Theion's sacks", 5, 1, SEC_M,
               walk=["...X."], names=names,
               notes="On the obsidian (each is drawn on the slope's full interior texture): `pit` and "
                     "`pit_b`, old knapping pits, shallow hollows ringed with waste flakes (the dig "
                     "spots); `flakes`, a scatter of chips; `sacks`, Theion's sacks of obsidian "
                     "(impassable); `core`, a big worked core lying on the glass.")
    B = s.B
    tex_ = _obsidian_tex()
    for i in range(5):
        for y in range(16):
            for x in range(16):
                B.px(i * 16 + x, y, tex_[(x, y)])
    for (ox, r) in ((0, 5.5), (16, 4.5)):
        for y in range(16):
            for x in range(16):
                d = math.hypot((x - 7.5) / r, (y - 8) / (r * 0.8))
                if d < 1:
                    c = "l0" if d > 0.75 else ("ob0" if y < 8 else "l0")
                    if d < 0.5:
                        c = "l1" if (x + y) % 3 else "l0"
                    B.px(ox + x, y, c)
        for (fx, fy) in ((1, 2), (12, 3), (2, 13), (13, 12), (7, 1)):
            put(B, ox + fx, fy, ["3.", "13"], {"3": "ob3", "1": "ob2"})
    for (fx, fy) in ((2, 3), (8, 2), (12, 7), (4, 10), (10, 12), (1, 14), (14, 14)):
        put(B, 32 + fx, fy, ["w3", "31"], {"w": "b4", "3": "ob3", "1": "ob2"})
    put(B, 48 + 1, 2, [
        "..kkkk...kkkk..",
        ".k3333k.k3333k.",
        "k333333k333333k",
        "k333333k333333k",
        "k33pp33k33pp33k",
        "k3pppp3k3pppp3k",
        "k33pp33k33pp33k",
        "k333333k333333k",
        ".k3333k.k3333k.",
        "..kkkk...kkkk..",
        "...............",
        "..kkkkkkkkkk...",
    ], {"k": "kt1", "3": "p1", "p": "ob1"})
    put(B, 64 + 3, 4, [
        "..kkkkk...",
        ".k33bb2k..",
        "k3bbbb22k.",
        "kbbbbb222k",
        ".k2222211k",
        "..kkkkkkk.",
    ], {"k": "ob0", "3": "ob3", "b": "ob2", "2": "ob1", "1": "ob0"})
    return s


# --------------------------------------------------------------------------
# Klima's boathouses
# --------------------------------------------------------------------------

def boathouses():
    names = {"R_L": (0, 0), "R_M": (1, 0), "R_R": (2, 0),
             "U_L": (0, 1), "U_balcony": (1, 1), "U_R": (2, 1),
             "land_door": (0, 2), "sea_red_L": (1, 2), "sea_red_R": (2, 2),
             "sea_blue_L": (3, 2), "sea_blue_R": (4, 2), "sea_green_L": (5, 2), "sea_green_R": (6, 2),
             "slip_L": (1, 3), "slip_R": (2, 3), "U_balcony_blue": (3, 1), "U_balcony_green": (4, 1)}
    s = struct("boathouse", "Klima's boathouses", 7, 4, SEC_M,
               walk=["XXXXXXX", "XXXXXXX", "DXXXXXX", "XXX...."], names=names,
               notes="Melos's boathouses at the waterline, whitewashed, built into the shore: a roof "
                     "row (`R_*`), an upper floor with a painted balcony door (`U_balcony`, "
                     "`U_balcony_blue`, `U_balcony_green`), and on the ground floor a pair of sea "
                     "doors over the boat (`sea_red_L` `sea_red_R`, `sea_blue_*`, `sea_green_*`) "
                     "with the family's `land_door` beside them (`MB_NON_ANIMATED_DOOR`). Below the "
                     "sea doors, `slip_L` `slip_R` run a short stone slip into the sea (borrowed "
                     "sea). A boathouse is 3 wide: `land_door` then a pair of sea doors; match the "
                     "balcony's color to the doors'.")
    ground(s, "sea", [(1, 3), (2, 3)])
    ground(s, "sand", [(0, 3), (3, 3), (4, 3), (5, 3), (6, 3)])
    B, M = s.B, s.M
    from kythera_town import door, roof_cell, wall_cell, window
    for cx, side in ((0, "L"), (1, "M"), (2, "R")):
        roof_cell(B, cx * 16, 0, side)
    for cx in range(3, 7):
        roof_cell(B, cx * 16, 0, "M")
    for cx, side in ((0, "L"), (1, "M"), (2, "R"), (3, "M"), (4, "M"), (5, "M"), (6, "M")):
        wall_cell(B, cx * 16, 16, "U", side)
        wall_cell(B, cx * 16, 32, "G", side)
    # balconies: a painted door and a little wooden railing
    for (cx, col, dark) in ((1, "rs1", "pf2"), (3, "b1", "ab0"), (4, "kgr", "my2")):
        ox = cx * 16
        put(B, ox + 3, 16 + 2, [
            "kkkkkkkkkk",
            "kAaAaAaAak",
            "kaAaAaAaAk",
            "kAaAaAaAak",
            "kaAaAaAaAk",
            "kAaAaAaAak",
            "kaAaAaAaAk",
            "kkkkkkkkkk",
        ], {"k": "cw3", "A": col, "a": dark})
        for x in range(ox + 1, ox + 15):
            B.px(x, 16 + 10, col)
            B.px(x, 16 + 13, col)
        for x in range(ox + 1, ox + 15, 3):
            for y in range(16 + 10, 16 + 14):
                B.px(x, y, col)
        for x in range(ox + 1, ox + 15):
            B.px(x, 16 + 14, "cw2")
    window(B, 0, 16)
    window(B, 32, 16)
    # the land door (blue, white frame), and pairs of arched sea doors
    door(B, 0, 32, pink=False)
    for (cx, col, dark) in ((1, "rs1", "pf2"), (3, "b1", "ab0"), (5, "kgr", "my2")):
        for half in (0, 1):
            ox = (cx + half) * 16
            for y in range(32 + 2, 48):
                for x in range(16):
                    xx = x if half == 0 else 15 - x
                    if xx < 2:
                        continue
                    yy = y - 32
                    # arch: the doors' top curves down at the outer edges
                    arch = 2 + max(0, 6 - xx) * 0.6
                    if yy < arch:
                        continue
                    if yy < arch + 1 or xx == 2:
                        c = "cw3"
                    else:
                        c = col if (xx // 2) % 2 else dark
                        if yy in (8, 13):
                            c = dark
                    B.px(ox + x, y, c)
            if half == 0:
                for y in range(32 + 8, 48):
                    B.px(ox + 15, y, "ink")
    # the short slips below the sea doors
    for cx in (1, 2):
        ox = cx * 16
        for y in range(0, 10):
            for x in range(16):
                xx = x if cx == 1 else 15 - x
                if xx < 2:
                    continue
                c = "kr2" if (x + y) % 5 else "kr1"
                if y in (0,):
                    c = "kr1"
                if y > 6 and (x + y) % 2:
                    c = None
                if c:
                    M.px(ox + x, 48 + y, c)
    return s


# --------------------------------------------------------------------------
# The well, vines, grey terrace walls and the niche
# --------------------------------------------------------------------------

def tuff_px(X, Y):
    """Melos's grey-white tuff, laid in rough courses."""
    x, y = X % 16, Y % 16
    course = y // 4
    if y % 4 == 3:
        return "kr1"
    if (x + 5 * course) % 7 == 0:
        return "kr1"
    if y % 4 == 0:
        return "kr3"
    return "kr2" if (x * 3 + y) % 7 else "kr3"


def village():
    names = {"well": (0, 0), "trough": (1, 0), "vine": (2, 0), "vine_end": (3, 0),
             "wall_L": (0, 1), "wall": (1, 1), "wall_R": (2, 1), "niche": (3, 1),
             "wall_steps": (4, 1), "top": (1, 2), "top_L": (0, 2), "top_R": (2, 2),
             "top_niche": (3, 2), "top_steps": (4, 2), "terrace_lip": (4, 0)}
    s = struct("village", "The well, vines, and Melos's tuff terraces", 5, 3, SEC_M,
               walk=["XXXX.", "XXXX.", "....."], names=names,
               notes="On borrowed path and grass. `well`, a round stone well with a bucket, and "
                     "`trough`, its stone trough (the girl at the well; both impassable). `vine` "
                     "and `vine_end`, vines on a trellis for the terraces (with aethos tall grass for "
                     "the barley). The terrace walls are Melos's grey tuff: a `top_*` row (the upper "
                     "terrace's edge, walkable) over a wall row `wall_L` `wall` `wall_R`; "
                     "`wall_steps` under `top_steps` is a stair through it. `niche` is the terrace-"
                     "wall niche with its low plinth where the armless statue stands (an object, "
                     "16x32: place her on the niche cell); the mirror facing her is an object too. "
                     "`terrace_lip` is a lone stretch of coping on grass (walkable).")
    ground(s, "path", [(0, 0), (1, 0)])
    ground(s, "grass", [(2, 0), (3, 0), (4, 0), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (0, 1),
                        (2, 1)])
    B, M = s.B, s.M
    # well: a round kerb with a dark mouth, a wooden frame and bucket
    put(M, 1, 1, [
        "....kkkkkk....",
        "..kk322223kk..",
        ".k3222222223k.",
        "k32200000022k.",
        "k22000000002k.",
        "k22000000002k.",
        "k32200000022k.",
        ".k2222222221k.",
        ".k1222222211k.",
        ".k1111111111k.",
        "..kkkkkkkkkk..",
    ], {"k": "kr0", "3": "kr3", "2": "kr2", "1": "kr1", "0": "b3"})
    for y in range(3, 8):
        M.px(5, y, "kr0")
        M.px(6, y, "kq1")
    put(M, 4, 0, ["wwww"], {"w": "l1"})
    put(M, 16 + 1, 4, [
        "kkkkkkkkkkkkkk",
        "k33333333333kk",
        "k3qqqqqqqqqq1k",
        "k3qkkqqqqqqq1k",
        "k3qqqqqqqqqq1k",
        "k1111111111111",
        ".kkkkkkkkkkkk.",
    ], {"k": "kr0", "3": "kr3", "q": "kq1", "1": "kr1"})
    # vines: two posts, a wire between them, the vine trained along it with
    # bunches of pale grapes, its shadow on the grass
    import kythera_land as La
    for (ox, end) in ((32, False), (48, True)):
        right = 11 if end else 16
        for y in range(11, 15):
            for x in range(1, right):
                if (x + y) % 2 == 0 or y == 13:
                    M.px(ox + x, y, "gd" if y > 11 else "g1")
        for px_ in ((2,) if not end else (2, 10)):
            for y in range(2, 14):
                M.px(ox + px_, y, "kt1")
                M.px(ox + px_ + 1, y, "kt2" if y < 12 else "kt1")
        canopy = np.zeros((16, 16), bool)
        for y in range(1, 10):
            for x in range(0, right):
                if 2 + 1.5 * math.sin(x / 2.0) <= y <= 8 + math.sin(x / 3.0 + 1):
                    canopy[y, x] = True
        tmp = K.Layer(16, 16)
        La.foliage(tmp, canopy, ("my1", "my1", "my2", "my3"), seed=21 + ox, outline="t0")
        for y in range(16):
            for x in range(16):
                if tmp.a[y, x, 3]:
                    M.px(ox + x, y, tmp.get(x, y))
        for (gx, gy) in ((5, 7), (9, 8), (13, 6)):
            if gx < right - 1:
                put(M, ox + gx, gy, ["44", "34", ".3"], {"4": "my4", "3": "my3"})
    # tuff walls
    for cx, end in ((0, "L"), (1, None), (2, "R"), (3, "N"), (4, "S")):
        ox, oy = cx * 16, 16
        tgt = M if end in ("L", "R") else B
        for y in range(16):
            for x in range(16):
                if end == "L" and x < 3:
                    continue
                if end == "R" and x > 12:
                    continue
                c = tuff_px(ox + x, oy + y)
                if y < 2:
                    c = "w0" if y == 0 else "kr3"
                tgt.px(ox + x, oy + y, c)
    put(B, 48 + 3, 16 + 2, [
        "...1111...",
        "..122221..",
        ".12000021.",
        "1200000021",
        "1200000021",
        "1200000021",
        "1200000021",
        "1201111021",
        "1213333121",
        "1213333121",
        "1211111121",
        "1111111111",
    ], {"1": "kr1", "2": "kr2", "0": "kr0", "3": "w0"})
    for i, y in enumerate(range(0, 16, 4)):
        for x in range(2, 14):
            for k, c in enumerate(("w0", "kr3", "kr2", "kr1")):
                B.px(64 + x, 16 + y + k, c)
    # the tops: coping at the foot of each cell
    for cx in range(5):
        ox, oy = cx * 16, 32
        for x in range(16):
            if cx == 0 and x < 3 or cx == 2 and x > 12:
                continue
            if cx == 4 and 2 <= x <= 13:
                M.px(ox + x, oy + 15, "kr3")
                M.px(ox + x, oy + 14, "w0")
                continue
            M.px(ox + x, oy + 14, "kr3")
            M.px(ox + x, oy + 15, "w0")
    for x in range(16):
        M.px(64 + x, 14, "kr3")
        M.px(64 + x, 15, "w0")
    s.ground[(4, 0)] = "grass"
    return s


# --------------------------------------------------------------------------
# The open sea: stakes, Anydros, the wreck
# --------------------------------------------------------------------------

def sea_marks():
    s = struct("sea_marks", "Anydros's rock and the Antikythera wreck", 5, 2, SEC_S,
               walk=["XXXXX", "XXXXX"], names={"anydros": (0, 0), "wreck": (2, 0)},
               notes="On borrowed sea, with breathing foam (animated). `anydros` (2 x 2): Anydros, "
                     "the bare rock on Route 22 with one dead fig tree clinging to it. `wreck` (3 x "
                     "2): the old wreck's ribs standing out of the water on the Antikythera reef, a "
                     "spar across them. Both impassable.")
    ground(s, "sea")
    M = s.M
    frames = anim_layer(s, "surf", 3)
    allf = [M] + frames
    sub = K.Layer(M.w, M.h)
    pts = [(3, 22), (5, 14), (10, 8), (17, 6), (24, 9), (28, 16), (29, 24), (24, 28), (12, 29), (5, 27)]
    for L in allf:
        rock_blob(L, 0, 0, pts, seed=3)
    sub.poly(pts, "kr0")
    # the dead fig: grey twisting branches
    for L in allf:
        for (x0, y0, x1, y1) in ((15, 13, 15, 4), (15, 8, 10, 3), (15, 7, 20, 2), (15, 10, 21, 7),
                                 (10, 3, 8, 1), (20, 2, 22, 0)):
            L.line(x0, y0, x1, y1, "kr0")
            L.line(x0 + 1, y0, x1 + 1, y1, "kr1")
    foam_ring(allf, 0, 0, 32, 32, lambda X, Y: sub.get(X, Y) is not None and Y > 12, width=(2, 3, 2))
    # the wreck: blackened ribs in a reef
    reef = K.Layer(M.w, M.h)
    rpts = [(34, 20), (40, 15), (52, 16), (64, 14), (76, 18), (78, 26), (64, 28), (46, 28), (36, 26)]
    for L in allf:
        rock_blob(L, 0, 0, rpts, seed=8)
    reef.poly(rpts, "kr0")
    for L in allf:
        for (rx, top) in ((40, 6), (46, 3), (52, 2), (58, 2), (64, 4), (70, 7)):
            for y in range(top, 22):
                L.px(rx, y, "kr0")
                L.px(rx + 1, y, "l1" if y > top + 1 else "ks1")
            L.px(rx, top - 1, "l1")
        L.line(38, 12, 74, 10, "l1")
        L.line(38, 13, 74, 11, "kr0")
        for x in range(40, 72):
            if L.get(x, 22) in ("kr2", "kr3", "w0"):
                L.px(x, 22, "kr0")
    foam_ring(allf, 32, 0, 48, 32, lambda X, Y: reef.get(X, Y) is not None, width=(2, 3, 2))
    return s


# --------------------------------------------------------------------------
# Echo's sea caves
# --------------------------------------------------------------------------

def dark_px(X, Y):
    return stone_px(X, Y, 2)


def cave():
    names = {
        "ceil": (0, 0), "ceil_S": (1, 0), "ceil_S_b": (2, 0), "ceil_E": (3, 0), "ceil_W": (4, 0),
        "ceil_NW": (5, 0), "ceil_NE": (6, 0), "crack": (7, 0),
        "wall_L": (0, 1), "wall": (1, 1), "wall_b": (2, 1), "wall_R": (3, 1),
        "ceil_in_SE": (4, 1), "ceil_in_SW": (5, 1), "wall_lamp": (6, 1), "stair_up": (7, 1),
        "base_L": (0, 2), "base": (1, 2), "base_R": (2, 2), "floor": (3, 2), "floor_b": (4, 2),
        "floor_pebbles": (5, 2), "light_L": (6, 2), "light_R": (7, 2),
        "pool_N": (0, 3), "pool_S": (1, 3), "pool_E": (2, 3), "pool_W": (3, 3),
        "brazier_cold": (4, 3), "brazier_lit": (5, 3), "mouth_L": (6, 3), "mouth_R": (7, 3),
    }
    walk = ["XXXXXXXX", "XXXXXXXD", "XXX.....", "XXXXXXWW"]
    s = struct("cave", "Echo's sea caves", 8, 4, SEC_C, walk=walk, names=names,
               notes="Dark pink rock, the spring's water running down to the sea. The rock mass is "
                     "`ceil` (the cave's roof seen from above), edged by `ceil_S` (its south lip, "
                     "over a wall face), `ceil_E` / `ceil_W` (a wall running north-south, the floor "
                     "to the east / west), `ceil_NW` / `ceil_NE` (outer corners, floor to the south-"
                     "east / south-west) and `ceil_in_SE` / `ceil_in_SW` (inner corners). Below a "
                     "`ceil_S` run a wall face two cells high: `wall_L` `wall` `wall_b` `wall_R` "
                     "over `base_L` `base` `base_R`, where it meets the floor. `crack` is the "
                     "Speaking Hall's roof crack, with `light_L` `light_R` the patch of daylight it "
                     "throws on the floor. The floor: `floor`, `floor_b`, `floor_pebbles` "
                     "(walkable). `pool_N` `_S` `_E` `_W` edge a cave pool (borrowed sea; named by "
                     "where the water is). `wall_lamp` is a lamp in a niche by the diver; "
                     "`brazier_cold` / `brazier_lit` the dark gallery's brazier (SYSTEMS §2; swap "
                     "cold for lit). `stair_up` climbs back to the spring (the door). `mouth_L` "
                     "`mouth_R` are the sea mouth: a low arch opening on daylit sea (borrowed sea, "
                     "surfable).")
    ground(s, "sea", [(0, 3), (1, 3), (2, 3), (3, 3), (6, 3), (7, 3)])
    B, M = s.B, s.M

    def ceil_px(X, Y):
        x, y = X % 16, Y % 16
        k = K.hp(X, Y, 61)
        return "cv0" if k % 9 else "rm0"

    def floor_px(X, Y, peb=False):
        x, y = X % 16, Y % 16
        k = K.hp(X, Y, 63)
        c = "rm1" if k % 5 else "rm0"
        if k % 17 == 0:
            c = "rm2"
        if peb and k % 11 == 0:
            c = "rm3"
        return c
    for y in range(16):
        for x in range(16):
            B.px(x, y, ceil_px(x, y))
    # ceil_S: the lip over a face: mass, a lit rim, the face's top
    for cx in (1, 2):
        ox = cx * 16
        for y in range(16):
            for x in range(16):
                X = ox + x
                rim = 9 + int(round(wob(X + 3 * cx, 0.5) * 0.7))
                if y < rim:
                    c = ceil_px(X, y)
                elif y == rim:
                    c = "rm2"
                elif y == rim + 1:
                    c = "rm1"
                else:
                    c = dark_px(X, y)
                B.px(X, y, c)
    # ceil_E / ceil_W: the mass on one side, a lit rim, floor on the other
    for cx, side in ((3, "E"), (4, "W")):
        ox = cx * 16
        for y in range(16):
            e = 8 + int(round(wob(y + cx, 0.5) * 0.7))
            for x in range(16):
                xx = x if side == "E" else 15 - x
                X = ox + x
                if xx < e:
                    c = ceil_px(X, y)
                elif xx == e:
                    c = "rm2" if side == "E" else "rm3"
                elif xx == e + 1:
                    c = "rm0"
                else:
                    c = floor_px(X, y)
                B.px(X, y, c)
    # outer corners: mass to the north-west (ceil_NW means floor south-east of it)
    for cx, side in ((5, "W"), (6, "E")):
        ox = cx * 16
        for y in range(16):
            for x in range(16):
                xx = x if side == "W" else 15 - x
                X = ox + x
                r = math.hypot(max(0, xx - 7.5), max(0, y - 7.5))
                if r < 0.5 and (xx < 8 or y < 8):
                    c = ceil_px(X, y)
                elif r < 1.5:
                    c = "rm2"
                elif r < 2.5:
                    c = "rm0"
                else:
                    c = floor_px(X, y)
                if xx < 8 and y < 8:
                    c = ceil_px(X, y)
                B.px(X, y, c)
    # crack: a jagged lit seam across the roof
    for y in range(16):
        for x in range(16):
            B.px(112 + x, y, ceil_px(112 + x, y))
    for i in range(16):
        y = 4 + int(round(3 * math.sin(i / 2.0)))
        B.px(112 + i, y, "rm4")
        B.px(112 + i, y + 1, "rm5" if i % 3 else "w0")
        B.px(112 + i, y + 2, "rm2")
    # wall faces (two rows: wall then base)
    for cx, end in ((0, "L"), (1, None), (2, None), (3, "R")):
        ox = cx * 16
        for row, oy in ((0, 16), (1, 32)):
            for y in range(16):
                for x in range(16):
                    X, Y = ox + x, oy + y
                    c = dark_px(X + 5 * (cx == 2), Y)
                    if row == 1 and y >= 10:
                        c = floor_px(X, Y) if y > 11 else "cv0"
                    if end == "L" and x < 3:
                        c = ceil_px(X, Y) if row == 0 or y < 10 else floor_px(X, Y)
                        if x == 2:
                            c = "rm2"
                    if end == "R" and x > 12:
                        c = ceil_px(X, Y) if row == 0 or y < 10 else floor_px(X, Y)
                        if x == 13:
                            c = "rm0"
                    B.px(X, Y, c)
    # inner corners of the mass
    for cx, side in ((4, "E"), (5, "W")):
        ox, oy = cx * 16, 16
        for y in range(16):
            for x in range(16):
                xx = x if side == "E" else 15 - x
                X, Y = ox + x, oy + y
                if xx < 8 and y < 8:
                    r = math.hypot(8 - xx, 8 - y)
                    c = ceil_px(X, Y) if r > 1.5 else "rm2"
                elif xx < 8:
                    c = ceil_px(X, Y) if xx < 7 else "rm2"
                elif y < 8:
                    c = ceil_px(X, Y) if y < 7 else "rm2"
                else:
                    c = dark_px(X, Y)
                B.px(X, Y, c)
    # wall_lamp: a niche with a burning clay lamp
    for y in range(16):
        for x in range(16):
            B.px(96 + x, 16 + y, dark_px(96 + x, 16 + y))
    put(B, 96 + 4, 16 + 3, [
        ".kkkkkk.",
        "k000000k",
        "k00ww00k",
        "k00w300k",
        "k0333330",
        "k2222222",
        ".kkkkkk.",
    ], {"k": "rm0", "0": "cv0", "w": "w0", "3": "rm4", "2": "rm2"})
    # stair up: rock steps rising north into a lighter opening
    for y in range(16):
        for x in range(16):
            X, Y = 112 + x, 16 + y
            if 3 <= x <= 12:
                step = y // 4
                c = ("rm4", "rm3", "rm2", "rm1")[y % 4] if step > 0 else ("rm5" if y < 2 else "rm4")
            else:
                c = dark_px(X, Y)
                if x in (2, 13):
                    c = "rm0"
            B.px(X, Y, c)
    # floors
    for cx, peb in ((3, False), (4, False), (5, True)):
        for y in range(16):
            for x in range(16):
                B.px(cx * 16 + x, 32 + y, floor_px(cx * 16 + x + 7 * (cx == 4), 32 + y, peb))
    for (px_, py_) in ((3, 3), (10, 5), (6, 11), (12, 12)):
        put(B, 80 + px_, 32 + py_, ["32", "21"], {"3": "rm3", "2": "rm2", "1": "rm0"})
    # the patch of light under the crack
    for cx in (6, 7):
        for y in range(16):
            for x in range(16):
                X = cx * 16 + x
                d = math.hypot((X - 112) / 13.0, (y - 8) / 6.5)
                c = floor_px(X, 32 + y)
                if d < 1:
                    c = {"rm0": "rm2", "rm1": "rm3", "rm2": "rm4", "rm3": "rm5"}[c]
                    if d < 0.5 and (X + y) % 3 == 0:
                        c = "rm5"
                B.px(X, 32 + y, c)
    # pools: a dark rock lip, the water borrowed
    for cx, side in ((0, "N"), (1, "S"), (2, "E"), (3, "W")):
        ox, oy = cx * 16, 48
        for y in range(16):
            for x in range(16):
                d = {"N": 15 - y, "S": y, "E": x, "W": 15 - x}[side]
                d = d + int(round(wob((x if side in "NS" else y) + cx, 0.5) * 0.6))
                if d < 7:
                    c = floor_px(ox + x, oy + y)
                elif d < 8:
                    c = "rm2"
                elif d < 9:
                    c = "cv0"
                else:
                    continue
                M.px(ox + x, oy + y, c)
    # the brazier (bronze group: its own tiles), cold and lit, on the floor
    for cx, lit in ((4, False), (5, True)):
        ox, oy = cx * 16, 48
        for y in range(16):
            for x in range(16):
                B.px(ox + x, oy + y, floor_px(ox + x, oy + y))
        put(M, ox + 2, oy + 4, [
            "kkkkkkkkkkkk",
            "k3333333333k",
            ".k22222222k.",
            "..k111111k..",
            "...k.kk.k...",
            "..k..kk..k..",
            ".k...kk...k.",
            "kk..kkkk..kk",
        ], {"k": "bz0", "3": "bz3", "2": "bz2", "1": "bz1"})
        if lit:
            put(M, ox + 4, oy, [
                "...m....",
                "..mmm.m.",
                ".mrmmmm.",
                ".mrrwrm.",
                "mrrwwwrm",
            ], {"m": "mr", "r": "bz2", "w": "w0"})
        else:
            put(M, ox + 4, oy + 3, ["kkkkkkkk"], {"k": "ink"})
    # the sea mouth: a low arch, daylit sea beyond (borrowed), rock either side
    for cx, side in ((6, "L"), (7, "R")):
        ox, oy = cx * 16, 48
        for y in range(16):
            for x in range(16):
                xx = x if side == "L" else 15 - x
                X, Y = ox + x, oy + y
                arch = 9 - math.sqrt(max(0, 81 - (16 - xx) ** 2 * 0.4)) * 0.8
                if xx < 3:
                    c = dark_px(X, Y)
                elif y < 4 + max(0, 6 - xx) * 0.9:
                    c = dark_px(X, Y) if y < 3 + max(0, 6 - xx) * 0.9 else "rm2"
                else:
                    continue
                M.px(X, Y, c)
    return s


def build_melos():
    return [obsidian(), obsidian_bits(), boathouses(), village()]


def build_sea():
    return [sea_marks()]


def build_cave():
    return [cave()]


def build():
    return build_melos() + build_sea() + build_cave()
