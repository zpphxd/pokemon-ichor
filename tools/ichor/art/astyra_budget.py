#!/usr/bin/env python3
"""Tile budget per structure for gTileset_Astyra and gTileset_Akropolis: how
many distinct 8x8 tiles (up to flips) each structure draws, and how many of
those no other structure shares (what cutting it would free). Counted before
near-duplicate merging, so the totals run a little over the compiled count.

    /usr/bin/python3 tools/ichor/art/astyra_budget.py [akropolis|astyra]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import astyra_build as AB  # noqa: E402
import kythera_lib as K  # noqa: E402


def main():
    for name in sys.argv[1:] or AB.NAMES:
        sp = AB.spec(name)
        structs = [s for _, ss in sp["sections"] for s in ss]
        occ = K.tiles_of(structs)
        own = {}
        for t, where in occ.items():
            keys = {w[0] for w in where}
            for k in keys:
                own.setdefault(k, [0, 0])[0] += 1
                if len(keys) == 1:
                    own[k][1] += 1
        print(f"{name}: {len(occ)} distinct tiles before merging, "
              f"{sum(s.w * s.h for s in structs)} cells")
        for s in sorted(structs, key=lambda s: -own.get(s.key, [0, 0])[1]):
            a, b = own.get(s.key, [0, 0])
            print(f"  {s.key:22s} {s.w:2d}x{s.h:<2d} tiles {a:4d}  unique {b:4d}")


if __name__ == "__main__":
    main()
