#!/usr/bin/env python3
"""The twelve 64x64 black-figure paintings from SYSTEMS.md section 5."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
PALETTE = [
    (255, 0, 255), (32, 24, 24), (184, 88, 48), (224, 128, 64),
    (248, 184, 104), (112, 48, 32), (72, 32, 24), (248, 216, 152),
    (152, 64, 40), (224, 168, 56), (96, 56, 32), (200, 104, 56),
    (240, 152, 80), (136, 72, 48), (216, 136, 88), (248, 200, 128),
]


def person(d, x, y, height=26, arm=None):
    head = max(2, height // 8)
    d.ellipse((x - head, y, x + head, y + head * 2), fill=1)
    neck = y + head * 2
    hem = y + height - 6
    d.polygon([(x - 3, neck), (x + 3, neck), (x + 6, hem),
               (x - 6, hem)], fill=1)
    d.line([(x - 3, hem), (x - 4, y + height)], fill=1, width=2)
    d.line([(x + 2, hem), (x + 4, y + height)], fill=1, width=2)
    d.line([(x - 2, neck + 3), (x - 7, neck + 8)], fill=1, width=2)
    d.line([(x + 2, neck + 3), arm or (x + 7, neck + 8)], fill=1, width=2)
    d.line([(x - 4, hem - 2), (x + 4, hem - 2)], fill=3)


def beast(d, x, y, donkey=False):
    d.ellipse((x - 8, y - 4, x + 7, y + 4), fill=1)
    d.line([(x + 5, y), (x + 8, y - 7)], fill=1, width=3)
    d.rectangle((x + 6, y - 8, x + 12, y - 5), fill=1)
    for dx in (-6, -2, 3, 6):
        d.line([(x + dx, y + 2), (x + dx - 1, y + 10)], fill=1, width=2)
    d.line([(x - 7, y), (x - 11, y + 4)], fill=1, width=2)
    if donkey:
        d.line([(x + 7, y - 7), (x + 6, y - 12)], fill=1, width=2)
        d.line([(x + 10, y - 7), (x + 11, y - 12)], fill=1, width=2)
    else:
        d.line([(x + 7, y - 8), (x + 4, y - 11)], fill=1, width=2)


def panel(myth):
    im = Image.new("P", (64, 64), 0)
    im.putpalette([c for rgb in PALETTE for c in rgb])
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1, 1, 62, 62), radius=4, fill=5, outline=1, width=2)
    d.rectangle((5, 5, 58, 58), fill=3, outline=4)
    d.rectangle((8, 10, 55, 52), fill=2)
    for x in range(8, 56, 8):
        for y in (6, 54):
            d.line([(x, y + 3), (x, y), (x + 5, y), (x + 5, y + 3),
                    (x + 2, y + 3), (x + 2, y + 2)], fill=1)
    d.line((9, 50, 54, 50), fill=1)
    if myth == 0:
        person(d, 17, 19, arm=(30, 29))
        person(d, 43, 16, 29, arm=(31, 28))
        d.ellipse((27, 24, 34, 32), fill=7, outline=1)
        d.line([(29, 26), (33, 30)], fill=5)
    elif myth == 1:
        person(d, 29, 16, 31, arm=(43, 30))
        d.polygon([(29, 24), (36, 43), (29, 43)], fill=6)
        d.ellipse((40, 26, 48, 34), fill=5, outline=1)
        for x, y in ((42, 28), (45, 28), (42, 30), (45, 30), (42, 32), (45, 32)):
            d.point((x, y), fill=7)
    elif myth == 2:
        person(d, 18, 17, arm=(34, 26))
        d.rectangle((32, 14, 49, 39), outline=1, width=2)
        for x in range(35, 48, 3):
            d.line((x, 16, x, 38), fill=1)
        for y in (23, 29, 35):
            d.line((34, y, 47, y), fill=5)
        d.ellipse((43, 43, 47, 47), fill=1)
        for dx in (-1, 1):
            for dy in (-3, -1, 1, 3):
                d.line([(45, 45), (45 + dx * 7, 45 + dy)], fill=1)
    elif myth == 3:
        person(d, 17, 29, 16, arm=(28, 36))
        beast(d, 39, 34)
        d.line([(23, 36), (31, 32)], fill=1)
        for x in (27, 33, 39):
            d.line([(x + 2, 47), (x, 48), (x + 2, 49)], fill=1)
    elif myth == 4:
        beast(d, 37, 35, donkey=True)
        person(d, 34, 15, 20, arm=(26, 29))
        person(d, 15, 20, arm=(27, 31))
        d.line([(21, 29), (37, 30)], fill=1)
        d.rectangle((23, 24, 28, 28), fill=1)
        d.line((25, 28, 25, 31), fill=1)
    elif myth == 5:
        d.ellipse((37, 37, 44, 44), fill=1)
        d.polygon([(38, 38), (29, 20), (23, 24), (35, 41)], fill=1)
        d.line([(29, 25), (18, 20), (14, 25)], fill=1, width=2)
        d.line([(34, 32), (45, 25), (48, 19)], fill=1, width=2)
        d.line([(25, 23), (20, 13)], fill=1, width=2)
        for x, y in ((12, 16), (49, 37), (17, 38), (40, 12)):
            d.line([(x, y), (x + 4, y + 5)], fill=1)
            d.line([(x, y + 3), (x + 3, y + 3)], fill=1)
    elif myth == 6:
        person(d, 20, 17, arm=(39, 27))
        d.ellipse((35, 31, 49, 48), fill=5, outline=1, width=2)
        d.rectangle((38, 29, 46, 33), fill=1)
        d.line([(35, 26), (46, 22)], fill=1, width=3)
        d.ellipse((41, 39, 43, 41), fill=7)
    elif myth == 7:
        person(d, 24, 16, arm=(34, 28))
        d.arc((29, 23, 39, 36), 0, 180, fill=1, width=2)
        d.line((30, 23, 30, 31), fill=1, width=2)
        d.line((38, 23, 38, 31), fill=1, width=2)
        for x in (32, 34, 36):
            d.line((x, 24, x, 33), fill=1)
        beast(d, 44, 39)
        d.ellipse((10, 36, 16, 40), fill=1)
        d.line([(14, 38), (18, 34)], fill=1)
    elif myth == 8:
        d.ellipse((29, 18, 35, 24), fill=1)
        d.polygon([(31, 24), (38, 35), (29, 38), (25, 28)], fill=1)
        d.line([(28, 29), (17, 39)], fill=1, width=2)
        d.line([(34, 35), (44, 39), (48, 46)], fill=1, width=2)
        d.line([(29, 37), (23, 44), (16, 45)], fill=1, width=2)
        d.ellipse((13, 38, 18, 43), fill=9, outline=1)
    elif myth == 9:
        person(d, 24, 15, 23, arm=(37, 29))
        d.polygon([(30, 28), (48, 28), (45, 36), (32, 36)], fill=1)
        for x in (33, 45):
            d.ellipse((x - 4, 36, x + 4, 44), outline=1, width=2)
            d.line((x, 36, x, 44), fill=1)
        d.polygon([(42, 25), (39, 17), (44, 20), (45, 11),
                   (50, 20), (53, 16), (51, 28)], fill=9, outline=1)
    elif myth == 10:
        person(d, 14, 20, 26, arm=(24, 32))
        for x, y in ((30, 15), (40, 17), (50, 19)):
            person(d, x, y, 25)
        d.ellipse((22, 28, 27, 33), fill=9, outline=1)
    else:
        person(d, 18, 19, arm=(29, 30))
        person(d, 43, 18, 29, arm=(32, 31))
        d.line([(40, 21), (37, 15), (36, 20)], fill=1, width=2)
        d.line([(46, 21), (49, 15), (50, 20)], fill=1, width=2)
        d.line((29, 19, 29, 37), fill=7, width=2)
        d.line([(17, 46), (29, 46), (29, 43), (39, 43), (39, 48)], fill=7)
    return im


def main():
    sheet = Image.new("P", (64, 64 * 12), 0)
    sheet.putpalette([c for rgb in PALETTE for c in rgb])
    panels = [panel(myth) for myth in range(12)]
    assert len({painting.tobytes() for painting in panels}) == 12
    for myth, painting in enumerate(panels):
        sheet.paste(painting, (0, 64 * myth))
    assert sheet.size == (64, 768)
    assert len(sheet.getpalette()) == 16 * 3
    assert max(sheet.getdata()) < 16
    out = ROOT / "graphics/ichor/amphorae.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
