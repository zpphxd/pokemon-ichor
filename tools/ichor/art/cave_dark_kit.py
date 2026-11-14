"""The cave_dark wall, floor, light and water kit, and its autotiler.

The kit is built from 8x8 quadrants, so every join is seamless and the
whole kit costs few tiles:

  * Rock is a 3/4 view with depth. A rock cell whose south neighbour is not
    rock is the face's base (`fb`); one more row up is the face's top with its
    rim (`ft`); the rest is the rock's top surface (`T`), dark and out of
    reach. The face is two cells tall, so a wall reads as a wall.
  * The top surface has a lit lip wherever it meets floor or a recessed face
    (SYSTEMS.md §2, rule 2: rim-lit walls read inside a torch's radius).
    Rims are drawn from a distance field, so edges, rounded corners and
    inner corners all agree pixel for pixel.
  * Faces are rows of 8 px flowstone flutes. Every flute shares its edge
    columns, so any flute meets any other; the autotiler picks variants by
    position, so long walls never repeat in step.
  * Floor carries soft contact shadows under faces and beside west walls.
  * Lit floor (moonlight from a shaft, daylight at a mouth) and still water
    are regions with soft quadrant edges.

classify() and autotile() turn a character grid into metatile ids, using the
catalog the build writes, so map builders never pick wall pieces by hand.
"""
from __future__ import annotations

import math

import numpy as np

from cave_dark_lib import C, Layer, Struct, h

# --------------------------------------------------------------------------
# Textures
# --------------------------------------------------------------------------

# The rock's top surface: dark, soft low lumps, period 16. Kept quiet so it
# reads as solid rock out of reach, never as a pattern.
MASS = [
    "1111111111111111",
    "1112222111111111",
    "1122222211111111",
    "1122222211111111",
    "1112222111111111",
    "1111111111111111",
    "1111111111112221",
    "1111111111122222",
    "1111111111122222",
    "2211111111112221",
    "2221111111111111",
    "2221111111111111",
    "1211111112221111",
    "1111111122222111",
    "1111111112221111",
    "1111111111111111",
]
MASS_C = {"0": "k0", "1": "k1", "2": "k2", "3": "k3"}

# The floor: cave clay, damp patches and small stones lit from the upper left.
FLOOR = [
    "3333333333333333",
    "3333333333332333",
    "3354333333333333",
    "3342333333333333",
    "3333333333333333",
    "3333333222333333",
    "3333332222333543",
    "3233333223333422",
    "3333333333333333",
    "3333333333333333",
    "3333543333333333",
    "3333422333333333",
    "3333333333333323",
    "2233333333333333",
    "3223333333354333",
    "3333333333342333",
]
FLOOR_C = {"2": "f2", "3": "f3", "4": "f4", "5": "f5"}

# A second plain floor, scattered by the autotiler so open floor never
# repeats in step.
FLOOR2 = [
    "3333333333333333",
    "3333332333333333",
    "3333333333354333",
    "3333333333342333",
    "3354333333333333",
    "3342223333333333",
    "3332222333333333",
    "3333223333333333",
    "3333333333333333",
    "3333333333332333",
    "3333333543333333",
    "3333333422333333",
    "3333333333333333",
    "3333333333333333",
    "3323333333333543",
    "3333333333333422",
]

# Lit floor: the same clay in moonlight.
LIT_C = {"2": "f4", "3": "mn1", "4": "mn2", "5": "dl"}


def tex(rows, cmap, x, y):
    return cmap[rows[y % 16][x % 16]]


def wob16(t, phase=0.0):
    """A small periodic wobble (period 16), -1..1, for organic edges."""
    v = math.sin(2 * math.pi * (t + phase) / 16)
    return int(round(v * 0.9))


# --------------------------------------------------------------------------
# The rock's top surface (T cells)
# --------------------------------------------------------------------------

RAMP_N = ["k0", "k7", "k6", "k4", "k2"]
RAMP_W = ["k0", "k6", "k5", "k3", "k2"]
RAMP_E = ["k0", "k3", "k5", "k3", "k2"]
RIM = 5          # rim width in px
ROUND = 5        # outer corner radius


