"""Laurel line: Nebrel, Kladoe, Daphnyad (Grass starter). Daphne and Apollo."""
from mon_lib import C, Mat, Mon, bez

INK = C.ink

# --------------------------------------------------------------------------
# Nebrel, the laurel fawn
# --------------------------------------------------------------------------

NEBREL_COLORS = [
    ("ink", INK),
    ("coat0", (112, 72, 40)), ("coat1", (160, 112, 64)), ("coat2", (200, 152, 96)), ("coat3", (232, 192, 136)),
    ("pale", (240, 224, 184)), ("white", C.white),
    ("leaf0", (40, 64, 32)), ("leaf1", (72, 104, 40)), ("leaf2", (120, 152, 64)), ("silver", (176, 192, 136)),
    ("gold", C.sungold[1]), ("bark", (72, 48, 40)),
]
NEBREL_SHINY = {
    "leaf0": (128, 64, 24), "leaf1": (192, 120, 32), "leaf2": (232, 176, 56), "silver": (248, 224, 136),
    "coat0": (136, 128, 128), "coat1": (176, 168, 160), "coat2": (208, 200, 192), "coat3": (232, 224, 216),
    "pale": (248, 248, 240),
}

coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.42, 0.68])
pale = Mat(["coat2", "coat3", "pale"], line="coat1", cuts=[0.4, 0.62])
leaf = Mat(["leaf0", "leaf1", "leaf2", "silver"], line="leaf0", cuts=[0.18, 0.42, 0.72])
hoof = Mat(["bark"])
twig = Mat(["bark", "coat0"], cuts=[0.5])


def _leaf(p, a, b, w, **kw):
    pid = p.lens(a, b, w, leaf, **kw)
    if p.big:
        # midrib
        p.stroke([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)], "leaf0")
    return pid


def _hoof(p, x, y, far=False):
    """A small cloven hoof whose top-left is at (x, y)."""
    p.rect(x, y, x + 2, y + 1, hoof, bias=0.3 if far else 0)
    if p.big:
        p.px(x + 1, y + 1, "ink")


def _spot(p, x, y):
    """A laurel-leaf spot, three pixels on a slant."""
    p.pxs([(x, y + 1), (x + 1, y), (x + 1, y + 1), (x + 2, y)], "white")


