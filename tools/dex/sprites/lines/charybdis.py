"""Trybdis (#136), the Whirlpool: Charybdis, who drinks the sea three times a day.

Direction A, "The Frilled Maw". An indigo sea-serpent rears out of its own
coils in a frilled lizard's threat display. Its jaws are thrown open toward
the viewer on a round throat ringed with three rows of hooked fangs, each
row deeper, smaller and darker, all hooked the same way round so the rings
turn like the whirlpool they are; the sea spirals in between them toward a
magenta glow in the deep. Behind the head a violet palmette frill (the
anthemion Hexylla wears as six webbed necks) spreads in a pinwheel, light
coming through its membrane and magenta glowing in its ribs, and runs on
down the spine as a sail. The tail rises at the right and turns to living
fig wood at the tip: the fig tree Odysseus hung from while the whirlpool
swallowed his raft.

The battle sprites are hand finished in tools/dex/sprites/art/; this file is
the draft they started from, and it still draws the icon and the follower
frames. LAYERS lets a finishing script render one layer of the front or
back at a time (frill, body, jaw_lo, jaw_up, maw); the build leaves it None.
"""
import math

from mon_lib import Mat, Mon, bez, bez3, lens_pts

COLORS = [
    ("ink", (32, 24, 40)),
    # indigo serpent scales, darkest to the wet sheen
    ("b0", (24, 32, 88)), ("b1", (40, 64, 144)), ("b2", (64, 112, 200)), ("b3", (128, 176, 232)),
    # marble: fangs, foam, the sheen on wet scales, eye shine
    ("wh", (240, 240, 232)),
    # limestone: belly plates, lower jaw, fig bark (the Ground in it)
    ("l0", (136, 104, 80)), ("l1", (208, 192, 152)),
    # the palmette frill's violet membrane, and the throat
    ("v0", (56, 24, 88)), ("v1", (104, 48, 144)), ("v2", (160, 96, 200)),
    # the signature glow, shared with Hexylla A
    ("g1", (224, 88, 224)), ("g2", (248, 184, 248)),
    # fig leaves
    ("f0", (56, 96, 48)), ("f1", (120, 160, 64)),
]
# "The water turns sun-gold and the rim turns marble white": the sea-blue
# scales (and the water they pull in) turn sun-gold, the limestone jaw and
# belly turn marble. The violet frill and magenta glow stay.
SHINY = {
    "b0": (104, 56, 24), "b1": (176, 112, 32), "b2": (224, 168, 56), "b3": (248, 224, 120),
    "l0": (152, 144, 144), "l1": (224, 224, 216),
}

body = Mat(["b0", "b1", "b2", "b3"], line="b0", cuts=[0.2, 0.44, 0.7])
body_d = Mat(["b0", "b1", "b2"], line="b0", cuts=[0.4, 0.75])
belly = Mat(["l0", "l1", "wh"], line="l0", cuts=[0.3, 0.85])
web = Mat(["v0", "v1", "v2"], line="v0", cuts=[0.4, 0.7])
rib_m = Mat(["g1", "g2"], line="v0")
throat = Mat(["ink", "v0", "v1"], line="ink", cuts=[0.4, 0.75])
fang_m = Mat(["l0", "l1", "wh"], line="l0", cuts=[0.4, 0.68])
fang2_m = Mat(["v0", "v1", "v2"], line="v0", cuts=[0.4, 0.7])
bark = Mat(["l0", "l1"], line="ink", cuts=[0.6])
leaf = Mat(["f0", "f1"], line="f0", cuts=[0.55])
fig = Mat(["v0", "v1", "v2"], line="v0", cuts=[0.45, 0.8])
water = Mat(["b1", "b2", "b3", "wh"], line="b1", cuts=[0.25, 0.55, 0.8])
glow = Mat(["v1", "g1", "g2"], line="v0", cuts=[0.3, 0.7])

LAYERS = None  # a finishing script may set e.g. {"frill"}; the build leaves it None


