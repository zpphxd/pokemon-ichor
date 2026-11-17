#!/usr/bin/env python3
"""The Labyrinth's heart: Rings V-VII, the tomb, the forge's rooms, the Starry Chamber
and the Icarus Shaft (design/LABYRINTH.md, design/LABYRINTH_MAZE.md, design/maps/*.md).

Each ring is drawn in three moves:
1. its fixed architecture by hand (Asterion's ring road round the lake, the gallery,
   the forge, the dancing floor...), each piece where the story needs it;
2. a cave maze grown into what is left (maze()): a seeded lattice of passages, a
   spanning tree braided into loops, widened here and there, and carved through to
   every port the hand-drawn parts left open;
3. landmarks, items and the thread's anchors at the junctions and dead ends.
build() then autotiles, checks, writes the layout, map.json and the generated ON_LOAD
block, renders design/phase4/img/maps/<stem>*.png and prints LABYRINTH_MAZE.md §2's counts.

  /usr/bin/python3 tools/ichor/maps/labyrinth_heart.py [ring5 tomb ring6 ...] [--no-render] [--stem-suffix _pass1]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heart_lib as H  # noqa: E402

ROOT = H.ROOT
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


# --------------------------------------------------------------------------
# The maze generator
# --------------------------------------------------------------------------

def maze(m, mask, seed, step=4, origin=(1, 1), braid=0.35, widen=0.12, ports=(), floor=".",
         jitter=0.5, rooms=0.08):
    """Grow a braided cave maze into `mask` (a set of cells that may be carved).

    Nodes sit on a lattice of `step`; passages join neighbours through the cells
    between them. A random spanning tree keeps everything connected, then `braid` of
    the remaining links are added for loops. `ports` are (x, y) cells outside the
    mask that must join the maze: each tunnels straight to its nearest node."""
    rng = random.Random(seed)
    ox, oy = origin
    nodes = [(x, y) for y in range(oy, m.h, step) for x in range(ox, m.w, step) if (x, y) in mask]
    ns = set(nodes)
    links = []
    for (x, y) in nodes:
        for dx, dy in ((step, 0), (0, step)):
            n = (x + dx, y + dy)
            if n in ns and all((x + k * dx // step, y + k * dy // step) in mask for k in range(1, step)):
                links.append(((x, y), n))
    rng.shuffle(links)
    parent = {n: n for n in nodes}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    tree, rest = [], []
    for a, b in links:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            tree.append((a, b))
        else:
            rest.append((a, b))
    chosen = tree + [l for l in rest if rng.random() < braid]
    # jitter: each node may sit a cell off the lattice, so passages kink like a cave's
    pos = {}
    for n in nodes:
        x, y = n
        cands = [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                 if (x + dx, y + dy) in mask]
        pos[n] = rng.choice(cands) if rng.random() < jitter else n

    def carve_link(a, b):
        (x0, y0), (x1, y1) = pos[a], pos[b]
        if rng.random() < 0.5:   # an L: across, then along (or the other way)
            corner = (x1, y0)
        else:
            corner = (x0, y1)
        for (ax, ay), (bx, by) in (((x0, y0), corner), (corner, (x1, y1))):
            for x in range(min(ax, bx), max(ax, bx) + 1):
                for y in range(min(ay, by), max(ay, by) + 1):
                    if (x, y) in mask or m.T(x, y) == floor:
                        m.cell(x, y, floor)
        if rng.random() < widen:   # a wider stretch: the cave opening out
            if y0 == y1:
                dy = 1 if (min(x0, x1), y0 + 1) in mask and rng.random() < 0.5 else -1
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    if (x, y0 + dy) in mask:
                        m.cell(x, y0 + dy, floor)
            else:
                dx = 1 if (x0 + 1, min(y0, y1)) in mask and rng.random() < 0.5 else -1
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    if (x0 + dx, y) in mask:
                        m.cell(x0 + dx, y, floor)
    for n in nodes:
        m.cell(*pos[n], floor)
    for a, b in chosen:
        carve_link(a, b)
    # grottos: a few nodes open into small chambers
    for n in nodes:
        if rng.random() < rooms:
            x, y = pos[n]
            w, h = rng.choice(((3, 3), (4, 3), (3, 4), (4, 4)))
            for yy in range(y - 1, y - 1 + h):
                for xx in range(x - 1, x - 1 + w):
                    if (xx, yy) in mask and not ((xx in (x - 1, x - 2 + w)) and (yy in (y - 1, y - 2 + h))
                                                and rng.random() < 0.6):
                        m.cell(xx, yy, floor)
    for (px, py) in ports:
        best = min(nodes, key=lambda n: abs(pos[n][0] - px) + abs(pos[n][1] - py)) if nodes else None
        if best is None:
            continue
        best = pos[best]
        x, y = px, py
        while (x, y) != best:   # L-shaped tunnel, horizontal first
            if x != best[0]:
                x += 1 if best[0] > x else -1
            elif y != best[1]:
                y += 1 if best[1] > y else -1
            if m.T(x, y) in "R":
                m.cell(x, y, floor)
    return nodes, chosen


def prune(m, keep=(), short=2, floor="."):
    """Fill back the maze's short stubs (a dead end that reaches a junction within
    `short` cells): LABYRINTH_MAZE §2 wants few dead ends, each one paying."""
    keep = set(keep)

    def nb(x, y):
        return [(x + dx, y + dy) for dx, dy in DIRS if m.walkable_t(x + dx, y + dy)]
    changed = True
    while changed:
        changed = False
        for y in range(m.h):
            for x in range(m.w):
                if m.T(x, y) != floor or (x, y) in keep or len(nb(x, y)) != 1:
                    continue
                path, cur, prev = [(x, y)], (x, y), None
                while True:
                    nxt = [c for c in nb(*cur) if c != prev]
                    if len(nxt) != 1 or len(path) > short:
                        break
                    prev, cur = cur, nxt[0]
                    if len(nb(*cur)) >= 3:
                        break
                    path.append(cur)
                if len(path) <= short and all(m.T(*c) == floor and c not in keep for c in path):
                    for c in path:
                        m.cell(*c, "R")
                    changed = True


def braid_dead_ends(m, keep=(), reach=3, floor=".", allowed=None, rng=None, share=1.0):
    """Tunnel a dead end through to the nearest passage within `reach` cells (cave
    rock only): it becomes a loop. `share` of the dead ends are braided."""
    keep = set(keep)
    rng = rng or random.Random(0)
    for (x, y) in dead_ends(m):
        if (x, y) in keep or m.T(x, y) != floor or rng.random() > share:
            continue
        nbs = [(x + dx, y + dy) for dx, dy in DIRS if m.walkable_t(x + dx, y + dy)]
        if len(nbs) != 1:
            continue
        (nx, ny), = nbs
        fwd = (x - nx, y - ny)
        best = None
        for d in [fwd] + [dd for dd in DIRS if dd != fwd and dd != (-fwd[0], -fwd[1])]:
            path = []
            for k in range(1, reach + 2):
                c = (x + d[0] * k, y + d[1] * k)
                if m.walkable_t(*c):
                    if path and (best is None or len(path) < len(best)):
                        best = path
                    break
                if m.T(*c) != "R" or (allowed is not None and c not in allowed):
                    break
                path.append(c)
        if best:
            for c in best:
                m.cell(*c, floor)


def break_long_runs(m, limit=8, rng=None):
    """LABYRINTH_MAZE §2: no straight run longer than `limit` without a turn, junction or
    feature. Cut an alcove into the rock beside the middle of each long run and stand a
    stalagmite (or rubble) in it: a landmark, and nothing to walk into."""
    rng = rng or random.Random(1)
    for _ in range(6):
        s = m.graph_stats()
        if s["longest_run"] <= limit or s["longest_at"] is None:
            return
        ex, ey = s["longest_at"]
        # walk back along the run to its middle
        horiz = m.walkable_t(ex - 1, ey) and not m.walkable_t(ex, ey - 1)
        d = (1, 0) if horiz else (0, 1)
        k = s["longest_run"] // 2 + 1
        cx, cy = ex - d[0] * k, ey - d[1] * k
        placed = False
        for side in ((d[1], d[0]), (-d[1], -d[0])):
            ax, ay = cx + side[0], cy + side[1]
            if m.T(ax, ay) == "R" and m.T(ax + side[0], ay + side[1]) in "RM":
                m.cell(ax, ay, ".")
                m.place(ax, ay, "formations", rng.choice(["mite_a", "mite_b", "rubble"]), solid=True)
                m.notes[(cx, cy)] = "alcove"
                m.notes[(ax, ay)] = "alcove"
                placed = True
                break
        if not placed:
            m.notes[(cx, cy)] = "mark"   # a mason's mark on the floor: the run still has a feature


def dead_ends(m):
    return [(x, y) for y in range(m.h) for x in range(m.w)
            if m.walkable_t(x, y) and sum(m.walkable_t(x + dx, y + dy) for dx, dy in DIRS) == 1]


def band(m, x0, y0, x1, y1, keep=()):
    """The rock cells of a rectangle that the maze may carve, minus `keep` cells."""
    k = set(keep)
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
            if m.T(x, y) == "R" and (x, y) not in k}


def walls_around(m, ch="M", region=None, floors=","):
    """Turn the rock beside a built floor into the house's masonry."""
    for y in range(m.h):
        for x in range(m.w):
            if m.T(x, y) != "R" or (region and (x, y) not in region):
                continue
            near = [m.T(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
            if any(n in floors for n in near):
                m.cell(x, y, ch)


# --------------------------------------------------------------------------
# Ring V, the Hunt (LABYRINTH §6 Ring V; LABYRINTH_MAZE §1, §5)
# --------------------------------------------------------------------------

# Asterion's loop, the paved ring road round the lake: his WALK_SEQUENCE_RIGHT_DOWN_LEFT_UP
# rectangle, from its north-west corner, range 15 x 15 (the engine's largest).
R5_LOOP = (20, 16, 35, 31)
R5_POOLS = {1: [(23, 16), (24, 16)], 2: [(39, 16), (40, 16)], 3: [(35, 34), (35, 35)], 4: [(16, 31), (17, 31)],
            5: [(29, 16)], 6: [(28, 31)], 7: [(20, 24), (20, 25)], 8: [(35, 23)]}
R5_STAIR_UP = (27, 2)        # from Ring IV (the Labyrinth I build's map)
R5_STAIR_DOWN = (27, 40)     # to Ring VI
R5_TOMB_STAIR = (44, 13)     # down into Minos's tomb (the Labyrinth I build's map)
R5_CLIMB = (4, 2)            # the rope climb back up to Ring IV
R5_HOLE = (45, 44)           # drops into Ring VI at the same cell
R5_GRATE = (53, 33)          # the bronze grate that opens only from the south


def map_exists(name):
    return (ROOT / "data/maps" / name / "map.json").exists()


def ring5(stem_suffix="", render=True):
    m = H.HeartMap("LabyrinthRing5", "mychos", 56, 48)
    x0, y0, x1, y1 = R5_LOOP
    # the lake: its north arm under the gallery, the basin inside the loop, an island
    m.carve(15, 11, 40, 15, "~")
    m.carve(21, 17, 34, 30, "~")
    m.draw(["RRRR ", "R..RR", "RR.oR", " RRRR"], 26, 21)   # the island: a skylight on a ledge
    m.carve(14, 12, 14, 14, "~")
    m.carve(12, 12, 13, 14, "P")            # where the lake spills into the dark, to Ring VI's falls
    m.carve(41, 12, 41, 14, "~")
    # the ring road (built: the house's slabs)
    m.carve(x0, y0, x1, y0, ",")
    m.carve(x0, y1, x1, y1, ",")
    m.carve(x0, y0, x0, y1, ",")
    m.carve(x1, y0, x1, y1, ",")
    # the gallery (built, lit by the Titans' lamps), its grate over the lake
    m.carve(19, 5, 36, 9, ",")
    m.carve(26, 3, 29, 4, ",")
    # the four corner spurs, running straight on past the loop's corners
    m.carve(x1 + 1, y0, 42, y0, ",")        # NE, east: %1 at (43,16), Minos's tomb
    m.carve(x1, y1 + 1, x1, 37, ",")        # SE, south: %2 at (35,38), the shortcut to the stair
    m.carve(14, y1, x0 - 1, y1, ",")        # SW, west: %3 at (13,31), the treasure room
    m.carve(x0, 11, x0, y0 - 1, ",")        # NW, north: the causeway down from the gallery
    m.carve(x0, 10, 22, 10, ",")
    m.carve(44, 14, 46, 18, ",")            # the tomb's forecourt, behind %1
    m.carve(7, 29, 12, 33, ",")             # the treasure room, behind %3
    m.carve(24, 41, 31, 44, ",")            # the south stair hall (dark), Ring VI below
    m.carve(x1, 39, x1, 40, ".")            # %2's way on
    m.carve(3, 3, 5, 5, ".")                # the rope grotto (the climb up to Ring IV)
    m.carve(43, 43, 46, 45, ".")            # the sinkhole grotto (the drop to Ring VI)
    m.carve(R5_GRATE[0], 30, R5_GRATE[0], 36, ".")   # the grate's tunnel
    for cells in R5_POOLS.values():
        for (x, y) in cells:
            m.cell(x, y, "o")
    for (x, y) in ((40, 15), (40, 17), (35, 33), (16, 32), (16, 30), (27, 32), (36, 24), (19, 22)):
        if m.T(x, y) == "R":
            m.cell(x, y, ".")
    fixed = {(x, y) for y in range(m.h) for x in range(m.w) if m.T(x, y) != "R"}
    keep_off = set()
    for (x, y) in fixed:     # a rock collar round every fixed part, so the maze joins only at ports
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                keep_off.add((x + dx, y + dy))
    # Two mazes: everything outside the loop north of the south wall, and the dark south.
    # Only the loop's crossings, %2, the lake and the one-way grate join them.
    north = band(m, 1, 1, 54, 31, keep=keep_off) - {(x, y) for x in range(18, 38) for y in range(28, 32)}
    north -= {(R5_GRATE[0] + dx, y) for dx in (-1, 0, 1) for y in range(31, 36)}
    south = band(m, 1, 36, 54, 45, keep=keep_off)
    north_ports = [(18, 7), (37, 7), (19, 20), (19, 27), (36, 20), (36, 28), (43, 15), (12, 31),
                   (4, 6), (R5_GRATE[0], 29)]
    south_ports = [(24, 37), (31, 37), (36, 40), (23, 42), (32, 43), (44, 42), (R5_GRATE[0], 37)]
    maze(m, north, seed=55, step=4, origin=(2, 2), braid=0.5, widen=0.15, ports=north_ports)
    maze(m, south, seed=56, step=4, origin=(2, 37), braid=0.5, widen=0.15, ports=south_ports)
    # the loop's south crossings, down to the dark half
    m.carve(24, 32, 24, 36, ".")
    m.carve(31, 32, 31, 36, ".")
    for (px, py) in north_ports + south_ports:
        m.cell(px, py, ".")
    reserved = {(27, 4), (45, 16), (10, 31), (19, 22), (18, 22), (4, 4), (45, 44), (R5_GRATE[0], 34)}
    keep = fixed | reserved | set(north_ports) | set(south_ports)
    prune(m, keep=keep, short=3)
    braid_dead_ends(m, keep=keep, reach=6, allowed=north | south, rng=random.Random(5), share=1.0)
    prune(m, keep=keep, short=3)
    walls_around(m, "M", floors=",")
    return finish_ring5(m, stem_suffix, render)


R5_VISIBLE = ["ITEM_REVIVE", "ITEM_MAX_ELIXIR", "ITEM_NUGGET"]
R5_HIDDEN = [("ITEM_HYPER_POTION", "FLAG_ICHOR_HIDDEN_ITEM_RING5_A"),
             ("ITEM_MAX_ETHER", "FLAG_ICHOR_HIDDEN_ITEM_RING5_B"),
             ("ITEM_ULTRA_BALL", "FLAG_ICHOR_HIDDEN_ITEM_RING5_C")]


def finish_ring5(m, stem_suffix, render):
    x0, y0, x1, y1 = R5_LOOP
    m.crack(43, 16, "FLAG_ICHOR_RING5_WALL_TOMB")
    m.crack(35, 38, "FLAG_ICHOR_RING5_WALL_SOUTH")
    m.crack(13, 31, "FLAG_ICHOR_RING5_WALL_TREASURE")
    # the gallery: its grate over the lake, lamps, sickle banners, the dance's fresco
    for x in range(19, 37):
        m.cell(x, 10, "M")
    m.carve(x0, 10, 22, 10, ",")
    for x in range(23, 37):
        m.place(x, 10, "grates", "gallery", solid=True)
    # the Titans' watch post: lamps, sickle banners, a duty desk, supply chests
    for x in (19, 36, 23, 32):
        m.place_block(x, 5, "lamp_stand")
    for x in (21, 25, 30, 34):
        m.place(x, 4, "banners", "face")
    m.place_block(20, 8, "archive_desk")
    m.place(34, 8, "vault", "chest_l")
    m.place(35, 8, "vault", "chest_r")
    m.place(35, 7, "vault", "ingots")
    # the south hall: the stair's lamps, long cold
    for x in (25, 30):
        m.place_block(x, 41, "lamp_stand")
    m.place(24, 40, "banners", "torn")
    m.place(31, 40, "banners", "torn")
    m.place_block(32, 2, "fresco_v")
    for (dx, dy) in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)):
        m.cell(32 + dx, 2 + dy, "M")
    # the stairs: up to Ring IV, down to Ring VI, down into the tomb
    sx, sy = R5_STAIR_UP
    m.cell(sx, sy, "M"); m.cell(sx + 1, sy, "M")
    m.place(sx, sy, "stairs", "up_l", solid=False)
    m.place(sx + 1, sy, "stairs", "up_r", solid=False)
    dx_, dy_ = R5_STAIR_DOWN
    m.cell(dx_, dy_, "M"); m.cell(dx_ + 1, dy_, "M")
    m.place(dx_, dy_, "stairs", "down_l", solid=False)
    m.place(dx_ + 1, dy_, "stairs", "down_r", solid=False)
    tx, ty = R5_TOMB_STAIR
    m.cell(tx, ty, "M"); m.cell(tx + 1, ty, "M")
    m.place(tx, ty, "stairs", "down_l", solid=False)
    m.place(tx + 1, ty, "stairs", "down_r", solid=False)
    # the rope climb (a cave face: the grotto's back wall), the sinkhole, the grate
    cx, cy = R5_CLIMB
    m.cell(cx, cy, "R"); m.cell(cx, cy - 1, "R")
    m.place(cx, cy, "formations", "climb", solid=False)
    m.place(cx, cy - 1, "formations", "climb_top", solid=True)
    m.place(*R5_HOLE, "formations", "hole", solid=False)
    m.cell(44, 42, "R"); m.cell(44, 41, "R")                 # the rope up from Ring VI's east caves
    m.place(44, 42, "formations", "climb", solid=False)
    m.place(44, 41, "formations", "climb_top", solid=True)
    m.place(*R5_GRATE, "doorways", "grate", solid=True)
    # the bell, in its niche off the west road
    m.cell(18, 22, ".")
    m.place(18, 22, "formations", "bell", solid=True)
    # a column and stalagmites where the cave opens out
    lay_dressing(m, seed=5)
    for cells in R5_POOLS.values():
        for c in cells:
            m.notes[c] = "pool"
    break_long_runs(m)
    m.lay()

    # --- events ---------------------------------------------------------------------------------
    ring4 = "MAP_LABYRINTH_RING4" if map_exists("LabyrinthRing4") else "MAP_LABYRINTH_RING5"
    tomb = "MAP_LABYRINTH_MINOS_TOMB" if map_exists("LabyrinthMinosTomb") else "MAP_LABYRINTH_RING5"
    m.warp(sx, sy, ring4, 1)                       # 0
    m.warp(sx + 1, sy, ring4, 1)                   # 1
    m.warp(dx_, dy_, "MAP_LABYRINTH_RING6", 0)     # 2
    m.warp(dx_ + 1, dy_, "MAP_LABYRINTH_RING6", 0) # 3
    m.warp(tx, ty, tomb, 0)                        # 4
    m.warp(tx + 1, ty, tomb, 0)                    # 5
    m.warp(cx, cy, ring4, 2)                       # 6: the rope
    m.warp(44, 42, "MAP_LABYRINTH_RING6", 4)       # 7: the rope down to Ring VI's east caves
    for w in m.warps:
        if w["dest_map"] == "MAP_LABYRINTH_RING5":
            w["dest_warp_id"] = "0"
    m.header.update({"requires_flash": True, "music": "MUS_ICHOR_HOLLOW", "map_type": "MAP_TYPE_UNDERGROUND",
                     "allow_escaping": True})
    # Asterion, on his loop; the scene's bull and Kleon (Scene E)
    m.obj("SPECIES(ASTERLORN)", x0, y0, "LabyrinthRing5_EventScript_Asterion",
          move="MOVEMENT_TYPE_WALK_SEQUENCE_RIGHT_DOWN_LEFT_UP", local_id="LOCALID_RING5_ASTERION",
          rx=x1 - x0, ry=y1 - y0, flag="FLAG_ICHOR_ASTERION_FREED")
    m.objects[-1]["graphics_id"] = "OBJ_EVENT_GFX_SPECIES(ASTERLORN)"
    m.obj("SPECIES(ASTERLORN)", 31, 16, "0", move="MOVEMENT_TYPE_FACE_LEFT", local_id="LOCALID_RING5_BULL",
          flag="FLAG_ICHOR_HIDE_KLEON_RING5")
    m.objects[-1]["graphics_id"] = "OBJ_EVENT_GFX_SPECIES(ASTERLORN)"
    m.obj("ICHOR_KLEON", 19, 20, "0", move="MOVEMENT_TYPE_FACE_RIGHT", local_id="LOCALID_RING5_KLEON",
          flag="FLAG_ICHOR_HIDE_KLEON_RING5")
    for x in (20, 21, 22):
        m.trigger(x, 10, "LabyrinthRing5_EventScript_SceneE", var="VAR_ICHOR_KNOSSA", value=9)
    m.trigger(*R5_HOLE, "LabyrinthRing5_EventScript_Sinkhole", var="VAR_TEMP_0", value=0)
    m.trigger(dx_, dy_ + 2, "LabyrinthRing5_EventScript_SouthStair", var="VAR_ICHOR_KNOSSA", value=11)
    m.trigger(dx_ + 1, dy_ + 2, "LabyrinthRing5_EventScript_SouthStair", var="VAR_ICHOR_KNOSSA", value=11)
    # signs: the Titans' notice, the bell, the fresco, the spill, the grate, the island
    m.sign(25, 10, "LabyrinthRing5_EventScript_Notice")
    m.sign(18, 22, "LabyrinthRing5_EventScript_Bell")
    m.sign(33, 4, "LabyrinthRing5_EventScript_Fresco")
    m.sign(R5_GRATE[0], R5_GRATE[1], "LabyrinthRing5_EventScript_Grate")
    m.sign(13, 15, "LabyrinthRing5_EventScript_Spill") if m.walkable_t(13, 15) else None
    # treasure behind %3: the bull's own TM, and a star
    m.item_ball(8, 30, "ITEM_TM_BULK_UP", "FLAG_ICHOR_RING5_ITEM_4")
    m.item_ball(8, 32, "ITEM_STAR_PIECE", "FLAG_ICHOR_RING5_ITEM_5")
    m.bgs.append({"type": "hidden_item", "x": 28, "y": 22, "elevation": 3, "item": "ITEM_BIG_PEARL",
                  "flag": "FLAG_ICHOR_HIDDEN_ITEM_RING5_ISLAND", "quantity": 1, "underfoot": False})
    # the thread's bronze rings
    for (x, y, name) in ((27, 4, "THREAD_ANCHOR_RING5_GALLERY"), (45, 16, "THREAD_ANCHOR_RING5_TOMB"),
                         (10, 31, "THREAD_ANCHOR_RING5_TREASURE"), (27, 42, "THREAD_ANCHOR_RING5_SOUTH")):
        m.anchor(x, y, name)
    # every dead end pays (LABYRINTH_MAZE §2): items, hidden items, or a bronze ring
    rewards_at_dead_ends(m, R5_VISIBLE, ["FLAG_ICHOR_RING5_ITEM_1", "FLAG_ICHOR_RING5_ITEM_2",
                                        "FLAG_ICHOR_RING5_ITEM_3"], R5_HIDDEN,
                         anchor_names=["THREAD_ANCHOR_RING5_WEST", "THREAD_ANCHOR_RING5_EAST",
                                       "THREAD_ANCHOR_RING5_DEEP"],
                         skip={(cx, cy + 1), (cx, cy + 2), R5_HOLE, (R5_GRATE[0], 34), (19, 22), (13, 15)})
    for cells in R5_POOLS.values():
        for c in cells:
            m.notes[c] = "pool"
    m.gen += ["call(LabyrinthRing5_EventScript_OnLoadExtra)"]
    if render:
        H.ensure_map(m.name, m.w, m.h, m.ts, "MUS_ICHOR_HOLLOW")
        m.build("labyrinth_ring5" + stem_suffix, starts=[(27, 3)],
                must_reach=[(27, 42, "the south hall"), (45, 16, "the tomb forecourt")],
                extra={(43, 16), (35, 38), (13, 31), R5_GRATE},
                views=[(27, 6), (21, 14), (40, 16), (18, 24), (35, 34), (27, 42), (8, 31), (50, 8), (10, 40)])
        m.write_generated()
    return m


