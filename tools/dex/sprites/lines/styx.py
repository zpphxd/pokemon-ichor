"""Styx line: Stygiad (#134, Ice/Ghost). The Styx, the river of oaths.

Concept C, "The Libation". A Froslass-lineage ice spirit with a pale ice
mask and fin arms. Behind her head a gold libation phiale (the dish oaths
were sealed with) hangs tipped like a halo grown from frost, and from its
low lip one thread of black Styx water spills, falls past her back and
freezes into the black icicle river of her gown. One sleeve-fin is raised
in the oath with frost at its tip. Teal glow, gold rim, black water.
"""
import math

from mon_lib import C, Mat, Mon, bez, bez3, ellipse_pts, lens_pts, ribbon  # noqa: F401

INK = C.ink

COLORS = [
    ("ink", INK),
    # the black water of the Styx and its slate sheen
    ("wa0", (24, 32, 56)), ("wa1", (64, 72, 120)),
    # ice: deep, mid, light, frost, white
    ("ic0", (40, 64, 136)), ("ic1", (88, 136, 208)), ("ic2", (152, 200, 240)), ("fr", (216, 240, 248)),
    ("wh", (248, 248, 248)),
    # the phiale's gold
    ("go0", (136, 80, 32)), ("go1", (208, 144, 48)), ("go2", (248, 208, 96)),
    # Styx teal, the oath's glow
    ("tg0", (32, 144, 144)), ("tg1", (96, 232, 200)),
    # ghost-violet mist
    ("vi0", (96, 80, 168)), ("vi1", (160, 144, 224)),
]
# "The ice turns smoky marble gray and the black water turns silver."
SHINY = {
    "ic0": (72, 72, 88), "ic1": (120, 120, 136), "ic2": (176, 176, 184), "fr": (224, 224, 224),
    "wa0": (120, 128, 144), "wa1": (192, 200, 208),
}

hood_m = Mat(["ic0", "ic1", "ic2", "fr"], line="ic0", cuts=[0.2, 0.45, 0.72])
robe_m = Mat(["ic0", "ic1", "ic2", "fr", "wh"], line="ic0", cuts=[0.14, 0.34, 0.58, 0.8])
mask_m = Mat(["ic2", "fr", "wh"], line="ic1", cuts=[0.42, 0.66])
fin_m = Mat(["ic1", "ic2", "fr", "wh"], line="ic0", cuts=[0.2, 0.46, 0.74])
gold_m = Mat(["go0", "go1", "go2", "wh"], line="go0", cuts=[0.2, 0.48, 0.82])
water_m = Mat(["wa0", "wa1"], line="ink", cuts=[0.3])
mist_m = Mat(["vi0", "vi1"], line="vi0", outline="vi0", cuts=[0.5])
teal_m = Mat(["tg0", "tg1", "fr"], line="tg0", cuts=[0.3, 0.6])


