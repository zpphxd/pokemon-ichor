"""Mask line: Prosomime (Psychic/Poison). The two-faced mask of the
Dionysia, and Thespis, the first actor, who stepped out of the chorus and
spoke as someone else."""
import math

from mon_lib import C, Mat, Mon, bez3

INK = C.ink

PROSOMIME_COLORS = [
    ("ink", INK),
    # marble face: the comic half and the tragic half are separate ramps so
    # the shiny can paint them differently; they share the top highlight
    ("com0", (136, 128, 136)), ("com1", (192, 184, 184)), ("com2", (224, 216, 208)),
    ("tra0", (136, 128, 136)), ("tra1", (192, 184, 184)), ("tra2", (224, 216, 208)),
    ("white", C.white),
    # terracotta cheek paint
    ("terra0", (152, 56, 40)), ("terra1", (216, 112, 72)),
    # wine-violet haze and the dark of the hollows
    ("wine0", (64, 24, 72)), ("wine1", (120, 64, 136)), ("wine2", (176, 120, 200)),
    # Psychic-pink ribbons
    ("rose0", (192, 72, 120)), ("rose1", (240, 144, 176)),
]
PROSOMIME_SHINY = {
    # the comic half sun-gold, the tragic half black-figure ink
    "com0": (176, 112, 32), "com1": (224, 168, 56), "com2": (248, 208, 96),
    "tra0": (32, 24, 32), "tra1": (56, 48, 56), "tra2": (96, 88, 96),
}

m_com = Mat(["com0", "com1", "com2", "white"], line="com0", cuts=[0.2, 0.5, 0.78])
m_tra = Mat(["tra0", "tra1", "tra2", "white"], line="tra0", cuts=[0.2, 0.5, 0.78])
m_rib = Mat(["rose0", "rose1"], line="rose0", cuts=[0.5])
m_haze = Mat(["wine1", "wine2"], line="wine1", outline="wine1", cuts=[0.5])
m_hole = Mat(["wine0"])


def _ribbon(p, path, w, group, far=False):
    """A flat ribbon streaming along path, twisting: wider where it faces
    the viewer, a thin edge where it turns."""
    def wid(t):
        return w * (0.45 + 0.55 * abs(math.cos(t * math.pi * 2.2)))
    from mon_lib import ribbon
    poly = ribbon(path, wid)
    return p.poly(poly, m_rib, group=group, bias=0.25 if far else 0.0)


