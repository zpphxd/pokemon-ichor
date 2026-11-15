"""Arachne line: Raknit, Hyphantis (Bug, then Bug/Dark). The Lydian weaver
who out-wove Athena and was made a spider that weaves forever; her webs are
tapestries of the gods behaving badly."""
from mon_lib import C, Mat, Mon

INK = C.ink

# --------------------------------------------------------------------------
# Raknit, the spiderling
# --------------------------------------------------------------------------

RAKNIT_COLORS = [
    ("ink", INK),
    # terracotta body
    ("body0", (104, 40, 24)), ("body1", (160, 64, 40)), ("body2", (208, 104, 64)), ("body3", (240, 160, 112)),
    # black-figure legs with a ceramic sheen
    ("leg0", (48, 40, 48)), ("leg1", (88, 80, 88)), ("leg2", (136, 128, 136)),
    # limestone tapestry border
    ("lime0", (160, 128, 88)), ("lime1", (216, 192, 144)), ("lime2", (240, 224, 184)),
    # marble-white silk
    ("silk0", (176, 184, 208)), ("silk1", C.white),
]
RAKNIT_SHINY = {
    "body0": (24, 48, 104), "body1": (40, 88, 160), "body2": (88, 144, 208), "body3": (152, 192, 232),
    "lime0": (176, 120, 32), "lime1": (232, 184, 56), "lime2": (248, 224, 128),
}

r_body = Mat(["body0", "body1", "body2", "body3"], line="body0", cuts=[0.24, 0.5, 0.78])
r_leg = Mat(["leg0", "leg1", "leg2"], line="leg0", cuts=[0.45, 0.8])
r_lime = Mat(["lime0", "lime1", "lime2"], line="lime0", cuts=[0.4, 0.75])


def _rk(x, y, k=0.84):
    """The spiderling is drawn at 0.84 of its design, shrunk toward its feet."""
    return (32 + (x - 32) * k, 60 + (y - 60) * k)


def _legs(p, legs, mat, k=0.84):
    for pts, w0, w1, kw in legs:
        p.limb([_rk(*q, k) for q in pts], max(w0 * k, 3.1), max(w1 * k, 2.5), mat, **kw)


