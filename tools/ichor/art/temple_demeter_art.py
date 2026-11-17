"""The Temple of Demeter's interior: gTileset_TempleDemeter, an underground
megaron for the Lesser Mysteries (SYSTEMS.md §12: dark and light).

The Telesterion's hall under Eleusa: a forest of columns in near-darkness,
rock-cut tiers along the walls, the Descent of Persephone painted round the
frieze, tripod braziers and wall torches (cold and lit), the Anaktoron (the
inner shrine) with the Hierophant's throne by its door, kykeon vessels and
baskets of sacred things, the draughty doorway hung with ribbons, the crypt's
stone sentinels, and the wreck the Titans leave.

The rite's puzzle verbs and how the art serves them:

  Light   Every light source has a cold and a lit metatile; the lit one is the
          cold one + 1, as in the Hearth Trial. A lit brazier or torch stands in
          a pool of warmed floor: the seven `glow_*` ring cells (also cold +
          offset free: swap them in round it).
  Douse   Glow-paint. Persephone's pomegranate seeds on the floor and Hecate's
          chalk on the walls are painted in two *latent* colors, one step off
          the stone beside them, so by torchlight they don't show.
          temple_demeter_build.py writes a second palette set (`glow/`) that is
          black everywhere except those two colors (seeds blaze red, chalk
          glows violet) and the flames. Loading it with the torch doused shows
          the marks across the whole screen; the walls vanish.
  Wind    The draughty doorway: a partition wall's opening hung with ribbons
          that stream through it, in two variants for the two directions.
  Reveal  A doorway painted in the frieze, and the same wall opened (closed +
          1): a lit brazier can reveal it.

Everything is in the bottom (opaque) and middle layers, as in the Temple of
Hestia, so every metatile is COVERED and the primary never shows through.
Light falls from the top left; rims and highlights are torch-warm.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agros_lib as A  # noqa: E402
from agros_lib import Layer, Struct  # noqa: E402,F401
from eleusa_lib import put  # noqa: E402

# --------------------------------------------------------------------------
# Colors and palette groups
# --------------------------------------------------------------------------

NEW = {
    # Eleusis's dark limestone by torchlight, from the void to the rim light
    "dk0": (16, 8, 16), "dk1": (40, 32, 40), "dk2": (64, 56, 64), "dk3": (96, 80, 80),
    "dk4": (136, 112, 96), "dk5": (184, 152, 112),
    # latent glow-paint: one step off dk2 (floor) and dk3 (wall)
    "dls": (64, 56, 72), "dlf": (72, 56, 64), "dlc": (96, 80, 88),
    # stone warmed by a lit brazier
    "dw1": (104, 72, 56), "dw2": (152, 104, 64), "dw3": (200, 144, 80), "dw4": (240, 192, 112),
    "du": (152, 136, 120),
    # the fresco: red and yellow ochre, lime white, Egyptian blue, green, skin
    "fr": (176, 56, 32), "fy": (216, 168, 80), "fw": (232, 216, 184), "fb": (64, 96, 152),
    "fg": (88, 120, 64), "fp": (216, 144, 112),
    # bronze, flame, ash and coal
    "bz0": (56, 32, 16), "bz1": (112, 72, 32), "bz2": (176, 120, 56), "bz3": (224, 176, 96),
    "fx0": (168, 40, 16), "fx1": (232, 104, 24), "fx2": (248, 176, 48), "fx3": (248, 232, 136),
    "fx4": (248, 248, 216), "ash": (80, 72, 72), "coal": (120, 24, 16),
    # marble by torchlight, gilding, the throne's red cushion
    "mb1": (224, 200, 160), "mb2": (184, 160, 120), "mb3": (144, 120, 96), "mb4": (104, 80, 72),
    "ga": (216, 168, 64), "gb": (160, 112, 40), "rd1": (152, 40, 32), "rd2": (200, 72, 48),
    # clay, kykeon, wicker, ribbons
    "tk0": (104, 40, 24), "tk1": (168, 80, 48), "tk2": (216, 128, 80), "mint": (104, 144, 72),
    "barl": (216, 184, 104), "wc1": (112, 80, 48), "wc2": (168, 128, 72), "rbn": (192, 48, 40),
    "rbw": (232, 224, 208), "rbs": (232, 176, 48),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    assert _n not in A.C or A.C[_n] == _c, f"color name clash: {_n}"
    A.C[_n] = _c
    A.RGB2NAME.setdefault(_c, _n)
C = A.C

STONE = ["dk0", "dk1", "dk2", "dk3", "dk4", "dk5"]
GROUPS = {
    "floor": STONE + ["dls", "dlf", "dw1", "dw2", "dw3", "dw4", "du", "ga", "gb"],
    "wall": STONE + ["dlc", "fr", "fy", "fw", "fb", "fg", "fp", "ga"],
    "fire": ["bz0", "bz1", "bz2", "bz3", "fx0", "fx1", "fx2", "fx3", "fx4", "ash", "coal",
             "dk0", "dk2", "dk3", "dk4"],
    "marble": ["mb1", "mb2", "mb3", "mb4", "ga", "gb", "rd1", "rd2"] + STONE[:6] + ["fw"],
    "clay": ["tk0", "tk1", "tk2", "dk0", "mint", "barl", "wc1", "wc2", "rbn", "rbw", "rbs",
             "ga", "dk2", "dk3", "fw"],
    "warm": ["dw1", "dw2", "dw3", "dw4", "fr", "fy", "fw", "fb"] + STONE,
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}

# Glow-paint: latent color name -> the color it glows when the torch is doused
LATENT = {"dls": (248, 80, 104), "dlf": (200, 184, 248), "dlc": (200, 184, 248)}
# ... and the base color it imitates by torchlight
LATENT_BASE = {"dls": "dk2", "dlf": "dk2", "dlc": "dk3"}
# Flames stay lit in the glow set: they are the landmarks in the dark
FLAMES = ["fx1", "fx2", "fx3", "fx4", "coal"]

SEC = "temple"


def struct(key, title, w, h, walk=None, notes="", names=None, behaviors=None):
    s = Struct(key, title, w, h, SEC, walk=walk, notes=notes, names=names)
    for cy, row in enumerate(s.walk):
        for cx, ch in enumerate(row):
            if ch == "D":
                s.behaviors[(cx, cy)] = "MB_NON_ANIMATED_DOOR"
            elif ch == "S":
                s.behaviors[(cx, cy)] = "MB_SOUTH_ARROW_WARP"
    s.behaviors.update(behaviors or {})
    return s


# --------------------------------------------------------------------------
# Floor
# --------------------------------------------------------------------------


def floor_px(x, y, variant=0):
    """Dark flagstones, 16 px periodic: two courses of long slabs, each lit
    along its top-left edge, joints in shadow."""
    xx, yy = x % 16, y % 16
    course = yy // 8
    off = (0, 6, 3)[variant % 3] if course else 0
    sx = (xx + off) % 16
    if yy % 8 == 7 or sx in (0, 10):
        return "dk1"
    if yy % 8 == 0 or sx in (1, 11):
        return "dk3"
    if (xx * 7 + yy * 5 + variant * 3) % 31 == 0:
        return "dk4"
    if (xx * 3 + yy * 11 + variant) % 17 == 0:
        return "dk1"
    return "dk2"


def floor(L, ox, oy, variant=0):
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, floor_px(x, y, variant))


def warm(c, level):
    """Stone warmed by firelight: level 1 faint .. 3 strong."""
    ramp = {"dk1": ["dk1", "dk2", "dw1", "dw1"], "dk2": ["dk2", "dw1", "dw2", "dw2"],
            "dk3": ["dk3", "dw2", "dw3", "dw3"], "dk4": ["dk4", "dw3", "dw4", "dw4"],
            "dk5": ["dk5", "dw4", "dw4", "dw4"], "dk0": ["dk0", "dk1", "dk2", "dw1"],
            "dls": ["dls", "dw1", "dw2", "dw2"]}
    return ramp.get(c, [c] * 4)[level]


def lit_disc(L, ox, oy, w, h, cx, cy, r):
    """Warm the floor pixels of a box by distance from a light at (cx, cy)."""
    for y in range(h):
        for x in range(w):
            c = L.get(ox + x, oy + y)
            if c is None:
                continue
            d = ((x - cx) ** 2 + ((y - cy) * 1.15) ** 2) ** 0.5 / r
            lv = 3 if d < 0.35 else (2 if d < 0.65 else (1 if d < 1.0 else 0))
            if lv == 1 and (x + y) % 2 and d > 0.82:
                lv = 0
            if lv == 2 and (x + y) % 2 and d > 0.55:
                lv = 1
            if lv:
                L.px(ox + x, oy + y, warm(c, lv))


SEED = [".ss.", "ssss", "ssss", ".ss."]
CHALK_Y = [
    "......c.c.......",
    ".......c........",
    ".......c........",
    "......ccc.......",
]


def floor_pieces():
    keys = ["floor", "floor_b", "floor_c", "floor_cracked", "bootprints", "draught",
            "seed", "seeds", "chalk_fork", "chalk_trail_h", "chalk_trail_v", "rubble", "void",
            "floor_inlay"]
    s = struct("floor", "Floor: flagstones, the trail and the wreck", 7, 2,
               walk=[".......", "....XX."],
               names={k: (i % 7, i // 7) for i, k in enumerate(keys)},
               notes="Walkable flagstones (`floor`, `floor_b`, `floor_c` to break up a run, "
                     "`floor_cracked`), the Titans' `bootprints`, and `draught`: dust "
                     "streaming toward a draughty doorway. `seed` and `seeds` are Persephone's "
                     "pomegranate seeds and `chalk_fork`, `chalk_trail_h`/`_v` Hecate's "
                     "chalk, painted in the latent color: plain floor by torchlight, glowing "
                     "when the torch is doused (the `glow/` palettes). `rubble` blocks; "
                     "`void` is black, for the border; `floor_inlay` is the Anaktoron's "
                     "gilt threshold.")
    L = s.B
    for i, k in enumerate(keys):
        ox, oy = (i % 7) * 16, (i // 7) * 16
        floor(L, ox, oy, {"floor_b": 1, "floor_c": 2}.get(k, 0))
        if k == "floor_cracked":
            for (x, y) in ((3, 2), (4, 3), (4, 4), (5, 5), (6, 5), (7, 6), (7, 7), (11, 9),
                           (12, 10), (12, 11), (13, 12)):
                L.px(ox + x, oy + y, "dk0")
        elif k == "bootprints":
            for bx, by in ((2, 2), (9, 7)):
                put(L, ox + bx, oy + by, [".11.", "1111", "1111", ".11.", "....", ".11.", ".11."],
                    {"1": "dk1"})
        elif k == "draught":
            for (x, y, n) in ((1, 3, 6), (5, 8, 7), (2, 12, 5), (9, 5, 5), (8, 13, 6)):
                for i2 in range(n):
                    L.px(ox + x + i2, oy + y, "du" if i2 % 3 else "dk3")
        elif k in ("seed", "seeds"):
            spots = [(6, 6)] if k == "seed" else [(3, 3), (9, 5), (5, 10), (11, 11), (7, 7)]
            for sx, sy in spots:
                for j, row in enumerate(SEED):
                    for i2, ch in enumerate(row):
                        if ch == "s":
                            L.px(ox + sx + i2, oy + sy + j, "dls")
        elif k == "chalk_fork":
            put(L, ox, oy + 5, [r.replace("s", "c") for r in [
                "..s.......s.....",
                "...s.....s......",
                "....s...s.......",
                ".....sss........",
                "......s.........",
                "......s.........",
                "......s.........",
            ]], {"c": "dlf"})
        elif k == "chalk_trail_h":
            for x in range(0, 16):
                if x % 4 != 3:
                    L.px(ox + x, oy + 8, "dlf")
            put(L, ox + 10, oy + 6, ["s.", ".s", "s."], {"s": "dlf"})
        elif k == "chalk_trail_v":
            for y in range(0, 16):
                if y % 4 != 3:
                    L.px(ox + 8, oy + y, "dlf")
            put(L, ox + 6, oy + 4, ["s.s", ".s."], {"s": "dlf"})
        elif k == "rubble":
            for (x, y, r) in ((5, 9, 4), (11, 10, 3), (8, 5, 3), (3, 12, 2)):
                for yy in range(-r, r + 1):
                    for xx in range(-r, r + 1):
                        if xx * xx + yy * yy * 1.4 <= r * r:
                            c = "dk4" if xx + yy < -1 else ("dk3" if xx + yy < 2 else "dk1")
                            L.px(ox + x + xx, oy + y + yy, c)
        elif k == "void":
            L.rect(ox, oy, 16, 16, "dk0")
        elif k == "floor_inlay":
            for x in range(16):
                for y in (5, 10):
                    L.px(ox + x, oy + y, "gb")
                if x % 4 in (1, 2):
                    L.px(ox + x, oy + 7, "ga")
                    L.px(ox + x, oy + 8, "gb")
    return s


# --------------------------------------------------------------------------
# Light: the ring of warmed floor round a lit brazier or torch
# --------------------------------------------------------------------------


def glow_ring():
    """Seven floor cells that sit round a lit 1 x 2 light (bowl over legs):
    left and right of the bowl (l0, r0) and the legs (l1, r1), and the row
    below (bl, b, br). The trial swaps them in when the light is lit."""
    names = {"l0": (0, 0), "r0": (2, 0), "l1": (0, 1), "r1": (2, 1),
             "bl": (0, 2), "b": (1, 2), "br": (2, 2)}
    big = Layer(48, 48)
    for cy in range(3):
        for cx in range(3):
            floor(big, cx * 16, cy * 16)
    lit_disc(big, 0, 0, 48, 48, 24, 17, 25)
    s = struct("glow", "Warmed floor round a lit light", 4, 2, walk=["....", "...."],
               names={"l0": (0, 0), "r0": (1, 0), "l1": (2, 0), "r1": (3, 0),
                      "bl": (0, 1), "b": (1, 1), "br": (2, 1), "pool": (3, 1)},
               notes="Swap these in round a brazier or torch when it lights, on cells that "
                     "hold plain `floor`; swap `floor` back when it goes out. Around a 1 x 2 "
                     "light at (x, y)-(x, y+1): `l0` (x-1, y), `r0` (x+1, y), `l1` (x-1, y+1), "
                     "`r1` (x+1, y+1), `bl` `b` `br` along row y+2. `pool` is floor warmed all "
                     "over, for a lit zone's heart.")
    for name, (gx, gy) in names.items():
        dx, dy = s.names[name]
        s.B.a[dy * 16:dy * 16 + 16, dx * 16:dx * 16 + 16] = big.a[gy * 16:gy * 16 + 16, gx * 16:gx * 16 + 16]
    pool = Layer(16, 16)
    floor(pool, 0, 0)
    for y in range(16):
        for x in range(16):
            pool.px(x, y, warm(pool.get(x, y), 2 if (x + y) % 5 else 1))
    s.B.a[16:32, 48:64] = pool.a
    return s


# --------------------------------------------------------------------------
# Walls: rim-lit top, the painted frieze, the lower wall
# --------------------------------------------------------------------------


def wall_top(L, ox, oy, side="M"):
    """The ceiling's dark over the wall, with the rim light that marks the
    wall line in the dark (SYSTEMS.md §2, readable darkness rule 2)."""
    for y in range(16):
        for x in range(16):
            c = "dk0" if y < 9 else ("dk1" if y < 12 else "dk2")
            if y == 12:
                c = "dk5" if x % 8 else "dk4"
            if y == 13:
                c = "dk4"
            if y in (14, 15):
                c = "dk3" if (x + y) % 6 else "dk2"
            L.px(ox + x, oy + y, c)
    if side in ("L", "R"):
        # the corner mitres into the side wall's rim
        sx = 12 if side == "L" else 3
        for y in range(0, 16):
            L.px(ox + sx, oy + y, "dk5" if y < 13 else "dk4")
            for x in (range(0, sx) if side == "L" else range(sx + 1, 16)):
                L.px(ox + x, oy + y, "dk0")


def side_wall(L, ox, oy, side):
    """The side walls seen from above: black beyond, a rim-lit edge."""
    for y in range(16):
        for x in range(16):
            if side == "L":
                c = "dk0" if x < 12 else ("dk5" if x == 12 else ("dk4" if x == 13 else "dk2"))
            else:
                c = "dk0" if x > 3 else ("dk4" if x == 3 else ("dk3" if x == 2 else "dk2"))
            L.px(ox + x, oy + y, c)


def lower_wall(L, ox, oy):
    """The wall's lower row: dressed blocks over a skirting."""
    for y in range(16):
        for x in range(16):
            course = y // 5
            joint = y % 5 == 4 or (x + course * 8) % 16 == 0
            c = "dk1" if joint else ("dk3" if y % 5 == 0 else "dk2")
            if y >= 13:
                c = ("dk4", "dk3", "dk1")[y - 13]
            L.px(ox + x, oy + y, c)


