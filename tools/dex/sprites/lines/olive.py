"""Olive line: Elaleaf, Elapling, Hierolive (Grass, then Grass/Fighting).
Athena's olive, the stump that sprouted after the fire, and Herakles's club."""
from mon_lib import C, Mat, Mon, bez

INK = C.ink

# --------------------------------------------------------------------------
# Elaleaf, the olive cutting
# --------------------------------------------------------------------------

ELALEAF_COLORS = [
    ("ink", INK),
    ("bk0", (96, 80, 64)), ("bk1", (144, 120, 88)), ("bk2", (184, 160, 120)), ("bk3", (216, 200, 160)),
    ("wood", (240, 232, 200)),
    ("lf0", (48, 72, 32)), ("lf1", (88, 112, 48)), ("lf2", (136, 160, 72)),
    ("sv0", (152, 168, 136)), ("sv1", (200, 216, 184)),
    ("fr0", (88, 120, 32)), ("fr1", (152, 176, 64)),
    ("white", C.white), ("blush", (216, 128, 104)),
]
ELALEAF_SHINY = {
    # sun-gold leaves and a black olive
    "lf0": (136, 88, 24), "lf1": (200, 136, 40), "lf2": (240, 192, 64),
    "sv0": (216, 168, 88), "sv1": (248, 224, 144),
    "fr0": (40, 32, 48), "fr1": (88, 72, 104),
}

e_bark = Mat(["bk0", "bk1", "bk2", "bk3"], line="bk0", cuts=[0.18, 0.42, 0.68])
e_root = Mat(["bk0", "bk1", "bk2"], line="bk0", cuts=[0.34, 0.62])
e_leaf = Mat(["lf0", "lf1", "lf2", "sv0"], line="lf0", cuts=[0.2, 0.46, 0.74])
e_under = Mat(["lf1", "sv0", "sv1"], line="lf1", cuts=[0.3, 0.6])
e_cut = Mat(["bk3", "wood"], line="bk2", cuts=[0.5])
e_fruit = Mat(["fr0", "fr1"], line="fr0", cuts=[0.5])


e_face = Mat(["bk3", "wood"], line="bk2", cuts=[0.5])


def elaleaf(p, view, phase):
    """The hand-finished battle art is the reference; this draft gives the
    icon and followers the same plump cutting: big ear-leaves, a pale face,
    the olive dangling like a toy."""
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        step = phase if view == "side" else 0
        for cx, cy, rx in ((36.6, 56 - step, 2.4), (26.4, 56.2 - (1 - step), 2.8)):
            p.blob(cx, cy, rx, 1.7, e_root, group=40)
        p.lens((35.4, 39.6 - L), (49.4, 29.6 - 3 * L), 8.0, e_under, bend=-1.8, fat=0.4)
        p.limb([(39, 46), (42.4, 44.6), (44.4, 45)], 2.6, 2.0, e_root)
        p.blob(44.6, 51.6, 3.4, 3.8, e_fruit)
        p.blob(31.4, 46.6, 9.6, 9.0, e_bark, group=1, bias=0.0 if p.big else -0.12)
        if p.big:
            p.blob(29.0, 48.4, 5.6, 4.2, e_face, group=2)
        p.lens((28.4, 39.6 - L), (14.6, 25.4 - 2 * L), 8.6, e_leaf, bend=1.6, fat=0.4)
        if p.big:
            p.eye(29, 42, 5, 6, shine="white", shine_at=(1, 1))
            p.eye(24, 43, 4, 5, shine="white", shine_at=(1, 1))
            p.pxs([(34, 48), (35, 48), (23, 48)], "blush")
            p.stroke([(28, 50), (29, 50)], "ink")
            p.px(43, 49, "white")
        else:
            p.pxs([(30, 44), (30, 45), (25, 45)], "ink")
            p.px(30, 43, "white")
            if p.s > 0.45:
                p.px(34, 48, "blush")
        return

    if view == "back":
        p.lens((37.6, 33.6), (55.4, 19.6), 10.4, e_under, bend=-2.2, fat=0.4)
        p.limb([(43, 44), (47, 42.6), (49.6, 43.2)], 3.2, 2.4, e_root)
        p.blob(49.6, 49.6, 4.0, 4.6, e_fruit)
        p.blob(31, 50, 14.4, 17.6, e_bark, group=1)
        p.lens((26.4, 33.6), (9.4, 15.6), 10.8, e_leaf, bend=2.0, fat=0.4)
        if p.big:
            p.eye(37, 38, 5, 5, shine="white", shine_at=(2, 1))
        return

    if view in ("down", "up"):
        step = phase
        for cx, cy in ((27.4, 56.4 - step), (36.6, 56.4 - (1 - step))):
            p.blob(cx, cy, 2.8, 1.7, e_root, group=40)
        lean = 1 - 2 * step
        if view == "up":
            p.lens((29, 39), (15, 27 + step), 8.4, e_leaf, bend=1.4, fat=0.4)
            p.lens((35, 39), (49, 27 + (1 - step)), 8.4, e_leaf, bend=-1.4, fat=0.4)
            p.blob(32, 47, 9.4, 9.0, e_bark, group=1)
            p.blob(42.6, 51 + lean * 0.5, 2.8, 3.2, e_fruit)
        else:
            p.lens((29, 39), (15, 27 + step), 8.4, e_under, bend=1.4, fat=0.4)
            p.lens((35, 39), (49, 27 + (1 - step)), 8.4, e_under, bend=-1.4, fat=0.4)
            p.blob(32, 47, 9.4, 9.0, e_bark, group=1)
            p.blob(32, 49, 6.4, 4.4, e_face, group=2)
            p.blob(43, 51 + lean * 0.5, 2.8, 3.2, e_fruit)
            p.eye(27, 43, 3, 4, shine="white", shine_at=(1, 1))
            p.eye(34, 43, 3, 4, shine="white", shine_at=(1, 1))
            if p.big:
                p.pxs([(25, 48), (39, 48)], "blush")
                p.stroke([(31, 50), (32, 50)], "ink")
        return


