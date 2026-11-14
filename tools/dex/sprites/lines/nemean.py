"""Nemean line: Nemecub, Nemeleon (Normal). The lion of Nemea, the first
Labor of Herakles, whose hide no weapon could pierce."""
import math

from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Nemecub, the golden cub
# --------------------------------------------------------------------------

NEMECUB_COLORS = [
    ("ink", INK),
    ("gold0", (152, 88, 32)), ("gold1", (200, 136, 48)), ("gold2", (232, 176, 64)), ("gold3", (248, 216, 112)),
    ("cream0", (216, 184, 128)), ("cream1", (240, 224, 176)), ("white", C.white),
    ("terra0", (120, 48, 24)), ("terra1", (184, 88, 48)), ("terra2", (224, 136, 88)),
]
NEMECUB_SHINY = {
    # marble white with a silver sheen
    "gold0": (120, 120, 136), "gold1": (168, 168, 184), "gold2": (208, 208, 216), "gold3": (240, 240, 240),
    "cream0": (192, 200, 208), "cream1": (224, 232, 232),
}

c_fur = Mat(["gold0", "gold1", "gold2", "gold3"], line="gold0", cuts=[0.24, 0.5, 0.8])
c_cream = Mat(["cream0", "cream1", "white"], line="gold1", cuts=[0.42, 0.72])
c_tuft = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.3, 0.62])


