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
        tail = p.lens((42, 48), (51.5, 36 - F), 7.4, g_tn, bend=-2.2, fat=0.55)
        p.lens((48.5, 40 - F), (51.5, 36 - F), 6, g_mask, clip=[tail], group=tail)
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
        head = p.blob(17.5, 41.5 + F, 8, 7, g_tn, group=3)
        p.blob(10.5, 45 + F, 4.6, 2.8, g_tn, group=3)
        p.blob(13, 47.5 + F, 6.4, 2.6, g_white, clip=[head], group=4)
        # the mask: a band across the eyes, turned up at the cheek into a grin
        p.poly([(5.5, 43 + F), (11, 40.5 + F), (17, 39.6 + F), (23, 40.4 + F), (25.5, 38.8 + F), (26, 41 + F),
                (21, 45 + F), (14, 46 + F), (8, 45.5 + F)], g_mask, clip=[head], group=6)
        p.circle(14, 36.5 + F, 2.9, g_tn, group=7)
        # the stolen olive
        p.blob(4.5, 48.5 + F, 2.8, 2.2, g_olive, group=8)
        if p.big:
            p.eye(14, 41 + F, 3, 4, shine="w1", shine_at=(1, 1))
            p.pxs([(3, 44 + F), (4, 44 + F)], "ink")
            p.stroke([(8, 47 + F), (15, 47 + F), (17, 46 + F)], "mk0")
            p.px(13, 36 + F, "pink")
        else:
            p.pxs([(15, 42 + F), (16, 42 + F)], "w1")
        return

    if view == "back":
        # the hand-finished art replaces this
        p.limb(bez((10, 66), (26, 50), (40, 40)), 22, 14, g_tn, group=1)
        p.blob(44, 30, 8, 7, g_tn, group=3)
        p.blob(56, 34, 2.8, 2.2, g_olive, group=7)
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

