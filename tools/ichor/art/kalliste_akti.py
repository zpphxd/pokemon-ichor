"""Akti Town structures: the Temple of Hestia's facade, the harbor kit (quay,
steps, bollards, boats, nets, amphorae, crates) and a harbor shrine to
Poseidon. Drawn into kalliste_lib Structs; see kalliste_build.py.
"""
from __future__ import annotations

import math

from kalliste_lib import Struct
from kalliste_parts import doric_column

SEC = "akti"


# --------------------------------------------------------------------------
# Temple of Hestia (group "marble")
# --------------------------------------------------------------------------

BRONZE_DOOR = [
    "kkkkkkkkkkkk",
    "kGGgggkGGggk",
    "kGyggbkGyggk",
    "kGggggkGgggk",
    "kgbbbbkgbbbk",
    "kGggggkGgggk",
    "kGyggbkGyggk",
    "kGggggkGgggk",
    "kGggggkGgggk",
    "kGgggbkGgggk",
    "kGggoobooggk",
    "kGggoobooggk",
    "kGggggkGgggk",
    "kgbbbbkgbbbk",
    "kGggggkGgggk",
    "kGyggbkGyggk",
    "kGggggkGgggk",
    "kGggggkGgggk",
    "kGyggbkGyggk",
    "kGggggkGgggk",
    "kgbbbbkgbbbk",
    "kGggggkGgggk",
    "kGggggkGgggk",
    "kGyggbkGyggk",
    "kgbbbbkgbbbk",
    "kkkkkkkkkkkk",
]
BRONZE_KEY = {"k": "ink", "G": "g1", "g": "g0", "b": "br", "y": "fc", "o": "br"}

FLAME = [
    "    f    ",
    "   ff  f ",
    "  fcf ff ",
    " ffccff  ",
    " fcyycf  ",
    "fcyyyycf ",
    " fcyycff ",
]
FLAME_KEY = {"f": "fl", "c": "g1", "y": "fc"}

TRIPOD = [
    "kkkkkkkkkkkk",
    "kGGgggggggbk",
    " kGgggggbbk ",
    "  kkbbbbkk  ",
    "   kb  bk   ",
    "  kb    bk  ",
    "  kb    bk  ",
    " kb      bk ",
    " kb      bk ",
    " kk      kk ",
]
TRIPOD_KEY = {"k": "ink", "G": "g1", "g": "g0", "b": "br"}


