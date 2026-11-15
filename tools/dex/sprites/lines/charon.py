"""Charon line: Obolorn, Kalyptor, Charonaut (Ghost, Ghost, Ghost/Water).
The unburied shade with no obol for the ferryman, the hooded shades crowding
the bank of the Styx, and Charon himself, fused to his reed skiff."""

from mon_lib import C, Mat, Mon, lens_pts

INK = C.ink


def _spline(pts, n=10):
    """A smooth path through pts (Catmull-Rom)."""
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[-1])
    return out


def _closed(pts, n=8):
    """A smooth closed outline through pts."""
    P = list(pts) + list(pts[:3])
    out = _spline(P, n)
    k = n
    return out[k:k + n * len(pts)]


# --------------------------------------------------------------------------
# Obolorn, the unburied shade
# --------------------------------------------------------------------------

OBOLORN_COLORS = [
    ("ink", INK),
    # marble-gray shade
    ("g0", (136, 144, 160)), ("g1", (184, 184, 200)), ("g2", (224, 224, 224)), ("white", C.white),
    # Aegean-blue shadows, fading to nothing at the tail
    ("sh0", (32, 48, 104)), ("sh1", (64, 96, 160)), ("sh2", (120, 160, 208)), ("mist", (184, 208, 232)),
    # the glint where the obol should be
    ("gold0", (176, 120, 32)), ("gold1", (240, 192, 64)), ("gold2", (248, 240, 176)),
]
OBOLORN_SHINY = {
    # a cold green-gray, and the glint turns silver
    "g0": (120, 144, 128), "g1": (168, 192, 168), "g2": (208, 224, 208), "white": (232, 248, 232),
    "gold0": (120, 128, 144), "gold1": (192, 200, 216), "gold2": (248, 248, 248),
}

ob_body = Mat(["sh1", "g0", "g1", "g2", "white"], line="sh1", cuts=[0.12, 0.3, 0.52, 0.76])
ob_tail = Mat(["sh1", "g0", "sh2", "mist"], line="sh1", outline="sh0", cuts=[0.3, 0.5, 0.74])
ob_face = Mat(["g1", "g2", "white"], line="g0", cuts=[0.44, 0.72])
ob_arm = Mat(["sh1", "g0", "g1", "g2"], line="sh1", cuts=[0.24, 0.5, 0.76])


