"""Sprite toolkit for the Aethos dex.

Every species is drawn in code, once per *view*, on a 64x64 design canvas,
with the parts renderer from tools/ichor/art/sprites_lib.py (auto outline,
interior lines, top-left light). A Pen maps design coordinates onto the
target canvas, so the same drawing renders at battle size, icon size and
follower size, and the outline stays 1 px at every size.

Views a species draws (see SPRITES.md for the house style):
    front   battle front, 3/4 view facing left; phase 0/1 are the two
            anim_front frames
    back    battle back, seen from behind, facing right
    down    follower facing the camera; phase 0/1 are the two walk frames
    up      follower seen from behind (optional: falls back to back)
    side    follower facing left (optional: falls back to front)
    icon    party icon (optional: falls back to front)

The build (build.py) writes each species in the expansion's own layout under
design/dex/sprites/<name>/, ready to copy into graphics/pokemon/<name>/.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "ichor", "art"))
from sprites_lib import Palette, Mat, Fig, DEFAULT_CUTS, bresenham  # noqa: E402,F401
from scipy import ndimage  # noqa: E402

SS = 4  # supersampling for shape coverage


# --------------------------------------------------------------------------
# Colors. The master families from design/phase1/PLAN.md come first; the
# extended families give the dex the range 18 types need. Any RGB whose
# channels are multiples of 8 is legal, so these are a starting point.
# --------------------------------------------------------------------------

class C:
    ink = (32, 24, 24)
    white = (248, 248, 240)
    # master palette
    aegean = [(24, 56, 120), (48, 104, 176), (112, 168, 224), (176, 216, 240)]
    marble = [(168, 160, 152), (216, 208, 192), (248, 248, 240)]
    olive = [(56, 72, 32), (96, 112, 48), (144, 160, 72), (168, 184, 136)]
    cypress = [(24, 56, 40), (40, 88, 56)]
    terracotta = [(120, 48, 24), (184, 88, 48), (224, 136, 88)]
    sungold = [(200, 144, 40), (240, 192, 64)]
    limestone = [(176, 144, 96), (208, 184, 136), (232, 216, 176)]
    # extended
    ember = [(152, 32, 32), (216, 64, 48), (248, 120, 72)]
    flame = [(200, 80, 24), (240, 144, 40), (248, 208, 88), (248, 240, 176)]
    wine = [(72, 32, 80), (120, 64, 136), (168, 112, 184), (208, 168, 224)]
    rose = [(176, 72, 104), (224, 128, 152), (248, 192, 200)]
    bronze = [(104, 64, 32), (160, 104, 48), (208, 160, 80), (240, 208, 128)]
    ash = [(64, 64, 72), (104, 104, 112), (152, 152, 160), (200, 200, 208)]
    night = [(40, 32, 64), (72, 64, 112), (112, 104, 160)]
    seagreen = [(32, 96, 88), (64, 152, 128), (128, 200, 168)]
    ice = [(120, 168, 200), (184, 224, 240), (232, 248, 248)]
    bark = [(72, 48, 32), (112, 80, 48), (152, 112, 72)]
    ghost = [(80, 96, 160), (136, 168, 216), (200, 224, 248)]


# --------------------------------------------------------------------------
# Volume shading. The trainer renderer shades each part by where a pixel sits
# in its row and column; creatures need round forms. MonFig treats every
# shading group as a dome raised from its silhouette (a distance transform),
# lights it from the upper left and front, and darkens it a little toward
# its base. Outlines, interior lines, cast shadow, quantizing and details are
# the same as Fig's.
# --------------------------------------------------------------------------

LIGHT = np.array([-0.6, -0.8, 0.62])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


class MonFig(Fig):
    def __init__(self, pal, w=64, h=64, light=None):
        super().__init__(pal, w, h)
        self.light = LIGHT if light is None else np.asarray(light, float) / np.linalg.norm(light)

    def _shading(self, gmap, zmap):
        h, w = self.h, self.w
        pid = self.pid
        s = np.zeros((h, w), float)
        for g in np.unique(gmap[pid > 0]):
            gm = (gmap == g) & (pid > 0)
            members = [p for p in self.parts[1:] if p.group == g]
            base = members[0]
            d = ndimage.distance_transform_edt(np.pad(gm, 1))[1:-1, 1:-1]
            D = max(d.max(), 1.0)
            hgt = np.sqrt(np.clip(d * (2 * D - d), 0, None))
            hgt = ndimage.gaussian_filter(hgt, 0.9) * gm
            gy, gx = np.gradient(hgt)
            n = np.stack([-gx, -gy, np.full_like(gx, 0.9)])
            n /= np.linalg.norm(n, axis=0)
            dot = n[0] * self.light[0] + n[1] * self.light[1] + n[2] * self.light[2]
            raw = np.clip((1 - dot) / 1.25, 0, 1)
            ys = np.nonzero(gm)[0]
            y0, y1 = ys.min(), ys.max()
            v = (np.arange(h)[:, None] - y0) / max(y1 - y0, 1)
            wy = base.wy if base.wy is not None else 0.22
            val = (1 - wy) * raw + wy * v
            s[gm] = val[gm]
            for p in members:
                s[pid == p.pid] += p.bias
        return s

    def render(self):
        h, w = self.h, self.w
        pid = self.pid
        out = np.zeros((h, w), np.int32)
        zmap = np.full((h, w), -10 ** 9)
        gmap = np.zeros((h, w), np.int32)
        for p in self.parts[1:]:
            m = pid == p.pid
            zmap[m] = p.z
            gmap[m] = p.group

        s = self._shading(gmap, zmap)

        # cast shadow from parts drawn over this one, above or to the left
        occ = pid > 0
        for dx, dy, wgt in ((0, -1, 0.28), (-1, -1, 0.14), (0, -2, 0.14), (-1, 0, 0.1), (-1, -2, 0.07)):
            zs = np.full((h, w), -10 ** 9)
            gs = np.zeros((h, w), np.int32)
            ys0, ys1 = max(0, dy), h + min(0, dy)
            xs0, xs1 = max(0, dx), w + min(0, dx)
            zs[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx] = np.where(occ, zmap, -10 ** 9)[ys0:ys1, xs0:xs1]
            gs[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx] = gmap[ys0:ys1, xs0:xs1]
            # zs[y, x] holds zmap[y + dy, x + dx]
            hit = occ & (zs > zmap) & (gs != gmap)
            s[hit] += wgt
        s += self.shade_adj

        lvl = np.zeros((h, w), np.int32)
        for p in self.parts[1:]:
            m = pid == p.pid
            if not m.any():
                continue
            n = len(p.mat.ramp)
            if p.flat is not None:
                lvl[m] = p.flat
                continue
            cuts = p.mat.cuts or DEFAULT_CUTS[n]
            idx = np.searchsorted(np.array(cuts), s[m], side="right")
            lvl[m] = np.clip((n - 1) - idx, 0, n - 1)

        # despeckle: a lone pixel takes its neighbors' level
        for y in range(h):
            for x in range(w):
                if not pid[y, x]:
                    continue
                nb = []
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < w and 0 <= yy < h and gmap[yy, xx] == gmap[y, x] and pid[yy, xx]:
                        nb.append(lvl[yy, xx])
                if len(nb) >= 3 and lvl[y, x] not in nb:
                    vals, counts = np.unique(nb, return_counts=True)
                    lvl[y, x] = vals[np.argmax(counts)]

        for p in self.parts[1:]:
            m = pid == p.pid
            for i, name in enumerate(p.mat.ramp):
                out[m & (lvl == i)] = self.pal[name]

        line = out.copy()
        for y in range(h):
            for x in range(w):
                p = pid[y, x]
                if not p:
                    continue
                part = self.parts[p]
                edge_out = edge_in = False
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if yy >= h:
                        continue  # a body cropped by the bottom of the frame has no outline there
                    if not (0 <= xx < w and 0 <= yy < h) or pid[yy, xx] == 0:
                        edge_out = True
                    elif gmap[yy, xx] != gmap[y, x] and zmap[yy, xx] < zmap[y, x]:
                        edge_in = True
                if edge_out and not part.nooutline:
                    line[y, x] = self.pal[part.mat.outline]
                elif edge_in and not part.noline:
                    line[y, x] = self.pal[part.mat.line]
        out = line

        for op in self.post:
            if op[0] == "px":
                _, x, y, c = op
                if 0 <= x < w and 0 <= y < h:
                    out[y, x] = 0 if c == "_" else self.pal[c]
            elif op[0] == "line":
                _, pts, c = op
                for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                    for x, y in bresenham(x0, y0, x1, y1):
                        if 0 <= x < w and 0 <= y < h:
                            out[y, x] = self.pal[c]
            elif op[0] == "patch":
                _, x0, y0, rows, legend = op
                for j, row in enumerate(rows):
                    for i, ch in enumerate(row):
                        if ch in ". ":
                            continue
                        x, y = x0 + i, y0 + j
                        if 0 <= x < w and 0 <= y < h:
                            c = legend[ch]
                            out[y, x] = 0 if c == "_" else self.pal[c]
        return out


# --------------------------------------------------------------------------
# Geometry helpers. All work in design coordinates (floats, 64x64 canvas,
# pixel i covers [i, i+1)).
# --------------------------------------------------------------------------

def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def bez(p0, p1, p2, n=12):
    """Quadratic Bezier through p0 and p2, pulled toward p1."""
    out = []
    for i in range(n + 1):
        t = i / n
        a, b = (1 - t) ** 2, 2 * (1 - t) * t
        out.append((a * p0[0] + b * p1[0] + t * t * p2[0], a * p0[1] + b * p1[1] + t * t * p2[1]))
    return out


def bez3(p0, p1, p2, p3, n=16):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def ellipse_pts(cx, cy, rx, ry, ang=0.0, n=None):
    n = n or max(16, int((rx + ry) * 2.2))
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def _normals(path):
    out = []
    for i in range(len(path)):
        a = path[max(i - 1, 0)]
        b = path[min(i + 1, len(path) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1.0
        out.append((-dy / d, dx / d))
    return out


def _lengths(path):
    acc = [0.0]
    for a, b in zip(path, path[1:]):
        acc.append(acc[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    total = acc[-1] or 1.0
    return [v / total for v in acc]


def ribbon(path, widths):
    """Polygon around a polyline; widths(t) gives the full width at t in 0..1."""
    nm = _normals(path)
    ts = _lengths(path)
    left, right = [], []
    for (x, y), (nx, ny), t in zip(path, nm, ts):
        h = widths(t) / 2
        left.append((x + nx * h, y + ny * h))
        right.append((x - nx * h, y - ny * h))
    return left + right[::-1]


def lens_pts(a, b, w, bend=0.0, n=14, fat=0.5):
    """A leaf / petal / flame shape pointed at both ends, from a to b.
    w is the widest full width; bend bows the midline sideways (design px,
    positive bows to the left of a->b); fat moves the widest point toward
    b (0.5 is centered)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / d, dx / d
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        # width profile peaking at t = fat
        u = t / fat if t < fat else (1 - t) / (1 - fat)
        h = w / 2 * math.sin(math.pi / 2 * max(0.0, min(1.0, u))) ** 0.9
        off = bend * math.sin(math.pi * t)
        cx, cy = a[0] + dx * t + nx * off, a[1] + dy * t + ny * off
        left.append((cx + nx * h, cy + ny * h))
        right.append((cx - nx * h, cy - ny * h))
    return left + right[::-1]


