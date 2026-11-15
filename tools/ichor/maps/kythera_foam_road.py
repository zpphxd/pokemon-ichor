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
SKANDEIA_ROAD = (9, 11)        # east edge: the road's rows
PAPHIA_ROAD = (8, 10)          # west edge: the road's rows
PAPHIA_GATE_Y = 21             # Paphia's east gate rows start here (its road is rows 21..23)
STAIR = (41, 42)               # the stair up to the spring, at the north edge
SPRING_OPENING_X = 12          # the spring's south opening starts at its x = 12


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


def compose():
    m = Map(NAME, "kythera", W, H, fill=A.GRASS)
    m.border = [A.SEA] * 4
    m.header = {"music": "MUS_ICHOR_ROAD", "weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_ROUTE",
                "show_map_name": True, "allow_cycling": True, "allow_running": True}

    # ---- the sea under everything south --------------------------------------------------
    m.rect(0, 13, W - 1, H - 1, A.SEA, False)

    # ==== the Skandeia strip, x 56..63: aethos only ==========================================
    m.rect(56, 0, 63, 12, A.GRASS, False)
    for x, y in ((56, 1), (58, 0), (60, 2), (62, 0), (61, 5), (57, 5)):
        m.olive(x, y)
    for x, y in ((59, 4), (63, 3), (56, 3)):
        m.cypress(x, y)
    m.path_patch(54, 9, 63, 11)
    m.rect(56, 12, 63, 13, A.SAND, False)
    aethos_shore(m, 56, 63, 14)
    m.rect(57, 7, 58, 7, A.ANEMONE, False)
    m.set(62, 7, A.TALL, False)

    # ==== the calm stretch and band 1, x 45..55 ===============================================
    # the ridge over the terrace
    m.rect(44, 0, 55, 3, A.GRASS, False)
    hedge(m, 44, 52, 3)
    for x, y in ((45, 0), (48, 1), (52, 0)):
        m.olive(x, y)
    m.cypress(51, 1)
    m.cypress(54, 1)
    m.piece("flowers", "briar_L", 53, 3)
    m.piece("flowers", "briar_R", 54, 3)
    m.piece("myrtle", "single", 55, 3)
    # the terrace, rows 4-5, stepping down east in two ledges
    m.rect(44, 4, 55, 5, A.GRASS, False)
    for y in (4, 5):
        m.set(47, y, A.LEDGE["E"], False)
        m.set(53, y, A.LEDGE["E"], False)
    for x in (45, 50, 51):
        m.piece("flowers", "thrift", x, 4)
    # the hedge between terrace and road
    hedge(m, 44, 52, 6)
    hedge(m, 44, 52, 7, ends=False)
    m.piece("myrtle", "SE", 52, 7)
    m.piece("myrtle", "NE", 52, 6)
    # the road, the shingle, and band 1 between hedge and sea-cliff
    m.rect(44, 8, 55, 11, A.SAND, False)
    m.blob("shingle", ["..#####...",
                       ".#######..",
                       "..######.."], 45, 9)
    m.blob("seagrass", ["###",
                        "###",
                        "###",
                        "###"], 49, 8)
    cliff(m, 49, 55, 12, foot="sea")
    m.set(56, 12, A.SAND, False)

    # ==== Amphitos's beach, x 44..48 ==========================================================
    m.shore(["#####",
             "~~~~~"], 44, 12)
    m.piece("sand_decor", "shells", 45, 11)
    m.piece("sand_decor", "wrack", 47, 12)
    m.piece("rocks", "tide_rock", 46, 15)

    # ==== the fork, x 39..43 ==================================================================
    m.rect(36, 0, 43, 3, A.GRASS, False)
    hedge(m, 36, 40, 3)
    hedge(m, 43, 43, 3, ends=False)
    m.piece("myrtle", "single", 43, 3)
    for x in STAIR:
        for y in range(0, 4):
            m.set(x, y, A.PATH, False)
        m.piece("myrtle", "gap_stair", x, 3)
    m.piece("myrtle", "V", 40, 0)
    m.piece("myrtle", "V", 40, 1)
    m.piece("myrtle", "V", 40, 2)
    m.piece("myrtle", "V", 43, 0)
    m.piece("myrtle", "V", 43, 1)
    m.piece("myrtle", "V", 43, 2)
    m.olive(37, 0)
    m.cypress(39, 1)
    m.path_patch(39, 4, 44, 11)
    m.set(41, 4, A.PATH)
    m.set(42, 4, A.PATH)
    m.piece("herm", "herm", 44, 5)
    m.piece("herm", "herm_base", 44, 6)
    m.set(39, 7, A.STELE, True)                  # the fork's sign
    m.shore(["######",
             "~~~~~~"], 38, 12)

    # ==== the cutting, x 28..38 ===============================================================
    m.rect(28, 0, 38, 4, A.GRASS, False)
    for x, y in ((28, 1), (31, 0), (35, 1)):
        m.olive(x, y)
    m.cypress(33, 2)
    m.cypress(30, 3)
    hedge(m, 36, 38, 4)
    cliff(m, 28, 38, 5, foot="sand", ends=False)
    m.rect(28, 8, 38, 8, A.SAND, False)
    m.shore(["###########",
             "~~~~~~~~~~~"], 28, 8)
    m.rect(38, 7, 39, 11, A.SAND, False)
    m.path_patch(39, 7, 41, 11)
    # the neck: marble blocks along the water's side of the path, east of Skopas
    for x in (36, 37, 38):
        m.piece("quarry", "blocks" if x % 2 else "block", x, 8)
    # the neck: marble blocks along the water's side of the path
    # band 2, straight behind Skopas
    m.blob("seagrass", ["####",
                        "####"], 30, 7)

    # ==== Aphrodite's rock, x 16..27 ==========================================================
    m.rect(16, 0, 27, 3, A.GRASS, False)
    cliff(m, 16, 27, 4, foot="sand", ends=False)
    m.piece("cliff", "seep", 25, 5)
    m.piece("falls", "basin", 25, 6)
    m.rect(16, 7, 27, 12, A.SAND, False)
    m.blob("shingle", ["....####....",
                       "...######...",
                       "..######...."], 16, 9, edge_in=False)
    m.shore(["############",
             "~~~~~~~~~~~~"], 16, 12)
    m.piece("sand_decor", "sherd_dig", 22, 11)
    m.piece("sand_decor", "scallop", 18, 10)
    m.piece("sand_decor", "lace", 20, 12 - 1)
    m.piece("sand_decor", "lace", 21, 12 - 1)
    m.piece("sand_decor", "footprints", 23, 8)
    m.piece("sand_decor", "wrack", 26, 11)
    rock = m.s("aphrodite_rock")
    for j in range(3):
        for i in range(3):
            m.set(19 + i, 15 + j, rock["ids"][j][i], True)
    # the reef spit out to Pontinos's platform
    for y in (13, 14, 15):
        m.piece("rocks", "spit_V", 25, y)
    m.piece("rocks", "spit_head", 25, 16)
    for x, y in ((23, 16), (24, 16), (23, 17), (24, 17)):
        m.piece("rocks", "spit_head", x, y)
    m.piece("rocks", "tide_rocks", 27, 18)
    m.piece("rocks", "tide_rock", 17, 19)

    # the quarry, cut into the hill behind the beach (the Girdle moves its drums)
    for x in range(16, 24):
        e = "cut_L" if x == 16 else ("cut_R" if x == 23 else "cut")
        m.piece("quarry", e, x, 0)
    m.part("quarry", "gate_TL", 18, 4, 2, 2)
    m.rect(17, 1, 22, 3, A.PATH, False)
    m.piece("quarry", "face_L", 16, 1)
    m.piece("quarry", "face_carved", 16, 2)
    m.piece("quarry", "face_R", 23, 1)
    m.piece("quarry", "face", 23, 2)
    m.piece("quarry", "face", 16, 3)
    m.piece("quarry", "face", 23, 3)
    m.piece("quarry", "step", 22, 1)
    m.piece("quarry", "step_edge", 22, 2)
    m.blob("seagrass", ["####.",
                        "#####"], 17, 1)
    m.piece("quarry", "drum_up", 21, 3)
    m.piece("quarry", "chips", 20, 2)

    # ==== the headland, the cascade and the cove (the Horn), x 9..15 ==========================
    m.rect(9, 12, 15, 13, A.GRASS, False)
    for x in range(9, 15):
        e = "_L" if x == 9 else ""
        m.piece("cliff", "lip" + e, x, 14)
        m.piece("cliff", "face" + e, x, 15)
        m.piece("cliff", "foot_sea" + e, x, 16)
    for y in (12, 13):
        m.piece("cliff", "side_E", 15, y)
        m.piece("cliff", "side_W", 8, y)
    m.piece("cliff", "lip_R", 15, 14)
    m.piece("cliff", "face_R", 15, 15)
    m.piece("cliff", "foot_sea_R", 15, 16)
    m.piece("cliff", "lip_L", 8, 14)
    m.piece("cliff", "face_L", 8, 15)
    m.piece("cliff", "foot_sea_L", 8, 16)
    m.piece("falls", "thin_fall", 12, 14)
    m.piece("falls", "thin_fall", 12, 15)
    m.piece("falls", "thin_sea", 12, 16)
    m.piece("falls", "thin_foot", 12, 13)
    m.piece("flowers", "thrift", 10, 12)
    m.piece("flowers", "briar", 14, 12)

    # ==== the myrtle grove and band 3, x 10..15 ===============================================
    m.rect(8, 0, 15, 11, A.GRASS, False)
    for x, y in ((8, 0), (11, 1), (14, 0)):
        m.olive(x, y)
    m.cypress(13, 3)
    m.piece("myrtle", "bush", 10, 4)
    hedge(m, 8, 15, 5)
    hedge(m, 8, 15, 11)
    m.rect(8, 6, 15, 10, A.GRASS, False)
    m.path_patch(8, 7, 15, 9)
    m.blob("seagrass", ["###",
                        "###",
                        "###",
                        "###",
                        "###"], 12, 6)
    m.piece("flowers", "petals", 9, 6)
    m.piece("flowers", "petals", 15, 10)

    # ==== the approach to Paphia, x 8..10, and Kassiteros's boat ===============================
    m.put("rollers", 8, 6)
    m.piece("myrtle", "bush", 9, 9)
    m.piece("myrtle", "single", 10, 9)

    # ==== the Paphia strip, x 0..7: aethos only ==============================================
    m.rect(0, 0, 7, 12, A.GRASS, False)
    m.path_patch(0, 7, 7, 10)
    for x, y in ((0, 1), (3, 0), (5, 2), (1, 4), (6, 11), (2, 11)):
        m.olive(x, y)
    for x, y in ((7, 4), (4, 4)):
        m.cypress(x, y)
    m.rect(0, 13, 7, 13, A.SAND, False)
    aethos_shore(m, 0, 7, 14)
    m.set(6, 6, A.STELE, True)                   # PAPHIA. The Temple of Aphrodite.
    return m