def obolorn(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "icon") else 0
        sw = phase
        # the smoke tail trailing back and curling, fading to mist
        tail = _spline([(32, 40), (36.5, 47), (42, 51 + sw), (47.5, 50.6 + sw), (49.6, 47.2)])
        p.limb(tail, 10.0, 2.0, ob_tail, group=2)
        p.limb(_spline([(35, 45), (38.6, 52.4), (36, 55.6 - sw)]), 4.4, 1.4, ob_tail, group=3, bias=0.1)
        # the body, a drop narrowing into the tail
        p.blob(31.6, 39.0 - L, 8.0, 8.4, ob_body, ang=30, group=1)
        # the back of the shade sweeping down from behind the head
        p.poly(_closed([(30, 21 - L), (36.5, 24 - L), (39.6, 31 - L), (38.6, 39), (35, 43.5), (30, 42), (27, 34 - L)]),
               ob_body, group=1, bias=0.04)
        # the far arm, a stub against the body
        p.limb([(36.5, 38.5 - L), (39.5, 42.5 - L)], 3.2, 2.4, ob_arm, bias=0.3, group=4)
        # the head: round and pale, tilted toward the empty palm
        p.blob(27.6, 29.0 - L, 9.4, 8.8, ob_face, group=6)
        # the near arm held out, palm up and open
        p.limb(_spline([(28, 39.5 - L), (22, 41 - L), (16, 40 - L)]), 3.2, 2.2, ob_arm, group=7)
        p.blob(14.0, 39.4 - L, 3.4, 1.8, ob_arm, ang=-8, group=7)
        for fx, fy in ((10.8, 37.0), (12.8, 36.4), (16.6, 37.2)):
            p.limb([(fx + 1.0, fy + 2.0 - L), (fx, fy - L)], 1.5, 1.2, ob_arm, group=7)
        if p.big:
            # hollow eyes looking down at the palm, a downturned mouth, the
            # coin-shaped glint where the obol should be
            p.patch(19, 26 - L, ["............", "..11....11..", ".1111..1111.", ".1111..1111.", ".1611..1611.",
                                 "..11....11..", "............", "......55....", ".....5..5..."],
                    {"1": "ink", "5": "g0", "6": "sh2"})
            p.patch(11, 33 - L, [".bcb.", "b...b", ".bcb."], {"b": "gold0", "c": "gold1"})
            p.px(13, 32 - L, "gold2")
        else:
            p.pxs([(23.5, 29 - L), (29.5, 29 - L)], "ink")
        return

    if view == "back":
        # over the shoulder: the head turned right in profile, the palm held
        # out to the right, the body sweeping down out of the frame
        p.limb(_spline([(30, 44), (22, 54), (16, 60), (14, 67)]), 13, 9, ob_tail, group=2)
        p.limb(_spline([(20, 50), (10, 54), (5.6, 50.6)]), 5.0, 1.6, ob_tail, group=3, bias=0.08)
        p.poly(_closed([(38, 14), (30, 18), (24.6, 28), (24, 40), (28.6, 50), (36, 52), (42, 44), (44, 30)]), ob_body,
               group=1)
        p.limb(_spline([(36, 41), (44, 44), (52, 42.6)]), 4.4, 3.2, ob_arm, group=7)
        p.blob(54.6, 41.8, 4.2, 2.4, ob_arm, ang=8, group=7)
        for fx, fy in ((58.6, 38.4), (56.6, 37.6), (52.4, 38.8)):
            p.limb([(fx - 1.2, fy + 2.4), (fx, fy)], 1.9, 1.4, ob_arm, group=7)
        p.blob(40, 26, 10.6, 10.2, ob_face, group=6)
        p.patch(43, 22, [".11.", "1111", "1111", "1611", ".11."], {"1": "ink", "6": "sh2"})
        p.patch(45, 32, [".55.", "5..5"], {"5": "g0"})
        p.patch(52, 33, [".bcb.", "b...b", ".bcb."], {"b": "gold0", "c": "gold1"})
        p.px(56, 32, "gold2")
        return

    if view in ("down", "up"):
        # follower: drifting toward the player with its palm out (down), or
        # away (up); the tail sways
        S = 1 if phase else -1
        p.limb(_spline([(32, 42), (32 + 3 * S, 50), (32 - 2 * S, 56), (32 - 5 * S, 58)]), 9, 2, ob_tail, group=2)
        p.blob(32, 40, 8, 7.4, ob_body, group=1)
        if view == "down":
            p.limb(_spline([(26, 40), (20, 42), (15, 40)]), 3.2, 2.4, ob_arm, group=7)
            p.blob(13.6, 39.6, 3.2, 1.8, ob_arm, group=7)
            p.limb([(38, 40), (40, 44)], 3, 2.4, ob_arm, group=7, bias=0.2)
            p.blob(32, 28, 9.4, 9.0, ob_face, group=6)
            p.patch(25, 25, [".11...11.", "1111.1111", "1611.1611", ".11...11.", ".........", "...555...", "..5...5.."],
                    {"1": "ink", "6": "sh2", "5": "g0"})
            if p.big:
                p.patch(11, 35, [".bcb.", "b...b", ".bcb."], {"b": "gold0", "c": "gold1"})
        else:
            p.limb(_spline([(26, 40), (20, 42), (15, 40)]), 3.2, 2.4, ob_arm, group=0, bias=0.3)
            p.blob(32, 28, 9.4, 9.0, ob_body, group=6)
        return


# --------------------------------------------------------------------------
# Kalyptor, the hooded wraith
# --------------------------------------------------------------------------

