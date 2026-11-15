"""Belemnite line: Sepidart, Sepivolt (Rock / Electric). The thunderstones.

Belemnites were squid kin whose bullet-shaped guards turn up as fossils named
from belemnon, the Greek for dart. For centuries people took them for
thunderbolts fallen where lightning struck, Pliny's ceraunia. Sepidart is a
little squid revived with its stone guard still on its back like a sheath,
holding lightning; Sepivolt is the grown thunder-squid, its guard a spear
point and a quiver of spare darts along its back, which it fires as bolts.

The battle front and back are hand-finished in tools/dex/sprites/art/; the
drafts here set their poses and still draw the icons and the followers.
"""
from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink


# --------------------------------------------------------------------------
# Sepidart, the revived dart
# --------------------------------------------------------------------------

SEPIDART_COLORS = [
    ("ink", INK),
    # Aegean-blue body
    ("body0", (24, 48, 112)), ("body1", (48, 96, 176)), ("body2", (96, 152, 216)), ("body3", (176, 216, 240)),
    # the limestone guard with a marble sheen
    ("stone0", (128, 104, 80)), ("stone1", (176, 152, 112)), ("stone2", (216, 200, 160)), ("white", C.white),
    # sun-gold sparks
    ("gold0", (208, 136, 32)), ("gold1", (248, 200, 72)), ("spark", (248, 248, 176)),
]
SEPIDART_SHINY = {
    # the guard turns cypress-dark and the body terracotta red
    "stone0": (16, 40, 32), "stone1": (32, 72, 48), "stone2": (72, 120, 88),
    "body0": (104, 32, 24), "body1": (168, 64, 40), "body2": (216, 112, 72), "body3": (240, 176, 136),
}

s_body = Mat(["body0", "body1", "body2", "body3"], line="body0", cuts=[0.2, 0.46, 0.72])
s_arm = Mat(["body0", "body1", "body2"], line="body0", cuts=[0.4, 0.68])
s_stone = Mat(["stone0", "stone1", "stone2", "white"], line="stone0", cuts=[0.22, 0.5, 0.78])


def _spark(p, x, y, r=2, flick=0):
    """A sun-gold spark: a bright core with four rays (two long on a flick)."""
    if not p.big:
        p.px(x, y, "spark")
        return
    a, b = (r + 1, r) if flick else (r, r + 1)
    p.stroke([(x - a, y), (x + a, y)], "gold1")
    p.stroke([(x, y - b), (x, y + b)], "gold1")
    p.pxs([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)], "spark")
    p.px(x, y, "white")
    p.pxs([(x - a - 1, y), (x + a + 1, y), (x, y - b - 1), (x, y + b + 1)], "gold0")


def _arm(p, base, ctrl, tip, w0, w1, mat, curl=None, **kw):
    """A short squid arm along a curve, optionally ending in a little curl."""
    p.limb(bez(base, ctrl, tip), w0, w1, mat, **kw)
    if curl:
        p.limb(bez(tip, curl[0], curl[1]), w1, max(w1 * 0.8, 1.2), mat, **kw)


SEPIDART_EYE = [".111.", "11ww1", "111w1", "11111", "1gy11", ".1y1."]


def _guard(p, root, tip, w, mat, **kw):
    """A belemnite guard: a stone bullet, a blunt rounded front at root and
    straight sides that close to a point at tip."""
    import math
    dx, dy = tip[0] - root[0], tip[1] - root[1]
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    nx, ny = -uy, ux
    h = w / 2

    def at(t, o):
        return (root[0] + ux * d * t + nx * o, root[1] + uy * d * t + ny * o)
    pts = [at(0.0, h * 0.4), at(-0.03, 0), at(0.0, -h * 0.4)]
    pts = [at(0.02, h * 0.85)] + pts + [at(0.02, -h * 0.85)]
    side = [at(t, -h * (1.0 if t < 0.5 else (1 - t) / 0.5 * 0.95 + 0.05)) for t in (0.08, 0.3, 0.5, 0.65, 0.8, 0.92)]
    top = [at(t, h * (1.0 if t < 0.5 else (1 - t) / 0.5 * 0.95 + 0.05)) for t in (0.92, 0.8, 0.65, 0.5, 0.3, 0.08)]
    return p.poly(pts[2:] + side + [tip] + top + pts[:2], mat, **kw)


