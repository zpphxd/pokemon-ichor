#!/usr/bin/env python3
"""Write the walk grids of Emporion's two maps as a Lua table for emporion.lua.

A cell is open when its blockdata is passable and dry, nobody stands on it for
good (people who wander or walk, and the cast that leaves, are left out: the
test steps round them), and it isn't a coord trigger (stepped on on purpose).

Usage: tools/ichor/tests/emporion_grids.py > build/emporion_test/grids.lua
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
MAPS = {"MAP_CITY": "EmporionCity", "MAP_HARBOR": "EmporionHarbor"}
MOVING = ("MOVEMENT_TYPE_WANDER_AROUND", "MOVEMENT_TYPE_WALK_LEFT_AND_RIGHT")
TRANSIENT = ("KLEON", "ALETHEA", "KERYKOS", "NUMBER_NINE", "HARPECK")


def grid(name):
    ev = json.loads((ROOT / "data/maps" / name / "map.json").read_text())
    lay = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    entry = next(l for l in lay["layouts"] if l.get("id") == ev["layout"])
    w = entry["width"]
    b = np.fromfile(ROOT / "data/layouts" / name / "map.bin", "<u2").reshape(-1, w)
    open_ = (((b >> 10) & 3) == 0) & ((b >> 12) != 1)
    for o in ev["object_events"]:
        if o["movement_type"] in MOVING:
            continue
        if any(t in o.get("local_id", "") for t in TRANSIENT):
            continue
        if 0 <= o["y"] < b.shape[0] and 0 <= o["x"] < w:
            open_[o["y"], o["x"]] = False
    # coord triggers are stepped on on purpose, never on the way somewhere else
    for t in ev["coord_events"]:
        open_[t["y"], t["x"]] = False
    return open_


def main():
    out = ["return {"]
    for key, name in MAPS.items():
        g = grid(name)
        rows = ", ".join('"' + "".join("." if c else "#" for c in row) + '"' for row in g)
        out.append(f"  {key} = {{ {rows} }},")
    out.append("}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
