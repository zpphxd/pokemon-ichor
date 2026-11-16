"""Amalthea line: Eripip, Kerazap, Kerastorm (the region's mascot).

Amalthea, the goat who nursed the infant Zeus in the Diktaean cave. Her
broken horn became the cornucopia and her hide the aegis, the storm-cloud
Zeus shook to raise thunder (Ovid, Fasti 5; Hyginus, Astronomica 2.13).
The line grows from a static-charged puff of a kid, through a prancing
young goat with sparking horn buds, into the storm-fleeced nurse goat whose
snapped horn pours out fruit.
"""
from mon_lib import C, Mat, Mon, bez

INK = C.ink


def _zig(p, pts, core="gold1", edge=None):
    """A little zigzag spark: a 1 px bright line, optionally with a darker
    edge pixel under each bend."""
    p.stroke(pts, core)
    if edge and p.big:
        for x, y in pts[1:-1]:
            p.px(x, y + 1, edge)


# --------------------------------------------------------------------------
# Eripip, the static kid
# --------------------------------------------------------------------------

ERIPIP_COLORS = [
    ("ink", INK),
    # marble-white fleece shaded warm, toward limestone
    ("fl0", (160, 144, 120)), ("fl1", (200, 192, 168)), ("fl2", (232, 224, 208)), ("fl3", C.white),
    # limestone muzzle, inner ears and hooves
    ("lm0", (120, 88, 56)), ("lm1", C.limestone[0]), ("lm2", C.limestone[1]), ("lm3", C.limestone[2]),
    # sun-gold sparks with one pale Aegean highlight
    ("gold0", (200, 136, 32)), ("gold1", C.sungold[1]), ("gold2", (248, 240, 168)),
    ("sky", C.aegean[3]), ("iris", C.aegean[1]),
]
ERIPIP_SHINY = {
    # pale Aegean-blue fleece, marble-white sparks
    "fl0": (96, 128, 176), "fl1": (144, 184, 224), "fl2": (192, 224, 240), "fl3": (232, 248, 248),
    "gold0": (168, 160, 152), "gold1": (216, 208, 200), "gold2": (248, 248, 240),
    "sky": (248, 224, 120),
}

e_fleece = Mat(["fl0", "fl1", "fl2", "fl3"], line="fl0", cuts=[0.3, 0.56, 0.9])
e_face = Mat(["fl1", "fl2", "fl3"], line="fl0", cuts=[0.5, 0.8])
e_ear = Mat(["lm1", "lm2", "lm3"], line="lm0", cuts=[0.4, 0.66])
e_muzzle = Mat(["lm1", "lm2", "lm3"], line="lm0", cuts=[0.4, 0.62])
e_leg = Mat(["fl1", "fl2", "fl3"], line="fl0", cuts=[0.4, 0.66])
e_hoof = Mat(["lm0", "lm1"], line="ink", cuts=[0.5])
# at icon size the shared icon palettes turn fl1 gray, so keep the fleece light
e_fleece_s = Mat(["fl1", "fl2", "fl3"], line="fl1", cuts=[0.72, 0.95])
e_face_s = Mat(["fl2", "fl3"], line="fl1", cuts=[0.85])


def _ehoof(p, x, y, far=False):
    p.rect(x, y, x + 2, y + 1, e_hoof, bias=0.3 if far else 0)


def _cloud(p, puffs, mat, group, **kw):
    """Several circles as one shaded form (a scalloped fleece edge)."""
    from mon_lib import ellipse_pts
    polys = [ellipse_pts(x, y, r, r * k) for x, y, r, k in puffs]
    return p.polys(polys, mat, group=group, **kw)


