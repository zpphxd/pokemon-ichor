#!/usr/bin/env python3
"""Draw the Temple of Hestia interior: the temple_hestia secondary tileset.

Doric, firelit and warm: a honey-marble floor with a Greek-key inlay, a red
wool runner, an ochre hall under a black-figure frieze, Doric columns, the
great round hearth with Hestia's flame, bronze tripod braziers (cold and lit),
the Hierophant's dais with its inner hearth, and the hymn's household: the
door, the table, the loom and the bed.

Every pixel is drawn here as a character grid (legend in COLORS). The script
lays the grids out into the three layer PNGs that Porytiles compiles:
  bottom.png  backgrounds (floor, wall, dais), always fully opaque
  middle.png  objects over the bottom layer; magenta is transparent
  top.png     unused, because nothing in the temple is drawn over sprites
So every metatile is COVERED, and its first layer is opaque. The engine never
shows the primary's backdrop color, or its "garbage" tile, through it.

The temple must render the same on any primary, since the Greek interior
primary is being drawn separately. So it uses only its own tiles and palettes
6-12. No color here appears in aethos, the primary Porytiles pairs it with, so
Porytiles cannot reuse a primary palette or tile. main() checks this.

Usage: /usr/bin/python3 tools/ichor/art/temple_hestia.py
Then run tools/ichor/art/temple_room.py, which compiles with Porytiles, checks
the result and renders the mock room.
"""
import csv
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "data/tilesets/secondary/temple_hestia/porytiles_src"
PRIMARY_PALS = ROOT / "data/tilesets/primary/aethos/porytiles_bin/palettes"
MAGENTA = (255, 0, 255)  # Porytiles' extrinsic transparency
FIRST_ID = 0x200         # NUM_METATILES_IN_PRIMARY
COLS = 8                 # metatiles per sheet row (128 px)

# --- Legend ---------------------------------------------------------------
# All values are multiples of 8, so they are exact in BGR555. The families are
# the master palette's (design/phase1/PLAN.md), shifted warm for a firelit room.
COLORS = {
    "K": (48, 24, 16),     # black-figure ink: outlines
    # white marble: columns, stele, dais, cornice, hearth ring
    "1": (248, 240, 224), "2": (232, 216, 192), "3": (200, 184, 160),
    "4": (160, 136, 120), "5": (112, 88, 80),
    # honey marble: the hall floor
    "a": (240, 216, 176), "b": (224, 192, 152), "c": (200, 160, 120),
    "d": (168, 128, 96),
    # the floor lit by the great hearth
    "l": (248, 224, 160), "m": (232, 176, 112),
    # red wool: runner, cord, blankets, cloth
    "r": (208, 72, 48), "s": (160, 40, 32), "t": (104, 24, 24),
    # gold thread and gilding
    "g": (240, 184, 72), "h": (192, 128, 40),
    # terracotta: the frieze ground, pots
    "w": (240, 168, 112), "x": (224, 128, 80), "y": (184, 80, 48),
    "z": (128, 48, 32),
    # ochre plaster
    "o": (232, 192, 128), "p": (208, 160, 96), "q": (168, 120, 72),
    # the dark under the roof
    "u": (64, 40, 32), "v": (96, 64, 48),
    # hearth bronze
    "B": (88, 48, 24), "C": (152, 96, 40), "D": (208, 152, 72),
    "E": (240, 200, 120),
    # fire, from the edge to the white-hot core
    "F": (176, 40, 16), "G": (232, 104, 24), "H": (248, 168, 40),
    "I": (248, 224, 96), "J": (248, 248, 200),
    # ash and char
    "A": (120, 104, 96), "N": (72, 56, 48),
    # olive wood
    "W": (96, 56, 32), "X": (144, 96, 56), "Y": (192, 144, 88),
    # laurel leaves
    "P": (56, 96, 48), "Q": (104, 144, 64), "R": (160, 184, 96),
}
CLEAR = "."

# The seven secondary palettes (slots 6-12), planned by hand. Every 8 x 8 tile
# of every layer uses colors from one of these; main() checks it. They go to
# Porytiles as packing hints, because its own search does not find a packing
# for this many colors in reasonable time.
PALETTES = {
    "floor": "abcdlmrstghKxyz",    # floor, firelight, runner, inlay, doormat
    "marble": "12345Kabcdrstgh",   # dais, steps, columns, stele
    "wall": "uvK1234opqwxyz",      # wall top, frieze, lower wall
    "fire": "K234BCDEFGHIJNA",     # hearths, braziers, bronze lamps
    "clay": "KwxyzPQRWXY2rs",      # amphorae, laurel, wreath, the table
    "cloth": "K1234uvWXYrstog",    # loom, bed niche, side door, cord
}

# A shadow darkens whatever it falls on by one step.
SHADE = {"a": "b", "b": "c", "c": "d", "l": "a", "m": "c", "1": "2", "2": "3",
         "3": "4", "4": "5", "r": "s", "s": "t", "g": "h"}
SHADOW = "c"  # the key objects use to mark their shadow on the ground


def g(*rows):
    """A character grid from rows of text; every row must be the same width."""
    width = len(rows[0])
    for r in rows:
        if len(r) != width:
            raise ValueError(f"grid row is {len(r)} wide, expected {width}: {r!r}")
    return np.array([list(r) for r in rows])


def blank(h=16, w=16, fill=CLEAR):
    return np.full((h, w), fill)


def over(dst, src, x=0, y=0):
    """Paint src onto dst at (x, y), skipping CLEAR pixels of src."""
    h, w = src.shape
    region = dst[y:y + h, x:x + w]
    mask = src[:region.shape[0], :region.shape[1]] != CLEAR
    region[mask] = src[:region.shape[0], :region.shape[1]][mask]
    return dst


def hflip(a):
    return a[:, ::-1].copy()


def vflip(a):
    return a[::-1, :].copy()


def recolor(a, table):
    out = a.copy()
    for k, v in table.items():
        out[a == k] = v
    return out


def tiles(canvas):
    """Cut a canvas into 16 x 16 metatile grids, row by row."""
    h, w = canvas.shape
    return [[canvas[y:y + 16, x:x + 16].copy() for x in range(0, w, 16)] for y in range(0, h, 16)]


# --- Floor -----------------------------------------------------------------

def slab(field="b", hi="a", lo="c", corner="d"):
    """One 16 px slab: lit top and left edges, a shaded joint bottom and right."""
    t = blank(fill=field)
    t[0, :15] = hi
    t[:15, 0] = hi
    t[15, 1:] = lo
    t[1:, 15] = lo
    t[0, 15] = field
    t[15, 0] = field
    t[15, 15] = corner
    return t


