#!/usr/bin/env python3
"""Original clay-tablet close-up for Daphne's raking-light revelation."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
PALETTE = [
    (255, 0, 255), (32, 24, 24), (72, 32, 24), (112, 48, 32),
    (152, 64, 40), (184, 88, 48), (200, 104, 56), (224, 128, 64),
    (216, 136, 88), (224, 168, 104), (240, 176, 112), (248, 200, 128),
    (248, 216, 152), (128, 72, 48), (168, 96, 56), (248, 184, 104),
]


def main():
    image = Image.new("P", (64, 64), 0)
    image.putpalette([channel for color in PALETTE for channel in color])
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, 62, 62), radius=4, fill=2, outline=1, width=2)
    for x in range(7, 57, 8):
        for y in (5, 55):
            draw.line([(x, y + 3), (x, y), (x + 5, y), (x + 5, y + 3),
                       (x + 2, y + 3), (x + 2, y + 2)], fill=11)
    draw.polygon([(10, 14), (49, 11), (56, 16), (54, 48),
                  (48, 53), (12, 51), (8, 46)], fill=3, outline=1)
    draw.polygon([(11, 14), (48, 12), (53, 17), (51, 47),
                  (46, 50), (12, 48), (9, 44)], fill=8)
    for x in range(12, 52):
        shade = 11 if x < 20 else 10 if x < 28 else 9 if x < 38 else 8 if x < 45 else 6
        draw.line((x, 17, x - 1, 46), fill=shade)
    for x, y in ((17, 18), (43, 20), (14, 31), (46, 39), (28, 44), (38, 17)):
        draw.line((x, y, x + 3, y + 1), fill=8)
    # Incisions have a light lip above a dark groove, revealed from the left.
    strokes = [
        [(15, 23), (20, 23)], [(17, 23), (17, 28)],
        [(24, 28), (26, 22), (29, 28)], [(25, 26), (28, 26)],
        [(32, 22), (32, 28), (37, 28)], [(36, 22), (36, 28)],
        [(41, 22), (46, 22), (41, 28), (46, 28)],
        [(15, 35), (17, 32), (20, 35), (17, 39), (15, 35)],
        [(24, 32), (24, 39)], [(23, 35), (29, 35)], [(28, 32), (28, 39)],
        [(33, 39), (36, 32), (39, 39)], [(34, 37), (38, 37)],
        [(43, 32), (43, 39), (48, 39)], [(47, 32), (47, 39)],
    ]
    for stroke in strokes:
        draw.line([(x - 1, y - 1) for x, y in stroke], fill=12)
        draw.line(stroke, fill=13)
    draw.line([(49, 12), (46, 15), (48, 19)], fill=3)
    draw.line([(11, 42), (15, 44), (13, 48)], fill=3)
    output = ROOT / "graphics/ichor/tablet_back.png"
    image.save(output, optimize=True, bits=4)
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
