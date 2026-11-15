"""Route 22's two sea maps and Route 23's western stretch (SCRIPT.md Part 2),
all optional, by Surf (Poseidon's Conch); the story crosses them on the
Euploia's deck.

  MAP_ROUTE22_CRETAN_SEA   80x30  Kaldera (east, Act II's) to Melos (west)
  MAP_ROUTE22_MYRTOAN_SEA  80x30  Melos (east) to Skandeia's east bay, north half (west)
  MAP_ROUTE23_CRETAN_SEA   60x40  Skandeia's east bay, south half (west) to the open
                                  lane along Knossa's coast (east): Antikythera

Each is open sea broken into lanes by lines of tide rocks, with the trireme
lane's stakes down the middle, a landmark, its trainers and a reward.
Melos's coast runs on into the Route 22 maps beside it (melos.COAST_*).

Seams: the three share gTileset_Melos with Melos, so those seams are exempt.
Skandeia (gTileset_Skandeia), Kaldera and the Knossa coast are other
tilesets, so the 8 columns nearest those seams use only aethos metatiles.
"""
import kythera_outdoor as K
from kythera_outdoor import obj, item_ball, sign

ROCK2 = {  # aethos 2x2 sea stacks: General's ocean rocks, solid
    "block": ((0x166, 0x167), (0x16E, 0x16F)),
    "big": ((0x172, 0x173), (0x17A, 0x17B)),
    "peak": ((0x174, 0x175), (0x17C, 0x17D)),
}


