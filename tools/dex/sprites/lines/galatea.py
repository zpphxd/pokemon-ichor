"""Galatea line: Glyphlet, Kalliglyph (Rock, then Rock/Fairy). Pygmalion's
statue, carved from a single chip and warmed into life by love."""
from mon_lib import C, Mat, Mon, bez, bez3, lens_pts, _fp

INK = C.ink

# --------------------------------------------------------------------------
# Glyphlet, the marble chip
# --------------------------------------------------------------------------

GLYPHLET_COLORS = [
    ("ink", INK),
    # temple marble, cool in shadow
    ("mb0", (104, 96, 112)), ("mb1", (152, 144, 152)), ("mb2", (200, 192, 192)), ("mb3", (232, 224, 216)),
    ("white", C.white),
    # faint limestone veins
    ("vn0", (176, 152, 120)), ("vn1", (216, 200, 168)),
    # the carved eye's sun-gold glint
    ("gd0", (192, 128, 40)), ("gd1", (240, 200, 72)),
]
GLYPHLET_SHINY = {
    # rose-pink marble veined with sun-gold
    "mb0": (152, 80, 104), "mb1": (200, 128, 152), "mb2": (232, 176, 184), "mb3": (248, 208, 208),
    "white": (248, 232, 232), "vn0": (200, 136, 40), "vn1": (240, 192, 72),
}

g_mb = Mat(["mb0", "mb1", "mb2", "mb3", "white"], line="mb0", cuts=[0.18, 0.38, 0.6, 0.8])
g_ft = Mat(["mb0", "mb1", "mb2"], line="mb0", cuts=[0.4, 0.7])


def _almond(p, x, y, w, h, L=0):
    """Glyphlet's carved eye, its left corner at (x, y): an almond of white
    marble under a carved lid, a big dark iris with a gold glint and a
    shine. Hand-placed at battle size."""
    if p.big:
        p.patch(x, y - L, [
            "...11111....",
            ".111666511..",
            "116611115611",
            "16661111cb661",
            ".1661111bc61.",
            "..1166666611.",
            "....111111...",
        ][:h + 3], {"1": "ink", "6": "white", "5": "mb3", "b": "gd1", "c": "gd0"})
    else:
        p.px(x + 4, y + 2 - L, "ink")
        p.px(x + 5, y + 2 - L, "ink")