def want(name):
    if LAYERS is None or name in LAYERS or name.split(".")[0] in LAYERS:
        return True
    return any(L.startswith(name + ".") for L in LAYERS)


def arc(c, rx, ry, a0, a1, n=None, tilt=0.0):
    """Points on an ellipse around c from angle a0 to a1 (degrees, y down)."""
    n = n or max(6, int(abs(a1 - a0) / 8))
    ct, st = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    out = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((c[0] + x * ct - y * st, c[1] + x * st + y * ct))
    return out


def polar(c, rx, ry, deg):
    a = math.radians(deg)
    return (c[0] + rx * math.cos(a), c[1] + ry * math.sin(a))


# --------------------------------------------------------------------------
# The frill: a palmette of webbed lobes spread behind the head like a frilled
# lizard's, each lobe swept the same way round so the fan turns like a
# pinwheel. Membrane dark at the root, lit through toward the rim, and a
# glowing rib down the middle of every lobe.
# --------------------------------------------------------------------------

def frill(p, F, rx, ry, angs, sweep=14, r0=0.3, group=10, wmul=1.0, pulse=0, dark=(), back=False):
    """Lobes first, then a glowing rib down every lobe, drawn over them all.
    back=True is the frill seen from behind: the membrane in shadow."""
    lobes, pids = [], []
    for i, a in enumerate(angs):
        root = polar(F, rx * r0, ry * r0, a - sweep * 0.7)
        tip = polar(F, rx, ry, a + sweep * 0.3)
        span = math.radians(abs(angs[1] - angs[0])) * (rx + ry) / 2 * 0.74
        w = span * 1.1 * wmul
        g = group + i
        dk = i in dark or back
        pid = p.poly(lens_pts(root, tip, w, bend=-1.8, fat=0.62, n=18), web, group=g, flat=0 if dk else 1)
        pids.append(pid)
        if p.big:
            # the outer membrane lit through, the root in the head's shadow
            pids.append(p.poly(lens_pts(polar(F, rx * 0.64, ry * 0.64, a + sweep * 0.0), tip, w * 0.92, bend=-0.8,
                                        fat=0.34, n=12), web, group=g, clip=[pid], flat=1 if dk else 2))
            pids.append(p.poly(lens_pts(root, polar(F, rx * 0.52, ry * 0.52, a - sweep * 0.3), w * 0.9, bend=-0.6,
                                        fat=0.7), web, group=g, clip=[pid], flat=0))
        lobes.append((root, tip, a))
    if p.big:
        for i, (root, tip, a) in enumerate(lobes):
            rib = bez(polar(F, rx * 0.36, ry * 0.36, a - sweep * 0.62), polar(F, rx * 0.66, ry * 0.66, a - sweep * 0.1),
                      polar(F, rx * 0.95, ry * 0.95, a + sweep * 0.26), n=14)
            p.limb(rib, 1.15, 0.95, rib_m, group=500 + i, clip=pids, flat=0, noline=True)
            k = (i + pulse) % 3
            p.limb(rib[3 + 2 * k:6 + 2 * k], 1.15, 1.0, rib_m, group=500 + i, clip=pids, flat=1, noline=True)
    return lobes


def fig_leaf(p, base, ang, size, group, lobes=3):
    """A fig leaf: palmate, three deep lobes (five on big leaves) fanned from
    the stalk, the middle one longest."""
    spread = [0.0, -48.0, 48.0, -88.0, 88.0][:lobes]
    for k, da in enumerate(spread):
        L = size * (1.0 if k == 0 else (0.8 if k < 3 else 0.55))
        a = math.radians(ang + da)
        tip = (base[0] + math.cos(a) * L, base[1] + math.sin(a) * L)
        p.lens(base, tip, size * (0.62 if k == 0 else 0.5), leaf, bend=0.0, fat=0.58, group=group, bias=0.04 * k)


