"""Mask line: Prosomime (Psychic/Poison). The two-faced mask of the
Dionysia, and Thespis, the first actor, who stepped out of the chorus and
spoke as someone else. A violet smoke ghost lives in the mask and wears it."""
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
    # wine-violet haze: the ghost's smoke body and the glow in the hollows
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
m_hole = Mat(["ink"])
m_smoke = Mat(["wine0", "wine1", "wine2"], line="wine0", cuts=[0.4, 0.72])


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
        # matches it for the icon and the follower: the smoke ghost behind,
        # its tongues streaming back, the mask with its carved features
        L = 1 if (phase == 1 and view == "front") else 0
        sw = phase
        for ang, r, rad in ((-118, 16.5, 6.4), (-60, 16, 6.6), (-25, 15.5, 7.0), (10, 15, 7.4), (45, 14, 7.6),
                            (95, 13, 8.0), (135, 14.5, 6.6), (170, 15, 5.6)):
            a = math.radians(ang)
            p.circle(32 + r * math.cos(a), 31 + r * 0.95 * math.sin(a) - L, rad, m_smoke, group=20)
        p.blob(33, 32 - L, 17, 17.5, m_smoke, group=20)
        for a, b, w, bend in (((43, 19), (52, 7 + sw), 7.0, -2.4), ((47, 25), (57, 16 - sw), 6.0, -2.0),
                              ((47.5, 33), (58, 28 + sw), 5.0, -1.4)):
            p.lens((a[0], a[1] - L), (b[0], b[1] - L), w, m_smoke, bend=bend, fat=0.35, group=20)
        p.limb(bez3((36, 44), (42, 54), (51, 55), (54.5, 48 + sw)), 14.0, 3.2, m_smoke, group=20)
        _ribbon(p, bez3((45, 22 - L), (54, 16), (54, 27), (61.5, 29 + sw)), 4.6, 30)
        _ribbon(p, bez3((45, 25 - L), (54, 26), (52, 37), (60.5, 42 - sw)), 5.0, 31)
        mask = p.poly(mask_pts(30, 31 - L, 14.2, 16.4, -6), m_com, group=1)
        for x, y, r in ((44.5, 21, 3.2), (16, 21.5, 3.0), (41.5, 16.5, 3.6), (19, 16.5, 3.6), (36.5, 13.2, 3.8),
                        (24, 13.2, 3.8), (30.2, 11.8, 4.0)):
            p.circle(x, y - L, r, m_com if x < 30 else m_tra, group=2)
        p.poly([(29.5, 0), (28, 64), (64, 64), (64, 0)], m_tra, group=1, clip=[mask])
        # eye holes and the open stage mouth as parts, so they scale
        p.poly(poly_from(bez3((18, 27.5), (19.5, 21.5), (24.5, 21.5), (26, 27.5)) + [(23.5, 25.5), (20.5, 25.5)], -L),
               m_haze, group=91)
        p.poly(poly_from([(32, 23), (36, 24.5), (41.5, 28.5), (37, 29), (33.5, 26)], -L), m_haze, group=92)
        p.poly(poly_from(bez3((19.5, 31.5), (21.5, 34.8), (25, 35.6), (29, 35.2))
                         + bez3((29, 35.2), (33, 34.8), (37.5, 36), (40.5, 40.8))[1:]
                         + bez3((40.5, 40.8), (38, 42.4), (34.5, 43.4), (29.5, 43.6))[1:]
                         + bez3((29.5, 43.6), (24.5, 43.6), (20.5, 40), (19.5, 31.5))[1:], -L), m_hole, group=90)
        # spectral fingers gripping the chin
        for f in (bez3((15.5, 45.5), (17, 44), (18.5, 43.8), (19.8, 44.6)), bez3((16.5, 47.5), (18.5, 46.4), (20, 46.4), (21.2, 47.3))):
            p.limb(poly_from(f, -sw), 2.4, 1.8, m_smoke, group=95)
        if p.big:
            p.pxs([(22, 24 - L), (37, 26 - L)], "white")
            p.pxs([(19, 30 - L), (20, 30 - L), (21, 30 - L), (20, 31 - L)], "terra1")
        return

    if view == "back":
        # the ghost from behind wearing the mask (the hand-finished art
        # replaces this)
        p.blob(26, 60, 23.5, 15, m_smoke, group=20)
        p.blob(33, 33, 11, 13, m_smoke, group=20)
        outer = p.poly(mask_pts(43, 34, 13.4, 19.5, 8), m_tra, group=1)
        p.poly([(44, 0), (44, 64), (64, 64), (64, 0)], m_com, group=1, clip=[outer])
        p.blob(35.5, 34.5, 9.6, 12.5, m_smoke, group=21)
        _ribbon(p, bez3((30, 26), (20, 22), (18, 32), (8, 30)), 5.0, 30)
        return

    if view in ("down", "up"):
        # follower: the ghost bobbing toward the player behind its mask, the
        # tragic half turned toward them; walking away, its smoky back with
        # the ribbons' bow and the mask's rim at the sides
        st = phase
        cx, cy = 32, 31 - st
        p.blob(32, 33 - st, 17, 16, m_smoke, group=20)
        for a, b in (((20, 22), (12, 10 + st)), ((44, 22), (52, 10 + (1 - st)))):
            p.lens((a[0], a[1] - st), b, 7.0, m_smoke, bend=1.6 if a[0] < 32 else -1.6, fat=0.35, group=20)
        p.limb(bez3((32, 44), (30, 52), (36, 56), (40, 53 - st)), 12, 3, m_smoke, group=20)
        if view == "down":
            mask = p.poly(mask_pts(cx, cy, 13.4, 15.4, 4), m_com, group=1)
            for x, y, r in ((21, 19.5, 3.0), (25.5, 16.5, 3.2), (31, 15.5, 3.4), (36.5, 16.5, 3.2), (41, 19.5, 3.0)):
                p.circle(x, y - st, r, m_com if x < 29 else m_tra, group=2)
            p.poly([(29, 10), (29, 60), (60, 60), (60, 10)], m_tra, group=1, clip=[mask])
            p.poly(poly_from(bez3((20, 28), (21.5, 22.5), (26.5, 22.5), (28, 28)) + [(25.5, 26), (22.5, 26)], -st),
                   m_haze, group=91)
            p.poly(poly_from([(34, 23), (38.5, 25), (43, 29.5), (38.5, 30), (35, 27)], -st), m_haze, group=92)
            p.poly(poly_from(bez3((20, 33), (23, 37.5), (28, 38), (32, 37.5)) + bez3((32, 37.5), (36, 36.5), (40, 39), (42, 44))[1:]
                             + bez3((42, 44), (39, 44.5), (35, 45), (32, 45)) + bez3((32, 45), (26, 45.5), (21.5, 41.5), (20, 33))[1:],
                             -st), m_hole, group=90)
            _ribbon(p, bez3((45, 26), (53, 30), (49, 40), (55, 48 - (1 - st))), 3.6, 31)
        else:
            for x in (18.5, 45.5):
                p.blob(x, 30 - st, 2.6, 8, m_tra if x > 32 else m_com, group=1)
            p.blob(32, 25 - st, 2.6, 2.6, m_rib, group=32)
            _ribbon(p, bez3((31, 26), (26, 33), (32, 41), (27, 50 - st)), 4.0, 30)
            _ribbon(p, bez3((33, 26), (38, 33), (32, 41), (37, 50 - (1 - st))), 4.0, 31)
        return


def poly_from(pts, dy=0):
    return [(x, y + dy) for x, y in pts]


MONS = [
    Mon("Prosomime", PROSOMIME_COLORS, PROSOMIME_SHINY, prosomime, foot="blank"),
]