# --------------------------------------------------------------------------
# Pen
# --------------------------------------------------------------------------

class Pen:
    """Draws on a Fig through a transform: canvas = (ox, oy) + s * design.

    Shape methods add parts (they take a Mat and the Fig.add keywords:
    group, under, clip, bias, noline, nooutline, flat, wx, wy). Detail
    methods (px, stroke, eye, patch) paint over the rendered parts.
    """

    def __init__(self, fig: Fig, s=1.0, ox=0.0, oy=0.0, view="front", phase=0):
        self.fig, self.s, self.ox, self.oy = fig, s, ox, oy
        self.view, self.phase = view, phase
        self.W, self.H = fig.w, fig.h

    # ---- transform ---------------------------------------------------------
    @property
    def big(self):
        """True at battle size; use it to skip fine detail on icons."""
        return self.s >= 0.85

    def pt(self, x, y):
        return (self.ox + x * self.s, self.oy + y * self.s)

    def ipt(self, x, y):
        X, Y = self.pt(x + 0.5, y + 0.5)
        return (int(math.floor(X)), int(math.floor(Y)))

    # ---- masks -------------------------------------------------------------
    def mask(self, *polys, thresh=0.5):
        im = Image.new("L", (self.W * SS, self.H * SS), 0)
        d = ImageDraw.Draw(im)
        for poly in polys:
            if len(poly) < 3:
                continue
            d.polygon([((self.ox + x * self.s) * SS, (self.oy + y * self.s) * SS) for x, y in poly], fill=255)
        a = np.asarray(im, np.float32).reshape(self.H, SS, self.W, SS).mean(axis=(1, 3)) / 255.0
        return a >= thresh

    def add(self, mask, mat, **kw):
        if not mask.any():
            return 0
        return self.fig.add(mask, mat, **kw)

    # ---- shapes ------------------------------------------------------------
    def poly(self, pts, mat, **kw):
        return self.add(self.mask(pts), mat, **kw)

    def polys(self, polys, mat, **kw):
        """Several polygons as one part."""
        return self.add(self.mask(*polys), mat, **kw)

    def blob(self, cx, cy, rx, ry, mat, ang=0.0, **kw):
        """An ellipse, optionally rotated by ang degrees."""
        return self.poly(ellipse_pts(cx, cy, rx, ry, ang), mat, **kw)

    def circle(self, cx, cy, r, mat, **kw):
        return self.blob(cx, cy, r, r, mat, **kw)

    def rect(self, x0, y0, x1, y1, mat, **kw):
        """Inclusive pixel rectangle in design coordinates."""
        return self.poly([(x0, y0), (x1 + 1, y0), (x1 + 1, y1 + 1), (x0, y1 + 1)], mat, **kw)

    def _minw(self, w):
        # keep limbs at least ~1 canvas px wide when drawn small
        return max(w, 1.15 / self.s)

    def limb(self, path, w0, w1=None, mat=None, cap=True, **kw):
        """A tapered limb, neck or tail along a polyline (use bez for curves).
        Widths are full widths in design px; round caps by default."""
        w1 = w0 if w1 is None else w1
        a, b = self._minw(w0), self._minw(w1)
        polys = [ribbon(path, lambda t: a + (b - a) * t)]
        if cap:
            polys.append(ellipse_pts(path[0][0], path[0][1], a / 2, a / 2, n=12))
            polys.append(ellipse_pts(path[-1][0], path[-1][1], b / 2, b / 2, n=12))
        return self.add(self.mask(*polys), mat, **kw)

    def taper(self, path, w, mat, **kw):
        """A limb tapering from width w to a point (horns, claws, tail tips)."""
        a = self._minw(w)
        return self.add(self.mask(ribbon(path, lambda t: a * (1 - t) + 0.3 * t),
                                  ellipse_pts(path[0][0], path[0][1], a / 2, a / 2, n=12)), mat, **kw)

    def lens(self, a, b, w, mat, bend=0.0, fat=0.5, **kw):
        """A leaf, petal, feather, fin or flame tongue from a to b."""
        return self.poly(lens_pts(a, b, self._minw(w), bend, fat=fat), mat, **kw)

    def drop(self, tip, cx, cy, r, mat, **kw):
        """A teardrop: round end at (cx, cy) of radius r, point at tip."""
        dx, dy = tip[0] - cx, tip[1] - cy
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        tri = [tip, (cx + nx * r, cy + ny * r), (cx - nx * r, cy - ny * r)]
        return self.add(self.mask(tri, ellipse_pts(cx, cy, r, r)), mat, **kw)

    def erase(self, pts):
        """Cut a hole (negative space between legs, under a raised paw)."""
        self.fig.add(self.mask(pts), None, erase=True)

    def shade(self, pts, delta):
        """Darken (+) or lighten (-) the shading inside a polygon."""
        m = self.mask(pts)
        self.fig.shade_adj[m] += delta

    # ---- details (painted after render) ---------------------------------------
    def px(self, x, y, color):
        X, Y = self.ipt(x, y)
        self.fig.px(X, Y, color)

    def pxs(self, pts, color):
        for x, y in pts:
            self.px(x, y, color)

    def stroke(self, pts, color):
        """A 1 px line in a palette color (mouths, veins, cracks)."""
        ipts = [self.ipt(x, y) for x, y in pts]
        if len(ipts) == 1:
            ipts = ipts * 2
        self.fig.line(ipts, color)

    def patch(self, x, y, rows, legend=None, small=None):
        """A hand-placed ASCII patch at battle size: '.' or ' ' leaves a pixel,
        '_' clears it. With no legend, characters are palette indices in hex
        ('1'-'9', 'a'-'f'), the same characters build.py --dump prints, so a
        dumped region can be edited and pasted back. At small sizes the patch
        is skipped, or `small` (x, y, rows) is used instead."""
        if legend is None:
            legend = {"_": "_"}
            for i, name in enumerate(self.fig.pal.names):
                if i:
                    legend["0123456789abcdef"[i]] = name
        if self.big:
            X, Y = self.ipt(x, y)
            self.fig.patch(X, Y, rows, legend)
        elif small:
            sx, sy, srows = small
            X, Y = self.ipt(sx, sy)
            self.fig.patch(X, Y, srows, legend)

    def eye(self, x, y, w=3, h=4, iris=None, shine="white", pupil="ink", shine_at=None):
        """A Gen 3 eye whose top-left pixel is at design (x, y): a dark w x h
        oval (corners rounded when it is at least 3x4), an optional iris
        color in the lower half and a 1 px shine, by default one in from the
        top-right corner (shine_at=(i, j) moves it). Drawn small, it is a
        1 px (or 1x2) dark mark."""
        if not self.big:
            X, Y = self.ipt(x + w / 2 - 0.5, y + h / 2 - 0.5)
            self.fig.px(X, Y, pupil)
            if self.s >= 0.55 and h >= 4:
                self.fig.px(X, Y - 1, pupil)
            return
        X0, Y0 = self.ipt(x, y)
        rounded = w >= 3 and h >= 4
        for j in range(h):
            for i in range(w):
                if rounded and i in (0, w - 1) and j in (0, h - 1):
                    continue
                c = pupil
                if iris and j >= (h + 1) // 2 and (w <= 2 or 0 < i < w - 1):
                    c = iris
                self.fig.px(X0 + i, Y0 + j, c)
        if shine:
            i, j = shine_at if shine_at else (max(0, w - 2), 1 if h >= 3 else 0)
            self.fig.px(X0 + i, Y0 + j, shine)


