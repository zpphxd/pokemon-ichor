"""The ground plans of Arkadia, the Cypress Wood and the Pool of Mnemosyne.

Each plan is a grid of ground characters; tools/ichor/maps/arkadia.py auto-tiles
it and stamps the structures over it. The art build reads the plans too
(`shapes()`), so each soft-edged set draws only the outlines the maps use.

Ground characters:
  .  grass (aethos)                 =  path (aethos's limestone patch)
  A  aethos woods (cypress spires, stone pines, olives over deep-shade grass)
  K  the canopy: a mass of cypress crowns (soft blob region, impassable)
  R  rock seen from above (soft blob region; impassable)
  f  a rock face below rock (impassable)
  ~  pond water (aethos)            :  the Wood's floor in deep shade
  ,  ferns (the Wood's tall grass)   s  the stump clearing's starlit floor
  v  asphodel (the Pool's tall grass)
"""
from __future__ import annotations

ARKADIA_W, ARKADIA_H = 50, 44
WOOD_W, WOOD_H = 36, 30
POOL_W, POOL_H = 24, 20

# Arkadia's seams (MAP_DESIGN §5): every edge is a seam now or later, so the
# strips are aethos-only: rows 0-5 and 38-43, columns 0-7 and 42-49.
NORTH_ROAD = (23, 24)          # Route 12's road (verges 22 and 25), offset -6
EAST_ROAD = (23, 24)           # rows: Route 13 (batch 4), the huntresses' cordon
SOUTH_ROAD = (13, 14)          # columns: Route 27 (Act III), the Lakonian hoplite
WEST_ROAD = (36, 37)           # rows: Route 32 (post-game), verges 35 and 38
STRIP_ROWS = set(range(0, 6)) | set(range(38, 44))
STRIP_COLS = set(range(0, 8)) | set(range(42, 50))

# The Wood joins the Pool at its west edge: Wood rows 13-15 to Pool rows 9-11.
WOOD_WEST_ROWS = (13, 14, 15)
POOL_EAST_ROWS = (9, 10, 11)
WOOD_TO_POOL_OFFSET = WOOD_WEST_ROWS[0] - POOL_EAST_ROWS[0]     # 4


