#!/usr/bin/env python3
"""The Temple of Hermes map: the Herald's Run, its acolytes and Kerykos's dais.

The room is design/phase2/SCRIPT.md Part 5's switchback stoa, drawn with the
temple_hermes tileset (design/phase2/TILES_temple_hermes.md) on oikos. ROOM below is
the design, one character per cell; this script turns it into
LAYOUT_EMPORION_CITY_TEMPLE_OF_HERMES, writes the map's events and the room-drawing
scripts, solves the puzzle and checks it.

1. Writes data/layouts/EmporionCity_TempleOfHermes/map.bin and border.bin, the
   layout's size in layouts.json, the METATILE_TempleHermes_* labels in
   include/constants/metatile_labels.h, and data/maps/EmporionCity_TempleOfHermes/
   map.json (every person, warp, step counter, turnstile and sign).
2. Writes the generated block of scripts.pory (between two markers): the scripts that
   draw the room from the run's state, and one script per turnstile.
3. Solves the run as a directed graph (a turnstile passes one way and carries you
   through), and checks:
   - every leg (door to H1, H1 to H2, H2 to H3, H3 to Kerykos) has a route, its length,
     and the cost of each wrong turnstile (the loops);
   - each junction herm's pointing direction is the first step of the shortest route;
   - no softlock: from every reachable tile the door can be reached, before the run,
     during it and after it;
   - every walkable tile on the run has a step counter, and the map has at most 255
     coord events (the engine's u8 count);
   - the people stand on walkable tiles, Podarge and Euchidas see the route, and
     Philonides sees nothing (he is optional).
4. Renders, in design/phase2/img/ (from the compiled tileset, as the game draws it,
   with the people's walkers composited):
   temple_hermes.png         the room before the run, at 2x
   temple_hermes_solved.png  after the Laurel: the gate open, every herm facing the dais
   temple_hermes_events.png  2x plan: people, sight, warps, turnstiles, the route
   temple_hermes_views.png   GBA-screen-sized views (15 x 10 tiles) along the route, 2x
   temple_hermes_stages.png  the room at each stage of the run, 1x

Usage: /usr/bin/python3 tools/ichor/maps/temple_hermes.py [--check] [--report]
  --check verifies the generated files are current and writes nothing.
  --report prints the solver's legs and loops.
Needs build/temple_hermes/catalog.json:
  /usr/bin/python3 tools/ichor/art/emporion_build.py temple_hermes
"""
import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
import render_map  # noqa: E402

LAYOUT_ID = "LAYOUT_EMPORION_CITY_TEMPLE_OF_HERMES"
MAP_ID = "MAP_EMPORION_CITY_TEMPLE_OF_HERMES"
LAYOUT_DIR = ROOT / "data/layouts/EmporionCity_TempleOfHermes"
MAP_DIR = ROOT / "data/maps/EmporionCity_TempleOfHermes"
CATALOG = ROOT / "build/temple_hermes/catalog.json"
LABELS = ROOT / "include/constants/metatile_labels.h"
IMG = ROOT / "design/phase2/img"
PREFIX = "EmporionCity_TempleOfHermes_EventScript_"

# The door mat's warps lead to Emporion. ICHOR placeholder: the city's temple door
# warp id is fixed at merge (the city is built in parallel).
CITY_DEST_WARP_ID = "0"

# --- The design ----------------------------------------------------------------------
# One character per cell.
#   #  wall (the top three rows and the side columns are drawn from their position)
#   .  marble floor            =  balustrade (joins itself)       V  void   M  door mat
#   R  riser (a terrace's face) S  steps through a riser          G  the dais gate
#   > < ^ v  a one-way turnstile, passed in the chevron's direction
#   D  dais floor   O  the roundel under Kerykos   L  the lectern   l  a dais lamp
#   C c  a column (top, bottom)   A a s  the statue of Hermes (top, middle, plinth)
#   T t  a relay torch (bowl, stand)   Y y  the step-glass (glass, stand)   o  oil jar
#   K k  Kerykos's table of scrolls (left, right)   P p Q q  a pigeonhole cabinet
#   1-4  junction herm J1-J4's head   5-7  herald-herm H1-H3's head   |  a herm's shaft
#   m  the caduceus mosaic's top-left (a 2 x 2, walkable)
ROOM = """
#####################
#####################
#####################
#DPQDDDDADODADDDDPQD#
#DpqDTDDaDLDaDDTDpqD#
#DDDDtDDsDDDsDDtDDDD#
#=========G=========#
#RRRRRRRRRSRRRRRRRRR#
#7....<.............#
#|v=====C====C====.4#
#=......c....c..<..|#
#...............>...#
#RRvRRRRRRRRRRRRRRSR#
#...>.......<.......#
#3..==C===.===C==...#
#|..<.c.......c.>..6#
#...=...........=..|#
#R^vRRRRRRRRRRRRRRRR#
#2..............<...#
#|v===.YKk...1.=...5#
#..PQ=.y.o...|.=...|#
#..pq=.........>....#
#....>.........=....#
VVVVVVVVVMMMVVVVVVVVV
"""

HERMS = {"1": "J1", "2": "J2", "3": "J3", "4": "J4", "5": "H1", "6": "H2", "7": "H3"}
JUNCTIONS = ["J1", "J2", "J3", "J4"]
HERALDS = ["H1", "H2", "H3"]
# Where the player stands to read each junction herm: the head points along the first
# step of the shortest route from here. Each is beside the herm, at the fork.
READ_AT = {"J1": (13, 21), "J2": (2, 18), "J3": (2, 14), "J4": (18, 10)}
# Turnstiles that turn round when the third scroll is delivered (the upper colonnade).
REVERSING = {(6, 8), (16, 10), (16, 11)}
DOOR = (10, 23)           # warp 0, the middle of the mat: where the player arrives
ENTRANCE = (10, 22)       # where a failed run puts the player back
KERYKOS_PORCH = (8, 20)   # by the oil jar, before the run
KERYKOS_DAIS = (10, 3)    # on the roundel, behind the lectern
TALK_DAIS = (10, 5)       # the player's tile across the lectern
RUN_START = (8, 21)       # the player's tile when Kerykos hands over the scrolls
DAIS_ROWS = range(3, 6)   # the dais: closed during the run, so no step counters

