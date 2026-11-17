"""Ring I, the Threshold (design/LABYRINTH.md §6 Ring I, LABYRINTH_MAZE.md,
design/maps/LabyrinthRing1.md).

Hestia's verb: carry the flame. The threshold hearth's fire lasts 30 steps on
the torch (26 Spartan, 36 Mortal); the five braziers take only that fire, and a
lit brazier relights it. The relay's spine is laid by hand and the rest of the
ring is a braided maze around it; every seed is measured and kept only if:

- every hop the solution needs fits Spartan's 26 steps;
- B3 (in the fresco hall) is past Hero's 30 from every earlier fire until the
  fresco door, shown only in B1's light, opens the short way from B1;
- B4 (in the old cave) needs B3's fire;
- the short way from B4 to B5 runs through a draught that snuffs the flame,
  and the safe way round still fits;
- the gate brazier G, by the stair down, takes the fire only once B1-B5 burn.
"""
from __future__ import annotations

from collections import deque

from labyrinth_lib import Maze, PITCH, cell
from kythera_maps import DIRS4

NAME = "LabyrinthRing1"
W, H = 42, 34                # 10 x 8 nodes
FLAME, FAR = 26, 30
HALL = (4, 0, 5, 1)          # the threshold hall: the stair up, the hearth
GATE = (6, 6, 7, 7)          # the gate room: G and the stair down
FRESCO = (1, 3, 2, 4)        # the fresco hall: B3

SPINE = [
    [(4, 1), (3, 1), (2, 1), (2, 0)],                 # hall -> B1's alcove
    [(5, 0), (6, 0), (7, 0), (8, 0)],                 # the thread lesson's dead end
    [(5, 1), (6, 1), (7, 1), (7, 2), (8, 2)],         # hall -> the cleft -> B2's alcove
    [(5, 1), (5, 2)],                                 # hall -> south (Akakallis)
    [(1, 2), (2, 2), (2, 3)],                         # behind the fresco door -> the hall of B3
    [(1, 4), (1, 5), (0, 5), (0, 6), (0, 7)],         # out of the fresco hall -> B4's alcove
    [(0, 6), (1, 6), (2, 6), (3, 6), (3, 7)],         # B4 -> B5, the short way (draught on 1,6-2,6)
    [(1, 6), (1, 7), (2, 7), (2, 6)],                 # ...and the safe way round
    [(3, 6), (4, 6), (5, 6), (6, 6)],                 # B5 -> the gate room
    [(0, 1), (0, 0)],                                 # Xenodike's corner, the TM
]
DOOR = ((2, 1), (2, 2))      # the fresco door (opens when B1 is lit)
DRAUGHT = ((1, 6), (2, 6))
CLOSED = [  # walls the random maze must never open
    ((2, 2), (3, 2)), ((2, 2), (2, 1)), ((1, 2), (0, 2)), ((1, 2), (1, 1)), ((1, 2), (1, 3)),
    ((2, 0), (1, 0)), ((2, 0), (3, 0)), ((6, 0), (6, 1)), ((7, 0), (7, 1)), ((8, 0), (8, 1)),
    ((8, 0), (9, 0)), ((8, 2), (9, 2)), ((8, 2), (8, 1)), ((8, 2), (8, 3)),
    ((0, 3), (1, 3)), ((0, 4), (1, 4)), ((2, 3), (3, 3)), ((2, 4), (3, 4)), ((2, 4), (2, 5)),
    ((0, 7), (1, 7)), ((3, 7), (4, 7)), ((3, 7), (2, 7)), ((0, 0), (1, 0)),
    ((2, 7), (3, 7)), ((5, 6), (5, 7)), ((5, 6), (5, 5)), ((4, 6), (4, 5)), ((4, 6), (4, 7)),
    ((3, 6), (3, 5)), ((2, 6), (2, 5)), ((0, 5), (0, 4)), ((1, 5), (2, 5)), ((0, 6), (0, 5)),
]
ALCOVES = {"B1": (2, 0), "B2": (8, 2), "B4": (0, 7), "B5": (3, 7)}


def cave(x, y):
    """The karst cleft along the east side, and the old cave pocket to the
    south-west the house's builders broke into."""
    return (x >= 30 and y < 22) or (x < 10 and y >= 22)


