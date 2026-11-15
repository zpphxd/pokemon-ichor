"""Owl line: Glaukoin, Sophowl (Psychic/Flying). Athena's little owl, the
glaux, stamped on the silver coins of Athens, and grown into her bird of
wisdom."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink


def _feather_row(p, pts, w, mat, bend=0.4, **kw):
    """A row of overlapping feathers: pts is [(base, tip), ...] drawn back
    to front, each feather a pointed lens."""
    for a, b in pts:
        p.lens(a, b, w, mat, bend=bend, fat=0.4, **kw)


# --------------------------------------------------------------------------
# Glaukoin, the coin owlet
# --------------------------------------------------------------------------

GLAUKOIN_COLORS = [
    ("ink", INK),
    # marble-white and limestone down
    ("down0", (112, 88, 72)), ("down1", (168, 136, 104)), ("down2", (208, 184, 152)), ("down3", (240, 232, 208)),
    ("white", C.white),
    # the silver coin of its face
    ("silver0", (112, 120, 136)), ("silver1", (168, 176, 192)), ("silver2", (216, 224, 232)),
    # sun-gold eyes and beak, Psychic-pink glints
    ("gold0", (200, 136, 32)), ("gold1", (248, 200, 72)), ("pink", (240, 112, 176)),
    # the olive twig
    ("olive0", (64, 88, 40)), ("olive1", (136, 160, 72)),
]
GLAUKOIN_SHINY = {
    # a gold stater instead of a silver owl
    "silver0": (168, 104, 24), "silver1": (224, 160, 48), "silver2": (248, 216, 112),
}

g_down = Mat(["down0", "down1", "down2", "down3"], line="down0", cuts=[0.2, 0.44, 0.7])
g_pale = Mat(["down2", "down3", "white"], line="down1", cuts=[0.42, 0.7])
g_coin = Mat(["silver0", "silver1", "silver2", "white"], line="silver0", cuts=[0.22, 0.5, 0.78])
g_leaf = Mat(["olive0", "olive1"], line="olive0", cuts=[0.52])
g_twig = Mat(["down0", "down1"], line="down0", cuts=[0.5])
g_beak = Mat(["gold0", "gold1"], line="gold0", cuts=[0.55])
g_toe = Mat(["silver0", "silver1"], line="silver0", cuts=[0.55])


def _g_eye(p, x, y, L=0):
    """A huge staring owl eye, top-left at (x, y): 7x7, a gold iris ring
    round a big ink pupil with a white shine and a pink glint."""
    p.patch(x, y - L, [".11111.",
                       "1aaaaa1",
                       "1a1161a"[:6] + "1",
                       "1b111b1",
                       "1bc11b1",
                       "1bbbbb1",
                       ".11111."], {"1": "ink", "a": "gold0", "b": "gold1", "6": "white", "c": "pink"})


def glaukoin(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        hop = phase if view == "side" else 0
        perch = view != "side"

        if perch:
            # the olive twig it perches on, with three leaves
            p.limb(bez((14, 59), (32, 57), (51, 59)), 2.6, 2.0, g_twig, group=30)
            p.lens((18, 58.5), (11.5, 62.5), 3.2, g_leaf, bend=0.6, group=31)
            p.lens((46, 58.5), (53.5, 54.5), 3.2, g_leaf, bend=-0.6, group=32)
            p.lens((24, 59), (27.5, 62.8), 2.8, g_leaf, bend=-0.4, group=33)

        # tail, a short fan under the wing
        p.lens((41, 53 - hop), (50, 57 - hop), 5, g_down, bend=-0.6, bias=0.2, group=20)
        # the far wing's edge, behind the back
        p.lens((41, 38 - hop), (49, 52 - hop), 7, g_down, bend=-1.0, bias=0.3, group=21)

        # body and head: one round ball of down
        body = [p.blob(33.5, 47 - hop, 13, 10, g_down, group=1),
                p.blob(30.5, 34.5 - L - hop, 13, 11.5, g_down, group=1)]
        p.blob(28.5, 50.5 - hop, 8.5, 6.5, g_pale, clip=body, group=2)

        # ear tufts
        p.lens((22.5, 27 - L - hop), (18, 19 - L - hop), 5, g_down, bend=0.9, group=3)
        p.lens((36, 25.5 - L - hop), (41, 18.5 - L - hop), 5, g_down, bend=-0.9, group=4)

        # the near wing folded over the side, in rows of feathers
        wing = p.lens((38.5, 39 - hop), (47.5, 57 - hop), 11, g_down, bend=-1.4, fat=0.38, group=10)
        if p.big:
            # long flight feathers, back to front, then two rows of coverts
            for i, (a, b) in enumerate((((45.5, 46), (48.5, 54.5)), ((43, 47), (46.5, 56.5)),
                                        ((40.5, 47.5), (43.5, 57)), ((38.5, 48), (40.5, 56)))):
                p.lens(a, b, 3.8, g_down, bend=-0.3, fat=0.35, clip=[wing], group=11 + i, bias=0.12 - 0.04 * i)
            for i, (a, b) in enumerate((((43, 42.5), (46.5, 48)), ((40.5, 43), (43.5, 48.5)), ((38, 43.5), (40.5, 49)),
                                        ((42.5, 39), (45.5, 44)), ((40, 39.5), (43, 44.5)), ((37.5, 40), (40, 45)))):
                p.lens(a, b, 3.8, g_down, bend=-0.3, fat=0.45, clip=[wing], group=20 + i, bias=0.06 - 0.03 * (i % 3))

        # feet gripping the twig
        for fx in (28.5, 35):
            p.limb([(fx - 2, 57 - hop), (fx + 1.6, 57 - hop)], 1.8, 1.4, g_toe, group=13)

        # the coin face, turned straight out at the viewer
        p.circle(28.5, 35.5 - L - hop, 9.4, g_coin, group=5)

        if p.big:
            _g_eye(p, 21, 32 - hop, L)
            _g_eye(p, 29, 32 - hop, L)
            p.patch(27, 38 - L - hop, ["1b1", "bba", ".a."], {"1": "ink", "a": "gold0", "b": "gold1"})
            for x, y in ((25, 50), (29, 52), (32, 49), (27, 54)):
                p.pxs([(x, y), (x, y + 1)], "down1")
            for x, y in ((39, 29), (41, 33), (40, 37), (43, 36)):
                p.px(x, y - L, "white")
            for x, y in ((44, 45), (41, 46), (39, 47), (43, 41), (41, 42), (38, 43)):
                p.px(x, y - hop, "white")
        else:
            # small sizes: gold-ringed eyes and a beak dot, so the face still
            # reads as an owl's on the icon and the follower
            leg = {"1": "ink", "a": "gold0", "b": "gold1"}
            for ex in (23.5, 31.5):
                p.patch(0, 0, [], leg, small=(ex, 34.5 - L - hop, ["bab", "a1a", ".a."]))
            p.patch(0, 0, [], leg, small=(28, 39 - L - hop, ["a"]))
        return

    if view == "back":
        # over the shoulder at about 1.2x: one round ball of down seen from
        # behind, the wings folded down both sides, the head turned right so
        # the coin face shows in profile
        p.lens((28, 25), (23, 15), 6, g_down, bend=1.0, bias=-0.06, group=4)
        p.lens((39, 24), (44, 14.5), 6, g_down, bend=-1.0, bias=0.06, group=6)
        # body, then the head turned right on top of it
        p.blob(30.5, 54, 17.5, 14.5, g_down, bias=-0.12, group=1)
        p.blob(31, 45, 16.5, 9, g_down, bias=-0.12, group=1)
        p.blob(33.5, 32, 15, 12.5, g_down, bias=-0.14, group=3)
        # folded wings down both sides of the back
        p.lens((15.5, 42), (22, 68), 12, g_down, bend=2.6, bias=-0.1, group=10)
        p.lens((46.5, 43), (42, 68), 10, g_down, bend=-2.0, bias=-0.02, group=11)
        # soften the head's shadow on the shoulders and its own underside
        p.shade([(8, 36), (44, 36), (44, 47), (8, 47)], -0.16)
        # the coin face in profile, the beak past it
        p.blob(47.6, 34.5, 3.6, 9.6, g_coin, ang=-6, group=5)
        if p.big:
            p.patch(46, 30, [" 111", "1aa1", "1a61", "1b11", "1bc1", "1bb1", " 11"],
                    {"1": "ink", "a": "gold0", "b": "gold1", "6": "white", "c": "pink"})
            p.patch(51, 36, ["1", "b1", "ba1", "a1", "1"], {"1": "ink", "a": "gold0", "b": "gold1"})
            for x, y in ((28, 30), (33, 27), (37, 31), (31, 35), (26, 38), (35, 39), (40, 36), (29, 44), (37, 46)):
                p.px(x, y, "white")
        return

    if view == "up":
        # follower walking away: the round back and folded wings, but the
        # head turned all the way round to watch the player
        step = phase
        leg = {"1": "ink", "a": "gold0", "b": "gold1"}
        p.limb([(28, 54), (28, 58 - step)], 3.6, 3.2, g_down, group=12)
        p.limb([(36, 54), (36, 58 - (1 - step))], 3.6, 3.2, g_down, group=13)
        p.lens((32, 50), (32, 59), 6, g_down, bias=0.15, group=20)
        p.blob(32, 46, 11.5, 10, g_down, group=1)
        p.lens((24.5, 39), (25.5, 56), 9, g_down, bend=1.2, group=10)
        p.lens((39.5, 39), (38.5, 56), 9, g_down, bend=-1.2, group=11)
        p.blob(32, 34, 11, 9.4, g_down, group=3)
        p.lens((26, 28), (22.5, 22.5), 4.4, g_down, bend=0.6, group=4)
        p.lens((38, 28), (41.5, 22.5), 4.4, g_down, bend=-0.6, group=6)
        p.circle(32, 34.5, 8.4, g_coin, group=5)
        if p.big:
            _g_eye(p, 25, 31)
            _g_eye(p, 33, 31)
        else:
            for ex in (27.5, 35.5):
                p.patch(0, 0, [], leg, small=(ex, 33.5, ["bab", "a1a", ".a."]))
        return

    if view == "down":
        # follower walking toward the camera: the coin face and both eyes
        step = phase
        p.limb([(28, 54), (28, 59 - step)], 3.6, 3.2, g_pale, group=12)
        p.limb([(36, 54), (36, 59 - (1 - step))], 3.6, 3.2, g_pale, group=13)
        p.blob(32, 46, 11.5, 10, g_down, group=1)
        p.blob(32, 48, 6.5, 6.5, g_pale, group=2)
        p.lens((23, 40), (22, 53), 6, g_down, bend=1.0, group=10)
        p.lens((41, 40), (42, 53), 6, g_down, bend=-1.0, group=11)
        p.blob(32, 35, 11, 9.4, g_down, group=1)
        p.lens((26, 29), (22.5, 23.5), 4.4, g_down, bend=0.6, group=3)
        p.lens((38, 29), (41.5, 23.5), 4.4, g_down, bend=-0.6, group=4)
        p.circle(32, 35.5, 8.4, g_coin, group=5)
        if p.big:
            _g_eye(p, 25.5, 32.5)
            _g_eye(p, 32.5, 32.5)
        else:
            leg = {"1": "ink", "a": "gold0", "b": "gold1"}
            for ex in (27.5, 35.5):
                p.patch(0, 0, [], leg, small=(ex, 33.5, ["bab", "a1a", ".a."]))
            p.patch(0, 0, [], leg, small=(32, 38.5, ["a"]))
        return



# --------------------------------------------------------------------------
# Sophowl, the owl of Athena
# --------------------------------------------------------------------------

SOPHOWL_COLORS = [
    ("ink", INK),
    # limestone shading up into marble plumage
    ("p0", (88, 64, 56)), ("p1", (152, 112, 80)), ("p2", (208, 176, 128)), ("p3", (240, 224, 184)),
    ("white", C.white),
    # the gray ruff and the marble-silver coin face
    ("g0", (64, 72, 96)), ("g1", (136, 144, 168)), ("g2", (208, 216, 224)),
    # Aegean-blue wingtips and crest
    ("b0", (24, 56, 120)), ("b1", (64, 120, 192)),
    # sun-gold eyes, Psychic-pink glints
    ("gold", (240, 192, 64)), ("pink", (240, 112, 176)),
    # the olive sprig
    ("o0", (64, 88, 40)), ("o1", (136, 160, 72)),
]
SOPHOWL_SHINY = {
    # a gold coin and a gold-leaf wreath
    "g0": (152, 96, 32), "g1": (216, 152, 48), "g2": (248, 216, 112),
    "b0": (144, 88, 24), "b1": (224, 168, 56),
}

s_plum = Mat(["p0", "p1", "p2", "p3"], line="p0", cuts=[0.2, 0.44, 0.7])
s_pale = Mat(["p2", "p3", "white"], line="p1", cuts=[0.4, 0.7])
s_ruff = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.36, 0.7])
s_coin = Mat(["g1", "g2", "white"], line="g0", cuts=[0.34, 0.7])
s_blue = Mat(["b0", "b1", "g2"], line="b0", cuts=[0.4, 0.8])
s_leaf = Mat(["o0", "o1"], line="o0", cuts=[0.5])
s_silv = Mat(["o0", "o1", "g2"], line="o0", cuts=[0.4, 0.75])
s_twig = Mat(["p0", "p1"], line="p0", cuts=[0.5])
s_talon = Mat(["g0", "g1"], line="g0", cuts=[0.5])


def _sprig(p, base, tip, sc=1.0, sw=0.0):
    """The olive sprig held like a staff: a stem from base to tip, narrow
    leaves in alternating pairs along its upper half, silver on their
    undersides, and two olives."""
    x0, y0 = base
    tip = (tip[0] + sw, tip[1])
    stem = bez(base, ((x0 + tip[0]) / 2 + 1.2, (y0 + tip[1]) / 2), tip)
    p.limb(stem, 1.7, 1.2, s_twig, group=90)
    ang = math.atan2(tip[1] - y0, tip[0] - x0)
    n = len(stem) - 1
    for t, side, ln in ((0.42, -1, 5.2), (0.55, 1, 5.6), (0.68, -1, 5.4), (0.8, 1, 5.0), (0.9, -1, 4.4)):
        bx, by = stem[int(round(t * n))]
        a = ang + side * 0.95
        e = (bx + ln * sc * math.cos(a), by + ln * sc * math.sin(a))
        p.lens((bx, by), e, 2.5 * sc, s_silv if side > 0 else s_leaf, bend=0.5 * side, group=91 + int(t * 10))
    p.lens(tip, (tip[0] + 4.6 * math.cos(ang), tip[1] + 4.6 * math.sin(ang)), 2.5, s_silv, group=99)
    if p.big:
        for t, dx in ((0.5, 1.6), (0.62, -1.8)):
            bx, by = stem[int(round(t * n))]
            p.circle(bx + dx, by + 1.2, 1.25, Mat(["o0", "o1"], cuts=[0.55]), group=100)


def _talons(p, x, y, toes=((-3.2, 1.6), (-0.6, 2.6), (2, 2)), bias=0.0):
    """Feathered toes, ankle at (x, y), each ending in a dark hooked talon."""
    for dx, dy in toes:
        tx, ty = x + dx, y + dy
        p.limb([(x, y), (tx, ty)], 2.4, 2.0, s_pale, bias=bias)
        p.taper(bez((tx, ty), (tx - 0.9, ty + 0.4), (tx - 1.2, ty + 1.6)), 1.7, s_talon, bias=bias)


def _crest(p, L=0, sw=0.0):
    """The helmet crest: an Aegean-blue plume rising from the brow and
    arching back over the crown like the crest of Athena's helmet, with a
    shorter far plume under it."""
    p.lens((31.3, 13.3 - L), (47.5 + sw, 14.6 - L), 4.6, s_blue, bend=-1.3, fat=0.35, bias=0.25, group=60)
    near = p.lens((22, 13.3 - L), (48.5 + sw, 8.4 - L), 7.0, s_blue, bend=-3.2, fat=0.3, group=62)
    return near


def sophowl(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0

        # far wing: the cloak's back fold on the left, its blue tips trailing
        p.poly(bez3((20, 25), (15.5, 33), (15.5, 43), (16, 51)) + [(19, 52.5), (23, 52)] +
               bez3((23, 52), (22, 43), (23, 36), (25, 28)), s_plum, bias=0.28, group=20)
        p.lens((16.5, 48), (17, 55.5), 4.0, s_blue, bend=0.3, bias=0.28, group=21)
        p.lens((19.8, 48.5), (21, 55), 3.8, s_blue, bend=0.3, bias=0.3, group=21)

        # legs under the cloak: the far one planted, talons spread
        p.limb([(30.5, 49), (31.5, 56)], 5, 4.4, s_pale, bias=0.12, group=14)
        _talons(p, 32, 56.5, bias=0.12)

        # body: upright, the marble breast showing between the cloak's folds
        body = [p.blob(30, 39.5, 11, 12.5, s_plum, group=1)]
        p.blob(26.5, 40, 7, 11.5, s_pale, clip=body, group=2)

        # the near wing folded like a himation from the shoulder to the
        # shins, its trailing edge lifting a little off the body; on frame 2
        # it flares out, the hem swinging up and the primaries fanning
        flare = phase == 1 and view == "front"
        if flare:
            hem = [(38, 53.5), (43, 54), (48.5, 52.5), (55, 48.5)]
            edge = bez3((55, 48.5), (55.5, 39), (51, 28), (44, 21.5))
            prims = (((50.5, 45), (59, 50)), ((48, 48.5), (56.5, 56)), ((44, 50.5), (50.5, 59)),
                     ((39.5, 51.5), (42.5, 58.5)))
        else:
            hem = [(38, 53.5), (42, 54.5), (46.5, 55), (52, 53.5)]
            edge = bez3((52, 53.5), (50.5, 44), (49.5, 30), (44, 21.5))
            prims = (((47.5, 50), (52.5, 58.5)), ((43.5, 51), (47, 59)), ((40, 51.5), (42, 58.5)),
                     ((36.5, 51), (37.5, 57)))
        cloak = bez3((38, 25), (35, 33), (34, 43), (34.5, 52)) + hem + edge
        p.poly(cloak, s_plum, group=10)
        # the lining of the lifted edge, pale where it turns to the light
        p.limb(edge[:9], 2.6, 1.2, s_pale, group=11, bias=-0.1)
        for i, (a, b) in enumerate(prims):
            if not (p.big and view == "front"):     # the battle art lays its own primaries
                p.lens(a, b, 4.8, s_blue, bend=-0.3, group=50 + i, under=True)
        if p.big:
            # the himation's folds: a lit leading edge and long shadowed
            # creases falling to the hem
            p.shade(bez3((34.5, 30), (33, 38), (32.5, 46), (33, 53)) + bez3((35.5, 53), (35, 46), (35.5, 38), (37, 30)), -0.35)
            for pts in ((39, 33, 40, 53), (43, 34, 44.5, 54)):
                x0, y0, x1, y1 = pts
                p.shade([(x0, y0), (x0 + 1.4, y0), (x1 + 1.4, y1), (x1, y1)], 0.22)
            # the shadow side of the cloak
            p.shade(bez3((46, 26), (47, 36), (47.5, 46), (48, 54)) + [(56, 54), (56, 24)], 0.3)

        # the near foot, raised, gripping the olive sprig it holds like a staff
        _sprig(p, (22, 55), (9, 34 - L), sc=1.2, sw=0)
        p.limb([(26, 49), (23.5, 54)], 5.4, 4.6, s_pale, group=15)
        _talons(p, 23.5, 54.5, toes=((-3, 0.4), (-1.6, 2.4), (1.4, 2.0)))

        # head (about 0.9 the first draft's): the crest, the crown, a soft
        # feathered facial disc whose tips flare at the cheeks and chin, and
        # the round silver coin of the face
        _crest(p, L)
        p.blob(30.4, 19.2 - L, 11.2, 9.9, s_plum, group=3)
        p.circle(25.4, 20.8 - L, 10.0, s_ruff, group=4)
        for ang, r1, w in ((95, 13.6, 4.6), (120, 13.2, 4.4), (145, 12.8, 4.0), (172, 12.0, 3.6),
                           (68, 13.2, 4.4), (42, 12.4, 4.0), (15, 11.6, 3.6)):
            a = math.radians(ang)
            p.lens((25.4 + 8.0 * math.cos(a), 20.8 - L + 8.0 * math.sin(a)),
                   (25.4 + r1 * math.cos(a), 20.8 - L + r1 * math.sin(a)), w, s_ruff, fat=0.3, group=4)
        p.circle(25, 20 - L, 8.5, s_coin, group=5)

        if p.big:
            for x in (18, 26):
                p.patch(x, 17 - L, ["  111  ", " 1ggg1 ", "1gg17g1", "1g111g1", "1gg1gg1", " 1ggg1 ", "  111  "],
                        {"1": "ink", "g": "gold", "7": "white"})
            p.patch(24, 23 - L, ["1c1", "1cp", " 1 "], {"1": "ink", "c": "gold", "p": "p1"})
            for x, y in ((22, 35), (26, 37), (21, 40), (25, 43), (22, 46), (26, 49)):
                p.pxs([(x, y), (x + 1, y + 1), (x + 2, y)], "p1")
        else:
            leg = {"1": "ink", "g": "gold"}
            for ex in (20.5, 28.5):
                p.patch(0, 0, [], leg, small=(ex, 19.5 - L, ["ggg", "g1g", "ggg"]))
        return

    if view == "back":
        # over the shoulder at about 1.2x: both wings folded down the back
        # like a cloak, high at the shoulders and crossing at the hem; the
        # head turned right, the coin face in profile, the crest sweeping
        # back over the crown
        # the cloak: two wings meeting down the spine
        lw = p.poly(bez3((31, 31), (21, 26), (11, 36), (9, 66)) + [(33, 66)] + bez3((33, 66), (33, 52), (32, 42), (31, 31)),
                    s_plum, group=10)
        rw = p.poly(bez3((31, 31), (41, 27), (50, 34), (53, 66)) + [(30, 66)] + bez3((30, 66), (31, 52), (31.5, 42), (31, 31)),
                    s_plum, bias=0.12, group=11)
        if p.big:
            # scapulars and long feathers on each wing, blue primaries at the hem
            for i, (a, b) in enumerate((((17, 38), (14, 54)), ((22.5, 36), (20.5, 56)), ((28, 36), (27.5, 58)))):
                p.lens(a, b, 6, s_plum, bend=0.6, clip=[lw], group=30 + i)
            for i, (a, b) in enumerate((((45, 38), (48, 54)), ((39.5, 36), (42, 56)), ((34.5, 36), (35.5, 58)))):
                p.lens(a, b, 6, s_plum, bend=-0.6, clip=[rw], bias=0.08, group=40 + i)
            for i, (a, b) in enumerate((((12, 57), (15.5, 66)), ((18.5, 58), (21.5, 67)), ((25, 59), (28, 67)))):
                p.lens(a, b, 5, s_blue, bend=0.3, group=50 + i)
            for i, (a, b) in enumerate((((50, 57), (47, 66)), ((44, 58), (41, 67)), ((38, 59), (35, 67)))):
                p.lens(a, b, 5, s_blue, bend=-0.3, bias=0.1, group=55 + i)
        # head, sunk into the high shoulders of the cloak
        p.blob(34.5, 25, 13.5, 11.5, s_plum, group=3)
        p.blob(42.5, 27, 6, 9.5, s_plum, group=3)
        # crest sweeping back (to the left) from the brow
        p.lens((35, 15), (16, 16), 5.2, s_blue, bend=1.6, fat=0.35, bias=0.25, group=60)
        p.lens((43, 14), (14, 9.5), 8.0, s_blue, bend=3.2, fat=0.32, group=62)
        # the face disc seen edge-on as the head turns right: a thin crescent
        # of gray ruff and silver rim, with the eye and the beak past it
        p.lens((47, 13.5), (47.5, 37), 4.6, s_ruff, bend=-2.6, fat=0.5, group=4)
        p.lens((49, 15.5), (49.5, 35), 2.4, s_coin, bend=-2.8, fat=0.5, group=5)
        if p.big:
            p.patch(50, 21, [" 111", "1cc71", "1c111", "1c111", "1cc11", " 111"],
                    {"1": "ink", "c": "gold", "7": "white"})
            p.patch(51, 27, ["1c1", "1cc1", " 1c31", "  131", "   1"], {"1": "ink", "c": "gold", "3": "p1"})
        return

    if view in ("down", "up"):
        # follower: the owl from the front or behind, wings wrapped like a
        # cloak, the crest on its crown
        step = phase
        p.limb([(28, 52), (28, 59 - step)], 3.6, 3, s_pale, group=12)
        p.limb([(36, 52), (36, 59 - (1 - step))], 3.6, 3, s_pale, group=13)
        p.blob(32, 45, 11, 11, s_plum, group=1)
        if view == "down":
            p.blob(32, 46, 6, 9, s_pale, group=2)
        p.lens((24, 36), (22.5, 57), 9, s_plum, bend=1.2, group=10)
        p.lens((40, 36), (41.5, 57), 9, s_plum, bend=-1.2, group=11)
        p.lens((22, 52), (22.5, 59), 4.4, s_blue, group=14)
        p.lens((42, 52), (41.5, 59), 4.4, s_blue, group=15)
        if view == "down":
            # the crest seen head-on: a short fan arching back over the crown
            p.lens((32, 17), (33, 8), 9, s_blue, bend=-0.6, fat=0.4, group=6)
        p.blob(32, 25, 12, 11, s_plum, group=3)
        if view == "up":
            # from behind, the crest runs back over the crown and down the nape
            p.lens((32, 13), (32, 31), 6.5, s_blue, fat=0.3, group=6)
        if view == "down":
            p.circle(32, 26, 10.5, s_ruff, group=4)
            p.circle(32, 25.5, 8.6, s_coin, group=5)
            if p.big:
                for ex in (25, 33):
                    p.patch(ex, 22, ["  111  ", " 1ccc1 ", "1c116c1", "1c111c1", "1cd11c1", " 1ccc1 ", "  111  "],
                            {"1": "ink", "c": "gold", "6": "white", "d": "pink"})
            else:
                leg = {"1": "ink", "g": "gold"}
                for ex in (27.5, 35.5):
                    p.patch(0, 0, [], leg, small=(ex, 24.5, ["ggg", "g1g", "ggg"]))
        return


MONS = [
    Mon("Glaukoin", GLAUKOIN_COLORS, GLAUKOIN_SHINY, glaukoin, foot="bird"),
    Mon("Sophowl", SOPHOWL_COLORS, SOPHOWL_SHINY, sophowl, foot="bird"),
]
