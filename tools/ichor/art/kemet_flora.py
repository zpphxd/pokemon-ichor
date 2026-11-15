"""Kemet's trees: the date palm (with grass, sand and mud under it), a young palm,
and the sacred sycomore fig. Aethos's olives and cypresses stay Greek; these are
the trees a Greek trader noticed first in Egypt.
"""
from __future__ import annotations

import copy
import math

import numpy as np

import kemet_lib as L
from kemet_lib import Layer, Struct, finish


def frond(Ly, cx, cy, ang, length, droop, lit=True):
    """One palm frond from (cx, cy): a rib curving down under its own weight, with
    pinnae hanging from it on both sides."""
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    pts = []
    for i in range(length + 1):
        t = i / length
        x = cx + dx * i
        y = cy + dy * i + droop * t * t * length
        pts.append((round(x), round(y)))
    # pinnae: short strokes hanging below and beside the rib, longer mid-frond
    for i, (x, y) in enumerate(pts[2:], 2):
        t = i / length
        span = 3 if 0.25 < t < 0.8 else 2 if t <= 0.9 else 1
        for k in range(1, span + 1):
            Ly.px(x, y + k, "pg1" if k == span else "pg2")
            if i % 2 == 0:
                Ly.px(x + (1 if dx > 0 else -1), y + k, "pg1")
        if t < 0.85:
            Ly.px(x, y - 1, "pg2")
    for i, (x, y) in enumerate(pts):
        t = i / length
        Ly.px(x, y, "pg4" if (lit and t < 0.6) else "pg3")
    return pts


