"""Kouretes line: Kymbash, Kourodin (Steel). The Kouretes, who clashed spear
on shield around the Diktaean cave so Kronos would not hear the infant Zeus."""
from mon_lib import C, Mat, Mon, bez, bez3

INK = C.ink

# --------------------------------------------------------------------------
# Kymbash, the clashing shield
# --------------------------------------------------------------------------

KYMBASH_COLORS = [
    ("ink", INK),
    # sun-gold and terracotta bronze, with a pale specular
    ("br0", (88, 40, 24)), ("br1", (144, 72, 32)), ("br2", (192, 112, 48)), ("br3", (232, 160, 64)),
    ("br4", (248, 208, 112)), ("spec", (248, 248, 216)),
    # the black-figure glaze of the painted dancer
    ("paint", (48, 32, 32)),
    # marble-white eyes
    ("eye0", (176, 168, 160)), ("white", C.white),
    # the spear-shaft: ash wood
    ("wood0", (96, 56, 32)), ("wood1", (152, 104, 56)), ("wood2", (200, 152, 96)),
]
KYMBASH_SHINY = {
    # silver bronze, and the dancer painted Aegean blue
    "br0": (56, 56, 72), "br1": (104, 104, 120), "br2": (152, 152, 168), "br3": (200, 200, 208),
    "br4": (232, 232, 240), "spec": (248, 248, 248),
    "paint": (48, 104, 176),
}

ky = Mat(["br0", "br1", "br2", "br3", "br4"], line="br0", cuts=[0.14, 0.34, 0.56, 0.78])
ky_in = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.24, 0.5, 0.76])
ky_wood = Mat(["wood0", "wood1", "wood2"], line="wood0", cuts=[0.36, 0.7])
ky_eye = Mat(["eye0", "white"], line="eye0", cuts=[0.62])


ky_icon = Mat(["br1", "br2", "br3", "br4"], line="br1", cuts=[0.3, 0.52, 0.74])

# the black-figure dancer leaping in a split, about 16 x 11: arms flung up
# and forward, one leg forward, one back
DANCER = [
    "...........11...",
    ".....11....1....",
    "....1111..1.....",
    "....1111.1......",
    ".....11.11......",
    ".1..111111......",
    "..1111111.......",
    ".....1111.......",
    "....111.111.....",
    "..111.....1111..",
    "111.........111.",
]
KY_EYES = [".111...111.", "1www1.1www1", "11ww1.11ww1", "11we1.11we1", ".111...111."]
KY_EYES_SHUT = ["...........", "11.......11", "..111.111..", "11.......11", "..........."]


def _dancer(p, x, y, color="paint"):
    """The painted dancer, top-left at (x, y); skipped below battle size."""
    p.patch(x, y, DANCER, {"1": color})


def _ky_face(p, x, y, shut=False):
    """Kymbash's wide eyes, top-left at (x, y), and the dent of a mouth below."""
    if p.big:
        legend = {"1": "ink", "w": "white", "e": "eye0", "2": "br0", "6": "br4"}
        p.patch(x, y, KY_EYES_SHUT if shut else KY_EYES, legend)
        p.patch(x + 2, y + 6, [".111.", "12221", ".111."] if shut else ["1...1", ".111.", ".66.."], legend)
    else:
        p.px(x + 2, y + 2, "white")
        p.px(x + 8, y + 2, "white")


