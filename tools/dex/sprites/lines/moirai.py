"""The Moirai (#143-145): Nemira, Lotira and Thanira, the three Fates.

Direction A, "Daughters of Night". In Aristophanes' Birds black-winged
Night lays the first egg of the world, and Hesiod names the Moirai as her
daughters, so here they are her three great birds. One body plan for all
three: a swan's neck arched in an S, a crested head, two wings raised high
in a V and built in layers (pale coverts, a black-figure tongue frieze on
the greater coverts, Night-dark flight feathers incised along the shaft and
pricked with stars), and a bronze whorl set in the breast. From the whorl
the golden thread runs as a glowing seam up the neck to the brow-gem and
back along the spine into the tail, which is each sister's instrument:

    Nemira   the tail feathers twist into a spindle with a bronze whorl ring;
             the thread spins off its point, so her thread begins here
    Lotira   one ruler-straight plume banded in bronze at every cubit; the
             thread runs taut through her from beak to plume, edge to edge
    Thanira  two steel blade feathers crossing like shears; the thread comes
             in and is cut where the blades meet

All three wear the trio's pink brow-gem. The battle sprites are hand
finished in tools/dex/sprites/art/; this file is the draft they started
from, and it still draws the icons and the follower frames.
"""
import math

from mon_lib import C, Mat, Mon, bez, bez3, lerp, lens_pts

INK = C.ink

# --------------------------------------------------------------------------
# Palettes. Every Fate has the same slots, so one drawing serves all three:
#   r0 p0 p1 p2 p3   the body ramp, darkest to lightest
#   n0 n1 n2         the flight-feather ramp: Night's violet, Lotira's olive
#   x                one extra each: Nemira's dusk mauve where rose turns to
#                    Night, Lotira's crane-red crown, Thanira's dark steel
#   b0 g0 g1 g2      dark bronze, bronze, gold, the thread's glow
#   pk               the trio's pink brow-gem
# --------------------------------------------------------------------------

NEMIRA_COLORS = [
    ("ink", INK),
    ("r0", (144, 64, 112)), ("p0", (200, 120, 160)), ("p1", (232, 168, 192)), ("p2", (248, 208, 216)),
    ("p3", C.white),
    ("n0", (40, 32, 88)), ("n1", (80, 64, 152)), ("n2", (144, 128, 216)),
    ("x", (176, 104, 176)),
    ("b0", (120, 64, 40)), ("g0", (200, 128, 48)), ("g1", (240, 192, 72)), ("g2", (248, 240, 168)),
    ("pk", (248, 72, 152)),
]
# "The chiton turns pale Aegean blue and the thread turns silver": the rose
# plumage turns pale Aegean blue and the gold thread silver.
NEMIRA_SHINY = {
    "r0": (48, 96, 160), "p0": (112, 160, 216), "p1": (168, 208, 240), "p2": (208, 232, 248),
    "x": (96, 112, 200),
    "g1": (192, 200, 216), "g2": (240, 248, 248),
}

LOTIRA_COLORS = [
    ("ink", INK),
    ("r0", (112, 96, 72)), ("p0", (168, 152, 120)), ("p1", (208, 192, 160)), ("p2", (232, 224, 200)),
    ("p3", (248, 248, 232)),
    ("n0", (40, 56, 32)), ("n1", (88, 104, 48)), ("n2", (144, 160, 80)),
    ("x", (200, 64, 48)),
    ("b0", (104, 56, 32)), ("g0", (184, 120, 40)), ("g1", (232, 184, 64)), ("g2", (248, 240, 168)),
    ("pk", (248, 72, 152)),
]
# "The chiton turns sun-gold and the thread turns terracotta red": the pale
# plumage turns sun-gold and the thread terracotta.
LOTIRA_SHINY = {
    "r0": (152, 96, 32), "p0": (200, 144, 40), "p1": (232, 184, 64), "p2": (240, 216, 120),
    "p3": (248, 240, 192),
    "g1": (216, 104, 64), "g2": (248, 168, 128),
}

THANIRA_COLORS = [
    ("ink", INK),
    ("r0", (40, 24, 64)), ("p0", (64, 48, 96)), ("p1", (96, 72, 136)), ("p2", (136, 112, 176)),
    ("p3", (224, 216, 240)),
    ("n0", (24, 16, 40)), ("n1", (120, 72, 200)), ("n2", (192, 152, 248)),
    ("x", (104, 112, 144)),
    ("b0", (176, 184, 208)), ("g0", (184, 112, 40)), ("g1", (240, 184, 64)), ("g2", (248, 240, 168)),
    ("pk", (248, 72, 152)),
]
# "The chiton turns marble white and the shears turn silver": the violet
# plumage turns marble white, and the steel blades turn bright silver.
THANIRA_SHINY = {
    "r0": (104, 96, 112), "p0": (160, 152, 160), "p1": (208, 200, 200), "p2": (232, 232, 224),
    "p3": (248, 248, 240),
    "x": (152, 160, 168), "b0": (232, 232, 240),
}


def M(*ramp, line=None, cuts=None):
    return Mat(list(ramp), line=line or ramp[0], cuts=cuts)


body_m = M("r0", "p0", "p1", "p2", "p3", line="r0", cuts=[0.12, 0.3, 0.52, 0.76])
cov_m = M("r0", "p0", "p1", "p2", line="r0", cuts=[0.18, 0.42, 0.7])
night_m = M("n0", "n1", "n2", line="n0", cuts=[0.4, 0.72])
dusk_m = M("n1", "x", "p0", line="n0", cuts=[0.4, 0.72])
bronze_m = M("b0", "g0", "g1", "g2", line="b0", cuts=[0.22, 0.48, 0.76])
beak_m = M("g0", "g1", "g2", line="b0", cuts=[0.42, 0.75])
steel_m = M("x", "b0", "p3", line="ink", cuts=[0.4, 0.75])


# --------------------------------------------------------------------------
# Geometry
# --------------------------------------------------------------------------

def _tag(p, key, pid, **geo):
    """Record which part is which, for the scratch finisher that painted the
    battle art (it reads p.tags when present; the build never sets it)."""
    tags = getattr(p, "tags", None)
    if tags is not None and pid:
        tags.setdefault(key, []).append(dict(pid=pid, **geo))
    return pid


