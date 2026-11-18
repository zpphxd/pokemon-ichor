#!/usr/bin/env python3
"""Pieces for Delphoi's interiors: limen_art.py's whole kit (oikia's palettes,
furniture and walls), ergasteria's treasury pieces (the shield and spear, the
chest, the votive shelf, the coin table), and Delphoi's own: the melissai's
wall of hive-jars, clay votive limbs on pegs, kitharas and a lyre on stands,
lead question-strips on nails, the Lesche's two great paintings, a painted
frieze of gods and giants, a little gilded tripod and a potted laurel.

Built into gTileset_OikiaDelphoi by tools/ichor/maps/delphoi_rooms.py.
"""
import math

import numpy as np

import ergasteria_art as EA
import limen_art as LA

PALETTES = LA.PALETTES
PALETTE_ORDER = LA.PALETTE_ORDER
FLOORS = LA.FLOORS
WALLS = LA.WALLS
VOID = LA.VOID
RUGS = LA.RUGS
STAMPS = dict(LA.STAMPS)
for _k in ("shield_spear", "votive_shelf", "turtle_chest", "brazier_small", "workbench"):
    STAMPS[_k] = dict(EA.STAMPS[_k], source="ergasteria")
for _k, _v in LA.__dict__.items():
    if _k.isupper() and _k not in globals():
        globals()[_k] = _v


class Art:
    def __init__(self, pal, w, h):
        self.pal, self.c = pal, PALETTES[pal]
        self.a = np.zeros((h * 16, w * 16, 4), np.uint8)

    def px(self, x, y, ch):
        if 0 <= y < self.a.shape[0] and 0 <= x < self.a.shape[1]:
            self.a[y, x, :3] = self.c[ch]
            self.a[y, x, 3] = 255

    def rect(self, x, y, w, h, ch):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, ch)

    def hline(self, x0, x1, y, ch):
        self.rect(x0, y, x1 - x0 + 1, 1, ch)

    def vline(self, x, y0, y1, ch):
        self.rect(x, y0, 1, y1 - y0 + 1, ch)

    def ellipse(self, x0, y0, x1, y1, ch):
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 0.5, (y1 - y0) / 2 + 0.5
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    self.px(x, y, ch)


def stamp(name, art, w, h, walk=(), note=""):
    STAMPS[name] = {"pal": art.pal, "img": art.a, "top": None, "w": w, "h": h, "walk": set(walk),
                    "behavior": {}, "flatten": False, "note": note, "source": "delphoi"}


def _hive_wall():
    a = Art("clay", 2, 2)
    a.rect(0, 0, 32, 32, "t")
    for row in range(4):
        for col in range(4):
            x = col * 8 + (4 if row % 2 else 0) - 2
            y = row * 8 + 1
            a.ellipse(x, y, x + 7, y + 6, "m")
            a.ellipse(x + 1, y + 1, x + 5, y + 4, "l")
            a.ellipse(x + 3, y + 2, x + 4, y + 4, "k")
    for (x, y) in ((6, 4), (21, 12), (14, 27), (27, 20), (9, 18)):
        a.px(x, y, "n")
        a.px(x + 1, y, "k")
    stamp("hive_wall", a, 2, 2, note="the melissai's wall of clay hive-jars, the bees coming and going")


def _votives():
    a = Art("clay", 2, 1)
    for x in range(1, 32, 6):
        a.px(x + 2, 1, "k")
        a.vline(x + 2, 2, 3, "s")
    shapes = [((0, 4), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 9)),        # a leg
              ((0, 4), (1, 4), (2, 4), (0, 5), (1, 5), (2, 5), (1, 6)),         # an eye
              ((1, 4), (0, 5), (1, 5), (2, 5), (1, 6), (1, 7), (1, 8)),         # an arm
              ((0, 4), (1, 4), (1, 5), (2, 5), (1, 6), (0, 6)),                 # an ear
              ((1, 4), (1, 5), (0, 6), (1, 6), (2, 6), (1, 7), (1, 8), (1, 9))]
    for i, x in enumerate(range(1, 32, 6)):
        for (dx, dy) in shapes[i % len(shapes)]:
            a.px(x + 1 + dx, dy + 2, "h")
        a.px(x + 1, 6, "m")
    stamp("votives", a, 2, 1, note="clay arms, legs, eyes and ears on pegs, each a thank-you for a cure")


