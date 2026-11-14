"""Pegaunos (#148), the Storm Steed: Pegasus as Zeus's thunder-bearer.

Concept A, "Thunderhead Rampant": a marble-white stallion rearing on bronze
hooves that throw sparks, Athena's golden bridle across his face, a mane and
tail of forked lightning, and wings that are thunderheads -- white cumulus
along the arm, darkening to storm-gray primaries with lightning crackling
between the feathers. The gorgoneion on his breast collar is the one quiet
hint of where he came from: the Gorgon's severed neck.
"""
import math

from mon_lib import C, Mat, Mon, bez, ribbon, ellipse_pts

INK = C.ink

COLORS = [
    ("ink", INK),
    # marble coat, shaded cool: the white of cloud tops, the blue of their shadows
    ("c0", (112, 128, 184)), ("c1", (168, 184, 224)), ("c2", (216, 224, 248)), ("c3", C.white),
    # storm grays for the thunderhead wings
    ("s0", (48, 48, 88)), ("s1", (88, 96, 144)),
    # Zeus's lightning: gold with a white-hot core
    ("g0", (184, 96, 24)), ("g1", (240, 168, 40)), ("g2", (248, 224, 88)), ("g3", (248, 248, 192)),
    # bronze hooves and breast collar
    ("b0", (112, 64, 32)), ("b1", (192, 128, 56)),
    # the signature glow: electric blue-white around the bolts, in the eye
    ("blue", (40, 96, 200)), ("glow", (144, 208, 248)),
]
# The coat turns storm-dark gray and the lightning turns Aegean blue; the
# electric halo and the eye flip to gold, so he is the storm's negative.
SHINY = {
    "c0": (40, 40, 64), "c1": (72, 80, 104), "c2": (112, 120, 144), "c3": (160, 168, 184),
    "g0": (24, 56, 120), "g1": (48, 104, 176), "g2": (112, 168, 224), "g3": (208, 240, 248),
    "blue": (200, 136, 32), "glow": (248, 224, 120),
}

coat = Mat(["c0", "c1", "c2", "c3"], line="c0", cuts=[0.34, 0.54, 0.74])
cloud = Mat(["s1", "c0", "c1", "c2", "c3"], line="c0", cuts=[0.2, 0.36, 0.52, 0.7])
bolt_m = Mat(["g0", "g1", "g2", "g3"], line="g0", cuts=[0.22, 0.44, 0.68])
bronze = Mat(["b0", "b1", "g1"], line="b0", cuts=[0.42, 0.74])


def _rot(pts, c, deg):
    """Rotate design points about c (degrees, clockwise on screen)."""
    ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


# --------------------------------------------------------------------------
# Shapes
# --------------------------------------------------------------------------

def bolt(p, pts, w0, w1, mat, **kw):
    """A lightning lock: a zigzag ribbon with sharp elbows, tapering from w0
    to w1 and then to a point over the last leg."""
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
            # a square-ish elbow keeps the kink sharp
            polys.append(ellipse_pts(b[0], b[1], wb / 2, wb / 2, n=4))
    return p.add(p.mask(*polys), mat, **kw)


def billow(p, cx, cy, r, group, under=False, dark_=False):
    """One cumulus billow with toon-crisp shading: a storm-gray underside,
    a cool shadow crescent, a white body and a lit top-left cap."""
    kw = dict(group=group, under=under)
    lv = (0, 0, 1, 2) if dark_ else (0, 1, 3, 4)
    base = p.circle(cx, cy, r, cloud, flat=lv[0], **kw)
    if not base:
        return 0
    mid = p.circle(cx - 0.14 * r, cy - 0.2 * r, r * 0.94, cloud, flat=lv[1], clip=[base], noline=True, group=group)
    body = p.circle(cx - 0.3 * r, cy - 0.38 * r, r * 0.84, cloud, flat=lv[2], clip=[base, mid], noline=True, group=group)
    if r >= 3.2:
        p.circle(cx - 0.5 * r, cy - 0.58 * r, r * 0.5, cloud, flat=lv[3], clip=[body], noline=True, group=group)
    return base


# --------------------------------------------------------------------------
# Battle front: rearing, three-quarter view facing left
# --------------------------------------------------------------------------

