#!/usr/bin/env python3
"""The climax's small objects (design/phase4/SCRIPT.md III-9 to III-11), 16x16, on
the theoxenia palette so they keep their color in the Frozen Hour without
coloring the cast and folk frozen round them:

  spark   one of the Fates' sparks, circling a sundial on the Stair (it heals)
  harpe   the Harpe, the adamant sickle, falling end over end

  python3 tools/ichor/art/sprites_climax.py [--write]
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "graphics/object_events/pics/misc/ichor"
PAL = ROOT / "graphics/object_events/palettes/ichor_theoxenia.pal"

# palette indices: 1 ink, 5 gold shade, 6 gold, 7 pale gold, 10 linen, 11 white,
# 12 stone, 13 dark
LEGEND = {"k": 1, "g": 5, "G": 6, "y": 7, "l": 10, "w": 11, "s": 12, "d": 13}

OBJECTS = {
    "spark": [
        "................",
        ".......y........",
        ".......y........",
        "......yGy.......",
        "..y...yGy...y...",
        "...y..GwG..y....",
        "....yGwwwGy.....",
        ".yyyGwwwwwGyyy..",
        "....yGwwwGy.....",
        "...y..GwG..y....",
        "..y...yGy...y...",
        "......yGy.......",
        ".......y........",
        ".......y........",
        "................",
        "................"],
    "harpe": [
        "................",
        "......kkkk......",
        "....kkddddkk....",
        "...kdsskkkddk...",
        "..kdsk....kdk...",
        "..kdk......kk...",
        "..kdk...........",
        "..kdsk..........",
        "...kdskk........",
        "....kddskk......",
        ".....kkddk......",
        ".......kGGk.....",
        "........kGGk....",
        ".........kgGk...",
        "..........kgk...",
        "...........k...."],
}


def palette():
    v = list(map(int, PAL.read_text().split()[3:]))
    return [tuple(v[i * 3:i * 3 + 3]) for i in range(16)]


def build(rows):
    arr = np.zeros((16, 16), np.uint8)
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != ".":
                arr[y, x] = LEGEND[ch]
    return arr


def main():
    pal = palette()
    flat = [c for rgb in pal for c in rgb]
    for name, rows in OBJECTS.items():
        im = Image.fromarray(build(rows), "P")
        im.putpalette(flat)
        if "--write" in sys.argv:
            OUT.mkdir(parents=True, exist_ok=True)
            im.save(OUT / f"{name}.png", transparency=0)
            print("wrote", OUT / f"{name}.png")


if __name__ == "__main__":
    main()
