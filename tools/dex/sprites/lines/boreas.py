"""Boreas line: Kryopuff, Borapteryx (Ice, then Ice/Flying). Boreas, the
winged North Wind, who carried off Oreithyia in a whirlwind (Ovid,
Metamorphoses 6) and wrecked the Persian fleet off Artemision for the
Athenians who prayed to him (Herodotus 7.189).

Kryopuff is a little cold gust with the puffed cheeks of the wind faces on
the Tower of the Winds, a cloud of puffs blowing through a small round
mouth. Borapteryx is the North Wind as a creature: a bird-dragon rushing
forward on dusky purple wings, a crest of frost feathers streaming from its
crown and a ruff of icicle feathers at its throat (the old god's wild hair
and frost beard), blowing a blast of snow from its open beak, its body
trailing into two curling tails of gale like the snake-legged Boreas on the
Chest of Kypselos (Pausanias 5.19.1).

The battle sprites are hand finished in tools/dex/sprites/art/; this file is
the draft they started from, and it still draws the icons and followers.
"""
import math

from mon_lib import C, Mat, Mon, bez, bez3, lerp, lens_pts

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


def _qb(p0, p1, p2, t):
    a, b, c = (1 - t) ** 2, 2 * (1 - t) * t, t * t
    return (a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1])


def round_feather(a, b, w, bend=0.0, n=10, root=0.5):
    """A feather with a rounded tip, narrow at the root a."""
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