def _torpedo(cx, cy, rx, ry, ang_deg, taper=0.28, n=40):
    """Outline of a squid mantle: an ellipse along ang_deg that narrows
    toward its far (+rx) end."""
    import math
    a = math.radians(ang_deg)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        u = rx * math.cos(t)
        v = ry * math.sin(t) * (1.0 - taper * max(0.0, math.cos(t)))
        pts.append((cx + u * math.cos(a) - v * math.sin(a), cy + u * math.sin(a) + v * math.cos(a)))
    return pts


def sepidart(p, view, phase):
    if view in ("front", "side", "icon"):
        # the hand-finished battle sprite follows this pose: the mantle and
        # its stone dart angled up and back from a round head, the short
        # arms hanging under it
        b = 1.0 if (phase == 1 and view in ("front", "side")) else 0.0      # bob up
        f = 1.6 if (phase == 1 and view == "front") else 0.0                # arms draw up
        K, OX, OY = 0.84, 31.0, 41.0

        def P(x, y):
            return (OX + (x - OX) * K, OY + (y - OY) * K - b)

        def PL(pts):
            return [P(x, y) for x, y in pts]

        # far fin, peeking up behind the mantle's tip
        p.poly(PL([(34.5, 25.5), (35.5, 20.8), (39, 18.6), (41.4, 20.4), (40, 24.6)]), s_body, bias=0.3, group=11)
        # far arms, hanging in shade
        for a0, a1, a2 in (((18, 46.5), (16.4 + f, 50.6 - f), (18 + f, 53.2 - f)), ((27.4, 46.5), (29.4 - f, 50 - f), (28.2 - f, 52.8 - f))):
            p.limb(bez(*PL([a0, a1, a2])), 3.4, 2.0, s_arm, bias=0.3, group=10)
        # the mantle, rising up and back from the head
        cx, cy = P(33.6, 32.4)
        p.poly(_torpedo(cx, cy, 10.8 * K, 7.2 * K, -36), s_body, group=1)
        # near fin, a rounded flap off the mantle's tip
        fin = [(39.5, 30.6), (43.6, 27.6), (47.6, 28.4), (48.2, 31.8), (45.2, 34.4), (41.4, 34.2)] if not f else \
              [(39.5, 30.6), (43.4, 29.0), (47.8, 30.8), (48.0, 34.0), (44.8, 35.8), (41.0, 34.6)]
        p.poly(PL(fin), s_body, group=12)
        # the stone guard along the back, out to a point
        gr, gt = P(24.2, 32.0), P(50.5, 15.6)
        _guard(p, gr, gt, 6.0, s_stone, group=2)
        # head: big and round, and the siphon under it
        hx, hy = P(22, 41)
        p.blob(hx, hy, 7.8 * K, 7.2 * K, s_body, group=3)
        sx, sy = P(28.4, 45.6)
        p.blob(sx, sy, 1.9, 1.3, s_arm, group=4)
        # near arms: short and thick, tips turning in
        for a0, a1, a2 in (((15.6, 45.5), (12.6 + f * 0.6, 49.4 - f), (14.6 + f * 1.4, 52.8 - f)),
                           ((21, 47.6), (20.2 - f * 0.4, 51.6 - f), (22.6 - f * 0.6, 54.4 - f * 1.2)),
                           ((25, 47.6), (26.2 - f * 0.4, 51.4 - f), (28.4 - f * 1.2, 53.4 - f))):
            p.limb(bez(*PL([a0, a1, a2])), 3.8, 2.2, s_arm, group=13)
        if p.big:
            ex, ey = P(17.5, 37.5)
            p.patch(int(round(ex)), int(round(ey)), SEPIDART_EYE, {"1": "ink", "w": "white", "g": "gold0", "y": "gold1"})
            _spark(p, int(gt[0]), int(gt[1]), 2, phase == 1 and view == "front")
        else:
            ex, ey = P(19.5, 39.5)
            p.px(ex, ey, "ink")
            p.px(gt[0], gt[1], "spark")
        return

    if view == "back":
        # over the shoulder: the mantle cropped by the frame, the stone guard
        # along its back running down to a sparking point, the head turned
        # right with one big eye, the arms curled under it
        p.blob(5, 50, 4.4, 3.2, s_body, ang=-30, bias=0.2, group=11)
        p.blob(30, 54, 17, 12, s_body, ang=-24, group=1)
        p.blob(12.5, 58.5, 5.6, 3.6, s_body, ang=-10, group=12)
        _guard(p, (44, 35), (6, 53), 11.0, s_stone, group=2)
        p.blob(47.5, 36, 9.4, 8.6, s_body, group=3)
        for base, ctrl, tip, curl in (((44, 43), (42, 48), (44.5, 51.5), ((47, 54), (48.5, 51))),
                                      ((50, 44), (51.5, 49), (54.5, 51), ((57.5, 52), (57, 48.5))),
                                      ((54.5, 41), (58.5, 43.5), (59.5, 47), ((60.5, 50), (58, 50)))):
            _arm(p, base, ctrl, tip, 4.4, 3.0, s_arm, curl=curl, group=13)
        p.patch(48, 30, [".1111.", "111111", "1111w1", "111111", "1gy111", ".1111."],
                {"1": "ink", "w": "white", "g": "gold0", "y": "gold1"})
        if p.big:
            p.stroke([(31, 41), (33, 47)], "stone1")
            p.stroke([(22, 45), (24, 51)], "stone1")
            _spark(p, 6, 53, 2)
        return

    if view == "down":
        # follower floating toward the camera: the round head with both eyes,
        # the arms curled under, the guard rising behind like a dart
        b = phase
        p.blob(22, 30 + b, 3.4, 2.4, s_body, ang=-30, group=11)
        p.blob(42, 30 + b, 3.4, 2.4, s_body, ang=30, group=12)
        _guard(p, (32, 32 + b), (32, 8 + b), 8.0, s_stone, group=2)
        p.blob(32, 30 + b, 7.4, 6, s_body, group=1)
        p.blob(32, 39 + b, 9, 7.6, s_body, group=3)
        for i, (bx, cx, tx, curl) in enumerate(((25, 22, 23, (25.5, 27)), (29.5, 28.5, 29, (31, 31.5)),
                                                (34.5, 35.5, 35, (33, 32.5)), (39, 42, 41, (38.5, 37)))):
            _arm(p, (bx, 45 + b), (cx, 49 + b), (tx, 52 + b), 3.4, 2.4, s_arm,
                 curl=((tx + (1 if i < 2 else -1) * 0.5, 54.5 + b), (curl[0 if b else 1], 54 + b)), group=13 + i)
        p.patch(26, 36 + b, SEPIDART_EYE, {"1": "ink", "w": "white", "g": "gold0", "y": "gold1"})
        p.patch(33, 36 + b, SEPIDART_EYE, {"1": "ink", "w": "white", "g": "gold0", "y": "gold1"})
        _spark(p, 32, 8 + b, 2, b)
        return

    if view == "up":
        # follower floating away: the mantle and its stone guard from
        # behind, the fins spread, the arm tips under it
        b = phase
        for i, x in enumerate((25, 30, 34, 39)):
            _arm(p, (x, 46 + b), (x + (-1 if i < 2 else 1), 50 + b), (x, 53 + b), 3.4, 2.4, s_arm, group=13 + i)
        p.blob(32, 42 + b, 9, 6.6, s_body, group=3)
        p.blob(21.5, 33 + b, 4.4, 3, s_body, ang=-30, group=11)
        p.blob(42.5, 33 + b, 4.4, 3, s_body, ang=30, group=12)
        p.blob(32, 33 + b, 8, 9, s_body, group=1)
        _guard(p, (32, 40 + b), (32, 9 + b), 9.0, s_stone, group=2)
        _spark(p, 32, 9 + b, 2, b)
        return


