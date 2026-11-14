"""Player battle pics: Theo and Ianthe, "the Unwoven" (they replace Brendan and May).

Usage: python3 tools/ichor/art/sprites_player.py [--write] [--preview DIR]

--write   writes the front pics (64x64), the back pics (64x256, four frames)
          and the shared palettes:
            graphics/trainers/front_pics/{brendan,may}.png
            graphics/trainers/back_pics/{brendan,may}.png
            graphics/trainers/palettes/{brendan,may}.pal
--preview writes the review sheets to DIR: the fronts beside Kleon and Ione
          on a battle backdrop, the four back frames in order, and pixel grids.

The spec, shared with the overworld sprites:
  * a wide-brimmed petasos in sun-gold straw
  * an Aegean-blue chlamys pinned at the right shoulder (it covers the left
    arm and leaves the right arm free)
  * a cream chiton: knee length on Theo, a little longer on Ianthe
  * brown laced sandals and a small terracotta satchel on a strap
  * Theo: short black hair. Ianthe: dark-brown hair in a low braid
  * an eager, ready-to-travel stance, holding a Poke Ball

Front and back pics share one palette, so both use the index layout in
`palette()`. Back frames: 0 holding the ball, 1 wind-up, 2 release,
3 empty-handed rest (sAnimCmd_Hoenn plays 0, 1, 2, 0, 3).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import (ROOT, Palette, Mat, Fig, save_indexed, to_rgba, battle_bg,  # noqa: E402
                         upscale, palette_report, grid_preview)
from PIL import Image, ImageDraw  # noqa: E402

INK = (32, 24, 24)

VARIANTS = {
    "brendan": dict(name="Theo", girl=False, hair_l=(72, 72, 104)),
    "may": dict(name="Ianthe", girl=True, hair_l=(152, 96, 64)),
}


def palette(v):
    """One index layout for both characters and for front and back.

    Only hair_l differs: Theo's black hair is ink with a slate sheen, and
    Ianthe's dark-brown hair is the leather brown with a warm highlight.
    """
    return Palette([
        ("ink", INK),
        ("skin_l", (248, 208, 168)), ("skin_m", (224, 160, 112)), ("skin_d", (168, 104, 72)),
        ("brown", (96, 56, 40)),
        ("hair_l", v["hair_l"]),
        ("blue_d", (24, 56, 120)), ("blue_m", (48, 104, 176)), ("blue_l", (112, 168, 224)),
        ("gold_d", (152, 96, 32)), ("gold_m", (208, 152, 48)), ("gold_l", (240, 200, 88)),
        ("cream_d", (200, 176, 136)), ("cream_l", (248, 240, 216)),
        ("terra", (192, 80, 48)),
    ])


def mats():
    return dict(
        skin=Mat(["skin_d", "skin_m", "skin_l"], outline="ink", line="skin_d", cuts=[0.52, 0.86]),
        cloak=Mat(["blue_d", "blue_m", "blue_l"], wx=0.85, wy=0.2, cuts=[0.3, 0.72]),
        gold=Mat(["gold_d", "gold_m", "gold_l"], wx=0.7, wy=0.4, cuts=[0.3, 0.7]),
        cream=Mat(["cream_d", "cream_l"], wx=0.85, wy=0.2, cuts=[0.62]),
        lea=Mat(["brown"]),
        terra=Mat(["brown", "terra"], cuts=[0.7]),
    )


BALL = [
    ".kkkk.",
    "kRRRrk",
    "kkWkkk",
    "kWWWck",
    ".kcck.",
]
BALL_KEY = {"k": "ink", "R": "terra", "r": "brown", "W": "cream_l", "w": "cream_d", "c": "cream_d"}

KEY = {"k": "ink", "G": "gold_l", "M": "gold_m", "D": "gold_d", "b": "brown",
       "h": "hair_l", "L": "skin_l", "S": "skin_m", "d": "skin_d", "W": "cream_l", "w": "cream_d",
       "B": "blue_l", "U": "blue_m", "N": "blue_d", "T": "terra", "_": "_"}


# --------------------------------------------------------------------------
# Front pic: 3/4 view facing left, ball held out toward the opponent
# --------------------------------------------------------------------------

def front(key):
    v = VARIANTS[key]
    pal = palette(v)
    m = mats()
    f = Fig(pal)
    girl = v["girl"]
    hem = 49 if girl else 46

    # cloak: the back of it billows out to the right
    f.poly([(31, 24), (39, 24), (45, 29), (49, 36), (53, 44), (55, 50), (51, 50), (48, 53), (45, 49),
            (41, 51), (39, 44), (36, 30)], m["cloak"])
    f.shade_poly([(46, 37), (47, 37), (51, 50), (49, 50)], 0.5)
    f.shade_poly([(43, 42), (44, 42), (45, 50), (44, 50)], 0.45)
    # legs
    f.poly([(23, hem - 1), (28, hem - 1), (27, 51), (26, 56), (22, 56), (22, 51)], m["skin"], group=100)
    f.poly([(32, hem - 1), (37, hem - 1), (37, 51), (37, 56), (33, 56), (32, 51)], m["skin"], group=101)
    # chiton: torso, belt, skirt
    tun = f.poly([(22, 26), (36, 26), (37, 35), (39, hem), (30, hem + 1), (21, hem), (22, 35)], m["cream"])
    f.rect(18, 35, 42, 36, m["lea"], clip=tun)
    f.shade_poly([(34, 37), (40, 37), (40, hem + 1), (35, hem + 1)], 0.35)
    # folds fanning from the belt, notches where they meet the hem, and the
    # blousing (kolpos) over the belt
    for (xa, xb) in ((25, 24), (29, 29), (33, 34)):
        f.line([(xa, 38), (xb, hem - 1)], "cream_d")
        f.px(xb, hem, "ink")
    f.line([(23, 34), (34, 34)], "cream_d")
    # cloak drape: across the chest from the fibula, over the near arm
    f.poly([(22, 26), (30, 24), (38, 24), (42, 28), (44, 34), (44, 41), (40, 42), (38, 36), (36, 30),
            (29, 31), (23, 30)], m["cloak"], group=250)
    f.shade_poly([(39, 33), (40, 33), (41, 41), (40, 41)], 0.45)
    # satchel on the near hip below the drape, strap across the chest
    f.line([(24, 30), (34, 39)], "brown")
    f.patch(34, 38, [".kkkkk.", "kbbbbbk", "kbbGbbk", "kTkkkTk", "kTTTTTk", "kTTTTbk", ".kkkkk."], KEY)
    # far (right) arm: Theo holds the ball out toward the opponent,
    # Ianthe raises it beside her shoulder
    if girl:
        f.thick_line([(21, 30), (16, 34)], 5, m["skin"], group=400)
        f.thick_line([(16, 34), (13, 27)], 4, m["skin"], group=400)
        ball, fingers = (9, 20), (11, 23)
    else:
        f.thick_line([(21, 30), (16, 31)], 5, m["skin"], group=400)
        f.thick_line([(16, 31), (11, 28)], 4, m["skin"], group=400)
        ball, fingers = (5, 23), (9, 25)
    f.poly([(19, 26), (24, 26), (24, 31), (19, 32)], m["cream"], group=401)
    # neck
    f.rect(26, 22, 30, 26, m["skin"], group=500)
    # fibula pinning the chlamys at the right shoulder
    f.patch(21, 25, [".k.", "kGk", ".k."], KEY)
    # ball in the hand, fingers curled over it
    f.patch(ball[0], ball[1], BALL, BALL_KEY)
    f.patch(fingers[0], fingers[1], ["..kk.", ".kLLk", "kLLSk", "kSLk.", ".kk.."], KEY)
    # sandals with laces up the shin
    for x0 in (19, 32):
        f.patch(x0, 51, [
            "...k.k..",
            "...bLb..",
            "...LbL..",
            "..kbLbk.",
            "..kLbLk.",
            ".kLbLLLk",
            "kLLbLLLk",
            "kbbbbbbk",
            ".kkkkkk.",
        ], KEY)
    # head under the petasos
    f.patch(15, 1, HAT_FRONT + HEAD_FRONT[key], KEY)
    if girl:
        # the low braid brought forward over the near shoulder
        f.patch(32, 20, [".kbk.", "kbhbk", "khbbk", "kkbkk", "kbbhk", "kbhbk", "kkbkk", "kbhbk", "khbbk",
                         "kkbkk", "kbbhk", "kGGMk", ".kbk.", "..k.."], KEY)
    return f, pal


HAT_FRONT = [
    "............kkkkkk...........",
    "..........kkGGGGMMkk.........",
    ".........kGGGGGMMMMMk........",
    "........kGGGGGMMMMMMDk.......",
    "........kbbbbbbbbbbbbk.......",
    "....kkkkGGMMMMMMMMMMMDkkkk...",
    "..kkGGGGGGGGMMMMMMMMMMMMDDkk.",
    ".kGGGGGGGGGMMMMMMMMMMMMMMDDDk",
    "kDGGGGGMMMMMMMMMMMMMMMMMDDDDk",
    "kkDDDDDDDDDDDDDDDDDDDDDDDDkkk",
    "..kkkkkkkkkkkkkkkkkkkkkkkk...",
]


HEAD_FRONT = {
    "brendan": [
        "....kkkkhkkkkkkkhkkhkk.......",
        "....kSkkSSkkSSSkkkhhk........",
        "....kSSSSSSSSSSSSkkhk........",
        "....kLkkLLLkkLLSdkhk.........",
        "....kLkWLLLkWLLSSdSk.........",
        "....kLkkLLLkkLLSSdSk.........",
        "....kLLLLdLLLLSSSdk..........",
        ".....kLLLLLLdSSSdk...........",
        ".....kLLLkkSSSSdk............",
        "......bLLLLSSSdb.............",
        ".......bbLSSSdb..............",
        ".........bbbbb...............",
    ],
    "may": [
        "...kkbbhbbbbbbbhbbbbkk.......",
        "...kbhbbSSbbbSSSbbbbhbk......",
        "...kbbSSSSSSSSSSSSbbhbk......",
        "...kbkkkLLLkkkLSdbbhbbk......",
        "...kbLkWLLLkWLLSSdbbhbk......",
        "...kbLkkLLLkkLLSSdbbbk.......",
        "...kbLLLLdLLLLSSSdbbk........",
        "...kbbLLLLLLdSSSdbbk.........",
        "....kbLLLkkSSSSdbbk..........",
        "....kbbLLLLSSSdbk............",
        ".....kkbbLSSSdbk.............",
        "......kk.bbbbbk..............",
    ],
}


# --------------------------------------------------------------------------
# Back pic: from behind, facing right, cropped at the waist.
# Frames: 0 holding the ball, 1 wind-up, 2 release, 3 empty-handed rest.
# --------------------------------------------------------------------------

# throwing arm (the near, left arm): shoulder, elbow, wrist per frame
ARM = {
    0: [(14, 47), (7, 56), (8, 46)],
    1: [(16, 45), (7, 36), (9, 26)],
    2: [(23, 47), (38, 43), (50, 38)],
}

# the hand from behind, fingers curled around the ball
HAND_BALL = [
    "...kkkkk...",
    "..kRRRRrk..",
    ".kRRRRRRrk.",
    ".kRRRRRrrk.",
    ".kkkkWkkkk.",
    ".kWWWkwwwk.",
    "kLkWWWwwkSk",
    "kLLkkkkkLSk",
    "kLLLLLLLSSk",
    ".kLLLLLSSdk",
    ".kLLLLSSdk.",
    "..kLLSSdk..",
]
# the hand just after the release, fingers open toward the opponent
HAND_OPEN = [
    ".....kk.......",
    "...kkLLkkkk...",
    "..kLLLLLLLLkk.",
    ".kLLLLLLLLLLLk",
    "kLLLLLLSSSSkk.",
    "kSLLLSSkkkkk..",
    ".kSSSSk.......",
    "..kkkk........",
]

BRAID = ["kbhbk", "khbbk", "kkbkk", "kbbhk", "kbhbk", "kkbkk"]


def ell(f, box):
    return f._mask_from_draw(lambda d: d.ellipse(box, fill=255, outline=255))


def fold(f, p0, p1, w0, w1, delta):
    """A tapered shading stroke for cloth folds, w0 wide at p0, w1 at p1."""
    (x0, y0), (x1, y1) = p0, p1
    f.shade_poly([(x0, y0), (x0 + w0, y0), (x1 + w1, y1), (x1, y1)], delta)


def back(key, frame):
    v = VARIANTS[key]
    pal = palette(v)
    m = mats()
    f = Fig(pal)
    girl = v["girl"]
    dx = 2 if frame == 2 else 0  # lean into the throw

    # cloak over the back, pinned at the right shoulder
    f.poly([(28 + dx, 38), (22 + dx, 39), (16 + dx, 41), (12 + dx, 44), (9, 48), (7, 54), (5, 63),
            (59, 63), (58, 56), (56 + dx, 49), (54 + dx, 44), (50 + dx, 41), (45 + dx, 39), (39 + dx, 38)],
           m["cloak"], group=10)
    # folds radiate from the fibula; the left side hangs straight
    pin = (48 + dx, 42)
    fold(f, pin, (40, 63), 1, 4, 0.5)
    fold(f, (pin[0] + 1, pin[1] + 1), (50, 63), 1, 3, 0.45)
    fold(f, (pin[0] - 3, pin[1]), (28, 63), 1, 4, 0.4)
    fold(f, (pin[0] - 2, pin[1]), (36, 63), 1, 2, -0.35)
    fold(f, (19 + dx, 44), (15, 63), 1, 3, 0.4)
    fold(f, (24 + dx, 42), (22, 63), 1, 2, -0.3)
    # satchel strap from the left shoulder to the right hip, satchel peeking in
    f.thick_line([(20 + dx, 41), (35 + dx, 51), (52, 63)], 2, m["lea"], group=20)
    f.patch(45, 54, [
        "..kkkkkkkkk.",
        ".kbbbbbbbbbk",
        "kbbbbbGbbbbk",
        "kTkbbbbbbkTk",
        "kTTkkkkkkTTk",
        "kTTTTTTTTTTk",
        "kTTTTTTTTTTk",
        "kTTTTTTTTTTk",
        "kTTTTTTTTTbk",
        "kTTTTTTTTbbk",
    ], KEY)
    # neck
    f.rect(30 + dx, 31, 39 + dx, 40, m["skin"], group=30)
    # fibula on the right shoulder
    f.patch(46 + dx, 38, [".kkkk.", "kGGGMk", "kGMMDk", ".kkkk."], KEY)

    if frame in (0, 2):
        arm(f, m, frame)

    # head (back of the head, ear and cheek on the right), over the arm
    f.patch(20 + dx, 21, HEAD_BACK[key], KEY)
    if girl:
        rows = [".kbk."] + [BRAID[i % len(BRAID)] for i in range(16)] + ["kGGMk", "kGMDk", "kbhbk", ".kbk.", "..k.."]
        f.patch(28 + dx, 37, rows, KEY)
    out = f.render()

    # the petasos sits over the head; the wind-up arm is raised in front of it
    h = Fig(pal)
    hat(h, m, dx)
    out = layer(out, h.render())
    if frame == 1:
        a = Fig(pal)
        arm(a, m, frame)
        out = layer(out, a.render())
    return out, pal


def layer(base, top):
    return np.where(top > 0, top, base)


def arm(f, m, frame):
    sh, el, wr = ARM[frame]
    f.thick_line([sh, el], 8, m["skin"], group=40)
    f.thick_line([el, wr], 7, m["skin"], group=40)
    if frame in (0, 1):
        # the chiton's short sleeve over the shoulder
        sx, sy = sh[0] + (el[0] - sh[0]) * 0.35, sh[1] + (el[1] - sh[1]) * 0.35
        f.thick_line([(sh[0] + 1, sh[1] - 2), (round(sx), round(sy))], 9, m["cream"], group=41)
    else:
        # swung across the body, the arm comes out from under the cloak
        f.poly([(16, 42), (24, 40), (30, 43), (29, 50), (22, 52), (17, 49)], m["cloak"], group=41)
    if frame in (0, 1):
        f.patch(wr[0] - 5, wr[1] - 11, HAND_BALL, dict(KEY, R="terra", r="brown", w="cream_d"))
    else:
        f.patch(wr[0] - 1, wr[1] - 5, HAND_OPEN, KEY)


def hat(f, m, dx):
    """The petasos from behind and a little above: wide brim, low crown."""
    rows = np.arange(64)[:, None]
    brim = ell(f, (13 + dx, 12, 53 + dx, 25))
    f.add(brim, m["gold"], group=60)
    rim = brim & ~ell(f, (13 + dx, 11, 53 + dx, 24))
    f.add(rim, Mat(["gold_d"]), group=60, nooutline=True)
    crown = (ell(f, (25 + dx, 7, 41 + dx, 23)) & (rows <= 15)) | ell(f, (25 + dx, 12, 41 + dx, 19))
    f.add(crown, m["gold"], group=61)
    band = f._mask_from_draw(lambda d: d.arc((25 + dx, 11, 41 + dx, 19), 0, 180, fill=255, width=2))
    band &= crown
    f.add(band, Mat(["brown"]), group=61, nooutline=True)


HEAD_BACK = {
    "brendan": [
        "...kkkkkkkkkkkkkkkkkkkkk....",
        "..kkkkkkkkkkkkkkkkkkkkkkk...",
        ".kkkkhkkkkkkkkkkkkkkkkkdSk..",
        ".kkkhhkkkkkkkkkkkkkkkkdSSSk.",
        "kkkhhkkkkkkkkkkkkkkkkdSSSSk.",
        "kkkhkkkkkkkkkkkkkkkkkSLLLSSk",
        "kkkkkkkkkkkkkkkSSkkkSLLLLLkk",
        "kkhkkkkkkkkkkkSddSkkLLLLLLWk",
        "kkhkkkkkkkkkkkSdSSkSLLLLLLSk",
        "kkkkkkkkkkkkkkSddSkSSLLLLSk.",
        ".kkkkkkkkkkkkkkSSkSSSLLLSSk.",
        ".kkkkkkkkkkkkkkkkkSSSLLSSSk.",
        "..kkkkkkkkkkkkkkkdSSSSSSdk..",
        "...kkkkkkkkkkkkkkdSSSSSdk...",
        "....kkkkkkkkkkkkddSSSddk....",
        ".....kkkkkkkkkkddSSddkk.....",
        "......kkkkkkkkdddSSSk.......",
        ".........kkkkddSSSSk........",
    ],
    "may": [
        "...kkkkkkkkkkkkkkkkkkkkk....",
        "..kbbbbbbbbbbbbbbbbbbbbbk...",
        ".kbbhhbbbbbbbbbbbbbbbbbdSk..",
        ".kbhhbbbbbhhbbbbbbbbbbdSSSk.",
        "kbbhbbbbhhbbbbbbbbbbbdSSSSk.",
        "kbhbbbbhbbbbbbbbbbbbkSLLLSSk",
        "kbhbbbbhbbbbbbbbSSbbkSLLLLkk",
        "kbbbbbhbbbbbbbbSddSbbLLLLLWk",
        "kbbbbbhbbbbbbbbSdSSbSLLLLLSk",
        "kkbbbbbbbbbbbbbSddSbSSLLLSk.",
        ".kbbbbbhbbbbbbbbSSbSSSLLSSk.",
        ".kkbbbbbbhbbbbbbbbbSSSLSSSk.",
        "..kkbbbbbbbbbbbbbbdSSSSSdk..",
        "...kkbbbbbbbbbbbbkdSSSSdk...",
        "....kkkbbbbbbbkkddSSSddk....",
        ".....kkkbbbbbkkddSSddkk.....",
        "......kkkbbbkdddSSSk........",
        ".........kkkddSSSSk.........",
    ],
}


def build(key):
    ff, pal = front(key)
    fr = ff.render()
    frames = []
    for i in range(4):
        frames.append(back(key, i)[0])
    return pal, fr, np.vstack(frames)


def battle_tile(im):
    tile = battle_bg().crop((240 - 96, 40, 240, 112)).copy()
    tile.alpha_composite(im, (16, 4))
    return tile


def preview(built, pv):
    os.makedirs(pv, exist_ok=True)
    tiles = []
    refs = [("kleon", "graphics/trainers/front_pics/kleon.png"),
            ("hierophant_ione", "graphics/trainers/front_pics/hierophant_ione.png")]
    tiles.append(battle_tile(Image.open(os.path.join(ROOT, refs[0][1])).convert("RGBA")))
    for key in ("brendan", "may"):
        pal, fr, _ = built[key]
        tiles.append(battle_tile(to_rgba(fr, pal)))
    tiles.append(battle_tile(Image.open(os.path.join(ROOT, refs[1][1])).convert("RGBA")))
    sheet = Image.new("RGBA", (96 * len(tiles), 72))
    for i, t in enumerate(tiles):
        sheet.alpha_composite(t, (96 * i, 0))
    upscale(sheet, 3).save(os.path.join(pv, "front.png"))
    for key in ("brendan", "may"):
        pal, fr, bk = built[key]
        grid_preview(to_rgba(fr, pal), 12, 4, 0, 60, 64).save(os.path.join(pv, key + "_front_grid.png"))
        grid_preview(to_rgba(fr, pal), 20, 12, 0, 46, 28).save(os.path.join(pv, key + "_head_grid.png"))
        for i in range(4):
            grid_preview(to_rgba(bk[64 * i:64 * i + 64], pal), 10, 0, 0, 64, 64).save(
                os.path.join(pv, "%s_back%d_grid.png" % (key, i)))
    # back frames in sequence, on the battle backdrop
    rows = []
    for key in ("brendan", "may"):
        pal, fr, bk = built[key]
        bg = battle_bg(64 * 4 + 12, 72)
        for i in range(4):
            bg.alpha_composite(to_rgba(bk[64 * i:64 * i + 64], pal), (4 + 64 * i, 8))
        rows.append(bg)
    sheet = Image.new("RGBA", (rows[0].width, 72 * len(rows)))
    for j, r in enumerate(rows):
        sheet.alpha_composite(r, (0, 72 * j))
    upscale(sheet, 3).save(os.path.join(pv, "back.png"))


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    built = {}
    for key in ("brendan", "may"):
        pal, fr, bk = build(key)
        palette_report(np.vstack([fr, bk]), pal, key)
        built[key] = (pal, fr, bk)
        if "--write" in args:
            save_indexed(fr, pal, os.path.join(ROOT, "graphics/trainers/front_pics", key + ".png"))
            save_indexed(bk, pal, os.path.join(ROOT, "graphics/trainers/back_pics", key + ".png"))
            pal.write_jasc(os.path.join(ROOT, "graphics/trainers/palettes", key + ".pal"))
    if pv:
        preview(built, pv)


if __name__ == "__main__":
    main()
