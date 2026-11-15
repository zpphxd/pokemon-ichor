"""Daedalus's workshop: the pieces for gTileset_Labyrinth's workshop section.

LABYRINTH.md §6 (Ring III) and §8 (scenes D and L): "A long vaulted room. Rows
of bronze automata stand still. On the bench sits a half-polished bronze collar.
A grate seals a shaft of grey light. A music box ticks."

Every piece here is drawn for the labyrinth palette plan (labyrinth_art.GROUPS).
Pieces standing on the slab floor come as twins, `<key>` for a top-left cell where
x + y is even and `<key>_odd` where it is odd, because the floor's slabs are two
cells long: the twins share every object tile and differ only in the floor drawn
under them.
"""
from __future__ import annotations

import copy
import math

import labyrinth_art as A
from labyrinth_art import Struct, blit

BZ = {"k": "ink", "0": "bz0", "1": "bz1", "2": "bz2", "3": "bz3", "4": "bz4", "w": "bw",
      "e": "be", "v": "bv0", "V": "bv1", "i": "bi0", "I": "bi1", "s": "ts0", "S": "ts1",
      "r": "brp"}
TM = {"k": "ink", "0": "tw0", "1": "tw1", "2": "tw2", "3": "tw3", "a": "tp0", "b": "tp1",
      "c": "tp2", "r": "tr", "g": "tg", "x": "tx", "B": "tb0", "L": "tb1", "q": "tq"}
MN = {"k": "ink", "0": "mt0", "1": "mt1", "2": "mt2", "R": "mr0", "r": "mr1", "o": "mo0",
      "O": "mo1", "y": "mo2", "g": "mg1", "G": "mg2", "b": "mb"}
FI = {"k": "ink", "e": "fe0", "E": "fe1", "f": "ff0", "c": "ff1", "y": "ff2", "w": "ff3",
      "1": "fz0", "2": "fz1", "3": "fz2", "i": "fi0", "I": "fi1"}


# --------------------------------------------------------------------------
# The floor under things, and the parity twins
# --------------------------------------------------------------------------

def on_floor(s, cells=None, odd=False):
    """Lay the slab floor in the bottom layer of `cells` (default: all of them)."""
    if cells is None:
        cells = [(x, y) for y in range(s.h) for x in range(s.w)]
    s.floor_cells = list(cells)
    for (cx, cy) in cells:
        A.slab(s.B, cx * 16, cy * 16, "l" if (cx + cy + odd) % 2 == 0 else "r")
    return s


def twins(s):
    """[s, its odd twin]. The odd twin's key ends in _odd and holds only the rows
    of s that show floor (a bench's top row has none), redrawn on the other
    parity; for those rows it replaces s's, the rest of s serves both."""
    rows = sorted({cy for (_, cy) in s.floor_cells})
    r0, r1 = rows[0], rows[-1] + 1
    t = copy.deepcopy(s)
    t.key = s.key + "_odd"
    t.title = s.title + " (odd cells)"
    on_floor(t, s.floor_cells, odd=True)
    if (r0, r1) != (0, s.h):
        t.h = r1 - r0
        for ln in t.layers:
            sub = A.K.Layer(t.w * 16, t.h * 16)
            sub.a[:] = t.layers[ln].a[r0 * 16:r1 * 16]
            t.layers[ln] = sub
        t.walk = t.walk[r0:r1]
        t.behaviors = {(x, y - r0): mb for (x, y), mb in t.behaviors.items() if r0 <= y < r1}
        t.ground = {(x, y - r0): g for (x, y), g in t.ground.items() if r0 <= y < r1}
        t.names = {n: (x, y - r0) for n, (x, y) in t.names.items() if r0 <= y < r1}
        t.floor_cells = [(x, y - r0) for (x, y) in s.floor_cells]
    t.twin_of = (s.key, r0)
    t.notes = (f"`{s.key}` for a top-left cell where x + y is odd" +
               (f": its rows {r0}-{r1 - 1}; keep `{s.key}`'s other rows." if (r0, r1) != (0, s.h)
                else "."))
    s.parity = "even"
    t.parity = "odd"
    return [s, t]


# --------------------------------------------------------------------------
# A small painter for bronze figures: parts, shaded left-lit, outlined in ink
# --------------------------------------------------------------------------

def _ramp(n, ramp=("bz4", "bz3", "bz2", "bz1", "bz0")):
    hi, l1, m, d1, d2 = ramp
    if n <= 1:
        return [m]
    if n == 2:
        return [l1, d1]
    if n == 3:
        return [l1, m, d1]
    if n == 4:
        return [hi, l1, m, d1]
    return [hi, l1] + [m] * (n - 4) + [d1, d2]


def _part_pixels(p):
    kind = p[0]
    px = set()
    if kind == "r":
        _, x, y, w, h = p[:5]
        px = {(x + i, y + j) for j in range(h) for i in range(w)}
    elif kind == "e":
        _, x0, y0, x1, y1 = p[:5]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rx, ry = (x1 - x0 + 1) / 2, (y1 - y0 + 1) / 2
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    px.add((x, y))
    elif kind == "t":
        _, y0, y1, a0, a1, b0, b1 = p[:7]
        for y in range(y0, y1 + 1):
            f = 0 if y1 == y0 else (y - y0) / (y1 - y0)
            l = round(a0 + (b0 - a0) * f)
            r = round(a1 + (b1 - a1) * f)
            px |= {(x, y) for x in range(l, r + 1)}
    elif kind == "p":
        px = set(p[1])
    return px


def figure(L, parts, x0=0, y0=0, ramp=None, ink=True):
    """Paint parts (see _part_pixels) shaded row by row, light on the left, and
    outline the union in ink. A part may end with a dict of options: ramp, top
    (a highlight color for its top row), color (one flat color)."""
    mask = set()
    for p in parts:
        opts = p[-1] if isinstance(p[-1], dict) else {}
        pix = _part_pixels(p)
        rows = {}
        for (x, y) in pix:
            rows.setdefault(y, []).append(x)
        rp = opts.get("ramp", ramp) or ("bz4", "bz3", "bz2", "bz1", "bz0")
        top = min(rows) if rows else 0
        for y, xs in rows.items():
            xs.sort()
            cols = _ramp(len(xs), rp)
            for i, x in enumerate(xs):
                c = opts.get("color") or cols[i]
                if y == top and opts.get("top") and i < len(xs) - 1:
                    c = opts["top"]
                L.px(x0 + x, y0 + y, c)
        if not opts.get("no_mask"):
            mask |= pix
    if ink:
        ring = set()
        for (x, y) in mask:
            for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q not in mask:
                    ring.add(q)
        for (x, y) in ring:
            L.px(x0 + x, y0 + y, "ink")
    return mask


# --------------------------------------------------------------------------
# The automata
# --------------------------------------------------------------------------

