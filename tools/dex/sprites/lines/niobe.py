"""Niobe line: Dakrock (Rock/Water), a single stage. Niobe, who boasted over
Leto and was turned to a rock on Mount Sipylos that still weeps."""

from mon_lib import C, Mat, Mon

INK = C.ink


def _spline(pts, n=8):
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
    return out[n:n + n * len(pts)]


def _mx(pts, cx=32):
    """Mirror points about x = cx (for the symmetric follower views)."""
    return [(2 * cx - x, y) for x, y in pts]


# --------------------------------------------------------------------------
# Dakrock, the weeping rock
# --------------------------------------------------------------------------

DAKROCK_COLORS = [
    ("ink", INK),
    # the shared deep shadow of the stone
    ("st0", (72, 64, 64)),
    # limestone: the warm crag of the robe and the hands
    ("lime1", (120, 104, 88)), ("lime2", (168, 152, 120)), ("lime3", (208, 192, 152)),
    # marble: the cool gray veil
    ("mar1", (128, 128, 144)), ("mar2", (176, 176, 184)), ("mar3", (216, 216, 216)), ("white", C.white),
    # olive moss in the folds
    ("moss0", (56, 72, 32)), ("moss1", (96, 112, 48)), ("moss2", (144, 160, 72)),
    # Aegean-blue tears
    ("w0", (24, 56, 120)), ("w1", (48, 104, 176)), ("w2", (120, 176, 232)),
]
DAKROCK_SHINY = {
    # pale marble-white stone with sun-gold tears
    "st0": (112, 104, 112), "lime1": (168, 160, 160), "lime2": (208, 200, 192), "lime3": (232, 232, 224),
    "mar1": (176, 176, 184), "mar2": (216, 216, 224), "mar3": (240, 240, 240),
    "w0": (152, 96, 24), "w1": (224, 160, 40), "w2": (248, 224, 104),
}

d_robe = Mat(["st0", "lime1", "lime2", "lime3"], line="st0", cuts=[0.2, 0.46, 0.74])
d_crag = Mat(["st0", "lime1", "lime2"], line="st0", cuts=[0.34, 0.66])
d_veil = Mat(["st0", "mar1", "mar2", "mar3", "white"], line="mar1", cuts=[0.12, 0.3, 0.56, 0.84])
d_skin = Mat(["lime2", "lime3", "white"], line="lime1", cuts=[0.4, 0.78])
d_hand = Mat(["lime1", "lime2", "lime3"], line="st0", cuts=[0.3, 0.64])
d_hood = Mat(["st0"], line="st0")
d_moss = Mat(["moss0", "moss1", "moss2"], line="moss0", cuts=[0.34, 0.66])
d_water = Mat(["w0", "w1", "w2"], line="w0", outline="w0", cuts=[0.3, 0.62])
d_pool = Mat(["w0", "w1", "w2"], line="w0", cuts=[0.4, 0.75])


def _stream(p, pts, w=1.6, **kw):
    """A thin stream of tears along a smooth path."""
    path = _spline(pts, 6)
    pid = p.limb(path, w, w, d_water, flat=1, **kw)
    if p.big:
        # a lit thread down the stream's left side
        p.stroke([(x - 0.4, y) for x, y in path[1:-1:3]], "w2")
    return pid


def _moss(p, cx, cy, rx, ry, ang=0.0, **kw):
    return p.blob(cx, cy, rx, ry, d_moss, ang=ang, **kw)