def fig_tree(p, top, s=1.0, sway=0.0):
    """The fig crown at the end of the tail wood: two branches, leaves, figs."""
    x, y = top
    q = lambda dx, dy: (x + dx * s, y + dy * s)
    p.limb(bez(q(0, 0), q(-4, -4), q(-9.5 + sway, -5.5)), 2.6 * s, 1.6 * s, bark, group=132)
    p.limb(bez(q(0.4, -0.5), q(3, -3.5), q(4 + sway, -7)), 2.4 * s, 1.6 * s, bark, group=133)
    for k, (dx, dy, ang, sz, lb) in enumerate(((-10.5, -5.5, 200, 6.4, 5), (4.5, -7.5, 285, 5.6, 3),
                                               (-5.0, -3.5, 120, 5.0, 3), (5.5, -2.5, 30, 5.2, 3),
                                               (-1.5, 4.0, 160, 4.4, 3))):
        fig_leaf(p, q(dx + sway * (1 if dy < 0 else 0), dy), ang, sz * s, 140 + k, lobes=lb)
    for k, (dx, dy) in enumerate(((-7.0, -1.8), (2.5, 1.6))):
        p.drop(q(dx, dy - 1.8), *q(dx, dy), 1.5 * s, fig, group=150 + k)


def fin(p, pts, h, n, group, lean=0.5, side=None):
    """A dorsal sail along pts, the frill running on down the spine: n
    pointed lobes of violet membrane, a glowing rib in each. side forces
    the normal (+1/-1); by default the sail stands up."""
    pids, ribs = [], []
    for k in range(n):
        t = (k + 0.5) / n
        i = min(int(t * (len(pts) - 1)), len(pts) - 2)
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy) or 1.0
        nx, ny = dy / d, -dx / d
        if (side is None and ny > 0) or (side is not None and side < 0):
            nx, ny = -nx, -ny
        hh = h * (1 - 0.5 * abs(t - 0.4))
        tip = (x0 + nx * hh + dx / d * hh * lean, y0 + ny * hh + dy / d * hh * lean)
        pid = p.lens((x0, y0), tip, h * 0.85, web, bend=-0.6, fat=0.3, group=group + k, flat=1)
        pids.append(pid)
        if p.big:
            pids.append(p.lens(((x0 + tip[0]) / 2, (y0 + tip[1]) / 2), tip, h * 0.6, web, bend=-0.3, fat=0.3,
                               group=group + k, clip=[pid], flat=2))
        ribs.append(((x0, y0), tip))
    if p.big:
        for k, (a, b) in enumerate(ribs):
            p.limb([a, b], 1.1, 0.9, rib_m, group=group + 40 + k, clip=pids, flat=0, noline=True)


# --------------------------------------------------------------------------
# The maw, the jaws and the eyes
# --------------------------------------------------------------------------

def fang_ring(p, c, rx, ry, n, length, width, phase, twist, mat, group, tilt=-6.0, vary=0.0):
    """n fangs on an ellipse, each aimed at the centre and hooked round the
    same way, the top and bottom ones longest."""
    for i in range(n):
        a = 360.0 * (i + phase) / n
        base = arc(c, rx, ry, a, a, n=1, tilt=tilt)[0]
        dx, dy = c[0] - base[0], c[1] - base[1]
        d = math.hypot(dx, dy) or 1.0
        L = min(length * (1 + vary * (abs(math.sin(math.radians(a))) - 0.4)), d - 0.6)
        ang = math.atan2(dy, dx) + math.radians(twist)
        tip = (base[0] + math.cos(ang) * L, base[1] + math.sin(ang) * L)
        p.poly(lens_pts(base, tip, width, bend=-0.3 * L, fat=0.16, n=8), mat, group=group + i, noline=True)