def plinth(M, x0, y0=16, plaque=None, rope=True):
    """An automaton's slate plinth in the lower cell, y 9-15 of it: a lit top face,
    a dark front, a bronze plaque. plaque: None (plain), or tally strokes as a
    string of '|' and 'P' (Attic numerals: P is five)."""
    rows = ["..kkkkkkkkkkkk..",
            ".kIIIIIIIIIIIIk.",
            ".kSSSSSSSSSSSSk.",
            ".kss33333333ssk.",
            ".kss21111112ssk.",
            ".kssssssssssssk.",
            "..kkkkkkkkkkkk.."]
    blit(M, rows, BZ, x0, y0 + 9)
    if plaque:
        # strokes over the plate, centred
        w = sum(3 if ch == "P" else 2 for ch in plaque) - 1
        x = x0 + 8 - (w + 1) // 2
        for ch in plaque:
            if ch == "P":
                M.px(x, y0 + 12, "ink")
                M.px(x + 1, y0 + 12, "ink")
                M.px(x, y0 + 13, "ink")
                x += 3
            else:
                M.px(x, y0 + 12, "ink")
                M.px(x, y0 + 13, "ink")
                x += 2
    if rope:
        # a ring in the plinth's top and a rope up to the figure's ankles
        M.px(x0 + 12, y0 + 10, "bz3")
        M.px(x0 + 12, y0 + 9, "ink")


def ankle_rope(M, x0, y, x1, x2):
    """The joke in the myth: Daedalus's statues had to be tied down or they'd walk
    off. A rope round the ankles at row y from x1 to x2, knotted, down to the plinth."""
    for x in range(x1, x2 + 1):
        M.px(x0 + x, y, "brp")
    M.px(x0 + x2 + 1, y, "brp")
    M.px(x0 + x2 + 1, y + 1, "brp")
    M.px(x0 + x2 + 2, y + 1, "brp")
    if x2 + 2 < 12:
        M.px(x0 + 12, y + 2, "brp")


def kore(M, x0):
    """A bronze handmaid in a Minoan tiered skirt, hair in a high knot."""
    parts = [
        ("e", 6, 1, 9, 4, {"top": "bz4"}),                 # the hair knot
        ("e", 5, 4, 10, 10, {"top": "bz4"}),               # head
        ("r", 7, 11, 2, 1),                                # neck
        ("t", 12, 17, 4, 11, 6, 9),                        # bodice
        ("r", 2, 13, 2, 7),                                # arms
        ("r", 12, 13, 2, 7),
        ("r", 6, 18, 4, 1, {"color": "bz4"}),              # girdle
        ("t", 19, 20, 5, 10, 4, 11, {"top": "bz4"}),       # three flounces
        ("t", 22, 23, 4, 11, 3, 12, {"top": "bz4"}),
        ("t", 25, 26, 3, 12, 2, 13, {"top": "bz4"}),
    ]
    figure(M, parts, x0, 0)
    M.px(x0 + 6, 7, "bz0")
    M.px(x0 + 9, 7, "bz0")
    M.px(x0 + 6, 5, "bw")


def kouros(M, x0, lamp=None):
    """A bronze youth, arms at his sides, in a belted kilt. lamp: None, 'lit' or
    'cold' makes him a lamp-bearer, his left arm raised with a clay lamp."""
    head_ramp = ("bz3", "bz3", "bz2", "bz1", "bz0") if lamp else None
    parts = [
        ("e", 5, 3, 10, 10, {"top": "bz2", "ramp": head_ramp} if lamp else {"top": "bz2"}),
        ("r", 7, 11, 2, 1),
        ("t", 12, 18, 4, 11, 5, 10),                       # chest
        ("r", 12, 13, 2, 7),                               # right arm (ours)
        ("t", 19, 21, 5, 10, 4, 11, {"top": "bz4"}),       # kilt
        ("r", 5, 22, 2, 4),                                # legs
        ("r", 9, 22, 2, 4),
    ]
    if lamp:
        parts.append(("p", [(3, 11), (3, 10), (2, 9), (2, 8), (3, 12), (4, 12)]))
    else:
        parts.append(("r", 2, 13, 2, 7))
    figure(M, parts, x0, 0)
    # hair: a cap of curls
    for x in range(6, 10):
        M.px(x0 + x, 3, "bz1")
    M.px(x0 + 6, 4, "bz1")
    M.px(x0 + 9, 4, "bz0")
    M.px(x0 + 6, 7, "bz1" if lamp else "bz0")
    M.px(x0 + 9, 7, "bz0")
    M.px(x0 + 6, 5, "bz3" if lamp else "bw")
    ankle_rope(M, x0, 24, 5, 10)
    if lamp:
        # the raised hand and its clay lamp: fire colors only above y 8
        rows = ["..f..",
                ".fcf.",
                ".cyc.",
                "fcwcf"] if lamp == "lit" else ["....."] * 4
        blit(M, rows, FI, x0 + 1, 0)
        blit(M, ["k33k2k", ".k221k", "..k1k."], FI, x0 + 0, 4)
        M.px(x0 + 2, 7, "fz1")
        M.px(x0 + 3, 7, "fz0")
        M.px(x0 + 1, 7, "ink")
        M.px(x0 + 4, 7, "ink")


def hound(M, x0):
    """Number Four: a bronze hound sitting on her plinth, ears up, jaws a little
    open. 'Don't touch Number Four. She bites.'"""
    parts = [
        ("p", [(6, 3), (6, 4), (7, 4), (6, 5), (7, 5), (8, 5)], {"top": "bz4"}),   # ear
        ("p", [(9, 4), (9, 5), (10, 5), (9, 6), (10, 6)]),                        # far ear
        ("e", 4, 5, 10, 11, {"top": "bz4"}),                                     # head
        ("r", 0, 8, 5, 3, {"top": "bz4"}),                                       # muzzle
        ("t", 11, 17, 5, 9, 4, 10),                                              # neck, chest
        ("e", 7, 14, 14, 24, {"top": "bz3"}),                                    # haunch
        ("r", 4, 17, 2, 8),                                                      # forelegs
        ("r", 7, 18, 2, 7),
        ("r", 3, 24, 3, 1),                                                      # paws
        ("r", 7, 24, 3, 1),
        ("p", [(14, 19), (15, 18), (15, 17), (14, 16)]),                         # tail
    ]
    figure(M, parts, x0, 0)
    # the open jaw, a tooth, the amber eye, a collar with her tag
    M.px(x0 + 1, 10, "ink")
    M.px(x0 + 2, 10, "ink")
    M.px(x0 + 3, 10, "ink")
    M.px(x0 + 1, 11, "bw")
    M.px(x0 + 3, 11, "bw")
    M.px(x0 + 6, 8, "be")
    M.px(x0 + 0, 8, "ink")
    for (x, y) in ((5, 12), (6, 12), (7, 12), (8, 12), (9, 12)):
        M.px(x0 + x, y, "bz4" if x < 8 else "bz3")
    M.px(x0 + 6, 13, "bz4")
    ankle_rope(M, x0, 23, 4, 9)


