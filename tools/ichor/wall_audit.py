#!/usr/bin/env python3
"""Fail on invisible walls: blocked cells that look like open ground, and objects that can't draw.

1. A cell with collision set whose metatile is plain floor (MB_NORMAL or a grass
   behavior) that is walkable in at least 3 of every 4 places Ichor's maps use it,
   while a neighbouring cell with the same metatile is walkable and reachable. It looks like the ground the player is standing on, so the stop
   reads as an invisible wall. Cells under an object are skipped: the object is
   what blocks there.
2. An object event whose graphics id has no graphics info (or isn't a var
   graphics id, or an OBJ_EVENT_GFX_SPECIES of a defined species), so it blocks
   a cell without drawing.

Usage: wall_audit.py [-v]   exit 1 on any finding.
"""
import re
import sys
from collections import Counter

from mapdata import UPSTREAM_PREFIXES, Map, Repo, Walker, entries

FLOOR = {"MB_NORMAL", "MB_TALL_GRASS", "MB_LONG_GRASS", "MB_SHORT_GRASS", "MB_ASHGRASS", "MB_SAND"}


def gfx_ids(repo):
    ptrs = (repo.root / "src/data/object_events/object_event_graphics_info_pointers.h").read_text()
    have = set(re.findall(r"\[(OBJ_EVENT_GFX_\w+)\]\s*=", ptrs))
    consts = (repo.root / "include/constants/event_objects.h").read_text()
    have |= set(re.findall(r"#define (OBJ_EVENT_GFX_VAR_\w+)", consts))
    species = (repo.root / "include/constants/species.h").read_text()
    have |= {f"OBJ_EVENT_GFX_SPECIES({s})" for s in re.findall(r"\bSPECIES_(\w+)", species)}
    return have


def floor_ids(repo, names):
    """Metatiles that are open ground almost everywhere they are used: primary ids, or (secondary, id)."""
    free, blk = Counter(), Counter()
    for name in names:
        m = Map(repo, name)
        sec = repo.layouts[m.json["layout"]]["secondary_tileset"]
        for v in m.cells:
            mid = v & 0x3FF
            key = mid if mid < 0x200 else (sec, mid)
            (blk if (v >> 10) & 3 else free)[key] += 1
    return {k for k in free if free[k] >= 3 * blk[k]}


def walls(m, floor):
    sec = m.repo.layouts[m.json["layout"]]["secondary_tileset"]
    w = Walker(m)
    starts = [s for _, tiles in entries(m) for s in w.starts(tiles)]
    reach = {(x, y) for x, y, _ in w.reach(starts)} if starts else set()
    objs = {(o["x"], o["y"]) for o in m.objects}
    out = []
    for y in range(m.h):
        for x in range(m.w):
            mid, col, _ = m.cell(x, y)
            key = mid if mid < 0x200 else (sec, mid)
            if not col or (x, y) in objs or m.behavior(mid) not in FLOOR or key not in floor:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c = m.cell(x + dx, y + dy)
                if c and c[0] == mid and not c[1] and (x + dx, y + dy) in reach:
                    out.append((x, y, mid))
                    break
    return out


def main(argv):
    repo = Repo()
    gfx = gfx_ids(repo)
    names = [n for n in repo.names if not n.startswith(UPSTREAM_PREFIXES)]
    floor = floor_ids(repo, names)
    fails = 0
    for name in names:
        m = Map(repo, name)
        bad = walls(m, floor)
        if bad:
            fails += 1
            shown = bad if "-v" in argv else bad[:8]
            print(f"WALL FAIL: {name}: {len(bad)} blocked floor cells beside walkable ones: "
                  + ", ".join(f"({x},{y})=0x{v:03X}" for x, y, v in shown) + (" ..." if len(shown) < len(bad) else ""))
        for i, o in enumerate(m.objects):
            g = o.get("graphics_id", "")
            if g not in gfx:
                fails += 1
                print(f"WALL FAIL: {name}: object {i} at ({o.get('x')},{o.get('y')}) has no graphics ({g!r})")
    if not fails:
        print("wall_audit: no invisible walls, every object draws")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
