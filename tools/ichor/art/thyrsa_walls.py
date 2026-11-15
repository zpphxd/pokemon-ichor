"""Thyrsa's streets and its Cyclopean walls (gTileset_Thyrsa).

Streets: the grey-buff flags (a 16 px texture, so any cell meets any other),
their shaded variants, kerbs against grass, broad steps, and the Cyclopean
terrace walls that hold the city's levels, with the Kadmeia's parapet.

Walls: the city wall, all in one masonry texture that repeats every 32 px.
- An east-west wall is three rows: the battlement (wall-walk and merlons) and
  two rows of face. Place its pieces at even map columns: `wall_face`'s run
  cells come as an even/odd pair and must alternate with the map column, so
  the blocks run on unbroken. The north and south walls both use it.
- A north-south wall is a strip two cells wide seen from above: merlons on
  its outer edge, the wall-walk, and the shadow it casts inward. The east
  wall is the west wall mirrored, which costs no tiles.
- The gates: the Elektran Gate (the main gate, a wide arch between two
  towers, 8 cells), a gate through a north-south strip (the Neistan and the
  Proitid), and bricked-up gates of both kinds: Thyrsa had seven gates and
  uses three.
- The theater's outer gate: a small propylon with a mask in its pediment, the
  door warp to the theater.
"""
from __future__ import annotations

import thyrsa_lib as T
from thyrsa_lib import finish, struct

# ==========================================================================
# Streets
# ==========================================================================


def _shade(L, x0, y0, north=True, west=False, depth=3):
    """Darken a paved cell's north or west edge: the shadow a wall or a house
    casts on the street south or east of it (light from the top left)."""
    dark = {"cg5": "cg3", "cg4": "cg3", "cg3": "cg2", "cg2": "cg1", "cb": "cg2"}
    for y in range(16):
        for x in range(16):
            if (north and y < depth) or (west and x < depth):
                c = L.get(x0 + x, y0 + y)
                if c in dark:
                    L.px(x0 + x, y0 + y, dark[c])


def paving_set():
    s = struct("paving", "Street flags", 5, 1, walk=["....."], ground="pave",
               notes="Thyrsa's streets: irregular grey-buff flags, three or four to a cell. "
                     "The texture repeats every cell, so any paving cell meets any other. "
                     "(0) the flags, (1) a cracked slab with a tuft of weed (scatter it "
                     "sparingly). (2)-(4) the flags in shadow: (2) along the north edge, for "
                     "the row under a wall or a house's front, (3) along the west edge, for "
                     "the column east of a building's end, (4) both, for the corner. All "
                     "walkable.")
    L = s.M
    # (1) a crack and a weed
    L.blit(["k   ", " k  ", " kk ", "   k", "   k"], {"k": "cg1"}, 20, 4)
    L.blit([" 3 ", "323", " 2 "], {"2": "iv2", "3": "iv3"}, 25, 9)
    finish(s)
    _shade(s.B, 32, 0, north=True)
    _shade(s.B, 48, 0, north=False, west=True)
    _shade(s.B, 64, 0, north=True, west=True)
    s.names = {"flag": (0, 0), "crack": (1, 0), "shade_n": (2, 0), "shade_w": (3, 0),
               "shade_nw": (4, 0)}
    return s


