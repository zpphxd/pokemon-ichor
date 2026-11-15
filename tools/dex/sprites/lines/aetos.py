"""Aetos line: Aetling, Aetarch (Flying, then Electric/Flying). Zeus's eagle,
king of the birds and bearer of his thunderbolts. Periphas, a king so just
that Zeus made him an eagle (Antoninus Liberalis 6); the eagle that carried
Ganymede and tore at Prometheus (Hesiod, Theogony 521-525).

Aetling is a scowling eaglet in marble-white down, mantling on a limestone
crag. Aetarch is the heraldic eagle of the Elis coins: wings raised high and
spread, talons thrust forward around a double-ended keraunos.

The battle sprites are hand finished in tools/dex/sprites/art/; this file is
the draft they started from, and it still draws the icons and followers.
"""
import math

from mon_lib import C, Mat, Mon, bez, lerp, lens_pts

INK = C.ink


# --------------------------------------------------------------------------
# Shared geometry
# --------------------------------------------------------------------------

def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    return dx / d, dy / d


def _rot(pt, c, deg):
    ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    x, y = pt[0] - c[0], pt[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def fluff_pts(cx, cy, rx, ry, tufts=(), ang=0.0, n=64):
    """An ellipse whose rim sprouts tufts of down: tufts is a list of
    (angle in degrees, 0 = right and 90 = down; length in px; half-width in
    degrees). Each tuft is a sharp spike, so the rim reads as fluff."""
    pts = []
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    for i in range(n):
        t = 360.0 * i / n
        r = 1.0
        x, y = rx * math.cos(math.radians(t)), ry * math.sin(math.radians(t))
        ext = 0.0
        for ta, ln, hw in tufts:
            d = abs((t - ta + 180) % 360 - 180)
            if d < hw:
                ext = max(ext, ln * (1 - d / hw) ** 1.6)
        rr = math.hypot(x, y) or 1
        x, y = x * (rr + ext) / rr * r, y * (rr + ext) / rr * r
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def taper_feather(a, b, w, bend=0.0, fat=0.35, n=12):
    """A flight feather: widest a third of the way out, tapering to a point
    at b (an eagle's emarginated primary, a finger)."""
    return lens_pts(a, b, w, bend, n=n, fat=fat)


def round_feather(a, b, w, bend=0.0, n=10, root=0.5):
    """A feather with a rounded tip: narrow at the root a, full width toward
    the tip b, bowed sideways by bend (secondaries, coverts, tail)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / d, dx / d
    ux, uy = dx / d, dy / d
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        off = bend * math.sin(math.pi * t)
        cx, cy = a[0] + dx * t + nx * off, a[1] + dy * t + ny * off
        h = w / 2 * (root + (1 - root) * min(1.0, t / 0.55))
        left.append((cx + nx * h, cy + ny * h))
        right.append((cx - nx * h, cy - ny * h))
    cap = []
    for i in range(1, 8):
        a_ = math.pi * i / 8
        c, s = math.cos(a_), math.sin(a_)
        cap.append((b[0] + nx * (w / 2) * c + ux * (w / 2) * s, b[1] + ny * (w / 2) * c + uy * (w / 2) * s))
    return left + cap + right[::-1]


def _lit_left(a, b):
    """True when the +normal side of a->b faces the upper-left light."""
    return (b[1] - a[1]) - (b[0] - a[0]) > 0


def flat_feather(p, pts, a, b, mat, lit, shade, **kw):
    """A Gen 3 feather: flat-toned, the half facing the light at ramp level
    `lit` and the other at `shade`, split along the rachis a->b."""
    if not p.big:
        return p.poly(pts, mat, flat=lit, **kw)
    pid = p.poly(pts, mat, flat=shade, **kw)
    n = len(pts) // 2
    left, right = pts[:n], pts[len(pts) - n:][::-1]
    mid = [((u[0] + v[0]) / 2, (u[1] + v[1]) / 2) for u, v in zip(left, right)]
    edge = left if _lit_left(a, b) else right
    kw.pop("group", None)
    kw.pop("bias", None)
    p.poly(edge + mid[::-1], mat, clip=[pid], flat=lit, noline=True, **kw)
    return pid


def _qb(p0, p1, p2, t):
    a, b, c = (1 - t) ** 2, 2 * (1 - t) * t, t * t
    return (a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1])


class Wing:
    """A real wing: a curved leading edge from the shoulder S, bowed through
    C, to the wrist Wr, and the hand on to Hd. Primaries fan out of the hand
    to separate points; secondaries hang from the forearm; the greater
    coverts and the marginal band (the arm) lie over their roots. Four value
    masses, light at the leading edge and dark at the trailing edge."""

    def __init__(self, S, C, Wr, Hd, prim, sec, pw, sw, cov=5.0, ncov=5, arm=(4.4, 2.4), pfat=0.35,
                 sec_round=True, flat=None):
        self.flat = flat  # ((lit, shade) for primaries, (lit, shade) for secondaries)
        self.S, self.C, self.Wr, self.Hd = S, C, Wr, Hd
        self.prim, self.sec = prim, sec
        self.pw, self.sw = pw, sw
        self.cov, self.ncov = cov, ncov
        self.arm_w = arm
        self.pfat = pfat
        self.sec_round = sec_round

    def arm(self, t):
        """t 0 at the shoulder, 1 at the wrist, up to 1.6 out along the hand."""
        if t <= 1:
            return _qb(self.S, self.C, self.Wr, t)
        return lerp(self.Wr, self.Hd, (t - 1) / 0.6)

    def trail(self, t):
        """Unit vector from the arm toward the trailing edge at t."""
        p0, p1 = self.arm(max(0, t - 0.03)), self.arm(min(1.6, t + 0.03))
        tx, ty = p1[0] - p0[0], p1[1] - p0[1]
        d = math.hypot(tx, ty) or 1
        nx, ny = -ty / d, tx / d
        cx = sum(q[0] for q in self.sec) / len(self.sec)
        cy = sum(q[1] for q in self.sec) / len(self.sec)
        q = self.arm(t)
        if (cx - q[0]) * nx + (cy - q[1]) * ny < 0:
            nx, ny = -nx, -ny
        return nx, ny

    def moved(self, dx=0.0, dy=0.0, rot=0.0, about=None):
        """A copy moved and rotated about the shoulder (a wingbeat)."""
        c = about or self.S

        def T(q):
            q = _rot(q, c, rot)
            return (q[0] + dx, q[1] + dy)
        w = Wing(T(self.S), T(self.C), T(self.Wr), T(self.Hd), [T(q) for q in self.prim],
                 [T(q) for q in self.sec], self.pw, self.sw, self.cov, self.ncov, self.arm_w, self.pfat,
                 self.sec_round, self.flat)
        return w

    def draw(self, p, mats, g0, bias=0.0, small=None):
        """mats: (primaries, secondaries, coverts, arm). Returns the next
        free group."""
        mp, ms, mc, ma = mats
        g = g0
        n = len(self.prim)
        big = p.big if small is None else not small
        # primaries, outermost first so each inner one overlaps the next
        for i, tip in enumerate(self.prim):
            if not big and i % 2:
                continue
            base = lerp(self.Hd, self.Wr, 0.85 * i / max(n - 1, 1))
            w = self.pw[i] if isinstance(self.pw, (list, tuple)) else self.pw
            if not big:
                w *= 1.5
            pts = taper_feather(base, tip, w, fat=self.pfat)
            if self.flat:
                flat_feather(p, pts, base, tip, mp, self.flat[0][0], self.flat[0][1], group=g, bias=bias)
            else:
                p.poly(pts, mp, group=g, bias=bias)
            g += 1
        # secondaries: one mass with a scalloped trailing edge
        m = len(self.sec)
        polys = []
        for i, tip in enumerate(self.sec):
            t = 0.95 - 0.8 * i / max(m - 1, 1)
            base = self.arm(t)
            if self.sec_round:
                polys.append(round_feather(base, tip, self.sw, root=0.7))
            else:
                polys.append(taper_feather(base, tip, self.sw, fat=0.5))
        if self.flat and big:
            for i, (pts, tip) in enumerate(zip(polys, self.sec)):
                t = 0.95 - 0.8 * i / max(m - 1, 1)
                flat_feather(p, pts, self.arm(t), tip, ms, self.flat[1][0], self.flat[1][1], group=g, bias=bias)
                g += 1
        else:
            p.polys(polys, ms, group=g, bias=bias)
            g += 1
        # greater coverts: rounded tongues along the arm, one mass
        polys = []
        for j in range(self.ncov):
            t = 0.1 + 1.15 * (j + 0.5) / self.ncov
            q = self.arm(t)
            tx, ty = self.trail(t)
            a = (q[0] + tx * 0.8, q[1] + ty * 0.8)
            L = self.cov * (0.8 + 0.2 * (1 - abs(t - 0.8) / 0.8))
            b = (a[0] + tx * L, a[1] + ty * L)
            polys.append(round_feather(a, b, 4.2 if big else 5.0, root=0.75))
        p.polys(polys, mc, group=g, bias=bias)
        g += 1
        # the arm: the marginal coverts along the leading edge
        path = [self.arm(k / 20 * 1.6) for k in range(21)]
        p.limb(path, self.arm_w[0], self.arm_w[1], ma, group=g, bias=bias - 0.05)
        return g + 1


# --------------------------------------------------------------------------
# Aetling, the scowling eaglet
# --------------------------------------------------------------------------

AETLING_COLORS = [
    ("ink", INK),
    # marble-white down with warm marble shadows
    ("down0", (120, 112, 112)), ("down1", (168, 160, 152)), ("down2", (216, 208, 192)), ("down3", C.white),
    # limestone-tan flight feathers, and the limestone crag
    ("tan0", (96, 64, 40)), ("tan1", (152, 112, 72)), ("tan2", (200, 168, 120)), ("tan3", (232, 216, 176)),
    # sun-gold beak and feet
    ("gold0", (168, 96, 24)), ("gold1", (224, 160, 48)), ("gold2", (248, 216, 104)),
    # the crest: the two stray crown feathers
    ("crest0", (208, 136, 32)), ("crest1", (248, 200, 72)),
]
# "Cypress-dark down with an Aegean-blue crest."
AETLING_SHINY = {
    "down0": (16, 40, 32), "down1": (32, 64, 48), "down2": (56, 96, 72), "down3": (96, 136, 104),
    "crest0": (48, 104, 176), "crest1": (112, 168, 224),
}

a_down = Mat(["down0", "down1", "down2", "down3"], line="down0", cuts=[0.36, 0.66, 0.88])
a_brow = Mat(["down0", "down1", "down2"], line="down0", cuts=[0.4, 0.75])
a_tan = Mat(["tan0", "tan1", "tan2", "tan3"], line="tan0", cuts=[0.2, 0.46, 0.74])
a_prim = Mat(["tan0", "tan1", "tan2"], line="tan0", cuts=[0.36, 0.7])
a_cov = Mat(["tan1", "tan2", "tan3"], line="tan0", cuts=[0.36, 0.7])
a_gold = Mat(["gold0", "gold1", "gold2"], line="gold0", cuts=[0.42, 0.72])
a_crest = Mat(["crest0", "crest1"], line="crest0", cuts=[0.5])
a_rock = Mat(["tan0", "tan1", "tan2"], line="tan0", cuts=[0.34, 0.68])
A_WING = (a_prim, a_tan, a_cov, a_down)


def _crag(p, x0=21, x1=46, top=54.5, bottom=61.5):
    pts = [(x0, bottom), (x0 + 0.4, 58.5), (x0 + 2.5, 56), (x0 + 6, top + 0.4), (x0 + 10, top + 0.8),
           (x0 + 15, top), (x0 + 19, top + 0.5), (x1 - 2, top + 2.2), (x1, top + 4), (x1 + 0.6, bottom)]
    pid = p.poly(pts, a_rock, group=70)
    if p.big:
        p.stroke([(x0 + 4, bottom - 1), (x0 + 7, bottom - 3), (x0 + 11, bottom - 2.5)], "tan0")
        p.stroke([(x0 + 16, bottom - 1.5), (x0 + 19, bottom - 3.5)], "tan0")
    return pid


def _talons(p, x, y, far=False):
    """Gold toes gripping the crag edge at (x, y), black claws curling over."""
    g = 80 + int(far)
    b = 0.3 if far else 0.0
    p.limb([(x + 1.5, y - 2.5), (x + 1, y)], 2.8, 2.4, a_gold, group=g, bias=b)
    p.limb([(x + 1, y + 0.2), (x - 2, y + 0.8)], 2.2, 1.6, a_gold, group=g, bias=b)
    p.limb([(x + 1.5, y + 0.2), (x + 4, y + 0.8)], 2.2, 1.6, a_gold, group=g, bias=b)
    if p.big:
        p.pxs([(x - 3, y + 1), (x - 3, y + 2)], "ink")
        p.pxs([(x + 4, y + 2)], "ink")


AET_NEAR = Wing((30, 43), (26, 38.5), (20.5, 39), (16.5, 41.5),
                [(9.5, 43.5), (10, 47.5), (12.5, 51)],
                [(17, 51.5), (21, 52), (25, 51)], pw=[4.0, 4.4, 4.4], sw=4.6, cov=4.0, ncov=4,
                arm=(5.4, 3.4), pfat=0.42)
AET_FAR = Wing((39, 40), (41.5, 35.5), (45, 33), (48.5, 31.5),
               [(55, 31.5), (56, 35.5), (54.5, 39.5)],
               [(50.5, 43), (46.5, 44.5)], pw=4.0, sw=4.4, cov=3.6, ncov=3, arm=(4.6, 3.0), pfat=0.42)


def _aetling_head(p, L, open_=False):
    """Head, hackles, crown feathers, brow and the big hooked beak, facing
    left, centered near (29, 31)."""
    hx, hy = 29.5, 32 - L
    hackles = fluff_pts(hx, hy, 8.6, 8.0, tufts=[(-80, 2.0, 12), (-50, 3.4, 15), (-22, 3.6, 15), (6, 3.0, 14),
                                                  (34, 2.4, 13), (-110, 1.4, 10)])
    p.poly(hackles, a_down, group=3)
    # the two stray crown feathers
    p.lens((27.5, 25.5 - L), (24, 18.5 - L), 3.0, a_crest, bend=0.8, fat=0.6, group=8)
    p.lens((30.5, 25 - L), (32.5, 19 - L), 3.0, a_crest, bend=-0.6, fat=0.6, group=9)
    # the heavy brow, a ledge over the eye sloping down to the beak
    p.poly([(19, 29 - L), (21, 26.6 - L), (26, 25.8 - L), (29.6, 27 - L), (29, 28.8 - L),
            (24.5, 28.4 - L), (21, 30.2 - L)], a_brow, group=5)
    # the beak: a deep cere and a heavy hook curling down at the tip
    gape = 1.6 if open_ else 0.0
    upper = [(23.5, 29 - L), (19.5, 29.2 - L), (16, 30.6 - L), (13.6, 33.2 - L), (13.4, 37 - L),
             (14.8, 36.4 - L), (15.6, 34.6 - L), (18, 34 - L), (23.5, 34.8 - L)]
    p.poly(upper, a_gold, group=7)
    lower = [(16.8, 34.4 - L + gape * 0.4), (23, 34.6 - L), (22.4, 36.6 - L + gape), (18.5, 36.6 - L + gape)]
    p.poly(lower, a_gold, group=6, bias=0.2)
    if not p.big:
        p.px(23, 30 - L, "ink")
        return
    p.stroke([(21, 29.6 - L), (21, 33.6 - L)], "gold0")      # cere
    p.px(19, 31 - L, "gold0")                                # nostril
    p.stroke([(16.5, 34.4 - L), (22.5, 34.4 - L)], "gold0")  # gape
    p.patch(22, 28 - L, ["1111", "1711", "1111", "1c11", ".11."], {"1": "ink", "7": "down3", "c": "gold2"})


def aetling(p, view, phase):
    if view == "icon":
        # the party icon: the eaglet facing out, wings flared, hopping
        aetling(p, "down", phase)
        return
    if view in ("front", "side"):
        L = 1 if (phase == 1 and view == "front") else 0
        beat = -8 * L
        _crag(p)
        for a, b, w in (((42, 49), (51, 51.5), 4.0), ((41.5, 50.5), (49.5, 55), 4.0)):
            p.poly(round_feather(a, b, w, root=0.7), a_tan, group=60)
        AET_FAR.moved(rot=-beat).draw(p, A_WING, 10, bias=0.12)
        _talons(p, 37, 54, far=True)
        body = fluff_pts(34, 46, 8.6, 8.8, tufts=[(200, 1.4, 10), (240, 1.4, 9), (300, 1.6, 10), (330, 1.8, 10),
                                                  (0, 1.6, 10), (30, 1.8, 10), (60, 1.4, 9), (100, 1.2, 9),
                                                  (140, 1.4, 9), (170, 1.6, 9)], ang=-10)
        p.poly(body, a_down, group=1)
        p.blob(30, 52, 3.0, 2.6, a_down, group=2)
        _talons(p, 29, 54.5)
        AET_NEAR.moved(rot=beat * 0.5).draw(p, A_WING, 20)
        _aetling_head(p, L, open_=bool(L))
        return

    if view == "back":
        # over the shoulder at about 1.2x, the head turned right in profile
        far = Wing((36, 40), (31, 30), (24, 22), (19, 18),
                   [(11, 13), (8, 18), (7, 24), (9, 30)], [(12, 36), (17, 40), (23, 42)],
                   pw=4.4, sw=5.4, cov=5.4, ncov=4, arm=(6.4, 4), pfat=0.4)
        far.draw(p, A_WING, 10, bias=0.05)
        body = fluff_pts(34, 60, 22, 16, tufts=[(190, 2.0, 8), (215, 2.4, 9), (240, 2.2, 9), (265, 2.0, 8),
                                                (295, 2.4, 9), (320, 2.0, 8), (345, 2.2, 9)])
        p.poly(body, a_down, group=1)
        near = Wing((50, 44), (54, 37), (57, 33), (60, 31),
                    [(63, 36), (63, 41), (61, 46)], [(57, 50), (53, 52)],
                    pw=4.0, sw=5.0, cov=4.6, ncov=3, arm=(5.6, 3.6), pfat=0.4)
        near.draw(p, A_WING, 20)
        # head in right profile
        hx, hy = 40, 27
        p.poly(fluff_pts(hx, hy, 9.2, 8.6, tufts=[(190, 3.6, 16), (220, 4.0, 16), (250, 3.2, 14), (160, 2.6, 12)]),
               a_down, group=3)
        p.limb(bez((40, 19), (41, 14), (43.5, 10)), 2.6, 1.6, a_crest, group=8)
        p.limb(bez((37, 19.5), (35.5, 15), (36.5, 11)), 2.6, 1.6, a_crest, group=9)
        p.poly([(49, 22.5), (45, 21), (40, 21.5), (39, 23.5), (44, 23.5), (49.5, 25)],
               a_brow, group=5)
        p.poly([(46, 23.5), (51, 24), (55, 26), (57, 29.5), (57, 33), (55.6, 32.4), (54.6, 30.5), (51.5, 30),
                (46, 30.5)], a_gold, group=7)
        p.poly([(51, 30.2), (46, 30.5), (46.5, 32.5), (50, 32.5)], a_gold, group=6, bias=0.2)
        if p.big:
            p.stroke([(48.5, 24.5), (48.5, 29)], "gold0")
            p.patch(42, 24, ["1111", "1171", "1111", "1c11", ".11."], {"1": "ink", "7": "down3", "c": "gold2"})
        return

    if view == "down":
        # follower hopping toward the camera, wings flared to look bigger
        hop = 2 * phase
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            w = Wing((X(28), 40 - hop), (X(24), 36 - hop), (X(20), 35 - hop - phase), (X(16), 36 - hop - phase),
                     [(X(9), 37 - hop - 2 * phase), (X(8.5), 42 - hop - phase), (X(10.5), 46 - hop)],
                     [(X(15), 48 - hop), (X(20), 49 - hop)], pw=3.8, sw=4.6, cov=4.0, ncov=3, arm=(5, 3),
                     pfat=0.4)
            w.draw(p, A_WING, 10 if sx < 0 else 20)
        for x in (28.5, 35.5):
            p.limb([(x, 50 - hop), (x, 56 - hop)], 3.2, 2.6, a_gold, group=30)
            p.rect(int(x) - 2, 56 - hop, int(x) + 1, 57 - hop, a_gold, group=30)
        p.poly(fluff_pts(32, 46 - hop, 8.6, 7.6, tufts=[(150, 1.4, 12), (30, 1.4, 12), (90, 1.2, 14)]), a_down,
               group=1)
        p.poly(fluff_pts(32, 32 - hop, 8.2, 7.4, tufts=[(-90, 2.0, 12), (-130, 2.2, 14), (-50, 2.2, 14),
                                                       (180, 1.6, 12), (0, 1.6, 12)]), a_down, group=3)
        p.limb(bez((30.5, 26 - hop), (29, 22 - hop), (27, 19 - hop)), 2.2, 1.4, a_crest, group=8)
        p.limb(bez((33.5, 26 - hop), (35, 22 - hop), (37, 19 - hop)), 2.2, 1.4, a_crest, group=9)
        p.poly([(29, 31 - hop), (35, 31 - hop), (35, 34 - hop), (33, 38 - hop), (31, 38 - hop), (29, 34 - hop)],
               a_gold, group=7)
        p.eye(26, 29 - hop, 2, 3, shine="down3", shine_at=(0, 0))
        p.eye(36, 29 - hop, 2, 3, shine="down3", shine_at=(1, 0))
        if p.big:
            p.stroke([(25, 28 - hop), (29, 29 - hop)], "down0")
            p.stroke([(35, 29 - hop), (39, 28 - hop)], "down0")
        return

    if view == "up":
        hop = 2 * phase
        for x in (28.5, 35.5):
            p.limb([(x, 50 - hop), (x, 56 - hop)], 3.2, 2.6, a_gold, group=30)
        p.poly(round_feather((32, 48 - hop), (32, 57 - hop), 6, root=0.7), a_tan, group=60)
        p.poly(fluff_pts(32, 45 - hop, 8.6, 8, tufts=[(150, 1.4, 12), (30, 1.4, 12)]), a_down, group=1)
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            w = Wing((X(28), 40 - hop), (X(24), 35 - hop), (X(20), 34 - hop - phase), (X(16), 35 - hop - phase),
                     [(X(9), 36 - hop - 2 * phase), (X(8.5), 41 - hop - phase), (X(10.5), 45 - hop)],
                     [(X(15), 47 - hop), (X(20), 48 - hop)], pw=3.8, sw=4.6, cov=4.0, ncov=3, arm=(5, 3),
                     pfat=0.4)
            w.draw(p, A_WING, 10 if sx < 0 else 20)
        p.poly(fluff_pts(32, 32 - hop, 8.2, 7.6, tufts=[(-90, 2.0, 12), (-130, 2.4, 14), (-50, 2.4, 14),
                                                       (90, 2.6, 30)]), a_down, group=3)
        p.limb(bez((30.5, 26 - hop), (29, 22 - hop), (27, 19 - hop)), 2.2, 1.4, a_crest, group=8)
        p.limb(bez((33.5, 26 - hop), (35, 22 - hop), (37, 19 - hop)), 2.2, 1.4, a_crest, group=9)
        return



# --------------------------------------------------------------------------
# Aetarch, the eagle of Zeus
# --------------------------------------------------------------------------

AETARCH_COLORS = [
    ("ink", INK),
    # terracotta flight feathers running up into sun-gold coverts and breast
    ("w0", (112, 40, 24)), ("w1", (176, 80, 40)), ("w2", (216, 128, 48)),
    ("g0", (240, 184, 56)), ("g1", (248, 232, 136)),
    # the marble-white head and tail
    ("m0", (152, 144, 144)), ("m1", (208, 200, 192)), ("m2", C.white),
    # Aegean-blue and white lightning
    ("b0", (24, 56, 120)), ("b1", (48, 104, 176)), ("b2", (112, 168, 224)), ("b3", (200, 232, 248)),
    # the hooked sun-gold beak and talons
    ("k0", (184, 120, 24)), ("k1", (248, 208, 64)),
]
# "Cypress-dark plumage with a white head and Aegean-blue lightning."
AETARCH_SHINY = {
    "w0": (16, 32, 32), "w1": (24, 56, 48), "w2": (40, 88, 64), "g0": (72, 128, 88), "g1": (136, 176, 128),
}

e_prim = Mat(["w0", "w1", "w2"], line="ink", cuts=[0.4, 0.74])
e_sec = Mat(["w0", "w1", "w2"], line="w0", cuts=[0.3, 0.64])
e_cov = Mat(["w1", "w2", "g0", "g1"], line="w0", cuts=[0.3, 0.56, 0.84])
e_arm = Mat(["w2", "g0", "g1"], line="w1", cuts=[0.36, 0.7])
e_gold = Mat(["w1", "w2", "g0", "g1"], line="w1", cuts=[0.2, 0.46, 0.76])
e_white = Mat(["m0", "m1", "m2"], line="m0", cuts=[0.42, 0.74])
e_beak = Mat(["k0", "k1"], line="k0", cuts=[0.55])
e_bolt = Mat(["b1", "b2", "b3"], line="b0", outline="ink", cuts=[0.34, 0.62])
E_WING = (e_prim, e_sec, e_cov, e_arm)
# the far wing sits in shadow, a step darker, so the face reads in front of it
E_FAR = (e_prim, Mat(["w0", "w1"], line="w0", cuts=[0.5]), Mat(["w0", "w1", "w2"], line="w0", cuts=[0.3, 0.62]),
         Mat(["w1", "w2", "g0"], line="w0", cuts=[0.34, 0.68]))


def zigzag(a, b, amp, k, phase=1):
    """A polyline from a to b kinked k times sideways by amp, alternating."""
    ux, uy = _unit(a, b)
    nx, ny = -uy, ux
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    pts = [a]
    for i in range(1, k + 1):
        t = i / (k + 1)
        s = amp * (1 if (i + phase) % 2 else -1)
        pts.append((a[0] + ux * L * t + nx * s, a[1] + uy * L * t + ny * s))
    pts.append(b)
    return pts


def keraunos(p, c, ang, L=17.0, g0=90, flick=0):
    """Zeus's thunderbolt as it is on the coins of Elis: a spindle grip with
    a collar at each end and a sheaf of three bolts flaring from each collar,
    the middle one a straight zigzag and the side ones curling outward.
    c is the middle of the grip, ang its direction in degrees, L the length
    of one half."""
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    nx, ny = -uy, ux

    def P(u, v):
        return (c[0] + ux * u + nx * v, c[1] + uy * u + ny * v)
    g = g0
    for sgn in (-1, 1):
        s = sgn
        f = flick * sgn
        # side bolts curl outward, then the middle bolt
        for side in (-1, 1):
            path = bez(P(s * 4.5, side * 1.0), P(s * 9, side * 4.8), P(s * (L - 2), side * (5.5 + f * 0.5)), n=10)
            p.taper(path, 4.2, e_bolt, group=g)
            g += 1
        mid = zigzag(P(s * 4.5, 0), P(s * (L + 1.5), 0.6 * sgn), 2.2, 3)
        p.taper(mid, 5.2, e_bolt, group=g)
        g += 1
        # the collar
        p.blob(*P(s * 4.4, 0), 1.6, 3.2, e_bolt, ang=ang, group=g)
        g += 1
    # the grip, a spindle swelling at the middle
    p.limb([P(-4.2, 0), P(0, 0), P(4.2, 0)], 2.6, 2.6, e_bolt, group=g)
    p.blob(*c, 2.4, 1.9, e_bolt, ang=ang, group=g)
    return g + 1


# facing left in three-quarter view, the near wing is on the right, in
# front of the body; the far wing rises on the left behind the head
AE_FAR = Wing((30.5, 27), (27.5, 9.5), (17.5, 6), (11.5, 5),
              [(4.5, 1.6), (1.6, 5.4), (1.2, 10.5), (2, 15.5), (3.8, 20.5)],
              [(6.6, 24.6), (10.6, 27.4), (15.2, 29.4), (20.4, 30.6)],
              pw=[3.2, 3.6, 3.8, 3.8, 4.0], sw=4.8, cov=5.0, ncov=5, arm=(4.6, 2.8), pfat=0.34,
              flat=((0, 0), (0, 0)))
AE_NEAR = Wing((38.5, 31.5), (39.5, 15.5), (46.5, 8.5), (52.5, 5),
               [(50.4, 0.6), (55.8, 0.8), (60.4, 3.4), (62.6, 8.4), (62.6, 14.2)],
               [(60.6, 21.6), (58, 26.6), (54.4, 30.6), (49.8, 33.8), (44.6, 35.8)],
               pw=[4.8, 5.2, 5.4, 5.4, 5.4], sw=5.8, cov=6.0, ncov=7, arm=(5.6, 3.0), pfat=0.3,
               flat=((0, 0), (0, 0)))


def _aetarch_head(p, L, open_=False, crackle=0):
    """The marble-white head in three-quarter view facing left: a flat,
    fierce brow, a sun-gold hooked beak, hackles raised at the nape."""
    hx, hy = 24.5, 18 - L
    for a, b, w in (((27.5, 13.5 - L), (37, 7 - L), 4.6), ((28.5, 16.5 - L), (39.5, 13 - L), 4.4),
                    ((28.5, 20 - L), (38, 19.5 - L), 4.2)):
        p.lens(a, b, w, e_white, bend=-0.8, fat=0.3, group=4)
    p.blob(hx, hy, 6.8, 6.0, e_white, group=3)
    p.blob(20, 20 - L, 3.6, 3.0, e_white, group=3)
    p.poly([(17, 16.1 - L), (20.5, 13.9 - L), (26, 13.5 - L), (27, 15.1 - L), (21.5, 15.9 - L), (18.5, 17.5 - L)],
           Mat(["m0", "m1"], line="m0", cuts=[0.6]), group=5)
    gape = 1.4 if open_ else 0.0
    upper = [(20, 16.5 - L), (16, 16.7 - L), (12.5, 18.1 - L), (10.1, 20.9 - L), (10.1, 24.5 - L),
             (11.5, 23.9 - L), (12.3, 22.1 - L), (14.5, 21.5 - L), (20, 22.1 - L)]
    p.poly(upper, e_beak, group=7)
    p.poly([(13.5, 21.7 - L + gape * 0.4), (19.5, 21.9 - L), (19, 23.5 - L + gape), (15, 23.5 - L + gape)],
           e_beak, group=6, bias=0.25)
    if not p.big:
        p.px(21, 17 - L, "ink")
        return
    p.stroke([(17.5, 17.1 - L), (17.5, 21.1 - L)], "k0")
    p.px(15.5, 18.5 - L, "k0")
    p.stroke([(13, 21.9 - L), (19, 21.9 - L)], "k0")
    p.patch(19, 15 - L, ["1111", "kk11", "k1m1", ".kk."], {"1": "ink", "k": "k1", "m": "m2"})


def aetarch(p, view, phase):
    if view == "icon":
        # the party icon: the displayed eagle of a coat of arms, bolt in its talons
        aetarch(p, "down", phase)
        return
    if view in ("front", "side"):
        ph = phase if view == "front" else 0
        L = ph
        beat = 5 * ph
        AE_FAR.moved(rot=-beat).draw(p, E_FAR, 10, bias=0.1)
        # tail: a white fan behind, spreading to the lower right
        for i, (a, b, w) in enumerate((((41, 46), (55.5, 51.5), 5.0), ((40.5, 47.5), (55.5, 56.5), 5.2),
                                       ((39, 48.5), (51, 60.4), 5.2), ((37.5, 49), (45, 61.2), 4.8))):
            p.poly(round_feather(a, b, w, root=0.6), e_white, group=60 + i, bias=0.04 * (3 - i))
        # far leg, thrust forward
        p.limb([(32, 43), (26, 47.5), (21.5, 50.5)], 6.0, 4.2, e_gold, group=40, bias=0.15)
        # body: breast and belly
        p.blob(32, 36.5, 9.0, 9.8, e_gold, ang=-15, group=1)
        p.blob(35.5, 44, 7.8, 6.8, e_gold, ang=-25, group=1)
        # the white neck under the head
        p.limb([(31, 31), (27, 22)], 10.4, 9.0, e_white, group=2)
        # the white hood ends over the breast in a ragged edge of feathers
        for a, b in (((26.5, 30), (27.5, 35.5)), ((29.5, 31), (30.5, 37)), ((32.5, 31), (34, 36.5)),
                     ((35, 29.5), (37.5, 34))):
            p.lens(a, b, 4.0, e_white, fat=0.4, group=2)
        AE_NEAR.moved(rot=beat).draw(p, E_WING, 20)
        # near leg, the feathered trousers
        p.limb([(36, 45), (31, 49.5), (27, 51.5)], 7.6, 4.8, e_gold, group=41)
        # the thunderbolt, then the talons around its grip
        keraunos(p, (24, 55), -6, L=19, flick=ph)
        for x, y in ((20.5, 51.5), (26.5, 52)):
            p.limb([(x + 1.5, y - 1.5), (x, y + 1)], 3.4, 3.0, e_beak, group=95)
        _aetarch_head(p, L, open_=bool(ph))
        return

    if view == "back":
        # over the shoulder at about 1.2x: wings spread, the head turned
        # right in profile, the thunderbolt held high in a raised talon
        far = Wing((44, 46), (49, 33), (55, 22), (57, 14),
                   [(52, 3), (57, 2), (61.5, 5), (63, 10.5)],
                   [(62.5, 18), (62, 25), (60, 32), (56, 38)],
                   pw=3.6, sw=5.0, cov=5.6, ncov=4, arm=(5.0, 3.0), pfat=0.36)
        far.draw(p, E_WING, 10, bias=0.12)
        near = Wing((24, 46), (16, 34), (9, 20), (8, 12),
                    [(14, 1.5), (8.5, 1.5), (4, 4), (1.4, 8.5), (1.2, 14)],
                    [(1.2, 21), (1.6, 28), (4, 35), (8, 41), (13.5, 46)],
                    pw=4.2, sw=5.6, cov=6.4, ncov=5, arm=(6.4, 3.6), pfat=0.36)
        p.blob(32, 60, 21, 13, e_gold, group=1)
        p.blob(34, 47, 10, 8, e_gold, group=1)
        near.draw(p, E_WING, 20)
        p.limb([(37, 44), (41, 35), (44, 29)], 10, 9, e_white, group=2)
        p.blob(45.5, 23, 7.8, 7.0, e_white, group=3)
        for a, b, w in (((41, 20), (31, 16), 4.8), ((40.5, 24), (30.5, 24.5), 4.6), ((42, 17), (36, 10), 4.4)):
            p.lens(a, b, w, e_white, bend=1.0, fat=0.3, group=4)
        p.poly([(50, 20), (55, 20.5), (59, 23), (61, 27), (61, 30.5), (59.5, 29.6), (58.5, 27.5), (55, 27),
                (50, 27.5)], e_beak, group=7)
        p.poly([(54.5, 27.2), (50, 27.5), (50.5, 29.5), (54, 29.4)], e_beak, group=6, bias=0.25)
        # the raised talon and the bolt above the far shoulder
        p.limb([(44, 46), (50, 41), (53, 36)], 6, 4.4, e_gold, group=42)
        keraunos(p, (54, 33), -60, L=15)
        p.limb([(52.5, 36), (55, 33.5)], 3.2, 2.6, e_beak, group=96)
        if p.big:
            p.patch(47, 20, ["1111", "kk11", "k1m1", ".kk."], {"1": "ink", "k": "k1", "m": "m2"})
        return

    if view in ("down", "up"):
        # follower: the displayed eagle of a coat of arms, wings spread wide
        beat = 6 * phase
        face = view == "down"
        if not face:
            for a, b in (((32, 46), (26, 59)), ((32, 46), (32, 60)), ((32, 46), (38, 59))):
                p.poly(round_feather(a, b, 5.0, root=0.6), e_white, group=60)
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            w = Wing((X(28), 34), (X(22), 24), (X(14), 18), (X(9), 14),
                     [(X(8), 6), (X(4), 9), (X(2), 14), (X(2.4), 19.5), (X(4.4), 24)],
                     [(X(7), 29), (X(11), 33), (X(16), 36), (X(22), 38)],
                     pw=3.8, sw=5.0, cov=5.4, ncov=4, arm=(5.0, 3.0), pfat=0.36)
            w.moved(rot=-sx * beat, about=(X(28), 34)).draw(p, E_WING, 10 if sx < 0 else 20)
        p.blob(32, 38, 7.4, 9.0, e_gold if face else e_cov, group=1)
        if face:
            for x in (28.5, 35.5):
                p.limb([(x, 44), (x, 50)], 4.4, 3.4, e_gold, group=41)
            keraunos(p, (32, 52.5), 0, L=13)
            for x in (28.5, 35.5):
                p.limb([(x, 49.5), (x, 52.5)], 3.0, 2.6, e_beak, group=95)
        p.blob(32, 24, 6.4, 6.2, e_white, group=3)
        p.lens((28, 21), (22, 15), 4.0, e_white, fat=0.3, group=4)
        p.lens((36, 21), (42, 15), 4.0, e_white, fat=0.3, group=4)
        if face:
            p.poly([(29.5, 24), (34.5, 24), (34, 28), (32, 31), (30, 28)], e_beak, group=7)
            p.eye(27, 22, 3, 2, iris=None, shine=None)
            p.eye(34, 22, 3, 2, iris=None, shine=None)
            if p.big:
                p.pxs([(27, 23), (36, 23)], "k1")
        return


MONS = [
    # icon palette 1 keeps the white down, tan wings and gold beak
    Mon("Aetling", AETLING_COLORS, AETLING_SHINY, aetling, foot="bird", icon_pal=1),
    # icon palette 3 keeps the plumage warm brown and gold and the bolt blue
    Mon("Aetarch", AETARCH_COLORS, AETARCH_SHINY, aetarch, foot="bird", icon_pal=3),
]