def maw(p, M, rx, ry, phase=0, tilt=-6.0):
    gp = 0.5 * phase
    p.blob(M[0], M[1], rx, ry, throat, ang=tilt, group=300, flat=2)
    if not p.big:
        p.blob(M[0] + 1.0, M[1], rx * 0.5, ry * 0.5, throat, group=300, flat=0)
        p.blob(M[0] + 1.0, M[1], rx * 0.25, ry * 0.25, glow, group=301, flat=2, noline=True)
        return
    # deeper is darker; each ring sits further back toward the neck
    c2, c3 = (M[0] + 1.0, M[1] + 0.3), (M[0] + 1.8, M[1] + 0.5)
    p.blob(c2[0], c2[1], rx * 0.7, ry * 0.7, throat, ang=tilt, group=300, flat=1)
    p.blob(c3[0], c3[1], rx * 0.42, ry * 0.42, throat, ang=tilt, group=300, flat=0)
    p.blob(c3[0] + 0.5, c3[1], 2.6 + gp, 2.4 + gp, glow, group=301, flat=1, noline=True)
    p.blob(c3[0] + 0.5, c3[1], 1.2 + gp, 1.1 + gp, glow, group=301, flat=2, noline=True)
    fang_ring(p, c3, rx * 0.36, ry * 0.36, 6, 2.2, 1.6, 0.3, 34, fang2_m, 350, tilt=tilt)
    fang_ring(p, c2, rx * 0.62, ry * 0.62, 8, 3.2, 2.2, 0.55, 32, fang2_m, 330, tilt=tilt, vary=0.3)
    fang_ring(p, M, rx * 0.94, ry * 0.94, 10, 5.4, 3.2, 0.0, 30, fang_m, 310, tilt=tilt, vary=0.5)


def jaw_lo(p, M, rx, ry, drop=0.0, tilt=-6.0):
    """Lower jaw: an indigo lip round the bottom of the maw, the chin's pale
    plates beneath."""
    x, y = M
    y += drop
    ring = arc((x, y), rx + 3.0, ry + 3.2, -4, 184, tilt=tilt) + arc((x, y), rx - 1.0, ry - 1.0, 184, -4, tilt=tilt)
    p.poly(ring, body, group=220, bias=0.06)
    p.poly(arc((x - 0.6, y + 0.6), rx + 2.0, ry + 3.4, 40, 140, tilt=tilt) +
           arc((x - 0.6, y + 0.6), rx - 0.5, ry + 0.6, 140, 40, tilt=tilt), belly, group=221, bias=-0.04)


def jaw_up(p, M, rx, ry, up=0.0, tilt=-6.0):
    """Upper jaw: a heavy indigo arch over the maw, the snout bridge over the
    opening, the forehead domed behind it, a brow horn sweeping back from
    over each eye into the frill, the near cheek rounded under the eye."""
    x, y = M
    dx, dy = x - 23.5, y - 31.0 + up
    # far brow horn and the narrow far cheek
    p.lens((14.0 + dx, 16.5 + dy), (5.0 + dx, 10.5 + dy), 3.8, body, bend=0.8, fat=0.3, group=200, bias=0.04)
    p.blob(10.6 + dx, 26.0 + dy, 3.4, 8.6, body, ang=8, group=201, bias=0.04)
    # near cheek: the jaw muscle, rounded, in the shade
    p.blob(38.2 + dx, 26.0 + dy, 5.8, 9.6, body, ang=-10, group=202, bias=0.06)
    # the arch over the maw, and the forehead dome behind the snout
    ring = arc((x, y + up), rx + 3.0, ry + 3.4, 176, 364, tilt=tilt) + arc((x, y + up), rx - 1.0, ry - 1.0, 364, 176,
                                                                           tilt=tilt)
    p.polys([ring, [(a + dx, b + dy) for a, b in arc((23.0, 16.6), 9.8, 5.6, 170, 370)]], body, group=210)
    # near brow horn over everything
    p.lens((28.0 + dx, 16.0 + dy), (46.0 + dx, 5.4 + dy), 5.6, body, bend=1.5, fat=0.26, group=211)
    up_i = int(round(up))
    if not p.big:
        p.px(x + 9, y - 13 + up_i, "g2")
        return
    X, Y = p.ipt(x + 6, y - 15 + up_i)
    p.fig.patch(X, Y, [
        "..#######",
        ".##GGWG#g",
        "#gGGGgg#g",
        "#ggg##g#.",
        ".###..#..",
    ], {"#": "ink", "g": "g1", "G": "g2", "W": "wh"})
    X, Y = p.ipt(x - 15, y - 13 + up_i)
    p.fig.patch(X, Y, [
        "####.",
        "#GG#g",
        ".#gG#",
        "..##.",
    ], {"#": "ink", "g": "g1", "G": "g2"})