def feather(p, a, b, w, mat, curl=0.0, point=False, **kw):
    """A broad flight feather from root a to a rounded tip at b (or a pointed
    one); curl bows it (design px, positive bows it clockwise on screen)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    path = []
    for i in range(9):
        t = i / 8
        off = curl * math.sin(math.pi * t)
        path.append((a[0] + dx * t - dy / d * off, a[1] + dy * t + dx / d * off))
    if point:
        wa = p._minw(w)
        prof = lambda t: wa * (0.5 + 0.5 * min(1.0, t / 0.6)) * (1.0 if t < 0.72 else max(0.08, (1 - t) / 0.28))
        return p.add(p.mask(ribbon(path, prof)), mat, **kw)
    return p.limb(path, w * 0.45, w, mat, **kw)


wing_m = Mat(["s0", "s1", "c0", "c1", "c2"], line="s0")


def fan_feather(p, c, ang, r0, ln, w, group, bands=(0.66, 0.4), dim=0, curl=1.2, point=False):
    """One storm feather of a wing fanned about c: a dark rim on its clockwise
    edge (where it overlaps the feather below), lit on its other edge, and
    banded lighter toward the cloud it grows from. dim darkens every band."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    a = (c[0] + r0 * ca, c[1] + r0 * sa)
    b = (c[0] + ln * ca, c[1] + ln * sa)
    base = feather(p, a, b, w, wing_m, curl=curl, point=point, group=group, flat=0)
    if not base or not p.big:
        return base
    ox, oy = 0.9 * sa, -0.9 * ca            # toward the feather's counterclockwise edge
    body = feather(p, (a[0] + ox, a[1] + oy), (b[0] + ox, b[1] + oy), w * 0.9, wing_m, curl=curl, point=point,
                   group=group, flat=1, clip=[base], noline=True)
    keep = [body]
    for k, f in enumerate(bands):
        lvl = 2 + k - dim
        if lvl < 1:
            continue
        keep.append(p.circle(c[0], c[1], r0 + f * (ln - r0), wing_m, group=group, flat=lvl,
                             clip=list(keep), noline=True))
    return base


