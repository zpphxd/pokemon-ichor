#!/usr/bin/env python3
"""Draw the Labrys seal field object: a bronze disc stamped with the double
axe, set in a stone footing. It marks every gate the Labrys opens, so it must
never read as a breakable rock.

  /usr/bin/python3 tools/ichor/art/labrys_seal.py

Writes graphics/object_events/pics/misc/ichor/labrys_seal.png on the
ICHOR_CAST palette (shared with tablet.png).
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
PAL_SRC = ROOT / "graphics/object_events/pics/misc/ichor/tablet.png"
OUT = ROOT / "graphics/object_events/pics/misc/ichor/labrys_seal.png"

# ICHOR_CAST indices: 1 outline, 2 dark bronze, 4 bronze, 8 gold, 9 pale gold,
# 10 stone, 11 stone light, 14 stone shadow, 3 deep red (the stamped field).
ART = """
.....KKKKKK.....
...KKMMMMMMKK...
..KMMDDKKDDDDK..
.KMKKDDHGDDKKDK.
.KMHHKDHGDKHGDK.
KMDHHHKHGKHHGDDK
KMDHHHHHGHHHGDDK
KMDHHHKHGKHHGDDK
.KDHHKDHGDKHGDK.
.KDKKDDHGDDKKDK.
..KDDDDHGDDDDK..
.SKKDDDKKDDDKKs.
SLLLLLLLLLLLLLss
SLSSLSSSSLSSSSss
SSSSSSSSSSSSSSss
.ssssssssssssss.
"""
KEY = {".": 0, "K": 1, "D": 2, "M": 4, "G": 8, "H": 9, "r": 3,
       "S": 10, "L": 11, "s": 14}


def main():
    rows = [r for r in ART.strip("\n").split("\n")]
    assert len(rows) == 16 and all(len(r) == 16 for r in rows), [len(r) for r in rows]
    pal = Image.open(PAL_SRC).getpalette()
    im = Image.new("P", (16, 16), 0)
    im.putpalette(pal)
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            im.putpixel((x, y), KEY[c])
    im.save(OUT)
    im.resize((128, 128), Image.NEAREST).convert("RGB").save(
        ROOT / "build/labrys_seal_8x.png")
    print(OUT)


if __name__ == "__main__":
    main()
