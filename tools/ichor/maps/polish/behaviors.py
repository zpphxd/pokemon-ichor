#!/usr/bin/env python3
"""List each tileset's metatiles by behavior (everything but MB_NORMAL).

  behaviors.py gTileset_Aethos gTileset_Kyllene
"""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from mapdata import Repo  # noqa: E402

r = Repo()
for ts in sys.argv[1:]:
    a = r.attrs(ts)
    base = 0 if ts in ("gTileset_Aethos", "gTileset_Oikos") else 0x200
    d = defaultdict(list)
    for i, v in enumerate(a):
        d[r.mb.get(v & 0xFF, "?")].append(f"{base + i:03X}")
    print(ts)
    for k, v in sorted(d.items()):
        if k != "MB_NORMAL":
            print(f"  {k:32} {len(v):3}  {' '.join(v[:24])}")
