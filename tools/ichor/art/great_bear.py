"""The Great Bear's seven stars, hung at the top of the screen at sea by night
(design/ODYSSEY.md §4, "keep the Bear on your left"; design/postgame/ENGINE.md §5).

Usage:
    /usr/bin/python3 tools/ichor/art/great_bear.py [--preview DIR]

Writes graphics/field_effects/pics/ichor_great_bear.png: a 32x16 4bpp sprite,
index 0 transparent, pale gold stars on nothing. src/ichor_sailing.c loads it
with a blend-immune palette tag, so the night tint never dims it.

The shape is the asterism as seen looking north: the handle to the left
(Alkaid, Mizar with faint Alcor beside it, Alioth), the bowl to the right
(Megrez, Phecda, Merak, Dubhe). Merak and Dubhe, the pointers, line up toward
where the pole star would be, off the top right. The brightest stars get a
small cross of gold; the rest are single bright points with a soft gold halo.

--preview DIR also writes DIR/great_bear_preview.png at 8x on a night-sea blue.
"""
import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "graphics/field_effects/pics/ichor_great_bear.png"
W, H = 32, 16

# Index 0 is transparent (drawn as magenta so it's obvious in an editor).
PALETTE = [
    (255, 0, 255),    # 0 transparent
    (255, 250, 222),  # 1 the star's core, near white
    (248, 222, 140),  # 2 pale gold
    (196, 160, 88),   # 3 dim gold halo
]
PALETTE += [(0, 0, 0)] * (16 - len(PALETTE))

# (name, x, y, size): 2 = a cross, 1 = a point with a dim halo, 0 = a faint point
STARS = [
    ("Alkaid", 2, 7, 1),
    ("Mizar", 8, 4, 1),
    ("Alcor", 10, 3, 0),
    ("Alioth", 13, 5, 2),
    ("Megrez", 18, 7, 1),
    ("Phecda", 19, 12, 1),
    ("Merak", 27, 13, 2),
    ("Dubhe", 28, 6, 2),
]


def draw():
    img = Image.new("P", (W, H), 0)
    img.putpalette([c for rgb in PALETTE for c in rgb])
    px = img.load()

    def put(x, y, index):
        if 0 <= x < W and 0 <= y < H and (px[x, y] == 0 or px[x, y] > index):
            px[x, y] = index

    for _, x, y, size in STARS:
        if size == 0:
            put(x, y, 3)
            continue
        put(x, y, 1)
        arms = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in arms:
            put(x + dx, y + dy, 2 if size == 2 else 3)
        if size == 2:
            for dx, dy in arms:
                put(x + 2 * dx, y + 2 * dy, 3)
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preview", help="also write a large preview into this folder")
    args = ap.parse_args()
    img = draw()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(OUT)
    if args.preview:
        bg = Image.new("RGB", (W, H), (24, 40, 88))
        mask = Image.frombytes("L", (W, H), bytes(0 if i == 0 else 255 for i in img.tobytes()))
        bg.paste(img.convert("RGB"), (0, 0), mask)
        out = Path(args.preview) / "great_bear_preview.png"
        bg.resize((W * 8, H * 8), Image.NEAREST).save(out)
        print(out)


if __name__ == "__main__":
    main()
