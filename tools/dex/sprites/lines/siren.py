"""Siren line: Elegull, Seirenade (Ghost, then Ghost/Flying). The Sirens,
the bird-bodied singers whose song wrecks sailors on their rocks (Odyssey
12.39-54, 158-200), drawn as concept C, "The False Beacon": a frigatebird
whose glowing throat sac is a false lighthouse luring ships onto the rocks.

Elegull is the frigate chick: a downy, big-headed fledgling perched on a
bleached bone from the Sirens' meadow, its loose throat pouch giving off
the first faint ember glow when it cries. Seirenade is the grown wrecker:
a black ghost-frigatebird on long angular wings, its inflated throat sac
blazing like a beacon, its forked tail curving into the arms of a lyre
strung with the same ember light.

The battle sprites are hand finished in tools/dex/sprites/art/; this file
is the draft they started from, and it still draws the icons and followers.
"""
import math

from mon_lib import Mat, Mon, bez, lerp, lens_pts

# --------------------------------------------------------------------------
# Shared geometry
# --------------------------------------------------------------------------


def _rot(pt, c, deg):
    ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    x, y = pt[0] - c[0], pt[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def fuzz_pts(cx, cy, rx, ry, n=10, jag=1.2, rot=0.0, skip=()):
    """An ellipse whose rim breaks into soft tufts of down. skip lists the
    tuft indices to leave smooth (where a beak or wing covers the rim)."""
    pts = []
    for i in range(n * 2):
        t = 2 * math.pi * i / (n * 2) + rot
        k = jag if (i % 2 == 0 and i // 2 not in skip) else 0.0
        pts.append((cx + (rx + k) * math.cos(t), cy + (ry + k) * math.sin(t)))
    return pts


def round_feather(a, b, w, bend=0.0, n=10, root=0.5):
    """A feather with a rounded tip: narrow at the root a, full width toward
    the tip b (secondaries, coverts, tail)."""
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


class FrigateWing:
    """A frigatebird wing (after the eagle wing in aetos.py): a short arm
    bowed from the shoulder S through C up to a sharply bent wrist Wr, then
    a long hand on to Hd whose primaries sweep back to one sharp tip.
    Secondaries hang from the arm; greater coverts and the marginal band lie
    over their roots. Four value masses: lit leading edge, coverts,
    secondaries, dark primaries.

    prim: primary tips from the outermost (the wing tip) inward. sec:
    secondary tips from the hand back to the body."""

    def __init__(self, S, C, Wr, Hd, prim, sec, pw, sw, cov=5.0, ncov=5, arm=(4.4, 2.4), pfat=0.3,
                 flat=None):
        self.S, self.C, self.Wr, self.Hd = S, C, Wr, Hd
        self.prim, self.sec = prim, sec
        self.pw, self.sw = pw, sw
        self.cov, self.ncov = cov, ncov
        self.arm_w = arm
        self.pfat = pfat
        self.flat = flat

    def arm(self, t):
        """t 0 at the shoulder, 1 at the wrist, up to 1.6 out along the hand."""
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

    def moved(self, rot=0.0, about=None, dx=0.0, dy=0.0, tip=0.0):
        """A copy rotated about the shoulder (a wingbeat); tip also swings
        the hand about the wrist."""
        c = about or self.S

        def M(q):
            q = _rot(q, c, rot)
            return (q[0] + dx, q[1] + dy)
        w = FrigateWing(M(self.S), M(self.C), M(self.Wr), M(self.Hd), [M(q) for q in self.prim],
                        [M(q) for q in self.sec], self.pw, self.sw, self.cov, self.ncov, self.arm_w, self.pfat,
                        self.flat)
        if tip:
            w.Hd = _rot(w.Hd, w.Wr, tip)
            w.prim = [_rot(q, w.Wr, tip) for q in w.prim]
        return w

    def draw(self, p, mats, g0, bias=0.0):
        """mats: (primaries, secondaries, coverts, arm). Returns the next
        free group."""
        mp, ms, mc, ma = mats
        g = g0
        n = len(self.prim)
        big = p.big
        for i, tip in enumerate(self.prim):
            if not big and i % 2:
                continue
            base = lerp(self.Hd, self.Wr, 0.9 * i / max(n - 1, 1))
            w = self.pw[i] if isinstance(self.pw, (list, tuple)) else self.pw
            if not big:
                w *= 1.5
            pts = lens_pts(base, tip, w, 0.0, fat=self.pfat)
            if self.flat:
                flat_feather(p, pts, base, tip, mp, self.flat[0][0], self.flat[0][1], group=g, bias=bias)
            else:
                p.poly(pts, mp, group=g, bias=bias)
            g += 1
        m = len(self.sec)
        polys = []
        for i, tip in enumerate(self.sec):
            t = 0.98 - 0.85 * i / max(m - 1, 1)
            polys.append(round_feather(self.arm(t), tip, self.sw, root=0.7))
        if self.flat and big:
            for i, (pts, tip) in enumerate(zip(polys, self.sec)):
                t = 0.98 - 0.85 * i / max(m - 1, 1)
                flat_feather(p, pts, self.arm(t), tip, ms, self.flat[1][0], self.flat[1][1], group=g, bias=bias)
                g += 1
        else:
            p.polys(polys, ms, group=g, bias=bias)
            g += 1
        polys = []
        for j in range(self.ncov):
            t = 0.1 + 1.2 * (j + 0.5) / self.ncov
            q = self.arm(t)
            tx, ty = self.trail(t)
            a = (q[0] + tx * 0.8, q[1] + ty * 0.8)
            L = self.cov * (0.75 + 0.25 * (1 - abs(t - 0.8) / 0.8))
            b = (a[0] + tx * L, a[1] + ty * L)
            polys.append(round_feather(a, b, 4.2 if big else 5.0, root=0.75))
        p.polys(polys, mc, group=g, bias=bias)
        g += 1
        path = [self.arm(k / 20 * 1.6) for k in range(21)]
        p.limb(path, self.arm_w[0], self.arm_w[1], ma, group=g, bias=bias - 0.05)
        return g + 1


# --------------------------------------------------------------------------
# Elegull, the frigate chick
# --------------------------------------------------------------------------

ELEGULL_COLORS = [
    ("ink", (16, 8, 24)),
    # dark, night-purple down coming in on the body and cap
    ("n0", (40, 32, 64)), ("n1", (72, 64, 104)), ("n2", (112, 104, 152)),
    # the white down of a frigate chick's head, and the bleached bone
    ("w0", (152, 152, 184)), ("w1", (208, 208, 224)), ("w2", (248, 248, 240)),
    # the loose throat pouch, pale pink, and the first ember glow inside it
    ("pk0", (200, 120, 144)), ("pk1", (240, 184, 192)),
    ("em1", (232, 96, 56)), ("em3", (248, 216, 128)),
    # Aegean tears, and the sheen on the first flight feathers
    ("ae1", (48, 104, 176)), ("ae2", (120, 176, 224)),
    # the gold tips of the stubby tail
    ("go0", (176, 112, 40)), ("go1", (232, 184, 72)),
]
# "The down turns soft sun-gold and the tear marks turn terracotta."
ELEGULL_SHINY = {
    "n0": (120, 72, 32), "n1": (184, 128, 56), "n2": (232, 184, 104),
    "ae1": (152, 64, 32), "ae2": (224, 136, 88),
}

e_down = Mat(["n0", "n1", "n2"], line="n0", cuts=[0.3, 0.64])
e_white = Mat(["w0", "w1", "w2"], line="w0", cuts=[0.4, 0.7])
e_beak = Mat(["n2", "w0", "w1"], line="n1", cuts=[0.34, 0.66])
e_pouch = Mat(["pk0", "pk1"], line="pk0", cuts=[0.5])
e_bone = Mat(["w0", "w1", "w2"], line="n2", cuts=[0.34, 0.66])
e_wing = Mat(["n0", "n1", "n2", "ae1"], line="n0", cuts=[0.2, 0.5, 0.82])
e_gold = Mat(["n1", "go0", "go1"], line="n0", cuts=[0.3, 0.64])
e_foot = Mat(["w0", "w1"], line="n1", cuts=[0.5])
e_shadow = Mat(["n0"], line="n0")


def _bone(p, x0, x1, y):
    """A bleached thighbone lying across the ground, knuckled at both ends."""
    p.limb([(x0 + 1, y), (x1 - 1, y - 0.6)], 2.8, 2.8, e_bone, group=41)
    for cx, cy, r in ((x0, y - 1.1, 1.9), (x0 - 0.2, y + 1.1, 1.7), (x1, y - 1.7, 1.9), (x1 + 0.5, y + 0.3, 1.7)):
        p.circle(cx, cy, r, e_bone, group=41)


def _elegull_body(p, L=0, peep=0, small=False):
    """The chick in three-quarter view facing left, perched; L lifts the
    head, peep opens the beak."""
    # stubby forked tail with the first curl of the lyre, gold-tipped
    p.limb(bez((39, 47), (44, 45), (46.5, 41.5)), 3.0, 2.0, e_gold, group=3)
    p.limb(bez((39.5, 49), (45, 49.5), (48, 46.5)), 3.0, 2.0, e_gold, group=4, bias=0.12)
    # downy body, pear-shaped and a little hunched
    p.poly(fuzz_pts(32, 44.5, 9.2, 8.2, n=10, jag=1.3, rot=0.25), e_down, group=1)
    # feet on the bone
    for x in (27.5, 33):
        p.limb([(x + 0.6, 51.5), (x, 54)], 2.6, 2.4, e_foot, group=42)
    # the awkward stubby wing, held a little away from the body
    p.poly(lens_pts((33.5, 38), (42, 49.5), 7.0, bend=-1.4, fat=0.38), e_wing, group=5)
    # the loose throat pouch under the beak
    p.drop((19.5, 34 - L), 21.5, 39.5 - L, 3.6, e_pouch, group=6)
    # big round head of white down; the dark cap is the adult's black coming in
    p.poly(fuzz_pts(26, 28.5 - L, 9.4, 8.6, n=11, jag=1.2, rot=0.15, skip=(5, 6)), e_white, group=7, bias=-0.1)
    p.poly([(26, 19.4 - L), (31.5, 20.4 - L), (35.4, 24.5 - L), (36, 30 - L), (34.5, 34.5 - L), (32, 30 - L),
            (29.5, 25 - L), (25, 22.5 - L)], e_down, group=8)
    # small hooked beak, open when it peeps
    g = 1.5 * peep
    p.poly([(19.5, 28.6 - L), (15, 28.8 - L), (11.6, 30 - L), (11.4, 32.6 - L), (12.8, 31.6 - L), (19.5, 31.6 - L)],
           e_beak, group=9)
    p.poly([(19, 31.6 - L), (13.5, 31.8 - L + g * 0.6), (14, 33 - L + g), (19, 33.2 - L)], e_beak, group=9, bias=0.2)


def elegull(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        peep = 1 if (phase == 1 and view != "side") else 0
        p.blob(32, 58.5, 15, 2.2, e_shadow, group=40, flat=0)
        _bone(p, 19, 46, 55.5)
        _elegull_body(p, L, peep)
        if p.big:
            # big wet eyes with an ember glint, and Aegean tears
            p.patch(19, 25 - L, [".11.", "1121", "1111", "1e11", ".11."], {"1": "ink", "2": "w2", "e": "em1"})
            p.patch(20, 30 - L, ["a", "a", "b"], {"a": "ae1", "b": "ae2"})
            p.pxs([(16, 26 - L), (16, 27 - L), (16, 28 - L)], "ink")
            p.stroke([(13, 31.5 - L), (19, 31.5 - L)], "n1")
            # the faint ember glow in the pouch
            p.pxs([(21, 38 - L), (22, 39 - L)], "em1")
            p.px(21, 39 - L, "em3" if phase else "em1")
        else:
            p.px(20.5, 27 - L, "ink")
        return

    if view == "back":
        # over the shoulder at 1.2x: the downy back, the stubby wing, the
        # head turned right in profile with the pouch hanging under the beak
        p.limb(bez((40, 56), (50, 56), (55, 51)), 4.2, 2.6, e_gold, group=3)
        p.poly(fuzz_pts(31, 59, 23, 17, n=14, jag=1.8, rot=0.1), e_down, group=1)
        p.poly(lens_pts((21, 44), (6, 62), 10, bend=1.8, fat=0.38), e_wing, group=5)
        p.drop((50, 37), 49, 43.5, 4.8, e_pouch, group=6)
        p.poly(fuzz_pts(39, 30, 12.5, 11.5, n=11, jag=1.5, rot=0.2, skip=(0, 10)), e_white, group=7)
        p.poly([(28, 23), (32, 19), (39, 18.4), (36, 24), (34, 31), (31, 40), (27.5, 36)], e_down, group=8)
        p.poly([(48, 31), (54, 31.2), (58.6, 32.8), (58.8, 36), (57, 34.8), (48, 34.8)], e_beak, group=9)
        p.poly([(48, 34.8), (55.5, 35), (55, 36.8), (48, 37)], e_beak, group=9, bias=0.2)
        if p.big:
            p.patch(44, 26, [".11.", "1211", "1111", "11e1", ".11."], {"1": "ink", "2": "w2", "e": "em1"})
        return

    if view in ("down", "up"):
        step = phase
        face = view == "down"
        for x, s in ((28, step), (36, 1 - step)):
            p.limb([(x, 52), (x, 58 - s)], 2.8, 2.6, e_foot, group=42)
        if not face:
            p.limb(bez((31, 50), (28, 54), (25, 53)), 3.0, 2.0, e_gold, group=3)
            p.limb(bez((33, 50), (36, 54), (39, 53)), 3.0, 2.0, e_gold, group=3)
        p.poly(fuzz_pts(32, 46, 9.5, 8, n=10, jag=1.3, rot=0.3), e_down, group=1)
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            p.poly(lens_pts((X(25), 41), (X(19), 51 - (step if sx < 0 else 1 - step)), 6, bend=sx * 1.2, fat=0.4),
                   e_wing, group=5)
        if face:
            p.drop((32, 37), 32, 42, 3.4, e_pouch, group=6)
        p.poly(fuzz_pts(32, 30, 10, 9, n=11, jag=1.2, rot=0.2), e_white if face else e_down, group=7)
        if face:
            p.poly([(27, 21.5), (32, 20), (37, 21.5), (34, 24), (30, 24)], e_down, group=8)
            p.poly([(30, 31), (34, 31), (33, 35.5), (32, 36.5), (31, 35.5)], e_beak, group=9)
            p.eye(26, 27, 3, 4, shine="w2")
            p.eye(35, 27, 3, 4, shine="w2")
            if p.big:
                p.pxs([(27, 31), (27, 32), (36, 31), (36, 32)], "ae1")
                p.px(32, 40, "em1")
        else:
            p.poly([(26, 23), (32, 21), (38, 23), (36, 29), (28, 29)], e_down, group=8)
        return


# --------------------------------------------------------------------------
# Seirenade, the False Beacon
# --------------------------------------------------------------------------

SEIRENADE_COLORS = [
    ("ink", (16, 8, 24)),
    # night-black plumage: deep violet-black through a lilac rim light
    ("n0", (40, 32, 64)), ("n1", (64, 56, 96)), ("n2", (96, 88, 136)), ("n3", (144, 136, 184)),
    # the ghostly iridescent sheen on the black feathers
    ("sh0", (48, 112, 152)), ("sh1", (120, 200, 216)),
    # the beacon: crimson through ember to a white-hot core
    ("em0", (136, 24, 48)), ("em1", (216, 72, 48)), ("em2", (248, 144, 64)), ("em3", (248, 216, 120)),
    ("hot", (248, 248, 216)),
    # the gilded lyre arms
    ("go0", (136, 80, 32)), ("go1", (216, 160, 56)),
    # the pale hooked beak
    ("bk", (192, 192, 208)),
]
# "The plumage turns deep cypress green and the lyre turns silver."
SEIRENADE_SHINY = {
    "n0": (16, 40, 32), "n1": (32, 64, 48), "n2": (56, 96, 72), "n3": (104, 144, 112),
    "go0": (104, 104, 120), "go1": (184, 184, 200),
}

s_plume = Mat(["n0", "n1", "n2", "n3"], line="n0", cuts=[0.2, 0.48, 0.78])
s_prim = Mat(["n0", "n1", "sh0"], line="ink", cuts=[0.44, 0.8])
s_sec = Mat(["n0", "n1", "n2"], line="n0", cuts=[0.34, 0.7])
s_cov = Mat(["n1", "n2", "n3"], line="n0", cuts=[0.3, 0.64])
s_arm = Mat(["n2", "n3", "sh1"], line="n1", cuts=[0.4, 0.8])
s_beak = Mat(["n2", "n3", "bk"], line="n1", cuts=[0.3, 0.64])
s_mask = Mat(["n2", "n3", "bk"], line="n1", cuts=[0.36, 0.7])
s_pouch = Mat(["em0", "em1", "em2", "em3"], line="em0", outline="em0", cuts=[0.24, 0.5, 0.74])
s_gold = Mat(["go0", "go1", "em3"], line="go0", cuts=[0.36, 0.72])
s_tail = Mat(["n0", "n1", "n2"], line="ink", cuts=[0.36, 0.7])
S_WING = (s_prim, s_sec, s_cov, s_arm)
S_FAR = (Mat(["n0", "n1"], line="ink", cuts=[0.6]), Mat(["n0", "n1"], line="n0", cuts=[0.55]),
         Mat(["n0", "n1", "n2"], line="n0", cuts=[0.4, 0.75]), Mat(["n1", "n2", "n3"], line="n0", cuts=[0.4, 0.75]))

class Wing:
    """A frigatebird wing laid out feather by feather: a narrow blade bent
    sharply at the wrist, its arm rising from the shoulder and its long hand
    sweeping back to one sharp tip, so the pair reads as the frigatebird's
    angular M. Four value masses run along the blade: the lit leading edge,
    the coverts, the secondaries hanging from the arm and the dark primaries
    sweeping to the tip.

    lead: the leading edge from the shoulder over the wrist toward the tip.
    prim: (base, tip, width) primaries, innermost first. sec: (base, tip,
    width) secondaries from the wrist back to the body. cov: (base, tip,
    width) covert tongues."""

    def __init__(self, lead, prim, sec, cov, lw=(2.8, 1.8)):
        self.lead, self.prim, self.sec, self.cov, self.lw = lead, prim, sec, cov, lw

    def moved(self, c, rot=0.0, tip=0.0, wrist=None, dx=0.0, dy=0.0):
        """A copy rotated by rot about c (a wingbeat); tip also swings the
        hand (everything beyond the wrist) about the wrist."""
        def M(q, far=False):
            if tip and far and wrist is not None:
                q = _rot(q, wrist, tip)
            q = _rot(q, c, rot)
            return (q[0] + dx, q[1] + dy)

        def hand(q):
            return wrist is not None and math.hypot(q[0] - wrist[0], q[1] - wrist[1]) > 4 and \
                (q[0] - wrist[0]) * (self.lead[-1][0] - wrist[0]) + (q[1] - wrist[1]) * (self.lead[-1][1] - wrist[1]) > 0

        lead = [M(q, hand(q)) for q in self.lead]
        prim = [(M(a, hand(a)), M(b, True), w) for a, b, w in self.prim]
        sec = [(M(a), M(b), w) for a, b, w in self.sec]
        cov = [(M(a, hand(a)), M(b, hand(a)), w) for a, b, w in self.cov]
        return Wing(lead, prim, sec, cov, self.lw)

    def draw(self, p, mats, g0, bias=0.0):
        mp, ms, mc, ma = mats
        g = g0
        k = 1.0 if p.big else 1.35
        for a, b, w in self.sec:
            p.poly(round_feather(a, b, w * k, root=0.72), ms, group=g, bias=bias)
        g += 1
        for i, (a, b, w) in enumerate(self.prim):
            if not p.big and i % 2:
                continue
            flat_feather(p, lens_pts(a, b, w * k, 0.0, fat=0.28), a, b, mp, 1, 0, group=g, bias=bias)
            g += 1
        p.polys([round_feather(a, b, w * k, root=0.8) for a, b, w in self.cov], mc, group=g, bias=bias)
        g += 1
        p.limb(self.lead, self.lw[0] * k, self.lw[1] * k, ma, group=g, flat=1)
        return g + 1


# the lyre tail: the two streamers of the forked tail run back from the rump,
# bow apart and curl back in, and their tips are joined by a curved yoke
LYRE_A = [(42.5, 42), (46.6, 41.4), (50.6, 42.6), (54.6, 45.4), (58.2, 49.7)]
LYRE_B = [(42.6, 44.6), (43.2, 49.4), (45.8, 53.4), (49.4, 55.8), (52.4, 56.7)]
LYRE_YOKE = ((58.2, 49.7), (59.1, 56.4), (52.4, 56.7))
LYRE_CURL = [((58.2, 49.7), (60.8, 48.8)), ((52.4, 56.7), (52.6, 59.4))]
LYRE_ROOT = (45.4, 45.6)


def _catmull(pts, n=6):
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    out.append(pts[-1])
    return out


def _lyre(p, sh=0):
    """The forked tail as a lyre: dark streamers at the rump, gilded where
    they bow into the arms, the curled tips joined by a curved yoke."""
    A = _catmull(LYRE_A)
    B = _catmull(LYRE_B)
    k = len(A) // 3
    p.limb(A[:k + 2], 4.2, 3.0, s_tail, group=60)
    p.limb(B[:k + 2], 4.2, 3.0, s_tail, group=62, bias=0.12)
    p.limb(A[k:], 3.0, 2.2, s_gold, group=61)
    p.limb(B[k:], 3.0, 2.2, s_gold, group=63, bias=0.12)
    p.limb(bez(*LYRE_YOKE), 2.4, 2.4, s_gold, group=64)
    for a, b in LYRE_CURL:
        p.taper([a, b], 2.4, s_gold, group=64)
    if p.big:
        # three strings of ember light from the yoke back to the rump
        yk = bez(*LYRE_YOKE, n=20)
        for t, d in ((0.28, (1.2, -1.0)), (0.5, (0.0, 0.0)), (0.72, (-1.0, 1.2))):
            q = yk[int(t * 20)]
            p.stroke([(q[0] - 0.8, q[1] - 0.8), (LYRE_ROOT[0] + d[0], LYRE_ROOT[1] + d[1])], "em1")


def _sei_head(p, hx=18, hy=22, gape=0.0):
    """Head in three-quarter view facing left: a pale ghost mask round the
    eye, and the long frigatebird beak with its hooked tip."""
    p.blob(hx, hy, 7.0, 6.2, s_plume, group=42)
    p.poly([(hx - 5, hy - 2), (hx - 1, hy - 4.4), (hx + 3.4, hy - 3.4), (hx + 4.4, hy + 0.4), (hx + 2.2, hy + 3.8),
            (hx - 2.6, hy + 3.6), (hx - 5.2, hy + 1)], s_mask, group=43)
    # upper mandible: long and straight, then a sharp downward hook
    bx, by = hx - 4, hy
    p.poly([(bx + 0.5, by - 3), (bx - 5, by - 2.2), (bx - 10, by - 1.4), (bx - 13, by - 0.4), (bx - 14.4, by + 1.6),
            (bx - 14.2, by + 4.2), (bx - 12.8, by + 4.4), (bx - 12, by + 2.6), (bx - 7, by + 1.8), (bx + 0.5, by + 1.6)],
           s_beak, group=45)
    # lower mandible, dropped open in song
    p.poly([(bx + 0.5, by + 1.6), (bx - 6, by + 2.4 + gape * 0.5), (bx - 11, by + 3.2 + gape),
            (bx - 10.6, by + 4.8 + gape), (bx - 5, by + 4.6 + gape * 0.5), (bx + 1.5, by + 4.4)], s_beak, group=44,
           bias=0.25)


# facing left in three-quarter view: the near wing rises on the right, in
# front of the body; the far wing rises on the left behind the head. Both
# are raised, wrists high and hands swept back, so the pair reads as the
# frigatebird's angular M. The followers still use FrigateWing.
SEI_NEAR = Wing(
    lead=[(39, 31), (40.2, 21), (42.8, 11.5), (45.8, 4.6), (48.4, 3), (52.6, 5.4), (57, 9.6), (60.4, 14.8), (61.4, 20.5)],
    prim=[((47.6, 13), (52.6, 17.6), 3.8), ((48.2, 11), (55, 18.6), 4.0), ((48.8, 9), (57.6, 19.8), 4.2),
          ((49.6, 7), (60, 21), 4.2), ((50.6, 5.6), (61.6, 22.2), 4.0)],
    sec=[((45.6, 9), (52, 18), 5.4), ((44.6, 13.6), (51.6, 23), 5.6), ((43.2, 18.4), (50.6, 28), 5.6),
         ((41.8, 23), (48.2, 32.4), 5.6), ((40.4, 27), (44.4, 35.6), 5.4)],
    cov=[((41.6, 28), (45.4, 29.2), 4.2), ((42.4, 23.6), (46.4, 24.6), 4.4), ((43.4, 19), (47.6, 19.8), 4.4),
         ((44.6, 14.4), (48.6, 15), 4.4), ((46.2, 9.6), (50, 10.6), 4.2), ((48.6, 6), (51.4, 8.8), 4.0),
         ((52, 7.6), (53.8, 10.8), 3.6)],
    lw=(3.0, 1.8))
SEI_FAR = Wing(
    lead=[(31.5, 28), (29, 17.5), (26.4, 8), (24.6, 3.6), (22, 3), (16, 5.8), (9.4, 9.6), (2.6, 13.6)],
    prim=[((22.2, 11), (13.6, 14.2), 3.4), ((21.6, 9), (9.6, 14.8), 3.6), ((21, 7), (5.8, 15), 3.6),
          ((20, 5.4), (2.4, 14.4), 3.4)],
    sec=[((24.4, 7.4), (17.6, 14.2), 4.8), ((25.6, 12), (19.6, 19.6), 4.8), ((27, 17), (21.6, 24.4), 4.8),
         ((28.6, 22), (24.2, 29), 4.6)],
    cov=[((28.4, 24), (25.2, 25), 3.8), ((27.6, 19.4), (24.2, 20.2), 4.0), ((26.6, 14.6), (23, 15.2), 4.0),
         ((25.4, 9.8), (21.8, 10.6), 3.8), ((22, 5.6), (19.2, 8.6), 3.6), ((18.2, 6.6), (16.6, 9.4), 3.4)],
    lw=(2.6, 1.6))

def seirenade(p, view, phase):
    if view in ("front", "side", "icon"):
        ph = phase if view == "front" else 0
        beat = 3 * ph
        SEI_FAR.moved((31.5, 28), rot=beat).draw(p, S_FAR, 10, bias=0.1)
        _lyre(p, ph)
        # body: a slim, keeled frigatebird body on a diagonal
        p.blob(35, 37, 10, 6.2, s_plume, ang=30, group=1)
        p.blob(29, 32, 6, 6, s_plume, group=1)
        p.limb([(29, 31), (20, 22)], 8.4, 7.0, s_plume, group=1)
        SEI_NEAR.moved((39, 31), rot=-beat).draw(p, S_WING, 20)
        # the beacon: the inflated throat sac hanging from the lower jaw
        p.poly([(19, 25.5), (12, 26), (8, 28.5), (6.5, 33), (7.5, 38), (11, 41.5), (16, 42.5), (21, 41),
                (24, 37.5), (24.5, 33), (22, 28.5)], s_pouch, group=50)
        _sei_head(p, 19.5, 21, gape=1.2 + 0.8 * ph)
        if p.big:
            # ghost-lit eye inside the mask
            p.patch(17, 19, [".11.", "1hs1", "1ss1", ".11."], {"1": "ink", "h": "hot", "s": "sh1"})
            # hot core of the beacon
            p.patch(10, 31, ["..33", ".3hh3", ".3hh3", "..33"], {"3": "em3", "h": "hot"})
        else:
            p.px(17.5, 20, "sh1")
        return

    if view == "back":
        # over the shoulder: the front's wings mirrored and spread high, the
        # broad black back and the lyre tail below, the head turned right in
        # profile with the beacon glowing under its beak
        def mirror(w, dx=0.0, dy=0.0):
            M = lambda q: (64 - q[0] + dx, q[1] + dy)
            return Wing([M(q) for q in w.lead], [(M(a), M(b), wd) for a, b, wd in w.prim],
                        [(M(a), M(b), wd) for a, b, wd in w.sec], [(M(a), M(b), wd) for a, b, wd in w.cov], w.lw)
        mirror(SEI_FAR, -0.5, 5).draw(p, S_FAR, 10, bias=0.1)
        p.limb(_catmull([(26, 50), (17, 52), (11, 56), (7, 60), (6, 63)]), 4.6, 3.0, s_tail, group=60)
        p.limb(_catmull([(28, 54), (22, 58), (19, 63)]), 4.6, 3.6, s_tail, group=62, bias=0.12)
        p.limb([(9, 58), (5, 60), (4, 63.5)], 3.0, 3.0, s_gold, group=61)
        p.limb(bez((4.5, 61), (8, 57), (13, 58)), 2.4, 2.4, s_gold, group=64)
        p.blob(36, 60, 19, 12, s_plume, group=1)
        p.blob(38, 46, 10, 9, s_plume, group=1)
        mirror(SEI_NEAR, 1.5, 6).draw(p, S_WING, 20)
        p.limb([(40, 44), (43, 35), (45, 29)], 10, 8.6, s_plume, group=2)
        p.poly([(43, 30.5), (50, 30.5), (55, 32.5), (56, 37), (53, 41.5), (47.5, 42.5), (44, 39)], s_pouch, group=50)
        p.blob(45, 24, 7.4, 6.6, s_plume, group=3)
        p.poly([(43.5, 21), (48, 19.4), (52, 21), (52.6, 25), (49, 28), (45, 27.4)], s_mask, group=4)
        p.poly([(50.5, 21.4), (56, 22), (60.6, 23.2), (62.4, 25.4), (62.2, 28), (60.8, 28.2), (60.2, 25.8), (55, 25.4),
                (50.5, 25.2)], s_beak, group=6)
        p.poly([(50.5, 25.2), (55, 26), (59.4, 27.2), (59, 28.6), (54, 28.4), (50.5, 28)], s_beak, group=5, bias=0.25)
        if p.big:
            p.patch(47, 21, [".11.", "1sh1", "1ss1", ".11."], {"1": "ink", "h": "hot", "s": "sh1"})
            p.patch(47, 34, [".33.", "3hh3", ".33."], {"3": "em3", "h": "hot"})
        return

    if view in ("down", "up"):
        # follower: soaring toward or away from the camera on spread wings
        beat = 6 * phase
        face = view == "down"
        if not face:
            p.limb(bez((31, 44), (25, 52), (27, 58)), 3.0, 2.0, s_gold, group=60)
            p.limb(bez((33, 44), (39, 52), (37, 58)), 3.0, 2.0, s_gold, group=61)
            p.limb(bez((27, 58), (32, 60), (37, 58)), 2.2, 2.2, s_gold, group=62)
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            w = FrigateWing((X(28), 33), (X(22), 22), (X(16), 18), (X(10), 21),
                            [(X(1.5), 26), (X(3.5), 28), (X(6), 29.5), (X(8.5), 30.5)],
                            [(X(11), 33), (X(15), 35), (X(19.5), 37), (X(24), 38)],
                            pw=3.8, sw=4.6, cov=4.4, ncov=4, arm=(4.0, 2.4))
            w.moved(rot=-sx * beat, about=(X(28), 33)).draw(p, S_WING if face else S_FAR, 10 if sx < 0 else 20)
        p.blob(32, 38, 6, 9, s_plume, group=1)
        if face:
            p.blob(32, 33, 5.6, 5.4, s_pouch, group=50)
        p.blob(32, 24, 5.4, 5.2, s_plume, group=3)
        if face:
            p.poly([(28, 22), (36, 22), (35, 26), (29, 26)], s_mask, group=4)
            p.poly([(30.5, 25), (33.5, 25), (33, 30), (32, 31.5), (31, 30)], s_beak, group=5)
            p.px(29.5, 23.5, "sh1")
            p.px(34.5, 23.5, "sh1")
            if p.big:
                p.pxs([(31, 34), (32, 34), (31, 33)], "hot")
        return


MONS = [
    # icon palette 2 keeps the night-purple plumage and the warm pouch
    Mon("Elegull", ELEGULL_COLORS, ELEGULL_SHINY, elegull, foot="bird", icon_pal=2),
    Mon("Seirenade", SEIRENADE_COLORS, SEIRENADE_SHINY, seirenade, foot="bird", icon_pal=2),
]
