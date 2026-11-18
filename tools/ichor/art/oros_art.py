#!/usr/bin/env python3
"""gTileset_Oros (Greek: mountain), the outdoor snows of Olympus (design/LEAGUE.md,
design/maps/Ascent_*.md).

Oros is the mountain under open sky: the Leuke snowfield, the Glacier, Boreas's
ridge and the terraces above the cloud, ending at the Propylaia's facade. It is
drawn here in Ichor's own art, 3/4 view, after the feel of Gen 4's snowy
mountain routes (never their tiles): snow you wade through, drifts, frozen
tarns, snow-laden firs, sheer cliff faces with stairs cut into them, rocks
poking through the snow, wind-scoured ridges and a sea of cloud below.

The terrain is an autotile drawn procedurally, one metatile per signature, so
every edge, corner and end exists (STYLE.md §4.3):

  ground  g0..g3 (snow, MB_SAND: footprints), gs (in a face's shadow),
          gw0/gw1 (wind-scoured), deep0/deep1 (deep snow, MB_DEEP_SAND: wild
          Pokémon; its front puffs are on the top layer, so you wade in it)
  ice     ice_<sig> (a frozen tarn, MB_ICE: you slide), sig is its shore
  rim     rim_<bits> (a plateau's west, east and north edges, solid)
  face    face_<row>_<left>_<right>[_c] (the south-facing cliff, solid): row
          t/m/b, each end o (open), i (against higher ground) or n; _c drops
          into the cloud sea
  stair   stair_t/m/b (steps cut into a face), ledge_l/m/r (a snow cornice
          you can jump down, MB_JUMP_SOUTH)
  cloud   cloud_0..3 (the sea of cloud round the mountain, a 2x2 pattern)

Props and the facade are drawn below. tools/ichor/art/oros_build.py compiles it.
Palette rule: every 8x8 tile draws from one group of at most 15 colors.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chion_lib as base  # noqa: E402
from chion_lib import Struct  # noqa: E402

C = {
    # snow on the ground, shadow to sunlit; a cool blue-grey so falling flakes read
    "sn0": (96, 112, 160), "sn1": (136, 152, 192), "sn2": (176, 192, 224), "sn3": (208, 216, 240),
    "sn4": (224, 232, 248), "sn5": (248, 248, 248),
    # ice: the frozen tarns
    "ic0": (48, 96, 168), "ic1": (88, 152, 216), "ic2": (136, 200, 240), "ic3": (200, 232, 248),
    # rock: blue-grey limestone, ink to lit
    "rk0": (24, 24, 40), "rk1": (48, 56, 80), "rk2": (80, 88, 120), "rk3": (112, 120, 152),
    "rk4": (144, 152, 184), "rk5": (184, 192, 216),
    # firs and their bark
    "pn0": (16, 40, 48), "pn1": (24, 64, 64), "pn2": (40, 96, 80), "pn3": (72, 128, 96),
    "bk0": (56, 40, 40), "bk1": (104, 72, 48),
    # marble, gold, Olympian blue and red
    "mb0": (72, 72, 96), "mb1": (128, 128, 152), "mb2": (168, 168, 184), "mb3": (208, 200, 208),
    "mb4": (232, 224, 224), "mb5": (248, 240, 232), "au0": (160, 104, 40), "au1": (224, 176, 64),
    "au2": (248, 224, 136), "obl": (40, 72, 144), "ord": (160, 48, 40),
    # bronze and fire
    "bz0": (64, 40, 32), "bz1": (112, 72, 40), "bz2": (168, 112, 56), "bz3": (216, 160, 96),
    "fr0": (200, 64, 24), "fr1": (240, 136, 40), "fr2": (248, 216, 104),
    # sky and the cloud sea
    "sk0": (96, 144, 216), "sk1": (136, 184, 232), "sk2": (176, 208, 240),
    "cl0": (152, 160, 200), "cl1": (192, 200, 232), "cl2": (224, 224, 248), "cl3": (240, 240, 232),
    # the gods' small things: wine, a poppy, a peacock's eye, a silver arrow
    "wn0": (88, 32, 80), "wn1": (144, 64, 120), "pp": (216, 40, 48), "sv": (200, 208, 224),
    # alpine grass through the thinning snow, low on the climb
    "gr1": (72, 128, 64), "gr2": (128, 168, 80),
}

GROUPS = {
    "snow": ["sn0", "sn1", "sn2", "sn3", "sn4", "sn5", "ic0", "ic1", "ic2", "ic3", "rk1", "rk2", "rk3", "pp", "rk0"],
    "rock": ["rk0", "rk1", "rk2", "rk3", "rk4", "rk5", "sn1", "sn2", "sn3", "sn4", "sn5", "ic1", "ic2", "ic3", "bz2"],
    "pine": ["pn0", "pn1", "pn2", "pn3", "bk0", "bk1", "sn1", "sn2", "sn3", "sn4", "sn5", "sn0", "rk1", "rk2", "sv"],
    "marble": ["mb0", "mb1", "mb2", "mb3", "mb4", "mb5", "au0", "au1", "au2", "obl", "ord", "sn2", "sn3", "sn4", "sk1"],
    "bronze": ["bz0", "bz1", "bz2", "bz3", "fr0", "fr1", "fr2", "rk0", "rk1", "mb2", "mb3", "mb4", "sn3", "sn4", "au1"],
    "sky": ["sk0", "sk1", "sk2", "cl0", "cl1", "cl2", "cl3", "sn1", "sn2", "sn3", "sn4", "rk2", "rk3", "rk4", "rk1"],
    "accent": ["wn0", "wn1", "pp", "gr1", "gr2", "au1", "au2", "sv", "sn1", "sn2", "sn3", "sn4", "rk1", "bk1", "pn2"],
}


def h(*a):
    return base.h(*a)


# --------------------------------------------------------------------------
# A canvas of color names
# --------------------------------------------------------------------------

class Cv:
    def __init__(self, w, hh, fill=None):
        self.w, self.h = w, hh
        self.p = np.full((hh, w), fill, object)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[y, x] = c

    def get(self, x, y):
        return self.p[y, x] if 0 <= x < self.w and 0 <= y < self.h else None

    def rect(self, x, y, w, hh, c):
        for yy in range(y, y + hh):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def blit(self, other, x, y):
        for j in range(other.h):
            for i in range(other.w):
                c = other.p[j, i]
                if c is not None:
                    self.px(x + i, y + j, c)

    def ellipse(self, cx, cy, rx, ry, fn):
        """fn(dx, dy, d) -> color for each pixel inside (d: 0 center .. 1 edge)."""
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                if d <= 1.0:
                    c = fn(x + 0.5 - cx, y + 0.5 - cy, d)
                    if c:
                        self.px(x, y, c)

    def poly(self, pts, c):
        from PIL import Image, ImageDraw
        m = Image.new("1", (self.w, self.h), 0)
        ImageDraw.Draw(m).polygon(pts, fill=1)
        ys, xs = np.nonzero(np.array(m))
        for y, x in zip(ys, xs):
            self.px(int(x), int(y), c(int(x), int(y)) if callable(c) else c)

    def line(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.px(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

    def crop(self, x, y, w, hh):
        o = Cv(w, hh)
        o.p[:, :] = self.p[y:y + hh, x:x + w]
        return o

    def hflip(self):
        o = Cv(self.w, self.h)
        o.p[:, :] = self.p[:, ::-1]
        return o

    def recolor(self, table):
        o = Cv(self.w, self.h)
        for y in range(self.h):
            for x in range(self.w):
                c = self.p[y, x]
                o.p[y, x] = table.get(c, c) if c is not None else None
        return o

    def mask(self):
        return np.array([[c is not None for c in r] for r in self.p])

    def rgba(self):
        a = np.zeros((self.h, self.w, 4), np.uint8)
        for y in range(self.h):
            for x in range(self.w):
                c = self.p[y, x]
                if c is not None:
                    a[y, x, :3] = C[c]
                    a[y, x, 3] = 255
        return a

    def outline(self, ink, lit=None):
        m = self.mask()
        out = []
        for y in range(self.h):
            for x in range(self.w):
                if m[y, x]:
                    continue
                hit = []
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    X, Y = x + dx, y + dy
                    if 0 <= X < self.w and 0 <= Y < self.h and m[Y, X]:
                        hit.append((dx, dy))
                if hit:
                    out.append((x, y, lit if lit and all(d in ((1, 0), (0, 1)) for d in hit) else ink))
        for x, y, c in out:
            self.px(x, y, c)


def ascii_cv(rows, legend):
    cv = Cv(len(rows[0]), len(rows))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in legend:
                cv.p[y, x] = legend[ch]
    return cv


# --------------------------------------------------------------------------
# Ground
# --------------------------------------------------------------------------

GL = {".": "sn3", "+": "sn4", "-": "sn2", ":": "sn1", "*": "sn5", "o": "rk2", "O": "rk3", "x": "rk1"}

GROUND = {
    "g0": ["................",
           "................",
           "..++++..........",
           ".+----+.........",
           "................",
           "...........+....",
           "..........+-+...",
           "................",
           "................",
           "................",
           "....+++.........",
           "...+---+........",
           "................",
           "..........++....",
           ".........+--+...",
           "................"],
    "g1": ["................",
           "........+++.....",
           ".......+---+....",
           "................",
           "................",
           "..+.............",
           ".+-+............",
           "................",
           "...........+++..",
           "..........+---+.",
           "................",
           "................",
           ".....++.........",
           "....+--+........",
           "................",
           "................"],
    "g2": ["................",
           "................",
           "......+.........",
           ".....+-+........",
           "................",
           "............*...",
           "................",
           "..++............",
           ".+--+...........",
           "................",
           "...........++...",
           "..........+--+..",
           "................",
           "...*............",
           "................",
           "................"],
    "g3": ["................",
           "..........++....",
           ".........+--+...",
           "................",
           "...+............",
           "..+O+...........",
           "..+oo...........",
           "................",
           "................",
           ".........+++....",
           "........+---+...",
           "................",
           "................",
           "....++..........",
           "...+--+.........",
           "................"],
    # wind-scoured: the snow blown thin, streaks and bare rock showing
    "gw0": ["................",
            "-----...........",
            "++++++..........",
            "..........------",
            "...........+++++",
            "................",
            "....o...........",
            "...xo...........",
            "................",
            ".....--------...",
            "......++++++....",
            "................",
            "-..........-----",
            "+...........++++",
            "................",
            "................"],
    "gw1": ["................",
            "........-------.",
            ".........++++++.",
            "................",
            "--..............",
            "++..............",
            "..........o.....",
            ".........xoo....",
            "................",
            "---.............",
            "+++++...........",
            "................",
            ".........-------",
            "..........++++++",
            "................",
            "................"],
}


def ground_cv(key="g0"):
    return ascii_cv(GROUND[key], GL)


def alpine_cv(variant):
    """Alpine grass showing through patchy snow, low on the climb: tufts of green,
    a few wildflowers (poppies, gold), the snow lying in drifts between."""
    cv = Cv(16, 16, "sn3")
    tufts = [[(2, 3), (9, 2), (13, 8), (5, 10), (10, 13)], [(4, 1), (12, 4), (1, 8), (8, 9), (13, 13), (4, 14)],
             [(7, 3), (2, 7), (11, 9), (6, 13)]][variant]
    for (tx, ty) in tufts:
        for (dx, dy, c) in ((0, 0, "gr1"), (1, 0, "gr2"), (-1, 1, "gr1"), (0, 1, "gr2"), (1, 1, "gr1"), (2, 1, "pn2"),
                            (0, 2, "pn2"), (1, 2, "gr1")):
            cv.px((tx + dx) % 16, (ty + dy) % 16, c)
    if variant == 1:
        for (fx, fy, c) in ((6, 6, "pp"), (14, 11, "au2"), (3, 12, "pp")):
            cv.px(fx, fy, c)
    if variant == 2:
        for (fx, fy, c) in ((10, 5, "au2"), (4, 9, "pp")):
            cv.px(fx, fy, c)
    for (x, y) in ((11, 1), (12, 1), (6, 15), (7, 15), (15, 6)):
        cv.px(x, y, "sn4")
    for (x, y) in ((3, 5), (4, 5), (12, 12)):
        cv.px(x, y, "sn2")
    return cv


def path_cv(N, S, E, W):
    """Packed snow, trodden into a path: smoother and bluer than the drifts round it,
    with old footprints; a soft fringe of loose snow on each side that meets them."""
    cv = Cv(16, 16, "sn2")
    for (x, y) in ((3, 2), (4, 3), (10, 6), (11, 7), (5, 10), (6, 11), (12, 13), (13, 14), (2, 14), (8, 1)):
        cv.px(x, y, "sn1")
    for (x, y) in ((7, 4), (1, 8), (14, 9), (9, 12), (12, 2)):
        cv.px(x, y, "sn3")
    for i in range(16):
        k = 2 + (1 if (i * 7) % 5 == 0 else 0)
        for j in range(k):
            c = "sn3" if j == k - 1 else "sn4" if j else "sn3"
            if N:
                cv.px(i, j, c)
            if S:
                cv.px(i, 15 - j, c)
            if W:
                cv.px(j, i, c)
            if E:
                cv.px(15 - j, i, c)
    return cv


def shadow_cv():
    """Ground at a cliff's foot: the face's shadow along the top."""
    cv = ground_cv("g1")
    for x in range(16):
        cv.px(x, 0, "sn1")
        cv.px(x, 1, "sn2")
        cv.px(x, 2, "sn2" if (x // 3) % 2 else "sn3")
    return cv


DEEP_MOUNDS = [
    [(3.5, 3.5, 4.2, 3.0), (11.5, 5.0, 4.8, 3.3), (6.5, 11.5, 5.4, 3.6), (14.5, 12.5, 3.6, 3.0), (-1.0, 12.0, 3.4, 3.0)],
    [(5.0, 4.5, 5.2, 3.4), (13.5, 3.0, 3.6, 2.8), (2.0, 12.5, 4.0, 3.2), (10.5, 11.0, 5.0, 3.5), (17.5, 12.0, 3.0, 3.0)],
    [(8.0, 3.5, 5.6, 3.2), (0.5, 6.5, 3.2, 2.8), (4.0, 12.0, 4.6, 3.4), (12.5, 12.5, 4.4, 3.2), (16.5, 6.5, 3.0, 2.8)],
]


def deep_cv(variant=0):
    """Deep snow: soft white heaps over blue hollows; the front heaps' lower
    halves are on the top layer, so the player wades in up to the knees."""
    bot, top = Cv(16, 16, "sn3"), Cv(16, 16)
    for y in range(16):
        for x in range(16):
            if (x * 3 + y * 5 + variant) % 13 == 0:
                bot.px(x, y, "sn2")
    for (cx, cy, rx, ry) in sorted(DEEP_MOUNDS[variant], key=lambda m: m[1]):
        front = cy > 9

        def col(dx, dy, d, rx=rx, ry=ry):
            if dy > ry * 0.55:
                return "sn2" if dy < ry * 0.85 else "sn1"
            if dy > ry * 0.1:
                return "sn4"
            if dy < -ry * 0.3 and dx < rx * 0.3:
                return "sn5"
            return "sn5" if d < 0.3 else "sn4"
        for ox in (-16, 0, 16):
            (top if front else bot).ellipse(cx + ox, cy, rx, ry, col)
            if front:
                bot.ellipse(cx + ox, cy, rx, ry, col)
    for y in range(16):
        for x in range(16):
            if y < 9:
                top.p[y, x] = None
    return bot, top


# --------------------------------------------------------------------------
# Ice
# --------------------------------------------------------------------------

def ice_center(variant=0):
    """Slick ice the Gen 3 way: pale azure crossed by bold diagonal bands of light,
    a few darker scratches (it repeats every 16 px, so the bands run on)."""
    cv = Cv(16, 16, "ic2")
    for y in range(16):
        for x in range(16):
            t = (x + y + variant * 5) % 16
            if t < 5:
                cv.px(x, y, "ic3")
            elif t == 5 or t == 15:
                cv.px(x, y, "ic2")
            elif t == 10 and (x // 4 + variant) % 2:
                cv.px(x, y, "ic3")
    for i in range(3):
        cv.px((5 + i + variant * 6) % 16, (12 - i) % 16, "ic1")
    cv.px((12 + variant * 3) % 16, 6, "sn5")
    return cv


def ice_cv(sig):
    """sig: a set of shore sides out of n s e w (straight shores) and
    ne nw se sw (inner corners: only the diagonal is land)."""
    cv = ice_center(0)

    def bank(x, y, d):
        # d: depth into the ice from the shore (0 = the shore line)
        if d == 0:
            cv.px(x, y, "sn4")
        elif d == 1:
            cv.px(x, y, "sn3")
        elif d == 2:
            cv.px(x, y, "sn1")
        elif d == 3:
            cv.px(x, y, "ic1")
    for y in range(16):
        for x in range(16):
            ds = []
            if "n" in sig:
                ds.append(y)
            if "s" in sig:
                ds.append(15 - y + 1)
            if "w" in sig:
                ds.append(x)
            if "e" in sig:
                ds.append(15 - x + 1)
            for corner, (cx, cy) in (("nw", (0, 0)), ("ne", (16, 0)), ("sw", (0, 16)), ("se", (16, 16))):
                if corner in sig:
                    r = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                    ds.append(max(0, int(r) - 2) if r < 6 else 9)
            if ds:
                d = min(ds)
                if "s" in sig and d == 15 - y + 1:
                    # the south shore: the bank is seen from above, the ice lip below it
                    d = {1: 0, 2: 1, 3: 3}.get(d, d)
                bank(x, y, d) if d <= 3 else None
                if d < 0:
                    cv.px(x, y, "sn4")
    # snow beyond the shore line
    for y in range(16):
        for x in range(16):
            if ("n" in sig and y < 1) or ("w" in sig and x < 1) or ("e" in sig and x > 14) or ("s" in sig and y > 15):
                cv.px(x, y, "sn4")
    return cv


ICE_SIGS = {
    "c": set(), "n": {"n"}, "s": {"s"}, "e": {"e"}, "w": {"w"},
    "nw": {"n", "w"}, "ne": {"n", "e"}, "sw": {"s", "w"}, "se": {"s", "e"},
    "inw": {"nw"}, "ine": {"ne"}, "isw": {"sw"}, "ise": {"se"},
}


# --------------------------------------------------------------------------
# Cliff faces, rims, stairs, ledges
# --------------------------------------------------------------------------

_FACETS = {}


def facets(seed, n=3):
    """A 16x16 tile of rock masses (Voronoi on a torus): (facet id, its center) per pixel."""
    if seed not in _FACETS:
        pts = [((i * 16 / n + (h(seed, i) % 50) / 10.0) % 16, (h(seed, i, 7) % 160) / 10.0) for i in range(n)]
        ids = np.zeros((16, 16), int)
        for y in range(16):
            for x in range(16):
                best, bi = 1e9, 0
                for i, (px_, py_) in enumerate(pts):
                    dx = min(abs(x + 0.5 - px_), 16 - abs(x + 0.5 - px_))
                    dy = min(abs(y + 0.5 - py_), 16 - abs(y + 0.5 - py_)) * 1.15
                    d = dx * dx + dy * dy
                    if d < best:
                        best, bi = d, i
                ids[y, x] = bi
        _FACETS[seed] = (ids, pts)
    return _FACETS[seed]


def rock_cell(seed, snowy=0.5):
    """Craggy rock in chunky masses: each mass split into a lit plane (top left)
    and a shaded one (bottom right), inked under and right, its top edge
    catching light or a lip of snow."""
    ids, pts = facets(seed)
    cv = Cv(16, 16)
    for y in range(16):
        for x in range(16):
            f = ids[y, x]
            cx, cy = pts[f]
            dx = (x + 0.5 - cx + 8) % 16 - 8
            dy = (y + 0.5 - cy + 8) % 16 - 8
            up, dn = ids[(y - 1) % 16, x], ids[(y + 1) % 16, x]
            rt = ids[y, (x + 1) % 16]
            lf = ids[y, (x - 1) % 16]
            plane = dx * 0.9 + dy * 0.6
            c = "rk4" if plane < -2.2 else "rk3" if plane < 2.0 else "rk2"
            if dn != f or rt != f:
                c = "rk1"
            elif up != f:
                c = "sn4" if (h(seed, f, 3) % 100) < snowy * 100 else "rk5"
            elif ids[(y - 2) % 16, x] != f and (h(seed, f, 3) % 100) < snowy * 100:
                c = "sn3"
            elif lf != f:
                c = "rk4" if c != "rk2" else "rk3"
            cv.px(x, y, c)
    return cv


def face_cv(row, left, right, cloud=False, variant=0):
    cv = rock_cell(11 + variant * 5 + {"t": 0, "m": 1, "b": 2}[row])
    if row == "t":
        # the snow cornice over the cliff's edge: a wavy overhang, icicles under it
        for x in range(16):
            lip = 4 + round(1.2 * math.sin((x + variant * 4) * 0.9) + 0.6 * math.sin(x * 2.1))
            for y in range(lip):
                cv.px(x, y, "sn5" if y == 0 else "sn4" if y < lip - 1 else "sn3")
            cv.px(x, lip, "rk0" if x % 4 else "rk1")
            if (x + variant * 3) % 5 == 1:
                cv.px(x, lip + 1, "ic3")
                cv.px(x, lip + 2, "ic2")
    if row == "b":
        # the foot: darker rock, a shadow line, the snow drifted against it
        for y in range(16):
            for x in range(16):
                if y > 6 and cv.p[y, x] == "rk3":
                    cv.px(x, y, "rk2")
        for x in range(16):
            top = 11 + round(1.1 * math.sin((x + variant * 5) * 0.7))
            cv.px(x, top - 1, "rk1")
            for y in range(top, 16):
                cv.px(x, y, "sn5" if y == top else "sn4" if y < top + 2 else "sn3")
    # ends
    for side in ("l", "r"):
        kind = left if side == "l" else right
        if kind == "n":
            continue
        for y in range(16):
            for i in range(5):
                x = i if side == "l" else 15 - i
                if kind == "o":
                    # the cliff's end: rounded, ground beyond
                    w = 2 + (1 if row == "t" and y < 6 else 0) + (1 if row == "b" and y > 9 else 0)
                    if i < w - 1:
                        cv.px(x, y, "sn3" if not (row == "b" and y > 12) else "sn3")
                    elif i == w - 1:
                        cv.px(x, y, "rk1")
                    elif i == w:
                        cv.px(x, y, "rk4" if side == "l" else "rk2")
                elif kind == "i":
                    # against higher ground: a corner in shadow
                    if i == 0:
                        cv.px(x, y, "rk1")
                    elif i == 1:
                        cv.px(x, y, "rk2")
    if row == "t":
        for side, kind in (("l", left), ("r", right)):
            if kind == "o":
                for y in range(4):
                    for i in range(2 + (1 if y < 3 else 0)):
                        cv.px(i if side == "l" else 15 - i, y, "sn3")
    if cloud:
        cv = cv.recolor({"rk0": "rk1", "rk5": "rk4", "sn5": "sn4", "ic2": "sn3", "ic1": "sn2", "ic3": "sn4"})
        if row == "b":
            # the cliff drops into the cloud: wisps over the rock
            for y in range(16):
                for x in range(16):
                    t = y + 3 * math.sin((x + variant * 3) * 0.55)
                    if t > 11:
                        cv.px(x, y, "cl2" if t < 13 else "cl1")
                    elif t > 9.5:
                        cv.px(x, y, "cl3")
        for side, kind in (("l", left), ("r", right)):
            if kind == "o":
                for y in range(16):
                    for i in range(2):
                        x = i if side == "l" else 15 - i
                        if cv.p[y, x] in ("sn3",):
                            cv.px(x, y, "cl1")
    return cv


def rim_cv(N, W, E, iNW, iNE):
    """A plateau's edge: a band of craggy rock where the ground drops away (west,
    east or north), the snow curling over it."""
    cv = ground_cv("g0")
    rock = rock_cell(21, snowy=0.2)
    for y in range(16):
        wl = 4 + (1 if (y // 3) % 2 else 0)
        for x in range(16):
            if W and x < wl:
                cv.px(x, y, "rk1" if x == 0 else rock.p[y, x])
            if E and x > 15 - wl:
                cv.px(x, y, "rk1" if x == 15 else rock.p[y, x])
        if W:
            cv.px(wl, y, "sn5")
            cv.px(wl + 1, y, "sn4")
        if E:
            cv.px(15 - wl, y, "sn4")
            cv.px(14 - wl, y, "sn3")
    if N:
        for x in range(16):
            hl = 3 + (1 if (x // 4) % 2 else 0)
            for y in range(hl):
                cv.px(x, y, "rk1" if y == 0 else rock.p[y, x])
            cv.px(x, hl, "sn5")
            cv.px(x, hl + 1, "sn4")
    if N and W:
        for y in range(6):
            for x in range(6):
                if x + y < 4:
                    cv.px(x, y, "rk1" if x + y < 2 else "rk2")
    if N and E:
        for y in range(6):
            for x in range(10, 16):
                if (15 - x) + y < 4:
                    cv.px(x, y, "rk1" if (15 - x) + y < 2 else "rk2")
    for corner, on in (("nw", iNW), ("ne", iNE)):
        if not on:
            continue
        for y in range(6):
            for i in range(6):
                x = i if corner == "nw" else 15 - i
                r = math.hypot(i + 0.5, y + 0.5)
                if r < 3.0:
                    cv.px(x, y, "rk1" if r < 1.8 else rock.p[y, x])
                elif r < 4.0:
                    cv.px(x, y, "sn5")
                elif r < 5.0:
                    cv.px(x, y, "sn4")
    return cv


def rim_key(N, W, E, iNW, iNE):
    s = "".join(k for k, v in (("N", N), ("W", W), ("E", E), ("a", iNW), ("b", iNE)) if v)
    return "rim_" + s


def rim_combos():
    out = []
    for N in (0, 1):
        for W in (0, 1):
            for E in (0, 1):
                for a in (0, 1):
                    for b in (0, 1):
                        if (a and (N or W)) or (b and (N or E)):
                            continue
                        if not (N or W or E or a or b):
                            continue
                        out.append((N, W, E, a, b))
    return out


def stair_cv(row):
    cv = Cv(16, 16)
    for y in range(16):
        yy = y % 8
        for x in range(16):
            if yy < 2:
                c = "sn4" if yy == 0 else "sn3"
            elif yy < 5:
                c = "rk4" if yy == 2 else "rk3"
            elif yy < 7:
                c = "rk2"
            else:
                c = "rk1"
            cv.px(x, y, c)
        cv.px(0, y, "rk1")
        cv.px(15, y, "rk1")
        cv.px(1, y, "rk2")
        cv.px(14, y, "rk2")
    if row == "t":
        for x in range(16):
            cv.px(x, 0, "sn4")
    if row == "b":
        for x in range(16):
            for y in (14, 15):
                cv.px(x, y, "sn3" if y == 14 else "sn2")
    return cv


def ledge_cv(part):
    cv = ground_cv("g0")
    for x in range(16):
        top = 8 + (1 if x % 5 == 2 else 0)
        for y in range(top, 16):
            d = y - top
            cv.px(x, y, ("sn5", "sn4", "sn4", "sn3", "sn1", "sn2", "sn2", "sn3")[min(d, 7)])
    if part in ("l", "r"):
        for y in range(6, 16):
            for i in range(3):
                x = i if part == "l" else 15 - i
                if i + (y - 6) // 3 < 3:
                    cv.px(x, y, "sn3" if i else "sn2")
    return cv


def cloud_sheet():
    """The cloud sea: a 32x32 repeating sheet of puffs over the sky's blue."""
    cv = Cv(32, 32, "sk2")
    puffs = [(6, 6, 7, 5), (22, 4, 8, 5), (14, 17, 9, 6), (30, 19, 6, 5), (2, 22, 6, 5), (24, 29, 8, 5),
             (8, 30, 7, 4)]
    for (cx, cy, rx, ry) in puffs:
        for oy in (-32, 0, 32):
            for ox in (-32, 0, 32):
                cv.ellipse(cx + ox, cy + oy, rx, ry,
                           lambda dx, dy, d: "cl0" if dy > ry * 0.55 else "cl1" if dy > 0 else
                           "cl3" if (dy < -ry * 0.4 and dx < 0) else "cl2")
    return cv


