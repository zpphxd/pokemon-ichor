"""gTileset_SteppeTown: the Greek colonies on the steppe's coast.

LABORS's Abdera (Labor 8: a small Thracian port town, a colony of Teos) and,
for the Oikoumene, Olbia on the Borysthenes and any other colony town there.
Greek houses built from what the north coast has: mud-brick and weathered
timber under terracotta or reed thatch; an Asclepeion and an Agora in the same
materials; a timber quay at the river mouth with a gangplank; a horse market;
a small temple of Apollo, the colonists' god.

  ground   the steppe's dirt road and its joins onto aethos's path
  houses   a house kit (two roofs, two walls) and the fronts built from it
  civic    the Asclepeion and the Agora, the temple of Apollo
  harbor   the timber quay, its gangplank, a fishing boat
  market   stalls, a cart, the horse-market pen
"""
from __future__ import annotations

import math

import numpy as np

import farlands_lib as F
import farlands_houses as Hs
import farlands_steppe as St
from farlands_lib import ground, put, struct

GROUPS = {
    "earth": St.GROUPS["earth"],
    # roofs: terracotta pantiles and reed thatch
    "roof": ["tc0", "tc1", "tc2", "sg0", "sg1", "sg2", "sg3", "tb0", "tb1", "ink", "gd", "g1",
             "w1", "w0", "bz3"],
    # walls: mud-brick, timber, whitewash; fences
    "wall": ["mb1", "mb2", "mb3", "tb0", "tb1", "tb2", "tb3", "tb4", "w0", "w1", "ink", "gd",
             "k1", "fb", "g1"],
    # the quay and the boat
    "quay": ["b2", "b3", "b4", "w0", "tb0", "tb1", "tb2", "tb3", "tb4", "sn1", "sn2", "sn3", "ink",
             "sg3", "fr2"],
    # stalls and goods
    "market": ["fr1", "fr2", "fr3", "fc1", "fc2", "tc1", "tc2", "tb1", "tb2", "tb3", "sn2", "sn3",
               "ink", "gd", "sg2"],
    # limestone and bronze: the temple of Apollo, signs
    "temple": ["w0", "w1", "k2", "k3", "p1", "p2", "p3", "bz1", "bz2", "bz3", "ink", "tc1", "b1",
               "gd", "g1"],
}

SEC_G, SEC_H, SEC_C, SEC_Q, SEC_M = "ground", "houses", "civic", "harbor", "market"

FRONTS = {
    # name: rows of piece names (from `house`), and what it is
    "brick_house": (["tile_A_L", "tile_A_M", "tile_A_R"], ["tile_B_L", "tile_B_M", "tile_B_R"],
                    ["brick_L", "brick_door", "brick_R"]),
    "timber_house": (["thatch_A_L", "thatch_A_M", "thatch_A_R"],
                     ["thatch_B_L", "thatch_B_M", "thatch_B_R"],
                     ["timber_L", "timber_door", "timber_R"]),
    "long_house": (["tile_A_L", "tile_A_M", "tile_A_M", "tile_A_R"],
                   ["tile_B_L", "tile_B_M", "tile_B_M", "tile_B_R"],
                   ["timber_L", "timber_window", "timber_door", "timber_R"]),
    "wide_house": (["tile_A_L", "tile_A_M", "tile_A_M", "tile_A_M", "tile_A_R"],
                   ["tile_B_L", "tile_B_M", "tile_B_M", "tile_B_M", "tile_B_R"],
                   ["brick_L", "brick_window", "brick_door", "brick_shutter", "brick_R"]),
    "cottage": (["thatch_A_L", "thatch_A_M", "thatch_A_M", "thatch_A_R"],
                ["thatch_B_L", "thatch_B_M", "thatch_B_M", "thatch_B_R"],
                ["brick_L", "brick_shutter", "brick_door", "brick_R"]),
}


