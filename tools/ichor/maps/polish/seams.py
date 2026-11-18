#!/usr/bin/env python3
"""Aethos-only seam strips for the polished Arkadian climb (MAP_DESIGN.md 'Seam strips').

A connected neighbour is drawn with the tilesets of the map the player stands
on, so the cells a player can see across a seam must look the same under both
maps' tilesets (tools/ichor/seam_audit.py checks it). These passes redraw those
strips from Aethos. Each one sets every cell it owns outright, so it can run any
number of times; styx.py and route12.py call them last, and running this file
applies them to the committed maps:

  styx_north     Styx Falls rows 0-5, under Route 11 (Skiron): the drum pass's
                 cypress road comes down between cypress walls to the cliff gap.
  route12_north  Route 12 rows 4-5 x8-15, seen from Styx Falls' south road
                 (styx_falls shares Kyllene's 0x200-0x2A7, not its tall grass
                 edges or piled stone).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mapedit import Layout  # noqa: E402

GRASS, TALL, BOULDER = 0x001, 0x00D, 0x0E0
CY_TOP, CY_BOT = 0x00E, 0x016
PINE = ((0x01E, 0x01F), (0x026, 0x027))
PATH_W, PATH_E = 0x1D8, 0x1DA         # a two-wide road's west and east halves (Route 11's)


def styx_north(m):
    """Rows 0-5. The road (x12-13) runs down from Route 11 (its x11-12) between
    cypress walls (x10-11, x14-15) to the gap in the cliff at row 6; the two
    clearings either side of the gap stay open grass (x8-10 and x15-17, row 5;
    x9 and x16, row 4); the rest is cypress and stone pine woods, as on Route 11's
    last rows."""
    open_cells = {(9, 4), (16, 4), (8, 5), (9, 5), (10, 5), (15, 5), (16, 5), (17, 5)}
    rocks = {(8, 4), (10, 4), (15, 4), (17, 4)}
    # stone pines, 2x2 on the pair rows 0-1, 2-3 and 4-5, about one woods block
    # in three (a fixed hash, so the pass repeats); the rest cypress pairs
    keep = open_cells | rocks | {(x, y) for y in range(6) for x in range(10, 16)}
    placed = set()
    for py in (0, 2, 4):
        for px in range(0, m.w - 1):
            cells = {(px + i, py + j) for j in range(2) for i in range(2)}
            if cells & (keep | placed) or (px * 7 + py * 13 + px * py) % 11 >= 4:
                continue
            for x, y in cells:
                m.put(x, y, PINE[y - py][x - px], solid=True)
            placed |= cells
    for y in range(6):
        for x in range(m.w):
            if (x, y) in placed:
                continue
            if x == 12:
                m.put(x, y, PATH_W, solid=False)
            elif x == 13:
                m.put(x, y, PATH_E, solid=False)
            elif (x, y) in open_cells:
                m.put(x, y, GRASS, solid=False)
            elif (x, y) in rocks:
                m.put(x, y, BOULDER, solid=True)
            else:
                m.put(x, y, CY_TOP if y % 2 == 0 else CY_BOT, solid=True)


def route12_north(m):
    """The meadow's tall grass along rows 4-5 (x8-14) is Aethos tall grass, and the
    piled stone at (15,5) an Aethos boulder; rows 6-7 keep their edged grass."""
    for y in (4, 5):
        for x in range(8, 15):
            if m.id(x, y) >= 0x200:       # Kyllene's edged tall grass
                m.put(x, y, TALL, solid=False)
    m.put(15, 5, BOULDER, solid=True)


def main():
    for name, fn in (("StyxFalls", styx_north), ("Route12_CypressRoad", route12_north)):
        m = Layout(name)
        fn(m)
        m.save()
        print(f"seams: {name}")


if __name__ == "__main__":
    main()
