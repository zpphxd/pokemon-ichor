"""MAP_KYTHERA_SKANDEIA: Kythera's harbor town (SCRIPT.md Part 2, "Skandeia";
beats III-1C, III-1C2's street half, III-1I, the call on the way to Gytheion
and III-2's pointer).

Identity: the shipyard with no ships. North to south:
  the north bay, open water to Route 24, with the woods running down to it;
  the slipways, every one empty and chalked with a sickle but the one leaky
  boat the Titans left; Phereklos's yard beside them; the Euploia moored in
  the bay, her gangplank down on the quay's north edge;
  the promenade along the water, where the Titanborn porters carry oars;
  the east quay, where the Kronist preaches on the steps and the old sailor
  mends nets, with the Asclepeion and the Agora facing it from the first row
  of buildings (both in view from the gangplank), and the harbor shrine of
  Aphrodite at its south end;
  the town behind: the main street climbs west from the quay's head past
  Axylos's and Nikarete's doors to the west gate and the Foam Road; a pink
  terrace wall with a stair and a spring spout drops to the lower lane, the
  perfumer's and the divers' houses, and a pocket beach.

The main street's head (x = 19, rows 16-17) is the only way from the quay
into the town, so III-1C2's trigger there always runs before Axylos's door.

Seams (MAP_DESIGN.md §5): the west edge meets the Foam Road (gTileset_Kythera)
on the road at rows 16-17; the east edge meets Route 22's Myrtoan sea (rows
0-14) and Route 23 (rows 15-29), both gTileset_Melos; the north bay meets
Route 24 (the Lakonia writer's). So x 0-7, x 32-39 and rows 0-5 use only
aethos metatiles; check() enforces it.
"""
import kythera_outdoor as K
from kythera_outdoor import obj, sign, trigger, warp

NAME = "KytheraSkandeia"
P = "KytheraSkandeia_EventScript_"
W, H = 40, 30


def R(*segs):
    row = "".join(c * n for c, n in segs)
    assert len(row) == W, (row, len(row))
    return row


# ~ sea  s sand  g grass  f flowers  p limestone paving (streets, quay)
# T woods  B a structure laid in code  h a garden hedge (myrtle)  r rocky shore
PLAN = [
    R(("T", 20), ("s", 2), ("~", 18)),                                          # 0 the north bay
    R(("T", 20), ("s", 2), ("~", 18)),
    R(("T", 20), ("s", 2), ("~", 18)),
    R(("T", 20), ("s", 2), ("~", 18)),
    R(("T", 20), ("s", 2), ("~", 18)),
    R(("T", 20), ("s", 2), ("~", 18)),                                          # 5
    R(("T", 8), ("B", 5), ("g", 1), ("B", 8), ("~", 18)),                       # 6 Phereklos's yard; the slips
    R(("T", 8), ("B", 5), ("g", 1), ("B", 8), ("~", 18)),                       # 7  (the Euploia: x 22-29)
    R(("T", 8), ("B", 5), ("g", 1), ("~", 26)),                                 # 8 the slips' feet
    R(("T", 8), ("p", 6), ("B", 17), ("B", 1), ("~", 8)),                       # 9 the quay's north edge
    R(("T", 8), ("p", 23), ("B", 1), ("~", 8)),                                 # 10 the promenade
    R(("T", 8), ("p", 23), ("B", 1), ("~", 8)),                                 # 11
    R(("T", 8), ("h", 13), ("B", 4), ("p", 6), ("B", 1), ("~", 8)),             # 12 the Asclepeion
    R(("T", 7), ("g", 1), ("B", 5), ("h", 2), ("B", 4), ("h", 2), ("B", 4), ("p", 6), ("B", 1), ("~", 8)),  # 13
    R(("T", 7), ("g", 1), ("B", 5), ("h", 2), ("B", 4), ("h", 2), ("B", 4), ("p", 6), ("B", 1), ("~", 8)),  # 14
    R(("T", 5), ("g", 2), ("g", 1), ("B", 5), ("h", 2), ("B", 4), ("h", 2), ("B", 4), ("p", 6), ("B", 1), ("~", 8)),  # 15
    R(("p", 31), ("B", 1), ("~", 8)),                                           # 16 the main street, the road west
    R(("p", 31), ("B", 1), ("~", 8)),                                           # 17
    R(("T", 7), ("g", 1), ("B", 12), ("h", 1), ("p", 10), ("B", 1), ("~", 8)),  # 18 the terrace's top
    R(("T", 7), ("g", 1), ("B", 12), ("h", 1), ("B", 4), ("p", 6), ("B", 1), ("~", 8)),  # 19 the wall; the Agora
    R(("T", 8), ("g", 1), ("B", 3), ("g", 3), ("B", 3), ("g", 2), ("h", 1), ("B", 4), ("p", 6), ("B", 1), ("~", 8)),  # 20
    R(("T", 8), ("f", 1), ("B", 3), ("g", 1), ("p", 1), ("g", 1), ("B", 3), ("f", 1), ("g", 1), ("h", 1), ("B", 4), ("p", 6), ("B", 1), ("~", 8)),  # 21
    R(("T", 8), ("g", 1), ("B", 3), ("g", 1), ("p", 1), ("g", 1), ("B", 3), ("g", 2), ("h", 1), ("B", 4), ("p", 6), ("B", 1), ("~", 8)),  # 22
    R(("T", 8), ("p", 12), ("h", 1), ("p", 10), ("B", 1), ("~", 8)),            # 23 the lower lane; the Agora's front
    R(("T", 8), ("p", 12), ("h", 1), ("p", 10), ("B", 1), ("~", 8)),            # 24
    R(("T", 12), ("s", 8), ("b", 1), ("p", 10), ("B", 1), ("~", 8)),            # 25 the pocket beach; the shrine
    R(("T", 12), ("s", 8), ("b", 1), ("B", 11), ("~", 8)),                      # 26 the quay's south edge
    R(("T", 12), ("s", 6), ("~", 22)),                                          # 27
    R(("T", 12), ("~", 28)),                                                    # 28
    R(("T", 12), ("~", 28)),                                                    # 29
]
assert len(PLAN) == H

