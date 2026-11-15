"""Stoneborn line: Pebblith, Cairnolith, Laolith (Rock). The stones that
Deucalion and Pyrrha threw over their shoulders, which became people."""
from mon_lib import C, Mat, Mon

INK = C.ink

# --------------------------------------------------------------------------
# Pebblith, the thrown pebble
# --------------------------------------------------------------------------

PEBBLITH_COLORS = [
    ("ink", INK),
    # river-smoothed marble, dark to light, and its limestone sheen
    ("stone0", (88, 80, 88)), ("stone1", (128, 120, 120)), ("stone2", (168, 160, 152)), ("stone3", (208, 200, 184)),
    ("sheen", (240, 232, 208)),
    # the chalk handprint and its pressed-in edge
    ("chalk", (248, 248, 240)), ("chalk0", (200, 192, 176)),
    # terracotta earth clinging to its base
    ("earth0", (112, 48, 32)), ("earth1", (168, 88, 48)), ("earth2", (216, 136, 88)),
]
PEBBLITH_SHINY = {
    # the stone turns terracotta red, the handprint sun-gold
    "stone0": (112, 40, 32), "stone1": (160, 72, 48), "stone2": (200, 104, 72), "stone3": (232, 152, 112),
    "sheen": (248, 208, 168),
    "chalk": (248, 216, 112), "chalk0": (200, 144, 40),
    "earth0": (72, 56, 48), "earth1": (112, 88, 64), "earth2": (152, 128, 96),
}

p_stone = Mat(["stone0", "stone1", "stone2", "stone3"], line="stone0", cuts=[0.2, 0.44, 0.7])
p_earth = Mat(["earth0", "earth1", "earth2"], line="earth0", cuts=[0.36, 0.66])
p_chalk = Mat(["chalk0", "chalk"], line="chalk0", cuts=[0.5])


def pebblith(p, view, phase):
    if view in ("front", "side", "icon"):
        L = phase if view == "front" else 0
        roll = phase if view == "side" else 0
        # far nub, flung up for balance
        p.blob(42.5 + roll, 41 - L, 3, 2.6, p_stone, ang=-30, bias=0.3, group=10)
        # the pebble, tilted forward as if still tumbling
        body = p.blob(31, 47, 12, 10, p_stone, ang=-24 - 8 * roll, group=1)
        # the handprint wrapping round its back
        p.poly([(41, 44), (43.5, 45), (43, 51), (40, 52)], p_chalk, clip=[body], group=3)
        # earth crust at the base
        p.blob(32, 56.5, 8.5, 3, p_earth, group=4)
        p.blob(25, 55.5, 3.6, 2.2, p_earth, group=4)
        p.blob(39, 55, 3, 2.2, p_earth, group=4)
        # near nub, braced forward
        p.blob(19.5, 51 + L, 3.2, 2.8, p_stone, ang=20, group=11)
        if p.big:
            p.eye(22, 42, 3, 4, shine="chalk", shine_at=(1, 1))
            p.eye(28, 42, 3, 4, shine="chalk", shine_at=(1, 1))
            p.stroke([(21, 40), (24, 41)], "ink")
            p.stroke([(28, 41), (31, 40)], "ink")
            p.stroke([(24, 49), (28, 49)], "stone0")
            p.pxs([(26, 38), (27, 38), (28, 38), (25, 39)], "sheen")
        else:
            p.pxs([(23, 44), (29, 44)], "ink")
        return

    if view == "back":
        # over the shoulder: the pale handprint on its back, the face turned
        # right in profile, the earth crust cropped by the frame
        body = p.blob(30, 50, 19, 16, p_stone, ang=-16, group=1)
        p.blob(51, 41, 3.6, 3, p_stone, group=11)
        p.blob(30, 64, 16, 4, p_earth, group=4)
        # the hand: palm and five fingers, thumb to the left
        p.blob(28, 49, 5.6, 5, p_chalk, clip=[body], group=3)
        for a, b in (((23, 45), (17, 41)), ((25, 44), (22, 36)), ((28.5, 44), (28, 35)), ((32, 44.5), (34, 36.5)),
                     ((33, 47.5), (38.5, 42))):
            p.limb([a, b], 3, 2.4, p_chalk, clip=[body], group=3)
        p.eye(44, 40, 3, 4, shine="chalk", shine_at=(1, 1))
        if p.big:
            p.stroke([(42, 38), (46, 39)], "ink")
            p.stroke([(46, 47), (48, 47)], "stone0")
        return

    if view in ("down", "up"):
        # follower: rolling end over end; phase turns it a quarter
        L = phase
        p.blob(32, 48, 8.5, 9.5 - L, p_stone, ang=10 * L, group=1)
        p.blob(32, 57, 6, 2, p_earth, group=4)
        p.blob(22.5, 50, 2.4, 2.2, p_stone, group=11)
        p.blob(41.5, 50, 2.4, 2.2, p_stone, group=12)
        if view == "down":
            p.eye(28, 44, 2, 3, shine="chalk")
            p.eye(34, 44, 2, 3, shine="chalk")
            p.stroke([(27, 43), (29, 43)], "ink")
            p.stroke([(34, 43), (36, 43)], "ink")
            p.stroke([(31, 50), (33, 50)], "stone0")
        else:
            p.blob(32, 47, 3.4, 3.4, p_chalk, group=3)
            p.limb([(30, 45), (29, 41)], 1.6, 1.4, p_chalk, group=3)
            p.limb([(33, 45), (34, 41)], 1.6, 1.4, p_chalk, group=3)
        return