# --------------------------------------------------------------------------
# Elapling, the olive sapling that survived the fire
# --------------------------------------------------------------------------

ELAPLING_COLORS = [
    ("ink", INK),
    ("bk0", (72, 64, 56)), ("bk1", (112, 104, 88)), ("bk2", (160, 136, 104)), ("bk3", (208, 184, 144)),
    ("lf0", (48, 72, 32)), ("lf1", (88, 112, 48)), ("lf2", (136, 160, 72)), ("sv1", (192, 208, 176)),
    ("char", (40, 32, 32)), ("ember", (152, 64, 32)),
    ("shoot0", (96, 160, 40)), ("shoot1", (168, 216, 88)),
    ("fruit", (72, 56, 88)), ("white", C.white),
]
ELAPLING_SHINY = {
    # sun-gold foliage over pale marble bark
    "lf0": (136, 88, 24), "lf1": (200, 136, 40), "lf2": (240, 192, 64), "sv1": (248, 232, 160),
    "bk0": (136, 128, 120), "bk1": (184, 176, 168), "bk2": (216, 208, 192), "bk3": (248, 248, 240),
}

a_bark = Mat(["bk0", "bk1", "bk2", "bk3"], line="bk0", cuts=[0.18, 0.42, 0.68])
a_root = Mat(["bk0", "bk1", "bk2"], line="bk0", cuts=[0.34, 0.62])
a_leaf = Mat(["lf0", "lf1", "lf2", "sv1"], line="lf0", cuts=[0.2, 0.44, 0.72])
a_char = Mat(["char", "bk0"], line="ink", cuts=[0.6])
a_shoot = Mat(["shoot0", "shoot1"], line="lf0", cuts=[0.5])
a_fruit = Mat(["char", "fruit"], line="char", cuts=[0.5])


def _canopy(p, cx, cy, rx, ry, n=7, mat=None, **kw):
    """A small olive canopy: overlapping leaf clumps."""
    mat = mat or a_leaf
    import math
    pids = [p.blob(cx, cy, rx, ry, mat, group=50, **kw)]
    for i in range(n):
        a = math.pi * (0.95 + 1.1 * i / max(n - 1, 1))
        x, y = cx + rx * 0.82 * math.cos(a), cy + ry * 0.8 * math.sin(a)
        pids.append(p.blob(x, y, rx * 0.42, ry * 0.46, mat, group=50, **kw))
    return pids


A_CLUMPS = [(26, 17, 6.2, 4.6, 0.08), (38.6, 17.4, 6.0, 4.6, 0.14), (32, 13.6, 6.4, 4.2, 0.04),
            (31, 21, 10.6, 4.4, 0.0)]


