"""Endymion line: Amnoze (Normal/Psychic). The shepherd loved by Selene,
granted eternal sleep on Mount Latmos, as one of his own lambs: curled up,
never waking, a shepherd's crook for a horn and the moon on its flank."""
from mon_lib import C, Mat, Mon, bez

INK = C.ink

AMNOZE_COLORS = [
    ("ink", INK),
    # marble-white fleece with pale Aegean-blue shading
    ("wool0", (96, 120, 184)), ("wool1", (152, 176, 224)), ("wool2", (208, 216, 240)), ("wool3", C.white),
    # a soft, warm face and legs
    ("face0", (168, 120, 120)), ("face1", (224, 176, 160)), ("face2", (248, 216, 200)),
    # limestone crook horn
    ("horn0", (144, 112, 72)), ("horn1", (208, 184, 136)), ("horn2", (240, 224, 184)),
    # Psychic-pink dream bubbles
    ("pink0", (200, 88, 160)), ("pink1", (240, 152, 208)), ("pink2", (248, 216, 240)),
    # the crescent moon curled into the fleece
    ("moon", (240, 216, 136)),
]
AMNOZE_SHINY = {
    # pale sun-gold fleece, like the moon low on the horizon
    "wool0": (192, 136, 64), "wool1": (232, 184, 104), "wool2": (248, 224, 160), "wool3": (248, 248, 216),
    "moon": (232, 240, 248),
}

a_wool = Mat(["wool0", "wool1", "wool2", "wool3"], line="wool0", cuts=[0.2, 0.45, 0.7])
a_face = Mat(["face0", "face1", "face2"], line="face0", cuts=[0.35, 0.68])
a_horn = Mat(["horn0", "horn1", "horn2"], line="horn0", cuts=[0.35, 0.7])
a_bub = Mat(["pink0", "pink1", "pink2"], line="pink0", cuts=[0.4, 0.75])


# the fleece: a cloud of puffs (cx, cy, r, layer)
AMNOZE_CLOUD = [(30, 40.5, 5.6, 0), (37, 38.5, 6.0, 0), (43.5, 41, 5.4, 0), (27, 45, 5.0, 1), (48, 46.5, 5.0, 1),
                (34, 45, 6.6, 1), (42, 47.5, 6.2, 1), (47, 52, 4.6, 2), (25.5, 51, 5.2, 2), (32, 52, 6.0, 2),
                (40, 53, 5.4, 2)]


def _bubble(p, x, y, r):
    p.circle(x, y, r, a_bub, group=40 + int(x))
    if p.big:
        p.px(x - r * 0.45, y - r * 0.45, "pink2")


def _crook(p, y):
    """The horn that curves into a shepherd's crook."""
    p.limb(bez((21.5, y(41)), (22, y(33)), (20.5, y(29))), 4.6, 3.8, a_horn, group=9)
    p.limb(bez((20.5, y(29)), (18.5, y(25)), (15, y(27.5))), 3.8, 3.4, a_horn, group=9)
    p.limb([(15, y(27.5)), (14.5, y(31.5))], 3.4, 3.0, a_horn, group=9)