# People: local id, graphics, x, y, facing, trainer sight (0 = not a trainer), script, flag.
PEOPLE = [
    ("LOCALID_HERMES_KERYKOS", "OBJ_EVENT_GFX_ICHOR_KERYKOS", *KERYKOS_PORCH, "down", 0, "Kerykos", "FLAG_TEMP_4"),
    ("LOCALID_HERMES_ANGELOS", "OBJ_EVENT_GFX_ICHOR_YOUTH_M", 12, 22, "left", 0, "Angelos", "0"),
    ("LOCALID_HERMES_PODARGE", "OBJ_EVENT_GFX_ICHOR_ACOLYTE_F", 19, 21, "left", 3, "Podarge", "0"),
    ("LOCALID_HERMES_EUCHIDAS", "OBJ_EVENT_GFX_ICHOR_ACOLYTE_M", 7, 15, "right", 4, "Euchidas", "0"),
    ("LOCALID_HERMES_PHILONIDES", "OBJ_EVENT_GFX_ICHOR_ACOLYTE_M", 4, 10, "up", 1, "Philonides", "0"),
]
MANDATORY = {"Podarge", "Euchidas"}

# Signs: bg events on blocking cells, by the ROOM character there.
SIGNS = {"Y": "StepGlass", "y": "StepGlass", "o": "OilJar", "K": "ScrollTable", "k": "ScrollTable",
         "A": "Altar", "a": "Altar", "s": "Altar", "P": "Pigeonholes", "Q": "Pigeonholes",
         "p": "Pigeonholes", "q": "Pigeonholes"}
FRIEZE_SIGNS = [(5, 2), (15, 2)]   # the lower wall under the running figures, read from the dais

# The frieze row: one motif per column, Hermes running across the middle.
FRIEZE = {2: "frieze_caduceus", 4: "frieze_petasos", 6: "frieze_talaria", 8: "frieze_wings",
          9: "frieze_runner_l", 10: "frieze_runner_r", 11: "frieze_wings", 13: "frieze_lyre",
          15: "frieze_petasos", 17: "frieze_caduceus"}
LOWER_WALL = {4: "lower_torch", 16: "lower_torch", 7: "lower_niche", 13: "lower_niche"}

# Floor scatter: a veined or worn slab here and there, fixed so the room never changes.
SCATTER = {(3, 10): "vein_a", (12, 11): "vein_b", (8, 13): "vein_a", (14, 16): "vein_b",
           (6, 18): "vein_a", (12, 19): "vein_b", (17, 22): "vein_a", (2, 22): "vein_b",
           (13, 8): "worn", (10, 15): "worn", (10, 13): "worn", (8, 22): "wing", (14, 20): "wing",
           (9, 10): "vein_b", (17, 13): "vein_a"}
# The racetrack inlay: porphyry lanes in the floor (decoration, all walkable). The run
# starts at a sill in the porch, and its first lane leads to the first turnstile (the
# leg that teaches); each herald-herm stands at a turning post (the kampter), as the
# stadium's lanes turn at its far end.
LANES = {(9, 21): "start_v", (10, 21): "h", (11, 21): "h", (12, 21): "h", (13, 21): "h", (14, 21): "h",
         (18, 20): "post", (18, 15): "post", (2, 8): "post"}
# Every turnstile but the two drops out of side places has a porphyry chevron on its far
# side, pointing the way it turns, so its one way reads from a screen away.
NO_ARROW = {(3, 12), (2, 9)}

DIRS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
TURN_DIR = {">": "E", "<": "W", "^": "N", "v": "S"}
OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}
GAME_DIR = {"S": "DIR_SOUTH", "N": "DIR_NORTH", "W": "DIR_WEST", "E": "DIR_EAST"}
WORD = {"N": "Up", "S": "Down", "W": "Left", "E": "Right"}


def room_rows():
    rows = [r for r in ROOM.strip("\n").splitlines()]
    w = len(rows[0])
    for n, r in enumerate(rows):
        if len(r) != w:
            raise ValueError(f"ROOM row {n} is {len(r)} wide, expected {w}")
    return rows


ROWS = room_rows()
W, H = len(ROWS[0]), len(ROWS)


def cell(x, y):
    return ROWS[y][x] if 0 <= x < W and 0 <= y < H else "V"


def find(ch):
    return [(x, y) for y in range(H) for x in range(W) if ROWS[y][x] == ch]


HERM_HEAD = {name: find(ch)[0] for ch, name in HERMS.items()}
HERM_SHAFT = {name: (x, y + 1) for name, (x, y) in HERM_HEAD.items()}
TURNSTILES = {(x, y): TURN_DIR[ROWS[y][x]] for y in range(H) for x in range(W) if ROWS[y][x] in TURN_DIR}
GATE = find("G")[0]
TORCHES = find("T")    # left lit by H1, right by H2
GLASS = find("Y")[0]
TABLE = find("K")[0]


# --- The catalog -------------------------------------------------------------------------

def load_catalog():
    if not CATALOG.exists():
        sys.exit("temple_hermes: run /usr/bin/python3 tools/ichor/art/emporion_build.py temple_hermes first")
    ids, blocking, behaviors = {}, {}, {}
    for s in json.loads(CATALOG.read_text()):
        for part, (c, r) in s["names"].items():
            name = f"{s['key']}.{part}"
            ids[name] = s["ids"][r][c]
            blocking[name] = s["walk"][r][c] == "X"
            if f"{c},{r}" in s["behaviors"]:
                behaviors[name] = s["behaviors"][f"{c},{r}"]
    return ids, blocking, behaviors


# --- Drawing the grid ----------------------------------------------------------------------

BAL_ARMS = ["NS", "N", "S", "EW", "E", "W", "ES", "SW", "NE", "NW", "NES", "ESW", "NSW", "NEW", "NESW"]


def balustrade_piece(x, y, rows):
    joins = ""
    for d in "NESW":
        dx, dy = DIRS[d]
        n = rows[y + dy][x + dx] if 0 <= x + dx < W and 0 <= y + dy < H else "#"
        if n in "=G":
            joins += d
    # A run that meets the side wall ends in a pedestal against it.
    if not joins:
        return "balustrade.post"
    if joins in BAL_ARMS:
        return "balustrade." + joins
    raise ValueError(f"balustrade at ({x},{y}) joins {joins}")