def elapling(p, view, phase):
    """The hand-finished battle art is the reference; this draft gives the
    icon and followers the same boxer: fists up, scorched side, young crown."""
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        step = phase if view == "side" else 0
        lb = 0.0 if p.big else -0.18   # lighter bark when drawn small, so the icon keeps its warm tan
        p.limb([(38, 33), (44, 38.5), (42.4, 31.6 - L)], 5.0, 4.2, a_bark, bias=0.25 + lb, group=20)
        p.blob(41.6, 29.6 - L, 3.4, 3.1, a_bark, bias=0.2 + lb, group=20)
        for path, w in ((((39, 51), (43, 55.4), (47.4, 58.6 - (1 - step))), 4.4),
                        (((42, 52), (48.6, 55.8), (52, 56.6)), 3.0)):
            p.limb(list(path), w, 2.4, a_root, bias=0.25, group=41)
        p.poly([(26, 24), (38.6, 24), (40.2, 31), (38.8, 38), (39.6, 46), (42, 52.6), (24, 52.6), (26, 46),
                (26.6, 38), (24.8, 31)], a_bark, bias=lb, group=1)
        for path, w in ((((27, 51), (22.6, 55), (17.6, 58.6 - step)), 4.8), (((31, 52.6), (29, 58.8)), 4.0),
                        (((25, 50), (19, 52.6), (15.4, 53.6)), 3.0)):
            p.limb(list(path), w, 2.4, a_root, group=40)
        p.blob(34.6, 43, 2.6, 3.2, a_char, group=5)
        p.limb(bez((37, 41), (41, 39), (42, 33)), 1.6, 1.2, a_shoot, group=6)
        leafm = a_leaf if p.big else Mat(["lf1", "lf2"], line="lf0", cuts=[0.45])
        for cx, cy, rx, ry, bias in A_CLUMPS:
            p.blob(cx, cy - L, rx, ry, leafm, bias=bias)
        p.limb([(27, 33), (21.6, 38.6), (19.4, 32.4 - L)], 5.4, 4.6, a_bark, bias=lb, group=22)
        p.blob(19.0, 30.0 - L, 3.8, 3.4, a_bark, bias=lb, group=22)
        if p.big:
            p.eye(27, 29, 3, 3, shine="white", shine_at=(1, 1))
            p.eye(33, 29, 4, 3, shine="white", shine_at=(1, 1))
        else:
            p.px(28, 30, "ink")
            p.px(34, 30, "ink")
        return

    if view == "back":
        p.limb([(42, 40), (51, 44), (52.6, 34)], 6.4, 5.4, a_bark, group=20)
        p.blob(52.4, 30.8, 4.6, 4.2, a_bark, group=20)
        p.poly([(19, 27), (43, 27), (45.6, 36), (44, 46), (46, 56), (48, 64), (14, 64), (16, 56), (18, 46),
                (16.6, 36)], a_bark, group=1)
        for cx, cy, rx, ry, bias in ((23, 15.4, 8.0, 5.6, 0.06), (39.6, 15.6, 7.6, 5.6, 0.14),
                                     (31, 10.6, 8.0, 5.0, 0.04), (30.6, 21.6, 14.4, 5.2, 0.02)):
            p.blob(cx, cy, rx, ry, a_leaf, bias=bias)
        p.blob(41, 46, 3.6, 4.4, a_char, group=5)
        p.limb([(20, 40), (11, 44), (9.4, 34)], 6.4, 5.4, a_bark, group=22)
        p.blob(9.6, 30.6, 4.6, 4.2, a_bark, group=22)
        return

    if view in ("down", "up"):
        step = phase
        for path in (((28, 51), (24, 59 - 2 * step)), ((36, 51), (40, 59 - 2 * (1 - step)))):
            p.limb(list(path), 4.6, 2.4, a_root, group=40)
        p.poly([(26.5, 24), (37.5, 24), (38.5, 52), (25.5, 52)], a_bark, group=1)
        p.limb([(27, 32), (20, 37), (19, 29)], 4.4, 3.6, a_bark, group=22)
        p.limb([(37, 32), (44, 37), (45, 29)], 4.4, 3.6, a_bark, group=23)
        p.blob(19, 28, 3, 2.8, a_bark, group=22)
        p.blob(45, 28, 3, 2.8, a_bark, group=23)
        for cx, cy, rx, ry, bias in ((26, 17, 6, 4.6, 0.08), (38, 17, 6, 4.6, 0.12), (32, 13.6, 6.4, 4.2, 0.04),
                                     (32, 21, 10.6, 4.4, 0.0)):
            p.blob(cx, cy, rx, ry, a_leaf, bias=bias)
        if view == "up":
            p.blob(36, 42, 2.4, 3.4, a_char, group=5)
        else:
            p.eye(28, 29, 2, 3, shine="white")
            p.eye(34, 29, 2, 3, shine="white")
        return