# --------------------------------------------------------------------------
# Battle front
# --------------------------------------------------------------------------

FRILL_ANGS = [152 + 20 * i for i in range(13)]

# front geometry, shared with the finishing script: maw centre and radii,
# frill centre and radii, by phase
FRONT = {
    0: dict(M=(23.5, 31.0), mr=(11.2, 10.4), F=(30.0, 25.5), fr=(28.4, 23.8)),
    1: dict(M=(23.5, 31.0), mr=(11.8, 11.4), F=(30.0, 25.5), fr=(29.6, 24.6)),
}


# the body's tubes on the front: (centreline, width at start, width at end)
FRONT_TUBES = {
    "back": (bez3((10.0, 50.0), (6.5, 41.0), (14.0, 38.5), (24.0, 41.0)), 10.0, 9.0),
    "tail": (bez3((47.0, 46.0), (56.0, 47.5), (62.0, 42.0), (58.0, 30.0)), 10.0, 6.0),
    "neck": (bez3((44.0, 52.0), (46.5, 44.0), (42.0, 36.0), (35.0, 30.0)), 12.0, 15.0),
    "front": (bez3((45.0, 50.0), (40.0, 60.0), (16.0, 60.5), (9.0, 49.5)), 11.0, 10.0),
}


def _front_body(p, phase):
    T = FRONT_TUBES
    # the back of the loop: up out of the water at the left, behind the neck,
    # and out again at the right as the tail
    if want("body.back"):
        fin(p, T["back"][0][1:13], 9.0, 3, 60, lean=0.45, side=1)
        p.limb(T["back"][0], T["back"][1], T["back"][2], body_d, group=100)
    if want("body.tail"):
        fin(p, T["tail"][0][2:12], 4.0, 3, 70, lean=0.5)
        p.limb(T["tail"][0], T["tail"][1], T["tail"][2], body, group=101)
        p.limb(T["tail"][0][:9], 3.0, 2.4, belly, group=101, bias=-0.06)
    # neck, out of the coil up behind the head, belly plates toward us
    if want("body.neck"):
        p.limb(T["neck"][0], T["neck"][1], T["neck"][2], body, group=110)
        p.limb(bez3((39.0, 53.0), (40.0, 46.0), (35.0, 41.0), (28.0, 38.0)), 6.0, 8.0, belly, group=110, bias=-0.08)
    # the front of the loop, swinging round toward us along the bottom
    if want("body.front"):
        p.limb(T["front"][0], T["front"][1], T["front"][2], body, group=120)
        p.limb(bez3((44.0, 53.5), (39.0, 61.5), (17.0, 62.0), (10.0, 52.5)), 4.2, 3.6, belly, group=120, bias=-0.06)
    # fig wood at the tail tip
    if want("body.wood"):
        wood = bez3((58.0, 31.0), (55.0, 24), (59.5, 18), (56.0, 11.5))
        p.limb(wood, 5.2, 3.0, bark, group=131)
        fig_tree(p, (56.0, 11.0), sway=0.5 * phase)


def _front(p, phase):
    g = FRONT[phase]
    M, (mrx, mry), F, (frx, fry) = g["M"], g["mr"], g["F"], g["fr"]
    if want("frill"):
        frill(p, F, frx, fry, FRILL_ANGS, wmul=1.0 + 0.04 * phase, pulse=phase, dark=(11, 12))
    if want("body"):
        _front_body(p, phase)
    if want("jaw_lo"):
        jaw_lo(p, M, 11.2, 10.4, drop=float(phase))
    if want("jaw_up"):
        jaw_up(p, M, 11.2, 10.4, up=-1.0 * phase)
    if want("maw"):
        maw(p, M, mrx, mry, phase)


