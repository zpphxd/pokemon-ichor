"""Weasel line: Galekit, Gelasable (Normal). Galanthis, the servant who
laughed, and Hecate's weasel."""
from mon_lib import C, Mat, Mon, bez

INK = C.ink


# --------------------------------------------------------------------------
# Galekit, the weasel kit
# --------------------------------------------------------------------------

GALEKIT_COLORS = [
    ("ink", INK),
    ("tn0", (120, 80, 48)), ("tn1", (168, 128, 80)), ("tn2", (208, 168, 112)), ("tn3", (232, 208, 160)),
    ("w0", (208, 200, 184)), ("w1", (248, 248, 240)),
    ("mk0", (72, 32, 24)), ("mk1", (112, 56, 40)), ("mk2", (160, 88, 56)),
    ("ol0", (48, 64, 24)), ("ol1", (96, 120, 48)), ("ol2", (160, 176, 80)),
    ("pink", (216, 128, 128)),
]
GALEKIT_SHINY = {
    "tn0": (128, 128, 136), "tn1": (176, 176, 184), "tn2": (216, 216, 216), "tn3": (240, 240, 240),
    "mk0": (144, 96, 16), "mk1": (208, 152, 40), "mk2": (248, 200, 72),
}

g_tn = Mat(["tn0", "tn1", "tn2", "tn3"], line="tn0", cuts=[0.16, 0.42, 0.7])
g_white = Mat(["w0", "w1"], line="tn1", cuts=[0.52])
g_mask = Mat(["mk0", "mk1", "mk2"], line="mk0", cuts=[0.3, 0.62])
g_olive = Mat(["ol0", "ol1", "ol2"], line="ol0", cuts=[0.34, 0.66])