def house():
    cols = ["L", "M", "R"]
    names = {}
    # roofs: rows 0-1 tile, 2-3 thatch
    for r, style in ((0, "tile"), (2, "thatch")):
        for i, c in enumerate(cols):
            names[f"{style}_A_{c}"] = (i, r)
            names[f"{style}_B_{c}"] = (i, r + 1)
    # walls: row 4 brick, row 5 timber
    kinds = ["L", "M", "R", "door", "window", "shutter"]
    for r, style in ((4, "brick"), (5, "timber")):
        for i, k in enumerate(kinds):
            names[f"{style}_{k}"] = (i, r)
    w = 6
    walk = ["TTTTTT", "XXXXXX", "TTTTTT", "XXXXXX", "XXXDXX", "XXXDXX"]
    s = struct("house", "The colony house kit", w, 6, SEC_H, walk=walk, names=names, oik=True,
               notes="Greek houses built from the north coast's materials, as a kit: a front is "
                     "three rows, the roof's upper half (`*_A_*`, drawn over the player), its lower "
                     "half (`*_B_*`, ending in the eave) and the wall. Roofs: `tile` (terracotta "
                     "pantiles, the colonists' pride) or `thatch` (reed, as the Thracians roof). "
                     "Walls: `brick` (plastered mud-brick) or `timber` (weathered planks), each with "
                     "`L` `M` `R`, a `door` (`MB_NON_ANIMATED_DOOR`), a `window` and a shuttered "
                     "`shutter`. Repeat `_M` for a longer house. Ready-made fronts are listed below "
                     "(`fronts`), five of them, for Abdera and for the Oikoumene's Olbia. On "
                     "borrowed grass: put a path or the road in front of the door.")
    ground(s, "grass")
    M, T = s.M, s.T
    for r, px, edge, eave, dark in ((0, Hs.tile_roof_px, "tc0", "tc2", "tc0"),
                                    (2, Hs.thatch_px, "sg0", "sg3", "sg0")):
        tmp = F.Layer(w * 16, s.h * 16)
        Hs.roof_cells(tmp, 0, r * 16, px, edge, eave, dark)
        Hs.mirror_cell(tmp, (0, r * 16), (32, r * 16))
        Hs.mirror_cell(tmp, (0, r * 16 + 16), (32, r * 16 + 16))
        for y in range(r * 16, r * 16 + 32):
            for x in range(48):
                c = tmp.get(x, y)
                if c:
                    (T if y < r * 16 + 16 else M).px(x, y, c)
    for r, px, base in ((4, Hs.brick_px, ("mb1", "tb1")), (5, Hs.timber_wall_px, ("tb1", "tb0"))):
        Hs.wall_cells(M, 0, r * 16, px, base, "tb0", ["L", "M", "L", "door", "window", "shutter"])
        Hs.mirror_cell(M, (0, r * 16), (32, r * 16))
    # spare cells in the roof rows: repeat M
    for r in (0, 1, 2, 3):
        for cx in (3, 4, 5):
            (T if r in (0, 2) else M).a[r * 16:r * 16 + 16, cx * 16:cx * 16 + 16] = \
                (T if r in (0, 2) else M).a[r * 16:r * 16 + 16, 16:32]
    s.fronts = FRONTS
    return s


