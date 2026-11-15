#!/usr/bin/env python3
"""MAP_KYTHERA_FOAM_ROAD: Skandeia's west gate to Paphia's east gate (64 x 24).

design/phase4/SCRIPT.md Part 2 ("The Foam Road") and beats III-1D, III-1D2.
East to west, walking away from Skandeia: the road out of Skandeia's olive wood
and its sign; forced grass band 1 between the myrtle hedge and the sea-cliff;
Amphitos fishing off the shingle cove by his jetty; the fork (Kythera's great
herm; the stair up to the Spring of Kallirhoe); the cutting under the
sea-cliff (Skopas at its neck, band 2 straight behind him); Aphrodite's rock off
the beach, with Alethea's dig and the freshwater basin; Pontinos out on the
reef spit guarding a jar; the quarry behind its fallen drums (the Girdle); the
headland's cascade (the Horn) and its cliff-top meadow; band 3 in the myrtle
grove; Kassiteros and his boat on rollers at the narrow approach; Paphia.

The ground is drawn from PLAN (one character a cell), then the cliffs, the
quarry and the set pieces go over it in code. The terrace above the hedge drops
east in a run of ledges, so the walk back to Skandeia skips band 1. Seams
(MAP_DESIGN.md §5): the 8 columns at each end are aethos only (Skandeia's and
Paphia's secondaries differ); the stair's seam with the spring is exempt (both
kythera). The checks below prove each forced band can't be walked round.

  /usr/bin/python3 tools/ichor/maps/kythera_foam_road.py [--no-render]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kythera_maps import A, Map  # noqa: E402

W, H = 64, 24
NAME = "KytheraFoamRoad"
P = "KytheraFoamRoad_EventScript_"

# The seams the neighbours agree on.
SKANDEIA_ROAD = (9, 10)        # east edge: the road's rows
SKANDEIA_GATE_Y = 16           # Skandeia's west gate road is its rows 16-17
PAPHIA_ROAD = (7, 10)          # west edge: Paphia's gate rows 20..23 sit on these rows
PAPHIA_GATE_Y = 20
STAIR = (41, 42)               # the stair up to the spring, at the north edge
SPRING_OPENING_X = 12          # the spring's south opening starts at its x = 12

HERM = (43, 5)                 # the great herm's top; its base (the bg event) is the row below
ROCK_TRIGGER = [(27, 7), (27, 8)]
STRIP = 8                      # the aethos-only columns at each end

# One character a cell. T wood, . grass, g tall grass (sea-grass), = the road,
# s sand, ~ sea, h myrtle hedge, e an east-facing ledge, L/F a cliff's lip and
# face (the foot is the row below the face), Q the quarry, X a set piece placed in
# code over grass, w aethos's own waterline (the west strip), j the jetty.
def _row(*segs):
    """A plan row from (text, count) runs, read west to east."""
    return "".join(t * n for t, n in segs)


T, G, R, S, SEA = "T", "g", "=", "s", "~"
PLAN = [
    # x:  0-7 west strip | 8-15 the grove, Kassiteros, the Horn | 16-27 the rock beach, the quarry
    #     28-38 the cutting | 39-44 the fork | 45-55 the terrace, band 1, the cove | 56-63 east strip
    _row((T, 16), ("Q", 8), (T, 16), ("h", 1), (R, 2), ("h", 1), (T, 20)),                         # 0
    _row((T, 16), ("Q", 8), (T, 16), ("h", 1), (R, 2), ("h", 1), (T, 20)),                         # 1
    _row((T, 16), ("Q", 8), (T, 16), ("h", 1), (R, 2), ("h", 1), (T, 20)),                         # 2
    _row((T, 16), ("Q", 8), (T, 16), ("h", 1), (R, 2), ("h", 1), (T, 20)),                         # 3
    _row((T, 16), ("L", 12), (T, 11), (G, 2), (R, 2), (".", 1), (G, 3), ("e", 1), (G, 5), ("e", 1),
         (G, 2), (T, 8)),                                                                            # 4
    _row((T, 16), ("F", 12), ("L", 11), (G, 2), (R, 2), ("X", 1), (G, 3), ("e", 1), (G, 5), ("e", 1),
         (G, 2), (T, 8)),                                                                            # 5
    _row((T, 4), (".", 4), ("X", 3), ("k", 1), (G, 3), (".", 1), (G, 3), (".", 9), ("F", 11), ("X", 1),
         (".", 1), (R, 2), ("X", 1), ("h", 10), (G, 2), (".", 2), (T, 6)),                           # 6
    _row((".", 6), ("X", 1), (".", 1), ("X", 3), (R, 1), (G, 3), (R, 1), (R, 13), (".", 2), (G, 5),
         (R, 3), (R, 6), ("h", 9), (G, 2), (".", 2), (T, 6)),                                        # 7
    _row((R, 11), (R, 1), (G, 4), (G, 5), (".", 7), (R, 2), (G, 5), (R, 2), ("X", 2), (R, 6), (R, 3),
         (G, 8), ("X", 1), (".", 2), (T, 5)),                                                        # 8
    _row((R, 8), (".", 1), ("X", 2), (G, 4), (".", 1), (S, 12), (SEA, 11), (R, 9), (G, 8), (R, 8)),   # 9
    _row((".", 2), ("b", 5), (".", 1), ("h", 3), (".", 1), (G, 3), ("k", 1), (S, 12), (SEA, 11), (S, 9),
         (G, 8), (R, 8)),                                                                            # 10
    _row((T, 2), ("b", 6), ("h", 8), (S, 12), (SEA, 11), (S, 9), (G, 8), (".", 2), (T, 6)),         # 11
    _row((T, 2), ("b", 5), (".", 1), ("X", 1), (G, 6), ("X", 1), (S, 12), (SEA, 11), (S, 10), ("L", 7),
         (".", 2), (T, 6)),                                                                          # 12
    _row((S, 8), ("X", 1), (G, 3), ("X", 1), (G, 2), ("X", 1), (SEA, 31), ("j", 1), (SEA, 1), ("F", 7),
         (".", 6), (T, 2)),                                                                          # 13
    _row(("w", 8), ("L", 4), ("X", 1), ("L", 3), (SEA, 31), ("j", 1), (SEA, 8), (S, 1), ("b", 4), (".", 1),
         (T, 2)),                                                                                    # 14
    _row((SEA, 8), ("F", 4), ("X", 1), ("F", 3), (SEA, 31), ("j", 1), (SEA, 8), (S, 1), ("b", 5), (T, 2)),  # 15
    _row((SEA, 47), ("j", 1), (SEA, 7), (S, 2), ("b", 3), (T, 2), (T, 2)),                          # 16
    _row((SEA, 35), (S, 2), (SEA, 17), (S, 3), ("b", 3), (T, 2), (T, 2)),                           # 17
    _row((SEA, 34), (S, 4), (SEA, 15), (S, 4), ("b", 5), (T, 2)),                                   # 18
    _row((SEA, 35), (S, 2), (SEA, 15), (S, 5), ("b", 4), (".", 1), (T, 2)),                         # 19
    _row((SEA, 52), (S, 5), (".", 2), (T, 5)),                                                      # 20
    _row((SEA, 53), (S, 4), (T, 7)),                                                                # 21
    _row((SEA, 53), (S, 4), (T, 7)),                                                                # 22
    _row((SEA, 54), (S, 3), (T, 7)),                                                                # 23
]
assert len(PLAN) == H and all(len(r) == W for r in PLAN), [len(r) for r in PLAN]


def at(x, y):
    return PLAN[y][x] if 0 <= x < W and 0 <= y < H else "~"


def cells_of(chars, x0=0, x1=W - 1, y0=0, y1=H - 1):
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if at(x, y) in chars}


def strip(x, y):
    return x < STRIP or x >= W - STRIP


def cliff_run(m, x0, x1, y, ends=(True, True), feet=None):
    """A south-facing pink cliff: lip row y, face y+1, and its foot on row y+2
    chosen by what PLAN has there (sea, sand or grass), unless `feet` says."""
    for x in range(x0, x1 + 1):
        e = "_L" if (x == x0 and ends[0]) else ("_R" if (x == x1 and ends[1]) else "")
        m.piece("cliff", "lip" + e, x, y)
        m.piece("cliff", "face" + e, x, y + 1)
        below = feet if feet else at(x, y + 2)
        if below == "~":
            m.piece("cliff", "foot_sea" + e, x, y + 2)
        elif below == "s":
            m.piece("cliff", "foot_sand" if (x * 5 + y) % 4 else "foot_sand_rocks", x, y + 2)
        elif below in ".=X":
            m.piece("cliff", "foot_grass", x, y + 2)


def compose():
    m = Map(NAME, "kythera", W, H, fill=A.GRASS)
    # The border: an olive wood, as the ridge the camera sees past the quarry.
    m.border = [A.OLIVE_TOP[0], A.OLIVE_TOP[1], A.OLIVE_BOT_TIP[0], A.OLIVE_BOT_TIP[1]]
    m.header = {"music": "MUS_ICHOR_ROAD", "weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_ROUTE",
                "show_map_name": True, "allow_cycling": True, "allow_running": True}

    # ---- ground ---------------------------------------------------------------------------
    for (x, y) in cells_of("s"):
        m.set(x, y, A.SAND, False)
    for (x, y) in cells_of("~j"):
        m.set(x, y, A.SEA, False)
    for (x, y) in cells_of("w"):
        m.set(x, y, 0x12C, False)                 # aethos's beach edge, sea to the south
    for (x, y) in cells_of("e"):
        m.set(x, y, A.LEDGE["E"], False)
    for (x, y) in cells_of("b"):
        m.set(x, y, A.TALL, False)                # barley in the aethos strips

    # ---- the cliffs ------------------------------------------------------------------------
    cliff_run(m, 16, 27, 4, ends=(False, False))  # behind the rock beach (the quarry's gate in it)
    cliff_run(m, 28, 38, 5, ends=(False, True))   # over the cutting
    cliff_run(m, 49, 55, 12)                      # the headland under band 1
    cliff_run(m, 8, 15, 14)                       # the Horn's headland
    for y in (12, 13):
        m.piece("cliff", "side_W", 8, y)
        m.piece("cliff", "side_E", 15, y)
    m.piece("cliff", "seep", 25, 5)
    m.piece("falls", "basin", 25, 6)

    # ---- the sea's edge -------------------------------------------------------------------
    sea = cells_of("~j") | cells_of("w")
    m.coast(sea, draw={(x, y) for (x, y) in sea if not strip(x, y)})
    # the cliffs' sea feet stay cliff
    for x in range(49, 56):
        m.piece("cliff", "foot_sea" + ("_L" if x == 49 else "_R" if x == 55 else ""), x, 14)
    for x in range(8, 16):
        m.piece("cliff", "foot_sea" + ("_L" if x == 8 else "_R" if x == 15 else ""), x, 16)

    # ---- hedges ---------------------------------------------------------------------------
    m.hedge(cells_of("h"))
    for (x, y) in cells_of("k"):
        m.piece("myrtle", "bush", x, y)
    for x in STAIR:
        m.piece("myrtle", "gap_stair", x, 3)

    # ---- the road -------------------------------------------------------------------------
    m.path(cells_of("="))

    # ---- the quarry, cut into the hill; the Girdle moves its drums ----------------------------
    for x in range(16, 24):
        m.piece("quarry", "cut_L" if x == 16 else ("cut_R" if x == 23 else "cut"), x, 0)
    m.rect(17, 1, 22, 3, A.PATH, False)
    for y, n in ((1, "face_L"), (2, "face_carved"), (3, "face")):
        m.piece("quarry", n, 16, y)
    for y, n in ((1, "face_R"), (2, "face"), (3, "face")):
        m.piece("quarry", n, 23, y)
    m.piece("quarry", "step", 22, 1)
    m.piece("quarry", "step_edge", 22, 2)
    m.piece("quarry", "blocks", 20, 2)            # cut stone across the floor: round by the grass
    m.piece("quarry", "block", 21, 2)
    m.piece("quarry", "drum_up", 21, 3)
    m.piece("quarry", "chips", 20, 3)
    m.piece("quarry", "chips", 22, 3)
    m.part("quarry", "gate_TL", 18, 4, 2, 2)
    m.tallgrass({(17, 1), (18, 1), (19, 1), (20, 1), (17, 2), (18, 2), (19, 2), (17, 3), (18, 3), (19, 3)})

    # ---- the tall grass ---------------------------------------------------------------------
    quarry = {(x, y) for x in range(16, 24) for y in range(0, 4)}
    m.tallgrass(cells_of("g") - quarry)

    # ---- the woods ------------------------------------------------------------------------
    singles = [("myrtle", "bush"), ("myrtle", "single"), ("flowers", "briar"), ("myrtle", "bush"),
               ("rocks", "rock_grass")]
    m.woods(cells_of("T", y1=10), salt=7, aethos_only=strip, singles=singles, from_bottom=True)
    m.woods(cells_of("T", y0=11), salt=8, aethos_only=strip, singles=singles)

    # ---- the set pieces -------------------------------------------------------------------
    # the fork: the great herm and its sign
    m.piece("herm", "herm", HERM[0], HERM[1])
    m.piece("herm", "herm_base", HERM[0], HERM[1] + 1)
    m.set(39, 6, A.STELE, True)                   # the fork's sign
    m.set(56, 8, A.STELE, True)                   # THE FOAM ROAD
    m.set(6, 7, A.STELE, True)                    # PAPHIA. The Temple of Aphrodite.
    # Skopas's marble at the cutting's neck
    m.piece("quarry", "blocks", 37, 8)
    m.piece("quarry", "block", 38, 8)
    # Kassiteros's boat on its rollers, north of the neck, and his briar
    m.put("rollers", 8, 6)
    m.piece("flowers", "briar", 10, 9)
    # the Horn's cascade off the headland, and the meadow on top
    m.piece("falls", "thin_foot", 12, 13)
    m.piece("falls", "thin_fall", 12, 14)
    m.piece("falls", "thin_fall", 12, 15)
    m.piece("falls", "thin_sea", 12, 16)

    # Aphrodite's rock in the shallows, the reef spit, the tide rocks
    rock = m.s("aphrodite_rock")
    for j in range(3):
        for i in range(3):
            m.set(19 + i, 15 + j, rock["ids"][j][i], True)
    for y in (13, 14, 15):
        m.piece("rocks", "spit_V", 25, y)
    for x, y in ((25, 16), (23, 16), (24, 16), (23, 17), (24, 17)):
        m.piece("rocks", "spit_head", x, y)
    for name, x, y in (("tide_rocks", 28, 18), ("tide_rock", 17, 19), ("tide_rock", 31, 11),
                       ("tide_rocks", 41, 16), ("tide_rock", 47, 17), ("tide_rocks", 50, 18),
                       ("tide_rock", 14, 18), ("tide_rocks", 9, 19), ("tide_rock", 27, 14),
                       ("tide_rock", 33, 20), ("tide_rocks", 44, 21)):
        m.piece("rocks", name, x, y)
    for (x, y) in ((2, 16), (5, 19), (6, 20)):    # rocks off the west strip (aethos)
        m.set(x, y, A.SEA_ROCK_DEEP, True)
    for name, x, y in (("tide_rocks", 9, 21), ("tide_rock", 39, 20), ("tide_rocks", 40, 21),
                       ("tide_rock", 22, 21)):
        m.piece("rocks", name, x, y)
    # Amphitos's jetty off the shingle cove, a kaiki moored beside it, another drawn
    # up in the cove under the east wood
    for y in (13, 14, 15, 16):
        m.piece("jetty", "gangplank", 47, y)
    m.part("kaiki", "afloat", 44, 14, 3, 2)
    m.part("kaiki", "beached", 53, 21, 3, 2)

    # ---- shingle, sand and flowers --------------------------------------------------------
    m.sand_rim(cells_of("s"), lambda x, y: 0 <= x < W and 0 <= y < H and at(x, y) not in "s~jw")
    m.blob("shingle", ["...####...",
                       "..######..",
                       ".#######.."], 16, 9, edge_in=False)
    m.blob("shingle", ["..###.",
                       ".#####",
                       "..###."], 39, 10, edge_in=False)
    m.blob("shingle", [".##",
                       "###",
                       "##."], 53, 18, edge_in=False)
    for name, x, y in (("sherd_dig", 22, 11), ("scallop", 18, 11), ("lace", 20, 12), ("lace", 21, 12),
                       ("footprints", 24, 10), ("wrack", 26, 11), ("shells", 17, 9), ("lace", 16, 12),
                       ("shells", 44, 12), ("lace", 42, 12), ("wrack", 39, 12), ("footprints", 46, 10),
                       ("lace", 53, 21), ("shells", 55, 18), ("scallop", 36, 18), ("lace", 34, 18)):
        m.piece("sand_decor", name, x, y)
    for name, x, y in (("rocks_sand", 26, 9), ("rock_sand", 16, 10), ("rock_sand", 48, 12)):
        m.piece("rocks", name, x, y)

    # thrift on the terrace and the clifftops, petals blown along the road
    for x, y in ((43, 4), (55, 11), (57, 12), (61, 13), (2, 10), (7, 12), (29, 7), (36, 7), (20, 6),
                 (22, 6), (21, 8), (23, 8), (58, 20), (57, 6)):
        if int(m.mid[y, x]) != A.GRASS:
            continue
        if not strip(x, y):
            m.piece("flowers", "thrift", x, y)
        else:
            m.set(x, y, A.ANEMONE, False)
    for x, y in ((11, 6), (28, 7), (26, 6), (24, 6), (19, 6), (25, 8), (40, 6)):
        if int(m.mid[y, x]) == A.GRASS:
            m.piece("flowers", "petals", x, y)
    for x, y in ((1, 7), (3, 7), (4, 6), (57, 7), (56, 11), (7, 10), (60, 12), (58, 12), (61, 19)):
        if int(m.mid[y, x]) == A.GRASS:
            m.set(x, y, A.ANEMONE, False)
    return m


def events(m):
    # signs
    m.sign(56, 8, P + "SignEast")
    m.sign(39, 6, P + "SignFork")
    m.sign(6, 7, P + "SignPaphia")
    m.sign(HERM[0], HERM[1] + 1, P + "Herm")
    m.sign(25, 6, P + "Basin")
    m.sign(22, 11, P + "DigSpot")
    m.sign(18, 5, P + "Drums")
    m.sign(19, 5, P + "Drums")
    m.sign(15, 12, P + "Cascade")
    for x in (8, 9, 10):
        m.sign(x, 8, P + "Boat")

    # people
    m.obj("ICHOR_FISHER", 45, 11, P + "Amphitos", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=2)
    m.obj("HIKER", 36, 8, P + "Skopas", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1)
    m.obj("ICHOR_DIVER", 24, 17, P + "Pontinos", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1)
    m.obj("ICHOR_TITAN_GRUNT", 9, 9, P + "Kassiteros", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1,
          flag="FLAG_ICHOR_HIDE_KASSITEROS")
    m.obj("ICHOR_ALETHEA", 21, 10, P + "Alethea", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_ALETHEA_FOAM_ROAD", local_id="LOCALID_FOAM_ROAD_ALETHEA")
    m.obj("ICHOR_YOUTH_M", HERM[0] + 1, HERM[1], P + "Messenger", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_MESSENGER_FOAM_ROAD", local_id="LOCALID_FOAM_ROAD_MESSENGER")

    # the second wave (MAP_DESIGN §8): Lykon keeps the east end, Theano walks the terrace,
    # Kymodoke has the islet, Menalkas the clifftop meadow, Amaryllis the grove's edge
    m.obj("ICHOR_HOPLITE", 58, 8, P + "Lykon", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2)
    m.obj("ICHOR_ACOLYTE_F", 50, 4, P + "Theano", "MOVEMENT_TYPE_FACE_LEFT", trainer=True, sight=3)
    m.obj("ICHOR_DIVER", 36, 17, P + "Kymodoke", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=3)
    m.obj("ICHOR_SHEPHERD", 58, 13, P + "Menalkas", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3)
    m.obj("ICHOR_HARVESTER", 15, 6, P + "Amaryllis", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=3)
    m.obj("SPECIES(WOOLOO)", 59, 15, P + "Sheep", "MOVEMENT_TYPE_WANDER_AROUND", rx=1, ry=1)
    m.obj("SPECIES(WOOLOO)", 58, 18, P + "Sheep", "MOVEMENT_TYPE_FACE_LEFT")

    # items
    m.item_ball(3, 12, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_FOAM_ROAD_ULTRA_BALL")
    m.item_ball(23, 17, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_FOAM_ROAD_HYPER_POTION")
    m.item_ball(22, 1, "ITEM_RARE_CANDY", "FLAG_ICHOR_ITEM_FOAM_ROAD_RARE_CANDY")
    m.item_ball(10, 13, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_ITEM_FOAM_ROAD_PRETTY_FEATHER")
    m.item_ball(35, 18, "ITEM_PEARL_STRING", "FLAG_ICHOR_ITEM_FOAM_ROAD_PEARL_STRING")
    m.hidden(43, 4, "ITEM_ETHER", "FLAG_ICHOR_HIDDEN_FOAM_ROAD_ETHER")
    m.hidden(13, 13, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_FOAM_ROAD_HEART_SCALE")
    m.hidden(47, 17, "ITEM_NET_BALL", "FLAG_ICHOR_HIDDEN_FOAM_ROAD_NET_BALL")
    m.hidden(54, 22, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_FOAM_ROAD_STARDUST")

    # Aphrodite's rock: Alethea's scene, where the cutting opens onto the beach
    for x, y in ROCK_TRIGGER:
        m.trigger(x, y, P + "AletheaRock", var="VAR_TEMP_0", value=1)

    # connections
    m.connect("up", STAIR[0] - SPRING_OPENING_X, "MAP_KYTHERA_SPRING_OF_KALLIRHOE")
    m.connect("left", PAPHIA_ROAD[0] - PAPHIA_GATE_Y, "MAP_KYTHERA_PAPHIA")
    m.connect("right", SKANDEIA_ROAD[0] - SKANDEIA_GATE_Y, "MAP_KYTHERA_SKANDEIA")
    m.seam("left")
    m.seam("right")


VIEWS = [(58, 9), (51, 8), (45, 9), (41, 5), (34, 8), (25, 8), (20, 3), (21, 14), (13, 8), (5, 8), (12, 13),
         (36, 18)]


def check_bands(m):
    """Each forced band is walked through, never round: the fewest tall-grass
    steps from one side to the other."""
    errors = []
    for name, start, goal, need in (("band 1", [(57, 9)], [(47, 8), (47, 9)], 8),
                                    ("band 2", [(36, 7)], [(29, 8), (28, 7), (28, 8)], 4),
                                    ("band 3", [(16, 8)], [(10, 8)], 3)):
        n = m.min_grass(start, goal)
        print(f"  {name}: {n} tall-grass steps at the least")
        if n is None or n < need:
            errors.append(f"{name} can be crossed in {n} grass steps (needs {need})")
    return errors


def main():
    m = compose()
    events(m)
    must = [(19, 6, "the quarry gate"), (22, 12, "the dig spot"), (24, 16, "Pontinos's platform"),
            (41, 0, "the spring stair"), (25, 7, "the basin"), (0, 8, "the Paphia seam"),
            (HERM[0], HERM[1] + 2, "the great herm's landing"), (47, 16, "the jetty's end"),
            (43, 4, "behind the herm")]
    errors = m.build("kythera_foam_road", starts=[(63, 9)], must_reach=must, views=VIEWS,
                     render="--no-render" not in sys.argv)
    errors += check_bands(m)
    # the cliff-top meadow is the Horn's: not reachable on foot
    if (10, 13) in m.reach([(63, 9)], extra={(18, 4), (19, 4), (18, 5), (19, 5)}):
        errors.append("the Horn's meadow is reachable on foot")
    for e in errors[-3:]:
        print(f"{NAME} CHECK: {e}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