def mask_pts(cx, cy, rx, ry, rot=0.0):
    """The mask's outline: a broad brow, full cheeks and a rounded chin."""
    pts = []
    n = 48
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = math.cos(t), math.sin(t)
        # a little narrower at the chin, broad at the brow
        k = 1.0 - 0.16 * max(0.0, y) ** 2
        x, y = x * rx * k, y * ry
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def prosomime(p, view, phase):
    if view in ("front", "side", "icon"):
        # the battle front is hand-finished in the art files; this draft
        # matches it for the icon and the follower
        L = 1 if (phase == 1 and view == "front") else 0
        sw = phase
        # a soft trail of violet haze under the mask, drifting back like a tail
        p.limb(bez3((30, 44 - L), (34, 51), (41, 52), (46, 58 - sw)), 6.4, 1.6, m_haze, group=29)
        _ribbon(p, bez3((40, 25 - L), (53, 20), (49, 37), (59, 44 + sw)), 5.6, 30, far=True)
        _ribbon(p, bez3((40, 29 - L), (54, 33), (44, 46), (54, 58 - sw)), 6.0, 31)
        mask = p.poly(mask_pts(28.8, 32 - L, 15.0, 15.8, -6), m_com, group=1)
        crest = []
        for x, y, r in ((17.6, 20, 3.1), (21.4, 16.4, 3.3), (26.6, 14.4, 3.6), (32.8, 14.6, 3.5), (37.8, 16.6, 3.3),
                        (41.2, 20.5, 3.0)):
            crest.append(p.circle(x, y - L, r, m_com if x < 29 else m_tra, group=2 + len(crest)))
        mid = bez3((29, 6 - L), (28.5, 22 - L), (27.5, 34 - L), (27, 52 - L))
        p.poly(mid + [(50, 52 - L), (50, 6 - L)], m_tra, group=1, clip=[mask])
        p.blob(41, 27 - L, 2.2, 2.6, m_rib, group=32)
        if p.big:
            p.patch(14, 22 - L, ["...1111", "..1cddc1", ".1cd8ddc1", "1cddddddc1", "1c111111c1", "11......11"],
                    {"1": "ink", "c": "wine1", "d": "wine2", "8": "white"})
            p.patch(30, 22 - L, ["111", "1cc11", ".1cdd11", ".1c8ddc11", "..1ddddcc1", "...11dccc1", ".....1111"],
                    {"1": "ink", "c": "wine1", "d": "wine2", "8": "white"})
            mouth = poly_from(bez3((15.2, 33), (18, 37.5), (23, 38.8), (27.5, 38.4))
                              + bez3((27.5, 38.4), (31.5, 36.6), (36, 39.5), (38.6, 45))[1:]
                              + bez3((38.6, 45), (35.5, 43.6), (32, 41.2), (27.5, 43.4))[1:]
                              + bez3((27.5, 43.4), (21.5, 46.4), (16.5, 41.5), (15.2, 33))[1:], -L)
            p.poly(mouth, m_hole, group=90)
            p.pxs([(16, 30 - L), (17, 30 - L), (18, 30 - L), (17, 29 - L)], "terra1")
            p.pxs([(38, 29 - L), (38, 30 - L), (38, 31 - L)], "wine2")
        else:
            # at icon size the features are parts, so they scale
            p.poly(poly_from(bez3((14, 27.5), (16, 21.5), (22, 21.5), (24, 27.5)) + [(21, 25.5), (17, 25.5)], -L),
                   m_haze, group=91)
            p.poly(poly_from([(30, 22.5), (34, 24.5), (39.5, 28.5), (35, 29), (31.5, 26)], -L), m_haze, group=92)
            p.poly(poly_from(bez3((15.2, 33), (18, 37.5), (23, 38.8), (27.5, 38.4))
                             + bez3((27.5, 38.4), (31.5, 36.6), (36, 39.5), (38.6, 45))[1:]
                             + bez3((38.6, 45), (35.5, 43.6), (32, 41.2), (27.5, 43.4))[1:]
                             + bez3((27.5, 43.4), (21.5, 46.4), (16.5, 41.5), (15.2, 33))[1:], -L), m_hole, group=90)
        return

    if view == "back":
        # the hollow inside of the mask (the hand-finished art replaces this)
        _ribbon(p, bez3((13, 33), (2, 36), (10, 48), (3, 58)), 5.4, 30, far=True)
        outer = p.poly(mask_pts(32.5, 45, 18, 20, 6), m_tra, group=1)
        p.poly([(34, 10), (34, 70), (70, 70), (70, 10)], m_com, group=1, clip=[outer])
        inner = p.poly(mask_pts(31, 47, 14.2, 16.6, 6), m_tra, group=2, bias=0.2)
        p.poly([(34, 10), (34, 70), (70, 70), (70, 10)], m_com, group=2, clip=[inner], bias=0.2)
        _ribbon(p, bez3((51, 33), (61, 38), (53, 49), (60, 60)), 5.4, 31)
        return

    if view in ("down", "up"):
        # follower: the mask bobbing toward the player, its tragic half
        # turned toward them; walking away, the hollow inside shows
        st = phase
        cx, cy = 32, 32 - st
        if view == "down":
            _ribbon(p, bez3((19, 26), (11, 32), (16, 42), (11, 52 - st)), 3.6, 30, far=True)
            _ribbon(p, bez3((45, 26), (53, 32), (48, 42), (53, 52 - (1 - st))), 3.6, 31, far=True)
            mask = p.poly(mask_pts(cx, cy, 13.4, 15.4, 4), m_com, group=1)
            for x, y, r in ((21, 19.5, 3.0), (25.5, 16.5, 3.2), (31, 15.5, 3.4), (36.5, 16.5, 3.2), (41, 19.5, 3.0)):
                p.circle(x, y - st, r, m_com if x < 29 else m_tra, group=2)
            p.poly([(29, 10), (29, 60), (60, 60), (60, 10)], m_tra, group=1, clip=[mask])
            # comic eye arch and mouth corner on the left, the tragic droop
            # and the tear on the right, turned toward the player
            p.poly(poly_from(bez3((20, 28), (21.5, 22.5), (26.5, 22.5), (28, 28)) + [(25.5, 26), (22.5, 26)], -st),
                   m_haze, group=91)
            p.poly(poly_from([(34, 23), (38.5, 25), (43, 29.5), (38.5, 30), (35, 27)], -st), m_haze, group=92)
            p.poly(poly_from(bez3((20, 34), (23, 39.5), (28, 40), (32, 39.5)) + bez3((32, 39.5), (36, 38), (40, 41), (42, 46))[1:]
                             + bez3((42, 46), (39, 44), (36, 42.5), (32, 44)) + bez3((32, 44), (26, 46.5), (21.5, 41.5), (20, 34))[1:],
                             -st), m_hole, group=90)
            p.limb(poly_from([(42, 31), (42.5, 35)], -st), 1.6, 1.4, m_haze, group=93)
        else:
            outer = p.poly(mask_pts(cx, cy, 13.4, 15.4, 0), m_tra, group=1)
            p.poly([(32, 10), (32, 60), (60, 60), (60, 10)], m_com, group=1, clip=[outer])
            inner = p.poly(mask_pts(cx - 0.5, cy + 1, 10.5, 12.6, 0), m_tra, group=2, bias=0.2)
            p.poly([(32, 10), (32, 60), (60, 60), (60, 10)], m_com, group=2, clip=[inner], bias=0.2)
            for x in (19, 45):
                p.blob(x, 27 - st, 2.4, 2.6, m_rib, group=32)
            _ribbon(p, bez3((20, 28), (14, 36), (22, 44), (16, 54 - st)), 3.6, 30)
            _ribbon(p, bez3((44, 28), (50, 36), (42, 44), (48, 54 - (1 - st))), 3.6, 31)
        return


def poly_from(pts, dy=0):
    return [(x, y + dy) for x, y in pts]


MONS = [
    Mon("Prosomime", PROSOMIME_COLORS, PROSOMIME_SHINY, prosomime, foot="blank"),
]
