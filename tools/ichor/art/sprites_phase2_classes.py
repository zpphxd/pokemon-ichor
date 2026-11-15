"""Trainer front pics for Phase 2's first batch: the voyage and Aegina.

Alethea's front pic, and the portraits for the Merchant, the Pilgrim and an
Ichor Sailor. Each is a 64x64, 16-color Gen 3 front pic in a 3/4 view facing
the player's side (screen left), lit from the top left, in the slice's style
(sprites_classes.py). See design/phase2/SPRITES.md.

Usage: python3 tools/ichor/art/sprites_phase2_classes.py [NAME ...] [--write] [--preview DIR]

--write   writes the indexed PNGs to graphics/trainers/front_pics/ and, when
          no NAME is given, the contact sheet design/phase2/img/sprites_classes.png.
--preview writes the 3x battle-background contact sheet (the slice's cast and
          classes above for scale), a 6x review row, 6x singles and pixel grids to DIR.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import (ROOT, Palette, Mat, Fig, save_indexed, to_rgba,  # noqa: E402
                         upscale, palette_report, grid_preview)
from sprites_classes import (INK, SKIN_SUN, SKIN_TAN, skin_mat, render, pole,  # noqa: E402
                             load_pic, sheet)
import sprites_alethea_back as AB  # noqa: E402
from PIL import Image  # noqa: E402

FRONT = os.path.join(ROOT, "graphics/trainers/front_pics")
SHEET = os.path.join(ROOT, "design/phase2/img/sprites_classes.png")

HAND = [".bbbb.", "bLLLLb", "bLbLMb", "bLLMMb", ".bbbb."]

# Alethea's letters, on her back pic's palette (sprites_alethea_back.PAL)
AKEY = {"k": "ink", "b": "brown", "h": "umber", "u": "umber", "L": "skin_l", "M": "skin_m", "D": "skin_d",
        "U": "blue_l", "B": "blue_m", "N": "blue_d", "O": "gold_l", "o": "gold_m",
        "W": "linen_l", "w": "linen_d", "R": "red"}


def hand(f, x, y, outline="brown"):
    f.patch(x, y, HAND, {"b": outline, "L": "skin_l", "M": "skin_m"})


# --------------------------------------------------------------------------
# Alethea: Daphne's apprentice, a digger of ruins. Dark ponytail under a blue
# headband, a sun-gold chiton to the knee, a satchel of scrolls on her left
# hip, a small trowel held up in her right hand. Her back pic's palette.
# --------------------------------------------------------------------------

def alethea():
    pal = AB.PAL
    skin = Mat(["skin_d", "skin_m", "skin_l"], outline="brown", cuts=[0.5, 0.86])
    chiton = Mat(["umber", "gold_m", "gold_l"], wx=0.85, wy=0.2, cuts=[0.3, 0.74])
    lea = Mat(["brown"])
    satchel = Mat(["brown", "umber"], wx=0.6, wy=0.5, cuts=[0.55])
    hair = Mat(["brown", "umber"], outline="ink", wx=0.9, wy=0.1, cuts=[0.7])
    f = Fig(pal)

    # the ponytail, tied at the back of her head and swinging behind her shoulder
    tail = f.poly([(36, 13), (39, 12), (43, 15), (44, 21), (49, 26),
                   (47, 29), (43, 27), (41, 22), (39, 18)], hair, group=40)
    # legs, weight on the far one
    f.poly([(26, 45), (31, 45), (28, 51), (24, 57), (20, 57), (23, 51)], skin, group=100)
    f.poly([(34, 45), (38, 45), (39, 51), (40, 57), (36, 57), (35, 51)], skin, group=101)
    f.poly([(20, 55), (25, 56), (24, 59), (25, 61), (17, 61), (17, 59)], lea)
    f.poly([(35, 57), (41, 57), (42, 61), (35, 61)], lea)
    f.line([(21, 57), (24, 57)], "umber")
    f.line([(36, 57), (39, 57)], "umber")
    # the chiton to the knee, bloused over a leather girdle
    body = f.poly([(26, 23), (38, 23), (40, 31), (41, 38), (43, 47), (22, 47), (24, 38), (25, 31)], chiton)
    f.rect(22, 33, 42, 34, lea, clip=body, noline=True)
    for x in (28, 33, 38):
        f.shade_poly([(x, 37), (x + 1, 37), (x + 1 + (x - 33) // 4, 46), (x + (x - 33) // 4, 46)], 0.45)
    f.shade_poly([(31, 25), (32, 25), (32, 31), (31, 31)], 0.35)
    f.shade_poly([(25, 30), (27, 30), (24, 46), (22, 46)], -0.3)
    f.rect(29, 19, 34, 25, skin, group=400)
    # satchel strap from her right shoulder across to the left hip
    f.thick_line([(27, 24), (34, 30), (40, 36)], 2, lea, group=20)
    # far arm down, hand on the satchel's flap
    f.thick_line([(39, 25), (42, 30), (42, 35)], 4, skin, group=300)
    f.poly([(37, 23), (41, 24), (42, 28), (39, 29)], chiton, group=310)
    # near arm raised, the trowel held up like a find
    f.thick_line([(26, 26), (21, 30)], 5, skin, group=200)
    f.thick_line([(21, 30), (18, 23)], 4, skin, group=200)
    f.poly([(24, 23), (28, 23), (28, 28), (25, 29), (23, 27)], chiton, group=210)
    # the satchel of scrolls on her left hip
    f.poly([(37, 37), (47, 37), (47, 44), (45, 46), (39, 46), (37, 44)], satchel, group=500)

    f.textures = [((tail,), ["brown", "umber"], [(39, 14), (41, 17), (42, 21), (45, 25), (47, 27)],
                   [(0, 0), (0, 1)])]
    # a kolpos line where the chiton blouses over the girdle
    f.line([(24, 32), (40, 32)], "gold_m")
    # satchel flap, buckle and two scroll ends
    f.patch(36, 32, [
        "..kkk.kkk...",
        ".kWWWkWWwk..",
        ".kwWwkwWwk..",
        "kkkkkkkkkkk.",
        "kbbbbbbbbbbk",
        "khhhhhhhhhbk",
        ".khhhkOkhhbk",
        "..kbbbbbbbk.",
    ], AKEY)
    hand(f, 39, 33, "brown")
    # the trowel: an iron-bladed trowel, its handle in her fist
    f.patch(13, 9, [
        "...k...",
        "..kWk..",
        "..kWwk.",
        ".kWWwk.",
        ".kWWwwk",
        "kWWwwwk",
        "kkkkkkk",
        "...kk..",
        "..kuuk.",
        "..kuuk.",
        "..kbbk.",
    ], AKEY)
    hand(f, 15, 19, "brown")
    # dust from the dig on her hem and knee
    f.pxs([(24, 45), (27, 46), (39, 45), (27, 51)], "umber")
    # head: a blue headband over dark hair parted in a fringe, eyes wide, a grin
    f.patch(22, 5, [
        "......kkkkk.....",
        "....kkbhhbbkk...",
        "...kbhhbbbbbbk..",
        "..kbhbbbbbbbbbk.",
        "..kUUUUBBBBBNNk.",
        "..kBBBBBBBBNNNk.",
        "..kbbbLLbbLLbbk.",
        "..kbLLLLLLLLbbk.",
        "..bLLkkLLLkkMbk.",
        "..bLLkWLLLkWMbk.",
        "..bLLkkLLLkkMbk.",
        "...bLLLLLLLMMbk.",
        "...bLLMLLLMMMbk.",
        "....bLLkWkMMbk..",
        ".....bLLLMMbk...",
        "......bLMMbk....",
        ".......bbbb.....",
    ], AKEY)
    return f, pal


# --------------------------------------------------------------------------
# Merchant: a portly trader in a dyed himation, a fat purse at his belt and a
# set of scales held up to weigh your silver. The walker is the slice's
# merchant (balding, brown beard, Aegean blue).
# --------------------------------------------------------------------------

def merchant():
    pal = Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("brown", (88, 48, 32)),
        ("hair", (112, 64, 40)),
        ("blue_l", (112, 152, 224)), ("blue_m", (48, 88, 176)), ("blue_d", (32, 40, 112)),
        ("lin_l", (248, 240, 216)), ("lin_d", (200, 184, 152)),
        ("gold_l", (248, 216, 112)), ("gold_m", (216, 152, 56)),
        ("ter", (184, 72, 48)),
    ])
    skin = skin_mat("brown")
    robe = Mat(["blue_d", "blue_m", "blue_l"], wx=0.85, wy=0.25, cuts=[0.28, 0.7])
    linen = Mat(["lin_d", "lin_l"], outline="brown", wx=0.8, wy=0.3, cuts=[0.62])
    lea = Mat(["brown"])
    purse = Mat(["brown", "ter"], wx=0.6, wy=0.6, cuts=[0.55])
    f = Fig(pal)

    # legs under the chiton's hem, planted wide under the weight
    f.poly([(25, 52), (29, 52), (29, 57), (25, 57)], skin, group=100)
    f.poly([(36, 52), (40, 52), (40, 57), (36, 57)], skin, group=101)
    f.poly([(22, 57), (29, 57), (29, 61), (21, 61)], lea)
    f.poly([(36, 57), (42, 57), (44, 61), (36, 61)], lea)
    # the linen chiton, to the shin
    f.poly([(25, 24), (39, 24), (43, 34), (43, 54), (22, 54), (21, 34)], linen)
    for x in (27, 33, 39):
        f.shade_poly([(x, 50), (x + 1, 50), (x + 1, 54), (x, 54)], 0.5)
    # the dyed himation round a round belly, its edge from the near hip to the far shoulder
    f.poly([(33, 23), (41, 23), (45, 28), (46, 36), (46, 44), (44, 49), (38, 52), (29, 52), (23, 50),
            (19, 46), (18, 41), (20, 38), (26, 36), (32, 31)], robe, group=130)
    f.shade_poly([(38, 38), (39, 38), (40, 51), (39, 51)], 0.45)
    f.shade_poly([(42, 30), (43, 30), (45, 47), (44, 47)], 0.45)
    f.shade_poly([(28, 44), (36, 41), (36, 43), (28, 46)], 0.35)
    f.shade_poly([(19, 40), (26, 37), (26, 43), (20, 46)], -0.35)
    f.rect(29, 19, 35, 25, skin, group=400)
    # far arm hangs to the purse, wrapped in the himation
    f.thick_line([(41, 26), (46, 32), (45, 38)], 5, robe, group=300)
    # near arm held out, the scales hanging from his fist
    f.poly([(23, 24), (28, 24), (27, 30), (22, 31), (20, 28)], linen, group=200)
    f.thick_line([(21, 29), (12, 23)], 4, skin, group=210)
    # purse at his hip, heavy with coin
    f.ellipse((38, 39, 47, 48), purse, group=500)

    # gold dyer's stripe along the himation's edge
    f.line([(19, 40), (26, 36), (32, 31), (34, 25)], "gold_m")
    # purse: drawstring and a coin peeking out
    f.patch(40, 37, [
        "..kkk..",
        ".kbObk.",
        "..kbk..",
    ], {"k": "ink", "b": "brown", "O": "gold_l"})
    hand(f, 42, 37, "brown")
    # the scales: a bronze beam on a cord from his fist, two pans, the near
    # one dipping under a pair of coins
    f.patch(2, 25, [
        "........kk.......",
        ".kkkkkkkkkkkkkkk.",
        "kGGGGGGGGGGGGGGgk",
        ".kkkkkkkkkkkkkkk.",
        ".k.............k.",
        ".k.............k.",
        "k.k...........k.k",
        "k.k...........k.k",
        "k..k.........kkkk",
        "k..k.........kGgk",
        "kkkkk.........kk.",
        "kGggk............",
        ".kkk.............",
    ], {"k": "ink", "G": "gold_l", "g": "gold_m"})
    f.pxs([(3, 35), (5, 35)], "gold_l")
    hand(f, 8, 20, "brown")
    # head: balding crown, brown hair round the sides, full beard, a pleased smile
    f.patch(23, 2, [
        "......kkkkkk........",
        "....kkLLLLLLkk......",
        "...kLLLLLLLLLMk.....",
        "..kLLLLLLLLLLMMk....",
        "..kLLLLLLLLLLMMDk...",
        ".kHLLLLLLLLLMMMDHk..",
        ".kHHLLLLLLLLMMDHHk..",
        ".kHbbbLLLLbbbDHHHk..",
        ".bLkkkLLLLkkkMbHHk..",
        ".bLkWLLLLLkWMDbHk...",
        "bLLLLLLLLLLMDMbHk...",
        "bLLLLDLLLLMMMMbHk...",
        ".bHHDDHHHHHMMbHk....",
        ".kHHkWWWWkHHHHHk....",
        ".kHHHkkkkHHHHHHk....",
        "..kHHHHHHHHHHHk.....",
        "...kHHHHHHHHHk......",
        "....kkHHHHHkk.......",
        "......kkkk..........",
    ], {"k": "ink", "H": "hair", "b": "brown", "L": "skin_l", "M": "skin_m", "D": "skin_d",
        "W": "lin_l"})
    return f, pal


# --------------------------------------------------------------------------
# Pilgrim (female): a devotee on the roads in a dark hooded cloak over a white
# chiton, a staff, and a covered dish of Hecate's supper for the crossroads.
# The walker shares the initiate's white body under the same dark cloak.
# --------------------------------------------------------------------------

def pilgrim():
    pal = Palette([
        ("ink", INK),
        *SKIN_TAN,
        ("brown", (88, 48, 32)),
        ("cl_l", (80, 96, 160)), ("cl_m", (48, 56, 112)), ("cl_d", (24, 32, 64)),
        ("lin_l", (248, 240, 216)), ("lin_d", (200, 184, 152)),
        ("ter_l", (216, 112, 72)), ("ter_d", (152, 64, 40)),
        ("saf", (240, 184, 56)),
        ("wood", (168, 112, 64)),
    ])
    cloak = Mat(["cl_d", "cl_m", "cl_l"], wx=0.8, wy=0.3, cuts=[0.35, 0.78])
    linen = Mat(["lin_d", "lin_l"], outline="brown", wx=0.8, wy=0.3, cuts=[0.6])
    wood = Mat(["brown", "wood"], cuts=[0.7])
    lea = Mat(["brown"])
    f = Fig(pal)

    # staff in her far hand, planted beside her
    pole(f, (47, 4), (46, 61), wood, group=50)
    # white chiton to the ankle
    f.poly([(25, 30), (39, 30), (42, 44), (44, 58), (21, 58), (23, 44)], linen)
    f.poly([(23, 58), (28, 58), (28, 61), (22, 61)], lea)
    f.poly([(35, 58), (40, 58), (41, 61), (35, 61)], lea)
    for x in (29, 34):
        f.shade_poly([(x, 50), (x + 1, 50), (x + 1, 57), (x, 57)], 0.45)
    # the cloak: hood up, falling past her knees, open at the front
    f.poly([(25, 4), (36, 3), (43, 8), (45, 16), (44, 22), (46, 30), (47, 42), (47, 52), (42, 54),
            (37, 52), (37, 34), (33, 28), (28, 30), (26, 40), (27, 52), (21, 53), (19, 48), (20, 34),
            (22, 22), (21, 14)], cloak, group=60)
    for p in ([(40, 32), (41, 32), (43, 52), (42, 52)], [(23, 34), (24, 34), (23, 51), (22, 51)]):
        f.shade_poly(p, 0.45)
    f.shade_poly([(21, 14), (26, 6), (30, 6), (24, 24), (21, 24)], -0.35)
    # saffron cord at the waist
    f.rect(27, 41, 37, 42, Mat(["saf"]), noline=True)
    # far arm forward to the staff
    f.thick_line([(40, 27), (44, 32), (46, 33)], 5, cloak, group=300)
    # near arm holds the covered dish out at her waist
    f.thick_line([(25, 27), (22, 34), (24, 38)], 5, cloak, group=200)
    # the dish: a terracotta bowl under a linen cloth knotted with saffron
    f.patch(8, 28, [
        "......kkk........",
        ".....kYYYk.......",
        "....kkLYLkkk.....",
        "..kkLLLLLLlkk....",
        ".kLLLLLLLLLllk...",
        ".kLLLLLLLLllldk..",
        "kLLLLLLLLLlllldk.",
        "kLkLLkLLLkLlkldk.",
        ".kTTkTTTkTTtkttk.",
        ".kTTTTTTTTtttttk.",
        "..kTTTTTTtttttk..",
        "...kkTTttttkkk...",
        ".....kkkkkk......",
    ], {"k": "ink", "L": "lin_l", "l": "lin_d", "d": "brown", "Y": "saf",
        "T": "ter_l", "t": "ter_d"})
    hand(f, 21, 37, "brown")
    hand(f, 44, 30, "brown")
    # staff head: a knot of wood
    f.patch(45, 1, [
        ".kkk.",
        "kWwWk",
        "kwWwk",
        ".kwk.",
    ], {"k": "ink", "W": "wood", "w": "brown"})
    # face inside the hood: dark hair, one eyebrow up, a wry smile
    f.patch(25, 9, [
        "...kkkkkkkk...",
        "..kHHHHHhHHk..",
        ".kHHhLLLHHHHk.",
        ".kHLLLLLLLLHk.",
        "kHLHHLLLLHHMHk",
        "kLLkkLLLLkkMHk",
        "kLLkWLLLLkWDHk",
        "kLLLLLLLLLMDHk",
        "kLLLDLLLLMMMk.",
        ".kLDDLLLMMMHk.",
        ".kLLLLLLbMHk..",
        "..kLbbbbMMk...",
        "...kLLLMMk....",
        "....kkkkk.....",
    ], {"k": "ink", "H": "brown", "h": "wood", "L": "skin_l", "M": "skin_m", "D": "skin_d",
        "W": "lin_l", "b": "brown"})
    return f, pal


# --------------------------------------------------------------------------
# Sailor (Ichor): a bare-chested oarsman, tousled hair under a terracotta
# headband, a short jaw beard, an undyed linen chiton worn down as a kilt with
# a blue sash, and a coil of rope over one shoulder. The walker is the
# slice's sailor.
# --------------------------------------------------------------------------

def sailor():
    pal = Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("hair", (56, 40, 32)),
        ("ter_l", (224, 112, 72)), ("ter_m", (176, 64, 48)),
        ("lin_l", (240, 232, 208)), ("lin_d", (192, 176, 144)),
        ("blue_m", (48, 104, 176)), ("blue_d", (24, 56, 120)),
        ("rope_l", (232, 200, 136)), ("rope_m", (184, 144, 80)), ("rope_d", (120, 88, 48)),
        ("brown", (88, 48, 32)),
    ])
    skin = skin_mat("brown")
    kilt = Mat(["lin_d", "lin_l"], outline="brown", wx=0.8, wy=0.3, cuts=[0.62])
    sash = Mat(["blue_d", "blue_m"], cuts=[0.6])
    rope = Mat(["rope_d", "rope_m", "rope_l"], wx=0.6, wy=0.5, cuts=[0.4, 0.75])
    lea = Mat(["brown"])
    f = Fig(pal)

    # the coil's loops hanging behind his far shoulder
    back = f.ellipse((39, 21, 50, 41), rope, group=590)
    f.ellipse((42, 25, 47, 37), rope, group=590, erase=True)
    # legs, a wide sailor's stance
    f.poly([(24, 42), (30, 42), (29, 50), (27, 57), (22, 57), (23, 50)], skin, group=100)
    f.poly([(35, 42), (40, 42), (42, 50), (44, 57), (39, 57), (37, 50)], skin, group=101)
    f.poly([(20, 57), (28, 57), (28, 61), (19, 61)], lea)
    f.poly([(38, 57), (45, 57), (47, 61), (38, 61)], lea)
    # bare torso, broad at the shoulders
    f.poly([(24, 23), (40, 23), (43, 26), (41, 34), (40, 40), (25, 40), (23, 34), (21, 26)], skin, group=110)
    # the kilt, the linen chiton rolled down to the waist
    f.poly([(23, 37), (41, 37), (43, 46), (37, 47), (31, 46), (22, 46)], kilt)
    f.shade_poly([(30, 39), (31, 39), (31, 46), (30, 46)], 0.45)
    f.shade_poly([(36, 39), (37, 39), (38, 46), (37, 46)], 0.45)
    f.rect(22, 37, 42, 38, sash, noline=True)
    f.rect(29, 19, 34, 24, skin, group=400)
    # the coil across his chest, far shoulder to near hip
    band = f.thick_line([(40, 23), (32, 30), (24, 37)], 5, rope, group=600)
    # near arm: fist on his hip
    f.thick_line([(23, 25), (18, 31)], 5, skin, group=200)
    f.thick_line([(18, 31), (22, 36)], 4, skin, group=200)
    # far arm bent, thumb hooked under the rope at his shoulder
    f.thick_line([(41, 25), (46, 31)], 5, skin, group=300)
    f.thick_line([(46, 31), (41, 30)], 4, skin, group=300)

    # rope strands
    f.textures = [((back, band), ["rope_d", "rope_m", "rope_l"],
                   [(x, y) for x in range(20, 52, 2) for y in range(20, 42, 3)], [(0, 0)])]
    # chest and belly: pecs and a line of muscle
    f.line([(26, 30), (29, 31)], "skin_d")
    f.pxs([(33, 34), (33, 36), (35, 34), (35, 36)], "skin_m")
    hand(f, 19, 33, "brown")
    hand(f, 38, 27, "brown")
    # head: tousled hair under a terracotta headband with tails, short jaw beard, a grin
    f.patch(23, 2, [
        "....kk.kkkk.k.......",
        "...kHHkHHHHkHk......",
        "..kHHHHHHhHHHHk.....",
        ".kHHhHHHHHHHhHHk....",
        ".kHHHHHHHHHHHHHHk...",
        ".kTTTTTTTTTTTttHk...",
        ".kttttttttttttHHk.k.",
        ".kHLHHHLLLHHHMHHkTtk",
        ".bLHHHLLLLHHHMbHHttk",
        ".bLkkLLLLLLkkMbHkTk.",
        ".bLkWLLLLLLkWDbHk.k.",
        "bLLLLLLLLLLMDMbHk...",
        "bLLLLDLLLLMMMbHk....",
        ".bHLDDLLLMMMHbk.....",
        ".bHHkWWWWkMHHbk.....",
        "..bHHkkkkMHHbk......",
        "...bHHHHHHHbk.......",
        "....bbbbbbbk........",
    ], {"k": "ink", "H": "hair", "h": "brown", "b": "brown", "L": "skin_l", "M": "skin_m",
        "D": "skin_d", "W": "lin_l", "T": "ter_l", "t": "ter_m"})
    return f, pal


CLASSES = {
    "alethea": alethea,
    "merchant": merchant,
    "pilgrim": pilgrim,
    "ichor_sailor": sailor,
}


# --------------------------------------------------------------------------
# Previews
# --------------------------------------------------------------------------

def contact_sheet(figs):
    """3x: the slice's cast and classes on the top row for scale, then these."""
    refs = [load_pic(os.path.join(FRONT, n + ".png")) for n in
            ("kleon", "professor_daphne", "shepherd", "harvester", "hoplite")]
    news = [to_rgba(arr, pal) for arr, pal in figs.values()]
    cols = max(len(refs), len(news))
    pad = [Image.new("RGBA", (64, 64))] * (-len(refs) % cols)
    return upscale(sheet(refs + pad + news, cols=cols), 3)


def review_row(figs, k=6):
    """Every portrait at k times on a flat grass color, side by side."""
    tiles = []
    for arr, pal in figs.values():
        bg = Image.new("RGBA", (64, 64), (168, 200, 120, 255))
        bg.alpha_composite(to_rgba(arr, pal))
        tiles.append(bg)
    out = Image.new("RGBA", (66 * len(tiles), 64), (200, 220, 200, 255))
    for i, t in enumerate(tiles):
        out.paste(t, (66 * i, 0))
    return upscale(out, k)


def preview(figs, pv):
    os.makedirs(pv, exist_ok=True)
    contact_sheet(figs).save(os.path.join(pv, "classes.png"))
    review_row(figs).save(os.path.join(pv, "row6x.png"))
    for name, (arr, pal) in figs.items():
        upscale(to_rgba(arr, pal), 6).save(os.path.join(pv, name + ".png"))
        grid_preview(to_rgba(arr, pal), 12, 0, 0, 64, 64).save(os.path.join(pv, name + "_grid.png"))


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
        contact_sheet(figs).save(SHEET)
    if pv:
        preview(figs, pv)


if __name__ == "__main__":
    main()