KALYPTOR_COLORS = [
    ("ink", INK),
    ("void", (16, 24, 40)),
    # cypress-dark robe with Aegean-blue folds
    ("cy0", (16, 40, 40)), ("cy1", (32, 72, 56)), ("cy2", (56, 104, 80)),
    ("ae0", (32, 64, 128)), ("ae1", (64, 112, 176)), ("ae2", (128, 176, 224)),
    # marble-gray hands
    ("hd0", (112, 112, 128)), ("hd1", (168, 168, 176)), ("hd2", (216, 216, 216)),
    # the thin sun-gold rim on the hood
    ("gd0", (176, 120, 32)), ("gd1", (240, 200, 72)),
    ("white", C.white),
]
KALYPTOR_SHINY = {
    # the robe turns from cypress to a deep terracotta red
    "cy0": (64, 16, 16), "cy1": (112, 40, 24), "cy2": (168, 72, 40),
}

k_robe = Mat(["cy0", "cy1", "ae0", "cy2"], line="cy0", cuts=[0.22, 0.5, 0.78])
k_fold = Mat(["ae0", "ae1", "ae2"], line="cy0", cuts=[0.4, 0.75])
k_hand = Mat(["hd0", "hd1", "hd2"], line="hd0", cuts=[0.34, 0.7])
k_void = Mat(["void"], line="void", outline="ink")


def _tatter(p, a, b, w, mat, bend=0.0, **kw):
    """A ragged strip of robe from a to its tip b."""
    return p.poly(lens_pts(a, b, p._minw(w), bend, fat=0.25), mat, **kw)


