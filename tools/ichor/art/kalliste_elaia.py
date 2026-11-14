"""Elaia Village structures: Cycladic houses, the blue-domed shrine, the festival
square (paving, altar, Klotheia garland posts), dry-stone walls, terraces and
the olive-press shed. Drawn into kalliste_lib Structs; see kalliste_build.py.
"""
from __future__ import annotations

import math

from kalliste_lib import Struct
from kalliste_parts import (CHIMNEY, CHIMNEY_KEY, POT, POT_KEY, SMALL_WINDOW, WINDOW_KEY,
                            door, doric_column, facade, flat_roof, flagstones,
                            joints, paint_flagstones, shade_stones, voronoi_labels, window)

SEC = "elaia"


# --------------------------------------------------------------------------
# Houses
# --------------------------------------------------------------------------

def house_small():
    s = Struct("house_small", "Small Cycladic house", 4, 3, SEC,
               walk=["XXXX", "XXXX", "XDXX"],
               notes="Whitewashed cube with a flat parapet roof, a Cycladic chimney, "
                     "an Aegean-blue door and shuttered window, and a basil pot. "
                     "Door at the bottom row, second column: put the warp there.")
    L = s.B
    flat_roof(L, 0, 0, 64, 17)
    facade(L, 0, 17, 64, 31)
    L.blit(CHIMNEY, CHIMNEY_KEY, 48, 2)
    door(L, 18, 26)
    window(L, 41, 23)
    L.blit(POT, POT_KEY, 4, 37)
    return s


