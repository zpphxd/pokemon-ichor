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


# --------------------------------------------------------------------------
# Athena Promachos (4 x 9): drawn on a 2x mask, reduced, hand-finished at 1x
# --------------------------------------------------------------------------

# the bronze ramp, darkest to brightest (outline, crease, shadow, half-tone,
# mid, light, gold highlight): the value steps every fold and limb uses
RAMP = ["bz0", "bzd", "bz1", "bzm", "bz2", "bz3", "pg2"]
LEG = {"#": "bz0", "d": "bzd", "1": "bz1", "m": "bzm", "2": "bz2", "3": "bz3", "g": "pg2",
       "G": "pg1", "w": "pgw", "r": "pr1", "R": "prd", "W": "cm5", "o": "cm3"}

# The head, placed by hand at 1x: the Corinthian helmet pushed back on her
# crown (its visor tipped up over the brow, eye-holes and nose-guard showing,
# a gold rim), the face under it (brows, inlaid eyes glancing toward the
# spear, the nose's lit ridge, a closed mouth, the chin), hair falling behind
# her neck. Columns are x 16..43, rows y 6..36.
HEAD = [
    ".......########.............",   # 6
    "......#wg33322d#............",   # 7
    ".....#wg333222211#..........",   # 8
    "....#gg3332222211d#.........",   # 9
    "....#g333222222111d#........",   # 10
    "...#33322222221111dd#.......",   # 11
    "...#gggggggGGGGGGGGd#.......",   # 12
    "...#3322222222111111#.......",   # 13
    "...#3###2232###1111d#.......",   # 14
    "...#3#d#2231#d#1ddd#........",   # 15
    "...#32#2223122#11dd#........",   # 16
    "....#22222311111dd#.........",   # 17
    "....#d#dd1dd1dd1d##d#.......",   # 18
    "...#1#3332222221d#dd#.......",   # 19
    "...#m#3ddd22ddd1d#1d#.......",   # 20
    "...#m#3#W22#od1d#1dd#.......",   # 21
    "...#1#33222322211d#1d#......",   # 22
    "...#1##33222312211#1d#......",   # 23
    "...#m.#33223122d1#.1dd#.....",   # 24
    "...#1.#332mdm221#..1dd#.....",   # 25
    "...#d.#33222221d#..#1d#.....",   # 26
    "...##..#32ddd2d#...#1dd#....",   # 27
    ".......#322m21d#...#1dd#....",   # 28
    "........#3222d#.....#dd#....",   # 29
    ".........#####......#dd#....",   # 30
    ".........#32m1#......##.....",   # 31
    ".........#3221#.............",   # 34
    "........#33221d#............",   # 35
    "........#32221d#............",   # 36
]
HEAD_X, HEAD_Y = 16, 8

# The owl on her shield, in gold: ear tufts, two great eyes, the beak, the
# breast feathers in chevrons, the talons. 11 x 15, centred on the shield.
OWL = [
    "#.........#",
    "#g#.....#G#",
    "#gg#####GG#",
    "#gwww#wwwG#",
    "#gw#wGw#wG#",
    "#gwwwGwwwG#",
    "#ggg#d#GGG#",
    ".#ggGdGGG#.",
    ".#gGgGgGG#.",
    ".#ggGgGGG#.",
    ".#gGgGgGG#.",
    "..#ggGGG#..",
    "..#gGgGG#..",
    "...#####...",
    "..#G#.#G#..",
]
SHIELD = (53.5, 64, 10.5, 17)         # centre x, y, radii


