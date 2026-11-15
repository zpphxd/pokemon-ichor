#!/usr/bin/env python3
"""MAP_KYTHERA_PAPHIA: the temple town on its hill above a west-facing bay (44 x 34).

design/phase4/SCRIPT.md Part 2 ("Paphia") and beats III-1D2 (Hermes's reveal at
the gate herm) and III-1F (Alethea sails on the honey boat). The Foam Road
comes in at the east gate onto the square, where the Asclepeion and the Agora
stand side by side in view of the gate, with the plain gate herm. The main
street runs west under the terraces to the foot of the great stair, which
climbs the hill's spine to the Temple of Aphrodite, alone at the top with doves
along its ridge. The households: Pygmalion's workshop by the stair, the
dovecote, the potter's cube house, the orchard house below the north gate, and
the mirror-house at the head of the jetty stair. North, through the orchard
and the gate, the road to the Neraida falls.

Seams (MAP_DESIGN.md §5): the 8 columns at the east edge (the Foam Road,
gTileset_Kythera) and the 6 rows at the north edge (the falls, gTileset_Neraida)
are aethos only.

  /usr/bin/python3 tools/ichor/maps/kythera_paphia.py [--no-render]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kythera_maps import A, Map  # noqa: E402

W, H = 44, 34
NAME = "KytheraPaphia"
P = "KytheraPaphia_EventScript_"

GATE_ROWS = (20, 23)           # the east gate: the Foam Road's rows 7..10
FOAM_ROAD_Y = 7
NORTH_ROAD = (30, 31)          # the road to the falls at the north edge
FALLS_OPENING_X = 14           # the falls' south opening starts at its x = 14

# The town's doors, in warp order (kythera_homes.py's DOORS uses these ids).
TEMPLE_DOOR = (22, 9)
DOORS = [
    ("MAP_KYTHERA_TEMPLE_OF_APHRODITE", TEMPLE_DOOR),
    ("MAP_KYTHERA_PAPHIA_ASCLEPEION", (38, 16)),
    ("MAP_KYTHERA_PAPHIA_AGORA", (33, 16)),
    ("MAP_KYTHERA_PAPHIA_PYGMALIONS_WORKSHOP", (17, 13)),
    ("MAP_KYTHERA_PAPHIA_DOVECOTE", (27, 13)),
    ("MAP_KYTHERA_PAPHIA_MIRROR_HOUSE", (10, 19)),
    ("MAP_KYTHERA_PAPHIA_ORCHARD_HOUSE", (34, 11)),
    ("MAP_KYTHERA_PAPHIA_POTTERS_HOUSE", (27, 18)),
]
JETTY_TRIGGER = [(9, 21), (9, 22)]
BOAT = (6, 24)                  # the honey boat's sail, top-left; hull below


def cells(*rects):
    out = set()
    for x0, y0, x1, y1 in rects:
        out |= {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    return out


def grove(m, olives=(), cypresses=(), pines=()):
    for x, y in olives:
        m.olive(x, y)
    for x, y in pines:
        m.pine(x, y)
    for x, y in cypresses:
        m.cypress(x, y)


def apple(m, x, y):
    m.part("apple", "apple_TL", x, y, 2, 2)


def terrace(m, x0, x1, y, steps=()):
    """A pink-rubble terrace wall on row y, with its coping (walkable) on row y-1."""
    for x in range(x0, x1 + 1):
        if x in steps:
            m.piece("terrace", "top_steps", x, y - 1)
            m.piece("terrace", "steps", x, y)
            continue
        n = "L" if x == x0 else ("R" if x == x1 else ("M2" if x % 4 == 1 else "M"))
        m.piece("terrace", "top_" + n if n != "M" else "top", x, y - 1)
        m.piece("terrace", n, x, y)


def compose():
    m = Map(NAME, "paphia", W, H, fill=A.GRASS)
    m.border = [A.SEA] * 4
    m.header = {"music": "MUS_ICHOR_AKTI", "weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_TOWN",
                "show_map_name": True, "allow_cycling": True, "allow_running": True}

    # ---- the bay (west) and the sea (south) ------------------------------------------------
    land = [[True] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if y >= 27 or (x <= 8 and y >= 14) or (x <= 3 and y >= 12):
                land[y][x] = False
    for y in range(H):
        for x in range(W):
            if not land[y][x]:
                m.set(x, y, A.SEA, False)
    # a sand margin round the water, then the waterline from the surf kit
    rows = []
    for y in range(10, H):
        r = ""
        for x in range(W):
            if not land[y][x]:
                r += "~"
            elif any(0 <= x + dx < W and 0 <= y + dy < H and not land[y + dy][x + dx]
                     for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                r += "#"
            else:
                r += " "
        rows.append(r)
    m.shore(rows, 0, 10)
    m.rect(10, 26, 35, 26, A.SAND, False)
    # the east strip's beach in aethos's own kit
    m.rect(36, 26, 43, 26, A.SAND, False)
    for x in range(36, 44):
        m.set(x, 27, 0x12C, False)

    # ---- the north band (rows 0..5, aethos only): olives, the road to the falls -----------
    grove(m, olives=[(0, 0), (3, 1), (6, 0), (9, 2), (12, 0), (15, 1), (18, 0), (21, 2), (24, 0),
                     (27, 1), (34, 1), (37, 0), (40, 2), (42, 0), (1, 4), (13, 4)],
          cypresses=[(5, 3), (8, 4), (11, 3), (17, 3), (20, 4), (26, 3), (33, 3), (36, 3), (39, 4), (42, 3)],
          pines=[(23, 3)])
    north = cells((NORTH_ROAD[0], 0, NORTH_ROAD[1], 19))
    m.set(28, 5, A.STELE, True)                   # NORTH: THE NERAIDA FALLS
    # the north gate: dry-stone walls either side of the road
    for x in range(25, 30):
        m.set(x, 6, A.WALL["L"] if x == 25 else A.WALL["M"], True)
    for x in range(32, 36):
        m.set(x, 6, A.WALL["R"] if x == 35 else A.WALL["M"], True)

    # ---- the upper terrace: the temple, the orchard, Pygmalion's, the dovecote -------------
    m.put("temple_front", 19, 6)
    # the orchard either side of the road to the north gate
    for x, y in ((28, 7), (26, 8), (28, 10), (32, 7), (34, 7)):
        apple(m, x, y)
    grove(m, olives=[(37, 7), (40, 9), (11, 7), (14, 6), (8, 10)], cypresses=[(18, 6), (26, 6), (42, 6), (39, 11),
                                                                         (36, 11), (10, 10)])
    for x, y in ((29, 12), (25, 10), (16, 9), (12, 10)):
        m.piece("myrtle", "bush" if x % 2 else "single", x, y)
    for x, y in ((26, 10), (27, 10), (13, 9), (17, 10), (35, 12)):
        m.piece("flowers", "petals" if (x + y) % 2 else "thrift", x, y)
    m.front("paphia_house", 32, 9)                # the orchard house (Eumelos)
    m.front("chapel_house", 15, 11)               # Pygmalion's workshop
    m.put("dovecote", 26, 11)                     # Peristera's dovecote
    for name, x, y in (("block", 12, 12), ("block_face", 13, 13), ("bench", 11, 13), ("chips", 12, 13),
                       ("chips", 14, 13)):
        m.piece("sculptors", name, x, y)
    m.part("sculptors", "hoist", 14, 12, 1, 1)
    for x, y in ((19, 12), (25, 12), (20, 13), (24, 13), (28, 12)):
        m.piece("flowers", "petals", x, y)

    # ---- the great stair down the hill's spine ----------------------------------------------
    for y in range(11, 19):
        row = "land" if y == 15 else ""
        for i, side in enumerate(("L", "M", "R")):
            name = (row + "_" + side if side != "M" else row) if row else side
            m.piece("great_stair", name, 21 + i, y)
    for i, n in enumerate(("foot_L", "foot", "foot_R")):
        m.piece("great_stair", n, 21 + i, 19)
    m.set(24, 19, A.STELE, True)                  # THE TEMPLE OF APHRODITE

    # ---- the terrace wall between the upper town and the street ----------------------------
    terrace(m, 10, 20, 15, steps=(13,))
    terrace(m, 24, 29, 15, steps=())
    m.piece("terrace", "niche", 17, 15)
    m.piece("terrace", "top_niche", 17, 14)
    m.piece("terrace", "spout", 26, 15)
    m.piece("terrace", "top_spout", 26, 14)

    # ---- the middle: the mirror-house, the potter's -----------------------------------------
    m.front("paphia_narrow", 9, 17)               # Leukippe's mirror-house, at the jetty stair's head
    m.front("cube", 26, 16)                       # Lysis the potter
    for x, y in ((25, 18), (29, 18)):
        m.piece("house", "pot_rose", x, y)
    m.piece("flowers", "briar_L", 14, 17)
    m.piece("flowers", "briar_R", 15, 17)
    m.piece("flowers", "briar", 19, 17)

    # ---- the square, the Asclepeion and the Agora, the gate herm ----------------------------
    m.block(A.AGORA, 32, 13)
    m.block(A.ASCLEPEION, 37, 13)
    for (x, y) in ((33, 16), (38, 16)):
        m.set(x, y, int(m.mid[y, x]), False)      # the doors
    m.set(42, 18, A.HERM, True)                   # the plain gate herm
    m.set(36, 18, A.TRIPOD_TOP, False)            # a bronze tripod in the square
    m.set(36, 19, A.TRIPOD, True)
    # the middle terrace's garden, between the mirror-house and the stair
    m.olive(16, 17)
    for x, y in ((18, 17), (19, 18), (14, 19), (20, 16)):
        m.piece("flowers", "petals" if x % 2 else "thrift", x, y)
    m.piece("myrtle", "bush", 18, 19)
    m.piece("myrtle", "single", 30 - 1, 17)
    grove(m, cypresses=[(42, 15), (43, 12), (36, 17)], olives=[(40, 24), (37, 24), (42, 24)])

    # ---- the street, the square, the jetty stair ---------------------------------------------
    street = cells((10, 20, 30, 21), (31, 20, 43, 22), (31, 17, 41, 19), (22, 22, 24, 22), (36, 23, 43, 23), (NORTH_ROAD[0], 13, NORTH_ROAD[1], 19),
                   (13, 16, 13, 19))
    m.path(street | north)
    m.set(9, 21, A.STEPS, False)
    m.set(9, 22, A.STEPS, False)
    m.set(9, 20, A.BOULDER_SAND, True)
    m.set(9, 23, A.BOULDER_SAND, True)

    # gardens south of the street
    for x, y in ((12, 23), (16, 24), (20, 23), (25, 24), (29, 23), (33, 24)):
        m.olive(x, y)
    for x, y in ((15, 23), (19, 24), (24, 23), (28, 24), (32, 23)):
        m.piece("flowers", "petals" if x % 2 else "briar", x, y)
    for x, y in ((18, 23), (23, 24), (31, 24)):
        m.cypress(x, y)

    # ---- the jetty ------------------------------------------------------------------------
    for x in range(2, 9):
        m.piece("quay", "N" if x > 2 else "out_NW", x, 20)
        m.set(x, 21, A.PATH, False)
        m.set(x, 22, A.PATH, False)
        m.piece("quay", "S" if x > 2 else "out_SW", x, 23)
    m.piece("quay", "W", 2, 21)
    m.piece("quay", "W", 2, 22)
    m.piece("quay", "S_plank", 6, 23)
    m.put("honey_boat", BOAT[0], BOAT[1])
    m.part("kaiki", "afloat", 1, 27, 3, 2)
    return m


def events(m):
    for i, (dest, (x, y)) in enumerate(DOORS):
        m.warp(x, y, dest, 0)

    m.sign(24, 19, P + "TempleStairSign")
    m.sign(28, 5, P + "SignFalls")
    m.sign(42, 18, P + "GateHerm")
    m.sign(11, 19, P + "JettyMirror")
    m.sign(33, 11, P + "OrchardMirror")
    m.sign(17, 15, P + "Niche")
    m.sign(26, 15, P + "Spout")

    # people
    m.obj("ICHOR_ALETHEA", 5, 21, P + "Alethea", "MOVEMENT_TYPE_FACE_RIGHT",
          flag="FLAG_ICHOR_HIDE_ALETHEA_PAPHIA", local_id="LOCALID_PAPHIA_ALETHEA")
    m.obj("ICHOR_SAILOR", 7, 22, P + "Skipper", "MOVEMENT_TYPE_FACE_LEFT",
          flag="FLAG_ICHOR_HIDE_ALETHEA_PAPHIA", local_id="LOCALID_PAPHIA_SKIPPER")
    m.obj("ICHOR_YOUTH_M", 41, 18, P + "Hermes", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_HERMES_PAPHIA", local_id="LOCALID_PAPHIA_HERMES")
    m.obj("ICHOR_HOPLITE", 32, 7, P + "Gatekeeper", "MOVEMENT_TYPE_FACE_LEFT")
    m.obj("ICHOR_KID_F", 34, 20, P + "Girl", "MOVEMENT_TYPE_LOOK_AROUND")
    m.obj("ICHOR_ELDER_M", 33, 12, P + "OldMan", "MOVEMENT_TYPE_FACE_UP")

    for x, y in JETTY_TRIGGER:
        m.trigger(x, y, P + "AletheaSails", var="VAR_TEMP_0", value=1)

    m.connect("right", GATE_ROWS[0] - FOAM_ROAD_Y, "MAP_KYTHERA_FOAM_ROAD")
    m.connect("up", NORTH_ROAD[0] - FALLS_OPENING_X, "MAP_KYTHERA_NERAIDA_FALLS")
    m.seam("right")
    m.seam("up")


VIEWS = [(42, 21), (36, 19), (30, 21), (22, 20), (22, 12), (14, 18), (8, 21), (30, 9), (30, 3)]


def main():
    m = compose()
    events(m)
    must = [(x, y + 1, "a door's step") for _, (x, y) in DOORS]
    must += [(NORTH_ROAD[0], 0, "the falls road"), (6, 22, "the jetty")]
    errors = m.build("kythera_paphia", starts=[(43, 21)], must_reach=must, views=VIEWS,
                     render="--no-render" not in sys.argv)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
