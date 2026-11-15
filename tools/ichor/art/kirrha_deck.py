"""Panopeus's ferry, for gTileset_GulfFerry: the deck of a small merchant boat
crossing the Gulf of Korinthos (Route 10, beat 37B).

Drawn in 3/4 view like the Euploia's deck: the far gunwale along the north,
the deck's planks, the near gunwale and the hull's side along the south, the
gulf's animated water all round (aethos's sea, borrowed). One mast amidships
with a patched square sail hanging from its yard over the far rail; a low
deckhouse at the stern where Panopeus keeps the steering oar; a pen of goats
amidships; amphorae, grain sacks and rope lashed at the bow. The bow points
west, toward Aigion. No hatch.
"""
from __future__ import annotations

import math
import random

import numpy as np

import kirrha_lib as KL
from kirrha_lib import Layer, struct

SEC = "deck"
# the deck's rows, top to bottom, inside a 7-row hull: far rail, deck x3, near rail,
# hull side, waterline
RAIL_N, DECK0, NEAR, SIDE, WATER = 0, 1, 4, 5, 6


def _rail_n(L, x0, w):
    """The far gunwale along the top of a deck cell: a cap rail, its inner face, a
    shadow on the planks."""
    for x in range(x0, x0 + w):
        L.px(x, 0, "ink")
        L.px(x, 1, "wd3")
        L.px(x, 2, "wd2")
        L.px(x, 3, "wd1")
        L.px(x, 4, "wd1" if x % 8 else "wd0")
        L.px(x, 5, "wd0")
    for x in range(x0, x0 + w, 8):
        L.vline(x + 3, 1, 4, "wd0")


def _near_rail(L, x0, y0, w):
    """The near gunwale: the deck's last planks, then the rail cap seen from above
    and its outer face, oar-tholes every 16 px."""
    for x in range(x0, x0 + w):
        L.px(x, y0 + 7, "wd0")
        L.px(x, y0 + 8, "ink")
        L.px(x, y0 + 9, "wd3")
        L.px(x, y0 + 10, "wd3")
        L.px(x, y0 + 11, "wd2")
        L.px(x, y0 + 12, "wd1")
        L.px(x, y0 + 13, "wd1")
        L.px(x, y0 + 14, "wd0")
        L.px(x, y0 + 15, "ink")
    for x in range(x0 + 5, x0 + w, 16):
        L.rect(x, y0 + 5, 2, 4, "wd1")
        L.px(x, y0 + 5, "wd3")


def _hull(L, x0, y0, w, h=16, bottom=False):
    """The hull's side: tarred strakes, a blue painted strake, a red boot-top at
    the waterline (bottom cell: the waterline and the wake below it)."""
    for x in range(x0, x0 + w):
        for j in range(h):
            y = y0 + j
            if not bottom:
                k = j // 4
                c = ("b1", "b2", "wd1", "wd0")[k] if j % 4 != 3 else "ink"
                if j % 4 == 0 and k >= 2:
                    c = "wd2"
            else:
                if j < 4:
                    c = "wd0" if j % 4 != 3 else "ink"
                elif j < 8:
                    c = "rd"
                elif j == 8:
                    c = "ink"
                else:
                    continue
            L.px(x, y, c)
    if bottom:
        for x in range(x0, x0 + w):
            L.px(x, y0 + 9, "b0")
            if (x - x0) % 4 == 1:
                L.px(x, y0 + 10, "b3")
                L.px(x + 1, y0 + 10, "w0")
            if (x - x0) % 7 == 3:
                L.px(x, y0 + 12, "b3")


def midships():
    """A 2-wide slice of the hull from far rail to waterline, to repeat along the
    boat. Rows: far rail, deck, deck, deck, near rail, hull side, waterline."""
    s = struct("midships", "The ferry's hull, a slice amidships", 2, 7,
               walk=["..", "..", "..", "..", "XX", "XX", "XX"],
               notes="Repeat along the boat. Row 0: the deck under the far gunwale (water "
                     "north of it: fish from here). Rows 1-3: planks (row 2's left cell has "
                     "a cleat). Row 4: the near gunwale (impassable: the rail). Row 5: the "
                     "hull's painted side. Row 6: the waterline, on aethos's sea.",
               section=SEC)
    KL.ground(s, "deck", [(x, y) for y in range(5) for x in range(2)])
    KL.ground(s, "none", [(0, 5), (1, 5)])
    KL.ground(s, "sea", [(0, 6), (1, 6)])
    B, M = s.B, s.M
    _rail_n(M, 0, 32)
    # a cleat and a coil on the planks of row 2
    M.blit(["kkkkkk", "k3333k", " kkkk "], {"k": "ink", "3": "wd3"}, 4, 38)
    _near_rail(M, 0, 64, 32)
    _hull(B, 0, 80, 32)
    _hull(M, 0, 96, 32, bottom=True)
    return s


