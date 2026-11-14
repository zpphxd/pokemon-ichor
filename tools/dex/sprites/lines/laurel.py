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

DAPHNYAD_COLORS = [
    ("ink", INK),
    ("coat0", (112, 72, 40)), ("coat1", (160, 112, 64)), ("coat2", (200, 152, 96)), ("coat3", (232, 192, 136)),
    ("marble", (248, 240, 224)),
    ("leaf0", (40, 64, 32)), ("leaf1", (72, 104, 40)), ("leaf2", (120, 152, 64)), ("silver", (176, 192, 136)),
    ("gold", C.sungold[1]), ("gold0", (184, 112, 32)),
    ("bark0", (40, 56, 48)), ("bark1", (72, 96, 80)), ("bark2", (120, 136, 112)),
]
DAPHNYAD_SHINY = {
    "leaf0": (128, 64, 24), "leaf1": (192, 120, 32), "leaf2": (232, 176, 56), "silver": (248, 224, 136),
    "bark0": (128, 120, 112), "bark1": (192, 184, 168), "bark2": (232, 224, 208),
}

d_skin = Mat(["coat1", "coat2", "coat3", "marble"], line="coat0", cuts=[0.2, 0.46, 0.74])
d_leaf = Mat(["leaf0", "leaf1", "leaf2", "silver"], line="leaf0", cuts=[0.2, 0.44, 0.76])
d_bark = Mat(["bark0", "bark1", "bark2"], line="bark0", cuts=[0.34, 0.66])
d_berry = Mat(["gold0", "gold"], line="gold0", cuts=[0.55])


def _dleaf(p, a, b, w, **kw):
    pid = p.lens(a, b, w, d_leaf, **kw)
    if p.big:
        p.stroke([a, ((a[0] * 2 + b[0]) / 3, (a[1] * 2 + b[1]) / 3)], "leaf0")
    return pid


def _spray(p, base, tips, w=4.4, twig=1.8, **kw):
    """A laurel branch end: twigs from base to each tip, a leaf at each."""
    for tip, bend in tips:
        mid = ((base[0] + tip[0]) / 2, (base[1] + tip[1]) / 2)
        p.limb([base, mid], twig, twig * 0.8, d_bark)
        _dleaf(p, mid, tip, w, bend=bend, **kw)


def _berry(p, x, y):
    p.circle(x, y, 1.3, d_berry)
    if p.big:
        p.px(x - 0.5, y - 0.6, "marble")


