"""Olympanax (#149), the Sky Lord: Zeus's lot of the broad sky.

Direction B, "The Elemental Titans". The Cyclopes forged one war-gear for
the three sons of Kronos: the same Corinthian helm and muscled cuirass. Inside
Olympanax's gear the body is the storm itself. A thunderhead fills the gold
cuirass and boils out of its joints, it spreads cloud-eagle wings with
feathered storm edges, its lower body twists down into a storm funnel, and
the crest of its helm is living lightning. Its far forearm is the
thunderbolt: past the gold vambrace the arm is a forking bolt striking down.
It has no face, only its lot's emblem, a bolt, glowing gold-white in the T of
the visor.
"""
import math

from mon_lib import Mat, Mon, bez, bez3, ellipse_pts, ribbon

COLORS = [
    ("ink", (24, 16, 40)),
    # the thunderhead: storm indigo up to a lightning-lit white
    ("k0", (40, 40, 80)), ("k1", (72, 80, 128)), ("k2", (112, 128, 176)), ("k3", (168, 184, 224)),
    ("k4", (232, 240, 248)),
    # the Cyclopes' gold
    ("g0", (104, 56, 24)), ("g1", (168, 104, 32)), ("g2", (224, 160, 48)), ("g3", (248, 208, 96)),
    ("g4", (248, 240, 184)),
    # lightning
    ("y", (248, 248, 104)), ("e0", (64, 88, 200)), ("e1", (136, 192, 248)),
    ("e2", (96, 64, 152)),
]
# The shiny is a storm at night: the thunderhead goes to midnight, the gold to
# pale silver and the lightning to Aegean blue.
SHINY = {
    "k0": (24, 24, 48), "k1": (48, 48, 88), "k2": (80, 88, 136), "k3": (128, 144, 192), "k4": (208, 224, 248),
    "g0": (72, 80, 104), "g1": (128, 136, 160), "g2": (184, 192, 208), "g3": (224, 232, 240), "g4": (248, 248, 248),
    "y": (120, 216, 248), "e0": (40, 96, 200), "e1": (176, 232, 248), "e2": (56, 64, 152),
}

cloud = Mat(["k0", "k1", "k2", "k3"], line="k0", cuts=[0.2, 0.44, 0.7])
gold = Mat(["g0", "g1", "g2", "g3"], line="g0", cuts=[0.2, 0.44, 0.7])
gold_hi = Mat(["g0", "g1", "g2", "g3", "g4"], line="g0", cuts=[0.16, 0.36, 0.56, 0.8])
bolt_m = Mat(["y", "k4"], line="y", outline="ink", cuts=[0.5])


# --------------------------------------------------------------------------
# The helm: one Corinthian helm for the three brothers, 3/4 view facing left.
# Tones 0-4 run dark to light; v is the dark of the T; b is the rim bead.
# The god's emblem is painted into the T over the v pixels (c core, h halo).
# --------------------------------------------------------------------------

HELM = [
    "......#####.......",
    "....##44433##.....",
    "...#444443332#....",
    "..#34444333221#...",
    "..#33443333221#...",
    ".#bbbbbbbbbb3211#.",
    ".#vvvvvvvvvv2110#.",
    "#2vvvvvvvvvv21100#",
    "#3vvvvvvvvv221100#",
    "#23vvvvvvv3221100#",
    ".#23vvvv2b3211000#",
    ".#232vv2b32110000#",
    ".#232vv2b3211#000#",
    ".#122vv2b211#.#00#",
    "..#12vv2b210#..##.",
    "..#11#vv#b1#......",
    "...##..#.##.......",
]
# Zeus's lot: a bolt, white-hot in an electric-yellow halo
BOLT = [
    "", "", "", "", "", "",
    "..........cc",
    "........ccch",
    "......cccc",
    "...hcccch",
    ".....hcc",
    ".....cch",
    ".....hc",
    "......c",
    "......h",
]
HELM_LEGEND = {"#": "ink", "v": "ink", "0": "g0", "1": "g1", "2": "g2", "3": "g3", "4": "g4", "b": "g4",
               "c": "k4", "h": "y"}


