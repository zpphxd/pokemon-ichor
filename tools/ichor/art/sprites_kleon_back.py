"""Kleon's battle back pic: he fights beside the player on the night of the Mysteries.

Usage: python3 tools/ichor/art/sprites_kleon_back.py [--write] [--preview DIR] [--grids DIR]

--write   writes graphics/trainers/back_pics/kleon.png (64x256, four frames). The
          palette is embedded in the PNG and is his front pic's colors
          (sprites_trainers.kleon), so the two read as one boy.
--preview writes sprites_kleon_back.png to DIR: his four frames on the battle
          backdrop, with Theo's for comparison.
--grids   writes upscaled pixel grids with coordinates to DIR.

The multi battle of beat 22 (design/phase2/SCRIPT.md) slides the partner in from
behind, so PARTNER_ICHOR_KLEON_ELEUSA_* needs TRAINER_PIC_KLEON to have a back pic.

He matches the player back pics in sprites_player.py: from behind, facing right,
cropped at the waist, throwing with the near (left) arm. The arm path, the hands,
the ball and the chlamys pinned at the right shoulder come from there, so the throw
lines up frame for frame with the player's beside him. Frames: 0 holding the ball,
1 wind-up, 2 release, 3 empty-handed rest (sBackAnims_Hoenn).

His look, from the front pic: spiky dark-brown hair and no hat, the Lakonian red
cloak over his back pinned with a bronze brooch, a linen exomis under it.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import (ROOT, Palette, Mat, Fig, save_indexed, to_rgba, battle_bg,  # noqa: E402
                         upscale, palette_report, grid_preview)
import sprites_player as P  # noqa: E402
from PIL import Image  # noqa: E402

OUT = os.path.join(ROOT, "graphics/trainers/back_pics/kleon.png")

# His front pic's palette (sprites_trainers.kleon), less its unused shades.
PAL = Palette([
    ("ink", (32, 24, 24)),
    ("skin_l", (248, 208, 168)), ("skin_m", (224, 160, 112)), ("skin_d", (176, 104, 72)),
    ("hair_d", (48, 32, 32)), ("hair_l", (96, 64, 48)),
    ("cr_l", (216, 72, 64)), ("cr_m", (168, 40, 48)), ("cr_d", (104, 24, 40)),   # the red cloak
    ("br_l", (248, 216, 120)), ("br_m", (216, 160, 64)),                          # the brooch
    ("lin_l", (248, 240, 216)), ("lin_d", (200, 176, 144)),                       # linen, the ball's white
    ("lea", (104, 56, 40)),
])

KEY = {"k": "ink", "b": "hair_d", "h": "hair_l", "L": "skin_l", "S": "skin_m", "d": "skin_d",
       "W": "lin_l", "w": "lin_d", "R": "cr_m", "r": "cr_d", "G": "br_l", "M": "br_m", "D": "lea",
       "_": "_"}


def mats():
    return dict(
        skin=Mat(["skin_d", "skin_m", "skin_l"], outline="ink", line="skin_d", cuts=[0.52, 0.86]),
        cloak=Mat(["cr_d", "cr_m", "cr_l"], wx=0.85, wy=0.2, cuts=[0.3, 0.72]),
        linen=Mat(["lin_d", "lin_l"], wx=0.85, wy=0.2, cuts=[0.62]),
    )


# --------------------------------------------------------------------------
# The head: the back of it, turned a little right so the right ear and cheek
# show. The lower rows are Ianthe's (the same turn, dark hair); above them, a
# short crop that stands up in spikes, as on his front pic.
# --------------------------------------------------------------------------

HEAD_X, HEAD_Y = 20, 8            # top-left of the head patch at dx = 0

# spike tips (x, y) in patch coordinates, swept back and to the left
SPIKES = [(2, 9), (6, 4), (10, 1), (15, 0), (19, 3), (23, 7)]


def head_rows():
    may = P.HEAD_BACK["may"]                 # rows at y 21..38
    w = len(may[0])
    y0 = HEAD_Y
    h = 39 - y0
    grid = [["."] * w for _ in range(h)]
    for j in range(1, len(may)):
        grid[21 + j - y0] = list(may[j])
    # the crown: an ellipse that meets Ianthe's widest hair row at y 22
    cx, cy, rx, ry = 13.0, 24.0, 12.0, 12.0
    fill = np.zeros((h, w), bool)
    for y in range(y0, 23):
        t = 1 - ((y - cy) / ry) ** 2
        if t <= 0:
            continue
        half = rx * t ** 0.5
        for x in range(int(round(cx - half)), int(round(cx + half)) + 1):
            if 0 <= x < w:
                fill[y - y0, x] = True
    # the spikes: triangles from the dome's edge up to each tip
    for tx, ty in SPIKES:
        for y in range(ty, 16):
            k = (y - ty) / 2.2
            for x in range(int(round(tx - k)), int(round(tx + k)) + 1):
                if 0 <= x < w and 0 <= y < h:
                    fill[y, x] = True
    # hair fills the crown; an ink edge where it meets the background
    top = 23 - y0
    for y in range(top):
        for x in range(w):
            if fill[y, x]:
                grid[y][x] = "b"
    for y in range(top):
        for x in range(w):
            if not fill[y, x]:
                continue
            edge = any(not (0 <= x + dx < w and 0 <= y + dy < h) or
                       (y + dy < top and not fill[y + dy, x + dx]) or
                       (y + dy >= top and grid[y + dy][x + dx] == ".")
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge:
                grid[y][x] = "k"
    # sheen: a light streak down each spike and across the crown
    for tx, ty in SPIKES:
        for y in range(ty + 2, min(ty + 6, top)):
            x = int(round(tx + (y - ty) * 0.25))
            if 0 <= x < w and grid[y][x] == "b":
                grid[y][x] = "h"
    for (x, y) in ((8, 13), (9, 13), (12, 12), (13, 12), (17, 13), (18, 14), (5, 17), (6, 16), (20, 17)):
        if grid[y][x] == "b":
            grid[y][x] = "h"
    return ["".join(r) for r in grid]


def figure(frame):
    m = mats()
    f = Fig(PAL)
    dx = 2 if frame == 2 else 0      # he leans into the release

    # the red cloak over the back, pinned at the right shoulder (Theo's chlamys)
    f.poly([(28 + dx, 38), (22 + dx, 39), (16 + dx, 41), (12 + dx, 44), (9, 48), (7, 54), (5, 63),
            (59, 63), (58, 56), (56 + dx, 49), (54 + dx, 44), (50 + dx, 41), (45 + dx, 39), (39 + dx, 38)],
           m["cloak"], group=10)
    pin = (48 + dx, 42)
    P.fold(f, pin, (40, 63), 1, 4, 0.5)
    P.fold(f, (pin[0] + 1, pin[1] + 1), (50, 63), 1, 3, 0.45)
    P.fold(f, (pin[0] - 3, pin[1]), (28, 63), 1, 4, 0.4)
    P.fold(f, (pin[0] - 2, pin[1]), (36, 63), 1, 2, -0.35)
    P.fold(f, (19 + dx, 44), (15, 63), 1, 3, 0.4)
    P.fold(f, (24 + dx, 42), (22, 63), 1, 2, -0.3)
    # the exomis's linen shows at the nape, under the cloak's edge
    f.poly([(27 + dx, 37), (42 + dx, 37), (44 + dx, 40), (25 + dx, 40)], m["linen"], group=25)
    # neck
    f.rect(30 + dx, 31, 39 + dx, 40, m["skin"], group=30)
    # the bronze brooch on the right shoulder (behind the arm on the release)
    if frame != 2:
        f.patch(46, 38, [".kkkk.", "kGGGMk", "kGMMDk", ".kkkk."], KEY)

    if frame in (0, 2):
        arm(f, m, frame)
    elif frame == 3:
        f.thick_line([(14, 47), (11, 56)], 8, m["skin"], group=40)
        f.thick_line([(11, 56), (11, 64)], 7, m["skin"], group=40)
        f.poly(P.SHOULDER_FLAP[0], m["cloak"], group=41)

    f.patch(HEAD_X + dx, HEAD_Y, head_rows(), KEY)
    out = f.render()
    if frame == 1:
        # the raised arm is in front of the head
        a = Fig(PAL)
        arm(a, m, frame)
        out = P.layer(out, a.render())
    return out


def arm(f, m, frame):
    """sprites_player.arm, with his red cloak over the shoulder."""
    sh, el, wr = P.ARM[frame]
    f.thick_line([sh, el], 8, m["skin"], group=40)
    f.thick_line([el, wr], 7, m["skin"], group=40)
    f.poly(P.SHOULDER_FLAP[frame], m["cloak"], group=41)
    if frame in (0, 1):
        f.patch(wr[0] - 5, wr[1] - 11, P.HAND_BALL, dict(KEY, R="cr_m", r="cr_d", w="lin_d"))
    else:
        f.patch(wr[0] - 1, wr[1] - 5, P.HAND_OPEN, KEY)


def build():
    return np.vstack([figure(i) for i in range(4)])


def preview(bk, pv):
    os.makedirs(pv, exist_ok=True)
    rows = []
    bg = battle_bg(64 * 4 + 12, 72)
    for i in range(4):
        bg.alpha_composite(to_rgba(bk[64 * i:64 * i + 64], PAL), (4 + 64 * i, 8))
    rows.append(bg)
    theo = Image.open(os.path.join(ROOT, "graphics/trainers/back_pics/brendan.png")).convert("RGBA")
    bg = battle_bg(64 * 4 + 12, 72)
    for i in range(4):
        fr = theo.crop((0, 64 * i, 64, 64 * i + 64))
        px = np.array(fr)
        px[(px[..., 0] == 112) & (px[..., 1] == 192) & (px[..., 2] == 160)] = 0
        bg.alpha_composite(Image.fromarray(px), (4 + 64 * i, 8))
    rows.append(bg)
    sheet = Image.new("RGBA", (rows[0].width, 72 * len(rows)))
    for j, r in enumerate(rows):
        sheet.alpha_composite(r, (0, 72 * j))
    upscale(sheet, 3).save(os.path.join(pv, "sprites_kleon_back.png"))


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    gd = args[args.index("--grids") + 1] if "--grids" in args else None
    bk = build()
    palette_report(bk, PAL, "kleon back")
    if "--write" in args:
        save_indexed(bk, PAL, OUT)
    if pv:
        preview(bk, pv)
    if gd:
        os.makedirs(gd, exist_ok=True)
        for i in range(4):
            grid_preview(to_rgba(bk[64 * i:64 * i + 64], PAL), 10, 0, 0, 64, 64).save(
                os.path.join(gd, "kleon_back%d_grid.png" % i))


if __name__ == "__main__":
    main()
