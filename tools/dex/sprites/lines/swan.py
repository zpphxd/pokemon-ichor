"""Swan line: Hymnet, Hymnaria (Fire, then Fire/Flying). Apollo's singing
swans, which drew his chariot to the Hyperboreans."""
import math

from mon_lib import C, Mat, Mon, bez3, ellipse_pts, lerp, ribbon

INK = C.ink


# --------------------------------------------------------------------------
# Hymnet, the sun cygnet
# --------------------------------------------------------------------------

HYMNET_COLORS = [
    ("ink", INK),
    # marble-gray down
    ("d0", (80, 80, 96)), ("d1", (128, 128, 144)), ("d2", (176, 176, 184)), ("d3", (216, 216, 216)),
    ("white", C.white),
    # ember wingtips: terracotta to sun-gold to a white-hot glow
    ("em0", (176, 56, 24)), ("em1", (232, 120, 32)), ("em2", (248, 184, 56)), ("em3", (248, 240, 168)),
    # the spring water
    ("aq0", (40, 88, 160)), ("aq1", (96, 152, 216)), ("aq2", (168, 216, 240)),
]
HYMNET_SHINY = {
    # limestone-tan down, Aegean-blue ember tips
    "d0": (120, 96, 64), "d1": (168, 136, 88), "d2": (208, 176, 128), "d3": (232, 216, 176),
    "em0": (24, 48, 112), "em1": (48, 104, 184), "em2": (104, 168, 232), "em3": (192, 232, 248),
}

h_down = Mat(["d0", "d1", "d2", "d3"], line="d0", cuts=[0.3, 0.56, 0.8])
h_head = Mat(["d1", "d2", "d3", "white"], line="ink", cuts=[0.3, 0.56, 0.8])
h_beak = Mat(["ink", "d0"], line="ink", cuts=[0.6])
h_ember = Mat(["em0", "em1", "em2", "em3"], line="em0", outline="ink", cuts=[0.2, 0.45, 0.7])
h_water = Mat(["aq0", "aq1", "aq2"], line="aq0", outline="aq0", cuts=[0.3, 0.62])


def _ember_wing(p, root, tip, w, far=False, bend=1.2, **kw):
    """A stubby downy wing from root to tip, its end glowing like a coal:
    a curved leading edge, a rounded paddle of down and short primaries
    that run from sun-gold to a white-hot point."""
    b = 0.3 if far else kw.pop("bias", 0.0)
    pid = p.lens(root, tip, w, h_down if far else h_head, bend=bend, fat=0.62, bias=b, **kw)
    kw.pop("group", None)
    p.lens(lerp(root, tip, 0.5), tip, w * 0.95, h_ember, bend=bend * 0.5, fat=0.4, clip=[pid], flat=1, **kw)
    p.lens(lerp(root, tip, 0.68), tip, w * 0.66, h_ember, bend=bend * 0.3, fat=0.4, clip=[pid], flat=2,
           noline=True, **kw)
    if p.big:
        p.lens(lerp(root, tip, 0.84), tip, w * 0.34, h_ember, fat=0.5, clip=[pid], flat=3, noline=True, **kw)
    return pid


def _ripple(p, cx, cy, rx, ry, front, **kw):
    """Half of a ripple ring on the water: the back half (drawn first) or the
    front half (drawn over the swimmer's waterline)."""
    outer = ellipse_pts(cx, cy, rx, ry, n=40)
    inner = ellipse_pts(cx, cy, rx - 3.2, ry - 1.3, n=40)
    half = lambda pts: [q for q in pts if (q[1] >= cy) == front]
    o, i = half(outer), half(inner)
    o.sort(key=lambda q: q[0]); i.sort(key=lambda q: -q[0])
    return p.poly(o + i, h_water, **kw)