def palm_art(w=2, h=3, crown_cy=11, trunk_top=13, scale=1.0, dates=True):
    """Layers for a date palm: crown on `top`, trunk on `mid` (the caller splits by row)."""
    W, H = w * 16, h * 16
    crown = Layer(W, H)
    trunk = Layer(W, H)
    cx = W // 2
    # trunk: leaf-base scales in a diamond pattern, lit on the left, a slight curve
    for y in range(trunk_top, H - 1):
        t = (y - trunk_top) / max(1, H - 1 - trunk_top)
        xm = cx - 1 + round(1.5 * math.sin(t * 2.2))
        half = 2 if t < 0.85 else 3
        for x in range(xm - half, xm + half + 1):
            if x == xm - half or x == xm + half:
                c = "ink"
            elif (y + (x - xm)) % 4 == 0 or (y - (x - xm)) % 4 == 0:
                c = "tr0"
            elif x < xm:
                c = "tr2"
            else:
                c = "tr1"
            trunk.px(x, y, c)
    for x in range(cx - 4, cx + 3):
        trunk.px(x, H - 1, "ink" if x in (cx - 4, cx + 2) else "tr0")
    # dates hang under the crown
    if dates:
        for (x, y) in ((cx - 4, crown_cy + 4), (cx + 2, crown_cy + 5)):
            crown.blit([" dd ", "dDdd", "dddD", " dd "], {"d": "dt", "D": "dt2"}, x, y)
    # fronds, back to front: the back ones darker
    k = scale
    back = [(-150, 13, 0.55), (-115, 11, 0.6), (-65, 11, 0.6), (-30, 13, 0.55)]
    front = [(-175, 15, 0.45), (-5, 15, 0.45), (160, 12, 0.35), (20, 12, 0.35),
             (-90, 9, 0.9), (130, 10, 0.3), (50, 10, 0.3)]
    for ang, ln, dr in back:
        frond(crown, cx, crown_cy, ang, round(ln * k), dr, lit=False)
    for ang, ln, dr in front:
        frond(crown, cx, crown_cy, ang, round(ln * k), dr, lit=True)
    crown.blit([" ab ", "abba", " ba "], {"a": "pg3", "b": "tr1"}, cx - 2, crown_cy - 1)
    # an ink outline round the crown's silhouette
    a = crown.a[..., 3] > 0
    pad = np.pad(a, 1)
    ring = ~a & (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
    ys, xs = np.nonzero(ring)
    for y, x in zip(ys, xs):
        if y < (crown_cy + 10):
            crown.px(x, y, "ink")
    return crown, trunk


def date_palm(ground, key, title):
    s = Struct(key, title, 2, 3, walk=["TT", "XX", "XX"], ground=ground,
               notes="A date palm, 2x3: its crown's top row is drawn over the player, who "
                     "walks behind it. Dates hang under the fronds.")
    crown, trunk = palm_art()
    # rows 0-1: crown and the trunk under it, all on the top layer; row 2 the
    # trunk's foot on the middle layer
    for y in range(32):
        for x in range(32):
            for src in (trunk, crown):
                if src.a[y, x, 3]:
                    s.T.a[y, x] = src.a[y, x]
    for y in range(32, 48):
        for x in range(32):
            for src in (trunk, crown):
                if src.a[y, x, 3]:
                    s.M.a[y, x] = src.a[y, x]
    # a little shade at the foot
    for x in range(9, 22):
        if not s.M.a[46, x, 3] and x % 2 == 0:
            s.M.px(x, 46, "pg0" if ground != "mud" else "md0")
    return finish(s)


def young_palm(ground, key, title):
    s = Struct(key, title, 1, 2, walk=["T", "X"], ground=ground,
               notes="A young date palm, 1x2: crown over the player, trunk solid.")
    W, H = 16, 32
    crown = Layer(W, H)
    cx, cy = 8, 9
    for ang, ln, dr in ((-160, 7, 0.6), (-20, 7, 0.6), (-100, 6, 0.8), (-60, 6, 0.8),
                        (170, 6, 0.5), (10, 6, 0.5)):
        frond(crown, cx, cy, ang, ln, dr)
    a = crown.a[..., 3] > 0
    pad = np.pad(a, 1)
    ring = ~a & (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(ring)):
        crown.px(x, y, "ink")
    for y in range(cy + 2, H - 1):
        for x in range(cx - 2, cx + 2):
            c = "ink" if x in (cx - 2, cx + 1) else ("tr2" if x == cx - 1 else "tr1")
            if (y % 3 == 0) and x not in (cx - 2, cx + 1):
                c = "tr0"
            (s.T if y < 16 else s.M).px(x, y, c)
    for y in range(16):
        for x in range(16):
            if crown.a[y, x, 3]:
                s.T.a[y, x] = crown.a[y, x]
    for y in range(16, 32):
        for x in range(16):
            if crown.a[y, x, 3] and not s.M.a[y, x, 3]:
                pass
    s.M.hline(cx - 3, cx + 2, 31, "tr0")
    return finish(s)


def sycomore(ground="grass"):
    s = Struct("sycomore", "Sycomore fig", 2, 2, walk=["XX", "XX"], ground=ground,
               notes="The sycomore fig, Hathor's tree, 2x2: a broad dark canopy with figs "
                     "on the trunk. Solid, like aethos's olive.")
    cnv = Layer(32, 32)
    # canopy: overlapping lobes, dark below and lit at the top left
    lobes = [(9, 9, 8, 6), (22, 8, 8, 6), (15, 5, 9, 5), (6, 15, 6, 5), (25, 15, 6, 5),
             (16, 13, 10, 6)]
    for (x, y, rx, ry) in lobes:
        cnv.ellipse(x - rx, y - ry, x + rx, y + ry, "pg1")
    for (x, y, rx, ry) in lobes:
        cnv.ellipse(x - rx + 1, y - ry, x + rx - 3, y + ry - 3, "pg2")
    for (x, y, rx, ry) in lobes[:3]:
        cnv.ellipse(x - rx + 3, y - ry + 1, x + 1, y - 1, "pg3")
    for yy in range(32):
        for xx in range(32):
            if cnv.get(xx, yy) == "pg2" and L._h(xx, yy, 5) < 40:
                cnv.px(xx, yy, "pg1")
            if cnv.get(xx, yy) == "pg3" and L._h(xx, yy, 6) < 30:
                cnv.px(xx, yy, "pg4")
    a = cnv.a[..., 3] > 0
    pad = np.pad(a, 1)
    ring = ~a & (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(ring)):
        cnv.px(x, y, "ink")
    # trunk and figs
    trunk = ["k1122k", "k1122k", "k12221k", "kk1221kk", "k112221k"]
    for j, row in enumerate(trunk):
        cnv.blit([row], {"k": "ink", "1": "tr2", "2": "tr1"}, 13 - (len(row) - 6) // 2, 21 + j * 2)
        cnv.blit([row], {"k": "ink", "1": "tr2", "2": "tr1"}, 13 - (len(row) - 6) // 2, 22 + j * 2)
    for (x, y) in ((14, 23), (17, 25), (15, 27)):
        cnv.px(x, y, "dt2")
    for y in range(16):
        for x in range(32):
            if cnv.a[y, x, 3]:
                s.T.a[y, x] = cnv.a[y, x]
    for y in range(16, 32):
        for x in range(32):
            if cnv.a[y, x, 3]:
                s.M.a[y, x] = cnv.a[y, x]
    return finish(s)


def build():
    out = [date_palm("grass", "palm", "Date palm"),
           date_palm("sand", "palm_sand", "Date palm on sand"),
           date_palm("mud", "palm_mud", "Date palm on mud"),
           young_palm("grass", "palm_young", "Young date palm"),
           young_palm("sand", "palm_young_sand", "Young date palm on sand")]
    return out
