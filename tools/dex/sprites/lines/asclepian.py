"""Asclepian line: Ophidrop, Panacoil (Poison, Poison/Fairy). The sacred
snakes of the Asclepeion and the serpent on Asclepius's staff. Pharmakon:
one drop of venom is harm or help, depending on the dose."""
import math

from mon_lib import C, Mat, Mon, bez

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


def _along(path, t):
    """Point and unit direction at fraction t along a polyline."""
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:])]
    d = t * sum(lens)
    for (a, b), ln in zip(zip(path, path[1:]), lens):
        if d <= ln and ln:
            k = d / ln
            return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k), ((b[0] - a[0]) / ln, (b[1] - a[1]) / ln)
        d -= ln
    a, b = path[-2], path[-1]
    ln = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
    return b, ((b[0] - a[0]) / ln, (b[1] - a[1]) / ln)


def _offset(path, d, t0=0.0, t1=1.0, n=24):
    """The path from t0 to t1, pushed sideways by d (positive: to the left
    of the direction of travel)."""
    out = []
    for i in range(n + 1):
        (x, y), (ux, uy) = _along(path, t0 + (t1 - t0) * i / n)
        out.append((x + uy * d, y - ux * d))
    return out


def _zigzag(path, d, t0, t1, amp, k, n=None):
    """A zigzag line along a path, offset by d, swinging amp to each side,
    with k teeth."""
    n = n or k * 2
    out = []
    for i in range(n + 1):
        (x, y), (ux, uy) = _along(path, t0 + (t1 - t0) * i / n)
        s = d + (amp if i % 2 else -amp)
        out.append((x + uy * s, y - ux * s))
    return out


# --------------------------------------------------------------------------
# Ophidrop, the temple snakelet
# --------------------------------------------------------------------------

OPHIDROP_COLORS = [
    ("ink", INK),
    # pale olive scales
    ("sc0", (72, 88, 40)), ("sc1", (120, 136, 64)), ("sc2", (168, 176, 96)), ("sc3", (208, 216, 144)),
    # the cypress-dark zigzag down the back
    ("zig0", (24, 56, 40)), ("zig1", (48, 96, 64)),
    # marble-white belly
    ("bel0", (176, 168, 144)), ("bel1", (224, 216, 192)), ("white", C.white),
    # wine-violet venom
    ("ven0", (88, 40, 96)), ("ven1", (144, 80, 160)), ("ven2", (208, 160, 224)),
    # the eye's gold
    ("gold0", (184, 120, 32)), ("gold", (240, 200, 72)),
]
OPHIDROP_SHINY = {
    # sun-gold scales with a terracotta zigzag
    "sc0": (160, 104, 24), "sc1": (208, 152, 40), "sc2": (240, 192, 72), "sc3": (248, 232, 144),
    "zig0": (120, 48, 24), "zig1": (184, 88, 48),
}

o_scale = Mat(["sc0", "sc1", "sc2", "sc3"], line="sc0", cuts=[0.2, 0.46, 0.74])
o_belly = Mat(["bel0", "bel1", "white"], line="bel0", cuts=[0.4, 0.74])
o_herb = Mat(["zig0", "zig1", "sc3"], line="zig0", cuts=[0.4, 0.72])
o_venom = Mat(["ven0", "ven1", "ven2"], line="ven0", cuts=[0.34, 0.66])


def _herb(p, x, y, sw=0, k=1.0):
    """A sprig of temple herb whose stem foot is at (x, y): a thin stalk with
    small paired leaves and a violet bud on top; k scales it."""
    p.limb(bez((x, y), (x + 0.6 * k, y - 5 * k), (x - 0.6 * k + sw, y - 10 * k)), 1.3, 1.0, o_herb)
    for a, b, w in (((x + 0.3 * k, y - 3.0 * k), (x + 4.4 * k, y - 4.8 * k), 2.8 * k),
                    ((x + 0.3 * k, y - 4.4 * k), (x - 3.6 * k, y - 6.6 * k), 2.8 * k),
                    ((x + 0.2 * k + sw * 0.5, y - 7.0 * k), (x + 3.6 * k + sw, y - 9.2 * k), 2.4 * k)):
        p.lens(a, b, w, o_herb, bend=0.4)
    p.circle(x - 0.6 * k + sw, y - 10.6 * k, 1.4 * k, o_venom)