def _rot(pt, c, deg):
    ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    x, y = pt[0] - c[0], pt[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def round_feather(a, b, w, bend=0.0, n=10, root=0.45):
    """A feather with a rounded tip: narrow at the root a, full width toward
    the tip b, bowed sideways by bend."""
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
        ang = math.pi * i / 8
        c, s = math.cos(ang), math.sin(ang)
        cap.append((b[0] + nx * (w / 2) * c + ux * (w / 2) * s, b[1] + ny * (w / 2) * c + uy * (w / 2) * s))
    return left + cap + right[::-1]


def rule_feather(a, b, w, bend=0.0):
    """Lotira's evenly ruled feather: straight sides and a square-cut tip,
    slanted like the end of a ruler."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / d * w / 2, dx / d * w / 2
    ux, uy = dx / d, dy / d
    m = lerp(a, b, 0.3)
    return [(a[0] + nx * 0.5, a[1] + ny * 0.5), (m[0] + nx, m[1] + ny), (b[0] + nx, b[1] + ny),
            (b[0] + ux * 0.8, b[1] + uy * 0.8),
            (b[0] - nx + ux * 1.4, b[1] - ny + uy * 1.4), (m[0] - nx, m[1] - ny), (a[0] - nx * 0.5, a[1] - ny * 0.5)]


def knife_feather(a, b, w, bend=0.0):
    """Thanira's ragged knife feather: a blade with a hooked point."""
    return lens_pts(a, b, w, bend, n=12, fat=0.32)


SHAPES = {"soft": round_feather, "rule": rule_feather, "knife": knife_feather}
STYLE = {"nemira": "soft", "lotira": "rule", "thanira": "knife"}


# --------------------------------------------------------------------------
# Wings: a fan of flight feathers about the shoulder. Each feather is an
# angular sector (degrees, screen coordinates, outermost primary first) with
# a tip radius; a swirl curves every feather the same way, so the wing
# sweeps rather than spreading like a hand fan. The coverts are the inner
# part of the fan and the arm is a band along the leading edge.
# --------------------------------------------------------------------------

def _wing(c, tips, swirl, cov, arm_r, sign):
    """tips: each feather's tip (x, y), outermost first. Sector borders fall
    halfway between neighboring tips; the swirl (degrees at the root, none at
    the tips) curves the feathers without moving their tips."""
    angs, rads = [], []
    prev = None
    for x, y in tips:
        a = math.degrees(math.atan2(y - c[1], x - c[0]))
        if prev is not None:
            while a - prev > 180:
                a -= 360
            while a - prev < -180:
                a += 360
        angs.append(a)
        rads.append(math.hypot(x - c[0], y - c[1]))
        prev = a
    out = []
    for i, (a, R) in enumerate(zip(angs, rads)):
        lo = a - (angs[1] - angs[0]) / 2 if i == 0 else (angs[i - 1] + a) / 2
        hi = a + (a - angs[i - 1]) / 2 if i == len(angs) - 1 else (a + angs[i + 1]) / 2
        out.append((lo, hi, R + 0.8))
    return dict(c=c, feathers=out, swirl=swirl, cov=cov, arm_r=arm_r, sign=sign, rows=[])


NEAR = _wing((32, 33), [(4, 3), (2, 9), (1.8, 15.5), (3, 22), (5.5, 28), (9, 33), (13.5, 37.5), (18.5, 41),
                        (24, 42.5)], swirl=10, cov=0.44, arm_r=24, sign=-1)
# covert rows: tip radius at the leading edge, how much it shortens toward
# the trailing edge, and how many tongues
NEAR["rows"] = [dict(rc=23, taper=0.5, n=6, bump=2.2), dict(rc=15, taper=0.45, n=4, bump=1.8)]
FAR = _wing((44, 36.5), [(55, 2), (59.5, 4.5), (62, 9.5), (62.5, 15.5), (61.5, 21.5), (59, 27), (55.5, 31.5),
                         (51.5, 34.5)],
            swirl=-8, cov=0.42, arm_r=23, sign=1)
FAR["rows"] = [dict(rc=19.5, taper=0.5, n=5, bump=2.0), dict(rc=13, taper=0.45, n=3, bump=1.5)]


# --------------------------------------------------------------------------
# Each sister's own silhouette on the shared plan:
#   Nemira   round and buoyant, the breast full, wings lifted high
#   Lotira   a crane standing tall: body upright, neck straight, a tall V
#   Thanira  hunched and gaunt: body low and lean, the neck arched over so
#            the hooded head hangs forward, wings narrow and swept like blades
# head: where the head's center sits (the face is drawn about (29.5, 9.8)
# and moved there); body: (cx, cy, rx, ry, angle) blobs; spine: the seam
# from the whorl into the tail; tail: the instrument's anchor.
# --------------------------------------------------------------------------

GEO = {
    "nemira": dict(
        near=_wing((32, 33), [(4.5, 2), (2, 7.5), (1.5, 13.5), (2.5, 19.5), (4.5, 25.5), (8, 30.5), (12.5, 34.5),
                              (17.5, 37.5), (23, 39.5)], swirl=10, cov=0.44, arm_r=24, sign=-1),
        far=_wing((44, 36.5), [(54.5, 1.5), (59, 3.5), (62, 8), (62.5, 14), (61.5, 20), (59, 25.5), (55.5, 30),
                               (51.5, 33.5)], swirl=-8, cov=0.42, arm_r=23, sign=1),
        body=[(41, 42.5, 12, 9.4, 14), (33.5, 39.5, 10, 9.6, 0)],
        neck=[(33.5, 37), (24, 30.5), (41, 23), (31, 14)], neck_w=(12.0, 7.2),
        head=(29.5, 9.8), head_r=(7.6, 6.6), whorl=(31.5, 38.5),
        spine=[(34.5, 39), (39, 40.5), (43.5, 43.5), (46.5, 46)],
        tailfan=[((45.5, 42.5), (54, 37.5), 4.0), ((46.5, 43.5), (56.5, 41.5), 4.4), ((47, 45), (57, 46.5), 4.2)],
        tail=(0, 0)),
    "lotira": dict(
        near=_wing((34, 34), [(13, 1.5), (7.5, 3.5), (3.5, 8), (2, 14), (2, 20.5), (3.5, 27), (7, 32.5), (12, 36.5),
                              (18, 39)], swirl=8, cov=0.44, arm_r=26, sign=-1),
        far=_wing((45, 38), [(51, 1.5), (56, 2.5), (60, 5.5), (62, 10.5), (62.5, 16.5), (61.5, 22.5), (59, 28),
                             (55.5, 32.5), (51.5, 36)], swirl=-6, cov=0.42, arm_r=25, sign=1),
        body=[(41, 46, 11, 8.2, 48), (35.5, 41.5, 8.8, 8.8, 0)],
        neck=[(35.5, 38), (35.5, 29), (34, 20), (33.5, 12)], neck_w=(10.6, 6.2),
        head=(31.5, 7.8), head_r=(7.0, 6.0), whorl=(34, 41),
        spine=[(36.5, 42), (39.5, 45), (42.5, 48), (45, 51)],
        tailfan=[((43.5, 47), (51, 43), 4.0), ((44.5, 48.5), (54, 47.5), 4.4), ((45, 50), (53.5, 53), 4.2)],
        tail=(0, 4)),
    "thanira": dict(
        near=_wing((35, 30), [(16, 1.5), (11, 2.5), (7, 5), (4.5, 9), (4, 13.5), (6, 17.5), (10, 20.5),
                              (15, 22.5), (20.5, 24)], swirl=10, cov=0.4, arm_r=24, sign=-1),
        far=_wing((44, 34), [(50, 1.5), (55, 3), (58.5, 6.5), (60.5, 11), (61, 16), (59.5, 21), (56, 25),
                             (51.5, 28)], swirl=-10, cov=0.4, arm_r=22, sign=1),
        body=[(42, 41, 12, 7.4, 8), (34, 39, 8.2, 8.2, 0)],
        neck=[(33, 36.5), (38, 26), (32.5, 15), (26.5, 23)], neck_w=(9.4, 5.6),
        head=(22.5, 26.8), head_r=(6.8, 6.0), whorl=(31, 39),
        spine=[(35.5, 38.5), (40, 38.5), (45, 40), (49, 42)],
        tailfan=[((48, 39), (56, 35.5), 3.6), ((48.5, 40.5), (58, 39.5), 4.0), ((48.5, 42), (57, 44), 3.8)],
        tail=(3, -3)),
}
GEO["nemira"]["near"]["rows"] = [dict(rc=23, taper=0.5, n=6, bump=2.2), dict(rc=15, taper=0.45, n=4, bump=1.8)]
GEO["nemira"]["far"]["rows"] = [dict(rc=19.5, taper=0.5, n=5, bump=2.0), dict(rc=13, taper=0.45, n=3, bump=1.5)]
GEO["lotira"]["near"]["rows"] = [dict(rc=29, taper=0.5, n=6, bump=2.2), dict(rc=19, taper=0.45, n=4, bump=1.8)]
GEO["lotira"]["far"]["rows"] = [dict(rc=25, taper=0.5, n=5, bump=2.0), dict(rc=16, taper=0.45, n=3, bump=1.6)]
GEO["thanira"]["near"]["rows"] = [dict(rc=19, taper=0.45, n=5, bump=2.0), dict(rc=12, taper=0.4, n=3, bump=1.6)]
GEO["thanira"]["far"]["rows"] = [dict(rc=17, taper=0.5, n=5, bump=1.8), dict(rc=11, taper=0.45, n=3, bump=1.4)]


# --------------------------------------------------------------------------
# Wings, pass 3: real wings rather than fans. Each has a curved leading edge
# from the shoulder S (bowed through C) to the wrist Wr, and the hand on to
# Hd. The primaries fan out of the hand to separate points of their own
# lengths; the secondaries hang from the forearm and curve back into the
# body; two rows of coverts and the arm's marginal band lie over the roots.
# Each sister's feathers have her own shape:
#   Nemira   broad and rounded, each tip curling under like wool off a spindle
#   Lotira   long narrow crane primaries splayed like fingers, cut square
#   Thanira  ragged blades with gaps between them, like shears
# --------------------------------------------------------------------------

def fwing(S, C, Wr, Hd, prim, sec, pw, sw, cov=(6.0, 4.2), ncov=(6, 4)):
    return dict(S=S, C=C, Wr=Wr, Hd=Hd, prim=prim, sec=sec, pw=pw, sw=sw, cov=cov, ncov=ncov)


def _qb(p0, p1, p2, t):
    a, b, c = (1 - t) ** 2, 2 * (1 - t) * t, t * t
    return (a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1])


