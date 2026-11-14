#!/usr/bin/env python3
"""Check that aethos's tiles fit the primary's 6 palettes x 15 colors.

Porytiles packs palettes itself, but when packing fails it can't say why.
This lists every distinct tile color set (anim tiles take the union over
their frames), packs them greedily the way a human would, and reports the
sets that don't fit, so painters can trim colors before compiling.

Usage: /usr/bin/python3 tools/ichor/art/aethos_palcheck.py
"""
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aethos_lib import PAL, ALIASES, load_rgba, split_tiles, ANIMS, OUT  # noqa: E402

NAMES = {v: k for k, v in PAL.items() if k not in ALIASES}


def colorsets():
    sets = Counter()
    for n in ("bottom", "middle", "top"):
        for t in split_tiles(load_rgba(OUT / f"{n}.png")):
            c = frozenset(tuple(int(v) for v in p) for p in t[t[..., 3] > 0][:, :3])
            if c:
                sets[c] += 1
    for name in ANIMS:
        d = OUT / "anim" / name
        frames = [split_tiles(load_rgba(p)) for p in sorted(d.glob("*.png"))]
        for i in range(len(frames[0])):
            c = set()
            for f in frames:
                t = f[i]
                c |= {tuple(int(v) for v in p) for p in t[t[..., 3] > 0][:, :3]}
            if c:
                sets[frozenset(c)] += 1
    return sets


def pack(sets, npal=6, size=15):
    """Greedy: biggest sets first, each into the palette it grows least."""
    pals = [set() for _ in range(npal)]
    failed = []
    for s in sorted(sets, key=lambda s: -len(s)):
        best = None
        for p in pals:
            if s <= p:
                best = p
                break
            grow = len(s - p)
            if len(p) + grow <= size and (best is None or grow < len(s - best)):
                best = p
        if best is None:
            failed.append(s)
        else:
            best |= s
    return pals, failed


def name(c):
    return NAMES.get(c, str(c))


def main():
    sets = colorsets()
    allc = set().union(*sets)
    print(f"{len(sets)} distinct tile color sets, {len(allc)} colors in all")
    big = [s for s in sets if len(s) > 15]
    for s in big:
        print("  TOO MANY COLORS:", len(s), sorted(name(c) for c in s))
    # drop subsets
    maximal = [s for s in sets if not any(s < o for o in sets)]
    pals, failed = pack(maximal)
    for i, p in enumerate(pals):
        print(f"pal {i} ({len(p)}):", " ".join(sorted(name(c) for c in p)))
    for s in failed:
        print("  DOES NOT FIT:", len(s), " ".join(sorted(name(c) for c in s)))
    return 1 if failed or big else 0


if __name__ == "__main__":
    sys.exit(main())