def mass_cell(N, W, E, nubs=()):
    """16x16 RGBA of a T cell. N/W/E: that side is exposed. nubs: subset of
    {'nw','ne','sw','se'}, inner corners where only the diagonal is exposed."""
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            px, py = x + 0.5, y + 0.5
            best, ramp = 99.0, None
            if N:
                d = py - wob16(x, 3) * 0.6
                if d < best:
                    best, ramp = d, RAMP_N
            if W:
                d = px - wob16(y, 7) * 0.6
                if d < best:
                    best, ramp = d, RAMP_W
            if E:
                d = 16 - px - wob16(y, 11) * 0.6
                if d < best:
                    best, ramp = d, RAMP_E
            # rounded outer corners
            for cx, cy, a, b, rp in ((ROUND, ROUND, N, W, RAMP_N), (16 - ROUND, ROUND, N, E, RAMP_N)):
                if a and b and ((cx == ROUND and px < cx) or (cx != ROUND and px > cx)) and py < cy:
                    d = ROUND - math.hypot(px - cx, py - cy)
                    best, ramp = d, rp
            for name, (cx, cy), rp in (("nw", (0, 0), RAMP_N), ("ne", (16, 0), RAMP_N),
                                       ("sw", (0, 16), RAMP_W), ("se", (16, 16), RAMP_E)):
                if name in nubs:
                    d = math.hypot(px - cx, py - cy) - 0.6
                    if d < best:
                        best, ramp = d, rp
            if ramp is not None and best < RIM:
                i = max(0, int(best))
                L.px(x, y, ramp[i])
            else:
                L.px(x, y, tex(MASS, MASS_C, x, y))
    return L.a


# --------------------------------------------------------------------------
# Faces: flowstone flutes, 8 px wide, 32 px tall (ft rows 0-15, fb rows 16-31)
# --------------------------------------------------------------------------

TOP = 2          # rim outline row at the flute edges

# Bodies of the flutes, rows 6-31, lit from the upper left. Columns 0 and 7
# of every strip follow one shared profile, so any flute meets any other;
# the bedding planes at rows 14 and 23 run through every flute, so long
# walls read as layered limestone.
BODIES = {
    "A": [  # two lobes of flowstone, one over the other
        "67887666", "67876556", "57765445", "56654435", "56544435", "55443325", "54332225",
        "53222235", "32233343", "66777766", "56776555", "56765445", "46654434", "45543334",
        "44432234", "44322234", "43223344", "32233433", "55666555", "45555444", "44444434",
        "33433333", "33332323", "22222222", "11111111", "xxxxxxxx"],
    "B": [  # a tall drapery fold
        "67876566", "67865456", "57654345", "57654335", "56654325", "56543325", "56543225",
        "56543235", "35432233", "66543356", "56543255", "56432245", "45432234", "45432234",
        "44432234", "44322234", "44322334", "33322333", "55432355", "44432344", "44322334",
        "33322333", "33222323", "22222222", "11111111", "xxxxxxxx"],
    "C": [  # a rounded boss, and a crack below
        "66666556", "66655556", "55555445", "55667545", "56777645", "56776535", "55665325",
        "53444225", "32222233", "66655666", "55544455", "55433455", "44322344", "44432444",
        "44443344", "44444344", "44434344", "33343333", "55566555", "44555444", "44444344",
        "33333333", "33433233", "22222222", "11111111", "xxxxxxxx"],
    "D": [  # two stalactites off the rim, a drip stain below
        "67763756", "67763746", "57753735", "54753645", "54744445", "54644445", "54544445",
        "55455545", "32233333", "66666666", "55665555", "5565t455", "4455t444", "4445t444",
        "44443344", "4444t344", "44434344", "33333333", "55556555", "44455444", "4444t344",
        "33333333", "33343323", "22222222", "11111111", "xxxxxxxx"],
    "wet": [  # a seep: water weeps from a crack and stains the stone
        "656x6556", "656T6556", "55tT5545", "55tT5545", "55tT6545", "55tw6545", "55tT5445",
        "55tT5445", "333t3333", "66tT6666", "55tT5555", "54tT5545", "44tt5434", "44tT4434",
        "44tt4334", "44tT4334", "44tt3334", "333t3333", "55tT5545", "44tw4434", "44tt3344",
        "33tt3333", "33tT2343", "22tt2222", "11tt1111", "xxxxxxxx"],
    "weed": [  # the tide line: barnacles, then weed down to the water (wet style)
        "67776566", "67765456", "57654345", "5765w445", "56654335", "56573325", "55432235",
        "55432235", "33233333", "66576566", "56757655", "56575445", "45474434", "44743434",
        "4t443t34", "4tT43tT4", "4tT4tTt4", "3tTttTt3", "5tTtTtT5", "4TtTtTt4", "4tTtTtT4",
        "3tttttt3", "3t2t2t23", "22222222", "11111111", "xxxxxxxx"],
}
# Outline row of the rim per column (lumps and dips); edges stay at TOP.
LUMPS = {"A": [2, 2, 1, 1, 1, 2, 2, 2], "B": [2, 2, 2, 1, 2, 2, 1, 2], "C": [2, 2, 2, 3, 3, 2, 2, 2],
         "D": [2, 1, 1, 2, 2, 2, 3, 2], "wet": [2, 2, 1, 1, 2, 2, 2, 2],
         "weed": [2, 2, 1, 1, 2, 2, 2, 2]}