# --------------------------------------------------------------------------
# Battle back: over the shoulder. The back of the frill fans out at the
# left, the coils fill the bottom, and the head turns right into profile,
# jaws gaping at the foe with the fang rows going down the throat.
# --------------------------------------------------------------------------

BACK_FRILL_ANGS = [96 + 20 * i for i in range(13)]

BACK_TUBES = {
    "coil": (bez3((24.0, 55.0), (40.0, 45.0), (54.0, 49.0), (53.5, 67.0)), 14.0, 15.0),
    "neck": (bez3((22.0, 67.0), (17.0, 50.0), (26.0, 38.0), (36.0, 30.0)), 18.0, 14.0),
}


def _back(p, phase):
    ph = phase
    T = BACK_TUBES
    if want("frill"):
        p.blob(29.0, 26.0, 9.0, 9.0, web, group=9, flat=0)
        frill(p, (28.0, 25.5), 25.5 + ph, 23.4 + ph * 0.6, BACK_FRILL_ANGS, sweep=-14, back=True, pulse=ph)
    if want("body.coil"):
        fin(p, T["coil"][0][3:12], 5.0, 4, 60, lean=0.35)
        p.limb(T["coil"][0], T["coil"][1], T["coil"][2], body, group=100)
    if want("body.neck"):
        fin(p, T["neck"][0][3:15], 13.0, 4, 70, lean=0.25, side=1)
        p.limb(T["neck"][0], T["neck"][1], T["neck"][2], body, group=110)
    if want("jaw_lo"):
        # lower jaw, dropped open toward the foe, its pale underside below
        d = ph
        p.blob(37.5, 31.0, 6.0, 6.4, body, group=195, bias=0.04)
        p.poly([(37, 31.0), (45, 34.0 + d), (52, 37.0 + d), (58, 40.0 + d), (61.8, 42.6 + d), (60.4, 45.4 + d),
                (55, 46.6 + d), (48, 45.4 + d), (41, 42.8), (34.5, 38.5)], body, group=200)
        p.poly([(39, 41.6), (47, 44.4 + d), (55, 46.0 + d), (60.6, 45.0 + d), (57, 47.6 + d), (49, 47.6 + d),
                (42, 45.6), (37, 42.8)], belly, group=201)
    if want("maw"):
        d = ph
        p.poly([(40, 25.0 - d), (48, 22.2 - d), (55, 19.8 - d), (61.5, 18.6 - d), (61.8, 42.0 + d), (55, 38.6 + d),
                (48, 35.4 + d), (41.5, 32.0)], throat, group=300, flat=1)
        p.blob(43.0, 28.6, 2.8, 3.2, glow, group=301, flat=1, noline=True)
        p.blob(42.8, 28.6, 1.3, 1.5, glow, group=301, flat=2, noline=True)
    if want("jaw_up"):
        # skull and upper jaw thrown up toward the foe, a brow horn swept back
        up = -ph
        p.blob(36.0, 22.0, 9.0, 10.0, body, group=205)
        p.poly([(36, 14.0 + up), (43, 10.6 + up), (50, 9.6 + up), (56, 10.2 + up), (60.6, 12.0 + up), (62.4, 14.4 + up),
                (61.8, 17.6 + up), (56, 19.4 + up), (49, 21.8 + up), (43, 24.6 + up), (37.5, 27.0)],
               body, group=210)
        p.lens((45.5, 15.0 + up), (28.0, 4.2 + up), 6.0, body, bend=-1.6, fat=0.3, group=211)
        if p.big:
            X, Y = p.ipt(41, 15 + up)
            p.fig.patch(X, Y, [
                ".#######",
                "##GGWG#g",
                ".#gGg#g#",
                "..#####.",
            ], {"#": "ink", "g": "g1", "G": "g2", "W": "wh"})