def _front(p, phase):
    big = p.big
    L = phase          # frame 2: head up a pixel
    beat = 5 * phase   # frame 2: wings beat up (degrees about the root)

    # ---- far wing: a darker thunderhead rising behind the neck --------------
    fr = (38, 24)
    for i, (ang, ln, w) in enumerate(((-80, 20.5, 4.8), (-96, 20.5, 4.8), (-112, 19, 4.4))):
        fan_feather(p, fr, ang + beat, 8, ln, w, 40 + i, dim=1, curl=-1.0)
    billow(p, 35.5, 14 - phase, 4.2, 45, dark_=True)

    # ---- near wing: a thunderhead raised behind the withers ------------------
    # Storm feathers fan out of a cumulus shoulder like rays from a cloud.
    nr = (40, 25)
    fan = ((38, 15.5, 4.8), (24, 17.5, 5.2), (10, 19.5, 5.6), (-4, 20.5, 5.8), (-18, 21.5, 5.8),
           (-32, 23.5, 5.8), (-46, 24.5, 5.6), (-60, 23.5, 5.2), (-74, 21.5, 4.6))
    for i, (ang, ln, w) in enumerate(fan):
        fan_feather(p, nr, ang - beat, 7, ln, w, 70 + i)
    # the cumulus shoulder: grey billows behind, white billows in front
    for i, (cx, cy, r) in enumerate(((48, 28, 3.4), (50, 22, 3.6), (49.5, 15.5, 3.5), (47, 9.5, 3.3),
                                     (42.5, 6.5, 3.0))):
        (cx, cy), = _rot([(cx, cy)], nr, -beat)
        billow(p, cx, cy, r, 80 + i, dark_=True)
    bil = ((41.5, 26, 5.0), (45, 20.5, 4.8), (44.5, 14.5, 4.4), (41, 10, 3.8))
    for i, (cx, cy, r) in reversed(list(enumerate(bil))):
        (cx, cy), = _rot([(cx, cy)], nr, -beat)
        billow(p, cx, cy, r, 90 + i)

    # ---- tail: forks of lightning streaming back and down ----------------------
    bolt(p, [(50, 41), (56.5, 39), (54.5, 44.5), (61, 43.5), (58.5, 49.5), (62.4, 56)], 6.0, 2.8, bolt_m, group=60)
    bolt(p, [(51, 44.5), (55.5, 49), (52, 52.5), (57, 58.5)], 4.6, 2.2, bolt_m, group=61, bias=0.12)
    bolt(p, [(53, 40), (58.5, 36.5), (56.5, 33), (61.6, 30.5)], 4.0, 2.0, bolt_m, group=62, bias=0.04)

    # ---- far legs, in shadow ---------------------------------------------------
    p.limb([(41.5, 43.5), (36.5, 49.5), (40, 54.5)], 8.0, 4.8, coat, bias=0.28, group=10)
    p.circle(40, 54.5, 2.4, coat, bias=0.28, group=10)                      # hock
    p.limb([(40, 54.5), (38.4, 57.6)], 4.2, 3.8, coat, bias=0.28, group=10)
    p.poly([(36.4, 57.6), (40.0, 57.6), (40.8, 61.4), (35.6, 61.4)], bronze, bias=0.15, group=20)
    # far foreleg: struck high and forward
    p.limb([(26, 28), (17, 25.5)], 8.0, 5.4, coat, bias=0.28, group=11)
    p.circle(17, 25.8, 2.8, coat, bias=0.28, group=11)                      # knee
    p.limb([(17, 25.5), (11.5, 28.5), (9, 31.6)], 4.6, 3.8, coat, bias=0.28, group=11)
    p.poly([(7.4, 30.4), (10.6, 32.6), (8.6, 35.6), (5.2, 33.6)], bronze, bias=0.15, group=21)

    # ---- body: barrel, then the masses that model it ---------------------------
    torso = [(36.5, 21.5), (41, 26.5), (45, 31.5), (48.5, 35), (52, 38.2), (54.6, 41.6), (55.2, 45.4),
             (54, 49.4), (50, 50.5), (44.5, 49.5), (41, 46.8), (37.5, 44.4), (34, 42.4), (30.5, 40.2),
             (27, 38.2), (23.5, 35), (21.6, 30.5), (22.4, 26), (26, 22.5), (31, 20.5)]
    p.poly(torso, coat, group=1)                                                  # barrel, tucked belly
    p.limb(bez((30.5, 28), (25, 18), (23, 11)), 12.5, 8.0, coat, group=1)        # neck
    p.limb(bez((36, 22), (30, 9), (24, 6)), 5.0, 6.4, coat, group=1)             # crest
    p.blob(28.5, 30.5, 7.8, 7.6, coat, group=1)                                  # deep chest
    p.blob(46.5, 42.5, 7.8, 7.6, coat, group=8)                                  # haunch
    if big:
        p.shade([(22, 20), (30, 37), (23, 36), (19, 24)], 0.12)   # under the neck
        p.shade([(36, 41), (46, 50), (41, 50), (33, 44)], 0.1)    # belly

    # near hind leg: gaskin, stifle forward, hock back, hoof planted
    p.limb([(47, 44), (44.5, 49.5), (50, 54)], 10.4, 5.6, coat, group=12)
    p.circle(50, 54, 2.8, coat, group=12)                                   # hock
    p.limb([(50, 54), (48.6, 57.8)], 5.0, 4.4, coat, group=12)
    p.poly([(46.2, 57.8), (50.6, 57.8), (51.4, 61.6), (45.2, 61.6)], bronze, group=22)

    # ---- head: noble, tucked, the muzzle tapering on a dished curve ------------
    hy = -L
    head = [(22.5, 4.6), (19.5, 5.2), (16.6, 6.8), (13.6, 9.2), (10.8, 11.9), (8.4, 14.2), (6.6, 15.9),
            (5.6, 17.4), (5.8, 19.0), (7.0, 20.2), (9.0, 20.7), (11.2, 20.1), (13.2, 19.0), (15.4, 18.3),
            (17.8, 18.0), (20.0, 17.1), (21.7, 15.2), (22.6, 13.0), (24.6, 9.6), (25.0, 6.8), (24.0, 5.0)]
    p.poly([(x, y + hy) for x, y in head], coat, group=3)
    p.circle(19.5, 13.2 + hy, 4.2, coat, group=3)                          # round jowl
    p.lens((20.6, 5.8 + hy), (19.4, 0.9 + hy), 3.4, coat, bend=0.7, group=4)          # near ear
    p.lens((23.6, 5.8 + hy), (24.6, 1.4 + hy), 3.0, coat, bend=0.5, bias=0.2, group=5)  # far ear
    if big:
        p.shade([(12, 18), (22, 13), (22, 18), (12, 21)], 0.12)     # under the jaw

    # ---- mane: forks of lightning along the crest --------------------------------
    bolt(p, [(24, 4.5 + hy), (29.5, 2.5), (28, 6), (34.5, 3.8)], 4.4, 2.4, bolt_m, group=63)
    bolt(p, [(26, 8.5), (32, 8), (30, 11.5), (37.5, 10.5)], 4.8, 2.4, bolt_m, group=64)
    bolt(p, [(28.5, 13.5), (34, 15), (32, 18.5), (39, 18.5)], 4.6, 2.2, bolt_m, group=65)
    bolt(p, [(31, 19), (35.5, 22.5), (33.5, 25.5), (39.5, 27.5)], 4.0, 2.0, bolt_m, group=67)

    # near foreleg: forearm thrust forward, knee folded, cannon hanging, hoof down
    p.limb([(30.5, 34), (20.5, 35.5)], 9.0, 5.8, coat, group=13)
    p.circle(20.4, 35.8, 3.0, coat, group=13)                               # knee
    p.limb([(20.5, 35.5), (17.8, 39.5), (17.2, 42.6)], 5.0, 4.2, coat, group=13)
    p.poly([(15.0, 42.6), (19.4, 42.6), (20.2, 46.2), (14.2, 46.2)], bronze, group=23)


