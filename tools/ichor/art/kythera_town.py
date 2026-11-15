"""Kythera's towns: the Cycladic house kit (white cubes, Aegean-blue doors,
rose-pink door frames, bronze mirrors by the doors, pots of roses and basil,
doves on the roofs), the great herm, Aphrodite of the Harbor's shrine, the
dovecote, Paphia's great stair, the Temple of Aphrodite's front, and the
sculptors' yard.

The house kit is parts on a grid, as Eleusa's is: a roof row (R), an upper
wall (U) and a ground-floor wall (G), each in three columns, L (the lit west
corner), M (repeats) and R (the shaded east corner). Textures are locked to
the 16 px grid, so any part sits beside any other in its row, and the fronts
in FRONTS are only arrangements of parts.
"""
from __future__ import annotations

import math

import numpy as np

import kythera_lib as K
from kythera_lib import ground, put, struct
from kythera_coast import stone_px

SEC = "town"

# --------------------------------------------------------------------------
# The Cycladic house kit
# --------------------------------------------------------------------------


def wash(X, Y):
    """Whitewash, 16 px periodic: bright, with a few soft lime smudges."""
    x, y = X % 16, Y % 16
    if (x, y) in ((4, 5), (5, 5), (11, 10), (12, 11), (2, 12)):
        return "cw1"
    return "w0"


def roof_cell(L, ox, oy, side):
    for y in range(16):
        for x in range(16):
            X, Y = ox + x, oy + y
            if y == 0:
                c = "cw3"
            elif y == 1:
                c = "w0"
            elif y == 2:
                c = "cw2"
            elif y <= 11:
                c = "cw1" if (x * 3 + y * 5) % 17 else "cw2"
                if (x + y) % 13 == 0:
                    c = "w0"
            elif y == 12:
                c = "cw2"
            elif y <= 14:
                c = "w0"
            else:
                c = "cw1"
            L.px(X, Y, c)
    if side == "L":
        for y in range(16):
            L.px(ox, oy + y, "cw3")
            L.px(ox + 1, oy + y, "w0" if y > 0 else "cw3")
        L.px(ox + 1, oy + 1, "cw3")
        L.px(ox, oy, "cw3")
        L.px(ox + 2, oy + 2, "cw2")
    if side == "R":
        for y in range(16):
            L.px(ox + 15, oy + y, "cw3")
            L.px(ox + 14, oy + y, "cw2" if 2 < y < 12 else ("cw1" if y else "cw3"))
        L.px(ox + 14, oy + 1, "cw3")
        L.px(ox + 15, oy, "cw3")


def wall_cell(L, ox, oy, row, side):
    for y in range(16):
        for x in range(16):
            X, Y = ox + x, oy + y
            c = wash(X, Y)
            if row == "U" and y < 2:
                c = "cw1" if y == 0 else ("cw1" if x % 3 else "w0")
            if row == "G":
                if y == 13:
                    c = "cw1"
                elif y == 14:
                    c = "cw2"
                elif y == 15:
                    c = "cw3"
            L.px(X, Y, c)
    if side == "L":
        for y in range(16):
            L.px(ox, oy + y, "cw3")
            if not (row == "G" and y >= 13):
                L.px(ox + 1, oy + y, "w0")
    if side == "R":
        for y in range(16):
            L.px(ox + 15, oy + y, "cw3")
            if not (row == "G" and y >= 14):
                L.px(ox + 14, oy + y, "cw2")
                L.px(ox + 13, oy + y, "cw1" if (y % 3) else L.get(ox + 13, oy + y))


def door(L, ox, oy, pink=True, arch=False):
    """A blue plank door in a rose-pink (or white) frame, a step below."""
    fr1, fr2 = ("pf1", "pf2") if pink else ("w0", "cw2")
    x0, x1 = 3, 12
    top = 1
    for y in range(top, 15):
        for x in range(x0, x1 + 1):
            if x in (x0, x1) or y == top or (y == top + 1 and x in (x0 + 1, x1 - 1)):
                c = fr1 if x != x1 else fr2
                if y == top:
                    c = fr1
            elif x in (x0 + 1, x1 - 1) or y == top + 1:
                c = fr2 if pink else "cw2"
            else:
                pl = (x - x0 - 2) % 3
                c = ("b1", "ab0", "b1")[pl] if y > top + 2 else "ab0"
                if pl == 0 and y % 4 == 0:
                    c = "b3"
            L.px(ox + x, oy + y, c)
    if arch:
        for x in range(x0, x1 + 1):
            L.px(ox + x, oy + top, "cw2" if x in (x0, x1) else fr1)
        L.px(ox + x0, oy + top, wash(ox + x0, oy + top))
        L.px(ox + x1, oy + top, wash(ox + x1, oy + top))
    L.px(ox + 9, oy + 9, "ink")       # latch
    L.px(ox + 9, oy + 8, "cw2")
    for x in range(x0 - 1, x1 + 2):    # the step
        L.px(ox + x, oy + 15, "cw2")
        L.px(ox + x, oy + 14, "w0" if x0 <= x <= x1 else L.get(ox + x, oy + 14))


