"""Emporion's streets and its two-storey merchant houses (gTileset_Emporion).

Streets: marble paving and its variants, kerbs where paving meets grass, broad
steps, and the marble terrace walls that hold the city's levels (with the
cistern mouth under the Agora steps).

Houses: a kit of parts, not whole houses. Every house is four rows tall: a
terracotta roof (ridge row and eaves row), an upper storey and a ground
storey. The upper and ground storeys are strips of one-cell parts (corner
pilasters, plain wall, windows, a balcony, trade signs, doors, a shopfront)
that combine into any width. Every part comes in ochre stucco with Aegean-blue
paint and, recolored slot for slot, in rose stucco with sea-green paint; the
rose parts are the ochre parts' tiles in another palette, so they cost no
tiles. Doors and windows are mirror-symmetric in their cells, so each costs
half its tiles. TILES_emporion.md lists eight house recipes built from the kit.
"""
from __future__ import annotations

import math

import emporion_lib as E
from emporion_lib import Struct, finish

# ==========================================================================
# Streets
# ==========================================================================


def paving_set():
    s = Struct("paving", "Marble street paving", 7, 1, walk=["......."], ground="none",
               notes="Great square marble flags, one to a cell, softly bevelled. (0) the flag, "
                     "(1) split in two, (2) split in four, (3) a bronze drain grate: lay (0) "
                     "everywhere and scatter the others. (4)-(6) the flag in shadow: (4) along "
                     "its north edge, for the row under a building's front or a wall, (5) along "
                     "its west edge, for the column east of a building's end, (6) both, for the "
                     "corner. All walkable, and all meet each other on every side.")
    for i, v in enumerate((0, 1, 2, 0, 0, 0, 0)):
        E.paving(s.B, i * 16, 0, 16, 16, ox=i * 16, variant=v)
    L = s.B
    L.rect(52, 4, 8, 8, "m4")
    E.outline_rect(L, 51, 3, 10, 10, "m5")
    for x in (53, 55, 56, 58):
        L.vline(x, 5, 10, "ink")
    L.hline(51, 60, 13, "w0")
    E.shade_paving(L, 64, 0, north=True)
    E.shade_paving(L, 80, 0, north=False, west=True)
    E.shade_paving(L, 96, 0, north=True, west=True)
    s.names = {"flag": (0, 0), "flag_2": (1, 0), "flag_4": (2, 0), "drain": (3, 0),
               "shade_n": (4, 0), "shade_w": (5, 0), "shade_nw": (6, 0)}
    return finish(s)


def plaza_inlay():
    """A 2x2 star of colored marble in a square frame, four-fold symmetric (one
    quarter's tiles, flipped)."""
    s = Struct("plaza_rose", "Plaza inlay: an eight-pointed star in colored marble", 2, 2,
               walk=["..", ".."], ground="none",
               notes="For the middle of the Agora or a crossroads: a star of blue and red "
                     "marble with a gold heart, in a ring, in a square frame. Walkable.")
    L = s.B
    cx = cy = 15.5
    for y in range(16):
        for x in range(16):
            dx, dy = x - cx, y - cy
            r = math.hypot(dx, dy)
            a = math.atan2(dy, dx)
            star = 6 + 8 * abs(math.cos(4 * a)) ** 3
            if x == 0 or y == 0:
                c = "w0"
            elif x == 1 or y == 1:
                c = "m3"
            elif 13.2 <= r <= 14.5:
                c = "m4"
            elif 12 < r < 13.2:
                c = "w0"
            elif r <= star and r < 12:
                c = "g1" if r < 3 else ("b1" if math.cos(4 * a) > 0 else "rd")
            elif r < 12:
                c = "m1" if (x + y) % 2 else "w0"
            else:
                c = "m2" if (x + y) % 4 == 0 else "m1"
            L.px(x, y, c)
    E.mirror_half(L, 0, 32, 0, 16)
    L.a[16:32] = L.a[0:16][::-1]
    return finish(s)


