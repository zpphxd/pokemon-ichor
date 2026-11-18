"""Ring III, the Mysteries (design/LABYRINTH.md §6 Ring III, LABYRINTH_MAZE.md,
design/maps/LabyrinthRing3.md).

Demeter's verb: dark and light. The ring is pitch dark and its corridors are
strung with webs. Two ways reach Daedalus's workshop: the front way burns
through the webs past Automaton No. 3 to the front door; the back way is
Daedalus's own, marked with labrys signs in glow-paint that only show with the
torch doused, to the back door. The stream runs down the ring's east side in a
cave channel, crossed at one ford; the old cave in the south-west hides a hole
down to the Titans' dig in Ring IV, and a sealed web pocket catches whoever
falls through Ring II's sunken floor.
"""
from __future__ import annotations

from collections import deque

from labyrinth_lib import Maze, cell, gap, cave_grid, notch, mid, ST, PITCH
from kythera_maps import DIRS4
import labyrinth_tiles as LT

NAME = "LabyrinthRing3"
W, H = 54, 46                # 13 x 11 nodes
SEED = 3
P = NAME + "_EventScript_"

ENTRY = (0, 0, 1, 1)
NO7 = (4, 8, 5, 9)
FRONT = (6, 9, 8, 10)
BACK = (12, 3, 12, 4)
POCKET = (2, 4)
POCKET_EXIT = ((2, 4), (2, 5))
FRONT_DOOR = (30, 37)        # in the front room's north face
BACK_DOOR = (50, 13)         # in the back room's north face
STREAM_X = (44, 45)          # the channel, between node columns 10 and 11
FORD_Y = ()          # no ford: the back way needs Poseidon's Conch
CAVE_NODES = {(11, y) for y in range(11)} | {(12, y) for y in range(11)} | {(10, 0), (10, 1)} | \
             {POCKET, (1, 4), (0, 8), (1, 8), (0, 9), (1, 9), (2, 9), (0, 10), (1, 10), (2, 10), (3, 10)}


def maze(seed=SEED):
    mz = Maze(13, 11, seed)
    for r in (ENTRY, NO7, FRONT, BACK):
        mz.room(*r)
    keep = [POCKET_EXIT, ((2, 4), (1, 4)), ((2, 4), (3, 4)), ((2, 4), (2, 3)),
            ((12, 3), (12, 2)), ((12, 4), (12, 5)), ((6, 9), (6, 8)), ((7, 9), (7, 8)), ((8, 9), (8, 8)),
            ((4, 8), (3, 8)), ((4, 8), (4, 7)), ((5, 8), (5, 7)), ((4, 9), (3, 9)), ((5, 9), (6, 9)),
            ((4, 9), (4, 10)), ((5, 9), (5, 10)), ((8, 10), (9, 10))]
    # the stream channel splits node columns 10 and 11 except at the ford (row 7)
    for y in range(11):
        if y != 7:
            keep.append(((10, y), (11, y)))
    mz.link((5, 8), (6, 8))       # No. 7's door
    mz.link((8, 9), (9, 9))       # the front room's way in (Automaton No. 3)
    mz.link((12, 4), (11, 4))     # the back room's way in
    mz.link(POCKET, (1, 4))       # the pocket's one way out, webbed
    mz.link((1, 4), (1, 5))
    mz.carve((1, 1), keep=keep)
    for n in mz.nodes():
        if mz.deg(n) == 0:
            mz.carve(n, keep=keep)
    mz.braid(0.7, keep_dead={POCKET}, keep=keep)
    mz.crossings(14, keep=keep, avoid={POCKET, (1, 4)})
    return mz


def grid_of(mz):
    g = cave_grid(mz, W, H, CAVE_NODES, seed=6)
    # the stream: a channel two cells wide down the cave, with one ford
    for y in range(1, H - 1):
        for x in STREAM_X:
            if y in FORD_Y:
                g[y][x] = ";"
            elif g[y][x] in "%#,":
                g[y][x] = "~"
    for y in range(1, H - 1):       # rock either side of the channel where it isn't floor
        for x in (STREAM_X[0] - 1, STREAM_X[1] + 1):
            pass
    # the islet with the Big Pearl
    g[18][44] = ","
    return g


def walk(g, start, blocked=(), surf=False):
    d = {start: 0}
    prev = {}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in DIRS4:
            n = (x + dx, y + dy)
            if n in d or n in blocked or not (0 <= n[0] < W and 0 <= n[1] < H):
                continue
            if g[n[1]][n[0]] in ("#%o" if surf else "#%~o"):
                continue
            d[n] = d[(x, y)] + 1
            prev[n] = (x, y)
            q.append(n)
    return d, prev


def path(prev, a, b):
    out = [b]
    while out[-1] != a:
        out.append(prev[out[-1]])
    return out[::-1]


