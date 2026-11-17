"""The roads of Lakonia: Route 25 up the Eurotas, Route 26 past the training
grounds, Route 27 over the hills to Arkadia.

Trees (holm-oak, walnut, black pine), hyacinths, the throne of Amyklai and its
altar's fire, the roadside herm-shrines, the roofless farmhouse of Hestia's
visit, the Vapheio beehive tomb's bronze door, the running track's posts, the
Phoibaion, the ravine and its plank bridge, the Karyai spring, the Skiritai
watchtower, the fallen column drum and the cracked Hammer rock.
"""
from __future__ import annotations

import math

import numpy as np

import lakonia_lib as L
from lakonia_lib import ground, put, struct
from kythera_land import foliage

SEC = "route"
hp, mx = L.hp, L.mx

HOLM = ("ho1", "ho2", "my2", "my3")
WALNUT = ("my1", "my2", "my3", "my4")


def _crown(T, M, mask, ramp, seed, split=16, clump=4.0, outline="t0"):
    tmp = L.Layer(mask.shape[1], mask.shape[0])
    foliage(tmp, mask, ramp, seed=seed, clump=clump, outline=outline, periodic=False)
    for y, x in zip(*np.nonzero(tmp.a[..., 3] > 0)):
        (T if y < split else M).px(int(x), int(y), tmp.get(int(x), int(y)))


def trees():
    names = {"holm_TL": (0, 0), "holm_TR": (1, 0), "holm_BL": (0, 1), "holm_BR": (1, 1),
             "pine_TL": (2, 0), "pine_TR": (3, 0), "pine_ML": (2, 1), "pine_MR": (3, 1),
             "pine_BL": (2, 2), "pine_BR": (3, 2),
             "walnut_00": (4, 0), "walnut_10": (5, 0), "walnut_20": (6, 0),
             "walnut_01": (4, 1), "walnut_11": (5, 1), "walnut_21": (6, 1),
             "walnut_02": (4, 2), "walnut_12": (5, 2), "walnut_22": (6, 2),
             "holm_small": (0, 2), "shrub": (1, 2)}
    s = struct("trees", "Holm-oak, black pine and walnut", 7, 3, SEC,
               walk=["TTTTTTT", "XXXXXXX", "XXXXXXX"], names=names,
               notes="The hill country's trees, on borrowed grass. The holm-oak (`holm_*`, 2 x "
                     "2): a dense dark evergreen crown, top row over the player. The black pine "
                     "(`pine_*`, 2 x 3): tiers of dark needles high on Taygetos and the "
                     "Skiritis, its top row over the player. The walnut (`walnut_XY`, 3 x 3): "
                     "a broad pale-green crown on a gray trunk, the Karyai spring's trees. "
                     "`holm_small` is a young holm-oak and `shrub` a kermes-oak bush, 1 x 1, "
                     "impassable. Plant trunk rows impassable.")
    ground(s, "grass")
    T, M = s.T, s.M
    # holm-oak: crown 32 x 26 over a short dark trunk
    m = np.zeros((48, 112), bool)
    for y in range(30):
        for x in range(32):
            a = math.atan2(y - 13, x - 16)
            if math.hypot((x - 16) / 15, (y - 13) / 12.5) < 1 + 0.07 * math.sin(a * 7 + 1):
                m[y, x] = True
    for y in range(22, 31):
        for x in range(13, 19):
            if abs(x - 15.5) <= 1.6 + max(0, y - 27) * 0.8:
                M.px(x, y, "kt1" if x > 15 else "t0")
    L.shadow(M, 4, 27, 26, 5, lambda x, y: math.hypot((x - 17) / 12, (y - 29) / 2.6) < 1)
    _crown(T, M, m, HOLM, 21, clump=3.5)
    # young holm-oak and a kermes-oak shrub
    m = np.zeros((48, 112), bool)
    for y in range(32, 46):
        for x in range(0, 16):
            if math.hypot((x - 7.5) / 6.5, (y - 38) / 5.8) < 1:
                m[y, x] = True
    for y in range(32, 46):
        for x in range(16, 32):
            a = math.atan2(y - 40, x - 23.5)
            if math.hypot((x - 23.5) / 7.0, (y - 40) / 5.0) < 1 + 0.12 * math.sin(a * 9):
                m[y, x] = True
    for y in range(42, 47):
        M.px(7, y, "kt1")
        M.px(8, y, "t0")
    L.shadow(M, 0, 43, 32, 4, lambda x, y: (y - 43) < 3)
    _crown(T, M, m, HOLM, 23, split=0, clump=3.0)
    # black pine: three tiers, 32 x 44, a crooked trunk
    for y in range(34, 46):
        M.px(48 + 15, y, "kt1")
        M.px(48 + 16, y, "t0")
    L.shadow(M, 36, 42, 26, 6, lambda x, y: math.hypot((x - 64) / 12, (y - 45) / 2.5) < 1)
    m = np.zeros((48, 112), bool)
    for t_, (cy_, rx, ry) in enumerate(((7, 9.5, 6.5), (18, 13.0, 7.5), (29, 15.0, 7.0))):
        for y in range(48):
            for x in range(32):
                a = math.atan2(y - cy_, x - 15.5)
                if math.hypot((x - 15.5) / rx, (y - cy_) / ry) < 1 + 0.12 * math.sin(a * 8 + t_):
                    if y < cy_ + ry * 0.55:
                        m[y, 32 + x] = True
    _crown(T, M, m, ("ho1", "my1", "my2", "my3"), 25, clump=3.0)
    # walnut: like the plane's crown, paler, a pale gray trunk
    m = np.zeros((48, 112), bool)
    for y in range(40):
        for x in range(48):
            a = math.atan2(y - 17, x - 24)
            if math.hypot((x - 24) / 23.0, (y - 17) / 16.0) < 1 + 0.06 * math.sin(a * 6):
                m[y, 64 + x] = True
    for y in range(26, 47):
        for x in range(19, 29):
            half = 3.0 + max(0, y - 41) * 0.7
            if abs(x - 23.5) <= half:
                c = "kt3" if x < 23 else ("kt2" if x < 26 else "kt1")
                if hp(x, y, 4) % 6 == 0:
                    c = "kt2"
                M.px(64 + x, y, c)
    L.shadow(M, 64 + 8, 42, 34, 6, lambda x, y: math.hypot((x - 88) / 15, (y - 44) / 3) < 1)
    _crown(T, M, m, WALNUT, 27, clump=5.0, outline="my1")
    return s