def glyphlet(p, view, phase):
    if view in ("front", "icon", "side", "down"):
        hop = 1 if (phase == 1 and view in ("front", "side", "down")) else 0
        L = hop
        # two chipped corners for feet
        p.poly([(22, 56 - L), (27.5, 55 - L), (29, 59.5), (22.5, 60)], g_ft, group=2)
        p.poly([(37, 56 - L), (42.5, 55.5 - L), (43, 59), (37.5, 59.6)], g_ft, bias=0.2, group=3)
        # the chunk: a rounded block with chisel-cut planes
        body = p.poly([(18.4, 47 - L), (19.4, 42.6 - L), (22.5, 39 - L), (27, 36.6 - L), (32.5, 35.8 - L),
                       (38, 36.6 - L), (42.6, 39 - L), (45.6, 42.6 - L), (46.8, 47.4 - L), (46.2, 52.2 - L),
                       (43.8, 55.8 - L), (39.5, 57.8 - L), (32, 58.6 - L), (25, 58.2 - L), (20.8, 55.8 - L),
                       (18.8, 51.8 - L)], g_mb, group=1)
        if view != "down":
            # chisel-cut facets: a lit cut on the brow, a shadowed one on the flank
            p.poly([(22.5, 39 - L), (27, 36.6 - L), (32.5, 35.8 - L), (34.5, 38.6 - L), (29, 41.4 - L), (22.6, 42 - L)],
                   g_mb, clip=[body], flat=4, group=4)
            p.poly([(42.6, 39 - L), (45.6, 42.6 - L), (46.8, 47.4 - L), (46.2, 52.2 - L), (43.6, 53.6 - L),
                    (41.2, 47.6 - L), (40.6, 42.4 - L)], g_mb, clip=[body], flat=1, group=5)
        if p.big:
            if view == "down":
                _almond(p, 26, 44, 12, 4, L)
            else:
                _almond(p, 22, 44, 12, 4, L)
            # chisel marks around the eye
            for (x0, y0), (x1, y1) in (((21, 52), (23, 54)), ((36, 44), (37, 46)), ((34, 53), (36, 55))):
                p.stroke([(x0, y0 - L), (x1, y1 - L)], "mb1")
            # faint limestone veins
            p.stroke([(31, 37 - L), (33, 39 - L), (32, 41 - L)], "vn1")
            p.stroke([(41, 47 - L), (43, 50 - L)], "vn0")
        else:
            p.px(27, 47 - L, "ink")
        return

    if view == "back":
        # the chip from behind, a little closer: the rough back of the
        # block, chisel scars, the eye just visible on the turned face
        p.poly([(10, 64), (9, 50), (13, 40), (21, 33), (31, 30), (41, 31), (50, 36), (55, 44), (56, 54), (54, 64)],
               g_mb, group=1)
        p.poly([(13, 40), (21, 33), (31, 30), (41, 31), (45, 36), (33, 38), (20, 41)], g_mb, bias=-0.16, group=1)
        if p.big:
            for (x0, y0), (x1, y1) in (((18, 48), (21, 52)), ((26, 44), (28, 47)), ((33, 52), (36, 56)),
                                       ((40, 45), (42, 48)), ((22, 56), (24, 60))):
                p.stroke([(x0, y0), (x1, y1)], "mb1")
            p.stroke([(30, 31), (33, 35), (31, 39), (34, 43)], "vn1")
            p.patch(49, 42, ["1111", "6611", "1bc1", "6611"], {"1": "ink", "6": "white", "b": "gd1", "c": "gd0"})
        return

    if view == "up":
        p.poly([(22, 56), (27.5, 55), (29, 59.5), (22.5, 60)], g_ft, group=2)
        p.poly([(37, 56), (42.5, 55.5), (43, 59), (37.5, 59.6)], g_ft, group=3)
        p.poly([(18.5, 47), (20, 41), (24.5, 37.5), (31, 36), (38.5, 37), (44, 40.5), (46, 46.5),
                (45.5, 52), (42, 56.5), (35, 58.5), (26, 58.5), (20.5, 55.5)], g_mb, group=1)
        if p.big:
            p.stroke([(28, 44 - phase), (30, 47 - phase)], "mb1")
            p.stroke([(36, 49 - phase), (38, 52 - phase)], "mb1")
        return


# --------------------------------------------------------------------------
# Kalliglyph, the living statue
# --------------------------------------------------------------------------

KALLIGLYPH_COLORS = [
    ("ink", INK),
    ("mb0", (88, 80, 104)), ("mb1", (144, 136, 152)), ("mb2", (192, 184, 192)), ("mb3", (224, 216, 216)),
    ("white", C.white),
    # the warm glow that spreads round the cracks
    ("glow", (248, 216, 168)),
    # sun-gold light in the cracks and eyes, bright at the core
    ("gl0", (216, 120, 32)), ("gl1", (248, 184, 56)), ("gl2", (248, 240, 168)),
    # rose blush where love has warmed the stone
    ("pink", (224, 88, 128)), ("rose", (240, 168, 184)),
    # the painted meander and fillet, bold Aegean blue
    ("bl0", (40, 72, 152)), ("bl1", (88, 136, 208)),
]
KALLIGLYPH_SHINY = {
    "mb0": (136, 72, 96), "mb1": (192, 120, 144), "mb2": (224, 168, 184), "mb3": (240, 200, 208),
    "white": (248, 232, 232),
}

k_mb = Mat(["mb0", "mb1", "mb2", "mb3", "white"], line="mb0", cuts=[0.34, 0.5, 0.66, 0.8])
k_robe = Mat(["mb0", "mb1", "mb2", "mb3", "white"], line="mb0", cuts=[0.36, 0.52, 0.68, 0.82])
k_hair = Mat(["mb0", "mb1", "mb2", "mb3", "white"], line="mb1", cuts=[0.36, 0.52, 0.68, 0.82])


MANTLE = [(33, 19.5), (38.5, 20.6), (43.6, 25.6), (47.4, 33), (50.4, 42), (53.4, 51), (55.8, 59.4), (52, 61),
          (45, 61), (41, 54), (38.4, 42), (36, 30)]