def civic():
    names = {"ascl_ped": (0, 0), "ascl_door": (1, 0), "ascl_col": (2, 0), "agora_ped": (3, 0),
             "agora_door": (4, 0), "agora_awning": (5, 0)}
    s = struct("civic", "Asclepeion and Agora pieces", 6, 1, SEC_C, walk=["TDXTDX"], names=names,
               oik=True,
               notes="The colony's Asclepeion and Agora, built from the house kit plus these. "
                     "Asclepeion (5 wide): roof `tile_A_L tile_A_M ascl_ped tile_A_M tile_A_R` (the "
                     "pediment carries the bronze rod of Asclepius), `tile_B_*` below, wall "
                     "`brick_L ascl_col ascl_door ascl_col brick_R` (whitewashed porch posts, the "
                     "door with its snake plaque). Agora (5 wide): roof `thatch_A_L thatch_A_M "
                     "agora_ped thatch_A_M thatch_A_R` (a painted pinax of an amphora), `thatch_B_*`, "
                     "wall `timber_L agora_awning agora_door agora_awning timber_R` (a striped awning "
                     "over goods). Doors are `MB_NON_ANIMATED_DOOR`; the pediments are drawn over the "
                     "player.")
    ground(s, "grass")
    M, T = s.M, s.T
    # pediments: a whitewashed gable with a plaque, over a roof cell's upper half
    for i, sign in ((0, "rod"), (3, "amphora")):
        for y in range(16):
            for x in range(16):
                c = Hs.tile_roof_px(i * 16 + x, y, top=3) if sign == "rod" else Hs.thatch_px(i * 16 + x, y, top=3)
                if y < 3:
                    continue
                T.px(i * 16 + x, y, c)
        put(T, i * 16 + 2, 3, [
            "......kk......",
            ".....kwwk.....",
            "....kwwwwk....",
            "...kwwwwwwk...",
            "..kwwwwwwwwk..",
            ".kwwwwwwwwwwk.",
            "kkkkkkkkkkkkkk",
        ], {"k": "ink", "w": "w0"})
        if sign == "rod":
            for y in range(5, 10):
                T.px(i * 16 + 8, y, "tb1")
            for (x, y) in ((7, 6), (9, 7), (7, 8), (9, 9)):
                T.px(i * 16 + x, y, "bz3")
        else:
            put(T, i * 16 + 6, 5, [".tt.", "tbbt", ".tt."], {"t": "tc1", "b": "tb0"})
    # Asclepeion door, porch post
    for y in range(16):
        for x in range(16):
            M.px(16 + x, y, "w0" if (x + y) % 7 else "w1")
            M.px(32 + x, y, "w1" if x > 11 else "w0")
    for y in range(2, 16):
        for x in range(3, 13):
            c = "k2" if x in (3, 12) or y == 2 else ("bz1" if x < 8 else "bz0" if False else "k3")
            M.px(16 + x, y, c)
    for (x, y) in ((7, 6), (8, 7), (7, 8), (8, 9)):
        M.px(16 + x, y, "bz3")
    for y in range(16):
        for x in range(5, 11):
            M.px(32 + x, y, "p2" if x < 8 else "p1")
        M.px(32 + 4, y, "ink")
        M.px(32 + 11, y, "ink")
    for x in range(16):
        M.px(16 + x, 15, "k2")
        M.px(32 + x, 15, "k2")
    # Agora door and awning (market colors)
    for y in range(16):
        for x in range(16):
            M.px(64 + x, y, Hs.timber_wall_px(64 + x, y) and ("tb3" if (x + y) % 5 else "tb2"))
    for y in range(2, 16):
        for x in range(3, 13):
            c = "tb2" if x < 8 else "tb1"
            if y == 2 or x in (3, 12):
                c = "ink"
            M.px(64 + x, y, c)
    for y in range(16):
        for x in range(16):
            if y < 6:
                c = "fr2" if (x // 3) % 2 else "fc2"
                if y == 5:
                    c = "fr1" if (x // 3) % 2 else "fc1"
            else:
                c = "tb2" if y > 12 else ("tc2" if (x % 5) < 2 and y > 8 else ("fc1" if x % 5 == 3 else "tb3"))
                if y == 6:
                    c = "ink"
            M.px(80 + x, y, c)
    return s


def temple():
    names = {f"c{x}{y}": (x, y) for y in range(3) for x in range(4)}
    names["door_L"] = (1, 2)
    names["door_R"] = (2, 2)
    s = struct("temple", "A small temple of Apollo", 4, 3, SEC_C, walk=["TTTT", "XXXX", "XDDX"],
               names=names, oik=True,
               notes="The colonists' temple of Apollo the Healer, 4 x 3 on borrowed grass: a "
                     "limestone porch of four Ionic columns on three steps, a pediment with the "
                     "sun's bronze disc and a painted cornice, the doorway between the middle "
                     "columns (`door_L` and `door_R`, a two-cell doorway, `MB_NON_ANIMATED_DOOR`). "
                     "Its top row is drawn over the player. For Olbia (the Oikoumene's) and any "
                     "colony that has room for it.")
    ground(s, "grass")
    M, T = s.M, s.T
    W = 64
    # pediment
    for y in range(2, 18):
        for x in range(W):
            half = (y - 2) * 2.0
            if abs(x - 31.5) <= half + 1 and y < 14:
                c = "w0" if x < 32 else "w1"
                if abs(x - 31.5) >= half - 0.5:
                    c = "ink"
                (T if y < 16 else M).px(x, y, c)
            elif 14 <= y < 18:
                c = "tc1" if y == 15 else ("b1" if y == 16 and x % 4 < 2 else "w1")
                if y == 14:
                    c = "ink"
                if y == 17:
                    c = "k3"
                (T if y < 16 else M).px(x, y, c)
    for y in range(6, 12):
        for x in range(27, 37):
            if math.hypot(x - 31.5, y - 9) < 3.2:
                T.px(x, y, "bz3" if (x + y) % 3 else "bz2")
    # columns and cella wall
    for y in range(18, 42):
        for x in range(2, 62):
            M.px(x, y, "k2" if (x + y) % 9 else "k3")
    for cx in (6, 22, 41, 57):
        for y in range(18, 42):
            for x in range(cx - 3, cx + 3):
                c = "w0" if x < cx - 1 else ("w1" if x < cx + 1 else "k3")
                if (x - cx) % 2 == 0 and 21 < y < 40:
                    c = "w1" if x < cx else "k3"
                M.px(x, y, c)
        put(M, cx - 5, 18, ["kwwwwwwwwk", ".kw1111wk.", "..kwwwwk.."], {"k": "ink", "w": "w0", "1": "w1"})
    # doorway
    for y in range(28, 42):
        for x in range(27, 37):
            M.px(x, y, "ink" if y > 29 else "bz1")
    # steps
    for y in range(42, 48):
        for x in range(W):
            c = "p3" if y % 2 == 0 else ("p2" if x < 40 else "p1")
            if y == 47:
                c = "k2"
            M.px(x, y, c)
    return s


def quay():
    names = {"deck": (0, 0), "edge_S": (1, 0), "edge_E": (2, 0), "edge_W": (3, 0),
             "corner_SE": (4, 0), "corner_SW": (5, 0), "gangplank": (6, 0), "post": (7, 0),
             "boat_L": (0, 1), "boat_R": (1, 1), "nets": (2, 1)}
    s = struct("quay", "The river-mouth quay", 8, 2, SEC_Q,
               walk=["......XX", "XXX....."], names=names, oik=True,
               notes="A timber quay on piles where the river meets the sea. `deck`: plain planking "
                     "(walkable, drawn whole). Its edges over borrowed sea, walkable: `edge_S` (the "
                     "deck's south edge, the water below), `edge_E` `edge_W`, `corner_SE` "
                     "`corner_SW`. `gangplank`: the edge with a plank run out over the water to the "
                     "ship (put `EventScript_IchorBoardShip` here, and the voyage row in "
                     "`ichor_voyages.h`). `post`: a mooring post on the deck (impassable). "
                     "`boat_L` `boat_R`: a Thracian fishing boat drawn up on borrowed sea; `nets`: "
                     "nets drying on a rack (on the deck, impassable). For Abdera's harbor and "
                     "Olbia's (the Oikoumene's).")
    ground(s, "sea", [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (0, 1), (1, 1)])
    M, B = s.M, s.B

    def planks(L, ox, oy, x0=0, x1=16, y0=0, y1=16):
        for y in range(y0, y1):
            for x in range(x0, x1):
                k = F.hp(ox + x, oy + y, 3)
                b = (y % 5)
                c = "tb3" if b in (1, 2) else ("tb4" if b == 0 else "tb2")
                if (x + (y // 5) * 7) % 16 == 0:
                    c = "tb1"
                if k % 13 == 0:
                    c = "tb2"
                L.px(ox + x, oy + y, c)
    planks(B, 0, 0)
    for i, side in ((1, "S"), (2, "E"), (3, "W"), (4, "SE"), (5, "SW"), (6, "S")):
        ox = i * 16
        x0 = 0 if side in ("S", "W", "SW") else 0
        x1 = 16
        y1 = 11 if "S" in side else 16
        if side in ("E", "SE"):
            x1 = 11
        if side in ("W", "SW"):
            x0 = 5
        planks(M, ox, 0, x0, x1, 0, y1)
        if "S" in side:
            for x in range(x0, x1):
                M.px(ox + x, 11, "tb0")
                M.px(ox + x, 12, "tb1" if x % 6 > 1 else "tb0")
                if x % 6 in (0, 1):
                    M.px(ox + x, 13, "tb0")
                    M.px(ox + x, 14, "b2")
                elif x % 2:
                    M.px(ox + x, 14, "w0")
        if side in ("E", "SE"):
            for y in range(0, y1 + 2):
                M.px(ox + 11, y, "tb0")
                M.px(ox + 12, y, "b2" if y % 6 else "tb0")
        if side in ("W", "SW"):
            for y in range(0, y1 + 2):
                M.px(ox + 4, y, "tb0")
                M.px(ox + 3, y, "b2" if y % 6 else "tb0")
    # gangplank over the edge
    for y in range(8, 16):
        for x in range(5, 11):
            c = "tb4" if x < 8 else "tb3"
            if x in (5, 10):
                c = "tb1"
            if y % 3 == 0:
                c = "tb2"
            M.px(96 + x, y, c)
    # mooring post on the deck
    planks(M, 112, 0)
    put(M, 112 + 5, 2, ["..kk..", ".k44k.", ".k33k.", ".k32k.", "rrrrrr", ".k32k.", ".k32k.",
                        ".k32k.", ".k32k.", ".k22k.", "kkkkkk"],
        {"k": "tb0", "4": "tb4", "3": "tb3", "2": "tb2", "r": "sg3"})
    # boat: a plank-built fishing boat, 2 cells
    for y in range(16):
        for x in range(32):
            d = abs(y - 8) / 7.0
            if (x - 1) > d * 6 and (30 - x) > d * 5 and 1 < y < 15:
                c = "tb2" if y < 8 else "tb1"
                if y in (2, 3):
                    c = "tb3"
                if 4 < y < 12 and 5 < x < 27:
                    c = "tb0" if y < 6 else ("tb2" if (x // 4) % 2 else "tb3")
                M.px(x, 16 + y, c)
    for x in range(2, 30):
        if M.get(x, 16 + 15) is None:
            M.px(x, 16 + 15, "b4" if x % 3 else "w0")
    for y in range(18, 26):
        M.px(14, y, "tb0")
    # nets drying on a rack, on the deck
    planks(B, 32, 16)
    for y in range(3, 14):
        for x in range(1, 15):
            if (x + y) % 3 == 0 or (x - y) % 3 == 0:
                M.px(32 + x, 16 + y, "sn2" if y > 4 else "tb1")
        M.px(32 + 1, 16 + y, "tb0")
        M.px(32 + 14, 16 + y, "tb0")
    for x in range(1, 15):
        M.px(32 + x, 16 + 3, "tb0")
    # spare cells: deck
    for cx in range(3, 8):
        B.a[16:32, cx * 16:cx * 16 + 16] = B.a[0:16, 0:16]
    s.names = {k: v for k, v in names.items()}
    F.set_walk(s, ["......XX", "XXX....."])
    return s


def market():
    names = {"stall_TL": (0, 0), "stall_TR": (1, 0), "stall_BL": (0, 1), "stall_BR": (1, 1),
             "fur_TL": (2, 0), "fur_TR": (3, 0), "fur_BL": (2, 1), "fur_BR": (3, 1),
             "cart_L": (4, 1), "cart_R": (5, 1), "amphorae": (4, 0), "salt_fish": (5, 0)}
    s = struct("market", "Stalls, a cart, goods", 6, 2, SEC_M, walk=["TTTTXX", "XXXXXX"],
               names=names, oik=True,
               notes="On borrowed grass (or set them on aethos path). `stall` (2 x 2): a striped "
                     "felt awning on poles over a counter of Thracian goods; `fur` (2 x 2): a "
                     "trader's stall hung with furs from the north; their top rows are drawn over "
                     "the player, the counters impassable (put the clerk behind). `cart_L` `cart_R`: "
                     "a two-wheeled ox-cart loaded with grain sacks. `amphorae`: a stack of wine "
                     "jars; `salt_fish`: fish drying on a rack (the Pontic trade). All impassable.")
    ground(s, "grass")
    M, T = s.M, s.T
    for ox, stripe, goods in ((0, ("fr2", "fc2"), "jars"), (32, ("fr1", "fc1"), "furs")):
        for y in range(4, 16):
            for x in range(1, 31):
                c = stripe[0] if (x // 4) % 2 else stripe[1]
                if y == 15:
                    c = "fr1" if (x // 4) % 2 else "fc1"
                if y == 4:
                    c = "ink"
                T.px(ox + x, y, c)
        for y in range(16, 32):
            for x in (2, 3, 28, 29):
                M.px(ox + x, y, "tb2" if x % 2 == 0 else "tb1")
        for y in range(24, 31):
            for x in range(2, 30):
                c = "tb3" if y == 24 else ("tb2" if y < 30 else "ink")
                M.px(ox + x, y, c)
        if goods == "jars":
            for gx in (6, 12, 18, 24):
                put(M, ox + gx - 2, 17, [".tt.", "t22t", "t21t", ".11."], {"t": "tc2", "2": "tc1", "1": "tb1"})
        else:
            for gx in range(4, 28, 5):
                for y in range(16, 24):
                    M.px(ox + gx, y, "tb2" if y < 22 else "tb1")
                    M.px(ox + gx + 1, y, "tb3" if (y % 3) else "fc1")
                    M.px(ox + gx + 2, y, "tb2")
    # amphorae stack
    for (gx, gy) in ((4, 7), (11, 7), (7, 3)):
        put(M, 64 + gx - 3, gy, ["..tt..", ".t22t.", "t2221t", "t2211t", ".t11t.", "..tt.."],
            {"t": "ink", "2": "tc2", "1": "tc1"})
    # salt fish
    for y in range(2, 15):
        M.px(80 + 2, y, "tb1")
        M.px(80 + 13, y, "tb1")
    for x in range(2, 14):
        M.px(80 + x, 3, "tb2")
    for fx in (4, 7, 10):
        put(M, 80 + fx - 1, 4, ["s", "3", "3", "3", "2", "s"], {"s": "sn3", "3": "sn3", "2": "sn2"})
    # the cart
    for y in range(16, 32):
        for x in range(64, 96):
            if 18 <= y <= 25 and 66 <= x <= 92:
                c = "fc1" if (x // 5 + y // 4) % 2 else "fc2"
                if y == 25:
                    c = "tb1"
                M.px(x, y, c)
    for y in range(26, 28):
        for x in range(64, 96):
            M.px(x, y, "tb2" if y == 26 else "tb1")
    for cx in (72, 86):
        for y in range(24, 32):
            for x in range(cx - 4, cx + 5):
                d = math.hypot(x - cx, y - 28)
                if 3.0 < d < 4.2:
                    M.px(x, y, "tb1")
                elif d < 1.2:
                    M.px(x, y, "ink")
    for x in range(92, 96):
        M.px(x, 25, "tb1")
    return s


def pen():
    from farlands_kits import FENCE_NOTES, fence_kit
    s = fence_kit("pen", "The horse-market pen", SEC_M, ("tb0", "tb1", "tb2", "tb3"), "gd",
                  notes=FENCE_NOTES + " For the horse market (put horses in it as Pokémon "
                  "objects) and any paddock in town.", oik=True)
    return s


def build():
    out = {}
    stp = St.build()
    for k in ("road", "road_join"):
        out[k] = stp[k]
    for s in (house(), civic(), temple(), quay(), market(), pen()):
        out[s.key] = s
    return out


SPEC = {
    "symbol": "gTileset_SteppeTown", "dir": "steppe_town", "label": "SteppeTown",
    "title": "the Greek colonies of the steppe coast: Abdera and Olbia",
    "doc": "TILES_steppe_town.md",
    "limit": 496,
    "sections": [
        ("ground", ["road", "road_join"]),
        ("houses", ["house"]),
        ("civic", ["civic", "temple"]),
        ("harbor", ["quay"]),
        ("market", ["market", "pen"]),
    ],
    "rows": {"ground": 0, "houses": 10, "civic": 18, "harbor": 24, "market": 28},
    "why_split": "The steppe's land (grasses, rivers, kurgans, the heights) fills `steppe`'s 504 "
                 "tiles, so the towns built on it are their own sets: this one for the Greek "
                 "colonies, `steppe_camp` for the horse-peoples' camps. A colony that borders the open "
                 "steppe meets it across a seam strip of aethos ground (MAP_DESIGN 5). The road and its "
                 "joins are the steppe's own, redrawn here.",
}