def window(L, ox, oy, pink=False, y0=3):
    """Open blue shutters either side of a small dark window, a sill below."""
    put(L, ox + 2, oy + y0, [
        "bb.ffffff.bb",
        "bAbfkkkkfbAb",
        "bAbfkkkkfbAb",
        "bAbfkk3kfbAb",
        "bAbfkkkkfbAb",
        "bb.ffffff.bb",
        "...cccccc...",
    ], {"b": "ab0", "A": "b1", "f": "pf1" if pink else "cw2", "k": "ink", "3": "cw3", "c": "cw2"})


def pot(L, ox, oy, kind):
    """A terracotta pot against the wall's foot: roses or basil."""
    if kind == "rose":
        put(L, ox + 4, oy + 3, [
            "..rg.gr.",
            ".grggrgg",
            "gggrggrg",
            ".grgggg.",
            "..gggg..",
        ], {"r": "rs1", "g": "my2"})
    else:
        put(L, ox + 4, oy + 3, [
            "...gg...",
            ".gGggGg.",
            "gGggGggG",
            ".gggggg.",
            "..gggg..",
        ], {"g": "my2", "G": "kgr"})
    put(L, ox + 4, oy + 8, [
        "tttttttt",
        ".TTTTTTt",
        ".TTTTTtt",
        "..TTTtt.",
        "..tttt..",
    ], {"t": "tc1", "T": "tc2"})


def house_kit():
    names = {
        "R_L": (0, 0), "R_M": (1, 0), "R_R": (2, 0), "R_chimney": (3, 0), "R_dove": (4, 0),
        "R_doves": (5, 0), "R_jar": (6, 0),
        "U_L": (0, 1), "U_M": (1, 1), "U_R": (2, 1), "U_window": (3, 1), "U_window_pink": (4, 1),
        "U_niche": (5, 1), "U_vine": (6, 1),
        "G_L": (0, 2), "G_M": (1, 2), "G_R": (2, 2), "door": (3, 2), "door_white": (4, 2),
        "door_arch": (5, 2), "G_window": (6, 2),
        "pot_rose": (0, 3), "pot_basil": (1, 3), "mirror": (2, 3), "mirror_dim": (3, 3),
        "G_bench": (4, 3), "G_shell": (5, 3), "G_steps": (6, 3),
    }
    walk = ["XXXXXXX", "XXXXXXX", "XXXDDDX", "XXXXXXX"]
    s = struct("house", "The Cycladic house kit", 7, 4, SEC, walk=walk, names=names,
               notes="Parts that snap together into whitewashed cube houses (see *House fronts* "
                     "below). Rows: `R_*` the flat roof and its parapet, seen from above; `U_*` the "
                     "upper wall; `G_*` and the doors, the ground-floor wall on its grey-washed foot. "
                     "Columns `_L` (the lit west corner), `_M` (repeat it), `_R` (the shaded east "
                     "corner). Roof extras: `R_chimney`, `R_dove` / `R_doves` (Paphia's roofs), "
                     "`R_jar` (a water jar on the roof). Upper-wall extras: `U_window` (blue "
                     "shutters), `U_window_pink`, `U_niche` (a little lamp niche), `U_vine` (a vine "
                     "trained over the wall). Doors (`MB_NON_ANIMATED_DOOR`, put the warp here): "
                     "`door` (Aegean blue in a rose-pink frame), `door_white` (the same in a white "
                     "frame, for Skandeia's plainer houses), `door_arch` (an arched doorway). "
                     "Ground-wall extras: `G_window`, "
                     "`pot_rose`, `pot_basil` (a pot on the step), `mirror` (a polished bronze "
                     "mirror by the door, Paphia's custom) and `mirror_dim` (the same, a dim figure "
                     "in it), `G_bench` (a whitewashed bench), `G_shell` (a scallop shell set in the "
                     "wall), `G_steps` (an outside stair up to the roof). Every cell is impassable "
                     "except the doors.")
    L = s.B
    for cx, side in ((0, "L"), (1, "M"), (2, "R"), (3, "M"), (4, "M"), (5, "M"), (6, "M")):
        roof_cell(L, cx * 16, 0, side)
    for cx, side in ((0, "L"), (1, "M"), (2, "R"), (3, "M"), (4, "M"), (5, "M"), (6, "M")):
        wall_cell(L, cx * 16, 16, "U", side)
    for cx, side in ((0, "L"), (1, "M"), (2, "R"), (3, "M"), (4, "M"), (5, "M"), (6, "M")):
        wall_cell(L, cx * 16, 32, "G", side)
    for cx in range(7):
        wall_cell(L, cx * 16, 48, "G", "M")
    # roof extras
    put(L, 48 + 5, 2, [
        ".kkkkk.",
        "k33333k",
        "kwwwwwk",
        "kw000wk",
        "kwwwwwk",
        "kwwwwck",
        "kwwwwck",
        "kcccccc",
    ], {"k": "cw3", "3": "cw2", "w": "w0", "0": "ink", "c": "cw2"})

    def dove(x, y, flip=False):
        put(L, x, y, [
            "..ww...",
            ".wkww..",
            "pwwwwww",
            "..wwwc2",
            "...cc..",
            "...p.p.",
        ], {"w": "w0", "k": "ink", "p": "pf2", "c": "cw2", "2": "cw3"}, hflip=flip)
    dove(64 + 5, 7)
    dove(80 + 1, 7)
    dove(80 + 8, 6, flip=True)
    put(L, 96 + 4, 3, [
        "..kkk...",
        ".kTTTk..",
        "kTttttk.",
        "kTttttk.",
        "kTttttk.",
        ".kttttk.",
        "..kkkk..",
        ".cccccc.",
    ], {"k": "tc1", "T": "tc2", "t": "tc2", "c": "cw2"})
    # upper-wall extras
    window(L, 48, 16)
    window(L, 64, 16, pink=True)
    put(L, 80 + 5, 16 + 3, [
        ".cccc.",
        "c3333c",
        "c3kk3c",
        "c3kt3c",
        "cccccc",
    ], {"c": "cw2", "3": "cw1", "k": "ink", "t": "tc2"})
    for (vx, vy) in ((1, 2), (3, 4), (5, 3), (7, 6), (9, 5), (11, 8), (13, 7), (2, 9), (6, 10),
                     (10, 12), (4, 13), (12, 11), (8, 2), (14, 4)):
        put(L, 96 + vx, 16 + vy, ["gG", ".g"], {"g": "my2", "G": "kgr"})
    for x in range(96, 112):
        if x % 2:
            L.px(x, 16 + 1, "kgr")
    # doors
    door(L, 48, 32, pink=True)
    door(L, 64, 32, pink=False)
    door(L, 80, 32, pink=True, arch=True)
    window(L, 96, 32, y0=4)
    pot(L, 0, 48, "rose")
    pot(L, 16, 48, "basil")
    # bench
    put(L, 64 + 1, 48 + 7, [
        "cccccccccccccc",
        "wwwwwwwwwwwwww",
        "c.k........k.c",
        "c.k........k.c",
    ], {"c": "cw2", "w": "w0", "k": "cw3"})
    # scallop over the wall
    put(L, 80 + 4, 48 + 3, [
        "..cccc..",
        ".cwcwcc.",
        "cwcwcwcc",
        "cwcwcwcc",
        ".ccwcwc.",
        "..cccc..",
        "...cc...",
    ], {"c": "cw2", "w": "w0"})
    # an outside stair climbing to the roof, west to east
    for i in range(6):
        for y in range(16 - (i + 1) * 2, 16):
            for x in range(96 + 1 + i * 2, 96 + 3 + i * 2):
                if y == 16 - (i + 1) * 2:
                    c = "w0"
                elif y == 16 - (i + 1) * 2 + 1:
                    c = "cw1"
                else:
                    c = "cw1" if x % 2 else "w0"
                L.px(x, 48 + y, c)
        L.px(96 + 3 + i * 2, 48 + 16 - (i + 1) * 2, "cw2")
    s.walk = walk
    s.behaviors = {(3, 2): "MB_NON_ANIMATED_DOOR", (4, 2): "MB_NON_ANIMATED_DOOR",
                   (5, 2): "MB_NON_ANIMATED_DOOR"}
    return s


