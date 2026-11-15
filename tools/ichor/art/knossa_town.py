"""Amnisos: the Minoan house kit with a hive on every roof, the harbor shrine,
and the Titans' triremes at the mole.

The house kit follows the Town Mosaic, the faience plaques of Minoan house
fronts found at Knossos: plastered walls banded with timber, the round ends
of the floor beams showing in a row, windows of four red-painted panes, and
flat roofs of beaten earth. Amnisos keeps bees on every roof (LABYRINTH §2):
horizontal clay hive-tubes stacked in threes, the Minoan kind, and domed
straw skeps, with bees about their mouths (the `bees` animation).

The kit is parts on a grid, like Kythera's: a roof row (R), an upper wall (U)
and a ground-floor wall (G), each in columns L (the lit west corner), M (it
repeats) and R (the shaded east corner). Textures lock to the 16 px grid, so
any part sits beside any other in its row; FRONTS are arrangements of parts.
Every pixel is in the `minoan` group (the labyrinth's own reds, ochres,
gypsum and black).
"""
from __future__ import annotations

import knossa_lib as N
from knossa_lib import anim_layer, ground, grid, struct

SEC = "town"


# --------------------------------------------------------------------------
# Textures
# --------------------------------------------------------------------------

def plaster(X, Y):
    """Lime plaster, warm white, 16 px periodic, a few soft trowel marks."""
    x, y = X % 16, Y % 16
    if (x, y) in ((3, 4), (4, 4), (12, 9), (13, 10), (7, 13), (1, 10), (10, 2)):
        return "mg1"
    return "mg2"


ROOF = [
    "................",
    "......ggg.......",
    "..........d.....",
    "...gg......gg...",
    "................",
    ".d..........gg..",
    "......gggg......",
    "................",
    "..gg........d...",
    "................",
    "........gg......",
    "....d...........",
]


def roof_px(x, y):
    """Beaten-earth roof, sun-baked clay plaster, 16 px periodic: smooth, with
    a few pale trowel strokes and the odd crack."""
    ch = ROOF[(y - 3) % len(ROOF)][x] if 3 <= y else "."
    return {"g": "mg2", "d": "mo1"}.get(ch, "mo2")


def roof_cell(L, ox, oy, side):
    for y in range(16):
        for x in range(16):
            if y == 0:
                c = "mt0"
            elif y == 1:
                c = "mo1"
            elif y == 2:
                c = "mo2" if x % 5 else "mg2"
            elif y <= 11:
                c = roof_px(x, y)
            elif y == 12:
                c = "mg2"           # the front parapet's lit top
            elif y == 13:
                c = "mg1"
            elif y == 14:
                c = "mo1"           # its face
            else:
                c = "mt0"           # the cornice beam's shadow
            L.px(ox + x, oy + y, c)
    if side == "L":
        for y in range(16):
            L.px(ox, oy + y, "mt0")
            L.px(ox + 1, oy + y, "mg2" if 0 < y < 14 else L.get(ox + 1, oy + y))
    if side == "R":
        for y in range(16):
            L.px(ox + 15, oy + y, "mt0")
            L.px(ox + 14, oy + y, "mo1" if 0 < y < 15 else "mt0")


def beam_band(L, ox, oy, y0):
    """A floor beam across the front: a dark timber band, the round ends of
    the joists showing in a row."""
    for x in range(16):
        L.px(ox + x, oy + y0, "mt0")
        L.px(ox + x, oy + y0 + 1, "mt1" if x % 4 else "mt0")
        L.px(ox + x, oy + y0 + 2, "mt0")
    for x in (1, 5, 9, 13):
        L.px(ox + x, oy + y0 + 1, "mo1")
        L.px(ox + x + 1, oy + y0 + 1, "mt2")