def flowers():
    s = struct("flowers", "Hyacinths", 2, 1, SEC, walk=[".."],
               names={"hyacinths": (0, 0), "hyacinths_b": (1, 0)},
               notes="Hyacinths, dark blue-violet, by the tomb under Amyklai's throne (the "
                     "object beside the tomb): AI AI written on their petals. Walkable, on "
                     "borrowed grass.")
    ground(s, "grass")
    M = s.M
    for cx, pts in ((0, ((3, 2), (10, 4), (6, 9), (12, 11), (2, 12))),
                    (1, ((4, 4), (11, 2), (8, 10), (2, 9), (13, 12)))):
        for (fx, fy) in pts:
            put(M, cx * 16 + fx, fy, [".h.", "hHh", "hHh", ".g.", "g.g"],
                {"h": "hy1", "H": "hy2", "g": "my2"})
    return s


# --------------------------------------------------------------------------
# Amyklai: the throne, the altar's fire, the spring
# --------------------------------------------------------------------------

def amyklai():
    names = {"crown_L": (0, 0), "crown": (1, 0), "crown_R": (2, 0),
             "body_L": (0, 1), "body": (1, 1), "body_R": (2, 1),
             "seat_L": (0, 2), "seat": (1, 2), "seat_R": (2, 2),
             "tomb_L": (0, 3), "tomb": (1, 3), "tomb_R": (2, 3)}
    s = struct("throne", "The throne of Amyklai", 3, 4, SEC,
               walk=["TTT", "XXX", "XXX", "XXX"], names=names,
               notes="Apollo of Amyklai (an object): an old bronze god like a column, helmeted, "
                     "with spear and bow, seated on a stone throne the size of a house, which "
                     "stands on the mound of Hyakinthos's tomb. 3 x 4; the god's helmet and "
                     "spear (top row) are drawn over the player. Put the hyacinths beside the "
                     "tomb, the altar in front. On borrowed grass at the top corners.")
    ground(s, "grass", [(0, 0), (1, 0), (2, 0)])
    B, M, T = s.B, s.M, s.T
    W = 48
    # the tomb mound and the throne's stone, bottom layer from row 1 down
    for y in range(16, 64):
        for x in range(W):
            # throne: back slab, arms, a stepped base on the mound
            c = None
            if y < 44:
                if 6 <= x <= 41:
                    c = "sn2" if (x + y) % 7 else "sn1"
                    if x in (6, 41):
                        c = "sn1"
                    if x in (7,):
                        c = "sn3"
                    if y in (16, 17):
                        c = "sn3" if y == 16 else "sn2"
                    # reliefs on the back: faint figures in panels
                    if 9 <= x <= 38 and 19 <= y <= 30 and (x - 9) % 10 in (0,) :
                        c = "sn1"
                else:
                    c = L.grass_px(x, y)
                    c = "gd" if c == "g3" else c
            elif y < 52:
                # the base, three steps
                st = (y - 44) // 3
                c = ("sn3", "sn2", "sn1")[min(2, (y - 44) % 3)]
                if x < 3 + st * 0 or x > 44:
                    c = "gd"
            else:
                # the mound: grassy earth over the tomb, a dark doorway in it
                a = abs(x - 23.5)
                if y > 54 + a * 0.25 and a > 15:
                    c = L.grass_px(x, y)
                    c = "gd" if c == "g3" else c
                else:
                    c = "gd" if (x + y) % 3 else "g1"
                    if 19 <= x <= 28 and y >= 56:
                        c = "ink" if 20 <= x <= 27 else "sn1"
                    if y == 55 and 18 <= x <= 29:
                        c = "sn3"
            B.px(x, y, c)
    # the god: a bronze column with arms, helmet, spear and bow (red group)
    god = [
        "......3........",
        ".....323.......",
        "....32223......",
        "...3222223.....",
        "...1222221.....",
        "...12ii221.....",
        "...1222221.....",
        "....12221......",
        "..112222211....",
        ".12222222221...",
        "123222222321...",
        "122222222221...",
        "1231222221321..",
        "12312222213221.",
        ".2312222213221.",
        ".23122222132v1.",
        ".1v1222221v221.",
        "..1.22222.1221.",
        "....12221..221.",
        "....12221...21.",
        "....12221...21.",
        "....1v221....1.",
        "....12221......",
        "....12221......",
        "....12221......",
        "....1222v......",
        "....12221......",
        "....12221......",
        "...1222221.....",
        "...1222v221....",
        "..122222221....",
        "..111111111....",
    ]
    for j, row in enumerate(god):
        for i, ch in enumerate(row):
            if ch == ".":
                continue
            c = {"1": "bz0", "2": "bz1", "3": "bz2", "i": "ink", "v": "vg1"}[ch]
            X, Y = 17 + i, 4 + j
            (T if Y < 16 else M).px(X, Y, c)
    # spear (left, up past the helmet) and bow (right hand)
    for y in range(0, 30):
        (T if y < 16 else M).px(15, y, "bz1" if y > 1 else "bz3")
    for y in range(0, 2):
        T.px(14, y + 1, "bz2")
        T.px(16, y + 1, "bz2")
    for y in range(14, 30):
        dx = round(2.2 * math.sin(math.pi * (y - 14) / 16))
        M.px(32 + dx, y, "bz0")
    for y in range(14, 30):
        M.px(31, y, "w0" if y % 3 == 0 else None) if False else None
    # sun-glints on his helmet and shoulders
    for (x, y) in ((21, 6), (19, 15), (25, 16)):
        (T if y < 16 else M).px(x, y, "bz3")
    return s