def kerbs():
    """Flags meeting grass: a 3x3 border plus inner corners. A row of dressed
    kerbstones runs round the paved area; on its south edge the kerb's face
    shows, the street a step above the grass."""
    s = struct("kerb", "Street flags' kerbed edge against grass", 5, 3,
               walk=[".....", ".....", "....."], ground="none",
               notes="Columns 0-2 are the paved area's border: NW, N, NE / W, plain, E / SW, "
                     "S, SE. Columns 3-4, rows 0-1, are inner corners (grass diagonally beyond): "
                     "NW, NE / SW, SE. (3,2) and (4,2) are the plain flags and a cracked slab.")
    L = s.B
    T.paving(L, 0, 0, 80, 48)
    W = 48
    K = {"o": "cg0", "a": "cg2", "b": "cg4", "c": "cg5"}

    def kerb_h(x0, x1, y, face=False):
        # a course of kerbstones 3 px deep, joints every 8 px
        for x in range(x0, x1):
            L.px(x, y, "cg0")
            L.px(x, y + 1, "cg5" if x % 8 else "cg2")
            L.px(x, y + 2, "cg3" if x % 8 else "cg2")
        if face:
            for x in range(x0, x1):
                L.px(x, y + 3, "cg2")
                L.px(x, y + 4, "cg1")
                L.px(x, y + 5, "cg0")

    def kerb_v(x, y0, y1, east=False):
        for y in range(y0, y1):
            L.px(x if not east else x + 2, y, "cg0")
            L.px(x + 1, y, "cg4" if y % 8 else "cg2")
            L.px(x + 2 if not east else x, y, "cg3" if y % 8 else "cg2")
    kerb_h(0, W, 0)
    kerb_v(0, 0, 48)
    kerb_v(W - 3, 0, 48, east=True)
    # the south edge: the kerb's face shows below it
    for x in range(W):
        for y in range(42, 48):
            L.px(x, y, {42: "cg0", 43: "cg5", 44: "cg3", 45: "cg2", 46: "cg1", 47: "cg0"}[y]
                 if x % 8 else {42: "cg0", 43: "cg2", 44: "cg2", 45: "cg1", 46: "cg1", 47: "cg0"}[y])
    kerb_v(0, 0, 42)
    kerb_v(W - 3, 0, 42, east=True)
    for x in (0, W - 1):
        L.vline(x, 42, 47, "cg0")
    # inner corners: a short kerb nib in the corner toward the grass
    for (cx, cy, sx, sy) in ((3, 0, 0, 0), (4, 0, 1, 0), (3, 1, 0, 1), (4, 1, 1, 1)):
        px = cx * 16 + (13 if sx else 0)
        py = cy * 16 + (13 if sy else 0)
        L.rect(px, py, 3, 3, "cg3")
        L.hline(px, px + 2, py + (2 if sy else 0), "cg0")
        L.vline(px + (2 if sx else 0), py, py + 2, "cg0")
    L.blit(["k   ", " k  ", " kk ", "   k"], {"k": "cg1"}, 68, 37)
    s.names = {"NW": (0, 0), "N": (1, 0), "NE": (2, 0), "W": (0, 1), "C": (1, 1), "E": (2, 1),
               "SW": (0, 2), "S": (1, 2), "SE": (2, 2), "inNW": (3, 0), "inNE": (4, 0),
               "inSW": (3, 1), "inSE": (4, 1), "C2": (4, 2)}
    return finish(s)


def steps():
    s = struct("steps", "Broad steps", 3, 2, walk=["...", "..."], ground="none",
               notes="Four worn treads climbing north, two per row: west cheek, run (repeat "
                     "it for width), east cheek. The Kadmeia's broad stair, and the temple's "
                     "and the Asclepeion's steps.")
    L = s.B
    W = 48
    for k in range(4):
        y = k * 8
        L.rect(0, y, W, 8, "cg4")
        L.hline(0, W - 1, y, "cg5")
        L.hline(0, W - 1, y + 1, "cg5")
        L.hline(0, W - 1, y + 5, "cg3")
        L.hline(0, W - 1, y + 6, "cg2")
        L.hline(0, W - 1, y + 7, "cg1")
        # wear in the middle of each tread
        for x in range(0, W, 16):
            L.px(x + 6, y + 3, "cg3")
            L.px(x + 11, y + 2, "cg3")
    for x0, lit in ((0, True), (W - 5, False)):
        L.rect(x0, 0, 5, 32, "cg3" if lit else "cg2")
        L.vline(x0, 0, 31, "cg0")
        L.vline(x0 + 4, 0, 31, "cg0")
        L.vline(x0 + 1, 0, 31, "cg5" if lit else "cg3")
        L.vline(x0 + 3, 0, 31, "cg2" if lit else "cg1")
        for y in range(7, 32, 8):
            L.hline(x0 + 1, x0 + 3, y, "cg1")
    s.names = {"W": (0, 0), "run": (1, 0), "E": (2, 0), "W2": (0, 1), "run2": (1, 1), "E2": (2, 1)}
    return finish(s)


def _lip(L, x0, x1, y=0):
    """The dressed coping along the top of a terrace wall."""
    for x in range(x0, x1):
        L.px(x, y, "cg5")
        L.px(x, y + 1, "cg4" if x % 16 else "cg2")
        L.px(x, y + 2, "cg2")
        L.px(x, y + 3, "cg0")


