"""Painters for gTileset_Astyra: the capital below the rock, and its harbor.

The city's sentence: "a capital under its Akropolis". The rock and its wall
run along the map's north edge with the Parthenon's pediment and Athena
Promachos's helmet, shield and gleaming spear over the wall (the same art as
gTileset_Akropolis, cropped: the skyline is the real thing, seen from below).
Under it: the Panathenaic Way, the Stoa of the Archon framing the agora, the
Corinthian Library, the Asclepeion by the Dipylon gate, courtyard-house
blocks on the slopes, the city wall, the fountain house, the Pnyx's speaker's
platform, and the harbor's quays and ship sheds.

Columns come from tools/ichor/art/columns.py; the rock, the Parthenon and
Promachos from astyra_art.py. astyra_build.py astyra compiles it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import astyra_art as AA  # noqa: E402
import columns as CK  # noqa: E402
import kythera_lib as K  # noqa: E402
from kythera_lib import struct  # noqa: E402
from astyra_art import canvas, cut, crop, hp, mask_draw, outline_mask, rock_px, shadow_band  # noqa: E402

LABELS = []


# --------------------------------------------------------------------------
# Terracotta roofs and plastered walls
# --------------------------------------------------------------------------

def roof_px(X, Y, y0, y1):
    """A terracotta tile roof seen from the front, rows y0..y1: the ridge's
    cover tiles on top, courses of pan and cover tiles (pans lit, covers
    darker), antefixes and a shadow along the eave."""
    y = Y - y0
    hh = y1 - y0
    if y == 0:
        return "ink"
    if y <= 2:
        return "tc3" if (X % 8) < 6 else "tc2"            # ridge tiles
    if y == 3:
        return "tc0"
    if y >= hh - 2:
        if y == hh:
            return "ink"
        # the eave: antefixes (small palmettes) every 8 px
        return "tc3" if X % 8 in (3, 4) else "tc0"
    course = (y - 4) % 5
    if course == 4:
        return "tc0"
    if X % 4 == 0:
        return "tc1" if course else "tc0"                 # cover-tile ribs
    return "tc3" if course == 0 else "tc2" if X % 4 == 1 else "tc1"


def paint_roof(L, x0, x1, y0, y1, hip=True):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = roof_px(x, y, y0, y1)
            if hip and (x - x0 < 2 or x1 - x < 2):
                c = "ink" if x in (x0, x1) else "tc0"
            L.px(x, y, c)


def wall_px(X, Y, y0, y1, socle=4):
    """Plastered wall from y0 to y1: lit plaster, a few cracks, a stone socle
    along the foot, an eave shadow at the top."""
    y = Y - y0
    if y < 2:
        return "hw1"
    if y1 - Y < socle:
        if Y == y1:
            return "ink"
        return "hw1" if (X + 3 * ((Y - y1) // 2)) % 6 == 0 else "hw2"
    k = hp(X, Y, 4)
    if k % 31 == 0:
        return "hw1"
    return "hw3" if k % 5 else "hw2"


def paint_wall(L, x0, x1, y0, y1, windows=(), door=None):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = wall_px(x, y, y0, y1)
            if x in (x0, x1):
                c = "ink"
            L.px(x, y, c)
    for wx in windows:
        # a small high window with a timber grille
        for y in range(y0 + 4, y0 + 8):
            for x in range(wx, wx + 4):
                L.px(x, y, "cd0" if (x + y) % 2 else "wd0")
        for x in range(wx - 1, wx + 5):
            L.px(x, y0 + 8, "hw1")
    if door:
        dx, dw = door
        for y in range(y0 + 3, y1 + 1):
            for x in range(dx, dx + dw):
                e = x in (dx, dx + dw - 1) or y == y0 + 3
                L.px(x, y, "wd0" if e else "wd1" if (x - dx) % 3 else "wd2")
        L.px(dx + dw - 3, y0 + 9, "pr1")                    # a bronze ring pull


def house_kit(key="house", on="grass"):
    """Courtyard houses of the asty, on borrowed ground. Roofs, two rows:
    RT_L RT_M RT_R over RB_L RB_M RB_R. Walls: W_L W_M W_R (one storey, blank),
    W_win (a high grilled window), U_L U_M U_R (an upper storey with windows,
    over a W row), door (a timber door with a ring), and F_L F_M F_R, a flat
    plastered roof terrace for the third height. Blank walls and one door:
    life is inside, round the court."""
    names = {"RT_L": (0, 0), "RT_M": (1, 0), "RT_R": (2, 0), "F_L": (3, 0), "F_M": (4, 0), "F_R": (5, 0),
             "RB_L": (0, 1), "RB_M": (1, 1), "RB_R": (2, 1), "U_L": (3, 1), "U_M": (4, 1), "U_R": (5, 1),
             "W_L": (0, 2), "W_M": (1, 2), "W_R": (2, 2), "W_win": (3, 2), "door": (4, 2), "W_jar": (5, 2)}
    walk = ["XXXXXX", "XXXXXX", "XXXXDX"]
    s = struct(key, "courtyard houses", 6, 3, "town", walk=walk, names=names, on=on)
    L = s.M
    # the pitched roof, 2 rows, with hipped ends
    for cx, part in ((0, "L"), (1, "M"), (2, "R")):
        x0 = cx * 16
        for y in range(2, 32):
            for x in range(x0, x0 + 16):
                c = roof_px(x, y, 2, 31)
                if part == "L":
                    edge = x - x0 < max(1, 6 - y // 5)
                    if edge:
                        continue
                    if x - x0 == max(1, 6 - y // 5):
                        c = "ink"
                if part == "R":
                    edge = x0 + 15 - x < max(1, 6 - y // 5)
                    if edge:
                        continue
                    if x0 + 15 - x == max(1, 6 - y // 5):
                        c = "ink"
                L.px(x, y, c)
    # the flat roof terrace: plaster with a low parapet and a drain
    for cx, part in ((3, "L"), (4, "M"), (5, "R")):
        x0 = cx * 16
        for y in range(4, 16):
            for x in range(x0, x0 + 16):
                c = "hw3" if y < 6 else "hw2" if (x + y) % 9 else "hw1"
                if y == 4:
                    c = "ink"
                if (part == "L" and x == x0) or (part == "R" and x == x0 + 15):
                    c = "ink"
                if y == 15:
                    c = "hw1"
                L.px(x, y, c)
        if part == "M":
            L.px(x0 + 8, 14, "cd0")
    # upper storey: plaster with two windows per cell
    for cx, part in ((3, "L"), (4, "M"), (5, "R")):
        x0 = cx * 16
        for y in range(16, 32):
            for x in range(x0, x0 + 16):
                c = wall_px(x, y, 16, 40, socle=0)
                if (part == "L" and x == x0) or (part == "R" and x == x0 + 15):
                    c = "ink"
                L.px(x, y, c)
        for wx in (x0 + 3, x0 + 10):
            for y in range(21, 26):
                for x in range(wx, wx + 3):
                    L.px(x, y, "cd0" if y > 21 else "wd0")
            for x in range(wx - 1, wx + 4):
                L.px(x, 26, "hw1")
    # one storey of wall
    for cx, part in ((0, "L"), (1, "M"), (2, "R"), (3, "win"), (4, "door"), (5, "jar")):
        x0 = cx * 16
        for y in range(32, 48):
            for x in range(x0, x0 + 16):
                c = wall_px(x, y, 32, 46)
                if (part == "L" and x == x0) or (part == "R" and x == x0 + 15):
                    c = "ink"
                L.px(x, y, c)
        for x in range(x0, x0 + 16):
            L.px(x, 47, "ps" if on == "path" else "gd")
        if part == "win":
            for y in range(36, 40):
                for x in range(x0 + 6, x0 + 10):
                    L.px(x, y, "cd0" if (x + y) % 2 else "wd0")
        if part == "door":
            for y in range(35, 47):
                for x in range(x0 + 4, x0 + 12):
                    e = x in (x0 + 4, x0 + 11) or y == 35
                    L.px(x, y, "wd0" if e else "wd1" if (x - x0) % 3 else "wd2")
            L.px(x0 + 9, 41, "pr1")
        if part == "jar":
            # a pithos against the wall
            for y in range(37, 47):
                w = 3 if y < 39 else 4 if y < 44 else 3
                for x in range(x0 + 8 - w, x0 + 8 + w):
                    L.px(x, y, "tc3" if x < x0 + 7 else "tc2" if x < x0 + 9 else "tc1")
            for x in range(x0 + 5, x0 + 11):
                L.px(x, 37, "tc0")
    return s


# --------------------------------------------------------------------------
# The rock from the city: the Akropolis wall, the cliff, the ramp stair
# --------------------------------------------------------------------------

def akro_wall(key="akro_wall"):
    """The Akropolis wall crowning the rock, one row on borrowed path (the
    plateau behind it): a coping course over coursed ashlar. M, M_b, L, R,
    and the gate: gate_L, gate (a door: the way up to the Propylaia), gate_R."""
    names = {"L": (0, 0), "M": (1, 0), "M_b": (2, 0), "R": (3, 0), "gate_L": (4, 0), "gate": (5, 0),
             "gate_R": (6, 0)}
    s = struct(key, "the Akropolis wall", 7, 1, "rock", walk=["XXXXXDX"], names=names, on="path")
    L = s.M
    for name, (cx, _) in names.items():
        x0 = cx * 16
        for y in range(16):
            for x in range(x0, x0 + 16):
                lx = x - x0
                if name == "L" and lx < 3 or name == "R" and lx > 12:
                    continue
                if y < 3:
                    c = "ar5" if y == 0 else "ar4" if y == 1 else "ar1"
                else:
                    course = (y - 3) // 4
                    jx = (x + 8 * (course % 2)) % 16
                    c = "ar1" if (y - 3) % 4 == 3 or jx == 0 else "ar4" if (y - 3) % 4 == 0 else "ar3"
                    if name == "M_b" and course == 1 and 4 <= lx <= 11:
                        c = "ar0" if y in (7, 10) else "ar2"     # a spolia block
                if (name == "L" and lx == 3) or (name == "R" and lx == 12):
                    c = "ar0"
                L.px(x, y, c)
    # the gate: a dark opening under a lintel, jambs either side
    x0 = names["gate"][0] * 16
    for y in range(3, 16):
        for x in range(x0 + 2, x0 + 14):
            L.px(x, y, "ar0" if y == 3 or x in (x0 + 2, x0 + 13) else "t0" if y > 12 else "ar0")
    for x in range(x0, x0 + 16):
        L.px(x, 2, "ar5")
        L.px(x, 3, "ar1")
    s.behaviors[(5, 0)] = "MB_NON_ANIMATED_DOOR"
    s.notes = ("The Akropolis wall along the rock's top (`L` `M` `M_b` `R`, `M_b` with a re-used "
               "block), and `gate`, the door up to the Propylaia between `gate_L` and `gate_R`.")
    return s


def rock_stair(key="rock_stair"):
    """A stair cut up the rock's face to the gate, 1 wide: `face` (repeat it up
    the cliff) and `foot` (on borrowed grass, where it meets the street)."""
    s = struct(key, "the rock-cut stair", 2, 1, "rock", walk=[".."], names={"face": (0, 0), "foot": (1, 0)})
    L = s.B
    for cx in (0, 1):
        x0 = cx * 16
        for y in range(16):
            for x in range(x0, x0 + 16):
                lx = x - x0
                if lx < 2 or lx > 13:
                    c = rock_px(x, y + 16 * cx) if lx < 2 else "ar1"
                    if lx == 1:
                        c = "ar4"
                    if lx == 14:
                        c = "ar0"
                else:
                    t = y % 4
                    c = "ar5" if t == 0 else "ar4" if t == 1 else "ar3" if t == 2 else "ar1"
                if cx == 1 and y > 11 and (lx < 2 or lx > 13):
                    c = "gd"
                L.px(x, y, c)
    return s


# --------------------------------------------------------------------------
# The Stoa of the Archon
# --------------------------------------------------------------------------

def stoa(key="stoa"):
    """The Stoa of the Archon, a long colonnade framing the agora's north side,
    built from repeatable cells (on borrowed path where its edges show the
    ground):
      roof row 0, 1:  RT_L RT_M RT_R / RB_L RB_M RB_R (terracotta, the ridge
                      and the eave with its antefixes)
      colonnade row 2, 3: C_L (the end wall, painted), C_M (a Doric column in
                      front of the painted back wall: the Poikile's pictures),
                      C_M2 (another picture), C_door (the doorway into the
                      Assembly; a door) over B_L B_M B_door B_R
      the step, row 4: S_L S_M S_R (walkable: the player stands at the door)
      the wings' pediments for the ends: P_L P_M P_R (a gable front, row 0/1
                      over a pedimented end bay)"""
    names = {"RT_L": (0, 0), "RT_M": (1, 0), "RT_R": (2, 0), "P_L": (3, 0), "P_M": (4, 0), "P_R": (5, 0),
             "RB_L": (0, 1), "RB_M": (1, 1), "RB_R": (2, 1), "Q_L": (3, 1), "Q_M": (4, 1), "Q_R": (5, 1),
             "C_L": (0, 2), "C_M": (1, 2), "C_M2": (2, 2), "C_door": (3, 2), "C_R": (4, 2), "C_M3": (5, 2),
             "B_L": (0, 3), "B_M": (1, 3), "B_M2": (2, 3), "B_door": (3, 3), "B_R": (4, 3), "B_M3": (5, 3),
             "S_L": (0, 4), "S_M": (1, 4), "S_R": (2, 4), "S_M2": (3, 4), "S_M3": (4, 4), "S_x": (5, 4)}
    walk = ["XXXXXX", "XXXXXX", "XXXXXX", "XXXDXX", "......"]
    s = struct(key, "the Stoa of the Archon", 6, 5, "town", walk=walk, names=names, on="path")
    L = s.M
    # roof
    for cx, part in ((0, "L"), (1, "M"), (2, "R")):
        x0 = cx * 16
        for y in range(4, 32):
            for x in range(x0, x0 + 16):
                c = AA_roof(x, y, 4, 31)
                if part == "L" and x - x0 < 2:
                    c = "ink" if x == x0 + 1 else None
                if part == "R" and x0 + 15 - x < 2:
                    c = "ink" if x == x0 + 14 else None
                if c:
                    L.px(x, y, c)
    # the gable fronts for the wings: a pediment 3 cells wide over rows 0-1
    G = canvas(3, 2)
    AA.pediment(G, 0, 47, 0, 26, sculpture=False, color="pr1", akroteria=True)
    for y in range(26, 32):
        for x in range(0, 48):
            G.px(x, y, ["cm0", "cm5", "pr1", "cm1", "cm4", "cm2"][y - 26] if x not in (0, 47) else "cm0")
    for y in range(32):
        for x in range(48):
            c = G.get(x, y)
            if c:
                L.px(48 + x, y, c)
    # colonnade: entablature on top, columns before the painted back wall
    PICS = [["pr1", "pg1", "pb1"], ["pb1", "pr1", "pg2"], ["pg1", "pb0", "pr1"]]
    for name in ("C_L", "C_M", "C_M2", "C_door", "C_R", "C_M3"):
        cx, cy = names[name]
        x0, y0 = cx * 16, 32
        for y in range(y0, y0 + 32):
            for x in range(x0, x0 + 16):
                L.px(x, y, "cd1" if y > y0 + 9 else "cd0")
        # the painted pictures on the back wall
        if name in ("C_M", "C_M2", "C_M3"):
            pal = PICS[("C_M", "C_M2", "C_M3").index(name)]
            for y in range(y0 + 12, y0 + 22):
                for x in range(x0 + 1, x0 + 15):
                    if x in (x0 + 1, x0 + 14) or y in (y0 + 12, y0 + 21):
                        L.px(x, y, "pg1")
                    else:
                        k = ((x - x0) // 3 + (y - y0) // 4) % 3
                        L.px(x, y, pal[k] if (x + y) % 3 else "cd0")
        if name == "C_door":
            for y in range(y0 + 12, y0 + 32):
                for x in range(x0 + 3, x0 + 13):
                    e = y == y0 + 12 or x in (x0 + 3, x0 + 12)
                    L.px(x, y, "cm3" if e else "cd0")
        if name in ("C_L", "C_R"):
            for y in range(y0 + 8, y0 + 32):
                for x in range(x0, x0 + 16):
                    lx = x - x0
                    c = "cm4" if (y - y0) % 8 else "cm2"
                    if (lx + 4 * ((y - y0) // 8)) % 16 == 0:
                        c = "cm2"
                    if (name == "C_L" and lx == 0) or (name == "C_R" and lx == 15):
                        c = "cm0"
                    L.px(x, y, c)
        else:
            if name != "C_door":
                CK.paint_column(L, x0 + 8, y0 + 8, y0 + 30, "doric", "marble")
            else:
                for (xa, xb) in ((x0, x0 + 2), (x0 + 13, x0 + 15)):
                    for y in range(y0 + 8, y0 + 31):
                        for x in range(xa, xb + 1):
                            L.px(x, y, "cm4" if x == xa else "cm2")
        # the entablature: architrave and a plain frieze with painted triglyphs
        for x in range(x0, x0 + 16):
            for j, c in enumerate(["cm0", "cm5", "cm4", "pb1", "pb1", "cm4", "cm2", "cm0"]):
                cc = c
                if j in (3, 4) and (x - x0) % 8 in (3, 4):
                    cc = "pb0"
                if j in (3, 4) and (x - x0) % 8 not in (2, 3, 4, 5):
                    cc = "cm4"
                L.px(x, y0 + j, cc)
        for x in range(x0, x0 + 16):
            L.px(x, y0 + 31, "cm1")
    # the step in front: walkable, a lit tread and a riser
    for name in ("S_L", "S_M", "S_R", "S_M2", "S_M3", "S_x"):
        cx, cy = names[name]
        x0, y0 = cx * 16, 64
        for y in range(y0, y0 + 8):
            for x in range(x0, x0 + 16):
                lx = x - x0
                if name == "S_L" and lx < 1 or name == "S_R" and lx > 14:
                    continue
                c = "cm5" if y == y0 else "cm4" if y < y0 + 3 else "cm3" if y < y0 + 7 else "cm1"
                if name in ("S_M2",) and lx % 8 == 0 and y > y0 + 2:
                    c = "cm2"
                L.px(x, y, c)
        for x in range(x0 + 2, x0 + 16):
            if (x + y0) % 2 == 0 and name != "S_x":
                L.px(x, y0 + 8, "ps")
    s.behaviors[(3, 3)] = "MB_NON_ANIMATED_DOOR"
    return s


def AA_roof(x, y, y0, y1):
    return roof_px(x, y, y0, y1)


# --------------------------------------------------------------------------
# The Library (Corinthian) and the Asclepeion (Ionic)
# --------------------------------------------------------------------------

def library(key="library"):
    """The Library of Astyra, 7 x 5 on borrowed path: the city's one
    Corinthian building, four columns at a 32 px pitch with bronze capitals,
    a pediment, the doorway behind the middle gap (cell 3, a door)."""
    W, H = 7, 5
    L = canvas(W, H)
    x1 = W * 16 - 1
    for y in range(28, 70):
        for x in range(2, x1 - 1):
            L.px(x, y, "cd1" if y > 34 else "cd0")
    for y in range(38, 70):
        for x in range(51, 61):
            e = y == 38 or x in (51, 60)
            L.px(x, y, "pg1" if e else "cd0")
    for k in range(4):
        CK.paint_column(L, 8 + 32 * k, 30, 69, "corinthian", "poly")
    for x in range(1, x1):
        for j, c in enumerate(["cm0", "cm5", "cm4", "cm2", "cm5", "cm3", "cm1"]):
            L.px(x, 23 + j, c if x not in (1, x1 - 1) else "cm0")
    for x in range(1, x1):
        if x % 4 == 1:
            L.px(x, 22, "cm4")
    AA.pediment(L, 0, x1, 0, 20, sculpture=False, color="pb1")
    # an inscribed scroll-case relief in the pediment: two gold lines
    for x in range(48, 64):
        L.px(x, 14, "pg1")
        L.px(x, 16, "pg2")
    for s_ in range(2):
        y = 70 + 4 * s_
        for x in range(1 - s_, x1 + s_):
            for j in range(4):
                L.px(x, y + j, "cm5" if j == 0 else "cm4" if j == 1 else "cm3" if j == 2 else "cm1")
    # the stair in front of the door: walkable
    shadow_band(L, 0, x1, 78, rows=2)
    walk = ["XXXXXXX", "XXXXXXX", "XXXXXXX", "XXXDXXX", "XXX.XXX"]
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    s = cut(key, "the Library of Astyra", W, H, {"middle": L}, walk, names=names, section="town",
            notes="The Library (7 x 5): Astyra's one Corinthian building, bronze capitals, a pediment "
                  "with a gold scroll-case relief. Door at r3c3; r4c3 is its walkable step.")
    s.behaviors[(3, 3)] = "MB_NON_ANIMATED_DOOR"
    return s


def asclepeion(key="asclepeion"):
    """The Asclepeion, 5 x 4: a terracotta-roofed hall with an Ionic porch in
    antis (two columns between the side walls), the door (cell 2, row 3) and
    the snake-staff painted over it."""
    W, H = 5, 4
    L = canvas(W, H)
    x1 = W * 16 - 1
    paint_roof(L, 0, x1, 2, 31)
    for y in range(32, 64):
        for x in range(1, x1):
            L.px(x, y, "cd1" if y > 38 else "cd0")
    for x in range(30, 50):
        for y in range(42, 64):
            e = y == 42 or x in (30, 49)
            L.px(x, y, "cm3" if e else "cd0")
    # the snake and staff over the door, gold
    for y in range(34, 41):
        L.px(39, y, "pg1")
    for (x, y) in ((38, 35), (40, 36), (38, 37), (40, 38), (38, 39)):
        L.px(x, y, "pg2")
    for k in (1, 3):
        CK.paint_column(L, 16 * k + 8, 32, 61, "ionic", "marble")
    for ax in (0, x1 - 9):
        for y in range(32, 63):
            for x in range(ax, ax + 10):
                c = "cm4" if (y - 32) % 8 else "cm2"
                if x in (ax, ax + 9):
                    c = "cm0"
                L.px(x, y, c)
    for x in range(0, x1 + 1):
        L.px(x, 62, "cm4")
        L.px(x, 63, "cm1")
    walk = ["XXXXX", "XXXXX", "XXXXX", "XXDXX"]
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    s = cut(key, "the Asclepeion", W, H, {"middle": L}, walk, names=names, on="grass", section="town",
            notes="The Asclepeion (5 x 4) on borrowed grass: terracotta roof, an Ionic porch in antis, "
                  "the snake-staff over the door (r3c2).")
    s.behaviors[(2, 3)] = "MB_NON_ANIMATED_DOOR"
    return s


def roof_marble_split(s):
    """Roof cells drawn on the middle layer share it with marble below: fine,
    since every 8 px tile is all roof or all marble."""
    return s


# --------------------------------------------------------------------------
# The city wall, its towers and gates
# --------------------------------------------------------------------------

def city_wall(key="city_wall"):
    """The Themistoklean wall, on borrowed grass:
      v, v_b       a north-south run seen from above (the walkway between two
                   parapets), one cell wide
      v_end_N, v_end_S
                   its ends
      tower_TL tower_TR / tower_BL tower_BR
                   a square tower (2 x 2) seen from above, its roof of tiles
      h_top h_top_b / h_face h_face_b
                   an east-west run: the walkway's parapet over the outer face
      h_L h_R, hf_L hf_R
                   its ends
      gate_top gate_face
                   a gate's lintel (top layer) over its walkable passage"""
    names = {"v": (0, 0), "v_b": (1, 0), "v_end_N": (2, 0), "v_end_S": (3, 0), "tower_TL": (4, 0),
             "tower_TR": (5, 0), "h_top": (6, 0), "h_top_b": (7, 0),
             "h_L": (0, 1), "h_R": (1, 1), "hf_L": (2, 1), "hf_R": (3, 1), "tower_BL": (4, 1),
             "tower_BR": (5, 1), "h_face": (6, 1), "h_face_b": (7, 1),
             "gate_top": (0, 2), "gate_face": (1, 2)}
    walk = ["XXXXXXXX", "XXXXXXXX", "TT......"]
    s = struct(key, "the city wall", 8, 3, "town", walk=walk + [], names=names, on="grass")
    s.walk = ["XXXXXXXX", "XXXXXXXX", "TT......"]
    L = s.M
    st = lambda X, Y: "ar3" if (Y % 6 == 0 or (X + 5 * ((Y // 6) % 2)) % 10 == 0) else "ar4" if hp(X, Y, 2) % 7 else "ar2"
    # north-south runs: parapets left and right, the walkway between
    for name in ("v", "v_b", "v_end_N", "v_end_S"):
        cx, cy = names[name]
        x0 = cx * 16
        for y in range(16):
            for x in range(x0 + 1, x0 + 15):
                lx = x - x0
                if name == "v_end_N" and y < 3 or name == "v_end_S" and y > 12:
                    continue
                if lx in (1, 14):
                    c = "ar0"
                elif lx in (2, 3, 12, 13):
                    c = "ar5" if lx in (2, 12) else "ar3"
                    if name == "v_b" and y % 8 < 3 and lx in (12, 13):
                        c = "ar1"           # a crenel
                else:
                    c = "ar2" if (y + (lx // 4)) % 4 else "ar1"
                L.px(x, y, c)
            L.px(x0 + 15, y, "gd")
        if name == "v_end_N":
            for x in range(x0 + 1, x0 + 15):
                L.px(x, 3, "ar0")
                L.px(x, 4, "ar5")
        if name == "v_end_S":
            for x in range(x0 + 1, x0 + 15):
                L.px(x, 12, "ar0")
                L.px(x, 13, "gd")
    # a tower seen from above: a tiled pyramid roof
    for name in ("tower_TL", "tower_TR", "tower_BL", "tower_BR"):
        cx, cy = names[name]
        x0, y0 = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                X, Y = x + (0 if name.endswith("L") else 16), y + (0 if name[6] == "T" else 16)
                if X < 1 or X > 30 or Y < 1 or Y > 28:
                    continue
                c = "ar1"
                if 3 <= X <= 28 and 3 <= Y <= 26:
                    # four slopes meeting at the peak
                    dx, dy = X - 15.5, Y - 14.5
                    if abs(dx) > abs(dy):
                        c = "ar4" if dx < 0 else "ar2"
                    else:
                        c = "ar5" if dy < 0 else "ar1"
                    if (X + Y) % 4 == 0:
                        c = "ar3"
                if X in (1, 30) or Y in (1, 28):
                    c = "ar0"
                if Y > 28:
                    c = "gd"
                L.px(x0 + x, y0 + y, c)
        if name[6] == "B":
            for x in range(16):
                L.px(x0 + x, y0 + 13, "ar0")
                if (x + 14) % 2 == 0:
                    L.px(x0 + x, y0 + 14, "gd")
                L.px(x0 + x, y0 + 15, "gd")
    # east-west runs: parapet and walkway (top), the outer face (face)
    for name in ("h_top", "h_top_b", "h_L", "h_R"):
        cx, cy = names[name]
        x0, y0 = cx * 16, cy * 16
        for y in range(4, 16):
            for x in range(x0, x0 + 16):
                lx = x - x0
                if name == "h_L" and lx < 2 or name == "h_R" and lx > 13:
                    continue
                if y == 4:
                    c = "ar0"
                elif y < 8:
                    c = "ar5" if y == 5 else "ar3"
                    if name == "h_top_b" and lx % 8 < 3:
                        c = "ar1"
                else:
                    c = "ar2" if (lx + y) % 5 else "ar1"
                if (name == "h_L" and lx == 2) or (name == "h_R" and lx == 13):
                    c = "ar0"
                L.px(x, y0 + y, c)
    for name in ("h_face", "h_face_b", "hf_L", "hf_R", "gate_face"):
        cx, cy = names[name]
        x0, y0 = cx * 16, cy * 16
        for y in range(16):
            for x in range(x0, x0 + 16):
                lx = x - x0
                if name == "hf_L" and lx < 2 or name == "hf_R" and lx > 13:
                    continue
                if name == "gate_face":
                    if 2 <= lx <= 13:
                        continue
                if y > 12:
                    c = "ar0" if y == 13 else "gd"
                else:
                    c = st(x, y)
                    if name == "h_face_b" and 5 <= lx <= 10 and 3 <= y <= 8:
                        c = "ar1" if (lx + y) % 2 else "ar0"     # an arrow slit
                if (name == "hf_L" and lx == 2) or (name == "hf_R" and lx == 13):
                    c = "ar0"
                L.px(x, y0 + y, c)
    # the gate's lintel, over the player
    cx, cy = names["gate_top"]
    x0, y0 = cx * 16, cy * 16
    for y in range(4, 16):
        for x in range(x0, x0 + 16):
            c = "ar0" if y in (4, 15) else "ar5" if y == 5 else "ar3" if y < 12 else "ar1"
            L.px(x, y0 + y, c)
    s.notes = ("The city wall: `v` runs north-south (seen from above), `h_top` over `h_face` east-west; "
               "towers 2 x 2; `gate_top` is a lintel drawn over the player above a walkable gap; "
               "`gate_face` is a wall face with the gap open.")
    return s


# --------------------------------------------------------------------------
# The agora's furniture
# --------------------------------------------------------------------------

def fountain(key="fountain"):
    """The fountain house (Enneakrounos), 3 x 3 on borrowed path: a Doric
    porch roof, three bronze lion-head spouts pouring into a marble basin
    (animation 'spout'), the basin's rim walkable in front? No: solid."""
    W, H = 3, 3
    L = canvas(W, H)
    x1 = 47
    for y in range(8, 34):
        for x in range(1, x1):
            L.px(x, y, "cd1" if y > 12 else "cd0")
    AA.pediment(L, 0, x1, 0, 8, sculpture=False, color="pb1", akroteria=False)
    for x in range(1, x1):
        for j, c in enumerate(["cm0", "cm5", "cm4", "cm1"]):
            L.px(x, 10 + j, c)
    for k in (0, 2):
        CK.paint_column(L, 8 + 16 * k, 14, 34, "doric", "marble", cap=True)
    spouts = (24,)
    for sx in spouts:
        for (x, y, c) in ((sx - 2, 16, "bz2"), (sx - 1, 16, "bz2"), (sx, 16, "bz2"), (sx + 1, 16, "bz1"),
                          (sx - 2, 17, "bz1"), (sx - 1, 17, "cm0"), (sx, 17, "bz1"), (sx + 1, 17, "bz1"),
                          (sx - 1, 18, "bz2"), (sx, 18, "bz1")):
            L.px(x, y, c)
    # the basin
    for y in range(32, 46):
        for x in range(1, x1):
            c = "cm4" if y < 35 else "cm3" if x < 30 else "cm2"
            if y == 32:
                c = "cm5"
            if 35 <= y <= 39 and 3 <= x <= x1 - 4:
                c = "aw2" if (x + y) % 5 else "aw3"
            if x in (1, x1 - 1) or y == 45:
                c = "cm0"
            L.px(x, y, c)
    frames = []
    for f in range(3):
        F = canvas(W, H)
        for sx in spouts:
            for y in range(19, 36):
                if (y + f * 2) % 6 < 4:
                    F.px(sx - 1 + (y % 2), y, "aw3")
                    F.px(sx - 1 + ((y + 1) % 2), y, "aw2")
                else:
                    F.px(sx - 1, y, "aw1")
                    F.px(sx, y, "aw2")
            for (dx, dy) in ((-3, 36), (2, 37), (-1, 38)):
                if (dx + f) % 3 == 0:
                    F.px(sx + dx, dy, "aw3")
        frames.append(("middle", F))
    names = {f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)}
    s = cut(key, "the fountain house", W, H, {"middle": L}, ["XXX"] * 3, names=names, section="town",
            notes="The fountain house (3 x 3): a Doric porch and a pediment, the bronze lion's head "
                  "pouring into the marble basin (animation `spout`). Solid; read it from the front.",
            anims={"spout": frames[1:]})
    K.settle(s, "spout", [(1, 1), (1, 2)])
    return s


def statue(key, figure, on="path"):
    """A bronze statue on a marble plinth, 1 x 2 on borrowed ground: the
    figure on the top layer (walk behind), the plinth solid."""
    W, H = 1, 2
    T = canvas(W, H)
    P = canvas(W, H)
    for y in range(22, 31):
        for x in range(2, 14):
            c = "cm5" if y == 22 else "cm4" if y < 25 else "cm3" if x < 10 else "cm2"
            if x in (2, 13) or y == 30:
                c = "cm0"
            P.px(x, y, c)
    for x in range(5, 16):
        if (x + 31) % 2 == 0 or x < 12:
            P.px(x, 31, CK.SHADOW.get(on, "ps"))
    rows = figure
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            c = {"#": "bz0", "h": "bz3", "m": "bz2", "d": "bz1", "g": "pg2", "r": "pr1", "v": "vg1"}.get(ch)
            if c:
                (T if 4 + j < 16 else P).px(2 + i, 4 + j, c)
    walk = ["T", "X"]
    s = cut(key, f"a bronze statue ({key})", W, H, {"middle": P, "top": T}, walk,
            names={"top": (0, 0), "base": (0, 1)}, on=on, section="town")
    return s


KODROS = [
    # the king who walked into the spears: helmet, round shield, a spear point down
    "....###.....",
    "...#rrr#....",
    "...#hhm#....",
    "....#mm#....",
    "...#hmmd#...",
    "..#hhmmdd#..",
    ".#h#hmmd##..",
    ".#h#hmmd#g#.",
    "..##hmmd#g#.",
    "...#hm#d#...",
    "...#hm#d#...",
    "...#h#.#d#..",
    "..#h#...#d#.",
    "..##.....##.",
    "............",
    "............",
    "............",
    "............",
]
KAIROS = [
    # the runner on the razor: winged heels, a lock of hair in front, scales
    "............",
    "....##......",
    "...#hm#.....",
    "..##hmd#....",
    ".#h#hmm#....",
    "#h#.#hmd##..",
    "....#hmmdd#g",
    "...#hmmd#.#g",
    "...#hm##...g",
    "..#hd#.#d#..",
    ".#hd#...#d#.",
    "#vh#.....#v#",
    "............",
    ".gggggggggg.",
    "............",
    "............",
    "............",
    "............",
]


def stall(key="stall", on="path"):
    """A market stall (2 x 2): a striped awning over a table of jars and fish;
    the awning on the top layer, the table solid."""
    W, H = 2, 2
    T = canvas(W, H)
    M_ = canvas(W, H)
    for y in range(4, 14):
        for x in range(1, 31):
            c = "pr1" if (x // 4) % 2 == 0 else "hw3"
            if y == 4:
                c = "ink"
            if y == 13:
                c = "tc0" if (x // 4) % 2 == 0 else "hw1"
            T.px(x, y, c)
    for y in range(14, 16):
        for x in (2, 29):
            T.px(x, y, "wd0")
    for y in range(16, 30):
        for x in (2, 29):
            M_.px(x, y, "wd0")
    for y in range(18, 27):
        for x in range(1, 31):
            c = "wd2" if y < 20 else "wd1"
            if y == 18:
                c = "wd0"
            if y == 26:
                c = "ink"
            M_.px(x, y, c)
    for jx in (5, 11, 19, 25):
        for y in range(16, 19):
            w = 2 if y < 15 else 3
            for x in range(jx - w, jx + w):
                M_.px(x, y, "tc3" if x < jx else "tc1")
    for x in range(4, 31):
        if (x + 27) % 2 == 0:
            M_.px(x, 28, "ps")
    s = cut(key, "a market stall", W, H, {"middle": M_, "top": T}, ["TT", "XX"],
            names={"TL": (0, 0), "TR": (1, 0), "BL": (0, 1), "BR": (1, 1)}, on=on, section="town")
    return s


def bema(key="bema", on="grass"):
    """The Pnyx's speaker's platform (3 x 2): a block cut from the living
    rock with three steps up its front; solid."""
    W, H = 3, 2
    L = canvas(W, H)
    for y in range(4, 30):
        for x in range(2, 46):
            c = rock_px(x, y)
            if y < 8:
                c = "ar5" if y == 4 else "ar4"
            if x in (2, 45) or y == 29:
                c = "ar0"
            L.px(x, y, c)
    for s_ in range(3):
        y = 18 + 4 * s_
        for x in range(16 - 2 * s_, 32 + 2 * s_):
            for j in range(4):
                L.px(x, y + j, "ar5" if j == 0 else "ar3" if j < 3 else "ar1")
    for x in range(6, 48):
        if (x + 30) % 2 == 0 or x < 40:
            L.px(x, 30, "gd")
    return cut(key, "the speaker's platform", W, H, {"middle": L}, ["XXX", "XXX"], on=on, section="town",
               names={"L": (0, 0), "M": (1, 0), "R": (2, 0), "BL": (0, 1), "B": (1, 1), "BR": (2, 1)},
               notes="The bema on the Pnyx (3 x 2), cut from the rock; solid. A sign on its front "
                     "(the vista).")


# --------------------------------------------------------------------------
# The harbor
# --------------------------------------------------------------------------

def quay(key="quay"):
    """The harbor's stone quay over borrowed sea: N (land to the north, its
    edge and the sea), W, E, S, the outer corners NW NE SW SE, a bollard on the
    quay (on borrowed path), and steps down to the water."""
    names = {"N": (0, 0), "NW": (1, 0), "NE": (2, 0), "W": (3, 0), "E": (4, 0), "S": (5, 0),
             "SW": (6, 0), "SE": (7, 0), "bollard": (0, 1), "steps": (1, 1), "ring": (2, 1)}
    s = struct(key, "the harbor quay", 8, 2, "harbor", walk=["XXXXXXXX", "X.X....."], names=names)
    for n in ("N", "NW", "NE", "W", "E", "S", "SW", "SE"):
        s.ground[names[n]] = "sea"
    for n in ("bollard", "steps", "ring"):
        s.ground[names[n]] = "path"
    for c in [(x, 1) for x in range(3, 8)]:
        s.ground[c] = "path"
    L = s.M
    q = lambda X, Y: "cm4" if (Y % 8 == 0 or (X + 4 * ((Y // 8) % 2)) % 8 == 0) and False else (
        "cm2" if (Y % 8 == 7 or (X + 4 * ((Y // 8) % 2)) % 8 == 7) else "cm4" if hp(X, Y, 6) % 5 else "cm3")

    def block(cx, cy, fn):
        for y in range(16):
            for x in range(16):
                c = fn(x, y)
                if c:
                    L.px(cx * 16 + x, cy * 16 + y, c)
    # land to the north of the N edge: the quay's stones down to 10, the edge, wet foot
    def north(x, y, corner=None):
        if corner == "W" and x < 4:
            return None
        if corner == "E" and x > 11:
            return None
        if y < 9:
            return q(x, y)
        if y == 9:
            return "cm5"
        if y < 13:
            return "cm2" if (x // 4) % 2 else "cm1"
        if y == 13:
            return "cm0"
        return None
    block(0, 0, lambda x, y: north(x, y))
    block(1, 0, lambda x, y: north(x, y, "W") if x >= 4 else ("cm0" if x == 4 and y < 14 else None))
    block(2, 0, lambda x, y: north(x, y, "E"))
    block(3, 0, lambda x, y: (q(x, y) if x > 6 else "cm1" if x > 3 else "cm0" if x == 3 else None))
    block(4, 0, lambda x, y: (q(x, y) if x < 9 else "cm2" if x < 12 else "cm0" if x == 12 else None))
    block(5, 0, lambda x, y: (q(x, y) if y > 6 else "cm5" if y == 6 else "cm0" if y == 5 else None))
    block(6, 0, lambda x, y: (q(x, y) if (y > 6 and x > 6) else "cm0" if (y == 5 and x > 5) or (x == 5 and y > 5) else None))
    block(7, 0, lambda x, y: (q(x, y) if (y > 6 and x < 9) else "cm0" if (y == 5 and x < 10) or (x == 10 and y > 5) else None))
    # a bronze-capped bollard, steps down to the water, a mooring ring
    block(0, 1, lambda x, y: ("bz1" if 5 <= x <= 10 and 4 <= y <= 12 else None))
    for (x, y) in ((6, 4), (7, 4), (8, 4), (9, 4)):
        L.px(x, 16 + y, "bz2")
    s.layers["middle"].a[16 + 4:16 + 13, 5:11] = s.layers["middle"].a[16 + 4:16 + 13, 5:11]
    # steps: drawn opaque on the bottom (stone treads into the water)
    for y in range(16):
        for x in range(16):
            t = y % 4
            s.B.px(16 + x, 16 + y, "cm5" if t == 0 else "cm4" if t == 1 else "cm3" if t == 2 else "cm1")
    s.ground.pop((1, 1), None)
    for x in range(5, 11):
        L.px(32 + x, 16 + 8, "bz1")
        L.px(32 + x, 16 + 9, "bz2" if x in (5, 10) else None) if x in (5, 10) else None
    # the bollard needs its own colors: bronze sits in the bronze group
    s.notes = ("The quay over borrowed sea: `N` (the quay to the north, its lit edge, the wet foot), "
               "corners, `W` `E` `S` edges; on the quay: `bollard`, `ring`; `steps` go down into the "
               "water (walkable).")
    return s


def ship_shed(key="ship_shed"):
    """A ship shed (3 x 3): a long tiled roof on stone piers over a slip that
    runs down into the water, a trireme's ram glinting in the dark."""
    W, H = 3, 3
    L = canvas(W, H)
    x1 = 47
    paint_roof(L, 0, x1, 2, 23)
    for y in range(24, 48):
        for x in range(0, 48):
            if x < 5 or x > 42:
                c = "hw3" if x in (1, 2, 44, 45) else "hw1"
                if x in (0, 47) or (y - 24) % 8 == 7:
                    c = "ink" if x in (0, 47) else "hw1"
                L.px(x, y, c)
            else:
                L.px(x, y, "cd0")
    # the slip's timber ways and a hull's prow in the dark
    for y in range(32, 48):
        for x in (14, 33):
            L.px(x, y, "wd1")
            L.px(x + 1, y, "wd0")
    for (x, y, c) in ((23, 38, "wd2"), (24, 38, "wd2"), (22, 39, "wd1"), (23, 39, "wd2"), (24, 39, "wd2"),
                      (25, 39, "wd1"), (21, 40, "wd1"), (22, 40, "wd2"), (25, 40, "wd1"), (26, 40, "wd0"),
                      (23, 41, "tc3"), (24, 41, "tc3"), (23, 42, "tc2"), (24, 42, "tc1")):
        L.px(x, y, c)
    return cut(key, "a ship shed", W, H, {"middle": L}, ["XXX", "XXX", "XXX"], on="sea", section="harbor",
               names={f"r{y}c{x}": (x, y) for y in range(H) for x in range(W)},
               notes="A ship shed (3 x 3) at the water: a tiled roof on stone piers, the slip's timber "
                     "ways running down into the dark, a ram's bronze. Solid; set its bottom row at the "
                     "waterline.")


def sea_door(key="sea_door"):
    """The salt spring's sea-door in the harbor's west rock (1 x 2 over
    borrowed sea at its foot): a sealed stone door in the cliff."""
    W, H = 1, 2
    L = canvas(W, H)
    for y in range(32):
        for x in range(16):
            L.px(x, y, rock_px(x, y))
    for y in range(8, 30):
        for x in range(3, 13):
            e = x in (3, 12) or y == 8
            L.px(x, y, "ar0" if e else "ar3" if (y - 8) % 6 else "ar1")
    for x in range(3, 13):
        L.px(x, 30, "ar0")
        L.px(x, 31, "ar1")
    return cut(key, "the sea-door", W, H, {"bottom": L}, ["X", "X"], on=None, section="harbor",
               names={"top": (0, 0), "door": (0, 1)},
               notes="The salt spring's sealed sea-door in the harbor rock (1 x 2). Solid; the bg "
                     "event sits on `door`.")


def gate_mat(key="gate_mat"):
    """The harbor road's threshold under the south gate: worn stone with a
    rut (south arrow warp: step south to go down to the harbor)."""
    s = struct(key, "the harbor gate threshold", 1, 1, "town", walk=["."], names={"mat": (0, 0)})
    for y in range(16):
        for x in range(16):
            c = "ar4" if (y % 8) else "ar3"
            if x in (4, 11):
                c = "ar2"
            if (x + 8 * ((y // 8) % 2)) % 16 == 0:
                c = "ar2"
            s.B.px(x, y, c)
    s.behaviors[(0, 0)] = "MB_SOUTH_ARROW_WARP"
    return s


def city_structures():
    by = {}
    akro = AA.parthenon()
    by["skyline_parthenon"] = crop(akro, "skyline_parthenon", 0, 0, 14, 4, title="the Parthenon over the wall",
                                   notes="The Parthenon's pediment, frieze and capitals over the Akropolis "
                                         "wall (14 x 4; the same art as gTileset_Akropolis). Solid.")
    import astyra_statues as ST
    pro = ST.promachos()
    sk = crop(pro, "skyline_promachos", 0, 0, 4, 5, title="Athena Promachos over the wall",
              notes="Promachos from the city (4 x 5): crest, helmet, aegis, the owl shield and the spear "
                    "with its gleaming tip (animation `glint`), standing behind the Akropolis wall. "
                    "Solid scenery.", walk=["XXXX"] * 5)
    # in the city she is scenery: her art moves from the top layer to the middle
    sk.M.a[:] = np.where(sk.T.a[..., 3:4] > 0, sk.T.a, sk.M.a)
    sk.T.a[:] = 0
    for an in sk.anims.values():
        an["layer"] = "middle"
    by["skyline_promachos"] = sk
    cl = AA.cliff("path", key="cliff", section="rock", foot_on="grass")
    by["cliff"] = K.pick(cl, ["face", "face_b", "face_W", "face_E", "foot", "foot_b", "foot_W", "foot_E",
                              "rock"], w=4, key="cliff",
                         notes="The rock's face from the city, under the Akropolis wall: `face` `face_b` "
                               "(repeat them), `foot` `foot_b` on the grass with the cast shadow, `_W` "
                               "and `_E` ends, `rock` solid. All solid.")
    by["akro_wall"] = akro_wall()
    by["rock_stair"] = rock_stair()
    by["stoa"] = stoa()
    by["library"] = library()
    by["asclepeion"] = asclepeion()
    by["house"] = house_kit()
    cw = city_wall()
    by["city_wall"] = K.pick(cw, ["v", "v_end_N", "v_end_S", "tower_TL", "tower_TR", "h_top", "h_L", "h_R",
                                  "tower_BL", "tower_BR", "h_face", "h_face_b", "gate_top", "gate_face"],
                             w=7, key="city_wall", notes=cw.notes)
    by["fountain"] = fountain()
    by["kodros"] = ST.hero_statue("kodros", ST.KODROS, "Kodros, the last king")
    by["kairos"] = ST.hero_statue("kairos", ST.KAIROS, "Kairos, the Moment")
    by["altar"] = AA.altar(key="altar", on="path", section="town")
    by["stall"] = stall()
    by["bema"] = bema()
    by["kerameikos"] = K.pick(CK.ruins("marble", "grass", key="kerameikos"),
                              ["stub", "plinth_feet", "poppies"], w=3, key="kerameikos",
                              notes="The Kerameikos's broken grave monuments, on borrowed grass: `stub`, "
                                    "`plinth_feet`, `drum` (solid), `poppies` (walkable).")
    by["quay"] = quay()
    by["ship_shed"] = ship_shed()
    by["sea_door"] = sea_door()
    by["gate_mat"] = gate_mat()
    return by


def sections(by):
    return [
        ("rock", [by["skyline_parthenon"], by["skyline_promachos"], by["cliff"], by["akro_wall"],
                  by["rock_stair"]]),
        ("town", [by["stoa"], by["library"], by["asclepeion"], by["house"], by["city_wall"],
                  by["fountain"], by["kodros"], by["kairos"], by["altar"], by["stall"], by["bema"],
                  by["kerameikos"]]),
        ("harbor", [by["quay"], by["ship_shed"], by["sea_door"]]),
    ]


if __name__ == "__main__":
    by = city_structures()
    out = K.ROOT / "build/astyra_art"
    out.mkdir(parents=True, exist_ok=True)
    K.shelf_preview(list(by.values()), scale=2, width=1800).save(out / "astyra_pieces.png")
    print(out / "astyra_pieces.png", len(K.tiles_of(list(by.values()))))
    for k, s in by.items():
        print(k, s.w, s.h, len(K.tiles_of([s])))