def mirrors(s):
    """Paint the bronze mirrors into the kit's mirror cells (bronze group: the
    mirror's tiles carry the wall's whites too)."""
    L = s.B
    for (cx, cy, dim) in ((2, 3, False), (3, 3, True)):
        ox, oy = cx * 16, cy * 16
        mx = ox + (2 if cx == 5 else 4)
        if cx == 5:
            # beside the door: a narrow mirror on the door's left jamb
            put(L, ox, oy + 2, [
                "..k..",
                ".kkk.",
                "k323k",
                "k333k",
                "k223k",
                "k212k",
                ".k1k.",
                "..k..",
            ], {"k": "bz0", "3": "bz3", "2": "bz2", "1": "bz1"})
            continue
        put(L, mx, oy + 1, [
            "...k....",
            "..kkk...",
            ".k1111k.",
            "k123331k",
            "k133333k",
            "k133332k",
            "k133322k",
            "k122221k",
            ".k1111k.",
            "..kkkk..",
        ], {"k": "bz0", "1": "bz1", "2": "bz2", "3": "bz3"})
        if dim:
            put(L, mx + 2, oy + 4, [".kk.", "kkkk", ".kk.", ".kk."], {"k": "bz1"})
        # a thin shadow under the mirror on the whitewash
        for x in range(mx + 1, mx + 8):
            if L.get(x, oy + 11) in ("w0", "cw1"):
                L.px(x, oy + 11, "cw1")