def events(m):
    # signs
    m.sign(55, 8, P + "SignEast")
    m.sign(39, 7, P + "SignFork")
    m.sign(6, 6, P + "SignPaphia")
    m.sign(44, 6, P + "Herm")
    m.sign(25, 6, P + "Basin")
    m.sign(22, 11, P + "DigSpot")
    m.sign(18, 5, P + "Drums")
    m.sign(19, 5, P + "Drums")
    m.sign(15, 12, P + "Cascade")
    m.sign(9, 7, P + "Boat")
    m.sign(10, 7, P + "Boat")

    # people
    m.obj("ICHOR_FISHER", 46, 12, P + "Amphitos", "MOVEMENT_TYPE_FACE_DOWN", trainer=True, sight=2)
    m.obj("HIKER", 34, 7, P + "Skopas", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=4)
    m.obj("ICHOR_DIVER", 24, 17, P + "Pontinos", "MOVEMENT_TYPE_FACE_UP", trainer=True, sight=1)
    m.obj("ICHOR_TITAN_GRUNT", 7, 8, P + "Kassiteros", "MOVEMENT_TYPE_FACE_RIGHT", trainer=True, sight=3,
          flag="FLAG_ICHOR_HIDE_KASSITEROS")
    m.obj("ICHOR_ALETHEA", 21, 10, P + "Alethea", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_ALETHEA_FOAM_ROAD", local_id="LOCALID_FOAM_ROAD_ALETHEA")
    m.obj("ICHOR_YOUTH_M", 44, 7, P + "Messenger", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_MESSENGER_FOAM_ROAD", local_id="LOCALID_FOAM_ROAD_MESSENGER")

    # items
    m.item_ball(23, 17, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_FOAM_ROAD_HYPER_POTION")
    m.item_ball(22, 1, "ITEM_RARE_CANDY", "FLAG_ICHOR_ITEM_FOAM_ROAD_RARE_CANDY")
    m.item_ball(10, 13, "ITEM_PRETTY_FEATHER", "FLAG_ICHOR_ITEM_FOAM_ROAD_PRETTY_FEATHER")

    # Aphrodite's rock: Alethea's scene, across the beach where the cutting opens
    for y in (7, 8):
        m.trigger(27, y, P + "AletheaRock")

    # connections
    m.connect("up", STAIR[0] - SPRING_OPENING_X, "MAP_KYTHERA_SPRING_OF_KALLIRHOE")
    m.connect("left", PAPHIA_ROAD[0] - PAPHIA_GATE_Y, "MAP_KYTHERA_PAPHIA")
    # TODO(skandeia): connect("right", ..., "MAP_KYTHERA_SKANDEIA") once Skandeia exists; its
    # west gate's road rows meet this map's rows SKANDEIA_ROAD (9..11).
    m.seam("left")
    m.seam("right")


VIEWS = [(58, 10), (51, 9), (46, 9), (41, 6), (36, 7), (31, 7), (24, 9), (20, 4), (21, 14), (12, 8), (5, 8), (12, 12)]


def main():
    m = compose()
    events(m)
    must = [(19, 6, "the quarry gate"), (22, 11, "the dig spot"), (24, 16, "Pontinos's platform"),
            (41, 0, "the spring stair"), (25, 7, "the basin")]
    errors = m.build("kythera_foam_road", starts=[(63, 10)], must_reach=must, views=VIEWS,
                     render="--no-render" not in sys.argv)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