def terrace_wall():
    s = struct("terrace", "Cyclopean terrace wall", 5, 1, walk=["XXXX."], ground="none",
               notes="A retaining wall one cell tall, the upper level to the north, in the city "
                     "wall's masonry under a dressed coping: (0) west end, (1)-(2) the run, an "
                     "even/odd pair (put (1) on even map columns), (3) east end, (4) a narrow "
                     "stair up through the wall (walkable).")
    L = s.B
    for i in range(5):
        T.fill_masonry(L, i * 16, 0, 16, 16, "wall", ox=-16 * (i % 2), oy=-16)
    _lip(L, 0, 80)
    # ends: the wall's dressed quoins
    for x0, lit in ((0, True), (48, False)):
        xs = range(x0, x0 + 4) if lit else range(x0 + 12, x0 + 16)
        for x in xs:
            for y in range(16):
                L.px(x, y, "cg4" if lit else "cg2")
        L.vline(x0 if lit else x0 + 15, 0, 15, "cg0")
        for y in range(4, 16, 6):
            L.hline(xs[0], xs[-1], y, "cg1")
    # a narrow stair through the wall
    x0 = 64
    for k in range(4):
        y = k * 4
        L.rect(x0 + 2, y, 12, 4, "cg4")
        L.hline(x0 + 2, x0 + 13, y, "cg5")
        L.hline(x0 + 2, x0 + 13, y + 3, "cg2")
    L.vline(x0 + 1, 0, 15, "cg0")
    L.vline(x0 + 14, 0, 15, "cg0")
    s.names = {"W": (0, 0), "run": (1, 0), "run_odd": (2, 0), "E": (3, 0), "stair": (4, 0)}
    return finish(s)


def parapet():
    s = struct("parapet", "The Kadmeia's parapet", 4, 1, walk=["XXXX"], ground="none",
               notes="The top of the Kadmeia's retaining wall seen from above: a low parapet "
                     "of squared blocks along the citadel's edge, with its wall-walk behind. "
                     "Lay it as the row above a terrace wall: (0) west end, (1) run, (2) east "
                     "end, (3) a run with a worn stone seat built into it (Manto's).")
    L = s.B
    T.paving(L, 0, 0, 64, 16)
    for x in range(64):
        for y in range(7, 16):
            X = x % 16
            c = "cg4"
            if y == 7:
                c = "cg5"
            elif y in (14, 15):
                c = "cg1" if y == 14 else "cg0"
            elif X == 15:
                c = "cg2"
            elif y == 13:
                c = "cg3"
            L.px(x, y, c)
        L.px(x, 6, "cg0")
    for x0, lit in ((0, True), (32, False)):
        x = x0 if lit else x0 + 15
        L.vline(x, 6, 15, "cg0")
    # Manto's seat: a smoothed block with a sheepskin
    L.rect(52, 8, 9, 4, "cg5")
    L.hline(52, 60, 11, "cg3")
    L.blit([" eeeee ", "eeeeeee"], {"e": "cg5"}, 53, 6)
    s.names = {"W": (0, 0), "run": (1, 0), "E": (2, 0), "seat": (3, 0)}
    return finish(s)


# ==========================================================================
# The city wall
# ==========================================================================

MERLON = 10   # px of merlon in every 16


def _battlement(L, x0, w, y0=0, walk_rows=8):
    """The wall's top row seen from the south: the wall-walk's flags behind,
    then a row of merlons standing on the outer (south) edge."""
    T.paving(L, x0, y0, w, walk_rows)
    for x in range(x0, x0 + w):
        X = (x - x0) % 16
        L.px(x, y0 + walk_rows - 1, "cg2")
        merlon = 2 <= X < 2 + MERLON
        top = y0 + 2 if merlon else y0 + walk_rows
        for y in range(top, y0 + 16):
            c = "cg4"
            if y == top:
                c = "cg5"
            elif y >= y0 + 14:
                c = "cg2"
            elif merlon and X in (2, 3):
                c = "cg5"
            elif merlon and X in (2 + MERLON - 2, 2 + MERLON - 1):
                c = "cg3"
            L.px(x, y, c)
        if merlon:
            L.px(x, top - 1, "cg0")
        if X in (2, 2 + MERLON - 1):
            for y in range(y0 + 2, y0 + walk_rows):
                L.px(x, y, "cg0")
    L.hline(x0, x0 + w - 1, y0 + 15, "cg1")