# --------------------------------------------------------------------------
# Other views
# --------------------------------------------------------------------------

HEAD_PROFILE = [(22.5, 4.6), (19.5, 5.2), (16.6, 6.8), (13.6, 9.2), (10.8, 11.9), (8.4, 14.2), (6.6, 15.9),
                (5.6, 17.4), (5.8, 19.0), (7.0, 20.2), (9.0, 20.7), (11.2, 20.1), (13.2, 19.0), (15.4, 18.3),
                (17.8, 18.0), (20.0, 17.1), (21.7, 15.2), (22.6, 13.0), (24.6, 9.6), (25.0, 6.8), (24.0, 5.0)]


def _back(p):
    """Over the left shoulder: the vast near wing spread up and left, the far
    wing rising behind the neck, the head turned right into profile."""
    def hd(x, y):  # the front's head, mirrored to face right
        return (62 - x, y + 13)

    # far wing, rising up and right behind the neck and head
    for i, (ang, ln, w) in enumerate(((-12, 18.5, 6.0), (-26, 20.5, 6.4), (-40, 25, 6.6), (-54, 31, 6.6),
                                      (-68, 35, 6.4), (-82, 35.5, 6.0))):
        fan_feather(p, (39, 40), ang, 8, ln, w, 40 + i, dim=1, curl=1.4)
    billow(p, 44, 36, 5.0, 46, dark_=True)
    # near wing: a huge fan up and out to the left
    for i, (ang, ln, w) in enumerate(((-174, 17, 7.0), (-161, 21.5, 7.4), (-148, 26.5, 7.8), (-135, 33, 8.0),
                                      (-122, 41, 8.0), (-109, 38, 7.6), (-97, 33.5, 7.2), (-85, 28.5, 6.6))):
        fan_feather(p, (28, 43), ang, 9, ln, w, 70 + i, curl=-2.0, bands=(0.6, 0.4))
    # back, withers and shoulders, cropped by the frame
    p.blob(31, 66, 28, 15, coat, group=1)                        # back and withers
    p.blob(21, 57, 12.5, 9.5, coat, group=2)                     # near shoulder
    p.limb(bez((37, 56), (37, 42), (43, 28)), 19, 13.5, coat, group=1)   # neck, arched
    p.limb(bez((31, 52), (32, 38), (38, 22)), 8, 8, coat, group=1)       # crest
    # head in right profile
    p.poly([hd(x, y) for x, y in HEAD_PROFILE], coat, group=3)
    p.circle(*hd(19.5, 13.2), 4.6, coat, group=3)
    p.lens(hd(20.6, 5.8), hd(19.4, 0.9), 3.6, coat, bend=-0.7, group=4)
    p.lens(hd(23.6, 5.8), hd(24.6, 1.4), 3.2, coat, bend=-0.5, bias=0.2, group=5)
    # the cumulus shoulder of the near wing, over its root
    for i, (cx, cy, r) in enumerate(((25, 31.5, 4.8), (20.5, 33.5, 5.0), (17.5, 38, 5.0), (18, 43, 4.6),
                                     (24.5, 37, 5.4), (21.5, 42, 5.4))):
        billow(p, cx, cy, r, 90 + i)
    # mane: lightning locks streaming back off the crest
    bolt(p, [(38, 19), (32, 17), (34, 21), (27, 21.5)], 4.4, 2.4, bolt_m, group=63)
    bolt(p, [(35.5, 26), (29.5, 26), (32, 29.5), (24.5, 31)], 4.8, 2.4, bolt_m, group=64)
    bolt(p, [(33.5, 34), (28, 35.5), (31, 38.5), (23.5, 41)], 4.6, 2.2, bolt_m, group=65)
    if p.big:
        p.eye(46, 20, 3, 4, iris="blue", shine="c3")


