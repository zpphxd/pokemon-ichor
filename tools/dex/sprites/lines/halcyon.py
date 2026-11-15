"""Halcyon line: Halcyling, Galenyon. Alcyone and Ceyx, the kingfishers.

Ceyx drowned at sea and Alcyone leapt into the waves after him; the gods
turned both into kingfishers, and each winter Aeolus holds back the winds
for the seven days she broods her floating nest: the halcyon days (Ovid,
Metamorphoses 11). The chick rides that nest on a dead-flat sea; the adult
flies low over water so calm it is a mirror.
"""
from mon_lib import C, Mat, Mon, bez

INK = C.ink

# --------------------------------------------------------------------------
# Halcyling, the halcyon chick in its floating nest
# --------------------------------------------------------------------------

HALCYLING_COLORS = [
    ("ink", INK),
    # Aegean-blue crown and back, a kingfisher's cyan flash
    ("bl0", (24, 48, 112)), ("bl1", (40, 96, 176)), ("bl2", (72, 152, 216)), ("bl3", (152, 208, 240)),
    # terracotta-orange breast
    ("or0", (152, 64, 32)), ("or1", (216, 112, 56)), ("or2", (240, 168, 104)),
    # marble-white throat
    ("wh0", (200, 200, 200)), ("wh", C.white),
    # the dead-flat sea (it stays blue on the shiny)
    ("sea", (112, 176, 224)),
    # driftwood (limestone) and sea-wrack (olive)
    ("nst0", (112, 80, 48)), ("nst1", (184, 152, 104)),
    ("ol0", (72, 96, 32)), ("ol1", (136, 160, 64)),
]
HALCYLING_SHINY = {
    # olive-green back, sun-gold breast
    "bl0": (40, 64, 24), "bl1": (80, 112, 40), "bl2": (128, 160, 64), "bl3": (192, 216, 128),
    "or0": (168, 112, 24), "or1": (232, 176, 48), "or2": (248, 224, 120),
}

h_blue = Mat(["bl0", "bl1", "bl2", "bl3"], line="bl0", cuts=[0.2, 0.42, 0.7])
h_breast = Mat(["or0", "or1", "or2"], line="or0", cuts=[0.36, 0.64])
h_white = Mat(["wh0", "wh"], line="wh0", cuts=[0.6])
h_beak = Mat(["ink", "wh0"], line="ink", cuts=[0.12])
h_wood = Mat(["nst0", "nst1"], line="nst0", cuts=[0.5])
h_wrack = Mat(["ol0", "ol1"], line="ol0", cuts=[0.5])
h_water = Mat(["sea", "wh"], line="sea", cuts=[0.4])


def _nest(p, cx, top, w, L=0, water=True):
    """A floating nest of driftwood and sea-wrack on a dead-flat waterline."""
    p.blob(cx, top + 4, w / 2, 5, h_wood, group=40)
    # sticks across the rim, sea-wrack strands draped over it
    for i, (a, b) in enumerate((((cx - w / 2 + 1, top + 2), (cx + 3, top - 0.5)),
                                ((cx - 4, top), (cx + w / 2 - 1, top + 2.5)))):
        p.limb([a, b], 2.2, 2.0, h_wood, group=41 + i)
    for x0, x1, y1 in ((cx - w / 2 + 3, cx - w / 2 + 1, top + 8), (cx - 1, cx, top + 8.5), (cx + w / 2 - 4, cx + w / 2 - 2, top + 7.5)):
        p.limb([(x0, top + 1), (x1, y1)], 2.4, 1.6, h_wrack, group=45)
    if water:
        # the waterline: perfectly flat, wider than the nest
        p.rect(int(cx - w / 2 - 6), int(top + 7), int(cx + w / 2 + 5), int(top + 7), h_water, flat=1, nooutline=True)
        p.rect(int(cx - w / 2 - 3), int(top + 8), int(cx + w / 2 + 2), int(top + 8), h_water, flat=0, nooutline=True)


