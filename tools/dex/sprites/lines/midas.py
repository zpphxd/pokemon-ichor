"""Midas line: Onotis, Midonos (Normal, then Normal/Steel). King Midas, who
turned all he touched to gold and was given a donkey's ears by Apollo."""
from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Onotis, the big-eared foal
# --------------------------------------------------------------------------

ONOTIS_COLORS = [
    ("ink", INK),
    # limestone-gray coat, warm in the shadows
    ("coat0", (88, 80, 80)), ("coat1", (128, 120, 112)), ("coat2", (168, 160, 152)), ("coat3", (208, 200, 192)),
    # marble muzzle, belly and eye ring
    ("pale", (232, 224, 208)), ("white", C.white),
    # bristly mane, ear rims, tail tuft and hooves
    ("mane", (56, 48, 48)),
    # terracotta ear insides
    ("terra0", (168, 80, 56)), ("terra1", (216, 128, 96)), ("terra2", (240, 184, 152)),
    ("iris", (96, 64, 48)),
]
ONOTIS_SHINY = {
    # a pale sun-gold coat, as if Midas had patted it
    "coat0": (160, 112, 40), "coat1": (208, 160, 64), "coat2": (232, 200, 104), "coat3": (248, 232, 160),
    "pale": (248, 240, 208), "mane": (112, 72, 32),
}

o_coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.42, 0.7])
o_pale = Mat(["coat2", "pale", "white"], line="coat1", cuts=[0.36, 0.72])
o_ear_in = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.3, 0.62])
o_mane = Mat(["mane", "coat0"], line="mane", cuts=[0.62])
o_hoof = Mat(["mane", "coat0"], cuts=[0.6])


def _ear(p, base, tip, w, mat, inner, bend=0.0, far=False, show=0.55, group=None):
    """A long donkey ear from base to tip: the gray outer ear, its terracotta
    inside (show: how wide a share of it faces us) and a dark rim at the tip."""
    b = 0.22 if far else 0.0
    pid = p.lens(base, tip, w, mat, bend=bend, fat=0.42, bias=b, group=group)
    if show > 0:
        ix = base[0] + (tip[0] - base[0]) * 0.12
        iy = base[1] + (tip[1] - base[1]) * 0.12
        jx = base[0] + (tip[0] - base[0]) * 0.86
        jy = base[1] + (tip[1] - base[1]) * 0.86
        p.lens((ix, iy), (jx, jy), w * show, inner, bend=bend * 0.8, fat=0.45, clip=[pid], bias=b)
    # dark rim around the tip
    kx = base[0] + (tip[0] - base[0]) * 0.8
    ky = base[1] + (tip[1] - base[1]) * 0.8
    p.lens((kx, ky), (tip[0] + (tip[0] - base[0]) * 0.1, tip[1] + (tip[1] - base[1]) * 0.1), w * 0.8,
           Mat(["mane"]), clip=[pid], noline=True)
    return pid


def _foal_hoof(p, x, y, far=False):
    """A small dark hoof whose top-left is at (x, y): 3 wide, 2 tall."""
    p.rect(x, y, x + 2, y + 1, o_hoof, bias=0.3 if far else 0)


def _bristles(p, pts, mat, h=2.2, w=2.6, n=None, group=60):
    """A short upright donkey mane along pts (poll first): a dark ridge with
    a row of bristly tufts standing out on its left-hand side."""
    import math
    p.limb(pts, w, w * 0.8, mat, group=group)
    segs = list(zip(pts, pts[1:]))
    n = n or max(3, int(sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs) / 2.6))
    tot = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
    for i in range(n):
        d = (i + 0.5) / n * tot
        for a, b in segs:
            ln = math.hypot(b[0] - a[0], b[1] - a[1])
            if d <= ln:
                break
            d -= ln
        k = d / ln if ln else 0
        x, y = a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
        ux, uy = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
        nx, ny = uy, -ux             # left-hand normal of the path
        hh = h * (0.8 + 0.4 * ((i * 7) % 3) / 2)
        tip = (x + nx * (w / 2 + hh) - ux * 0.8, y + ny * (w / 2 + hh) - uy * 0.8)
        p.poly([(x - ux * 1.1, y - uy * 1.1), tip, (x + ux * 1.1, y + uy * 1.1)], mat, group=group)