def _hull_end(tipx=6, midy=56, reach=34, rx=40.0, cut=26):
    """A west-facing end of the hull (the bow; mirrored and rounder for the
    stern), 48 x 128, matching midships' rows shifted down one (row 0 is the
    water above, where the stem rises). Returns (layer, deck_left(y))."""
    W, H = 48, 128
    L = Layer(W, H)

    def xl(y):
        d = (y - midy) / rx
        return tipx + reach * (1 - math.sqrt(max(0.0, 1 - d * d)))

    # the deck, its planks running fore and aft
    for y in range(16, 88):
        x0 = int(round(xl(y)))
        for x in range(max(0, x0), W):
            Y = y % 16
            row = Y // 4
            c = "wd2"
            if Y % 4 == 3 or (x + row * 5) % 16 == 0:
                c = "wd1"
            elif Y % 4 == 0:
                c = "wd3"
            L.px(x, y, c)
    # the gunwale along the outline: a lit cap, its inner face, ink outside
    for y in range(16, 88):
        x0 = int(round(xl(y)))
        for k, c in ((0, "ink"), (1, "wd3"), (2, "wd3"), (3, "wd2"), (4, "wd1"), (5, "wd0")):
            if x0 + k < W:
                L.px(x0 + k, y, c)
    # the far rail along the top (y 16-21), joining the outline's cap
    x_join = int(round(xl(16)))
    for x in range(x_join, W):
        for j, c in ((0, "ink"), (1, "wd3"), (2, "wd2"), (3, "wd1"), (4, "wd1"), (5, "wd0")):
            L.px(x, 16 + j, c)
    # the near rail (y 80-95) from where it meets the outline
    xn = int(round(xl(84)))
    for x in range(xn, W):
        L.px(x, 87, "wd0")
        for j, c in ((8, "ink"), (9, "wd3"), (10, "wd3"), (11, "wd2"), (12, "wd1"), (13, "wd1"),
                     (14, "wd0"), (15, "ink")):
            L.px(x, 80 + j, c)
    # the hull's side (y 96-120), receding to the forefoot
    for y in range(96, 121):
        x0 = xn + int((y - 96) * 0.45)
        for x in range(x0, W):
            j = y - 96
            if j < 16:
                k = j // 4
                c = ("b1", "b2", "wd1", "wd0")[k] if j % 4 != 3 else "ink"
                if j % 4 == 0 and k >= 2:
                    c = "wd2"
            elif j < 20:
                c = "wd0"
            elif j < 24:
                c = "rd"
            else:
                c = "ink"
            L.px(x, y, c)
        L.px(x0, y, "ink")
    for x in range(xn + 11, W):
        L.px(x, 121, "b0")
        if x % 4 == 1:
            L.px(x, 122, "b3")
            L.px(x + 1, 122, "w0")
    # the cutwater: the hull's leading edge from the near rail down
    for y in range(80, 121):
        x0 = xn + int(max(0, y - 96) * 0.45)
        L.px(x0, y, "ink")
    return L, xl


def _split(s, L):
    for y in range(L.h):
        for x in range(L.w):
            c = L.get(x, y)
            if c:
                (s.T if y < 16 else s.M).px(x, y, c)


def bow():
    """The bow, pointing west: the hull narrowing to the stem, the stem post curling
    up over the water, a painted eye. 3 wide, 8 tall: row 0 is the water above."""
    s = struct("bow", "The ferry's bow, pointing west", 3, 8,
               walk=["XXX", "XX.", "X..", "X..", "X..", "XXX", "XXX", "XXX"],
               notes="Row 0 is the water above the bow, where the stem post's curl rises "
                     "(drawn over the player). Rows 1-7 match midships' rows 0-6. Its "
                     "rightmost column joins midships.", section=SEC)
    KL.ground(s, "sea")
    L, xl = _hull_end()
    KL.boat_eye(L, 26, 99)
    # the stem post: up from the tip of the deck, curling over into row 0
    pts = [(8, 60), (5, 46), (4, 32), (5, 20), (8, 11), (12, 6), (16, 5), (18, 8), (16, 11),
           (13, 10)]
    for (a, b) in zip(pts, pts[1:]):
        L.line(a[0], a[1], b[0], b[1], "wd2")
        L.line(a[0] + 1, a[1], b[0] + 1, b[1], "wd1")
        L.line(a[0] - 1, a[1], b[0] - 1, b[1], "ink")
    L.line(13, 12, 30, 22, "rp")
    _split(s, L)
    return s