def frieze_ground(L, ox, oy):
    """The fresco band: lime plaster between ochre rules."""
    for y in range(16):
        for x in range(16):
            if y < 2 or y > 13:
                c = "dk3" if y in (1, 14) else "dk2"
            elif y in (2, 13):
                c = "fr"
            else:
                c = "fw"
            L.px(ox + x, oy + y, c)


# The Descent of Persephone, in eight panels (10 px tall, on the plaster)
FRESCO = {
    "maiden": [            # Persephone gathers flowers: the narcissus
        "....KK..........",
        "...KPPK.........",
        "...KKK..........",
        "..KYYYK.........",
        "..KYYYYPP.......",
        ".KYYYYYK...Y.Y..",
        ".KYYYYYY...G.G.Y",
        "KYYYYYYY...G.GYG",
        "KYYYYYYYK..G.G.G",
        ".KK..KK..GGGGGGG",
    ],
    "horses": [            # the earth opens: the black horses of Hades
        "..........KK....",
        ".........KKKK.K.",
        "....K...KKKKKKK.",
        "...KKKKKKKKK....",
        "..KKKKKKKKKK....",
        ".KKKKKKKKKK.....",
        "KK.K.KKKK.K.....",
        "K..K...K...K....",
        "RR.K..RK...KRRRR",
        "RRRRRRRRRRRRRRRR",
    ],
    "seized": [            # Hades in his chariot seizes her
        "...KK.......Y...",
        "..KKKK....YYPY..",
        "..KKKKKKKKKYY...",
        "...KKKK..KYYY...",
        "...KKKK..KYYYK..",
        "..KKKKKKKKKKKKK.",
        ".K..KKK......K..",
        "K.K.K.K.........",
        "K..KKK.K........",
        ".K.K.K..........",
    ],
    "search": [            # Demeter, veiled, searches with two torches
        "..R..........R..",
        ".RYR..KK....RYR.",
        "..K..KBBK....K..",
        "..K..KPPK....K..",
        "..KBBBBBBBBBBK..",
        "...KBBBBBBBK....",
        "....BBBBBBB.....",
        "....BBBBBBB.....",
        "...BBBBBBBBB....",
        "...KK.....KK....",
    ],
    "hecate": [            # Hecate meets her at the crossroads with her torches
        ".R..R...........",
        "RYRRYR....KK....",
        ".K..K....KRRK...",
        ".KKKK....KPPK...",
        "..KK...KRRRRRRK.",
        "..KK....KRRRRK..",
        "..KK....RRRRRR..",
        ".KKKK..RRRRRRRR.",
        ".K..K..RRRRRRRR.",
        "K....K..KK..KK..",
    ],
    "grief": [             # Demeter sits grieving by the Maiden's Well
        "................",
        ".....KK.........",
        "....KBBK........",
        "....KPPK........",
        "...KBBBBK.......",
        "...KBBBBBBK.....",
        "...KBBBBBBBK....",
        "..KKKKKKKKKKK...",
        "..KWWWWWWWWWK...",
        "..KKKKKKKKKKK...",
    ],
    "hermes": [            # Hermes leads Persephone up into the light
        ".KKK.......KK...",
        "KKKKK.....KPPK..",
        "..KPK.....KKK...",
        "..KKK.Y..KYYYK..",
        ".KKKKKY..KYYYYK.",
        "KKKKKKY.KYYYYYK.",
        "..KKK.Y.KYYYYYYK",
        "..K.K.Y.KYYYYYYK",
        ".K..K.Y.KYYYYYYK",
        "K....KY..KK..KK.",
    ],
    "return": [            # she returns, a pomegranate in hand; the wheat springs
        "....KK......Y.Y.",
        "...KPPK....YGYG.",
        "...KKK......G.G.",
        "..KYYYKRR...G.G.",
        "..KYYYYRR..YGYGY",
        ".KYYYYYK...G.G.G",
        ".KYYYYYY..YGYGYG",
        "KYYYYYYY...G.G.G",
        "KYYYYYYYK.GGGGGG",
        ".KK..KK..GGGGGGG",
    ],
}
FRESCO_LEGEND = {"K": "dk0", "P": "fp", "Y": "fy", "R": "fr", "B": "fb", "G": "fg", "W": "dk3"}