def _fwing(p, c, mirror, group, beat=0, dim=0, lens=(13, 17, 19, 17)):
    """A follower's raised wing: four broad storm feathers and a cloud."""
    sx = -1 if mirror else 1
    for i, (ang, ln) in enumerate(zip((-176, -150, -124, -98), lens)):
        a = math.radians(ang + 8 * beat)
        b = (c[0] + sx * ln * math.cos(a), c[1] + ln * math.sin(a))
        p.limb([c, b], 4.5, 7.5, wing_m, flat=max(0, (2 if i % 2 else 3) - dim), group=group + i)
    p.circle(c[0] - sx * 1, c[1] - 2, 5.5, cloud, flat=4 - dim, group=group + 9)


def _fhead_front(p, y0=0):
    """The face, seen head-on, for the walking-down follower."""
    p.lens((26, 15 + y0), (22.5, 4 + y0), 6, coat, bend=0.9, group=4)
    p.lens((38, 15 + y0), (41.5, 4 + y0), 6, coat, bend=-0.9, group=5)
    p.blob(32, 18 + y0, 9.4, 7.6, coat, group=3)
    p.blob(32, 27 + y0, 6.4, 7.0, coat, group=3)
    p.blob(32, 33 + y0, 5.8, 3.8, coat, group=3)
    bolt(p, [(32, 12 + y0), (34.5, 15.5 + y0), (30.5, 16.5 + y0), (33, 21 + y0)], 4, 2.4, bolt_m, flat=2,
         noline=True, group=66)
    p.stroke([(23, 13 + y0), (41, 13 + y0)], "g1")             # browband
    p.stroke([(26, 29 + y0), (38, 29 + y0)], "g1")             # noseband
    if p.big:
        p.eye(24, 17 + y0, 4, 4, iris="blue", shine="c3")
        p.eye(36, 17 + y0, 4, 4, iris="blue", shine="c3")
    else:
        for x in (25.5, 38.0):                                   # small: ink over blue
            p.px(x, 17.5 + y0, "ink")
            p.px(x, 19.6 + y0, "blue")
    p.pxs([(29, 34 + y0), (35, 34 + y0)], "ink")


def _down(p, phase):
    """Follower walking toward the camera."""
    st = phase
    _fwing(p, (23, 40), False, 40, beat=st, lens=(12, 16, 18, 16))
    _fwing(p, (41, 40), True, 50, beat=st, lens=(12, 16, 18, 16))
    p.limb([(29.5, 50), (29.5, 58)], 4, 3.4, coat, bias=0.3, group=10)      # hind legs between
    p.limb([(34.5, 50), (34.5, 58)], 4, 3.4, coat, bias=0.3, group=11)
    p.blob(32, 44, 10, 8.6, coat, group=1)                                    # chest
    p.limb([(26.5, 47), (26, 61 - 2 * st)], 5.4, 4.2, coat, group=12)
    p.limb([(37.5, 47), (38, 61 - 2 * (1 - st))], 5.4, 4.2, coat, group=13)
    p.rect(23.5, 59 - 2 * st, 28.5, 61 - 2 * st, bronze, flat=1, group=22)
    p.rect(35.5, 59 - 2 * (1 - st), 40.5, 61 - 2 * (1 - st), bronze, flat=1, group=23)
    p.limb([(32, 40), (32, 30)], 12, 10, coat, group=1)                       # neck
    bolt(p, [(26, 26), (20, 29), (23.5, 31), (17, 35)], 4.6, 2.4, bolt_m, flat=2, noline=True, group=63)
    bolt(p, [(38, 26), (44, 29), (40.5, 31), (47, 35)], 4.6, 2.4, bolt_m, flat=2, noline=True, group=64)
    _fhead_front(p, st * 0)
    p.circle(32, 42, 2.2, bronze, flat=2, group=24)                           # gorgoneion boss