def onotis(p, view, phase):
    if view in ("front", "side", "icon"):
        walk = view == "side"
        L = 1 if (phase == 1 and not walk) else 0       # head lifts
        sw = 1 if (phase == 1 and not walk) else 0      # ears swivel
        D = 2                                            # everything above the legs

        # legs: (hip, knee, foot); splayed like a foal finding its feet
        if walk and phase:
            far_front = [(34, 50.5), (33.5, 55), (33, 59)]
            far_hind = [(41, 50.5), (43.5, 55), (43, 59)]
            near_front = [(30.5, 50.5), (28.5, 55), (28, 59)]
            near_hind = [(44.5, 49.5), (46, 54.5), (46.5, 59)]
        else:
            far_front = [(34, 50.5), (35, 55), (35.5, 59)]
            far_hind = [(41, 50.5), (41.5, 55), (40.5, 59)]
            near_front = [(30.5, 50.5), (28.5, 55), (26.5, 59)]
            near_hind = [(44.5, 49.5), (47, 54.5), (48, 59)]

        p.limb(far_front, 3.4, 2.6, o_coat, bias=0.42, group=10)
        p.limb(far_hind, 3.6, 2.6, o_coat, bias=0.42, group=11)
        if p.big:
            p.blob(far_front[1][0], far_front[1][1], 2.0, 1.6, o_coat, bias=0.42, group=10)
            p.blob(far_hind[1][0], far_hind[1][1], 2.0, 1.6, o_coat, bias=0.42, group=11)
        _foal_hoof(p, int(far_front[-1][0]) - 1, 59, far=True)
        _foal_hoof(p, int(far_hind[-1][0]) - 1, 59, far=True)

        # tail: a thin switch ending in a dark tuft
        p.limb(bez((46.5, 43 + D), (49.5, 44 + D), (50, 48 + D)), 1.9, 1.5, o_coat)
        p.lens((49.8, 47 + D), (50.5, 53 + D), 3.8, o_mane, bend=-0.4)

        # far ear, swivelled back, behind the head
        _ear(p, (29.5, 29.5 + D - L), (40 - sw, 14 + D - L), 7.0, o_coat, o_ear_in, bend=-0.7, far=True,
             show=0.3)

        # body: a short round barrel on gangly legs
        body = p.blob(38.5, 45 + D, 8, 5.6, o_coat, ang=-4, group=1)
        p.blob(32.5, 45 + D, 5, 5.4, o_coat, group=1)
        p.blob(43.5, 44 + D, 4.8, 5, o_coat, group=1)
        p.blob(38, 49.8 + D, 6.4, 2.0, o_pale, clip=[body], group=2)

        # neck, then the big head, cocked as if listening
        p.limb([(32.5, 44 + D), (30.5, 39 + D), (29, 35.5 + D - L)], 7, 6.4, o_coat, group=1)
        p.circle(25.5, 32 + D - L, 7.2, o_coat, group=3)
        # a short, round donkey muzzle
        p.limb(bez((22, 34 + D - L), (19, 35.5 + D - L), (17.5, 37.5 + D - L)), 8.4, 8.4, o_coat, group=3)
        p.blob(16.8, 37.4 + D - L, 4.2, 3.6, o_pale, ang=15, group=4)
        # short bristly mane from the poll down the crest of the neck
        _bristles(p, [(29.5, 28.5 + D - L), (31.5, 31 + D - L), (33, 35 + D), (34, 39.5 + D), (35, 43 + D)],
                  o_mane, h=1.6, w=2.2)

        # near legs, over the body, with knobbly knees
        p.limb(near_front, 3.6, 2.8, o_coat, group=12)
        p.limb([(44, 45.5 + D)] + near_hind, 6.2, 2.8, o_coat, group=13)
        if p.big:
            p.blob(near_front[1][0], near_front[1][1], 2.1, 1.7, o_coat, group=12)
            p.blob(near_hind[1][0], near_hind[1][1], 2.1, 1.7, o_coat, group=13)
        _foal_hoof(p, int(near_front[-1][0]) - 1, 59)
        _foal_hoof(p, int(near_hind[-1][0]) - 1, 59)

        # near ear, enormous, cocked forward toward a sound
        _ear(p, (24.5, 28.5 + D - L), (15.5 + sw, 11 + D - L - sw), 7.6, o_coat, o_ear_in, bend=1.0, show=0.56)

        # face
        if p.big:
            p.eye(22, 29 + D - L, 4, 5, iris="iris", shine="white", shine_at=(1, 1))
            p.pxs([(14, 36 + D - L), (15, 36 + D - L)], "ink")                # nostril
            p.stroke([(15, 39 + D - L), (18, 39.5 + D - L)], "coat1")         # mouth
        else:
            p.px(21, 31 + D - L, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the foal's back and rump, the
        # head turned right in profile, both great ears up
        _ear(p, (41.5, 28), (33, 9), 8.6, o_coat, o_ear_in, bend=0.9, far=True, show=0.0)
        p.blob(21, 61, 20, 15, o_coat, ang=-8, group=1)
        p.blob(35, 53, 11.5, 11, o_coat, group=1)
        p.limb([(36, 50), (39.5, 43), (42.5, 38)], 13, 11.5, o_coat, group=1)
        p.circle(46, 34, 8.8, o_coat, group=3)
        p.limb(bez((51, 36), (54, 37), (56, 39.5)), 10.4, 10.4, o_coat, group=3)
        p.blob(56.5, 40, 5, 4.4, o_pale, ang=-15, group=4)
        _bristles(p, [(30, 46), (33.5, 41), (36.5, 36), (39, 32), (41, 28)], o_mane, h=2.0, w=3)
        # tail tuft hanging off the rump
        p.limb(bez((4.5, 50), (2.5, 53), (3, 57)), 2.6, 2.0, o_coat)
        p.lens((3, 55.5), (4.5, 62), 4.6, o_mane)
        _ear(p, (46.5, 27), (52, 7.5), 8.8, o_coat, o_ear_in, bend=-0.8, show=0.34)
        p.eye(47, 30, 4, 5, iris="iris", shine="white", shine_at=(2, 1))
        if p.big:
            p.pxs([(60, 38), (60, 39)], "ink")
            p.stroke([(56, 43), (59, 43)], "coat1")
        return

    if view == "down":
        # follower walking toward the camera: ears up in a V
        st = phase
        p.limb([(28.5, 50), (28.5, 60 - 2 * st)], 3.2, 2.6, o_coat, group=12)
        p.limb([(35.5, 50), (35.5, 60 - 2 * (1 - st))], 3.2, 2.6, o_coat, group=13)
        _foal_hoof(p, 27, 59 - 2 * st)
        _foal_hoof(p, 34, 59 - 2 * (1 - st))
        p.blob(32, 46, 7.2, 6.6, o_coat, group=1)
        p.blob(32, 49.5, 4.4, 2.6, o_pale, group=2)
        _ear(p, (28.5, 28), (19 - st, 11), 7.2, o_coat, o_ear_in, bend=-0.8, show=0.5)
        _ear(p, (35.5, 28), (45 + (1 - st), 11), 7.2, o_coat, o_ear_in, bend=0.8, show=0.5)
        p.blob(32, 33, 6.8, 6.4, o_coat, group=3)
        p.blob(32, 39.5, 4.4, 3.6, o_pale, group=4)
        p.eye(27, 31, 2, 4, shine="white")
        p.eye(35, 31, 2, 4, shine="white")
        if p.big:
            p.pxs([(30, 40), (33, 40)], "ink")
        return

    if view == "up":
        # follower walking away: rump, tail tuft and the backs of the ears
        st = phase
        p.limb([(28.5, 50), (28.5, 60 - 2 * st)], 3.4, 2.8, o_coat, group=12)
        p.limb([(35.5, 50), (35.5, 60 - 2 * (1 - st))], 3.4, 2.8, o_coat, group=13)
        _foal_hoof(p, 27, 59 - 2 * st)
        _foal_hoof(p, 34, 59 - 2 * (1 - st))
        p.blob(32, 33, 6.6, 6.2, o_coat, group=3)
        _ear(p, (28.5, 28), (19 - st, 11), 7.2, o_coat, o_ear_in, bend=-0.8, show=0.0)
        _ear(p, (35.5, 28), (45 + (1 - st), 11), 7.2, o_coat, o_ear_in, bend=0.8, show=0.0)
        p.blob(32, 46, 7.6, 7, o_coat, group=1)
        _bristles(p, [(32, 28), (32, 33), (32, 39)], o_mane)
        p.limb([(32, 46), (32.5, 51)], 1.9, 1.5, o_coat)
        p.lens((32.5, 50), (32 + st, 57), 3.6, o_mane)
        return


# --------------------------------------------------------------------------
# Midonos, the golden donkey
# --------------------------------------------------------------------------

MIDONOS_COLORS = [
    ("ink", INK),
    # limestone-gray coat, a shade darker than the foal's
    ("coat0", (80, 72, 72)), ("coat1", (120, 112, 104)), ("coat2", (160, 152, 144)), ("coat3", (200, 192, 184)),
    ("pale", (224, 216, 200)), ("mane", (48, 40, 40)),
    # sun-gold leaf with a marble highlight
    ("gold0", (136, 80, 24)), ("gold1", (200, 136, 40)), ("gold2", (240, 192, 64)), ("gold3", (248, 232, 144)),
    ("white", C.white),
    # the terracotta Phrygian cap
    ("cap0", (112, 40, 24)), ("cap1", (176, 80, 48)), ("cap2", (224, 128, 88)),
]
MIDONOS_SHINY = {
    # the gold turns pale silver and the cap Aegean blue
    "gold0": (88, 96, 112), "gold1": (144, 152, 168), "gold2": (192, 200, 208), "gold3": (232, 232, 240),
    "cap0": (24, 56, 120), "cap1": (48, 104, 176), "cap2": (112, 168, 224),
}

m_coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.42, 0.7])
m_pale = Mat(["coat2", "pale", "white"], line="coat1", cuts=[0.36, 0.74])
m_gold = Mat(["gold0", "gold1", "gold2", "gold3"], line="gold0", cuts=[0.2, 0.46, 0.74])
m_cap = Mat(["cap0", "cap1", "cap2"], line="cap0", cuts=[0.3, 0.64])
m_mane = Mat(["mane", "coat0"], line="mane", cuts=[0.62])