def amnoze(p, view, phase):
    if view == "icon":
        # party icon: the sleeping lamb simplified for 32 px, a few big puffs
        # of fleece so it reads as one soft cloud
        B = 2 + phase
        y = lambda v: v - B  # noqa: E731
        for cx, cy, r in ((34, 41, 8), (42, 45, 7.4), (30, 50, 8.4), (41, 52, 7)):
            p.blob(cx, y(cy), r, r * 0.9, a_wool, group=20)
        p.blob(20, y(46.4), 7.4, 6.2, a_face, bias=-0.14, group=6)
        p.blob(14.6, y(48.4), 4.2, 3.6, a_face, bias=-0.16, group=6)
        p.blob(23, y(40.5), 4.6, 3.8, a_wool, group=7)
        _crook(p, y)
        p.px(17, y(46), "ink")
        p.px(19, y(46), "ink")
        return
    if view in ("front", "side"):
        # curled up asleep with its chin on its forelegs, drifting a little
        # above the ground; dream bubbles rise from it (the art files
        # hand-finish this)
        B = 2 + (1 if phase == 1 else 0)
        y = lambda v: v - B  # noqa: E731
        for cx, cy, r, g in AMNOZE_CLOUD:
            p.blob(cx, y(cy), r, r * 0.9, a_wool, bias=-0.04, group=20 + g)
        p.blob(46, y(55.4), 2.6, 1.6, a_face, bias=0.1, group=3)
        p.limb([(26, y(53.5)), (17, y(54))], 4.4, 4.0, a_face, bias=0.08, group=4)
        p.blob(15.6, y(54), 2.2, 1.8, a_face, bias=0.1, group=4)
        p.blob(20, y(46.4), 7.0, 5.8, a_face, bias=-0.12, group=6)
        p.blob(14.6, y(48.2), 3.8, 3.2, a_face, bias=-0.14, group=6)
        p.blob(22.5, y(40.5), 4.2, 3.6, a_wool, bias=-0.06, group=7)
        p.blob(26, y(42.5), 3.6, 3.4, a_wool, bias=-0.02, group=7)
        p.lens((24, y(45)), (30.5, y(50)), 3.8, a_face, bend=-1.0, bias=-0.06, group=8)
        _crook(p, y)
        if view != "icon":
            bub = 3 if phase == 1 else 0
            for bx, by, r in ((30, 31, 3.4), (37, 25, 2.4), (42.5, 19.5, 1.8)):
                _bubble(p, bx + bub / 3, y(by - bub), r)
        if p.big:
            p.patch(15, y(45), ["1...1", ".111"], {"1": "ink"})
            p.px(11, y(48), "ink")
            p.pxs([(20, y(48)), (21, y(48))], "pink1")
            p.patch(39, y(45), ["..33f3", ".3ff33", "3ff3", "3ff", "3ff3", ".3fff3", "..333"],
                    {"3": "wool1", "f": "moon"})
        else:
            p.px(17, y(46), "ink")
            p.px(42, y(48), "moon")
        return

    if view == "back":
        # over the shoulder: the fleece cropped by the frame, the sleeping
        # head in profile, the crook hooked toward the foe
        for cx, cy, r, g in ((14, 46, 7.5, 1), (24, 41, 8.0, 1), (35, 41, 7.4, 1), (8, 55, 7.5, 2), (19, 52, 8.5, 2),
                             (31, 51, 8.5, 2), (41, 50, 7.0, 2), (12, 63, 8.0, 3), (25, 62, 9.0, 3), (38, 61, 8.0, 3)):
            p.blob(cx, cy, r, r * 0.92, a_wool, group=20 + g)
        p.blob(46.5, 44, 7.4, 6.6, a_face, bias=-0.1, group=5)
        p.blob(52.5, 47, 4.4, 3.6, a_face, bias=-0.12, group=5)
        p.limb(bez((45.5, 38), (45.5, 29), (47.5, 24)), 5.2, 4.4, a_horn, group=8)
        p.limb(bez((47.5, 24), (50, 19.5), (53.5, 22)), 4.4, 4.0, a_horn, group=8)
        for bx, by, r in ((35, 26, 3.4), (29, 18, 2.4), (24, 11, 1.8)):
            _bubble(p, bx, by, r)
        return

    if view == "down":
        # follower carried along asleep, drifting toward the camera: the
        # round fleece, the sleeping face in the middle, the crook on top,
        # bobbing up and down
        B = 2 * phase
        y = lambda v: v - B  # noqa: E731
        for cx, cy, r in ((22, 44, 7), (42, 44, 7), (26, 51, 7.5), (38, 51, 7.5), (32, 41, 7)):
            p.blob(cx, y(cy), r, r * 0.9, a_wool, group=20)
        p.blob(32, y(47), 7.4, 6.2, a_face, bias=-0.12, group=6)
        p.blob(32, y(51), 4.4, 3.0, a_face, bias=-0.16, group=6)
        p.lens((25.5, y(45)), (18.5, y(50)), 3.8, a_face, bend=1, group=7)
        p.lens((38.5, y(45)), (45.5, y(50)), 3.8, a_face, bend=-1, group=7)
        p.blob(32, y(40.5), 4.8, 3.4, a_wool, group=8)
        p.limb(bez((33, y(40)), (34, y(33)), (32, y(29))), 3.8, 3.2, a_horn, group=9)
        p.limb(bez((32, y(29)), (29.5, y(26)), (27.5, y(29.5))), 3.2, 3.0, a_horn, group=9)
        if p.big:
            p.patch(27, y(47), ["1..1", ".11"], {"1": "ink"})
            p.patch(34, y(47), ["1..1", ".11"], {"1": "ink"})
            p.pxs([(31, y(51)), (32, y(51))], "face0")
        else:
            p.pxs([(29, y(47.5)), (35, y(47.5))], "ink")
        return

    if view == "up":
        # follower drifting away: the cloud of fleece from behind, the ear
        # tips and the crook above it, the moon curl on one flank
        B = 2 * phase
        y = lambda v: v - B  # noqa: E731
        p.lens((25, y(40)), (18, y(45)), 3.8, a_face, bend=1, group=7)
        p.lens((39, y(40)), (46, y(45)), 3.8, a_face, bend=-1, group=7)
        p.limb(bez((33, y(37)), (34, y(30)), (32, y(26)), ), 3.8, 3.2, a_horn, group=9)
        p.limb(bez((32, y(26)), (29.5, y(23)), (27.5, y(26.5))), 3.2, 3.0, a_horn, group=9)
        for cx, cy, r in ((32, 39, 7), (23, 45, 7), (41, 45, 7), (27, 52, 7.5), (37, 52, 7.5)):
            p.blob(cx, y(cy), r, r * 0.9, a_wool, group=20)
        if p.big:
            p.patch(23, y(47), [".3f", "3f3", "3f", ".3f"], {"3": "wool1", "f": "moon"})
        return


MONS = [
    # icon palette 0 keeps the fleece white and the face warm
    Mon("Amnoze", AMNOZE_COLORS, AMNOZE_SHINY, amnoze, foot="hoof", icon_pal=0),
]