VEINS = [
    None,
    g(
        "................",
        "................",
        "..........a.....",
        ".........ac.....",
        "........ac......",
        ".......c........",
        "......c.........",
        ".....ac.........",
        "....a...........",
        "................",
        "................",
        "................",
        "............c...",
        "...........c....",
        "................",
        "................",
    ),
    g(
        "................",
        "................",
        "................",
        "...a............",
        "....c...........",
        "....c....a......",
        ".....c..........",
        "......cc........",
        "........c.......",
        "........ac......",
        "..........c.....",
        "...........c....",
        "................",
        "................",
        "................",
        "................",
    ),
]


def floor(variant=0):
    t = slab()
    if VEINS[variant] is not None:
        over(t, VEINS[variant])
    return t


def dais_slab():
    """Polished white marble: a lit top edge and a fine joint, with a faint
    vein, so the dais reads as one stone floor rather than a grid."""
    t = blank(fill="2")
    t[0, :15] = "1"
    t[15, :] = "3"
    t[:, 15] = "3"
    for x, y in ((4, 5), (5, 5), (11, 10)):
        t[y, x] = "3"
    t[4, 4] = "1"
    return t


# The red wool runner, one tile wide: gold borders and a gold lozenge per tile.
# Columns: 0 floor edge | 1 selvage | 2-3 gold | 4 lit wool | 5-11 wool |
# 12-13 gold | 14 selvage | 15 floor joint.
LOZENGE = g(
    "..gh..",
    ".gssh.",
    "gsrrsh",
    "gsrrsh",
    ".gssh.",
    "..hh..",
)


def runner(bg=None):
    t = floor() if bg is None else bg.copy()
    for y in range(16):
        t[y, 1:15] = list("tghrssssssshgt")
    over(t, LOZENGE, 5, 5)
    t[0, 7:9] = "g"
    t[15, 7:9] = "h"
    return t


def runner_end(bg=None):
    """The runner's south end: a gold hem and a wool fringe on the floor."""
    t = floor() if bg is None else bg.copy()
    r = runner()
    t[0:9, 1:15] = r[0:9, 1:15]
    t[9, 1:15] = list("tggggggggggggt")
    t[10, 1:15] = list("thhhhhhhhhhhht")
    t[11, 1:15] = list("tttttttttttttt")
    for x in range(2, 14, 2):
        t[12, x] = "r"
        t[13, x] = "s"
    return t


def runner_end_north(bg):
    """The north end: the south end turned around, on bg."""
    t = vflip(runner_end(vflip(bg)))
    # Keep the gold hem lit from above.
    t[6, 1:15] = list("tggggggggggggt")
    return t


# Greek key, as on the pottery dialogue frame (tools/ichor/art/ui_frames.py):
# one 5 px hook every 8 px, so the floor and the UI share one motif.
MEANDER = [
    "#####.##",
    "....#.#.",
    ".####.#.",
    ".#....#.",
    ".######.",
]
SALTIRE = [
    "#########",
    "##.....##",
    "#.#...#.#",
    "#..#.#..#",
    "#...#...#",
    "#..#.#..#",
    "#.#...#.#",
    "##.....##",
    "#########",
]
INLAY_LINE, INLAY_KEY = "c", "d"


def band_h():
    t = blank()
    t[4, :] = INLAY_LINE
    t[12, :] = INLAY_LINE
    for y, row in enumerate(MEANDER):
        for x in range(16):
            if row[x % 8] == "#":
                t[6 + y, x] = INLAY_KEY
    return t


def band_corner():
    """The inlay frame's top-left corner: a saltire square, the bands leaving
    it to the right and downward."""
    t = blank()
    for y, row in enumerate(SALTIRE):
        for x, ch in enumerate(row):
            if ch == "#":
                edge = x in (0, 8) or y in (0, 8)
                t[4 + y, 4 + x] = INLAY_LINE if edge else INLAY_KEY
    t[4, 13:] = INLAY_LINE
    t[12, 13:] = INLAY_LINE
    t[13:, 4] = INLAY_LINE
    t[13:, 12] = INLAY_LINE
    return t


def inlay(kind):
    t = floor()
    if kind == "h":
        over(t, band_h())
    elif kind == "v":
        over(t, band_h().T.copy())
    else:
        c = band_corner()
        if "r" in kind:
            c = hflip(c)
        if "b" in kind:
            c = vflip(c)
        over(t, c)
    return t


# --- The hearth's light on the floor ----------------------------------------

WARM = {"a": "l", "b": "a", "c": "b", "d": "c", "s": "r", "t": "s", "h": "g"}
HOT = {"a": "l", "b": "l", "c": "m", "d": "c", "s": "r", "t": "s", "h": "g"}


