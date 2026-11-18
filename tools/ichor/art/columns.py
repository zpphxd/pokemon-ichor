"""Ichor's column kit: the three Greek orders, drawn for 16x16 metatiles.

Every builder that needs a column paints it with this module, so a Doric
column in Astyra, Kaldera and on Olympus is the same column. STYLE.md's
"Architecture: Gen 3 craft and Greek forms" section is the rulebook; this
file is its implementation. Run it to draw the reference sheet:

    /usr/bin/python3 tools/ichor/art/columns.py      # design/art/columns_kit.png

Usage (the API is stable; other builders import it):

    sys.path.insert(0, "tools/ichor/art")
    import columns as CK
    import kythera_lib as K                      # Layer, struct, composite, validate
    # a facade: paint columns into your own canvas, then cut it into cells
    L = K.Layer(13 * 16, 7 * 16)
    for k in range(6):                           # pitch 32 = a 1-tile intercolumniation
        CK.paint_column(L, 24 + 32 * k, top=52, bottom=99, order="doric", variant="poly")
    CK.paint_architrave(L, 2, 205, y=44, rows=8)
    CK.paint_stylobate(L, 4, 203, y=100, rows=4, steps=3)
    # a colossal order: the same call with a taller span (3-4 metatiles of shaft)
    CK.paint_column(L, 40, top=0, bottom=95, order="ionic", variant="snow")
    # ready-made pieces for a map (structures on borrowed aethos ground)
    col = CK.free_column("corinthian", "marble", height=4, on="path")   # heights 2-6
    fallen = CK.ruins("moss", on="grass")
    groups = {g: CK.GROUPS[g] for g in ("marble", "bronze", "ruin", "snow")}  # add yours

The kit, in three layers of use:

1. Painters, for buildings that draw their own facade (a stoa, a temple):
       paint_column(L, cx, top, bottom, order, variant)
   paints one column into any agros/kythera Layer, its axis between pixels
   cx-1 and cx, from the abacus's top row `top` to the base's last row
   `bottom` (inclusive). Columns may sit at any pixel pitch; a pitch of 16
   (one column per metatile) or 32 (one metatile between columns, the
   standard 1-tile intercolumniation) costs the fewest tiles. Use
   paint_stylobate() and paint_architrave() for the parts above and below.
2. Ready structures, for maps that place columns as objects in the open:
       free_column(order, variant, height, on="path")
   is a 1 x height structure (2-4) on borrowed aethos ground: the capital
   and shaft on the top layer (the player walks behind them, walk code T),
   the base on the middle layer (solid, X), with its cast shadow falling
   down and to the right onto the floor. colonnade_shadow() adds the long
   shadow cell to the right of a base.
3. Ruins: ruins(variant, on) is a structure of fallen pieces (a broken
   shaft, a short stub, toppled drums, a fallen capital of each order, a
   line of drums) in the same proportions as the standing columns.

Orders (proportions in pixels, inside one 16 px slot):
    doric       shaft 10 wide, 20 flutes drawn as 4 light/dark pairs, no base,
                annulets, a cushion echinus and a full 16 px square abacus
    ionic       shaft 8 wide, fluted with fillets, a bead astragal, two
                volutes that reach the slot's edges, an egg-and-dart echinus,
                a thin abacus, an Attic base (plinth, torus, scotia, torus)
    corinthian  shaft 8 wide, a tall bell of two tiers of acanthus leaves
                with corner helices and a concave abacus, an Attic base

Variants:
    marble      living temple marble: bright, cool, a dark slate outline
    poly        marble with painted polychromy: red and blue bands on the
                capital and abacus, gold on the echinus or leaves
    bronze      a marble shaft with a capital of bronze and gold
    moss        weathered marble: warmer and darker, drum joints showing,
                moss under each joint and at the foot, ivy on the shadow side
    snow        marble dusted with Olympus's snow: a cap on the abacus that
                overhangs and drips, snow in the capital, a dusting on each
                drum joint's lit side, a drift banked at the foot (snow_dust())

Light comes from the upper left. Every shaft is lit on its left third,
shadowed on its right third, and outlined in its own darkest color.

Palette groups (each <= 15 colors; every 8x8 tile draws from one):
    GROUPS["marble"]   marble, poly and the shadows they cast
    GROUPS["bronze"]   bronze-capped capitals (and any bronze statue)
    GROUPS["ruin"]     the moss variant and every fallen piece
    GROUPS["snow"]     the snow variant (marble, its paint, the snow's two values)
A tileset that uses the kit adds these groups (by name) to its seven.
All colors are multiples of 8 (exact BGR555).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_lib as K  # noqa: E402
from kythera_lib import Layer, struct  # noqa: E402,F401

ROOT = K.ROOT
A = K.A

# --------------------------------------------------------------------------
# Colors
# --------------------------------------------------------------------------

NEW = {
    # living marble, from the outline to the sunlit fillet
    "cm0": (48, 48, 72), "cm1": (112, 112, 136), "cm2": (160, 160, 176), "cm3": (200, 200, 208),
    "cm4": (232, 232, 232), "cm5": (248, 248, 248),
    # the dark behind a colonnade: pronaos, cella, a stoa's back wall
    "cd0": (24, 24, 40), "cd1": (64, 56, 88),
    # painted polychromy: Egyptian blue, cinnabar red, gilding
    "pr1": (184, 48, 40), "pb0": (32, 48, 120), "pb1": (64, 104, 184),
    "pg1": (208, 152, 48), "pg2": (248, 216, 112),
    # a cast shadow on aethos's limestone path
    "ps": (168, 144, 104),
    # weathered marble, moss, ivy, poppy and soil for ruins
    "wm0": (56, 48, 40), "wm1": (112, 104, 88), "wm2": (160, 152, 128), "wm3": (200, 192, 168),
    "wm4": (224, 216, 192), "mo1": (72, 96, 48), "mo2": (112, 136, 64), "iv1": (40, 72, 40),
    "iv2": (80, 120, 56), "pp1": (200, 40, 40), "so1": (120, 88, 56),
    # snow on marble (Olympus): the lit drift and its blue shadow
    "sw1": (224, 232, 248), "sw2": (168, 184, 216),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in K.C or K.C[_n] == _c, f"color name clash: {_n}"
    K.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    "marble": ["cm0", "cm1", "cm2", "cm3", "cm4", "cm5", "cd0", "cd1", "pr1", "pb0", "pb1",
               "pg1", "pg2", "ps", "gd"],
    "bronze": ["bz0", "bz1", "bz2", "bz3", "vg1", "vg2", "pg1", "pg2", "cm0", "cm1", "cm2",
               "cm3", "cm4", "cm5", "pr1"],
    "ruin": ["wm0", "wm1", "wm2", "wm3", "wm4", "mo1", "mo2", "iv1", "iv2", "pp1", "so1",
             "ps", "gd", "cd0", "g1"],
    "snow": ["cm0", "cm1", "cm2", "cm3", "cm4", "cm5", "sw1", "sw2", "cd0", "cd1", "pr1", "pb0",
             "pb1", "pg1", "pg2"],
}
for _g, _names in GROUPS.items():
    assert len(_names) <= 15, (_g, len(_names))
    assert len(set(C[n] for n in _names)) == len(_names), _g

# ramps, darkest first: outline, shadow, mid, light, bright, highlight
RAMP = {
    "marble": ["cm0", "cm1", "cm2", "cm3", "cm4", "cm5"],
    "poly": ["cm0", "cm1", "cm2", "cm3", "cm4", "cm5"],
    "bronze": ["cm0", "cm1", "cm2", "cm3", "cm4", "cm5"],
    "moss": ["wm0", "wm1", "wm2", "wm3", "wm4", "wm4"],
    "snow": ["cm0", "cm1", "cm2", "cm3", "cm4", "cm5"],
}
BRONZE = ["bz0", "bz1", "bz2", "bz3", "pg2", "cm5"]
SHADOW = {"path": "ps", "grass": "gd"}

ORDERS = ("doric", "ionic", "corinthian")
VARIANTS = ("marble", "poly", "bronze", "moss", "snow")
SHAFT_W = {"doric": 10, "ionic": 8, "corinthian": 8}


def cap_height(order):
    """Rows from the abacus's top to the first row of plain shaft."""
    return {"doric": 9, "ionic": 9, "corinthian": 14}[order]


