"""Hand-edited ASCII pixel sources for Ichor's sprites.

Each sprite source is a text file in tools/ichor/art/src/:

    # comment lines
    palette:
    k ink 32 24 24          one char, a name and an RGB (multiples of 8)
    ...
    origin: X Y             where the first character of the art lands
    art:
    ....kkkk....            '.' is transparent

The art block is the canonical, hand-editable pixel data. The shape scripts
(sprites_trainers.py and friends) can draft a starting point with --dump,
which writes a source file to edit by hand.

Usage:
    python3 tools/ichor/art/sprites_ascii.py SRC.txt OUT.png [--size W H]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import Palette, save_indexed  # noqa: E402

SRC_DIR = os.path.join(os.path.dirname(__file__), "src")


def load(path, size=(64, 64)):
    """Returns (index array, Palette, chars->name)."""
    named, chars = [], {}
    origin = (0, 0)
    art = []
    mode = None
    with open(path) as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if mode != "art" and (not line.strip() or line.lstrip().startswith("#")):
                continue
            if line.startswith("palette:"):
                mode = "pal"
                continue
            if line.startswith("origin:"):
                origin = tuple(int(v) for v in line.split()[1:3])
                continue
            if line.startswith("size:"):
                size = tuple(int(v) for v in line.split()[1:3])
                continue
            if line.startswith("art:"):
                mode = "art"
                continue
            if mode == "pal":
                ch, name, r, g, b = line.split()[:5]
                named.append((name, (int(r), int(g), int(b))))
                chars[ch] = name
            elif mode == "art":
                art.append(line)
    pal = Palette(named)
    w, h = size
    arr = np.zeros((h, w), np.int32)
    ox, oy = origin
    for j, row in enumerate(art):
        for i, ch in enumerate(row):
            if ch in ". ":
                continue
            if ch not in chars:
                raise ValueError(f"{path}: unknown char {ch!r} at row {j} col {i}")
            arr[oy + j, ox + i] = pal[chars[ch]]
    return arr, pal, chars


def dump(arr, pal, chars, path, comment="", crop=None):
    """Writes an editable source; chars maps one char -> palette name."""
    inv = {name: ch for ch, name in chars.items()}
    ys, xs = np.nonzero(arr)
    if crop is None:
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    else:
        x0, y0, x1, y1 = crop
    with open(path, "w") as fh:
        if comment:
            for c in comment.splitlines():
                fh.write("# " + c + "\n")
        fh.write("size: %d %d\n" % (arr.shape[1], arr.shape[0]))
        fh.write("palette:\n")
        for i in range(1, 16):
            name = pal.names[i]
            if name.startswith("_pad"):
                continue
            fh.write("%s %-8s %3d %3d %3d\n" % ((inv[name], name) + pal.colors[i]))
        fh.write("origin: %d %d\n" % (x0, y0))
        fh.write("art:\n")
        for y in range(y0, y1 + 1):
            row = "".join("." if arr[y, x] == 0 else inv[pal.names[arr[y, x]]] for x in range(x0, x1 + 1))
            fh.write(row.rstrip(".") + "\n")


def main():
    src, out = sys.argv[1], sys.argv[2]
    arr, pal, _ = load(src)
    save_indexed(arr, pal, out)


if __name__ == "__main__":
    main()
