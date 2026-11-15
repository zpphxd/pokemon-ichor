"""MAP_MELOS: Klima, the fishing hamlet on Melos's great round bay (SCRIPT.md
Part 2, "Melos"; beats III-1B2 and the statue's rite, Part 5).

Klima stands on a blunt promontory into the bay, so the sea wraps it on three
sides and Route 22's two sea maps join it east and west across open water. From
the waterline up: the bay; the jetty where the Euploia's boat lands and FISHER
Kimolos fishes off the end; the boathouse with its red, blue and green sea doors
(Myrtis and Kalchedon live over their boat); the lane with the well; Kentrios's
farmhouse and Melanippos's workshop; terrace wall B and its stair (Kentrios's
warning); the middle terrace, where the armless goddess stands in her niche in
wall A with the old bronze mirror propped facing her across the path; wall A's
stair at the east end; the barley band, 3 deep, the only way up; TITANBORN
Theion at the top of it, watching wall C's stair; and above, the obsidian slope
with its knapping pits and the seam. The crest is pine and olive. A path runs
west along the shore to the white pumice cliffs, a dead end with a Star Piece
on the lip.

Seams: Melos and Route 22's maps all use gTileset_Melos, so their shared seams
are exempt from the aethos-only strip (MAP_DESIGN.md §5). The sea maps draw
Melos's coast near the seam from COAST_WEST and COAST_EAST below.
"""
import kythera_outdoor as K
from kythera_outdoor import obj, item_ball, sign, trigger, warp

NAME = "Melos"
P = "Melos_EventScript_"
W, H = 32, 34

# ~ sea  s sand  g grass  f flowers  , tall grass (the barley)  o obsidian
# p limestone path  T woods  B a building's footprint  k pumice (placed in code)
# Rows 8-9, 14-15 and 18-19 are terrace walls C, A and B, laid in code.
PLAN = [
    "T" * 32,                                       # 0  the crest
    "T" * 32,                                       # 1
    "T" * 32,                                       # 2
    "T" * 32,                                       # 3
    "TTTTTTTggooooooggoooooooooggTTTT",             # 4  the obsidian slope
    "TTTTTggooooooooooooooooooooogTTT",             # 5
    "TTTTggoooooooooooooooooooooogTTT",             # 6
    "TTTTTgggooooooooooooooooooogTTTT",             # 7
    "TTTTTggggggggggggggggggggggggTTT",             # 8  wall C's top
    "TTTTTggggggggggggggggggggggggTTT",             # 9  wall C, stair at 15-16
    "TTTTggggggggggggggggggggggggggTT",             # 10 the strip under the slope
    "TTTT" + "," * 25 + "TTT",                     # 11 the barley band
    "TTT" + "," * 26 + "TTT",                      # 12
    "TTTT" + "," * 26 + "TT",                      # 13
    "TTTggggggggggggggggggggggggggggT",             # 14 wall A's top
    "TTTggggggggggggggggggggggggggggT",             # 15 wall A: the niche at 20, stair at 27
]


def R(*segs):
    row = "".join(c * n for c, n in segs)
    assert len(row) == 32, (row, len(row))
    return row


