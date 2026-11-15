"""The Palace of Minos's four rooms (LABYRINTH §3, §8; SCRIPT.md Part 2) and
the Bull Road vault: the Throne Room (the gypsum throne, benches, the
griffins, the lustral basin), the West Magazines (rows of giant pithoi, cists,
the Titans' camp), the Queen's Megaron (the dolphin fresco, Ariadne's bed and
bath, a light well) and the Grand Staircase (flights going down past a red
balustrade into the dark, to Ring I). The vault is a corbelled chamber
painted with lilies.

Like the labyrinth tileset, it draws all its own ground (every bottom layer
opaque, palettes 6-12 only), so it works on any primary; it is meant for
oikos, as the Labyrinth is, and its rooms' gypsum, red and fresco blue are the
Labyrinth's own colors.

The house kit is the labyrinth's shape: a north wall three rows tall (a
painted frieze, a plaster field where frescoes hang, a dado of veined gypsum
slabs), side walls as dark strips, the south wall's threshold, the void.
"""
from __future__ import annotations

import math

import knossa_lib as N
import knossa_palace as P
from knossa_lib import grid, struct

SEC = "rooms"


def floor_cell(L, ox, oy, name="A", seed=0, shade=False):
    P.pave(L, ox, oy, name, seed=seed)
    if shade:
        for y in range(16):
            for x in range(16):
                if y < 6:
                    c = L.get(ox + x, oy + y)
                    L.px(ox + x, oy + y, {"mg2": "mg1", "mg1": "mg0", "mt2": "mt1"}.get(c, c))