def base_grid(state):
    """Metatile names for every cell in a given state of the run.

    state: dict(delivered=0-3, done=bool, badge=bool, running=bool, oiled=set of J names)
    """
    g = [[None] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            ch = ROWS[y][x]
            g[y][x] = cell_name(x, y, ch, state)
    # The caduceus mosaic, 2 x 2 from its top-left.
    for mx, my in find("m"):
        g[my][mx], g[my][mx + 1] = "rostrum.mosaic_tl", "rostrum.mosaic_tr"
        g[my + 1][mx], g[my + 1][mx + 1] = "rostrum.mosaic_bl", "rostrum.mosaic_br"
    for (x, y), name in LANES.items():
        g[y][x] = "lane." + name
    for (x, y), name in arrow_cells(state).items():
        g[y][x] = name
    return g


def arrow_cells(st):
    """The porphyry chevron on each turnstile's far side, in a given state."""
    out = {}
    for (x, y), d in TURNSTILES.items():
        if (x, y) in NO_ARROW:
            continue
        if st["done"] and (x, y) in REVERSING:
            d = OPPOSITE[d]
        dx, dy = DIRS[d]
        out[(x + dx, y + dy)] = "lane.arrow_" + d.lower()
    return out


def herm_head(name, state):
    """The head metatile of a herm in a given state."""
    oiled = name in state["oiled"]
    if state["done"]:
        return "herm.head_oiled_n" if oiled else "herm.head_n"
    if not oiled:
        return "herm.head_s"
    return "herm.head_oiled_" + POINTING[name][state["delivered"]].lower()


def cell_name(x, y, ch, state):
    if y == 0:
        if x == 0:
            return "wall.side_w"
        if x == W - 1:
            return "wall.side_e"
        if x == 1:
            return "wall.cornice_w"
        if x == W - 2:
            return "wall.cornice_e"
        return "wall.cornice_acro" if x == W // 2 else "wall.cornice"
    if ch == "#" and x == 0:
        return "wall.side_w"
    if ch == "#" and x == W - 1:
        return "wall.side_e"
    if y == 1:
        return "wall." + FRIEZE.get(x, "frieze")
    if y == 2:
        return "wall." + LOWER_WALL.get(x, "lower")
    if ch == "V":
        return "floor.void"
    if ch == "M":
        return {DOOR[0] - 1: "wall.mat_l", DOOR[0]: "wall.mat_m", DOOR[0] + 1: "wall.mat_r"}[x]
    if ch in ".m" or ch == "n":
        return "floor." + SCATTER.get((x, y), "slab") if ch == "." else "floor.slab"
    if ch == "=":
        return balustrade_piece(x, y, ROWS)
    if ch == "R":
        left, right = ROWS[y][x - 1], ROWS[y][x + 1]
        if left == "#":
            return "rostrum.riser_w"
        if right == "#":
            return "rostrum.riser_e"
        return "rostrum.riser"
    if ch == "S":
        return "rostrum.steps"
    if ch in TURN_DIR:
        d = TURNSTILES[(x, y)]
        if state["done"] and (x, y) in REVERSING:
            d = OPPOSITE[d]
        return "turnstile.turn_" + d.lower()
    if ch == "G":
        return "turnstile.gate_h_open" if state["done"] else "turnstile.gate_h_shut"
    if ch == "D":
        return "rostrum.dais"
    if ch == "O":
        return "rostrum.dais_roundel"
    if ch == "L":
        return "rostrum.lectern"
    if ch == "l":
        return "rostrum.dais_lamp"
    if ch == "C":
        return "column.col_top"
    if ch == "c":
        return "column.col_bot"
    if ch == "A":
        return "column.statue_top"
    if ch == "a":
        return "column.statue_mid"
    if ch == "s":
        return "column.statue_bot"
    if ch == "T":
        i = TORCHES.index((x, y))
        return "props.torch_lit" if state["done"] or state["delivered"] > i else "props.torch_cold"
    if ch == "t":
        return "props.torch_stand"
    if ch == "Y":
        return "props.floor" if state["badge"] else "props.glass_top"
    if ch == "y":
        return "props.glass_stand"
    if ch == "o":
        return "props.oil"
    if ch in "Kk":
        full = not state["running"] and not state["done"]
        side = "l" if ch == "K" else "r"
        return f"scroll_table.{'full' if full else 'empty'}_{side}"
    if ch in "PQpq":
        return "pigeonholes." + {"P": "cab_tl", "Q": "cab_tr", "p": "cab_bl", "q": "cab_br"}[ch]
    if ch in HERMS:
        return herm_head(HERMS[ch], state)
    if ch == "|":
        for name, (sx, sy) in HERM_SHAFT.items():
            if (sx, sy) == (x, y):
                if name in HERALDS and (state["done"] or state["delivered"] > HERALDS.index(name)):
                    return "herm.shaft_scroll"
                return "herm.shaft"
    raise ValueError(f"no metatile for {ch!r} at ({x},{y})")


STATE_PRE = dict(delivered=0, done=False, badge=False, running=False, oiled=set())


def state(**kw):
    s = dict(STATE_PRE)
    s.update(kw)
    return s


# --- Collision and the walk graph -------------------------------------------------------

WALKABLE_CH = set(".mSDOM") | set(TURN_DIR)


def walkable(x, y, st, people=()):
    """Can the player stand on (x, y)? Turnstile cells are passed, never stood on."""
    if not (0 <= x < W and 0 <= y < H) or (x, y) in people:
        return False
    ch = ROWS[y][x]
    if ch == "G":
        return st["done"]
    # The mosaic's other three cells are '.' in ROOM, so they are floor already.
    return ch in ".mSDOM"


def blocks(x, y, ids_blocking, name):
    """Collision for map.bin: blocking metatiles, the lectern, the shut gate."""
    ch = ROWS[y][x]
    if ch in TURN_DIR or ch in ".mSDOM":
        return False
    if ch == "G":
        return True            # the gate opens by script (setmetatile ... FALSE)
    return True


def neighbours(x, y, st, people=()):
    """(nx, ny, cost, first step dir) moves from a standing tile."""
    out = []
    for d, (dx, dy) in DIRS.items():
        nx, ny = x + dx, y + dy
        if (nx, ny) in TURNSTILES:
            allowed = TURNSTILES[(nx, ny)]
            if st["done"] and (nx, ny) in REVERSING:
                allowed = OPPOSITE[allowed]
            if allowed == d:
                fx, fy = nx + dx, ny + dy
                if walkable(fx, fy, st, people):
                    out.append((fx, fy, 2, d))
            continue
        if walkable(nx, ny, st, people):
            out.append((nx, ny, 1, d))
    return out


def bfs(start, st, people=()):
    """Dijkstra over the walk graph (costs 1 or 2): distance and first step to each tile."""
    dist = {start: 0}
    first = {start: None}
    todo = [(0, start)]
    import heapq
    while todo:
        d0, (x, y) = heapq.heappop(todo)
        if d0 > dist[(x, y)]:
            continue
        for nx, ny, c, step in neighbours(x, y, st, people):
            nd = d0 + c
            if nd < dist.get((nx, ny), 1 << 30):
                dist[(nx, ny)] = nd
                first[(nx, ny)] = first[(x, y)] or step
                heapq.heappush(todo, (nd, (nx, ny)))
    return dist, first


def access_tiles(name, st):
    """Tiles from which the player can face a herm (its head or shaft)."""
    out = set()
    for cx, cy in (HERM_HEAD[name], HERM_SHAFT[name]):
        for dx, dy in DIRS.values():
            if walkable(cx + dx, cy + dy, st):
                out.add((cx + dx, cy + dy))
    return out


def route(start, goals, st, people=()):
    dist, first = bfs(start, st, people)
    best = min((dist[g], g) for g in goals if g in dist) if any(g in dist for g in goals) else None
    if best is None:
        return None, None, None
    return best[0], best[1], first[best[1]]


def compute_pointing():
    """Each junction herm's direction toward the next undelivered herald-herm, by
    the number delivered (0, 1, 2), from its READ_AT tile."""
    st = state(running=True)
    out = {}
    for j in JUNCTIONS:
        out[j] = []
        for k in range(3):
            _, _, step = route(READ_AT[j], access_tiles(HERALDS[k], st), st)
            if step is None:
                raise ValueError(f"{j} has no route to {HERALDS[k]}")
            out[j].append(step)
    return out


POINTING = compute_pointing()


# --- Checks ----------------------------------------------------------------------------------

def people_tiles():
    return {(p[2], p[3]) for p in PEOPLE}


def standing_tiles(st):
    return {(x, y) for y in range(H) for x in range(W) if walkable(x, y, st)}


def counter_tiles():
    """Every tile the player can stand on during the run gets a step counter."""
    st = state(running=True)
    reach, _ = bfs(ENTRANCE, st)
    return sorted((x, y) for (x, y) in reach if y not in DAIS_ROWS and ROWS[y][x] != "M")


def sight_cells(p):
    _, _, x, y, facing, sight = p[:6]
    dx, dy = {"down": (0, 1), "up": (0, -1), "left": (-1, 0), "right": (1, 0)}[facing]
    out = []
    for k in range(1, sight + 1):
        cx, cy = x + dx * k, y + dy * k
        if not walkable(cx, cy, state(running=True)) and (cx, cy) not in TURNSTILES:
            break
        out.append((cx, cy))
    return out


def solve(report=False):
    errors, lines = [], []
    st = state(running=True)
    people = people_tiles()

    # The legs, start to H1, H1 to H2, H2 to H3, and H3 up to Kerykos once the run is done.
    total = 0
    here = RUN_START
    for k, h in enumerate(HERALDS):
        n, goal, _ = route(here, access_tiles(h, st), st, people)
        if n is None:
            errors.append(f"no route to {h}")
            return errors, lines
        lines.append(f"leg {k + 1}: {here} -> {h} at {goal}: {n} steps")
        total += n
        here = goal
    lines.append(f"the run, start to the third scroll: {total} steps (glass 120)")
    if total > 100:
        errors.append(f"the optimal run is {total} steps: too tight for a 120 glass")
    done = state(done=True)
    n, _, _ = route(here, {TALK_DAIS}, done, people)
    if n is None:
        errors.append("no route from H3 to Kerykos once the run is done")
    else:
        lines.append(f"leg 4: H3 -> Kerykos {n} steps (after the turnstiles turn)")
    if route(here, {TALK_DAIS}, st, people)[0] is not None:
        errors.append("the dais is reachable before the third scroll")

    # Each wrong turnstile at a junction: the steps it costs to come back.
    for j in JUNCTIONS:
        jx, jy = READ_AT[j]
        for d, (dx, dy) in DIRS.items():
            t = (jx + dx, jy + dy)
            if t not in TURNSTILES:
                continue
            allowed = TURNSTILES[t]
            if allowed != d:
                lines.append(f"{j}: the turnstile {d} of it turns the other way (2 steps, a bounce)")
                continue
            land = (t[0] + dx, t[1] + dy)
            back = bfs(land, st, people)[0].get((jx, jy))
            lines.append(f"{j}: through the turnstile {d}: {'no way back' if back is None else str(back + 2) + ' steps back to the herm'}")

    # The pointing table.
    for j in JUNCTIONS:
        lines.append(f"{j} points: " + ", ".join(f"H{k + 1} {POINTING[j][k]}" for k in range(3)))

    # No softlock in any state: from every reachable tile the entrance is reachable.
    for label, s in (("before the run", state()), ("during the run", st),
                     ("after the run", state(done=True, badge=True))):
        reach, _ = bfs(ENTRANCE, s)
        for t in reach:
            if ENTRANCE not in bfs(t, s)[0]:
                errors.append(f"softlock {label}: no way back to the door from {t}")
                break

    # The step counters and the engine's coord event limit.
    counters = counter_tiles()
    n_coord = len(counters) + len(TURNSTILES)
    lines.append(f"coord events: {len(counters)} step counters + {len(TURNSTILES)} turnstiles = {n_coord} (max 255)")
    if n_coord > 255:
        errors.append(f"{n_coord} coord events: the engine counts them in a u8")

    # People.
    for p in PEOPLE:
        if not walkable(p[2], p[3], state()):
            errors.append(f"{p[6]} stands on {ROWS[p[3]][p[2]]!r} at ({p[2]},{p[3]})")
    reach, _ = bfs(ENTRANCE, st)
    for p in PEOPLE:
        if p[5] == 0:
            continue
        seen = sight_cells(p)
        # The engine checks trainer sight before coord events, so a trainer who saw a
        # turnstile's own tile would stop the player inside it.
        for c in seen:
            if c in TURNSTILES:
                errors.append(f"{p[6]}'s sight reaches the turnstile at {c}")
        if p[6] in MANDATORY:
            # Every route on to the next herm must cross the sight line.
            pass
        elif any(c in reach for c in seen):
            errors.append(f"{p[6]} is optional but sees {seen}")
    if report:
        print("\n".join(lines))
    return errors, lines


def mandatory_check():
    """Podarge and Euchidas must stand in the way: with their sight cells closed, the
    next herald-herm can't be reached."""
    errors = []
    st = state(running=True)
    people = people_tiles()
    for p, k in (("Podarge", 0), ("Euchidas", 1)):
        person = next(q for q in PEOPLE if q[6] == p)
        blocked = people | set(sight_cells(person))
        start = RUN_START if k == 0 else next(iter(access_tiles(HERALDS[k - 1], st)))
        n, _, _ = route(start, access_tiles(HERALDS[k], st), st, blocked)
        if n is not None:
            errors.append(f"{p} can be walked past on the way to {HERALDS[k]}")
    return errors


# --- Writing the layout, labels and events ----------------------------------------------

def layout_blocks(grid, ids):
    out = []
    for y, row in enumerate(grid):
        for x, name in enumerate(row):
            v = ids[name]
            v |= (1 if blocks(x, y, None, name) else 0) << 10
            v |= 3 << 12           # interiors use elevation 3 throughout
            out.append(v)
    return np.array(out, "<u2")


def border_blocks(ids):
    return np.array([ids["floor.void"] | (1 << 10) | (3 << 12)] * 4, "<u2")


def label(name):
    """floor.vein_a -> Floor_VeinA; herm.head_oiled_e -> Herm_HeadOiledE."""
    sec, part = name.split(".")
    camel = "".join(w[:1].upper() + w[1:] for w in part.split("_"))
    return f"METATILE_TempleHermes_{sec.title().replace('_', '')}_{camel}"


SCRIPTED = ["herm.head_s", "herm.head_n", "herm.head_oiled_n", "herm.head_oiled_e", "herm.head_oiled_s",
            "herm.head_oiled_w", "herm.shaft", "herm.shaft_scroll",
            "turnstile.turn_n", "turnstile.turn_e", "turnstile.turn_s", "turnstile.turn_w",
            "turnstile.gate_h_shut", "turnstile.gate_h_open",
            "props.torch_lit", "props.torch_cold", "props.glass_top", "props.floor",
            "scroll_table.full_l", "scroll_table.full_r", "scroll_table.empty_l", "scroll_table.empty_r"]
LABEL_BEGIN = "// gTileset_TempleHermes (Ichor: the Herald's Run), written by tools/ichor/maps/temple_hermes.py"
LABEL_END = "// end gTileset_TempleHermes"


def labels_block(ids):
    room_script()      # records every metatile the scripts set
    lines = [LABEL_BEGIN]
    for name in SCRIPTED + sorted(USED_LABELS - set(SCRIPTED)):
        lines.append(f"#define {label(name):<48} 0x{ids[name]:03X}")
    lines.append(LABEL_END)
    return "\n".join(lines)


def spliced_labels(ids):
    text = LABELS.read_text()
    block = labels_block(ids)
    a, b = text.find(LABEL_BEGIN), text.find(LABEL_END)
    if a >= 0 and b >= 0:
        return text[:a] + block + text[b + len(LABEL_END):]
    end = text.rfind("#endif")
    return text[:end] + block + "\n\n" + text[end:]


FACING = {"down": "MOVEMENT_TYPE_FACE_DOWN", "up": "MOVEMENT_TYPE_FACE_UP",
          "left": "MOVEMENT_TYPE_FACE_LEFT", "right": "MOVEMENT_TYPE_FACE_RIGHT"}


def map_events():
    objects = []
    for lid, gfx, x, y, facing, sight, script, flag in PEOPLE:
        objects.append({
            "local_id": lid, "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
            "movement_type": FACING[facing], "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NORMAL" if sight else "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": str(sight), "script": PREFIX + script, "flag": flag,
        })
    warps = [{"x": x, "y": DOOR[1], "elevation": 0, "dest_map": "MAP_EMPORION_CITY",
              "dest_warp_id": CITY_DEST_WARP_ID} for x in (DOOR[0], DOOR[0] - 1, DOOR[0] + 1)]
    coords = []
    for (x, y), d in sorted(TURNSTILES.items(), key=lambda t: (t[0][1], t[0][0])):
        coords.append({"type": "trigger", "x": x, "y": y, "elevation": 3, "var": "VAR_TEMP_4",
                       "var_value": "0", "script": PREFIX + turnstile_label(x, y)})
    for x, y in counter_tiles():
        coords.append({"type": "trigger", "x": x, "y": y, "elevation": 3, "var": "VAR_TEMP_3",
                       "var_value": "1", "script": PREFIX + "Step"})
    bgs = []

    def sign(x, y, script):
        bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                    "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": PREFIX + script})
    for name in JUNCTIONS + HERALDS:
        for x, y in (HERM_HEAD[name], HERM_SHAFT[name]):
            sign(x, y, "Herm" + name)
    for y in range(H):
        for x in range(W):
            if ROWS[y][x] in SIGNS:
                sign(x, y, SIGNS[ROWS[y][x]])
    for x, y in FRIEZE_SIGNS:
        sign(x, y, "Frieze")
    return objects, warps, coords, bgs


