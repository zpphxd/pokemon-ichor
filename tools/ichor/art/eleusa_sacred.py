"""Eleusa's sanctuary and public buildings.

The sacred buildings share one kit, in honey marble with Eleusis's dark grey
stone: the roof seen from above (the house kit's gable slopes, turned 7 wide),
a pediment row, an entablature row, two column rows and a step row. The
Temple of Demeter, the Greater Propylaea and the Telesterion are all built
from it, so their columns, frieze and steps are the same tiles.

  Temple of Demeter  wheat-gold: a sheaf in the pediment, gold wheat in the
                     metopes, torch-bearer statues at either end of the porch
  Greater Propylaea  the sanctuary's gate: walk through its middle bay
  Telesterion        the hall of initiation: a great hipped roof with its
                     lantern, a blind wall, and Philon's colonnade
  Asclepeion, Agora  Eleusa's own, in the village's plaster and tile
  Kallichoron well   where Demeter sat grieving, in its ring of paving
  Plutonion          the cave mouth to the underworld, under the rock
  Sacred Way         the processional road's great slabs and wheel ruts
  Rheitoi            the kerbed salt pools, with a slab bridge
  and the procession's torch posts, a grain shrine, a pomegranate tree.

Light from the top left; objects outlined in ink.
"""
from __future__ import annotations

import numpy as np

import eleusa_house as HZ
from eleusa_lib import Layer, ground, on_other_ground, put, struct

SEC = "sanctuary"
SEC_CIVIC = "civic"
DARK = {"rf3": "rf2", "rf2": "rf1", "rf1": "rf0", "rf0": "rf0"}

# --------------------------------------------------------------------------
# Kit painters (marble group: w0 m1-m5 eg0 eg1 wh2 wh3 fl fc rf1 rf2 ink)
# --------------------------------------------------------------------------

SHAFT = ["ink", "m1", "w0", "m1", "m2", "m2", "m3", "m3", "m4", "m4", "m5", "ink"]


def porch_bg(L, ox, oy, h=16, top=False):
    """The deep shade of the porch behind the columns: warm dark marble,
    darkest under the ceiling (top=True for a cell right under the frieze)."""
    for y in range(h):
        for x in range(16):
            c = "m5"
            if top and y < 3:
                c = "eg0"
            L.px(ox + x, oy + y, c)


def column(L, ox, oy, part, bg=True):
    """A Doric column, 12 px wide, centred. part 0: capital and upper shaft;
    part 1: lower shaft standing on the stylobate."""
    if bg:
        porch_bg(L, ox, oy, top=part == 0)
    for y in range(16):
        for i, c in enumerate(SHAFT):
            L.px(ox + 2 + i, oy + y, c)
    if part == 0:
        # abacus, echinus, necking
        L.hline(ox + 0, ox + 15, oy + 0, "ink")
        L.hline(ox + 0, ox + 15, oy + 1, "m1")
        L.hline(ox + 0, ox + 15, oy + 2, "m3")
        L.hline(ox + 1, ox + 14, oy + 3, "ink")
        L.hline(ox + 1, ox + 14, oy + 4, "m1")
        L.hline(ox + 2, ox + 13, oy + 5, "m3")
        L.px(ox + 1, oy + 4, "ink")
        L.px(ox + 14, oy + 4, "ink")
        L.hline(ox + 3, ox + 12, oy + 7, "m4")
    else:
        L.hline(ox + 1, ox + 14, oy + 15, "ink")


def intercol(L, ox, oy, part):
    """The porch between two columns: shade, with the cella wall's foot."""
    porch_bg(L, ox, oy, top=part == 0)
    if part == 1:
        L.hline(ox, ox + 15, oy + 12, "eg1")
        L.hline(ox, ox + 15, oy + 13, "m5")
        L.hline(ox, ox + 15, oy + 14, "m4")
        L.hline(ox, ox + 15, oy + 15, "ink")


def bronze_door(L, ox, oy, part):
    """Tall gilt-bronze doors in the cella wall, seen between the columns."""
    porch_bg(L, ox, oy, top=part == 0)
    if part == 0:
        L.hline(ox + 1, ox + 14, oy + 2, "m2")
        L.hline(ox + 1, ox + 14, oy + 3, "m4")
        L.hline(ox + 1, ox + 14, oy + 1, "ink")
        y0 = 4
    else:
        y0 = 0
    for y in range(y0, 16):
        for x in range(2, 14):
            c = "wh2" if x < 8 else "m4"
            if x in (2, 13):
                c = "ink"
            elif x == 3:
                c = "wh3"
            elif x in (7, 8):
                c = "m5" if x == 7 else "wh2"
            L.px(ox + x, oy + y, c)
    # studs and the ring handles
    for sy in ((7, 11) if part == 0 else (3, 7, 11)):
        for sx in (4, 6, 9, 11):
            L.px(ox + sx, oy + sy, "wh3" if sx < 8 else "wh2")
    if part == 1:
        put(L, ox + 5, oy + 4, ["K.KK.K", "K.KK.K"], {"K": "m5"})
        L.hline(ox + 1, ox + 14, oy + 14, "m2")
        L.hline(ox + 1, ox + 14, oy + 15, "ink")