def frieze_cell(L, ox, oy, motif):
    frieze_ground(L, ox, oy)
    if motif in FRESCO:
        put(L, ox, oy + 3, FRESCO[motif], FRESCO_LEGEND)
    elif motif == "wheat":
        for x0 in (1, 9):
            put(L, ox + x0, oy + 3, [
                ".Y.Y.",
                "YKYKY",
                ".YKY.",
                "YKYKY",
                ".YKY.",
                "..K..",
                "..K..",
                ".GKG.",
                "..K..",
                "..K..",
            ], {"Y": "fy", "K": "fr", "G": "fg"})
    elif motif == "key":
        put(L, ox, oy + 4, [
            "KKKKKKK.KKKKKKK.",
            "K.....K.K.....K.",
            "K.KKK.K.K.KKK.K.",
            "K.K.K.KKK.K.K.KK",
            "K.K...K...K...K.",
            "K.KKKKK.K.KKKKK.",
            "K.......K.......",
            "KKKKKKKKKKKKKKKK",
        ], {"K": "fr"})


def wall_pieces():
    out = []
    top = ["top", "corner_l", "corner_r", "side_l", "side_r"]
    s = struct("wall", "Walls: the rim-lit top, corners, side walls, the lower wall", 8, 1,
               walk=["XXXXXXXX"],
               names={"top": (0, 0), "corner_l": (1, 0), "corner_r": (2, 0), "side_l": (3, 0),
                      "side_r": (4, 0), "lower": (5, 0), "lower_chalk": (6, 0),
                      "lower_cracked": (7, 0)},
               notes="A room shows three wall rows: `top` (the dark under the roof, its "
                     "rim-lit lip marking the wall in the dark), the frieze, then `lower`. "
                     "Side walls run down both edges of the map. `lower_chalk` carries "
                     "Hecate's chalk (latent: it glows when doused); `lower_cracked` is "
                     "for the Titans' wreck.")
    L = s.B
    wall_top(L, 0, 0)
    wall_top(L, 16, 0, "L")
    wall_top(L, 32, 0, "R")
    side_wall(L, 48, 0, "L")
    side_wall(L, 64, 0, "R")
    lower_wall(L, 80, 0)
    lower_wall(L, 96, 0)
    put(L, 99, 2, [
        "c.c.c...",
        ".ccc....",
        "..c.....",
        "..c..cc.",
        "..c.c..c",
        "..c..cc.",
    ], {"c": "dlc"})
    lower_wall(L, 112, 0)
    for (x, y) in ((116, 1), (117, 2), (117, 3), (118, 4), (119, 5), (119, 6), (120, 7), (121, 8)):
        L.px(x, y, "dk0")
    out.append(s)
    motifs = list(FRESCO) + ["wheat", "key"]
    s = struct("frieze", "The frieze: the Descent of Persephone", 5, 2, walk=["XXXXX", "XXXXX"],
               names={m: (i % 5, i // 5) for i, m in enumerate(motifs)},
               notes="The wall's middle row, painted round the hall. Read left to right: "
                     "`maiden` (she gathers the narcissus), `horses` (the earth opens), "
                     "`seized` (Hades's chariot), `search` (Demeter with her torches), "
                     "`hecate` (Hecate meets her), `grief` (Demeter at the Maiden's Well), "
                     "`hermes` (Hermes leads Persephone up), `return` (the pomegranate, and "
                     "the wheat springs). `wheat` and `key` are plain bands between the "
                     "scenes.")
    for i, m in enumerate(motifs):
        frieze_cell(s.B, (i % 5) * 16, (i // 5) * 16, m)
    out.append(s)
    return out


# --------------------------------------------------------------------------
# Wall lights, the revealed door, the niche
# --------------------------------------------------------------------------

SCONCE = [
    "......fff.......",
    ".....fFFFf......",
    ".....fFWFf......",
    "......fFf.......",
    ".....KbbbK......",
    ".....KbBbK......",
    "......KbK.......",
    "......KbK.......",
    ".....KKbKK......",
    ".....KbbbK......",
]
SCONCE_COLD = [
    "................",
    "................",
    "................",
    "......KaK.......",
    ".....KaaaK......",
    ".....KbBbK......",
    "......KbK.......",
    "......KbK.......",
    ".....KKbKK......",
    ".....KbbbK......",
]
SCONCE_LEGEND = {"f": "fx1", "F": "fx2", "W": "fx4", "K": "dk0", "b": "bz1", "B": "bz2",
                 "a": "ash"}


def wall_lights():
    s = struct("wall_lights", "Wall torches, the painted door, the niche", 8, 2,
               walk=["XXXX.XXX", "XXXXXXXD"],
               names={"sconce_cold": (0, 0), "sconce_lit": (1, 0), "niche_cold": (2, 0),
                      "niche_lit": (3, 0), "floor_sconce": (4, 0), "door_top_painted": (5, 0),
                      "door_top_open": (6, 0), "lower_lit": (7, 0),
                      "frieze_lit": (0, 1), "door_bottom_painted": (6, 1),
                      "door_bottom_open": (7, 1)},
               notes="Lower-wall cells. `sconce_lit` is `sconce_cold` + 1: a bronze torch "
                     "bracket, its flame warming the wall round it; put `floor_sconce` on "
                     "the floor cell below a lit sconce, and `lower_lit` / `frieze_lit` "
                     "beside it to spread the light. `niche_lit` is `niche_cold` + 1: a clay "
                     "lamp in a niche. The Reveal: `door_top_painted` (frieze row) over "
                     "`door_bottom_painted` (lower row) is a doorway painted in the fresco; "
                     "in a lit brazier's light swap each for its `_open` (painted + 1, the "
                     "bottom is MB_NON_ANIMATED_DOOR): a real door into the dark.")
    L, M = s.B, s.M
    lower_wall(L, 0, 0)
    put(M, 0, 3, SCONCE_COLD, SCONCE_LEGEND)
    lower_wall(L, 16, 0)
    lit_disc(L, 16, 0, 16, 16, 7, 3, 12)
    put(M, 16, 3, SCONCE, SCONCE_LEGEND)
    for ox, lit in ((32, False), (48, True)):
        lower_wall(L, ox, 0)
        if lit:
            lit_disc(L, ox, 0, 16, 16, 8, 6, 11)
        for y in range(3, 11):
            for x in range(4, 12):
                if y < 5 and (x - 7.5) ** 2 + (y - 5) ** 2 > 12:
                    continue
                L.px(ox + x, y, "dk1" if lit else "dk0")
        L.hline(ox + 3, ox + 12, 11, "dk4")
        put(M, ox + 5, 7, ["..f..", ".fWf.", "KbbbK", ".KKK."] if lit else
            [".....", ".....", "KbbbK", ".KKK."], {"f": "fx2", "W": "fx4", "K": "dk0", "b": "bz2"})
    floor(L, 64, 0)
    lit_disc(L, 64, 0, 16, 16, 8, -6, 16)
    # the doorway painted in the fresco, and the same opened
    frieze_ground(L, 80, 0)
    put(L, 80, 3, [
        "................",
        "....RRRRRRRR....",
        "....RYYYYYYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
    ], {"R": "fr", "Y": "fy", "K": "fb"})
    frieze_ground(L, 96, 0)
    put(L, 96, 3, [
        "................",
        "....KKKKKKKK....",
        "....K000000K....",
        "....K000000K....",
        "....K000000K....",
        "....K000000K....",
        "....K000000K....",
        "....K000000K....",
        "....K000000K....",
        "....K000000K....",
    ], {"K": "dk3", "0": "dk0"})
    lower_wall(L, 112, 0)
    lit_disc(L, 112, 0, 16, 16, -6, 3, 16)
    frieze_ground(L, 0, 16)
    lit_disc(L, 0, 16, 16, 16, 18, 14, 18)
    lower_wall(L, 96, 16)
    put(L, 96, 16, [
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYKKKKYR....",
        "....RYYYYYYR....",
        "....RRRRRRRR....",
    ], {"R": "fr", "Y": "fy", "K": "fb"})
    lower_wall(L, 112, 16)
    for y in range(0, 15):
        for x in range(4, 12):
            L.px(112 + x, 16 + y, "dk0")
        L.px(112 + 4, 16 + y, "dk3")
        L.px(112 + 11, 16 + y, "dk1")
    L.hline(116, 123, 31, "dk2")
    # unused cells in the second row: plain lower wall
    for ox in (16, 32, 48, 64, 80):
        lower_wall(L, ox, 16)
    s.names.update({"lower_2": (1, 1)})
    return s



# --------------------------------------------------------------------------
# Tiers, columns, braziers
# --------------------------------------------------------------------------


def tiers():
    """The rock-cut tiers along the hall's walls where the initiates stood:
    three rows of steps descending toward the floor."""
    s = struct("tiers", "The rock-cut tiers", 3, 3, walk=["...", "...", "..."],
               names={f"{r}_{c}": (i, j) for j, r in enumerate(("top", "mid", "low"))
                      for i, c in enumerate("LMR")},
               notes="Walkable steps, three rows: `top_*` against the wall, `low_*` meeting "
                     "the floor. L and R end each run with its cut side. Run them along the "
                     "north wall below the wall rows, as the Telesterion's were on all four "
                     "sides.")
    L = s.B
    for j in range(3):
        for i in range(3):
            ox, oy = i * 16, j * 16
            for y in range(16):
                for x in range(16):
                    r = y % 8
                    step = y // 8
                    # tread (lit nosing, worn top), then the riser in shadow
                    c = "dk5" if r == 0 else ("dk3" if r < 4 else ("dk2" if r < 6 else "dk1"))
                    if r == 1:
                        c = "dk4"
                    if r == 7:
                        c = "dk0"
                    if (x + step * 6 + j * 3) % 12 == 0 and 1 <= r <= 6:
                        c = "dk1"                   # the joint between two blocks
                    if r in (2, 3) and (x * 5 + y * 3 + j) % 13 == 0:
                        c = "dk2"                   # wear
                    L.px(ox + x, oy + y, c)
            if i == 0:
                for y in range(16):
                    L.px(ox, oy + y, "dk5" if y % 8 < 4 else "dk3")
                    L.px(ox + 1, oy + y, "dk4" if y % 8 < 4 else "dk2")
            elif i == 2:
                for y in range(16):
                    L.px(ox + 15, oy + y, "dk0")
                    L.px(ox + 14, oy + y, "dk1")
            if j == 2:
                for x in range(16):
                    L.px(ox + x, oy + 15, "dk1")
    return s


COLUMN = ["dk0", "dk3", "dk5", "dk4", "dk4", "dk3", "dk3", "dk2", "dk2", "dk1", "dk0"]


def column_cell(L, ox, oy, part, bg=True):
    if bg:
        floor(L, ox, oy)
    for y in range(16):
        for i, c in enumerate(COLUMN):
            L.px(ox + 3 + i, oy + y, c)
    if part == 0:
        L.hline(ox + 1, ox + 14, oy + 0, "dk0")
        L.hline(ox + 1, ox + 14, oy + 1, "dk5")
        L.hline(ox + 1, ox + 14, oy + 2, "dk3")
        L.hline(ox + 2, ox + 13, oy + 3, "dk0")
        L.hline(ox + 2, ox + 13, oy + 4, "dk4")
        L.px(ox + 1, oy + 1, "dk0")
        L.px(ox + 14, oy + 1, "dk0")
    else:
        # the base: a torus on a square plinth, its shadow on the floor
        L.hline(ox + 2, ox + 13, oy + 11, "dk0")
        L.hline(ox + 2, ox + 13, oy + 12, "dk4")
        L.hline(ox + 1, ox + 14, oy + 13, "dk0")
        L.hline(ox + 1, ox + 14, oy + 14, "dk3")
        L.hline(ox + 1, ox + 14, oy + 15, "dk0")


def columns():
    s = struct("columns", "The forest of columns", 5, 2, walk=["XXXXX", "XXXXX"],
               names={"top": (0, 0), "torch_cold": (1, 0), "torch_lit": (2, 0),
                      "broken_top": (3, 0), "drum": (4, 0), "bottom": (0, 1),
                      "bottom_b": (1, 1), "bottom_lit": (2, 1), "drum_b": (4, 1)},
               notes="A column is `top` over `bottom` (both block). `torch_lit` is "
                     "`torch_cold` + 1: an iron bracket and torch on the column; with it lit "
                     "put `bottom_lit` under it and the `glow` ring round it. `broken_top` "
                     "is a column the Titans cracked; `drum` and `drum_b` are fallen drums "
                     "on the floor (block).")
    L, M = s.B, s.M
    column_cell(L, 0, 0, 0)
    column_cell(L, 0, 16, 1)
    column_cell(L, 16, 16, 1)
    for ox, lit in ((16, False), (32, True)):
        floor(L, ox, 0)
        if lit:
            lit_disc(L, ox, 0, 16, 16, 8, 4, 16)
        column_cell(L, ox, 0, 0, bg=False)
        if lit:
            # the torch catches the column's near flank
            for y in range(5, 16):
                L.px(ox + 4, y, "dw4")
                L.px(ox + 5, y, "dw3")
                L.px(ox + 6, y, "dw3" if y % 3 else "dk4")
        put(M, ox + 4, 2, [
            "...fff..",
            "..fFWFf.",
            "..fFFFf.",
            "...KbK..",
            "...KbK..",
            ".KKKbKK.",
            ".K.....K",
        ] if lit else [
            "........",
            "........",
            "...KaK..",
            "...KbK..",
            "...KbK..",
            ".KKKbKK.",
            ".K.....K",
        ], {"f": "fx1", "F": "fx2", "W": "fx4", "K": "dk0", "b": "bz1", "a": "ash"})
    floor(L, 32, 16)
    lit_disc(L, 32, 16, 16, 16, 8, -8, 18)
    column_cell(L, 32, 16, 1, bg=False)
    for y in range(0, 11):
        L.px(32 + 4, 16 + y, "dw4")
        L.px(32 + 5, 16 + y, "dw3")
    # the broken column: snapped, its top jagged
    column_cell(L, 48, 0, 0)
    for y in range(0, 9):
        for x in range(0, 16):
            jag = [8, 7, 6, 7, 8, 6, 5, 6, 7, 8, 7, 6, 7, 8, 8, 7][x]
            if y < jag:
                L.px(48 + x, y, floor_px(x, y))
    for x in range(3, 14):
        jag = [8, 7, 6, 7, 8, 6, 5, 6, 7, 8, 7, 6, 7, 8, 8, 7][x]
        L.px(48 + x, jag, "dk5")
        L.px(48 + x, jag + 1, "dk4")
    floor(L, 48, 16)
    for y in range(16):
        for i, c in enumerate(COLUMN):
            L.px(48 + 3 + i, 16 + y, c)
    L.hline(48 + 2, 48 + 13, 16 + 11, "dk0")
    L.hline(48 + 2, 48 + 13, 16 + 12, "dk4")
    L.hline(48 + 1, 48 + 14, 16 + 13, "dk0")
    L.hline(48 + 1, 48 + 14, 16 + 14, "dk3")
    L.hline(48 + 1, 48 + 14, 16 + 15, "dk0")
    s.names["broken_bottom"] = (3, 1)
    # fallen drums: a round drum lying on its side, fluted
    for oy in (0, 16):
        floor(L, 64, oy)
        for y in range(16):
            for x in range(16):
                dx, dy = (x - 7.5) / 7, (y - 9) / 5
                if dx * dx + dy * dy <= 1:
                    c = COLUMN[min(10, max(0, int((dx + 1) * 5.5)))]
                    if y < 7:
                        c = "dk4" if c not in ("dk0",) else c
                    M.px(64 + x, oy + y, c)
        for y in range(16):
            for x in range(16):
                dx, dy = (x - 7.5) / 7, (y - 9) / 5
                if 1 < dx * dx + dy * dy <= 1.3:
                    M.px(64 + x, oy + y, "dk0")
    return s


BOWL = [
    "................",
    "................",
    "..KKKKKKKKKKKK..",
    ".KbBBBBBBBBBBbK.",
    "..KbbbbbbbbbbK..",
    "...KKbbbbbbKK...",
    ".....KbbbbK.....",
    "......KbbK......",
    "......KbbK......",
    ".....KbbbbK.....",
    "....KbK..KbK....",
    "...KbK....KbK...",
    "..KbK......KbK..",
    ".KbK........KbK.",
    "KbK..........KbK",
    "KK............KK",
]
FLAME = [
    ".......f........",
    "......fF..f.....",
    "...f..fFf.fF....",
    "..fF.fFWFfFf....",
    "..fFFFWWWFFf.f..",
    ".fFFWWWWWWFFfF..",
    ".fFWWWWWWWWFFf..",
    "..cccccccccccc..",
]
LEGS = [
    "......KbbK......",
    "......KbbK......",
    ".....KbBbbK.....",
    "....KbK..KbK....",
    "...KbK.KK.KbK...",
    "...KbK.Kb.KbK...",
    "..KbK..Kb..KbK..",
    "..KbK..Kb..KbK..",
    ".KKKK..KK..KKKK.",
    "................",
]
EMBERS = [
    "..aaaaaaaaaaaa..",
]
PLAQUE = {
    "vestibule": ["..K.K..", "...K...", "..KKK..", "...K..."],   # Hecate's crossroads
    "spring": [".K.K.", "KKKKK", ".KKK.", "..K.."],               # a flower
    "summer": [".K.K.", "..K..", ".K.K.", "..K.."],               # an ear of wheat
    "autumn": ["..K..", ".KKK.", "KKKKK", ".KKK."],               # the pomegranate
    "winter": ["K.K.K", ".KKK.", "..K..", "..K.."],               # a bare branch
}


def brazier_top(L, M, ox, oy, lit):
    floor(L, ox, oy)
    if lit:
        lit_disc(L, ox, oy, 16, 16, 8, 6, 15)
    rows = BOWL
    # the bowl sits in the lower half of the top cell; legs run into the cell below
    put(M, ox, oy + 9, rows[2:9], {"K": "dk0", "b": "bz1", "B": "bz3"})
    if lit:
        put(M, ox, oy + 2, FLAME, {"f": "fx1", "F": "fx2", "W": "fx3", "c": "coal"})
        M.px(ox + 7, oy + 6, "fx4")
        M.px(ox + 8, oy + 5, "fx4")
    else:
        put(M, ox, oy + 9, EMBERS, {"a": "ash"})


def brazier_legs(L, M, ox, oy, lit, plaque):
    floor(L, ox, oy)
    if lit:
        lit_disc(L, ox, oy, 16, 16, 8, -6, 18)
    put(M, ox, oy, LEGS, {"K": "dk0", "b": "bz1", "B": "bz2"})
    # a stone plinth with a bronze plaque
    M.hline(ox + 3, ox + 12, oy + 10, "dk0")
    for y in range(11, 15):
        for x in range(3, 13):
            M.px(ox + x, oy + y, "dk4" if y == 11 else ("dk3" if x < 11 else "dk2"))
        M.px(ox + 2, oy + y, "dk0")
        M.px(ox + 13, oy + y, "dk0")
    M.hline(ox + 2, ox + 13, oy + 15, "dk0")
    for y in range(11, 15):
        for x in range(5, 11):
            M.px(ox + x, oy + y, "bz2" if not lit else "bz3")
    glyph = PLAQUE[plaque]
    gw = len(glyph[0])
    put(M, ox + 8 - gw // 2, oy + 11, glyph, {"K": "bz0"})


def braziers():
    plaques = list(PLAQUE)
    w = 2 + 2 * len(plaques)
    names = {"top_cold": (0, 0), "top_lit": (1, 0)}
    for i, p in enumerate(plaques):
        names[f"{p}_cold"] = (2 + 2 * i, 0)
        names[f"{p}_lit"] = (3 + 2 * i, 0)
    s = struct("braziers", "Tripod braziers: the vestibule's and the four seasons'", 6, 2,
               walk=["XXXXXX", "XXXXXX"], names={},
               notes="A brazier is a bowl (`top_*`) over legs on a plinth whose bronze plaque "
                     "names it: `vestibule` (Hecate's crossroads), and the season braziers "
                     "of the hall's four quarters: `spring` (a flower), `summer` (an ear of "
                     "wheat), `autumn` (the pomegranate), `winter` (a bare branch). **Each "
                     "lit metatile is its cold one + 1.** Swap both cells together and keep "
                     "them impassable, then swap the `glow` ring in round it.")
    L, M = s.B, s.M
    cells = [("top", None)] + [(p, p) for p in plaques]
    k = 0
    for name, plaque in cells:
        for lit in (False, True):
            cx, cy = k % 6, k // 6
            ox, oy = cx * 16, cy * 16
            if name == "top":
                brazier_top(L, M, ox, oy, lit)
            else:
                brazier_legs(L, M, ox, oy, lit, plaque)
            s.names[f"{name}_{'lit' if lit else 'cold'}"] = (cx, cy)
            k += 1
    return s


def overturned():
    s = struct("overturned", "An overturned brazier, kicked over in the raid", 2, 1, walk=["XX"],
               notes="The Titans' wreck (STORY.md §6.2): a tripod on its side, its coals "
                     "spilled cold across the floor.")
    L, M = s.B, s.M
    floor(L, 0, 0)
    floor(L, 16, 0, 1)
    for (x, y) in ((18, 12), (21, 13), (24, 11), (27, 13), (23, 14), (29, 12), (20, 10)):
        M.px(x, y, "ash")
        M.px(x + 1, y, "dk0")
    put(M, 1, 3, [
        "..KK..........KK",
        ".KbbK....KKKKKbK",
        "KbBBbK..KbbbbbK.",
        "KbBBBbKKbbKKKK..",
        "KbBBBbbbbK......",
        ".KbBbbKKbbK.....",
        "..KbbK..KbbK....",
        "...KK....KK.....",
    ], {"K": "dk0", "b": "bz1", "B": "bz2"})
    for x in range(5, 12):
        M.px(x, 12, "ash" if x % 2 else "coal")
    return s


# --------------------------------------------------------------------------
# The draughty doorway, the Anaktoron, the throne and the dais
# --------------------------------------------------------------------------

RIBBONS_S = [
    "KKKKKKKKKKKKKKKK",
    "dKrKwKsKrKwKsKKd",
    "d.r.w.s.r.w.s..d",
    "d..r.w.s..r.w..d",
    "d..r..w.s.r..w.d",
    "d...r.w..s.r.w.d",
    "d...r..w.s..r..d",
    "d....r.w..s.r..d",
]
RIBBONS_N = [
    "KKKKKKKKKKKKKKKK",
    "dKrKwKsKrKwKsKKd",
    "d.r.w.s.r.w.s..d",
    "dr.w.s.r.w.s...d",
    "d.r.w.s.r.w.s..d",
    "dr.w.s.r.w.s...d",
    "d.r..w.s.r.w...d",
    "dr..w..s.r..w..d",
]


def partition():
    s = struct("partition", "Partition wall and the draughty doorway", 6, 1,
               walk=["XXX..X"],
               names={"W": (0, 0), "M": (1, 0), "E": (2, 0), "door_draught": (3, 0),
                      "door_draught_b": (4, 0), "post": (5, 0)},
               notes="A low wall across the hall, one row: `W` `M` ... `E`. The doorway's "
                     "ribbons stream through it on the draught (SYSTEMS.md §2, the wind verb: "
                     "it blows out a carried flame). `door_draught` streams south, "
                     "`door_draught_b` sways the other way: alternate them to make the "
                     "ribbons flutter. Both are walkable. `post` ends a wall standing alone.")
    L, M = s.B, s.M

    def wall(ox, side):
        for y in range(16):
            for x in range(16):
                if y < 4:
                    c = "dk4" if y == 0 else ("dk3" if y < 3 else "dk1")
                else:
                    joint = (y - 4) % 4 == 3 or (x + ((y - 4) // 4) * 6) % 12 == 0
                    c = "dk1" if joint else "dk2"
                    if y == 15:
                        c = "dk0"
                L.px(ox + x, y, c)
        if side == "W":
            for y in range(16):
                L.px(ox, y, "dk0")
                L.px(ox + 1, y, "dk5" if y < 4 else "dk3")
        elif side == "E":
            for y in range(16):
                L.px(ox + 15, y, "dk0")
                L.px(ox + 14, y, "dk1")
    wall(0, "W")
    wall(16, "M")
    wall(32, "E")
    for ox, rib in ((48, RIBBONS_S), (64, RIBBONS_N)):
        floor(L, ox, 0)
        for y in range(16):
            L.px(ox + 0, y, "dk3")
            L.px(ox + 15, y, "dk1")
        for x in range(1, 15):
            L.px(ox + x, 0, "dk4")
            L.px(ox + x, 1, "dk2")
        put(M, ox, 1, rib, {"K": "dk0", "r": "rbn", "w": "rbw", "s": "rbs", "d": "dk2"})
    wall(80, "W")
    for y in range(16):
        L.px(80 + 15, y, "dk0")
        L.px(80 + 14, y, "dk1")
    return s


def anaktoron():
    s = struct("anaktoron", "The Anaktoron: the inner shrine in the hall", 5, 3,
               walk=["XXXXX", "XXXXX", "XXDXX"],
               notes="The small, ancient stone house at the heart of the Telesterion, where "
                     "the holy things were kept. A rough slab roof, walls of old limestone "
                     "with a gilt band, and one door (MB_NON_ANIMATED_DOOR): warp to the "
                     "inner shrine, where Chloe waits. Put the Hierophant's `throne` on the "
                     "floor beside the door, as at Eleusis.")
    L = s.B
    W = 80
    for y in range(48):
        for x in range(W):
            if y < 14:
                # the roof: big slabs seen from above, rim-lit at the front edge
                slab = (x // 20 + (y // 7)) % 2
                c = "dk3" if slab else "dk2"
                if y % 7 == 0 or x % 20 == 0:
                    c = "dk1"
                if y == 12:
                    c = "dk5"
                elif y == 13:
                    c = "dk4"
            elif y < 17:
                c = "dk0" if y == 14 else "dk1"
            elif y in (24, 25):
                c = "gb" if y == 24 else "ga"           # the gilt band
            else:
                course = (y - 17) // 5
                joint = (y - 17) % 5 == 4 or (x + course * 7) % 14 == 0
                c = "dk1" if joint else ("dk4" if (x * 7 + y * 13) % 29 == 0 else "dk3")
                if y >= 45:
                    c = ("dk4", "dk2", "dk0")[y - 45]
            L.px(x, y, c)
    for y in range(48):
        L.px(0, y, "dk0")
        L.px(1, y, "dk5" if y >= 14 else "dk4")
        L.px(W - 1, y, "dk0")
        L.px(W - 2, y, "dk1")
    # the door: a dark opening under a gilt lintel, a lamp's glow within
    for y in range(32, 47):
        for x in range(36, 44):
            L.px(x, y, "dk0")
    L.hline(34, 45, 30, "ga")
    L.hline(34, 45, 31, "gb")
    for y in range(32, 47):
        L.px(35, y, "dk4")
        L.px(44, y, "dk1")
    L.px(39, 40, "dw2")
    L.px(40, 40, "dw3")
    L.px(39, 41, "dw1")
    return s


def throne():
    s = struct("throne", "The Hierophant's throne", 1, 2, walk=["X", "X"],
               notes="Marble, with a red cushion and gilt finials. Beside the Anaktoron's door.")
    floor(s.B, 0, 0)
    floor(s.B, 0, 16)
    put(s.M, 2, 2, [
        "K........K..",
        "KgK....KgK..",
        "K1K....K3K..",
        "K1KKKKKK3K..",
        "K11111113K..",
        "K12222223K..",
        "K12222223K..",
        "K12222223K..",
        "K11111113K..",
        "KrrrrrrrrK..",
        "KRRRRRRRRK..",
        "KRRRRRRRrK..",
        "K11111113K..",
        "K12222223K..",
        "K1K....K3K..",
        "K1K....K3K..",
        "K1KKKKKK3K..",
        "K44K..K44K..",
        "KKKK..KKKK..",
    ], {"K": "dk0", "g": "ga", "1": "mb1", "2": "mb2", "3": "mb3", "4": "mb4", "r": "rd1",
        "R": "rd2"})
    # shift the throne to centre it
    s.M.a[:, 2:] = s.M.a[:, :-2].copy()
    s.M.a[:, :2] = 0
    return s


def dais():
    s = struct("dais", "The Mystagogue's dais", 4, 2, walk=["...X", "XX.X"],
               names={"L": (0, 0), "M": (1, 0), "R": (2, 0), "altar_empty": (3, 0),
                      "riser_L": (0, 1), "riser_M": (1, 1), "steps": (2, 1), "riser_R": (3, 1)},
               notes="Marble floor (`L` `M` ... `R`, walkable) over a front riser (`riser_*`, "
                     "blocks) with `steps` up. `altar_empty` (blocks) is the altar the "
                     "Mysteries' last secret appears on: swap in the vessels set's "
                     "`altar_ear` for Chloe's reveal, a single reaped ear of grain "
                     "(METATILE_TempleDemeter_Altar_Empty / _Ear).")
    L = s.B
    for i in range(3):
        ox = i * 16
        for y in range(16):
            for x in range(16):
                c = "mb2" if (x + y) % 9 else "mb3"
                if y % 8 == 0 or x % 16 == 0:
                    c = "mb3"
                L.px(ox + x, y, c)
        if i == 0:
            for y in range(16):
                L.px(ox, y, "dk0")
                L.px(ox + 1, y, "mb1")
        if i == 2:
            for y in range(16):
                L.px(ox + 15, y, "dk0")
                L.px(ox + 14, y, "mb4")
    # risers
    for i, kind in enumerate(("L", "M", "steps", "R")):
        ox = i * 16
        for y in range(16):
            for x in range(16):
                if kind == "steps":
                    r = y % 5
                    c = "mb1" if r == 0 else ("mb2" if r < 3 else "mb4")
                else:
                    c = "mb1" if y == 0 else ("mb3" if y < 12 else "mb4")
                    if y == 15:
                        c = "dk0"
                L.px(ox + x, 16 + y, c)
        if kind == "L":
            for y in range(16):
                L.px(ox, 16 + y, "dk0")
        if kind == "R":
            for y in range(16):
                L.px(ox + 15, 16 + y, "dk0")
    # the altar on the dais, cold marble with a cloth laid ready
    ox = 48
    for y in range(16):
        for x in range(16):
            L.px(ox + x, y, "mb2" if (x + y) % 9 else "mb3")
    altar(s.M, ox, 0, ear=False)
    return s


def altar(M, ox, oy, ear):
    put(M, ox + 1, oy + 3, [
        "KKKKKKKKKKKKKK",
        "KwwwwwwwwwwwwK",
        "K11111111111bK",
        "K12222222223bK",
        "K12222222223bK",
        "K12222222223bK",
        "K13333333333bK",
        "K4444444444444",
        "KKKKKKKKKKKKKK",
    ], {"K": "dk0", "w": "fw", "1": "mb1", "2": "mb2", "3": "mb3", "4": "mb4", "b": "mb3"})
    if ear:
        put(M, ox + 2, oy + 1, [
            "....g.g......",
            "...gGgGg.....",
            "..gGgGgGkkkkk",
            "...gGgGg.....",
            "....g.g......",
        ], {"g": "ga", "G": "mb1", "k": "gb"})


# --------------------------------------------------------------------------
# Vessels, baskets, lamps, stairs, sentinels
# --------------------------------------------------------------------------


def vessels():
    keys = ["kykeon", "kylikes", "kernos", "kistai", "floor_spare", "liknon", "kiste_smashed",
            "lamp_cold", "lamp_lit", "altar_ear"]
    s = struct("vessels", "Kykeon, the sacred baskets, lamps", 5, 2,
               walk=["XXXX.", "XXXXX"],
               names={k: (i % 5, i // 5) for i, k in enumerate(keys)},
               notes="On the floor, all blocking. `kykeon` a krater of the barley-and-mint "
                     "drink the initiates broke their fast with; `kylikes` cups set out on a "
                     "board; `kernos` the many-cupped offering vessel; `kistai` two lidded "
                     "baskets of the holy things, tied with red fillets; `liknon` the "
                     "winnowing basket under its cloth; `kiste_smashed` one the Titans broke "
                     "open. `lamp_lit` is `lamp_cold` + 1: the one lamp on the steps in the "
                     "robbed Telesterion. `altar_ear` is the dais's `altar_empty` with the "
                     "single reaped ear of grain on it.")
    L, M = s.B, s.M
    for i in range(10):
        floor(L, (i % 5) * 16, (i // 5) * 16, i % 3)
    leg = {"K": "dk0", "0": "tk0", "1": "tk1", "2": "tk2", "m": "mint", "b": "barl",
           "w": "wc1", "W": "wc2", "r": "rbn", "v": "rbw", "s": "rbs", "g": "ga", "f": "fw"}
    put(M, 1, 2, [
        "..KKKKKKKKKK..",
        ".K2mbmbmbmb2K.",
        ".KK2222222KKK.",
        "K12K22222K21K.",
        "K1.K22222K.1K.",
        ".KK122222KKK..",
        "...K12221K....",
        "....K121K.....",
        "....K111K.....",
        "...KK000KK....",
        "...K00000K....",
        "...KKKKKKK....",
    ], leg)
    put(M, 17, 4, [
        "KKKK..KKKK....",
        "K22K..K22K.KKK",
        "K1mK..K1bK.K2K",
        ".KK....KK..K1K",
        "..K....K....K.",
        "KKKKKKKKKKKKKK",
        "KwwwwwwwwwwwwK",
        "KKKKKKKKKKKKKK",
    ], leg)
    put(M, 33, 3, [
        "...KK.KK.KK...",
        "..K2KK2KK2K...",
        ".KK1KK1KK1KK..",
        "K2K.K2222K.K2K",
        "K1KK222222KK1K",
        ".KK12222221KK.",
        "...K111111K...",
        "....K1111K....",
        "....KK00KK....",
        "...K000000K...",
        "...KKKKKKKK...",
    ], leg)
    for bx in (1, 8):
        put(M, 48 + bx, 3, [
            ".KKKKK.",
            "KWWWWWK",
            "KrrrrrK",
            "KwWwWwK",
            "KWwrwWK",
            "KwWrWwK",
            "KWwrwWK",
            "KwWwWwK",
            "KWWWWWK",
            ".KKKKK.",
        ], leg)
    put(M, 1, 19, [
        "...KKKKKKKK...",
        "..KffffffffK..",
        ".KffvffvfffK..",
        "KWffffffffffK.",
        "KwWfvffffvfWK.",
        "KWwWwWwWwWwK..",
        ".KwWwWwWwWK...",
        "..KKKKKKKK....",
    ], leg)
    put(M, 17, 18, [
        ".KKK..KK......",
        "KWWWK.KwK..K..",
        "KWr.WKKWK.KK..",
        "KW.r.WWwK.....",
        "KWwr.WwWK..gK.",
        ".KWwWwWK..K...",
        "..KKKKK.......",
        "......r.......",
        ".....r...r....",
    ], leg)
    for ox, lit in ((32, False), (48, True)):
        if lit:
            lit_disc(L, ox, 16, 16, 16, 8, 8, 13)
        put(M, ox + 3, 16 + 6, [
            "......f...",
            ".....fW...",
            "..KKKKKK..",
            ".K2222221K",
            "K22222211K",
            ".K111111K.",
            "..KKKKKK..",
        ] if lit else [
            "..........",
            "..........",
            "..KKKKKK..",
            ".K2222221K",
            "K22222211K",
            ".K111111K.",
            "..KKKKKK..",
        ], {**leg, "f": "rbs", "W": "fw"})
    # the altar with the ear of grain, on the dais's marble
    for y in range(16):
        for x in range(16):
            L.px(64 + x, 16 + y, "mb2" if (x + y) % 9 else "mb3")
    altar(M, 64, 16, ear=True)
    return s


def stairs():
    s = struct("stairs", "Stairs: up to the daylight, down to the crypt", 5, 1,
               walk=["SSSSD"],
               names={"up_L": (0, 0), "up_M": (1, 0), "up_R": (2, 0), "up_single": (3, 0),
                      "crypt": (4, 0)},
               notes="The megaron is underground: its way out is a stair rising south to the "
                     "temple above, lit by the daylight at its head. Put the stair on the "
                     "map's bottom row (`up_L` `up_M` ... `up_R`, or `up_single`); each cell "
                     "is MB_SOUTH_ARROW_WARP with a warp event, like a door mat. `crypt` is "
                     "the dark stair down past the sentinels (MB_NON_ANIMATED_DOOR).")
    L = s.B
    for i, k in enumerate(("L", "M", "R", "single")):
        ox = i * 16
        for y in range(16):
            for x in range(16):
                step = y // 4
                r = y % 4
                c = ("dk3", "dk4", "dw3", "dw4")[step] if r == 0 else \
                    ("dk2", "dk3", "dw2", "dw3")[step]
                if r == 3:
                    c = ("dk1", "dk2", "dw1", "dw2")[step]
                L.px(ox + x, y, c)
        if k in ("L", "single"):
            for y in range(16):
                L.px(ox, y, "dk0")
                L.px(ox + 1, y, "dk5")
        if k in ("R", "single"):
            for y in range(16):
                L.px(ox + 15, y, "dk0")
                L.px(ox + 14, y, "dk1")
    ox = 64
    floor(L, ox, 0)
    for y in range(2, 16):
        for x in range(2, 14):
            step = (y - 2) // 3
            r = (y - 2) % 3
            c = ("dk2", "dk1", "dk1", "dk0", "dk0")[min(step, 4)] if r == 0 else "dk0"
            L.px(ox + x, y, c)
        L.px(ox + 1, y, "dk4")
        L.px(ox + 14, y, "dk1")
    L.hline(ox + 1, ox + 14, 1, "dk4")
    return s


def sentinel():
    s = struct("sentinel", "A stone sentinel of the crypt", 1, 2, walk=["X", "X"],
               notes="Grey kouroi with blank eyes, who turn back the uninitiated (the Helm of "
                     "Darkness gate, SYSTEMS.md §1). Stand two either side of the crypt stair.")
    floor(s.B, 0, 0)
    floor(s.B, 0, 16)
    put(s.M, 3, 1, [
        "...KKKK...",
        "..K5544K..",
        "..K4KK4K..",
        "..K4443K..",
        "...K43K...",
        ".KK4443KK.",
        "K55444433K",
        "K54K44K33K",
        "K4K4443K3K",
        "K4K4443K3K",
        "K4K4433K3K",
        "KKK4433KKK",
        "..K4433K..",
        "..K4433K..",
        "..K443K...",
        "..K4K3K...",
        "..K4K3K...",
        "..K4K3K...",
        "..K4K3K...",
        "..K4K3K...",
        "..K4K3K...",
        ".KK4KK3K..",
        "KdddddddK.",
        "KddddddddK",
        "KKKKKKKKKK",
    ], {"K": "dk0", "5": "dk5", "4": "dk4", "3": "dk3", "d": "dk2"})
    return s



# --------------------------------------------------------------------------
# Hera's serpent pits (the Seat of Hera on Olympus borrows this set)
# --------------------------------------------------------------------------

PIT_COLS = ("l", "m", "r", "s")
SERPENT = [
    "....gg......",
    "...gGGg.....",
    "..gG..Gg.y..",
    "..gG...gGGg.",
    "...gGGGGGkg.",
    "....gggggg..",
]


def pit_cell(L, ox, oy, row, col, snake=False):
    """One cell of a sunken pit seen from above at 3/4: the far wall's face
    under a lit lip, black depth, thin side walls, and a near lip where the
    floor resumes. row: top/bot of a two-row pit, or one; col: l/m/r, or s
    for a one-wide pit."""
    L.rect(ox, oy, 16, 16, "dk0")
    for (x, y) in ((3, 9), (11, 12), (7, 14), (13, 6)):
        L.px(ox + x, oy + y, "dk1")
    if row in ("top", "one"):
        L.hline(ox, ox + 15, oy, "dk4")
        for y, c in ((1, "dk3"), (2, "dk2"), (3, "dk2"), (4, "dk1")):
            L.hline(ox, ox + 15, oy + y, c)
        for x in range(0, 16, 5):
            L.px(ox + x, oy + 2, "dk1")
    if col in ("l", "s"):
        L.vline(ox, oy, oy + 15, "dk2")
        L.vline(ox + 1, oy + (5 if row in ("top", "one") else 0), oy + 15, "dk1")
    if col in ("r", "s"):
        L.vline(ox + 15, oy, oy + 15, "dk3")
        L.vline(ox + 14, oy + (5 if row in ("top", "one") else 0), oy + 15, "dk2")
    if row in ("bot", "one"):
        L.hline(ox, ox + 15, oy + 15, "dk3")
    if snake:
        put(L, ox + 2, oy + (8 if row != "top" else 7), SERPENT,
            {"g": "fg", "G": "dk3", "y": "fy", "k": "dk0"})


def serpent_pits():
    names = {}
    order = ([("top", c, False) for c in PIT_COLS] + [("bot", c, False) for c in PIT_COLS]
             + [("one", c, False) for c in PIT_COLS]
             + [("bot", "l", True), ("bot", "s", True), ("one", "m", True), ("top", "m", True)])
    s = struct("serpent_pit", "Hera's serpent pits", 8, 2, walk=["XXXXXXXX", "XXXXXXXX"],
               notes="Sunken pits for the Seat of Hera, where Hera's serpents (the Hydra's "
                     "kin, Ladon's) keep their dens between the columns. Pieces by row "
                     "(`top`, `bot` of a two-row pit, or `one`) and column (`l`, `m`, `r`, "
                     "or `s` for a one-wide pit), e.g. `top_l`; `bot_l_snake`, "
                     "`bot_s_snake`, `one_m_snake` and `top_m_snake` show a coiled serpent.")
    L = s.B
    for i, (row, col, snake) in enumerate(order):
        ox, oy = (i % 8) * 16, (i // 8) * 16
        pit_cell(L, ox, oy, row, col, snake)
        names[f"{row}_{col}" + ("_snake" if snake else "")] = (i % 8, i // 8)
    s.names = names
    return s

def build():
    return [floor_pieces(), glow_ring(), *wall_pieces(), wall_lights(), tiers(), columns(),
            braziers(), overturned(), partition(), anaktoron(), throne(), dais(), vessels(),
            stairs(), sentinel(), serpent_pits()]