def stern():
    """The stern, east: the hull rounding up, the steering oar on its post at the
    quarter, its blade in the water, a little ensign. 3x8 like the bow."""
    s = struct("stern", "The ferry's stern and steering oar", 3, 8,
               walk=["XXX", "..X", "..X", ".XX", "..X", "XXX", "XXX", "XXX"],
               notes="Row 0: water, the stern post's tip and the ensign over it. Rows 1-7 "
                     "match midships'. Its leftmost column joins midships. The steering "
                     "oar's post is at (1,3); Panopeus stands at (0,3).", section=SEC)
    KL.ground(s, "sea")
    L0, xl = _hull_end(tipx=10, reach=26, rx=44.0)
    # mirror it: the stern faces east
    L = Layer(48, 128)
    L.a[:] = L0.a[:, ::-1]
    # the stern post, rising and curving in at the top
    pts = [(38, 60), (42, 46), (43, 32), (42, 20), (39, 12), (35, 8), (32, 8)]
    for (a, b) in zip(pts, pts[1:]):
        L.line(a[0], a[1], b[0], b[1], "wd2")
        L.line(a[0] - 1, a[1], b[0] - 1, b[1], "wd1")
        L.line(a[0] + 1, a[1], b[0] + 1, b[1], "ink")
    # the ensign on a staff
    L.vline(28, 2, 20, "wd1")
    L.px(28, 1, "ink")
    L.blit(["rrrrr", "rwwrr", "rrrr "], {"r": "rd", "w": "w0"}, 29, 3)
    # the steering oar: its post on the deck at (1,3), the loom angling down past
    # the quarter into the water, the blade under the surface
    L.rect(22, 52, 5, 16, "wd1")
    L.vline(22, 52, 67, "ink")
    L.vline(26, 52, 67, "ink")
    L.hline(22, 26, 52, "wd3")
    L.line(14, 58, 42, 112, "wd2")
    L.line(15, 58, 43, 112, "wd1")
    L.line(14, 59, 42, 113, "ink")
    L.ellipse(37, 108, 47, 124, "wd1")
    L.ellipse(38, 109, 46, 122, "b2")
    L.px(42, 116, "b3")
    L.blit(["kkk", "333"], {"k": "ink", "3": "wd3"}, 12, 56)
    _split(s, L)
    return s


def deckhouse():
    """The deckhouse at the stern: a low plank cabin with a pan-tile roof, a door
    and a shuttered window, Panopeus's cloak on a peg. 3x2 on the deck."""
    s = struct("deckhouse", "The ferry's deckhouse", 3, 2, walk=["XXX", "XXX"],
               notes="On the deck's planks at the stern: row 0 the roof, row 1 the front with "
                     "a door and a window. Impassable (the cabin is the captain's).",
               section=SEC)
    KL.ground(s, "deck")
    M = s.M
    KL.roof(M, 0, 0, 48, 16, ridge=True, eaves=True)
    for y in range(16, 31):
        for x in range(1, 47):
            X = (x - 1) % 6
            M.px(x, y, "wd2" if X not in (0, 5) else ("wd3" if X == 0 else "wd1"))
    M.hline(0, 47, 16, "ink")
    M.vline(0, 16, 31, "ink")
    M.vline(47, 16, 31, "ink")
    M.hline(0, 47, 31, "ink")
    M.rect(20, 19, 9, 12, "ink")
    M.rect(21, 20, 7, 11, "wd1")
    M.vline(24, 20, 30, "wd0")
    M.rect(6, 20, 7, 5, "ink")
    M.rect(4, 20, 2, 5, "b1")
    M.rect(13, 20, 2, 5, "b1")
    M.rect(35, 19, 6, 8, "rd")
    M.vline(37, 18, 19, "ink")
    M.hline(35, 40, 26, "wd0")
    return s


