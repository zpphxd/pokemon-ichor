"""Alectryon line: Eopeep, Alekrow, Hoplektor (Fighting). The young sentry
Ares turned into a rooster for sleeping on watch, so he crows before every
dawn."""
from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Eopeep, the dawn chick
# --------------------------------------------------------------------------

EOPEEP_COLORS = [
    ("ink", INK),
    ("down0", (168, 104, 32)), ("down1", (216, 152, 48)), ("down2", (240, 192, 72)), ("down3", (248, 224, 136)),
    ("lime0", (208, 184, 128)), ("lime1", (240, 232, 192)), ("white", C.white),
    ("terra0", (120, 48, 24)), ("terra1", (184, 88, 48)), ("terra2", (232, 144, 88)),
    ("comb0", (152, 40, 32)), ("comb1", (216, 80, 56)),
]
EOPEEP_SHINY = {
    # marble-white down, an Aegean-blue comb
    "down0": (136, 136, 144), "down1": (184, 184, 192), "down2": (216, 216, 216), "down3": (240, 240, 232),
    "lime0": (200, 200, 200), "lime1": (232, 232, 232),
    "comb0": (24, 56, 120), "comb1": (48, 112, 184),
}

e_down = Mat(["down0", "down1", "down2", "down3"], line="down0", cuts=[0.16, 0.42, 0.7])
e_belly = Mat(["lime0", "lime1", "white"], line="down1", cuts=[0.4, 0.75])
e_leg = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.3, 0.65])
e_comb = Mat(["comb0", "comb1"], line="comb0", cuts=[0.5])


def _toes(p, x, y, mat, far=False, n=3):
    """Three forward toes and a hind toe, the foot's heel at (x, y)."""
    b = 0.3 if far else 0.0
    p.limb([(x, y), (x - 4.5, y + 0.8)], 1.6, 1.3, mat, bias=b)
    p.limb([(x, y), (x - 3.5, y + 1.6)], 1.6, 1.3, mat, bias=b)
    p.limb([(x, y), (x + 2, y + 1)], 1.5, 1.2, mat, bias=b)