def kymbash(p, view, phase):
    if view in ("front", "side", "icon"):
        # The battle front is hand-finished (art/kymbash_front*); this draft
        # gives the icon and the side follower the same shield.
        icon = view == "icon"
        B = ky_icon if icon else ky
        NEAR = {"flat": 2} if icon else {}
        FAR = {"flat": 1} if icon else {}
        LIT = {"flat": 3} if icon else {}
        clang = phase == 1 and view == "front"
        bob = 1 if (view == "side" and phase == 1) else 0
        y = -bob - 2 * clang
        T = 2.2 * clang
        # the shaft behind, sticking out like a pair of arms; spear-point
        # left, butt-spike right
        p.limb([(10, 44.7 - T + y), (54, 32.1 + T + y)], 3.6, 3.6, ky_wood, group=30)
        p.lens((11.6, 44.2 - T + y), (2.6, 47.1 - T + y), 5.2, B, fat=0.4, group=31, **LIT)
        p.lens((52.6, 32.5 + T + y), (59.4, 30.3 + T + y), 3.8, B, fat=0.3, group=32, **FAR)
        # the shield's depth, its rim, the field, the boss
        p.blob(33.6, 37.4 + y, 12.6, 16.4, B, bias=0.34, group=6, **FAR)
        sh = p.blob(30, 37 + y, 13.0, 16.6, B, bias=-0.2, group=7, **NEAR)
        p.blob(30.5, 37.4 + y, 10.0, 13.4, B, clip=[sh], bias=-0.26, group=8, **LIT)
        p.blob(29.2, 42 + y, 7.2, 6.6, B, bias=-0.16, group=9, **NEAR)
        if p.big:
            _dancer(p, 21, 24 + y)
        _ky_face(p, 24, 39 + y, shut=clang)
        return

    if view == "back":
        # (the hand-finished art replaces this) the inside of the shield,
        # the boss peering past the rim, the shaft aimed at the foe
        p.blob(43.4, 41.4, 7.6, 8.6, ky, bias=-0.3, group=5)
        rim = p.blob(27, 42, 16, 25, ky, group=6)
        p.blob(25.2, 42.8, 12.2, 21.4, ky_in, clip=[rim], bias=0.3, group=7)
        p.limb([(3, 53), (55, 27)], 3.6, 3.6, ky_wood, group=30)
        p.lens((54, 27.5), (62, 23.6), 6.4, ky, fat=0.42, group=31)
        p.patch(44, 35, [".111.", "1www1", "1ww11", "1ww11", "1ewe1", ".111."],
                {"1": "ink", "w": "white", "e": "eye0"})
        return

    if view in ("down", "up"):
        # follower: the shield bouncing along face-on, its shaft for arms
        bob = phase
        y = -2 * bob
        p.limb([(6, 40 + y), (58, 40 + y)], 3.6, 3.6, ky_wood, group=30)
        p.lens((7.6, 40 + y), (1.6, 40 + y), 5.0, ky, fat=0.4, group=31)
        p.lens((56.4, 40 + y), (62, 40 + y), 3.6, ky, fat=0.3, group=32)
        rim = p.blob(32, 38 + y, 15, 17, ky, bias=-0.2 if view == "down" else 0.1, group=7)
        if view == "down":
            p.blob(32, 38.4 + y, 11.8, 13.8, ky, clip=[rim], bias=-0.26, group=8)
            p.blob(32, 43 + y, 7.6, 7.0, ky, bias=-0.16, group=9)
            if p.big:
                _dancer(p, 24, 25 + y)
            _ky_face(p, 27, 40 + y)
        else:
            p.blob(32, 39 + y, 12, 14, ky_in, clip=[rim], bias=0.3, group=8)
            p.limb([(24, 41 + y), (40, 38 + y)], 5.0, 5.0, ky, bias=-0.1, group=9)
        return


# --------------------------------------------------------------------------
# Kourodin, the shield-dancer
# --------------------------------------------------------------------------

KOURODIN_COLORS = [
    ("ink", INK),
    ("br0", (80, 40, 24)), ("br1", (144, 72, 32)), ("br2", (200, 120, 48)), ("br3", (232, 168, 72)),
    ("br4", (248, 216, 128)), ("spec", (248, 248, 216)),
    # the horsehair crest and the kilt's pleats
    ("crest0", (104, 32, 24)), ("crest1", (168, 56, 32)), ("crest2", (216, 104, 56)),
    # limestone skin
    ("skin0", (152, 128, 104)), ("skin1", (208, 192, 160)), ("skin2", (240, 232, 208)),
    # the eyes: Kymbash's in the shield, and its own behind the visor
    ("eye0", (176, 168, 160)), ("white", C.white),
]
KOURODIN_SHINY = {
    "br0": (56, 56, 72), "br1": (104, 104, 120), "br2": (152, 152, 168), "br3": (200, 200, 208),
    "br4": (232, 232, 240), "spec": (248, 248, 248),
    "crest0": (24, 56, 120), "crest1": (48, 104, 176), "crest2": (112, 168, 224),
}

kd = Mat(["br0", "br1", "br2", "br3", "br4"], line="br0", cuts=[0.14, 0.34, 0.56, 0.78])
kd_in = Mat(["br0", "br1", "br2", "br3"], line="br0", cuts=[0.24, 0.5, 0.76])
kd_crest = Mat(["crest0", "crest1", "crest2"], line="crest0", cuts=[0.36, 0.68])
kd_skin = Mat(["skin0", "skin1", "skin2"], line="skin0", cuts=[0.36, 0.68])
kd_wood = Mat(["br0", "br1"], line="br0", cuts=[0.5])
kd_icon = Mat(["br1", "br2", "br3", "br4"], line="br1", cuts=[0.3, 0.52, 0.74])


