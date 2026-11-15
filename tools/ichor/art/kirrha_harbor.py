"""The harbors' waterfront, for gTileset_Kirrha: the grey quay and its steps,
moored boats (Panopeus's ferry with its patched sail among them), nets, crates,
amphorae, the pilgrims' bundles, the fish market under the old fig, the Agora
stall in its fishing shed, and the Kronist's crate of bread.
"""
from __future__ import annotations

import math
import random

import kirrha_lib as KL
from kirrha_lib import Layer, struct

SEC = "harbor"


# --------------------------------------------------------------------------
# The quay
# --------------------------------------------------------------------------

def quay():
    s = struct("quay", "The quay: grey ashlar paving, edges and corners", 5, 3,
               walk=[".....", ".....", "....."],
               notes="Big grey limestone blocks in running bond. The water beyond is aethos's "
                     "sea, placed next to these. Row 0: NW outer corner, north edge (water "
                     "north: coping only), NE outer corner, inner corners NW and NE (water "
                     "diagonally beyond). Row 1: west edge, plain quay, east edge, inner "
                     "corners SW and SE. Row 2: SW outer corner, south edge (water south: the "
                     "wet face shows), SE outer corner, then two plain alternates. All "
                     "walkable; the water beside is the sea's.", section=SEC)
    L = s.B
    KL.quay_paving(L, 0, 0, 80, 48)
    KL.coping_n(L, 0, 0, 48)
    L.vline(0, 0, 15, "pg1"); L.vline(1, 1, 15, "pg5"); L.vline(2, 2, 15, "pg4")
    L.vline(3, 2, 15, "pg4"); L.vline(4, 4, 15, "pg2")
    L.vline(47, 0, 15, "pg1"); L.vline(46, 1, 15, "pg4"); L.vline(45, 2, 15, "pg4")
    L.vline(44, 2, 15, "pg3"); L.vline(43, 4, 15, "pg2")
    L.blit(["1555", "54  ", "5   ", "5   "], {"1": "pg1", "5": "pg5", "4": "pg4"}, 48, 0)
    L.blit(["5551", "  45", "   4", "   4"], {"1": "pg1", "5": "pg4", "4": "pg4"}, 76, 0)
    L.vline(0, 16, 31, "pg1"); L.vline(1, 16, 31, "pg5"); L.vline(2, 16, 31, "pg4")
    L.vline(3, 16, 31, "pg4"); L.vline(4, 16, 31, "pg2")
    L.vline(47, 16, 31, "pg1"); L.vline(46, 16, 31, "pg4"); L.vline(45, 16, 31, "pg4")
    L.vline(44, 16, 31, "pg3"); L.vline(43, 16, 31, "pg2")
    L.blit(["5   ", "5   ", "54  ", "1155"], {"1": "pg1", "5": "pg5", "4": "pg4"}, 48, 28)
    L.blit(["   4", "   4", "  44", "4411"], {"1": "pg1", "4": "pg4"}, 76, 28)
    for x0 in (0, 16, 32):
        L.hline(x0, x0 + 15, 38, "pg5")
        L.hline(x0, x0 + 15, 39, "pg4")
        KL.quay_face(L, x0, 40, 16, 8)
    L.vline(0, 32, 39, "pg1"); L.vline(1, 32, 38, "pg5"); L.vline(2, 32, 38, "pg4")
    L.vline(47, 32, 39, "pg1"); L.vline(46, 32, 38, "pg4"); L.vline(45, 32, 38, "pg3")
    L.vline(0, 40, 47, "pg0")
    L.vline(47, 40, 47, "pg0")
    # the two alternates: a worn slab and a slab with an iron mooring ring
    L.rect(52, 36, 8, 4, "pg2")
    L.hline(52, 59, 36, "pg1")
    L.blit([" 111 ", "1   1", "1   1", " 111 "], {"1": "pg0"}, 69, 37)
    L.px(71, 36, "pg1")
    return s


