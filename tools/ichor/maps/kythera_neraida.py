#!/usr/bin/env python3
"""MAP_KYTHERA_NERAIDA_FALLS: the green ravine north of Paphia (30 x 44).

design/phase4/SCRIPT.md Part 2 ("The Neraida falls"), Part 5 ("The Silent
Falls") and beat III-1H. South to north: the calm stretch past Paphia's orchard
and the sign, forced grass band 1 in the riverbank meadow (walled by the river
and a myrtle hedge), Lykidas on his rock with the goats, Myles's mill (the one
still turning: the rest point), the berry terraces up the west bank (Lum and
Sitrus trees, optional grass, Kerinthos and his hives, a Max Repel on the top
terrace), an idle mill, the ford's stepping stones and Mopsos on the far bank
(band 2 straight behind him), the silent double-width falls over the plunge
pool and the Naiads' shrine (Krenaia, the horn on the altar), and, up the fall
with the Horn, the upper pool: page VII in its crevice, the Minoan vault door,
a Protein on a rock in the pool, Thestylis cutting reeds, and the ledge path
down the east side, one way, back to the river.

The river is turquoise shallows between pink kerbs (impassable); the pools'
surfable cells are the falls' foot and the kerb kit's lilies. Seams (MAP_DESIGN
§5): the 6 rows at the south edge (Paphia, gTileset_Paphia) are aethos only.

  /usr/bin/python3 tools/ichor/maps/kythera_neraida.py [--no-render]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kythera_maps import A, Map  # noqa: E402

W, H = 30, 44
NAME = "KytheraNeraidaFalls"
P = "KytheraNeraidaFalls_EventScript_"

SOUTH_ROAD = (14, 15)          # the road to Paphia at the south edge (Paphia's x 30-31)
PAPHIA_ROAD_X = 30
FALL = (14, 15)                # the double-width falls' columns
MILL_DOOR = (12, 28)
IDLE_WHEEL = (14, 19)          # the idle mill's wheel, top-left (turns once the Horn is given)
ALTAR = (22, 11)
FORD_Y = 25


def cells(*rects):
    out = set()
    for x0, y0, x1, y1 in rects:
        out |= {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    return out


def shallow(m, x, y):
    """River and pool water the player can't wade or surf: turquoise shallows, blocked."""
    m.set(x, y, A.SHALLOW, True)


def trees(m, olives=(), cypresses=(), planes=(), oleanders=(), myrtles=()):
    for x, y in olives:
        m.olive(x, y)
    for x, y in planes:
        m.put("plane", x, y)
    for x, y in cypresses:
        m.cypress(x, y)
    for x, y in oleanders:
        m.piece("flowers", "oleander", x, y)
    for x, y in myrtles:
        m.piece("myrtle", "bush" if (x + y) % 2 else "single", x, y)


def hedgerow(m, x, y0, y1):
    """A solid north-south line of mixed shrubs and cypresses, never one plant in a row."""
    y = y0
    while y <= y1:
        k = (x * 7 + y * 13) % 6
        if k == 0 and y + 1 <= y1:
            m.cypress(x, y)
            y += 2
            continue
        name = ("myrtle", "single") if k in (1, 4) else ("myrtle", "bush") if k == 2 else \
            ("flowers", "oleander") if k == 3 else ("myrtle", "V")
        m.piece(name[0], name[1], x, y)
        y += 1