def maze(seed, braid=0.8):
    mz = Maze(10, 8, seed)
    for r in (HALL, GATE, FRESCO):
        mz.room(*r)
    for path in SPINE:
        for a, b in zip(path, path[1:]):
            mz.link(a, b)
    seen = set()
    for e in mz.edges:
        seen |= set(e)
    keep = CLOSED + [DOOR, ((1, 7), (0, 7))]
    # grow the rest of the ring out of the spine's west, south and east
    mz.carve((5, 2), keep=keep)
    for n in mz.nodes():
        if n not in seen and mz.deg(n) == 0:
            mz.carve(n, keep=keep)
    protect = set(ALCOVES.values()) | {(8, 0), (1, 2), (0, 0)}
    mz.braid(braid, keep_dead=protect, keep=keep)
    mz.crossings(6, keep=keep, avoid=protect | set(sum(SPINE[4:8], [])))
    return mz


CAVE_NODES = {(7, 0), (8, 0), (9, 0), (7, 1), (8, 1), (9, 1), (7, 2), (8, 2), (9, 2), (8, 3), (9, 3),
              (9, 4), (8, 4), (0, 5), (0, 6), (0, 7), (1, 6), (1, 7), (2, 7), (1, 5)}


def grid_of(mz, seed=3):
    from labyrinth_lib import cave_grid
    return cave_grid(mz, W, H, CAVE_NODES, seed=seed)


def gap(a, b):
    (ax, ay), (bx, by) = sorted((a, b))
    if ay == by:
        return [(PITCH * ax + 4 + i, PITCH * ay + 2 + j) for i in range(2) for j in range(2)]
    return [(PITCH * ax + 2 + i, PITCH * ay + 4 + j) for i in range(2) for j in range(2)]


def walk(g, start, blocked=(), opened=()):
    blocked, opened = set(blocked), set(opened)
    d = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in DIRS4:
            n = (x + dx, y + dy)
            if n in d or n in blocked or not (0 <= n[0] < W and 0 <= n[1] < H):
                continue
            if g[n[1]][n[0]] in "#%" and n not in opened:
                continue
            d[n] = d[(x, y)] + 1
            q.append(n)
    return d


def alcove_stand(n):
    """The alcove's brazier fills node n; the player stands in the cell of the
    passage just outside it (the one the spine enters from)."""
    for path in SPINE:
        for a, b in zip(path, path[1:]):
            if b == n:
                (ax, ay), (bx, by) = a, b
                g = gap(a, b)
                # the gap cell nearest the alcove, left column/top row
                if bx > ax:
                    return (PITCH * ax + 5, PITCH * ay + 2)
                if bx < ax:
                    return (PITCH * bx + 4, PITCH * by + 2)
                if by > ay:
                    return (PITCH * ax + 2, PITCH * ay + 5)
                return (PITCH * bx + 2, PITCH * by + 4)
    raise KeyError(n)


# the hearth and the in-room braziers (top-left cells, 2x2), and where you stand
HEARTH = (19, 4)
B3_AT = (6, 14)              # in the fresco hall's north-west corner
G_AT = (30, 27)              # in the gate room, by the stair


def stands():
    s = {k: alcove_stand(v) for k, v in ALCOVES.items()}
    s["H"] = (HEARTH[0], HEARTH[1] + 2)
    s["B3"] = (B3_AT[0], B3_AT[1] + 2)
    s["G"] = (G_AT[0] - 1, G_AT[1] + 1)
    return s


def solids():
    """Cells the braziers and the hearth fill."""
    out = set()
    for n in ALCOVES.values():
        out |= {cell(n, i, j) for i in range(2) for j in range(2)}
    for (x, y) in (HEARTH, B3_AT, G_AT):
        out |= {(x + i, y + j) for i in range(2) for j in range(2)}
    return out


