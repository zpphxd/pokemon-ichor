"""Alethea's battle back pic: she throws the ball in the catch tutorial.

Usage: python3 tools/ichor/art/sprites_alethea_back.py [--write] [--preview DIR] [--grids DIR]

--write   writes graphics/trainers/back_pics/alethea.png (64x256, four
          frames). The palette is embedded in the PNG; she has no front pic
          yet, so nothing else shares it.
--preview writes sprites_alethea_back.png to DIR: her four frames on the
          battle backdrop, with Ianthe's for comparison.
--grids   writes upscaled pixel grids with coordinates to DIR.

She matches the player back pics in sprites_player.py: from behind, facing
right, cropped at the waist, throwing with the near (left) arm. The arm path,
the hands and the ball come from there, so the throw lines up frame for frame.
Frames: 0 holding the ball, 1 wind-up, 2 release, 3 empty-handed rest
(sBackAnims_Hoenn: the battle intro shows 3, the throw plays 0, 1, 2, 0, 3).

Her look, from the overworld sprite (sprites_npc.py): dark-brown hair under a
blue headband with a ponytail down her back, a sun-gold chiton with short
sleeves, and a leather satchel of scrolls on her left hip.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import (ROOT, Palette, Mat, Fig, save_indexed, to_rgba, battle_bg,  # noqa: E402
                         upscale, palette_report, grid_preview)
import sprites_player as P  # noqa: E402
from PIL import Image  # noqa: E402

OUT = os.path.join(ROOT, "graphics/trainers/back_pics/alethea.png")

PAL = Palette([
    ("ink", (32, 24, 24)),
    ("skin_l", (248, 208, 168)), ("skin_m", (224, 160, 112)), ("skin_d", (168, 104, 72)),
    ("brown", (88, 48, 32)),        # hair, leather
    ("umber", (168, 88, 48)),       # hair sheen, chiton shadow
    ("blue_d", (24, 56, 120)), ("blue_m", (48, 104, 176)), ("blue_l", (112, 168, 224)),
    ("gold_m", (216, 160, 64)), ("gold_l", (248, 216, 112)),   # the sun-gold chiton
    ("linen_d", (200, 176, 144)), ("linen_l", (248, 240, 216)),  # scrolls, the ball's white
    ("red", (192, 80, 48)),         # the ball's red half
])

KEY = {"k": "ink", "b": "brown", "h": "umber", "u": "umber",
       "L": "skin_l", "S": "skin_m", "d": "skin_d",
       "N": "blue_d", "B": "blue_m", "U": "blue_l",
       "O": "gold_l", "o": "gold_m", "W": "linen_l", "w": "linen_d", "R": "red", "_": "_"}
# sprites_player's patches use its own letters; map them onto this palette
P_KEY = dict(KEY, G="gold_l", M="gold_m", D="umber", T="red", c="linen_d", r="brown")


def mats():
    return dict(
        skin=Mat(["skin_d", "skin_m", "skin_l"], outline="ink", line="skin_d", cuts=[0.52, 0.86]),
        chiton=Mat(["umber", "gold_m", "gold_l"], wx=0.85, wy=0.2, cuts=[0.38, 0.86]),
        lea=Mat(["brown"]),
        satchel=Mat(["brown", "umber"], cuts=[0.6]),
    )


# --------------------------------------------------------------------------
# The head: the back of it, turned a little right so the right ear and cheek
# show. The lower rows are Ianthe's (same hair, same turn); the crown above
# them is new, since Alethea wears no hat.
# --------------------------------------------------------------------------

HEAD_X, HEAD_Y = 20, 10          # top-left of the head patch at dx = 0


def head_rows():
    may = P.HEAD_BACK["may"]                 # rows at y 21..38
    w = len(may[0])
    y0 = HEAD_Y
    rows = [["."] * w for _ in range(39 - y0)]    # y 10..38
    for j in range(1, len(may)):
        rows[21 + j - y0] = list(may[j])
    # the crown: an ellipse that meets Ianthe's widest hair row at y 22
    cx, cy, rx, ry = 13.0, 24.0, 12.0, 14.0
    for y in range(y0, 22):
        t = 1 - ((y - cy) / ry) ** 2
        if t <= 0:
            continue
        half = rx * t ** 0.5
        a, b = int(round(cx - half)), int(round(cx + half))
        r = ["."] * w
        for x in range(a, b + 1):
            r[x] = "b"
        r[a] = r[b] = "k"
        if y == y0 or all(c == "." for c in rows[y - y0 - 1]):
            for x in range(a, b + 1):
                r[x] = "k"
        rows[y - y0] = r
    # the top of the outline steps down at the shoulders of the dome
    for y in range(y0 + 1, 22):
        prev, r = rows[y - y0 - 1], rows[y - y0]
        for x in range(w):
            if r[x] == "b" and prev[x] == ".":
                r[x] = "k"
    # sheen: strands sweeping back and down toward the ponytail's knot
    for (x, y) in ((8, 12), (9, 12), (6, 13), (7, 13), (16, 12), (17, 13), (18, 13),
                   (4, 21), (5, 20), (19, 21), (20, 22), (10, 22), (11, 21)):
        if rows[y - y0][x] == "b":
            rows[y - y0][x] = "h"
    # the headband: an arc over the crown, down behind the ears
    for x in range(w):
        dxn = (x - cx) / 12.6
        if abs(dxn) >= 1:
            continue
        yc = 25.0 - 9.0 * (1 - dxn * dxn) ** 0.5
        for k, ch in ((-1, "U"), (0, "B"), (1, "N")):
            y = int(round(yc)) + k
            if y0 <= y <= 38 and rows[y - y0][x] in "bh":
                rows[y - y0][x] = ch
    return ["".join(r) for r in rows]


# The ponytail, tied with a blue cord at the back of the head and falling down
# the middle of her back.
PONYTAIL = [
    "..kkkkk...",
    ".kNBUBNk..",
    ".kNBBBNk..",
    "..kbhbk...",
    ".kbbhbbk..",
    "kbbhbbhbk.",
    "kbhbbhbbk.",
    "kbhbbhbbbk",
    "kbbhbbhbbk",
    "kbbhbbhbbk",
    ".kbhbbhbbk",
    ".kbbhbbhbk",
    ".kbbhbbhk.",
    "..kbhbbhk.",
    "..kbhbbbk.",
    "..kbbhbk..",
    "...kbhbk..",
    "...kbhk...",
    "...khbk...",
    "....kk....",
]
PONY_X, PONY_Y = 26, 27

# Scroll ends poking out of the satchel on her left hip.
SATCHEL = [
    "...kk.kk.......",
    "..kWWkWwk......",
    "..kwWkWwk.kk...",
    ".kkkkkkkkkWWk..",
    "kbbbbbbbbkwWk..",
    "kbbbbbOobbkkkk.",
    "kbbbbbobbbbbbbk",
    "khkkkkkkkkkkhbk",
    "khhhhhhhhhhhhbk",
    "khhhhhhhhhhhhbk",
    "khhhhhhhhhhhbbk",
    "khhhhhhhhhhhbbk",
]
SATCHEL_X, SATCHEL_Y = 14, 52

# The near arm hangs at her side on the rest frame: shoulder, elbow, wrist.
REST_ARM = [(15, 46), (12, 55), (12, 66)]
REST_SLEEVE = [(10, 43), (19, 39), (22, 45), (18, 51), (12, 52), (9, 48)]


def figure(frame):
    m = mats()
    f = Fig(PAL)
    dx = 2 if frame == 2 else 0      # she leans into the release

    # far (right) arm, mostly behind the body
    f.thick_line([(50 + dx, 45), (55 + dx, 54), (56 + dx, 66)], 8, m["skin"], group=5)
    f.poly([(46 + dx, 40), (53 + dx, 41), (58 + dx, 47), (57 + dx, 52), (51 + dx, 50)], m["chiton"], group=6)
    # the chiton over the back, to the waist
    f.poly([(28 + dx, 38), (22 + dx, 39), (16 + dx, 41), (13 + dx, 44), (12 + dx, 50), (13, 57), (13, 63),
            (54, 63), (54 + dx, 56), (53 + dx, 49), (52 + dx, 44), (49 + dx, 41), (44 + dx, 39), (39 + dx, 38)],
           m["chiton"], group=10)
    # folds fall from the shoulder pins and gather at the girdle
    for p0, p1, w0, w1, d in (((21 + dx, 42), (24, 58), 1, 2, 0.45), ((35 + dx, 41), (34, 58), 1, 1, -0.35),
                              ((44 + dx, 41), (41, 58), 1, 2, 0.45)):
        P.fold(f, p0, p1, w0, w1, d)
    # the blousing (kolpos) catches the light just over the girdle
    f.shade_poly([(15, 56), (52, 56), (52, 58), (15, 58)], -0.3)
    # the girdle, a little blousing over it, and the skirt below it
    f.rect(13, 59, 54, 60, m["lea"], group=11)
    # neck
    f.rect(30 + dx, 31, 39 + dx, 40, m["skin"], group=30)
    # satchel strap from the right shoulder down to the left hip
    f.thick_line([(47 + dx, 41), (33 + dx, 48), (22, 54)], 2, m["lea"], group=20)

    if frame in (0, 2):
        arm(f, m, frame)
    elif frame == 3:
        f.thick_line(REST_ARM[:2], 8, m["skin"], group=40)
        f.thick_line(REST_ARM[1:], 7, m["skin"], group=40)
        f.poly(REST_SLEEVE, m["chiton"], group=41)

    # the satchel sits over the strap, under the hanging arm
    f.patch(SATCHEL_X, SATCHEL_Y, SATCHEL, KEY)
    f.patch(HEAD_X + dx, HEAD_Y, head_rows(), KEY)
    f.patch(44 + dx, 27, ["kLL.", "kWk.", "kkLk", "LSSk", "LSSk", "SSk."], KEY)
    f.patch(PONY_X + dx + (1 if frame == 2 else 0), PONY_Y, PONYTAIL, KEY)
    out = f.render()

    if frame == 3:
        # the resting arm hangs in front of the satchel
        a = Fig(PAL)
        a.thick_line(REST_ARM[:2], 8, m["skin"], group=40)
        a.thick_line(REST_ARM[1:], 7, m["skin"], group=40)
        a.poly(REST_SLEEVE, m["chiton"], group=41)
        out = P.layer(out, a.render())
    if frame in (0, 1):
        # the raised arm is in front of the satchel (0) and the head (1)
        a = Fig(PAL)
        arm(a, m, frame)
        out = P.layer(out, a.render())
    return out


def arm(f, m, frame):
    """sprites_player.arm with a short gold sleeve for the cloak flap."""
    sh, el, wr = P.ARM[frame]
    f.thick_line([sh, el], 8, m["skin"], group=40)
    f.thick_line([el, wr], 7, m["skin"], group=40)
    f.poly(P.SHOULDER_FLAP[frame], m["chiton"], group=41)
    if frame in (0, 1):
        f.patch(wr[0] - 5, wr[1] - 11, P.HAND_BALL, dict(P_KEY, R="red", r="brown", w="linen_d"))
    else:
        f.patch(wr[0] - 1, wr[1] - 5, P.HAND_OPEN, P_KEY)


def build():
    return np.vstack([figure(i) for i in range(4)])


def preview(bk, pv):
    os.makedirs(pv, exist_ok=True)
    rows = []
    bg = battle_bg(64 * 4 + 12, 72)
    for i in range(4):
        bg.alpha_composite(to_rgba(bk[64 * i:64 * i + 64], PAL), (4 + 64 * i, 8))
    rows.append(bg)
    may = Image.open(os.path.join(ROOT, "graphics/trainers/back_pics/may.png")).convert("RGBA")
    bg = battle_bg(64 * 4 + 12, 72)
    for i in range(4):
        fr = may.crop((0, 64 * i, 64, 64 * i + 64))
        px = np.array(fr)
        px[(px[..., 0] == 112) & (px[..., 1] == 192) & (px[..., 2] == 160)] = 0
        bg.alpha_composite(Image.fromarray(px), (4 + 64 * i, 8))
    rows.append(bg)
    sheet = Image.new("RGBA", (rows[0].width, 72 * len(rows)))
    for j, r in enumerate(rows):
        sheet.alpha_composite(r, (0, 72 * j))
    upscale(sheet, 3).save(os.path.join(pv, "sprites_alethea_back.png"))


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    gd = args[args.index("--grids") + 1] if "--grids" in args else None
    bk = build()
    palette_report(bk, PAL, "alethea back")
    if "--write" in args:
        save_indexed(bk, PAL, OUT)
    if pv:
        preview(bk, pv)
    if gd:
        os.makedirs(gd, exist_ok=True)
        for i in range(4):
            grid_preview(to_rgba(bk[64 * i:64 * i + 64], PAL), 10, 0, 0, 64, 64).save(
                os.path.join(gd, "alethea_back%d_grid.png" % i))


if __name__ == "__main__":
    main()