def entablature(L, ox, oy, side="M", metope=None):
    """Cornice, triglyph frieze and architrave. metope: 'wheat' paints a gold
    ear of wheat in each metope (Demeter's temple)."""
    for x in range(16):
        L.px(ox + x, oy + 0, "w0")
        L.px(ox + x, oy + 1, "m1")
        L.px(ox + x, oy + 2, "m3")
        L.px(ox + x, oy + 3, "ink" if x % 4 else "m5")       # mutules
        for y in range(4, 10):
            k = x % 8
            if k in (0, 1, 2):
                c = ("m3", "eg1", "m4")[k] if y > 4 else "m2"   # triglyph grooves
            else:
                c = "m2" if k < 6 else "m3"
            L.px(ox + x, oy + y, c)
        L.px(ox + x, oy + 10, "m1")
        L.px(ox + x, oy + 11, "m2")
        L.px(ox + x, oy + 12, "m2")
        L.px(ox + x, oy + 13, "m3")
        L.px(ox + x, oy + 14, "m4")
        L.px(ox + x, oy + 15, "ink")
    if metope == "wheat":
        for mx in (4, 12):
            put(L, ox + mx - 1, oy + 4, [".3.", "323", ".3.", "323", ".2."], {"3": "wh3", "2": "wh2"})
    if side == "L":
        L.vline(ox, oy, oy + 15, "ink")
        L.vline(ox + 1, oy, oy + 14, "w0")
    elif side == "R":
        L.vline(ox + 15, oy, oy + 15, "ink")
        L.vline(ox + 14, oy, oy + 14, "m4")


def steps(L, ox, oy, side="M"):
    """Three marble steps up to the stylobate."""
    rows = ["w0", "m1", "m3", "m3", "m4", "m1", "m2", "m4", "m4", "m5", "m2", "m3", "m5",
            "eg1", "eg0", "ink"]
    for y, c in enumerate(rows):
        for x in range(16):
            cc = c
            if c in ("m1", "m2") and x % 8 == 7:
                cc = "m3"
            L.px(ox + x, oy + y, cc)
    if side == "L":
        for y in range(16):
            L.px(ox, oy + y, "ink")
            L.px(ox + 1, oy + y, "m1" if y < 14 else "eg1")
    elif side == "R":
        for y in range(16):
            L.px(ox + 15, oy + y, "ink")
            L.px(ox + 14, oy + y, "m5" if y < 14 else "eg0")


def roof_above(L, ox, oy, wcells):
    """The roof from above, ridge running back from the pediment's apex: the
    house kit's gable slope cells, laid wcells wide (odd). House group."""
    W = wcells * 16
    mid = W // 2
    for y in range(16):
        for x in range(W):
            if x < mid - 1:
                c = HZ.roof(y, x)
            elif x > mid:
                c = DARK[HZ.roof(y, W - 1 - x)]
            else:
                c = "rf3" if x == mid - 1 else "rf1"     # the ridge: a lit seam
                if y % 4 == 3:
                    c = "rf0"
            L.px(ox + x, oy + y, c)
    L.hline(ox, ox + W - 1, oy, "ink")
    for y in range(16):
        L.px(ox, oy + y, "ink")
        L.px(ox + 1, oy + y, "rf3")
        L.px(ox + W - 1, oy + y, "ink")
        L.px(ox + W - 2, oy + y, "rf0")


def pediment(L, ox, oy, wcells, emblem):
    """A low pediment one row tall: roof above the raking cornice (marble
    group's two terracottas), a dark tympanum, and the emblem in gold."""
    W = wcells * 16
    mid = (W - 1) / 2
    for y in range(16):
        for x in range(W):
            d = abs(x - mid)
            edge = 2 + d * 11 / mid                       # raking cornice: low at the apex
            xs = d                                        # mirror-symmetric, so the halves share tiles
            gilt = emblem == "sheaf"      # Demeter's own temple: a gilded cornice
            if y < edge - 3:
                c = "rf2" if (y + int(xs)) % 4 else "rf1"
            elif y < edge - 2:
                c = "ink"
            elif y < edge - 1:
                c = "wh3" if gilt else "m1"
            elif y < edge:
                c = "wh2" if gilt else "m3"
            elif y >= 13:
                c = ("m1", "m3", "ink")[y - 13]
            else:
                c = "eg1"
            L.px(ox + x, oy + y, c)
    for y in range(16):
        L.px(ox, oy + y, "ink")
        L.px(ox + W - 1, oy + y, "ink")
    cx = ox + W // 2
    if emblem == "sheaf":
        # gilt acroteria: a palmette at each end of the cornice and the apex
        for ax, flip in ((2, False), (W - 9, True)):
            put(L, ox + ax, oy + 6, [
                "..3....",
                ".323.3.",
                "3.3232.",
                ".22322.",
                "..2222.",
            ], {"3": "wh3", "2": "wh2"}, hflip=flip)
        put(L, cx - 3, oy + 0, ["3.3.3", ".323.", "..2.."], {"3": "wh3", "2": "wh2"})
        # Demeter's sheaf, two torches and two poppies, in gilt relief
        put(L, cx - 5, oy + 3, [
            ".3.3.3.3.",
            "333232333",
            ".3323233.",
            "..32323..",
            "...222...",
            "...333...",
            "..32223..",
            ".3.2.2.3.",
        ][0:8], {"3": "wh3", "2": "wh2"})
        L.hline(cx - 2, cx + 2, oy + 8, "m4")
        for tx in (-16, 14):
            put(L, cx + tx, oy + 6, [".f.", "fcf", ".3.", ".2.", ".2.", ".2."],
                {"f": "fl", "c": "fc", "3": "wh3", "2": "wh2"})
        for px_ in (-26, 25):
            put(L, cx + px_, oy + 9, [".f.", "fff", ".2."], {"f": "fl", "2": "wh2"})
    elif emblem == "torches":
        # the Propylaea: Demeter's two crossed torches in a wheat wreath
        for i in range(8):
            L.px(cx - 4 + i, oy + 11 - i, "wh2")
            L.px(cx + 3 - i, oy + 11 - i, "wh3")
        put(L, cx - 6, oy + 2, ["fcf"], {"f": "fl", "c": "fc"})
        put(L, cx + 4, oy + 2, ["fcf"], {"f": "fl", "c": "fc"})
        L.px(cx - 5, oy + 1, "fl")
        L.px(cx + 5, oy + 1, "fl")
        for k in range(5):
            L.px(cx - 11 + k, oy + 9 + (k % 2), "wh3")
            L.px(cx + 10 - k, oy + 9 + (k % 2), "wh2")


