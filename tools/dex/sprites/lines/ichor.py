"""Ichor line: Ichorin (#152, Psychic, the First Myth). The title mythical.

The Marble Child: a tiny archaic statue that has stepped off its plinth
into the air. Parian marble with the archaic smile, a beaded gold fillet,
Hypnos's little wings at its temples and a sun-disc halo with a meander
rim. One vein of ichor, the gods' golden blood, runs from its heart down
its tail to Talos's bronze nail, set in the eye of an Ionic volute where
the tail scrolls shut. Gold light leaks through hairline cracks in the
stone, and motes of it orbit the child.
"""
import math

from mon_lib import Mat, Mon, bez, bez3
from sprites_lib import bresenham

INK = (32, 24, 24)

ICHORIN_COLORS = [
    ("ink", INK),
    # Parian marble: cool lavender shadows, warm light
    ("m0", (96, 88, 144)), ("m1", (160, 152, 200)), ("m2", (216, 208, 224)),
    ("m3", (248, 240, 224)), ("m4", (248, 248, 248)),
    # light coming through the stone
    ("warm", (240, 200, 168)),
    # ichor, the signature glow: amber to white-hot
    ("g0", (160, 88, 24)), ("g1", (232, 160, 32)), ("g2", (248, 216, 72)), ("g3", (248, 248, 176)),
    # Talos's bronze nail
    ("b0", (88, 48, 32)), ("b1", (168, 104, 48)),
    # the Psychic shimmer on its edge, and the soft aura it gives off
    ("psy", (232, 128, 176)), ("aura", (232, 200, 240)),
]
# The gold turns quicksilver white with pale Aegean-blue shading.
ICHORIN_SHINY = {
    "g0": (72, 112, 168), "g1": (152, 192, 232), "g2": (216, 232, 248), "g3": (248, 248, 248),
    "warm": (208, 224, 240),
}

marble = Mat(["m0", "m1", "m2", "m3", "m4"], line="m0", cuts=[0.1, 0.36, 0.62, 0.88])
stone = Mat(["m0", "m1", "m2", "m3"], line="m0", cuts=[0.3, 0.6, 0.84])
feather = Mat(["m1", "m2", "m3", "m4"], line="m0", cuts=[0.3, 0.55, 0.78])
# the drawn wing: mostly white stone, its shadow only along the trailing edge
plume = Mat(["m1", "m2", "m3", "m4"], line="m0", cuts=[0.12, 0.42, 0.7])
bronze = Mat(["b0", "b1", "g1"], line="b0", cuts=[0.45, 0.8])

MARBLE = {"m0", "m1", "m2", "m3", "m4", "warm"}


# --------------------------------------------------------------------------
# After-render effects. The parts renderer draws the child; light, halo,
# vein and motes are painted onto the rendered grid, the halo and motes only
# into clear pixels so the child's ink outline stays whole.
# --------------------------------------------------------------------------

class _Grid:
    def __init__(self, arr, pal, p):
        self.a, self.pal, self.p = arr, pal, p
        self.h, self.w = arr.shape

    def name(self, X, Y):
        if 0 <= X < self.w and 0 <= Y < self.h:
            return self.pal.names[self.a[Y, X]]
        return None

    def put(self, X, Y, c):
        if 0 <= X < self.w and 0 <= Y < self.h:
            self.a[Y, X] = 0 if c == "_" else self.pal[c]

    def clear(self, X, Y):
        return 0 <= X < self.w and 0 <= Y < self.h and self.a[Y, X] == 0

    def under(self, X, Y, c):
        if self.clear(X, Y):
            self.put(X, Y, c)

    def c(self, x, y):
        """design -> canvas pixel"""
        return self.p.ipt(x, y)

    def path(self, pts):
        ip = [self.c(x, y) for x, y in pts]
        out = []
        for (x0, y0), (x1, y1) in zip(ip, ip[1:] or ip):
            for q in bresenham(x0, y0, x1, y1):
                if not out or out[-1] != q:
                    out.append(q)
        return out


def _after(p, fn):
    fig = p.fig
    orig = fig.render

    def render():
        arr = orig()
        fn(_Grid(arr, fig.pal, p))
        return arr
    fig.render = render