def _gilt_leg(p, path, w0, w1, gild, far=False, group=None, hoof=True):
    """A thick leg along path, gold from `gild` (0..1 along it) down: the
    gold leaf climbs it in a ragged, flaking edge. The hoof is solid gold,
    flared at the bottom."""
    import math
    b = 0.36 if far else 0.0
    pid = p.limb(path, w0, w1, m_coat, bias=b, group=group)
    n = len(path) - 1
    t = gild * n
    i = min(int(t), n - 1)
    k = t - i
    gx = path[i][0] + (path[i + 1][0] - path[i][0]) * k
    gy = path[i][1] + (path[i + 1][1] - path[i][1]) * k
    ux, uy = path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]
    d = math.hypot(ux, uy) or 1
    ux, uy = ux / d, uy / d
    nx, ny = -uy, ux
    # a torn top edge across the leg, then everything below it
    ww = w0 + 3
    edge = []
    for j in range(7):
        s_ = -ww / 2 + ww * j / 6
        up = (0.0, 1.6, 0.4, 2.2, 0.2, 1.4, 0.0)[j]
        edge.append((gx + nx * s_ - ux * up, gy + ny * s_ - uy * up))
    lx, ly = path[-1]
    far_pts = [(lx + nx * ww / 2 + ux * 4, ly + ny * ww / 2 + uy * 4), (lx - nx * ww / 2 + ux * 4, ly - ny * ww / 2 + uy * 4)]
    p.poly(edge + far_pts[::-1] if False else edge + [far_pts[0], far_pts[1]][::-1], m_gold, clip=[pid], bias=b,
           group=group)
    if hoof:
        hx, hy = path[-1]
        hw = w1 / 2 + 0.6
        p.poly([(hx - hw, hy - 1.2), (hx + hw, hy - 1.2), (hx + hw + 1.2, hy + 1.6), (hx - hw - 1.2, hy + 1.6)],
               m_gold, bias=b - 0.12, group=None if group is None else group + 100)
    return pid