FRONTS = {
    "stair_house": {"title": "A house with an outside stair", "who": "a stair up to the roof terrace",
                    "rows": [["R_L", "R_M", "R_R"], ["U_L", "U_window", "U_R"],
                             ["G_steps", "door_white", "G_R"]]},
    "cube": {"title": "A cube house", "who": "the commonest Kythera house: one room, a blue door",
             "rows": [["R_L", "R_M", "R_R"], ["U_L", "U_window", "U_R"], ["G_L", "door_white", "G_R"]]},
    "cube_pot": {"title": "A cube house with roses", "who": "Skandeia: a pot of roses on the step",
                 "rows": [["R_L", "R_chimney", "R_M", "R_R"], ["U_L", "U_window", "U_M", "U_R"],
                          ["G_L", "door_white", "pot_rose", "G_R"]]},
    "long_house": {"title": "A long house", "who": "a family house, basil by the door, a bench",
                   "rows": [["R_L", "R_M", "R_jar", "R_M", "R_R"],
                            ["U_L", "U_window", "U_M", "U_window", "U_R"],
                            ["G_L", "pot_basil", "door_white", "G_bench", "G_R"]]},
    "paphia_house": {"title": "A Paphian house", "who": "Paphia: rose-pink frame, a bronze mirror by "
                                                        "the door, doves on the roof",
                     "rows": [["R_L", "R_doves", "R_M", "R_R"],
                              ["U_L", "U_window_pink", "U_vine", "U_R"],
                              ["G_L", "mirror", "door", "G_R"]]},
    "paphia_narrow": {"title": "A narrow Paphian house", "who": "Paphia's terraces",
                      "rows": [["R_L", "R_dove", "R_M", "R_R"], ["U_L", "U_niche", "U_M", "U_R"],
                               ["G_L", "door", "mirror_dim", "G_R"]]},
    "chapel_house": {"title": "A house with an arched door", "who": "a richer house, scallop over "
                                                                     "the door",
                     "rows": [["R_L", "R_M", "R_chimney", "R_R"],
                              ["U_L", "U_window_pink", "U_M", "U_R"],
                              ["G_L", "G_shell", "door_arch", "G_R"]]},
}


# --------------------------------------------------------------------------
# The great herm and Aphrodite of the Harbor
# --------------------------------------------------------------------------

def herm_shrine():
    s = struct("herm_shrine", "The great herm and the harbor shrine", 2, 2, SEC,
               walk=["TT", "XX"], names={"herm": (0, 0), "shrine": (1, 0), "herm_base": (0, 1),
                                         "shrine_base": (1, 1)},
               notes="Two 1 x 2 monuments, top cells drawn over the player. `herm`: Kythera's great "
                     "herm at the Foam Road's fork, a tall marble pillar with Hermes's bearded head, "
                     "the oil on his face long dried to a dark stain, on a plinth carved with the "
                     "roads (on borrowed grass; bg event on the plinth). `shrine`: Aphrodite of the "
                     "Harbor, a marble niche with a bronze dove, its sill heaped with old shells (on "
                     "borrowed path, at the quay's south end).")
    ground(s, "grass", [(0, 0), (0, 1)])
    ground(s, "path", [(1, 0), (1, 1)])
    M, T = s.M, s.T
    herm = [
        "....kkkkkk......",
        "...k333332k.....",
        "...k3bb3b2k.....",
        "..k33bbbb32k....",
        "..k3bkbbkb2k....",
        "..k33bbbb32k....",
        "..kk3ooo32kk....",
        "...ko11o12k.....",
        "...ko1111o2k....",
        "...kooooo2k.....",
        "....k3332k......",
        "....k3332k......",
        "...kk33322kk....",
        "...k3333222k....",
        "...k3333222k....",
        "...k3333222k....",
        "...k333k222k....",
        "...k333k222k....",
        "...k3333222k....",
        "...k3333222k....",
        "...k3333222k....",
        "..kkkkkkkkkkk...",
        "..k333333322k...",
        "..k3k3k3k322k...",
        "..k333333322k...",
        "..k3kk3k3k22k...",
        "..k333333322k...",
        ".kkkkkkkkkkkkk..",
        ".k33333333332k..",
        ".k22222222222k..",
        ".kkkkkkkkkkkkk..",
    ]
    for j, row in enumerate(herm):
        for i, ch in enumerate(row):
            c = {"k": "cw3", "3": "w0", "2": "cw2", "b": "cw1", "o": "bz1", "1": "bz0"}.get(ch)
            if c:
                (T if 1 + j < 16 else M).px(i, 1 + j, c)
    for y in range(1 + 31, 16 + 16):
        pass
    # the shrine: a pedimented niche with a bronze dove, shells on the sill
    shrine = [
        "......kk........",
        "....kk33kk......",
        "..kk333333kk....",
        ".k2222222222k...",
        ".kkkkkkkkkkkk...",
        ".k3k......k2k...",
        ".k3k......k2k...",
        ".k3k..dd..k2k...",
        ".k3k.dddd.k2k...",
        ".k3kdDddd.k2k...",
        ".k3k..dd..k2k...",
        ".k3k..kk..k2k...",
        ".k3kkkkkkkk2k...",
        "kk3333333332kk..",
        "k3ssssssssss2k..",
        "k3sSsSsSsSss2k..",
        "kkkkkkkkkkkkkk..",
        ".k33333333332k..",
        ".k32222222222k..",
        ".k32222222222k..",
        ".k32222222222k..",
        ".kkkkkkkkkkkkk..",
    ]
    for j, row in enumerate(shrine):
        for i, ch in enumerate(row):
            c = {"k": "cw3", "3": "w0", "2": "cw2", "d": "bz2", "D": "bz3", "s": "cw1",
                 "S": "pl", ".": None}.get(ch)
            if ch == "." and 5 <= j <= 11 and 4 <= i <= 9:
                c = "bz0"
            if c:
                (T if j + 2 < 16 else M).px(16 + 1 + i, 2 + j, c)
    return s


# --------------------------------------------------------------------------
# The dovecote
# --------------------------------------------------------------------------