# --------------------------------------------------------------------------
# Follower and icon views
# --------------------------------------------------------------------------

def _down(p, phase):
    """Walking toward the camera: coiled, frill spread, maw open at us."""
    ph = phase
    bob = ph * 0.8
    F = (32.0, 28.0 + bob)
    frill(p, F, 26.0, 21.0 + ph * 0.6, [150 + 30 * i for i in range(9)], sweep=6, r0=0.22)
    C = (32.0, 50.0)
    p.limb(arc(C, 18.0, 6.0, 180, 360), 9.0, 9.0, body_d, group=100)
    p.limb(arc((C[0], C[1] + 2.0), 19.0, 6.4, 0, 180), 10.0, 10.0, body, group=120)
    p.limb(arc((C[0], C[1] + 4.0), 17.0, 5.0, 20, 160), 3.0, 3.0, belly, group=121)
    # the fig tail rising at one side
    p.limb(bez3((48.0, 50.0), (56.0, 46.0), (56.0, 38.0), (53.0, 32.0)), 6.0, 3.6, body, group=125)
    for k, (a, b, w, bd) in enumerate((((53, 32), (49.0, 25.5), 6.0, 1), ((53, 32), (58.5, 26.5), 6.0, -1))):
        p.lens(a, b, w, leaf, bend=bd, group=126 + k)
    # head: brow horns, jaw ring, pale chin, fanged maw, glow, eyes
    M = (32.0, 33.0 + bob)
    p.lens((26.0, 23.0 + bob), (15.0, 14.5 + bob), 5.0, body, bend=-0.8, fat=0.3, group=198)
    p.lens((38.0, 23.0 + bob), (49.0, 14.5 + bob), 5.0, body, bend=0.8, fat=0.3, group=199)
    p.blob(M[0], M[1], 14.4, 13.4, body, group=200)
    p.poly(arc((M[0], M[1] + 2.0), 12.6, 11.4, 30, 150), belly, group=201)
    p.blob(M[0], M[1] + 1.0, 10.0, 9.4 + ph * 0.5, throat, group=300, flat=0)
    p.blob(M[0], M[1] + 1.0, 3.4 + ph * 0.6, 3.2 + ph * 0.6, glow, group=301, flat=1, noline=True)
    p.blob(M[0], M[1] + 1.0, 1.4, 1.4, glow, group=301, flat=2, noline=True)
    fang_ring(p, (M[0], M[1] + 1.0), 9.6, 9.0 + ph * 0.5, 6, 6.0, 5.0, 0.1, 36, Mat(["wh"]), 310, tilt=0)
    for sx in (-1, 1):
        p.blob(M[0] + sx * 9.0, M[1] - 10.0, 3.4, 2.4, Mat(["g2"]), group=320 + sx, flat=0)


def _up(p, phase):
    """Walking away: the back of the frill fanned round the back of the head,
    the coil beneath, the fig tail rising at one side."""
    ph = phase
    bob = ph * 0.6
    # the fig tail behind the coil at the right
    p.limb(bez3((44.0, 50.0), (55.0, 48.0), (56.0, 36.0), (52.0, 27.0)), 7.0, 4.0, body, group=90)
    p.limb(bez((52.0, 27.5), (50.0, 22.0), (53.0, 16.5)), 3.6, 2.4, bark, group=91)
    for k, (a, b, w, bd) in enumerate((((53, 17), (47.5, 12.0), 7.0, 1), ((53, 17), (59.0, 12.0), 7.0, -1),
                                      ((53, 17), (53.5, 9.5), 6.0, 0))):
        p.lens(a, b, w, leaf, bend=bd, group=92 + k)
    # the frill from behind, dark, ribs glowing through, fanned down to the coil
    frill(p, (31.0, 31.0 + bob), 23.0, 20.0, [128 + 22 * i for i in range(14)], sweep=0, back=True, r0=0.2)
    # the coil, the thick neck rising out of it, the back of the head
    C = (31.0, 50.0)
    p.limb(arc(C, 18.0, 6.0, 180, 360), 9.0, 9.0, body_d, group=100)
    p.limb(bez3((32.0, 50.0 + bob), (31.0, 45.0), (31.5, 40.0), (31.0, 34.0 + bob)), 15.0, 13.0, body, group=110)
    p.limb(arc((C[0], C[1] + 2.0), 19.0, 6.4, 0, 180), 10.0, 10.0, body, group=120)
    p.blob(31.0, 31.0 + bob, 9.0, 8.0, body, group=200)
    # the brow horns from behind, swept out over the frill
    p.lens((26.0, 27.0 + bob), (16.5, 18.0 + bob), 4.4, body, bend=0.6, fat=0.3, group=201)
    p.lens((36.0, 27.0 + bob), (45.5, 18.0 + bob), 4.4, body, bend=-0.6, fat=0.3, group=202)


