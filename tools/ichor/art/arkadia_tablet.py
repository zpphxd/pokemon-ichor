#!/usr/bin/env python3
"""Draw Iapetos's wax tablet for its picture window (beat 42, STORY.md §6.4).

Fresh wax in a wooden frame, a neat hand in five lines, and at the end of the
last line a little hook. 64x64, 16 colors, index 0 transparent.
Writes graphics/ichor/act2/kleon_tablet.png; src/ichor_arkadia.c shows it.

Usage: /usr/bin/python3 tools/ichor/art/arkadia_tablet.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "graphics/ichor/act2/kleon_tablet.png"

PAL = [
    (0, 0, 0),          # 0 transparent (the window's white shows round the tablet)
    (32, 24, 24),       # 1 ink
    (72, 48, 32),       # 2 frame shadow
    (120, 80, 48),      # 3 frame
    (168, 120, 72),     # 4 frame lit
    (208, 168, 112),    # 5 frame edge
    (56, 40, 24),       # 6 wax, deep
    (88, 64, 32),       # 7 wax
    (120, 88, 48),      # 8 wax lit
    (200, 176, 128),    # 9 the scratched letters
    (232, 216, 176),    # 10 letters, catching light
    (248, 248, 240),    # 11 white
]


def main():
    img = Image.new("P", (64, 64), 0)
    img.putpalette([c for rgb in PAL for c in rgb] + [0] * (3 * (256 - len(PAL))))
    px = img.load()
    # the frame: a board 56 x 48, with a raised rim
    x0, y0, x1, y1 = 4, 8, 59, 55
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            edge = x in (x0, x1) or y in (y0, y1)
            rim = x0 < x < x1 and y0 < y < y1 and (x < x0 + 4 or x > x1 - 4 or y < y0 + 4 or y > y1 - 4)
            if edge:
                px[x, y] = 1
            elif rim:
                px[x, y] = 5 if (y < y0 + 2 or x < x0 + 2) else (4 if (x + y) % 5 else 3)
            else:
                px[x, y] = 7 if (x * 3 + y) % 11 else 6
    # the wax's inner shadow, top and left
    for x in range(x0 + 4, x1 - 3):
        px[x, y0 + 4] = 6
    for y in range(y0 + 4, y1 - 3):
        px[x0 + 4, y] = 6
    # a gleam on the fresh wax
    for i in range(10):
        if 0 <= 44 - i < 64:
            px[44 - i, y0 + 6 + i // 2] = 8
    # five lines of a neat small hand: short strokes with gaps between words
    lines_y = [y0 + 9, y0 + 16, y0 + 23, y0 + 30, y0 + 37]
    words = [[5, 8, 4, 7], [6, 3, 9, 5], [7, 6, 4, 6], [4, 9, 6, 5], [8, 5, 6]]
    for ly, ws in zip(lines_y, words):
        x = x0 + 8
        for w in ws:
            for i in range(w):
                h = (x * 7 + ly) % 3
                px[x, ly - h] = 9
                px[x, ly - h - 1] = 10 if (x % 3 == 0) else 9
                if (x + ly) % 4 == 0:
                    px[x, ly + 1] = 9
                x += 1
            x += 2
        last_x = x
    # the hook, at the end of the last line: a little curl, brighter than the rest
    hx, hy = last_x, lines_y[-1]
    for (dx, dy) in ((0, 0), (1, 0), (2, -1), (2, -2), (2, -3), (1, -4), (0, -3)):
        px[hx + dx, hy + dy] = 11
    img.save(OUT, transparency=0)
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