def _arm(W, t):
    """A point on the arm: t 0 at the shoulder, 1 at the wrist, up to 1.6
    out along the hand."""
    if t <= 1:
        return _qb(W["S"], W["C"], W["Wr"], t)
    return lerp(W["Wr"], W["Hd"], (t - 1) / 0.6)


def curl_feather(a, b, w, curl=1.6, n=12):
    """Nemira's feather: broad, round-ended, its tip curling under."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / d, dx / d
    ux, uy = dx / d, dy / d
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        off = curl * t ** 3
        cx, cy = a[0] + dx * t + nx * off, a[1] + dy * t + ny * off
        h = w / 2 * (0.5 + 0.5 * min(1.0, t / 0.45))
        left.append((cx + nx * h, cy + ny * h))
        right.append((cx - nx * h, cy - ny * h))
    tip = (a[0] + dx + nx * curl, a[1] + dy + ny * curl)
    cap = []
    for i in range(1, 8):
        ang = math.pi * i / 8
        c, s_ = math.cos(ang), math.sin(ang)
        cap.append((tip[0] + nx * (w / 2) * c + ux * (w / 2) * s_, tip[1] + ny * (w / 2) * c + uy * (w / 2) * s_))
    return left + cap + right[::-1]


def finger_feather(a, b, w, bend=0.0):
    """Lotira's crane primary: long, even, the end cut square."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / d * w / 2, dx / d * w / 2
    m = lerp(a, b, 0.25)
    return [(a[0] + nx * 0.6, a[1] + ny * 0.6), (m[0] + nx, m[1] + ny), (b[0] + nx, b[1] + ny),
            (b[0] - nx, b[1] - ny), (m[0] - nx, m[1] - ny), (a[0] - nx * 0.6, a[1] - ny * 0.6)]


def blade_feather(a, b, w, bend=0.0):
    """Thanira's primary: a blade, widest a third out, to a sharp point."""
    return lens_pts(a, b, w, bend, n=12, fat=0.33)


FEATHER = {"soft": lambda a, b, w, sg: curl_feather(a, b, w, 1.5 * sg),
           "rule": lambda a, b, w, sg: finger_feather(a, b, w),
           "knife": lambda a, b, w, sg: blade_feather(a, b, w, 0.6 * sg)}