def build(render=True):
    from labyrinth_lib import LMap, setmetatiles
    from labyrinth_upper import DARK
    mz = maze()
    g = grid_of(mz)
    hdr = dict(DARK)
    m = LMap(NAME, W, H, hdr)
    m.g = g
    keep = {(x, y) for x in range(3, 8) for y in range(0, 3)} | {(FRONT_DOOR[0] + i, FRONT_DOOR[1] + j)
                                                                  for i in (-1, 0, 1) for j in (-1, 0)}
    keep |= {(BACK_DOOR[0] + i, BACK_DOOR[1] + j) for i in (-1, 0, 1) for j in (-1, 0)}
    keep |= {(x, y) for x in range(STREAM_X[0] - 1, STREAM_X[1] + 2) for y in range(H)}
    notch(m.g, keep=keep)
    m.g0 = [row[:] for row in m.g]
    m.lay()

    start = (4, 2)
    m.stairs(4, 1, "up")
    m.anchor(*start, "THREAD_ANCHOR_R3_ENTRANCE")
    # the doors into the workshop: the arcade's door cell in a masonry face
    door = LT.mid("labyrinth", "arcade", "door_pier")
    door_cell = ST["arcade"]["ids"][2][4]
    for (x, y) in (FRONT_DOOR, BACK_DOOR):
        m.set(x, y, door_cell, False)
        m.stops.add((x, y))
    m.anchor(FRONT_DOOR[0], FRONT_DOOR[1] + 1, "THREAD_ANCHOR_R3_WORKSHOP_DOOR")

    # --- the two ways: the glow trail (back) and the webs (front) -----------------------
    d, prev = walk(m.g, start)
    ds, prevs = walk(m.g, start, surf=True)
    back = path(prevs, start, (BACK_DOOR[0], BACK_DOOR[1] + 1))
    front = path(prev, start, (FRONT_DOOR[0], FRONT_DOOR[1] + 1))
    backset = set(back)
    # glow-marks: a labrys sign on a wall top beside the trail wherever it turns or branches
    names = {v: k for k, v in ((k, LT.mid("labyrinth", "walls", k)) for k in ST["walls"]["names"])}
    glows = []
    for i in range(1, len(back) - 1):
        (x, y) = back[i]
        nx, ny = back[i + 1]
        branches = sum(m.walkable(x + dx, y + dy) for dx, dy in DIRS4)
        if branches < 3 and (i % 7):
            continue
        for dx, dy in DIRS4:
            wx, wy = x + dx, y + dy
            if not m.ok(wx, wy) or m.at(wx, wy) != "#":
                continue
            kit = names.get(int(m.mid[wy, wx]))
            if kit in ("top", "top_n", "top_w", "top_e", "top_we"):
                if kit == "top":
                    a = {(0, -1): "arrow_n", (-1, 0): "arrow_w", (1, 0): "arrow_e"}.get((nx - x, ny - y), "top")
                    m.named("glow", a, wx, wy)
                else:
                    m.named("glow", kit, wx, wy)
                glows.append((wx, wy))
                break
    m.glows = glows
    # webs across the front way's passages, never on the trail
    webs = []
    for i in range(6, len(front) - 4):
        if len(webs) >= 3:
            break
        x, y = front[i]
        nx, ny = front[i + 1]
        if (x, y) in backset or (nx, ny) in backset:
            continue
        if any(abs(x - wx) + abs(y - wy) < 10 for (wx, wy, _) in webs):
            continue
        if nx != x and m.walkable(x, y + 1) and m.walkable(nx, y + 1) and not m.walkable(x, y - 1):
            webs.append((nx, y, "h"))           # a curtain across an east-west passage
        elif ny != y and m.walkable(x + 1, y) and m.walkable(x + 1, ny) and not m.walkable(x - 1, y):
            webs.append((x, ny, "v"))
    m.webs = webs
    return m, mz, front, back


VIEWS = [(6, 4), (20, 6), (46, 6), (8, 18), (24, 20), (46, 22), (10, 38), (30, 38), (48, 38)]


