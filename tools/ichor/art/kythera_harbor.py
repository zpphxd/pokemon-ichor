"""Skandeia's harbor: the curved stone quay, the empty slipways chalked with
sickles, a hauled-up boat, the half-built keel, fishing boats, the boat on log
rollers, the trireme Euploia, and the harbor's gear (oars, nets, rope,
amphorae).

The quay's top is aethos's limestone path, so the town's lanes run onto it
without a seam and props stand on it as on any path; only its edges, where the
quay wall drops into the sea, are drawn here, over the borrowed sea.
"""
from __future__ import annotations

import math

import numpy as np

import kythera_lib as K
from kythera_lib import ground, put, struct
from kythera_coast import wob

SEC = "harbor"
PATH = 0x1D9


def path_px(X, Y):
    rgb = tuple(int(v) for v in K.aethos(PATH)[Y % 16, X % 16])
    return K.A.RGB2NAME[rgb]


def ashlar_px(X, Y, top):
    """The quay wall's face: pale limestone courses below the coping."""
    x, y = X % 16, Y - top
    if y == 0:
        return "p3"
    if y == 1:
        return "p2"
    course = y // 3
    if y % 3 == 0:
        return "l1"
    if (x + 5 * course) % 8 == 0:
        return "l1"
    return "p1" if (x + y) % 5 else "ks1"


# --------------------------------------------------------------------------
# The quay
# --------------------------------------------------------------------------

