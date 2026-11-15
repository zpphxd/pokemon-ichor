"""Trainer front pics for Act II, batch 1 (beats 26-34).

The four new classes (Maenad, Satyr, Actor, Vintner) and two named pics
(Hierophant Thespis, Silenos). Each is a 64x64, 16-color Gen 3 trainer pic in
the slice's house style (sprites_classes.py): a 3/4 view facing the player's
side (screen left), lit from the top left, the palette embedded in the PNG.
See design/phase3/SPRITES.md.

Usage: python3 tools/ichor/art/sprites_act2_classes.py [NAME ...] [--write] [--preview DIR]

--write   writes the indexed PNGs to graphics/trainers/front_pics/ and, when no
          NAME is given, the portrait sheet design/phase3/img/portraits_batch1.png
--preview writes the 3x sheet, 6x singles and pixel grids to DIR
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, Mat, Fig, save_indexed, to_rgba, upscale, palette_report, grid_preview  # noqa: E402,E501
from sprites_classes import (INK, SKIN_TAN, SKIN_SUN, render, pole, stagger, skin_mat,  # noqa: E402
                             load_pic, battle_tile, FRONT)
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

FIST = [".bbbb.", "bLLLLb", "bLbLMb", "bLLMMb", ".bbbb."]
FIST_LEGEND = {"b": "out", "L": "skin_l", "M": "skin_m"}


def fist(f, x, y, out="hair"):
    f.patch(x, y, FIST, {"b": out, "L": "skin_l", "M": "skin_m"})


# --------------------------------------------------------------------------
# Maenad: a bacchant mid-whirl. Loose dark hair crowned with ivy streaming
# behind her, a fawnskin knotted over her left shoulder on a saffron chiton,
# bare feet, and the thyrsus held high: a fennel staff wound with ivy and
# tipped with a pine cone.
# --------------------------------------------------------------------------

def maenad():
    pal = Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("hair", (56, 32, 24)), ("hair_l", (104, 56, 40)),
        ("saf_l", (248, 200, 72)), ("saf_m", (224, 144, 32)), ("saf_d", (160, 88, 32)),
        ("fawn_l", (216, 160, 96)), ("fawn_d", (152, 96, 56)),
        ("spot", (248, 232, 200)),
        ("ivy_l", (128, 176, 64)), ("ivy_d", (48, 96, 40)),
    ])
    skin = skin_mat("hair")
    chiton = Mat(["saf_d", "saf_m", "saf_l"], outline="hair", wx=0.8, wy=0.3, cuts=[0.28, 0.68])
    fawn = Mat(["fawn_d", "fawn_l"], outline="hair", wx=0.8, wy=0.4, cuts=[0.62])
    hair = Mat(["hair", "hair_l"], outline="ink", wx=0.8, wy=0.3, cuts=[0.7])
    fennel = Mat(["fawn_d", "fawn_l"], cuts=[0.6], wx=1.0, wy=0.0)
    f = Fig(pal)

    # hair streaming out behind her as she turns
    f.poly([(36, 6), (44, 7), (52, 12), (56, 18), (55, 24), (51, 22), (52, 28), (47, 25), (45, 30),
            (41, 25), (36, 22)], hair, group=40)
    # the thyrsus, held high in her near hand
    pole(f, (19, 6), (23, 44), fennel, group=50)
    # far leg kicked back mid-step, near leg planted, bare feet
    f.poly([(37, 47), (41, 47), (44, 52), (48, 55), (46, 58), (41, 54)], skin, group=101)
    f.poly([(45, 55), (50, 56), (52, 59), (48, 60), (44, 58)], skin, group=102)
    f.poly([(28, 48), (33, 48), (33, 56), (30, 57)], skin, group=100)
    f.poly([(26, 56), (32, 56), (33, 59), (31, 61), (25, 61)], skin, group=103)
    f.rect(29, 19, 34, 24, skin, group=400)
    # saffron chiton, its hem swinging wide with the whirl
    body = f.poly([(26, 22), (39, 22), (41, 30), (42, 36), (47, 41), (53, 46), (47, 49), (37, 51), (27, 51),
                   (17, 50), (21, 44), (24, 36), (24, 28)], chiton)
    for pts in ([(28, 38), (29, 38), (25, 50), (24, 50)], [(34, 38), (35, 38), (36, 50), (35, 50)],
                [(39, 37), (40, 37), (46, 46), (45, 46)]):
        f.shade_poly(pts, 0.45)
    f.shade_poly([(24, 30), (27, 30), (22, 48), (19, 48)], -0.3)
    # ivy girdle
    f.rect(22, 34, 44, 35, Mat(["ivy_d", "ivy_l"], cuts=[0.6]), clip=body, noline=True)
    # fawnskin over her left shoulder, knotted at the near breast, a hoof hanging
    fawn_id = f.poly([(33, 22), (41, 22), (43, 27), (43, 33), (40, 36), (33, 38), (28, 36), (31, 30)],
                     fawn, group=70)
    f.poly([(42, 31), (45, 33), (45, 38), (43, 38), (42, 35)], fawn, group=71)
    # near arm raised to the thyrsus, far arm flung out for balance
    f.thick_line([(27, 24), (24, 18), (22, 13)], 4, skin, group=200)
    f.thick_line([(40, 24), (45, 29), (50, 31)], 4, skin, group=300)

    f.textures = [((fawn_id,), ["fawn_d", "fawn_l"], stagger(29, 23, 43, 37, 4, 3), [(0, 0)])]
    # fawn spots and the hoof
    f.pxs([(35, 25), (38, 28), (34, 31), (31, 34), (40, 31), (37, 34)], "spot")
    f.pxs([(43, 37), (44, 37)], "ink")
    # pine cone at the thyrsus's head, with a tuft of ivy below it
    f.patch(17, 0, [
        "..kkk..",
        ".kTtTk.",
        "kTtTtdk",
        "ktTtTdk",
        "kTtTtdk",
        ".kTtdk.",
        ".GkkkG.",
        "GgG.GgG",
    ], {"k": "ink", "T": "fawn_l", "t": "fawn_d", "d": "hair_l", "G": "ivy_l", "g": "ivy_d"})
    # ivy wound round the staff
    for y in (14, 20, 26, 32, 38):
        f.patch(18 + (y - 14) // 8, y, ["G.", "gG"], {"G": "ivy_l", "g": "ivy_d"})
    # her fist round the staff, and the open far hand
    fist(f, 18, 9)
    f.patch(48, 28, [
        "..kk...",
        ".kLLkk.",
        "kLLLLLk",
        "kLLLLMk",
        ".kLMMk.",
        "..kkk..",
    ], {"k": "hair", "L": "skin_l", "M": "skin_m"})
    # head: loose hair under an ivy crown, face tipped up, mouth open in the cry
    f.patch(22, 2, [
        "......kkkkkkk......",
        "....kkHHHHHhhkk....",
        "..kkGgHHGgHhhGgkk..",
        ".kgGGgGGgGGgGGgGhk.",
        ".kGgHHHHgHHhhhgGhhk",
        "kHHHHHHHHHhhhhhhhhk",
        "kbHLLLLLLLLMbhhhhhk",
        ".bkkLLLLkkkMbhhhhhk",
        ".bLWkLLLkWLMDbhhhk.",
        "bLLLLLLLLLLMDbhhhk.",
        "bLLLLDLLLLMMMbhhhhk",
        ".bLLDDLLLMMMMbhhhhk",
        ".bLLLkkkLMMMbhhhhk.",
        "..bLLkRkLMMbhhhhk..",
        "...bLLLMMMbhhhk....",
        "....bbbbbbkhhk.....",
        "...........kk......",
    ], {"k": "ink", "H": "hair_l", "h": "hair", "G": "ivy_l", "g": "ivy_d", "b": "hair", "L": "skin_l",
        "M": "skin_m", "D": "skin_d", "W": "spot", "R": "saf_d"})
    return f, pal


# --------------------------------------------------------------------------
# Satyr: a comic chorus man in the satyr play's costume. A snub-nosed satyr
# mask with goat ears and horn stubs pushed up on his dark curls, a wide grin
# and a beard, a bare chest, shaggy goat-hair breeches to the hooves with a
# tail behind, and a wineskin under his arm. One fist up: "Euoi!"
# --------------------------------------------------------------------------

def satyr():
    pal = Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("hair", (56, 40, 32)),
        ("goat_l", (176, 152, 120)), ("goat_m", (120, 96, 72)), ("goat_d", (72, 56, 48)),
        ("mask_l", (248, 240, 216)), ("mask_d", (200, 176, 144)),
        ("nose", (192, 80, 56)),
        ("skin_l2", (184, 104, 64)), ("lea_d", (112, 56, 40)),
    ])
    skin = skin_mat("hair")
    goat = Mat(["goat_d", "goat_m", "goat_l"], outline="ink", wx=0.75, wy=0.35, cuts=[0.4, 0.75])
    skin_wine = Mat(["lea_d", "skin_l2"], outline="ink", wx=0.7, wy=0.5, cuts=[0.55])
    f = Fig(pal)

    # tail curling up behind
    f.thick_line([(42, 44), (48, 45), (51, 41), (50, 37)], 3, goat, group=30)
    # shaggy goat-hair legs to cloven hooves, planted wide
    f.poly([(25, 40), (32, 40), (32, 47), (30, 56), (24, 56), (24, 47)], goat, group=100)
    f.poly([(34, 40), (41, 40), (42, 47), (44, 56), (38, 56), (35, 47)], goat, group=101)
    f.poly([(23, 56), (30, 56), (30, 60), (22, 60)], Mat(["ink"]))
    f.poly([(38, 56), (45, 56), (46, 60), (38, 60)], Mat(["ink"]))
    f.rect(29, 19, 34, 24, skin, group=400)
    # bare chest and belly
    f.poly([(26, 23), (39, 23), (41, 31), (41, 41), (24, 41), (24, 31)], skin, group=410)
    f.shade_poly([(36, 25), (41, 25), (41, 40), (37, 40)], 0.45)
    f.shade_poly([(31, 30), (34, 30), (34, 31), (31, 31)], 0.4)
    f.shade_poly([(31, 35), (32, 35), (32, 38), (31, 38)], 0.35)
    # the costume's goat-hair waist
    waist = f.poly([(23, 38), (42, 38), (43, 44), (22, 44)], goat, group=120)
    # near arm up in a fist, far arm round the wineskin
    f.thick_line([(26, 25), (21, 22), (19, 15)], 5, skin, group=200)
    f.poly([(37, 27), (44, 25), (49, 28), (50, 34), (47, 38), (40, 38), (37, 34)],
                     skin_wine, group=500)
    f.thick_line([(40, 25), (44, 31), (40, 35)], 4, skin, group=300)

    f.textures = [((100, 101, waist, 30), ["goat_d", "goat_m", "goat_l"], stagger(22, 38, 50, 56, 3, 3),
                   [(0, 0), (0, 1)])]
    # wineskin's neck, tied with a cord
    f.patch(46, 22, [
        ".kk..",
        "kLDk.",
        ".kkkk",
        "..kDk",
        "...k.",
    ], {"k": "ink", "L": "skin_l2", "D": "lea_d"})
    fist(f, 16, 10)
    f.pxs([(39, 33), (40, 34)], "skin_m")
    # head: satyr mask pushed up on his curls; his own face grinning under it
    f.patch(22, 0, [
        "..kk.k......k.kk...",
        ".kWkkFk....kFkkWk..",
        ".kWWkkkkkkkkkWWk...",
        "..kkWWWWWWWWWkk....",
        "...kWkkWWWkkWwk....",
        "...kWWWWNNWWWwk....",
        "...kWWWNNNNWWwkk...",
        "..khkWWWkkWWwkhhk..",
        "..khhkkkkkkkkhhhhk.",
        "..khHhHHhHHhHhhhhk.",
        "..kbLLLLLLLLMbhhhk.",
        "..bkkkLLLLkkkMbhhk.",
        "..bLWkLLLLkWLMDbhk.",
        ".bLLLLLLLLLLMMDbhk.",
        ".bLLLLDNLLLLMMbhhk.",
        "..bLWWWWWWWLMbhhk..",
        "..bLkWkWkWkMMbhhk..",
        "..khhLLLLLMMhhhk...",
        "...khhhhhhhhhhk....",
        "....kkhhhhhhkk.....",
        "......kkkkkk.......",
    ], {"k": "ink", "W": "mask_l", "w": "mask_d", "F": "goat_l", "N": "nose", "h": "hair", "H": "goat_m",
        "b": "hair", "L": "skin_l", "M": "skin_m", "D": "skin_d"})
    return f, pal


# --------------------------------------------------------------------------
# Actor: a tragic actor declaiming. Dark curls under a gold fillet, a short
# beard, a long-sleeved wine-red robe patterned in gold zigzags and white dots,
# tragic boots with thick soles; his white mask hangs from his far hand, and
# his near hand is flung up to the gods.
# --------------------------------------------------------------------------

def actor():
    pal = Palette([
        ("ink", INK),
        *SKIN_TAN,
        ("hair", (48, 32, 32)),
        ("wine_l", (216, 80, 104)), ("wine_m", (160, 40, 72)), ("wine_d", (96, 24, 56)),
        ("gold_l", (248, 208, 88)), ("gold_d", (184, 120, 40)),
        ("mask_l", (248, 248, 240)), ("mask_d", (184, 176, 168)),
        ("boot", (88, 48, 32)),
        ("dot", (240, 224, 216)),
    ])
    skin = skin_mat("boot")
    robe = Mat(["wine_d", "wine_m", "wine_l"], wx=0.85, wy=0.25, cuts=[0.3, 0.72])
    gold = Mat(["gold_d", "gold_l"], wx=1.0, wy=0.0, cuts=[0.65])
    mask = Mat(["mask_d", "mask_l"], outline="ink", wx=0.8, wy=0.3, cuts=[0.62])
    boot = Mat(["boot"])
    f = Fig(pal)

    # tragic boots on thick soles
    f.poly([(23, 55), (30, 55), (30, 61), (22, 61)], boot)
    f.poly([(35, 55), (42, 55), (43, 61), (35, 61)], boot)
    f.rect(29, 18, 34, 23, skin, group=400)
    # the long robe
    body = f.poly([(26, 22), (39, 22), (41, 31), (42, 43), (44, 56), (21, 56), (23, 43), (24, 31)], robe)
    for x in (28, 33, 38):
        f.shade_poly([(x, 40), (x + 1, 40), (x + 1 + (x - 33) // 4, 55), (x + (x - 33) // 4, 55)], 0.45)
    f.shade_poly([(24, 30), (27, 30), (25, 54), (22, 54)], -0.3)
    # patterned bands: a gold collar, a zigzag band at the chest, a gold hem
    f.rect(19, 29, 46, 31, gold, clip=body, noline=True)
    f.rect(19, 52, 46, 55, gold, clip=body, noline=True)
    # near arm flung up in a long sleeve, far arm down to the mask
    f.thick_line([(26, 24), (21, 17), (18, 10)], 5, robe, group=200)
    f.thick_line([(40, 24), (43, 33), (44, 40)], 5, robe, group=300)
    f.ellipse((40, 40, 51, 53), mask, group=600)

    # zigzag in the chest band, dots on the skirt
    for x in range(22, 44, 2):
        f.px(x, 30 if x % 4 else 29, "wine_d")
    for x, y in stagger(23, 35, 42, 50, 4, 4):
        f.px(x, y, "dot")
    for x in range(22, 45, 3):
        f.px(x, 53, "wine_d")
    f.line([(19, 14), (23, 19)], "wine_l")
    # the open hand, palm to the sky
    f.patch(14, 3, [
        ".k.k...",
        "kLkLk..",
        "kLkLkk.",
        "kLLLLLk",
        "kLLLLMk",
        ".kLLMk.",
        "..kkk..",
    ], {"k": "boot", "L": "skin_l", "M": "skin_m"})
    # his fingers at the mask's chin; the mask: a tragic face, mouth agape
    f.patch(40, 38, [
        "...........",
        "..kkLLkkk..",
        ".kLkkkkLLk.",
        ".kLnnLnnlk.",
        ".kLLLlLLlk.",
        ".kLLkkkLlk.",
        ".kLknnnklk.",
        ".kLLkkkLlk.",
        "..kLLLLlk..",
        "..bbbbkk...",
        "..bLLMb....",
    ], {"k": "ink", "L": "mask_l", "l": "mask_d", "n": "hair", "b": "boot", "M": "skin_m"})
    # head: curls under a gold fillet, beard, mouth open mid-line
    f.patch(23, 4, [
        "......kkkkkk.......",
        "....kkhkhhkhkk.....",
        "...khhkhhkhhkhhk...",
        "..khhhhhhhhhhhhhk..",
        "..kGGGGGGGGGgggghk.",
        ".khbLLLLLLLLMbhhhk.",
        ".khkkLLLLLkkMbhhhk.",
        ".kbLWkLLLLkWMDbhhk.",
        ".bLLLLLLLLLLMDbhk..",
        ".bLLLLDLLLLMMMbhk..",
        ".bhLLDDLLLMMMhbhk..",
        ".khhLLkkkLMMhhhk...",
        "..khhhkRkhhhhhk....",
        "...khhhhhhhhhk.....",
        "....kkhhhhhkk......",
        "......kkkkk........",
    ], {"k": "ink", "h": "hair", "G": "gold_l", "g": "gold_d", "b": "boot", "L": "skin_l", "M": "skin_m",
        "D": "skin_d", "W": "mask_l", "R": "wine_m"})
    return f, pal


# --------------------------------------------------------------------------
# Vintner: a vineyard man home from the treading floor. A wine-red headscarf,
# a short beard, an undyed exomis off his near shoulder, legs stained purple
# to the knee, a basket of black grapes on his far shoulder and a pruning hook
# held up in his near hand.
# --------------------------------------------------------------------------

def vintner():
    pal = Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("brown", (88, 48, 32)),
        ("grape_d", (56, 32, 80)), ("grape_m", (112, 56, 136)), ("lilac", (184, 136, 208)),
        ("wick_l", (224, 184, 104)), ("wick_d", (160, 112, 56)),
        ("lin_l", (232, 224, 200)), ("lin_d", (176, 160, 128)),
        ("wine", (160, 40, 72)),
        ("steel", (184, 184, 192)),
        ("leaf", (96, 136, 48)),
    ])
    skin = skin_mat("brown")
    exomis = Mat(["lin_d", "lin_l"], outline="brown", wx=0.85, wy=0.3, cuts=[0.6])
    stain = Mat(["grape_d", "grape_m"], outline="ink", wx=0.9, wy=0.1, cuts=[0.6])
    wicker = Mat(["brown", "wick_d", "wick_l"], outline="brown", wx=0.7, wy=0.5, cuts=[0.45, 0.8])
    wood = Mat(["brown", "wick_d"], cuts=[0.6])
    f = Fig(pal)

    # legs: skin to the knee, purple below
    f.poly([(26, 42), (31, 42), (31, 50), (29, 57), (24, 57), (25, 50)], skin, group=100)
    f.poly([(35, 42), (39, 42), (41, 50), (43, 57), (38, 57), (36, 50)], skin, group=101)
    f.poly([(25, 49), (31, 49), (29, 57), (24, 57)], stain, group=110)
    f.poly([(36, 49), (41, 49), (43, 57), (38, 57)], stain, group=111)
    f.poly([(22, 57), (30, 57), (30, 61), (21, 61)], stain)
    f.poly([(37, 57), (44, 57), (45, 61), (37, 61)], stain)
    f.rect(29, 20, 34, 25, skin, group=400)
    # undyed exomis, belted with a cord, off his near shoulder
    body = f.poly([(28, 24), (39, 24), (41, 33), (43, 45), (35, 46), (24, 45), (25, 33), (26, 28)], exomis)
    f.poly([(24, 24), (29, 24), (29, 30), (25, 31)], skin, group=410)
    f.rect(23, 35, 44, 36, Mat(["brown"]), clip=body, noline=True)
    f.shade_poly([(31, 37), (32, 37), (32, 45), (31, 45)], 0.45)
    f.shade_poly([(37, 37), (38, 37), (40, 45), (39, 45)], 0.45)
    # the pruning hook, held up in his near hand
    pole(f, (18, 14), (21, 34), wood, group=50)
    f.thick_line([(26, 26), (22, 31), (20, 26)], 5, skin, group=200)
    # far arm up to the basket on his shoulder
    f.thick_line([(39, 26), (44, 22), (45, 17)], 5, skin, group=300)
    bask = f.poly([(37, 12), (55, 12), (54, 17), (51, 21), (41, 21), (38, 17)], wicker, group=500)

    f.textures = [((bask,), ["brown", "wick_d", "wick_l"], stagger(38, 13, 55, 21, 4, 2), [(0, 0), (1, 0)])]
    # the stain's ragged top edge and a few splashes higher up
    f.pxs([(26, 48), (28, 47), (30, 48), (37, 48), (39, 47), (40, 48), (27, 45), (38, 44)], "grape_m")
    f.pxs([(29, 49), (37, 49)], "skin_m")
    # the bunches heaped above the rim, a vine leaf on top
    f.patch(37, 3, [
        "......kk.kk.......",
        ".....kLLkLLk......",
        "...kkkLlLLlkkk....",
        "..kAgkkkLkkkAgk...",
        ".kAggAgkkkAgAgAk..",
        ".kgAgAgAkAgAggAgk.",
        "kAgdgAgdgAgdgAgdgk",
        "kgdgdgdgdgdgdgdgdk",
        "kwwwwwwwwwwwwwwwwk",
        ".kkkkkkkkkkkkkkkk.",
    ], {"k": "ink", "L": "leaf", "l": "brown", "A": "lilac", "g": "grape_m", "d": "grape_d", "w": "wick_l"})
    # the hook's blade, curling forward
    f.patch(13, 8, [
        "..kkkk.",
        ".kSSSSk",
        "kSkkkSk",
        "kSk.kSk",
        ".k..kk.",
    ], {"k": "ink", "S": "steel"})
    fist(f, 17, 22, "brown")
    fist(f, 42, 15, "brown")
    # head: wine-red headscarf knotted at the back, short beard, a grin
    f.patch(24, 4, [
        ".....kkkkkkk.......",
        "...kkRRRRRRRkk.....",
        "..kRRRRRRRRRRRk....",
        ".kRRRRRRRRRRRRRk...",
        ".kRRRRRRRRRRRRRkkk.",
        "kRRRRRRRRRRRRRkRRk.",
        "kbbbbbbbbbbbbbkRRk.",
        ".bkkkLLLkkkMbbbkRk.",
        ".bLWkLLLkWLMDbbkk..",
        "bLLLLLLLLLLMDbbk...",
        "bLLLLDLLLLMMMbbk...",
        ".bbLDDLLLMMMbbbk...",
        ".bbbLLLLLLMbbbk....",
        "..bbbkWWkbbbbk.....",
        "...bbbbbbbbbk......",
        "....kbbbbbbk.......",
        "......kkkk.........",
    ], {"k": "ink", "R": "wine", "b": "brown", "L": "skin_l", "M": "skin_m", "D": "skin_d", "W": "lin_l"})
    return f, pal


# --------------------------------------------------------------------------
# Hierophant Thespis, the Masked Player: a tall, theatrical man of about
# fifty in a long grape-purple robe patterned with ivy and hemmed in gold,
# on tragic boots. His face is his oldest Prosomime: a mask split down the
# middle, its near half laughing and its far half weeping, violet haze in its
# eye holes. Gray-streaked hair under an ivy crown, one arm flung wide.
# --------------------------------------------------------------------------

def thespis():
    pal = Palette([
        ("ink", INK),
        *SKIN_TAN,
        ("gray", (168, 160, 160)), ("hair", (72, 56, 56)),
        ("pur_l", (160, 104, 192)), ("pur_m", (104, 56, 136)), ("pur_d", (56, 32, 80)),
        ("ivy_l", (128, 176, 64)), ("ivy_d", (48, 96, 40)),
        ("gold", (232, 184, 72)),
        ("mask_l", (248, 248, 240)), ("mask_m", (192, 184, 192)),
        ("lips", (192, 72, 72)),
    ])
    skin = skin_mat("hair")
    robe = Mat(["pur_d", "pur_m", "pur_l"], wx=0.85, wy=0.25, cuts=[0.3, 0.72])
    gold = Mat(["gold"])
    boot = Mat(["hair"])
    f = Fig(pal)

    # tragic boots
    f.poly([(23, 56), (30, 56), (30, 61), (22, 61)], boot)
    f.poly([(36, 56), (43, 56), (44, 61), (36, 61)], boot)
    f.rect(29, 19, 34, 24, skin, group=400)
    # the long robe, its far side swept back by the gesture
    body = f.poly([(26, 22), (40, 22), (42, 31), (44, 43), (48, 57), (20, 57), (23, 43), (24, 31)], robe)
    for x in (28, 34, 40):
        f.shade_poly([(x, 38), (x + 1, 38), (x + 2 + (x - 33) // 4, 56), (x + 1 + (x - 33) // 4, 56)], 0.45)
    f.shade_poly([(24, 30), (27, 30), (24, 55), (21, 55)], -0.3)
    f.rect(18, 54, 49, 56, gold, clip=body, noline=True)
    f.rect(18, 34, 49, 35, gold, clip=body, noline=True)
    # near arm flung wide and up, far hand on his breast
    f.thick_line([(26, 24), (19, 20), (13, 13)], 5, robe, group=200)
    f.thick_line([(40, 25), (42, 31), (36, 31)], 5, robe, group=300)

    # ivy trailing over the robe in leaf pairs
    for x, y in [(27, 26), (35, 27), (30, 39), (38, 41), (26, 46), (34, 48), (42, 50), (23, 51)]:
        f.patch(x, y, ["Gg.", ".gG"], {"G": "ivy_l", "g": "ivy_d"})
    f.line([(28, 27), (31, 39), (27, 46), (24, 51)], "ivy_d")
    f.line([(36, 28), (39, 41), (35, 48), (43, 50)], "ivy_d")
    # the open hand, palm up to the audience
    f.patch(8, 6, [
        "..k.k..",
        ".kLkLk.",
        "kkLkLkk",
        "kLLLLLk",
        "kLLLLMk",
        ".kLLMk.",
        "..kkk..",
    ], {"k": "hair", "L": "skin_l", "M": "skin_m"})
    f.patch(34, 28, [
        ".kkkk.",
        "kLLLLk",
        "kLMLMk",
        ".kkkk.",
    ], {"k": "hair", "L": "skin_l", "M": "skin_m"})
    # head: the split mask framed by gray-streaked hair and beard, an ivy
    # crown, lilac ribbons behind. The near half laughs (brow up, mouth corner
    # up), the far half weeps (brow slanted, a tear, mouth corner down).
    f.patch(22, 3, [
        "......kkkkkkk......",
        "....kkGgGgGgGkk....",
        "...kGgHgGgHgGgHk...",
        "..kHhGgHhhGgHhhhk..",
        "..kHkkkkkkkkkhhhhk.",
        ".kHkWWWWWwwwwkhhhk.",
        ".kHkWkWWWWkwwkhhhk.",
        ".kHkWnkWWknnwkhhPk.",
        ".kHkWWWWWwwnwkhhPk.",
        ".kHkRWWWWwwRwkhhPk.",
        ".kHkWkWWWwwwwkhhkP.",
        ".kHkWWkkkkkwwkhhkP.",
        ".kHkWWknnnnkwkhk...",
        "..kHkWWkkkkwkkhk...",
        "..kHHkWWwwwkhhk....",
        "...kHHkkkkkhhk.....",
        "....kHHHHHhhk......",
        ".....kkHHhhk.......",
        ".......kkk.........",
    ], {"k": "ink", "G": "ivy_l", "g": "ivy_d", "H": "gray", "h": "hair", "W": "mask_l", "w": "mask_m",
        "n": "pur_d", "R": "lips", "P": "pur_l"})
    return f, pal


# --------------------------------------------------------------------------
# Silenos: the god's old tutor. Bald, round and very old, red-nosed and
# merry-eyed, pointed satyr's ears, a white beard spilling over his belly, a
# goatskin slung over his far shoulder, and the wineskin he never puts down
# hugged under his near arm. His far hand waves you over: "Sit!"
# --------------------------------------------------------------------------

def silenos():
    pal = Palette([
        ("ink", INK),
        ("skin_l", (248, 192, 152)), ("skin_m", (216, 136, 104)), ("skin_d", (160, 88, 64)),
        ("nose", (216, 72, 64)),
        ("wh_l", (248, 248, 240)), ("wh_d", (200, 192, 184)),
        ("goat_l", (176, 152, 120)), ("goat_m", (120, 96, 72)), ("goat_d", (72, 56, 48)),
        ("lea_l", (184, 96, 56)), ("lea_d", (112, 56, 40)),
        ("brown", (96, 56, 40)),
    ])
    skin = skin_mat("brown")
    goat = Mat(["goat_d", "goat_m", "goat_l"], outline="ink", wx=0.75, wy=0.35, cuts=[0.4, 0.75])
    linen = Mat(["wh_d", "wh_l"], outline="brown", wx=0.8, wy=0.3, cuts=[0.6])
    wine = Mat(["lea_d", "lea_l"], outline="ink", wx=0.7, wy=0.5, cuts=[0.55])
    lea = Mat(["brown"])
    f = Fig(pal)

    # short legs, sandals
    f.poly([(26, 49), (31, 49), (31, 56), (25, 56)], skin, group=100)
    f.poly([(35, 49), (40, 49), (41, 56), (35, 56)], skin, group=101)
    f.poly([(23, 56), (31, 56), (31, 60), (22, 60)], lea)
    f.poly([(35, 56), (42, 56), (43, 60), (35, 60)], lea)
    # a great round belly, broad in the shoulder
    f.ellipse((18, 21, 47, 51), skin, group=410)
    # linen loincloth below it
    f.poly([(22, 45), (44, 45), (42, 51), (24, 51)], linen, group=420)
    # goatskin over his far shoulder
    gs = f.poly([(37, 22), (44, 22), (48, 30), (49, 40), (47, 45), (45, 39), (43, 42), (41, 32)], goat, group=70)
    # the wineskin hugged under his near arm
    f.poly([(8, 31), (20, 29), (23, 34), (21, 41), (14, 43), (7, 39)], wine, group=500)
    f.thick_line([(23, 27), (18, 34), (21, 38)], 5, skin, group=200)
    # far arm up, beckoning
    f.thick_line([(44, 27), (49, 22), (51, 16)], 5, skin, group=300)

    f.textures = [((gs,), ["goat_d", "goat_m", "goat_l"], stagger(37, 23, 49, 46, 3, 3), [(0, 0), (0, 1)])]
    # the wineskin's tied neck, dribbling
    f.patch(4, 33, [
        ".kk..",
        "kLDk.",
        "kDkk.",
        ".kk..",
        "..N..",
    ], {"k": "ink", "L": "lea_l", "D": "lea_d", "N": "nose"})
    fist(f, 18, 35, "brown")
    f.patch(48, 10, [
        ".k.k...",
        "kLkLk..",
        "kLkLkk.",
        "kLLLLLk",
        "kLLLLMk",
        ".kLLMk.",
        "..kkk..",
    ], {"k": "brown", "L": "skin_l", "M": "skin_m"})
    # belly button and a shine on the belly
    f.pxs([(31, 39)], "skin_d")
    f.line([(28, 41), (30, 42), (33, 42), (35, 41)], "skin_m")
    # head: bald, satyr ears, merry squint, red nose, beard over the belly
    f.patch(21, 5, [
        "........kkkkkk.......",
        "......kkLLLLLMkk.....",
        ".....kLLLLLLLLMMk....",
        ".k..kLLLLLLLLLMMMk.k.",
        ".kLkLLLLLLLLLLMMMkLk.",
        "..kLkLLLLLLLLMMMkLMk.",
        "..kLbLLLLLLLLMMDbLk..",
        "...bLkLLLLkLMMDbk....",
        "...bkLkLLkLkMDbk.....",
        "..bLLLLNNLLLMMb......",
        "..bLWWLNNNWWMbk......",
        ".kWWWWWWkkWWWWWk.....",
        ".kWWWWWkllkWWWwk.....",
        ".kWwWWWWWWWWWwwk.....",
        "..kWWwWWWWWWwwk......",
        "..kWWWwWWWWwwk.......",
        "...kWWWWwWwwk........",
        "...kWWwWWwwk.........",
        "....kWWWwwk..........",
        ".....kkWwk...........",
        ".......kk............",
    ], {"k": "ink", "L": "skin_l", "M": "skin_m", "D": "skin_d", "b": "brown", "N": "nose", "W": "wh_l",
        "w": "wh_d", "l": "lea_d"})
    return f, pal


CLASSES = {
    "maenad": maenad,
    "satyr": satyr,
    "actor": actor,
    "vintner": vintner,
    "hierophant_thespis": thespis,
    "silenos": silenos,
}

SHEET = os.path.join(ROOT, "design/phase3/img/portraits_batch1.png")
REFS = ("kleon", "harvester", "goatherd", "acolyte_m", "hierophant_ione")


def tiles_sheet(images, cols):
    tiles = [battle_tile(im) for im in images]
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGBA", (96 * cols, 72 * rows), (232, 224, 200, 255))
    for i, t in enumerate(tiles):
        out.alpha_composite(t, (96 * (i % cols), 72 * (i // cols)))
    return out


def contact_sheet(figs, k=3):
    """The slice's Kleon and four Act I portraits on the top row for scale and
    style, then the batch's six, on the grass battle background, labelled."""
    refs = [load_pic(os.path.join(FRONT, n + ".png")) for n in REFS]
    news = [to_rgba(arr, pal) for arr, pal in figs.values()]
    cols = max(len(REFS), 3)
    pad = [Image.new("RGBA", (64, 64))] * (-len(refs) % cols)
    big = upscale(tiles_sheet(refs + pad + news, cols), k)
    d = ImageDraw.Draw(big)
    try:
        font = ImageFont.load_default(size=16)
    except TypeError:
        font = ImageFont.load_default()
    names = list(REFS) + [""] * len(pad) + list(figs)
    for i, n in enumerate(names):
        if n:
            label = n + (" (Act I)" if n in REFS else "")
            d.text((96 * k * (i % cols) + 6, 72 * k * (i // cols) + 4), label, fill=(32, 24, 24, 255), font=font)
    return big


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    write = "--write" in args
    only = [a for a in args if a in CLASSES]
    figs = {}
    for name, fn in CLASSES.items():
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
        contact_sheet(figs, 2).save(SHEET)
    if pv:
        os.makedirs(pv, exist_ok=True)
        contact_sheet(figs).save(os.path.join(pv, "portraits.png"))
        for name, (arr, pal) in figs.items():
            upscale(to_rgba(arr, pal), 6).save(os.path.join(pv, name + ".png"))
            grid_preview(to_rgba(arr, pal), 12, 4, 0, 60, 64).save(os.path.join(pv, name + "_grid.png"))


if __name__ == "__main__":
    main()