def temple_hestia():
    s = Struct("temple_hestia", "Temple of Hestia, exterior", 7, 6, SEC,
               walk=["XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXDXXX", "......."],
               notes="A tetrastyle Doric front in marble: terracotta roof, a pediment with "
                     "a relief hearth in the tympanum and a bronze fire-tripod as the apex "
                     "acroterion, gilded palmettes at the corners, a triglyph frieze, bronze "
                     "doors between two lit braziers, and three steps. Door: row 4, middle "
                     "column (MB_NON_ANIMATED_DOOR). The step row is walkable.")
    L = s.B
    W = 112
    cx = 55.5
    # ---- roof, seen above the pediment: Laconian tile courses down each slope
    for y in range(0, 32):
        for x in range(W):
            lit = x < 56
            col = x % 4
            course = y % 4
            if lit:
                c = ["tc2", "tc1", "tc1", "tc0"][col]
            else:
                c = ["tc1", "tc0", "tc0", "ink"][col]
            if course == 3:
                c = "tc0" if lit else "ink"
            L.px(x, y, c)
    # ridge
    L.vline(55, 0, 31, "tc2")
    L.vline(56, 0, 31, "tc1")
    L.vline(54, 0, 31, "ink")
    L.vline(57, 0, 31, "ink")
    L.hline(0, W - 1, 0, "ink")
    L.vline(0, 0, 31, "ink")
    L.vline(W - 1, 0, 31, "ink")

    # ---- pediment: raking cornice and tympanum
    def ytop(x):
        return int(round(31 - 21 * (1 - abs(x - cx) / cx)))
    for x in range(W):
        t = ytop(x)
        L.px(x, t, "ink")
        L.px(x, t + 1, "w0")
        L.px(x, t + 2, "m1")
        L.px(x, t + 3, "m3")
        for y in range(t + 4, 32):
            L.px(x, y, "m2")
        if t + 4 <= 31:
            L.px(x, t + 4, "m4") if t + 4 < 31 else None
    L.hline(1, W - 2, 31, "m3")
    # relief: a round hearth with its fire, olive sprays either side
    hearth = [
        "     kkkk     ",
        "   kk1111kk   ",
        "  k11wwww11k  ",
        "  k1wbbbbw1k  ",
        "   kkkkkkkk   ",
    ]
    L.blit(FLAME, FLAME_KEY, 52, 17)
    L.blit(hearth, {"k": "m4", "1": "m1", "w": "w0", "b": "g0"}, 49, 24)
    for side in (-1, 1):
        for i in range(14):
            x = int(cx + side * (10 + i))
            y = 28 - int(round(3 * math.sin(math.pi * i / 13)))
            L.px(x, y, "m4")
            if i % 3 == 1:
                L.px(x, y - 1, "m1")
                L.px(x + side, y - 1, "m4")
    # apex acroterion: Hestia's fire on a bronze tripod
    L.blit(TRIPOD, TRIPOD_KEY, 50, 6)
    L.blit(FLAME, FLAME_KEY, 51, 0)
    # corner acroteria: gilded palmettes
    palm = [
        " g G g ",
        "gGkGkGg",
        " GgGgG ",
        "  kGk  ",
        " kkkkk ",
    ]
    L.blit(palm, {"g": "g0", "G": "g1", "k": "br"}, 1, 24)
    L.blit(palm, {"g": "g0", "G": "g1", "k": "br"}, W - 8, 24)

    # ---- horizontal cornice, frieze, architrave
    L.hline(0, W - 1, 32, "w0")
    L.hline(0, W - 1, 33, "m1")
    L.hline(0, W - 1, 34, "m3")
    L.pattern(["44442222"], {"4": "m4", "2": "m2"}, 0, 35, W, 1)
    L.rect(0, 36, W, 6, "m1")
    for tx in range(8, W, 16):
        for i, c in enumerate(["m4", "m2", "m5", "m2", "m5", "m2"]):
            L.vline(tx - 3 + i, 36, 41, c)
        L.hline(tx - 3, tx + 2, 43, "m3")
        L.px(tx - 2, 44, "m4")
        L.px(tx, 44, "m4")
        L.px(tx + 2, 44, "m4")
    for mx in range(16, W, 16):
        L.blit(["tt", "tt"], {"t": "tc1"}, mx - 1, 38)
    L.hline(0, W - 1, 42, "w0")
    L.rect(0, 44, W, 3, "m1")
    for tx in range(8, W, 16):
        L.px(tx - 2, 44, "m4")
        L.px(tx, 44, "m4")
        L.px(tx + 2, 44, "m4")
    L.hline(0, W - 1, 43, "m3")
    L.hline(0, W - 1, 47, "m4")
    L.vline(0, 31, 47, "ink")
    L.vline(W - 1, 31, 47, "ink")

    # ---- pronaos: the cella wall in shade behind the columns
    L.rect(1, 48, W - 2, 32, "m4")
    L.rect(1, 48, W - 2, 3, "m5")
    L.vline(0, 48, 79, "ink")
    L.vline(W - 1, 48, 79, "ink")
    # bronze doors in a marble frame
    L.rect(48, 52, 16, 28, "m1")
    L.hline(48, 63, 52, "w0")
    L.vline(48, 52, 79, "w0")
    L.vline(63, 52, 79, "m3")
    L.blit(BRONZE_DOOR, BRONZE_KEY, 50, 54)
    # braziers between the outer columns
    for bx in (24, 88):
        L.blit(TRIPOD, TRIPOD_KEY, bx - 6, 68)
        L.blit(FLAME, FLAME_KEY, bx - 5, 61)
        # firelight on the wall behind
        for (dx, dy) in ((-7, 62), (6, 62), (-8, 66), (7, 66)):
            L.px(bx + dx, dy, "m3")
    # columns, each with its shadow on the wall to the right
    ramp = ["m4", "m3", "m2", "m1", "w0"]
    for c in (8, 40, 72, 104):
        for y in range(51, 80):
            for x in range(c + 7, c + 10):
                if 0 < x < W - 1 and L.get(x, y) == "m4":
                    L.px(x, y, "m5")
        doric_column(L, c - 7, 48, 14, 32, ramp, "ink")

    # ---- stylobate and three steps
    for k, y in enumerate((80, 85, 90)):
        L.hline(0, W - 1, y, "w0")
        L.hline(0, W - 1, y + 1, "m1")
        L.hline(0, W - 1, y + 2, "m1")
        L.hline(0, W - 1, y + 3, "m2")
        L.hline(0, W - 1, y + 4, "m3")
    L.hline(0, W - 1, 95, "m5")
    L.vline(0, 80, 95, "ink")
    L.vline(W - 1, 80, 95, "ink")
    return s