def write_map_json(check):
    path = MAP_DIR / "map.json"
    m = json.loads(path.read_text())
    m["object_events"], m["warp_events"], m["coord_events"], m["bg_events"] = map_events()
    text = json.dumps(m, indent=2) + "\n"
    if check:
        return [] if path.read_text() == text else ["map.json"]
    path.write_text(text)
    return []


# --- Generated scripts --------------------------------------------------------------------

SCRIPT_BEGIN = "// --- Room scripts: generated by tools/ichor/maps/temple_hermes.py from the room. Do not edit. ---"
SCRIPT_END = "// --- End of generated room scripts. ---"


def turnstile_label(x, y):
    return f"Turnstile_{x}_{y}"


USED_LABELS = set()


def set_mt(x, y, name, solid):
    USED_LABELS.add(name)
    return f"setmetatile({x}, {y}, {label(name)}, {'TRUE' if solid else 'FALSE'})"


def exits(x, y):
    """The two floor cells either side of a turnstile, along its axis."""
    dx, dy = DIRS[TURNSTILES[(x, y)]]
    return [(x + dx, y + dy), (x - dx, y - dy)]


def room_script():
    out = [SCRIPT_BEGIN, ""]
    # DrawRoom: everything that changes, from VAR_TEMP_1 (scrolls delivered), VAR_TEMP_3
    # (the run is on) and the flags.
    out.append("// Draws every herm head, the delivered scrolls, the relay torches, the gate, the")
    out.append("// turnstiles that turn round, the table of scrolls and the step-glass from the state.")
    out.append(f"script {PREFIX}DrawRoom {{")
    for j in JUNCTIONS + HERALDS:
        out.append(f"    call({PREFIX}DrawHerm{j})")
    for k, h in enumerate(HERALDS):
        x, y = HERM_SHAFT[h]
        out.append(f"    if (flag(FLAG_ICHOR_HERALDS_RUN_DONE) || var(VAR_TEMP_1) >= {k + 1}) {{")
        out.append(f"        {set_mt(x, y, 'herm.shaft_scroll', True)}")
        out.append("    } else {")
        out.append(f"        {set_mt(x, y, 'herm.shaft', True)}")
        out.append("    }")
    for i, (x, y) in enumerate(TORCHES):
        out.append(f"    if (flag(FLAG_ICHOR_HERALDS_RUN_DONE) || var(VAR_TEMP_1) >= {i + 1}) {{")
        out.append(f"        {set_mt(x, y, 'props.torch_lit', True)}")
        out.append("    } else {")
        out.append(f"        {set_mt(x, y, 'props.torch_cold', True)}")
        out.append("    }")
    gx, gy = GATE
    pre, post = base_grid(state()), base_grid(state(done=True))
    out.append("    if (flag(FLAG_ICHOR_HERALDS_RUN_DONE)) {")
    out.append(f"        {set_mt(gx, gy, 'turnstile.gate_h_open', False)}")
    for g in (post,):
        for (x, y) in sorted(REVERSING):
            out.append(f"        {set_mt(x, y, g[y][x], False)}")
            for ex, ey in exits(x, y):
                out.append(f"        {set_mt(ex, ey, g[ey][ex], False)}")
    out.append("    } else {")
    out.append(f"        {set_mt(gx, gy, 'turnstile.gate_h_shut', True)}")
    for (x, y) in sorted(REVERSING):
        out.append(f"        {set_mt(x, y, pre[y][x], False)}")
        for ex, ey in exits(x, y):
            out.append(f"        {set_mt(ex, ey, pre[ey][ex], False)}")
    out.append("    }")
    tx, ty = TABLE
    out.append("    if (var(VAR_TEMP_3) == 1 || flag(FLAG_ICHOR_HERALDS_RUN_DONE)) {")
    out.append(f"        {set_mt(tx, ty, 'scroll_table.empty_l', True)}")
    out.append(f"        {set_mt(tx + 1, ty, 'scroll_table.empty_r', True)}")
    out.append("    } else {")
    out.append(f"        {set_mt(tx, ty, 'scroll_table.full_l', True)}")
    out.append(f"        {set_mt(tx + 1, ty, 'scroll_table.full_r', True)}")
    out.append("    }")
    out.append("    if (flag(FLAG_BADGE02_GET)) {")
    out.append(f"        {set_mt(*GLASS, 'props.floor', True)}")
    out.append("    }")
    out.append("    return")
    out.append("}")

    for name in JUNCTIONS + HERALDS:
        x, y = HERM_HEAD[name]
        out.append("")
        out.append(f"script {PREFIX}DrawHerm{name} {{")
        flag = f"FLAG_ICHOR_HERMES_HERM_{name}" if name in JUNCTIONS else None
        out.append("    if (flag(FLAG_ICHOR_HERALDS_RUN_DONE)) {")
        if flag:
            out.append(f"        if (flag({flag})) {{")
            out.append(f"            {set_mt(x, y, 'herm.head_oiled_n', True)}")
            out.append("            return")
            out.append("        }")
        out.append(f"        {set_mt(x, y, 'herm.head_n', True)}")
        out.append("        return")
        out.append("    }")
        if flag:
            out.append(f"    if (!flag({flag})) {{")
            out.append(f"        {set_mt(x, y, 'herm.head_s', True)}")
            out.append("        return")
            out.append("    }")
            out.append("    switch (var(VAR_TEMP_1)) {")
            for k in range(3):
                d = POINTING[name][k].lower()
                case = f"case {k}:" if k < 2 else "default:"
                out.append(f"        {case} {set_mt(x, y, 'herm.head_oiled_' + d, True)}")
            out.append("    }")
        else:
            out.append(f"    {set_mt(x, y, 'herm.head_s', True)}")
        out.append("    return")
        out.append("}")

    # One script per turnstile: it sets the way it turns, then the shared script decides.
    for (x, y), d in sorted(TURNSTILES.items(), key=lambda t: (t[0][1], t[0][0])):
        out.append("")
        out.append(f"script {PREFIX}{turnstile_label(x, y)} {{")
        if (x, y) in REVERSING:
            out.append("    if (flag(FLAG_ICHOR_HERALDS_RUN_DONE)) {")
            out.append(f"        setvar(VAR_0x8004, {GAME_DIR[OPPOSITE[d]]})")
            out.append("    } else {")
            out.append(f"        setvar(VAR_0x8004, {GAME_DIR[d]})")
            out.append("    }")
        else:
            out.append(f"    setvar(VAR_0x8004, {GAME_DIR[d]})")
        out.append(f"    goto({PREFIX}Turnstile)")
        out.append("}")
    out.append("")
    out.append(SCRIPT_END)
    return "\n".join(out)