def dovecote():
    s = struct("dovecote", "A dovecote", 2, 3, SEC, walk=["TT", "XX", "XD"],
               names={"top": (0, 0), "door": (1, 2)},
               notes="Paphia's dovecotes: a whitewashed tower, its upper walls pierced in triangles "
                     "and diamonds for the doves, a pyramid cap with doves on it (drawn over the "
                     "player), a low door. 2 x 3; the door (`MB_NON_ANIMATED_DOOR`) is the dovecote "
                     "household's way in.")
    L, T = s.B, s.T
    ground(s, "grass", [(0, 0), (1, 0)])
    s.ground = {(0, 0): "grass", (1, 0): "grass"}
    for y in range(16, 48):
        for x in range(32):
            c = wash(x, y)
            if x in (0, 31):
                c = "cw3"
            elif x == 1:
                c = "w0"
            elif x >= 29:
                c = "cw2"
            if y == 47:
                c = "cw3"
            elif y == 46:
                c = "cw2"
            L.px(x, y, c)
    # cap: a white pyramid roof over the top cell and into the second
    for y in range(4, 20):
        half = 2 + (y - 4) * 0.95
        for x in range(32):
            if abs(x - 15.5) <= half:
                c = "w0" if x < 15.5 - half / 3 else ("cw1" if x < 15.5 + half / 3 else "cw2")
                if abs(x - 15.5) > half - 1:
                    c = "cw3"
                if y == 19:
                    c = "cw3"
                (T if y < 16 else L).px(x, y, c)
    put(T, 13, 1, ["..ww..", ".wkww.", "pwwwww", "..cc.."], {"w": "w0", "k": "ink", "p": "pf2",
                                                             "c": "cw2"})
    # dove-holes: rows of triangles and diamonds
    for (row_y, kind) in ((22, "tri"), (28, "dia"), (34, "tri")):
        for i, hx in enumerate(range(4, 28, 6)):
            if kind == "tri":
                put(L, hx, row_y, ["..k..", ".kkk.", "kkkkk"], {"k": "ink"})
            else:
                put(L, hx, row_y, ["..k..", ".kkk.", "..k.."], {"k": "ink"})
    # the door and a perched dove on the sill
    put(L, 16 + 4, 32 + 3, [
        "pppppppp",
        "pbbbbbbp",
        "pbAbAbAp",
        "pbAbAbAp",
        "pbAbAbAp",
        "pbAbAbAp",
        "pbAbAbAp",
        "pbbbbbbp",
        "pbbbbkbp",
        "pbbbbbbp",
        "pbbbbbbp",
        "cccccccc",
    ], {"p": "pf1", "b": "ab0", "A": "b1", "k": "ink", "c": "cw2"})
    put(L, 5, 40, ["..ww...", ".wkww..", "pwwwwww", "..cc..."], {"w": "w0", "k": "ink", "p": "pf2",
                                                                  "c": "cw2"})
    return s


# --------------------------------------------------------------------------
# Paphia's great stair
# --------------------------------------------------------------------------