def unfinished(M, x0):
    """An automaton on its stand, unfinished: no head yet, the chest open on its
    gears, one arm hung on a peg."""
    # the stand: an iron post on a cross foot
    for y in range(13, 26):
        M.px(x0 + 7, y, "bi1")
        M.px(x0 + 8, y, "bi0")
    blit(M, ["kkkkkkkk", "kIIIIIik"], BZ, x0 + 4, 24)
    # the hollow torso: a bronze shell round a dark chest
    shell = [("t", 4, 13, 3, 12, 4, 11, {"top": "bz4"})]
    figure(M, shell, x0, 0)
    for y in range(6, 12):
        for x in range(5, 11):
            if 5 < x < 10 or y < 11:
                M.px(x0 + x, y, "ts0")
    # gears in the chest
    blit(M, ["..3.3..", ".33433.", "34.k.43", ".3k.k3.", "34.k.43", ".33433.", "..3.3.."],
         {"3": "bz3", "4": "bz4", "k": "bz1", ".": None}, x0 + 4, 5)
    M.px(x0 + 7, 8, "bz0")
    # the neck socket
    blit(M, ["kSSk", "kssk"], BZ, x0 + 6, 2)
    # an arm hung on the stand
    figure(M, [("r", 12, 14, 2, 7)], x0, 0)
    M.px(x0 + 11, 14, "bi1")


def automaton(key, title, draw, plaque=None, rope=True, notes=""):
    s = Struct(key, title, 1, 2, walk=["X", "X"], notes=notes)
    on_floor(s)
    draw(s.M, 0)
    plinth(s.M, 0, plaque=plaque, rope=rope)
    s.names = {"top": (0, 0), "base": (0, 1)}
    return twins(s)


def empty_plinth(key, title, plaque, cut=False, notes=""):
    s = Struct(key, title, 1, 2, walk=[".", "X"], notes=notes)
    on_floor(s)
    plinth(s.M, 0, plaque=plaque, rope=False)
    # the rope left on the plinth: coiled, or cut and trailing
    if cut:
        blit(s.M, ["..rrr.....", ".r...rr...", "..rr...r.r", ".....rr..r"], BZ, 3, 21)
        s.M.px(12, 25, "brp")
    else:
        blit(s.M, [".rrrr.", "r.rr.r", ".rrrr."], BZ, 5, 22)
    s.names = {"top": (0, 0), "base": (0, 1)}
    return twins(s)


def automata():
    out = []
    out += automaton("auto_kore", "Automaton: a bronze handmaid", kore,
                     notes="A bronze handmaid in a Minoan tiered skirt on her slate plinth, tied "
                           "at the ankles to a ring in it: Daedalus's statues had to be tied down "
                           "or they'd walk off. Put the object text on the base.")
    out += automaton("auto_kouros", "Automaton: a bronze youth", kouros,
                     notes="A bronze youth in a belted kilt, tied to his plinth.")
    out += automaton("auto_hound", "Automaton: Number Four, the bronze hound", hound,
                     plaque="||||",
                     notes="Number Four (IIII on her plinth, Attic numerals): a bronze hound "
                           "sitting, jaws a little open, one amber eye. \"Don't touch Number "
                           "Four. She bites.\"")
    out += automaton("auto_lamp", "Automaton: a lamp-bearer, lit",
                     lambda M, x: kouros(M, x, lamp="lit"),
                     notes="A bronze youth holding up a lit clay lamp: the workshop's lights, "
                           "as Homer's golden youths lit Alkinoos's hall. The flame is in the "
                           "fire palette (it stays lit in the glow set).")
    out += automaton("auto_lamp_cold", "Automaton: a lamp-bearer, burned out",
                     lambda M, x: kouros(M, x, lamp="cold"),
                     notes="The lamp-bearer at dawn (scene L): the lamp burned out.")
    out += automaton("auto_open", "Automaton: unfinished, on its stand", unfinished, rope=False,
                     notes="A headless automaton on an iron stand, its chest open on its gears, "
                           "one arm hung on a peg.")
    out += empty_plinth("plinth_three", "Automaton plinth: Number Three's, empty", "|||",
                        notes="III: Number Three's plinth, its rope untied. He is out in the "
                              "web maze, a trainer (LABYRINTH.md §6, Ring III).")
    out += empty_plinth("plinth_seven", "Automaton plinth: Number Seven's, empty", "P||",
                        notes="Attic seven: Number Seven, the other trainer in the maze.")
    out += empty_plinth("plinth_nine", "Automaton plinth: Number Nine's, empty", "P||||",
                        cut=True,
                        notes="Number Nine's plinth, its rope cut: he walked off to Emporion a "
                              "year ago (seed 4). The top cell is walkable floor.")
    return out


# --------------------------------------------------------------------------
# Benches, tables and the music box
# --------------------------------------------------------------------------

def bench_top(L, x0, end=None):
    """A bench's top seen from above, filling the cell: planks running across, a
    lit front edge. end: 'l' or 'r' closes that end. Repeats every 8 px."""
    for y in range(16):
        for x in range(16):
            if y == 0:
                c = "tw0"
            elif y in (5, 10):
                c = "tw1"
            elif y == 13:
                c = "tw3"
            elif y >= 14:
                c = "tw1"
            else:
                c = "tw2"
                if ((x % 8) * 5 + y * 3) % 17 == 0:
                    c = "tw3"
            L.px(x0 + x, y, c)
    if end == "l":
        for y in range(16):
            L.px(x0, y, "ink")
            if 0 < y < 14:
                L.px(x0 + 1, y, "tw3")
    if end == "r":
        for y in range(16):
            L.px(x0 + 15, y, "ink")
            if 0 < y < 14:
                L.px(x0 + 14, y, "tw1")


def bench_front(M, x0, end=None):
    """A bench's front, over the floor: the apron, legs at the ends, a stretcher."""
    for x in range(16):
        M.px(x0 + x, 0, "tw1")
        M.px(x0 + x, 1, "tw1")
        M.px(x0 + x, 2, "tw0")
        M.px(x0 + x, 3, "ink")
        M.px(x0 + x, 10, "tw1")
        M.px(x0 + x, 11, "tw0")
    if end == "l":
        for y in range(0, 16):
            M.px(x0, y, "ink")
            if y < 15:
                M.px(x0 + 1, y, "tw3")
                M.px(x0 + 2, y, "tw2")
                M.px(x0 + 3, y, "ink")
        M.px(x0 + 1, 15, "ink")
        M.px(x0 + 2, 15, "ink")
    if end == "r":
        for y in range(0, 16):
            M.px(x0 + 15, y, "ink")
            if y < 15:
                M.px(x0 + 13, y, "tw2")
                M.px(x0 + 14, y, "tw1")
                M.px(x0 + 12, y, "ink")
        M.px(x0 + 13, 15, "ink")
        M.px(x0 + 14, 15, "ink")