def eripip(p, view, phase):
    # The battle front and back are hand-finished (art/eripip_*.txt); this
    # draft drives the icon and the follower, so it keeps the same design:
    # a white puffball kid, sideways ears, a limestone muzzle and hooves.
    if view in ("front", "side", "icon"):
        fleece, face = (e_fleece, e_face) if p.big or view == "side" else (e_fleece_s, e_face_s)
        walk = view == "side"
        hop = walk and phase == 1     # the follower pronks: all four legs tucked at once
        E = 1 if (phase == 1 and not walk) else 0     # ears flick up
        dy = -2 if hop else 0
        legs = [(32.5, 37.5), (40, 45)]
        for x, far in ((34, True), (40, True), (28, False), (45, False)):
            x0 = x + (0.8 if hop and x < 36 else -0.8 if hop else 0)
            p.limb([(x, 53 + dy), (x0, (57 if hop else 59) + (0 if far else 1))], 3.4 if far else 3.8,
                   3.0 if far else 3.4, e_leg, bias=0.3 if far else 0, group=10 + int(far))
            fy = (57 if hop else 59) + (0 if far else 1)
            p.rect(int(x0) - 1, int(fy), int(x0) + 1, int(fy) + 1, e_hoof, bias=0.3 if far else 0)
        p.lens((41.5, 39 + dy), (45, 33.5 + dy), 4, fleece, bend=-0.5, group=19)            # tail
        _cloud(p, [(36.5, 46.5 + dy, 9, 0.85), (42.6, 40.6 + dy, 3.8, 1),
                   (37.2, 38.8 + dy, 4.2, 1), (31.6, 40.2 + dy, 3.8, 1),
                   (45.2, 46.6 + dy, 3.6, 1), (41.2, 52.8 + dy, 3.6, 1),
                   (35, 53.8 + dy, 3.6, 1), (29.6, 52.4 + dy, 3.4, 1),
                   (28.6, 47 + dy, 4.3, 1)], fleece, 1)
        # ears stick out sideways (flicked up in frame 2)
        p.lens((17, 41 + dy), (11, 41.5 - 4 * E + dy), 3.4, e_ear, bend=0.3, bias=0.2, group=30)
        p.lens((30, 41 + dy), (37, 42 - 6 * E + dy), 3.6, e_ear, bend=-0.4, group=31)
        p.blob(24, 44.3 + dy, 7.4, 7, face, group=32)
        p.blob(18.2, 47.7 + dy, 3.8, 2.7, e_muzzle, ang=10, group=32)
        _cloud(p, [(24.6, 36.9 + dy, 3.4, 0.85), (29, 38.3 + dy, 2.8, 0.93), (20.6, 38.6 + dy, 2.2, 0.95)],
               fleece, 33)
        if p.big:
            p.eye(24, 40 + dy, 4, 6, iris="iris", shine="fl3", shine_at=(1, 1))
            p.eye(18, 41 + dy, 2, 4, shine="fl3", shine_at=(0, 1))
            p.pxs([(15, 45 + dy), (16, 45 + dy)], "ink")
            p.stroke([(17, 47 + dy), (19, 48 + dy)], "lm0")
            _zig(p, [(36, 33), (37, 31), (38, 31), (40, 29)], "gold1", "gold0")
            p.px(38, 31, "sky")
            _zig(p, [(46, 41), (49, 38), (47, 38), (50, 35 - E)], "gold2", "gold0")
            p.stroke([(33, 41 + dy), (35, 40 + dy), (38, 41 + dy)], "fl3")
            p.stroke([(38, 48 + dy), (40, 50 + dy), (42, 49 + dy)], "fl1")
        else:
            p.pxs([(19, 42 + dy), (24, 42 + dy)], "ink")
            p.px(37, 33, "gold1")
        return

    if view == "back":
        # (the hand-finished art replaces this) over the shoulder, the head
        # turned right in profile on the fleece
        p.lens((9, 40), (8, 35.5), 4.4, e_fleece, group=19)
        _cloud(p, [(28, 58, 19, 0.53), (12, 50, 5.4, 1), (19, 45, 6, 0.93), (28, 43, 6.2, 0.94),
                   (36.5, 45, 5.6, 0.96), (38.5, 41, 6, 0.9), (46, 46, 5.4, 1.04)], e_fleece, 1)
        p.lens((36, 31), (30, 34), 4.4, e_ear, bend=-0.5, group=30)
        p.blob(44, 33, 8.6, 8.2, e_face, group=32)
        p.blob(52.6, 37.6, 4.6, 3.3, e_muzzle, ang=-8, group=32)
        _cloud(p, [(42, 25, 4.2, 0.76), (37.3, 27, 2.8, 0.96), (46.8, 25.8, 2.8, 0.9)], e_fleece, 33)
        p.eye(44, 28, 4, 6, iris="iris", shine="fl3", shine_at=(1, 1))
        if p.big:
            p.px(56, 36, "ink")
            p.stroke([(51, 39), (54, 39)], "lm0")
            _zig(p, [(17, 40), (19, 37), (17, 37), (20, 34)], "gold1", "gold0")
            p.px(20, 34, "sky")
            p.stroke([(19, 48), (22, 46), (25, 47)], "fl3")
            p.stroke([(30, 52), (33, 54), (36, 53)], "fl1")
        return

    if view in ("down", "up"):
        # follower: facing the camera, or walking away; phase 1 bunches the
        # legs for a pronk
        s = phase
        for x, dx in ((27.5, -0.6), (36.5, 0.6)):
            x1 = x + dx * (1 - s) * 2
            p.limb([(x, 53), (x1, 59 - 2 * s)], 3.8, 3.4, e_leg, group=12)
            p.rect(int(x1) - 1, int(59 - 2 * s), int(x1) + 1, int(60 - 2 * s), e_hoof)
        if view == "up":
            p.lens((23, 41), (16, 41.5 - 2 * s), 3.6, e_ear, bias=0.1, group=30)
            p.lens((41, 41), (48, 41.5 - 2 * s), 3.6, e_ear, bias=0.1, group=31)
            p.blob(32, 40, 7, 6.2, e_face, group=32)
            _cloud(p, [(32, 35.5, 4.4, 0.8), (28, 36.6, 2.6, 1), (36, 36.6, 2.6, 1)], e_fleece, 33)
            _cloud(p, [(32, 50, 10, 0.75), (24, 47, 3.6, 1), (40, 47, 3.6, 1), (28, 44.5, 3.6, 1), (36, 44.5, 3.6, 1)],
                   e_fleece, 1)
            p.lens((32, 45.5), (33, 40), 4, e_fleece, group=2)
            return
        _cloud(p, [(32, 49, 10, 0.72), (24, 46, 3.5, 1), (40, 46, 3.5, 1), (25, 52, 3.5, 1), (39, 52, 3.5, 1)],
               e_fleece, 1)
        p.lens((25, 39), (17, 39.5 - 2 * s), 3.8, e_ear, group=30)
        p.lens((39, 39), (47, 39.5 - 2 * s), 3.8, e_ear, group=31)
        p.blob(32, 41, 7.4, 6.8, e_face, group=32)
        p.blob(32, 45.6, 3.8, 2.6, e_muzzle, group=32)
        _cloud(p, [(32, 35, 4.6, 0.75), (28, 36, 2.6, 1), (36, 36, 2.6, 1)], e_fleece, 33)
        p.eye(27, 39, 3, 4, iris="iris", shine="fl3")
        p.eye(35, 39, 3, 4, iris="iris", shine="fl3")
        p.pxs([(31, 45), (32, 45)], "ink")
        if p.big:
            _zig(p, [(43, 36), (44, 34), (45, 34), (46, 32)], "gold1", "gold0")
        return


