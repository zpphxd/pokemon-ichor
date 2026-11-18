"""Ring II, the Runner's Ring (design/LABYRINTH.md §6 Ring II, LABYRINTH_MAZE.md,
design/maps/LabyrinthRing2.md).

Hermes's verb: race and route. From the stair, one corridor reaches a fork of two
carved gates, the sun gate (open by day) and the moon gate (open by night): one
reaches the TM room, the other the Moon Room and its sunken floor. Both feed a
maze that meets in the Long Hall, where Asterion is first seen (scene C) and
breaks a cracked wall. Then the heralds' way: three bronze plates, each opening a
grate for a few steps, the gates 8-10 steps from their plates. Off the east side
the old cave grotto takes the trickle where the stream begins, Ring I's hole and
a flowstone climb back up.
"""
from __future__ import annotations

from labyrinth_lib import Maze, cell, gap, cave_grid, state_diff, setmetatiles
from kythera_maps import DIRS4

NAME = "LabyrinthRing2"
W, H = 54, 42                # 13 x 10 nodes
SEED = 9
P = NAME + "_EventScript_"

ENTRY = (0, 0, 1, 1)
TMROOM = (1, 3, 2, 4)
MOONROOM = (5, 2, 6, 3)
HALL = (3, 5, 7, 6)
GROTTO = (10, 0, 12, 1)
STAIRS = (10, 8, 12, 9)
SUN_GATE = ((2, 1), (2, 2))
MOON_GATE = ((4, 1), (4, 2))
# the heralds' way: (plate node, path to the gate, gate edge)
HERALDS = [
    ((8, 4), [(8, 4), (9, 4), (10, 4)], ((10, 4), (11, 4))),
    ((11, 5), [(11, 5), (11, 6), (10, 6)], ((10, 6), (9, 6))),
    ((9, 7), [(9, 7), (9, 8)], ((9, 8), (10, 8))),
]
CRACK_ALCOVE = ((5, 6), (5, 7))     # the Long Hall's cracked wall and the Full Heal behind it

SPINE = [
    [(1, 1), (2, 1), (3, 1), (4, 1)],                 # the entry to the fork
    [(2, 2), (2, 3)],                                 # sun gate -> the TM room
    [(4, 2), (5, 2)],                                 # moon gate -> the Moon Room
    [(7, 5), (8, 5), (8, 4)],                         # the Long Hall -> the first plate
    [(9, 4), (10, 4)], [(8, 4), (9, 4)],
    [(11, 4), (11, 5), (11, 6), (10, 6)],             # after gate 1 -> plate 2 -> gate 2
    [(9, 6), (9, 7), (9, 8)],                         # after gate 2 -> plate 3 -> gate 3
    [(9, 2), (10, 2)], [(10, 2), (10, 1)],            # the grotto's way into the maze
]
HERALD_NODES = {(8, 4), (9, 4), (10, 4), (11, 4), (11, 5), (11, 6), (10, 6), (9, 6), (9, 7), (9, 8)}
NORTH = {(2, 0), (3, 0), (4, 0), (2, 1), (3, 1), (4, 1)}
CAVE_NODES = {(9, 0), (9, 1), (9, 2), (10, 2), (11, 2), (12, 2), (10, 0), (11, 0), (12, 0), (10, 1),
              (11, 1), (12, 1), (0, 7), (0, 8), (0, 9), (1, 8), (1, 9), (2, 9), (12, 3), (12, 4),
              (3, 9), (4, 9), (5, 9), (6, 9), (5, 8), (7, 9)}


