"""Skiron tombs: the roadside dead. Grave stelai, marble lekythoi, a
sarcophagus, the walls of a family plot, a burial mound, a milestone; and the
toppled tomb the Titans brought down across the road, as rubble that a relic
breaks and the road it leaves behind.

Greek roads out of a city were lined with the dead: families built their
plots along the road so that every traveller would pass them, read the names
and remember. Pentelic-white marble, painted ribbons, myrtle.
"""
from __future__ import annotations

import math

import numpy as np

from skiron_ground import FULL, paint_road
from skiron_lib import Layer, Struct, disc, ground, oval_shadow, regrounded

SEC = "tombs"


def outline(L, color="ink"):
    a = L.a[..., 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        L.px(x, y, color)


def split_tall(s, art, top_rows=1):
    """A 1-wide tall monument on borrowed grass: the top rows drawn over the
    player (T), the rest in the middle layer."""
    ground(s, "grass")
    for cy in range(s.h):
        dst = s.T if cy < top_rows else s.M
        dst.a[cy * 16:cy * 16 + 16] = art.a[cy * 16:cy * 16 + 16]
    return s


def plinth(L, x0, x1, y0, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            L.px(x, y, "m2" if y > y0 else "m1")
    L.vline(x1, y0, y1, "m3")
    L.hline(x0, x1, y1, "m3")


# --------------------------------------------------------------------------
# Grave stelai and lekythoi
# --------------------------------------------------------------------------

def stele_family():
    """The pedimented stele with a seated woman holding a small girl's hand."""
    s = Struct("stele_family", "Grave stele: the seated woman", 1, 2, SEC, walk=["T", "X"],
               notes="A pedimented marble stele carved with a seated woman holding a small "
                     "girl's hand (the mourner's grandmother, Route 4). The pediment is drawn "
                     "over the player.")
    A = Layer(16, 32)
    oval_shadow(A, 8, 30, 7, 2)
    A.rect(2, 7, 12, 21, "m1")                       # the slab
    A.poly([(1, 7), (8, 1), (14, 7)], "m1")          # pediment
    A.hline(1, 14, 7, "m2")
    A.hline(2, 13, 8, "m3")
    A.px(1, 6, "m1")
    A.px(14, 6, "m1")
    A.px(8, 2, "w0")
    A.rect(3, 9, 10, 15, "m2")                       # the recessed field
    A.vline(3, 9, 23, "m3")
    A.hline(3, 9, 12, "m3")
    # the woman seated left, the girl standing right, hands joined
    A.blit([
        " hh       ",
        " hm       ",
        " ww    h  ",
        "wwww   m  ",
        "wwwwHHww  ",
        "wwww  ww  ",
        "cwww  ww  ",
        "cwwwww w  ",
        "c www  w  ",
        "c w w  w  ",
        "c w w ww  ",
    ], {"h": "m4", "m": "m3", "w": "w0", "H": "m3", "c": "m3"}, 3, 11)
    A.rect(1, 24, 14, 5, "m2")                       # the base
    A.hline(1, 14, 24, "m1")
    A.hline(2, 12, 26, "m3")                         # the name cut in it
    A.vline(14, 7, 28, "m3")
    outline(A)
    A.px(8, 27, "tc1")                               # a red ribbon
    A.px(9, 28, "tc1")
    return split_tall(s, A)


def stele_palmette():
    s = Struct("stele_palmette", "Grave stele: the palmette shaft", 1, 2, SEC, walk=["T", "X"],
               notes="A tall slender shaft crowned with a carved palmette, two rosettes and "
                     "a painted name band. A red ribbon is tied round it. The finial is drawn "
                     "over the player.")
    A = Layer(16, 32)
    oval_shadow(A, 8, 30, 6, 2)
    A.rect(5, 8, 6, 20, "m1")
    A.vline(10, 8, 27, "m3")
    A.vline(5, 8, 27, "w0")
    # palmette: a fan of leaves over volutes
    A.blit([
        "  w w w  ",
        " wmwmwmw ",
        " wmwwwmw ",
        "  wmwmw  ",
        " mwwmwwm ",
        "  mm mm  ",
    ], {"w": "w0", "m": "m2"}, 4, 1)
    A.hline(4, 11, 7, "m2")
    for y in (12, 17):
        A.blit([" m ", "mwm", " m "], {"m": "m3", "w": "w0"}, 6, y)
    A.hline(6, 9, 22, "tc1")                          # the painted name band
    A.hline(6, 9, 23, "m3")
    A.hline(5, 10, 10, "tc1")                         # the ribbon
    A.px(4, 11, "tc1")
    A.px(4, 12, "tc1")
    plinth(A, 3, 12, 27, 29)
    outline(A)
    return split_tall(s, A)


def stele_low():
    s = Struct("stele_low", "A small grave marker", 1, 1, SEC, walk=["X"],
               notes="A low rounded marker for a poorer grave, a ribbon and a sprig of myrtle "
                     "laid on it. Impassable.")
    ground(s, "grass")
    A = s.M
    oval_shadow(A, 8, 14, 6, 2)
    A.ellipse(4, 3, 11, 10, "m1")
    A.rect(4, 7, 8, 6, "m1")
    A.vline(11, 6, 12, "m3")
    A.hline(5, 10, 9, "m3")
    A.rect(3, 12, 10, 2, "m2")
    outline(A)
    A.hline(5, 10, 6, "tc1")
    A.px(4, 7, "tc1")
    A.blit(["cc", " cc"], {"c": "c2"}, 7, 11)
    return s


def lekythos():
    s = Struct("lekythos", "Marble lekythos on its plinth", 1, 2, SEC, walk=["T", "X"],
               notes="A marble oil flask taller than a child, set on a stepped plinth over a "
                     "grave: the mourners' vase made permanent. A relief band of a farewell "
                     "handshake runs round its belly. The neck is drawn over the player.")
    A = Layer(16, 32)
    oval_shadow(A, 8, 30, 7, 2)
    A.rect(6, 0, 4, 2, "m1")                          # mouth
    A.rect(7, 2, 2, 4, "m2")                          # neck
    A.px(7, 2, "w0")
    A.ellipse(3, 5, 12, 9, "m1")                      # shoulder
    A.rect(4, 8, 8, 14, "m1")                         # body
    A.vline(4, 8, 21, "w0")
    A.vline(5, 8, 21, "w0")
    A.vline(11, 7, 21, "m3")
    A.vline(10, 9, 21, "m2")
    A.hline(5, 10, 21, "m2")
    A.rect(6, 22, 4, 2, "m2")                         # foot
    A.blit(["m m ", "mm m", "m mm"], {"m": "m3"}, 6, 13)   # the relief band
    A.hline(4, 11, 12, "m2")
    A.hline(4, 11, 17, "m2")
    A.line(12, 6, 13, 9, "m2")                        # the handle
    A.px(13, 10, "m2")
    plinth(A, 3, 12, 24, 26)
    plinth(A, 2, 13, 27, 29)
    outline(A)
    return split_tall(s, A)


def sarcophagus():
    s = Struct("sarcophagus", "A sarcophagus by the road", 2, 1, SEC, walk=["XX"],
               notes="A marble chest under a gabled lid with corner acroteria, a garland "
                     "carved along its side. Impassable.")
    ground(s, "grass")
    A = s.M
    oval_shadow(A, 16, 14, 15, 2)
    A.rect(2, 7, 28, 7, "m1")                         # the chest's long side
    A.hline(2, 29, 13, "m3")
    A.vline(29, 7, 13, "m3")
    for x in range(4, 28):                            # a carved garland swag
        y = 9 + int(round(2 * abs(math.sin(math.pi * (x - 4) / 8))))
        A.px(x, y, "m3")
    A.poly([(1, 7), (6, 2), (25, 2), (30, 7)], "m2")   # the lid, gabled
    A.hline(1, 30, 7, "w0")
    A.hline(6, 25, 2, "w0")
    A.line(1, 7, 6, 2, "w0")
    for x in (1, 29):
        A.rect(x, 4, 2, 3, "m1")                      # acroteria
    outline(A)
    return s


# --------------------------------------------------------------------------
# The family plot's walls
# --------------------------------------------------------------------------

PLOT_KEYS = ["EW", "EW2", "NS", "ES", "SW", "NE", "NW", "E", "W"]


def paint_plot_wall(L, ox, oy, key):
    """Fine ashlar, a coping of white marble. An east-west run shows its south
    face; a north-south run its coping from above, lit on the west."""
    n, e, s_, w = ("N" in key), ("E" in key), ("S" in key), ("W" in key)
    if key == "post":
        n = e = s_ = w = False
    ns = n or s_ or not (e or w)
    if ns:
        top = 0 if n else 4
        bot = 15 if s_ else 6
        for y in range(top, bot + 1):
            L.px(ox + 4, oy + y, "ink")
            L.px(ox + 5, oy + y, "w0")
            for x in range(6, 11):
                L.px(ox + x, oy + y, "m1" if x < 8 else "m2")
            L.px(ox + 11, oy + y, "m3")
            L.px(ox + 12, oy + y, "ink")
            if y % 8 == 7:
                L.hline(ox + 6, ox + 10, oy + y, "m3")
        if not n:
            L.hline(ox + 4, ox + 12, oy + top - 1, "ink")
        if not s_:
            # the column's end shows its face: poros under the marble coping
            for y in range(bot + 1, 15):
                for x in range(4, 13):
                    L.px(ox + x, oy + y, "l1" if (y - bot) % 4 == 0 or x == 12 else "p1")
                L.px(ox + 4, oy + y, "ink")
                L.px(ox + 12, oy + y, "ink")
            L.hline(ox + 4, ox + 12, oy + 15, "ink")
            L.hline(ox + 5, ox + 11, oy + bot + 1, "w0")
    if e or w:
        x0 = 0 if w else 4
        x1 = 15 if e else 12
        L.hline(ox + x0, ox + x1, oy + 1, "ink")
        L.hline(ox + x0, ox + x1, oy + 2, "w0")       # marble coping
        L.hline(ox + x0, ox + x1, oy + 3, "m1")
        L.hline(ox + x0, ox + x1, oy + 4, "m3")
        for y in range(5, 14):                         # a face of warm poros ashlar
            course = (y - 5) // 3
            for x in range(x0, x1 + 1):
                jx = (x + course * 4) % 8 == 7
                c = "l1" if (y - 5) % 3 == 2 or jx else "p1"
                L.px(ox + x, oy + y, c)
        L.hline(ox + x0, ox + x1, oy + 14, "ink")
        for x in range(x0, x1 + 1):
            if x % 2 == 0:
                L.px(ox + x, oy + 15, "gd")
        if not w:
            L.vline(ox + x0, oy + 1, oy + 14, "ink")
        if not e:
            L.vline(ox + x1, oy + 1, oy + 14, "ink")
        if key == "EW2":
            # an inscribed panel: the family's name
            L.rect(ox + 3, oy + 6, 10, 6, "m1")
            L.hline(ox + 3, ox + 12, oy + 6, "m3")
            L.vline(ox + 3, oy + 6, oy + 11, "m3")
            for x in range(5, 12, 2):
                L.px(ox + x, oy + 8, "m4")
                L.px(ox + x - 1, oy + 10, "m4")


def plot_walls():
    s = Struct("plot_wall", "Family plot walls: poros under a marble coping", 5, 2, SEC,
               walk=["XXXXX", "XXXXX"],
               names={k: (i % 5, i // 5) for i, k in enumerate(PLOT_KEYS)},
               notes="The walls of a family burial plot (a peribolos), fine ashlar under a "
                     "white coping, named by the sides they join (N E S W). The front wall "
                     "faces the road: run it east-west with `EW`, and `EW2` for the panel "
                     "carved with the family's name; `E`/`W` end it at a gateway. On "
                     "borrowed grass. Impassable.")
    for i, k in enumerate(PLOT_KEYS):
        paint_plot_wall(s.M, (i % 5) * 16, (i // 5) * 16, k)
    ground(s, "grass")
    return s


# --------------------------------------------------------------------------
# The burial mound and the milestone
# --------------------------------------------------------------------------

def mound():
    s = Struct("mound", "Burial mound", 3, 2, SEC, walk=["XXX", "XXX"],
               notes="An old tumulus, grassed over: a ring of kerbstones round its foot and a "
                     "small marker on its crown. Older than the road. Impassable.")
    ground(s, "grass")
    A = Layer(24, 32)
    # Drawn as its west half and mirrored, lit from above, so it costs half
    # its tiles. x is measured from the mound's middle (column 24).
    rx, ry, cy = 22.0, 17.0, 22
    for y in range(32):
        for x in range(24):
            d = 23.5 - x
            if (d / rx) ** 2 + ((y - cy) / ry) ** 2 > 1 or y > 28:
                continue
            u = (y - 6) / 22 + (d / rx) ** 2 * 0.5
            c = "g3" if u < 0.25 else "g2" if u < 0.55 else "g1" if u < 0.85 else "gd"
            if (x * 5 + y * 7) % 13 == 0:
                c = {"g3": "g2", "g2": "g1", "g1": "gd", "gd": "gd"}[c]
            A.px(x, y, c)
    # kerbstones round its foot, following the curve
    for x in range(1, 24):
        t = (23.5 - x) / rx
        if abs(t) >= 1:
            continue
        yb = min(28, int(cy + ry * math.sqrt(1 - t * t) * 0.42) + 6)
        for y in range(yb - 3, yb + 1):
            A.px(x, y, "m3" if x % 5 == 3 else ("m1" if y == yb - 3 else "m2"))
        A.px(x, yb + 1, "ink")
        if x % 2 == 0:
            A.px(x, yb + 2, "gd")
    a = A.a[..., 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2])
    for y, x in zip(*np.nonzero(edge)):
        if y < 24:
            A.px(x, y, "gd")
    # the marker on its crown (half of it)
    A.rect(22, 3, 2, 7, "m1")
    A.hline(22, 23, 2, "ink")
    A.vline(21, 3, 9, "ink")
    A.hline(21, 23, 10, "ink")
    A.px(23, 5, "tc1")
    s.M.a[:, 0:24] = A.a
    s.M.a[:, 24:48] = A.a[:, ::-1]
    return s


def milestone():
    s = Struct("milestone", "A milestone", 1, 1, SEC, walk=["X"],
               notes="A squat marble post cut with the miles to the city. Alethea sits on one "
                     "at the procession's camp. Impassable. `milestone_path` sits on the path.")
    ground(s, "grass")
    A = s.M
    oval_shadow(A, 8, 14, 6, 2)
    A.rect(4, 3, 8, 11, "m1")
    A.vline(4, 3, 13, "w0")
    A.vline(11, 3, 13, "m3")
    A.hline(4, 11, 3, "w0")
    for y in (6, 8, 10):
        A.hline(6, 9, y, "m3")
    A.px(7, 7, "m3")
    outline(A)
    return [s, regrounded(s, "milestone_path", "A milestone, on the path", "path")]


# --------------------------------------------------------------------------
# The toppled tomb: the Titans' rockslide
# --------------------------------------------------------------------------

def road_floor(s, cells):
    for (cx, cy) in cells:
        paint_road(s.B, cx * 16, cy * 16, FULL, "mid")


def block(A, x0, y0, w, h, face=3, carve=None):
    """A squared marble block lying askew: lit top, face below, ink outline."""
    A.rect(x0, y0, w, h, "m1")
    A.hline(x0, x0 + w - 1, y0, "w0")
    A.rect(x0, y0 + h - face, w, face, "m2")
    A.vline(x0 + w - 1, y0, y0 + h - 1, "m3")
    A.hline(x0, x0 + w - 1, y0 + h - face, "m3")
    if carve == "dentils":
        for x in range(x0 + 1, x0 + w - 1, 2):
            A.px(x, y0 + h - 2, "m4")
    if carve == "shovel":
        # Alethea's clue: fresh pick and shovel marks scored into the marble
        for i in range(3):
            A.line(x0 + 2 + i * 2, y0 + 1, x0 + 4 + i * 2, y0 + h - face - 1, "m3")


def drum(A, cx, cy, r):
    """A column drum lying with its flutes toward us."""
    m = disc(A.w, A.h, cx, cy, r, r)
    for y, x in zip(*np.nonzero(m)):
        a = math.atan2(y - cy, x - cx)
        A.px(x, y, "m2" if int((a + math.pi) / (2 * math.pi) * 16) % 2 else "m1")
    A.ellipse(cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2, "m1")
    A.px(cx, cy, "m3")


def lying_drum(A):
    """A column drum lying on its side, its flutes running along it, its cut
    end toward the west."""
    for y in range(5, 13):
        for x in range(5, 15):
            A.px(x, y, "w0" if y == 5 else "m3" if y == 12 else ("m1" if (y - 5) % 2 else "m2"))
    A.ellipse(1, 4, 8, 13, "m1")
    A.ellipse(2, 5, 7, 12, "m2")
    A.ellipse(3, 7, 6, 10, "m1")
    for (x, y) in ((1, 8), (2, 5), (5, 4), (7, 6), (7, 11), (4, 13), (1, 10)):
        A.px(x, y, "m3")                                   # the flutes' scallops at the cut end


def rubble():
    out = []
    s = Struct("rubble", "The toppled tomb: a heap of rubble", 2, 2, SEC, walk=["XX", "XX"],
               notes="Route 4's rockslide: a marble tomb pulled down across the road in heaps: "
                     "cornice blocks, a column drum, the pediment's palmette, dust, and fresh "
                     "shovel marks. The Bronze Hammer breaks it; swap in `rubble_cleared`. Its "
                     "floor is the paved road's `mid`.")
    road_floor(s, [(0, 0), (1, 0), (0, 1), (1, 1)])
    A = s.M
    # the heap itself: earth and broken marble piled across the road
    heap = disc(32, 32, 16, 18, 16, 14)
    heap[31:] = False
    for y, x in zip(*np.nonzero(heap)):
        h = (x * 7 + y * 5) % 11
        A.px(x, y, "m2" if h < 2 else "m3" if h < 4 else "l1" if h < 7 else "p1" if h < 9 else "m1")
    block(A, 1, 15, 14, 10, face=4, carve="dentils")       # a cornice block
    block(A, 16, 17, 14, 11, face=4, carve="shovel")       # an ashlar block, shovel-scored
    block(A, 8, 6, 13, 9, face=3, carve="shovel")          # one more, thrown on top
    drum(A, 25, 9, 6)                                      # a column drum
    block(A, 2, 5, 6, 6, face=2)                           # small pieces
    block(A, 12, 24, 5, 5, face=2)
    # the pediment's palmette finial, broken off and lying on the heap
    A.blit([" w w ", "wmwmw", " wmw ", "  m  "], {"w": "w0", "m": "m3"}, 21, 2)
    outline(A)
    for (x, y) in ((1, 29), (29, 30), (6, 31), (24, 31), (31, 24)):
        A.px(x, y, "m2")                                    # chips spilled on the road
    out.append(s)
    c = Struct("rubble_cleared", "The road where the rubble was", 2, 2, SEC,
               walk=["..", ".."],
               notes="Swapped in for `rubble` once it's broken: the paved road, white with "
                     "marble dust and chips. Walkable.")
    road_floor(c, [(0, 0), (1, 0), (0, 1), (1, 1)])
    # chips and dust in a few places only, so the rest is the road's own tiles
    for (x, y) in ((10, 11), (13, 13), (11, 14), (20, 18), (22, 20), (19, 21), (17, 17)):
        c.M.px(x, y, "w0")
        c.M.px(x + 1, y, "m2")
    for (x, y) in ((12, 12), (14, 11), (21, 19), (18, 20), (9, 13), (23, 17)):
        c.M.px(x, y, "m1")
    out.append(c)
    # one-cell versions for scattering and smaller obstacles
    s1 = Struct("rubble_small", "A small heap of rubble", 1, 1, SEC, walk=["X"],
                notes="One cell of marble rubble on the road; `rubble_small_cleared` replaces "
                      "it.")
    road_floor(s1, [(0, 0)])
    heap = disc(16, 16, 8, 9, 8, 7)
    heap[15:] = False
    for y, x in zip(*np.nonzero(heap)):
        h = (x * 7 + y * 5) % 11
        s1.M.px(x, y, "m2" if h < 2 else "m3" if h < 4 else "l1" if h < 7 else "p1" if h < 9 else "m1")
    block(s1.M, 1, 6, 9, 7, face=3, carve="shovel")
    block(s1.M, 7, 2, 8, 7, face=3)
    outline(s1.M)
    out.append(s1)
    c1 = Struct("rubble_small_cleared", "Where the small heap was", 1, 1, SEC, walk=["."],
                notes="The road with marble chips; walkable.")
    road_floor(c1, [(0, 0)])
    for (x, y) in ((9, 9), (12, 11), (10, 13)):
        c1.M.px(x, y, "w0")
        c1.M.px(x + 1, y, "m2")
    out.append(c1)
    # a loose piece lying in the grass (a fallen block is held for the budget)
    for key, title, fn in (("drum", "A fallen column drum", lying_drum),):
        t = Struct(key, title, 1, 1, SEC, walk=["X"],
                   notes="Debris from the toppled tomb, lying in the grass. Impassable.")
        ground(t, "grass")
        oval_shadow(t.M, 8, 14, 7, 2)
        fn(t.M)
        outline(t.M)
        out.append(t)
    return out


def build():
    return [stele_family(), stele_palmette(), stele_low(), lekythos(), sarcophagus(), plot_walls(),
            mound(), *milestone(), *rubble()]
