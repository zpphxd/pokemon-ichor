"""Narcissus line: Narcibulb, Narcisheen (Kythera Isle). Narcissus, who fell in
love with his own reflection in a spring and became the flower that bends
over the water (Ovid, Metamorphoses 3)."""
from mon_lib import C, Mat, Mon, bez, bez3, ellipse_pts

INK = C.ink

# --------------------------------------------------------------------------
# Narcibulb, the spring bulb
# --------------------------------------------------------------------------

NARCIBULB_COLORS = [
    ("ink", INK),
    # the marble-white bulb, shadowed a cool lilac-gray
    ("bl0", (144, 136, 152)), ("bl1", (192, 184, 192)), ("bl2", (232, 224, 224)), ("bl3", (248, 248, 240)),
    # limestone papery skin
    ("pp0", (120, 88, 56)), ("pp1", (176, 144, 96)), ("pp2", (208, 184, 136)), ("pp3", (232, 216, 176)),
    # the olive shoot
    ("ol0", (48, 64, 32)), ("ol1", (88, 112, 48)), ("ol2", (136, 160, 72)), ("ol3", (184, 200, 112)),
    # sleepy pink cheeks
    ("blush", (232, 160, 160)),
]
NARCIBULB_SHINY = {
    # the bulb turns a pale sun-gold
    "bl0": (184, 136, 64), "bl1": (224, 184, 96), "bl2": (248, 224, 144), "bl3": (248, 240, 200),
}

n_bulb = Mat(["bl0", "bl1", "bl2", "bl3"], line="bl0", cuts=[0.2, 0.46, 0.72])
n_skin = Mat(["pp0", "pp1", "pp2", "pp3"], line="pp0", cuts=[0.2, 0.46, 0.72])
n_root = Mat(["pp0", "pp1"], line="pp0", cuts=[0.55])
n_leaf = Mat(["ol0", "ol1", "ol2", "ol3"], line="ol0", cuts=[0.2, 0.46, 0.74])


def _bulb_body(p, cx, cy, s=1.0, L=0, squash=0.0):
    """A plump onion-shaped bulb: a round belly tapering to a neck on top."""
    r = 11 * s
    body = p.blob(cx, cy, r, (9.6 - squash) * s, n_bulb, group=1)
    p.poly([(cx - 5.6 * s, cy - 6 * s), (cx - 2.2 * s, cy - 12.5 * s - L), (cx + 1.6 * s, cy - 14 * s - L),
            (cx + 4.6 * s, cy - 11 * s - L), (cx + 7 * s, cy - 6 * s)], n_bulb, group=1)
    return body