def kerbs():
    """Paving meeting grass: a 3x3 border plus inner corners, like akti's plaza."""
    s = Struct("kerb", "Paving's kerbed edge against grass", 5, 3,
               walk=[".....", ".....", "....."], ground="none",
               notes="Columns 0-2 are the paved area's border: NW, N, NE / W, plain, E / "
                     "SW, S, SE. A dark kerbstone runs round the outside; on the south "
                     "edge its face shows, the street a step above the grass. Columns 3-4, "
                     "rows 0-1, are inner corners (grass diagonally beyond): NW, NE / SW, "
                     "SE. (3,2) and (4,2) are plain paving and its worn variant.")
    L = s.B
    E.paving(L, 0, 0, 80, 48)
    E.paving(L, 64, 32, 16, 16, ox=64, variant=2)
    W = 48
    L.hline(0, W - 1, 0, "m5")
    L.hline(0, W - 1, 1, "m3")
    L.hline(0, W - 1, 2, "m2")
    L.vline(0, 0, 47, "m5")
    L.vline(1, 0, 47, "m3")
    L.vline(2, 0, 47, "m2")
    L.vline(W - 1, 0, 47, "m5")
    L.vline(W - 2, 0, 47, "m4")
    L.vline(W - 3, 0, 47, "m2")
    for y, c in ((43, "m2"), (44, "m3"), (45, "m4"), (46, "m4"), (47, "m5")):
        L.hline(0, W - 1, y, c)
    for (cx, cy, sx, sy) in ((3, 0, 0, 0), (4, 0, 1, 0), (3, 1, 0, 1), (4, 1, 1, 1)):
        px = cx * 16 + (13 if sx else 0)
        py = cy * 16 + (13 if sy else 0)
        L.rect(px, py, 3, 3, "m4")
        L.hline(px, px + 2, py + (2 if sy else 0), "m5")
        L.vline(px + (2 if sx else 0), py, py + 2, "m5")
    s.names = {"NW": (0, 0), "N": (1, 0), "NE": (2, 0), "W": (0, 1), "C": (1, 1), "E": (2, 1),
               "SW": (0, 2), "S": (1, 2), "SE": (2, 2), "inNW": (3, 0), "inNE": (4, 0),
               "inSW": (3, 1), "inSE": (4, 1)}
    return finish(s)


def steps():
    s = Struct("steps", "Broad marble steps", 3, 2, walk=["...", "..."], ground="none",
               notes="Four treads climbing north, two per row: west cheek, run (repeat it "
                     "for width), east cheek. Lay them against a terrace wall's gap, a "
                     "podium or a stoa's front (one row of them makes its stylobate).")
    L = s.B
    W = 48
    for k in range(4):
        y = k * 8
        L.rect(0, y, W, 8, "m1")
        L.hline(0, W - 1, y, "w0")
        L.hline(0, W - 1, y + 1, "w0")
        L.hline(0, W - 1, y + 5, "m2")
        L.hline(0, W - 1, y + 6, "m3")
        L.hline(0, W - 1, y + 7, "m4")
    for x0, lit in ((0, True), (W - 5, False)):
        L.rect(x0, 0, 5, 32, "m2" if lit else "m3")
        L.vline(x0, 0, 31, "ink")
        L.vline(x0 + 4, 0, 31, "ink")
        L.vline(x0 + 1, 0, 31, "w0" if lit else "m2")
        L.vline(x0 + 3, 0, 31, "m3" if lit else "m4")
        for y in range(7, 32, 8):
            L.hline(x0 + 1, x0 + 3, y, "m4")
    return finish(s)