class Plan:
    def __init__(self, w, h, fill="."):
        self.w, self.h = w, h
        self.g = [[fill] * w for _ in range(h)]

    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h - 1, y1) + 1):
            for x in range(max(0, x0), min(self.w - 1, x1) + 1):
                self.g[y][x] = c

    def cells(self, pts, c):
        for x, y in pts:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.g[y][x] = c

    def rows(self, x0, y0, rows):
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != " ":
                    self.g[y0 + j][x0 + i] = c

    def at(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.g[y][x]
        return None

    def text(self):
        return ["".join(r) for r in self.g]


def arkadia():
    p = Plan(ARKADIA_W, ARKADIA_H, ".")
    # the aethos woods all round, in the seam strips
    p.rect(0, 0, 49, 5, "A")
    p.rect(0, 38, 49, 43, "A")
    p.rect(0, 0, 7, 43, "A")
    p.rect(42, 0, 49, 43, "A")
    # Route 12's road through the north strip, a clearing either side of the gate
    p.rect(19, 3, 28, 5, ".")
    p.rect(22, 0, 25, 2, ".")
    p.rect(23, 0, 24, 13, "=")
    # the woods reach in past the strips, raggedly: the town stands in a forest
    p.rect(8, 6, 8, 34, "A")
    for (y0, y1) in ((6, 12), (21, 34)):
        p.rect(9, y0, 9, y1, "A")
    p.rect(10, 22, 10, 27, "A")
    p.rect(10, 30, 11, 34, "A")
    p.rect(40, 6, 41, 21, "A")
    p.rect(38, 6, 39, 7, "A")
    p.rect(41, 26, 41, 37, "A")
    # the east road (Route 13): verges on rows 22 and 25
    p.rect(35, EAST_ROAD[0] - 1, 49, EAST_ROAD[1] + 1, ".")
    p.rect(35, EAST_ROAD[0], 49, EAST_ROAD[1], "=")
    # the south road (Route 27) and the west road (Route 32)
    p.rect(SOUTH_ROAD[0] - 1, 38, SOUTH_ROAD[1] + 1, 43, ".")
    p.rect(SOUTH_ROAD[0], 21, SOUTH_ROAD[1], 43, "=")
    p.rect(0, WEST_ROAD[0] - 1, 12, WEST_ROAD[1] + 1, ".")
    p.rect(0, WEST_ROAD[0], 14, WEST_ROAD[1], "=")
    # the Asclepeion's outcrop: the building stands against its south face, and
    # Pan's grotto opens in the face west of it
    p.rect(10, 6, 18, 7, "R")
    p.rect(10, 8, 12, 12, "R")
    # the square: beaten earth, below the upper terrace (wall on row 12); the main
    # road runs on south through it to the lane along its foot (row 21)
    p.rect(12, 13, 33, 17, "=")
    p.rect(23, 18, 24, 21, "=")
    p.rect(SOUTH_ROAD[0], 21, 35, 21, "=")
    p.rect(12, 18, 12, 21, "=")
    p.rect(15, 12, 15, 12, "=")
    p.rect(29, 12, 29, 12, "=")
    p.rect(33, 12, 33, 12, "=")
    # the racecourse's terrace, east of the square
    p.rect(34, 12, 39, 20, ".")
    # the temple hill: the plateau and its face, cypress groves either side; the
    # waterfall cliff, wooded on top, beside it
    p.rect(17, 24, 23, 31, "R")
    p.rect(18, 23, 22, 23, "R")
    p.rect(17, 32, 23, 33, "f")
    p.rect(16, 24, 16, 33, "K")
    p.rect(15, 26, 15, 33, "K")
    p.rect(24, 23, 26, 33, "K")
    p.rect(27, 25, 27, 33, "K")
    p.rect(28, 22, 33, 26, "K")
    p.rect(27, 23, 27, 24, "K")
    p.rect(28, 27, 33, 27, "R")
    p.rect(28, 28, 33, 33, "f")
    # the plunge pool
    p.rect(29, 34, 33, 37, "~")
    # the temple road along the hill's foot, from the south road to the stair
    p.rect(SOUTH_ROAD[1], 34, 28, 35, "=")
    return p


WOOD_ROWS = [
    # 0         1         2         3
    # 012345678901234567890123456789012345
    "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",  # 0
    "KKKKKKKKKKKKKKKKKKKK::::KKKKKKKKKKKK",  # 1  the vixen's hollow
    "KKKKKKKKKKKK:::::::K:::::KKKKKKKKKKK",  # 2
    "KKKKKKKKKKK:::::::::::::KKKKKKKKKKKK",  # 3  the hedge gap at (19,3)
    "KKKKKKKKKKK::::::::KKKKKKKKKKKKKKKKK",  # 4  Agapenor's kiln
    "KKKKKKKKKKKK::::::KKKKKKKKKKKKKKKKKK",  # 5
    "KKKKKKKKKKKKKK::KKKKKKKKKKKKKKKKKKKK",  # 6  the north spur
    "KKKKKKKKKKKKKK::KKKKKKKKKKKKKKKKKKKK",  # 7
    "KKKKKKKKKKKKKsssssKKKKKKKKKKKKKKKKKK",  # 8  the stump clearing
    "KKKKKKKKKKKsssssssssKKKKKKKKKKKKKKKK",  # 9
    "KKKKKKKKKKsssssssssssKKKKKKKKKKKKKKK",  # 10
    "KKKKKKKKKKsssssssssssKKKKKKKKKKKKKKK",  # 11
    "KKK:::,,,:ssssssssssssKKKKKKKKKKKKKK",  # 12 band 2
    "::::::,,,:ssssssssssssKKKKKKKKKKKKKK",  # 13 to the Pool
    "::::::,,,:ssssssssssssKKKKKKKKKKKKKK",  # 14
    "::::::,,,:sssssssssssKKKKKKKKKKKKKKK",  # 15
    "KK::::KKKKKsssssssssssKKKKKKKKKKKKKK",  # 16
    "KK::::KKKKKKssssssssssKKKKKKKKKKKKKK",  # 17
    "KK:::::KKKKKKKsssssssKKKKKKKKKKKKKKK",  # 18
    "KK::::::KKKKKKKKKKK:KKKKKKKKKKKKKKKK",  # 19 the narrow, column 19
    "K::::::::KKKKKKKKKK:KKKKKKKKKKKKKKKK",  # 20
    "K::::::::KKKKKKKKK::KKKKKKKKKKKKKKKK",  # 21 Euadne at (18,21)
    "K::::::::KKKKKKKKKK:::::::::::::::KK",  # 22
    "K::::::::KKKKKKKKKK::::::::::::::::K",  # 23
    "K::::::::KKKKKKKKKKKKKKKKKKKK::::::K",  # 24
    "K::::::::KKKKKKKKKKKKKKKKKKKK,,,,,,K",  # 25 band 1
    "K::::::::KKKKKKKKKKKKKKKKKKKK,,,,,,K",  # 26
    "KK::::::KKKKKKKKKKKKKKKKKKKKK,,,,,,K",  # 27
    "KKK::::KKKKKKKKKKKKKKKKKKKKKK::::::K",  # 28
    "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK::KK",  # 29 the gate's mats (32-33, 29)
]


def wood():
    p = Plan(WOOD_W, WOOD_H, "K")
    assert len(WOOD_ROWS) == WOOD_H and all(len(r) == WOOD_W for r in WOOD_ROWS)
    p.rows(0, 0, WOOD_ROWS)
    return p


POOL_ROWS = [
    # 0         1         2
    # 012345678901234567890123
    "KKKKKKKKKKKKKKKKKKKKKKKK",  # 0
    "KKKKKK..........KKKKKKKK",  # 1
    "KKKK..vvvv........KKKKKK",  # 2
    "KKK..vvvvvv....vvv..KKKK",  # 3
    "KK..vvvvv......vvvvv.KKK",  # 4
    "KK.vvvv.........vvvvv.KK",  # 5
    "K.vvv............vvvv.KK",  # 6
    "K.vv..............vv..KK",  # 7
    "K......................K",  # 8
    "K.......................",  # 9  from the Wood (rows 9-11)
    "K.......................",  # 10
    "K.vv....................",  # 11
    "K.vvvv............vvv..K",  # 12
    "KK.vvvvv.........vvvv.KK",  # 13
    "KK..vvvvv.......vvvv..KK",  # 14
    "KKK...vvvvv...vvvvv..KKK",  # 15
    "KKKK....vvvvvvvvv...KKKK",  # 16
    "KKKKKK............KKKKKK",  # 17
    "KKKKKKKKK......KKKKKKKKK",  # 18
    "KKKKKKKKKKKKKKKKKKKKKKKK",  # 19
]


def pool():
    p = Plan(POOL_W, POOL_H, "K")
    assert len(POOL_ROWS) == POOL_H and all(len(r) == POOL_W for r in POOL_ROWS)
    p.rows(0, 0, POOL_ROWS)
    return p


def plans():
    return {"Arkadia": arkadia(), "Arkadia_CypressWood": wood(), "PoolOfMnemosyne": pool()}


NEIGH = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def blob_key(inside, x, y):
    b = [1 if inside(x + dx, y + dy) else 0 for dx, dy in NEIGH]
    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):
        if not (b[a] and b[c]):
            b[d] = 0
    return "1|" + "".join(str(v) for v in b)