def measure(g):
    """The relay's hops, and whether the puzzle holds."""
    s, sol = stands(), solids()
    dr = set(gap(*DRAUGHT))
    door = set(gap(*DOOR))
    D = {k: walk(g, v, sol) for k, v in s.items()}
    Dd = {k: walk(g, v, sol, door) for k, v in s.items()}
    Ds = {k: walk(g, v, sol | dr) for k, v in s.items()}

    def d(a, b, t=D):
        return t[a].get(s[b], 999)
    hops = {
        "H-B1": d("H", "B1"), "H/B1-B2": min(d("H", "B2"), d("B1", "B2")),
        "B3 without the door": min(d(k, "B3") for k in ("H", "B1", "B2")),
        "B1-B3 through the door": d("B1", "B3", Dd),
        "B3-B4": d("B3", "B4"), "B4 from H/B1/B2 (door open)": min(d(k, "B4", Dd) for k in ("H", "B1", "B2")),
        "B4-B5 short (draught)": d("B4", "B5"), "B4-B5 safe": d("B4", "B5", Ds),
        "B5 from earlier fires (safe, door open)": min(walk(g, s[k], sol | dr, door).get(s["B5"], 999)
                                                       for k in ("H", "B1", "B2", "B3")),
        "B5-G": d("B5", "G"),
    }
    ok = (hops["H-B1"] <= FLAME and hops["H/B1-B2"] <= FLAME and hops["B3 without the door"] > FAR
          and hops["B1-B3 through the door"] <= FLAME and hops["B3-B4"] <= FLAME
          and hops["B4 from H/B1/B2 (door open)"] > FLAME
          and hops["B4-B5 short (draught)"] < hops["B4-B5 safe"] <= FLAME
          and hops["B5 from earlier fires (safe, door open)"] > FLAME and hops["B5-G"] <= FLAME)
    return ok, hops


SEED = 99
P = NAME + "_EventScript_"
LOCALS = {}


def decorate_cave(m, keep_free, rng, every=3):
    """Stalagmites and boulders in the cave's nodes where they leave the way
    open: each is kept only if nothing it stands beside is cut off."""
    import random
    r = random.Random(rng)
    base = m.reach_all()
    picks = ["stalagmite", "stalagmites", "boulder", "rock_pile", "stalagmite"]
    placed = 0
    cells = [(x, y) for y in range(m.h) for x in range(m.w) if m.at(x, y) == "," and (x, y) not in keep_free]
    r.shuffle(cells)
    for (x, y) in cells:
        if placed >= len(cells) // (every * 4):
            break
        # never in a 1-wide spot: both cells across the corridor must be floor
        if not ((m.at(x - 1, y) in ",;" and m.at(x + 1, y) in ",;") or (m.at(x, y - 1) in ",;" and m.at(x, y + 1) in ",;")):
            if sum(m.at(x + dx, y + dy) in ",;" for dx, dy in DIRS4) < 2:
                continue
        m.g[y][x] = "%"
        if m.reach_all(start=next(iter(base))) != base - {(x, y)}:
            m.g[y][x] = ","
            continue
        m.g[y][x] = ","
        m.deco.append((x, y, picks[placed % len(picks)]))
        base = base - {(x, y)}
        placed += 1