def nemecub(p, view, phase):
    if view == "icon":
        # party icon, drawn at icon size: a big head on a small sitting body
        L = phase
        p.limb(bez((22, 25), (28, 24), (26.5, 17 - L)), 2.4, 2, c_fur, group=20)
        p.lens((26.5, 18 - L), (25, 12.5 - L), 4, c_tuft, bend=0.6, group=21)
        p.blob(17, 22.5, 7, 5.6, c_fur, group=1)
        p.blob(13.5, 22.5, 3.4, 4, c_cream, group=2)
        p.blob(11.5, 27, 3.2, 1.6, c_fur, group=12)
        p.blob(18.5, 27, 3, 1.6, c_fur, bias=0.2, group=13)
        p.blob(7.5, 6.5, 3, 3, c_fur, group=5)
        p.blob(21, 6.5, 3, 3, c_fur, group=5)
        p.blob(14.5, 12.5, 8.2, 7.2, c_fur, group=3)
        p.lens((17.5, 6.5), (13, 0.5), 5.6, c_tuft, bend=1.4, group=7)
        p.lens((19, 6.5), (21, 2), 3.6, c_tuft, bend=-0.4, group=7)
        p.eye(8, 10, 2, 3, shine="white", shine_at=(1, 0))
        p.eye(15, 10, 2, 3, shine="white", shine_at=(1, 0))
        p.pxs([(10, 14), (11, 15), (12, 15), (13, 14), (10, 15), (13, 15)], "cream1")
        p.px(11, 14, "terra1")
        p.px(12, 14, "terra1")
        p.pxs([(11, 16), (12, 16)], "terra0" if L else "cream0")
        return

    if view == "side":
        # follower walking left, tail up
        st = phase
        p.limb(bez((43, 44), (51, 43), (50, 35)), 2.8, 2.2, c_fur, group=20)
        p.lens((50, 36), (53, 29.5), 4.6, c_tuft, bend=-0.6, group=21)
        far = [(28, 48), (29 + 2 * st, 58)], [(40, 48), (41 - 2 * st, 58)]
        near = [(26, 48), (25 - 2 * st + 2, 58)], [(42, 48), (43 + 2 * st - 2, 58)]
        for leg in far:
            p.limb(leg, 4.2, 4, c_fur, bias=0.3, group=10)
            p.blob(leg[1][0] - 0.8, 59, 3, 1.7, c_fur, bias=0.3, group=10)
        p.blob(34, 46, 10.5, 6.5, c_fur, group=1)
        p.blob(32, 50, 7, 2.4, c_cream, group=2)
        for leg in near:
            p.limb(leg, 4.6, 4.4, c_fur, group=12)
            p.blob(leg[1][0] - 0.8, 59.2, 3.4, 1.8, c_fur, group=12)
        p.blob(25.5, 30.5, 3.4, 3.4, c_fur, bias=0.1, group=5)
        p.blob(20, 38, 8.6, 8, c_fur, group=3)
        p.blob(13.5, 41.5, 3.8, 2.8, c_cream, group=4)
        p.blob(17.5, 31, 3.4, 3.4, c_fur, group=6)
        p.lens((22, 31), (16, 24), 5.4, c_tuft, bend=1.2, group=7)
        p.lens((24.5, 31), (26.5, 25), 4, c_tuft, bend=-0.4, group=7)
        p.eye(16, 35, 2, 4, shine="white", shine_at=(0, 0))
        p.px(10, 40, "terra1")
        return

    if view == "front":
        L = 1 if (phase == 1 and view == "front") else 0

        # far ear, behind the head
        p.blob(35.5, 29 - L, 3.8, 3.8, c_fur, bias=0.1, group=5)
        p.blob(35.8, 29.8 - L, 1.8, 2, c_tuft, bias=-0.1, group=5)
        # body: the sitting haunch, then the puffed chest
        p.blob(40.5, 53, 7.6, 7, c_fur, group=1)
        torso = p.blob(31, 50, 7.6, 8, c_fur, group=1)
        # far foreleg and paw
        p.limb([(33.5, 50.5), (34, 57)], 5.6, 5.2, c_fur, bias=0.3, group=10)
        p.blob(35, 58.6, 4.2, 2.5, c_fur, bias=0.3, group=10)
        # hind foot, flat on the ground
        p.blob(45, 59.2, 4.4, 2, c_fur, bias=0.1, group=11)
        # tail curled forward around the hind foot, terracotta tuft
        p.limb(bez((47.5, 55.5), (55.5, 61.5), (42, 60.8)), 3.2, 2.6, c_fur, group=20)
        p.lens((43.5, 60.5), (37.5, 57), 5, c_tuft, bend=-0.8, group=21)
        # chest fluff
        for a, b, w in (((27, 45), (25.5, 52.5), 5), ((29.5, 46), (29, 53.5), 4)):
            p.lens(a, b, w, c_cream, clip=[torso], group=2)
        # head: big and round, cheek fluff, a short muzzle
        p.blob(27, 37.5 - L, 10, 9, c_fur, group=3)
        for a, b, w in (((35, 40), (39, 43), 3.4), ((34, 43), (37.5, 46.5), 3.4), ((19.5, 43.5), (15.5, 46), 3)):
            p.lens((a[0], a[1] - L), (b[0], b[1] - L), w, c_fur, group=3)
        p.blob(23, 42.5 - L, 4.6, 3, c_cream, group=4)
        # near ear
        p.blob(18.5, 29.5 - L, 3.8, 3.8, c_fur, group=6)
        p.blob(18.6, 30.2 - L, 1.8, 2, c_tuft, bias=-0.1, group=6)
        # near foreleg and its oversized paw
        p.limb([(26.5, 50), (25, 56.5)], 6.4, 6, c_fur, group=12)
        p.blob(24, 58.3, 5.6, 2.9, c_fur, group=12)
        # the tuft where the mane will grow: a quiff swept forward
        for a, b, w, bend in (((32.5, 30.5 - L), (36, 25.5 - L), 3.6, -0.4),
                              ((30.5, 30 - L), (32, 22.5 - L), 5, -0.8),
                              ((27, 30 - L), (20.5, 22 - L), 6, 1.5)):
            p.lens(a, b, w, c_tuft, bend=bend, group=7)

        if p.big:
            p.eye(19, 34 - L, 4, 6, shine="white")
            p.eye(27, 34 - L, 3, 6, shine="white", shine_at=(1, 1))
            p.pxs([(22, 40 - L), (23, 40 - L), (24, 40 - L), (23, 41 - L)], "terra1")
            p.pxs([(23, 42 - L), (22, 43 - L), (21, 43 - L), (24, 43 - L), (25, 43 - L)], "gold0")
        else:
            p.pxs([(20, 36 - L), (28, 36 - L)], "ink")
        return

    if view == "back":
        # over the shoulder: the cub from behind, head turned right so the
        # face shows in profile, body cropped by the bottom of the frame
        p.limb(bez((12, 57), (2, 51), (7, 41)), 4.2, 3.4, c_fur, group=20)
        p.lens((7.5, 42), (12, 33), 6, c_tuft, bend=1.0, group=21)
        p.blob(26, 63, 20, 14, c_fur, group=1)
        p.blob(33, 49, 12, 9, c_fur, group=1)
        p.blob(30, 21.5, 5, 5, c_fur, bias=0.1, group=5)
        p.blob(40, 31, 12.6, 11.6, c_fur, group=3)
        for a, b, w in (((44, 40), (46, 46.5), 4.2), ((40, 41), (39, 47), 4.4), ((48, 38), (51.5, 43), 3.6)):
            p.lens(a, b, w, c_fur, group=3)
        p.blob(53.5, 36.5, 5.4, 3.8, c_cream, group=4)
        p.blob(48.5, 18.5, 4.4, 4.4, c_fur, group=6)
        p.blob(49.5, 19.5, 2.2, 2.4, c_tuft, bias=-0.1, group=6)
        for a, b, w, bend in (((34, 21), (30, 12.5), 5, 1.0), ((37, 20), (38, 10.5), 6, -0.4),
                              ((41, 20.5), (48, 12.5), 7, -1.6)):
            p.lens(a, b, w, c_tuft, bend=bend, group=7)
        if p.big:
            p.eye(47, 28, 4, 6, shine="white", shine_at=(2, 1))
            p.pxs([(57, 33), (58, 33), (58, 34)], "terra1")
            p.stroke([(53, 38), (56, 38)], "gold0")
        return

    if view == "down":
        # follower facing the camera; phase lifts one paw then the other
        step = phase
        p.limb(bez((38, 50), (46, 48), (45, 40)), 3, 2.4, c_fur, group=20)
        p.lens((45, 41), (46, 35), 4, c_tuft, group=21)
        p.blob(32, 50, 8, 7.5, c_fur, group=1)
        p.blob(32, 50, 4.4, 6, c_cream, group=2)
        p.limb([(28, 52), (27.5, 58 - step)], 5, 4.6, c_fur, group=12)
        p.limb([(36, 52), (36.5, 58 - (1 - step))], 5, 4.6, c_fur, group=13)
        p.blob(27.5, 59 - step, 3.8, 2.4, c_fur, group=12)
        p.blob(36.5, 59 - (1 - step), 3.8, 2.4, c_fur, group=13)
        p.blob(21.5, 30, 4.2, 4.2, c_fur, group=5)
        p.blob(42.5, 30, 4.2, 4.2, c_fur, group=6)
        p.blob(21.5, 30.5, 2.2, 2.2, c_tuft, group=5)
        p.blob(42.5, 30.5, 2.2, 2.2, c_tuft, group=6)
        p.blob(32, 38, 10.4, 9, c_fur, group=3)
        p.blob(32, 42.5, 4.6, 3.2, c_cream, group=4)
        for a, b, w, bend in (((32, 30), (30, 22), 5.4, 1.0), ((34, 30), (38, 24), 4, -0.6), ((30, 30.5), (25, 25), 3.6, 0.6)):
            p.lens(a, b, w, c_tuft, bend=bend, group=7)
        p.eye(26, 35, 3, 5, shine="white")
        p.eye(35, 35, 3, 5, shine="white")
        p.pxs([(31, 41), (32, 41)], "terra1")
        return

    if view == "up":
        # follower walking away: the cub from behind, tail swinging up
        step = phase
        p.blob(21.5, 30, 4.2, 4.2, c_fur, group=5)
        p.blob(42.5, 30, 4.2, 4.2, c_fur, group=6)
        p.limb([(28, 52), (27.5, 58 - step)], 5, 4.6, c_fur, group=12)
        p.limb([(36, 52), (36.5, 58 - (1 - step))], 5, 4.6, c_fur, group=13)
        p.blob(27.5, 59 - step, 3.8, 2.4, c_fur, group=12)
        p.blob(36.5, 59 - (1 - step), 3.8, 2.4, c_fur, group=13)
        p.blob(32, 50, 8.5, 7.5, c_fur, group=1)
        p.blob(32, 37, 10.4, 9, c_fur, group=3)
        p.limb(bez((32, 54), (44 - 4 * step, 55), (45 - 6 * step, 44)), 3, 2.4, c_fur, group=20)
        p.lens((45 - 6 * step, 45), (46 - 7 * step, 38), 4.6, c_tuft, bend=-0.6, group=21)
        for a, b, w, bend in (((32, 30), (30, 22), 5.4, 1.0), ((34, 30), (38, 24), 4, -0.6), ((30, 30.5), (25, 25), 3.6, 0.6)):
            p.lens(a, b, w, c_tuft, bend=bend, group=7)
        return