def raknit(p, view, phase):
    if view == "icon":
        # party icon: a round spiderling, big eyes, the woven band bold
        L = phase
        for pts in ([(36, 46), (46, 40), (51, 50)], [(37, 50), (44, 52), (45, 59)], [(28, 46 - L), (31, 36 - L), (28, 29 - L)]):
            p.limb(pts, 3.4, 2.6, r_leg, bias=0.2, group=1)
        abdo = p.blob(39, 46, 10, 9, r_body, ang=-18, group=10)
        p.rect(28, 44, 50, 48, r_lime, clip=[abdo], group=10, flat=1)
        p.blob(24, 50 - L, 9, 7.6, r_body, bias=-0.1, group=11)
        for pts in ([(19, 54), (11, 50), (9, 59)], [(24, 56), (18, 57), (17, 60)], [(17, 51 - L), (10, 42 - L), (14, 32 - L)]):
            p.limb(pts, 3.8, 2.8, r_leg, group=5)
        p.rect(18, 47 - L, 20, 50 - L, Mat(["ink"]), group=12)
        p.rect(24, 47 - L, 26, 50 - L, Mat(["ink"]), group=13)
        return
    if view in ("front", "side"):
        # crouched on six legs, the front two raised holding a strand of
        # silk mid-stitch (the art files hand-finish this)
        L = 1 if (phase == 1 and view == "front") else 0
        R = L
        st = view == "side" and phase == 1
        _legs(p, [([(34, 45), (43, 36), (50.5, 44), (52, 58.5)], 3.6, 2.6, dict(bias=0.22, group=1)),
                  ([(36, 50), (46, 46), (50, 51.5), (48.5 - st, 59)], 3.6, 2.6, dict(bias=0.22, group=2)),
                  ([(29, 43 - L), (34, 36 - L - R), (31, 29.5 - L - 2 * R)], 3.6, 2.6, dict(bias=0.15, group=3))],
              r_leg)
        x, y = _rk(39, 45)
        p.blob(x, y, 9.6 * 0.84, 9.0 * 0.84, r_body, ang=-18, group=10)
        _legs(p, [([(34, 53), (41.5, 55), (42.5 + st, 59.5)], 3.6, 2.8, dict(bias=0.18, group=4))], r_leg)
        x, y = _rk(25, 49.5 - L)
        p.blob(x, y, 9.4 * 0.84, 7.8 * 0.84, r_body, bias=-0.1, group=11)
        _legs(p, [([(19, 54 - L), (12.5, 50.5), (10.5 - st, 59)], 4.0, 2.8, dict(group=5)),
                  ([(24, 55.5 - L), (18.5, 55.5), (17 + st, 60)], 4.0, 2.8, dict(group=6)),
                  ([(30, 55.5 - L), (34, 55.5), (34 - st, 60)], 3.8, 2.8, dict(group=7)),
                  ([(17, 52 - L), (9.5, 43 - L - R), (14, 32.5 - L - 2 * R)], 4.0, 2.8, dict(group=8))], r_leg)
        if p.big:
            p.patch(20, 48 - L, [".11..11", "1991.1991", "1911.1911", "1111.1111", ".11...11"],
                    {"1": "ink", "9": "silk1"})
            p.patch(32, 45, ["..9aaaaaaa9", ".9aaaaaaaaaa9", "9b2b2b2b2b2b2", "9aaaaaaaaaaaa", ".999999999999"],
                    {"9": "lime0", "a": "lime1", "b": "lime2", "2": "body0"})
            p.stroke([(18, 34 - L - 2 * R), (24, 35 - L - 2 * R), (30, 33 - L - 2 * R)], "silk1")
            p.pxs([(21, 35 - L - 2 * R), (27, 34 - L - 2 * R)], "silk0")
        else:
            p.pxs([(22, 49), (27, 48)], "ink")
            p.px(37, 46, "lime1")
        return

    if view == "back":
        # over the shoulder: the round abdomen with its woven border, the
        # head in profile, forelegs raised with the thread
        p.limb([(12, 46), (5.5, 36), (3, 52)], 4.0, 3.2, r_leg, bias=0.22, group=2)
        p.limb([(44, 40), (41.5, 31), (45, 23)], 4.0, 3.2, r_leg, bias=0.15, group=3)
        p.blob(23, 53, 17.5, 15, r_body, ang=-10, group=10)
        p.blob(44.5, 47, 10.5, 9, r_body, bias=-0.08, group=11)
        p.limb([(36, 56), (30, 62), (27, 66)], 4.8, 4.0, r_leg, group=4)
        p.limb([(50, 54), (58, 50), (61, 64)], 4.8, 3.6, r_leg, group=5)
        p.limb([(51, 42), (58, 34), (55, 24)], 4.8, 3.6, r_leg, group=6)
        return

    if view == "down":
        # follower scuttling toward the camera: the round head with its row
        # of eyes, the abdomen behind, legs splayed and stepping in turn
        st = phase
        for sx in (-1, 1):
            s = st if sx < 0 else 1 - st
            p.limb([(32 + 6 * sx, 48), (32 + 15 * sx, 42 + s), (32 + 18 * sx, 58)], 3.6, 2.6, r_leg, group=1)
            p.limb([(32 + 6 * sx, 51), (32 + 12 * sx, 50 - s), (32 + 13 * sx, 61)], 3.6, 2.6, r_leg, group=2)
        p.blob(32, 40, 10, 8.4, r_body, bias=0.06, group=3)
        p.patch(24, 36, ["9aaaaaaaaaaaaaa9", "2b2b2b2b2b2b2b2b", "9aaaaaaaaaaaaaa9"],
                {"9": "lime0", "a": "lime1", "b": "lime2", "2": "body0"})
        p.blob(32, 50, 8.6, 7, r_body, bias=-0.06, group=4)
        if p.big:
            p.patch(24, 47, [".1....1.", "11.11.11", "11911911", "..1111"], {"1": "ink", "9": "silk1"})
            p.pxs([(30, 54), (34, 54)], "lime1")
        else:
            p.pxs([(29, 49), (35, 49)], "ink")
        return

    if view == "up":
        # follower scuttling away: the round abdomen and its woven border,
        # legs splayed either side
        st = phase
        for sx in (-1, 1):
            s = st if sx < 0 else 1 - st
            p.limb([(32 + 6 * sx, 48), (32 + 15 * sx, 42 + s), (32 + 18 * sx, 58)], 3.6, 2.6, r_leg, group=1)
            p.limb([(32 + 6 * sx, 52), (32 + 12 * sx, 50 - s), (32 + 13 * sx, 61)], 3.6, 2.6, r_leg, group=2)
        p.blob(32, 39, 6.4, 5, r_body, group=3)
        p.blob(32, 50, 11, 9.4, r_body, bias=-0.04, group=4)
        if p.big:
            p.patch(22, 48, ["9aaaaaaaaaaaaaaaaaa9", "2b2b2b2b2b2b2b2b2b2b", "9aaaaaaaaaaaaaaaaaa9"],
                    {"9": "lime0", "a": "lime1", "b": "lime2", "2": "body0"})
        else:
            p.px(32, 49, "lime1")
        return


