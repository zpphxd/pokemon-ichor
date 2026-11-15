"""Lakonia's town: the plain flat-roofed house kit (and the Lesche, the
syssition and the agoge's barracks built from it), the beaten-sand yards, the
battle-school ring, the Persian Stoa, the chained Enyalios, a burial plot,
the Sown Field's furrows, the palaestra's colonnade and wrestling sands,
Orthia's little temple and its willows, and the rope across the Mani road.

Lakonia has no walls and no ornament to speak of: lime plaster gone tan over
mudbrick, stone footings, roofs of beaten clay, timber doors stained red.
"""
from __future__ import annotations

import math

import numpy as np

import lakonia_lib as L
from lakonia_lib import ground, put, struct

SEC = "town"
hp = L.hp

# --------------------------------------------------------------------------
# Wall, roof and footing textures (stone group)
# --------------------------------------------------------------------------


def plaster(X, Y, worn=False):
    """Lime plaster over mudbrick, tan, a little sun-bleached up top (each
    cell mirror-symmetric, so a plain wall costs two tiles)."""
    x, y = L.mx(X), Y % 16
    k = hp(x, y, 71)
    if worn and 3 <= x and 4 <= y <= 11:
        # plaster fallen away: mudbrick courses
        if (y - 4) % 3 == 2 or (x + 3 * ((y - 4) // 3)) % 6 == 0:
            return "ro1"
        return "ro2"
    if y < 6 and (k % 5 == 0 or y < 3 and k % 2):
        return "pw2"
    if k % 31 == 0:
        return "sn3"
    return "pw1"


def roof_px(X, Y):
    """A flat roof of beaten clay seen from above: cracks and grit."""
    x, y = L.mx(X), Y % 16
    k = hp(x, y, 81)
    if (x + 2 * y) % 13 == 0 and 2 < x and y % 7 < 4:
        return "ro1"
    if k % 29 == 0:
        return "pw1"
    return "ro2"


def socle(X, Y, top):
    """Rubble footing: stones with dark joints."""
    y = Y - top
    if y < 0:
        return None
    if y == 0:
        return "sn3"
    row = y // 3
    x = X % 16
    if y % 3 == 2 or (x + 4 * row) % 6 == 0:
        return "sn1"
    return "sn2" if (x + y) % 5 else "sn3"


# --------------------------------------------------------------------------
# The house kit
# --------------------------------------------------------------------------

KIT = {
    # roofs
    "RB_L": (0, 0), "RB_M": (1, 0), "RB_R": (2, 0), "R_L": (3, 0), "R_M": (4, 0), "R_R": (5, 0),
    "R_jar": (6, 0), "R_brush": (7, 0),
    "RF_L": (0, 1), "RF_M": (1, 1), "RF_R": (2, 1), "R_vent": (3, 1), "RF_jar": (4, 1),
    "T_L": (5, 1), "T_M": (6, 1), "T_R": (7, 1),
    # upper wall
    "U_L": (0, 2), "U_M": (1, 2), "U_R": (2, 2), "U_window": (3, 2), "U_shield": (4, 2),
    "U_worn": (5, 2), "U_cloak": (6, 2), "U_list": (7, 2),
    # ground floor
    "G_L": (0, 3), "G_M": (1, 3), "G_R": (2, 3), "door": (3, 3), "G_window": (4, 3),
    "G_open": (5, 3), "G_bench": (6, 3), "G_jar": (7, 3),
    # porch (the Lesche) and extras
    "P_L": (0, 4), "P_col": (1, 4), "P_gap": (2, 4), "door_porch": (3, 4), "P_R": (4, 4),
    "G_spears": (5, 4), "G_wood": (6, 4), "G_worn": (7, 4),
}

FRONTS = {
    "house": {"title": "A plain house", "who": "most Lakonian households",
              "rows": [["R_L", "R_M", "R_R"], ["U_L", "U_window", "U_R"], ["G_L", "door", "G_R"]]},
    "house_wide": {"title": "A wider house round its yard", "who": "Chilon's, Lichas's",
                   "rows": [["RB_L", "RB_M", "RB_M", "RB_R"], ["RF_L", "RF_jar", "RF_M", "RF_R"],
                            ["U_L", "U_window", "U_M", "U_R"], ["G_jar", "G_M", "door", "G_R"]]},
    "lampito": {"title": "Lampito's house: a shield over the door",
                "who": "Rhea (Lampito) and Kleon; the burial plot stands beside it",
                "rows": [["R_L", "R_brush", "R_M", "R_R"], ["U_L", "U_shield", "U_worn", "U_R"],
                         ["G_L", "door", "G_bench", "G_R"]]},
    "low_house": {"title": "A low house, one room", "who": "Gylippos's, the poorest",
                  "rows": [["R_L", "R_M", "R_R"], ["G_wood", "door", "G_R"]]},
    "syssition": {"title": "The syssition, the mess hall: long, low, no windows",
                  "who": "Dexippos the cook; the smoke hole over the cauldron",
                  "rows": [["R_L", "R_M", "R_vent", "R_M", "R_M", "R_R"],
                           ["G_L", "G_M", "G_wood", "door", "G_M", "G_R"]]},
    "barracks": {"title": "The agoge's barracks, under reed thatch",
                 "who": "Archidamos and his herd of boys",
                 "rows": [["T_L", "T_M", "T_M", "T_M", "T_M", "T_R"],
                          ["U_L", "U_cloak", "U_list", "U_M", "U_cloak", "U_R"],
                          ["G_spears", "G_open", "G_M", "door", "G_open", "G_R"]]},
    "lesche": {"title": "The Lesche, the elders' hall, with its porch",
               "who": "the elders; the Augur on its roof",
               "rows": [["RB_L", "RB_M", "RB_M", "RB_M", "RB_R"],
                        ["RF_L", "RF_M", "RF_M", "RF_M", "RF_R"],
                        ["P_L", "P_col", "door_porch", "P_col", "P_R"]]},
}


def house_kit():
    names = dict(KIT)
    w, hh = 8, 5
    walk = ["XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "XXXDXXXX", "XXXDXXXX"]
    s = struct("house", "Plain flat-roofed houses", w, hh, SEC, walk=walk, names=names,
               notes="Lakonian houses: tan lime plaster over mudbrick on a rubble footing, flat "
                     "roofs of beaten clay, timber doors stained red, no ornament. Build a front "
                     "from rows: a roof (`R_L` `R_M` `R_R` one row deep; or `RB_*` over `RF_*` "
                     "for a deeper house), an optional upper wall (`U_*`), and the ground floor "
                     "(`G_*` with the `door`). A house with no upper wall is low, one room. "
                     "`R_jar` `RF_jar` `R_brush` put a jar or a heap of brushwood on a roof; "
                     "`R_vent` is the syssition's smoke hole. `T_L` `T_M` `T_R` are reed thatch, "
                     "for the barracks. `U_window`, `U_worn` (plaster fallen off the brick), "
                     "`U_shield` (a bronze shield with the lambda hung over Lampito's door), "
                     "`U_cloak` (a red cloak on a peg), `U_list` (the herd's names painted by "
                     "the barracks door). `G_window`, `G_open` (an open doorway, dark), "
                     "`G_bench` (a stone bench), `G_jar` (a pithos), `G_spears` (a rack of "
                     "practice spears), `G_wood` (stacked firewood), `G_worn`. The Lesche's "
                     "porch: `P_L` `P_col` `P_gap` `P_R` with `door_porch` at its back. Every "
                     "cell is impassable but the doors (`MB_NON_ANIMATED_DOOR`). The fronts "
                     "below arrange them.")
    for (cx, cy), mb in list(s.behaviors.items()):
        pass
    B, T = s.B, s.T

    def cell(name):
        return names[name][0] * 16, names[name][1] * 16

    def side_edges(ox, oy, left, right, top=0, bot=16):
        for y in range(oy + top, oy + bot):
            if left:
                B.px(ox, y, "sn1")
            if right:
                B.px(ox + 15, y, "sn1")
                B.px(ox + 14, y, "sn2" if B.get(ox + 14, y) in ("pw1", "pw2", "sn3") else B.get(ox + 14, y))

    # --- roofs: back row (coping at the top), front row (coping in front),
    # single row (both)
    def roof(name, back, front, left, right):
        ox, oy = cell(name)
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, oy + y
                c = roof_px(X, Y)
                if back and y <= 1:
                    c = "pw2" if y == 0 else "pw1"
                if front and y >= 11:
                    c = ("pw2", "pw1", "sn3", "sn2", "sn1")[y - 11]
                if left and x <= 1:
                    c = "pw2" if x == 0 else ("pw1" if 2 <= y <= 10 or not front else c)
                if right and x >= 14:
                    c = "pw1" if x == 14 else "sn2"
                    if front and y >= 11:
                        c = ("pw1", "sn3", "sn2", "sn1", "sn1")[y - 11]
                B.px(X, Y, c)
        if front:
            # joist ends under the coping
            for bx in range(ox + 3, ox + 16, 6):
                if left and bx < ox + 3 or right and bx > ox + 12:
                    continue
                B.px(bx, oy + 14, "ro1")
                B.px(bx + 1, oy + 14, "ro2")
                B.px(bx, oy + 15, "ink")
                B.px(bx + 1, oy + 15, "ro1")
        if left:
            for y in range(16):
                B.px(ox, oy + y, "sn1" if y >= 11 else B.get(ox, oy + y))

    for nm, b, f in (("RB", True, False), ("RF", False, True), ("R", True, True)):
        roof(nm + "_L", b, f, True, False)
        roof(nm + "_M", b, f, False, False)
        roof(nm + "_R", b, f, False, True)
    roof("RF_jar", False, True, False, False)
    roof("R_jar", True, True, False, False)
    roof("R_brush", True, True, False, False)
    roof("R_vent", True, True, False, False)
    for nm in ("RF_jar", "R_jar"):
        ox, oy = cell(nm)
        put(B, ox + 4, oy + 1, [
            "...aaa...",
            "..abbba..",
            ".abcbbba.",
            ".abcbbbad",
            ".abbbbbad",
            "..abbbad.",
            "...aaad..",
            "....ddd..",
        ], {"a": "ro1", "b": "ro2", "c": "pw2", "d": "sn1"})
    ox, oy = cell("R_brush")
    for i, (x0, y0, x1, y1) in enumerate(((3, 3, 12, 7), (4, 6, 13, 3), (2, 6, 11, 8),
                                          (5, 8, 13, 5), (3, 5, 9, 9))):
        B.line(ox + x0, oy + y0, ox + x1, oy + y1, "ro1" if i % 2 else "sn1")
    B.line(ox + 4, oy + 9, ox + 12, oy + 9, "sn1")
    ox, oy = cell("R_vent")
    put(B, ox + 4, oy + 2, [
        "..iiiii.",
        ".iiiiiii",
        ".i0000ii",
        ".i0iii0i",
        ".i00000i",
        "..iiiii.",
        "....1...",
        "...1.1..",
    ], {"i": "sn1", "0": "ink", "1": "sn0"})
    for (x, y) in ((6, 0), (8, 1), (10, 0), (5, 1)):
        B.px(ox + x, oy + y, "sn1")

    # --- reed thatch (the barracks): bundles laid in courses, straw running
    # down each, a ragged eave
    for nm, left, right in (("T_L", True, False), ("T_M", False, False), ("T_R", False, True)):
        ox, oy = cell(nm)
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, oy + y
                u = L.mx(X)
                course = y // 4
                v = y % 4
                c = "re3" if (u + course * 3) % 4 else "re2"
                if v == 3:
                    c = "wd1" if (u + course) % 3 else "re2"
                elif v == 0 and (u + course) % 5 == 0:
                    c = "re4"
                if y == 0:
                    c = "wd0" if u % 3 == 0 else "wd1"
                if y >= 13:
                    c = ("re2", "wd1", "wd0")[y - 13]
                    if y == 15 and (u + 1) % 3 == 0:
                        c = "re2"
                if left and x <= 1:
                    c = "wd1" if x == 1 else "wd0"
                if right and x >= 14:
                    c = "re2" if x == 14 else "wd0"
                B.px(X, Y, c)

    # --- walls
    def wall(name, upper, left=False, right=False, worn=False):
        ox, oy = cell(name)
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, oy + y
                if upper:
                    c = plaster(X, Y, worn)
                    if y == 0:
                        c = "sn1"
                    elif y == 1:
                        c = "sn2" if X % 6 else "sn1"
                else:
                    c = socle(X, Y, oy + 11) or plaster(X, Y, worn)
                    if y == 15:
                        c = "sn1"
                B.px(X, Y, c)
        side_edges(ox, oy, left, right)

    for nm, up in (("U", True), ("G", False)):
        wall(nm + "_L", up, left=True)
        wall(nm + "_M", up)
        wall(nm + "_R", up, right=True)
    for nm in ("U_window", "U_shield", "U_cloak", "U_list"):
        wall(nm, True)
    wall("U_worn", True, worn=True)
    for nm in ("door", "G_window", "G_open", "G_bench", "G_jar", "G_spears", "G_wood"):
        wall(nm, False)
    wall("G_worn", False, worn=True)

    def window(ox, oy, y0):
        put(B, ox + 4, oy + y0, [
            "11111111",
            ".i0000i.",
            ".i0000i.",
            ".i0000i.",
            ".3333333",
        ], {"1": "ro1", "i": "sn1", "0": "ink", "3": "sn3"})

    window(*cell("U_window"), 4)
    window(*cell("G_window"), 3)
    # the door: red timber in a timber frame, a stone threshold
    ox, oy = cell("door")
    put(B, ox + 3, oy, [
        "1111111111",
        "1i222122i1",
        "1i222122i1",
        "1i212122i1",
        "1i212122i1",
        "1i2121221.",
        "1i2121s2i1",
        "1i2121221.",
        "1i212122i1",
        "1i212122i1",
        "1i212122i1",
        "1i222122i1",
        "1iiiiiiii1",
        "3333333333",
        "sssssssss.",
    ], {"1": "ro1", "i": "ink", "2": "lr2", "s": "sn1", "3": "sn3"})
    ox, oy = cell("door_porch")
    # open doorway
    ox, oy = cell("G_open")
    put(B, ox + 4, oy + 1, [
        "11111111",
        "1000000.",
        "10iiiii.",
        "10iiiii.",
        "10iiiii.",
        "10iiiii.",
        "10iiiii.",
        "10iiiii.",
        "10iiiii.",
        "10iiiii.",
        "10iiiii.",
        "3333333.",
    ], {"1": "ro1", "0": "ink", "i": "sn0", "3": "sn3"})
    # stone bench against the wall
    ox, oy = cell("G_bench")
    for x in range(1, 15):
        B.px(ox + x, oy + 8, "sn4")
        B.px(ox + x, oy + 9, "sn3")
        B.px(ox + x, oy + 10, "sn2")
        B.px(ox + x, oy + 11, "sn1")
    for x in (2, 3, 12, 13):
        for y in range(12, 15):
            B.px(ox + x, oy + y, "sn2" if x in (2, 12) else "sn1")
    # pithos against the wall
    ox, oy = cell("G_jar")
    put(B, ox + 3, oy + 1, [
        "...1111...",
        "..122221..",
        "...1221...",
        ".12222221.",
        "1222322221",
        "1223222221",
        "1223222221",
        "1222222221",
        "1222222211",
        ".12222211.",
        ".11222111.",
        "..111111..",
        "...1111...",
        ".ssssssss.",
    ], {"1": "ro1", "2": "ro2", "3": "pw2", "s": "sn1"})
    # firewood stacked against the wall
    ox, oy = cell("G_wood")
    for row in range(4):
        for i in range(5):
            bx = ox + 1 + i * 3 + (row % 2)
            by = oy + 3 + row * 3
            put(B, bx, by, [".1.", "121", ".1."], {"1": "ro1", "2": "pw1"})
    for x in range(1, 16):
        B.px(ox + x, oy + 15, "sn1")
    # practice spears in a rack
    ox, oy = cell("G_spears")
    for i, bx in enumerate((3, 6, 9, 12)):
        for y in range(1, 13):
            B.px(ox + bx, oy + y, "ro1" if y > 2 else "sn3")
        B.px(ox + bx, oy + 1, "sn4")
        B.px(ox + bx + 1, oy + 2 + i % 2, "sn1")
    for x in range(1, 15):
        B.px(ox + x, oy + 6, "ro1")
        B.px(ox + x, oy + 11, "ro1")
        B.px(ox + x, oy + 12, "sn1")
    # the lambda shield over Lampito's door (bronze; on the top layer, so the
    # wall keeps its own palette)
    ox, oy = cell("U_shield")
    sh = L.ellipse_mask(16, 16, 7.5, 7.0, 6.6, 6.2)
    for y in range(16):
        for x in range(16):
            if not sh[y, x]:
                continue
            d = math.hypot((x - 7.5) / 6.6, (y - 7.0) / 6.2)
            lit = -(x - 7.5) - (y - 7.0)
            c = "bz2" if lit > 1 else ("bz1" if lit > -4 else "bz0")
            if d > 0.86:
                c = "bz3" if lit > 2 else ("bz1" if lit > -3 else "bz0")
            T.px(ox + x, oy + y, c)
    put(T, ox + 5, oy + 3, ["..2..", "..2..", ".2.2.", ".2.2.", "2...2", "2...2", "2...2"],
        {"2": "lr2"})
    for x in range(3, 13):
        if T.get(ox + x, oy + 14) is None:
            T.px(ox + x, oy + 14, None)
    # a red cloak on a peg
    ox, oy = cell("U_cloak")
    put(B, ox + 4, oy + 2, [
        "...11...",
        "..a11a..",
        ".a2a12a.",
        ".a2a12a.",
        "a22a122a",
        "a22a1a2a",
        "a22a1a2a",
        "a22a1a2a",
        "a2a21a2a",
        "a2a21a2a",
        "aaa2aa1a",
        ".s.ss.s.",
    ], {"1": "lr1", "a": "lr1", "2": "lr2", "s": "sn2"})
    put(B, ox + 7, oy + 2, ["11"], {"1": "ro1"})
    # the herd's names painted on the plaster, some struck through
    ox, oy = cell("U_list")
    for i, y in enumerate(range(3, 14, 2)):
        ln = 6 + (hp(i, 3, 5) % 5)
        for x in range(3, 3 + ln):
            if (x + i) % 3 != 2:
                B.px(ox + x, oy + y, "sn1")
        if i in (2, 4):
            B.line(ox + 2, oy + y, ox + 3 + ln, oy + y, "lr1")
    for x in range(2, 14):
        B.px(ox + x, oy + 2, "sn2")
    # --- the porch: piers, its shaded depth, the door at its back
    for nm in ("P_L", "P_col", "P_gap", "door_porch", "P_R"):
        ox, oy = cell(nm)
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, oy + y
                c = "sn0" if y < 9 else "sn1"
                if y >= 12:
                    c = ("sn3", "sn4", "sn3", "sn2")[y - 12]
                B.px(X, Y, c)
    for nm, x0, x1 in (("P_L", 0, 6), ("P_col", 5, 11), ("P_R", 10, 16)):
        ox, oy = cell(nm)
        for y in range(0, 12):
            for x in range(x0, x1):
                c = "pw1"
                if x == x0:
                    c = "pw2" if nm != "P_R" else "sn2"
                elif x == x1 - 1:
                    c = "sn2"
                if y == 0:
                    c = "sn3"
                B.px(ox + x, oy + y, c)
    ox, oy = cell("door_porch")
    put(B, ox + 4, oy + 1, [
        "11111111",
        "1i2212i1",
        "1i2212i1",
        "1i2212i1",
        "1i2s12i1",
        "1i2212i1",
        "1i2212i1",
        "1i2212i1",
        "1iiiiii1",
    ], {"1": "ro1", "i": "ink", "2": "lr2", "s": "sn3"})
    # (the cloaked wall cell: the top layer is the shield only)
    s.behaviors = {(names["door"]): "MB_NON_ANIMATED_DOOR",
                   (names["door_porch"]): "MB_NON_ANIMATED_DOOR"}
    walk = [list("X" * w) for _ in range(hh)]
    for nm in ("door", "door_porch"):
        x, y = names[nm]
        walk[y][x] = "D"
    s.walk = ["".join(r) for r in walk]
    return s


# --------------------------------------------------------------------------
# Beaten-sand yards and the wrestling sands (autotiles on borrowed grass)
# --------------------------------------------------------------------------

def yard():
    def paint(s, X, Y, d):
        u, v = L.mx(X), Y % 16
        if d > 0.6:
            s.M.px(X, Y, L.yard_px(X, Y))
        elif d > -0.4:
            s.M.px(X, Y, "ya0" if (u + v) % 3 else "ya1")
        elif d > -1.4 and (u * 3 + v) % 4 == 0:
            s.M.px(X, Y, "gd")

    s = L.autotile("yard", "Beaten sand (the yards, the agoge's yard), soft-edged", SEC, paint,
                   notes="The beaten sand of house yards and the agoge's great yard, on borrowed "
                         "grass, as all 47 soft-edge shapes (kythera_lib.blob_key gives a "
                         "cell's key from a mask). Walkable. The full interior is `1|11111111`; "
                         "the battle-school ring stands on it.", seed=2.0)
    ground(s, "grass")
    return s


def sands():
    """The wrestling sands: a rectangular pit (a 3 x 3 kit) of dug sand in a
    stone kerb, on borrowed grass."""
    names = {"TL": (0, 0), "T": (1, 0), "TR": (2, 0), "L": (0, 1), "C": (1, 1), "R": (2, 1),
             "BL": (0, 2), "B": (1, 2), "BR": (2, 2), "C_b": (3, 1), "T_gap": (3, 0),
             "B_gap": (3, 2)}
    s = struct("sands", "The wrestling sands, a dug pit in a stone kerb", 4, 3, SEC,
               walk=["...." for _ in range(3)], names=names,
               notes="The palaestra's wrestling sands: soft, dug, raked pale sand sunk in a "
                     "low stone kerb, a 3 x 3 kit on borrowed grass (`TL` `T` `TR` / `L` `C` "
                     "`R` / `BL` `B` `BR`; repeat the middles). `C_b` is the sand scuffed "
                     "where two have wrestled; `T_gap` `B_gap` are the kerb's north and south "
                     "runs with a step down into the pit. Walkable throughout (a Geogrip lives "
                     "here by day).")
    ground(s, "grass")
    M = s.M
    k0, k1 = 2, 5            # the kerb runs from 2 to 5 px in from the pit's outer edge
    for nm, (cx, cy) in names.items():
        ox, oy = cx * 16, cy * 16
        n = nm in ("TL", "T", "TR", "T_gap")
        sth = nm in ("BL", "B", "BR", "B_gap")
        w = nm in ("TL", "L", "BL")
        e = nm in ("TR", "R", "BR")
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, oy + y
                u = L.mx(X)
                # distance in from the pit's outer edge on each open side
                dn = y if n else 99
                ds = 15 - y if sth else 99
                dw = x if w else 99
                de = 15 - x if e else 99
                d = min(dn, ds, dw, de)
                if d < k0:
                    continue
                if d < k1:
                    step = (nm == "T_gap" and dn == d or nm == "B_gap" and ds == d) and 5 <= x <= 10
                    if step:
                        c = ("sn4", "sn3", "sn2")[d - k0] if d - k0 < 3 else "sn2"
                    elif d == k0:
                        c = "sn4" if (dn == d or dw == d) else "sn2"
                    elif d == k1 - 1:
                        c = "sn1"
                    else:
                        c = "sn3" if (u + Y) % 6 else "sn2"
                        if (dn == d or ds == d) and x % 6 == 0 or (dw == d or de == d) and y % 6 == 0:
                            c = "sn1"
                    M.px(X, Y, c)
                    continue
                c = L.soft_sand_px(X, Y)
                if (dn == d or dw == d) and d == k1:
                    c = "ya0"
                elif (dn == d or dw == d) and d == k1 + 1:
                    c = "ya1"
                M.px(X, Y, c)
        # a shadow on the grass under the south kerb
        if sth:
            for x in range(16):
                if (x + oy) % 2 == 0 and not (w and x < k0) and not (e and x > 15 - k0):
                    M.px(ox + x, oy + 15, "gd")
    ox, oy = 48, 16
    for (fx, fy) in ((3, 3), (6, 5), (9, 4), (11, 8), (5, 10), (8, 12)):
        put(M, ox + fx, oy + fy, ["11", "1."], {"1": "ya1"})
    for x in range(2, 14):
        if x % 3 == 0:
            M.px(ox + x, oy + 7, "ya1")
    return s


# --------------------------------------------------------------------------
# The battle-school ring
# --------------------------------------------------------------------------

def ring():
    """The ring, 9 x 9 cells: a floor of raked sand 7 cells across in a low
    rounded wall. Every pixel is mirror-symmetric about the middle column, so
    Porytiles stores each west cell and its east twin once."""
    n = 9
    W = n * 16
    c0 = W / 2 - 0.5                       # 71.5: the axis of symmetry
    a, rc, band = 67.0, 44.0, 9.0          # the wall's outer half-size, corner radius, width
    cyp = c0 - 1

    def sdf(x, y):
        qx = abs(x - c0) - (a - rc)
        qy = abs(y - cyp) - (a - rc)
        out = math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0)
        return out - rc

    s = struct("ring", "The battle-school ring", n, n, SEC,
               names={"gap": (4, 8), "center": (4, 4), "NW": (0, 0), "N": (4, 0), "W": (0, 4)},
               notes="The agoge's ring (beat III-5I): a round floor of raked sand 7 cells across "
                     "in a low stone wall the cadets sit on, 9 x 9 cells in all, standing on the "
                     "yard's beaten sand (its corners meet `yard`'s interior exactly). Its gap is "
                     "the south middle cell (`gap`, the coord trigger); `center` is the middle of "
                     "the floor. Wall cells are impassable; seat the cadets on them.")
    B = s.B
    top = np.zeros((W, W), bool)
    face = np.zeros((W, W), np.int8)
    for y in range(W):
        for x in range(W):
            d = sdf(x, y)
            gap = abs(x - c0) < 9 and y > cyp + 20
            if -band <= d < 0 and not gap:
                top[y, x] = True
    fh = 4
    for y in range(W):
        for x in range(W):
            if top[y, x]:
                continue
            for k in range(1, fh + 1):
                if y - k >= 0 and top[y - k, x]:
                    face[y, x] = k
                    break
    for y in range(W):
        for x in range(W):
            u = min(x, W - 1 - x)               # mirror coordinate
            d = sdf(x, y)
            if top[y, x]:
                # stone blocks along the band; joints across it
                if abs(x - c0) <= a - rc:         # north or south straight run
                    j = (int(abs(x - c0)) + 2) % 9 == 0
                elif abs(y - cyp) <= a - rc:      # east or west straight run
                    j = (int(abs(y - cyp)) + 4) % 9 == 0
                else:
                    ang = math.atan2(abs(y - cyp) - (a - rc), abs(x - c0) - (a - rc))
                    j = (ang * rc / 9) % 1 < 0.12
                rr = -d                          # 0 at the outer edge .. band at the inner
                c = "sn3"
                if j:
                    c = "sn1"
                elif rr < 1 or rr > band - 1:
                    c = "sn2"
                elif (u * 3 + y) % 11 == 0:
                    c = "sn4"
                if y == 0 or not top[y - 1, x]:
                    c = "sn4"
                B.px(x, y, c)
            elif face[y, x]:
                k = face[y, x]
                c = ("sn2", "sn2", "sn1", "sn0")[k - 1]
                if k == 2 and (u // 4) % 2 == 0:
                    c = "sn1"
                B.px(x, y, c)
            elif d < 0:
                B.px(x, y, L.soft_sand_px(x, y))
            else:
                B.px(x, y, L.yard_px(x, y))
    # shadow under the wall's face, on the sand
    for y in range(1, W):
        for x in range(W):
            if not top[y, x] and not face[y, x] and face[y - 1, x]:
                c = B.get(x, y)
                if c in ("ya1", "ya2", "ya3"):
                    B.px(x, y, "ya0" if c != "ya3" else "ya1")
    walk = []
    for cy in range(n):
        row = ""
        for cx in range(n):
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            frac = (top[sl] | (face[sl] > 0)).mean()
            row += "X" if frac > 0.3 else "."
        walk.append(row)
    s.walk = walk
    return s


# --------------------------------------------------------------------------
# The Persian Stoa, the colonnade, Orthia's temple
# --------------------------------------------------------------------------

def tile_roof(L_, ox, oy, w, rows=16, ridge=False):
    """A roof of clay tiles seen from above: rows of pan and cover tiles."""
    for y in range(rows):
        for x in range(w):
            X, Y = ox + x, oy + y
            c = "ro2" if x % 4 in (1, 2) else "ro1"
            if x % 4 == 0:
                c = "sn1" if y % 4 else "ro1"
            if y % 4 == 3:
                c = "ro1" if x % 4 else "sn1"
            if x % 4 == 1 and y % 4 == 0:
                c = "pw1"
            L_.px(X, Y, c)


def persian(B, ox, oy):
    """A column carved as a captive Persian holding up the roof: 16 x 48."""
    rows = [
        # capital block and the raised hands
        "4444444444444444",
        "3333333333333333",
        "2222222222222222",
        "...3444444443...",
        "...2333333332...",
        "...h3.....3h....",
        "...h2.444.2h....",
        "...h2.4443.h....",
        "...h2.4443.h....",
        "...h2.4433.h....",
        "...h2.3332.h....",
        "...h2.f3f2.h....",
        "...h2.333..h....",
        "...h2.bbb2.h....",
        "...h2.bbb2.h....",
        "...hh.bbbhhh....",
        # torso in a long-sleeved tunic, belt, folded sleeves
        "...hh44443hh....",
        "...h4433332h....",
        "...4443332221...",
        "...44r3332221...",
        "...4443r32221...",
        "...44433r2221...",
        "....443332r1....",
        "....rrrrrrrr....",
        "....44333221....",
        "....44333221....",
        "....4r3332r1....",
        "....44r3r221....",
        "....443r3221....",
        "....44333221....",
        "....4433322.....",
        "....rrrrrrrr....",
        # trousers, striped, and the feet on a block
        "....443.3221....",
        "....4r3.3r21....",
        "....443.3221....",
        "....4r3.3r21....",
        "....443.3221....",
        "....4r3.3r21....",
        "....443.3221....",
        "....443.3221....",
        "...4433.33221...",
        "...1111.11111...",
        "3333333333333333",
        "4444444444444444",
        "3333333333333333",
        "2222222222222222",
        "1111111111111111",
        "1111111111111111",
    ]
    put(B, ox, oy, rows, {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1", "h": "sn3",
                          "f": "sn1", "b": "sn2", "r": "lr1"})


def stoa():
    w = 7
    s = struct("stoa", "The Persian Stoa", w, 6, SEC,
               names={"roof_L": (0, 0), "roof": (1, 0), "roof_R": (6, 0), "beam_L": (0, 1),
                      "beam": (1, 1), "beam_R": (6, 1), "col_top": (1, 2), "col_mid": (1, 3),
                      "col_base": (1, 4), "gap_top": (2, 2), "gap_mid": (2, 3),
                      "gap_base": (2, 4), "step_L": (0, 5), "step": (1, 5), "step_R": (6, 5)},
               walk=["XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXXXXX", "......."],
               notes="The Persian Stoa along the agora's east side (an object, Part 2): its "
                     "roof held up by carved men in trousers and tall hats, captives from the "
                     "war, a trace of red paint left on their clothes. Drawn 7 wide; widen it "
                     "by repeating the middle columns (`col_*` and `gap_*`, 3 tall, "
                     "alternating) and the middle `roof`, `beam` and `step` cells. The step "
                     "row is walkable; put the object's bg event on a column's base.")
    B = s.B
    tile_roof(B, 0, 0, w * 16)
    for x in range(w * 16):
        B.px(x, 14, "sn3")
        B.px(x, 15, "sn2")
    for y in range(16):
        B.px(0, y, "sn1")
        B.px(w * 16 - 1, y, "sn1")
    # the beam (architrave and a plain frieze)
    for y in range(16, 32):
        for x in range(w * 16):
            yy = y - 16
            c = ("sn4", "sn3", "sn3", "sn3", "sn2", "sn4", "sn4", "sn3", "sn3", "sn3", "sn3",
                 "sn2", "sn2", "sn1", "sn1", "sn1")[yy]
            if 5 <= yy <= 11 and x % 16 in (6, 9):
                c = "sn2"
            if x in (0, w * 16 - 1):
                c = "sn1"
            B.px(x, y, c)
    # the colonnade: dark depth behind, figures in front
    for y in range(32, 80):
        for x in range(w * 16):
            yy = y - 32
            c = "sn0" if yy < 34 else "sn1"
            B.px(x, y, c)
    for i in range(w):
        if i % 2 == 1 or i in (0, w - 1):
            persian(B, i * 16, 32 - 16)
    # the end antae: plain stone piers
    for x0 in (0, w * 16 - 6):
        for y in range(32, 80):
            for x in range(x0, x0 + 6):
                c = "sn3" if x - x0 in (1, 2) else "sn2"
                if x - x0 == 0:
                    c = "sn4" if x0 == 0 else "sn2"
                if x - x0 == 5:
                    c = "sn1"
                B.px(x, y, c)
    # steps (walkable)
    for y in range(80, 96):
        for x in range(w * 16):
            yy = y - 80
            c = ("sn4", "sn3", "sn3", "sn2", "sn1", "sn4", "sn3", "sn3", "sn2", "sn1", "sn4",
                 "sn3", "sn3", "sn2", "sn1", "sn1")[yy]
            if yy in (1, 6, 11) and ((x % 16) * 5) % 17 == 0:
                c = "sn2"
            B.px(x, y, c)
    return s


def colonnade():
    w = 5
    s = struct("colonnade", "A Doric colonnade (the palaestra's porch)", w, 3, SEC,
               names={"roof_L": (0, 0), "roof": (1, 0), "roof_R": (4, 0), "col_L": (0, 1),
                      "col": (1, 1), "gap": (2, 1), "col_R": (4, 1), "base_L": (0, 2),
                      "base_col": (1, 2), "base_gap": (2, 2), "door": (3, 2), "base_R": (4, 2)},
               walk=["XXXXX", "XXXXX", "XXXDX"],
               notes="The palaestra's porch on the wrestling sands: a tiled roof over plain "
                     "Doric columns (2 cells tall) and the court's shade behind them. Repeat "
                     "`col`/`gap` (and the roof and base under them) to lengthen it. `door` "
                     "(base row) is the palaestra's door (`MB_NON_ANIMATED_DOOR`), at the back "
                     "of the porch.")
    B = s.B
    tile_roof(B, 0, 0, w * 16, rows=12)
    for x in range(w * 16):
        for y, c in zip(range(12, 16), ("sn4", "sn3", "sn2", "sn1")):
            B.px(x, y, c)
    for y in range(16, 48):
        for x in range(w * 16):
            yy = y - 16
            c = "sn0" if yy < 20 else "sn1"
            if yy >= 27:
                c = ("sn4", "sn3", "sn2", "sn1", "sn1")[yy - 27]
            B.px(x, y, c)
    for i in range(w):
        if i in (0, 1, 4) or i == 3 and False:
            pass
    for cxp in (8, 24, 56, 72):
        for y in range(16, 43):
            yy = y - 16
            for x in range(cxp - 4, cxp + 4):
                dx = x - (cxp - 4)
                if yy <= 2:
                    c = ("sn4", "sn3", "sn2")[yy]
                    B.px(x - (1 if dx == 0 else 0), y, c)
                    if dx == 7:
                        B.px(x + 1, y, c)
                    continue
                c = ("sn2", "sn4", "sn4", "sn3", "sn3", "sn3", "sn2", "sn1")[dx]
                if dx in (2, 5) and yy % 2 == 0:
                    c = "sn3" if dx == 2 else "sn2"
                B.px(x, y, c)
    ox, oy = 48, 32
    put(B, ox + 4, oy + 0, [
        "11111111",
        "1i2212i1",
        "1i2212i1",
        "1i2s12i1",
        "1i2212i1",
        "1i2212i1",
        "1iiiiii1",
    ], {"1": "ro1", "i": "ink", "2": "lr2", "s": "sn3"})
    s.behaviors = {(3, 2): "MB_NON_ANIMATED_DOOR"}
    return s


def orthia():
    s = struct("orthia", "The sanctuary of Artemis Orthia", 3, 4, SEC,
               names={"pediment_L": (0, 0), "pediment": (1, 0), "pediment_R": (2, 0),
                      "cella_L": (0, 1), "cella": (1, 1), "cella_R": (2, 1),
                      "front_L": (0, 2), "door": (1, 2), "front_R": (2, 2),
                      "altar": (1, 3), "step_L": (0, 3), "step_R": (2, 3)},
               walk=["XXX", "XXX", "XDX", "XX."],
               notes="Orthia's little temple on the Eurotas's marshy bank, among willows: an old "
                     "gabled front of plain limestone, two columns before a dark doorway, an "
                     "altar on the steps where the cheese game is played (Kleta, the "
                     "priestess). `door` is `MB_NON_ANIMATED_DOOR`; `altar` (impassable) "
                     "takes the bg event. Stands on grass (the bottom row borrows it).")
    B, M = s.B, s.M
    # gable (pediment) and its tiled roof slopes, against borrowed grass
    ground(s, "grass", [(0, 0), (1, 0), (2, 0)])
    for y in range(16):
        for x in range(48):
            dx = abs(x + 0.5 - 24)
            ridge = 2 + dx * 0.42
            if y < ridge - 1:
                continue
            elif y < ridge + 1:
                M.px(x, y, "sn4" if x < 24 else "sn2")
            else:
                c = "sn3"
                if y >= 13:
                    c = ("sn4", "sn3", "sn1")[y - 13]
                elif dx < 12 and y > ridge + 2:
                    c = "sn2" if (x + y) % 2 else "sn3"
                M.px(x, y, c)
    put(M, 21, 7, ["..1..", ".121.", "12221", ".121."], {"1": "sn1", "2": "lr1"})
    for (x, y) in ((1, 13), (46, 13), (23, 1)):
        M.px(x, y - 1, "sn4")
    # cella front: dark doorway between two columns
    for y in range(16, 48):
        for x in range(48):
            yy = y - 16
            c = "sn0" if yy < 22 else "sn1"
            if yy < 2:
                c = ("sn3", "sn2")[yy]
            B.px(x, y, c)
    for cxp in (6, 41):
        for y in range(18, 44):
            for x in range(cxp - 4, cxp + 4):
                dx = x - (cxp - 4)
                B.px(x, y, ("sn2", "sn4", "sn4", "sn3", "sn3", "sn2", "sn2", "sn1")[dx])
        for x in range(cxp - 5, cxp + 5):
            B.px(x, 18, "sn4")
            B.px(x, 19, "sn3")
    for x in range(14, 34):
        B.px(x, 22, "ro1")
    for y in range(23, 44):
        B.px(14, y, "ro1")
        B.px(33, y, "ro1")
    for y in range(44, 48):
        for x in range(48):
            B.px(x, y, ("sn4", "sn3", "sn2", "sn1")[y - 44])
    # steps and altar on grass
    ground(s, "grass", [(0, 3), (1, 3), (2, 3)])
    for y in range(48, 64):
        for x in range(48):
            yy = y - 48
            if yy < 5:
                M.px(x, y, ("sn4", "sn3", "sn2", "sn4", "sn2")[yy])
            elif yy < 7 and (x + y) % 2:
                M.px(x, y, "gd")
    put(M, 18, 50, [
        "444444444444",
        "433333333332",
        "432222222232",
        "43r2r2r2r232",
        "432222222232",
        "433333333332",
        "222222222221",
        ".1111111111.",
        "..g.g.g.g...",
    ], {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1", "r": "lr1", "g": "gd"})
    s.behaviors = {(1, 2): "MB_NON_ANIMATED_DOOR"}
    return s


# --------------------------------------------------------------------------
# The chained Enyalios, the burial plot, the rope on the Mani road
# --------------------------------------------------------------------------

def enyalios():
    s = struct("enyalios", "The chained Enyalios", 1, 2, SEC, walk=["T", "X"],
               names={"top": (0, 0), "base": (0, 1)},
               notes="The bronze war god in the agora, his ankles bound in bronze fetters so War "
                     "will never leave Lakonia, a fresh garland hung on his chain (an object). "
                     "`top` (his helmet and spear, drawn over the player) over `base` (his "
                     "fettered legs on a plinth; impassable, the bg event). On borrowed path.")
    ground(s, "path")
    T, M = s.T, s.M
    put(T, 2, 0, [
        "......1.....",
        ".....121....",
        "....12221...",
        "...122321...",
        "...123321.a.",
        "...1g22g1.a.",
        "....1221..a.",
        "...111111.a.",
        "..12233221a.",
        ".122333322a.",
        ".12232232aa.",
        ".1v23322v1a.",
        ".1v22322v1a.",
        "..1222221.a.",
        "..1v2222v1a.",
        "..12222221a.",
    ], {"1": "bz0", "2": "bz1", "3": "bz2", "g": "ink", "v": "vg1", "a": "bz1"})
    put(T, 11, 0, ["3", "3"], {"3": "bz3"})
    put(M, 2, 16, [
        "..12222221a.",
        "..12232221a.",
        "..1222vv21a.",
        "...122.221..",
        "...1v2.2v1..",
        "...122.221..",
        "..o0oo0oo0o.",
        "..1v2.12v1..",
        "..o0oo0oo0o.",
        "..1112111ag.",
        "4444444444gg",
        "3333333333g2",
        "3311333113g2",
        "3333333333g2",
        "2222222222g2",
        ".1111111111.",
    ], {"1": "bz0", "2": "bz1", "3": "sn3", "4": "sn2", "v": "vg1", "o": "bz2", "0": "bz0",
        "a": "bz1", "g": "vg1"})
    for x in range(2, 14):
        for y in range(26, 32):
            c = M.get(x, y)
            if c == "bz1" and x < 12 and y >= 27:
                M.px(x, y, "sn2" if y < 30 else "sn1")
    return s


def burial():
    s = struct("burial", "A small burial plot", 3, 2, SEC, walk=["XXX", "XXX"],
               names={"TL": (0, 0), "T": (1, 0), "TR": (2, 0), "BL": (0, 1), "B": (1, 1),
                      "BR": (2, 1)},
               notes="A low kerb of stones round a patch of grass, two small rounded stelai "
                     "and a row of field stones: beside Lampito's house (her two children; "
                     "fragment 8's widow keeps another). Impassable. On borrowed grass; the "
                     "middle `T` and `B` repeat to widen it.")
    ground(s, "grass")
    M = s.M
    W, H = 48, 32
    for y in range(H):
        for x in range(W):
            on = (y in (3, 4) or y in (27, 28)) and 1 <= x <= 46 or \
                 (x in (1, 2) or x in (45, 46)) and 3 <= y <= 28
            if on:
                k = ((x % 16) // 3 + y // 3) % 3
                c = ("sn3", "sn4", "sn2")[k]
                if y in (4, 28) or x in (2, 46):
                    c = "sn1" if y in (28,) or x == 46 else c
                M.px(x, y, c)
            elif y in (29, 30) and 2 <= x <= 47 and (x + y) % 2:
                M.px(x, y, "gd")
    for sx in (13, 29):
        put(M, sx, 6, [
            "..4444..",
            ".443332.",
            "44333332",
            "43333322",
            "43r33r22",
            "43333322",
            "43333322",
            "43333322",
            "43333322",
            "43333322",
            "43333322",
            "11111111",
            "gggggggg",
        ], {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1", "r": "sn2", "g": "gd"})
    for i, sx in enumerate((8, 16, 24, 32, 40)):
        put(M, sx, 22, [".44.", "4332", "2221"], {"4": "sn4", "3": "sn3", "2": "sn2", "1": "sn1"})
    # a sprig of wild thyme left on one
    put(M, 15, 4, ["g.g", ".g."], {"g": "g1"})
    return s


def rope():
    s = struct("rope", "The rope across the Mani road", 3, 1, SEC, walk=["XXX"],
               names={"post_L": (0, 0), "rope": (1, 0), "post_R": (2, 0)},
               notes="Route 31's closed road south: a rope slung between two posts with a "
                     "strip of red cloth tied in the middle (`post_L` `rope` `post_R`, on "
                     "borrowed path; repeat `rope` for a wider road). Put an aethos stele "
                     "(`0x003`) beside it as the sign. Impassable until the post-game.")
    ground(s, "path")
    M = s.M
    for px_ in (6, 41):
        for y in range(2, 15):
            c = "wd2" if px_ == 6 else "wd1"
            M.px(px_, y, "wd3" if y == 2 else c)
            M.px(px_ + 1, y, "wd1")
            M.px(px_ + 2, y, "wd0")
        M.px(px_, 15, "sn1")
        M.px(px_ + 1, 15, "sn1")
        M.px(px_ + 2, 15, "sn1")
    for x in range(8, 42):
        t = (x - 8) / 33
        y = 5 + round(4 * math.sin(math.pi * t))
        M.px(x, y, "wd3" if x % 2 else "wd2")
        M.px(x, y + 1, "wd1")
    put(M, 23, 8, [".11.", "1111", ".11.", ".1.1", "1..1"], {"1": "lr1"})
    return s


# --------------------------------------------------------------------------
# The Sown Field: plough furrows, tall grass
# --------------------------------------------------------------------------

def sown():
    names = {"TL": (0, 0), "T": (1, 0), "TR": (2, 0), "L": (0, 1), "C": (1, 1), "R": (2, 1),
             "BL": (0, 2), "B": (1, 2), "BR": (2, 2), "C_teeth": (3, 1), "C_b": (3, 0)}
    s = struct("sown", "The Sown Field: plough furrows (tall grass)", 4, 3, SEC,
               walk=["GGGG", "GGGG", "GGG."], names=names,
               notes="The battle school's practice strip in the training fields: ploughed "
                     "furrows running east-west with green shoots in them. `MB_TALL_GRASS` "
                     "(cadets practice in it; on Sporadon days things come up in it). A 3 x 3 "
                     "kit on borrowed grass: `TL` `T` `TR` / `L` `C` `R` / `BL` `B` `BR`; `C_b` "
                     "is a variant interior, `C_teeth` a furrow with something white in it.")
    ground(s, "grass")
    M = s.M

    def furrow(X, Y):
        y = Y % 16
        x = X % 16
        k = hp(x, y, 101)
        ph = y % 4
        if ph == 0:
            return "kt2" if k % 5 else "my3"
        if ph == 1:
            return "kt1"
        if ph == 2:
            c = "kt1" if (x + y) % 3 else "my1"
            if (x * 3 + y) % 7 == 0:
                c = "my2"
            return c
        return "my2" if (x + 2 * (y // 4)) % 5 == 0 else ("kt2" if k % 3 else "my3")

    for (cx, cy) in [v for k_, v in names.items()]:
        nm = [k_ for k_, v in names.items() if v == (cx, cy)][0]
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, cy * 16 + y
                top = nm in ("TL", "T", "TR") and y < 3
                bot = nm in ("BL", "B", "BR") and y > 12
                left = nm in ("TL", "L", "BL") and x < 3
                right = nm in ("TR", "R", "BR") and x > 12
                if top or bot or left or right:
                    edge = (top and y == 2) or (bot and y == 13) or (left and x == 2) or (right and x == 13)
                    if edge and not ((top or bot) and (left or right)):
                        M.px(X, Y, "my1" if (X + Y) % 2 else "gd")
                    continue
                c = furrow(X, Y)
                if nm == "C_b" and hp(x, y, 7) % 9 == 0:
                    c = "my3"
                M.px(X, Y, c)
    ox, oy = 48, 16
    for (tx, ty) in ((4, 5), (10, 9), (7, 13)):
        put(M, ox + tx, oy + ty, ["w.w", "ww."], {"w": "w0"})
    return s


# --------------------------------------------------------------------------
# Willows (Orthia's grove)
# --------------------------------------------------------------------------

def willow():
    s = struct("willow", "A weeping willow", 2, 3, SEC, walk=["TT", "XX", "XX"],
               names={"TL": (0, 0), "TR": (1, 0), "ML": (0, 1), "MR": (1, 1), "BL": (0, 2),
                      "BR": (1, 2)},
               notes="Orthia's willows by the river: a weeping crown of long silvery fronds "
                     "over a dark trunk, 2 x 3; the top row is drawn over the player, the rest "
                     "is impassable. On borrowed grass.")
    ground(s, "grass")
    M, T = s.M, s.T
    W, H = 32, 48
    m = np.zeros((H, W), bool)
    for y in range(H):
        for x in range(W):
            # a dome on top, curtains of fronds hanging to ~y 40
            dome = math.hypot((x - 15.5) / 14.5, (y - 14) / 12) < 1
            hang = abs(x - 15.5) < 14.5 - max(0, y - 30) * 0.3 and 12 <= y < 41 - abs(math.sin(x * 1.3)) * 3
            if dome or hang:
                m[y, x] = True
    for y in range(28, 46):
        for x in range(13, 19):
            if abs(x - 15.5) < 1.5 + max(0, y - 41) * 0.6:
                M.px(x, y, "kt1" if x > 15 else "t0")
    for y in range(43, 48):
        for x in range(4, 28):
            if math.hypot((x - 16) / 12, (y - 45) / 2.5) < 1 and M.get(x, y) is None:
                M.px(x, y, "gd" if (x + y) % 2 else "g1")
    for y, x in zip(*np.nonzero(m)):
        x, y = int(x), int(y)
        # vertical fronds: stripes of light and shade
        stripe = (x * 3 + (x // 3)) % 5
        k = hp(x, y, 111)
        up = y == 0 or not m[y - 1, x]
        c = "my2" if stripe < 1 else ("ho2" if stripe < 3 else ("my1" if stripe < 4 else "ho1"))
        if up or (y < 12 and x < 14 and k % 4 == 0):
            c = "my3" if k % 2 else "my2"
        if not (y + 1 < H and m[y + 1, x]):
            c = "my1" if stripe < 2 else "t0"
        if k % 37 == 0 and y < 30:
            c = "my4"
        if (y > 30 and stripe == 4 and k % 2) or (28 <= y and 14 <= x <= 17 and k % 4 == 0):
            continue
        (T if y < 16 else M).px(x, y, c)
    return s


def well():
    s = struct("well", "A village well", 1, 1, SEC, walk=["X"], names={"well": (0, 0)},
               notes="A well in a village yard (the mother at the well): a low round kerb of "
                     "stone over dark water, a timber crosspiece and its bucket. On the "
                     "yard's beaten sand (it meets `yard`'s interior). Impassable.")
    B = s.B
    for y in range(16):
        for x in range(16):
            B.px(x, y, L.yard_px(x, y))
    put(B, 1, 1, [
        "..1........1..",
        "..1........1..",
        "..1222222221..",
        "..1..1..1..1..",
        "..4444444444..",
        ".433333333334.",
        "4330000000033.",
        "4300000000003.",
        "3300000000002.",
        "3330000000022.",
        ".333333333222.",
        ".122222222211.",
        "..111111111...",
        "...00.0.00....",
    ], {"1": "sn1", "2": "sn2", "3": "sn3", "4": "sn4", "0": "sn0"})
    return s


def build():
    return [house_kit(), yard(), sands(), ring(), stoa(), colonnade(), orthia(), enyalios(),
            burial(), rope(), sown(), willow(), well()]