def great_stair():
    names = {"L": (0, 0), "M": (1, 0), "R": (2, 0), "land_L": (0, 1), "land": (1, 1),
             "land_R": (2, 1), "foot_L": (0, 2), "foot": (1, 2), "foot_R": (2, 2)}
    s = struct("great_stair", "Paphia's great stair", 3, 3, SEC,
               walk=["X.X", "X.X", "X.X"], names=names,
               notes="White marble steps between rose-pink balustrades, straight up the hill's spine "
                     "to the temple. A flight is `L` `M`... `R` (repeat `M` for width, stack rows for "
                     "height); `land_*` is a landing between flights, `foot_*` the first, wider "
                     "step at the bottom. The steps are walkable; the balustrade cells are not.")
    L = s.B
    for cy, kind in ((0, "flight"), (1, "land"), (2, "foot")):
        for cx, side in ((0, "L"), (1, "M"), (2, "R")):
            ox, oy = cx * 16, cy * 16
            for y in range(16):
                for x in range(16):
                    X, Y = ox + x, oy + y
                    if kind == "land":
                        c = "rm5" if (x + y) % 8 else "w0"
                        if y % 8 == 7 or (x + (y // 8) * 8) % 16 == 0:
                            c = "mw2"
                    else:
                        r = y % 4
                        c = ("w0", "rm5", "rm3", "rm2")[r]
                        if kind == "foot" and y >= 12:
                            c = ("w0", "rm5", "rm4", "mw3")[r]
                    L.px(X, Y, c)
            # balustrade: a pink rail with a lit top, posts every 8 px
            if side in ("L", "R"):
                xs = range(16) if side == "L" else range(16)
                for y in range(16):
                    for x in range(16):
                        xx = x if side == "R" else 15 - x
                        if xx < 7:
                            continue
                        X, Y = ox + x, oy + y
                        if xx == 7:
                            c = "rm2" if side == "L" else "rm4"
                        elif xx == 8:
                            c = "rm4" if side == "L" else "rm5"
                        elif xx <= 12:
                            c = "rm3" if (y % 8) else "rm5"
                        else:
                            c = "g2" if (x + y) % 5 else "g1"
                        L.px(X, Y, c)
    return s


# --------------------------------------------------------------------------
# The Temple of Aphrodite, its front
# --------------------------------------------------------------------------

def temple_front():
    W, H = 7, 5
    s = struct("temple_front", "The Temple of Aphrodite", W, H, SEC,
               walk=["TTTTTTT", "XXXXXXX", "XXXXXXX", "XXXDXXX", "......."],
               names={"door": (3, 3), "ridge": (3, 0), "steps": (3, 4)},
               notes="Paphia's crown, alone at the top of the great stair: white marble veined with "
                     "pink, a roof of rose-pink tiles with doves along its ridge (the top row is "
                     "drawn over the player), a pediment carved with the goddess's scallop shell, "
                     "Ionic columns with roses climbing them, and an open bronze-framed door into the "
                     "cella. The door (3, 3) is `MB_NON_ANIMATED_DOOR`; the steps (bottom row) are "
                     "walkable.")
    L, T = s.B, s.T
    ground(s, "grass", [(x, 0) for x in range(W)])
    s.ground = {(x, 0): "grass" for x in range(W)}
    WP = W * 16

    def marble(X, Y):
        x, y = X % 16, Y % 16
        if (x + 2 * y) % 19 == 0:
            return "rm3"
        return "w0" if (x * 5 + y * 3) % 11 else "rm5"
    # roof: rose tiles, eaves sloping to both ends; row 0 over the player
    for y in range(4, 22):
        inset = max(0, (12 - (y - 4)) * 2) if y < 16 else 0
        for x in range(2 + inset // 3, WP - 2 - inset // 3):
            c = ("rm4", "rm3", "rm3", "rm2")[x % 4]
            if y % 4 == 3:
                c = "rm2" if x % 4 else "rm1"
            if y == 4 or x in (2 + inset // 3, WP - 3 - inset // 3):
                c = "rm1"
            (T if y < 16 else L).px(x, y, c)
    for x in range(8, WP - 8):
        T.px(x, 3, "rm1")
        T.px(x, 4, "rm4")
    # doves along the ridge
    for i, dx in enumerate((14, 34, 52, 70, 90)):
        put(T, dx, 0, ["..ww.", ".wkww", "wwwwc", ".cc.."], {"w": "w0", "k": "cv0", "c": "mw2"},
            hflip=bool(i % 2))
    # pediment: a triangle of marble with the scallop relief, cornice below
    for y in range(20, 34):
        half = (y - 20) * 3.6 + 4
        for x in range(WP):
            if abs(x - WP / 2) <= half:
                c = marble(x, y)
                if abs(x - WP / 2) > half - 2:
                    c = "mw2" if x > WP / 2 else "w0"
                L.px(x, y, c)
    for x in range(WP):
        if abs(x - WP / 2) > (20 - 20) * 3.6 + 4 and L.get(x, 20) is None:
            pass
    # fill the pediment row's sides with roof
    for y in range(16, 34):
        for x in range(WP):
            if L.get(x, y) is None:
                c = ("rm4", "rm3", "rm3", "rm2")[x % 4]
                if y % 4 == 3:
                    c = "rm2" if x % 4 else "rm1"
                L.px(x, y, c)
    put(L, WP // 2 - 8, 22, [
        ".....kkkkkk.....",
        "...kk3w3w3wkk...",
        "..k3w3w3w3w3wk..",
        ".k3w3w3w3w3w3wk.",
        ".kw3w3w3w3w3w3k.",
        "..k3w3w3w3w3wk..",
        "...kkw3w3w3kk...",
        ".....kk33kk.....",
        "......kkkk......",
    ], {"k": "rm2", "3": "rm4", "w": "w0"})
    # cornice and frieze: row 2 top
    for x in range(WP):
        L.px(x, 34, "rm1")
        L.px(x, 35, "w0")
        L.px(x, 36, "rm4")
        for y in range(37, 41):
            L.px(x, y, "rm3" if (x // 4) % 2 else "rm5")
        L.px(x, 41, "rm2")
    # columns (Ionic) and the cella wall behind them
    cols = [6, 22, 38, 70, 86, 102]
    for y in range(42, 76):
        for x in range(WP):
            L.px(x, y, "rm0" if y < 46 else ("rm1" if (x % 16) not in (0, 15) else "rm0"))
    for cx_ in cols:
        # volute capital
        put(L, cx_ - 5, 42, [
            ".kkk..kkk..",
            "kw3k..k3wk.",
            "k3ckkkkc3k.",
            ".kk3333kk..",
        ], {"k": "rm2", "w": "w0", "3": "rm4", "c": "rm3"})
        for y in range(46, 74):
            for x in range(cx_ - 3, cx_ + 4):
                c = ("w0", "rm5", "w0", "rm5", "mw2", "rm4", "mw3")[x - (cx_ - 3)]
                L.px(x, y, c)
        put(L, cx_ - 4, 74, ["kkkkkkkkk", "w5555555m"], {"k": "rm2", "w": "w0", "5": "rm5",
                                                          "m": "mw2"})
        # roses climbing: leaves and blooms spiral up the shaft
        for y in range(48, 74, 3):
            off = int(2.5 * math.sin(y / 3.0))
            L.px(cx_ + off, y, "my2")
            L.px(cx_ + off + 1, y + 1, "my3")
            if y % 9 == 0:
                put(L, cx_ + off - 1, y - 1, [".a.", "aba", ".a."], {"a": "rm3", "b": "rm2"})
        for (lx, ly) in ((-3, 72), (3, 71), (-2, 70)):
            put(L, cx_ + lx, ly, ["ab", "ba"], {"a": "my2", "b": "my3"})
    # the door: a bronze-framed opening (bronze is out of this group: a dark
    # pink-stone frame), the cella's dark with a glimpse of the statue
    for y in range(48, 80):
        for x in range(50, 62):
            if x in (50, 61) or y == 48:
                c = "rm4"
            elif x in (51, 60) or y == 49:
                c = "rm2"
            else:
                c = "cv0" if (x + y) % 9 else "rm0"
            L.px(x, y, c)
    put(L, 54, 54, [".55.", "5ww5", ".ww.", ".ww.", "5ww5", ".ww.", ".w5."],
        {"5": "rm5", "w": "w0"})
    # steps (row 4): three marble steps across the front, walkable
    for y in range(64, 80):
        for x in range(WP):
            if y >= 76:
                pass
    for y in range(76, 80):
        for x in range(WP):
            L.px(x, y, ("w0", "rm5", "rm3", "rm2")[y - 76])
    for y in range(64, 76):
        for x in range(WP):
            if L.get(x, y) in ("rm1", "rm0") and y >= 74:
                L.px(x, y, "rm1")
    for y in range(64, 80):
        for x in range(WP):
            if y >= 64 and y < 76:
                continue
    for y in range(64, 80):
        r = (y - 64) % 4
        for x in range(WP):
            if y >= 64:
                pass
    # bottom row: steps
    for y in range(64, 80):
        for x in range(WP):
            if (x, y) and y >= 64:
                c = ("w0", "rm5", "rm3", "rm2")[(y - 64) % 4]
                L.px(x, y, c)
    # re-draw column bases and the door's foot over the top step
    for cx_ in cols:
        put(L, cx_ - 4, 64, ["kkkkkkkkk", "w5555555m"], {"k": "rm2", "w": "w0", "5": "rm5",
                                                          "m": "mw2"})
    return s


# --------------------------------------------------------------------------
# The sculptors' yard
# --------------------------------------------------------------------------

def sculptors():
    names = {"block": (0, 0), "block_face": (1, 0), "hoist": (2, 0), "bench": (3, 0),
             "chips": (4, 0), "hoist_foot": (2, 1)}
    s = struct("sculptors", "The sculptors' yard", 5, 2, SEC,
               walk=["XXTX.", "XXXXX"], names=names,
               notes="On borrowed path, for Paphia's carvers and Pygmalion's yard. `block`, a white "
                     "marble block on chocks; `block_face`, a block with a woman's face half freed "
                     "from it; `hoist` over `hoist_foot`, shear-legs with block and tackle (its top "
                     "drawn over the player); `bench`, a carving bench with mallet and chisels; "
                     "`chips`, marble chips and dust (walkable).")
    ground(s, "path", [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (2, 1)])
    s.ground = {(0, 0): "path", (1, 0): "path", (2, 0): "path", (3, 0): "path", (4, 0): "path",
                (2, 1): "path"}
    M, T = s.M, s.T

    def mblock(ox, oy, face=False):
        put(M, ox + 1, oy + 1, [
            ".kkkkkkkkkkkk.",
            "kwwwwwwwwwwwmk",
            "kw55555555555k",
            "k5555555555m5k",
            "kmmmmmmmmmmm3k",
            "k55555555555mk",
            "k5555555555m3k",
            "k55555555555mk",
            "k5555555555m3k",
            "k55555555555mk",
            "kmmmmmmmmmm33k",
            ".kkkkkkkkkkkk.",
            ".kk.......kk..",
        ], {"k": "rm2", "w": "w0", "5": "rm5", "m": "mw2", "3": "mw3"})
        if face:
            put(M, ox + 4, oy + 5, [
                ".www.",
                "wkwkw",
                "ww3ww",
                ".wmw.",
                "..w..",
            ], {"w": "w0", "k": "rm1", "3": "rm3", "m": "rm2"})
    mblock(0, 0)
    mblock(16, 0, face=True)
    # hoist: two legs meeting at the top with a pulley and a hanging hook
    for i in range(30):
        y = 1 + i
        xl = 32 + 2 + int(i * 0.15)
        xr = 32 + 13 - int(i * 0.15)
        (T if y < 16 else M).px(32 + 7 - int((30 - i) * 0.17), y, "wd2")
        (T if y < 16 else M).px(32 + 8 + int((30 - i) * 0.17), y, "wd1")
    put(T, 32 + 6, 1, ["kkkk", "k33k", "kkkk"], {"k": "wd0", "3": "wd3"})
    for y in range(4, 22):
        (T if y < 16 else M).px(32 + 8, y, "wd3")
    put(M, 32 + 7, 22, ["k.k", "kkk"], {"k": "ink"})
    # bench with tools
    put(M, 48 + 1, 4, [
        "kkkkkkkkkkkkkk",
        "k3333333333333",
        "k2222222222222",
        ".k..........k.",
        ".k..........k.",
        ".k..........k.",
        ".kk........kk.",
    ], {"k": "wd0", "3": "wd3", "2": "wd2"})
    put(M, 48 + 3, 2, ["1111.", ".kk.."], {"1": "kr1", "k": "wd1"})
    put(M, 48 + 9, 1, ["..k", ".k.", "3.."], {"k": "kr1", "3": "kr2"})
    # chips
    for (px_, py_) in ((2, 3), (7, 2), (12, 5), (4, 9), (10, 10), (1, 13), (13, 13), (7, 7)):
        put(M, 64 + px_, py_, ["wr", "rk"], {"w": "w0", "r": "rm4", "k": "rm2"})
    return s


STATUE = [
    # a draped goddess on a square plinth, lit from the upper left (16 x 32)
    "......kkkk......",
    ".....k5w55k.....",
    ".....kw555k.....",
    ".....k55m5k.....",
    "......k5mk......",
    "....kk55555kk...",
    "...k5w555555mk..",
    "...kw55555555k..",
    "...k5k55555mkmk.",
    "...kwk55555m3kk.",
    "....kk5w55m3k...",
    ".....k5w5mm3k...",
    ".....kw55m33k...",
    "....k5w55m5m3k..",
    "....kw55m55m3k..",
    "....k5w5m55m3k..",
    "...k5w55m5m53mk.",
    "...kw55m55m553k.",
    "...k5w5m55m5m3k.",
    "..k5w55m55m55m3k",
    "..kkkkkkkkkkkkkk",
    ".k44444444444443",
    ".k5555555555553k",
    ".k5w555555555m3k",
    ".k5w55kkkk555m3k",
    ".k5w55k22k555m3k",
    ".k5w55kkkk555m3k",
    ".k5w555555555m3k",
    ".k5555555555m33k",
    ".kmmmmmmmmmmm33k",
    ".kkkkkkkkkkkkkkk",
    "..33333333333333",
]
STATUE_COLORS = {"k": "mw3", "5": "rm5", "w": "w0", "m": "mw2", "3": "rm2", "4": "rm4", "2": "rm1"}


def props():
    """Paphia's street props: a marble statue of the goddess on her plinth (on
    path and on grass), and a market stall."""
    names = {"statue": (0, 0), "statue_base": (0, 1), "statue_g": (1, 0), "statue_g_base": (1, 1),
             "stall_TL": (2, 0), "stall_TR": (3, 0), "stall_BL": (2, 1), "stall_BR": (3, 1)}
    s = struct("props", "Statues and a market stall", 4, 2, SEC, walk=["TTXX", "XXXX"], names=names,
               notes="Paphia's agora and gardens. `statue` over `statue_base`: the goddess in white "
                     "marble on a square plinth, her top drawn over the player (on borrowed path; "
                     "`statue_g` / `statue_g_base` stand on grass). `stall_TL` `stall_TR` over "
                     "`stall_BL` `stall_BR`: a market stall, a striped awning on poles over a counter "
                     "of amphorae, fish and apples (on borrowed path). All impassable but the "
                     "statues' tops.")
    ground(s, "path", [(0, 0), (0, 1), (2, 0), (3, 0), (2, 1), (3, 1)])
    ground(s, "grass", [(1, 0), (1, 1)])
    M, T = s.M, s.T
    for ox in (0, 16):
        for j, row in enumerate(STATUE):
            for i, ch in enumerate(row):
                c = STATUE_COLORS.get(ch)
                if c:
                    (T if j < 16 else M).px(ox + i, j, c)
    # the stall: an awning striped in terracotta and white, on two timber poles
    ox = 32
    for y in range(2, 14):
        for x in range(1, 31):
            stripe = ((x - 1) // 4) % 2
            c = "tc1" if stripe else "w0"
            if y == 2:
                c = "wd0"
            elif y == 3:
                c = "tc0" if stripe else "kr2"
            elif y >= 12:
                # the scalloped valance
                if (x - 1) % 4 in (0, 3) and y == 13:
                    continue
                c = "tc0" if stripe else "kr1"
            if x in (1, 30) and y > 2:
                c = "wd0"
            M.px(ox + x, y, c)
    for x in (2, 29):
        for y in range(14, 22):
            M.px(ox + x, y, "wd1")
            M.px(ox + x + (1 if x == 2 else -1), y, "wd0")
    # the counter and its wares
    for y in range(20, 31):
        for x in range(1, 31):
            c = "wd2" if y < 23 else ("wd1" if (x + y) % 6 else "wd0")
            if y == 20:
                c = "wd3"
            if x in (1, 30) or y == 30:
                c = "wd0"
            M.px(ox + x, y, c)
    put(M, ox + 4, 14, [
        "..kk....kk.......rr.rr...",
        ".kttk..kttk.....rrrrrrr..",
        ".kttk..kttk.....rr.rr.r..",
        "kttttkkttttk.bbbbbbbbbb..",
        "kt22tkkt22tk.b2222bb222b.",
        ".kttk..kttk...bbbbbbbbb..",
    ], {"k": "ink", "t": "tc2", "2": "tc3", "r": "rs1", "b": "kr1", "B": "kr2"})
    return s


def build():
    h = house_kit()
    mirrors(h)
    sc = sculptors()
    return [h, herm_shrine(), dovecote(), great_stair(), temple_front(),
            K.pick(sc, ["block", "block_face", "hoist", "bench", "chips", "hoist_foot"], w=6), props()]
