"""The great Agora of Emporion (gTileset_Emporion).

The stoa: a long Doric colonnade under a terracotta roof, built from bays two
cells wide. Its roof and entablature repeat every bay; the bottom row of a bay
is chosen per shop (a door into a shop, a counter of goods, an open bay, the
Agora shop itself under its striped awning). Lay the broad steps' lower row
along its front as the stylobate.

The market: free-standing stalls under striped awnings (spices, bronze,
pottery, cloth, fish, wine) and Kydon's honey stall under its painted
bull-leaper. Also the public notice board with the Archon's owl seal (and the
little hook under it), and Corinth's emblem, a gilded Pegasus on a column.
"""
from __future__ import annotations

import emporion_lib as E
from emporion_lib import Struct, finish

# ==========================================================================
# The stoa
# ==========================================================================

STOA_W = 32   # a bay is two cells


def _stoa_upper(L, w, columns):
    """Rows 0-2 of the stoa, w px wide: roof, entablature, capitals over each
    column (x of the column's left edge)."""
    E.roof(L, 0, 0, w, 32, ends=(True, True))
    y = 32
    L.hline(0, w - 1, y, "w0")
    L.hline(0, w - 1, y + 1, "m2")
    # the triglyph frieze: a triglyph over each column and mid-bay, painted metopes
    for x in range(0, w):
        X = x % 16
        for yy in range(y + 2, y + 7):
            if X in (1, 2, 3, 4, 5):
                c = "b0" if X in (2, 4) else "b1"
            else:
                c = "m1"
                if X in (10, 11, 12) and yy in (y + 3, y + 4, y + 5):
                    c = "rd" if (X == 11 and yy == y + 4) else "m2"
            L.px(x, yy, c)
    L.hline(0, w - 1, y + 7, "m3")
    L.hline(0, w - 1, y + 8, "w0")
    L.hline(0, w - 1, y + 9, "m1")
    L.hline(0, w - 1, y + 10, "m4")
    L.rect(0, y + 11, w, 5, "m5")
    L.hline(0, w - 1, y + 11, "ink")
    for x in columns:
        E.doric_capital(L, x + 2, y + 10, 5)
        E.shaft(L, x + 1, y + 15, 7, 1)
    # the end walls (antae), capped by the entablature
    for x0, aw, lit in ((0, 8, True), (w - 7, 7, False)):
        L.rect(x0, y + 11, aw, 5, "m2" if lit else "m3")
        L.vline(x0, y, y + 15, "ink")
        L.vline(x0 + aw - 1, y + 11, y + 15, "ink")
        L.vline(x0 + 1, y + 11, y + 15, "w0" if lit else "m4")
        L.vline(x0 + aw - 2, y + 11, y + 15, "m3" if lit else "m4")


def _column_lower(L, x):
    """The bottom row of a stoa column at x (its left edge), with its base."""
    L.vline(x, 48, 60, "ink")
    E.shaft(L, x + 1, 48, 7, 13)
    L.rect(x, 61, 9, 3, "m1")
    L.hline(x, x + 8, 61, "w0")
    L.hline(x, x + 8, 63, "m4")
    L.vline(x, 61, 63, "ink")
    L.vline(x + 8, 61, 63, "ink")


def _anta_lower(L, x0, lit, w=8):
    """The end wall's foot, w px wide (a whole tile column, so the portico's
    colors never share its tiles)."""
    L.rect(x0, 48, w, 16, "m2" if lit else "m3")
    L.vline(x0, 48, 63, "ink")
    L.vline(x0 + w - 1, 48, 63, "ink")
    L.vline(x0 + 1, 48, 62, "w0" if lit else "m4")
    L.vline(x0 + w - 2, 48, 62, "m3" if lit else "m4")
    for y in range(51, 63, 4):
        L.hline(x0 + 1, x0 + w - 2, y, "m3" if lit else "m4")
    L.hline(x0, x0 + w - 1, 63, "ink")


def _portico(L, bx, w):
    """The portico floor in deep shade and the back wall's foot (market group)."""
    L.rect(bx, 48, w, 16, "ink")
    L.rect(bx, 49, w, 11, "wd1")