def mast_and_sail():
    """The mast amidships and its patched square sail on the yard, hanging over the
    far rail and the water beyond it. 6 wide: rows 0-1 over the water, row 2 over
    the far-rail deck cells, row 3 the mast's foot on the deck."""
    s = struct("sail", "The mast and the patched square sail", 6, 4,
               walk=["XXXXXX", "XXXXXX", "......", "XX.XXX"],
               notes="Rows 0-1: the sail over open water (aethos's sea; impassable water). "
                     "Row 2: the far-rail deck cells, the sail's foot drawn over the player "
                     "(walkable). Row 3: deck, the mast's foot at (2,3) and the sheet "
                     "cleats either side (impassable); the outer cells plain deck.",
               section=SEC)
    KL.ground(s, "sea", [(x, y) for y in (0, 1) for x in range(6)])
    KL.ground(s, "deck", [(x, y) for y in (2, 3) for x in range(6)])
    s.walk = ["XXXXXX", "XXXXXX", "......", ".XX.X."]
    s.behaviors = {}
    T, M = s.T, s.M
    W = 96
    _rail_n(M, 0, 96)
    for x in range(0, 96):
        M.px(x, 32, None)  # (rail drawn at y 32: re-draw below at the right rows)
    M.a[:] = 0
    rail = Layer(96, 16)
    _rail_n(rail, 0, 96)
    M.copy_from(rail, dy=32)
    sail = Layer(W, 64)
    mx = 40
    sx0, sx1, sy0, sy1 = 8, 79, 6, 44
    # the yard and its lifts
    sail.hline(sx0 - 5, sx1 + 5, sy0 - 2, "ink")
    sail.hline(sx0 - 5, sx1 + 5, sy0 - 1, "wd3")
    sail.hline(sx0 - 5, sx1 + 5, sy0, "wd2")
    sail.hline(sx0 - 5, sx1 + 5, sy0 + 1, "ink")
    sail.line(mx, 0, sx0 - 4, sy0 - 2, "rp")
    sail.line(mx + 1, 0, sx1 + 4, sy0 - 2, "rp")
    for y in range(sy0 + 2, sy1):
        bell = int(round(3 * math.sin(math.pi * (y - sy0) / (sy1 - sy0))))
        for x in range(sx0 - bell, sx1 + 1 + bell):
            # the wind fills it: lit at the upper left, linen-shaded toward the right
            # and the foot, darker along the panels' seams
            t = (x - sx0) / (sx1 - sx0) + 0.6 * (y - sy0) / (sy1 - sy0)
            c = "w0" if t < 0.75 else ("sa0" if t < 1.25 else "rp")
            if (x - sx0) % 12 == 0:
                c = "sa0" if c == "w0" else "rp"
            elif (x - sx0) % 12 == 1 and c == "w0":
                c = "w0"
            sail.px(x, y, c)
        sail.px(sx0 - bell - 1, y, "ink")
        sail.px(sx1 + bell + 1, y, "ink")
    sail.hline(sx0, sx1, sy1, "ink")
    sail.hline(sx0, sx1, sy1 - 1, "rp")
    # patches: ochre, faded red, a blue square, and their stitches
    for (px_, py_, pw, ph, col) in ((14, 12, 12, 10, "oc1"), (52, 24, 14, 9, "rd"),
                                    (30, 30, 9, 7, "b2"), (62, 9, 8, 7, "oc1")):
        sail.rect(px_, py_, pw, ph, col)
        for x in range(px_, px_ + pw, 2):
            sail.px(x, py_, "wd1")
            sail.px(x, py_ + ph - 1, "wd1")
        for y in range(py_, py_ + ph, 2):
            sail.px(px_, y, "wd1")
            sail.px(px_ + pw - 1, y, "wd1")
    # the mast in front of the sail
    sail.vline(mx, 0, 63, "wd1")
    sail.vline(mx + 1, 0, 63, "wd2")
    sail.vline(mx + 2, 0, 63, "ink")
    sail.vline(mx - 1, 0, 63, "ink")
    sail.blit(["kk", "rr", "rr"], {"k": "ink", "r": "rd"}, mx, 0)
    # sheets from the sail's corners down to the cleats on the deck
    sail.line(sx0, sy1, 20, 62, "rp")
    sail.line(sx1, sy1, 68, 62, "rp")
    for y in range(48):
        for x in range(W):
            c = sail.get(x, y)
            if c:
                T.px(x, y, c)
    # row 3: the mast's foot, a ring of rope round it; cleats with the sheets
    for y in range(48, 64):
        for x in range(W):
            c = sail.get(x, y)
            if c:
                M.px(x, y, c)
    M.ellipse(mx - 6, 54, mx + 8, 63, "rp")
    M.ellipse(mx - 3, 56, mx + 5, 61, "wd1")
    M.rect(mx - 1, 48, 4, 12, "wd1")
    M.vline(mx - 1, 48, 59, "ink")
    M.vline(mx + 2, 48, 59, "ink")
    for cx in (18, 66):
        M.blit(["kkkkkk", "k3333k", " kkkk "], {"k": "ink", "3": "wd3"}, cx, 58)
    return s