def terrace_wall():
    s = Struct("terrace_wall", "Marble terrace wall, its steps and the cistern mouth", 6, 1,
               walk=["XX.XXX"], ground="none",
               notes="A retaining wall one cell tall, the upper level to the north: (0) west "
                     "end, (1) run (repeat it), (2) steps up through the wall (walkable), (3) "
                     "east end, (4) the cistern mouth under the Agora steps, a black arch with "
                     "its grille torn away and two eyes catching the light, (5) its painted "
                     "board, 'No light, no entry'. Put a warp or a bg event on the mouth; it "
                     "opens with Hecate's Torch (SYSTEMS.md §1).")
    L = s.B
    W = 96
    for x in range(W):
        for y in range(16):
            bx = (x + (8 if y >= 8 else 0)) % 16
            c = "m2"
            if y == 0:
                c = "w0"
            elif y == 1:
                c = "m1"
            elif y == 2:
                c = "m4"
            elif y == 15:
                c = "m5"
            elif bx == 0 or y == 9:
                c = "m3"
            elif y in (3, 10):
                c = "m1"
            L.px(x, y, c)
    x0 = 32
    E.paving(L, x0, 0, 16, 16, ox=x0)
    for k in range(2):
        y = 2 + k * 7
        L.rect(x0, y, 16, 7, "m1")
        L.hline(x0, x0 + 15, y, "w0")
        L.hline(x0, x0 + 15, y + 4, "m2")
        L.hline(x0, x0 + 15, y + 5, "m3")
        L.hline(x0, x0 + 15, y + 6, "m4")
    L.vline(x0, 0, 15, "m5")
    L.vline(x0 + 15, 0, 15, "m5")
    L.vline(0, 0, 15, "ink")
    L.vline(1, 1, 14, "w0")
    L.vline(63, 0, 15, "ink")
    L.vline(62, 1, 14, "m4")
    ax = 64
    arch = [
        "    kkkkkk    ",
        "  kk555555kk  ",
        " k5kkkkkkkk5k ",
        " k5kkkkkkkk5k ",
        "k5kkkkkkkkkk5k",
        "k5kkkkkkkkkk5k",
        "k5kkkkkkk1kk5k",
        "k5kkkkkkkkkk5k",
        "k5kk3kkkkkkk5k",
        "k5kkkkkkkkkk5k",
        "k5kkkkkkkkkk5k",
        "k5k1kkkkkkkk5k",
        "kkkkkkkkkkkkkk",
    ]
    L.blit(arch, {"k": "ink", "5": "m4", "1": "b2", "3": "m3"}, ax + 1, 3)
    L.px(ax + 6, 8, "g1")
    L.px(ax + 8, 8, "g1")
    for y in range(6, 15, 2):
        L.px(ax + 12, y, "m3")
    L.vline(ax + 13, 5, 15, "m4")
    bx = 82
    L.rect(bx, 3, 12, 9, "w0")
    E.outline_rect(L, bx - 1, 2, 14, 11, "ink")
    for y in (5, 7, 9):
        for x in range(bx + 1, bx + 11):
            if x % 4 != 3:
                L.px(x, y, "rd")
    L.vline(bx + 2, 13, 15, "m5")
    L.vline(bx + 9, 13, 15, "m5")
    s.names = {"W": (0, 0), "run": (1, 0), "stairs": (2, 0), "E": (3, 0),
               "cistern": (4, 0), "cistern_sign": (5, 0)}
    return finish(s)


# ==========================================================================
# The house kit
# ==========================================================================

def roof_kit():
    s = Struct("roof", "House roof: terracotta, two rows", 5, 2,
               walk=["XXXXX", "XXXXX"], ground="none",
               notes="Row 0 is the ridge, row 1 the eaves with palmette antefixes. Columns: "
                     "west end, run (repeat it), east end, then two ridge-row variants of the "
                     "run: a clay chimney pot and a ridge acroterion (their eaves row is the "
                     "plain run). A terrace of houses shares one long roof line, each house "
                     "closed by its own ends.")
    L = s.B
    E.roof(L, 0, 0, 48, 32)
    E.roof(L, 48, 0, 32, 32, ends=(False, False))
    for y in range(0, 32):
        L.px(1, y, "tc3")
        L.px(2, y, "tc2")
        L.px(46, y, "tc0")
        L.px(45, y, "tc1")
    L.blit([" kkkk ", "kt22tk", "k1221k", "k1110k", "k1110k", "kk00kk", "k0000k", " kkkk "],
           {"k": "ink", "t": "tc3", "2": "tc2", "1": "tc1", "0": "tc0"}, 53, 3)
    L.px(55, 1, "w2")
    L.px(56, 0, "w2")
    L.px(54, 2, "w0")
    L.blit(["  k  ", " k3k ", "k323k", "k232k", " k2k ", " kkk "],
           {"k": "ink", "3": "tc3", "2": "tc2"}, 69, 0)
    s.names = {"W": (0, 0), "run": (1, 0), "E": (2, 0), "chimney": (3, 0), "acroterion": (4, 0),
               "eaves_W": (0, 1), "eaves_run": (1, 1), "eaves_E": (2, 1)}
    return finish(s)