def keys_of(p, chars, region_chars=None, outside_in=True):
    region_chars = region_chars or chars
    inside = lambda x, y: (outside_in and not (0 <= x < p.w and 0 <= y < p.h)) or \
        (0 <= x < p.w and 0 <= y < p.h and p.g[y][x] in region_chars)
    out = set()
    for y in range(p.h):
        for x in range(p.w):
            if p.g[y][x] in chars:
                out.add(blob_key(inside, x, y))
    return out


def shapes():
    """The blob keys each soft set must hold, from the plans (the map builder
    may overwrite some cells with stamps; extra keys cost little)."""
    pl = plans()
    a, w, q = pl["Arkadia"], pl["Arkadia_CypressWood"], pl["PoolOfMnemosyne"]
    return {
        "town_canopy": sorted(keys_of(a, "K", outside_in=False)),
        "town_rock": sorted(keys_of(a, "R", region_chars="Rf", outside_in=False)),
        "wood_canopy": sorted(keys_of(w, "K")),
        "pool_canopy": sorted(keys_of(q, "K")),
    }


if __name__ == "__main__":
    for name, p in plans().items():
        print(name)
        for i, r in enumerate(p.text()):
            print(f"{i:2d} {r}")
    for k, v in shapes().items():
        print(k, len(v))