def _face(L, x0, y0, w, h, cx0, cy0):
    """Cyclopean face, its texture phased by the map column and row of the
    structure's top-left cell (cx0, cy0)."""
    T.fill_masonry(L, x0, y0, w, h, "wall", ox=x0 - 16 * (cx0 % 2) * 0 - 16 * (cx0 % 2),
                   oy=y0 - 16 * (cy0 % 2))


def wall_face():
    s = struct("wall", "City wall, north and south faces", 4, 3,
               walk=["XXXX"] * 3, ground="none",
               notes="The wall's three rows: the battlement (wall-walk and merlons), then two "
                     "rows of Cyclopean face. Columns: (0) west end, the face's corner, for an "
                     "even map column; (1)-(2) the run, an even/odd pair, (1) on even map "
                     "columns; (3) east end, for an odd map column. The battlement row is the "
                     "same in every column but the corners. Where the north wall meets a "
                     "north-south strip, the run simply stops against the strip.")
    L = s.B
    _battlement(L, 0, 64)
    # the face: two rows, texture phased so (1) is even, (2) odd
    for i in range(4):
        T.fill_masonry(L, i * 16, 16, 16, 32, "wall", ox=16 * (i % 2) * 0 + i * 16 - 16 * (i % 2),
                       oy=16)
    # the face's string course under the battlement
    for x in range(64):
        L.px(x, 16, "cg0")
        L.px(x, 17, "cg2")
    # outer corners: dressed quoins up the face's ends
    for x0, lit in ((0, True), (48, False)):
        for y in range(0, 48):
            for k in range(4):
                x = x0 + k if lit else x0 + 15 - k
                if y >= 16:
                    c = ("cg4", "cg4", "cg3", "cg0")[k] if lit else ("cg0", "cg1", "cg2", "cg2")[k]
                    if (y - 16) % 8 == 7:
                        c = "cg1" if k < 3 else "cg0"
                    L.px(x, y, c)
        L.vline(x0 if lit else x0 + 15, 0, 47, "ink")
    s.names = {"W": (0, 0), "run": (1, 0), "run_odd": (2, 0), "E": (3, 0)}
    return finish(s)


def wall_ivy():
    """Ivy cascades over the wall's face: the face's own tiles under the ivy, so
    only the ivy costs tiles."""
    s = struct("wall_ivy", "City wall face under ivy", 1, 3, walk=["X"] * 3, ground="none",
               notes="A drop-in replacement for wall's even run cell (put it on an even map "
                     "column), ivy pouring over the battlement and down the face.")
    L = s.B
    _battlement(L, 0, 16)
    T.fill_masonry(L, 0, 16, 16, 32, "wall", ox=0, oy=16)
    for x in range(16):
        L.px(x, 16, "cg0")
        L.px(x, 17, "cg2")
    M = s.M
    T.ivy_drape(M, 1, 12, 14, 26, seed=5, top_full=8)
    s.names = {"run": (0, 0)}
    return finish(s)


def _strip(L, x0, y0, h, outer_west=True):
    """A north-south wall seen from above, 32 px wide: merlons on the outer edge,
    the wall-walk, a lip on the inner edge and the start of its shadow."""
    for y in range(y0, y0 + h):
        Y = (y - y0) % 16
        for k in range(32):
            x = x0 + k if outer_west else x0 + 31 - k
            if k < 2:
                c = "cg0" if k == 0 else "cg2"
            elif k < 9:
                merlon = 2 <= Y < 2 + MERLON
                c = ("cg5" if k == 2 else "cg4" if k < 7 else "cg3") if merlon else "cg2"
                if merlon and Y in (2,):
                    c = "cg5"
                if merlon and Y == 1 + MERLON:
                    c = "cg1"
                if not merlon and k == 2:
                    c = "cg1"
            elif k == 9:
                c = "cg1"
            elif k < 26:
                c = None
            elif k == 26:
                c = "cg5"
            elif k < 29:
                c = "cg4"
            elif k == 29:
                c = "cg2"
            else:
                c = "cg0" if k == 30 else "cg1"
            if c:
                L.px(x, y, c)
    # the wall-walk's flags between
    for y in range(y0, y0 + h):
        for k in range(10, 26):
            x = x0 + k if outer_west else x0 + 31 - k
            tex = T.masonry("flag")
            L.px(x, y, tex[(y - y0) % 16][k % 16])