def _trail(W, t):
    """Unit vector from the arm toward the trailing edge at t."""
    p0, p1 = _arm(W, max(0, t - 0.03)), _arm(W, min(1.6, t + 0.03))
    tx, ty = p1[0] - p0[0], p1[1] - p0[1]
    d = math.hypot(tx, ty) or 1
    nx, ny = -ty / d, tx / d
    cx = sum(q[0] for q in W["sec"]) / len(W["sec"])
    cy = sum(q[1] for q in W["sec"]) / len(W["sec"])
    q = _arm(W, t)
    if (cx - q[0]) * nx + (cy - q[1]) * ny < 0:
        nx, ny = -nx, -ny
    return nx, ny


def wing2(p, kind, W, beat, g0, side="near", bias=0.0, back=False):
    """Draw a wing; tags every feather for the finisher."""
    style = STYLE[kind]
    shape = FEATHER[style]
    sg = 1 if side == "near" else -1
    rot = (-beat if side == "near" else beat)
    c = W["S"]

    def R(pt, k=1.0):
        return _rot(pt, c, rot * k)
    g = g0
    n = len(W["prim"])
    if not p.big:
        # icons and followers: a few broad feathers, one covert mass, the arm,
        # so the wing still reads at 32 px
        for i, tip in enumerate(W["prim"]):
            if i % 2:
                continue
            base = R(lerp(W["Hd"], W["Wr"], i / max(n - 1, 1)))
            w = W["pw"][i] if isinstance(W["pw"], (list, tuple)) else W["pw"]
            p.poly(lens_pts(base, R(tip, 1.3), w * 1.9, 0, fat=0.45), night_m, group=g, bias=bias)
            g += 1
        for i, tip in enumerate(W["sec"]):
            if i % 2:
                continue
            t = 0.9 - 0.68 * i / max(len(W["sec"]) - 1, 1)
            p.poly(lens_pts(R(_arm(W, t)), R(tip), W["sw"] * 1.8, 0, fat=0.45), night_m, group=g, bias=bias)
            g += 1
        q0, q1 = _arm(W, 0.25), _arm(W, 1.05)
        tx, ty = _trail(W, 0.65)
        p.poly(lens_pts(R(q0), R((q1[0] + tx * 3, q1[1] + ty * 3)), 9, 0, fat=0.5), cov_m, group=g, bias=bias)
        path = [R(_arm(W, k / 12 * 1.4)) for k in range(13)]
        p.limb(path, 4.4, 2.6, body_m, group=g + 1, bias=bias - 0.05)
        return g + 2
    for i, tip in enumerate(W["prim"]):
        base = R(lerp(W["Hd"], W["Wr"], i / max(n - 1, 1)))
        b = R(tip, 1.3)
        w = W["pw"][i] if isinstance(W["pw"], (list, tuple)) else W["pw"]
        pid = p.poly(shape(base, b, w, sg), night_m, group=g, bias=bias)
        _tag(p, side + "_prim", pid, a=base, b=b, w=w, i=i, n=n)
        g += 1
    m = len(W["sec"])
    for i, tip in enumerate(W["sec"]):
        t = 0.9 - 0.68 * i / max(m - 1, 1)
        base = R(_arm(W, t))
        b = R(tip)
        w = W["sw"]
        pid = p.poly(shape(base, b, w, sg) if style != "soft" else curl_feather(base, b, w, 1.0 * sg),
                     night_m, group=g, bias=bias)
        _tag(p, side + "_sec", pid, a=base, b=b, w=w, i=i, n=m)
        g += 1
    # coverts: greater then lesser, each a row of rounded tongues along the arm
    for row, (ln, cnt) in enumerate(zip(W["cov"], W["ncov"])):
        for j in range(cnt):
            t = 0.12 + (1.2 - 0.12) * (j + 0.5) / cnt
            q = _arm(W, t)
            tx, ty = _trail(W, t)
            off = 1.2 if row == 0 else 0.4
            a = (q[0] + tx * off, q[1] + ty * off)
            L = ln * (0.75 + 0.25 * (1 - abs(t - 0.8) / 0.8))
            b = (a[0] + tx * L, a[1] + ty * L)
            w = 4.6 if row == 0 else 3.8
            pid = p.poly(round_feather(R(a), R(b), w, 0.3 * sg, root=0.7), cov_m, group=g, bias=bias)
            _tag(p, side + ("_gcov" if row == 0 else "_lcov"), pid, a=R(a), b=R(b), w=w, j=j)
            g += 1
    # the arm: the marginal coverts along the leading edge, root to hand
    path = [R(_arm(W, k / 20 * 1.6)) for k in range(21)]
    pid = p.limb(path, 4.2, 2.4, body_m, group=g, bias=bias - 0.05)
    _tag(p, side + "_arm", pid, path=path)
    return g + 1


WINGS = {
    "nemira": dict(
        near=fwing((31, 33), (28.5, 18), (19, 15), (13, 10),
                   [(4.5, 1.5), (1.5, 7), (1.5, 13.5), (2.5, 20), (5, 26), (9, 30.5), (14, 34)],
                   [(18.5, 37.5), (22.5, 40), (26, 41.5), (29, 42)], pw=[5.0, 5.4, 5.6, 5.6, 5.6, 5.4, 5.2], sw=5.0),
        far=fwing((44, 36), (42.5, 23), (48.5, 15), (52.5, 9),
                  [(56, 1.5), (60.5, 4.5), (62.4, 10), (62.4, 16), (61, 22), (58, 27.5), (54.5, 31.5)],
                  [(51.5, 35), (48.5, 38), (46, 39.5)], pw=[4.6, 5.0, 5.2, 5.2, 5.0, 4.8, 4.6], sw=4.6,
                  cov=(5.0, 3.6), ncov=(5, 3))),
    "lotira": dict(
        near=fwing((33, 33), (32.5, 18.5), (22, 13), (16.5, 7.5),
                   [(9.5, 1.2), (3.5, 3.5), (1.4, 9.5), (1.6, 16), (3.5, 22.5), (7.5, 28)],
                   [(12, 33), (16.5, 36.5), (21.5, 39), (26.5, 40.5), (30.5, 40.5)], pw=3.8, sw=4.2,
                   cov=(7.0, 4.6), ncov=(6, 4)),
        far=fwing((45, 37), (43.5, 22.5), (50, 14), (53, 7.5),
                  [(55, 1.2), (59.5, 3), (62.4, 7.5), (62.4, 13.5), (61.5, 19.5), (59, 25.5)],
                  [(56.5, 30.5), (53.5, 34.5), (50, 37.5)], pw=3.6, sw=4.0, cov=(4.4, 3.0), ncov=(5, 3))),
    "thanira": dict(
        near=fwing((35, 30), (34, 16.5), (25, 12), (19.5, 6),
                   [(13, 1.2), (8, 2.5), (4.5, 6), (3, 11), (4, 16.5), (7, 21)],
                   [(11, 24.5), (15.5, 27), (20.5, 29), (26, 30)], pw=4.2, sw=4.2, cov=(5.0, 3.6), ncov=(5, 3)),
        far=fwing((44, 34), (42.5, 21.5), (49, 14), (52, 7),
                  [(54, 1.2), (58, 3), (61, 7), (62.4, 12), (61.5, 17.5), (59.5, 22.5)],
                  [(56.5, 26.5), (53, 29.5), (49.5, 31.5)], pw=4.0, sw=4.0, cov=(4.6, 3.2), ncov=(4, 3))),
}
# the back view: the near wing sweeps out to the left and toward us, its
# secondaries curving down in groups; the far wing rises behind the head
BK_WINGS = {
    k: dict(
        near=fwing((21, 46), (17, 34), (10, 21), (8, 12),
                   [(16, 1.5), (10, 1.4), (4.5, 3.5), (1.6, 8.5), (1.4, 15)] if k != "lotira" else
                   [(17, 1.2), (11, 1.2), (5, 2.8), (1.6, 7.5), (1.4, 13.5)],
                   [(1.4, 23), (1.8, 30), (3.5, 36.5), (7, 42), (12, 46.5)],
                   pw=5.4 if k == "nemira" else (4.0 if k == "lotira" else 4.6), sw=5.6, cov=(6.0, 4.0), ncov=(5, 3)),
        far=fwing((42, 45), (46, 33), (51, 22), (52.5, 13),
                  [(47, 1.5), (52.5, 1.5), (57.5, 4), (61, 8.5), (62.4, 14)],
                  [(62.4, 22), (61, 29), (58, 35), (54, 40)],
                  pw=5.0 if k == "nemira" else (3.8 if k == "lotira" else 4.4), sw=5.0, cov=(5.0, 3.6), ncov=(4, 3)))
    for k in ("nemira", "lotira", "thanira")
}