def _kd_eyes_boss(p, x, y, shut=False):
    """Kymbash's wide eyes, still open in the shield's boss."""
    legend = {"1": "ink", "w": "white", "e": "eye0"}
    if p.big:
        p.patch(x, y, KY_EYES_SHUT if shut else KY_EYES, legend)
    else:
        p.px(x + 2, y + 2, "white")
        p.px(x + 7, y + 2, "white")


def kourodin(p, view, phase):
    if view in ("front", "side", "icon"):
        # The battle front is hand-finished (art/kourodin_front*); this draft
        # gives the icon and the side follower the same leap: near knee high,
        # the eyed shield on the near arm, the spear raised to strike it.
        icon = view == "icon"
        B = kd_icon if icon else kd
        NEAR = {"flat": 2} if icon else {}
        FAR = {"flat": 1} if icon else {}
        LIT = {"flat": 3} if icon else {}
        st = 1 if (view == "side" and phase == 1) else 0
        # far arm raised with the spear, the crest, the spear
        p.blob(40.4, 22.6, 4.4, 4.2, kd_skin, bias=0.16, group=20)
        p.limb([(40.4, 22.4), (49.6, 18.4)], 5.6, 5.0, kd_skin, bias=0.14, group=20)
        p.limb([(49.6, 18.4), (52.2, 9.2)], 5.0, 4.4, kd_skin, bias=0.08, group=21)
        cpath = bez3((18.0, 13.0), (18.6, 6.0), (44.6, 3.6), (47.8, 20.6), n=24)
        p.limb(cpath[:13], 5.0, 9.6, kd_crest, group=40)
        p.limb(cpath[12:], 9.6, 3.0, kd_crest, group=40)
        p.limb([(60.0, 3.8), (36.0, 18.2)], 2.6, 2.6, kd_wood, group=41)
        p.lens((37.8, 17.2), (29.6, 22.2), 4.8, B, fat=0.36, group=42, **LIT)
        p.blob(52.2, 8.6, 3.2, 3.0, kd_skin, group=43)
        # far leg stretched down and back
        far = [(40.8, 42.0), (47.6, 49.2), (52.6, 55.2), (55.4, 60.2)]
        if st:
            far = [(40.8, 42.0), (42.6, 49.2), (42.6, 55.2), (41.4, 60.2)]
        p.limb(far[:2], 7.2, 6.0, kd_skin, bias=0.2, group=10)
        p.limb(far[1:3], 5.8, 4.6, B, bias=0.2, group=11, **FAR)
        p.limb(far[2:], 4.0, 2.8, kd_skin, bias=0.22, group=12)
        # torso, kilt, near leg
        p.blob(33.6, 28.0, 8.8, 9.6, B, ang=-12, bias=0.04, group=1, **NEAR)
        p.poly([(26.6, 34.6), (40.6, 33.0), (45.0, 37.0), (50.4, 43.0), (47.4, 45.6), (39.4, 46.4),
                (31.6, 46.6), (25.0, 44.6), (25.4, 39.0)], kd_crest, bias=-0.08, group=2)
        if p.big:
            p.stroke([(26, 44), (49, 44)], "skin2")
        p.limb([(34.0, 41.6), (25.2, 46.2)], 8.2, 7.0, kd_skin, bias=-0.12, group=13)
        p.limb([(24.8, 48.6), (26.0, 55.0)], 5.8, 4.6, B, bias=-0.1, group=14, **NEAR)
        p.limb([(26.0, 55.0), (27.4, 58.8)], 4.0, 2.8, kd_skin, group=14)
        # helmet
        p.poly([(27.6, 12.4), (33.6, 14.2), (34.0, 19.8), (31.4, 22.2), (27.0, 21.2)], B, bias=0.06, group=3, **FAR)
        p.blob(24.8, 14.6, 7.0, 7.2, B, bias=-0.14, group=4, **NEAR)
        p.poly([(18.2, 12.6), (17.6, 18.6), (19.6, 22.6), (23.2, 23.4), (26.4, 21.2), (26.8, 13.8), (22.2, 10.8)],
               B, bias=-0.2, group=5, **LIT)
        # the shield
        p.blob(20.2, 31.0, 10.6, 12.4, B, bias=0.34, group=6, **FAR)
        sh = p.blob(17.4, 30.6, 11.0, 12.8, B, bias=-0.22, group=7, **NEAR)
        p.blob(17.8, 30.9, 8.4, 10.0, B, clip=[sh], bias=-0.26, group=8, **LIT)
        p.blob(16.8, 33.8, 5.8, 5.6, B, bias=-0.16, group=9, **NEAR)
        _kd_eyes_boss(p, 12, 30)
        if p.big:
            p.patch(18, 14, ["1113531112", "1f13531ff1", "1ef141ffe1"],
                    {"1": "ink", "2": "br0", "3": "br1", "5": "br3", "4": "br2", "f": "white", "e": "eye0"})
        else:
            p.px(19, 15.5, "white")
            p.px(24.5, 15.5, "white")
        return

    if view == "back":
        # (the hand-finished art replaces this) the helmet in right profile
        # under the crest, the spear aloft, the shield's inside on the left
        p.limb([(51.0, 42.0), (57.0, 33.0), (56.4, 22.6)], 6.2, 5.2, kd_skin, group=20)
        p.limb([(54.6, 44.0), (58.6, 6.0)], 2.8, 2.8, kd_wood, group=21)
        p.blob(36, 60, 18, 22, kd, group=1)
        cpath = bez3((46.4, 17.0), (46.0, 4.2), (22.0, 3.6), (19.4, 34.0), n=24)
        p.limb(cpath, 8.0, 3.0, kd_crest, group=40)
        p.blob(38.6, 24.4, 8.0, 8.4, kd, group=3)
        sh = p.blob(14, 46, 11.4, 14.6, kd, group=7)
        p.blob(12.8, 46.8, 8.6, 12.0, kd_in, clip=[sh], bias=0.3, group=8)
        return

    if view in ("down", "up"):
        # follower: marching toward or away from the camera, the shield on
        # its left arm, the spear upright in its right hand, crest high
        step = phase
        p.limb([(28.4, 44), (27.6, 51), (27.6, 59 - 2 * step)], 5.4, 4.0, kd_skin, group=12)
        p.limb([(35.6, 44), (36.4, 51), (36.4, 59 - 2 * (1 - step))], 5.4, 4.0, kd_skin, group=13)
        p.limb([(27.6, 50), (27.6, 56 - 2 * step)], 5.0, 4.4, kd, group=14)
        p.limb([(36.4, 50), (36.4, 56 - 2 * (1 - step))], 5.0, 4.4, kd, group=15)
        p.poly([(24, 46), (26, 37), (38, 37), (40, 46)], kd_crest, group=2)
        if p.big:
            p.stroke([(24, 45), (40, 45)], "skin2")
        p.blob(32, 30, 8.4, 8.0, kd, bias=-0.06, group=1)
        # facing the camera its left (shield) arm is on our right
        sx = 18 if view == "down" else 46          # the spear hand
        hx = 46 if view == "down" else 18          # the shield arm
        p.limb([(32 + (sx - 32) * 0.55, 26), (sx, 31)], 4.4, 4.0, kd_skin, group=20)
        p.limb([(sx, 6), (sx, 42)], 2.4, 2.4, kd_wood, group=21)
        p.lens((sx, 7), (sx, -0.6), 4.2, kd, fat=0.4, group=22)
        if view == "down":
            p.limb(bez((32, 14), (32, 1), (32, 2)), 4.6, 4.0, kd_crest, group=40)
        p.blob(32, 18, 7.2, 7.4, kd, bias=-0.1, group=3)
        if view == "up":
            p.limb(bez((32, 7), (32, 14), (32, 30)), 7.0, 3.6, kd_crest, group=40)
        sh = p.blob(hx, 35, 10.4, 11.4, kd, bias=-0.16 if view == "down" else 0.2, group=7)
        if view == "down":
            p.blob(hx, 35.4, 8.0, 8.8, kd, clip=[sh], bias=-0.26, group=8)
            p.blob(hx, 37.4, 5.0, 4.8, kd, bias=-0.16, group=9)
            _kd_eyes_boss(p, hx - 5, 35)
            p.patch(28, 17, ["1f1..1f1", "1ff11ff1"], {"1": "ink", "f": "white"}, small=(29, 18, ["1..1"]))
        else:
            p.blob(hx, 36, 8.0, 9.0, kd_in, clip=[sh], bias=0.3, group=8)
        return


# Kourodin dances on the balls of its feet: a narrow bare foot, toes and pad
KOURODIN_FOOT = [
    "................",
    ".....#.#.#......",
    "....#.#.#.#.....",
    "................",
    ".....######.....",
    "....#######.....",
    "....#######.....",
    ".....#####......",
    ".....####.......",
    ".....####.......",
    "................",
    ".....####.......",
    ".....####.......",
    "......##........",
    "................",
    "................",
]

MONS = [
    # icon palette 5 keeps the bronze field warm (palette 0 turns it olive)
    Mon("Kymbash", KYMBASH_COLORS, KYMBASH_SHINY, kymbash, foot="blank", icon_pal=5),
    # icon palette 5 keeps the bronze gold and the crest red
    Mon("Kourodin", KOURODIN_COLORS, KOURODIN_SHINY, kourodin, foot=KOURODIN_FOOT, icon_pal=5),
]