def altar():
    names = {"fire_L": (0, 0), "fire_R": (1, 0), "cold_L": (2, 0), "cold_R": (3, 0)}
    s = struct("altar", "Altars: Amyklai's fire, the Phoibaion", 4, 1, SEC, walk=["XXXX"],
               names=names,
               notes="A long stone altar, 2 x 1. `fire_L` `fire_R`: Amyklai's, where Polyboia "
                     "keeps the fire (animated): Apollo's daily prayer, and the flame Hestia's "
                     "test carries. `cold_L` `cold_R`: the Phoibaion on Route 26, the little old "
                     "altar where the two teams made their offering; its step holds the "
                     "visible item. On borrowed grass; impassable.")
    ground(s, "grass")
    M = s.M
    for ox in (0, 32):
        put(M, ox + 2, 3, [
            "4444444444444444444444444444",
            "4333333333333333333333333332",
            "4333333333333333333333333332",
            "4322222222222222222222222232",
            "4321212121212121212121212232",
            "4322222222222222222222222232",
            "4333333333333333333333333332",
            "2222222222222222222222222221",
            ".11111111111111111111111111.",
            "..g.g.g.g.g.g.g.g.g.g.g.g...",
        ], {"4": "sn3", "3": "sn2", "2": "sn1", "1": "sn1", "g": "gd"})
    put(M, 32 + 8, 2, ["1111111111111", "1.1.1.1.1.1.1"], {"1": "sn1"})
    put(M, 32 + 20, 0, [".g.", "g1g", ".1."], {"g": "gd", "1": "sn1"})
    frames = L.anim_layer(s, "flame", 3, layer="middle")
    for fi, F in enumerate([M] + frames):
        for k, fx in enumerate((6, 12, 18, 24)):
            L.flame(F, fx, -1 + (k % 2), (fi + k) % 3)
    L.settle(s, "flame", [(0, 0), (1, 0)])
    return s