def _bay_lower(L, x0, kind):
    """The bottom row of a bay: x0..x0+8 the column, x0+9..x0+31 the bay."""
    bx = x0 + 9
    _portico(L, x0 + 8, 24)
    _column_lower(L, x0)
    if kind == "open":
        L.rect(bx + 8, 49, 7, 10, "ink")
        L.rect(bx + 1, 56, 20, 2, "w0")
        L.hline(bx + 1, bx + 20, 58, "sl2")
        L.vline(bx + 2, 58, 60, "sl2")
        L.vline(bx + 19, 58, 60, "sl2")
    elif kind == "door":
        L.rect(bx + 5, 49, 12, 12, "w0")
        L.rect(bx + 7, 51, 8, 10, "rd")
        L.vline(bx + 11, 51, 60, "ink")
        L.px(bx + 10, 56, "sf")
        L.px(bx + 12, 56, "sf")
        for yy in (52, 57):
            L.hline(bx + 8, bx + 9, yy, "tc0")
            L.hline(bx + 13, bx + 14, yy, "tc0")
        L.hline(bx + 5, bx + 16, 61, "sl3")
    elif kind in ("spice", "cloth", "pots"):
        L.rect(bx, 55, 23, 6, "wd2")
        L.hline(bx, bx + 22, 55, "sf2")
        L.hline(bx, bx + 22, 60, "ink")
        for xx in range(bx + 3, bx + 23, 6):
            L.vline(xx, 57, 59, "wd1")
        if kind == "spice":
            for i, (c, hi) in enumerate((("sf", "sf2"), ("rd", "tc2"), ("w0", "w0"), ("ol1", "sf2"))):
                xx = bx + 1 + i * 5
                L.blit([" 12 ", "1222", "kwwk"], {"1": c, "2": hi, "k": "ink", "w": "wd2"}, xx, 52)
            for xx in range(bx + 2, bx + 21, 5):
                L.blit(["k", "t", "t"], {"k": "ink", "t": "tc1"}, xx, 49)
        elif kind == "cloth":
            for i, c in enumerate(("pu1", "sf", "w0", "pu0", "rd")):
                xx = bx + 1 + i * 4
                L.rect(xx, 49, 3, 6, c)
                L.vline(xx + 2, 49, 54, "ink" if c in ("w0", "pu0") else "pu0")
            for i, c in enumerate(("pu1", "w0", "sf")):
                L.rect(bx + 2 + i * 7, 53, 5, 2, c)
                L.hline(bx + 2 + i * 7, bx + 6 + i * 7, 54, "ink")
        elif kind == "pots":
            for i in range(3):
                E.amphora(L, bx + 1 + i * 7, 48, small=True, body="tc2", lit="w0", shade="tc1")
            for i in range(4):
                xx = bx + 2 + i * 5
                L.blit(["kkkk", "k22k", " kk "], {"k": "ink", "2": "tc2"}, xx, 52)


def _agora_bay(L, x0):
    """The Agora shop's bay (bottom row): its pinax sign (the Agora's jar) and
    the shop's door. Its striped awning is in the row above (_shaft_row)."""
    bx = x0 + 9
    _portico(L, x0 + 8, 24)
    _column_lower(L, x0)
    L.rect(bx + 4, 49, 12, 12, "w0")
    L.rect(bx + 6, 50, 8, 11, "rd")
    L.rect(bx + 7, 51, 6, 10, "tc1")
    L.vline(bx + 10, 51, 60, "ink")
    L.hline(bx + 4, bx + 15, 61, "sl3")
    L.rect(bx + 17, 49, 5, 7, "w0")
    E.outline_rect(L, bx + 16, 48, 7, 9, "ink")
    L.blit([" k ", "k2k", "k2k", " k "], {"k": "tc0", "2": "tc2"}, bx + 17, 50)


