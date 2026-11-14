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


MONS = [
    Mon("Nebrel", NEBREL_COLORS, NEBREL_SHINY, nebrel, foot="hoof"),
]