# --------------------------------------------------------------------------
# Cairnolith, the roadside cairn standing up to walk
# --------------------------------------------------------------------------

CAIRNOLITH_COLORS = [
    ("ink", INK),
    # marble-gray stones
    ("gray0", (80, 72, 80)), ("gray1", (120, 112, 112)), ("gray2", (168, 160, 152)), ("gray3", (208, 200, 184)),
    # limestone stones
    ("lime0", (144, 112, 72)), ("lime1", (184, 152, 104)), ("lime2", (224, 200, 152)),
    # the terracotta stone
    ("terra0", (120, 48, 24)), ("terra1", (176, 80, 48)), ("terra2", (216, 128, 80)),
    # olive lichen
    ("lichen0", (88, 104, 40)), ("lichen1", (144, 160, 72)),
    ("white", (240, 240, 224)),
]
CAIRNOLITH_SHINY = {
    # every stone terracotta red, the lichen sun-gold
    "gray0": (104, 32, 24), "gray1": (152, 64, 40), "gray2": (200, 104, 64), "gray3": (232, 152, 104),
    "lime0": (128, 48, 32), "lime1": (176, 88, 56), "lime2": (224, 144, 96),
    "terra0": (88, 24, 24), "terra1": (136, 40, 32), "terra2": (184, 72, 48),
    "lichen0": (200, 144, 40), "lichen1": (240, 192, 64),
}

c_gray = Mat(["gray0", "gray1", "gray2", "gray3"], line="gray0", cuts=[0.2, 0.44, 0.7])
c_lime = Mat(["lime0", "lime1", "lime2"], line="lime0", cuts=[0.34, 0.64])
c_terra = Mat(["terra0", "terra1", "terra2"], line="terra0", cuts=[0.34, 0.64])


