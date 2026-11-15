"""Kallisto line: Arkoby, Starkos (Dark, then Dark/Fairy). The huntress
turned bear and set among the stars as the Great Bear; her cub is Arkas's
Little Bear, with the seven stars it will one day wear already on its back."""
from mon_lib import C, Mat, Mon, bez

INK = C.ink

# The battle art (tools/dex/sprites/art/arkoby_*, starkos_*) is hand-finished
# over sphere-shaded forms; these drafts give the icons and follower frames.

# --------------------------------------------------------------------------
# Arkoby, the star cub
# --------------------------------------------------------------------------

ARKOBY_COLORS = [
    ("ink", INK),
    # black-figure ink going into dark Aegean blue
    ("fur0", (32, 32, 72)), ("fur1", (48, 64, 128)), ("fur2", (72, 104, 176)), ("fur3", (104, 144, 216)),
    ("fur4", (160, 192, 240)),
    # the marble crescent on the chest
    ("mar0", (152, 152, 176)), ("mar1", (208, 208, 224)), ("white", C.white),
    # the seven star spots and their faint halo
    ("star", (240, 248, 248)), ("glow", (176, 168, 240)),
    # Fairy-pink nose and paw pads
    ("pink0", (192, 88, 128)), ("pink1", (248, 160, 192)),
    ("gold", C.sungold[1]),
]
ARKOBY_SHINY = {
    "fur0": (16, 40, 32), "fur1": (24, 64, 48), "fur2": (40, 96, 64), "fur3": (72, 136, 88), "fur4": (128, 184, 136),
    "star": (248, 208, 72), "glow": (184, 128, 40),
}

a_fur = Mat(["fur0", "fur1", "fur2", "fur3"], line="fur0", cuts=[0.26, 0.48, 0.7])
a_muz = Mat(["fur2", "fur3", "fur4"], line="fur1", cuts=[0.34, 0.66])
a_mar = Mat(["mar0", "mar1", "white"], line="mar0", cuts=[0.4, 0.66])
a_pad = Mat(["pink0", "pink1"], line="pink0", cuts=[0.5])


ARKOBY_STARS = ((40, 45), (38, 46), (37, 48), (38, 52), (42, 51), (43, 55), (39, 56))