def quay_steps():
    s = struct("quay_steps", "Quay steps, the bollard, the drain and the notice board", 5, 1,
               walk=["....X"],
               notes="Left: steps down to the water north of the quay. Second: steps in the "
                     "south face. Third: a stone bollard with a rope, on the north edge. "
                     "Fourth: a drain grate in the paving (the fish market's drain, under "
                     "the fig: the hidden Pearl). Fifth: a notice board on a post (the ferry's "
                     "sign; impassable).", section=SEC)
    L = s.B
    KL.quay_paving(L, 0, 0, 80, 16)
    # the notice board (wood, middle layer): a post and a board with a painted boat
    N = s.M
    N.rect(71, 9, 2, 7, "wd1")
    N.vline(73, 9, 15, "wd0")
    N.rect(65, 1, 14, 9, "wd2")
    N.hline(65, 78, 1, "wd3")
    N.hline(65, 78, 9, "wd0")
    N.vline(65, 1, 9, "ink")
    N.vline(78, 1, 9, "ink")
    N.hline(65, 78, 0, "ink")
    N.hline(65, 78, 10, "ink")
    N.rect(67, 3, 10, 5, "sa0")
    N.blit(["  w   ", " ww   ", "bbbbbb", " bbbb "], {"w": "w0", "b": "b1"}, 68, 3)
    N.px(76, 4, "rd")
    treads = [("pg2", "pg1"), ("pg2", "pg1"), ("pg3", "pg2"), ("pg4", "pg2")]
    for k, (tr, ed) in enumerate(treads):
        y = k * 4
        L.rect(2, y, 12, 3, tr)
        L.hline(2, 13, y + 3, ed)
        L.hline(2, 13, y, "lv1" if k == 0 else tr)
    for x in (0, 14):
        L.rect(x, 0, 2, 16, "pg3")
    L.vline(0, 0, 15, "pg4"); L.vline(1, 0, 15, "pg4")
    L.vline(14, 0, 15, "pg2"); L.vline(15, 0, 15, "pg1")
    L.hline(0, 15, 0, "pg1")
    L.hline(16, 31, 6, "pg5")
    L.hline(16, 31, 7, "pg4")
    KL.quay_face(L, 16, 8, 16, 8)
    yy = 8
    for tr, ri in (("pg4", "pg2"), ("pg3", "pg1"), ("pg2", "pg0")):
        L.rect(19, yy, 10, 1, tr)
        L.rect(19, yy + 1, 10, 2, ri)
        yy += 3
    L.rect(19, yy, 10, 16 - yy, "lv1")
    L.vline(18, 6, 15, "pg1")
    L.vline(29, 6, 15, "pg0")
    # bollard
    KL.coping_n(L, 32, 0, 16)
    L.blit(["  kkkk  ", " k5544k ", "k554433k", "k443322k", "k333222k", "k1222211", "k332211k",
            "k322211k", " k2211k ", "  kkkk  "],
           {"k": "pg0", "5": "pg5", "4": "pg4", "3": "pg3", "2": "pg2", "1": "pg1"}, 36, 4)
    L.hline(37, 44, 14, "pg1")
    for (x, y) in ((44, 8), (45, 7), (46, 6), (46, 5), (47, 4), (47, 3)):
        L.px(x, y, "e1")
    # the drain: a slotted stone, dark and wet round it
    L.rect(51, 5, 10, 7, "pg1")
    for x in range(52, 60, 2):
        L.vline(x, 6, 10, "pg0")
    L.hline(50, 61, 4, "pg2")
    L.hline(50, 61, 12, "pg4")
    L.px(55, 13, "lv1")
    L.px(56, 13, "lv0")
    return s


# --------------------------------------------------------------------------
# Boats, on aethos's animated sea
# --------------------------------------------------------------------------

def _hull_side(M, x0, x1, top, bot, bow_left=True, paint="b1", band="rd", lift=5, wood=False):
    """A small hull seen from the side: a lit gunwale, a painted strake, the body
    (whitewashed, or tarred timber strakes when wood), the red boot-top at the
    waterline, the bow lifting at one end."""
    for x in range(x0, x1 + 1):
        t = (x - x0) / max(1, x1 - x0)
        b = (1 - t) if bow_left else t
        up = int(round(lift * max(0.0, b - 0.75) / 0.25)) if b > 0.75 else 0
        down = int(round(3 * max(0.0, b - 0.8) / 0.2)) if b > 0.8 else 0
        y0, y1 = top - up, bot - down
        for y in range(y0, y1 + 1):
            if y == y0:
                c = "wd3"
            elif y == y0 + 1:
                c = paint
            elif y == y0 + 2:
                c = "b2" if paint == "b1" else paint
            elif y >= y1 - 1:
                c = band
            elif wood:
                k = (y - y0 - 3) % 3
                c = ("wd2", "wd1", "wd0")[k]
                if (x + (y - y0) * 7) % 23 == 0:
                    c = "wd3"
            else:
                c = "w0" if (y - y0) % 3 else "sa0"
            M.px(x, y, c)
        M.px(x, y0 - 1, "ink")
        M.px(x, y1 + 1, "ink")
        M.px(x, y1 + 2, "b0")
        if x % 3 == 0:
            M.px(x, y1 + 3, "b3")