def _up(p, phase):
    """Follower walking away: rump, lightning tail, wings raised."""
    st = phase
    _fwing(p, (24, 32), False, 40, beat=st)
    _fwing(p, (40, 32), True, 50, beat=st)
    p.limb([(32, 36), (32, 24)], 11, 9, coat, group=1)                        # neck from behind
    p.lens((28, 16), (25.5, 6), 5, coat, bend=0.8, group=4)
    p.lens((36, 16), (38.5, 6), 5, coat, bend=-0.8, group=5)
    p.blob(32, 19, 7.0, 6.0, coat, group=3)                                   # poll
    bolt(p, [(32, 14), (29, 20), (34, 23), (30, 30)], 5.0, 2.8, bolt_m, flat=2, noline=True, group=63)
    p.limb([(27, 50), (26.5, 61 - 2 * st)], 6, 4.4, coat, group=12)
    p.limb([(37, 50), (37.5, 61 - 2 * (1 - st))], 6, 4.4, coat, group=13)
    p.rect(24, 59 - 2 * st, 29, 61 - 2 * st, bronze, flat=1, group=22)
    p.rect(35, 59 - 2 * (1 - st), 40, 61 - 2 * (1 - st), bronze, flat=1, group=23)
    p.blob(27, 44, 7.6, 8.2, coat, group=1)                                   # haunches
    p.blob(37, 44, 7.6, 8.2, coat, group=2)
    bolt(p, [(32, 38), (35.5, 44), (30, 48), (34, 57)], 5.6, 2.8, bolt_m, flat=2, noline=True, group=60)


def _side(p, phase):
    """Follower trotting left, wing raised, sparks at the hooves."""
    st = phase
    for i, (ang, ln) in enumerate(((-30, 15), (-52, 19), (-74, 21), (-96, 19), (-118, 15))):
        a = math.radians(ang - 6 * st)
        b = (36 + ln * math.cos(a), 32 + ln * math.sin(a))
        p.limb([(36, 32), b], 4.5, 7.5, wing_m, flat=1 if i % 2 else 2, group=70 + i)
    p.circle(35, 30, 6, cloud, flat=4, group=79)
    bolt(p, [(47, 37), (54, 36), (51.5, 41), (58, 42), (55.5, 46), (60, 51)], 5.4, 2.6, bolt_m, flat=2,
         noline=True, group=60)
    if st:
        legs = ([(24, 44), (19, 50), (18, 56)], [(42, 44), (46, 50), (48, 59)],
                [(27, 44), (28, 52), (27, 59)], [(45, 44), (42, 51), (40, 56)])
    else:
        legs = ([(24, 44), (24, 52), (24, 59)], [(42, 44), (40, 51), (38, 56)],
                [(27, 44), (21, 50), (20, 56)], [(45, 44), (48, 51), (50, 59)])
    p.limb(legs[0], 5, 4, coat, bias=0.3, group=10)
    p.limb(legs[1], 6.6, 4, coat, bias=0.3, group=11)
    for (x, y) in (legs[0][-1], legs[1][-1]):
        p.rect(x - 2, y, x + 2, y + 2, bronze, flat=0, group=20)
    p.blob(35, 39, 13, 7.6, coat, group=1)
    p.blob(25, 37, 8, 7.6, coat, group=1)
    p.blob(45, 39, 7.4, 7.2, coat, group=1)
    p.limb(bez((25, 36), (20, 28), (18, 21)), 11, 8, coat, group=1)
    p.poly([(x * 0.62 + 4, y * 0.62 + 12) for x, y in HEAD_PROFILE], coat, group=3)
    p.circle(16, 20, 3.4, coat, group=3)
    p.lens((17, 16), (16.5, 9), 4, coat, bend=0.6, group=4)
    bolt(p, [(19, 15), (26, 14), (24, 18.5), (32, 19)], 5, 2.6, bolt_m, flat=2, noline=True, group=63)
    bolt(p, [(21, 22), (28, 23.5), (26, 27.5), (33, 29)], 4.8, 2.6, bolt_m, flat=2, noline=True, group=64)
    p.limb(legs[2], 5.2, 4.2, coat, group=12)
    p.limb(legs[3], 7, 4.2, coat, group=13)
    for (x, y) in (legs[2][-1], legs[3][-1]):
        p.rect(x - 2, y, x + 2, y + 2, bronze, flat=1, group=21)
    p.eye(12, 17, 2, 3, iris="blue", shine="c3")