def _leaf_patch(p, cx, cy, rx, ry, clip, group, seed=0, ang=0.0):
    """A ragged patch of gold leaf: an ellipse with a torn, flaking rim."""
    import math
    pts = []
    n = 14
    for j in range(n):
        a = 2 * math.pi * j / n
        r = 1.0 - 0.28 * (((j * 5 + seed * 3) % 4) / 3.0)
        x, y = rx * r * math.cos(a), ry * r * math.sin(a)
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return p.poly(pts, m_gold, clip=clip, group=group)


def _phrygian(p, x, y, L=0, ear=True, flop=0, k=1, sc=0.78):
    """The floppy Phrygian cap, the front of its band at (x, y): a soft cap
    pushed up and back by the ears crushed flat under it, its tip flopping
    forward over the brow, and one ear tip escaping through a split seam.
    k=1 faces left (the cap's back to the right); k=-1 faces right."""
    def q(dx, dy):
        return (x + k * dx * sc, y + dy * sc)
    # the crown, long and lumpy over the flattened ears
    crown = p.poly(bez3(q(0, 0.5), q(-0.5, -4.5), q(6, -8), q(12, -6.5)) +
                   bez3(q(12, -6.5), q(17.5, -5), q(18.5, -0.5), q(16, 1.5)) +
                   [q(7, 2)], m_cap, group=70)
    # the soft cone, its top folding forward over the brow
    p.limb(bez3(q(8, -5), q(7.5, -10), q(3, -11.5), q(0.5 - flop, -9 + flop)), 8.6 * sc, 5.4 * sc, m_cap,
           group=70)
    cx, cy = q(0.4 - flop, -8.4 + flop)
    p.circle(cx, cy, 2.6 * sc, m_cap, group=70)
    # the band
    p.limb(bez(q(-0.5, 0.5), q(7, 3), q(16, 1)), 3.0 * sc, 2.6 * sc, m_cap, group=71)
    if ear:
        # the escaping ear tip, poking up and back through the split seam
        e = p.lens(q(11, -4), q(20, -11.5 - L), 5.8 * sc, m_coat, bend=-0.6 * k, fat=0.4, group=72)
        if p.big:
            p.lens(q(17.5, -9 - L), q(21, -12.6 - L), 4.4 * sc, Mat(["mane"]), clip=[e], noline=True)
    return crown


