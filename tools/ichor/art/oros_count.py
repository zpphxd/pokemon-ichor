#!/usr/bin/env python3
"""Count gTileset_Oros's distinct 8x8 tiles (flips folded), piece by piece, so
the 504-tile budget can be watched while drawing. Usage: oros_count.py [oros|propylon] [--all]"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pantheon_lib as P  # noqa: E402
import oros_art as art  # noqa: E402


def tiles_of(s):
    for n in ("bottom", "middle", "top"):
        a = s.layers[n].a
        for ty in range(s.h * 2):
            for tx in range(s.w * 2):
                t = a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                if not t[..., 3].any():
                    continue
                forms = [t, t[:, ::-1], t[::-1, :], t[::-1, ::-1]]
                yield min(f.tobytes() for f in forms)


def main():
    P.use(art.C, art.GROUPS)
    seen = set()
    which = next((a for a in sys.argv[1:] if not a.startswith('-')), 'oros')
    for sec, structs in art.sections(which):
        start = len(seen)
        for s in structs:
            before = len(seen)
            seen.update(tiles_of(s))
            if "--all" in sys.argv:
                print(f"  {s.key:28s} +{len(seen) - before}")
        print(f"{sec}: +{len(seen) - start} (total {len(seen)})")


if __name__ == "__main__":
    main()