def arkoby(p, view, phase):
    if view in ("front", "side", "icon"):
        # sitting up on its haunches, muzzle raised to the sky, the near
        # forepaw lifted toward the stars (the art files hand-finish this)
        L = 1 if (phase == 1 and view == "front") else 0
        walk = view == "side" and phase == 1
        p.blob(39.2, 25.6 - L, 3.8, 3.7, a_fur, bias=0.1, group=1)
        p.blob(39.2, 26.1 - L, 2.0, 1.9, a_muz, bias=0.3, group=1)
        p.blob(23.4 + walk, 58.8, 3.2, 2.0, a_fur, bias=0.15, group=2)
        p.blob(44.6, 57.4, 2.2, 2.0, a_fur, bias=0.1, group=3)
        body = p.blob(34.2, 51.4, 9.4, 8.8, a_fur, ang=5, bias=-0.04, group=4)
        p.blob(39.6, 54.6, 6.0, 5.5, a_fur, ang=-18, bias=-0.08, group=6)
        p.blob(29.8 - walk, 58.7, 4.8, 2.3, a_fur, ang=-5, group=7)
        p.lens((27.5, 44.6), (39.5, 44.0), 3.4, a_mar, bend=2.3, clip=[body], group=8)
        p.blob(31.2, 34.2 - L, 9.4, 8.6, a_fur, ang=-6, bias=-0.06, group=9)
        p.limb(bez((26, 37.6 - L), (23.5, 36 - L), (21.6, 33.6 - L)), 7.4, 6.6, a_muz, group=10)
        p.blob(29.6, 23.6 - L, 4.0, 3.9, a_fur, bias=-0.06, group=11)
        p.blob(29.4, 24.2 - L, 2.1, 2.0, a_muz, group=11)
        p.limb([(31, 49), (25.5, 50)], 5.6, 5.2, a_fur, group=12)
        p.limb([(25.5, 50), (22, 45.5 - L)], 5.2, 5.0, a_fur, group=12)
        p.blob(20.6, 43.6 - L, 3.6, 3.4, a_fur, bias=-0.08, group=12)
        if p.big:
            p.eye(25, 28 - L, 3, 5, shine="white", shine_at=(0, 1))
            p.px(26, 31 - L, "gold")
            p.pxs([(19, 31 - L), (20, 31 - L), (19, 32 - L), (20, 32 - L)], "pink0")
            p.pxs([(18, 42 - L), (22, 42 - L), (19, 43 - L), (20, 43 - L), (21, 43 - L)], "pink1")
            for x, y in ARKOBY_STARS:
                p.px(x, y, "star")
        else:
            p.px(25.5, 30 - L, "ink")
            p.px(19.5, 32 - L, "pink0")
            for x, y in ARKOBY_STARS[::2]:
                p.px(x, y, "star")
        return

    if view == "back":
        # over the shoulder: the round back with the seven stars, the head
        # turned right in profile looking up (hand-finished in the art file)
        p.blob(45.2, 23.4, 4.2, 4.1, a_fur, bias=0.12, group=1)
        p.blob(29, 61, 24, 21, a_fur, ang=-6, bias=0.1, group=2)
        p.blob(11.5, 58.5, 8.5, 7.5, a_fur, bias=0.04, group=3)
        p.blob(40, 33.5, 10.8, 10.0, a_fur, ang=6, bias=-0.06, group=4)
        p.limb(bez((47.5, 37), (50.5, 35), (53.5, 31.5)), 8.0, 7.2, a_muz, group=5)
        p.blob(34.4, 24.6, 4.8, 4.6, a_fur, group=6)
        if p.big:
            p.eye(45, 29, 3, 5, shine="white", shine_at=(2, 1))
            for x, y in ((40, 47), (35, 44), (30, 45), (25, 48), (24, 54), (16, 55), (15, 49)):
                p.px(x, y, "star")
        return

    if view == "down":
        # follower toddling toward the camera: big round head, both ears,
        # the crescent on the chest, feet stepping in turn
        st = phase
        p.limb([(28, 52), (27.5, 60 - 2 * st)], 6, 5.4, a_fur, group=12)
        p.limb([(36, 52), (36.5, 60 - 2 * (1 - st))], 6, 5.4, a_fur, group=13)
        p.blob(32, 49, 9, 8, a_fur, group=1)
        p.lens((25.5, 43.5), (38.5, 43.5), 3.2, a_mar, bend=2.6, group=2)
        p.limb([(24.5, 45), (22.5, 51 + st)], 4.6, 4.2, a_fur, group=14)
        p.limb([(39.5, 45), (41.5, 51 + (1 - st))], 4.6, 4.2, a_fur, group=15)
        for sx in (-1, 1):
            p.blob(32 + 8.5 * sx, 24, 4.0, 3.9, a_fur, group=5 + sx)
            p.blob(32 + 8.5 * sx, 24.6, 2.1, 2.0, a_muz, group=5 + sx)
        p.blob(32, 32, 10, 8.8, a_fur, group=3)
        p.blob(32, 36.5, 4.4, 3.4, a_muz, group=4)
        if p.big:
            p.eye(26, 30, 3, 4, shine="white", shine_at=(0, 1))
            p.eye(35, 30, 3, 4, shine="white", shine_at=(0, 1))
            p.pxs([(31, 35), (32, 35)], "pink0")
            p.pxs([(31, 38), (32, 38)], "fur1")
        else:
            p.pxs([(27, 31), (36, 31)], "ink")
        return

    if view == "up":
        # follower walking away: the round back with the seven stars, the
        # ears and a stub of a tail
        st = phase
        p.limb([(27.5, 54), (27, 60 - 2 * st)], 6.2, 5.6, a_fur, group=12)
        p.limb([(36.5, 54), (37, 60 - 2 * (1 - st))], 6.2, 5.6, a_fur, group=13)
        for sx in (-1, 1):
            p.blob(32 + 8.5 * sx, 25, 4.0, 3.9, a_fur, group=5 + sx)
        p.blob(32, 33, 10, 8.6, a_fur, group=3)
        p.blob(32, 49.5, 10, 9, a_fur, group=1)
        p.limb([(24.5, 44), (22.5, 51 + st)], 4.6, 4.2, a_fur, bias=0.1, group=14)
        p.limb([(39.5, 44), (41.5, 51 + (1 - st))], 4.6, 4.2, a_fur, bias=0.1, group=15)
        p.blob(32, 56.5, 2.4, 2.0, a_fur, group=16)
        if p.big:
            for x, y in ((29, 42), (32, 43), (34, 45), (35, 49), (31, 49), (30, 53), (36, 53)):
                p.px(x, y, "star")
        return