def torchbearer(L, ox, oy):
    """A marble torch-bearer on a pedestal, torch raised, against the anta.
    Two rows: 0 is the figure's head and the torch, 1 the robe and pedestal."""
    for y in range(32):
        for x in range(16):
            c = "m2" if x < 13 else "m4"
            if x == 0:
                c = "ink"
            elif x == 1:
                c = "m1"
            elif x == 15:
                c = "ink"
            if y % 8 == 7 and 1 < x < 15:
                c = "m3"
            L.px(ox + x, oy + y, c)
    put(L, ox + 2, oy + 0, [
        "..fcf.......",
        "..fcf.......",
        ".ffcff......",
        "..f3f.......",
        "..K2K.......",
        "..K2K.KKK...",
        "..K2KK111K..",
        "..K2K11111K.",
        "..K2KK1113K.",
        "...K11K13K..",
        "....K1113K..",
        "...K111133K.",
        "..K1111133K.",
        "..K11W1133K.",
        "..K11W1133K.",
        "..K1W11333K.",
        "..K1W11333K.",
        "..K11W1333K.",
        "..K11W1333K.",
        "..K1W11333K.",
        ".K11W113333K",
        ".K1W1113333K",
        ".K11W113333K",
        ".KKKKKKKKKKK",
        "KwwwwwwwwwwK",
        "K1111111133K",
        "K1311111333K",
        "K1111111333K",
        "K1111111333K",
        "K3333333334K",
        "K4444444444K",
        "KKKKKKKKKKKK",
    ], {"K": "ink", "1": "w0", "3": "m3", "4": "m4", "W": "m2", "w": "m1", "f": "fl", "c": "fc",
        "2": "wh2"})


# --------------------------------------------------------------------------
# The buildings
# --------------------------------------------------------------------------


def temple_demeter():
    s = struct("temple_demeter", "Temple of Demeter, exterior", 7, 6, SEC,
               walk=["XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXDXXX", "......."],
               notes="Wheat-gold Doric: a gilt sheaf between two torches and two poppies in "
                     "the pediment, gold ears of wheat in the metopes, gilt-bronze doors, and "
                     "a marble torch-bearer at either end of the porch. Door: row 4, middle "
                     "column (MB_NON_ANIMATED_DOOR). The step row is walkable.")
    L = s.B
    roof_above(L, 0, 0, 7)
    pediment(L, 0, 16, 7, "sheaf")
    for i in range(7):
        entablature(L, i * 16, 32, "L" if i == 0 else ("R" if i == 6 else "M"), metope="wheat")
    for part in (0, 1):
        y = 48 + part * 16
        for i, kind in enumerate(("stat", "col", "inter", "door", "inter", "col", "stat")):
            if kind == "col":
                column(L, i * 16, y, part)
            elif kind == "inter":
                intercol(L, i * 16, y, part)
            elif kind == "door":
                bronze_door(L, i * 16, y, part)
    torchbearer(L, 0, 48)
    tb = Layer(16, 32)
    torchbearer(tb, 0, 0)
    L.a[48:80, 96:112] = tb.a[:, ::-1]
    for i in range(7):
        steps(L, i * 16, 80, "L" if i == 0 else ("R" if i == 6 else "M"))
    return s


def propylaea():
    s = struct("propylaea", "The Greater Propylaea: the sanctuary's gate", 7, 6, SEC,
               walk=["XXXTXXX", "XXXTXXX", "XXXTXXX", "XXXTXXX", "XXXTXXX", "......."],
               notes="The gate of the Mysteries. A Doric front with Demeter's crossed torches "
                     "in the pediment. Walk through the middle bay: its column (x = 3) is "
                     "passable all the way up and the gate is drawn over the player, so put "
                     "the sanctuary's ground directly north of it. The step row is walkable.")
    full = Layer(112, 96)
    roof_above(full, 0, 0, 7)
    pediment(full, 0, 16, 7, "torches")
    for i in range(7):
        entablature(full, i * 16, 32, "L" if i == 0 else ("R" if i == 6 else "M"), metope="wheat")
    for part in (0, 1):
        y = 48 + part * 16
        for i in range(7):
            if i in (0, 2, 4, 6):
                column(full, i * 16, y, part)
            elif i == 3:
                pass
            else:
                intercol(full, i * 16, y, part)
    for i in range(7):
        steps(full, i * 16, 80, "L" if i == 0 else ("R" if i == 6 else "M"))
    s.B.a[:] = full.a
    # the passage: the gate's dark inside under everything; the facade above
    # the passage is drawn over the player, who walks through into the shade
    for y in range(0, 80, 16):
        porch_bg(s.B, 48, y, top=y == 48)
    # the passage's floor: slabs running back into the shade
    for y in range(72, 80):
        for x in range(48, 64):
            c = "m3" if y > 76 else "m4"
            if (y in (73, 77)) or (x - 48) % 8 == (3 if y < 77 else 6):
                c = "eg1"
            s.B.px(x, y, c)
    s.T.a[0:48, 48:64] = full.a[0:48, 48:64]
    return s