def daphnyad(p, view, phase):
    if view in ("front", "side", "icon"):
        # Bernini's Daphne: the body sinking into a rooted bark gown in an
        # S-curve, the near arm flung up and forward into a bough, the far arm
        # swept up and back, the head tilted toward the sky
        sw = 1 if (phase == 1 and view != "icon") else 0     # the boughs sway

        # far arm and bough, behind and in shade
        p.limb(bez((35.5, 30.5), (41.5, 26.5), (44, 19)), 4.4, 3.8, d_skin, bias=0.3, group=20)
        p.limb(bez((44, 19), (45.5 + sw, 15), (47 + sw, 10.5)), 3.8, 2.4, d_bark, bias=0.2, group=21)
        for a, b, w, bend in (((47.5 + sw, 10.5), (57 + 2 * sw, 3 + sw), 7.2, -1.1), ((48 + sw, 12.5), (61 + sw, 12.5 - sw), 7.0, -0.8),
                              ((46.5 + sw, 10), (41.5 + sw, 2.5), 6.0, 0.8), ((47.5 + sw, 14.5), (56.5 + sw, 21 - sw), 6.2, 0.7)):
            _dleaf(p, a, b, w, bend=bend, bias=0.22)
        # rooted gown flaring to a hem of roots, bigger roots in front
        p.poly([(29.6, 41), (39, 41), (41, 43), (42.6, 45.5), (44.8, 49), (47.6, 52.4), (51.5, 55.6), (22.5, 55.6),
                (25.8, 52.5), (27.6, 49.5), (28.8, 46)], d_bark, group=30)
        for path, w0 in (([(47, 53), (53, 54.5), (58.5, 55.5)], 3.4), ([(25.5, 53), (21, 53.5), (17, 54)], 3.0),
                         ([(44, 54), (49, 57), (53.5, 59.5)], 4.6), ([(38, 55), (39.5, 58.5), (38.5, 61)], 4.6),
                         ([(32.5, 55), (30, 58.5), (26.5, 61.5)], 5.6), ([(27, 54), (19, 57.5), (10, 60.5)], 6.0)):
            p.limb(path, w0, 2.2, d_bark, group=31)
        # torso in an S-curve, bark climbing the waist in tongues
        p.blob(30.2, 33, 6.2, 5.0, d_skin, group=1)
        p.limb([(30.6, 34), (33.8, 41)], 9.0, 6.6, d_skin, group=1)
        p.poly([(28, 42), (29, 37), (30.5, 41), (33, 35), (35, 41), (37, 38), (39, 42)], d_bark, group=30)
        p.limb([(30.5, 30), (27.5, 20.5)], 6.0, 5.2, d_skin, group=1)
        # leaf-ears streaming back like hair
        _dleaf(p, (28.5, 17), (39, 28.5), 5.4, bend=-0.8, bias=0.2)
        _dleaf(p, (29.5, 14.5), (44, 22.5 + sw), 6.2, bend=-0.9)
        _dleaf(p, (29, 11.5), (46.5, 14.5 + sw), 6.8, bend=0.6)
        # head tilted up toward the sky, a short refined muzzle
        p.blob(25, 14.5, 6.6, 6, d_skin, ang=-15, group=3)
        p.limb([(19.5, 15), (14.5, 13.5)], 5.0, 3.8, d_skin, group=3)
        # the living wreath, berries of sun-gold
        for a, b in (((18.5, 9), (15.5, 5.5)), ((21, 7.5), (19.5, 3.2)), ((24, 7), (24.5, 2.5)), ((27, 7.5), (30, 3.8)),
                     ((29.5, 9), (34, 7))):
            _dleaf(p, a, b, 3.6, bend=0.3)
        for x, y in ((18, 8), (23, 6), (28, 7)):
            _berry(p, x, y)
        # near arm flung up and forward, turning to bark, and its bough
        p.limb(bez((27, 30.5), (16, 29.5), (12, 21.5)), 4.8, 3.8, d_skin, group=22)
        p.limb(bez((12, 21.5), (9.5 - sw, 17), (8 - sw, 11)), 3.8, 2.6, d_bark, group=23)
        for a, b, w, bend in (((10 - sw, 12.5), (19.5 - sw, 6 + sw), 6.2, -0.7), ((9.5 - sw, 16), (2 - sw, 22), 6.0, 0.6),
                              ((8.5 - sw, 13), (0.5, 14.5 + sw), 7.0, 0.9), ((8 - sw, 10.5), (1 + sw, 3), 7.4, 1.2),
                              ((9 - sw, 10), (15.5 - 2 * sw, 2 + sw), 7.2, -1.2)):
            _dleaf(p, a, b, w, bend=bend)

        if p.big:
            p.stroke([(20, 12), (24, 12)], "ink")        # the lid
            p.pxs([(21, 13), (23, 13), (25, 11)], "ink")
            p.px(22, 13, "marble")
            p.px(21, 14, "gold")
            p.pxs([(16, 13), (17, 13)], "ink")           # the far eye, just showing
            p.pxs([(13, 13), (14, 13), (13, 14)], "ink") # nose
        else:
            p.px(22, 13, "ink")
        return

    if view == "back":
        _dleaf(p, (32, 18), (16, 30), 8, bend=1.2)
        p.blob(26, 66, 22, 18, d_skin, group=1)
        p.limb([(30, 52), (38, 32)], 12, 10, d_skin, group=1)
        p.blob(40, 24, 8.4, 8.2, d_skin, group=3)
        p.limb([(45, 27), (53, 29)], 8, 6.4, d_skin, group=3)
        p.limb([(26, 48), (14, 30), (10, 16)], 6, 4.4, d_bark, group=20)
        _spray(p, (10, 16), [((3, 9), 1.0), ((10, 3), 0.8), ((18, 6), -0.8)], w=6)
        for a, b, bend in (((34, 18), (31, 12), 0.5), ((38, 16), (37, 10), 0.5), ((42, 16), (45, 11), -0.5),
                           ((45, 18), (50, 15), -0.5)):
            _dleaf(p, a, b, 4, bend=bend)
        for x, y in ((36, 16), (41, 15), (46, 17)):
            _berry(p, x, y)
        p.eye(45, 21, 4, 4, shine="marble", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower: gliding on her roots, the boughs held high; phase sways
        # the roots like a hem and stirs the leaves
        sway = phase
        p.poly([(26, 44), (38, 44), (40, 54), (24, 54)], d_bark, group=30)
        for path in (([(27, 53), (20, 57 + sway)]), ([(30, 54), (28, 60)]), ([(34, 54), (36, 60)]),
                     ([(37, 53), (44, 57 + 1 - sway)])):
            p.limb(path, 3.8, 2.2, d_bark, group=31)
        if view == "up":
            p.limb([(32, 30), (32, 43)], 9, 8, d_skin, group=1)
        # the boughs are not a mirror: one flung high, the other swept wide
        p.limb([(27, 33), (19, 24)], 4.4, 3.8, d_skin, group=22)
        p.limb([(37, 33), (46, 28)], 4.4, 3.8, d_skin, group=23)
        p.limb([(19, 24), (14, 11)], 3.8, 2.8, d_bark, group=22)
        p.limb([(46, 28), (51, 18)], 3.8, 2.8, d_bark, group=23)
        for base, tip, w, bend in (((14, 12), (4, 5 + sway), 6.6, 1.0), ((14, 12), (20, 2.5), 6.0, -1.0),
                                   ((15, 15), (5, 16 - sway), 5.2, 0.5), ((51, 19), (60, 13 + 1 - sway), 5.6, -1.0),
                                   ((51, 19), (47, 10), 4.6, 1.0), ((50, 21), (59, 23 - (1 - sway)), 4.8, -0.5)):
            _dleaf(p, base, tip, w, bend=bend, bias=0.15 if base[0] > 40 else 0.0)
        if view == "down":
            _dleaf(p, (26, 18), (22, 31), 5.6, bend=0.6)
            _dleaf(p, (38, 18), (42, 31), 5.6, bend=-0.6)
            p.limb([(32, 30), (32, 43)], 9, 8, d_skin, group=1)
            p.blob(32, 33, 3, 2.6, d_skin, bias=-0.15, group=1)
        p.blob(32, 19, 7, 6.4, d_skin, group=3)
        if view == "down":
            p.limb([(32, 22), (32, 27)], 7, 4.4, d_skin, group=3)
        for a, b, bend in (((27, 14), (23, 10), 0.5), ((30, 12), (29, 8), 0.5), ((34, 12), (35, 8), -0.5),
                           ((37, 14), (41, 10), -0.5)):
            _dleaf(p, a, b, 3.6, bend=bend)
        for x, y in ((28, 13), (32, 11), (36, 13)):
            _berry(p, x, y)
        if view == "up":
            _dleaf(p, (28, 20), (25, 34), 6.0, bend=0.6)
            _dleaf(p, (36, 20), (39, 34), 6.0, bend=-0.6)
        else:
            p.eye(28, 18, 2, 3, shine="marble")
            p.eye(34, 18, 2, 3, shine="marble")
            p.px(32, 25, "ink")
        return


MONS = [
    Mon("Nebrel", NEBREL_COLORS, NEBREL_SHINY, nebrel, foot="hoof"),
    # icon palette 5 keeps both the greens and the tan coat
    Mon("Kladoe", KLADOE_COLORS, KLADOE_SHINY, kladoe, foot="hoof", icon_pal=5),
    Mon("Daphnyad", DAPHNYAD_COLORS, DAPHNYAD_SHINY, daphnyad, foot="root", icon_pal=5),
]