def lay_dressing(m, seed):
    """Stalagmites and columns in the cave's wider places: a landmark for each screen,
    never on a corridor a single cell wide (they'd block it)."""
    rng = random.Random(seed)
    for y in range(2, m.h - 2):
        for x in range(2, m.w - 2):
            if m.T(x, y) != "." or (x, y) in m.deco:
                continue
            open8 = sum(m.walkable_t(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                        if (dx, dy) != (0, 0))
            if open8 >= 7 and rng.random() < 0.10:
                # blocking it must not cut a path: all its walkable neighbours stay joined
                around = [(x + dx, y + dy) for dx, dy in DIRS if m.walkable_t(x + dx, y + dy)]
                m.cell(x, y, "x")
                ok = joined(m, around, (x, y))
                if not ok:
                    m.cell(x, y, ".")
                    continue
                m.cell(x, y, ".")
                part = rng.choice(["mite_a", "mite_b", "mite_a", "rubble"])
                m.place(x, y, "formations", part, solid=True)
                m.notes[(x, y)] = part


def joined(m, cells, blocked):
    """Are all `cells` connected to each other without passing `blocked` (local search)?"""
    if len(cells) <= 1:
        return True
    start, goal = cells[0], set(cells[1:])
    seen, q = {start}, [start]
    while q and goal - seen:
        x, y = q.pop()
        for dx, dy in DIRS:
            n = (x + dx, y + dy)
            if n in seen or n == blocked or abs(n[0] - blocked[0]) > 4 or abs(n[1] - blocked[1]) > 4:
                continue
            if m.walkable_t(*n) and n not in m.deco:
                seen.add(n)
                q.append(n)
    return not (goal - seen)


def rewards_at_dead_ends(m, visible, visible_flags, hidden, anchor_names, skip=()):
    ends = [c for c in dead_ends(m) if c not in set(skip) and m.T(*c) == "." and c not in m.deco
            and not any(o["x"] == c[0] and o["y"] == c[1] for o in m.objects)]
    # farthest from the entrance first: the best things are the hardest to reach
    sx, sy = m.warps[0]["x"], m.warps[0]["y"] + 1
    reach = bfs_dist(m, (sx, sy))
    ends.sort(key=lambda c: -reach.get(c, 0))
    plan = ([("item", it, fl) for it, fl in zip(visible, visible_flags)]
            + [("hidden", it, fl) for it, fl in hidden]
            + [("anchor", n, None) for n in anchor_names])
    i = 0
    for c in ends:
        kind, what, flag = plan[i % len(plan)] if i < len(plan) else ("anchor", None, None)
        if kind == "item":
            m.item_ball(c[0], c[1], what, flag)
        elif kind == "hidden":
            m.bgs.append({"type": "hidden_item", "x": c[0], "y": c[1], "elevation": 3, "item": what,
                          "flag": flag, "quantity": 1, "underfoot": False})
            m.notes[c] = "hidden"
        else:
            m.anchor(c[0], c[1], what or "THREAD_ANCHOR_UNNAMED")
        i += 1
    m.dead_end_count = len(ends)


def bfs_dist(m, start):
    d = {start: 0}
    q = [start]
    for c in q:
        for dx, dy in DIRS:
            n = (c[0] + dx, c[1] + dy)
            if n not in d and m.walkable_t(*n):
                d[n] = d[c] + 1
                q.append(n)
    return d


def stats_report(m):
    s = m.graph_stats()
    print(f"{m.name}: walkable {s['walkable']}, junctions {s['junctions']} ({s['per_screen']}/screen), "
          f"dead ends {s['dead_ends']}, loops {s['loops']}, longest straight run {s['longest_run']} at {s['longest_at']}, "
          f"components {s['components']}")
    return s


# --------------------------------------------------------------------------
# Ring VI, the Forge (LABYRINTH §6 Ring VI, Scenes G and H; LABYRINTH_MAZE §1)
# --------------------------------------------------------------------------

# Daedalus's dials (LABYRINTH §5.5): three wheels in the Hall of Dials swing three
# bronze bars across each of three corridors. A bar is open when its wheel stands where
# that corridor wants it: forge B A B, archive A B A, vault B B A. Bit i of
# VAR_ICHOR_LABYRINTH is wheel W(i+1) (0 = A, 1 = B); bit 3 is the teaching dial W0.
R6_BARS = {   # corridor: [(x, y, wheel bit, wanted position)]
    "forge": [(12, 18, 0, 1), (11, 18, 1, 0), (10, 18, 2, 1)],
    "archive": [(35, 18, 0, 0), (36, 18, 1, 1), (37, 18, 2, 0)],
    "vault": [(34, 13, 0, 1), (35, 13, 1, 1), (36, 13, 2, 0)],
}
R6_TEACH_WALL = [(23, 11), (24, 11)]
R6_DIALS = {0: (19, 12), 1: (25, 12), 2: (29, 12)}    # wheel bit -> its dial, on the hall's north wall
R6_TEACH_DIAL = (17, 8)
R6_LEVER = (15, 12)
R6_SEAL = [(23, 32), (24, 32)]
R6_STAIR_UP = (23, 2)
R6_STAIR_DOWN = (27, 39)       # in the free-standing stair-house on the landing
R6_CLIMB = (40, 27)          # the rope up to Ring V's sinkhole grotto
R6_ARCHIVE_BACK = (42, 24)
R6_FALLS = (12, 30)          # the waterfall's foot: the stream from Ring V's lake
R6_HALL = (14, 12, 33, 24)


def ring6(stem_suffix="", render=True):
    m = H.HeartMap("LabyrinthRing6", "mychos", 48, 48)
    # the arrival landing and the teaching antechamber
    m.carve(20, 3, 27, 5, ",")
    m.carve(16, 6, 31, 10, ",")
    m.carve(23, 11, 24, 11, ",")
    # the forge corridor: west through the bars, then south down to the cavern
    m.carve(7, 18, 13, 18, ",")
    m.carve(7, 19, 7, 28, ",")
    m.carve(8, 24, 8, 24, ",")                  # Mimas's alcove
    # the forge cavern (x 1-13): magma, the furnace, the quench pool under the falls
    m.draw([" ............",
            "..............",
            "..............",
            "......LLL..~~.",
            ".....LLLLL.~~.",
            "....LLLLLL....",
            "....LLLLLLL...",
            "...LLLLLLLL...",
            "...LLLLLLL....",
            "....LLLLLL....",
            " ....LLLL.....",
            " .........  ..",
            "  .......   ..",
            "   .....      "], 0, 29)
    for y in range(29, 44):
        m.cell(0, y, "R")
        m.cell(14, y, "R")
    m.carve(R6_FALLS[0], 27, R6_FALLS[0], 30, "~")    # the falls' column, down into the pool
    m.carve(11, 25, 13, 26, ".")                       # the ledge above the falls
    # the archive (east) and the vault (north-east), the Titans' rooms
    m.carve(34, 18, 37, 18, ",")
    m.carve(38, 13, 46, 23, ",")
    m.carve(34, 13, 37, 13, ",")
    m.carve(37, 7, 37, 12, ",")
    m.carve(38, 3, 45, 9, ",")
    # the barracks south of the hall, and the sealed landing with the shrine below it
    m.carve(23, 25, 24, 25, ",")
    m.carve(18, 26, 29, 31, ",")
    m.carve(17, 33, 30, 43, ",")
    m.carve(21, 37, 29, 39, "M")                       # the stair-house: the fresco, the stair down
    m.carve(R6_ARCHIVE_BACK[0], R6_ARCHIVE_BACK[1], R6_ARCHIVE_BACK[0], 26, ".")
    m.carve(R6_CLIMB[0] - 1, R6_CLIMB[1] + 1, R6_CLIMB[0] + 1, R6_CLIMB[1] + 2, ".")
    m.carve(43, 43, 46, 45, ".")                      # where Ring V's sinkhole lands you
    # The Hall of Dials is itself a maze: a built grid of passages one cell wide, with a
    # chamber for each dial, the reset lever and each sentry's beat.
    hx0, hy0, hx1, hy1 = R6_HALL
    hall = {(x, y) for y in range(hy0, hy1 + 1) for x in range(hx0, hx1 + 1)}
    hall_ports = [(23, hy0), (24, hy0), (hx0, 18), (hx1, 18), (hx1, 13), (23, hy1), (24, hy1)]
    maze(m, hall, seed=66, step=2, origin=(hx0 + 1, hy0 + 1), braid=0.2, widen=0.0, jitter=0.0,
         rooms=0.0, floor=",", ports=hall_ports)
    for (x, y) in hall_ports:
        m.cell(x, y, ",")
    for (sx0, sy0) in ((15, 19), (27, 15)):          # the sentries' beats: a ring round one pillar
        m.carve(sx0, sy0, sx0 + 2, sy0 + 2, ","); m.cell(sx0 + 1, sy0 + 1, "R")
    m.carve(25, 23, 25, 23, ",")                       # the thread's ring, mid-hall
    fixed = {(x, y) for y in range(m.h) for x in range(m.w) if m.T(x, y) != "R"} | hall
    keep_off = set()
    for (x, y) in fixed:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                keep_off.add((x + dx, y + dy))
    # three cave mazes that never meet: the north-west caves off the antechamber (before the
    # dials), the forge's back caves (behind Mimas), and the east caves (the barracks' side door,
    # the archive's back grate, the sinkhole)
    nw = band(m, 1, 1, 13, 15, keep=keep_off)
    fw = band(m, 1, 19, 13, 28, keep=keep_off)
    east = band(m, 32, 25, 46, 46, keep=keep_off) | band(m, 31, 44, 46, 46, keep=keep_off)
    maze(m, nw, seed=61, step=4, origin=(2, 2), braid=0.55, ports=[(15, 8), (14, 3)])
    maze(m, fw, seed=62, step=3, origin=(2, 20), braid=0.55, ports=[(6, 22), (8, 20), (2, 28)])
    maze(m, east, seed=63, step=4, origin=(34, 27), braid=0.55,
         ports=[(30, 29), R6_ARCHIVE_BACK, (R6_CLIMB[0], R6_CLIMB[1] + 1), (44, 42)])
    ports = ((15, 8), (14, 3), (6, 22), (8, 20), (2, 28), (30, 29))
    for p in ports:
        m.cell(*p, ".")
    keep = fixed | set(ports) | {(44, 44)}
    prune(m, keep=keep, short=3)
    braid_dead_ends(m, keep=keep, reach=5, allowed=nw | fw | east, rng=random.Random(6), share=1.0)
    prune(m, keep=keep, short=3)
    walls_around(m, "M", floors=",")
    return finish_ring6(m, stem_suffix, render)


def finish_ring6(m, stem_suffix, render):
    # walls that the scripts swing: the bars, the teaching wall, the landing's seal
    for bars in R6_BARS.values():
        for (x, y, bit, want) in bars:
            m.cell(x, y, ",")
    # the hall's furniture: dials, the lever, lamps and banners
    for bit, (x, y) in R6_DIALS.items():
        m.place(x, y, "dials", "dial_a", solid=True)
    m.place(*R6_TEACH_DIAL, "dials", "dial_a", solid=True)
    m.place(*R6_LEVER, "dials", "lever", solid=True)
    for x in (14, 33):
        m.place_block(x, 22, "lamp_stand")
    for x in (17, 21, 27, 31):
        m.place(x, 11, "banners", "face")
    m.place_block(28, 3, "lamp_stand")
    m.place_block(19, 3, "lamp_stand")
    # the stairs
    sx, sy = R6_STAIR_UP
    m.cell(sx, sy, "M"); m.cell(sx + 1, sy, "M")
    m.place(sx, sy, "stairs", "up_l", solid=False)
    m.place(sx + 1, sy, "stairs", "up_r", solid=False)
    dx_, dy_ = R6_STAIR_DOWN
    m.cell(dx_, dy_, "M"); m.cell(dx_ + 1, dy_, "M")
    m.place(dx_, dy_, "stairs", "down_l", solid=False)
    m.place(dx_ + 1, dy_, "stairs", "down_r", solid=False)
    for (x, y) in R6_SEAL:
        m.cell(x, y, "M")
        m.place(x, y, "doorways", "seal", solid=True)
    # the forge: the furnace against the cavern wall, Hyperion's anvil, the kit, lamps
    m.place_block(3, 29, "forge")
    m.place_block(10, 30, "anvil")
    m.place(1, 35, "forge_kit", "bellows_l")
    m.place(2, 35, "forge_kit", "bellows_r")
    m.place(6, 31, "forge_kit", "trough")
    m.place(2, 39, "forge_kit", "mold")
    m.place(1, 40, "forge_kit", "slag")
    m.place(12, 40, "forge_kit", "slag")
    m.place_block(9, 29, "lamp_stand")
    m.place(1, 30, "banners", "face") if m.T(1, 29) in "RM" else None
    # the falls: the lake's spill from Ring V, a waterfall the Horn of Achelous climbs
    fx, fy = R6_FALLS
    m.place(fx, 26, "waterfall", "lip", solid=False)
    for y in (27, 28):
        m.place(fx, y, "waterfall", "fall", solid=False)
    m.place(fx, 29, "waterfall", "foam", solid=False)
    # the archive: shelves of revised prophecies, the clerk's desk with the scraped tablet
    for x in (39, 42):
        m.place_block(x, 13, "archive")
    m.place_block(45, 13, "lamp_stand")
    m.place_block(41, 18, "archive_desk")
    m.place(*R6_ARCHIVE_BACK, "doorways", "grate", solid=True)
    m.cell(*R6_ARCHIVE_BACK, "M")
    # the vault: chests, ingots, gold
    for i, x in enumerate((39, 41, 43)):
        m.place(x, 4, "vault", "chest_l")
        m.place(x + 1, 4, "vault", "chest_r")
    m.place(45, 4, "vault", "gold")
    m.place(45, 5, "vault", "ingots")
    # the barracks: lamps, chests, a banner
    for x in (17, 30):
        m.place_block(x, 26, "lamp_stand")
    m.place(19, 31, "vault", "ingots")
    m.place(20, 31, "vault", "chest_l")
    m.place(21, 31, "vault", "chest_r")
    for x in (19, 28):
        m.place(x, 25, "banners", "face")
    # the landing: the Mistress's shrine, its lamps
    m.place_block(18, 34, "shrine")
    m.place_block(17, 33, "lamp_stand")
    m.place_block(21, 33, "lamp_stand")
    m.place_block(21, 37, "fresco_vi")
    for dx in range(3):
        for dy in range(3):
            m.cell(21 + dx, 37 + dy, "M")
    # the rope up to Ring V
    cx, cy = R6_CLIMB
    m.cell(cx, cy, "R"); m.cell(cx, cy - 1, "R")
    m.place(cx, cy, "formations", "climb", solid=False)
    m.place(cx, cy - 1, "formations", "climb_top", solid=True)
    lay_dressing(m, seed=6)
    break_long_runs(m)
    m.lay()

    # --- events ---------------------------------------------------------------------------------
    m.warp(sx, sy, "MAP_LABYRINTH_RING5", 2)              # 0
    m.warp(sx + 1, sy, "MAP_LABYRINTH_RING5", 3)          # 1
    m.warp(dx_, dy_, "MAP_LABYRINTH_RING7", 0)            # 2
    m.warp(dx_ + 1, dy_, "MAP_LABYRINTH_RING7", 1)        # 3
    m.warp(cx, cy, "MAP_LABYRINTH_RING5", 7)              # 4: the rope up to Ring V's grotto
    m.header.update({"music": "MUS_ICHOR_TITAN", "map_type": "MAP_TYPE_UNDERGROUND", "allow_escaping": True,
                     "requires_flash": False})
    # sentries: the teaching room's Bronzong, then two in the Hall of Dials
    m.obj("SPECIES(BRONZONG)", 27, 7, "LabyrinthRing6_EventScript_Sentry1",
          move="MOVEMENT_TYPE_WALK_SEQUENCE_RIGHT_DOWN_LEFT_UP", local_id="LOCALID_RING6_SENTRY_1",
          rx=3, ry=2, trainer=True, sight=4, flag="FLAG_ICHOR_HIDE_SENTRY_1")
    m.obj("SPECIES(BRONZONG)", 15, 19, "LabyrinthRing6_EventScript_Sentry2",
          move="MOVEMENT_TYPE_WALK_SEQUENCE_RIGHT_DOWN_LEFT_UP", local_id="LOCALID_RING6_SENTRY_2",
          rx=2, ry=2, trainer=True, sight=4, flag="FLAG_ICHOR_HIDE_SENTRY_2")
    m.obj("SPECIES(BRONZONG)", 27, 15, "LabyrinthRing6_EventScript_Sentry3",
          move="MOVEMENT_TYPE_WALK_SEQUENCE_RIGHT_DOWN_LEFT_UP", local_id="LOCALID_RING6_SENTRY_3",
          rx=2, ry=2, trainer=True, sight=4, flag="FLAG_ICHOR_HIDE_SENTRY_3")
    for o in m.objects:
        o["graphics_id"] = "OBJ_EVENT_GFX_SPECIES(BRONZONG)"
    # the Gigas and the last grunt; Hyperion at his anvil
    m.obj("ICHOR_TITAN_GRUNT", 8, 24, "LabyrinthRing6_EventScript_Mimas", move="MOVEMENT_TYPE_FACE_LEFT",
          trainer=True, sight=1, local_id="LOCALID_RING6_MIMAS")
    m.obj("ICHOR_TITAN_GRUNT", 38, 6, "LabyrinthRing6_EventScript_Alkyoneus", move="MOVEMENT_TYPE_FACE_LEFT",
          trainer=True, sight=1, local_id="LOCALID_RING6_ALKYONEUS")
    m.obj("ICHOR_TITAN_GRUNT", 26, 29, "LabyrinthRing6_EventScript_Smyris", move="MOVEMENT_TYPE_FACE_LEFT",
          trainer=True, sight=4, local_id="LOCALID_RING6_SMYRIS")
    m.obj("ICHOR_TITAN_GRUNT", 9, 32, "LabyrinthRing6_EventScript_Hyperion", move="MOVEMENT_TYPE_FACE_UP",
          local_id="LOCALID_RING6_HYPERION", flag="FLAG_ICHOR_HIDE_HYPERION_KNOSSA")
    m.obj("ICHOR_PRIESTESS", 19, 36, "LabyrinthRing6_EventScript_ShrinePriestess", move="MOVEMENT_TYPE_FACE_DOWN",
          local_id="LOCALID_RING6_PRIESTESS")
    # triggers: Scene H at the archive's door, Scene G at the cavern's mouth
    m.trigger(38, 18, "LabyrinthRing6_EventScript_SceneH", var="VAR_TEMP_1", value=0)
    m.trigger(7, 29, "LabyrinthRing6_EventScript_SceneG", var="VAR_TEMP_1", value=0)
    # signs and dials
    for bit, (x, y) in R6_DIALS.items():
        m.sign(x, y, f"LabyrinthRing6_EventScript_Dial{bit + 1}")
    m.sign(*R6_TEACH_DIAL, "LabyrinthRing6_EventScript_TeachDial")
    m.sign(*R6_LEVER, "LabyrinthRing6_EventScript_Lever")
    m.sign(20, 6, "LabyrinthRing6_EventScript_Notice")
    m.sign(42, 18, "LabyrinthRing6_EventScript_Ledger")
    m.sign(*R6_ARCHIVE_BACK, "LabyrinthRing6_EventScript_ArchiveGrate")
    m.sign(22, 39, "LabyrinthRing6_EventScript_Fresco")
    for i, x in enumerate((39, 41, 43)):
        m.sign(x, 4, f"LabyrinthRing6_EventScript_Chest{i + 1}")
    m.sign(45, 4, "LabyrinthRing6_EventScript_Chest4")
    m.sign(R6_SEAL[0][0], R6_SEAL[0][1], "LabyrinthRing6_EventScript_Seal")
    m.sign(R6_SEAL[1][0], R6_SEAL[1][1], "LabyrinthRing6_EventScript_Seal")
    m.sign(4, 31, "LabyrinthRing6_EventScript_Furnace")
    m.bgs.append({"type": "hidden_item", "x": 15, "y": 24, "elevation": 3, "item": "ITEM_PP_UP",
                  "flag": "FLAG_ICHOR_HIDDEN_ITEM_RING6_FALLS", "quantity": 1, "underfoot": False})
    m.item_ball(2, 31, "ITEM_TM_IRON_TAIL", "FLAG_ICHOR_RING6_ITEM_4")     # the bellows' corner
    for (x, y, name) in ((23, 4, "THREAD_ANCHOR_RING6_LANDING"), (25, 23, "THREAD_ANCHOR_RING6_DIALS"),
                         (7, 21, "THREAD_ANCHOR_RING6_FORGE"), (24, 41, "THREAD_ANCHOR_RING6_SHRINE")):
        m.anchor(x, y, name)
    rewards_at_dead_ends(m, ["ITEM_HYPER_POTION", "ITEM_MAX_REVIVE", "ITEM_HYPER_POTION"],
                         ["FLAG_ICHOR_RING6_ITEM_1", "FLAG_ICHOR_RING6_ITEM_2", "FLAG_ICHOR_RING6_ITEM_3"],
                         [("ITEM_ULTRA_BALL", "FLAG_ICHOR_HIDDEN_ITEM_RING6_A"),
                          ("ITEM_FULL_HEAL", "FLAG_ICHOR_HIDDEN_ITEM_RING6_B"),
                          ("ITEM_MAX_POTION", "FLAG_ICHOR_HIDDEN_ITEM_RING6_C")],
                         anchor_names=["THREAD_ANCHOR_RING6_WEST", "THREAD_ANCHOR_RING6_EAST",
                                       "THREAD_ANCHOR_RING6_DEEP"],
                         skip={(15, 24), (14, 24), (16, 24), (14, 25), (16, 25), (2, 31)})
    m.gen += ["call(LabyrinthRing6_EventScript_OnLoadExtra)"]
    if render:
        H.ensure_map(m.name, m.w, m.h, m.ts, "MUS_ICHOR_TITAN")
        extra = {(x, y) for bars in R6_BARS.values() for (x, y, _, _) in bars} | set(R6_TEACH_WALL) \
            | set(R6_SEAL) | {R6_ARCHIVE_BACK}
        m.build("labyrinth_ring6" + stem_suffix, starts=[(23, 3)],
                must_reach=[(7, 30, "the forge"), (42, 20, "the archive"), (41, 7, "the vault"),
                            (24, 41, "the shrine landing")],
                extra=extra, blockers=[],
                views=[(23, 7), (23, 18), (8, 20), (8, 34), (41, 17), (41, 6), (23, 29), (23, 39), (40, 36)])
        m.write_generated()
        write_bar_script(m)
    return m


def write_bar_script(m):
    """LabyrinthRing6_EventScript_DrawBars, generated from R6_BARS: each bar is open (slab)
    when its wheel stands where its corridor wants it, shut (a swung wall) otherwise."""
    lines = ["script LabyrinthRing6_EventScript_DrawBars {", "    call(LabyrinthRing6_EventScript_ReadDials)"]
    tvar = {0: "VAR_TEMP_5", 1: "VAR_TEMP_6", 2: "VAR_TEMP_7"}
    for name, bars in R6_BARS.items():
        lines.append(f"    // the {name} corridor")
        for (x, y, bit, want) in bars:
            slab = "METATILE_Mychos_SlabL" if (x + y) % 2 == 0 else "METATILE_Mychos_SlabR"
            lines += [f"    if (var({tvar[bit]}) == {want}) {{",
                      f"        setmetatile({x}, {y}, {slab}, FALSE)",
                      "    } else {",
                      f"        setmetatile({x}, {y}, METATILE_Mychos_DialFaceSeg, TRUE)",
                      "    }"]
    lines.append("}")
    block = "\n".join(lines)
    p = ROOT / "data/maps" / m.name / "scripts.pory"
    text = p.read_text()
    b0, b1 = "// ---- BEGIN GENERATED BARS ----", "// ---- END GENERATED BARS ----"
    a, b = text.index(b0) + len(b0), text.index(b1)
    p.write_text(text[:a] + "\n" + block + "\n" + text[b:])


# --------------------------------------------------------------------------
# Ring VII, the Choros (LABYRINTH §5.7, §6 Ring VII, Scene I; LABYRINTH_MAZE §1)
# --------------------------------------------------------------------------

R7_FLOOR = (14, 16)          # the dancing floor's A1 corner: 5 x 5, A-E west to east, 1-5 north to south
R7_DANCE = ["SXWRL", "LRLWR", "RWSXL", "RWLWW", "WXWLX"]
R7_STEPS = [(4, 4), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (2, 2)]   # E5 E4 E3 E2 D2 C2 B2 B3 C3
R7_MIRRORS = {"M1": (9, 13, "LEFT", "DOWN"), "M2": (9, 23, "UP", "RIGHT"), "M3": (12, 23, "DOWN", "UP")}
R7_CRYSTAL = (12, 18)
R7_TEACH = (26, 7)           # the teaching mirror under its own little shaft
R7_DISC = (26, 4)
R7_FRESCO = (3, 3)           # the faded fresco: three bays from here east


def ring7(stem_suffix="", render=True):
    m = H.HeartMap("LabyrinthRing7", "astra", 32, 32)
    # the landing below Ring VI's stair
    m.carve(13, 2, 18, 3, "m")
    # the dome: one vast cavern, its floor of cave rock round a marble ring
    m.draw(["    ........    ",
            "  ............  ",
            " .............. ",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            "................",
            " .............. ",
            " .............. ",
            "  ............  ",
            "    ........    "], 8, 11)
    fx, fy = R7_FLOOR
    m.carve(fx - 1, fy - 1, fx + 5, fy + 5, "m")              # the marble ring round the floor
    m.carve(fx, fy, fx + 4, fy + 4, "x")                      # the floor itself (no thread)
    m.carve(15, 4, 16, 10, ".")                               # down from the landing into the dome
    # the beam's path, kept clear: M1 down to M2, east to M3, up to the crystal
    (x1_, y1_, _, _), (x2_, y2_, _, _), (x3_, y3_, _, _) = R7_MIRRORS["M1"], R7_MIRRORS["M2"], R7_MIRRORS["M3"]
    m.carve(x1_, y1_, x2_, y2_, ".")
    m.carve(x2_, y2_, x3_, y3_, ".")
    m.carve(x3_, R7_CRYSTAL[1], x3_, y3_, ".")
    # the teaching antechamber (north-east) and the fresco corridor (north-west)
    m.carve(23, 3, 28, 8, "m")
    m.carve(R7_FRESCO[0], 6, R7_FRESCO[0] + 8, 6, "m")
    fixed = {(x, y) for y in range(m.h) for x in range(m.w) if m.T(x, y) != "R"}
    keep_off = set()
    for (x, y) in fixed:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                keep_off.add((x + dx, y + dy))
    for (x, y) in [(R7_FRESCO[0] + i, R7_FRESCO[1] + j) for i in range(9) for j in range(3)]:
        keep_off.add((x, y))
    mask = band(m, 1, 1, 30, 30, keep=keep_off)
    ports = [(12, 3), (19, 3), (22, 5), (12, 6), (2, 6), (7, 18), (24, 18), (16, 26), (9, 25), (22, 24), (15, 10), (20, 12)]
    maze(m, mask, seed=77, step=3, origin=(2, 2), braid=0.7, widen=0.05, ports=ports, rooms=0.03)
    for p in ports:
        m.cell(*p, ".")
    keep = fixed | set(ports)
    prune(m, keep=keep, short=2)
    braid_dead_ends(m, keep=keep, reach=4, allowed=mask, rng=random.Random(7), share=1.0)
    prune(m, keep=keep, short=2)
    return finish_ring7(m, stem_suffix, render)


def finish_ring7(m, stem_suffix, render):
    fx, fy = R7_FLOOR
    for j in range(5):
        for i in range(5):
            m.place(fx + i, fy + j, "dance", "blank", solid=False)
    # the stair up to Ring VI
    m.cell(15, 1, "M"); m.cell(16, 1, "M")
    m.place(15, 1, "stairs", "up_l", solid=False)
    m.place(16, 1, "stairs", "up_r", solid=False)
    # the mirrors' bases and the shaft of light (sunlight by day; ON_LOAD swaps starlight in)
    for name, (x, y, _, _) in R7_MIRRORS.items():
        m.place(x, y, "beam", "base", solid=True)
    m.place(R7_MIRRORS["M1"][0], R7_MIRRORS["M1"][1], "beam", "shaft_sun", solid=True)
    m.place(*R7_CRYSTAL, "beam", "base_b", solid=True)
    m.place(*R7_TEACH, "beam", "shaft_sun", solid=True)
    m.place(*R7_DISC, "beam", "base_b", solid=True)
    # the faded fresco of the whole dance, three bays
    for b in range(3):
        m.place_block(R7_FRESCO[0] + 3 * b, R7_FRESCO[1], "fresco_faded")
        for i in range(3):
            for j in range(3):
                m.cell(R7_FRESCO[0] + 3 * b + i, R7_FRESCO[1] + j, "M")
    # crystals and stalagmites round the dome, lamps at the landing
    for (x, y) in ((8, 15), (24, 15), (9, 25), (22, 25), (19, 11), (11, 11)):
        if m.walkable_t(x, y):
            m.place(x, y, "formations", "crystal_a" if (x + y) % 2 else "crystal_b", solid=True)
            m.notes[(x, y)] = "crystal"
    for x in (13, 18):
        m.place_block(x, 2, "lamp_stand")
    lay_dressing(m, seed=7)
    break_long_runs(m)
    m.lay()
    # the dome's ceiling: crystal stars set in the rock
    starred = 0
    for y in range(m.h):
        for x in range(m.w):
            if m.T(x, y) == "R" and (x, y) not in m.deco and int(m.mid[y, x]) == m.catalog["kit"].get("T|...", -1):
                if kit_hash(x, y) % 5 == 0:
                    m.set(x, y, m.pid("stars", "abcd"[kit_hash(x, y) % 4]), True)
                    starred += 1

    # --- events ---------------------------------------------------------------------------------
    m.warp(15, 1, "MAP_LABYRINTH_RING6", 2)              # 0
    m.warp(16, 1, "MAP_LABYRINTH_RING6", 3)              # 1
    m.warp(fx + 2, fy + 2, "MAP_LABYRINTH_STARRY_CHAMBER", 0)   # 2: the stair the dance opens
    m.warps[-1]["unreached_ok"] = True
    m.warps[-1]["_scripted"] = True
    m.header.update({"music": "MUS_ICHOR_HOLLOW", "map_type": "MAP_TYPE_UNDERGROUND", "allow_escaping": True,
                     "requires_flash": False})
    for name, (x, y, start, want) in R7_MIRRORS.items():
        m.obj("ICHOR_MIRROR", x, y, f"LabyrinthRing7_EventScript_Mirror{name[1]}",
              move="MOVEMENT_TYPE_ICHOR_MIRROR" + ("" if start == "DOWN" else "_" + start),
              local_id=f"LOCALID_RING7_{name}")
        m.objects[-1]["_floats"] = True
    m.obj("ICHOR_MIRROR_MARK", *R7_CRYSTAL, "LabyrinthRing7_EventScript_Crystal", local_id="LOCALID_RING7_CRYSTAL")
    m.objects[-1]["_floats"] = True
    m.obj("ICHOR_MIRROR", *R7_TEACH, "LabyrinthRing7_EventScript_TeachMirror",
          move="MOVEMENT_TYPE_ICHOR_MIRROR_LEFT", local_id="LOCALID_RING7_TEACH")
    m.objects[-1]["_floats"] = True
    m.obj("ICHOR_MIRROR_MARK", *R7_DISC, "LabyrinthRing7_EventScript_Disc", local_id="LOCALID_RING7_DISC")
    m.objects[-1]["_floats"] = True
    # Scene I: Ariadne, and the two Gigas on the dancing floor
    m.obj("ICHOR_TITAN_GRUNT", fx + 1, fy + 2, "0", move="MOVEMENT_TYPE_FACE_UP", local_id="LOCALID_RING7_PORPHYRION",
          flag="FLAG_ICHOR_HIDE_GIGAS_RING7")
    m.obj("ICHOR_TITAN_GRUNT", fx + 3, fy + 2, "0", move="MOVEMENT_TYPE_FACE_UP", local_id="LOCALID_RING7_GIGAS2",
          flag="FLAG_ICHOR_HIDE_GIGAS_RING7")
    m.obj("ICHOR_PRIESTESS", 13, 11, "LabyrinthRing7_EventScript_Ariadne", move="MOVEMENT_TYPE_FACE_DOWN",
          local_id="LOCALID_RING7_ARIADNE", flag="FLAG_ICHOR_HIDE_ARIADNE_RING7")
    for x in (15, 16):
        m.trigger(x, 9, "LabyrinthRing7_EventScript_SceneI", var="VAR_ICHOR_KNOSSA", value=14)
    # the dance: one trigger per square, live while VAR_TEMP_3 is 0
    for j in range(5):
        for i in range(5):
            m.trigger(fx + i, fy + j, f"LabyrinthRing7_EventScript_Step{j * 5 + i}", var="VAR_TEMP_3", value=0)
    for i in range(5):   # stepping back onto the south rim after a wrong step re-arms the floor
        m.trigger(fx + i, fy + 5, "LabyrinthRing7_EventScript_Rearm", var="VAR_TEMP_3", value=2)
    m.sign(R7_FRESCO[0] + 4, R7_FRESCO[1] + 2, "LabyrinthRing7_EventScript_Fresco")
    for (x, y, name) in ((15, 3, "THREAD_ANCHOR_RING7_STAIR"), (16, 12, "THREAD_ANCHOR_RING7_DOME"),
                         (7, 13, "THREAD_ANCHOR_RING7_MIRRORS")):
        m.anchor(x, y, name)
    rewards_at_dead_ends(m, ["ITEM_STAR_PIECE", "ITEM_MOON_STONE"], ["FLAG_ICHOR_RING7_ITEM_1", "FLAG_ICHOR_RING7_ITEM_2"],
                         [("ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_ITEM_RING7_A"),
                          ("ITEM_MAX_ETHER", "FLAG_ICHOR_HIDDEN_ITEM_RING7_B")],
                         anchor_names=["THREAD_ANCHOR_RING7_DEEP"])
    m.gen += ["call(LabyrinthRing7_EventScript_OnLoadExtra)"]
    if render:
        H.ensure_map(m.name, m.w, m.h, m.ts, "MUS_ICHOR_HOLLOW")
        m.build("labyrinth_ring7" + stem_suffix, starts=[(15, 2)],
                must_reach=[(fx + 2, fy + 5, "the dancing floor's south edge"), (12, 19, "the crystal")],
                views=[(15, 5), (16, 18), (7, 18), (25, 6), (6, 6), (16, 26)])
        m.write_generated()
        write_dance_script(m)
    return m


NOTE = {"X": "SE_NOTE_D", "W": "SE_NOTE_E", "L": "SE_NOTE_F", "R": "SE_NOTE_G", "S": "SE_NOTE_A"}


def write_dance_script(m):
    """The crane dance's scripts (LABYRINTH §5.7), generated from R7_DANCE and R7_STEPS."""
    fx, fy = R7_FLOOR
    L = []
    for j in range(5):
        for i in range(5):
            L += [f"script LabyrinthRing7_EventScript_Step{j * 5 + i} {{",
                  f"    setvar(VAR_0x8008, {j * 5 + i})", "    goto(LabyrinthRing7_EventScript_Step)", "}", ""]
    L += ["script LabyrinthRing7_EventScript_Step {", "    lockall", "    switch (var(VAR_TEMP_1)) {"]
    for n, (i, j) in enumerate(R7_STEPS):
        L += [f"        case {n}:", f"            if (var(VAR_0x8008) != {j * 5 + i}) {{",
              "                goto(LabyrinthRing7_EventScript_Wrong)", "            }"]
    L += ["    }", "    switch (var(VAR_0x8008)) {"]
    for j in range(5):
        for i in range(5):
            sym = R7_DANCE[j][i]
            L += [f"        case {j * 5 + i}:", f"            setmetatile({fx + i}, {fy + j}, METATILE_Astra_Dance{sym}Lit, FALSE)",
                  f"            playse({NOTE[sym]})"]
    L += ["    }", "    special(DrawWholeMapView)", "    addvar(VAR_TEMP_1, 1)",
          f"    if (var(VAR_TEMP_1) == {len(R7_STEPS)}) {{", "        goto(LabyrinthRing7_EventScript_Danced)", "    }",
          "    releaseall", "}", ""]
    L += ["script LabyrinthRing7_EventScript_RevealFloor {"]
    for j in range(5):
        for i in range(5):
            L.append(f"    setmetatile({fx + i}, {fy + j}, METATILE_Astra_Dance{R7_DANCE[j][i]}, FALSE)")
    L += ["}", "", "script LabyrinthRing7_EventScript_LightDance {"]
    for (i, j) in R7_STEPS:
        L.append(f"    setmetatile({fx + i}, {fy + j}, METATILE_Astra_Dance{R7_DANCE[j][i]}Lit, FALSE)")
    L += ["}", "", "script LabyrinthRing7_EventScript_Bays {"]
    P = m.P
    for b, key in enumerate(("fresco_iv", "fresco_v", "fresco_vi")):
        for cy in range(3):
            for cx in range(3):
                L.append(f"    setmetatile({R7_FRESCO[0] + 3 * b + cx}, {R7_FRESCO[1] + cy}, 0x{P[key]['ids'][cy][cx]:03X}, TRUE)")
    L += ["}"]
    block = "\n".join(L)
    p = ROOT / "data/maps" / m.name / "scripts.pory"
    text = p.read_text()
    b0, b1 = "// ---- BEGIN GENERATED DANCE ----", "// ---- END GENERATED DANCE ----"
    a, b = text.index(b0) + len(b0), text.index(b1)
    p.write_text(text[:a] + "\n" + block + "\n" + text[b:])


def kit_hash(x, y):
    return H.kit.h("star", x, y)


BUILDERS = {"ring5": ring5, "ring6": ring6, "ring7": ring7}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("maps", nargs="*")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--stem-suffix", default="")
    ap.add_argument("--ascii", action="store_true")
    args = ap.parse_args()
    for name in args.maps or list(BUILDERS):
        m = BUILDERS[name](args.stem_suffix, not args.no_render)
        if args.ascii:
            print(m.ascii())
        stats_report(m)


if __name__ == "__main__":
    main()