def nebrel(p, view, phase):
    if view in ("front", "side", "icon"):
        walk = view == "side"
        lift = 1 if (phase == 1 and not walk) else 0
        ear_up = 2 if lift else 0

        # legs: (hip, knee or hock, foot)
        if walk and phase:
            far_front = [(34, 49), (33, 55), (32, 59)]
            far_hind = [(43, 48), (46, 54), (45, 59)]
            near_front = [(30.5, 49), (30, 55), (29, 59)]
            near_hind = [(46, 47), (48, 53), (47, 59)]
        elif walk:
            far_front = [(34, 49), (35, 55), (35, 59)]
            far_hind = [(43, 48), (45, 54), (43, 59)]
            near_front = [(30.5, 49), (27.5, 54), (25.5, 58)]
            near_hind = [(46, 47), (50, 53), (50, 59)]
        else:
            far_front = [(34.5, 49), (34.5, 55), (34.5, 58.5)]
            far_hind = [(42, 49), (43.5, 54), (42.5, 58.5)]
            # mid-step: the near foreleg lifted, knee forward
            near_front = [(30, 49), (27, 53.5), (28.5, 56.5)]
            near_hind = [(46.5, 47), (50, 53.5), (48, 59.5)]

        p.limb(far_front, 4.6, 3.6, coat, bias=0.4, group=10)
        p.limb(far_hind, 4.8, 3.6, coat, bias=0.4, group=11)
        _hoof(p, int(far_front[-1][0]) - 1, 59, far=True)
        _hoof(p, int(far_hind[-1][0]) - 1, 59, far=True)

        # tail: an upright sapling sprig with two laurel leaves
        p.limb([(48.5, 42), (50, 38.5), (50.5, 35)], 2.6, 1.6, twig)
        _leaf(p, (50.5, 35.5), (57, 31.5), 4.4, bend=-0.8)
        _leaf(p, (50.5, 35), (53, 27.5), 4.2, bend=0.8, bias=0.1)

        # far ear, behind the head
        _leaf(p, (30.5, 21.5 - lift), (43, 11 - ear_up), 7.4, bend=1.3, bias=0.18)

        # body: chest, barrel and rump shaded as one form
        body = p.blob(38.5, 45.5, 9, 5.8, coat, ang=-5, group=1)
        p.blob(32.5, 45, 5.6, 5.8, coat, group=1)
        p.blob(45, 44, 5.4, 5.2, coat, group=1)
        p.blob(38, 50.2, 8, 2.2, pale, clip=[body], group=2)

        # neck, short and thick, then the big round head
        p.limb([(32.5, 43), (30.5, 37.5), (28, 33)], 8, 7.4, coat, group=1)
        p.blob(26, 27 - lift, 7.6, 7, coat, group=3)
        p.blob(18.5, 30.5 - lift, 5.2, 3.3, coat, ang=8, group=3)
        p.blob(19.5, 32.4 - lift, 4.2, 1.6, pale, ang=8, group=4)

        # near legs, over the body
        p.limb(near_front, 4.8, 3.8, coat, group=12)
        p.limb([(45.5, 45)] + near_hind, 7, 3.8, coat, group=13)
        fx, fy = near_front[-1]
        _hoof(p, int(fx) - 1, int(fy))
        _hoof(p, int(near_hind[-1][0]) - 1, 59)

        # near ear, in front of the head
        _leaf(p, (25, 21 - lift), (8.5, 12 - ear_up - lift), 7.6, bend=-1.4)

        # face
        L = lift
        p.eye(20, 24 - L, 4, 6, shine="white")
        if p.big:
            p.px(21, 28 - L, "gold")              # sun-gold glint
            p.pxs([(13, 29 - L), (14, 29 - L)], "ink")      # nose
            p.px(14, 30 - L, "ink")
            p.stroke([(15, 32 - L), (17, 32 - L)], "coat0")  # mouth
            p.px(23, 24 - L, "coat1")              # brow
            # chest tuft
            p.patch(28, 39, ["..w.", ".ww.", "wwwp", ".wwp", "..wp"],
                    {"w": "pale", "p": "coat3"})
            # laurel-leaf spots along the back
            for x, y in ((35, 41), (39, 40), (43, 40), (37, 44), (42, 44)):
                _spot(p, x, y)
            # leaf sheen along the upper edges
            p.pxs([(12, 14 - ear_up - L), (14, 15 - ear_up - L), (16, 16 - L)], "silver")
            p.pxs([(34, 17 - ear_up), (36, 15 - ear_up)], "silver")
        else:
            p.px(13, 29 - L, "ink")
        return

    if view == "back":
        # battle back: over the shoulder, head turned right in profile,
        # cropped by the bottom of the frame
        _leaf(p, (46, 15), (56, 2), 8.4, bend=-1.2, bias=0.2)
        p.blob(24, 59, 20, 14, coat, group=1)
        p.blob(34, 48, 10, 8, coat, group=1)
        p.limb([(34, 46), (37, 38), (40, 31)], 11.5, 10, coat, group=1)
        p.blob(42.5, 22, 9.2, 8.8, coat, group=3)
        p.blob(52, 25.5, 6.4, 4.4, coat, ang=-6, group=3)
        p.blob(51, 29.4, 5, 1.8, pale, ang=-6, group=4)
        p.limb([(12, 48), (10, 43), (9.5, 38)], 3.4, 2.4, twig)
        _leaf(p, (9.5, 38.5), (2, 34), 5.4, bend=-0.8)
        _leaf(p, (9.5, 38), (12, 29), 5.4, bend=0.8)
        _leaf(p, (38, 16), (22, 5), 9.4, bend=1.4)
        p.eye(47, 18, 4, 6, shine="white", shine_at=(1, 1))
        if p.big:
            p.px(48, 22, "gold")
            p.pxs([(58, 24), (58, 25)], "ink")
            p.stroke([(53, 28), (56, 28)], "coat0")
            for x, y in ((14, 50), (20, 48), (26, 46), (18, 54), (25, 52), (31, 50)):
                _spot(p, x, y)
        return

    if view == "up":
        # follower walking away: the whole fawn from behind
        p.limb([(35, 54), (37, 59), (37, 63)], 5, 4, coat, bias=0.4, group=10)
        p.limb([(46, 46), (48, 55), (48, 63)], 4.4, 3.4, coat, bias=0.45, group=11)
        _leaf(p, (44, 24), (32, 15), 8.5, bend=1.2)
        _leaf(p, (52, 23), (61, 13), 8.5, bend=-1.2, bias=0.1)
        p.limb([(43, 40), (46, 34), (47, 30)], 8.5, 8, coat, group=1)
        p.blob(48, 27, 7.2, 6.6, coat, group=3)
        p.blob(39, 43, 11.5, 8, coat, ang=-24, group=1)
        p.blob(29, 49, 11, 10, coat, group=1)
        p.limb([(24, 55), (22, 59), (22, 63)], 6, 5, coat, group=12)
        p.limb([(25, 41), (22, 36), (21, 32)], 3, 2, twig)
        _leaf(p, (21, 32), (12, 27), 5.5, bend=-0.8)
        _leaf(p, (21, 32), (22, 21), 5.5, bend=0.8)
        if p.big:
            for x, y in ((31, 41), (36, 38), (41, 35), (35, 45), (45, 38)):
                p.pxs([(x, y), (x + 1, y), (x + 1, y - 1)], "white")
        return

    if view == "down":
        step = phase
        p.blob(32, 47, 7.5, 7, coat, group=1)
        p.limb([(28.5, 51), (28.5, 61 - 2 * step)], 3.2, 2.6, coat, group=12)
        p.limb([(35.5, 51), (35.5, 61 - 2 * (1 - step))], 3.2, 2.6, coat, group=13)
        p.rect(27, 60 - 2 * step, 29, 61 - 2 * step, hoof)
        p.rect(34, 60 - 2 * (1 - step), 36, 61 - 2 * (1 - step), hoof)
        _leaf(p, (28, 30), (16, 24 + step), 6.5, bend=-1)
        _leaf(p, (36, 30), (48, 24 + step), 6.5, bend=1)
        p.blob(32, 33, 6.4, 6, coat, group=3)
        p.blob(32, 38, 3.6, 2.6, pale, group=3)
        p.eye(28, 31, 2, 3, shine="gold")
        p.eye(34, 31, 2, 3, shine="gold")
        p.px(32, 39, "ink")
        return


# --------------------------------------------------------------------------
# Kladoe, the laurel doe in flight
# --------------------------------------------------------------------------

KLADOE_COLORS = [
    ("ink", INK),
    # a deeper coat than the fawn's: the grown doe's shadows run darker
    ("coat0", (88, 48, 32)), ("coat1", (144, 96, 56)), ("coat2", (200, 152, 96)), ("coat3", (232, 192, 136)),
    ("pale", (240, 224, 184)), ("white", C.white),
    ("leaf0", (40, 64, 32)), ("leaf1", (72, 104, 40)), ("leaf2", (120, 152, 64)), ("silver", (176, 192, 136)),
    ("gold", C.sungold[1]),
    # laurel bark: cypress-dark, gray-green
    ("bark0", (40, 56, 48)), ("bark1", (72, 96, 80)), ("bark2", (120, 136, 112)),
]
KLADOE_SHINY = {
    "leaf0": (128, 64, 24), "leaf1": (192, 120, 32), "leaf2": (232, 176, 56), "silver": (248, 224, 136),
    "bark0": (72, 72, 80), "bark1": (120, 120, 128), "bark2": (176, 176, 184),
}