def compose():
    m = Map(NAME, "neraida", W, H, fill=A.GRASS)
    face = m.s("cliff")["ids"][1][1]
    m.border = [face] * 4                         # the ravine's rock beyond the edges
    m.header = {"music": "MUS_ICHOR_HOLLOW", "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_ROUTE",
                "show_map_name": True, "allow_cycling": False, "allow_running": True}

    # ==== the north cliff and the Minoan vault door ===========================================
    for x in range(W):
        for y in (0, 1):
            m.piece("cliff", "face", x, y)
        m.piece("cliff", "foot_grass", x, 2)
    m.part("vault", "vault_TL", 20, 0, 2, 2)
    m.set(21, 1, int(m.mid[1, 21]), True)         # the sealed door: solid until the Labrys

    # ==== the shelf and the upper pool (rows 2..6) ============================================
    for x in range(10, 20):
        m.piece("kerb", "NW" if x == 10 else ("NE" if x == 19 else "S"), x, 2)
        m.piece("kerb", "SW" if x == 10 else ("SE" if x == 19 else "N"), x, 6)
    for y in range(3, 6):
        m.piece("kerb", "E", 10, y)
        m.piece("kerb", "W", 19, y)
        for x in range(11, 19):
            shallow(m, x, y)
    # a channel of lilies across the pool from the fall's lip to the stones at either bank
    for x, y in ((14, 5), (15, 5), (13, 5), (11, 4), (12, 4), (13, 4), (14, 4), (15, 4), (16, 4), (17, 4),
                 (18, 4)):
        m.piece("kerb", "lily", x, y)
    for x, y in ((11, 3), (17, 5), (18, 3), (16, 3)):
        m.piece("kerb", "reeds", x, y)
    m.piece("kerb", "stones", 12, 3)              # the Protein's rock
    m.piece("kerb", "stones_b", 10, 4)            # stepping out, west and east
    m.piece("kerb", "stones", 19, 4)
    m.piece("falls", "lip_L", FALL[0], 6)
    m.piece("falls", "lip_R", FALL[1], 6)
    trees(m, cypresses=[(2, 3), (5, 2), (24, 2), (27, 3)], planes=[(0, 3)], olives=[(28, 2)],
          oleanders=[(7, 5), (21, 5)], myrtles=[(4, 5), (22, 4)])
    for x, y in ((7, 3), (8, 6), (20, 3), (23, 6)):
        m.piece("flowers", "narcissus" if x % 2 else "petals", x, y)

    # ==== the cliff under the shelf, the falls and the plunge pool ===========================
    for x in range(6, 23):
        if x in FALL:
            continue
        e = "_L" if x == 6 else ("_R" if x == 22 else "")
        m.piece("cliff", "lip" + e, x, 7)
        for y in (8, 9, 10):
            m.piece("cliff", "face" + e, x, y)
    # the wood closes the shelf's ends instead of more rock
    for x, y in ((1, 7), (3, 7), (1, 9), (3, 9)):
        m.olive(x, y)
    for y in (7, 9):
        m.cypress(5, y)
        m.cypress(23, y)
    hedgerow(m, 24, 7, 10)
    for y in range(7, 11):
        for x in FALL:
            m.set(x, y, A.FALL, False)
    for y in (8, 9, 10):
        m.piece("falls", "face_fall_L", FALL[0] - 1, y)
        m.piece("falls", "face_fall_R", FALL[1] + 1, y)
    # the plunge pool, rows 11..15
    for y in range(11, 15):
        m.piece("kerb", "E", 10, y)
        for x in range(11, 20):
            shallow(m, x, y)
    m.piece("falls", "foot_face_L", FALL[0] - 1, 11)
    m.piece("falls", "foot_L", FALL[0], 11)
    m.piece("falls", "foot_R", FALL[1], 11)
    for x in (16, 17, 18, 19, 20):                # a rocky landing from the shrine to the fall's foot
        m.piece("kerb", "stones" if x % 2 else "stones_b", x, 11)
    for y in (12, 13, 14):
        m.piece("kerb", "W", 20, y)
    for x, y in ((12, 13), (18, 13), (13, 14)):
        m.piece("kerb", "lily" if x % 2 else "reeds", x, y)
    for x in range(10, 21):
        if x in (14, 15, 16, 17, 18):
            continue
        m.piece("kerb", "SW" if x == 10 else ("SE" if x == 20 else "N"), x, 15)
    m.piece("bridge_weir", "weir_W", 14, 15)
    for x in (15, 16, 17):
        m.piece("bridge_weir", "weir", x, 15)
    m.piece("bridge_weir", "weir_E", 18, 15)

    # the Naiads' shrine, east of the pool
    m.piece("naiad_altar", "horn", ALTAR[0], ALTAR[1])
    trees(m, oleanders=[(21, 14)])
    for x, y in ((22, 12), (23, 13), (22, 14)):
        m.piece("flowers", "narcissus" if (x + y) % 2 else "petals", x, y)

    # ==== the river, rows 16..34, then east along rows 35..36 ===================================
    for y in range(16, 35):
        m.piece("kerb", "E", 14, y)
        m.piece("kerb", "W", 18, y)
        for x in (15, 16, 17):
            shallow(m, x, y)
    for y in (35, 36):
        for x in range(15, W):
            shallow(m, x, y)
    m.piece("kerb", "E", 14, 35)
    m.piece("kerb", "E", 14, 36)
    m.piece("kerb", "SW", 14, 37)
    for x in range(15, W):
        m.piece("kerb", "N", x, 37)
    m.piece("kerb", "in_NE", 18, 34)
    for x in range(19, W):
        m.piece("kerb", "S", x, 34)
    for x, y in ((16, 21), (15, 30), (17, 17), (24, 35), (27, 36)):
        m.piece("kerb", "reeds" if (x + y) % 2 else "lily", x, y)
    # a low broken weir
    m.piece("bridge_weir", "weir_low_W", 14, 31)
    for x in (15, 16, 17):
        m.piece("bridge_weir", "weir_low", x, 31)
    m.piece("bridge_weir", "weir_low_E", 18, 31)
    # the ford
    for x in range(14, 19):
        m.piece("kerb", "stones" if x % 2 else "stones_b", x, FORD_Y)
    # the plank bridge over the bend
    for x in (21, 22):
        m.piece("bridge_weir", "bridge_N", x, 34)
        m.piece("bridge_weir", "bridge_V", x, 35)
        m.piece("bridge_weir", "bridge_V", x, 36)
        m.piece("bridge_weir", "bridge_S", x, 37)

    # ==== the mills ============================================================================
    house = [(i, j) for i in range(3) for j in range(3)]
    m.put("mill", 11, 26, cells=house + [(3, 1), (4, 1), (3, 2), (4, 2)])     # Myles's, turning
    m.put("mill", 11, 18, cells=house)                                       # an idle one
    m.part("mill", "wheel_still", IDLE_WHEEL[0], IDLE_WHEEL[1], 2, 2)
    m.set(12, 20, m.s("mill")["ids"][1][0], True)                            # its door, shut and empty

    # ==== the east bank: band 2, Mopsos's narrow, the landing ===================================
    m.blob("seagrass", ["####",
                        "####",
                        "####",
                        "####"], 19, 15, edge_in=False)
    for y in range(15, 19):
        m.piece("myrtle", "V", 23, y)
    for y in range(20, 25):                       # Mopsos's narrow: one tile wide, x 20
        for x in (19, 21):
            trees(m, oleanders=[(x, y)] if (x + y) % 2 else [], myrtles=[(x, y)] if not (x + y) % 2 else [])
    trees(m, olives=[(22, 20), (22, 22)], myrtles=[(22, 24), (23, 24), (23, 25), (20, 33)],
          oleanders=[(19, 29), (23, 32)], planes=[(20, 26)])

    # ==== the ledge path down the east side, one way =========================================
    hedgerow(m, 24, 11, 30)
    hedgerow(m, 27, 3, 33)
    for y in range(3, 33, 2):
        m.olive(28, y)
    for y in range(7, 11):
        for x in (25, 26):
            m.set(x, y, A.GRASS, False)
    for y in (9, 15, 21, 27):
        for x in (25, 26):
            m.set(x, y, A.LEDGE["S"], False)
    for x, y in ((25, 12), (26, 18), (25, 24), (26, 30)):
        m.piece("flowers", "thrift", x, y)

    # ==== the west bank: terraces, berry trees, the main path ===================================
    for y in range(11, 36, 2):                    # the west wood: olives two deep, with a plane
        m.olive(0, y)
    trees(m, planes=[(0, 21)], cypresses=[(2, 11), (2, 13)])
    # terrace walls with steps; the lowest is a ledge back down toward Paphia
    for x in range(2, 9):
        n = "L" if x == 2 else ("R" if x == 8 else "M")
        for y, step in ((20, 7), (25, 4)):
            if x == step:
                m.piece("terrace", "top_steps", x, y - 1)
                m.piece("terrace", "steps", x, y)
            else:
                m.piece("terrace", "top" if n == "M" else "top_" + n, x, y - 1)
                m.piece("terrace", n, x, y)
        m.set(x, 30, A.LEDGE["S"], False)
    m.blob("seagrass", [".#####.",
                        "#######",
                        "######.",
                        ".####.."], 2, 15, edge_in=False)
    m.blob("seagrass", ["..####",
                        ".#####",
                        "######"], 2, 21, edge_in=False)
    m.blob("seagrass", ["#######",
                        "#######",
                        "#######"], 7, 32)
    for y in (32, 33, 34):
        m.piece("myrtle", "V", 6, y)
    m.piece("myrtle", "B", 6, 35)
    m.path(cells((9, 21, 10, 31), (11, 22, 13, 24), (13, 25, 13, 25), (11, 29, 13, 29), (9, 31, 13, 31),
                 (12, 36, 13, 37), (SOUTH_ROAD[0], 37, SOUTH_ROAD[1], H - 1)))
    for x, y in ((3, 27), (7, 28), (8, 29)):
        m.piece("flowers", "oleander" if x % 2 else "petals", x, y)
    m.piece("flowers", "briar", 2, 28)
    for x, y in ((2, 32), (4, 32), (2, 34), (4, 34), (2, 36), (4, 36)):   # the wood west of band 1
        m.olive(x, y)

    # ==== the south strip, rows 38..43: aethos only ===========================================
    m.rect(0, 38, W - 1, H - 1, A.GRASS, False)
    trees_south = [(0, 38), (3, 40), (6, 38), (9, 41), (18, 41), (24, 39), (27, 41), (20, 42)]
    for x, y in trees_south:
        m.olive(x, y)
    for x, y in ((12, 39), (17, 38), (26, 38), (2, 42)):
        m.cypress(x, y)
    m.path(cells((SOUTH_ROAD[0], 37, SOUTH_ROAD[1], H - 1), (12, 38, 13, 38), (16, 38, 22, 39)))
    m.set(13, 40, A.STELE, True)                  # THE NERAIDA FALLS
    for x, y in ((11, 42), (16, 41), (23, 41)):
        m.set(x, y, A.ANEMONE, False)
    return m