def kaiki():
    s = struct("kaiki", "Moored fishing kaiki", 3, 2, walk=["XXX", "XXX"],
               notes="A fishing kaiki moored side-on, bow to the left: white and blue hull, "
                     "red boot-top, an eye on the bow, a short mast with the sail furled, "
                     "nets heaped aft. On aethos's animated sea.", section=SEC)
    KL.ground(s, "sea")
    M = s.M
    # deck seen from above, nets heaped at the stern
    for y in range(10, 18):
        for x in range(8, 44):
            M.px(x, y, "wd2" if y % 3 else "wd3")
    M.hline(6, 44, 9, "ink")
    M.hline(6, 44, 10, "b2")
    M.vline(44, 9, 18, "ink")
    for (nx, ny) in ((32, 12), (35, 11), (38, 13), (34, 14), (40, 12)):
        M.blit([" rr ", "r1r1", " rr "], {"r": "rp", "1": "wd1"}, nx, ny)
    # mast and furled sail
    M.vline(22, 0, 16, "wd1")
    M.vline(23, 0, 16, "ink")
    M.rect(17, 3, 12, 3, "w0")
    M.hline(17, 28, 3, "ink")
    M.hline(17, 28, 5, "rp")
    M.px(16, 4, "ink"); M.px(29, 4, "ink")
    _hull_side(M, 2, 45, 18, 25, bow_left=True)
    KL.boat_eye(M, 6, 18)
    M.vline(1, 9, 22, "wd1")
    M.vline(0, 9, 22, "ink")
    return s


def rowboat():
    s = struct("rowboat", "Moored rowing boat", 2, 1, walk=["XX"],
               notes="A small boat moored side-on, bow to the right, oars shipped. On aethos's "
                     "animated sea.", section=SEC)
    KL.ground(s, "sea")
    M = s.M
    for y in range(2, 7):
        for x in range(4, 28 - abs(y - 4)):
            M.px(x, y, "wd2" if y % 2 else "wd3")
    M.rect(12, 2, 2, 5, "wd1")
    M.rect(20, 2, 2, 5, "wd1")
    M.line(6, 3, 26, 5, "wd3")
    M.hline(3, 29, 1, "ink")
    _hull_side(M, 2, 30, 7, 11, bow_left=False, paint="dg" if False else "b1", lift=3)
    return s