def build(render=True):
    from labyrinth_lib import LMap, mid, ST
    from labyrinth_upper import DARK
    mz = maze(SEED)
    g = grid_of(mz)
    ok, hops = measure(g)
    assert ok, hops
    m = LMap(NAME, W, H, dict(DARK))
    m.g = [row[:] for row in g]
    # a little gravel where the cave floor runs wide
    for y in range(H):
        for x in range(W):
            if m.g[y][x] == "," and (x * 7 + y * 3) % 11 == 0:
                m.g[y][x] = ";"
    m.lay()

    # --- the fixed pieces --------------------------------------------------------------
    hall_stand = (21, 2)
    m.stairs(21, 1, "up")
    m.anchor(*hall_stand, "THREAD_ANCHOR_R1_THRESHOLD")
    m.put("hearth", *HEARTH)
    for (x, y) in [(HEARTH[0] + i, HEARTH[1] + j) for i in range(2) for j in range(2)]:
        m.solid[y, x] = True
    braz = {k: cell(v) for k, v in ALCOVES.items()}
    braz["B3"], braz["G"] = B3_AT, G_AT
    for k, (x, y) in braz.items():
        m.put("brazier", x, y, cells={(0, 0), (1, 0), (0, 1), (1, 1)})
    m.stairs(30, 25, "down")
    m.anchor(30, 26, "THREAD_ANCHOR_R1_GATE")
    m.anchor(8, 16, "THREAD_ANCHOR_R1_FRESCO")       # A1, by B3
    m.anchor(38, 6, "THREAD_ANCHOR_R1_CLEFT")        # where the climb from Ring II comes up
    m.anchor(2, 19, "THREAD_ANCHOR_UNNAMED")         # the hidden anchor, behind B3's hall
    # Akakallis's lamp narrows the hall's south door to one lane
    m.put("lamp_stand", 23, 8)
    # the hole down to Ring II, in the cleft's far dead end
    m.named("hole", "hole", 38, 3, False) if "hole" in ST["hole"]["names"] else m.put("hole", 38, 3)
    m.stops.add((38, 3))
    # niches and a shrine in the masonry faces; fresco signs
    m.named("niche", "shrine", 7, 1)
    m.named("niche", "back", 19, 29)
    m.named("niche", "lamp_out", 6, 21)

    # --- events --------------------------------------------------------------------------
    m.arrival(*hall_stand)                                         # 0: from the Grand Staircase
    from labyrinth_lib import dest
    up, upw = dest("MAP_KNOSSA_PALACE_GRAND_STAIRCASE", ("MAP_LABYRINTH_RING1", 0))
    upw = 0 if upw is None else upw       # the Grand Staircase's warp 0 lands by its stair down
    m.warp(21, 1, up, upw)                                         # 1, 2: the stair up
    m.warp(22, 1, up, upw)
    m.arrival(30, 26)                                              # 3: up from Ring II
    m.warp(30, 25, "MAP_LABYRINTH_RING2", 0)                       # 4, 5: the stair down
    m.warp(31, 25, "MAP_LABYRINTH_RING2", 0)
    m.arrival(38, 6)                                               # 6: the climb up from Ring II

    hearth_cells = [(HEARTH[0] + i, HEARTH[1] + j) for i in range(2) for j in range(2)]
    for (x, y) in hearth_cells:
        m.sign(x, y, P + "Hearth")
    def faced(x, y):
        return any(m.walkable(x + dx, y + dy) for dx, dy in DIRS4)
    for k, (x, y) in braz.items():
        for i in range(2):
            for j in range(2):
                if faced(x + i, y + j):
                    m.sign(x + i, y + j, P + "Brazier" + k)
    for (x, y) in gap(*DRAUGHT):
        m.trigger(x, y, P + "Draught")
    m.sign(7, 1, P + "Shrine")
    m.sign(19, 29, P + "FrescoBulls")
    m.trigger(38, 3, P + "Hole")
    m.trigger(8, 16, P + "TieLesson", var="VAR_TEMP_1", value="0")

    m.obj("ICHOR_PRIESTESS", 22, 11, P + "Akakallis", move="MOVEMENT_TYPE_FACE_UP", trainer=True,
          sight=3, local_id="LOCALID_R1_AKAKALLIS")
    m.obj("ICHOR_PRIESTESS", 2, 3, P + "Xenodike", move="MOVEMENT_TYPE_FACE_UP", trainer=True,
          sight=1, local_id="LOCALID_R1_XENODIKE")
    m.item(35, 2, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_R1_HYPER_POTION")
    m.item(2, 2, "ITEM_TM_ROCK_TOMB", "FLAG_ICHOR_ITEM_R1_TM_ROCK_SLIDE")
    m.item(3, 18, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_R1_HYPER_POTION_2")
    m.item(11, 22, "ITEM_ETHER", "FLAG_ICHOR_ITEM_R1_ETHER")
    m.hidden(7, 2, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_ITEM_R1_BRONZE_OBOL")
    m.hidden(19, 31, "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_ITEM_R1_REVIVE")

    # --- the generated state: lit braziers, the fresco door, the gate ----------------------
    lit = {}
    for k, (x, y) in braz.items():
        lit[k] = [(x + i, y + j, int(m.mid[y + j, x + i]) + 2) for i in range(2) for j in range(2)]
    flag = {k: f"FLAG_ICHOR_BRAZIERS_START + 0x{0x30 + i:02X}" for i, k in enumerate(["B1", "B2", "B3", "B4", "B5", "G"])}
    door_state = door_tiles(m, g)
    gen = []
    for k in lit:
        gen.append(f"if (flag({flag[k]})) {{")
        gen += [f"    setmetatile({x}, {y}, 0x{t:03X}, TRUE)" for (x, y, t) in lit[k]]
        if k == "B1":
            gen += [f"    setmetatile({x}, {y}, 0x{t:03X}, {str(s).upper()})" for (x, y, t, s) in door_state]
        gen.append("}")
    grate = mid("doorways", "grate")
    gen += ["if (!flag(FLAG_ICHOR_RING1_GATE)) {",
            f"    setmetatile(30, 25, 0x{grate:03X}, TRUE)", f"    setmetatile(31, 25, 0x{grate:03X}, TRUE)", "} else {",
            f"    setmetatile(30, 25, 0x{mid('stairs', 'down_l'):03X}, FALSE)",
            f"    setmetatile(31, 25, 0x{mid('stairs', 'down_r'):03X}, FALSE)", "}"]
    m.gen = gen
    m.extra_scripts = brazier_scripts(flag)

    starts = [hall_stand]
    m.forced_open = set(gap(*DOOR))
    m.stops |= set(gap(*DOOR))
    m.break_runs(starts)
    errs, reach = m.build("labyrinth_ring1", starts, views=VIEWS, render=render,
                          extra=set(gap(*DOOR)))
    return m, mz, hops


def brazier_scripts(flag):
    """The six braziers' scripts: each takes only the hearth's fire, and a lit
    one hands it back (the relay)."""
    out = []
    for k in ["B1", "B2", "B3", "B4", "B5", "G"]:
        f = flag[k]
        s = [f"", f"script {P}Brazier{k} {{", "    lockall",
             f"    if (flag({f})) {{", f"        call({P}Relight)", "        releaseall", "        end", "    }",
             "    specialvar(VAR_RESULT, Ichor_GetFlameKind)",
             "    if (var(VAR_RESULT) != FLAME_THRESHOLD) {",
             '        msgbox(format("A cold bronze brazier. The torch\'s own flame just slides off the ash.\\p'
             'It wants the threshold fire."), MSGBOX_DEFAULT)',
             "        releaseall", "        end", "    }"]
        if k == "G":
            cond = " || ".join(f"!flag({flag[b]})" for b in ["B1", "B2", "B3", "B4", "B5"])
            s += [f"    if ({cond}) {{",
                  '        msgbox(format("The gate brazier won\'t take the fire.\\pIts five sisters are '
                  'still dark."), MSGBOX_DEFAULT)', "        releaseall", "        end", "    }"]
        s += [f"    setvar(VAR_0x8004, {f})", "    setvar(VAR_0x8005, FALSE)",
              "    call(EventScript_IchorBrazier)", "    if (var(VAR_RESULT) == TRUE) {"]
        if k == "G":
            s += ["        setflag(FLAG_ICHOR_RING1_GATE)"]
        s += [f"        call({P}DrawState)", "        special(DrawWholeMapView)"]
        if k == "B1":
            s += ['        msgbox(format("In the new light, a seam shows in the wall to the south.\\p'
                  'A painted door. It swings in at a touch."), MSGBOX_DEFAULT)']
        if k == "G":
            s += ["        setflag(FLAG_ICHOR_RING1_GATE)",
                  "        if (var(VAR_ICHOR_KNOSSA) < 6) {", "            setvar(VAR_ICHOR_KNOSSA, 6)", "        }",
                  "        playse(SE_DOOR)",
                  '        msgbox(format("Under the gate brazier, the grate grinds up into the stone.\\p'
                  'The stair down is open."), MSGBOX_DEFAULT)']
        s += [f"        call({P}Relight)", "    }", "    releaseall", "    end", "}"]
        out += s
    return out


def door_tiles(m, g):
    """The fresco door's cells and their neighbours as they are once it opens:
    (x, y, metatile, solid) for every cell that changes."""
    from labyrinth_lib import LMap
    from labyrinth_upper import DARK
    g2 = [row[:] for row in g]
    for (x, y) in gap(*DOOR):
        g2[y][x] = "."
    m2 = LMap(NAME, W, H, dict(DARK))
    m2.g = g2
    m2.lay()
    out = []
    xs = [c[0] for c in gap(*DOOR)]
    ys = [c[1] for c in gap(*DOOR)]
    for y in range(min(ys) - 2, max(ys) + 3):
        for x in range(min(xs) - 2, max(xs) + 3):
            if int(m2.mid[y, x]) != int(m.mid[y, x]) or bool(m2.solid[y, x]) != bool(m.solid[y, x]):
                out.append((x, y, int(m2.mid[y, x]), bool(m2.solid[y, x])))
    return out


VIEWS = [(21, 5), (8, 6), (35, 6), (8, 16), (22, 17), (35, 15), (5, 27), (20, 27), (31, 28)]


if __name__ == "__main__" and "--search" not in __import__("sys").argv:
    import sys
    build(render="--no-render" not in sys.argv)

if __name__ == "__main__" and "--search" in __import__("sys").argv:
    import sys
    lo = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 0
    for seed in range(lo, lo + 300):
        mz = maze(seed)
        met = mz.metrics()
        g = grid_of(mz)
        ok, hops = measure(g)
        if ok and met["loops"] >= 8 and met["components"] == 1 and met["dead_ends"] <= 9 and met["junctions"] >= 27:
            print("seed", seed, {k: met[k] for k in ("loops", "junctions", "dead_ends")})
            print(hops)
            print(mz.sketch())
            break
    else:
        print("none; last", hops)
