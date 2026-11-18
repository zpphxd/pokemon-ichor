"""Astyra's statues, painted to STYLE.md's statue rules (Architecture: Statues).

The quality bar is design/art/refs/statue_zeus_reference.png: readable
anatomy, a head that reads at 1x, an attribute in the hands, drapery folds in
value steps, a proper plinth seen in 3/4 (lit top face, front, shadowed side),
crisp dark outlines and a cast shadow falling down and to the right.

  promachos()      Athena Promachos, the 4 x 9 colossus (gTileset_Akropolis;
                   its top 4 x 5 is the city's skyline in gTileset_Astyra)
  hero_statue()    a 2 x 3 bronze statue on a 3/4 stone plinth, from an ASCII
                   figure: Kodros and Kairos in the agora
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import astyra_art as AA  # noqa: E402
import kythera_lib as K  # noqa: E402
from astyra_art import canvas, cut, mask_draw  # noqa: E402

FOLD = ["bz1", "bz2", "bz3", "bz3", "bz2", "bz1", "bz0"]       # one fold's value steps


def _figure():
    """Region labels for Promachos on a 64 x 144 canvas (heroic proportions,
    about six heads, so the head reads at 1x)."""
    W, H = 64, 144
    lab = np.zeros((H, W), np.uint8)
    regions = {}

    def region(n, fn):
        regions[n] = len(regions) + 1
        lab[mask_draw(W, H, fn)] = regions[n]
    region("crest", lambda d: d.polygon([(28, 14), (26, 7), (28, 2), (33, 0), (38, 3), (39, 9), (37, 15)], fill=1))
    region("skirt", lambda d: d.polygon([(22, 66), (42, 66), (45, 90), (47, 110), (18, 110), (20, 90)], fill=1))
    region("torso", lambda d: d.polygon([(22, 42), (42, 42), (42, 66), (22, 66)], fill=1))
    region("overfold", lambda d: d.polygon([(21, 58), (43, 58), (44, 70), (32, 74), (20, 71)], fill=1))
    region("aegis", lambda d: d.polygon([(18, 34), (46, 34), (45, 44), (32, 50), (19, 44)], fill=1))
    region("neck", lambda d: d.rectangle([29, 29, 35, 35], fill=1))
    region("helmet", lambda d: d.ellipse([23, 9, 41, 29], fill=1))
    region("face", lambda d: d.polygon([(27, 19), (37, 19), (37, 27), (34, 31), (30, 31), (27, 27)], fill=1))
    region("arm_r", lambda d: d.polygon([(18, 34), (24, 37), (20, 47), (15, 46)], fill=1))
    region("fore_r", lambda d: d.polygon([(15, 46), (20, 47), (17, 52), (12, 50)], fill=1))
    region("hand_r", lambda d: d.ellipse([8, 45, 16, 53], fill=1))
    region("spear", lambda d: d.rectangle([11, 10, 13, 112], fill=1))
    region("tip", lambda d: d.polygon([(12, 0), (14, 4), (14, 9), (12, 11), (10, 9), (10, 4)], fill=1))
    region("arm_l", lambda d: d.polygon([(41, 36), (46, 37), (49, 50), (44, 51)], fill=1))
    region("shield", lambda d: d.ellipse([36, 42, 62, 76], fill=1))
    region("feet", lambda d: d.polygon([(22, 107), (30, 107), (31, 112), (20, 112)], fill=1))
    region("feet2", lambda d: d.polygon([(35, 107), (43, 107), (45, 112), (35, 112)], fill=1))
    region("girdle", lambda d: d.rectangle([22, 57, 42, 59], fill=1))
    return lab, regions


def _shade(r, x, y):
    lit = x < 30                      # light from the upper left
    if r == "crest":
        c = "pr1"
        if x in (32, 33) or (y > 10 and x > 36):
            c = "bz1"
        if (x + y) % 5 == 0 and x > 34:
            c = "bz0"
        return c
    if r == "helmet":
        c = "bz3" if x < 29 else "bz2" if x < 36 else "bz1"
        if y < 12 and x < 32:
            c = "pg2"
        if y > 22 and (x < 27 or x > 37):
            c = "bz1" if x < 32 else "bz0"
        return c
    if r == "face":
        c = "bz3" if x < 31 else "bz2" if x < 35 else "bz1"
        if y == 22 and x in (29, 30, 34, 35):
            c = "bz0"
        if y == 23 and x in (29, 34):
            c = "bz0"
        if y == 23 and x in (30, 35):
            c = "pg2"
        if x == 32 and 23 <= y <= 26:
            c = "bz1" if y < 26 else "bz0"
        if y == 28 and 31 <= x <= 33:
            c = "bz0"
        if y == 30 and 30 <= x <= 34:
            c = "bz1"
        return c
    if r == "neck":
        return "bz1" if x > 32 else "bz2"
    if r == "aegis":
        c = ("bz3" if lit else "bz2") if (x + 2 * y) % 4 else ("bz1" if lit else "bz0")
        dd = (x - 32) ** 2 + (y - 40) ** 2
        if dd <= 6:
            c = "pg2" if x < 32 else "pg1"
        elif dd <= 9:
            c = "bz0"
        if y >= 42 and x % 3 == 0:
            c = "vg1"
        return c
    if r == "torso":
        c = "bz3" if x < 26 else "bz2" if x < 37 else "bz1"
        if x in (28, 35) and y > 46:
            c = "bz1"
        return c
    if r == "overfold":
        f = (x - 18) % 7
        c = FOLD[f] if lit or f in (5, 6) else ("bz2" if f < 4 else "bz1")
        if 69 - (x - 20) // 8 <= y <= 74:
            c = "bz3" if lit else "bz2"
        return c
    if r == "girdle":
        return "pg2" if x < 30 else "pg1"
    if r == "skirt":
        f = (x - 17) % 7
        c = FOLD[f]
        if not lit and f in (2, 3):
            c = "bz2"
        if x > 38:
            c = "bz1" if f < 5 else "bz0"
        if 80 <= y <= 92 and 34 <= x <= 39:
            c = "bz3" if x < 37 else "bz2"        # the relaxed knee catching the light
        if y > 104:
            c = "bz1" if f < 5 else "bz0"
        if (x * 7 + y * 3) % 29 == 0:
            c = "vg1"                               # verdigris in the creases
        return c
    if r == "arm_r":
        return "bz3" if (x + y) % 9 else "bz2"
    if r == "fore_r":
        return "bz2"
    if r == "arm_l":
        return "bz1"
    if r == "hand_r":
        return "bz2" if x < 12 else "bz1"
    if r == "spear":
        return "bz1" if x == 11 else "bz0" if x == 13 else "bz2"
    if r == "tip":
        return "cm5" if x == 12 and y < 9 else "pg2" if x < 12 else "pg1"
    if r == "shield":
        d = math.hypot((x - 49) / 13, (y - 59) / 17)
        if d > 0.88:
            return "pg2" if (x < 46 and y < 56) else "bz1"
        if d > 0.80:
            return "bz0"
        if d > 0.74:
            return "bz3" if x < 49 else "bz1"
        c = "bz2" if x < 47 else "bz1"
        if (abs(x - 46) <= 1 or abs(x - 52) <= 1) and 54 <= y <= 56:
            c = "pg2"                               # the owl's eyes
        if x in (46, 52) and y == 55:
            c = "bz0"
        if x == 49 and 57 <= y <= 58:
            c = "pg1"
        if 47 <= x <= 51 and 59 <= y <= 64 and (x + y) % 2 == 0:
            c = "pg1"
        if d < 0.7 and (x + y) % 13 == 0:
            c = "vg1"
        return c
    if r == "feet":
        return "bz2"
    if r == "feet2":
        return "bz1"
    return None


def plinth_3q(P, x0, x1, top, bottom, shadow="ps", ramp=("cm0", "cm1", "cm2", "cm3", "cm4", "cm5"),
              inscription=True):
    """A plinth in 3/4 view from x0 to x1, rows top..bottom: the lit top face
    (a band whose far edge is brightest), a moulded cornice, the front with a
    worn inscription, the east side face in shadow, a base course, and the cast
    shadow falling down and to the right of it."""
    o, s1, s2, s3, s4, s5 = ramp
    tf = top + max(3, (bottom - top) // 5)          # end of the top face
    cor = tf + 3
    base = bottom - 5
    side = x1 - max(3, (x1 - x0) // 10)
    for y in range(top, bottom + 1):
        for x in range(x0, x1 + 1):
            if y < tf:
                if x < x0 + 1 + (tf - 1 - y) // 2:
                    continue
                c = s5 if y < top + 2 else s4
            elif y < cor:
                c = s2 if y == tf else s4 if y == tf + 1 else s3
            elif y < base:
                if x < x0 + 2:
                    continue
                c = s4 if x < x0 + (x1 - x0) // 6 else s3
                if inscription and y == (cor + base) // 2 and x0 + 8 <= x <= side - 6 and x % 3:
                    c = s1
            else:
                c = s5 if y == base else s3 if y < bottom - 1 else s1
            if x >= side and y >= tf:
                c = s1 if x > side + 1 else s2
            if x in (x0, x1) or y == bottom:
                c = o
            P.px(x, y, c)
    if shadow:
        for y in range(top + 3, bottom + 3):
            for x in range(x1 + 1, x1 + 5):
                if (y - top - 3) // 3 >= x - x1 - 1 and ((x + y) % 2 == 0 or x < x1 + 3):
                    P.px(x, y, shadow)
        for x in range(x0 + 4, x1 + 5):
            if x < x1 - 8 or (x + bottom) % 2 == 0:
                P.px(x, bottom + 1, shadow)


def promachos(key="promachos", anim=True):
    """Athena Promachos, 4 x 9 on borrowed path: her figure on the top layer
    (rows 0-6, walk T: the player walks behind her shins), the plinth on the
    middle layer (rows 7-8, solid). Animation 'glint': a sparkle runs down the
    gold spear tip (cell r0c0)."""
    W, H = 4, 9
    L = canvas(W, H)
    lab, reg = _figure()
    inv = {v: k for k, v in reg.items()}
    for y in range(lab.shape[0]):
        for x in range(lab.shape[1]):
            r = inv.get(int(lab[y, x]))
            if r:
                c = _shade(r, x, y)
                if c:
                    L.px(x, y, c)
    m = lab > 0
    pad = np.pad(m, 1)
    edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if lab[y, x] != reg["tip"]:
            L.px(int(x), int(y), "bz0")
    # inner outlines where an arm or the shield crosses the body
    over = {reg[n] for n in ("shield", "arm_r", "fore_r", "hand_r")}
    for y in range(1, 143):
        for x in range(1, 64):
            a_, b_ = int(lab[y, x]), int(lab[y, x - 1])
            if a_ and b_ and a_ != b_ and (a_ in over or b_ in over):
                L.px(x, y, "bz0")
    P = canvas(W, H)
    plinth_3q(P, 2, 58, 112, 139)
    for y in range(112, 114):
        for x in range(64):
            if L.get(x, y):
                P.px(x, y, L.get(x, y))
    L.a[112:] = 0
    frames = []
    if anim:
        for f in range(3):
            F = canvas(W, H)
            pts = [((12, 2), (11, 3), (13, 3), (12, 4)),
                   ((12, 0), (12, 1), (9, 2), (15, 2), (10, 2), (14, 2), (12, 3), (12, 4), (11, 1), (13, 1),
                    (11, 3), (13, 3)),
                   ((12, 6), (11, 7), (13, 7), (12, 8))][f]
            for (x, y) in pts:
                F.px(x, y, "pg2" if (x, y) in ((9, 2), (15, 2)) else "cm5")
            frames.append(("top", F))
    walk = ["TTTT"] * 7 + ["XXXX"] * 2
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    s = cut(key, "Athena Promachos", W, H, {"middle": P, "top": L}, walk, names=names,
            notes="Athena Promachos, bronze, 4 x 9 on borrowed path: the Attic helmet and its red crest, "
                  "a face that reads at 1x (brows, inlaid eyes, nose, mouth), the aegis with the "
                  "gorgoneion, the owl shield on her left arm, the spear in her right hand with its gold "
                  "tip (the gleam sailors saw from Sounion; animation `glint` on r0c0), the peplos in "
                  "folds of five value steps. Rows 0-6 are drawn over the player (T); rows 7-8 are the "
                  "marble plinth in 3/4 with its cast shadow (X).",
            anims={"glint": frames} if anim else None)
    if anim:
        K.settle(s, "glint", [(0, 0)])
    return s


HERO_LEGEND = {"#": "bz0", "h": "bz3", "m": "bz2", "d": "bz1", "g": "pg2", "G": "pg1", "r": "pr1",
               "v": "vg1", "w": "cm5", "s": "cm3"}

KODROS = [
    # King Kodros: bearded, a plain cloak (he went out dressed as a woodcutter),
    # the spear he walked into reversed in his right hand, a crown at his feet
    "..........#.........",
    ".........#g#........",
    ".........#m#........",
    "......####d###......",
    ".....#hhhmmmdd#.....",
    ".....#hh#mm#dd#.....",
    ".....#hhmmmmdd#.....",
    "......#hmmmdd#......",
    "......#hhwwwd#......",
    ".....##hwwwwd##.....",
    "....#hh#hwwd#dd#....",
    "...#hhhmmmmmmddd#...",
    "..#hh#hhmmmmdd#dd#..",
    "..#h#.#hhmmmmd#.#d#.",
    "..#h#.#hhmmmdd#.#d#.",
    ".#hh#.#hmhmdmd#.#dd#",
    ".#mm#.#hmhmdmd#..##.",
    "..##..#hmhmdmd#.....",
    "...#..#hmhmdmd#.....",
    "...#..#hmhmdmd#.....",
    "...#.#hhmhmdmdd#....",
    "...#.#hmhmhmdmd#....",
    "...#.#hmhmhmdmd#....",
    "...#.#hmhmhmdmd#....",
    "...#.#hmhmhmdmd#....",
    "...#.#hhmhmdmdd#....",
    "...#..#hh#.#dd#.....",
    "...#..#hd#.#dd#.....",
    "...#.##hd#.#dd##....",
    "...#.#hhd#.#ddd#gG#.",
    "...##.####.####.##..",
]

KAIROS = [
    # Kairos, the Moment: a running youth with a forelock and a shaven nape,
    # winged heels, a razor in his left hand with a balance on its edge
    "....................",
    ".......###..........",
    "......#hhh#.........",
    ".....#hhhmm##.......",
    "....#hh#hmmd#.......",
    "....#h#hhmmd#.......",
    ".....##hmmdd#.......",
    "......#hmdd#........",
    ".....##hmmd###......",
    "....#hh#hmmdd##.#GG#",
    "...#hhh#hmmmdd##ggG#",
    "..#hh##hhmmmddd#.#G#",
    ".#hh#.#hhmmmdd#d#.#.",
    ".#h#..#hhmmmdd##d#..",
    "#hh#..#hhmmmdd#.#d#.",
    "#mm#...#hmmmd#..#d#.",
    ".##....#hmmmd#...#dg",
    "......#hhmmmdd#...##",
    "......#hhmm#dd#.....",
    ".....#hhm##.#dd#....",
    ".....#hm#...#dd#....",
    "....#hm#.....#dd#...",
    "...#hm#.......#dd#..",
    "..#hm#.........#dd#.",
    ".#hm#...........#d#.",
    ".#m#.............#d#",
    "#gw#.............#dw",
    "#gg#............#gww",
    ".##..............##.",
    "....................",
    "....................",
]


def hero_statue(key, figure, title, on="path", stone="marble"):
    """A bronze statue on a plinth, 2 x 3 on borrowed ground: the figure on the
    top layer (rows 0-1, walk T) and the plinth with its cast shadow on the
    middle layer (row 2, solid)."""
    W, H = 2, 3
    T = canvas(W, H)
    P = canvas(W, H)
    plinth_3q(P, 3, 27, 32, 45, shadow=AA.CK.SHADOW.get(on, "ps"))
    for j, rowstr in enumerate(figure):
        for i, ch in enumerate(rowstr):
            c = HERO_LEGEND.get(ch)
            if c:
                y = 2 + j
                (T if y < 32 else P).px(6 + i, y, c)
    return cut(key, title, W, H, {"middle": P, "top": T}, ["TT", "TT", "XX"],
               names={"TL": (0, 0), "TR": (1, 0), "ML": (0, 1), "MR": (1, 1), "BL": (0, 2), "BR": (1, 2)},
               on=on, section="town",
               notes=f"{title} (2 x 3): bronze on a 3/4 marble plinth, its cast shadow on the floor. "
                     "Rows 0-1 over the player, the plinth solid; the bg event is on the plinth.")