def wall_strip():
    s = struct("strip", "City wall, west side, seen from above", 2, 2,
               walk=["XX", "XX"], ground="none",
               notes="The west wall runs north-south as a strip two cells wide: merlons on its "
                     "outer (west) edge, the wall-walk, and a lip on the inner edge. Row 0 is "
                     "the run; repeat it. Row 1 is its south end, where it turns into the "
                     "south wall's battlement (lay it in the battlement's row; the face below "
                     "it is the wall's west end). strip_e is the east wall, mirrored.")
    L = s.B
    _strip(L, 0, 0, 16)
    # the south end: the battlement turns the corner
    _battlement(L, 0, 32, y0=16)
    _strip(L, 0, 16, 8)
    for x in range(0, 9):
        for y in range(18, 32):
            L.px(x, y, "cg4" if x > 1 else ("cg0" if x == 0 else "cg2"))
    L.vline(0, 16, 31, "ink")
    s.names = {"run": (0, 0), "run_in": (1, 0), "end": (0, 1), "end_in": (1, 1)}
    return finish(s)


def side_gate():
    s = struct("side_gate", "A gate through the west wall", 2, 5,
               walk=["XX", "XX", "..", "XX", "XX"], ground="none",
               notes="A gate through a north-south strip, for the Neistan Gate: two square "
                     "towers seen from above and from the south, and the road between them "
                     "under the gate's lintel (row 2, walkable; the lintel draws over the "
                     "player). Rows: 0 the north tower's top, 1 its face, 2 the passage, 3 the "
                     "south tower's top, 4 its face. side_gate_e is the Proitid Gate, "
                     "mirrored. Lay the strip's run above and below it.")
    L, Tl = s.B, s.T
    W = 32
    for y0 in (0, 48):
        # the tower's top: a platform with merlons all round
        T.paving(L, 0, y0, W, 16)
        for x in range(W):
            for y in (y0, y0 + 1):
                L.px(x, y, "cg5" if y == y0 + 1 else "cg0")
            if x % 8 < 5:
                L.px(x, y0 + 2, "cg4")
                L.px(x, y0 + 3, "cg3")
        for y in range(y0, y0 + 16):
            L.px(0, y, "ink")
            L.px(1, y, "cg5")
            L.px(W - 1, y, "ink")
            L.px(W - 2, y, "cg2")
        L.hline(0, W - 1, y0 + 15, "cg0")
        # the tower's south face
        T.fill_masonry(L, 0, y0 + 16, W, 16, "wall", ox=0, oy=y0 + 16)
        L.vline(0, y0 + 16, y0 + 31, "ink")
        L.vline(W - 1, y0 + 16, y0 + 31, "ink")
        L.vline(1, y0 + 16, y0 + 31, "cg4")
        L.vline(W - 2, y0 + 16, y0 + 31, "cg1")
        # an arrow slit
        L.vline(15, y0 + 20, y0 + 27, "ink")
        L.vline(16, y0 + 20, y0 + 27, "ink")
        L.px(15, y0 + 19, "cg0")
    # the passage: road flags in the gate's shadow, the lintel over it
    T.paving(L, 0, 32, W, 16)
    for y in range(32, 48):
        for x in range(W):
            c = L.get(x, y)
            if y < 38:
                L.px(x, y, {"cg5": "cg3", "cg4": "cg2", "cg3": "cg2", "cg2": "cg1"}.get(c, c))
    # the lintel: a single huge block spanning the passage, on the top layer
    for x in range(W):
        Tl.px(x, 32, "ink")
        Tl.px(x, 33, "cg4")
        Tl.px(x, 34, "cg3")
        Tl.px(x, 35, "cg2")
        Tl.px(x, 36, "cg0")
    s.names = {"tower_top": (0, 0), "tower_face": (0, 1), "passage": (0, 2)}
    return finish(s)