# --------------------------------------------------------------------------
# Species
# --------------------------------------------------------------------------

class Mon:
    """One species: its palette, shiny swap, footprint and drawing.

    colors: list of (name, rgb), at most 15; the first should be 'ink'.
    shiny:  {name: rgb} for the colors the shiny palette changes.
    draw:   function(p: Pen, view: str, phase: int).
    foot:   a FOOTPRINTS key or a list of 16 strings ('#' marks the print).
    """

    def __init__(self, name, colors, shiny, draw, foot="blank", follow=None):
        self.name = name
        self.colors = list(colors)
        self.shiny = dict(shiny)
        self.draw = draw
        self.foot = foot
        self.follow = follow  # optional follower height in px (default by size)
        unknown = set(self.shiny) - {n for n, _ in self.colors}
        if unknown:
            raise ValueError(f"{name}: shiny names not in palette: {sorted(unknown)}")

    def palette(self, shiny=False):
        named = [(n, self.shiny.get(n, c) if shiny else c) for n, c in self.colors]
        return Palette(named)


# --------------------------------------------------------------------------
# Footprints: 16x16, 1 bit. '#' is the print.
# --------------------------------------------------------------------------

def _fp(rows):
    rows = [r.ljust(16, ".") for r in rows]
    return rows + ["." * 16] * (16 - len(rows))


