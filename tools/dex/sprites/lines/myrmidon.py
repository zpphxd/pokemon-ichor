"""Myrmidon line: Ergant, Hoplomex (Bug). Aeacus's ants, turned into men."""
from mon_lib import C, Mat, Mon, bez

INK = C.ink

# --------------------------------------------------------------------------
# Ergant, the worker ant with its grain of wheat
# --------------------------------------------------------------------------

ERGANT_COLORS = [
    ("ink", INK),
    # terracotta-brown chitin, dark to light
    ("body0", (88, 40, 24)), ("body1", (136, 64, 32)), ("body2", (184, 96, 48)), ("body3", (216, 136, 80)),
    # limestone sheen on the chitin
    ("lime1", (208, 184, 136)), ("lime2", (240, 224, 184)),
    # the sun-gold wheat
    ("gold0", (152, 96, 24)), ("gold1", (208, 144, 40)), ("gold2", (240, 192, 72)), ("gold3", (248, 232, 152)),
    ("white", C.white),
]
ERGANT_SHINY = {
    # black-figure ink chitin with sun-gold highlights
    "body0": (40, 32, 40), "body1": (64, 56, 64), "body2": (96, 88, 88), "body3": (136, 120, 112),
    "lime1": (216, 160, 48), "lime2": (248, 216, 112),
}

e_chitin = Mat(["body0", "body1", "body2", "body3"], line="body0", cuts=[0.18, 0.42, 0.66])
e_leg = Mat(["body0", "body1", "body2"], line="body0", cuts=[0.4, 0.66])
e_grain = Mat(["gold0", "gold1", "gold2", "gold3"], line="gold0", cuts=[0.2, 0.44, 0.72])
e_stalk = Mat(["gold0", "gold1"], line="gold0", cuts=[0.5])