def _icon(p, phase):
    """Party icon: the front's pose in a few bold shapes that survive 0.45x."""
    up = phase * 1.5
    # wing: five broad storm feathers fanned up and back, one cloud at the root
    for i, ang in enumerate((20, -4, -28, -52, -76)):
        a = math.radians(ang - 6 * phase)
        ln = (17, 21, 23, 23, 21)[i]
        b = (40 + ln * math.cos(a), 25 + ln * math.sin(a))
        p.limb([(40, 25), b], 5, 8.5, wing_m, flat=1 if i % 2 else 2, group=70 + i)
    p.circle(41, 22, 7.5, cloud, flat=4, group=80)
    bolt(p, [(50, 42), (58, 41), (55, 47), (62, 52)], 6.5, 3.5, bolt_m, flat=2, noline=True, group=60)  # tail
    p.limb([(42, 44), (38, 52), (40, 59)], 8, 5, coat, flat=1, group=10)                # far hind
    p.limb([(26, 28), (14, 26), (9, 32)], 7.5, 5, coat, flat=1, group=11)              # far fore
    p.poly([(36.5, 21.5), (45, 31.5), (52, 38), (55, 45), (52, 50), (44, 49.5), (34, 42.4),
            (27, 38.2), (21.6, 30.5), (22.4, 26), (31, 20.5)], coat, flat=3, group=1)   # body
    p.blob(46.5, 42.5, 8, 7.6, coat, flat=3, group=1)
    p.limb(bez((30.5, 28), (25, 18), (23, 11)), 13, 9, coat, flat=3, group=1)          # neck
    p.limb([(47, 44), (45, 50), (50, 54), (48.5, 60)], 9, 5.5, coat, flat=3, group=12)  # near hind
    p.poly([(p_[0], p_[1] - up) for p_ in HEAD_PROFILE], coat, flat=3, group=3)        # head
    p.circle(19.5, 13.2 - up, 4.4, coat, flat=3, group=3)
    p.lens((20.6, 7 - up), (18.6, 0.5 - up), 5, coat, flat=3, group=4)                 # ear
    bolt(p, [(24, 5), (32, 3), (30, 8), (40, 7)], 6, 3.5, bolt_m, flat=2, noline=True, group=63)     # mane
    bolt(p, [(28, 13), (36, 13), (34, 18), (43, 18)], 6, 3.5, bolt_m, flat=2, noline=True, group=64)
    p.limb([(30.5, 34), (19, 36), (16, 44)], 8, 5.5, coat, flat=3, group=13)            # near fore
    for (x, y) in ((8, 33), (16, 45), (40, 60), (48.5, 61)):
        p.blob(x, y, 3.4, 2.4, bronze, flat=1, group=20)
    p.eye(14, 8 - up, 2, 2, iris="blue", shine="c3")


def pegaunos(p, view, phase):
    if view == "front":
        _front(p, phase)
    elif view == "icon":
        _icon(p, phase)
    elif view == "back":
        _back(p)
    elif view == "down":
        _down(p, phase)
    elif view == "up":
        _up(p, phase)
    elif view == "side":
        _side(p, phase)


MONS = [
    # icon palette 3 keeps the coat white, the bolts yellow and the wing storm-blue
    Mon("Pegaunos", COLORS, SHINY, pegaunos, foot="hoof", icon_pal=3),
]
