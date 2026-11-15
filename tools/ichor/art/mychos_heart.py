"""Ring VII (the Choros) and the Starry Chamber, for gTileset_Mychos.

  choros  starlit marble, square slabs a cell each (no parity: one floor and its
          ten thread twins); the mirrors' beam (ENGINE E9's six consecutive beam
          metatiles, by day sunlight and by night starlight) with its corners on
          the mirror bases; the 5 x 5 dancing floor (LABYRINTH.md §5.7), each of
          its five symbols blank, revealed and lit; the spiral stair the dance
          opens; the frescoes of the whole dance, faded and clear
  heart   the Starry Chamber (scene J): the black lustral basin, its water
          twinkling with the star-clock's reflection (animated); the star-clock's
          ring inlaid round it; the pillar of horns Asterion is chained to; the
          anvil with the three adamant fragments in their bronze collar

Everything here stands on marble, which has no parity, so nothing needs a twin.
"""
from __future__ import annotations

import math

import labyrinth_art as A
import labyrinth_kit as KIT
import labyrinth_rings as R
from labyrinth_art import Struct, blit

NI = {"k": "nk", "0": "nn0", "1": "nn1", "2": "nn2", "3": "nn3", "w": "ns0", "y": "ns1",
      "m": "nm0", "M": "nm1", "W": "nm2", "p": "np0", "P": "np1", "g": "ng0", "G": "ng1"}
BZ = {"k": "ink", "0": "bz0", "1": "bz1", "2": "bz2", "3": "bz3", "4": "bz4", "w": "bw",
      "e": "be", "v": "bv0", "V": "bv1", "i": "bi0", "I": "bi1", "s": "ts0", "S": "ts1"}
MN = {"k": "ink", "R": "mr0", "r": "mr1", "e": "mr2", "o": "mo0", "O": "mo1", "y": "mo2",
      "g": "mg0", "G": "mg1", "W": "mg2", "b": "mb"}


def marble(L, x0, y0):
    KIT.marble_slab(L, x0, y0)


# --------------------------------------------------------------------------
# Ring VII: the floor, the beam, the dancing floor
# --------------------------------------------------------------------------

def marble_floor():
    return KIT.thread_block(
        "marble", "Floors: starlit marble and its thread twins",
        [("marble", "marble", None, None)], section="choros",
        notes="Ring VII's floor (and the Starry Chamber's): Cretan marble in starlight, one "
              "square slab a cell, so it has no parity: lay `marble` everywhere. Its ten "
              "thread twins follow it: `Ichor_AddThreadFloor(marble, marble + 1)` beside the "
              "ring's `dark_l` and `dark_r` if it has slab corridors too. The other cells are "
              "void.")


SUN = {"e": "ff1", "c": "ff2", "w": "ff3"}
STAR = {"e": "nn2", "c": "ns0", "w": "ns1"}


def _beam(M, x0, y0, sides, light):
    """A beam of light crossing a cell: four pixels wide through the middle,
    from the middle to each side in `sides` (n, s, w, e), a glint every eight
    pixels. Symmetric about the middle, so its tiles serve every direction
    flipped."""
    col = SUN if light == "sun" else STAR
    straight = set(sides) in ({"w", "e"}, {"n", "s"})
    for y in range(16):
        for x in range(16):
            inx, iny = 6 <= x <= 9, 6 <= y <= 9
            if inx and iny and not straight:
                c = col["w"] if (x in (7, 8) and y in (7, 8)) else col["c"]
            elif straight and set(sides) == {"w", "e"} and iny:
                k = y - 6
                c = col["e"] if k in (0, 3) else (col["w"] if x % 8 in (3, 4) else col["c"])
            elif straight and set(sides) == {"n", "s"} and inx:
                k = x - 6
                c = col["e"] if k in (0, 3) else (col["w"] if y % 8 in (3, 4) else col["c"])
            elif iny and (("w" in sides and x < 6) or ("e" in sides and x > 9)):
                k = y - 6
                c = col["e"] if k in (0, 3) else (col["w"] if x % 8 in (3, 4) else col["c"])
            elif inx and (("n" in sides and y < 6) or ("s" in sides and y > 9)):
                k = x - 6
                c = col["e"] if k in (0, 3) else (col["w"] if y % 8 in (3, 4) else col["c"])
            else:
                continue
            M.px(x0 + x, y0 + y, c)