# --------------------------------------------------------------------------
# Hyphantis, Arachne herself, still weaving
# --------------------------------------------------------------------------

HYPHANTIS_COLORS = [
    ("ink", INK),
    # terracotta body, deeper than the spiderling's
    ("body0", (88, 32, 24)), ("body1", (144, 56, 40)), ("body2", (192, 88, 56)), ("body3", (232, 136, 88)),
    # black-figure legs and hair with a ceramic sheen
    ("leg0", (40, 32, 40)), ("leg1", (80, 72, 88)), ("leg2", (136, 128, 144)),
    # limestone tapestry ground
    ("lime0", (176, 144, 96)), ("lime1", (216, 192, 144)), ("lime2", (240, 224, 184)),
    # marble-white silk
    ("silk0", (176, 184, 208)), ("silk1", C.white),
    # sun-gold thread
    ("gold0", (200, 136, 40)), ("gold1", (248, 208, 80)),
]
HYPHANTIS_SHINY = {
    # Athena's own colors: Aegean blue and a sun-gold tapestry
    "body0": (24, 40, 96), "body1": (40, 80, 152), "body2": (72, 128, 200), "body3": (136, 184, 232),
    "lime0": (184, 120, 32), "lime1": (232, 176, 56), "lime2": (248, 224, 128),
}

h_body = Mat(["body0", "body1", "body2", "body3"], line="body0", cuts=[0.22, 0.48, 0.76])
h_leg = Mat(["leg0", "leg1", "leg2"], line="leg0", cuts=[0.45, 0.8])
h_lime = Mat(["lime0", "lime1", "lime2"], line="lime0", cuts=[0.4, 0.75])