def closed():
    keep = []
    allowed = set()
    for path in SPINE:
        for a, b in zip(path, path[1:]):
            allowed.add(frozenset({a, b}))
    for (_, path, g) in HERALDS:
        for a, b in zip(path, path[1:]):
            allowed.add(frozenset({a, b}))
    allowed |= {frozenset({(7, 5), (8, 5)})}
    # above the fork: a short comb, not a room (the shrine at (2,0), the fresco at (4,0))
    allowed |= {frozenset(e) for e in (((3, 0), (3, 1)), ((2, 0), (3, 0)), ((4, 0), (3, 0)))}
    guarded = HERALD_NODES | NORTH | {(8, 5)}
    for n in guarded:
        for dx, dy in DIRS4:
            m = (n[0] + dx, n[1] + dy)
            if 0 <= m[0] < 13 and 0 <= m[1] < 10 and frozenset({n, m}) not in allowed:
                keep.append((n, m))
    for (_, _, g) in HERALDS:
        keep.append(g)
    keep += [SUN_GATE, MOON_GATE, CRACK_ALCOVE, ((0, 1), (0, 2)), ((1, 1), (1, 2))]
    # the stair room's north wall stays whole above the stair
    keep += [((12, 7), (12, 8)), ((11, 7), (11, 8))]
    # the Moon Room and the TM room open only by their gates and one way out each
    for (x0, y0, x1, y1), outs in ((MOONROOM, {((6, 3), (6, 4))}), (TMROOM, {((1, 4), (1, 5))})):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                for dx, dy in DIRS4:
                    m = (x + dx, y + dy)
                    if x0 <= m[0] <= x1 and y0 <= m[1] <= y1:
                        continue
                    e = ((x, y), m)
                    if frozenset(e) in {frozenset(o) for o in outs} or frozenset(e) in allowed:
                        continue
                    keep.append(e)
    return keep


def maze(seed=SEED):
    mz = Maze(13, 10, seed)
    mz.off |= {(9, 5), (10, 5)}          # solid rock inside the heralds' way
    for r in (ENTRY, TMROOM, MOONROOM, HALL, GROTTO, STAIRS):
        mz.room(*r)
    for path in SPINE:
        for a, b in zip(path, path[1:]):
            mz.link(a, b)
    for (_, path, g) in HERALDS:
        for a, b in zip(path, path[1:]):
            mz.link(a, b)
    mz.link((6, 3), (6, 4))
    mz.link((1, 4), (1, 5))
    keep = closed()
    for n in mz.nodes():
        if mz.deg(n) == 0:
            mz.carve(n, keep=keep)
    protect = {CRACK_ALCOVE[1]}
    mz.braid(0.75, keep_dead=protect, keep=keep)
    mz.crossings(12, keep=keep, avoid=HERALD_NODES | NORTH | protect)
    # the alcove behind the cracked wall: reached only through it
    for dx, dy in DIRS4:
        m = (CRACK_ALCOVE[1][0] + dx, CRACK_ALCOVE[1][1] + dy)
        mz.unlink(CRACK_ALCOVE[1], m)
    return mz


def grid_of(mz):
    return cave_grid(mz, W, H, CAVE_NODES, seed=4)


