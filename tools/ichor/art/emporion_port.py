"""The port of Lechaion and the Diolkos (gTileset_Emporion).

Quays of warm poros with their coping and wet faces, bollards, warehouses (the
hiring hall among them), ship sheds with their slipways, a harbor crane, the
harbor's goods, a merchant ship with a swan-neck stern, and the Diolkos: the
paved stone track with its wheel ruts on which ships were hauled across the
Isthmus, with the same merchant ship riding its wheeled cradle.

The sea is always aethos's animated sea: cells marked sea borrow it.
"""
from __future__ import annotations

import emporion_lib as E
from emporion_lib import Struct, finish

WOODK = {"k": "ink", "0": "wd0", "1": "wd1", "2": "wd2", "3": "wd3", "r": "rp", "w": "w0",
         "R": "rd", "b": "b0", "B": "b1", "G": "g1", "g": "g0", "z": "br"}

# ==========================================================================
# Quays
# ==========================================================================


def _coping_n(L, x0, y0, w):
    """Coping along a quay's north edge, the water beyond: big lit blocks."""
    for x in range(x0, x0 + w):
        L.px(x, y0, "s5")
        L.px(x, y0 + 1, "s4")
        L.px(x, y0 + 2, "s4" if (x - x0) % 16 else "s2")
        L.px(x, y0 + 3, "s2")
        L.px(x, y0 + 4, "s1")


def _face_s(L, x0, y0, w):
    """A quay's south edge: coping, then its wet face down to the water."""
    for x in range(x0, x0 + w):
        L.px(x, y0, "s4")
        L.px(x, y0 + 1, "s3")
        L.px(x, y0 + 2, "s1")
        for y in range(y0 + 3, y0 + 9):
            c = "wt1" if (x + y) % 8 else "wt0"
            if (x - x0) % 16 == 0:
                c = "wt0"
            L.px(x, y, c)
        L.px(x, y0 + 9, "ol1" if x % 4 else "wt0")
        L.px(x, y0 + 10, "wt0")
        L.px(x, y0 + 11, "ink")


def _coping_w(L, x0, y0, h):
    for y in range(y0, y0 + h):
        L.px(x0, y, "s1")
        L.px(x0 + 1, y, "s5")
        L.px(x0 + 2, y, "s4")
        L.px(x0 + 3, y, "s4" if (y - y0) % 16 else "s2")
        L.px(x0 + 4, y, "s2")


def _coping_e(L, x1, y0, h):
    for y in range(y0, y0 + h):
        L.px(x1, y, "ink")
        L.px(x1 - 1, y, "s2")
        L.px(x1 - 2, y, "s3")
        L.px(x1 - 3, y, "s4" if (y - y0) % 16 else "s2")
        L.px(x1 - 4, y, "s2")


def quay():
    s = Struct("quay", "Lechaion's quays: poros paving, edges and corners", 5, 3,
               walk=["XX.XX", "...XX", "XX.XX"], ground="none",
               notes="Long poros blocks in a running bond; the sea is aethos's, in the next "
                     "cells. Row 0: NW outer corner, north edge (water north: coping only), NE "
                     "outer corner, inner corners NW and NE (water diagonally beyond). Row 1: "
                     "west edge, plain quay, east edge, inner corners SW and SE. Row 2: SW "
                     "corner, south edge (water south: the wet face shows, weed at the "
                     "waterline), SE corner, then the plain quay's two alternates. The walk "
                     "codes are akti's: open the water-side edges only for surfing.")
    L = s.B
    E.quay_paving(L, 0, 0, 80, 48)
    # outer edges of the 3x3
    _coping_n(L, 0, 0, 48)
    _coping_w(L, 0, 0, 48)
    _coping_e(L, 47, 0, 48)
    _face_s(L, 0, 36, 48)
    # inner corners: a coping notch at one corner
    for (cx, cy, sx, sy) in ((3, 0, 0, 0), (4, 0, 1, 0), (3, 1, 0, 1), (4, 1, 1, 1)):
        x0, y0 = cx * 16 + (11 if sx else 0), cy * 16 + (11 if sy else 0)
        L.rect(x0, y0, 5, 5, "s4")
        L.hline(x0, x0 + 4, y0 + (4 if sy else 0), "s1")
        L.vline(x0 + (4 if sx else 0), y0, y0 + 4, "s1")
        L.px(x0 + (4 if sx else 0), y0 + (4 if sy else 0), "sk")
    # (4,2): a mooring ring set in the quay
    L.blit([" kkk ", "k   k", "k   k", " kkk "], {"k": "sk"}, 69, 37)
    L.px(70, 38, "s5")
    s.names = {"NW": (0, 0), "N": (1, 0), "NE": (2, 0), "inNW": (3, 0), "inNE": (4, 0),
               "W": (0, 1), "C": (1, 1), "E": (2, 1), "inSW": (3, 1), "inSE": (4, 1),
               "SW": (0, 2), "S": (1, 2), "SE": (2, 2), "C2": (3, 2), "ring": (4, 2)}
    return finish(s)