FOOTPRINTS = {
    "blank": _fp([]),
    "hoof": _fp([
        "", "", "", "",
        ".....##..##.....",
        "....###..###....",
        "....###..###....",
        "....###..###....",
        "....###..###....",
        ".....##..##.....",
        "......#..#......",
    ]),
    "paw": _fp([
        "", "", "",
        ".....#...#......",
        "....##...##.....",
        "..#.........#...",
        "..##.......##...",
        "......###.......",
        ".....#####......",
        "....#######.....",
        "....#######.....",
        ".....#####......",
    ]),
    "bigpaw": _fp([
        "", "",
        "....##...##.....",
        "...###...###....",
        ".##.........##..",
        ".###.......###..",
        ".....#####......",
        "....#######.....",
        "...#########....",
        "...#########....",
        "...#########....",
        "....#######.....",
    ]),
    "claw": _fp([
        "", "",
        "...#...#...#....",
        "...#...#...#....",
        "...##..#..##....",
        "....#.###.#.....",
        ".....#####......",
        ".....#####......",
        "......###.......",
    ]),
    "bird": _fp([
        "", "", "",
        "..#.....#.....#.",
        "...#....#....#..",
        "....#...#...#...",
        ".....#..#..#....",
        "......#.#.#.....",
        ".......###......",
        "........#.......",
        "........#.......",
        "........#.......",
    ]),
    "webbed": _fp([
        "", "", "",
        "...#...#...#....",
        "...##..#..##....",
        "...#########....",
        "....#######.....",
        ".....#####......",
        "......###.......",
    ]),
    "hand": _fp([
        "", "",
        "....#.#.#.......",
        "....#.#.#.......",
        "..#.#####.......",
        "...#######......",
        "...#######......",
        "....#####.......",
        "....#####.......",
    ]),
    "fin": _fp([
        "", "", "", "",
        "......#.........",
        ".....###........",
        "....#####.......",
        "...#######......",
        "....#####.......",
        "......#.###.....",
        ".........##.....",
    ]),
    "root": _fp([
        "", "", "",
        "......##........",
        "......##........",
        ".....####.......",
        "....##..##......",
        "...##....##.....",
        "..#..#..#..#....",
    ]),
    "coil": _fp([
        "", "", "",
        ".....######.....",
        "....#......#....",
        "...#..####..#...",
        "...#.#....#.#...",
        "...#.#..#.#.#...",
        "...#..##..#.....",
        "....#....#......",
        ".....####.......",
    ]),
}