def _icon(p, phase):
    """Party icon: the frilled head and its maw, big and simple, on a coil."""
    ph = phase
    F = (31.0, 25.0)
    frill(p, F, 27.0 + ph, 22.0 + ph, [150 + 26 * i for i in range(10)], sweep=8, r0=0.25)
    p.limb(bez3((44.0, 50.0), (56.0, 50.0), (60.0, 38.0), (55.0, 28.0)), 10.0, 6.0, body, group=100)
    for k, (a, b, w, bd) in enumerate((((55, 28), (49.0, 19.0), 9.0, 1), ((55, 28), (62.0, 20.0), 9.0, -1))):
        p.lens(a, b, w, leaf, bend=bd, group=101 + k)
    p.limb(bez3((46.0, 50.0), (42.0, 60.0), (16.0, 60.0), (9.0, 48.0)), 13.0, 11.0, body, group=110)
    p.limb(bez3((45.0, 54.0), (40.0, 63.0), (17.0, 63.0), (10.0, 52.0)), 4.6, 4.0, belly, group=110)
    M = (27.0, 29.0)
    # brow horns, the jaw ring, the pale chin, the maw, the glow
    p.lens((32.0, 18.0), (47.0, 7.0), 7.0, body, bend=1.4, fat=0.3, group=199)
    p.lens((21.0, 18.0), (9.0, 9.0), 6.0, body, bend=-1.2, fat=0.3, group=198)
    p.blob(M[0], M[1], 16.0, 15.0, body, group=200)
    p.poly(arc((M[0], M[1] + 2.0), 14.0, 12.4, 30, 150), belly, group=201)
    p.blob(M[0], M[1] + 0.5, 11.4, 10.8, throat, group=300, flat=0)
    p.blob(M[0] + 1.0, M[1] + 1.0, 3.8 + ph * 0.6, 3.6 + ph * 0.6, glow, group=302, flat=1, noline=True)
    p.blob(M[0] + 1.0, M[1] + 1.0, 1.8 + ph * 0.4, 1.8 + ph * 0.4, glow, group=302, flat=2, noline=True)
    fang_ring(p, (M[0], M[1] + 0.5), 10.6, 10.0, 7, 6.0, 6.0, 0.1, 34, Mat(["wh"]), 320, tilt=0)
    for ex, ey in ((M[0] - 10.0, M[1] - 11.5), (M[0] + 9.0, M[1] - 12.5)):
        p.blob(ex, ey, 3.4, 2.4, Mat(["g2"]), group=330, flat=0)


def trybdis(p, view, phase):
    if view == "front":
        _front(p, phase)
    elif view == "side":
        _front(p, phase)
    elif view == "back":
        _back(p, phase)
    elif view == "down":
        _down(p, phase)
    elif view == "up":
        _up(p, phase)
    elif view == "icon":
        _icon(p, phase)


MONS = [
    # icon palette 4 keeps the frill magenta against the blue body
    Mon("Trybdis", COLORS, SHINY, trybdis, foot="blank", follow=27, icon_pal=4),
]
