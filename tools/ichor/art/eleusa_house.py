"""Eleusa's farmhouses: a kit of parts that snap together into house fronts,
and the courtyard walls that close a farm compound.

An Eleusa house is Attic country building, not Cycladic: warm lime plaster
over mudbrick on a rubble socle, a pitched roof of red Laconian tiles (or
golden reed thatch on humbler houses), dark timber, and doors and shutters
painted ox-blood. Some farms keep a stone tower (pyrgos) for the grain.

Every part is one 16 x 16 metatile on a fixed grid of rows:

  T0, T1   the tower's cap and its upper wall (2 wide, above the roof)
  R0, R1   the roof: ridge and upper tiles, then lower tiles and the eave
  W0       the upper wall: windows, a niche, strings of garlic
  W1       the lower wall on its socle: doors, a pithos, sheaves, a bench

and three columns: L (the lit west corner), M (repeats) and R (the shaded east
corner). Textures are locked to the 16 px grid, so any part sits beside any
other of its row seamlessly, and the fronts in FRONTS are only arrangements
of these parts: they cost no metatiles of their own.
"""
from __future__ import annotations

from eleusa_lib import Layer, put, struct

SEC = "houses"

# --------------------------------------------------------------------------
# Textures (pixel functions of absolute x, y so repeats tile)
# --------------------------------------------------------------------------


def _h(x, y, k=0):
    return (x * 73 + y * 151 + k * 37 + (x * y) % 7) % 97


# Where the plaster has worn: little patches of darker daub (16 px periodic)
_WORN = {(4, 5), (5, 5), (5, 6), (11, 11), (12, 11)}
_LIT = {(3, 4), (10, 10)}


def plaster(x, y, shade=0):
    """Lime plaster over mudbrick, smooth with a few worn patches; shade 1 =
    under a porch."""
    ramp = ["pl3", "pl2", "pl1", "pl0"]
    p = (x % 16, y % 16)
    i = 1
    if p in _WORN:
        i = 2
    elif p in _LIT:
        i = 0
    if shade:
        i = 2 if i != 2 else 3
    return ramp[i]


