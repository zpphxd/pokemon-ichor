"""Acrocorinth, the Isthmian sanctuary and the city's workshops (gTileset_Emporion).

Acrocorinth: the great limestone crag over the city, with its fortified walls
and towers on the skyline. A band three rows tall: the walls on the crest, then
two rows of cliff. It repeats east to west; a gate with a rock-cut stair climbs
through it.

The Isthmian sanctuary of Poseidon: the stadium's stone starting line with its
gate posts, a victor's pine wreath on its post, and Poseidon's altar. Its pines
are aethos's stone pines.

The workshops: the bronze-smith's forge, his anvil and helmets; the potter's
beehive kiln and his rack of black-figure vases drying; the perfumer's shelf
of aryballoi; and the shipwright's hull on the stocks.
"""
from __future__ import annotations

import math

import emporion_lib as E
from emporion_lib import Struct, finish
from emporion_port import WOODK

# ==========================================================================
# Acrocorinth
# ==========================================================================

ROCK = {"k": "ink", "K": "sk", "0": "s0", "1": "s1", "2": "s2", "3": "s3", "4": "s4", "5": "s5",
        "o": "ol1", "O": "ol2", "w": "wt0", "W": "wt1"}

# cliff faces 16 px square, light from the top left: facets lit on their upper
# left, cracks and shadows lower right. Two, so a long cliff doesn't repeat
# every cell; each repeats down the cliff.
FACE_A = [
    "4433221K34433221",
    "4332211K43322110",
    "3322110K3322111K",
    "322110KK322110KK",
    "22110K0K221100K0",
    "1100KK0K1100KK0K",
    "KKKK0K00KK0KK0KK",
    "34433221K3443322",
    "4433221104433221",
    "433221110K332211",
    "33221100K0322110",
    "322110KK0K22110K",
    "22110K0K0K1100KK",
    "1100KKK0KK00KK0K",
    "0KKK0KK0KKKK0KK0",
    "K34433221K344332",
]
FACE_B = [
    "221110K3443322o1",
    "11100K34433221O1",
    "1100K3443322110o",
    "00KK34433221110K",
    "KK0K4332211100KK",
    "0K0K33221100KK0K",
    "KK0K2211KKK0KK0K",
    "3443322K34433221",
    "443322104433221K",
    "43322110K332211K",
    "33221100K32211KK",
    "3221100KK22110K0",
    "2211KK0K0K1100KK",
    "1100K0KK0KKK0K0K",
    "oKKK0K0KK0KKK0KK",
    "O34433221K344332",
]
PLATEAU = ["OO3oO2O3", "3Oo2O32O", "o3O2oO3O", "2O3O2o3O"]


def _rock_sites(seed, n):
    """Boulder centres on a 16 x 32 torus (two cell-rows of cliff, repeating
    every 16 px across), from a fixed seed so the art never changes by itself."""
    import random
    rnd = random.Random(seed)
    sites = []
    for k in range(n):
        sites.append((rnd.uniform(0, 16), (k + rnd.uniform(0.1, 0.9)) * 32 / n,
                      rnd.uniform(0.85, 1.25)))
    return sites


SITES = {"A": _rock_sites(7, 7), "B": _rock_sites(23, 6)}


def _face(L, x0, y0, w, h, pat):
    """A cliff face of limestone boulders and facets, light from the top left:
    a Voronoi field on a 16 x 32 torus (so it repeats every 16 px across and its
    two rows differ). Each facet is lit where it faces up and left and shadowed
    where it faces down and right; dark crevices part them. pat: FACE_A or
    FACE_B, two different fields to alternate along a long cliff."""
    sites = SITES["B" if pat is FACE_B else "A"]
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = (x - x0) % 16 + 0.5, (y - y0) % 32 + 0.5
            best = []
            for (sx, sy, k) in sites:
                for ox in (-16, 0, 16):
                    for oy in (-32, 0, 32):
                        dx, dy = X - (sx + ox), (Y - (sy + oy)) * 1.35
                        best.append(((dx * dx + dy * dy) ** 0.5 * k, dx, dy))
            best.sort()
            d1, dx, dy = best[0]
            d2 = best[1][0]
            if d2 - d1 < 0.9:
                c = "sk" if d2 - d1 < 0.45 else "s0"
            else:
                lit = -(dx * 0.6 + dy * 0.8)      # facing the light up and left
                c = ("s5" if lit > 3.2 else "s4" if lit > 1.2 else "s3" if lit > -1.2
                     else "s2" if lit > -3.2 else "s1")
            L.px(x, y, c)
    if pat is FACE_B:
        # a tuft of scrub clinging in a crevice
        for (dx, dy, c) in ((3, 20, "ol2"), (4, 20, "ol1"), (3, 21, "ol1"), (11, 9, "ol2"),
                            (12, 9, "ol1")):
            for xx in range(x0, x0 + w, 16):
                L.px(xx + dx, y0 + dy, c)