def hymnet(p, view, phase):
    if view in ("front", "side", "icon"):
        F = phase == 1 and view == "front"     # frame 2: a peep, the wing lifts
        L = 1 if F else 0

        # ---- the ripple behind it
        _ripple(p, 34, 55, 17, 3.4, front=False, flat=1, group=40)

        # ---- far wing, a glowing stub peeking over the back
        _ember_wing(p, (40, 46), (50, 39.5 - L), 6.4, far=True, bend=-1.0, group=10)

        # ---- body: a round ball of down, tail tuft up behind
        p.blob(46, 46, 4.0, 3.0, h_down, ang=-30, group=1, bias=0.05)
        p.blob(35, 48, 11.4, 8.4, h_down, group=1)
        # ---- head: big and round, the neck tucked down into the body
        p.blob(25.5, 37 - L, 7.6, 7.2, h_head, group=3)
        # a curl of down on the crown
        p.lens((26, 31 - L), (23.5, 27 - 2 * L), 3.0, h_head, bend=1.2, group=3)
        # ---- beak: short and dark
        p.lens((19.5, 38.5 - L), (13.5, 39.6 - L), 3.6, h_beak, bend=-0.4, fat=0.3, group=5)

        # ---- near wing, stubby and raised
        _ember_wing(p, (32.5, 46.5), (42.5, 30.5 - 2 * L), 8.6, bend=2.0, group=11, bias=-0.12)

        # ---- the ripple in front, over its waterline
        _ripple(p, 34, 55, 17, 3.4, front=True, flat=1, group=41)

        if p.big:
            p.eye(20, 34 - L, 3, 5, shine="white", shine_at=(1, 1))
        else:
            p.px(21, 36, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the round downy back cropped by
        # the frame, the head turned right in profile, the near wing raised
        _ember_wing(p, (40, 54), (54, 45), 8.0, far=True, bend=1.2, group=10)
        p.blob(27, 58, 21, 14.5, h_down, group=1)
        p.blob(43, 47, 6.5, 6, h_down, group=1)
        p.blob(44.5, 33, 9.0, 8.6, h_head, group=3)
        p.lens((43.5, 25.5), (40, 20), 3.6, h_head, bend=-1.4, group=3)
        p.lens((52.5, 34), (60, 35.8), 4.4, h_beak, bend=0.5, fat=0.3, group=5)
        _ember_wing(p, (20, 52), (5, 36), 10.4, bend=-2.4, group=11, bias=-0.1)
        if p.big:
            p.eye(47, 29, 3, 5, shine="white", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower: paddling toward or away from the camera, the wings
        # bobbing in turn, a wisp of steam rising off the water
        st = phase
        down = view == "down"
        _ripple(p, 32, 55.5, 15, 3.2, front=False, flat=1, group=40)
        for sx, lift in ((-1, st), (1, 1 - st)):
            _ember_wing(p, (32 + sx * 7, 47), (32 + sx * 15, 39 - 2 * lift), 6.4, bend=1.0 * sx * (1 if down else -1),
                        group=10 + (sx > 0), bias=0.05)
        p.blob(32, 48, 10.5, 8.0, h_down, group=1)
        if not down:
            p.blob(32, 43, 3.4, 3.0, h_down, group=1)
        p.blob(32, 35, 7.6, 7.0, h_head, group=3)
        p.lens((32, 29), (30, 24.5), 3.0, h_head, bend=1.0, group=3)
        if down:
            p.lens((32, 37), (32, 41.5), 3.6, h_beak, fat=0.3, group=5)
            p.eye(26.5, 31.5, 3, 4, shine="white", shine_at=(1, 1))
            p.eye(34.5, 31.5, 3, 4, shine="white", shine_at=(1, 1))
        _ripple(p, 32, 55.5, 15, 3.2, front=True, flat=1, group=41)
        if p.big:
            p.lens((47 - 30 * st, 54), (49 - 30 * st, 47), 2.6, h_down, bend=1.0, flat=3, nooutline=True)
        return


# --------------------------------------------------------------------------
# Hymnaria, the swan of Apollo
# --------------------------------------------------------------------------

HYMNARIA_COLORS = [
    ("ink", INK),
    # marble-white plumage with cool, lilac shadows
    ("w0", (112, 112, 152)), ("w1", (168, 168, 200)), ("w2", (216, 216, 232)), ("w3", (248, 248, 240)),
    # sun-gold primaries, burning
    ("g0", (200, 112, 32)), ("g1", (240, 176, 48)), ("g2", (248, 232, 136)),
    ("f0", (176, 40, 24)), ("f1", (240, 104, 32)),
    # the bill
    ("bill", (232, 96, 56)),
    # the Kastalian spring
    ("aq0", (40, 88, 160)), ("aq1", (96, 152, 216)), ("aq2", (168, 216, 240)),
]
HYMNARIA_SHINY = {
    # black plumage, Aegean-blue flames: a black swan at night
    "w0": (24, 24, 40), "w1": (56, 56, 80), "w2": (96, 96, 128), "w3": (152, 152, 184),
    "g0": (40, 88, 176), "g1": (96, 160, 232), "g2": (184, 224, 248),
    "f0": (24, 40, 120), "f1": (48, 104, 200),
}

s_plume = Mat(["w0", "w1", "w2", "w3"], line="w0", cuts=[0.16, 0.42, 0.7])
s_wing = Mat(["w0", "w1", "w2", "w3"], line="w0", cuts=[0.2, 0.46, 0.74])
s_gold = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.3, 0.62])
s_fire = Mat(["f0", "f1", "g1", "g2"], line="f0", outline="f0")
s_bill = Mat(["f0", "bill", "g2"], line="f0", cuts=[0.12, 0.86])
s_water = Mat(["aq0", "aq1", "aq2"], line="aq0", outline="aq0", cuts=[0.3, 0.62])
s_halo = Mat(["g1", "g2"], line="g1", outline="g1", cuts=[0.5])


