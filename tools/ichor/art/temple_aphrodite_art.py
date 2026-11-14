"""The Temple of Aphrodite's interior: gTileset_TempleAphrodite, Galatea's
Gallery (SCRIPT.md Part 5, SYSTEMS §12: marble and mirrors).

Three rooms one behind the other, each larger than the last: the pronaos, a
marble corridor with a statue niche, a tall bronze mirror at its end and the
painted dove; the gallery, a colonnade of Ionic columns with roses climbing
them, low statue plinths between, wall mirrors, rose petals on the floor; and
the rose court, an open courtyard of gravel paths between rose beds, with
Galatea's dais under a striped awning at its north end.

White marble veined with pink throughout. Like the Temple of Demeter it is
self-contained: every metatile is COVERED (opaque bottom, objects in the
middle layer), so it works on any interior primary (it is meant for oikos).
The statues and the turnable mirrors on stands are objects, not metatiles.
"""
from __future__ import annotations

import math

import numpy as np

import kythera_lib as K
from kythera_lib import put, struct

NEW = {
    # veined white marble, from its sunlit face to the shadow under a cornice
    "tm1": (240, 232, 232), "tm2": (224, 208, 208), "tm3": (192, 176, 184), "tm4": (152, 136, 152),
    "tdk": (64, 48, 64),
    # gravel in the rose court
    "gv1": (232, 216, 192), "gv2": (208, 192, 168), "gv3": (176, 160, 136),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, f"color name clash: {_n}"
    K.C[_n] = _c
    K.A.RGB2NAME.setdefault(_c, _n)

MARBLE = ["w0", "tm1", "tm2", "tm3", "tm4", "tdk"]
GROUPS = {
    # floors: veined marble, rose petals strewn on it
    "floor": MARBLE + ["rm3", "rm2", "rm4", "rs1", "rs2", "rs3", "rm1"],
    # walls: marble, the rose frieze, the dove fresco's sky
    "wall": MARBLE + ["rm2", "rm3", "rm4", "my2", "my3", "rs1", "rs2", "b3", "b4"],
    # bronze: the wall mirrors, the dove altar's bronze
    "bronze": MARBLE + ["bz0", "bz1", "bz2", "bz3", "vg1", "vg2", "rm3", "rs2"],
    # the rose beds and the roses climbing the columns
    "rose": ["t0", "my1", "my2", "my3", "my4", "rs1", "rs2", "rs3", "w0", "gv1", "tm3", "tm4",
             "kt1", "gv2", "gv3"],
    # the court's gravel and its marble edging
    "court": ["gv1", "gv2", "gv3", "w0", "tm1", "tm2", "tm3", "tm4", "rs2", "rs3", "rm3", "my3",
              "tdk"],
    # the awning's striped cloth, its poles, the dais
    "cloth": ["rs1", "rs2", "rs3", "w0", "tm1", "tm2", "tm3", "tm4", "kt1", "kt2", "tdk", "rm2",
              "rm3", "bz2", "bz3"],
    # Ionic columns with roses climbing them
    "column": MARBLE + ["my2", "my3", "rs1", "rs2", "rm3", "rm2"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(K.C[n] for n in names)) == len(names), g
GROUP_RGB = {g: {K.C[n] for n in names} for g, names in GROUPS.items()}

SEC = "temple"


def marble_px(X, Y, k=0):
    """Polished white marble in square slabs, faint pink veins, 16 px periodic:
    two slabs per cell, a fine joint between."""
    x, y = X % 16, Y % 16
    if x == 15 or y == 15:
        return "tm3"
    if x == 7 and y < 15:
        return "tm2"
    v = math.sin((x + 2.2 * y) / 2.6 + k) + 0.7 * math.sin((x - y) / 4.0 + 1.3 * k)
    if abs(v - 1.1) < 0.12:
        return "rm3"
    if abs(v + 0.9) < 0.1:
        return "tm2"
    return "w0" if (x * 3 + y * 5 + k) % 13 else "tm1"


def floor():
    names = {"floor": (0, 0), "floor_b": (1, 0), "petals": (2, 0), "petals_b": (3, 0),
             "inlay": (4, 0), "threshold": (5, 0), "exit": (6, 0), "void": (7, 0)}
    s = struct("floor", "Marble floors, petals, the threshold", 8, 1, SEC,
               walk=["......SX"], names=names,
               notes="Walkable white marble veined with pink: `floor` and `floor_b` (another vein, "
                     "to break up a hall), `petals` and `petals_b` (rose petals on the floor, the "
                     "gallery's and the court's edge), `inlay` (a scallop inlaid before the dais), "
                     "`threshold` (a doorway's sill between rooms). `exit` is the entrance's marble "
                     "step down (`MB_SOUTH_ARROW_WARP`: the map's bottom row, a warp on it). `void` is "
                     "black, for the border.")
    s.behaviors[(6, 0)] = "MB_SOUTH_ARROW_WARP"
    B = s.B
    for i in range(8):
        for y in range(16):
            for x in range(16):
                X = i * 16 + x
                if i == 7:
                    c = "tdk"
                else:
                    c = marble_px(X, y, 1.7 if i in (1, 3) else 0)
                B.px(X, y, c)
    for (ox, pts) in ((32, ((2, 3), (9, 2), (5, 8), (12, 10), (3, 13), (13, 4))),
                      (48, ((4, 2), (11, 6), (2, 9), (8, 12), (13, 13)))):
        for (px_, py_) in pts:
            put(B, ox + px_, py_, ["ab", ".b"], {"a": "rs2", "b": "rs1" if px_ % 2 else "rs3"})
    put(B, 64 + 2, 2, [
        "....kkkk....",
        "..kk3r3rkk..",
        ".k3r3r3r3rk.",
        "kr3r3r3r3r3k",
        "k3r3r3r3r3rk",
        ".kr3r3r3r3k.",
        "..kkr3r3kk..",
        "....kkkk....",
        ".....kk.....",
    ], {"k": "rm2", "3": "rm4", "r": "rm3"})
    for y in range(16):
        for x in range(16):
            c = "tm2" if y in (0, 15) else ("w0" if y in (1,) else ("tm1" if y < 8 else "tm2"))
            if y == 8:
                c = "tm3"
            B.px(80 + x, y, c)
    for y in range(16):
        for x in range(16):
            c = ("w0", "tm1", "tm2", "tm3")[min(3, y // 4)]
            if y % 4 == 3:
                c = "tm4"
            B.px(96 + x, y, c)
    return s


def walls():
    names = {"top": (0, 0), "top_L": (1, 0), "top_R": (2, 0), "frieze": (0, 1), "frieze_rose": (1, 1),
             "frieze_dove": (2, 1), "lower": (0, 2), "lower_niche": (1, 2), "fresco": (2, 2),
             "side_L": (3, 0), "side_R": (4, 0), "side_L_low": (3, 1), "side_R_low": (4, 1),
             "door_top": (3, 2), "door": (4, 2), "inner_L": (5, 0), "inner_R": (5, 1),
             "part": (5, 2)}
    s = struct("walls", "Walls, the frieze, the dove fresco, doorways", 6, 3, SEC,
               walk=["XXXXXX", "XXXXXX", "XXXXDX"], names=names,
               notes="A back wall is three rows: `top` (the cornice and the dark of the roof above, "
                     "`top_L` / `top_R` its corners), the frieze (`frieze`, a band of roses and "
                     "doves: `frieze_rose`, `frieze_dove`), then `lower` (the polished wall above "
                     "the floor). `lower_niche` is a niche with a low plinth (the pronaos's statue "
                     "S1 stands in one); `fresco` is the painted dove whose eye follows you (read "
                     "it). Side walls run down a room's edges: `side_L` / `side_R`, and `side_*_low` "
                     "where they meet a back wall's lower row. Between rooms, a partition is the "
                     "wall's top and lower rows (`part` is the partition's top seen from the room "
                     "south of it); its doorway is `door_top` over `door` (walkable, the threshold "
                     "into the next room; no warp needed). `inner_L` / `inner_R` are a partition's "
                     "ends against the side walls.")
    B = s.B

    def top_px(X, Y):
        y = Y % 16
        if y < 9:
            return "tdk"
        if y == 9:
            return "tm4"
        if y == 10:
            return "w0"
        if y in (11, 12):
            return ("tm1", "tm2")[(X // 2) % 2] if y == 12 else "tm1"
        if y == 13:
            return "tm3"
        return "tm2" if y == 14 else "tm3"

    def lower_px(X, Y):
        x, y = X % 16, Y % 16
        if y < 2:
            return "tm3" if y == 0 else "tm2"
        if y >= 13:
            return ("tm2", "tm3", "tm4")[y - 13]
        if x in (0, 8) and y > 2:
            return "tm2"
        return marble_px(X, Y + 3, 0.6)
    for cx in range(3):
        for y in range(16):
            for x in range(16):
                B.px(cx * 16 + x, y, top_px(cx * 16 + x, y))
    for y in range(16):
        B.px(16, y, "tm4" if y > 8 else "tdk")
        B.px(17, y, "w0" if y > 8 else "tdk")
        B.px(47, y, "tm4" if y > 8 else "tdk")
        B.px(46, y, "tm3" if y > 8 else "tdk")
    # the frieze: rose band, a garland, roses and doves in turn
    for cx in range(3):
        for y in range(16):
            for x in range(16):
                X = cx * 16 + x
                if y < 2 or y > 13:
                    c = "rm2" if y in (0, 15) else "rm4"
                else:
                    c = "rm3" if (y in (2, 13)) else "tm1"
                B.px(X, 16 + y, c)
        for x in range(16):
            yy = 8 + int(round(2.5 * math.sin(2 * math.pi * x / 16)))
            B.px(cx * 16 + x, 16 + yy, "my2")
            if x % 4 == 1:
                B.px(cx * 16 + x, 16 + yy - 1, "my3")
    put(B, 16 + 6, 16 + 4, [".aa.", "abba", "abba", ".aa."], {"a": "rs2", "b": "rs1"})
    put(B, 32 + 4, 16 + 4, [
        "..ww....",
        ".wbww...",
        "wwwwwwwt",
        "..wwwt..",
        "...tt...",
    ], {"w": "w0", "b": "tdk", "t": "tm3"})
    # lower wall, the niche, the fresco
    for cx in range(3):
        for y in range(16):
            for x in range(16):
                B.px(cx * 16 + x, 32 + y, lower_px(cx * 16 + x, 32 + y))
    put(B, 16 + 3, 32 + 1, [
        "...4444...",
        "..433334..",
        ".43dddd34.",
        "43dddddd34",
        "43dddddd34",
        "43dddddd34",
        "4wwwwwwww4",
        "4w111111w4",
        "4444444444",
    ], {"4": "tm4", "3": "tm3", "d": "tdk", "w": "w0", "1": "tm2"})
    put(B, 32 + 2, 32 + 2, [
        "rrrrrrrrrrrr",
        "rbbbbbbbbbbr",
        "rbbbwwbbbbbr",
        "rbbwkwwbbbbr",
        "rbwwwwwwwtbr",
        "rbbbwwwtbbbr",
        "rbbbbttbbbbr",
        "rbbbbbbbbbbr",
        "rrrrrrrrrrrr",
    ], {"r": "rm3", "b": "b4", "w": "w0", "k": "tdk", "t": "tm3"})
    # side walls: a thin marble wall seen from above, lit on the room side
    for (cx, side) in ((3, "L"), (4, "R")):
        for cy, low in ((0, False), (1, True)):
            for y in range(16):
                for x in range(16):
                    xx = x if side == "L" else 15 - x
                    if xx < 4:
                        c = "tdk"
                    elif xx == 4:
                        c = "tm4"
                    elif xx == 5:
                        c = "w0" if side == "L" else "tm2"
                    elif xx == 6:
                        c = "tm3"
                    else:
                        c = marble_px(cx * 16 + x, cy * 16 + y)
                        if low and y >= 13:
                            c = ("tm2", "tm3", "tm4")[y - 13]
                    B.px(cx * 16 + x, cy * 16 + y, c)
    # doorway: the lintel over the opening, then the threshold
    for y in range(16):
        for x in range(16):
            X = 48 + x
            if 3 <= x <= 12:
                c = "tdk" if y > 5 else top_px(X, y + 8)
                if y == 5:
                    c = "tm4"
            else:
                c = lower_px(X, 32 + y)
                if x in (2, 13):
                    c = "tm4"
            B.px(X, 32 + y, c)
    for y in range(16):
        for x in range(16):
            X = 64 + x
            if 3 <= x <= 12:
                c = marble_px(X, y)
                if y < 2:
                    c = "tm3"
            else:
                c = lower_px(X, 32 + y)
                if x in (2, 13):
                    c = "tm4"
            B.px(X, 32 + y, c)
    # partition top and its ends
    for y in range(16):
        for x in range(16):
            B.px(80 + x, 32 + y, top_px(80 + x, y))
    for (cy, side) in ((0, "L"), (1, "R")):
        for y in range(16):
            for x in range(16):
                xx = x if side == "L" else 15 - x
                c = "tdk" if xx < 4 else top_px(80 + x, y)
                if xx == 4 and y > 8:
                    c = "tm4"
                B.px(80 + x, cy * 16 + y, c)
    return s


def column(L, ox, oy, roses=True):
    """An Ionic column two cells tall: volutes, a fluted shaft, roses climbing."""
    put(L, ox + 1, oy + 1, [
        ".kkkkkkkkkkkk.",
        "k3ww33333ww33k",
        "k3k3kkkkkk3k3k",
        ".kk.k3333k.kk.",
        "....k3333k....",
    ], {"k": "tm4", "3": "tm2", "w": "w0"})
    for y in range(6, 30):
        for x in range(4, 12):
            c = ("tm3", "w0", "tm1", "w0", "tm1", "tm2", "tm3", "tm4")[x - 4]
            L.px(ox + x, oy + y, c)
    put(L, ox + 2, oy + 28, [
        "kkkkkkkkkkkk",
        "w11111111223",
        "kkkkkkkkkkkk",
    ], {"k": "tm4", "w": "w0", "1": "tm1", "2": "tm2", "3": "tm3"})
    if roses:
        for y in range(8, 29, 2):
            off = int(round(2.6 * math.sin(y / 2.4)))
            L.px(ox + 7 + off, oy + y, "my2")
            L.px(ox + 8 + off, oy + y + 1, "my3")
            if y % 6 == 2:
                put(L, ox + 6 + off, oy + y - 1, [".a.", "aba", ".a."], {"a": "rs2", "b": "rs1"})
        for (lx, ly) in ((3, 27), (11, 26), (4, 25)):
            put(L, ox + lx, oy + ly, ["ab", "ba"], {"a": "my2", "b": "my3"})


def gallery():
    names = {"col_top": (0, 0), "col_base": (0, 1), "col_plain_top": (1, 0),
             "col_plain_base": (1, 1), "plinth": (2, 1), "plinth_rose": (3, 1),
             "altar": (2, 0), "bench": (3, 0)}
    s = struct("gallery", "Columns, plinths, the dove altar", 4, 2, SEC,
               walk=["XXXX", "XX.."], names=names,
               notes="On the marble floor. `col_top` over `col_base`: an Ionic column with roses "
                     "climbing it (impassable); `col_plain_*` the same without. `plinth`: a low "
                     "statue plinth (walkable: the statue is an object standing on it, and steps "
                     "off it when it moves); `plinth_rose`, with a rose laid on it. `altar`: the "
                     "dove altar by the pronaos's door, where Charis stands (impassable; read it). "
                     "`bench`: a marble bench (impassable).")
    B, M = s.B, s.M
    for cx in range(4):
        for cy in range(2):
            for y in range(16):
                for x in range(16):
                    B.px(cx * 16 + x, cy * 16 + y, marble_px(cx * 16 + x, cy * 16 + y))
    column(M, 0, 0, roses=True)
    column(M, 16, 0, roses=False)
    for (ox, rose) in ((32, False), (48, True)):
        put(M, ox + 1, 16 + 5, [
            ".kkkkkkkkkkkk.",
            "kwwwwwwwwwww3k",
            "k1111111111123",
            "k2222222222233",
            ".kkkkkkkkkkkk.",
        ], {"k": "tm4", "w": "w0", "1": "tm1", "2": "tm2", "3": "tm3"})
        if rose:
            put(M, ox + 5, 16 + 4, ["ab..", ".bcc"], {"a": "rs2", "b": "rs1", "c": "my2"})
    # the dove altar: a marble block with a bronze dove and offerings
    put(M, 32 + 1, 2, [
        "..kkkkkkkkkk..",
        ".k3333333333k.",
        "kwwwwwwwwwwww3",
        "k111bb11111113",
        "k11bbbb1111123",
        "k1111b11112223",
        "k1111111112223",
        "k2222222222233",
        "kkkkkkkkkkkkkk",
    ], {"k": "tm4", "3": "tm3", "w": "w0", "1": "tm1", "2": "tm2", "b": "rm3"})
    put(M, 32 + 5, 0, [".dd..", "dDddd", "..dd."], {"d": "tm3", "D": "tdk"})
    # bench
    put(M, 48 + 1, 5, [
        "kkkkkkkkkkkkkk",
        "wwwwwwwwwwwww3",
        "k1111111111112",
        ".k.........k3.",
        ".k.........k3.",
        ".kk.......kk3.",
    ], {"k": "tm4", "w": "w0", "1": "tm1", "2": "tm2", "3": "tm3"})
    return s


def mirrors():
    names = {"mirror_tall_top": (0, 0), "mirror_tall": (0, 1), "mirror_N": (1, 1),
             "mirror_N_top": (1, 0), "mirror_E": (2, 0), "mirror_W": (3, 0), "mirror_S": (2, 1),
             "mirror_dim": (3, 1)}
    s = struct("mirrors", "Wall-hung bronze mirrors", 4, 2, SEC, walk=["XXXX", "XXXX"],
               names=names,
               notes="Polished bronze, on the walls. `mirror_tall_top` over `mirror_tall`: M0, the "
                     "pronaos's tall mirror on its end wall (frieze row, then lower row), facing "
                     "south. `mirror_N_top` over `mirror_N`: a smaller wall mirror on a back wall "
                     "(W1), facing south. `mirror_E`: a mirror on a room's east side wall, facing "
                     "west (W2), seen edge-on; `mirror_W` on a west wall, facing east. `mirror_S`: "
                     "the back of one hung on a partition's south face. `mirror_dim`: a back-wall "
                     "mirror showing a pale figure, for when it reflects a statue.")
    B, M = s.B, s.M
    from_walls = walls()
    wl = from_walls.B.a
    # backgrounds: frieze over lower for the back-wall mirrors, side walls for E/W
    for (cx, cy, sx, sy) in ((0, 0, 0, 16), (0, 1, 0, 32), (1, 0, 0, 16), (1, 1, 0, 32),
                             (2, 0, 64, 0), (3, 0, 48, 0), (2, 1, 0, 32), (3, 1, 0, 32)):
        B.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = wl[sy:sy + 16, sx:sx + 16]
    # M0: a tall oval spanning two cells
    for y in range(2, 30):
        for x in range(2, 14):
            d = math.hypot((x - 7.5) / 5.6, (y - 16) / 13.6)
            if d <= 1:
                c = "bz2"
                if d > 0.88:
                    c = "bz0"
                elif d > 0.78:
                    c = "bz1"
                elif (x - 7.5) + (y - 16) * 0.35 < -2.5:
                    c = "bz3"
                if d < 0.6 and (x + y) % 9 == 0:
                    c = "w0"
                M.px(x, y, c)
    # W1 and the dim one: a round mirror on the lower wall with a frame
    for (ox, oy, dim) in ((16, 16, False), (48, 16, True)):
        for y in range(1, 15):
            for x in range(2, 14):
                d = math.hypot((x - 7.5) / 5.6, (y - 7.5) / 6.4)
                if d <= 1:
                    c = "bz2"
                    if d > 0.86:
                        c = "bz0"
                    elif d > 0.74:
                        c = "bz1"
                    elif (x - 7.5) + (y - 7.5) < -3:
                        c = "bz3"
                    M.px(ox + x, oy + y, c)
        if dim:
            put(M, ox + 6, oy + 4, [".ww.", "wwww", ".ww.", ".ww.", "wwww"], {"w": "tm3"})
        else:
            M.px(ox + 5, oy + 4, "w0")
    # the top of W1: a bronze hook and a ribbon over the frieze
    put(M, 16 + 6, 9, [".bb.", "b..b", ".rr.", ".rr."], {"b": "bz1", "r": "rs2"})
    # mirrors on side walls, seen edge-on: a bronze slab with one glint
    for (ox, side) in ((32, "E"), (48, "W")):
        for y in range(2, 14):
            for x in (7, 8, 9) if side == "W" else (6, 7, 8):
                c = "bz2" if x == 7 else ("bz0" if (x == 8) == (side == "E") else "bz3")
                M.px(ox + x, y, c)
        M.px(ox + 7, 5, "w0")
        M.px(ox + 7, 1, "bz1")
        M.px(ox + 7, 14, "bz1")
    # the back of a mirror on a partition: a dark bronze plate and its hanger
    for y in range(3, 13):
        for x in range(4, 12):
            M.px(32 + x, 16 + y, "bz0" if (x + y) % 4 else "bz1")
    return s


def court():
    names = {"gravel": (0, 0), "gravel_b": (1, 0), "gravel_petals": (2, 0), "edge_N": (3, 0),
             "bed": (0, 1), "bed_N": (1, 1), "bed_S": (2, 1), "bed_E": (3, 1), "bed_W": (4, 1),
             "bed_NW": (5, 1), "bed_NE": (6, 1), "bed_SW": (5, 2), "bed_SE": (6, 2),
             "bed_single": (4, 0), "edge_S": (5, 0), "edge_W": (6, 0), "edge_E": (7, 0),
             "urn": (7, 1)}
    s = struct("court", "The rose court: gravel paths, rose beds", 8, 3, SEC,
               walk=["........", "XXXXXXXX", "XXXXXXX."], names=names,
               notes="The open courtyard. `gravel`, `gravel_b`, `gravel_petals`: its paths "
                     "(walkable). `edge_N` `edge_S` `edge_W` `edge_E`: a path's marble kerb along a "
                     "bed or wall (walkable). The rose beds, low marble kerbs full of roses "
                     "(impassable): `bed` (inside), `bed_N` `bed_S` `bed_E` `bed_W` (an edge, named "
                     "by the side the kerb is on), `bed_NW` ... `bed_SE` (corners), `bed_single` (a "
                     "bed one cell big). `urn`: a marble urn of roses (impassable).")
    s.walk = ["........", "XXXXXXXX", "XXXXXXX."]
    B, M = s.B, s.M

    def gravel_px(X, Y, k=0):
        h = K.hp(X, Y, 71 + k)
        c = "gv1" if h % 3 else "gv2"
        if h % 11 == 0:
            c = "gv3"
        if h % 29 == 0:
            c = "w0"
        return c
    for cx in range(8):
        for cy in range(3):
            for y in range(16):
                for x in range(16):
                    B.px(cx * 16 + x, cy * 16 + y, gravel_px(cx * 16 + x, cy * 16 + y,
                                                            1 if cx == 1 else 0))
    for (px_, py_) in ((2, 3), (9, 5), (5, 10), (12, 12), (13, 2)):
        put(B, 32 + px_, py_, ["ab"], {"a": "rs2", "b": "rs3"})
    # kerbs along a path's edge
    for (cx, side) in ((3, "N"), (5, "S"), (6, "W"), (7, "E")):
        ox = cx * 16
        for y in range(16):
            for x in range(16):
                d = {"N": y, "S": 15 - y, "W": x, "E": 15 - x}[side]
                if d < 3:
                    c = ("tm4", "w0", "tm2")[d] if side in "NW" else ("tm4", "tm3", "tm1")[d]
                    B.px(ox + x, y, c)

    def bed(cx, cy, n, s_, e, w):
        ox, oy = cx * 16, cy * 16
        mask = np.zeros((16, 16), bool)
        for y in range(16):
            for x in range(16):
                inside = (y >= 3 if n else True) and (y <= 12 if s_ else True) and \
                    (x >= 3 if w else True) and (x <= 12 if e else True)
                if inside:
                    mask[y, x] = True
                kerb = (n and 1 <= y <= 2) or (s_ and 13 <= y <= 14) or (w and 1 <= x <= 2) or \
                    (e and 13 <= x <= 14)
                if kerb and (y >= 1 if n else True) and (y <= 14 if s_ else True) and \
                        (x >= 1 if w else True) and (x <= 14 if e else True):
                    c = "w0" if (n and y == 1) or (w and x == 1) else "tm3"
                    if (s_ and y == 14) or (e and x == 14):
                        c = "tm4"
                    B.px(ox + x, oy + y, c)
        # earth then rose bushes over the inside
        for y in range(16):
            for x in range(16):
                if mask[y, x]:
                    B.px(ox + x, oy + y, "kt1")
        tmp = K.Layer(16, 16)
        import kythera_land as La
        La.foliage(tmp, mask, ("my1", "my1", "my2", "my3"), seed=cx * 7 + cy, outline="t0",
                   flowers=["rs1", "rs2", "rs1", "rs3"], fl_rate=4)
        for y in range(16):
            for x in range(16):
                if tmp.a[y, x, 3]:
                    M.px(ox + x, oy + y, tmp.get(x, y))
    bed(0, 1, False, False, False, False)
    bed(1, 1, True, False, False, False)
    bed(2, 1, False, True, False, False)
    bed(3, 1, False, False, True, False)
    bed(4, 1, False, False, False, True)
    bed(5, 1, True, False, False, True)
    bed(6, 1, True, False, True, False)
    bed(5, 2, False, True, False, True)
    bed(6, 2, False, True, True, False)
    bed(4, 0, True, True, True, True)
    # a marble urn of roses
    put(M, 112 + 3, 16 + 6, [
        ".kkkkkkkk.",
        "k3wwwwww3k",
        ".k111112k.",
        "..k1112k..",
        "...k12k...",
        "..kkkkkk..",
        ".k111122k.",
    ], {"k": "tm4", "3": "tm3", "w": "w0", "1": "tm1", "2": "tm2"})
    urn = np.zeros((16, 16), bool)
    for y in range(0, 8):
        for x in range(2, 14):
            if math.hypot((x - 7.5) / 5.5, (y - 4.5) / 4) < 1:
                urn[y, x] = True
    tmp = K.Layer(16, 16)
    import kythera_land as La
    La.foliage(tmp, urn, ("my1", "my1", "my2", "my3"), seed=3, outline="t0",
               flowers=["rs1", "rs2", "rs3"], fl_rate=3)
    for y in range(16):
        for x in range(16):
            if tmp.a[y, x, 3]:
                M.px(112 + x, 16 + y, tmp.get(x, y))
    s.behaviors = {}
    return s


def dais():
    s = struct("dais", "Galatea's dais under the awning", 4, 3, SEC,
               walk=["XXXX", "X..X", "...."], names={"awning_L": (0, 0), "stand": (1, 1),
                                                    "steps_L": (0, 2)},
               notes="The rose court's north end: a raised marble dais under a striped rose-and-"
                     "white awning on bronze-capped poles (4 x 3). Galatea stands on `stand` (1, 1); "
                     "the bottom row is the dais's steps, walkable, which is where she steps down "
                     "(beat III-1G). The awning's top row and its poles are impassable.")
    B, M = s.B, s.M
    for y in range(48):
        for x in range(64):
            B.px(x, y, marble_px(x, y))
    # dais platform rows 1-2: a raised slab with a lit edge, then steps
    for y in range(16, 48):
        for x in range(64):
            if y < 34:
                c = "w0" if (x + y) % 11 else "tm1"
                if y == 16:
                    c = "tm3"
            else:
                c = ("w0", "tm1", "tm2", "tm3")[(y - 34) % 4] if y < 46 else "tm4"
            B.px(x, y, c)
    # the scallop carved on the dais's face
    put(B, 26, 20, [
        "...kkkkkk...",
        ".kk3r3r3rkk.",
        "k3r3r3r3r3rk",
        "kr3r3r3r3r3k",
        ".kkr3r3r3kk.",
        "....kkkk....",
    ], {"k": "rm2", "3": "rm4", "r": "rm3"})
    # awning: striped cloth across the top row, scalloped valance, poles
    for y in range(0, 14):
        for x in range(64):
            stripe = (x // 6) % 2
            c = "rs2" if stripe else "w0"
            if y < 2:
                c = "rs1"
            if y >= 11:
                c = ("rs1" if stripe else "tm2") if (x % 6) in (1, 2, 3, 4) or y == 11 else None
            if c:
                M.px(x, y, c)
    for px_ in (3, 60):
        for y in range(10, 36):
            M.px(px_, y, "kt2")
            M.px(px_ + 1, y, "kt1")
        put(M, px_ - 1, 9, ["3333", "2222"], {"3": "bz3", "2": "bz2"})
    return s


def build():
    return [floor(), walls(), gallery(), mirrors(), court(), dais()]