PLAN += [
    R(("T", 2), ("g", 1), ("t", 6), ("g", 5), ("f", 1), ("g", 11), ("f", 1), ("g", 3), ("T", 2)),  # 16 the middle terrace:
    R(("T", 2), ("g", 1), ("t", 6), ("g", 8), ("f", 1), ("g", 12), ("T", 2)),            # 17 Kentrios's field
    R(("T", 2), ("g", 28), ("T", 2)),                                              # 18 wall B's top: the mirror
    R(("T", 2), ("g", 7), ("B", 3), ("g", 18), ("T", 2)),                          # 19 wall B; the farmhouse
    R(("T", 2), ("g", 7), ("B", 3), ("g", 5), ("B", 3), ("g", 8), ("T", 4)),       # 20 the houses
    R(("T", 2), ("g", 6), ("f", 1), ("B", 3), ("g", 1), ("f", 1), ("g", 3), ("B", 3), ("g", 8),
      ("s", 1), ("T", 2), ("~", 1)),                                               # 21
    R(("g", 8), ("f", 1), ("B", 3), ("g", 4), ("f", 1), ("B", 3), ("g", 6), ("s", 3), ("~", 3)),  # 22 the lip
    R(("k", 7), ("p", 16), ("g", 2), ("s", 3), ("~", 4)),                          # 23 the lane
    R(("k", 7), ("g", 6), ("B", 7), ("g", 5), ("s", 3), ("~", 4)),                 # 24 the boathouse
    R(("~", 7), ("s", 6), ("B", 7), ("s", 6), ("~", 6)),                           # 25 (the pumice's foot)
    R(("~", 8), ("s", 5), ("B", 7), ("s", 1), ("q", 4), ("~", 7)),                 # 26 the jetty
    R(("~", 9), ("s", 4), ("B", 7), ("~", 1), ("q", 4), ("~", 7)),                 # 27 the slips
    R(("~", 21), ("q", 4), ("~", 7)),                                              # 28
    R(("~", 21), ("q", 4), ("~", 7)),                                              # 29 the jetty's end
    R(("~", 32)), R(("~", 32)), R(("~", 32)), R(("~", 32)),                       # 30-33 the bay
]
assert len(PLAN) == H

# Melos's coast at each edge, for the sea maps: the first sea row at x = 0 / 31.
COAST_WEST, COAST_EAST = 25, 21

LEGEND = {"~": "sea", "s": "sand", "g": "grass", "f": "flowers", ",": "tall", "p": "path", "t": "tilled",
          "o": "grass", "T": "grass", "B": "grass", "k": "grass", "q": "sea"}

FARM = (9, 19)          # the aethos farmhouse, 3x4, door at (10,22)
KNAPPER = (17, 20)      # a melos cube house, 3x3, door at (18,22)
BOATHOUSE = (13, 24)    # 7x4: the land door at (13,26)
JETTY = (21, 26)        # 4 wide: walkable x = 22-23, rows 26-29
NICHE = (20, 15)
MIRROR = (20, 18)
STAIR_C = (15, 16)      # wall C's stair columns, row 9
STAIR_A = 27            # wall A's stair column, row 15
STAIR_B = 13            # wall B's stair column, row 19
THEION = (14, 10)


def terrace(g, y_top, x0, x1, steps=(), niche=None, skip=()):
    """A melos tuff terrace wall: the upper level's top row at y_top, the wall
    one cell high below it, from x0 to x1, with stairs and a niche."""
    for x in range(x0, x1 + 1):
        if x in skip:
            continue
        if x in steps:
            g.piece("village", "top_steps", x, y_top)
            g.piece("village", "wall_steps", x, y_top + 1)
        elif x == niche:
            g.piece("village", "top_niche", x, y_top)
            g.piece("village", "niche", x, y_top + 1)
        else:
            top = "top_L" if x == x0 else "top_R" if x == x1 else "top"
            wall = "wall_L" if x == x0 else "wall_R" if x == x1 else "wall"
            g.piece("village", top, x, y_top)
            g.piece("village", wall, x, y_top + 1)


def obsidian(g):
    region = [[c == "o" for c in row] for row in PLAN]
    for y, row in enumerate(PLAN):
        for x, c in enumerate(row):
            if c == "o":
                key = K.blob_key(region, x, y)
                g.set(x, y, g.m("obsidian", key))