def _sflame(p, a, b, w, bend=0.0, **kw):
    pid = p.lens(a, b, w, s_fire, bend=bend, fat=0.3, flat=1, **kw)
    kw.pop("group", None)
    p.lens(a, lerp(a, b, 0.6), w * 0.6, s_fire, bend=bend * 0.6, fat=0.3, flat=2,
           noline=True, nooutline=True, clip=[pid], **kw)
    if p.big:
        p.lens(a, lerp(a, b, 0.3), w * 0.32, s_fire, bend=bend * 0.3, fat=0.3, flat=3,
               noline=True, nooutline=True, clip=[pid], **kw)
    return pid


def _mass_wing(p, arm, wr, prims, secs, band, band_off=(0.0, 0.0), step=0, flames=(), dy=0.0, lit=1, group=60):
    """A raised wing blocked in grouped value masses, the way the battle art
    is painted: white coverts along a curved leading edge (arm, shoulder to
    wrist), pale-gold secondaries hanging from the forearm, sun-gold
    primaries fanning from the wrist with tips of different lengths, and
    burning tips. Each mass is one group, so only the group edges get lines.
    step=1 paints it one value step darker (the far wing).

    prims: [(angle, length, width)] from the wrist.
    secs:  [(t, (dx, dy), length, (ox, oy))]: a secondary rooted at t along
           the arm (0 shoulder, 1 wrist), offset by (ox, oy), hanging along
           (dx, dy)."""
    sh = lambda q: (q[0], q[1] + dy)
    wx, wy = sh(wr)
    ptips = []
    for ang, L, w in prims:
        a = math.radians(ang)
        tip = (max(1.4, min(62.4, wx + L * math.cos(a))), max(1.4, wy + L * math.sin(a)))
        root = (wx + 3 * math.cos(a), wy + 3 * math.sin(a))
        p.lens(root, tip, w, s_gold, fat=0.42, flat=1 - step, group=group)
        ptips.append((root, tip))
    path = [sh(q) for q in bez3(*arm, n=24)]

    def at(t):
        k = t * (len(path) - 1)
        i = min(int(k), len(path) - 2)
        return lerp(path[i], path[i + 1], k - i)
    for t, (dx, dy2), L, (ox, oy) in secs:
        r0 = at(t)
        r0 = (r0[0] + ox, r0[1] + oy)
        tip = (max(1.4, min(62.4, r0[0] + dx * L)), r0[1] + dy2 * L)
        p.lens(r0, tip, 8.0, s_gold, bend=-1.0 * lit, fat=0.58, flat=2 - step, group=group + 1)
    cov = ribbon([(x + band_off[0], y + band_off[1]) for x, y in path], lambda t: band[0] + (band[1] - band[0]) * t)
    p.add(p.mask(cov, ellipse_pts(wx, wy + 1, 3.4, 3.0)), s_wing, flat=3 - step, group=group + 2)
    for root, tip in ptips:
        p.lens(lerp(root, tip, 0.8), tip, 3.6, s_fire, fat=0.4, flat=1, group=group + 3)
    if p.big:
        for k, h in flames:
            tx, ty = ptips[k][1]
            h = min(h, ty - 0.8)
            if h >= 2.5:
                _sflame(p, (tx - 0.4 * lit, ty + 0.8), (tx + 1.0 * lit, ty - h), 3.2, bend=-0.9 * lit)
    return ptips