def _upper_wall(L, x0, w, y0=0):
    """An upper-storey strip: the eaves' shadow, a thin painted band of blue
    dashes, plain stucco, and the string course marking the floor."""
    E.stucco(L, x0, y0, w, 16)
    L.hline(x0, x0 + w - 1, y0, "oc0")
    L.hline(x0, x0 + w - 1, y0 + 1, "oc1")
    for x in range(x0, x0 + w):
        L.px(x, y0 + 2, "b1" if x % 4 in (1, 2) else "w0")
    L.hline(x0, x0 + w - 1, y0 + 15, "w2")


def _lower_wall(L, x0, w, y0=0):
    E.stucco(L, x0, y0, w, 16)
    L.hline(x0, x0 + w - 1, y0, "oc1")
    for x in range(x0, x0 + w):
        L.px(x, y0 + 10, "tc2")
        for y in range(y0 + 11, y0 + 14):
            L.px(x, y, "tc1")
        L.px(x, y0 + 14, "w2")
        L.px(x, y0 + 15, "oc0")


def _pilasters(L, w, y0, h):
    """The house's corners: a plain pilaster strip at each end (mirrored, so the
    east one is the west one's tiles flipped)."""
    for y in range(y0, y0 + h):
        L.px(0, y, "ink")
        L.px(1, y, "w0")
        L.px(2, y, "w2")
        L.px(w - 1, y, "ink")
        L.px(w - 2, y, "w0")
        L.px(w - 3, y, "w2")


def _half(L, cx, y0, y1):
    """Mirror the 16 px cell starting at cx (its left half onto its right)."""
    E.mirror_half(L, cx, 16, y0, y1)


def _window(L, cx, y0, kind):
    """A window centered in the cell at cx, upper storey (y0 = the row's top).
    Drawn as a left half and mirrored."""
    if kind == "shutter":
        # louvred blue shutters folded back either side of a deep window
        L.rect(cx + 1, y0 + 4, 3, 10, "b1")
        for yy in range(y0 + 5, y0 + 14, 2):
            L.px(cx + 2, yy, "b0")
        E.outline_rect(L, cx + 1, y0 + 4, 3, 10)
        L.rect(cx + 4, y0 + 4, 4, 10, "w0")
        L.rect(cx + 5, y0 + 5, 3, 8, "ink")
        L.rect(cx + 5, y0 + 5, 3, 2, "wd0")
        L.hline(cx + 3, cx + 7, y0 + 13, "w0")
        L.hline(cx + 3, cx + 7, y0 + 14, "w2")
    elif kind == "grille":
        L.rect(cx + 3, y0 + 4, 5, 10, "w0")
        L.rect(cx + 4, y0 + 5, 4, 8, "ink")
        L.vline(cx + 5, y0 + 5, y0 + 12, "wd1")
        L.hline(cx + 4, cx + 7, y0 + 8, "wd1")
        L.hline(cx + 2, cx + 7, y0 + 13, "w0")
        L.hline(cx + 2, cx + 7, y0 + 14, "w2")
    elif kind == "arched":
        L.blit([" kkk ", "kwwwk", "kdddk", "kdddk", "kdddk", "kdddk", "kdddk", "kkkkk"],
               {"k": "ink", "w": "w0", "d": "wd0"}, cx + 2, y0 + 4)
        L.hline(cx + 1, cx + 7, y0 + 12, "w0")
        L.hline(cx + 1, cx + 7, y0 + 13, "w2")
    _half(L, cx, y0, y0 + 16)


def _balcony(L, x0, y0):
    """A timber balcony across two cells on the upper storey, with a rug hung
    over its rail and a door behind."""
    L.rect(x0 + 12, y0 + 6, 8, 8, "ink")
    L.rect(x0 + 13, y0 + 7, 6, 7, "b0")
    L.vline(x0 + 16, y0 + 7, y0 + 13, "ink")
    L.hline(x0 + 11, x0 + 20, y0 + 5, "w0")
    L.hline(x0 + 1, x0 + 30, y0 + 12, "wd1")
    L.hline(x0 + 1, x0 + 30, y0 + 13, "wd0")
    L.hline(x0, x0 + 31, y0 + 14, "ink")
    for bx in (x0 + 3, x0 + 28):
        L.px(bx, y0 + 15, "wd0")
    L.hline(x0 + 1, x0 + 30, y0 + 7, "wd1")
    L.hline(x0 + 1, x0 + 30, y0 + 6, "ink")
    for x in range(x0 + 2, x0 + 30, 4):
        L.vline(x, y0 + 8, y0 + 11, "wd1")
        L.vline(x + 1, y0 + 8, y0 + 11, "wd0")
    L.vline(x0, y0 + 6, y0 + 14, "ink")
    L.vline(x0 + 31, y0 + 6, y0 + 14, "ink")
    for y in range(y0 + 7, y0 + 14):
        for x in range(x0 + 21, x0 + 29):
            L.px(x, y, "tc2" if (x - x0) % 4 < 2 else "w0")
        L.px(x0 + 21, y, "ink")
        L.px(x0 + 29, y, "ink")
    L.hline(x0 + 21, x0 + 29, y0 + 14, "ink")
    for x in range(x0 + 22, x0 + 29, 2):
        L.px(x, y0 + 15, "tc1")


