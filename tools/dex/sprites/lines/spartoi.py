"""Spartoi line: Sporadon, Dorydrake (Dragon, then Dragon/Fighting). Cadmus
sowed the teeth of Ares's serpent and armed men sprang from the furrows,
fighting one another until five were left (Ovid, Metamorphoses 3)."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Sporadon, the sown tooth
# --------------------------------------------------------------------------

SPORADON_COLORS = [
    ("ink", INK),
    # marble enamel
    ("t0", (136, 128, 120)), ("t1", (184, 176, 160)), ("t2", (224, 216, 200)), ("t3", (248, 248, 240)),
    # limestone dentin at the root end
    ("lime0", (168, 136, 88)), ("lime1", (216, 192, 144)),
    # terracotta earth
    ("e0", (88, 40, 24)), ("e1", (136, 64, 32)), ("e2", (184, 96, 56)), ("e3", (216, 144, 96)),
    # the seedling crest
    ("r0", (144, 32, 32)), ("r1", (216, 64, 48)),
    # sun-gold eyes glowing in the crack
    ("g0", (208, 144, 40)), ("g1", (248, 232, 128)),
]
SPORADON_SHINY = {
    # a sun-gold tooth and an Aegean-blue crest
    "t0": (168, 112, 32), "t1": (208, 152, 48), "t2": (240, 192, 72), "t3": (248, 232, 152),
    "lime0": (152, 96, 32), "lime1": (224, 168, 64),
    "r0": (24, 56, 120), "r1": (64, 128, 200),
}

s_tooth = Mat(["t0", "t1", "t2", "t3"], line="t0", cuts=[0.22, 0.46, 0.72])
s_root = Mat(["lime0", "lime1"], line="lime0", cuts=[0.5])
s_earth = Mat(["e0", "e1", "e2", "e3"], line="e0", cuts=[0.2, 0.44, 0.7])
s_crest = Mat(["r0", "r1"], line="r0", cuts=[0.5])


def _crest(p, edge, t0, t1, n, out=1, k=1.0, F=0):
    """The horsehair crest: red bristles along a curve, swept toward its
    end, like a hoplite's helmet crest. out=1 puts them on the left of the
    curve's direction, -1 on the right."""
    m = len(edge) - 1
    for i in reversed(range(n)):
        t = t0 + (t1 - t0) * i / max(n - 1, 1)
        j = min(m - 1, int(t * m))
        (px, py), (qx, qy) = edge[j], edge[j + 1]
        ex, ey = qx - px, qy - py
        d = math.hypot(ex, ey) or 1.0
        ox, oy = out * ey / d, -out * ex / d
        L = (5.0 + 2.4 * math.sin(i / max(n - 1, 1) * math.pi)) * k * (1 - 0.25 * F * (i % 2))
        p.lens((px - ox * 0.8, py - oy * 0.8), (px + ox * L + ex / d * 3.2 * k, py + oy * L + ey / d * 3.2 * k),
               3.6 * k * (1 if p.big else 1.4), s_crest, bend=-0.6 * out, fat=0.35)


