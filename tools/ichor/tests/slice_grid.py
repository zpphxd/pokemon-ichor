#!/usr/bin/env python3
"""Print a map's walk grid: one cell per tile, as the game sees it.

  tools/ichor/tests/slice_grid.py AktiTown_Asclepeion

Each cell is two characters: the first is '#' for a collision cell, '~' for
water, a ledge arrow (v ^ < >), or '.'; the second is the elevation (0-F).
Objects show as 'O', warps as 'W', coord triggers as 'T' in the first character.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).parent))
from slice_map_audit import Map, behaviors  # noqa: E402


def main():
    name = sys.argv[1]
    mb = behaviors()
    layouts = {l["id"]: l for l in json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"] if "id" in l}
    m = Map(name, layouts, mb)
    marks = {}
    for o in m.json.get("object_events", []):
        marks[(o["x"], o["y"])] = "O"
    for w in m.json.get("warp_events", []):
        marks[(w["x"], w["y"])] = "W"
    for c in m.json.get("coord_events", []):
        marks.setdefault((c["x"], c["y"]), "T")
    print("    " + "".join(f"{x:<2d}"[-2:] if x % 5 == 0 else "  " for x in range(m.w)))
    for y in range(m.h):
        row = []
        for x in range(m.w):
            mid, col, elev = m.cell(x, y)
            b = m.behavior(mid)
            ch = "#" if col else "~" if "WATER" in b else {"MB_JUMP_SOUTH": "v", "MB_JUMP_NORTH": "^",
                                                            "MB_JUMP_WEST": "<", "MB_JUMP_EAST": ">"}.get(b, ".")
            row.append(marks.get((x, y), ch) + "%X" % elev)
        print(f"{y:3d} " + "".join(row))


if __name__ == "__main__":
    main()