SIGNS = {
    # trade signs hung from a bracket: drawn 9x8 inside the board
    "tavern": ["         ", "  kkkkk  ", " k1oooo1k", " k1oooo1k", "  koook  ", "   kok   ",
               "  kooook ", "         "],
    "bronze": ["   kkk   ", "  koook  ", " ko1ooak ", " ko1aaak ", " kook ok ", " ko k ok ",
               "  k   k  ", "         "],
    "potter": ["   kkk   ", "   kok   ", "  kkokk  ", " k1oook  ", " k1oook  ", "  k1ok   ",
               "   kk    ", "         "],
    "perfume": ["   kk    ", "   kk    ", "  kaak   ", " k1aaak  ", " k1aaak  ", "  kaak   ",
                "   kk    ", "         "],
    "ships": ["    k    ", "    k1   ", "    k11  ", "    kaaa ", " kooooook", "  kooook ",
              "   aaa   ", "         "],
    "grain": ["   k k   ", "  kakak  ", "  koook  ", " k1ooook ", " k1ooook ", " k1ooook ",
              "  kkkkk  ", "         "],
    "wheel": ["  kkkkk  ", " k1 o 1k ", " k  o  k ", " kooaook ", " k  o  k ", " k1 o 1k ",
              "  kkkkk  ", "         "],
}


def _sign(L, x0, kind, y0=0):
    """A trade sign hung from an iron bracket over the street, on an upper wall."""
    L.hline(x0 + 2, x0 + 13, y0 + 6, "ink")
    L.px(x0 + 2, y0 + 5, "ink")
    L.px(x0 + 2, y0 + 7, "ink")
    L.vline(x0 + 4, y0 + 7, y0 + 8, "ink")
    L.vline(x0 + 12, y0 + 7, y0 + 8, "ink")
    L.rect(x0 + 3, y0 + 8, 11, 7, "w0")
    E.outline_rect(L, x0 + 2, y0 + 8, 13, 8, "ink")
    L.blit(SIGNS[kind], {"k": "ink", "o": "tc1", "1": "tc3", "a": "b1"}, x0 + 4, y0 + 8)


