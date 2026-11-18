#!/usr/bin/env python3
"""Crops of every Astyra statue at 1x and 3x, on their real ground, beside the
reference (design/art/refs/statue_zeus_reference.png): the statue review gate.

    /usr/bin/python3 tools/ichor/art/astyra_statue_crops.py   # design/awe/img/statues_*.png
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import astyra_art as AA  # noqa: E402
import astyra_statues as ST  # noqa: E402
import kythera_lib as K  # noqa: E402

OUT = K.ROOT / "design/awe/img"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pieces = [("promachos", ST.promachos()),
              ("maidens", AA.crop(AA.erechtheion(), "maidens", 6, 3, 4, 4)),
              ("kodros", ST.hero_statue("kodros", ST.KODROS, "Kodros")),
              ("kairos", ST.hero_statue("kairos", ST.KAIROS, "Kairos"))]
    ims = []
    for name, s in pieces:
        im = Image.fromarray(K.composite(s))
        im.save(OUT / f"statues_{name}_1x.png")
        im3 = im.resize((im.width * 3, im.height * 3), Image.NEAREST)
        im3.save(OUT / f"statues_{name}_3x.png")
        ims.append((name, im, im3))
    W = sum(i3.width for _, _, i3 in ims) + sum(i.width for _, i, _ in ims) + 20 * len(ims) * 2
    H = max(i3.height for _, _, i3 in ims) + 24
    sheet = Image.new("RGB", (W, H), (28, 28, 36))
    d = ImageDraw.Draw(sheet)
    x = 10
    for name, im, im3 in ims:
        d.text((x, 4), name + " 1x / 3x", fill=(230, 230, 200))
        sheet.paste(im, (x, 20))
        x += im.width + 10
        sheet.paste(im3, (x, 20))
        x += im3.width + 20
    sheet.save(OUT / "statues_sheet.png")
    print(OUT / "statues_sheet.png")


if __name__ == "__main__":
    main()