def _mirror_base(L, x0, y0):
    """A round marble plate inlaid with a gold ring, where a mirror turns."""
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - 7.5, y - 8.0)
            if d <= 6.6:
                c = "nm2" if (x - 7.5) + (y - 8) < -3 else "nm1"
                if 4.6 < d <= 5.6:
                    c = "ng1" if y < 8 else "ng0"
                elif d > 5.6:
                    c = "nm0"
                L.px(x0 + x, y0 + y, c)


def beam():
    """The mirrors' beam (ENGINE E9): six consecutive metatiles per light,
    straights on marble and corners on the mirror bases."""
    s = Struct("beam", "The mirrors' beam: sunlight and starlight", 8, 2,
               walk=["......XX", "......XX"], section="choros",
               notes="Ring VII's beam (ichor_beam.c, `Ichor_TraceBeam` with VAR_0x8005 = the "
                     "first of six): row 0 by **day** (sunlight), row 1 by **night** "
                     "(starlight), each `ew`, `ns`, `ne`, `nw`, `se`, `sw` in the engine's "
                     "order (pass `sun_ew` or `star_ew`). The straights cross marble; the "
                     "corners, which only ever lie under a mirror, are drawn on its base. (6) "
                     "`base`: the mirror base unlit, under every mirror object; (7) `shaft_sun` / "
                     "`shaft_star`: the floor under the ceiling's light shaft, where the first "
                     "mirror stands. Corners and bases block; the straights keep the floor's "
                     "passability (they take no thread: Ring VII's antechamber is a thread "
                     "stop while the beam is lit).")
    L, M = s.B, s.M
    order = [("ew", "we"), ("ns", "ns"), ("ne", "ne"), ("nw", "nw"), ("se", "se"), ("sw", "sw")]
    s.names = {}
    for r, light in enumerate(("sun", "star")):
        for i, (nm, sides) in enumerate(order):
            x0, y0 = i * 16, r * 16
            if i < 2:
                marble(L, x0, y0)
            else:
                marble(L, x0, y0)
                _mirror_base(L, x0, y0)
            _beam(M, x0, y0, sides, light)
            s.names[f"{light}_{nm}"] = (i, r)
        marble(L, 96, r * 16)
        _mirror_base(L, 96, r * 16)
        marble(L, 112, r * 16)
        for y in range(16):
            for x in range(16):
                d = math.hypot((x - 7.5) * 0.9, y - 8)
                c = L.get(112 + x, r * 16 + y)
                lit = ({"nm1": "ng1", "nm2": "ns1", "nm0": "ng0", "nn1": "ng0"} if light == "sun"
                       else {"nm1": "nm2", "nm2": "ns0", "nm0": "nm1", "nn1": "nn3"})
                if d < 6.2 or (d < 8 and (x + y) % 2 == 0):
                    L.px(112 + x, r * 16 + y, lit.get(c, c))
    s.names["base"] = (6, 0)
    s.names["base_b"] = (6, 1)
    s.names["shaft_sun"] = (7, 0)
    s.names["shaft_star"] = (7, 1)
    s.walk = ["......XX", "......XX"]
    for i in (2, 3, 4, 5):
        s.walk = [w[:i] + "X" + w[i + 1:] for w in s.walk]
    return s


# the dancing floor's symbols, 10 x 10, in three states
DANCE = {
    "X": ["..........",
          ".#......#.",
          ".##.##.##.",
          ".########.",
          ".##.##.##.",
          ".#..##..#.",
          "....##....",
          "....##....",
          "....##....",
          ".........."],
    "W": ["..........",
          "...###....",
          "..#...#...",
          ".#..##.#..",
          ".#.#..#.#.",
          ".#..#...#.",
          "..#....#..",
          "...####.##",
          "..........",
          ".........."],
    "L": ["....##....",
          ".#..##..#.",
          ".##.##.##.",
          "..######..",
          "...####...",
          "....##....",
          "....##....",
          "...#..#...",
          "..#....#..",
          ".........."],
    "R": ["...####...",
          "..#....#..",
          ".#.#..#.#.",
          "#...##...#",
          "#..####..#",
          "#..####..#",
          "#...##...#",
          ".#.#..#.#.",
          "..#....#..",
          "...####..."],
    "S": ["....##....",
          "....##....",
          ".#..##..#.",
          "..######..",
          "####..####",
          "####..####",
          "..######..",
          ".#..##..#.",
          "....##....",
          "....##...."],
}


