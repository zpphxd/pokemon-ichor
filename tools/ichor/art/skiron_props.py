"""Skiron props: the Corinthian potters' works by the road, beehives, and
the procession's camp.

- Works (clay group): round updraft kilns (firing and cold), a rack of
  drying Corinthian pots, a wasters' heap of sherds, firewood, amphorae.
- Beehives (clay): horizontal clay hives on stones, single and stacked.
- The camp: linen tents, bedrolls, myrtle, the sacred baskets (linen group);
  the cookfire and the procession's cart (clay group).
"""
from __future__ import annotations

import math

import numpy as np

from skiron_lib import Struct, disc, ground, oval_shadow

SEC_WORKS, SEC_CAMP = "works", "camp"


def outline(L, color="ink", skip=()):
    a = L.a[..., 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if L.get(x, y) not in skip:
            L.px(x, y, color)


def shaded_disc(L, cx, cy, rx, ry, ramp):
    m = disc(L.w, L.h, cx, cy, rx, ry)
    for y, x in zip(*np.nonzero(m)):
        u = ((x - cx) / max(rx, 1) + (y - cy) / max(ry, 1)) / 2
        k = 0.5 - 0.8 * u
        L.px(x, y, ramp[int(max(0, min(len(ramp) - 1, round(k * (len(ramp) - 1)))))])
    return m


# --------------------------------------------------------------------------
# The potters' works
# --------------------------------------------------------------------------

def kiln(lit):
    key = "kiln" if lit else "kiln_cold"
    s = Struct(key, "Potter's kiln, firing" if lit else "Potter's kiln, cold", 2, 2, SEC_WORKS,
               walk=["XX", "XX"],
               notes=("A round updraft kiln of mud-plastered brick, soot-black round its vent, "
                      "the stoke-hole glowing: Corinth's black glaze is fired here, the vents "
                      "closed at the end to starve the fire. Impassable."
                      if lit else "The same kiln cooling, its stoke-hole dark and stacked with "
                                  "fresh wood. Impassable."))
    ground(s, "grass")
    A = s.M
    oval_shadow(A, 17, 29, 15, 3)
    # the dome
    dome = disc(32, 32, 16, 17, 13, 14)
    dome[28:] = False
    for y, x in zip(*np.nonzero(dome)):
        u = ((x - 16) / 13 + (y - 17) / 14) / 2
        c = "p2" if u < -0.5 else "p1" if u < -0.15 else "l1" if u < 0.25 else "wd1"
        if y < 9 and abs(x - 16) < 6 and (x + y) % 2 == 0:
            c = "k1"                                           # soot round the vent
        A.px(x, y, c)
    for (x0, y0, x1, y1) in ((8, 12, 10, 18), (23, 9, 24, 15), (20, 20, 22, 24)):
        A.line(x0, y0, x1, y1, "wd1")                          # cracks in the plaster
    A.ellipse(13, 3, 19, 6, "ink")                             # the vent
    if lit:
        A.ellipse(14, 4, 18, 5, "tc1")
        A.px(16, 4, "tg")
    # a brick ring round its foot
    for x in range(4, 29):
        A.px(x, 27, "tc1" if x % 3 else "tc0")
        A.px(x, 28, "tc0")
    # the stoke-hole, an arch of fired brick
    for y in range(17, 28):
        for x in range(10, 23):
            r = ((x - 16) / 6.0) ** 2 + ((y - 21) / 4.5) ** 2
            if y >= 21 or r <= 1.0:
                if abs(x - 16) >= 5 or (y < 21 and r > 0.65):
                    A.px(x, y, "tc1")
                else:
                    A.px(x, y, "ink")
    if lit:
        A.blit(["  tt   ",
                " tggt  ",
                "tgyygt ",
                "tgyyygt",
                "ccttcct"], {"t": "tc1", "g": "tc2", "y": "tg", "c": "tc0"}, 13, 22)
    else:
        for (x, y) in ((13, 25), (16, 24), (19, 25), (14, 23), (18, 23)):
            A.blit(["oo", "kk"], {"o": "wd2", "k": "wd1"}, x, y)
    outline(A, skip=("tc0",))
    return s


def pots():
    s = Struct("pot_rack", "Drying rack of Corinthian pots", 2, 1, SEC_WORKS, walk=["XX"],
               notes="A plank on trestles crowded with pale Corinthian ware drying before the "
                     "kiln: round aryballoi, cups, a jug, banded in black and purple. "
                     "Impassable.")
    ground(s, "grass")
    A = s.M
    for x in range(1, 31, 2):
        A.px(x, 15, "gd")
    A.rect(1, 10, 30, 2, "wd2")
    A.hline(1, 30, 12, "wd1")
    for x in (3, 15, 28):
        A.vline(x, 13, 15, "wd1")
    shapes = [
        (2, ["  kk  ", " pppp ", "pkkkkp", "pppppp", " pccp ", "  pp  "]),       # aryballos
        (8, [" kkkk ", "pppppp", "kkkkkk", " pppp ", "  pp  "]),                 # kotyle
        (14, [" k ", " pp", "pkpp", "pppp", "kkkk", "pppp", " pp "]),           # jug
        (19, ["  kk  ", " pppp ", "pkckcp", "pppppp", " pppp ", "  pp  "]),
        (25, ["kkkkk", "ppppp", "ckckc", " ppp ", "  p  "]),
    ]
    for x0, rows in shapes:
        h = len(rows)
        A.blit(rows, {"p": "p2", "k": "ink", "c": "tc0"}, x0, 10 - h)
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == "p" and (i == 0 or row[:i].strip() == ""):
                    A.px(x0 + i, 10 - h + j, "p1")
    return s


def sherds():
    s = Struct("sherds", "Wasters' heap", 1, 1, SEC_WORKS, walk=["X"],
               notes="Pots that cracked in the firing, thrown on a heap: every kiln yard has "
                     "one. Impassable.")
    ground(s, "grass")
    A = s.M
    A.poly([(1, 14), (7, 4), (11, 6), (15, 14)], "l1")
    for (x, y, c) in ((4, 11, "tc1"), (8, 7, "tc2"), (10, 11, "p2"), (6, 9, "tc1"), (12, 12, "tc2"),
                      (3, 13, "p2"), (9, 13, "tc0"), (7, 12, "p1")):
        A.blit(["cc", "c "], {"c": c}, x, y)
        A.px(x + 1, y + 1, "ink")
    A.blit(["kk", "pp", "pp"], {"k": "ink", "p": "tc1"}, 7, 2)     # a jar's neck sticking up
    A.px(8, 3, "tc2")
    outline(A)
    for x in range(1, 16, 2):
        A.px(x, 15, "gd")
    return s


def firewood():
    s = Struct("firewood", "Firewood stack", 2, 1, SEC_WORKS, walk=["XX"],
               notes="Split pine logs stacked end-out and bundles of brushwood: a kiln eats a "
                     "hillside a year. Impassable.")
    ground(s, "grass")
    A = s.M
    for x in range(0, 32, 2):
        A.px(x, 15, "gd")
    for row, (y, xs) in enumerate(((11, range(2, 20, 4)), (7, range(4, 18, 4)), (3, range(6, 16, 4)))):
        for x in xs:
            A.ellipse(x, y, x + 3, y + 3, "ink")
            A.ellipse(x + 1, y + 1, x + 2, y + 2, "wd2")
            A.px(x + 1, y + 1, "p1")
    for i in range(5):                                         # brushwood bundles
        A.line(20 + i * 2, 14, 24 + i * 2, 4, "wd1")
        A.line(21 + i * 2, 14, 25 + i * 2, 5, "k1")
    A.hline(19, 31, 9, "tg")                                   # the binding
    return s


def amphorae():
    s = Struct("amphorae", "Amphorae, leaning", 1, 1, SEC_WORKS, walk=["X"],
               notes="Three amphorae propped together. Impassable.")
    ground(s, "grass")
    A = s.M
    oval_shadow(A, 8, 14, 7, 2)
    for i, x0 in enumerate((1, 6, 10)):
        y0 = 2 + (i % 2)
        A.blit([" kk ",
                " cc ",
                "kccck",
                "cbccc",
                "cbccc",
                "cbccc",
                " ccc ",
                "  c  ",
                "  k  "], {"k": "ink", "c": "tc1", "b": "tc2"}, x0, y0)
        A.vline(x0 + 3, y0 + 3, y0 + 6, "tc0")
    outline(A)
    return s


# --------------------------------------------------------------------------
# Beehives
# --------------------------------------------------------------------------

def hive_at(A, cx, cy, r):
    """A clay tube hive lying north-south, seen end-on: its round mouth, a
    plug of clay with the bees' door low in it, a flat stone laid on top for
    shade."""
    shaded_disc(A, cx, cy, r, r, ("tc0", "tc1", "tc1", "tc2"))
    A.ellipse(cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2, "p1")   # the clay plug
    A.ellipse(cx - r + 3, cy - r + 3, cx + r - 2, cy + r - 2, "l1")
    A.px(cx, cy + r - 3, "ink")                                       # the bees' door
    A.px(cx + 1, cy + r - 3, "ink")
    A.rect(cx - r - 1, cy - r - 2, 2 * r + 3, 2, "l1")                # the shading stone
    A.hline(cx - r - 1, cx + r + 1, cy - r - 2, "p2")
    for (dx, dy) in ((-r - 2, 1), (r + 2, -1), (1, r + 2)):
        A.px(cx + dx, cy + dy, "ink")
        A.px(cx + dx + 1, cy + dy, "tg")


def hives():
    out = []
    s = Struct("hive", "A clay beehive", 1, 1, SEC_WORKS, walk=["X"],
               notes="A long clay hive laid on two stones, its door to the sun. Impassable.")
    ground(s, "grass")
    A = s.M
    oval_shadow(A, 8, 14, 7, 2)
    A.blit(["ss", "ll"], {"s": "p1", "l": "l1"}, 3, 12)
    A.blit(["ss", "ll"], {"s": "p1", "l": "l1"}, 11, 12)
    hive_at(A, 8, 8, 5)
    outline(A, skip=("tg",))
    out.append(s)
    t = Struct("hives", "Beehives on a bench", 2, 1, SEC_WORKS, walk=["XX"],
               notes="Three clay hives stacked on a stone bench in the thyme: a beekeeper's "
                     "row. Impassable.")
    ground(t, "grass")
    A = t.M
    for x in range(1, 31):
        A.px(x, 13, "p1" if x % 6 else "l1")
        A.px(x, 14, "l1")
        if x % 2:
            A.px(x, 15, "gd")
    hive_at(A, 6, 8, 4)
    hive_at(A, 16, 8, 4)
    hive_at(A, 26, 8, 4)
    outline(A, skip=("tg", "gd"))
    out.append(t)
    return out


# --------------------------------------------------------------------------
# The procession's camp
# --------------------------------------------------------------------------

def tent():
    s = Struct("tent", "Pilgrims' tent", 2, 2, SEC_CAMP, walk=["XX", "XX"],
               notes="A linen ridge tent of the procession, its door flap tied back, guy ropes "
                     "pegged out. `tent_b` is its mirror. Impassable.")
    ground(s, "grass")
    A = s.M
    for x in range(4, 31):
        for y in (26, 27, 28):
            if (x + y) % 2 == 0:
                A.px(x, y, "gd")
    # the sunlit south slope, widening to its hem
    for y in range(6, 25):
        spread = (y - 6) // 5
        for x in range(5 - spread, 28 + spread):
            c = "w0" if y < 11 else "w1" if y < 21 else "m3"
            if (x - 3) % 7 == 0 and y > 7:
                c = "w1" if c == "w0" else "m3"                 # seams
            A.px(x, y, c)
    # the shaded east gable
    for y in range(6, 25):
        for x in range(28 + (y - 6) // 5, 28 + (y - 6) // 5 + 2 + (y - 6) // 6):
            A.px(x, y, "m3")
    A.hline(3, 29, 5, "wd2")                                    # the ridge pole
    A.hline(4, 28, 4, "wd1")
    A.vline(3, 3, 6, "wd1")
    A.vline(29, 3, 6, "wd1")
    # the door, its flap tied back
    for y in range(12, 25):
        half = (y - 12) // 2
        for x in range(16 - half, 17 + half):
            A.px(x, y, "ink" if x > 16 - half else "k1")
    for y in range(13, 22):
        A.px(15 - (y - 12) // 2 - 1, y, "w0")
    A.hline(8, 12, 15, "tc1")                                   # a woven band
    # guy ropes and pegs
    A.line(3, 6, 0, 18, "wd1")
    A.line(29, 6, 31, 18, "wd1")
    A.px(0, 19, "wd2")
    A.px(31, 19, "wd2")
    for y in range(24, 26):
        for x in range(2, 31):
            if A.get(x, y) in ("m3", "w1"):
                A.px(x, y, "m3" if y == 24 else "ink")
    outline(A, skip=("wd1", "wd2", "gd"))
    t = Struct("tent_b", "Pilgrims' tent, mirrored", 2, 2, SEC_CAMP, walk=["XX", "XX"],
               notes="The mirror of `tent`.")
    for ln in ("bottom", "middle", "top"):
        t.layers[ln].a[:] = s.layers[ln].a[:, ::-1]
    ground(t, "grass")
    return [s, t]


def camp_small():
    out = []
    s = Struct("bedrolls", "Bedrolls and a bundle", 1, 1, SEC_CAMP, walk=["X"],
               notes="Striped blankets rolled up for the day, a linen bundle. Impassable.")
    ground(s, "grass")
    A = s.M
    oval_shadow(A, 8, 14, 7, 2)
    A.blit([" wwwwwwww ",
            "wwrwwrwwrw",
            "wwrwwrwwrw",
            " mmmmmmmm "], {"w": "w1", "r": "tc1", "m": "m3"}, 2, 8)
    A.ellipse(4, 2, 11, 8, "w0")
    A.ellipse(8, 4, 11, 8, "w1")
    A.px(7, 2, "wd1")
    A.px(8, 2, "wd1")
    outline(A, skip=("gd",))
    out.append(s)
    s = Struct("myrtle", "Myrtle bundles on staves", 1, 1, SEC_CAMP, walk=["X"],
               notes="The initiates' myrtle: bundles of flowering branches on their walking "
                     "staves, leaning together. Impassable.")
    ground(s, "grass")
    A = s.M
    oval_shadow(A, 8, 14, 6, 2)
    for (x0, x1) in ((4, 8), (12, 8), (8, 8)):
        A.line(x0, 14, x1, 3, "wd2")
    for (cx, cy) in ((5, 5), (11, 5), (8, 3)):
        A.ellipse(cx - 3, cy - 2, cx + 3, cy + 3, "c1")
        A.ellipse(cx - 2, cy - 2, cx + 2, cy + 1, "c2")
        A.px(cx - 1, cy - 1, "c3")
        A.px(cx + 1, cy, "w0")
        A.px(cx - 2, cy + 1, "w0")
    outline(A, skip=("gd", "wd2"))
    out.append(s)
    s = Struct("baskets", "The sacred baskets", 1, 1, SEC_CAMP, walk=["X"],
               notes="Lidded wicker kistai, the sacred things the procession carries to "
                     "Eleusa, tied shut with red wool. Nobody looks inside. Impassable.")
    ground(s, "grass")
    A = s.M
    oval_shadow(A, 8, 14, 7, 2)
    for (x0, y0, w, h) in ((1, 6, 8, 7), (8, 4, 7, 9)):
        A.rect(x0, y0, w, h, "wd2")
        for y in range(y0 + 1, y0 + h):
            for x in range(x0, x0 + w):
                if (x + y) % 3 == 0:
                    A.px(x, y, "wd1")
        A.rect(x0 - 1, y0 - 1, w + 2, 2, "wd1")
        A.hline(x0 - 1, x0 + w, y0 - 1, "wd2")
        A.vline(x0 + w // 2, y0 - 1, y0 + h - 1, "tc1")
    outline(A, skip=("gd",))
    out.append(s)
    return out


def cookfire():
    s = Struct("cookfire", "The camp's cookfire", 1, 1, SEC_CAMP, walk=["X"],
               notes="A ring of stones round a cooking fire, a pot of barley on the embers. "
                     "Impassable.")
    ground(s, "grass")
    A = s.M
    for i in range(12):
        a = 2 * math.pi * i / 12
        x, y = 8 + round(6 * math.cos(a)), 10 + round(3.5 * math.sin(a))
        A.blit(["pl", "ll"], {"p": "p1", "l": "l1"}, x - 1, y - 1)
        A.px(x, y + 1, "ink")
    A.ellipse(3, 8, 12, 12, "k1")
    A.blit(["  y  ",
            " yty ",
            " tgt ",
            "tgygt",
            "ctgtc",
            "wwcww"], {"y": "tg", "t": "tc1", "g": "tc2", "c": "tc0", "w": "wd1"}, 5, 4)
    return s


def cart():
    s = Struct("cart", "The procession's cart", 3, 2, SEC_CAMP, walk=["XXX", "XXX"],
               notes="A two-wheeled cart piled with myrtle, the sacred baskets roped on top, "
                     "its shafts down to the west where the pack donkey stands. Impassable.")
    ground(s, "grass")
    M = s.M
    for x in range(6, 46):
        for y in (28, 29, 30):
            if (x + y) % 2 == 0:
                M.px(x, y, "gd")
    M.line(0, 25, 14, 17, "ink")
    M.line(0, 24, 14, 16, "wd2")
    M.line(1, 26, 14, 18, "wd1")
    M.rect(12, 14, 33, 3, "wd2")
    M.hline(12, 44, 13, "ink")
    M.hline(12, 44, 17, "ink")
    M.rect(12, 18, 33, 2, "wd1")
    M.hline(12, 44, 20, "ink")
    M.vline(12, 13, 20, "ink")
    M.vline(44, 13, 20, "ink")
    # the load: myrtle heaped high, white-flowered, two baskets roped on
    for (cx, cy, rx, ry) in ((19, 9, 7, 5), (30, 8, 8, 6), (40, 10, 5, 4), (25, 4, 5, 3)):
        m = disc(48, 32, cx, cy, rx, ry)
        for y, x in zip(*np.nonzero(m)):
            u = ((x - cx) / rx + (y - cy) / ry) / 2
            M.px(x, y, "g1" if u < -0.2 else "gd")
    for (x, y) in ((16, 7), (22, 5), (27, 9), (33, 4), (38, 8), (19, 11), (31, 11), (25, 3)):
        M.px(x, y, "p2")
    for (x0, y0) in ((22, 6), (33, 5)):
        M.rect(x0, y0, 7, 6, "wd2")
        M.hline(x0, x0 + 6, y0, "wd1")
        M.vline(x0 + 3, y0, y0 + 5, "tc1")
        M.hline(x0 - 1, x0 + 7, y0 - 1, "ink")
    M.line(14, 13, 44, 6, "tg")                                 # the rope over the load
    # the wheel
    cx, cy, r = 29, 22, 8
    for y in range(cy - r - 1, cy + r + 2):
        for x in range(cx - r - 1, cx + r + 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if r - 1.5 <= d <= r + 0.5:
                M.px(x, y, "ink" if d > r - 0.3 else "wd1")
    for (dx, dy) in ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
        M.line(cx, cy, cx + dx * (r - 2), cy + dy * (r - 2), "wd2")
    M.ellipse(cx - 2, cy - 2, cx + 2, cy + 2, "ink")
    M.px(cx, cy, "tg")
    return s


def works():
    # The cold kiln and the single hive are drawn but held for the tile budget.
    return [kiln(True), pots(), sherds(), firewood(), amphorae(), hives()[1]]


def camp():
    return [*tent(), *camp_small(), cookfire(), cart()]