def _broad_wing(p, inner, outer, prim_y, step=0, lit=1, flames=(), group=60):
    """A raised wing seen head-on or from behind as one broad feathered
    shape: a smooth curved leading edge on the inside (inner, shoulder to
    top) and an outer edge cut into feather tips (outer, top to bottom).
    Pale-gold secondaries fill it, sun-gold primaries take the top above
    prim_y, white coverts run along the leading edge, and the top tips burn."""
    pid = p.poly(inner + outer, s_gold, flat=2 - step, group=group)
    p.poly([(-4, -4), (68, -4), (68, prim_y), (-4, prim_y)], s_gold, clip=[pid], flat=1 - step, group=group)
    p.add(p.mask(ribbon(inner, lambda t: 11 - 3 * t)), s_wing, clip=[pid], flat=3 - step, group=group + 1)
    for tx, ty in outer[::2]:
        if ty < prim_y - 6:
            p.circle(tx + 0.5 * lit, ty + 1.6, 1.8, s_fire, clip=[pid], flat=1, group=group + 2)
    if p.big:
        for k, h in flames:
            tx, ty = outer[k]
            if ty - h > 0.8:
                _sflame(p, (tx, ty + 0.8), (tx - 1.0 * lit, ty - h), 3.0, bend=0.9 * lit)
    return pid


def _fan_pair(p, dy=(0.0, 0.0), step=(0, 0)):
    """Both wings raised and opened into wide fans, a V around the head (the
    follower views, head-on or from behind)."""
    for sx, d, st in ((-1, dy[0], step[0]), (1, dy[1], step[1])):
        X = lambda x: 32 + sx * (x - 32)
        inner = [(X(27.5), 50), (X(24), 42), (X(21.5), 34), (X(20), 26), (X(19.5), 18), (X(20), 10 - d)]
        outer = [(X(18.5), 3.0 - d), (X(15.6), 8.4 - d), (X(12), 2.6 - d), (X(10.6), 9.6 - d), (X(6.6), 4.8 - d),
                 (X(6.4), 11.6 - d), (X(2.6), 9.6 - d), (X(4.4), 15.6 - d), (X(1.8), 17.6), (X(4.4), 21.4), (X(2.4), 26),
                 (X(5.6), 29), (X(4.8), 34), (X(8.4), 36.6), (X(8.6), 42), (X(12.4), 44.4), (X(14.4), 49), (X(20), 52)]
        _broad_wing(p, inner, outer, prim_y=20 - d, step=st, lit=-sx, flames=((0, 3.6), (2, 4.4)),
                    group=60 + 10 * (sx > 0))