def events(m):
    m.warp(MILL_DOOR[0], MILL_DOOR[1], "MAP_KYTHERA_NERAIDA_FALLS_MILL", 0)

    m.sign(13, 40, P + "Sign")
    m.sign(20, 13, P + "SilentFalls")
    m.sign(ALTAR[0], ALTAR[1], P + "Altar")

    m.sign(8, 1, P + "PageSeven")
    m.sign(21, 1, P + "VaultDoor")
    m.sign(12, 20, P + "IdleMill")

    m.obj("ICHOR_PRIESTESS", 21, 12, P + "Krenaia", "MOVEMENT_TYPE_FACE_LEFT", local_id="LOCALID_NERAIDA_KRENAIA")
    m.obj("ICHOR_GOATHERD", 11, 30, P + "Lykidas", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=1)
    m.obj("SPECIES(SKIDDO)", 8, 30 - 1, P + "Goat", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1)
    m.obj("SPECIES(SKIDDO)", 13, 33, P + "Goat", "MOVEMENT_TYPE_FACE_LEFT")
    m.obj("ICHOR_MAN", 7, 22, P + "Kerinthos", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=2)
    m.obj("ICHOR_AUGUR", 20, 19, P + "Mopsos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=5)
    m.obj("ICHOR_HARVESTER", 8, 5, P + "Thestylis", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=1)
    m.obj("ICHOR_KID_M", 22, 36, P + "Boy", "MOVEMENT_TYPE_FACE_LEFT")
    m.berry_tree(4, 28, "BERRY_TREE_ICHOR_NERAIDA_LUM")
    m.berry_tree(6, 23, "BERRY_TREE_ICHOR_NERAIDA_SITRUS")
    m.item_ball(3, 16, "ITEM_MAX_REPEL", "FLAG_ICHOR_ITEM_NERAIDA_MAX_REPEL")
    m.item_ball(12, 3, "ITEM_PROTEIN", "FLAG_ICHOR_ITEM_NERAIDA_PROTEIN")
    m.objects[-1]["_floats"] = True               # on its rock in the pool, reached by Surf

    m.connect("down", PAPHIA_ROAD_X - SOUTH_ROAD[0], "MAP_KYTHERA_PAPHIA")
    m.seam("down")


VIEWS = [(14, 40), (11, 33), (10, 27), (5, 21), (13, 24), (20, 23), (20, 15), (21, 12), (14, 5), (25, 14)]


def main():
    m = compose()
    events(m)
    must = [(13, 25, "the ford's west end"), (19, 25, "the ford's east end"), (21, 13, "Krenaia's shrine"),
            (MILL_DOOR[0], MILL_DOOR[1] + 1, "the mill's door"), (3, 17, "the top terrace's jar"),
            (16, 11, "the fall's foot landing"), (5, 28, "the Lum tree"), (6, 24, "the Sitrus tree")]
    errors = m.build("kythera_neraida_falls", starts=[(14, H - 1), (9, 3), (20, 4)], must_reach=must, views=VIEWS,
                     render="--no-render" not in sys.argv)
    # the ledge path from the shelf comes back down, one way
    shelf = m.reach([(25, 4)])
    if (20, 30) not in shelf:
        errors.append("the ledge path from the upper shelf doesn't come back down to the river")
        print(f"{NAME} CHECK: {errors[-1]}")
    if (25, 4) in m.reach([(14, H - 1)]):
        errors.append("the upper shelf is reachable on foot from below")
        print(f"{NAME} CHECK: {errors[-1]}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
