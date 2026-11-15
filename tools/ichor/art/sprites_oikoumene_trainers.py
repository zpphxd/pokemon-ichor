"""Trainer front pics for the Oikoumene's batch 1: eleven classes and four named people.

The Troad (Trojan Hoplite, Charioteer, Shepherd of Ida, Prince Hektor), the Black
Sea (Argonaut, Colchian Sorceress, Chalybes Smith, Medea) and Egypt (Priest of the
Sun, Scribe of Thoth, Embalmer, Nile Boatman, Phoenician Trader, Pharaoh Proteus,
Helen of Sparta). Each is a 64x64, 16-color Gen 3 front pic in the slice's hand
(sprites_classes.py): a 3/4 view toward the player's side, lit from the top left,
ink outlines, and black-figure ornament. Each land's people are drawn the way Greek
painters drew foreigners on their own pots (OIKOUMENE.md §7). See
design/oikoumene/SPRITES.md, "Trainer pics".

Usage: python3 tools/ichor/art/sprites_oikoumene_trainers.py [NAME ...] [--write] [--preview DIR]

--write   writes the indexed PNGs to graphics/trainers/front_pics/ and, when no
          NAME is given, the 2x review sheet design/oikoumene/img/trainers_batch1.png.
--preview writes the 3x battle-background sheet (the slice's Hoplite and Shepherd
          for scale), 6x singles and pixel grids to DIR.
"""
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import (ROOT, Palette, Mat, Fig, save_indexed, to_rgba,  # noqa: E402
                         upscale, palette_report, grid_preview)
from sprites_classes import render, pole, stagger, load_pic, battle_tile, INK  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

FRONT = os.path.join(ROOT, "graphics/trainers/front_pics")
SHEET = os.path.join(ROOT, "design/oikoumene/img/trainers_batch1.png")

# Skin ramps (light, mid, dark). Greek painters gave each people its own look;
# here that is dress first, and a skin ramp per land.
SKIN_TAN = [("skin_l", (248, 200, 152)), ("skin_m", (216, 144, 96)), ("skin_d", (160, 96, 64))]
SKIN_SUN = [("skin_l", (232, 176, 120)), ("skin_m", (192, 120, 72)), ("skin_d", (136, 80, 48))]
SKIN_FAIR = [("skin_l", (248, 216, 184)), ("skin_m", (224, 168, 128)), ("skin_d", (176, 112, 80))]
SKIN_OLIVE = [("skin_l", (232, 192, 144)), ("skin_m", (192, 136, 96)), ("skin_d", (136, 88, 64))]
# Egyptian men as the Egyptians and the Greeks both painted them: red-brown
SKIN_NILE = [("skin_l", (216, 144, 96)), ("skin_m", (176, 96, 64)), ("skin_d", (120, 64, 48))]


def skin_mat(outline):
    return Mat(["skin_d", "skin_m", "skin_l"], outline=outline, cuts=[0.5, 0.86])


def P(f, x0, y0, art, legend):
    """An ASCII patch given as one block of text ('.' leaves pixels alone)."""
    rows = [r.strip() for r in textwrap.dedent(art).strip("\n").split("\n")]
    f.patch(x0, y0, rows, legend)


def fist(f, x, y, line):
    f.patch(x, y, [".bbbb.", "bLLLLb", "bLbLMb", "bLLMMb", ".bbbb."],
            {"b": line, "L": "skin_l", "M": "skin_m"})


# --------------------------------------------------------------------------
# Faces. Every head starts from one of these, drawn first; hair and headgear
# go on top as a second patch with '.' over the face. One hand for all fifteen,
# matching the slice's (Kleon, the Hoplite): 3/4 toward the player, eyes
# looking left, light from the top left. 16 x 11, the forehead on row 0.
#   k ink  o outline  L M D skin  W eye white  H hair or beard  R lips
# --------------------------------------------------------------------------

FACE_M = """
    .oLLLLLLLLLLMMo.
    oLLkkkLLLLkkkMMo
    oLLLkWLLLLLkWMDo
    oLLLLLLLLLLMMMDo
    oLLLLLLDLLLMMDo.
    .oLLLLLDDLLMMDo.
    .oLLLLLLLLLMMMo.
    ..oLLLkkkLLMMo..
    ..oLLLLLLLLMMo..
    ...oLLLLLMMMo...
    ....oooooooo....
"""

FACE_F = """
    .oLLLLLLLLLLMMo.
    oLLLkkLLLLLkkMMo
    oLLkkWLLLLkkWMDo
    oLLLLLLLLLLMMMDo
    oLLLLLLDLLLMMMo.
    .oLLLLLLLLLMMMo.
    .oLLLLLRRLLMMMo.
    ..oLLLLLLLLMMo..
    ...oLLLLLMMMo...
    ....oooooooo....
"""

FACE_BEARD = """
    .oLLLLLLLLLLMMo.
    oLLkkkLLLLkkkMMo
    oLLLkWLLLLLkWMDo
    oLLLLLLLLLLMMMDo
    oHLLLLLDLLLMMDHo
    oHHLLLDDLLLMMHHo
    oHHHHHHHHHHHHHHo
    oHHHHkkkkHHHHHHo
    .oHHHHHHHHHHHHo.
    ..oHHHHHHHHHHo..
    ...oHHHHHHHHo...
    ....oooooooo....
"""

# Egyptian eyes: the kohl line runs past each eye's outer corner
FACE_KOHL = """
    .oLLLLLLLLLLMMo.
    oLLkkkkLLLkkkkMo
    oLkkWkLLLLkkWkko
    oLLLLLLLLLLMMMDo
    oLLLLLLDLLLMMDo.
    .oLLLLLDDLLMMDo.
    .oLLLLLLLLLMMMo.
    ..oLLLkkkLLMMo..
    ..oLLLLLLLLMMo..
    ...oLLLLLMMMo...
    ....oooooooo....
"""


def face(f, x, y, art, outline, white="W", hair=None, lips=None, edits=()):
    legend = {"k": "ink", "o": outline, "L": "skin_l", "M": "skin_m", "D": "skin_d", "W": white}
    if hair:
        legend["H"] = hair
    if lips:
        legend["R"] = lips
    P(f, x, y, art, legend)
    for dx, dy, c in edits:
        f.px(x + dx, y + dy, c)


# A smile on a face: the mouth's corners (row 6) turned up over its line (row 7).
SMILE = [(5, 6, "ink"), (9, 6, "ink")]


# ==========================================================================
# The Troad: Greek painters drew Trojans as Greeks, with Phrygian caps and
# patterned sleeves for Paris and his kind.
# ==========================================================================

def trojan_hoplite():
    """A gate guard of Ilion: a bronze Attic helmet worn down, a tall blue
    crest on a stilt, a round shield braced toward you painted in black-figure
    with Troy's horse, a spear grounded at his side."""
    pal = Palette([
        ("ink", INK), *SKIN_TAN, ("brown", (104, 56, 40)),
        ("br_l", (248, 216, 120)), ("br_m", (216, 160, 64)), ("br_d", (144, 88, 40)),
        ("bl_l", (128, 176, 232)), ("bl_m", (56, 104, 184)), ("bl_d", (32, 56, 120)),
        ("clay_l", (232, 144, 80)), ("clay_d", (184, 96, 48)),
        ("lin", (240, 232, 208)), ("hair", (56, 40, 32)),
    ])
    skin = skin_mat("brown")
    bronze = Mat(["br_d", "br_m", "br_l"], cuts=[0.35, 0.72])
    blue = Mat(["bl_d", "bl_m", "bl_l"], wx=0.85, wy=0.2, cuts=[0.25, 0.65])
    clay = Mat(["clay_d", "clay_l"], wx=0.8, wy=0.6, cuts=[0.62])
    wood = Mat(["br_d", "clay_d"], cuts=[0.75])
    lea = Mat(["brown"])
    f = Fig(pal)

    # blue cloak behind, falling to his right
    f.poly([(25, 22), (41, 22), (47, 30), (50, 44), (47, 48), (40, 46), (30, 46)], blue, bias=0.3)
    # spear grounded at his right side
    pole(f, (51, 8), (51, 61), wood, group=50)
    # legs and bronze greaves
    f.poly([(26, 45), (31, 45), (30, 51), (29, 57), (25, 57), (25, 51)], skin, group=100)
    f.poly([(35, 45), (39, 45), (41, 51), (43, 57), (39, 57), (37, 51)], skin, group=101)
    f.poly([(25, 49), (30, 49), (29, 57), (25, 57)], bronze, group=110)
    f.poly([(37, 49), (41, 49), (43, 57), (39, 57)], bronze, group=111)
    f.poly([(23, 57), (30, 57), (30, 61), (22, 61)], lea)
    f.poly([(38, 57), (44, 57), (46, 61), (38, 61)], lea)
    # blue chiton skirt under linen strips
    f.poly([(25, 38), (42, 38), (44, 47), (23, 47)], blue)
    # bronze bell cuirass
    f.poly([(26, 22), (40, 22), (42, 30), (41, 40), (26, 40), (25, 30)], bronze)
    f.rect(31, 19, 36, 24, skin, group=400)
    # right arm out to the spear
    f.poly([(39, 22), (44, 23), (44, 27), (40, 28)], bronze, group=210)
    f.thick_line([(42, 26), (48, 30)], 5, skin, group=200)
    # the shield, braced toward you
    rim = f.ellipse((3, 23, 31, 51), bronze, group=600)
    f.ellipse((6, 26, 28, 48), clay, group=610, clip=rim, noline=True)

    # pteruges and greave ridges
    for x in (27, 31, 35, 39):
        f.line([(x, 40), (x - 1, 46)], "lin")
    f.line([(26, 50), (26, 56)], "br_l")
    f.line([(39, 50), (40, 56)], "br_l")
    # cuirass: the muscle line
    f.line([(33, 26), (33, 36)], "br_d")
    f.line([(28, 31), (31, 33), (35, 33), (38, 31)], "br_d")
    # shield rim highlights
    f.line([(9, 25), (15, 23)], "br_l")
    f.line([(4, 33), (5, 29)], "br_l")
    # Troy's horse on the shield: a black-figure protome, eye and mane incised
    P(f, 8, 29, """
        .......k.k......
        ......kkkk......
        .....kkkkkk.....
        ....kkLkkkkk....
        ...kkkkkkkkkL...
        ..kkkkkkkkkkkL..
        .kkkkkkk.kkkkkL.
        kkkkkkk...kkkkkL
        kkkkk.....kkkkkk
        .kk.......kkkkkk
        ..........kkkkkk
        .........kkkkkkk
        ........kkkkkkkk
    """, {"k": "ink", "L": "clay_l"})
    fist(f, 47, 27, "brown")
    # spearhead
    P(f, 49, 0, """
        ..k..
        .kGk.
        .kGYk
        kGYYk
        kGYYk
        .kGYk
        .kYk.
        .kkk.
        ..k..
    """, {"k": "ink", "G": "br_l", "Y": "br_m"})
    # face, then the Attic helmet over it: cheek pieces down, a blue crest on a stilt
    face(f, 25, 11, FACE_M, "brown", white="lin", edits=[(8, 7, "skin_m")])
    P(f, 22, 0, """
        .........kkkkkkkk.......
        ......kkkBBBBBBBBkkk....
        ....kkBBBBBBBbbbbbbbkk..
        ...kBBBbbbbbbbbbbbbbbbk.
        ...kkkkkkkkkkkkkbbbbbbdk
        .........kYk....kkbbbddk
        .......kkkYkkkk...kbbddk
        ......kGGGYYYYYkk..kbddk
        .....kGGYYYYYYYYyk..kddk
        ....kGGYYYYYYYYYyyk..kk.
        ...kGGYYYYYYYYYYyyyk....
        ...kkkkkkkkkkkkkkkkyyk..
        ..kGYk............kYyyk.
        ..kGYk............kYyyk.
        ..kGYk............kYyyk.
        ..kGYk...........kYyyyk.
        ..kGYYk..........kYyyk..
        ...kGYk.........kYyyk...
        ...kGYk........kYyyk....
        ....kYk.......kkyyk.....
        .....kk........kkk......
    """, {"k": "ink", "B": "bl_l", "b": "bl_m", "d": "bl_d", "G": "br_l", "Y": "br_m", "y": "br_d"})
    return f, pal