def tip_r(style, R, u, k):
    """The tip radius across one feather (u 0..1 from its leading side)."""
    if style == "soft":
        return R - 1.6 + 1.6 * math.sin(math.pi * u) ** 0.6
    if style == "rule":
        return R - (0.9 if (u < 0.1 or u > 0.9) else 0.0)
    # knife: a slanted blade point, every other feather cut short
    return R * (1.0 if k % 2 == 0 else 0.88) - 6.0 * u


def wing_field(W, beat, x, y, style="soft"):
    """(k, u, t, r) for a canvas point inside the wing's fan, else None:
    feather index, position across it, fraction of its length, radius."""
    cx, cy = W["c"]
    dx, dy = x - cx, y - cy
    r = math.hypot(dx, dy)
    th = math.degrees(math.atan2(dy, dx))
    th -= W["swirl"] * max(0.0, 1 - r / 38.0) + W["sign"] * -beat
    fs = W["feathers"]
    lo, hi = fs[0][0], fs[-1][1]
    for off in (0, 360, -360):
        tt = th + off
        if min(lo, hi) <= tt <= max(lo, hi):
            break
    else:
        return None
    for k, (a, b, R) in enumerate(fs):
        if min(a, b) <= tt <= max(a, b):
            u = (tt - a) / (b - a)
            rt = tip_r(style, R, u, k)
            if r > rt:
                return None
            return k, u, r / rt, r
    return None


def wing_poly(W, beat, style, inner=None):
    """The wing's silhouette as a polygon (or, with inner=f, the region within
    f of each feather's length: the coverts)."""
    cx, cy = W["c"]
    pts = []

    def P(r, th):
        th = th + W["swirl"] * max(0.0, 1 - r / 38.0) + W["sign"] * -beat
        return (cx + r * math.cos(math.radians(th)), cy + r * math.sin(math.radians(th)))
    fs = W["feathers"]
    a0 = fs[0][0]
    R0 = tip_r(style, fs[0][2], 0.0, 0) * (inner or 1.0)
    for i in range(0, 13):
        pts.append(P(R0 * i / 12, a0))
    for k, (a, b, R) in enumerate(fs):
        for j in range(0, 9):
            u = j / 8
            rt = tip_r(style, R, u, k)
            if inner:
                rt = min(R * inner + 1.3 * math.sin(math.pi * u), W["arm_r"] * 0.8 + 1.3 * math.sin(math.pi * u))
            pts.append(P(rt, a + (b - a) * u))
    bl = fs[-1][1]
    Rl = pts[-1]
    for i in range(12, -1, -1):
        r = math.hypot(Rl[0] - cx, Rl[1] - cy)
        pts.append(P(r * i / 12, bl))
    return pts


def _span(W):
    fs = W["feathers"]
    return fs[0][0], fs[-1][1]


def _swirled(W, beat, x, y):
    cx, cy = W["c"]
    dx, dy = x - cx, y - cy
    r = math.hypot(dx, dy)
    th = math.degrees(math.atan2(dy, dx)) - W["swirl"] * max(0.0, 1 - r / 38.0) - W["sign"] * -beat
    lo, hi = _span(W)
    for off in (0, 360, -360):
        if min(lo, hi) <= th + off <= max(lo, hi):
            return r, (th + off - lo) / (hi - lo)
    return r, None


def covert_tip(row, f):
    """Tip radius of a covert row at fraction f across the wing."""
    n = row["n"]
    j = min(int(f * n), n - 1)
    u = f * n - j
    mid = (j + 0.5) / n
    return row["rc"] * (1 - row["taper"] * mid) - row["bump"] + row["bump"] * math.sin(math.pi * u) ** 0.7, j, u


def covert_at(W, beat, row, x, y):
    r, f = _swirled(W, beat, x, y)
    if f is None:
        return None
    rt, j, u = covert_tip(row, f)
    if r > rt:
        return None
    return j, u, r / rt


def covert_poly(W, beat, row):
    cx, cy = W["c"]
    lo, hi = _span(W)

    def P(r, f):
        th = lo + (hi - lo) * f
        th = th + W["swirl"] * max(0.0, 1 - r / 38.0) + W["sign"] * -beat
        return (cx + r * math.cos(math.radians(th)), cy + r * math.sin(math.radians(th)))
    pts = [P(0, 0)]
    N = row["n"] * 10
    for i in range(N + 1):
        f = i / N
        rt, _, _ = covert_tip(row, min(f, 0.9999))
        pts.append(P(rt, f))
    return pts