SKIRT = [(25, 32), (36.6, 32), (38.4, 38), (39.6, 46), (41.6, 53), (44.4, 59.4), (42, 60.6), (17.4, 60.6),
         (18.6, 55), (19.4, 49), (20.4, 45), (22, 40)]
WRAP = [(21.4, 39.6), (26, 35.4), (32, 33), (37.4, 32.4), (39.2, 36.2), (35, 38.4), (28.4, 41.6), (22.6, 44.2)]
HAIR = [(20.6, 10.4), (21, 6.6), (23.4, 3.4), (27, 2.0), (31, 2.6), (34, 4.8), (35.6, 8.4), (35.4, 12.6),
        (34, 16.4), (32, 16.8), (31.6, 12.6), (30.4, 9), (28.4, 7.2), (25.6, 6.6), (23.2, 7.4), (21.8, 10.4)]


def _sparkle(p, x, y):
    p.px(x, y, "gl2")
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        p.px(x + dx, y + dy, "gl1")


def kalliglyph(p, view, phase):
    """The battle sprites are hand-finished in art/kalliglyph_*.txt; this
    draft gives the follower, the icon and the art's starting shapes."""
    if view in ("front", "side"):
        L = 1 if (phase == 1 and view == "front") else 0
        # the himation's back fall, the hanging arm, the fluted chiton
        p.poly(MANTLE, k_robe, bias=0.12, group=30)
        p.limb([(35.6, 23.4), (38.4, 30.6), (40.4, 37.4)], 4.6, 3.8, k_mb, group=20)
        p.circle(41.2, 39.4, 2.4, k_mb, group=20)
        skirt = p.poly(SKIRT, k_robe, group=31)
        p.blob(23.4, 46.6, 3.4, 4.6, k_robe, ang=-10, clip=[skirt], bias=-0.15, group=33)
        p.limb([(29.6, 21.6), (30, 27), (30.6, 33)], 11, 9.4, k_mb, group=1)
        p.poly(WRAP, k_robe, bias=-0.05, group=32)
        # neck, chignon, head and carved hair
        p.limb([(29, 16.4), (29.8, 21.6)], 4.4, 5.0, k_mb, bias=0.1, group=1)
        p.circle(38, 9.8, 4.5, k_hair, group=6)
        p.blob(27.6, 11.6, 7.0, 7.4, k_mb, group=5)
        p.blob(25.4, 15.2, 4.4, 3.6, k_mb, group=5)
        p.poly(HAIR, k_hair, bias=-0.1, group=7)
        # the far arm raised, the hand at her cheek
        p.limb([(24.4, 23.4), (19.6, 29.4)], 4.4, 4.0, k_mb, group=21)
        p.limb([(19.6, 29.4), (19.4, 22.4 - L), (20.4, 17.8 - L)], 4.0, 3.4, k_mb, group=21)
        p.circle(20.8, 16.4 - L, 2.4, k_mb, group=21)
        if p.big:
            p.eye(21, 10, 3, 5, iris="gl2", pupil="gl1", shine="white")
            p.eye(26, 10, 4, 5, iris="gl2", pupil="gl1", shine="white")
            p.patch(24, 7, [".11.", "1a91", ".11."], {"1": "ink", "a": "gl2", "9": "gl1"})
            p.stroke([(31, 25), (33, 27), (32, 29)], "gl1")
            p.stroke([(23, 43), (37, 36)], "bl0")
        else:
            p.px(22, 12, "gl1")
            p.px(27.5, 12, "gl1")
            p.px(32, 27, "gl1")
            p.stroke([(24, 42), (37, 36)], "bl0")
        return

    if view == "icon":
        # party icon: a big head over the fluted robe, gold eyes, the hand
        # lifted to her cheek
        p.poly([(22, 33), (40, 33), (44, 46), (48, 56), (16, 56), (19, 46)], k_robe, group=31)
        p.poly([(38, 30), (46, 36), (50, 48), (52, 56), (44, 56), (40, 44)], k_robe, bias=0.15, group=30)
        p.limb([(32, 26), (32, 34)], 9, 9, k_mb, group=1)
        p.circle(42, 13, 5.6, k_hair, group=6)
        p.blob(31, 17, 10, 10.2, k_mb, group=5)
        p.poly([(21, 15), (22, 9), (27, 5), (33, 4.4), (39, 6.6), (41.6, 12), (41, 19), (38, 22), (37, 16),
                (34, 11.6), (29, 10.4), (24.6, 12), (22.6, 16)], k_hair, group=7)
        p.limb([(24, 33), (17.6, 27), (19.6, 20)], 5, 4, k_mb, group=21)
        p.circle(20.4, 19, 3.2, k_mb, group=21)
        p.eye(23.5, 13, 3, 5, pupil="gl1")
        p.eye(29.5, 13, 3, 5, pupil="gl1")
        p.px(27.5, 10.5, "gl2")
        p.stroke([(19, 45), (44, 42)], "bl0")
        return

    if view == "back":
        p.blob(32, 60, 16, 14, k_robe, group=30)
        p.limb([(36, 56), (37, 40)], 13, 11, k_mb, group=1)
        p.blob(40, 24, 9, 9, k_mb, group=5)
        p.blob(34, 20, 8, 8, k_hair, group=6)
        if p.big:
            p.eye(44, 21, 3, 5, iris="gl1", shine="white", shine_at=(1, 1))
        return

    if view in ("down", "up"):
        # follower: the statue walking toward or away from the camera, stiff
        # at first; the robe's hem swings from side to side
        st = phase
        dn = view == "down"
        sw = 1 if st else -1
        p.poly([(25, 30), (39, 30), (41, 42), (44 + sw, 58), (20 + sw, 58), (23, 42)], k_robe, group=31)
        if dn:
            p.limb([(37.6, 24), (41, 32), (41.6, 39)], 3.8, 3.2, k_mb, group=20)
            p.circle(41.6, 40, 2.0, k_mb, group=20)
        else:
            p.poly([(26, 22), (38, 22), (42, 34), (44 + sw, 56), (21 + sw, 56), (23, 34)], k_robe, bias=0.1, group=33)
        p.limb([(32, 19), (32, 31)], 11, 9.6, k_mb, group=1)
        p.poly([(22.6, 38), (32, 34.6), (41.4, 38), (41, 40.4), (32, 37), (23, 40.4)], k_robe, bias=-0.06, group=32)
        p.limb([(26.4, 23), (22.6, 29), (24, 16.6)], 3.6, 3.0, k_mb, group=21)
        if dn:
            p.circle(32, 4.6, 3.8, k_hair, group=6)
            p.blob(32, 12, 7.0, 7.4, k_mb, group=5)
            p.poly([(25, 11), (25.6, 6.4), (29, 4.2), (35, 4.2), (38.4, 6.4), (39, 11), (37.6, 8.4), (32, 7),
                    (26.4, 8.4)], k_hair, group=7)
            p.circle(24.6, 15.4, 2.2, k_mb, group=22)
            p.eye(27.5, 10, 3, 5, iris="gl2", pupil="gl1", shine="white")
            p.eye(33.5, 10, 3, 5, iris="gl2", pupil="gl1", shine="white")
            p.px(31.5, 7.6, "gl2")
            p.stroke([(23, 39), (41, 39)], "bl0")
        else:
            p.blob(32, 12, 7.0, 7.4, k_hair, group=5)
            p.circle(32, 14.6, 4.0, k_hair, group=6)
            p.stroke([(25, 8), (39, 8)], "bl0")
            p.circle(24.6, 15.4, 2.2, k_mb, group=22)
        return


# a statue's slender bare foot
KALLIGLYPH_FOOT = [
    "", "",
    ".......#.#......",
    "................",
    "................",
    "................",
    ".......####.....",
    ".......####.....",
    ".......###......",
    ".......###......",
    "........##......",
]

MONS = [
    Mon("Glyphlet", GLYPHLET_COLORS, GLYPHLET_SHINY, glyphlet, foot="blank"),
    Mon("Kalliglyph", KALLIGLYPH_COLORS, KALLIGLYPH_SHINY, kalliglyph, foot=_fp(KALLIGLYPH_FOOT), icon_pal=0),
]