def _band(p, path, d, t0, t1, amp, k, clip, mat, w=1.6):
    """A zigzag band painted onto a body part (clip)."""
    return p.limb(_zigzag(path, d, t0, t1, amp, k), w, w, mat, clip=clip, noline=True, cap=False)


def _arc(cx, cy, rx, ry, a0, a1, n=16):
    """Points on an ellipse from angle a0 to a1 (degrees; 0 is right, 90 is
    down, as on screen)."""
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


o_zig = Mat(["zig0", "zig1"], line="zig0", cuts=[0.5])


def ophidrop(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view != "icon") else 0
        # a loose spiral on the ground: from the neck the body runs right
        # along the front, turns at the right end, comes back along the far
        # side behind the neck and curls round to the tail tip in front
        far = _spline([(46, 49.6), (40, 48.4), (32, 48.4), (25, 50)])
        near = _spline([(31.5, 57), (39, 58.6), (46, 57.4), (49.6, 53.6), (48.4, 50.4), (45, 49.2)])
        tail = _spline([(25.6, 49.8), (21.6, 52.4), (21.6, 56.2), (25, 58.6), (29.2, 59.2)])
        fa = p.limb(far, 6.2, 6.0, o_scale, group=1, bias=0.14)
        _herb(p, 46.2, 51.5, sw=L, k=1.0 if p.big else 0.8)
        ta = p.limb(tail, 6.0, 1.6, o_scale, group=2, bias=0.04)
        fr = p.limb(near, 6.8, 6.4, o_scale, group=3)
        p.limb(_offset(near, -2.6, 0.05, 0.55), 1.4, 1.4, o_belly, clip=[fr], group=3, noline=True)
        neck = _spline([(32.5, 56.4), (29.4, 51.8), (29.0, 47.2), (30.8, 43.6 - L), (29.4, 40 - L)])
        nk = p.limb(neck, 6.8, 6.0, o_scale, group=5)
        p.limb(_offset(neck, 2.1, 0.08, 1.0), 2.4, 2.4, o_belly, clip=[nk], group=5, noline=True)
        if p.big:
            _band(p, far, 1.4, 0.0, 1.0, 0.9, 5, [fa], o_zig)
            _band(p, near, 1.6, 0.42, 1.0, 0.9, 4, [fr], o_zig)
            _band(p, tail, 1.2, 0.0, 0.75, 0.7, 4, [ta], o_zig, w=1.3)
            _band(p, neck, -1.8, 0.0, 0.92, 0.8, 4, [nk], o_zig)
        # the head: a big round young skull tilted kindly, a short snout
        hx, hy = 25.5, 36.4 - L
        p.blob(hx, hy, 8.2, 6.8, o_scale, ang=-14, group=6)
        p.blob(hx - 6.2, hy + 2.8, 4.6, 3.4, o_scale, ang=14, group=6)
        p.blob(hx - 3.6, hy + 5.0, 5.2, 1.6, o_belly, ang=12, group=7)
        if p.big:
            p.eye(hx - 5.5, hy - 4.5, 4, 5, iris="gold", shine="white", shine_at=(1, 1))
            p.px(hx - 11, hy + 1.2, "ink")                       # nostril
            p.stroke([(hx - 10, hy + 3.8), (hx - 3, hy + 4.6)], "sc0")   # mouth
            # the fang and its drop
            p.patch(hx - 7.5, hy + 5.0, ["a..", "1b1", "bcd1", "1cc1", ".11."], None)
        else:
            p.px(hx - 3, hy - 1, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the near loop of the coil across
        # the bottom of the frame, the neck rising from it with the zigzag
        # down its back, the head turned right in profile, the herb tucked
        # in the coil and the tail tip curling up at the right
        far = _spline([(8, 50), (18, 46.4), (32, 46), (46, 47.6), (55, 51)])
        fa = p.limb(far, 7.6, 7.6, o_scale, group=1, bias=0.16)
        tail = _spline([(53, 52), (58.6, 48.4), (59.6, 43), (56.6, 40.4)])
        ta = p.limb(tail, 6.6, 1.8, o_scale, group=2, bias=0.06)
        _herb(p, 12.5, 47, k=1.3)
        neck = _spline([(25, 60), (24.6, 50), (27.4, 41.6), (33, 35.4), (37, 32.6)])
        nk = p.limb(neck, 9.4, 8.2, o_scale, group=4)
        p.limb(_offset(neck, -3.4, 0.4, 1.0), 2.2, 2.2, o_belly, clip=[nk], group=4, noline=True)
        near = _spline([(-2, 58.6), (10, 56.4), (28, 56.8), (46, 58), (60, 61.4), (66, 64)])
        ne = p.limb(near, 10.0, 10.0, o_scale, group=3)
        if p.big:
            _band(p, far, -1.8, 0.05, 0.95, 1.0, 8, [fa], o_zig, w=1.8)
            _band(p, near, -2.4, 0.08, 0.9, 1.2, 9, [ne], o_zig, w=2.0)
            _band(p, neck, 0.6, 0.0, 0.8, 1.3, 5, [nk], o_zig, w=2.0)
        hx, hy = 41, 26.6
        p.blob(hx, hy, 9.4, 7.8, o_scale, ang=14, group=6)
        p.blob(hx + 7.4, hy + 3.2, 5.4, 3.8, o_scale, ang=-14, group=6)
        p.blob(hx + 4.2, hy + 5.8, 6.0, 1.8, o_belly, ang=-12, group=7)
        p.eye(hx + 2, hy - 4, 4, 5, iris="gold", shine="white", shine_at=(2, 1))
        p.px(hx + 12.4, hy + 1.6, "ink")
        p.stroke([(hx + 5, hy + 4.6), (hx + 11.6, hy + 4.2)], "sc0")
        p.patch(hx + 8, hy + 6, ["a..", "1b1", "1dcb1", "1cc1", ".11."], None)
        return

    if view in ("down", "up"):
        # follower: the snakelet facing the player (down) or seen from
        # behind (up), its head raised over a coil; the steps sway the neck
        S = 1 if phase else -1
        ring = _arc(32, 54, 13, 5, 180, 360)
        rf = _arc(32, 54, 13, 5, 0, 180)
        r1 = p.limb(ring, 7.4, 7.4, o_scale, group=1, bias=0.12)
        r2 = p.limb(rf, 8.0, 8.0, o_scale, group=2)
        _herb(p, 43, 51, sw=S * 0.5)
        neck = _spline([(32 + 3 * S, 57), (32 + 3 * S, 49), (32 - S, 42), (32, 36)])
        nk = p.limb(neck, 8.4, 7.4, o_scale, group=3)
        if view == "down":
            p.limb(_spline([(32 + 3 * S, 57), (32 + 3 * S, 49), (32 - S, 42), (32, 37)]), 3.6, 3.2, o_belly,
                   clip=[nk], group=3, noline=True)
            if p.big:
                _band(p, rf, -2.4, 0.08, 0.92, 1.1, 7, [r2], o_zig, w=1.8)
        else:
            if p.big:
                _band(p, neck, 0.0, 0.0, 0.95, 1.2, 4, [nk], o_zig, w=2.0)
                _band(p, ring, 2.0, 0.1, 0.9, 1.0, 6, [r1], o_zig, w=1.8)
                _band(p, rf, -2.4, 0.08, 0.92, 1.1, 7, [r2], o_zig, w=1.8)
        hy = 30
        p.blob(32, hy, 8.4, 7.0, o_scale, group=4)
        if view == "down":
            p.blob(32, hy + 4.6, 5.6, 3.6, o_scale, group=4)
            p.blob(32, hy + 6.6, 4.4, 1.4, o_belly, group=5)
            p.eye(25, hy - 3, 4, 5, iris="gold", shine="white", shine_at=(1, 1))
            p.eye(35, hy - 3, 4, 5, iris="gold", shine="white", shine_at=(2, 1))
            if p.big:
                p.pxs([(30, hy + 4), (33, hy + 4)], "ink")
                p.patch(30, hy + 7, ["a", "1", "c", "b"], None)
        elif p.big:
            _band(p, [(32, hy - 6), (32, hy + 6)], 0.0, 0.0, 1.0, 1.2, 3, None, o_zig, w=2.0)
        return


# --------------------------------------------------------------------------
# Panacoil, the serpent of the staff
# --------------------------------------------------------------------------

PANACOIL_COLORS = [
    ("ink", INK),
    # pale olive scales
    ("sc0", (64, 80, 40)), ("sc1", (112, 128, 64)), ("sc2", (160, 176, 96)), ("sc3", (208, 216, 144)),
    # the marble-white hood and flanks
    ("mb0", (168, 160, 144)), ("mb1", (216, 208, 192)), ("white", C.white),
    # the limestone staff, warm enough to double as the gold of the eye
    ("st0", (128, 88, 48)), ("st1", (200, 152, 72)), ("st2", (240, 208, 128)),
    # wine-violet belly bands
    ("wn0", (96, 40, 96)), ("wn1", (152, 88, 160)),
    # the Fairy-pink halo
    ("pk0", (224, 112, 160)), ("pk1", (248, 192, 216)),
]
PANACOIL_SHINY = {
    # sun-gold scales on a marble staff, like a gilded temple offering
    "sc0": (152, 96, 24), "sc1": (200, 144, 40), "sc2": (240, 192, 72), "sc3": (248, 232, 144),
    "st0": (136, 128, 128), "st1": (192, 184, 176), "st2": (232, 224, 216),
}

pc_scale = Mat(["sc0", "sc1", "sc2", "sc3"], line="sc0", cuts=[0.2, 0.46, 0.74])
pc_hood = Mat(["mb0", "mb1", "white"], line="mb0", cuts=[0.36, 0.7])
pc_staff = Mat(["st0", "st1", "st2"], line="st0", cuts=[0.34, 0.68])
pc_belly = Mat(["wn0", "wn1"], line="wn0", cuts=[0.55])
pc_halo = Mat(["pk0", "pk1", "white"], line="pk0", outline="pk0", cuts=[0.4, 0.8])


def _runs(h):
    """Splits a helix into runs that are in front of the staff and behind."""
    runs, cur = [], [h[0]]
    for q in h[1:]:
        if q[2] != cur[-1][2]:
            cur.append(q)
            runs.append(cur)
            cur = [q]
        else:
            cur.append(q)
    runs.append(cur)
    return [([(x, y) for x, y, _ in r], r[len(r) // 2][2]) for r in runs]


def _staff(p, x0, y0, x1, y1, w, knots=(), **kw):
    """The knotted staff from its head (x0, y0) to its foot (x1, y1)."""
    pid = p.limb([(x0, y0), (x1, y1)], w, w * 1.1, pc_staff, **kw)
    for t, side, r in knots:
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        p.blob(x + side * w * 0.42, y, r, r * 0.9, pc_staff, group=kw.get("group"))
    return pid


def _ring(p, cx, cy, r_out, r_in, mat, **kw):
    outer = p.mask(_circle(cx, cy, r_out))
    inner = p.mask(_circle(cx, cy, r_in))
    return p.add(outer & ~inner, mat, **kw)


def _circle(cx, cy, r, n=48):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _coils(p, h, wfn, mat, belly, group0, bias=0.16, sides=("back", "front"), under=None):
    """Draws a helix: runs behind the staff ('back') or in front ('front').
    In front, the pale underside shows along the lower edge (under), barred
    with the wine-violet belly bands (belly)."""
    runs = _runs(h)
    total = sum(len(r) - 1 for r, _ in runs) or 1
    pos = 0
    ids = []
    for k, (pts, front) in enumerate(runs):
        t0, t1 = pos / total, (pos + len(pts) - 1) / total
        pos += len(pts) - 1
        side = "front" if front else "back"
        if side not in sides:
            continue
        w0, w1 = wfn(t0), wfn(t1)
        pid = p.limb(pts, w0, w1, mat, group=group0 + k, bias=0 if front else bias)
        if front and under is not None:
            p.limb(_offset(pts, -(w0 + w1) / 2 * 0.32, 0.0, 1.0), (w0 + w1) / 2 * 0.42, (w0 + w1) / 2 * 0.42, under,
                   clip=[pid], group=group0 + k, noline=True)
        if front and belly is not None and p.big:
            n = max(2, int(len(pts) / 3))
            for i in range(1, n):
                (x, y), (ux, uy) = _along(pts, i / n)
                w = wfn(t0 + (t1 - t0) * i / n)
                a_ = (x - uy * w * 0.1, y + ux * w * 0.1)
                b_ = (x - uy * w * 0.5, y + ux * w * 0.5)
                p.stroke([a_, b_], "wn1")
        ids.append(pid)
    return ids


# Panacoil's body, tail to neck: the knots of the diagonal runs and their
# round turns (the same path the hand-finished battle front was drawn on)
PC_KNOTS = [
    (40.4, 62.0), (34.4, 61.4), (26.0, 59.8), (19.6, 57.6), (16.6, 55.0),   # tail wrap F1, turn L1
    (20.4, 52.6), (34.0, 50.6), (46.6, 48.6), (51.6, 46.2),                 # B1 behind, turn R1
    (48.0, 43.4), (34.0, 41.6), (21.0, 39.4), (16.6, 37.0),                 # F2 in front, turn L2
    (20.6, 34.2), (33.4, 32.2), (45.6, 30.2), (50.4, 27.6),                 # B2 behind, turn R2
    (49.4, 23.6),                                                           # into the neck, behind the veil
]
PC_APEX = (4, 8, 12, 16)    # the turns: runs between them alternate front, back
PC_FRONT = {0, 2}


def _helix_fn(cx, cy, rx, ry, a0, a1, n=160):
    """A coil whose center (cx(t), cy(t)) and radius rx(t) vary along it;
    angles in degrees, 90 nearest the viewer. Returns [(x, y, front)]."""
    out = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(a0 + (a1 - a0) * t)
        out.append((cx(t) + rx(t) * math.cos(a), cy(t) + ry * math.sin(a), math.sin(a) > 0))
    return out


def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def panacoil(p, view, phase):
    if view in ("front", "side", "icon"):
        # the battle front is hand-finished in the art files; this draft
        # follows it for the icon and the follower. The body is a chain of
        # diagonal runs with round turns (PC_KNOTS): front runs rise to the
        # left in front of the staff, back runs rise to the right behind it.
        L = 1 if (phase == 1 and view != "icon") else 0
        K = [(x, y - (L if y < 36 else 0)) for x, y in PC_KNOTS]
        # the party icon squats the coils so the head, veil and halo stay big
        sq = (lambda y: 26 + (y - 26) * 0.62 if y > 26 else y) if view == "icon" else (lambda y: y)
        K = [(x, sq(y)) for x, y in K]
        path = _spline(K, 12)
        lens = [0.0]
        for a_, b_ in zip(path, path[1:]):
            lens.append(lens[-1] + math.hypot(b_[0] - a_[0], b_[1] - a_[1]))
        tot = lens[-1]
        W = lambda t: 2.4 + 6.6 * _smooth(t / 0.28) + 1.4 * t
        apex = [min(range(len(path)), key=lambda i: (path[i][0] - K[j][0]) ** 2 + (path[i][1] - K[j][1]) ** 2)
                for j in PC_APEX]
        cuts = [0] + apex + [len(path) - 1]
        segs = [(path[cuts[k]:cuts[k + 1] + 1], lens[cuts[k]] / tot, lens[cuts[k + 1]] / tot, k in PC_FRONT)
                for k in range(len(cuts) - 1)]
        for k, (sp, t0, t1, front) in enumerate(segs):
            if not front:
                p.limb(sp, W(t0), W(t1), pc_scale, group=10 + k, bias=0.16)
        p.limb(_spline([(49.0, 24.0 - L), (47.4, 16.6 - L), (42.4, 12.0 - L), (36.0, 10.4 - L)]), 10.0, 9.0, pc_scale,
               group=40, bias=0.1)
        _staff(p, 33.6, 22.0, 35.6, sq(62.2), 5.4, knots=((0.6, -1, 1.8), (0.85, 1, 1.7)), group=5)
        p.circle(33.8, 22.6 - L, 3.4, pc_staff, group=5)
        for k, (sp, t0, t1, front) in enumerate(segs):
            if front:
                pid = p.limb(sp, W(t0), W(t1), pc_scale, group=10 + k)
                w = (W(t0) + W(t1)) / 2
                if view != "icon":
                    p.limb([(x, y + w * 0.3) for x, y in sp], w * 0.46, w * 0.46, pc_hood, clip=[pid], group=10 + k,
                           noline=True)
        # the veil: draped from the crown, falling behind the neck to a hem
        veil = [(25.0, 4.0), (28.0, 2.4), (33.0, 1.8), (38.4, 3.2), (42.6, 6.2), (45.6, 10.4), (48.0, 15.6),
                (50.2, 21.0), (52.2, 26.4), (53.4, 31.2), (49.2, 31.8), (44.2, 32.2), (39.6, 32.6), (38.0, 29.6),
                (37.0, 24.6), (36.0, 19.6), (34.4, 15.4), (32.2, 11.6), (30.0, 8.0), (27.6, 5.4)]
        p.poly([(x, sq(y) - L) for x, y in veil], pc_hood, group=41)
        # the halo, a full ring framing the head
        _ring(p, 27.6, 17.4 - L, 16.7, 14.4, pc_halo, group=45, noline=True)
        # the head: round and sweet, resting on the staff's head
        hx, hy = 25.0, 13.4 - L
        p.blob(hx, hy, 11.0, 8.2, pc_scale, ang=10, group=46)
        p.blob(hx - 7.0, hy + 3.8, 5.6, 4.0, pc_scale, ang=14, group=46)
        p.blob(hx - 4.0, hy + 6.6, 7.0, 1.8, pc_hood, ang=10, group=47)
        if p.big:
            p.eye(hx - 4, hy - 4, 6, 7, iris="st2", shine="white", shine_at=(1, 1))
        else:
            p.px(hx - 2, hy - 1, "ink")
            p.px(hx - 2, hy, "st1")
        return

    if view == "back":
        # over the shoulder at about 1.15x: the staff from behind with the
        # coils round it and the tail wrapped low on it, the veil seen from
        # behind, the head turned right in profile over the staff's head
        sx0, sy0, sx1, sy1 = 30.0, 24.0, 31.4, 70.0
        hx, hy = 41.6, 15.6
        _ring(p, 34.0, 18.4, 15.6, 12.8, pc_halo, group=90, noline=True)
        cx = lambda t: 31.4 - 1.2 * t
        cy = lambda t: 70 - 38 * t
        rx = lambda t: 6.0 + 9.0 * _smooth(t / 0.14) - 4.4 * max(0.0, (t - 0.14) / 0.86)
        w = lambda t: 2.2 + 5.0 * _smooth(t / 0.3) + 1.6 * t
        a1 = 210 + 360 * 3
        h = _helix_fn(cx, cy, rx, 1.6, a1 - 360 * 3.1, a1)
        _coils(p, h, w, pc_scale, None, 10, sides=("back",))
        _staff(p, sx0, sy0, sx1, sy1, 5.0, knots=((0.3, 1, 1.8), (0.58, -1, 1.7)), group=5)
        p.circle(sx0, sy0 - 1, 3.8, pc_staff, group=5)
        _coils(p, h, w, pc_scale, None, 10, sides=("front",))
        neck = _spline([(23.2, 32.4), (21.8, 25), (27, 17.6), (35, 14.6)])
        p.limb(neck, 8.8, 8.0, pc_scale, group=40)
        veil = _spline([(hx - 0.6, hy - 8), (hx - 7, hy - 9.8), (hx - 12.6, hy - 5.6), (hx - 16, hy + 3),
                        (hx - 19.6, hy + 13), (hx - 20, hy + 20.4), (hx - 15.6, hy + 18.8), (hx - 12, hy + 21.8),
                        (hx - 8.6, hy + 17.6), (hx - 6, hy + 10.8), (hx - 1.0, hy + 4.4), (hx + 2.4, hy - 2.4)])
        p.poly(veil, pc_hood, group=41, bias=0.06)
        p.blob(hx - 0.8, hy, 8.2, 6.0, pc_scale, ang=-22, group=42)
        p.blob(hx + 6.0, hy + 4.0, 5.2, 3.2, pc_scale, ang=-28, group=42)
        p.blob(hx + 3.6, hy + 6.0, 5.6, 1.6, pc_belly, ang=-26, group=43)
        if p.big:
            p.eye(hx + 1, hy - 3, 5, 4, iris="wn1", shine="white", shine_at=(2, 1))
            p.stroke([(hx, hy - 3.2), (hx + 6, hy - 3.2)], "ink")
            p.px(hx + 11, hy + 5.6, "ink")
        return

    if view in ("down", "up"):
        # follower: gliding along carrying its staff in its coils, the head
        # on top facing the player (down) or seen from behind (up)
        S = 1 if phase else -1
        _ring(p, 32, 15, 12.6, 10.4, pc_halo, group=90, noline=True)
        cx = lambda t: 32 + 0.6 * S * math.sin(t * 6)
        cy = lambda t: 58.6 - 30 * t
        rx = lambda t: 5.0 + 7.4 * _smooth(t / 0.18) - 2.6 * max(0.0, (t - 0.18) / 0.82)
        w = lambda t: 2.0 + 4.6 * _smooth(t / 0.3) + 1.2 * t
        a1 = 330 + 360 * 3
        h = _helix_fn(cx, cy, rx, 2.2, a1 - 360 * 2.8, a1)
        _coils(p, h, w, pc_scale, None, 10, sides=("back",))
        _staff(p, 32, 21, 32, 61, 4.2, group=5)
        p.circle(32, 20, 3.4, pc_staff, group=5)
        _coils(p, h, w, pc_scale, pc_belly if view == "down" else None, 10, sides=("front",))
        if view == "down":
            veil = [(26, 6), (32, 3.6), (38, 6), (43, 14), (45, 24), (40.6, 26.4), (37, 20), (32, 22),
                    (27, 20), (23.4, 26.4), (19, 24), (21, 14)]
            p.poly(_spline(veil + [veil[0]]), pc_hood, group=41)
            p.blob(32, 13, 6.6, 6.0, pc_scale, group=42)
            p.blob(32, 18, 4.4, 3.2, pc_scale, group=42)
            p.blob(32, 20.2, 3.4, 1.2, pc_belly, group=43)
            p.eye(26.6, 11, 3, 4, iris="wn1", shine="white", shine_at=(1, 1))
            p.eye(34.4, 11, 3, 4, iris="wn1", shine="white", shine_at=(1, 1))
            if p.big:
                p.pxs([(30, 18), (33, 18)], "ink")
        else:
            # from behind: the back of the head over the veil, its wine band
            # and scalloped hem falling down the neck
            p.limb([(32, 24), (32, 15)], 7.4, 7.0, pc_scale, group=40)
            p.blob(32, 9.6, 6.4, 5.4, pc_scale, group=42)
            veil = [(25.4, 9), (32, 7.4), (38.6, 9), (43, 16), (45, 26), (41.4, 28.6), (38, 27), (35, 29.4), (32, 27.6),
                    (29, 29.4), (26, 27), (22.6, 28.6), (19, 26), (21, 16)]
            vid = p.poly(_spline(veil + [veil[0]], 4), pc_hood, group=41)
            p.poly([(22, 13.6), (32, 11.4), (42, 13.6), (42.4, 15.6), (32, 13.4), (21.6, 15.6)], pc_belly, clip=[vid],
                   group=41, noline=True)
        return


MONS = [
    Mon("Ophidrop", OPHIDROP_COLORS, OPHIDROP_SHINY, ophidrop, foot="coil"),
    Mon("Panacoil", PANACOIL_COLORS, PANACOIL_SHINY, panacoil, foot="coil"),
]