def spiral(c, r0, r1, a0, turns, n=40, sq=1.0):
    """An Archimedean spiral around c from radius r0 at angle a0 (degrees)
    to radius r1 after `turns` turns (positive turns run clockwise)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(a0 + 360 * turns * t)
        r = r0 + (r1 - r0) * t
        pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a) * sq))
    return pts


class Wing:
    """A real wing: a curved leading edge from the shoulder S, bowed through
    C, to the wrist Wr, and the hand on to Hd. Primaries fan out of the hand
    to separate points; secondaries hang from the forearm; the coverts and
    the marginal band (the arm) lie over their roots."""

    def __init__(self, S, C, Wr, Hd, prim, sec, pw, sw, cov=5.0, ncov=5, arm=(4.4, 2.4), pfat=0.35):
        self.S, self.C, self.Wr, self.Hd = S, C, Wr, Hd
        self.prim, self.sec = prim, sec
        self.pw, self.sw = pw, sw
        self.cov, self.ncov = cov, ncov
        self.arm_w = arm
        self.pfat = pfat

    def arm(self, t):
        if t <= 1:
            return _qb(self.S, self.C, self.Wr, t)
        return lerp(self.Wr, self.Hd, (t - 1) / 0.6)

    def trail(self, t):
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
        c = about or self.S

        def T(q):
            q = _rot(q, c, rot)
            return (q[0] + dx, q[1] + dy)
        return Wing(T(self.S), T(self.C), T(self.Wr), T(self.Hd), [T(q) for q in self.prim],
                    [T(q) for q in self.sec], self.pw, self.sw, self.cov, self.ncov, self.arm_w, self.pfat)

    def draw(self, p, mats, g0, bias=0.0):
        """mats: (primaries, secondaries, coverts, arm)."""
        mp, ms, mc, ma = mats
        g = g0
        n = len(self.prim)
        big = p.big
        for i, tip in enumerate(self.prim):
            if not big and i % 2:
                continue
            base = lerp(self.Hd, self.Wr, 0.85 * i / max(n - 1, 1))
            w = self.pw[i] if isinstance(self.pw, (list, tuple)) else self.pw
            if not big:
                w *= 1.5
            p.poly(lens_pts(base, tip, w, 0, n=12, fat=self.pfat), mp, group=g, bias=bias)
            g += 1
        m = len(self.sec)
        for i, tip in enumerate(self.sec):
            if not big and i % 2:
                continue
            t = 0.95 - 0.8 * i / max(m - 1, 1)
            p.poly(round_feather(self.arm(t), tip, self.sw * (1 if big else 1.4), root=0.7), ms, group=g,
                   bias=bias)
            g += 1
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
        path = [self.arm(k / 20 * 1.6) for k in range(21)]
        p.limb(path, self.arm_w[0], self.arm_w[1], ma, group=g, bias=bias - 0.05)
        return g + 1


def puff_pts(lobes, n=48):
    """The outline of a cloud: the union of round lobes [(cx, cy, r), ...],
    as polygons for one part."""
    out = []
    for cx, cy, r in lobes:
        out.append([(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n))
                    for i in range(n)])
    return out


# --------------------------------------------------------------------------
# Kryopuff, the cold gust
# --------------------------------------------------------------------------

KRYOPUFF_COLORS = [
    ("ink", INK),
    # marble-white and pale Aegean-blue cloud
    ("c0", (104, 144, 200)), ("c1", (160, 200, 232)), ("c2", (208, 232, 248)), ("c3", C.white),
    # darker Aegean-blue frost: the breath and the cowlick
    ("f0", (24, 56, 120)), ("f1", (48, 104, 176)), ("f2", (112, 168, 224)),
    # dusky purple wingtips
    ("p0", (56, 40, 88)), ("p1", (104, 80, 144)), ("p2", (160, 136, 200)),
    # a cold flush on the puffed cheeks
    ("blush", (224, 168, 200)),
]
# "Limestone-tan cloud with sun-gold frost."
KRYOPUFF_SHINY = {
    "c0": (160, 120, 72), "c1": (208, 176, 120), "c2": (232, 216, 168), "c3": (248, 240, 216),
    "f0": (152, 88, 16), "f1": (200, 144, 40), "f2": (240, 200, 72),
}

k_cloud = Mat(["c0", "c1", "c2", "c3"], line="c0", cuts=[0.24, 0.5, 0.74])
k_frost = Mat(["f0", "f1", "f2", "c3"], line="f0", cuts=[0.24, 0.5, 0.78])
k_wisp = Mat(["p0", "p1", "p2"], line="p0", cuts=[0.36, 0.7])
k_tip = Mat(["c1", "c2", "c3"], line="c0", cuts=[0.4, 0.72])
k_breath = Mat(["f1", "f2", "c3"], line="f1", cuts=[0.4, 0.7])


def _wisp(p, root, tips, g, bias=0.0):
    """A stubby feathery wing-wisp: cloud feathers with dusky purple tips."""
    for i, tip in enumerate(tips):
        p.poly(round_feather(root, tip, 3.6, root=0.6), k_wisp, group=g + i, bias=bias)
    # cloud coverts over the roots
    p.blob(root[0], root[1], 3.2, 2.8, k_cloud, group=g + len(tips), bias=bias)


def _breath(p, mouth, L, sway=0):
    """The stream of frost: a tapering ribbon curling away from the mouth."""
    x, y = mouth
    path = bez3((x, y), (x - 5, y + 1), (x - 8, y + 6 + sway), (x - 13, y + 5 + sway), n=16)
    p.limb(path, 3.6, 1.4, k_frost, group=90)
    curl = spiral((x - 13.5, y + 2.6 + sway), 2.6, 0.8, 90, -0.8, n=14)
    p.limb(curl, 1.6, 1.2, k_frost, group=90)


def kryopuff(p, view, phase):
    if view in ("front", "side", "icon"):
        L = phase if view == "front" else 0
        bob = -L
        # far wing-wisp, up behind the back
        _wisp(p, (40, 36 + bob), [(45, 29.6 + bob - L), (48.4, 32 + bob - L), (49, 36 + bob)], 10, bias=0.15)
        # the cloud body: lobes around a round middle
        lobes = [(33.6, 44 + bob, 8.0), (29, 37 + bob, 5.2), (36.6, 35.4 + bob, 4.8), (42.4, 39.8 + bob, 4.4),
                 (43.2, 46.2 + bob, 4.2), (39, 51.2 + bob, 4.0), (32.4, 51.8 + bob, 4.0), (26.6, 49.4 + bob, 3.8)]
        p.polys(puff_pts(lobes), k_cloud, group=1)
        # near wing-wisp, stubby, on the side
        _wisp(p, (39, 45 + bob), [(46.4, 42.6 + bob - L), (47.6, 46.6 + bob), (45.6, 50.6 + bob + L)], 20)
        # the puffed near cheek
        p.blob(25.6, 45.4 + bob, 4.6, 4.0, k_cloud, group=3, bias=-0.2)
        # the cowlick: a curl of frost on the brow
        p.limb(bez((30, 36 + bob), (27.5, 30.5 + bob), (31.6, 29.6 + bob)), 3.4, 2.2, k_frost, group=8)
        p.limb(bez((31.6, 29.6 + bob), (34, 30.6 + bob), (32.6, 33 + bob)), 2.2, 1.6, k_frost, group=8)
        # a small round blowing mouth and the frost breath streaming from it
        p.blob(21.6, 46.6 + bob, 1.6, 1.6, Mat(["f0"]), group=6)
        path = bez3((18.6, 46.6 + bob), (13, 47.4 + bob), (10.6, 52 + bob + L), (6.4, 50 + bob + L), n=14)
        p.limb(path, 4.6 if p.big else 5.6, 1.8, k_breath, group=90)
        if p.big:
            p.limb(spiral((7.6, 47.4 + bob + L), 2.6, 0.8, 100, -0.8, n=10), 2.0, 1.4, k_breath, group=90)
        if not p.big:
            p.px(26, 39 + bob, "ink")
            p.px(32, 38.5 + bob, "ink")
            return
        # big eyes, the near one larger
        p.eye(24, 37 + bob, 4, 5, shine="c3", shine_at=(2, 1))
        p.eye(31, 37 + bob, 4, 5, shine="c3", shine_at=(2, 1))
        p.pxs([(26, 46 + bob), (27, 46 + bob)], "blush")
        p.px(20, 46 + bob, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the back of the cloud, the head
        # turned right in profile, the breath streaming off to the right
        p.polys(puff_pts([(30, 54, 14), (20, 50, 8), (40, 50, 8), (28, 42, 9.5), (37, 40, 8.5), (24, 60, 8)]),
                k_cloud, group=1)
        _wisp(p, (16, 50), [(8, 46), (6.5, 51), (8, 56)], 10)
        p.blob(44, 46, 4.6, 4.2, k_cloud, group=3)
        p.limb(bez((32, 33), (34, 26), (30, 25)), 3.4, 2.4, k_frost, group=8)
        p.limb(spiral((29.5, 28), 2.8, 0.8, -90, -0.7, n=12), 2.4, 1.6, k_frost, group=8)
        p.blob(48.5, 47, 2.2, 2.2, Mat(["c0", "c1"], line="c0", cuts=[0.5]), group=6)
        path = bez3((50, 47.5), (55, 48.5), (58, 53), (62, 52), n=16)
        p.limb(path, 4.2, 1.6, k_frost, group=90)
        if p.big:
            p.eye(40, 39, 3, 5, shine="c3", shine_at=(1, 1))
            p.pxs([(42, 45), (43, 45)], "blush")
        return

    if view in ("down", "up"):
        bob = -phase
        face = view == "down"
        lobes = [(32, 44 + bob, 9), (26, 38 + bob, 5.4), (38, 38 + bob, 5.4), (23.5, 46 + bob, 4.6),
                 (40.5, 46 + bob, 4.6), (32, 51 + bob, 5)]
        _wisp(p, (23, 45 + bob), [(16, 41 + bob), (15, 46 + bob), (17, 50 + bob)], 10)
        _wisp(p, (41, 45 + bob), [(48, 41 + bob), (49, 46 + bob), (47, 50 + bob)], 20)
        p.polys(puff_pts(lobes), k_cloud, group=1)
        p.limb(bez((32, 37 + bob), (30, 31 + bob), (34, 30 + bob)), 2.8, 2.0, k_frost, group=8)
        if face:
            p.blob(27, 47 + bob, 3.6, 3.2, k_cloud, group=3)
            p.blob(37, 47 + bob, 3.6, 3.2, k_cloud, group=3)
            p.blob(32, 48.5 + bob, 1.8, 1.8, Mat(["c0", "c1"], line="c0", cuts=[0.5]), group=6)
            p.eye(25.5, 38 + bob, 4, 5, shine="c3", shine_at=(2, 1))
            p.eye(34.5, 38 + bob, 4, 5, shine="c3", shine_at=(1, 1))
        else:
            # the breath streams behind, over the top
            p.limb(bez((32, 36 + bob), (28 + 2 * phase, 31), (31, 26)), 3.0, 1.4, k_frost, group=90)
        return


# --------------------------------------------------------------------------
# Borapteryx, the North Wind
# --------------------------------------------------------------------------

BORAPTERYX_COLORS = [
    ("ink", INK),
    # marble-white and pale Aegean-blue body and gale, darker Aegean shading
    ("g0", (40, 72, 136)), ("g1", (88, 136, 200)), ("g2", (160, 200, 232)), ("g3", (216, 232, 248)),
    ("white", C.white),
    # dusky purple wings
    ("p0", (56, 40, 88)), ("p1", (104, 80, 144)), ("p2", (152, 128, 192)), ("p3", (200, 184, 224)),
    # the frost crest and the icicle ruff at the throat
    ("h0", (120, 144, 168)), ("h1", (184, 200, 216)), ("h2", (232, 240, 240)),
    # an ice-blue glow in the eyes and the blast
    ("glow", (136, 232, 248)),
    ("night", (24, 32, 72)),
]
# "Sun-gold wings and a limestone-gray beard": the beard is now the throat
# ruff (and the crest shares its frost), so they turn limestone gray.
BORAPTERYX_SHINY = {
    "p0": (112, 64, 16), "p1": (184, 120, 32), "p2": (232, 176, 56), "p3": (248, 224, 136),
    "h0": (128, 120, 104), "h1": (184, 176, 160), "h2": (224, 216, 200),
}

b_body = Mat(["g0", "g1", "g2", "g3"], line="g0", cuts=[0.2, 0.46, 0.72])
b_gale = Mat(["g1", "g2", "g3", "white"], line="g0", cuts=[0.24, 0.5, 0.76])
b_prim = Mat(["night", "p0", "p1"], line="night", cuts=[0.36, 0.66])
b_sec = Mat(["p0", "p1", "p2"], line="p0", cuts=[0.36, 0.66])
b_cov = Mat(["p1", "p2", "p3"], line="p0", cuts=[0.36, 0.7])
b_arm = Mat(["p1", "p2", "p3"], line="p0", cuts=[0.3, 0.6])
b_hair = Mat(["h0", "h1", "h2"], line="h0", cuts=[0.38, 0.7])
B_WING = (b_prim, b_sec, b_cov, b_arm)

# rushing left, the wings swept back: the far wing raised high behind, the
# near wing spread back to the right over the body
BW_FAR = Wing((34, 25), (32.5, 11.5), (38.5, 4.5), (43.5, 2.5),
              [(44.6, 1.0), (49.4, 1.0), (54, 2.2), (57.8, 5.0)],
              [(58.4, 9.4), (55, 12.8), (50.4, 15.4), (45, 17.2), (39.6, 18.2)],
              pw=[4.6, 5.0, 5.2, 5.2], sw=5.8, cov=5.0, ncov=6, arm=(5.4, 3.0), pfat=0.3)
BW_NEAR = Wing((35.5, 28.5), (39.5, 16.5), (47.5, 14.5), (54, 16.5),
               [(62.6, 13.4), (62.6, 19.4), (62.2, 25.4), (60.4, 31.4)],
               [(57.6, 37.6), (52.6, 40.6), (47, 41.6), (41.6, 40.6)],
               pw=[4.8, 5.2, 5.4, 5.4], sw=6.0, cov=6.4, ncov=7, arm=(6.4, 3.4), pfat=0.3)
# the far wing sits a step darker, in its own shadow
B_FAR = (b_prim, Mat(["night", "p0", "p1"], line="night", cuts=[0.36, 0.66]),
         Mat(["p0", "p1", "p2"], line="p0", cuts=[0.36, 0.7]), Mat(["p1", "p2", "p3"], line="p0", cuts=[0.3, 0.6]))


b_beak = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.4, 0.7])
b_maw = Mat(["night"])


def _bdragon(p, X, Y, k=1.0, gape=0.0, flip=False):
    """The bird-dragon head in three-quarter view facing left, its skull
    centred at (X, Y): a crest of frost feathers streaming back, a ruff of
    icicle feathers at the throat, a hooked glacier-blue beak open on the
    blast, a frost brow ridge over a glowing ice eye set on the side of the
    skull."""
    S = -1 if flip else 1

    def P(x, y):
        return (X + S * (x - 27) * k, Y + (y - 16.5) * k)
    for a, b, w, bd in (((31, 18.4), (38.4, 19.6), 4.4, -0.4), ((30.4, 14.6), (46.6, 9.4), 5.6, -1.2),
                        ((28.6, 12.4), (45.4, 3.6), 6.2, -1.8), ((26, 11.4), (40.4, 0.6), 6.0, -2.0),
                        ((23.4, 11.0), (30.4, 1.0), 5.0, -1.4)):
        p.lens(P(*a), P(*b), w * k, b_hair, bend=bd * k * S, fat=0.26, group=4)
    for a, b, w, bd in (((31.4, 21.6), (35.6, 37.0), 5.4, 1.0), ((27.6, 22.6), (29.8, 41.6), 6.2, 1.4),
                        ((23.4, 23.0), (23.6, 40.0), 6.0, 1.2), ((19.6, 23.0), (17.6, 35.4), 5.0, 0.8)):
        p.lens(P(*a), P(*b), w * k, b_hair, bend=bd * k * S, fat=0.22, group=5)
    p.blob(*P(27, 16.5), 8.6 * k, 6.6 * k, b_body, ang=-6 * S, group=3)
    p.poly([P(22, 21.2), P(16, 22.4 + gape), P(12, 24.2 + gape), P(10.4, 25.8 + gape), P(12.6, 26.8 + gape),
            P(17.4, 26.2 + gape), P(22.6, 24.4)], b_beak, group=6)
    p.poly([P(21.6, 19.8), P(13.2, 20.0), P(12.4, 22.4 + gape * 0.6), P(16, 22.6 + gape * 0.8), P(21.6, 21.6)],
           b_maw, group=6)
    p.poly([P(22.4, 12.4), P(16.6, 13.2), P(12.8, 15.0), P(10.2, 17.6), P(9.2, 20.2), P(9.8, 22.8), P(11.2, 21.6),
            P(13.4, 20.0), P(22.6, 19.6)], b_beak, group=7)
    p.poly([P(19.6, 13.4), P(22.6, 10.6), P(28.6, 10.4), P(31.4, 12.0), P(30.4, 13.4), P(25.2, 13.4),
            P(21.4, 15.4)], b_hair, group=8)
    ex, ey = P(23, 14)
    p.eye(ex - (3 if flip else 0), ey, 4, 3, iris="glow", shine="white", shine_at=(1 if flip else 2, 0))


def _gale_tail(p, path, w0, w1, g, bias=0.0):
    p.limb(path, w0, w1, b_gale, group=g, bias=bias)


def _bhead34(p, phase, wing=False):
    """The icon and the walking follower: the bird-dragon head and a curl of
    wind (and for the icon, one great wing behind)."""
    bob = -phase
    if wing:
        Wing((36, 32), (41, 20), (49, 12), (55, 10),
             [(61, 8), (62.6, 14), (61.6, 20)], [(57, 26), (51, 31), (44, 34)],
             pw=6.0, sw=7.0, cov=6.0, ncov=4, arm=(6.4, 3.6)).draw(p, B_WING, 10, bias=0.1)
    p.limb(spiral((30, 52 + bob), 6.6, 1.6, 200 + 40 * phase, -1.0, n=24), 5.0, 2.0, b_gale, group=60)
    _bdragon(p, 30, 20 + bob, k=1.3, gape=phase)


def borapteryx(p, view, phase):
    if view == "icon":
        _bhead34(p, phase, wing=True)
        return
    if view == "side":
        _bhead34(p, phase)
        return
    if view == "front":
        L = phase
        beat = 4 * phase
        BW_FAR.moved(rot=beat).draw(p, B_FAR, 10, bias=0.1)
        # the far gale tail, trailing back to the right and curling up
        _gale_tail(p, bez3((39, 44), (46, 52), (54, 56), (58.6, 50), n=20) +
                   spiral((54.8, 49.2), 3.8, 1.2, 15, -0.85, n=14)[1:], 7.4, 1.8, 60, bias=0.12)
        # torso and the neck rising to the head
        p.blob(35, 34, 7.6, 7.0, b_body, ang=15, group=1)
        p.limb([(34, 34), (37.5, 41), (38.5, 46)], 12, 7, b_body, group=1)
        p.limb([(34, 34), (31.5, 27), (28, 21 - L)], 11, 9, b_body, group=2)
        BW_NEAR.moved(rot=-beat).draw(p, B_WING, 20)
        # the near gale tail, curling down and forward under the body
        _gale_tail(p, bez3((37, 44), (35.5, 54), (28, 58.5), (20.5, 56), n=20) +
                   spiral((21.6, 51.6), 4.2, 1.2, 100, 0.85, n=14)[1:], 8.4, 2.0, 61)
        _bdragon(p, 29, 17 - L, k=1.15, gape=L)
        # the blast of snow from the open beak
        for b_, w in (((1.2, 17), 4.4), ((1.2, 26), 5.4), ((3.4, 36), 5.0)):
            p.lens((10.4, 23.6 - L), b_, w, b_gale, fat=0.25, group=92)
        return

    if view == "back":
        # over the shoulder at about 1.2x: the head turned right in profile,
        # the near wing a fan of feathers arcing up, the far wing behind
        Wing((47, 40), (51, 25), (55.5, 13.6), (57.6, 7.6),
             [(53.4, 1.4), (57.4, 1.2), (61, 3.6), (62.6, 8.0)], [(62.6, 13.4), (61.4, 18), (58.6, 21.4)],
             pw=4.6, sw=6.0, cov=5.0, ncov=5, arm=(5.2, 3.0), pfat=0.32).draw(p, B_FAR, 10, bias=0.1)
        pv = (27, 46)

        def at(ang, r):
            return (pv[0] + r * math.cos(math.radians(ang)), pv[1] + r * math.sin(math.radians(ang)))
        for ang, tip, w in ((158, (11.8, 47.4), 6.4), (172, (6.2, 42.4), 6.8), (-174, (2.4, 35.2), 7.0),
                            (-161, (1.2, 26.4), 7.0), (-148, (1.4, 17.6), 6.6)):
            p.poly(round_feather(at(ang, 12), tip, w, root=0.6), b_sec, group=20)
        for ang, tip, w in ((-134, (2.0, 9.6), 6.0), (-122, (6.6, 4.2), 6.0), (-110, (13.6, 1.6), 5.8),
                            (-98, (21, 1.6), 5.4)):
            p.lens(at(ang, 12), tip, w, b_prim, fat=0.32, group=21 + int(-ang))
        p.polys([round_feather(at(ang, 5), at(ang, 19), 6.4, root=0.8) for ang in range(-96, 175, 13)], b_cov, group=40)
        p.polys([round_feather(at(ang, 3), at(ang, 10.5), 6.0, root=0.85) for ang in range(-92, -175, -14)], b_arm,
                group=41)
        p.blob(34, 64, 21, 15, b_body, group=1)
        p.blob(35, 50, 11.5, 9, b_body, group=1)
        p.limb([(36, 48), (37, 38), (39.5, 30)], 12, 10, b_body, group=2)
        _bdragon(p, 39.5, 23.5, k=1.2, flip=True)
        return

    if view in ("down", "up"):
        # follower: just the head and a curl of wind
        bob = -phase
        face = view == "down"
        p.limb(spiral((32, 50 + bob), 7.0, 1.6, 180 + 40 * phase, -1.1, n=24), 4.6, 1.8, b_gale, group=60)
        # the crest of frost feathers, fanned up and out behind the head
        for ang, ln, w in ((-160, 17, 6.0), (-128, 20, 6.6), (-92, 18, 6.4), (-56, 20, 6.6), (-20, 17, 6.0)):
            a = math.radians(ang + (8 if phase else 0) * (1 if ang < -90 else -1))
            tip = (32 + math.cos(a) * ln, 26 + bob + math.sin(a) * ln)
            p.lens((32 + math.cos(a) * 4, 26 + bob + math.sin(a) * 4), tip, w, b_hair, fat=0.26, group=4)
        # the ruff of icicle feathers at the throat
        for a_, b_, w, bend in (((27, 32 + bob), (23.4, 46 + bob), 6.0, -1.2), ((37, 32 + bob), (40.6, 46 + bob), 6.0, 1.2),
                                ((32, 33 + bob), (32, 49 + bob), 6.6, 0.0)):
            p.lens(a_, b_, w, b_hair, bend=bend, fat=0.26, group=5)
        p.blob(32, 27 + bob, 8.0, 6.8, b_body, group=3)
        if face:
            # the beak pointing at us, open on a cold breath
            p.poly([(29.4, 30.6 + bob), (34.6, 30.6 + bob), (33.4, 35.4 + bob), (32, 36.6 + bob), (30.6, 35.4 + bob)],
                   b_maw, group=6)
            p.poly([(27.6, 26.6 + bob), (36.4, 26.6 + bob), (35, 31 + bob), (32, 34 + bob), (29, 31 + bob)], b_beak,
                   group=7)
            # frost brow ridges over eyes set on the sides of the skull
            p.poly([(23.6, 21.6 + bob), (29.4, 23.4 + bob), (29, 25 + bob), (24, 24 + bob)], b_hair, group=8)
            p.poly([(40.4, 21.6 + bob), (34.6, 23.4 + bob), (35, 25 + bob), (40, 24 + bob)], b_hair, group=9)
            if p.big:
                p.eye(24.4, 24.6 + bob, 3, 3, iris="glow", shine="white", shine_at=(1, 0))
                p.eye(36.6, 24.6 + bob, 3, 3, iris="glow", shine="white", shine_at=(1, 0))
            else:
                # at follower size the eyes are two points of glowing ice
                p.pxs([(25.4, 25.4 + bob), (37.6, 25.4 + bob)], "glow")
        return


MONS = [
    # icon palette 0 keeps the pale blue and the dusky purple
    Mon("Kryopuff", KRYOPUFF_COLORS, KRYOPUFF_SHINY, kryopuff, foot="blank", icon_pal=0),
    Mon("Borapteryx", BORAPTERYX_COLORS, BORAPTERYX_SHINY, borapteryx, foot="blank", icon_pal=0),
]
