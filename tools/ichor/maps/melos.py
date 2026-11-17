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
on the lip past a clifftop meadow of wild grass (a Pearl hides in the pumice
hollow, reached by sea). Wild grass fills the corner under wall B's east step
too, a Revive at its back; Black Glasses wait at the slope's east end, past
Theion; an Ultra Ball hides under the jetty's last stone, and a Heart Scale
at the niche's foot once the goddess has had her offering.

Seams: Melos and Route 22's maps all use gTileset_Melos, so their shared seams
are exempt from the aethos-only strip (MAP_DESIGN.md §5). The sea maps draw
Melos's coast near the seam from COAST_WEST and COAST_EAST below.
"""
import kythera_outdoor as K
from kythera_outdoor import obj, item_ball, sign, trigger, warp, hidden

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
    "TTTTTTTggoooooooooooooooooggTTTT",             # 4  the obsidian slope
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
    R(("T", 2), ("g", 1), ("t", 6), ("g", 9), ("f", 2), ("g", 1), ("f", 2), ("g", 7), ("T", 2)),  # 16 the middle terrace:
    R(("T", 2), ("g", 1), ("t", 6), ("g", 21), ("T", 2)),                         # 17 Kentrios's field
    R(("T", 2), ("g", 28), ("T", 2)),                                              # 18 wall B's top: the mirror
    R(("T", 2), ("g", 7), ("B", 3), ("g", 18), ("T", 2)),                          # 19 wall B; the farmhouse
    # 20-22: the houses; west, the clifftop meadow before the pumice (the Star
    # Piece past it); east, wild grass in the corner under wall B's step (a
    # Revive at its back)
    R(("T", 2), ("g", 7), ("B", 3), ("g", 5), ("B", 3), ("g", 1), (",", 2), ("g", 5), ("T", 4)),  # 20
    R(("T", 2), (",", 1), ("g", 2), (",", 2), ("g", 1), ("f", 1), ("B", 3), ("g", 1), ("f", 1), ("g", 3),
      ("B", 3), ("g", 1), (",", 6), ("g", 1), ("s", 1), ("T", 2), ("~", 1)),       # 21
    R(("g", 2), (",", 5), ("g", 1), ("f", 1), ("B", 3), ("g", 4), ("f", 1), ("B", 3), ("g", 2), (",", 3),
      ("g", 1), ("s", 3), ("~", 3)),                                               # 22 the lip
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
SEAM = (16, 5)          # the slope's fixed find, where the long vein runs in


def terrace(g, y_top, x0, x1, steps=(), niche=None, skip=(), rise=None):
    """A melos tuff terrace wall: the upper level's top row at y_top, the wall
    one cell high below it, from x0 to x1, with stairs and a niche. `rise`
    maps x to a row offset, so the wall steps up or down a row and follows the
    hill instead of a ruler line: a step between two columns is sealed by the
    walls themselves (the lower run's wall meets the higher run's), and each run
    ends in its own corner stones."""
    rise = rise or (lambda x: 0)
    cols = [x for x in range(x0, x1 + 1) if x not in skip]
    for x in cols:
        y = y_top + rise(x)
        left_end = x == x0 or (x - 1 in skip) or rise(x - 1) != rise(x)
        right_end = x == x1 or (x + 1 in skip) or rise(x + 1) != rise(x)
        if x in steps:
            g.piece("village", "top_steps", x, y)
            g.piece("village", "wall_steps", x, y + 1)
        elif x == niche:
            g.piece("village", "top_niche", x, y)
            g.piece("village", "niche", x, y + 1)
        else:
            g.piece("village", "top_L" if left_end else "top_R" if right_end else "top", x, y)
            g.piece("village", "wall_L" if left_end else "wall_R" if right_end else "wall", x, y + 1)


def veins(g):
    """Black glass veins through the scree, and the knappers' spoil heaps.
    Each chain runs end_E, then joints, then end_W (the pieces name the sides
    they join); only cells deep inside the slope take a vein."""
    region = [[c == "o" for c in row] for row in PLAN]
    chains = [
        [(17, 5, "end_E"), (18, 5, "WE"), (19, 5, "SW"), (19, 6, "NE"), (20, 6, "WE"), (21, 6, "end_W")],
        [(10, 5, "end_E"), (11, 5, "SW"), (11, 6, "NE"), (12, 6, "end_W")],
        [(23, 6, "end_E"), (24, 6, "NW"), (24, 5, "SE"), (25, 5, "end_W")],
    ]
    for chain in chains:
        for (x, y, name) in chain:
            if K.blob_key(region, x, y) == "1|11111111":
                g.piece("obsidian_veins", name, x, y)
    for (x, y, name) in ((8, 6, "spoil"), (22, 5, "spoil"), (14, 6, "lens"), (26, 6, "lens"),
                         (15, 5, "spoil")):
        if K.blob_key(region, x, y) == "1|11111111":
            g.piece("obsidian_veins", name, x, y)


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

    # ---- the slope's things: pits (the daily digs), the seam, a core, Theion's
    # sacks, and the veins of glass with the knappers' spoil heaps
    veins(g)
    for (x, y, name) in ((9, 6, "pit"), (23, 5, "pit_b"), SEAM + ("pit_b",), (20, 7, "flakes"),
                         (6, 6, "flakes"), (25, 6, "core"), (13, 7, "sacks")):
        g.piece("obsidian_bits", name, x, y)

    # ---- the terraces, top down. Each wall follows the hill, stepping a row up
    # or down along its length, and each terrace grows its own crop: barley on
    # the upper, Kentrios's field and vines on the middle, gardens below.
    terrace(g, 8, 5, 28, steps=STAIR_C,
            rise=lambda x: 1 if x <= 8 else -1 if 20 <= x <= 24 else 0)
    terrace(g, 14, 3, 30, steps=(STAIR_A,), niche=NICHE[0],
            rise=lambda x: -1 if 9 <= x <= 13 else 1 if x >= 24 else 0)
    terrace(g, 18, 2, 29, steps=(STAIR_B,), skip=range(FARM[0], FARM[0] + 3),
            rise=lambda x: 1 if x >= 24 else 0)
    # Theion's sacks by wall C's stair
    g.piece("obsidian_bits", "sacks", THEION[0] - 1, THEION[1])
    # vines on the middle terrace: a trellis by the field, and a row on the east
    # step where the terrace widens (row 17 stays open for the path)
    for x in (9, 10, 11):
        g.piece("village", "vine" if x != 11 else "vine_end", x, 16)
    for x in (23, 24, 25):
        g.piece("village", "vine" if x != 25 else "vine_end", x, 18)
    # the barley's ragged ends: vines at the band's edges
    for (x, y) in ((4, 11), (3, 12), (29, 13), (28, 11)):
        g.piece("village", "vine_end", x, y)
    # a kitchen garden below the farmhouse's terrace
    for (x, y, k) in ((3, 20, "tl"), (4, 20, "tr"), (3, 21, "bl"), (4, 21, "br")):
        g.set(x, y, K.TILLED[k])

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
    # two skerries, off the pumice point and off the east shore (STYLE §4.2)
    for (x, y) in ((3, 28), (4, 28), (4, 29), (29, 30), (30, 30), (30, 31)):
        g.piece("rocks", "tide_rock" if (x + y) % 2 else "tide_rocks", x, y)
    g.set(20, 26, K.STELE, True)                               # KLIMA, MELOS
    g.set(0, 22, K.BOULDER["grass"], True)                     # the lip ends here, short of the seam
    for (x, y, n) in ((11, 26, "shells"), (24, 25, "wrack"), (26, 23, "shells"), (12, 25, "lace")):
        g.piece("sand_decor", n, x, y)

    # ---- greenery: the crest and the flanks
    woods = [(x, y) for y, row in enumerate(PLAN) for x, c in enumerate(row) if c == "T"]
    def shrub(x, y):
        # wild roses and lichened rocks between the trees
        if K.hashed(x, y, 17) < 0.6:
            g.piece("flowers", "briar", x, y)
        else:
            g.piece("rocks", "rock_grass", x, y)
    g.woods(woods, seed=3, pines=0.3, cypresses=0.7, skip=0.15, shrubs=shrub)
    # flowers grow in beds: by the farmhouse's and the knapper's doors (the
    # plan's f cells) and either side of the goddess's niche, Kentrios's offering
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
        # past Theion, where the slope runs out under the pines
        item_ball(28, 5, "ITEM_BLACK_GLASSES", "FLAG_ICHOR_ITEM_MELOS_BLACK_GLASSES"),
        # at the back of the wild grass under wall B's east step
        item_ball(23, 20, "ITEM_REVIVE", "FLAG_ICHOR_ITEM_MELOS_REVIVE"),
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
        sign(*SEAM, P + "Seam"),
        sign(13, 7, P + "Sacks"),
        sign(20, 26, P + "Sign"),
        # the niche's foot, beside the goddess: a Heart Scale once she's had
        # her offering (scripted, so it waits for the rite)
        sign(NICHE[0] - 1, NICHE[1], P + "NicheFoot", "north"),
        hidden(21, 29, "ITEM_ULTRA_BALL", "FLAG_ICHOR_HIDDEN_ITEM_MELOS_ULTRA_BALL"),   # the jetty's last stone
        hidden(2, 24, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_ITEM_MELOS_PEARL"),              # the pumice hollow, by sea
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