def firelight(canvas, cx, cy, rx, ry):
    """Warm the floor around a fire: two rings of light, each eased in with a
    narrow checkerboard instead of a noisy dither."""
    out = canvas.copy()
    h, w = canvas.shape
    for y in range(h):
        for x in range(w):
            d = np.hypot((x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry)
            v = (1.0 - d) * 3.0
            level = int(np.floor(v + (0.25 if (x + y) % 2 else -0.25)))
            ch = canvas[y, x]
            if level >= 2:
                out[y, x] = HOT.get(ch, ch)
            elif level >= 1:
                out[y, x] = WARM.get(ch, ch)
    return out


# --- Walls -------------------------------------------------------------------
# A Gen 3 room shows three wall rows: the wall top (roof shadow and cornice),
# the painted frieze, and the lower wall down to the floor.

def wall_top():
    t = blank()
    prof = "uuuuuuvvK12xx34K"
    for y, ch in enumerate(prof):
        t[y, :] = ch
    # Dentils under the cornice: blocks with dark gaps.
    for x in range(16):
        m = x % 4
        t[11, x] = "u" if m == 3 else ("2" if m < 2 else "3")
        t[12, x] = "u" if m == 3 else ("3" if m < 2 else "4")
    return t


def side_wall(right=False):
    """The side wall's top seen from above: the wall top turned on its side."""
    t = wall_top().T.copy()
    return hflip(t) if right else t


def wall_corner(right=False):
    """The wall top meeting a side wall, the cornice mitred at 45 degrees."""
    top, side = wall_top(), side_wall()
    t = blank()
    for y in range(16):
        for x in range(16):
            t[y, x] = top[y, x] if y < x else side[y, x]
    return hflip(t) if right else t


def frieze(motif):
    """The painted frieze: black-figure on terracotta between marble fillets."""
    t = blank(fill="x")
    for y, ch in enumerate("23Ky" + "x" * 8 + "yK24"):
        t[y, :] = ch
    if motif is not None:
        over(t, motif, 0, 3)
    return t


F_KEY = blank(10, 16)
for _y, _row in enumerate(MEANDER):
    for _x in range(16):
        if _row[_x % 8] == "#":
            F_KEY[2 + _y, _x] = "K"

F_PALMETTE = g(
    "................",
    "......K..K......",
    "...K..K..K..K...",
    "...KK.KKKK.KK...",
    "....KKKKKKKK....",
    "..KK.KKwwKK.KK..",
    "...KKKKKKKKKK...",
    ".......KK.......",
    ".....KKKKKK.....",
    "................",
)
F_FLAME = g(
    "................",
    "........K.......",
    ".......KK..K....",
    "......KwK.KK....",
    "......KwwKK.....",
    ".......KKK......",
    ".....KKKKKKK....",
    "......K.K.K.....",
    ".....KKKKKKK....",
    "................",
)
F_AMPHORA = g(
    "................",
    "......KKKK......",
    ".......KK.......",
    ".....K.KK.K.....",
    ".....KKKKKK.....",
    "......KwwK......",
    "......KKKK......",
    ".......KK.......",
    "......KKKK......",
    "................",
)
# Hestia enthroned and veiled, holding out a phiale toward her altar, in added
# white for her face and arm as the Attic painters did for women.
F_HESTIA_L = g(
    "................",
    ".......KKK......",
    "......KKK22.....",
    "...K..KKKK2.....",
    "...K.KKKKK222K..",
    "...K.KKKKK..KK..",
    "...KKKKKKKKKK...",
    "...K.KKKKK.KK...",
    "...K.......KK...",
    "..KK.......KKK..",
)
F_HESTIA_R = g(
    "................",
    ".........K......",
    "........KK..K...",
    ".......KwK.KK...",
    ".......KwwKK....",
    "........KKK.....",
    "......KKKKKKK...",
    ".......K.K.K....",
    "......KKKKKKK...",
    "................",
)


def lower_wall():
    t = blank(fill="o")
    for y, ch in enumerate("pop" + "o" * 6 + "zyyyz34"):
        t[y, :] = ch
    for x, y in ((3, 5), (11, 7), (7, 4), (14, 6), (1, 8)):
        t[y, x] = "p"
    return t


def void():
    """The dark outside the room, for the map border. A faint weave keeps it
    from matching a solid tile in some primary, which Porytiles would reuse."""
    t = blank(fill="K")
    for y in range(16):
        for x in range(16):
            if (x + 2 * y) % 8 == 0:
                t[y, x] = "u"
    return t


# --- Dais ----------------------------------------------------------------------

SUN = g(
    "......g.......",
    "...g..gh..g...",
    "....g.gh.g....",
    ".....ggh......",
    "..ggggg11hhh..",
    "..hhhh11hggg..",
    "......ghh.....",
    "....h.gh.h....",
    "...h..gh..h...",
    ".......h......",
)


def dais(sun=False):
    t = dais_slab()
    if sun:
        over(t, SUN, 1, 3)
    return t


def dais_edge(right=False):
    t = dais()
    if right:
        t[:, 15] = "K"
        t[:, 14] = "4"
    else:
        t[:, 0] = "K"
        t[:, 1] = "1"
    return t


def riser(end=None):
    """The dais front: the marble lip, a face of blocks, its shadow."""
    t = floor()
    for y, ch in enumerate("21K2333333" "4Kdc"):
        t[y, :] = ch
    t[4:10, 7] = "4"
    t[4:10, 15] = "4"
    if end == "l":
        t[0:12, 0] = "K"
        t[0:3, 1] = "1"
    elif end == "r":
        t[0:12, 15] = "K"
        t[0:3, 14] = "3"
    return t


def steps(with_runner=True):
    """Two steps up to the dais, optionally with the runner climbing them."""
    t = floor()
    prof = "21K442133442133K"
    for y, ch in enumerate(prof[:14]):
        t[y, :] = ch
    t[14, :] = "d"
    t[0:14, 0] = "K"
    t[0:14, 15] = "K"
    if with_runner:
        wool = {"2": "r", "1": "r", "3": "s", "4": "t", "K": "t"}
        for y in range(14):
            base = t[y, 5]
            lit = base in "12"
            t[y, 1] = "t"
            t[y, 2] = "g" if lit else "h"
            t[y, 3] = "h"
            t[y, 4:12] = wool.get(base, "s")
            t[y, 12] = "h"
            t[y, 13] = "g" if lit else "h"
            t[y, 14] = "t"
        t[14, 1:15] = "t"
        t[15, 1:15] = list("tghrsssssssshg")[:14]
        t[15, 14] = "t"
    return t


# --- Doormat: the exit warp ----------------------------------------------------

def mat(part):
    """A woven threshold mat in terracotta and gold: part l, m, r or single."""
    t = floor()
    x0 = 1 if part in ("l", "single") else 0
    x1 = 15 if part in ("r", "single") else 16
    t[3:16, x0:x1] = "y"
    for y in range(6, 13):
        for x in range(x0, x1):
            if (x + y) % 4 == 0:
                t[y, x] = "x"
            elif (x - y) % 4 == 0:
                t[y, x] = "z"
    t[3, x0:x1] = "K"
    t[4, x0:x1] = "g"
    t[5, x0:x1] = "h"
    t[13, x0:x1] = "h"
    t[14, x0:x1] = "g"
    t[15, x0:x1] = "z"
    if part in ("l", "single"):
        t[3:16, x0] = "K"
        t[4:15, x0 + 1] = "g"
    if part in ("r", "single"):
        t[3:16, x1 - 1] = "K"
        t[4:15, x1 - 2] = "h"
    return t


# --- Objects: the middle layer ---------------------------------------------------

COLUMN = g(
    ".KKKKKKKKKKKKKK.",
    ".K111111111112K.",
    ".K222222222333K.",
    ".KKKKKKKKKKKKKK.",
    "..K1122222334K..",
    "...K12222334K...",
    "...K22222334K...",
    "...KKKKKKKKKK...",
    "...K12123234K...",
    "...K44444444K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234K...",
    "...K12123234Kc..",
    "...K12123234Kcc.",
    "...K22223344Kcc.",
    "....KKKKKKKKccc.",
    ".....cccccccc...",
)

# A Doric half-column set into the wall, its capital under the cornice.
PILASTER = g(
    "..KKKKKKKKKKKK..",
    "..K1111111112K..",
    "..KKKKKKKKKKKK..",
    "...K11222334K...",
    "....K122334K....",
    "....KKKKKKKK....",
    "....K121234K....",
    "....K444444K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "....K121234K....",
    "...KK222334KK...",
    "...K11222334K...",
    "...K33333344K...",
    "...KKKKKKKKKK...",
)

# The stele with the Hymn of the Hearth, just inside the door.
STELE = g(
    "................",
    ".......KK.......",
    "......K12K......",
    ".....K1223K.....",
    "....K112233K....",
    "...K11222334K...",
    "..KKKKKKKKKKKK..",
    "..K1111111123K..",
    "..KKKKKKKKKKKK..",
    "...K22222223K...",
    "...K2K5K55K3K...",
    "...K22222223K...",
    "...K25K5K553K...",
    "...K22222223K...",
    "...K2K55K5K3K...",
    "...K22222223K...",
    "...K255K5K53K...",
    "...K22222223K...",
    "...K2K5K55K3K...",
    "...K22222223K...",
    "...K25K55K53K...",
    "...K22222223K...",
    "...K2K5K5553K...",
    "...K22222333K...",
    "..KKKKKKKKKKKK..",
    "..K1111111123K..",
    "..K2222222334K..",
    "..K3333333444K..",
    "..KKKKKKKKKKKKc.",
    "...cccccccccccc.",
    "................",
    "................",
)

# A bronze tripod: a deep bowl on three splayed legs with lion feet, on a low
# marble plinth whose bronze plaque names the station. Rows 0-15 are the bowl
# tile and rows 16-31 the leg tile; legs and the plaque's glyph are added in
# brazier().
BRAZIER = g(
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "...KKKKKKKKKK...",
    "..KDNNANNANNDK..",
    ".KEEDDDDDDDDDCK.",
    ".KKKKKKKKKKKKKK.",
    "..KEDDDDDDCCBK..",
    "..KDDDDDCCCBBK..",
    "...KDDDCCCBBK...",
    "....KKDCCBKK....",
    "......KDBK......",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "KKKKKKKKKKKKKKKK",
    "K22222222222223K",
    "KKKKKKKKKKKKKKKK",
    "K333DDDDDDDD333K",
    "K333DDDDDDDD333K",
    "K333DDDDDDDD333K",
    "K444DDDDDDDD444K",
    "KKKKKKKKKKKKKKKK",
)
# Where each of the outer legs crosses rows 15-23: the left leg's x (the
# right leg mirrors it), from the bowl's knob out to the feet.
TRIPOD_LEFT = [6, 6, 5, 5, 4, 4, 3, 3, 2]


def tripod():
    """Rows 15-23 of the brazier: two splayed legs and the back leg."""
    t = blank(9, 16)
    for j, xl in enumerate(TRIPOD_LEFT):
        t[j, xl] = "D"
        t[j, 15 - xl] = "C"
        t[j, 7] = "C"
        t[j, 8] = "B"
    out = t.copy()
    for j in range(9):
        for x in range(16):
            if t[j, x] != CLEAR:
                for dx in (-1, 1):
                    if 0 <= x + dx < 16 and t[j, x + dx] == CLEAR:
                        out[j, x + dx] = "K"
    # Lion feet on the plinth.
    out[8] = list(".KEDK.KCBK.KCBK.")
    return out

BRAZIER_FLAME = g(
    "......F.........",
    ".....FF.....F...",
    ".....FGF...FF...",
    "..F.FGHGF.FGF...",
    "..FFGHIHGFGHF.F.",
    ".FGGHIIIHGHIHFF.",
    ".FGHIIJJIIHIIGF.",
    ".KFGHIJJJIIIHGK.",
)

# The four stations of the hymn, plus Hestia's flame for the dais pair:
# 6 x 4 glyphs incised in a bronze plaque.
GLYPHS = {
    "door": g(
        "KKKKKK",
        ".K..K.",
        ".K..K.",
        ".K..K.",
    ),
    "table": g(
        "..KK..",
        ".KKKK.",
        "KK..KK",
        "KKKKKK",
    ),
    "loom": g(
        "..K...",
        ".KKK..",
        "..K...",
        "..K...",
    ),
    "bed": g(
        "K.....",
        "K.KK..",
        "KKKKKK",
        "K....K",
    ),
    "hearth": g(
        "..K...",
        ".KK.K.",
        ".KKKK.",
        "KKKKKK",
    ),
}
def brazier(lit, glyph):
    b = BRAZIER.copy()
    over(b, tripod(), 0, 15)
    over(b, GLYPHS[glyph], 5, 27)
    if lit:
        # Coals in the bowl, firelight on the bronze, flames above.
        b[7] = list("..KGHIHHGHIGHK..")
        b[8] = list(".KEEEDDDDDDDDCK.")
        b[10] = list("..KEEDDDDDCCBK..")
        b[11] = list("..KEDDDDCCCBBK..")
        over(b, BRAZIER_FLAME, 0, 0)
        b[12:31] = recolor(b[12:31], {"B": "C", "D": "E"})
        b[25] = list("K2222IIIIII2223K")
    return b


# The cord across the dais approach: a red-and-white woolen fillet, the sign
# of a closed sacred place. It burns away when the dais braziers flare.
def cord():
    """A twisted red-and-white rope sagging between the two bowls, with a
    wool tassel at its lowest point."""
    t = blank()
    for x in range(16):
        u = (x + 0.5 - 8) / 8
        y = int(round(6 + 4 * (1 - u * u)))
        t[y - 1, x] = "K"
        t[y, x] = "r" if (x + y) % 3 else "2"
        t[y + 1, x] = "s" if (x + y + 1) % 3 else "2"
        t[y + 2, x] = "K"
    tassel = g(
        ".K.",
        "KrK",
        "KrK",
        "rsr",
        "K.K",
    )
    over(t, tassel, 7, 11)
    return t

AMPHORA = g(
    "......KKKK......",
    ".....KxwxyK.....",
    "......KxyK......",
    "....KKKxyKKK....",
    "...K.KwxxyK.K...",
    "...K.KwxxxyK.K..",
    "....KKKKKKKKK...",
    "....KwKKKKKyK...",
    "....KKK2KKKKK...",
    "....KwKKKKKyK...",
    "....KKKKKKKKK...",
    ".....KwxxxyK....",
    "......KxxyK.....",
    "......KyyzK.....",
    ".....KKKKKKK....",
    "......ccccccc...",
)
# A red-figure pair: the clay shows through the black glaze.
AMPHORA_RED = g(
    "......KKKK......",
    ".....KKKKKK.....",
    "......KKKK......",
    "....KKKKKKKK....",
    "...K.KKKKKKK.K..",
    "...K.KKwxKKK.K..",
    "....KKwxxyKKK...",
    "....KKxxwxyKK...",
    "....KKxyxxyKK...",
    "....KKKxyyKKK...",
    "....KKKKKKKKK...",
    ".....KKKKKKK....",
    "......KKKKK.....",
    "......KyyzK.....",
    ".....KKKKKKK....",
    "......ccccccc...",
)

# A potted laurel, two tiles tall.
LAUREL = g(
    "................",
    ".....K.KK.......",
    "....KQKRQK.KK...",
    "...KRQKQPKKQRK..",
    "..KQRQPKQPQRQK..",
    "..KRQPQKRQPQPK..",
    ".KQQPKQRQPKQRPK.",
    ".KRQPQPQPQPQPQK.",
    "..KPQRQPKQRQPK..",
    ".KQPQPQPQPQPQPK.",
    "..KPKQPQPQPKPK..",
    "...KK.KPPK.KK...",
    "......KWXK......",
    "......KWXK......",
    "......KWXK......",
    ".....KKWXKK.....",
    "...KKKKKKKKKK...",
    "...KwxxxxxyyK...",
    "...KKKKKKKKKK...",
    "....KxxxxxyK....",
    "....KwKKKKyK....",
    "....KxK2KKyK....",
    "....KwKKKKyK....",
    "....KxxxxyyK....",
    ".....KxxxyK.....",
    ".....KyyyzK.....",
    "....KKKKKKKK....",
    ".....cccccccc...",
    "................",
    "................",
    "................",
    "................",
)

# Three bronze oil lamps burning on a low offering step.
VOTIVE = g(
    "................",
    "................",
    "...J......J.....",
    "..JI.....IJ.....",
    "..IH..J..HI.....",
    "..KH.IJ..HK.....",
    ".KDCK.IH.KDCK...",
    "KEDDCKHK.KEDCBK.",
    ".KKKKKDCK.KKKK..",
    "....KEDDCBK.....",
    "..KKKKKKKKKKKK..",
    "..K2222222223K..",
    "..K3333333344K..",
    "..KKKKKKKKKKKK..",
    "...cccccccccccc.",
    "................",
)

# A laurel wreath tied with a red ribbon, hung on the wall.
WREATH = g(
    "................",
    "......KQKK......",
    "....KQRK.KQK....",
    "...KRQK...KQK...",
    "..KQPK.....KPK..",
    "..KRK.......KQK.",
    "..KQK.......KRK.",
    "..KPQK.....KQPK.",
    "...KQRK...KPQK..",
    "....KQPKrKQRK...",
    "......KKrKK.....",
    ".......KsrK.....",
    "......KrK.Kr....",
    "......Ks...sK...",
    "................",
    "................",
)

# Votive lamps burning on a marble ledge along the wall.
LAMP_LEDGE = g(
    "................",
    "................",
    "..J.....J.....J.",
    ".JI....IJ....JI.",
    ".IH....HI....IH.",
    ".KHK..KHK...KHK.",
    "KDCBKKEDCK.KDCBK",
    ".KKKK.KKKK..KKKK",
    "KKKKKKKKKKKKKKKK",
    "2222222222222233",
    "3333333333333344",
    "KKKKKKKKKKKKKKKK",
    ".44..........44.",
    "..4..........4..",
    "................",
    "................",
)


# --- The great hearth (3 x 3) ---------------------------------------------------

HEARTH_FLAME = g(
    "............F...........",
    "............FF..........",
    "...........FGF..........",
    "...........FGF......F...",
    "..........FGGF......FF..",
    "..........FGHGF....FGF..",
    "....F.....FGHGF....FGF..",
    "....FF...FGHHGF...FGGF..",
    "...FGF...FGHIHGF..FGHF..",
    "...FGF..FGHHIHGF.FGHGF..",
    "...FGGF.FGHIIIHGFFGHGF..",
    "..FGHGFFGHHIJIHHGFGHHGF.",
    "..FGHHGGGHIIJIIHGGHIHGF.",
    ".FGGHHGHHIIJJIIHGHHIHGF.",
    ".FGHHIHHIIJJJJIIHHIIHGF.",
    ".FGHIIHIIJJJJJJIIHIIHGGF",
    "FGHHIIIIJJJJJJJJIIIIHHGF",
    "FGHHIIIJJJJJJJJJJIIIHHGF",
    "FGHIIIJJJJJJJJJJJJIIHHGF",
    "FGHIIIJJJJJJJJJJJJIIIHGF",
    "FGHHIIIJJJJJJJJJJIIIHHGF",
    ".FGHIIIIJJJJJJJJIIIIHGF.",
    ".FGHHIIIIJJJJJJIIIIHHGF.",
    "..FGHHIIIIIIIIIIIIHHGF..",
)


def great_hearth():
    """48 x 48: a stone ring clad in bronze, a bed of coals, Hestia's flame."""
    size = 48
    t = blank(size, size)
    cx, cy = 24.0, 30.0
    rxo, ryo = 22.5, 12.5
    rxi, ryi = 15.5, 7.5
    face = 6

    def ell(x, y, rx, ry):
        return ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2

    # The bronze-clad front of the ring: the rim's ellipse swept downward.
    for y in range(size):
        for x in range(size):
            inside = ell(x, y, rxo, ryo) <= 1.0
            swept = any(ell(x, y - k, rxo, ryo) <= 1.0 for k in range(1, face + 1))
            if swept and not inside and y + 0.5 > cy:
                u = (x + 0.5 - (cx - rxo)) / (2 * rxo)
                t[y, x] = "D" if u < 0.25 else ("C" if u < 0.72 else "B")
    for x in range(size):
        col = [y for y in range(size) if t[y, x] in "BCD"]
        if not col:
            continue
        top, bot = min(col), max(col)
        t[bot, x] = "K"
        mid = (top + bot) // 2
        if x % 6 == 3 and mid < bot:
            t[mid, x] = "E" if x < cx else "D"
    # The ring's stone top, lit from the top left and cut into eight blocks.
    for y in range(size):
        for x in range(size):
            if ell(x, y, rxo, ryo) <= 1.0 and ell(x, y, rxi, ryi) > 1.0:
                a = np.degrees(np.arctan2((y + 0.5 - cy) / ryo, (x + 0.5 - cx) / rxo))
                light = -np.cos(np.radians(a + 45))
                ch = "2" if light > 0.3 else ("3" if light > -0.6 else "4")
                if int((a + 180 + 11) // 45) != int((a + 180 + 13) // 45):
                    ch = "4"
                t[y, x] = ch
    # Outlines: the outer rim and the lip of the pit.
    out = t.copy()
    for y in range(size):
        for x in range(size):
            if t[y, x] not in "1234":
                continue
            if ell(x, y, rxo, ryo) > 0.86 and y + 0.5 < cy + 2:
                out[y, x] = "K"
            if ell(x, y, rxi, ryi) <= 1.18:
                out[y, x] = "K" if y + 0.5 < cy else "N"
    t = out
    # The pit: char, ash and glowing coals.
    rng = np.random.default_rng(7)
    for y in range(size):
        for x in range(size):
            if ell(x, y, rxi, ryi) <= 1.0:
                r = rng.random()
                if ell(x, y, rxi * 0.6, ryi * 0.7) <= 1.0:
                    t[y, x] = "H" if r < 0.35 else ("G" if r < 0.75 else "I")
                else:
                    t[y, x] = "N" if r < 0.45 else ("A" if r < 0.6 else ("G" if r < 0.85 else "F"))
    # Hestia's flame, rising from the coals in front of the ring's back.
    fh, fw = HEARTH_FLAME.shape
    fx, fy = int(cx - fw / 2), int(cy + 2 - fh)
    for y in range(fh):
        for x in range(fw):
            ch = HEARTH_FLAME[y, x]
            ty, tx = fy + y, fx + x
            if ch == CLEAR or ty < 0:
                continue
            if ty + 0.5 > cy and ell(tx, ty, rxi, ryi) > 1.0:
                continue
            t[ty, tx] = ch
    return t


# --- The inner hearth on the dais (3 x 1) ------------------------------------

def inner_hearth():
    """48 x 16: a long marble altar-hearth with Hestia's sacred flame."""
    w = 48
    t = blank(16, w)
    body = [
        "." * 2 + "K" * 44 + "." * 2,
        "." + "K" + "E" + "D" * 40 + "CCB" + "K" + ".",
        "." + "K" * 46 + ".",
        "." + "K" + "2" * 41 + "334" + "K" + ".",
        "." + "K" + "2" * 41 + "334" + "K" + ".",
        "." + "K" + "3" * 41 + "444" + "K" + ".",
        "." + "K" * 46 + ".",
        "." * 2 + "c" * 44 + "." * 2,
    ]
    over(t, g(*body), 0, 8)
    # Triglyph grooves on the altar's face.
    for x in range(8, 42, 8):
        t[11:13, x] = "4"
        t[11:13, x + 2] = "4"
    # Coals along the top and the flame at the center.
    rng = np.random.default_rng(3)
    for x in range(3, 45):
        r = rng.random()
        t[9, x] = "N" if r < 0.4 else ("A" if r < 0.55 else ("G" if r < 0.85 else "H"))
    flame = g(
        "......F.........",
        "......FF....F...",
        ".....FGF...FF...",
        "...F.FGHF..FGF..",
        "...FFGHIHFFGHF..",
        "..FGHIIJIHGHF...",
        "..FGHIJJJJIHGF..",
        ".FGHIJJJJJJIHGF.",
        ".FGHIIJJJJIIHGF.",
        "..FGHHIIIIHHGF..",
    )
    over(t, flame, 16, 0)
    return t


# --- The hymn's household ---------------------------------------------------------

LOAF = g(
    "..KKKK..",
    ".KYwwYK.",
    "KYwYYYXK",
    "KYYXYXXK",
    "KXYYXXWK",
    ".KKKKKK.",
)
JUG = g(
    ".KKKK.",
    "KxwxyK",
    ".KxyK.",
    "KxwxyK",
    "KwxxyK",
    "KxxyyK",
    "KxyyzK",
    ".KKKK.",
)
OLIVES = g(
    ".KKKK.",
    "KQPQPK",
    "KPRPQK",
    "KYYXXK",
    ".KKKK.",
)


def table():
    """32 x 32: an olive-wood table set with bread, olives and a jug."""
    t = blank(32, 32)
    top = [
        "..KKKKKKKKKKKKKKKKKKKKKKKKKKKK..",
        ".KYYYYYYYYYYYYYYYYYYYYYYYYYYYXK.",
        ".KYYYYYYYYYYYYYYYYYYYYYYYYYYXXK.",
        ".KYYYYYYYYYYYYYYYYYYYYYYYYYYXXK.",
        ".KXXXXXXXXXXXXXXXXXXXXXXXXXXXWK.",
        ".KKKKKKKKKKKKKKKKKKKKKKKKKKKKKK.",
        ".KXWKXXXXXXXXXXXXXXXXXXXXXKWXWK.",
        ".KXWKKKKKKKKKKKKKKKKKKKKKKKWXWK.",
    ]
    over(t, g(*top), 0, 7)
    leg = [".KXWK"] * 7 + [".KKKK"]
    for y, row in enumerate(leg):
        over(t, g(row), 0, 15 + y)
        over(t, g(row[::-1]), 26, 15 + y)
    t[23, 5:27] = "c"
    t[22, 5:27] = "c"
    over(t, LOAF, 5, 4)
    over(t, LOAF, 10, 6)
    over(t, OLIVES, 15, 6)
    over(t, JUG, 22, 1)
    return t


def loom():
    """32 x 32: a warp-weighted loom with a red cloth and a gold key band."""
    t = blank(32, 32)
    post = "KXK"
    for y in range(0, 30):
        over(t, g(post), 2, y)
        over(t, g(post), 27, y)
    t[0, 2:5] = "K"
    t[0, 27:30] = "K"
    beam = [
        "." + "K" * 30 + ".",
        "." + "K" + "Y" * 28 + "K" + ".",
        "." + "K" + "X" * 27 + "W" + "K" + ".",
        "." + "K" * 30 + ".",
    ]
    over(t, g(*beam), 0, 2)
    # The woven cloth: red with a gold Greek-key band.
    cloth = blank(10, 22, "s")
    cloth[0, :] = "r"
    cloth[1, :] = "g"
    cloth[8, :] = "g"
    cloth[9, :] = "t"
    for y, row in enumerate(MEANDER):
        for x in range(22):
            cloth[2 + y, x] = "t" if row[x % 8] == "#" else "g"
    cloth[7, :] = "g"
    over(t, cloth, 5, 6)
    # The warp hanging below, the shed rod across it, then the weights.
    for y in range(16, 24):
        for x in range(5, 27):
            t[y, x] = ("2" if y < 20 else "3") if x % 2 == 1 else CLEAR
    t[19, 5:27] = "K"
    t[19, 6:26] = "X"
    weights = g(
        "K2.K2.K2.K2.K2.K2.K2.K",
        "23K23K23K23K23K23K23K2",
        "34K34K34K34K34K34K34K3",
        "KK.KK.KK.KK.KK.KK.KK.K",
    )
    over(t, weights, 5, 24)
    t[30, 1:31] = "K"
    t[30, 2:5] = list("KXK")
    t[30, 27:30] = list("KXK")
    t[31, 3:30] = "c"
    return t


# A side door of olive wood with bronze studs in a marble frame, for the wall
# rows. Kanthos the donkey is tied beside it.
def side_door():
    t = blank(32, 16)
    rows = [
        "................",
        "................",
        ".KKKKKKKKKKKKKK.",
        ".K111111111112K.",
        ".K222222222334K.",
        ".KKKKKKKKKKKKKK.",
    ]
    for _ in range(22):
        rows.append(".K2KYXXWYXXWK3K.")
    rows += [
        ".K2KKKKKKKKKK3K.",
        ".K222222222233K.",
        ".KKKKKKKKKKKKKK.",
        "................",
    ]
    over(t, g(*rows))
    for y in (8, 13, 21, 26):
        t[y, 5] = "g"
        t[y, 9] = "g"
    t[16:18, 7:9] = "g"
    return t


KLINE = g(
    "KK..................",
    "KYK.................",
    "KYK.KKKK............",
    "KYKK2o22KKKKKKKKKKK.",
    "KYKK2oo2KrrrrrrrrrrK",
    "KYKKKKKKKrrsrrsrrssK",
    "KYK2222222rsrrsrsstK",
    "KYKKKKKKKKKKKKKKKKKK",
    "KXYYYYYYYYYYYYYYYYXK",
    "KXXXXXXXXXXXXXXXXXWK",
    "KKKKKKKKKKKKKKKKKKKK",
    ".KXK............KXK.",
)


def bed_niche():
    """32 x 32: an arched alcove in the wall with a kline made up for the
    night watch."""
    rows = [
        "." * 32,
        "." + "K" * 30 + ".",
        ".K" + "1" * 27 + "3" + "K.",
        ".K" + "2" * 26 + "34" + "K.",
        ".K12" + "K" * 24 + "34K.",
        ".K12K" + "KK" + "u" * 18 + "KK" + "K34K.",
        ".K12K" + "K" + "u" * 20 + "K" + "K34K.",
    ]
    for _ in range(7, 28):
        rows.append(".K12K" + "u" + "v" * 20 + "u" + "K34K.")
    rows += [
        ".K" + "2" * 27 + "3" + "K.",
        ".K" + "3" * 26 + "44" + "K.",
        "." + "K" * 30 + ".",
        "." * 32,
    ]
    t = g(*rows)
    over(t, KLINE, 6, 16)
    return t


# --- The sheet ----------------------------------------------------------------------

def build():
    """Every metatile as (name, bottom, middle, behavior), in id order."""
    M = []

    def add(name, bottom, middle=None, behavior="MB_NORMAL"):
        if middle is not None:
            # An object's shadow is painted into the ground beneath it, so
            # objects never need the floor's colors in their own palette.
            middle = middle.copy()
            bottom = bottom.copy()
            mask = middle == SHADOW
            bottom[mask] = [SHADE.get(ch, ch) for ch in bottom[mask]]
            middle[mask] = CLEAR
            if not (middle != CLEAR).any():
                middle = None
        M.append((name, bottom, middle, behavior))

    def add_object(names, canvas, bottoms):
        """Cut a multi-tile object; bottoms is a grid of background tiles."""
        cut = tiles(canvas)
        for j, row in enumerate(names):
            for i, name in enumerate(row):
                if name:
                    add(name, bottoms[j][i], cut[j][i])

    F = floor()
    D = dais()
    WT, FR, LW = wall_top(), frieze(F_KEY), lower_wall()
    def fl(n):
        return [[F] * n]

    # Row 0: floor and runner.
    add("void", void())
    add("floor", F)
    add("floor_vein_a", floor(1))
    add("floor_vein_b", floor(2))
    add("runner", runner())
    add("runner_end_s", runner_end())
    add("runner_end_n_dais", runner_end_north(D))
    add("runner_cord", runner(), cord())
    # Row 1: the key inlay and the doormat.
    add("inlay_h", inlay("h"))
    add("inlay_v", inlay("v"))
    add("inlay_tl", inlay("tl"))
    add("inlay_tr", inlay("tr"))
    add("inlay_bl", inlay("bl"))
    add("inlay_br", inlay("br"))
    add("mat_l", mat("l"), behavior="MB_SOUTH_ARROW_WARP")
    add("mat_m", mat("m"), behavior="MB_SOUTH_ARROW_WARP")
    # Row 2: more mat, the wall top and side walls, the lower wall.
    add("mat_r", mat("r"), behavior="MB_SOUTH_ARROW_WARP")
    add("mat_single", mat("single"), behavior="MB_SOUTH_ARROW_WARP")
    add("wall_top", WT)
    add("wall_corner_l", wall_corner())
    add("wall_corner_r", wall_corner(right=True))
    add("side_wall_l", side_wall())
    add("side_wall_r", side_wall(right=True))
    add("wall_lower", LW)
    # Row 3: the frieze and the lower wall's dressings.
    add("frieze_key", FR)
    add("frieze_palmette", frieze(F_PALMETTE))
    add("frieze_flame", frieze(F_FLAME))
    add("frieze_amphora", frieze(F_AMPHORA))
    add("frieze_hestia_l", frieze(F_HESTIA_L))
    add("frieze_hestia_r", frieze(F_HESTIA_R))
    add("wall_lower_wreath", LW, WREATH)
    add("wall_lower_lamps", LW, LAMP_LEDGE)
    # Rows 4-5: things set in the wall (two tall), and the dais.
    wall2 = [[FR], [LW]]
    p = tiles(PILASTER)
    door = tiles(side_door())
    niche = tiles(bed_niche())
    add("pilaster_top", FR, p[0][0])
    add("side_door_top", FR, door[0][0])
    add("bed_niche_tl", FR, niche[0][0])
    add("bed_niche_tr", FR, niche[0][1])
    add("dais", D)
    add("dais_sun", dais(sun=True))
    add("dais_edge_l", dais_edge())
    add("dais_edge_r", dais_edge(right=True))
    add("pilaster_bottom", LW, p[1][0])
    add("side_door_bottom", LW, door[1][0])
    add("bed_niche_bl", LW, niche[1][0])
    add("bed_niche_br", LW, niche[1][1])
    add("riser", riser())
    add("riser_l", riser("l"))
    add("riser_r", riser("r"))
    add("steps_runner", steps())
    # Rows 6-7: standing objects, tops above bottoms.
    col, stele, laurel = tiles(COLUMN), tiles(STELE), tiles(LAUREL)
    tab = tiles(table())
    add("column_top", F, col[0][0])
    add("stele_top", F, stele[0][0])
    add("amphora", F, AMPHORA)
    add("amphora_red", F, AMPHORA_RED)
    add("laurel_top", F, laurel[0][0])
    add("votive_lamps", F, VOTIVE)
    add("table_tl", F, tab[0][0])
    add("table_tr", F, tab[0][1])
    add("column_bottom", F, col[1][0])
    add("stele_bottom", F, stele[1][0])
    add("steps_plain", steps(with_runner=False))
    add("runner_end_n", runner_end_north(F))
    add("laurel_bottom", F, laurel[1][0])
    add("dais_runner", runner(D))
    add("table_bl", F, tab[1][0])
    add("table_br", F, tab[1][1])
    # Rows 8-9: braziers. Each lit metatile is its cold one + 1.
    cold_top = tiles(brazier(False, "door"))[0][0]
    lit_top = tiles(brazier(True, "door"))[0][0]
    add("brazier_top_cold", F, cold_top)
    add("brazier_top_lit", F, lit_top)
    for glyph in ("door", "table", "loom", "bed", "hearth"):
        add(f"brazier_{glyph}_cold", F, tiles(brazier(False, glyph))[1][0])
        add(f"brazier_{glyph}_lit", F, tiles(brazier(True, glyph))[1][0])
    ih = tiles(inner_hearth())
    add("inner_hearth_l", D, ih[0][0])
    add("inner_hearth_c", D, ih[0][1], behavior="MB_COUNTER")
    add("inner_hearth_r", D, ih[0][2])
    add("floor_spare", F)
    # Rows 10-14: the great hearth in its pool of light (columns 0-4), and the
    # loom (columns 5-6).
    region = np.empty((80, 80), dtype="<U1")
    for j in range(5):
        for i in range(5):
            region[j * 16:(j + 1) * 16, i * 16:(i + 1) * 16] = runner() if i == 2 else F
    lit = firelight(region, 40, 40, 40, 36)
    lit_tiles = tiles(lit)
    hearth = tiles(great_hearth())
    lm = tiles(loom())
    side = {
        (10, 5): ("loom_tl", F, lm[0][0]), (10, 6): ("loom_tr", F, lm[0][1]),
        (11, 5): ("loom_bl", F, lm[1][0]), (11, 6): ("loom_br", F, lm[1][1]),
    }
    for j in range(5):
        for i in range(COLS):
            if i < 5:
                inner = 1 <= i <= 3 and 1 <= j <= 3
                name = f"hearth_{j - 1}{i - 1}" if inner else f"glow_{j}{i}"
                add(name, lit_tiles[j][i], hearth[j - 1][i - 1] if inner else None)
            elif (10 + j, i) in side:
                add(*side[(10 + j, i)])
            else:
                add(f"spare_{10 + j}_{i}", F)
    return M


# --- Output -------------------------------------------------------------------------

def to_rgba(grid, opaque):
    h, w = grid.shape
    img = np.zeros((h, w, 4), np.uint8)
    img[..., 3] = 255
    for y in range(h):
        for x in range(w):
            ch = grid[y, x]
            if ch == CLEAR:
                if opaque:
                    raise ValueError("a bottom-layer pixel is transparent")
                img[y, x, :3] = MAGENTA
            else:
                img[y, x, :3] = COLORS[ch]
    return img


def primary_colors():
    used = set()
    for p in sorted(PRIMARY_PALS.glob("0[0-5].pal")):
        vals = [int(v) for v in p.read_text().split()[3:]]
        for i in range(1, len(vals) // 3):
            used.add(tuple(v & 0xF8 for v in vals[i * 3:i * 3 + 3]))
    return used


def check_colors(M):
    errors = []
    for k, c in COLORS.items():
        if any(v % 8 for v in c):
            errors.append(f"color {k} {c} is not a multiple of 8")
        if c == MAGENTA:
            errors.append(f"color {k} is magenta")
    clash = {k for k, c in COLORS.items() if c in primary_colors()}
    if clash:
        errors.append(f"colors shared with the aethos primary: {sorted(clash)}")
    if len(set(COLORS.values())) != len(COLORS):
        errors.append("two legend keys share a color")
    if len(PALETTES) > 7:
        errors.append("more than 7 palettes")
    for pname, keys in PALETTES.items():
        if len(keys) > 15 or len(set(keys)) != len(keys):
            errors.append(f"palette {pname} needs 15 distinct colors at most")
    # Every 8 x 8 tile of each layer must fit one planned palette.
    for n, (name, bottom, middle, _) in enumerate(M):
        for layer, grid in (("bottom", bottom), ("middle", middle)):
            if grid is None:
                continue
            for ty in (0, 8):
                for tx in (0, 8):
                    used = set(grid[ty:ty + 8, tx:tx + 8].ravel()) - {CLEAR}
                    if not any(used <= set(keys) for keys in PALETTES.values()):
                        errors.append(f"{name} {layer} tile ({tx},{ty}) fits no palette: "
                                      f"{''.join(sorted(used))}")
    return errors


def write_config():
    """The per-tileset Porytiles config: the primary pairing and our palettes."""
    path = ROOT / "porytiles/tilesets/gTileset_TempleHestia/config.yaml"
    lines = [
        "# Written by tools/ichor/art/temple_hestia.py; edit it there.",
        "tileset:",
        "  # Porytiles compiles a secondary against a primary it manages. The",
        "  # temple shares no colors with aethos, so nothing is reused from it and",
        "  # the result works on any primary.",
        "  primary_pairing:",
        "    mode: manual",
        "    partners: [gTileset_Aethos]",
        "  palettes:",
        "    packing:",
        "      hints_enabled: true",
        "      hints:",
    ]
    for pname, keys in PALETTES.items():
        lines.append(f"        - name: {pname}")
        lines.append("          colors:")
        for k in keys:
            r, gg, b = COLORS[k]
            lines.append(f"            - [{r}, {gg}, {b}]")
    path.write_text("\n".join(lines) + "\n")


def catalog(M=None):
    """name -> metatile id."""
    M = M or build()
    return {name: FIRST_ID + n for n, (name, *_rest) in enumerate(M)}


def main():
    M = build()
    errors = check_colors(M)
    if errors:
        sys.exit("temple_hestia: " + "\n  ".join(errors))
    rows = (len(M) + COLS - 1) // COLS
    sheets = {k: np.zeros((rows * 16, COLS * 16, 4), np.uint8) for k in ("bottom", "middle", "top")}
    for s in sheets.values():
        s[..., :3] = MAGENTA
        s[..., 3] = 255
    for n, (name, bottom, middle, _) in enumerate(M):
        y, x = divmod(n, COLS)
        sheets["bottom"][y * 16:y * 16 + 16, x * 16:x * 16 + 16] = to_rgba(bottom, True)
        if middle is not None:
            sheets["middle"][y * 16:y * 16 + 16, x * 16:x * 16 + 16] = to_rgba(middle, False)
    # Pad the last row with plain floor so every bottom stays opaque.
    for n in range(len(M), rows * COLS):
        y, x = divmod(n, COLS)
        sheets["bottom"][y * 16:y * 16 + 16, x * 16:x * 16 + 16] = to_rgba(floor(), True)
    SRC.mkdir(parents=True, exist_ok=True)
    for k, s in sheets.items():
        Image.fromarray(s, "RGBA").save(SRC / f"{k}.png")
    with open(SRC / "attributes.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "behavior"])
        for n, (_, _, _, beh) in enumerate(M):
            if beh != "MB_NORMAL":
                w.writerow([n, beh])
    write_config()
    print(f"temple_hestia: {len(M)} metatiles, {rows} sheet rows -> {SRC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