def sporadon(p, view, phase):
    if view in ("front", "side", "icon"):
        # the code draft of the hand-finished front: a hooked fang risen from
        # the furrow, its point swept back, a helmet crest along its crown
        F = 1 if (phase == 1 and view == "front") else 0
        hop = 2 if (phase == 1 and view == "side") else 0
        fr = [(x, y - hop) for x, y in bez3((22, 55), (15.5, 41), (22, 22), (47 - F, 9 + F))]
        bk = [(x, y - hop) for x, y in bez3((47 - F, 9 + F), (42.5, 23), (37.5, 38), (40.5, 55))]
        p.poly(bez3((13, 62), (15, 53), (24, 50.5), (32, 50.5)) + bez3((32, 50.5), (41, 50.5), (50, 53), (53, 62)),
               s_earth, group=20)
        _crest(p, fr, 0.45, 0.88, 8, F=F)
        tooth = p.poly(fr + bk, s_tooth, group=1)
        # the dentin root showing at the gumline
        p.poly([(18, 52.5 - hop), (44, 52.5 - hop), (44, 58), (18, 58)], s_root, clip=[tooth], group=2)
        p.poly(bez3((17, 62), (20, 56.5), (27, 54.5), (33, 55)) + bez3((33, 55), (38, 55.5), (43, 57), (46, 62)),
               s_earth, group=21)
        if p.big:
            p.patch(20 - F, 31 + F - hop, ["1............11..", ".11.......111ef1.", "...111..11eeff11.",
                                           "....1eef1ffff11..", "....1ff1.1f11....", ".....11...1......"],
                    {"1": "ink", "e": "g0", "f": "g1"})
        else:
            p.stroke([(22, 34 - hop), (33, 32 - hop)], "ink")
            p.pxs([(25, 34 - hop), (31, 33 - hop)], "g1")
        return

    if view == "back":
        # over the shoulder (the hand-finished art replaces this)
        fr = bez3((40, 70), (48, 52), (41, 27), (15, 6))
        bk = bez3((15, 6), (19, 26), (25, 46), (21, 70))
        p.poly(bez3((2, 66), (4, 57), (14, 53), (28, 53)) + bez3((28, 53), (42, 53), (54, 57), (60, 66)), s_earth, group=20)
        _crest(p, fr, 0.38, 0.9, 9, out=-1, k=1.2)
        p.poly(fr + bk, s_tooth, group=1)
        if p.big:
            p.patch(33, 33, ["1........", ".1111eef1", "....1fff1", ".....111."], {"1": "ink", "e": "g0", "f": "g1"})
        return

    if view in ("down", "up"):
        # follower: hopping along with its mound of earth; seen head-on the
        # fang is a pointed arch with the crest running up its spine
        hop = 2 * phase
        p.poly(bez3((18, 61.5), (20, 54), (27, 52), (32, 52)) + bez3((32, 52), (37, 52), (44, 54), (46, 61.5)),
               s_earth, group=20)
        arch = bez3((23.5, 56), (21.5, 40), (26, 24 - hop), (32, 13 - hop)) + bez3((32, 13 - hop), (38, 24 - hop), (42.5, 40), (40.5, 56))
        p.poly(arch, s_tooth, group=1)
        # the crest runs up the fang's spine, toward or away from us
        for i, y in enumerate((30, 26, 22, 18)):
            w = 3.6 if p.big else 4.6
            p.lens((32, y + 3 - hop), (32 + (-1) ** i * 1.0, y - 5 - hop), w, s_crest, fat=0.4, group=40 + i)
        if view == "down":
            if p.big:
                p.patch(23, 34 - hop, ["1..............1.", ".111.1111.1111...", "..1eef111.1fee1..",
                                       "...1ff1....1ff1..", "....11......11..."],
                        {"1": "ink", "e": "g0", "f": "g1"})
            else:
                p.stroke([(24, 35 - hop), (40, 35 - hop)], "ink")
                p.pxs([(27, 36 - hop), (37, 36 - hop)], "g1")
        p.poly(bez3((20, 61.5), (22, 57), (28, 56), (32, 56)) + bez3((32, 56), (36, 56), (42, 57), (44, 61.5)),
               s_earth, group=21)
        return


# --------------------------------------------------------------------------
# Dorydrake, the sown warrior
# --------------------------------------------------------------------------

DORYDRAKE_COLORS = [
    ("ink", INK),
    # cypress-green scales
    ("s0", (24, 48, 40)), ("s1", (40, 88, 56)), ("s2", (72, 128, 72)), ("s3", (136, 176, 96)),
    # sun-gold: the shield rim and the cuirass-like belly plates
    ("g0", (152, 96, 32)), ("g1", (216, 160, 48)), ("g2", (248, 216, 112)),
    # the red crest (its darkest shade doubles as wet earth)
    ("r0", (120, 32, 32)), ("r1", (200, 56, 48)), ("r2", (240, 112, 80)),
    # the marble spear and fang
    ("m0", (144, 136, 128)), ("m1", (208, 200, 184)), ("m2", (248, 248, 240)),
    # terracotta earth
    ("earth", (176, 88, 48)),
]
DORYDRAKE_SHINY = {
    # sun-gold scales and a marble-white crest: a bronze statue of itself
    "s0": (104, 64, 24), "s1": (168, 112, 40), "s2": (216, 160, 56), "s3": (248, 208, 112),
    "r0": (128, 120, 120), "r1": (200, 192, 184), "r2": (248, 248, 240),
}

