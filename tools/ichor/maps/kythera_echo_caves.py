#!/usr/bin/env python3
"""MAP_KYTHERA_ECHO_CAVES: Echo's sea caves under the spring (32 x 26).

design/phase4/SCRIPT.md Part 2 ("Echo's sea caves") and Part 5 ("Echo's
caves"), drawn with the melos tileset's cave kit (TILES_melos.md). Optional.
The rock stair from the Spring of Kallirhoe comes down into three chambers:

- the Speaking Hall (teach): a high chamber lit by a crack in the roof, a
  sea-fed pool where Kalamis fishes, the Echo in the wall, and a Big Pearl on
  the ledge you reach by walking round the pool's rim;
- the dark gallery (test): a winding passage past a cold brazier at its mouth,
  with a dead end paying a Zinc and another (its far end) for a hidden Heart
  Scale; Kolymbos waits by a lamp where it narrows, so he is seen first;
- the sea mouth (payoff): a beach under a low arch onto the daylit sea, with a
  rock in the water reached only by Surf (TM Hyper Voice, once it's a TM) and
  the way out to Route 23 (once Route 23 exists).

The plan is carved from rock in plan() below; the two open rows under any
rock above become its wall face (wall over base), as in Gen 3's caves.

  /usr/bin/python3 tools/ichor/maps/kythera_echo_caves.py [--no-render]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kythera_maps import A, Map  # noqa: E402

W, H = 32, 26
NAME = "KytheraEchoCaves"
P = "KytheraEchoCaves_EventScript_"


def plan():
    """The cave as rows of '#' rock, '.' open ground, '~' water, 'o' a floor tile
    in the water (the rock at the sea mouth)."""
    g = [["#"] * W for _ in range(H)]

    def carve(x0, y0, x1, y1, ch="."):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                g[y][x] = ch
    # the Speaking Hall, its pool, the walk round the rim to the ledge
    carve(2, 1, 13, 10)
    carve(3, 11, 11, 11)
    carve(4, 12, 9, 12)
    carve(6, 13, 6, 13)
    carve(5, 6, 10, 10, "~")
    # the dark gallery: the passage, the dead end north (the Zinc), the brazier's niche,
    # the neck past the lamp, Kolymbos's corner and the far end (the Heart Scale)
    carve(14, 4, 22, 7)
    carve(19, 1, 20, 3)
    carve(15, 8, 15, 8)
    carve(23, 5, 27, 7)
    carve(28, 3, 29, 7)
    # down to the sea mouth
    carve(27, 8, 28, 11)
    carve(12, 12, 29, 17)
    carve(11, 16, 11, 17)
    carve(10, 18, 29, 22)
    carve(10, 23, 28, 23)
    carve(12, 24, 26, 24)
    carve(14, 18, 23, 18, "~")
    carve(11, 19, 28, 22, "~")
    carve(11, 23, 27, 23, "~")
    carve(13, 24, 25, 24, "~")
    carve(15, 25, 16, 25, "~")
    g[21][23] = "o"
    return ["".join(r) for r in g]


PLAN = plan()
STAIR = (5, 1)                 # the stair up to the spring, in the hall's north wall
CRACK = (11, 0)                # the roof crack over the hall, its light below
KALAMIS = (7, 4)               # fishing at the gap in the pool's rim
PEARL = (6, 13)                # the ledge round the pool's rim
ECHO = (12, 2)                 # the dark crack in the wall that answers
BRAZIER = (15, 8)              # the cold brazier at the dark gallery's mouth
ZINC = (19, 3)                 # the dead end north of the gallery
LAMP = (25, 5)                 # the lamp in the neck's wall, by Kolymbos
KOLYMBOS = (29, 7)             # where the gallery turns down to the sea, facing the neck
HEART_SCALE = (29, 5)          # the gallery's far end (hidden: listed, not placed)
TM_ROCK = (23, 21)             # the rock at the sea mouth, by Surf
MOUTH = (15, 25)               # the low arch onto the sea


def classify():
    grid = [list(r) for r in PLAN]
    assert len(grid) == H and all(len(r) == W for r in grid), "the plan is 32 x 26"
    open_ = {(x, y) for y in range(H) for x in range(W) if grid[y][x] != "#"}
    water = {(x, y) for y in range(H) for x in range(W) if grid[y][x] == "~"}
    islets = {(x, y) for y in range(H) for x in range(W) if grid[y][x] == "o"}
    # wall faces: the two open cells below any rock cell (base, then floor)
    wall, base = set(), set()
    for (x, y) in open_:
        if (x, y - 1) not in open_ and (x, y) not in water:
            wall.add((x, y))
        elif (x, y - 2) not in open_ and (x, y - 1) in wall and (x, y) not in water:
            base.add((x, y))
    return open_, water, islets, wall, base


def compose():
    m = Map(NAME, "melos", W, H, fill=0)
    ceil = m.s("cave")
    ROCK = ceil["ids"][0][0]
    m.border = [ROCK] * 4
    m.header = {"music": "MUS_ICHOR_HOLLOW", "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_UNDERGROUND",
                "show_map_name": True, "allow_cycling": False, "allow_running": True, "allow_escaping": True}
    open_, water, islets, wall, base = classify()

    def is_open(c):
        return c in open_

    # rock: the roof seen from above, edged where it meets the cave
    for y in range(H):
        for x in range(W):
            if (x, y) in open_:
                continue
            n, e, s, w = (is_open((x, y - 1)), is_open((x + 1, y)), is_open((x, y + 1)), is_open((x - 1, y)))
            se, sw = is_open((x + 1, y + 1)), is_open((x - 1, y + 1))
            name = "ceil"
            if s:
                name = "ceil_S_b" if (x * 3 + y) % 4 == 0 else "ceil_S"
            elif e:
                name = "ceil_E"
            elif w:
                name = "ceil_W"
            elif se:
                name = "ceil_in_SE" if (x + 1, y + 1) in wall else "ceil_NW"
            elif sw:
                name = "ceil_in_SW" if (x - 1, y + 1) in wall else "ceil_NE"
            m.piece("cave", name, x, y)
    # wall faces and floor
    for (x, y) in open_:
        if (x, y) in water:
            m.set(x, y, A.SEA, False)
            continue
        left, right = (x - 1, y) not in open_ or (x - 1, y) in water, (x + 1, y) not in open_ or (x + 1, y) in water
        if (x, y) in wall:
            m.piece("cave", "wall_L" if left else ("wall_R" if right else ("wall_b" if (x + y) % 3 == 0 else "wall")), x, y)
        elif (x, y) in base:
            m.piece("cave", "base_L" if left else ("base_R" if right else "base"), x, y)
        else:
            r = (x * 7 + y * 13) % 9
            m.piece("cave", "floor_pebbles" if r == 0 else ("floor_b" if r < 3 else "floor"), x, y)

    # the pool in the Speaking Hall: a rim of stones, open where Kalamis fishes
    for (x, y) in water:
        if y > 12:
            continue
        for (dx, dy, name) in ((0, -1, "pool_S"), (0, 1, "pool_N"), (-1, 0, "pool_E"), (1, 0, "pool_W")):
            c = (x + dx, y + dy)
            if c in open_ and c not in water and c not in wall and c not in base:
                m.piece("cave", name, *c)
    for c in ((KALAMIS[0], KALAMIS[1] + 1), (KALAMIS[0] + 1, KALAMIS[1] + 1)):
        m.set(c[0], c[1], A.SEA, False)          # the gap Kalamis fishes through

    # the sea mouth's beach: a rim along the waterline with gaps to surf from
    for (x, y) in water:
        if y < 13 or (x, y - 1) in water or (x, y - 1) not in open_:
            continue
        c = (x, y - 1)
        if c not in wall and c not in base and (x % 4) != 1:
            m.piece("cave", "pool_S", *c)

    # the stair up, its landing, the roof crack and its light
    m.piece("cave", "stair_up", *STAIR)
    m.piece("cave", "floor", STAIR[0], STAIR[1] + 1)
    m.piece("cave", "crack", *CRACK)
    for (x, y, n) in ((11, 4, "light_L"), (12, 4, "light_R")):
        m.piece("cave", n, x, y)
    m.piece("cave", "brazier_cold", *BRAZIER)
    m.piece("cave", "wall_lamp", *LAMP)
    for (x, y) in islets:
        m.piece("cave", "floor_pebbles", x, y)
    m.piece("cave", "mouth_L", *MOUTH)
    m.piece("cave", "mouth_R", MOUTH[0] + 1, MOUTH[1])
    # the sea mouth's water: tide rocks, a fallen column, a drum awash (surfable)
    m.piece("rocks", "tide_rocks", 13, 21)
    m.piece("rocks", "tide_rock", 27, 20)
    m.piece("rocks", "sunken_column", 19, 22)
    m.piece("rocks", "sunken_drum", 16, 20)
    m.piece("rocks", "tide_rock", 25, 23)
    # pebbles along the beach and the hall's walls
    for (x, y) in ((3, 7), (2, 9), (12, 8), (13, 10), (8, 12), (24, 16), (26, 17), (11, 16), (10, 19), (29, 18),
                   (17, 6), (22, 7), (28, 9), (18, 15), (21, 14)):
        m.piece("cave", "floor_pebbles", x, y)
    return m


def events(m):
    m.warp(STAIR[0], STAIR[1], "MAP_KYTHERA_SPRING_OF_KALLIRHOE", 0)
    m.obj("ICHOR_FISHER", KALAMIS[0], KALAMIS[1], P + "Kalamis", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=1)
    m.obj("ICHOR_DIVER", KOLYMBOS[0], KOLYMBOS[1], P + "Kolymbos", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=4)
    m.item_ball(PEARL[0], PEARL[1], "ITEM_BIG_PEARL", "FLAG_ICHOR_ITEM_ECHO_CAVES_BIG_PEARL")
    m.item_ball(ZINC[0], ZINC[1], "ITEM_ZINC", "FLAG_ICHOR_ITEM_ECHO_CAVES_ZINC")
    m.sign(ECHO[0], ECHO[1], P + "Echo", "BG_EVENT_PLAYER_FACING_NORTH")
    m.sign(BRAZIER[0], BRAZIER[1], P + "Brazier")
    m.sign(16, 17, P + "SeaMouth", "BG_EVENT_PLAYER_FACING_SOUTH")


VIEWS = [(6, 4), (7, 10), (17, 6), (25, 7), (26, 12), (18, 15), (21, 21)]


def main():
    m = compose()
    events(m)
    must = [(PEARL[0], PEARL[1] - 1, "the Big Pearl's ledge"), (ZINC[0], ZINC[1] - 1, "the Zinc's dead end"),
            (HEART_SCALE[0], HEART_SCALE[1], "the gallery's far end (the hidden Heart Scale)"),
            (20, 16, "the sea mouth's beach")]
    errors = m.build("kythera_echo_caves", starts=[(STAIR[0], STAIR[1] + 1)], must_reach=must, views=VIEWS,
                     render="--no-render" not in sys.argv)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