# --------------------------------------------------------------------------
# Starkos, the Great Bear
# --------------------------------------------------------------------------

STARKOS_COLORS = [
    ("ink", INK),
    # deep Aegean blue going to black-figure ink in the shadows
    ("fur0", (16, 24, 56)), ("fur1", (32, 48, 104)), ("fur2", (56, 80, 152)), ("fur3", (88, 120, 192)),
    ("fur4", (136, 168, 232)),
    # the marble crescent and claws
    ("mar0", (136, 136, 176)), ("mar1", (200, 200, 224)), ("white", C.white),
    # the seven stars, marble-white with a Fairy-pink glow
    ("star", (248, 248, 248)), ("pink0", (184, 80, 152)), ("pink1", (240, 144, 200)), ("pink2", (248, 208, 232)),
    # sun-gold eyes
    ("gold0", (200, 128, 40)), ("gold1", (248, 200, 72)),
]
STARKOS_SHINY = {
    "fur0": (8, 32, 24), "fur1": (16, 56, 40), "fur2": (32, 88, 56), "fur3": (56, 128, 80), "fur4": (104, 168, 112),
    "star": (248, 224, 112), "pink0": (176, 112, 32), "pink1": (232, 168, 56), "pink2": (248, 224, 144),
}

s_fur = Mat(["fur0", "fur1", "fur2", "fur3", "fur4"], line="fur0", cuts=[0.2, 0.42, 0.7, 0.92])
s_muz = Mat(["fur2", "fur3", "fur4"], line="fur1", cuts=[0.28, 0.66])
s_mar = Mat(["mar0", "mar1", "white"], line="mar0", cuts=[0.4, 0.7])
s_claw = Mat(["mar0", "mar1"], line="mar0", cuts=[0.5])


# the Great Bear's seven stars on the front view: the bowl on the back,
# the handle up the tail (Dubhe, Merak, Phecda, Megrez, Alioth, Mizar, Alkaid)
STARKOS_DIPPER = [(37, 23), (38, 32), (47, 33), (47, 25), (53, 24), (59, 15), (56, 7)]
# one massive body: hump, back, rump and barrel as a single form
STARKOS_BODY = [(17, 47), (15.5, 38), (17.5, 29), (20.5, 22), (25, 16.5), (30, 13), (36, 12), (41, 13.5),
                (45.5, 17.5), (49.5, 20.5), (54, 21), (58, 23.5), (60.5, 28.5), (61.5, 35), (60.5, 42), (57, 48),
                (51, 51.5), (44, 53), (36, 53.5), (28, 52.5), (21.5, 50.5)]
# the shaggy ruff along the hump, swept back
STARKOS_RUFF = [((20, 24), (22.5, 15.5), 4.2), ((24, 20), (28, 11.5), 4.8), ((29, 17), (33.5, 9.5), 5.0),
                ((34, 16), (39, 10), 4.8), ((39, 17), (44, 13), 4.2), ((43.5, 19.5), (48, 17.5), 3.4)]


def _sk_stars(p, pts, big=(0, 4, 6), lines=True):
    """Stars joined by faint lines of pink light; the bright ones sparkle."""
    if lines and p.big:
        for a, b in ((0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6)):
            p.stroke([pts[a], pts[b]], "pink0")
    for i, (x, y) in enumerate(pts):
        if p.big:
            p.pxs([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)], "pink2" if i in big else "pink1")
            if i in big:
                p.pxs([(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)], "pink1")
        p.px(x, y, "star")