def spring():
    names = {"TL": (0, 0), "TR": (1, 0), "BL": (0, 1), "BR": (1, 1)}
    s = struct("spring", "A spring in a stone basin", 2, 2, SEC,
               walk=["XX", "XX"], names=names,
               notes="A spring welling into a stone basin under a carved spout, 2 x 2: "
                     "Amyklai's spring beside the throne and the Karyai spring under the "
                     "walnuts (both heal: put the bg event on the basin). The water is the "
                     "Eurotas's, animated. Impassable; on borrowed grass outside the kerb.")
    M = s.M
    W = 32
    for y in range(W):
        for x in range(W):
            d = max(abs(x - 15.5) / 14.5, abs(y - 17.5) / 13.0)
            if d > 1:
                M.px(x, y, L.grass_px(x, y) if L.grass_px(x, y) != "g3" else "g2")
            elif d > 0.78:
                lit = (y < 17) or (x < 8)
                c = "sn3" if lit else "sn2"
                if d > 0.93:
                    c = "sn4" if y < 12 else "sn1"
                M.px(x, y, c)
    # the spout block at the back, a thread of water
    put(M, 11, 2, ["1111111111", "1333333331", "1344444431", "1333003331", "1111001111"],
        {"1": "sn1", "3": "sn3", "4": "sn4", "0": "ink"})
    L.water(s, "eurotas", walk=None, behavior=None)
    for y in range(7, 12):
        M.px(15, y, "ew4" if y % 2 else None) if False else None
    return s


# --------------------------------------------------------------------------
# Herm-shrines, the farmhouse, the Vapheio door
# --------------------------------------------------------------------------

def herm_shrine():
    names = {"lit": (0, 0), "lit_base": (0, 1), "unlit": (1, 0), "unlit_base": (1, 1)}
    s = struct("herm_shrine", "Roadside herm-shrines", 2, 2, SEC, walk=["TT", "XX"],
               names=names,
               notes="A roadside herm-shrine: a stone pillar with a little roofed niche for a "
                     "lamp, 1 x 2 (the top drawn over the player, the base impassable). "
                     "`lit` (the lamp burning, animated) and `unlit`; Hestia's test relights a "
                     "carried flame at a lit one (swap `lit` over `unlit`). On borrowed grass.")
    ground(s, "grass")
    T, M = s.T, s.M
    for ox in (0, 16):
        put(T, ox + 2, 2, [
            "....3333....",
            "..33333333..",
            ".3222222223.",
            "311111111113",
            ".1322222231.",
            ".132000023..",
            ".132000023..",
            ".132000023..",
            ".132000023..",
            ".133333333..",
            ".1222222221.",
            "..12222221..",
            "..13333221..",
            "..13222221..",
        ], {"3": "sn3", "2": "sn2", "1": "sn1", "0": "ink"})
        put(M, ox + 2, 16, [
            "..13222221..",
            "..13222221..",
            "..13222221..",
            "..13222221..",
            "..13222221..",
            ".1333333221.",
            ".1222222221.",
            "..11111111..",
            "..g.g.g.g...",
        ], {"3": "sn3", "2": "sn2", "1": "sn1", "g": "gd"})
    frames = L.anim_layer(s, "flame", 3, layer="top")
    for fi, F in enumerate([T] + frames):
        L.flame(F, 5, 8, fi)
    L.settle(s, "flame", [(0, 0)])
    return s