def build(render=True):
    from labyrinth_lib import LMap, mid, dest
    from labyrinth_upper import DARK
    mz = maze()
    g = grid_of(mz)
    # the trickle: the stream's first water, down a cleft in the grotto
    for y in range(2, 8):
        g[y][51] = "~"
    for y in range(3, 8, 2):
        g[y][50] = ";"
    m = LMap(NAME, W, H, dict(DARK))
    m.g = [row[:] for row in g]
    m.g0 = [row[:] for row in g]
    # the heralds' plates
    plates = []
    for (pn, _, _) in HERALDS:
        x, y = cell(pn)
        m.g[y][x] = "P"
        plates.append((x, y))
    from labyrinth_lib import notch
    keep = {(x, y) for e in (SUN_GATE, MOON_GATE, CRACK_ALCOVE) + tuple(h[2] for h in HERALDS)
            for (gx, gy) in gap(*e) for x in (gx - 1, gx, gx + 1) for y in (gy - 1, gy, gy + 1)}
    keep |= {(x, 1) for x in (3, 4, 5, 6, 9, 10, 11, 18, 19, 20)} | {(x, y) for x in range(48, 53) for y in range(0, 3)}
    keep |= {(x, 33) for x in range(48, 54)}
    notch(m.g, keep=keep)
    m.g0 = [row[:] for row in m.g]
    m.lay()

    # --- the stairs, anchors, gates -------------------------------------------------------
    m.stairs(4, 1, "up")
    m.anchor(4, 2, "THREAD_ANCHOR_R2_ENTRANCE")
    m.stairs(50, 33, "down")
    m.anchor(50, 34, "THREAD_ANCHOR_R2_HERALDS")
    m.anchor(22, 24, "THREAD_ANCHOR_R2_LONG_HALL")
    m.anchor(44, 6, "THREAD_ANCHOR_R2_GROTTO")
    gen = []

    def opened(edges):
        g2 = [row[:] for row in m.g0]
        for e in edges:
            for (x, y) in gap(*e):
                g2[y][x] = "," if g2[y][x] == "%" else "."
        return state_diff(m, g2)

    def door_face(e):
        """The face cells of a closed vertical gate (the row seen from the south)."""
        cells = gap(*e)
        return sorted([c for c in cells if c[1] == max(cc[1] for cc in cells)])
    sun_open, moon_open = opened([SUN_GATE]), opened([MOON_GATE])
    for (x, y) in door_face(SUN_GATE):
        m.named("doorways", "sun", x, y)
    for (x, y) in door_face(MOON_GATE):
        m.named("doorways", "moon", x, y)
    gen += ["gettimeofday", "if (var(VAR_0x8000) == TIME_NIGHT) {"]
    gen += setmetatiles(moon_open, "    ")
    gen += ["} else {"] + setmetatiles(sun_open, "    ") + ["}"]
    # herald gates: shut by default (grates on their face rows); open while a run is on
    for k, (_, _, e) in enumerate(HERALDS, 1):
        for (x, y) in gap(*e):
            if (e[0][1] == e[1][1]):        # east-west gate: grate the whole gap's face... use both cells of each row
                pass
        cells = gap(*e)
        for (x, y) in cells:
            m.named("doorways", "grate", x, y)
    herald_open = {k: opened([e]) for k, (_, _, e) in enumerate(HERALDS, 1)}
    for k in herald_open:
        shut = [(x, y, int(m.mid[y, x]), bool(m.solid[y, x])) for (x, y, _, _) in herald_open[k]]
        gen += [f"if (var(VAR_TEMP_3) == {k} || flag(FLAG_TEMP_{k})) {{"] + setmetatiles(herald_open[k], "    ")
        gen += ["} else {"] + setmetatiles(shut, "    ") + ["}"]
    # the cracked wall (scene C) and the alcove behind it
    crack_cells = [c for c in gap(*CRACK_ALCOVE) if c[1] == min(cc[1] for cc in gap(*CRACK_ALCOVE))]
    for (x, y) in crack_cells:
        m.named("cracked", "face", x, y)
    wall_open = opened([CRACK_ALCOVE])
    gen += ["if (flag(FLAG_ICHOR_R2_LONG_HALL)) {"] + setmetatiles(wall_open, "    ") + ["}"]
    m.gen = gen

    # --- events ------------------------------------------------------------------------------
    m.arrival(4, 2)                                                   # 0: down from Ring I
    m.warp(4, 1, "MAP_LABYRINTH_RING1", 3)                           # 1, 2: the stair up
    m.warp(5, 1, "MAP_LABYRINTH_RING1", 3)
    m.arrival(44, 3)                                                  # 3: Ring I's hole lands here
    m.warp(50, 33, "MAP_LABYRINTH_RING3", 0)                         # 4, 5: the stair down
    m.warp(51, 33, "MAP_LABYRINTH_RING3", 0)
    m.arrival(50, 34)                                                 # 6: up from Ring III

    # the sunken floor in the Moon Room, and the flowstone climb in the grotto
    mx, my = cell((6, 3), 1, 1)
    m.put("hole", mx, my)
    m.stops.add((mx, my))
    m.trigger(mx, my, P + "SunkenFloor")
    m.trigger(49, 2, P + "Climb")
    m.sign(49, 1, P + "ClimbSign")
    # scene C: entering the Long Hall from the west or the north
    for cx in (20, 29):
        for y in range(22, 28):
            if m.at(cx, y) in ".,":
                m.trigger(cx, y, P + "SceneC", var="VAR_TEMP_4", value="0")
    m.trigger(51, 34, P + "StairDown")
    m.sign(*crack_cells[0], P + "CrackedWall")
    m.sign(*crack_cells[1], P + "CrackedWall")
    # the heralds: each plate starts a run; every cell of the run burns a step
    for k, ((pn, path, e), (px, py)) in enumerate(zip(HERALDS, plates), 1):
        m.trigger(px, py, P + f"Plate{k}")
        bx, by = cell(e[1])
        for (x, y) in [(bx, by), (bx + 1, by), (bx, by + 1), (bx + 1, by + 1)]:
            m.trigger(x, y, P + f"Past{k}")
        run = set()
        for n in path:
            if n == pn:
                continue
            run |= {cell(n, i, j) for i in range(2) for j in range(2)}
        for a, b in zip(path, path[1:]):
            run |= set(gap(a, b))
        run |= set(gap(*e))
        for (x, y) in sorted(run):
            m.trigger(x, y, P + "RunStep", var="VAR_TEMP_3", value=str(k))
    # people
    m.obj("ICHOR_TITAN_GRUNT", 47, 35, P + "Tephra", move="MOVEMENT_TYPE_FACE_RIGHT", trainer=True,
          sight=4, local_id="LOCALID_R2_TEPHRA")
    dead = [n for n in mz.metrics()["dead"] if isinstance(n[0], int) and n not in HERALD_NODES]
    m.dead = dead
    return m, mz, dead