def spliced_script():
    text = (MAP_DIR / "scripts.pory").read_text()
    a, b = text.find(SCRIPT_BEGIN), text.find(SCRIPT_END)
    if a < 0 or b < 0:
        sys.exit(f"temple_hermes: scripts.pory needs the markers:\n{SCRIPT_BEGIN}\n{SCRIPT_END}")
    return text[:a] + room_script() + text[b + len(SCRIPT_END):]


def script_checks():
    """Every setmetatile in scripts.pory targets a cell whose art may change, with art
    that belongs there."""
    errors = []
    text = (MAP_DIR / "scripts.pory").read_text()
    allowed = {}
    for st in all_states():
        g = base_grid(st)
        for y in range(H):
            for x in range(W):
                allowed.setdefault((x, y), set()).add(g[y][x])
    room_script()
    by_label = {label(n): n for n in set(SCRIPTED) | USED_LABELS}
    for x, y, lab in re.findall(r"setmetatile\((\d+),\s*(\d+),\s*(METATILE_\w+)", text):
        x, y = int(x), int(y)
        name = by_label.get(lab)
        if name is None:
            errors.append(f"setmetatile uses unknown label {lab}")
        elif name not in allowed.get((x, y), set()):
            errors.append(f"setmetatile({x}, {y}, {lab}) puts {name} where the room has {allowed.get((x, y))}")
    return errors