# --------------------------------------------------------------------------
# Harbor (groups "stone", "wood", "clay", "sea")
# --------------------------------------------------------------------------

def quay(L, x, y, w, h):
    """Ashlar quay paving in running bond, phase-locked to the 16 px grid."""
    for j in range(h):
        for i in range(w):
            X, Y = x + i, y + j
            row = Y // 8
            off = 8 if row % 2 else 0
            bx, by = (X + off) % 16, Y % 8
            # big pale blocks with soft joints, so a wide quay reads as stone
            # paving rather than brickwork
            if bx == 15 or by == 7:
                c = "s3"
            else:
                c = "s4"
                if (bx, by) in ((1, 1), (2, 1)):
                    c = "s5"
                elif (bx, by) in ((9, 4), (10, 4), (4, 5)) and row % 2:
                    c = "s3"
            L.px(X, Y, c)


def coping_n(L, x, y, w):
    """The quay's north edge with water beyond: rounded coping stones."""
    L.hline(x, x + w - 1, y, "s1")
    L.hline(x, x + w - 1, y + 1, "s5")
    L.hline(x, x + w - 1, y + 2, "s4")
    L.hline(x, x + w - 1, y + 3, "s4")
    L.hline(x, x + w - 1, y + 4, "s2")
    for jx in range(x + 7, x + w, 16):
        L.vline(jx, y + 1, y + 4, "s1")


def quay_face(L, x, y, w, h):
    """The quay's south face, wet toward the waterline, with weed at the foot."""
    for j in range(h):
        for i in range(w):
            X, Y = x + i, y + j
            row = j // 4
            off = 8 if row % 2 else 0
            bx, by = (X + off) % 16, j % 4
            wet = j >= h - 4
            if bx == 15 or by == 3:
                c = "wt0"
            elif by == 0:
                c = "s2" if not wet else "wt1"
            else:
                c = "s1" if not wet else "wt1"
            if j == h - 1 or (j == h - 2 and X % 3 == 0):
                c = "alg"
            L.px(X, Y, c)