def goat_pen():
    """A pen of wicker hurdles on the deck amidships, straw inside. 3x2."""
    s = struct("goat_pen", "The goats' pen", 3, 2, walk=["XXX", "XXX"],
               notes="Hurdles of woven withies round a floor of straw, on the deck. The two "
                     "goats (Kerazap) are objects standing in it; the hidden Heart Scale is "
                     "under the straw at (2,1) ('A goat was sitting on it.').", section=SEC)
    KL.ground(s, "deck")
    M = s.M
    # straw, on an 8 px pattern so the floor costs few tiles
    straw = ["31331313", "13113331", "33131133", "11331313", "31133131", "13311313",
             "31313311", "13131133"]
    for y in range(4, 30):
        for x in range(3, 45):
            ch = straw[y % 8][x % 8]
            M.px(x, y, "oc1" if ch == "3" else "wd3")
            if (x * 3 + y * 5) % 17 == 0:
                M.px(x, y, "wd2")

    def hurdle_h(y):
        for x in range(1, 47):
            M.px(x, y, "wd1" if (x // 2) % 2 else "wd2")
            M.px(x, y + 1, "wd2" if (x // 2) % 2 else "wd1")
            M.px(x, y + 2, "wd0")
        for x in range(1, 47, 7):
            M.vline(x, y - 2, y + 3, "wd0")
            M.px(x, y - 2, "wd3")

    def hurdle_v(x):
        for y in range(2, 31):
            M.px(x, y, "wd1" if (y // 2) % 2 else "wd2")
            M.px(x + 1, y, "wd0")
    hurdle_h(2)
    hurdle_v(1)
    hurdle_v(45)
    hurdle_h(27)
    # a water trough and a heap of droppings, honestly
    M.rect(30, 8, 10, 4, "wd1")
    M.hline(31, 38, 9, "b1")
    M.hline(31, 38, 10, "b2")
    for (x, y) in ((10, 20), (11, 21), (12, 20)):
        M.px(x, y, "wd0")
    return s


def bow_cargo():
    """At the bow: amphorae lashed in a rack, a stack of grain sacks, a coil of rope
    (2x2), on the deck."""
    s = struct("bow_cargo", "Cargo lashed at the bow", 2, 2, walk=["XX", "XX"],
               notes="Row 0: amphorae standing in a rack, roped. Row 1: grain sacks (Lamprias "
                     "sits on the next one) and a coil of rope. On the deck; impassable.",
               section=SEC)
    KL.ground(s, "deck")
    M = s.M
    M.hline(1, 30, 5, "wd1")
    M.hline(1, 30, 13, "wd1")
    for ax in (2, 9, 16, 23):
        M.blit(["  kk  ", " krrk ", "krrrrk", "krrr1k", "krrr1k", "krr11k", " krrk ", "  kk  ",
                "   k  "], {"k": "ink", "r": "oc1", "1": "wd1"}, ax, 3)
        M.blit([" kk ", "k33k"], {"k": "ink", "3": "wd3"}, ax + 1, 1)
    M.hline(1, 30, 8, "rp")
    for (bx, by) in ((2, 18), (12, 17), (6, 24)):
        M.ellipse(bx, by, bx + 10, by + 7, "sa0")
        M.hline(bx + 2, bx + 8, by + 2, "w0")
        M.outline("ink", region=(bx - 1, by - 1, 13, 10))
        M.px(bx + 5, by, "rp")
    M.ellipse(19, 20, 30, 30, "rp")
    M.ellipse(22, 22, 27, 28, "wd2")
    M.ellipse(24, 24, 25, 26, "rp")
    M.outline("ink", region=(17, 18, 15, 14))
    return s


def grain_sack():
    s = struct("grain_sack", "A grain sack to sit on", 1, 1, walk=["X"],
               notes="Lamprias's seat at the bow: a fat sack of Arkadian-bound grain on the "
                     "deck.", section=SEC)
    KL.ground(s, "deck")
    M = s.M
    M.ellipse(2, 5, 13, 14, "sa0")
    M.hline(4, 11, 7, "w0")
    M.outline("ink", region=(0, 0, 16, 16))
    M.blit(["kk", "rr"], {"k": "ink", "r": "rp"}, 7, 3)
    return s


def build():
    return [midships(), bow(), stern(), deckhouse(), mast_and_sail(), goat_pen(), bow_cargo(),
            grain_sack()]