def all_states():
    out = []
    oiled_all = set(JUNCTIONS)
    for oiled in (set(), oiled_all):
        # The third delivery sets FLAG_ICHOR_HERALDS_RUN_DONE at once, so 0-2 with the run on.
        for k in range(3):
            out.append(state(delivered=k, running=True, oiled=oiled))
        out.append(state(done=True, oiled=oiled))
        out.append(state(done=True, badge=True, oiled=oiled))
        out.append(state(oiled=oiled))
    return out


# --- Renders -------------------------------------------------------------------------------

def compiled_renderer(layout):
    render_map.read_fieldmap_constants()
    symbols = render_map.scan_tileset_symbols()
    prim = render_map.resolve_tileset(layout["primary_tileset"], symbols)
    sec = render_map.resolve_tileset(layout["secondary_tileset"], symbols)
    return render_map.Renderer(render_map.Tileset(prim), render_map.Tileset(sec))


def scaled(img, s):
    return img.resize((img.width * s, img.height * s), Image.NEAREST)


def font(size):
    return ImageFont.load_default(size=size)


SHEET_DIR = ROOT / "graphics/object_events/pics/people/ichor"
GFX_SHEET = {"OBJ_EVENT_GFX_ICHOR_KERYKOS": "kerykos", "OBJ_EVENT_GFX_ICHOR_YOUTH_M": "youth_m",
             "OBJ_EVENT_GFX_ICHOR_ACOLYTE_F": "acolyte_f", "OBJ_EVENT_GFX_ICHOR_ACOLYTE_M": "acolyte_m"}
