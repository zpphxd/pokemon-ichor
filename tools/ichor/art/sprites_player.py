"""Historical player battle painter and shared named-cast drawing helpers.

Canonical player PNGs are checked by player_sources.py --check. The legacy
--write command is rejected; reference previews do not reproduce the new art.

Usage: python3 tools/ichor/art/sprites_player.py [--write] [--preview DIR] [--grids DIR]

--write   retired; rejects protected player PNG/palette writes
--preview writes the 3x review sheets to DIR (design/phase1/img for the
          committed ones): sprites_player_battle.png, the fronts beside Kleon
          and Ione on a battle backdrop, and sprites_player_battle_back.png,
          the four back frames in order.
--grids   writes upscaled pixel grids with coordinates to DIR.

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
from PIL import Image  # noqa: E402
import player_sources  # noqa: E402

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
    hem = 46 if girl else 43

    f.poly([(31, 22), (39, 25), (43, 29), (50, 33), (57, 42), (60, 46),
            (57, 46), (56, 50), (51, 47), (46, 51), (41, 48), (34, 47), (27, 44)], m["cloak"])
    f.poly([(25, 26), (22, 31), (20, 39), (17, 43), (19, 45), (25, 40), (28, 28)], m["cloak"])
    for a, b, delta in (((39, 28), (48, 47), 0.5), ((43, 31), (55, 46), 0.4),
                        ((36, 29), (41, 46), -0.35)):
        fold(f, a, b, 1, 2, delta)
    # Weight is on the far leg; the near knee bends into the next step.
    f.poly([(24, hem - 2), (29, hem - 1), (27, 49), (23, 53), (21, 57),
            (17, 57), (19, 51), (22, 48)], m["skin"], group=100)
    f.poly([(32, hem - 2), (37, hem - 1), (36, 49), (39, 55), (39, 57),
            (35, 58), (32, 52), (31, 48)], m["skin"], group=101)
    tun = f.poly([(25, 24), (34, 23), (37, 29), (35, 34), (36, 38),
                  (40, hem), (36, hem + 1), (32, hem), (28, hem + 2),
                  (23, hem), (20, hem - 1), (24, 34), (22, 29)], m["cream"])
    f.rect(20, 33, 39, 34, m["lea"], clip=tun)
    f.patch(28, 33, ["GM", "DM"], KEY)
    for a, b in (((25, 35), (23, hem - 1)), ((29, 36), (29, hem)),
                 ((32, 35), (35, hem))):
        fold(f, a, b, 1, 2, 0.45)
    f.line([(25, 31), (28, 32), (33, 31)], "cream_d")
    f.poly([(24, 23), (29, 21), (35, 22), (40, 25), (39, 29),
            (34, 28), (30, 26), (25, 27), (21, 25)], m["cloak"], group=250)
    f.line([(26, 24), (30, 24), (34, 26), (37, 26)], "blue_l")
    f.line([(25, 27), (34, 37)], "brown")
    f.patch(34, 35, [".kkkkk.", "kTTTTbk", "kTbGbbk", "kTkkkTk",
                     "kTTTTTk", "kTTTTbk", ".kkkkk."], KEY)
    if girl:
        f.thick_line([(23, 27), (17, 31), (14, 23)], 4, m["skin"], group=400)
        ball, fingers = (10, 16), (12, 20)
        f.thick_line([(36, 28), (39, 33), (35, 34)], 4, m["skin"], group=410)
        f.patch(33, 32, [".kkk.", "kLLSk", "kSSSk", ".kkk."], KEY)
    else:
        f.thick_line([(23, 27), (17, 26), (10, 24)], 4, m["skin"], group=400)
        ball, fingers = (4, 19), (8, 22)
    f.poly([(21, 25), (25, 26), (24, 30), (20, 29)], m["cream"], group=401)
    f.rect(28, 20, 31, 24, m["skin"], group=500)
    f.patch(25, 23, [".k.", "kGk", ".k."], KEY)
    f.patch(ball[0], ball[1], BALL, BALL_KEY)
    f.patch(fingers[0], fingers[1], [".kk.", "kLLk", "kSSk", ".kk."], KEY)
    for x, y in ((16, 52), (34, 53)):
        f.patch(x, y, ["...bLb.", "...LbL.", "..kbLbk", "..kLbLk",
                       ".kLbLLk", "kLLbLLk", "kbbbbbk", ".kkkkk."], KEY)
    f.patch(23, 11, HEAD_FRONT[key], KEY)
    if girl:
        f.patch(35, 17, [".kbk.", "kbhbk", "khbbk", "kbbhk", "kbhbk",
                        "kkbkk", "kbbhk", "kGGMk", ".kbk."], KEY)
    f.patch(15, 2, HAT_FRONT, KEY)
    return f, pal


HAT_FRONT = [
    "............kkkkk............",
    "..........kkGGGMMkk..........",
    ".........kGGGGMMMMMk.........",
    "........kGGGGMMMMMMDk........",
    ".......kGGGMMMMMMMMDk........",
    "....kkkbbbbbbbbbbbbbbkkk.....",
    "..kkGGGGGGMMMMMMMMMMMDDDkk...",
    ".kGGGGGGMMMMMMMMMMMMMDDDDk...",
    "..kkDDDDDDDDDDDDDDDDDDDkk....",
    "....kkkkkkkkkkkkkkkkkkk......",
]


HEAD_FRONT = {
    "brendan": [
        ".kkhkkkkkhkkk..",
        "khkkkLkkkLkhhk.",
        "kkLSSLLLSSkkhk.",
        "kLLLkLLLkkLSdk.",
        "kLLkWkLLkWLSdk.",
        "kLLkkkLLkkLSdk.",
        ".kLLLLLLLLLSdk.",
        ".kLLSLLLSSSSk..",
        "..kLLkkWkSSk...",
        "...kLLLSSSk....",
        "....kLSSSk.....",
        ".....kkkk......",
    ],
    "may": [
        ".kbhbbbbhbbkk..",
        "kbhbbLbbbLbhbk.",
        "kbbSSLLLSSbbbk.",
        "kbLLkLLLkkLbdk.",
        "kbLkWkLLkWLbdk.",
        "kbLkkkLLkkLbdk.",
        ".bLLLLLLLLLbdk.",
        ".kbLSLLLSSSbk..",
        "..bLLkkWkSSbk..",
        "...bLLLSSSbk...",
        "....bLSSSbk....",
        ".....kkkk......",
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
SHOULDER_FLAP = {
    0: [(10, 43), (19, 39), (22, 45), (18, 51), (12, 52), (8, 49)],
    1: [(11, 43), (20, 39), (23, 45), (19, 50), (13, 50), (9, 47)],
    2: [(16, 42), (24, 40), (30, 43), (29, 50), (22, 52), (17, 49)],
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
    # fibula on the right shoulder (behind the arm on the release)
    if frame != 2:
        f.patch(46, 38, [".kkkk.", "kGGGMk", "kGMMDk", ".kkkk."], KEY)

    if frame in (0, 2):
        arm(f, m, frame)

    # head (back of the head, ear and cheek on the right), over the arm
    f.patch(20 + dx, 21, HEAD_BACK[key], KEY)
    f.patch(44 + dx, 27, ["kLL.", "kWk.", "kkLk", "LSSk", "LSSk", "SSk."], KEY)
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
    # the arm comes out from under the chlamys, draped over the left shoulder
    f.poly(SHOULDER_FLAP[frame], m["cloak"], group=41)
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
        ".kkkhhkkkkkkkkkkkkkkkkkdSk..",
        ".kkhhkkkhhkkkkkkkkkkkkdSSSk.",
        "kkhhkkkhhkkkkhkkkkkkkdSSSSk.",
        "kkhkkkhhkkkkhhkkkkkkkSLLLSSk",
        "kkhkkkhkkkkhhkkSSkkkSLLLLLkk",
        "kkkkkkkkkkkhkkSddSkkLLLLLLWk",
        "kkhkkkkhkkkkkkSdSSkSLLLLLLSk",
        "kkkkkkhkkkkkhkSddSkSSLLLLSk.",
        ".kkkkkkkkkkhkkkSSkSSSLLLSSk.",
        ".kkkkkkkkkkkkkkkkkSSSLLSSSk.",
        "..kkkkkkkkkkkkkkkdSSSSSSdk..",
        "...kkkkkkkkkkkkkkdSSSSSdk...",
        "....kkkkkkkkkkkkddSSSddk....",
        ".....kkkkkkkSkkddSSddkk.....",
        "......kkkkkSSkSdddSSSk......",
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
    """sprites_player_battle.png: Kleon, Theo, Ianthe and Ione on the battle
    backdrop. sprites_player_battle_back.png: back frames 0-3 in order."""
    os.makedirs(pv, exist_ok=True)
    tiles = [battle_tile(Image.open(os.path.join(ROOT, "graphics/trainers/front_pics/kleon.png")).convert("RGBA"))]
    for key in ("brendan", "may"):
        pal, fr, _ = built[key]
        tiles.append(battle_tile(to_rgba(fr, pal)))
    tiles.append(battle_tile(Image.open(
        os.path.join(ROOT, "graphics/trainers/front_pics/hierophant_ione.png")).convert("RGBA")))
    sheet = Image.new("RGBA", (96 * len(tiles), 72))
    for i, t in enumerate(tiles):
        sheet.alpha_composite(t, (96 * i, 0))
    upscale(sheet, 3).save(os.path.join(pv, "sprites_player_battle.png"))
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
    upscale(sheet, 3).save(os.path.join(pv, "sprites_player_battle_back.png"))


def grids(built, out):
    """Upscaled pixel grids with coordinates, for placing details."""
    os.makedirs(out, exist_ok=True)
    for key in ("brendan", "may"):
        pal, fr, bk = built[key]
        grid_preview(to_rgba(fr, pal), 12, 4, 0, 60, 64).save(os.path.join(out, key + "_front_grid.png"))
        for i in range(4):
            grid_preview(to_rgba(bk[64 * i:64 * i + 64], pal), 10, 0, 0, 64, 64).save(
                os.path.join(out, "%s_back%d_grid.png" % (key, i)))


def main():
    args = sys.argv[1:]
    if "--write" in args:
        player_sources.reject_legacy_write(
            os.path.join(ROOT, "graphics/trainers/front_pics/brendan.png"))
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    gd = args[args.index("--grids") + 1] if "--grids" in args else None
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
    if gd:
        grids(built, gd)


if __name__ == "__main__":
    main()