def base_height(order):
    return {"doric": 0, "ionic": 7, "corinthian": 7}[order]


# --------------------------------------------------------------------------
# Painting
# --------------------------------------------------------------------------

def _px(L, x, y, c):
    if c is not None:
        L.px(x, y, c)


def _row(L, cx, y, w, cols, rmp):
    """One row of a symmetric moulding w wide about axis cx: cols names the
    ramp steps (indices) from the left edge inward; the right half mirrors
    them one step darker (light from the left)."""
    x0 = cx - w // 2
    for i in range(w):
        t = i / max(1, w - 1)
        if i == 0 or i == w - 1:
            k = 0
        elif t < 0.25:
            k = cols[0]
        elif t < 0.55:
            k = cols[1]
        elif t < 0.8:
            k = cols[2]
        else:
            k = cols[3]
        _px(L, x0 + i, y, rmp[k])


def _flutes(w):
    """Ramp indices across a shaft w wide, outline to outline: the light side
    left, flutes as alternating light and dark stripes, the shadow side right."""
    fixed = {10: [0, 4, 5, 3, 4, 3, 2, 3, 1, 0], 9: [0, 4, 5, 3, 4, 2, 3, 1, 0],
             8: [0, 4, 5, 3, 4, 2, 1, 0], 7: [0, 4, 5, 3, 2, 1, 0], 6: [0, 4, 5, 2, 1, 0],
             5: [0, 4, 3, 1, 0], 4: [0, 4, 2, 0]}
    if w in fixed:
        return fixed[w]
    out = [0]
    for i in range(1, w - 1):
        t = i / (w - 1)
        out.append(5 if i == 1 else (4 if i % 2 else 3) if t < 0.5 else (2 if i % 2 else 3) if t < 0.8 else 1)
    return out + [0]