k_coat = Mat(["coat0", "coat1", "coat2", "coat3"], line="coat0", cuts=[0.16, 0.42, 0.68])
k_pale = Mat(["coat2", "coat3", "pale"], line="coat1", cuts=[0.4, 0.62])
k_leaf = Mat(["leaf0", "leaf1", "leaf2", "silver"], line="leaf0", cuts=[0.18, 0.42, 0.72])
k_bark = Mat(["bark0", "bark1", "bark2"], line="bark0", cuts=[0.34, 0.66])
k_twig = Mat(["bark0", "bark1"], line="bark0", cuts=[0.5])


def _kleaf(p, a, b, w, **kw):
    pid = p.lens(a, b, w, k_leaf, **kw)
    if p.big:
        p.stroke([a, ((a[0] * 2 + b[0]) / 3, (a[1] * 2 + b[1]) / 3)], "leaf0")
    return pid


def _brow_twigs(p, x, y, L=0):
    """Two short, antler-like laurel twigs on the brow, bases at (x, y) and
    (x + 6, y): a beam forking into a forward tine, a leaf on each tip."""
    # near twig: beam up and forward, forking
    p.limb(bez((x, y + 1), (x - 1, y - 3), (x - 4, y - 5 - L)), 2.6, 2.0, k_twig)
    p.limb([(x - 1, y - 2.5), (x + 1, y - 7 - L)], 2.0, 1.8, k_twig)
    _kleaf(p, (x - 4, y - 5 - L), (x - 9, y - 7 - L), 3.6, bend=0.6)
    _kleaf(p, (x + 1, y - 7 - L), (x + 1.5, y - 10 - L), 3.0, bend=-0.4)
    # far twig: straight up
    p.limb([(x + 6, y + 1), (x + 6.5, y - 6 - L)], 2.4, 1.9, k_twig, bias=0.1)
    _kleaf(p, (x + 6.5, y - 6 - L), (x + 7.5, y - 9.5 - L), 3.0, bend=0.4, bias=0.1)


def _khoof(p, x, y):
    """A cloven hoof, top-left at (x, y): 5 wide, 2 tall."""
    p.rect(x, y, x + 4, y + 1, Mat(["bark0", "bark1"], cuts=[0.5]))
    if p.big:
        p.px(x + 2, y + 1, "ink")