def collar(M, x0, y0):
    """The half-polished bronze collar lying on the bench (32 x 12): a heavy ring
    with three empty sockets for the sickle's three pieces. Its left side is still
    dull and green; its right is polished bright."""
    cx, cy = 15.5, 5.5
    for y in range(12):
        for x in range(32):
            dx, dy = (x - cx) / 13.5, (y - cy) / 5.5
            d = dx * dx + dy * dy
            di = ((x - cx) / 9.5) ** 2 + ((y - cy) / 2.6) ** 2
            if d <= 1.0 and di > 1.0:
                if x < 15:
                    c = "bz1" if y > cy else "bz2"
                    if (x + y * 3) % 7 == 0:
                        c = "bv0"
                    if (x * 3 + y) % 11 == 0:
                        c = "bv1"
                else:
                    c = "bz3" if y > cy + 1 else "bz4"
                    if y <= 2 and 17 < x < 24:
                        c = "bw"
                    if y >= 9:
                        c = "bz2"
                M.px(x0 + x, y0 + y, c)
    A.outline(M, x0 - 1, y0 - 1, 34, 14)
    # three sockets along the top
    for sx in (9, 15, 21):
        M.px(x0 + sx, y0 + 1, "ts0")
        M.px(x0 + sx + 1, y0 + 1, "ts0")
        M.px(x0 + sx, y0 + 2, "ink")
        M.px(x0 + sx + 1, y0 + 2, "ts0")


def bench():
    s = Struct("bench", "Workbench: four cells, the collar on it", 4, 2,
               walk=["XXXX", "XXXX"],
               notes="Daedalus's bench, four cells wide (top row the top, bottom row the "
                     "front). Perdix's saw and a mallet at (0, 0); the collar lies across (1, 0) "
                     "and (2, 0). At dawn (scene L) the collar is gone: put `bench_parts` "
                     "`cloth_l` and `cloth_r` there. Any length: `bench_parts` has a plain top "
                     "and fronts.")
    on_floor(s, [(x, 1) for x in range(4)])
    for i in range(4):
        bench_top(s.B, i * 16, "l" if i == 0 else "r" if i == 3 else None)
        _front(s.M, i * 16, 16, "l" if i == 0 else "r" if i == 3 else None)
    collar(s.M, 16, 2)
    tools_a(s.M, 0, 0)
    s.names = {"tools": (0, 0), "collar_l": (1, 0), "collar_r": (2, 0), "top_r": (3, 0),
               "front_l": (0, 1), "front_m": (1, 1), "front_m2": (2, 1), "front_r": (3, 1)}
    return twins(s)


def _front(M, x0, y0, end):
    sub = A.K.Layer(16, 16)
    bench_front(sub, 0, end)
    M.a[y0:y0 + 16, x0:x0 + 16][sub.a[..., 3] > 0] = sub.a[sub.a[..., 3] > 0]


def tools_a(M, x0, y0):
    """Tools at the bench's left end: Perdix's saw, a mallet, a bow drill."""
    # the saw: an iron blade, its teeth down, a bronze-brown grip
    blit(M, ["kkkkkkkkkk...",
             "kIIIIIIIIk11k",
             "kIIIIIIIk.k1k",
             "kiiiiiik..kk.",
             ".k.k.k.k....."], BZ, x0 + 2, y0 + 2)
    # the mallet
    blit(M, ["kkkk.....", "k32k.....", "k21kkkkk.", "k10k2211k", "kkkkkkkk."], BZ, x0 + 3, y0 + 8)


def bench_parts():
    s = Struct("bench_parts", "Workbench parts: plain, the cloth, the vise", 4, 2,
               walk=["XXXX", "XXXX"],
               notes="For benches of any length, and for scene L. Row 0: a plain top (0), the "
                     "polishing cloth left spread where the collar lay (1, 2: the collar is gone "
                     "at dawn), and a top with a vise holding a bronze hand (3). Row 1: the plain "
                     "front (0) and the left and right ends' fronts (1, 2), and the plain front "
                     "again (3).")
    on_floor(s, [(x, 1) for x in range(4)])
    for i in range(4):
        bench_top(s.B, i * 16)
    # the cloth, spread where the collar lay
    blit(s.M, ["..kkkkkkkkkkkkkk",
               ".krrrrrrrrrrrrrr",
               "krrrrrrrrrrrrrrr",
               "krrrrrrrrrrrrrrr",
               ".krrrrrrrrrrrrrr",
               "..kkkkkkkkkkkkkk"], BZ, 16, 4)
    blit(s.M, ["kkkkkkkkkk....",
               "rrrrrrrrrrk...",
               "rrrrrrrrrrrk..",
               "rrrrrrrrrrrrk.",
               "rrrrrrrrrrrk..",
               "kkkkkkkkkkk..."], BZ, 32, 4)
    # the vise and a bronze hand in it
    blit(s.M, ["..kkkk..",
               ".kIIIIk.",
               "kiIkkIik",
               "kik..kik",
               "kikkkkik",
               "kiiiiiik",
               ".kkkkkk."], BZ, 48 + 1, 3)
    blit(s.M, ["k.k.k.",
               "3k3k3k",
               "333332",
               "k3322k",
               ".k21k."], BZ, 48 + 9, 2)
    _front(s.M, 0, 16, None)
    _front(s.M, 16, 16, "l")
    _front(s.M, 32, 16, "r")
    _front(s.M, 48, 16, None)
    s.names = {"top": (0, 0), "cloth_l": (1, 0), "cloth_r": (2, 0), "vise": (3, 0),
               "front": (0, 1), "front_l": (1, 1), "front_r": (2, 1)}
    return twins(s)