def _loom(p, x0, x1, y0, y1):
    """A small upright loom: warp threads hung from a top bar, a band of
    cloth woven in silk and gold at the bottom."""
    if not p.big:
        p.rect(x0, y1 - 3, x1, y1, Mat(["silk0", "silk1"], line="silk0", cuts=[0.5]), group=60)
        return
    p.stroke([(x0, y0), (x1, y0)], "silk0")
    for x in range(int(x0) + 1, int(x1), 3):
        p.stroke([(x, y0 + 1), (x, y1 - 4)], "silk1")
    for y in range(int(y1) - 4, int(y1) + 1):
        for x in range(int(x0), int(x1) + 1):
            p.px(x, y, "silk1" if (x + y) % 2 else ("gold1" if (x // 2 + y) % 3 == 0 else "silk0"))
    p.stroke([(x0, y1 + 1), (x1, y1 + 1)], "gold0")


def hyphantis(p, view, phase):
    if view in ("front", "side", "icon"):
        # a spider in a wide working crouch on thick, jointed legs, the front
        # pair raised at a small upright loom; the abdomen woven like a
        # vase's frieze, a black bull and a white swan; her hair in a high bun
        # (the art files hand-finish this)
        L = 1 if (phase == 1 and view == "front") else 0
        R = L
        st = view == "side" and phase == 1
        hair = Mat(["body0", "body1", "body2"], line="ink", cuts=[0.45, 0.85])
        p.limb([(33, 45 - L), (47, 37), (52.5 - st, 58.5)], 4.8, 3.6, h_leg, bias=0.24, group=1)
        p.limb([(34, 48 - L), (55, 42), (60 + st, 58.5)], 4.8, 3.6, h_leg, bias=0.24, group=2)
        p.limb([(31, 42 - L), (33, 28.5 - L - R), (25, 15 - L - 2 * R)], 5.2, 3.8, h_leg, bias=0.12, group=3)
        abdo = p.blob(43.5, 30.5 - L, 14, 12, h_body, ang=-20, group=10)
        p.blob(56, 23 - L, 2.4, 2.2, h_body, bias=0.1, group=10)
        gold = Mat(["gold0", "gold1"], cuts=[0.5])
        for y0, h, mat in ((20 - L, 1, gold), (21 - L, 2, h_lime), (35 - L, 2, h_lime), (37 - L, 1, gold)):
            p.rect(28, y0, 58, y0 + h - 1, mat, clip=[abdo], group=10, flat=1)
        p.limb([(30, 51 - L), (40, 47), (44 - st, 59.5)], 5.2, 3.8, h_leg, bias=0.12, group=4)
        p.blob(24, 45 - L, 9.6, 7.6, h_body, bias=-0.08, group=11)
        p.lens((16.5, 40.5 - L), (22.5, 33.5 - L), 4.2, hair, bend=-1.2, group=12)
        p.blob(22, 32 - L, 4.0, 3.8, hair, bias=-0.04, group=12)
        p.limb([(18, 49 - L), (7.5, 40), (3.5 + st, 59)], 6.0, 4.2, h_leg, group=5)
        p.limb([(22, 51.5 - L), (14.5, 47), (12.5 - st, 59.5)], 6.0, 4.2, h_leg, group=6)
        p.limb([(28, 51.5 - L), (35.5, 46.5), (36.5 + st, 59.5)], 5.8, 4.2, h_leg, group=7)
        p.limb([(17, 46 - L), (8, 35 - L + R), (10, 13 - L - R)], 6.0, 4.4, h_leg, group=8)
        _loom(p, 12, 22, 16 - L - R, 27 - L - R)
        if p.big:
            for x, y in ((7.5, 40), (14.5, 47), (35.5, 46.5), (40, 47), (8, 35 - L + R)):
                p.circle(x, y, 2.0, Mat(["body1", "body2"], cuts=[0.5]), group=30 + int(x))
            p.patch(32, 29 - L, ["..1......", ".11....1.", "1111111.1", "11111111.", ".1111111.", "..1...1..",
                                 ".1.....1."], {"1": "ink"})
            p.patch(45, 24 - L, [".11..", "1..1.", "...1.", "1..1.", "11.11", ".1111", "..111"], {"1": "silk1"})
            p.pxs([(43, 25 - L), (45, 27 - L), (42, 28 - L), (44, 30 - L), (46, 29 - L), (41, 31 - L)], "gold1")
            p.patch(15, 42 - L, [".1111", "1ff91", ".11"], {"1": "ink", "f": "gold1", "9": "silk1"})
            p.patch(21, 41 - L, [".111", "1f91", ".11"], {"1": "ink", "f": "gold1", "9": "silk1"})
            p.pxs([(19, 31 - L), (19, 32 - L), (20, 33 - L), (21, 34 - L)], "gold1")
        else:
            p.px(17, 43 - L, "gold1")
            p.px(22, 32 - L, "gold1")
        return

    if view == "back":
        # over the shoulder: the whole tapestry on the abdomen, the head in
        # profile with its bun, the loom raised toward the foe
        p.limb([(14, 44), (5, 33), (2.5, 52)], 6.0, 4.4, h_leg, bias=0.22, group=1)
        p.limb([(46, 41), (43.5, 31), (47, 15.5)], 6.0, 4.4, h_leg, bias=0.12, group=3)
        abdo = p.blob(24, 47, 20.5, 17, h_body, ang=-8, group=10)
        p.rect(0, 31, 50, 33, h_lime, clip=[abdo], group=10, flat=1)
        p.rect(0, 48, 50, 50, h_lime, clip=[abdo], group=10, flat=1)
        p.blob(47.5, 48, 10, 8.2, h_body, bias=-0.08, group=11)
        p.blob(42, 35.5, 4.4, 4.2, Mat(["body0", "body1", "body2"], line="ink", cuts=[0.45, 0.85]), group=12)
        p.limb([(40, 55), (33, 60), (30, 66)], 6.8, 5.6, h_leg, group=4)
        p.limb([(52, 55), (60, 52), (61.5, 66)], 6.8, 5.2, h_leg, group=5)
        p.limb([(54, 44), (60, 34), (56.5, 16.5)], 6.8, 5.2, h_leg, group=6)
        _loom(p, 49, 55, 17, 31)
        return

    if view == "down":
        # follower stalking toward the camera: the head with its narrow eyes
        # and bun, the tapestry abdomen behind, the loom held up in front,
        # long legs stepping in turn
        st = phase
        for sx in (-1, 1):
            s = st if sx < 0 else 1 - st
            p.limb([(32 + 7 * sx, 48), (32 + 17 * sx, 40 + s), (32 + 20 * sx, 59)], 5.4, 3.8, h_leg, group=1)
            p.limb([(32 + 7 * sx, 52), (32 + 13 * sx, 49 - s), (32 + 14 * sx, 61)], 5.4, 3.8, h_leg, group=2)
        abdo = p.blob(32, 36, 12, 9.6, h_body, bias=0.06, group=3)
        p.rect(18, 33, 46, 40, h_lime, clip=[abdo], group=3, flat=1)
        p.blob(32, 49, 9, 7.4, h_body, bias=-0.06, group=4)
        p.blob(32, 42.5, 4, 3.4, Mat(["body0", "body1", "body2"], line="ink", cuts=[0.45, 0.85]), group=5)
        for sx in (-1, 1):
            p.limb([(32 + 5 * sx, 52), (32 + 10 * sx, 42), (32 + 7 * sx, 30)], 5.4, 4.0, h_leg, group=6 + sx)
        _loom(p, 26, 38, 29, 37)
        if p.big:
            p.patch(25, 47, ["1111..1111", "1ff9..9ff1", ".11....11."], {"1": "ink", "f": "gold1", "9": "silk1"})
        else:
            p.pxs([(28, 48), (36, 48)], "gold1")
        return

    if view == "up":
        # follower stalking away: the woven abdomen seen whole, legs splayed
        st = phase
        for sx in (-1, 1):
            s = st if sx < 0 else 1 - st
            p.limb([(32 + 7 * sx, 46), (32 + 17 * sx, 38 + s), (32 + 20 * sx, 59)], 5.4, 3.8, h_leg, group=1)
            p.limb([(32 + 7 * sx, 50), (32 + 13 * sx, 47 - s), (32 + 14 * sx, 61)], 5.4, 3.8, h_leg, group=2)
            p.limb([(32 + 4 * sx, 36), (32 + 9 * sx, 28), (32 + 7 * sx, 20)], 5.4, 4.0, h_leg, bias=0.15, group=6 + sx)
        p.blob(32, 36, 7, 5.6, h_body, group=3)
        abdo = p.blob(32, 48, 13, 11, h_body, bias=-0.04, group=4)
        p.rect(16, 44, 48, 53, h_lime, clip=[abdo], group=4, flat=1)
        if p.big:
            p.patch(24, 46, ["1.1.....", "11111111", "1a111111", ".1111111", ".1.1.11."], {"1": "ink", "a": "lime1"})
            p.patch(35, 46, ["11...", ".1...", ".1.1.", ".1111", "11111", ".111."], {"1": "ink"})
        return


MONS = [
    Mon("Raknit", RAKNIT_COLORS, RAKNIT_SHINY, raknit, foot="blank"),
    Mon("Hyphantis", HYPHANTIS_COLORS, HYPHANTIS_SHINY, hyphantis, foot="blank"),
]
