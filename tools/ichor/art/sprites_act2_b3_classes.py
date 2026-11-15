"""Trainer front pics for Act II, batch 3 (Arkadia, beats 38-44).

The two new classes (Huntress, Charcoaler) and Hierophant Kallisto. Each is a
64x64, 16-color Gen 3 trainer pic in the slice's house style
(sprites_classes.py, sprites_act2_classes.py): a 3/4 view facing the player's
side (screen left), lit from the top left, the palette embedded in the PNG.
See design/phase3/SPRITES.md, "Batch 3".

Usage: python3 tools/ichor/art/sprites_act2_b3_classes.py [NAME ...] [--write] [--preview DIR]

--write   writes the indexed PNGs to graphics/trainers/front_pics/ and, when no
          NAME is given, the portrait sheet design/phase3/img/portraits_batch3.png
--preview writes the 3x sheet, 6x singles and pixel grids to DIR
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, Mat, Fig, save_indexed, to_rgba, upscale, palette_report, grid_preview  # noqa: E402,E501
from sprites_classes import INK, SKIN_SUN, SKIN_TAN, render, pole, stagger, skin_mat, load_pic, FRONT  # noqa: E402
from sprites_act2_classes import fist, tiles_sheet  # noqa: E402
from PIL import ImageDraw, ImageFont  # noqa: E402


# --------------------------------------------------------------------------
# Huntress: one of Artemis's acolytes. A young woman in a short saffron
# chiton girt high for running, a fawnskin over her near shoulder pinned with
# a silver crescent, her hair bound up in a knot, laced hunting boots, the
# quiver on her back, and her bow held low in her near hand. Her far hand
# reaches back to the arrows.
# --------------------------------------------------------------------------

def huntress():
    pal = Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("hair", (56, 32, 24)), ("hair_l", (112, 64, 40)),
        ("saf_l", (248, 200, 72)), ("saf_m", (224, 144, 32)), ("saf_d", (160, 88, 32)),
        ("fawn_l", (216, 160, 96)), ("fawn_d", (152, 96, 56)),
        ("spot", (248, 232, 208)),
        ("wood", (96, 56, 32)),
        ("red", (176, 64, 48)),
        ("silver", (200, 200, 216)),
    ])
    skin = skin_mat("hair")
    chiton = Mat(["saf_d", "saf_m", "saf_l"], outline="hair", wx=0.8, wy=0.3, cuts=[0.28, 0.68])
    fawn = Mat(["fawn_d", "fawn_l"], outline="hair", wx=0.8, wy=0.4, cuts=[0.6])
    boot = Mat(["wood", "fawn_d"], outline="ink", wx=0.9, wy=0.1, cuts=[0.55])
    quiver = Mat(["wood", "red"], outline="ink", wx=0.8, wy=0.2, cuts=[0.5])
    bow = Mat(["wood", "fawn_d"], cuts=[0.6], wx=1.0, wy=0.0)
    f = Fig(pal)

    # the quiver on her back, slung from the far shoulder, its arrows up
    f.poly([(40, 12), (45, 10), (49, 32), (44, 34)], quiver, group=30)
    # legs: bare thighs below the short hem, laced boots to mid-shin
    f.poly([(27, 42), (32, 42), (32, 52), (29, 53), (27, 50)], skin, group=100)
    f.poly([(35, 42), (40, 42), (41, 50), (39, 53), (36, 52)], skin, group=101)
    f.poly([(26, 50), (32, 50), (32, 58), (33, 61), (24, 61), (26, 57)], boot, group=110)
    f.poly([(36, 50), (41, 50), (41, 57), (44, 61), (36, 61), (36, 57)], boot, group=111)
    f.rect(29, 19, 34, 24, skin, group=400)
    # the saffron chiton, girt high, hem at mid-thigh
    body = f.poly([(26, 22), (39, 22), (41, 30), (42, 38), (44, 45), (34, 46), (23, 45), (24, 38), (24, 30)],
                  chiton)
    for pts in ([(29, 35), (30, 35), (28, 45), (27, 45)], [(34, 35), (35, 35), (35, 45), (34, 45)],
                [(38, 34), (39, 34), (42, 44), (41, 44)]):
        f.shade_poly(pts, 0.45)
    f.shade_poly([(24, 30), (27, 30), (25, 44), (23, 44)], -0.3)
    # the girdle, high under the breast, and the blouse of cloth over it
    f.rect(22, 31, 44, 32, Mat(["red"]), clip=body, noline=True)
    # the fawnskin over her near shoulder, knotted at the far hip
    fawn_id = f.poly([(25, 22), (31, 22), (34, 27), (40, 35), (42, 40), (38, 41), (32, 34), (27, 29), (24, 27)],
                     fawn, group=70)
    f.poly([(40, 38), (43, 39), (44, 44), (42, 44)], fawn, group=71)
    # far arm up and back to the arrows; near arm down to the bow
    f.thick_line([(39, 24), (43, 20), (44, 14)], 4, skin, group=300)
    f.thick_line([(26, 24), (23, 31), (22, 37)], 4, skin, group=200)
    # the bow held low, its belly forward, the string slack behind
    f.spans(22, [(18, 19)] * 2 + [(17, 18)] * 3 + [(16, 17)] * 8 + [(17, 18)] * 4 + [(18, 19)] * 3
            + [(19, 20)] * 3 + [(20, 21)] * 3 + [(21, 22)] * 2, bow, group=50)

    f.textures = [((fawn_id,), ["fawn_d", "fawn_l"], stagger(25, 23, 42, 40, 4, 3), [(0, 0)])]
    f.line([(19, 22), (21, 34), (21, 40), (22, 54)], "spot")
    f.pxs([(28, 25), (31, 28), (34, 31), (37, 35), (39, 38), (29, 27), (36, 33)], "spot")
    # the crescent pin at the shoulder
    f.patch(25, 21, [".ss.", "s..s", ".kk."], {"s": "silver", "k": "ink"})
    # boot laces
    for y in (52, 54, 56):
        f.pxs([(28, y), (30, y + 1), (38, y), (40, y + 1)], "fawn_l")
    # arrows standing out of the quiver: shafts and red-and-white fletching
    f.patch(41, 2, [
        "..k...k..",
        ".kSk.kRk.",
        ".kSkkkRk.",
        "..kRkSk..",
        "..kRkSkk.",
        "...kwkwk.",
        "...kwkwk.",
        "....kwk..",
    ], {"k": "ink", "S": "spot", "R": "red", "w": "wood"})
    # her fist round the bow's grip; her far fingers at the fletching
    fist(f, 19, 34)
    f.patch(41, 11, [".kkk.", "kLLMk", "kLMMk", ".kkk."], {"k": "hair", "L": "skin_l", "M": "skin_m"})
    # head: hair bound up in a knot, a few loose strands, eyes on the quarry
    f.patch(23, 1, [
        "........kkkk.......",
        ".......kHHhhk......",
        "......kHhhhhk......",
        ".....kkkhhhkkk.....",
        "...kkHHHHhhhhhkk...",
        "..kHHhhhhhhhhhhhk..",
        ".khHhhhhhhhhhhhhhk.",
        ".khbLLLLLLLLMbhhhk.",
        ".kbLLLLLLLLLLMbhhk.",
        ".bkkkLLLLLkkkMbhk..",
        ".bLWkLLLLLkWLMDbk..",
        "bLLLLLLLLLLLMDbhk..",
        "bLLLLDLLLLLMMMbhk..",
        ".bLLDDLLLLMMMbhk...",
        ".bLLLLkkkLMMbhk....",
        "..bLLLLLLMMbk......",
        "...bbLLLMMbk.......",
        ".....bbbbbk........",
    ], {"k": "ink", "H": "hair_l", "h": "hair", "b": "hair", "L": "skin_l", "M": "skin_m",
        "D": "skin_d", "W": "spot"})
    return f, pal


# --------------------------------------------------------------------------
# Charcoaler: one of Arkadia's charcoal-burners. A stocky man black to the
# elbows, a sooty felt cap, a short beard and a soot-streaked face squinting
# against the smoke, a leather apron over a gray tunic, and the long iron
# rake over his far shoulder. Behind him a kiln mound smokes.
# --------------------------------------------------------------------------

def charcoaler():
    pal = Palette([
        ("ink", INK),
        *SKIN_SUN,
        ("soot_l", (152, 144, 136)), ("soot_m", (104, 96, 96)), ("soot_d", (64, 56, 56)),
        ("lea_l", (184, 128, 72)), ("lea_d", (120, 72, 40)),
        ("beard", (72, 48, 32)),
        ("smoke_l", (224, 224, 224)), ("smoke_d", (168, 168, 176)),
        ("earth", (136, 104, 72)),
        ("ember", (240, 120, 40)),
        ("iron", (200, 200, 208)),
    ])
    skin = skin_mat("beard")
    tunic = Mat(["soot_d", "soot_m", "soot_l"], outline="ink", wx=0.8, wy=0.3, cuts=[0.3, 0.7])
    apron = Mat(["lea_d", "lea_l"], outline="ink", wx=0.85, wy=0.25, cuts=[0.6])
    soot = Mat(["soot_d", "soot_m"], outline="ink", wx=0.8, wy=0.4, cuts=[0.6])
    iron = Mat(["soot_m", "iron"], cuts=[0.6], wx=1.0, wy=0.0)
    kiln = Mat(["lea_d", "earth"], outline="beard", wx=0.7, wy=0.5, cuts=[0.55])
    smoke = Mat(["smoke_d", "smoke_l"], outline="smoke_d", wx=0.7, wy=0.4, cuts=[0.55])
    f = Fig(pal)

    # the kiln mound behind him, smoke curling up from its crown
    kiln_id = f.ellipse((-4, 37, 28, 84), kiln, group=10)
    f.thick_line([(11, 39), (8, 31), (11, 24), (7, 17), (10, 10)], 5, smoke, group=12)
    f.ellipse((4, 5, 13, 12), smoke, group=12)
    # the rake's long iron shaft over his far shoulder, its head behind him
    f.thick_line([(36, 34), (46, 18), (55, 5)], 3, iron, group=40)
    f.rect(50, 1, 62, 3, Mat(["soot_d"]), group=41)
    # legs: short and thick, bare shins, wrapped feet
    f.poly([(25, 47), (31, 47), (31, 56), (25, 56)], skin, group=100)
    f.poly([(35, 47), (41, 47), (42, 56), (35, 56)], skin, group=101)
    f.poly([(23, 56), (31, 56), (31, 61), (22, 61)], soot)
    f.poly([(35, 56), (43, 56), (44, 61), (35, 61)], soot)
    f.rect(28, 20, 35, 25, skin, group=400)
    # the gray tunic: broad in the shoulder
    f.poly([(23, 23), (41, 23), (45, 30), (45, 41), (43, 49), (21, 49), (19, 41), (20, 30)], tunic)
    # the leather apron from chest to knee
    ap = f.poly([(24, 27), (39, 27), (41, 38), (42, 52), (22, 52), (23, 38)], apron, group=60)
    f.shade_poly([(33, 30), (34, 30), (36, 51), (35, 51)], 0.4)
    # near arm hanging, black to the elbow; far arm up to the shaft
    f.thick_line([(23, 25), (19, 33), (19, 40)], 6, skin, group=200)
    f.thick_line([(19, 34), (19, 41)], 6, soot, group=201)
    f.thick_line([(41, 25), (43, 31), (38, 34)], 6, skin, group=300)
    f.thick_line([(43, 30), (38, 34)], 6, soot, group=301)

    f.textures = [((ap,), ["lea_d", "lea_l"], stagger(24, 30, 41, 50, 5, 4), [(0, 0)]),
                  ((kiln_id,), ["lea_d", "earth"], stagger(0, 41, 24, 62, 4, 3), [(0, 0), (1, 0)])]
    # the apron's ties and a scorch on it
    f.pxs([(24, 27), (39, 27)], "beard")
    f.pxs([(29, 44), (30, 44), (30, 45)], "lea_d")
    # the rake's tines hanging from the head
    for x in (51, 54, 57, 60):
        f.line([(x, 4), (x, 7)], "soot_d")
    f.line([(50, 1), (62, 1)], "ink")
    # a glowing vent at the kiln's foot, sparks in the smoke
    f.patch(6, 52, [".kkkk.", "kEEEEk", "kEeeEk", "kkkkkk"], {"k": "beard", "E": "ember", "e": "smoke_l"})
    f.pxs([(10, 31), (13, 24), (8, 19)], "ember")
    # black fists
    f.patch(16, 39, [".kkkk.", "kddddk", "kdmddk", "kddmdk", ".kkkk."], {"k": "ink", "d": "soot_d", "m": "soot_m"})
    f.patch(35, 31, [".kkkk.", "kddddk", "kdmmdk", ".kkkk."], {"k": "ink", "d": "soot_d", "m": "soot_m"})
    # head: a sooty felt cap pulled low, a squint, soot on the cheek, a beard
    f.patch(22, 3, [
        "......kkkkkkk.......",
        "....kkTTTTTTTkk.....",
        "...kTTTTTTTTtttk....",
        "..kTTTTTTTTTTtttk...",
        "..kTTTTTTTTTTTttk...",
        ".ktttttttttttttttk..",
        ".kLLLLLLLLLLLLMbbk..",
        ".kLkkkLLLLLkkkMbbk..",
        ".kLLLLLLLLLLLLMDbk..",
        "kLLLLLLLLLLLMMDDbk..",
        "kLLLLsDLLLLLMMMbbk..",
        "kLsLLDDLLLsLMMbbbk..",
        ".kbbbLLLLLbbbbbbk...",
        ".bbbbbkkkbbbbbbbk...",
        "..bbbbbbbbbbbbbk....",
        "...bbbbbbbbbbbk.....",
        ".....kkbbbbkk.......",
    ], {"k": "ink", "T": "soot_m", "t": "soot_d", "b": "beard", "L": "skin_l", "M": "skin_m",
        "D": "skin_d", "s": "soot_m"})
    return f, pal


# --------------------------------------------------------------------------
# Hierophant Kallisto, the Huntress of the Moon: a woman of about thirty,
# tall and very still. A short silver-gray chiton girt for running, a dark
# bearskin over her far shoulder with the bear's head at her collarbone, a
# silver crescent pinning the chiton at the near shoulder, dark hair in one
# long braid over the near shoulder, and the bow she never draws slung across
# her back. Her face is lifted: she is looking at the sky.
# --------------------------------------------------------------------------

def hierophant_kallisto():
    pal = Palette([
        ("ink", INK),
        *SKIN_TAN,
        ("hair", (40, 32, 40)), ("hair_l", (96, 80, 96)),
        ("sil_l", (216, 216, 224)), ("sil_m", (160, 160, 176)), ("sil_d", (96, 96, 120)),
        ("bear_l", (112, 80, 64)), ("bear_d", (56, 40, 32)),
        ("white", (248, 248, 248)),
        ("wood", (144, 96, 56)),
        ("night", (48, 56, 112)),
    ])
    skin = skin_mat("hair")
    chiton = Mat(["sil_d", "sil_m", "sil_l"], outline="ink", wx=0.8, wy=0.35, cuts=[0.3, 0.62])
    bear = Mat(["bear_d", "bear_l"], outline="ink", wx=0.75, wy=0.4, cuts=[0.62])
    braid = Mat(["hair", "hair_l"], outline="ink", wx=1.0, wy=0.0, cuts=[0.55])
    bow = Mat(["wood"], outline="ink")
    sandal = Mat(["bear_d", "bear_l"], cuts=[0.6], wx=1.0, wy=0.0)
    f = Fig(pal)

    # the bow slung across her back, its upper limb over her far shoulder
    f.thick_line([(43, 17), (47, 10), (47, 3)], 3, bow, group=20)
    # the bearskin hanging down her back on the far side
    pelt = f.poly([(37, 18), (45, 18), (48, 26), (49, 40), (47, 52), (42, 55), (41, 42), (39, 30)], bear, group=30)
    # long legs, laced running boots
    f.poly([(27, 42), (32, 42), (32, 54), (28, 54)], skin, group=100)
    f.poly([(35, 42), (39, 42), (40, 54), (36, 54)], skin, group=101)
    f.poly([(27, 53), (32, 53), (32, 58), (33, 61), (25, 61), (27, 57)], sandal, group=110)
    f.poly([(36, 53), (40, 53), (40, 57), (43, 61), (36, 61)], sandal, group=111)
    f.rect(30, 16, 34, 21, skin, group=400)
    # the silver-gray chiton, girt at the waist, hem above the knee
    body = f.poly([(26, 19), (38, 19), (40, 27), (40, 35), (42, 44), (34, 45), (25, 44), (25, 35), (25, 27)],
                  chiton)
    for pts in ([(30, 33), (31, 33), (29, 44), (28, 44)], [(35, 33), (36, 33), (37, 44), (36, 44)]):
        f.shade_poly(pts, 0.45)
    f.shade_poly([(25, 27), (28, 27), (27, 43), (25, 43)], -0.3)
    f.rect(22, 30, 44, 31, Mat(["night"]), clip=body, noline=True)
    f.rect(22, 43, 44, 44, Mat(["night"]), clip=body, noline=True)
    # arms: the near one still at her side, the far hand on the bear's paw
    f.thick_line([(27, 21), (25, 29), (25, 36)], 4, skin, group=200)
    f.thick_line([(38, 21), (40, 27), (37, 30)], 4, skin, group=300)
    # the braid over her near shoulder and down her breast to the girdle
    f.thick_line([(30, 13), (29, 19), (29, 25), (30, 30)], 4, braid, group=500)

    f.textures = [((pelt,), ["bear_d", "bear_l"], stagger(37, 20, 49, 53, 3, 3), [(0, 0), (0, 1)])]
    # plaits down the braid, and its silver tie
    for y in (17, 20, 23, 26):
        f.pxs([(29, y), (30, y + 1)], "hair_l")
    f.patch(28, 30, ["kWWk", ".kk."], {"k": "ink", "W": "white"})
    # the bear's head on her far shoulder: round ears, a small eye, the snout
    f.patch(36, 11, [
        ".kk...kk..",
        "kBbk.kBbk.",
        "kbBBBBBbbk",
        ".kBkBBBBbk",
        ".kBBBBBbbk",
        "kkBBBbbbk.",
        "kbbbbbkk..",
        ".kkkkk....",
    ], {"k": "ink", "B": "bear_l", "b": "bear_d"})
    # the string of the slung bow, by its upper tip
    f.line([(46, 3), (44, 14)], "sil_l")
    # the crescent pin at her near shoulder
    f.patch(25, 18, ["kWWk.", "Wkkk.", "kWWk."], {"W": "white", "k": "ink"})
    # boot laces
    for y in (54, 56, 58):
        f.pxs([(29, y), (31, y), (37, y), (39, y)], "bear_l")
    # hands: near hand open at her side, far hand resting on the fur
    f.patch(23, 35, [".kkk.", "kLLLk", "kLLMk", "kLMMk", ".kkk."], {"k": "hair", "L": "skin_l", "M": "skin_m"})
    f.patch(35, 28, [".kkkk.", "kLLLMk", "kLMMMk", ".kkkk."], {"k": "hair", "L": "skin_l", "M": "skin_m"})
    # head: dark hair drawn smoothly back, the face lifted to the sky, the
    # eyes turned up, the mouth still
    f.patch(23, 0, [
        "........kkkkk.....",
        "......kkhhhhhkk...",
        ".....khHHhhhhhhk..",
        "....khHhhhhhhhhhk.",
        "...kLLLHhhhhhhhhk.",
        "..kLkkkLLhhhhhhhk.",
        "..kLWkLLLLhhhhhk..",
        ".kLLLLLLLLMhhhhk..",
        ".kLLLLLLLLMMhhhk..",
        "kLLLLDLLLLMMhhk...",
        "kLLLDDLLLMMMhhk...",
        ".kkLLLLLLMMbhk....",
        "..kLkkLLMMMbk.....",
        "..kLLLLLMMbk......",
        "...kkLLMMbk.......",
        ".....kkkkk........",
    ], {"k": "ink", "H": "hair_l", "h": "hair", "b": "hair", "L": "skin_l", "M": "skin_m",
        "D": "skin_d", "W": "white"})
    return f, pal


CLASSES = {
    "huntress": huntress,
    "charcoaler": charcoaler,
    "hierophant_kallisto": hierophant_kallisto,
}

SHEET = os.path.join(ROOT, "design/phase3/img/portraits_batch3.png")
REFS = ("kleon", "harvester", "maenad", "vintner", "hierophant_thespis")


def contact_sheet(figs, k=3):
    """Five earlier portraits on the top row for scale and style, then the
    batch's three, on the grass battle background, labelled."""
    refs = [load_pic(os.path.join(FRONT, n + ".png")) for n in REFS]
    news = [to_rgba(arr, pal) for arr, pal in figs.values()]
    cols = len(REFS)
    pad = []
    big = upscale(tiles_sheet(refs + pad + news, cols), k)
    d = ImageDraw.Draw(big)
    try:
        font = ImageFont.load_default(size=16)
    except TypeError:
        font = ImageFont.load_default()
    names = [n + " (earlier)" for n in REFS] + list(figs)
    for i, n in enumerate(names):
        d.text((96 * k * (i % cols) + 6, 72 * k * (i // cols) + 4), n, fill=(32, 24, 24, 255), font=font)
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
