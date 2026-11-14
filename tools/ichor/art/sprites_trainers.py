"""Trainer front pics for the Phase 1 cast (Kleon, Ione, Titan grunt, Daphne, Alethea).

Usage: python3 tools/ichor/art/sprites_trainers.py [NAME ...] [--write] [--preview DIR]

--write   writes the 64x64 indexed PNGs to graphics/trainers/front_pics/ and,
          for Daphne, also graphics/birch_speech/birch.png (the new-game
          intro portrait that replaces Birch).
--preview writes upscaled previews, a battle-background contact sheet and
          pixel grids to DIR.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import (ROOT, Palette, Mat, Fig, save_indexed, to_rgba, battle_bg,  # noqa: E402
                         upscale, palette_report, grid_preview)
from PIL import Image  # noqa: E402

INK = (32, 24, 24)
FRONT = os.path.join(ROOT, "graphics/trainers/front_pics")


# --------------------------------------------------------------------------
# Kleon, the rival from Lakonia
# --------------------------------------------------------------------------

def kleon():
    pal = Palette([
        ("ink", INK),
        ("skin_l", (248, 208, 168)), ("skin_m", (224, 160, 112)), ("skin_d", (176, 104, 72)),
        ("hair_d", (48, 32, 32)), ("hair_l", (96, 64, 48)),
        ("cr_l", (216, 72, 64)), ("cr_m", (168, 40, 48)), ("cr_d", (104, 24, 40)),
        ("br_l", (248, 216, 120)), ("br_m", (216, 160, 64)), ("br_d", (144, 88, 40)),
        ("lin_l", (248, 240, 216)), ("lin_d", (200, 176, 144)),
        ("lea", (104, 56, 40)),
    ])
    skin = Mat(["skin_d", "skin_m", "skin_l"], outline="lea", cuts=[0.5, 0.86])
    cloak = Mat(["cr_d", "cr_m", "cr_l"], wx=0.85, wy=0.15, cuts=[0.2, 0.6])
    linen = Mat(["lin_d", "lin_l"], wx=0.8, wy=0.2, cuts=[0.62])
    bronze = Mat(["br_d", "br_m", "br_l"], cuts=[0.3, 0.7])
    hair = Mat(["hair_d", "hair_l"], wx=0.5, wy=0.6, cuts=[0.3])
    leather = Mat(["lea"])
    ball_top = Mat(["cr_m", "cr_l"])
    ball_bot = Mat(["lin_d", "lin_l"])
    f = Fig(pal)

    # cloak, behind everything, billowing to his left
    f.poly([(25, 23), (38, 23), (43, 28), (47, 36), (51, 46), (52, 52), (48, 51), (45, 54), (41, 51),
            (37, 53), (31, 51), (26, 53), (21, 51), (20, 44), (21, 32)], cloak)
    f.shade_poly([(44, 36), (45, 36), (48, 52), (46, 52)], 0.5)
    f.shade_poly([(40, 40), (41, 40), (42, 52), (41, 52)], 0.5)
    f.shade_poly([(47, 40), (48, 40), (51, 50), (50, 50)], -0.4)
    # legs, feet apart
    f.poly([(25, 41), (29, 41), (29, 46), (28, 52), (27, 57), (24, 57), (24, 52), (24, 46)], skin, group=100)
    f.poly([(33, 41), (37, 41), (38, 46), (39, 52), (40, 57), (37, 57), (35, 52), (34, 46)], skin, group=101)
    f.poly([(22, 57), (28, 57), (28, 61), (21, 61)], leather)
    f.poly([(36, 57), (41, 57), (43, 61), (36, 61)], leather)
    # tunic (exomis) and belt
    tunic = f.poly([(25, 23), (37, 23), (37, 32), (39, 40), (37, 42), (31, 42), (25, 42), (23, 40), (25, 32)], linen)
    f.rect(22, 32, 40, 33, leather, clip=tunic)
    f.shade_poly([(30, 35), (31, 35), (31, 42), (30, 42)], 0.6)
    f.shade_poly([(35, 35), (36, 35), (37, 42), (36, 42)], 0.6)
    f.shade_poly([(33, 24), (35, 24), (35, 31), (33, 31)], 0.25)
    # right arm: fist on hip
    f.thick_line([(25, 25), (21, 31)], 4, skin, group=200)
    f.thick_line([(21, 31), (25, 34)], 3, skin, group=200)
    f.ellipse((23, 32, 26, 35), skin, group=200)
    # left arm: raised, showing off a ball
    upper = f.thick_line([(37, 25), (42, 29)], 4, skin, group=300)
    f.thick_line([(42, 29), (43, 22)], 3, skin, group=300)
    f.poly([(36, 26), (38, 25), (42, 27), (43, 30), (41, 31)], bronze, clip=upper)
    f.ellipse((40, 15, 46, 21), ball_bot, group=310)
    f.poly([(40, 17), (41, 15), (45, 15), (46, 17)], ball_top, group=311)
    f.ellipse((41, 20, 44, 23), skin, group=312)
    # neck (the head itself is hand-drawn below)
    f.rect(29, 20, 33, 25, skin, group=400)
    # cloak pinned at the left shoulder with a bronze brooch
    f.ellipse((35, 22, 37, 24), bronze)
    # tunic folds
    f.line([(28, 36), (27, 41)], "lin_d")
    f.line([(33, 35), (33, 41)], "lin_d")
    f.line([(27, 25), (29, 30)], "lin_d")
    # knees, sandal straps, armband shine
    f.pxs([(26, 49), (36, 49)], "skin_m")
    f.line([(24, 54), (27, 54)], "lea")
    f.line([(37, 54), (39, 54)], "lea")
    f.pxs([(38, 27), (39, 27), (35, 22)], "br_l")
    # head: cropped Lakonian hair, heavy brows, a smirk
    f.patch(24, 4, [
        ".....k..k..k....",
        "....kHkkHkkHkk..",
        "...kHhHHhHHHHHk.",
        "..kHhhHHhHHHhHHk",
        "..kHhHHHHHHhHHHk",
        ".kHHhHHHHHHHHHHk",
        ".kHHHHHhHHHHHhHk",
        ".kHHHHHHHHHHHHHk",
        ".kHHMMMMHMMMMHHk",
        ".kHLkkkLLLkkkMHk",
        ".kLLkkLLLLkkMDMb",
        ".kLLkWLLLLkWMDDb",
        ".kLLMMLLLLMMMDDb",
        ".kLLLLLLDLLMMDb.",
        "..bLLLLLDDLMMMb.",
        "..bLLLLLLLLkMMb.",
        "...bLLLLDkkMMb..",
        "...bLLLLLLLMMb..",
        "....bLLLLMMMb...",
        ".....bbbbbbb....",
    ], {"k": "ink", "H": "hair_d", "h": "hair_l", "L": "skin_l", "M": "skin_m", "D": "skin_d",
        "b": "lea", "W": "lin_l"})
    # the ball in his raised hand
    f.patch(40, 15, [
        ".kkkk.",
        "kRRCCk",
        "kkWkkk",
        "kWWwwk",
        ".kwwk.",
    ], {"k": "ink", "R": "cr_l", "C": "cr_m", "W": "lin_l", "w": "lin_d"})
    return f, pal


# --------------------------------------------------------------------------
# Hierophant Ione, the Hearthkeeper (Temple of Hestia)
# --------------------------------------------------------------------------

def hierophant_ione():
    pal = Palette([
        ("ink", INK),
        ("skin_l", (248, 216, 184)), ("skin_m", (224, 168, 128)), ("skin_d", (176, 112, 80)),
        ("lea", (112, 64, 48)),
        ("hair", (72, 40, 32)),
        ("veil_l", (248, 240, 216)), ("veil_m", (224, 200, 160)), ("veil_d", (168, 136, 104)),
        ("robe_l", (232, 136, 80)), ("robe_m", (192, 88, 48)), ("robe_d", (128, 48, 32)),
        ("gold_l", (248, 216, 96)), ("gold_m", (216, 152, 48)), ("gold_d", (136, 80, 32)),
    ])
    skin = Mat(["skin_d", "skin_m", "skin_l"], outline="lea", cuts=[0.5, 0.86])
    veil = Mat(["veil_d", "veil_m", "veil_l"], wx=0.8, wy=0.2, cuts=[0.3, 0.7])
    robe = Mat(["robe_d", "robe_m", "robe_l"], wx=0.85, wy=0.15, cuts=[0.25, 0.68])
    gold = Mat(["gold_d", "gold_m", "gold_l"], cuts=[0.3, 0.7])
    hair = Mat(["hair"])
    f = Fig(pal)

    # veil hanging down her back
    f.poly([(24, 20), (40, 20), (44, 30), (46, 44), (42, 48), (22, 48), (18, 44), (20, 30)], veil)
    # dark hair falling behind her shoulders, under the veil
    f.poly([(27, 20), (37, 20), (38, 26), (26, 26)], hair)
    # peplos, floor length
    robe_id = f.poly([(25, 22), (37, 22), (40, 30), (41, 40), (43, 52), (45, 60), (17, 60), (19, 52),
                      (21, 40), (22, 30)], robe)
    f.rect(16, 56, 46, 57, gold, clip=robe_id)
    f.rect(16, 37, 46, 38, gold, clip=robe_id)
    for x in (24, 29, 34, 39):  # long vertical folds
        f.shade_poly([(x, 40), (x + 1, 40), (x + 1 + (x - 31) // 5, 55), (x + (x - 31) // 5, 55)], 0.45)
    f.shade_poly([(26, 41), (27, 41), (26, 55), (25, 55)], -0.35)
    # sandal toes peeking out
    f.poly([(23, 60), (28, 60), (28, 62), (23, 62)], Mat(["lea"]))
    f.poly([(34, 60), (39, 60), (39, 62), (34, 62)], Mat(["lea"]))
    # neck
    f.rect(30, 20, 34, 25, skin, group=400)
    # veil panels falling over the shoulders and upper arms
    f.poly([(25, 20), (29, 21), (28, 28), (27, 36), (23, 40), (20, 39), (21, 30), (23, 24)], veil, group=500)
    f.poly([(35, 21), (39, 20), (41, 24), (43, 30), (44, 39), (41, 40), (37, 36), (36, 28)], veil, group=501)
    # forearms bringing the lamp to her chest
    f.thick_line([(24, 37), (29, 33)], 3, skin, group=600)
    f.thick_line([(40, 37), (35, 33)], 3, skin, group=601)
    # the bronze oil lamp: body, nozzle, ring handle
    f.ellipse((26, 31, 37, 36), gold, group=700)
    f.poly([(35, 31), (40, 30), (41, 32), (36, 35)], gold, group=700)
    f.ellipse((23, 31, 27, 35), gold, group=701)
    f.ellipse((24, 32, 26, 34), gold, erase=True)
    # hands over the lamp
    f.ellipse((27, 32, 30, 35), skin, group=602)
    f.ellipse((33, 32, 36, 35), skin, group=603)
    f.line([(29, 31), (34, 31)], "gold_d")
    f.pxs([(28, 32), (30, 31)], "gold_l")
    # flame on the nozzle
    f.patch(39, 24, [
        "..k..",
        ".kRk.",
        ".kRk.",
        "kRGRk",
        "kGWGk",
        ".kGk.",
    ], {"k": "robe_d", "R": "robe_l", "G": "gold_l", "W": "veil_l"})
    # head, framed by the veil
    f.patch(23, 4, [
        "........kkkk.......",
        "......kkWWWWkk.....",
        ".....kWWWWWWWVk....",
        "....kWWWWWWWWWVk...",
        "...kWWWWWWWWWWVVk..",
        "...kWWWWWWWWWWWVVk.",
        "..kWWWWkkkkkkkWWVVk",
        "..kWWWkHHHHHHHkWVVk",
        "..kWWkHHHHLHHHHkVVk",
        "..kWVHHHLLLLLHHHVVk",
        "..kWVHHDDLLDDMMHVVk",
        "..kWVHLkkLLkkMMHVVk",
        "..kWVHLkHLLkHMDHVVk",
        "..kWVHLLLLDLLMMHVVk",
        "..kWVHLLLLDLMMMHVVk",
        "..kWVHbLLLLLMMbHVVk",
        "..kWVHHbLDDLMbHHVVk",
        "..kWVHHHbLLMbHHHVVk",
        "..kWVVHHHbbbHHHVVVk",
    ], {"k": "ink", "W": "veil_l", "V": "veil_m", "H": "hair", "L": "skin_l", "M": "skin_m",
        "D": "skin_d", "b": "lea"})
    return f, pal


# --------------------------------------------------------------------------

CAST = {
    "kleon": kleon,
    "hierophant_ione": hierophant_ione,
}


def battle_tile(im):
    tile = battle_bg().crop((240 - 96, 40, 240, 112)).copy()
    tile.alpha_composite(im, (16, 4))
    return tile


def preview(figs, out, refs=("brendan", "may")):
    tiles = []
    for r in refs:
        p = os.path.join(os.path.dirname(out), "ref_%s.png" % r)
        if os.path.exists(p):
            tiles.append(battle_tile(Image.open(p).convert("RGBA")))
    for name, (arr, pal) in figs.items():
        tiles.append(battle_tile(to_rgba(arr, pal)))
    sheet = Image.new("RGBA", (96 * len(tiles), 72))
    for i, t in enumerate(tiles):
        sheet.alpha_composite(t, (96 * i, 0))
    upscale(sheet, 4).save(out)


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    write = "--write" in args
    only = [a for a in args if a in CAST]
    figs = {}
    for name, fn in CAST.items():
        if only and name not in only:
            continue
        f, pal = fn()
        arr = f.render()
        palette_report(arr, pal, name)
        figs[name] = (arr, pal)
        if write:
            save_indexed(arr, pal, os.path.join(FRONT, name + ".png"))
    if pv:
        os.makedirs(pv, exist_ok=True)
        preview(figs, os.path.join(pv, "trainers.png"))
        for name, (arr, pal) in figs.items():
            upscale(to_rgba(arr, pal), 6).save(os.path.join(pv, name + ".png"))
            grid_preview(to_rgba(arr, pal), 12, 8, 0, 56, 64).save(os.path.join(pv, name + "_grid.png"))


if __name__ == "__main__":
    main()