def helm_rows(glyph=BOLT):
    rows = [list(r) for r in HELM]
    for j, r in enumerate(glyph):
        for i, ch in enumerate(r):
            if ch in "ch" and j < len(rows) and i < len(rows[j]) and rows[j][i] == "v":
                rows[j][i] = ch
    return ["".join(r) for r in rows]


def helm(p, x, y):
    """The helm with its top-left at (x, y). Drawn small, a gold dome with a
    dark T and a hot point for the bolt."""
    if p.big:
        p.patch(x, y, helm_rows(), HELM_LEGEND)
        return
    p.poly([(x + 3, y + 3), (x + 9, y), (x + 15, y + 3), (x + 17, y + 13), (x + 13, y + 16), (x + 3, y + 16),
            (x + 0.5, y + 8)], gold, group=90)
    p.stroke([(x + 2, y + 7), (x + 10, y + 7)], "ink")
    p.stroke([(x + 5.5, y + 8), (x + 5.5, y + 15)], "ink")
    p.px(x + 6, y + 8, "k4")


# --------------------------------------------------------------------------
# Shapes
# --------------------------------------------------------------------------

def path(*segs):
    out = []
    for s in segs:
        if out and s and out[-1] == s[0]:
            s = s[1:]
        out.extend(s)
    return out


def bolt(p, pts, w0, w1, mat, **kw):
    """A zigzag ribbon with sharp elbows, tapering to a point on its last leg."""
    n = len(pts) - 1
    polys = [ellipse_pts(pts[0][0], pts[0][1], p._minw(w0) / 2, p._minw(w0) / 2, n=12)]
    for i in range(n):
        a, b = pts[i], pts[i + 1]
        wa = p._minw(w0 + (w1 - w0) * i / n)
        wb = p._minw(w0 + (w1 - w0) * (i + 1) / n)
        if i == n - 1:
            polys.append(ribbon([a, b], lambda t, wa=wa: wa * (1 - t) + 0.25 * t))
        else:
            polys.append(ribbon([a, b], lambda t, wa=wa, wb=wb: wa + (wb - wa) * t))
            polys.append(ellipse_pts(b[0], b[1], wb / 2, wb / 2, n=4))
    return p.add(p.mask(*polys), mat, **kw)


billow_m = Mat(["k0", "k1", "k2", "k3", "k4"], line="k0")


def billow(p, cx, cy, r, group, dark=0, under=False):
    """One storm billow with crisp toon shading: an indigo underside, a slate
    body and a lit cap toward the upper left. dark (0-2) drops every band."""
    lv = [max(0, v - dark) for v in (0, 1, 3, 4)]
    base = p.circle(cx, cy, r, billow_m, flat=lv[0], group=group, under=under)
    if not base:
        return 0
    if not p.big and r < 3:
        p.circle(cx - 0.2 * r, cy - 0.3 * r, r * 0.8, billow_m, flat=lv[2], clip=[base], noline=True, group=group)
        return base
    mid = p.circle(cx - 0.16 * r, cy - 0.22 * r, r * 0.92, billow_m, flat=lv[1], clip=[base], noline=True,
                   group=group)
    body = p.circle(cx - 0.32 * r, cy - 0.4 * r, r * 0.78, billow_m, flat=lv[2], clip=[base, mid], noline=True,
                    group=group)
    if r >= 3.0 and lv[3] > lv[2]:
        p.circle(cx - 0.52 * r, cy - 0.6 * r, r * 0.46, billow_m, flat=lv[3], clip=[body], noline=True, group=group)
    return base


feather_m = Mat(["ink", "k0", "k1", "k2", "k3"], line="k0")