def _halo(g, cx, cy, R, big=True):
    """The sun disc behind the head: a ring of light, white-hot inside and
    amber outside, with a pale glow inside it. Painted only into clear
    pixels. The meander on its band is hand-painted in the art files."""
    s = g.p.s
    X0, Y0 = g.p.pt(cx, cy)
    Rc = R * s
    rows = ("g3", "g2", "g1", "g0") if big else ("g2", "g1")
    n = len(rows)
    ss = 4
    for Y in range(g.h):
        for X in range(g.w):
            votes = [0] * n
            for sy in range(ss):
                for sx in range(ss):
                    r = math.hypot(X + (sx + 0.5) / ss - X0, Y + (sy + 0.5) / ss - Y0)
                    v = r - (Rc - n / 2)
                    if 0 <= v < n:
                        votes[int(v)] += 1
            if sum(votes) * 2 >= ss * ss:
                g.under(X, Y, rows[max(range(n), key=lambda i: votes[i])])
            elif big:
                v = math.hypot(X + 0.5 - X0, Y + 0.5 - Y0) - (Rc - n / 2)
                if -1.2 <= v < -0.2 and (X + Y) % 2 == 0:
                    g.under(X, Y, "g3")


def _glow_line(g, pts, core="g2", only=MARBLE):
    """The vein: a gold line through the stone, its pixels painted only over
    marble so it never crosses the outline."""
    for X, Y in g.path(pts):
        if g.name(X, Y) in only:
            g.put(X, Y, core)


def _mote(g, x, y, kind, c="g2"):
    X, Y = g.c(x, y)
    if kind == 0:
        g.under(X, Y, c)
    elif kind == 1:
        g.under(X, Y, "g3")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            g.under(X + dx, Y + dy, c)
    else:
        g.under(X, Y, "g3")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            g.under(X + dx, Y + dy, "g2")
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            g.under(X + dx, Y + dy, "g1")


def _spiral(cx, cy, r0, r1, a0, a1, n=28):
    out = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(a0 + (a1 - a0) * t)
        r = r0 + (r1 - r0) * t
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


# --------------------------------------------------------------------------
# Ichorin
# --------------------------------------------------------------------------

def _wing(p, base, tips, w, group, bias=0.0, mat=feather, bend=0.6):
    """Hypnos's temple wing: feathers fanning from one root, the first
    tip the top one. Later feathers sit in front."""
    for i, (tip, ww) in enumerate(zip(tips, w)):
        p.lens(base, tip, ww, mat, bend=bend, fat=0.62, group=group + i, bias=bias - 0.03 * i)


def _rim(g, box=None, colors=("m0", "m1"), to="warm", side=(1, -1)):
    """Backlight from the halo: dark marble right inside the outline on the
    side facing the light takes a warm rim."""
    pts = []
    for Y in range(g.h):
        for X in range(g.w):
            if g.name(X, Y) not in colors:
                continue
            if box and not (box[0] <= X <= box[2] and box[1] <= Y <= box[3]):
                continue
            if g.name(X + side[0], Y) == "ink" or g.name(X, Y + side[1]) == "ink":
                pts.append((X, Y))
    for X, Y in pts:
        g.put(X, Y, to)