def halcyling(p, view, phase):
    if not p.big:
        _halcyling_small(p, view, phase)
        return
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        hop = view == "side" and phase == 1
        if view == "side":
            # on land the chick hops behind the player on little red feet
            p.limb([(33, 49 - 2 * hop), (32, 53 - 2 * hop)], 2.2, 2, h_breast, group=40)
            p.limb([(37, 49 - 2 * hop), (37.5, 53 - 2 * hop)], 2.2, 2, h_breast, group=40)
        # far wing stub behind, crest tuft
        p.lens((40, 33 - L), (47, 28 - 2 * L), 4, h_blue, bend=-0.6, bias=0.2, group=1)
        p.lens((36, 24 - L), (42.5, 20.5 - L), 3.6, h_blue, bend=0.6, group=2)
        p.lens((35, 26 - L), (41.5, 25 - L), 3.4, h_blue, bend=-0.4, group=2)
        # body: round, blue above, orange breast
        p.blob(34, 41 - (2 if hop else 0), 9, 8, h_blue, group=3)
        p.blob(31, 44 - (2 if hop else 0), 7, 5.6, h_breast, group=4)
        # big head
        p.blob(30, 30 - L, 7.6, 7, h_blue, group=5)
        p.blob(27.5, 36 - L, 4.4, 2.6, h_white, group=6)                      # white throat
        p.blob(30.5, 33.5 - L, 3.2, 2, h_breast, group=6)                     # orange cheek
        # the oversized dagger beak
        p.poly([(24, 30.5 - L), (10, 34.5 - L), (24, 34 - L)], h_beak, group=7)
        # near wing stub
        p.lens((35, 37), (44, 44.5), 5, h_blue, bend=-1, group=8)
        if view != "side":
            _nest(p, 34, 45, 24)
        if p.big:
            p.eye(27, 26 - L, 3, 4, shine="wh")
            p.pxs([(30, 24 - L), (33, 23 - L), (31, 21 - L)], "bl3")
        else:
            p.px(28, 28 - L, "ink")
        return

    if view == "back":
        p.blob(30, 60, 20, 10, h_wood, group=40)
        p.blob(32, 48, 14, 12, h_blue, group=3)
        p.lens((38, 45), (54, 50), 7, h_blue, bend=1, group=8)
        p.blob(40, 32, 9.5, 9, h_blue, group=5)
        p.poly([(47, 31), (62, 36), (47, 36)], h_beak, group=7)
        p.blob(46, 38, 4, 2.4, h_white, group=6)
        p.lens((33, 26), (24, 20), 4.4, h_blue, bend=0.6, group=2)
        p.eye(43, 28, 3, 4, shine="wh", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        s = phase
        p.limb([(29, 52), (29, 57 - 2 * s)], 2.4, 2.2, h_breast, group=40)
        p.limb([(35, 52), (35, 57 - 2 * (1 - s))], 2.4, 2.2, h_breast, group=40)
        p.lens((24, 42), (19, 49 - s), 4.4, h_blue, group=1)
        p.lens((40, 42), (45, 49 - (1 - s)), 4.4, h_blue, group=1)
        p.blob(32, 45, 8.4, 8, h_blue if view == "up" else h_breast, group=3)
        p.lens((32, 26), (32, 19), 4, h_blue, group=2)
        p.blob(32, 32, 8, 7.4, h_blue, group=5)
        if view == "down":
            p.blob(32, 39, 4.4, 2.6, h_white, group=6)
            p.poly([(30.5, 34), (32, 44), (33.5, 34)], h_beak, group=7)
            p.eye(26, 30, 3, 4, shine="wh")
            p.eye(36, 30, 3, 4, shine="wh")
        return


def _halcyling_small(p, view, phase):
    """Native miniatures: the follower walks on feet, never in its nest."""
    if view == "up":
        rows = [
            ".........22.....",
            ".......2542.....",
            ".....254442.....",
            "....25544432....",
            "...2554443332...",
            "...2544433332...",
            "....24433332....",
            "...2444433332...",
            "..254443333332..",
            ".25444333333332.",
            "..244333333332..",
            "...2333333332...",
            "....23333332....",
            ".....222222.....",
            ".....6....6.....",
            "....666..666....",
        ]
    elif view == "down":
        rows = [
            "........22......",
            "......2542......",
            "....2554432.....",
            "...255444332....",
            "...241443132....",
            "...21a141a132...",
            "...2114411132...",
            "....2aa1aa32....",
            "...2889198732...",
            "..248881887432..",
            "..248876887432..",
            "...2877777632...",
            "....27777632....",
            ".....266662.....",
            ".....6....6.....",
            "....666..666....",
        ]
    else:
        rows = [
            "..........22....",
            "........2542....",
            "......2554432...",
            ".....255444332..",
            ".....21a144332..",
            ".....211144332..",
            "..229222443332..",
            "22222.2aa873332..",
            "......aa8876332.",
            ".....28888764432",
            ".....28887765432",
            "......2777634332",
            ".......26663332.",
            "........222222..",
            "........6...6...",
            ".......666.666..",
        ]
    rows = list(rows)
    if phase:
        rows[-2:] = [".....6....66....", "....666........."] if view in ("down", "up") else [
            "........66......", "...........666.."]
    x = (p.W - max(map(len, rows))) // 2
    y = p.H - len(rows) - 1 - (phase if view == "icon" else 0)
    legend = {format(i, "x"): name for i, name in enumerate(p.fig.pal.names) if i}
    p.fig.patch(x, y, rows, legend)


# --------------------------------------------------------------------------
# Galenyon, the halcyon: Alcyone over the calm sea
# --------------------------------------------------------------------------

GALENYON_COLORS = [
    ("ink", INK),
    # Aegean blue from deep to pale
    ("bl0", (16, 40, 96)), ("bl1", (32, 80, 160)), ("bl2", (56, 128, 208)), ("bl3", (104, 184, 232)),
    ("bl4", (184, 232, 248)),
    # terracotta-orange breast
    ("or0", (144, 56, 32)), ("or1", (208, 104, 48)), ("or2", (240, 160, 96)),
    # marble-white throat
    ("wh0", (200, 200, 208)), ("wh", C.white),
    # sun-gold eye ring
    ("gold", C.sungold[1]),
    # the spear beak
    ("beak", (64, 64, 80)), ("beak2", (128, 128, 144)),
    # the glassy sea below (it stays blue on the shiny)
    ("sea", (112, 176, 224)),
]
GALENYON_SHINY = {
    "bl0": (32, 56, 24), "bl1": (64, 104, 40), "bl2": (104, 152, 56), "bl3": (160, 200, 96),
    "bl4": (216, 240, 168),
    "or0": (168, 104, 24), "or1": (232, 168, 40), "or2": (248, 216, 112),
}

g_blue = Mat(["bl0", "bl1", "bl2", "bl3", "bl4"], outline="bl0", line="bl1",
             cuts=[0.14, 0.34, 0.58, 0.82])
g_breast = Mat(["or0", "or1", "or2"], line="or0", cuts=[0.36, 0.64])
g_white = Mat(["wh0", "wh"], line="wh0", cuts=[0.6])
g_beak = Mat(["beak", "beak2"], line="ink", cuts=[0.55])
g_water = Mat(["sea", "wh0", "wh"], line="sea", cuts=[0.3, 0.6])


def galenyon(p, view, phase):
    if not p.big:
        _galenyon_small(p, view, phase)
        return
    if view in ("front", "side", "icon"):
        up = phase == 1
        fw = 3 if up else 0
        p.poly([(29, 27), (24, 21), (16, 15 - fw), (7, 12 - fw),
                (9, 16 - fw), (14, 19), (10, 18), (13, 22), (19, 24),
                (15, 24), (20, 27), (27, 30)], g_blue, bias=0.2, group=1, noline=True)
        for a, b, w in (((40, 34), (53, 23), 4.5),
                        ((42, 35), (56, 29), 4), ((43, 36), (54, 35), 3)):
            p.lens(a, b, w, g_blue, bias=0.12, group=2, noline=True)
        p.blob(34, 34, 11, 5.5, g_blue, ang=-18, group=3, noline=True)
        p.blob(30, 37, 7.5, 3.5, g_breast, ang=-16, group=4, noline=True)
        p.lens((25, 25), (34, 20), 3.5, g_blue, bend=0.8, group=5, noline=True)
        p.lens((26, 26), (34, 25), 2.5, g_blue, group=5, noline=True)
        p.blob(23, 28, 5.5, 5, g_blue, group=6, noline=True)
        p.blob(22, 32, 3.3, 1.8, g_white, group=7, noline=True)
        p.poly([(18, 27), (5, 31), (18, 30)], g_beak, group=8, noline=True)
        p.poly([(31, 31), (36, 32), (43, 37 + fw), (51, 42 + fw),
                (57, 46 + fw), (53, 47 + fw), (48, 44 + fw), (50, 48 + fw),
                (46, 47 + fw), (42, 43), (44, 48), (40, 45), (37, 39),
                (35, 43), (32, 39), (29, 35)], g_blue, group=9, noline=True)
        if view != "side":
            p.rect(17, 54, 47, 54, g_water, flat=2, nooutline=True)
            p.rect(22, 55, 43, 55, g_water, flat=0, nooutline=True)
            p.rect(28, 55, 35, 55, g_breast, flat=1, nooutline=True)
        p.patch(20, 25, ["ccc", "c1c", "b1c", "cc."],
                {"c": "gold", "1": "ink", "b": "wh"})
        p.stroke([(7, 31), (17, 30)], "beak")
        p.stroke([(14, 17 - fw), (24, 25)], "bl3")
        p.stroke([(36, 35), (45, 42 + fw)], "bl4")
        p.stroke([(35, 37), (39, 42)], "bl1")
        p.stroke([(41, 38 + fw), (49, 44 + fw)], "bl3")
        p.pxs([(27, 34), (28, 34), (30, 36)], "or2")
        return

    if view == "back":
        p.poly([(31, 43), (21, 33), (11, 24), (4, 20), (6, 25),
                (12, 31), (8, 29), (11, 34), (17, 38), (14, 37),
                (18, 42), (27, 48)], g_blue, group=1, bias=0.2, noline=True)
        p.poly([(34, 45), (40, 40), (47, 35), (54, 29), (60, 25),
                (57, 32), (52, 38), (55, 36), (51, 42), (46, 44),
                (48, 44), (43, 48), (35, 51)], g_blue, group=2, noline=True)
        p.blob(30, 60, 11.5, 16, g_blue, group=3, noline=True)
        p.limb([(32, 47), (35, 41), (37, 37)], 10, 8, g_blue, group=3, noline=True)
        p.lens((34, 28), (26, 21), 3.5, g_blue, group=6, noline=True)
        p.blob(37, 33, 6.5, 6, g_blue, group=6, noline=True)
        p.blob(41, 38, 3, 1.5, g_white, group=7, noline=True)
        p.poly([(43, 32), (58, 37), (43, 36)], g_beak, group=8, noline=True)
        p.patch(39, 30, ["ccc", "c1c", "c1b", ".cc"],
                {"c": "gold", "1": "ink", "b": "wh"})
        p.stroke([(10, 29), (26, 43)], "bl4")
        p.stroke([(39, 45), (53, 34)], "bl4")
        p.stroke([(24, 50), (28, 59)], "bl3")
        p.stroke([(36, 49), (34, 61)], "bl1")
        p.stroke([(44, 36), (55, 37)], "beak")
        return

    if view in ("down", "up"):
        s = phase
        p.poly([(28, 34), (10, 30 - 4 * s), (4, 36 - 4 * s), (26, 42)], g_blue, group=1)
        p.poly([(36, 34), (54, 30 - 4 * s), (60, 36 - 4 * s), (38, 42)], g_blue, group=1)
        p.blob(32, 40, 7.4, 9, g_breast if view == "down" else g_blue, group=3)
        p.blob(32, 28, 6.6, 6, g_blue, group=6)
        if view == "down":
            p.blob(32, 34, 3.6, 2.4, g_white, group=7)
            p.poly([(30.5, 30), (32, 42), (33.5, 30)], g_beak, group=8)
            p.eye(27, 26, 2, 3, shine="wh")
            p.eye(35, 26, 2, 3, shine="wh")
        return


def _galenyon_small(p, view, phase):
    if view == "up":
        rows = [
            "..........22............",
            "..........2452..........",
            ".........2544432........",
            ".........2544432........",
            ".........2444332........",
            "..22......24332.....22..",
            ".24522....24432...22542.",
            "..24554222544332255442..",
            "...244554455443554432...",
            "....2244565444564322....",
            ".......2244433322.......",
            ".........243332.........",
            ".........233332.........",
            "..........2332..........",
            "...........22...........",
        ]
    elif view == "down":
        rows = [
            ".............22.........",
            "...........2542.........",
            ".........2554432........",
            ".........2c14c32........",
            ".........2b11b32........",
            "..........ab1ba.........",
            "..22.....299d9932...22..",
            ".24522..2499d9943225542.",
            "..24554224998994455442..",
            "...244554988879544432...",
            "....2244548887454322....",
            ".......2248873322.......",
            ".........277772.........",
            "..........2772..........",
            "...........22...........",
        ]
    else:
        rows = [
            "...22...................",
            "...24522................",
            "....2455422.....22......",
            ".....2445542..2542......",
            "......2245542254432.....",
            ".........22555c1332.....",
            "...........244b1332.....",
            "......ddeee22243332...22",
            "...ddddd2222.bb9883225442",
            ".............b9987544432",
            "..............287654432.",
            "...............2454432..",
            "................2444332.",
            ".................2332332",
            "..................22.22.",
        ]
    rows = list(rows)
    if phase:
        if view in ("down", "up"):
            rows[4] = ".22" + rows[4][3:21] + "22."
            rows[5] = "2542" + rows[5][4:20] + "2452"
            rows[6] = ".25422" + rows[6][6:18] + "22452."
            rows[7] = "..245542" + rows[7][8:16] + "2455442."
            rows[8] = "...22442" + rows[8][8:16] + "24422..."
            rows[9] = ".....222" + rows[9][8:16] + "222....."
            rows[10] = "........" + rows[10][8:16] + "........"
        else:
            rows[9:] = [
                ".............b9987545542",
                "..............2876555442",
                "...............24444432.",
                "................233332..",
                ".................2332232",
                "..................22.22.",
            ]
    legend = {format(i, "x"): name for i, name in enumerate(p.fig.pal.names) if i}
    p.fig.patch((p.W - max(map(len, rows))) // 2, p.H - len(rows) - 1, rows, legend)


MONS = [
    Mon("Halcyling", HALCYLING_COLORS, HALCYLING_SHINY, halcyling, foot="bird", icon_pal=3),
    Mon("Galenyon", GALENYON_COLORS, GALENYON_SHINY, galenyon, foot="bird", icon_pal=3),
]