def farmhouse():
    names = {"back_L": (0, 0), "back": (1, 0), "back_b": (2, 0), "back_R": (3, 0),
             "room_L": (0, 1), "hearth_L": (1, 1), "hearth_R": (2, 1), "room_R": (3, 1),
             "front_L": (0, 2), "door": (1, 2), "front": (2, 2), "front_R": (3, 2),
             "roof_BL": (0, 3), "roof_B": (1, 3), "roof_B2": (2, 3), "roof_BR": (3, 3),
             "roof_FL": (0, 4), "roof_F": (1, 4), "roof_F2": (2, 4), "roof_FR": (3, 4)}
    s = struct("farmhouse", "The roofless farmhouse", 4, 5, SEC,
               walk=["XXXX", "X..X", "XDXX", "XXXX", "XXXX"], names=names,
               notes="Hestia's theoxenia (E2): a farmhouse in the west fields with its roof "
                     "beams taken by the Titans, 4 x 3: thick mudbrick walls seen from above "
                     "round an open room, the cold hearth in its middle (`hearth_L` `hearth_R`, "
                     "the bg event), the doorway in the front wall (`door`, walkable: the room "
                     "is part of the map). `hearth_lit`'s two cells are the hearth burning: "
                     "swap them in after Hestia's visit. `roof_*` (4 x 2) is the roof the "
                     "farmer rebuilds after the climax: swap it over the top two rows. Walls "
                     "impassable.")
    B = s.B
    W = 64

    def wall_top(X, Y):
        k = hp(X % 16, Y % 16, 131)
        return "pw2" if k % 4 == 0 else "pw1"

    for y in range(48):
        for x in range(W):
            X, Y = x, y
            # walls: 5 px thick tops; the room's floor of trodden earth inside
            back = y < 9
            left = x < 6
            right = x >= W - 6
            front = y >= 35
            if back or left or right or front:
                if front and y >= 40:
                    # the front wall's face, plaster on a stone footing
                    c = "pw1" if y < 45 else ("sn2" if (x + y) % 4 else "sn1")
                    if y == 40:
                        c = "sn2"
                else:
                    c = wall_top(X, Y)
                    if (back and y == 8) or (front and y == 35):
                        c = "ro1" if back else "pw2"
                    if (left and x == 5) or (right and x == W - 6):
                        c = "ro1" if left else "pw2"
                    if y == 0 or x == 0 or x == W - 1:
                        c = "sn2"
                # crumbled tops where the beams were pulled out
                if (back and y < 2 and x % 16 in (6, 7)) or (front and y in (35,) and x % 16 == 9):
                    c = "ro1"
            else:
                c = "ro2" if hp(x % 16, y % 16, 133) % 5 else "ro1"
                if y == 9 or x == 6:
                    c = "sn1"
                if y == 10 or x == 7:
                    c = "ro1"
            B.px(X, Y, c)
    # the doorway in the front wall
    for y in range(35, 48):
        for x in range(19, 29):
            c = "ro2" if y < 40 else ("ro1" if x in (19, 28) else "ro2")
            if y >= 40 and x in (20, 27):
                c = "sn1"
            B.px(x, y, c)
    # the hearth: a ring of stones round cold ash
    def hearth(ox, oy):
        put(B, ox + 8, oy + 3, [
            "...33333333333...",
            "..3222222222223..",
            ".322000000000223.",
            ".320011110011023.",
            ".320111011100023.",
            ".320011100110023.",
            ".322000000000223.",
            "..3222222222223..",
            "...11111111111...",
        ], {"3": "sn3", "2": "sn2", "0": "sn1", "1": "sn0"})
    hearth(0, 16)
    # the rebuilt roof: flat clay, coping, joists, as Lakonia's houses
    import lakonia_town as Tn
    for y in range(48, 80):
        for x in range(W):
            yy = y - 48
            c = Tn.roof_px(x, y)
            if yy <= 1:
                c = "pw2" if yy == 0 else "pw1"
            if yy >= 27:
                c = ("pw2", "pw1", "sn3", "sn2", "sn1")[yy - 27]
            if x <= 1:
                c = "pw2" if x == 0 else "pw1"
            if x >= W - 2:
                c = "pw1" if x == W - 2 else "sn2"
            B.px(x, y, c)
    for bx in range(5, W - 4, 7):
        B.px(bx, 48 + 30, "ro1")
        B.px(bx, 48 + 31, "ink")
    s.behaviors = {}
    return s


def hearth_lit():
    """The farmhouse's hearth burning after Hestia's visit: its two cells."""
    f = farmhouse()
    s = struct("hearth_lit", "The farmhouse hearth, burning", 2, 1, SEC, walk=["XX"],
               names={"lit_L": (0, 0), "lit_R": (1, 0)},
               notes="The farmhouse's hearth after Hestia's visit, burning steadily (animated; "
                     "rain never reaches it): swap `lit_L` `lit_R` over `farmhouse`'s "
                     "`hearth_L` `hearth_R`. Impassable.")
    s.B.a[:] = f.B.a[16:32, 16:48]
    frames = L.anim_layer(s, "flame", 3, layer="middle")
    for fi, F in enumerate([s.M] + frames):
        for k, fx in enumerate((10, 16, 22)):
            L.flame(F, fx, 2 + (k % 2), (fi + k) % 3)
    return s


