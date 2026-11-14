#!/usr/bin/env python3
"""Akti's field objects: Diktys's upturned boat, as two 16x16 object halves.

Akti's bottom six rows sit on the Route 1 seam, and the engine draws a
connected map with the tilesets of the map the player stands on. From Route 1
any gTileset_Akti metatile there turns to garbage, so those rows may use only
aethos metatiles (MAP_DESIGN.md §5). Diktys's boat by the south gate is drawn
as object events instead, which look the same from either side.

The art is akti_harbor.upturned_boat(), moved into the "Ichor cast" OBJ palette
(each color to its nearest cast color), so it costs no extra palette slot on a
map that already shows the cast. Two halves, so each sits square on its cell.

Usage: /usr/bin/python3 tools/ichor/art/akti_objects.py [--write] [--preview out.png]
  --write   graphics/object_events/pics/misc/ichor/upturned_boat_l.png and _r.png
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, save_indexed, to_rgba, upscale  # noqa: E402
from sprites_npc import CAST_PAL  # noqa: E402
import akti_lib  # noqa: E402,F401  (registers Akti's colors with kalliste_lib)
import akti_harbor  # noqa: E402

OUT_DIR = os.path.join(ROOT, "graphics/object_events/pics/misc/ichor")


def boat_indexed():
    """The upturned boat (32x16) as indices into the cast palette."""
    a = akti_harbor.upturned_boat().M.a
    cols = np.array(CAST_PAL.colors[1:], float)
    out = np.zeros(a.shape[:2], np.int32)
    for y, x in zip(*np.nonzero(a[..., 3])):
        d = ((cols - a[y, x, :3]) ** 2).sum(1)
        out[y, x] = 1 + int(d.argmin())
    return out


def halves():
    arr = boat_indexed()
    return {"upturned_boat_l": arr[:, :16], "upturned_boat_r": arr[:, 16:]}


def main():
    args = sys.argv[1:]
    parts = halves()
    if "--write" in args:
        for name, arr in parts.items():
            path = os.path.join(OUT_DIR, name + ".png")
            save_indexed(arr, CAST_PAL, path)
            print(path)
    if "--preview" in args:
        from PIL import Image
        grass = Image.new("RGBA", (32, 16), (184, 184, 104, 255))
        grass.alpha_composite(to_rgba(np.hstack([parts["upturned_boat_l"], parts["upturned_boat_r"]]),
                                      CAST_PAL))
        out = args[args.index("--preview") + 1]
        upscale(grass, 8).save(out)
        print(out)


if __name__ == "__main__":
    main()
