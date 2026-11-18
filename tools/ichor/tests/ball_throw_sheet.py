"""A sheet of ball_throw.sh's screenshots: for each ball, the battle Bag, then
the throw, the ball opening on the Pokemon, and the wobble, cropped to the foe's
side of the screen, at 1x and 2x.

    /usr/bin/python3 tools/ichor/tests/ball_throw_sheet.py [shots_dir] [out.png]
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

SHOTS = sys.argv[1] if len(sys.argv) > 1 else "build/test_ball_throw/shots"
OUT = sys.argv[2] if len(sys.argv) > 2 else "design/art/img/balls/balls_battle.png"
BALLS = ["poseidon", "daedalus", "theseus", "nyx", "poke"]
TIMES = ["t128", "t156", "t168", "t200", "t216", "t240"]
CROP = (120, 8, 232, 96)       # the foe's side: the ball's arc, the opening, the wobble


def shot(ball, tag):
    files = sorted(glob.glob(os.path.join(SHOTS, f"*_{ball}_{tag}.png")))
    return Image.open(files[-1]).convert("RGB") if files else None


def main():
    cw, ch = CROP[2] - CROP[0], CROP[3] - CROP[1]
    k = 2
    row_h = ch * k + 20
    sheet = Image.new("RGB", (240 + len(TIMES) * (cw * k + 6) + 10, len(BALLS) * row_h + 24), (64, 40, 32))
    d = ImageDraw.Draw(sheet)
    d.text((6, 6), "battle Bag (1x) | the throw, the open and the wobble, 2x: frames " + ", ".join(TIMES),
           fill=(248, 224, 136))
    for r, ball in enumerate(BALLS):
        y = 24 + r * row_h
        d.text((6, y), ball, fill=(248, 240, 216))
        bag = shot(ball, "bag")
        if bag:
            sheet.paste(bag, (6, y + 14))
        for i, t in enumerate(TIMES):
            im = shot(ball, t)
            if im:
                c = im.crop(CROP).resize((cw * k, ch * k), Image.NEAREST)
                sheet.paste(c, (250 + i * (cw * k + 6), y + 14))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sheet.save(OUT)
    print(f"ball_throw_sheet.py: {OUT}")


if __name__ == "__main__":
    main()