LEGEND = {"~": "sea", "s": "sand", "g": "grass", "f": "flowers", "p": "path", "T": "grass",
          "B": "path", "h": "grass", "r": "sea", "b": "sand"}

ASCLEPEION = (21, 12)   # door (22,15)
AGORA = (21, 19)        # door (22,22)
AXYLOS = (8, 13)        # long_house, door (10,15)
NIKARETE = (15, 13)     # cube_pot, door (16,15)
PERFUMER = (9, 20)      # cube, door (10,22)
DIVERS = (15, 20)       # stair_house, door (16,22)
PHEREKLOS = (8, 6)      # long_house, door (10,8)
TRIREME = (22, 6)       # gangplank (25,8) onto the quay's N_plank (25,9)
GANGPLANK = (25, 10)    # where the player lands
STREET_HEAD = 19        # the trigger column, rows 16-17
SLIPS = 14              # x 14-21, rows 6-8; the boat in the first (westmost) slip


def quay(g):
    """The quay's edges, laid where its paving meets the sea."""
    for x in range(14, 31):
        g.piece("quay", "N_plank" if x == 25 else "N", x, 9)
    g.piece("quay", "out_NE", 31, 9)
    for y in range(10, 26):
        g.piece("quay", "steps_E" if y == 14 else "E", 31, y)
    g.piece("quay", "out_SE", 31, 26)
    for x in range(21, 31):
        g.piece("quay", "ring_S" if x == 27 else ("S_b" if x == 24 else "S"), x, 26)


