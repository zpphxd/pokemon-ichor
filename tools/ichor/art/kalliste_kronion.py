"""Kronion Hill structures: the cracked stylobate of an archaic shrine, standing
and broken Doric columns of weathered poros limestone, fallen drums, the broken
altar, and the Titanborn's fresh dig (pit, spoil heaps, a trowel).

All in the "stone" group: older and warmer than Hestia's marble. Drawn into
kalliste_lib Structs; see kalliste_build.py.
"""
from __future__ import annotations

from kalliste_lib import Struct
from kalliste_parts import doric_column

SEC = "kronion"
RAMP = ["s1", "s2", "s3", "s4", "s5"]   # weathered poros, dark -> lit


SLAB = [  # one big worn poros slab per metatile, rounded by wear at the corners
    "1444444444444441",
    "4555445555544432",
    "4544444444444332",
    "4444444434444332",
    "4444434444444332",
    "4444444444443332",
    "4444444444444332",
    "4434444444444332",
    "4444444444444332",
    "4444444443444332",
    "4444444444444332",
    "4444344444444322",
    "4333333333333222",
    "4333333333332222",
    "3222222222222221",
    "1111111111111110",
]


def slabs(L, x, y, w, h):
    """Worn stylobate slabs, one per metatile, phase-locked to the grid. Body s3,
    wear-lit rims s4/s5, shaded joints s2/s1."""
    key = {"5": "s5", "4": "s3", "3": "s2", "2": "s2", "1": "s1", "0": "s0"}
    for j in range(h):
        for i in range(w):
            X, Y = x + i, y + j
            ch = SLAB[Y % 16][X % 16]
            c = key[ch]
            if ch == "4" and (Y % 16 in (1, 2)) and 1 <= X % 16 <= 12:
                c = "s4"
            L.px(X, Y, c)


def crack(L, pts, c="sk", lit="s4"):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L.line(x0, y0, x1, y1, c)
    for (x, y) in pts[1:-1]:
        L.px(x + 1, y, lit)


def weeds(L, x, y):
    L.blit([" g G", "gGg ", " gG "], {"g": "ol1", "G": "ol2"}, x, y)


def stylobate():
    s = Struct("stylobate", "Kronion Hill: cracked stylobate", 4, 3, SEC,
               walk=["....", "....", "XXX."],
               notes="The shrine's platform of worn poros slabs. Layout: NW, N, NE, cracked "
                     "/ W, plain, E, weedy / SW, S, SE, slab missing (bare earth). The north "
                     "and side edges are flush with the hill; the south edge shows a "
                     "crumbling step face (impassable, or use the steps from the terrace "
                     "set). Ruins, drums and the dig all sit on these slabs.")
    L = s.B
    slabs(L, 0, 0, 64, 48)
    # edges: worn lit rims on N/W/E, a step face on S
    for x0 in (0, 16, 32):
        L.hline(x0, x0 + 15, 0, "s2")
        L.hline(x0, x0 + 15, 1, "s5")
    L.vline(0, 0, 47, "s2")
    L.vline(1, 1, 37, "s5")
    L.vline(47, 0, 47, "s1")
    L.vline(46, 1, 37, "s2")
    for x0 in (0, 16, 32):
        L.hline(x0, x0 + 15, 38, "s5")
        L.hline(x0, x0 + 15, 39, "s4")
        L.rect(x0, 40, 16, 7, "s2")
        L.hline(x0, x0 + 15, 46, "s1")
        L.hline(x0, x0 + 15, 47, "s0")
        for jx in range(x0 + 5, x0 + 16, 10):
            L.vline(jx, 40, 46, "s1")
    # (3,0) cracked
    crack(L, [(49, 2), (53, 6), (52, 10), (57, 13), (60, 15)])
    crack(L, [(53, 6), (56, 4), (59, 5)])
    # (3,1) weeds in the joints
    weeds(L, 50, 21)
    weeds(L, 58, 28)
    weeds(L, 55, 16)
    # (3,2) a slab gone: bare earth and a stone
    L.rect(49, 33, 14, 13, "e1")
    L.hline(49, 62, 33, "s0")
    L.vline(49, 33, 45, "s0")
    L.blit([" kk ", "k42k", " kk "], {"k": "s0", "4": "s4", "2": "s2"}, 53, 37)
    L.blit(["g G", " g "], {"g": "ol1", "G": "ol2"}, 58, 41)
    for (x, y) in ((51, 43), (60, 36), (56, 44)):
        L.px(x, y, "e2")
    return s


