"""Torpedo line: Narkeray (Water / Electric), a single stage. Meno's numbfish.

In Plato's Meno, Meno tells Socrates he is like the flat torpedo fish, the
narke, which numbs whoever touches it; Socrates answers that he numbs others
only because he is numb himself (Meno 80a-c). Narkeray is the ray of that
simile wearing the face it was compared to: its own eyes sit on top of its
head under a bald dome with furrow ridges, and beard curls fringe its
pointed snout. Two kidney-shaped electric organs glow at its wing roots, with
arcs crackling between them.

Every view is laid out in the ray's own frame (u across the wings, v from
tail to snout) and projected to the screen, so the pose can bank: one wing
raised and curling to show the pale belly, the other dipping.
"""
import math

from mon_lib import C, Mat, Mon, bez3

INK = C.ink

NARKERAY_COLORS = [
    ("ink", INK),
    # a darker sandy-brown back
    ("d0", (64, 40, 24)), ("d1", (104, 72, 40)), ("d2", (144, 104, 64)), ("d3", (184, 144, 96)),
    # the pale bald dome and the lit edges of the markings
    ("pale", (224, 192, 136)),
    # the pale belly, shown on the curled wingtip and the gill edge
    ("m0", (160, 144, 128)), ("m1", (216, 208, 192)), ("white", C.white),
    # Aegean-blue fin rims
    ("b0", (32, 72, 144)), ("b1", (96, 160, 224)),
    # the sun-gold glow of the electric organs
    ("g0", (216, 136, 32)), ("g1", (248, 200, 72)), ("g2", (248, 248, 184)),
    # the electric arcs and sparks
    ("arc", (152, 224, 248)),
]
NARKERAY_SHINY = {
    # the sandy back turns Aegean blue and the glow white; the rims take the sand
    "d0": (24, 40, 96), "d1": (40, 72, 144), "d2": (64, 112, 192), "d3": (104, 152, 224),
    "pale": (168, 208, 240),
    "b0": (104, 72, 40), "b1": (192, 152, 96),
    "g0": (168, 176, 200), "g1": (224, 232, 240), "g2": (248, 248, 248),
}

back = Mat(["d0", "d1", "d2", "d3"], line="d0", cuts=[0.18, 0.44, 0.72])
body = Mat(["d1", "d2", "d3", "pale"], line="d0", cuts=[0.2, 0.46, 0.74])
rimm = Mat(["b0", "b1"], line="b0", cuts=[0.55])
belly = Mat(["m0", "m1", "white"], line="m0", cuts=[0.36, 0.7])
glow = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.4, 0.72])
tailm = Mat(["d0", "d1", "d2"], line="d0", cuts=[0.4, 0.72])

# the disc in the ray's frame: u across the wings, v toward the snout
LEAD_R = ((0, 18.6), (6, 14.6), (21, 9.6), (29, -2))
TRAIL_R = ((29, -2), (25, -8), (11, -11.5), (3.5, -11))
TRAIL_L = ((-3.5, -11), (-11, -11.5), (-23, -8), (-27, -2))
LEAD_L = ((-27, -2), (-20, 9.6), (-6, 14.6), (0, 18.6))


class Frame:
    """Projects the ray's frame to design coordinates: a rotation by ang
    degrees about (cx, cy), scale k, and a bank that lifts the u < 0 wing
    (raise) and drops the u > 0 wing (dip)."""

    def __init__(self, cx, cy, ang, k=1.0, raise_=10.0, dip=5.6):
        a = math.radians(ang)
        self.cx, self.cy, self.k = cx, cy, k
        self.fw = (math.cos(a), math.sin(a))
        self.ff = (-math.sin(a), math.cos(a))
        self.raise_, self.dip = raise_, dip

    def __call__(self, u, v):
        x = self.cx + self.k * (u * self.fw[0] + v * self.ff[0])
        y = self.cy + self.k * (u * self.fw[1] + v * self.ff[1])
        if u < -13:
            y -= self.k * self.raise_ * ((-u - 13) / 14) ** 2
        elif u > 13:
            y += self.k * self.dip * ((u - 13) / 16) ** 2
        return (x, y)

    def path(self, *beziers, n=14):
        out = []
        for b in beziers:
            pts = bez3(*b, n=n)
            out += [self(u, v) for u, v in (pts if not out else pts[1:])]
        return out

    def ellipse(self, cu, cv, ru, rv, n=28):
        return [self(cu + ru * math.cos(2 * math.pi * i / n), cv + rv * math.sin(2 * math.pi * i / n))
                for i in range(n)]


def _inset(b, k):
    return tuple((u * k, v * k - (1 - k) * 2) for u, v in b)