# The rock's outer corners (rows 2-31): west lit, east in shadow; and the
# inner corners, where rock standing further forward meets the face.
ENDS = {
    "end_w": [
        "x76xxxxx", "x7788888", "x7777777", "x7666666", "x7676666", "x7665566", "x6655445",
        "x6654435", "x6544335", "x6543325", "x6432225", "x6322235", "x5233343", "x6777766",
        "x6776555", "x6765445", "x6654434", "x6543334", "x5432234", "x5322234", "x5223344",
        "x4233433", "x6666555", "x5555444", "x5444434", "x4433333", "x4332323", "x3222222",
        "x2111111", "xxxxxxxx"],
    "end_e": [
        "xxxxx64x", "8888864x", "7777754x", "6666643x", "6666543x", "6655432x", "5554432x",
        "5544322x", "5543322x", "5543221x", "5432221x", "5322221x", "3222221x", "6665432x",
        "5654321x", "5543321x", "4443221x", "4432221x", "4322221x", "4322211x", "4222211x",
        "3222211x", "5554321x", "4443221x", "4432221x", "3322211x", "3322211x", "2222111x",
        "111111xx", "xxxxxxxx"],
    "inner_w": [
        "xxxxxxxx", "12678888", "12567777", "12456666", "12456666", "12455566", "12345545",
        "12345445", "12344435", "12343325", "12332225", "12322235", "11222343", "12456666",
        "12345555", "12345445", "12344434", "12343334", "12332234", "12322234", "12223344",
        "11223433", "12345555", "12344444", "12344434", "11233333", "11232323", "11122222",
        "11111111", "xxxxxxxx"],
    "inner_e": [
        "xxxxxxxx", "88888762", "77777652", "66666542", "66666432", "66655432", "55554332",
        "55544322", "55443322", "55433221", "54322221", "53222221", "32222221", "66665432",
        "56654321", "55543321", "44443221", "44432221", "44322221", "44322211", "43222211",
        "33222211", "55554321", "44443221", "44432221", "33322211", "33322211", "22222111",
        "11111111", "xxxxxxxx"],
}
STRIP_C = {"x": "k0", "1": "k1", "2": "k2", "3": "k3", "4": "k4", "5": "k5", "6": "k6", "7": "k7",
           "8": "k8", "t": "tl1", "T": "tl2", "w": "wh"}
for _rows in list(BODIES.values()):
    assert len(_rows) == 26 and all(len(r) == 8 for r in _rows)
for _rows in list(ENDS.values()):
    assert len(_rows) == 30 and all(len(r) == 8 for r in _rows)


def flute(variant, x0=0):
    """8x32 RGBA strip of one flute. x0: the strip's x within its cell, so the
    mass texture above the rim stays in phase."""
    L = Layer(8, 32)
    lump = LUMPS[variant]
    body = BODIES[variant]
    for x in range(8):
        t = lump[x]
        for y in range(32):
            if y < 6 or y <= t + 3:
                if y < t:
                    c = tex(MASS, MASS_C, x0 + x, y)
                elif y == t:
                    c = "k0"
                elif y - t <= 3:
                    c = ("k8", "k7", "k6")[y - t - 1]
                else:
                    c = "k5"
            else:
                c = STRIP_C[body[y - 6][x]]
            L.px(x, y, c)
    return L.a