def telesterion():
    s = struct("telesterion", "The Telesterion: the hall of initiation, exterior", 9, 7, SEC,
               walk=["XXXXXXXXX"] * 5 + ["XXXXDXXXX", "........."],
               notes="The great square hall where the Mysteries were shown, and where the "
                     "Titans rob the sanctum. A hipped roof with the lantern (opaion) that "
                     "lets the smoke of the torches out, a blind wall of grey Eleusinian stone "
                     "(\"Who builds a temple with no windows?\"), and Philon's Doric colonnade. "
                     "Door: row 5, middle column. The step row is walkable.")
    L = s.B
    for i in range(9):
        side = "L" if i == 0 else ("R" if i == 8 else "M")
        HZ.roof_cell(L, i * 16, 0, "R0", side)
        HZ.roof_cell(L, i * 16, 16, "R1", side)
    lantern(L, 48, 0)
    for i in range(9):
        ashlar(L, i * 16, 32, "L" if i == 0 else ("R" if i == 8 else "M"))
        entablature(L, i * 16, 48, "L" if i == 0 else ("R" if i == 8 else "M"), metope="wheat")
    for part in (0, 1):
        y = 64 + part * 16
        for i in range(9):
            # Philon's prostyle colonnade: columns to both corners, a wide
            # middle bay before the doors
            if i == 4:
                bronze_door(L, i * 16, y, part)
            elif i % 2 == 0:
                column(L, i * 16, y, part)
            else:
                intercol(L, i * 16, y, part)
    for i in range(9):
        steps(L, i * 16, 96, "L" if i == 0 else ("R" if i == 8 else "M"))
    return s


def lantern(L, ox, oy):
    """The opaion's lantern astride the ridge: a raised box with louvres under
    its own small roof, 3 cells wide and one row tall (house group)."""
    for y in range(1, 16):
        for x in range(4, 44):
            if y < 6:
                c = HZ.roof(x, y)
                if x > 24:
                    c = DARK[c]
            elif y == 6:
                c = "rf3"
            elif y == 7:
                c = "ink"
            elif y < 14:
                louvre = (x - 4) % 6 in (2, 3)
                c = "wd0" if louvre else ("pl2" if x < 24 else "pl1")
                if louvre and y % 2:
                    c = "wdx"
            elif y == 14:
                c = "pl0"
            else:
                c = "rf0"
            L.px(ox + x, oy + y, c)
    for y in range(1, 16):
        L.px(ox + 3, oy + y, "ink")
        L.px(ox + 44, oy + y, "ink")
    L.hline(ox + 3, ox + 44, oy + 0, "ink")


def ashlar(L, ox, oy, side="M"):
    """The Telesterion's blind wall: big courses of grey Eleusinian stone with
    a honey-marble string course."""
    for y in range(16):
        for x in range(16):
            course = y // 5
            joint = y % 5 == 4 or (x + course * 6) % 12 == 0
            c = "eg0" if joint else ("eg1" if (x + y) % 13 else "m4")
            if y == 0:
                c = "m2"
            elif y == 1:
                c = "m4"
            L.px(ox + x, oy + y, c)
    if side == "L":
        L.vline(ox, oy, oy + 15, "ink")
        L.vline(ox + 1, oy, oy + 15, "m3")
    elif side == "R":
        L.vline(ox + 15, oy, oy + 15, "ink")


# --------------------------------------------------------------------------
# Village civic buildings
# --------------------------------------------------------------------------


def asclepeion():
    s = struct("asclepeion", "Eleusa's Asclepeion", 5, 4, SEC_CIVIC,
               walk=["XXXXX", "XXXXX", "XXXXX", "XXDXX"],
               notes="The village healing house: plaster and tile like the farms, a porch of "
                     "two marble columns, the rod of Asclepius painted on a plaque, and pots "
                     "of healing herbs. Door: bottom row, middle (MB_NON_ANIMATED_DOOR).")
    L = s.B
    for i in range(5):
        side = "L" if i == 0 else ("R" if i == 4 else "M")
        HZ.roof_cell(L, i * 16, 0, "R0", side)
        HZ.roof_cell(L, i * 16, 16, "R1", side)
    for part in (0, 1):
        y = 32 + part * 16
        HZ.wall_cell(L, 0, y, "W0" if part == 0 else "W1", "L")
        HZ.wall_cell(L, 64, y, "W0" if part == 0 else "W1", "R")
        column(L, 16, y, part)
        column(L, 48, y, part)
        plank_in_shade(L, 32, y, part)
    # the plaque with the rod of Asclepius, on the west pier
    put(L, 3, 35, [
        "KKKKKKKKKK",
        "K33333333K",
        "K3333g333K",
        "K333gWg33K",
        "K3333Wg33K",
        "K333gW333K",
        "K3333Wg33K",
        "K333gW333K",
        "K3333W333K",
        "K33333333K",
        "KKKKKKKKKK",
    ], {"K": "ink", "3": "pl3", "W": "wdx", "g": "ox"})
    # herb pots against the east pier
    put(L, 67, 52, [
        ".ggg..ggg.",
        "gGgGggGgGg",
        ".gGg..gGg.",
        "KrrK..KrrK",
        "KrrK..KrrK",
        ".KK....KK.",
    ], {"g": "sg1", "G": "pl3", "K": "ink", "r": "rf2"})
    return s