# --------------------------------------------------------------------------
# Nemeleon, the lion whose hide turned every weapon
# --------------------------------------------------------------------------

NEMELEON_COLORS = [
    ("ink", INK),
    ("terra0", (112, 40, 24)), ("terra1", (176, 80, 40)), ("mane1", (224, 144, 48)), ("mane2", (248, 200, 80)),
    ("hide0", (136, 96, 48)), ("hide1", (192, 144, 72)), ("hide2", (232, 192, 112)), ("hide3", (248, 224, 160)),
    ("plate0", (112, 72, 24)), ("plate1", (168, 120, 32)), ("plate2", (216, 168, 56)), ("plate3", (248, 224, 120)),
    ("white", C.white), ("shade", (88, 56, 32)),
]
NEMELEON_SHINY = {
    # marble hide, silver plates, an ink-dark mane
    "terra0": (24, 24, 40), "terra1": (48, 48, 72), "mane1": (80, 80, 112), "mane2": (128, 128, 160),
    "hide0": (144, 136, 136), "hide1": (192, 184, 176), "hide2": (224, 216, 208), "hide3": (240, 240, 232),
    "plate0": (88, 96, 112), "plate1": (136, 144, 160), "plate2": (184, 192, 200), "plate3": (224, 232, 240),
    "shade": (88, 88, 96),
}