def eopeep(p, view, phase):
    if view == "icon":
        # party icon at icon size: a round chick, fists up
        L = phase
        p.limb([(13, 22), (12.5, 26.5)], 1.8, 1.6, e_leg)
        p.limb([(18, 22), (19, 26.5)], 1.8, 1.6, e_leg)
        p.limb([(12.5, 26.5), (10, 27)], 1.4, 1.2, e_leg)
        p.limb([(19, 26.5), (16.5, 27)], 1.4, 1.2, e_leg)
        p.blob(24, 16 - L, 2.6, 2.4, e_down, bias=0.2, group=10)
        p.blob(16, 17, 8.4, 7.4, e_down, group=1)
        p.blob(12.5, 18, 4, 4.6, e_belly, group=2)
        p.blob(14, 10, 7, 6.4, e_down, group=3)
        p.lens((13, 4.5), (12, 1), 3, e_comb, group=4)
        p.lens((15.5, 4.5), (16.5, 1.5), 2.6, e_comb, group=4)
        p.poly([(8, 9.5), (4, 11), (8, 12.5)], e_leg, group=5)
        p.blob(8, 17 - L, 2.6, 2.4, e_down, group=14)
        p.eye(10, 7, 2, 3, shine="white", shine_at=(1, 0))
        p.eye(15, 7, 2, 3, shine="white", shine_at=(1, 0))
        return

    if view in ("front", "side"):
        L = 1 if (phase == 1 and view == "front") else 0

        # far wing, a stubby fist raised behind
        p.blob(42.5, 43 - L, 3.4, 3.6, e_down, ang=20, bias=0.25, group=10)
        # far leg, up on the toes, spur bump behind
        p.limb([(35, 54), (36.5, 58.5)], 2.4, 2, e_leg, bias=0.3, group=11)
        _toes(p, 36.5, 58.8, e_leg, far=True)
        # tail tuft
        p.lens((39, 46), (45, 43), 4, e_down, bend=-0.6, bias=0.1, group=12)
        p.lens((39, 48), (45.5, 47.5), 3.4, e_down, bend=-0.4, bias=0.15, group=12)
        # body: an egg of down, chest puffed forward
        body = p.blob(33, 48, 9.6, 9.4, e_down, ang=-10, group=1)
        p.blob(28.5, 49.5, 5.2, 6.8, e_belly, clip=[body], group=2)
        # head, big and round
        p.blob(28.5, 37.5 - L, 8.6, 8, e_down, group=3)
        # down tufts on the crown and cheek
        for a, b, w in (((30, 30.5 - L), (32.5, 27 - L), 2.8), ((32.5, 31 - L), (36, 28.5 - L), 2.6),
                        ((36.5, 40 - L), (39.5, 42 - L), 2.6)):
            p.lens(a, b, w, e_down, group=3)
        # comb nub
        p.lens((27.5, 31 - L), (26, 27 - L), 3.4, e_comb, bend=0.4, group=4)
        p.lens((29, 30.5 - L), (29.5, 27.5 - L), 2.4, e_comb, group=4)
        # beak
        p.poly([(21, 37.5 - L), (16, 39.5 - L), (21, 41.5 - L)], e_leg, group=5)
        # near leg
        p.limb([(29.5, 54.5), (28.5, 59)], 2.6, 2.2, e_leg, group=13)
        _toes(p, 29, 59.2, e_leg)
        # near wing: a little fist held up in front of the chest
        p.blob(23, 46.5 - L, 3.8, 3.6, e_down, ang=-20, group=14)

        if p.big:
            p.eye(22, 33 - L, 4, 6, shine="white")
            p.eye(29, 33 - L, 3, 6, shine="white", shine_at=(1, 1))
            p.px(17, 39 - L, "terra0")
        else:
            p.pxs([(22, 36 - L), (30, 36 - L)], "ink")
        return

    if view == "back":
        # over the shoulder: the round back of the chick, head turned right
        p.blob(28, 62, 19, 17, e_down, group=1)
        p.blob(39, 33, 11, 10.4, e_down, group=3)
        p.lens((37, 24), (36, 20), 4, e_comb, group=4)
        p.poly([(49, 33.5), (54, 35.5), (49, 37.5)], e_leg, group=5)
        p.blob(15, 41, 4, 3.6, e_down, group=14)
        if p.big:
            p.eye(43, 30, 3, 5, shine="white", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower: hopping toward or away from the camera
        hop = phase
        p.limb([(29, 54 - hop), (29, 59 - hop)], 2.4, 2, e_leg, group=11)
        p.limb([(35, 54 - hop), (35, 59 - hop)], 2.4, 2, e_leg, group=12)
        for x in (29, 35):
            p.limb([(x, 59.5 - hop), (x - 2, 61 - hop)], 1.6, 1.3, e_leg)
            p.limb([(x, 59.5 - hop), (x + 2, 61 - hop)], 1.6, 1.3, e_leg)
        p.blob(32, 46 - hop, 10, 9, e_down, group=1)
        if view == "down":
            p.blob(32, 48 - hop, 6, 6, e_belly, group=2)
        p.blob(32, 35 - hop, 8.4, 7.8, e_down, group=3)
        p.blob(21.5, 45 - hop, 3.4, 3.2, e_down, group=13)
        p.blob(42.5, 45 - hop, 3.4, 3.2, e_down, group=14)
        p.lens((31, 28 - hop), (30, 24 - hop), 3.6, e_comb, group=4)
        p.lens((33.5, 28 - hop), (34.5, 24.5 - hop), 3, e_comb, group=4)
        if view == "down":
            p.eye(27, 32 - hop, 2, 4, shine="white", shine_at=(1, 0))
            p.eye(35, 32 - hop, 2, 4, shine="white", shine_at=(0, 0))
            p.poly([(30, 37 - hop), (34, 37 - hop), (32, 40 - hop)], e_leg, group=5)
        else:
            p.lens((32, 52 - hop), (32, 57 - hop), 4, e_down, group=6)
        return


# --------------------------------------------------------------------------
# Alekrow, the cockerel
# --------------------------------------------------------------------------

ALEKROW_COLORS = [
    ("ink", INK),
    ("terra0", (112, 40, 24)), ("terra1", (176, 80, 40)), ("terra2", (216, 128, 72)),
    ("gold1", (216, 160, 56)), ("gold2", (248, 208, 96)),
    ("marble0", (160, 152, 144)), ("marble1", (216, 208, 192)), ("white", C.white),
    ("cyp0", (24, 48, 40)), ("cyp1", (40, 80, 64)), ("aegean1", (48, 104, 176)), ("aegean2", (112, 168, 224)),
    ("comb0", (152, 32, 32)), ("comb1", (224, 72, 56)),
]
ALEKROW_SHINY = {
    # marble-white feathers, an Aegean-blue comb and tail
    "terra0": (120, 120, 128), "terra1": (176, 176, 184), "terra2": (216, 216, 216),
    "comb0": (24, 56, 120), "comb1": (48, 112, 184),
    "cyp0": (24, 40, 96), "cyp1": (40, 80, 152), "aegean1": (112, 168, 224), "aegean2": (176, 216, 240),
}

a_body = Mat(["terra0", "terra1", "terra2", "gold1"], line="terra0", cuts=[0.18, 0.44, 0.72])
a_gold = Mat(["terra1", "gold1", "gold2"], line="terra0", cuts=[0.34, 0.64])
a_hackle = Mat(["marble0", "marble1", "white"], line="marble0", cuts=[0.38, 0.7])
a_tail = Mat(["cyp0", "cyp1", "aegean1", "aegean2"], line="cyp0", cuts=[0.24, 0.48, 0.66])
a_leg = Mat(["terra1", "gold1", "gold2"], line="terra0", cuts=[0.34, 0.66])
a_comb = Mat(["comb0", "comb1"], line="comb0", cuts=[0.5])
a_spur = Mat(["marble0", "marble1"], line="marble0", cuts=[0.5])


def alekrow(p, view, phase):
    if view == "icon":
        # party icon at icon size: the crowing cockerel
        L = phase
        for i, (pts, w) in enumerate(((((21, 14), (25, 4), (29, 8)), 2.8), (((21, 15), (28, 12), (28.5, 19)), 2.6))):
            p.taper(bez(*pts), w, a_tail, group=20 + i)
        p.limb([(17, 20), (18, 27)], 1.8, 1.6, a_leg)
        p.limb([(13, 20), (10.5, 24)], 1.8, 1.6, a_leg)
        p.limb([(18, 27), (15.5, 27.5)], 1.4, 1.2, a_leg)
        p.blob(16.5, 16.5, 6.6, 5, a_body, ang=-15, group=1)
        p.lens((15.5, 14), (9, 19), 4.4, a_gold, bend=0.8, group=6)
        p.blob(11, 11, 4, 4.4, a_hackle, group=3)
        p.blob(9, 6.5 - L, 3.4, 3.2, a_body, group=4)
        for a, b in (((7.5, 3.5 - L), (6.5, 0.5 - L)), ((9.5, 3 - L), (10, 0 - L)), ((11.5, 3.5 - L), (13, 1 - L))):
            p.lens(a, b, 2.4, a_comb, group=5)
        p.poly([(6, 5.5 - L), (2, 3 - 2 * L), (6, 7 - L)], a_leg, group=8)
        p.poly([(6, 7.5 - L), (2.5, 8.5), (6, 8.5 - L)], a_leg, group=8)
        p.px(8, 6 - L, "ink")
        return

    if view in ("front", "side"):
        L = 1 if (phase == 1 and view == "front") else 0

        # sickle tail coming in: dark feathers arcing up and over
        for a, b, w, bend in (((43, 35), (55, 15 - L), 5.6, -3.6), ((44, 36), (58.5, 26 - L), 5, -3.0),
                              ((44, 38), (57, 38), 4.6, -2.0), ((43, 34), (48, 12 - L), 4.4, -3.0)):
            p.lens(a, b, w, a_tail, bend=bend, group=20)
        # far wing, held out behind like a raised elbow
        p.lens((38, 31), (48, 41), 6.4, a_body, bend=-1.0, bias=0.25, group=10)
        # standing leg: feathered thigh, golden shank, a sharp spur
        p.limb([(38, 44), (39, 50)], 7.4, 4.8, a_body, bias=0.15, group=11)
        p.limb([(39, 50), (38, 58.5)], 3, 2.6, a_leg, group=12)
        p.taper([(39.5, 54.5), (43.5, 53)], 2.2, a_spur, group=12)
        for dx, dy in ((-5.5, 1.2), (-4.5, 2.2), (3, 1)):
            p.limb([(38, 58.8), (38 + dx, 58.8 + dy)], 1.8, 1.4, a_leg, group=12)
        # body: chest puffed out, back sloping to the tail
        p.blob(36.5, 38, 10, 7.8, a_body, ang=-20, group=1)
        p.blob(28.5, 38, 8.6, 9, a_body, group=1)
        # raised leg, knee up, toes curled, mid-strut
        p.limb([(31, 44), (26.5, 48.5)], 6.6, 4.4, a_body, group=13)
        p.limb([(26.5, 48.5), (24, 53.5)], 3, 2.6, a_leg, group=14)
        p.taper([(25.5, 51.5), (29, 54)], 2, a_spur, group=14)
        for dx, dy in ((-3.6, 2.4), (-2, 3.8), (-4.4, 0.4)):
            p.limb([(24, 53.5), (24 + dx, 53.5 + dy)], 1.7, 1.3, a_leg, group=14)
        # hackles: a ruff of pointed marble feathers over the shoulders
        for a, b, w, bend in (((30, 23), (35, 34), 5, -0.8), ((27, 23), (30, 36), 5.4, -0.4),
                              ((24, 22), (24.5, 36.5), 5.6, 0.2), ((21, 22), (18.5, 34), 5.4, 0.8)):
            p.lens((a[0], a[1] - L), b, w, a_hackle, bend=bend, group=3)
        p.blob(24, 24 - L, 7.6, 5.6, a_hackle, group=3)
        # the near wing held up in a guard, flight feathers like fingers
        p.lens((33, 32), (19, 41), 8.6, a_body, bend=1.6, group=6)
        p.lens((32.5, 31.5), (23, 36), 6.2, a_gold, bend=1.0, group=7)
        # head, tilted up to crow
        p.blob(19, 16 - L, 7, 6.4, a_body, group=4)
        # comb, tall and stiff like a helmet's crest
        for a, b, w in (((15, 11 - L), (11, 3 - L), 4.4), ((18.5, 10 - L), (18, 0.5 - L), 4.8),
                        ((22, 10.5 - L), (24.5, 2 - L), 4.4), ((24.5, 12.5 - L), (28.5, 7 - L), 3.6)):
            p.lens(a, b, w, a_comb, group=5)
        # beak open in a crow, wattles below
        p.poly([(13.5, 13 - L), (6.5, 9 - 2 * L), (13, 15.5 - L)], a_leg, group=8)
        p.poly([(13.5, 17 - L), (7.5, 18.5 - L + L), (13.5, 19 - L)], a_leg, group=8)
        p.blob(14.5, 22 - L, 2.2, 3, a_comb, group=9)

        if p.big:
            p.eye(15, 13 - L, 3, 4, iris="gold2", shine="white", shine_at=(1, 1))
        else:
            p.px(16, 14 - L, "ink")
        return

    if view == "back":
        # over the shoulder: the sickle tail arching up behind, a cape of
        # white hackles down the back, the head turned right to crow
        for i, (pts, w) in enumerate(((((20, 50), (4, 42), (3, 20), (14, 8)), 7),
                                      (((21, 52), (8, 47), (8, 28), (19, 18)), 6.6),
                                      (((22, 55), (12, 54), (12, 38), (22, 30)), 6))):
            p.taper(bez3(*pts), w, a_tail, group=20 + i)
        p.blob(30, 65, 22, 17, a_body, group=1)
        p.blob(36, 52, 13, 9, a_body, group=1)
        p.lens((13, 54), (40, 49), 10, a_gold, bend=-1.8, group=6)
        p.lens((14, 58), (40, 55), 9.6, a_body, bend=-1.4, group=7)
        p.limb(bez((47, 30), (44, 36), (40, 42)), 10, 12, a_hackle, group=2)
        for i, (a, b) in enumerate((((44, 32), (44, 51)), ((42, 33), (36, 52)), ((41, 33), (29, 50)),
                                    ((40, 32), (22, 46)), ((46, 32), (50, 47)))):
            p.lens(a, b, 7.4, a_hackle, bend=0.6 if i % 2 else -0.6, group=30 + i)
        p.blob(47, 24, 7.6, 7.2, a_body, group=4)
        for a, b, w in (((42, 19), (39, 9.5), 4.6), ((45.5, 18), (45.5, 7.5), 5), ((49, 18), (52, 9), 4.8),
                        ((51.5, 20), (56.5, 13.5), 4)):
            p.lens(a, b, w, a_comb, group=5)
        p.poly([(53, 21), (61, 16.5), (53.5, 24.5)], a_leg, group=8)
        p.poly([(53.5, 26.5), (60, 29), (53, 29)], a_leg, group=8)
        p.blob(52, 31.5, 2.4, 3, a_comb, group=9)
        if p.big:
            p.eye(49, 21, 3, 4, iris="gold2", shine="white", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower strutting toward or away from the camera, chest out
        st = phase
        if view == "up":
            # the sickle tail arching up over the back, swaying as it walks
            for i, (pts, w) in enumerate(((((29, 44), (12, 38), (14, 22 + st)), 8),
                                          (((32, 42), (30, 28), (33, 17)), 8),
                                          (((35, 44), (52, 38), (50, 22 + (1 - st))), 8))):
                p.taper(bez(*pts), w, a_tail, group=20 + i)
        p.limb([(28, 48), (28, 59 - 2 * st)], 2.6, 2.2, a_leg, group=11)
        p.limb([(36, 48), (36, 59 - 2 * (1 - st))], 2.6, 2.2, a_leg, group=12)
        for x, y in ((28, 59.5 - 2 * st), (36, 59.5 - 2 * (1 - st))):
            p.limb([(x, y), (x - 2.5, y + 1.5)], 1.6, 1.3, a_leg)
            p.limb([(x, y), (x + 2.5, y + 1.5)], 1.6, 1.3, a_leg)
        p.blob(32, 43, 9.4, 8.2, a_body, group=1)
        p.lens((25, 37), (21, 48), 6, a_gold, group=13)
        p.lens((39, 37), (43, 48), 6, a_gold, group=14)
        for i, (a, b) in enumerate((((30, 30), (26, 41)), ((34, 30), (38, 41)), ((32, 30), (32, 42)))):
            p.lens(a, b, 6.4, a_hackle, group=30 + i)
        p.blob(32, 27, 6, 5.4, a_hackle, group=3)
        p.blob(32, 22, 6, 5.6, a_body, group=4)
        for a, b, w in (((29.5, 17.5), (28, 10), 3.6), ((32, 17), (32, 8.5), 4), ((34.5, 17.5), (36, 10), 3.6)):
            p.lens(a, b, w, a_comb, group=5)
        if view == "down":
            p.poly([(30, 24), (34, 24), (32, 28)], a_leg, group=8)
            p.blob(32, 29.5, 1.8, 2, a_comb, group=9)
            p.eye(27, 20, 2, 3, iris="gold2", shine=None)
            p.eye(35, 20, 2, 3, iris="gold2", shine=None)
        return


# --------------------------------------------------------------------------
# Hoplektor, the war-cock
# --------------------------------------------------------------------------

HOPLEKTOR_COLORS = [
    ("ink", INK),
    ("bronze0", (104, 64, 32)), ("bronze1", (160, 104, 48)), ("bronze2", (208, 160, 80)), ("bronze3", (240, 208, 128)),
    ("white", C.white), ("marble1", (200, 192, 176)),
    ("terra0", (112, 40, 24)), ("terra1", (176, 80, 40)), ("terra2", (224, 136, 88)),
    ("cyp0", (24, 48, 40)), ("cyp1", (40, 80, 64)), ("aegean1", (48, 104, 176)), ("aegean2", (112, 168, 224)),
    ("marble0", (152, 144, 136)),
]
HOPLEKTOR_SHINY = {
    # silver-marble bronze, an Aegean-blue crest
    "bronze0": (88, 96, 112), "bronze1": (136, 144, 160), "bronze2": (184, 192, 200), "bronze3": (232, 232, 240),
    "terra0": (24, 56, 120), "terra1": (48, 104, 176), "terra2": (112, 168, 224),
}

h_bronze = Mat(["bronze0", "bronze1", "bronze2", "bronze3"], line="bronze0", cuts=[0.2, 0.46, 0.72])
h_crest = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.3, 0.64])
h_tail = Mat(["cyp0", "cyp1", "aegean1", "aegean2"], line="cyp0", cuts=[0.12, 0.28, 0.66])
h_feather = Mat(["cyp0", "cyp1", "aegean1"], line="cyp0", cuts=[0.4, 0.75])
h_field = Mat(["terra1", "terra2"], line="terra0", cuts=[0.55])
h_spur = Mat(["marble1", "white"], line="bronze0", cuts=[0.5])