def arm_poly(W, beat, width=5.0):
    """A band along the leading edge, root to wrist."""
    cx, cy = W["c"]
    a0 = W["feathers"][0][0]

    def P(r, th):
        th = th + W["swirl"] * max(0.0, 1 - r / 38.0) + W["sign"] * -beat
        return (cx + r * math.cos(math.radians(th)), cy + r * math.sin(math.radians(th)))
    out = [P(W["arm_r"] * i / 10, a0) for i in range(11)]
    back = []
    for i in range(10, -1, -1):
        r = W["arm_r"] * i / 10
        w = width * (0.6 + 0.4 * math.sin(math.pi * min(1, r / W["arm_r"] * 1.1)))
        ang = math.degrees(w / max(r, 3)) * W["sign"] * -1
        back.append(P(r, a0 - ang))
    return out + back


def wing(p, kind, W, beat, g0, bias=0.0, side="near"):
    style = STYLE[kind]
    pid = p.poly(wing_poly(W, beat, style), night_m, group=g0, bias=bias)
    _tag(p, side + "_wing", pid, W=W, beat=beat, style=style)
    for i, row in enumerate(W["rows"]):
        pid = p.poly(covert_poly(W, beat, row), cov_m, group=g0 + 1 + i, bias=bias)
        _tag(p, side + "_covert", pid, row=row)
    pid = p.poly(arm_poly(W, beat), body_m, group=g0 + 5, bias=bias - 0.05)
    _tag(p, side + "_arm", pid)
    return g0 + 6


TAILFAN = [((45.5, 42.5), (54, 37.5), 4.0), ((46.5, 43.5), (56.5, 41.5), 4.4), ((47, 45), (57, 46.5), 4.2)]


# --------------------------------------------------------------------------
# The front: three-quarter view facing left, wings raised high in a V
# --------------------------------------------------------------------------

NECK = [(33.5, 37), (23, 30.5), (41.5, 23), (31, 14)]
NECK_W = {"nemira": (9.2, 6.6), "lotira": (8.4, 6.0), "thanira": (8.0, 5.6)}
HEAD = (29.5, 9.8)
HEAD_R = {"nemira": (7.4, 6.4), "lotira": (7.0, 6.0), "thanira": (6.8, 6.0)}
WHORL = (31.5, 38)


def _head(p, kind, L):
    """Head, crest, beak, face and the brow-gem."""
    big = p.big
    hx, hy = HEAD[0], HEAD[1] - L
    rx, ry = GEO[kind]["head_r"]
    _tag(p, "head", p.blob(hx, hy, rx, ry, body_m, group=3))

    # ---- crest ----------------------------------------------------------------
    if kind == "nemira":
        for a, b, w, bend in (((31, 6 - L), (41, 2 - L), 4.4, -1.6), ((33, 8.5 - L), (43.5, 7.5 - L), 4.0, -1.4),
                              ((29, 5.5 - L), (32.5, 1.2 - L), 3.6, -1.2)):
            _tag(p, "crest", p.lens(a, b, w, body_m, bend=bend, fat=0.65, group=8))
    elif kind == "lotira":
        _tag(p, "crest", p.lens((31, 6 - L), (45, 1.4 - L), 3.0, cov_m, fat=0.2, group=8))
        _tag(p, "crest", p.lens((32.5, 7.5 - L), (46, 5.6 - L), 2.6, cov_m, fat=0.2, group=9))
    else:
        _tag(p, "crest", p.lens((36, 7.5 - L), (21, 5.5 - L), 6.6, M("r0", "p0", "p1", line="r0"),
                                bend=1.6, fat=0.62, group=8))

    # ---- beak ---------------------------------------------------------------------
    if kind == "thanira":
        _tag(p, "beak", p.lens((24.5, 11.5 - L), (17, 15 - L), 3.6, beak_m, bend=-1.0, fat=0.25, group=7))
    elif kind == "lotira":
        _tag(p, "beak", p.lens((24.5, 11.5 - L), (14.5, 13.5 - L), 3.2, beak_m, fat=0.2, group=7))
    else:
        _tag(p, "beak", p.lens((24.5, 11.5 - L), (18, 13 - L), 3.6, beak_m, fat=0.25, group=7))

    if not big:
        p.px(26, 9 - L, "ink")
        return

    # ---- face -------------------------------------------------------------------
    ex, ey = 26, 6 - L
    if kind == "nemira":
        p.patch(ex, ey, [".11.", "1w11", "1w11", "1111", "1ii1", ".11."], {"1": "ink", "w": "p3", "i": "pk"})
    elif kind == "lotira":
        p.patch(ex - 1, ey, ["11111"], {"1": "ink"})
        p.patch(ex, ey + 1, ["1w11", "1111", "1ii1", ".11."], {"1": "ink", "w": "p3", "i": "n1"})
    else:
        p.patch(ex - 1, ey, ["rrrrrr", "111111"], {"r": "r0", "1": "ink"})
        p.patch(ex, ey + 2, ["1i11", "1ii1", ".11."], {"1": "ink", "i": "n2"})
        p.px(ex + 1, ey + 2, "p3")
    gx, gy = 30, 3 - L
    p.pxs([(gx, gy - 1), (gx - 1, gy), (gx + 1, gy), (gx, gy + 1)], "pk")
    p.px(gx, gy, "p3")


def _moved(p, d, fn, *args):
    """Draw with the pen shifted by d design px (a sister's head or tail
    drawn about the shared position and moved to her own)."""
    ox, oy = p.ox, p.oy
    p.ox, p.oy = ox + d[0] * p.s, oy + d[1] * p.s
    try:
        fn(*args)
    finally:
        p.ox, p.oy = ox, oy


def fate_front(p, kind, phase):
    big = p.big
    beat = 4 * phase
    L = phase
    G = GEO[kind]

    # ---- tail: the instrument, behind the body ------------------------------
    _moved(p, G["tail"], {"nemira": _spindle, "lotira": _plume, "thanira": _shears}[kind], p, phase)

    # ---- a short fan of Night-dark tail coverts behind the instrument ---------
    for i, (a, b, w) in enumerate(G["tailfan"]):
        _tag(p, "tailfan", p.poly(SHAPES[STYLE[kind]](a, b, w, 0.4), night_m, group=50 + i, bias=0.1),
             a=a, b=b, w=w)

    wing2(p, kind, WINGS[kind]["far"], beat, 10, side="far", bias=0.12)

    # ---- body: breast and back as one form ------------------------------------
    for cx, cy, rx, ry, ang in G["body"]:
        _tag(p, "body", p.blob(cx, cy, rx, ry, body_m, ang=ang, group=1))

    wing2(p, kind, WINGS[kind]["near"], beat, 100, side="near")

    # ---- the swan's neck and head ------------------------------------------------
    neck = bez3(*G["neck"], n=24)
    nw0, nw1 = G["neck_w"]
    _tag(p, "neck", p.limb(neck, nw0, nw1, body_m, group=2), path=neck)
    hd = (G["head"][0] - HEAD[0], G["head"][1] - HEAD[1])
    _moved(p, hd, _head, p, kind, L)
    # the bronze whorl in the breast
    wx, wy = G["whorl"]
    _tag(p, "whorl", p.circle(wx, wy, 4.4, bronze_m, group=6))
    if not big:
        return

    _seam(p, kind, L)