# --------------------------------------------------------------------------
# Sepivolt, the thunderbolt squid
# --------------------------------------------------------------------------

SEPIVOLT_COLORS = [
    ("ink", INK),
    # Aegean blue, deepened for the big body, with a pale belly
    ("body0", (16, 32, 88)), ("body1", (32, 72, 152)), ("body2", (64, 120, 200)), ("body3", (120, 176, 232)),
    ("belly", (192, 224, 248)),
    # the stone guard and the darts
    ("stone0", (112, 88, 72)), ("stone1", (160, 136, 104)), ("stone2", (208, 192, 152)), ("white", C.white),
    # sun-gold lightning
    ("gold0", (200, 120, 24)), ("gold1", (248, 192, 56)), ("spark", (248, 248, 184)),
]
SEPIVOLT_SHINY = {
    # a cypress-dark stone guard and a terracotta-red body, like Sepidart's
    "stone0": (16, 40, 32), "stone1": (32, 72, 56), "stone2": (72, 120, 88),
    "body0": (88, 24, 16), "body1": (144, 48, 32), "body2": (192, 88, 56), "body3": (224, 136, 96),
    "belly": (248, 200, 168),
}

v_body = Mat(["body0", "body1", "body2", "body3"], line="body0", cuts=[0.18, 0.42, 0.68])
v_belly = Mat(["body2", "body3", "belly"], line="body1", cuts=[0.4, 0.66])
v_arm = Mat(["body0", "body1", "body2"], line="body0", cuts=[0.36, 0.64])
v_stone = Mat(["stone0", "stone1", "stone2", "white"], line="stone0", cuts=[0.22, 0.48, 0.76])
v_fin = Mat(["body0", "body1", "body2", "body3"], line="body0", cuts=[0.2, 0.44, 0.7])


