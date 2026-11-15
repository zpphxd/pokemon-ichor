#!/usr/bin/env python3
"""The Euploia's scene objects: the halcyon nest and the dark trireme.

  nest_eggs, nest_hatching, nest_empty   32x32: the floating nest of woven
      seaweed and feathers, with three eggs, then cracking with a chick's head
      out, then empty but for the shells (beat 10, at the ram)
  dark_trireme_bow, dark_trireme_stern   64x32 each, side by side: a trireme
      with no lamps, its oars muffled in leather, a sickle painted on its
      furled sail (beat 10's night leg, sliding past to starboard)

All in the "Ichor cast" OBJ palette (sprites_npc.CAST_PAL), so they cost no
palette slot on a map that shows the cast. Registered as
OBJ_EVENT_GFX_ICHOR_NEST_* and OBJ_EVENT_GFX_ICHOR_DARK_TRIREME_*.

Usage: /usr/bin/python3 tools/ichor/art/trireme_objects.py [--write] [--preview out.png]
  --write   graphics/object_events/pics/misc/ichor/<name>.png
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, save_indexed, to_rgba, upscale  # noqa: E402
from sprites_npc import CAST_PAL  # noqa: E402

OUT_DIR = os.path.join(ROOT, "graphics/object_events/pics/misc/ichor")
P = CAST_PAL


class Pic:
    def __init__(self, w, h):
        self.a = np.zeros((h, w), np.int32)
        self.w, self.h = w, h

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = 0 if c is None else P[c]

    def blit(self, rows, legend, x, y):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in legend:
                    self.px(x + i, y + j, legend[ch])

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(self.h):
            for x in range(self.w):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    self.px(x, y, c)


# ---------------------------------------------------------------------------
# The halcyon nest
# ---------------------------------------------------------------------------

def nest_base():
    """The floating nest, 32x32 with the nest in the lower half: ripples on the
    flat sea, a raft of woven seaweed, a ring of weed round a dark cup, and a few
    white feathers worked into the rim."""
    p = Pic(32, 32)
    for x in range(1, 31):
        if x % 5 in (0, 1, 2):
            p.px(x, 29, "linen_l" if x % 10 < 5 else "blue")
    for x in range(4, 28):
        if x % 4 in (1, 2):
            p.px(x, 30, "blue")
    # the raft
    p.ellipse(15.5, 25, 13, 4.2, "brown")
    p.ellipse(15.5, 24.2, 12, 3.4, "leaf")
    for x in range(3, 29):
        for y in range(20, 29):
            if p.a[y, x] == P["leaf"] and (x * 3 + y * 5) % 7 == 0:
                p.px(x, y, "umber")
    for (x0, d) in ((3, -1), (28, 1), (9, -1), (23, 1)):
        for k in range(4):
            p.px(x0 + d * k, 27 + (k + 1) // 2, "leaf" if k < 3 else "brown")
    # the rim of woven weed and the dark cup inside it
    p.ellipse(15.5, 21.5, 9.5, 3.6, "umber")
    p.ellipse(15.5, 21, 8.5, 3.0, "leaf")
    p.ellipse(15.5, 21, 6.5, 2.2, "brown")
    p.ellipse(15.5, 21.3, 5.2, 1.5, "ink")
    # outline the raft and rim against the water
    a = p.a
    m = (a > 0) & (a != P["blue"])
    m[28:, :] = False
    pad = np.pad(m, 1)
    edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        p.px(x, y, "ink")
    # white feathers worked into the rim
    for (x, y, rows) in ((5, 18, ["kLk", "kLLk", " kLk"]), (24, 18, [" kLk", "kLLk", "kLk "]),
                         (14, 22, ["kLLLk"]), (8, 22, ["kLLk"]), (21, 22, ["kLLk"])):
        p.blit(rows, {"k": "ink", "L": "linen_l"}, x, y)
    return p


def egg(p, x, y, crack=False):
    rows = [" kkk ", "kLLLk", "kLLlk", "kLllk", " kkk "]
    if crack:
        rows = [" kkk ", "kLkLk", "kkLkk", "kLllk", " kkk "]
    p.blit(rows, {"k": "ink", "L": "linen_l", "l": "linen_d"}, x, y)


def nest_eggs():
    p = nest_base()
    for (x, y) in ((10, 17), (14, 16), (18, 17)):
        egg(p, x, y)
    return p


def nest_hatching():
    p = nest_base()
    egg(p, 9, 17, crack=True)
    egg(p, 19, 17, crack=True)
    # a chick's blue head and bronze beak out of the middle shell
    p.blit(["  kkk   ", " kBBBk  ", "kBnBBBk ", "kBBBBkook", " kBBBk  ", "kLkkkLk ", "kLLLLLk ",
            " kkkkk  "],
           {"k": "ink", "B": "blue", "n": "blue_d", "o": "bronze", "L": "linen_l"}, 12, 11)
    return p


def nest_empty():
    p = nest_base()
    for (x, y) in ((10, 19), (15, 18), (19, 19)):
        p.blit([" k k ", "kLkLk", " kkk "], {"k": "ink", "L": "linen_l"}, x, y)
    return p


# ---------------------------------------------------------------------------
# The dark trireme: 128x32, bow to the west, cut into two 64x32 halves
# ---------------------------------------------------------------------------

def dark_trireme():
    p = Pic(128, 32)
    wl = 27                                    # waterline
    # faint wake along the hull, the only light about her
    for x in range(6, 124):
        if x % 7 in (0, 1):
            p.px(x, wl + 2, "blue")
        if x % 13 == 3:
            p.px(x, wl + 3, "linen_d")
    # the hull: long, low and black, sheer rising at both ends
    for x in range(10, 120):
        top = 19
        if x < 22:
            top = 19 - (22 - x) // 3
        if x > 106:
            top = 19 - (x - 106) // 2
        bot = wl if 14 <= x <= 114 else wl - 1
        for y in range(top, bot + 1):
            c = "ink"
            if y == top:
                c = "slate"
            elif y == top + 3:
                c = "brown"                     # the wale, unpainted
            p.px(x, y, c)
    # the oarbox and the muffled oars, dipping into the water
    for x in range(26, 104):
        p.px(x, 22, "slate" if x % 4 else "ink")
    for x0 in range(28, 104, 6):
        for k in range(6):
            p.px(x0 - k // 2, 23 + k, "brown")
        p.px(x0 - 3, 29, "slate")
    # the ram and the stem at the bow (west)
    p.blit(["kkkk     ", "kttkkkkkk", "kktttttkk", "  kkkkkk "], {"k": "ink", "t": "slate"}, 2, 24)
    for y in range(9, 20):
        p.px(12 - (19 - y) // 4, y, "ink")
        p.px(13 - (19 - y) // 4, y, "slate")
    p.blit(["kk ", "ktk", " kk"], {"k": "ink", "t": "slate"}, 9, 7)
    # the aphlaston at the stern (east), dark timbers curling forward
    for k in range(3):
        for i in range(24):
            t = i / 23
            x = 118 - k * 2 + 4 * math.sin(math.pi * t) - 9 * t * t
            y = 19 - 15 * math.sin(math.pi / 2 * t) + k
            p.px(int(round(x)), int(round(y)), "slate" if k == 1 else "ink")
    # the mast and the yard with the fat roll of the furled sail
    for y in range(2, 20):
        p.px(56, y, "ink")
        p.px(57, y, "slate")
    for x in range(32, 82):
        p.px(x, 1, "ink")
        p.px(x, 2, "slate")
        for y in range(3, 10):
            inside = 34 <= x < 80
            c = "ink" if not inside or y in (3, 9) else "slate" if y in (4, 8) else "brown"
            p.px(x, y, c)
    for x in range(36, 80, 6):
        for y in range(4, 9):
            p.px(x, y, "ink")                      # the gaskets
    # the sickle, painted pale across the furled cloth: a hooked blade, a haft
    p.blit([
        "      LLLLL     ",
        "    LLl   LLL   ",
        "   Ll       Ll  ",
        "  Ll          L ",
        "  L             ",
        "  Lb            ",
        "   bb           ",
    ], {"L": "linen_l", "l": "linen_d", "b": "umber"}, 44, 3)
    return p


def pics():
    ship = dark_trireme().a
    return {
        "nest_eggs": nest_eggs().a,
        "nest_hatching": nest_hatching().a,
        "nest_empty": nest_empty().a,
        "dark_trireme_bow": ship[:, :64],
        "dark_trireme_stern": ship[:, 64:],
    }


def main():
    args = sys.argv[1:]
    parts = pics()
    if "--write" in args:
        os.makedirs(OUT_DIR, exist_ok=True)
        for name, arr in parts.items():
            path = os.path.join(OUT_DIR, name + ".png")
            save_indexed(arr, CAST_PAL, path)
            print(path)
    if "--preview" in args:
        from PIL import Image
        sea = (48, 104, 176, 255)
        out = Image.new("RGBA", (128 + 3 * 36, 40), sea)
        x = 2
        for name in ("nest_eggs", "nest_hatching", "nest_empty"):
            out.alpha_composite(to_rgba(parts[name], CAST_PAL), (x, 4))
            x += 36
        out.alpha_composite(to_rgba(parts["dark_trireme_bow"], CAST_PAL), (x, 4))
        out.alpha_composite(to_rgba(parts["dark_trireme_stern"], CAST_PAL), (x + 64, 4))
        path = args[args.index("--preview") + 1]
        upscale(out, 4).save(path)
        print(path)


if __name__ == "__main__":
    main()
