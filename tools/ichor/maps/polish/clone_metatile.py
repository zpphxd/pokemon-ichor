#!/usr/bin/env python3
"""Clone a secondary metatile into a free slot with a new behavior.

Writes both the Porytiles sources (the three layer PNGs and attributes.csv)
and the compiled porytiles_bin (metatiles.bin, metatile_attributes.bin), so a
later recompile from source gives the same result. The clone reuses the
original's tiles and palettes; only its behavior differs.

  clone_metatile.py arkadia 0x23B 0x237 MB_JUMP_SOUTH
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools/ichor"))
from mapdata import Repo  # noqa: E402

name, src, dst, behavior = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16), sys.argv[4]
d = ROOT / "data/tilesets/secondary" / name
s, t = src - 0x200, dst - 0x200
mb = {v: k for k, v in Repo().mb.items()}[behavior]

# compiled
mt = bytearray((d / "porytiles_bin/metatiles.bin").read_bytes())
at = bytearray((d / "porytiles_bin/metatile_attributes.bin").read_bytes())
assert t * 16 + 16 <= len(mt), "slot past the end of the tileset"
assert not any(mt[t * 16:t * 16 + 16]), f"slot {dst:#x} is not free"
mt[t * 16:t * 16 + 16] = mt[s * 16:s * 16 + 16]
attr = int.from_bytes(at[s * 2:s * 2 + 2], "little")
attr = (attr & ~0xFF) | mb
at[t * 2:t * 2 + 2] = attr.to_bytes(2, "little")
(d / "porytiles_bin/metatiles.bin").write_bytes(bytes(mt))
(d / "porytiles_bin/metatile_attributes.bin").write_bytes(bytes(at))

# source
for layer in ("bottom", "middle", "top"):
    p = d / "porytiles_src" / f"{layer}.png"
    im = Image.open(p)
    box = lambda i: ((i % 8) * 16, (i // 8) * 16, (i % 8) * 16 + 16, (i // 8) * 16 + 16)  # noqa: E731
    im.paste(im.crop(box(s)), box(t)[:2])
    im.save(p)
csv = d / "porytiles_src/attributes.csv"
lines = [l for l in csv.read_text().splitlines() if l and not l.startswith(f"{t},")]
lines.append(f"{t},{behavior}")
csv.write_text("\n".join(lines) + "\n")
print(f"{name}: {src:#x} -> {dst:#x} as {behavior}")