def compose():
    g = K.Grid(W, H, "skandeia")
    K.lay_ground(g, PLAN, LEGEND)

    # ---- the north bay's rocky shore (aethos-only rows)
    for y, row in enumerate(PLAN):
        for x, c in enumerate(row):
            if c == "r":
                g.set(x, y, K.SEA_ROCK, True)
            elif c == "b":
                g.set(x, y, K.BOULDER["sand"], True)

    # ---- the slips: the one boat the Titans left in the westmost, then three empty
    g.put("slips", SLIPS, 6, cx=2, w=2)          # slip_boat
    for i in (2, 4, 6):
        g.put("slips", SLIPS + i, 6, cx=0, w=2)  # slip
    g.set(13, 6, K.GRASS)
    g.set(13, 7, K.GRASS)
    g.set(13, 8, K.PATH["c"])

    # ---- the Euploia, moored in the bay
    g.put("trireme", TRIREME[0], TRIREME[1])
    quay(g)

    # ---- buildings
    g.block(K.ASCLEPEION, *ASCLEPEION)
    g.block(K.AGORA, *AGORA)
    g.set(ASCLEPEION[0] + 1, ASCLEPEION[1] + 3, K.ASCLEPEION[3][1], False)
    g.set(AGORA[0] + 1, AGORA[1] + 3, K.AGORA[3][1], False)
    g.front("long_house", *AXYLOS)
    g.front("cube_pot", *NIKARETE)
    g.front("cube", *PERFUMER)
    g.front("stair_house", *DIVERS)
    g.front("long_house", *PHEREKLOS)

    # ---- the terrace between the street and the lower lane: its stair at 13, a spout
    for x in range(8, 20):
        if x == 13:
            g.piece("terrace", "top_steps", x, 18)
            g.piece("terrace", "steps", x, 19)
        elif x == 17:
            g.piece("terrace", "top_spout", x, 18)
            g.piece("terrace", "spout", x, 19)
        else:
            top = "top_L" if x == 8 else "top_R" if x == 19 else ("top_M2" if x % 3 == 0 else "top")
            wall = "L" if x == 8 else "R" if x == 19 else ("M2" if x % 3 == 0 else "M")
            g.piece("terrace", top, x, 18)
            g.piece("terrace", wall, x, 19)

    # ---- hedges: myrtle along the gardens and the town's east side
    for y, row in enumerate(PLAN):
        for x, c in enumerate(row):
            if c == "h":
                left = x > 0 and PLAN[y][x - 1] == "h"
                right = x + 1 < W and PLAN[y][x + 1] == "h"
                name = "M" if left and right else "L" if right else "R" if left else (
                    "bush" if (x + y) % 2 else "single")
                g.piece("myrtle", name, x, y)

    # ---- the harbor: gear on the quay and the promenade
    for (x, y, name) in ((30, 11, "bollard"), (30, 17, "bollard"), (30, 22, "bollard"),
                         (27, 20, "nets"), (29, 12, "amphorae"), (30, 12, "crate"),
                         (15, 10, "oars"), (21, 11, "oars"), (12, 11, "rope"),
                         (29, 19, "rope"), (25, 21, "crate"), (28, 24, "rope"),
                         (28, 10, "bollard"), (25, 24, "amphorae"),
                         (26, 24, "crate"), (29, 15, "nets"), (17, 11, "oars"),
                         (27, 17, "amphorae"), (28, 17, "crate"), (26, 18, "rope")):
        g.piece("gear", name, x, y)
    g.put("shrine", 30, 24)                       # Aphrodite of the Harbor

    # ---- the lower town's gardens
    for (x, y, k, n) in ((8, 20, "flowers", "thrift"), (19, 21, "flowers", "petals"),
                         (12, 20, "flowers", "briar"), (14, 22, "flowers", "thrift")):
        g.piece(k, n, x, y)
    g.cypress(18, 20) if g.free(18, 20, 1, 2) else None

    # ---- the west gate: dry-stone walls either side of the road, and its sign
    for y in (13, 14, 15):
        g.set(7, y, K.WALL["e"], True)
    for y in (18, 19):
        g.set(7, y, K.WALL["e"], True)
    g.set(5, 15, K.STELE, True)                  # THE FOAM ROAD
    g.set(6, 15, K.GRASS)
    g.set(23, 11, K.STELE, True)                 # SKANDEIA

    # ---- the pocket beach: shells and wrack; tide rocks off the quay
    for (x, y, n) in ((13, 25, "shells"), (16, 26, "scallop"), (18, 25, "wrack")):
        g.piece("sand_decor", n, x, y)
    for (x, y) in ((21, 28), (36, 12), (35, 24), (38, 3), (33, 18), (26, 4)):
        g.set(x, y, K.SEA_ROCK, True)

    # ---- the north bay's beach: sand under the woods, aethos's own surf edge
    # (these rows are the Route 24 seam's aethos-only strip)
    for y in range(0, 6):
        g.set(21, y, K.SAND)
        g.set(22, y, 0x125)                      # aethos beach, sea to the east

    # ---- greenery: olive groves on the slopes above the town, wild woods at
    # their edges and along the seams
    trees = [(x, y) for y, row in enumerate(PLAN) for x, c in enumerate(row) if c == "T"]
    grove = {(x, y) for (x, y) in trees if (2 <= x <= 18 and y <= 4) or (1 <= x <= 10 and y >= 20)}
    g.orchard(grove, seed=5)
    g.woods([p for p in trees if p not in grove], seed=11, pines=0.25, cypresses=0.55)
    # the groves are walled, so their open grass never reads as a way in
    g.wall_h(8, 19, 5)
    g.wall_v(7, 20, 24)
    g.wall_h(8, 11, 25)
    return g