s_tn = Mat(["tn0", "tn1", "tn2", "tn3"], line="tn0", cuts=[0.16, 0.42, 0.7])
s_white = Mat(["w0", "w1"], line="tn1", cuts=[0.52])
s_dark = Mat(["cd0", "cd1", "cd2"], line="cd0", cuts=[0.34, 0.66])
s_mouth = Mat(["m0", "m1"], line="m0", cuts=[0.5])


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
    """Battle sprites are hand-finished (art/gelasable_*.txt); this draft
    matches them for the icon and the follower."""
    if view in ("front", "side", "icon"):
        # coiled like a spring, haunches low, the head turned back over its
        # shoulder to laugh at whoever is behind it
        F = 1 if (phase == 1 and view != "side") else 0
        W = view == "side" and phase == 1
        p.limb(bez((15, 49), (0, 45), (5, 30 - F)), 6.4, 5.4, s_tn, group=20)
        p.limb(bez((5, 31 - F), (8, 20 - F), (17, 22 - 2 * F)), 5.4, 4.4, s_dark, group=20)
        if W:
            far_h, far_f = [(21, 52), (21, 59)], [(46, 52), (47, 59)]
            near_h, near_f = [(16, 52), (16, 59)], [(43, 51), (44, 59)]
        else:
            far_h, far_f = [(21, 52), (24, 56), (23.5, 59)], [(46, 52), (51, 56), (54.5, 59)]
            near_h, near_f = [(16, 52), (13.5, 56), (11, 59)], [(43, 51), (46, 55.5), (49, 59)]
        p.limb(far_h, 4.6, 3.2, s_tn, bias=0.35, group=10)
        p.limb(far_f, 3.8, 3.0, s_tn, bias=0.35, group=11)
        body = p.limb(bez((18, 50), (30, 41), (44, 47)), 12, 11, s_tn, group=1)
        p.blob(17, 50, 7.4, 6.6, s_tn, group=1)
        p.limb(bez((24, 53), (32, 52.5), (42, 53)), 3.4, 3, s_white, clip=[body], group=2)
        p.limb(near_h, 5.4, 3.4, s_tn, group=12)
        p.limb(near_f, 4.4, 3.4, s_tn, group=13)
        p.limb(bez((44, 46), (49, 37), (43, 30 - F)), 12, 10.5, s_tn, group=1)
        p.limb([(38.5, 38.5 - F), (44, 41.5), (50.5, 41)], 7.4, 7.4, s_dark, group=8)
        # the head turned all the way back to laugh at us: round skull, ears
        # low on the sides, a white muzzle round the open mouth
        p.circle(49, 19 - F, 2.7, s_tn, bias=0.25, group=5)
        p.circle(31, 19 - F, 2.9, s_tn, group=6)
        head = p.blob(40, 23.5 - F, 9, 8.2, s_tn, group=3)
        p.blob(40, 27.5 - F, 8.8, 4.6, s_tn, group=3)
        p.blob(40, 28 - F, 6.2, 4.4, s_white, clip=[head], group=4)
        p.blob(40, 27.6 - F, 4.4, 2.6, s_mouth, group=9)
        if p.big:
            p.pxs([(34, 20 - F), (35, 20 - F), (36, 20 - F), (42, 20 - F), (43, 20 - F)], "ink")
            p.pxs([(34, 21 - F), (42, 21 - F)], "w1")
            p.pxs([(35, 21 - F), (43, 21 - F)], "ink")
            p.pxs([(39, 23 - F), (40, 23 - F)], "ink")
            for x, y in ((39, 39), (44, 42), (49, 41)):
                _torch(p, x, y - (F if x < 42 else 0))
        else:
            p.pxs([(35, 21 - F), (43, 21 - F)], "ink")
            for x, y in ((39, 39), (44, 42), (49, 41)):
                p.px(x, y, "g1")
        return

    if view == "back":
        # the hand-finished art replaces this
        p.limb(bez((14, 72), (24, 50), (40, 44)), 24, 18, s_tn, group=1)
        p.limb(bez((40, 50), (44, 40), (43, 30)), 14, 12, s_tn, group=1)
        p.blob(38, 22, 8, 6.4, s_tn, group=3)
        return

    if view in ("down", "up"):
        # follower slinking low; every other step it stops to snicker
        s = phase
        p.limb([(27.5, 52), (27, 59)], 4, 3.2, s_tn, group=12)
        p.limb([(36.5, 52), (37, 59)], 4, 3.2, s_tn, group=13)
        tail = [(36, 52), (48, 50), (46, 36)] if view == "down" else [(32, 52), (44 + 2 * s, 46), (41 + 2 * s, 33)]
        p.limb(bez(*tail), 5, 4, s_tn, group=20)
        tip = tail[2]
        p.limb(bez((tip[0] + 0.5, tip[1] + 5), tip, (tip[0] - 4, tip[1] - 3)), 4.6, 3.4, s_dark, group=20)
        body = p.blob(32, 48, 8.4, 7.4, s_tn, group=1)
        if view == "down":
            p.blob(32, 49, 4.6, 5.6, s_white, clip=[body], group=2)
        p.limb([(32, 41.5), (32, 39)], 14, 12.4, s_dark, group=8)
        p.circle(24.5, 27, 3.2, s_tn, group=5)
        p.circle(39.5, 27, 3.2, s_tn, group=6)
        head = p.blob(32, 32 - s, 8.4, 6.8, s_tn, group=3)
        if view == "down":
            p.blob(32, 36.5 - s, 5, 3, s_white, group=4)
            p.blob(32, 36.6 - s, 3.4, 1.2 + 0.8 * s, s_mouth, group=9)
            p.pxs([(27, 29 - s), (28, 29 - s), (29, 29 - s), (35, 29 - s), (36, 29 - s), (37, 29 - s)], "ink")
            p.pxs([(28, 30 - s), (36, 30 - s)], "w1")
            p.pxs([(31, 34 - s), (32, 34 - s)], "ink")
        for x, y in ((27, 41), (31, 42), (35, 41)):
            _torch(p, x, y)
        return


MONS = [
    Mon("Galekit", GALEKIT_COLORS, GALEKIT_SHINY, galekit, foot="paw"),
    Mon("Gelasable", GELASABLE_COLORS, GELASABLE_SHINY, gelasable, foot="paw"),
]