def _rot(pt, c, deg):
    ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    x, y = pt[0] - c[0], pt[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def _dish(p, cx, cy, rx, ry, ang, L=0, wall=(-1.0, -1.6), pool=(3.0, 3.4)):
    """The phiale as a halo, tipped back and to the right: its back wall
    shows as a dark gold crescent past the upper-left rim; inside, the
    concave bowl is shadowed under the far rim and lit toward the near one,
    and a crescent of black Styx water pools in its low side. Returns the
    lip at the low right of the rim, where the water spills."""
    cy -= L
    p.blob(cx + wall[0], cy + wall[1], rx, ry, gold_m, ang=ang, group=70, flat=0)
    p.blob(cx, cy, rx, ry, gold_m, ang=ang, group=71, bias=-0.1)
    ix, iy, irx, iry = cx + 0.3, cy + 0.3, rx - 2.2, ry - 2.2
    op = p.blob(ix, iy, irx, iry, gold_m, ang=ang, group=72, flat=1)
    # the black water: a crescent pooled in the low side
    w = p.blob(ix, iy, irx, iry, water_m, ang=ang, clip=[op], group=73)
    p.blob(ix - pool[0], iy - pool[1], irx, iry, gold_m, ang=ang, clip=[w], group=72, flat=1, noline=True)
    # the lit half of the concave bowl, toward the near rim
    p.poly([(ix - 30, iy + 30), (ix + 30, iy - 30), (ix + 60, iy + 60)], gold_m, clip=[op], group=72, flat=2,
           noline=True)
    pts = ellipse_pts(ix, iy, irx, iry, ang, n=90)
    return max(pts, key=lambda q: q[1] + 0.8 * q[0])


DISH = dict(cx=31.6, cy=13.2, rx=15.4, ry=12.6, ang=-30)


def stygiad(p, view, phase):
    if view in ("front", "side", "icon"):
        _front(p, view, phase)
    elif view == "back":
        _back(p, phase)
    else:
        _follow(p, view, phase)


def _front(p, view, phase):
    L = 1 if (phase == 1 and view == "front") else 0

    def U(pts, d=L):
        return [(x, y - d) for x, y in pts]

    # ---- mist where the hem dissolves
    if p.big:
        for a, b, w, bd in (((10, 58.0), (24, 57.0), 2.4, 0.8), ((38, 57.6), (56, 56.2), 2.6, -0.8),
                            ((20, 59.4), (44, 59.4), 2.0, 0.4)):
            p.lens(a, b, w, mist_m, bend=bd, group=90)

    # ---- the phiale behind the head, tipped low on the right
    lip = _dish(p, L=L, **DISH)

    # ---- the black thread: spilling over the lip, falling past her
    # back, widening as it freezes into the river of her gown
    thread = bez3((lip[0] - 0.6, lip[1] - 0.4), (lip[0] + 3.4, lip[1] + 3.0),
                  (lip[0] + 3.4, lip[1] + 12.0), (49.0, 46.0))
    p.poly(ribbon(thread, lambda t: 3.6 - 0.8 * math.sin(math.pi * min(t, 0.5)) + 3.4 * max(0, t - 0.6)),
           water_m, group=60)

    # ---- the gown: a frozen fall of black water from the waist, sweeping
    # back into a tail where the thread feeds it, icicles along the hem
    gown = (bez3((21.4, 38.4), (17.6, 43.0), (14.8, 48.0), (15.4, 52.6)) +
            bez3((15.4, 52.6), (26.0, 55.6), (42.0, 54.6), (50.0, 51.6)) + [(54.6, 49.6), (57.0, 46.0)] +
            bez3((57.0, 46.0), (52.0, 46.6), (46.0, 45.4), (40.0, 43.6)) +
            bez3((40.0, 43.6), (35.6, 42.0), (32.6, 40.4), (30.8, 37.6)))
    gid = p.poly(gown, water_m, group=50)
    # black icicles hanging from the hem, clear ice at their tips
    for x, y, ln in ((17.4, 52.6, 3.4), (20.6, 53.4, 5.2), (24.0, 54.0, 3.8), (27.4, 54.4, 6.0), (31.0, 54.6, 4.2),
                     (34.6, 54.4, 5.6), (38.2, 54.0, 3.6), (41.6, 53.2, 4.8), (45.0, 52.0, 3.2), (48.4, 50.8, 3.8)):
        p.lens((x, y - 1.0), (x - 0.3, y + ln), 3.0, water_m, fat=0.25, group=52)
    # the ice bodice deepens through the waist into the black water
    p.poly(bez3((10, 47), (22, 42.6), (30, 43.0), (40, 38)) + [(40, 30), (10, 30)], robe_m, clip=[gid], group=51,
           bias=0.1)

    # ---- far arm (her right), raised in the oath: the sleeve falls from
    # the elbow in a long hanging fin; the forearm rises from it, frost at
    # its tip
    sleeve = (U([(16.4, 30.4)]) + bez3(U([(12.0, 27.4)])[0], (7.0, 31.0), (4.6, 39.0), (6.0, 47.0)) +
              bez3((6.0, 47.0), (9.4, 43.0), (13.4, 38.4), (17.6, 35.4)))
    p.limb(U([(21.0, 32.4), (14.4, 31.0)]), 4.6, 4.0, robe_m, group=41)
    p.poly(sleeve, fin_m, group=40)
    p.lens(U([(14.2, 31.0)])[0], (10.6, 3.2 - 2 * L), 5.0, robe_m, bend=0.8, fat=0.36, group=42)

    # ---- torso: a slender ice body under a shawl of frost
    p.blob(26.0, 34.6, 6.6, 4.8, robe_m, group=30)
    p.poly([(20.6, 34), (31.4, 34), (30.0, 40.0), (22.2, 40.0)], robe_m, group=30)
    p.blob(25.6, 31.4, 6.8, 2.2, fin_m, group=31)

    # ---- near arm (her left): a wide sleeve hanging along her side, its
    # point trailing into the black water
    p.poly(bez3((28.6, 31.0), (34.6, 32.0), (38.0, 38.0), (39.0, 47.0)) +
           bez3((39.0, 47.0), (35.0, 43.0), (31.0, 40.6), (28.6, 37.6)), fin_m, group=35)

    # ---- head: a hood of frozen ripples round a pale mask, crest-fins at
    # the temples
    p.lens(U([(31.0, 19.0)])[0], U([(37.6, 26.6)])[0], 4.0, hood_m, bend=1.0, fat=0.26, group=20)
    p.lens(U([(19.2, 15.0)])[0], U([(13.6, 7.4)])[0], 3.8, hood_m, bend=-0.6, fat=0.3, group=21, bias=0.1)
    p.limb(U([(25.2, 26.0)]) + [(25.6, 31.0)], 3.6, 4.2, robe_m, group=22)
    p.blob(25.0, 20.4 - L, 8.4, 8.8, hood_m, group=23)
    p.poly(U(bez3((17.6, 17.8), (20.2, 13.8), (26.8, 13.6), (29.4, 17.8)) +
             bez3((29.4, 17.8), (30.2, 23.2), (27.0, 28.2), (22.8, 28.8)) +
             bez3((22.8, 28.8), (19.2, 27.8), (16.8, 22.8), (17.6, 17.8))), mask_m, group=24)

    if p.big:
        # big simple eyes, a teal glow under a shine
        p.patch(19, 20 - L, ["11....111", "1t....1w1", "tt....tt1", "......tt."],
                {"1": "ink", "t": "tg1", "w": "wh"})
        p.px(10, 4 - 2 * L, "fr")


def _dish_back(p, cx, cy, rx, ry, ang, group=70):
    """The phiale from behind: the convex gold back of the bowl, its rim
    showing past the lower edge, the omphalos a raised boss in the middle."""
    p.blob(cx + 0.8, cy + 1.4, rx, ry, gold_m, ang=ang, group=group, flat=0)
    p.blob(cx, cy, rx, ry, gold_m, ang=ang, group=group + 1)
    if p.big:
        p.blob(cx - 0.6, cy - 0.4, rx * 0.22, ry * 0.24, gold_m, ang=ang, group=group + 2, bias=-0.1)


def _back(p, phase):
    # over the shoulder, about 1.2x: the dish from behind, high over her
    # left shoulder, pouring its thread down past her; the masked head
    # turned right in profile; the body cropped by the frame
    # the raised oath fin beyond her head
    p.lens((52.0, 40.0), (56.6, 5.0), 6.0, fin_m, bend=-1.0, fat=0.34, group=40)
    # body: ice shoulders and back, deepening into the black water
    body = bez3((8.0, 64.0), (10.0, 50.0), (18.0, 40.0), (32.0, 37.6)) + \
        bez3((32.0, 37.6), (46.0, 36.6), (58.0, 46.0), (60.0, 64.0))
    bid = p.poly(body, robe_m, group=30)
    p.poly(bez3((0, 58), (20, 52), (40, 56), (64, 50)) + [(64, 64), (0, 64)], water_m, clip=[bid], group=31)
    p.shade(ribbon(bez((34, 39), (33, 50), (34, 64)), lambda t: 1.6), 0.18)
    # the thread falling past her left side into the black water
    thread = bez3((12.0, 22.0), (8.0, 28.0), (8.0, 44.0), (11.0, 64.0))
    p.poly(ribbon(thread, lambda t: 4.0 + 2.6 * t), water_m, group=60)
    # neck, hood and the mask in right profile
    p.limb([(40.0, 42.0), (42.6, 30.0)], 10.0, 8.0, robe_m, group=22)
    p.lens((36.0, 24.0), (24.0, 34.0), 5.6, hood_m, bend=-1.4, fat=0.3, group=20)
    p.blob(42.0, 23.0, 10.0, 10.6, hood_m, group=23)
    p.poly(bez3((46.4, 16.0), (53.0, 15.0), (56.6, 21.0), (54.6, 28.0)) +
           bez3((54.6, 28.0), (52.0, 32.4), (47.0, 32.0), (45.6, 26.0)) + [(45.0, 20.0)], mask_m, group=24)
    p.lens((47.0, 15.0), (52.0, 4.6), 4.2, hood_m, bend=0.8, fat=0.3, group=21)
    # the dish from behind, its halo tipped over the back of the hood
    _dish_back(p, 25.0, 15.6, 16.4, 10.4, 22, group=70)
    if p.big:
        # frost crusting where the dish has grown from the hood
        for a, b in (((34.0, 22.0), (38.6, 18.0)), ((33.0, 25.0), (38.0, 25.6)), ((31.0, 24.0), (34.0, 29.0))):
            p.lens(a, b, 2.4, fin_m, group=80)
    if p.big:
        p.patch(51, 21, ["111", "1w1", "tt1", ".t."], {"1": "ink", "t": "tg1", "w": "wh"})


def _follow(p, view, phase):
    s = phase
    if view == "down":
        lip = _dish(p, 32.0, 15.0, 15.0, 12.0, -20)
    else:
        _dish_back(p, 32.0, 15.0, 15.0, 12.0, 20)
        lip = (20.0, 24.0)
    # the thread falling at her side into the gown
    x0 = lip[0] if view == "down" else 20.0
    p.poly(ribbon(bez3((x0, lip[1]), (x0 + 3, lip[1] + 6), (x0 + 3 - s, 40), (x0 + 1, 50)),
                  lambda t: 3.0 + 2.0 * t), water_m, group=60)
    p.poly(bez3((25, 36), (20, 44), (17, 50), (18, 56)) + [(22, 58), (26, 55), (30, 58), (34, 55), (38, 58), (42, 55),
                                                           (46, 57)] +
           bez3((46, 57), (48, 50), (45, 43), (39, 36)), water_m, group=50)
    p.blob(32, 34, 7.0, 5.0, robe_m, group=30)
    # sleeves: one raised in the oath, one hanging
    p.lens((24.0, 33.0), (19.0, 47.0 + s), 5.0, fin_m, bend=1.0, fat=0.3, group=40)
    p.lens((40.0, 32.0), (44.0, 12.0 - s), 4.6, fin_m, bend=-0.6, fat=0.34, group=41)
    p.lens((25.0, 18.0), (19.0, 10.0), 3.6, hood_m, bend=-0.6, fat=0.3, group=21)
    p.lens((39.0, 18.0), (45.0, 10.0), 3.6, hood_m, bend=0.6, fat=0.3, group=21)
    p.blob(32, 21, 8.0, 8.4, hood_m, group=23)
    if view == "down":
        p.blob(32, 22.6, 5.6, 6.2, mask_m, group=24)
        if p.big:
            p.patch(28, 21, ["11..11", "1t..t1", "tt..tt"], {"1": "ink", "t": "tg1"})
        else:
            p.pxs([(29.5, 22), (34.5, 22)], "ink")


MONS = [
    Mon("Stygiad", COLORS, SHINY, stygiad, foot="blank", follow=27, icon_pal=4),
]