def wall_cell(L, ox, oy, row, side):
    for y in range(16):
        for x in range(16):
            L.px(ox + x, oy + y, plaster(ox + x, oy + y))
    if row == "U":
        beam_band(L, ox, oy, 0)
        for x in range(16):
            L.px(ox + x, oy + 3, "mg1")
    if row == "G":
        beam_band(L, ox, oy, 0)
        for x in range(16):
            L.px(ox + x, oy + 3, "mg1")
            # the ochre dado and the gypsum socle at the foot
            L.px(ox + x, oy + 11, "mo0")
            L.px(ox + x, oy + 12, "mo1")
            L.px(ox + x, oy + 13, "mg0" if (x + 3) % 8 == 0 else "mg1")
            L.px(ox + x, oy + 14, "mg0" if (x + 3) % 8 == 0 else "mg1")
            L.px(ox + x, oy + 15, "mg0")
    if side == "L":
        for y in range(16):
            L.px(ox, oy + y, "mt0")
            if L.get(ox + 1, oy + y) == "mg2":
                L.px(ox + 1, oy + y, "mg2")
    if side == "R":
        for y in range(16):
            L.px(ox + 15, oy + y, "mt0")
            c = L.get(ox + 14, oy + y)
            L.px(ox + 14, oy + y, {"mg2": "mg1", "mg1": "mg0", "mo1": "mo0", "mt1": "mt0"}.get(c, c))


def window(L, ox, oy, y0=5, small=False):
    """A Town Mosaic window: four panes painted red in a timber frame."""
    if small:
        grid(L, ox + 4, oy + y0, [
            "kkkkkkkk",
            "kRrkRrkk",
            "kr1kr1kk",
            "kkkkkkkk",
            "kRrkRrkk",
            "kr1kr1kk",
            "kkkkkkkk",
            "gggggggg",
        ], {"k": "mt0", "R": "mr2", "r": "mr1", "1": "mr0", "g": "mg0"})
        return
    grid(L, ox + 3, oy + y0, [
        "kkkkkkkkkk",
        "kRRrkkRRrk",
        "kRrr1kRrr1",
        "kr111kr111",
        "kkkkkkkkkk",
        "kRRrkkRRrk",
        "kRrr1kRrr1",
        "kr111kr111",
        "kkkkkkkkkk",
        ".gggggggg.",
    ], {"k": "mt0", "R": "mr2", "r": "mr1", "1": "mr0", "g": "mg0"})


def door(L, ox, oy, sign=False):
    """A timber door in a red-painted frame, a gypsum step below."""
    x0, x1, top = 3, 12, 4
    for y in range(top, 15):
        for x in range(x0, x1 + 1):
            if x in (x0, x1):
                c = "mr1" if x == x0 else "mr0"
            elif y == top:
                c = "mr2"
            elif y == top + 1:
                c = "mr1"
            else:
                pl = (x - x0 - 1) % 3
                c = ("mt1", "mt0", "mt1")[pl]
                if pl == 1:
                    c = "mt0"
                elif y in (top + 4, top + 8):
                    c = "mt0"
                elif x == x0 + 1:
                    c = "mt2"
            L.px(ox + x, oy + y, c)
    L.px(ox + x1 - 2, oy + 10, "mo1")      # bronze ring handle
    L.px(ox + x1 - 2, oy + 11, "mo0")
    for x in range(x0 - 1, x1 + 2):         # the step
        L.px(ox + x, oy + 15, "mg0")
        L.px(ox + x, oy + 14, "mg2" if x0 <= x <= x1 else L.get(ox + x, oy + 14))
    if sign:
        # The Double Axe: a board hung from the beam, a red labrys on it
        grid(L, ox + 0, oy + 3, [
            ".k.......",
            "kkkkkkkk.",
            "kmmmmmmmk",
            "kmrmmmrmk",
            "kmrrrrrmk",
            "kmrmrmrmk",
            "kmmmrmmmk",
            "kmmmrmmmk",
            "kkkkkkkkk",
        ], {"k": "mt0", "m": "mg2", "r": "mr1"})


