"""Kaldera, Thera's drowned volcano, painted whole (design/AWE_PASS.md item 3, C2).

The map is one set piece, so it is painted as a single 40 x 40 scene and sliced
into cells, as the Loom is; tools/ichor/art/kaldera_build.py does the slicing,
compiling and cataloging. Plain sea stays aethos's own animated sea (0x170),
and cells where the sea shows through borrow it.

The land is a height map (lvl): 0 sea, 1 shore (the black-sand port, the
causeway, Nea Kameni), 2 terraces, 3 the caldera rim, 4 the temple terrace.
A drop to the south is drawn as a cliff face, ALT[high] - ALT[low] cells tall,
banded by altitude, so every face shows the same strata at the same height,
as Thera's do: black lava at the waterline, red scoria above it, a thin white
seam, red again, a black flow, and the thick white Minoan pumice on top.

On it: the white town on the eastern rim (Cycladic cubes, blue doors, blue
domes on the shrines only, STYLE §4.5), the Temple of Hephaestus on the
highest terrace, the switchback stair down to the port, the ash cliff with
Akrotiri's fresco wall and its Minoan door, and on the islet the unfinished
bronze man (6 x 10) in his casting pit, scaffold up one side, the Telchines'
forge mouth at his feet, one lava vein from neck to heel.

Light comes from the top left (STYLE §2). Every color is a multiple of 8.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402

W = H = 40
PX = 16

# --------------------------------------------------------------------------
# Colors and the seven palette groups (secondary slots 6-12)
# --------------------------------------------------------------------------

P = {
    "ink": (32, 24, 24),
    # strata: basalt, red scoria, white pumice
    "k_bk0": (24, 24, 40), "k_bk1": (48, 48, 64), "k_bk2": (80, 72, 88), "k_bk3": (120, 112, 120),
    "k_rd0": (96, 40, 40), "k_rd1": (144, 64, 48), "k_rd2": (184, 96, 64), "k_rd3": (216, 144, 104),
    "k_wp0": (176, 168, 160), "k_wp1": (208, 200, 184), "k_wp2": (232, 224, 208),
    "k_fw": (248, 248, 240), "k_och": (200, 160, 104),
    # rim soil (pumice ash) and the black sand
    "k_ag0": (144, 128, 112), "k_ag1": (176, 160, 136), "k_ag2": (200, 184, 160), "k_ag3": (224, 208, 184),
    "k_bs0": (32, 32, 40), "k_bs1": (56, 56, 64), "k_bs2": (88, 80, 88), "k_bs3": (128, 120, 120),
    "k_kq": (168, 224, 232), "k_sc1": (104, 112, 64), "k_sc2": (152, 152, 88),
    # whitewash and Aegean blue
    "k_cw1": (224, 224, 216), "k_cw2": (184, 184, 192), "k_cw3": (128, 128, 144),
    "k_ab0": (24, 48, 120), "k_ab1": (40, 88, 176), "k_ab2": (96, 144, 216),
    "k_tc1": (184, 88, 48), "k_tc2": (224, 136, 88), "k_bas": (72, 120, 64), "k_gold": (240, 200, 96),
    # bronze, verdigris and lava
    "k_bz0": (64, 32, 24), "k_bz1": (112, 64, 32), "k_bz2": (160, 104, 48), "k_bz3": (208, 152, 72),
    "k_bz4": (240, 208, 128), "k_vg0": (40, 96, 88), "k_vg1": (88, 160, 136),
    "k_lv0": (168, 32, 16), "k_lv1": (232, 96, 24), "k_lv2": (248, 176, 48), "k_lv3": (248, 240, 160),
    # Nea Kameni's lava rock
    "k_lr0": (24, 24, 32), "k_lr1": (48, 40, 48), "k_lr2": (72, 64, 72), "k_lr3": (112, 104, 104),
    "k_smk": (160, 152, 152),
    # the temple's marble, the scaffold's timber, painted red and blue
    "k_mw0": (248, 240, 224), "k_mw1": (216, 208, 192), "k_mw2": (168, 160, 152), "k_mw3": (112, 104, 112),
    "k_wd0": (64, 40, 24), "k_wd1": (112, 72, 40), "k_wd2": (160, 112, 64), "k_wd3": (208, 168, 120),
    "k_pr": (176, 48, 40), "k_pb": (40, 72, 152),
    # ruins (STYLE §4.8 proposal): weathered stone darker than the living temple, fresco
    "k_rw0": (96, 88, 80), "k_rw1": (136, 120, 104), "k_rw2": (184, 168, 144),
    "k_frb": (72, 120, 184), "k_frr": (184, 72, 48), "k_fro": (216, 168, 88), "k_moss": (88, 112, 64),
}
for _n, _c in P.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, _n
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)

GROUPS = {
    "strata": ["ink", "k_bk0", "k_bk1", "k_bk2", "k_bk3", "k_rd0", "k_rd1", "k_rd2", "k_rd3",
               "k_wp0", "k_wp1", "k_wp2", "k_fw", "k_och", "k_ag2"],
    "ground": ["ink", "k_ag0", "k_ag1", "k_ag2", "k_ag3", "k_bs0", "k_bs1", "k_bs2", "k_bs3",
               "k_wp1", "k_fw", "k_kq", "k_sc1", "k_sc2", "k_wp2"],
    "cyc": ["ink", "k_fw", "k_cw1", "k_cw2", "k_cw3", "k_ab0", "k_ab1", "k_ab2", "k_tc1", "k_tc2",
            "k_bas", "k_gold", "k_ag1", "k_ag2", "k_ag0"],
    "bronze": ["ink", "k_bz0", "k_bz1", "k_bz2", "k_bz3", "k_bz4", "k_vg0", "k_vg1", "k_gold",
               "k_lv0", "k_lv1", "k_lv2", "k_lv3", "k_bk0", "k_bk2"],
    "islet": ["ink", "k_lr0", "k_lr1", "k_lr2", "k_lr3", "k_lv0", "k_lv1", "k_lv2", "k_lv3",
              "k_smk", "k_rd0", "k_rd1", "k_bs1", "k_fw", "k_kq"],
    "temple": ["ink", "k_mw0", "k_mw1", "k_mw2", "k_mw3", "k_wd0", "k_wd1", "k_wd2", "k_wd3",
               "k_pr", "k_pb", "k_bz2", "k_bz3", "k_gold", "k_ag1"],
    "fresco": ["ink", "k_rw0", "k_rw1", "k_rw2", "k_frb", "k_frr", "k_fro", "k_ag0", "k_ag1",
               "k_ag2", "k_ag3", "k_moss", "k_bz1", "k_bz2", "k_bs1"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, _g
    assert len({P[n] for n in _names}) == len(_names), _g


def c(name):
    return P[name]


# --------------------------------------------------------------------------
# The land
# --------------------------------------------------------------------------

SEA, SHORE, TERRACE, RIM, TEMPLE = 0, 1, 2, 3, 4
ALT = {SEA: 0, SHORE: 0, TERRACE: 2, RIM: 4, TEMPLE: 5}   # cliff height above the sea, in cells


def _rim_north(x):
    if x < 6:
        return 0
    if x <= 8 or 14 <= x <= 17:
        return 2
    return 3


def _rim_east(y):
    for y1, x in ((4, 18), (8, 20), (12, 22), (17, 23), (21, 24)):
        if y <= y1:
            return x
    return None


def geography():
    lvl = np.zeros((H, W), int)
    kind = np.full((H, W), "sea", object)
    for y in range(H):
        for x in range(W):
            xe = _rim_east(y)
            if y < _rim_north(x) or (xe is not None and x >= xe):
                lvl[y, x], kind[y, x] = RIM, "rim"

    def box(x0, y0, x1, y1, lv, k):
        lvl[y0:y1 + 1, x0:x1 + 1] = lv
        kind[y0:y1 + 1, x0:x1 + 1] = k

    box(22, 22, 39, 39, TERRACE, "rim")          # the lower terrace, and the southeast
    box(0, 36, 28, 39, TERRACE, "rim")           # the south rim, seen from above
    box(6, 30, 21, 35, SHORE, "sand")            # the black-sand port
    box(22, 28, 28, 35, SHORE, "sand")
    box(11, 22, 13, 29, SHORE, "sand")           # the causeway to Nea Kameni
    for y in range(H):
        for x in range(W):
            if ((x - 11) / 6.6) ** 2 + ((y - 14.5) / 8.0) ** 2 < 1 and lvl[y, x] == SEA:
                lvl[y, x], kind[y, x] = SHORE, "islet"
    box(8, 8, 14, 13, TERRACE, "mound")           # the casting mound, its corners cut
    box(7, 9, 7, 13, TERRACE, "mound")
    box(15, 9, 15, 13, TERRACE, "mound")
    box(26, 0, 34, 4, TEMPLE, "rim")             # Hephaestus's terrace
    box(39, 0, 39, 39, SEA, "sea")               # the island's outer flank drops to the sea
    box(0, 39, 38, 39, SEA, "sea")
    return lvl, kind


LVL, KIND = geography()

# stairs cut through faces (walkable): the switchback, the temple's krepis, the mound
STAIRS = {(26, 28), (27, 28), (26, 29), (27, 29),       # port -> lower terrace
          (33, 22), (34, 22), (33, 23), (34, 23),       # lower terrace -> rim
          (29, 5), (30, 5), (31, 5),                    # rim -> temple
          (14, 14), (14, 15)}                           # islet -> the giant's mound
FORGE_DOOR = (11, 15)
AKROTIRI_DOOR = (24, 29)

# whitewashed lanes through the town and down the terrace
LANES = set()


def _lane(x0, y0, x1, y1):
    LANES.update((x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1))


_lane(29, 6, 32, 7)       # under the temple stair
_lane(31, 6, 32, 21)      # the main street down the rim
_lane(31, 19, 34, 21)     # to the stair head
_lane(32, 11, 36, 11)     # Asclepeion
_lane(28, 16, 31, 16)     # Agora
_lane(32, 18, 36, 18)     # Smith's house
_lane(22, 12, 30, 12)     # to the rim-edge shrine and the north path
_lane(22, 4, 23, 11)
_lane(18, 3, 23, 4)
_lane(26, 24, 34, 25)     # the terrace walk between the two stairs
_lane(26, 26, 27, 27)

QUAY = {(x, y) for x in range(14, 22) for y in range(30, 33)}
QUAY |= {(x, y) for x in range(16, 21) for y in range(33, 34)}

PEBBLES = set()
for _x, _y in ((23, 6), (24, 6), (24, 7), (21, 9), (26, 10), (27, 11), (33, 9), (32, 13),
               (36, 13), (35, 19), (36, 20), (37, 19), (25, 16), (24, 15), (29, 18), (34, 25),
               (30, 27), (31, 26), (38, 25), (36, 33), (37, 34), (4, 36), (14, 36), (15, 37),
               (22, 36), (26, 38), (20, 0), (21, 1), (8, 0), (35, 3), (37, 4), (38, 9)):
    PEBBLES.add((_x, _y))

SCRUB = {(x, y) for x in range(30, 39) for y in range(29, 38)
         if not (x < 32 and y > 34) and (x + 2 * y) % 13 != 0}


def face_info():
    """{(x, y): (high level, row in the face, face height, low level)}"""
    out = {}
    for x in range(W):
        for y in range(1, H):
            hi, lo = LVL[y - 1, x], LVL[y, x]
            if hi > lo and (x, y - 1) not in out:
                k = ALT[hi] - ALT[lo]
                for r in range(k):
                    if y + r < H and LVL[y + r, x] == lo:
                        out[(x, y + r)] = (hi, r, k, lo)
    return out


FACES = face_info()


# --------------------------------------------------------------------------
# Periodic noise (16 px), so textures repeat on the grid and cells dedupe
# --------------------------------------------------------------------------

def hp(X, Y, k=0):
    x, y = X % 16, Y % 16
    v = (x * 374761393 + y * 668265263 + k * 1442695041) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return (v ^ (v >> 16)) % 97


def hp8(X, Y, k=0):
    """hp() on an 8 px period: a texture whose 8x8 tiles all repeat (cheap)."""
    return hp(X % 8, Y % 8, k)


# --------------------------------------------------------------------------
# Ground
# --------------------------------------------------------------------------

def soil(X, Y):
    n = hp8(X, Y, 1)
    if n < 6:
        return c("k_ag1")
    if n > 90:
        return c("k_ag3")
    if (hp8(X // 2 * 2, Y // 2 * 2, 3) < 9):
        return c("k_ag1")
    return c("k_ag2")


def paving(X, Y):
    x, y = X % 16, Y % 16
    # whitewashed flags, 8 px courses offset by half
    off = 4 if (Y // 8) % 2 else 0
    if y % 8 == 7 or (x + off) % 8 == 7:
        return c("k_cw2")
    if hp8(X, Y, 5) < 8:
        return c("k_cw1")
    return c("k_fw")


LAVA_ROCK = """
aaaaacaaaaakbaaa
aaaacaaaaaakbaaa
aaaaaaaaaaakbbaa
kkaaaaaaaakbbaaa
bkkkaaaaakbaaaca
abbkkkkkkbaaacaa
aaaaabbbbaaaaaaa
aacaaaaaaaaaaaaa
acaaaaaaakkkaaaa
aaaaaaaakbbbkkaa
aaaaaaakbaaabkkk
kaaaaakbaaaaaabb
bkaaakbaacaaaaaa
abkkkbaacaaaaaaa
aabbbaaaaaaaaaaa
aaaaaaaaaaaaaaaa
""".split()

BLACK_SAND = """
aaaaaabaaaaaaaaa
aaaaabbaaaacaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaaabaaaaa
acaaaaaaabbaaaaa
aaaaaaaaaaaaaaba
aaaaabaaaaaaaaaa
aaaaaaaaaaaaaaaa
aaaaaaaaapaaaaaa
aabaaaaaaaaaaaaa
abbaaaaaaaaabaaa
aaaaaaaaaaaabbaa
aaaaaacaaaaaaaaa
aaaaaaaaaaaaaaaa
aaabaaaaaaaaaaca
aaaaaaaaaaaaaaaa
""".split()


def sand(X, Y):
    ch = BLACK_SAND[Y % 16][X % 16]
    return c({"a": "k_bs2", "b": "k_bs1", "c": "k_bs3", "p": "k_wp1"}[ch])


def lava_rock(X, Y):
    ch = LAVA_ROCK[Y % 16][X % 16]
    return c({"a": "k_lr2", "b": "k_lr1", "c": "k_lr3", "k": "k_lr0"}[ch])


PEBBLE = """
................
..p.............
.pq......o......
..........q.....
................
......pp........
.....pqo........
..............p.
.............pq.
..q.............
................
........o.......
...p...pq.......
..pqo...........
................
...........q....
""".split()


def pebbles(X, Y):
    """Rim soil strewn with pumice and scoria pebbles (the ground's variant)."""
    ch = PEBBLE[Y % 16][X % 16]
    if ch == "p":
        return c("k_ag3")
    if ch == "q":
        return c("k_wp1")
    if ch == "o":
        return c("k_ag0")
    return soil(X, Y)


def basalt_flags(X, Y):
    """The quay: dressed black basalt slabs in offset courses."""
    x, y = X % 16, Y % 16
    off = 8 if (Y // 8) % 2 else 0
    if y % 8 == 0 or (x + off) % 16 == 0:
        return c("k_bs1")
    if y % 8 == 1 or (x + off) % 16 == 1:
        return c("k_bs3")
    return c("k_bs2") if hp8(X, Y, 31) > 12 else c("k_bs3")


def scrub(X, Y):
    x, y = X % 16, Y % 16
    # two dry thyme mounds per cell on ash
    for cx, cy in ((3, 4), (11, 3), (7, 10), (14, 11), (0, 11)):
        d = (x - cx) ** 2 + ((y - cy) * 1.25) ** 2
        if d < 16:
            return c("k_sc2") if (x - cx) + (y - cy) < -1 else c("k_sc1")
        if d < 21 and y > cy:
            return c("k_ag0")
    return soil(X, Y)


# --------------------------------------------------------------------------
# Strata: the color of a cliff at an altitude (px above the sea)
# --------------------------------------------------------------------------

# Thera's layers, bottom up: (altitude where the layer starts, its name)
LAYERS = [(0, "basalt"), (12, "basalt2"), (16, "scoria"), (26, "seam"), (29, "scoria2"),
          (42, "flow"), (47, "scoria3"), (52, "ochre"), (55, "pumice")]
PERIOD = 32       # the layer boundaries wander on a 2-cell period, so faces stay cheap


def _wave(b, X):
    """How far boundary b wanders up or down at column X (px)."""
    x = X % PERIOD
    import math
    v = (1.6 * math.sin(2 * math.pi * (x / PERIOD) + b * 1.7)
         + 0.9 * math.sin(4 * math.pi * (x / PERIOD) + b * 0.6))
    v += (hp(x, b * 3, 40) % 3) - 1 if b % 2 else 0
    return int(round(v))


_WAVES = [[_wave(b, x) for x in range(PERIOD)] for b in range(len(LAYERS))]


def strata(alt, X, Y):
    n = hp8(X, Y, 9)
    x8 = X % 8
    xp = X % PERIOD
    k = 0
    for b in range(len(LAYERS) - 1, -1, -1):
        if alt >= LAYERS[b][0] + (_WAVES[b][xp] if b else 0):
            k = b
            break
    name = LAYERS[k][1]
    top = (LAYERS[k + 1][0] + _WAVES[k + 1][xp]) if k + 1 < len(LAYERS) else 999
    bottom = LAYERS[k][0] + (_WAVES[k][xp] if k else 0)
    dt, db = top - 1 - alt, alt - bottom
    # each layer's top is a little ledge that catches the light; its underside is in shadow
    if name in ("basalt", "basalt2"):
        if dt == 0:
            return c("k_bk3")
        if x8 == 5 or (db == 0 and k):
            return c("k_bk0")
        if x8 == 4:
            return c("k_bk2")
        return c("k_bk1") if n > 25 else c("k_bk2")
    if name.startswith("scoria"):
        if dt == 0:
            return c("k_rd3") if name != "scoria3" else c("k_rd2")
        if db == 0:
            return c("k_rd0")
        if n < 9:
            return c("k_rd0")
        if n > 90 and name == "scoria2":
            return c("k_wp0")         # a pumice clast in the scoria
        if name == "scoria3":
            return c("k_rd1") if n > 30 else c("k_rd0")
        return c("k_rd2") if (alt + (xp // 8)) % 9 > 1 else c("k_rd1")
    if name == "seam":
        return c("k_fw") if dt == 0 else (c("k_wp0") if db == 0 or n < 15 else c("k_wp1"))
    if name == "flow":
        if dt == 0:
            return c("k_bk3")
        if db == 0:
            return c("ink")
        return c("k_bk1") if n > 25 else c("k_bk2")
    if name == "ochre":
        return c("k_och") if db else c("k_rd1")
    # the Minoan pumice: thick, white, cut into gullies by rain
    if db == 0:
        return c("k_wp0")
    if xp in (6, 22) and alt < 76:
        return c("k_wp0")
    if xp in (5, 21) and alt < 76:
        return c("k_fw")
    return c("k_wp1") if alt < 66 else c("k_wp2")


# --------------------------------------------------------------------------
# The painter
# --------------------------------------------------------------------------

class Canvas:
    def __init__(self):
        self.U = np.zeros((H * PX, W * PX, 4), np.uint8)   # under the player
        self.T = np.zeros((H * PX, W * PX, 4), np.uint8)   # over the player
        self.walk = [["."] * W for _ in range(H)]          # . X D G S W
        self.solid = np.zeros((H, W), bool)

    def px(self, layer, X, Y, rgb):
        a = self.U if layer == "U" else self.T
        if 0 <= X < W * PX and 0 <= Y < H * PX:
            if rgb is None:
                a[Y, X] = 0
            else:
                a[Y, X, :3] = rgb
                a[Y, X, 3] = 255

    def get(self, layer, X, Y):
        a = self.U if layer == "U" else self.T
        if a[Y, X, 3] == 0:
            return None
        return tuple(int(v) for v in a[Y, X, :3])

    def rect(self, layer, x0, y0, w, h, rgb):
        for Y in range(y0, y0 + h):
            for X in range(x0, x0 + w):
                self.px(layer, X, Y, rgb)

    def outline(self, layer, x0, y0, w, h, rgb=None):
        """1 px ink silhouette on the opaque pixels of a box of a layer."""
        a = self.U if layer == "U" else self.T
        sub = a[y0:y0 + h, x0:x0 + w, 3] > 0
        pad = np.pad(sub, 1)
        edge = sub & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        for yy, xx in zip(*np.nonzero(edge)):
            self.px(layer, x0 + xx, y0 + yy, rgb or c("ink"))

    def cell_solid(self, x, y, code="X"):
        self.walk[y][x] = code
        self.solid[y, x] = code == "X"


def _land_field():
    """Bilinear land occupancy of the shore level against the sea, for soft coasts."""
    occ = (LVL >= SHORE).astype(float)
    ys, xs = np.mgrid[0:H * PX, 0:W * PX]
    fx = (xs + 0.5) / PX - 0.5
    fy = (ys + 0.5) / PX - 0.5
    x0 = np.clip(np.floor(fx).astype(int), 0, W - 1)
    y0 = np.clip(np.floor(fy).astype(int), 0, H - 1)
    x1, y1 = np.clip(x0 + 1, 0, W - 1), np.clip(y0 + 1, 0, H - 1)
    tx, ty = np.clip(fx - x0, 0, 1), np.clip(fy - y0, 0, 1)
    f = (occ[y0, x0] * (1 - tx) * (1 - ty) + occ[y0, x1] * tx * (1 - ty)
         + occ[y1, x0] * (1 - tx) * ty + occ[y1, x1] * tx * ty)
    noise = np.vectorize(lambda X, Y: hp8(X, Y, 11))(xs, ys) / 96.0 - 0.5
    return f + noise * 0.22


def paint_ground(cv):
    field = _land_field()
    for y in range(H):
        for x in range(W):
            k, lv = KIND[y, x], LVL[y, x]
            for py in range(PX):
                for px_ in range(PX):
                    X, Y = x * PX + px_, y * PX + py
                    if lv == SEA:
                        f = field[Y, X]
                        if f > 0.5:
                            cv.px("U", X, Y, sand(X, Y) if _near_sand(x, y) else lava_rock(X, Y))
                        elif f > 0.4:
                            cv.px("U", X, Y, c("k_fw") if hp8(X, Y, 12) > 25 else c("k_kq"))
                        continue
                    if (x, y) in QUAY:
                        rgb = basalt_flags(X, Y)
                    elif k == "sand":
                        rgb = sand(X, Y)
                    elif k in ("islet", "mound"):
                        rgb = lava_rock(X, Y)
                    elif (x, y) in LANES:
                        rgb = paving(X, Y)
                    elif (x, y) in SCRUB:
                        rgb = scrub(X, Y)
                    elif (x, y) in PEBBLES:
                        rgb = pebbles(X, Y)
                    else:
                        rgb = soil(X, Y)
                    if lv == SHORE:
                        f = field[Y, X]
                        if f < 0.5:
                            rgb = c("k_fw") if (f > 0.4 and hp8(X, Y, 12) > 25) else (
                                c("k_kq") if f > 0.4 else None)
                        elif f < 0.58:
                            rgb = c("k_bs0") if k == "sand" else c("k_lr0")
                    cv.px("U", X, Y, rgb)
            if lv == SHORE and k == "sand":
                cv.walk[y][x] = "S"
            if (x, y) in SCRUB:
                cv.walk[y][x] = "G"
    _lane_edges(cv)


def _near_sand(x, y):
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            xx, yy = x + dx, y + dy
            if 0 <= xx < W and 0 <= yy < H and KIND[yy, xx] == "sand":
                return True
    return False


def _lane_edges(cv):
    """Worn edges where the whitewashed paving meets the ash: a 2 px kerb of grey
    joints and ash creeping onto the flags."""
    for (x, y) in LANES:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n in LANES or not (0 <= n[0] < W and 0 <= n[1] < H) or LVL[n[1], n[0]] < TERRACE:
                continue
            for i in range(PX):
                for d in range(2):
                    if dx == 1:
                        X, Y = x * PX + 15 - d, y * PX + i
                    elif dx == -1:
                        X, Y = x * PX + d, y * PX + i
                    elif dy == 1:
                        X, Y = x * PX + i, y * PX + 15 - d
                    else:
                        X, Y = x * PX + i, y * PX + d
                    if d == 0 or (i // 3) % 2 == 0:
                        cv.px("U", X, Y, c("k_cw2") if d == 1 else c("k_ag1"))


def paint_faces(cv):
    for (x, y), (hi, r, k, lo) in FACES.items():
        cv.cell_solid(x, y)
        temple = hi == TEMPLE
        for py in range(PX):
            for px_ in range(PX):
                X, Y = x * PX + px_, y * PX + py
                alt = ALT[hi] * PX - (r * PX + py) - 1
                if lo == SHORE and KIND[y, x] in ("islet", "mound"):
                    rgb = _basalt(X, Y, alt)
                elif temple:
                    rgb = _krepis(X, Y, py)
                else:
                    rgb = strata(alt, X, Y)
                rag = 0 if temple else (_WAVES[3][X % PERIOD] + 1) // 2 + 1
                if r == 0 and py < rag and not temple and lo != SHORE:
                    rgb = soil(X, Y) if KIND[y - 1, x] == "rim" else lava_rock(X, Y)
                elif r == 0 and py == rag and not temple:
                    rgb = c("k_bk1")
                elif r == 0 and py == rag + 1 and not temple:
                    rgb = c("k_fw")
                elif r == 0 and py == 0 and temple:
                    rgb = c("ink")
                if r == k - 1 and py >= 14 and lo == SEA:
                    rgb = c("k_fw") if hp8(X, Y, 14) > 30 else c("k_bk0")
                elif r == k - 1 and py == 15 and lo != SEA:
                    rgb = c("k_bk0")
                cv.px("U", X, Y, rgb)
        # the face's ends: an outer corner gets an ink edge, an inner one a shadow
        for side, dx in (("L", -1), ("R", 1)):
            nx = x + dx
            nb = FACES.get((nx, y)) if 0 <= nx < W else None
            if nb and nb[0] == hi:
                continue
            higher = 0 <= nx < W and LVL[y, nx] > lo and (nx, y) not in FACES
            for py in range(PX):
                X = x * PX + (0 if dx < 0 else 15)
                Y = y * PX + py
                if higher:
                    for d in range(3):
                        XX = X - d * dx
                        cur = cv.get("U", XX, Y)
                        cv.px("U", XX, Y, _darker(cur))
                else:
                    cv.px("U", X, Y, c("ink") if not temple else c("k_mw3"))
                    cv.px("U", X - dx, Y, _darker(cv.get("U", X - dx, Y)))


def _darker(rgb):
    ramps = [["k_wp2", "k_wp1", "k_wp0", "k_bk3"], ["k_fw", "k_wp1", "k_wp0"],
             ["k_rd3", "k_rd2", "k_rd1", "k_rd0", "k_bk1"], ["k_och", "k_rd1"],
             ["k_bk3", "k_bk2", "k_bk1", "k_bk0", "ink"], ["k_lr3", "k_lr2", "k_lr1", "k_lr0"],
             ["k_mw0", "k_mw1", "k_mw2", "k_mw3"], ["k_ag3", "k_ag2", "k_ag1", "k_ag0"],
             ["k_cw1", "k_cw2", "k_cw3"]]
    if rgb is None:
        return c("ink")
    for ramp in ramps:
        rr = [P[n] for n in ramp]
        if rgb in rr:
            i = rr.index(rgb)
            return rr[min(i + 1, len(rr) - 1)]
    return rgb


def _basalt(X, Y, alt):
    n = hp8(X, Y, 15)
    x = X % 8
    if x == 3:
        return c("k_lr0")
    if x == 2:
        return c("k_lr3") if alt > 16 else c("k_lr2")
    if n < 10:
        return c("k_lr0")
    return c("k_lr2") if alt > 20 else c("k_lr1")


def _krepis(X, Y, py):
    """The temple terrace's front: three marble steps."""
    step = py // 5
    top = py % 5 == 0
    if top:
        return c("k_mw0")
    if py % 5 == 4:
        return c("k_mw2")
    return c("k_mw1") if hp(X, Y, 16) > 12 else c("k_mw2")


def paint_edges(cv):
    """The rim's side and back edges where no face is drawn."""
    for y in range(H):
        for x in range(W):
            lv = LVL[y, x]
            if lv < TERRACE or (x, y) in FACES:
                continue
            # west and east sides
            for dx in (-1, 1):
                nx = x + dx
                if not (0 <= nx < W) or LVL[y, nx] >= lv or (nx, y) in FACES and FACES[(nx, y)][0] >= lv:
                    continue
                for py in range(PX):
                    for d in range(5):
                        X = x * PX + (d if dx < 0 else 15 - d)
                        Y = y * PX + py
                        if lv == TEMPLE:
                            rgb = (c("ink"), c("k_mw3"), c("k_mw2"), c("k_mw1"), None)[d]
                        elif KIND[y, x] == "mound":
                            rgb = (c("k_lr0"), c("k_lr1"), c("k_lr1"), c("k_lr3"), None)[d]
                        else:   # the lip: whitewash over the edge
                            rgb = (c("ink"), c("k_wp0"), c("k_wp2"), None, None)[d]
                        if rgb:
                            cv.px("U", X, Y, rgb)
                # the cliff's side, seen obliquely, drawn over the sea beside it
                if LVL[y, nx] == SEA and lv >= RIM and KIND[y, x] == "rim":
                    for py in range(PX):
                        Y = y * PX + py
                        band = (c("k_wp1"), c("k_wp1"), c("k_wp0"), c("k_rd2"), c("k_rd2"), c("k_rd1"),
                                c("k_rd1"), c("k_wp1"), c("k_rd2"), c("k_rd1"), c("k_bk1"), c("k_bk1"),
                                c("k_bk2"), c("k_rd0"), c("k_bk1"), c("k_bk0"))[py]
                        for d in range(7):
                            X = nx * PX + (15 - d if dx < 0 else d)
                            rgb = band
                            if d == 6:
                                rgb = c("ink")
                            elif d == 0:
                                rgb = _darker(band)
                            elif d >= 4 and py % 4 == 1:
                                rgb = _darker(band)
                            cv.px("U", X, Y, rgb)
            # the back (north) edge: a lip seen from above
            ny = y - 1
            if ny >= 0 and LVL[ny, x] < lv and (x, ny) not in FACES:
                for px_ in range(PX):
                    X = x * PX + px_
                    mound = KIND[y, x] == "mound"
                    cv.px("U", X, y * PX, c("k_lr0") if mound else c("ink"))
                    cv.px("U", X, y * PX + 1, c("k_lr1") if mound else (
                        c("k_bk2") if lv != TEMPLE else c("k_mw3")))
                    cv.px("U", X, y * PX + 2, c("k_lr3") if mound else (
                        c("k_wp2") if lv != TEMPLE else c("k_mw0")))
            # the town's white parapet along the lip above a face
            sy = y + 1
            if sy < H and (x, sy) in FACES and FACES[(x, sy)][0] == lv and lv in (RIM, TERRACE) \
                    and KIND[y, x] == "rim" and (x, sy) not in STAIRS:
                for px_ in range(PX):
                    X = x * PX + px_
                    cv.px("U", X, y * PX + 12, c("k_fw"))
                    cv.px("U", X, y * PX + 13, c("k_fw"))
                    cv.px("U", X, y * PX + 14, c("k_cw2"))
                    cv.px("U", X, y * PX + 15, c("k_cw3") if px_ % 8 else c("k_cw2"))


def paint_stairs(cv):
    for (x, y) in STAIRS:
        cv.walk[y][x] = "."
        cv.solid[y, x] = False
        info = FACES.get((x, y))
        temple = info and info[0] == TEMPLE
        mound = KIND[y, x] in ("islet", "mound")
        for py in range(PX):
            for px_ in range(PX):
                X, Y = x * PX + px_, y * PX + py
                tread = py % 4
                if temple:
                    rgb = (c("k_mw0"), c("k_mw1"), c("k_mw1"), c("k_mw2"))[tread]
                elif mound:
                    rgb = (c("k_lr3"), c("k_lr2"), c("k_lr2"), c("k_lr0"))[tread]
                else:
                    rgb = (c("k_fw"), c("k_cw1"), c("k_ag2"), c("k_cw3"))[tread]
                cv.px("U", X, Y, rgb)
        # parapets on the outer sides
        for dx in (-1, 1):
            if (x + dx, y) in STAIRS:
                continue
            X = x * PX + (0 if dx < 0 else 15)
            for py in range(PX):
                Y = y * PX + py
                if temple:
                    cv.px("U", X, Y, c("k_mw3"))
                elif mound:
                    cv.px("U", X, Y, c("k_lr0"))
                else:
                    cv.px("U", X, Y, c("k_cw3"))
                    cv.px("U", X - dx, Y, c("k_fw"))
                    cv.px("U", X - 2 * dx, Y, c("k_cw2"))


# --------------------------------------------------------------------------
# Buildings: Cycladic cubes in 3/4 view (flat roof seen from above, south face)
# --------------------------------------------------------------------------

def shadow(cv, x0, y0, w, h):
    """A soft cast shadow down and to the right, one value darker, on the ground."""
    for Y in range(y0 + 4, y0 + h + 6):
        for X in range(x0 + w, x0 + w + 6):
            if Y >= y0 + h and X >= x0 + w + 6 - (Y - y0 - h):
                continue
            cur = cv.get("U", X, Y) if 0 <= X < W * PX and 0 <= Y < H * PX else None
            if cur:
                cv.px("U", X, Y, _darker(cur))
    for X in range(x0 + 3, x0 + w + 6):
        for Y in range(y0 + h, y0 + h + 3):
            if X > x0 + w + 2 + (y0 + h + 3 - Y):
                continue
            cur = cv.get("U", X, Y) if 0 <= X < W * PX and 0 <= Y < H * PX else None
            if cur:
                cv.px("U", X, Y, _darker(cur))


def cube(cv, cx, cy, w, h, roof_rows=1, door=None, windows=(), dome=False, layer_top=True):
    """A whitewashed cube of w x h cells at cell (cx, cy). The first roof_rows are
    the flat roof seen from above (drawn over the player); the rest are the south
    wall. door is a cell column (relative) for a blue door in the bottom row."""
    x0, y0 = cx * PX, cy * PX
    Wp, Hp = w * PX, h * PX
    rh = roof_rows * PX - 4
    shadow(cv, x0, y0, Wp, Hp)
    L = "T" if layer_top else "U"
    # roof (top layer, so the player passes behind the cube's top edge)
    for Y in range(y0, y0 + rh):
        for X in range(x0, x0 + Wp):
            edge = Y - y0 < 2 or X - x0 < 2 or x0 + Wp - X <= 2
            rgb = c("k_fw") if (edge or hp(X, Y, 17) > 6) else c("k_cw1")
            if Y == y0 + rh - 1 or x0 + Wp - X == 1:
                rgb = c("k_cw2")
            cv.px(L, X, Y, rgb)
    # parapet lip, then the wall (lit, with a cooler shade toward the right)
    for Y in range(y0 + rh, y0 + Hp):
        for X in range(x0, x0 + Wp):
            u = (X - x0) / Wp
            if Y - (y0 + rh) < 2:
                rgb = c("k_cw2")
            elif u > 0.9:
                rgb = c("k_cw2")
            else:
                rgb = c("k_cw1") if hp(X, Y, 18) < 5 else c("k_fw")
            layer = L if Y < y0 + roof_rows * PX else "U"
            cv.px(layer, X, Y, rgb)
    # base: a grey plinth strip
    for X in range(x0, x0 + Wp):
        cv.px("U", X, y0 + Hp - 1, c("k_cw3"))
        cv.px("U", X, y0 + Hp - 2, c("k_cw2"))
    for (wx, wy) in windows:
        X, Y = x0 + wx, y0 + wy
        cv.rect("U", X, Y, 5, 6, c("k_ab0"))
        cv.rect("U", X + 1, Y + 1, 3, 4, c("k_ab1"))
        cv.px("U", X + 1, Y + 1, c("k_ab2"))
        cv.rect("U", X - 1, Y + 6, 7, 1, c("k_cw3"))
    if door is not None:
        X = x0 + door * PX + 3
        Y = y0 + Hp - 13
        cv.rect("U", X - 1, Y - 1, 12, 13, c("k_cw3"))
        cv.rect("U", X, Y, 10, 12, c("k_ab1"))
        for yy in range(Y, Y + 12):
            cv.px("U", X + 4, yy, c("k_ab0"))
            cv.px("U", X + 5, yy, c("k_ab0"))
        cv.rect("U", X + 1, Y + 1, 2, 10, c("k_ab2"))
        cv.px("U", X + 7, Y + 6, c("k_gold"))
        cv.px("U", X + 2, Y + 6, c("k_gold"))
    # silhouette outline in ink, on both layers
    cv.outline(L, x0, y0, Wp, roof_rows * PX)
    for Y in range(y0, y0 + Hp):
        cv.px("U" if Y >= y0 + roof_rows * PX else L, x0, Y, c("ink"))
        cv.px("U" if Y >= y0 + roof_rows * PX else L, x0 + Wp - 1, Y, c("ink"))
    for X in range(x0, x0 + Wp):
        cv.px("U", X, y0 + Hp - 1, c("ink"))
    for j in range(h):
        for i in range(w):
            cv.cell_solid(cx + i, cy + j)
    if door is not None:
        cv.cell_solid(cx + door, cy + h - 1, "D")
        cv.solid[cy + h - 1, cx + door] = False


def dome(cv, cx, cy, w):
    """A blue dome on a shrine's roof (islands' shrines only, STYLE §4.5)."""
    x0, y0 = cx * PX, cy * PX
    r = w * PX // 2 - 3
    mx = x0 + w * PX // 2
    base = y0 + PX - 2
    for Y in range(base - r, base + 1):
        for X in range(mx - r, mx + r):
            d = ((X + 0.5 - mx) / r) ** 2 + ((Y - base) / r) ** 2
            if d <= 1:
                u = (X - mx) / r
                v = (Y - base) / r
                if u + v * 0.7 < -0.75:
                    rgb = c("k_ab2")
                elif u < 0.35:
                    rgb = c("k_ab1")
                else:
                    rgb = c("k_ab0")
                cv.px("T", X, Y, rgb)
    cv.outline("T", mx - r - 1, base - r - 1, 2 * r + 2, r + 2)
    # a little gold finial
    cv.px("T", mx, base - r - 2, c("k_gold"))
    cv.px("T", mx, base - r - 3, c("k_gold"))
    cv.px("T", mx - 1, base - r - 1, c("ink"))
    cv.px("T", mx, base - r - 1, c("ink"))


def niche(cv, cx, cy):
    """An open niche with an oil lamp, in a shrine's bottom row (no door: not a house)."""
    X, Y = cx * PX + 4, cy * PX + 3
    cv.rect("U", X, Y, 8, 10, c("k_cw3"))
    cv.rect("U", X + 1, Y + 1, 6, 9, c("k_ab0"))
    cv.rect("U", X + 3, Y + 5, 2, 2, c("k_gold"))
    cv.px("U", X + 3, Y + 4, c("k_tc2"))


def plaque_rod(cv, cx, cy):
    """The rod of Asclepius over the Asclepeion's door: a red serpent on a staff."""
    X, Y = cx * PX + 4, cy * PX + 2
    cv.rect("U", X, Y, 9, 11, c("k_cw3"))
    cv.rect("U", X + 1, Y + 1, 7, 9, c("k_fw"))
    for yy in range(Y + 2, Y + 10):
        cv.px("U", X + 4, yy, c("k_ab0"))
    for i, (dx, dy) in enumerate(((5, 3), (3, 4), (5, 5), (3, 6), (5, 7), (3, 8))):
        cv.px("U", X + dx, Y + dy, c("k_tc1"))
        cv.px("U", X + dx + (1 if dx == 5 else -1), Y + dy, c("k_tc1"))


def awning(cv, cx, cy, w):
    """The Agora's striped market awning (blue and white) over its front."""
    x0, y0 = cx * PX, cy * PX + 8
    for X in range(x0 - 2, x0 + w * PX + 2):
        stripe = ((X - x0) // 4) % 2
        for Y in range(y0, y0 + 6):
            cv.px("U", X, Y, c("k_ab1") if stripe else c("k_fw"))
        cv.px("U", X, y0 + 6, c("k_ab0") if stripe else c("k_cw2"))
        cv.px("U", X, y0 - 1, c("ink"))
    for X in (x0 - 2, x0 + w * PX + 1):
        for Y in range(y0, y0 + 7):
            cv.px("U", X, Y, c("ink"))


def pithos(cv, X, Y):
    rows = ["  oo  ", " occo ", "oddddo", "oddcdo", "odddko", " okko ", "  oo  "]
    leg = {"o": c("ink"), "c": c("k_tc2"), "d": c("k_tc1"), "k": c("k_cw3")}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in leg:
                cv.px("U", X + i, Y + j, leg[ch])


def anvil(cv, cx, cy):
    X, Y = cx * PX + 2, cy * PX + 5
    rows = ["oooooooooooo", "osssssssssso", " ommmmmmmmo ", "   okkkko   ", "   okkkko   ",
            "  oookkooo  ", " omkkkkkkmo ", " oooooooooo "]
    leg = {"o": c("ink"), "s": c("k_cw1"), "m": c("k_cw3"), "k": c("k_cw2")}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in leg:
                cv.px("U", X + i, Y + j, leg[ch])
    cv.cell_solid(cx, cy)


def stele(cv, cx, cy, kind="rim"):
    """A carved sign stone."""
    X, Y = cx * PX + 3, cy * PX + 1
    face, side, dark = ((c("k_mw0"), c("k_mw1"), c("k_mw3")) if kind != "sand"
                        else (c("k_wp1"), c("k_wp0"), c("k_bk2")))
    for yy in range(Y, Y + 14):
        for xx in range(X, X + 10):
            rgb = face if xx < X + 7 else side
            if yy == Y + 13:
                rgb = dark
            cv.px("U", xx, yy, rgb)
    for yy in (Y + 4, Y + 7, Y + 10):
        cv.rect("U", X + 2, yy, 4, 1, dark)
    cv.outline("U", X - 1, Y - 1, 12, 16)
    for xx in range(X - 1, X + 11):
        cv.px("U", xx, Y - 1, c("ink"))
    cv.cell_solid(cx, cy)


def tripod(cv, cx, cy):
    """A bronze tripod-cauldron (Iliad 18), the forge god's votive, on a stone base."""
    X, Y = cx * PX + 1, cy * PX
    rows = ["              ",
            "   o      o   ",
            "  ol      lo  ",
            " oooooooooooo ",
            "oyllllllllllyo",
            "obbbbbbbbbbbdo",
            "obbbbbbbbbbddo",
            " obbbbbbbbddo ",
            "  oddddddddo  ",
            "  ob o  o bo  ",
            "  ob o  o bo  ",
            " ob  o  o  bo ",
            " ob  o  o  bo ",
            "ssssssssssssss",
            "osssssssssssso",
            " oooooooooooo "]
    leg = {"o": c("ink"), "l": c("k_gold"), "y": c("k_bz4"), "b": c("k_bz3"), "d": c("k_bz1"),
           "s": c("k_mw1")}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in leg:
                cv.px("U", X + i, Y + j, leg[ch])
    cv.cell_solid(cx, cy)

def bollard(cv, cx, cy):
    X, Y = cx * PX + 5, cy * PX + 4
    rows = [" oooo ", "ommmmo", "omllmo", "ommmmo", " okko ", " okko ", " oooo "]
    leg = {"o": c("ink"), "m": c("k_bs3"), "l": c("k_wp1"), "k": c("k_bs2")}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in leg:
                cv.px("U", X + i, Y + j, leg[ch])
    cv.cell_solid(cx, cy)


def quay(cv, x0, x1, y):
    """Dressed black stone along the port's waterline."""
    for x in range(x0, x1 + 1):
        for py in range(0, 6):
            for px_ in range(PX):
                X, Y = x * PX + px_, y * PX + py
                joint = py == 5 or (px_ + (4 if py > 2 else 0)) % 8 == 0
                rgb = c("k_bs3") if py == 0 else (c("k_bs0") if joint else c("k_bs2"))
                cv.px("U", X, Y, rgb)


# --------------------------------------------------------------------------
# The Temple of Hephaestus: Doric hexastyle on its krepis, painted
# --------------------------------------------------------------------------

def temple(cv, cx, cy):
    w, h = 7, 5
    x0, y0 = cx * PX, cy * PX
    Wp = w * PX
    mid = x0 + Wp // 2
    shadow(cv, x0, y0 + 8, Wp, h * PX - 8)
    # the cella's dark pronaos behind the columns
    for Y in range(y0 + 40, y0 + h * PX):
        for X in range(x0 + 4, x0 + Wp - 4):
            cv.px("U", X, Y, c("k_mw3") if Y < y0 + 44 else c("ink"))
    # bronze doors in the cella's back wall (at the warp cell)
    dX = (cx + 3) * PX + 2
    for Y in range(y0 + 50, y0 + h * PX):
        for X in range(dX, dX + 12):
            rgb = c("k_bz2") if (X - dX) in (1, 2, 7, 8) else c("k_bz1")
            if (Y - y0) % 6 == 0 and (X - dX) % 5 == 2:
                rgb = c("k_gold")
            if X - dX in (5, 6):
                rgb = c("k_wd0")
            cv.px("U", X, Y, rgb)
    # six Doric columns, fluted, light from the left
    cols = [x0 + i * 16 + 3 for i in (0, 1, 2, 4, 5, 6)]   # the wide middle bay frames the door
    for X0 in cols:
        for Y in range(y0 + 38, y0 + h * PX - 1):
            for dx in range(10):
                X = X0 + dx
                rgb = (c("k_mw1"), c("k_mw0"), c("k_mw0"), c("k_mw1"), c("k_mw0"),
                       c("k_mw1"), c("k_mw1"), c("k_mw2"), c("k_mw2"), c("k_mw3"))[dx]
                if dx in (0, 9):
                    rgb = c("ink")
                cv.px("U", X, Y, rgb)
        # echinus and abacus
        for dx in range(-2, 12):
            cv.px("U", X0 + dx, y0 + 36, c("ink"))
            cv.px("U", X0 + dx, y0 + 37, c("k_mw1") if dx < 8 else c("k_mw2"))
    # architrave and the painted triglyph frieze
    for Y in range(y0 + 24, y0 + 36):
        for X in range(x0, x0 + Wp):
            rel = Y - y0
            if rel < 26:
                rgb = c("k_mw2")
            elif rel < 31:          # frieze: triglyphs blue, metopes red
                k = (X - x0) % 16
                rgb = c("k_pb") if 5 <= k < 11 else c("k_pr")
                if k in (6, 9):
                    rgb = c("ink")
            elif rel < 32:
                rgb = c("k_gold")
            else:
                rgb = c("k_mw0") if rel < 34 else c("k_mw1")
            cv.px("U", X, Y, rgb)
    # the pediment (raking cornice), its tympanum painted red with a bronze hammer
    # and anvil, akroteria at the peak and corners
    for Y in range(y0, y0 + 24):
        half = (Y - y0 + 2) * (Wp // 2) / 26
        for X in range(int(mid - half), int(mid + half)):
            inner = abs(X - mid) < half - 4 and Y > y0 + 4
            rgb = c("k_pr") if inner else c("k_mw0")
            if Y >= y0 + 21:
                rgb = c("k_mw1")
            cv.px("T", X, Y, rgb)
    cv.outline("T", x0, y0, Wp, 24)
    # hammer and anvil in the tympanum
    ax, ay = mid - 8, y0 + 13
    for dx in range(16):
        cv.px("T", ax + dx, ay, c("k_bz3"))
        cv.px("T", ax + dx, ay + 1, c("k_bz2"))
    for dx in range(5, 11):
        for dy in range(2, 6):
            cv.px("T", ax + dx, ay + dy, c("k_bz1"))
    for dy in range(-6, 0):
        cv.px("T", ax + 12, ay + dy, c("k_wd2"))
    cv.rect("T", ax + 10, ay - 8, 6, 3, c("k_bz2"))
    # akroteria
    for (X, Y) in ((mid - 2, y0 - 0), (x0 + 1, y0 + 20), (x0 + Wp - 5, y0 + 20)):
        cv.rect("T", X, Y, 4, 3, c("k_gold"))
    # roof edge tiles behind the pediment (terracotta, seen above it)
    for Y in range(y0 + 20, y0 + 24):
        for X in range(x0, x0 + Wp):
            if cv.get("T", X, Y) is None:
                cv.px("T", X, Y, c("k_mw2"))
    cv.outline("U", x0, y0 + 24, Wp, h * PX - 24)
    for j in range(h):
        for i in range(w):
            cv.cell_solid(cx + i, cy + j)
    cv.cell_solid(cx + 3, cy + h - 1, "D")
    cv.solid[cy + h - 1, cx + 3] = False


# --------------------------------------------------------------------------
# The bronze man: an archaic kouros, unfinished, in his casting pit
# --------------------------------------------------------------------------

GIANT = (8, 3)        # top-left cell; 6 x 10 cells
GIANT_W, GIANT_H = 6, 10
PLINTH_ROW = 11       # map row where his feet and plinth begin (drawn under the player)


_GIANT_CACHE = {}


def _giant_pixels():
    if "px" not in _GIANT_CACHE:
        import kaldera_giant
        _GIANT_CACHE["px"] = kaldera_giant.native()
    return _GIANT_CACHE["px"]


def paint_giant(cv, frame=0, eyes=False):
    gx, gy = GIANT[0] * PX, GIANT[1] * PX
    plinth_y = (PLINTH_ROW - GIANT[1]) * PX     # local y where the plinth row begins
    px_, pmap = _giant_pixels()
    # the scaffold behind his left side: drawn first, so he stands in front of it
    scaffold(cv, gx, gy, plinth_y)
    for (x, y), name in px_.items():
        layer = "T" if y < plinth_y else "U"
        cv.px(layer, gx + x, gy + y, c(name))
    if eyes:
        for x, y in ((44, 15), (45, 15), (51, 15), (52, 15)):
            cv.px("T", gx + x, gy + y, c("k_lv3") if x in (45, 51) else c("k_lv2"))
    # the stepped plinth of dressed stone, standing in the casting pit
    lava = [c("k_lv0"), c("k_lv1"), c("k_lv2"), c("k_lv3")]
    for (X0, X1) in ((gx + 1, gx + 13), (gx + 82, gx + 94)):
        Y0, Y1 = gy + plinth_y + 6, gy + GIANT_H * PX - 1
        cxm, cym = (X0 + X1) / 2, (Y0 + Y1) / 2
        rx, ry = (X1 - X0) / 2, (Y1 - Y0) / 2
        for Y in range(Y0, Y1 + 1):
            for X in range(X0, X1 + 1):
                d = ((X - cxm) / rx) ** 2 + ((Y - cym) / ry) ** 2
                if d > 1:
                    continue
                if d > 0.7:
                    rgb = c("k_lr0") if d > 0.86 else c("k_rd0")     # the pit's crust
                else:
                    k = ((X + 2 * Y) // 3 + frame) % 4                # lava creeping down
                    rgb = lava[k] if k else c("k_lv1")
                cv.px("U", X, Y, rgb)
    steps = ((gx + 22, gx + 74, gy + plinth_y + 4, gy + plinth_y + 12),
             (gx + 15, gx + 81, gy + plinth_y + 12, gy + plinth_y + 22),
             (gx + 12, gx + 84, gy + plinth_y + 22, gy + GIANT_H * PX))
    for (X0, X1, Y0, Y1) in steps:
        for Y in range(Y0, Y1):
            for X in range(X0, X1):
                top = Y < Y0 + 3
                joint = (X - gx) % 16 == (8 if Y0 % 2 else 0) or Y == Y1 - 1
                if top:
                    rgb = c("k_bk3") if Y == Y0 else c("k_bk2")
                elif joint:
                    rgb = c("k_bk0")
                else:
                    rgb = c("k_bk2") if X < X0 + (X1 - X0) * 0.4 else c("k_bk1")
                if X in (X0, X1 - 1):
                    rgb = c("ink")
                cv.px("U", X, Y, rgb)
    # he stands on the top step: redraw his feet over it
    for (x, y), name in px_.items():
        if y >= plinth_y:
            cv.px("U", gx + x, gy + y, c(name))
    for x in range(GIANT_W):
        for y in range(PLINTH_ROW, GIANT[1] + GIANT_H):
            cv.cell_solid(GIANT[0] + x, y)


def scaffold(cv, gx, gy, plinth_y):
    """Timber poles lashed with rope, a working platform at his elbow, and on it
    the open two-part mold of the forearm that was never poured."""
    wood = (c("ink"), c("k_wd2"), c("k_wd1"), c("ink"))
    for X0 in (gx + 80, gx + 91):
        for Y in range(gy + 28, gy + plinth_y + 26):
            layer = "T" if Y < gy + plinth_y else "U"
            for d, rgb in enumerate(wood):
                cv.px(layer, X0 + d, Y, rgb)
    def beam(Y, X0, X1):
        layer = "T" if Y < gy + plinth_y else "U"
        for X in range(X0, X1):
            cv.px(layer, X, Y - 1, c("ink"))
            cv.px(layer, X, Y, c("k_wd3"))
            cv.px(layer, X, Y + 1, c("k_wd1"))
            cv.px(layer, X, Y + 2, c("ink"))
    for Y in (gy + 34, gy + 66, gy + 102):
        beam(Y, gx + 76, gx + 96)
    # diagonal braces
    for i in range(30):
        cv.px("T", gx + 82 + i * 9 // 30, gy + 70 + i, c("k_wd1"))
        cv.px("T", gx + 83 + i * 9 // 30, gy + 70 + i, c("k_wd2"))
    # rope lashings at the joints
    for X0 in (gx + 80, gx + 91):
        for Y in (gy + 34, gy + 66, gy + 102):
            for dy in (-1, 1, 3):
                cv.px("T", X0 + 1, Y + dy, c("k_wd3"))
                cv.px("T", X0 + 2, Y + dy, c("k_och") if False else c("k_wd3"))
    # a hoisting rope from the top beam, with a pulley block
    for Y in range(gy + 36, gy + 58):
        cv.px("T", gx + 87, Y, c("k_wd3"))
    cv.rect("T", gx + 85, gy + 36, 5, 4, c("k_wd1"))
    cv.px("T", gx + 87, gy + 37, c("ink"))
    # the open mold on the platform: two clay half-shells, the forearm's hollow in each
    for k, X0 in enumerate((gx + 76, gx + 86)):
        for Y in range(gy + 58, gy + 65):
            for X in range(X0, X0 + 9):
                edge = X in (X0, X0 + 8) or Y in (gy + 58, gy + 64)
                hollow = X0 + 2 <= X <= X0 + 6 and gy + 60 <= Y <= gy + 62
                rgb = c("ink") if edge else (c("k_rd0") if hollow else
                                             (c("k_rd2") if X < X0 + 4 else c("k_rd1")))
                cv.px("T", X, Y, rgb)


def forge_mouth(cv):
    """The Telchines' forge: a basalt arch in the mound's face, embers inside."""
    x, y = FORGE_DOOR
    X0, Y0 = x * PX - 4, (y - 1) * PX + 4
    for Y in range(Y0, (y + 1) * PX):
        for X in range(X0, X0 + 24):
            dx = X - (X0 + 12)
            top = Y0 + 4 + int(abs(dx) ** 2 / 12)
            if Y < top:
                continue
            inner = abs(dx) < 7 and Y > top + 3
            if inner:
                k = hp(X, Y, 23)
                rgb = c("k_lr0") if Y < (y + 1) * PX - 5 or k > 40 else (
                    c("k_lv0") if k > 15 else c("k_lv1"))
            else:
                rgb = c("k_lr3") if dx < 0 else c("k_lr2")
                if (Y - Y0) % 6 == 0:
                    rgb = c("k_lr0")
            cv.px("U", X, Y, rgb)
    # bronze nails in the lintel
    for dx in (-6, 0, 6):
        cv.px("U", X0 + 12 + dx, Y0 + 6, c("k_lv2"))
    cv.cell_solid(x, y, "D")
    cv.solid[y, x] = False


def akrotiri(cv):
    """The ash cliff: Akrotiri's buried house shows through, a fresco wall of
    swallows and lilies, and its Minoan door (STYLE §4.8: fallen, half-buried,
    weathered darker than a living temple)."""
    dx, dy = AKROTIRI_DOOR
    # ashlar wall emerging from the ash, x 22-25 across both face rows
    for y in (dy - 1, dy):
        for x in range(22, 26):
            for py in range(PX):
                for px_ in range(PX):
                    X, Y = x * PX + px_, y * PX + py
                    buried = Y < (dy - 1) * PX + 5 + (3 if x in (22, 25) else 0) + (hp(X, 0, 24) % 3)
                    if buried:
                        rgb = c("k_ag2") if hp(X, Y, 25) > 20 else c("k_ag1")
                    else:
                        joint = (Y % 8 == 0) or ((X + (4 if (Y // 8) % 2 else 0)) % 12 == 0)
                        rgb = c("k_rw0") if joint else (c("k_rw2") if hp(X, Y, 26) < 30 else c("k_rw1"))
                    cv.px("U", X, Y, rgb)
    # the fresco panel: a swallow over red lilies on a cream ground
    fX, fY = 22 * PX + 4, (dy - 1) * PX + 10
    cv.rect("U", fX - 1, fY - 1, 26, 15, c("k_rw0"))
    cv.rect("U", fX, fY, 24, 13, c("k_ag3"))
    for (lx, ly) in ((3, 8), (9, 9), (15, 8), (20, 9)):
        for j in range(4):
            cv.px("U", fX + lx, fY + ly + j, c("k_moss"))
        cv.px("U", fX + lx - 1, fY + ly - 1, c("k_frr"))
        cv.px("U", fX + lx + 1, fY + ly - 1, c("k_frr"))
        cv.px("U", fX + lx, fY + ly - 2, c("k_frr"))
    sw = ["k    k", "kk  kk", " kbbk ", "  kk  "]
    for j, row in enumerate(sw):
        for i, ch in enumerate(row):
            if ch == "k":
                cv.px("U", fX + 8 + i, fY + 2 + j, c("ink"))
            elif ch == "b":
                cv.px("U", fX + 8 + i, fY + 2 + j, c("k_frb"))
    # a band of blue along the top, broken where the ash fell
    for X in range(fX, fX + 24):
        if hp(X, 3, 27) > 25:
            cv.px("U", X, fY, c("k_frb"))
    # the Minoan door: a timber-framed opening, its lintel carved with horns
    X0, Y0 = dx * PX + 2, (dy - 1) * PX + 8
    cv.rect("U", X0, Y0, 12, 2, c("k_bz1"))
    cv.rect("U", X0, Y0 + 2, 12, 22, c("k_rw0"))
    cv.rect("U", X0 + 2, Y0 + 3, 8, 21, c("ink"))
    cv.px("U", X0 + 2, Y0 - 1, c("k_rw2"))
    cv.px("U", X0 + 9, Y0 - 1, c("k_rw2"))
    cv.px("U", X0 + 3, Y0 - 2, c("k_rw2"))
    cv.px("U", X0 + 8, Y0 - 2, c("k_rw2"))
    # the doorway can be stood in once the seal is cleaved; the niche behind it
    # stays solid (an item ball sits in it), so the door never opens a way up the cliff
    cv.walk[dy][dx] = "."
    cv.solid[dy, dx] = False


def ruins(cv):
    """Fallen column drums and a broken pithos on the port's sand (ruins kit)."""
    for i, (x, y) in enumerate(((8, 33), (9, 33), (10, 34))):
        X, Y = x * PX + 2 + (i % 2) * 2, y * PX + 3
        for yy in range(Y, Y + 10):
            for xx in range(X, X + 12):
                d = ((xx - X - 6) / 6) ** 2 + ((yy - Y - 5) / 5) ** 2
                if d <= 1:
                    rgb = c("k_rw2") if xx - X < 4 else c("k_rw1") if xx - X < 9 else c("k_rw0")
                    if abs(xx - X - 6) == 2 and d < 0.6:
                        rgb = c("k_rw0")
                    cv.px("U", xx, yy, rgb)
        cv.outline("U", X - 1, Y - 1, 14, 12)
        cv.cell_solid(x, y)


KOULOURA = """
................
.....bbssbb.....
...bssbsbssb....
..bsbbbbbbsbb...
..bbscccccsbb...
.bsbc.....cbsb..
.bsbc.....cbsbo.
.bbsbc...cbbsbo.
..bbssbsbsbbbo..
..obbsbbbsbbo...
...oobbbbboo....
.....oooooo.....
................
................
................
................
""".split()


def vineyard(cv, cells):
    """Santorini's koulouri: vines trained low into baskets against the wind."""
    leg = {"b": c("k_sc1"), "s": c("k_sc2"), "c": c("k_ag0"), "o": c("k_ag1")}
    for (x, y) in cells:
        for j, row in enumerate(KOULOURA):
            for i, ch in enumerate(row):
                if ch in leg:
                    cv.px("U", x * PX + i, y * PX + j + 1, leg[ch])
        cv.cell_solid(x, y)


KAIKI = """
................................
................................
...........o..........o.........
..........oo..........oo........
.oooooooooommmmmmmmmmmmmooooooo.
oqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqo
oqwwoqqqqqqqqqqqqqqqqqqqqqqqqqqo
oqwkwqqqqqqqqqqqqqqqqqqqqqqqqqo.
.orrrrrrrrrrrrrrrrrrrrrrrrrrrro.
.obbbbbbbbbbbbbbbbbbbbbbbbbbbbo.
..obbbbbbbbbbbbbbbbbbbbbbbbbbo..
...oooooooooooooooooooooooooo...
....ssssssssssssssssssssssss....
................................
................................
................................
""".split()


def kaiki(cv, x, y):
    """A fishing boat drawn up on the sand: blue hull, red strake, an eye at the bow."""
    leg = {"o": c("ink"), "q": c("k_pb"), "w": c("k_mw0"), "k": c("ink"), "r": c("k_pr"),
           "b": c("k_wd1"), "m": c("k_wd2"), "s": c("k_mw3")}
    for j, row in enumerate(KAIKI):
        for i, ch in enumerate(row):
            if ch in leg:
                cv.px("U", x * PX + i, y * PX + j, leg[ch])
    cv.cell_solid(x, y)
    cv.cell_solid(x + 1, y)


def fumarole(cv, x, y):
    """A vent in Nea Kameni's rock: sulphur-red earth and a breath of steam."""
    for py in range(PX):
        for px_ in range(PX):
            X, Y = x * PX + px_, y * PX + py
            d = ((px_ - 8) ** 2 + ((py - 10) * 1.4) ** 2) ** 0.5
            if d < 3:
                cv.px("U", X, Y, c("k_lr0"))
            elif d < 5:
                cv.px("U", X, Y, c("k_rd0"))
            elif d < 7.5 and hp(X, Y, 30) > 30:
                cv.px("U", X, Y, c("k_rd1"))
    for (sx, sy) in ((7, 2), (8, 3), (9, 1), (6, 4), (8, 5), (10, 4), (7, 6), (9, 6), (8, 7)):
        cv.px("U", x * PX + sx, y * PX + sy, c("k_smk"))
    cv.cell_solid(x, y)


def nets(cv, cells):
    """Nets spread to dry on the black sand (walkable)."""
    for (x, y) in cells:
        for py in range(2, 14):
            for px_ in range(1, 15):
                if (px_ + py) % 4 == 0 or (px_ - py) % 4 == 0:
                    cv.px("U", x * PX + px_, y * PX + py, c("k_wp1") if py % 2 else c("k_ag1"))
        for px_ in range(1, 15):
            cv.px("U", x * PX + px_, y * PX + 13, c("k_bs0"))


def wall(cv, x0, x1, y):
    """A low whitewashed courtyard wall, seen from above and the south."""
    for x in range(x0, x1 + 1):
        for py in range(5, 16):
            for px_ in range(PX):
                X, Y = x * PX + px_, y * PX + py
                if py == 5:
                    rgb = c("ink")
                elif py < 8:
                    rgb = c("k_fw")
                elif py < 13:
                    rgb = c("k_cw2") if (px_ + (4 if py > 10 else 0)) % 8 == 0 else c("k_cw1")
                elif py == 13:
                    rgb = c("ink")
                else:
                    rgb = c("k_ag1")
                cv.px("U", X, Y, rgb)
        for py in range(5, 14):
            if x == x0:
                cv.px("U", x * PX, y * PX + py, c("ink"))
            if x == x1:
                cv.px("U", x * PX + 15, y * PX + py, c("ink"))
                cv.px("U", x * PX + 14, y * PX + py, c("k_cw2"))
        cv.cell_solid(x, y)


BOULDER = """
................
................
.....oooooo.....
...ooppqqqpoo...
..oppqqqqqqrpo..
..opqqqqqqqrro..
.oppqqqqqqrrrro.
.opqqqqqqrrrrro.
.oprrqqqrrrrrro.
..orrrrrrrrrso..
..ooorrrrrssoo..
....oooooooo....
.....tttttt.....
................
................
................
""".split()


def boulder(cv, x, y):
    """A pumice block thrown out by the old eruption."""
    leg = {"o": c("ink"), "p": c("k_wp2"), "q": c("k_wp1"), "r": c("k_wp0"), "s": c("k_bk3"),
           "t": c("k_ag1")}
    for j, row in enumerate(BOULDER):
        for i, ch in enumerate(row):
            if ch in leg:
                cv.px("U", x * PX + i, y * PX + j, leg[ch])
    cv.cell_solid(x, y)


# --------------------------------------------------------------------------
# Everything
# --------------------------------------------------------------------------

BUILDINGS = {
    "Asclepeion": dict(x=34, y=7, w=5, h=4, door=2),
    "Agora": dict(x=26, y=13, w=4, h=3, door=2),
    "SmithsHouse": dict(x=35, y=15, w=3, h=3, door=1),
}
TEMPLE_AT = (27, 0)
SHRINES = [(24, 9), (11, 0)]


def door_cell(name):
    b = BUILDINGS[name]
    return b["x"] + b["door"], b["y"] + b["h"] - 1


def paint(frame=0, eyes=False):
    cv = Canvas()
    paint_ground(cv)
    paint_faces(cv)
    paint_edges(cv)
    paint_stairs(cv)
    # the town
    b = BUILDINGS["Asclepeion"]
    cube(cv, b["x"], b["y"], b["w"], b["h"], door=b["door"],
         windows=((8, 22), (24, 22), (56, 22), (8, 40), (56, 40)))
    plaque_rod(cv, b["x"] + 2, b["y"] + 2)
    b = BUILDINGS["Agora"]
    cube(cv, b["x"], b["y"], b["w"], b["h"], door=b["door"], windows=((8, 20), (40, 20)))
    awning(cv, b["x"], b["y"] + 1, b["w"])
    for X, Y in ((25 * PX + 4, 15 * PX + 6), (30 * PX + 2, 15 * PX + 6)):
        pithos(cv, X, Y)
    cv.cell_solid(25, 15)
    cv.cell_solid(30, 15)
    b = BUILDINGS["SmithsHouse"]
    cube(cv, b["x"], b["y"], b["w"], b["h"], door=b["door"], windows=((30, 20),))
    anvil(cv, 38, 17)
    for sx, sy in SHRINES:
        cube(cv, sx, sy, 2, 3, roof_rows=1)
        dome(cv, sx, sy, 2)
        niche(cv, sx, sy + 2)
    temple(cv, *TEMPLE_AT)
    tripod(cv, 28, 7)
    tripod(cv, 33, 7)
    stele(cv, 26, 6)             # the temple's sign
    for X, Y in ((37 * PX + 4, 12 * PX + 4), (38 * PX + 4, 12 * PX + 6)):
        pithos(cv, X, Y)
    cv.cell_solid(37, 12)
    cv.cell_solid(38, 12)
    # koulouri on the rim and the south slope, a courtyard wall, pumice blocks
    vines = {(x, y) for y in (37, 38) for x in range(1, 28) if (x + y) % 2 == 0}
    vines |= {(x, y) for y in (17, 19, 21) for x in range(24, 30) if (x + y) % 2 == 0
              and x >= _rim_east(y) + 1}
    vines |= {(x, y) for y in (0, 2) for x in range(36, 39) if (x + y) % 2 == 0}
    vineyard(cv, vines)
    wall(cv, 33, 38, 14)
    for bx, by in ((5, 37), (19, 1), (38, 23), (23, 37), (36, 38)):
        boulder(cv, bx, by)
    # the port
    quay(cv, 14, 21, 30)
    bollard(cv, 15, 30)
    bollard(cv, 20, 30)
    stele(cv, 21, 33, "sand")    # KALDERA
    kaiki(cv, 7, 31)
    nets(cv, [(11, 35), (12, 35), (13, 35)])
    pithos(cv, 14 * PX + 1, 32 * PX + 6)
    pithos(cv, 14 * PX + 8, 32 * PX + 4)
    cv.cell_solid(14, 32)
    ruins(cv)
    akrotiri(cv)
    # the islet
    paint_giant(cv, frame, eyes)
    forge_mouth(cv)
    stele(cv, 9, 16, "sand")     # the forge's sign
    fumarole(cv, 7, 19)
    fumarole(cv, 15, 17)
    # the sea: cells that are mostly water are water
    for y in range(H):
        for x in range(W):
            if LVL[y, x] == SEA and (x, y) not in FACES:
                sub = cv.U[y * PX:(y + 1) * PX, x * PX:(x + 1) * PX, 3]
                if (sub == 0).mean() > 0.5:
                    cv.walk[y][x] = "W"
                    cv.solid[y, x] = False
                else:
                    cv.cell_solid(x, y)
    return cv


SIGNS = {"Sign": (21, 33), "ForgeSign": (9, 16), "TempleSign": (26, 6), "Plinth": (10, 12)}