def kalyptor(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "icon") else 0
        sw = phase
        # the tatters streaming back from the hem
        for a, b, w, bend, bias in (((40, 40), (58, 39 - sw), 7.0, 1.2, 0.18), ((40, 44), (57, 49 + sw), 7.0, -0.6, 0.12),
                                    ((38, 46), (49, 57 - sw), 6.4, -1.0, 0.06), ((34, 45), (38, 57 + sw), 5.6, -0.6, 0.0)):
            _tatter(p, a, b, w, k_robe, bend=bend, group=2, bias=bias)
        # the far arm, reaching higher, behind
        p.limb(_spline([(27, 25 - L), (19, 23.6 - L), (12.6, 21.4 - L)]), 4.4, 3.0, k_hand, group=4, bias=0.3)
        p.poly(_closed([(25, 22 - L), (31, 21.4 - L), (31.4, 28 - L), (23.4, 29 - L), (19.6, 26 - L)]), k_robe,
               group=4, bias=0.25)
        for fx, fy, dx, dy in ((12.6, 21.4, -4.6, -2.4), (12.6, 21.4, -5.2, 0.4), (12.6, 21.4, -3.6, 2.4)):
            p.limb([(fx, fy - L), (fx + dx, fy + dy - L)], 1.6, 1.0, k_hand, group=4, bias=0.3)
        # the body: shoulders hunched forward, the robe falling back
        body = _closed([(24, 21), (34, 18), (42, 24), (45, 34), (44, 42), (38, 47), (31, 45), (27, 36), (23, 28)])
        p.poly(body, k_robe, group=1)
        # the hood: a deep cowl, its tip blown back
        hood = _closed([(17.6, 15 - L), (22, 7 - L), (30, 3.6 - L), (38, 4.4 - L), (46, 3.4 - L), (42, 8 - L),
                        (38.6, 14 - L), (37, 23 - L), (30, 27 - L), (22, 26 - L), (17, 22 - L)])
        p.poly(hood, k_robe, group=3)
        p.blob(23.4, 18.4 - L, 5.0, 6.0, k_void, ang=-12, group=5)
        # the near arm, reaching ahead and lower
        p.poly(_closed([(33, 26), (37, 29), (34, 35), (27, 36), (23, 33), (27, 28)]), k_robe, group=6)
        p.limb(_spline([(25, 33), (18, 33.6), (12.4, 32 + sw * 0.5)]), 4.6, 3.2, k_hand, group=7)
        for dx, dy in ((-5.2, -2.2), (-5.6, 0.6), (-4.0, 3.0)):
            p.limb([(12.4, 32 + sw * 0.5), (12.4 + dx, 32 + dy + sw)], 1.7, 1.0, k_hand, group=7)
        if p.big:
            # two pale eyes in the dark of the cowl, the gold rim on its edge
            p.patch(19, 16 - L, ["..1....", ".a1..a.", ".a1..a1", "..1...."], {"a": "white", "1": "void"})
            p.stroke(_spline([(18.4, 22.4 - L), (17.6, 17 - L), (20.6, 12 - L), (26, 11 - L)], 3), "gd1")
        else:
            p.pxs([(20.5, 18 - L), (25.5, 18 - L)], "white")
        return

    if view == "back":
        # over the shoulder: the cowl in right profile, both arms reaching
        # right, the tatters streaming back toward the player
        for a, b, w, bend in (((24, 46), (2, 50), 9.0, 1.6), ((26, 52), (6, 63), 9.0, 0.4), ((32, 54), (20, 68), 8.0, -0.6)):
            _tatter(p, a, b, w, k_robe, bend=bend, group=2, bias=0.1)
        p.limb(_spline([(40, 26), (50, 25), (58.4, 22)]), 5.4, 3.8, k_hand, group=4, bias=0.3)
        for dx, dy in ((4.6, -3.4), (5.4, -0.4), (4.2, 2.4)):
            p.limb([(58.4, 22), (58.4 + dx, 22 + dy)], 2.0, 1.2, k_hand, group=4, bias=0.3)
        p.poly(_closed([(12, 66), (12, 44), (18, 30), (28, 22), (42, 22), (50, 30), (52, 44), (46, 66)]), k_robe, group=1)
        hood = _closed([(48.6, 14), (44, 6), (36, 2), (26, 3), (16, 2.6), (21, 8), (24, 16), (26, 26), (34, 32), (44, 31),
                        (50, 25)])
        p.poly(hood, k_robe, group=3)
        p.blob(47, 18, 4.6, 6.2, k_void, ang=10, group=5)
        p.poly(_closed([(36, 30), (46, 32), (50, 38), (44, 42), (36, 40)]), k_robe, group=6)
        p.limb(_spline([(44, 38), (52, 38.6), (58.6, 36)]), 5.6, 4.0, k_hand, group=7)
        for dx, dy in ((4.6, -3.6), (5.4, -0.6), (4.0, 2.4)):
            p.limb([(58.6, 36), (58.6 + dx, 36 + dy)], 2.0, 1.2, k_hand, group=7)
        if p.big:
            p.patch(48, 16, ["1..", "1a.", "1a1", "1.."], {"a": "white", "1": "void"})
            p.stroke(_spline([(50.6, 24), (51.6, 18), (49, 12.6), (44, 10.4)], 3), "gd1")
        return

    if view in ("down", "up"):
        # follower: the hooded shade gliding with both arms out ahead
        S = 1 if phase else -1
        for a, b, w in (((28, 44), (22 - S, 58), 6.0), ((32, 46), (32, 59 + S), 6.0), ((36, 44), (42 - S, 58), 6.0)):
            _tatter(p, a, b, w, k_robe, group=2, bias=0.12)
        p.poly(_closed([(22, 26), (32, 20), (42, 26), (44, 40), (38, 48), (26, 48), (20, 40)]), k_robe, group=1)
        if view == "down":
            for sx in (-1, 1):
                p.limb([(32 + sx * 8, 28), (32 + sx * 12, 36), (32 + sx * 10, 41 + (S * sx))], 4.0, 3.0, k_hand,
                       group=7)
            hood = _closed([(20.6, 18), (24, 8), (32, 2.6), (40, 8), (43.4, 18), (42, 27), (32, 30), (22, 27)])
            p.poly(hood, k_robe, group=3)
            p.blob(32, 19, 6.6, 6.8, k_void, group=5)
            p.pxs([(28.5, 18.5), (35.5, 18.5), (28.5, 19.5), (35.5, 19.5)], "white")
            if p.big:
                p.stroke(_spline([(24.6, 24), (25.4, 15), (32, 10.6), (38.6, 15), (39.4, 24)], 3), "gd1")
        else:
            # from behind: both sleeves reaching ahead past the shoulders, the
            # cowl with its tip flopped back, folds down the robe
            for sx in (-1, 1):
                p.limb([(32 + sx * 7, 27), (32 + sx * 13, 31), (32 + sx * 14, 36)], 5.0, 4.0, k_robe, group=0,
                       bias=0.1)
            hood = _closed([(21.6, 20), (24.6, 11), (31, 7.4), (38.6, 10), (42.4, 19), (40.6, 28), (32, 31), (23, 28)])
            p.poly(hood, k_robe, group=3)
            p.lens((33, 9), (39.6, 1.6 + S * 0.5), 5.4, k_robe, bend=-1.2, fat=0.3, group=4)
            if p.big:
                for x0 in (28, 32, 36):
                    p.stroke([(x0, 33), (x0 + (x0 - 32) * 0.3, 46)], "ae0")
        return