def _door(L, cx, y0, kind):
    """Ground-storey doors centered in the cell at cx (y0 = the row's top), each
    drawn as a left half and mirrored."""
    if kind == "double":
        L.rect(cx + 2, y0 + 1, 6, 14, "w0")
        L.hline(cx + 1, cx + 7, y0 + 1, "w0")
        L.hline(cx + 1, cx + 7, y0 + 2, "w2")
        L.rect(cx + 4, y0 + 3, 4, 12, "b1")
        L.vline(cx + 7, y0 + 3, y0 + 14, "ink")
        E.outline_rect(L, cx + 4, y0 + 4, 3, 4, "b0")
        E.outline_rect(L, cx + 4, y0 + 9, 3, 4, "b0")
        L.px(cx + 6, y0 + 8, "oc3")
        L.vline(cx + 3, y0 + 3, y0 + 14, "w2")
        L.hline(cx + 2, cx + 7, y0 + 15, "w2")
        L.hline(cx + 1, cx + 7, y0, "ink")
    elif kind == "arched":
        rows = [
            "   kkkk",
            "  kwwww",
            " kwkkkk",
            " kwk111",
            "kwk1000",
            "kwk1000",
            "kwk1o00",
            "kwk1000",
            "kwk1000",
            "kwk1000",
            "kwk1000",
            "kwk1o00",
            "kwk1000",
            "kwkkkkk",
            "kwwwwww",
        ]
        L.blit(rows, {"k": "ink", "w": "w0", "1": "wd1", "0": "wd0", "o": "oc3"}, cx + 1, y0 + 1)
    elif kind == "shop":
        L.rect(cx + 1, y0 + 2, 7, 13, "ink")
        L.rect(cx + 2, y0 + 3, 6, 6, "wd0")
        L.hline(cx + 2, cx + 7, y0 + 6, "wd1")
        L.blit(["k", "1", "1"], {"k": "tc0", "1": "tc2"}, cx + 3, y0 + 3)
        L.blit(["b", "0"], {"b": "b1", "0": "b0"}, cx + 6, y0 + 4)
        L.rect(cx + 1, y0 + 9, 7, 6, "wd1")
        L.hline(cx + 1, cx + 7, y0 + 9, "oc3")
        L.hline(cx + 1, cx + 7, y0 + 10, "oc2")
        L.hline(cx + 1, cx + 7, y0 + 14, "wd0")
        L.hline(cx, cx + 7, y0 + 1, "w0")
        E.outline_rect(L, cx, y0 + 1, 16, 15, "ink")
    elif kind == "window_low":
        L.rect(cx + 3, y0 + 2, 5, 6, "w0")
        L.rect(cx + 4, y0 + 3, 4, 4, "ink")
        L.vline(cx + 5, y0 + 3, y0 + 6, "wd1")
        L.hline(cx + 2, cx + 7, y0 + 8, "w2")
    elif kind == "jar":
        L.rect(cx + 1, y0 + 11, 7, 3, "w2")
        L.hline(cx + 1, cx + 7, y0 + 11, "w0")
        L.hline(cx, cx + 7, y0 + 14, "ink")
        E.amphora(L, cx + 4, y0 - 1, body="tc2", lit="tc3", shade="tc1")
        return   # the amphora isn't symmetric; its tiles are its own
    _half(L, cx, y0, y0 + 16)


def upper_storey():
    s = Struct("upper", "House upper storey, ochre", 8, 1, walk=["XXXXXXXX"], ground="none",
               notes="One-cell parts for the upper storey, in a row under the roof's eaves: "
                     "(0) west corner pilaster, (1) plain wall, (2) a window with blue "
                     "shutters folded back, (3) a window with a wooden grille, (4) a pair of "
                     "small arched windows, (5)-(6) a timber balcony with a rug over its rail "
                     "and a door behind (always as a pair), (7) east corner pilaster.")
    L = s.B
    _upper_wall(L, 0, 128)
    _pilasters(L, 128, 0, 16)
    _window(L, 32, 0, "shutter")
    _window(L, 48, 0, "grille")
    _window(L, 64, 0, "arched")
    _balcony(L, 80, 0)
    s.names = {"W": (0, 0), "wall": (1, 0), "shutters": (2, 0), "grille": (3, 0),
               "arched": (4, 0), "balcony_l": (5, 0), "balcony_r": (6, 0), "E": (7, 0)}
    return finish(s)


def signs_storey():
    kinds = ("tavern", "bronze", "potter", "perfume", "ships", "grain", "wheel")
    s = Struct("signs", "House upper storey with trade signs, ochre", 7, 1, walk=["XXXXXXX"],
               ground="none",
               notes="Upper-storey wall cells with a trade sign hung from an iron bracket: "
                     "(0) tavern (a kantharos cup), (1) bronze-smith (a Corinthian helmet), "
                     "(2) potter (an amphora), (3) perfumer (an aryballos), (4) shipwright "
                     "(a hull and sail), (5) grain and the hiring hall (a sack), (6) the "
                     "wheelwright, Alfred's chariot store (a spoked wheel). Put one over "
                     "the door of the trade's house.")
    L = s.B
    _upper_wall(L, 0, 112)
    for i, k in enumerate(kinds):
        _sign(L, i * 16, k)
    s.names = {k: (i, 0) for i, k in enumerate(kinds)}
    return finish(s)