l_hide = Mat(["shade", "hide0", "hide1", "hide2", "hide3"], line="shade", cuts=[0.14, 0.34, 0.56, 0.86])
l_mane = Mat(["terra0", "terra1", "mane1", "mane2"], line="terra0", cuts=[0.34, 0.56, 0.8])
l_plate = Mat(["plate0", "plate1", "plate2", "plate3"], line="plate0", cuts=[0.24, 0.5, 0.74])
l_claw = Mat(["hide3", "white"], line="hide1", cuts=[0.5])


def _lock(p, c, ang, r0, r1, w, bend=0.0, **kw):
    """A mane lock radiating from c at angle ang (degrees, 0 = right,
    90 = down), from radius r0 to r1."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    a = (c[0] + ca * r0, c[1] + sa * r0)
    b = (c[0] + ca * r1, c[1] + sa * r1)
    return p.lens(a, b, w, l_mane, bend=bend, **kw)


def _claws(p, pts, w=2.0):
    """Long hooked claws: each a tapered stroke from its root along pts."""
    for path in pts:
        p.taper(path, w, l_claw, group=14)


def nemeleon(p, view, phase):
    if view == "icon":
        # party icon at icon size: the maned head over a stalking body
        L = phase
        p.limb(bez((25, 15), (30, 13), (28.5, 6)), 2, 1.6, l_hide, group=20)
        p.lens((28.5, 7), (27, 1.5 - L), 4, l_mane, bend=0.6, group=21)
        p.limb([(13, 20), (12, 26.5)], 4, 3.6, l_hide, bias=0.3, group=10)
        p.limb([(22, 20), (23, 26.5)], 4, 3.6, l_hide, bias=0.3, group=11)
        p.blob(19, 17, 8.5, 5.6, l_plate, group=1)
        p.limb([(25, 18), (26.5, 26.5)], 4.4, 3.8, l_hide, group=13)
        for ang, r1, w in ((-140, 10, 6), (-100, 11, 6.5), (-60, 11, 6.5), (-20, 10, 6.5), (20, 10, 6.5),
                           (60, 10, 6), (100, 10, 6), (140, 9, 5.5)):
            _lock(p, (10, 12), ang, 2, r1, w, bend=0.8)
        p.limb([(8, 20), (6, 26.5)], 4.6, 4, l_hide, group=12)
        p.blob(8, 12.5, 4.8, 4.6, l_hide, group=3)
        p.blob(4.5, 15, 3.2, 2.6, l_hide, bias=-0.1, group=4)
        p.pxs([(5, 11), (9, 11)], "ink")
        p.px(2, 14, "terra0")
        if L:
            p.pxs([(3, 16), (4, 16)], "ink")
        return

    if view == "down":
        # follower facing the camera: the mane a blazing ring round the face
        step = phase
        p.limb([(25, 46), (25, 58 - 2 * step)], 6.4, 5.6, l_hide, group=12)
        p.limb([(39, 46), (39, 58 - 2 * (1 - step))], 6.4, 5.6, l_hide, group=13)
        p.blob(25, 59 - 2 * step, 4.4, 2.4, l_hide, group=12)
        p.blob(39, 59 - 2 * (1 - step), 4.4, 2.4, l_hide, group=13)
        p.blob(32, 44, 11, 9, l_plate, group=1)
        for ang in range(-180, 180, 30):
            _lock(p, (32, 30), ang + 15, 6, 19 if ang % 60 == 0 else 16, 9, bend=1.6, bias=0.15, group=30)
        for ang in range(-180, 180, 36):
            _lock(p, (32, 30), ang, 3, 13, 8, bend=1.2, group=31)
        p.blob(32, 30, 7.5, 7.5, l_hide, group=3)
        p.blob(32, 35, 4.6, 3.6, l_hide, bias=-0.1, group=4)
        p.eye(27, 28, 2, 3, iris="mane1", shine=None)
        p.eye(35, 28, 2, 3, iris="mane1", shine=None)
        p.pxs([(31, 33), (32, 33)], "terra0")
        return

    if view == "up":
        # follower walking away: mane, armored back, tail lashing
        step = phase
        p.limb([(26, 48), (26, 58 - 2 * step)], 6.4, 5.6, l_hide, group=12)
        p.limb([(38, 48), (38, 58 - 2 * (1 - step))], 6.4, 5.6, l_hide, group=13)
        p.blob(26, 59 - 2 * step, 4.4, 2.4, l_hide, group=12)
        p.blob(38, 59 - 2 * (1 - step), 4.4, 2.4, l_hide, group=13)
        p.blob(32, 45, 11, 10, l_plate, group=1)
        p.limb(bez((33, 52), (44 - 6 * step, 50), (42 - 8 * step, 38)), 3, 2.4, l_hide, group=20)
        p.lens((42 - 8 * step, 39), (43 - 9 * step, 31), 5, l_mane, group=21)
        for ang in range(-180, 180, 30):
            _lock(p, (32, 28), ang + 15, 4, 19 if ang % 60 == 0 else 16, 9.5, bend=1.6, bias=0.1, group=30)
        p.blob(32, 28, 9, 9, l_mane, group=31)
        return

    if view in ("front", "side"):
        L = 1 if (phase == 1 and view == "front") else 0
        c = (21, 25)

        # tail lashing up in an S, its tuft blazing
        p.limb(bez3((55, 32), (63.5, 31), (62, 21), (56.5, 14)), 3.8, 2.8, l_hide, group=20)
        for a, b, w, bend in (((56.5, 16), (51.5, 5 - L), 6, 1.4), ((57, 15.5), (59.5, 4.5 + L), 5, -0.6),
                              ((56, 17), (49.5, 11.5 + L), 4.6, 1.0)):
            p.lens(a, b, w, l_mane, bend=bend, group=21)
        # far legs, in shadow
        p.limb([(29, 44), (27.5, 51), (28, 57.5)], 9.4, 7.6, l_hide, bias=0.3, group=10)
        p.blob(27, 58.4, 5.8, 2.8, l_hide, bias=0.3, group=10)
        p.limb([(45, 43), (47.5, 50.5), (45.5, 57.5)], 8.6, 6.6, l_hide, bias=0.32, group=11)
        p.blob(45, 58.4, 5.2, 2.6, l_hide, bias=0.32, group=11)
        # the mane's back layer: great locks blazing up and back, darker
        for ang, r1, w, bend in ((-132, 19, 7.5, 2.0), (-110, 24, 8, 3.0), (-88, 21, 8, 2.6), (-66, 25, 9, 3.6),
                                 (-44, 22, 9, 3.2), (-22, 25, 9.5, 3.6), (0, 21.5, 9, 2.8), (22, 23.5, 9, 2.6),
                                 (46, 21, 9, 1.8), (70, 22.5, 9, 1.0), (94, 22, 8.5, 0.2), (118, 19.5, 8, -0.8)):
            _lock(p, c, ang, 8, r1, w, bend=bend + (0.3 if L else 0), bias=0.2, group=30)
        # body: massive shoulders high, the plated barrel sloping to the haunch
        b1 = p.blob(42, 36, 14.4, 10.6, l_hide, ang=8, group=1)
        b2 = p.blob(52.5, 38.5, 8.4, 10, l_hide, group=1)
        b3 = p.blob(31, 36.5, 10.6, 11.6, l_hide, group=1)
        p.blob(41, 45, 10, 2.4, l_hide, bias=0.35, clip=[b1, b2, b3], group=2)
        # near hind leg
        p.limb([(52, 40), (57.5, 49), (55, 57.5)], 11.4, 7.6, l_hide, group=13)
        p.blob(54.5, 58.4, 6, 2.8, l_hide, group=13)
        # the mane's middle layer, gold
        for ang, r1, w, bend in ((-122, 16, 7.5, 1.8), (-98, 19, 8, 2.4), (-74, 17.5, 8.5, 2.4), (-50, 19.5, 9, 3.0),
                                 (-26, 17.5, 9, 2.4), (-2, 19, 9, 2.4), (22, 17, 9, 1.8), (46, 18.5, 8.5, 1.2),
                                 (70, 17.5, 8, 0.6), (94, 18.5, 7.5, 0.0), (116, 16, 7, -0.6)):
            _lock(p, c, ang, 4, r1, w, bend=bend - (0.3 if L else 0), bias=-0.08, group=31)
        # near foreleg thrust forward, the paw planted, claws out
        p.limb([(23, 41), (15.5, 49.5), (10.5, 56.5)], 12.6, 8.4, l_hide, group=12)
        p.blob(8.5, 58.2, 6.8, 3.2, l_hide, group=12)
        _claws(p, [[(4.5, 58.5), (2.5, 60.5)], [(7, 59), (5, 61.2)], [(9.6, 59.4), (8, 61.5)], [(12, 59.6), (11, 61.6)]])
        # the front locks falling over the chest
        for a, b, w, bend in (((19, 36), (15, 48), 7.5, 0.8), ((24, 37), (23, 49.5), 7.5, 0.0),
                              ((28.5, 36), (31, 47), 7, -0.8), ((15, 35), (9, 44), 6.5, 1.0)):
            p.lens(a, b, w, l_mane, group=32)
        # head thrust forward, jaw open in a roar
        p.blob(15, 24, 8.4, 8, l_hide, group=3)
        p.blob(8.5, 28.5, 5.8, 4.6, l_hide, bias=-0.1, group=4)
        p.blob(10, 33.5, 4.6, 2.6, l_hide, bias=0.1, group=4)
        # forelock over the brow
        p.lens((23, 17), (12, 12.5), 6.4, l_mane, bend=1.6, group=5)
        p.lens((26, 17), (20, 9), 6, l_mane, bend=1.4, group=5)

        if p.big:
            p.eye(9, 21, 4, 3, iris="mane1", shine="white", shine_at=(0, 1))
            p.eye(16, 21, 3, 3, iris="mane1", shine="white", shine_at=(0, 1))
            p.pxs([(2, 27), (3, 27), (4, 27), (3, 28)], "terra0")
            p.patch(4, 30, ["1111111", "1e.2.e1", ".1222.1", "..111.."], {"1": "ink", "2": "terra0", "e": "white"})
        else:
            p.pxs([(10, 22), (17, 22)], "ink")
        return

    if view == "back":
        # over the shoulder: the plated back like a cuirass, the great mane
        # blazing around a head turned right in profile; cropped below
        c = (37, 28)
        p.limb(bez3((12, 54), (1, 50), (9, 38), (6, 29)), 4.4, 3.4, l_hide, group=20)
        for a, b, w, bend in (((6, 31), (1.5, 18), 6.6, 1.2), ((6.5, 30.5), (10.5, 18), 5.6, -1.0),
                              ((6, 32), (12.5, 24), 4.6, -1.2)):
            p.lens(a, b, w, l_mane, bend=bend, group=21)
        p.blob(25.5, 66, 24, 19, l_hide, group=1)
        p.blob(31, 51, 15, 12, l_hide, group=1)
        # the head, mostly hidden by the mane, its face showing at the right
        p.blob(51, 29, 8, 8, l_hide, group=3)
        p.blob(57.5, 33, 4.8, 4.2, l_hide, bias=-0.1, group=4)
        p.blob(55.5, 38, 4, 2.3, l_hide, bias=0.1, group=4)
        for ang, r1, w, bend in ((-176, 23, 9.5, -2.4), (-152, 26, 10, -3.2), (-128, 27, 10.5, -3.4),
                                 (-104, 27, 10.5, -3.4), (-80, 26, 10.5, -3.0), (-56, 25, 10, -2.6), (-34, 22, 9.5, -2.0),
                                 (152, 27, 10.5, 2.6), (128, 26, 10.5, 2.0), (104, 23, 10, 1.2), (176, 24, 9.5, 2.6),
                                 (80, 19, 9, 0.6)):
            _lock(p, c, ang, 8, r1, w, bend=bend, bias=0.2, group=30)
        for ang, r1, w, bend in ((-164, 18, 9, -2.0), (-140, 21, 9.5, -2.6), (-116, 22, 9.5, -2.8), (-92, 22, 9.5, -2.6),
                                 (-68, 20.5, 9, -2.2), (-44, 18, 8.5, -1.6), (164, 18, 9, 2.0), (140, 19, 9, 1.8),
                                 (116, 18, 8.5, 1.2), (-22, 16, 8, -1.2), (90, 15, 8, 0.6)):
            _lock(p, c, ang, 4, r1, w, bend=bend, bias=-0.06, group=31)
        for ang, r1, w, bend in ((-150, 13, 8, -1.4), (-120, 14.5, 8, -1.6), (-90, 14, 8, -1.4), (170, 13, 8, 1.2),
                                 (140, 13, 7.5, 1.0), (-60, 13, 7.5, -1.2)):
            _lock(p, c, ang, 2, r1, w, bend=bend, bias=-0.14, group=32)
        # the cheek ruff in front of the jaw's hinge
        for a, b, w, bend in (((47, 31), (49, 41), 6, -0.8), ((46, 26), (50, 18.5), 6, 1.0)):
            p.lens(a, b, w, l_mane, bend=bend, group=33)
        if p.big:
            p.eye(55, 26, 4, 3, iris="mane1", shine="white", shine_at=(3, 1))
        return


MONS = [
    Mon("Nemecub", NEMECUB_COLORS, NEMECUB_SHINY, nemecub, foot="paw", icon_pal=3),
    Mon("Nemeleon", NEMELEON_COLORS, NEMELEON_SHINY, nemeleon, foot="bigpaw", icon_pal=3),
]
