#!/usr/bin/env python3
"""MAP_KYTHERA_PAPHIA: the temple town on its hill above a west-facing bay (44 x 34).

design/phase4/SCRIPT.md Part 2 ("Paphia") and beats III-1D2 (Hermes's reveal at
the gate herm) and III-1F (Alethea sails on the honey boat). The Foam Road
comes in at the east gate onto the agora square: the Asclepeion by the gate, the
Agora across from it, the plain gate herm, a tripod, the goddess's statue and
two market stalls. The paved main street runs west under the terraces to the
foot of the great stair, which climbs the hill's spine past an avenue of
statues to the Temple of Aphrodite, alone at the top in its sacred wood with
cypresses at its flanks. The households: Pygmalion's workshop and his
sculptors' yard of marble blocks and half-carved figures; the dovecote and the
orchard house inside the north gate; the potter's house under the terrace; the
mirror-house at the head of the jetty stair. Below the street, garden plots
and olives run down to the beach, where the fishers' boats are drawn up; out on
the bay, the honey boat at the jetty. North, through the gate, the road to the
Neraida falls.

Seams (MAP_DESIGN.md §5): the 8 columns at the east edge (the Foam Road,
gTileset_Kythera) and the 6 rows at the north edge (the falls, gTileset_Neraida)
are aethos only.

  /usr/bin/python3 tools/ichor/maps/kythera_paphia.py [--no-render]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kythera_maps import A, Map, _hash  # noqa: E402

W, H = 44, 34
NAME = "KytheraPaphia"
P = "KytheraPaphia_EventScript_"

GATE_ROWS = (20, 23)           # the Foam Road's rows 7..10 sit on these rows (its road is our 21-22)
FOAM_ROAD_Y = 7
NORTH_ROAD = (30, 31)          # the road to the falls at the north edge
FALLS_OPENING_X = 14           # the falls' south opening starts at its x = 14

# The town's doors, in warp order (kythera_homes.py's DOORS uses these ids).
TEMPLE_DOOR = (22, 9)
DOORS = [
    ("MAP_KYTHERA_TEMPLE_OF_APHRODITE", TEMPLE_DOOR),
    ("MAP_KYTHERA_PAPHIA_ASCLEPEION", (39, 16)),
    ("MAP_KYTHERA_PAPHIA_AGORA", (33, 16)),
    ("MAP_KYTHERA_PAPHIA_PYGMALIONS_WORKSHOP", (14, 11)),
    ("MAP_KYTHERA_PAPHIA_DOVECOTE", (28, 12)),
    ("MAP_KYTHERA_PAPHIA_MIRROR_HOUSE", (10, 18)),
    ("MAP_KYTHERA_PAPHIA_ORCHARD_HOUSE", (34, 11)),
    ("MAP_KYTHERA_PAPHIA_POTTERS_HOUSE", (27, 18)),
]
JETTY_TRIGGER = [(9, 21), (9, 22)]
BOAT = (6, 24)                  # the honey boat's sail, top-left; hull below
EAST = 36                       # the aethos-only strip starts here
NORTH = 6                       # ... and above this row


def _row(*segs):
    return "".join(t * n for t, n in segs)


T = "T"
# One character a cell (zones: x 0-8 the bay, 9-17 the sculptors' quarter, 18-26
# the temple and its stair, 27-35 the north road, orchard and square, 36-43 the
# east strip). T wood, . grass, = limestone path, f flagstones, s sand, ~ sea,
# w aethos's waterline, Q the jetty, t a garden plot, y the sculptors' yard
# (marble chips), u / V the terrace's coping and wall, W a dry-stone wall,
# c a cypress, X a building or set piece placed in code (over grass).
PLAN = [
    _row((T, 9), (T, 9), (T, 9), (T, 3), ("=", 2), (T, 4), (T, 8)),                                       # 0
    _row((T, 9), (T, 9), (T, 9), (T, 3), ("=", 2), (T, 4), (T, 8)),                                       # 1
    _row((T, 9), (T, 9), (T, 9), (T, 3), ("=", 2), (T, 4), (T, 8)),                                       # 2
    _row((T, 9), (T, 9), (T, 9), (T, 3), ("=", 2), (T, 4), (T, 8)),                                       # 3
    _row((T, 9), (T, 9), (T, 9), (T, 3), ("=", 2), (T, 4), (T, 8)),                                       # 4
    _row((T, 9), (T, 9), (T, 9), (T, 2), ("X", 1), ("=", 2), (T, 4), (T, 8)),                             # 5
    _row((T, 9), (T, 5), (".", 4), ("c", 1), ("X", 7), ("c", 1), ("W", 3), ("=", 2), ("W", 4), (T, 8)),   # 6
    _row((T, 9), (T, 5), (".", 4), ("c", 1), ("X", 7), ("c", 1), ("X", 2), (".", 1), ("=", 2), ("X", 4),
         (T, 8)),                                                                                         # 7
    _row((T, 9), (T, 2), (".", 7), ("c", 1), ("X", 7), ("c", 1), ("X", 2), (".", 1), ("=", 2), ("X", 4),
         (T, 8)),                                                                                         # 8
    _row((T, 9), ("y", 3), ("X", 4), (".", 2), ("c", 1), ("X", 7), ("c", 1), ("t", 2), (".", 1), ("=", 2),
         ("X", 4), (T, 8)),                                                                               # 9
    _row((T, 9), ("y", 3), ("X", 4), (".", 2), (".", 1), ("X", 7), (".", 1), ("X", 2), (".", 1), ("=", 2),
         ("X", 4), (T, 8)),                                                                               # 10
    _row((T, 6), ("s", 3), ("y", 3), ("X", 4), (".", 2), ("f", 3), ("X", 3), ("f", 3), ("X", 2), (".", 1),
         ("=", 2), ("X", 4), (T, 8)),                                                                     # 11
    _row(("~", 4), ("s", 5), ("y", 7), (".", 2), ("X", 1), (".", 2), ("X", 3), (".", 2), ("X", 1), ("X", 2),
         (".", 1), ("=", 2), (".", 4), (T, 8)),                                                           # 12
    _row(("~", 6), ("s", 3), ("y", 7), (".", 2), ("X", 1), (".", 2), ("X", 3), (".", 2), ("X", 1), (".", 3),
         ("=", 2), ("X", 4), (".", 2), ("X", 4), (T, 2)),                                                 # 13
    _row(("~", 7), ("s", 2), ("u", 9), ("u", 3), ("X", 3), ("u", 3), ("u", 3), ("=", 2), ("X", 4), (".", 2),
         ("X", 4), (T, 2)),                                                                               # 14
    _row(("~", 7), ("s", 2), ("V", 9), ("V", 3), ("X", 3), ("V", 3), ("V", 3), ("=", 2), ("X", 4), (".", 2),
         ("X", 4), (T, 2)),                                                                               # 15
    _row(("~", 7), ("s", 2), ("X", 4), (".", 1), ("t", 3), (".", 1), (".", 3), ("X", 3), (".", 2), ("X", 1),
         ("X", 2), (".", 1), ("=", 2), ("X", 4), (".", 2), ("X", 4), (T, 2)),                             # 16
    _row(("~", 7), ("s", 2), ("X", 4), (".", 1), ("t", 3), (".", 1), (".", 3), ("X", 3), (".", 2), ("X", 1),
         ("X", 2), ("=", 7), ("=", 6), (T, 2)),                                                           # 17
    _row(("~", 7), ("s", 2), ("X", 4), (".", 1), ("t", 3), (".", 1), (".", 3), ("X", 3), (".", 2), ("X", 1),
         ("X", 2), ("=", 3), ("X", 2), ("=", 2), ("=", 6), (T, 2)),                                       # 18
    _row(("~", 7), ("s", 2), (".", 9), (".", 3), ("X", 3), ("X", 1), (".", 2), (".", 2), ("=", 3), ("X", 2),
         ("=", 1), ("X", 1), ("=", 1), ("=", 1), ("=", 3), ("=", 1), ("X", 1), (T, 1)),                   # 19
    _row(("~", 2), ("Q", 7), ("X", 1), ("f", 8), ("f", 9), ("f", 2), ("=", 6), ("X", 1), ("=", 6), (".", 2)),  # 20
    _row(("~", 2), ("Q", 7), ("X", 1), ("f", 8), ("f", 9), ("f", 2), ("=", 3), ("X", 2), ("=", 2), ("=", 8)),  # 21
    _row(("~", 2), ("Q", 7), ("X", 1), ("f", 3), (".", 5), (".", 9), (".", 2), ("=", 3), ("X", 2), ("=", 2),
         ("=", 8)),                                                                                       # 22
    _row(("~", 2), ("Q", 7), ("X", 1), (T, 2), ("t", 4), (".", 2), ("=", 2), (T, 6), ("t", 3), (".", 1),
         ("=", 2), (T, 4), (".", 8)),                                                                     # 23
    _row(("~", 8), ("s", 1), (".", 1), (T, 2), ("t", 4), ("f", 4), (T, 6), ("t", 3), (".", 1), ("=", 2),
         (T, 4), (".", 4), (T, 4)),                                                                       # 24
    _row(("~", 8), ("s", 8), ("f", 4), ("s", 20), (T, 4)),                                                # 25
    _row(("~", 8), ("s", 36)),                                                                            # 26
    _row(("~", 8), ("s", 24), ("~", 4), ("w", 8)),                                                        # 27
    _row(("~", 44)),                                                                                      # 28
    _row(("~", 44)),                                                                                      # 29
    _row(("~", 44)),                                                                                      # 30
    _row(("~", 44)),                                                                                      # 31
    _row(("~", 44)),                                                                                      # 32
    _row(("~", 44)),                                                                                      # 33
]
assert len(PLAN) == H and all(len(r) == W for r in PLAN), [(i, len(r)) for i, r in enumerate(PLAN) if len(r) != W]


def at(x, y):
    return PLAN[y][x] if 0 <= x < W and 0 <= y < H else "~"


def cells_of(chars, x0=0, x1=W - 1, y0=0, y1=H - 1):
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if at(x, y) in chars}


def strip(x, y):
    return x >= EAST or y < NORTH


def apple(m, x, y):
    m.part("apple", "apple_TL", x, y, 2, 2)


def terrace(m, x0, x1, y, steps=(), niche=(), spout=()):
    """A pink-rubble terrace wall on row y, with its coping (walkable) on row y-1."""
    for x in range(x0, x1 + 1):
        if x in steps:
            m.piece("terrace", "top_steps", x, y - 1)
            m.piece("terrace", "steps", x, y)
            continue
        if x in niche or x in spout:
            k = "niche" if x in niche else "spout"
            m.piece("terrace", "top_" + k, x, y - 1)
            m.piece("terrace", k, x, y)
            continue
        n = "L" if x == x0 else ("R" if x == x1 else ("M2" if x % 4 == 1 else "M"))
        m.piece("terrace", "top_" + n if n != "M" else "top", x, y - 1)
        m.piece("terrace", n, x, y)


def plot(m, cells):
    """A garden plot of tilled earth (aethos), edged by which neighbours are plot too."""
    for (x, y) in cells:
        n, s_ = (x, y - 1) in cells, (x, y + 1) in cells
        w, e = (x - 1, y) in cells, (x + 1, y) in cells
        v = "t" if not n else ("b" if not s_ else "")
        h = "l" if not w else ("r" if not e else "")
        key = {"tl": 0x103, "t": 0x104, "tr": 0x105, "l": 0x10B, "": 0x10C, "r": 0x10D,
               "bl": 0x113, "b": 0x114, "br": 0x115}[v + h]
        m.set(x, y, key, False)


def wall(m, x0, x1, y):
    for x in range(x0, x1 + 1):
        m.set(x, y, A.WALL["L"] if x == x0 else (A.WALL["R"] if x == x1 else A.WALL["M"]), True)


def flags(m, cells):
    for (x, y) in cells:
        k = _hash(x, y, 31) % 9
        m.piece("flags", "worn" if k == 0 else ("A", "B", "C")[(x * 2 + y + k) % 3], x, y)


def compose():
    m = Map(NAME, "paphia", W, H, fill=A.GRASS)
    m.border = [A.SEA] * 4
    m.header = {"music": "MUS_ICHOR_AKTI", "weather": "WEATHER_SUNNY", "map_type": "MAP_TYPE_TOWN",
                "show_map_name": True, "allow_cycling": True, "allow_running": True}

    # ---- ground ---------------------------------------------------------------------------
    for (x, y) in cells_of("s"):
        m.set(x, y, A.SAND, False)
    for (x, y) in cells_of("~Q"):
        m.set(x, y, A.SEA, False)
    for (x, y) in cells_of("w"):
        m.set(x, y, 0x12C, False)
    sea = cells_of("~Q") | cells_of("w")
    m.coast(sea, draw={(x, y) for (x, y) in sea if not strip(x, y)})
    m.sand_rim(cells_of("s"), lambda x, y: 0 <= x < W and 0 <= y < H and at(x, y) not in "s~wQ")
    square = {(x, y) for x in range(29, 42) for y in range(17, 23)}
    m.path(cells_of("="), context=cells_of("f") | (square & cells_of("X")) | {(9, 21), (9, 22)})
    flags(m, {c for c in cells_of("f") if not strip(*c)})
    plot(m, cells_of("t"))
    for (x, y) in cells_of("y"):
        m.piece("sculptors", "chips", x, y) if _hash(x, y, 3) % 3 == 0 else m.set(x, y, A.PATH, False)

    # ---- the north wood, the gate and the road to the falls ----------------------------------
    wall(m, 27, 29, 6)
    wall(m, 32, 35, 6)
    m.set(29, 5, A.STELE, True)                   # NORTH: THE NERAIDA FALLS

    # ---- the temple, its flanking cypresses, the forecourt's statues ---------------------------
    m.put("temple_front", 19, 6)
    for (x, y) in cells_of("c"):
        if at(x, y - 1) != "c" or (y - 6) % 2 == 0:
            if (y - 6) % 2 == 0:
                m.cypress(x, y)
                m.solid[y, x] = True          # the temple's flank: walked round
    for x in (18, 26):
        m.piece("props", "statue_g", x, 12)
        m.piece("props", "statue_g_base", x, 13)

    # ---- the great stair down the hill's spine ----------------------------------------------
    for y in range(11, 19):
        row = "land" if y == 15 else ""
        for i, side in enumerate(("L", "M", "R")):
            name = (row + "_" + side if side != "M" else row) if row else side
            m.piece("great_stair", name, 21 + i, y)
    for i, n in enumerate(("foot_L", "foot", "foot_R")):
        m.piece("great_stair", n, 21 + i, 19)
    m.set(24, 19, A.STELE, True)                  # THE TEMPLE OF APHRODITE

    # ---- the terrace wall between the upper town and the middle --------------------------------
    terrace(m, 9, 20, 15, steps=(15,), niche=(11,))
    terrace(m, 24, 29, 15, steps=(25,), spout=(27,))

    # ---- Pygmalion's workshop and the sculptors' yard ----------------------------------------
    m.front("chapel_house", 12, 9)
    for name, x, y in (("block_face", 9, 9), ("block", 10, 9), ("hoist", 9, 11), ("hoist_foot", 9, 12),
                       ("bench", 11, 13), ("block_face", 13, 13), ("block", 15, 12)):
        m.piece("sculptors", name, x, y)
    for name, x, y in (("drum_up", 11, 10), ("drum_fallen", 10, 12), ("drum_fallen_R", 11, 12),
                       ("blocks", 9, 13), ("block", 15, 13), ("chips_grass", 16, 12), ("chips_grass", 17, 13)):
        m.piece("marble", name, x, y)
    m.piece("props", "statue_g", 16, 10)          # the finished one, waiting to be fetched
    m.piece("props", "statue_g_base", 16, 11)

    # ---- the dovecote, the orchard and its house, the north gate's garden ---------------------
    m.put("dovecote", 27, 10)
    apple(m, 27, 7)
    apple(m, 32, 7)
    apple(m, 34, 7)
    m.front("paphia_house", 32, 9)                # the orchard house (Eumelos)

    # ---- the middle terrace: the mirror-house, the garden, the potter's ---------------------------
    m.front("paphia_narrow", 9, 16)               # Leukippe's mirror-house, at the jetty stair's head
    m.front("cube", 26, 16)                       # Lysis the potter
    m.piece("house", "pot_rose", 25, 18)
    m.piece("house", "pot_rose", 29, 18)
    m.piece("props", "statue_g", 19, 16)          # the garden's goddess
    m.piece("props", "statue_g_base", 19, 17)

    # ---- the agora square, the Asclepeion and the Agora, the gate herm ----------------------------
    m.block(A.AGORA, 32, 13)
    m.block(A.ASCLEPEION, 38, 13)
    for (_, (x, y)) in DOORS[1:3]:
        m.set(x, y, int(m.mid[y, x]), False)      # the doors
    m.set(42, 19, A.HERM, True)                   # the plain gate herm
    m.set(37, 14, A.TRIPOD_TOP, False)            # a bronze tripod on the green by the Asclepeion
    m.set(37, 15, A.TRIPOD, True)
    m.piece("props", "statue", 35, 19)
    m.piece("props", "statue_base", 35, 20)
    m.part("props", "stall_TL", 32, 18, 2, 2)
    m.part("props", "stall_TL", 32, 21, 2, 2)

    # ---- the jetty and the bay ---------------------------------------------------------------
    for x in range(2, 9):
        m.piece("quay", "N" if x > 2 else "out_NW", x, 20)
        m.set(x, 21, A.PATH, False)
        m.set(x, 22, A.PATH, False)
        m.piece("quay", "S" if x > 2 else "out_SW", x, 23)
    m.piece("quay", "W", 2, 21)
    m.piece("quay", "W", 2, 22)
    m.piece("quay", "S_plank", 6, 23)
    m.set(9, 21, A.STEPS, False)
    m.set(9, 22, A.STEPS, False)
    m.set(9, 20, A.BOULDER_SAND, True)
    m.set(9, 23, A.BOULDER_SAND, True)
    m.put("honey_boat", BOAT[0], BOAT[1])
    m.part("kaiki", "afloat", 1, 27, 3, 2)
    for name, x, y in (("nets", 4, 21), ("amphorae", 8, 22)):
        m.piece("gear", name, x, y)

    # ---- the beach: boats drawn up, the fishers' landing, boats out on the bay ------------------
    m.part("kaiki", "beached", 11, 25, 3, 2)
    m.part("kaiki", "beached", 24, 25, 3, 2)
    m.part("kaiki", "afloat", 15, 30, 3, 2)
    m.part("kaiki", "afloat", 29, 29, 3, 2)
    for name, x, y in (("nets", 16, 24), ("crate", 16, 25), ("amphorae", 19, 25)):
        m.piece("gear", name, x, y)
    for name, x, y in (("shells", 14, 27), ("lace", 21, 27), ("scallop", 29, 26), ("lace", 9, 26),
                       ("shells", 33, 26), ("lace", 26, 27)):
        m.piece("sand_decor", name, x, y)
    for (x, y) in ((3, 31), (22, 31), (38, 30), (41, 32), (7, 29), (34, 32), (12, 32)):
        m.set(x, y, A.SEA_ROCK_DEEP, True)

    # ---- the woods ------------------------------------------------------------------------
    m.woods(cells_of("T", y1=12), salt=11, aethos_only=strip, singles=[("myrtle", "bush"), ("myrtle", "single"),
                                                                        ("flowers", "briar")], from_bottom=True)
    m.woods(cells_of("T", y0=13), salt=12, aethos_only=strip, singles=[("myrtle", "bush"), ("flowers", "briar")])

    # ---- hedges, roses, flowers -------------------------------------------------------------
    for x, y in ((13, 16), (17, 16), (13, 18), (17, 18)):
        m.piece("myrtle", "bush" if (x + y) % 2 else "single", x, y)
    for x, y in ((18, 18), (20, 18), (24, 16), (24, 17), (10, 8), (17, 8)):
        m.piece("flowers", "briar", x, y)
    for x, y in ((14, 6), (15, 7), (12, 8), (16, 8), (18, 10), (26, 10), (19, 12), (25, 13), (24, 12),
                 (20, 13), (10, 19), (12, 19), (14, 19), (18, 19), (25, 19), (29, 12), (29, 9), (13, 22),
                 (16, 22), (26, 22), (21, 22), (34, 12), (35, 12), (29, 16), (29, 17)):
        m.piece("flowers", "petals" if (x + y) % 2 else "thrift", x, y)
    for x, y in ((36, 13), (37, 15), (36, 16), (41, 20), (39, 23), (36, 24), (43, 23), (37, 12)):
        m.set(x, y, A.ANEMONE, False)
    return m


def events(m):
    for i, (dest, (x, y)) in enumerate(DOORS):
        m.warp(x, y, dest, 0)

    m.sign(24, 19, P + "TempleStairSign")
    m.sign(29, 5, P + "SignFalls")
    m.sign(42, 19, P + "GateHerm")
    m.sign(11, 18, P + "JettyMirror")
    m.sign(33, 11, P + "OrchardMirror")
    m.sign(11, 15, P + "Niche")
    m.sign(27, 15, P + "Spout")

    # people
    m.obj("ICHOR_ALETHEA", 5, 21, P + "Alethea", "MOVEMENT_TYPE_FACE_RIGHT",
          flag="FLAG_ICHOR_HIDE_ALETHEA_PAPHIA", local_id="LOCALID_PAPHIA_ALETHEA")
    m.obj("ICHOR_SAILOR", 7, 22, P + "Skipper", "MOVEMENT_TYPE_FACE_LEFT",
          flag="FLAG_ICHOR_HIDE_ALETHEA_PAPHIA", local_id="LOCALID_PAPHIA_SKIPPER")
    m.obj("ICHOR_YOUTH_M", 41, 19, P + "Hermes", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_HERMES_PAPHIA", local_id="LOCALID_PAPHIA_HERMES")
    m.obj("ICHOR_HOPLITE", 29, 7, P + "Gatekeeper", "MOVEMENT_TYPE_FACE_RIGHT")
    m.obj("ICHOR_KID_F", 34, 21, P + "Girl", "MOVEMENT_TYPE_LOOK_AROUND")
    m.obj("ICHOR_ELDER_M", 33, 12, P + "OldMan", "MOVEMENT_TYPE_FACE_UP")

    m.item_ball(36, 13, "ITEM_LOVE_BALL", "FLAG_ICHOR_ITEM_PAPHIA_LOVE_BALL")
    m.hidden(28, 9, "ITEM_ULTRA_BALL", "FLAG_ICHOR_HIDDEN_PAPHIA_ULTRA_BALL")
    m.hidden(11, 19, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_PAPHIA_PEARL")

    for x, y in JETTY_TRIGGER:
        m.trigger(x, y, P + "AletheaSails", var="VAR_TEMP_0", value=1)

    m.connect("right", GATE_ROWS[0] - FOAM_ROAD_Y, "MAP_KYTHERA_FOAM_ROAD")
    m.connect("up", NORTH_ROAD[0] - FALLS_OPENING_X, "MAP_KYTHERA_NERAIDA_FALLS")
    m.seam("right")
    m.seam("up")


VIEWS = [(42, 21), (36, 19), (30, 20), (22, 20), (22, 12), (14, 12), (8, 21), (30, 9), (30, 3), (18, 25),
         (14, 18), (28, 24)]


def main():
    m = compose()
    events(m)
    must = [(x, y + 1, "a door's step") for _, (x, y) in DOORS]
    must += [(NORTH_ROAD[0], 0, "the falls road"), (6, 22, "the jetty"), (29, 6 + 1, "the gatekeeper's spot"),
             (19, 26, "the beach")]
    errors = m.build("kythera_paphia", starts=[(43, 21)], must_reach=must, views=VIEWS,
                     render="--no-render" not in sys.argv)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