def bricked_side_gate():
    s = struct("side_gate_bricked", "A bricked-up gate in the west wall", 2, 1,
               walk=["XX"], ground="none",
               notes="side_gate's passage, walled up with rubble and mortar: put it in place "
                     "of row 2 for one of Thyrsa's four shut gates.")
    L = s.B
    _bricks(L, 0, 0, 32, 16)
    for x in range(32):
        L.px(x, 0, "ink")
        L.px(x, 1, "cg4")
        L.px(x, 2, "cg2")
    return finish(s)


def _bricks(L, x0, y0, w, h):
    """A gate walled up in a hurry: rubble courses of small blocks, mortar pale."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            Y = (y - y0)
            row = Y // 4
            off = 3 if row % 2 else 0
            X = (x - x0 + off) % 7
            c = "cg2"
            if Y % 4 == 3 or X == 6:
                c = "cg4"
            elif Y % 4 == 0:
                c = "cg3"
            elif (x * 5 + y * 3) % 11 == 0:
                c = "cg1"
            L.px(x, y, c)


def bricked_arch():
    s = struct("arch_bricked", "A bricked-up gate in the wall's face", 2, 1,
               walk=["XX"], ground="none",
               notes="One of Thyrsa's four shut gates, set in a wall face: a low round arch of "
                     "dressed voussoirs, walled up with rubble, a votive niche in the fill. Lay "
                     "it in the face's lower row (an even map row) at an even map column. 'A "
                     "bricked-up gate. Thyrsa had seven. It uses three.'")
    L = s.B
    T.fill_masonry(L, 0, 0, 32, 16, "wall", ox=0, oy=0)
    cx = 15.5
    for y in range(16):
        for x in range(32):
            dx = x - cx
            # arch: semicircle of radius 11 springing at y=12, jambs below
            r = ((dx) ** 2 + (max(0, 12 - y)) ** 2) ** 0.5
            inside = r < 9 and y > 2
            ring = 9 <= r < 12.5 and y >= 0
            if inside:
                L.px(x, y, None)
            elif ring:
                ang = (dx / max(r, 1))
                L.px(x, y, "cg5" if (x + y) % 5 == 0 else ("cg4" if dx < 0 else "cg3"))
                if 11.8 <= r:
                    L.px(x, y, "cg0")
    _bricks_mask = [(x, y) for y in range(16) for x in range(32) if L.get(x, y) is None]
    tmp = T.Layer(32, 16)
    _bricks(tmp, 0, 0, 32, 16)
    for (x, y) in _bricks_mask:
        L.px(x, y, tmp.get(x, y))
    # a votive niche in the rubble (the Rare Candy's hiding place on the Kadmeia)
    L.rect(14, 8, 4, 5, "cg0")
    L.hline(13, 18, 13, "cg4")
    return finish(s)


def elektran_gate():
    s = struct("elektran", "The Elektran Gate", 8, 5,
               walk=["XX....XX", "XX....XX", "XXTTTTXX", "XXTTTTXX", "XX....XX"], ground="none",
               notes="Thyrsa's main gate, in the south wall: a wide arch of dressed voussoirs "
                     "between two square towers that rise a row above the battlement, ivy and "
                     "festival garlands on them, the gate's bronze-bound leaves folded back "
                     "against the jambs. Lay it with its row 2 in the south wall's battlement "
                     "row, at an even map column; rows 0-1 between the towers are the street "
                     "inside the gate (paved). The passage, columns 2-5 of rows 2-4, is "
                     "walkable; rows 2-3 draw the wall over the player.")
    L, Tl = s.B, s.T
    W = 128
    # the street inside, and the passage's floor
    T.paving(L, 32, 0, 64, 80)
    # the towers: top platforms (row 0) and faces (rows 1-4)
    for x0 in (0, 96):
        T.paving(L, x0, 0, 32, 16)
        for x in range(x0, x0 + 32):
            L.px(x, 0, "cg0")
            L.px(x, 1, "cg5")
            if (x - x0) % 8 < 5:
                L.px(x, 2, "cg4")
                L.px(x, 3, "cg3")
                L.px(x, 13, "cg4")
                L.px(x, 12, "cg5")
            L.px(x, 14, "cg2")
            L.px(x, 15, "cg0")
        T.fill_masonry(L, x0, 16, 32, 64, "wall", ox=x0, oy=16)
        for y in range(0, 80):
            L.px(x0, y, "ink")
            L.px(x0 + 31, y, "ink")
            L.px(x0 + 1, y, "cg5" if y < 16 else "cg4")
            L.px(x0 + 30, y, "cg2" if y < 16 else "cg1")
        # a slit window and a string course
        L.vline(x0 + 15, 22, 30, "ink")
        L.vline(x0 + 16, 22, 30, "ink")
        for x in range(x0 + 1, x0 + 31):
            L.px(x, 32, "cg0")
            L.px(x, 33, "cg2")
    # the wall over the arch: battlement (row 2) and face (rows 3-4), on the top layer
    tmp = T.Layer(W, 80)
    _battlement(tmp, 32, 64, y0=32)
    T.fill_masonry(tmp, 32, 48, 64, 32, "wall", ox=32, oy=16)
    for x in range(32, 96):
        tmp.px(x, 48, "cg0")
        tmp.px(x, 49, "cg2")
    # cut the arch out of the face: a semicircle springing low in row 4
    cx, spring, R = 63.5, 70, 30
    for y in range(48, 80):
        for x in range(32, 96):
            dx = x - cx
            dy = max(0, spring - y)
            r = (dx * dx + dy * dy) ** 0.5
            if r < R - 4:
                tmp.px(x, y, None)
            elif r < R:
                # voussoirs, alternating light and shaded, radial joints
                ang = (dx + 40) // 6
                tmp.px(x, y, "cg5" if ang % 2 else "cg4")
                if r >= R - 1 or (dx + 40) % 6 == 0:
                    tmp.px(x, y, "cg1")
                if r < R - 3:
                    tmp.px(x, y, "cg2")
    Tl.copy_from(tmp)
    # the passage's dark interior under the arch, and the leaves folded back
    for y in range(32, 80):
        for x in range(32, 96):
            c = L.get(x, y)
            shade = {"cg5": "cg2", "cg4": "cg2", "cg3": "cg1", "cg2": "cg1", "cb": "cg1"}
            if y < 72:
                L.px(x, y, shade.get(c, c) if y >= 40 else {"cg5": "cg3", "cg4": "cg3", "cg3": "cg2",
                                                             "cg2": "cg1"}.get(c, c))
    for x0, d in ((32, 1), (95, -1)):
        for k in range(6):
            x = x0 + k * d
            for y in range(50, 79):
                L.px(x, y, "cg1" if k in (0, 5) else ("cg3" if k == 1 else "cg2"))
            for y in (56, 66, 76):
                L.px(x, y, "cg0")
        L.px(x0 + 2 * d, 61, "cg5")
    T.mirror_half(L, 32, 64, 0, 80)
    T.mirror_half(Tl, 32, 64, 32, 80)
    s.names = {"passage": (2, 4)}
    return finish(s)


def theater_gate():
    s = struct("theater_gate", "The theater's high gate", 3, 4,
               walk=["XXX", "XXX", "XXX", "XDX"], ground="none",
               notes="The gate in the east wall onto the theater terrace: a little propylon of "
                     "two Doric columns under a pediment, a comic and a tragic mask over the "
                     "doorway, the doors standing open on the dark of the theater's upper "
                     "passage. Door: bottom row, middle (MB_NON_ANIMATED_DOOR); the warp to "
                     "MAP_THYRSA_THEATER goes there. Its top row stands on the flags.")
    s.ground_rows(["ppp", "nnn", "nnn", "nnn"])
    L = s.B
    W = 48
    # pediment and roof
    cx = (W - 1) / 2
    for x in range(W):
        top = int(round(2 + 12 * abs(x - cx) / cx))
        for y in range(0, 16):
            if y < top:
                continue
            c = "cg4"
            if y == top:
                c = "ink"
            elif y == top + 1:
                c = "cg5"
            elif y == top + 2:
                c = "cg3"
            elif y > top + 2:
                c = "cb"
            L.px(x, y, c)
    for x in range(W):
        L.px(x, 15, "cg0")
    # entablature: an ivy garland on the frieze
    for x in range(W):
        for y in range(16, 24):
            L.px(x, y, "cg4" if y < 18 else "cg3")
        L.px(x, 16, "cg5")
        L.px(x, 23, "cg1")
        sag = int(2 * abs(((x % 12) - 6)) / 6)
        L.px(x, 19 + 2 - sag, "iv1")
        L.px(x, 20 + 2 - sag, "iv2" if x % 2 else "iv0")
    # the back wall and the doorway
    T.fill_masonry(L, 0, 24, W, 40, "wall", ox=0, oy=16)
    L.rect(14, 30, 20, 34, "ink")
    L.rect(16, 32, 16, 32, "cg0")
    for y in range(32, 64):
        L.px(16, y, "cg1")
    L.rect(13, 28, 22, 3, "cg5")
    L.hline(13, 34, 30, "cg2")
    # columns
    for x0 in (3, 38):
        L.rect(x0, 24, 7, 40, "cg4")
        L.vline(x0, 24, 63, "ink")
        L.vline(x0 + 6, 24, 63, "ink")
        L.vline(x0 + 1, 24, 63, "cg5")
        L.vline(x0 + 5, 24, 63, "cg2")
        L.vline(x0 + 3, 26, 61, "cg3")
        L.rect(x0 - 1, 24, 9, 2, "cg5")
        L.hline(x0 - 1, x0 + 7, 25, "cg2")
        L.rect(x0 - 1, 61, 9, 3, "cg3")
        L.hline(x0 - 1, x0 + 7, 63, "cg1")
    T.mirror_half(L, 0, W, 0, 64)
    # the masks, comic and tragic, after the mirroring
    tmp = T.Layer(W, 64)
    T.mask(tmp, 12, 4, "comic", hair=True)
    T.mask(tmp, 28, 4, "tragic", hair=True)
    # in the stone's own colors, so the masks share the pediment's tiles' palette
    stone = {"ink": "cg0", "w0": "w0", "rd": "e1", "g0": "e2", "iv1": "iv1", "iv2": "iv2"}
    for yy in range(64):
        for xx in range(W):
            c = tmp.get(xx, yy)
            if c:
                L.px(xx, yy, stone[c])
    s.names = {"door": (1, 3)}
    return finish(s)


def stele():
    s = struct("stele", "A stone stele on the flags", 1, 1, walk=["X"], ground="pave",
               notes="A stone stele with a pediment, painted letters and an ivy wreath, for "
                     "signs on the paving (aethos's 0x003 stands on grass).")
    M = s.M
    M.blit([
        "    kkkkkk    ",
        "   kwwwwwwk   ",
        "  kkkkkkkkkk  ",
        "   kwwwwwwk   ",
        "   kw3w3wwk   ",
        "   kwwwwwwk   ",
        "   kw33w3wk   ",
        "   kwwwwwwk   ",
        "   kw3w33wk   ",
        "   kwwwwwwk   ",
        "   k222222k   ",
        "  kkkkkkkkkk  ",
        "  k22222222k  ",
        "  kkkkkkkkkk  ",
    ], {"k": "cg0", "w": "cg5", "3": "cg1", "2": "cg3"}, 1, 1)
    for x in range(5, 11):
        M.px(x, 3, "iv2" if x % 2 else "iv1")
    s.names = {"sign": (0, 0)}
    return finish(s)


def build_streets():
    return [paving_set(), kerbs(), steps(), terrace_wall(), parapet(), stele()]


def _mirrored(s, key, title, notes, names):
    t = T.mirror(s, key, title, notes=notes)
    t.names = names
    return t


def build_walls():
    strip = wall_strip()
    gate = side_gate()
    strip_e = _mirrored(strip, "strip_e", "City wall, east side, seen from above",
                        "The east wall: strip, mirrored (its tiles are the west wall's, flipped).",
                        {"run": (1, 0), "run_in": (0, 0), "end": (1, 1), "end_in": (0, 1)})
    gate_e = _mirrored(gate, "side_gate_e", "A gate through the east wall",
                       "The Proitid Gate: side_gate, mirrored.",
                       {"tower_top": (1, 0), "tower_face": (1, 1), "passage": (1, 2)})
    out = [wall_face(), wall_ivy(), strip, strip_e, gate, gate_e, bricked_arch(), elektran_gate(),
           theater_gate()]
    return out