def _ray(p, T, F=0, eyes=True, tail_pts=None, small=False, curl=-1, gills=True):
    """The whole ray in frame T. F flares the discharge and lifts the
    raised wing a little more (frame 2). curl picks the wingtip that curls
    over (-1 the u < 0 wing), gills shows the belly by the snout."""
    # the long whip tail first, behind the disc, with its fin
    if tail_pts:
        p.limb(tail_pts, 4.2 * T.k, 1.6 * T.k, tailm, group=30)
        a, b = tail_pts[-2], tail_pts[-1]
        p.lens(a, (b[0] + (b[0] - a[0]) * 0.6, b[1] + (b[1] - a[1]) * 0.6 - 2 * T.k), 4 * T.k, rimm,
               bend=-1.2, group=31)
    # the pale belly showing under the leading edge by the gills
    if gills:
        p.poly(T.path(((-1, 20.4), (-7, 20.4), (-14, 17), (-21, 10.4)), ((-21, 10.4), (-14, 12.6), (-6, 15.4), (-1, 16.4))),
               belly, group=5)
    # the disc: an Aegean rim, the darker back inset
    p.poly(T.path(LEAD_R, TRAIL_R, TRAIL_L, LEAD_L), rimm, group=1)
    p.poly(T.path(_inset(LEAD_R, 0.9), _inset(TRAIL_R, 0.94), _inset(TRAIL_L, 0.94), _inset(LEAD_L, 0.9)),
           back, group=1, noline=True)
    # the raised wingtip curls over, showing its pale underside
    tip = T(27 * curl, -2)
    p.lens((tip[0] + 2.4 * T.k, tip[1] + 4.4 * T.k), (tip[0] + 1.4 * T.k, tip[1] - (7 + F) * T.k), 5.6 * T.k,
           belly, bend=-2.2 * T.k, group=6)
    # the raised body down the middle, narrowing into the pointed snout
    p.poly(T.path(((0, 16), (6, 14), (9, 6), (8.4, -2)), ((8.4, -2), (7.6, -9), (3, -11), (0, -11)),
                  ((0, -11), (-3, -11), (-7.6, -9), (-8.4, -2)), ((-8.4, -2), (-9, 6), (-6, 14), (0, 16))),
           body, group=2, noline=True, bias=-0.06)
    if small:
        for s in (-1, 1):
            p.poly(T.ellipse(11.5 * s, 2.5, 2.6, 3.8), glow, group=40, noline=True)
        if eyes:
            for s in (-1, 1):
                x, y = T(4.6 * s, 7.6)
                p.px(x, y, "ink")
        return
    for s in (-1, 1):
        p.poly(T.ellipse(11.5 * s, 2.5, 3, 4.4), glow, group=40 + (s > 0), noline=True)
    if eyes:
        for s in (-1, 1):
            x, y = T(4.6 * s, 7.6)
            p.eye(x - 1.5, y - 2, 3, 4, shine="white", shine_at=(1, 1))


def narkeray(p, view, phase):
    if view in ("front", "icon", "side"):
        # gliding toward us and to the left, banking: the left wing raised
        # and curling, the right one dipping, the whip tail trailing away
        F = 1 if (phase == 1 and view in ("front", "side")) else 0
        T = Frame(30, 36, 20, raise_=10 + F * 1.6, dip=5.6 - F)
        tail = [T(0, -10), T(0.6, -17), (43, 12.6 - F), (51, 8.6 - F), (58.4, 9.6 - 2 * F)]
        _ray(p, T, F, tail_pts=tail, small=not p.big)
        return

    if view == "back":
        # over the shoulder, about 1.2x: banking away up and to the right,
        # the far wing raised and curling at the upper left, the near one
        # dipping off the bottom of the frame, the tail trailing toward us
        # off the lower left. The organs sit on a diagonal, so they never
        # pair up like eyes.
        T = Frame(30, 37, 225, k=1.2, raise_=-5, dip=-8)
        # the tail thickens as it comes toward us
        p.limb([T(0, -10), (15, 54), (8, 68)], 4.4, 6.4, tailm, group=30)
        p.lens((14.6, 52.6), (7.6, 49), 4.4, rimm, bend=-0.8, group=31)
        _ray(p, T, eyes=False, curl=1, gills=False)
        return

    if view in ("down", "up"):
        # follower: gliding toward us (down) or away (up), the wings
        # beating, a hand's breadth off the ground
        T = Frame(32, 40, 0 if view == "down" else 180, raise_=3 + 3 * phase, dip=-3 - 3 * phase)
        tail = [T(0, -10), T(0, -18), T(0, -24)] if view == "up" else None
        _ray(p, T, tail_pts=tail, eyes=(view == "down"), small=not p.big, gills=False)
        return


MONS = [
    Mon("Narkeray", NARKERAY_COLORS, NARKERAY_SHINY, narkeray, foot="blank"),
]
