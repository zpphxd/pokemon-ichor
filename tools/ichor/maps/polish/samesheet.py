#!/usr/bin/env python3
"""Which secondary metatile ids draw the same in two tilesets (for seam strips).

  samesheet.py kyllene styx_falls
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[4]


def load(name):
    d = ROOT / "data/tilesets/secondary" / name / "porytiles_bin"
    mt = (d / "metatiles.bin").read_bytes()
    tiles = Image.open(d / "tiles.png")
    pals = []
    for i in range(16):
        p = d / "palettes" / f"{i:02}.pal"
        pals.append(p.read_text().split("\n")[3:19] if p.exists() else [])
    return mt, tiles, pals


def tile_px(tiles, idx):
    w = tiles.width // 8
    x, y = (idx % w) * 8, (idx // w) * 8
    return tuple(tiles.crop((x, y, x + 8, y + 8)).getdata()) if y < tiles.height else None


def meta(mt, tiles, pals, i):
    out = []
    for k in range(8):
        v = int.from_bytes(mt[i * 16 + k * 2: i * 16 + k * 2 + 2], "little")
        t, pal = v & 0x3FF, v >> 12
        if t >= 512:
            px = tile_px(tiles, t - 512)
            px = tuple(pals[pal][c] if c < len(pals[pal]) else c for c in px) if px else None
        else:
            px = ("prim", t, pal)
        out.append((px, v & 0xC00))
    return tuple(out)


a, b = load(sys.argv[1]), load(sys.argv[2])
n = min(len(a[0]), len(b[0])) // 16
same = [0x200 + i for i in range(n) if meta(*a, i) == meta(*b, i)]
print(len(same), "of", n, "the same")
print(" ".join(f"{i:03X}" for i in same))