def starkos(p, view, phase):
    if view in ("front", "side", "icon"):
        # one massive bear, weight thrown forward over thick forelegs, the
        # broad head low and roaring; the shaggy ruff on the hump, the long
        # Great-Bear tail tapering up into a tuft (the art files hand-finish
        # this)
        L = 1 if (phase == 1 and view == "front") else 0
        J = 4 if (phase == 1 and view == "front") else 1
        T = 1 if phase == 1 else 0
        st = view == "side" and phase == 1
        p.limb(bez((54, 25), (64, 17), (56.5 - T, 6)), 11.2, 3.8, s_fur, bias=-0.02, group=1)
        p.lens((57 - T, 8), (51 - 2 * T, 2.5), 5.4, s_fur, bend=1.6, bias=-0.04, group=1)
        p.limb([(57, 45), (58.5 - st, 51), (58 - st, 55.5)], 9.6, 7.6, s_fur, bias=0.32, group=2)
        p.blob(57.4 - st, 59, 4.2, 2.0, s_fur, bias=0.32, group=2)
        p.limb([(34, 46), (33 + st, 52), (32 + st, 55)], 11.6, 9.2, s_fur, bias=0.32, group=3)
        p.blob(31 + st, 59, 5.8, 2.0, s_fur, bias=0.32, group=3)
        p.poly(STARKOS_BODY, s_fur, bias=-0.02, group=4)
        for a, b, w in STARKOS_RUFF:
            p.lens(a, b, w, s_fur, bend=-0.9, bias=-0.1, group=4)
        p.blob(50.5, 41.5, 10.6, 11.2, s_fur, ang=-12, bias=-0.06, group=5)
        p.limb([(50.5, 48), (49.5 + st, 52), (48.5 + st, 54.5)], 13.2, 10, s_fur, group=5)
        p.blob(47 + st, 58.8, 7.6, 2.4, s_fur, group=6)
        p.limb([(26, 39), (23 - st, 49), (21 - st, 54)], 15.6, 11.2, s_fur, bias=-0.04, group=8)
        p.blob(18.8 - st, 58.6, 9.2, 2.6, s_fur, group=9)
        p.lens((24, 46.5), (38, 46), 3.4, s_mar, bend=3.0, group=7)
        p.blob(24.8, 18.6 - L, 3.3, 3.2, s_fur, bias=-0.04, group=10)
        p.poly([(3, 40.5 - L), (13.5, 41 - L), (13, 44 + J - L), (4.5, 43.5 + J - L)], Mat(["fur0"]), group=11)
        p.blob(9.5, 44 + J - L, 5.6, 2.6, s_muz, bias=0.06, group=12)
        p.blob(15.5, 31 - L, 11.4, 10.4, s_fur, bias=-0.06, group=13)
        p.blob(17.5, 39 - L, 9.6, 5.2, s_fur, bias=0.06, group=13)
        p.blob(9, 36.5 - L, 6.8, 4.8, s_muz, bias=-0.06, group=14)
        p.blob(5.8, 24.5 - L, 3.2, 3.1, s_fur, bias=-0.04, group=15)
        if p.big:
            p.patch(12, 27 - L, [".6666", "11111", "1ff91", ".1ee1"],
                    {"1": "ink", "6": "fur4", "f": "gold1", "e": "gold0", "9": "white"})
            p.patch(21, 26 - L, [".666", "1111", "1ff1", ".11"], {"1": "ink", "6": "fur4", "f": "gold1"})
            p.patch(1, 31 - L, ["..11111", ".1222221", "12622221", ".122221", "..1111"],
                    {"1": "ink", "2": "fur0", "6": "fur4"})
            p.pxs([(4, 40 - L), (10, 40 - L), (5, 43 + J - L), (9, 43 + J - L)], "white")
            p.pxs([(10, 59), (13, 59), (16, 59), (39, 59), (42, 59)], "mar1")
            _sk_stars(p, STARKOS_DIPPER, (1, 4, 5) if T else (0, 4, 6))
        else:
            p.px(13.5, 29 - L, "gold1")
            p.px(3, 33 - L, "ink")
            for x, y in STARKOS_DIPPER:
                p.px(x, y, "star")
        return

    if view == "back":
        # over the shoulder: the vast back with the full seven-star pattern
        # and the tail rising behind, the head in profile watching the foe
        p.limb(bez((11, 48), (0.5, 31), (8.5, 15)), 11.6, 3.8, s_fur, group=1)
        p.lens((8, 16.5), (15, 9.5), 5.6, s_fur, bend=-1.6, group=1)
        p.blob(49.5, 19.2, 3.2, 3.1, s_fur, bias=0.04, group=2)
        p.blob(29, 61, 28, 22, s_fur, ang=-4, bias=0.06, group=3)
        p.blob(36, 42, 17, 14, s_fur, ang=-18, bias=-0.04, group=3)
        for a, b, w in (((44, 31), (38, 24.5), 4.6), ((38, 31), (31, 25.5), 5.0), ((32, 33), (25, 28.5), 4.8),
                        ((26, 36), (19, 33), 4.4), ((20, 40), (14, 38.5), 4.0)):
            p.lens(a, b, w, s_fur, bend=0.8, bias=-0.08, group=3)
        p.poly([(49, 38.5), (59.5, 38), (58, 42.5), (50, 42)], Mat(["fur0"]), group=4)
        p.blob(53.5, 42.5, 5.4, 2.5, s_muz, bias=0.06, group=5)
        p.blob(45.5, 28.5, 11, 10, s_fur, bias=-0.06, group=6)
        p.blob(44, 37, 8.4, 4.8, s_fur, bias=0.06, group=6)
        p.blob(53.5, 34.5, 6.2, 4.6, s_muz, bias=-0.06, group=7)
        p.blob(38.5, 21, 3.4, 3.3, s_fur, bias=-0.04, group=8)
        if p.big:
            _sk_stars(p, [(33, 44), (31, 53), (20, 55), (19, 47), (11, 38), (6, 28), (10, 18)], (0, 4, 6))
            p.patch(46, 25, [".6666", "11111", "19ff1", ".1ee1"],
                    {"1": "ink", "6": "fur4", "f": "gold1", "e": "gold0", "9": "white"})
            p.patch(55, 30, [".1111", "122221", "122621", ".1111"], {"1": "ink", "2": "fur0", "6": "fur4"})
        return

    if view == "down":
        # follower lumbering toward the camera: the low head, the hump
        # behind it, the tail rising with its stars, forepaws stepping
        st = phase
        p.limb(bez((40, 30), (47, 22), (43, 12)), 7, 4.4, s_fur, bias=0.1, group=1)
        p.blob(32, 38, 16, 13, s_fur, bias=0.06, group=2)
        p.limb([(24, 46), (23, 60 - 2 * st)], 10, 9, s_fur, group=12)
        p.limb([(40, 46), (41, 60 - 2 * (1 - st))], 10, 9, s_fur, group=13)
        p.blob(23, 60 - 2 * st, 5.4, 2.4, s_fur, group=12)
        p.blob(41, 60 - 2 * (1 - st), 5.4, 2.4, s_fur, group=13)
        p.lens((24, 43), (40, 43), 3.4, s_mar, bend=3, group=3)
        for sx in (-1, 1):
            p.blob(32 + 8.5 * sx, 27, 3.8, 3.7, s_fur, group=5 + sx)
        p.blob(32, 35, 10, 8.6, s_fur, group=4)
        p.blob(32, 40, 5.4, 4.2, s_muz, group=8)
        if p.big:
            p.eye(26, 33, 3, 3, iris="gold1", shine="white", shine_at=(1, 0))
            p.eye(35, 33, 3, 3, iris="gold1", shine="white", shine_at=(1, 0))
            p.pxs([(31, 39), (32, 39), (31, 38), (32, 38)], "fur0")
            for x, y in ((43, 13), (45, 19), (44, 25)):
                p.px(x, y, "star")
        else:
            p.pxs([(27.5, 34), (36.5, 34)], "gold1")
        return

    if view == "up":
        # follower walking away: the broad back carrying the whole Great
        # Bear, the tail held high, hind legs stepping
        st = phase
        p.limb([(24, 48), (23, 60 - 2 * st)], 10, 9, s_fur, group=12)
        p.limb([(40, 48), (41, 60 - 2 * (1 - st))], 10, 9, s_fur, group=13)
        for sx in (-1, 1):
            p.blob(32 + 8 * sx, 22, 3.6, 3.5, s_fur, group=5 + sx)
        p.blob(32, 28, 9, 7.6, s_fur, group=4)
        p.blob(32, 42, 16, 13, s_fur, group=2)
        p.limb(bez((32, 42), (40, 32), (34, 18)), 7.4, 4.6, s_fur, group=1)
        if p.big:
            _sk_stars(p, [(26, 42), (25, 49), (33, 50), (33, 43), (37, 36), (36, 28), (34, 20)], (0, 4, 6))
        return


MONS = [
    # icon palette 3 keeps the blue a blue
    Mon("Arkoby", ARKOBY_COLORS, ARKOBY_SHINY, arkoby, foot="paw", icon_pal=3),
    Mon("Starkos", STARKOS_COLORS, STARKOS_SHINY, starkos, foot="bigpaw", icon_pal=3),
]