# --------------------------------------------------------------------------
# Charonaut, the ferryman
# --------------------------------------------------------------------------

CHARONAUT_COLORS = [
    ("ink", INK),
    # the cypress-dark hood and robe
    ("cy0", (16, 32, 32)), ("cy1", (32, 64, 56)), ("cy2", (64, 104, 88)),
    # limestone reeds
    ("rd0", (112, 80, 48)), ("rd1", (176, 144, 96)), ("rd2", (224, 200, 152)),
    # the darkest Aegean water at the hull
    ("aq0", (16, 24, 64)), ("aq1", (32, 64, 128)),
    # bone: beard, hands and face
    ("bn0", (104, 104, 120)), ("bn1", (168, 168, 168)), ("bn2", (224, 216, 200)),
    # sun-gold lantern and coin, and the lantern's light
    ("gd0", (192, 120, 32)), ("gd1", (248, 200, 64)), ("glow", (248, 248, 200)),
]
CHARONAUT_SHINY = {
    # black reeds, and the lantern burns pale blue
    "rd0": (24, 24, 32), "rd1": (56, 56, 64), "rd2": (96, 96, 104),
    "gd0": (64, 112, 184), "gd1": (136, 192, 240), "glow": (216, 240, 248),
}

c_robe = Mat(["cy0", "cy1", "cy2"], line="cy0", cuts=[0.4, 0.74])
c_reed = Mat(["rd0", "rd1", "rd2"], line="rd0", cuts=[0.34, 0.7])
c_water = Mat(["aq0", "aq1"], line="aq0", outline="aq0", cuts=[0.6])
c_bone = Mat(["bn0", "bn1", "bn2"], line="bn0", cuts=[0.36, 0.7])
c_gold = Mat(["gd0", "gd1", "glow"], line="gd0", cuts=[0.4, 0.74])
c_void = Mat(["ink"])


def _lantern(p, x, y, glow=True):
    """A bronze lantern whose ring is at (x, y): a cap, a cage and the light."""
    p.limb([(x, y), (x, y + 2.4)], 1.2, 1.2, c_reed, group=60)
    p.poly([(x - 3.2, y + 4.6), (x - 1.6, y + 2.6), (x + 1.6, y + 2.6), (x + 3.2, y + 4.6)], c_reed, group=61)
    p.poly(_closed([(x - 3.6, y + 5), (x + 3.6, y + 5), (x + 4.0, y + 9.6), (x + 2.6, y + 12.6), (x - 2.6, y + 12.6),
                    (x - 4.0, y + 9.6)]), c_gold, group=62)
    p.rect(x - 3.0, y + 12.4, x + 2.0, y + 13.4, c_reed, group=63)


