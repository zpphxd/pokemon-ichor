"""Ring IV, the Masks (design/LABYRINTH.md §6 Ring IV, LABYRINTH_MAZE.md,
design/maps/LabyrinthRing4.md).

Dionysus's verb: masks and roles. The first Titan territory, lit by their oil
lamps: barracks, an armory, a mess hall where the grunts let the passwords
slip, four sentry posts on the way through the maze, and Enkelados's
checkpoint at the stair down. A Titan helmet from the barracks locker lets the
player pass the posts as a recruit. West and south lies the Titans' dig, raw
cave the grunts were tunnelling, where the stream comes out of the rock and
runs to a chute that drops to Ring V's lake.
"""
from __future__ import annotations

from labyrinth_lib import Maze, cell, gap, cave_grid, notch, PITCH
from kythera_maps import DIRS4

NAME = "LabyrinthRing4"
W, H = 50, 42               # 12 x 10 nodes
SEED = 5
P = NAME + "_EventScript_"

ENTRY = (0, 0, 1, 1)
BARRACKS = (3, 2, 5, 3)
ARMORY = (10, 0, 11, 1)
MESS = (6, 5, 9, 6)
CHECK = (9, 8, 11, 9)
STAIR = (44, 33)            # in the checkpoint room's north face
CAVE_NODES = {(x, y) for x in range(0, 4) for y in range(5, 10)} | {(4, 8), (4, 9), (5, 9), (2, 4), (0, 4)}
STREAM_X = (12, 13)         # between node columns 2 and 3, from the spring down to the chute
SPRING_Y = 20


def maze(seed=SEED):
    mz = Maze(12, 10, seed)
    for r in (ENTRY, BARRACKS, ARMORY, MESS, CHECK):
        mz.room(*r)
    keep = [((10, 7), (10, 8)), ((11, 7), (11, 8)), ((9, 7), (9, 8))]   # the checkpoint's north wall
    keep += [((8, 9), (9, 9))]                                          # its one door is (8,8)-(9,8)
    for y in range(5, 10):                                              # the stream splits the dig
        if y != 7:
            keep.append(((2, y), (3, y)))
    mz.link((8, 8), (9, 8))
    mz.carve((1, 1), keep=keep)
    for n in mz.nodes():
        if mz.deg(n) == 0:
            mz.carve(n, keep=keep)
    mz.braid(0.7, keep=keep)
    mz.crossings(12, keep=keep)
    return mz


def grid_of(mz):
    g = cave_grid(mz, W, H, CAVE_NODES, seed=8)
    for y in range(SPRING_Y, H - 1):
        for x in STREAM_X:
            if y in (30, 31):
                g[y][x] = ";"           # the dig's plank ford
            elif g[y][x] in "%#,":
                g[y][x] = "~"
    return g


def build(render=True):
    from labyrinth_lib import LMap, mid, setmetatiles
    from labyrinth_upper import DARK
    mz = maze()
    g = grid_of(mz)
    hdr = dict(DARK)
    hdr.update({"requires_flash": False, "music": "MUS_ICHOR_TITAN"})   # lit by the Titans' lamps
    m = LMap(NAME, W, H, hdr)
    m.g = g
    keep = {(x, y) for x in range(2, 8) for y in range(0, 3)} | {(x, y) for x in range(42, 48) for y in range(32, 35)}
    keep |= {(x, y) for x in range(STREAM_X[0] - 1, STREAM_X[1] + 2) for y in range(H)}
    notch(m.g, keep=keep)
    m.g0 = [row[:] for row in m.g]
    m.lay()
    start = (4, 2)
    m.stairs(4, 1, "up")
    m.anchor(*start, "THREAD_ANCHOR_R4_ENTRANCE")
    m.stairs(*STAIR, "down")
    m.anchor(STAIR[0], STAIR[1] + 1, "THREAD_ANCHOR_R4_CHECKPOINT")

    # --- the rooms' furniture -----------------------------------------------------------------
    bx, by = cell((3, 2))
    for (x, y) in ((bx, by + 1), (bx + 3, by + 1), (bx + 6, by + 1), (bx, by + 4), (bx + 6, by + 4)):
        m.put("bunk", x, y)
    m.put("helmets", bx + 3, by + 4)
    m.put("lamp_stand", bx + 9, by)
    mx, my = cell((6, 5))
    for (x, y) in ((mx + 1, my + 1), (mx + 6, my + 1), (mx + 11, my + 1)):
        m.put("mess_table", x, y)
    m.put("lamp_stand", mx, my)
    m.put("lamp_stand", mx + 15, my)
    ax, ay = cell((10, 0))
    m.put("armory", ax, ay)
    m.put("armory", ax + 4, ay)
    cx, cy = cell((9, 8))
    m.put("lamp_stand", cx + 1, cy + 4)
    m.put("lamp_stand", cx + 9, cy)
    # the sickle banners on the barracks' and the checkpoint's north faces
    m.put("banners", bx + 1, by - 1)
    m.put("banners", cx + 1, cy - 1)
    m.anchor(cx + 4, cy + 5, "THREAD_ANCHOR_UNNAMED")
    m.anchor(bx + 4, by + 2, "THREAD_ANCHOR_R4_BARRACKS")
    m.anchor(6, 22, "THREAD_ANCHOR_R4_DIG")
    m.rooms = dict(barracks=(bx, by), mess=(mx, my), armory=(ax, ay), check=(cx, cy))
    return m, mz