def vapheio():
    names = {"mound_L": (0, 0), "mound_TL": (1, 0), "mound_TR": (2, 0), "mound_R": (3, 0),
             "dromos_L": (0, 1), "door_TL": (1, 1), "door_TR": (2, 1), "dromos_R": (3, 1),
             "steps_L": (0, 2), "door_BL": (1, 2), "door_BR": (2, 2), "steps_R": (3, 2),
             "open_TL": (4, 1), "open_TR": (5, 1), "open_BL": (4, 2), "open_BR": (5, 2)}
    s = struct("vapheio", "The Vapheio door: a beehive tomb's bronze door", 6, 3, SEC,
               walk=["XXXXXX", "XXXXXX", "XXXXDD"], names=names,
               notes="The Vapheio tholos in the hillside below Amyklai (one of LABYRINTH §9's "
                     "five Minoan vaults): a grassy mound, a passage of dressed stone cut into "
                     "it (the dromos), and at its end a bronze door with no handle, only a "
                     "hollow shaped like a double axe, under a great lintel and its "
                     "relieving triangle. 4 x 3, impassable. `open_*` (2 x 2) is the door swung "
                     "in, dark beyond: swap it over `door_*` after the Labrys opens it (its "
                     "bottom cells are doors, `MB_NON_ANIMATED_DOOR`). The mound's top row "
                     "stands on borrowed grass.")
    ground(s, "grass", [(0, 0), (3, 0), (4, 0), (5, 0)])
    B, M = s.B, s.M
    # the mound: a grassy dome over the tomb, darker toward its flanks
    for y in range(16):
        for x in range(64):
            a = abs(x - 31.5)
            if y > 12 - (1 - (a / 31.5) ** 2) * 10:
                c = L.grass_px(x, y)
                if a > 20:
                    c = "gd" if (x + y) % 2 else "g1"
                (B if 16 <= x < 48 else M).px(x, y, c if c != "g3" else "g2")
    for y in range(16):
        for x in range(16, 48):
            if B.get(x, y) is None:
                B.px(x, y, L.grass_px(x, y) if L.grass_px(x, y) != "g3" else "g2")
    # dromos walls of dressed stone, and the door under its lintel
    for y in range(16, 48):
        for x in range(64):
            if 16 <= x < 48:
                continue
            side = x < 16
            lx = x if side else 63 - x
            c = Lr_course(x, y)
            if lx > 12:
                c = "sn1" if side else "sn2"
            if y >= 40 and lx < 12:
                c = ("sn3", "sn2", "sn2", "sn1", "sn3", "sn2", "sn1", "sn1")[y - 40]
            B.px(x, y, c)
    # door frame: lintel, relieving triangle, jambs
    for y in range(16, 48):
        for x in range(16, 48):
            dx = abs(x - 31.5)
            if y < 22:
                c = "sn3" if y < 18 else ("sn2" if dx > 6 - (y - 18) * 1.5 else "sn0")
                if 18 <= y < 22 and dx <= 6 - (y - 18) * 1.5:
                    c = "sn0"
            elif y < 24:
                c = "sn4" if y == 22 else "sn2"
            elif dx > 12:
                c = "sn3" if x < 31 else "sn1"
            else:
                c = None
            if c:
                B.px(x, y, c)
    # the bronze door (stone group can't hold bronze: draw it on the middle layer)
    for y in range(24, 48):
        for x in range(20, 44):
            dx = x - 20
            c = "bz1" if (dx + y) % 7 else "vg1"
            if dx in (11, 12):
                c = "bz0"
            if dx == 0 or y == 24:
                c = "bz2"
            if dx == 23 or y > 45:
                c = "bz0"
            if (y - 27) % 6 == 0 and dx % 6 == 3:
                c = "bz3"
            M.px(x, y, c)
    put(M, 26, 30, [
        ".000.....000.",
        "0vvv0...0vvv0",
        "0vvvv000vvvv0",
        "0vvvvv0vvvvv0",
        "0vvvv000vvvv0",
        "0vvv0.0.0vvv0",
        ".000..0..000.",
        "......0......",
        "......0......",
        "......0......",
    ], {"0": "bz0", "v": "ink"})
    for y in range(24, 48):
        for x in range(16, 20):
            B.px(x, y, "sn1")
        for x in range(44, 48):
            B.px(x, y, "sn2")
    # grass below the steps (bottom row's outer cells are walls' feet)
    # the open door: dark, the leaf swung in at the side
    for y in range(16, 48):
        for x in range(64, 96):
            B.px(x, y, B.get(x - 48, y))
    for y in range(24, 48):
        for x in range(68, 92):
            M.px(x, y, None)
            B.px(x, y, "ink" if x < 88 else "sn0")
        for x in range(88, 92):
            M.px(x, y, "bz0" if x % 2 else "bz1")
    s.behaviors = {(4, 2): "MB_NON_ANIMATED_DOOR", (5, 2): "MB_NON_ANIMATED_DOOR"}
    s.walk = ["XXXXXX", "XXXXXX", "XXXXDD"]
    return s


