#!/usr/bin/env python3
"""The Labyrinth's upper rings: Ring I (the Threshold), Ring II (the Runner's
Ring), Ring III (the Mysteries), Daedalus's workshop, Ring IV (the Masks) and
Minos's tomb (design/LABYRINTH.md §6, design/LABYRINTH_MAZE.md,
design/maps/Labyrinth_System.md).

Each ring is a braided maze on labyrinth_lib's coarse grid, with its chambers
stamped first and its puzzle placed by measuring the walk: Ring I's braziers
sit at dead ends chosen so the threshold fire's 30 steps reach each in turn
only the right way round.

  /usr/bin/python3 tools/ichor/maps/labyrinth_upper.py [ring1 ring2 ring3 workshop ring4 tomb] [--no-render] [--plan]
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from labyrinth_lib import LMap, Maze, PITCH, cell, mid, ST  # noqa: E402
from kythera_maps import DIRS4  # noqa: E402

DARK = {"requires_flash": True, "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_UNDERGROUND",
        "show_map_name": True, "allow_cycling": False, "allow_running": True, "allow_escaping": False,
        "region_map_section": "MAPSEC_WATER_LABYRINTH", "music": "MUS_ICHOR_HOLLOW"}


def bfs(m, start, extra=(), blocked=()):
    """Walk distances from start over walkable cells."""
    blocked = set(blocked)
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in DIRS4:
            n = (x + dx, y + dy)
            if n in dist or n in blocked:
                continue
            if not (m.walkable(*n, extra) or n in extra):
                continue
            dist[n] = dist[(x, y)] + 1
            q.append(n)
    return dist


def report(name, maze, m, reach):
    met = maze.metrics()
    screens = m.w * m.h / 150
    print(f"{name}: {screens:.1f} screens; graph {met['nodes']} nodes, {met['edges']} edges, "
          f"{met['loops']} loops, {met['junctions']} junctions ({met['junctions'] / screens:.1f}/screen), "
          f"{met['dead_ends']} dead ends, {len(reach)} walkable cells")
    return met