def narcibulb(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        step = view == "side" and phase == 1
        cx, cy = 32, 48.5
        # the green shoot, rising from the neck and leaning forward
        p.lens((33.5, 37 - L), (23.5 - L, 20 - 2 * L), 5.0, n_leaf, bend=2.6, fat=0.4, group=20)
        # roots: little feet under the basal plate
        for fx, fy, tx in ((25, 56.5, 23), (30, 57.5, 29.5), (36, 57.5, 37 + step), (40, 55.5, 42)):
            p.limb([(fx, fy), (tx, 59.5 - (1 if step and fx == 30 else 0))], 2.6, 1.8, n_root, group=30)
        # the bulb
        _bulb_body(p, cx, cy, L=L)
        # papery skin: a coat peeling around the back, and the tuft on top
        p.poly([(38.5, 39), (42.5, 44), (43.6, 50), (41, 56), (36, 58.4), (39.5, 51), (39.5, 45)], n_skin, group=10)
        p.poly([(30, 36 - L), (33.8, 27.5 - L), (36.5, 25.8 - L), (35.4, 29.5 - L), (38.4, 30.5 - L),
                (36, 33 - L), (35.2, 36.8 - L)], n_skin, group=11)
        # the basal plate
        p.blob(32, 57.2, 7.6, 1.8, n_skin, group=12, bias=0.2)
        if p.big:
            # sleepy, half-shut eyes looking down and away
            p.patch(23, 45, ["1111", "1222", ".11."], {"1": "ink", "2": "ink"})
            p.patch(30, 45, ["1111", "2221", ".11."], {"1": "ink", "2": "ink"})
            p.pxs([(23, 48), (24, 48), (32, 48), (33, 48)], "blush")
            p.stroke([(27, 50), (28, 50)], "bl0")
            # the shoot's midrib, and the fine lines of the bulb's scales
            p.stroke([(32.5, 35 - L), (29, 28 - L), (26, 23 - 2 * L)], "ol1")
            p.stroke([(36, 40), (37.5, 46), (37, 53)], "bl1")
            p.stroke([(29, 39 - L), (27.5, 42)], "bl1")
        else:
            p.px(25, 46, "ink")
            p.px(31, 46, "ink")
        return

    if view == "back":
        # over the shoulder: the papery coat over its back, the shoot and the
        # tuft above, one sleepy eye turned right, cropped by the frame
        cx, cy = 31, 56
        p.lens((32, 39), (23, 19), 5.8, n_leaf, bend=2.4, fat=0.4, group=20)
        _bulb_body(p, cx, cy, s=1.25)
        p.poly([(17, 52), (19, 46), (23, 41), (28, 38), (27, 46), (25, 56), (23, 64), (15, 64), (15, 58)], n_skin, group=10)
        p.poly([(29, 41), (32.5, 30), (35.5, 27.5), (34.5, 32), (38.5, 33), (36, 37), (35.5, 42)], n_skin, group=11)
        if p.big:
            p.patch(38, 50, ["11111", "22221", ".111."], {"1": "ink", "2": "ink"})
            p.pxs([(39, 54), (40, 54), (41, 54)], "blush")
            p.stroke([(32, 37), (27, 26)], "ol1")
        return

    if view in ("down", "up"):
        # the follower walks with its eyes on the ground
        st = phase
        for fx, tx in ((26, 24), (30.5, 30 - st), (34, 34.5 + st), (38, 40)):
            p.limb([(fx, 56), (tx, 59.5)], 2.6, 1.8, n_root, group=30)
        _bulb_body(p, 32, 48)
        p.lens((32, 36), (30, 22 + st), 4.6, n_leaf, bend=0.8, fat=0.42, group=20)
        p.poly([(29, 36), (31, 27), (33.5, 25.5), (33, 29), (36, 30), (34.5, 34), (34.5, 37)], n_skin, group=11)
        if view == "down":
            p.patch(25, 47, ["1111", ".11."], {"1": "ink"})
            p.patch(35, 47, ["1111", ".11."], {"1": "ink"})
            p.pxs([(25, 49), (26, 49), (37, 49), (38, 49)], "blush")
        else:
            p.poly([(23, 44), (27, 38), (32, 37), (37, 38), (41, 44), (42, 52), (38, 57), (26, 57), (22, 52)],
                   n_skin, group=10)
        return


# --------------------------------------------------------------------------
# Narcisheen, the narcissus bent over its spring
# --------------------------------------------------------------------------

import math  # noqa: E402

NARCISHEEN_COLORS = [
    ("ink", INK),
    # marble-white petals
    ("pt0", (152, 152, 168)), ("pt1", (200, 200, 208)), ("pt2", (232, 232, 232)), ("pt3", (248, 248, 240)),
    # the sun-gold trumpet, its rim burnt orange
    ("gd0", (192, 96, 24)), ("gd1", (232, 160, 40)), ("gd2", (248, 216, 80)),
    # olive stem and leaves
    ("ol0", (40, 64, 32)), ("ol1", (80, 112, 48)), ("ol2", (128, 160, 64)), ("ol3", (184, 200, 112)),
    # Aegean-blue water
    ("wt0", (24, 56, 120)), ("wt1", (56, 112, 184)), ("wt2", (136, 184, 232)),
]
NARCISHEEN_SHINY = {
    # petals sun-gold like a wild daffodil's, and a white trumpet
    "pt0": (200, 136, 32), "pt1": (232, 184, 56), "pt2": (248, 216, 96), "pt3": (248, 240, 168),
    "gd0": (152, 144, 160), "gd1": (208, 208, 216), "gd2": (248, 248, 240),
}

s_petal = Mat(["pt0", "pt1", "pt2", "pt3"], line="pt0", cuts=[0.2, 0.46, 0.72])
s_gold = Mat(["gd0", "gd1", "gd2"], line="gd0", cuts=[0.36, 0.66])
s_leaf = Mat(["ol0", "ol1", "ol2", "ol3"], line="ol0", cuts=[0.2, 0.46, 0.74])
s_water = Mat(["wt0", "wt1", "wt2"], line="wt0", cuts=[0.3, 0.66])
s_spathe = Mat(["pt0", "pt1", "pt2"], line="pt0", cuts=[0.4, 0.7])


def _flower(p, cx, cy, r, tilt=0.0, rot=0.0, reflect=False):
    """The narcissus head: six petals in a star round a gold trumpet, seen at
    an angle (tilt squashes it toward its facing). rot turns the star."""
    for k in range(6):
        a = math.radians(rot + 60 * k)
        tip = (cx + r * math.cos(a), cy + r * math.sin(a) * (1 - tilt))
        base = (cx + 1.2 * math.cos(a), cy + 1.2 * math.sin(a) * (1 - tilt))
        back = math.sin(a) < -0.2
        p.lens(base, tip, r * 0.78, s_petal, fat=0.55, bias=0.12 if back else 0.0, group=40 + k)
    p.blob(cx, cy, r * 0.42, r * 0.42 * (1 - tilt * 0.6), s_gold, group=50)
    p.blob(cx - r * 0.06, cy - r * 0.02, r * 0.3, r * 0.3 * (1 - tilt * 0.6), s_gold, group=51, bias=0.25)


def _nodding(p, cx, cy, r, fx, fy, k=0.55, rot=8.0, cup=5.4, L=0):
    """A nodding narcissus: the petal star seen at an angle, its gold trumpet
    pointing along (fx, fy) with its face, a disc ringed in burnt orange, turned
    the same way. k foreshortens the star along that direction."""
    n = math.hypot(fx, fy)
    fx, fy = fx / n, fy / n
    ux, uy = -fy, fx                                # across the face
    petals = []
    for j in range(6):
        a = math.radians(rot + 60 * j)
        dx = math.cos(a) * ux + math.sin(a) * fx * k
        dy = math.cos(a) * uy + math.sin(a) * fy * k
        petals.append((math.sin(a), dx, dy))
    for sa, dx, dy in sorted(petals):
        tip = (cx + r * dx, cy + r * dy)
        base = (cx + 1.0 * dx, cy + 1.0 * dy)
        w = r * (0.66 if sa >= 0 else 0.56)
        p.lens(base, tip, w, s_petal, fat=0.48, bias=0.2 if sa < 0 else -0.05, group=40)
    # the trumpet's side, then its face: a gold disc ringed burnt orange
    ex, ey = cx + cup * fx, cy + cup * fy
    p.limb([(cx, cy), (ex, ey)], r * 0.5, r * 0.62, s_gold, group=50, bias=0.2)
    ang = math.degrees(math.atan2(uy, ux))
    p.poly(ellipse_pts(ex, ey, r * 0.44, r * 0.3, ang=ang), Mat(["gd0"]), group=51)
    p.poly(ellipse_pts(ex + 0.3 * fx, ey + 0.3 * fy, r * 0.36, r * 0.22, ang=ang), s_gold, group=52, bias=-0.15)
    return ex, ey


def narcisheen(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        # the pool at its feet
        p.blob(29, 56.5, 22, 4.8, s_water, group=1, bias=-0.1)
        # long strap leaves rising from the base, one bowed toward the water
        p.lens((43, 55), (54, 26), 5.2, s_leaf, bend=-3.0, fat=0.35, group=10, bias=0.15)
        p.lens((44, 55), (50, 40), 4.0, s_leaf, bend=-1.0, fat=0.35, group=12, bias=0.25)
        p.lens((41, 55), (30, 39 - L), 4.8, s_leaf, bend=2.0, fat=0.35, group=11)
        # the stem, rising and bowing over the water
        p.limb(bez3((42, 55), (43, 34), (44, 13), (34, 12 - L), n=24), 4.2, 3.0, s_leaf, group=20)
        p.limb(bez((34, 12 - L), (29, 13 - L), (27, 17 - L)), 3.0, 2.6, s_leaf, group=20)
        # the papery spathe at the neck
        p.lens((34, 11 - L), (39.5, 5.5 - L), 3.8, s_spathe, bend=-1.0, group=21)
        # root feet standing in the pool
        for fx, tx in ((39, 37), (42, 42), (45, 47.5)):
            p.limb([(fx, 55), (tx, 59)], 2.8, 2.0, s_leaf, group=30)
        # the flower, nodding over the water, its face turned down to it
        fx_, fy_ = _nodding(p, 24, 23 - L, 13.5, -0.62, 0.78, k=0.55, rot=8, cup=5.6)
        if p.big:
            # closed, contented eyes on the trumpet
            ex, ey = int(fx_), int(fy_)
            p.pxs([(ex - 4, ey - 2), (ex - 3, ey - 1), (ex - 2, ey - 1)], "ink")
            p.pxs([(ex + 1, ey + 1), (ex + 2, ey + 2), (ex + 3, ey + 2)], "ink")
            # its face drawn in the water below
            p.blob(17, 56.4, 6.8, 2.1, Mat(["wt2", "pt1"], cuts=[0.55]), group=2, noline=True, nooutline=True)
            p.blob(17, 56.4, 2.8, 1.2, Mat(["gd1", "gd2"], cuts=[0.5]), group=3, noline=True, nooutline=True)
        return

    if view == "back":
        # over the shoulder: the bowed neck arching away to the right, the
        # flower hanging over the water with its face turned down to it
        p.blob(34, 65, 27, 6, s_water, group=1, bias=-0.1)
        p.lens((20, 66), (8, 34), 7.0, s_leaf, bend=2.6, fat=0.35, group=10, bias=0.1)
        p.lens((25, 66), (21, 44), 5.4, s_leaf, bend=1.0, fat=0.35, group=11, bias=0.2)
        p.limb(bez3((25, 66), (24, 40), (27, 14), (41, 12), n=28), 5.6, 4.0, s_leaf, group=20)
        p.limb(bez((41, 12), (48, 12), (50, 18)), 4.0, 3.4, s_leaf, group=20)
        p.lens((40, 10.5), (34, 3.5), 4.6, s_spathe, bend=1.0, group=21)
        ex, ey = _nodding(p, 48, 28, 15.5, 0.5, 0.86, k=0.5, rot=-20, cup=6.4)
        if p.big:
            p.pxs([(int(ex) - 1, int(ey) - 1), (int(ex), int(ey)), (int(ex) + 1, int(ey))], "ink")
        p.lens((40, 60), (31, 41), 4.6, s_leaf, bend=-1.4, fat=0.35, group=12, bias=0.25)
        return

    if view in ("down", "up"):
        # the follower never looks up at the player
        sw = phase
        p.blob(32, 57, 12, 3, s_water, group=1)
        for fx, tx in ((29, 27 - sw), (32, 32), (35, 37 + sw)):
            p.limb([(fx, 52), (tx, 58)], 2.4, 1.8, s_leaf, group=30)
        p.lens((31, 54), (20, 36), 4.4, s_leaf, bend=1.6, fat=0.35, group=10)
        p.lens((33, 54), (44, 36), 4.4, s_leaf, bend=-1.6, fat=0.35, group=11)
        p.limb([(32, 54), (32, 30), (32, 24)], 3.6, 3, s_leaf, group=20)
        if view == "down":
            _flower(p, 32, 26, 10, tilt=0.55, rot=90)
            p.blob(32, 30, 3.6, 2.6, s_gold, group=50)
        else:
            _flower(p, 32, 24, 10, tilt=0.55, rot=-90)
        return


MONS = [
    Mon("Narcibulb", NARCIBULB_COLORS, NARCIBULB_SHINY, narcibulb, foot="root"),
    Mon("Narcisheen", NARCISHEEN_COLORS, NARCISHEEN_SHINY, narcisheen, foot="root", icon_pal=4),
]