def flute_end(side, x0=0):
    """8x32 strip for a face's outer end, the rock's corner: the side rim of
    the rock above runs down into it. side 'w' or 'e'."""
    L = Layer(8, 32)
    rows = ENDS["end_" + side]
    for y in range(32):
        for x in range(8):
            if y < 2:
                if side == "w":
                    d = x + 0.5 - wob16(y, 7) * 0.6
                    ramp = RAMP_W
                else:
                    d = 8 - (x + 0.5) - wob16(y, 11) * 0.6
                    ramp = RAMP_E
                c = ramp[max(0, int(d))] if d < RIM else tex(MASS, MASS_C, x0 + x, y)
            else:
                c = STRIP_C[rows[y - 2][x]]
            L.px(x, y, c)
    return L.a


def flute_inner(side, x0=0):
    """8x32 strip where the face meets rock standing further forward on that
    side: on the west, the forward rock's shadow; on the east, a crease."""
    L = Layer(8, 32)
    rows = ENDS["inner_" + side]
    for y in range(32):
        for x in range(8):
            c = tex(MASS, MASS_C, x0 + x, y) if y < 2 else STRIP_C[rows[y - 2][x]]
            L.px(x, y, c)
    return L.a


FLUTES = ["A", "B", "C", "D"]


def face_cell(kind, left, right):
    """16x16 RGBA of a face cell. kind 'ft' or 'fb'; left/right: a flute
    variant, or 'end' (outer corner) or 'inner' (meets rock in front)."""
    out = np.zeros((16, 16, 4), np.uint8)
    for half, st, side in ((0, left, "w"), (1, right, "e")):
        if st == "end":
            strip = flute_end(side, half * 8)
        elif st == "inner":
            strip = flute_inner(side, half * 8)
        else:
            strip = flute(st, half * 8)
        y0 = 0 if kind == "ft" else 16
        out[:, half * 8:half * 8 + 8] = strip[y0:y0 + 16]
    return out


# --------------------------------------------------------------------------
# Floor, with contact shadows
# --------------------------------------------------------------------------

def floor_cell(N=False, W=False, nw=False, lit=False, rows=None):
    """16x16 RGBA of floor. N: a face stands to the north (its shadow);
    W: rock to the west; nw: rock only at the north-west diagonal."""
    L = Layer(16, 16)
    cmap = LIT_C if lit else FLOOR_C
    for y in range(16):
        for x in range(16):
            c = tex(rows or FLOOR, cmap, x, y)
            d = 99
            if N:
                d = min(d, y)
            if W:
                d = min(d, x + (1 if wob16(y, 5) > 0 else 0))
            if nw:
                d = min(d, int(math.hypot(x + 0.5, y + 0.5)))
            if d == 0:
                c = "f0"
            elif d == 1:
                c = "f1"
            elif d == 2:
                c = "f2" if (x + y) % 2 == 0 or c == "f2" else c
            L.px(x, y, c)
    return L.a


def lit_cell(N, S, W, E, nubs=()):
    """16x16 RGBA of lit floor, dithering into plain floor on unlit sides."""
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            px, py = x + 0.5, y + 0.5
            d = 99.0
            if N:
                d = min(d, py)
            if S:
                d = min(d, 16 - py)
            if W:
                d = min(d, px)
            if E:
                d = min(d, 16 - px)
            # outer corners round off, so a pool of light is never a rug
            R = 7.0
            for a, b, sx, sy in ((N, W, -1, -1), (N, E, 1, -1), (S, W, -1, 1), (S, E, 1, 1)):
                if a and b:
                    cx = R if sx < 0 else 16 - R
                    cy = R if sy < 0 else 16 - R
                    if (px - cx) * sx > 0 and (py - cy) * sy > 0:
                        r = math.hypot(px - cx, py - cy)
                        d = min(d, R - r) if r < R else -1
            for name, (cx, cy) in (("nw", (0, 0)), ("ne", (16, 0)), ("sw", (0, 16)), ("se", (16, 16))):
                if name in nubs:
                    d = min(d, math.hypot(px - cx, py - cy))
            lit = tex(FLOOR, LIT_C, x, y)
            plain = tex(FLOOR, FLOOR_C, x, y)
            if d < 1.5:
                c = plain
            elif d < 3:
                c = lit if (x + 2 * y) % 4 == 0 else plain
            elif d < 4.5:
                c = lit if (x + y) % 2 == 0 else plain
            elif d < 6:
                c = lit if (x + 2 * y) % 4 else plain
            else:
                c = lit
            L.px(x, y, c)
    return L.a


