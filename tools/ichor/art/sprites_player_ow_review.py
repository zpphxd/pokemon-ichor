"""Crops tools/ichor/tests/player_ow_walk.lua's screenshots into 3x filmstrips.

Usage:
    python3 tools/ichor/art/sprites_player_ow_review.py SHOTS_DIR OUT.png [--title TEXT]

Each row is one move from the walk test (walk up, down, left, right, then run
the same way holding B); each cell is the player 2 frames apart while the key
is held, so every walk and run frame appears mid-step. The first cell of the
first row is the player standing before the test moves.
"""
import argparse
import glob
import os
import re

from PIL import Image, ImageDraw

# The player's 16x32 frame sits at (112, 56) on the 240x160 screen; the crop
# adds a margin for the shadow and the fishing rod's reach.
BOX = (104, 52, 136, 92)
SCALE = 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shots")
    ap.add_argument("out")
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    rows = {}
    for path in sorted(glob.glob(os.path.join(args.shots, "*.png"))):
        m = re.match(r"(\d\d)_(\w+?)_(\d{3})\.png$", os.path.basename(path))
        if m:
            rows.setdefault((m.group(1), m.group(2)), []).append(path)
    stand = os.path.join(args.shots, "00_stand.png")

    cw, ch = (BOX[2] - BOX[0]) * SCALE, (BOX[3] - BOX[1]) * SCALE
    label_w, pad, top = 90, 2, 18 if args.title else 0
    ncol = max(len(v[::2]) for v in rows.values()) + 1
    out = Image.new("RGB", (label_w + ncol * (cw + pad), top + len(rows) * (ch + pad)), (40, 40, 48))
    d = ImageDraw.Draw(out)
    if args.title:
        d.text((4, 3), args.title, fill=(255, 255, 255))

    def cell(path, x, y):
        im = Image.open(path).convert("RGB").crop(BOX)
        out.paste(im.resize((cw, ch), Image.NEAREST), (x, y))

    for r, ((num, name), paths) in enumerate(sorted(rows.items())):
        y = top + r * (ch + pad)
        d.text((4, y + ch // 2 - 5), name.replace("_", " "), fill=(255, 255, 255))
        x = label_w
        if r == 0 and os.path.exists(stand):
            cell(stand, x, y)
        x += cw + pad
        for p in paths[::2]:
            cell(p, x, y)
            x += cw + pad
    out.save(args.out)


if __name__ == "__main__":
    main()