def shaft_edges(order, t):
    """(left inset, right inset) of the shaft at height t (0 at the capital,
    1 at the foot): entasis as a 1 px taper over the top third, the left
    (lit) edge straight until the necking."""
    left = 1 if t < 0.06 else 0
    right = 1 if t < 0.22 else 0
    return left, right


def paint_shaft(L, cx, y0, y1, order, variant, joints=None, span=None):
    """The shaft from row y0 to y1 (inclusive). `span` = (top, bottom) of the
    whole shaft when this is only a piece of it, so entasis is measured on
    the whole column. Joints: rows where one drum meets the next."""
    rmp = RAMP[variant]
    W = SHAFT_W[order]
    top, bot = span or (y0, y1)
    prof = _flutes(W)
    for y in range(y0, y1 + 1):
        t = (y - top) / max(1, bot - top)
        li, ri = shaft_edges(order, t)
        x0, x1 = cx - W // 2 + li, cx + W // 2 - 1 - ri
        w = x1 - x0 + 1
        pr = prof if w == W else _flutes(w)
        for i in range(w):
            _px(L, x0 + i, y, rmp[pr[i]])
        if joints and (y - top) % joints == joints - 1 and y != bot:
            for x in range(x0 + 1, x1):
                _px(L, x, y, rmp[2] if x < cx else rmp[1])
            if variant == "moss":
                for x in range(x0 + 1, x1):
                    if (x * 5 + y) % 3 == 0:
                        _px(L, x, y + 1, "mo1" if x > cx else "mo2")
    if variant == "moss":
        # ivy climbing the shadow side, from the foot up about half the shaft
        for y in range(y0, y1 + 1):
            t = (y - top) / max(1, bot - top)
            if t > 0.45:
                x = cx + W // 2 - 2 + ((y // 2) % 2)
                if (y * 7) % 5 < 3:
                    _px(L, x, y, "iv2" if (y // 2) % 3 else "iv1")
                    if (y // 3) % 2 == 0:
                        _px(L, x + 1, y, "iv1")


def _cap_ramp(variant):
    return BRONZE if variant == "bronze" else RAMP[variant]


def paint_doric_capital(L, cx, y, variant):
    """Abacus (3 rows, 16 wide), echinus (3 rows), annulets (2): 8 rows, then
    the necking (1 row)."""
    r = _cap_ramp(variant)
    # abacus: a square slab, lit top, a hard shadow under it
    _row(L, cx, y, 16, [5, 4, 4, 3], r)
    _row(L, cx, y + 1, 16, [4, 3, 3, 2], r)
    _row(L, cx, y + 2, 16, [1, 1, 1, 0], r)
    if variant == "poly":
        for x in range(cx - 7, cx + 7):
            # a painted meander on the abacus's face
            L.px(x, y + 1, "pb1" if (x - cx) % 4 in (0, 1) else "pb0")
    # echinus: the cushion, widest under the abacus
    for j, w in enumerate((14, 12, 11)):
        _row(L, cx, y + 3 + j, w, [5, 4, 3, 2] if j == 0 else [4, 3, 2, 1], r)
    if variant == "poly":
        for x in range(cx - 5, cx + 5):
            L.px(x, y + 4, "pg1" if x < cx + 2 else "pg1")
            if (x - cx) % 2 == 0:
                L.px(x, y + 3, "pr1")
    # annulets: two thin rings
    _row(L, cx, y + 6, 10, [2, 1, 1, 0], r)
    _row(L, cx, y + 7, 10, [4, 3, 2, 1], r)
    if variant == "poly":
        _row(L, cx, y + 6, 10, [0, 0, 0, 0], r)
        for x in range(cx - 4, cx + 4):
            L.px(x, y + 6, "pr1")
    # the necking, one row of the narrowed shaft in shadow
    rr = RAMP[variant]
    for x in range(cx - 4, cx + 4):
        _px(L, x, y + 8, rr[0] if x in (cx - 4, cx + 3) else rr[1] if x > cx else rr[2])


VOLUTE = [
    # 6 x 6, the left volute: '#' outline, 'h' the lit turn, 'm' its shadow,
    # 'e' the eye at the spiral's heart
    ".####.",
    "#hhmm#",
    "#h#e##",
    "#hm#m#",
    "#mmmm#",
    ".####.",
]


def paint_ionic_capital(L, cx, y, variant):
    """Abacus (2 rows, 14 wide), the volute band (5 rows, 16 wide) with an
    egg-and-dart echinus between the volutes, the bead astragal (1 row) and
    the top of the shaft: 9 rows."""
    r = _cap_ramp(variant)
    _row(L, cx, y, 14, [5, 4, 3, 2], r)
    _row(L, cx, y + 1, 14, [2, 2, 1, 1], r)
    # the cushion between the volutes
    for j in range(4):
        _row(L, cx, y + 2 + j, 12, [4, 4, 3, 2] if j < 2 else [3, 3, 2, 1], r)
    # egg-and-dart along the echinus's lower edge
    for x in range(cx - 4, cx + 4):
        e = (x - cx) % 3
        L.px(x, y + 4, r[4] if e == 0 else r[1] if e == 1 else r[2])
        if variant == "poly" and e == 0:
            L.px(x, y + 4, "pr1")
        if variant == "poly" and e == 2:
            L.px(x, y + 4, "pb1")
    eye = "pg2" if variant in ("poly",) else r[3]
    for side in (-1, 1):
        ox = cx - 8 if side < 0 else cx + 2
        for j, row in enumerate(VOLUTE):
            if side > 0:
                row = row[::-1]
            for i, ch in enumerate(row):
                if ch == ".":
                    continue
                c = {"#": r[0], "h": r[4] if side < 0 else r[3], "m": r[2] if side < 0 else r[1],
                     "e": eye}[ch]
                L.px(ox + i, y + 2 + j, c)
    # the bead astragal
    for x in range(cx - 4, cx + 4):
        L.px(x, y + 7, r[4] if (x - cx) % 2 == 0 else r[1])
    rr = RAMP[variant]
    for x in range(cx - 4, cx + 4):
        _px(L, x, y + 8, rr[0] if x in (cx - 4, cx + 3) else rr[2] if x < cx else rr[1])


LEAF = [
    # 4 x 5, one acanthus leaf, its tip curling outward; 'h' lit lobe, 'm' mid,
    # 'd' the rib and the curl's shadow
    ".dh.",
    "dhmd",
    "hmdm",
    "hmdm",
    ".md.",
]


def paint_corinthian_capital(L, cx, y, variant):
    """A concave abacus (2 rows), corner helices, and a bell of acanthus in two
    tiers, widening upward from the shaft: 14 rows to the first shaft row."""
    r = _cap_ramp(variant)
    gold = variant in ("poly", "bronze")
    # concave abacus: horned corners, a flower (fleuron) in the middle
    _row(L, cx, y, 16, [5, 4, 3, 2], r)
    _row(L, cx, y + 1, 14, [2, 2, 1, 1], r)
    L.px(cx - 1, y + 1, "pg2" if gold else r[5])
    L.px(cx, y + 1, "pg1" if gold else r[4])
    # the bell behind the leaves, tapering from 14 to 10 wide
    for j in range(12):
        w = 14 - (j * 4) // 11
        _row(L, cx, y + 2 + j, w, [3, 3, 2, 1], r)
    # corner helices: small curls springing out under the abacus horns
    for side in (-1, 1):
        x = cx - 7 if side < 0 else cx + 4
        curl = ["##.", "#h#", ".##"] if side < 0 else [".##", "#m#", "##."]
        for j, row in enumerate(curl):
            for i, ch in enumerate(row):
                if ch != ".":
                    L.px(x + i, y + 2 + j, r[0] if ch == "#" else (r[4] if side < 0 else r[2]))
    # two tiers of acanthus: the upper tier between the lower tier's leaves
    def leaf(x0, y0, flip=False):
        for j, row in enumerate(LEAF):
            if flip:
                row = row[::-1]
            for i, ch in enumerate(row):
                if ch == ".":
                    continue
                lit = (x0 + i) < cx
                c = {"h": r[5] if lit else r[3], "m": r[3] if lit else r[2], "d": r[0] if not lit else r[1]}[ch]
                if gold and ch == "h":
                    c = "pg2" if lit else "pg1"
                L.px(x0 + i, y0 + j, c)
    leaf(cx - 6, y + 4)
    leaf(cx + 2, y + 4, flip=True)
    leaf(cx - 2, y + 5)
    leaf(cx - 5, y + 8)
    leaf(cx + 1, y + 8, flip=True)
    # the shaft's top ring under the bell
    for x in range(cx - 4, cx + 4):
        L.px(x, y + 13, r[1] if (x - cx) % 2 else r[4])


def paint_attic_base(L, cx, y, variant):
    """7 rows from y: upper torus (2), scotia (1), lower torus (2), plinth (2)."""
    r = RAMP[variant]
    _row(L, cx, y, 10, [5, 4, 3, 1], r)
    _row(L, cx, y + 1, 12, [4, 3, 2, 1], r)
    _row(L, cx, y + 2, 10, [1, 1, 1, 0], r)
    _row(L, cx, y + 3, 12, [5, 4, 3, 2], r)
    _row(L, cx, y + 4, 14, [4, 3, 2, 1], r)
    _row(L, cx, y + 5, 14, [3, 3, 2, 2], r)
    _row(L, cx, y + 6, 14, [1, 1, 1, 0], r)
    if variant == "moss":
        for x in range(cx - 6, cx + 7):
            if (x * 3) % 4 != 1:
                L.px(x, y + 6, "mo1" if x > cx else "mo2")
        L.px(cx + 5, y + 5, "mo1")


def paint_column(L, cx, top, bottom, order, variant, joints=16, cap=True, base=True):
    """A whole column, abacus top at `top`, base (or the Doric shaft's foot)
    ending at `bottom`. cap=False / base=False leave those off (a column
    under a lintel that is drawn elsewhere, or one sunk in rubble)."""
    ch = cap_height(order) if cap else 0
    bh = base_height(order) if base else 0
    s0, s1 = top + ch, bottom - bh
    if cap:
        {"doric": paint_doric_capital, "ionic": paint_ionic_capital,
         "corinthian": paint_corinthian_capital}[order](L, cx, top, variant)
    paint_shaft(L, cx, s0, s1, order, variant, joints=joints if variant == "moss" else None,
                span=(s0, s1))
    if base and bh:
        paint_attic_base(L, cx, s1 + 1, variant)
    elif order == "doric" and variant == "moss":
        for x in range(cx - 5, cx + 5):
            if (x + bottom) % 3:
                L.px(x, bottom, "mo1" if x > cx else "mo2")
    if variant == "snow":
        snow_dust(L, cx, top, bottom, order, cap=cap, joints=joints)


def snow_dust(L, cx, top, bottom, order="doric", cap=True, joints=16):
    """Olympus's snow on a column: a cap of snow on the abacus that overhangs
    and drips, snow lodged in the capital, a dusting on the lit side of every
    drum joint, and a drift banked against the foot. Draw it over any column
    (paint_column does, for variant 'snow'); its colors are GROUPS['snow']."""
    if cap:
        for x in range(cx - 8, cx + 8):
            L.px(x, top, "cm5" if x < cx + 4 else "sw1")
            if top - 1 >= 0 and cx - 7 <= x <= cx + 5 and (x * 3) % 7:
                L.px(x, top - 1, "cm5" if x < cx else "sw1")
        for x in (cx - 7, cx - 2, cx + 5):
            L.px(x, top + 1, "sw1")
        L.px(cx - 7, top + 2, "sw2")
        k = cap_height(order)
        for x in range(cx - 5, cx + 4, 2):
            L.px(x, top + k // 2, "sw1")
    s0 = top + (cap_height(order) if cap else 0)
    for y in range(s0 + joints - 1, bottom - 6, joints):
        for x in range(cx - SHAFT_W[order] // 2 + 1, cx):
            L.px(x, y, "sw1" if x < cx - 2 else "sw2")
    for j, w in enumerate((6, 10, 14)):
        y = bottom - 2 + j
        for x in range(cx - w // 2 - 1, cx + w // 2):
            L.px(x, y, "cm5" if x < cx else "sw1" if x < cx + w // 2 - 2 else "sw2")


def cast_shadow(L, cx, foot, ground="path", length=7, rows=3):
    """The column's shadow on the floor: a band falling down and to the right
    from its foot, `rows` tall, fading at its far end."""
    c = SHADOW[ground]
    for j in range(rows):
        y = foot - rows + 2 + j
        x0 = cx + 3 + j
        for i in range(length - j):
            x = x0 + i
            if L.get(x, y) is None and (i < length - j - 2 or (x + y) % 2 == 0):
                L.px(x, y, c)


def paint_stylobate(L, x0, x1, y, rows=4, variant="marble", steps=1):
    """A stepped platform's top (the stylobate) from x0 to x1, `rows` tall per
    step: a lit tread, a riser, a shadow line under it. steps > 1 draws a
    krepis, each lower step 2 px wider each side."""
    r = RAMP[variant]
    for s in range(steps):
        a, b = x0 - 2 * s, x1 + 2 * s
        yy = y + s * rows
        for x in range(a, b + 1):
            edge = x in (a, b)
            L.px(x, yy, r[0] if edge else r[5] if x < a + 3 else r[4])
            for k in range(1, rows - 1):
                L.px(x, yy + k, r[0] if edge else r[3] if (x + k) % 9 else r[2])
            L.px(x, yy + rows - 1, r[1] if not edge else r[0])
        # block joints on the risers
        for x in range(a + 6, b, 12 + 2 * s):
            for k in range(1, rows - 1):
                L.px(x, yy + k, r[2])


def paint_architrave(L, x0, x1, y, rows=5, variant="marble", regulae=None):
    """A plain architrave beam: lit top fillet, face, a dark soffit line."""
    r = RAMP[variant]
    for x in range(x0, x1 + 1):
        edge = x in (x0, x1)
        L.px(x, y, r[0] if edge else r[5])
        for k in range(1, rows - 1):
            L.px(x, y + k, r[0] if edge else r[4] if k == 1 else r[3])
        L.px(x, y + rows - 1, r[0])
    if regulae:
        for x in regulae:
            for i in range(-2, 2):
                L.px(x + i, y + 1, r[2])


# --------------------------------------------------------------------------
# Ready-made structures
# --------------------------------------------------------------------------

def free_column(order, variant, height=3, on="path", key=None, shadow=True):
    """A free-standing column, 1 x height metatiles (2-6; 5-6 is a colossal
    order), on borrowed aethos ground. Cells: 'cap' (top), 'shaft_top'
    (height >= 4), 'shaft' (height >= 3), 'shaft_2', 'shaft_3' (heights 5, 6),
    'base'. The upper cells are on the top layer and walkable (T): the player
    walks behind the column. The base is on the middle layer and solid (X),
    with the cast shadow. A Doric column stands on a square stylobate block."""
    assert 2 <= height <= 6
    key = key or f"col_{order}_{variant}_{height}"
    names = (["cap"] + (["shaft_top"] if height >= 4 else []) + (["shaft"] if height >= 3 else [])
             + [f"shaft_{i}" for i in range(2, height - 2)] + ["base"])
    s = struct(key, f"{order} column ({variant}, {height} tall)", 1, height, "columns",
               walk=["T"] * (height - 1) + ["X"], names={n: (0, i) for i, n in enumerate(names)}, on=on)
    H = height * 16
    full = Layer(16, H)
    foot = H - 3
    if order == "doric":
        paint_column(full, 8, 1, foot - 4, order, variant)
        # the square block it stands on
        r = RAMP[variant]
        for x in range(1, 15):
            edge = x in (1, 14)
            full.px(x, foot - 3, r[0] if edge else r[5])
            full.px(x, foot - 2, r[0] if edge else r[3])
            full.px(x, foot - 1, r[0] if edge else r[2])
            full.px(x, foot, r[0])
    else:
        paint_column(full, 8, 1, foot, order, variant)
    if shadow:
        cast_shadow(full, 8, foot + 1, on if on in SHADOW else "path", length=9, rows=3)
    # split: everything above the base cell goes on the top layer
    s.T.a[:(height - 1) * 16] = full.a[:(height - 1) * 16]
    s.M.a[(height - 1) * 16:] = full.a[(height - 1) * 16:]
    return s


def colonnade_shadow(on="path", key="col_shadow"):
    """The long shadow a column casts across the next cell to its right."""
    s = struct(key, "column shadow tail", 1, 1, "columns", walk=["."], names={"tail": (0, 0)}, on=on)
    c = SHADOW[on]
    for j in range(3):
        y = 13 + j
        for x in range(0, 6 - j):
            if x < 4 - j or (x + y) % 2 == 0:
                s.M.px(x, y, c)
    return s


def drum(L, x, y, variant="moss", order="doric", flip=False):
    """A toppled drum lying on its side, 14 x 8 px from (x, y): the curved
    body seen from above with its flutes running along it, and its round end
    face catching the light, the dowel hole in the middle."""
    r = RAMP[variant]
    w = 14
    body = [0, 5, 4, 3, 4, 2, 1, 0]          # rows: lit top, flutes, shadowed underside
    for j in range(8):
        for i in range(w):
            xx = x + (w - 1 - i if flip else i)
            L.px(xx, y + j, r[body[j]])
    ex = x if not flip else x + w - 5
    face = [".###.", "#545#", "#4.4#", "#434#", "#333#", "#323#", "#222#", ".###."]
    for j, row in enumerate(face):
        for i, ch in enumerate(row):
            if ch == ".":
                continue
            L.px(ex + i, y + j, r[0] if ch == "#" else r[1] if ch == "." else r[int(ch)])
    L.px(ex + 2, y + 2, r[1])
    if variant == "moss":
        for i in range(2, w - 1, 3):
            L.px(x + i, y + 7, "mo1")
        L.px(x + 6, y + 6, "mo2")
        L.px(x + 9, y + 1, "iv2")


def ruins(variant="moss", on="grass", key=None):
    """Fallen pieces, each one metatile unless named wider:
      stub        a broken shaft, its top snapped off in a jagged line (solid)
      broken_T, broken_B
                  a taller broken column, 1 x 2 (top on the top layer)
      drum, drum_b
                  one toppled drum, two lying angles
      drums_L, drums_M, drums_R
                  a fallen column as a line of separated drums (3 x 1)
      cap_doric, cap_ionic, cap_corinthian
                  a fallen capital lying where it fell
      plinth_feet a statue's plinth with only the feet left
      poppies     poppies and thistle in the cracks (walkable)
    """
    names = ["stub", "drum", "drum_b", "cap_doric", "cap_ionic", "cap_corinthian", "plinth_feet",
             "poppies", "broken_T", "drums_L", "drums_M", "drums_R"]
    w = 8
    pos = {n: (i % w, i // w) for i, n in enumerate(names)}
    pos["broken_B"] = (pos["broken_T"][0], pos["broken_T"][1] + 1)
    rows = ["XXXXXXX.", "TXXX....", "X......."]
    s = struct(key or f"ruins_{variant}", f"fallen column pieces ({variant})", w, 3, "ruins", walk=rows,
               names=pos, on=on)
    sh = SHADOW.get(on, "gd")
    r = RAMP[variant]

    def at(n):
        cx, cy = pos[n]
        return cx * 16, cy * 16

    # a broken stub: the shaft's foot and a snapped top
    x, y = at("stub")
    L = Layer(16, 16)
    paint_shaft(L, 8, 4, 13, "doric", variant, span=(-30, 13))
    for x2, cut in zip(range(3, 13), (6, 5, 4, 5, 7, 6, 4, 5, 6, 7)):
        for yy in range(4, cut):
            L.px(x2, yy, None)
        L.px(x2, cut, r[5] if x2 < 8 else r[3])
    for x2 in range(2, 15):
        L.px(x2, 14, r[0] if x2 in (2, 14) else r[2])
    s.M.a[y:y + 16, x:x + 16] = L.a
    _shadow_px(s.M, x, y, sh)
    # a taller broken column, 2 cells
    x, y = at("broken_T")
    L = Layer(16, 32)
    paint_shaft(L, 8, 9, 28, "doric", variant, joints=12, span=(-10, 28))
    for x2, cut in zip(range(3, 13), (12, 10, 9, 11, 13, 12, 10, 11, 14, 15)):
        for yy in range(9, cut):
            L.px(x2, yy, None)
        L.px(x2, cut, r[5] if x2 < 8 else r[3])
    for x2 in range(2, 15):
        L.px(x2, 29, r[0] if x2 in (2, 14) else r[2])
        L.px(x2, 30, r[1] if x2 not in (2, 14) else r[0])
    s.T.a[y:y + 16, x:x + 16] = L.a[0:16]
    s.M.a[y + 16:y + 32, x:x + 16] = L.a[16:32]
    _shadow_px(s.M, x, y + 16, sh)
    # toppled drums
    x, y = at("drum")
    drum(s.M, x + 1, y + 5, variant)
    _shadow_px(s.M, x, y, sh, rows=2)
    x, y = at("drum_b")
    drum(s.M, x + 1, y + 3, variant, flip=True)
    _shadow_px(s.M, x, y - 2, sh, rows=2)
    # a line of drums across three cells, a little offset, as they rolled
    x, y = at("drums_L")
    for k, (dx, dy) in enumerate(((2, 5), (17, 6), (33, 4))):
        drum(s.M, x + dx, y + dy, variant, flip=k == 2)
    for k in range(3):
        _shadow_px(s.M, x + 16 * k, y, sh, rows=2)
    # fallen capitals
    for n, order in (("cap_doric", "doric"), ("cap_ionic", "ionic"), ("cap_corinthian", "corinthian")):
        x, y = at(n)
        L = Layer(16, 16)
        if order == "corinthian":
            paint_corinthian_capital(L, 8, 1, variant)
            # lying on its side: cut it off at the leaves
            L.a[13:] = 0
        elif order == "ionic":
            paint_ionic_capital(L, 8, 5, variant)
            L.a[13:] = 0
        else:
            paint_doric_capital(L, 8, 5, variant)
            L.a[13:] = 0
        # it lies tilted: drop the right half by a pixel
        a = L.a.copy()
        a[:, 8:] = np.roll(a[:, 8:], 1, axis=0)
        s.M.a[y:y + 16, x:x + 16] = np.where(a[..., 3:4] > 0, a, s.M.a[y:y + 16, x:x + 16])
        if variant == "moss":
            for xx in range(x + 3, x + 13, 2):
                s.M.px(xx, y + 13, "mo1")
            s.M.px(x + 2, y + 12, "iv2")
            s.M.px(x + 3, y + 11, "iv1")
        _shadow_px(s.M, x, y, sh, rows=2)
    # the plinth with only the feet
    x, y = at("plinth_feet")
    for yy in range(7, 15):
        for xx in range(2, 14):
            edge = xx in (2, 13) or yy == 14
            k = 0 if edge else 5 if yy == 7 else 4 if yy < 10 else 3 if yy < 13 else 2
            s.M.px(x + xx, y + yy, r[k])
    feet = ["#hh#..#mm#", "#hhh#.#mmm#"]
    for j, row in enumerate(feet):
        for i, ch in enumerate(row):
            if ch != ".":
                s.M.px(x + 3 + i, y + 5 + j, r[0] if ch == "#" else r[4] if ch == "h" else r[2])
    for xx in range(3, 13):
        s.M.px(x + xx, y + 10, r[2] if xx % 3 else r[1])       # the worn inscription
    _shadow_px(s.M, x, y, sh)
    # poppies and thistle in the cracks (walkable)
    x, y = at("poppies")
    for (dx, dy, c) in ((3, 9, "pp1"), (4, 8, "pp1"), (4, 10, "mo1"), (10, 5, "pp1"), (11, 6, "mo2"),
                        (12, 11, "iv2"), (7, 12, "pp1"), (8, 13, "mo1"), (6, 4, "mo2"), (13, 12, "iv1")):
        s.M.px(x + dx, y + dy, c)
    return s


def _shadow_px(L, x, y, c, rows=3):
    """A shadow on the cell's floor under and right of whatever is drawn."""
    for j in range(rows):
        yy = y + 15 - j
        for xx in range(x + 5 + j, x + 16):
            if L.get(xx, yy) is None and (xx + yy) % 2 == 0 or (L.get(xx, yy) is None and xx < x + 12 and j == 0):
                L.px(xx, yy, c)


def kit(on="path", orders=ORDERS, variants=VARIANTS, height=3):
    """Every free-standing column of the given orders and variants."""
    return [free_column(o, v, height, on) for o in orders for v in variants]


# --------------------------------------------------------------------------
# The reference sheet
# --------------------------------------------------------------------------

def reference_sheet(out=None, scale=4):
    """design/art/columns_kit.png: every order in every variant, standing and
    in a colonnade, the parts named, and the ruins."""
    from PIL import Image, ImageDraw
    out = out or ROOT / "design/art/columns_kit.png"
    pad, lab = 6, 12
    panels = []
    # 1. the orders: three heights in marble, each variant at height 4
    for o in ORDERS:
        for v in VARIANTS:
            panels.append((f"{o[:4]} {v}", free_column(o, v, 4, "path")))
    panels.append(("colossal ionic (6)", free_column("ionic", "marble", 6, "path", key="colossal_i")))
    panels.append(("colossal doric snow (6)", free_column("doric", "snow", 6, "path", key="colossal_d")))
    # 2. a colonnade on its stylobate, in front of a dark cella, pitch 16 and 32
    colo = []
    for o, v in (("doric", "poly"), ("ionic", "marble"), ("corinthian", "bronze"), ("doric", "moss"),
                 ("ionic", "snow")):
        s = struct(f"colo_{o}_{v}", "colonnade", 6, 4, "ref", walk=["XXXXXX"] * 4)
        L = s.B
        L.rect(0, 0, 96, 64, "cd1")
        L.rect(0, 0, 96, 4, "cd0")
        paint_architrave(L, 0, 95, 0, 6, "marble" if v != "moss" else "moss")
        for i in range(6):
            paint_column(L, 8 + 16 * i, 6, 55, o, v)
        paint_stylobate(L, 0, 95, 56, 4, "marble" if v != "moss" else "moss", steps=2)
        colo.append((f"{o} {v}, pitch 16", s))
    panels += colo
    s = struct("colo_wide", "colonnade", 8, 4, "ref", walk=["XXXXXXXX"] * 4)
    s.B.rect(0, 0, 128, 64, "cd1")
    paint_architrave(s.B, 0, 127, 0, 6)
    for i in range(4):
        paint_column(s.B, 8 + 32 * i, 6, 55, "doric", "marble")
    paint_stylobate(s.B, 0, 127, 56, 4, steps=2)
    panels.append(("doric, pitch 32 (1-tile gaps)", s))
    panels.append(("ruins (moss)", ruins("moss", "grass")))
    panels.append(("ruins (marble)", ruins("marble", "path", key="ruins_marble")))
    imgs = []
    for name, st in panels:
        im = Image.fromarray(K.composite(st)).resize((st.w * 16 * scale, st.h * 16 * scale), Image.NEAREST)
        imgs.append((name, im))
    W = 1800
    rows, cur, cw = [], [], pad
    for n, im in imgs:
        w = max(im.width, len(n) * 7) + pad
        if cur and cw + w > W:
            rows.append(cur)
            cur, cw = [], pad
        cur.append((n, im))
        cw += w
    rows.append(cur)
    H = 40 + sum(max(i.height for _, i in r) + lab + pad for r in rows) + pad
    sheet = Image.new("RGB", (W, H), (28, 28, 36))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 8), "Ichor column kit (tools/ichor/art/columns.py): orders x variants, colonnades, ruins. "
           "4x; grid = 16 px metatiles. Light from the upper left.", fill=(240, 230, 200))
    y = 32
    for r in rows:
        x = pad
        for n, im in r:
            d.text((x, y), n, fill=(230, 230, 200))
            sheet.paste(im, (x, y + lab))
            x += max(im.width, len(n) * 7) + pad
        y += max(i.height for _, i in r) + lab + pad
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    return out


if __name__ == "__main__":
    print(reference_sheet())