FRAME = {"down": 0, "up": 1, "left": 2, "right": 2}


def walker_frame(gfx, facing):
    """The 16 x 32 standing frame of a walker, RGBA, or None if its sheet is missing."""
    p = SHEET_DIR / (GFX_SHEET.get(gfx, "") + ".png")
    if not p.exists():
        return None
    im = Image.open(p)
    idx = np.array(im)
    rgba = np.array(im.convert("RGBA"))
    rgba[idx == 0, 3] = 0
    f = Image.fromarray(rgba, "RGBA").crop((FRAME[facing] * 16, 0, FRAME[facing] * 16 + 16, 32))
    return f.transpose(Image.FLIP_LEFT_RIGHT) if facing == "right" else f


def with_people(base, people):
    """Composite walkers onto a 1x render; a 16 x 32 sprite stands with its feet on its tile."""
    img = base.convert("RGBA")
    for gfx, x, y, facing in people:
        f = walker_frame(gfx, facing)
        if f is not None:
            img.alpha_composite(f, (x * 16, y * 16 - 16))
    return img.convert("RGB")


def room_people(st):
    out = []
    for lid, gfx, x, y, facing, sight, script, flag in PEOPLE:
        if script == "Kerykos":
            if st["done"]:
                x, y = KERYKOS_DAIS
            elif st["running"]:
                continue
        out.append((gfx, x, y, facing))
    return out


def render_state(r, ids, st, people=True):
    img = render_map.render_blocks(r, layout_blocks(base_grid(st), ids), W)
    return with_people(img, room_people(st)) if people else img


def labelled(img, text, pad=22):
    out = Image.new("RGB", (img.width, img.height + pad), (40, 40, 48))
    out.paste(img, (0, pad))
    ImageDraw.Draw(out).text((6, 4), text, fill=(230, 230, 200), font=font(14))
    return out


def sheet(images, cols, gap=10, bg=(40, 40, 48)):
    w = max(i.width for i in images)
    h = max(i.height for i in images)
    rows = (len(images) + cols - 1) // cols
    out = Image.new("RGB", (cols * w + (cols + 1) * gap, rows * h + (rows + 1) * gap), bg)
    for n, im in enumerate(images):
        rr, c = divmod(n, cols)
        out.paste(im, (gap + c * (w + gap), gap + rr * (h + gap)))
    return out


def screen_view(img_margin, margin, cx, cy):
    """The 240 x 160 GBA screen with the camera on tile (cx, cy)."""
    x0 = (cx + margin - 7) * 16
    y0 = (cy + margin) * 16 - 72
    return img_margin.crop((x0, y0, x0 + 240, y0 + 160))


def with_margin(img, margin, r, ids):
    void = Image.fromarray(r.metatile(ids["floor.void"])[0])
    out = Image.new("RGB", (img.width + 32 * margin, img.height + 32 * margin))
    for y in range(0, out.height, 16):
        for x in range(0, out.width, 16):
            out.paste(void, (x, y))
    out.paste(img, (16 * margin, 16 * margin))
    return out


VIEWS = [("the porch", 9, 20), ("J1 and the turnstile east", 13, 21), ("Podarge and H1", 17, 20),
         ("the way back west", 9, 18), ("J2 at the stair", 3, 18), ("J3's fork", 4, 14),
         ("Euchidas at the gap", 10, 15), ("H2 and the east stair", 16, 14), ("J4", 15, 10),
         ("the upper colonnade", 9, 8), ("H3 and the pocket", 5, 9), ("the dais", 10, 5)]