def house():
    names = {"void": (0, 0), "floor_A": (1, 0), "floor_B": (2, 0), "floor_C": (3, 0),
             "floor_D": (4, 0), "shade": (5, 0), "shade_b": (6, 0), "rug": (7, 0),
             "frieze_L": (0, 1), "frieze": (1, 1), "frieze_R": (2, 1), "field": (3, 1),
             "field_red": (4, 1), "dado": (5, 1), "dado_b": (6, 1), "door": (7, 1),
             "field_L": (0, 2), "field_R": (2, 2), "dado_L": (3, 2), "dado_R": (4, 2),
             "side_W": (5, 2), "side_E": (6, 2), "exit": (7, 2), "door_top": (1, 2),
             "south_W": (0, 3), "south": (1, 3), "south_E": (2, 3), "lilies": (3, 3),
             "lilies_red": (4, 3), "corbel": (5, 3), "niche": (6, 3), "lamp": (7, 3)}
    s = struct("house", "The rooms' floors and walls", 8, 4, SEC,
               walk=["X.......", "XXXXXXXD", "XXXXXXXX", "XXXXXXXX"], names=names,
               notes="The house kit for every palace room. **Floors** (walkable): gypsum slabs "
                     "set in red plaster, `floor_A` to `floor_D` in a mix, `shade` / `shade_b` "
                     "for the row in front of the north wall, `rug` (a woven runner). `void` is "
                     "the black outside the rooms (the layout's border; block it). **The north "
                     "wall** is three rows tall: `frieze_*` (a band of red, black and ochre "
                     "under the ceiling beam), over `field` (white plaster, where frescoes "
                     "hang; `field_red` is the red-painted kind), over `dado` (veined gypsum "
                     "slabs on a baseboard; `dado_b` a slab with a mason's double axe). `_L` "
                     "and `_R` turn the wall into the side walls. `door_top` over `door` is a "
                     "doorway in the north wall to the next room (`MB_NON_ANIMATED_DOOR`, put "
                     "the warp on `door`). **Side walls**: `side_W` `side_E`, dark strips beside "
                     "the floor; the south wall is `south_W` `south` `south_E`, its doorway "
                     "`exit` (`MB_SOUTH_ARROW_WARP`, the warp out). **The Bull Road vault**: "
                     "`lilies` and `lilies_red`, a field painted with lilies, bright as the day "
                     "they were done; `corbel`, the vault's corbelled stone overhead in place "
                     "of a frieze; `niche`, a lamp niche in a field; `lamp`, a clay lamp on a "
                     "bracket.")
    B, M, Tl = s.B, s.M, s.T
    B.rect(0, 0, 16, 16, "ink")
    for i, n in enumerate("ABCD"):
        floor_cell(B, 16 + i * 16, 0, n, seed=i)
    floor_cell(B, 80, 0, "A", shade=True)
    floor_cell(B, 96, 0, "C", shade=True, seed=2)
    floor_cell(B, 112, 0, "D")
    for y in range(16):     # the rug: a red runner with a blue border and rosettes
        for x in range(2, 14):
            c = "mr1"
            if x in (2, 13):
                c = "mt0"
            elif x in (3, 12):
                c = "mo1"
            elif (y % 8) in (3, 4) and 6 <= x <= 9:
                c = "mo1" if x in (7, 8) else "mr2"
            B.px(112 + x, y, c)

    def frieze(ox, oy):
        for y in range(16):
            for x in range(16):
                if y < 3:
                    c = ("ink", "mt0", "mt1")[y]
                elif y < 5:
                    c = "mb"
                elif y < 11:
                    k = (x + (y - 5) * 2) % 8
                    c = "mo1" if y in (5, 10) else ("mr1" if k < 4 else "mr2")
                    if y in (7, 8) and x % 8 in (2, 3, 4):
                        c = "mg2"
                elif y < 13:
                    c = "mb"
                else:
                    c = "mg2" if y == 13 else "mg1"
                B.px(ox + x, oy + y, c)

    def field(ox, oy, red=False):
        for y in range(16):
            for x in range(16):
                if red:
                    c = "mr1" if (x * 3 + y * 7) % 23 else "mr2"
                else:
                    c = "mg2" if (x * 5 + y * 3) % 19 else "mg1"
                B.px(ox + x, oy + y, c)

    def dado(ox, oy, labrys=False):
        for y in range(16):
            for x in range(16):
                if y < 2:
                    c = "mb" if y == 0 else "mg0"
                elif y < 13:
                    xx = x % 8
                    if xx == 7:
                        c = "mg0"
                    else:
                        # veined alabaster: soft wavy veins
                        v = math.sin((x * 0.9 + y * 0.5) + (x // 8) * 2.0) + math.sin(y * 1.3 + x * 0.2)
                        c = "mg1" if v > 0.9 else "mg2"
                        if v > 1.6:
                            c = "mg0"
                else:
                    c = ("mt0", "mt1", "ink")[y - 13]
                B.px(ox + x, oy + y, c)
        if labrys:
            grid(B, ox + 4, oy + 3, [
                "k.....k",
                "kk...kk",
                "kkk.kkk",
                "kkkkkkk",
                "kkk.kkk",
                "kk.k.kk",
                "k..k..k",
                "...k...",
            ], {"k": "mg0"})

    def end(ox, oy, side):
        x0 = 0 if side == "L" else 12
        for y in range(16):
            for x in range(x0, x0 + 4):
                B.px(ox + x, oy + y, "ink" if (x < 3 if side == "L" else x > 12) else "mb")
    frieze(0, 16)
    frieze(16, 16)
    frieze(32, 16)
    end(0, 16, "L")
    end(32, 16, "R")
    field(48, 16)
    field(64, 16, red=True)
    dado(80, 16)
    dado(96, 16, labrys=True)
    # the north wall's doorway: a dark opening under a red lintel
    field(16, 32)
    dado(112, 16)
    for y in range(16):
        for x in range(3, 13):
            B.px(112 + x, 16 + y, "ink" if y > 2 else ("mr1", "mr0", "mb")[y])
        B.px(112 + 2, 16 + y, "mg2")
        B.px(112 + 13, 16 + y, "mg0")
    for y in range(8, 16):
        for x in range(3, 13):
            B.px(16 + x, 32 + y, "mr1" if y < 14 else "mr0")
        B.px(16 + 2, 32 + y, "mg2")
        B.px(16 + 13, 32 + y, "mg0")
    for x in range(2, 14):
        B.px(16 + x, 32 + 7, "mb")
    field(0, 32)
    end(0, 32, "L")
    field(32, 32)
    end(32, 32, "R")
    dado(48, 32)
    end(48, 32, "L")
    dado(64, 32)
    end(64, 32, "R")
    # side walls and the south wall
    for (ox, side) in ((80, "W"), (96, "E")):
        floor_cell(B, ox, 32, "A")
        for y in range(16):
            for x in range(16):
                if (side == "W" and x < 4) or (side == "E" and x > 11):
                    B.px(ox + x, 32 + y, "ink")
                elif (side == "W" and x < 6) or (side == "E" and x > 9):
                    B.px(ox + x, 32 + y, "mb")
    for (ox, part) in ((0, "W"), (16, "M"), (32, "E")):
        for y in range(16):
            for x in range(16):
                c = "ink" if y > 9 else ("mb" if y > 6 else None)
                if c is None:
                    continue
                B.px(ox + x, 48 + y, c)
        floor_cell(B, ox, 48, "A") if False else None
        for y in range(7):
            for x in range(16):
                B.px(ox + x, 48 + y, P.slab_px(x, y, P.LAYOUTS["A"]))
        if part == "W":
            for y in range(16):
                for x in range(4):
                    B.px(ox + x, 48 + y, "ink")
        if part == "E":
            for y in range(16):
                for x in range(12, 16):
                    B.px(ox + x, 48 + y, "ink")
    # the exit: the south wall's doorway, a gypsum threshold, light beyond
    for y in range(16):
        for x in range(16):
            if y < 7:
                c = P.slab_px(x, y, P.LAYOUTS["D"])
            elif 3 <= x <= 12:
                c = "mg2" if y < 9 else ("mg1" if y < 13 else "mg0")
            else:
                c = "ink" if y > 9 else "mb"
            B.px(112 + x, 32 + y, c)
    # the vault: lilies on white and on red, the corbelled roof, a niche, a lamp
    for (ox, red) in ((48, False), (64, True)):
        field(ox, 48, red=red)
        for (lx, ly) in ((1, 4), (9, 2), (5, 9), (12, 10)):
            grid(B, ox + lx, 48 + ly, [
                "w.w.w",
                ".www.",
                "..y..",
                "..g..",
                ".gg..",
            ], {"w": "mg2" if red else "mg0", "y": "mo1", "g": "mt0" if red else "mo0"})
    for y in range(16):
        for x in range(16):
            course = y // 4
            c = ("mb", "mt0", "mg0", "mg0")[y % 4] if course < 4 else "mb"
            if (x + course * 3) % 8 == 7:
                c = "mb"
            B.px(80 + x, 48 + y, c)
    field(96, 48)
    for y in range(4, 12):
        for x in range(4, 12):
            B.px(96 + x, 48 + y, "mb" if y > 4 else "mg0")
    B.px(96 + 7, 48 + 9, "mo1")
    B.px(96 + 8, 48 + 9, "mo1")
    field(112, 48)
    grid(M, 112 + 3, 48 + 4, [
        "....yy....",
        "...yYy....",
        ".kkkkkkkk.",
        "k22111110k",
        ".k111100k.",
        "..kkkkkk..",
        "....kk....",
        "...kkkk...",
    ], {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0", "y": "mo1", "Y": "mo2"})
    s.walk = ["X.......", "XXXXXXXX", "XXXXXXXX", "XXXXXXXX"]
    s.walk[1] = "XXXXXXXD"
    s.walk[2] = "XXXXXXX."
    s.behaviors = {(7, 1): "MB_NON_ANIMATED_DOOR", (7, 2): "MB_SOUTH_ARROW_WARP"}
    # fix names: (7,1) is the door, (7,2) the exit, (1,2) door_top
    return s


# --------------------------------------------------------------------------
# Frescoes for the rooms: the griffins, the dolphins
# --------------------------------------------------------------------------

GRIFFIN = [
    "...........bwb........",
    "..........bwbwb.......",
    ".........bbwbb........",
    "........bbkkkk........",
    "........kccccck.......",
    ".......kccckcckk......",
    ".......kcccccckyyk....",
    "......kccccccckyyyk...",
    "......kcccccckkkyk....",
    ".....kccrcccck..k.....",
    "....kccrrcccck........",
    "...kcccccccccck.......",
    ".kkcrccrcccrccckkkkk..",
    "kcccrcccrcccrcccrccck.",
    "kccrcccrcccrcccrcccck.",
    ".kcccccccccccccccccck.",
    "..kkyykkkkkkkkkkyykk..",
    "...kkk..........kkk...",
]


def griffin(L, ox, oy, flip=False):
    """A wingless griffin couchant, the Throne Room's guardian: an eagle's
    head and crest of plumes on a lion's body, painted with red spirals."""
    grid(L, ox, oy, GRIFFIN, {"k": "ink", "c": "fcr", "r": "fr", "b": "fb2", "w": "fw",
                              "y": "fy0"}, flip=flip)


DOLPHIN = [
    "......kk..........",
    ".....kbbk.........",
    "...kkbbbbkkkk.....",
    "..kbbbbbbbbbbbkk..",
    ".kbebbyyyyyybbbbk.",
    "kbbbyyyyyyyyyybbbk",
    ".kwwwwwwwwwwwkk.kk",
    "..kkkkkkkkkkk.....",
]


def dolphin(L, ox, oy, flip=False):
    grid(L, ox, oy, DOLPHIN, {"k": "fb0", "b": "fb1", "e": "ink", "y": "fy0", "w": "fw"},
         flip=flip)


def room_frescoes():
    names = {"griffin_TL": (0, 0), "griffin_TR": (1, 0), "griffin_BL": (0, 1),
             "griffin_BR": (1, 1), "griffin2_TL": (2, 0), "griffin2_TR": (3, 0),
             "griffin2_BL": (2, 1), "griffin2_BR": (3, 1),
             "dolphins_TL": (4, 0), "dolphins_T": (5, 0), "dolphins_TR": (6, 0),
             "dolphins_BL": (4, 1), "dolphins_B": (5, 1), "dolphins_BR": (6, 1),
             "saffron": (7, 0), "monkey": (7, 1)}
    s = struct("frescoes", "The griffins, the dolphins, the saffron gatherer, the blue monkey",
               8, 2, SEC, walk=["XXXXXXXX", "XXXXXXXX"], names=names,
               notes="Panels for the north wall's `frieze` and `field` rows (each panel is two "
                     "rows: lay it over a frieze and a field cell, the dado below). **The "
                     "griffins** (LABYRINTH §3; Griffins are décor, not forms): `griffin_*` "
                     "faces east and `griffin2_*` west; hang one either side of the throne, "
                     "couchant among lilies on a red ground. **The dolphins** (`dolphins_*`, 3 "
                     "x 2), the Queen's Megaron's fresco: dolphins and little fish over a "
                     "sea-blue band. `saffron`: a saffron gatherer, a girl picking crocuses; "
                     "`monkey`: a blue monkey among papyrus (one-cell panels for a `field` row, "
                     "the West Magazines' and the Grand Staircase's walls). All impassable; bg "
                     "events.")
    B, M = s.B, s.M
    # griffins: red ground, lilies, a wavy blue band at the foot
    for (ox, flip) in ((0, False), (32, True)):
        for y in range(32):
            for x in range(32):
                if y < 2 or y > 29 or x < 1 or x > 30:
                    c = "ink"
                elif y > 24:
                    c = "fb1" if (y + int(2 * math.sin((x + ox) / 3.0))) % 4 < 2 else "fw"
                else:
                    c = "fr"
                B.px(ox + x, y, c)
        for (lx, ly) in ((3, 5), (24, 4), (26, 15), (2, 17)):
            grid(B, ox + lx, ly, ["w.w.w", ".www.", "..y..", "..g..", ".gg.."],
                 {"w": "fw", "y": "fy1", "g": "fg1"})
        griffin(B, ox + (6 if not flip else 4), 7, flip=flip)
    # the dolphins: a pale ground, a blue wave band, dolphins and fish
    for y in range(32):
        for x in range(48):
            X = 64 + x
            if y < 2 or y > 29 or x < 1 or x > 46:
                c = "ink"
            elif y > 25:
                c = "fb1" if (y + int(2 * math.sin(x / 3.0))) % 3 else "fb2"
            elif y < 5:
                c = "fy0" if (x // 3) % 2 else "fr"
            else:
                c = "fw" if (x * 3 + y * 5) % 17 else "fb3"
            B.px(X, y, c)
    dolphin(B, 64 + 4, 7)
    dolphin(B, 64 + 26, 14, flip=True)
    dolphin(B, 64 + 9, 18)
    for (fx, fy) in ((30, 7), (36, 9), (22, 13), (40, 22), (4, 23)):
        grid(B, 64 + fx, fy, ["fff.", "fyyf", "fff."], {"f": "fq", "y": "fy1"})
    # the saffron gatherer: a girl among crocuses on an ochre ground
    for y in range(16):
        for x in range(16):
            c = "ink" if y < 1 or y > 14 or x < 1 or x > 14 else ("fy1" if y < 10 else "fg1")
            B.px(112 + x, y, c)
    grid(B, 112 + 5, 2, [
        ".kk..",
        "kssk.",
        ".ss..",
        "sbbbs",
        ".bbb.",
        ".rrr.",
        "rrrrr",
        ".r.r.",
    ], {"k": "ink", "s": "fw", "b": "fb1", "r": "fr"})
    for (cx_, cy_) in ((3, 11), (11, 10), (8, 12), (13, 12)):
        grid(B, 112 + cx_, cy_, ["f.f", ".y."], {"f": "fq", "y": "fy0"})
    # the blue monkey among papyrus
    for y in range(16):
        for x in range(16):
            c = "ink" if y < 1 or y > 14 or x < 1 or x > 14 else ("fr" if y < 11 else "fy0")
            B.px(112 + x, 16 + y, c)
    grid(B, 112 + 3, 16 + 3, [
        "...bb.....",
        "..bbbb....",
        "..bkbb.b..",
        "...bbbbb..",
        "..bbbbbbb.",
        ".bb.bbb.b.",
        ".b..b.b..b",
        "....b.b...",
    ], {"b": "fb2", "k": "ink"})
    for (px_, h_) in ((11, 8), (13, 6)):
        for y in range(16 + 14 - h_, 16 + 14):
            B.px(112 + px_, y, "fg0")
        grid(B, 112 + px_ - 1, 16 + 14 - h_ - 2, ["ggg", ".g."], {"g": "fg1"})
    return s


# --------------------------------------------------------------------------
# Furniture: the throne, benches, basin; pithoi and cists; the Titan camp;
# Ariadne's bed and bath; the Grand Staircase
# --------------------------------------------------------------------------

def furniture():
    names = {"throne_back": (0, 0), "throne": (0, 1), "bench_L": (1, 1), "bench": (2, 1),
             "bench_R": (3, 1), "bowl": (1, 0), "basin_TL": (2, 0), "basin_TR": (3, 0),
             "pithos_top": (4, 0), "pithos": (4, 1), "pithoi_top": (5, 0), "pithoi": (5, 1),
             "cist": (6, 0), "cist_open": (7, 0), "bedroll": (6, 1), "crate": (7, 1),
             "banner": (0, 2), "table_L": (1, 2), "table_R": (2, 2), "spears": (3, 2),
             "bed_top": (4, 2), "bed": (4, 3), "bath": (5, 2), "chest": (6, 2), "loom": (7, 2),
             "basin_BL": (2, 3), "basin_BR": (3, 3), "well_TL": (0, 3), "well_TR": (1, 3),
             "stand": (5, 3), "brazier": (6, 3), "wall_spears": (7, 3)}
    s = struct("furniture", "The throne, the pithoi, the Titans' camp, Ariadne's rooms", 8, 4,
               SEC, walk=["XXXXXXXX", "XXXXXXXX", "XXXXXXXX", "XXXXXXXX"], names=names,
               notes="Standing on the rooms' floor (`house.floor_A` under each). **The Throne "
                     "Room** (scene A): `throne_back` (its wavy high back, set in the dado row "
                     "against the north wall) over `throne` (the gypsum seat); `bench_L` "
                     "`bench` `bench_R`, the gypsum benches along the walls; `bowl`, the "
                     "porphyry basin before the throne; the lustral basin, `basin_TL` `basin_TR` "
                     "over `basin_BL` `basin_BR`, a sunken bath stepping down. **The West "
                     "Magazines**: `pithos_top` over `pithos`, one giant jar; `pithoi_top` over "
                     "`pithoi`, two side by side, for the long rows; `cist` (a stone-lined pit "
                     "in the floor, lidded) and `cist_open`. **The Titans' camp** among them: "
                     "`bedroll`, `crate` (a sickle burnt in its lid), `banner` (the sickle "
                     "banner, hung on a `field`), `table_L` `table_R` (a slate-draped table), "
                     "`spears` (a rack), `brazier`, `wall_spears` (hung on a `field`). **The "
                     "Queen's Megaron**: `bed_top` over `bed` (Ariadne's, a saffron coverlet bordered in red), "
                     "`bath` (a painted clay tub), `chest`, `loom`, `stand` (a lamp stand), and "
                     "a light well, `well_TL` `well_TR` (open to the sky, a red column going "
                     "down; lay it over two floor cells). All impassable.")
    B, M, Tl = s.B, s.M, s.T
    for cy in range(4):
        for cx in range(8):
            floor_cell(B, cx * 16, cy * 16, "ABCD"[(cx + cy) % 4], seed=cx)
    # the throne's back: a high gypsum slab with a wavy edge, in front of the dado
    for y in range(16):
        for x in range(16):
            c = None
            edge = 4 + 1.6 * math.sin(x / 2.2)
            if 3 <= x <= 12 and y >= edge:
                c = "mg2" if x < 6 else ("mg1" if x < 11 else "mg0")
            if c:
                B.px(x, y, c)
    # the dado behind the throne's back
    for y in range(16):
        for x in range(16):
            if B.get(x, y) not in ("mg2", "mg1", "mg0") or not (3 <= x <= 12):
                B.px(x, y, "mg2" if y > 1 else "mb") if y < 13 else B.px(x, y, ("mt0", "mt1", "ink")[y - 13])
    for y in range(16):
        x0 = 3
        while x0 <= 12 and not (y >= 4 + 1.6 * math.sin(x0 / 2.2)):
            x0 += 1
    for x in range(3, 13):
        top = int(4 + 1.6 * math.sin(x / 2.2))
        M.px(x, top, "ink")
        for y in range(top + 1, 16):
            M.px(x, y, "mg2" if x < 6 else ("mg1" if x < 11 else "mg0"))
    for y in range(4, 16):
        M.px(2, y, "ink")
        M.px(13, y, "ink")
    # the seat
    grid(M, 0, 16, [
        "..kkkkkkkkkkkk..",
        "..k2222222111k..",
        "..k2111111110k..",
        "..k2kkkkkkk10k..",
        "..k2k22221k10k..",
        "..k2k21110k10k..",
        "..k2kkkkkkk10k..",
        "..k2111111100k..",
        "..k2110000000k..",
        "..k21k....k00k..",
        "..k21k....k00k..",
        "..kkkk....kkkk..",
    ], {"k": "ink", "2": "mg2", "1": "mg1", "0": "mg0"})
    # benches
    for (cx, end) in ((1, "L"), (2, None), (3, "R")):
        ox = cx * 16
        for y in range(3, 13):
            for x in range(16):
                if end == "L" and x < 2:
                    continue
                if end == "R" and x > 13:
                    continue
                c = "mg2" if y < 6 else ("mg1" if y < 11 else "mg0")
                if y == 3:
                    c = "ink"
                if y == 12:
                    c = "ink"
                M.px(ox + x, 16 + y, c)
        if end == "L":
            for y in range(3, 13):
                M.px(ox + 2, 16 + y, "ink")
        if end == "R":
            for y in range(3, 13):
                M.px(ox + 13, 16 + y, "ink")
    # the porphyry bowl
    grid(M, 16 + 3, 4, [
        "..kkkkkk..",
        ".k221110k.",
        "kbbbbbbbbk",
        ".kbbbbbbk.",
        "..k1110k..",
        "...k10k...",
        "..kkkkkk..",
    ], {"k": "ink", "2": "mr2", "1": "mr1", "0": "mr0", "b": "mr0"})
    # the lustral basin: steps down along the west, a dark floor
    for cy in range(2):
        for cx in range(2):
            ox, oy = 32 + cx * 16, cy * 16 if cy == 0 else 48
            for y in range(16):
                for x in range(16):
                    X, Y = cx * 16 + x, cy * 16 + y
                    if X < 2 or X > 29 or Y < 2 or Y > 29:
                        c = "mg2" if (X < 2 or Y < 2) else "mg0"
                        if X == 0 or Y == 0 or X == 31 or Y == 31:
                            c = "ink"
                    elif X < 12:
                        step = (X - 2) // 3
                        c = ("mg1", "mg0", "mo0", "mt0")[min(3, step)] if (X - 2) % 3 else "mb"
                    else:
                        c = "mt0" if (X + Y) % 5 else "mb"
                    B.px(ox + x, oy + y, c)
    # pithoi
    def jar(L, ox, oy, rows_top, rows_bot):
        grid(L, ox, oy, rows_top, {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0", "r": "mr1"})
        grid(L, ox, oy + 16, rows_bot, {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0",
                                         "r": "mr1"})
    top = [
        "................",
        "......kkkk......",
        ".....k2211k.....",
        "....kk2110kk....",
        "...k22211100k...",
        "..k2222111100k..",
        "..k2k1k1k1k0k...",
        "..k2221111100k..",
        "..k21r1r1r1r0k..",
        "..k2r1r1r1r10k..",
        "..k2221111100k..",
        "..kk2kk1kk0kkk..",
        "..k2221111100k..",
        "..k2221111100k..",
        "..k2r1r1r1r10k..",
        "..k2211111100k..",
    ]
    bot = [
        "..k2211111000k..",
        "..k2111111000k..",
        "...k21111100k...",
        "...kk2kk1k0kk...",
        "....k2111100k...",
        "....k2111100k...",
        ".....k21100k....",
        ".....kkkkkkk....",
    ]
    jar(M, 64, 0, top, bot)
    small_top = [
        "................",
        "................",
        "..kkkk....kkkk..",
        ".k2110k..k2110k.",
        "..k10k....k10k..",
        ".kk21kk..kk21kk.",
        "k222110kk222110k",
        "k2k1k0kkk2k1k0kk",
        "k221110kk221110k",
        "k2r1r10kk2r1r10k",
        "k2211r0kk2211r0k",
        "k2r1r10kk2r1r10k",
        "k221100kk221100k",
        "kk2k1kkkkk2k1kkk",
        "k221100kk221100k",
        "k221100kk221100k",
    ]
    small_bot = [
        ".k2110k..k2110k.",
        ".k2110k..k2110k.",
        "..k10k....k10k..",
        "..kkkk....kkkk..",
    ]
    jar(M, 80, 0, small_top, small_bot)
    # cists: lidded and open
    for (ox, open_) in ((96, False), (112, True)):
        for y in range(3, 13):
            for x in range(2, 14):
                if x in (2, 13) or y in (3, 12):
                    c = "mb"
                elif open_:
                    c = "ink" if y > 5 else "mb"
                else:
                    c = "mg2" if y < 6 else "mg1"
                    if x == 7 and 5 < y < 10:
                        c = "mg0"
                M.px(ox + x, y, c)
    # the Titans' camp: bedroll, crate, banner, table, spears, brazier
    grid(M, 96 + 1, 16 + 4, [
        ".kkkkkkkkkkkk.",
        "k1111111111a1k",
        "k1222222222a1k",
        "k1111111111a1k",
        "k0000000000a0k",
        ".kkkkkkkkkkkk.",
    ], {"k": "ink", "1": "ts1", "2": "ts2", "0": "ts0", "a": "wd1"})
    grid(M, 112 + 2, 16 + 2, [
        "kkkkkkkkkkkk",
        "k3333333332k",
        "k3k2222222kk",
        "kkkkkkkkkkkk",
        "k2222222221k",
        "k22g2222221k",
        "k2g222g2221k",
        "k2g22g22221k",
        "k22gg222221k",
        "k1111111110k",
        "kkkkkkkkkkkk",
    ], {"k": "ink", "3": "wd3", "2": "wd2", "1": "wd1", "0": "wd0", "g": "tgd"})
    # banner: hung from a rod on the wall; drawn on a plaster field
    for y in range(16):
        for x in range(16):
            B.px(x, 32 + y, "mg2" if (x * 5 + y * 3) % 19 else "mg1")
    grid(M, 2, 32 + 1, [
        "kkkkkkkkkkkk",
        ".k11111111k.",
        ".k11gg1111k.",
        ".k1g11g111k.",
        ".k1g1111g1k.",
        ".k11g1111gk.",
        ".k111gggg1k.",
        ".k1111g111k.",
        ".k11111g11k.",
        ".k1111111gk.",
        ".k0000000.k.",
        ".k0k0k0k0kk.",
        ".kk.k.k.k.k.",
    ], {"k": "ink", "1": "ts1", "0": "ts0", "g": "tgd"})
    # table: slate cloth over trestles, a lamp and a tablet on it
    for (cx, side) in ((1, "L"), (2, "R")):
        ox = cx * 16
        for y in range(3, 14):
            for x in range(16):
                if side == "L" and x < 2:
                    continue
                if side == "R" and x > 13:
                    continue
                if y < 10:
                    c = "ts1" if y > 3 else "ink"
                    if y == 9:
                        c = "ts0"
                else:
                    c = None
                    if x in (4, 11):
                        c = "wd1"
                if c:
                    M.px(ox + x, 32 + y, c)
    grid(M, 16 + 9, 32 + 4, ["kk", "gg"], {"k": "wd0", "g": "tgd"})
    grid(M, 32 + 3, 32 + 4, ["kkkk", "k22k", "kkkk"], {"k": "wd0", "2": "wd3"})
    # spears in a rack
    for i, x in enumerate((4, 7, 10)):
        for y in range(1, 14):
            M.px(48 + x, 32 + y, "wd2" if y > 3 else "bz2")
        M.px(48 + x - 1, 32 + 2, "bz1")
        M.px(48 + x + 1, 32 + 2, "bz1")
    for x in range(2, 14):
        M.px(48 + x, 32 + 9, "wd0")
        M.px(48 + x, 32 + 13, "wd0")
    # Ariadne's bed: gypsum frame, a blue coverlet with a red border, a pillow
    grid(M, 64 + 1, 32 + 2, [
        ".kkkkkkkkkkkk.",
        "k222222222221k",
        "k2wwwwwwwwww1k",
        "k2wwwwwwwwww1k",
        "k2rrrrrrrrrr1k",
        "k2bbbbbbbbbb1k",
        "k2bBbbbbbBbb1k",
        "k2bbbbbbbbbb1k",
        "k2bbbbBbbbbb1k",
        "k2bbbbbbbbbb1k",
        "k2bbbBbbbbbb1k",
        "k2bbbbbbbbbb1k",
        "k2bbbbbbbbBb1k",
        "k2bbbbbbbbbb1k",
    ], {"k": "ink", "2": "mg2", "1": "mg0", "w": "mg2", "r": "mr1", "b": "mo1", "B": "mo2"})
    grid(M, 64 + 1, 48, [
        "k2bbbbbbbbbb1k",
        "k2bbbbbbbbbb1k",
        "k2rrrrrrrrrr1k",
        "k222222222221k",
        "k211111111100k",
        "k2k.......k0k.",
        "kkk.......kkk.",
    ], {"k": "ink", "2": "mg2", "1": "mg1", "0": "mg0", "b": "mo1", "r": "mr1"})
    # the bath: a clay larnax painted with reeds
    grid(M, 80 + 1, 32 + 3, [
        ".kkkkkkkkkkkk.",
        "k222222222221k",
        "k2mmmmmmmmmm1k",
        "k21111111111kk",
        "k21r1r1r1r110k",
        "k2r1r1r1r1r10k",
        "k21111111111kk",
        ".k1111111100k.",
        "..kkkkkkkkkk..",
    ], {"k": "mt0", "2": "mt2", "1": "mt1", "0": "mt0", "m": "mb", "r": "mr1"})
    # a chest, a loom, a lamp stand, a brazier, spears on a wall
    grid(M, 96 + 2, 32 + 3, [
        "kkkkkkkkkkkk",
        "k2222222221k",
        "kkkkkkkkkkkk",
        "k2111111110k",
        "k21r1rr1r10k",
        "k2111111110k",
        "k2111111110k",
        "kkkkkkkkkkkk",
    ], {"k": "wd0", "2": "wd3", "1": "wd2", "0": "wd1", "r": "bz2"})
    for y in range(1, 15):
        for x in (2, 13):
            M.px(112 + x, 32 + y, "wd1")
    for x in range(2, 14):
        M.px(112 + x, 32 + 2, "wd0")
    for x in range(3, 13):
        for y in range(3, 11):
            M.px(112 + x, 32 + y, "tc3" if x % 2 else "wd3")
    for x in range(3, 13):
        M.px(112 + x, 32 + 12, "wd2")
        for (wx, wy) in ((4, 13), (7, 13), (10, 13)):
            M.px(112 + wx, 32 + wy, "tc0")
    # the light well over two floor cells: a parapet, a dark shaft, a column
    for y in range(16):
        for x in range(32):
            X = x
            if x < 2 or x > 29 or y < 2:
                c = "mg2" if (x < 2 or y < 2) else "mg0"
                if x == 0 or x == 31 or y == 0:
                    c = "ink"
                B.px(X, 48 + y, c)
            else:
                B.px(X, 48 + y, "ink" if y > 5 else "mb")
    for y in range(4, 16):
        for x in range(19, 25):
            B.px(x, 48 + y, "mr1" if x < 23 else "mr0")
        B.px(18, 48 + y, "ink")
        B.px(25, 48 + y, "ink")
    # the lamp stand
    for y in range(4, 14):
        M.px(80 + 7, 48 + y, "bz1")
        M.px(80 + 8, 48 + y, "bz0")
    grid(M, 80 + 4, 48 + 1, ["..y..", ".yYy.", "kkkkk"], {"y": "bz3", "Y": "w0", "k": "bz0"})
    grid(M, 80 + 4, 48 + 13, ["kkkkk", ".k.k."], {"k": "bz0"})
    # the brazier: an iron bowl on legs, embers
    grid(M, 96 + 2, 48 + 4, [
        "..rryrrr..",
        ".kkkkkkkk.",
        "k22222222k",
        ".k111111k.",
        "..kkkkkk..",
        "..k....k..",
        ".k......k.",
    ], {"k": "ink", "2": "ts2", "1": "ts1", "r": "bz2", "y": "tgd"})
    # spears on a wall (a field cell with spears crossed)
    for y in range(16):
        for x in range(16):
            B.px(112 + x, 48 + y, "mg2" if (x * 5 + y * 3) % 19 else "mg1")
    M.line(112 + 2, 48 + 14, 112 + 13, 48 + 2, "wd1")
    M.line(112 + 13, 48 + 14, 112 + 2, 48 + 2, "wd1")
    grid(M, 112 + 11, 48 + 1, ["bb.", "bbb"], {"b": "bz2"})
    grid(M, 112 + 2, 48 + 1, [".bb", "bbb"], {"b": "bz2"})
    return s


def staircase():
    names = {"head_L": (0, 0), "head": (1, 0), "head_R": (2, 0), "flight_L": (0, 1),
             "flight": (1, 1), "flight_R": (2, 1), "deep_L": (0, 2), "deep": (1, 2),
             "deep_R": (2, 2), "balustrade": (3, 0), "balustrade_col": (3, 1),
             "balustrade_end": (3, 2), "dark": (4, 2), "landing": (4, 1), "top_col": (4, 0)}
    s = struct("staircase", "The Grand Staircase", 5, 3, SEC,
               walk=[".....", "...X.", "...XD"], names=names,
               notes="The Grand Staircase (LABYRINTH §3, scene B): flights of broad gypsum "
                     "treads going down to the north, darker as they go, beside a balustrade "
                     "of red columns that taper downward, open to a light well. A flight is "
                     "`head_*` (its top treads, lit) over `flight_*` over `deep_*` (deep in "
                     "shadow); `_L` and `_R` are its sides. All walkable: going north is going "
                     "down. `balustrade` (its parapet), `balustrade_col` (a short column on it), "
                     "`balustrade_end` run down the flight's side (impassable). `top_col` is a "
                     "column's capital rising beside the head, drawn over the player. "
                     "`landing` is a half-landing's floor. `dark` is the foot of the last flight, "
                     "where it turns into the dark toward Ring I: `MB_NON_ANIMATED_DOOR`, the "
                     "warp down to `MAP_LABYRINTH_RING1`.")
    B, M, Tl = s.B, s.M, s.T
    ramp = [("mg2", "mg1", "mg0", "mo0"), ("mg1", "mg0", "mo0", "mt0"), ("mg0", "mo0", "mt0", "mb")]
    for row in range(3):
        for cx, side in ((0, "L"), (1, None), (2, "R")):
            ox, oy = cx * 16, row * 16
            r = ramp[row]
            for y in range(16):
                for x in range(16):
                    k = y % 4
                    c = r[k] if k < 3 else ("mb" if row < 2 else "ink")
                    B.px(ox + x, oy + y, c)
            if side == "L":
                for y in range(16):
                    B.px(ox + 0, oy + y, "ink")
                    B.px(ox + 1, oy + y, "mb")
            if side == "R":
                for y in range(16):
                    B.px(ox + 15, oy + y, "ink")
                    B.px(ox + 14, oy + y, "mb")
    # balustrade: a gypsum parapet, a short red column on it, running down
    for row in range(3):
        ox, oy = 48, row * 16
        for y in range(16):
            for x in range(16):
                B.px(ox + x, oy + y, ("mg1", "mg0", "mo0")[row] if (y % 4) else "mb")
        for y in range(16):
            for x in range(5, 11):
                M.px(ox + x, oy + y, "mg2" if x == 5 else ("mg0" if x == 10 else "mg1"))
    for y in range(0, 14):
        t = y / 14.0
        half = 3.4 - 1.0 * t
        for x in range(16):
            d = x + 0.5 - 8
            if abs(d) <= half:
                M.px(48 + x, 16 + y, "mr2" if d < -half + 1.5 else ("mr0" if d > half - 1.2 else "mr1"))
            elif abs(d) <= half + 1:
                M.px(48 + x, 16 + y, "ink")
    grid(M, 48 + 3, 16, ["kkkkkkkkkk", ".kbbbbbbk."], {"k": "ink", "b": "mb"})
    # landing, dark foot, a column's top
    for y in range(16):
        for x in range(16):
            B.px(64 + x, 16 + y, P.slab_px(x, y, P.LAYOUTS["D"]))
            c = B.get(64 + x, 16 + y)
            B.px(64 + x, 16 + y, {"mg2": "mg1", "mg1": "mg0", "mt2": "mt1"}.get(c, c))
            B.px(64 + x, 32 + y, "ink" if y > 3 else "mb")
    for x in range(16):
        B.px(64 + x, 32 + 0, "mo0")
    for y in range(16):
        for x in range(16):
            B.px(64 + x, y, ("mg1", "mg0", "mg0", "mb")[y % 4])
    P.column(Tl, M, 64, -16 + 16) if False else None
    grid(Tl, 64 + 1, 6, [
        "kkkkkkkkkkkkkk",
        "k666666666655k",
        "kkkkkkkkkkkkkk",
        ".kbbbbbbbbbbk.",
        "kbBbbbbbbbbbbk",
        "kbBbbbbbbbbbbk",
        ".kbbbbbbbbbbk.",
        "..kkkkkkkkkk..",
        "..k23333332k..",
        "..kkkkkkkkkk..",
    ], {"k": "ink", "6": "mg2", "5": "mg1", "b": "mb", "B": "mg0", "2": "mo1", "3": "mo0"})
    s.walk = [".....", "...X.", "...XD"]
    s.behaviors = {(4, 2): "MB_NON_ANIMATED_DOOR"}
    return s


def build():
    return [house(), room_frescoes(), furniture(), staircase()]