def dakrock(p, view, phase):
    if view in ("front", "side", "icon"):
        S = 1 if (phase == 1 and view == "front") else 0   # the sob: head and hands heave
        walk = view == "side"
        st = phase if walk else 0                            # the hem shuffling on the walk

        # crag boulders at the foot of her back
        p.poly(_closed([(46, 53), (53, 46.5), (59, 47), (62, 53), (61.5, 60.5), (46, 60.5)], 4),
               d_crag, bias=0.1, group=40)
        p.poly(_closed([(50, 34), (56, 31), (60, 34), (60.5, 41), (55, 42)], 4), d_crag, bias=0.04, group=41)

        # the veil: a curtain of flowstone from the hunched shoulders to the
        # ground, in long folds of uneven width, back to front
        p.poly(_closed([(28, 10), (40, 6), (50, 12), (55, 24), (57, 38), (57.5, 52), (55, 60.5), (34, 60.5),
                        (30, 40)], 6), d_veil, bias=0.18, group=20)
        for i, (a, m, b, w0, w1) in enumerate((((50, 15), (55, 36), (56.5, 57.5), 4.2, 5.6),
                                               ((45.5, 13), (49.5, 36), (51, 59.5 - st), 6.0, 7.4),
                                               ((40.5, 13), (43, 36), (44.5, 58), 4.4, 5.4),
                                               ((36.5, 14), (38, 36), (39, 59.5 - st), 6.4, 7.6))):
            p.limb(_spline([a, m, b], 6), w0, w1, d_veil, bias=0.1 - 0.04 * i, group=21 + i)
        # the robe in front, falling from under the hands to a flared hem
        robe = p.poly(_closed([(17, 29), (26, 28), (31, 34), (33, 46), (34, 60.5), (20, 61), (6, 60.5),
                               (5, 56.5), (8.5, 50), (11.5, 41), (14, 34)], 6), d_robe, group=1)
        p.lens((22, 36), (12, 60.2), 8.4, d_robe, bend=1.4, fat=0.66, clip=[robe], group=11)

        # the mantle over the hunched shoulders, then the hood over the
        # bowed head, set a little apart so the nape shows
        p.poly(_closed([(27, 12), (33, 6.5), (40, 4.5), (47, 6.5), (51.5, 11.5), (52, 17), (44, 18.5),
                        (36, 20), (30, 22)], 6), d_veil, group=29)
        hood = p.poly(_closed([(10.5, 19 - S), (11.5, 11.5 - S), (16, 6 - S), (23, 3.8 - S), (29.5, 5.5 - S),
                               (33.5, 11 - S), (34, 18 - S), (30.5, 25 - S), (24, 28.5 - S), (15.5, 27.5 - S)], 6),
                      d_veil, group=30)
        # the hollow of the hood and the face inside it
        p.blob(18.6, 19.8 - S, 7.4, 7.6, d_hood, ang=-14, clip=[hood], group=4)
        p.blob(17.8, 20.6 - S, 6.0, 6.0, d_skin, ang=-14, group=5)

        # the near arm in its veil-sleeve: the forearm across the body from
        # the elbow up to the wrist, the hand pressed to the near cheek
        p.limb(_spline([(33, 20), (30.5, 30), (28, 36.5)], 5), 7, 6.4, d_veil, group=31)
        p.limb(_spline([(28.5, 37.5), (20, 33.5), (11, 29.5 - S)], 5), 6.4, 5.4, d_veil, group=32)
        p.blob(11, 21.5 - S, 3.0, 5.4, d_hand, group=7)
        if p.big:
            for fx in (9, 11, 13):
                p.limb([(fx + 0.5, 20 - S), (fx + 0.5, 16.5 - S + abs(fx - 11) * 0.6)], 2.0, 1.8, d_hand, group=8)

        # moss on the shoulders, the boulders and the robe
        if p.big:
            _moss(p, 41, 5.6, 3.6, 1.3, ang=10, group=12)
            _moss(p, 54, 48.4, 4.0, 1.3, ang=12, group=13)
            _moss(p, 9.5, 52, 2.8, 1.3, ang=-50, clip=[robe], group=15)
        else:
            _moss(p, 54, 48.4, 4.2, 1.8, ang=12, group=13)

        # two streams of tears, over the hands and down the robe to the pool
        _stream(p, [(17, 27 - S), (16.6, 36), (13.6, 46), (10.4, 52), (9.2, 57)])
        _stream(p, [(23, 27 - S), (22.8, 38), (21.2, 46), (20, 52), (19.6, 57)])
        # the pool at her feet (the follower leaves it behind)
        if not walk:
            p.blob(13, 59.4, 9.4, 2.5, d_pool, group=50)

        # face: big downcast eyes brimming with tears, no nose or mouth
        if p.big:
            p.eye(15, 17 - S, 4, 6, iris="w1", shine="white", shine_at=(1, 1))
            p.eye(21, 17 - S, 3, 6, iris="w1", shine="white", shine_at=(1, 1))
        else:
            p.px(16, 20, "ink")
            p.px(22, 20, "ink")
        return

    if view == "back":
        # over the shoulder at 1.2x, from behind and to her left: the veil
        # falls down her back like a cliff face, crags break out low on the
        # left, and the hood is bowed to the right into her hands, so no
        # face shows at all, only the tears running from under it
        p.poly(_closed([(8, 40), (13, 33), (18, 36), (19, 50), (16, 64), (0, 64), (1, 50)], 4),
               d_crag, bias=0.08, group=40)
        p.poly(_closed([(-1, 56), (6, 50), (14, 52), (18, 64), (-1, 64)], 4), d_crag, bias=0.16, group=41)
        # the curtain of the veil down her back
        p.poly(_closed([(14, 22), (22, 12), (34, 9), (46, 12), (54, 22), (57, 36), (58, 50), (59, 64),
                        (14, 64), (12, 44)], 6), d_veil, bias=0.16, group=20)
        for i, (a, b, w0, w1) in enumerate((((50, 26), (56, 64), 6.4, 8), ((44, 24), (48, 64), 7, 8.6),
                                            ((38, 22), (39.5, 64), 7, 8.6), ((31, 21), (31, 64), 7, 8.6),
                                            ((24, 22), (22.5, 64), 6.4, 8))):
            p.limb(_spline([a, ((a[0] + b[0]) / 2 - 0.6, (a[1] + b[1]) / 2), b], 6), w0, w1, d_veil,
                   bias=0.1 - 0.03 * i, group=21 + i)
        # the hunched shoulders and the bowed hood in right profile
        p.poly(_closed([(13, 26), (17, 15), (26, 8), (36, 6.5), (44, 9), (48, 16), (44, 24), (34, 27),
                        (22, 28)], 6), d_veil, group=30)
        hood = p.poly(_closed([(34, 22), (36, 13), (42, 7.5), (50, 7), (56, 11), (59.5, 18), (60, 26),
                               (57.5, 33), (52, 36), (44, 34), (37, 30)], 6), d_veil, group=31)
        # the far hand, just showing at the hood's edge, cupped to the face
        p.blob(57, 32.5, 3.4, 3.0, d_hand, ang=20, group=6)
        if p.big:
            _moss(p, 25, 10.5, 4.6, 1.4, ang=-24, group=10)
            _moss(p, 9, 34.5, 3.6, 1.3, ang=-30, group=11)
            _moss(p, 6, 51.2, 4.2, 1.3, ang=-20, group=12)
        _stream(p, [(57.5, 35.5), (58.5, 42), (58, 52), (58.5, 63.5)], w=1.8)
        return

    if view in ("down", "up"):
        # follower: the bowed, veiled figure gliding forward on its hem; the
        # hem's folds and the tears trade places step to step
        st = phase
        down = view == "down"
        # the veil's curtain, flaring to the ground
        p.poly(_closed([(32, 8), (42, 11), (47, 22), (50, 36), (53, 50), (54, 59), (44, 60.5 - st), (32, 61),
                        (20, 60.5 - (1 - st)), (10, 59), (11, 50), (14, 36), (17, 22), (22, 11)], 6),
               d_veil, bias=0.12, group=20)
        for i, (x0, x1) in enumerate(((19, 13.5), (26, 23), (38, 41), (45, 50.5))):
            if down and 24 < x0 < 40:
                continue
            p.limb(_spline([(x0, 26), ((x0 + x1) / 2, 44), (x1, 58.5 - (st if x0 > 32 else 1 - st))], 5),
                   5.4, 6.4, d_veil, bias=0.08, group=21 + i)
        if down:
            # the robe in front, the arms folded up to the face in their
            # sleeves, the hood, the face, the hands pressed to the cheeks
            p.poly(_closed([(26, 30), (38, 30), (41, 44), (43, 59), (32, 60), (21, 59), (23, 44)], 6),
                   d_robe, group=1)
            p.limb(_spline([(21, 36), (24, 33), (25.4, 27)], 5), 6.4, 5.4, d_veil, group=30)
            p.limb(_spline([(43, 36), (40, 33), (38.6, 27)], 5), 6.4, 5.4, d_veil, group=31)
            hood = p.blob(32, 16, 11, 10, d_veil, group=32)
            p.blob(32, 19.5, 6.8, 7.2, d_hood, clip=[hood], group=4)
            p.blob(32, 20.5, 5.6, 5.8, d_skin, group=5)
            p.blob(25.6, 22.6, 2.4, 3.8, d_hand, group=6)
            p.blob(38.4, 22.6, 2.4, 3.8, d_hand, group=7)
            _stream(p, [(28.5, 26), (27.5, 34), (25.5, 46), (24.5, 58)])
            _stream(p, [(35.5, 26), (36.5, 34), (38.5, 46), (39.5, 58)])
            p.eye(27.5, 17, 3, 5, iris="w1", shine="white", shine_at=(1, 1))
            p.eye(33.5, 17, 3, 5, iris="w1", shine="white", shine_at=(1, 1))
        else:
            # from behind: the veil fanning from the bowed head down the
            # back, moss on the crown and a boulder at the hem
            p.blob(32, 18, 12, 11, d_veil, group=32)
            for i, (x0, x1) in enumerate(((27, 22), (32, 32), (37, 42))):
                p.limb(_spline([(x0, 24), ((x0 + x1) / 2, 42), (x1, 58.5 - (st if i != 1 else 1 - st))], 5),
                       5.4, 7, d_veil, bias=0.06 * (i % 2), group=33 + i)
            p.poly(_closed([(40, 52), (47, 47), (54, 51), (55, 60.5), (41, 60.5)], 4), d_crag, group=40)
            _moss(p, 32, 8, 4.6, 1.6, group=10)
            _moss(p, 47.5, 47.6, 4, 1.4, ang=20, group=11)
        return


MONS = [
    # icon palette 3 keeps the gray stone gray and the tears blue
    Mon("Dakrock", DAKROCK_COLORS, DAKROCK_SHINY, dakrock, foot="blank", icon_pal=3),
]