def galekit(p, view, phase):
    """Battle sprites are hand-finished (art/galekit_*.txt); this draft
    matches them for the icon and the follower."""
    if view in ("front", "side", "icon"):
        F = 1 if (phase == 1 and view != "side") else 0     # head bob and tail flick
        W = view == "side" and phase == 1
        # bushy tail plume, raised, its tip in the mask color
        tail = p.lens((42, 48), (51.5 + F, 34 - F), 8.4, g_tn, bend=-2.2, fat=0.55)
        p.lens((48.5, 40 - F), (51.5 + F, 34 - F), 6, g_mask, clip=[tail], group=tail)
        if W:
            far_f, far_h = [(24, 52), (23, 59)], [(40, 52), (41, 59)]
            near_f, near_h = [(21.5, 52), (20, 59)], [(38.5, 51), (42, 59)]
        else:
            far_f, far_h = [(25, 52), (20.5, 59)], [(40, 51), (46.5, 58.5)]
            near_f, near_h = [(22.5, 52), (16.5, 58.5)], [(38.5, 50), (44, 58.5)]
        p.limb(far_f, 3.4, 2.8, g_tn, bias=0.35, group=10)
        p.limb(far_h, 4.0, 2.8, g_tn, bias=0.35, group=11)
        body = p.limb(bez((24, 50), (33, 44.5), (42, 48.5)), 11, 9.6, g_tn, group=1)
        p.limb(bez((22, 53.5), (31, 53), (39, 54)), 3.6, 3, g_white, clip=[body], group=2)
        p.limb(near_f, 3.8, 3.0, g_tn, group=12)
        p.limb(near_h, 4.8, 3.0, g_tn, group=13)
        # big round kit head with round ears
        p.circle(24, 36.5 + F, 2.8, g_tn, bias=0.2, group=5)
        head = p.blob(18.5, 42 + F, 7.8, 7.4, g_tn, group=3)
        p.blob(11, 45 + F, 4.4, 2.8, g_white, group=3)
        p.blob(15, 47.5 + F, 5.4, 2.6, g_white, clip=[head], group=4)
        # the mask: a band across the eyes, turned up at the cheek into a grin
        p.limb(bez((10, 43 + F), (16, 38 + F), (24, 41 + F)), 4.4, 3.4, g_mask, clip=[head], group=6)
        p.circle(14, 36.5 + F, 2.9, g_tn, group=7)
        # the stolen olive
        p.blob(7.5, 48.5 + F, 2.8, 2.2, g_olive, group=8)
        if p.big:
            p.eye(16, 40 + F, 3, 5, shine="w1", shine_at=(1, 1))
            p.pxs([(7, 44 + F), (8, 44 + F)], "ink")
            p.stroke([(10, 47 + F), (13, 48 + F), (16, 47 + F)], "mk0")
            p.px(13, 36 + F, "pink")
        else:
            p.pxs([(15, 42 + F), (16, 42 + F)], "w1")
        return

    if view == "back":
        tail = p.lens((15, 58), (7, 37), 10, g_tn, bend=2.2, group=9)
        p.lens((9, 44), (7, 37), 7, g_mask, clip=[tail], group=9)
        p.blob(26, 64, 21, 15, g_tn, group=1)
        p.limb(bez((32, 54), (38, 47), (42, 40)), 14, 12, g_tn, group=1)
        p.circle(38, 28, 3.8, g_tn, group=5)
        p.circle(49, 29, 3.4, g_tn, group=6)
        head = p.blob(44, 35, 9, 8, g_tn, group=3)
        p.blob(52, 39, 5, 3.4, g_white, group=3)
        p.limb(bez((38, 33), (46, 31), (54, 37)), 4.4, 3, g_mask, clip=[head], group=7)
        p.eye(47, 32, 3, 5, shine="w1")
        p.px(56, 37, "ink")
        p.blob(56, 42, 2.8, 2.2, g_olive, group=8)
        if p.big:
            p.px(49, 28, "pink")
            p.stroke([(52, 41), (50, 42), (48, 41)], "mk0")
            p.stroke([(23, 50), (29, 52), (33, 55)], "tn3")
            p.stroke([(36, 48), (33, 53), (34, 57)], "tn0")
        return

    if view == "down":
        # follower trotting toward us: masked face, the olive in its mouth
        s = phase
        p.lens((38, 50), (43 + s, 37), 6, g_tn, bend=-1.2)
        p.lens((41.5 + s, 40.5), (43 + s, 37), 5, g_mask)
        p.limb([(28, 52), (27.5, 60 - 2 * s)], 3.8, 3.2, g_tn, group=12)
        p.limb([(36, 52), (36.5, 60 - 2 * (1 - s))], 3.8, 3.2, g_tn, group=13)
        body = p.blob(32, 50, 8, 6.6, g_tn, group=1)
        p.blob(32, 51, 4.4, 5.4, g_white, clip=[body], group=2)
        p.circle(24.5, 34, 3.2, g_tn, group=5)
        p.circle(39.5, 34, 3.2, g_tn, group=6)
        head = p.blob(32, 40, 9, 7.4, g_tn, group=3)
        p.blob(32, 44.5, 5, 3, g_white, clip=[head], group=4)
        p.poly([(22.5, 39), (27, 37), (32, 38), (37, 37), (41.5, 39), (40.5, 41.5), (36, 42), (32, 41.5),
                (28, 42), (23.5, 41.5)], g_mask, clip=[head], group=7)
        p.blob(32, 47.5, 3, 2.2, g_olive, group=8)
        p.eye(27, 38, 2, 3, shine="w1")
        p.eye(35, 38, 2, 3, shine="w1")
        p.pxs([(31, 43), (32, 43)], "ink")
        return

    if view == "up":
        # follower trotting away: the tail up, ears, the back
        s = phase
        p.limb([(28, 52), (27.5, 60 - 2 * s)], 3.8, 3.2, g_tn, group=12)
        p.limb([(36, 52), (36.5, 60 - 2 * (1 - s))], 3.8, 3.2, g_tn, group=13)
        p.blob(32, 49, 8.4, 7, g_tn, group=1)
        p.circle(24.5, 34, 3.2, g_tn, group=5)
        p.circle(39.5, 34, 3.2, g_tn, group=6)
        p.blob(32, 40, 8.6, 7, g_tn, group=3)
        tail = p.lens((32, 52), (33 + 2 * s, 37), 7, g_tn, bend=-1.2)
        p.lens((32.5 + 2 * s, 41), (33 + 2 * s, 37), 6, g_mask, clip=[tail], group=tail)
        return


