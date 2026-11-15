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

g_blue = Mat(["bl0", "bl1", "bl2", "bl3"], line="bl0", cuts=[0.2, 0.42, 0.7])
g_breast = Mat(["or0", "or1", "or2"], line="or0", cuts=[0.36, 0.64])
g_white = Mat(["wh0", "wh"], line="wh0", cuts=[0.6])
g_beak = Mat(["beak", "beak2"], line="ink", cuts=[0.55])
g_water = Mat(["sea", "wh0", "wh"], line="sea", cuts=[0.3, 0.6])


def galenyon(p, view, phase):
    if view in ("front", "side", "icon"):
        up = phase == 1
        # far wing, raised behind the head (the upstroke in frame 2)
        fw = 3 if up else 0
        p.poly([(30, 22), (20, 12 - fw), (10, 8 - 2 * fw), (4, 10 - 2 * fw), (12, 16 - fw), (22, 24)],
               g_blue, bias=0.2, group=1)
        # fanned tail
        for a, b in (((44, 30), (56, 22)), ((44, 31), (58, 27)), ((44, 32), (57, 32))):
            p.lens(a, b, 4, g_blue, bias=0.1, group=2)
        # body: sleek, orange breast
        p.blob(34, 31, 11, 6.4, g_blue, ang=-12, group=3)
        p.blob(32, 34, 9, 4, g_breast, ang=-12, group=4)
        # head, crest swept back
        p.lens((22, 20), (34, 15), 4.4, g_blue, bend=0.8, group=5)
        p.lens((24, 22), (35, 20), 3.6, g_blue, bend=0.4, group=5)
        p.blob(22, 24, 6.6, 6, g_blue, group=6)
        p.blob(20, 28.5, 3.8, 2.2, g_white, group=7)
        # the spear beak
        p.poly([(16.5, 23), (2, 29), (16.5, 27)], g_beak, group=8)
        # near wing: a wide downstroke over the water
        p.poly([(30, 29), (42, 33 + fw), (52, 38 + fw), (60, 44 + fw), (54, 45 + fw), (42, 41), (32, 36)],
               g_blue, group=9)
        # the calm water, reflecting the breast
        if view != "side":
            p.rect(14, 53, 50, 53, g_water, flat=2, nooutline=True)
            p.rect(18, 54, 46, 55, g_water, flat=1, nooutline=True)
            p.rect(26, 54, 36, 55, g_breast, flat=1, nooutline=True)
        if p.big:
            p.eye(20, 21, 3, 4, shine="wh")
            p.px(23, 23, "gold")
        else:
            p.px(21, 23, "ink")
        return

    if view == "back":
        p.poly([(30, 40), (12, 26), (2, 22), (4, 30), (18, 44)], g_blue, group=1)
        p.poly([(34, 40), (52, 26), (62, 22), (60, 30), (46, 44)], g_blue, group=1)
        p.blob(32, 56, 12, 14, g_blue, group=3)
        p.blob(34, 30, 8, 7.4, g_blue, group=6)
        p.poly([(41, 29), (61, 34), (41, 33)], g_beak, group=8)
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


MONS = [
    Mon("Halcyling", HALCYLING_COLORS, HALCYLING_SHINY, halcyling, foot="bird", icon_pal=3),
    Mon("Galenyon", GALENYON_COLORS, GALENYON_SHINY, galenyon, foot="bird", icon_pal=3),
]