def _shaft_row(L, w, columns, y, agora_x=None):
    """The colonnade's middle row, y..y+15: tall shafts before the deep shadow of
    the portico, the back wall's top; over the Agora's bay, its red-and-white
    awning slung between the columns."""
    for x in range(w):
        for yy in range(y, y + 16):
            L.px(x, yy, "ink" if yy < y + 9 else "wd1")
        L.px(x, y + 9, "tc0")
    if agora_x is not None:
        bx = agora_x + 9
        L.hline(bx - 1, bx + 23, y + 9, "ink")
        for x in range(bx - 1, bx + 24):
            stripe = "rd" if ((x - bx) // 3) % 2 == 0 else "w0"
            for yy in range(y + 10, y + 15):
                L.px(x, yy, stripe)
            L.px(x, y + 15, stripe if (x - bx) % 3 == 1 else "ink")
    for x in columns:
        L.vline(x, y, y + 15, "ink")
        E.shaft(L, x + 1, y, 7, 16)
        L.vline(x + 8, y, y + 15, "ink")
    for x0, aw, lit in ((0, 8, True), (w - 7, 7, False)):
        L.rect(x0, y, aw, 16, "m2" if lit else "m3")
        L.vline(x0, y, y + 15, "ink")
        L.vline(x0 + aw - 1, y, y + 15, "ink")
        L.vline(x0 + 1, y, y + 15, "w0" if lit else "m4")
        L.vline(x0 + aw - 2, y, y + 15, "m3" if lit else "m4")
        for yy in range(y + 3, y + 16, 4):
            L.hline(x0 + 1, x0 + aw - 2, yy, "m3" if lit else "m4")


KINDS = ["open", "door", "spice", "cloth", "pots", "agora"]

TITLES = {
    "open": ("stoa_bay", "Stoa bay: open",
             "One bay of the colonnade, two cells wide and five tall: roof, eaves, the "
             "triglyph frieze with its painted metopes, and a tall Doric column at the bay's "
             "left before the portico's deep shadow. Its bottom row is the portico with a bench "
             "and a doorway at the back. Repeat bays for length: every bay's top four rows are "
             "the same tiles. All impassable."),
    "door": ("stoa_bay_door", "Stoa bay: a shop door",
             "As stoa_bay, with a red door at the back of the portico: bottom row, second "
             "column, MB_NON_ANIMATED_DOOR. Put a shop's warp there."),
    "spice": ("stoa_bay_spice", "Stoa bay: the spice seller's counter",
              "As stoa_bay, with a counter of baskets heaped with saffron, sumac, salt and "
              "herbs. Both bottom cells are MB_COUNTER, so the player talks across them to a "
              "seller standing in front of the bay's column."),
    "cloth": ("stoa_bay_cloth", "Stoa bay: the cloth merchant's counter",
              "As stoa_bay_spice, with bolts of purple, saffron and white cloth."),
    "pots": ("stoa_bay_pots", "Stoa bay: the potter's counter",
             "As stoa_bay_spice, with black-figure cups and jugs and three amphorae."),
    "agora": ("stoa_agora", "Stoa bay: the Agora shop",
              "The Agora (the game's shop) as a bay of the stoa: a red-and-white awning slung "
              "between the columns, a pinax with the Agora's jar, and the door: bottom row, "
              "second column, MB_NON_ANIMATED_DOOR. Warp to the Agora interior here."),
}


def stoa():
    """Every stoa piece on one sheet: the west end, six bays, the east end; five
    rows: roof, eaves, entablature, the tall shafts, the bays' contents."""
    n = len(KINDS)
    w = 16 + n * STOA_W + 16
    low = Struct("_stoa4", "", w // 16, 4, ground="none")
    L = low.B
    cols = [16 + i * STOA_W for i in range(n + 1)]
    _stoa_upper(L, w, cols)
    _portico(L, 8, 8)
    _anta_lower(L, 0, True)
    for i, k in enumerate(KINDS):
        x0 = 16 + i * STOA_W
        if k == "agora":
            _agora_bay(L, x0)
        else:
            _bay_lower(L, x0, k)
    xe = 16 + n * STOA_W
    _column_lower(L, xe)
    L.vline(xe + 8, 48, 60, "ink")
    _anta_lower(L, xe + 9, False, w=7)
    s = Struct("_stoa", "", w // 16, 5, ground="none")
    s.B.a[0:48] = L.a[0:48]
    s.B.a[64:80] = L.a[48:64]
    _shaft_row(s.B, w, cols, 48, agora_x=16 + KINDS.index("agora") * STOA_W)
    return s


def stoa_pieces():
    s = stoa()
    out = [E.sub(s, "stoa_end_w", "Stoa: west end", 0, 0, 1, 5,
                 notes="The stoa's west end: the roof's verge, the entablature's return and "
                       "the end wall (anta). Impassable.")]
    for i, k in enumerate(KINDS):
        key, title, notes = TITLES[k]
        walk = ["XX"] * 5
        if k in ("door", "agora"):
            walk[4] = "XD"
        b = E.sub(s, key, title, 1 + i * 2, 0, 2, 5, walk=walk, notes=notes)
        if k in ("spice", "cloth", "pots"):
            b.behaviors[(0, 4)] = "MB_COUNTER"
            b.behaviors[(1, 4)] = "MB_COUNTER"
        out.append(b)
    out.append(E.sub(s, "stoa_end_e", "Stoa: east end", s.w - 1, 0, 1, 5,
                     notes="The stoa's east end: the last column, the shaded verge and the "
                           "end wall. Impassable."))
    return out


# ==========================================================================
# Market stalls
# ==========================================================================

GOODS = {
    "spice": "Saffron, sumac, cumin and salt heaped in baskets",
    "bronze": "Bronze mirrors, a jug, a helmet and a little tripod (Corinthian bronze)",
    "pottery": "Black-figure jugs and cups, and an amphora",
    "cloth": "Bolts of Tyrian purple, saffron and white",
    "fish": "Silver fish on a wet slab, an octopus and a basket of sprats",
    "wine": "A krater, wine jugs and a rack of amphorae",
}


def _awning(M, c1, edge):
    """A striped canvas awning (row 0), in the clay palette: stripes of c1 and
    white, symmetric every 8 px, a shaded valance and a scalloped hem, the four
    posts' tops. Recolored to clay2 it is the rose or green awning, same tiles."""
    for y in range(1, 14):
        for x in range(32):
            X = x % 8
            M.px(x, y, c1 if X in (2, 3, 4, 5) else "w0")
    M.hline(0, 31, 1, "ink")
    M.vline(0, 1, 13, "ink")
    M.vline(31, 1, 13, "ink")
    M.hline(1, 30, 11, edge)
    for x in range(32):
        X = x % 4
        M.px(x, 13, "ink" if X in (0, 3) else (c1 if x % 8 in (2, 3, 4, 5) else "w0"))
        if X in (0, 3):
            M.px(x, 12, edge)
    M.hline(0, 31, 14, "ink")
    for x in (1, 30):
        M.px(x, 15, "ink")
    for x in (2, 29):
        M.px(x, 15, "wd1")


def _stall_frame(M):
    """The stall's posts and counter (row 1); its lower half is every stall's."""
    for x in (1, 30):
        M.vline(x, 16, 30, "ink")
    for x in (2, 29):
        M.vline(x, 16, 30, "wd1")
    M.rect(1, 22, 30, 8, "wd2")
    M.hline(1, 30, 22, "wd1")
    M.hline(1, 30, 29, "ink")
    M.vline(0, 22, 29, "ink")
    M.vline(31, 22, 29, "ink")
    for x in (7, 8, 15, 16, 23, 24):
        M.vline(x, 24, 28, "wd1")
    M.hline(2, 29, 30, "ink")


AWNINGS = {
    # colorway: (clay color, valance shade, recolor to clay2?)
    "ochre": ("oc2", "oc0", False), "blue": ("b1", "b0", False),
    "rose": ("oc2", "oc0", True), "green": ("b1", "b0", True),
}


def _stall(key, title, notes, colorway):
    s = Struct(key, title, 2, 2, walk=["XX", "XX"],
               notes=notes + " Free-standing on the paving; the seller stands beside it.")
    M = s.M
    c1, edge, rose = AWNINGS[colorway]
    _awning(M, c1, edge)
    if rose:
        aw = E.recolor(s, E.ROSE)
        M.a[0:16] = aw.M.a[0:16]
    _stall_frame(M)
    return s


def stalls():
    out = []
    s = _stall("stall_spice", "Market stall: spices", GOODS["spice"] + ".", "ochre")
    M = s.M
    for i, (c, hi) in enumerate((("sf", "sf2"), ("rd", "tc2"), ("wd2", "sf2"), ("w0", "w0"),
                                 ("ol1", "sf2"))):
        M.blit([" 12 ", "1222", "kwwk"], {"1": c, "2": hi, "k": "ink", "w": "wd1"}, 4 + i * 5, 18)
    out.append(s)
    s = _stall("stall_bronze", "Market stall: bronze", GOODS["bronze"] + ".", "blue")
    M = s.M
    M.blit([" kk ", "kGgk", "kgbk", " kk "], {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 4, 17)
    M.blit(["  kkk ", " kGggk", "kGgkgk", "kgk gk", " kk kk"], {"k": "ink", "G": "g1", "g": "g0"}, 9, 16)
    M.blit([" kkk ", "kGggk", " kgk ", " kgk ", "kgggk"], {"k": "ink", "G": "g1", "g": "g0"}, 16, 16)
    M.blit(["kkkkk", "kGggk", " k k ", "k   k"], {"k": "ink", "G": "g1", "g": "g0"}, 22, 17)
    out.append(s)
    s = _stall("stall_pottery", "Market stall: pottery", GOODS["pottery"] + ".", "rose")
    M = s.M
    for i in range(3):
        M.blit(["kkkk", "k22k", "kkkk", "k22k", " kk "], {"k": "ink", "2": "tc2"}, 4 + i * 6, 17)
    M.blit(["  kk  ", " k22k ", "k2211k", "k2211k", " k11k "], {"k": "ink", "2": "tc2", "1": "tc1"},
           22, 16)
    out.append(s)
    s = _stall("stall_cloth", "Market stall: cloth", GOODS["cloth"] + ".", "green")
    M = s.M
    for i, c in enumerate(("pu1", "sf", "w0", "pu0", "rd")):
        x = 4 + i * 5
        M.rect(x, 18, 4, 4, c)
        M.hline(x, x + 3, 21, "ink" if c != "pu0" else "pu1")
        M.px(x + 3, 18, "ink")
    out.append(s)
    s = _stall("stall_fish", "Market stall: fish", GOODS["fish"] + ".", "blue")
    M = s.M
    M.rect(3, 19, 26, 3, "sl3")
    for x in range(4, 22, 6):
        M.blit(["kssssk ", " kwwssk"], {"k": "ink", "s": "sl2", "w": "w0"}, x, 18)
    M.blit([" rr ", "rrrr", "r rr"], {"r": "rd"}, 23, 17)
    out.append(s)
    s = _stall("stall_wine", "Market stall: wine", GOODS["wine"] + ".", "rose")
    M = s.M
    M.blit(["kkkkkkk", "k22222k", " k222k ", "  k2k  ", " kkkkk "], {"k": "ink", "2": "tc2"}, 4, 16)
    for x in (14, 19, 24):
        M.blit([" k ", "kpk", "kpk", " k "], {"k": "ink", "p": "pu1"}, x, 17)
    out.append(s)
    # Kydon's honey: a Minoan bull-leaper painted on the awning
    s = Struct("stall_honey", "Kydon's honey stall", 2, 2, walk=["XX", "XX"],
               notes="Kydon, the Knossan honey-seller (LABYRINTH.md seed 3): his awning is "
                     "painted with a bull-leaper over a wavy Minoan border. Honey jars and a "
                     "comb on the counter.")
    M = s.M
    M.rect(0, 1, 32, 13, "w0")
    M.hline(0, 31, 1, "ink")
    M.vline(0, 1, 13, "ink")
    M.vline(31, 1, 13, "ink")
    for x in range(1, 31):
        M.px(x, 11 + (1 if (x // 3) % 2 else 0), "rd")
    M.hline(0, 31, 14, "ink")
    M.hline(0, 31, 13, "ink")
    bull = [
        "            k ",
        " kk  kkkkkkkrk",
        "krrkkrrrrrrrrk",
        " krrrrrrrrrrk ",
        "  krkk  krkrk ",
        "  kk     k  k ",
    ]
    M.blit(bull, {"k": "ink", "r": "rd"}, 8, 4)
    M.blit(["  kk", " kk ", "kk  "], {"k": "ink"}, 15, 2)
    M.px(17, 2, "sf")
    for x in (1, 30):
        M.px(x, 15, "ink")
    for x in (2, 29):
        M.px(x, 15, "wd1")
    _stall_frame(M)
    for i in range(3):
        M.blit([" kk ", "ksfk", "kffk", " kk "], {"k": "ink", "s": "sf2", "f": "sf"}, 4 + i * 6, 18)
    M.blit(["kkkk", "k22k", "k22k", "kkkk"], {"k": "ink", "2": "sf2"}, 22, 18)
    out.append(s)
    return out


# ==========================================================================
# The notice board and Pegasus
# ==========================================================================

def notice_board():
    s = Struct("notice_board", "The public notice board (the Archon's owl seal)", 2, 2,
               walk=["XX", "XX"],
               notes="A whitened board (leukoma) on a marble base, where proclamations are "
                     "posted. The notice carries the Archon's owl seal in red wax, with a tiny "
                     "hook cut under it (STORY.md I-4: 'Odd. There's a little hook under the "
                     "owl.'). Give both bottom cells the same bg event.")
    M = s.M
    M.rect(2, 3, 28, 19, "w0")
    E.outline_rect(M, 1, 2, 30, 21, "ink")
    M.hline(2, 29, 3, "m1")
    M.hline(1, 30, 1, "m3")
    M.hline(3, 28, 0, "m2")
    for y in (6, 8, 10, 12, 14):
        for x in range(4, 28):
            if x % 8 not in (3, 6) and not (y == 14 and x > 15) and not (y == 12 and x > 19):
                M.px(x, y, "m4")
    M.hline(4, 18, 5, "ink")
    seal = [" kkkk ", "krrrrk", "krwwrk", "krkkrk", "krwwrk", " kkkk "]
    M.blit(seal, {"k": "ink", "r": "rd", "w": "g1"}, 21, 13)
    M.px(24, 20, "ink")
    M.px(24, 21, "ink")
    M.px(23, 21, "ink")
    M.rect(5, 23, 22, 7, "m2")
    M.hline(5, 26, 23, "m1")
    M.hline(5, 26, 29, "m4")
    M.vline(4, 23, 29, "ink")
    M.vline(27, 23, 29, "ink")
    M.hline(4, 27, 30, "ink")
    M.rect(6, 25, 20, 3, "m3")
    M.hline(7, 24, 26, "m2")
    return s


def pegasus():
    s = Struct("pegasus_column", "Pegasus on his column, Corinth's emblem", 2, 3,
               walk=["TT", "XX", "XX"],
               notes="A gilded bronze Pegasus rearing on an Ionic column: Bellerophon caught "
                     "him at the Peirene spring. Put it in the middle of the Agora. The top "
                     "row draws over the player.")
    T, M = s.T, s.M
    E.shaft(M, 11, 22, 10, 30)
    E.ionic_capital(M, 11, 17, 10)
    M.rect(7, 52, 18, 10, "m2")
    M.hline(7, 24, 52, "m1")
    M.hline(7, 24, 53, "w0")
    M.hline(7, 24, 61, "m4")
    M.vline(6, 52, 61, "ink")
    M.vline(25, 52, 61, "ink")
    M.hline(6, 25, 62, "ink")
    M.hline(6, 25, 51, "ink")
    M.rect(9, 55, 14, 4, "m3")
    M.blit(["k k k", " kkk "], {"k": "g0"}, 13, 56)
    # rearing to the west, wings raised, his hind hooves on the capital
    horse = [
        "              kk      ",
        "             kGGk  kk ",
        "            kGgGk kGGk",
        "   kkk     kGgGk kGgGk",
        "  kGGGk   kGgGk kGgGk ",
        " kGgGGgk kGgGk kGgGk  ",
        " kkgggGkkGgGk kGgGk   ",
        "  kkkggGkGgGkkGgGk    ",
        "   k  kGGGggGGgGk     ",
        "  kGk kGgggggggk      ",
        " kGgGkkGggggggbk      ",
        " kgk kGggggggbbk      ",
        "  k   kgggbbbbk       ",
        "      kgbk kgbk       ",
        "      kgk   kgk       ",
        "     kbk    kbk       ",
        "     kk     kk        ",
    ]
    T.blit(horse, {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 5, 0)
    for y in range(16, 18):
        for x in range(32):
            if T.a[y, x, 3]:
                M.a[y, x] = T.a[y, x]
                T.a[y, x] = 0
    return s


def stall(kind):
    """One stall by kind (spice, bronze, pottery, cloth, fish, wine, honey), finished."""
    s = next(t for t in stalls() if t.key == f"stall_{kind}")
    return finish(s)


def build():
    out = stoa_pieces() + stalls() + [notice_board(), pegasus()]
    for t in out:
        finish(t)
    return out