# --------------------------------------------------------------------------
# Gelasable, Hecate's laughing weasel
# --------------------------------------------------------------------------

GELASABLE_COLORS = [
    ("ink", INK),
    ("tn0", (120, 80, 48)), ("tn1", (168, 128, 80)), ("tn2", (208, 168, 112)), ("tn3", (232, 208, 160)),
    ("w0", (208, 200, 184)), ("w1", (248, 248, 240)),
    ("cd0", (40, 32, 56)), ("cd1", (72, 64, 96)), ("cd2", (112, 104, 136)),
    ("g0", (200, 128, 32)), ("g1", (248, 200, 72)), ("flame", (248, 240, 176)),
    ("m0", (136, 40, 56)), ("m1", (216, 96, 104)),
]
GELASABLE_SHINY = {
    "tn0": (128, 128, 136), "tn1": (176, 176, 184), "tn2": (216, 216, 216), "tn3": (240, 240, 240),
    "cd0": (24, 48, 112), "cd1": (48, 96, 168), "cd2": (104, 160, 216),
}
GELASABLE_FOOTPRINT = [
    "................",
    "................",
    "................",
    ".....#...#......",
    "....##...##.....",
    "..#.........#...",
    "..##.......##...",
    "......###.......",
    ".....#####......",
    "....#######.....",
    "....#######.....",
    ".....#####......",
    "................",
    "................",
    "................",
    "................",
]

s_tn = Mat(["tn0", "tn1", "tn2", "tn3"], line="tn0", cuts=[0.16, 0.42, 0.7])
s_white = Mat(["w0", "w1"], line="tn1", cuts=[0.52])
s_dark = Mat(["cd0", "cd1", "cd2"], line="cd0", cuts=[0.34, 0.66])
s_mouth = Mat(["m0", "m1"], line="m0", cuts=[0.5])

GELASABLE_MINI = {
    "side": [
        "..................8998",
        ".................8a99.",
        "..................8942",
        "...25............23442",
        "..25542...........2442",
        "..551144..........2442",
        ".16771143.........2442",
        ".766efe632.......23442",
        "..266f6632..25554444432",
        "...2666332255444433332",
        "....8ac988544333333322",
        "...cd8cdb8443332222232",
        "....cb8cb8343322222222",
        ".....6624443322...2332",
        ".....2443332.......232",
        "....24432232.......232",
        "...24432..232.....23432",
        "..24432...232.....24432",
        ".23222.....22......222.",
    ],
    "down": [
        ".............8998...",
        "..............a98...",
        ".......22....2442...",
        "......2552...2442...",
        ".....2555442.2442...",
        "....2515544322442...",
        "....571..17432332...",
        "....6761e76623332...",
        ".....66efe6623322...",
        "......2666623332....",
        ".....88ac9ac9882....",
        ".....cd8cd8cd832....",
        "......b8b8b844332...",
        "......7644444332...",
        "......6444333322...",
        "......244333322.....",
        ".....24432.2332.....",
        ".....2332...2332....",
        ".....222.....222....",
    ],
    "up": [
        ".............8998...",
        "..............a98...",
        ".......22....2442...",
        "......2552...2442...",
        ".....2555442.2442...",
        "....2555544322442...",
        "....5554443323332...",
        "....5544443323332...",
        ".....443333223332...",
        "......2333223332....",
        ".....88ac9ac9882....",
        ".....cd8cd8cd832....",
        "......b8b8b844332...",
        "......5544444332...",
        "......5444333322...",
        "......244333322.....",
        ".....24432.2332.....",
        ".....2332...2332....",
        ".....222.....222....",
    ],
}
GELASABLE_MINI_STEP = {
    "side": {
        0: ".................8998.",
        1: "................8a99..",
        2: ".................89442",
        14: ".....2443332......2332.",
        15: ".....24332232.....232..",
        16: "......24332232...2342..",
        17: ".......2443232...2432..",
        18: ".......222.22....222...",
    },
    "down": {
        0: "............8998....",
        1: ".............a98....",
        2: ".......22...24442...",
        7: "....676ee76623332...",
        8: ".....66eff6623322...",
        16: "......2432.24432....",
        17: "......232...2332....",
        18: "......22....222.....",
    },
    "up": {
        0: "............8998....",
        1: ".............a98....",
        2: ".......22...24442...",
        16: "......2432.24432....",
        17: "......232...2332....",
        18: "......22....222.....",
    },
}