def hymnaria(p, view, phase):
    if view in ("front", "side", "icon"):
        F = phase == 1 and view == "front"     # frame 2: the song swells, wings lift
        W = 1 if F else 0
        H = 1 if F else 0

        # ---- the ripple behind it
        _ripple_s(p, 36, 57.5, 23, 3.6, front=False, flat=1)

        # ---- far wing: spread up and back behind the neck, its fan arching
        # over the sun-disc, one value step darker than the near wing
        fw = (22, 9.5 - W)
        fprims = []
        for tx, ty, w in ((26.5, 1.4, 4.6), (19.5, 1.2, 5.2), (13.0, 1.6, 5.6), (7.5, 3.6, 5.6), (3.2, 8.0, 5.0)):
            ty = max(1.4, ty - W)
            fprims.append((math.degrees(math.atan2(ty - fw[1], tx - fw[0])), math.hypot(tx - fw[0], ty - fw[1]), w))
        _mass_wing(p, ((37, 45), (35, 32), (31, 18), (22.5, 10 - W)), fw, fprims,
                   [(0.84, (0.86, -0.5), 9.0, (1.6, 1.6)), (0.68, (0.95, -0.28), 10.0, (2.0, 1.4)),
                    (0.5, (0.98, 0.08), 9.5, (2.2, 1.0)), (0.32, (0.86, 0.48), 8.0, (2.2, 0.8))],
                   (9.0, 6.0), band_off=(2.4, 1.0), step=1, flames=((1, 3.0), (3, 3.2)), group=40)

        # ---- the sun-disc halo behind the head
        if p.big:
            ring = ellipse_pts(15.5, 18.5 - H, 10.0, 10.0, n=48)
            inner = ellipse_pts(15.5, 18.5 - H, 8.2, 8.2, n=48)
            p.add(p.mask(ring) & ~p.mask(inner), s_halo, flat=1, nooutline=True, noline=True)

        # ---- body: a long boat of white plumage, breast forward, tail up
        body = bez3((19.5, 50), (19.5, 43), (30, 41), (40, 42)) + bez3((40, 42), (50, 42), (55, 40), (57.5, 43))[1:] + \
            bez3((57.5, 43), (55.5, 48), (51.5, 56.5), (40, 57.5))[1:] + bez3((40, 57.5), (28, 58.5), (19.5, 56), (19.5, 50))[1:]
        p.poly(body, s_plume, group=1)

        # ---- neck: the high S, then the small head
        neck = bez3((26, 47), (11, 40), (27, 31 - H), (16.5, 23 - H))
        p.limb(neck, 8.6, 6.0, s_plume, group=2)
        p.poly([(9.5, 18.5 - H), (10.5, 15.5 - H), (13, 13.6 - H), (16.5, 13.4 - H), (19.4, 14.8 - H), (21, 17.6 - H),
                (21, 21 - H), (20, 24 - H), (17, 25.5), (14, 24.5 - H), (11, 22.5 - H)], s_plume, group=2)
        # bill, open in song: the upper mandible and the lower
        p.lens((10.5, 18 - H), (1.5, 20.5 - H), 3.6, s_bill, bend=0.5, fat=0.25, group=3)
        p.lens((10.5, 21), (4, 23.5), 2.6, s_bill, bend=-0.3, fat=0.25, group=4, bias=0.2)

        # ---- near wing: big and sweeping, a sun-fan of burning primaries
        _mass_wing(p, ((36, 46), (33.5, 37), (37, 28.5), (46, 22 - W)), (45.5, 23 - W),
                   [(-92 - 4 * W, 20.5, 5.0), (-73 - 4 * W, 21.0, 5.6), (-54 - 4 * W, 20.0, 5.8),
                    (-36 - 4 * W, 18.5, 5.8), (-18 - 4 * W, 16.5, 5.6), (0 - 4 * W, 14.5, 5.2)],
                   [(0.92, (0.93, 0.36), 17.0, (3.2, 1.4)), (0.76, (0.84, 0.54), 18.0, (3.2, 1.4)),
                    (0.6, (0.74, 0.67), 17.0, (3.2, 1.4)), (0.44, (0.62, 0.78), 15.0, (3.2, 1.4)),
                    (0.28, (0.5, 0.87), 12.0, (3.2, 1.4)), (0.14, (0.4, 0.92), 8.5, (3.0, 1.4))],
                   (10.5, 7.0), band_off=(3.4, 1.4), flames=((1, 6.0), (3, 6.6), (4, 4.2)), group=50)

        # ---- the ripple in front
        _ripple_s(p, 36, 57.5, 23, 3.6, front=True, flat=1)

        if p.big:
            p.eye(14, 16 - H, 2, 3, shine="w3", shine_at=(1, 1))
            p.pxs([(9, 16 - H), (10, 16 - H), (9, 17 - H)], "ink")       # the black knob
        else:
            p.px(14.5, 17.5, "ink")
        return

    if view == "back":
        # over the shoulder (the hand-finished art replaces this): both wings
        # opened into wide fans, a V around the head turned right in profile
        _fan_pair(p, step=(0, 1))
        if p.big:
            ring = ellipse_pts(28.5, 17.5, 10.0, 10.0, n=48)
            inner = ellipse_pts(28.5, 17.5, 8.2, 8.2, n=48)
            p.add(p.mask(ring) & ~p.mask(inner), s_halo, flat=1, nooutline=True, noline=True)
        p.blob(32, 62, 24, 13, s_plume, group=1)
        p.limb(bez3((31, 62), (24, 48), (35, 40), (28, 26)), 11.5, 7.6, s_plume, group=2)
        p.blob(29, 18, 7.6, 6.4, s_plume, ang=8, group=2)
        p.lens((35, 16), (46, 18.5), 4.4, s_bill, bend=-0.6, fat=0.25, group=3)
        p.lens((35, 20), (43, 23), 3.0, s_bill, bend=0.4, fat=0.25, group=4, bias=0.2)
        if p.big:
            p.eye(30, 15, 2, 3, shine="w3", shine_at=(0, 1))
        return

    if view in ("down", "up"):
        # follower: gliding toward or away from the camera, wings raised in
        # a V, their burning tips flickering in turn
        st = phase
        down = view == "down"
        _ripple_s(p, 32, 56, 17, 3.2, front=False, flat=1)
        # both wings open into wide fans, a V around the head; their burning
        # tips lift in turn
        _fan_pair(p, dy=(st, 1 - st))
        p.blob(32, 49, 11, 7.5, s_plume, group=1)
        p.limb([(32, 46), (32, 28)], 7.4, 6.0, s_plume, group=2)
        p.blob(32, 24, 5.4, 5.0, s_plume, group=2)
        if down:
            p.lens((32, 26), (32, 34), 3.6, s_bill, fat=0.3, group=3)
            p.eye(28, 22, 2, 3, shine="w3", shine_at=(0, 0))
            p.eye(35, 22, 2, 3, shine="w3", shine_at=(1, 0))
        _ripple_s(p, 32, 56, 17, 3.2, front=True, flat=1)
        return


def _ripple_s(p, cx, cy, rx, ry, front, **kw):
    outer = ellipse_pts(cx, cy, rx, ry, n=48)
    inner = ellipse_pts(cx, cy, rx - 3.6, ry - 1.4, n=48)
    half = lambda pts: [q for q in pts if (q[1] >= cy) == front]
    o, i = half(outer), half(inner)
    o.sort(key=lambda q: q[0]); i.sort(key=lambda q: -q[0])
    return p.poly(o + i, s_water, **kw)


MONS = [
    Mon("Hymnet", HYMNET_COLORS, HYMNET_SHINY, hymnet, foot="webbed"),
    Mon("Hymnaria", HYMNARIA_COLORS, HYMNARIA_SHINY, hymnaria, foot="webbed"),
]
