#!/usr/bin/env python3
"""64x64 trainer front pics for the Olympiad's five Brains and Olympias
(design/POSTGAME.md §3.1, design/LABORS.md §1, design/postgame/SPRITES.md).

Usage:
    python3 tools/ichor/art/sprites_pg_portraits.py [NAME ...] [--write] [--preview DIR] [--pass N]

--write    writes graphics/trainers/front_pics/ichor_pg_<name>.png (64x64,
           4bpp indexed, color 0 transparent; the palette is read from the PNG)
--preview  writes DIR/pg_portraits_pass<N>.png, every portrait at 4x for
           passes 1-3, and DIR/pg_<name>_x8.png of the last pass
--pass N   paints only up to pass N (default 3, the shipped art)

Each portrait is painted in three passes, kept in the code so the progress
can be re-rendered:

    pass 1  blocking: flat masses for hair, face, body, clothes and props, and
            the silhouette line
    pass 2  form: shading clipped to each material, and the features (brows,
            eyes, nose, mouth, beard)
    pass 3  finish: expression, highlights, locks and folds, the details that
            say who they are

The figures are cut at the knee, as Emerald's Frontier Brains are, so the
faces have room. Each has its own 16-color palette, embedded in the PNG. Light
comes from the upper left, as on every Ichor portrait.
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, save_indexed, to_rgba, upscale  # noqa: E402
from portraits_theoxenia import Canvas, legend_of, palette_of  # noqa: E402

FRONT = os.path.join(ROOT, "graphics/trainers/front_pics")


def skin(l, m, d, dd):
    return [("S", "skin_l", l), ("m", "skin_m", m), ("d", "skin_d", d), ("D", "skin_dd", dd)]


SKINS = ["skin_l", "skin_m", "skin_d", "skin_dd"]


def new(colors):
    assert len(colors) <= 15, len(colors)
    pal = palette_of(colors)
    return Canvas(pal, legend_of(colors)), pal


def shade_face(c, face_box, right_side, jaw):
    """Light from the upper left: a lit oval, the far cheek and the jaw in shade."""
    c.ellipse(face_box, "skin_l", clip=["skin_m"])
    c.poly(right_side, "skin_d", clip=["skin_m", "skin_l"])
    c.poly(jaw, "skin_d", clip=["skin_m", "skin_l"])


# ==========================================================================
# Achilles: swift-footed, restless, young, bronze-haired, unexpectedly funny
# ==========================================================================

ACHILLES_COLORS = [("k", "ink", (40, 24, 24))] + skin(
    (248, 216, 184), (232, 176, 136), (200, 128, 96), (136, 80, 64)) + [
    ("Y", "hair_l", (248, 224, 128)),
    ("y", "hair_m", (224, 160, 64)),
    ("h", "hair_d", (152, 96, 40)),
    ("W", "white", (248, 248, 232)),
    ("w", "white_d", (192, 184, 168)),
    ("G", "cloak", (96, 168, 112)),
    ("g", "cloak_d", (40, 96, 72)),
    ("t", "ash", (184, 136, 88)),
    ("T", "ash_d", (112, 72, 48)),
    ("r", "lip", (208, 96, 80)),
]


def achilles(npass=3):
    c, pal = new(ACHILLES_COLORS)
    hair = ["hair_m", "hair_l", "hair_d"]
    # ---- pass 1: masses
    # the sea-green chlamys behind him, flaring out to his left as he turns
    c.poly([(40, 28), (50, 29), (57, 38), (62, 50), (63, 63), (44, 63), (46, 50), (45, 37)], "cloak")
    # legs apart, cut at the knee
    c.poly([(24, 55), (31, 55), (31, 63), (24, 63)], "skin_m")
    c.poly([(34, 55), (41, 55), (42, 63), (35, 63)], "skin_m")
    # the short chiton, girt high
    c.poly([(21, 30), (43, 30), (44, 44), (45, 57), (20, 57), (21, 44)], "white")
    # his left arm, hand on the hip, elbow out
    c.poly([(42, 30), (47, 32), (52, 39), (50, 43), (45, 46), (42, 47), (41, 43), (46, 40), (44, 35)], "skin_m")
    # his right arm down to the spear
    c.poly([(22, 30), (18, 33), (15, 38), (14, 41), (18, 42), (19, 38), (22, 35)], "skin_m")
    # the ash spear the length of the frame, a bronze leaf at its tip
    c.poly([(11, 9), (13, 9), (13, 63), (11, 63)], "ash")
    c.poly([(12, 0), (14, 3), (14, 7), (12, 9), (10, 7), (10, 3)], "hair_m")
    c.ellipse((9, 37, 17, 44), "skin_m")
    # neck, the chlamys over his right shoulder
    c.poly([(29, 23), (36, 23), (37, 31), (28, 31)], "skin_m")
    c.poly([(19, 30), (28, 28), (30, 31), (23, 35), (19, 35)], "cloak")
    # ears, face
    c.ellipse((21, 13, 25, 21), "skin_m")
    c.ellipse((40, 13, 44, 21), "skin_m")
    c.poly([(24, 8), (40, 8), (41, 13), (41, 19), (39, 24), (35, 27), (30, 27), (26, 24), (24, 19), (23, 13)],
           "skin_m")
    # hair: long bronze locks to the jaw, loose and wavy
    c.poly([(21, 21), (20, 12), (22, 6), (26, 2), (32, 1), (38, 2), (42, 5), (44, 10), (44, 18), (43, 25),
            (41, 28), (40, 22), (41, 15), (39, 11), (36, 9), (33, 10), (30, 9), (27, 10), (25, 13), (24, 18),
            (24, 24), (22, 28), (20, 25)], "hair_m")
    # the gold belt
    c.poly([(21, 43), (44, 43), (44, 45), (21, 45)], "hair_m")
    if npass >= 2:
        # ---- pass 2: form
        shade_face(c, (24, 9, 37, 24),
                   [(37, 10), (41, 13), (41, 19), (39, 24), (35, 27), (34, 25), (38, 19)],
                   [(28, 24), (37, 24), (36, 27), (29, 27)])
        c.poly([(28, 26), (37, 26), (37, 30), (28, 29)], "skin_d", clip=["skin_m"])
        c.poly([(24, 56), (27, 56), (27, 63), (24, 63)], "skin_l", clip=["skin_m"])
        c.poly([(34, 56), (37, 56), (37, 63), (34, 63)], "skin_l", clip=["skin_m"])
        c.poly([(29, 56), (31, 56), (31, 63), (29, 63)], "skin_d", clip=["skin_m"])
        c.poly([(39, 56), (42, 56), (42, 63), (40, 63)], "skin_d", clip=["skin_m"])
        c.poly([(18, 33), (21, 31), (18, 39), (16, 39)], "skin_l", clip=["skin_m"])
        c.poly([(46, 33), (51, 39), (50, 42), (47, 39)], "skin_d", clip=["skin_m"])
        # chiton: shade on the right, folds falling from the belt
        c.poly([(39, 30), (43, 30), (44, 43), (40, 43)], "white_d", clip=["white"])
        c.poly([(39, 46), (45, 46), (45, 57), (40, 57)], "white_d", clip=["white"])
        c.line([(38, 33), (37, 42)], "white_d", clip=["white"])
        c.line([(27, 46), (25, 56)], "white_d", clip=["white"])
        c.line([(32, 47), (32, 56)], "white_d", clip=["white"])
        c.line([(29, 34), (33, 42)], "white_d", clip=["white"])
        # the cloak in shade where it falls behind him
        c.poly([(45, 37), (53, 39), (60, 52), (63, 63), (50, 63), (47, 50)], "cloak_d", clip=["cloak"])
        c.poly([(23, 33), (30, 31), (28, 35)], "cloak_d", clip=["cloak"])
        # the spear's shade and the leaf's midrib
        c.line([(13, 9), (13, 63)], "ash_d", clip=["ash"])
        c.line([(12, 1), (12, 8)], "hair_l", clip=["hair_m"])
        c.line([(13, 3), (13, 7)], "hair_d", clip=["hair_m"])
        # hair: lit to the upper left, dark where it parts and falls behind
        c.poly([(22, 7), (27, 3), (32, 2), (30, 5), (25, 10), (22, 16)], "hair_l", clip=hair)
        c.poly([(38, 4), (43, 9), (44, 18), (43, 25), (41, 26), (41, 15), (40, 10)], "hair_d", clip=hair)
        c.poly([(20, 19), (24, 18), (24, 25), (21, 25)], "hair_d", clip=hair)
        c.line([(21, 43), (35, 43)], "hair_l", clip=["hair_m"])
        c.line([(36, 45), (44, 45)], "hair_d", clip=["hair_m"])
        c.patch(21, 30, ["kYk", "Yyh", "khk"])
        c.outline("ink")
        c.seam(hair, ["skin_m", "skin_l", "skin_d"], "ink")
        # brows, his left one cocked; bright green eyes; a lopsided grin
        c.patch(25, 11, [
            "..........hhh..",
            ".hhhhh...h...h.",
            "...............",
            ".kkkk.....kkkk.",
            "kWWgk.....kgWWk",
            ".mddm.....mddm.",
        ])
        c.patch(31, 18, ["md", "md", "Smd", "dD."])
        c.patch(28, 21, [
            "......kD",
            "Dkkkkk..",
            ".dWWWd..",
            "..dDd...",
        ])
    if npass >= 3:
        # ---- pass 3: finish
        # locks over the brow and loose at the cheeks, lit at their tips
        for x, y in ((27, 9), (31, 8), (35, 9)):
            c.patch(x - 1, y - 1, [".h.", "hyY", ".hk"], clip=hair + ["skin_m", "skin_l"])
        c.patch(21, 22, ["hY", "yh", "hk"], clip=hair + ["ink"])
        c.patch(42, 22, ["Yh", "hy", "kh"], clip=hair + ["ink"])
        c.patch(23, 3, ["Y", ".Y"], clip=hair)
        # the grin's dimple, high on his cheek
        c.patch(37, 21, ["d"], clip=["skin_m", "skin_l", "skin_d"])
        # knuckles on the shaft, the hand on his hip
        c.patch(9, 38, ["kmmmmmk", "mSSSmdk", "mmmmddk", "kdddddk"], clip=SKINS + ["ink", "ash", "ash_d"])
        c.patch(42, 43, ["kmmd", "mSmd", "kddk"], clip=SKINS + ["white", "white_d", "ink", "hair_m", "hair_d"])
        # the cloak's lit edge where the wind lifts it
        c.line([(57, 38), (62, 50)], "cloak", clip=["cloak_d"])
        c.line([(49, 30), (55, 36)], "cloak", clip=["cloak", "cloak_d"])
        # knees, and sandal straps at the frame's foot
        c.patch(26, 61, ["dd"], clip=["skin_l", "skin_m"])
        c.patch(37, 61, ["dd"], clip=["skin_l", "skin_m"])
    return c, pal


# ==========================================================================
# Odysseus: broad, gray-bearded, clever eyes, a traveler's pilos; Homer's
# purple cloak with its gold brooch (Odyssey 19.225), and the wooden horse
# he keeps as the Horse's Brain
# ==========================================================================

ODYSSEUS_COLORS = [("k", "ink", (40, 24, 32))] + skin(
    (240, 200, 168), (216, 160, 120), (176, 112, 80), (120, 72, 56)) + [
    ("G", "gray_l", (232, 232, 224)),
    ("g", "gray", (168, 168, 160)),
    ("q", "gray_d", (104, 104, 112)),
    ("F", "felt", (184, 128, 72)),
    ("f", "felt_d", (112, 72, 48)),
    ("P", "purple", (144, 80, 152)),
    ("p", "purple_d", (80, 40, 96)),
    ("O", "gold", (248, 208, 96)),
    ("o", "gold_d", (176, 120, 48)),
    ("L", "linen", (232, 224, 200)),
]


def odysseus(npass=3):
    c, pal = new(ODYSSEUS_COLORS)
    gray = ["gray", "gray_l", "gray_d"]
    # ---- pass 1
    # the purple cloak over both broad shoulders
    c.poly([(14, 30), (50, 30), (56, 40), (59, 63), (5, 63), (8, 40)], "purple")
    # the linen tunic where the cloak parts
    c.poly([(26, 32), (39, 32), (42, 63), (23, 63)], "linen")
    c.poly([(24, 48), (41, 48), (41, 50), (24, 50)], "felt_d")
    # his right forearm out of the cloak, and the little wooden horse in his hand
    c.poly([(12, 44), (20, 41), (24, 45), (24, 49), (16, 51), (11, 50)], "skin_m")
    HORSE = [
        "........kk...",
        ".......kFFk..",
        "......kFFkFk.",
        "......kFFFfk.",
        ".....kFFk.k..",
        "kk..kFFFk....",
        "kFkkFFFFFFk..",
        ".kFOOOOOFFFk.",
        "..kFFFFFFFfk.",
        "..kfffffffk..",
        "..kfk...kfk..",
        ".kfffffffffk.",
        "..kOk...kOk..",
        "...k.....k...",
    ]
    # neck, ears, the broad face
    c.poly([(27, 24), (37, 24), (38, 32), (26, 32)], "skin_m")
    c.ellipse((19, 13, 24, 21), "skin_m")
    c.ellipse((40, 13, 45, 21), "skin_m")
    c.poly([(23, 9), (41, 9), (42, 14), (42, 20), (40, 25), (32, 28), (24, 25), (22, 20), (22, 14)], "skin_m")
    # gray at the temples, the short curled beard and the mustache
    c.poly([(20, 11), (24, 11), (24, 18), (21, 18)], "gray")
    c.poly([(40, 11), (44, 11), (43, 18), (40, 18)], "gray")
    c.poly([(22, 17), (24, 22), (27, 27), (31, 31), (34, 31), (38, 27), (41, 22), (42, 17), (43, 21), (41, 28),
            (36, 33), (29, 33), (24, 29), (21, 22)], "gray")
    c.poly([(23, 20), (41, 20), (40, 25), (36, 28), (29, 28), (24, 25)], "gray")
    c.poly([(27, 21), (37, 21), (37, 23), (27, 23)], "gray")
    # the pilos: a felt cone with a rolled brim
    c.poly([(32, 0), (39, 4), (43, 10), (21, 10), (25, 4)], "felt")
    c.poly([(19, 9), (45, 9), (46, 12), (18, 12)], "felt_d")
    # the gold brooch at his right shoulder
    c.ellipse((25, 32, 31, 38), "gold")
    if npass >= 2:
        shade_face(c, (23, 10, 37, 24),
                   [(37, 10), (42, 14), (42, 20), (40, 22), (38, 18)], [(30, 26), (34, 26), (33, 28), (31, 28)])
        c.poly([(26, 24), (38, 24), (38, 32), (26, 32)], "skin_d", clip=["skin_m"])
        # the cloak's folds and shade; its gold border
        c.poly([(40, 30), (50, 30), (56, 40), (59, 63), (44, 63), (42, 40)], "purple_d", clip=["purple"])
        c.line([(14, 52), (12, 63)], "purple_d", clip=["purple"])
        c.line([(20, 50), (19, 63)], "purple_d", clip=["purple"])
        c.line([(9, 40), (14, 31)], "gold_d", clip=["purple"])
        c.line([(23, 63), (25, 34)], "gold_d", clip=["purple", "linen"])
        c.poly([(35, 32), (39, 32), (42, 63), (37, 63)], "gray_l", clip=["linen"])
        c.line([(32, 51), (32, 63)], "gray", clip=["linen", "gray_l"])
        # the hand under it
        c.poly([(12, 46), (20, 43), (21, 45), (14, 49)], "skin_l", clip=["skin_m"])
        # beard: curls lit on the left, dark under the chin
        c.poly([(22, 17), (27, 26), (30, 30), (27, 30), (23, 25)], "gray_l", clip=gray)
        c.poly([(33, 28), (40, 24), (42, 20), (41, 27), (36, 32), (31, 32)], "gray_d", clip=gray)
        c.poly([(40, 11), (44, 11), (43, 18), (41, 18)], "gray_d", clip=gray)
        # the pilos's shade, the brim's lit roll
        c.poly([(33, 1), (39, 4), (43, 10), (36, 10)], "felt_d", clip=["felt"])
        c.line([(19, 10), (36, 10)], "felt", clip=["felt_d"])
        # the brooch: a hound and a fawn are too small to see; a gold ring
        c.patch(25, 32, [".OOOo.", "OGOOOo", "OOooOo", "OOookf", ".ooff."], clip=["gold"])
        c.outline("ink")
        c.seam(["felt", "felt_d"], SKINS + gray, "ink")
        c.seam(gray, ["skin_m", "skin_l", "skin_d"], "gray_d")
        # one brow up, eyes narrowed with a glint, bags of long years
        c.patch(24, 12, [
            "...........qqq...",
            ".qqqq.....q...q..",
            "..........qqqq...",
            ".kkkk......kkk...",
            "kmGqk.....kqGk...",
            ".dddm.....mddd...",
        ])
        c.patch(31, 18, ["md", "md", "Smd", "SmdD", "Dkd"])
        # the mustache over a wry, one-sided smile
        c.patch(26, 22, [
            "..ggGGggggq.",
            ".qgGGgqqggqq",
            "..q.kkkkkD..",
            "....qggq.D..",
        ])
    if npass >= 3:
        # curls in the beard and at the temples
        for x, y in ((24, 25), (30, 30), (37, 27)):
            c.patch(x, y, ["Gg", "gq"], clip=gray)
        # the cap's seam, a weathered brow line, crow's feet
        c.line([(32, 1), (32, 9)], "felt_d", clip=["felt"])
        c.patch(26, 10, ["d.......d"], clip=SKINS)
        c.patch(22, 16, ["d"], clip=SKINS)
        c.patch(39, 16, ["D"], clip=SKINS)
        # knuckles under the horse, the horse's eye and mane
        c.patch(13, 43, ["kmk.mk"], clip=SKINS + ["felt", "felt_d", "ink"])
        pass
        # the brooch's pin glint, the cloak's lit shoulder
        c.patch(26, 33, ["G"], clip=["gold", "gray_l"])
        c.line([(15, 31), (24, 31)], "purple", clip=["purple", "purple_d"])
        c.line([(9, 39), (14, 32)], "gold", clip=["gold_d"])
    if npass >= 1:
        c.patch(10, 28, HORSE if npass >= 2 else [r.replace("O", "F").replace("f", "F") for r in HORSE])
    return c, pal


# ==========================================================================
# Hippolyta: queen of the Amazons, daughter of Ares; formal, generous, fierce
# ==========================================================================

HIPPOLYTA_COLORS = [("k", "ink", (32, 24, 32))] + skin(
    (240, 200, 160), (208, 152, 104), (168, 104, 72), (112, 64, 48)) + [
    ("H", "hair", (72, 56, 64)),
    ("h", "hair_l", (128, 104, 112)),
    ("C", "crimson", (232, 80, 64)),
    ("c", "crimson_d", (168, 40, 48)),
    ("x", "crimson_dd", (104, 24, 40)),
    ("O", "gold_l", (248, 224, 120)),
    ("o", "gold", (216, 160, 64)),
    ("b", "bronze_d", (144, 96, 40)),
    ("L", "linen", (240, 232, 216)),
    ("s", "steel", (168, 176, 184)),
]


def hippolyta(npass=3):
    c, pal = new(HIPPOLYTA_COLORS)
    hair = ["hair", "hair_l"]
    gold = ["gold_l", "gold", "bronze_d"]
    # ---- pass 1
    # the pelta on her left arm: a crescent shield, its horns up
    c.ellipse((41, 27, 63, 55), "gold")
    c.ellipse((47, 20, 57, 33), "_")
    # patterned leggings, then the crimson tunic
    c.poly([(23, 56), (31, 56), (31, 63), (23, 63)], "linen")
    c.poly([(34, 56), (42, 56), (42, 63), (34, 63)], "linen")
    c.poly([(21, 30), (43, 30), (45, 44), (46, 57), (18, 57), (19, 44)], "crimson")
    # the war-belt, broad, plaqued in gold
    c.poly([(19, 41), (45, 41), (45, 48), (19, 48)], "gold")
    # her right arm, the hand resting on the belt
    c.poly([(21, 30), (17, 33), (15, 40), (17, 46), (21, 47), (25, 44), (21, 41), (21, 36)], "skin_m")
    # neck, ears, face
    c.poly([(29, 23), (35, 23), (36, 31), (28, 31)], "skin_m")
    c.ellipse((22, 13, 26, 20), "skin_m")
    c.ellipse((38, 13, 42, 20), "skin_m")
    c.poly([(25, 8), (39, 8), (40, 13), (40, 19), (37, 24), (34, 26), (30, 26), (27, 24), (24, 19), (24, 13)],
           "skin_m")
    # black hair under a gold diadem, and the long braid over her right shoulder
    c.poly([(22, 22), (21, 12), (23, 5), (28, 2), (32, 1), (36, 2), (41, 5), (43, 12), (42, 22), (40, 25),
            (39, 15), (36, 10), (28, 10), (25, 15), (24, 25)], "hair")
    for box in ((19, 23, 25, 29), (18, 28, 24, 34), (18, 33, 24, 39), (18, 38, 23, 43)):
        c.ellipse(box, "hair")
    c.ellipse((18, 43, 23, 46), "gold")
    c.poly([(19, 46), (22, 46), (23, 51), (18, 51)], "hair")
    c.poly([(23, 6), (41, 6), (41, 9), (23, 9)], "gold")
    c.poly([(30, 1), (34, 1), (35, 6), (29, 6)], "gold")
    if npass >= 2:
        shade_face(c, (25, 9, 36, 23),
                   [(36, 10), (40, 13), (40, 19), (37, 24), (34, 26), (35, 22), (37, 17)],
                   [(29, 24), (35, 24), (34, 26), (30, 26)])
        c.poly([(28, 25), (36, 25), (36, 31), (28, 30)], "skin_d", clip=["skin_m"])
        c.poly([(18, 34), (20, 32), (18, 42), (16, 41)], "skin_l", clip=["skin_m"])
        # the pelta: a crimson face inside a gold rim, a bronze boss
        c.ellipse((43, 29, 61, 53), "crimson_d", clip=["gold"])
        c.ellipse((45, 33, 60, 52), "crimson", clip=["crimson_d"])
        c.ellipse((49, 37, 55, 43), "gold", clip=["crimson", "crimson_d"])
        c.ellipse((50, 38, 53, 41), "gold_l", clip=["gold"])
        c.poly([(56, 30), (63, 40), (62, 52), (56, 54), (60, 44)], "bronze_d", clip=["gold"])
        # the tunic: shade on her left side, folds below the belt, a key-pattern hem
        c.poly([(37, 30), (43, 30), (45, 41), (38, 41)], "crimson_d", clip=["crimson"])
        c.poly([(37, 48), (46, 48), (46, 57), (38, 57)], "crimson_d", clip=["crimson"])
        c.line([(26, 49), (24, 56)], "crimson_d", clip=["crimson"])
        c.line([(31, 49), (31, 56)], "crimson_d", clip=["crimson"])
        c.poly([(18, 54), (46, 54), (46, 57), (18, 57)], "crimson_dd", clip=["crimson", "crimson_d"])
        for x in range(19, 46, 3):
            c.patch(x, 55, ["O"], clip=["crimson_dd"])
        # the belt's plaques
        c.line([(19, 41), (45, 41)], "gold_l", clip=gold)
        c.line([(19, 48), (45, 48)], "bronze_d", clip=gold)
        for x in range(21, 45, 4):
            c.patch(x, 43, ["Ob", "bb"], clip=gold)
        # leggings: the Amazons' zigzag
        for x0 in (23, 34):
            c.patch(x0, 57, ["k.k.k.k.", ".k.k.k.k", "........", "k.k.k.k.", ".k.k.k.k", "........",
                             "k.k.k.k."], clip=["linen"])
        # hair and braid sheen; the diadem's shade
        c.poly([(23, 5), (28, 2), (32, 2), (27, 5), (24, 10)], "hair_l", clip=hair)
        for box in ((20, 24, 22, 26), (19, 29, 21, 31), (19, 34, 21, 36), (19, 39, 21, 41)):
            c.ellipse(box, "hair_l", clip=hair)
        c.line([(23, 9), (41, 9)], "bronze_d", clip=gold)
        c.line([(23, 6), (36, 6)], "gold_l", clip=gold)
        c.outline("ink")
        c.seam(hair, ["skin_m", "skin_l", "skin_d"], "ink")
        # level, strong brows; dark eyes; a composed mouth
        c.patch(25, 11, [
            ".HHHH....HHHH.",
            "H....H..H....H",
            ".kkkk....kkkk.",
            "kLHkk....kkHLk",
            ".mddm....mddm.",
        ])
        c.patch(31, 17, ["md", "md", "Smd", "dD"])
        c.patch(29, 22, ["Dkkkkd", ".dCCd."])
    if npass >= 3:
        # the hand on the belt, fingers over the plaques
        c.patch(20, 43, ["kmmmk", "mSSmd", "kmkmk"], clip=SKINS + gold + ["ink", "crimson"])
        # gold earrings, a gem in the diadem
        c.patch(23, 19, ["O", "o"], clip=SKINS + hair)
        c.patch(40, 19, ["o", "b"], clip=SKINS + hair)
        c.patch(31, 2, ["CC", "cc"], clip=gold)
        # cheekbones
        c.patch(26, 19, ["m"], clip=SKINS)
        c.patch(36, 18, ["D"], clip=SKINS)
    return c, pal


# ==========================================================================
# Atalanta: the huntress no man could outrun, raised by a bear; quick,
# practical, unbothered
# ==========================================================================

ATALANTA_COLORS = [("k", "ink", (40, 24, 24))] + skin(
    (248, 208, 168), (224, 160, 112), (184, 112, 72), (128, 72, 48)) + [
    ("R", "auburn_l", (224, 128, 72)),
    ("r", "auburn", (176, 80, 48)),
    ("a", "auburn_d", (112, 48, 40)),
    ("L", "linen", (248, 240, 216)),
    ("l", "linen_d", (200, 184, 152)),
    ("B", "bear", (144, 104, 72)),
    ("b", "bear_d", (80, 56, 48)),
    ("w", "wood", (216, 168, 96)),
    ("g", "green", (88, 136, 72)),
    ("c", "red", (208, 72, 56)),
]


def atalanta(npass=3):
    c, pal = new(ATALANTA_COLORS)
    hair = ["auburn", "auburn_l", "auburn_d"]
    bear = ["bear", "bear_d"]
    # ---- pass 1
    # the bearskin over her shoulders, its head thrown back behind her own
    c.poly([(17, 30), (23, 27), (41, 27), (47, 30), (52, 39), (55, 50), (54, 63), (10, 63), (9, 50), (12, 39)],
           "bear")
    for x, y in ((10, 44), (9, 52), (10, 59), (53, 44), (55, 52), (55, 59)):
        c.poly([(x, y), (x + (-2 if x < 32 else 2), y + 2), (x, y + 4)], "bear")
    # legs
    c.poly([(24, 57), (31, 57), (31, 63), (24, 63)], "skin_m")
    c.poly([(34, 57), (41, 57), (41, 63), (34, 63)], "skin_m")
    # the short chiton, off her right shoulder
    c.poly([(22, 30), (42, 30), (43, 44), (44, 58), (20, 58), (21, 44)], "linen")
    c.poly([(21, 29), (28, 29), (26, 36), (21, 36)], "skin_m")
    c.poly([(21, 43), (43, 43), (43, 46), (21, 46)], "bear_d")
    # her right arm, an arrow held loose and low
    c.poly([(22, 30), (18, 34), (16, 42), (16, 48), (20, 49), (21, 41), (24, 35)], "skin_m")
    c.line([(10, 60), (22, 40)], "wood", width=1)
    # her left arm and the bow
    c.poly([(42, 30), (46, 33), (49, 40), (51, 44), (48, 47), (45, 41), (42, 37)], "skin_m")
    c.line([(51, 12), (55, 22), (56, 38), (55, 52), (51, 62)], "wood", width=2)
    c.line([(50, 12), (50, 62)], "linen_d")
    c.ellipse((47, 41, 53, 48), "skin_m")
    c.ellipse((14, 46, 21, 52), "skin_m")
    # neck, ears, face
    c.poly([(29, 23), (35, 23), (36, 31), (28, 31)], "skin_m")
    c.ellipse((22, 13, 26, 20), "skin_m")
    c.ellipse((38, 13, 42, 20), "skin_m")
    c.poly([(25, 8), (39, 8), (40, 13), (40, 19), (37, 24), (34, 26), (30, 26), (27, 24), (24, 19), (24, 13)],
           "skin_m")
    # auburn hair pulled back, the tail swinging out behind
    c.poly([(22, 18), (21, 10), (24, 5), (29, 3), (35, 3), (40, 5), (43, 10), (42, 18), (40, 20), (39, 13),
            (36, 10), (28, 10), (25, 14), (24, 20)], "auburn")
    c.poly([(40, 6), (45, 3), (50, 6), (52, 12), (50, 19), (48, 14), (44, 9)], "auburn")
    # the bear's paws knotted at her breast
    c.ellipse((29, 29, 35, 34), "bear")
    if npass >= 2:
        shade_face(c, (25, 9, 36, 23),
                   [(36, 10), (40, 13), (40, 19), (37, 24), (34, 26), (35, 22), (37, 17)],
                   [(29, 24), (35, 24), (34, 26), (30, 26)])
        c.poly([(28, 25), (36, 25), (36, 31), (28, 30)], "skin_d", clip=["skin_m"])
        c.poly([(17, 36), (20, 33), (18, 44), (16, 44)], "skin_l", clip=["skin_m"])
        c.poly([(22, 30), (26, 30), (25, 33), (22, 34)], "skin_l", clip=["skin_m"])
        c.poly([(24, 58), (27, 58), (27, 63), (24, 63)], "skin_l", clip=["skin_m"])
        c.poly([(34, 58), (36, 58), (36, 63), (34, 63)], "skin_l", clip=["skin_m"])
        c.poly([(29, 58), (31, 58), (31, 63), (29, 63)], "skin_d", clip=["skin_m"])
        c.poly([(39, 58), (41, 58), (41, 63), (39, 63)], "skin_d", clip=["skin_m"])
        # the bearskin: fur in shade on her left and below, the snout behind her head
        c.poly([(40, 27), (48, 30), (54, 40), (58, 50), (57, 63), (42, 63)], "bear_d", clip=bear)
        c.poly([(17, 30), (23, 27), (26, 28), (19, 33)], "bear", clip=bear)
        c.poly([(12, 50), (18, 52), (20, 63), (12, 63)], "bear_d", clip=bear)
        # the chiton's shade and folds
        c.poly([(37, 30), (42, 30), (43, 43), (38, 43)], "linen_d", clip=["linen"])
        c.poly([(36, 46), (44, 46), (44, 58), (38, 58)], "linen_d", clip=["linen"])
        c.line([(27, 47), (25, 57)], "linen_d", clip=["linen"])
        c.line([(31, 47), (32, 57)], "linen_d", clip=["linen"])
        # the arrow: iron head at the bottom, red fletching at the top
        c.patch(9, 59, ["k.", "kk", ".k"], clip=None)
        c.patch(21, 38, [".c", "cc", "c."], clip=None)
        # hair: lit at the crown, dark at the tie and the tail's underside
        c.poly([(23, 6), (29, 4), (33, 4), (27, 7), (24, 12)], "auburn_l", clip=hair)
        c.poly([(38, 5), (43, 10), (42, 18), (40, 18)], "auburn_d", clip=hair)
        c.poly([(45, 9), (51, 13), (50, 19), (48, 14)], "auburn_d", clip=hair)
        c.poly([(45, 3), (49, 5), (47, 7)], "auburn_l", clip=hair)
        c.outline("ink")
        c.seam(hair, ["skin_m", "skin_l", "skin_d"], "ink")
        c.seam(["bear", "bear_d"], ["skin_m", "skin_l", "linen"], "ink")
        # unbothered: lids half down, eyes slid aside, one corner up
        c.patch(25, 11, [
            ".aaa.....aaa..",
            "a...a...a...a.",
            ".kkkk....kkkk.",
            ".kLgk....kLgk.",
            ".mddm....mddm.",
        ])
        c.patch(31, 17, ["md", "md", "Smd", "dD"])
        c.patch(29, 22, ["dkkkkD", "..cc.."])
    if npass >= 3:
        # freckles across the nose, the tie at her crown
        c.patch(29, 18, ["m.m"], clip=["skin_l", "skin_m"])
        c.patch(34, 18, ["m"], clip=["skin_l", "skin_m"])
        c.patch(40, 5, ["bb", "ww"], clip=hair + ["ink"])
        # the fur's tufts along the cape's edge
        for x, y in ((12, 46), (11, 53), (13, 60), (53, 46), (53, 55)):
            c.patch(x, y, ["B", "b"], clip=bear + ["ink"])
        # the knotted paws and their claws
        c.patch(29, 29, [".kBBk.", "kBbbBk", "kbLLbk", ".kkkk."], clip=bear + ["linen", "linen_d", "ink", "skin_m"])
        # her fingers round the bow's grip and the arrow
        c.patch(47, 42, ["kmmk", "mSmd", "mmdd", "kddk"], clip=SKINS + ["wood", "linen_d", "ink"])
        c.patch(15, 46, ["kmmk", "mSmd", "kddk"], clip=SKINS + ["wood", "ink"])
        # a sash of green ribbon round the bow's tips
        c.patch(51, 11, ["g", "g"], clip=["wood", "ink", "_"])
        c.patch(50, 61, ["g"], clip=["wood", "ink", "_"])
    return c, pal


# ==========================================================================
# Ariadne: mistress of the Labyrinth; dry, guarded. Arms folded, the red
# spool in her hand, the thread running out of the frame.
# ==========================================================================

ARIADNE_COLORS = [("k", "ink", (32, 24, 32))] + skin(
    (248, 224, 200), (232, 184, 152), (200, 136, 112), (144, 88, 80)) + [
    ("H", "hair", (64, 48, 64)),
    ("h", "hair_l", (120, 96, 120)),
    ("O", "gold_l", (248, 224, 128)),
    ("o", "gold", (216, 160, 64)),
    ("b", "gold_d", (152, 96, 48)),
    ("C", "crimson", (216, 64, 64)),
    ("c", "crimson_d", (144, 32, 48)),
    ("B", "blue", (72, 120, 192)),
    ("n", "blue_d", (40, 64, 128)),
    ("L", "linen", (248, 240, 224)),
]


def ariadne(npass=3):
    c, pal = new(ARIADNE_COLORS)
    hair = ["hair", "hair_l"]
    gold = ["gold_l", "gold", "gold_d"]
    # ---- pass 1
    # long black curls falling behind her to the waist
    c.poly([(18, 8), (22, 2), (32, 0), (42, 2), (46, 8), (48, 24), (50, 44), (43, 46), (42, 28), (22, 28),
            (21, 46), (14, 44), (16, 24)], "hair")
    # the flounced skirt, banded
    c.poly([(18, 45), (46, 45), (50, 63), (14, 63)], "blue")
    # the gold bodice over a linen chemise
    c.poly([(21, 28), (43, 28), (44, 46), (20, 46)], "gold")
    c.poly([(28, 28), (36, 28), (34, 34), (30, 34)], "linen")
    # upper arms, and the forearms folded across
    c.poly([(19, 29), (24, 29), (23, 41), (18, 41)], "skin_m")
    c.poly([(40, 29), (45, 29), (46, 41), (41, 41)], "skin_m")
    c.poly([(18, 37), (40, 34), (44, 37), (44, 41), (22, 44), (18, 42)], "skin_m")
    c.poly([(21, 40), (46, 37), (46, 41), (24, 44)], "skin_m")
    # the red spool in her right hand, tucked at her left elbow
    c.ellipse((40, 33, 47, 40), "crimson")
    # neck, ears, face
    c.poly([(29, 23), (35, 23), (36, 29), (28, 29)], "skin_m")
    c.ellipse((22, 13, 26, 20), "skin_m")
    c.ellipse((38, 13, 42, 20), "skin_m")
    c.poly([(25, 8), (39, 8), (40, 13), (40, 19), (37, 24), (34, 26), (30, 26), (27, 24), (24, 19), (24, 13)],
           "skin_m")
    # the front curls over her brow and down over her shoulders
    c.poly([(22, 18), (21, 9), (25, 4), (32, 2), (39, 4), (43, 9), (42, 18), (40, 21), (39, 13), (35, 10),
            (28, 10), (25, 13), (24, 21)], "hair")
    for box in ((17, 22, 24, 30), (16, 29, 23, 37), (40, 22, 47, 30), (41, 29, 48, 37)):
        c.ellipse(box, "hair")
    c.poly([(23, 6), (41, 6), (41, 8), (23, 8)], "gold")
    if npass >= 2:
        shade_face(c, (25, 9, 36, 23),
                   [(36, 10), (40, 13), (40, 19), (37, 24), (34, 26), (35, 22), (37, 17)],
                   [(29, 24), (35, 24), (34, 26), (30, 26)])
        c.poly([(28, 25), (36, 25), (36, 29), (28, 28)], "skin_d", clip=["skin_m"])
        # the forearms: the upper one lit, the lower in its shadow
        c.poly([(18, 37), (40, 34), (41, 35), (19, 39)], "skin_l", clip=["skin_m"])
        c.poly([(22, 42), (46, 39), (46, 41), (24, 44)], "skin_d", clip=["skin_m"])
        c.poly([(42, 30), (45, 29), (46, 37), (43, 36)], "skin_d", clip=["skin_m"])
        # the bodice's shade and its gold edging; the chemise's folds
        c.poly([(37, 28), (43, 28), (44, 46), (39, 46)], "gold_d", clip=["gold"])
        c.line([(21, 28), (28, 28)], "gold_l", clip=["gold"])
        c.line([(30, 30), (32, 33)], "gold_d", clip=["linen"])
        # the skirt's flounces: blue, crimson, linen, blue, each with a dark lip
        c.poly([(14, 49), (50, 49), (50, 53), (14, 53)], "crimson", clip=["blue"])
        c.poly([(14, 53), (50, 53), (50, 57), (14, 57)], "linen", clip=["blue"])
        for y in (48, 52, 56, 63):
            c.line([(14, y), (50, y)], "blue_d", clip=["blue"])
        c.line([(14, 52), (50, 52)], "crimson_d", clip=["crimson"])
        c.line([(14, 56), (50, 56)], "gold", clip=["linen"])
        for x in range(16, 50, 3):
            c.patch(x, 54, ["C"], clip=["linen"])
        c.poly([(40, 45), (50, 45), (50, 63), (43, 63)], "blue_d", clip=["blue"])
        c.poly([(40, 49), (50, 49), (50, 52), (42, 52)], "crimson_d", clip=["crimson"])
        # the spool: red wound thread with a gold rim
        c.ellipse((41, 34, 45, 38), "crimson_d", clip=["crimson"])
        c.line([(40, 36), (47, 36)], "gold", clip=["crimson", "crimson_d"])
        # curls: lit swirls
        for x, y in ((18, 24), (17, 31), (43, 24), (44, 31), (20, 39), (45, 39)):
            c.patch(x, y, ["h.", ".h", "h."], clip=hair)
        c.poly([(23, 5), (29, 3), (33, 3), (27, 6), (24, 10)], "hair_l", clip=hair)
        c.outline("ink")
        c.seam(hair, ["skin_m", "skin_l", "skin_d"], "ink")
        c.seam(["skin_m", "skin_l"], ["skin_d"], "skin_d")
        # flat, level, unimpressed
        c.patch(25, 11, [
            "..............",
            ".HHHHH..HHHHH.",
            ".kkkk....kkkk.",
            "kkHLk....kLHkk",
            ".mddm....mddm.",
        ])
        c.patch(31, 17, ["md", "md", "Smd", "dD"])
        c.patch(29, 22, [".kkkk.", "..dd.."])
    if npass >= 3:
        # the thread running from the spool out of the frame
        c.line([(46, 39), (49, 44), (48, 50), (51, 56), (50, 63)], "crimson")
        c.patch(45, 38, ["C"])
        # curl rings in the long hair behind
        for x, y in ((16, 41), (47, 42), (15, 35), (48, 30), (20, 12), (43, 12)):
            c.patch(x, y, [".h", "h."], clip=hair)
        # gold earrings, the band's studs
        c.patch(23, 19, ["O", "b"], clip=SKINS + hair)
        c.patch(40, 19, ["o", "b"], clip=SKINS + hair)
        for x in range(25, 40, 4):
            c.patch(x, 7, ["O"], clip=gold)
        # her fingers on her upper arm, a heavy-lidded look
        c.patch(19, 36, ["Sm", "mm", "dd"], clip=SKINS)
        c.patch(26, 13, ["mmmm.....mmmm"], clip=["ink", "skin_l", "skin_m"])
    return c, pal


# ==========================================================================
# Olympias: the Serpent Queen, Hera's seat; commands, never asks; proud of
# her creatures; warmth she won't admit
# ==========================================================================

OLYMPIAS_COLORS = [("k", "ink", (32, 24, 32))] + skin(
    (248, 224, 208), (232, 192, 168), (200, 144, 128), (144, 96, 96)) + [
    ("H", "hair", (48, 40, 56)),
    ("O", "gold_l", (248, 224, 120)),
    ("o", "gold", (216, 160, 56)),
    ("b", "gold_d", (144, 96, 40)),
    ("P", "purple_l", (184, 112, 184)),
    ("p", "purple", (136, 64, 144)),
    ("x", "purple_d", (80, 32, 88)),
    ("G", "serpent_l", (144, 192, 96)),
    ("g", "serpent", (72, 128, 72)),
    ("r", "lip", (184, 64, 88)),
]


def olympias(npass=3):
    c, pal = new(OLYMPIAS_COLORS)
    gold = ["gold_l", "gold", "gold_d"]
    snake = ["serpent", "serpent_l"]
    # ---- pass 1
    # the purple peplos, falling to the frame's foot
    c.poly([(20, 30), (44, 30), (46, 44), (50, 63), (14, 63), (18, 44)], "purple")
    # her right arm down at her side
    c.poly([(20, 30), (16, 34), (14, 44), (14, 54), (18, 54), (19, 44), (21, 36)], "skin_m")
    # her left arm: elbow down, forearm raised, the hand open at her shoulder
    c.poly([(43, 30), (48, 33), (52, 43), (49, 46), (46, 40), (44, 35)], "skin_m")
    c.poly([(48, 46), (52, 43), (53, 34), (51, 27), (48, 27), (49, 35), (47, 43)], "skin_m")
    c.ellipse((46, 23, 53, 30), "skin_m")
    # the serpents: one wound up her raised arm, its head up and turned to her;
    # one round her right arm, its tail hanging to the hem
    c.line([(47, 45), (53, 41), (48, 37), (53, 33), (49, 29), (47, 22), (44, 18)], "serpent", width=3)
    c.ellipse((40, 13, 47, 19), "serpent")
    c.line([(14, 38), (20, 41), (14, 45), (19, 49), (15, 53), (13, 57)], "serpent", width=3)
    c.ellipse((9, 55, 15, 60), "serpent")
    # neck, ears, face
    c.poly([(29, 23), (35, 23), (36, 31), (28, 31)], "skin_m")
    c.ellipse((22, 13, 26, 20), "skin_m")
    c.ellipse((38, 13, 42, 20), "skin_m")
    c.poly([(25, 9), (39, 9), (40, 13), (40, 19), (37, 24), (34, 26), (30, 26), (27, 24), (24, 19), (24, 13)],
           "skin_m")
    # black waves under the tall gold polos
    c.poly([(20, 24), (19, 13), (22, 8), (42, 8), (45, 13), (44, 24), (41, 30), (40, 16), (37, 11), (27, 11),
            (24, 16), (23, 30)], "hair")
    c.poly([(22, 2), (42, 2), (40, 9), (24, 9)], "gold")
    # the gold girdle and the neckline's border
    c.poly([(18, 43), (46, 43), (46, 45), (18, 45)], "gold")
    c.poly([(26, 30), (38, 30), (32, 37)], "gold")
    c.poly([(28, 30), (36, 30), (32, 35)], "skin_m")
    if npass >= 2:
        shade_face(c, (25, 10, 36, 23),
                   [(36, 11), (40, 13), (40, 19), (37, 24), (34, 26), (35, 22), (37, 17)],
                   [(29, 24), (35, 24), (34, 26), (30, 26)])
        c.poly([(28, 25), (36, 25), (36, 31), (28, 30)], "skin_d", clip=["skin_m"])
        c.poly([(16, 35), (19, 32), (17, 44), (15, 44)], "skin_l", clip=["skin_m"])
        c.poly([(48, 33), (51, 29), (52, 38), (50, 42)], "skin_d", clip=["skin_m"])
        # the peplos: purple in shade on her left and below, deep folds
        c.poly([(38, 30), (44, 30), (46, 44), (50, 63), (40, 63), (40, 45)], "purple_d", clip=["purple"])
        c.poly([(20, 31), (26, 31), (24, 42), (20, 42)], "purple_l", clip=["purple"])
        for x0, x1 in ((24, 22), (29, 28), (34, 35)):
            c.line([(x0, 46), (x1, 63)], "purple_d", clip=["purple"])
        c.line([(14, 62), (50, 62)], "gold", clip=["purple", "purple_d"])
        c.line([(14, 63), (50, 63)], "gold_d", clip=["purple", "purple_d"])
        # the polos's bands and the girdle's shade
        c.line([(22, 2), (42, 2)], "gold_l", clip=gold)
        c.line([(23, 4), (41, 4)], "gold_d", clip=gold)
        c.line([(24, 8), (40, 8)], "gold_d", clip=gold)
        c.poly([(36, 2), (42, 2), (40, 9), (35, 9)], "gold_d", clip=gold)
        for x in range(25, 39, 4):
            c.patch(x, 5, ["Ob", "bO"], clip=gold)
        c.line([(18, 43), (34, 43)], "gold_l", clip=gold)
        c.line([(36, 45), (46, 45)], "gold_d", clip=gold)
        # the serpents' scales: lit backs, dark undersides
        for x, y in ((48, 44), (51, 40), (50, 36), (51, 32), (48, 26), (46, 21), (15, 39), (18, 42), (16, 46),
                     (18, 50), (16, 56), (17, 61)):
            c.patch(x, y, ["G"], clip=snake)
        c.outline("ink")
        c.seam(["hair"], ["skin_m", "skin_l", "skin_d"], "ink")
        # heavy lids, a level look down her nose, a thin knowing smile
        c.patch(25, 11, [
            "..HHH....HHH..",
            ".H...H..H...H.",
            ".kkkkk..kkkkk.",
            ".mkHSk..kSHkm.",
            "..mdd....ddm..",
        ])
        c.patch(31, 17, ["md", "md", "Smd", "dD"])
        c.patch(29, 22, ["dkkkkD", ".rrrr."])
    if npass >= 3:
        # the raised serpent's head, its eye and its tongue, turned to her
        c.patch(39, 12, ["..kkkk..", ".kGGggk.", "kGgkggGk", "kgggggGk", "rkkggggk", "r..kkkk."])
        c.patch(8, 54, ["..kkkk..", ".kgGGGk.", "kGggkgGk", "kgggggGk", ".kkggk..", "..rr...."])
        # its coils' dark undersides
        c.patch(47, 38, ["g"], clip=snake)
        # gold earrings, long; a gold armband at her right shoulder
        c.patch(23, 19, ["O", "o", "b"], clip=SKINS + ["hair"])
        c.patch(40, 19, ["o", "b"], clip=SKINS + ["hair", "serpent", "serpent_l"])
        c.patch(17, 34, ["OOO", "bbb"], clip=SKINS)
        # her fingers spread under the serpent's coil
        c.patch(46, 24, [".kSk", "kSmS", "kmmd"], clip=SKINS + snake + ["ink"])
        # the hair's waves catching a little light
        c.patch(21, 14, ["k", ".", "k"], clip=["hair"])
        c.patch(42, 15, ["k", ".", "k"], clip=["hair"])
    return c, pal


PORTRAITS = {
    "achilles": achilles,
    "odysseus": odysseus,
    "hippolyta": hippolyta,
    "atalanta": atalanta,
    "ariadne": ariadne,
    "olympias": olympias,
}


def render(name, npass):
    c, pal = PORTRAITS[name](npass)
    if npass < 2:
        c.outline("ink")
    return c.a, pal


def sheet(npass, names, k=4, bg=(200, 200, 200)):
    out = Image.new("RGBA", (64 * len(names), 64), bg + (255,))
    for i, n in enumerate(names):
        a, pal = render(n, npass)
        out.alpha_composite(to_rgba(a, pal), (64 * i, 0))
    return upscale(out, k)


def main(argv):
    names = [a for a in argv if a in PORTRAITS] or list(PORTRAITS)
    npass = int(argv[argv.index("--pass") + 1]) if "--pass" in argv else 3
    if "--write" in argv:
        for n in names:
            a, pal = render(n, 3)
            save_indexed(a, pal, os.path.join(FRONT, f"ichor_pg_{n}.png"))
        print("wrote", ", ".join(f"ichor_pg_{n}.png" for n in names))
    if "--preview" in argv:
        d = argv[argv.index("--preview") + 1]
        os.makedirs(d, exist_ok=True)
        for p in (1, 2, 3):
            if p <= npass:
                sheet(p, names).save(os.path.join(d, f"pg_portraits_pass{p}.png"))
        for n in names:
            a, pal = render(n, npass)
            bg = Image.new("RGBA", (64, 64), (200, 200, 200, 255))
            bg.alpha_composite(to_rgba(a, pal))
            upscale(bg, 8).save(os.path.join(d, f"pg_{n}_x8.png"))
        print("preview in", d)


if __name__ == "__main__":
    main(sys.argv[1:])