def _wheat(p, a, b, w=6.4, awns=True, **kw):
    """An ear of wheat from its base a to its tip b. At battle size it is a
    braid of kernels, alternating above and below the midline and shrinking
    toward the tip, each a shaded grain of its own, with awns swept forward
    off the top; small, it is one plump grain head."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    if not p.big:
        return p.lens(a, b, w, e_grain, fat=0.42, **kw)
    n = 6
    if awns:
        for i in range(n):
            t = 0.12 + 0.8 * i / (n - 1)
            if i % 2:
                continue
            x, y = a[0] + dx * t, a[1] + dy * t - w * 0.4
            p.stroke([(x, y), (x + dx * 0.14, y + dy * 0.14 - 3.6)], "gold0")
    pid = p.lens(a, b, w * 0.7, e_grain, fat=0.42, bias=0.2, **kw)
    for i in range(n):
        t = 0.1 + 0.82 * i / (n - 1)
        side = -1 if i % 2 == 0 else 1
        r = w * (0.36 - 0.12 * t)
        cx = a[0] + dx * t
        cy = a[1] + dy * t + side * w * 0.2
        p.blob(cx, cy, r * 1.25, r, e_grain, ang=-20 * side, group=900 + i)
    return pid


def ergant(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        step = phase if view == "side" else 0

        # far legs, behind the body
        p.limb([(31, 50.5), (32, 54.5), (31, 59)], 2.8, 2.0, e_leg, bias=0.35, group=10)
        p.limb([(35, 50.5), (41, 53.5), (43 - step, 58.5)], 2.8, 2.0, e_leg, bias=0.35, group=11)
        # far front leg, up behind the head to the grain
        p.limb([(29, 46), (31.5, 39.5), (30, 33 - L)], 2.6, 2.0, e_leg, bias=0.3, group=12)
        # far antenna
        p.limb([(23, 40), (24, 36.5 - L), (18.5, 35 - L)], 1.6, 1.4, e_leg, bias=0.3)

        # gaster, petiole, thorax
        p.blob(40.5, 49.5, 6.4, 5.8, e_chitin, ang=-10, group=1)
        p.circle(34, 49, 1.9, e_chitin, group=2)
        p.limb([(32, 48.5), (27.5, 46)], 5.2, 6.2, e_chitin, group=3)

        # the wheat ear, held high over the head
        _wheat(p, (37.5, 30.5 - L), (15, 30 - 2 * L), 6.6)
        p.limb([(37.5, 30.5 - L), (42, 33 - L)], 1.6, 1.2, e_stalk)

        # head: big and round, young proportions
        p.blob(21.5, 45.5, 6.6, 6.2, e_chitin, group=4)
        p.blob(17.5, 48.5, 3.4, 2.6, e_chitin, group=4)
        # mandibles: curved blades, opening a little more on frame 2
        p.limb(bez((18.5, 51), (15.5, 52.5 + L), (12.5, 50.5 + L)), 2.8, 1.2, e_chitin, group=5)
        p.limb(bez((16.5, 50), (13.5, 50), (12, 48 - L)), 2.4, 1.2, e_chitin, bias=0.25, group=6, under=True)

        # near legs, over the body
        p.limb([(29.5, 51), (26.5, 54.5), (25.5, 59.5)], 3.0, 2.2, e_leg, group=13)
        p.limb([(33, 51), (37, 54.5), (38.5 + step, 59.5)], 3.0, 2.2, e_leg, group=14)
        # near front leg, along the back of the head up to the grain
        p.limb([(27.5, 48), (27.5, 40.5), (25, 33.5 - L)], 2.8, 2.2, e_leg, group=15)
        # near antenna: scape up, elbow, funiculus forward under the grain
        p.limb([(19.5, 40.5), (20, 37 - L), (14, 36 - L)], 1.8, 1.4, e_leg, group=16)
        p.circle(13.6, 35.8 - L, 1.1, e_leg, group=16)

        if p.big:
            p.eye(16, 43, 4, 5, shine="white", shine_at=(2, 1))
            p.px(17, 46, "gold2")
            p.pxs([(20, 41), (21, 41), (22, 41), (19, 42)], "lime2")
            p.pxs([(28, 44), (29, 44)], "lime1")
            p.pxs([(37, 45), (38, 45), (39, 45), (36, 46)], "lime2")
            p.stroke([(39, 45), (37, 52)], "body0")
            p.stroke([(43, 45), (42, 54)], "body0")
        else:
            p.px(17, 45, "ink")
        return

    if view == "back":
        # over the shoulder: the gaster in the foreground, the thorax rising
        # to the head, turned right in profile, the grain held overhead
        p.limb([(37, 38), (33, 27), (34, 16)], 3.6, 3.0, e_leg, bias=0.3, group=12)
        p.limb([(52, 25), (56, 19), (61, 22)], 2, 1.6, e_leg, bias=0.25)
        p.limb([(45, 48), (52, 54), (54, 64)], 4, 3, e_leg, group=17)
        p.blob(20, 58, 17.5, 12.5, e_chitin, ang=-8, group=1)
        p.circle(35, 46, 3.4, e_chitin, group=2)
        p.limb([(37, 46), (43, 37)], 9.5, 10.5, e_chitin, group=3)
        _wheat(p, (22, 13), (52, 10), 9)
        p.blob(47.5, 30, 9.2, 8.4, e_chitin, group=4)
        p.blob(54, 34, 4.6, 3.6, e_chitin, group=4)
        p.limb(bez((54, 37), (59, 39.5), (61, 35.5)), 3.4, 1.4, e_chitin, group=5)
        p.limb([(44, 38), (43, 27), (45, 15)], 4, 3.4, e_leg, group=15)
        p.limb([(50, 23), (54, 18.5), (59.5, 20.5)], 2.2, 1.8, e_leg, group=16)
        p.circle(60, 21, 1.4, e_leg, group=16)
        p.eye(50, 25, 5, 6, shine="white", shine_at=(3, 1))
        return

    if view == "up":
        # follower walking away: gaster foremost, the grain above the head
        step = phase
        for x0, x1, k in ((26, 20, 0), (38, 44, 1), (27, 22, 1), (37, 42, 0)):
            lift = 1 if (k == step) else 0
            p.limb([(x0, 46), (x1, 52), (x1, 58 - lift)], 3, 2.2, e_leg, bias=0.2, group=10 + x0)
        p.blob(32, 39.5, 6.5, 6, e_chitin, group=4)
        _wheat(p, (21, 31), (43, 31), 7, awns=False)
        p.limb([(28, 40), (26, 33)], 2.6, 2.2, e_leg, group=12)
        p.limb([(36, 40), (38, 33)], 2.6, 2.2, e_leg, group=13)
        p.limb([(29, 35), (27, 29), (23.5, 27)], 1.8, 1.4, e_leg, group=14)
        p.limb([(35, 35), (37, 29), (40.5, 27)], 1.8, 1.4, e_leg, group=15)
        p.blob(32, 51, 7.6, 7, e_chitin, group=1)
        p.circle(32, 44.5, 2.6, e_chitin, group=2)
        return

    if view == "down":
        # follower walking toward the camera: the face, the grain overhead
        step = phase
        for x0, x1, k in ((27, 21, 0), (37, 43, 1), (28, 22, 1), (36, 42, 0)):
            lift = 1 if (k == step) else 0
            p.limb([(x0, 48), (x1, 53), (x1, 59 - lift)], 3, 2.2, e_leg, bias=0.25, group=10 + x0)
        p.blob(32, 50, 5.6, 4.6, e_chitin, group=1)
        _wheat(p, (20, 29.5), (44, 29.5), 7, awns=False)
        p.limb([(28, 44), (24, 37), (25.5, 31)], 2.6, 2.2, e_leg, group=12)
        p.limb([(36, 44), (40, 37), (38.5, 31)], 2.6, 2.2, e_leg, group=13)
        p.blob(32, 41, 7.2, 6.4, e_chitin, group=4)
        p.limb([(29.5, 36), (27, 31.5), (22.5, 31)], 1.8, 1.4, e_leg, group=14)
        p.limb([(34.5, 36), (37, 31.5), (41.5, 31)], 1.8, 1.4, e_leg, group=15)
        p.limb(bez((30, 46), (26.5, 49), (29.5, 51.5)), 2.6, 1.4, e_chitin, group=5)
        p.limb(bez((34, 46), (37.5, 49), (34.5, 51.5)), 2.6, 1.4, e_chitin, group=6)
        p.eye(26.5, 39, 3, 4, shine="white")
        p.eye(34.5, 39, 3, 4, shine="white")
        return


# --------------------------------------------------------------------------
# Hoplomex, the myrmidon: an ant-soldier in a hoplite's guard
# --------------------------------------------------------------------------

HOPLOMEX_COLORS = [
    ("ink", INK),
    # terracotta-brown body plates
    ("body0", (88, 40, 24)), ("body1", (136, 64, 32)), ("body2", (184, 96, 48)), ("body3", (216, 136, 80)),
    # sun-gold bronze: shield, helmet, greaves, and its specular
    ("bronze0", (112, 64, 24)), ("bronze1", (168, 112, 40)), ("bronze2", (216, 168, 64)),
    ("bronze3", (240, 208, 112)), ("spec", (248, 240, 200)),
    # limestone crest, which also lights the chitin
    ("crest0", (160, 128, 88)), ("crest1", (208, 184, 136)), ("crest2", (240, 224, 184)),
    ("white", C.white),
]
HOPLOMEX_SHINY = {
    # a black-figure ink body with a silver marble shield and helmet
    "body0": (40, 32, 40), "body1": (64, 56, 64), "body2": (96, 88, 96), "body3": (136, 128, 128),
    "bronze0": (96, 96, 104), "bronze1": (144, 144, 152), "bronze2": (192, 192, 200),
    "bronze3": (224, 224, 224), "spec": (248, 248, 248),
}

h_chitin = Mat(["body0", "body1", "body2", "body3"], line="body0", cuts=[0.18, 0.42, 0.66])
h_bronze = Mat(["bronze0", "bronze1", "bronze2", "bronze3"], line="bronze0", cuts=[0.2, 0.44, 0.7])
h_crest = Mat(["crest0", "crest1", "crest2"], line="crest0", cuts=[0.36, 0.66])


def _ant_emblem(p, x, y, flip=False):
    """The black-figure ant painted on the shield, about 13 x 9, its top-left
    at (x, y), facing left (right with flip)."""
    rows = [
        "..1.....1....",
        "...1...1.....",
        "..111.1......",
        ".11111.111...",
        "1111111111111",
        ".111.1111111.",
        ".1..1.1..111.",
        "1..1...1.....",
        "..1.....1....",
    ]
    if flip:
        rows = [r[::-1] for r in rows]
    p.patch(x, y, rows, {"1": "ink"})


def hoplomex(p, view, phase):
    # The battle sprites are hand-finished (art/hoplomex_*); this draft gives
    # the icon and the follower the same design: a hoplite lunging behind its
    # round shield, spear leveled, crest sweeping back.
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        step = 1 if (view == "side" and phase == 1) else 0
        # gaster, hanging behind the hips
        p.blob(49, 40, 7.6, 7, h_chitin, ang=-35, bias=0.1, group=2)
        # far leg, thrown back in the lunge
        p.limb([(42, 43), (47, 50)], 5.6, 4.4, h_chitin, bias=0.3, group=10)
        p.limb([(47, 50), (49 - 2 * step, 58)], 4.6, 3.8, h_bronze, bias=0.3, group=11)
        # crest, sweeping back over the helmet
        p.limb(bez((27, 9), (34, -1), (45, 8)), 5.2, 4.6, h_crest, group=30)
        p.limb([(45, 8), (48, 15)], 4.4, 2.4, h_crest, group=30)
        # thorax, the spear behind the far fist
        p.blob(39, 31, 6.4, 8.6, h_chitin, group=1)
        p.limb([(59, 21), (15, 32)], 2.4, 2.4, h_crest, group=40)
        p.lens((15, 32), (3, 35), 4.6, h_bronze, group=41)
        p.blob(50, 23, 3.6, 3.4, h_chitin, group=20)
        # helmet head
        p.blob(36.5, 14, 8, 8, h_bronze, group=4)
        p.limb([(31, 17), (31.5, 21)], 4.6, 3.2, h_bronze, group=4)
        p.limb(bez((30, 20), (26, 23), (27.5, 26)), 2.8, 1.4, h_chitin, group=5)
        # near leg, forward in the lunge
        p.limb([(23, 46), (16 + 2 * step, 52)], 5.8, 4.6, h_chitin, group=12)
        p.limb([(16 + 2 * step, 52), (13 + 2 * step, 58)], 4.6, 3.8, h_bronze, group=13)
        # the shield
        sh = p.blob(24, 41, 12.6, 13, h_bronze, group=7)
        p.blob(24.5, 41.5, 10, 10.4, h_bronze, clip=[sh], bias=0.06, group=8)
        # near fist on the spear
        p.blob(19, 30, 3.6, 3.4, h_chitin, group=21)
        if p.big:
            _ant_emblem(p, 18, 37)
            p.eye(33, 13 - L, 3, 4, shine="white", shine_at=(1, 1))
        else:
            p.px(33, 14, "ink")
        return

    if view == "back":
        # (the hand-finished art replaces this) the shield's inside, the head
        # in right profile under its crest, the spear raised toward the foe
        p.limb(bez((28, 12), (38, 0), (50, 8)), 6, 5, h_crest, group=30)
        p.blob(32, 50, 18, 16, h_chitin, group=1)
        p.blob(42, 17, 10, 9.6, h_bronze, group=4)
        p.limb([(46, 63), (59, 6)], 2.4, 2.4, h_crest, group=40)
        sh = p.blob(16, 46, 14.6, 18, h_bronze, group=7)
        p.blob(16, 46, 12, 15.4, h_bronze, clip=[sh], bias=0.4, group=8)
        p.eye(46, 14, 3, 4, shine="white", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower: the hoplite marching, shield on its arm, spear upright
        step = phase
        p.limb([(28, 44), (27, 51)], 5.4, 4.6, h_chitin, group=12)
        p.limb([(36, 44), (37, 51)], 5.4, 4.6, h_chitin, group=13)
        p.limb([(27, 51), (27, 59 - 2 * step)], 4.6, 4, h_bronze, group=14)
        p.limb([(37, 51), (37, 59 - 2 * (1 - step))], 4.6, 4, h_bronze, group=15)
        if view == "up":
            p.blob(32, 44, 6.6, 6, h_chitin, group=2)
        p.blob(32, 33, 7.6, 8.4, h_chitin, group=1)
        p.limb([(20, 6 + step), (20, 56 + step)], 2.2, 2.2, h_crest, nooutline=True, group=40)
        p.lens((20, 8 + step), (20, -1 + step), 3.6, h_bronze, group=41)
        p.blob(21, 33 + step, 3.4, 3.2, h_chitin, group=21)
        if view == "down":
            p.limb([(32, 11), (32, 2)], 5, 4.4, h_crest, group=30)
        p.blob(32, 17, 7.6, 7.4, h_bronze, group=4)
        if view == "up":
            p.limb([(32, 9), (32, 25)], 5, 4, h_crest, group=30)
        else:
            p.limb(bez((29.5, 23), (27, 26), (29.5, 28.5)), 2.6, 1.4, h_chitin, group=5)
            p.limb(bez((34.5, 23), (37, 26), (34.5, 28.5)), 2.6, 1.4, h_chitin, group=6)
        sh = p.blob(41, 37, 9, 10, h_bronze, bias=0.15 if view == "up" else 0.0, group=7)
        if view == "down":
            p.blob(41.3, 37.3, 7, 8, h_bronze, clip=[sh], bias=0.06, group=8)
            p.eye(27, 16, 2, 3, shine="white")
            p.eye(35, 16, 2, 3, shine="white")
        return


ANT_FOOT = [
    "................",
    "................",
    "....#......#....",
    "....##....##....",
    "................",
    "................",
    "..#..........#..",
    "..##........##..",
    "................",
    "................",
    "....#......#....",
    "....##....##....",
    "................",
    "................",
    "................",
    "................",
]

MONS = [
    Mon("Ergant", ERGANT_COLORS, ERGANT_SHINY, ergant, foot=ANT_FOOT),
    Mon("Hoplomex", HOPLOMEX_COLORS, HOPLOMEX_SHINY, hoplomex, foot=ANT_FOOT, icon_pal=1),
]