def paddle(p, a, b, w, group, tone=2, bend=0.0):
    """A storm feather from root a to a rounded tip at b: a dark body with a
    lit stripe along its upper-left edge. tone is the body's level in
    feather_m (1 darkest .. 3)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    path_ = []
    for i in range(7):
        t = i / 6
        off = bend * math.sin(math.pi * t)
        path_.append((a[0] + dx * t - dy / d * off, a[1] + dy * t + dx / d * off))
    base = p.limb(path_, w * 0.5, w, feather_m, group=group, flat=tone)
    if not base or not p.big:
        return base
    nx, ny = -dy / d, dx / d
    if nx + ny > 0:
        nx, ny = -nx, -ny          # the edge facing the light
    o = 0.3 * w
    lit = [(x + nx * o, y + ny * o) for x, y in path_]
    p.limb(lit, w * 0.3, w * 0.55, feather_m, group=group, flat=min(4, tone + 1), clip=[base], noline=True)
    return base


def storm_wing(p, wrist, prim, sec, cov, bank, group, dark=0):
    """A cloud-eagle wing raised high: finger primaries splayed from the
    wrist, secondaries hung along the arm, a row of coverts over their
    roots, and a bank of lit billows along the leading edge."""
    for k, (b, w, bend) in enumerate(prim):
        paddle(p, wrist, b, w, group + k, tone=2 - dark, bend=bend)
    for k, (a, b, w, bend) in enumerate(sec):
        paddle(p, a, b, w, group + 10 + k, tone=2 - dark, bend=bend)
    for k, (a, b, w, bend) in enumerate(cov):
        paddle(p, a, b, w, group + 20 + k, tone=3 - dark, bend=bend)
    for k, (cx, cy, r) in enumerate(bank):
        billow(p, cx, cy, r, group + 30 + k, dark=dark)


# --------------------------------------------------------------------------
# Battle front: 3/4 view facing left, floating high on its storm funnel
# --------------------------------------------------------------------------

def _front_wings(p, phase):
    # ---- far wing (left of frame): raised behind the helm, in the storm's shadow
    storm_wing(p, (12, 8),
               prim=[((17.5, 3.4), 3.6, -0.3), ((12.5, 3.2), 4.0, 0.0), ((8.2, 3.6), 4.2, 0.4),
                     ((4.8, 5.4), 4.2, 0.6), ((3.8, 11), 4.2, 0.6)],
               sec=[((11.5, 12), (4.0, 18), 4.8, 0.8), ((13.5, 16), (4.2, 25), 5.2, 0.9),
                    ((15.5, 20), (6.4, 32), 5.2, 0.9), ((18.5, 23), (9.5, 35.5), 5.0, 0.8),
                    ((21.5, 26), (15, 37), 4.4, 0.6)],
               cov=[((12.5, 11), (7.5, 15), 3.8, 0.5), ((14.5, 15), (8.5, 21), 4.0, 0.6),
                    ((16.5, 19), (11, 26), 4.0, 0.6), ((19.5, 22.5), (14.5, 29.5), 3.8, 0.5)],
               bank=[(21.5, 22.5, 4.2), (17, 19, 3.6), (18.5, 15.5, 3.6), (14, 13.5, 3.2), (15.5, 10.5, 3.2), (12.4, 7.6, 2.8)],
               group=10, dark=1)
    # ---- near wing (right of frame): spread up and out
    storm_wing(p, (52, 8),
               prim=[((46.5, 3.4), 3.8, 0.3), ((51.5, 3.2), 4.2, 0.0), ((56.2, 3.6), 4.6, -0.4),
                     ((60, 5.0), 4.6, -0.6), ((60.8, 11), 4.6, -0.6)],
               sec=[((52.5, 12), (60.8, 18), 5.0, -0.8), ((50.5, 16), (60.6, 25), 5.4, -0.9),
                    ((48.5, 20), (58.4, 32), 5.4, -0.9), ((45.5, 23), (54.5, 36), 5.2, -0.8),
                    ((42.5, 26), (48.5, 38), 4.6, -0.6)],
               cov=[((51.5, 11), (56.5, 15), 4.0, -0.5), ((49.5, 15), (55.5, 21), 4.2, -0.6),
                    ((47.5, 19), (53, 26), 4.2, -0.6), ((44.5, 22.5), (49.5, 29.5), 4.0, -0.5)],
               bank=[(42, 22.5, 4.6), (47, 19.5, 4.0), (45.2, 16.2, 4.2), (50.5, 14.5, 3.6), (48.6, 11.2, 3.6), (51.6, 7.6, 3.0)],
               group=40)


def _front_body(p, phase):
    ph = phase
    big = p.big
    # ---- far arm (left of frame): cloud upper arm, gold vambrace, and past it the arm is the bolt
    billow(p, 13.8, 31.6, 4.4, 70)
    p.limb([(11, 35.5), (9.4, 40.5)], 5.8, 5.2, gold, group=71)
    p.limb([(11.3, 34.4), (11.5, 35.8)], 7.0, 7.0, gold_hi, group=72)         # the vambrace's flared cuff
    bolt(p, [(9.4, 41), (13.6, 46.4), (7.4, 50.4), (10.6, 53.4), (4.4, 60.5)], 5.2, 3.0, bolt_m, group=73)
    bolt(p, [(12.8, 46.6), (17.6, 49.8), (16.2, 53.8)], 2.8, 1.6, bolt_m, group=74)
    bolt(p, [(8.2, 50.6), (3.6, 51.4), (2.6, 55.4)], 2.6, 1.4, bolt_m, group=75)

    # ---- the storm funnel: bands twisting down to a point that trails back
    bands = [
        [(28, 53.5), (34, 54), (38.5, 53), (39, 55.5), (37.5, 58.5), (35.5, 56.5), (31, 55.5)],
        [(23, 49), (30, 51.5), (37, 51), (40.5, 49), (40, 53), (35.5, 55), (29, 54.5), (25, 52)],
        [(19, 44.5), (27, 47.5), (36, 47.5), (42, 45), (41.5, 49.5), (36.5, 52), (28, 52), (21.5, 49)],
    ]
    for k, band in enumerate(bands):
        p.poly(band, cloud, group=80 + k, bias=0.2 - 0.06 * k)
    for k, (cx, cy, r, dk) in enumerate(((40.5, 43.4, 3.4, 1), (20, 43, 3.8, 0), (25.5, 44.6, 4.0, 0),
                                         (33.5, 45, 4.2, 0), (29, 43.2, 3.4, 0))):
        billow(p, cx, cy, r, 85 + k, dark=dk)

    # ---- storm boiling out at the neck
    billow(p, 23, 21.4, 3.6, 95)
    billow(p, 32.5, 21.4, 3.6, 96, dark=1)

    # ---- the cuirass: a muscled gold shell, pecs and belly worked in relief
    p.poly(path(bez3((19.5, 24.5), (23, 22.5), (32, 22.5), (38.5, 24.5)), bez3((38.5, 24.5), (41, 29), (39, 34), (38.5, 40)),
                bez((38.5, 40), (29, 42.5), (19.5, 40)), bez3((19.5, 40), (19.5, 35), (17, 29.5), (19.5, 24.5))),
           gold_hi, group=100, bias=0.08)
    if big:
        p.blob(23.4, 27.6, 4.2, 3.4, gold_hi, group=101, noline=True, bias=-0.04)    # far pec
        p.blob(31.6, 27.8, 5.6, 3.8, gold_hi, group=102, noline=True, bias=-0.02)    # near pec
        for k, (cx, cy, rx, ry) in enumerate(((25.2, 33.6, 2.2, 1.8), (30.8, 33.8, 2.8, 1.8), (25.6, 36.6, 2.0, 1.4),
                                              (30.8, 36.8, 2.6, 1.4))):
            p.blob(cx, cy, rx, ry, gold_hi, group=103 + k, noline=True, bias=0.0)
        p.shade([(36, 22), (42, 26), (42, 41), (36, 41)], 0.1)         # the turning side
    # the hem: a chased meander band
    p.poly(path(bez((19.2, 38.6), (29, 41.2), (38.8, 38.6)), [(39, 41)], bez((39, 41), (29, 43.6), (19, 41))),
           gold, group=112, bias=0.1)

    # ---- near arm (right of frame): cloud upper arm, vambrace, gauntlet fist
    billow(p, 45.5, 32.5, 4.2, 120)
    p.limb([(48, 36.5), (50.2, 42)], 5.8, 5.4, gold, group=121)
    p.limb([(47.6, 35.4), (48.0, 36.8)], 7.0, 7.0, gold_hi, group=122)
    p.blob(51, 45.4, 4.0, 3.6, gold_hi, group=123)

    # ---- pauldrons: three lames each
    p.blob(45, 30.6, 3.6, 2.2, gold, ang=36, group=130)
    p.blob(43.4, 28.2, 4.6, 2.6, gold, ang=30, group=131)
    p.blob(41.2, 24.8, 5.6, 3.8, gold_hi, ang=20, group=132)
    p.blob(15.8, 27.8, 3.8, 2.2, gold, ang=-32, group=133, bias=0.06)
    p.blob(17.6, 24.8, 4.6, 3.4, gold_hi, ang=-20, group=134, bias=0.04)

    # ---- the crest: living lightning arching back over the helm
    crest = path(bez3((20.5, 9), (20, 3), (25, 1.4), (31, 1.4)), bez3((31, 1.4), (39, 1.6), (46, 6), (49, 16)),
                 [(46.5, 17)], bez3((46.5, 17), (43, 11), (38, 7.5), (31, 6.5)), [(24, 8.5)])
    p.poly(crest, bolt_m, group=140, flat=0)
    if big:
        p.stroke([(22, 6), (25, 3), (29, 3.5), (33, 2.5), (38, 4.5), (41, 4), (44, 8), (46, 9), (47, 14)], "k4")
    helm(p, 20, 6 - ph)


# --------------------------------------------------------------------------
# Battle back: over the shoulder, helm turned right in profile, bolt raised
# --------------------------------------------------------------------------

# The helm in right profile, for the back view (tones as HELM): the dome,
# the brow bead, the eye slot with the god's light in it, the long cheek
# guard sweeping down to the chin, the ear notch and the flared nape guard.
HELM_SIDE = [
    "......######.......",
    "....##444333##.....",
    "...#4444443332#....",
    "..#344444333322#...",
    "..#334444333222#...",
    ".#23344433332221#..",
    ".#22333333332221#..",
    ".#122333333bbbbbb#.",
    ".#12233333#hccccc#.",
    ".#1122333332#hch#..",
    ".#11223333332##21#.",
    ".#011222333221112#.",
    ".#0111222322111112#",
    ".#00111222#1211112#",
    ".#0011112#.#21111#.",
    "#00#0011#..#2111#..",
    "#0#.#00#...#2111#..",
    "##..##.....#b111#..",
    "...........#b11#...",
    "............#b1#...",
    ".............##....",
]


def helm_side(p, x, y):
    """The helm in right profile with its top-left at (x, y)."""
    if p.big:
        p.patch(x, y, HELM_SIDE, HELM_LEGEND)
        return
    p.poly([(x + 2, y + 15), (x + 2, y + 5), (x + 9, y), (x + 16, y + 4), (x + 18, y + 13), (x + 15, y + 20),
            (x + 12, y + 14), (x + 6, y + 17)], gold, group=200)
    p.px(x + 14, y + 8, "k4")


def _back_wings(p, phase):
    # ---- wings, vast, spread up from the shoulder blades
    storm_wing(p, (12, 9),
               prim=[((17, 2.2), 4.4, -0.3), ((11, 1.8), 4.8, 0.0), ((5.4, 3.6), 5.0, 0.4),
                     ((2.6, 9.6), 5.0, 0.6), ((2.2, 16.5), 4.8, 0.6)],
               sec=[((12, 15), (2.6, 23), 5.6, 0.8), ((14, 20), (3.0, 31), 6.0, 0.9),
                    ((16.5, 25), (4.6, 39), 6.0, 0.9), ((19, 30), (8.5, 46), 5.8, 0.8)],
               cov=[((13.5, 13), (8, 18), 4.4, 0.5), ((15.5, 18), (9, 25), 4.6, 0.6),
                    ((18, 24), (12, 32), 4.6, 0.6)],
               bank=[(23, 40, 5.0), (20.5, 33, 4.6), (18, 26, 4.4), (15.5, 19, 4.0), (13, 12.5, 3.4)],
               group=10)
    storm_wing(p, (47, 11),
               prim=[((42, 3.2), 4.0, 0.3), ((47.5, 2.4), 4.4, 0.0), ((53, 3.6), 4.6, -0.4)],
               sec=[((49, 16), (59.6, 18), 5.0, -0.8), ((48, 21), (60.2, 28), 5.6, -0.9),
                    ((46, 26), (58.6, 37), 5.6, -0.9), ((43.5, 31), (52.5, 42), 5.4, -0.8)],
               cov=[((47, 15), (53, 19), 4.0, -0.5), ((45.5, 20), (52, 26), 4.2, -0.6)],
               bank=[(41.5, 36, 4.6), (43.5, 29, 4.4), (45.5, 22, 4.0), (47, 16, 3.6), (47, 11.5, 3.0)],
               group=40, dark=1)


def _back_body(p, phase):
    # ---- the far arm hanging, cropped by the frame
    billow(p, 12, 56, 4.4, 60)
    p.limb([(10.5, 59), (9.6, 64)], 6.4, 6.2, gold, group=61, bias=0.06)
    # ---- the storm boiling up around the shoulders and neck
    for k, (cx, cy, r) in enumerate(((20, 47, 4.6), (27, 44.5, 4.8), (35, 44, 4.6), (42.5, 46, 4.4))):
        billow(p, cx, cy, r, 62 + k)
    # ---- the back plate: shoulder blades and spine, cropped by the frame
    p.poly(path(bez3((16, 54), (18, 50), (25, 48.5), (31, 48.5)), bez3((31, 48.5), (38, 48.5), (44, 50), (46, 54)),
                [(45.5, 64), (16.5, 64)]), gold_hi, group=70)
    if p.big:
        p.blob(24.5, 55, 6.0, 4.8, gold_hi, group=71, noline=True, bias=-0.02)
        p.blob(37.5, 55, 5.6, 4.6, gold_hi, group=72, noline=True, bias=0.04)
    # ---- pauldrons
    p.blob(17, 52, 5.4, 3.8, gold_hi, ang=-24, group=80)
    p.blob(45.5, 51.5, 5.0, 3.6, gold, ang=24, group=81)
    # ---- the bolt arm raised: cloud, vambrace, and the arm is lightning
    billow(p, 51.5, 45, 4.4, 90)
    p.limb([(54.6, 40), (57, 32.5)], 6.0, 5.6, gold, group=91)
    p.limb([(54.4, 41.2), (54.2, 39.6)], 7.2, 7.2, gold_hi, group=92)
    bolt(p, [(57.2, 32), (54.2, 25.5), (59.6, 19.5), (55.8, 13), (59.6, 3.6)], 5.4, 3.0, bolt_m, group=93)
    # ---- the crest arching back over the helm, and the helm in profile
    p.poly(path(bez3((43.5, 21.5), (44, 13), (38, 10.6), (33, 11)), bez3((33, 11), (26, 11.6), (22, 17), (20, 27)),
                [(23, 28)], bez3((23, 28), (25, 21), (29, 17.5), (35, 18)), [(41, 22)]), bolt_m, group=100, flat=0)
    helm_side(p, 29, 20 - phase)


def _back(p, phase):
    _back_wings(p, phase)
    _back_body(p, phase)


def _front(p, phase):
    _front_wings(p, phase)
    _front_body(p, phase)


# --------------------------------------------------------------------------
# Follower views
# --------------------------------------------------------------------------

def _follow_wing(p, side, phase, dark=0, group=10):
    """A raised storm wing for the follower: side -1 is the left of frame."""
    beat = 1.5 * phase
    cx = 32 + side * 9
    tips = [(32 + side * 24, 11 - beat), (32 + side * 22, 5 - beat), (32 + side * 16, 4 - beat),
            (32 + side * 25, 18 - beat), (32 + side * 23, 26)]
    for k, t in enumerate(tips):
        paddle(p, (cx + side * 4, 20), t, 6.0, group + k, tone=2 - dark, bend=-0.6 * side)
    for k, (dx, dy, r) in enumerate(((4, 22, 5.0), (9, 16, 4.6), (14, 11 - beat, 4.0))):
        billow(p, cx + side * dx, dy, r, group + 10 + k, dark=dark)


def _down(p, phase):
    bob = phase
    _follow_wing(p, -1, phase, group=10)
    _follow_wing(p, 1, phase, group=30)
    # funnel
    p.poly([(21, 44 + bob), (43, 44 + bob), (36, 53 + bob), (32, 58 + bob), (28, 53 + bob)], cloud, group=50, bias=0.1)
    billow(p, 25, 45 + bob, 4.4, 51)
    billow(p, 39, 45 + bob, 4.4, 52)
    billow(p, 32, 47 + bob, 4.6, 53)
    # cuirass, face-on
    p.poly(path(bez3((20, 28 + bob), (26, 25 + bob), (38, 25 + bob), (44, 28 + bob)),
                bez3((44, 28 + bob), (46, 36 + bob), (42, 42 + bob), (42, 45 + bob)),
                bez((42, 45 + bob), (32, 48 + bob), (22, 45 + bob)),
                bez3((22, 45 + bob), (22, 42 + bob), (18, 36 + bob), (20, 28 + bob))), gold_hi, group=60)
    p.rect(21, 42 + bob, 42, 44 + bob, gold, group=61)
    p.blob(18, 29 + bob, 5, 4, gold_hi, group=62)
    p.blob(46, 29 + bob, 5, 4, gold_hi, group=63)
    # arms: the bolt arm on the left of frame, a fist on the right
    p.limb([(16, 33 + bob), (14, 41 + bob)], 6, 5.4, gold, group=64)
    bolt(p, [(14, 42 + bob), (17, 47 + bob), (12, 51 + bob), (15, 57)], 4.6, 2.8, bolt_m, group=65)
    p.limb([(48, 33 + bob), (50, 41 + bob)], 6, 5.4, gold, group=66)
    p.blob(50.5, 44 + bob, 3.8, 3.4, gold_hi, group=67)
    # helm face-on, crest above
    p.poly([(30, 12 + bob), (32, 3 + bob), (34, 12 + bob)], bolt_m, group=70, flat=0)
    p.poly([(23, 16 + bob), (26, 10 + bob), (32, 8 + bob), (38, 10 + bob), (41, 16 + bob), (41, 25 + bob),
            (35, 28 + bob), (29, 28 + bob), (23, 25 + bob)], gold_hi, group=71)
    p.rect(25, 15 + bob, 38, 17 + bob, Mat(["ink"]), group=72, flat=0, noline=True)
    p.rect(31, 18 + bob, 33, 27 + bob, Mat(["ink"]), group=73, flat=0, noline=True)
    p.stroke([(29, 16 + bob), (35, 16 + bob)], "k4")
    p.stroke([(32, 18 + bob), (32, 25 + bob)], "y")
    p.px(32, 17 + bob, "k4")


def _up(p, phase):
    bob = phase
    _follow_wing(p, -1, phase, group=10)
    _follow_wing(p, 1, phase, group=30)
    p.poly([(21, 44 + bob), (43, 44 + bob), (36, 53 + bob), (32, 58 + bob), (28, 53 + bob)], cloud, group=50, bias=0.1)
    billow(p, 25, 45 + bob, 4.4, 51)
    billow(p, 39, 45 + bob, 4.4, 52)
    billow(p, 32, 47 + bob, 4.6, 53)
    # back plate
    p.poly(path(bez3((20, 28 + bob), (26, 25 + bob), (38, 25 + bob), (44, 28 + bob)),
                bez3((44, 28 + bob), (46, 36 + bob), (42, 42 + bob), (42, 45 + bob)),
                bez((42, 45 + bob), (32, 48 + bob), (22, 45 + bob)),
                bez3((22, 45 + bob), (22, 42 + bob), (18, 36 + bob), (20, 28 + bob))), gold_hi, group=60)
    p.rect(21, 42 + bob, 42, 44 + bob, gold, group=61)
    if p.big:
        p.stroke([(32, 29 + bob), (32, 41 + bob)], "g1")
    p.blob(18, 29 + bob, 5, 4, gold_hi, group=62)
    p.blob(46, 29 + bob, 5, 4, gold_hi, group=63)
    p.limb([(16, 33 + bob), (14, 41 + bob)], 6, 5.4, gold, group=64)
    p.limb([(48, 33 + bob), (50, 41 + bob)], 6, 5.4, gold, group=66)
    bolt(p, [(50, 42 + bob), (47, 47 + bob), (52, 51 + bob), (49, 57)], 4.6, 2.8, bolt_m, group=65)
    # the back of the helm: dome and flared nape guard, the crest running down it
    p.poly([(23, 16 + bob), (26, 10 + bob), (32, 8 + bob), (38, 10 + bob), (41, 16 + bob), (43, 26 + bob),
            (37, 27 + bob), (27, 27 + bob), (21, 26 + bob)], gold_hi, group=71)
    p.limb([(32, 4 + bob), (32, 22 + bob)], 4.0, 2.4, bolt_m, group=72, flat=0)
    if p.big:
        p.stroke([(32, 4 + bob), (32, 20 + bob)], "k4")


def _icon(p, phase):
    """Party icon: a compact bust, the helm large so the bolt in the T reads."""
    ox, oy = 17, 18
    up = phase
    for side in (-1, 1):
        cx = ox + 15 + side * 7
        for k, (tx, ty) in enumerate(((ox + 15 + side * 15, oy + 11 - up), (ox + 15 + side * 14, oy + 4 - up),
                                      (ox + 15 + side * 10, oy + 1 - up))):
            paddle(p, (cx, oy + 13), (tx, ty), 4.4, 10 + k + (5 if side > 0 else 0), tone=2)
        billow(p, cx + side * 2, oy + 10, 3.4, 20 + side)
    p.poly([(ox + 8, oy + 20), (ox + 22, oy + 20), (ox + 21, oy + 27.6), (ox + 9, oy + 27.6)], gold_hi, group=30)
    p.blob(ox + 7.5, oy + 21, 3.6, 3.0, gold_hi, group=31)
    p.blob(ox + 22.5, oy + 21, 3.6, 3.0, gold_hi, group=32)
    bolt(p, [(ox + 5, oy + 22), (ox + 3.4, oy + 24.5), (ox + 5, oy + 25.5), (ox + 2.6, oy + 28)], 2.6, 1.6, bolt_m, group=33)
    p.limb(bez3((ox + 8.5, oy + 8), (ox + 9, oy + 1.5), (ox + 20, oy + 0.6), (ox + 25, oy + 9 - up)), 3.0, 2.0, bolt_m,
           group=34)
    helm(p, ox + 6, oy + 5 - up)


def olympanax(p, view, phase):
    if view == "icon":
        _icon(p, phase)
    elif view in ("front", "side"):
        _front(p, phase)
    elif view == "back":
        _back(p, phase)
    elif view == "down":
        _down(p, phase)
    elif view == "up":
        _up(p, phase)


MONS = [
    # icon palette 3 keeps the storm blue and the gold warm
    Mon("Olympanax", COLORS, SHINY, olympanax, foot="blank", icon_pal=3),
]