def _gelasable_mini(p, view, phase):
    direction = "side" if view == "icon" else view
    rows = list(GELASABLE_MINI[direction])
    if phase:
        for y, row in GELASABLE_MINI_STEP[direction].items():
            rows[y] = row
    if view == "icon":
        rows[5] = "..551154..........2442"
        rows[6] = ".167711143........2442"
        rows[7] = ".766eff632.......23442" if phase else ".766efe632.......23442"
    points = [(x, y) for y, row in enumerate(rows) for x, value in enumerate(row) if value != "."]
    x0 = 16 - (min(x for x, _ in points) + max(x for x, _ in points)) // 2
    y0 = 30 - max(y for _, y in points)
    legend = {format(i, "x"): name for i, name in enumerate(p.fig.pal.names) if i}
    p.fig.patch(x0, y0, rows, legend)


def _torch(p, x, y):
    """A torch spot on the collar: a gold flame with a pale heart."""
    if p.big:
        p.pxs([(x, y), (x + 1, y), (x, y - 1), (x + 1, y - 1)], "g1")
        p.px(x, y - 2, "g1")
        p.px(x + 1, y + 1, "g0")
        p.px(x, y + 1, "g0")
        p.px(x, y - 1, "flame")
    else:
        p.px(x, y, "g1")