# --------------------------------------------------------------------------
# Still water
# --------------------------------------------------------------------------

# Still water: a dark mirror with a few long, faint reflections.
WATER = [
    "1111111111111111",
    "1111111111111111",
    "1111122222211111",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "2111111111133222",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "1112222111111111",
    "1111111111111111",
    "1111111111111111",
    "1111111112221111",
    "1111111111111111",
    "1111111111111111",
]
WATER_C = {"1": "w1", "2": "w2", "3": "w3"}


def water_cell(N, S, W, E, nubs=()):
    """16x16 RGBA of still water. A north bank shows its sunlit lip and the
    bank's face falling to the water; other banks show their lip."""
    L = Layer(16, 16)
    for y in range(16):
        for x in range(16):
            px, py = x + 0.5, y + 0.5
            c = tex(WATER, WATER_C, x, y)
            # depth: darker near banks
            dn = py if N else 99
            ds = 16 - py if S else 99
            dw = px if W else 99
            de = 16 - px if E else 99
            dc = 99
            for name, (cx, cy) in (("nw", (0, 0)), ("ne", (16, 0)), ("sw", (0, 16)), ("se", (16, 16))):
                if name in nubs:
                    dc = min(dc, math.hypot(px - cx, py - cy))
            # north bank: lip, face, waterline
            if dn < 99 or (dc < 99 and dc == min(dn, ds, dw, de, dc) and py < 8):
                d = min(dn, dc) - wob16(x, 2) * 0.5
                if d < 1:
                    c = "f3"
                elif d < 2:
                    c = "f4"
                elif d < 4:
                    c = "f2"
                elif d < 5:
                    c = "f1"
                elif d < 6:
                    c = "w0"
                elif d < 7:
                    c = "w3" if x % 4 else "w4"
            d = min(ds, dw, de, dc if py >= 8 else 99)
            if d < 99:
                d -= wob16(x if ds <= min(dw, de) else y, 9) * 0.5
                if d < 1:
                    c = "f2"
                elif d < 2:
                    c = "f4"
                elif d < 3:
                    c = "f1"
                elif d < 4:
                    c = "w0"
            L.px(x, y, c)
    return L.a


# --------------------------------------------------------------------------
# Classification and the autotiler
# --------------------------------------------------------------------------

ROCK, FLOOR_CH, LIT_CH, WATER_CH = "#", ".", ",", "~"