def drafting():
    """Drafting tables: a tilted board with a sheet pinned to it, on splayed legs.
    The left board shows the collar's design; the right one a fresh sheet."""
    s = Struct("drafting", "Drafting tables: the collar's design, a fresh sheet", 4, 2,
               walk=["XXXX", "XXXX"],
               notes="Two drafting tables, two cells each. The left board shows the collar's "
                     "design: a ring with its three sockets, measured (\"That collar binds the "
                     "sickle's pieces. I made it.\"). The right board has a fresh sheet pinned "
                     "to it. The top row is the board, the bottom "
                     "row its legs.")
    on_floor(s, [(x, 1) for x in range(4)])
    for i in range(2):
        x0 = i * 32
        for y in range(16):
            for x in range(32):
                if x in (0, 31) or y == 0:
                    c = "ink"
                elif x in (1, 30) or y in (1, 15):
                    c = "tw1"
                elif y == 14:
                    c = "tw2"
                else:
                    c = "tp1"
                    if x in (2, 29) or y == 2:
                        c = "tp0"
                s.B.px(x0 + x, y, c)
        for (px, py) in ((3, 3), (28, 3), (3, 12), (28, 12)):
            s.B.px(x0 + px, py, "tx")
        sub = A.K.Layer(32, 16)
        for x in range(32):
            sub.px(x, 0, "tw2")
            sub.px(x, 1, "tw0")
            sub.px(x, 2, "ink")
        for (lx, d) in ((4, -1), (26, 1)):
            for y in range(3, 16):
                xx = lx + (d if y > 9 else 0)
                sub.px(xx - 1, y, "ink")
                sub.px(xx, y, "tw2")
                sub.px(xx + 1, y, "tw1")
                sub.px(xx + 2, y, "ink")
        for x in range(7, 25):
            sub.px(x, 8, "tw1")
            sub.px(x, 9, "ink")
        A.E.mirror_half(sub, 0, 32, 0, 16)
        s.M.a[16:32, x0:x0 + 32][sub.a[..., 3] > 0] = sub.a[sub.a[..., 3] > 0]
    # the collar's design: a ring, three sockets, a measure under it
    for t in range(0, 360, 5):
        x = 15.5 + 7 * math.cos(math.radians(t))
        y = 7.5 + 3.6 * math.sin(math.radians(t))
        s.B.px(round(x), round(y), "tr")
    for sx in (11, 15, 19):
        s.B.px(sx, 4, "tg")
        s.B.px(sx + 1, 4, "tg")
    for x in range(8, 24, 2):
        s.B.px(x, 12, "tg")
    s.names = {"design_l": (0, 0), "design_r": (1, 0), "fresh_l": (2, 0), "fresh_r": (3, 0),
               "legs_l": (0, 1), "legs_r": (1, 1)}
    return twins(s)


def music_box():
    s = Struct("music_box", "The bronze music box on its tripod", 1, 2, walk=["X", "X"],
               notes="Daedalus's first music box, the prototype of Elpis's (seed 17), on a "
                     "bronze tripod with lion's feet: its lid open on the steel comb and the "
                     "pinned drum, its winding key on the right. Object text on either cell: "
                     "\"A little bronze music box. Its tune never quite reaches the end.\"")
    on_floor(s)
    M = s.M
    rows = ["................",
            "..kkkkkkkkkkk...",
            "..k44444444443k.",
            "..k43333333332k.",
            "..kkkkkkkkkkkkk.",
            ".k3wIwIwIwIwI1k.",
            ".k3kkkkkkkkkk1k.",
            ".k34k4k4k4k431kk",
            ".k344444444431k3",
            ".k322222222221kk",
            ".k211111111110k.",
            ".k21kk3333kk10k.",
            ".k211111111110k.",
            "kkkkkkkkkkkkkkkk",
            "k44333333333221k",
            ".kk0011111100kk.",
            "..k1k..k1k..k1k.",
            "..k1k..k1k..k1k.",
            ".k21k..k1k..k1k.",
            ".k1k...k1k...k1k",
            ".k1k...k1k...k1k",
            "k21k...k1k...k1k",
            "k1k....k1k....k1",
            "k1k....k1k....k1",
            "k1k...k21k....k1",
            "k32k..k32k...k32",
            "kkkk..kkkk...kkk",
            "................",
            "................",
            "................",
            "................",
            "................"]
    rows = [r.ljust(16, ".")[:16] for r in rows]
    blit(M, rows, BZ, 0, 0)
    s.names = {"top": (0, 0), "legs": (0, 1)}
    return twins(s)


# --------------------------------------------------------------------------
# The heal bed and the Pithos
# --------------------------------------------------------------------------

def kline():
    s = Struct("kline", "The heal bed: Daedalus's kline", 2, 2, walk=["XX", "XX"],
               notes="Daedalus's own bed, where the player's Pokémon rest (the heal). A timber "
                     "kline with a turned headboard, linen, a blue wool blanket and a fleece at "
                     "its foot.")
    on_floor(s)
    rows = ["................................",
            "................................",
            "..kkkk..........................",
            ".k3322k.........................",
            ".k3k21k.........................",
            ".k3221kkkkkkkkkkkkkkkkkkkkkkkkk.",
            ".k3221kcccbkLLLLLLLLLLLLLLLLLq k",
            ".k3221kccbbkLLLLLLLLLLLLLLLLLqqk",
            ".k3221kcbbbkLBLLLLLLBLLLLLLLLqqk",
            ".k3221kbbbbkLLLLLLLLLLLLLLLLqqqk",
            ".k3221kkkkkkBLLLLLBLLLLLLLLBqqqk",
            ".k3221ccccccLLLLLLLLLLLLLLLLqqbk",
            ".k3221bbbbbbBBBBBBBBBBBBBBBBqbbk",
            ".k3221bbbbbbBBBBBBBBBBBBBBBBbbbk",
            ".k2211aaaaaaaaaaaaaaaaaaaaaaaaak",
            ".k2211kkkkkkkkkkkkkkkkkkkkkkkkkk",
            ".k3322222222222222222222222222k.",
            ".k2111111111111111111111111111k.",
            ".kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.",
            "..k32k....................k21k..",
            "..k21k....................k10k..",
            "..k21k....................k10k..",
            "..kkkk....................kkkk..",
            "................................",
            "................................",
            "................................",
            "................................",
            "................................",
            "................................",
            "................................",
            "................................",
            "................................"]
    rows = [r.ljust(32, ".")[:32] for r in rows]
    blit(s.M, rows, TM, 0, 4)
    s.names = {"head_t": (0, 0), "foot_t": (1, 0), "head_b": (0, 1), "foot_b": (1, 1)}
    return twins(s)


def pithos():
    """The Pithos (TERMS.md: the storage jar that replaces the PC), as a Minoan
    pithos from the West Magazines: broad in the shoulder, narrow in the foot,
    raised rope bands, a rolled rim and a clay lid sealed with wax. Lit from the
    front and symmetric, so its right half is its left half flipped."""
    s = Struct("pithos", "The Pithos: a Minoan storage jar", 2, 3, walk=["XX", "XX", "XX"],
               notes="The Pithos, Pokémon storage (MB_PC on the bottom row). A tall Minoan "
                     "pithos like the West Magazines', broad-shouldered, with raised rope bands, "
                     "a rolled rim and a wax-sealed clay lid, a double axe painted on its "
                     "shoulder.")
    on_floor(s)
    M = s.M
    cx = 15.5

    def hw(y):
        if y < 8:
            return 7.5                       # the rolled rim
        if y < 10:
            return 6.5                       # the neck
        if y < 17:
            return 6.5 + (y - 9) * 1.2       # the shoulder flaring
        if y < 23:
            return 15.0
        if y < 44:
            return 15.0 - (y - 22) * 0.36    # the long taper to the foot
        return 7.0

    for y in range(4, 47):
        h = hw(y)
        for x in range(32):
            d = abs(x - cx)
            if d > h:
                continue
            c = "mt1"
            if d > h - 1.6:
                c = "mt0"
            elif d < 4 and 12 <= y < 30:
                c = "mt2"
            if y == 4:
                c = "mt2"
            elif y == 7:
                c = "mt0"
            if y >= 16 and y % 8 in (0, 1) and y < 44 and d <= h - 1.6:
                c = ("mt2" if (x % 4) < 2 else "mt1") if y % 8 == 0 else \
                    ("mt0" if (x % 4) < 2 else "mt1")
            M.px(x, y, c)
    # the lid in the rim, a knob, a seal of wax on it
    blit(M, ["......kkkk......",
             ".....k2112k.....",
             "...kk211110kk...",
             "..k2111111110k..",
             "..kkkkkkkkkkkk.."], MN, 8, 0)
    blit(M, ["Rr", "rR"], MN, 15, 1)
    # handles on the shoulder: rolled clay loops
    blit(M, ["k0k", "k1k", "k0k"], MN, 1, 18)
    # the painted double axe on the shoulder
    blit(M, ["R..R..R", "RRRRRRR", "R..R..R", "...R...", "...R..."], MN, 12, 18)
    A.outline(M, 0, 0, 32, 48)
    for x in range(10, 22):
        M.px(x, 47, "ink")
    A.E.mirror_half(M, 0, 32, 0, 48)
    s.behaviors[(0, 2)] = "MB_PC"
    s.behaviors[(1, 2)] = "MB_PC"
    s.names = {"tl": (0, 0), "tr": (1, 0), "ml": (0, 1), "mr": (1, 1), "bl": (0, 2), "br": (1, 2)}
    return twins(s)


