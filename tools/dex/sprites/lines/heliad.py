"""Heliad line: Elektear (Electric / Grass). The Heliades.

When Phaethon fell from the sun chariot, his sisters wept on the riverbank
until they took root and turned into poplars; their tears still drip from
the branches and harden in the sun into amber, elektron, the word that gave
us "electric" (Ovid, Metamorphoses 2). Elektear is a Heliad caught halfway
into the tree: legs fused into a narrow poplar trunk, arms raised into
trembling branches, a columnar poplar crown for hair, and strings of amber
tear-beads that spark where they touch.
"""
from mon_lib import Mat, Mon, bez, bez3, lens_pts

INK = (32, 24, 24)

ELEKTEAR_COLORS = [
    ("ink", INK),
    # marble-gray poplar bark, pale as white poplar, with dark lenticels
    ("bark0", (80, 80, 88)), ("bark1", (128, 128, 128)), ("bark2", (176, 176, 168)), ("bark3", (216, 216, 208)),
    ("skin", (240, 240, 232)),
    # olive leaves with a silver-leaf underside
    ("leafd", (24, 40, 32)), ("leaf0", (40, 64, 40)), ("leaf1", (88, 112, 48)), ("leaf2", (144, 160, 72)),
    ("silver", (192, 208, 184)),
    # sun-gold amber tears, glowing from within, and their sparks
    ("amb0", (176, 88, 24)), ("amb1", (240, 160, 40)), ("amb2", (248, 224, 112)), ("spark", (248, 248, 200)),
]
ELEKTEAR_SHINY = {
    # silver-white bark with Aegean-blue tears
    "bark0": (96, 104, 120), "bark1": (152, 160, 176), "bark2": (200, 208, 216), "bark3": (232, 232, 240),
    "skin": (248, 248, 248),
    "amb0": (24, 56, 120), "amb1": (48, 104, 176), "amb2": (112, 168, 224), "spark": (200, 232, 248),
}

e_bark = Mat(["bark0", "bark1", "bark2", "bark3"], line="bark0", cuts=[0.16, 0.42, 0.7])
e_skin = Mat(["bark2", "bark3", "skin"], line="bark1", cuts=[0.36, 0.66])
e_twig = Mat(["bark0", "bark1", "bark2"], line="bark0", cuts=[0.36, 0.7])
e_leaf = Mat(["leaf0", "leaf1", "leaf2", "silver"], line="leaf0", cuts=[0.2, 0.46, 0.74])
e_crown = Mat(["leafd", "leaf0", "leaf1", "leaf2", "silver"], line="leafd", cuts=[0.14, 0.34, 0.58, 0.84])


def _pleaf(p, base, tip, w=3.6, depth=1, **kw):
    """A trembling poplar leaf: broad near its stalk, pointed at the tip.
    depth 0 shows the silver underside catching the light, 2 sits in shade."""
    flat = (3, 2, 1)[depth] if not p.big else None
    bias = (-0.06, 0.06, 0.24)[depth]
    return p.poly(lens_pts(base, tip, p._minw(w), kw.pop("bend", 0.0), fat=0.34), e_leaf,
                  bias=bias, flat=flat, **kw)


def _wand(p, path, leaves, sw=0, far=False):
    """An arm's tall, thin branch: a whip along `path` with leaves on short
    stalks along it, alternating sides: [(t, side, length, width)]."""
    import math
    p.limb(path, 2.0, 1.0, e_twig, bias=0.2 if far else 0, group=21 if far else 23)
    n = len(path) - 1
    for t, side, ln, w in leaves:
        i = min(n - 1, int(t * n))
        (x0, y0), (x1, y1) = path[i], path[i + 1]
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy) or 1
        ux, uy = dx / d, dy / d
        nx, ny = -uy * side, ux * side
        bx, by = x0 + dx * 0.5, y0 + dy * 0.5
        tip = (bx + (nx * 0.8 + ux * 0.6) * ln + sw * 0.6 * side, by + (ny * 0.8 + uy * 0.6) * ln)
        depth = 2 if far else (0 if side < 0 else 1)
        _pleaf(p, (bx, by), tip, w, depth=depth)


def _plume(p, x, y, sw=0, back=False):
    """The poplar crown's plume: a narrow column of leaf-locks rising from the
    back of the crown at (x, y) and leaning back like a Lombardy poplar."""
    m = (lambda u: 2 * x - u) if back else (lambda u: u)
    P = lambda u, v: (m(u), v)
    b = 1.6 if back else -1.6
    p.poly(lens_pts(P(x, y), P(x + 6.5 + sw, y - 16), 11, bend=b, fat=0.3), e_crown, group=40)
    if p.big:
        for a, c, w in (((x + 2, y - 10), (x + 0.5, y - 14.5), 3.6), ((x + 4.5, y - 6), (x + 5.5 + sw, y - 11.5), 3.6),
                        ((x + 1, y - 4), (x - 1.5, y - 9.5), 4), ((x + 6, y - 3), (x + 9 + sw, y - 8.5), 3.6)):
            _pleaf(p, P(*a), P(*c), w, depth=0, group=45, bend=0.5 if not back else -0.5)