def _seam(p, kind, L):
    """The golden thread as a seam: brow down the neck to the whorl, and from
    the whorl along the spine into the tail."""
    G = GEO[kind]
    neck = bez3(*G["neck"], n=12)
    p.stroke([(x + 1, y) for x, y in neck], "g2")
    p.stroke(G["spine"], "g2")


def _spindle(p, phase):
    """The tail hangs as a drop spindle: the cop of twisted tail feathers
    wound with gold, a bronze whorl, the shaft and a fine point."""
    _tag(p, "tail", p.blob(49.5, 51, 4.6, 4.6, cov_m, group=60))
    _tag(p, "whorl2", p.blob(49, 56.5, 6.2, 2.0, bronze_m, group=62))
    _tag(p, "shaft", p.taper([(49, 57), (49, 62)], 2.4, bronze_m, group=61))
    if p.big:
        for y in (49, 52):
            p.stroke([(46, y + 1), (52, y - 1)], "g1")


def _plume(p, phase):
    _tag(p, "tail", p.limb([(44.5, 43.5), (60.5, 59.5)], 5.6, 4.0, cov_m, group=60),
         a=(44.5, 43.5), b=(60.5, 59.5), w=5.0)
    if p.big:
        for k in range(1, 7):
            x, y = 44.5 + k * 16 / 7, 43.5 + k * 16 / 7
            p.stroke([(x - 2, y + 1.8), (x + 1.8, y - 2)], "g0")
        p.stroke([(45.5, 44.5), (61.5, 60.5)], "g2")


def _shears(p, phase):
    _tag(p, "blade", p.lens((46.5, 43), (57.5, 62), 4.8, steel_m, fat=0.22, bend=-0.6, group=60),
         a=(46.5, 43), b=(57.5, 62), w=4.8)
    _tag(p, "blade", p.lens((43.5, 47.5), (62.4, 53.5), 4.8, steel_m, fat=0.22, bend=0.6, group=61),
         a=(43.5, 47.5), b=(62.4, 53.5), w=4.8)
    _tag(p, "pivot", p.circle(50.5, 50, 1.9, bronze_m, group=62))
    if p.big:
        p.stroke([(62, 59), (55.5, 56)], "g2")


# --------------------------------------------------------------------------
# The back: over the shoulder, about 1.2x the front, the head turned right
# into profile, both wings spread vast, the seam glowing down the spine and
# the instrument swinging out at the lower left
# --------------------------------------------------------------------------

BK_NEAR = _wing((19, 46), [(17, 1.5), (11, 2), (6, 4.5), (2.5, 9), (1.2, 15), (1.2, 21.5), (2, 28), (4, 34),
                           (7.5, 39)], swirl=-8, cov=0.42, arm_r=32, sign=-1)
BK_NEAR["rows"] = [dict(rc=26, taper=0.5, n=7, bump=2.4), dict(rc=16, taper=0.45, n=5, bump=2.0)]
BK_FAR = _wing((41, 44), [(43, 1.5), (49, 2), (54.5, 4), (58.5, 8), (61.5, 13.5), (62.5, 19.5), (62.5, 26),
                          (61, 32), (58, 37)], swirl=8, cov=0.42, arm_r=30, sign=1)
BK_FAR["rows"] = [dict(rc=24, taper=0.5, n=6, bump=2.2), dict(rc=15, taper=0.45, n=4, bump=1.8)]
BK_NECK = [(33, 51), (27, 45), (44.5, 45), (40, 37.5)]
BK_NECK_W = {k: (g["neck_w"][0] * 1.05, g["neck_w"][1] * 1.05) for k, g in GEO.items()}
BK_HEAD = (44.5, 31)
BK_HEAD_R = {k: (g["head_r"][0] * 1.2, g["head_r"][1] * 1.2) for k, g in GEO.items()}


def fate_back(p, kind):
    {"nemira": _bk_spindle, "lotira": _bk_plume, "thanira": _bk_shears}[kind](p)
    wing2(p, kind, BK_WINGS[kind]["far"], 0, 10, side="far", bias=0.12, back=True)
    # the back, cropped by the frame, with the shoulders the wings rise from
    _tag(p, "body", p.blob(31, 61, 22, 12.5, body_m, group=1))
    _tag(p, "body", p.blob(41, 50, 7.5, 6.5, body_m, group=1))
    wing2(p, kind, BK_WINGS[kind]["near"], 0, 100, side="near", back=True)
    _tag(p, "body", p.blob(19.5, 52, 9, 7.5, body_m, group=4))
    neck = bez3(*BK_NECK, n=24)
    nw0, nw1 = BK_NECK_W[kind]
    _tag(p, "neck", p.limb(neck, nw0, nw1, body_m, group=2), path=neck)
    _moved(p, (BK_HEAD[0] - 45, BK_HEAD[1] - 27), _bk_head, p, kind)
    if p.big:
        _bk_seam(p, kind)


def _bk_head(p, kind):
    hx, hy = 45, 27
    rx, ry = BK_HEAD_R[kind]
    _tag(p, "head", p.blob(hx, hy, rx, ry, body_m, group=3))
    tip = {"nemira": (60.5, 29), "lotira": (62, 28.5), "thanira": (60, 32)}[kind]
    _tag(p, "beak", p.lens((hx + rx - 1.5, hy + 1), tip, 4.0, beak_m, fat=0.25, group=7))
    if kind == "nemira":
        for a, b, w in (((41, 22), (30, 19), 5.0), ((40, 25.5), (28.5, 26), 4.6), ((43, 20), (36, 13.5), 4.4)):
            _tag(p, "crest", p.lens(a, b, w, body_m, bend=-1.5, fat=0.6, group=8))
    elif kind == "lotira":
        _tag(p, "crest", p.lens((41, 22), (26, 17), 3.4, cov_m, fat=0.2, group=8))
        _tag(p, "crest", p.lens((40.5, 24.5), (25.5, 22.5), 3.0, cov_m, fat=0.2, group=9))
    else:
        _tag(p, "crest", p.lens((36, 26), (54, 22), 7.6, M("r0", "p0", "p1", line="r0"), bend=1.8, fat=0.38, group=8))
    if p.big:
        p.eye(48, 23, 3, 5, iris="pk" if kind == "nemira" else ("g1" if kind == "lotira" else "n2"), shine="p3",
              shine_at=(1, 1))