def gelasable(p, view, phase):
    """Low, long-bodied laughing mustelid; matched native battle and field poses."""
    if not p.big and view in ("icon", "down", "up", "side"):
        _gelasable_mini(p, view, phase)
        return
    if view in ("front", "side", "icon"):
        laugh = phase if view != "side" else 0
        walk = phase if view == "side" else 0
        head = 5 - laugh
        p.limb(bez((43, 49), (60, 43), (54, 25 - laugh)), 6, 4.2, s_tn, group=20)
        p.limb(bez((54, 26 - laugh), (55, 18 - laugh), (46 - laugh, 20)),
               4.6, 3.2, s_dark, group=20)
        if walk:
            far_f, far_h = [(23, 49), (26, 58)], [(45, 49), (42, 59)]
            near_f, near_h = [(20, 48), (17, 59)], [(43, 50), (50, 59)]
        else:
            far_f, far_h = [(24, 49), (23, 58)], [(44, 49), (45, 59)]
            near_f, near_h = [(21, 48), (17, 55), (11, 59)], [(44, 49), (49, 56), (53, 59)]
        p.limb(far_f, 3.6, 2.6, s_tn, bias=0.45, group=10)
        p.limb(far_h, 4.2, 2.8, s_tn, bias=0.45, group=11)
        body = p.limb(bez((22, 47), (32, 49), (44, 48)), 11, 12, s_tn, group=1)
        p.blob(43, 49, 7.2, 6, s_tn, group=1)
        neck = p.limb(bez((23, 45), (26, 40), (24, 28 + head)), 10, 8.5, s_tn, group=1)
        p.limb(bez((20, 32 + head), (20, 47), (35, 53)), 4.8, 3.2, s_white,
               clip=[body, neck], group=2)
        p.limb(near_f, 4.2, 3, s_tn, group=12)
        p.limb(near_h, 4.8, 3, s_tn, group=13)
        p.limb(bez((18, 38 - laugh), (24, 41 - laugh), (30, 38 - laugh)),
               5.8, 4.6, s_dark, clip=[neck], group=8)
        p.circle(29, 19 + head, 2.2, s_tn, bias=0.4, group=5)
        p.circle(19, 17 + head, 2.5, s_tn, group=6)
        p.blob(23, 23 + head, 7.8, 6.3, s_tn, ang=-0.12, group=3)
        p.poly([(13, 24 + head), (20, 24 + head), (26, 27 + head),
                (22, 32 + head), (17, 31 + head), (12, 27 + head)], s_white, group=4)
        p.poly([(16, 26 + head), (23, 27 + head), (20, 31 + head)],
               s_mouth, group=9)
        if p.big:
            p.patch(16, 21 + head, [
                "211....21",
                ".71....7.",
                ".........",
                ".........",
                ".77......",
                "..7e17...",
                "...ef1...",
                "....f....",
            ])
            p.pxs([(12, 25 + head), (13, 25 + head)], "ink")
        else:
            p.pxs([(18, 22 + head), (25, 23 + head)], "ink")
            p.px(18, 23 + head, "w1")
            p.px(13, 25 + head, "ink")
        for x, y in ((19, 39), (24, 41), (29, 39)):
            _torch(p, x, y - laugh)
        return

    if view == "back":
        p.limb(bez((21, 63), (3, 42), (10, 28)), 9, 5.5, s_tn, group=20)
        p.limb(bez((10, 28), (12, 19), (22, 22)), 5.8, 3.8, s_dark, group=20)
        body = p.limb(bez((25, 68), (30, 51), (43, 41)), 29, 18, s_tn, group=1)
        neck = p.limb(bez((43, 46), (46, 39), (44, 32)), 15, 12, s_tn, group=1)
        p.limb(bez((49, 35), (49, 47), (42, 54)), 5, 3.8, s_white,
               clip=[body, neck], group=2)
        p.limb(bez((37, 42), (44, 45), (51, 40)), 7, 5, s_dark, clip=[neck], group=8)
        p.circle(38, 25, 3, s_tn, group=5)
        p.circle(47, 26, 2.4, s_tn, bias=0.4, group=6)
        p.blob(43, 31, 9, 7, s_tn, group=3)
        p.poly([(48, 31), (55, 33), (54, 36), (48, 39), (45, 35)], s_white, group=4)
        p.poly([(49, 35), (53, 35), (50, 39)], s_mouth, group=9)
        p.eye(47, 29, 3, 2, shine="w1", shine_at=(1, 1))
        p.pxs([(54, 32), (55, 32)], "ink")
        p.px(49, 35, "w1")
        for x, y in ((38, 42), (44, 44), (50, 41)):
            _torch(p, x, y)
        return

    if view in ("down", "up"):
        s = phase
        p.limb([(27, 51), (25 + 2 * s, 60 - 2 * s)], 3.6, 2.8, s_tn, group=12)
        p.limb([(37, 51), (39 - 2 * s, 58 + 2 * s)], 3.6, 2.8, s_tn, group=13)
        p.limb(bez((36, 51), (48 - s, 47), (43 - s, 31)), 5.4, 3.6, s_tn, group=20)
        p.limb(bez((43 - s, 32), (45 - s, 27), (39 - s, 28)), 3.8, 2.8, s_dark, group=20)
        body = p.blob(32, 48, 8.8, 7.2, s_tn, group=1)
        if view == "down":
            p.blob(32, 49, 4.5, 5, s_white, clip=[body], group=2)
        p.limb([(26, 43), (32, 45), (38, 43)], 5, 4, s_dark, group=8)
        p.circle(26, 33 - s, 2.4, s_tn, group=5)
        p.circle(37, 34 - s, 2, s_tn, group=6)
        p.blob(32, 38 - s, 7.3, 5.8, s_tn, group=3)
        if view == "down":
            p.blob(31, 41 - s, 4.8, 3.2, s_white, group=4)
            p.poly([(28, 41 - s), (34, 41 - s), (31, 45 - s)], s_mouth, group=9)
            p.pxs([(27, 36 - s), (28, 36 - s), (34, 37 - s)], "ink")
            p.px(28, 37 - s, "w1")
            p.pxs([(30, 39 - s), (31, 39 - s)], "ink")
        for x, y in ((27, 44), (32, 46), (37, 44)):
            _torch(p, x, y)
        return


MONS = [
    Mon("Galekit", GALEKIT_COLORS, GALEKIT_SHINY, galekit, foot="paw", icon_pal=5),
    Mon("Gelasable", GELASABLE_COLORS, GELASABLE_SHINY, gelasable, foot=GELASABLE_FOOTPRINT, icon_pal=5),
]