def events_image(base, s=2):
    img = scaled(base, s).convert("RGBA")
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    c = 16 * s

    def box(x, y, fill, outline, inset=1):
        d.rectangle([x * c + inset, y * c + inset, x * c + c - 1 - inset, y * c + c - 1 - inset],
                    fill=fill, outline=outline, width=2)

    # The optimal route, start to Kerykos.
    st = state(running=True)
    here = RUN_START
    path_cells = []
    people = people_tiles()
    for h in HERALDS:
        path_cells += path_to(here, access_tiles(h, st), st, people)
        here = path_cells[-1]
    path_cells += path_to(here, {TALK_DAIS}, state(done=True), people)
    for x, y in path_cells:
        d.ellipse([x * c + c // 2 - 3, y * c + c // 2 - 3, x * c + c // 2 + 3, y * c + c // 2 + 3],
                  fill=(255, 255, 255, 200))
    for (x, y), dr in TURNSTILES.items():
        box(x, y, (255, 220, 0, 60), (255, 220, 0, 230))
        d.text((x * c + c // 2, y * c + c // 2), {"N": "^", "S": "v", "E": ">", "W": "<"}[dr],
               fill=(0, 0, 0, 255), font=font(14), anchor="mm")
    for p in PEOPLE:
        x, y = p[2], p[3]
        for sx, sy in sight_cells(p):
            box(sx, sy, (255, 60, 40, 70), (255, 60, 40, 255))
        box(x, y, (40, 220, 90, 60), (20, 120, 40, 255))
        d.text((x * c + c // 2, y * c - 2), p[6], fill=(255, 255, 255, 255), font=font(11),
               anchor="md", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    for name in JUNCTIONS + HERALDS:
        x, y = HERM_HEAD[name]
        d.text((x * c + c // 2, y * c + 2), name, fill=(120, 220, 255, 255), font=font(11),
               anchor="mt", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    d.rectangle([DOOR[0] * c + 6, DOOR[1] * c + 6, DOOR[0] * c + c - 7, DOOR[1] * c + c - 7],
                outline=(255, 60, 200, 255), width=2)
    img = Image.alpha_composite(img, over)
    key = [((255, 255, 255), "the optimal route"), ((255, 220, 0), "turnstile (its one way)"),
           ((40, 220, 90), "person"), ((255, 60, 40), "trainer sight"), ((255, 60, 200), "warp 0 to Emporion")]
    pad = 18
    out = Image.new("RGBA", (img.width, img.height + pad * len(key) + 8), (40, 40, 48, 255))
    out.paste(img, (0, 0))
    dd = ImageDraw.Draw(out)
    for i, (col, text) in enumerate(key):
        y = img.height + 6 + i * pad
        dd.rectangle([8, y, 20, y + 12], fill=col)
        dd.text((28, y), text, fill=(230, 230, 200), font=font(11))
    return out.convert("RGB")


def path_to(start, goals, st, people=()):
    """The tiles of a shortest route (turnstile cells included)."""
    import heapq
    dist, prev = {start: 0}, {start: None}
    todo = [(0, start)]
    while todo:
        d0, cur = heapq.heappop(todo)
        if cur in goals:
            out = []
            while cur is not None:
                out.append(cur)
                p = prev[cur]
                if p is not None and abs(p[0] - cur[0]) + abs(p[1] - cur[1]) == 2:
                    out.append(((p[0] + cur[0]) // 2, (p[1] + cur[1]) // 2))
                cur = p
            return out[::-1]
        if d0 > dist[cur]:
            continue
        for nx, ny, cst, _ in neighbours(*cur, st, people):
            if d0 + cst < dist.get((nx, ny), 1 << 30):
                dist[(nx, ny)] = d0 + cst
                prev[(nx, ny)] = cur
                heapq.heappush(todo, (d0 + cst, (nx, ny)))
    return [start]


def renders(r, ids):
    IMG.mkdir(parents=True, exist_ok=True)
    pre = render_state(r, ids, state())
    solved = render_state(r, ids, state(done=True, badge=True, oiled=set(JUNCTIONS)))
    scaled(pre, 2).save(IMG / "temple_hermes.png")
    scaled(solved, 2).save(IMG / "temple_hermes_solved.png")
    events_image(render_state(r, ids, state(), people=False)).save(IMG / "temple_hermes_events.png")
    margin = 8
    big = with_margin(pre, margin, r, ids)
    views = [labelled(scaled(screen_view(big, margin, x, y), 2), f"{t} ({x},{y})") for t, x, y in VIEWS]
    sheet(views, 3).save(IMG / "temple_hermes_views.png")
    oiled = set(JUNCTIONS)
    stages = [("before the run", state()),
              ("the run: J1-J4 oiled", state(running=True, oiled=oiled)),
              ("H1 delivered", state(running=True, delivered=1, oiled=oiled)),
              ("H2 delivered", state(running=True, delivered=2, oiled=oiled)),
              ("the third scroll", state(done=True, oiled=oiled)),
              ("after the Laurel", state(done=True, badge=True, oiled=oiled))]
    sheet([labelled(render_state(r, ids, s), t, 18) for t, s in stages], len(stages)).save(
        IMG / "temple_hermes_stages.png")
    return ["temple_hermes.png", "temple_hermes_solved.png", "temple_hermes_events.png",
            "temple_hermes_views.png", "temple_hermes_stages.png"]


# --- Main ------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="verify the generated files are current")
    ap.add_argument("--report", action="store_true", help="print the solver's legs and loops")
    ap.add_argument("--no-render", action="store_true", help="skip the renders")
    args = ap.parse_args()

    ids, _, _ = load_catalog()
    grid = base_grid(state())
    layouts_path = ROOT / "data/layouts/layouts.json"
    layouts = json.loads(layouts_path.read_text())
    layout = next(l for l in layouts["layouts"] if l.get("id") == LAYOUT_ID)

    errors, _ = solve(report=args.report)
    errors += mandatory_check()
    blocks_, border = layout_blocks(grid, ids), border_blocks(ids)
    stale = []
    if args.check:
        if (layout["width"], layout["height"]) != (W, H):
            stale.append("layouts.json")
        for p, want in ((LAYOUT_DIR / "map.bin", blocks_), (LAYOUT_DIR / "border.bin", border)):
            if not p.exists() or not np.array_equal(np.fromfile(p, "<u2"), want):
                stale.append(p.name)
        if LABELS.read_text() != spliced_labels(ids):
            stale.append("metatile_labels.h")
        if (MAP_DIR / "scripts.pory").read_text() != spliced_script():
            stale.append("scripts.pory")
        stale += write_map_json(check=True)
        if stale:
            sys.exit(f"temple_hermes: {', '.join(stale)} out of date; run tools/ichor/maps/temple_hermes.py")
    else:
        if (layout["width"], layout["height"]) != (W, H):
            layout["width"], layout["height"] = W, H
            layouts_path.write_text(json.dumps(layouts, indent=2) + "\n")
        blocks_.tofile(LAYOUT_DIR / "map.bin")
        border.tofile(LAYOUT_DIR / "border.bin")
        LABELS.write_text(spliced_labels(ids))
        (MAP_DIR / "scripts.pory").write_text(spliced_script())
        write_map_json(check=False)
    errors += script_checks()
    if errors:
        sys.exit("temple_hermes: " + "\n  ".join(["checks failed:"] + errors))
    if not args.check and not args.no_render:
        r = compiled_renderer(layout)
        for p in renders(r, ids):
            print("design/phase2/img/" + p)
    print(f"temple_hermes: {W}x{H} on {layout['primary_tileset']} + {layout['secondary_tileset']}, "
          f"{len(PEOPLE)} people, {len(counter_tiles())} step counters, {len(TURNSTILES)} turnstiles; checks pass")


if __name__ == "__main__":
    main()