def classify(grid):
    """Cell kinds: 'T', 'ft', 'fb' for rock, 'floor', 'lit', 'water'."""
    H, W = len(grid), len(grid[0])

    def rock(x, y):
        return not (0 <= x < W and 0 <= y < H) or grid[y][x] == ROCK

    kinds = [[None] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            ch = grid[y][x]
            if ch == ROCK:
                if not rock(x, y + 1):
                    kinds[y][x] = "fb"
                elif not rock(x, y + 2):
                    kinds[y][x] = "ft"
                else:
                    kinds[y][x] = "T"
            elif ch == WATER_CH:
                kinds[y][x] = "water"
            elif ch == LIT_CH:
                kinds[y][x] = "lit"
            else:
                kinds[y][x] = "floor"
    return kinds


def base_row(grid, x, y):
    """The first non-rock row at or below y in column x (where a face stands)."""
    H = len(grid)
    while y < H and grid[y][x] == ROCK:
        y += 1
    return y


FLUTE_SETS = {None: (FLUTES, FLUTES), "cave": (FLUTES, FLUTES),
              "wet": (["A", "wet"], ["C", "weed"]), "crypt": (["A"], ["B"])}


def cell_key(grid, kinds, x, y, style=None):
    """The kit key of a cell, e.g. 'T|N.W.' or 'ft|A|end'. style picks the face
    variants a wall style has: the wet grottos add seeps and weed, the crypt's
    ashlar alternates its two block courses."""
    H, W = len(grid), len(grid[0])

    def k(xx, yy):
        if not (0 <= xx < W and 0 <= yy < H):
            return "T"
        return kinds[yy][xx]

    kind = kinds[y][x]
    rockish = ("T", "ft", "fb")
    if kind == "T":
        N = k(x, y - 1) not in rockish
        Wx = k(x - 1, y) != "T"
        E = k(x + 1, y) != "T"
        nubs = []
        if not N and not Wx and k(x - 1, y - 1) != "T":
            nubs.append("nw")
        if not N and not E and k(x + 1, y - 1) != "T":
            nubs.append("ne")
        if not Wx and k(x, y + 1) == "T" and k(x - 1, y + 1) != "T":
            nubs.append("sw")
        if not E and k(x, y + 1) == "T" and k(x + 1, y + 1) != "T":
            nubs.append("se")
        return mass_key(N, Wx, E, nubs)
    if kind in ("ft", "fb"):
        b0 = base_row(grid, x, y)
        sides = []
        for dx, half in ((-1, 0), (1, 1)):
            nk = k(x + dx, y)
            if nk not in rockish:
                sides.append("end")
            elif nk == "T":
                sides.append("inner")
            else:
                b1 = base_row(grid, x + dx, y) if 0 <= x + dx < W else 99
                if b1 < b0:
                    sides.append("end")
                elif b1 > b0:
                    sides.append("inner")
                else:
                    pool = FLUTE_SETS[style][half]
                    sides.append(pool[h("flute", x, half, b0) % len(pool)])
        return f"{kind}|{sides[0]}|{sides[1]}"
    if kind == "water":
        def nw(xx, yy):
            return k(xx, yy) != "water"
        N, S, Wx, E = nw(x, y - 1), nw(x, y + 1), nw(x - 1, y), nw(x + 1, y)
        nubs = [n for n, (dx, dy), a, b in (("nw", (-1, -1), N, Wx), ("ne", (1, -1), N, E),
                                             ("sw", (-1, 1), S, Wx), ("se", (1, 1), S, E))
                if not a and not b and nw(x + dx, y + dy)]
        return water_key(N, S, Wx, E, nubs)
    if kind == "lit":
        def un(xx, yy):
            return k(xx, yy) == "floor"
        N, S, Wx, E = un(x, y - 1), un(x, y + 1), un(x - 1, y), un(x + 1, y)
        nubs = [n for n, (dx, dy), a, b in (("nw", (-1, -1), N, Wx), ("ne", (1, -1), N, E),
                                             ("sw", (-1, 1), S, Wx), ("se", (1, 1), S, E))
                if not a and not b and un(x + dx, y + dy)]
        return lit_key(N, S, Wx, E, nubs)
    # plain floor
    N = k(x, y - 1) in rockish
    Wx = k(x - 1, y) in rockish
    nw = not N and not Wx and k(x - 1, y - 1) in rockish
    v = not N and not Wx and not nw and h("floor", x, y) % 3 == 0
    return floor_key(N, Wx, nw, v)


def fallbacks(key):
    """Keys to try for a cell, most specific first: rare inner-corner nubs drop
    away, and unusual flutes fall back to the common ones."""
    import itertools
    yield key
    parts = key.split("|")
    if parts[0] in ("T", "water", "lit") and len(parts) == 3:
        nubs = parts[2].split(",")
        for n in range(len(nubs) - 1, -1, -1):
            for combo in itertools.combinations(nubs, n):
                yield "|".join(parts[:2] + ([",".join(combo)] if combo else []))
    if parts[0] in ("ft", "fb"):
        common = {"B": "A", "D": "C", "wet": "A", "weed": "C"}
        yield "|".join([parts[0], common.get(parts[1], parts[1]), common.get(parts[2], parts[2])])
        yield "|".join([parts[0], "A" if parts[1] not in ("end", "inner") else parts[1], "A"
                        if parts[2] not in ("end", "inner") else parts[2]])
    if parts[0] == "floor" and len(parts) == 3:
        yield "|".join(parts[:2])


def kit_id(catalog, key, style=None):
    """The metatile id for a kit key, from the catalog JSON (as loaded): the
    style's own cells first, then the cave's, each through the fallbacks."""
    table = catalog.get("styles", {}).get(style, {}) if style else {}
    keys = list(fallbacks(key))
    for k in keys:
        if k in table:
            return table[k]
    for k in keys:
        if k in catalog["kit"]:
            return catalog["kit"][k]
    raise KeyError(key)


def autotile(grid, catalog, style=None):
    """Metatile ids for a terrain grid: rows of '#' rock, '.' floor, ','
    lit floor, '~' still water. style: None (the cave), 'wet' or 'crypt'.
    Place pieces over the result by id from catalog["pieces"]."""
    kinds = classify(grid)
    return [[kit_id(catalog, cell_key(grid, kinds, x, y, style), style) for x in range(len(grid[0]))]
            for y in range(len(grid))]


def mass_key(N, W, E, nubs):
    return "T|" + "".join(c if v else "." for c, v in (("N", N), ("W", W), ("E", E))) + \
        ("|" + ",".join(sorted(nubs)) if nubs else "")


def floor_key(N, W, nw, v=False):
    if v:
        return "floor|..|v2"
    return "floor|" + "".join(c if v else "." for c, v in (("N", N), ("W", W))) + ("|nw" if nw else "")


def water_key(N, S, W, E, nubs):
    return "water|" + "".join(c if v else "." for c, v in (("N", N), ("S", S), ("W", W), ("E", E))) + \
        ("|" + ",".join(sorted(nubs)) if nubs else "")


def lit_key(N, S, W, E, nubs):
    return "lit|" + "".join(c if v else "." for c, v in (("N", N), ("S", S), ("W", W), ("E", E))) + \
        ("|" + ",".join(sorted(nubs)) if nubs else "")


# --------------------------------------------------------------------------
# Enumerating the kit
# --------------------------------------------------------------------------

MAX_NUBS = 2     # three or four inner corners in one cell are left to the fallbacks


def _subsets(items, most=MAX_NUBS):
    out = [[]]
    for it in items:
        out += [o + [it] for o in out]
    return [o for o in out if len(o) <= most]


def mass_keys():
    keys = []
    for N in (False, True):
        for W in (False, True):
            for E in (False, True):
                free = []
                if not N and not W:
                    free.append("nw")
                if not N and not E:
                    free.append("ne")
                if not W:
                    free.append("sw")
                if not E:
                    free.append("se")
                for nubs in _subsets(free):
                    keys.append((mass_key(N, W, E, nubs), (N, W, E, tuple(nubs))))
    return keys


def region_keys(keyfn):
    keys = []
    for N in (False, True):
        for S in (False, True):
            for W in (False, True):
                for E in (False, True):
                    free = [n for n, a, b in (("nw", N, W), ("ne", N, E), ("sw", S, W), ("se", S, E))
                            if not a and not b]
                    for nubs in _subsets(free):
                        keys.append((keyfn(N, S, W, E, nubs), (N, S, W, E, tuple(nubs))))
    return keys


def face_keys():
    lefts = ["A", "C", "B", "D", "end", "inner"]
    rights = ["A", "C", "B", "D", "end", "inner"]
    out = []
    for kind in ("ft", "fb"):
        for l in lefts:
            for r in rights:
                out.append((f"{kind}|{l}|{r}", (kind, l, r)))
    return out


def kit_cells():
    """{key: (layers, walk, behavior)} for every kit cell."""
    cells = {}
    for key, (N, W, E, nubs) in mass_keys():
        cells[key] = ({"bottom": mass_cell(N, W, E, nubs)}, "X", None)
    for key, (kind, l, r) in face_keys():
        cells[key] = ({"bottom": face_cell(kind, l, r)}, "X", None)
    for N in (False, True):
        for W in (False, True):
            for nw in (False, True):
                if nw and (N or W):
                    continue
                cells[floor_key(N, W, nw)] = ({"bottom": floor_cell(N, W, nw)}, ".", "MB_CAVE")
    cells[floor_key(False, False, False, True)] = ({"bottom": floor_cell(rows=FLOOR2)}, ".", "MB_CAVE")
    for key, (N, S, W, E, nubs) in region_keys(water_key):
        cells[key] = ({"bottom": water_cell(N, S, W, E, nubs)}, "~", None)
    for key, (N, S, W, E, nubs) in region_keys(lit_key):
        cells[key] = ({"bottom": lit_cell(N, S, W, E, nubs)}, ".", "MB_NORMAL")
    return cells
