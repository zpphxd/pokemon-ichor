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

Finds: a Sea Incense in the pocket beach's far corner; hidden, a Big Pearl in
the harbor shrine's niche among the shells and a Heart Scale at the foot of
the boat's slip.

The main street's head (x = 19, rows 16-17) is the only way from the quay
into the town, so III-1C2's trigger there always runs before Axylos's door.

Seams (MAP_DESIGN.md §5): the west edge meets the Foam Road (gTileset_Kythera)
on the road at rows 16-17; the east edge meets Route 22's Myrtoan sea (rows
0-14) and Route 23 (rows 15-29), both gTileset_Melos; the north bay meets
Route 24 (the Lakonia writer's). So x 0-7, x 32-39 and rows 0-5 use only
aethos metatiles; check() enforces it.
"""
import kythera_outdoor as K
from kythera_outdoor import obj, sign, trigger, warp, hidden, item_ball

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
RECESS = (17, 18, 19, 20, 21)   # the mooring bay in the quay's east face


def quay(g):
    """The quay's edges, laid where its paving meets the sea."""
    for x in range(14, 31):
        g.piece("quay", "N_plank" if x == 25 else "N", x, 9)
    g.piece("quay", "out_NE", 31, 9)
    # the east face steps back into a mooring bay (rows 17-21), so the quay
    # never runs as one ruler line down the harbor (STYLE §4.2 "Edges")
    for y in range(10, 26):
        if y in RECESS:
            g.set(31, y, K.SEA, False)
            g.piece("quay", "E", 30, y)
        elif y == RECESS[0] - 1:
            g.piece("quay", "out_SE", 31, y)
            g.piece("quay", "in_SE", 30, y)
        elif y == RECESS[-1] + 1:
            g.piece("quay", "out_NE", 31, y)
            g.piece("quay", "in_NE", 30, y)
        else:
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

    # ---- buildings: each house its own front (roofs, doves, a chimney, a vine,
    # an outside stair, pots on the step), and Nikarete's under a tiled roof
    g.block(K.ASCLEPEION, *ASCLEPEION)
    g.block(K.AGORA, *AGORA)
    g.set(ASCLEPEION[0] + 1, ASCLEPEION[1] + 3, K.ASCLEPEION[3][1], False)
    g.set(AGORA[0] + 1, AGORA[1] + 3, K.AGORA[3][1], False)

    def facade(x, y, rows):
        for j, row in enumerate(rows):
            for i, name in enumerate(row):
                g.piece("house", name, x + i, y + j)
    facade(*AXYLOS, [["R_L", "R_doves", "R_jar", "R_M", "R_R"],
                     ["U_L", "U_window", "U_M", "U_vine", "U_R"],
                     ["G_L", "pot_basil", "door_white", "G_bench", "G_R"]])
    g.block(K.FARMHOUSE, NIKARETE[0], NIKARETE[1] - 1)          # door (16,15)
    g.set(NIKARETE[0] + 1, NIKARETE[1] + 2, K.FARMHOUSE[3][1], False)
    facade(*PERFUMER, [["R_L", "R_chimney", "R_R"],
                       ["U_L", "U_window_pink", "U_R"],
                       ["G_L", "door", "G_R"]])
    facade(*DIVERS, [["R_L", "R_jar", "R_R"],
                     ["U_L", "U_window", "U_R"],
                     ["G_steps", "door_white", "G_R"]])
    facade(*PHEREKLOS, [["R_L", "R_M", "R_chimney", "R_dove", "R_R"],
                        ["U_L", "U_niche", "U_M", "U_window", "U_R"],
                        ["G_L", "G_bench", "door_white", "G_shell", "G_R"]])

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
    # (clipped runs broken by single bushes and wild roses, so no hedge reads
    # as a ruler line)
    kind = {}
    for y, row in enumerate(PLAN):
        for x, c in enumerate(row):
            if c == "h":
                r = K.hashed(x, y, 51)
                kind[(x, y)] = "briar" if r < 0.18 else "bush" if r < 0.36 else "run"
    for (x, y), k in kind.items():
        if k == "briar":
            g.piece("flowers", "briar", x, y)
        elif k == "bush":
            g.piece("myrtle", "bush", x, y)
        else:
            left = kind.get((x - 1, y)) == "run"
            right = kind.get((x + 1, y)) == "run"
            g.piece("myrtle", "M" if left and right else "L" if right else "R" if left else "single", x, y)

    # a gap in the promenade's hedge where a path of thrift runs into the
    # garden, so the hedge never runs as one ruler line (STYLE §4.2)
    g.piece("flowers", "thrift", 19, 12)

    # Nikarete's tiled roof sits where the hedge line runs
    g.block(K.FARMHOUSE, NIKARETE[0], NIKARETE[1] - 1)
    g.set(NIKARETE[0] + 1, NIKARETE[1] + 2, K.FARMHOUSE[3][1], False)

    # ---- the quay's paving: dressed flags wherever the harbor is stone, so the
    # quay reads at a glance; the town's lanes stay limestone path
    for y in range(9, 26):
        for x in range(13, 31):
            if PLAN[y][x] not in "pB" or g.get(x, y) not in (K.PATH["c"],) + tuple(K.PATH.values()):
                continue
            if x < 20 and y > 11:
                continue                          # the main street and the town
            r = K.hashed(x, y, 31)
            name = "A" if r < 0.36 else "B" if r < 0.7 else "C"
            if g.get(x - 1, y) == g.m("flags", name):
                name = {"A": "B", "B": "C", "C": "A"}[name]
            if x == 30 and (y in RECESS or y in (RECESS[0] - 1, RECESS[-1] + 1)):
                continue
            if x == 30 and y % 5 == 1:
                name = "ring"
            elif K.hashed(x, y, 33) < 0.05:
                name = "drain" if y % 2 else "worn"
            g.piece("flags", name, x, y)

    # ---- the harbor at work. The requisition: oars, crates and amphorae stacked
    # either side of the Euploia's plank, a Titanborn on guard, the requisitioned
    # hulls moored along the quay's south face. Bollards down the edge, nets
    # drying where the old sailor mends them, a fish corner by the Agora with
    # nothing to sell, and Aphrodite's shrine at the end.
    for (x, y, name) in ((19, 10, "oars"), (20, 10, "oars"), (21, 10, "crate"), (22, 10, "amphorae"),
                         (23, 10, "rope"), (27, 10, "crate"), (28, 10, "bollard"), (29, 10, "amphorae"),
                         (30, 10, "oars"), (29, 12, "amphorae"), (30, 12, "crate"),
                         (15, 10, "oars"), (12, 11, "rope"), (11, 11, "amphorae"),
                         (30, 13, "bollard"), (29, 16, "bollard"), (29, 22, "bollard"),
                         (29, 15, "nets"), (27, 19, "nets"), (27, 20, "nets"), (29, 19, "rope"),
                         (25, 21, "crate"), (27, 22, "crate"), (26, 22, "crate"), (25, 23, "amphorae"),
                         (28, 24, "rope"), (26, 16, "rope"), (27, 17, "amphorae"), (28, 17, "crate")):
        g.piece("gear", name, x, y)
    g.put("shrine", 30, 24)                       # Aphrodite of the Harbor
    for x in (21, 25, 29):
        g.put("kaiki", x, 27, cx=0, w=3, h=2)    # requisitioned, waiting for their oars

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
    g.set(24, 11, K.STELE, True)                 # SKANDEIA

    # ---- the pocket beach: shells and wrack; tide rocks off the quay
    for (x, y, n) in ((13, 25, "shells"), (16, 26, "scallop"), (18, 25, "wrack")):
        g.piece("sand_decor", n, x, y)
    for (x, y) in ((25, 3), (26, 3), (26, 4), (34, 24), (35, 24), (35, 25), (37, 13), (38, 13)):
        g.set(x, y, K.SEA_ROCK, True)

    # ---- the north bay's beach: sand under the woods, aethos's own surf edge
    # (these rows are the Route 24 seam's aethos-only strip)
    for y in range(0, 6):
        g.set(21, y, K.SAND)
        g.set(22, y, 0x125)                      # aethos beach, sea to the east
    # a sandy point pushes out at rows 2-3 (aethos's island kit: outer corners
    # 11D/12D, the notches 13D/146 where it leaves the straight shore)
    g.set(22, 2, 0x13D)
    g.set(22, 3, 0x146)
    g.set(23, 2, 0x11D)
    g.set(23, 3, 0x12D)

    # ---- greenery: wild olive woods on the slopes above the town, staggered,
    # with glades, pines and cypresses; myrtle and briar where the tileset may go
    def shrub(x, y):
        if x >= 8 and y >= 6:
            g.piece("myrtle" if K.hashed(x, y, 41) < 0.6 else "flowers",
                    ("bush" if K.hashed(x, y, 43) < 0.5 else "single") if K.hashed(x, y, 41) < 0.6 else "briar",
                    x, y)
    trees = [(x, y) for y, row in enumerate(PLAN) for x, c in enumerate(row) if c == "T"]
    g.woods(trees, seed=11, pines=0.25, cypresses=0.7, shrubs=shrub, skip=0.16)
    # the little garden between Axylos's and Nikarete's: myrtle, a rose, thrift
    g.piece("myrtle", "L", 13, 13)
    g.piece("myrtle", "R", 14, 13)
    g.piece("flowers", "thrift", 13, 14)
    g.piece("myrtle", "single", 14, 14)
    g.piece("flowers", "briar", 13, 15)
    g.piece("myrtle", "bush", 14, 15)
    g.cypress(18, 13)
    g.piece("flowers", "briar", 18, 15)
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
        # the pocket beach's far corner, under the olives
        item_ball(12, 27, "ITEM_SEA_INCENSE", "FLAG_ICHOR_ITEM_SKANDEIA_SEA_INCENSE"),
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
        # a sailor's thanks lost in the niche among the shells, and something
        # the tide left at the foot of the boat's slip
        hidden(30, 24, "ITEM_BIG_PEARL", "FLAG_ICHOR_HIDDEN_ITEM_SKANDEIA_BIG_PEARL"),
        hidden(SLIPS, 8, "ITEM_HEART_SCALE", "FLAG_ICHOR_HIDDEN_ITEM_SKANDEIA_HEART_SCALE"),
        sign(5, 15, P + "SignFoamRoad"),
        sign(24, 11, P + "SignSkandeia"),
        sign(17, 19, P + "Spout", "south"),
    ]
    coords = [trigger(STREET_HEAD, y, P + "AletheaRejoins", "VAR_TEMP_1", 1) for y in (16, 17)]
    coords += [trigger(x, 13, P + "KronistPreaches", "VAR_TEMP_2", 1) for x in range(25, 30)]
    spec = K.Spec(NAME, g, music="MUS_ICHOR_AKTI", mapsec="MAPSEC_KYTHERA_ISLE", map_type="MAP_TYPE_TOWN",
                  border=[K.SEA] * 4, objects=objects, warps=warps, bgs=bgs, coords=coords,
                  start=GANGPLANK,
                  seams={"west": 8, "east": 8, "north": 6},
                  connections=
                  [("right", "MAP_ROUTE22_MYRTOAN_SEA", -15), ("right", "MAP_ROUTE23_CRETAN_SEA", 15),
                   ("left", "MAP_KYTHERA_FOAM_ROAD", 7)],
                  screens={"1_gangplank": GANGPLANK, "2_slips": (13, 9), "3_quay": (28, 16),
                           "4_street_head": (20, 17), "5_street": (12, 17), "6_gate": (4, 16),
                           "7_lower_lane": (13, 23), "8_shrine": (27, 24), "9_agora": (23, 23)})
    return [spec]