def elektear(p, view, phase):
    if view == "icon":
        # party icon: the front pose in bold flat shapes, so the pale figure,
        # the green crown and the amber tears read at 32 px
        for sx, hand, top in ((-1, (14.5, 21), (13, 3)), (1, (42, 21), (44, 4))):
            sh = (24, 37) if sx < 0 else (33, 37)
            el = (16.5, 31) if sx < 0 else (40, 30)
            p.limb([sh, el, hand], 4.6, 3.6, e_skin, flat=1)
            p.limb([hand, top], 2.6, 1.6, e_twig, flat=1)
            for k, (dx, dy) in enumerate(((-4, -3), (4, -6), (-3, -12), (3, -15))):
                p.blob(hand[0] + dx * 0.9 + (top[0] - hand[0]) * (k + 1) / 5, hand[1] + (top[1] - hand[1]) * (k + 1) / 5,
                       4.2, 3.2, e_leaf, flat=2 if k % 2 else 1)
        p.poly(lens_pts((30, 18), (37, 1.6), 11, bend=-1.4, fat=0.3), e_crown, flat=3)
        p.poly(bez3((27.6, 43), (26.4, 49), (26.8, 54), (24.4, 57.6)) + [(28.4, 58.9), (32.6, 58.9)] +
               bez3((36.4, 57.6), (34.2, 54), (34.2, 49), (33.4, 43)), e_bark, flat=2)
        p.limb([(28.4, 36.5), (30.4, 45.5)], 10.4, 7, e_skin, flat=2)
        # the hair stays a clear green at icon size (leaf1 and leaf2, never the
        # darkest leaf tones, which the shared icon palettes turn gray)
        p.blob(26.5, 21, 10, 8.4, e_crown, flat=2)
        p.blob(26, 27.5, 6.4, 6.8, e_skin, flat=2)
        p.limb([(26.5, 17.5), (20, 23)], 4, 2.6, e_crown, flat=3)
        p.limb([(20.5, 21), (17.6, 33)], 3.6, 2.4, e_crown, flat=3)
        p.limb([(33, 19), (33.6, 32)], 3.6, 2.4, e_crown, flat=2)
        p.pxs([(22.5, 26.5), (28.5, 26.5)], "ink")
        p.pxs([(22.5, 29), (28.5, 29)], "amb1")
        return
    if view in ("front", "side"):
        sw = 1 if (phase == 1 and view == "front") else 0   # frame 2: the leaves tremble, the head bows
        L = sw
        hx, hy = 26, 26.5 - L          # the face's center

        # ---- far arm, raised up and out; the hand rises into a tall branch
        p.limb(bez((33, 37.5), (39, 35.5), (40.2, 29.5)), 3.8, 3.2, e_bark, bias=0.1, group=20)
        p.limb(bez((40.2, 30), (41, 25.5), (41.6, 21.5)), 3.2, 2.6, e_bark, bias=0.1, group=20)
        _wand(p, bez((41.6, 22), (44.5, 13), (42.6 + sw * 0.6, 4)),
              [(0.1, 1, 6.4, 5), (0.32, -1, 6.4, 5), (0.54, 1, 6, 4.8), (0.74, -1, 5.6, 4.4), (0.94, 1, 5, 4)], sw, far=True)
        # ---- the plume and the cap of hair
        _plume(p, 31, 18 - L, sw)
        p.blob(26.5, 21 - L, 9.8, 8.2, e_crown, group=46)
        # ---- the trunk: legs fused into a narrow poplar bole, rooting like a hem
        bole = bez3((27.6, 43), (26.4, 49), (26.8, 54), (24.4, 57.6)) + [(28.4, 58.9), (32.6, 58.9)] + \
            bez3((36.4, 57.6), (34.2, 54), (34.2, 49), (33.4, 43))
        p.poly(bole, e_bark, group=30, bias=0.08)
        for path, w0 in (([(25.6, 57.2), (21, 59.4), (17.4, 60)], 3.8), ([(30.6, 58.2), (30.2, 60.8)], 3.4),
                         ([(35.2, 57.2), (39.4, 59.4), (43, 60)], 3.8)):
            p.limb(path, w0, 1.4, e_bark, group=31)
        # ---- torso, neck and the marble face
        p.limb([(28.4, 36.5), (29.6, 41), (30.4, 45.5)], 10.4, 7, e_skin, group=1)
        p.blob(28.4, 38.6, 6.4, 3.6, e_skin, ang=-8, group=1)
        p.limb([(25.6, 30 - L), (26.4, 36)], 4.4, 5.6, e_skin, group=1)
        p.poly([(26.4, 47), (27, 42.6), (28.4, 44.2), (29.6, 41), (31, 44), (32.4, 41.8), (34.4, 47)], e_bark, group=30)
        p.blob(hx, hy, 6.6, 7, e_skin, group=3)
        # bangs over the brow and the long locks at the sides
        _pleaf(p, (27, 17 - L), (21.5, 24 - L), 4.6, depth=0, group=41, bend=0.6)
        _pleaf(p, (29.5, 17 - L), (26.2, 23 - L), 4.2, depth=0, group=42, bend=0.4)
        _pleaf(p, (24, 17 - L), (18.4, 22 - L), 3.8, depth=0, group=43, bend=0.6)
        _pleaf(p, (33, 19 - L), (33.6, 33 - L), 4.6, depth=1, group=44, bend=-0.8)
        _pleaf(p, (20.5, 21 - L), (17.6, 35 - L), 4, depth=0, group=47, bend=0.8)
        # a collar of poplar leaves at the neckline
        if p.big:
            _pleaf(p, (27.4, 34.2), (26.6, 39.6), 4.2, depth=1, group=48)
            _pleaf(p, (24.6, 34.4), (20.8, 38.4), 4, depth=0, group=49)
            _pleaf(p, (30.2, 34), (33.8, 38), 4, depth=2, group=50)
        # ---- near arm, raised up and forward; the hand rises into a tall branch
        p.limb(bez((24, 37.6), (18.6, 36), (16.4, 30)), 4.4, 3.6, e_skin, group=22)
        p.limb(bez((16.4, 30.5), (15.4, 26), (15.2, 21.5)), 3.6, 2.8, e_skin, group=22)
        _wand(p, bez((15.2, 22), (12.2, 13), (15 + sw * 0.6, 3.4)),
              [(0.08, -1, 6.6, 5.2), (0.3, 1, 6.4, 5), (0.52, -1, 6.4, 5), (0.72, 1, 6, 4.6), (0.93, -1, 5.2, 4.2)], sw)
        # ---- the face: downcast eyes under drooping lids, strings of amber tears
        if p.big:
            p.patch(20, 24 - L, [
                " 1111  1111",
                "11f1 1 1f11",
                " 1dd1  1dd1",
                "  11    11 ",
                " ed     ed ",
                " dc     dc ",
                " f       f ",
                "ed      ed ",
                "dc      dc ",
            ], {"1": "ink", "c": "amb0", "d": "amb1", "e": "amb2", "f": "spark"})
            for x, y in ((31, 49), (32, 49), (29, 53), (30, 53), (32, 55), (33, 55), (28, 47), (29, 47)):
                p.px(x, y, "bark0")
        else:
            p.px(22, 26 - L, "ink")
            p.px(28, 26 - L, "ink")
            p.px(22, 28 - L, "amb1")
            p.px(28, 28 - L, "amb1")
        return

    if view == "back":
        # over the shoulder at about 1.2x: her pale back, cropped by the
        # frame; the head turned right in profile with a string of tears;
        # the poplar spire, and both arms raised into tall branches
        p.limb(bez((44, 47), (51.5, 42), (52, 32)), 5, 4, e_skin, bias=0.22, group=20)
        p.limb(bez((52, 32.5), (52.5, 27), (52.5, 22)), 4, 3, e_skin, bias=0.22, group=20)
        _wand(p, bez((52.5, 22.5), (55, 12), (52, 2.5)),
              [(0.08, 1, 6, 4.4), (0.24, -1, 6, 4.4), (0.42, 1, 6, 4.2), (0.6, -1, 5.6, 4.0),
               (0.78, 1, 5, 3.8), (0.94, -1, 4.4, 3.4)], far=True)
        p.poly(lens_pts((33, 22), (29, 1.5), 14, bend=0.8, fat=0.32), e_crown, group=40)
        p.blob(34, 27, 10, 9.4, e_crown, group=40)
        p.blob(30, 64, 22, 17, e_skin, group=1)
        p.limb([(31, 50), (35, 39)], 9, 6.4, e_skin, group=1)
        for x, y in ((24, 54), (31, 57), (37, 53), (21, 60), (28, 61), (40, 59)):
            p.pxs([(x, y), (x + 1, y), (x + 1, y - 1)], "bark1")
        # the face in right profile
        p.blob(40.5, 31, 6.2, 7, e_skin, ang=-10, group=3)
        _pleaf(p, (32, 21), (46, 26), 6.6, depth=0, group=41, bend=-1.4)
        _pleaf(p, (30, 22), (24, 38), 7, depth=1, group=42, bend=1.2)
        # near arm, raised up the left side
        p.limb(bez((19, 49), (10, 45), (9, 35)), 6, 4.8, e_skin, group=22)
        p.limb(bez((9, 35.5), (8, 29), (8.5, 24)), 4.6, 3.4, e_skin, group=22)
        _wand(p, bez((8.5, 24.5), (6, 13), (10, 2)),
              [(0.06, -1, 6.4, 4.6), (0.22, 1, 6.4, 4.6), (0.4, -1, 6.4, 4.4), (0.58, 1, 6, 4.2),
               (0.76, -1, 5.4, 4.0), (0.92, 1, 4.6, 3.6)])
        if p.big:
            p.patch(41, 29, ["111.", "1c1.", ".1..", "..yo", "..ob", "...s", "..yo", "..ob", "..s.", ".yo.", ".ob."],
                    {"1": "ink", "c": "amb1", "y": "amb2", "o": "amb1", "b": "amb0", "s": "spark"})
        return

    if view in ("down", "up"):
        # follower: gliding on her roots with both branches raised; a dropped
        # amber bead glows on the ground, then blinks out
        down = view == "down"
        if phase == 0:
            bx = 44 if down else 19
            p.patch(bx, 57, [".f.", "edc", ".c."], {"e": "amb2", "d": "amb1", "c": "amb0", "f": "spark"},
                    small=(bx, 58, ["d"]))
        bole = bez3((28.6, 42), (27.6, 48), (27.8, 53), (25.6, 56.6)) + [(29, 57.8), (35, 57.8)] + \
            bez3((38.4, 56.6), (36.2, 53), (36.4, 48), (35.4, 42))
        p.poly(bole, e_bark, group=30)
        for path in (([(26.6, 56), (21.4, 59 + phase)]), ([(32, 57), (32, 60.4 - phase)]), ([(37.4, 56), (42.6, 60 - phase)])):
            p.limb(path, 3.6, 1.4, e_bark, group=31)
        for sx in (-1, 1):
            X = lambda x: 32 + sx * (x - 32)
            k = phase if sx < 0 else 1 - phase
            p.limb(bez((X(27.6), 35), (X(20.6), 33), (X(18.6), 25)), 4.2, 3.2, e_skin, group=22 if sx < 0 else 24)
            _wand(p, bez((X(18.6), 25.5), (X(16), 15), (X(18.6) + k * sx, 4)),
                  [(0.1, -sx, 6, 4.8), (0.34, sx, 6, 4.6), (0.58, -sx, 5.6, 4.4), (0.8, sx, 5, 4), (0.97, -sx, 4.2, 3.4)],
                  far=not down)
        p.limb([(32, 31), (32, 44)], 10, 7.4, e_skin, group=1)
        p.poly([(28.4, 45), (29, 41.6), (30.5, 43.2), (32, 40.4), (33.5, 43.2), (35, 41.6), (35.6, 45)], e_bark, group=30)
        _plume(p, 32, 18, back=not down)
        p.blob(32, 22, 9.6, 8.6, e_crown, group=46)
        if down:
            p.blob(32, 26.5, 7, 7.2, e_skin, group=3)
            _pleaf(p, (32, 17), (25.5, 24), 5, depth=0, group=41, bend=0.6)
            _pleaf(p, (32, 17), (38.5, 24), 5, depth=1, group=42, bend=-0.6)
            _pleaf(p, (25, 21), (23.6, 34), 4, depth=0, group=43, bend=0.6)
            _pleaf(p, (39, 21), (40.4, 34), 4, depth=1, group=44, bend=-0.6)
            p.patch(26, 25, ["1111 1111", "1fd1 1fd1", " 11   11 ", " ed   ed ", " dc   dc "],
                    {"1": "ink", "c": "amb0", "d": "amb1", "e": "amb2", "f": "spark"},
                    small=(28, 26, ["1...1", "d...d"]))
        else:
            for a, b, bend, dp in (((29, 22), (25, 38), -1.2, 1), ((35, 22), (39, 38), 1.2, 1), ((32, 23), (32, 41), 0.0, 0)):
                _pleaf(p, a, b, 7, depth=dp, bend=bend)
            p.blob(32, 19, 8, 5.6, e_crown, group=47)
        return


MONS = [
    # icon palette 5 keeps the greens and turns the tears orange rather than gray
    Mon("Elektear", ELEKTEAR_COLORS, ELEKTEAR_SHINY, elektear, foot="root", icon_pal=5),
]
