"""Ladon: Melodrakon (#139, Dragon/Fairy), the hundred-voiced serpent coiled
round the tree of golden apples in the garden of the Hesperides.

Concept A, "The Tree That Hisses": the guardian has grown into the tree it
guards. Its tail coils are the roots, gripping the ground; its body spirals
up on itself, tightening into the trunk, and the gold scales turn to bark as
it climbs; its cobra hood spreads into the canopy, the hood's gold ribs are
the boughs, the leaves grow on the ribs like scales, and the golden apples
hang from the rib tips as the hood's own fruit. A few small serpent heads
hiss from the shade under the canopy, the hundred voices. The head is a
gold dragon-serpent's: a wedge skull, a horned brow ridge over a slit-pupiled
Fairy-pink eye, a rounded snout with nostrils and a forked tongue.

The battle sprites are hand finished in tools/dex/sprites/art/; this file is
the draft they started from, and it still draws the icon and the follower.
"""
import math

from mon_lib import C, Mat, Mon, bez, lens_pts

INK = C.ink

COLORS = [
    ("ink", INK),
    # gold scales, umber to sun-gold; g0 doubles as the darkest bark
    ("g0", (96, 48, 24)), ("g1", (168, 104, 32)), ("g2", (224, 160, 48)), ("g3", (248, 216, 104)),
    # terracotta bark, also the belly scutes
    ("bk1", (136, 72, 48)), ("bk2", (192, 120, 72)),
    # evening leaves: cypress shade to olive; g3 is their sunset-lit edge
    ("lf0", (24, 56, 48)), ("lf1", (48, 112, 64)), ("lf2", (112, 168, 72)),
    # the Fairy glow
    ("rose", (208, 72, 120)), ("pink", (248, 160, 200)),
    ("shine", (248, 248, 232)),
    # the golden apples, their own colors so the shiny can turn them blue
    ("apd", (200, 104, 24)), ("ap", (248, 192, 40)),
]
# "The scales turn silver-white and the apples turn pale Aegean blue."
SHINY = {
    "g0": (72, 72, 96), "g1": (136, 144, 160), "g2": (200, 208, 216), "g3": (240, 240, 248),
    "apd": (88, 144, 200), "ap": (160, 208, 240),
}

scale_m = Mat(["g0", "g1", "g2", "g3"], line="g0", cuts=[0.2, 0.44, 0.7])
bark_m = Mat(["g0", "bk1", "bk2"], line="g0", cuts=[0.36, 0.66])
belly_m = Mat(["bk1", "bk2"], line="g0", cuts=[0.5])
leaf_m = Mat(["lf0", "lf1", "lf2", "g3"], line="lf0", cuts=[0.24, 0.5, 0.82])
apple_m = Mat(["apd", "ap", "g3"], line="apd", cuts=[0.4, 0.74])
root_m = Mat(["g0", "bk1"], line="g0", cuts=[0.5])
rib_m = Mat(["g1", "g2"], line="g1", cuts=[0.5])


# --------------------------------------------------------------------------
# Geometry
# --------------------------------------------------------------------------

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


class _Rand:
    """A tiny deterministic generator, so leaf jitter is the same every build."""

    def __init__(self, seed):
        self.s = seed

    def __call__(self, a=0.0, b=1.0):
        self.s = (self.s * 1103515245 + 12345) & 0x7FFFFFFF
        return a + (b - a) * (self.s / 0x7FFFFFFF)