def kladoe(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        stride = view == "side" and phase == 1

        # far arm, the back arm of the stride: elbow thrown back
        p.limb([(39, 35), (46, 37.5)], 4.2, 3.6, k_coat, bias=0.3, group=20)
        p.limb([(46, 37.5), (48.5, 42)], 3.6, 3.0, k_coat, bias=0.3, group=20)
        # leaf mantle hanging from a twig collar and streaming back: a long
        # leaf behind, one hanging down the back, a lifted one on top
        _kleaf(p, (38, 28.5), (57, 28.5 - L), 6.6, bend=0.6, bias=0.2)
        _kleaf(p, (37.5, 31), (49, 38.5 - L), 5.6, bend=-0.8, bias=0.12)
        _kleaf(p, (35, 23.5), (48.5, 22.5 - L), 6.4, bend=0.8, bias=0.05)
        _kleaf(p, (33, 27), (42, 27.5), 4.6, bend=0.3)

        # far ear, raised behind the head
        _kleaf(p, (29, 12 - L), (39.5, 2.5 - L), 6.2, bend=1.0, bias=0.2)
        # far leg: forward and planted (back on the passing step)
        if stride:
            far_leg = [(37, 43), (38, 48.5), (42, 54), (41.5, 59)]
        else:
            far_leg = [(37, 43), (31.5, 48), (34, 54), (31.5, 59)]
        p.limb(far_leg[:2], 6.6, 5.2, k_coat, bias=0.3, group=10)
        p.limb(far_leg[1:], 4.6, 3.8, k_bark, bias=0.25, group=11)
        _khoof(p, int(far_leg[-1][0]) - 2, 59)

        # torso, leaning into the run
        body = p.limb([(31, 33), (37.5, 41)], 10, 8, k_coat, group=1)
        p.blob(30.5, 34, 5, 4.8, k_coat, group=1)
        p.blob(41, 44, 6, 5, k_coat, ang=-25, group=1)
        p.blob(28.8, 34.4, 3, 3.8, k_pale, clip=[body], group=2)
        p.limb([(30, 37.5), (35.5, 42.5)], 3.4, 2.2, k_pale, clip=[body], group=2)
        # neck and head
        p.limb([(30, 31), (27, 25)], 7, 6.4, k_coat, group=1)
        p.blob(23.5, 18.5 - L, 7.2, 6.6, k_coat, group=3)
        p.limb([(19, 21 - L), (13.5, 22.5 - L)], 6.4, 5.0, k_coat, group=3)
        p.blob(17.5, 24.6 - L, 3.8, 1.4, k_pale, ang=10, group=4)
        # near ear, a big leaf swept back
        _kleaf(p, (27, 15 - L), (46.5, 15 - L), 8.6, bend=0.6)
        # brow twigs
        _brow_twigs(p, 19, 11.5 - L, L)

        # near leg: pushing off behind (forward on the passing step)
        if stride:
            near_leg = [(42, 44), (36, 49), (38.5, 54.5), (35, 59)]
        else:
            near_leg = [(42, 44), (42.5, 49.5), (48, 54), (50.5, 59)]
        p.limb(near_leg[:2], 8, 5.8, k_coat, group=12)
        p.limb(near_leg[1:], 4.8, 4.0, k_bark, group=13)
        _khoof(p, int(near_leg[-1][0]) - 2, 59)

        # near arm: sprinter's front arm, hand up by the chin
        p.limb([(32, 31), (24.5, 37)], 5.2, 4.4, k_coat, group=21)
        p.limb([(24.5, 37), (16, 30)], 4.4, 3.6, k_coat, group=21)
        p.blob(15.5, 29.5, 2.4, 2.2, k_coat, group=21)

        if p.big:
            p.eye(19, 14 - L, 5, 6, shine="white", shine_at=(2, 1))
            p.px(20, 18 - L, "gold")
            p.px(25, 13 - L, "ink")                 # lash
            p.pxs([(11, 21 - L), (11, 22 - L), (12, 21 - L), (12, 22 - L)], "ink")   # nose
            p.stroke([(13, 23 - L), (16, 23 - L)], "coat0")                         # mouth
            p.pxs([(14, 28), (14, 29)], "bark0")    # hooflike fingertips
            for x, y in ((41, 43), (44, 46), (35, 33)):
                p.pxs([(x, y + 1), (x + 1, y), (x + 1, y + 1), (x + 2, y)], "white")
        else:
            p.px(20, 16 - L, "ink")
        return

    if view == "back":
        # battle back (the hand-finished art replaces this): over the
        # shoulder, head turned right, the leaf cape streaming
        _kleaf(p, (40, 15), (17, 11), 9, bend=1.2)
        p.blob(25, 65, 23.5, 19.5, k_coat, group=1)
        p.limb([(31, 50), (42, 30)], 13, 11, k_coat, group=1)
        p.blob(43, 21, 9, 8.5, k_coat, group=3)
        p.limb([(49, 24), (56.5, 26)], 9, 7.5, k_coat, group=3)
        _brow_twigs(p, 47, 13)
        _kleaf(p, (36, 44), (4, 34), 9, bend=1.0)
        _kleaf(p, (35, 48), (3, 47), 8, bend=0.2)
        _kleaf(p, (34, 51), (8, 59), 7, bend=-0.6)
        p.eye(46, 17, 4, 6, shine="white", shine_at=(1, 1))
        return

    if view == "down":
        # follower walking toward the camera
        step = phase
        p.limb([(29.5, 48), (29, 61 - 2 * step)], 4.6, 3.6, k_bark, group=12)
        p.limb([(34.5, 48), (35, 61 - 2 * (1 - step))], 4.6, 3.6, k_bark, group=13)
        _khoof(p, 27, 60 - 2 * step)
        _khoof(p, 33, 60 - 2 * (1 - step))
        _kleaf(p, (28, 33), (17, 42 + step), 6, bend=-0.8)
        _kleaf(p, (36, 33), (47, 42 + (1 - step)), 6, bend=0.8)
        p.blob(32, 46, 6.4, 4.6, k_coat, group=1)
        p.blob(32, 38.5, 6, 7, k_coat, group=1)
        p.blob(32, 37.5, 3, 5, k_pale, group=2)
        p.limb([(26, 34), (24, 43)], 3.6, 3, k_coat, group=20)
        p.limb([(38, 34), (40, 43)], 3.6, 3, k_coat, group=21)
        _kleaf(p, (27, 18), (14, 13 + step), 7.4, bend=-1.0)
        _kleaf(p, (37, 18), (50, 13 + (1 - step)), 7.4, bend=1.0)
        p.limb(bez((29.5, 15), (28, 10), (25, 7)), 2.4, 2, k_twig)
        p.limb(bez((34.5, 15), (36, 10), (39, 7)), 2.4, 2, k_twig)
        _kleaf(p, (25, 7), (22, 3.5), 3.2, bend=0.4)
        _kleaf(p, (39, 7), (42, 3.5), 3.2, bend=-0.4)
        p.blob(32, 21, 7, 6.6, k_coat, group=3)
        p.blob(32, 27, 4, 3.6, k_coat, group=3)
        p.blob(32, 29.2, 2.6, 1.4, k_pale, group=4)
        p.eye(27, 19, 2, 4, shine="white")
        p.eye(35, 19, 2, 4, shine="white")
        p.pxs([(31, 27), (32, 27)], "ink")
        return

    if view == "up":
        # follower walking away: the doe from behind, the cape on her back
        step = phase
        p.limb([(29.5, 48), (29, 61 - 2 * step)], 4.6, 3.6, k_bark, group=12)
        p.limb([(34.5, 48), (35, 61 - 2 * (1 - step))], 4.6, 3.6, k_bark, group=13)
        _khoof(p, 27, 60 - 2 * step)
        _khoof(p, 33, 60 - 2 * (1 - step))
        p.limb([(26, 34), (24, 43)], 3.6, 3, k_coat, group=20)
        p.limb([(38, 34), (40, 43)], 3.6, 3, k_coat, group=21)
        p.blob(32, 46, 6.4, 4.6, k_coat, group=1)
        p.blob(32, 38.5, 6, 7, k_coat, group=1)
        p.limb(bez((29.5, 15), (28, 10), (25, 7)), 2.4, 2, k_twig)
        p.limb(bez((34.5, 15), (36, 10), (39, 7)), 2.4, 2, k_twig)
        _kleaf(p, (25, 7), (22, 3.5), 3.2, bend=0.4)
        _kleaf(p, (39, 7), (42, 3.5), 3.2, bend=-0.4)
        p.blob(32, 21, 7, 6.6, k_coat, group=3)
        _kleaf(p, (27, 18), (14, 13 + step), 7.4, bend=-1.0)
        _kleaf(p, (37, 18), (50, 13 + (1 - step)), 7.4, bend=1.0)
        # the cape over the back
        _kleaf(p, (30, 30), (24, 46 + step), 7, bend=-0.6)
        _kleaf(p, (34, 30), (40, 46 + (1 - step)), 7, bend=0.6)
        _kleaf(p, (32, 30), (32, 48), 6.4)
        if p.big:
            for x, y in ((29, 42), (34, 44)):
                p.pxs([(x, y + 1), (x + 1, y), (x + 1, y + 1), (x + 2, y)], "white")
        return


# --------------------------------------------------------------------------
# Daphnyad, the laurel dryad
# --------------------------------------------------------------------------

from mon_lib import bez3, lens_pts  # noqa: E402

DAPHNYAD_COLORS = [
    ("ink", INK),
    # pale marble skin with warm limestone shadows, after the fawn's coat
    ("skin0", (168, 128, 104)), ("skin1", (216, 184, 152)), ("skin2", (240, 224, 200)), ("marble", (248, 248, 240)),
    # deep laurel green with a silver sheen on the leaf tops
    ("leaf0", (24, 64, 40)), ("leaf1", (56, 112, 48)), ("leaf2", (112, 160, 64)), ("silver", (184, 208, 136)),
    # cypress-dark bark
    ("bark0", (40, 48, 48)), ("bark1", (72, 88, 80)), ("bark2", (104, 120, 104)), ("bark3", (152, 160, 136)),
    ("gold0", (192, 120, 32)), ("gold", (240, 200, 72)),
]
DAPHNYAD_SHINY = {
    "leaf0": (128, 64, 24), "leaf1": (192, 120, 32), "leaf2": (232, 176, 56), "silver": (248, 224, 136),
    "bark0": (96, 88, 96), "bark1": (160, 152, 152), "bark2": (208, 200, 192), "bark3": (240, 240, 232),
}

d_skin = Mat(["skin0", "skin1", "skin2", "marble"], line="skin0", cuts=[0.24, 0.52, 0.8])
d_leaf = Mat(["leaf0", "leaf1", "leaf2", "silver"], line="leaf0", cuts=[0.2, 0.46, 0.76])
d_bark = Mat(["bark0", "bark1", "bark2", "bark3"], line="bark0", cuts=[0.16, 0.42, 0.74])
d_twig = Mat(["bark0", "bark1", "bark2"], line="bark0", cuts=[0.4, 0.72])
d_berry = Mat(["gold0", "gold"], line="gold0", cuts=[0.55])


def _dleaf(p, a, b, w, bend=0.0, depth=1, **kw):
    """A long, pointed laurel leaf from a (stalk) to b (tip), split along its
    midrib into a lit half and a shaded half, flat-toned like a Gen 3 leaf.
    depth 0 is a front leaf with a silver sheen, 2 a dark leaf at the back."""
    import math
    kw.pop("bias", None)
    lit, shade = ((2, 1), (2, 1), (1, 1))[depth]
    pts = lens_pts(a, b, p._minw(w), bend, fat=0.42)
    if not p.big:
        return p.poly(pts, d_leaf, flat=lit if depth < 2 else shade, **kw)
    pid = p.poly(pts, d_leaf, flat=shade, **kw)
    n = len(pts) // 2
    left, right = pts[:n], pts[n:][::-1]
    mid = [((u[0] + v[0]) / 2, (u[1] + v[1]) / 2) for u, v in zip(left, right)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    edge = left if dy - dx > 0 else right            # the half facing the upper-left light
    kw.pop("group", None)
    p.poly(edge + mid[::-1], d_leaf, clip=[pid], flat=lit, noline=True, **kw)
    if depth == 0:
        # a silver sheen just inside the lit edge, near the widest part
        for i in (int(n * 0.36), int(n * 0.5)):
            ex, ey = edge[i]
            mx, my = mid[i]
            d = math.hypot(mx - ex, my - ey) or 1
            k = min(1.5, d * 0.6) / d
            p.px(ex + (mx - ex) * k - 0.5, ey + (my - ey) * k - 0.5, "silver")
    return pid


def _dleaves(p, leaves, sw=0):
    """Laurel leaves at absolute positions: [(bx, by, tx, ty, width, bend,
    depth), ...]; sw sways every tip sideways (frame 2)."""
    for bx, by, tx, ty, w, bend, dp in leaves:
        _dleaf(p, (bx, by), (tx + sw, ty), w, bend=bend, depth=dp)


def _berry(p, x, y):
    p.circle(x, y, 1.5, d_berry)
    if p.big:
        p.px(x - 0.6, y - 0.6, "marble")


def _dwreath(p, x, y):
    """The laurel wreath across the crown, front end at (x, y): small leaves
    fanning up and out, with sun-gold berries."""
    for a, b, dp in (((x + 1, y + 2), (x - 3.5, y - 1.5), 0), ((x + 3.5, y), (x + 1.5, y - 5), 0),
                     ((x + 7, y - 1), (x + 7.5, y - 6), 1), ((x + 10.5, y - 0.5), (x + 13, y - 5.5), 1),
                     ((x + 13, y + 1), (x + 17.5, y - 1.5), 2)):
        _dleaf(p, a, b, 4.0, bend=0.4, depth=dp)
    for bx, by in ((x + 2, y + 0.5), (x + 6, y - 2), (x + 10.5, y - 1.5)):
        _berry(p, bx, by)


def daphnyad(p, view, phase):
    if view == "icon":
        # party icon: the front pose simplified for 32 px, with a big head
        # and bold leaves so the face and the canopy read at a glance
        p.poly([(29, 40), (39, 40), (44, 47), (52, 56), (16, 56), (24, 47)], d_bark, group=30)
        for path in ([(20, 55), (14, 60)], [(31, 56), (30, 61)], [(42, 56), (48, 60)]):
            p.limb(path, 4.6, 2.4, d_bark, group=31)
        p.limb([(39, 33), (47, 27), (50, 18)], 5, 4, d_skin, bias=0.3, group=20)
        _dleaves(p, [(50, 18, 44, 8, 9, 0.8, 2), (50, 18, 58, 10, 9, -0.8, 2), (50, 18, 52, 6, 8, 0, 1)])
        _dleaf(p, (38, 20), (48, 38), 10, bend=-1.4, depth=2)
        p.limb([(33, 32), (34.5, 41)], 11, 8, d_skin, group=1)
        p.blob(33, 20, 12.5, 11, d_leaf, group=40, flat=1)
        _dleaf(p, (38, 15), (58, 11), 9, bend=-1.8, depth=0)
        p.blob(29, 24, 7.6, 8, d_skin, group=3, flat=3)
        _dleaf(p, (39, 12), (21, 19), 7.5, bend=1.6, depth=0, group=41)
        p.limb(bez((30, 33), (21, 31), (16, 24)), 6, 5, d_skin, group=22)
        p.limb([(16, 25), (13, 16)], 5, 4, d_bark, group=23)
        _dleaves(p, [(13, 16, 3, 12, 9, 0.8, 1), (13, 16, 8, 4, 9, 0.8, 0), (13, 16, 20, 8, 8.5, -0.8, 0)])
        for x, y in ((25, 12), (31, 9.5), (37, 10.5), (13, 13), (50, 15)):
            _berry(p, x, y)
        p.pxs([(25.5, 24), (25.5, 25), (31.5, 24), (31.5, 25)], "ink")
        return

    if view in ("front", "side"):
        # Bernini's Daphne: the near arm flung high and branching into a
        # laurel bough, the far arm reaching up and back, the body in an S
        # curve sinking into a flared bark gown that roots into the ground,
        # the head tilted back under a helmet of laurel-leaf hair
        sw = 1 if (phase == 1 and view == "front") else 0     # boughs and hair sway
        L = sw                                                 # head tilt

        # far arm and its bough, behind everything and in shade
        p.limb([(49, 13.5), (51.5, 8), (54, 3.8)], 3.0, 1.8, d_twig, bias=0.28)
        p.limb([(51, 10.5), (56 - sw, 10.5)], 2.4, 1.4, d_twig, bias=0.28)
        _dleaves(p, [(50, 12.5, 44.5, 12, 5.2, 0.6, 2), (50.6, 10, 45, 5, 5.6, 0.7, 2),
                     (53.5, 5, 50.8, 1.8, 5.0, 0.5, 2), (54, 11, 57.5, 16.5, 5.4, 0.6, 2),
                     (55.5, 10.5, 61.5, 9, 5.4, -0.6, 2), (52.2, 7, 58.5, 4.2, 5.6, -0.7, 1),
                     (54, 4, 56.5, 1.6, 4.6, -0.3, 1)], -sw)
        p.limb(bez((38, 30.5), (43.5, 28.5), (46, 22.5)), 5.2, 4.4, d_skin, bias=0.32, group=20)
        p.limb(bez((46, 22.5), (48, 18), (49, 13.5)), 4.4, 3.4, d_bark, bias=0.25, group=21)

        # far leaf-ear, raised behind the head
        _dleaf(p, (34, 10.5 - L), (46, 2.2 - L), 5.8, bend=1.2, depth=2)

        # laurel-leaf hair falling down her back, behind the shoulders
        _dleaf(p, (36, 10 - L), (52, 19 + sw), 7.4, bend=-1.6, group=50)
        _dleaf(p, (36, 14 - L), (50, 28 + sw), 7.4, bend=-1.4, group=51)
        _dleaf(p, (35, 18 - L), (46, 35 + sw), 7.0, bend=-1.0, depth=2, group=52)
        _dleaf(p, (34, 22 - L), (40.5, 39 + sw), 6.0, bend=-0.6, depth=2, group=53)

        # the gown: bark flaring from the waist like a bell to a hem that
        # splits into roots gripping the ground
        left = bez3((31.2, 39), (29.6, 46.5), (23.5, 53.5), (11.5, 57.2))
        right = bez3((58.5, 57.2), (47.5, 53.5), (42, 46.5), (40, 39))
        hem = [(15, 58.4), (21, 57.8), (27, 58.6), (33, 58), (39, 58.6), (45, 57.8), (51, 58.4), (55.5, 57.8)]
        p.poly(left + hem + right, d_bark, group=30, bias=-0.1)
        for path, w0 in (([(15, 57), (10, 59.6), (5.5, 61)], 4.0), ([(23.5, 57.6), (21.5, 60), (18, 61.5)], 4.4),
                         ([(32.5, 58), (33, 60.2), (30.5, 61.6)], 4.6), ([(41.5, 58), (43.5, 60.2), (47, 61.5)], 4.6),
                         ([(51.5, 57.6), (55.5, 59.6), (60, 61)], 4.0)):
            p.limb(path, w0, 1.8, d_bark, group=31)

        # torso in an S: chest forward, waist, hips back into the gown
        p.limb([(32, 32), (34, 37.5), (35.5, 42)], 11, 7.6, d_skin, group=1)
        p.blob(31.5, 32.5, 6.6, 5.0, d_skin, ang=-15, group=1)
        # the bark bodice climbing from the waist in tongues
        p.poly([(29.2, 46), (29.6, 39), (31, 40.2), (32.2, 35.8), (33.6, 39.2), (35.2, 34.2), (36.6, 38.6),
                (38, 36.4), (39, 40), (41.4, 46)], d_bark, group=30)

        # neck, hair helmet, face
        p.limb([(28.5, 24 - L), (30.5, 30.5)], 4.6, 5.6, d_skin, group=1)
        p.blob(30.5, 13.5 - L, 10.5, 9, d_leaf, group=40, flat=1)
        # sculpted leaves over the crown, sweeping forward from the back
        _dleaf(p, (41, 15 - L), (32, 6 - L), 7.0, bend=-1.0, group=44)
        _dleaf(p, (39, 10 - L), (21, 7 - L), 7.4, bend=-1.6, depth=0, group=45)
        p.blob(26.5, 19.5 - L, 6.6, 7.0, d_skin, ang=-6, group=3, flat=3)
        # bangs arching over the eyes, and the locks framing the cheeks
        _dleaf(p, (39, 11 - L), (33.5, 17.5 - L), 5.0, bend=0.6, group=43)
        _dleaf(p, (34, 9.5 - L), (28, 15 - L), 4.6, bend=0.8, depth=0, group=46)
        _dleaf(p, (31, 8.5 - L), (21, 16.5 - L), 6.2, bend=1.4, depth=0, group=41)
        _dleaf(p, (22, 10 - L), (19, 25.5 - L), 4.6, bend=0.8, group=42)

        # near leaf-ear sweeping back from the temple
        _dleaf(p, (35, 13.5 - L), (56.5, 8 - L - sw), 7.0, bend=-1.8, depth=0)
        # the wreath
        _dwreath(p, 22, 8 - L)

        # near arm flung high, turning to bark from the forearm
        p.limb(bez((28, 31), (21, 30), (15.5, 25.5)), 6.0, 5.0, d_skin, group=22)
        p.limb(bez((15.5, 25.5), (13.5, 23), (12.5, 21)), 5.0, 4.6, d_skin, group=22)
        p.limb(bez((13, 22), (11, 18.5), (10, 15)), 4.6, 3.8, d_bark, group=23)
        # and its bough: a twig that branches into a broad canopy
        p.limb([(10.5, 16), (9.5, 10), (9 + sw, 5)], 3.0, 1.8, d_twig)
        p.limb([(10, 13), (6 + sw, 12.5)], 2.4, 1.4, d_twig)
        p.limb([(9.8, 9), (13.5 + sw, 6.5)], 2.2, 1.4, d_twig)
        _dleaves(p, [(10.8, 12, 17, 11, 5.4, -0.6, 2), (9.6, 14.5, 2.2, 18, 5.6, -0.8, 1),
                     (9.2, 9, 3, 4, 5.8, 0.8, 1), (11.5, 7.6, 13.5, 1.8, 5.4, -0.6, 1),
                     (8, 12.6, 1.8, 10.5, 6.0, 0.8, 0), (13.5, 6.6, 20, 5, 5.6, -0.7, 0),
                     (9.1, 5.5, 8.2, 1.6, 5.0, 0.4, 0)], sw)
        for x, y in ((6 + sw, 12.5), (13.8 + sw, 6.5), (9.8, 10), (56 - sw, 10.5)):
            _berry(p, x, y)

        # the face: big serene gold eyes under the bangs, each with a white
        # shine and a dark lash (the art file hand-finishes the face)
        if p.big:
            p.patch(22, 16 - L, [".........1", "111...1111", "e5e..1e5e1", "f1f..1f1f.", "ef....fff.", ".......e.."],
                    {"1": "ink", "e": "gold0", "f": "gold", "5": "marble"})
        else:
            p.px(28.5, 19 - L, "ink")
            p.px(23, 19 - L, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the head turned right in profile,
        # the laurel hair cascading down her back, the near arm raised into a
        # bough, the bark gown climbing from below
        # back and shoulders, cropped by the frame
        p.blob(32, 55, 29, 16, d_skin, group=1)
        p.limb([(46, 31), (43.5, 40)], 7.4, 10, d_skin, group=1)
        # the bark gown climbing her back in tongues
        p.poly([(2, 64), (3, 56), (7, 54), (10, 50), (13.5, 53.5), (17, 48.5), (21, 52.5), (26, 48), (31, 52.5),
                (36, 49), (41, 53), (46, 50), (50, 54), (55, 52), (59, 55), (62, 64)], d_bark, group=30)
        # hair helmet, then the face in profile
        p.blob(36, 20, 13, 12, d_leaf, group=40, flat=1)
        p.blob(48.5, 23, 6.4, 9, d_skin, ang=-8, group=3, flat=3)
        # the great fall of laurel-leaf hair down her back
        _dleaf(p, (36, 26), (24, 55), 9.6, bend=2.0, group=50)
        _dleaf(p, (32, 22), (12, 48), 9.0, bend=2.2, depth=2, group=51)
        _dleaf(p, (40, 29), (37, 57), 8.4, bend=1.0, group=52)
        _dleaf(p, (34, 28), (30, 58), 8.0, bend=1.6, depth=0, group=53)
        _dleaf(p, (30, 17), (14, 36), 8.4, bend=1.8, group=54)
        # crown leaves sweeping back from the brow
        _dleaf(p, (46, 11), (27, 13), 8.0, bend=1.8, depth=0, group=55)
        _dleaf(p, (45, 16), (30, 26), 7.8, bend=1.6, group=56)
        # bangs over the brow
        _dleaf(p, (40, 10), (54, 16), 6.8, bend=-1.6, depth=0, group=57)
        # the leaf-ear sweeping back from the temple
        _dleaf(p, (39, 15), (19, 4), 7.8, bend=2.0, depth=0, group=59)
        _dwreath(p, 30, 10)
        # near arm raised, becoming a bough
        p.limb(bez((14, 47), (7.5, 42), (8, 34)), 9.4, 7.6, d_skin, group=22)
        p.limb(bez((8, 35), (8.5, 30), (9, 26)), 7.4, 5.6, d_bark, group=23)
        p.limb([(9, 27), (8, 16), (7.5, 6)], 4.4, 2.4, d_twig)
        p.limb([(8.5, 21), (14, 16.5), (18.5, 12)], 3.0, 1.8, d_twig)
        p.limb([(8, 14), (3.5, 11)], 2.8, 1.6, d_twig)
        _dleaves(p, [(14, 16.5, 21.5, 20, 6.4, -0.8, 2), (11, 19, 15.5, 26, 6.0, 0.7, 2),
                     (8.6, 23, 2, 27.5, 7.0, -0.8, 1), (8.3, 17.5, 1.6, 17, 7.0, 0.8, 1),
                     (7.8, 12, 2.2, 5.5, 7.0, 0.8, 0), (16.5, 14.5, 18.5, 6, 6.6, -0.7, 0), (18.5, 12, 25.5, 11, 6.2, -0.6, 1),
                     (7.6, 7.5, 11.5, 1.8, 6.0, -0.5, 0), (12, 11, 13, 4.5, 5.6, 0.4, 1)])
        for x, y in ((4, 11.5), (13.5, 17), (19, 12)):
            _berry(p, x, y)
        if p.big:
            p.patch(49, 20, ["11111", "e5ee", "f1fe", ".ff"], {"1": "ink", "e": "gold0", "f": "gold", "5": "marble"})
        return

    if view in ("down", "up"):
        # follower: gliding on her roots with both boughs raised; the boughs
        # and the root-hem sway in turn
        sw = phase
        p.poly([(27, 40), (37, 40), (41, 46), (48, 54.5), (16, 54.5), (23, 46)], d_bark, group=30,
               bias=-0.05 if view == "down" else 0.05)
        for path in (([(19, 54), (13, 58 + sw)]), ([(27, 54.5), (25.5, 60 - sw)]), ([(37, 54.5), (38.5, 60 - (1 - sw))]),
                     ([(45, 54), (51, 58 + (1 - sw))])):
            p.limb(path, 4.6, 2.2, d_bark, group=31)
        # arms raised, turning to bark, and their boughs
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            p.limb(bez((X(27), 32), (X(19), 30), (X(15.5), 21)), 5.4, 4.4, d_skin, group=22 if sx < 0 else 24)
            p.limb([(X(15.5), 22), (X(13.5), 13)], 4.4, 3.4, d_bark, group=23 if sx < 0 else 25)
            s = sw if sx < 0 else 1 - sw
            _dleaves(p, [(X(13.5), 13, X(4.5), 10 + s, 7.4, 0.8 * sx, 1), (X(13.5), 13, X(8), 3.5 + s, 7.4, 0.8 * sx, 0),
                         (X(13.5), 13, X(18.5), 5 + s, 6.8, -0.8 * sx, 1), (X(13.5), 14, X(6), 17 + s, 6.6, -0.8 * sx, 2)])
            _berry(p, X(13.5), 12)
        # the leaf-ears sweeping up and out from the temples
        _dleaf(p, (26, 14), (18, 3), 6.6, bend=1.2, depth=0)
        _dleaf(p, (38, 14), (46, 3), 6.6, bend=-1.2, depth=0)
        if view == "down":
            # hair falling behind the shoulders, the torso, the face
            _dleaf(p, (25, 18), (22, 34), 7, bend=-1.0, depth=2)
            _dleaf(p, (39, 18), (42, 34), 7, bend=1.0, depth=2)
            p.limb([(32, 29), (32, 41)], 10, 7, d_skin, group=1)
            p.poly([(27, 41.5), (28, 37), (29.5, 39), (31, 35.5), (32.5, 39), (34, 36), (35.5, 39), (36.5, 37), (37.5, 41.5)],
                   d_bark, group=30)
            p.blob(32, 17, 10.5, 9.5, d_leaf, group=40, flat=1)
            p.blob(32, 21, 6.8, 7.2, d_skin, group=3, flat=3)
            _dleaf(p, (33, 10), (24, 17.5), 6.2, bend=1.2, depth=0, group=41)
            _dleaf(p, (31, 10), (40, 17.5), 6.2, bend=-1.2, group=42)
            _dleaf(p, (25.5, 13), (23.5, 27), 4.6, bend=-0.6, group=43)
            _dleaf(p, (38.5, 13), (40.5, 27), 4.6, bend=0.6, group=44)
            p.eye(27, 19, 3, 5, iris="gold", shine="marble", shine_at=(1, 1))
            p.eye(34, 19, 3, 5, iris="gold", shine="marble", shine_at=(1, 1))
        else:
            p.limb([(32, 29), (32, 41)], 10, 7, d_skin, group=1)
            p.blob(32, 18, 10.5, 10, d_leaf, group=40, flat=1)
            for a, b, bend, dp in (((30, 18), (25, 42), -1.4, 2), ((34, 18), (39, 42), 1.4, 2), ((32, 19), (32, 45), 0.0, 0)):
                _dleaf(p, a, b, 9, bend=bend, depth=dp)
            _dleaf(p, (32, 9), (24, 17), 6.2, bend=1.2, depth=0)
            _dleaf(p, (32, 9), (40, 17), 6.2, bend=-1.2, depth=1)
        _dwreath(p, 25, 11)
        return


MONS = [
    Mon("Nebrel", NEBREL_COLORS, NEBREL_SHINY, nebrel, foot="hoof"),
    # icon palette 5 keeps both the greens and the tan coat
    Mon("Kladoe", KLADOE_COLORS, KLADOE_SHINY, kladoe, foot="hoof", icon_pal=5),
    Mon("Daphnyad", DAPHNYAD_COLORS, DAPHNYAD_SHINY, daphnyad, foot="root", icon_pal=5),
]