def _spill(g, src=("g1", "g2", "g3"), colors=("m1", "m2"), to="warm"):
    """Ichor light spilling into the stone beside the vein."""
    pts = []
    for Y in range(g.h):
        for X in range(g.w):
            if g.name(X, Y) in colors and any(g.name(X + dx, Y + dy) in src
                                              for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                pts.append((X, Y))
    for X, Y in pts:
        g.put(X, Y, to)


def _stamp(g, x, y, rows, legend):
    X0, Y0 = g.c(x, y)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch not in ". ":
                g.put(X0 + i, Y0 + j, legend[ch])


LEG = {"1": "ink", "w": "m4", "W": "m3", "l": "m2", "m": "m1", "d": "m0", "o": "g0", "g": "g1", "G": "g2",
       "H": "g3", "b": "b0", "B": "b1", "r": "warm", "p": "psy"}


def ichorin(p, view, phase):
    big = p.big
    if view in ("front", "icon", "side"):
        ph = phase if view == "front" else 0
        L = ph  # frame 2 floats a pixel higher
        # ---- tail: out of the small of the back, sweeping low and right,
        # then up and rolled shut like an Ionic volute
        curl = 18 * ph
        sp = _spiral(50, 44 - L, 8.6, 2.0, 105, -290 - curl, n=40)
        tail = bez3((33.5, 42.5 - L), (39.5, 44 - L), (42, 52.5 - L), sp[0], n=12) + sp[1:]
        n = len(tail)
        cut = int(n * 0.5)
        p.limb(tail[:cut], 6.0, 4.6, stone, group=20, bias=-0.06)
        p.limb(tail[cut - 1:], 4.6, 3.6, stone, group=21, bias=-0.1)
        nx, ny = tail[-1]
        p.circle(nx, ny, 2.4, bronze, group=22)

        # ---- far leg, stepping forward, toe pointed: a kouros off its plinth
        p.limb(bez((23.5, 44 - L), (20.2, 47.5 - L), (19.6, 52 - L)), 6.4, 3.4, marble, group=10, bias=0.16)
        p.taper([(19.6, 51.5 - L), (17, 56 - L)], 3.4, marble, group=10, bias=0.16)
        # ---- far arm, held close
        p.limb([(21, 33.5 - L), (19.4, 37 - L), (19.2, 40 - L)], 3.6, 3.2, marble, group=11, bias=0.16)
        p.circle(19.4, 40.6 - L, 2.0, marble, group=11, bias=0.16)

        # ---- body: a small kouros torso, chest round like a child's
        p.blob(27, 38 - L, 6.6, 6.6, marble, ang=-8, group=1, bias=-0.05)
        p.blob(28, 43 - L, 5.2, 3.4, marble, group=1, bias=-0.05)

        # ---- near leg, back, toe trailing
        p.limb(bez((30.5, 44 - L), (33, 48 - L), (33.6, 52 - L)), 6.4, 3.4, marble, group=12, bias=-0.04)
        p.taper([(33.6, 51.5 - L), (35.5, 56 - L)], 3.4, marble, group=12, bias=-0.04)

        # ---- back hair: beaded archaic tresses falling to the shoulder
        for i, (a, b) in enumerate((((40.5, 17), (41.5, 29)), ((37.5, 18), (38, 31)))):
            if not big and i == 0:
                continue  # at icon size one strand is enough
            p.limb([(a[0], a[1] - L), (b[0], b[1] - L)], 3.6, 3.2, stone, group=30 + i,
                   bias=(0.02 - 0.05 * i) if big else -0.2)

        # ---- head: big and round, the face toward us
        p.blob(25.5, 21.5 - L, 10.8, 10.4, marble, group=3, bias=-0.08)
        p.blob(22, 25 - L, 7.4, 6.8, marble, group=3, bias=-0.08)

        # ---- near arm, held close, fist at the hip
        p.limb([(32.5, 33.5 - L), (33.8, 37.5 - L), (33.6, 40.5 - L)], 4.0, 3.4, marble, group=13)
        p.circle(33.4, 41 - L, 2.2, marble, group=13)

        # ---- near temple wing: Hypnos's, swept back over the halo as one
        # broad feathered blade, gold-dipped at the tips
        p.lens((33, 16.5), (51.5, 6), 11.5, plume, bend=2.2, fat=0.38, group=44, bias=-0.12)
        if big:
            p.lens((34, 15.5), (51, 12.5), 5.0, plume, bend=-0.8, group=45, bias=0.0)

        if not big:
            # at icon and follower size the face is two dark almond marks
            p.eye(24, 19.5 - L, 4, 6, pupil="ink", shine=None)
            p.eye(17, 20 - L, 2, 5, pupil="ink", shine=None)

        def fx(g):
            # the icon wears a smaller sun so the child itself reads larger
            _halo(g, 27, 22 - L, 18 if view != "icon" else 14, big=big)
            for wx, wy in ((50.5, 6.2), (49.5, 6.8), (50, 12.4), (49, 12.8)):
                X, Y = g.c(wx, wy)
                if g.name(X, Y) in MARBLE:
                    g.put(X, Y, "g1")
            if not big:
                _glow_line(g, [(26, 35 - L), (30, 42 - L)] + tail[2:-2], core="g1")
                hx, hy = g.c(26, 35 - L)
                g.put(hx, hy, "g2")
                return
            # the vein: heart, belly, tail, nail
            vein = [(25, 35 - L), (28, 39 - L), (31, 42.5 - L)] + tail[1:-3]
            _glow_line(g, vein, core="g1")
            for k, (X, Y) in enumerate(g.path(vein)):
                if g.name(X, Y) == "g1" and (k + 2 * ph) % 5 == 0:
                    g.put(X, Y, "g3" if ph else "g2")
            _spill(g)
            _rim(g)
            # fillet: a beaded band across the brow and round the head
            band = [(15, 18), (18, 16.4), (22, 15.4), (26, 15), (30, 15.6), (33.5, 17)]
            for k, (X, Y) in enumerate(g.path([(x, y - L) for x, y in band])):
                if g.name(X, Y) in MARBLE:
                    g.put(X, Y, "g2" if k % 2 == 0 else "g1")
                if g.name(X, Y + 1) in MARBLE:
                    g.put(X, Y + 1, "g0")
            # face: almond eyes with ichor-gold irises
            _stamp(g, 23.5, 19 - L, [".111.", "1w111", "11111", "1ggg1", "1GgG1", ".1g1."], LEG)
            _stamp(g, 16.5, 19.5 - L, [".11", "1w1", "111", "1g1", "1G1", ".1."], LEG)
            _stamp(g, 19, 28 - L, ["d..d", ".dd."], LEG)
            # heart
            _stamp(g, 24, 34 - L, [".o.o.", "oGgGo", ".gHg.", "..g.."], LEG)
            # motes, orbiting
            ang = 30 * ph
            for k, (r, a0, kind) in enumerate(((23, 200, 1), (25, 250, 0), (22, 160, 2), (26, 320, 0),
                                               (21, 120, 0), (27, 20, 1))):
                a = math.radians(a0 + ang)
                _mote(g, 28 + r * math.cos(a), 32 + 0.8 * r * math.sin(a), kind)
            # a drop of ichor hanging from the nail
            dx_, dy_ = g.c(nx, ny + 2.8)
            g.under(dx_, dy_, "g2")
            if ph:
                g.under(dx_, dy_ + 1, "g1")
        _after(p, fx)
        return

    if view == "back":
        # over the shoulder: head turned right in profile, halo behind, the
        # vein glowing down the spine; the tail rises from below the frame,
        # in front of the small of the back, and scrolls shut by the flank
        # far wing, tips over the crown
        _wing(p, (37, 15), [(30, 3.5), (25, 5)], [4.0, 4.2], group=40, bias=0.3, bend=-0.3)
        # shoulders and back, cropped by the frame
        p.blob(27, 55, 22, 15, marble, ang=-4, group=1, bias=-0.06)
        p.limb([(33, 44), (36, 38)], 12, 11, marble, group=1, bias=-0.06)
        # near arm hanging close
        p.limb([(9.5, 47), (7.5, 55), (7, 64)], 8.4, 7.4, marble, group=10, bias=0.02)
        # beaded tresses down the nape
        for i, (a, b) in enumerate((((28, 23), (24.5, 41)), ((31.5, 25), (29.5, 43)), ((35, 27), (34.5, 42)))):
            p.limb([a, b], 4.4, 3.8, stone, group=30 + i, bias=0.04 - 0.04 * i)
        # head in profile, facing right
        p.blob(38, 24, 12.6, 12.2, marble, group=3, bias=-0.1)
        p.blob(44, 29.5, 7.2, 6.6, marble, group=3, bias=-0.1)
        # near temple wing, swept back over the crown
        _wing(p, (40, 18), [(28.5, 3), (24, 7.5), (23, 13), (26, 17.5)], [4.6, 5.0, 4.6, 3.8], group=44, bend=0.6)
        p.blob(40, 18, 3.0, 2.8, feather, group=49)
        # tail: up from below the frame into its volute
        sp = _spiral(53, 51, 8.6, 2.2, 120, -285, n=44)
        tail = bez3((37, 67), (39, 61), (44, 59.5), sp[0], n=10) + sp[1:]
        cut = len(tail) * 2 // 5
        p.limb(tail[:cut], 6.0, 5.0, stone, group=60, bias=-0.05)
        p.limb(tail[cut - 1:], 5.0, 3.6, stone, group=61, bias=-0.1)
        nx, ny = tail[-1]
        p.circle(nx, ny, 2.6, bronze, group=62)

        def fx(g):
            _halo(g, 38, 23, 20, big=big)
            if not big:
                return
            _glow_line(g, [(36, 38), (34.5, 46), (33.5, 54), (33, 63)], core="g1")
            _glow_line(g, tail[3:-3], core="g1")
            _spill(g)
            band = [(50, 18), (46, 16.4), (41, 16), (36, 16.8), (31, 18.8), (27, 21.5)]
            for k, (X, Y) in enumerate(g.path(band)):
                if g.name(X, Y) in MARBLE:
                    g.put(X, Y, "g2" if k % 2 == 0 else "g1")
                if g.name(X, Y + 1) in MARBLE:
                    g.put(X, Y + 1, "g0")
            _stamp(g, 45, 21, [".11.", "1w11", "1111", "1oo1", "1gg1", "1GG1", ".11."], LEG)
            _stamp(g, 48, 31, ["d.", ".d"], LEG)
        _after(p, fx)
        return

    if view in ("down", "up"):
        # the follower: facing the camera (down) or seen from behind (up),
        # bobbing in the air under its sun, wings swept back from the temples
        L = phase
        back = view == "up"
        sp = _spiral(45, 46 - L, 5.2, 1.6, 150, -240, n=28)
        tail = bez3((33, 44 - L), (37, 50 - L), (41, 51 - L), sp[0], n=8) + sp[1:]
        if not back:
            p.limb(tail, 4.0, 2.8, stone, group=20)
            p.circle(tail[-1][0], tail[-1][1], 1.8, bronze, group=22)
        for sx in (-1, 1):
            p.lens((32 + 7.5 * sx, 17 - L), (32 + 21 * sx, 6 - L), 9.0, plume, bend=-1.6 * sx, fat=0.38,
                   group=40 + (sx > 0), bias=-0.1)
        p.limb(bez((29.5, 43 - L), (28, 47 - L), (28.5 - L, 52 - L)), 4.4, 2.4, marble, group=10)
        p.limb(bez((34.5, 43 - L), (36, 47 - L), (35.5 + L, 52 - L)), 4.4, 2.4, marble, group=11)
        p.blob(32, 38.5 - L, 6.4, 6.6, marble, group=1, bias=-0.06)
        p.limb([(26.2, 34 - L), (25.2, 41 - L)], 3.6, 3.2, marble, group=12)
        p.limb([(37.8, 34 - L), (38.8, 41 - L)], 3.6, 3.2, marble, group=13)
        if back:
            for i, x in enumerate((28.5, 32, 35.5)):
                p.limb([(x, 25 - L), (x + (x - 32) * 0.15, 37 - L)], 4.0, 3.6, stone, group=30 + i)
        p.blob(32, 23 - L, 10.8, 10.2, marble, group=3, bias=-0.1)
        if back:
            p.limb(tail, 4.0, 2.8, stone, group=20)
            p.circle(tail[-1][0], tail[-1][1], 1.8, bronze, group=22)

        def fx(g):
            _halo(g, 32, 21 - L, 17.5, big=big)
            if back:
                _glow_line(g, [(32, 39 - L), (32, 45 - L)], core="g1")
            else:
                _glow_line(g, [(32, 35 - L), (32, 44 - L)], core="g1")
                hx, hy = g.c(32, 35 - L)
                g.put(hx, hy, "g2")
            _glow_line(g, tail[2:-2], core="g1")
            band = ([(22, 20 - L), (27, 21.5 - L), (32, 22 - L), (37, 21.5 - L), (42, 20 - L)] if back else
                    [(22.5, 18 - L), (27, 15.6 - L), (32, 15 - L), (37, 15.6 - L), (41.5, 18 - L)])
            for k, (X, Y) in enumerate(g.path(band)):
                if g.name(X, Y) in MARBLE:
                    g.put(X, Y, "g2" if k % 2 == 0 else "g1")
        _after(p, fx)
        if not back:
            p.eye(26, 20 - L, 4, 6, iris="g1", shine="m4", shine_at=(1, 1))
            p.eye(34, 20 - L, 4, 6, iris="g1", shine="m4", shine_at=(1, 1))
        return


MONS = [
    # icon palette 5 keeps the marble white with mauve shadows and the ichor gold
    Mon("Ichorin", ICHORIN_COLORS, ICHORIN_SHINY, ichorin, foot="blank", icon_pal=5),
]