def plank_in_shade(L, ox, oy, part):
    """The Asclepeion's door: a plank door set in the porch's shade."""
    porch_bg(L, ox, oy)
    if part == 0:
        L.hline(ox + 1, ox + 14, oy + 6, "m2")
        L.hline(ox + 1, ox + 14, oy + 7, "m4")
        y0 = 8
    else:
        y0 = 0
    for y in range(y0, 16):
        for x in range(3, 13):
            c = ("m5", "m4", "m4")[(x - 3) % 3]
            if x in (3, 12):
                c = "ink"
            L.px(ox + x, oy + y, c)
    if part == 1:
        L.px(ox + 10, oy + 6, "wh3")
        L.hline(ox + 1, ox + 14, oy + 14, "m2")
        L.hline(ox + 1, ox + 14, oy + 15, "ink")


def agora():
    s = struct("agora", "Eleusa's Agora: the grain market", 5, 4, SEC_CIVIC,
               walk=["XXXXX", "XXXXX", "XXXXX", "XXDXX"],
               notes="A thatched market stoa on timber posts: sacks of grain and baskets of "
                     "figs and pomegranates on the counter, a sign with a gilt ear of wheat. "
                     "Door: bottom row, middle (MB_NON_ANIMATED_DOOR).")
    L = s.B
    for i in range(5):
        side = "L" if i == 0 else ("R" if i == 4 else "M")
        HZ.thatch_cell(L, i * 16, 0, "R0", side)
        HZ.thatch_cell(L, i * 16, 16, "R1", side)
    porch = Layer(48, 32)
    HZ.porch(porch)
    # W0 row: post, beam, beam (sign), beam, post (mirrored)
    def cell(src_x, src_y, dst_x, dst_y, flip=False):
        a = porch.a[src_y:src_y + 16, src_x:src_x + 16]
        L.a[dst_y:dst_y + 16, dst_x:dst_x + 16] = a[:, ::-1] if flip else a
    cell(0, 0, 0, 32)
    cell(16, 0, 16, 32)
    cell(16, 0, 32, 32)
    cell(16, 0, 48, 32)
    cell(0, 0, 64, 32, flip=True)
    cell(0, 16, 0, 48)
    cell(32, 16, 32, 48)
    cell(0, 16, 64, 48, flip=True)
    counter(L, 16, 48, "sacks")
    counter(L, 48, 48, "fruit")
    # the sign: a board with a gilt ear of wheat, hung from the beam
    put(L, 33, 36, [
        "..K.......K..",
        "..K.......K..",
        "KKKKKKKKKKKKK",
        "Kwwwww3wwwwwK",
        "Kwwww323wwwwK",
        "Kwwwww3wwwwwK",
        "Kwwww323wwwwK",
        "Kwwwww2wwwwwK",
        "KKKKKKKKKKKKK",
    ], {"K": "ink", "w": "wdx", "3": "pl3", "2": "pl2"})
    return s


def counter(L, ox, oy, goods):
    """A market counter in the stoa's shade with goods on it (clay group on
    the front, house group behind)."""
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, HZ.plaster(x, y, shade=1))
    for x in range(16):
        L.px(ox + x, oy + 8, "ink")
        for y in range(9, 15):
            L.px(ox + x, oy + y, "wdx" if (x + y) % 4 else "wd0")
        L.px(ox + x, oy + 9, "wdy")
        L.px(ox + x, oy + 15, "ink")
    if goods == "sacks":
        for sx in (0, 8):
            put(L, ox + sx, oy + 0, [
                "..KK....",
                ".KppK...",
                "Kp33pK..",
                "Kp3333K.",
                "Kp3333pK",
                "Kpp333pK",
                ".KpppppK",
                "..KKKKK.",
            ], {"K": "ink", "p": "pl1", "3": "pl3"})
        put(L, ox + 3, oy + 2, ["wwy"], {"w": "pl3", "y": "rf3"})
    else:
        for sx, fruit in ((1, "ox"), (9, "wd0")):
            put(L, ox + sx, oy + 1, [
                ".rKrKr.",
                "KrrKrrK",
                "KyyyyyK",
                "KyKyKyK",
                ".KyyyK.",
                "..KKK..",
                ".......",
            ], {"K": "ink", "r": fruit, "y": "wdy"})


# --------------------------------------------------------------------------
# The precinct's smaller monuments
# --------------------------------------------------------------------------