def harbor_quay():
    s = Struct("quay", "Harbor quay: ashlar paving, edges and corners", 5, 3, SEC,
               walk=["XX.XX", "...XX", "XX.XX"],
               notes="Big limestone blocks in running bond. Water is aethos ocean, placed "
                     "next to these. Row 0: NW outer corner, north edge (water to the north: "
                     "coping only, the face is hidden), NE outer corner, then inner corners "
                     "NW and NE (water diagonally beyond). Row 1: west edge (water west), "
                     "plain quay, east edge (water east), inner corners SW and SE. Row 2: "
                     "SW outer corner, south edge (water to the south: the wet face shows), "
                     "SE outer corner, then two plain quay alternates. Edge cells are "
                     "walkable; mark the water side impassable unless surfing.")
    L = s.B
    quay(L, 0, 0, 80, 48)
    # row 0
    coping_n(L, 0, 0, 48)
    for x0 in (0,):
        L.vline(x0, 0, 15, "s1"); L.vline(x0 + 1, 1, 15, "s5"); L.vline(x0 + 2, 2, 15, "s4")
        L.vline(x0 + 3, 2, 15, "s4"); L.vline(x0 + 4, 4, 15, "s2")
    L.vline(47, 0, 15, "s1"); L.vline(46, 1, 15, "s4"); L.vline(45, 2, 15, "s4")
    L.vline(44, 2, 15, "s3"); L.vline(43, 4, 15, "s2")
    # inner corners NW (water to the NW) and NE
    L.blit(["1555", "54  ", "5   ", "5   "], {"1": "s1", "5": "s5", "4": "s4"}, 48, 0)
    L.blit(["5551", "  45", "   4", "   4"], {"1": "s1", "5": "s4", "4": "s4"}, 76, 0)
    # row 1: west edge, plain, east edge, inner SW, inner SE
    L.vline(0, 16, 31, "s1"); L.vline(1, 16, 31, "s5"); L.vline(2, 16, 31, "s4")
    L.vline(3, 16, 31, "s4"); L.vline(4, 16, 31, "s2")
    L.vline(47, 16, 31, "s1"); L.vline(46, 16, 31, "s4"); L.vline(45, 16, 31, "s4")
    L.vline(44, 16, 31, "s3"); L.vline(43, 16, 31, "s2")
    L.blit(["5   ", "5   ", "54  ", "1155"], {"1": "s1", "5": "s5", "4": "s4"}, 48, 28)
    L.blit(["   4", "   4", "  44", "4411"], {"1": "s1", "4": "s4"}, 76, 28)
    # row 2: SW, S, SE with the face showing
    for x0 in (0, 16, 32):
        L.hline(x0, x0 + 15, 38, "s5")
        L.hline(x0, x0 + 15, 39, "s4")
        quay_face(L, x0, 40, 16, 8)
    L.vline(0, 32, 39, "s1"); L.vline(1, 32, 38, "s5"); L.vline(2, 32, 38, "s4")
    L.vline(47, 32, 39, "s1"); L.vline(46, 32, 38, "s4"); L.vline(45, 32, 38, "s3")
    L.vline(0, 40, 47, "wt0")
    L.vline(47, 40, 47, "wt0")
    return s


def harbor_steps():
    s = Struct("quay_steps", "Harbor steps down to the water", 3, 1, SEC,
               walk=["..."],
               notes="Steps cut into the quay. Left: water to the north, steps descending "
                     "away from the viewer, wet toward the sea. Middle: water to the south, "
                     "steps cut into the visible face. Right: a stone bollard with a rope, "
                     "on the north edge. Put the surf start on the water next to a step.")
    L = s.B
    quay(L, 0, 0, 48, 16)
    # north steps: 4 treads, driest at the bottom (quay level)
    treads = [("wt1", "wt0"), ("s1", "s0"), ("s2", "s1"), ("s3", "s2")]
    for k, (tr, ed) in enumerate(treads):
        y = k * 4
        L.rect(2, y, 12, 3, tr)
        L.hline(2, 13, y + 3, ed)
        L.hline(2, 13, y, "alg" if k == 0 else tr)
    for x in (0, 14):
        L.rect(x, 0, 2, 16, "s3")
    L.vline(0, 0, 15, "s4")
    L.vline(1, 0, 15, "s4")
    L.vline(14, 0, 15, "s2")
    L.vline(15, 0, 15, "s1")
    L.hline(0, 15, 0, "s1")
    # south steps in the face
    L.hline(16, 31, 6, "s5")
    L.hline(16, 31, 7, "s4")
    quay_face(L, 16, 8, 16, 8)
    yy = 8
    for k, (tr, ri) in enumerate([("s4", "s2"), ("s3", "wt1"), ("wt1", "wt0")]):
        L.rect(19, yy, 10, 1, tr)
        L.rect(19, yy + 1, 10, 2, ri)
        yy += 3
    L.rect(19, yy, 10, 16 - (yy - 0) if yy < 16 else 0, "alg")
    L.vline(18, 6, 15, "s1")
    L.vline(29, 6, 15, "s0")
    # bollard on the north edge
    coping_n(L, 32, 0, 16)
    bollard = [
        "  kkkk  ",
        " k5544k ",
        "k554433k",
        "k443322k",
        "keeeeeek",
        "k1eeee1k",
        "k332211k",
        "k322211k",
        " k2211k ",
        "  kkkk  ",
    ]
    L.blit(bollard, {"k": "sk", "5": "s5", "4": "s4", "3": "s3", "2": "s2", "1": "e1", "e": "e2"},
           36, 4)
    L.hline(37, 44, 14, "s1")
    # rope trailing to the water
    for (x, y) in ((44, 8), (45, 7), (46, 6), (46, 5), (47, 4), (47, 3)):
        L.px(x, y, "e2")
    return s