def column(L, x, y, h, broken_at=None):
    """A weathered poros column. broken_at: y where the shaft snaps off."""
    if broken_at is None:
        doric_column(L, x, y, 12, h, RAMP, "sk")
        # chips in the abacus and lichen
        L.px(x - 2, y, None)
        L.px(x + 13, y + 1, "s1")
        for (dx, dy) in ((3, 14), (8, 22), (4, 30)):
            L.px(x + dx, y + dy, "alg")
        L.line(x + 8, y + 9, x + 6, y + 15, "s1")
        return
    top = broken_at
    doric_column(L, x, top, 12, y + h - top, RAMP, "sk", capital=False)
    jag = [2, 0, 1, 3, 1, 0, 2, 4, 2, 1, 3, 2]
    for i, d in enumerate(jag):
        for k in range(d):
            L.px(x + i, top + k, None)
        L.px(x + i, top + d, "s4" if i < 8 else "s2")
        L.px(x + i, top + d + 1, "s3" if i < 8 else "s1")


def columns():
    s = Struct("ruin_columns", "Kronion Hill: standing and broken Doric columns", 4, 3, SEC,
               walk=["T...", "TT..", "XXXX"],
               notes="Weathered poros columns on stylobate slabs. Column 0: a standing "
                     "column (3 cells). Column 1: a column snapped at mid height (its top "
                     "cell is plain slab). Columns 2 and 3: a stump, and a stump of two "
                     "drums with rubble (bottom cells; the cells above are plain slab). "
                     "T cells draw over the player (walk behind); bottom cells are "
                     "impassable.")
    B, M, T = s.B, s.M, s.T
    slabs(B, 0, 0, 64, 48)
    # standing column: capital and upper shaft on the top layer, foot on middle
    col = type(T)(16, 48)
    column(col, 2, 0, 48)
    for ln, rows in ((T, range(0, 32)), (M, range(32, 48))):
        for yy in rows:
            for xx in range(16):
                c = col.get(xx, yy)
                if c:
                    ln.px(xx, yy, c)
    # broken at mid height
    col = type(T)(16, 48)
    column(col, 2, 0, 48, broken_at=21)
    for ln, rows in ((T, range(0, 32)), (M, range(32, 48))):
        for yy in rows:
            for xx in range(16):
                c = col.get(xx, yy)
                if c:
                    ln.px(16 + xx, yy, c)
    # a low stump
    col = type(T)(16, 48)
    column(col, 2, 0, 48, broken_at=36)
    for yy in range(32, 48):
        for xx in range(16):
            c = col.get(xx, yy)
            if c:
                M.px(32 + xx, yy, c)
    # two-drum stump with rubble at its foot
    col = type(T)(16, 48)
    column(col, 2, 0, 48, broken_at=33)
    for yy in range(32, 48):
        for xx in range(16):
            c = col.get(xx, yy)
            if c:
                M.px(48 + xx, yy, c)
    M.hline(50, 61, 41, "s1")
    M.blit([" kk  k", "k43kk3k", "k32k21k", " kk kk "], {"k": "sk", "4": "s4", "3": "s3", "2": "s2", "1": "s1"},
           50, 44)
    return s