def _bk_seam(p, kind):
    p.stroke(bez3(*BK_NECK, n=12), "g2")
    p.stroke([(31, 50), (31, 56), (31, 63)], "g2")


def _bk_spindle(p):
    _tag(p, "tail", p.lens((12, 39), (11, 52), 12.0, cov_m, fat=0.5, group=60))
    _tag(p, "whorl2", p.blob(11, 53, 9.0, 2.6, bronze_m, group=62))
    _tag(p, "shaft", p.taper([(11, 54), (11, 61)], 3.0, bronze_m, group=61))


def _bk_plume(p):
    _tag(p, "tail", p.limb([(20, 44), (2, 62)], 8.0, 7.0, cov_m, group=60))


def _bk_shears(p):
    _tag(p, "blade", p.lens((22, 44), (2, 54), 6.4, steel_m, fat=0.22, bend=0.6, group=60))
    _tag(p, "blade", p.lens((22, 48), (8, 63), 6.4, steel_m, fat=0.22, bend=-0.6, group=61))


# --------------------------------------------------------------------------
# Follower: facing the camera (down) and walking away (up), wings raised
# --------------------------------------------------------------------------

def _mirror(W):
    """The same wing on the other side of x = 32."""
    cx, cy = W["c"]
    fs = [(180 - b, 180 - a, R) for a, b, R in W["feathers"]]
    return dict(W, c=(64 - cx, cy), feathers=fs, swirl=-W["swirl"], sign=-W["sign"],
                rows=list(W["rows"]))


FL = _wing((26, 33), [(15, 3), (9, 6), (5, 11), (3.5, 17), (4, 23), (6.5, 28.5), (10.5, 32.5), (15.5, 35.5)],
           swirl=-6, cov=0.42, arm_r=20, sign=-1)
FL["rows"] = [dict(rc=17, taper=0.5, n=5, bump=1.8)]
FR = _wing((38, 33), [(49, 3), (55, 6), (59, 11), (60.5, 17), (60, 23), (57.5, 28.5), (53.5, 32.5), (48.5, 35.5)],
           swirl=6, cov=0.42, arm_r=20, sign=1)
FR["rows"] = [dict(rc=17, taper=0.5, n=5, bump=1.8)]


def fate_follow(p, kind, view, phase):
    beat = 5 * phase
    face = view == "down"
    # the instrument hangs below
    if kind == "nemira":
        p.blob(32, 50, 3.6, 3.8, cov_m, group=60)
        p.blob(32, 55, 5.4, 1.8, bronze_m, group=62)
        p.taper([(32, 55.5), (32, 61)], 2.4, bronze_m, group=61)
    elif kind == "lotira":
        p.limb([(32, 44), (32, 61)], 4.6, 3.4, cov_m, group=60)
        for y in (49, 53, 57):
            p.rect(30, y, 34, y, bronze_m, group=61 + y)
    else:
        p.lens((30, 44), (37, 61), 4.0, steel_m, fat=0.25, group=60)
        p.lens((34, 44), (27, 61), 4.0, steel_m, fat=0.25, group=61)
        p.circle(32, 50, 1.6, bronze_m, group=62)
    wing(p, kind, FL, beat, 10, side="left")
    wing(p, kind, FR, beat, 20, side="right")
    p.blob(32, 41, 9.5, 8.5, body_m, group=1)
    nw0, nw1 = NECK_W[kind]
    p.limb(bez((32, 38), (34, 28), (32, 21)), nw0, nw1, body_m, group=2)
    p.circle(32, 15 - phase, 6.4, body_m, group=3)
    if kind == "nemira":
        p.blob(35, 8 - phase, 3.4, 2.6, body_m, ang=-30, group=8)
        p.blob(29, 8 - phase, 3.4, 2.6, body_m, ang=30, group=8)
    elif kind == "lotira":
        p.lens((33, 10 - phase), (40, 3 - phase), 2.6, cov_m, fat=0.2, group=8)
        p.lens((31, 10 - phase), (24, 3 - phase), 2.6, cov_m, fat=0.2, group=9)
    else:
        p.lens((32, 6 - phase), (32, 17 - phase), 13, M("r0", "p0", "p1", line="r0"), fat=0.35, group=8)
    if face:
        p.lens((32, 17 - phase), (32, 23 - phase), 4.4, beak_m, fat=0.3, group=7)
        if kind == "thanira":
            p.rect(28, 15 - phase, 29, 15 - phase, Mat(["ink"]), group=9)
            p.rect(35, 15 - phase, 36, 15 - phase, Mat(["ink"]), group=9)
        else:
            p.eye(27.5, 12 - phase, 2, 4 if kind == "nemira" else 3, iris="pk" if kind == "nemira" else None,
                  shine="p3", shine_at=(0, 0))
            p.eye(34.5, 12 - phase, 2, 4 if kind == "nemira" else 3, iris="pk" if kind == "nemira" else None,
                  shine="p3", shine_at=(1, 0))
        p.circle(32, 37, 2.4, bronze_m, group=6)
        if p.big:
            p.pxs([(32, 9 - phase)], "pk")
            p.stroke([(32, 21), (32, 35)], "g2")
    elif p.big:
        p.stroke([(32, 12), (32, 48)], "g2")


def make(kind):
    def draw(p, view, phase):
        if view in ("front", "side", "icon"):
            fate_front(p, kind, phase if view == "front" else 0)
            return
        if view == "back":
            fate_back(p, kind)
            return
        if view in ("down", "up"):
            fate_follow(p, kind, view, phase)
            return
    return draw


MONS = [
    Mon("Nemira", NEMIRA_COLORS, NEMIRA_SHINY, make("nemira"), foot="bird", icon_pal=0, follow=27),
    Mon("Lotira", LOTIRA_COLORS, LOTIRA_SHINY, make("lotira"), foot="bird", icon_pal=4, follow=27),
    Mon("Thanira", THANIRA_COLORS, THANIRA_SHINY, make("thanira"), foot="bird", icon_pal=2, follow=27),
]