h_hackle = Mat(["marble0", "marble1", "white"], line="marble0", cuts=[0.4, 0.72])


def hoplektor(p, view, phase):
    if view == "icon":
        # party icon at icon size: crest, helmet, hoplon, sickle tail
        L = phase
        for i, (pts, w) in enumerate(((((18, 9), (24, 0), (28.5, 12)), 3), (((18, 11), (26, 6), (27, 22)), 2.8))):
            p.taper(bez(*pts), w, h_tail, group=20 + i)
        p.limb([(13, 21), (11, 27)], 2.2, 1.8, h_bronze)
        p.limb([(18, 21), (20, 27)], 2.2, 1.8, h_bronze, bias=0.2)
        p.blob(16, 14, 5, 7, h_feather, group=1)
        p.circle(11.5, 16, 6.4, h_bronze, group=5)
        p.circle(11.5, 16, 4.4, h_field, group=6)
        p.limb(bez((7, 4 - L), (12, -2 - L), (20, 4 - L)), 2.6, 3, h_crest, group=15)
        p.blob(11, 6.5 - L, 4.4, 4, h_bronze, group=7)
        p.poly([(7, 6 - L), (2.5, 7.5 - L), (7, 9 - L)], h_spur, group=9)
        p.px(9, 6 - L, "ink")
        p.pxs([(11, 15), (12, 15), (11, 16), (12, 17), (10, 14)], "ink")
        return

    if view in ("front", "side"):
        L = 1 if (phase == 1 and view == "front") else 0

        # the sickle tail: long feathers arching high over the back and
        # falling to the ground behind like a cloak
        for i, (pts, w) in enumerate((
                (((38, 21), (47, 3 + L), (61, 9 + L), (60.5, 34)), 7.6),
                (((39, 24), (50, 11 + L), (61.5, 22), (58.5, 47)), 7.6),
                (((39, 27), (50, 21), (59, 36), (54.5, 58.5)), 7.2),
                (((38, 30), (45.5, 31), (51, 47), (47.5, 60.5)), 6.6))):
            p.taper(bez3(*pts), w, h_tail, group=20 + i)
        # far leg braced back: feathered thigh, bronze greave, marble spur
        p.limb([(37, 39), (41.5, 47)], 9, 6, h_feather, bias=0.25, group=11)
        p.limb([(41.5, 47), (43.5, 58.5)], 4.6, 3.8, h_bronze, bias=0.25, group=12)
        p.taper([(43.5, 53), (48.5, 51.5)], 2.6, h_spur, group=12)
        for dx, dy in ((-6, 1.4), (-4.5, 2.4), (3.6, 1.2)):
            p.limb([(43.5, 58.8), (43.5 + dx, 58.8 + dy)], 2.2, 1.7, h_bronze, bias=0.25, group=12)
        # body: upright, the chest out behind the shield
        p.blob(33, 30, 10.4, 13.4, h_feather, group=1)
        # near leg planted forward
        p.limb([(29, 40), (25.5, 47.5)], 9.6, 6.6, h_feather, group=13)
        p.limb([(25.5, 47.5), (22.5, 58.5)], 5, 4.2, h_bronze, group=14)
        p.taper([(24.5, 53), (29.5, 51.5)], 2.8, h_spur, group=14)
        for dx, dy in ((-7, 1.4), (-5.5, 2.4), (3.8, 1.2)):
            p.limb([(22.5, 58.8), (22.5 + dx, 58.8 + dy)], 2.4, 1.8, h_bronze, group=14)
        # the shield wing folded across the chest
        p.circle(23, 33.5, 13, h_bronze, group=5)
        p.circle(23, 33.5, 9.8, h_field, group=6)
        # helmet and crest (the hand-finished art replaces these details)
        p.blob(25.5, 11.5 - L, 7.6, 7, h_bronze, group=7)
        p.blob(20.5, 16 - L, 4, 5.6, h_bronze, group=7)
        p.poly([(17, 12 - L), (9, 14.5 - L), (17, 17 - L)], h_spur, group=9)
        p.limb(bez3((17, 7 - L), (17, 0 - L), (36, 0 - L), (44.5, 6 - L)), 4.6, 6, h_crest, group=15)

        if p.big:
            p.eye(18, 10 - L, 3, 3, iris="terra2", shine="white", shine_at=(0, 0))
        else:
            p.px(19, 11 - L, "ink")
        return

    if view == "back":
        # over the shoulder: the shield's bronze back and the cypress
        # mantle, white hackles falling from the helmet, the crest sweeping
        # back over us; the helmeted head turned right
        for i, (pts, w) in enumerate(((((30, 56), (14, 50), (8, 30), (18, 16)), 7.4),
                                      (((32, 58), (19, 54), (15, 38), (24, 28)), 7))):
            p.taper(bez3(*pts), w, h_tail, group=20 + i)
        p.blob(36, 64, 21, 18, h_feather, group=1)
        p.blob(39, 47, 13, 10, h_feather, group=1)
        p.circle(13.5, 51, 12.5, h_bronze, bias=0.15, group=5)
        p.circle(13.5, 51, 9.6, h_bronze, bias=0.35, group=6)
        p.limb([(5, 48), (22, 54)], 3, 3, h_crest, group=7)
        for i, (a, b) in enumerate((((44, 34), (44, 52)), ((42, 34), (35, 52)), ((40, 33), (28, 49)),
                                    ((47, 34), (51, 49)))):
            p.lens(a, b, 7.6, h_hackle, bend=0.6 if i % 2 else -0.6, group=30 + i)
        p.blob(46, 22, 9.6, 9, h_bronze, group=8)
        p.blob(51, 28, 4.8, 6, h_bronze, group=8)
        p.poly([(56, 22), (62, 25), (56, 27.5)], h_spur, group=9)
        p.limb(bez3((53, 14), (52, 2), (34, 0.5), (27, 13)), 5, 6.6, h_crest, group=15)
        p.lens((29, 10), (26, 28), 6, h_crest, bend=-1, group=15)
        if p.big:
            p.eye(51, 18, 3, 3, iris="terra2", shine="white", shine_at=(2, 0))
        return

    if view in ("down", "up"):
        # follower marching toward or away from the camera
        st = phase
        p.limb([(28, 46), (27.5, 59 - 2 * st)], 3.6, 3, h_bronze, group=11)
        p.limb([(36, 46), (36.5, 59 - 2 * (1 - st))], 3.6, 3, h_bronze, group=12)
        for x, y in ((27.5, 59.5 - 2 * st), (36.5, 59.5 - 2 * (1 - st))):
            p.limb([(x, y), (x - 3, y + 1.5)], 2, 1.6, h_bronze)
            p.limb([(x, y), (x + 3, y + 1.5)], 2, 1.6, h_bronze)
        if view == "up":
            for i, (pts, w) in enumerate(((((29, 40), (17, 34), (17, 52 - st)), 7),
                                          (((35, 40), (47, 34), (47, 52 - (1 - st))), 7))):
                p.taper(bez(*pts), w, h_tail, group=20 + i)
        p.blob(32, 37, 9.6, 11, h_feather, group=1)
        for i, (a, b) in enumerate((((29, 26), (25, 38)), ((35, 26), (39, 38)), ((32, 26), (32, 40)))):
            p.lens(a, b, 7, h_hackle, group=30 + i)
        p.circle(21 if view == "down" else 43, 40, 7.6, h_bronze, group=5)
        p.circle(21 if view == "down" else 43, 40, 5.2, h_field if view == "down" else h_bronze, group=6)
        p.blob(32, 20, 7, 7, h_bronze, group=8)
        p.limb([(32, 18), (32, 6)], 5, 5.6, h_crest, group=15)
        if view == "down":
            p.poly([(30, 22), (34, 22), (32, 27)], h_spur, group=9)
            p.eye(27, 18, 2, 2, iris=None, shine=None)
            p.eye(35, 18, 2, 2, iris=None, shine=None)
        return


MONS = [
    Mon("Eopeep", EOPEEP_COLORS, EOPEEP_SHINY, eopeep, foot="bird", icon_pal=1),
    Mon("Alekrow", ALEKROW_COLORS, ALEKROW_SHINY, alekrow, foot="bird", icon_pal=3),
    Mon("Hoplektor", HOPLEKTOR_COLORS, HOPLEKTOR_SHINY, hoplektor, foot="bird", follow=28),
]