def quay():
    """The quay's edges over borrowed sea. Directions name where the sea is."""
    names = {"S": (0, 0), "S_b": (1, 0), "N": (2, 0), "E": (3, 0), "W": (4, 0),
             "out_SE": (5, 0), "out_SW": (6, 0), "out_NE": (7, 0),
             "out_NW": (0, 1), "in_SE": (1, 1), "in_SW": (2, 1), "in_NE": (3, 1), "in_NW": (4, 1),
             "steps_E": (5, 1), "steps_S": (6, 1), "ring_S": (7, 1),
             "N_plank": (0, 2), "S_plank": (1, 2)}
    s = struct("quay", "The curved stone quay", 8, 3, SEC,
               walk=["XXXXXXXX", "XXXXX..X", "..XXXXXX"],
               names=names,
               notes="Skandeia's quay (and Paphia's jetty). Its top is aethos's limestone path "
                     "(0x1D9): pave the quay with it, and these edges finish it where its wall drops "
                     "into the sea (each borrows aethos's sea). Named by where the sea is: `S` (sea "
                     "south; `S_b` adds a drain, `ring_S` a bronze mooring ring), `N`, `E`, `W`; "
                     "`out_SE` is the quay's rounded south-east corner (the sea round it), `in_SE` "
                     "the inside of a bend (sea only to the south-east): the rounded corners make "
                     "the quay curve. `steps_E` and `steps_S` go down into the water for boats "
                     "(walkable). `N_plank` is the north edge with a ship's gangplank landing on "
                     "it (a ship moored to the north, as the Euploia's plank comes down to it), "
                     "`S_plank` the south edge with a plank going down to a boat (both walkable). "
                     "Edge cells are otherwise impassable: the quay's walkable top ends on the "
                     "path cell behind them.")
    ground(s, "sea")
    M = s.M

    def edge(cx, cy, sd, extra=None):
        """sd(x, y) > 0 on the quay top. The wall face runs 6 px below the
        coping into the sea."""
        ox, oy = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, oy + y
                d = sd(x, y)
                if d > 0.5:
                    M.px(X, Y, path_px(X, Y))
                elif d > -0.5:
                    M.px(X, Y, "p3")
                elif d > -1.5:
                    M.px(X, Y, "p2")
                elif d > -6.5:
                    k = int(-d)
                    c = "l1" if k in (3, 6) else ("p1" if (X + Y) % 6 else "ks1")
                    if (X + 4 * (k // 3)) % 9 == 0:
                        c = "l1"
                    M.px(X, Y, c)
                elif d > -7.5:
                    M.px(X, Y, "kr0")
                elif d > -8.5:
                    M.px(X, Y, "kq2" if (X + Y) % 2 else None)
        if extra:
            extra(ox, oy)

    # straight edges: the coping line at y=7 for S (face below), etc.
    S_ = lambda x, y: 6 - y
    N_ = lambda x, y: y - 11          # sea north: you see only the coping's back
    E_ = lambda x, y: 9 - x
    W_ = lambda x, y: x - 6

    def rnd_out(a, b, r=5.0):
        if a < r and b < r:
            return r - math.hypot(r - a, r - b)
        return min(a, b)

    def rnd_in(a, b, r=5.0):
        return -rnd_out(-a, -b, r)

    edge(0, 0, S_)
    edge(1, 0, S_, lambda ox, oy: put(M, ox + 6, oy + 9, ["kkk", "k0k"], {"k": "kr0", "0": "kr1"}))
    # north edge: sea to the north; the quay's back coping only, low wall face hidden
    for y in range(16):
        for x in range(16):
            X, Y = 32 + x, y
            if y >= 5:
                M.px(X, Y, path_px(X, Y))
            elif y == 4:
                M.px(X, Y, "p3")
            elif y == 3:
                M.px(X, Y, "l1")
            elif y == 2:
                M.px(X, Y, "kq2" if x % 2 else None)
    # east and west: the coping runs north-south, a sliver of wall shows
    edge(3, 0, E_)
    edge(4, 0, W_)
    edge(5, 0, lambda x, y: rnd_out(S_(x, y), E_(x, y)))
    edge(6, 0, lambda x, y: rnd_out(S_(x, y), W_(x, y)))
    edge(7, 0, lambda x, y: rnd_out(N_(x, y) + 5, E_(x, y)))
    edge(0, 1, lambda x, y: rnd_out(N_(x, y) + 5, W_(x, y)))
    edge(1, 1, lambda x, y: rnd_in(S_(x, y), E_(x, y)))
    edge(2, 1, lambda x, y: rnd_in(S_(x, y), W_(x, y)))
    edge(3, 1, lambda x, y: rnd_in(N_(x, y) + 5, E_(x, y)))
    edge(4, 1, lambda x, y: rnd_in(N_(x, y) + 5, W_(x, y)))
    # steps down into the water, east and south
    ox = 5 * 16
    for y in range(16):
        for x in range(16):
            X, Y = ox + x, 16 + y
            step = x // 4
            if step < 3:
                c = ("p3", "p2", "p1")[min(2, (x % 4))] if x % 4 < 3 else "l1"
                if step == 2 and x % 4 == 3:
                    c = "kr0"
                M.px(X, Y, c)
            elif x < 14:
                M.px(X, Y, "kq1" if (x + y) % 3 else "kq2")
            elif x == 14:
                M.px(X, Y, "kq2" if y % 2 else None)
    ox = 6 * 16
    for y in range(16):
        for x in range(16):
            X, Y = ox + x, 16 + y
            step = y // 4
            if step < 3:
                c = ("p3", "p2", "p1", "l1")[y % 4]
                M.px(X, Y, c)
            elif y < 14:
                M.px(X, Y, "kq1" if (x + y) % 3 else "kq2")
            elif y == 14:
                M.px(X, Y, "kq2" if x % 2 else None)
    for X in (ox, ox + 15):
        for y in range(16):
            M.px(X, 16 + y, "l1")
    edge(7, 1, S_, lambda ox, oy: put(M, ox + 6, oy + 8, [".kk.", "k..k", ".kk."], {"k": "kr0"}))
    # plank landings: the north edge with a plank coming down onto it, the
    # south edge with one going down from it
    for y in range(16):
        for x in range(16):
            X, Y = x, 32 + y
            if y >= 5:
                M.px(X, Y, path_px(X, Y))
            elif y == 4:
                M.px(X, Y, "p3")
            elif y == 3:
                M.px(X, Y, "l1")
            elif y == 2:
                M.px(X, Y, "kq2" if x % 2 else None)
    edge(1, 2, S_)
    for (ox, oy, y0, y1) in ((0, 32, 0, 9), (16, 32, 4, 16)):
        for y in range(y0, y1):
            for x in range(4, 12):
                if x in (4, 11):
                    c = "kr0"
                elif x == 5:
                    c = "p3"
                else:
                    c = "ks2" if (y - y0) % 3 else "l1"
                M.px(ox + x, oy + y, c)
    s.walk = ["XXXXXXXX", "XXXXX..X", "..XXXXXX"]
    s.ground = {k: v for k, v in s.ground.items() if k[1] < 2 or k[0] < 2}
    for k in [(x, 2) for x in range(2, 8)]:
        s.ground.pop(k, None)
    return s


# --------------------------------------------------------------------------
# Boats
# --------------------------------------------------------------------------

def kaiki_h(L, ox, oy, chalk=False, wet=True):
    """A small fishing boat, bow to the right, 3 cells x 2: white hull with a
    blue sheer stripe and a red boot-top, planked deck, a mast stepped and
    lowered, an eye on the bow."""
    put(L, ox, oy + 4, [
        "......................................kk......",
        "..kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkwwk.....",
        ".kddddddddddddddddddddddddddddddddddddddwk....",
        "kwd3dd3dd3dd3dd3dd3dd3dd3dd3dd3dd3dd3dddwk....",
        "kwddddddddddddddddddddddddddddddddddddddddkk..",
        "kbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbk.",
        "kwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwkwwwwk",
        ".kwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwkiwwwk.",
        "..kwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwk..",
        "...krrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrk...",
        "....kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk....",
    ], {"k": "ink", "d": "wd2", "3": "wd3", "w": "w0", "b": "b1", "r": "rs1", "i": "b2"})
    # the lowered mast and a furled sail along the deck
    L.line(ox + 6, oy + 6, ox + 34, oy + 5, "wd1")
    for x in range(ox + 10, ox + 28):
        L.px(x, oy + 4, "w0" if x % 3 else "kr2")
    # thwarts and a coil of net
    put(L, ox + 30, oy + 6, ["kk", "kk"], {"k": "wd1"})
    put(L, ox + 13, oy + 7, ["2222", "2..2", "2222"], {"2": "kr2"})
    if chalk:
        put(L, ox + 33, oy + 11, ["..w", ".w.", "ww."], {"w": "w0"})
    if wet:
        for x in range(ox + 3, ox + 44):
            if L.get(x, oy + 15) is None and x % 3:
                L.px(x, oy + 15, "w0" if x % 2 else "b2")


def kaiki_v(L, ox, oy, chalk=True, note=False):
    """The same boat hauled up a slip, bow up (north), 2 cells x 3."""
    rows = [
        "..........kk..........",
        ".........kwwk.........",
        "........kwddwk........",
        ".......kwdddddk.......",
        "......kbwdddddwk......",
        ".....kbwdd3dddwbk.....",
        "....kbwddddddddwbk....",
        "....kbwdd3dd3ddwbk....",
        "...kbwddddddddddwbk...",
        "...kbwddd3dd3dddwbk...",
        "...kbwddddddddddwbk...",
        "...kbwdd3dddd3ddwbk...",
        "...kbwddddddddddwbk...",
        "...kbwddd3dd3dddwbk...",
        "...kbwddddddddddwbk...",
        "...kbwdd3dddd3ddwbk...",
        "...kbwddddddddddwbk...",
        "...kbwddd3dd3dddwbk...",
        "...kbwddddddddddwbk...",
        "...kbwddddddddddwbk...",
        "....kbwddddddddwbk....",
        "....kbwdd3dd3ddwbk....",
        "....kbwddddddddwbk....",
        ".....kbwddddddwbk.....",
        ".....kbwwwwwwwwbk.....",
        "......kbbbbbbbbk......",
        "......krrrrrrrrk......",
        ".......kkkkkkkk.......",
    ]
    put(L, ox + 5, oy + 2, rows, {"k": "ink", "d": "wd2", "3": "wd3", "w": "w0", "b": "b1",
                                  "r": "rs1"})
    if chalk:
        # a sickle chalked on the bow planking
        put(L, ox + 13, oy + 6, [".w.", "..w", "..w", ".w.", "w.."], {"w": "w0"})
    if note:
        put(L, ox + 10, oy + 14, ["w.w.ww", "......", "ww.w.w"], {"w": "kr2"})


def kaiki():
    s = struct("kaiki", "A fishing boat, afloat and beached", 6, 2, SEC,
               walk=["XXXXXX", "XXXXXX"], names={"afloat": (0, 0), "beached": (3, 0)},
               notes="A kaiki, the island's fishing boat, bow to the east, 3 x 2 each: `afloat` on "
                     "borrowed sea, `beached` drawn up on the sand (borrowed sand). Impassable.")
    ground(s, "sea", [(x, y) for x in range(3) for y in range(2)])
    ground(s, "sand", [(x, y) for x in range(3, 6) for y in range(2)])
    M = s.M
    kaiki_h(M, 1, 8, wet=False)
    kaiki_h(M, 49, 8, wet=False)
    for x in range(52, 94):
        if M.get(x, 24) is None and (x % 2):
            M.px(x, 24, "wd0")
    return s


def rollers():
    s = struct("rollers", "The boat on log rollers", 3, 2, SEC, walk=["XXX", "XXX"],
               names={"boat": (0, 0)},
               notes="The boat KASSITEROS hauled up the Foam Road toward Paphia on log rollers "
                     "(borrowed path), a sickle chalked on her bow; after Knossa she is still there, "
                     "abandoned. 3 x 2, impassable; the bg event goes on her bow.")
    ground(s, "path")
    M = s.M
    for lx in (4, 18, 32):
        put(M, lx, 22, [".kkkk.", "k3223k", "k2222k", "k2112k", ".kkkk."], {"k": "wd0", "3": "wd3",
                                                                           "2": "wd2", "1": "wd1"})
    kaiki_h(M, 1, 8, chalk=True, wet=False)
    for x in range(4, 44):
        if M.get(x, 27) is None and x % 2:
            M.px(x, 27, "wd0")
    return s


def honey_boat():
    s = struct("honey_boat", "The honey boat", 2, 3, SEC, walk=["TT", "XX", "XX"],
               names={"sail": (0, 0), "hull": (0, 2)},
               notes="The small sailboat Alethea takes at Paphia's jetty (beat III-1F): a single "
                     "lateen sail over a short hull with jars of honey lashed aboard, on borrowed sea; "
                     "its sail's top row is drawn over the player. Use the hull rows alone (and swap "
                     "the top row to plain sea) once she has sailed, or make her an object.")
    ground(s, "sea")
    M, T = s.M, s.T
    # sail: a lateen triangle, cream with a stripe
    for y in range(4, 30):
        for x in range(3, 30):
            if x >= 6 + (y - 4) * 0.2 and x <= 6 + (y - 4) * 0.95 and y >= 4:
                c = "w0" if (x + y) % 7 else "wd3"
                if x > 6 + (y - 4) * 0.9:
                    c = "kr2"
                if 16 <= y <= 17:
                    c = "rs1"
                (T if y < 16 else M).px(x, y, c)
    # yard and mast
    for i in range(30):
        x, y = 5 + i * 0.85, 3 + i * 0.95
        (T if y < 16 else M).px(int(x), int(y), "wd1")
    for y in range(18, 36):
        M.px(16, y, "wd1")
    put(M, 2, 33, [
        "kkkkkkkkkkkkkkkkkkkkkkkkkkkk",
        "kdd3ddaaddaadd3ddddddddddwwk",
        "kwwwwwwwwwwwwwwwwwwwwwwwwwwk",
        ".kbbbbbbbbbbbbbbbbbbbbbbbbk.",
        "..kwwwwwwwwwwwwwwwwwwwwwwk..",
        "...krrrrrrrrrrrrrrrrrrrrk...",
        "....kkkkkkkkkkkkkkkkkkkk....",
    ], {"k": "ink", "d": "wd2", "3": "wd3", "w": "w0", "b": "b1", "r": "rs1", "a": "tc2"})
    for x in range(4, 30):
        if M.get(x, 40) is None and x % 3:
            M.px(x, 40, "w0")
    return s


# --------------------------------------------------------------------------
# Slipways, the hauled-up boat, the half-built keel
# --------------------------------------------------------------------------

def slips():
    s = struct("slips", "Slipways, a hauled-up boat, the half-built keel", 7, 3, SEC,
               walk=["XXXXXXX", "XXXXXXX", "WWWWXXX"],
               names={"slip": (0, 0), "slip_boat": (2, 0), "keel": (4, 0)},
               notes="The slipways at the quay's north end, every one empty, chalked with a sickle. "
                     "`slip` (2 wide x 3 tall at its top-left): a stone ramp with greased timber "
                     "runners down into the sea, its foot on borrowed sea. `slip_boat`: the one boat "
                     "the Titans left, hauled up the same slip, a sickle on her bow and, smaller, "
                     "somebody else's note; after the climax swap boats back onto the empty slips. "
                     "`keel` (3 x 3): Phereklos's half-built keel on trestles, ribs rising from it, "
                     "shavings round it (borrowed path). Impassable; the slips' feet are water.")
    ground(s, "sea", [(0, 2), (1, 2), (2, 2), (3, 2)])
    ground(s, "path", [(x, y) for x in range(4, 7) for y in range(3)])
    M, B = s.M, s.B

    def ramp(L, ox, oy, rows=48, water_from=32):
        """A slipway: a smooth stone ramp between low kerbs, two greased timber
        runners down its length, a sleeper across it every 8 px."""
        for y in range(rows):
            for x in range(32):
                X, Y = ox + x, oy + y
                wet = y >= water_from
                k = K.h(X, Y, 17)
                if x in (0, 31):
                    c = "ink"
                elif x == 1:
                    c = "w0"
                elif x == 30:
                    c = "kr1"
                elif x in (2, 29):
                    c = "kr1" if x == 29 else "kr2"
                elif x in (8, 9, 22, 23):        # timber runners, lit on the left
                    c = "wd3" if x in (8, 22) else "wd1"
                elif y % 8 == 0 and 3 <= x <= 28:
                    c = "wd1"                       # a sleeper
                elif y % 8 == 1 and 3 <= x <= 28:
                    c = "wd0"
                else:
                    c = "kr2" if k % 7 else "kr1"
                    if k % 23 == 0:
                        c = "w0"
                if wet:
                    if y > water_from + 6:
                        c = None
                    elif (y - water_from) > 2 and (x + y) % 2:
                        c = None
                    elif c is not None:
                        c = "b2" if c in ("kr1", "wd0", "wd1", "ink") else "b1"
                if c:
                    L.px(X, Y, c)
    # the two slips: rows 0-1 are the ramp on its own ground (bottom layer)
    for ox in (0, 32):
        ramp(B, ox, 0, rows=32, water_from=99)
        ramp(M, ox, 32, rows=16, water_from=0)
    # chalk sickles on the empty slip's stone
    put(B, 12, 10, [".ww.", "...w", "...w", "..w.", "ww.."], {"w": "w0"})
    put(B, 18, 20, ["ww..", "..w.", "...w", "..w.", ".w.."], {"w": "w0"})
    # the boat hauled up the second slip
    kaiki_v(B, 32, 0, chalk=True, note=True)
    # keel on trestles: a long keel north-south with ribs, trestles under it
    for y in range(4, 46):
        for x in range(64 + 21, 64 + 27):
            c = "wd2" if x < 64 + 23 else ("wd1" if x < 64 + 26 else "wd0")
            if x == 64 + 21:
                c = "wd3"
            M.px(x, y, c)
    for (ry, span) in ((9, 9), (15, 11), (21, 12), (27, 12), (33, 11), (39, 8)):
        for x in range(64 + 24 - span, 64 + 24 + span):
            dy = int(((x - (64 + 24)) / span) ** 2 * 3)
            M.px(x, ry - dy, "wd2")
            M.px(x, ry - dy + 1, "wd0")
        M.px(64 + 24 - span, ry - 3, "wd3")
        M.px(64 + 24 + span - 1, ry - 3, "wd1")
    for (tx, ty) in ((64 + 14, 12), (64 + 14, 34), (64 + 30, 12), (64 + 30, 34)):
        put(M, tx, ty, ["kkkkkk", ".k..k.", "k....k"], {"k": "wd1"})
    # shavings and an adze
    for (sx, sy) in ((64 + 6, 8), (64 + 40, 20), (64 + 9, 40), (64 + 38, 42), (64 + 4, 26)):
        put(M, sx, sy, [".3.", "3.3"], {"3": "wd3"})
    put(M, 64 + 36, 6, ["111.", "..1.", "..1.", "..k."], {"1": "kr1", "k": "wd1"})
    return s


# --------------------------------------------------------------------------
# The trireme Euploia (Akti's, recolored into Kythera's palettes)
# --------------------------------------------------------------------------

def trireme():
    import akti_art
    src = akti_art.trireme()
    s = struct("trireme", "The trireme Euploia", src.w, src.h, SEC, walk=list(src.walk),
               names={"gangplank": (3, 2)},
               notes="The Euploia moored bow to the east, as at Akti, on borrowed sea; place her with "
                     "her bottom row on the water just north of the quay, so her gangplank (bottom "
                     "row, column 3) lands on the quay's south edge below. Impassable. At Skandeia "
                     "she is requisitioned: Molybdos stands at the plank.")
    ground(s, "sea")
    terra = [K.C[n] for n in K.GROUPS["terra"]]
    a = src.layers["middle"].a
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if a[y, x, 3]:
                r, g, b = (int(v) for v in a[y, x, :3])
                best = min(terra, key=lambda c: (c[0] - r) ** 2 * 3 + (c[1] - g) ** 2 * 4 + (c[2] - b) ** 2 * 2)
                s.M.rgb(x, y, best)
    return s


# --------------------------------------------------------------------------
# The harbor's gear
# --------------------------------------------------------------------------

def gear():
    names = {"oars": (0, 0), "nets": (1, 0), "rope": (2, 0), "amphorae": (3, 0),
             "crate": (4, 0), "bollard": (5, 0), "gangplank": (6, 0)}
    s = struct("gear", "The harbor's gear", 7, 1, SEC, walk=["XX.XXX."], names=names,
               notes="On borrowed path (the quay's top). `oars`, a stack of oars the Titanborn carry to "
                     "the slips; `nets`, a heap of nets with floats (the old sailor mends them); "
                     "`rope`, a coil (walkable); `amphorae`, a rack of jars; `crate`, a fish crate; "
                     "`bollard`, a stone bollard. `gangplank` is a plank over borrowed sea (walkable) "
                     "from the quay's edge to a ship's side.")
    ground(s, "path", [(x, 0) for x in range(6)])
    ground(s, "sea", [(6, 0)])
    M = s.M
    # oars: long shafts with blades, stacked on two chocks
    for i, y in enumerate((3, 6, 9, 12)):
        for x in range(1, 15):
            M.px(x, y, "wd2" if x < 12 else "wd3")
            M.px(x, y + 1, "wd1" if x < 12 else "wd2")
        put(M, 11 + (i % 2), y - 1, ["33", "33", "22"], {"3": "wd3", "2": "wd1"})
    put(M, 3, 13, ["kk"], {"k": "wd0"})
    put(M, 9, 13, ["kk"], {"k": "wd0"})
    # nets: a heap of brown netting with cork floats
    for y in range(4, 15):
        for x in range(16 + 1, 16 + 15):
            if math.hypot((x - 24) / 7, (y - 10) / 5) < 1:
                M.px(x, y, "wd1" if (x + y) % 2 else ("wd2" if (x - y) % 3 else "wd0"))
    for (fx, fy) in ((19, 6), (26, 5), (22, 11), (28, 9)):
        put(M, fx, fy, ["33", "22"], {"3": "tc3", "2": "tc1"})
    # rope coil
    for r, c in ((5.5, "wd1"), (4.5, "wd3"), (3.5, "wd2"), (2.5, "wd3"), (1.5, "wd1")):
        for a_ in range(64):
            th = 2 * math.pi * a_ / 64
            M.px(32 + 8 + int(round(r * math.cos(th))), 8 + int(round(r * 0.8 * math.sin(th))), c)
    M.px(40, 8, "wd0")
    # amphorae in a rack
    for (ax, ay) in ((1, 3), (6, 2), (11, 3)):
        put(M, 48 + ax, ay, [
            ".k.",
            "k3k",
            "323",
            "322",
            "322",
            "322",
            ".21",
            "..1",
        ], {"k": "tc0", "3": "tc2", "2": "tc1", "1": "tc0"})
    for x in range(48, 64):
        M.px(x, 12, "wd1")
        M.px(x, 13, "wd0")
    # crate of fish
    put(M, 64 + 2, 4, [
        "kkkkkkkkkkkk",
        "k3333333333k",
        "k3wbwbwbwb3k",
        "k3bwbwbwbw3k",
        "k3333333333k",
        "k2222222222k",
        "k2222222222k",
        "kkkkkkkkkkkk",
    ], {"k": "wd0", "3": "wd3", "2": "wd2", "w": "w0", "b": "kr2"})
    # bollard
    put(M, 80 + 4, 3, [
        ".kkkkkk.",
        "k223222k",
        "k222221k",
        ".k2221k.",
        "..k22k..",
        "..k21k..",
        ".k22211k",
        "k2222111",
        "kkkkkkkk",
    ], {"k": "ink", "2": "kr2", "3": "w0", "1": "kr1"})
    # gangplank over the sea
    for y in range(16):
        for x in range(4, 12):
            c = "wd2" if x not in (4, 11) else "wd0"
            if y % 4 == 0 and x not in (4, 11):
                c = "wd3"
            M.px(96 + x, y, c)
    return s


def flags():
    """Dressed limestone flags for the quay's top, so the harbor reads as paved
    stone and not as more beach (a critique pass on Skandeia). Drawn in the
    path's own colors, so lanes and the quay edges' coping meet them softly."""
    names = {"A": (0, 0), "B": (1, 0), "C": (2, 0), "drain": (3, 0), "ring": (4, 0),
             "worn": (5, 0)}
    s = struct("flags", "Quay flagstones", 6, 1, SEC, walk=["......"], names=names,
               notes="The quay's paving: lay `A`, `B` and `C` in a staggered mix (no two of a kind "
                     "side by side reads best), with a `drain` grate, an iron mooring `ring` let "
                     "into a slab, and a `worn` cracked slab here and there. Walkable.")
    B = s.B
    # slab layouts, (x0, y0, w, h) in a 16x16 cell; joints are the gaps
    layouts = {
        "A": [(0, 0, 9, 7), (9, 0, 7, 7), (0, 7, 5, 9), (5, 7, 11, 9)],
        "B": [(0, 0, 6, 8), (6, 0, 10, 8), (0, 8, 11, 8), (11, 8, 5, 8)],
        "C": [(0, 0, 12, 6), (12, 0, 4, 6), (0, 6, 7, 10), (7, 6, 9, 10)],
    }
    for name, (cx, cy) in names.items():
        ox, oy = cx * 16, cy * 16
        lay = layouts.get(name, layouts["A" if name != "worn" else "B"])
        for i, (x0, y0, w, h_) in enumerate(lay):
            gray = K.h(cx * 5 + i, cy + i, 23) % 4 == 0
            for y in range(y0, y0 + h_):
                for x in range(x0, x0 + w):
                    X, Y = ox + x, oy + y
                    edge_l, edge_t = x == x0, y == y0
                    edge_r, edge_b = x == x0 + w - 1, y == y0 + h_ - 1
                    if edge_r or edge_b:
                        c = "l1" if not gray else "kr1"
                    elif edge_l or edge_t:
                        c = "p3" if not gray else "kr3"
                    else:
                        k = K.h(X, Y, 29 + i) % 9
                        c = ("kr2" if k < 2 else "kr3") if gray else ("p1" if k < 2 else "p2")
                    B.px(X, Y, c)
        if name == "drain":
            put(B, ox + 4, oy + 5, [
                "kkkkkkkk",
                "k0k0k0kk",
                "k0k0k0kk",
                "k0k0k0kk",
                "kkkkkkkk",
            ], {"k": "kr0", "0": "kr1"})
        elif name == "ring":
            for a_ in range(32):
                th = 2 * math.pi * a_ / 32
                B.px(ox + 8 + int(round(3 * math.cos(th))), oy + 10 + int(round(2.2 * math.sin(th))), "kr0")
            put(B, ox + 7, oy + 6, ["kk", "kk"], {"k": "kr0"})
        elif name == "worn":
            for (x, y) in ((3, 2), (4, 3), (4, 4), (5, 5), (6, 5), (7, 6), (11, 10), (12, 11), (12, 12)):
                B.px(ox + x, oy + y, "l1")
    return s


def build():
    return [quay(), slips(), kaiki(), rollers(), honey_boat(), trireme(), gear(), flags()]