def _promachos_masks():
    """Region masks drawn at 2x (smooth limbs and drapery) and reduced to the
    64 x 144 canvas, back to front."""
    W, H, S = 64, 144, 2
    lab = np.zeros((H, W), np.uint8)
    regions = {}

    def put(n, big):
        small = big.reshape(H, S, W, S).sum(axis=(1, 3)) >= 2
        regions.setdefault(n, len(regions) + 1)
        lab[small] = regions[n]

    def poly(n, pts):
        put(n, mask_draw(W * S, H * S, lambda d: d.polygon([(x * S, y * S) for x, y in pts], fill=1)))

    def ell(n, x0, y0, x1, y1):
        put(n, mask_draw(W * S, H * S, lambda d: d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=1)))
    # the crest, standing off the helmet on its holder, sweeping back
    poly("crest", [(x, y + 2) for x, y in
                   [(22, 10), (20.5, 5), (23, 1.5), (28, 0), (34, 0), (39, 2), (42.5, 6.5), (43.5, 12),
                    (42.5, 18), (40, 21), (37.5, 19), (39, 13), (37.5, 7.5), (33.5, 4.5), (28, 4.5),
                    (25.5, 6.5), (24.5, 9)]])
    # the peplos: the weight leg (her right) straight, the free knee pushing forward
    poly("skirt", [(20, 61), (37, 62), (40, 71), (42.5, 82), (42, 92), (42.5, 101), (46.5, 109),
                   (36, 110.5), (26, 110), (16, 109), (16.5, 101), (17, 90), (15.5, 76), (16, 67)])
    poly("foot_r", [(17.5, 108), (26, 108), (27.5, 114), (17, 114)])
    poly("foot_l", [(37, 109), (45, 109), (47.5, 114.5), (37, 114.5)])
    poly("torso", [(19.5, 42), (36.5, 42), (37, 49), (35.5, 56), (36.5, 62), (19.5, 61), (20.5, 56), (18.5, 49)])
    poly("overfold", [(16, 57), (38.5, 58), (41, 66), (39, 70.5), (29, 72), (18, 71), (14.5, 66.5)])
    poly("girdle", [(18, 57), (38.5, 58.5), (38.5, 60.5), (18, 59)])
    # the aegis over her shoulders, scalloped where its snakes hang
    pts = [(17.5, 39), (20, 37), (36, 37), (38.5, 39), (40.5, 42.5)]
    for i, x in enumerate(range(40, 15, -3)):
        pts.append((x, 47 - abs(x - 28) * 0.18 + (1.6 if i % 2 else 0)))
    pts += [(15.5, 42.5)]
    poly("aegis", pts)
    # her right arm raised, out from the body, the fist round the spear
    poly("arm_r", [(20, 37.5), (20, 43.5), (15, 47.5), (11, 46), (12.5, 40.5)])
    poly("fore_r", [(16, 45), (11.5, 47.5), (7, 26), (11.5, 23.5)])
    poly("spear", [(4, 12), (7.5, 12), (7.5, 111.5), (4, 111.5)])
    poly("tip", [(6, 0), (9.5, 6), (9, 11), (7.5, 13.5), (4.5, 13.5), (3, 11), (2.5, 6)])
    ell("hand_r", 3.5, 18, 11.5, 26.5)
    # her left arm out to the side, the shield held clear of the drapery
    poly("arm_l", [(37, 37.5), (42.5, 39), (47, 45), (51.5, 51), (47.5, 54.5), (43, 49.5), (38.5, 45)])
    cx, cy, rx, ry = SHIELD
    ell("shield", cx - rx, cy - ry, cx + rx, cy + ry)
    return lab, regions


def _fold(x, creases):
    """The value step at x across a field of folds: each fold between two
    creases is lit on its left (light from the upper left), its crest a third
    of the way across, falling into shadow toward the next crease."""
    t = 0.5
    for a, b in zip(creases, creases[1:]):
        if a <= x < b:
            t = (x - a) / max(1e-6, b - a)
            break
    for lim, k in ((0.1, 1), (0.22, 4), (0.45, 5), (0.6, 4), (0.78, 3), (0.92, 2), (1.01, 1)):
        if t < lim:
            return k
    return 2