def bollards():
    s = Struct("bollards", "Bollards: one with a mooring line", 2, 1, walk=["XX"], ground="quay",
               notes="Stone bollards for the quay's edge: (0) bare, (1) with a hawser running "
                     "up to a ship moored to the north.")
    M = s.M
    for x0 in (0, 16):
        M.blit(["  kkkk  ", " k5444k ", " k4332k ", "  k32k  ", "  k32k  ", " k4322k ",
                " k3222k ", "  kkkk  "], {"k": "ink", "5": "s3", "4": "s2", "3": "s1", "2": "s0"},
               x0 + 4, 5)
    for y in range(0, 9):
        M.px(16 + 7 + (y % 2), y, "e2" if y % 2 else "e1")
    M.px(16 + 6, 9, "e2")
    M.px(16 + 9, 9, "e1")
    return s


# ==========================================================================
# Warehouses and ship sheds
# ==========================================================================

def warehouse_wall():
    s = Struct("warehouse", "Warehouse wall (roof it with the house roof)", 6, 1,
               walk=["XXDDXX"], ground="none",
               notes="The single-storey front of a harbor warehouse in poros ashlar, to roof "
                     "with the house kit's roof (two rows, any width): (0) west end, (1) wall "
                     "with high slit windows, (2)-(3) a great double cart-door (both cells "
                     "MB_NON_ANIMATED_DOOR), (4) wall with the hiring hall's chalked board, (5) "
                     "east end. The hiring hall is the warehouse with the board, where "
                     "Hyperion's crew bosses hire dockhands (STORY.md, Bases).")
    L = s.B
    E.ashlar(L, 0, 0, 96, 16, course=5)
    L.hline(0, 95, 0, "s1")
    L.hline(0, 95, 1, "s2")
    L.hline(0, 95, 15, "sk")
    # ends
    L.vline(0, 0, 15, "ink")
    L.vline(1, 1, 14, "s5")
    L.vline(95, 0, 15, "ink")
    L.vline(94, 1, 14, "s1")
    # slit windows
    for x in (21, 26):
        L.rect(x, 3, 2, 6, "ink")
        L.px(x, 2, "s5")
    # the great double door
    L.rect(34, 2, 28, 14, "ink")
    L.rect(36, 4, 24, 12, "s0")
    for x in range(36, 60, 4):
        L.vline(x, 4, 15, "sk")
    L.vline(47, 4, 15, "ink")
    L.vline(48, 4, 15, "ink")
    L.hline(36, 59, 8, "sk")
    L.hline(36, 59, 9, "s1")
    L.px(45, 10, "s4")
    L.px(50, 10, "s4")
    L.hline(33, 62, 2, "s4")
    E.mirror_half(L, 32, 32, 0, 16)
    # the hiring hall's chalk board: a dark board with white tallies
    L.rect(67, 3, 12, 8, "sk")
    E.outline_rect(L, 66, 2, 14, 10, "ink")
    for y in (4, 6, 8):
        for x in range(68, 78):
            if (x + y) % 3:
                L.px(x, y, "w0")
    return finish(s)


