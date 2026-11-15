#!/usr/bin/env python3
"""MAP_KYTHERA_FOAM_ROAD: Skandeia's west gate to Paphia's east gate (64 x 24).

design/phase4/SCRIPT.md Part 2 ("The Foam Road") and beats III-1D, III-1D2.
East to west, walking away from Skandeia: a calm stretch and the road sign,
forced grass band 1 between the myrtle hedge and a sea-cliff, Amphitos on the
shingle, the fork (Kythera's great herm; the stair up to the Spring of
Kallirhoe), the cutting under the sea-cliff (Skopas at its neck, grass band 2
straight behind him), Aphrodite's rock with Alethea's dig and the freshwater
basin, Pontinos out on the reef spit guarding a jar, the quarry behind its
fallen drums (the Girdle), the cascade off the headland (the Horn) with its
cove, grass band 3 in the myrtle grove, Kassiteros and his boat on rollers at
the narrow approach, and the road on to Paphia.

The terrace above the hedge drops east in a run of ledges, so the walk back to
Skandeia skips band 1. Seams (MAP_DESIGN.md §5): the 8 columns at each end are
aethos only (Skandeia's and Paphia's secondaries differ); the stair's seam with
the spring is exempt (both kythera).

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
PAPHIA_ROAD = (7, 10)          # west edge: the road's rows
PAPHIA_GATE_Y = 20             # Paphia's east gate road is its rows 20..23
STAIR = (41, 42)               # the stair up to the spring, at the north edge
SPRING_OPENING_X = 12          # the spring's south opening starts at its x = 12

HERM = (43, 5)                 # the great herm's top; its base (the bg event) is the row below
ROCK_TRIGGER = [(27, 7), (27, 8)]


def hedge(m, x0, x1, y, ends=True):
    for x in range(x0, x1 + 1):
        n = "L" if (x == x0 and ends) else ("R" if (x == x1 and ends) else ("M2" if x % 3 == 2 else "M"))
        m.piece("myrtle", n, x, y)


def cliff(m, x0, x1, y, foot="sand", ends=True):
    """A south-facing pink cliff: lip row y, face y+1, foot y+2."""
    for x in range(x0, x1 + 1):
        e = "_L" if (x == x0 and ends) else ("_R" if (x == x1 and ends) else "")
        m.piece("cliff", "lip" + e, x, y)
        m.piece("cliff", "face" + e, x, y + 1)
        if foot == "sea":
            m.piece("cliff", "foot_sea" + e, x, y + 2)
        elif foot == "sand":
            m.piece("cliff", "foot_sand" if (x * 5 + y) % 7 else "foot_sand_rocks", x, y + 2)
        elif foot == "grass":
            m.piece("cliff", "foot_grass", x, y + 2)


def aethos_shore(m, x0, x1, y):
    """Row y is the waterline under sand, in aethos's own beach kit (for seam strips)."""
    for x in range(x0, x1 + 1):
        m.set(x, y, 0x12C, False)


def grove(m, olives=(), cypresses=(), pines=(), bushes=(), briars=()):
    for x, y in olives:
        m.olive(x, y)
    for x, y in pines:
        m.pine(x, y)
    for x, y in cypresses:
        m.cypress(x, y)
    for x, y in bushes:
        m.piece("myrtle", "bush" if (x + y) % 2 else "single", x, y)
    for x, y in briars:
        m.piece("flowers", "briar", x, y)