VIEWS = [(6, 4), (20, 10), (44, 6), (6, 24), (30, 22), (44, 22), (8, 36), (24, 36), (44, 36)]


def finish(m, mz, render=True):
    from labyrinth_lib import cell as c_
    bx, by = m.rooms["barracks"]
    mx, my = m.rooms["mess"]
    ax, ay = m.rooms["armory"]
    cx, cy = m.rooms["check"]
    o = m.obj
    # the helmet locker, the barracks' loot
    for i in range(2):
        for j in range(2):
            m.sign(bx + 3 + i, by + 4 + j, P + "HelmetLocker")
    m.item(bx + 8, by + 5, "ITEM_MAX_REVIVE", "FLAG_ICHOR_ITEM_R4_MAX_REVIVE")
    m.hidden(bx + 1, by + 3, "ITEM_ULTRA_BALL", "FLAG_ICHOR_HIDDEN_ITEM_R4_ULTRA_BALL")
    # the mess hall's talkers: the passwords
    o("ICHOR_TITAN_GRUNT", mx + 2, my + 4, P + "Talker1", move="MOVEMENT_TYPE_FACE_UP")
    o("ICHOR_TITAN_GRUNT", mx + 8, my, P + "Talker2", move="MOVEMENT_TYPE_FACE_DOWN")
    o("ICHOR_TITAN_GRUNT", mx + 13, my + 4, P + "Talker3", move="MOVEMENT_TYPE_FACE_UP")
    # the armory: Pelos and the Hyper Potion behind him
    o("ICHOR_TITAN_GRUNT", ax + 2, ay + 4, P + "Pelos", move="MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2,
      local_id="LOCALID_R4_PELOS")
    m.item(ax + 3, ay + 2, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_R4_HYPER_POTION")
    m.objects[-3]["trainer_type"] = "TRAINER_TYPE_ICHOR_TITANBORN"
    # Enkelados at the checkpoint's door
    o("ICHOR_TITAN_GRUNT", cx, cy + 1, P + "Enkelados", move="MOVEMENT_TYPE_FACE_LEFT",
      local_id="LOCALID_R4_ENKELADOS")
    m.trigger(cx - 1, cy, P + "Checkpoint", var="VAR_TEMP_2", value="0")
    m.trigger(cx - 1, cy + 1, P + "Checkpoint", var="VAR_TEMP_2", value="0")
    # the four posts, on the way from the stair to the checkpoint
    d, path = route(m, (4, 2), (cx - 2, cy))
    posts = []
    names = ["Lithos", "Koniortos", "Sideros", "Chalkos"]
    for i in range(len(path) // 6, len(path) - 3):
        if len(posts) == 4:
            break
        x, y = path[i]
        if any(abs(x - a) + abs(y - b) < 9 for (a, b, _) in posts):
            continue
        nx, ny = path[i + 1]
        # stand on the far lane, facing back along the way
        dx, dy = nx - x, ny - y
        side = (dy, dx)
        sx, sy = x + side[0], y + side[1]
        if not m.walkable(sx, sy) or (sx, sy) in path:
            sx, sy = x - side[0], y - side[1]
            if not m.walkable(sx, sy) or (sx, sy) in path:
                continue
        face = {(1, 0): "LEFT", (-1, 0): "RIGHT", (0, 1): "UP", (0, -1): "DOWN"}[(dx, dy)]
        if not m.walkable(sx + dx * 2, sy + dy * 2):
            continue
        posts.append((sx + dx * 2, sy + dy * 2, face))
    for (x, y, face), nm in zip(posts, names):
        e = o("ICHOR_TITAN_GRUNT", x, y, P + nm, move=f"MOVEMENT_TYPE_FACE_{face}", trainer=True, sight=5,
              local_id=f"LOCALID_R4_{nm.upper()}")
        e["trainer_type"] = "TRAINER_TYPE_ICHOR_SENTRY"
    m.posts = posts
    # the fresco of the dance's steps 1-3, in a bay by the mess hall
    m.sign(mx + 7, my - 1, P + "FrescoDance")
    # the dig: the spring, the chute down to Ring V's lake, the Iron, the Nugget
    m.sign(12, 19, P + "Spring")
    for x in (12, 13):
        m.trigger(x, H - 2, P + "Chute")
    m.item(4, 38, "ITEM_IRON", "FLAG_ICHOR_ITEM_R4_IRON")
    m.hidden(8, 26, "ITEM_NUGGET", "FLAG_ICHOR_HIDDEN_ITEM_R4_NUGGET")
    # warps
    m.arrival(4, 2)                                               # 0: down from the workshop
    m.warp(4, 1, "MAP_LABYRINTH_WORKSHOP", 4)                     # 1, 2: the stair up
    m.warp(5, 1, "MAP_LABYRINTH_WORKSHOP", 4)
    m.arrival(6, 22)                                              # 3: Ring III's hole lands in the dig
    m.warp(*STAIR, "MAP_LABYRINTH_RING5", 0)                      # 4, 5: the stair down
    m.warp(STAIR[0] + 1, STAIR[1], "MAP_LABYRINTH_RING5", 0)
    m.arrival(STAIR[0], STAIR[1] + 1)                             # 6: up from Ring V
    m.gen = []
    starts = [(4, 2)]
    m.forced_open = set()
    import labyrinth_extras as X
    from labyrinth_lib import mid as mid_
    grate = mid_("doorways", "grate")
    X.block_gap(m, (1, 1), (1, 2), "rubble", "the stair room's way down, blocked by a Titan cave-in")
    X.block_gap(m, (8, 8), (9, 8), "chain", "bronze chains across the checkpoint's door: the Labrys cuts them")
    rx, ry = min(((x, y) for y in range(28, 40) for x in range(2, 11) if m.at(x, y) == "," and m.walkable(x, y)),
                 key=lambda c: abs(c[0] - 9) + abs(c[1] - 32))
    X.obstacle(m, rx, ry, "roots", why="roots in the dig's side tunnel")
    stairs = [(STAIR[0], STAIR[1], mid_("stairs", "down_l"), False, grate, True),
              (STAIR[0] + 1, STAIR[1], mid_("stairs", "down_r"), False, grate, True)]
    drums, plates = [(40, 36), (43, 36), (46, 37)], [(40, 38), (43, 38), (42, 37)]
    rm = [(x, y) for y in range(34, 40) for x in range(38, 48) if m.walkable(x, y) and (x, y) not in set(drums + plates)]
    X.plate_puzzle(m, "Stair", drums, plates, stairs, "FLAG_TEMP_4", rm, (43, 33, 46, 38), P,
                   "the stair down is grated: three drums, and the third must go in first or wait")
    X.remains(m, 5, 30, P, "1", "A snapped spear, Titan-made, and claw marks on the rock beside it.")
    X.remains(m, 30, 13, P, "2", "Chalked on the barracks wall: DRIVE IT WITH THE TORCHES. IT HATES THE TORCHES.")
    X.remains(m, 20, 37, P, "3", "Bones, a broken shield with an owl on it, and a pack. The owl is Astyra's.")
    m.break_runs(starts)
    water = {(x, y) for y in range(H) for x in range(W) if m.at(x, y) == "~"}
    errs, reach = m.build("labyrinth_ring4", starts, views=VIEWS, render=render, extra=water)
    return errs


def route(m, a, b):
    from collections import deque
    prev = {a: None}
    q = deque([a])
    while q:
        p = q.popleft()
        if p == b:
            break
        for dx, dy in DIRS4:
            n = (p[0] + dx, p[1] + dy)
            if n not in prev and m.walkable(*n):
                prev[n] = p
                q.append(n)
    out, p = [], b
    while p is not None:
        out.append(p)
        p = prev.get(p)
    return len(out), out[::-1]


if __name__ == "__main__":
    import sys
    m, mz = build()
    met = mz.metrics()
    print({k: met[k] for k in ("nodes", "edges", "loops", "junctions", "dead_ends", "components")}, met["dead"])
    if "--plan" in sys.argv:
        print(mz.sketch())
    finish(m, mz, render="--no-render" not in sys.argv)
    print("posts", m.posts)