def ferry_moored():
    """Panopeus's ferry at its mooring, side-on, bow to the left: a broad little
    merchant boat, one mast with a patched square sail, the deckhouse at the stern,
    goats' heads over the pen amidships. 6x3, on aethos's sea."""
    s = struct("ferry", "Panopeus's ferry, moored", 6, 3,
               walk=["TTTTTT", "XXXXXX", "XXXXXX"],
               notes="The Gulf ferry alongside the quay, bow to the left: a square sail "
                     "patched in ochre and red on one mast, the low deckhouse and the steering "
                     "oar at the stern, a goat looking over the side. Row 0 is the sail's head "
                     "over the water, drawn over the player; rows 1-2 the boat. Moor it with "
                     "the quay along its north side (row 0 is open water, so it can stand in "
                     "the sea north of a quay too).", section=SEC)
    KL.ground(s, "sea")
    M, T = s.M, s.T
    W = 96
    # --- the hull, rows 1-2 (y 16-47) ---
    # deck seen from above
    for y in range(24, 31):
        for x in range(10, 88):
            M.px(x, y, "wd3" if (x // 4 + y) % 5 == 0 else "wd2")
    M.hline(8, 88, 23, "ink")
    M.hline(9, 87, 24, "wd3")
    # the goat pen amidships: a hurdle and two goats' heads
    for x in range(38, 58):
        M.px(x, 27, "wd1" if x % 2 else "wd0")
        M.px(x, 29, "wd1" if x % 2 else "wd0")
    for gx in (42, 51):
        M.blit([" kk  ", "kwwk ", "kwwwk", " kwk ", "  k  "], {"k": "ink", "w": "w0"}, gx, 22)
        M.px(gx, 21, "wd1")
        M.px(gx + 3, 21, "wd1")
    # amphorae lashed at the bow
    for ax in (14, 19, 24):
        M.blit([" kk ", "krrk", "krrk", " kk "], {"k": "ink", "r": "oc1"}, ax, 25)
    # the deckhouse at the stern
    M.rect(68, 17, 16, 8, "wd2")
    M.hline(66, 85, 16, "ink")
    M.hline(67, 84, 17, "wd3")
    M.hline(67, 84, 18, "oc1")
    for x in range(68, 84, 3):
        M.vline(x, 19, 24, "wd1")
    M.rect(73, 19, 5, 6, "wd0")
    M.vline(66, 16, 24, "ink")
    M.vline(85, 16, 24, "ink")
    # the steering oar over the stern quarter
    M.line(88, 17, 94, 40, "wd1")
    M.line(89, 17, 95, 40, "wd0")
    M.rect(92, 38, 4, 6, "wd2")
    # hull side
    _hull_side(M, 4, 92, 31, 41, bow_left=True, paint="b1", band="rd", lift=8, wood=True)
    # stem post at the bow, curling
    M.line(4, 33, 1, 20, "wd2")
    M.line(5, 33, 2, 20, "ink")
    M.blit(["kk ", "k2k", " kk"], {"k": "ink", "2": "wd3"}, 0, 17)
    KL.boat_eye(M, 8, 32)
    # --- mast and sail: the mast rises from amidships; the sail's head (row 0) is
    # on the top layer over the water, its body over the deck in row 1 ---
    mx = 46
    for y in range(2, 30):
        L = T if y < 16 else M
        L.px(mx, y, "wd1")
        L.px(mx + 1, y, "ink")
    sail = Layer(W, 32)
    sx0, sx1, sy0, sy1 = 28, 66, 4, 22
    # yard
    sail.hline(sx0 - 3, sx1 + 3, sy0 - 1, "ink")
    sail.hline(sx0 - 3, sx1 + 3, sy0, "wd2")
    sail.hline(sx0 - 3, sx1 + 3, sy0 + 1, "ink")
    for y in range(sy0 + 2, sy1):
        bell = int(2 * math.sin(math.pi * (y - sy0) / (sy1 - sy0)))
        for x in range(sx0 - bell, sx1 + 1 + bell):
            # filled by the wind: lit upper left, linen shade to the right and foot
            t = (x - sx0) / (sx1 - sx0) + 0.6 * (y - sy0) / (sy1 - sy0)
            c = "w0" if t < 0.7 else ("sa0" if t < 1.2 else "rp")
            if (x - sx0) % 9 == 0:
                c = "sa0" if c == "w0" else "rp"
            sail.px(x, y, c)
        sail.px(sx0 - bell - 1, y, "ink")
        sail.px(sx1 + bell + 1, y, "ink")
    sail.hline(sx0, sx1, sy1, "ink")
    # the patches: an ochre square, a faded red one, a sewn seam
    sail.rect(31, 8, 7, 6, "oc1")
    sail.hline(31, 37, 8, "wd3")
    sail.rect(52, 13, 8, 5, "rd")
    sail.hline(52, 59, 13, "w0")
    for x in range(40, 50, 2):
        sail.px(x, 17, "wd1")
    # sheets down to the deck
    sail.line(sx0, sy1, sx0 - 2, 31, "rp")
    sail.line(sx1, sy1, sx1 + 3, 31, "rp")
    for y in range(32):
        for x in range(W):
            c = sail.get(x, y)
            if c:
                (T if y < 16 else M).px(x, y, c)
    for y in range(2, 30):
        L = T if y < 16 else M
        if sail.get(mx, y) is None or y < sy0:
            L.px(mx, y, "wd1")
            L.px(mx + 1, y, "ink")
    T.px(mx, 1, "rd")
    T.px(mx + 1, 1, "rd")
    T.px(mx + 2, 2, "rd")
    return s


# --------------------------------------------------------------------------
# On the quay
# --------------------------------------------------------------------------

def quay_goods():
    s = struct("quay_goods", "Nets, crates, amphorae and bundles on the quay", 6, 2,
               walk=["XX.XXX", "XXXXXX"],
               notes="All on quay paving. Row 0: a net drying on a two-post rack (2 cells), "
                     "plain quay, a heap of net with cork floats, a stack of fish crates, a "
                     "coil of rope. Row 1: amphorae lashed in a stack (2 cells), an octopus "
                     "drying line (2 cells), and two pilgrims' bundles with name tags.",
               section=SEC)
    KL.ground(s, "quay")
    M = s.M
    # net rack
    for px_ in (2, 27):
        M.rect(px_, 1, 3, 14, "wd2")
        M.vline(px_, 1, 14, "ink")
        M.vline(px_ + 2, 1, 14, "wd0")
    M.hline(2, 29, 1, "ink")
    M.hline(2, 29, 2, "wd3")
    for y in range(3, 13):
        for x in range(5, 27):
            if (x + y) % 3 == 0 or (x - y) % 3 == 0:
                M.px(x, y, "rp")
    for x in range(6, 27, 4):
        M.px(x, 12, "oc1")
    for x in range(4, 30):
        M.px(x, 15, "wd0")
    # net heap with floats
    M.ellipse(50, 5, 62, 14, "rp")
    for y in range(6, 14):
        for x in range(51, 62):
            if (x + y) % 2 == 0 and M.get(x, y) == "rp":
                M.px(x, y, "wd2")
    for (fx, fy) in ((52, 7), (57, 6), (60, 10), (54, 11)):
        M.px(fx, fy, "oc1")
        M.px(fx + 1, fy, "wd1")
    M.outline("ink", region=(48, 0, 16, 16))
    # fish crates
    for i, cy in enumerate((9, 3)):
        M.rect(66, cy, 13, 6, "wd2")
        M.hline(66, 78, cy, "wd3")
        M.hline(66, 78, cy + 5, "wd0")
        M.vline(66, cy, cy + 5, "ink")
        M.vline(78, cy, cy + 5, "ink")
        M.hline(66, 78, cy - 1, "ink")
    M.hline(67, 77, 15, "ink")
    for x in range(68, 77, 3):
        M.px(x, 2, "w0")
        M.px(x + 1, 2, "b2")
    # rope coil
    M.ellipse(82, 4, 94, 13, "rp")
    M.ellipse(85, 6, 91, 11, "wd2")
    M.ellipse(87, 7, 89, 10, "rp")
    M.outline("ink", region=(80, 0, 16, 16))
    # amphorae lashed together: four in a row, a rope round them
    for i, ax in enumerate((1, 9, 17, 25)):
        M.blit(["  kk  ", " krrk ", "krrrrk", "krrrrk", "krr1rk", "krrr1k", " krrk ", "  kk  "],
               {"k": "ink", "r": "oc1", "1": "wd1"}, ax, 20)
        M.blit(["  kk  ", " kwwk ", "  kk  "], {"k": "ink", "w": "wd3"}, ax, 17)
    M.hline(2, 29, 24, "rp")
    M.hline(2, 29, 29, "wd0")
    # the octopus line: two posts and four octopuses drying in the sun
    for px_ in (34, 61):
        M.rect(px_, 17, 2, 14, "wd2")
        M.vline(px_ + 1, 17, 30, "wd0")
    M.hline(34, 62, 18, "rp")
    for ox_ in (37, 45, 53):
        M.blit([" kk ", "krrk", "krrk", "kr1k", "r1r1", "1 1 "], {"k": "ink", "r": "rd", "1": "wd1"},
               ox_, 19)
    # pilgrims' bundles
    for bx, col in ((66, "sa0"), (82, "oc1")):
        M.ellipse(bx + 1, 21, bx + 12, 30, col)
        M.hline(bx + 3, bx + 10, 25, "wd1")
        M.outline("ink", region=(bx - 2, 16, 16, 16))
        M.px(bx + 6, 20, "wd1")
        M.rect(bx + 9, 26, 3, 2, "w0")
    return s


def upturned_boat():
    s = struct("upturned", "Upturned boat on trestles", 2, 1, walk=["XX"],
               notes="A boat turned keel-up on two trestles on aethos grass, being tarred.",
               section=SEC)
    KL.ground(s, "grass")
    M = s.M
    for x in (6, 24):
        M.vline(x, 9, 14, "wd1")
        M.vline(x + 1, 9, 14, "wd2")
    for x in range(2, 30):
        bulge = int(round(2.5 * math.sin(math.pi * (x - 2) / 27)))
        top = 5 - bulge
        for y in range(top, 11):
            c = "ink" if y > 8 else ("wd1" if y == top else "wd0")
            if y in (9, 10) and x % 2:
                c = "rd"
            M.px(x, y, c)
        M.px(x, top - 1, "ink")
        M.px(x, 11, "ink")
    M.vline(1, 4, 11, "ink")
    M.vline(30, 4, 11, "ink")
    return s


def fish_market():
    """The fish market under the old fig at the quay's head: the fig's great crown
    shading a long stone table of fish, an octopus and a set of scales, baskets
    beneath. 3x3."""
    s = struct("fish_market", "The fish market under the old fig", 3, 3,
               walk=["TTT", "TTT", "XXX"],
               notes="Kirrha's fish market at the head of the quay: an old fig's crown over "
                     "a long stone table laid with fish, an octopus and a scale, baskets "
                     "beneath. Rows 0-1 are the fig's crown, drawn over the player (walk "
                     "under it, in its shade); row 2 the table, on quay paving. The fishwife "
                     "stands in front; put the drain (quay_steps) in front of the table.",
               section=SEC)
    import numpy as np
    KL.ground(s, "quay", [(x, 2) for x in range(3)])
    KL.ground(s, "none", [(x, y) for y in (0, 1) for x in range(3)])
    B, M, T = s.B, s.M, s.T
    # under the crown (rows 0-1): the quay's paving in the fig's shade, drawn in the
    # market group's greys (m4 and m3 are the quay's pg2 and pg3), so the fig's grey
    # trunk can stand on it in the same tiles
    KL.quay_paving(B, 0, 0, 48, 32)
    B.replace(0, 0, 48, 32, "pg4", "m3")
    B.replace(0, 0, 48, 32, "pg3", "m4")
    B.replace(0, 0, 48, 32, "pg2", "m4")
    # the table (market group: marble-grey slab, fish)
    M.rect(1, 36, 46, 5, "m2")
    M.hline(1, 46, 36, "m1")
    M.hline(1, 46, 40, "m4")
    M.vline(1, 36, 46, "m4")
    M.vline(46, 36, 46, "m4")
    for lx in (3, 22, 41):
        M.rect(lx, 41, 3, 6, "m3")
        M.vline(lx + 2, 41, 46, "m4")
    for fx in (3, 11, 19, 27):
        M.blit(["  kkkk  ", "kksSSssk", " kddddk "], {"k": "ink", "s": "sl3", "S": "w0",
                                                     "d": "sl2"}, fx, 33)
    M.blit([" kk ", "krrk", "rkkr", "r rr"], {"k": "ink", "r": "rd"}, 36, 32)
    # the scales, hanging from the fig's low bough
    M.vline(43, 27, 34, "br")
    M.hline(39, 47, 27, "br")
    M.blit(["kk", "gg"], {"k": "ink", "g": "g0"}, 38, 28)
    M.blit(["kk", "gg"], {"k": "ink", "g": "g0"}, 45, 28)
    for bx in (8, 32):
        M.blit(["kkkkkkkk", "k2121212", "k1212121"], {"k": "ink", "1": "br", "2": "tc1"}, bx, 43)
    # the fig's trunk: smooth and grey (marble greys), in the shaded cells' bottom
    # layer so the crown is their one other layer; behind the table below
    for y in range(12, 36):
        w = 3 if y < 24 else 4
        L = B if y < 32 else M
        for x in range(4, 4 + w + 1):
            L.px(x, y, "m2" if x < 6 else "m4")
        L.px(4 + w + 1, y, "ink")
        L.px(3, y, "ink")
    B.line(8, 14, 16, 8, "m4")
    B.line(8, 15, 16, 9, "ink")
    # the market's drain, under the fig in cell (1,1): a slotted stone, wet round it
    B.rect(19, 22, 10, 6, "m4")
    for x in range(20, 28, 2):
        B.vline(x, 23, 26, "ink")
    B.hline(18, 29, 21, "m3")
    B.hline(18, 29, 28, "m2")
    s.names = {"drain": (1, 1)}
    # the crown: broad, the big hand-shaped leaves lit at the top left
    crown = Layer(48, 32)
    rnd = random.Random(5)
    yy, xx = np.mgrid[0:32, 0:48]
    mask = np.zeros((32, 48), bool)
    for (bx, by, rx, ry) in ((24, 13, 23, 12), (10, 17, 10, 9), (38, 17, 10, 9),
                             (22, 5, 14, 6)):
        mask |= ((xx - bx) / rx) ** 2 + ((yy - by) / ry) ** 2 <= 1
    mask[28:, :] = False
    for y in range(32):
        for x in range(48):
            if mask[y, x]:
                t = (x - 24) * 0.35 + (y - 13) * 1.0
                c = "lf1"
                if t > 8:
                    c = "ov1"
                elif t > 3:
                    c = "ov2"
                elif t < -7:
                    c = "lf2"
                crown.px(x, y, c)
    for _ in range(46):
        x, y = rnd.randint(3, 44), rnd.randint(1, 26)
        if not mask[y, x]:
            continue
        lit = (x - 24) * 0.35 + (y - 13) < 2
        crown.blit(["1 1", "111", " 1 "] if lit else ["0 0", "000", " 0 "],
                   {"1": "lf2", "0": "ov1"}, x - 1, y - 1)
    for _ in range(9):
        x, y = rnd.randint(6, 42), rnd.randint(8, 25)
        if mask[y, x]:
            crown.px(x, y, "ov0")
            crown.px(x + 1, y, "tk0")
    edge = mask & ~(np.roll(mask, 1, 0) & np.roll(mask, -1, 0) & np.roll(mask, 1, 1) &
                    np.roll(mask, -1, 1))
    for y, x in zip(*np.nonzero(edge)):
        crown.px(x, y, "ov0")
    T.copy_from(crown)
    return s


def stall_shed():
    """The Agora stall: a fishing shed on the quay, plank walls, a reed-and-tile roof,
    a ship's lantern over the door, votive wreaths and clay feet on strings at the
    side. 3x3, door at the bottom middle."""
    s = struct("stall", "The Agora stall in a fishing shed", 3, 3,
               walk=["XXX", "XXX", "XDX"],
               notes="Kirrha's Agora stall (warp 1): a plank shed on the quay with a pitched "
                     "roof of old pan tiles, a ship's lantern over the door, votives hung "
                     "beside it. Door at (1,2), on quay paving.", section=SEC)
    KL.ground(s, "quay")
    M = s.M
    # roof, row 0 (clay group via the shared roof painter); walls below in wood,
    # so the two never share an 8x8 tile
    KL.roof(M, 0, 0, 48, 16, ridge=True, eaves=True)
    # plank walls (wood group), rows 1-2
    for y in range(17, 46):
        for x in range(1, 47):
            X = (x - 1) % 6
            c = "wd2" if X not in (0, 5) else ("wd3" if X == 0 else "wd1")
            if y > 42:
                c = "wd0"
            M.px(x, y, c)
    M.vline(0, 16, 46, "ink")
    M.vline(47, 16, 46, "ink")
    M.hline(1, 46, 16, "ink")
    M.hline(1, 46, 17, "wd0")
    # door
    M.rect(18, 26, 12, 20, "wd0")
    M.rect(19, 27, 10, 19, "kt" if False else "ink")
    M.rect(20, 28, 8, 18, "wd1")
    M.vline(24, 28, 45, "wd0")
    M.hline(18, 29, 26, "wd3")
    # ship's lantern over the door
    M.blit([" k ", "kgk", "kwk", "kgk", " k "], {"k": "ink", "g": "oc1", "w": "w0"}, 22, 19)
    M.px(23, 18, "ink")
    # votives: wreaths and clay feet on strings at the left, a sign board at the right
    for (vx, vy) in ((5, 22), (10, 24)):
        M.vline(vx + 2, 18, vy, "rp")
        M.ellipse(vx, vy, vx + 4, vy + 4, "lv1")
        M.px(vx + 2, vy + 2, "wd2")
    M.vline(14, 18, 30, "rp")
    M.blit(["kk", "oo", "ooo"], {"k": "ink", "o": "oc1"}, 13, 30)
    M.rect(34, 24, 10, 7, "sa0")
    M.hline(34, 43, 24, "ink"); M.hline(34, 43, 30, "ink")
    M.vline(34, 24, 30, "ink"); M.vline(43, 24, 30, "ink")
    M.blit(["b b", " b ", "b b"], {"b": "b1"}, 37, 26)
    M.px(41, 27, "rd")
    return s


def kronist_crate():
    s = struct("kronist_crate", "The Kronist's crate of bread", 1, 1, walk=["X"],
               notes="A crate at the quay's head turned into a table: a cloth, loaves and a "
                     "jug. On quay paving. The Kronist stands behind it.", section=SEC)
    KL.ground(s, "quay")
    M = s.M
    M.rect(1, 6, 14, 9, "br")
    M.hline(1, 14, 6, "tc2")
    M.vline(1, 6, 14, "ink"); M.vline(14, 6, 14, "ink"); M.hline(1, 14, 15, "ink")
    for x in range(2, 14, 4):
        M.vline(x, 8, 14, "tc0")
    M.rect(0, 4, 16, 3, "w0")
    M.hline(0, 15, 6, "m2")
    M.blit([" kkk ", "k222k", "k121k", " kkk "], {"k": "ink", "1": "g0", "2": "tc2"}, 1, 0)
    M.blit([" kkk ", "k222k", "k121k", " kkk "], {"k": "ink", "1": "g0", "2": "tc2"}, 6, 1)
    M.blit([" k ", "kmk", "kmk"], {"k": "ink", "m": "tc1"}, 12, 1)
    return s


def beached():
    """A small fishing boat hauled up on the beach, bow to the right, its oars
    across the thwarts, the keel's furrow in the sand behind it. 2x1 on sand."""
    s = struct("beached", "Boat hauled up on the beach", 2, 1, walk=["XX"],
               notes="A rowing boat drawn up on aethos sand, bow to the right, tilted on its "
                     "keel, oars shipped. Impassable.", section=SEC)
    KL.ground(s, "sand")
    M = s.M
    for y in range(3, 8):
        for x in range(4, 27 - abs(y - 5)):
            M.px(x, y, "wd2" if y % 2 else "wd3")
    M.rect(12, 3, 2, 5, "wd1")
    M.rect(20, 3, 2, 5, "wd1")
    M.line(5, 4, 28, 6, "wd3")
    M.line(5, 5, 28, 7, "wd1")
    M.hline(3, 29, 2, "ink")
    _hull_side(M, 2, 30, 8, 12, bow_left=False, paint="b1", lift=3)
    # the sand under it: its shadow and the keel's furrow (wood group has no sand:
    # leave the borrowed sand bare, and shade with timber's darkest brown)
    for x in range(4, 29, 2):
        M.px(x, 14, "wd0")
    return s


def net_poles():
    """A net hung to dry between two driftwood poles on the beach, cork floats along
    its head rope. 2x2 on sand."""
    s = struct("net_poles", "Nets drying on poles on the beach", 2, 2, walk=["XX", "XX"],
               notes="Two driftwood poles on aethos sand with a net hung between them, cork "
                     "floats along its head rope. Impassable.", section=SEC)
    KL.ground(s, "sand")
    M = s.M
    for x in (3, 27):
        M.vline(x, 2, 29, "wd1")
        M.vline(x + 1, 2, 29, "wd2")
        M.px(x, 1, "ink")
        M.px(x + 1, 1, "ink")
        M.hline(x - 1, x + 2, 30, "wd0")
    for x in range(5, 27):
        sag = 0 if 9 <= x <= 22 else 1
        M.px(x, 5 + sag, "rp")
        for y in range(6 + sag, 23):
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                M.px(x, y, "wd2" if (x + y) % 8 else "wd1")
        M.px(x, 23, "rp")
        if x % 4 == 1:
            M.blit(["kk", "ok"], {"k": "ink", "o": "oc1"}, x, 4 + sag)
    for x in range(6, 26, 2):
        M.px(x, 27, "wd0")
    return s


def build():
    return [quay(), quay_steps(), kaiki(), rowboat(), ferry_moored(), quay_goods(),
            upturned_boat(), fish_market(), stall_shed(), kronist_crate(), beached(), net_poles()]