def cells(*rects):
    out = set()
    for x0, y0, x1, y1 in rects:
        out |= {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    return out


def compose():
    m = Map(NAME, "kythera", W, H, fill=A.GRASS)
    # The border: an olive wood, matching the ridge the camera sees past the quarry.
    m.border = [A.OLIVE_TOP[0], A.OLIVE_TOP[1], A.OLIVE_BOT_TIP[0], A.OLIVE_BOT_TIP[1]]
    m.header = {"music": "MUS_ICHOR_ROAD", "weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_ROUTE",
                "show_map_name": True, "allow_cycling": True, "allow_running": True}
    m.rect(0, 13, W - 1, H - 1, A.SEA, False)

    # ==== the Skandeia strip, x 56..63: aethos only; the road leaves at rows 9-10 =========
    grove(m, olives=[(56, 1), (59, 0), (62, 2), (57, 4), (60, 5), (62, 11), (58, 11)],
          cypresses=[(61, 3), (63, 6), (56, 6), (59, 3)])
    m.path(cells((52, 9, 55, 10), (54, 8, 55, 8), (56, 9, 63, 10)))
    for x, y in ((58, 8), (59, 8), (61, 8), (57, 7)):
        m.set(x, y, A.ANEMONE, False)
    m.rect(56, 13, 63, 13, A.SAND, False)
    m.set(56, 12, A.SAND, False)
    m.set(57, 12, A.SAND, False)
    m.set(63, 13, A.BOULDER_SAND, True)
    aethos_shore(m, 56, 63, 14)
    m.set(55, 7, A.STELE, True)                  # THE FOAM ROAD

    # ==== the ridge, the terrace and band 1, x 44..55 ========================================
    grove(m, olives=[(44, 0), (49, 1), (53, 0)], cypresses=[(47, 1), (52, 2), (55, 1)],
          bushes=[(46, 3), (51, 3)], briars=[(48, 3), (55, 3)])
    for y in (4, 5):                              # the terrace drops east in two ledges
        m.set(47, y, A.LEDGE["E"], False)
        m.set(53, y, A.LEDGE["E"], False)
    for x, y in ((45, 4), (49, 5), (50, 4), (52, 5), (54, 4)):
        m.piece("flowers", "thrift", x, y)
    hedge(m, 44, 53, 6)
    hedge(m, 44, 53, 7, ends=False)
    m.piece("myrtle", "SE", 53, 7)
    m.piece("myrtle", "NE", 53, 6)
    m.piece("myrtle", "SW", 44, 7)
    m.piece("myrtle", "NW", 44, 6)
    m.rect(44, 8, 51, 11, A.SAND, False)
    m.blob("shingle", ["..####..",
                       ".######.",
                       "..####.."], 43, 9, edge_in=False)
    m.blob("seagrass", ["###",
                        "###",
                        "###",
                        "###"], 49, 8)
    cliff(m, 49, 55, 12, foot="sea")
    m.piece("cliff", "corner_in_W", 49, 12)

    # ==== the fork, x 36..44: the stair to the spring, the great herm =========================
    grove(m, olives=[(36, 0), (38, 2)], cypresses=[(39, 0), (44, 3)], bushes=[(37, 4)])
    for x in (40, 43):
        for y in (0, 1, 2):
            m.piece("myrtle", "V", x, y)
        m.piece("myrtle", "B", x, 3)

    # ==== the cutting, x 28..38, and the rock beach, x 16..27 =================================
    grove(m, olives=[(28, 0), (31, 1), (34, 0)], pines=[(36, 2)], cypresses=[(30, 3), (33, 3), (29, 3)])
    cliff(m, 28, 37, 5, foot="sand", ends=False)
    m.piece("cliff", "lip_R", 38, 5)
    m.piece("cliff", "face_R", 38, 6)
    rows = []                                     # one shoreline from the beach along the cutting to the fork
    for y in range(6, 14):
        r = ""
        for x in range(16, 44):
            land = y <= 8 if 28 <= x <= 38 else y <= 12
            r += "#" if land else "~"
        rows.append(r)
    m.shore(rows, 16, 6)
    m.rect(39, 6, 43, 10, A.GRASS, False)         # the fork is a meadow above its own beach
    m.blob("shingle", ["...####",
                       ".######"], 37, 11, edge_in=False)
    for x in range(28, 38):
        m.piece("cliff", "foot_sand" if (x * 3) % 7 else "foot_sand_rocks", x, 7)
    m.blob("seagrass", ["####",
                        "####"], 30, 7)
    for x in (36, 37, 38):                        # the neck: marble blocks on the water's side
        m.piece("quarry", "blocks" if x % 2 else "block", x, 8)

    road = cells((STAIR[0], 0, STAIR[1], 7), (38, 7, 39, 8), (38, 8, 44, 9), (43, 10, 44, 10))
    m.path(road)
    for x in STAIR:
        m.piece("myrtle", "gap_stair", x, 3)
    m.piece("herm", "herm", HERM[0], HERM[1])
    m.piece("herm", "herm_base", HERM[0], HERM[1] + 1)
    m.set(39, 6, A.STELE, True)                   # the fork's sign
    for x, y in ((40, 5), (44, 5), (39, 4), (42, 10), (40, 10), (39, 10)):
        m.piece("flowers", "petals" if x % 2 else "thrift", x, y)

    # the beach: cliff, seep and basin, shingle, the dig, the rock offshore, the reef spit
    grove(m, olives=[(24, 0), (26, 2)], cypresses=[(25, 2)])
    cliff(m, 16, 27, 4, foot="sand", ends=False)
    m.piece("cliff", "seep", 25, 5)
    m.piece("falls", "basin", 25, 6)
    m.blob("shingle", ["....####....",
                       "...######...",
                       "..######...."], 16, 9, edge_in=False)
    for name, x, y in (("sherd_dig", 22, 11), ("scallop", 18, 10), ("lace", 20, 12), ("lace", 21, 12),
                       ("footprints", 23, 8), ("wrack", 26, 11), ("shells", 17, 7)):
        m.piece("sand_decor", name, x, y)
    rock = m.s("aphrodite_rock")
    for j in range(3):
        for i in range(3):
            m.set(19 + i, 15 + j, rock["ids"][j][i], True)
    for y in (13, 14, 15):
        m.piece("rocks", "spit_V", 25, y)
    for x, y in ((25, 16), (23, 16), (24, 16), (23, 17), (24, 17)):
        m.piece("rocks", "spit_head", x, y)
    m.piece("rocks", "tide_rocks", 28, 18)
    m.piece("rocks", "tide_rock", 17, 19)
    m.piece("rocks", "tide_rock", 33, 12)
    m.piece("rocks", "tide_rocks", 47, 16)

    # the quarry, cut into the hill behind the beach; the Girdle moves its drums
    for x in range(16, 24):
        m.piece("quarry", "cut_L" if x == 16 else ("cut_R" if x == 23 else "cut"), x, 0)
    m.rect(17, 1, 22, 3, A.PATH, False)
    for y, n in ((1, "face_L"), (2, "face_carved"), (3, "face")):
        m.piece("quarry", n, 16, y)
    for y, n in ((1, "face_R"), (2, "face"), (3, "face")):
        m.piece("quarry", n, 23, y)
    m.blob("seagrass", ["###..",
                        "####.",
                        "###.."], 17, 1, edge_in=False)
    m.piece("quarry", "step", 22, 1)
    m.piece("quarry", "step_edge", 22, 2)
    m.piece("quarry", "drum_up", 21, 3)
    m.piece("quarry", "chips", 20, 2)
    m.piece("quarry", "chips", 21, 1)
    m.part("quarry", "gate_TL", 18, 4, 2, 2)

    # ==== the headland, its cascade and the cove (the Horn), x 8..15 ===========================
    m.rect(9, 12, 14, 13, A.GRASS, False)
    for x in range(8, 16):
        e = "_L" if x == 8 else ("_R" if x == 15 else "")
        m.piece("cliff", "lip" + e, x, 14)
        m.piece("cliff", "face" + e, x, 15)
        m.piece("cliff", "foot_sea" + e, x, 16)
    for y in (12, 13):
        m.piece("cliff", "side_E", 15, y)
        m.piece("cliff", "side_W", 8, y)
    m.piece("falls", "thin_foot", 12, 13)
    m.piece("falls", "thin_fall", 12, 14)
    m.piece("falls", "thin_fall", 12, 15)
    m.piece("falls", "thin_sea", 12, 16)
    m.piece("flowers", "thrift", 9, 12)
    m.piece("flowers", "briar", 14, 12)
    m.piece("flowers", "petals", 13, 12)

    # ==== the myrtle grove and band 3, x 11..15; the approach, x 8..10 ==========================
    grove(m, olives=[(8, 0), (11, 1), (14, 0), (13, 3)], cypresses=[(10, 3), (15, 3)], bushes=[(9, 3)])
    hedge(m, 8, 15, 5)
    hedge(m, 11, 15, 11)
    m.path(cells((8, 8, 15, 8), (11, 7, 15, 9)))
    m.blob("seagrass", ["###",
                        "###",
                        "###",
                        "###",
                        "###"], 12, 6)
    m.piece("flowers", "petals", 11, 6)
    m.piece("flowers", "petals", 15, 10)
    m.put("rollers", 8, 6)                        # Kassiteros's boat, north of the neck
    m.piece("myrtle", "single", 9, 9)
    m.piece("flowers", "briar", 10, 9)
    hedge(m, 8, 10, 10)
    for x in (8, 9, 10):
        m.piece("flowers", "thrift" if x % 2 else "petals", x, 11)
    for name, x, y in (("rocks_sand", 17, 8), ("rock_sand", 26, 9), ("rocks_sand", 16, 11)):
        m.piece("rocks", name, x, y)

    # ==== the Paphia strip, x 0..7: aethos only; the road leaves at rows 7-10 ==================
    grove(m, olives=[(0, 0), (3, 1), (6, 0), (1, 4), (5, 4), (0, 11), (3, 11), (6, 11)],
          cypresses=[(7, 2), (4, 3), (2, 3)])
    m.path(cells((0, 8, 7, 9), (5, 7, 7, 7)))
    m.set(5, 6, A.STELE, True)                    # PAPHIA. The Temple of Aphrodite.
    for x, y in ((1, 7), (3, 7), (2, 6)):
        m.set(x, y, A.ANEMONE, False)
    m.rect(0, 13, 7, 13, A.SAND, False)
    m.set(0, 13, A.BOULDER_SAND, True)
    aethos_shore(m, 0, 7, 14)
    return m


def events(m):
    # signs
    m.sign(55, 7, P + "SignEast")
    m.sign(39, 6, P + "SignFork")
    m.sign(5, 6, P + "SignPaphia")
    m.sign(HERM[0], HERM[1] + 1, P + "Herm")
    m.sign(25, 6, P + "Basin")
    m.sign(22, 11, P + "DigSpot")
    m.sign(18, 5, P + "Drums")
    m.sign(19, 5, P + "Drums")
    m.sign(15, 12, P + "Cascade")
    for x in (8, 9, 10):
        m.sign(x, 7, P + "Boat")

    # people
    m.obj("ICHOR_FISHER", 46, 12, P + "Amphitos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2)
    m.obj("HIKER", 34, 7, P + "Skopas", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=4)
    m.obj("ICHOR_DIVER", 24, 17, P + "Pontinos", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1)
    m.obj("ICHOR_TITAN_GRUNT", 7, 8, P + "Kassiteros", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3,
          flag="FLAG_ICHOR_HIDE_KASSITEROS")
    m.obj("ICHOR_ALETHEA", 21, 10, P + "Alethea", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_ALETHEA_FOAM_ROAD", local_id="LOCALID_FOAM_ROAD_ALETHEA")
    m.obj("ICHOR_YOUTH_M", HERM[0] + 1, HERM[1], P + "Messenger", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_MESSENGER_FOAM_ROAD", local_id="LOCALID_FOAM_ROAD_MESSENGER")

    # items
    m.item_ball(23, 17, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_FOAM_ROAD_HYPER_POTION")
    m.item_ball(22, 1, "ITEM_RARE_CANDY", "FLAG_ICHOR_ITEM_FOAM_ROAD_RARE_CANDY")
    m.item_ball(10, 13, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_ITEM_FOAM_ROAD_PRETTY_FEATHER")

    # Aphrodite's rock: Alethea's scene, where the cutting opens onto the beach
    for x, y in ROCK_TRIGGER:
        m.trigger(x, y, P + "AletheaRock", var="VAR_TEMP_0", value=1)

    # connections
    m.connect("up", STAIR[0] - SPRING_OPENING_X, "MAP_KYTHERA_SPRING_OF_KALLIRHOE")
    m.connect("left", PAPHIA_ROAD[0] - PAPHIA_GATE_Y, "MAP_KYTHERA_PAPHIA")
    m.connect("right", SKANDEIA_ROAD[0] - SKANDEIA_GATE_Y, "MAP_KYTHERA_SKANDEIA")
    m.seam("left")
    m.seam("right")


VIEWS = [(58, 9), (51, 9), (46, 9), (41, 6), (35, 7), (27, 8), (21, 9), (20, 3), (21, 14), (12, 8), (4, 8), (12, 12)]


def main():
    m = compose()
    events(m)
    must = [(19, 6, "the quarry gate"), (22, 12, "the dig spot"), (24, 16, "Pontinos's platform"),
            (41, 0, "the spring stair"), (25, 7, "the basin"), (0, 8, "the Paphia seam"),
            (HERM[0], HERM[1] + 2, "the great herm's landing")]
    errors = m.build("kythera_foam_road", starts=[(63, 9)], must_reach=must, views=VIEWS,
                     render="--no-render" not in sys.argv)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