def compose():
    g = K.Grid(W, H, "melos")
    K.lay_ground(g, PLAN, LEGEND)
    obsidian(g)

    # ---- the slope's things: pits (the daily digs), the seam, flakes, a core
    for (x, y, name) in ((9, 6, "pit"), (23, 5, "pit_b"), (16, 4, "pit_b"), (12, 5, "flakes"),
                         (20, 7, "flakes"), (25, 6, "core"), (13, 7, "sacks"), (18, 5, "flakes")):
        g.piece("obsidian_bits", name, x, y)

    # ---- the terraces, top down
    terrace(g, 8, 5, 28, steps=STAIR_C)
    terrace(g, 14, 3, 30, steps=(STAIR_A,), niche=NICHE[0])
    terrace(g, 18, 2, 29, steps=(STAIR_B,), skip=range(FARM[0], FARM[0] + 3))
    # Theion's sacks by wall C's stair; vines along the middle terrace's back
    g.piece("obsidian_bits", "sacks", THEION[0] - 1, THEION[1])
    for x in (9, 10, 11):
        g.piece("village", "vine" if x != 11 else "vine_end", x, 16)
    # the barley's ragged ends: a few vines at the band's edges
    for (x, y) in ((4, 11), (3, 12), (29, 13)):
        g.piece("village", "vine_end", x, y)

    # ---- the houses
    g.block(K.FARMHOUSE, FARM[0], FARM[1])
    g.set(FARM[0] + 1, FARM[1] + 3, K.FARMHOUSE[3][1], False)
    g.front("cube", KNAPPER[0], KNAPPER[1])
    g.piece("village", "well", 14, 22)
    g.piece("village", "trough", 15, 22)

    # ---- the boathouse: one long building, the family's land door at its west
    # end, then its three bays of sea doors, red, blue and green
    bx, by = BOATHOUSE
    roof = ["R_L"] + ["R_M"] * 5 + ["R_R"]
    upper = ["U_L", "U_balcony", "U_R", "U_balcony_blue", "U_R", "U_balcony_green", "U_R"]
    ground = ["land_door", "sea_red_L", "sea_red_R", "sea_blue_L", "sea_blue_R", "sea_green_L", "sea_green_R"]
    for i in range(7):
        g.piece("boathouse", roof[i], bx + i, by)
        g.piece("boathouse", upper[i], bx + i, by + 1)
        g.piece("boathouse", ground[i], bx + i, by + 2)
    g.set(bx, by + 3, K.SAND)                                  # the step below the land door
    for i in (1, 3, 5):
        g.piece("boathouse", "slip_L", bx + i, by + 3)
        g.piece("boathouse", "slip_R", bx + i + 1, by + 3)

    # ---- the jetty: aethos paving between the quay kit's edges
    jx, jy = JETTY
    for y in range(jy, jy + 4):
        last = y == jy + 3
        g.piece("quay", "out_SW" if last else "W", jx, y)
        g.set(jx + 1, y, g.m("quay", "steps_S") if last else K.PATH["c"])
        g.set(jx + 2, y, g.m("quay", "steps_S") if last else K.PATH["c"])
        g.piece("quay", "out_SE" if last else "E", jx + 3, y)
    g.put("kaiki", 8, 25, cx=3, w=3, h=2)                      # the Euploia's boat, run up on the shingle
    g.put("kaiki", 26, 27, cx=0, w=3, h=2)                     # Kimolos's boat, moored off the jetty

    # ---- the pumice cliffs at the west end of the shore
    for x in range(0, 7):
        g.piece("pumice", "top_R" if x == 6 else "top", x, 23)
        g.piece("pumice", "hollow" if x == 2 else "mass", x, 24)
        g.piece("pumice", "foot_R" if x == 6 else "foot", x, 25)

    # ---- sea marks: tide rocks off the point and the shore
    for (x, y) in ((4, 29), (28, 25), (30, 30), (10, 31), (17, 30)):
        g.piece("rocks", "tide_rock" if (x + y) % 2 else "tide_rocks", x, y)
    g.set(20, 26, K.STELE, True)                               # KLIMA, MELOS
    g.set(0, 22, K.BOULDER["grass"], True)                     # the lip ends here, short of the seam
    for (x, y, n) in ((11, 26, "shells"), (24, 25, "wrack"), (26, 23, "shells"), (12, 25, "lace")):
        g.piece("sand_decor", n, x, y)

    # ---- greenery: the crest and the flanks
    woods = [(x, y) for y, row in enumerate(PLAN) for x, c in enumerate(row) if c == "T"]
    g.woods(woods, seed=3, pines=0.3, cypresses=0.6)
    for (x, y) in ((2, 20), (6, 19), (12, 20), (21, 19), (26, 20), (24, 17)):
        if g.free(x, y):
            g.set(x, y, K.FLOWERS)
    return g