def hive_tubes(L, ox, oy):
    """Three horizontal clay hive-tubes stacked on a gypsum slab, lying north
    to south: each shows its top running back and its round lid at the
    front, a small dark hole in it for the bees."""
    for x in range(1, 16):
        L.px(ox + x, oy + 14, "mg0")
        L.px(ox + x, oy + 15, "mt0" if x in (1, 15) else "mg1")
    tube = [
        "..kkkk..",
        ".k2211k.",
        ".k2211k.",
        ".k2211k.",
        "kk2211kk",
        "k211110k",
        "k21bb10k",
        "k211100k",
        ".k1000k.",
        "..kkkk..",
    ]
    lg = {"k": "mt0", "1": "mt1", "2": "mt2", "0": "mt0", "b": "mb"}
    grid(L, ox + 4, oy + 0, tube, lg)
    grid(L, ox + 0, oy + 5, tube, lg)
    grid(L, ox + 8, oy + 5, tube, lg)


def skeps(L, ox, oy):
    """Two domed straw skeps on a flat stone."""
    for x in range(1, 15):
        L.px(ox + x, oy + 14, "mg0")
        L.px(ox + x, oy + 13, "mg1")
    skep = [
        "..kkk..",
        ".k221k.",
        "k22111k",
        "k00000k",
        "k21110k",
        "k22111k",
        "k00000k",
        "k21110k",
        "kk1bb0k",
        ".kkbbkk",
    ]
    lg = {"k": "mo0", "2": "mo2", "1": "mo1", "0": "mo0", "b": "ink"}
    grid(L, ox + 1, oy + 3, skep, lg)
    grid(L, ox + 8, oy + 4, skep[:-1], lg)


def bees(frames, ox, oy, spots):
    """Paint bees (one dark pixel, a pale wing) about a hive into each frame:
    `spots` lists per frame the (x, y) of each bee."""
    for f, pts in zip(frames, spots):
        for (x, y) in pts:
            f.px(ox + x, oy + y, "ink")
            f.px(ox + x, oy + y - 1, "mg2")


def horns(L, ox, oy, y0=4):
    """Horns of consecration on the parapet: the stone of the bull's horns."""
    grid(L, ox + 2, oy + y0, [
        "kk........kk",
        "k2k......k1k",
        "k2k......k1k",
        "k22k....k11k",
        "k222kkkkk11k",
        "k22222221110",
        "kkkkkkkkkkkk",
    ], {"k": "mb", "2": "mg2", "1": "mg1", "0": "mg0"})


def ladder(L, ox, oy, y0, y1):
    for y in range(y0, y1):
        for x in (4, 11):
            L.px(ox + x, oy + y, "mt0")
            L.px(ox + x + 1, oy + y, "mt1")
        if (y - y0) % 4 == 2:
            for x in range(5, 11):
                L.px(ox + x, oy + y, "mt1")
            L.px(ox + 5, oy + y + 1, "mt0")