def _bolt(p, pts, core="spark", edge="gold1", tip="gold0"):
    """A zigzag lightning arc through pts: a bright core with gold edges."""
    if not p.big:
        return
    p.stroke(pts, edge)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        p.px((x0 + x1) / 2, (y0 + y1) / 2, core)
    p.px(pts[-1][0], pts[-1][1], tip)


def sepivolt(p, view, phase):
    import math
    from mon_lib import lens_pts
    if view in ("front", "side", "icon"):
        # the hand-finished battle sprite follows this pose: launching up and
        # back, the spear-guard leading, the dart quiver raked along the back,
        # the arms trailing and the two long tentacles reaching forward
        F = 1 if (phase == 1 and view == "front") else 0
        B = -1.0 if phase == 1 and view in ("front", "side") else 0.0
        ang = math.radians(-33)
        ux, uy = math.cos(ang), math.sin(ang)
        HX, HY = 17.5, 40.5 + B
        DX = HX - 18.0

        def ax(t, o=0.0):
            """t px along the body axis from the head, o px to the belly side."""
            return (HX + ux * t - uy * o, HY + uy * t + ux * o)

        def sh(path):
            return [(x + DX, y) for x, y in path]

        # far fin, spread up off the back like fletching
        p.poly(lens_pts(ax(24, -6), ax(39, -14.5 - F), 7.4, bend=-1.4, fat=0.6), v_fin, bias=0.22, group=11)
        # far arms, trailing beneath in shade
        for c in ((16, 47 + B), (16, 52), (20, 54), (21 + F, 58.5)), ((21, 47 + B), (24, 51), (28.5, 52), (31 + F, 55.5)), \
                 ((24.5, 45 + B), (28.5, 47), (33, 47), (37 + F, 49.5)):
            p.limb(sh(bez3(*c)), 5.0, 1.8, v_arm, bias=0.3, group=10)
        # the mantle: a long torpedo rising to the guard, a pale belly
        p.poly(bez3(ax(3, -9), ax(12, -10.5), ax(25, -8.5), ax(33, -4.5)) + [ax(34, 0)] +
               bez3(ax(33, 4.5), ax(25, 8.5), ax(12, 10.5), ax(3, 9)), v_body, group=1)
        p.poly(bez3(ax(6, 4), ax(14, 9.6), ax(26, 7.6), ax(32, 3.8)) + [ax(32, 6), ax(6, 11)], v_belly, group=2, noline=True)
        # the spare darts along the back, raked toward the guard: a quiver
        ra = math.radians(-38)
        dux, duy = ux * math.cos(ra) - uy * math.sin(ra), ux * math.sin(ra) + uy * math.cos(ra)
        for i, t in enumerate((6.0, 12.0, 18.0, 24.0)):
            r0 = ax(t, -7.6 + 0.5 * i)
            ld = 11.0 - 0.8 * i
            _guard(p, r0, (r0[0] + dux * ld, r0[1] + duy * ld), 3.5, v_stone, bias=0.06 * (3 - i), group=20 + i)
        # the spear-like guard
        _guard(p, ax(29, -1), ax(52, -1.5), 9.6, v_stone, group=3)
        # near fin, spread down from the rear of the mantle
        p.poly(lens_pts(ax(24, 6), ax(39, 14.5 + F), 7.8, bend=1.4, fat=0.6), v_fin, group=12)
        # the head
        p.blob(HX - 1, HY + 1, 9.0, 8.4, v_body, group=4)
        # near arms trailing beneath
        for c in ((12.5, 47.5 + B), (10.5, 52.5), (14, 55.5), (13 - F, 60)), ((17.5, 48.5 + B), (18.5, 53.5), (23.5, 55), (25 - F, 59.5)), \
                 ((22, 47.5 + B), (26, 51), (31, 51), (34 - F, 54)), ((25.5, 44 + B), (30, 44.5), (34.5, 43.5), (39 - F, 45)):
            p.limb(sh(bez3(*c)), 6.0, 2.0, v_arm, group=13)
        # the two long tentacles reaching forward, their clubs crackling
        t1 = sh(bez3((10, 45 + B), (4.5, 45), (3, 38), (6.5, 32 - F)))
        t2 = sh(bez3((12.5, 49 + B), (7, 56), (2.5, 53), (3.4, 47 + F)))
        p.limb(t1, 3.6, 2.8, v_arm, group=14)
        p.blob(t1[-1][0], t1[-1][1] - 1.4, 2.4, 3.0, v_arm, group=14)
        p.limb(t2, 3.6, 2.8, v_arm, group=15)
        p.blob(t2[-1][0], t2[-1][1] + 1.0, 2.4, 3.0, v_arm, group=15)
        if p.big:
            ex, ey = int(HX - 6), int(HY - 5)
            p.patch(ex, ey, ["..11111.", ".1111111", "1yy111w1", "1g111111", "1gy1111.", ".11111.."],
                    {"1": "ink", "w": "white", "g": "gold0", "y": "gold1"})
            d = int(DX)
            _bolt(p, [(6 + d, 30), (8 + d, 34), (5 + d, 37), (7 + d, 41), (4 + d, 45)])
            tip = ax(51, -1.5)
            _bolt(p, [(tip[0] + 1, tip[1] - 1), (tip[0] - 1, tip[1] - 4), (tip[0] + 1, tip[1] - 6), (tip[0] - 1, tip[1] - 8)])
        else:
            p.px(HX - 3, HY - 2, "ink")
        return

    if view == "back":
        # over the shoulder: the dart quiver along the spine, the mantle
        # running back to the spear-guard at lower left, the head turned
        # right with one eye, the arms trailing down the right side
        ux, uy = -0.88, 0.47

        def ax(t, o=0.0):
            return (47 + ux * t - uy * o, 31 + uy * t + ux * o)
        p.poly(bez3(ax(18, 6), ax(20, 16), ax(26, 22), ax(32, 22)) + bez(ax(32, 22), ax(32, 12), ax(30, 5)), v_fin,
               bias=0.18, group=11)
        p.poly(bez3(ax(-2, -11), ax(10, -14), ax(26, -10), ax(36, -5)) +
               bez3(ax(36, 5), ax(26, 12), ax(10, 15), ax(-2, 12)), v_body, group=1)
        p.poly(bez3(ax(18, -6), ax(20, -15), ax(25, -21), ax(31, -20)) + bez(ax(31, -20), ax(32, -12), ax(31, -4)), v_fin,
               group=12)
        _guard(p, ax(32), ax(53), 12.0, v_stone, group=3)
        for i, (t, o) in enumerate(((2, -3.5), (5, 3), (9, -3), (12, 3.5), (16, -2), (19, 3.5))):
            r0 = ax(t, o)
            _guard(p, r0, (r0[0] + ux * 12, r0[1] + uy * 12 - 1.0), 4.0, v_stone, bias=0.05 * (i % 2), group=20 + i)
        p.blob(50, 30, 10.5, 10, v_body, group=4)
        for base, c1, c2, tip, w in (((47, 39), (45, 47), (49, 52), (47, 60), 5.0), ((52, 40), (53, 47), (57, 51), (56, 58), 5.0),
                                     ((57, 37), (61, 42), (60, 48), (61.5, 53), 4.4)):
            p.limb(bez3(base, c1, c2, tip), w, 1.6, v_arm, group=13)
        p.limb(bez3((44, 38), (38, 45), (40, 52), (36, 57)), 2.8, 2.2, v_arm, group=14)
        p.blob(35.5, 58, 2.4, 3.2, v_arm, ang=20, group=14)
        p.patch(51, 24, ["..1111.", ".111111", "1111w11", "11111yy", "111111g", ".11111."],
                {"1": "ink", "w": "white", "g": "gold0", "y": "gold1"})
        if p.big:
            tip = ax(53)
            _bolt(p, [(tip[0] + 1, tip[1] - 2), (tip[0] + 3, tip[1] - 5), (tip[0] + 1, tip[1] - 7)])
            _bolt(p, [(37, 55), (40, 53), (39, 50)])
        return

    if view == "down":
        # follower swimming toward the camera: the face, both eyes, the arms
        # streaming beneath, the mantle and the spear-guard rising behind
        b = phase
        p.poly([(24, 26 + b), (12, 20 + b), (14, 28 + b), (22, 32 + b)], v_fin, group=11)
        p.poly([(40, 26 + b), (52, 20 + b), (50, 28 + b), (42, 32 + b)], v_fin, group=12)
        _guard(p, (32, 22 + b), (32, 3 + b), 8.0, v_stone, group=3)
        for i, x in enumerate((26, 29.5, 34.5, 38)):
            _guard(p, (x, 24 + b), (x + (x - 32) * 0.4, 13 + b), 3.2, v_stone, group=20 + i)
        p.blob(32, 28 + b, 9, 9, v_body, group=1)
        p.blob(32, 40 + b, 10, 8.4, v_body, group=4)
        for i, (bx, tx) in enumerate(((25, 21), (29, 27.5), (35, 36.5), (39, 43))):
            p.limb(bez((bx, 46 + b), (bx + (tx - bx) * 0.3, 52 + b), (tx + (b if i % 2 else -b), 58)), 3.6, 1.4, v_arm,
                   group=13 + i)
        p.patch(25, 36 + b, ["..111", ".1111", "1y1w1", "1g111", ".111."], {"1": "ink", "w": "white", "g": "gold0", "y": "gold1"})
        p.patch(34, 36 + b, ["111..", "1111.", "1w1y1", "111g1", ".111."], {"1": "ink", "w": "white", "g": "gold0", "y": "gold1"})
        if p.big:
            _bolt(p, [(31, 2 + b), (33, 0 + b), (32, -1 + b)])
        return

    if view == "up":
        # follower swimming away: the quiver up its back, the guard, the fins
        b = phase
        for i, x in enumerate((25, 29.5, 34.5, 39)):
            p.limb(bez((x, 48 + b), (x, 53 + b), (x + (1 if i % 2 else -1) * (1 + b), 58)), 3.6, 1.4, v_arm, group=13 + i)
        p.blob(32, 43 + b, 9.5, 7, v_body, group=4)
        p.poly([(25, 30 + b), (12, 24 + b), (14, 33 + b), (24, 37 + b)], v_fin, group=11)
        p.poly([(39, 30 + b), (52, 24 + b), (50, 33 + b), (40, 37 + b)], v_fin, group=12)
        p.blob(32, 32 + b, 9.5, 11, v_body, group=1)
        _guard(p, (32, 26 + b), (32, 3 + b), 9.0, v_stone, group=3)
        for i, (x, y) in enumerate(((28, 40), (36, 40), (27.5, 33), (36.5, 33))):
            _guard(p, (x, y + b), (x + (x - 32) * 0.25, y - 10 + b), 3.4, v_stone, group=20 + i)
        return


MONS = [
    # icon palette 3 keeps the Aegean blue and the tan guard
    Mon("Sepidart", SEPIDART_COLORS, SEPIDART_SHINY, sepidart, icon_pal=3),
    Mon("Sepivolt", SEPIVOLT_COLORS, SEPIVOLT_SHINY, sepivolt, icon_pal=3),
]