def _dance_cell(L, M, x0, y0, sym, state):
    """A square of the dancing floor: polished marble in a gold-cornered border,
    its symbol blank (before the beam reaches the floor), revealed, or lit
    (stepped on in the dance)."""
    lit = state == "lit"
    for y in range(16):
        for x in range(16):
            e = min(x, y, 15 - x, 15 - y)
            if e == 0:
                c = "nn1"
            elif e == 1:
                c = "nm0" if not lit else "ng0"
            elif e == 2:
                c = "nm2" if not lit else "ns1"
            else:
                c = "nm1" if not lit else "ng1"     # a stepped square glows gold
            if e <= 2 and min(x, 15 - x) <= 2 and min(y, 15 - y) <= 2:
                c = "ng0" if not lit else "ns1"
            L.px(x0 + x, y0 + y, c)
    if sym is None:
        return
    glyph = DANCE[sym]
    # revealed: inlaid in lapis; lit: white fire on the gold, outlined
    col = {"blank": None, "dim": "nn1", "lit": "ns0"}[state]
    if lit:
        for j, row in enumerate(glyph):
            for i, ch in enumerate(row):
                if ch == "#":
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        xx, yy = i + dx, j + dy
                        if not (0 <= xx < 10 and 0 <= yy < 10) or glyph[yy][xx] != "#":
                            L.px(x0 + 3 + xx, y0 + 3 + yy, "ng0")
    for j, row in enumerate(glyph):
        for i, ch in enumerate(row):
            if ch == "#":
                L.px(x0 + 3 + i, y0 + 3 + j, col)