def drums():
    s = Struct("ruin_drums", "Kronion Hill: fallen drums and a capital", 4, 1, SEC,
               walk=["XXXX"],
               notes="On stylobate slabs. A fallen run of two drums lying east-west (2 "
                     "cells), a single drum lying with its fluted end toward the viewer, and "
                     "a toppled capital.")
    B, M = s.B, s.M
    slabs(B, 0, 0, 64, 16)
    # fallen drums lying east-west: flutes run along the length
    for x in range(1, 31):
        for y in range(3, 14):
            c = ["sk", "s4", "s5", "s4", "s3", "s3", "s4", "s3", "s2", "s2", "s1", "sk"][y - 3 + 0] \
                if 3 <= y <= 14 else None
            if c:
                M.px(x, y, c)
    M.vline(15, 4, 12, "s1")         # the joint between the two drums
    M.vline(16, 4, 12, "s5")
    # the broken end, facing us on the right
    end = [
        " kkkk ",
        "k5544k",
        "k5k43k",
        "k4432k",
        "k43k2k",
        "k4322k",
        "k3221k",
        "k3211k",
        " kkkk ",
    ]
    M.blit(end, {"k": "sk", "5": "s5", "4": "s4", "3": "s3", "2": "s2", "1": "s1"}, 26, 4)
    # single drum, end-on: a fluted disc
    disc = [
        "   kkkkkk   ",
        "  k545454k  ",
        " k54444443k ",
        "k5444443332k",
        "k4443333322k",
        "k4433332221k",
        "k4433322221k",
        "k3332222211k",
        " k32222111k ",
        "  k1212121k ",
        "   kkkkkk   ",
    ]
    M.blit(disc, {"k": "sk", "5": "s5", "4": "s4", "3": "s3", "2": "s2", "1": "s1"}, 34, 3)
    M.hline(36, 45, 14, "s1")
    # toppled capital: abacus slab and echinus on its side
    cap = [
        "kkkkkkkkkkkk ",
        "k55555544442k",
        "k44444433331k",
        "kkkkkkkkkkkkk",
        " k443333222k ",
        "  k4332221k  ",
        "   kkkkkkk   ",
    ]
    M.blit(cap, {"k": "sk", "5": "s5", "4": "s4", "3": "s3", "2": "s2", "1": "s1"}, 50, 5)
    M.hline(51, 62, 12, "s1")
    return s