# --------------------------------------------------------------------------
# The bays of the arcade: the Icarus Shaft, the lift, shelves, plans
# --------------------------------------------------------------------------

def shaft():
    """The Icarus Shaft: a four-cell bay whose recess is the foot of the shaft
    Icarus flew from. Grey light falls down it. Closed, a bronze grate seals it;
    open (scene L), the grate is drawn up into the vault and the light spills
    out over the sill."""
    s = Struct("shaft", "The Icarus Shaft: grated, and open at dawn", 8, 4,
               walk=["XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "........"],
               notes="Two states of the same four-cell bay, for an `arch4`-sized gap in the "
                     "arcade. Columns 0-3: the grate shut on the shaft's grey light (scene D). "
                     "Columns 4-7: the grate drawn up and the dawn light falling (scene L). Row "
                     "3 is the sill in front of the bay, the row a north wall's shadow would be "
                     "on: grey light leaks through the bars onto it when shut, and floods it "
                     "when open. Swap the whole 4 x 4 block with `setmetatile` to open it.")
    for i, opened in enumerate((False, True)):
        x0 = i * 64
        ins = A.arch(s.B, x0, 64, rise=17)
        _shaft_inside(s.B, x0, ins)
        if opened:
            _grate_raised(s.M, x0, ins)
        else:
            _grate(s.M, x0, ins)
        _sill(s.B, x0, 48, opened)
    s.names = {}
    for i, st in enumerate(("shut", "open")):
        for cy in range(4):
            for cx in range(4):
                s.names[f"{st}_{cy}{cx}"] = (i * 4 + cx, cy)
    return s


def _shaft_inside(L, x0, inside):
    """The foot of the shaft behind the arch: grey sky far above, the light
    falling in soft streaks and dimming as it falls, the shaft's sides in shadow,
    the pale floor it lands on. Laid out on the 8 px grid and symmetric about the
    bay's middle, so it costs few tiles."""
    for y in range(4, 48):
        for x in range(x0, x0 + 64):
            if not inside(x, y):
                continue
            X = x - x0
            col = min(X, 63 - X) // 8          # 0 outermost .. 3 middle
            xx, yy = X % 8, y % 8
            band = y // 8                      # 0-1 sky, 2-3 bright fall, 4 dim, 5 floor
            if band <= 1:
                c = ("ls3", "ld0", "ld1", "ld1")[col]
                if col == 1 and (xx + yy) % 2:
                    c = "ld1"
                if y < 7 and col >= 2:
                    c = "lw1"            # first light, the sky warming far above
                elif y == 7 and col >= 2 and xx % 2:
                    c = "lw1"
            elif band <= 4:
                if col == 0:
                    c = "ls3" if yy == 0 else "ls2"
                elif col == 1:
                    c = "ld0" if xx in (3, 4) or (xx + yy) % 3 == 0 else "ls4"
                else:
                    c = "ld0" if xx in (3, 4) else "ld1"
            else:
                c = ("ls4", "ld0", "ld1", "ld1")[col]
                if col == 1 and yy > 3 and (xx + yy) % 2:
                    c = "ls4"
            L.px(x, y, c)


def _grate(M, x0, inside):
    """The grate: a bronze portcullis under the arch's lunette, a top rail, bars
    every 8 px, two crossbars, a lock plate with a labrys."""
    for y in range(14, 48):
        for x in range(x0 + 8, x0 + 56):
            X = x - x0
            xx = X % 8
            c = None
            if y in (14, 15):
                c = "bz4" if y == 14 else "bz1"
            elif y == 16:
                c = "ink"
            elif xx == 3:
                c = "bz3"
            elif xx == 4:
                c = "bz1"
            elif xx in (2, 5):
                c = "ink"
            if y in (28, 29, 44, 45):
                c = "bz4" if y in (28, 44) else "bz1"
            if y in (30, 46) and c is None:
                c = "ink"
            if c:
                M.px(x, y, c)
    for y in (13, 14, 15, 16):
        M.px(x0 + 7, y, "ink")
        M.px(x0 + 56, y, "ink")
    # the lock plate: a double axe in relief
    blit(M, ["kkkkkkkkkkkkkkkk",
             "k33333333333333k",
             "k3kk33k22k33kk3k",
             "k3kkkkkkkkkkkk3k",
             "k3kk33k22k33kk3k",
             "k22222k22k22222k",
             "k11111111111111k",
             "kkkkkkkkkkkkkkkk"], BZ, x0 + 24, 32)


def _grate_raised(M, x0, inside):
    """The grate drawn up into the vault: its rail and spiked feet hang just under
    the crown of the arch."""
    for y in range(8, 16):
        for x in range(x0 + 8, x0 + 56):
            X = x - x0
            xx = X % 8
            if y in (8, 9):
                M.px(x, y, "bz4" if y == 8 else "bz1")
            elif y == 10:
                M.px(x, y, "ink")
            elif xx == 3:
                M.px(x, y, "bz3" if y < 14 else "bz4")
            elif xx == 4:
                M.px(x, y, "bz1" if y < 14 else "bz2")
            elif xx in (2, 5) and y < 14:
                M.px(x, y, "ink")
    for y in (7, 8, 9, 10):
        M.px(x0 + 7, y, "ink")
        M.px(x0 + 56, y, "ink")


def _sill(L, x0, y0, opened):
    """The sill across the shaft's mouth: the grate's groove, a lit edge, and the
    grey light on it, barred by the grate's shadow while it is shut."""
    for y in range(16):
        for x in range(64):
            col = min(x, 63 - x) // 8
            xx = x % 8
            if y == 0:
                c = "ls2"
            elif y == 1:
                c = "ls1"
            elif y == 15:
                c = "lj"
            elif opened:
                c = ("ls6", "ld0", "ld1", "ld1")[col]
                if col == 0 and y > 9:
                    c = "ls5"
                if col == 1 and y > 12 and xx % 2:
                    c = "ld1"
            else:
                c = "ls6" if y == 2 else "ls5"
                if col >= 1 and 3 <= y <= 9:
                    c = "ls4" if xx in (2, 3, 4, 5) else ("ld0" if y < 7 else "ls6")
            L.px(x0 + x, y0 + y, c)


def light_spill():
    """The dawn light past the sill (scene L): the slab floor washed grey, fading."""
    s = Struct("light_spill", "Dawn light on the floor below the open shaft", 4, 1,
               walk=["...."],
               notes="The row in front of the open shaft's sill (scene L): the slab floor with "
                     "the grey dawn light fading out across it. The Icarus Shaft is unique, so "
                     "it comes in one parity: lay it with its first cell where x + y is even "
                     "(the shaft's own columns, as the mock does).")
    s.floor_cells = []
    for cx in range(4):
        h = "l" if cx % 2 == 0 else "r"

        def tone(x, y, cx=cx):
            X = cx * 16 + x
            col = min(X, 63 - X) // 8
            if y >= 8 or col == 0:
                return None
            if col >= 2:
                return "d2" if y < 3 else "d1" if y < 5 or (x + y) % 2 else None
            return "d1" if y < 3 or (y < 6 and (x + y) % 2) else None
        A.slab(s.B, cx * 16, 0, h, tone=tone)
    s.names = {f"c{i}": (i, 0) for i in range(4)}
    return [s]


def bay(key, title, notes, contents, walk=None, deep=False):
    s = Struct(key, title, 3, 3, walk=walk or ["XXX", "XXX", "XXX"], notes=notes)
    ins = A.arch(s.B, 0, 48)
    A.recess(s.B, 0, 48, ins)
    contents(s, ins)
    s.names = {f"{n}{cy}": (cx, cy) for cy in range(3) for cx, n in enumerate("lmr")}
    return s


def _wings_plan(s, ins):
    """The Wings: a sheet pinned up, a wing drawn feather by feather; below it a
    basket of feathers and a pot of wax, gone cold."""
    M = s.M
    _sheet(M)
    blit(M, ["rrrrrrrrrrrrrrrr",
             ".rgrgrgrgrgrgrrr",
             ".ggggggggggggggr",
             ".g.g.g.g.g.g.gg.",
             ".g.g.g.g.g.ggg..",
             "..g.g.g.g.gg....",
             "..g.g.g.gg......",
             "...g.g.g........",
             "...g.gg.........",
             "....g..........."], TM, 16, 22)
    for x in range(16, 32, 3):
        M.px(x, 34, "tg")
    blit(M, ["..c.c.c.", ".cbcbcbc", "k1k1k1k1", "k0101010", ".kkkkkkk"], TM, 8, 42)
    blit(M, ["........", ".kkkkk..", "kxxxxxk.", "k0xxx0k.", ".k000k.."], TM, 32, 41)


def _labyrinth_plan(s, ins):
    """The Labyrinth's plan, pinned up: seven rings round a star, the way through
    them."""
    M = s.M
    _sheet(M)
    cx, cy = 23.5, 27.5
    for ring in range(7):
        r = 1.5 + ring * 1.45
        gap_top = ring % 2 == 0
        for t in range(0, 360, 2):
            if gap_top and 75 < t % 360 < 105:
                continue
            if not gap_top and 255 < t % 360 < 285:
                continue
            x = cx + r * math.cos(math.radians(t))
            y = cy - r * 0.9 * math.sin(math.radians(t))
            M.px(round(x - 0.01 if x < cx else x + 0.01), round(y), "tr" if ring % 2 else "tg")
    M.px(23, 27, "tx")
    M.px(24, 27, "tx")
    A.E.mirror_half(M, 8, 32, 16, 40)


def _shelves(s, ins):
    """Shelves of parts: a timber rack filling the recess, four shelves, and on
    them heads, gears, hands, springs, oil flasks, scrolls and a little bronze
    partridge. Every shelf is one tile row and every part one tile."""
    B, M = s.B, s.M
    for y in range(16, 48):
        for x in range(8, 40):
            yy = y % 8
            c = "tw0" if yy < 6 else "tw2" if yy == 6 else "tw1"
            if x in (8, 39):
                c = "tw1" if yy < 6 else "tw0"
            B.px(x, y, c)
    parts = {
        "gear": ["..3.3...", ".34443..", "34k.k43.", ".4.k.4..", "34k.k43.", ".34443.."],
        "head": ["..kkkk..", ".k4432k.", ".k3k1k..", ".k3321k.", "..k21k..", "...kk..."],
        "bird": ["...kk...", "..k43k..", ".k443kkk", "k43222kk", ".k3221k.", "..k11k.."],
        "hand": ["k.k.k...", "3k3k3k..", "33333k..", "k33321k.", ".k321k..", "..kkk..."],
        "spring": [".kIkIk..", ".I.I.I..", ".kIkIk..", ".I.I.I..", ".kIkIk..", "........"],
        "ingot": ["........", "........", ".kkkkkk.", "k443332k", "k322221k", ".kkkkkk."],
    }
    clay = {"flask": ["...k....", "..k1k...", "..k21k..", ".k2110k.", ".k2110k.", "..kkkk.."]}
    rolls = ["........", "........", "kccbkcbk", "kcbbkbbk", "kkkkkkkk", "........"]
    layout = [("head", "gear", "bird", "gear"),
              ("hand", "spring", None, "hand"),
              ("flask", "ingot", "flask", "spring"),
              ("rolls", None, "ingot", "rolls")]
    for r, row in enumerate(layout):
        for c, item in enumerate(row):
            x, y = 8 + c * 8, 16 + r * 8
            if item in parts:
                blit(M, parts[item], BZ, x, y)
            elif item in clay:
                blit(M, clay[item], MN, x, y)
            elif item == "rolls":
                blit(B, rolls, TM, x, y)
    M.px(8 + 2 * 8 + 3, 18, "ink")    # the partridge's eye


def _lift(s, ins):
    """Daedalus's lift: a counterweighted platform rising up a shaft to the Grand
    Staircase landing. The platform, its bronze frame and its deck, are all in the
    bay's floor cell, so swapping that one cell sends it away."""
    B, M = s.B, s.M
    _lift_platform(B, M, 16, 32)
    # the pulley wheel at the crown
    blit(M, ["..kkkk..",
             ".k3443k.",
             "k32kk23k",
             "k4k22k4k",
             "k3k22k3k",
             "k23kk32k",
             ".k2222k.",
             "..kkkk.."], BZ, 20, 6)
    # the rope from the wheel down to the platform's crossbar
    for y in range(14, 32):
        M.px(23, y, "brp")
        M.px(24, y, "brp")
    for y in range(14, 32, 3):
        M.px(24, y, "bz2")
    # the counterweight in the right of the recess, on its rope over the wheel
    for x in range(28, 37):
        M.px(x, 8, "brp")
    for y in range(9, 14):
        M.px(36, y, "brp")
    blit(M, ["kkkkkkk",
             "k44443k",
             "k4k3k1k",
             "k43331k",
             "k3k2k1k",
             "k32221k",
             "kkkkkkk"], BZ, 33, 14)


def pier_cold():
    s = Struct("pier_cold", "Walls: a pier, its sconce burned out", 1, 3, walk=["X", "X", "X"],
               notes="`arcade`'s `pier_sconce` with its lamp gone cold, for scene L.")
    A.pier(s.B, 0)
    A.sconce(s.M, 0, 26, lit=False)
    s.names = {"top": (0, 0), "mid": (0, 1), "low": (0, 2)}
    return s


def bays():
    out = [pier_cold()]
    out.append(bay("bay_wings", "Bay: the Wings plan pinned up",
                   "A three-cell bay holding the plan of the Wings, pinned up, with a basket "
                   "of feathers and a pot of wax below it.", _wings_plan))
    out.append(bay("bay_plan", "Bay: the Labyrinth's plan pinned up",
                   "The Labyrinth's plan: seven rings round a star (the Starry Chamber), "
                   "drawn in sinopia and charcoal (LABYRINTH.md §4).", _labyrinth_plan))
    out.append(bay("bay_shelves", "Bay: shelves of parts",
                   "Shelves in the recess: automaton heads, gears, a little bronze partridge "
                   "(Perdix), hands, springs, oil flasks, ingots and scrolls.", _shelves))
    out.append(bay("lift", "Daedalus's lift",
                   "The counterweighted lift (LABYRINTH.md §4): the platform is the bay's "
                   "floor, cell (1, 2), walkable; put the lift's script there. The pulley at "
                   "the crown, the counterweight hanging on the right. (1, 3) of `lift_deck` "
                   "is the empty shaft, for while the platform is up at the Grand Staircase.",
                   _lift, walk=["XXX", "XXX", "X.X"]))
    out.append(lift_deck())
    return out


def _sheet(M, x0=8, y0=16, w=32, h=24):
    """A sheet of papyrus pinned up in a bay: pale, its edge a shade darker,
    bronze pins at the corners."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            c = "tp1"
            if x in (x0, x0 + w - 1) or y in (y0, y0 + h - 1):
                c = "tp0"
            M.px(x, y, c)
    for (px, py) in ((x0 + 1, y0 + 1), (x0 + w - 2, y0 + 1), (x0 + 1, y0 + h - 2),
                     (x0 + w - 2, y0 + h - 2)):
        M.px(px, py, "tx")


def lift_deck():
    """The lift's platform cell gone: the empty shaft, for while it's up."""
    s = Struct("lift_deck", "Daedalus's lift, the platform away", 1, 1, walk=["X"],
               notes="Swap it over `lift` (1, 2) while the platform is up at the Grand "
                     "Staircase (before scene D, and while the player rides). The ropes and "
                     "the counterweight stay as they are.")
    big = A.K.Layer(48, 48)
    ins = A.arch(big, 0, 48)
    A.recess(big, 0, 48, ins)
    s.B.a[:] = big.a[32:48, 16:32]
    for y in range(16):
        for x in range(16):
            s.B.px(x, y, "lk" if y < 12 else "ls1")
    s.names = {"empty": (0, 0)}
    return s


def _lift_platform(B, M, x0, y0):
    """The lift's platform in one 16 x 16 cell: a plank deck (timber, bottom
    layer) in a bronze frame with a crossbar the rope is tied to (middle)."""
    for y in range(16):
        for x in range(16):
            if y < 8:
                c = "ls1" if y < 7 else "ls2"
            elif y == 8:
                c = "tw3"
            elif y < 14:
                c = "tw2" if (y - 9) % 3 else "tw1"
            elif y == 14:
                c = "tw1"
            else:
                c = "tw0"
            B.px(x0 + x, y0 + y, c)
    blit(M, ["kkkkkkkkkkkkkkkk",
             "k4444444rr44443k",
             "kk3kkkkkkkkkk3kk",
             ".k3k........k2k.",
             ".k3k........k2k.",
             ".k3k........k2k.",
             ".k3k........k1k.",
             ".k4k........k2k.",
             ".k3k........k1k.",
             ".k3k........k1k.",
             ".k3k........k1k.",
             ".k3k........k1k.",
             ".k3k........k1k.",
             ".k3k........k1k.",
             ".k4kkkkkkkkkk2k.",
             ".kkk........kkk."], BZ, x0, y0)


def runner():
    """A long woven runner in Minoan red and ochre, a running-spiral border down
    each side, laid from the threshold to Daedalus's bench."""
    s = Struct("runner", "A woven runner, Minoan red", 2, 3, walk=["..", "..", ".."],
               notes="A runner two cells wide: (row 0) its top end, (row 1) the middle, to "
                     "repeat as long as it needs, (row 2) its bottom end. It covers the floor "
                     "completely, so it needs no twin; lay it anywhere.")
    L = s.B
    for y in range(48):
        for x in range(32):
            d = min(x, 31 - x)                 # symmetric about the middle
            yy = y % 8
            if d == 0:
                c = "mb"
            elif d == 1:
                c = "mo0"
            elif d < 7:
                # the running spiral, every 8 px down
                sp = ["oooooo",
                      "oRRRRo",
                      "oRooRo",
                      "oRoRRo",
                      "oRoooo",
                      "oRRRRR",
                      "oooooR",
                      "RRRRRR"][yy][d - 1]
                c = "mo0" if sp == "o" else "mb"
            elif d == 7:
                c = "mb"
            else:
                c = "mr0"
                # a lozenge on the middle every 16 px
                k = abs(y % 16 - 8) + (15 - d)
                if k <= 4:
                    c = "mr1" if k < 4 else "mo0"
            L.px(x, y, c)
    # the ends: a dark band and an ochre fringe line
    for x in range(32):
        for y in (0, 1, 2):
            L.px(x, y, ("mb", "mo2", "mb")[y])
        for y in (45, 46, 47):
            L.px(x, y, ("mb", "mo2", "mb")[y - 45])
    s.names = {"top_l": (0, 0), "top_r": (1, 0), "mid_l": (0, 1), "mid_r": (1, 1),
               "end_l": (0, 2), "end_r": (1, 2)}
    return [s]


def build():
    out = []
    out += automata()
    out += bench()
    out += bench_parts()
    out += drafting()
    out += music_box()
    out += kline()
    out += pithos()
    out.append(shaft())
    out += light_spill()
    out += bays()
    out += runner()
    for s in out:
        s.section = "workshop"
    return out