def _promachos_figure():
    """The figure as a 144 x 64 grid of color names (None = clear)."""
    lab, reg = _promachos_masks()
    inv = {v: k for k, v in reg.items()}
    H, W = lab.shape
    G = np.full((H, W), None, object)
    for y in range(H):
        for x in range(W):
            r = inv.get(int(lab[y, x]))
            if not r:
                continue
            k = None
            if r == "crest":
                # horsehair: lit along its outer rim, dark inside and down the tail
                inner = lab[min(H - 1, y + 2), x] != lab[y, x] or (x > 37 and y > 8)
                G[y, x] = "prd" if inner else "pr1"
                continue
            if r == "skirt":
                g = (y - 62) / 48
                cr = [10, 21.5 - 2 * g, 27.5 + 0.5 * g, 33.5 + 3 * g, 39 + 4.5 * g, 60]
                k = _fold(x, cr)
                if x > 37:
                    k -= 1                                  # the shadow side
                if 34 <= x <= 39 and 78 <= y <= 92:
                    k = 5 if 35 <= x <= 37 else 4           # the free knee catches the light
                    if (x, y) in ((36, 83), (36, 84), (35, 84)):
                        k = 6
                if y >= 104 and k > 2:
                    k -= 1                                  # the hem in its own shadow
                if y in (72, 73) and 19 <= x <= 40:
                    k = min(k, 2)                           # the overfold's cast shadow

            elif r == "overfold":
                k = _fold(x, [10, 22, 29, 35.5, 60])
                if x > 36:
                    k -= 1
                bot = 66 + (x - 16) * 0.07 if x < 29 else 71 - (x - 29) * 0.25
                if y >= bot:
                    k = 2 if y >= bot + 1 else 3            # the hem rolls under
            elif r == "torso":
                k = 5 if x < 23 else 4 if x < 30 else 3 if x < 35 else 2
                if y in (51, 52) and (21 <= x <= 26 or 29 <= x <= 34):
                    k -= 1                                  # under the breasts
            elif r == "girdle":
                G[y, x] = "pg2" if x < 29 else "pg1"
                continue
            elif r == "aegis":
                k = 3 if x < 23 else 2 if x < 33 else 1
                if y <= 38 or (y == 39 and x < 30):
                    k += 1                                  # the shoulders lit on top
                if lab[min(H - 1, y + 1), x] != lab[y, x]:
                    G[y, x] = "pg1" if x > 27 else "pg2"    # the snakes' gold rim
                    continue
                if (x - 28) ** 2 + (y - 42.5) ** 2 <= 6.5:
                    G[y, x] = "pg2" if x < 28 else "pg1"    # the gorgoneion
                    if (x, y) in ((27, 42), (29, 42), (28, 44)):
                        G[y, x] = "bz0"
                    continue
            elif r == "arm_r":
                k = 5 if y < 41 + (20 - x) * 0.45 else 4 if y < 44 + (20 - x) * 0.3 else 2
            elif r == "fore_r":
                k = 5 if x < 9.5 + (y - 25) * 0.2 else 4 if x < 12 + (y - 25) * 0.2 else 3
            elif r == "hand_r":
                k = 5 if x < 7 and y < 23 else 4 if x < 9 else 3
                if y == 22 and 4 <= x <= 9:
                    k = 2                                   # the knuckles' line
            elif r == "spear":
                G[y, x] = {4: "bz0", 5: "bz3", 6: "bz1", 7: "bz0"}.get(x, "bz0")
                if y in (12, 13, 14):
                    G[y, x] = {4: "bz0", 5: "pg2", 6: "pg1", 7: "bz0"}.get(x, "bz0")   # the socket
                continue
            elif r == "tip":
                G[y, x] = "pgw" if x < 5 or (x == 5 and y < 10) else "pg2" if x < 7 else "pg1"
                continue
            elif r == "arm_l":
                k = 4 if y < 41 else 3 if x < 44 else 2
            elif r == "shield":
                cx, cy, rx, ry = SHIELD
                d = math.hypot((x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry)
                ul = (x - cx) + (y - cy) * 0.7 < 0
                if d > 0.84:
                    G[y, x] = ("pgw" if (x - cx) + (y - cy) < -14 else "pg2") if ul else "pg1"
                    continue
                if d > 0.76:
                    G[y, x] = "bzd"
                    continue
                k = 4 if (x - cx) + (y - cy) < -10 else 3 if ul or d < 0.5 else 2
            elif r in ("foot_r", "foot_l"):
                k = 5 if x < (21 if r == "foot_r" else 41) else 4
                if y >= 113:
                    k = 3
            if k is not None:
                G[y, x] = RAMP[max(1, min(6, k))]
    # the silhouette: a heavy outline in bronze's darkest
    m = lab > 0
    pad = np.pad(m, 1)
    edge = m & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    tipr = reg["tip"]
    for y, x in zip(*np.nonzero(edge)):
        G[y, x] = ("pg1" if y < 10 and x < 7 else "bz0") if lab[y, x] == tipr else "bz0"
    # inner outlines, a step lighter, where a limb or the shield crosses the body
    front = {reg[n] for n in ("arm_r", "fore_r", "hand_r", "arm_l", "shield", "overfold")}
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            a = int(lab[y, x])
            if a not in front or G[y, x] == "bz0":
                continue
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                b = int(lab[y + dy, x + dx])
                if b and b != a and b != reg["girdle"] and not (a == reg["overfold"] and dy == -1):
                    G[y, x] = "bzd"
                    break
    # the owl, in gold on the shield
    ox, oy = int(SHIELD[0]) - 5, int(SHIELD[1]) - 8
    for j, row in enumerate(OWL):
        for i, ch in enumerate(row):
            if ch != ".":
                G[oy + j, ox + i] = LEG[ch]
    # the head; the helmet (rows 6-17) is gilded, a material apart from the face
    gild = {"3": "g", "2": "G", "1": "m", "g": "w", "G": "g"}
    for j, row in enumerate(HEAD):
        for i, ch in enumerate(row):
            if ch != ".":
                if j <= 11:
                    ch = gild.get(ch, ch)
                G[HEAD_Y + j, HEAD_X + i] = LEG[ch]
    return G


def bronze_safe_marble(P, y0, y1):
    """Keep rows y0..y1-1 of a plinth to the three marble values the bronze
    palette carries (cm5, cm3, cm1), so bronze feet can share its tiles.
    Compares colors, not names: another module may own a marble value's name."""
    swap = {K.C["cm4"]: "cm5", K.C["cm2"]: "cm3", K.C["cm0"]: "cm1"}
    for y in range(y0, y1):
        for x in range(P.w):
            if P.a[y, x, 3]:
                c = swap.get(tuple(int(v) for v in P.a[y, x, :3]))
                if c:
                    P.px(x, y, c)


def plinth_hex(P, x0, x1, top, bottom, shadow="ps", face=7, base=6, shadow_from=None):
    """A hexagonal plinth in 3/4, as in the reference: the lit top face as a
    flattened hexagon (cm5, cm3, cm1 only, so feet in the bronze palette can
    stand on it), a cornice, the die's three faces (west lit, the front with a
    worn inscription, east in shadow), a projecting base course, and the cast
    shadow down and to the right."""
    xa, xb = x0 + 5, x1 - 5                    # the front face's corners
    tf = top + face                            # the top face's front edge
    mid = (tf + bottom) // 2
    for y in range(top, bottom + 1):
        for x in range(x0, x1 + 1):
            c = None
            if y <= tf:
                inset = abs(y - (top + face // 2)) * 5 // 3
                if x0 + inset <= x <= x1 - inset:
                    c = "cm5" if y < top + face // 2 or x < xa + 6 else "cm3" if y < tf else "cm1"
                    if x in (x0 + inset, x1 - inset) or y == top:
                        c = "cm1"
            elif y <= tf + 3:                  # the cornice
                c = ["cm4", "cm3", "cm1"][y - tf - 1]
                if x > xb:
                    c = "cm2" if y < tf + 3 else "cm0"
                if x in (x0, x1):
                    c = "cm0"
            elif y < bottom - base:            # the die
                if x0 + 2 <= x <= x1 - 2:
                    c = "cm4" if x < xa else "cm2" if x > xb else "cm3"
                    if x in (xa, xb):
                        c = "cm1" if x == xb else "cm5"
                    if y == mid and xa + 8 <= x <= xb - 8 and x % 4:
                        c = "cm1"              # the worn inscription
                    if y == mid + 2 and xa + 12 <= x <= xb - 12 and x % 3 == 0:
                        c = "cm2"
                    if x in (x0 + 2, x1 - 2):
                        c = "cm0"
            else:                              # the base course
                yy = y - (bottom - base)
                c = "cm5" if yy == 0 else "cm4" if yy < 2 else "cm3" if yy < 5 else "cm1"
                if x > xb + 2:
                    c = "cm2" if yy < 5 else "cm0"
                if x in (x0, x1) or y == bottom:
                    c = "cm0"
            if c:
                P.px(x, y, c)
    if shadow:
        s0 = top + 6 if shadow_from is None else shadow_from
        for y in range(s0, bottom + 3):
            for x in range(x1 + 1, x1 + 4):
                if (y - s0) // 3 >= x - x1 - 1 and ((x + y) % 2 == 0 or x < x1 + 2):
                    P.px(x, y, shadow)
        for x in range(x0 + 5, x1 + 4):
            if x < x1 - 6 or (x + bottom) % 2 == 0:
                P.px(x, bottom + 1, shadow)


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
    """Athena Promachos, 4 x 9 on borrowed path: the figure on the top layer
    (rows 0-6, walk T: the player walks behind her), the hexagonal plinth on
    the middle layer (rows 7-8, solid) with her feet standing on its top.
    Animation 'glint': a sparkle runs down the gold spear tip (cell r0c0)."""
    W, H = 4, 9
    L = canvas(W, H)
    P = canvas(W, H)
    plinth_hex(P, 1, 59, 110, 141)
    # the tile row her feet share with the plinth (y 112-119) keeps to the
    # three marble values the bronze palette carries
    bronze_safe_marble(P, 112, 120)
    G = _promachos_figure()
    for y in range(G.shape[0]):
        for x in range(G.shape[1]):
            if G[y, x]:
                (L if y < 112 else P).px(x, y, G[y, x])
    # her shadow on the plinth's top, falling right of her feet
    for (x0, x1, y) in ((28, 31, 113), (48, 51, 114), (28, 30, 114), (48, 50, 115)):
        for x in range(x0, x1 + 1):
            if P.get(x, y) in ("cm5", "cm3"):
                P.px(x, y, "cm1" if y == 113 or x % 2 else "cm3")
    # the plinth's top in rows 110-111 sits in row 6, on the top layer
    for y in range(110, 112):
        for x in range(64):
            if P.get(x, y) and not L.get(x, y):
                L.px(x, y, P.get(x, y))
            P.px(x, y, None)
    frames = []
    if anim:
        for f in range(3):
            F = canvas(W, H)
            pts = [((5, 3), (4, 4), (6, 4), (5, 5)),
                   ((5, 0), (5, 1), (2, 3), (9, 3), (3, 3), (8, 3), (5, 4), (5, 5), (4, 2), (6, 2),
                    (4, 4), (6, 4)),
                   ((5, 8), (4, 9), (6, 9), (5, 10))][f]
            for (x, y) in pts:
                F.px(x, y, "pg2" if (x, y) in ((2, 3), (9, 3)) else "cm5")
            frames.append(("top", F))
    walk = ["TTTT"] * 7 + ["XXXX"] * 2
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    s = cut(key, "Athena Promachos", W, H, {"middle": P, "top": L}, walk, names=names,
            notes="Athena Promachos, bronze, 4 x 9 on borrowed path, in contrapposto: the spear raised "
                  "in her right fist, held clear of her body, its gold tip the gleam sailors saw from "
                  "Sounion (animation `glint` on r0c0); the owl shield held out on her left arm; the "
                  "Corinthian helmet pushed back on her crown with its red crest, showing her face; the "
                  "aegis with the gorgoneion; the peplos in four big folds, the free knee lit. Rows 0-6 "
                  "are drawn over the player (T); rows 7-8 are the hexagonal marble plinth in 3/4 with "
                  "its cast shadow (X).",
            anims={"glint": frames} if anim else None)
    if anim:
        K.settle(s, "glint", [(0, 0)])
    return s


HERO_LEGEND = LEG

KODROS = [
    # King Kodros, the last king: bearded, in the plain cloak he wore to go out
    # as a woodcutter, folds falling across him; the spear he walked onto held
    # reversed, its gold point down; the crown he set aside at his feet
    "..........#####.........",
    ".........#3322m#........",
    "........#3d322d1#.......",
    "........#3#232#1#.......",
    "....###.#3323m1d#.......",
    "....#3#.#3dddd1d#.......",
    "....#3#..#3m2m1#........",
    "....#3#..#33m21#........",
    "....#3#...#2m1#.........",
    "....#3#.##33322##.......",
    "....#3###33332221d#.....",
    "....#3#33#33322221d#....",
    "...#33#3##333222m1d#....",
    "...#33##.#3m33222m1d#...",
    "....#3#..#3mm3322m11#...",
    "....#3#..#33mm33m2m1d#..",
    "....#3#..#323mm33m21d#..",
    "....#3#..#3223mm33m1#d#.",
    "....#3#..#32223mm3m1#2#.",
    "....#3#..#322223mm31##..",
    "....#3#..#32222m3m31#...",
    "....#3#..#3222m2m231#...",
    "....#3#..#322m2m2m21#...",
    "....#3#..#32m2m2m2m1#...",
    "....#3#..#3m2m2m2m21#...",
    "....#3#..#3m2m2m2m21#...",
    "....#3#...#3m2##m21#....",
    "....#3#...#32#..#21#....",
    "....#G#...#32#..#21#....",
    "...#gwG#..#32#..#21#....",
    "...#ggG#.#332#..#211#gGg",
    "....#G#..#####..#####Gw#",
]

KAIROS = [
    # Kairos, the Moment: a running youth, the forelock to seize him by blown
    # forward and the nape shaven behind; the razor in his raised left hand
    # with a balance on its edge; wings at his heels
    ".......####.............",
    "....###3332#............",
    "...#33#33221#...........",
    "....##3d2d1d#...........",
    "......#3#2#1#...........",
    "......#3323d#...........",
    "......#32dd1#...........",
    ".......#3211#...........",
    "........#21#............",
    "......##33221##.....#gg#",
    ".....#33#33221d#...#gwG#",
    "....#33##332221d#.#G#G#.",
    "...#33#.#3332221d#G##...",
    "..#33#..#33322m1#d#.....",
    ".#33#...#3332m21#d#.....",
    "#33#....#333m221#.......",
    "#3#.....#33m2221#.......",
    ".#......#3m22m1#........",
    ".......#33m22m1d#.......",
    "......#33m2##m21d#......",
    ".....#33m2#..#m21d#.....",
    "....#33m2#....#m21d#....",
    "...#33m2#......#m21d#...",
    "..#33m2#........#m21d#..",
    "..#3m2#..........#m21#..",
    ".#3m2#............#m21#.",
    ".#3m#..............#m1#.",
    "#g3#...............#21#.",
    "#wg#..............#g21#.",
    "#gg#.............#gwm1#.",
    ".##..............#gg11#.",
    "..................#####.",
]


def hero_statue(key, figure, title, on="path", stone="marble"):
    """A bronze statue on a hexagonal plinth, 2 x 3 on borrowed ground: the
    figure on the top layer (rows 0-1, walk T) and the plinth in 3/4 with its
    cast shadow on the middle layer (row 2, solid), the feet standing on it."""
    W, H = 2, 3
    T = canvas(W, H)
    P = canvas(W, H)
    plinth_hex(P, 2, 27, 31, 45, shadow=AA.CK.SHADOW.get(on, "ps"), face=4, base=4, shadow_from=40)
    bronze_safe_marble(P, 31, 40)              # the tile row the feet share
    for x in range(32):                         # the plinth's back edge sits in row 1
        if P.get(x, 31):
            T.px(x, 31, P.get(x, 31))
        P.px(x, 31, None)
    for j, rowstr in enumerate(figure):
        assert len(rowstr) == 24, (key, j, len(rowstr))
        for i, ch in enumerate(rowstr):
            c = LEG.get(ch)
            if c:
                y = 1 + j
                (T if y < 32 else P).px(4 + i, y, c)
    return cut(key, title, W, H, {"middle": P, "top": T}, ["TT", "TT", "XX"],
               names={"TL": (0, 0), "TR": (1, 0), "ML": (0, 1), "MR": (1, 1), "BL": (0, 2), "BR": (1, 2)},
               on=on, section="town",
               notes=f"{title} (2 x 3): bronze on a hexagonal 3/4 marble plinth, its cast shadow on the "
                     "floor. Rows 0-1 over the player, the plinth solid; the bg event is on the plinth.")