# --------------------------------------------------------------------------
# Hierolive, the sacred olive, Herakles's club
# --------------------------------------------------------------------------

HIEROLIVE_COLORS = [
    ("ink", INK),
    ("bk0", (56, 48, 40)), ("bk1", (96, 80, 64)), ("bk2", (144, 120, 96)), ("bk3", (176, 152, 120)),
    ("bk4", (216, 192, 152)),
    ("cy0", (24, 40, 32)), ("cy1", (40, 72, 48)),
    ("lf0", (40, 64, 32)), ("lf1", (72, 104, 40)), ("lf2", (120, 152, 64)), ("sv1", (176, 200, 152)),
    ("sun", (224, 232, 152)), ("olive", (56, 40, 64)), ("gold", C.sungold[1]),
]
HIEROLIVE_SHINY = {
    # a sun-gold canopy and pale marble bark, like a tree in a temple painting
    "lf0": (136, 88, 24), "lf1": (192, 128, 40), "lf2": (232, 176, 56), "sv1": (248, 216, 112), "sun": (248, 248, 200),
    "bk0": (104, 96, 96), "bk1": (152, 144, 136), "bk2": (192, 184, 176), "bk3": (224, 216, 208), "bk4": (248, 248, 240),
}

h_bark = Mat(["bk0", "bk1", "bk2", "bk3", "bk4"], line="bk0", cuts=[0.14, 0.34, 0.56, 0.76])
h_root = Mat(["bk0", "bk1", "bk2"], line="bk0", cuts=[0.34, 0.62])
h_leaf = Mat(["lf0", "lf1", "lf2", "sv1", "sun"], line="lf0", cuts=[0.16, 0.38, 0.6, 0.8])
h_hollow = Mat(["cy0", "cy1"], line="ink", cuts=[0.5])
h_olive = Mat(["cy0", "olive"], line="cy0", cuts=[0.5])


def _club(p, x, y, r, **kw):
    """A knotted club-head: a big burl with smaller knots."""
    p.blob(x, y, r, r * 0.92, h_bark, **kw)
    p.blob(x - r * 0.55, y - r * 0.5, r * 0.5, r * 0.46, h_bark, **kw)
    p.blob(x + r * 0.5, y + r * 0.45, r * 0.46, r * 0.42, h_bark, **kw)


H_CLUMPS = [(13, 8.6, 7.0, 4.8, 0.14), (27, 5.8, 8.4, 4.2, 0.12), (40.5, 8.0, 7.2, 4.8, 0.16),
            (8.6, 14.4, 5.6, 4.4, 0.06), (46, 14.4, 5.4, 4.4, 0.12), (19.6, 11.4, 8.4, 5.8, -0.04),
            (34.4, 11.2, 8.6, 5.8, 0.0), (26.6, 16.6, 15.4, 3.8, 0.06)]
h_wreath = Mat(["lf1", "lf2", "sv1", "sun"], line="lf0", cuts=[0.25, 0.5, 0.75])