def socle(x, y):
    """Rubble stone socle: rough grey stones in earthy mortar, 5 px tall."""
    yy = y % 16
    xx = x % 16
    row = 0 if yy < 13 else 1
    off = 0 if row == 0 else 3
    stone_w = (5, 4, 6)[((xx + off) // 5) % 3]
    edge = (xx + off) % 5 == 4
    if yy in (10,):
        return "pl0"
    if edge or yy == 15 or (row == 1 and yy == 13):
        return "pl0" if (xx + yy) % 3 else "sg0"
    if (yy == 11 or yy == 13 + 1) and not edge:
        return "sg1"
    return "sg0" if (xx * 3 + yy) % 5 == 0 else "sg1"


def roof(x, y):
    """Laconian roof tiles: rows of cover tiles over pans, lit from the left."""
    c = x % 4
    course = y % 4
    weathered = _h((x // 4) % 4, (y // 4) % 4, 3) < 14      # 16 px periodic
    if course == 3:
        return "rf0" if c == 3 else "rf1"
    col = ("rf3", "rf2", "rf1", "rf0")[c]
    if weathered and col == "rf2":
        col = "rf1"
    if course == 0 and c in (1, 2):
        col = "rf3" if c == 1 else "rf2"
    return col


def thatch(x, y):
    """Reed thatch laid in courses: each course a scalloped row of bundles,
    lit on its upper edge and shaded where the next course overlaps it."""
    yy = y % 16
    xx = x % 16
    course = yy // 4
    r = yy % 4
    # the shaggy lower edge of each course hangs unevenly over the next
    ragged = (xx * 7 + course * 5) % 5
    if r == 3:
        return "wk" if ragged < 2 else "wh1"
    if r == 2 and ragged == 0:
        return "wh1"
    # straw strokes: light, mid and shaded reeds side by side
    k = (xx + course * 2) % 4
    if r == 0:
        return ("sb3", "wh3", "sb2", "wh2")[k]
    return ("sb3", "sb2", "wh2", "sb2")[k] if r == 1 else ("sb2", "wh2", "wh2", "wh1")[k]


# --------------------------------------------------------------------------
# Part painters: each fills one 16 x 16 cell of a layer at (ox, oy)
# --------------------------------------------------------------------------


def fill(L, ox, oy, fn, x0=0, y0=0, x1=15, y1=15):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            L.px(ox + x, oy + y, fn(x, y))


def corner(L, ox, oy, side, rows=range(16), lit="pl3", shade="pl0"):
    """The house's lit west or shaded east corner, down a wall cell."""
    for y in rows:
        if side == "L":
            L.px(ox, oy + y, "ink")
            L.px(ox + 1, oy + y, lit)
        elif side == "R":
            L.px(ox + 15, oy + y, "ink")
            L.px(ox + 14, oy + y, shade)


def wall_cell(L, ox, oy, row, side="M", shade=0):
    """A plain wall cell: W0 is all plaster, W1 stands on the socle."""
    fill(L, ox, oy, lambda x, y: plaster(x, y, shade))
    if row == "W1":
        fill(L, ox, oy, socle, y0=10)
        L.hline(ox, ox + 15, oy + 15, "ink")
    corner(L, ox, oy, side, rows=range(16) if row == "W0" else range(15))
    if side == "L" and row == "W1":
        for y in range(10, 15):
            L.px(ox + 1, oy + y, "sg1")
    if side == "R" and row == "W1":
        for y in range(10, 15):
            L.px(ox + 14, oy + y, "sg0")


def roof_cell(L, ox, oy, row, side="M"):
    """Tiled roof: R0 carries the ridge, R1 the eave with its antefixes."""
    fill(L, ox, oy, roof)
    if row == "R0":
        L.hline(ox, ox + 15, oy, "ink")
        for x in range(16):
            # the ridge: a run of round cover tiles, each lit on its left
            k = x % 6
            L.px(ox + x, oy + 1, "rf3" if k in (0, 1) else "rf2")
            L.px(ox + x, oy + 2, "rf2" if k < 4 else "rf1")
            L.px(ox + x, oy + 3, "rf1" if k != 5 else "rf0")
            L.px(ox + x, oy + 4, "rf0")
    else:
        # eave: the last course, antefixes on each cover-tile line, then the
        # dark underside and the wall in the eave's shadow
        for x in range(16):
            L.px(ox + x, oy + 9, "rf3" if x % 4 == 0 else "rf2")
            L.px(ox + x, oy + 10, "rf1" if x % 4 != 3 else "rf0")
            L.px(ox + x, oy + 11, "ink")
            L.px(ox + x, oy + 12, "rf0")
            L.px(ox + x, oy + 13, "pl0")
            L.px(ox + x, oy + 14, "pl1" if x % 2 else "pl0")
            L.px(ox + x, oy + 15, "pl1")
        for x in range(0, 16, 4):
            # antefix: a small palmette standing on the eave
            L.px(ox + x, oy + 8, "rf3")
            L.px(ox + x + 1, oy + 8, "rf2")
            L.px(ox + x, oy + 7, "pl3")
    if side == "L":
        for y in range(16 if row == "R0" else 13):
            L.px(ox, oy + y, "ink")
            L.px(ox + 1, oy + y, "rf3")
        if row == "R1":
            L.px(ox, oy + 13, "ink")
            for y in range(13, 16):
                L.px(ox, oy + y, "ink")
                L.px(ox + 1, oy + y, "pl2")
    elif side == "R":
        for y in range(16 if row == "R0" else 13):
            L.px(ox + 15, oy + y, "ink")
            L.px(ox + 14, oy + y, "rf0")
        if row == "R1":
            for y in range(13, 16):
                L.px(ox + 15, oy + y, "ink")
                L.px(ox + 14, oy + y, "pl0")


def thatch_cell(L, ox, oy, row, side="M"):
    """Golden reed thatch: R0 carries a bound ridge roll, R1 a thick eave."""
    fill(L, ox, oy, thatch)
    if row == "R0":
        L.hline(ox, ox + 15, oy, "wk")
        for x in range(16):
            L.px(ox + x, oy + 1, "wh4" if x % 5 else "wh3")
            L.px(ox + x, oy + 2, "wh3")
            L.px(ox + x, oy + 3, "wh2" if x % 5 else "wk")
            L.px(ox + x, oy + 4, "wh1")
            L.px(ox + x, oy + 5, "wk" if x % 2 else "wh1")
    else:
        for x in range(16):
            L.px(ox + x, oy + 11, "wh4" if x % 3 else "wh3")
            L.px(ox + x, oy + 12, "wh3")
            L.px(ox + x, oy + 13, "wh2")
            L.px(ox + x, oy + 14, "wh1" if x % 2 else "wk")
            L.px(ox + x, oy + 15, "wk")
    if side == "L":
        for y in range(16):
            L.px(ox, oy + y, "wk")
            L.px(ox + 1, oy + y, "wh4" if y % 3 else "wh3")
    elif side == "R":
        for y in range(16):
            L.px(ox + 15, oy + y, "wk")
            L.px(ox + 14, oy + y, "wh1")


def gable_cells(L, ox, oy):
    """A 3 x 2 gable-fronted roof: R0 is the roof seen from above, its ridge
    running back from the apex; R1 is the gable's triangle with barge boards."""
    W = 48
    darker = {"rf3": "rf2", "rf2": "rf1", "rf1": "rf0", "rf0": "rf0"}

    def slope(x, y):
        # tile rows run down each slope, so the pattern is turned on its side
        c = roof(y, x if x < 24 else 47 - x)
        return c if x < 24 else darker[c]
    for y in range(16):
        for x in range(W):
            # R0: the two slopes from above, lit west, shaded east, and the
            # ridge running back from the apex as a lit seam (the same cells as
            # a temple's roof, eleusa_sacred.roof_above)
            c = slope(x, y)
            if x in (23, 24):
                c = "rf3" if x == 23 else "rf1"
                if y % 4 == 3:
                    c = "rf0"
            L.px(ox + x, oy + y, c)
    L.hline(ox, ox + W - 1, oy, "ink")
    for y in range(16):
        L.px(ox, oy + y, "ink")
        L.px(ox + 1, oy + y, "rf3")
        L.px(ox + W - 1, oy + y, "ink")
        L.px(ox + W - 2, oy + y, "rf0")
    for y in range(16):
        for x in range(W):
            yy = oy + 16 + y
            left = 23.5 - 1.5 * y
            right = 24.5 + 1.5 * y
            if left <= x <= right:
                c = plaster(x, y)
                # the round vent high in the gable
                if (x - 24) ** 2 + (y - 8.5) ** 2 <= 5:
                    c = "wd0"
                elif (x - 24) ** 2 + (y - 8.5) ** 2 <= 9:
                    c = "pl0" if x > 24 else "pl3"
                L.px(ox + x, yy, c)
            else:
                L.px(ox + x, yy, slope(x, y + 16))
        # barge boards along both slopes, lit on the west one
        for d in range(3):
            lx = int(round(23.5 - 1.5 * y)) - d
            rx = int(round(24.5 + 1.5 * y)) + d
            L.px(ox + lx, oy + 16 + y, ("rf3", "rf2", "ink")[d])
            L.px(ox + rx, oy + 16 + y, ("rf1", "rf0", "ink")[d])
    for y in range(16):
        L.px(ox, oy + 16 + y, "ink")
        L.px(ox + W - 1, oy + 16 + y, "ink")
    # the eave ends at the gable's foot
    for x in list(range(0, 4)) + list(range(W - 4, W)):
        L.px(ox + x, oy + 31, "ink")


def window(L, ox, oy, kind):
    wall_cell(L, ox, oy, "W0")
    if kind == "shutters":
        # an open window: dark room, a stone lintel and sill, ox-blood shutters
        L.rect(ox + 5, oy + 4, 6, 7, "wd0")
        L.px(ox + 6, oy + 5, "wdx")
        L.hline(ox + 4, ox + 11, oy + 3, "sg1")
        L.hline(ox + 4, ox + 11, oy + 2, "ink")
        L.hline(ox + 4, ox + 11, oy + 11, "pl3")
        L.hline(ox + 4, ox + 11, oy + 12, "pl0")
        for sx in (2, 12):
            L.rect(ox + sx, oy + 4, 2, 7, "ox")
            L.vline(ox + sx + (1 if sx == 2 else 0), oy + 4, oy + 10, "rf1")
            L.px(ox + sx, oy + 7, "wd0")
            L.px(ox + sx + 1, oy + 7, "wd0")
        L.vline(ox + 1, oy + 4, oy + 10, "ink")
        L.vline(ox + 14, oy + 4, oy + 10, "ink")
    elif kind == "lattice":
        # a small high window with a timber grille
        L.rect(ox + 4, oy + 3, 8, 7, "wd0")
        for x in range(4, 12):
            for y in range(3, 10):
                if (x - 4) % 3 == 2 or (y - 3) % 3 == 2:
                    L.px(ox + x, oy + y, "wdy" if (x + y) % 2 else "wdx")
        L.hline(ox + 3, ox + 12, oy + 2, "ink")
        L.hline(ox + 3, ox + 12, oy + 10, "pl3")
        L.vline(ox + 3, oy + 3, oy + 9, "ink")
        L.vline(ox + 12, oy + 3, oy + 9, "pl0")
    elif kind == "closed":
        # shutters closed for the heat of the day
        L.hline(ox + 4, ox + 11, oy + 3, "sg1")
        L.hline(ox + 4, ox + 11, oy + 2, "ink")
        L.rect(ox + 4, oy + 4, 8, 7, "ox")
        L.vline(ox + 7, oy + 4, oy + 10, "wd0")
        L.vline(ox + 8, oy + 4, oy + 10, "rf1")
        for y in (5, 8):
            L.hline(ox + 4, ox + 11, oy + y, "rf1")
        L.vline(ox + 3, oy + 4, oy + 10, "ink")
        L.vline(ox + 12, oy + 4, oy + 10, "wd0")
        L.hline(ox + 4, ox + 11, oy + 11, "pl3")
    elif kind == "garlic":
        # a peg hung with strings of garlic and red onions
        L.hline(ox + 3, ox + 12, oy + 2, "wdx")
        L.px(ox + 7, oy + 1, "wd0")
        for sx, colr in ((4, "pl3"), (8, "ox"), (11, "pl3")):
            for k in range(4):
                y = oy + 3 + k * 2
                L.px(ox + sx, y, colr)
                L.px(ox + sx + 1, y, colr if colr == "ox" else "pl2")
                L.px(ox + sx, y + 1, "pl0" if colr != "ox" else "rf1")
    elif kind == "niche":
        # a wall niche with a little clay figure of the Two Goddesses
        L.rect(ox + 5, oy + 3, 6, 8, "wd0")
        L.hline(ox + 6, ox + 9, oy + 2, "wd0")
        L.hline(ox + 4, ox + 11, oy + 11, "pl3")
        L.vline(ox + 4, oy + 3, oy + 10, "pl3")
        L.vline(ox + 11, oy + 3, oy + 10, "pl0")
        put(L, ox + 6, oy + 5, [".33", "3223", ".22", "2112"], {"3": "rf3", "2": "rf2", "1": "rf1"})


def door(L, ox, oy, kind, shade=0):
    wall_cell(L, ox, oy, "W1", shade=shade)
    if kind in ("plank", "dutch"):
        # stone lintel, ox-blood jambs, a door of dark planks with iron studs
        L.rect(ox + 3, oy + 0, 10, 2, "sg1")
        L.hline(ox + 3, ox + 12, oy + 2, "ink")
        for y in range(1, 16):
            L.px(ox + 3, oy + y, "ox")
            L.px(ox + 12, oy + y, "ox")
            L.px(ox + 2, oy + y, "ink")
            L.px(ox + 13, oy + y, "ink")
        for y in range(3, 15):
            for x in range(4, 12):
                c = "wdx" if (x - 4) % 3 else "wd0"
                if (x - 4) % 3 == 1:
                    c = "wdy"
                L.px(ox + x, oy + y, c)
        for x in (5, 8, 11):
            L.px(ox + x - 1, oy + 5, "sg1")
            L.px(ox + x - 1, oy + 12, "sg1")
        L.px(ox + 10, oy + 9, "sg1")
        if kind == "dutch":
            # the top leaf stands open: the warm dark of the house inside
            L.rect(ox + 4, oy + 3, 8, 5, "wd0")
            L.px(ox + 5, oy + 4, "wdx")
            L.hline(ox + 4, ox + 11, oy + 8, "ox")
        L.hline(ox + 3, ox + 12, oy + 15, "sg1")
    elif kind == "curtain":
        # an arched doorway hung with a striped woollen curtain, half drawn
        for y in range(0, 15):
            for x in range(3, 13):
                if y < 4 and (x - 7.5) ** 2 + (y - 4) ** 2 > 22:
                    continue
                L.px(ox + x, oy + y, "wd0")
        for y in range(0, 15):
            for x in range(4, 12):
                if y < 4 and (x - 7.5) ** 2 + (y - 4) ** 2 > 13:
                    continue
                if x <= 9 or y < 3:
                    L.px(ox + x, oy + y, "ox" if (y // 2) % 3 else "pl3")
        for y in range(2, 15):
            L.px(ox + 9, oy + y, "rf1")
        L.hline(ox + 3, ox + 12, oy + 15, "sg1")
        for y in range(4, 15):
            L.px(ox + 3, oy + y, "ink")
            L.px(ox + 12, oy + y, "ink")
    elif kind == "barn_l" or kind == "barn_r":
        # one leaf of a wide double door under a timber lintel
        right = kind == "barn_r"
        L.rect(ox, oy + 0, 16, 3, "wdx")
        L.hline(ox, ox + 15, oy + 0, "ink")
        L.hline(ox, ox + 15, oy + 3, "ink")
        L.hline(ox, ox + 15, oy + 1, "wdy")
        x0, x1 = (0, 13) if right else (2, 15)
        for y in range(4, 16):
            for x in range(x0, x1 + 1):
                c = "wdx" if (x % 4) else "wd0"
                if x % 4 == 1:
                    c = "wdy"
                L.px(ox + x, oy + y, c)
        # a brace across the leaf
        for i in range(10):
            bx = (x0 + 1 + i) if not right else (x1 - 1 - i)
            L.px(ox + bx, oy + 14 - i, "wdy")
        edge = 14 if right else 1
        L.vline(ox + edge, oy + 4, oy + 15, "ink")
        L.vline(ox + (0 if right else 15), oy + 4, oy + 15, "wd0")
    if kind != "barn_l" and kind != "barn_r":
        pass


def extra(L, ox, oy, kind):
    """Lower-wall cells with something against the wall."""
    wall_cell(L, ox, oy, "W1")
    if kind == "bench":
        L.rect(ox + 1, oy + 8, 14, 2, "sg1")
        L.hline(ox + 1, ox + 14, oy + 8, "pl3")
        L.hline(ox + 1, ox + 14, oy + 10, "ink")
        for x in (2, 12):
            L.rect(ox + x, oy + 11, 2, 4, "sg0")
            L.vline(ox + x - 1, oy + 11, oy + 14, "ink")
    elif kind == "amphorae":
        for ax in (2, 9):
            put(L, ox + ax, oy + 3, [
                ".KK.",
                "K32K",
                ".K2K",
                "K332K"[:4],
                "K321",
                "K321",
                "K321",
                ".K21",
                ".K1K",
                "..K.",
            ], {"K": "ink", "3": "rf3", "2": "rf2", "1": "rf1"})


def tower_cells(L, ox, oy):
    """A 2 x 2 stone tower: a tiled pyramid cap, then ashlar with a slit
    window. Its top row stands on borrowed grass round the cap."""
    W = 32
    for y in range(16):
        for x in range(W):
            # pyramid cap: a trapezoid narrowing to a finial
            half = 6 + y * 0.7
            if abs(x - 15.5) <= half and y >= 3:
                c = roof(x, y)
                if x > 15:
                    c = {"rf3": "rf2", "rf2": "rf1", "rf1": "rf0", "rf0": "rf0"}[c]
                L.px(ox + x, oy + y, c)
    # hips and finial
    for y in range(3, 16):
        L.px(ox + 15, oy + y, "rf3")
        L.px(ox + 16, oy + y, "rf1")
    put(L, ox + 14, oy + 0, [".33.", "3221", ".11."], {"3": "rf3", "2": "rf2", "1": "rf1"})
    L.outline("ink")
    # the upper wall: grey ashlar, coursed, lit on the west
    for y in range(16, 32):
        for x in range(2, 30):
            cy = (y - 16) // 4
            joint = (y - 16) % 4 == 3 or (x + (cy % 2) * 4) % 8 == 0
            c = "sg0" if joint else ("pl3" if x < 4 else ("sg1" if x < 26 else "sg0"))
            L.px(ox + x, oy + y, c)
        L.px(ox + 1, oy + y, "ink")
        L.px(ox + 30, oy + y, "ink")
    for x in range(1, 31):
        L.px(ox + x, oy + 16, "rf0")
    # the slit window
    L.rect(ox + 14, oy + 20, 3, 8, "wd0")
    L.vline(ox + 13, oy + 20, oy + 27, "pl3")
    L.vline(ox + 17, oy + 20, oy + 27, "sg0")
    # the ground either side of the tower's foot is roof, not grass: it stands
    # behind the house, so its foot is hidden by the house's ridge row
    for y in range(16, 32):
        for x in (0, 31):
            L.px(ox + x, oy + y, None)


# --------------------------------------------------------------------------
# Courtyard walls
# --------------------------------------------------------------------------


def court_wall(L, ox, oy, key):
    """A courtyard wall cell on borrowed grass: plaster on a socle under a tiled
    coping. key: 'EW' run, 'E' or 'W' (the run's end on that side), 'NS',
    'NE' or 'NW' (a corner joining north and that side), or 'gate'."""
    def ew(x0, x1):
        for x in range(x0, x1 + 1):
            for y in range(4, 7):
                L.px(ox + x, oy + y, ("rf3", "rf2", "rf0")[y - 4] if x % 4 else ("rf2", "rf1", "rf0")[y - 4])
            L.px(ox + x, oy + 3, "ink")
            for y in range(7, 15):
                L.px(ox + x, oy + y, plaster(x, y) if y < 11 else socle(x, y - 1))
            L.px(ox + x, oy + 7, "pl0")
            L.px(ox + x, oy + 15, "ink")

    def ns(x0, x1, y0, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = ("rf3", "rf2", "rf2", "rf1", "rf1", "rf0")[x - x0] if y % 4 else "rf0"
                L.px(ox + x, oy + y, c)
            L.px(ox + x0 - 1, oy + y, "ink")
            L.px(ox + x1 + 1, oy + y, "ink")
            L.px(ox + x1 + 2, oy + y, "pl0")
    if key == "EW":
        ew(0, 15)
    elif key in ("E", "W"):
        # the run ends in a squared pier, lit on the west
        if key == "W":
            ew(3, 15)
            for y in range(3, 16):
                L.px(ox + 2, oy + y, "ink")
                L.px(ox + 3, oy + y, "pl3" if y > 7 else "rf3")
        else:
            ew(0, 12)
            for y in range(3, 16):
                L.px(ox + 13, oy + y, "ink")
                L.px(ox + 12, oy + y, "pl0" if y > 7 else "rf0")
    elif key == "NS":
        ns(5, 10, 0, 15)
    elif key in ("NE", "NW"):
        # a front corner: the north-south run comes down onto the east-west run
        if key == "NE":
            ew(5, 15)
            for y in range(3, 16):
                L.px(ox + 4, oy + y, "ink")
                L.px(ox + 5, oy + y, "pl3" if y > 7 else "rf3")
        else:
            ew(0, 10)
            for y in range(3, 16):
                L.px(ox + 11, oy + y, "ink")
                L.px(ox + 10, oy + y, "pl0" if y > 7 else "rf0")
        ns(5, 10, 0, 3)
    elif key == "gate":
        # two piers under a little tiled roof; the gate leaves stand open
        for y in range(0, 6):
            for x in range(0, 16):
                if y == 0:
                    L.px(ox + x, oy + y, "ink")
                else:
                    L.px(ox + x, oy + y, roof(x, y) if y < 4 else ("rf3", "rf2", "rf0", "ink")[min(3, y - 3)] if y < 6 else "ink")
        L.hline(ox, ox + 15, oy + 4, "rf3")
        L.hline(ox, ox + 15, oy + 5, "ink")
        for px_ in (0, 13):
            for y in range(6, 16):
                for x in range(px_, px_ + 3):
                    L.px(ox + x, oy + y, ("pl3", "pl2", "pl0")[x - px_] if y < 12 else socle(x, y - 1))
            L.vline(ox + px_ + (3 if px_ == 0 else -1), oy + 6, oy + 15, "ink")
        # open leaves pushed back against the piers
        for y in range(7, 15):
            L.px(ox + 4, oy + y, "wdx")
            L.px(ox + 11, oy + y, "wd0")
        L.hline(ox, ox + 2, oy + 15, "ink")
        L.hline(ox + 13, ox + 15, oy + 15, "ink")


# --------------------------------------------------------------------------
# The kit as structures (each one a row or block of named parts)
# --------------------------------------------------------------------------


def build_parts():
    out = []
    s = struct("roof_tile", "Tiled roof: ridge row and eave row", 3, 2, SEC,
               walk=["XXX", "XXX"],
               names={"R0_L": (0, 0), "R0_M": (1, 0), "R0_R": (2, 0),
                      "R1_L": (0, 1), "R1_M": (1, 1), "R1_R": (2, 1)},
               notes="Red Laconian tiles. Repeat the middle column for a wider house.")
    for i, side in enumerate("LMR"):
        roof_cell(s.B, i * 16, 0, "R0", side)
        roof_cell(s.B, i * 16, 16, "R1", side)
    out.append(s)
    s = struct("roof_thatch", "Reed-thatched roof: ridge row and eave row", 3, 2, SEC,
               walk=["XXX", "XXX"],
               names={"R0_L": (0, 0), "R0_M": (1, 0), "R0_R": (2, 0),
                      "R1_L": (0, 1), "R1_M": (1, 1), "R1_R": (2, 1)},
               notes="Golden reed thatch for humbler houses, barns and the granary.")
    for i, side in enumerate("LMR"):
        thatch_cell(s.B, i * 16, 0, "R0", side)
        thatch_cell(s.B, i * 16, 16, "R1", side)
    out.append(s)
    s = struct("roof_gable", "Gable-fronted roof, 3 wide", 3, 2, SEC, walk=["XXX", "XXX"],
               names={"R0_L": (0, 0), "R0_M": (1, 0), "R0_R": (2, 0),
                      "R1_L": (0, 1), "R1_M": (1, 1), "R1_R": (2, 1)},
               notes="The house turned end-on: the roof from above with its ridge running "
                     "back, then the gable's triangle with a round vent. Always 3 wide; put "
                     "3-wide wall rows under it.")
    gable_cells(s.B, 0, 0)
    out.append(s)
    s = struct("wall", "Wall rows: upper and lower (on the socle)", 3, 2, SEC,
               walk=["XXX", "XXX"],
               names={"W0_L": (0, 0), "W0_M": (1, 0), "W0_R": (2, 0),
                      "W1_L": (0, 1), "W1_M": (1, 1), "W1_R": (2, 1)},
               notes="Plain plaster. Every window, door and extra below is a W0 or W1 M "
                     "cell, so it can stand anywhere between the corners.")
    for i, side in enumerate("LMR"):
        wall_cell(s.B, i * 16, 0, "W0", side)
        wall_cell(s.B, i * 16, 16, "W1", side)
    out.append(s)
    kinds = ["shutters", "lattice", "closed", "garlic"]
    s = struct("windows", "Upper-wall cells: windows and garlic", 4, 1, SEC,
               walk=["XXXX"], names={k: (i, 0) for i, k in enumerate(kinds)},
               notes="W0 cells. `shutters` is an open window with ox-blood shutters, "
                     "`lattice` a small timber grille, `closed` shutters shut, `garlic` "
                     "strings of garlic and onions on a peg.")
    for i, k in enumerate(kinds):
        window(s.B, i * 16, 0, k)
    out.append(s)
    dk = ["plank", "dutch", "curtain", "barn_l", "barn_r"]
    s = struct("doors", "Doors (lower-wall cells)", 5, 1, SEC, walk=["DDDDD"],
               names={k: (i, 0) for i, k in enumerate(dk)},
               notes="W1 cells; every one is a door (MB_NON_ANIMATED_DOOR): put the warp "
                     "there. `plank` a dark plank door in ox-blood jambs, `dutch` its top "
                     "leaf open, `curtain` an arched doorway with a striped wool curtain, "
                     "`barn_l` + `barn_r` a wide double door (warp on both).")
    for i, k in enumerate(dk):
        door(s.B, i * 16, 0, k)
    out.append(s)
    ek = ["bench", "amphorae"]
    s = struct("wall_extras", "Lower-wall cells with things against the wall", 2, 1, SEC,
               walk=["XX"], names={k: (i, 0) for i, k in enumerate(ek)},
               notes="W1 cells: a stone bench, two amphorae.")
    for i, k in enumerate(ek):
        extra(s.B, i * 16, 0, k)
    out.append(s)
    s = struct("porch", "Porch (pastas) on timber posts", 3, 2, SEC, walk=["XXX", "XXD"],
               names={"W0_post": (0, 0), "W0_mid": (1, 0), "W0_beam_end": (2, 0),
                      "W1_post": (0, 1), "W1_mid": (1, 1), "W1_door": (2, 1)},
               notes="Wall rows in the porch's shade, under a tiled roof's R1 row. A post "
                     "stands in `*_post` cells; `*_mid` repeats; `W1_door` is a plank door "
                     "in the shade (MB_NON_ANIMATED_DOOR). Mirror the order for a post on "
                     "the right: posts are drawn on the cell's west side.")
    porch(s.B)
    out.append(s)
    s = struct("tower", "Pyrgos: the farm's stone tower", 2, 2, SEC, walk=["XX", "XX"],
               names={"T0_L": (0, 0), "T0_R": (1, 0), "T1_L": (0, 1), "T1_R": (1, 1)},
               notes="Two rows that stand above a house's R0 at one end, so the tower "
                     "rises behind the roof. The cap's top corners are borrowed grass.")
    from eleusa_lib import ground
    tower_cells(s.M, 0, 0)
    ground(s, "grass", [(0, 0), (1, 0)])
    # the tower's lower row is opaque: copy into the bottom layer
    s.B.a[16:32] = s.M.a[16:32]
    s.M.a[16:32] = 0
    # fill the two edge columns of the lower row with the roof ridge colour
    for y in range(16, 32):
        for x in (0, 31):
            s.B.px(x, y, "ink")
    out.append(s)
    ck = ["EW", "W", "E", "NS", "NE", "NW", "gate"]
    s = struct("court_wall", "Courtyard walls: plaster under tiled coping", 7, 1, SEC,
               walk=["XXXXXXT"], names={k: (i, 0) for i, k in enumerate(ck)}, on="grass",
               notes="On borrowed grass. `EW` the run, `W`/`E` its ends, `NS` a run "
                     "going north (seen from above), `NE`/`NW` front corners where a "
                     "side wall comes down onto the front run, `gate` an open gateway "
                     "under a little roof (walk through it; drawn over the player).")
    for i, k in enumerate(ck):
        court_wall(s.T if k == "gate" else s.M, i * 16, 0, k)
    out.append(s)
    return out


def porch(L):
    for i in range(3):
        wall_cell(L, i * 16, 0, "W0", shade=1)
        wall_cell(L, i * 16, 16, "W1", shade=1)
    # the porch beam under the eave
    for x in range(48):
        L.px(x, 0, "wdy")
        L.px(x, 1, "wdx")
        L.px(x, 2, "ink")
        L.px(x, 3, "pl0")
    door(L, 32, 16, "plank", shade=1)
    for x in range(32, 48):
        for y in range(0, 4):
            L.px(x, y, ("wdy", "wdx", "ink", "pl0")[y])
    # posts on the west side of the post cells
    for y in range(3, 32):
        L.px(2, y, "ink")
        L.px(3, y, "wdy")
        L.px(4, y, "wdx")
        L.px(5, y, "wd0")
        L.px(6, y, "ink")
    for x in range(1, 8):
        L.px(x, 30, "sg1")
        L.px(x, 31, "ink")
    L.hline(1, 7, 29, "pl3")
    # the post's capital: a plain block under the beam
    L.hline(1, 7, 3, "wdy")
    L.hline(1, 7, 4, "ink")


# --------------------------------------------------------------------------
# House fronts: arrangements of parts (no metatiles of their own)
# --------------------------------------------------------------------------

# Each front is rows of "struct.name" part references, top row first. "." is
# not part of the house (leave the map's own ground there).
FRONTS = {
    "cottage": {
        "title": "Smallholder's cottage",
        "who": "a reaper's family: three wide, one window, a plank door",
        "rows": [
            ["roof_tile.R0_L", "roof_tile.R0_M", "roof_tile.R0_R"],
            ["roof_tile.R1_L", "roof_tile.R1_M", "roof_tile.R1_R"],
            ["wall.W0_L", "windows.shutters", "wall.W0_R"],
            ["wall.W1_L", "doors.plank", "wall.W1_R"],
        ],
    },
    "longhouse": {
        "title": "Long farmhouse with a barn door",
        "who": "a big household: five wide, garlic by the window, double doors",
        "rows": [
            ["roof_tile.R0_L", "roof_tile.R0_M", "roof_tile.R0_M", "roof_tile.R0_M", "roof_tile.R0_R"],
            ["roof_tile.R1_L", "roof_tile.R1_M", "roof_tile.R1_M", "roof_tile.R1_M", "roof_tile.R1_R"],
            ["wall.W0_L", "windows.lattice", "wall.W0_M", "windows.garlic", "wall.W0_R"],
            ["wall.W1_L", "wall_extras.amphorae", "doors.barn_l", "doors.barn_r", "wall.W1_R"],
        ],
    },
    "porch_house": {
        "title": "House with a porch",
        "who": "a shaded pastas on timber posts along the front",
        "rows": [
            ["roof_tile.R0_L", "roof_tile.R0_M", "roof_tile.R0_M", "roof_tile.R0_R"],
            ["roof_tile.R1_L", "roof_tile.R1_M", "roof_tile.R1_M", "roof_tile.R1_R"],
            ["porch.W0_post", "porch.W0_mid", "porch.W0_mid", "porch.W0_post"],
            ["porch.W1_post", "porch.W1_mid", "porch.W1_door", "porch.W1_post"],
        ],
    },
    "tower_farm": {
        "title": "Tower farmhouse",
        "who": "a farm with a stone grain tower rising behind its west end",
        "rows": [
            ["tower.T0_L", "tower.T0_R", ".", "."],
            ["tower.T1_L", "tower.T1_R", ".", "."],
            ["roof_tile.R0_L", "roof_tile.R0_M", "roof_tile.R0_M", "roof_tile.R0_R"],
            ["roof_tile.R1_L", "roof_tile.R1_M", "roof_tile.R1_M", "roof_tile.R1_R"],
            ["wall.W0_L", "windows.closed", "windows.garlic", "wall.W0_R"],
            ["wall.W1_L", "wall_extras.bench", "doors.dutch", "wall.W1_R"],
        ],
    },
    "gable_house": {
        "title": "Gable-fronted house",
        "who": "end-on to the lane, a curtain in the doorway",
        "rows": [
            ["roof_gable.R0_L", "roof_gable.R0_M", "roof_gable.R0_R"],
            ["roof_gable.R1_L", "roof_gable.R1_M", "roof_gable.R1_R"],
            ["wall.W0_L", "windows.lattice", "wall.W0_R"],
            ["wall.W1_L", "doors.curtain", "wall.W1_R"],
        ],
    },
    "thatch_cottage": {
        "title": "Thatched cottage",
        "who": "a poor tenant's house under golden reed thatch",
        "rows": [
            ["roof_thatch.R0_L", "roof_thatch.R0_M", "roof_thatch.R0_M", "roof_thatch.R0_R"],
            ["roof_thatch.R1_L", "roof_thatch.R1_M", "roof_thatch.R1_M", "roof_thatch.R1_R"],
            ["wall.W0_L", "windows.closed", "wall.W0_M", "wall.W0_R"],
            ["wall.W1_L", "doors.plank", "wall_extras.bench", "wall.W1_R"],
        ],
    },
    "granary": {
        "title": "Granary barn",
        "who": "the village's grain store: thatch, a high hatch and barn doors",
        "rows": [
            ["roof_thatch.R0_L", "roof_thatch.R0_M", "roof_thatch.R0_M", "roof_thatch.R0_R"],
            ["roof_thatch.R1_L", "roof_thatch.R1_M", "roof_thatch.R1_M", "roof_thatch.R1_R"],
            ["wall.W0_L", "windows.lattice", "windows.lattice", "wall.W0_R"],
            ["wall.W1_L", "doors.barn_l", "doors.barn_r", "wall.W1_R"],
        ],
    },
    "gable_tower": {
        "title": "Gable house with a tower",
        "who": "the headman's house: a gable front and a grain tower beside it",
        "rows": [
            [".", ".", ".", "tower.T0_L", "tower.T0_R"],
            [".", ".", ".", "tower.T1_L", "tower.T1_R"],
            ["roof_gable.R0_L", "roof_gable.R0_M", "roof_gable.R0_R", "roof_tile.R0_M", "roof_tile.R0_R"],
            ["roof_gable.R1_L", "roof_gable.R1_M", "roof_gable.R1_R", "roof_tile.R1_M", "roof_tile.R1_R"],
            ["wall.W0_L", "windows.shutters", "wall.W0_M", "windows.garlic", "wall.W0_R"],
            ["wall.W1_L", "doors.curtain", "wall.W1_M", "wall_extras.amphorae", "wall.W1_R"],
        ],
    },
}


def front_image(structs, rows):
    """RGB array of a front composed from part references (for previews)."""
    import numpy as np
    from eleusa_lib import aethos, composite
    by = {s.key: s for s in structs}
    comps = {}
    h, w = len(rows), len(rows[0])
    out = np.zeros((h * 16, w * 16, 3), np.uint8)
    for j, row in enumerate(rows):
        for i, ref in enumerate(row):
            if ref == ".":
                out[j * 16:j * 16 + 16, i * 16:i * 16 + 16] = aethos(0x001)
                continue
            key, name = ref.split(".")
            s = by[key]
            if key not in comps:
                comps[key] = composite(s)
            cx, cy = s.names[name]
            out[j * 16:j * 16 + 16, i * 16:i * 16 + 16] = comps[key][cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
    return out


def build():
    return build_parts()