def house_two_story():
    s = Struct("house_large", "Two-story Cycladic house with an outside stair", 5, 5, SEC,
               walk=["XXXXX", "XXXXX", "XXXXX", "XXXXX", "XDXXX"],
               notes="Two floors under one flat roof. A whitewashed outside stair climbs "
                     "the front from the right corner to a landing at the blue upper door. "
                     "Only the ground-floor door (bottom row, second column) is a warp; the "
                     "upper door and the stair are scenery.")
    L = s.B
    flat_roof(L, 0, 0, 80, 17)
    facade(L, 0, 17, 80, 63)
    L.blit(CHIMNEY, CHIMNEY_KEY, 8, 2)
    L.blit(CHIMNEY, CHIMNEY_KEY, 64, 2)
    # upper floor: two shuttered windows and the upper door
    window(L, 9, 23)
    window(L, 57, 23)
    door(L, 34, 26, step=False)

    # landing in front of the upper door, carried on a solid whitewashed pier
    lx0, lx1 = 30, 50
    L.hline(lx0, lx1, 45, "w3")            # shade where it meets the wall
    L.rect(lx0, 46, lx1 - lx0 + 1, 2, "w0")  # its top
    L.hline(lx0, lx1, 48, "w2")
    L.rect(lx0, 49, lx1 - lx0 + 1, 31, "w0")
    L.vline(lx0, 45, 79, "dk")
    L.vline(lx0 + 1, 49, 78, "w1")
    L.hline(lx0, lx1, 79, "w4")
    # a small arched store under the landing
    arch = [
        "  kkkk  ",
        " kdddd3 ",
        "kdddddd3",
        "kdddddd3",
        "kdddddd3",
        "kdddddd3",
        "kdddddd3",
        "kdddddd3",
        "kdddddd3",
        "kdddddd3",
        "kddtTdd3",
        "kdttTTd3",
    ]
    L.blit(arch, {"k": "dk", "d": "w4", "3": "w2", "t": "tc1", "T": "tc2"}, 37, 66)
    L.hline(37, 44, 78, "w3")

    # the stair: 4 px steps running down to the right-hand corner
    def profile(x):
        return 49 + 4 * ((x - 51) // 4)
    for x in range(51, 80):
        p = profile(x)
        # treads, seen from above against the wall
        L.vline(x, p - 4, p - 1, "w0")
        L.px(x, p - 5, "w3")              # where the treads meet the wall
        # the stair's cast shade on the wall just above the treads
        L.px(x, p - 6, "w2")
        L.px(x, p - 7, "w2")
        # the front face of the stair down to the ground
        L.vline(x, p, 79, "w0")
        L.px(x, p, "dk")
    for k in range(8):
        x = 51 + 4 * k
        if x > 79:
            break
        p = profile(x)
        L.vline(x, p - 4, p - 1, "w2")    # step edges
        L.vline(x, p - 4 + 4, p - 1 + 4, "dk") if x > 51 else None
    # risers drawn as the vertical part of the outline profile
    for k in range(1, 8):
        x = 51 + 4 * k
        if x > 79:
            break
        L.vline(x, profile(x) - 4, profile(x), "dk")
    L.vline(51, 45, 49, "dk")
    L.hline(51, 79, 79, "w4")
    L.vline(79, 49, 79, "dk")
    # pots of geranium on two steps
    small_pot = [
        " gGg ",
        "gGrGg",
        "kkkkk",
        "kTTtk",
        " ktk ",
    ]
    key = {"g": "ol1", "G": "ol2", "r": "tc1", "k": "ink", "T": "tc2", "t": "tc1"}
    L.blit(small_pot, key, 56, profile(56) - 8)
    L.blit(small_pot, key, 68, profile(68) - 8)
    # ground floor: the main door, a small window and a pot
    door(L, 18, 58)
    L.blit(SMALL_WINDOW, WINDOW_KEY, 6, 59)
    L.blit(POT, POT_KEY, 4, 69)
    return s


def shrine():
    s = Struct("shrine_dome", "Blue-domed shrine with a columned porch", 5, 5, SEC,
               walk=["XXXXX", "XXXXX", "XXXXX", "XXXXX", "XXDXX"],
               notes="A whitewashed chapel-shrine: Aegean-blue dome on a windowed drum, "
                     "a porch of four white Doric columns under a meander frieze, and a "
                     "blue door on two steps. Door: bottom row, middle column.")
    L = s.B
    flat_roof(L, 0, 0, 80, 40)
    # dome on its drum, centered on the middle column
    cx = 40
    # drum
    L.rect(25, 26, 31, 9, "w1")
    L.vline(25, 26, 34, "dk")
    L.vline(55, 26, 34, "dk")
    L.vline(26, 26, 34, "w0")
    L.vline(54, 26, 34, "w2")
    L.hline(25, 55, 35, "dk")
    L.hline(26, 54, 34, "w2")
    for wx in (29, 38, 47):
        L.rect(wx, 28, 4, 5, "dk")
        L.hline(wx, wx + 3, 28, "b0")
        L.px(wx, 29, "b1")
    # hemisphere: shaded from the top left, with a bright sheen
    rx, ry, base = 17, 21, 27
    for y in range(base - ry, base + 1):
        for x in range(cx - rx, cx + rx + 1):
            nx, ny = (x - cx) / (rx + 0.5), (y - base) / (ry + 0.5)
            if nx * nx + ny * ny > 1.0:
                continue
            nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
            lum = -0.55 * nx - 0.35 * ny + 0.75 * nz
            c = "b0" if lum < 0.15 else "b1" if lum < 0.62 else "b2" if lum < 0.86 else "b3"
            L.px(x, y, c)
    # silhouette outline
    for y in range(base - ry - 1, base + 1):
        for x in range(cx - rx - 1, cx + rx + 2):
            inside = lambda xx, yy: ((xx - cx) / (rx + 0.5)) ** 2 + ((yy - base) / (ry + 0.5)) ** 2 <= 1 and yy <= base
            if not inside(x, y) and any(inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                L.px(x, y, "ink")
    L.hline(cx - rx, cx + rx, base, "b0")
    # finial: a small white lantern with a gilt-free knob
    fin = [
        " k ",
        "kwk",
        " k ",
        "kwk",
        "k1k",
        "k1k",
    ]
    L.blit(fin, {"k": "dk", "w": "w0", "1": "w1"}, cx - 1, 1)
    # porch roof edge and meander frieze
    L.hline(1, 78, 40, "w0")
    meander = [
        "#####.##",
        "....#.#.",
        ".####.#.",
        ".#....#.",
        ".######.",
    ]
    L.rect(1, 41, 78, 5, "w0")
    L.pattern(meander, {"#": "b1"}, 2, 41, 76, 5, ox=2, oy=41)
    L.hline(1, 78, 46, "w0")
    L.hline(1, 78, 47, "w3")
    L.vline(0, 40, 79, "dk")
    L.vline(79, 40, 79, "dk")
    # porch: shaded back wall, door, columns
    L.rect(1, 48, 78, 26, "w3")
    L.rect(1, 48, 78, 2, "w4")
    door(L, 34, 54, step=False)
    ramp = ["w4", "w3", "w1", "w0", "w0"]
    for c in (8, 24, 56, 72):
        doric_column(L, c - 4, 48, 9, 26, ramp, "dk", fluted=False)
    # stylobate and two steps across the front
    L.hline(1, 78, 74, "w0")
    L.hline(1, 78, 75, "w2")
    L.hline(1, 78, 76, "w3")
    L.hline(1, 78, 77, "w0")
    L.hline(1, 78, 78, "w2")
    L.hline(0, 79, 79, "w4")
    return s


# --------------------------------------------------------------------------
# Festival square
# --------------------------------------------------------------------------

def paving():
    s = Struct("paving", "Festival-square paving: Cycladic flagstones in whitewashed lime", 4, 3, SEC,
               walk=["....", "....", "...."],
               notes="Slate flagstones set in white lime, one 16 px pattern so any piece "
                     "joins any other. Layout: NW, N, NE, plain / W, plain, E, plain / SW, "
                     "S, SE, plain. The curb faces down on the south edge. "
                     "Also good for Akti's streets.")
    L = s.B
    for cy in range(3):
        for cx in range(4):
            paint_flagstones(L, cx * 16, cy * 16, 16, 16)

    def north(x, y):
        L.hline(x, x + 15, y, "w2")
        L.hline(x, x + 15, y + 1, "w0")
        L.hline(x, x + 15, y + 2, "w0")
        L.hline(x, x + 15, y + 3, "pj1")

    def south(x, y):
        L.hline(x, x + 15, y + 11, "pj1")
        L.hline(x, x + 15, y + 12, "w0")
        L.hline(x, x + 15, y + 13, "w0")
        L.hline(x, x + 15, y + 14, "w2")
        L.hline(x, x + 15, y + 15, "w3")

    def west(x, y, y0=0, y1=15):
        L.vline(x, y + y0, y + y1, "w2")
        L.vline(x + 1, y + y0, y + y1, "w0")
        L.vline(x + 2, y + y0, y + y1, "w0")
        L.vline(x + 3, y + y0, y + y1, "pj1")

    def east(x, y, y0=0, y1=15):
        L.vline(x + 12, y + y0, y + y1, "pj1")
        L.vline(x + 13, y + y0, y + y1, "w0")
        L.vline(x + 14, y + y0, y + y1, "w0")
        L.vline(x + 15, y + y0, y + y1, "w2")

    # row 0: NW, N, NE
    north(0, 0); west(0, 0, 1)
    north(16, 0)
    north(32, 0); east(32, 0, 1)
    # row 1: W, B, E
    west(0, 16)
    east(32, 16)
    # row 2: SW, S, SE (the curb's face shows on the south side)
    west(0, 32, 0, 12); south(0, 32)
    south(16, 32)
    east(32, 32, 0, 12); south(32, 32)
    return s


def paving_inner():
    s = Struct("paving_inner", "Festival-square paving: inner corners", 2, 2, SEC,
               walk=["..", ".."],
               notes="Concave corners for L-shaped squares: NW, NE / SW, SE. Each has "
                     "the curb only in the one corner it names.")
    L = s.B
    for cy in range(2):
        for cx in range(2):
            paint_flagstones(L, cx * 16, cy * 16, 16, 16)
    corner = ["2", "0", "0", "j"]
    cols = {"2": "w2", "0": "w0", "j": "pj1"}
    # a small curb return in each corner
    for (ox, oy, fx, fy) in ((0, 0, 1, 1), (16, 0, -1, 1), (0, 16, 1, -1), (16, 16, -1, -1)):
        bx = ox if fx == 1 else ox + 15
        by = oy if fy == 1 else oy + 15
        for i, ch in enumerate(corner):
            for j in range(4 - i):
                L.px(bx + fx * i, by + fy * j, cols[ch])
                L.px(bx + fx * j, by + fy * i, cols[ch])
    return s


def altar():
    s = Struct("altar_square", "Festival altar of the Klotheia", 2, 2, SEC,
               walk=["XX", "XX"],
               notes="A marble altar with volute bolsters, a painted meander and a bronze "
                     "fire-bowl, standing on the square's flagstones. Two layers: paving "
                     "below, the altar over it.")
    B, M = s.B, s.M
    paint_flagstones(B, 0, 0, 32, 32)
    # plinth
    M.rect(3, 26, 26, 4, "m2")
    M.hline(3, 28, 26, "m1")
    M.hline(3, 28, 29, "m4")
    M.vline(2, 26, 29, "ink")
    M.vline(29, 26, 29, "ink")
    M.hline(2, 29, 30, "ink")
    # body
    M.rect(5, 12, 22, 14, "m1")
    M.vline(5, 12, 25, "ink")
    M.vline(26, 12, 25, "ink")
    M.vline(6, 12, 25, "w0")
    M.vline(25, 12, 25, "m3")
    M.hline(6, 25, 25, "m3")
    # painted meander band and a garland relief
    M.rect(6, 13, 20, 4, "tc1")
    M.pattern(["##.#", "..#.", "###.", "...."], {"#": "tc0"}, 6, 13, 20, 4, ox=6, oy=13)
    M.hline(6, 25, 17, "m3")
    for x in range(8, 24):
        dy = int(round(2.5 * math.sin(math.pi * (x - 8) / 15)))
        M.px(x, 19 + dy, "m4")
        M.px(x, 20 + dy, "m3")
    for x in (8, 15, 23):
        M.blit([" o ", "omo", " o "], {"o": "m4", "m": "m2"}, x - 1, 18)
    # top slab with volute bolsters
    M.rect(4, 7, 24, 5, "m1")
    M.hline(4, 27, 7, "ink")
    M.hline(5, 26, 8, "w0")
    M.hline(4, 27, 11, "m3")
    M.vline(3, 7, 11, "ink")
    M.vline(28, 7, 11, "ink")
    vol = [
        " kkk ",
        "kwm3k",
        "km4mk",
        "k3m3k",
        " kkk ",
    ]
    vk = {"k": "ink", "w": "w0", "m": "m1", "3": "m3", "4": "m4"}
    M.blit(vol, vk, 2, 6)
    M.blit(vol, vk, 25, 6)
    # bronze fire-bowl and flame
    bowl = [
        "kkkkkkkkkk",
        "kGggggggbk",
        " kGgggbbk ",
        "  kkbbkk  ",
        "   kbbk   ",
    ]
    M.blit(bowl, {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 11, 5)
    flame = [
        "    f     ",
        "   ff  f  ",
        "  ffcf ff ",
        "  fccff f ",
        " ffccyff  ",
        " fcyyycf  ",
    ]
    M.blit(flame, {"f": "fl", "c": "g1", "y": "fc"}, 11, 0)
    return s


def garland_posts():
    s = Struct("klotheia_posts", "Klotheia garland posts", 5, 2, SEC,
               walk=["TTTTT", "X.X.X"],
               notes="Thread-wrapped posts for the festival, with spindle-whorl tops and "
                     "garlands of olive, myrtle and flowers. Top row (drawn over the "
                     "player): post top with garland both sides, garland swag, post top "
                     "garland left only, post top garland right only, post top bare. "
                     "Bottom row: post base, plain paving, post base, plain paving, post "
                     "base. Place a post top above every base; swags go between post tops.")
    B, M, T = s.B, s.M, s.T
    paint_flagstones(B, 0, 0, 80, 32)
    key = {"k": "ink", "w": "w0", "t": "tc3", "L": "wd2", "d": "wd1", "r": "rd", "g": "g1",
           "G": "g0"}
    # a distaff: a head of white wool wound with red thread, on a plain pole
    top = [
        "      kkkk      ",
        "     kwwwwk     ",
        "    kwwwwwtk    ",
        "    kwrrwttk    ",
        "   kwwwwrrttk   ",
        "   kwwwwwtrrk   ",
        "   kwwrrwtttk   ",
        "    kwwwrrtk    ",
        "    rkwwtttkg   ",
        "    r kkkkk g   ",
        "   r  kLdk  g   ",
        "   r  kLdk   g  ",
        "    r kLdk   g  ",
        "    r kgGk  g   ",
        "   r  kLdk  g   ",
        "   r  kLdk   g  ",
    ]
    base = [
        "    r kLdk   g  ",
        "     rkLdk  g   ",
        "      kLdk      ",
        "      kLdk      ",
        "      krrk      ",
        "      kLdk      ",
        "      kLdk      ",
        "      kLdk      ",
        "      kLdk      ",
        "      kLdk      ",
        "      kLdk      ",
        "    kkLLddkk    ",
        "   kLLLddddk    ",
        "    kkkkkkk     ",
    ]

    def post_top(x, left, right):
        # garland stubs end at the cell edges at y 6, where every swag starts
        if left:
            garland(T, x, x + 4, 6, 0)
        if right:
            garland(T, x + 12, x + 15, 6, 0)
        T.blit(top, key, x, 0)

    def post_base(x):
        y0 = 16
        M.blit(base, key, x, y0)

    # top row: both sides, swag, left only, right only, bare
    post_top(0, True, True)
    garland(T, 16, 31, 6, 5)
    post_top(32, True, False)
    post_top(48, False, True)
    post_top(64, False, False)
    post_base(0)
    post_base(32)
    post_base(64)
    return s


def garland(L, x0, x1, y0, sag):
    """A swag of olive and myrtle with white and gold flowers, from x0 to x1."""
    n = max(1, x1 - x0)
    for x in range(x0, x1 + 1):
        if not (0 <= x < L.w):
            continue
        t = (x - x0) / n
        y = y0 + int(round(sag * 4 * t * (1 - t)))
        L.px(x, y - 2, "ink")
        L.px(x, y - 1, "ol3" if x % 2 else "ol2")
        L.px(x, y, "ol2" if x % 3 else "ol1")
        L.px(x, y + 1, "ol1")
        L.px(x, y + 2, "ink")
        if x % 5 == 1:
            L.px(x, y, "w0")
            L.px(x, y - 1, "w0")
        elif x % 5 == 3:
            L.px(x, y, "g1")
        elif x % 5 == 4:
            L.px(x, y + 1, "rd")


# --------------------------------------------------------------------------
# Dry-stone walls and terraces (group "stone")
# --------------------------------------------------------------------------

WALL_SEEDS = [(2, 2), (7, 3), (12, 2), (4, 7), (10, 7), (15, 8), (1, 9), (7, 10)]
_WL = voronoi_labels(16, 11, WALL_SEEDS, stretch=(0.75, 1.0))
_WJ = joints(_WL)
_WALL_FACE = shade_stones(_WL, _WJ, ["s2", "s3", "e2", "s2", "s3", "s2", "e2", "s3"],
                          {"s2": "s3", "s3": "s4", "e2": "s3"}, {"s2": "s1", "s3": "s2", "e2": "e1"})

CAP_SEEDS = [(3, 3), (10, 2), (14, 6), (6, 9), (12, 12), (2, 13), (8, 15)]
_CL = voronoi_labels(16, 16, CAP_SEEDS)
_CJ = joints(_CL)
_CAPS = shade_stones(_CL, _CJ, ["s4", "s5", "s4", "s4", "s5", "s4", "s5"],
                     {"s4": "s5"}, {"s4": "s3", "s5": "s4"})


def wall_face(L, x, y, h=11):
    for j in range(h):
        for i in range(16):
            c = _WALL_FACE[j % 11, i]
            L.px(x + i, y + j, c if c else "sk")


def wall_caps_row(L, x, y):
    """Whitewashed capstones seen edge-on: the top of a wall running east-west."""
    L.hline(x, x + 15, y, "s3")
    L.hline(x, x + 15, y + 1, "s5")
    L.hline(x, x + 15, y + 2, "s5")
    L.hline(x, x + 15, y + 3, "s4")
    L.hline(x, x + 15, y + 4, "s1")
    for jx in (x + 4, x + 11):
        L.vline(jx, y + 1, y + 3, "s2")


def wall_caps_top(L, x, y):
    for j in range(16):
        for i in range(16):
            c = _CAPS[j, i]
            L.px(x + i, y + j, c if c else "s2")
    L.vline(x, y, y + 15, "s3")
    L.vline(x + 15, y, y + 15, "s1")


def walls():
    s = Struct("wall_drystone", "Dry-stone walls with whitewashed caps", 5, 2, SEC,
               walk=["XXXXX", "XXXX-"],
               notes="Row 0: an east-west run: west end, middle A, middle B, east end, and "
                     "a lone pier (also the south end of a north-south run, or a gate post). "
                     "Row 1: a north-south run seen from above: middle, north end, and the "
                     "corners NW and NE where an east-west run turns south. For SW and SE "
                     "corners use the east-west ends.")
    L = s.B

    def run(x, y, west=False, east=False, shift=0):
        wall_caps_row(L, x, y)
        for j in range(11):
            for i in range(16):
                c = _WALL_FACE[j, (i + shift) % 16]
                L.px(x + i, y + 5 + j, c if c else "sk")
        if west:
            L.vline(x, y, y + 15, "s1")
            L.vline(x + 1, y + 1, y + 3, "s5")
        if east:
            L.vline(x + 15, y, y + 15, "s0")
        L.hline(x, x + 15, y + 15, "s0")

    run(0, 0, west=True)
    run(16, 0)
    run(32, 0, shift=8)  # the same stones half a cell on, so long runs repeat less
    run(48, 0, east=True)
    run(64, 0, west=True, east=True)
    # north-south run from above, its north end, and the two corners
    wall_caps_top(L, 0, 16)
    for x in (16, 32, 48):
        wall_caps_top(L, x, 16)
        L.hline(x, x + 15, 16, "s3")
        L.hline(x + 1, x + 14, 17, "s5")
    L.vline(32, 16, 31, "s3")
    L.vline(63, 16, 31, "s1")
    # (4,1) stays empty
    return s


TER_SEEDS = [(3, 3), (11, 2), (7, 7), (14, 8), (2, 10), (10, 11)]
_TL = voronoi_labels(16, 12, TER_SEEDS, stretch=(0.7, 1.0))
_TJ = joints(_TL)
_TER_FACE = shade_stones(_TL, _TJ, ["s2", "e2", "s3", "s2", "e2", "s2"],
                         {"s2": "s3", "s3": "s4", "e2": "s3"}, {"s2": "s1", "s3": "s2", "e2": "e1"})


def terraces():
    s = Struct("terrace", "Terrace retaining walls and steps", 5, 2, SEC,
               walk=["XXX.X", "XJJ.X"],
               notes="Retaining walls for terraced hillside, lower ground to the south. "
                     "Row 0: west end, middle A, middle B, steps up through the wall, east "
                     "end. Row 1: the same pieces as one-way ledges (MB_JUMP_SOUTH) for the "
                     "two middles; the ends and steps repeat so a ledge run can close.")
    L = s.B

    def ter(x, y, shift=0, west=False, east=False):
        L.hline(x, x + 15, y, "s3")
        L.hline(x, x + 15, y + 1, "s5")
        L.hline(x, x + 15, y + 2, "s4")
        L.hline(x, x + 15, y + 3, "s1")
        for j in range(11):
            for i in range(16):
                c = _TER_FACE[j, (i + shift) % 16]
                L.px(x + i, y + 4 + j, c if c else "sk")
        L.hline(x, x + 15, y + 15, "s0")
        if west:
            L.vline(x, y, y + 15, "s1")
        if east:
            L.vline(x + 15, y, y + 15, "s0")

    def stair(x, y):
        L.rect(x, y, 16, 16, "s3")
        yy = y
        for k in range(4):
            L.hline(x + 2, x + 13, yy, "s5")
            L.hline(x + 2, x + 13, yy + 1, "s4")
            L.hline(x + 2, x + 13, yy + 2, "s2")
            L.hline(x + 2, x + 13, yy + 3, "s1")
            yy += 4
        L.rect(x, y, 2, 16, "s2")
        L.vline(x, y, y + 15, "s1")
        L.rect(x + 14, y, 2, 16, "s1")
        L.vline(x + 15, y, y + 15, "s0")
        L.hline(x, x + 1, y, "s4")

    for row in (0, 16):
        ter(0, row, west=True)
        ter(16, row)
        ter(32, row, shift=8)
        stair(48, row)
        ter(64, row, east=True)
    return s


# --------------------------------------------------------------------------
# Olive-press house (group "cyc")
# --------------------------------------------------------------------------

def olive_press():
    s = Struct("olive_press", "Olive-press house", 3, 3, SEC,
               walk=["XXX", "XXX", "XXX"],
               notes="A whitewashed press-house with a wide arched opening onto its "
                     "trapetum: a round stone basin, a central pier and two upright "
                     "millstones on a wooden axle, with a basket of olives. Scenery; the "
                     "olive farmer stands in front. Roof and wall tiles are shared with the "
                     "houses, so it costs few tiles.")
    L = s.B
    flat_roof(L, 0, 0, 48, 17)
    facade(L, 0, 17, 48, 31)
    # the arch: a thick wall, so the reveal shows (shaded left and top, lit right)
    x0, x1, top, spring = 7, 40, 21, 28
    cxa, r = (x0 + x1) / 2, (x1 - x0) / 2
    def inside(x, y):
        if y >= spring:
            return x0 <= x <= x1
        return ((x - cxa) / (r + 0.5)) ** 2 + ((y - spring) / (spring - top + 0.5)) ** 2 <= 1.0
    for y in range(top - 1, 48):
        for x in range(x0 - 1, x1 + 2):
            if inside(x, y):
                L.px(x, y, "dk")
            elif any(inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                L.px(x, y, "ink")
    for y in range(top, 48):
        row = [x for x in range(x0, x1 + 1) if inside(x, y)]
        if not row:
            continue
        L.px(row[0], y, "w3")
        L.px(row[0] + 1, y, "w4")
        L.px(row[-1], y, "w1")
        if y < spring + 2:
            for x in row[2:-1]:
                if not inside(x, y - 2):
                    L.px(x, y, "w4")
    # the floor of the press room, catching some light
    L.hline(x0 + 2, x1 - 1, 46, "w4")
    L.hline(x0, x1, 47, "w3")
    # trapetum: basin rim, the central pier, two upright millstones on an axle
    L.ellipse(10, 37, 37, 46, "ink")
    L.ellipse(11, 37, 36, 45, "w2")
    L.ellipse(11, 39, 36, 45, "w3")
    L.ellipse(14, 39, 33, 44, "w4")
    L.rect(22, 29, 4, 12, "w3")
    L.vline(22, 29, 40, "ink")
    L.vline(25, 29, 40, "ink")
    L.vline(23, 29, 40, "w1")
    L.hline(22, 25, 29, "w0")
    stone = [
        "  kkkk  ",
        " k0011k ",
        "k001122k",
        "k011223k",
        "k012233k",
        "k112233k",
        "k122334k",
        " k2334k ",
        "  kkkk  ",
    ]
    sk = {"k": "ink", "0": "w0", "1": "w1", "2": "w2", "3": "w3", "4": "w4"}
    # the axle runs from the pier out past the rim, where the donkey is yoked
    L.rect(24, 33, 17, 2, "tc1")
    L.hline(24, 40, 33, "tc2")
    L.px(41, 33, "ink")
    L.px(41, 34, "ink")
    L.blit(stone, sk, 14, 33)
    # a basket of olives at the door
    basket = [
        " gGgGg ",
        "gGgGgGg",
        "kkkkkkk",
        "kTtTtTk",
        " kTtTk ",
    ]
    L.blit(basket, {"g": "ol1", "G": "ol2", "k": "ink", "T": "tc2", "t": "tc1"}, 39, 42)
    return s


def build():
    return [house_small(), house_two_story(), shrine(), paving(), altar(),
            garland_posts(), walls(), terraces(), olive_press()]