# ---- boats ----

def sea(L, x, y, w, h):
    """Open water matching aethos's deep sea: b1 with wr ripple strokes."""
    L.rect(x, y, w, h, "b1")
    rip = [(7, 0), (8, 1), (8, 2), (9, 3), (9, 4), (10, 5), (11, 6), (12, 6), (13, 7), (14, 7),
           (15, 8), (0, 9), (0, 10), (1, 11), (1, 12), (2, 13), (3, 14), (4, 14), (5, 15), (6, 15)]
    for j in range(y, y + h):
        for i in range(x, x + w):
            if ((i % 16), (j % 16)) in rip:
                L.px(i, j, "wr")


def boat_eye(L, x, y):
    """The oculus painted on the bow: a white almond with a dark pupil."""
    eye = [
        "  kkk  ",
        " kwwbk ",
        "kwwbbwk",
        " kkkkk ",
    ]
    L.blit(eye, {"k": "ink", "w": "w0", "b": "b0"}, x, y)


def kaiki():
    s = Struct("boat_kaiki", "Moored kaiki with painted eyes", 3, 2, SEC,
               walk=["XXX", "XXX"],
               notes="A fishing kaiki moored side-on, bow to the right: white hull with a "
                     "blue gunwale and red boot-top, an eye on the bow, a short mast with a "
                     "furled sail and a little stern awning. Two layers: sea below, boat over "
                     "it. The sea matches aethos's deep water but does not animate.")
    B, M = s.B, s.M
    sea(B, 0, 0, 48, 32)
    # shadow and foam on the water around the hull
    for x in range(3, 47):
        for y in (25, 26, 27):
            B.px(x, y, "wa1" if y < 27 else "b1")
        if x % 4 == 0:
            B.px(x, 24, "b3")
    # deck seen from above
    for y in range(9, 19):
        t = (y - 9) / 9
        x0 = 4
        x1 = 44 - int(round(6 * abs(t - 0.5) * 2))
        for x in range(x0, x1 + 1):
            M.px(x, y, "wd3" if (y % 3 == 0) else "wd2")
    # gunwale rim, blue, lit on top
    for x in range(3, 46):
        M.px(x, 8, "ink")
        M.px(x, 9, "b2" if x < 40 else "b1")
    M.vline(3, 8, 19, "ink")
    M.vline(4, 9, 18, "b1")
    # thwarts and a coil of rope
    for tx in (16, 28):
        M.rect(tx, 10, 2, 8, "wd1")
    M.blit([" rr ", "r11r", " rr "], {"r": "rp", "1": "wd2"}, 33, 12)
    # stern awning
    M.rect(5, 6, 9, 3, "w0")
    M.hline(5, 13, 6, "ink")
    M.hline(5, 13, 8, "b1")
    M.vline(5, 6, 15, "wd1")
    M.vline(13, 6, 15, "wd1")
    # mast with a furled sail
    M.vline(23, 0, 15, "wd1")
    M.vline(24, 0, 15, "ink")
    M.rect(20, 3, 9, 3, "w0")
    M.hline(20, 28, 3, "ink")
    M.hline(20, 28, 5, "rp")
    M.px(19, 4, "ink")
    M.px(29, 4, "ink")
    # near side of the hull
    for x in range(3, 47):
        top = 19
        bow = max(0, x - 40)
        bot = 25 - (bow // 2)
        for y in range(top - bow, bot + 1):
            c = "w0"
            if y == top - bow:
                c = "b1"
            elif y >= bot - 1:
                c = "rd"
            M.px(x, y, c)
        M.px(x, bot + 1, "ink")
        M.px(x, top - bow - 1, "ink")
    M.vline(2, 18, 26, "ink")
    # stem post rising at the bow
    M.vline(46, 10, 21, "wd1")
    M.vline(47, 10, 21, "ink")
    M.px(46, 9, "ink")
    boat_eye(M, 36, 19)
    # a plank seam along the hull
    M.hline(4, 40, 22, "rp")
    return s


def rowboat():
    s = Struct("boat_small", "Small moored rowing boat", 2, 1, SEC,
               walk=["XX"],
               notes="A small blue-and-white boat with an eye on the bow, side-on, bow to "
                     "the right. Sea below, boat over it.")
    B, M = s.B, s.M
    sea(B, 0, 0, 32, 16)
    for x in range(2, 31):
        B.px(x, 13, "wa1")
        B.px(x, 14, "wa1")
        if x % 3 == 1:
            B.px(x, 12, "b3")
    # interior from above
    for y in range(3, 8):
        for x in range(4, 27 - abs(y - 5)):
            M.px(x, y, "wd2" if y % 2 else "wd3")
    M.rect(12, 3, 2, 5, "wd1")
    M.rect(20, 3, 2, 5, "wd1")
    for x in range(3, 30):
        M.px(x, 2, "ink")
        M.px(x, 3, "w0")
    # hull side
    for x in range(2, 31):
        bow = max(0, x - 25)
        top, bot = 8 - bow // 2, 12 - bow // 2
        for y in range(top, bot + 1):
            M.px(x, y, "b1" if y >= bot - 1 else ("w0" if y > top else "b2"))
        M.px(x, top - 1, "ink")
        M.px(x, bot + 1, "ink")
    M.vline(2, 2, 13, "ink")
    M.vline(30, 3, 10, "ink")
    boat_eye(M, 21, 7)
    return s


# ---- harbor goods on the quay ----

def nets():
    s = Struct("quay_nets", "Drying nets, net pile, amphorae and crates", 4, 2, SEC,
               walk=["XXX.", "XXXX"],
               notes="All on quay paving (two layers: quay below). Row 0: a net hung to dry "
                     "on a two-post rack (2 cells), a heap of net with cork floats, and plain "
                     "quay. Row 1: stacked amphorae (2 cells), a stack of fish crates, and a "
                     "lone amphora.")
    B, M = s.B, s.M
    quay(B, 0, 0, 64, 32)
    # rack posts and the hung net
    for px_ in (2, 27):
        M.rect(px_, 1, 3, 15, "wd2")
        M.vline(px_, 1, 15, "ink")
        M.vline(px_ + 2, 1, 15, "wd1")
        M.vline(px_ + 3, 1, 15, "ink")
        M.hline(px_, px_ + 3, 0, "ink")
    M.hline(5, 26, 2, "wd1")
    M.hline(5, 26, 1, "ink")
    for y in range(3, 14):
        for x in range(5, 27):
            sag = int(round(2 * math.sin(math.pi * (x - 5) / 21)))
            if y > 12 + sag:
                continue
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                M.px(x, y, "wd2" if (x + y) % 8 else "wd1")
        x = 5
    for fx in range(7, 26, 5):
        M.blit(["kk", "gk"], {"k": "ink", "g": "g1"}, fx, 2)
    # net heap with floats
    heap = [
        "    rrrr    ",
        "  rrwrrrwr  ",
        " rwrrrgrrwr ",
        "rrrgrrwrrrgr",
        "rwrrrrrrrrrr",
        "rrrrwrrgrrwr",
        " 11111111111",
    ]
    M.blit(heap, {"r": "wd2", "w": "wd3", "g": "g1", "1": "wd1"}, 34, 8)
    # amphorae leaning in a row
    amph = [
        " kk ",
        "k32k",
        " kk ",
        "k32k",
        "k332k",
        "k3321k",
        "k3321k",
        "k3321k",
        " k321k",
        " k321k",
        "  k21k",
        "  k21k",
        "   kk ",
    ]
    amph = [r.ljust(6) for r in amph]
    for i, ax in enumerate((0, 8, 16, 24)):
        M.blit(amph, {"k": "ink", "3": "tc2", "2": "tc1", "1": "tc0"}, ax, 18)
        # a black-figure band on each
        M.hline(ax + 1, ax + 4, 23, "ink")
    # crates
    crate = [
        "kkkkkkkkkk",
        "k3333333kk",
        "k2k2k2k2k",
        "k2k2k2k2k",
        "kkkkkkkkkk",
    ]
    for (cx_, cy_) in ((35, 19), (34, 24), (40, 25)):
        M.blit(crate, {"k": "ink", "3": "wd3", "2": "wd2"}, cx_, cy_)
    M.blit(["kkk", "kbk", "kbk"], {"k": "ink", "b": "b1"}, 44, 20)  # a fish in the top crate
    # a lone amphora
    M.blit(amph, {"k": "ink", "3": "tc2", "2": "tc1", "1": "tc0"}, 56, 18)
    M.hline(57, 60, 23, "ink")
    return s


# --------------------------------------------------------------------------
# Harbor shrine to Poseidon (group "cyc")
# --------------------------------------------------------------------------

def poseidon_shrine():
    s = Struct("shrine_poseidon", "Harbor shrine to Poseidon", 2, 3, SEC,
               walk=["XX", "XX", "XX"],
               notes="A small whitewashed naiskos on the quay: blue tympanum with a wave "
                     "scroll, two slim columns, a verdigris-bronze trident standing in a "
                     "blue niche, and conch offerings on the step. Talk-to scenery.")
    L = s.B
    W = 32
    # roof slopes above the pediment
    for y in range(0, 14):
        for x in range(W):
            L.px(x, y, "w1" if x < 16 else "w2")
    L.hline(0, W - 1, 0, "dk")
    L.vline(0, 0, 47, "dk")
    L.vline(W - 1, 0, 47, "dk")
    # pediment with a blue tympanum
    for x in range(W):
        t = int(round(13 - 9 * (1 - abs(x - 15.5) / 15.5)))
        L.px(x, t, "dk")
        L.px(x, t + 1, "w0")
        for y in range(t + 2, 14):
            L.px(x, y, "b1")
    wave = ["  ww ", " w  w", "w  w ", "w    "]
    L.pattern(wave, {"w": "w0"}, 6, 9, 20, 4, ox=6, oy=9)
    L.blit([" k ", "kwk", " k "], {"k": "dk", "w": "w0"}, 14, 1)  # finial
    L.hline(0, W - 1, 14, "w0")
    L.hline(0, W - 1, 15, "w2")
    L.hline(0, W - 1, 16, "w3")
    # niche with a trident
    L.rect(1, 17, 30, 23, "b0")
    L.rect(1, 17, 30, 2, "dk")
    for c in (4, 27):
        L.rect(c - 2, 17, 5, 23, "w1")
        L.vline(c - 2, 17, 39, "dk")
        L.vline(c + 2, 17, 39, "dk")
        L.vline(c - 1, 17, 39, "w0")
        L.vline(c + 1, 17, 39, "w2")
        L.hline(c - 3, c + 3, 17, "w0")
    trident = [
        "k  k  k",
        "L  L  L",
        "L  L  L",
        "L  L  L",
        "LkkLkkL",
        " LLLLL ",
        "   L   ",
    ]
    L.blit(trident, {"k": "ink", "L": "b3"}, 12, 19)
    L.vline(15, 26, 38, "b2")
    L.vline(16, 26, 38, "b0")
    L.hline(13, 18, 38, "ink")
    # podium and a step with conch shells
    L.hline(0, W - 1, 40, "w0")
    L.rect(1, 41, 30, 3, "w1")
    L.hline(1, 30, 43, "w2")
    L.hline(0, W - 1, 44, "w0")
    L.hline(1, 30, 45, "w2")
    L.hline(1, 30, 46, "w3")
    L.hline(0, W - 1, 47, "w4")
    conch = [" kk ", "kTtk", "kttk"]
    L.blit(conch, {"k": "ink", "T": "tc2", "t": "tc1"}, 5, 41)
    L.blit(conch, {"k": "ink", "T": "tc2", "t": "tc1"}, 23, 41)
    return s


def build():
    return [temple_hestia(), harbor_quay(), harbor_steps(), kaiki(), kaiki_mirrored(), nets(),
            poseidon_shrine()]


def kaiki_mirrored():
    """The kaiki turned bow-left. Porytiles reuses the flipped tiles, so this costs
    metatile ids but no new tiles."""
    k = kaiki()
    s = Struct("boat_kaiki_left", "Moored kaiki, bow to the left", 3, 2, SEC,
               walk=["XXX", "XXX"], notes="The same kaiki facing the other way, for the other "
                                           "side of a mooring.")
    for ln in ("bottom", "middle", "top"):
        s.layers[ln].a[:] = k.layers[ln].a[:, ::-1]
    return s
