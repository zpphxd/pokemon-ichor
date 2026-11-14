"""Akti's coast for gTileset_Akti: craggy limestone in the sea and on the shore.

Rocks are drawn as crags: a lit top surface (a polygon) above a shaded south
face, the face streaked with strata, wet and weedy where it meets the water,
and ringed with foam. Everything sits on aethos's animated sea or its sand.

Pieces: a sea stack, small rocks and a reef awash, the west headland (a 2-wide
rocky spur in four rows), rocks on the sand and on the grass, and beach things:
shells, driftwood, nets drying on poles and a kaiki hauled up on the sand.
"""
from __future__ import annotations

import math
import random

import numpy as np
from PIL import Image, ImageDraw

from akti_lib import Struct, ground
import kalliste_akti as KA
from kalliste_parts import voronoi_labels

SEC = "akti"


def _mask(w, h, pts):
    m = Image.new("1", (w, h), 0)
    ImageDraw.Draw(m).polygon(pts, fill=1)
    return np.array(m)


def crag(L, pts, face, seed=0, foam=True, wet=True, shrub=0):
    """Paint a limestone crag. `pts` outline its top surface; the south face
    hangs `face` px below it. Foam rings the foot when it stands in water."""
    rng = random.Random(seed)
    w, h = L.w, L.h
    top = _mask(w, h, pts)
    body = top.copy()
    for d in range(1, face + 1):
        body[d:] |= top[:-d]
    face_m = body & ~top
    ys, xs = np.nonzero(body)
    if not len(xs):
        return
    # foam first, on the water around the foot of the rock
    if foam:
        foot = np.zeros_like(body)
        foot[1:] |= body[:-1]
        foot[:, 1:] |= body[:, :-1]
        foot[:, :-1] |= body[:, 1:]
        ring = foot & ~body
        ring2 = np.zeros_like(ring)
        ring2[1:] |= ring[:-1]
        ring2[:, 1:] |= ring[:, :-1]
        ring2[:, :-1] |= ring[:, 1:]
        ring2 &= ~body & ~ring
        for y, x in zip(*np.nonzero(ring)):
            if y > ys.min() + 2:
                L.px(x, y, "w0" if rng.random() < 0.7 else "b3")
        for y, x in zip(*np.nonzero(ring2)):
            if y > ys.min() + 4 and rng.random() < 0.45:
                L.px(x, y, "b3")
    # top surface: broken into facets, each tilted toward or away from the sun,
    # joined by dark cracks. Facets lit on their upper-left edges.
    tys, txs = np.nonzero(top)
    n_seeds = max(3, int(top.sum() // 28))
    seeds = [(int(txs[i]), int(tys[i])) for i in rng.sample(range(len(txs)), min(n_seeds, len(txs)))]
    lab = voronoi_labels(w, h, seeds, wrap=False, stretch=(1.0, 1.3))
    tilt = [rng.choice(("s5", "s4", "s4", "s3", "s4", "s3")) for _ in seeds]
    lo = {"s5": "s4", "s4": "s3", "s3": "s2"}
    hi = {"s4": "s5", "s3": "s4", "s5": "s5"}
    for y, x in zip(tys, txs):
        k = lab[y, x]
        c = tilt[k]
        right = x + 1 < w and lab[y, x + 1] != k and top[y, x + 1]
        down = y + 1 < h and lab[y + 1, x] != k and top[y + 1, x]
        left = x > 0 and lab[y, x - 1] != k
        up = y > 0 and lab[y - 1, x] != k
        if right or down:
            c = "s1" if (right and down) or rng.random() < 0.6 else "s2"
        elif left or up:
            c = hi.get(c, c)
        elif (x + y * 3 + k) % 9 == 0:
            c = lo.get(c, c)
        # the crag's own upper-left rim catches the sun; its lower-right rim is dark
        if not top[y - 1, x] or not top[y, x - 1]:
            c = "s5"
        elif not top[min(h - 1, y + 1), x] or not top[y, min(w - 1, x + 1)]:
            c = "s2"
        L.px(x, y, c)
    # south face: shaded, streaked with strata, wet and weedy at the waterline
    for y, x in zip(*np.nonzero(face_m)):
        depth = 0
        while depth < face and y - depth - 1 >= 0 and face_m[y - depth - 1, x]:
            depth += 1
        below = y + 1 >= h or not body[y + 1, x]
        c = "s2" if (x * 3 + seed) % 7 else "s1"
        if depth == 0:
            c = "s3"                       # the lip under the top's edge
        if (x + depth) % 5 == 0:
            c = "s1"                       # a stratum
        if wet and below:
            c = "wt0"
        elif wet and (y + 2 < h and not body[min(h - 1, y + 2), x]):
            c = "alg" if (x + seed) % 3 else "wt1"
        if not body[y, max(0, x - 1)]:
            c = "s3" if c not in ("wt0", "alg", "wt1") else c
        L.px(x, y, c)
    # outline the silhouette
    pad = np.pad(body, 1)
    edge = body & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if L.get(x, y) not in ("s5",):
            L.px(x, y, "sk")
    # scrub on top: lentisk and thyme
    for _ in range(shrub):
        tys, txs = np.nonzero(top)
        i = rng.randrange(len(txs))
        x, y = int(txs[i]), int(tys[i])
        for (dx, dy, c) in ((0, 0, "ol1"), (1, 0, "ol1"), (-1, 1, "ol1"), (0, 1, "alg"), (1, 1, "alg"),
                            (2, 1, "ol1"), (0, -1, "ol1")):
            if top[min(h - 1, max(0, y + dy)), min(w - 1, max(0, x + dx))]:
                L.px(x + dx, y + dy, c)


# --------------------------------------------------------------------------
# In the sea
# --------------------------------------------------------------------------

def sea_stack():
    s = Struct("sea_stack", "Limestone sea stack", 2, 2, SEC, walk=["XX", "XX"],
               notes="A tall crag of pale limestone standing in the sea, with a smaller rock "
                     "at its foot, foam round both. On aethos's animated sea.")
    ground(s, "sea")
    crag(s.M, [(9, 3), (17, 1), (24, 4), (26, 10), (22, 14), (12, 15), (7, 11)], face=14, seed=3,
         shrub=2)
    crag(s.M, [(1, 19), (6, 17), (10, 19), (9, 22), (3, 23)], face=5, seed=7)
    return s


def sea_rocks():
    s = Struct("sea_rocks", "Rocks awash", 1, 1, SEC, walk=["X"],
               notes="A broken pair of crags with foam, to scatter around the stacks and "
                     "the headland in clusters.")
    ground(s, "sea")
    crag(s.M, [(2, 7), (6, 5), (9, 7), (7, 9), (3, 10)], face=3, seed=12)
    crag(s.M, [(10, 3), (13, 2), (15, 4), (13, 5)], face=2, seed=13)
    return s


def headland():
    """The west headland: a rocky spur two cells wide, built from four rows.

    Row 0: its tip, sea to the north. Row 1: rock on the left, its east edge on
    the sea at the right. Row 2: solid rock, to repeat. Row 3: the spur's south
    face, dropping onto grass."""
    s = Struct("headland", "West headland: a limestone spur", 2, 4, SEC,
               walk=["XX", "XX", "XX", "XX"],
               notes="A two-wide rocky spur, its west side on the map edge. Row 0: the tip, "
                     "sea north and east. Row 1: rock at left, its east edge on the sea at "
                     "right. Row 2: solid rock; repeat it for length. Row 3: the spur's south "
                     "face, dropping onto grass. Scrub grows on top.")
    ground(s, "sea", [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)])
    ground(s, "grass", [(0, 3), (1, 3)])
    M = s.M
    # the spur's outline: tip rounded at the top right, east edge ragged in row 1,
    # full width from row 2, its south face ending in row 3
    pts = [(0, 3), (6, 1), (14, 2), (21, 5), (25, 10), (24, 16), (27, 20), (25, 26), (28, 30),
           (31, 32), (31, 50), (28, 52), (20, 51), (12, 53), (4, 51), (0, 52)]
    crag(M, pts, face=6, seed=21, shrub=0, wet=True)
    # broken crags heaped on the spur, each with its own face and shadow
    crag(M, [(2, 6), (9, 3), (16, 6), (15, 12), (6, 13), (1, 11)], face=4, seed=22, foam=False,
         wet=False, shrub=2)
    crag(M, [(14, 14), (21, 12), (24, 18), (19, 22), (13, 20)], face=4, seed=23, foam=False,
         wet=False, shrub=1)
    crag(M, [(0, 24), (7, 21), (13, 25), (11, 31), (2, 32)], face=5, seed=24, foam=False,
         wet=False, shrub=2)
    crag(M, [(16, 30), (25, 28), (31, 33), (30, 39), (19, 40)], face=4, seed=25, foam=False,
         wet=False, shrub=1)
    # the lower part stands on grass: a dry face there, no foam, a shadow on the turf
    for y in range(48, 64):
        for x in range(32):
            if M.get(x, y) in ("w0", "b3"):
                M.px(x, y, None)
            if M.get(x, y) in ("wt0", "wt1", "alg"):
                M.px(x, y, "s1")
    for x in range(0, 32):
        bot = max((y for y in range(48, 64) if M.a[y, x, 3]), default=None)
        if bot is not None:
            for d in (1, 2):
                if bot + d < 64 and (x + d) % 2 == 0:
                    M.px(x, bot + d, "ol1")
    # inland, the spur runs off the map's west edge: no gaps there
    for y in range(4, 48):
        for x in range(0, 3):
            if M.get(x, y) is None:
                M.px(x, y, "s3")
    return s


# --------------------------------------------------------------------------
# On the shore
# --------------------------------------------------------------------------

def rocks_sand():
    s = Struct("rocks_sand", "Limestone rocks on the sand", 2, 1, SEC, walk=["XX"],
               notes="Two single-cell crags on aethos sand, with a shadow: a tall one and a "
                     "low pair. Use them where the beach meets the tide rocks.")
    ground(s, "sand")
    M = s.M
    for x in range(3, 14):
        M.px(x, 14, "s2")
        if x % 2:
            M.px(x + 1, 15, "s2")
    crag(M, [(3, 5), (8, 2), (12, 5), (13, 9), (8, 11), (3, 10)], face=3, seed=31, foam=False,
         wet=False)
    for x in range(18, 30):
        M.px(x, 14, "s2")
    crag(M, [(17, 9), (21, 7), (24, 9), (22, 12), (18, 12)], face=2, seed=32, foam=False, wet=False)
    crag(M, [(24, 10), (28, 8), (31, 11), (27, 13)], face=2, seed=33, foam=False, wet=False)
    return s


def rock_grass():
    s = Struct("rock_grass", "Limestone rock in the grass", 2, 1, SEC, walk=["XX"],
               notes="Two crags on aethos grass, each with its shadow and a tuft: for the "
                     "edges of the town and the olive groves.")
    ground(s, "grass")
    M = s.M
    for x in range(4, 14):
        M.px(x, 13, "ol1")
        if x % 2 == 0:
            M.px(x + 1, 14, "ol1")
    for x in range(19, 30):
        M.px(x, 13, "ol1")
        if x % 2:
            M.px(x, 14, "ol1")
    crag(M, [(3, 4), (8, 1), (12, 4), (13, 8), (9, 11), (3, 10)], face=3, seed=41, foam=False,
         wet=False, shrub=1)
    crag(M, [(18, 7), (24, 5), (29, 8), (27, 12), (19, 12)], face=2, seed=42, foam=False, wet=False)
    return s


def shells():
    s = Struct("beach_shells", "Shells and driftwood on the sand", 2, 1, SEC, walk=[".X"],
               notes="On aethos sand: shells, pebbles and a line of weed left by the tide "
                     "(walkable), and a sun-bleached driftwood branch (solid).")
    ground(s, "sand")
    M = s.M
    shell = [" ww ", "w53w", " 33 "]
    for (x, y) in ((3, 4), (10, 9), (5, 12)):
        M.blit(shell, {"w": "w0", "5": "s5", "3": "s3"}, x, y)
    for (x, y, c) in ((12, 3, "s2"), (13, 3, "s1"), (8, 6, "b3"), (2, 9, "s1"), (14, 13, "s2"),
                      (9, 14, "w0")):
        M.px(x, y, c)
    # weed left by the tide
    for x in range(0, 16):
        y = 1 + int(round(1.2 * math.sin(x * 0.8)))
        M.px(x, y, "alg")
        if x % 3 == 0:
            M.px(x, y + 1, "ol1")
    # driftwood
    for k in range(12):
        x, y = 18 + k, 10 - k // 4
        M.px(x, y, "s4")
        M.px(x, y + 1, "s3")
        M.px(x, y + 2, "s1")
    for (x, y) in ((20, 8), (21, 7), (22, 6), (26, 11), (27, 12)):
        M.px(x, y, "s3")
    M.px(17, 12, "sk")
    M.px(30, 8, "sk")
    for x in range(19, 30):
        M.px(x, 13, "s2")
    return s


def net_poles():
    """A fishing net hung to dry between two poles on the beach, cork floats along it."""
    s = Struct("net_poles", "Nets drying on poles", 2, 2, SEC, walk=["XX", "XX"],
               notes="Two driftwood poles on the sand with a net hung between them, cork "
                     "floats along its head rope. On aethos sand.")
    ground(s, "sand")
    M = s.M
    for x in (3, 27):
        M.vline(x, 2, 29, "wd1")
        M.vline(x + 1, 2, 29, "wd2")
        M.px(x, 1, "ink")
        M.px(x + 1, 1, "ink")
        M.hline(x - 1, x + 2, 30, "wd0")
    # the net: a diamond mesh repeating every 4 px, its head rope sagging only at
    # the ends, so the middle tiles repeat
    for x in range(5, 27):
        sag = 0 if 9 <= x <= 22 else (1 if 7 <= x <= 24 else 0)
        M.px(x, 5 + sag, "rp")
        for y in range(6 + sag, 23):
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                M.px(x, y, "wd2" if (x + y) % 8 else "wd1")
        M.px(x, 23, "rp")
        if x % 4 == 1:
            M.blit(["kk", "gk"], {"k": "ink", "g": "g1"}, x, 4 + sag)
    for x in range(6, 26):
        M.px(x, 27, "wd0" if x % 2 else None)
    return s


def boat_beached():
    """The kaiki hauled up on the sand, bow to the right."""
    k = KA.kaiki()
    s = Struct("boat_beached", "Kaiki hauled up on the beach", 3, 2, SEC,
               walk=["XXX", "XXX"],
               notes="The kaiki drawn up on aethos sand, its hull sunk a little into it.")
    ground(s, "sand")
    s.M.a[:] = k.M.a
    # trim the waterline and let the keel bed into the sand
    for x in range(48):
        for y in range(24, 32):
            if s.M.get(x, y) == "rd":
                s.M.px(x, y, "wd0")
        bot = max((y for y in range(32) if s.M.a[y, x, 3]), default=None)
        if bot is not None and bot < 31:
            s.M.px(x, bot + 1, "wd1" if x % 2 else None)
    return s


def build():
    return [sea_stack(), sea_rocks(), headland(), rocks_sand(), rock_grass(), shells(),
            net_poles(), boat_beached()]