def specs():
    g = compose()
    bx, by = BOATHOUSE
    objects = [
        obj("ICHOR_SAILOR", 23, 27, "left", P + "Nausikles", "LOCALID_MELOS_NAUSIKLES",
            "FLAG_ICHOR_CROSSED_ROUTE22"),
        obj("ICHOR_FISHER", 23, 29, "down", P + "Kimolos", "LOCALID_MELOS_KIMOLOS", trainer=1),
        obj("ICHOR_KID_F", 14, 23, "up", P + "Girl", "LOCALID_MELOS_GIRL"),
        obj("ICHOR_ELDER_M", 21, 16, "left", P + "Kentrios", "LOCALID_MELOS_KENTRIOS"),
        # The armless goddess turns, rooted, in her niche; the mirror faces her.
        # Placeholder sprites until the art lead draws a marble statue and a
        # bronze mirror on its stand (SCRIPT.md Part 10).
        obj("ICHOR_PRIESTESS", NICHE[0], NICHE[1], "MOVEMENT_TYPE_ICHOR_STATUE_ROOTED", P + "Statue",
            "LOCALID_MELOS_STATUE", solid_ok=True),
        obj("ICHOR_TABLET", MIRROR[0], MIRROR[1], "MOVEMENT_TYPE_ICHOR_MIRROR_UP", P + "Mirror",
            "LOCALID_MELOS_MIRROR"),
        obj("ICHOR_TITAN_GRUNT", THEION[0], THEION[1], "right", P + "Theion", "LOCALID_MELOS_THEION",
            trainer=2),
        item_ball(1, 22, "ITEM_STAR_PIECE", "FLAG_ICHOR_ITEM_MELOS_STAR_PIECE"),
    ]
    warps = [
        warp(FARM[0] + 1, FARM[1] + 3, "MAP_MELOS_FARMHOUSE", 0),
        warp(KNAPPER[0] + 1, KNAPPER[1] + 2, "MAP_MELOS_KNAPPERS_HOUSE", 0),
        warp(bx, by + 2, "MAP_MELOS_BOATHOUSE", 0),
    ]
    bgs = [
        sign(14, 22, P + "Well", "north"), sign(15, 22, P + "Well", "north"),
        sign(3, 23, P + "Pumice", "south"), sign(4, 23, P + "Pumice", "south"),
        sign(9, 6, P + "DigSpot"), sign(23, 5, P + "DigSpot"),
        sign(16, 4, P + "Seam"),
        sign(13, 7, P + "Sacks"),
        sign(20, 26, P + "Sign"),
    ]
    coords = [trigger(STAIR_B, 19, P + "KentriosWarning", "VAR_TEMP_1", 0)]
    spec = K.Spec(NAME, g, music="MUS_ICHOR_ROAD", mapsec="MAPSEC_MELOS", map_type="MAP_TYPE_TOWN",
                  border=[K.SEA] * 4, objects=objects, warps=warps, bgs=bgs, coords=coords,
                  start=(22, 27),
                  connections=[("left", "MAP_ROUTE22_MYRTOAN_SEA", 0), ("right", "MAP_ROUTE22_CRETAN_SEA", 0)],
                  screens={"1_jetty": (22, 27), "2_boathouse": (14, 25), "3_lane": (12, 23),
                           "4_wall_b": (13, 19), "5_statue": (20, 17), "6_band": (24, 12),
                           "7_theion": (16, 10), "8_slope": (15, 6), "9_pumice": (3, 22),
                           "10_east_shore": (26, 22)})
    return [spec]