# --------------------------------------------------------------------------
# Kerazap, the spark goat
# --------------------------------------------------------------------------

KERAZAP_COLORS = [
    ("ink", INK),
    # marble-white fleece with marble-gray cloud shading
    ("fl0", (120, 120, 128)), ("fl1", (168, 168, 168)), ("fl2", (216, 208, 200)), ("fl3", C.white),
    # limestone face, coat and legs
    ("lm0", (112, 80, 48)), ("lm1", (168, 136, 88)), ("lm2", (208, 176, 128)), ("lm3", (232, 216, 176)),
    # sun-gold horn tips and sparks
    ("gold0", (200, 136, 32)), ("gold1", C.sungold[1]), ("gold2", (248, 240, 168)),
    ("sky", C.aegean[3]), ("iris", C.aegean[1]),
    ("hoof", (80, 56, 40)),
]
KERAZAP_SHINY = {
    # pale Aegean-blue fleece, marble-white horn sparks
    "fl0": (72, 104, 152), "fl1": (128, 168, 216), "fl2": (184, 216, 240), "fl3": (232, 248, 248),
    "gold0": (168, 160, 152), "gold1": (216, 208, 200), "gold2": (248, 248, 240),
    "sky": (248, 224, 120),
}

z_fleece = Mat(["fl0", "fl1", "fl2", "fl3"], line="fl0", cuts=[0.34, 0.6, 0.92])
z_coat = Mat(["lm0", "lm1", "lm2", "lm3"], line="lm0", cuts=[0.18, 0.42, 0.7])
z_leg = Mat(["lm0", "lm1", "lm2"], line="lm0", cuts=[0.3, 0.6])
z_horn = Mat(["hoof", "lm1", "lm2"], line="hoof", cuts=[0.34, 0.66])
z_tip = Mat(["gold0", "gold1", "gold2"], line="gold0", cuts=[0.3, 0.62])
z_hoof = Mat(["hoof", "lm0"], line="ink", cuts=[0.5])