def charioteer():
    """Kebriones's kind: the long fluted chiton of a driver, girt high, crossed
    straps, a blue fillet with its ends flying; reins in his fists and the goad."""
    pal = Palette([
        ("ink", INK), *SKIN_TAN, ("brown", (104, 56, 40)),
        ("wh_l", (248, 248, 232)), ("wh_m", (216, 208, 184)), ("wh_d", (160, 152, 136)),
        ("bl_l", (128, 176, 232)), ("bl_m", (56, 104, 184)), ("bl_d", (32, 56, 120)),
        ("hair_l", (120, 72, 48)), ("hair_d", (64, 40, 32)),
        ("gold_l", (248, 208, 88)), ("gold_d", (184, 120, 40)),
    ])
    skin = skin_mat("brown")
    white = Mat(["wh_d", "wh_m", "wh_l"], outline="brown", wx=0.9, wy=0.15, cuts=[0.5, 0.82])
    lea = Mat(["brown"])
    f = Fig(pal)

    # the goad, held up behind him
    f.thick_line([(44, 31), (55, 3)], 2, lea, group=50)
    # long chiton to the ankles, a little flared at the hem
    body = f.poly([(26, 22), (38, 22), (40, 30), (40, 42), (42, 52), (44, 59), (20, 59), (22, 52),
                   (23, 42), (24, 30)], white)
    for x in (25, 28, 31, 34, 37, 40):  # the fluting of the Delphi charioteer
        f.shade_poly([(x, 34), (x + 1, 34), (x + 1 + (x - 32) // 5, 58), (x + (x - 32) // 5, 58)], 0.5)
    f.shade_poly([(24, 34), (26, 34), (24, 58), (21, 58)], -0.3)
    # bare feet
    f.poly([(25, 59), (30, 59), (30, 62), (24, 62)], skin, group=90)
    f.poly([(34, 59), (39, 59), (40, 62), (34, 62)], skin, group=91)
    f.rect(30, 19, 34, 24, skin, group=400)
    # high girdle
    f.rect(20, 31, 44, 32, Mat(["bl_d", "bl_m"], cuts=[0.6]), clip=body, noline=True)
    # arms forward, both fists on the reins
    f.thick_line([(26, 24), (21, 30), (17, 32)], 5, white, group=200)
    f.thick_line([(38, 24), (41, 30), (37, 34)], 5, white, group=300)
    f.thick_line([(20, 30), (15, 32)], 4, skin, group=210)
    f.thick_line([(38, 31), (33, 34)], 4, skin, group=310)

    # crossed straps, a gold boss where they meet
    f.line([(27, 23), (36, 30)], "ink")
    f.line([(37, 23), (28, 30)], "ink")
    f.line([(28, 23), (37, 30)], "brown")
    f.line([(36, 23), (27, 30)], "brown")
    f.pxs([(32, 26), (31, 26), (32, 27), (31, 27)], "gold_l")
    # reins: leather lines running off toward his team
    f.line([(12, 33), (8, 36), (4, 37), (0, 37)], "ink")
    f.line([(12, 34), (8, 37), (4, 38), (0, 38)], "brown")
    f.line([(30, 36), (24, 40), (16, 42), (8, 42), (0, 41)], "ink")
    f.line([(30, 37), (24, 41), (16, 43), (8, 43), (0, 42)], "brown")
    fist(f, 11, 30, "brown")
    fist(f, 29, 32, "brown")
    # goad tip
    P(f, 53, 0, """
        .k.
        kGk
        kgk
        .k.
    """, {"k": "ink", "G": "gold_l", "g": "gold_d"})
    # face: intent, mouth set
    face(f, 24, 10, FACE_M, "brown", white="wh_l", edits=[(6, 7, "skin_l")])
    # short curls, a blue fillet tied behind with its ends flying
    P(f, 22, 1, """
        ........kkkkkk........
        ......kkHhHHhHkk......
        .....kHhHHhHHhHHk.....
        ....kHHhHHHHhHHhHk....
        ...kHhHHhHHHHhHHHHk...
        ...kHHHHHHhHHHHhHHk...
        ..kBBBBBBBBBBBBbbbbkk.
        ..kbbbbbbbbbbbbbbbbdBk
        ..kHHhH.......HHhHkBbk
        ..kHH..........HHkkbk.
        ..kH...........Hk.kk..
        ...k............k.....
    """, {"k": "ink", "H": "hair_d", "h": "hair_l", "B": "bl_l", "b": "bl_m", "d": "bl_d"})
    return f, pal


def shepherd_ida():
    """Paris's kind, as the vase painters dressed him: a soft Phrygian cap with
    its peak falling forward, a sleeved tunic and trousers in diamond-work, a
    short throwing-crook, and a golden apple held up."""
    pal = Palette([
        ("ink", INK), *SKIN_FAIR, ("brown", (104, 56, 40)),
        ("red_l", (224, 96, 72)), ("red_m", (176, 48, 48)), ("red_d", (104, 32, 40)),
        ("saf_l", (248, 208, 104)), ("saf_m", (224, 152, 56)), ("saf_d", (160, 96, 40)),
        ("bl_m", (56, 104, 184)), ("bl_d", (32, 56, 120)),
        ("hair", (72, 48, 32)), ("wood", (176, 120, 72)),
    ])
    skin = skin_mat("brown")
    red = Mat(["red_d", "red_m", "red_l"], wx=0.8, wy=0.3, cuts=[0.3, 0.7])
    saf = Mat(["saf_d", "saf_m", "saf_l"], wx=0.85, wy=0.25, cuts=[0.3, 0.72])
    trou = Mat(["bl_d", "bl_m"], wx=0.8, wy=0.2, cuts=[0.62])
    wood = Mat(["brown", "wood"], cuts=[0.7])
    lea = Mat(["brown"])
    f = Fig(pal)

    # short red cloak pinned at the throat, falling behind
    f.poly([(26, 22), (40, 22), (45, 30), (47, 42), (43, 45), (37, 43), (24, 44), (21, 36)], red, bias=0.3)
    # trousers (anaxyrides), soft boots
    f.poly([(26, 43), (31, 43), (30, 50), (29, 57), (25, 57), (25, 50)], trou, group=100)
    f.poly([(34, 43), (39, 43), (40, 50), (42, 57), (38, 57), (36, 50)], trou, group=101)
    f.poly([(23, 56), (30, 56), (30, 61), (22, 61)], lea)
    f.poly([(37, 56), (43, 56), (45, 61), (37, 61)], lea)
    # saffron tunic to mid-thigh, belted
    body = f.poly([(26, 22), (39, 22), (41, 31), (43, 45), (23, 45), (24, 31)], saf)
    f.rect(21, 32, 44, 33, lea, clip=body, noline=True)
    f.rect(30, 19, 34, 24, skin, group=400)
    # the crook, held low at his side, its hooked end up
    pole(f, (16, 26), (14, 61), wood, group=60)
    # near arm down at his side (sleeved to the wrist)
    f.thick_line([(26, 24), (21, 30), (18, 34)], 5, saf, group=200)
    # far arm raised, the apple held up
    f.thick_line([(39, 24), (45, 22), (47, 15)], 5, saf, group=300)

    # diamond-work on the skirt, the Trojan pattern on Greek pots
    for x in range(25, 43, 4):
        f.pxs([(x + 1, 36), (x, 37), (x + 2, 37), (x + 1, 38)], "ink")
        f.pxs([(x + 3, 40), (x + 2, 41), (x + 4, 41), (x + 3, 42)], "ink")
    f.line([(23, 44), (42, 44)], "red_d")
    # zigzag down the trousers and sleeves
    for y in range(46, 56, 3):
        f.pxs([(27, y), (28, y + 1), (29, y)], "ink")
        f.pxs([(37, y), (38, y + 1), (39, y)], "ink")
    for (x, y) in ((40, 23), (43, 22), (45, 19), (46, 16), (23, 27), (21, 30)):
        f.pxs([(x, y), (x + 1, y + 1)], "ink")
    # crook head: the shepherd's short throwing stick
    P(f, 13, 21, """
        ..kkk.
        .kWwWk
        kWk.kk
        kWk...
        .kk...
    """, {"k": "ink", "W": "wood", "w": "brown"})
    fist(f, 13, 32, "brown")
    # the golden apple
    P(f, 43, 4, """
        ....kk..
        ...kgk..
        .kkkbkk.
        kSSSSssk
        kSWSSssk
        kSSSsssk
        kSSsssdk
        kSsssddk
        .kssddk.
        ..kkkk..
    """, {"k": "ink", "b": "brown", "g": "bl_m", "S": "saf_l", "s": "saf_m", "d": "saf_d", "W": "wood"})
    fist(f, 44, 13, "brown")
    # face, then the Phrygian cap: the peak falls forward, lappets at the cheeks
    face(f, 26, 10, FACE_M, "brown", white="saf_l", edits=SMILE)
    P(f, 21, 0, """
        .......kkkk.............
        .....kkRRRRkk...........
        ...kkRRRrrrrrk..........
        ..kRRRRkkrrrrrk.........
        .kRRkk..kRrrrrrk........
        .kRk...kRRrrrrrrkk......
        ..k...kRRRrrrrrrrrk.....
        .....kRRRrrrrrrrrrrk....
        ....kRRRrrrrrrrrrrrrdk..
        ....kRRrrrrrrrrrrrrrddk.
        ....kRrkkkkkkkkkkkkkrddk
        ....kRk.............krdk
        ....kRk..............kdk
        ....kRk..............kdk
        ....kRk..............kdk
        ....kRk.............krdk
        ....kRk.............kdk.
        ....kRk............krdk.
        .....kk...........krdk..
        ..................krk...
        ...................k....
    """, {"k": "ink", "R": "red_l", "r": "red_m", "d": "red_d", "H": "hair"})
    return f, pal


def prince_hektor():
    """Hektor of the shining helmet, as his son saw it (Iliad 6.466-473): the
    bronze and the horsehair crest nodding from the top, cheek pieces raised.
    A royal blue cloak bordered in black-figure meander, the great bronze shield
    of Troy on his arm and a long spear."""
    pal = Palette([
        ("ink", INK), *SKIN_TAN, ("brown", (104, 56, 40)),
        ("br_l", (248, 224, 136)), ("br_m", (216, 160, 64)), ("br_d", (152, 96, 40)), ("br_x", (88, 56, 32)),
        ("bl_l", (120, 160, 224)), ("bl_m", (56, 88, 168)), ("bl_d", (32, 40, 104)),
        ("crest", (96, 88, 104)), ("hair", (56, 40, 32)), ("lin", (240, 232, 208)),
    ])
    skin = skin_mat("brown")
    bronze = Mat(["br_x", "br_d", "br_m", "br_l"], cuts=[0.12, 0.42, 0.74])
    blue = Mat(["bl_d", "bl_m", "bl_l"], wx=0.85, wy=0.2, cuts=[0.25, 0.65])
    wood = Mat(["br_x", "br_d"], cuts=[0.7])
    lea = Mat(["brown"])
    f = Fig(pal)

    # the crest's long tail down his back
    f.poly([(42, 8), (47, 10), (51, 18), (53, 28), (50, 30), (47, 20), (43, 14)],
           Mat(["ink", "crest"], cuts=[0.55]), group=20)
    # royal cloak, wide behind him
    f.poly([(22, 22), (42, 21), (49, 28), (53, 40), (55, 52), (50, 54), (44, 51), (30, 53), (19, 50),
            (17, 38)], blue, bias=0.25)
    # the spear, long, held upright in his left hand
    pole(f, (11, 6), (11, 61), wood, group=50)
    # legs, greaves, sandals
    f.poly([(25, 45), (30, 45), (29, 51), (28, 57), (24, 57), (24, 51)], skin, group=100)
    f.poly([(35, 45), (39, 45), (41, 51), (42, 57), (38, 57), (36, 51)], skin, group=101)
    f.poly([(24, 49), (29, 49), (28, 57), (24, 57)], bronze, group=110)
    f.poly([(36, 49), (40, 49), (42, 57), (38, 57)], bronze, group=111)
    f.poly([(22, 57), (29, 57), (29, 61), (21, 61)], lea)
    f.poly([(37, 57), (43, 57), (45, 61), (37, 61)], lea)
    # linen skirt and bronze cuirass
    f.poly([(24, 38), (41, 38), (43, 47), (22, 47)], Mat(["br_d", "lin"], outline="brown", cuts=[0.7]))
    f.poly([(25, 21), (40, 21), (42, 30), (41, 40), (25, 40), (23, 30)], bronze)
    f.rect(29, 18, 34, 23, skin, group=400)
    # left arm out to the spear
    f.thick_line([(25, 23), (18, 28), (14, 30)], 5, skin, group=200)
    f.poly([(22, 21), (28, 21), (27, 26), (22, 27)], bronze, group=210)
    # the shield of Troy on his right arm: bronze rings and a boss
    rim = f.ellipse((33, 25, 60, 52), bronze, group=600)
    f.ellipse((36, 28, 57, 49), bronze, group=610, clip=rim, bias=0.15)
    f.ellipse((40, 32, 53, 45), bronze, group=620, clip=rim, bias=-0.1)
    f.ellipse((44, 36, 49, 41), bronze, group=630, clip=rim, bias=-0.3)

    # cuirass detail and skirt strips
    f.line([(32, 25), (32, 36)], "br_d")
    f.line([(26, 30), (29, 32), (32, 32)], "br_d")
    for x in (26, 29, 32, 35, 38):
        f.line([(x, 40), (x - 1, 46)], "brown")
    f.line([(25, 50), (25, 56)], "br_l")
    f.line([(38, 50), (39, 56)], "br_l")
    # meander on the cloak's hem, black-figure
    for x in range(18, 56, 4):
        f.pxs([(x, 52), (x + 1, 52), (x + 1, 51), (x + 2, 51)], "ink")
    f.line([(37, 27), (42, 26)], "br_l")
    f.line([(34, 33), (35, 30)], "br_l")
    fist(f, 8, 27, "brown")
    # spearhead
    P(f, 8, 0, """
        ..k..
        .kGk.
        .kGYk
        kGYYk
        kGYyk
        .kGyk
        .kYk.
        .kkk.
    """, {"k": "ink", "G": "br_l", "Y": "br_m", "y": "br_d"})
    # face: a full beard, steady, the start of a smile
    face(f, 23, 12, FACE_BEARD, "ink", white="lin", hair="hair",
         edits=[(5, 7, "hair"), (9, 7, "hair"), (6, 7, "ink"), (7, 7, "ink"), (8, 7, "ink"), (9, 6, "ink")])
    # the helmet, cheek pieces hinged up; the crest on a tall stilt
    P(f, 18, 0, """
        ..........kkkkkkkkkkk.......
        ........kkCcCCcCCcCCCkkk....
        ......kkCCcCCcCCcCCcCCCCkk..
        .....kCCcCCcCCcCCcCCcCCCCCk.
        ....kCCCkkkkkkkkkkkkCCcCCCCk
        ....kkkk....kGk.....kkkCcCCk
        ............kGk........kkCk.
        .........kkkkYkkkkk......k..
        ........kGGGGYYYYYYkk.......
        .......kGGYYYYYYYYYYyk......
        ...kk.kGGYYYYYYYYYYYyyk.kk..
        ..kGYkkGYYYYYYYYYYYYyyykYyk.
        ..kGYYkkkkkkkkkkkkkkkkkkyyk.
        ...kGYk..............kYyk...
        ....kk................kk....
    """, {"k": "ink", "C": "crest", "c": "bl_d", "G": "br_l", "Y": "br_m", "y": "br_d"})
    return f, pal


# ==========================================================================
# The Black Sea
# ==========================================================================

def argonaut():
    """A veteran of the Argo: a sailor's felt pilos, a gray-shot beard, an
    exomis with one shoulder bare, a sea-green chlamys, an oar upright beside
    him and a coil of rope at his belt."""
    pal = Palette([
        ("ink", INK), *SKIN_SUN, ("brown", (96, 56, 40)),
        ("felt_l", (224, 184, 120)), ("felt_m", (176, 128, 72)), ("felt_d", (112, 80, 48)),
        ("oat_l", (240, 224, 184)), ("oat_m", (200, 176, 128)),
        ("sea_l", (96, 176, 152)), ("sea_m", (48, 120, 112)), ("sea_d", (24, 72, 72)),
        ("gray", (184, 176, 168)), ("hair", (72, 56, 48)),
    ])
    skin = skin_mat("brown")
    sea = Mat(["sea_d", "sea_m", "sea_l"], wx=0.85, wy=0.25, cuts=[0.28, 0.68])
    oat = Mat(["oat_m", "oat_l"], outline="brown", wx=0.8, wy=0.3, cuts=[0.6])
    wood = Mat(["felt_d", "felt_m", "felt_l"], wx=1.0, wy=0.0, cuts=[0.3, 0.7])
    lea = Mat(["brown"])
    f = Fig(pal)

    # the oar, upright at his left: loom down to the ground, blade up high
    pole(f, (49, 14), (49, 61), wood, group=50)
    # sea-green chlamys pinned at the right shoulder, hanging behind
    f.poly([(24, 21), (39, 21), (44, 28), (46, 40), (44, 47), (38, 45), (24, 46), (19, 42), (20, 30)],
           sea, bias=0.25)
    # legs, sandals
    f.poly([(26, 44), (31, 44), (30, 50), (29, 57), (25, 57), (25, 50)], skin, group=100)
    f.poly([(35, 44), (39, 44), (40, 50), (42, 57), (38, 57), (36, 50)], skin, group=101)
    f.poly([(23, 57), (30, 57), (30, 61), (22, 61)], lea)
    f.poly([(37, 57), (43, 57), (45, 61), (37, 61)], lea)
    # exomis: off the near shoulder, belted, to the knee
    body = f.poly([(31, 22), (39, 22), (41, 31), (43, 46), (24, 46), (25, 33), (27, 27)], oat)
    f.rect(22, 34, 44, 35, lea, clip=body, noline=True)
    # bare near shoulder and chest
    f.poly([(25, 22), (31, 22), (28, 27), (26, 32), (24, 30)], skin, group=150)
    f.rect(29, 19, 34, 24, skin, group=400)
    # near arm: fist on his hip
    f.thick_line([(25, 24), (21, 30), (24, 35)], 5, skin, group=200)
    # far arm up to the oar
    f.thick_line([(39, 24), (44, 28), (47, 26)], 5, skin, group=300)
    # sea-green fold over the far shoulder
    f.poly([(35, 21), (41, 21), (44, 26), (40, 28), (37, 25)], sea, group=310)

    # folds, and a black hem band with the running wave in clay
    f.line([(31, 37), (30, 42)], "oat_m")
    f.line([(37, 37), (38, 42)], "oat_m")
    f.rect(22, 42, 45, 45, Mat(["ink"]), clip=body, noline=True)
    for x in range(24, 44, 4):
        f.pxs([(x, 44), (x + 1, 43), (x + 2, 43), (x + 2, 44), (x + 3, 44)], "oat_l")
    f.pxs([(36, 22), (37, 22)], "felt_l")  # bronze pin
    # coil of rope on his belt
    P(f, 35, 33, """
        ..kkkk..
        .kFFFfk.
        kFkkkkfk
        kFk..kfk
        kFfkkffk
        .kfffdk.
        ..kkkk..
    """, {"k": "ink", "F": "felt_l", "f": "felt_m", "d": "felt_d"})
    fist(f, 21, 31, "brown")
    fist(f, 46, 24, "brown")
    # the oar blade
    P(f, 46, 0, """
        ..kkk..
        .kFFfk.
        kFFffdk
        kFFffdk
        kFfffdk
        kFfffdk
        kFfffdk
        kFfffdk
        kFfffdk
        .kFffk.
        .kFfdk.
        ..kfk..
        ..kfk..
        ..kfk..
    """, {"k": "ink", "F": "felt_l", "f": "felt_m", "d": "felt_d"})
    # face: weathered, gray in the beard, squinting at a horizon
    face(f, 24, 11, FACE_BEARD, "ink", white="oat_l", hair="hair",
         edits=[(4, 2, "ink"), (5, 2, "skin_m"), (11, 2, "ink"), (12, 2, "skin_m"),
                (3, 7, "gray"), (12, 8, "gray"), (6, 9, "gray"), (2, 5, "gray"), (13, 4, "gray"),
                (5, 7, "hair"), (6, 7, "ink"), (7, 7, "ink"), (8, 7, "ink"), (9, 6, "ink")])
    # the pilos, a felt cone, and gray curls under it
    P(f, 22, 0, """
        ........kkkk..........
        .......kFFFfk.........
        ......kFFFffk.........
        ......kFFfffdk........
        .....kFFFfffdk........
        .....kFFffffddk.......
        ....kFFFffffddk.......
        ....kFFfffffdddk......
        ...kFFFfffffdddk......
        ...kFFffffffddddk.....
        ..kkkkkkkkkkkkkkkk....
        ..kgHgH.......HgHgk...
        ..kHg..........gHk....
        ...k............kk....
    """, {"k": "ink", "F": "felt_l", "f": "felt_m", "d": "felt_d", "H": "hair", "g": "gray"})
    return f, pal


def colchian_sorceress():
    """One of Medea's acolytes, as the vase painters dressed the women of the
    east: a dark veil drawn over the head, a gold band at the brow, a long-sleeved
    gown patterned in dots and zigzags; a bronze pyxis of herbs, and a green sprig
    smoking in her hand."""
    pal = Palette([
        ("ink", INK), *SKIN_OLIVE, ("brown", (96, 48, 48)),
        ("tl_l", (112, 184, 160)), ("tl_m", (56, 128, 120)), ("tl_d", (24, 72, 72)),
        ("pur_l", (152, 104, 168)), ("pur_m", (96, 56, 120)), ("pur_d", (48, 32, 72)),
        ("grn_l", (184, 240, 112)), ("grn_m", (104, 184, 72)),
        ("br_l", (248, 208, 112)), ("br_m", (192, 128, 56)),
    ])
    skin = skin_mat("brown")
    gown = Mat(["tl_d", "tl_m", "tl_l"], wx=0.85, wy=0.2, cuts=[0.28, 0.7])
    veil = Mat(["pur_d", "pur_m", "pur_l"], wx=0.85, wy=0.2, cuts=[0.3, 0.75])
    lea = Mat(["brown"])
    f = Fig(pal)

    # the veil, from over her head down her back
    f.poly([(25, 6), (40, 6), (45, 18), (47, 32), (47, 46), (41, 48), (35, 30)], veil, group=10)
    # long sleeved gown to the ground
    body = f.poly([(25, 22), (38, 22), (40, 30), (41, 40), (43, 52), (45, 60), (19, 60), (21, 52), (23, 40),
                   (23, 30)], gown)
    for x in (26, 31, 36, 41):
        f.shade_poly([(x, 42), (x + 1, 42), (x + 1 + (x - 33) // 5, 59), (x + (x - 33) // 5, 59)], 0.45)
    f.rect(18, 53, 46, 57, Mat(["ink"]), clip=body, noline=True)
    f.poly([(24, 60), (29, 60), (29, 62), (24, 62)], lea)
    f.poly([(34, 60), (39, 60), (39, 62), (34, 62)], lea)
    f.rect(29, 19, 33, 24, skin, group=400)
    # far arm: the pyxis held at her waist
    f.thick_line([(37, 24), (41, 31), (37, 36)], 5, gown, group=300)
    # near arm raised: the sprig held up beside her face
    f.thick_line([(25, 24), (20, 30), (17, 24)], 5, gown, group=200)

    # gold dots, and a zigzag band in clay on black: the "eastern" pattern on Greek pots
    for (x, y) in stagger(24, 26, 40, 50, 4, 4):
        f.px(x, y, "br_l")
    for x in range(19, 46, 2):
        f.pxs([(x, 54 + (x // 2) % 2 * 2), (x + 1, 55)], "br_m")
    f.line([(22, 24), (18, 28)], "tl_l")
    # the bronze pyxis
    P(f, 31, 33, """
        .kkkkkk.
        kBBBBbbk
        kkkkkkkk
        kBbbbbbk
        kBbkkbbk
        kBbbbbbk
        .kkkkkk.
    """, {"k": "ink", "B": "br_l", "b": "br_m"})
    fist(f, 35, 33, "brown")
    # sprig and its green smoke
    P(f, 10, 6, """
        ...G....G..
        ..G.g..g...
        ...g..G....
        ..kk..g....
        .kGGk.kk...
        kGGgk.kGk..
        .kkgkkGgk..
        ...kgkkk...
        ..kGgk.....
        .kGGkgk....
        ..kk.kgk...
        .....kgk...
        ......kgk..
        ......kgk..
    """, {"k": "ink", "G": "grn_l", "g": "grn_m"})
    fist(f, 15, 18, "brown")
    # face: watchful, lips dark
    face(f, 24, 10, FACE_F, "brown", white="br_l", lips="pur_m")
    # the veil drawn over her head, a gold band at the brow, black hair at the temples
    P(f, 22, 1, """
        .......kkkkkk........
        .....kkPPPPPpkk......
        ....kPPPPPpppppk.....
        ...kPPPPpppppppdk....
        ..kPPPPpppppppppdk...
        ..kPPPpppppppppppdk..
        .kPPPpppppppppppppdk.
        .kPPpppppppppppppddk.
        .kPkBBBBBBBBBBBbbkddk
        .kPkHHH.......HHHkpdk
        .kPkH............kpdk
        .kPk.............kpdk
        .kPk.............kpdk
        .kPk.............kpdk
        .kPk............kppdk
        .kPPk...........kpdk.
        ..kPk..........kppdk.
        ..kPPk........kkpdk..
        ...kPk........kppdk..
        ...kPPk......kpppdk..
        ....kk......kppdkk...
    """, {"k": "ink", "P": "pur_l", "p": "pur_m", "d": "pur_d", "B": "br_l", "b": "br_m", "H": "pur_d"})
    return f, pal


def chalybes_smith():
    """Iron country: a smith of the Chalybes, who worked iron before anyone. A
    felt cap, a leather apron, soot; the hammer on his shoulder and a bar of hot
    iron held out in the tongs."""
    pal = Palette([
        ("ink", INK), *SKIN_TAN, ("brown", (96, 56, 40)),
        ("lea_l", (176, 112, 64)), ("lea_m", (120, 72, 48)),
        ("ir_l", (208, 216, 224)), ("ir_m", (136, 144, 160)), ("ir_d", (72, 80, 96)),
        ("hot_y", (248, 232, 112)), ("hot_r", (232, 96, 40)),
        ("felt_l", (200, 160, 104)), ("felt_d", (136, 96, 64)),
        ("hair", (40, 32, 32)),
    ])
    skin = skin_mat("brown")
    apron = Mat(["lea_m", "lea_l"], outline="ink", wx=0.8, wy=0.3, cuts=[0.62])
    felt = Mat(["felt_d", "felt_l"], wx=0.85, wy=0.3, cuts=[0.6])
    lea = Mat(["brown"])
    f = Fig(pal)

    # legs planted wide
    f.poly([(25, 44), (30, 44), (29, 50), (27, 57), (23, 57), (24, 50)], skin, group=100)
    f.poly([(35, 44), (39, 44), (41, 50), (43, 57), (39, 57), (37, 50)], skin, group=101)
    f.poly([(21, 57), (28, 57), (28, 61), (20, 61)], lea)
    f.poly([(38, 57), (44, 57), (46, 61), (38, 61)], lea)
    # short felt tunic, a big chest
    f.poly([(24, 22), (41, 22), (43, 31), (43, 46), (22, 46), (22, 31)], felt)
    # leather apron
    f.poly([(25, 28), (40, 28), (41, 38), (42, 49), (23, 49), (24, 38)], apron)
    f.rect(29, 18, 34, 23, skin, group=400)
    # far arm up: the hammer on his shoulder
    f.thick_line([(40, 24), (46, 30), (45, 22)], 6, skin, group=300)
    f.thick_line([(44, 25), (40, 4)], 3, Mat(["felt_d", "felt_l"], cuts=[0.6]), group=310)
    # near arm out: the tongs
    f.thick_line([(25, 24), (19, 30), (14, 32)], 6, skin, group=200)

    # apron strap, folds and stitching
    f.line([(25, 28), (31, 23)], "lea_m")
    f.line([(29, 38), (28, 48)], "lea_m")
    f.line([(36, 38), (37, 48)], "lea_m")
    f.pxs([(27, 40), (30, 41), (34, 41), (37, 40)], "lea_m")
    # soot on the apron and arm
    f.pxs([(28, 44), (29, 45), (36, 46), (20, 29), (39, 33)], "ir_d")
    # the hammer's head
    P(f, 34, 0, """
        .kkkkkkkkk..
        kIIIiiiiidk.
        kIIiiiiiiddk
        kkkkkkkkkkk.
    """, {"k": "ink", "I": "ir_l", "i": "ir_m", "d": "ir_d"})
    fist(f, 42, 21, "brown")
    # tongs and the bar of hot iron
    P(f, 0, 27, """
        .kkkkkk.........
        kYYYYYRk........
        kYWYYRRkkkkkkkk.
        kRRRRRRkiiiiiik.
        .kkkkkkkkkkkkkk.
        ........kiiik...
        .........kkk....
    """, {"k": "ink", "Y": "hot_y", "R": "hot_r", "W": "ir_l", "i": "ir_m"})
    fist(f, 12, 29, "brown")
    # sparks
    f.pxs([(3, 23), (8, 21), (1, 20), (6, 25)], "hot_y")
    f.pxs([(5, 22), (10, 24)], "hot_r")
    # face: a black beard, soot on the cheek, a grin
    face(f, 24, 10, FACE_BEARD, "ink", white="ir_l", hair="hair",
         edits=[(6, 7, "ir_l"), (7, 7, "ir_l"), (8, 7, "ir_l"), (3, 3, "ir_d"), (2, 4, "ir_d")])
    # felt cap, Hephaestus's kind, over cropped black hair
    P(f, 22, 0, """
        ........kkkk.........
        ......kkFFFfkk.......
        .....kFFFffffdk......
        ....kFFFfffffddk.....
        ....kFFffffffddk.....
        ...kFFfffffffdddk....
        ...kFffffffffdddk....
        ..kkkkkkkkkkkkkkkk...
        ..kHHHHHHHHHHHHHHk...
        ..kHH..........HHk...
        ..kH............Hk...
        ...k............k....
    """, {"k": "ink", "F": "felt_l", "f": "felt_d", "d": "lea_m", "H": "hair"})
    return f, pal


def priestess_medea():
    """Medea, priestess of Hecate, in Aietes's palace: the patterned gown and
    tall gold diadem the vase painters gave her, long black hair, a bronze ladle
    of the brew that makes old things young. Curious, and a little dangerous."""
    pal = Palette([
        ("ink", INK), *SKIN_OLIVE, ("brown", (88, 48, 48)),
        ("hair", (40, 32, 48)), ("hair_l", (88, 72, 112)),
        ("pur_l", (184, 88, 160)), ("pur_m", (128, 40, 112)), ("pur_d", (72, 24, 72)),
        ("gold_l", (248, 216, 104)), ("gold_m", (200, 144, 56)),
        ("grn_l", (176, 248, 120)), ("grn_m", (64, 176, 96)),
        ("wh", (248, 240, 224)),
    ])
    skin = skin_mat("brown")
    gown = Mat(["pur_d", "pur_m", "pur_l"], wx=0.85, wy=0.2, cuts=[0.26, 0.68])
    gold = Mat(["gold_m", "gold_l"], cuts=[0.6])
    hair = Mat(["hair", "hair_l"], wx=0.6, wy=0.5, cuts=[0.8])
    lea = Mat(["brown"])
    f = Fig(pal)

    # long black hair falling behind her to the waist
    f.poly([(25, 8), (42, 8), (46, 18), (48, 32), (46, 42), (38, 40), (24, 40), (21, 30), (22, 18)], hair,
           group=10)
    # gown to the ground, a gold meander band at the hem
    body = f.poly([(25, 22), (38, 22), (40, 30), (41, 40), (43, 52), (46, 60), (17, 60), (20, 52), (22, 40),
                   (23, 30)], gown)
    for x in (24, 29, 34, 39):
        f.shade_poly([(x, 41), (x + 1, 41), (x + 1 + (x - 31) // 5, 59), (x + (x - 31) // 5, 59)], 0.45)
    f.rect(16, 53, 47, 57, Mat(["ink"]), clip=body, noline=True)
    f.rect(16, 36, 47, 37, gold, clip=body, noline=True)
    f.poly([(24, 60), (29, 60), (29, 62), (24, 62)], lea)
    f.poly([(34, 60), (39, 60), (39, 62), (34, 62)], lea)
    f.rect(29, 19, 33, 24, skin, group=400)
    # far hand up at her chin: curious
    f.thick_line([(37, 24), (42, 30), (39, 24)], 5, gown, group=300)
    # near arm out: the ladle
    f.thick_line([(25, 24), (20, 31), (15, 33)], 5, gown, group=200)

    # gold meander on the hem band, clay on black, black-figure
    for x in range(17, 47, 4):
        f.pxs([(x, 54), (x + 1, 54), (x + 2, 54), (x + 2, 55), (x, 55), (x, 56), (x + 1, 56), (x + 2, 56),
               (x + 3, 56)], "gold_m")
    # dots on the gown
    for (x, y) in stagger(24, 27, 39, 50, 4, 4):
        f.px(x, y, "pur_l")
    f.line([(22, 25), (18, 30)], "pur_l")
    # the bronze ladle, and the brew dripping green
    P(f, 0, 26, """
        ....kkkkk.....
        ..kkGGggkk....
        .kGGkkkkgGkkk.
        .kGgggggggkkGk
        ..kgGLgggk.kkk
        ...kkkkkk.....
        .....kLk......
        ......k.......
        .....kLk......
        ......k.......
    """, {"k": "ink", "G": "gold_l", "g": "gold_m", "L": "grn_l"})
    f.pxs([(3, 30), (4, 30), (5, 30), (6, 30), (7, 30), (8, 30)], "grn_m")
    f.pxs([(4, 30), (6, 30)], "grn_l")
    fist(f, 12, 30, "brown")
    # face: head a little on one side, one brow up, a small smile
    face(f, 24, 10, FACE_F, "brown", white="wh", lips="pur_m",
         edits=[(4, 0, "ink"), (5, 0, "ink"), (4, 1, "skin_l"), (11, 1, "ink"), (12, 1, "ink"),
                (6, 6, "ink"), (7, 6, "pur_m"), (8, 6, "pur_m"), (9, 5, "ink")])
    # the tall gold diadem, black hair parted over it
    P(f, 22, 0, """
        .....kkkkkkkk.......
        ....kGkGkGkGkk......
        ....kGgGgGgGgk......
        ....kGgGgGgGgk......
        ....kkkkkkkkkkk.....
        ...kHhHHHHHHHHHk....
        ..kHHhHHHHHHHhHHk...
        ..kHHHHHHHhHHHHHk...
        ..kHHHHHHHHHHHHHHk..
        ..kHHHH.......HHHk..
        ..kHHk..........HHk.
        ..kHk...........HHk.
        ..kHk...........HHk.
        ..kHk...........HHk.
        ..kHk...........HHk.
        ..kHk...........HHk.
        ...kHk.........kHk..
        ....k...........k...
    """, {"k": "ink", "G": "gold_l", "g": "gold_m", "H": "hair", "h": "hair_l"})
    # her fingers at her chin
    P(f, 35, 18, """
        .bbb.
        bLLLb
        bLbLb
        bLLMb
        .bbb.
    """, {"b": "brown", "L": "skin_l", "M": "skin_m"})
    return f, pal


# ==========================================================================
# Egypt, as the Greeks painted it: shaved heads and linen, kohl, broad collars
# ==========================================================================

def sun_priest():
    """A priest of Heliopolis: a shaved head, the leopard skin of his office over
    white linen, a broad collar, the sun's gold disk held up on its staff."""
    pal = Palette([
        ("ink", INK), *SKIN_NILE, ("brown", (88, 48, 32)),
        ("lin_l", (248, 248, 232)), ("lin_m", (216, 208, 184)), ("lin_d", (160, 152, 136)),
        ("leo_l", (240, 192, 96)), ("leo_m", (200, 136, 56)),
        ("gold_l", (248, 224, 104)), ("gold_m", (232, 160, 48)), ("gold_d", (168, 96, 32)),
        ("lap", (48, 88, 176)), ("red", (216, 64, 40)),
    ])
    skin = skin_mat("brown")
    linen = Mat(["lin_d", "lin_m", "lin_l"], outline="brown", wx=0.85, wy=0.2, cuts=[0.5, 0.82])
    leo = Mat(["leo_m", "leo_l"], outline="brown", wx=0.8, wy=0.3, cuts=[0.6])
    wood = Mat(["gold_d", "gold_m"], cuts=[0.7])
    f = Fig(pal)

    # the staff, held upright at his left
    pole(f, (12, 14), (12, 61), wood, group=50)
    # long linen robe
    body = f.poly([(26, 22), (38, 22), (40, 32), (41, 44), (43, 59), (21, 59), (23, 44), (24, 32)], linen)
    for x in (27, 32, 37):
        f.shade_poly([(x, 40), (x + 1, 40), (x + 1 + (x - 32) // 5, 58), (x + (x - 32) // 5, 58)], 0.5)
    f.rect(19, 53, 45, 57, Mat(["ink"]), clip=body, noline=True)
    f.poly([(24, 59), (29, 59), (29, 62), (24, 62)], skin, group=90)
    f.poly([(34, 59), (39, 59), (40, 62), (34, 62)], skin, group=91)
    # the leopard skin over the far shoulder, its paws at his hip
    f.poly([(31, 23), (40, 22), (43, 30), (43, 44), (40, 50), (35, 46), (33, 36), (28, 30)], leo)
    f.rect(29, 19, 34, 24, skin, group=400)
    # broad collar
    f.poly([(25, 22), (39, 22), (40, 25), (35, 28), (29, 28), (24, 25)], Mat(["lap", "gold_l"], cuts=[0.5]),
           group=420)
    # near arm to the staff
    f.thick_line([(25, 24), (19, 29), (15, 30)], 5, skin, group=200)
    # far arm raised, palm out to the sun
    f.thick_line([(39, 24), (45, 25), (47, 18)], 5, skin, group=300)

    # leopard spots
    for (x, y) in stagger(32, 25, 42, 47, 3, 3):
        f.px(x, y, "ink")
    # the hem: sun disks and rays in clay on black
    for x in range(22, 43, 5):
        f.pxs([(x, 55), (x + 1, 55), (x, 56), (x + 1, 56), (x - 1, 54), (x + 2, 54), (x - 1, 57), (x + 2, 57)],
              "gold_m")
    # collar bands
    f.line([(26, 24), (29, 26), (35, 26), (38, 24)], "gold_l")
    f.line([(27, 25), (30, 27), (34, 27), (37, 25)], "red")
    fist(f, 9, 27, "brown")
    # open palm
    P(f, 44, 11, """
        .k.k...
        kLkLkk.
        kLkLkLk
        kLLLLLk
        kLLLLMk
        .kLLMk.
        ..kMk..
    """, {"k": "brown", "L": "skin_l", "M": "skin_m"})
    # the sun disk on the staff, rayed
    P(f, 3, 1, """
        ....k.k.k....
        .k...kkk...k.
        ..k.kGGgk.k..
        ...kGGGggk...
        .kkGGWGgggkk.
        ..kGGGggggk..
        ..kGGggggdk..
        .kkGgggggdkk.
        ...kgggddk...
        ..k.kkkkk.k..
        .k...kRk...k.
        .....kRk.....
        .....kkk.....
    """, {"k": "ink", "G": "gold_l", "g": "gold_m", "d": "gold_d", "W": "lin_l", "R": "red"})
    # face: kohl-lined eyes, serene
    face(f, 24, 9, FACE_KOHL, "brown", white="lin_l",
         edits=[(6, 7, "skin_m"), (7, 7, "ink"), (8, 7, "ink"), (9, 7, "skin_m")])
    # the shaved head
    P(f, 22, 0, """
        ........kkkkkkk.......
        ......kkLLLLLMMkk.....
        .....kLLLLLLLLMMDk....
        ....kLLLLLLLLLLMMDk...
        ...kLLWLLLLLLLLMMDDk..
        ...kLLLLLLLLLLLMMMDk..
        ..kLLLLLLLLLLLLLMMDDk.
        ..kLLLLLLLLLLLLLMMDDk.
        ..kLLLLLLLLLLLLLMMMDk.
        ..oL.............MMDk.
        ..o...............MDo.
        ..................Mo..
        ..................o...
    """, {"k": "ink", "o": "brown", "L": "skin_l", "M": "skin_m", "D": "skin_d", "W": "lin_l"})
    return f, pal


def scribe_thoth():
    """A scribe of Thoth: a short black wig, a white kilt, a broad collar, an
    open papyrus of riddles in hieroglyphs, a reed pen behind his ear and the
    scribe's palette with its red and black wells."""
    pal = Palette([
        ("ink", INK), *SKIN_NILE, ("brown", (88, 48, 32)),
        ("wig", (56, 56, 88)),
        ("lin_l", (248, 248, 232)), ("lin_m", (216, 208, 184)), ("lin_d", (160, 152, 136)),
        ("pap_l", (248, 232, 176)), ("pap_m", (208, 184, 120)),
        ("lap_l", (96, 144, 216)), ("lap_d", (40, 64, 144)),
        ("red", (200, 56, 40)), ("mal", (64, 160, 112)),
    ])
    skin = skin_mat("brown")
    linen = Mat(["lin_d", "lin_m", "lin_l"], outline="brown", wx=0.85, wy=0.2, cuts=[0.5, 0.82])
    pap = Mat(["pap_m", "pap_l"], outline="brown", wx=0.6, wy=0.4, cuts=[0.62])
    f = Fig(pal)

    # legs, bare feet
    f.poly([(26, 45), (31, 45), (30, 51), (29, 58), (25, 58), (25, 51)], skin, group=100)
    f.poly([(34, 45), (38, 45), (39, 51), (41, 58), (37, 58), (35, 51)], skin, group=101)
    f.poly([(24, 58), (30, 58), (30, 61), (23, 61)], skin, group=102)
    f.poly([(36, 58), (42, 58), (43, 61), (36, 61)], skin, group=103)
    # bare torso, kilt to the knee with a front panel
    f.poly([(26, 22), (38, 22), (40, 30), (39, 38), (25, 38), (24, 30)], skin, group=150)
    kilt = f.poly([(24, 36), (40, 36), (42, 48), (22, 48)], linen)
    f.poly([(30, 38), (35, 38), (36, 48), (29, 48)], linen, group=160, bias=-0.2)
    f.rect(22, 36, 42, 37, Mat(["lap_d", "lap_l"], cuts=[0.5]), clip=kilt, noline=True)
    f.rect(29, 19, 34, 24, skin, group=400)
    # broad collar
    f.poly([(25, 22), (39, 22), (40, 25), (35, 28), (29, 28), (24, 25)], Mat(["lap_d", "lap_l"], cuts=[0.5]),
           group=420)
    # the palette tucked under the far arm
    f.poly([(40, 26), (44, 25), (49, 46), (45, 47)], Mat(["pap_m"], outline="ink"), group=290)
    f.thick_line([(39, 24), (43, 31), (40, 36)], 5, skin, group=300)
    # near arm out, the papyrus unrolled toward you
    f.thick_line([(25, 24), (20, 30), (17, 34)], 5, skin, group=200)
    f.poly([(4, 28), (22, 31), (22, 44), (4, 41)], pap, group=500)

    # collar bands
    f.line([(26, 24), (29, 26), (35, 26), (38, 24)], "red")
    f.line([(27, 25), (30, 27), (34, 27), (37, 25)], "mal")
    # the palette's wells, red and black
    f.pxs([(44, 29), (45, 31)], "red")
    f.pxs([(45, 33), (46, 35)], "ink")
    # pleats, and a black hem band with a clay zigzag
    f.line([(26, 39), (24, 45)], "lin_d")
    f.line([(38, 39), (40, 45)], "lin_d")
    f.rect(20, 46, 44, 48, Mat(["ink"]), clip=kilt, noline=True)
    for x in range(22, 43, 2):
        f.px(x, 46 + (x // 2) % 2, "pap_m")
    # papyrus: rolled ends and three columns of hieroglyphs
    f.line([(3, 28), (3, 41)], "ink")
    f.line([(4, 28), (4, 41)], "pap_m")
    f.line([(22, 31), (22, 44)], "pap_m")
    P(f, 6, 31, """
        k..k.kk.....
        kk...k..kk..
        .....kk..k..
        .kk......k..
        .k..kk..kk..
        ......k.....
        .kk.kk..k.k.
        .k......kk..
        .....k......
    """, {"k": "ink"})
    f.pxs([(7, 39), (12, 33), (16, 38)], "red")
    fist(f, 16, 31, "brown")
    fist(f, 38, 32, "brown")
    # face: kohl-lined eyes, a thinking mouth
    face(f, 24, 10, FACE_KOHL, "brown", white="lin_l",
         edits=[(6, 7, "skin_l"), (7, 7, "ink"), (8, 7, "ink")])
    # the short black wig, a reed pen behind the ear
    P(f, 22, 1, """
        ........kkkkkk........
        ......kkWWwWWWkk......
        .....kWWwWWWWwWWk.....
        ....kWwWWWWwWWWWWk....
        ...kWWWWwWWWWWwWWk....
        ...kWwWWWWWWWWWWWWk...
        ..kWWWWWWWWwWWWWWWk...
        ..kWWW.......WWWWWWk..
        ..kWWk..........WWWk..
        ..kWk...........WWWWk.
        ..kWk...........WWWWk.
        ..kWk...........WWWWk.
        ..kWk...........kWWWk.
        ...kk............kkk..
    """, {"k": "ink", "W": "ink", "w": "wig"})
    P(f, 38, 3, """
        ....k.
        ...kRk
        ..kPk.
        .kPk..
        kPk...
        kk....
    """, {"k": "ink", "P": "pap_m", "R": "red"})
    return f, pal


def embalmer():
    """The embalmer of the Valley of Tombs: Anubis's black jackal mask pushed up
    on his head, white linen, a roll of bandage unspooling between his hands, and
    something pale and violet drifting out of it."""
    pal = Palette([
        ("ink", INK), *SKIN_NILE, ("brown", (88, 48, 32)),
        ("jk", (64, 64, 88)),
        ("gold_l", (248, 216, 96)), ("gold_d", (184, 120, 40)),
        ("lin_l", (248, 248, 232)), ("lin_m", (216, 208, 184)), ("lin_d", (160, 152, 136)),
        ("vio_l", (200, 176, 240)), ("vio_d", (120, 96, 176)),
        ("lap", (48, 88, 176)),
    ])
    skin = skin_mat("brown")
    linen = Mat(["lin_d", "lin_m", "lin_l"], outline="brown", wx=0.85, wy=0.2, cuts=[0.5, 0.82])
    f = Fig(pal)

    # long linen robe, wrapped
    body = f.poly([(26, 22), (38, 22), (40, 32), (41, 44), (43, 59), (21, 59), (23, 44), (24, 32)], linen)
    for x in (27, 32, 37):
        f.shade_poly([(x, 40), (x + 1, 40), (x + 1 + (x - 32) // 5, 58), (x + (x - 32) // 5, 58)], 0.5)
    f.shade_poly([(24, 30), (40, 38), (40, 40), (24, 32)], 0.5)
    f.rect(19, 53, 45, 57, Mat(["ink"]), clip=body, noline=True)
    f.poly([(24, 59), (29, 59), (29, 62), (24, 62)], skin, group=90)
    f.poly([(34, 59), (39, 59), (40, 62), (34, 62)], skin, group=91)
    f.rect(29, 19, 34, 24, skin, group=400)
    f.poly([(25, 22), (39, 22), (40, 25), (35, 28), (29, 28), (24, 25)], Mat(["lap", "gold_l"], cuts=[0.5]),
           group=420)
    # both arms forward, holding the bandage
    f.thick_line([(25, 24), (20, 31), (18, 36)], 5, skin, group=200)
    f.thick_line([(39, 24), (43, 31), (40, 37)], 5, skin, group=300)

    # the bandage, looping down between his hands
    f.thick_line([(19, 37), (22, 46), (30, 50), (37, 46), (40, 39)], 3, Mat(["lin_m", "lin_l"], outline="brown",
                                                                             cuts=[0.5]), group=500)
    f.line([(26, 24), (29, 26), (35, 26), (38, 24)], "gold_l")
    # the hem: a file of jackals, recumbent, in clay on black
    for x in range(21, 43, 6):
        f.pxs([(x, 56), (x + 1, 56), (x + 2, 56), (x + 3, 56), (x + 3, 55), (x + 4, 54), (x + 3, 54),
               (x + 4, 55), (x + 5, 55)], "lin_d")
    fist(f, 15, 34, "brown")
    fist(f, 38, 35, "brown")
    # the roll in his near hand
    P(f, 10, 33, """
        .kkkk.
        kWWwwk
        kWkkwk
        kWWwwk
        .kkkk.
    """, {"k": "brown", "W": "lin_l", "w": "lin_m"})
    # something leaving: violet wisps
    P(f, 2, 14, """
        ..vv......
        .vVVv.....
        .vVVVv....
        ..vVVv....
        ...vVVv...
        ....vVv...
        ....vVVv..
        .....vVv..
        .....vVVv.
        ......vVv.
        .......vv.
    """, {"v": "vio_d", "V": "vio_l"})
    P(f, 45, 38, """
        .vv....
        vVVv...
        .vVVv..
        ..vVv..
        ..vVVv.
        ...vv..
    """, {"v": "vio_d", "V": "vio_l"})
    # face: kohl, a calm and slightly sleepy look
    face(f, 24, 12, FACE_KOHL, "brown", white="lin_l",
         edits=[(5, 2, "ink"), (12, 2, "ink"), (6, 7, "skin_l"), (7, 7, "ink"), (8, 7, "ink")])
    # Anubis pushed up on his head: black jackal head, gold-lined ears and eye
    P(f, 15, 0, """
        ..................k...k.
        .................kjk.kjk
        .................kgjkkgk
        ................kjgjkkgk
        ................kjjjjjjk
        ...............kjjjjjjjk
        ...kkkkkkkkkkkkjjGjjjjjk
        ..kjjjjjjjjjjjjjjjjjjjjk
        .kjjjjjjjjjjjjjjjjjjjjjk
        ..kkkjjjjjjjjjjjjjjjjjjk
        .....kkkkkkkjjjjjjjjjjk.
        .........kGgGgGgGgGgGgk.
        .........kkkkkkkkkkkkkk.
        .........kJ.........JJk.
        .........kJk........Jk..
        ..........k..........k..
    """, {"k": "ink", "J": "ink", "j": "ink", "g": "gold_d", "G": "gold_l"})
    f.pxs([(19, 7), (23, 7), (27, 8), (31, 8), (35, 9), (34, 2), (36, 5)], "jk")
    return f, pal


def nile_boatman():
    """A boatman of the Nile: a striped headcloth, a white kilt, a punting pole
    with its forked foot, a coil of rope, and the day's fish."""
    pal = Palette([
        ("ink", INK), *SKIN_NILE, ("brown", (88, 48, 32)),
        ("wood_l", (200, 152, 96)), ("wood_d", (136, 88, 48)),
        ("lin_l", (248, 248, 232)), ("lin_d", (200, 192, 168)),
        ("bl_l", (120, 184, 224)), ("bl_m", (48, 112, 176)), ("bl_d", (24, 56, 112)),
        ("grn_l", (144, 192, 88)), ("grn_d", (72, 120, 48)),
        ("fish", (208, 216, 216)),
    ])
    skin = skin_mat("brown")
    linen = Mat(["lin_d", "lin_l"], outline="brown", wx=0.8, wy=0.3, cuts=[0.62])
    wood = Mat(["wood_d", "wood_l"], cuts=[0.7])
    f = Fig(pal)

    # the pole, leaning across him: foot forward at the bottom left
    pole(f, (51, 2), (13, 61), wood, group=50)
    # legs, bare feet
    f.poly([(26, 44), (31, 44), (30, 50), (29, 57), (25, 57), (25, 50)], skin, group=100)
    f.poly([(35, 44), (39, 44), (40, 50), (42, 57), (38, 57), (36, 50)], skin, group=101)
    f.poly([(23, 57), (30, 57), (30, 61), (22, 61)], skin, group=102)
    f.poly([(37, 57), (43, 57), (44, 61), (37, 61)], skin, group=103)
    # bare torso, kilt
    f.poly([(26, 22), (39, 22), (41, 30), (40, 38), (25, 38), (24, 30)], skin, group=150)
    kilt = f.poly([(24, 36), (41, 36), (43, 47), (22, 47)], linen)
    f.rect(20, 45, 45, 47, Mat(["ink"]), clip=kilt, noline=True)
    f.rect(29, 19, 34, 24, skin, group=400)
    # both hands on the pole
    f.thick_line([(26, 24), (24, 31), (29, 34)], 5, skin, group=200)
    f.thick_line([(39, 24), (44, 21), (45, 16)], 5, skin, group=300)

    # rope belt, papyrus reed tucked in
    f.line([(23, 37), (41, 37)], "wood_d")
    f.pxs([(25, 36), (28, 36), (31, 36), (34, 36), (37, 36), (40, 36)], "wood_l")
    f.line([(39, 38), (45, 28)], "grn_d")
    f.pxs([(45, 27), (46, 26), (44, 26), (46, 28)], "grn_l")
    # chest and kilt pleats
    f.line([(30, 28), (32, 29), (35, 28)], "skin_m")
    f.line([(27, 39), (26, 44)], "lin_d")
    f.line([(32, 39), (32, 44)], "lin_d")
    f.line([(37, 39), (38, 44)], "lin_d")
    for x in range(23, 43, 2):
        f.px(x, 45 + (x // 2) % 2, "wood_l")
    fist(f, 27, 31, "brown")
    fist(f, 43, 13, "brown")
    # the fork of the pole, and the fish hung on it by the gill
    P(f, 9, 54, """
        .kk.kk.
        kWk.kWk
        kWkkkWk
        .kWWWk.
    """, {"k": "ink", "W": "wood_l"})
    P(f, 40, 38, """
        ..kk......
        .kWk......
        .kWk......
        kFFFk.....
        kFkFFk....
        kFFFFk....
        kFFFFk....
        .kFFk.....
        .kFFk.....
        kFkkFk....
        kk..kk....
    """, {"k": "ink", "F": "fish", "W": "wood_d"})
    # drips off the pole's foot
    f.pxs([(7, 52), (6, 55), (17, 50)], "bl_l")
    # face: kohl, a squint against the river glare, a grin
    face(f, 24, 11, FACE_KOHL, "brown", white="lin_l",
         edits=[(5, 2, "ink"), (12, 2, "ink"), (6, 7, "lin_l"), (7, 7, "lin_l"), (8, 7, "lin_l"),
                (5, 7, "ink"), (9, 7, "ink")])
    # the striped headcloth, tied behind, its tail on his shoulder
    P(f, 22, 2, """
        ........kkkkkk........
        ......kkWWWWWWkk......
        .....kWWBBBBBBWWk.....
        ....kWBBWWWWWWBBWk....
        ...kWWWWBBBBBBWWWWk...
        ...kBBBBWWWWWWBBBBk...
        ..kWWWWWWWWWWWWWWWWk..
        ..kkkkkkkkkkkkkkkkkWk.
        ..kWBk..........kBWWk.
        ..kWk...........kWBWk.
        ..kBk...........kBWBk.
        ...k............kWBWWk
        ................kBWBk.
        .................kkk..
    """, {"k": "ink", "W": "lin_l", "B": "bl_m"})
    return f, pal


def phoenician_trader():
    """A trader of Tyre, from the Tyrians' Camp at Memphis: a robe of the purple
    his city is named for, fringed; a conical cap, a curled black beard, gold in
    his ear, and the bronze balance held up for your inspection."""
    pal = Palette([
        ("ink", INK), *SKIN_OLIVE, ("brown", (88, 48, 48)),
        ("pur_l", (216, 96, 128)), ("pur_m", (160, 40, 88)), ("pur_d", (88, 24, 56)),
        ("gold_l", (248, 224, 120)), ("gold_m", (216, 160, 56)), ("gold_d", (144, 88, 32)),
        ("hair", (40, 32, 40)), ("hair_l", (88, 72, 88)),
        ("wh_l", (248, 240, 224)), ("wh_d", (200, 184, 168)),
    ])
    skin = skin_mat("brown")
    robe = Mat(["pur_d", "pur_m", "pur_l"], wx=0.85, wy=0.2, cuts=[0.26, 0.68])
    gold = Mat(["gold_d", "gold_m", "gold_l"], cuts=[0.3, 0.7])
    lea = Mat(["brown"])
    f = Fig(pal)

    # long robe, fringed at the hem
    body = f.poly([(25, 22), (39, 22), (41, 31), (42, 42), (44, 58), (20, 58), (22, 42), (23, 31)], robe)
    for x in (26, 31, 36, 41):
        f.shade_poly([(x, 40), (x + 1, 40), (x + 1 + (x - 33) // 5, 57), (x + (x - 33) // 5, 57)], 0.45)
    f.rect(18, 33, 46, 34, gold, clip=body, noline=True)
    f.rect(18, 53, 46, 57, Mat(["ink"]), clip=body, noline=True)
    f.poly([(23, 58), (29, 58), (29, 61), (22, 61)], lea)
    f.poly([(35, 58), (40, 58), (41, 61), (35, 61)], lea)
    f.rect(29, 19, 34, 24, skin, group=400)
    # far arm, a bolt of white linen on his hip
    f.poly([(36, 33), (46, 32), (48, 40), (38, 42)], Mat(["wh_d", "wh_l"], outline="brown", cuts=[0.6]),
           group=280)
    f.thick_line([(39, 24), (44, 31), (41, 36)], 5, robe, group=300)
    # near arm raised: the balance held up
    f.thick_line([(25, 24), (20, 25), (16, 14)], 5, robe, group=200)

    # fringe, over a black-figure band of running spirals
    for x in range(21, 44, 2):
        f.px(x, 58, "gold_m")
    for x in range(20, 44, 4):
        f.pxs([(x, 54), (x + 1, 54), (x + 1, 55), (x + 2, 55), (x + 2, 56), (x + 3, 56)], "gold_m")
    # stripes on the linen bolt
    f.line([(39, 35), (47, 34)], "pur_m")
    f.line([(39, 38), (47, 37)], "pur_m")
    fist(f, 39, 33, "brown")
    # the balance: beam, cords, two pans, hanging from his fist
    P(f, 2, 13, """
        ...........kk.........
        .kkkkkkkkkkggkkkkkkkk.
        kGGGGGGGGGGgggggggggdk
        .kkk.kkkkkkkkkkkk.kkk.
        ..kk.............kk...
        ..k.k...........k.k...
        .k...k.........k...k..
        .k...k.........k...k..
        k.....k.......k.....k.
        kkkkkkk.......kkkkkkk.
        kGGgggk.......kGgggdk.
        .kkkkk.........kkkkk..
    """, {"k": "ink", "G": "gold_l", "g": "gold_m", "d": "gold_d"})
    f.pxs([(18, 22), (19, 22)], "gold_l")  # a coin in the pan
    fist(f, 11, 8, "brown")
    # face: an open, selling smile
    face(f, 24, 11, FACE_BEARD, "ink", white="wh_l", hair="hair",
         edits=[(5, 7, "wh_l"), (6, 7, "wh_l"), (7, 7, "wh_l"), (8, 7, "wh_l"), (4, 7, "ink"),
                (9, 7, "ink"), (3, 8, "hair_l"), (8, 9, "hair_l"), (11, 8, "hair_l"), (2, 6, "hair_l")])
    # the conical cap over black curls; gold in his ear
    P(f, 22, 0, """
        ..........kk..........
        .........kWWk.........
        ........kWWwwk........
        .......kWWWwwwk.......
        ......kWWWwwwwwk......
        .....kWWWWwwwwwwk.....
        ....kWWWWwwwwwwwwk....
        ...kPPPPPPPPPpppppk...
        ...kkkkkkkkkkkkkkkk...
        ..khHkhHkhHkhHkhHHHk..
        ..kHH..........HHkHk..
        ..kH............HGHk..
        ..kH............HgHk..
        ...k............kkk...
    """, {"k": "ink", "W": "wh_l", "w": "wh_d", "P": "pur_l", "p": "pur_m", "H": "hair", "h": "hair_l",
          "G": "gold_l", "g": "gold_m"})
    return f, pal


def pharaoh_proteus():
    """Pharaoh Proteus of Memphis, who kept Helen through the war: the striped
    nemes and the cobra, a braided beard, a broad collar, the white kilt and the
    crook. He likes Homer's version of himself: the lion mask on its stick is a
    joke he tells with his hands."""
    pal = Palette([
        ("ink", INK), *SKIN_NILE, ("brown", (88, 48, 32)),
        ("gold_l", (248, 224, 104)), ("gold_m", (232, 168, 48)), ("gold_d", (160, 96, 32)),
        ("lap_l", (88, 136, 224)), ("lap_d", (32, 56, 152)),
        ("lin_l", (248, 248, 232)), ("lin_m", (216, 208, 184)), ("lin_d", (160, 152, 136)),
        ("red", (208, 64, 48)), ("tq", (64, 176, 160)),
    ])
    skin = skin_mat("brown")
    linen = Mat(["lin_d", "lin_m", "lin_l"], outline="brown", wx=0.85, wy=0.2, cuts=[0.5, 0.82])
    gold = Mat(["gold_d", "gold_m", "gold_l"], cuts=[0.3, 0.7])
    lap = Mat(["lap_d", "lap_l"], cuts=[0.55])
    f = Fig(pal)

    # the nemes' lappets behind the shoulders
    f.poly([(23, 14), (42, 14), (44, 26), (42, 30), (24, 30), (21, 26)], lap, group=10)
    # legs, sandals
    f.poly([(26, 46), (31, 46), (30, 51), (29, 57), (25, 57), (25, 51)], skin, group=100)
    f.poly([(35, 46), (39, 46), (40, 51), (42, 57), (38, 57), (36, 51)], skin, group=101)
    f.poly([(23, 57), (30, 57), (30, 61), (22, 61)], Mat(["gold_d"]))
    f.poly([(37, 57), (43, 57), (45, 61), (37, 61)], Mat(["gold_d"]))
    # bare torso; the pleated royal kilt with its gold apron
    f.poly([(26, 22), (39, 22), (41, 30), (40, 38), (25, 38), (24, 30)], skin, group=150)
    kilt = f.poly([(24, 36), (41, 36), (44, 49), (21, 49)], linen)
    f.poly([(30, 38), (35, 38), (37, 49), (28, 49)], gold, group=160)
    f.rect(21, 36, 44, 37, gold, clip=kilt, noline=True)
    f.rect(29, 19, 34, 24, skin, group=400)
    # broad collar: lapis, gold, carnelian, turquoise
    f.poly([(24, 22), (40, 22), (42, 26), (36, 30), (28, 30), (22, 26)], lap, group=420)
    # far arm: the crook over his shoulder
    f.thick_line([(39, 24), (44, 30), (40, 33)], 5, skin, group=300)
    f.thick_line([(41, 32), (49, 6)], 3, Mat(["lap_d", "gold_m"], cuts=[0.5]), group=310)
    # near arm up: the lion mask on its stick
    f.thick_line([(25, 24), (19, 28), (17, 23)], 5, skin, group=200)
    f.thick_line([(17, 23), (13, 14)], 2, Mat(["brown"]), group=210)

    # collar bands
    f.line([(25, 24), (28, 26), (36, 26), (39, 24)], "gold_l")
    f.line([(25, 25), (29, 28), (35, 28), (40, 25)], "red")
    f.line([(28, 29), (36, 29)], "tq")
    # kilt pleats
    for x in (24, 26, 39, 41):
        f.line([(x, 39), (x - (1 if x < 32 else -1), 48)], "lin_d")
    f.pxs([(31, 40), (33, 42), (32, 45)], "lap_d")
    for x in list(range(22, 29)) + list(range(37, 44)):
        f.px(x, 47, "ink")
        f.px(x, 48, "ink")
        if x % 2:
            f.px(x, 47 + (x // 2) % 2, "gold_l")
    fist(f, 38, 30, "brown")
    fist(f, 14, 20, "brown")
    # the crook's hook
    P(f, 45, 0, """
        .kkkk..
        kGgggk.
        kgkkgGk
        kk..kgk
        ....kGk
        ....kgk
        .....k.
    """, {"k": "ink", "G": "gold_l", "g": "lap_d"})
    # the lion mask: Homer's lion, gold, with a mane
    P(f, 2, 1, """
        ...k..k..k....
        ..kMkkMkkMk...
        .kkMMmMMmMMkk.
        kMMmkkkkkkmMMk
        .kMkGGGGGgkMk.
        kMMkGkGGkgkMMk
        .kmkGGggggkmk.
        kMMkGGkkgdkMMk
        .kMmkGkkdkmMk.
        ..kMmkkkkmMk..
        .kMMMmmmmMMMk.
        ..kk.k..k.kk..
    """, {"k": "ink", "M": "gold_m", "m": "gold_d", "G": "gold_l", "g": "gold_m", "d": "gold_d"})
    # face: kohl, one eye winking, a grin
    face(f, 24, 11, FACE_KOHL, "brown", white="lin_l",
         edits=[(3, 2, "skin_l"), (4, 2, "ink"), (5, 2, "ink"), (6, 2, "skin_l"),
                (5, 7, "lin_l"), (6, 7, "lin_l"), (7, 7, "lin_l"), (8, 7, "ink"), (4, 6, "ink")])
    # the braided false beard
    P(f, 30, 21, """
        .kk.
        kGLk
        kLGk
        kGLk
        .kk.
    """, {"k": "ink", "G": "lap_l", "L": "lap_d"})
    # the nemes, striped gold and lapis, the cobra at the brow
    P(f, 20, 0, """
        ..........kkkk..........
        ........kkGRkkkk........
        ......kkGGkkGGGGkk......
        .....kGGGGGGGGGGGGk.....
        ....kLLLLLLLLLLLLLLk....
        ...kGGGGGGGGGGGGGGGGk...
        ...kLLLLLLLLLLLLLLLLk...
        ..kGGGGGGGGGGGGGGGGGGk..
        ..kLLLLLLLLLLLLLLLLLLk..
        ..kkkkkkkkkkkkkkkkkkkk..
        ..kGGk.............kGGk.
        ..kLLk.............kLLk.
        ..kGGk.............kGGk.
        ..kLLk.............kLLk.
        ..kGGk.............kGGk.
        ...kLk............kLLk..
        ....kk.............kk...
    """, {"k": "ink", "G": "gold_l", "L": "lap_d", "R": "red"})
    return f, pal


def queen_helen():
    """Helen of Sparta, Proteus's guest, who sat out the whole war in Memphis
    and never went home ("Sparta's cold"): golden hair under a gold diadem, a
    Greek chiton with a Spartan crimson himation, an Egyptian broad collar and
    armlets. She holds up a bronze mirror: everyone wanted a copy of her."""
    pal = Palette([
        ("ink", INK), *SKIN_FAIR, ("brown", (128, 64, 48)),
        ("hair_l", (248, 232, 144)), ("hair_m", (232, 184, 80)), ("hair_d", (168, 112, 48)),
        ("wh_l", (248, 248, 240)), ("wh_m", (224, 216, 200)), ("wh_d", (176, 168, 160)),
        ("cr_l", (224, 80, 72)), ("cr_m", (176, 40, 56)), ("cr_d", (104, 24, 48)),
        ("lap", (56, 96, 192)),
    ])
    skin = skin_mat("brown")
    white = Mat(["wh_d", "wh_m", "wh_l"], outline="brown", wx=0.85, wy=0.2, cuts=[0.5, 0.82])
    crimson = Mat(["cr_d", "cr_m", "cr_l"], wx=0.85, wy=0.25, cuts=[0.28, 0.68])
    gold = Mat(["hair_d", "hair_m", "hair_l"], cuts=[0.3, 0.7])
    f = Fig(pal)

    # golden hair down her back
    f.poly([(26, 8), (41, 8), (45, 18), (46, 30), (43, 36), (38, 34), (26, 34), (22, 26), (23, 16)], gold,
           group=10)
    # chiton to the ground
    f.poly([(25, 22), (38, 22), (40, 30), (41, 40), (43, 52), (45, 60), (18, 60), (20, 52), (22, 40),
            (23, 30)], white)
    for x in (25, 30, 35, 40):
        f.shade_poly([(x, 40), (x + 1, 40), (x + 1 + (x - 32) // 5, 59), (x + (x - 32) // 5, 59)], 0.45)
    f.poly([(25, 60), (30, 60), (30, 62), (25, 62)], Mat(["hair_d"]))
    f.poly([(34, 60), (39, 60), (39, 62), (34, 62)], Mat(["hair_d"]))
    # the crimson himation, wrapped from the far shoulder round her hips
    f.poly([(33, 22), (40, 22), (43, 32), (44, 44), (42, 54), (36, 56), (24, 52), (21, 44), (30, 40),
            (36, 34), (35, 26)], crimson)
    f.rect(29, 19, 33, 24, skin, group=400)
    # Egyptian broad collar
    f.poly([(25, 22), (38, 22), (39, 25), (34, 28), (29, 28), (24, 25)], Mat(["lap", "hair_l"], cuts=[0.5]),
           group=420)
    # far arm: a hand on her hip in the crimson
    f.thick_line([(38, 24), (43, 30), (39, 35)], 4, skin, group=300)
    # near arm raised: the mirror
    f.thick_line([(25, 24), (20, 29), (18, 23)], 4, skin, group=200)

    # himation hem: a black-figure band of Spartan crimson and gold
    f.line([(24, 52), (36, 56), (42, 54)], "hair_m")
    f.line([(24, 51), (36, 55), (42, 53)], "ink")
    f.line([(25, 24), (28, 26), (34, 26), (37, 24)], "hair_l")
    f.line([(26, 25), (29, 27), (33, 27), (36, 25)], "cr_m")
    # gold armlets
    f.pxs([(40, 27), (41, 28), (21, 27), (22, 28)], "hair_l")
    fist(f, 37, 32, "brown")
    # the bronze mirror on its handle
    P(f, 8, 2, """
        ...kkkkk...
        ..kGGGggk..
        .kGWWGgggk.
        kGWWGgggggk
        kGWGggggggk
        kGGgggggddk
        kGgggggdddk
        .kgggggddk.
        ..kgggddk..
        ...kkgkk...
        ....kdk....
        ....kgk....
        ...kgggk...
        ....kdk....
        ....kgk....
    """, {"k": "ink", "G": "hair_l", "g": "hair_m", "d": "hair_d", "W": "wh_l"})
    fist(f, 15, 19, "brown")
    # face: serene, a knowing smile
    face(f, 24, 10, FACE_F, "brown", white="wh_l", lips="cr_m",
         edits=[(7, 6, "cr_m"), (8, 6, "cr_m"), (6, 6, "skin_m"), (9, 5, "cr_d")])
    # golden hair in a knot, a gold diadem
    P(f, 22, 0, """
        ...........kkkk.....
        ..........kHHhhk....
        ......kkkkkHhhhdk...
        ....kkHHHHhhkkkk....
        ...kHHHHHHhhhhhdk...
        ..kHHHHHHhhhhhhhdk..
        ..kGGGGGGGGGGGgggk..
        ..kHHhHHHHhHHHhhddk.
        ..kHHHH........hhdk.
        ..kHHk..........hdk.
        ..kHk...........hhdk
        ..kHk...........hhdk
        ..kHk...........hhdk
        ..kHk...........hddk
        ...kHk.........khdk.
        ....k...........kk..
    """, {"k": "ink", "H": "hair_l", "h": "hair_m", "d": "hair_d", "G": "lap", "g": "lap"})
    return f, pal


PICS = {
    "trojan_hoplite": trojan_hoplite,
    "charioteer": charioteer,
    "shepherd_of_ida": shepherd_ida,
    "argonaut": argonaut,
    "colchian_sorceress": colchian_sorceress,
    "chalybes_smith": chalybes_smith,
    "priest_of_the_sun": sun_priest,
    "scribe_of_thoth": scribe_thoth,
    "embalmer": embalmer,
    "nile_boatman": nile_boatman,
    "phoenician_trader": phoenician_trader,
    "prince_hektor": prince_hektor,
    "priestess_medea": priestess_medea,
    "pharaoh_proteus": pharaoh_proteus,
    "queen_helen": queen_helen,
}


# --------------------------------------------------------------------------
# Previews
# --------------------------------------------------------------------------

def labelled_sheet(figs, k=2, cols=5, refs=("hoplite", "shepherd", "kleon", "hierophant_ione", "augur")):
    """The slice's pics for scale on the top row, then the new pics, each on the
    grass battle background with its name under it, at k x."""
    tiles = [(n, load_pic(os.path.join(FRONT, n + ".png"))) for n in refs]
    tiles += [(n, to_rgba(arr, pal)) for n, (arr, pal) in figs.items()]
    rows = (len(tiles) + cols - 1) // cols
    tw, th, lab = 96 * k, 72 * k, 12
    out = Image.new("RGBA", (tw * cols, (th + lab) * rows), (248, 240, 224, 255))
    d = ImageDraw.Draw(out)
    for i, (name, im) in enumerate(tiles):
        x, y = tw * (i % cols), (th + lab) * (i // cols)
        out.alpha_composite(upscale(battle_tile(im), k), (x, y))
        d.text((x + 4, y + th), name + (" (slice)" if name in refs else ""), fill=(64, 40, 32, 255))
    return out


def preview(figs, pv):
    os.makedirs(pv, exist_ok=True)
    labelled_sheet(figs, k=3, cols=5).save(os.path.join(pv, "sheet.png"))
    for name, (arr, pal) in figs.items():
        upscale(to_rgba(arr, pal), 6).save(os.path.join(pv, name + ".png"))
        grid_preview(to_rgba(arr, pal), 10).save(os.path.join(pv, name + "_grid.png"))


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    write = "--write" in args
    only = [a for a in args if a in PICS]
    figs = {}
    for name, fn in PICS.items():
        if only and name not in only:
            continue
        f, pal = fn()
        arr = render(f)
        palette_report(arr, pal, name)
        figs[name] = (arr, pal)
        if write:
            save_indexed(arr, pal, os.path.join(FRONT, name + ".png"))
    if write and not only:
        os.makedirs(os.path.dirname(SHEET), exist_ok=True)
        labelled_sheet(figs, k=2, cols=5).save(SHEET)
    if pv:
        preview(figs, pv)


if __name__ == "__main__":
    main()