def _leaf(p, a, b, w, bend=0.0, depth=1, **kw):
    """A pointed leaf-scale from a (stalk) to b (tip), split along its midrib
    into a lit half and a shaded half. depth 0 is a front leaf whose lit half
    catches the sunset gold, 2 a dark leaf at the back of the crown."""
    lit, shade = ((2, 1), (2, 1), (1, 0))[depth]
    pts = lens_pts(a, b, p._minw(w), bend, fat=0.42)
    if not p.big:
        return p.poly(pts, leaf_m, flat=lit if depth < 2 else shade, **kw)
    pid = p.poly(pts, leaf_m, flat=shade, **kw)
    n = len(pts) // 2
    left, right = pts[:n], pts[n:][::-1]
    mid = [((u[0] + v[0]) / 2, (u[1] + v[1]) / 2) for u, v in zip(left, right)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    edge = left if dy - dx > 0 else right            # the half facing the upper-left light
    kw.pop("group", None)
    p.poly(edge + mid[::-1], leaf_m, clip=[pid], flat=lit, noline=True, **kw)
    if depth == 0:
        i = int(n * 0.45)
        ex, ey = edge[i]
        mx, my = mid[i]
        p.px((ex + mx) / 2 - 0.5, (ey + my) / 2 - 0.5, "g3")
    return pid


# --------------------------------------------------------------------------
# Hand-placed details: legend for patches
# --------------------------------------------------------------------------

LG = {"#": "ink", "0": "g0", "1": "g1", "2": "g2", "3": "g3", "b": "bk1", "B": "bk2",
      "l": "lf0", "m": "lf1", "n": "lf2", "r": "rose", "p": "pink", "s": "shine",
      "d": "apd", "a": "ap", "_": "_"}

APPLE_BIG = [
    "..0...",
    ".#0##.",
    "#3sa a#".replace(" ", ""),
    "#3aaa#",
    "#aaad#",
    "#aadr#",
    ".####.",
]
APPLE = [
    ".0..",
    "#0##.",
    "#saa#",
    "#aad#",
    "#adr#",
    ".###.",
]


def _apple(p, x, y, big=False):
    """A golden apple hanging from its stem, stem top at (x, y)."""
    if p.big:
        rows = APPLE_BIG if big else APPLE
        p.patch(x - 1, y, rows, LG)
    else:
        p.circle(x + 1, y + 3, 1.8 if big else 1.5, apple_m)


# a small hissing head, the hundred voices, facing left / right
VOICE_L = [
    "..###.",
    ".#21#",
    "#p1#0#",
    "#1100#",
    ".####.",
]


# --------------------------------------------------------------------------
# Melodrakon
# --------------------------------------------------------------------------

HOOD = (33.0, 25.0)        # the hood's heart, behind the head, where its ribs meet
# the hood's leaf lobes, a palmette: (angle in screen degrees, distance of
# the lobe's round end from the heart, its radius); -90 is straight up.
# Listed in drawing order, the far ones first.
LOBES = [(14, 16.5, 6.8), (-178, 12.5, 7.0), (-4, 20.0, 7.8), (-150, 13.5, 8.0), (-30, 18.0, 8.4),
         (-118, 13.2, 8.4), (-58, 15.4, 8.6), (-88, 13.2, 8.4)]
# the ribs between them, out to the rim where the apples hang: (angle, reach)
RIBS = [(-164, 19), (-134, 19.5), (-103, 19.5), (-73, 20), (-44, 22.5), (-17, 25.5), (4, 25.5), (24, 22.5)]
APPLE_RIBS = (-44, -17, 4, 24)


def _polar(c, ang, r, ry=1.0):
    a = math.radians(ang)
    return (c[0] + math.cos(a) * r, c[1] + math.sin(a) * r * ry)


def melodrakon(p, view, phase):
    if view == "icon":
        _icon(p)
        return
    if view in ("front", "side"):
        _front(p, phase if view == "front" else 0)
        return
    if view == "back":
        _back(p)
        return
    if view in ("down", "up"):
        _follow(p, view, phase)
        return


def _rib_path(c, ang, r, F, sy, t0=0.0):
    a = _polar(c, ang, 3, sy)
    m = _polar(c, ang, r * 0.62, sy)
    b = _polar(c, ang, r + F, sy)
    b = (b[0], b[1] + 2.0 * abs(math.cos(math.radians(ang))))   # the side ribs droop at the rim
    pts = bez(a, m, b, 16)
    return pts[int(t0 * 16):]


def _scale_leaf(p, a, b, w, tone, clip, g):
    """One leaf-scale on the hood, flat-toned (tone 0 lit .. 3 deep shade),
    outlined in cypress where it overlaps the scales behind it, with a
    glint along its upper-left edge."""
    level = (2, 2, 1, 0)[tone]
    pid = p.poly(lens_pts(a, b, w, 0.0, fat=0.46), leaf_m, flat=level, clip=clip, group=g)
    if tone <= 1:
        # the sunlit edge: a short run just inside the upper-left side
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        if nx + ny > 0:
            nx, ny = -nx, -ny
        for t in ((0.42, 0.62) if tone == 0 else (0.5,)):
            x, y = a[0] + dx * t + nx * w * 0.24, a[1] + dy * t + ny * w * 0.24
            p.px(x - 0.5, y - 0.5, "g3" if tone == 0 else "lf2")
    return pid


clump_lit = Mat(["lf1", "lf2", "g3"], line="lf0", cuts=[0.24, 0.56])
clump_mid = Mat(["lf0", "lf1", "lf2"], line="lf0", cuts=[0.34, 0.66])
clump_dark = Mat(["lf0", "lf1"], line="lf0", cuts=[0.56])

# the hood's leaf clumps, the leaf-scales of a palmette: (angle from the
# heart in screen degrees, distance, rx, ry); -90 is straight up
CLUMPS = [
    # outer tier, the crown's scalloped rim
    (-176, 17.0, 6.0, 5.2), (-154, 18.0, 6.4, 5.4), (-130, 17.4, 6.6, 5.6), (-106, 16.4, 6.8, 5.6),
    (-82, 16.2, 6.8, 5.6), (-58, 17.4, 6.8, 5.6), (-35, 20.0, 6.6, 5.6), (-12, 22.0, 6.4, 5.4),
    (10, 21.0, 6.0, 5.2), (30, 17.5, 5.4, 4.8),
    # middle tier
    (-165, 10.0, 6.2, 5.2), (-138, 11.5, 6.8, 5.8), (-110, 11.0, 7.0, 6.0), (-84, 11.0, 7.0, 6.0),
    (-58, 12.0, 7.0, 6.0), (-32, 13.5, 7.0, 5.8), (-6, 14.5, 6.6, 5.6), (18, 12.5, 6.0, 5.0),
    # inner tier, round the heart
    (-150, 5.0, 6.0, 5.0), (-100, 5.0, 6.4, 5.4), (-50, 6.0, 6.4, 5.4), (0, 7.5, 6.0, 5.0),
]


def _hood(p, c, F=0, sy=1.0, g0=300, mirror=False, k=1.0, light_c=(38.0, 15.0)):
    """The canopy: the cobra hood spread into a palmette of leaf clumps that
    overlap like great leaf-scales, the upper over the lower, lit by one
    sunset light from the upper left. The gold ribs, the hood's ribs and the
    tree's boughs, radiate through it (drawn by the caller). mirror flips it
    for the back view, where the head is on the right."""
    cx, cy = light_c
    rx0, ry0 = 25.0 * k, 15.0 * k
    placed = []
    for i, (ang, d, rx, ry) in enumerate(CLUMPS):
        a = 180 - ang if mirror else ang
        o = _polar(c, a, (d + F * (d / 20)) * k, sy)
        placed.append((o[1], i, o, rx * k, ry * k, a))
    # lower clumps first, so each clump above lays its shadowed edge over them
    for _, i, o, rx, ry, a in sorted(placed, reverse=True):
        qx, qy = (o[0] - cx) / rx0, (o[1] - cy) / ry0
        light = -0.6 * qx - 0.9 * qy
        _clump(p, o[0], o[1], rx, ry, 0 if light > 0.42 else (1 if light > -0.5 else 2), g0 + i, a)


# a clump's tones by class (sunlit, mid, shade): (rim light, body, shadow), as
# levels of leaf_m (lf0, lf1, lf2, g3)
CLUMP_TONES = [(3, 2, 1), (2, 1, 0), (1, 0, 0)]


def _clump_polys(ox, oy, rx, ry, ang, n_tips=3):
    """A leaf cluster: a round body with n_tips pointed leaf tips fanning out
    on its outward side (ang, screen degrees, pointing away from the heart)."""
    polys = [_ell(ox, oy, rx * 0.86, ry * 0.86)]
    for j in range(n_tips):
        da = (j - (n_tips - 1) / 2) * 38
        a2 = ang + da
        base = _polar((ox, oy), a2, min(rx, ry) * 0.2)
        tip = _polar((ox, oy), a2, max(rx, ry) * 1.12 - abs(da) / 38 * 0.9)
        polys.append(lens_pts(base, tip, min(rx, ry) * 1.05, 0.0, fat=0.35))
    return polys


def _clump(p, ox, oy, rx, ry, cls, g, ang=-90.0):
    """A Torterra-style leaf clump: one tone for the body, a lit crescent on
    its upper left, a shadow crescent on its lower right."""
    rim, body, shadow = CLUMP_TONES[cls]
    polys = _clump_polys(ox, oy, rx, ry, ang)
    m = p.mask(*polys)
    if not p.big:
        return p.add(m, leaf_m, flat=body if cls < 2 else 1, group=g)
    up = p.mask(*[[(x + 1.5, y + 1.8) for x, y in q] for q in polys])
    dn = p.mask(*[[(x - 1.1, y - 1.4) for x, y in q] for q in polys])
    pid = p.add(m, leaf_m, flat=body, group=g)
    p.add(m & ~up, leaf_m, flat=rim, group=g)
    p.add(m & ~dn & up, leaf_m, flat=shadow, group=g)
    return pid


def _ell(cx, cy, rx, ry, n=20):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _split_bark(p, poly_mask, mat_low, g, bias, bark_y):
    """Adds a body part, scales below bark_y and bark above, with a ragged
    edge where the bark creeps down over the scales."""
    import numpy as np
    H, W = poly_mask.shape
    yy, xx = np.mgrid[0:H, 0:W]
    edge = p.oy + p.s * (bark_y + 1.8 * np.sin((xx - p.ox) / p.s * 1.3))
    ids = []
    lo = poly_mask & (yy >= edge)
    hi = poly_mask & (yy < edge)
    if lo.any():
        ids.append(p.add(lo, mat_low, group=g, bias=bias))
    if hi.any():
        ids.append(p.add(hi, bark_m, group=g, bias=bias))
    return ids


def _strand(p, phase0, y0, y1, x0, amp, w0, w1, g, bark_y, turns=1.0, front=True):
    """One strand of the braided trunk: a helix about x0 from y0 (bottom) to
    y1 (top). Draws its front (or back) runs."""
    from mon_lib import ribbon, ellipse_pts
    N = 48
    pts = []
    for i in range(N + 1):
        t = i / N
        th = phase0 + 2 * math.pi * turns * t
        pts.append((x0 + amp * math.sin(th), y0 + (y1 - y0) * t, math.cos(th) > 0, w0 + (w1 - w0) * t))
    runs, cur = [], [0]
    for i in range(1, N + 1):
        if pts[i][2] != pts[cur[-1]][2]:
            cur.append(i)
            runs.append(cur)
            cur = [i]
        else:
            cur.append(i)
    runs.append(cur)
    k = 0
    for idx in runs:
        is_front = pts[idx[len(idx) // 2]][2]
        if is_front != front:
            continue
        path = [(pts[i][0], pts[i][1]) for i in idx]
        if len(path) < 2:
            continue
        a, b = pts[idx[0]][3], pts[idx[-1]][3]
        m = p.mask(ribbon(path, lambda t: a + (b - a) * t),
                   ellipse_pts(path[0][0], path[0][1], a / 2, a / 2, n=12),
                   ellipse_pts(path[-1][0], path[-1][1], b / 2, b / 2, n=12))
        _split_bark(p, m, scale_m, g + k, 0.0 if front else 0.22, bark_y)
        k += 1


def _spiral_runs(cx, cy, r0, r1, turns, th0, squash, w0, w1, N=160):
    """The coiled tail as a flat spiral on the ground, from its tip (t=0,
    radius r0) in to the trunk's foot (t=1, radius r1); split into runs on
    the far side (back) and the near side (front)."""
    pts = []
    for i in range(N + 1):
        t = i / N
        th = th0 + 2 * math.pi * turns * t
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(th), cy + squash * r * math.sin(th), math.sin(th) >= 0,
                    w0 + (w1 - w0) * min(1.0, t / 0.22)))
    runs, cur = [], [0]
    for i in range(1, N + 1):
        if pts[i][2] != pts[cur[-1]][2]:
            cur.append(i)
            runs.append(cur)
            cur = [i]
        else:
            cur.append(i)
    runs.append(cur)
    return pts, runs


def _coils(p, F=0):
    """The root-coils, the tail lying in a flat spiral round the trunk's foot
    and sweeping out to a tip that roots in the ground, and the braided
    trunk rising out of the spiral's heart."""
    from mon_lib import ribbon, ellipse_pts
    pts, runs = _spiral_runs(34.0, 53.4, 27.5, 9.0, 1.28, math.radians(158), 0.27, 2.8, 7.6)

    def run(idx, g, bias):
        path = [(pts[i][0], pts[i][1]) for i in idx]
        if len(path) < 2:
            return None
        a, b = pts[idx[0]][3], pts[idx[-1]][3]
        m = p.mask(ribbon(path, lambda t: a + (b - a) * t),
                   ellipse_pts(path[0][0], path[0][1], a / 2, a / 2, n=12),
                   ellipse_pts(path[-1][0], path[-1][1], b / 2, b / 2, n=12))
        return p.add(m, scale_m, group=g, bias=bias)

    back = [idx for idx in runs if not pts[idx[len(idx) // 2]][2]]
    front = [idx for idx in runs if pts[idx[len(idx) // 2]][2]]
    for k, idx in enumerate(back):               # the far side, outer turns first
        run(idx, 10 + k, 0.16)
    # the trunk: the body and its own tail braided round each other, the
    # scales giving way to bark as they climb
    for fr in (False, True):
        _strand(p, 0.0, 53, 29, 37.2, 3.6, 8.2, 6.0, 30 if not fr else 34, 44, turns=1.15, front=fr)
        _strand(p, math.pi, 53, 29, 37.2, 3.6, 8.2, 6.0, 32 if not fr else 36, 44, turns=1.15, front=fr)
    for k, idx in enumerate(reversed(front)):    # the near side, inner turns first
        pid = run(idx, 40 + k, 0.0)
        if pid and p.big:
            belly = [(pts[i][0], pts[i][1] + pts[i][3] * 0.3) for i in idx]
            if len(belly) > 3:
                w = pts[idx[len(idx) // 2]][3] * 0.34
                p.limb(belly, w, w, belly_m, clip=[pid], group=40 + k, noline=True, cap=False)
    # the tail tip, splitting into roots that grip the ground
    tx, ty = pts[0][0], pts[0][1]
    for path, w in ((((tx, ty), (tx - 2.4, ty + 2.4)), 2.2), (((tx + 0.6, ty + 0.4), (tx + 1.2, ty + 3.0)), 1.8)):
        p.limb(list(path), w, 1.1, root_m, group=60)


# the head's outline, facing left, relative to the jaw hinge: a wedge skull,
# a brow ridge over the eye, a rounded snout, a short receding lower jaw
HEAD_PTS = [(-20.8, -3.0), (-20.4, -4.6), (-19.0, -6.0), (-16.5, -6.8), (-13.5, -7.6), (-11.5, -9.0),
            (-8.5, -9.8), (-5.0, -9.6), (-1.5, -8.6), (1.0, -6.5), (1.5, -2.0), (-1.0, 1.5),
            (-5.0, 2.6), (-10.0, 2.0), (-15.0, 1.2), (-18.4, 0.4), (-20.0, -1.0)]


def _head(p, hx, hy, g=51):
    """The head, facing left, its jaw hinge at (hx, hy) (hand-finished in the art)."""
    p.poly([(hx + x, hy + y) for x, y in HEAD_PTS], scale_m, group=g)
    # the lower jaw's underside, terracotta like the belly
    p.poly([(hx + x, hy + y) for x, y in [(-18.6, 0.2), (-15, 0.6), (-10, 1.2), (-5, 1.8), (-1.5, 1.0),
                                           (-1.0, 2.0), (-5, 2.8), (-10, 2.4), (-15, 1.6), (-18.6, 0.8)]],
           belly_m, group=g + 1)
    # the horned brow ridge, swept back
    p.taper(bez((hx - 9, hy - 10.5), (hx - 2.5, hy - 13.6), (hx + 4, hy - 16.6)), 3.0, scale_m, group=g + 2)


def _front(p, phase):
    F = 1 if phase else 0          # frame 2: the hood flares, the leaves rustle, the tongue flicks

    _hood(p, HOOD, F)
    _coils(p, F)
    # the hood's gold ribs radiating through the leaves, the boughs that
    # bear the apples at the rim
    _ribs(p, HOOD, F)

    # ---- the head, reared out of the front of the hood ----------------------------
    hx, hy = 26, 20 - F
    _head(p, hx, hy)
    if p.big:
        ex, ey = hx - 11, hy - 7
        p.eye(ex, ey, 4, 3, iris="rose", shine="shine", shine_at=(0, 0))
        p.px(ex + 2, ey + 1, "ink")
        p.px(hx - 18, hy - 5, "ink")
        p.stroke([(hx - 19.5, hy - 2), (hx - 12, hy - 1.6), (hx - 7, hy - 1.2), (hx - 4, hy)], "g0")
        L = 3 + F
        p.stroke([(hx - 20.5, hy - 2), (hx - 20.5 - L, hy - 2)], "rose")
        p.px(hx - 21.5 - L, hy - 3, "rose")
        p.px(hx - 21.5 - L, hy - 1, "rose")
        for ang, r in RIBS:
            if ang in APPLE_RIBS:
                pts = _rib_path(HOOD, ang, r, F, 1.0)
                b = pts[-1]
                _apple(p, b[0] - 1, b[1] + 0.5, big=ang == 4)
    else:
        p.px(hx - 12, hy - 4, "rose")


def _ribs(p, c, F=0, mirror=False, k=1.0, g0=280):
    """The hood's gold ribs radiating through the leaves."""
    for i, (ang, r) in enumerate(RIBS):
        a = 180 - ang if mirror else ang
        pts = _rib_path(c, a, r * k, F, 1.0, 0.3)
        if p.big:
            p.stroke([(x + 0.4, y + 1.0) for x, y in pts], "lf0")      # its shadow on the leaves
            p.stroke(pts[:len(pts) // 2], "g1")
            p.stroke(pts[len(pts) // 2:], "g2")
        else:
            p.limb(pts, 1.2, 1.0, rib_m, group=g0 + i, nooutline=True)


def _back(p):
    """Over the shoulder at about 1.15x: the braided trunk rising out of the
    bottom edge, a turn of the coil crossing its foot, the hood from behind
    filling the top of the frame, and the head turned right in profile in
    front of the hood's right side (the art file hand-finishes it)."""
    k = 1.14
    c = (27.0, 33.0)
    for fr in (False, True):
        _strand(p, 0.0, 70, 36, 27.0, 4.2, 9.8, 7.4, 30 if not fr else 34, 54, turns=0.95, front=fr)
        _strand(p, math.pi, 70, 36, 27.0, 4.2, 9.8, 7.4, 32 if not fr else 36, 54, turns=0.95, front=fr)
    # a turn of the coil passing in front of the trunk's foot, cropped below
    p.limb(_spline([(4, 68), (8, 60.5), (18, 56.8), (32, 56.4), (46, 58.6), (54, 63), (58, 68)], 8), 9.6, 9.6,
           scale_m, group=20)
    _hood(p, c, mirror=True, k=k, light_c=(26.0, 18.0))
    _ribs(p, c, mirror=True, k=k)
    # the head, turned right in profile
    hx, hy = 40, 28
    g = 51
    p.poly([(hx - x, hy + y) for x, y in HEAD_PTS], scale_m, group=g)
    p.poly([(hx - x, hy + y) for x, y in [(-18.6, 0.2), (-15, 0.6), (-10, 1.2), (-5, 1.8), (-1.5, 1.0),
                                           (-1.0, 2.0), (-5, 2.8), (-10, 2.4), (-15, 1.6), (-18.6, 0.8)]],
           belly_m, group=g + 1)
    p.taper(bez((hx + 9, hy - 10.5), (hx + 2.5, hy - 13.6), (hx - 4, hy - 16.6)), 3.0, scale_m, group=g + 2)
    if p.big:
        p.eye(hx + 8, hy - 7, 4, 3, iris="rose", shine="shine", shine_at=(3, 0))


def _icon(p):
    """The party icon: the front simplified for 32 px, the head big and the
    hood a few bold clumps in the lighter leaf tones, so the shared icon
    palette keeps them green."""
    c = (36.0, 26.0)
    for i, (ang, d, rx, ry) in enumerate([(-30, 15, 9, 8), (-150, 13, 8, 7), (-62, 16, 9.5, 8.5), (-118, 15, 9, 8),
                                          (-90, 15, 9.5, 8.5), (5, 15, 8, 7)]):
        o = _polar(c, ang, d)
        m = p.mask(*_clump_polys(o[0], o[1], rx, ry, ang))
        p.add(m, leaf_m, flat=2 if o[1] < 20 else 1, group=300 + i)
    p.circle(55, 34, 3.2, apple_m, group=290)
    p.circle(44, 37, 3.0, apple_m, group=290)
    p.limb(_spline([(38, 34), (39, 44), (37, 52)], 6), 11, 13, bark_m, group=20)
    p.limb(_spline([(14, 56), (26, 51), (46, 51), (56, 55), (46, 59.6), (24, 59.6), (14, 56)], 6), 7, 7, scale_m,
           group=21)
    hx, hy = 30, 24
    p.poly([(hx + x * 1.25, hy + y * 1.25) for x, y in HEAD_PTS], scale_m, group=51)
    p.taper(bez((hx - 11, hy - 12.5), (hx - 3, hy - 16.5), (hx + 5, hy - 20.5)), 4.2, scale_m, group=53)
    p.eye(hx - 14, hy - 8, 4, 4, iris="rose", shine="shine", shine_at=(0, 0))


# the follower's hood, spread symmetric behind the head like a palmette
FOLLOW_CLUMPS = [(-90, 15.0, 7.0, 6.0), (-62, 15.0, 6.6, 5.6), (-118, 15.0, 6.6, 5.6), (-34, 13.6, 6.2, 5.2),
                 (-146, 13.6, 6.2, 5.2), (-8, 11.6, 5.6, 4.8), (-172, 11.6, 5.6, 4.8), (-76, 8.0, 6.6, 5.6),
                 (-104, 8.0, 6.6, 5.6)]


def _follow(p, view, phase):
    """The follower: down walks toward the camera, the head facing it under
    the spread hood like a cobra's; up walks away, the hood seen from
    behind. The steps sway the hood and the trunk, and the coil slithers."""
    S = 1 if phase else -1
    c = (32.0, 30.0 + 0.5 * S)
    # the coil on the ground, slithering
    p.limb(_spline([(18 - S, 55.6), (25, 53.2), (39, 53.2), (46 + S, 55.6)], 6), 6.0, 6.0, scale_m, group=10, bias=0.18)
    p.limb(_spline([(46 + S, 55.6), (40, 58.6), (24, 58.6), (18 - S, 55.6)], 6), 6.6, 6.6, scale_m, group=12)
    # the braided trunk
    for fr in (False, True):
        _strand(p, 0.6 * S, 56, 33, 32.0 + 0.6 * S, 2.4, 6.4, 5.0, 20 if not fr else 24, 47, turns=1.0, front=fr)
        _strand(p, math.pi + 0.6 * S, 56, 33, 32.0 + 0.6 * S, 2.4, 6.4, 5.0, 22 if not fr else 26, 47, turns=1.0,
                front=fr)
    p.limb(_spline([(46 + S, 55.6), (40, 58.6), (24, 58.6), (18 - S, 55.6)], 6), 6.6, 6.6, scale_m, group=28)
    # the hood
    for i, (ang, d, rx, ry) in sorted(enumerate(FOLLOW_CLUMPS), key=lambda t: -_polar(c, t[1][0], t[1][1])[1]):
        o = _polar(c, ang + 2 * S * (1 if ang > -90 else -1), d)
        light = -0.6 * (o[0] - 26) / 16 - 0.9 * (o[1] - 18) / 12
        _clump(p, o[0], o[1], rx, ry, 0 if light > 0.42 else (1 if light > -0.5 else 2), 300 + i, ang)
    for ang in (-160, -125, -90, -55, -20):
        pts = _rib_path(c, ang, 17, 0, 1.0, 0.35)
        if p.big:
            p.stroke(pts, "g2")
        else:
            p.limb(pts, 1.2, 1.0, rib_m, group=280, nooutline=True)
    for x, y in ((16.0, 33.6), (48.0, 33.6)):
        p.circle(x, y, 2.3, apple_m, group=290)
    if view == "up":
        return
    # the head facing the camera: a wedge skull, two pink eyes under the brow
    # ridges, the horns sweeping up and out, a rounded snout
    hx, hy = 32.0, 32.0
    for sx in (-1, 1):
        p.taper(bez((hx + sx * 4, hy - 5), (hx + sx * 7.5, hy - 8.5), (hx + sx * 10.5, hy - 13)), 2.6, scale_m,
                group=50)
    p.blob(hx, hy - 1, 7.4, 6.0, scale_m, group=51)
    p.blob(hx, hy + 4.2, 4.6, 3.4, scale_m, group=51)
    p.blob(hx, hy + 6.6, 3.2, 1.2, belly_m, group=52)
    p.eye(hx - 5.5, hy - 2.5, 3, 3, iris="rose", shine="shine", shine_at=(0, 0))
    p.eye(hx + 2.5, hy - 2.5, 3, 3, iris="rose", shine="shine", shine_at=(0, 0))
    if p.big:
        p.pxs([(hx - 1.5, hy + 4), (hx + 0.5, hy + 4)], "ink")
        p.stroke([(hx - 0.5, hy + 7.5), (hx - 0.5, hy + 9.5)], "rose")


MONS = [
    # icon palette 5 keeps the leaves green and the scales gold
    Mon("Melodrakon", COLORS, SHINY, melodrakon, foot="coil", icon_pal=5),
]