def ground_storey():
    s = Struct("lower", "House ground storey, ochre", 8, 1, walk=["XDDDXXXX"], ground="none",
               notes="One-cell parts for the ground storey: (0) west pilaster, (1) a "
                     "double-leaf blue door in a marble frame, (2) an arched wooden door, "
                     "(3) an open shopfront with a counter (a door too), (4) plain wall, (5) "
                     "a low barred window, (6) a stone bench with an amphora, (7) east "
                     "pilaster. (1)-(3) are MB_NON_ANIMATED_DOOR: put the warp there.")
    L = s.B
    _lower_wall(L, 0, 128)
    _pilasters(L, 128, 0, 16)
    _door(L, 16, 0, "double")
    _door(L, 32, 0, "arched")
    _door(L, 48, 0, "shop")
    _door(L, 80, 0, "window_low")
    _door(L, 96, 0, "jar")
    s.names = {"W": (0, 0), "door": (1, 0), "door_arched": (2, 0), "shop": (3, 0),
               "wall": (4, 0), "window": (5, 0), "bench": (6, 0), "E": (7, 0)}
    return finish(s)


# Eight houses from the kit, each different. (title, rose?, upper rows, ground row,
# ridge variants). Upper and ground list the middle cells; the corner pilasters
# and the roof's ends are added. A second upper row makes a three-storey house.
RECIPES = [
    ("A house with shutters", False, [["shutters", "wall", "grille"]],
     ["door", "wall", "window"], [None, None, None]),
    ("A rose house with a balcony", True, [["balcony_l", "balcony_r"]],
     ["bench", "door_arched"], ["chimney", None]),
    ("The tavern", False, [["arched", "sign:tavern", "arched"]],
     ["window", "door", "bench"], [None, "acroterion", None]),
    ("A rose house with a shop", True, [["grille", "shutters"]],
     ["shop", "door"], [None, "chimney"]),
    ("The bronze-smith's house", False, [["sign:bronze", "balcony_l", "balcony_r", "shutters"]],
     ["shop", "wall", "door_arched", "window"], ["chimney", None, None, None]),
    ("The perfumer's house", True, [["shutters", "sign:perfume", "wall", "arched"]],
     ["window", "shop", "door", "bench"], [None, None, "acroterion", None]),
    ("The potter's narrow house", False, [["sign:potter"]], ["door_arched"], ["chimney"]),
    ("A tall rose house, three storeys", True,
     [["arched", "shutters", "arched"], ["grille", "balcony_l", "balcony_r"]],
     ["window", "door", "window"], [None, "chimney", None]),
]


def recipe_cells(recipe):
    """The house as rows of (structure key, part name), top to bottom."""
    title, is_rose, uppers, lower, ridge = recipe
    up, lo, sg = ("upper_rose", "lower_rose", "signs_rose") if is_rose else ("upper", "lower", "signs")
    n = len(lower)
    rows = [[("roof", "W")] + [("roof", r or "run") for r in ridge] + [("roof", "E")],
            [("roof", "eaves_W")] + [("roof", "eaves_run")] * n + [("roof", "eaves_E")]]
    for upper in uppers:   # top storey first
        rows.append([(up, "W")] + [((sg, p[5:]) if p.startswith("sign:") else (up, p))
                                     for p in upper] + [(up, "E")])
    rows.append([(lo, "W")] + [(lo, p) for p in lower] + [(lo, "E")])
    return rows


def rose(s, key, title):
    t = E.recolor(s, E.ROSE, key=key, title=title,
                  notes=s.notes.replace("ochre", "rose").replace("blue", "sea-green")
                  + " The rose parts are the ochre parts' own tiles in the rose palette.")
    t.names = dict(getattr(s, "names", {}))
    return t


def yard_paving():
    s = Struct("yard", "Poros yard paving", 1, 1, walk=["."], ground="quay",
               notes="The warm poros blocks of the workshops' yards and the back lanes. The "
                     "workshop props stand on it. It meets the marble paving with a plain "
                     "joint.")
    return finish(s)


def build(yard=True, terrace=True, plaza=True):
    up = upper_storey()
    lo = ground_storey()
    sg = signs_storey()
    streets = [paving_set()] + ([plaza_inlay()] if plaza else []) + [kerbs(), steps()]
    streets += ([terrace_wall()] if terrace else []) + ([yard_paving()] if yard else [])
    houses = [roof_kit(), up, rose(up, "upper_rose", "House upper storey, rose"),
              lo, rose(lo, "lower_rose", "House ground storey, rose"),
              sg, rose(sg, "signs_rose", "House upper storey with trade signs, rose")]
    return streets, houses