def cloud_bridge_cv(variant):
    cv = cloud_sheet().crop(16 * variant, 0, 16, 16)
    for y in range(4, 12):
        for x in range(16):
            cv.px(x, y, "cl3" if y in (4, 5) else "cl2" if y < 10 else "cl1")
    for x in range(0, 16, 5):
        cv.px((x + variant * 2) % 16, 8, "sn2")
    return cv


# --------------------------------------------------------------------------
# Props
# --------------------------------------------------------------------------

def fir(w, hh, tiers, trunk_h, lean=0, arrow=False):
    """A snow-laden fir on its own canvas: tiers of (top y, height, half width)."""
    cv = Cv(w, hh)
    cx = w / 2
    tx = int(cx) - 2
    for y in range(hh - trunk_h - 2, hh - 3):
        for x in range(tx, tx + 4):
            cv.px(x, y, "bk1" if x == tx else "bk0")
    for i, (ty, th, hw) in enumerate(tiers):
        off = lean * i
        pts_top = (cx + off, ty)

        def col(x, y, ty=ty, th=th, hw=hw, off=off):
            t = (y - ty) / th
            rel = (x + 0.5 - (cx + off)) / max(1.0, hw * t + 1)
            if y >= ty + th - 2:
                return "pn0"
            if rel < -0.45:
                return "pn3"
            if rel > 0.35:
                return "pn1"
            return "pn2"
        cv.poly([pts_top, (cx + off - hw, ty + th), (cx + off + hw, ty + th)], col)
        # snow on the tier: along its upper slopes, and clumps on the boughs' ends
        for y in range(int(ty), int(ty + th)):
            t = (y - ty) / th
            half = hw * t
            for x in range(int(cx + off - half), int(cx + off + half) + 1):
                if cv.get(x, y) is None:
                    continue
                above = cv.get(x, y - 1) is None or y - 1 < ty
                if above or (cv.get(x, y - 2) is None and (x + y) % 3):
                    cv.px(x, y, "sn5" if x < cx + off else "sn4")
                elif cv.get(x, y - 3) is None and (x * 3 + y) % 4 == 0:
                    cv.px(x, y, "sn3")
        yb = int(ty + th) - 1
        for x in range(int(cx + off - hw), int(cx + off + hw) + 1):
            if (x + i) % 4 in (0, 1) and cv.get(x, yb) is not None:
                cv.px(x, yb, "sn3")
                cv.px(x, yb - 1, "sn4")
    cv.outline("pn0")
    # snow heaped at the foot
    for x in range(int(cx) - 6, int(cx) + 6):
        for y in range(hh - 4, hh):
            if abs(x + 0.5 - cx) < 6 - (hh - 1 - y) * 0.5 + (y - (hh - 4)) * 0.6:
                cv.px(x, y, "sn4" if y == hh - 4 else "sn3" if y < hh - 1 else "sn2")
    if arrow:
        for i in range(9):
            cv.px(int(cx) - 1 + i, hh - trunk_h - 6 + (i // 4), "sv")
        cv.px(int(cx) + 8, hh - trunk_h - 7, "sn5")
        cv.px(int(cx) + 8, hh - trunk_h - 4, "sn5")
    return cv


def rock_cv(w, hh, seed=0, snow=True):
    cv = Cv(w, hh)
    cx, cy = w / 2, hh * 0.58
    rx, ry = w / 2 - 1.5, hh * 0.4

    def col(dx, dy, d):
        if dy < -ry * 0.35:
            return "sn5" if dx < 0 else "sn4"
        if dy < -ry * 0.15:
            return "sn3"
        if dx < -rx * 0.3:
            return "rk4"
        if dx > rx * 0.35 or dy > ry * 0.5:
            return "rk2"
        return "rk3"
    cv.ellipse(cx, cy, rx, ry, col)
    for i in range(3):
        x = int(cx + (h(seed, i) % 5) - 2)
        y = int(cy + (h(seed, i, 1) % 3))
        cv.px(x, y, "rk1")
        cv.px(x + 1, y + 1, "rk1")
    cv.outline("rk1")
    return cv


def drift_cv(w, hh, wine=False):
    cv = Cv(w, hh)
    for k in range(max(1, w // 12)):
        pass
    bumps = [(w * 0.3, hh * 0.55, w * 0.32, hh * 0.42), (w * 0.68, hh * 0.5, w * 0.34, hh * 0.45)]
    for (cx, cy, rx, ry) in bumps:
        cv.ellipse(cx, cy, rx, ry, lambda dx, dy, d, ry=ry: "sn5" if dy < -ry * 0.4 else
                   "sn4" if dy < 0 else "sn3" if dy < ry * 0.5 else "sn2")
    m = cv.mask()
    for y in range(hh):
        for x in range(w):
            if m[y, x] and (y + 1 >= hh or not m[y + 1, x]):
                cv.px(x, y, "sn1")
    if wine:
        for (x, y) in ((w // 2 - 2, hh // 2), (w // 2 - 1, hh // 2), (w // 2, hh // 2 + 1), (w // 2 + 1, hh // 2 + 1),
                       (w // 2 + 2, hh // 2), (w // 2 - 3, hh // 2 + 1), (w // 2 + 3, hh // 2 + 2), (w // 2, hh // 2 + 2),
                       (w // 2 - 1, hh // 2 + 1), (w // 2 + 1, hh // 2), (w // 2 + 4, hh // 2 + 2)):
            cv.px(x, y, "wn1")
        cv.px(w // 2, hh // 2 + 3, "wn0")
        cv.px(w // 2 + 1, hh // 2 + 3, "wn0")
    return cv


def grid_to(cv, structs_out, key, title, section, w, hh, walk, floor=None, top_rows=0, mb=None,
            names=None, notes="", behaviors=None):
    """Turn a canvas (w*16 x hh*16) into a Struct: `floor` (a Cv 16x16 or None)
    under every cell on the bottom layer, the art on the middle layer; the
    first `top_rows` rows' art goes to the top layer (drawn over the player)."""
    s = Struct(key, title, w, hh, section, walk=walk, notes=notes, names=names, floor_mb=mb)
    art = cv.rgba()
    if floor is not None:
        f = floor.rgba() if isinstance(floor, Cv) else floor
        for cy in range(hh):
            for cx in range(w):
                s.layers["bottom"].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = f
        for cy in range(hh):
            for cx in range(w):
                tgt = "top" if cy < top_rows else "middle"
                s.layers[tgt].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = art[cy * 16:cy * 16 + 16,
                                                                                  cx * 16:cx * 16 + 16]
    else:
        s.layers["bottom"].a[:] = art
    for (x, y), b in (behaviors or {}).items():
        s.behaviors[(x, y)] = b
    structs_out.append(s)
    return s


def flatten(cv, floor):
    """The art composited over a floor, as one opaque canvas."""
    out = Cv(cv.w, cv.h)
    for y in range(cv.h):
        for x in range(cv.w):
            c = cv.p[y, x]
            out.p[y, x] = c if c is not None else floor.p[y % floor.h, x % floor.w]
    return out


def plain_snow():
    return Cv(16, 16, "sn3")


def plate_cv(down):
    cv = Cv(16, 16, "sn3")
    for x in range(16):
        if x % 5 == 1:
            cv.px(x, 2, "sn4")
    cv.ellipse(8, 8.5, 6.5, 5.5, lambda dx, dy, d: ("bz1" if down else "bz3") if dy < -2 else
               ("bz0" if down else "bz2") if d > 0.7 else ("bz1" if down else "bz2"))
    for x in range(4, 13):
        cv.px(x, 8, "bz0" if not down else "rk1")
    for y in range(5, 12):
        cv.px(8, y, "bz0" if not down else "rk1")
    if not down:
        cv.ellipse(8, 8.5, 2.2, 1.8, lambda dx, dy, d: "au1")
    return cv


def grate_cv(up):
    cv = Cv(16, 16, "rk1")
    for y in range(16):
        for x in range(16):
            yy = y % 8
            cv.px(x, y, "sn4" if yy == 0 else "sn3" if yy < 3 else "rk1" if yy > 5 else "mb2")
        cv.px(0, y, "rk0")
        cv.px(15, y, "rk0")
    if not up:
        for x in (2, 5, 8, 11, 13):
            for y in range(16):
                cv.px(x, y, "bz2" if y % 4 else "bz3")
                cv.px(x + 1, y, "bz0")
        for x in range(16):
            cv.px(x, 3, "bz1")
            cv.px(x, 12, "bz1")
    return cv


def lever_cv():
    cv = Cv(16, 16, "sn3")
    cv.rect(6, 9, 4, 6, "bz1")
    cv.rect(6, 9, 1, 6, "bz2")
    cv.rect(5, 14, 6, 2, "rk1")
    cv.line(8, 9, 12, 3, "bz2")
    cv.line(9, 9, 13, 3, "bz0")
    cv.rect(11, 1, 3, 3, "au1")
    return cv


def stele_cv():
    cv = Cv(16, 32)
    cv.rect(3, 4, 10, 25, "rk3")
    cv.rect(3, 4, 2, 25, "rk4")
    cv.rect(11, 4, 2, 25, "rk2")
    for y in range(9, 25, 3):
        cv.rect(5, y, 6, 1, "rk1")
    cv.rect(2, 28, 12, 3, "rk2")
    cv.rect(2, 28, 12, 1, "rk4")
    for x in range(3, 13):
        cv.px(x, 3, "sn5")
        cv.px(x, 4, "sn4")
    cv.px(4, 5, "sn4")
    cv.px(9, 5, "sn4")
    cv.outline("rk1")
    return cv


def tripod_cv(lit=False):
    cv = Cv(16, 32)
    cv.ellipse(8, 10, 6.5, 3.5, lambda dx, dy, d: "bz3" if dy < -1 else "bz2" if d < 0.6 else "bz1")
    for x0, x1 in ((4, 2), (8, 8), (12, 14)):
        cv.line(x0, 12, x1, 29, "bz1")
    cv.line(5, 12, 3, 29, "bz2")
    cv.rect(5, 20, 7, 1, "bz2")
    if lit:
        for y in range(1, 8):
            for x in range(5, 12):
                d = abs(x - 8) + (8 - y) * 0.4
                if d < 3.5 - (7 - y) * 0.35 + 1.5:
                    cv.px(x, y, "fr2" if d < 1.2 else "fr1" if d < 2.4 else "fr0")
    else:
        for x in range(3, 14):
            cv.px(x, 8, "sn4")
            cv.px(x, 7, "sn4" if 4 < x < 12 else None)
    cv.outline("bz0")
    return cv


def mouth_cv(roped=False):
    """A cave mouth cut into a tall face (2x2 over its lower m and b rows)."""
    cv = Cv(32, 32)
    for (row, oy) in (("m", 0), ("b", 16)):
        f1, f2 = face_cv(row, "n", "n"), face_cv(row, "n", "n", variant=1)
        cv.blit(f1, 0, oy)
        cv.blit(f2, 16, oy)
    for y in range(6, 32):
        for x in range(4, 28):
            r = ((x + 0.5 - 16) / 12) ** 2 + ((y - 30) / 24) ** 2
            if r <= 1.0:
                cv.px(x, y, "rk0")
            elif r <= 1.18:
                cv.px(x, y, "rk1")
    for x in range(6, 26, 3):
        n = 2 + (x * 7) % 4
        for y in range(10 - (abs(x - 16) // 4), 10 - (abs(x - 16) // 4) + n):
            cv.px(x, y, "ic2" if y % 2 else "ic3")
    for x in range(8, 24):
        cv.px(x, 31, "rk1")
    if roped:
        for (px_, py_) in ((5, 18), (25, 18)):
            cv.rect(px_, py_, 2, 14, "bz2")
            cv.px(px_, py_, "sn5")
        for x in range(7, 25):
            y = 21 + int(2 * math.sin((x - 7) / 18 * math.pi))
            cv.px(x, y, "bz2")
            cv.px(x, y + 1, "rk1")
    return cv


def bronze_door_cv():
    cv = Cv(32, 32, "rk1")
    cv.rect(2, 2, 28, 30, "bz1")
    cv.rect(3, 3, 26, 29, "bz2")
    cv.rect(15, 3, 2, 29, "bz0")
    for i in range(12):
        a = i / 12 * 2 * math.pi
        x = int(16 + 9.5 * math.cos(a))
        y = int(16 + 9.5 * math.sin(a))
        cv.px(x, y, "au1")
        cv.px(x, y - 1, "bz3")
    cv.ellipse(16, 16, 3, 3, lambda dx, dy, d: "bz0" if d < 0.5 else "bz3")
    cv.rect(15, 15, 2, 4, "rk0")
    for x in range(2, 30):
        cv.px(x, 1, "sn4")
        cv.px(x, 2, "sn3")
    return cv


def giant_cv():
    """A Giant of the Gigantomachy frozen in a block of ice (3x3)."""
    cv = Cv(48, 48)
    cv.poly([(3, 10), (12, 2), (36, 1), (46, 9), (45, 46), (2, 46)], lambda x, y: "ic2")
    for y in range(48):
        for x in range(48):
            c = cv.get(x, y)
            if c and (x + y) % 11 == 0:
                cv.px(x, y, "ic3")
            if c and x > 38:
                cv.px(x, y, "ic1")
    # the giant: shoulders, a raised arm, the head, in the ice's murk
    body = Cv(48, 48)
    body.ellipse(24, 16, 5, 6, lambda dx, dy, d: "rk2" if dx > 1 else "rk3")
    body.poly([(12, 24), (36, 24), (34, 46), (14, 46)], lambda x, y: "rk2" if x > 26 else "rk3")
    body.poly([(32, 24), (40, 6), (44, 8), (37, 27)], lambda x, y: "rk2")
    body.poly([(13, 26), (6, 40), (10, 42), (17, 30)], lambda x, y: "rk2")
    for y in range(48):
        for x in range(48):
            if body.p[y, x] and cv.get(x, y):
                cv.px(x, y, body.p[y, x] if (x * 3 + y) % 5 else "ic1")
    cv.px(22, 15, "ic3")
    cv.px(26, 15, "ic3")
    for x in range(4, 46):
        for y in range(0, 6):
            if cv.get(x, y) and (cv.get(x, y - 1) is None or y == 0):
                cv.px(x, y, "sn5")
                cv.px(x, y + 1, "sn4")
    cv.outline("ic0")
    return cv


def frozen_fall_cv():
    """A waterfall frozen down a tall face (2x4: the face's t, m, m and b rows)."""
    cv = Cv(32, 64)
    for (row, oy) in (("t", 0), ("m", 16), ("m", 32), ("b", 48)):
        cv.blit(face_cv(row, "n", "n"), 0, oy)
        cv.blit(face_cv(row, "n", "n", variant=1), 16, oy)
    for y in range(2, 60):
        for x in range(6, 26):
            w = 7 + 2 * math.sin(y / 5.0) + y / 20
            if abs(x + 0.5 - 16) < w:
                band = (x + int(y / 3)) % 6
                cv.px(x, y, ("ic3", "ic2", "ic2", "ic1", "ic2", "ic3")[band])
    for x in range(3, 29):
        cv.px(x, 60, "sn4")
        cv.px(x, 61, "sn3")
        cv.px(x, 62, "sn3")
        cv.px(x, 63, "sn2")
    return cv


def handholds_cv():
    cv = Cv(16, 32)
    cv.blit(face_cv("m", "n", "n", variant=2), 0, 0)
    cv.blit(face_cv("b", "n", "n", variant=2), 0, 16)
    for y in range(7, 28, 5):
        x = 4 + (y * 3) % 7
        cv.rect(x, y, 3, 2, "rk0")
        cv.px(x, y - 1, "sn4")
    return cv


def crevasse_cv():
    cv = Cv(32, 16)
    cv.blit(ground_cv("g0"), 0, 0)
    cv.blit(ground_cv("g1"), 16, 0)
    cv.ellipse(16, 8, 14, 5, lambda dx, dy, d: "rk0" if d < 0.45 else "rk1" if d < 0.7 else
               "ic0" if dy > 0 else "sn1")
    for x in range(4, 28, 4):
        cv.px(x, 4, "sn5")
    return cv


def shield_cv():
    cv = Cv(16, 16, "sn3")
    cv.ellipse(8, 9, 6.5, 4.5, lambda dx, dy, d: "bz3" if (dx < -2 and dy < 0) else "bz2" if d < 0.6 else "bz1")
    for x in range(1, 16):
        for y in range(11, 16):
            cv.px(x, y, "sn4" if y == 11 else "sn3")
    cv.px(6, 7, "bz0")
    cv.px(7, 7, "bz0")
    cv.px(8, 8, "bz0")
    cv.px(10, 6, "rk1")
    cv.px(11, 7, "rk1")
    cv.px(12, 8, "rk1")
    return cv


def poppy_cv():
    cv = ground_cv("g2").recolor({})
    cv.px(8, 9, "rk1")
    cv.px(8, 10, "rk1")
    cv.px(9, 11, "rk1")
    cv.px(9, 12, "rk1")
    for (x, y) in ((6, 6), (7, 6), (8, 5), (9, 6), (10, 6), (7, 7), (8, 7), (9, 7), (7, 5), (9, 5)):
        cv.px(x, y, "pp")
    cv.px(8, 6, "rk0")
    for x in range(5, 12):
        cv.px(x, 13, "sn2")
    return cv


def trident_rock_cv():
    cv = rock_cv(16, 16, seed=9)
    for x0 in (5, 8, 11):
        for y in range(5, 12):
            cv.px(x0, y, "rk0")
    for x in range(5, 12):
        cv.px(x, 11, "rk0")
    return cv


def lyre_rock_cv():
    cv = rock_cv(16, 16, seed=4)
    for y in range(4, 14):
        cv.px(8, y, "rk0")
        cv.px(9, y, "rk1" if y % 3 else "rk0")
    return cv


def basin_cv():
    cv = Cv(32, 16)
    cv.rect(0, 0, 32, 16, "sn3")
    cv.ellipse(16, 8, 15, 7, lambda dx, dy, d: "mb4" if d > 0.62 and dy < 0 else "mb2" if d > 0.62 else "sk1")
    for x in range(8, 24, 3):
        cv.px(x, 8, "sn4")
    cv.px(22, 6, "mb5")
    cv.px(23, 6, "mb5")
    cv.px(24, 7, "au2")
    cv.px(9, 10, "au1")
    cv.px(10, 10, "au2")
    return cv


def herm_cv():
    cv = Cv(16, 16)
    cv.rect(5, 4, 6, 11, "mb3")
    cv.rect(5, 4, 1, 11, "mb4")
    cv.rect(10, 4, 1, 11, "mb2")
    cv.ellipse(8, 3.5, 3.2, 3, lambda dx, dy, d: "mb4" if dx < 0 else "mb3")
    cv.px(7, 3, "mb1")
    cv.px(9, 3, "mb1")
    cv.rect(6, 5, 4, 2, "mb2")
    cv.rect(4, 14, 8, 2, "mb2")
    cv.px(6, 0, "sn4")
    cv.px(7, 0, "sn4")
    cv.px(8, 0, "sn4")
    cv.outline("mb0")
    return cv


def signpost_cv():
    cv = Cv(16, 16)
    cv.rect(7, 8, 2, 8, "bk0")
    cv.rect(2, 3, 12, 7, "bk1")
    cv.rect(2, 3, 12, 1, "sn5")
    cv.rect(2, 9, 12, 1, "bk0")
    for x in range(4, 12, 2):
        cv.px(x, 6, "bk0")
    cv.outline("pn0")
    return cv


def far_peak_cv(w, hh):
    """The summit cone of Olympus far off, rising out of the cloud."""
    cv = cloud_sheet()
    big = Cv(w, hh)
    for y in range(hh):
        for x in range(w):
            big.p[y, x] = cv.p[y % 32, x % 32]
    apex = (w * 0.55, 2)
    for y in range(hh):
        for x in range(w):
            dx = x + 0.5 - apex[0]
            half = (y - apex[1]) * 0.95 + (2 * math.sin(y * 0.7) if y > 10 else 0)
            if y >= apex[1] and abs(dx) < half and y < hh - 10 + 3 * math.sin(x * 0.3):
                snow = y < apex[1] + 14 + 6 * math.sin(x * 0.45) or (x * 5 + y * 3) % 17 < 3
                if dx < -half * 0.2:
                    c = "sn4" if snow else "rk4"
                elif dx > half * 0.45:
                    c = "sn2" if snow else "rk2"
                else:
                    c = "sn3" if snow else "rk3"
                big.px(x, y, c)
    for x in range(w):
        y0 = hh - 10 + int(3 * math.sin(x * 0.3))
        for y in range(y0, hh):
            if (x * 3 + y) % 9 < 6:
                big.px(x, y, "cl2" if y < y0 + 3 else "cl1")
    return big


# --------------------------------------------------------------------------
# The Propylaia's facade: the grand entrance on the cliff top
# --------------------------------------------------------------------------

FW, FH = 44, 16          # metatiles: the whole width of 3F's top edge
# rows: 0-4 the pediment, 5-6 the painted entablature, 7-9 the portico's back wall and
# the bronze doors, 7-12 the columns (capitals on 7, walk behind the shafts on 10-11,
# the bases on 12, the porch's edge), 13-15 the stylobate's steps
DOOR_XS = (21, 22)       # the doors' cells on row DOOR_Y are MB_NON_ANIMATED_DOOR
DOOR_Y = 9
# the colonnade: Ionic columns from the shared kit (tools/ichor/art/columns.py), one cell
# wide at the kit's standard pitch (one cell between columns), the doors' bay 19-24
COLS = tuple(range(0, 19, 2)) + tuple(range(25, 44, 2))
CAP_Y, BASE_Y = 7, 12


# the kit's colors, snapped to Oros's marble group (the forms are the kit's exactly)
KIT_TO_OROS = {"cm0": "mb0", "cm1": "mb1", "cm2": "mb2", "cm3": "mb3", "cm4": "mb4", "cm5": "mb5",
               "cd0": "rk0", "cd1": "mb0", "pr1": "ord", "pb0": "obl", "pb1": "sk1", "pg1": "au1",
               "pg2": "au2", "ps": "mb2", "gd": "mb1", "sw1": "sn4", "sw2": "sn2"}


def ionic_column():
    """The Propylaia's column: the kit's Ionic order in its Olympus variant (columns.py,
    "snow": painted marble with snow on the abacus), 16 x 96 (capital, four rows of
    shaft, base)."""
    import columns as kit
    L = kit.Layer(16, 96)
    kit.paint_column(L, 8, 1, 95, "ionic", "snow")
    cv = Cv(16, 96)
    for y in range(96):
        for x in range(16):
            if L.a[y, x, 3]:
                name = kit.A.RGB2NAME.get(tuple(int(v) for v in L.a[y, x, :3]))
                cv.px(x, y, KIT_TO_OROS.get(name, "mb2"))
    return cv


def kit_free_column(height=3):
    """A free-standing column of the kit's Ionic order on the snow, to flank the
    processional way: the capital and shaft over the player, the base solid, its
    shadow down and right."""
    import columns as kit
    H = height * 16
    L = kit.Layer(16, H)
    kit.paint_column(L, 8, 1, H - 3, "ionic", "snow")
    cv = Cv(16, H)
    for y in range(H):
        for x in range(16):
            if L.a[y, x, 3]:
                name = kit.A.RGB2NAME.get(tuple(int(v) for v in L.a[y, x, :3]))
                cv.px(x, y, KIT_TO_OROS.get(name, "mb2"))
    return cv


def marble_stair_cv(row):
    """Broad marble steps for the processional way, snow swept to the treads' ends."""
    cv = Cv(16, 16)
    for y in range(16):
        yy = y % 8
        for x in range(16):
            c = "mb5" if yy == 0 else "mb4" if yy < 3 else "mb3" if yy < 5 else "mb2" if yy < 7 else "mb1"
            if yy in (1, 2) and (x < 2 or x > 13 or (x + y) % 11 == 0):
                c = "sn4"
            cv.px(x, y, c)
    if row == "t":
        for x in range(16):
            cv.px(x, 0, "sn4")
    if row == "b":
        for x in range(16):
            cv.px(x, 15, "sn3")
    return cv


def facade_layers():
    """The facade as two canvases: what lies under the player (bottom) and the
    columns' capitals and shafts that draw over him (top)."""
    W, H = FW * 16, FH * 16
    cv, top = Cv(W, H), Cv(W, H)
    cx = W / 2
    base_y = 79
    for y in range(base_y + 1):
        for x in range(W):
            cv.p[y, x] = "sk1"
    # the pediment: a slope of 1 in 4, so its cornice tiles repeat along it
    for y in range(base_y + 1):
        half = (y + 1) * 4
        for x in range(W):
            edge = half - abs(x + 0.5 - cx)
            if edge < 0:
                continue
            if edge < 2:
                c = "sn4"
            elif edge < 5:
                c = "mb5"
            elif edge < 7:
                c = "ord" if (x // 4) % 2 else "obl"
            elif edge < 8:
                c = "au1"
            elif edge < 12:
                c = "mb3"
            elif edge < 13:
                c = "mb1"
            else:
                c = "obl"
            cv.px(x, y, c)

    def figure(fx, ftop, w):
        for y in range(ftop, base_y - 2):
            t = (y - ftop) / max(1, base_y - 2 - ftop)
            hw = w * (0.32 if t < 0.2 else 0.5 + 0.5 * t)
            for x in range(int(fx - hw), int(fx + hw) + 1):
                if cv.get(x, y) == "obl":
                    cv.px(x, y, "au1" if x < fx else "au0")
        cv.ellipse(fx, ftop + 2, max(2.0, w * 0.36), 3, lambda dx, dy, d: "au2" if dx < 0 else "au1")
    figure(cx, 26, 16)
    cv.ellipse(cx, 27, 6, 6, lambda dx, dy, d: "au2" if dx < 0 else "au1")
    for (x0, y0, x1, y1) in ((cx + 18, 24, cx + 10, 44), (cx + 10, 44, cx + 19, 48), (cx + 19, 48, cx + 11, 70)):
        for k in (0, 1):
            cv.line(int(x0) + k, y0, int(x1) + k, y1, "au2")
    for i in range(30):
        x = int(cx - 50 + i)
        y = 58 - abs(i - 15) // 2
        for j in range(3):
            cv.px(x, y + j, "au2" if j == 0 else "au1")
    for side in (-1, 1):
        for dxp in (70, 108, 146, 184, 222, 260):
            ftop = int(base_y - (316 - dxp) / 4) + 6
            if ftop < base_y - 10:
                figure(cx + side * dxp, ftop, 8)
    # the entablature, painted: a blue-and-red cornice, a frieze of blue triglyphs and
    # red metopes with gold rosettes, a gold fillet, the architrave
    for y in range(80, 112):
        for x in range(W):
            if y < 82:
                c = "sn4" if y == 80 else "mb5"
            elif y < 85:
                c = "obl" if (x // 4) % 2 else "ord"
                if y == 84:
                    c = "au1" if x % 4 == 0 else "mb5"
            elif y < 101:
                m = x % 32
                if m < 10:
                    c = "obl" if m not in (3, 6) else "mb0"
                    if y < 87:
                        c = "au1"
                else:
                    c = "ord"
                    r = math.hypot(m - 21 + 0.5, y - 93 + 0.5)
                    if r < 4.5:
                        c = "au2" if r < 1.5 else "au1" if r < 3.5 else "au0"
            elif y < 103:
                c = "au1" if y == 101 else "mb1"
            elif y < 110:
                c = "mb4" if y < 105 else "mb3"
            else:
                c = "mb2"
            cv.px(x, y, c)
    # the portico: its back wall in shadow (rows 7-9), panelled
    for y in range(112, 160):
        for x in range(W):
            cv.px(x, y, "mb0" if y < 117 or y > 156 else "mb1" if (x % 32) and (y % 16) else "mb0")
    # the porch floor (rows 10-12): marble slabs, one a cell
    for y in range(160, 208):
        for x in range(W):
            c = "mb2" if x % 16 == 15 or y % 16 == 15 else "mb4" if (x % 16 == 0 or y % 16 == 0) else "mb3"
            cv.px(x, y, c)
    # the bronze doors, four cells wide and three tall (rows 7-9), in the middle bay:
    # a gold lintel, two leaves of studded panels, lion-head knockers
    dx0, dy0 = 20 * 16, 112
    for y in range(dy0, 160):
        for x in range(dx0, dx0 + 64):
            i, j = x - dx0, y - dy0
            if j < 4:
                c = "au1" if j in (1, 2) else "bz0"
            elif i < 3 or i > 60:
                c = "bz0"
            elif i in (31, 32):
                c = "bz0" if i == 31 else "bz1"
            else:
                pi_, pj = (i - 3) % 14, (j - 4) % 14
                c = "bz2"
                if pi_ in (0, 13) or pj in (0, 13):
                    c = "bz3" if (pi_ == 0 or pj == 0) else "bz1"
                elif pi_ in (6, 7) and pj in (6, 7):
                    c = "au1"
                elif (pi_ + pj) % 7 == 0:
                    c = "bz3"
            cv.px(x, y, c)
    for ix in (24, 39):
        cv.ellipse(dx0 + ix, dy0 + 26, 3.4, 3.4, lambda dx, dy, d: "au1" if d > 0.4 else "bz0")
        cv.px(dx0 + ix, dy0 + 30, "au1")
    # the stylobate's steps (rows 13-15)
    for y in range(208, 256):
        for x in range(W):
            yy = (y - 208) % 8
            c = "sn4" if yy == 0 else "mb4" if yy < 3 else "mb3" if yy < 6 else "mb1"
            cv.px(x, y, c)
    # the columns: capitals and shafts over the player, bases under him; each
    # casts its shadow down and right across the porch and the steps
    col = ionic_column()
    for cxc in COLS:
        x0, y0 = cxc * 16, CAP_Y * 16
        for y in range(96):
            for x in range(16):
                c = col.p[y, x]
                if c is None:
                    continue
                if y0 + y < BASE_Y * 16:
                    top.px(x0 + x, y0 + y, c)
                else:
                    cv.px(x0 + x, y0 + y, c)
        for y in range(166, 252):
            for x in range(x0 + 10, x0 + 30):
                k = (y - 166) * 0.25
                if x0 + 9 + k < x < x0 + 15 + k and x < W:
                    c = cv.get(x, y)
                    shade = {"mb3": "mb2", "mb4": "mb3", "mb2": "mb1", "sn4": "mb3", "mb1": "mb0", "mb5": "mb4"}
                    if c in shade and top.get(x, y) is None:
                        cv.px(x, y, shade[c])
    return cv, top


def facade_struct():
    walk = []
    for y in range(FH):
        row = ""
        for x in range(FW):
            in_col = x in COLS
            if y < DOOR_Y or (y == DOOR_Y and x not in DOOR_XS):
                row += "X"
            elif y == DOOR_Y:
                row += "."
            elif y < BASE_Y:
                row += "T" if in_col else "."
            elif y == BASE_Y:
                row += "X" if in_col else "."
            else:
                row += "."
        walk.append(row)
    s = Struct("facade", "the Propylaia's facade: the grand entrance", FW, FH, "facade", walk=walk)
    b, t = facade_layers()
    s.layers["bottom"].a[:] = b.rgba()
    s.layers["top"].a[:] = t.rgba()
    for x in DOOR_XS:
        s.behaviors[(x, DOOR_Y)] = "MB_NON_ANIMATED_DOOR"
    return s


TWELVE = ["hestia", "hermes", "demeter", "dionysus", "artemis", "hephaestus",
          "aphrodite", "apollo", "ares", "poseidon", "athena", "hera"]


def statue_cv(god):
    """One of the Twelve on a plinth (1x2): white marble, the god's mark in gold."""
    cv = Cv(16, 32)
    cv.rect(2, 24, 12, 8, "mb3")
    cv.rect(2, 24, 12, 1, "mb5")
    cv.rect(2, 31, 12, 1, "mb1")
    cv.rect(2, 24, 1, 8, "mb4")
    cv.rect(13, 24, 1, 8, "mb2")
    cv.rect(4, 27, 8, 2, "mb2")
    if god == "champion":
        for x in range(2, 14):
            cv.px(x, 23, "sn4")
        return cv
    # the figure: head, a long robe
    cv.ellipse(8, 5.5, 2.6, 2.8, lambda dx, dy, d: "mb5" if dx < 0 else "mb3")
    cv.poly([(5, 9), (11, 9), (12, 24), (4, 24)], lambda x, y: "mb4" if x < 7 else "mb3" if x < 10 else "mb2")
    for y in range(10, 24, 3):
        cv.px(7, y, "mb2")
        cv.px(9, y + 1, "mb2")
    mark = {
        "hestia": [(12, 10, "ord"), (12, 9, "au2"), (13, 10, "ord"), (12, 11, "au1"), (12, 12, "au1"), (12, 13, "au1")],
        "hermes": [(13, y, "au1") for y in range(6, 20)] + [(12, 7, "au2"), (14, 7, "au2"), (12, 9, "au1"), (14, 9, "au1"),
                                                            (5, 4, "au2"), (11, 4, "au2")],
        "demeter": [(3, y, "au1") for y in range(8, 18)] + [(2, 8, "au2"), (4, 8, "au2"), (2, 10, "au2"), (4, 10, "au2")],
        "dionysus": [(13, y, "au0") for y in range(4, 22)] + [(12, 4, "obl"), (13, 3, "obl"), (14, 4, "obl"),
                                                             (13, 5, "obl")],
        "artemis": [(2, y, "au1") for y in range(7, 19)] + [(3, 6, "au1"), (3, 19, "au1"), (4, 5, "au2"), (4, 20, "au2")],
        "hephaestus": [(13, y, "au0") for y in range(9, 18)] + [(12, 8, "au1"), (13, 8, "au1"), (14, 8, "au1"),
                                                               (12, 9, "au1"), (14, 9, "au1")],
        "aphrodite": [(12, 11, "au2"), (13, 11, "au2"), (13, 10, "au2"), (14, 12, "au1"), (12, 12, "au1"),
                      (13, 12, "au1")],
        "apollo": [(3, 11, "au1"), (3, 12, "au1"), (3, 13, "au1"), (3, 14, "au1"), (2, 10, "au2"), (4, 10, "au2"),
                   (2, 15, "au1"), (3, 15, "au1"), (4, 15, "au1"), (2, 11, "au1"), (4, 11, "au1")],
        "ares": [(13, y, "au0") for y in range(1, 24)] + [(13, 0, "au2"), (2, 12, "ord"), (3, 12, "ord"),
                                                         (2, 13, "ord"), (3, 13, "ord"), (2, 14, "ord")],
        "poseidon": [(13, y, "au1") for y in range(3, 24)] + [(12, 2, "au2"), (14, 2, "au2"), (12, 3, "au1"),
                                                             (14, 3, "au1"), (13, 1, "au2")],
        "athena": [(13, y, "au1") for y in range(2, 24)] + [(6, 2, "au1"), (7, 2, "au1"), (8, 1, "au2"), (9, 2, "au1"),
                                                           (10, 2, "au1"), (3, 13, "au0"), (3, 14, "au0")],
        "hera": [(6, 2, "au2"), (8, 1, "au2"), (10, 2, "au2"), (7, 2, "au1"), (9, 2, "au1")] +
                [(13, y, "au1") for y in range(6, 22)] + [(13, 5, "obl")],
    }[god]
    for (x, y, c) in mark:
        cv.px(x, y, c)
    m = cv.mask()
    cv2 = Cv(16, 32)
    cv2.p[:, :] = cv.p
    cv2.outline("mb0")
    for y in range(24, 32):
        for x in range(16):
            if cv.p[y, x] is None and cv2.p[y, x] == "mb0":
                cv2.p[y, x] = "mb1"
    return cv2


def statue_big(god):
    """The statue at the facade's scale (1x3): the figure drawn taller, on a
    stepped plinth with its name cut in it."""
    small = statue_cv(god)
    cv = Cv(16, 48)
    for y in range(34):
        sy = min(23, int(y * 24 / 34))
        for x in range(16):
            c = small.p[sy, x]
            if c is not None:
                cv.px(x, y, c)
    for y in range(34, 48):
        w = 6 if y < 36 else 7
        for x in range(8 - w, 8 + w):
            u = (x - (8 - w)) / (2 * w)
            c = "mb5" if y in (34, 36) else "mb4" if u < 0.3 else "mb3" if u < 0.8 else "mb2"
            if y == 47:
                c = "mb1"
            cv.px(x, y, c)
        if y in (40, 42):
            for x in range(4, 12, 2):
                cv.px(x, y, "mb1")
    if god == "champion":
        for x in range(2, 14):
            cv.px(x, 33, "sn4")
            cv.px(x, 34, "sn3")
        for y in range(34):
            for x in range(16):
                cv.p[y, x] = None
    for x in range(1, 15):
        cv.px(x, 47, "mb1")
    return cv


def brazier_cv():
    cv = Cv(16, 32)
    cv.rect(5, 18, 6, 12, "bz1")
    cv.rect(5, 18, 2, 12, "bz2")
    cv.rect(3, 29, 10, 3, "bz0")
    cv.ellipse(8, 15, 7, 4, lambda dx, dy, d: "bz3" if dy < -1 else "bz2" if d < 0.6 else "bz1")
    for y in range(1, 13):
        for x in range(2, 15):
            d = abs(x + 0.5 - 8) + (12 - y) * 0.45
            wob = math.sin(y * 1.3 + x) * 0.8
            if d + wob < 6.2 - (12 - y) * 0.12:
                cv.px(x, y, "fr2" if d < 2.2 else "fr1" if d < 4.2 else "fr0")
    cv.outline("bz0")
    return cv


# --------------------------------------------------------------------------
# Building the structs
# --------------------------------------------------------------------------

def one_cv(out, key, title, section, cv, walk=".", mb=None, top=None, behavior=None):
    s = Struct(key, title, 1, 1, section, walk=[walk], floor_mb=mb)
    s.layers["bottom"].a[:] = cv.rgba()
    if top is not None:
        s.layers["top"].a[:] = top.rgba()
    if behavior:
        s.behaviors[(0, 0)] = behavior
    out.append(s)
    return s


def terrain(which="oros"):
    """The autotile. Its common part comes first and in the same order in both
    tilesets, so the two get the same metatile ids for it: Boreas's ridge (Oros)
    and 3F (Propylon) are joined by a map connection, which draws each map's edge
    with the other's tileset, so their seams use only these. Propylon has no
    tarns, deep snow or ledges."""
    full = which == "oros"
    out = []
    for k in ("g0", "g1", "g2", "g3"):
        one_cv(out, k, "snow", "terrain", ground_cv(k), mb="MB_SAND")
    one_cv(out, "gs", "snow in a cliff's shadow", "terrain", shadow_cv(), mb="MB_SAND")
    for bits in range(16):
        N, S, E, W = (bits >> 3) & 1, (bits >> 2) & 1, (bits >> 1) & 1, bits & 1
        one_cv(out, f"path_{bits}", "a path of packed snow", "terrain", path_cv(N, S, E, W), mb="MB_SAND")
    for (N, W, E, a, b) in rim_combos():
        one_cv(out, rim_key(N, W, E, a, b), "a plateau's edge", "terrain", rim_cv(N, W, E, a, b), walk="X" if (N or W or E) else ".", mb=None if (N or W or E) else "MB_SAND")
    for row in ("t", "m", "b"):
        for left in ("o", "i", "n"):
            for right in ("o", "i", "n"):
                one_cv(out, f"face_{row}_{left}_{right}", "cliff face", "terrain", face_cv(row, left, right), walk="X")
        one_cv(out, f"face_{row}_n_n_v", "cliff face", "terrain", face_cv(row, "n", "n", variant=1), walk="X")
        for left in ("o", "n"):
            for right in ("o", "n"):
                one_cv(out, f"face_{row}_{left}_{right}_c", "cliff over the cloud", "terrain",
                       face_cv(row, left, right, cloud=True), walk="X")
    for row in ("t", "m", "b"):
        one_cv(out, f"stair_{row}", "steps cut in the cliff", "terrain", stair_cv(row))
    sheet = cloud_sheet()
    for i in range(4):
        one_cv(out, f"cloud_{i}", "the sea of cloud", "terrain", sheet.crop((i % 2) * 16, (i // 2) * 16, 16, 16), walk="X")
    COMMON.update(s.key for s in out)
    if not full:
        for row in ("t", "m", "b"):
            one_cv(out, f"mstair_{row}", "the processional way's marble steps", "terrain", marble_stair_cv(row))
    if full:
        for k in ("gw0", "gw1"):
            one_cv(out, k, "wind-scoured snow", "terrain", ground_cv(k), mb="MB_SAND")
        for v in (0, 1, 2):
            b, t = deep_cv(v)
            one_cv(out, f"deep{v}", "deep snow (wild Pokémon)", "terrain", b, walk="T", mb="MB_DEEP_SAND", top=t)
        one_cv(out, "ice_c2", "frozen tarn", "terrain", ice_center(1), mb="MB_ICE")
        for k, sig in ICE_SIGS.items():
            one_cv(out, f"ice_{k}", "frozen tarn", "terrain", ice_cv(sig), mb="MB_ICE")
        for part in ("l", "m", "r"):
            one_cv(out, f"ledge_{part}", "snow cornice: jump down", "terrain", ledge_cv(part), walk="J")
        one_cv(out, "exit_s", "the road down (a south arrow warp)", "terrain", path_cv(0, 0, 1, 1), walk="v")
        for v in range(3):
            one_cv(out, f"ag{v}", "alpine grass through the snow", "terrain", alpine_cv(v), mb="MB_SAND")
    return out


COMMON = set()


def props(which="oros"):
    out = []
    g0 = ground_cv("g0")
    common = which in ("oros", "propylon")
    if which == "oros":
        pine = fir(32, 48, [(2, 11, 5), (9, 12, 9), (17, 13, 12), (26, 13, 15)], 6)
        grid_to(pine, out, "fir", "a snow-laden fir", "props", 2, 3, ["TT", "XX", "XX"], floor=g0, top_rows=1)
        pine2 = fir(32, 48, [(4, 10, 4), (10, 11, 8), (18, 12, 11), (27, 12, 13)], 6, lean=1)
        grid_to(pine2, out, "fir_b", "a wind-bent fir", "props", 2, 3, ["TT", "XX", "XX"], floor=g0, top_rows=1)
        arrow = fir(32, 48, [(2, 11, 5), (9, 12, 9), (17, 13, 12), (26, 13, 15)], 6, arrow=True)
        grid_to(arrow, out, "fir_arrow", "a fir with a silver arrow in it (Artemis)", "props", 2, 3,
                ["TT", "XX", "XX"], floor=g0, top_rows=1)
        small = fir(16, 32, [(1, 8, 3), (6, 9, 5), (12, 10, 7), (19, 8, 7)], 4)
        grid_to(small, out, "fir_s", "a young fir", "props", 1, 2, ["T", "X"], floor=g0, top_rows=1)
    grid_to(rock_cv(16, 16, 1), out, "rock", "a rock through the snow", "props", 1, 1, ["X"], floor=g0)
    grid_to(rock_cv(16, 16, 5), out, "rock_b", "a rock through the snow", "props", 1, 1, ["X"], floor=ground_cv("g1"))
    if which == "oros":
        grid_to(rock_cv(32, 32, 3), out, "boulder", "a snow-capped boulder", "props", 2, 2, ["XX", "XX"], floor=g0)
        grid_to(drift_cv(32, 16), out, "drift", "a snowdrift", "props", 2, 1, ["XX"], floor=g0)
    if which == "oros":
        wine = drift_cv(32, 16, wine=True)
        grid_to(flatten(wine, g0).recolor({}), out, "drift_wine", "a drift stained purple (Dionysus)", "props", 2, 1,
                ["XX"])
        ice = ice_center(0)
        blue = {"rk1": "ic0", "rk2": "ic1", "rk3": "ic2", "rk4": "ic3", "rk5": "sn5"}
        grid_to(flatten(rock_cv(16, 16, 7).recolor(blue), ice), out, "ice_rock", "an ice boulder in the tarn",
                "props", 1, 1, ["X"])
        grid_to(flatten(rock_cv(16, 16, 2).recolor(blue), ice_center(1)), out, "ice_rock_b",
                "an ice boulder in the tarn", "props", 1, 1, ["X"])
    grid_to(plate_cv(False), out, "plate", "a bronze plate", "props", 1, 1, ["."])
    grid_to(plate_cv(True), out, "plate_down", "a pressed plate", "props", 1, 1, ["."])
    grid_to(grate_cv(False), out, "grate", "a bronze bar over a stair", "props", 1, 1, ["X"])
    grid_to(grate_cv(True), out, "grate_up", "the stair, the bar lifted", "props", 1, 1, ["."])
    grid_to(stele_cv(), out, "stele", "a stele with an inscription", "props", 1, 2, ["X", "X"], floor=g0)
    grid_to(herm_cv(), out, "herm", "a herm (the travel herm)", "props", 1, 1, ["X"], floor=plain_snow())
    grid_to(signpost_cv(), out, "sign", "a signpost", "props", 1, 1, ["X"], floor=g0)
    if which == "oros":
        grid_to(lever_cv(), out, "lever", "the seal's reset lever", "props", 1, 1, ["X"])
        grid_to(mouth_cv(), out, "mouth", "a cave mouth in the cliff", "props", 2, 2, ["XX", ".."],
                behaviors={(0, 1): "MB_NON_ANIMATED_DOOR", (1, 1): "MB_NON_ANIMATED_DOOR"})
        grid_to(mouth_cv(roped=True), out, "mouth_roped", "a roped-off cave (closed by the Archon)", "props", 2, 2,
                ["XX", "XX"])
        grid_to(bronze_door_cv(), out, "bronze_door", "a bronze door with the Twelve's marks", "props", 2, 2,
                ["XX", "XX"])
        grid_to(giant_cv(), out, "giant", "a Giant frozen in the ice", "props", 3, 3, ["XXX", "XXX", "XXX"], floor=g0)
        grid_to(giant_cv().hflip(), out, "giant_r", "a Giant frozen in the ice", "props", 3, 3,
                ["XXX", "XXX", "XXX"], floor=g0)
        grid_to(frozen_fall_cv(), out, "frozen_fall", "a frozen waterfall", "props", 2, 4, ["XX", "XX", "XX", "XX"])
        grid_to(handholds_cv(), out, "handholds", "handholds cut too far apart", "props", 1, 2, ["X", "X"])
        grid_to(crevasse_cv(), out, "crevasse", "a crevasse", "props", 2, 1, ["XX"])
        grid_to(shield_cv(), out, "shield", "a broken shield half-buried (Ares)", "props", 1, 1, ["X"])
        grid_to(poppy_cv(), out, "poppy", "a poppy in the snow (Demeter)", "props", 1, 1, ["."])
        grid_to(trident_rock_cv(), out, "trident_rock", "a rock split by three prongs (Poseidon)", "props", 1, 1,
                ["X"], floor=g0)
        grid_to(lyre_rock_cv(), out, "lyre_rock", "a split rock that hums (Apollo)", "props", 1, 1, ["X"], floor=g0)
        for v in (0, 1):
            one_cv(out, f"cloud_bridge_{v}", "a span of cloud (it won't hold yet)", "props", cloud_bridge_cv(v),
                   walk="X")
        pk = far_peak_cv(64, 48)
        grid_to(pk, out, "far_peak", "the summit cone of Olympus, far off", "props", 4, 3, ["XXXX"] * 3)
    else:
        grid_to(tripod_cv(True), out, "tripod", "a bronze tripod, lit (an Archon's offering)", "props", 1, 2,
                ["X", "X"], floor=plain_snow())
        grid_to(kit_free_column(3), out, "kcol", "an Ionic column (the shared kit) by the processional way", "props",
                1, 3, ["T", "T", "X"], floor=plain_snow(), top_rows=2)
        grid_to(brazier_cv(), out, "brazier", "a great brazier, lit", "props", 1, 2, ["X", "X"], floor=plain_snow())
        grid_to(basin_cv(), out, "basin", "the lustral basin, frozen", "props", 2, 1, ["XX"])
    return out


def facade():
    out = [facade_struct()]
    for god in ["champion"]:          # the Twelve themselves are objects now (tools/ichor/art/statues.py)
        champ = god == "champion"
        grid_to(statue_big(god), out, f"statue_{god}", f"the statue of {god.title()}", "facade", 1, 3,
                [".", "X", "X"] if champ else ["T", "X", "X"], floor=plain_snow(), top_rows=0 if champ else 1)
    return out


def sections(which="oros"):
    if which == "propylon":
        return [("terrain", terrain("propylon")), ("props", props("propylon")), ("facade", facade())]
    return [("terrain", terrain()), ("props", props())]