def _gold_hoof(p, x, y, w, far=False, tilt=0.0, group=None):
    """A solid gold hoof, its top centre at (x, y): flared, 4 px tall."""
    b = 0.3 if far else -0.1
    return p.poly([(x - w / 2 + tilt, y), (x + w / 2 + tilt, y), (x + w / 2 + 1.3, y + 3.6), (x - w / 2 - 1.3, y + 3.6)],
                  m_gold, bias=b, group=group)


def _gild(p, clip, top, bottom, x0, x1, far=False, group=None, teeth=(0, 1.8, 0.5, 2.4, 0.3, 1.5, 0)):
    """Gold leaf over part `clip` from a torn edge at `top` (y) down to
    `bottom`, across x0..x1."""
    n = len(teeth) - 1
    edge = [(x0 + (x1 - x0) * j / n, top - teeth[j]) for j in range(n + 1)]
    return p.poly(edge + [(x1, bottom), (x0, bottom)], m_gold, clip=clip, bias=0.3 if far else 0.0, group=group)


def midonos(p, view, phase):
    if view in ("front", "side", "icon"):
        walk = view == "side"
        L = 1 if (phase == 1 and not walk) else 0
        up = 1 if (phase == 1 and not walk) else 0

        # far legs, planted
        ff = p.limb([(32, 44), (32.5, 50.5), (32, 56.5)], 7, 5.4, m_coat, bias=0.36, group=10)
        _gild(p, [ff], 49, 60, 27, 37, far=True, group=10)
        _gold_hoof(p, 32, 56, 6.4, far=True, group=110)
        fh = p.limb([(44, 43), (45.5, 50), (45, 56.5)], 7, 5.4, m_coat, bias=0.36, group=11)
        _gild(p, [fh], 50, 60, 40, 50, far=True, group=11, teeth=(0, 2.2, 0.6, 1.4, 0.2, 2.0, 0))
        _gold_hoof(p, 45, 56, 6.4, far=True, group=111)

        # tail, its switch dipped in gold
        p.limb(bez((54, 31), (57.5, 33.5), (57, 40)), 2.4, 1.8, m_coat)
        p.lens((57, 38.5), (56, 48), 5.4, m_gold, bend=0.8)

        # body: neck, deep round chest, barrel and rump in one curved mass
        body = p.poly(bez3((34, 29.5), (37, 30.8), (42, 30.6), (47, 28.4)) +
                      bez3((47, 28.4), (52, 27.4), (56.5, 30), (57.5, 36)) +
                      bez3((57.5, 36), (58, 41), (55, 45), (48, 46.2)) +
                      bez3((48, 46.2), (41, 48.4), (31, 48.4), (24.5, 46.2)) +
                      bez3((24.5, 46.2), (18.5, 44.4), (16.6, 39), (18.5, 34.5)) +
                      bez3((18.5, 34.5), (19.8, 31), (22.5, 29.5), (23.5, 25)) +
                      [(25, 18), (29, 14.5)] +
                      bez3((29, 14.5), (32, 17), (32.4, 24), (34, 29.5)), m_coat, group=1)
        p.blob(36, 46, 9.5, 2.4, m_pale, clip=[body], group=2)
        # gold leaf flaking across the back and haunch
        if p.big:
            _leaf_patch(p, 43.5, 30, 7.4, 3.4, [body], 1, seed=1, ang=-8)
            _leaf_patch(p, 53.5, 37, 3.4, 4.4, [body], 1, seed=2)
            _leaf_patch(p, 34.5, 33, 3.2, 2.0, [body], 1, seed=3, ang=-8)
        else:
            _leaf_patch(p, 46, 32, 7, 4.5, [body], 1, seed=1, ang=-8)

        # near hind leg over the body: a heavy round haunch
        nh = p.poly(bez3((46, 35), (50, 30.5), (56.5, 32), (56.5, 39)) +
                    bez3((56.5, 39), (56.6, 44), (55, 47), (54.8, 50)) +
                    [(54.6, 56.8), (49.4, 56.8), (49.6, 51)] +
                    bez3((49.6, 51), (49.4, 48), (45.5, 46), (45, 42)) +
                    bez((45, 42), (44.5, 38), (46, 35)), m_coat, group=12)
        _gild(p, [nh], 49.5, 60, 47, 58, group=12, teeth=(0, 1.6, 0.4, 2.6, 0.6, 1.8, 0.2))
        _gold_hoof(p, 52, 56, 6.6, group=112)

        # neck crest mane
        _bristles(p, [(28.5, 14.5 - L), (30.5, 19 - L), (32, 24), (33.4, 29)], m_mane, h=1.6, w=2.4, group=61)
        # the head, chin held high
        p.blob(20, 19 - L, 8.2, 7.4, m_coat, ang=-12, group=3)
        p.blob(22, 24 - L, 5.6, 4.4, m_coat, ang=-25, group=3)
        p.limb(bez((16, 20.5 - L), (12, 19.5 - L), (8.5, 17.5 - L)), 9.8, 8.4, m_coat, group=3)
        p.blob(8.2, 18.6 - L, 3.8, 3.4, m_pale, ang=-24, group=4)
        # the cap
        _phrygian(p, 13, 14.5 - L, L, flop=up)

        # near foreleg raised: the forearm thrust forward, the gilded hoof
        # lifted and turned up to show off
        nf = p.limb([(23.5, 42), (17.5, 47.5 - up)], 8.2, 6.6, m_coat, group=13)
        nc = p.limb([(17.5, 47.5 - up), (17, 53.5 - up)], 6.4, 5.4, m_coat, group=13)
        _gild(p, [nf, nc], 46 - up, 60, 13, 24, group=13, teeth=(0, 2.0, 0.4, 1.4, 0.2, 2.2, 0.4))
        _gold_hoof(p, 17, 53.5 - up, 6.4, tilt=-0.6, group=113)

        # face: a heavy-lidded, smug eye under the brim
        if p.big:
            p.eye(13, 16 - L, 4, 4, iris="gold1", shine="white", shine_at=(1, 2))
            p.stroke([(12, 16 - L), (17, 16 - L)], "ink")             # heavy lid
            p.pxs([(4, 17 - L), (5, 17 - L)], "ink")                  # nostril
            p.stroke([(6, 21 - L), (10, 22 - L)], "coat1")            # mouth
        else:
            p.px(15, 18 - L, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the gilded back, the head turned
        # right in profile, the cap's split seam and the escaping ear
        body = p.blob(24, 62, 23, 17, m_coat, ang=-6, group=1)
        sh = p.blob(38, 52, 12.5, 11, m_coat, group=1)
        p.limb([(38, 50), (41, 42), (43, 36)], 15, 13, m_coat, group=1)
        p.circle(45.5, 30, 9.6, m_coat, group=3)
        p.blob(42.5, 37, 6.6, 5.2, m_coat, ang=20, group=3)
        p.limb(bez((51, 32), (55.5, 31), (59, 28.5)), 11, 9.4, m_coat, group=3)
        p.blob(58.6, 29.4, 4.2, 3.8, m_pale, ang=20, group=4)
        _bristles(p, [(29, 45), (32.5, 40), (35.5, 35), (37.5, 30)], m_mane, h=1.8, w=3)
        # gold leaf flaking across the back
        _leaf_patch(p, 19, 49, 10, 4.6, [body, sh], 1, seed=1, ang=-12)
        _leaf_patch(p, 32, 56, 5, 3.4, [body, sh], 1, seed=2, ang=-20)
        _leaf_patch(p, 8, 58, 4.5, 3.2, [body], 1, seed=3)
        # tail switch, dipped in gold
        p.limb(bez((5.5, 50), (3, 53), (3.5, 57)), 2.6, 2.0, m_coat)
        p.lens((3.5, 55.5), (5, 62), 4.8, m_gold)
        _phrygian(p, 53.5, 24, k=-1, sc=1.0)
        p.eye(47, 26, 4, 4, iris="gold1", shine="white", shine_at=(2, 2))
        if p.big:
            p.stroke([(46, 26), (51, 26)], "ink")
            p.pxs([(61, 27), (61, 28)], "ink")
            p.stroke([(56, 33), (59, 32)], "coat1")
        return

    if view in ("down", "up"):
        # follower: the stocky donkey head-on (down) or from behind (up)
        st = phase
        back = view == "up"
        for x, s_ in ((27.5, st), (36.5, 1 - st)):
            pid = p.limb([(x, 48), (x, 60 - 2 * s_)], 5.2, 4.4, m_coat, group=12 + int(x))
            p.rect(x - 2.5, 55 - 2 * s_, x + 2.5, 58 - 2 * s_, m_gold, clip=[pid])
            p.blob(x, 59.5 - 2 * s_, 3.4, 1.8, m_gold)
        p.blob(32, 43, 10, 8.5, m_coat, group=1)
        if back:
            _leaf_patch(p, 32, 40, 7, 4.5, None, 1, seed=1)
            p.limb([(32, 45), (32.5, 51)], 2.4, 1.8, m_coat)
            p.lens((32.5, 50), (32 + st, 57), 4.4, m_gold)
            p.blob(32, 28, 7.6, 7.2, m_coat, group=3)
        else:
            p.blob(32, 48, 6, 2.6, m_pale, group=2)
            p.blob(32, 28, 7.6, 7.2, m_coat, group=3)
            p.blob(32, 35, 5.6, 4.6, m_pale, group=4)
            p.eye(26, 27, 3, 3, iris="gold1", shine="white", shine_at=(1, 1))
            p.eye(35, 27, 3, 3, iris="gold1", shine="white", shine_at=(1, 1))
            if p.big:
                p.pxs([(29, 36), (34, 36)], "ink")
        # the cap: crown, a cone flopping to one side, the escaping ear
        p.blob(32, 21, 8.6, 4.6, m_cap, group=70)
        p.limb(bez3((32, 20), (31, 13), (27, 11), (24, 14 + st)), 8, 5, m_cap, group=70)
        p.circle(24, 14.5 + st, 2.6, m_cap, group=70)
        p.limb([(23.5, 24), (40.5, 24)], 3, 3, m_cap, group=71)
        e = p.lens((37, 19), (43, 9), 5.4, m_coat, bend=0.6, fat=0.4)
        if p.big:
            p.lens((41, 12), (44, 7.5), 4, Mat(["mane"]), clip=[e], noline=True)
        return


MONS = [
    Mon("Onotis", ONOTIS_COLORS, ONOTIS_SHINY, onotis, foot="hoof"),
    Mon("Midonos", MIDONOS_COLORS, MIDONOS_SHINY, midonos, foot="hoof"),
]