def _kitharas():
    a = Art("wood", 2, 2)
    a.hline(0, 31, 6, "d")
    a.hline(0, 31, 7, "m")
    for i, (x, h) in enumerate(((2, 12), (11, 17), (21, 22))):
        top = 30 - h
        a.vline(x, top, 29, "m")
        a.vline(x + 7, top, 29, "m")
        a.hline(x, x + 7, top, "b")
        a.rect(x, 26, 8, 4, "l")
        a.hline(x, x + 7, 30, "k")
        for sx in range(x + 2, x + 7, 2):
            a.vline(sx, top + 1, 25, "c")
    stamp("kitharas", a, 2, 2, note="kitharas on pegs, from small to enormous")


def _lead_strips():
    a = Art("bronze", 2, 1)
    for i, x in enumerate(range(1, 32, 4)):
        y = 2 + (i % 2) * 5
        a.px(x + 1, y, "k")
        a.rect(x, y + 1, 3, 4, "n" if i % 3 else "m")
        a.px(x + 1, y + 2, "k")
    stamp("lead_strips", a, 2, 1, note="folded lead strips on nails: questions for the god")


def _painting(name, scene):
    a = Art("cloth", 2, 1)
    a.rect(0, 1, 32, 13, "C" if scene == "city" else "n")
    a.hline(0, 31, 0, "k")
    a.hline(0, 31, 14, "k")
    if scene == "city":
        for x in range(2, 30, 5):
            a.rect(x, 5, 3, 7, "o")
            a.rect(x, 4, 3, 1, "R")
        for (x, y) in ((6, 9), (15, 8), (24, 10)):
            a.px(x, y, "r")
            a.px(x, y + 1, "k")
        a.rect(12, 2, 8, 2, "R")
    else:
        a.rect(0, 9, 32, 5, "i")
        for x in range(3, 30, 6):
            a.vline(x, 5, 9, "c")
            a.px(x, 4, "y")
        a.rect(20, 7, 6, 2, "n")
        a.px(27, 6, "c")
    stamp(name, a, 2, 1, note="a great wall painting by a painter long dead")


def _frieze():
    a = Art("cloth", 2, 1)
    a.rect(0, 2, 32, 11, "u")
    a.hline(0, 31, 1, "o")
    a.hline(0, 31, 13, "o")
    for i, x in enumerate(range(1, 32, 5)):
        c = "y" if i % 2 else "r"
        a.vline(x + 1, 5, 11, c)
        a.px(x + 1, 4, "C")
        a.px(x + 2 if i % 2 else x, 7, c)
    stamp("frieze", a, 2, 1, note="gods against giants, painted bright; gold leaf scraped off in places")


def _tripod_small():
    a = Art("bronze", 1, 2)
    for lx in (3, 8, 12):
        for y in range(16, 31):
            x = 8 + (lx - 8) * (y - 16) / 15
            a.px(int(round(x)), y, "z" if lx != 8 else "b")
    a.ellipse(2, 9, 13, 16, "k")
    a.ellipse(3, 10, 12, 15, "y")
    a.ellipse(4, 10, 11, 12, "b")
    a.ellipse(4, 4, 7, 9, "y")
    a.ellipse(8, 4, 11, 9, "y")
    stamp("tripod_small", a, 1, 2, note="a little gilded tripod, every one leaning slightly left")


def _laurel_pot():
    a = Art("nature", 1, 2)
    a.ellipse(3, 22, 12, 31, "m")
    a.ellipse(4, 22, 10, 25, "J")
    for (cx, cy, r) in ((8, 7, 6), (5, 13, 4), (11, 13, 4), (8, 18, 4)):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    a.px(x, y, "v" if (x - cx) + (y - cy) < -1 else "g" if (x - cx) + (y - cy) < 2 else "G")
    stamp("laurel_pot", a, 1, 2, note="a potted laurel, mostly dead")


for _f in (_hive_wall, _votives, _kitharas, _lead_strips, _frieze, _tripod_small, _laurel_pot):
    _f()
_painting("painting_city", "city")
_painting("painting_dead", "dead")
_ = math