def dancing_floor():
    s = Struct("dance", "Ariadne's dancing floor: the Choros", 6, 2,
               walk=["......", "D....."], section="choros",
               notes="The 5 x 5 dancing floor (LABYRINTH.md §5.7): every square polished "
                     "marble in a gold-cornered border. Row 0: (0) `blank`, every square before "
                     "the beam reaches the crystal (\"until lit, the floor's symbols are "
                     "blank\"); (1-5) `x`, `w`, `l`, `r`, `s` revealed: double axe, wave, lily, "
                     "rosette, star. Row 1: (1-5) the same **lit**, gold, for a square stepped "
                     "on in the dance: **each lit square is its revealed square + 8**. (0, 1) "
                     "`stair`: the spiral stair the finished dance opens at the star in the "
                     "middle (C3), MB_NON_ANIMATED_DOOR: its warp goes down to the Starry "
                     "Chamber. The squares take no thread: the thread stops at the floor's "
                     "edge, and the stair is the way on.")
    L, M = s.B, s.M
    _dance_cell(L, M, 0, 0, None, "blank")
    for i, sym in enumerate("XWLRS", 1):
        _dance_cell(L, M, i * 16, 0, sym, "dim")
        _dance_cell(L, M, i * 16, 16, sym, "lit")
    # the spiral stair: steps winding down round a newel into the dark
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - 7.5, y - 7.5)
            ang = (math.degrees(math.atan2(y - 7.5, x - 7.5)) + 360) % 360
            if d > 7.4:
                c = "nn1"
            elif d > 6.6:
                c = "ng0"
            elif d < 1.6:
                c = "nm1"
            else:
                step = int(ang // 40)          # each step round a little deeper
                c =["nm2", "nm1", "nm0", "nn3", "nn2", "nn1", "nn0", "nk", "nk"][min(8, step)]
                if int(ang) % 40 < 4:
                    c = "nm2" if step < 4 else "nn2"
            L.px(x + 0, y + 16, c)
    s.behaviors[(0, 1)] = "MB_NON_ANIMATED_DOOR"
    s.names = {"blank": (0, 0), "x": (1, 0), "w": (2, 0), "l": (3, 0), "r": (4, 0), "s": (5, 0),
               "stair": (0, 1), "x_lit": (1, 1), "w_lit": (2, 1), "l_lit": (3, 1),
               "r_lit": (4, 1), "s_lit": (5, 1)}
    return s


def choros_frescoes():
    return [
        R.fresco_bay("fresco_v", "Fresco: the dance's steps 4-6", "RWL",
                     "The dance's steps 4-6, rosette, wave, lily: with `fresco_iv` and "
                     "`fresco_vi`, the clear fresco of the whole dance in Ring VII's alcove, once "
                     "the floor is lit.", section="choros"),
        R.fresco_bay("fresco_faded", "Fresco: the whole dance, faded", "XXX",
                     "Ring VII's side alcove (LABYRINTH.md §6): the whole dance in silhouette, "
                     "too faded to read; lay it three bays wide, then swap the bays for "
                     "`fresco_iv`, `fresco_v` and `fresco_vi` when the dancing floor is lit.",
                     faded=True, section="choros"),
    ]


def choros():
    return A.order_for_packing([marble_floor(), beam(), dancing_floor(), *choros_frescoes()])


# --------------------------------------------------------------------------
# The Starry Chamber
# --------------------------------------------------------------------------

# star positions for the water's four variants (x, y, kind): kind 0 small, 1 bright
STARFIELDS = [
    [(3, 2, 1), (11, 5, 0), (6, 9, 0), (13, 12, 1), (2, 13, 0), (9, 14, 0)],
    [(5, 3, 0), (12, 2, 1), (2, 8, 0), (9, 10, 1), (14, 9, 0), (5, 13, 0)],
    [(2, 4, 0), (8, 3, 0), (13, 6, 0), (6, 11, 1), (11, 13, 0), (1, 14, 0)],
    [(7, 2, 1), (3, 7, 0), (12, 9, 0), (8, 13, 0), (14, 3, 0), (4, 12, 1)],
]


def _water(L, x0, y0, field, frame):
    """The lustral basin's black water, the star-clock in it."""
    for y in range(16):
        for x in range(16):
            # black water, a faint ripple across it here and there
            c = "nn0" if (y % 5 == 2 and (x + y * 3) % 9 < 2) else "nk"
            L.px(x0 + x, y0 + y, c)
    for k, (sx, sy, bright) in enumerate(field):
        ph = (k + frame) % 4
        if bright:
            core = ["ns0", "ns1", "ns0", "nn3"][ph]
            L.px(x0 + sx, y0 + sy, core)
            if ph in (0, 2):
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    L.px(x0 + sx + dx, y0 + sy + dy, "nn2" if ph == 0 else "nn3")
        else:
            L.px(x0 + sx, y0 + sy, ["nn3", "ns1", "nn2", "nn1"][ph])


def basin():
    """The lustral basin: a sunken Minoan pool, gypsum steps down into black
    water that holds the ceiling's stars."""
    s = Struct("basin", "The Starry Chamber: the lustral basin", 6, 3,
               walk=["XXXXXX"] * 3, section="heart",
               notes="The black lustral basin (scene J), the Minoan sunken pool, a rectangle "
                     "of any size: (0-2, 0-2) its frame round `water`, nw n ne / w water e / sw "
                     "s se; repeat `n`, `s`, `w`, `e` and the water to size. The north side shows "
                     "the basin's inner wall going down to the water; the others its rim. Its "
                     "water twinkles with the star-clock's stars (animated): mix `water`, "
                     "`water_b`, `water_c`, `water_d` (3-5, 0-1 and 3, 2) so the stars don't "
                     "repeat. (4, 2) `steps_n`: gypsum steps down into it, for the north side. "
                     "All block.")
    L = s.B
    frames = []

    def frame_layers():
        return [L] + frames

    # lay the base (frame 0) then the frames as copies, painting water per frame
    def rim_cell(Lx, cx, cy, n=False, s_=False, w=False, e=False, field=None, fr=0):
        x0, y0 = cx * 16, cy * 16
        _water(Lx, x0, y0, field or [], fr)
        for y in range(16):
            for x in range(16):
                c = None
                if n:
                    # the rim (gypsum) and the inner wall down to the water
                    if y < 3:
                        c = ["nm0", "nm2", "nm1"][y]
                    elif y < 9:
                        c = "nn1" if (x + (y // 3) * 4) % 8 == 0 or y % 3 == 2 else "nn2"
                        if y == 8:
                            c = "nn0"
                if s_ and y >= 12:
                    c = ["nm2", "nm1", "nm1", "nm0"][y - 12]
                if w and x < 4:
                    c = ["nm0", "nm2", "nm1", "nn1"][x] if not (n and y < 3) else c
                    if n and y < 3:
                        c = ["nm0", "nm2", "nm1"][y] if x > 0 else "nm0"
                if e and x >= 12:
                    c = ["nn1", "nm1", "nm2", "nm0"][x - 12] if not (n and y < 3) else c
                    if n and y < 3:
                        c = ["nm0", "nm2", "nm1"][y] if x < 15 else "nm0"
                if s_ and y >= 12 and (w and x < 4 or e and x >= 12):
                    c = "nm1" if y < 15 else "nm0"
                if c:
                    Lx.px(x0 + x, y0 + y, c)

    cells = {(0, 0): dict(n=True, w=True), (1, 0): dict(n=True), (2, 0): dict(n=True, e=True),
             (0, 1): dict(w=True), (2, 1): dict(e=True),
             (0, 2): dict(s_=True, w=True), (1, 2): dict(s_=True), (2, 2): dict(s_=True, e=True)}
    for (cx, cy), k in cells.items():
        rim_cell(L, cx, cy, **k)
    waters = {(1, 1): 0, (3, 0): 1, (4, 0): 2, (5, 0): 3, (3, 1): 1, (4, 1): 2, (5, 1): 3,
              (3, 2): 0}
    # frame 0
    for (cx, cy), f in waters.items():
        _water(L, cx * 16, cy * 16, STARFIELDS[f], 0)
    # steps down (cell 4, 2), for the north side: the rim, then gypsum treads
    # going down into the water, each darker, between the basin's inner walls
    rows = ["m", "W", "M",                  # the rim, as the north edge's
            "W", "M", "M", "2",             # tread, tread, riser
            "M", "m", "m", "2",
            "m", "1", "1",
            "0", "k"]                       # the water's edge
    for y in range(16):
        for x in range(16):
            c = NI[rows[y]]
            if y >= 3 and (x < 2 or x > 13):
                c = "nn1" if (x in (0, 15)) else "nn2"
            L.px(64 + x, 32 + y, c)
    # the frames: only the open water twinkles
    frames.extend(A.anim_layer(s, "stars", 4, layer="bottom"))
    for i, f in enumerate(frames, 1):
        for (cx, cy), fld in waters.items():
            _water(f, cx * 16, cy * 16, STARFIELDS[fld], i)
    # cell (5, 2): the rim's south corner piece for a basin seen whole... a lone rim
    rim_cell(L, 5, 2, s_=True)
    for f in frames:
        f.a[32:48, 80:96] = L.a[32:48, 80:96]
    s.names = {"nw": (0, 0), "n": (1, 0), "ne": (2, 0), "w": (0, 1), "water": (1, 1),
               "e": (2, 1), "sw": (0, 2), "s": (1, 2), "se": (2, 2), "water_b": (3, 0),
               "water_c": (4, 0), "water_d": (5, 0), "water_e": (3, 1), "water_f": (4, 1),
               "water_g": (5, 1), "water_h": (3, 2), "steps_n": (4, 2), "s_lone": (5, 2)}
    return s


def clock_ring():
    """The star-clock's ring, inlaid in the floor round the basin: a band of gold
    set with lapis stars, the hours marked."""
    s = Struct("clock", "The Starry Chamber: the star-clock's ring", 4, 2, walk=["...."] * 2,
               section="heart",
               notes="Daedalus's star-clock (LABYRINTH.md §6, the heart) is painted on the "
                     "ceiling and turns; its ring is inlaid in the marble round the basin, a gold "
                     "band set with lapis stars, the hours marked. A rectangle one cell out from "
                     "the basin's rim: corners `nw`, `ne`, `sw`, `se`; along it `h` and `h_star` "
                     "(north and south sides), `v` and `v_star` (west and east), alternating. "
                     "Walkable.")
    L = s.B
    # plain polished marble under the ring, so its pieces are symmetric and the
    # four corners and both sides of each band are one set of tiles, flipped
    for cx in range(4):
        for cy in range(2):
            for y in range(16):
                for x in range(16):
                    L.px(cx * 16 + x, cy * 16 + y, "nm1")

    def band(x0, y0, horiz, star):
        for y in range(16):
            for x in range(16):
                a, b = (y, x) if horiz else (x, y)
                if 6 <= a <= 9:
                    c = "ng1" if a in (6, 9) else "nn1"
                    if a in (7, 8) and b % 4 == 1:
                        c = "nn3"
                    L.px(x0 + x, y0 + y, c)
                elif a in (5, 10):
                    L.px(x0 + x, y0 + y, "nm0")
        if star:
            # an hour star, gold on lapis, on the band
            blit(L, ["...yy...", "..yGGy..", "yyGwwGyy", "yyGwwGyy", "..yGGy..", "...yy..."],
                 NI, x0 + 4, y0 + 5)

    def corner(x0, y0, sx, sy):
        # a quarter of a ring joining the two bands round the basin's corner
        # centred on the cell's inner corner, radius 8 to the band's middle
        ox = 15.5 if sx > 0 else -0.5
        oy = 15.5 if sy > 0 else -0.5
        for y in range(16):
            for x in range(16):
                d = math.hypot(x - ox, y - oy)
                for lo, hi, c in ((5.5, 6.5, "nm0"), (6.5, 7.5, "ng1"), (7.5, 9.5, "nn1"),
                                  (9.5, 10.5, "ng1"), (10.5, 11.5, "nm0")):
                    if lo <= d < hi:
                        L.px(x0 + x, y0 + y, c)

    corner(0, 0, 1, 1)       # nw: the band runs east and south from here
    corner(16, 0, -1, 1)     # ne
    corner(0, 16, 1, -1)     # sw
    corner(16, 16, -1, -1)   # se
    band(32, 0, True, False)
    band(48, 0, True, True)
    band(32, 16, False, False)
    band(48, 16, False, True)
    s.names = {"nw": (0, 0), "ne": (1, 0), "sw": (0, 1), "se": (1, 1), "h": (2, 0),
               "h_star": (3, 0), "v": (2, 1), "v_star": (3, 1)}
    return s


def horns_pillar():
    """The pillar of horns at the basin's near edge: Asterion is chained to it."""
    s = Struct("horns", "The Starry Chamber: the pillar of horns", 1, 2, walk=["X", "X"],
               section="heart",
               notes="A square gypsum pillar crowned with horns of consecration, a bronze "
                     "ring and chain at its foot: Asterion is chained to it, Rhea holds the "
                     "chain (scene J). Blocks.")
    L, M = s.B, s.M
    marble(L, 0, 0)
    marble(L, 0, 16)
    blit(M, ["k..........k....",
             "Wk........kW....",
             "WGk......kGW....",
             ".WGk....kGWk....",
             "..WWkkkkWWk.....",
             ".kGGGGGGGGk.....",
             ".kkkkkkkkkk....."], MN, 2, 1)
    for y in range(8, 29):
        for x in range(4, 12):
            c = "mg2" if x < 6 else "mg1" if x < 10 else "mg0"
            if x in (4, 11):
                c = "ink"
            if y in (14, 15):
                c = "mr1" if 4 < x < 11 else c
            M.px(x, y, c)
    for x in range(3, 13):
        M.px(x, 29, "ink")
        M.px(x, 28, "mg1")
    # the ring and a length of chain (ochre bronze, in the pillar's palette)
    blit(M, [".kk.", "kOOk", "kO.k", ".kk."], MN, 12, 19)
    blit(M, ["O", "o", "O", "o", "O", "o"], MN, 13, 23)
    s.names = {"top": (0, 0), "base": (0, 1)}
    return s


def anvil_heart():
    """Kronos's anvil at the basin's edge: the three adamant fragments of the
    Harpe on it, joined by a bronze collar (the collar Daedalus made)."""
    s = Struct("star_anvil", "The Starry Chamber: the anvil and the three fragments", 4, 1,
               walk=["XXXX"], section="heart",
               notes="Kronos's anvil at the basin's edge (scene J), two cells: (0, 1) with the "
                     "three adamant fragments on it, joined by Daedalus's bronze collar; (2, 3) "
                     "`empty_l`, `empty_r`, the same once the Harpe is forged and lifted into "
                     "its case. Blocks; Kronos stands north of it.")
    L, M = s.B, s.M
    for i in range(4):
        marble(L, i * 16, 0)
    for x0 in (0, 32):
        blit(M, ["..kkkkkkkkkkkkkkkkkkkkkkkkk...",
                 ".kIIIIIIIIIIIIIIIIIIIIIIIIIkk.",
                 "kkiiiiiiiiiiiiiiiiiiiiiiiiiiik",
                 "..kkkkkiiiiiiiiiiiiiiiiikkkk..",
                 ".......kiiiiiiiiiiiiiiik......",
                 "......kkiiiiiiiiiiiiiiikk.....",
                 ".....kSSSSSSSSSSSSSSSSSSSk....",
                 ".....kssssssssssssssssssssk...",
                 ".....kkkkkkkkkkkkkkkkkkkkkk..."], {**BZ, "i": "bi0", "I": "bi1"}, x0 + 1, 6)
    # the fragments: adamant, pale and hard, in their collar
    blit(M, ["....w.......w.....",
             "...wVk.....kVw....",
             "..wVVk.kk.kVVw....",
             "kk3333kwwk3333kk..",
             "..kkkkkkkkkkkkk..."], BZ, 7, 1)
    s.names = {"l": (0, 0), "r": (1, 0), "empty_l": (2, 0), "empty_r": (3, 0)}
    return s


def heart():
    return A.order_for_packing([basin(), clock_ring(), horns_pillar(), anvil_heart()])