def ship_sheds():
    """A row of ship sheds (neosoikoi): per bay a stone pier and a dark shed with
    a ship's stern on its slipway, which runs down into the water below."""
    w = 16 + 2 * 32 + 16
    s = Struct("_sheds", "", w // 16, 3, ground="none")
    L = s.B
    # roof: one long terracotta roof over the row of sheds (row 0)
    E.roof(L, 0, 0, w, 16, ridge=True, eaves=True)
    stern = [
        "        kk   ",
        "       k32k  ",
        "       k2k   ",
        "       k2k   ",
        "      k21k   ",
        "   kkk211kkkk",
        "  k3222211110",
        " k32RRRRRRRR0",
        " k22111111110",
        "  k211111110 ",
        "   kk0000000 ",
        "     kkkkkkk ",
    ]
    for bx in (16, 48):
        # the shed's gable under the eaves (y 16-23, clay): stucco and timber
        for x in range(bx + 8, bx + 32):
            dx = abs(x - (bx + 19.5))
            top = 16 + int(dx // 3)
            for y in range(16, 22):
                L.px(x, y, ("oc3" if x < bx + 20 else "oc2") if y >= top else "tc0")
            L.px(x, min(top, 21), "wd0")
        L.hline(bx + 8, bx + 31, 22, "wd1")
        L.hline(bx + 8, bx + 31, 23, "ink")
        # the dark shed, and a ship's stern hauled up out of it (y 24-39, wood)
        L.rect(bx + 8, 24, 24, 16, "ink")
        L.blit(stern, WOODK, bx + 11, 27)
        # the slipway (y 40-47, stone), wet where it meets the water
        for x in range(bx + 8, bx + 32):
            for y in range(40, 48):
                c = "s2" if (y % 3) else "s1"
                if x in (bx + 8, bx + 31):
                    c = "s1"
                if y >= 45:
                    c = "wt0" if y == 45 else "wt1"
                L.px(x, y, c)
    # the stone piers (the left 8 px of each bay) and the end walls
    for x0, x1 in ((0, 16), (16, 24), (48, 56), (80, 96)):
        for y in range(16, 48):
            for x in range(x0, x1):
                c = "s3"
                if x == x0:
                    c = "s5"
                elif x == x1 - 1:
                    c = "s1"
                elif (y - 16) % 6 == 5:
                    c = "s2"
                elif (x - x0) % 8 == 4 and (y - 16) % 12 > 6:
                    c = "s2"
                L.px(x, y, c)
            L.px(x0, y, "ink" if x0 in (0, 80) else "s5")
        L.hline(x0, x1 - 1, 47, "sk")
    L.vline(w - 1, 0, 47, "ink")
    L.vline(0, 0, 47, "ink")
    return s


def ship_shed_pieces():
    s = ship_sheds()
    out = [
        E.sub(s, "shed_end_w", "Ship shed: west end", 0, 0, 1, 3,
              notes="The row of ship sheds' west end: a thick ashlar end wall under the "
                    "roof's verge."),
        E.sub(s, "shed_bay", "Ship shed: a bay", 1, 0, 2, 3,
              notes="One shed of a row of ship sheds (neosoikoi), two cells wide: the "
                    "terracotta roof, the shed's gable, a stone pier, and a ship's stern "
                    "hauled up out of the dark on its slipway. The slipway's foot is at the "
                    "bottom row's lower edge: put aethos sea in the row below. Repeat bays; "
                    "all impassable."),
        E.sub(s, "shed_end_e", "Ship shed: east end", s.w - 1, 0, 1, 3,
              notes="The row's east end wall."),
    ]
    return out


# ==========================================================================
# The crane and the harbor's goods
# ==========================================================================

def crane():
    s = Struct("crane", "Harbor crane with a load of amphorae", 2, 3,
               walk=["TT", "XX", "XX"], ground="quay",
               notes="A timber harbor crane: a mast braced on a windlass platform, a boom "
                     "reaching east with its pulley, and a net of amphorae on the rope. Stand "
                     "it on the quay's edge; the top row draws over the player.")
    T, M = s.T, s.M
    # the mast (left cell), boom and pulley (row 0, top layer)
    for y in range(2, 16):
        T.px(5, y, "ink")
        T.px(6, y, "wd2")
        T.px(7, y, "wd1")
        T.px(8, y, "ink")
    T.blit(["kkkkk", "k232k", "kkkkk"], WOODK, 4, 0)
    for i in range(24):
        x, y = 8 + i, 6 - i // 4
        T.px(x, y, "ink")
        T.px(x, y + 1, "wd2")
        T.px(x, y + 2, "wd1")
        T.px(x, y + 3, "ink")
    T.blit([" kk ", "k32k", "k21k", " kk "], WOODK, 26, 4)
    # the rope from the pulley
    for y in range(8, 16):
        T.px(28, y, "rp")
    # rows 1-2 (middle layer): the mast's foot, braces and the load
    for y in range(16, 36):
        M.px(5, y, "ink")
        M.px(6, y, "wd2")
        M.px(7, y, "wd1")
        M.px(8, y, "ink")
    for i in range(10):
        M.px(9 + i // 2, 36 - i, "wd1")
        M.px(4 - i // 3, 36 - i, "wd1")
    for y in range(16, 20):
        M.px(28, y, "rp")
    # the net of amphorae hanging on the rope
    net = [
        "  kkkk  ",
        " krrrrk ",
        "kRkRRkRk",
        "kRrRRrRk",
        "kRkRRkRk",
        " kRrrRk ",
        "  kkkk  ",
    ]
    M.blit(net, WOODK, 24, 20)
    # the windlass platform
    M.rect(0, 36, 22, 10, "wd2")
    M.hline(0, 21, 36, "wd3")
    M.hline(0, 21, 45, "ink")
    M.vline(0, 36, 45, "ink")
    M.vline(21, 36, 45, "ink")
    M.rect(3, 38, 16, 5, "wd1")
    for x in range(4, 18, 3):
        M.vline(x, 38, 42, "rp")
    M.blit(["k", "1", "1", "1", "k"], WOODK, 2, 37)
    M.blit(["k", "1", "1", "1", "k"], WOODK, 19, 37)
    return s


def harbor_goods():
    s = Struct("harbor_goods", "The harbor's goods", 4, 1, walk=["XXXX"], ground="quay",
               notes="Things for the quays: (0)-(1) transport amphorae stacked in a pyramid, "
                     "(2)-(3) the hiring hall's crates of shovels and bronze helmets "
                     "(STORY.md: 'crates of shovels and helmets').")
    M = s.M
    amph = ["  kk  ", " k22k ", "k2221k", "k2211k", " k11k ", "  kk  "]
    for x in (2, 10, 18, 26):
        M.blit(amph, {"k": "ink", "2": "tc2", "1": "tc1"}, x, 9)
    for x in (6, 14, 22):
        M.blit(amph, {"k": "ink", "2": "tc2", "1": "tc1"}, x, 4)
    M.blit(amph, {"k": "ink", "2": "tc2", "1": "tc1"}, 14, 0)
    for x0 in (32, 48):
        M.blit(["kkkkkkkkkkkkk", "k33333333332k", "k32222222221k", "k32222222221k",
                "k22222222211k", "kkkkkkkkkkkkk"], WOODK, x0 + 1, 8)
    for x in (35, 38, 41):
        M.vline(x, 1, 8, "wd2")
        M.px(x, 0, "wd1")
    M.blit([" kkk ", "kGggk", "kgkgk", " k k "], WOODK, 51, 4)
    M.blit([" kkk ", "kGggk", "kgkgk", " k k "], WOODK, 56, 3)
    return s


# ==========================================================================
# The merchant ship, at sea and on the Diolkos
# ==========================================================================

def _ship_upper(M):
    """Rows 0-1 of the merchant ship (96 px long, bow to the right)."""
    # hull top: the rail and the cargo on deck (row 1, y 16-31)
    WL = 40

    def sheer(x):
        if x < 12:
            return 22 - (12 - x) // 2
        if x > 84:
            return 22 - (x - 84) // 3
        return 22
    for x in range(6, 92):
        top = sheer(x)
        for y in range(top, 32):
            c = "wd1"
            if y == top:
                c = "wd2"
            elif y == top + 1:
                c = "wd3"
            elif y == top + 5:
                c = "w0"
            elif y == top + 6:
                c = "rd"
            M.px(x, y, c)
        M.px(x, top - 1, "ink")
    M.vline(5, 16, 31, "ink")
    # the deckhouse at the stern
    M.rect(14, 15, 14, 7, "wd2")
    M.hline(14, 27, 15, "wd3")
    E.outline_rect(M, 13, 14, 16, 9, "ink")
    M.rect(18, 17, 3, 3, "ink")
    # cargo amphorae on deck
    for x in range(32, 72, 8):
        M.blit([" kk ", "kRRk", "kRRk", " kk "], WOODK, x, 17)
    # the swan-neck stern post curling up and forward (rows 0-1)
    neck = [
        "     kkk ",
        "    kGgk ",
        "    kk2k ",
        "      k2k",
        "      k2k",
        "     k21k",
        "    k21k ",
        "   k21k  ",
        "  k21k   ",
        " k21k    ",
        "k21k     ",
        "k1k      ",
    ]
    M.blit(neck, WOODK, 0, 6)
    # the bow and its painted eye
    M.blit([" kkk", "kwwbk", "kwbbk", " kkk"], WOODK, 84, 24)
    # the mast, yard and furled sail (rows 0-1)
    for y in range(0, 22):
        M.px(48, y, "ink")
        M.px(49, y, "wd2")
        M.px(50, y, "wd1")
        M.px(51, y, "ink")
    for x in range(26, 74):
        M.px(x, 3, "ink")
        M.px(x, 4, "wd2")
        M.px(x, 5, "rp" if (x // 4) % 2 else "w0")
        M.px(x, 6, "w0")
        M.px(x, 7, "rp")
        M.px(x, 8, "ink")
        if x % 8 == 2:
            M.vline(x, 5, 7, "wd1")
    M.vline(25, 3, 8, "ink")
    M.vline(74, 3, 8, "ink")
    # stays to the bow and stern
    # steering oars at the stern quarter
    for k in range(10):
        M.px(10 - k // 3, 24 + k, "wd2")
    return WL


def merchant_ship(cradle=False):
    key = "ship_cradle" if cradle else "ship"
    title = ("The Diolkos: a merchant ship on its wheeled cradle" if cradle
             else "Merchant ship with a swan-neck stern")
    notes = ("A round-bellied merchant ship (holkas), bow to the east: a swan-neck stern "
             "post, a deckhouse, amphorae lashed on deck, a furled square sail and a painted "
             "eye.")
    if cradle:
        notes += (" Here she rides the Diolkos on a wheeled timber cradle, hauled across the "
                  "Isthmus: the bottom row is the track itself, so lay diolkos runs either "
                  "side of it. Rows 0-1 are the moored ship's own tiles; they sit on aethos "
                  "grass.")
    else:
        notes += " Moored on aethos's animated sea."
    s = Struct(key, title, 6, 3, walk=["XXXXXX"] * 3, notes=notes,
               ground="grass" if cradle else "sea")
    M = s.M
    _ship_upper(M)
    if not cradle:
        # the lower hull meeting the water, and its shadow on the sea
        for x in range(6, 92):
            bot = 40 - (2 if x < 14 or x > 82 else 0) - (2 if x < 9 or x > 87 else 0)
            for y in range(32, bot):
                M.px(x, y, "wd1" if y < bot - 2 else "wd0")
            M.px(x, bot, "w0" if x % 8 not in (3, 6) else "b1")
            M.px(x, bot + 1, "b0")
            if x % 4 == 1:
                M.px(x, bot + 2, "b0")
        M.vline(5, 32, 37, "ink")
    else:
        s.set_ground("none", [(x, 2) for x in range(6)])
        diolkos_track(s.B, 0, 32, 96)
        # the full hull down to its keel
        for x in range(6, 92):
            bot = 39 - (2 if x < 14 or x > 82 else 0) - (2 if x < 9 or x > 87 else 0)
            for y in range(32, bot):
                M.px(x, y, "wd1" if y < bot - 2 else "wd0")
            M.px(x, bot, "ink")
        M.vline(5, 32, 37, "ink")
        # the cradle: timbers under the hull, on wheels in the ruts
        for x0 in (8, 40, 72):
            M.rect(x0, 38, 18, 4, "wd2")
            M.hline(x0, x0 + 17, 38, "wd3")
            E.outline_rect(M, x0 - 1, 37, 20, 6, "ink")
            for wx in (x0 + 1, x0 + 12):
                M.blit([" kkk ", "k232k", "k3k2k", "k232k", " kkk "], WOODK, wx, 42)
        # the hauling rope running forward along the track
        for x in range(88, 96):
            M.px(x, 40, "rp")
    return finish(s)


def diolkos_track(L, x0, y0, w):
    """The Diolkos: a road of big poros slabs laid across the way, alternately
    paler and darker, and two shallow ruts worn along it by the cradles' wheels."""
    for y in range(y0, y0 + 16):
        for x in range(x0, x0 + w):
            X, Y = (x - x0) % 16, y - y0
            c = "s3" if X < 8 else "s4"
            if X in (7, 15):
                c = "s2"
            elif Y == 1 and X not in (7, 15):
                c = "s4" if X < 8 else "s5"
            if Y == 0:
                c = "s2"
            elif Y == 15:
                c = "s1"
            elif Y in (4, 11):
                c = "s1"
            elif Y in (5, 12):
                c = "s2"
            L.px(x, y, c)


def diolkos():
    s = Struct("diolkos", "The Diolkos: the ship track across the Isthmus", 4, 1,
               walk=["...."], ground="none",
               notes="The paved stone track on which ships were hauled across the Isthmus, "
                     "running west to east: (0) the west end, sloping down into the Gulf "
                     "(put aethos sea west of it), (1) the track, (2) the track with a slab "
                     "worn through to the earth, (3) the east end, meeting a road. Walkable. "
                     "The merchant ship on her cradle (ship_cradle) sits on it.")
    L = s.B
    diolkos_track(L, 0, 0, 64)
    # (0): the slipway end, wet where it runs into the sea
    for y in range(0, 16):
        for x in range(0, 5):
            L.px(x, y, "wt1" if x > 1 else "wt0")
        L.px(5, y, "ol1" if y % 2 else "wt0")
    # (2): a worn slab
    L.rect(37, 6, 6, 4, "e2")
    L.hline(37, 42, 6, "e1")
    # (3): the east end, the track's kerb closing
    L.vline(63, 0, 15, "s1")
    L.vline(62, 1, 14, "s4")
    return finish(s)


def capstan():
    s = Struct("capstan", "Capstan for hauling ships", 1, 1, walk=["X"], ground="grass",
               notes="A capstan with four bars and the hauling rope wound on it, set beside "
                     "the Diolkos. On aethos grass.")
    M = s.M
    M.blit([
        "   kk kk    ",
        "kkkk2k1kkkk ",
        "k3221212213k",
        "kkkk1r2kkkk ",
        "   krrrrk   ",
        "   k2r2rk   ",
        "   krrrrk   ",
        "   k2r2rk   ",
        "   krrrrk   ",
        "  kk1111kk  ",
        "  k000000k  ",
        "   kkkkkk   ",
    ], WOODK, 2, 2)
    for x in range(10, 16):
        M.px(x, 8, "rp")
    return finish(s)


def build_port():
    out = [quay(), bollards(), warehouse_wall()] + ship_shed_pieces() + [crane(), harbor_goods()]
    return [finish(t) for t in out]


def build_diolkos():
    out = [merchant_ship(False), diolkos(), merchant_ship(True), capstan()]
    return [finish(t) for t in out]