d_scale = Mat(["s0", "s1", "s2", "s3"], line="s0", cuts=[0.2, 0.44, 0.72])
d_scale_icon = Mat(["s0", "s1", "s2", "s3"], line="s1", cuts=[0.06, 0.3, 0.6])
d_gold = Mat(["g0", "g1", "g2"], line="g0", cuts=[0.36, 0.68])
d_crest = Mat(["r0", "r1", "r2"], line="r0", cuts=[0.34, 0.66])
d_marble = Mat(["m0", "m1", "m2"], line="m0", cuts=[0.36, 0.68])
d_earth = Mat(["r0", "earth"], line="r0", cuts=[0.55])


def _clod(p, x, y, r=1.6):
    p.blob(x, y, r, r * 0.8, d_earth)


def _claws(p, x, y, n=3, far=False):
    """Three blunt claws on a foot whose front edge is at (x, y)."""
    for i in range(n):
        p.taper([(x + i * 2.4, y - 1.5), (x + i * 2.4 - 2.2, y + 0.6)], 2.0, d_marble, bias=0.3 if far else 0)


def dorydrake(p, view, phase):
    if view == "icon":
        # party icon: the front pose cut down to its signature shapes, drawn
        # big and lit a step lighter so the greens survive the icon palette
        L = phase
        p.limb([(60, 6 + L), (8, 12 + L)], 3.4, 3.4, d_marble, group=60)
        p.poly([(9, 9.5 + L), (2, 13 + L), (9, 15 + L)], d_marble, group=61)
        for i, (a, b) in enumerate((((44, 26), (56, 30)), ((46, 34), (58, 40)))):
            p.lens(a, b, 5, d_crest, group=40 + i)
        p.limb([(36, 46), (30, 58)], 11, 9, d_scale_icon, group=22)
        p.limb([(46, 46), (52, 58)], 11, 9, d_scale_icon, group=20)
        p.blob(40, 38, 12, 11, d_scale_icon, group=1)
        p.blob(28, 22 - L, 10, 8, d_scale_icon, group=3)
        p.limb([(22, 22 - L), (12, 25 - L)], 9, 7, d_scale_icon, group=3)
        for i, (a, b) in enumerate((((24, 15 - L), (22, 6 - L)), ((29, 14 - L), (31, 5 - L)), ((34, 16 - L), (40, 9 - L)))):
            p.lens(a, b, 5.6, d_crest, group=70 + i)
        p.blob(24, 40, 13, 15, d_gold, group=10)
        p.blob(24, 40, 10.4, 12.4, d_scale_icon, group=11)
        p.blob(46, 10 + L, 4, 4, d_scale_icon, group=50)
        p.px(21, 20 - L, "g2")
        return

    if view in ("front", "side"):
        L = 1 if (phase == 1 and view == "front") else 0   # spear cocked back, crest flicks
        # at icon size the scales are lit a step lighter so the greens survive
        # the shared icon palette
        sc = d_scale

        # the spear, brandished overhead in the far hand, fang tip forward
        p.limb([(61, 3 + L), (13 - L, 8.5 + L)], 2.6, 2.6, d_marble, group=60)
        p.poly(bez3((13 - L, 7 + L), (8, 7.4 + L), (4, 9.6 + L), (1.5 - L, 13.5 + L)) +
               bez3((1.5 - L, 13.5 + L), (5, 12.4 + L), (9, 11.6 + L), (13 - L, 11.2 + L)), d_marble, group=61)
        p.limb([(14, 7 + L), (14.5, 11 + L)], 2.6, 2.6, d_gold, group=62)
        # far arm raised high to hold it
        p.limb(bez((44, 27), (51, 17), (46, 6.5 + L)), 6.8, 5.2, sc, bias=0.2, group=50)
        p.blob(45.5, 6.4 + L, 3.6, 3.2, sc, bias=0.2, group=50)
        p.limb([(47.5, 12.5 + L), (49.8, 16.5 + L)], 6.2, 6.2, d_gold, group=52, cap=False)
        # the crest running down the back of the neck, behind
        for i, (a, b, w) in enumerate((((35, 19), (44, 21 - L), 4.6), ((37, 24), (46.5, 27.5 - L), 4.2),
                                       ((39, 29), (48, 33.5 - L), 3.8))):
            p.lens(a, b, w, d_crest, bend=-0.6, fat=0.4, group=40 + i)
        # tail, sweeping back and down, red spines along it
        for i, (a, b) in enumerate((((50, 42), (52.5, 37.5 - L)), ((55, 44), (59, 41 - L)), ((58, 48.5), (61, 46.5)))):
            p.lens(a, b, 2.6, d_crest, fat=0.3, group=35 + i)
        p.limb(bez3((44, 43), (54, 42), (59, 48), (61, 56)), 9.5, 2.2, sc, bias=0.2, group=30)
        # far leg, braced back
        p.limb([(43, 44), (50, 50), (48.5, 57.5)], 9, 6.6, sc, bias=0.3, group=20)
        p.blob(47, 58.6, 5, 2.4, sc, bias=0.3, group=21)
        _claws(p, 43.5, 60.5, far=True)
        # body: crouched, leaning into the shield; gold belly plates
        p.blob(38.5, 36, 10.5, 10.5, sc, group=1)
        p.blob(37.5, 41, 5.4, 7.4, d_gold, group=2)
        # neck and the draconic head with its cheek guard and crest
        p.limb(bez((35, 32), (31, 26), (29, 19)), 11, 9, sc, group=1)
        H = 3 - L
        p.blob(27, 18 + H, 7.4, 6.2, sc, group=3)
        p.poly(bez3((24, 13.4 + H), (18, 14 + H), (12.5, 15.8 + H), (9.6, 18.4 + H)) +
               bez3((9.6, 18.4 + H), (8.6, 21 + H), (10.5, 22.6 + H), (14, 23 + H)) +
               bez3((14, 23 + H), (18, 23.6 + H), (22, 25.4 + H), (26, 25.6 + H)), sc, group=3)
        for i, (a, b, w) in enumerate((((21.5, 12 + H), (19.5, 6.5 + H - L), 3.8), ((24.5, 11 + H), (25.5, 5 + H - L), 4.2),
                                       ((28, 11.5 + H), (32, 5.5 + H - L), 4.4), ((30.5, 12.5 + H), (37.5, 8.5 + H - L), 4.2),
                                       ((32, 15 + H), (40, 14 + H - L), 4.2))):
            p.lens(a, b, w, d_crest, bend=-0.6 if i > 1 else 0.6, fat=0.45, group=70 + i)
        p.poly(bez3((23.5, 17.5 + H), (29.5, 17 + H), (31, 23 + H), (27.5, 29 + H)) +
               bez3((27.5, 29 + H), (24.5, 27 + H), (22, 22.5 + H), (23.5, 17.5 + H)), sc, group=4)
        # near leg, bent forward under the shield
        p.limb([(35, 45), (30, 51), (31.5, 57.5)], 10, 6.8, sc, group=22)
        p.blob(29.5, 58.6, 5.6, 2.6, sc, group=23)
        _claws(p, 25, 60.5)
        # the shield: one great scale held forward, gold-rimmed
        p.blob(21.5, 39, 11.4, 14.2, d_gold, ang=6, group=10)
        sh = p.blob(21.8, 39, 9, 11.8, sc, ang=6, group=11)
        p.lens((22, 28), (22, 50), 4, sc, clip=[sh], bias=-0.25, group=12)
        # near hand gripping the shield's edge
        p.blob(33, 36.5, 3, 3.2, sc, group=13)
        for x, y in ((24, 61), (35, 60.5), (52, 60.5), (59, 55.5)):
            _clod(p, x, y)
        if p.big:
            p.patch(16, 15 + H, ["1111", "1881", "1781", ".11."], {"1": "ink", "8": "g2", "7": "g1"})
            p.px(11, 18 + H, "ink")
        else:
            p.px(17, 16 + H, "ink")
        return

    if view == "back":
        # over the shoulder: broad scaled back, the crest down the neck, the
        # great scale-shield slung across the back with its dragon emblem,
        # the spear held upright, the head in right profile
        p.limb([(52, 64), (55, 2)], 3, 3, d_marble, group=60)
        p.poly([(53.5, 4), (55.5, -2), (57.5, 4), (56.5, 8), (54.5, 8)], d_marble, group=61)
        p.blob(30, 66, 30, 22, d_scale, group=1)
        p.limb([(40, 46), (44, 28)], 16, 12, d_scale, group=1)
        for i, (a, b, w) in enumerate((((42, 11), (30, 6), 6), ((40, 17), (28, 15), 6), ((39, 24), (27, 24), 5.6),
                                       ((39, 31), (28, 33), 5.2))):
            p.lens(a, b, w, d_crest, bend=1.0, group=40 + i)
        p.blob(46, 18, 8.6, 7.4, d_scale, group=3)
        p.limb([(51, 20), (60, 23)], 7.4, 5.6, d_scale, group=3)
        p.lens((45, 18), (52, 28), 6.6, d_scale, bend=-0.8, group=4)
        p.blob(22, 48, 17, 15, d_gold, group=10)
        p.blob(22, 48, 14.6, 12.6, d_scale, group=11)
        p.blob(57, 34, 4, 4, d_scale, group=13)
        if p.big:
            p.eye(49, 15, 3, 3, iris=None, shine="g2", shine_at=(1, 0))
        return

    if view in ("down", "up"):
        step = phase
        p.limb([(26, 46), (25, 59 - 2 * step)], 7, 6, d_scale, group=20)
        p.limb([(38, 46), (39, 59 - 2 * (1 - step))], 7, 6, d_scale, group=21)
        _clod(p, 25, 60 - 2 * step)
        _clod(p, 39, 60 - 2 * (1 - step))
        if view == "up":
            p.limb(bez((32, 44), (40, 52), (46, 60)), 7, 3, d_scale, group=30)
        p.blob(32, 37, 10, 11, d_scale, group=1)
        if view == "down":
            p.blob(32, 39, 6, 8, d_gold, group=2)
        p.limb([(44, 38), (44, 12)], 2.6, 2.6, d_marble, group=60)
        p.poly([(42.5, 12), (44, 5), (45.5, 12)], d_marble, group=61)
        for i, (a, b) in enumerate((((32, 14), (32, 3)), ((32, 20), (32, 28)))):
            p.lens(a, b, 5, d_crest, group=40 + i)
        p.blob(32, 18, 6.6, 6.2, d_scale, group=3)
        if view == "down":
            p.blob(32, 22, 4, 3, d_scale, group=4)
            p.eye(28, 16, 2, 2, shine=None)
            p.eye(34, 16, 2, 2, shine=None)
            p.blob(21, 38, 7.4, 9, d_gold, group=10)
            p.blob(21, 38, 5.6, 7.2, d_scale, group=11)
        else:
            p.blob(32, 38, 9.4, 9.4, d_gold, group=10)
            p.blob(32, 38, 7.6, 7.6, d_scale, group=11)
        return


MONS = [
    Mon("Sporadon", SPORADON_COLORS, SPORADON_SHINY, sporadon, foot="blank"),
    # icon palette 4 keeps the cypress greens green and the crest red
    Mon("Dorydrake", DORYDRAKE_COLORS, DORYDRAKE_SHINY, dorydrake, foot="claw", icon_pal=4),
]