def Lr_course(X, Y):
    return L.stone_course_px(X, Y, 16, ramp=("sn4", "sn3", "sn2", "sn1"), course=4, brick=10)


# --------------------------------------------------------------------------
# Route 26 and 27's small pieces
# --------------------------------------------------------------------------

def odds():
    names = {"post": (0, 0), "start": (1, 0), "drum_L": (2, 0), "drum_R": (3, 0),
             "drag": (4, 0), "hammer": (5, 0), "rubble": (6, 0), "stele": (7, 0)}
    s = struct("odds", "Track posts, the column drum, the Hammer rock", 8, 1, SEC,
               walk=["X.XX.X.X"], names=names,
               notes="On borrowed grass. `post`: the running track's turning post, a stone "
                     "pillar (impassable); `start`: its starting sill, a grooved stone set in "
                     "the ground (walkable). `drum_L` `drum_R`: a fallen column drum lying "
                     "across a goat path, 2 x 1, that the Girdle of Herakles rolls aside; "
                     "`drag` is the path after, scraped where it went. `hammer`: a cracked "
                     "boulder the Bronze Hammer breaks; `rubble` what's left (walkable). "
                     "`stele`: a weathered boundary stone (Lakonia | Arkadia, at Karyai).")
    ground(s, "grass")
    M = s.M
    put(M, 4, 0, [
        "..4444..",
        ".433332.",
        ".433332.",
        ".433332.",
        ".433332.",
        ".433332.",
        ".433332.",
        ".433332.",
        ".433332.",
        ".433332.",
        ".433332.",
        "44333322",
        "43333321",
        "12222221",
        ".111111.",
        "..g.g.g.",
    ], {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1", "g": "gd"})
    put(M, 16 + 1, 5, [
        "44444444444444",
        "43131313131312",
        "43333333333332",
        "22222222222221",
        ".111111111111.",
    ], {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1"})
    # the drum: a fluted column drum on its side
    for y in range(16):
        for x in range(32):
            X = 32 + x
            if 2 <= y <= 13 and 1 <= x <= 30:
                c = "sn3" if (y - 2) % 3 else "sn2"
                if y in (2, 3):
                    c = "sn4"
                if y >= 12:
                    c = "sn1"
                if x in (1, 30):
                    c = "sn2"
                if x == 28 or x == 29:
                    c = "sn4" if y < 8 else "sn3"
                M.px(X, y, c)
            elif y in (14, 15) and 2 <= x <= 30 and (x + y) % 2:
                M.px(X, y, "gd")
    # the drag marks
    for x in range(2, 15):
        M.px(64 + x, 6, "gd")
        M.px(64 + x, 10, "gd")
        if x % 3 == 0:
            M.px(64 + x, 7, "g1")
    # the Hammer rock: a boulder split by a dark crack; and its rubble
    put(M, 80 + 1, 1, [
        "....4444444...",
        "..44433043332.",
        ".4433330333322",
        "44333300333322",
        "43333330333221",
        "43333303332221",
        "43333303322221",
        "33333330222221",
        "23333303222211",
        ".2222203222211",
        ".2222220222111",
        "..1111101111..",
        "...g.g.g.g.g..",
    ], {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1", "0": "sn0", "g": "gd"})
    for (rx, ry) in ((2, 4), (9, 3), (5, 9), (11, 10), (7, 6), (13, 7), (3, 12)):
        put(M, 96 + rx, ry, [".4.", "432", ".1."], {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1"})
    # boundary stele
    put(M, 112 + 4, 1, [
        "..4444..",
        ".433332.",
        "43333332",
        "43111332",
        "43333332",
        "43311332",
        "43333332",
        "43333332",
        "43333332",
        "43333332",
        "43333332",
        "22222221",
        ".111111.",
        "..g.g.g.",
    ], {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1", "g": "gd"})
    return s


def tower():
    names = {"top_L": (0, 0), "top_R": (1, 0), "mid_L": (0, 1), "mid_R": (1, 1),
             "base_L": (0, 2), "door": (1, 2)}
    s = struct("tower", "The Skiritai watchtower", 2, 3, SEC, walk=["TT", "XX", "XD"],
               names=names,
               notes="The lookout spur's watchtower: a round tower of rough stone with a "
                     "crenellated top, 2 x 3; its top is drawn over the player, its body "
                     "impassable. `door` is a dark low doorway (`MB_NON_ANIMATED_DOOR`, or "
                     "leave it closed). On borrowed grass.")
    ground(s, "grass")
    T, M = s.T, s.M
    for y in range(48):
        for x in range(32):
            a = abs(x - 15.5)
            if a > 13.5:
                continue
            if y < 6:
                if y < 2 and (x // 4) % 2 == 1:
                    continue
                c = "sn4" if y < 3 else "sn3"
                if y >= 4:
                    c = "sn1"
            elif y < 44:
                lit = x < 12
                c = L.stone_course_px(x, y, 6, ramp=("sn4" if lit else "sn3", "sn3" if lit else "sn2",
                                                     "sn2" if lit else "sn1", "sn1"),
                                      course=4, brick=7)
                if a > 12.5:
                    c = "sn1" if x > 15 else "sn2"
                if 14 <= x <= 16 and 14 <= y <= 18:
                    c = "ink"
            else:
                c = "gd" if (x + y) % 2 else "g1"
            (T if y < 16 else M).px(x, y, c)
    for y in range(36, 44):
        for x in range(19, 26):
            M.px(x, y, "ink" if x not in (19, 25) else "sn1")
    s.behaviors = {(1, 2): "MB_NON_ANIMATED_DOOR"}
    return s


def ravine():
    names = {"lip": (0, 0), "lip_b": (1, 0), "bridge_N": (2, 0),
             "chasm": (0, 1), "chasm_b": (1, 1), "bridge": (2, 1),
             "foot": (0, 2), "foot_b": (1, 2), "bridge_S": (2, 2)}
    s = struct("ravine", "A ravine and its plank bridge", 3, 3, SEC,
               walk=["XX.", "XX.", "XX."], names=names,
               notes="Route 27's ravine, running east-west across the path: `lip` (grass "
                     "dropping away) over `chasm` (dark depths) over `foot` (the far wall's "
                     "top, grass beyond); `_b` cells vary a run. The only way over is the "
                     "plank bridge, one cell wide, north to south: `bridge_N` `bridge` "
                     "`bridge_S` (Scout Othryades stands on it). Ravine impassable; the "
                     "bridge walkable.")
    import lakonia_mount as Mo
    B, M = s.B, s.M
    ground(s, "grass", [(0, 0), (1, 0), (2, 0), (0, 2), (1, 2), (2, 2)])
    for cx in range(3):
        for cy in range(3):
            Lr = B if cx == 2 else M
            for y in range(16):
                for x in range(16):
                    X, Y = cx * 16 + x, cy * 16 + y
                    if cy == 0:
                        rim = 9 + round(0.9 * math.sin(2 * math.pi * X / 16))
                        if y >= rim:
                            c = Mo.face_px(X, Y) if y > rim else "ty3"
                            if y >= 13:
                                c = "ty1" if y < 15 else "ty0"
                            Lr.px(X, Y, c)
                    elif cy == 1:
                        d = (y + 2) / 18
                        c = "ty0" if hp(x, y, 9) % 4 or d > 0.5 else "ty1"
                        B.px(X, Y, c)
                    else:
                        rim = 5 + round(0.9 * math.sin(2 * math.pi * X / 16 + 1))
                        if y < rim:
                            Lr.px(X, Y, "ty0" if y < rim - 2 else "ty1")
                        elif y == rim:
                            Lr.px(X, Y, "ty3")
                        elif y == rim + 1 and (X + Y) % 2:
                            Lr.px(X, Y, "gd")
    # the plank bridge on two ropes (wood group: draw it over its own cells)
    for cy in range(3):
        for y in range(16):
            for x in range(4, 12):
                Y = cy * 16 + y
                if cy == 0 and y < 6 or cy == 2 and y > 10:
                    continue
                c = "wd3" if (Y % 3) else "wd1"
                if x in (4, 11):
                    c = "wd0"
                (M if cy != 1 else M).px(32 + x, Y, c)
            for x in (3, 12):
                Y = cy * 16 + y
                if (cy == 0 and y < 6) or (cy == 2 and y > 10):
                    continue
                M.px(32 + x, Y, "wd2" if Y % 4 else "wd0")
    s.ground.pop((2, 0), None)
    s.ground.pop((2, 2), None)
    for (cx, cy) in ((2, 0), (2, 2)):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, cy * 16 + y
                if B.get(X, Y) is None:
                    c = L.grass_px(X, Y)
                    B.px(X, Y, "g2" if c == "g3" else c)
    return s


def build():
    return [trees(), flowers(), amyklai(), altar(), spring(), herm_shrine(), farmhouse(),
            hearth_lit(), vapheio(), odds(), tower(), ravine()]