def finish(m, mz, front, back, render=True):
    from labyrinth_lib import setmetatiles
    obj = m.obj
    # the webs: two strands each, each its own object (burn either to pass)
    for k, (x, y, kind) in enumerate(m.webs, 1):
        cells = [(x, y), (x, y + 1)] if kind == "h" else [(x, y), (x + 1, y)]
        for j, (cx, cy) in enumerate(cells):
            obj("CUTTABLE_TREE", cx, cy, P + "Web", flag=f"FLAG_ICHOR_HIDE_R3_WEB_{k}{'AB'[j]}")
    # the web pocket under Ring II's sunken floor: its one way out is webbed
    px, py = cell((2, 4))
    gx = gap(*POCKET_EXIT[::-1][::-1])
    pocket_gap = gap(POCKET, (1, 4))
    wx = min(c[0] for c in pocket_gap)
    obj("CUTTABLE_TREE", wx, py, P + "Web", flag="FLAG_ICHOR_HIDE_R3_WEB_4A")
    obj("CUTTABLE_TREE", wx, py + 1, P + "Web", flag="FLAG_ICHOR_HIDE_R3_WEB_4B")
    m.item(px + 1, py, "ITEM_RARE_BONE", "FLAG_ICHOR_ITEM_R3_RARE_BONE")
    # people and rooms
    nx_, ny_ = cell((8, 9))
    obj("ICHOR_HOPLITE", nx_ + 2, ny_, P + "Automaton3", move="MOVEMENT_TYPE_FACE_RIGHT", trainer=True,
        sight=3, local_id="LOCALID_R3_AUTOMATON_3")
    sx, sy = cell((4, 8))
    obj("ICHOR_HOPLITE", sx + 2, sy + 1, P + "Automaton7", move="MOVEMENT_TYPE_FACE_DOWN", trainer=True,
        sight=2, local_id="LOCALID_R3_AUTOMATON_7")
    m.item(sx, sy, "ITEM_TM_SHADOW_BALL", "FLAG_ICHOR_ITEM_R3_TM")
    m.item(44, 18, "ITEM_BIG_PEARL", "FLAG_ICHOR_ITEM_R3_PEARL")
    for (x, y) in m.glows[:1]:
        m.sign(x, y, P + "GlowSign")
    # dead ends: the first web's Max Ether, the trail's Star Piece, a Revive, the hole down
    dead = [n for n in mz.metrics()["dead"] if isinstance(n[0], int) and n != POCKET]
    backn = {((x - 2) // PITCH, (y - 2) // PITCH) for (x, y) in back}
    rewards = [("item", "ITEM_STAR_PIECE", "FLAG_ICHOR_ITEM_R3_STAR_PIECE"),
               ("item", "ITEM_MAX_ETHER", "FLAG_ICHOR_ITEM_R3_MAX_ETHER"),
               ("hole", None, None), ("hidden", "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_ITEM_R3_REVIVE")]
    dead.sort(key=lambda n: (n not in backn and min(abs(n[0] - a) + abs(n[1] - b) for (a, b) in backn) > 1, n))
    for n, (kind, it, fl) in zip(dead, rewards):
        x, y = cell(n)
        if kind == "item":
            m.item(x, y, it, fl)
        elif kind == "hidden":
            m.hidden(x, y, it, fl)
        else:
            m.put("hole", x, y)
            m.stops.add((x, y))
            m.trigger(x, y, P + "Hole")
    for n in dead[len(rewards):]:
        x, y = cell(n)
        if len(m.anchors) < 8:
            m.anchor(x + 1, y + 1, "THREAD_ANCHOR_UNNAMED")
    # warps
    m.arrival(4, 2)                                               # 0: down from Ring II
    m.warp(4, 1, "MAP_LABYRINTH_RING2", 6)                        # 1, 2: the stair up
    m.warp(5, 1, "MAP_LABYRINTH_RING2", 6)
    m.arrival(px, py + 1)                                         # 3: the web pocket
    m.warp(*FRONT_DOOR, "MAP_LABYRINTH_WORKSHOP", 0)              # 4: the front door
    m.warp(*BACK_DOOR, "MAP_LABYRINTH_WORKSHOP", 1)               # 5: the back door
    m.arrival(FRONT_DOOR[0], FRONT_DOOR[1] + 1)                   # 6, 7: out of the workshop
    m.arrival(BACK_DOOR[0], BACK_DOOR[1] + 1)
    m.gen = []
    starts = [(4, 2)]
    blockers = set()
    m.forced_open = set()
    import labyrinth_extras as X
    from labyrinth_lib import mid as mid_
    X.block_gap(m, (1, 1), (2, 1), "rubble", "the stair room's way out, fallen in")
    seal = mid_("doorways", "seal")
    door = ST["arcade"]["ids"][2][4]
    rm = [(x, y) for y in range(38, 44) for x in range(26, 36)
          if m.walkable(x, y) and (x, y) not in {(28, 40), (33, 40), (31, 41), (28, 42), (33, 42), (31, 39)}]
    X.plate_puzzle(m, "Door", [(28, 40), (33, 40), (31, 41)], [(28, 42), (33, 42), (31, 39)],
                   [(FRONT_DOOR[0], FRONT_DOOR[1], door, False, seal, True)], "FLAG_TEMP_4", rm,
                   (34, 37, 32, 42), P, "the workshop's front door is sealed: three drums onto three plates")
    X.remains(m, 6, 5, P, "1", "Bones under a drift of old web. A bronze pin in the dust: a girl's.")
    X.remains(m, 20, 25, P, "2", "Scratched deep: THE BRONZE MEN DROVE IT AT US WITH FIRE.\\pIT DID NOT WANT TO.")
    X.remains(m, 40, 30, P, "3", "An explorer's satchel, rotted through. A map inside, every line crossed out.")
    m.break_runs(starts)
    water = {(x, y) for y in range(H) for x in range(W) if m.at(x, y) == "~"}
    errs, reach = m.build("labyrinth_ring3", starts, views=VIEWS, render=render, extra=water)
    return errs


if __name__ == "__main__":
    import sys
    m, mz, front, back = build()
    met = mz.metrics()
    print({k: met[k] for k in ("nodes", "edges", "loops", "junctions", "dead_ends", "components")},
          f"front way {len(front)} steps, back way {len(back)}, {len(m.glows)} glow-marks, webs {m.webs}")
    if "--plan" in sys.argv:
        print(mz.sketch())
    finish(m, mz, front, back, render="--no-render" not in sys.argv)