def dig_site():
    s = Struct("dig_site", "Kronion Hill: the Titanborn's dig", 4, 2, SEC,
               walk=["XXXX", "XXXX"],
               notes="A fresh pit hacked through the slabs (2 x 2), a spoil heap with a "
                     "trowel stuck in it, a plain spoil heap, and two pried-up slabs. The "
                     "pit's north wall shows the hill's strata. Cells 2-3 of each row are "
                     "loose pieces to scatter around the pit.")
    L = s.B
    slabs(L, 0, 0, 64, 32)
    # the pit: broken slab rim, strata in the far wall, dark floor
    L.rect(2, 3, 28, 27, "sk")
    for y, c in ((4, "s2"), (5, "e2"), (6, "e2"), (7, "e1"), (8, "e1"), (9, "s1"), (10, "e1"),
                 (11, "s0"), (12, "s1"), (13, "s0")):
        L.hline(3, 28, y, c)
    for (x, y) in ((6, 6), (15, 8), (22, 5), (11, 10), (25, 9)):
        L.blit(["44", "21"], {"4": "s4", "2": "s2", "1": "s1"}, x, y)  # stones in the section
    L.rect(3, 14, 26, 15, "s0")
    for (x, y) in ((6, 17), (13, 21), (20, 16), (24, 24), (9, 25), (17, 26)):
        L.px(x, y, "e1")
        L.px(x + 1, y, "s1")
    # shovel marks in the floor
    L.line(16, 18, 23, 25, "e1")
    L.line(15, 18, 22, 25, "e2")
    # ragged rim: slab edges lit on the far (south-facing) side
    for x in range(2, 30):
        L.px(x, 2, "s1" if x % 5 else "sk")
        L.px(x, 29, "s4")
        L.px(x, 30, "s2")
    L.vline(1, 2, 30, "s1")
    L.vline(30, 2, 30, "s2")
    for (x, y) in ((4, 2), (5, 2), (18, 2), (26, 29), (27, 29)):
        L.px(x, y, "sk")
    # spoil heap with a trowel
    heap = [
        "      ee        ",
        "    e2e2ee      ",
        "   e2e12e1e     ",
        "  e2e1e2e11e    ",
        " e2e1e1e1e1e1   ",
        "ee1e1s1e1e1s1e  ",
        "e1e1s1e1s1e1s11 ",
        "1s1s1s1s1s1s1s11",
    ]
    hk = {"e": "e2", "2": "s3", "1": "e1", "s": "s1"}
    L.blit(heap, hk, 32, 7)
    L.blit(heap, hk, 32, 23)
    trowel = [
        "  k  ",
        "  h  ",
        "  h  ",
        " kkk ",
        "kwwtk",
        "kwttk",
        " kwk ",
        "  k  ",
    ]
    L.blit(trowel, {"k": "sk", "h": "e1", "w": "wt1", "t": "wt0"}, 39, 1)
    # pried-up slabs leaning
    slab = [
        "kkkkkkkkkkk ",
        "k55444444kk ",
        "k44333333k1k",
        "kkkkkkkkkk1k",
        "  k22222221k",
        "  kkkkkkkkkk",
    ]
    L.blit(slab, {"k": "sk", "5": "s5", "4": "s4", "3": "s3", "2": "s2", "1": "s1"}, 50, 4)
    L.blit(slab, {"k": "sk", "5": "s5", "4": "s4", "3": "s3", "2": "s2", "1": "s1"}, 50, 20)
    L.blit(["g G", "Gg "], {"g": "ol1", "G": "ol2"}, 58, 27)
    return s


def broken_altar():
    s = Struct("altar_broken", "Kronion Hill: the broken altar", 2, 2, SEC,
               walk=["..", "XX"],
               notes="An archaic altar split by a crack, one corner fallen. Bottom row is "
                     "the altar; the top row is slab with its back edge.")
    L = s.B
    slabs(L, 0, 0, 32, 32)
    # top slab of the altar
    L.rect(3, 12, 26, 6, "s4")
    L.hline(3, 28, 11, "sk")
    L.hline(4, 27, 12, "s5")
    L.hline(3, 28, 17, "s2")
    # front face with a worn moulding
    L.rect(4, 18, 24, 11, "s3")
    L.hline(4, 27, 19, "s2")
    L.hline(4, 27, 20, "s4")
    L.hline(4, 27, 27, "s2")
    L.hline(3, 28, 29, "sk")
    L.vline(3, 11, 29, "sk")
    L.vline(28, 11, 29, "sk")
    L.vline(4, 13, 28, "s5")
    L.vline(27, 13, 28, "s1")
    # the crack and the fallen corner
    crack(L, [(17, 11), (16, 15), (18, 19), (16, 24), (17, 29)])
    L.rect(24, 11, 5, 5, None)
    slabs_patch = [(24, 11), (25, 11), (26, 11), (27, 11), (28, 11)]
    for (x, y) in slabs_patch:
        pass
    for y in range(11, 16):
        for x in range(24, 29):
            L.px(x, y, "s3" if (x + y) % 7 else "s2")
    L.hline(24, 28, 16, "sk")
    L.vline(24, 11, 16, "sk")
    L.blit([" kkk ", "k443k", "k321k", " kkk "], {"k": "sk", "4": "s4", "3": "s3", "2": "s2", "1": "s1"}, 26, 27)
    # a sickle freshly scratched into the face
    L.blit(["  kk", " k  ", "k   ", " k  ", "  kk"], {"k": "s1"}, 8, 21)
    L.hline(7, 9, 26, "s1")
    return s


def build():
    return [stylobate(), columns(), drums(), dig_site(), broken_altar()]