def pithos(L, ox, oy):
    """A storage jar against the wall: rope bands in relief, wavy line."""
    grid(L, ox + 3, oy + 1, [
        "...kkkkkk...",
        "..k222211k..",
        "...k2110k...",
        "..k221110k..",
        ".k22111100k.",
        "k2221111100k",
        "k2k1kk1kk00k",
        "k221111110.k",
        "k21r1r1r100k",
        "k2r1r1r1r10k",
        "k22111111100",
        ".k211111100k",
        "kk2kk1kkk0kk",
        ".k21111100k.",
        "..k111100k..",
    ], {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0", "r": "mr1"})


def octopus_pots(L, ox, oy):
    """Clay octopus traps stacked at the wall's foot, an octopus drying on a
    line above them (the fisher's hut)."""
    for x in range(1, 15):
        L.px(ox + x, oy + 3, "mt0")
    grid(L, ox + 4, oy + 4, [
        "..rr..",
        ".rRRr.",
        "rRrrRr",
        "rr11rr",
        ".r1r1.",
        "r.r.r.",
        ".r..r.",
    ], {"r": "mr1", "R": "mr2", "1": "mr0"})
    pot = [".kk.", "k21k", "k11k", "kbbk", ".kk."]
    lg = {"k": "mt0", "2": "mt2", "1": "mt1", "b": "mb"}
    for (x, y) in ((1, 10), (5, 10), (9, 10), (3, 7), (7, 7), (11, 11)):
        grid(L, ox + x, oy + y, pot, lg)


# --------------------------------------------------------------------------
# The kit
# --------------------------------------------------------------------------

def house_kit():
    names = {
        "R_L": (0, 0), "R_M": (1, 0), "R_R": (2, 0), "R_hive": (3, 0), "R_skep": (4, 0),
        "R_horns": (5, 0), "R_ladder": (6, 0), "R_jar": (7, 0),
        "U_L": (0, 1), "U_M": (1, 1), "U_R": (2, 1), "U_window": (3, 1), "U_windows": (4, 1),
        "U_frieze": (5, 1), "U_ladder": (6, 1), "U_window_R": (7, 1),
        "G_L": (0, 2), "G_M": (1, 2), "G_R": (2, 2), "door": (3, 2), "door_axe": (4, 2),
        "G_window": (5, 2), "G_ladder": (6, 2), "G_pithos": (7, 2),
        "G_octopus": (0, 3), "G_bench": (1, 3), "R_hive_L": (2, 3), "R_hive_R": (3, 3),
        "G_window_R": (4, 3), "G_hives": (5, 3), "G_steps": (6, 3), "R_steps": (7, 3),
    }
    s = struct("house", "The Minoan house kit", 8, 4, SEC,
               walk=["XXXXXX.X", "XXXXXX.X", "XXXDDX.X", "XXXXXX.."],
               names=names,
               notes="Parts that snap together into Amnisos's houses (see *House fronts* below): "
                     "plastered walls banded with timber, the joists' round ends in a row, windows "
                     "of four red-painted panes, flat roofs of beaten earth. Rows: `R_*` the flat "
                     "roof and its parapet, seen from above; `U_*` the upper wall; `G_*` and the "
                     "doors, the ground-floor wall over its ochre dado and gypsum socle. Columns "
                     "`_L` (the lit west corner), `_M` (repeat it), `_R` (the shaded east corner). "
                     "**A hive on every roof** (LABYRINTH §2): `R_hive` (three clay hive-tubes, "
                     "the Minoan kind), `R_skep` (two straw skeps), and `R_hive_L` / `R_hive_R`, "
                     "the tubes at a roof's corners; bees fly at their mouths (the `bees` "
                     "animation). Roof extras: `R_horns` (horns of consecration on the parapet, "
                     "for the grander houses), `R_ladder` (a ladder's top over the parapet), "
                     "`R_jar` (a water jar). Upper wall: `U_window` (four red panes), "
                     "`U_window_R` (the same at the shaded corner), `U_windows` (two small ones), "
                     "`U_frieze` (a painted band of running spirals), `U_ladder`. Ground floor: "
                     "`door` and `door_axe` (`MB_NON_ANIMATED_DOOR`; `door_axe` hangs the "
                     "tavern's board with its red double axe), `G_window`, `G_window_R`, "
                     "`G_ladder`, `G_steps` (an outside stair climbing the wall west to east, arriving at `R_steps` on the roof), `G_pithos` (a storage jar against the wall), `G_octopus` "
                     "(octopus traps stacked by the wall, one drying on a line: the fisher's "
                     "hut), `G_bench` (a gypsum bench), `G_hives` (hive-tubes built into the "
                     "wall, Kydon's honey house). **The ladder** (`G_ladder`, `U_ladder`, "
                     "`R_ladder` in one column) climbs to a roof: its cells are walkable. To make a "
                     "roof a terrace to stand on, set its plain roof cells passable at a higher elevation than the street and the ladder elevation 0, as "
                     "for stairs, so the player can only get up by the ladder (the kid by the "
                     "hives waits up there). Every other cell is impassable.")
    L = s.B
    for cx, side in ((0, "L"), (1, "M"), (2, "R"), (3, "M"), (4, "M"), (5, "M"), (6, "M"),
                     (7, "M")):
        roof_cell(L, cx * 16, 0, side)
        wall_cell(L, cx * 16, 16, "U", side)
        wall_cell(L, cx * 16, 32, "G", side)
    for cx, side in ((0, "M"), (1, "M"), (2, "L"), (3, "R"), (4, "R"), (5, "M"), (6, "L")):
        wall_cell(L, cx * 16, 48, "G", side)
    # roof extras on the middle layer, so a hive can stand on any roof cell
    M = s.M
    hive_tubes(M, 48, 0)
    skeps(M, 64, 0)
    horns(M, 80, 0)
    ladder(M, 96, 0, 6, 16)
    for x in range(96 + 3, 96 + 13):
        M.px(x, 5, "mt0")
    grid(M, 112 + 4, 2, [
        "..kkkk..",
        ".k2222k.",
        "kmbbbbmk",
        "k211110k",
        "k211110k",
        "k211100k",
        ".k1110k.",
        "..kkkk..",
        ".gggggg.",
    ], {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0", "m": "mt1", "b": "mb", "g": "mo1"})
    # roof corners: the corner roof cells with tubes on them, rebuilt as roof
    roof_cell(L, 32, 48, "L")
    roof_cell(L, 48, 48, "R")
    hive_tubes(M, 32, 48)
    hive_tubes(M, 48, 48)
    # upper wall extras
    window(L, 48, 16)
    window(L, 64, 16, small=True)
    window(L, 112, 16)
    for y in range(16, 32):            # the shaded corner on U_window_R
        c = L.get(112 + 15, y)
        L.px(112 + 15, y, "mt0")
        c = L.get(112 + 14, y)
        L.px(112 + 14, y, {"mg2": "mg1", "mg1": "mg0"}.get(c, c))
    # the frieze: red running spirals on an ochre band
    for x in range(16):
        for y in range(6, 12):
            L.px(80 + x, 16 + y, "mo2" if y in (7, 10) else "mo1")
        L.px(80 + x, 16 + 6, "mt0")
        L.px(80 + x, 16 + 11, "mt0")
    for k in range(2):
        grid(L, 80 + k * 8, 16 + 7, [
            ".rrr....",
            "r..r.rr.",
            "r.rr.r.r",
            ".r..rrr.",
        ], {"r": "mr1"})
    ladder(M, 96, 16, 0, 16)
    # ground floor extras
    door(L, 48, 32)
    door(L, 64, 32, sign=True)
    window(L, 80, 32, y0=4, small=True)
    ladder(M, 96, 32, 0, 15)
    for x in range(96 + 3, 96 + 13):
        M.px(x, 32 + 15, "mg0")
    pithos(L, 112, 32)
    octopus_pots(L, 0, 48)
    grid(L, 16 + 1, 48 + 7, [
        "mmmmmmmmmmmmmm",
        "22222222222222",
        "0.k........k.0",
        "0.k........k.0",
    ], {"m": "mg1", "2": "mg2", "0": "mg0", "k": "mb"})
    window(L, 64, 48, y0=4, small=True)
    # G_hives: the honey house's wall of hive-tubes, mouths out
    for (x, y) in ((1, 4), (6, 4), (11, 4)):
        grid(L, 80 + x, 48 + y, [".kkk.", "k211k", "k1bbk", "k1b0k", ".kkk."],
             {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0", "b": "ink"})
    # bees at the hives (3 frames, ping-pong-ish order in knossa_build)
    frames = anim_layer(s, "bees", 3)
    allf = [M] + frames
    hive_bees = [
        [(3, 9), (13, 5), (8, 3)],
        [(1, 7), (14, 9), (10, 1)],
        [(4, 4), (12, 3), (6, 10)],
    ]
    for f, pts in zip(allf, hive_bees):
        for (x, y) in pts:
            for (ox, oy) in ((48, 0), (32, 48), (48, 48)):
                f.px(ox + x, oy + y, "ink")
                f.px(ox + x, oy + y - 1, "mg2")
    skep_bees = [[(4, 13), (13, 2), (8, 1)], [(2, 11), (14, 6), (11, 0)],
                 [(6, 12), (12, 11), (6, 1)]]
    for f, pts in zip(allf, skep_bees):
        for (x, y) in pts:
            f.px(64 + x, y, "ink")
            f.px(64 + x, y - 1, "mg2")
    # the wall hives' bees are drawn on the wall: put them in the bottom layer's
    # frames by moving the cell's art up a layer
    for y in range(48, 64):
        for x in range(80, 96):
            M.a[y, x] = L.a[y, x]
    for f, pts in zip(allf, [[(4, 2), (13, 12)], [(9, 3), (3, 12)], [(14, 3), (8, 13)]]):
        for (x, y) in pts:
            f.px(80 + x, 48 + y, "ink")
            f.px(80 + x, 48 + y - 1, "mg2")
    N.settle(s, "bees", [(3, 0), (4, 0), (2, 3), (3, 3), (5, 3)])
    # an outside stair, west to east, and its arrival on the roof
    for i in range(6):
        for y in range(16 - (i + 1) * 2, 16):
            for x in range(96 + 1 + i * 2, 96 + 3 + i * 2):
                if y == 16 - (i + 1) * 2:
                    c = "mg2"
                elif y == 16 - (i + 1) * 2 + 1:
                    c = "mg1"
                else:
                    c = "mg1" if x % 2 else "mg0"
                L.px(x, 48 + y, c)
        L.px(96 + 3 + i * 2, 48 + 16 - (i + 1) * 2, "mg0")
    roof_cell(L, 112, 48, "M")
    for y in range(12, 16):
        for x in range(1, 13):
            L.px(112 + x, 48 + y, ("mg2", "mg1", "mg1", "mg0")[y - 12])
    s.behaviors = {(3, 2): "MB_NON_ANIMATED_DOOR", (4, 2): "MB_NON_ANIMATED_DOOR"}
    return s


# House fronts: arrangements of the kit's parts. Each front has a door.
FRONTS = {
    "honey_house": {
        "title": "Kydon's honey house", "who": "Kydon's: hive-tubes in the wall, skeps and tubes on "
        "the roof (the Honey gift)", "kit": "house",
        "rows": [["R_L", "R_hive", "R_skep", "R_hive_R"],
                 ["U_L", "U_window", "U_M", "U_window_R"],
                 ["G_L", "G_hives", "door", "G_R"]]},
    "tavern": {
        "title": "The Double Axe", "who": "the tavern, its board hung by the door (the "
        "knucklebones champion)", "kit": "house",
        "rows": [["R_hive_L", "R_M", "R_jar", "R_skep", "R_R"],
                 ["U_L", "U_windows", "U_frieze", "U_window", "U_R"],
                 ["G_L", "G_pithos", "door_axe", "G_window", "G_R"]]},
    "xenia_house": {
        "title": "Aithon's house", "who": "the xenia host's, horns on the parapet (rest until a "
        "chosen hour)", "kit": "house",
        "rows": [["R_L", "R_hive", "R_horns", "R_skep", "R_R"],
                 ["U_L", "U_window", "U_frieze", "U_window", "U_R"],
                 ["G_L", "G_window", "door", "G_bench", "G_R"]]},
    "leaper_house": {
        "title": "The old leaper's house", "who": "Euanthe's, Sarpedon's wife: a ladder to the "
        "roof, where the kid by the hives waits", "kit": "house",
        "rows": [["R_L", "R_M", "R_ladder", "R_hive_R"],
                 ["U_L", "U_windows", "U_ladder", "U_window_R"],
                 ["G_L", "door", "G_ladder", "G_R"]]},
    "fisher_hut": {
        "title": "Polypos's hut", "who": "the fisher's: octopus traps and a catch drying (a "
        "trade, and the bean story)", "kit": "house",
        "rows": [["R_hive_L", "R_skep", "R_R"],
                 ["G_octopus", "door", "G_window_R"]]},
}


# --------------------------------------------------------------------------
# The harbor shrine
# --------------------------------------------------------------------------

def shrine():
    s = struct("shrine", "The harbor shrine", 1, 2, SEC, walk=["T", "X"],
               names={"top": (0, 0), "base": (0, 1)},
               notes="Amnisos's harbor shrine at the quay's end: a gypsum pillar under horns of "
                     "consecration, a red double axe painted on its face, a honey jar at its foot "
                     "(on borrowed path). `top` is drawn over the player; `base` is impassable and "
                     "takes the bg event. The Bronze Obol is hidden behind it.")
    ground(s, "path")
    T, M = s.T, s.M
    art = [
        "................",
        "...kk.......kk..",
        "...k2k.....k1k..",
        "...k22kkkkk11k..",
        "...k222222110k..",
        "...kkkkkkkkkkk..",
        "....k222221k....",
        "....k2kkk21k....",
        "....k22222kk....",
        "....kkkkkkkk....",
        "....k22222100k..",
        "....k22222100k..",
        "....kr222r100k..",
        "....krr2rr100k..",
        "....krrrrr100k..",
        "....krr2rr100k..",
        "....kr2r2r100k..",
        "....k22r22100k..",
        "....k22222100k..",
        "....k22222100k..",
        "...kkkkkkkkkkkk.",
        "...k22222222110k",
        "...k11111111000k",
        "..jjkkkkkkkkkkk.",
        ".jJjj...........",
        "j2Jjjj..........",
        "jJjjjj..........",
        "jjjj0j..........",
        ".jjjj...........",
        "................",
        "................",
        "................",
    ]
    for j, row in enumerate(art):
        for i, ch in enumerate(row):
            c = {"k": "mb", "2": "mg2", "1": "mg1", "0": "mg0", "r": "mr1", "j": "mt1",
                 "J": "mt2"}.get(ch)
            if c:
                (T if j < 16 else M).px(i, j, c)
    # fix the honey jar: the rim dark, the honey showing gold
    for (x, y) in ((1, 24), (2, 24)):
        M.px(x, y, "mo1")
    return s


# --------------------------------------------------------------------------
# The Titans' triremes
# --------------------------------------------------------------------------

def titan_trireme():
    """The Euploia's hull (akti_art's), tarred black for the Titans: a slate
    sail furled on the yard with a sickle chalked on it, grey shields, no red."""
    import kythera_harbor as H
    src = H.trireme()
    s = struct("titan_trireme", "A Titan trireme, furled", src.w, src.h, "harbor",
               walk=list(src.walk), names={"bow": (7, 1), "stern": (0, 1)},
               notes="One of the four Titan triremes moored at Amnisos's mole (SCRIPT.md III-3A): "
                     "black-tarred, her slate sail furled on the yard with a sickle chalked on it, "
                     "no crew on deck. 8 x 3 on borrowed sea, bow to the east; moor four along the "
                     "mole's north side, each wholly on sea cells. Impassable. **Sailed:** when "
                     "`FLAG_ICHOR_HIDE_TITAN_SHIPS` is set (after the Turning), swap each ship's "
                     "24 cells to aethos sea (`0x170`): nothing is left at the mole.")
    for ln in ("bottom", "middle", "top"):
        s.layers[ln].a[:] = src.layers[ln].a
    s.ground = dict(src.ground)
    N.recolor(s, {"wd2": "wd1", "wd3": "wd2", "rs1": "tc0", "tc1": "kr1", "tc2": "kr2",
                  "tc3": "kr2"})
    N.recolor(s, {"wd1": "wd0"})
    M = s.M
    # the sickle, chalked on the furled sail
    grid(M, 56, 8, [
        "..www...",
        ".w..ww..",
        "w.....w.",
        "......w.",
        ".....w..",
        "...ww...",
        "..w.....",
    ], {"w": "w0"})
    return s


def build():
    return [house_kit(), shrine(), titan_trireme()]