def kallichoron():
    """The Kallichoron well in its ring of paving, 3 x 3. Drawn as one quarter
    of the paving mirrored four ways; the curb in the middle."""
    s = struct("kallichoron", "The Kallichoron well, where Demeter sat grieving", 3, 3, SEC,
               walk=["...", ".X.", "..."],
               notes="The Maiden's Well of the Hymn to Demeter. A round curb of grey stone in "
                     "a ring of radiating slabs, walkable all round. Put the theoxenia's old "
                     "woman on the seat stone (`seat_stone`) beside it.")
    Q = Layer(24, 24)
    for y in range(24):
        for x in range(24):
            dx, dy = 23.5 - x, 23.5 - y
            r = (dx * dx + dy * dy) ** 0.5
            ang = (np.degrees(np.arctan2(dy, dx))) % 90
            if r > 24:
                c = "p2" if (x * 3 + y * 5) % 7 else "p1"
                if x % 8 == 0 or y % 8 == 0:
                    c = "l1"
            elif r > 22.6:
                c = "l0"
            else:
                ring = int(r // 4.5)
                seg = int(ang // (15 if ring >= 3 else 30))
                c = "p3" if (ring + seg) % 2 else "p2"
                if r % 4.5 < 0.8 or ang % (15 if ring >= 3 else 30) < 1.6:
                    c = "l1"
            Q.px(x, y, c)
    full = np.zeros((48, 48, 4), np.uint8)
    full[:24, :24] = Q.a
    full[:24, 24:] = Q.a[:, ::-1]
    full[24:, :24] = Q.a[::-1, :]
    full[24:, 24:] = Q.a[::-1, ::-1]
    s.B.a[:] = full
    # the curb: a thick ring of grey stone, lit top left, its far inner wall
    # in shadow, and deep water with one glint
    M = s.M
    for y in range(16, 32):
        for x in range(16, 32):
            dx, dy = x - 23.5, y - 23.5
            d = (dx * dx + dy * dy) ** 0.5
            if d <= 3.6:
                c = "cv" if not (dx < -0.5 and -2.5 < dy < -0.5) else "b1"
                M.px(x, y, c)
            elif d <= 4.6:
                M.px(x, y, "l0" if dy < 1 else "l1")          # the inner wall
            elif d <= 7.2:
                u = dx + dy
                c = "p3" if u < -4 else ("p2" if u < 3 else ("l1" if u < 7 else "l0"))
                M.px(x, y, c)
            elif d <= 8.2:
                M.px(x, y, "ink")
    return s


def seat_stone():
    s = struct("seat_stone", "The Mirthless Rock: a seat stone", 1, 1, SEC, walk=["X"],
               on="grass",
               notes="Agelastos Petra, where Demeter sat without laughing. On grass, beside "
                     "the well or the Plutonion.")
    put(s.M, 1, 4, [
        "....KKKKKK....",
        "..KK333322KK..",
        ".K3333332222K.",
        "K333322222211K",
        "K332222221111K",
        "K222222111110K",
        ".K2211111100K.",
        "..KK000000KK..",
        "....KKKKKK....",
    ], {"K": "ink", "3": "p3", "2": "p2", "1": "l1", "0": "l0"})
    for x in range(4, 14, 2):
        s.M.px(x, 13, "gd")
    return s


def _mass(layer, poly, lit_rows=3, seed=0):
    """One mass of the crag: a polygon of limestone, its top lit, its front
    banded with strata and split by cracks, its east edge in shadow."""
    from PIL import Image as _I, ImageDraw as _D
    m = _I.new("1", (layer.w, layer.h), 0)
    _D.Draw(m).polygon(poly, fill=1)
    mask = np.array(m, bool)
    top = np.full(layer.w, layer.h)
    right = np.full(layer.h, -1)
    for y, x in zip(*np.nonzero(mask)):
        top[x] = min(top[x], y)
        right[y] = max(right[y], x)
    for y, x in zip(*np.nonzero(mask)):
        d = y - top[x]
        if d < lit_rows:
            c = "p3" if d == 0 or (x + seed) % 5 else "p2"
        else:
            band = (y + seed) % 8
            c = "p2" if band < 3 else ("p1" if band < 7 else "l1")
            if band == 7 and (x % 16) in (3, 11):
                c = "l0"
            if (x % 16) == 6 and d > 4 and (y % 16) in (4, 5, 6, 7):
                c = "l0"                                  # a crack
        if right[y] - x < 2:
            c = "l0" if right[y] - x == 0 else "l1"
        layer.px(x, y, c)
    return mask


def plutonion():
    s = struct("plutonion", "The Plutonion: the cave mouth to the underworld", 4, 3, SEC,
               walk=["XXXX", "XXXX", "XDDX"],
               notes="A crag of the sanctuary's rock, split by a black cave mouth. Hades's "
                     "shrine stands just inside, two small columns barely lit. The mouth is "
                     "a two-cell door (MB_NON_ANIMATED_DOOR): put a warp on both. The crag's "
                     "top row stands on borrowed grass.")
    W, H = 64, 48
    layer = Layer(W, H)
    # three masses: the west shoulder, the east shoulder, and the brow over the
    # cave; drawn back to front so the nearer ones overlap
    masks = [
        _mass(layer, [(20, 6), (30, 1), (41, 2), (47, 7), (45, 22), (20, 22)], seed=2),
        _mass(layer, [(0, 47), (0, 17), (5, 10), (13, 7), (21, 11), (24, 20), (17, 47)], seed=0),
        _mass(layer, [(40, 13), (50, 6), (58, 9), (63, 15), (63, 47), (46, 47), (42, 30)], seed=0),
    ]
    union = masks[0] | masks[1] | masks[2]
    # grass and a shrub on the ledges
    for x in range(W):
        ys = np.nonzero(union[:, x])[0]
        if len(ys):
            y = ys[0]
            if x % 4 in (0, 1) and y > 2:
                layer.px(x, y - 1, "g1" if x % 2 else "g2")
    put(layer, 6, 7, [".gg.", "gGGg", ".gg."], {"g": "gd", "G": "g1"})
    put(layer, 52, 4, [".gg.", "gGGg", ".gg."], {"g": "gd", "G": "g1"})
    # the cave mouth: a black arch, its rim in shadow, the shrine glimpsed inside
    for y in range(16, 48):
        for x in range(14, 50):
            d = ((x - 31.5) / 16.5) ** 2 + ((y - 48) / 28) ** 2
            if d <= 1:
                layer.px(x, y, "cv")
            elif d <= 1.16:
                layer.px(x, y, "l0")
    put(layer, 24, 30, [
        "..KKKKKKKKKKKK..",
        "KKl1111111111lKK",
        "KllllllllllllllK",
        ".K1K........K1K.",
        ".K1K........K1K.",
        ".K1K...bb...K1K.",
        ".K1K..b..b..K1K.",
        ".K1K........K1K.",
        ".KlK........KlK.",
    ], {"K": "ink", "l": "l1", "1": "l0", "b": "b1"})
    for x in range(17, 47):
        layer.px(x, 46, "l1" if x % 6 else "l0")
        layer.px(x, 47, "ink")
    # outline the skyline only (the masses' sides run on as rock)
    sil = np.zeros((H, W), bool)
    for x in range(W):
        ys = np.nonzero(layer.a[:, x, 3] > 0)[0]
        if len(ys):
            sil[ys[0], x] = True
    for y, x in zip(*np.nonzero(sil)):
        if layer.get(x, y) not in ("g1", "g2"):
            layer.px(x, y, "ink")
    ground(s, "grass", [(i, 0) for i in range(4)])
    s.M.a[0:16] = layer.a[0:16]
    s.B.a[16:48] = layer.a[16:48]
    for y in range(16, 48):
        for x in range(W):
            if s.B.a[y, x, 3] == 0:
                s.B.px(x, y, "g2")
    return s


def sacred_way():
    """The Sacred Way's slabs: big polygonal flags with wheel ruts, kerbed
    where they meet grass."""
    keys = ["NW", "N", "NE", "W", "C", "E", "SW", "S", "SE", "C_ruts"]
    s = struct("sacred_way", "The Sacred Way: processional paving", 5, 2, SEC,
               walk=["....."] * 2,
               names={k: (i % 5, i // 5) for i, k in enumerate(keys)},
               notes="Big limestone slabs, kerbed where they meet grass. A 3 x 3 patch: "
                     "NW N NE / W C E / SW S SE. `C_ruts` carries the carts' wheel ruts "
                     "east-west down the middle of a run.")
    def slab(x, y):
        xx, yy = x % 16, y % 16
        # an irregular lattice of slabs, 16 px periodic
        rows = [0, 6, 11]
        r = max(i for i, v in enumerate(rows) if yy >= v)
        offs = [(0, 7), (4, 11), (2, 9)][r]
        joint = yy in rows or xx in offs
        if joint:
            return "p1" if (xx + yy) % 3 else "l1"
        lit = yy in [v + 1 for v in rows] or xx in [o + 1 for o in offs]
        return "p3" if lit else ("p2" if (xx * 3 + yy) % 9 else "p1")

    for i, k in enumerate(keys):
        ox, oy = (i % 5) * 16, (i // 5) * 16
        for y in range(16):
            for x in range(16):
                s.B.px(ox + x, oy + y, slab(x, y))
        if k == "C_ruts":
            for x in range(16):
                for ry in (4, 11):
                    s.B.px(ox + x, oy + ry, "l0")
                    s.B.px(ox + x, oy + ry + 1, "l1")
        # kerbs on the grass sides
        n, so = k in ("N", "NW", "NE"), k in ("S", "SW", "SE")
        w, e = k in ("NW", "W", "SW"), k in ("NE", "E", "SE")
        for y in range(16):
            for x in range(16):
                out = (n and y < 3) or (so and y > 12) or (w and x < 3) or (e and x > 12)
                if out:
                    gx, gy = ox + x, oy + y
                    from eleusa_lib import aethos
                    rgb = aethos(0x001)[y, x]
                    s.B.rgb(gx, gy, rgb)
                kerb = ((n and y == 3) or (so and y == 12) or (w and x == 3) or (e and x == 12))
                if kerb and not ((n and y < 3) or (so and y > 12) or (w and x < 3) or (e and x > 12)):
                    s.B.px(ox + x, oy + y, "w0" if (n and y == 3) or (w and x == 3) else "l0")
                if (so and y == 13) or (e and x == 13):
                    if not ((n and y < 3) or (w and x < 3)):
                        s.B.px(ox + x, oy + y, "gd")
    return s


def rheitoi():
    """The Rheitoi's stone kerbs round a pool of borrowed, animated sea."""
    keys = ["NW", "N", "NE", "W", "E", "SW", "S", "SE", "bridge"]
    s = struct("rheitoi", "The Rheitoi: kerbed salt pools and the bridge", 9, 1, SEC,
               walk=["XXXXXXXX."], names={k: (i, 0) for i, k in enumerate(keys)}, on="sea",
               notes="Kerbs for a rectangular pool: put aethos's sea (0x170) in the middle, "
                     "so the water animates. Each kerb cell is borrowed sea under a stone "
                     "edge and its grass. `bridge` is a slab bridge across the pool (walkable; "
                     "run it north-south and set its two ends on the kerb rows).")
    M = s.M
    # Kerbs are drawn mirror-symmetric (N/S, W/E, the four corners are flips of
    # one another), so Porytiles stores each shape once. The grass strip on the
    # land side is plain meadow green.
    profile = ["g2", "g2", "g2", "g2", "g1", "ink", "p3", "p2", "p2", "l1", "l0"]

    def depth(k, x, y):
        """How far into the cell from its land side(s): the min over sides."""
        ds = []
        if "N" in k:
            ds.append(y)
        if "S" in k:
            ds.append(15 - y)
        if "W" in k:
            ds.append(x)
        if "E" in k:
            ds.append(15 - x)
        return min(ds)
    for i, k in enumerate(keys):
        ox = i * 16
        if k == "bridge":
            for y in range(16):
                for x in range(1, 15):
                    c = "p2" if (y % 8) not in (0, 7) else "l1"
                    if x in (2, 13):
                        c = "p3" if y % 4 else "l1"
                    if x in (1, 14):
                        c = "ink"
                    M.px(ox + x, y, c)
            continue
        for y in range(16):
            for x in range(16):
                d = depth(k, x, y)
                if d < len(profile):
                    M.px(ox + x, y, profile[d])
    return s


def torch_post():
    s = struct("torch_post", "A procession torch on its bronze stand", 3, 1, SEC,
               walk=["TTX"], names={"top_lit": (0, 0), "top_cold": (1, 0), "foot": (2, 0)},
               on="grass",
               notes="Stand `foot` on the ground and put `top_lit` (or `top_cold`) in the cell "
                     "above it: the torch head draws over the player. Line the Sacred Way "
                     "with them for the night of the Mysteries. Each lit metatile is its cold "
                     "one - 1: swap top_cold for top_lit to light one "
                     "(METATILE_Eleusa_TorchPost_Lit / _Cold).")
    T, M = s.T, s.M
    for ox, lit in ((0, True), (16, False)):
        put(T, ox + 4, 4, [
            "..fcf...",
            ".fc3cf..",
            ".fcccf..",
            "..fff...",
        ] if lit else [
            "........",
            "........",
            "...KK...",
            "..KeeK..",
        ], {"f": "fl", "c": "fc", "3": "wh3", "K": "ink", "e": "eg1"})
        put(T, ox + 4, 8, [
            ".KwwwK..",
            ".K2w2K..",
            "..K2K...",
            "..K2K...",
            "..K2K...",
            "..K2K...",
            "..K2K...",
            "..K2K...",
        ], {"K": "ink", "w": "wh3", "2": "wh2"})
    put(M, 36, 0, [
        "..K2K...",
        "..K2K...",
        "..K2K...",
        "..K2K...",
        "..K2K...",
        "..K2K...",
        ".K222K..",
        ".K2m2K..",
        "KK2m2KK.",
        "Kmmmmm4K",
        "K11111mK",
        "K1mmmm4K",
        "KKKKKKKK",
    ], {"K": "ink", "2": "wh2", "m": "m3", "1": "m1", "4": "m4"})
    for x in range(40, 47, 2):
        M.px(x, 14, "m4")
    return s


def grain_shrine():
    s = struct("grain_shrine", "Demeter's field shrine", 1, 2, SEC, walk=["T", "X"], on="grass",
               notes="A little stone altar heaped with a sheaf, barley cakes and poppies: "
                     "a place for the rites' offerings (SYSTEMS.md: grain shrines in fields "
                     "for Demeter). The sheaf's top draws over the player.")
    put(s.T, 3, 7, [
        "..4.4.4...",
        ".4343434..",
        ".3333233..",
        "..32323...",
        "...222....",
        "...333....",
        "..32223...",
        "..3.2.3...",
        "..........",
    ], {"4": "wh3", "3": "wh3", "2": "wh2"})
    put(s.M, 1, 16, [
        "..ff........",
        ".fffK.KKKK..",
        "KKKKKKK33KKK",
        "K1111111111K",
        "Km1m1m1m1m4K",
        "K1111111114K",
        "K1mmmmmmmm4K",
        "K1m3333334mK",
        "K1m3333334mK",
        "K1mmmmmmmm4K",
        "K4444444444K",
        "KKKKKKKKKKKK",
    ], {"K": "ink", "1": "m1", "m": "m3", "4": "m4", "3": "m2", "f": "fl"})
    return s


def pomegranate():
    s = struct("pomegranate", "Pomegranate tree", 2, 2, SEC, walk=["XX", "XX"], on="grass",
               notes="Persephone's tree: glossy leaves, scarlet flowers and fruit. Its six "
                     "seeds kept her below for part of every year.")
    M = s.M
    import agros_flora as AF
    # trunk: twisted, grey-brown
    put(M, 12, 18, [
        "..K2K.K2K.",
        "...K22K2K.",
        "....K222K.",
        "....K221K.",
        "...K2221K.",
        "..K221111K",
        "..KKKKKKKK",
    ], {"K": "ink", "2": "k2", "1": "k1"})
    clusters = [(9, 11, 8, 7), (22, 10, 8, 7), (16, 6, 9, 6), (12, 17, 7, 4), (21, 17, 7, 4)]
    AF.foliage(M, clusters, ["lf0", "lf1", "lf2", "g3"], "t0", speck="g3")
    for fx, fy in ((7, 9), (19, 5), (24, 12), (13, 15), (27, 8)):
        put(M, fx, fy, [".r.", "rRr", ".r."] if (fx + fy) % 2 else ["rr", "Rr"],
            {"r": "pp1", "R": "pp2"})
    for fx, fy in ((11, 4), (22, 15)):
        M.px(fx, fy, "pp0")
    for x in range(8, 28):
        if x % 2:
            M.px(x, 30, "gd")
            M.px(x + 1, 31, "gd")
    return s


def build():
    tp, gs = torch_post(), grain_shrine()
    return [temple_demeter(), propylaea(), telesterion(), kallichoron(), seat_stone(),
            plutonion(), sacred_way(), rheitoi(), tp, gs, pomegranate(),
            on_other_ground(tp, "torch_post_path", "path",
                            title="A procession torch, on paving"),
            on_other_ground(gs, "grain_shrine_path", "path",
                            title="Demeter's field shrine, on paving")]


def build_civic():
    return [asclepeion(), agora()]
