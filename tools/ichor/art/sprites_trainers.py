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
    leather = Mat(["lea"])
    f = Fig(pal)

    f.poly([(24, 23), (36, 22), (41, 29), (45, 35), (53, 41), (57, 48),
            (54, 50), (47, 52), (42, 49), (35, 51), (26, 48), (19, 50), (20, 31)], cloak)
    for x, y in ((39, 29), (43, 34), (25, 31)):
        f.shade_poly([(x, y), (x + 1, y), (x + 7, 48), (x + 4, 48)], 0.45)
    f.shade_poly([(35, 29), (36, 29), (41, 48), (39, 48)], -0.35)
    f.poly([(25, 41), (30, 41), (28, 49), (23, 55), (19, 55), (23, 48)], skin, group=100)
    f.poly([(33, 40), (38, 40), (38, 47), (40, 55), (36, 56), (33, 49)], skin, group=101)
    f.poly([(19, 53), (24, 54), (24, 59), (26, 61), (15, 61), (15, 59)], leather)
    f.poly([(35, 54), (40, 53), (41, 58), (45, 60), (45, 61), (34, 61)], leather)
    f.line([(19, 57), (23, 57)], "br_d")
    f.line([(36, 57), (39, 57)], "br_d")
    tunic = f.poly([(25, 22), (36, 24), (36, 31), (35, 34), (39, 43),
                    (34, 44), (30, 43), (26, 44), (23, 42), (25, 33), (23, 27)], linen)
    f.rect(22, 33, 40, 34, leather, clip=tunic)
    for a, b in (((27, 35), (25, 42)), ((31, 36), (32, 43)), ((33, 25), (34, 31))):
        f.line([a, b], "lin_d")
    f.thick_line([(25, 26), (18, 31), (24, 35)], 5, skin, group=200)
    f.poly([(20, 25), (24, 23), (26, 25), (24, 29), (21, 29)], bronze, group=210)
    f.thick_line([(36, 26), (42, 30), (44, 22)], 4, skin, group=300)
    f.rect(28, 20, 31, 25, skin, group=400)
    f.poly([(24, 22), (29, 23), (35, 22), (39, 24), (38, 28),
            (32, 28), (26, 25), (22, 25)], cloak, group=410)
    f.ellipse((24, 22, 27, 25), bronze, group=420)
    f.pxs([(22, 25), (23, 25), (25, 23)], "br_l")
    f.line([(31, 25), (35, 26), (37, 25)], "cr_l")
    key = {"k": "ink", "H": "hair_d", "h": "hair_l", "L": "skin_l",
           "M": "skin_m", "D": "skin_d", "b": "lea", "W": "lin_l"}
    f.patch(22, 4, [
        "......k..k......",
        "...k.kHkkHk.k...",
        "..kHkHHhHHHkHk..",
        ".kHhhHHHHhHHHk..",
        "..kHHhHHHHHHHhk.",
        ".kHHHHHHHHHHHHk.",
        ".kHHLLHHLLLHHHk.",
        "..kLLkLLLLkkHHk.",
        "..kLkWkLLLkWMDk.",
        "..kLkkkLLLkkMDk.",
        "...kLLLLLLLMMbk.",
        "...kLLLMLLMMbk..",
        "....kLLkWWkMb...",
        ".....kLLLMMb....",
        "......kLMMb.....",
        ".......bbb......",
    ], key)
    f.patch(22, 33, [".bbbb.", "bLLLLb", "bLMLMb", ".bMMb."], key)
    f.patch(41, 21, [".bbb.", "bLLMb", "bLMMb", ".bbb."], key)
    f.patch(41, 16, [".kkkk.", "kRRCCk", "kkWkkk", "kWWwwk", ".kwwk."],
            {"k": "ink", "R": "cr_l", "C": "cr_m", "W": "lin_l", "w": "lin_d"})
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
    f.poly([(24, 20), (40, 20), (43, 28), (45, 40), (42, 47), (22, 47), (19, 40), (21, 28)], veil)
    # peplos, floor length, gold girdle and hem
    robe_id = f.poly([(25, 22), (37, 22), (40, 30), (41, 40), (43, 52), (45, 60), (17, 60), (19, 52),
                      (21, 40), (22, 30)], robe)
    f.rect(16, 56, 46, 57, gold, clip=robe_id, noline=True)
    f.rect(16, 38, 46, 39, gold, clip=robe_id, noline=True)
    for x in (24, 29, 34, 39):  # long vertical folds
        f.shade_poly([(x, 41), (x + 1, 41), (x + 1 + (x - 31) // 5, 55), (x + (x - 31) // 5, 55)], 0.45)
    f.shade_poly([(26, 41), (27, 41), (26, 55), (25, 55)], -0.35)
    # sandal toes peeking out
    f.poly([(23, 60), (28, 60), (28, 62), (23, 62)], Mat(["lea"]))
    f.poly([(34, 60), (39, 60), (39, 62), (34, 62)], Mat(["lea"]))
    # neck
    f.rect(30, 20, 34, 25, skin, group=400)
    # veil panels falling over the shoulders
    f.poly([(26, 20), (29, 21), (28, 27), (25, 34), (21, 33), (22, 26)], veil, group=500)
    f.poly([(35, 21), (38, 20), (42, 26), (43, 33), (39, 34), (36, 27)], veil, group=501)
    # forearms bringing the lamp to her chest
    f.thick_line([(23, 34), (28, 31)], 3, skin, group=600)
    f.thick_line([(41, 34), (36, 31)], 3, skin, group=601)
    # the bronze oil lamp: body, nozzle, ring handle
    f.ellipse((26, 29, 38, 35), gold, group=700)
    f.poly([(36, 29), (42, 27), (43, 29), (37, 33)], gold, group=700)
    f.ellipse((22, 29, 27, 34), gold, group=701)
    f.ellipse((24, 31, 25, 32), gold, erase=True)
    # hands cupping the lamp
    f.ellipse((26, 31, 29, 34), skin, group=602)
    f.ellipse((35, 31, 38, 34), skin, group=603)
    f.line([(30, 29), (34, 29)], "gold_l")
    f.pxs([(29, 30), (30, 31), (31, 31)], "gold_l")
    f.line([(30, 34), (34, 34)], "gold_d")
    # flame on the nozzle
    f.patch(40, 20, [
        "..k...",
        ".kRk..",
        ".kRRk.",
        "kRGRk.",
        "kGWGRk",
        "kGWWGk",
        ".kGGk.",
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

def titan_grunt():
    pal = Palette([
        ("ink", INK),
        ("skin_l", (240, 192, 152)), ("skin_m", (208, 144, 104)), ("skin_d", (152, 96, 64)),
        ("br_l", (248, 224, 136)), ("br_m", (216, 160, 64)), ("br_d", (152, 96, 40)), ("br_x", (88, 56, 32)),
        ("tu_l", (104, 96, 128)), ("tu_m", (64, 56, 88)), ("tu_d", (40, 32, 56)),
        ("crest_l", (184, 48, 48)), ("crest_d", (104, 24, 40)),
        ("lea", (96, 56, 40)),
    ])
    skin = Mat(["skin_d", "skin_m", "skin_l"], outline="lea", cuts=[0.5, 0.86])
    tunic = Mat(["tu_d", "tu_m", "tu_l"], wx=0.85, wy=0.15, cuts=[0.18, 0.6])
    bronze = Mat(["br_x", "br_d", "br_m", "br_l"], cuts=[0.12, 0.42, 0.74])
    lea = Mat(["lea"])
    f = Fig(pal)
    # legs in a low, wide crouch, weight on the back (left) leg, front knee bent
    f.poly([(23, 40), (29, 40), (27, 47), (22, 52), (20, 57), (16, 57), (18, 51), (21, 46)], tunic, group=100)
    f.poly([(32, 40), (38, 40), (41, 47), (44, 52), (45, 57), (41, 57), (39, 52), (35, 46)], tunic, group=101)
    f.poly([(14, 57), (21, 57), (21, 61), (13, 61)], lea)
    f.poly([(40, 57), (47, 57), (48, 61), (40, 61)], lea)
    f.poly([(18, 50), (23, 50), (21, 56), (16, 56)], bronze)
    f.poly([(39, 50), (43, 50), (45, 56), (41, 56)], bronze)
    # dark tunic, hunched forward, short pleated skirt
    body = f.poly([(23, 22), (39, 21), (41, 30), (43, 42), (31, 44), (19, 42), (22, 30)], tunic)
    f.rect(19, 31, 43, 32, lea, clip=body)
    for x in (24, 29, 34, 39):
        f.shade_poly([(x, 34), (x + 1, 34), (x + 1 + (x - 31) // 6, 43), (x + (x - 31) // 6, 43)], 0.5)
    f.shade_poly([(36, 22), (39, 22), (41, 30), (38, 30)], 0.35)
    # bronze shoulder guard on the near shoulder
    f.ellipse((19, 20, 27, 26), bronze, group=150)
    # near arm hangs low, gripping a bronze sickle
    f.thick_line([(22, 24), (18, 33)], 4, skin, group=200)
    f.ellipse((15, 32, 20, 37), skin, group=201)
    f.thick_line([(17, 36), (15, 43)], 2, lea, group=210)
    f.patch(8, 41, [
        "..kkkk...",
        ".kGYYyk..",
        "kGk..kyk.",
        "kYk...kk.",
        "kYk......",
        ".kYk.....",
        "..kYkk...",
        "...kkk...",
    ], {"k": "ink", "G": "br_l", "Y": "br_m", "y": "br_d"})
    # far arm cocked, fist raised at his chest
    f.thick_line([(38, 23), (44, 31)], 4, skin, group=300)
    f.thick_line([(44, 31), (39, 30)], 4, skin, group=300)
    f.ellipse((35, 27, 40, 32), skin, group=301)
    f.rect(28, 19, 33, 23, skin, group=400)
    # sickle emblem on the chest
    f.patch(27, 23, [
        "..YY..",
        ".Y..Y.",
        "Y...Y.",
        "Y.....",
        ".YYY..",
    ], {"Y": "br_l"})
    # low Corinthian helmet: swept-back crest, T-shaped face opening, glowing eyes
    f.patch(21, 6, [
        "......kkkkkk......",
        "..kkkRRRRRRCCkk...",
        ".kRRRCCCCCCCCCCck.",
        "kCCkkkkkkkkkkkkkkk",
        "..kGGYYYYYYYYyyk..",
        ".kGYYYYYYYYYYYyyk.",
        ".kGYYYYYYYYYYYYyk.",
        ".kGkkkkkkkkkkkkyk.",
        ".kGkRkkkkkkRkkkyk.",
        ".kGYYYYkkkYYYYyyk.",
        ".kYYyYYkLkYYyyyyk.",
        "..kYyyYkLkYyyyyk..",
        "..kyyyykLkyyyyk...",
        "...kkkkkkkkkkk....",
    ], {"k": "ink", "C": "crest_d", "c": "crest_d", "R": "crest_l", "G": "br_l", "Y": "br_m", "y": "br_d",
        "L": "skin_d"})
    f.pxs([(24, 11), (25, 11)], "br_l")
    return f, pal


def professor_daphne():
    pal = Palette([
        ("ink", INK),
        ("skin_l", (248, 216, 184)), ("skin_m", (224, 168, 128)), ("skin_d", (176, 112, 80)),
        ("hair_l", (176, 96, 56)), ("hair_d", (112, 56, 40)),
        ("leaf_l", (144, 160, 72)), ("leaf_d", (96, 112, 48)),
        ("him_l", (248, 248, 240)), ("him_m", (216, 208, 192)), ("him_d", (168, 160, 152)),
        ("blue_l", (48, 104, 176)), ("blue_d", (24, 56, 120)),
        ("par_l", (232, 216, 176)), ("par_d", (176, 144, 96)),
    ])
    skin = Mat(["skin_d", "skin_m", "skin_l"], outline="hair_d", cuts=[0.5, 0.86])
    him = Mat(["him_d", "him_m", "him_l"], wx=0.85, wy=0.15, cuts=[0.25, 0.65])
    chiton = Mat(["blue_d", "blue_l"], cuts=[0.6])
    par = Mat(["par_d", "par_l"], cuts=[0.6])
    f = Fig(pal)
    # blue chiton, floor length
    f.poly([(27, 23), (37, 24), (38, 37), (43, 58), (39, 60),
            (32, 59), (28, 61), (20, 60), (23, 45), (24, 34)], chiton)
    f.poly([(22, 60), (27, 60), (27, 62), (22, 62)], Mat(["hair_d"]))
    f.poly([(34, 60), (39, 60), (39, 62), (34, 62)], Mat(["hair_d"]))
    # himation wrapped diagonally from her left shoulder to the knees
    f.poly([(33, 23), (38, 24), (41, 33), (42, 44), (39, 53),
            (34, 54), (25, 49), (21, 44), (26, 37), (32, 31)], him)
    for a, b in (((36, 29), (28, 40)), ((38, 34), (26, 45)), ((39, 40), (34, 51))):
        f.line([a, b], "him_d")
    f.shade_poly([(35, 29), (37, 31), (26, 42), (24, 42)], -0.4)
    f.line([(23, 46), (34, 53)], "him_m")
    f.line([(27, 54), (25, 59)], "blue_d")
    f.line([(35, 54), (38, 58)], "blue_l")
    # right arm out in a welcoming gesture
    f.thick_line([(25, 25), (20, 32)], 4, chiton, group=200)
    f.thick_line([(20, 32), (16, 24)], 3, skin, group=201)
    # index finger raised: a teacher making a point
    f.patch(13, 16, [
        ".k...",
        "kLk..",
        "kLk..",
        "kLkkk",
        "kLLLk",
        "kLLMk",
        ".kkk.",
    ], {"k": "hair_d", "L": "skin_l", "M": "skin_m"})
    # left arm hugging a scroll
    f.thick_line([(38, 25), (41, 33)], 4, him, group=300)
    f.poly([(35, 30), (44, 34), (42, 38), (33, 34)], par, group=310)
    f.ellipse((32, 32, 36, 37), par, group=311)
    f.poly([(41, 36), (45, 36), (46, 47), (42, 48)], par, group=313)
    f.line([(42, 39), (44, 39)], "par_d")
    f.line([(43, 42), (45, 42)], "par_d")
    f.line([(43, 45), (44, 45)], "par_d")
    f.ellipse((38, 33, 42, 37), skin, group=312)
    f.rect(30, 20, 34, 25, skin, group=400)
    # head: chestnut hair in a bun, laurel wreath
    f.patch(23, 3, [
        "..........kkk...",
        ".........kHhhk..",
        ".......kkHHHHk..",
        "....kkGgGkkGgk..",
        "...kGhhhhhhHggk.",
        "..kghhHHHHhhhGk.",
        "..kHhHLLLLLhhhHk",
        "..kHhLLLLLLLhhHk",
        "..kHLkkLLLkkLHHk",
        "..kHLkWLLLkWMHHk",
        "..kHLLkLLLkMMHHk",
        "...HLLLLLLLMMHHk",
        "...HLLLMMLMMMHHk",
        "...HHLLLkWkMDHk.",
        "....HHLLLMMMHHk.",
        ".....HHLLMMHHk..",
        "......kHMMHk....",
        ".......kkkk.....",
    ], {"k": "ink", "H": "hair_d", "h": "hair_l", "G": "leaf_l", "g": "leaf_d", "L": "skin_l",
        "M": "skin_m", "D": "skin_d", "d": "skin_d", "b": "hair_d", "W": "him_l"})
    return f, pal


CAST = {
    "kleon": kleon,
    "hierophant_ione": hierophant_ione,
    "titan_grunt": titan_grunt,
    "professor_daphne": professor_daphne,
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
            if name == "professor_daphne":
                save_indexed(arr, pal, os.path.join(ROOT, "graphics/birch_speech/birch.png"))
    if pv:
        os.makedirs(pv, exist_ok=True)
        preview(figs, os.path.join(pv, "trainers.png"))
        for name, (arr, pal) in figs.items():
            upscale(to_rgba(arr, pal), 6).save(os.path.join(pv, name + ".png"))
            grid_preview(to_rgba(arr, pal), 12, 8, 0, 56, 64).save(os.path.join(pv, name + "_grid.png"))


if __name__ == "__main__":
    main()