def cairnolith(p, view, phase):
    if view in ("front", "side", "icon"):
        L = phase if view == "front" else 0
        sway = phase if view == "side" else 0
        # legs: two stumpy stone pillars
        p.limb([(37, 52), (38, 59)], 7, 7.4, c_gray, bias=0.3, group=20)
        p.blob(38.5, 59.5, 5, 2.2, c_gray, bias=0.3, group=20)
        # far arm, raised from the shoulder stone, fist up
        p.limb([(43, 30), (51, 24 - L)], 5, 5, c_lime, bias=0.3, group=21)
        p.blob(54, 22.5 - L, 3.8, 3.8, c_gray, bias=0.25, group=21)
        # the five stones, each set a little further forward: it leans into the walk
        p.blob(32, 46.5, 17, 6.5, c_gray, group=1)
        p.blob(31, 38.5, 14.5, 4.8, c_terra, group=2)
        p.blob(31.5 + sway, 31, 13.5, 4.4, c_lime, ang=-4, group=3)
        p.blob(29 + sway, 21.5, 10.5, 6, c_gray, group=4)
        p.blob(29.5 + sway, 13, 7.5, 3.2, c_lime, ang=6, group=5)
        p.blob(28.5 + L + 2 * sway, 7.5 - L, 3.6, 2.6, c_gray, group=6)
        # near leg
        p.limb([(25, 52), (24, 59)], 7.4, 7.8, c_gray, group=22)
        p.blob(23.5, 59.5, 5.4, 2.2, c_gray, group=22)
        # near arm, reaching forward and down
        p.limb([(19, 33), (13, 36 - L)], 5.4, 5.4, c_lime, group=23)
        p.blob(9, 38.5 - L, 4.2, 4.2, c_gray, group=23)
        if p.big:
            p.eye(20, 19, 2, 4, shine="white", shine_at=(1, 1))
            p.eye(25, 19, 3, 4, shine="white", shine_at=(1, 1))
            p.stroke([(20, 18), (28, 18)], "gray1")
            p.stroke([(21, 25), (24, 25)], "gray0")
            for x, y in ((38, 44), (41, 45), (18, 45), (37, 29), (35, 12)):
                p.pxs([(x, y), (x + 1, y)], "lichen1")
                p.px(x, y + 1, "lichen0")
        else:
            p.pxs([(21, 21), (26, 21)], "ink")
        return

    if view == "back":
        p.blob(30, 62, 26, 9, c_gray, group=1)
        p.blob(31, 49, 21, 6.5, c_terra, group=2)
        p.blob(33, 39, 18, 6, c_lime, group=3)
        p.limb([(14, 40), (6, 37)], 7, 7, c_lime, group=21)
        p.blob(5, 36, 4.4, 4.4, c_gray, group=21)
        p.blob(37, 25, 13, 8, c_gray, group=4)
        p.blob(37, 14, 8.6, 4.2, c_lime, group=5)
        p.blob(37, 7, 4.4, 3.2, c_gray, group=6)
        p.eye(45, 22, 3, 4, shine="white", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        step = phase
        p.limb([(27, 52), (27, 60 - 2 * step)], 7, 7.4, c_gray, group=20)
        p.limb([(37, 52), (37, 60 - 2 * (1 - step))], 7, 7.4, c_gray, group=21)
        p.blob(32, 47, 15, 6, c_gray, group=1)
        p.blob(32, 39.5, 13, 4.4, c_terra, group=2)
        p.blob(32, 32, 11.5, 4, c_lime, group=3)
        p.limb([(21, 34), (15, 37)], 5, 5, c_lime, group=23)
        p.limb([(43, 34), (49, 37)], 5, 5, c_lime, group=24)
        p.blob(32, 23 + step, 10, 5.6, c_gray, group=4)
        p.blob(32, 15 + step, 6.5, 3, c_lime, group=5)
        p.blob(32 + step, 9.5 + step, 3.4, 2.4, c_gray, group=6)
        if view == "down":
            p.eye(27, 20 + step, 3, 4, shine="white")
            p.eye(34, 20 + step, 3, 4, shine="white")
            p.stroke([(30, 26 + step), (34, 26 + step)], "gray0")
        return


# --------------------------------------------------------------------------
# Laolith, the stoneborn: a person of fitted blocks, glancing back
# --------------------------------------------------------------------------

LAOLITH_COLORS = [
    ("ink", INK),
    # marble and limestone stone, dark to light
    ("stone0", (72, 64, 72)), ("stone1", (112, 104, 104)), ("stone2", (152, 144, 128)), ("stone3", (192, 184, 160)),
    ("stone4", (224, 216, 192)), ("stone5", (248, 240, 216)),
    # terracotta cord
    ("cord0", (112, 40, 24)), ("cord1", (168, 80, 40)), ("cord2", (216, 128, 80)),
    # the chalk handprint
    ("chalk", (248, 248, 240)), ("chalk0", (208, 200, 184)),
    # a sun-gold spark of life in its eyes
    ("gold", (240, 192, 64)),
]
LAOLITH_SHINY = {
    # its stone turns terracotta red, the handprint sun-gold
    "stone0": (96, 32, 24), "stone1": (144, 56, 40), "stone2": (184, 88, 56), "stone3": (216, 128, 88),
    "stone4": (240, 168, 120), "stone5": (248, 208, 168),
    "cord0": (64, 48, 40), "cord1": (104, 80, 56), "cord2": (144, 120, 88),
    "chalk": (248, 216, 112), "chalk0": (200, 144, 40),
}

l_stone = Mat(["stone0", "stone1", "stone2", "stone3", "stone4"], line="stone0", cuts=[0.1, 0.26, 0.46, 0.68])
l_cord = Mat(["cord0", "cord1", "cord2"], line="cord0", cuts=[0.36, 0.66])
l_chalk = Mat(["chalk0", "chalk"], line="chalk0", cuts=[0.5])


def _fist(p, cx, cy, r, **kw):
    """A heavy boulder fist bound in terracotta cord."""
    g = kw.pop("group", None)
    p.circle(cx, cy, r, l_stone, group=g, **kw)
    p.limb([(cx - r * 0.9, cy - r * 0.35), (cx, cy - r * 0.15), (cx + r * 0.9, cy - r * 0.35)], 1.8, 1.8, l_cord,
           clip=None, group=(g or 0) + 100)
    if p.big:
        p.limb([(cx - r * 0.8, cy + r * 0.35), (cx, cy + r * 0.55), (cx + r * 0.8, cy + r * 0.35)], 1.6, 1.6, l_cord,
               group=(g or 0) + 101)


def laolith(p, view, phase):
    # The battle sprites are hand-finished (art/laolith_*); this draft gives the
    # icon and the follower the same colossus in rounded, chiselled masses.
    if view in ("front", "side", "icon"):
        L = phase if view == "front" else 0
        stride = view == "side" and phase == 1
        # far arm, swung forward, boulder fist
        p.limb([(14, 18), (10, 29), (9, 37)], 9, 7.4, l_stone, bias=0.3, group=20)
        _fist(p, 9.5, 44 + L, 8, bias=0.2, group=21)
        # trailing leg, its heel lifted
        fl = [(40, 43), (46, 50), (50, 56)] if not stride else [(40, 43), (41, 51), (40, 57)]
        p.limb(fl, 9.4, 7.4, l_stone, bias=0.35, group=10)
        p.blob(52, 58.5, 6, 2.8, l_stone, ang=20 if not stride else 0, bias=0.35, group=11)
        # pelvis, abdomen, chest
        p.blob(33, 42, 11, 5.6, l_stone, bias=0.2, group=1)
        p.blob(33, 33, 11.4, 6, l_stone, bias=0.1, group=2)
        p.blob(26, 21, 8.6, 8, l_stone, group=3)
        p.blob(40, 21, 8.4, 8, l_stone, bias=0.15, group=3)
        # far shoulder
        p.blob(19, 16.5, 9, 6.6, l_stone, group=5)
        # head, looking back to the right
        p.blob(40, 9, 7.6, 8, l_stone, group=6)
        # lead leg, forward and planted
        nl = [(28, 44), (21, 51), (19, 57)] if not stride else [(28, 44), (26, 51), (27, 57)]
        p.limb(nl, 10.4, 8.4, l_stone, group=12)
        p.blob(17, 58.5 if not stride else 58.5, 8.6, 3, l_stone, group=13)
        # near shoulder, arm and fist, swung back
        p.blob(50, 18, 8.6, 7.4, l_stone, bias=0.1, group=22)
        p.limb([(53, 24), (55, 32), (55, 38)], 8, 7, l_stone, bias=0.3, group=23)
        _fist(p, 54.5, 46 - L, 8, bias=0.15, group=24)
        if p.big:
            p.eye(39, 7 - L, 2, 3, shine="chalk", shine_at=(1, 0))
            p.eye(43, 7 - L, 2, 3, shine="chalk", shine_at=(1, 0))
            p.pxs([(39, 10 - L), (43, 10 - L)], "gold")
            p.stroke([(38, 6 - L), (45, 6 - L)], "stone0")
            for a, b in (((18, 33), (47, 32)), ((33, 14), (33, 27)), ((22, 42), (44, 41))):
                p.stroke([a, b], "stone0")
        else:
            p.pxs([(40, 9), (43, 9)], "ink")
        return

    if view == "back":
        # (the hand-finished art replaces this) the broad back with the pale
        # handprint between the shoulder blades, the head in right profile
        p.blob(8, 47, 7.4, 7.2, l_stone, group=21)
        back = p.blob(31, 48, 26, 25, l_stone, group=1)
        p.blob(56, 44, 6.6, 6.8, l_stone, group=24)
        p.blob(43, 11, 9, 9, l_stone, group=4)
        p.blob(31, 32, 6.4, 6, l_chalk, clip=[back], group=3)
        p.eye(46, 7, 3, 4, shine="chalk", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        step = phase
        p.limb([(26, 44), (25, 60 - 2 * step)], 9, 8, l_stone, group=12)
        p.limb([(38, 44), (39, 60 - 2 * (1 - step))], 9, 8, l_stone, group=13)
        p.blob(32, 42, 10, 5.6, l_stone, group=1)
        p.blob(32, 32, 11, 7, l_stone, group=2)
        p.blob(25, 22, 8, 7.4, l_stone, group=3)
        p.blob(39, 22, 8, 7.4, l_stone, group=3)
        p.blob(15, 19, 7, 6, l_stone, group=20)
        p.blob(49, 19, 7, 6, l_stone, group=23)
        p.limb([(14, 22), (11, 33)], 7.4, 6.6, l_stone, group=20)
        p.limb([(50, 22), (53, 33)], 7.4, 6.6, l_stone, group=23)
        _fist(p, 10.5, 41 - step, 6.4, group=21)
        _fist(p, 53.5, 41 - (1 - step), 6.4, group=24)
        p.blob(32, 10, 7, 7.4, l_stone, group=4)
        if view == "down":
            p.eye(28, 8, 2, 3, shine="chalk")
            p.eye(34, 8, 2, 3, shine="chalk")
            p.stroke([(27, 7), (37, 7)], "stone0")
            p.stroke([(30, 14), (34, 14)], "stone0")
        else:
            p.blob(32, 25, 5, 4.6, l_chalk, group=3)
            for a, b in (((28, 23), (25, 17)), ((31, 22), (30, 16)), ((34, 22), (35, 16)), ((36, 24), (39, 19))):
                p.limb([a, b], 2.4, 2, l_chalk, group=3)
        return


STONE_FOOT = [
    "................",
    "................",
    "................",
    ".....######.....",
    "....########....",
    "...##########...",
    "...##########...",
    "...##########...",
    "...##########...",
    "....########....",
    ".....######.....",
    "................",
    "................",
    "................",
    "................",
    "................",
]

MONS = [
    Mon("Pebblith", PEBBLITH_COLORS, PEBBLITH_SHINY, pebblith, foot="blank", follow=17),
    Mon("Cairnolith", CAIRNOLITH_COLORS, CAIRNOLITH_SHINY, cairnolith, foot=STONE_FOOT),
    Mon("Laolith", LAOLITH_COLORS, LAOLITH_SHINY, laolith, foot=STONE_FOOT),
]