VIEWS = [(6, 5), (18, 6), (44, 5), (8, 16), (22, 24), (40, 18), (8, 34), (26, 34), (46, 36)]


def finish(m, mz, dead, render=True):
    """Items and the optional scout at the dead ends, then check and write."""
    P_ = P
    loot = [("ITEM_MAX_REPEL", "FLAG_ICHOR_ITEM_R2_MAX_REPEL"), ("ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_R2_ULTRA_BALL")]
    hidden = [("ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_ITEM_R2_OBOL")]
    # rooms' own rewards
    tx, ty = cell((1, 3), 0, 0)
    m.item(tx, ty, "ITEM_TM_SHOCK_WAVE", "FLAG_ICHOR_ITEM_R2_TM")
    mx, my = cell((5, 2), 0, 0)
    m.item(mx, my, "ITEM_MOON_STONE", "FLAG_ICHOR_ITEM_R2_MOON_STONE")
    m.hidden(mx + 2, my + 2, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_ITEM_R2_STARDUST")
    ax, ay = cell(CRACK_ALCOVE[1], 0, 1)
    m.item(ax, ay, "ITEM_FULL_HEAL", "FLAG_ICHOR_ITEM_R2_FULL_HEAL")
    gx, gy = (48, 6)
    m.item(gx, gy, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_R2_ULTRA_BALL")
    loot = loot[:1]
    placed = []
    others = [n for n in dead if n != CRACK_ALCOVE[1] and n not in NORTH]
    # the comb above the fork: a goddess's shrine, and the fresco of the herald
    sx, sy = cell((2, 0))
    m.named("niche", "shrine", sx, sy - 1)
    m.sign(sx, sy - 1, P_ + "Shrine")
    fx, fy = cell((4, 0))
    m.named("niche", "back", fx + 1, fy - 1)
    m.sign(fx + 1, fy - 1, P_ + "FrescoHerald")
    m.hidden(fx, fy, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_ITEM_R2_OBOL")
    hidden = []
    for i, n in enumerate(others):
        x, y = cell(n)
        if i == 0:
            # the optional scout's gallery: Sinopos and the Silver Owl
            m.obj("ICHOR_TITAN_GRUNT", x, y + 1, P_ + "Sinopos", move="MOVEMENT_TYPE_FACE_UP", trainer=True,
                  sight=1, local_id="LOCALID_R2_SINOPOS")
            m.item(x, y, "ITEM_RELIC_SILVER", "FLAG_ICHOR_ITEM_R2_SILVER_OWL")
        elif loot:
            it, fl = loot.pop()
            m.item(x, y, it, fl)
        elif hidden:
            it, fl = hidden.pop()
            m.hidden(x, y, it, fl)
        elif len(m.anchors) < 8:
            m.anchor(x, y, "THREAD_ANCHOR_UNNAMED")
        else:
            m.sign(x, y - 1, P_ + "Fresco")
        placed.append(n)
    starts = [(4, 2)]
    m.forced_open = set()
    for e in (SUN_GATE, MOON_GATE, CRACK_ALCOVE) + tuple(h[2] for h in HERALDS):
        m.forced_open |= set(gap(*e))
    m.stops |= m.forced_open
    import labyrinth_extras as X
    from labyrinth_lib import mid as mid_
    grate = mid_("doorways", "grate")
    X.block_gap(m, (1, 1), (2, 1), "rubble", "the only way out of the stair room: the ceiling came down")
    X.block_gap(m, (9, 2), (10, 2), "roots", "roots from far above choke the way into the grotto")

    def lanes(y, xs):
        return [(x, y, int(m.mid[y, x]), False, grate, True) for x in xs]
    room = lambda x0, y0, x1, y1, skip: [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
                                         if (x, y) not in skip and m.walkable(x, y)]
    X.plate_puzzle(m, "Sun", [(8, 16)], [(8, 18)], lanes(20, (6, 7)), "FLAG_TEMP_4",
                   room(6, 14, 11, 19, {(8, 16), (8, 18)}), (10, 13, 9, 15), P,
                   "the TM room's way on is grated until a drum sits on its plate (Ring II teaches the idea)")
    X.plate_puzzle(m, "Moon", [(23, 12), (25, 12)], [(23, 14), (25, 14)], lanes(16, (26, 27)), "FLAG_TEMP_5",
                   room(22, 10, 27, 15, {(23, 12), (25, 12), (23, 14), (25, 14), (27, 15)}), (24, 9, 24, 11), P,
                   "the Moon Room's way on: two drums, two plates")
    X.remains(m, 44, 9, P, "1", "A dropped sandal, the strap cut clean through, by the trickle.")
    X.remains(m, 22, 21, P, "2", "Carved shallow in the Long Hall's wall: IT RAN AT THE FIRE, NOT AT US.")
    slots = X.free_dead_ends(m, mz)
    if slots:
        X.later_gate(m, slots[0], "chain", "FLAG_ICHOR_HIDE_R2_SEAL", P, "2", "Taurivet", 52, "FLAG_ICHOR_R2_STATIC",
                     "ITEM_RELIC_SILVER", "FLAG_ICHOR_ITEM_R2_SHRINE",
                     "the runners' shrine behind a labrys seal: a stray of the palace herd that found its way down")
    X.cellar_entries(m, mz, [2, 3], P)
    m.break_runs(starts)
    import labyrinth_turning as TURN
    TURN.lmap(m, (50, 34), (4, 1))   # the Turning: up from Ring III to the stair to Ring I
    errs, reach = m.build("labyrinth_ring2", starts, views=VIEWS, render=render)
    return errs


if __name__ == "__main__":
    import sys
    m, mz, dead = build()
    met = mz.metrics()
    print({k: met[k] for k in ("nodes", "edges", "loops", "junctions", "dead_ends", "components")}, dead)
    if "--plan" in sys.argv:
        print(mz.sketch())
    finish(m, mz, dead, render="--no-render" not in sys.argv)