def hierolive(p, view, phase):
    """The hand-finished battle art is the reference; this draft gives the
    icon and followers the same giant: crown of clumps, wreath on the brow,
    one club raised over its shoulder, one forward."""
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        step = phase if view == "side" else 0
        lb = 0.0 if p.big else -0.14   # lighter bark when drawn small, so the icon keeps its warm tan
        p.limb([(43, 32), (51, 28), (55.4, 20), (56, 13 - L)], 8.8, 7.0, h_bark, bias=0.2, group=20)
        _club(p, 55.6, 9.2 - L, 6.2, bias=0.15, group=20)
        for path, w in ((((40, 54), (45, 58.6), (49, 60.4)), 5.6), (((25, 54), (21, 59.4), (17, 60.6)), 5.2)):
            p.limb(list(path), w, 3.2, h_root, bias=0.3, group=41)
        p.poly([(16.5, 18), (45.5, 18), (47.4, 26), (45.4, 33), (44, 40), (46, 48), (50, 54.6), (54, 57),
                (10, 57), (14.4, 54.6), (18.2, 48), (19.8, 40), (17.6, 33), (15.2, 26)], h_bark, bias=lb, group=1)
        for path, w in ((((18, 53), (11, 57.4), (5.4, 59.8 - step)), 6.4), (((26, 55), (23.6, 60.6)), 6.2),
                        (((35, 55.5), (36, 60.8)), 6.0), (((44, 54), (51, 58), (57.6, 59.8 - (1 - step))), 6.0)):
            p.limb(list(path), w, 3.6, h_root, group=40)
        p.blob(34, 44.4, 3.0, 4.2, h_hollow, group=5)
        leafm = h_leaf if p.big else Mat(["lf1", "lf2"], line="lf0", cuts=[0.45])
        for cx, cy, rx, ry, bias in H_CLUMPS:
            p.blob(cx, cy - L, rx, ry, leafm, bias=bias)
        p.poly([(15, 19.4 - L), (25, 21.4 - L), (47, 18.6 - L), (47, 22.4 - L), (25, 25.2 - L), (15, 23.2 - L)],
               h_wreath if p.big else Mat(["lf2", "sun"], line="lf1", cuts=[0.6]), group=6)
        p.limb([(21, 31), (14, 36), (11, 42)], 9.0, 7.4, h_bark, group=22)
        _club(p, 10.4, 45.6, 6.6, group=22)
        if p.big:
            p.eye(19, 27, 3, 2, iris=None, shine="gold", shine_at=(1, 1))
            p.eye(25, 27, 3, 2, iris=None, shine="gold", shine_at=(1, 1))
        else:
            p.px(20, 28 - L, "gold")
            p.px(26, 28 - L, "gold")
        return

    if view == "back":
        p.limb([(47, 42), (53, 51), (54.6, 58)], 9.6, 8.0, h_bark, group=20)
        p.poly([(12, 22), (48, 22), (51, 32), (49, 42), (52, 54), (55, 64), (6, 64), (11, 52), (13, 42), (10, 32)],
               h_bark, group=1)
        for cx, cy, rx, ry, bias in H_CLUMPS:
            p.blob(cx + 2, cy + 1, rx * 1.1, ry * 1.1, h_leaf, bias=bias)
        p.limb([(15, 40), (8, 33), (5.6, 24), (6.4, 15)], 10, 8, h_bark, group=22)
        _club(p, 7.6, 10.4, 6.2, group=22)
        return

    if view in ("down", "up"):
        step = phase
        for path in (((26, 52), (20, 59 - 2 * step)), ((38, 52), (44, 59 - 2 * (1 - step))), ((32, 54), (32, 59))):
            p.limb(list(path), 6, 3, h_root, group=40)
        p.limb([(23, 30), (14, 38), (13, 46)], 6, 5, h_bark, group=20)
        p.limb([(41, 30), (50, 24), (52, 14)], 6, 5, h_bark, group=21)
        _club(p, 13, 48, 4.6, group=20)
        _club(p, 52, 11, 4.6, group=21)
        p.poly([(21, 19), (43, 19), (45, 40), (46, 54), (18, 54), (19, 40)], h_bark, group=1)
        for cx, cy, rx, ry, bias in ((22, 9, 7, 4.6, 0.1), (42, 9, 7, 4.6, 0.12), (32, 6, 8, 4, 0.08),
                                     (32, 14, 15, 5, 0.0)):
            p.blob(cx, cy, rx, ry, h_leaf, bias=bias)
        p.poly([(18, 18.6), (46, 18.6), (46, 22.4), (18, 22.4)], h_wreath, group=6)
        if view == "down":
            p.eye(25, 26, 3, 2, iris=None, shine="gold", shine_at=(1, 1))
            p.eye(35, 26, 3, 2, iris=None, shine="gold", shine_at=(1, 1))
            p.blob(32, 44, 3.0, 4.2, h_hollow, group=5)
        return


MONS = [
    Mon("Elaleaf", ELALEAF_COLORS, ELALEAF_SHINY, elaleaf, foot="root", icon_pal=5),
    Mon("Elapling", ELAPLING_COLORS, ELAPLING_SHINY, elapling, foot="root", icon_pal=5),
    Mon("Hierolive", HIEROLIVE_COLORS, HIEROLIVE_SHINY, hierolive, foot="root", icon_pal=5),
]