def charonaut(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "icon") else 0
        sw = phase
        # the black water under the hull, and its ripples
        p.blob(31, 58.2, 28.4, 3.4, c_water, group=1)
        # the stern post curling up behind him
        p.limb(_spline([(52, 50), (58.4, 44.6), (60.2, 37), (57.6, 32.6), (55, 34)]), 6.0, 2.4, c_reed, group=2,
               bias=0.22)
        # the far arm reaching forward and up with the lantern
        p.limb(_spline([(31, 23 - L), (24.4, 20 - L), (18.6, 13.8 - L)]), 4.6, 3.6, c_robe, group=3, bias=0.32)
        p.limb([(18.6, 13.8 - L), (16, 10.6 - L)], 2.6, 2.0, c_bone, group=3, bias=0.2)
        _lantern(p, 15.2, 10.2 - L + sw * 0.5)
        # the cloak behind, ragged at the hem over the reeds
        cloak = _closed([(28, 22), (36, 15), (50, 14), (58, 22), (58.6, 34), (56, 44), (52.6, 49), (47, 45.6),
                         (42, 50), (37, 45.4), (32.6, 49), (29.4, 40), (27.6, 30)])
        p.poly(cloak, c_robe, group=10)
        # the hood, tall, ragged and peaked
        p.poly(_closed([(30.6, 14 - L), (34, 6 - L), (40, 1.8 - L), (46.6, 2.6 - L), (50.6, 7 - L), (52, 15 - L),
                        (50.6, 22 - L), (44, 25 - L), (36, 23 - L), (31.4, 19 - L)]), c_robe, group=11)
        p.blob(38.6, 14.4 - L, 5.0, 5.6, c_void, ang=-8, group=12)
        # the beard, long ragged wisps falling from the hood to the waist
        p.poly(_closed([(34.4, 17.6 - L), (41.6, 17.6 - L), (44.6, 23), (44, 31), (41.6, 39), (39.4, 33),
                        (37, 39), (35.4, 31), (33, 24)]), c_bone, group=13)
        # the obol on its cord
        p.circle(42.6, 31.4, 2.6, c_gold, group=14)
        # the reed boat: a long bundle, the prow curling up at the bow
        p.limb(_spline([(7, 45), (16, 50.4), (32, 53), (46, 52), (55.4, 47.6)]), 7.4, 7.6, c_reed, group=30)
        p.limb(_spline([(8, 46.4), (4.4, 40), (5, 31.6), (10, 28), (13.6, 30.6), (11.6, 33.4)]), 6.0, 2.6, c_reed,
               group=31)
        # the reeds wrapping his waist where man and boat are one
        p.poly(_closed([(29, 44.6), (37, 43), (46, 43.4), (55, 44), (56, 49.6), (40, 52), (29, 50)]), c_reed, group=32)
        # the pole crossing the frame, gripped by the near hand
        p.limb([(58.8, 2.4), (45.2, 61.4)], 2.8, 2.8, c_reed, group=40)
        p.limb(_spline([(50, 20), (55.4, 26.6), (53.6, 33.6)]), 5.0, 4.0, c_robe, group=41)
        p.blob(52.6, 34.4, 2.8, 2.6, c_bone, group=41)
        if p.big:
            p.pxs([(36, 14 - L), (40, 14 - L), (36, 15 - L), (40, 15 - L)], "glow")
            for x in (12, 20, 28, 36, 44, 51):
                y = 47 + (0.0007 * (x - 32) ** 2) * 100
                p.stroke([(x, y - 3), (x + 1, y + 3)], "rd0")
        else:
            p.pxs([(37, 14 - L), (40, 14 - L)], "glow")
        return

    if view == "back":
        # over the shoulder: the ragged cloak and hood from behind, the head
        # turned right in profile with its glowing eye, the lantern held out
        # ahead, the pole planted, the stern curl and reeds cropped below
        p.blob(32, 64, 34, 5, c_water, group=1)
        p.limb([(10, 1.6), (22, 70)], 3.4, 3.4, c_reed, group=2, bias=0.15)
        p.limb(_spline([(40, 26), (50, 22), (55, 16)]), 5.2, 4.0, c_robe, group=3, bias=0.28)
        p.limb([(55, 16), (57, 12.4)], 3.2, 2.6, c_bone, group=3, bias=0.2)
        _lantern(p, 57.6, 11.6)
        cloak = _closed([(8, 66), (6, 48), (12, 34), (22, 24), (36, 20), (48, 26), (54, 40), (56, 54), (58, 66)])
        p.poly(cloak, c_robe, group=10)
        p.poly(_closed([(48, 12), (46, 5), (38, 1.6), (28, 3.6), (24, 10), (26, 22), (34, 30), (44, 28), (49, 21)]),
               c_robe, group=11)
        p.blob(46.6, 15, 3.6, 5.0, c_void, group=12)
        p.poly(_closed([(46, 18), (50, 22), (50, 30), (47, 38), (44, 30), (43, 22)]), c_bone, group=13)
        p.limb(_spline([(2, 58), (14, 54), (34, 54), (54, 56), (62, 60)]), 10, 10, c_reed, group=30)
        if p.big:
            p.pxs([(48, 14), (48, 15)], "glow")
        return

    if view in ("down", "up"):
        # follower: the skiff gliding with ripples under the hull, bow-on
        # (down) or stern-on (up)
        S = 1 if phase else -1
        p.blob(32, 57, 20, 3.6, c_water, group=1)
        if view == "down":
            p.limb([(46, 2), (44, 60)], 2.6, 2.6, c_reed, group=2, bias=0.15)
            p.poly(_closed([(20, 24), (32, 16), (44, 24), (46, 40), (42, 50), (22, 50), (18, 40)]), c_robe, group=10)
            p.poly(_closed([(23, 14), (28, 4), (32, 2), (36, 4), (41, 14), (40, 24), (32, 27), (24, 24)]), c_robe, group=11)
            p.blob(32, 15, 5.4, 5.6, c_void, group=12)
            p.poly(_closed([(27, 19), (37, 19), (37, 30), (32, 37), (27, 30)]), c_bone, group=13)
            p.limb([(22, 26), (16, 20), (14, 16)], 4, 3, c_robe, group=14)
            _lantern(p, 13, 13 + S * 0.5)
            p.poly(_closed([(18, 44), (32, 42), (46, 44), (44, 54), (32, 57), (20, 54)]), c_reed, group=30)
            p.limb(_spline([(32, 56), (32, 48), (30, 42), (33, 39)]), 5, 3, c_reed, group=31)
            p.pxs([(30, 14), (34, 14), (30, 15), (34, 15)], "glow")
        else:
            p.poly(_closed([(18, 44), (32, 42), (46, 44), (44, 54), (32, 57), (20, 54)]), c_reed, group=30)
            p.limb([(46, 2), (44, 60)], 2.6, 2.6, c_reed, group=2)
            p.poly(_closed([(20, 24), (32, 16), (44, 24), (46, 40), (42, 50), (22, 50), (18, 40)]), c_robe, group=10)
            p.poly(_closed([(23, 14), (28, 4), (32, 2), (36, 4), (41, 14), (40, 24), (32, 28), (24, 24)]), c_robe, group=11)
            p.limb(_spline([(32, 56), (32, 46), (30, 40), (33, 37)]), 6, 3, c_reed, group=31)
            p.limb([(22, 26), (16, 20), (14, 16)], 4, 3, c_robe, group=14, bias=0.2)
            _lantern(p, 13, 13 + S * 0.5)
        if p.big:
            for x in (14, 22, 42, 50):
                p.stroke([(x + S, 58), (x + 3 + S, 58)], "aq1")
        return


MONS = [
    Mon("Obolorn", OBOLORN_COLORS, OBOLORN_SHINY, obolorn, foot="blank"),
    # icon palette 4 keeps the robe a dark teal instead of black
    Mon("Kalyptor", KALYPTOR_COLORS, KALYPTOR_SHINY, kalyptor, foot="blank", icon_pal=4),
    # icon palette 4 keeps the black water blue and the reeds tan
    Mon("Charonaut", CHARONAUT_COLORS, CHARONAUT_SHINY, charonaut, foot="blank", icon_pal=4),
]