def _wall_row(L, x0, w, tower=False, gate=False):
    """The crest (y 0-15): the plateau's scrub at the top, a curtain wall with
    battlements, its foot on the cliff."""
    for y in range(0, 4):
        for x in range(x0, x0 + w):
            L.px(x, y, ROCK[PLATEAU[y][x % 8]])
    top = 1 if tower else 4
    for x in range(x0, x0 + w):
        X = (x - x0) % 4
        if X < 2:
            L.px(x, top, "s5")
            L.px(x, top + 1, "s4")
        else:
            L.px(x, top, "wt0")
            L.px(x, top + 1, "wt0")
        L.px(x, top + 2, "s4")
    for x in range(x0, x0 + w):
        for y in range(top + 3, 13):
            X, Y = (x - x0) % 16, y - top - 3
            c = "s3"
            if Y % 4 == 3 or (X + (8 if (Y // 4) % 2 else 0)) % 8 == 0:
                c = "s1"
            elif Y % 4 == 0:
                c = "s4"
            L.px(x, y, c)
        L.px(x, 13, "s1")
        L.px(x, 14, "s0")
        L.px(x, 15, "sk")
    if tower:
        L.vline(x0, top, 13, "ink")
        L.vline(x0 + w - 1, top, 13, "ink")
        L.vline(x0 + 1, top + 2, 12, "s5")
        L.vline(x0 + w - 2, top + 2, 12, "s1")
        L.rect(x0 + 7, 7, 2, 5, "ink")
    if gate:
        L.blit(["   kkkkkkkk   ", "  k44444444k  ", " k4kkkkkkkk4k ", "k4kkkkkkkkkk4k",
                "k4kkkkkkkkkk4k", "k4kkkkkkkkkk4k", "k4kkkkkkkkkk4k", "k4kkkkkkkkkk4k",
                "k4kkkkkkkkkk4k"], {"k": "ink", "4": "s4"}, x0 + 1, 7)


def acrocorinth():
    s = Struct("acrocorinth", "Acrocorinth: the crag and its fortified crest", 6, 3,
               walk=["XXXX.X", "XXXX.X", "XXXX.X"], ground="none",
               notes="The great crag over the city with walls on its skyline, a band three "
                     "rows tall that runs east-west: row 0 the crest (curtain wall and "
                     "battlements, the plateau's scrub above), rows 1-2 the cliff. Columns: (0) "
                     "the west end, (1) run A, (2) run B (alternate them), (3) a tower, (4) "
                     "the gate, a rock-cut stair climbing to it through the cliff (walkable), "
                     "(5) the east end. Put the map's highest ground above row 0, and grass or "
                     "rock beside the ends.")
    L = s.B
    W = 96
    _face(L, 0, 16, W, 32, FACE_A)
    _face(L, 32, 16, 16, 32, FACE_B)
    _wall_row(L, 0, W)
    _wall_row(L, 48, 16, tower=True)
    _wall_row(L, 64, 16, gate=True)
    for y in range(16, 48):
        for x in range(66, 78):
            k = (y - 16) % 4
            L.px(x, y, "s4" if k == 0 else "s3" if k == 1 else "s2" if k == 2 else "s1")
        L.px(65, y, "ink")
        L.px(78, y, "ink")
        L.px(64, y, "s1")
        L.px(79, y, "s4")
    # the ends: the crag's flank turns away, lit on the west, in shadow on the east
    for y in range(0, 48):
        L.px(0, y, "ink")
        L.px(1, y, "s5")
        L.px(2, y, "s4")
        L.px(W - 1, y, "ink")
        L.px(W - 2, y, "sk")
        L.px(W - 3, y, "s0")
    return finish(s)


# ==========================================================================
# The Isthmian sanctuary
# ==========================================================================

def starting_line():
    s = Struct("balbis", "The Isthmian stadium's starting line", 3, 1, walk=["X.X"],
               ground="path",
               notes="The stone starting sill (balbis) laid across the stadium track, two "
                     "grooves for the runners' toes, with the starting gate's posts at the "
                     "ends and a cord between them. On aethos path (0x1D9): (0) west post, "
                     "(1) the sill, repeat it across the track (walkable), (2) east post.")
    M = s.M
    for x in range(0, 48):
        M.px(x, 6, "s5")
        M.px(x, 7, "s4")
        M.px(x, 8, "sk" if x % 16 not in (0, 15) else "s4")
        M.px(x, 9, "s3")
        M.px(x, 10, "sk" if x % 16 not in (0, 15) else "s3")
        M.px(x, 11, "s2")
        M.px(x, 12, "s1")
    for x in range(7, 48, 16):
        M.px(x, 7, "s1")
        M.px(x + 1, 7, "s1")
    for x0 in (2, 44):
        M.blit(["kk", "15", "14", "14", "14", "13", "13", "13", "13", "13", "12", "kk"],
               {"k": "ink", "5": "s5", "4": "s4", "3": "s3", "2": "s2", "1": "s1"}, x0, 1)
    for x in range(4, 44):
        M.px(x, 3 + (1 if 12 < x < 36 else 0), "w0")
    return finish(s)


def wreath_post():
    s = Struct("wreath_post", "A victor's pine wreath on its post", 1, 2, walk=["T", "X"],
               ground="grass",
               notes="Isthmian victors were crowned with pine. A wreath of pine hangs on a "
                     "carved post. On aethos grass; the top cell draws over the player.")
    T, M = s.T, s.M
    for y in range(3, 16):
        T.px(7, y, "tk0")
        T.px(8, y, "tk1")
    T.blit([" kk ", "k11k", " kk "], {"k": "ink", "1": "tk1"}, 6, 1)
    for a in range(0, 360, 12):
        x = 7.5 + 5 * math.cos(math.radians(a))
        y = 10 + 4.5 * math.sin(math.radians(a))
        T.px(int(round(x)), int(round(y)), "c3" if a > 180 else "c2")
        T.px(int(round(7.5 + 4 * math.cos(math.radians(a)))), int(round(y)), "c1")
    T.px(7, 15, "tc1")
    T.px(8, 15, "tc2")
    for y in range(16, 29):
        M.px(7, y, "tk0")
        M.px(8, y, "tk1")
        M.px(6, y, "ink")
        M.px(9, y, "ink")
    M.rect(4, 28, 8, 3, "tk1")
    M.hline(4, 11, 31, "ink")
    M.hline(3, 12, 28, "ink")
    return finish(s)


def altar_poseidon():
    s = Struct("altar_poseidon", "Altar of Isthmian Poseidon", 2, 2, walk=["XX", "XX"],
               ground="grass",
               notes="A long marble altar with dolphins leaping across its face, a fire on "
                     "it, and Poseidon's gilded trident at its back. On aethos grass.")
    M = s.M
    M.rect(2, 12, 28, 16, "m1")
    M.hline(2, 29, 12, "w0")
    M.hline(2, 29, 13, "w0")
    M.hline(2, 29, 15, "m3")
    M.rect(2, 16, 28, 10, "m2")
    M.hline(2, 29, 26, "m4")
    E.outline_rect(M, 1, 11, 30, 18, "ink")
    M.blit(["  kkk  ", " kb11bk", "kb1bbk ", " kk kk "], {"k": "ink", "b": "b1", "1": "b2"}, 6, 18)
    E.mirror_half(M, 0, 32, 11, 32)
    M.vline(15, 0, 11, "g0")
    M.vline(16, 0, 11, "br")
    M.blit(["k k k", "g g g", "ggggg"], {"k": "ink", "g": "g1"}, 13, 0)
    M.blit([" rr ", "rgGr", "kkkk"], {"r": "rd", "g": "g0", "G": "g1", "k": "ink"}, 6, 8)
    return finish(s)


# ==========================================================================
# Workshops
# ==========================================================================

def forge():
    s = Struct("forge", "The bronze-smith's forge", 2, 2, walk=["XX", "XX"], ground="quay",
               notes="A brick forge under a hood, its charcoal glowing, with the leather "
                     "bellows at its side. On yard paving (the quay's poros).")
    M = s.M
    M.blit([
        "        kkkkkkkk        ",
        "        k011110k        ",
        "        k011110k        ",
        "       kk011110kk       ",
        "      k1111111111k      ",
        "    kk111111111111kk    ",
        "   k1111111111111111k   ",
        "  k000000000000000000k  ",
    ], {"k": "ink", "0": "wd0", "1": "wd1"}, 4, 4)
    for y in range(0, 4):
        M.px(16 + (y % 2), y, "rp")
    M.rect(5, 12, 22, 16, "wd1")
    for y in range(12, 28):
        for x in range(5, 27):
            if (y % 4 == 3) or ((x + (4 if (y // 4) % 2 else 0)) % 8 == 0):
                M.px(x, y, "wd0")
    M.rect(10, 16, 12, 7, "ink")
    for x in range(11, 21):
        M.px(x, 21, "fl" if x % 2 else "rd")
        M.px(x, 20, "g1" if x % 3 == 0 else "fl")
    E.flame(M, 13, 15)
    M.px(15, 18, "fc")
    E.outline_rect(M, 4, 11, 24, 18, "ink")
    M.blit([" kkkk ", "k3221k", "k2211k", " k11k ", "  kk  "], WOODK, 25, 20)
    return finish(s)


def smith_props():
    s = Struct("smith_props", "Anvil, and a rack of Corinthian helmets", 2, 1, walk=["XX"],
               ground="quay",
               notes="(0) an anvil on its block with a hammer; (1) a rack of Corinthian "
                     "helmets, the city's famous bronze. On yard paving.")
    M = s.M
    M.blit([
        "  kkkkkkkkk ",
        " k00000000wk",
        "kkkkk000kkk ",
        "    k00k    ",
        "   kk11kk   ",
        "  k111111k  ",
        "  k100001k  ",
        "  kkkkkkkk  ",
    ], {"k": "ink", "0": "wd0", "1": "wd1", "w": "w0"}, 1, 5)
    M.blit(["kk", "k2", "k1"], WOODK, 12, 3)
    M.hline(17, 30, 2, "ink")
    M.hline(17, 30, 3, "wd2")
    M.hline(17, 30, 12, "wd2")
    M.hline(17, 30, 13, "ink")
    M.vline(17, 2, 15, "ink")
    M.vline(30, 2, 15, "ink")
    helm = [" kkkk ", "kGggzk", "kgkkgk", "kgk kz", "kg  gk", " k  k "]
    M.blit(helm, WOODK, 18, 5)
    M.blit(helm, WOODK, 24, 5)
    return finish(s)


def kiln():
    s = Struct("kiln", "The potter's kiln", 2, 2, walk=["XX", "XX"], ground="quay",
               notes="A beehive kiln of clay, smoke from its vent, fire showing at its "
                     "stoking mouth. On yard paving.")
    M = s.M
    m = E.ellipse_mask(26, 26)
    E.fill_mask(M, m, 3, 5, "tc1")
    for y in range(5, 31):
        for x in range(3, 29):
            if M.get(x, y) == "tc1":
                if x < 12 and y < 16:
                    M.px(x, y, "tc2")
                elif x > 21 or y > 24:
                    M.px(x, y, "tc0")
                if x % 8 == 4 and y % 4 == 0:
                    M.px(x, y, "tc0")
    E.silhouette_outline(M, (0, 0, 32, 32), "ink")
    M.rect(3, 26, 26, 5, "tc0")
    M.hline(3, 28, 31, "ink")
    M.blit(["kkkk", "k  k"], {"k": "ink"}, 14, 4)
    for y in range(0, 4):
        M.px(15 + (y % 2), y, "sl3")
        M.px(16 - (y % 2), y, "w0" if y < 2 else "sl3")
    M.blit([" kkkkk ", "kssfssk", "ksfwfsk", "krrrrrk"], {"k": "ink", "s": "rd", "f": "sf",
                                                         "w": "sf2", "r": "tc0"}, 12, 22)
    return finish(s)


def vase_rack():
    s = Struct("vase_rack", "A rack of black-figure vases drying", 2, 1, walk=["XX"],
               ground="quay",
               notes="The potter's new pots drying in the sun: jugs and amphorae with "
                     "Corinth's black-figure animal friezes. On yard paving.")
    M = s.M
    M.hline(1, 30, 2, "ink")
    M.hline(1, 30, 3, "wd2")
    M.hline(1, 30, 13, "wd2")
    M.hline(1, 30, 14, "ink")
    M.vline(1, 2, 15, "ink")
    M.vline(30, 2, 15, "ink")
    for i, x in enumerate((3, 9, 16, 22)):
        if i % 2:
            M.blit([" kk ", "k22k", "kkkk", "k22k", " kk "], {"k": "ink", "2": "tc2"}, x, 7)
        else:
            M.blit(["  k  ", " k2k ", "k2k2k", "kk2kk", " k2k ", "  k  "],
                   {"k": "ink", "2": "tc2"}, x, 6)
    return finish(s)


def perfumer():
    s = Struct("perfumer", "The perfumer's shelf", 2, 1, walk=["XX"], ground="quay",
               notes="Shelves of aryballoi, Corinth's little round perfume flasks, in "
                     "painted clay, over baskets of roses and irises. On yard paving.")
    M = s.M
    M.hline(1, 30, 1, "ink")
    M.hline(1, 30, 2, "wd2")
    M.hline(1, 30, 8, "wd2")
    M.hline(1, 30, 9, "ink")
    M.vline(1, 1, 14, "ink")
    M.vline(30, 1, 14, "ink")
    for i, c in enumerate(("tc2", "pu1", "sf", "w0", "tc2", "pu1", "sf")):
        M.blit([" k ", "kck", " k "], {"k": "ink", "c": c}, 3 + i * 4, 5)
    for x0, c in ((4, "rd"), (17, "pu1")):
        M.blit(["k1k1k1k", "1k1k1k1", "kwwwwwk", " kkkkk "], {"k": "ink", "1": c, "w": "wd2"}, x0, 10)
    return finish(s)


def hull_stocks():
    s = Struct("hull_stocks", "The shipwright's hull on the stocks", 3, 2,
               walk=["XXX", "XXX"], ground="quay",
               notes="A merchant hull half built on its keel blocks: keel and posts laid, the "
                     "ribs standing bare, the first strakes planked at the stern. Bow to the "
                     "east. On yard paving.")
    M = s.M
    for x in (6, 22, 38):
        M.rect(x, 26, 6, 4, "wd1")
        E.outline_rect(M, x - 1, 25, 8, 6, "ink")
    M.rect(4, 22, 40, 3, "wd2")
    M.hline(4, 43, 22, "wd3")
    M.hline(3, 44, 25, "ink")
    M.hline(3, 44, 21, "ink")
    for i in range(14):
        M.px(42 + i // 4, 21 - i, "wd2")
        M.px(43 + i // 4, 21 - i, "ink")
        M.px(5 - i // 5, 21 - i, "wd2")
        M.px(4 - i // 5, 21 - i, "ink")
    for x in range(20, 41, 4):
        for k in range(14):
            M.px(x - k // 6, 21 - k, "wd3")
            M.px(x + 1 - k // 6, 21 - k, "wd1")
    for y in range(9, 21):
        for x in range(6, 18 - (21 - y) // 3):
            M.px(x, y, "wd2" if y % 3 else "wd1")
    M.line(6, 9, 16, 6, "ink")
    return finish(s)


def timber():
    s = Struct("timber", "Shipwright's timber and a sawhorse", 2, 1, walk=["XX"], ground="quay",
               notes="A stack of sawn pine planks and a sawhorse with a saw. On yard paving.")
    M = s.M
    for k in range(4):
        y = 4 + k * 3
        M.rect(1, y, 18, 3, "wd3" if k % 2 else "wd2")
        M.hline(1, 18, y + 2, "wd1")
        M.px(0, y, "ink")
        M.px(0, y + 1, "ink")
        M.px(19, y + 1, "wd1")
    M.hline(1, 18, 3, "ink")
    M.hline(1, 18, 16, "ink")
    M.blit(["kkkkkkkkk", "k3333333k", " k1   k1 ", "k1     k1"], WOODK, 21, 7)
    M.blit(["kkk", "rrr"], {"k": "ink", "r": "rp"}, 24, 5)
    return finish(s)


CHARIOT_LEG = {"k": "ink", "r": "rd", "f": "fl", "g": "g0", "G": "g1", "0": "wd0", "1": "wd1",
               "2": "wd2", "3": "wd3", "w": "fc"}
CHARIOT_CAR = [
    "..........kkkk..................",
    ".........kGGGGk.................",
    "........kGwfffGkk...............",
    "........kGfrrrrfGGkk............",
    "........kGfrrrrrrrfGGk..........",
    "........kGfrrrrrrrrrrfGk........",
    "........kGfrgggrrrrrrrrGk.......",
    "........kGfrrrrgggrrrrrrGk......",
    "........kGfrrrrrrrgggrrrrk......",
    "........kGfrrrrrrrrrrgggrk......",
    "........kGfrrrrrrrrrrrrrrk......",
    "........kGfrrrrrrrrrrrrrrk......",
    "........k3222222222222222k......",
    "........k1111111111111111k......",
    ".........kkkkkkkkkkkkkkkk.......",
]


def chariot():
    s = Struct("chariot", "Alfred's chariot on show", 2, 2, walk=["XX", "XX"], ground="path",
               notes="A light two-wheeled racing chariot, its car painted red with a gold "
                     "rim, parked with its pole resting on the yoke: the one Alfred builds "
                     "and sells. In the wheelwright's dirt yard.")
    M = s.M
    M.blit(CHARIOT_CAR, CHARIOT_LEG, 0, 6)
    # the pole, from under the car's front down to the yoke on the ground
    # the wheel over the car's back: rim, six spokes, a gold hub
    cx, cy, R = 20, 22, 7
    for y in range(cy - R - 1, cy + R + 2):
        for x in range(cx - R - 1, cx + R + 2):
            d = math.hypot(x - cx, y - cy)
            if R - 1.2 <= d <= R + 0.6:
                lit = (x - cx) + (y - cy) < 0
                M.px(x, y, "wd2" if lit else "wd1")
            elif R + 0.6 < d <= R + 1.5:
                M.px(x, y, "ink")
    for a in range(0, 360, 60):
        r = math.radians(a + 15)
        for t in range(2, R - 1):
            M.px(round(cx + t * math.cos(r)), round(cy + t * math.sin(r)), "wd3")
    M.blit([".k.", "kGk", ".k."], CHARIOT_LEG, cx - 1, cy - 1)
    E.silhouette_outline(M, (0, 0, 32, 32), "ink")
    # the pole goes on after the outline, as Gen 3 draws thin props: from under
    # the car's front down to the yoke resting on the ground
    for i in range(11):
        x, y = 9 - i, 20 + (i * 6) // 10
        M.px(x, y, "wd3"); M.px(x, y + 1, "wd1"); M.px(x, y + 2, "ink")
    M.blit(["kkk", "kGk", "k1k", "k1k", "kkk"], CHARIOT_LEG, 0, 23)
    return finish(s)


def build_city():
    return [acrocorinth(), forge(), smith_props(), kiln(), vase_rack(), perfumer(), chariot()]


def build_shipwright():
    return [hull_stocks(), timber()]


def build_isthmia():
    return [starting_line(), wreath_post(), altar_poseidon()]