def specs():
    g = compose()
    objects = [
        obj("ICHOR_SAILOR", 26, 10, "left", P + "Nausikles", "LOCALID_SKANDEIA_NAUSIKLES"),
        obj("ICHOR_TITAN_GRUNT", 25, 11, "up", P + "Molybdos", "LOCALID_SKANDEIA_MOLYBDOS",
            "FLAG_ICHOR_HIDE_MOLYBDOS"),
        obj("ICHOR_MAN", 30, 14, "left", P + "Kronist", "LOCALID_SKANDEIA_KRONIST",
            "FLAG_ICHOR_HIDE_KRONIST_SKANDEIA"),
        obj("ICHOR_YOUTH_M", 28, 15, "right", P + "Dockhand", "LOCALID_SKANDEIA_DOCKHAND"),
        obj("ICHOR_ELDER_M", 28, 20, "left", P + "OldSailor", "LOCALID_SKANDEIA_OLD_SAILOR"),
        obj("ICHOR_TITAN_GRUNT", 11, 10, "leftright", P + "Porter", "LOCALID_SKANDEIA_PORTER_1",
            "FLAG_ICHOR_HIDE_SKANDEIA_PORTERS", rng=(2, 0)),
        obj("ICHOR_TITAN_GRUNT", 18, 11, "leftright", P + "Porter", "LOCALID_SKANDEIA_PORTER_2",
            "FLAG_ICHOR_HIDE_SKANDEIA_PORTERS", rng=(2, 0)),
        obj("ICHOR_WOMAN", 26, 21, "left", P + "Philinna", "LOCALID_SKANDEIA_PHILINNA"),
        obj("ICHOR_ALETHEA", 11, 16, "up", P + "Alethea", "LOCALID_SKANDEIA_ALETHEA_DOOR",
            "FLAG_ICHOR_HIDE_ALETHEA_SKANDEIA"),
        obj("ICHOR_ALETHEA", 24, 10, "right", P + "AletheaCall", "LOCALID_SKANDEIA_ALETHEA_CALL",
            "FLAG_ICHOR_HIDE_ALETHEA_CALL"),
    ]
    warps = [
        warp(22, 15, "MAP_KYTHERA_SKANDEIA_ASCLEPEION", 0),
        warp(22, 22, "MAP_KYTHERA_SKANDEIA_AGORA", 0),
        warp(10, 15, "MAP_KYTHERA_SKANDEIA_AXYLOS_HOUSE", 0),
        warp(16, 15, "MAP_KYTHERA_SKANDEIA_NIKARETE_HOUSE", 0),
        warp(10, 22, "MAP_KYTHERA_SKANDEIA_PERFUMERS_HOUSE", 0),
        warp(16, 22, "MAP_KYTHERA_SKANDEIA_DIVERS_HOUSE", 0),
        warp(10, 8, "MAP_KYTHERA_SKANDEIA_SHIPWRIGHTS_HOUSE", 0),
    ]
    bgs = [
        sign(SLIPS, 7, P + "Slips", "east"), sign(SLIPS, 6, P + "Slips", "east"),
        sign(30, 25, P + "HarborShrine"),
        sign(5, 15, P + "SignFoamRoad"),
        sign(23, 11, P + "SignSkandeia"),
        sign(17, 19, P + "Spout", "south"),
    ]
    coords = [trigger(STREET_HEAD, y, P + "AletheaRejoins", "VAR_TEMP_1", 1) for y in (16, 17)]
    coords += [trigger(x, 13, P + "KronistPreaches", "VAR_TEMP_2", 1) for x in range(25, 30)]
    spec = K.Spec(NAME, g, music="MUS_ICHOR_AKTI", mapsec="MAPSEC_KYTHERA_ISLE", map_type="MAP_TYPE_TOWN",
                  border=[K.SEA] * 4, objects=objects, warps=warps, bgs=bgs, coords=coords,
                  start=GANGPLANK,
                  seams={"west": 8, "east": 8, "north": 6},
                  connections=
                  [("right", "MAP_ROUTE22_MYRTOAN_SEA", -15), ("right", "MAP_ROUTE23_CRETAN_SEA", 15)],
                  screens={"1_gangplank": GANGPLANK, "2_slips": (13, 9), "3_quay": (28, 16),
                           "4_street_head": (20, 17), "5_street": (12, 17), "6_gate": (4, 16),
                           "7_lower_lane": (13, 23), "8_shrine": (27, 24), "9_agora": (23, 23)})
    return [spec]