def _zhoof(p, x, y, far=False, w=3):
    p.rect(x, y, x + w - 1, y + 1, z_hoof, bias=0.3 if far else 0)
    if p.big:
        p.px(x + w // 2, y + 1, "ink")


def _horn_bud(p, base, tip, w, bias=0.0):
    """A stubby horn bud whose top third is a sun-gold spark tip."""
    mid = (base[0] + (tip[0] - base[0]) * 0.5, base[1] + (tip[1] - base[1]) * 0.5)
    p.limb([base, mid], w, w * 0.85, z_horn, bias=bias)
    p.limb([mid, tip], w * 0.85, w * 0.45, z_tip, bias=bias)


KERAZAP_MINI = {
    "side": (
        "......bc..bc..............",
        ".....9bb.9bb..............",
        "....19999991..............",
        "..18899989991.............",
        ".189951898991..........55.",
        "188891e189991.........4551",
        "188899989891........14531.",
        ".16788988891555.....14531..",
        "...17888555555551...1431...",
        "....17555555555554189991...",
        ".....15555555444544199991..",
        "....145555544433344188991..",
        "....155554433333334188891..",
        ".....14443333334441888891..",
        "......1233333344418888891..",
        ".....1881333344188898891...",
        "....1881.12334188888991....",
        "...1891..17881188818881....",
        "...881...17881.1781.1781...",
        "...ff1...17881..781..781...",
        ".........17881..781..781...",
        ".........1ff1...ff1.1ff1...",
    ),
    "down": (
        "....bc.....bc....",
        "....bb.....bb....",
        "...1991...1991...",
        ".189999999999981.",
        "18999999999999981",
        ".178995189951881.",
        "..1881e181e1881..",
        "...18899998881...",
        "...17889998871...",
        "....188118881....",
        "....145555541....",
        "..1555555555551..",
        ".155555555555541.",
        ".155555544444441.",
        "..1444444333341..",
        "..1233333333321..",
        "...17888888871...",
        "...1881...1781...",
        "...1891...1781...",
        "...1891...1781...",
        "...1ff1...1781...",
        "..........1ff1...",
    ),
    "up": (
        "....bc.....bc....",
        "....bb.....bb....",
        "...1991...1991...",
        ".189999999999981.",
        "18999999999999981",
        ".178899999998871.",
        "..178999999871...",
        "...1788888871....",
        "...1555555541....",
        "..155555555541...",
        ".155555555555441.",
        ".155555544444441.",
        "..1444444333341..",
        "..1233333333321..",
        "...17889558871...",
        "...18894551881...",
        "...18891431881...",
        "...1881...1781...",
        "...1891...1781...",
        "...1891...1781...",
        "...1ff1...1781...",
        "..........1ff1...",
    ),
}
KERAZAP_MINI_STEP = {
    "side": {
        16: "....1891.12334188888991....",
        17: ".....881.17881188818881....",
        18: ".....ff1.17881.1781.1881...",
        19: ".........17881.1781..881...",
        20: ".........17881.1781..ff1...",
        21: ".........1ff1..1ff1........",
    },
    "down": {
        19: "...1891...1781...",
        20: "...1891...1ff1...",
        21: "...1ff1..........",
    },
    "up": {
        19: "...1891...1781...",
        20: "...1891...1ff1...",
        21: "...1ff1..........",
    },
}


def _goat_mini(p, frames, steps, view, phase):
    direction = "side" if view == "icon" else view
    rows = list(frames[direction])
    if phase:
        for y, row in steps[direction].items():
            rows[y] = row
    points = [(x, y) for y, row in enumerate(rows) for x, value in enumerate(row) if value != "."]
    x0 = 16 - (min(x for x, _ in points) + max(x for x, _ in points)) // 2
    y0 = 30 - max(y for _, y in points)
    legend = {format(i, "x"): name for i, name in enumerate(p.fig.pal.names) if i}
    p.fig.patch(x0, y0, rows, legend)


def kerazap(p, view, phase):
    if view in ("down", "up", "side", "icon"):
        _goat_mini(p, KERAZAP_MINI, KERAZAP_MINI_STEP, view, phase)
        return
    if view == "front":
        lift = phase
        p.limb([(31, 43), (31, 51), (29, 59)], 3.5, 2.7, z_leg, bias=0.3, group=10)
        p.limb([(43, 44), (46, 51), (44, 59)], 4, 2.7, z_leg, bias=0.3, group=11)
        _zhoof(p, 28, 59, far=True)
        _zhoof(p, 43, 59, far=True)
        p.lens((47, 40), (53, 32 - lift), 4, z_fleece, bend=-0.4, group=19)
        p.blob(40, 41, 10, 6, z_coat, group=1)
        p.limb([(28, 37), (24, 28 - lift)], 7, 5.5, z_coat, group=2)
        p.lens((19, 23 - lift), (11, 22 - lift), 3, z_coat, bias=0.2, group=20)
        _horn_bud(p, (20, 21 - lift), (20, 16 - lift), 4, bias=0.2)

        for x, y, r in ((32, 35, 5.5), (26, 34, 5), (23, 39, 4.5),
                        (28, 42, 5), (34, 41, 4.5)):
            p.circle(x, y, r, z_fleece, group=3)
        p.blob(23, 26 - lift, 5.7, 5.2, z_coat, group=12)
        p.blob(15.5, 29 - lift, 4.5, 2.7, z_coat, group=12)
        p.lens((16, 32 - lift), (16, 37 - lift), 2.7, z_fleece, group=13)
        _horn_bud(p, (24, 22 - lift), (26, 16 - lift), 3.3)
        p.lens((27, 25 - lift), (34, 23 - 2 * lift), 3.1, z_coat, bend=0.4, group=14)

        p.limb([(26, 43), (20, 48 - lift), (21, 54 - lift)], 3.8, 2.8, z_leg, group=15)
        p.limb([(46, 43), (50, 50), (48, 60)], 5.5, 3, z_leg, group=16)
        _zhoof(p, 20, 54 - lift)
        _zhoof(p, 47, 60)
        p.eye(20, 25 - lift, 3, 4, iris="iris", shine="fl3", shine_at=(1, 1))
        p.pxs([(11, 28 - lift), (11, 29 - lift)], "ink")
        p.stroke([(13, 31 - lift), (16, 31 - lift)], "lm0")
        _zig(p, [(16, 36 - lift), (17, 38 - lift), (19, 38 - lift)], "gold1")
        _zig(p, [(26, 16 - lift), (27, 13 - lift), (29, 12 - lift)], "gold1", "gold0")
        p.px(28, 12 - lift, "sky")
        return

    if view == "back":
        p.blob(25, 62, 20, 12, z_coat, group=1)
        p.lens((17, 55), (9, 45), 4.2, z_fleece, bend=0.5, group=19)
        for x, y, r in ((31, 51, 8), (39, 44, 7), (47, 50, 6),
                        (38, 57, 8), (27, 58, 6)):
            p.circle(x, y, r, z_fleece, group=3)
        p.limb([(40, 44), (43, 34)], 9, 7, z_coat, group=10)
        p.blob(44, 28, 6.7, 6, z_coat, group=12)
        p.blob(53, 31, 5, 3, z_coat, group=12)
        p.lens((54, 34), (54, 40), 3, z_fleece, group=13)
        _horn_bud(p, (40, 23), (38, 17), 3.8)
        _horn_bud(p, (46, 23), (47, 17), 3.6, bias=0.2)
        p.lens((40, 28), (32, 26), 3.6, z_coat, bend=-0.4, group=14)
        p.eye(49, 27, 3, 4, iris="iris", shine="fl3", shine_at=(1, 1))
        p.stroke([(54, 33), (57, 33)], "lm0")
        return


# --------------------------------------------------------------------------
# Kerastorm, the storm-goat: Amalthea grown, the aegis and the cornucopia
# --------------------------------------------------------------------------

KERASTORM_COLORS = [
    ("ink", INK),
    # the thundercloud fleece: marble gray with Aegean-blue shadows
    ("cl0", (40, 56, 104)), ("cl1", (96, 112, 160)), ("cl2", (160, 168, 192)), ("cl3", (216, 216, 224)),
    ("cl4", C.white),
    # limestone face, legs and the great horn, warming to bronze in the shadows
    ("lm0", (88, 48, 32)), ("lm1", (192, 128, 72)), ("lm2", (232, 192, 128)),
    # sun-gold lightning
    ("gold0", (216, 144, 32)), ("gold1", (248, 224, 96)),
    # the horn of plenty: olive grapes and figs, a terracotta pomegranate, one Fairy-pink accent
    ("ol0", (72, 96, 32)), ("ol1", (144, 168, 64)), ("terra", (152, 80, 48)), ("pink", (240, 152, 168)),
]
KERASTORM_SHINY = {
    # a sunset sun-gold thundercloud with Aegean-blue lightning
    "cl0": (128, 56, 32), "cl1": (200, 104, 48), "cl2": (232, 160, 72), "cl3": (248, 208, 128),
    "cl4": (248, 240, 208),
    "gold0": (48, 104, 176), "gold1": (152, 208, 248),
}

s_cloud = Mat(["cl0", "cl1", "cl2", "cl3", "cl4"], line="cl1", cuts=[0.3, 0.48, 0.64, 0.84])
s_coat = Mat(["lm0", "terra", "lm1", "lm2"], line="lm0", cuts=[0.24, 0.44, 0.7])
s_horn = Mat(["lm0", "lm1", "lm2"], line="lm0", cuts=[0.3, 0.6])
s_hoof = Mat(["ink", "lm0"], line="ink", cuts=[0.5])
s_grape = Mat(["ol0", "ol1"], line="ol0", cuts=[0.55])
s_pom = Mat(["lm0", "terra", "lm1"], line="lm0", cuts=[0.3, 0.8])

KERASTORM_MINI = {
    "side": (
        "..........18888891...........",
        ".........189999999891.........",
        "........18991...199891........",
        ".......18991......19891.......",
        "...18991891........1981.......",
        "..18998991..........181.......",
        "..1cdd1891..........181.......",
        ".1cddc18991.......15431........",
        "..1cd1889991.....15654431......",
        ".1dd188999991..1566655541......",
        ".1df1889619999156666655431.....",
        "..1818991b1991566665554431.....",
        "..178999999916665544444331....",
        ".1e1788999915666544bb443331...",
        ".e87117897156665544ab443331...",
        "..e1...17456655444ba4433331...",
        "........1455544444b44333331...",
        "........134444444444333331...",
        "........133333444443333331...",
        ".........1333333333333331....",
        "........1881333333333881.....",
        ".......1891.133333338881......",
        "......1891..1781..188881......",
        "......181...1781..1781881.....",
        "......171...1781...781.881....",
        "............1781...781.781....",
        "............1111..11111111...",
    ),
    "down": (
        ".................1888891....",
        "................1899999891..",
        "...............18991..19891.",
        "......18891...18991....1981.",
        ".....189981...1891......181.",
        ".....1cdd91818991.......181.",
        "....1cddc18999991......181..",
        ".....1cd188999991.....1431..",
        "....1df18999999991555654431.",
        ".....1818961199615666555431.",
        "......17891b191b16665544431.",
        ".....1e188999999155554443331",
        ".....e871881178155444b443331",
        "......e115566615444ab443331.",
        ".....1556666555444ba443331..",
        "...1556666655554444b443331...",
        "..15666665555444444433331...",
        "..15665555444444333333331...",
        "...154444433333333333331...",
        "....1333333333333333331....",
        ".....1788881....188881.....",
        ".....189981.....178881.....",
        ".....18991......178891.....",
        ".....18991......178891.....",
        ".....11111......178891.....",
        "................111111.....",
    ),
    "up": (
        "...1888891..................",
        ".1899999891.................",
        "18991..19891................",
        "1891....19891...18891.......",
        "181......1981...189981......",
        "181.......1899181cdd91......",
        ".181......1899991cddc1......",
        ".1431....189999991cd1.......",
        "154431..1899999981df1.......",
        "15654431189999998181........",
        "156655541788888881e1........",
        "15666555415566541e871.......",
        "156655554456666541e1........",
        ".1555544446666655541........",
        "..15554444465555455431......",
        "...15444444445554444331.....",
        "...1334444444b4444333331....",
        "....13333344bb4443333331....",
        "....1333334ba44333333331....",
        ".....133333b44333333331....",
        "......178881......18881....",
        "......189981......17881....",
        "......18991.......17891....",
        "......18991.......17891....",
        "......11111.......17891....",
        "..................11111....",
    ),
}
KERASTORM_MINI_STEP = {
    "side": {
        22: ".......1881.1781..188881......",
        23: "........881.1781..1781881.....",
        24: "........111.1781..1781.881....",
        25: "............1781..1781.111....",
        26: "............1111..1111........",
    },
    "down": {
        23: ".....18991......178891.....",
        24: ".....18991......111111.....",
        25: ".....11111.................",
    },
    "up": {
        23: "......18991.......17891....",
        24: "......18991.......11111....",
        25: "......11111................",
    },
}


def kerastorm(p, view, phase):
    if view in ("down", "up", "side", "icon"):
        _goat_mini(p, KERASTORM_MINI, KERASTORM_MINI_STEP, view, phase)
        return
    if view == "front":
        lift = phase
        p.limb([(35, 43), (34, 51), (32, 59)], 4.5, 3, s_coat, bias=0.3, group=10)
        p.rect(30, 59, 34, 60, s_hoof, bias=0.3)
        p.limb([(44, 44), (47, 52), (45, 59)], 5, 3, s_coat, bias=0.3, group=12)
        p.rect(43, 59, 47, 60, s_hoof, bias=0.3)
        p.blob(41, 41, 12.5, 7, s_coat, group=1)
        p.limb([(30, 40), (26, 28 - lift)], 9, 7, s_coat, group=2)
        p.circle(56, 35, 3.2, s_cloud, group=11)
        for x, y, rx, ry in ((48, 36, 8, 7), (39, 34, 9, 8),
                             (32, 29, 7, 8), (31, 40, 7, 7),
                             (43, 42, 9, 6), (51, 43, 5, 5)):
            p.blob(x, y - (lift if y < 32 else 0), rx, ry, s_cloud, group=20)

        p.blob(23, 23 - lift, 6, 5.4, s_coat, group=3)
        p.blob(15.5, 26 - lift, 4.8, 2.8, s_coat, group=3)
        p.lens((17, 29 - lift), (18, 35 - lift), 3, s_cloud, group=4)
        p.limb(bez((26, 19 - lift), (29, 7 - lift), (40, 8 - lift), n=10)
               + [(47, 12 - lift), (51, 18 - lift), (51, 24 - lift)], 7, 2.2, s_horn, group=5)
        p.limb([(21, 18 - lift), (17, 12 - lift)], 4.6, 5.2, s_horn, group=6)
        for x, y in ((13, 14), (11, 16), (14, 17), (10, 19), (12, 20)):
            p.circle(x, y - lift, 1.5, s_grape, group=7)
        p.circle(8, 25 - lift, 2.7, s_pom, group=8)
        p.drop((6.5, 16 - lift), 7.5, 21 - lift, 2, s_grape, group=9)
        p.px(7, 20 - lift, "pink")
        p.lens((29, 24 - lift), (36, 23 - 2 * lift), 3.1, s_coat, bend=0.5, group=13)

        p.limb([(29, 43), (21, 48 - lift), (22, 55 - lift)], 5, 3.1, s_coat, group=14)
        p.rect(20, 55 - lift, 24, 56 - lift, s_hoof)
        p.limb([(49, 44), (54, 51), (52, 60)], 6, 3.2, s_coat, group=15)
        p.rect(50, 60, 54, 61, s_hoof)
        p.eye(21, 22 - lift, 3, 4, shine="cl4", shine_at=(1, 1))
        p.pxs([(11, 25 - lift), (11, 26 - lift)], "ink")
        p.stroke([(13, 28 - lift), (17, 28 - lift)], "lm0")
        _zig(p, [(39, 29), (36, 33), (40, 34), (37, 39)], "gold1", "gold0")
        _zig(p, [(49, 38), (47, 41), (50, 42)], "gold1")
        return

    if view == "back":
        p.lens((15, 52), (8, 45), 4.5, s_cloud, bend=0.4, group=11)
        for x, y, rx, ry in ((19, 56, 12, 12), (30, 50, 12, 12),
                             (41, 47, 10, 10), (45, 57, 10, 12),
                             (31, 62, 14, 9)):
            p.blob(x, y, rx, ry, s_cloud, group=20)
        p.limb([(40, 45), (44, 34)], 9, 7.5, s_coat, group=2)
        p.blob(45, 28, 7, 6, s_coat, group=3)
        p.blob(54.5, 31, 5, 3, s_coat, group=3)
        p.lens((55, 34), (55, 40), 3, s_cloud, group=4)
        p.limb(bez((42, 23), (35, 9), (25, 12), n=10)
               + [(19, 18), (17, 24)], 7, 2.2, s_horn, group=5)
        p.limb([(50, 23), (53, 17)], 4.8, 5.4, s_horn, group=6)
        for x, y in ((54, 18), (57, 19), (56, 22)):
            p.circle(x, y, 1.5, s_grape, group=7)
        p.drop((58, 22), 57, 26, 2, s_grape, group=9)
        p.px(57, 25, "pink")
        p.circle(59, 30, 2.4, s_pom, group=8)
        p.eye(50, 28, 3, 4, shine="cl4", shine_at=(1, 1))
        p.stroke([(55, 34), (58, 34)], "lm0")
        _zig(p, [(30, 44), (26, 49), (31, 50), (27, 57)], "gold1", "gold0")
        _zig(p, [(42, 55), (40, 58), (43, 59)], "gold1")
        return


MONS = [
    Mon("Eripip", ERIPIP_COLORS, ERIPIP_SHINY, eripip, foot="hoof"),
    Mon("Kerazap", KERAZAP_COLORS, KERAZAP_SHINY, kerazap, foot="hoof", icon_pal=5),
    Mon("Kerastorm", KERASTORM_COLORS, KERASTORM_SHINY, kerastorm, foot="hoof", icon_pal=3),
]