class Sea:
    def __init__(self, w, h, aethos_cols=()):
        self.w, self.h = w, h
        self.plan = [["~"] * w for _ in range(h)]
        self.aethos_cols = set(aethos_cols)

    def land(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.plan[y][x] = c

    def grid(self, legend):
        g = K.Grid(self.w, self.h, "melos")
        K.lay_ground(g, ["".join(r) for r in self.plan], legend)
        return g


def rock2(g, x, y, kind):
    g.block(ROCK2[kind], x, y, solid=True)


def tide(g, x, y, k=0):
    """A tide rock: melos's foam-collared rock, or aethos's in the seam strips."""
    if getattr(g, "aethos_cols", None) and x in g.aethos_cols:
        g.set(x, y, K.SEA_ROCK, True)
    else:
        g.piece("rocks", "tide_rocks" if k % 3 == 0 else "tide_rock", x, y)


def rock_line(g, y, x0, x1, gaps=(), wobble=0, seed=0):
    """A lane-breaking line of tide rocks along row y, with gaps (x ranges)."""
    for x in range(x0, x1 + 1):
        if any(a <= x <= b for a, b in gaps):
            continue
        dy = 0
        if wobble and K.hashed(x, y, seed) < 0.3:
            dy = 1 if K.hashed(x, y, seed + 1) < 0.5 else -1
        tide(g, x, y + dy, x + y)


def stakes(g, y, xs):
    for i, x in enumerate(xs):
        g.piece("rocks", "stakes" if i % 2 else "stake", x, y)


LEGEND = {"~": "sea", "s": "sand", "g": "grass", ",": "tall", "T": "grass", "r": "sea"}


# ===========================================================================
# Route 22, the Cretan Sea: Kaldera to Melos
# ===========================================================================

def cretan():
    W, H = 80, 30
    s = Sea(W, H)
    # Melos's eastern arm runs on from Melos's east edge, receding north-east
    # (a curving shore: a sandy cove, then a rocky point)
    coasts = [20, 20, 19, 19, 18, 18, 18, 17, 15, 14, 14, 13, 11, 10, 9, 9, 7, 5, 4, 2, 1]
    for x, coast in enumerate(coasts):
        sand = 1 if x in (11, 12, 16, 17, 18) else 2
        for y in range(0, coast + 1):
            s.land(x, y, "s" if y > coast - sand and x > 0 else "T")
    # Anydros: a bare rock, its one sandy ledge
    for (x, y) in ((49, 10), (49, 11), (48, 11)):
        s.land(x, y, "s")
    g = s.grid(LEGEND)
    g.aethos_cols = set(range(72, 80))
    g.put("sea_marks", 47, 9, cx=0, w=2)                     # anydros, its dead fig
    # the ring of reef round Anydros, open only to the south, where Antalkidas rows
    ring = [(44, 8), (45, 7), (46, 6), (47, 6), (48, 6), (49, 6), (50, 7), (51, 8), (52, 9), (52, 10),
            (52, 11), (51, 12), (50, 13), (49, 14), (46, 14), (45, 13), (44, 12), (43, 11), (43, 10),
            (43, 9)]
    for i, (x, y) in enumerate(ring):
        tide(g, x, y, i)
    g.put("kaiki", 50, 15, cx=0, w=3, h=2)                   # Antalkidas's boat
    # lanes
    rock_line(g, 4, 24, 70, gaps=((31, 33), (52, 55), (64, 66)), wobble=1, seed=2)
    rock_line(g, 25, 22, 71, gaps=((27, 29), (40, 43), (58, 60)), wobble=1, seed=4)
    for (x, y, k) in ((30, 10, "big"), (60, 20, "block"), (36, 21, "block"), (66, 9, "big")):
        rock2(g, x, y, k)
    stakes(g, 19, [24, 30, 36, 42, 54, 60, 66])
    for (x, y) in ((25, 13), (57, 27), (69, 16)):
        tide(g, x, y, x)                                     # (a drum under the shallows reads as a square glitch at sea)
    for (x, y) in ((74, 5), (77, 21), (75, 12)):
        g.set(x, y, K.SEA_ROCK, True)
    woods = [(x, y) for y, row in enumerate(s.plan) for x, c in enumerate(row) if c == "T"]
    g.woods(woods, seed=21, pines=0.3, cypresses=0.5)
    g.piece("rocks", "stake", 22, 23)                         # the route's sign at the Melos end
    g.piece("rocks", "stake", 70, 27)                         # and at the Kaldera end

    P = "Route22_CretanSea_EventScript_"
    objects = [
        obj("ICHOR_DIVER", 67, 13, "left", P + "Kymaios", "LOCALID_R22C_KYMAIOS", trainer=4),
        obj("ICHOR_SAILOR", 50, 15, "left", P + "Antalkidas", "LOCALID_R22C_ANTALKIDAS", trainer=3,
            solid_ok=True),
        item_ball(49, 10, "ITEM_MAX_ETHER", "FLAG_ICHOR_ITEM_ROUTE22_MAX_ETHER"),
    ]
    bgs = [sign(22, 23, P + "SignMelos"), sign(70, 27, P + "SignKaldera"),
           sign(47, 10, P + "Anydros"), sign(48, 10, P + "Anydros")]
    return K.Spec("Route22_CretanSea", g, music="MUS_ICHOR_ROAD", mapsec="MAPSEC_AETHOS_ROUTE_22",
                  map_type="MAP_TYPE_OCEAN_ROUTE", border=[K.SEA] * 4, objects=objects, bgs=bgs,
                  start=(30, 22), seams={"east": 8}, allow_cycling=False,
                  connections=[("left", "MAP_MELOS", 0)],
                  screens={"1_melos_end": (6, 24), "2_anydros": (48, 13), "3_kymaios": (64, 13),
                           "4_kaldera_end": (72, 20)})


# ===========================================================================
# Route 22, the Myrtoan Sea: Melos to Skandeia, under Cape Malea
# ===========================================================================

def myrtoan():
    W, H = 80, 30
    s = Sea(W, H)
    # Melos's western shore: woods behind a rocky edge, and its pumice cliffs
    for x in range(74, 80):
        for y in range(0, 23):
            s.land(x, y, "T")
    g = s.grid(LEGEND)
    g.aethos_cols = set(range(0, 8))
    # its rocky west shore: sea stacks hugging the woods, tide rocks between
    for y in range(0, 22, 2):
        if K.hashed(73, y, 3) < 0.6:
            rock2(g, 72, y, "big" if (y // 2) % 3 else "block")
        else:
            tide(g, 73, y, y)
            tide(g, 73, y + 1, y + 1)
    tide(g, 73, 22, 1)
    for x in range(72, 80):
        g.piece("pumice", "top_L" if x == 72 else "top", x, 23)
        g.piece("pumice", "mass", x, 24)
        g.piece("pumice", "foot_L" if x == 72 else "foot", x, 25)
    # Cape Malea's gray cliffs along the north edge, and the surf the player can't cross
    # (whole sea stacks on a 2-cell grid, the second row offset by one, so no
    # stack is ever cut in half)
    for i, x in enumerate(range(4, 62, 2)):
        rock2(g, x, 0, "big" if K.hashed(x, 0, 5) < 0.6 else "block")
        if x + 1 < 62:
            rock2(g, x + 1, 2, "block" if K.hashed(x, 2, 7) < 0.55 else "big")
    for x in range(4, 64):
        tide(g, x, 4, x)
    # lanes
    rock_line(g, 11, 10, 66, gaps=((18, 20), (39, 41), (57, 59)), wobble=1, seed=6)
    rock_line(g, 22, 12, 64, gaps=((20, 22), (44, 46)), wobble=1, seed=8)
    stakes(g, 17, [10, 16, 22, 28, 34, 46, 52, 58, 64, 70])
    g.piece("rocks", "sunken_column", 55, 25)                 # a whole temple under the sea, and this
    for (x, y) in ((30, 26), (62, 8), (45, 7)):
        tide(g, x, y, x)                                     # (a drum under the shallows reads as a square glitch at sea)
    for (x, y) in ((3, 9), (5, 21), (2, 26)):
        g.set(x, y, K.SEA_ROCK, True)
    rock2(g, 26, 14, "big")
    g.piece("rocks", "rock_sand", 38, 14)                     # Nikandros's fishing rock
    woods = [(x, y) for y, row in enumerate(s.plan) for x, c in enumerate(row) if c == "T"]
    g.woods(woods, seed=23, pines=0.3, cypresses=0.5)
    g.piece("rocks", "stake", 12, 6)                          # CAPE MALEA
    g.piece("rocks", "stake", 68, 27)                         # ROUTE 22, at the Melos end

    P = "Route22_MyrtoanSea_EventScript_"
    objects = [
        obj("ICHOR_FISHER", 38, 14, "down", P + "Nikandros", "LOCALID_R22M_NIKANDROS", trainer=3,
            solid_ok=True),
        obj("ICHOR_DIVER", 54, 25, "right", P + "Hagne", "LOCALID_R22M_HAGNE", trainer=1),
    ]
    bgs = [sign(12, 6, P + "SignMalea"), sign(68, 27, P + "SignMelos"),
           sign(55, 25, P + "SunkenColumn")]
    return K.Spec("Route22_MyrtoanSea", g, music="MUS_ICHOR_ROAD", mapsec="MAPSEC_AETHOS_ROUTE_22",
                  map_type="MAP_TYPE_OCEAN_ROUTE", border=[K.SEA] * 4, objects=objects, bgs=bgs,
                  start=(40, 18), seams={"west": 8}, allow_cycling=False,
                  connections=[("left", "MAP_KYTHERA_SKANDEIA", 15), ("right", "MAP_MELOS", 0)],
                  screens={"1_skandeia_end": (6, 22), "2_malea": (12, 8), "3_nikandros": (38, 16),
                           "4_hagne": (55, 23), "5_melos_end": (70, 26)})


# ===========================================================================
# Route 23, the Cretan Sea: Skandeia to Antikythera and on toward Knossa
# ===========================================================================

def route23():
    W, H = 60, 40
    s = Sea(W, H)
    # two sandbars, and Antikythera: a beach round a patch of grass, its reef south-east
    for x in range(12, 17):
        s.land(x, 6, "s")
    for x in range(13, 16):
        s.land(x, 7, "s")
    for x in range(33, 38):
        s.land(x, 19, "s")
    for x in range(34, 37):
        s.land(x, 20, "s")
    islet = [
        (26, "  ssssss     "),
        (27, " ssgg,,ss    "),
        (28, "ssg,,,,,gs   "),
        (29, "sgg,,,,,ggs  "),
        (30, "sgg,,,ggggs  "),
        (31, " sgggggggs   "),
        (32, "  sssssss    "),
    ]
    for (y, row) in islet:
        for i, c in enumerate(row):
            if c != " ":
                s.land(36 + i, y, c)
    g = s.grid(LEGEND)
    g.aethos_cols = set(range(0, 8)) | set(range(52, 60))
    # the islet's few trees
    g.cypress(39, 27) if g.free(39, 27, 1, 2) else None
    g.set(45, 29, K.BOULDER["grass"], True)
    # the reef: turquoise shallows at low water, walkable, ringed by tide rocks,
    # and the wreck's ribs on it
    reef_rows = {32: (44, 47), 33: (43, 49), 34: (42, 49), 35: (42, 49), 36: (43, 47)}
    reef = [(x, y) for y, (a, b) in reef_rows.items() for x in range(a, b + 1)]
    for (x, y) in reef:
        if g.get(x, y) == K.SEA or (g.get(x, y) or 0) >= 0x200:
            g.set(x, y, 0x0D1)
    g.put("sea_marks", 45, 34, cx=2, w=3)                     # the wreck
    for (i, (x, y)) in enumerate(((41, 33), (41, 35), (41, 36), (44, 37), (48, 37), (50, 35), (50, 33),
                                  (49, 31), (42, 37))):
        tide(g, x, y, i)
    for (x, y) in ((40, 35), (51, 34), (46, 38)):
        tide(g, x, y, x)                                     # (a drum under the shallows reads as a square glitch at sea)
    # the reef line that closes the islet's lane; Euthykles rows its gap
    for y in range(0, H):
        if 11 <= y <= 13:
            continue
        x = 26 + (1 if K.hashed(26, y, 9) < 0.25 else 0) - (1 if K.hashed(26, y, 10) < 0.2 else 0)
        tide(g, x, y, y)
    g.put("kaiki", 27, 14, cx=0, w=3, h=2)                   # Euthykles's boat, the only one they missed
    stakes(g, 12, [10, 16, 22, 32, 38, 44, 50])
    for (x, y, k) in ((18, 26, "big"), (34, 6, "block"), (12, 33, "block"), (40, 16, "big")):
        rock2(g, x, y, k)
    for (x, y) in ((4, 18), (56, 8), (54, 30), (3, 34)):
        g.set(x, y, K.SEA_ROCK, True)
    for (x, y) in ((20, 18), (30, 30)):
        tide(g, x, y, x)                                     # (a drum under the shallows reads as a square glitch at sea)
    g.piece("rocks", "stake", 9, 3)                           # ROUTE 23, off Skandeia
    g.piece("rocks", "stake", 50, 20)                         # the open sea

    P = "Route23_CretanSea_EventScript_"
    objects = [
        obj("ICHOR_DIVER", 14, 6, "down", P + "Bathyllos", "LOCALID_R23_BATHYLLOS", trainer=3),
        obj("ICHOR_SAILOR", 27, 14, "up", P + "Euthykles", "LOCALID_R23_EUTHYKLES", trainer=3, solid_ok=True),
        obj("ICHOR_DIVER", 44, 35, "right", P + "Myrsine", "LOCALID_R23_MYRSINE", trainer=1),
        item_ball(43, 27, "ITEM_BIG_PEARL", "FLAG_ICHOR_ITEM_ROUTE23_BIG_PEARL"),
    ]
    bgs = [sign(9, 3, P + "SignSkandeia"), sign(50, 20, P + "SignOpenSea"),
           sign(45, 34, P + "Wreck"), sign(46, 34, P + "GearBox"), sign(47, 34, P + "Wreck"),
           sign(45, 35, P + "Wreck"), sign(46, 35, P + "GearBox"), sign(47, 35, P + "Wreck")]
    return K.Spec("Route23_CretanSea", g, music="MUS_ICHOR_ROAD", mapsec="MAPSEC_AETHOS_ROUTE_23",
                  map_type="MAP_TYPE_OCEAN_ROUTE", border=[K.SEA] * 4, objects=objects, bgs=bgs,
                  start=(10, 10), seams={"west": 8, "east": 8}, allow_cycling=False,
                  connections=[("left", "MAP_KYTHERA_SKANDEIA", -15)],
                  screens={"1_skandeia_end": (6, 6), "2_bathyllos": (14, 9), "3_channel": (26, 12),
                           "4_antikythera": (42, 29), "5_wreck": (45, 33), "6_open_sea": (52, 20)})


def specs():
    return [cretan(), myrtoan(), route23()]
