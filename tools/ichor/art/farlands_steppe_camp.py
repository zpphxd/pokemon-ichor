"""gTileset_SteppeCamp: the horse-peoples' camps and halls.

LABORS's Themiskyra (Labor 9: the Amazons' camp-town on the Thermodon, its
palisade and gate, Hippolyta's hall, the felt tents, the practice yard, the
cook fires, the horse field) and Diomedes's yard (Labor 8: the stable and its
fenced yard), and, for the Oikoumene, the Scythians' Wagon Camp: felt-roofed
wagon-houses, tethered horses, camp hearths, mare-milking posts.

  ground   the steppe's road, its joins, its flowers and tussocks
  walls    a palisade of stakes on a stone footing, its gate
  halls    Hippolyta's timber hall, Diomedes's stable
  tents    round felt tents, the Asclepeion tent, the Agora tent
  wagons   three felt-roofed wagon-houses
  yard     hearths, the practice ground, a well, horses, fences, troughs
"""
from __future__ import annotations

import math

import numpy as np

import farlands_lib as F
import farlands_houses as Hs
import farlands_steppe as St
from farlands_lib import anim_layer, ground, put, struct

GROUPS = {
    "earth": St.GROUPS["earth"],
    "gold": St.GROUPS["gold"],
    # timber: stakes, hall walls, wagons, stands, fences, the horse
    "timber": ["tb0", "tb1", "tb2", "tb3", "tb4", "sg1", "sg2", "sg3", "ink", "gd", "g1", "w0",
               "k2", "k3", "b3"],
    # felt: tents, wagon roofs, targets, banners
    "felt": ["fr0", "fr1", "fr2", "fr3", "fc0", "fc1", "fc2", "fb", "ink", "gd", "g1", "sg3", "tb1",
             "w0", "bz3"],
    # Thracian bronze and fire: hearths, cauldrons, shields, Ares's spear
    "bronze": ["bz0", "bz1", "bz2", "bz3", "vg1", "fi1", "fi2", "fi3", "as1", "sn1", "sn2", "ink",
               "gd", "g1", "w0"],
    # field stone: the palisade's footing, the well
    "stone": ["sn0", "sn1", "sn2", "sn3", "w1", "w0", "g1", "g2", "g3", "gd", "md1", "lc", "ink",
              "b3", "tb1"],
    # roofs: turf and thatch, painted horse-head finials
    "roof": ["g1", "g2", "gd", "t1", "sg0", "sg1", "sg2", "sg3", "tb0", "tb1", "tb2", "tb3", "ink",
             "fr2", "w0"],
}

SEC_G, SEC_W, SEC_H, SEC_T, SEC_V, SEC_Y = "ground", "walls", "halls", "tents", "wagons", "yard"


# --------------------------------------------------------------------------
# The palisade
# --------------------------------------------------------------------------

def _stakes(L, ox, oy, x0, x1, top, bottom, pointed=True):
    """A row of sharpened stakes from y top to bottom (cell-local)."""
    for x in range(x0, x1):
        k = (x - x0) % 4
        t = top + (0 if k in (1, 2) else 1) - (1 if (x // 4) % 3 == 0 else 0)
        for y in range(max(0, t), bottom):
            c = "tb3" if k == 1 else ("tb2" if k == 2 else "tb1")
            if k == 3:
                c = "tb0"
            if y == t and pointed:
                c = "tb4" if k in (1, 2) else "tb1"
            L.px(ox + x, oy + y, c)


def _footing(L, ox, oy, x0, x1, top, bottom):
    for y in range(top, bottom):
        for x in range(x0, x1):
            row = (y - top) // 4
            xx = (x + row * 3) % 7
            c = "sn2" if (y - top) % 4 else "sn3"
            if xx == 6:
                c = "sn1"
            if (y - top) % 4 == 3:
                c = "sn1"
            if F.hp(ox + x, oy + y, 3) % 11 == 0:
                c = "lc"
            L.px(ox + x, oy + y, c)
    for x in range(x0, x1):
        L.px(ox + x, oy + bottom - 1, "sn0")


def palisade():
    names = {"top_L": (0, 0), "top": (1, 0), "top_R": (2, 0), "base_L": (0, 1), "base": (1, 1),
             "base_R": (2, 1), "V": (3, 0), "V_B": (3, 1), "tower_top": (4, 0), "tower": (4, 1)}
    s = struct("palisade", "The palisade", 5, 2, SEC_W, walk=["TTTXT", "XXXXX"], names=names,
               notes="Themiskyra's wall: sharpened stakes on a footing of field stone, on borrowed "
                     "grass, impassable. A west-east run is two rows, `top` over `base` (the stakes' "
                     "points, drawn over the player, over the stakes and the stone), with `top_L` / "
                     "`base_L` and `top_R` / `base_R` ending it. A north-south run is `V` (the stakes "
                     "seen end-on), ending in `V_B` on its footing. `tower_top` over `tower`: a "
                     "square watch-post where runs meet. Diomedes's yard uses the same wall.")
    ground(s, "grass")
    M, T = s.M, s.T
    for i, (x0, x1) in ((0, (4, 16)), (1, (0, 16)), (2, (0, 12))):
        tmp = F.Layer(16, 32)
        _stakes(tmp, 0, 0, x0, x1, 6, 24)
        for y in range(32):
            for x in range(16):
                c = tmp.get(x, y)
                if c:
                    (T if y < 16 else M).px(i * 16 + x, y, c)
        _footing(M, i * 16, 16, x0, x1, 8, 16)
        if i == 0:
            for y in range(6, 32):
                (T if y < 16 else M).px(i * 16 + 4, y, "ink") if y < 24 else None
        if i == 2:
            for y in range(6, 24):
                (T if y < 16 else M).px(i * 16 + 11, y, "ink")
    # end-on run: a narrow line of stake heads
    for y in range(16):
        for x in range(5, 11):
            c = "tb3" if x == 6 else ("tb2" if x < 9 else "tb1")
            if y % 4 == 0:
                c = "tb4" if x < 8 else "tb2"
            M.px(48 + x, y, c)
        M.px(48 + 11, y, "gd")
    for y in range(0, 8):
        for x in range(5, 11):
            M.px(48 + x, 16 + y, "tb2" if x < 8 else "tb1")
    _footing(M, 48, 16, 4, 12, 8, 16)
    # tower: a square post with a railed top
    for y in range(4, 32):
        for x in range(1, 15):
            if y < 12:
                c = "tb3" if y in (4, 5) else ("tb2" if x < 8 else "tb1")
                if x in (1, 14) or y == 11:
                    c = "tb0"
            elif y < 24:
                c = "tb2" if (x % 4) else "tb1"
                if x < 4:
                    c = "tb3" if x % 4 else "tb2"
            else:
                c = None
            if c:
                (T if y < 16 else M).px(64 + x, y, c)
    _footing(M, 64, 16, 0, 16, 8, 16)
    return s


def gate():
    names = {f"c{x}{y}": (x, y) for y in range(3) for x in range(4)}
    s = struct("gate", "The gate of Themiskyra", 4, 3, SEC_W, walk=["TTTT", "XTTX", "X..X"],
               names=names,
               notes="The camp's gate, 4 x 3 on borrowed grass: two timber gate-towers hung with "
                     "pelta shields, a lintel beam carved with horses across the top, the two middle "
                     "cells of the bottom rows open (walk through them). Join `palisade` runs to its "
                     "sides at the bottom two rows. The towers' tops and the lintel are drawn over "
                     "the player.")
    ground(s, "grass")
    M, T = s.M, s.T
    for tx in (0, 48):
        for y in range(2, 48):
            for x in range(1, 15):
                if y < 10:
                    c = "tb3" if y < 4 else ("tb2" if x < 8 else "tb1")
                    if x in (1, 14) or y in (2, 9):
                        c = "tb0"
                elif y < 40:
                    c = "tb2" if (x % 4) else "tb1"
                    if x < 4:
                        c = "tb3" if x % 4 else "tb2"
                else:
                    c = None
                if c:
                    (T if y < 16 else M).px(tx + x, y, c)
        _footing(M, tx, 32, 0, 16, 8, 16)
        # a shield on each tower
        for y in range(18, 28):
            for x in range(3, 13):
                d = math.hypot((x - 7.5) / 5, (y - 22.5) / 5)
                if d < 1 and not (y < 21 and abs(x - 7.5) < 2):
                    M.px(tx + x, y, "tb4" if d > 0.75 else ("tb3" if x < 8 else "tb2"))
    # lintel
    for y in range(6, 14):
        for x in range(10, 54):
            c = "tb3" if y < 8 else ("tb2" if y < 12 else "tb0")
            if y == 6:
                c = "tb4"
            if 8 <= y < 12 and (x // 5) % 2 == 0 and x % 5 in (1, 2, 3):
                c = "tb1"
            T.px(x, y, c)
    for y in range(14, 32):
        for x in (12, 13, 50, 51):
            (T if y < 16 else M).px(x, y, "tb1" if x % 2 else "tb2")
    return s


# --------------------------------------------------------------------------
# Halls
# --------------------------------------------------------------------------

def _hall(L_T, L_M, ox, oy, w, roof_px, roof_rows, wall_rows, doors, finials=True):
    """A gabled timber hall, w cells wide: roof_rows rows of roof (the first
    drawn over the player), wall_rows rows of plank wall. doors: cell columns
    of a wide door in the bottom wall row (two cells)."""
    W = w * 16
    top = 3
    rh = roof_rows * 16
    for y in range(top, rh):
        inset = max(0, (rh - y) // 3 - 2)
        for x in range(inset, W - inset):
            c = roof_px(ox + x, oy + y, top=oy + top)
            if y == top:
                c = "tb0"
            if y >= rh - 3:
                c = "tb1" if y == rh - 3 else "tb0"
            if x == inset or x == W - inset - 1:
                c = "tb0"
            (L_T if y < 16 else L_M).px(ox + x, oy + y, c)
    if finials:
        for fx in (2, W - 9):
            put(L_T, ox + fx, oy + 0, ["..rr...", ".r22r..", "r2222r.", ".r22..."] if fx < W // 2 else
                ["...rr..", "..r22r.", ".r2222r", "...22r."], {"r": "fr2", "2": "tb2"})
    for y in range(rh, rh + wall_rows * 16):
        for x in range(W):
            c = Hs.timber_wall_px(ox + x, oy + y)
            if y >= rh + wall_rows * 16 - 2:
                c = "tb1" if y == rh + wall_rows * 16 - 2 else "tb0"
            if x < 1 or x >= W - 1:
                c = "tb0"
            L_M.px(ox + x, oy + y, c)
    # the wide door
    dy = rh + (wall_rows - 1) * 16
    for d0 in doors:
        for y in range(dy + 1, dy + 16):
            for x in range(d0 * 16 + 2, d0 * 16 + 30):
                c = "tb2" if (x - d0 * 16) < 16 else "tb1"
                if x in (d0 * 16 + 2, d0 * 16 + 29, d0 * 16 + 15, d0 * 16 + 16) or y == dy + 1:
                    c = "tb0"
                if y == dy + 7 and x % 3 == 0:
                    c = "tb4"
                L_M.px(ox + x, oy + y, c)


def hall():
    w, h_ = 6, 4
    names = {f"c{x}{y}": (x, y) for y in range(h_) for x in range(w)}
    s = struct("hall", "Hippolyta's hall", w, h_, SEC_H,
               walk=["TTTTTT", "XXXXXX", "XXXXXX", "XXDDXX"], names=names,
               notes="The queen's hall, 6 x 4 on borrowed grass: a long timber hall under a high "
                     "turf roof, its gable ends crowned with carved horse heads painted red, round "
                     "bronze-rimmed shields hung along the wall, Ares's spear-standard by the door. "
                     "The wide double door is `c22` and `c32` (`MB_NON_ANIMATED_DOOR`, two cells: a "
                     "wide door, which is why this set stops at 496 tiles). The roof's top row is "
                     "drawn over the player.")
    ground(s, "grass")
    M, T = s.M, s.T
    _hall(T, M, 0, 0, w, Hs.turf_px, 2, 2, [2])
    # shields along the upper wall
    for sx in (10, 26, 62, 78):
        for y in range(36, 46):
            for x in range(sx - 5, sx + 5):
                d = math.hypot(x - sx + 0.5, y - 40.5)
                if d < 4.8:
                    c = "tb4" if d > 3.6 else ("tb3" if x < sx else "tb2")
                    if d < 1.4:
                        c = "tb4"
                    M.px(x, y, c)
    return s


def stable():
    w, h_ = 6, 3
    names = {f"c{x}{y}": (x, y) for y in range(h_) for x in range(w)}
    s = struct("stable", "Diomedes's stable", w, h_, SEC_H,
               walk=["TTTTTT", "XXXXXX", "XXDDXX"], names=names,
               notes="The man-eating mares' stable (LABORS 8), 6 x 3 on borrowed grass: a long low "
                     "barn of black timber under a sagging thatch, stall hatches barred shut along "
                     "its front, horse skulls nailed over the wide double door (`c22` `c32`, "
                     "`MB_NON_ANIMATED_DOOR`). The roof's top row is drawn over the player. For the "
                     "Oikoumene, any steppe stable.")
    ground(s, "grass")
    M, T = s.M, s.T
    _hall(T, M, 0, 0, w, Hs.thatch_px, 2, 1, [2], finials=False)
    for hx in (8, 24, 72, 88):
        for y in range(36, 42):
            for x in range(hx - 4, hx + 4):
                c = "tb0" if (x + y) % 3 else "tb1"
                if y in (36, 41) or x in (hx - 4, hx + 3):
                    c = "tb0"
                M.px(x, y, c)
        for x in range(hx - 4, hx + 4):
            M.px(x, 38, "tb3")
    # skulls over the door
    for sx in (36, 58):
        put(M, sx - 2, 32, [".ww.", "w.ww", "wwww", ".ww."], {"w": "w0"})
    return s


# --------------------------------------------------------------------------
# Tents
# --------------------------------------------------------------------------

def _tent(L_T, L_M, ox, oy, felt, trim, door=True, sign=None):
    """A round felt tent, 3 x 3: a domed roof with a smoke vent, felt walls
    lashed with bands, a door flap in the bottom middle cell."""
    W, H = 48, 48
    dark, mid, light, lit = felt
    for y in range(2, 46):
        for x in range(W):
            # the dome: an ellipse; the wall: a band below it
            dome = math.hypot((x - 23.5) / 22.5, (y - 22) / 20) < 1 and y < 30
            wall = 26 <= y < 46 and abs(x - 23.5) <= 21.5
            if not (dome or wall):
                continue
            if dome and y < 30:
                u = (x - 23.5) / 22.5
                v = (y - 22) / 20
                lt = -0.6 * u - 0.7 * v
                c = lit if lt > 0.55 else (light if lt > 0.15 else (mid if lt > -0.3 else dark))
                if y in (12, 20):
                    c = trim
                if abs(x - 23.5) % 9 < 1 and y > 6:
                    c = trim
            else:
                u = (x - 23.5) / 21.5
                c = light if u < -0.4 else (mid if u < 0.5 else dark)
                if y in (33, 34):
                    c = trim
                if y == 45:
                    c = "ink"
            (L_T if y < 16 else L_M).px(ox + x, oy + y, c)
    # vent
    for x in range(19, 29):
        L_T.px(ox + x, oy + 4, "ink")
        L_T.px(ox + x, oy + 5, dark)
    # outline
    m = np.zeros((48, 48), bool)
    for y in range(48):
        for x in range(48):
            m[y, x] = (L_T if y < 16 else L_M).get(ox + x, oy + y) is not None
    for y, x in np.argwhere(F.edge_of(m)):
        (L_T if y < 16 else L_M).px(ox + int(x), oy + int(y), "ink")
    if door:
        for y in range(34, 46):
            for x in range(18, 30):
                c = dark if x < 24 else "ink"
                if y == 34 or x in (18, 29):
                    c = trim
                L_M.px(ox + x, oy + y, c)
        if sign == "rod":
            for y in range(36, 45):
                L_M.px(ox + 21, oy + y, "fr2")
            for (x, y) in ((20, 37), (22, 39), (20, 41), (22, 43)):
                L_M.px(ox + x, oy + y, "fr1")
        if sign == "goods":
            for y in range(34, 40):
                for x in range(16, 32):
                    L_M.px(ox + x, oy + y, "fr2" if (x // 3) % 2 else "fc2")
    for x in range(4, 46):
        if L_M.get(ox + x, oy + 46) is None:
            L_M.px(ox + x, oy + 46, "gd")


def tents():
    names = {}
    for i, nm in enumerate(("red", "cream")):
        for y in range(3):
            for x in range(3):
                names[f"{nm}{x}{y}"] = (i * 3 + x, y)
    names.update({"ascl_door": (6, 2), "agora_door": (6, 1), "flap_open": (6, 0)})
    s = struct("tents", "Felt tents", 7, 3, SEC_T,
               walk=["TTTTTTX", "XXXXXXD", "XDXXDXD"], names=names,
               notes="Round felt tents, 3 x 3 on borrowed grass: `red` (`red00` to `red22`, column "
                     "then row) is the Amazons' red felt banded with cream; `cream` is undyed felt "
                     "banded red, the guest tent you're lodged in. The domes' top rows are drawn over "
                     "the player; the door flap is the bottom middle cell (`MB_NON_ANIMATED_DOOR`). "
                     "Swaps for the bottom middle cell: `ascl_door` (on the cream tent: the rod of "
                     "Asclepius painted on its flap, Themiskyra's Asclepeion tent), `agora_door` (on "
                     "the red tent: an awning and goods, the Agora of Pontic goods). `flap_open` is "
                     "a flap tied back (`MB_NON_ANIMATED_DOOR`), for a household that's expecting "
                     "you. For the Oikoumene's Wagon Camp too.")
    ground(s, "grass")
    M, T = s.M, s.T
    _tent(T, M, 0, 0, ("fr0", "fr1", "fr2", "fr3"), "fc2")
    _tent(T, M, 48, 0, ("fc0", "fc1", "fc2", "w0"), "fr2")
    # swaps: copy the bottom-middle cells and paint on them
    M.a[32:48, 96:112] = M.a[32:48, 64:80]
    _tent_sign(M, 96, 32, "rod")
    M.a[16:32, 96:112] = M.a[32:48, 16:32]
    _tent_sign(M, 96, 16, "goods")
    M.a[0:16, 96:112] = M.a[32:48, 16:32]
    for y in range(2, 14):
        for x in range(2, 14):
            if x > 5:
                M.px(96 + x, y, "ink")
        M.px(96 + 5, y, "fr3")
        M.px(96 + 4, y, "fr2")
    F.set_walk(s, ["TTTTTTX", "XXXXXXD", "XDXXDXD"])
    return s


def _tent_sign(M, ox, oy, sign):
    if sign == "rod":
        for y in range(4, 13):
            M.px(ox + 8, oy + y, "fr2")
        for (x, y) in ((7, 5), (9, 7), (7, 9), (9, 11)):
            M.px(ox + x, oy + y, "fr1")
    else:
        for y in range(1, 6):
            for x in range(0, 16):
                M.px(ox + x, oy + y, "fr2" if (x // 3) % 2 else "fc2")
        for (x, y) in ((4, 9), (10, 10)):
            put(M, ox + x - 1, oy + y, [".f.", "fff", ".f."], {"f": "fc1"})


# --------------------------------------------------------------------------
# Wagons
# --------------------------------------------------------------------------

def wagons():
    names = {}
    for i, nm in enumerate(("red", "cream", "black")):
        for x in range(3):
            names[f"{nm}_roof{x}"] = (x, i)
    for x in range(3):
        names[f"body{x}"] = (x, 3)
    s = struct("wagons", "Felt-roofed wagon-houses", 3, 4, SEC_V,
               walk=["TTT", "TTT", "TTT", "XDX"], names=names, oik=True,
               notes="The Scythians' houses on wheels (Herodotus 4.46): a wagon-house is 3 x 2, a "
                     "felt roof over a timber body on four solid wheels. Pick a roof row, "
                     "`red_roof0` `red_roof1` `red_roof2` (red felt), `cream_roof*` (undyed felt) or "
                     "`black_roof*` (black felt stitched with blue), drawn over the player, and put "
                     "`body0` `body1` `body2` below it; `body1` is the door (`MB_NON_ANIMATED_DOOR`), "
                     "the rest impassable. Three households, three roofs: the archer chief's, the "
                     "barrow-keeper's, the racer's (OIKOUMENE 4.4's Wagon Camp).")
    ground(s, "grass")
    M, T = s.M, s.T
    for i, felt in enumerate((("fr0", "fr1", "fr2", "fr3", "fc2"), ("fc0", "fc1", "fc2", "w0", "fr2"),
                              ("ink", "fr0", "fb", "fc0", "fb"))):
        dark, mid, light, lit, trim = felt
        for y in range(2, 16):
            for x in range(1, 47):
                d = math.hypot((x - 23.5) / 22.5, (y - 16) / 13.5)
                if d < 1:
                    u = (x - 23.5) / 22.5
                    c = lit if u < -0.55 else (light if u < -0.1 else (mid if u < 0.5 else dark))
                    if (x - 2) % 9 == 0 or y == 9:
                        c = trim
                    T.px(x, i * 16 + y, c)
        m = np.zeros((16, 48), bool)
        for y in range(16):
            for x in range(48):
                m[y, x] = T.get(x, i * 16 + y) is not None
        for y, x in np.argwhere(F.edge_of(m)):
            if y < 15:
                T.px(int(x), i * 16 + int(y), "ink")
    # body and wheels
    oy = 48
    for y in range(0, 10):
        for x in range(2, 46):
            c = "tb3" if y < 2 else ("tb2" if (x % 6) else "tb1")
            if y == 9:
                c = "tb0"
            M.px(x, oy + y, c)
    for y in range(0, 10):
        for x in range(18, 30):
            c = "tb1" if x < 24 else "tb0"
            if x in (18, 29) or y == 0:
                c = "tb0"
            M.px(x, oy + y, c)
    for cx in (8, 39):
        for y in range(16):
            for x in range(cx - 7, cx + 8):
                d = math.hypot(x - cx, (y - 10) * 1.0)
                if d < 6.5:
                    c = "tb2" if d > 4.8 else ("tb3" if d > 1.5 else "tb0")
                    if d > 6:
                        c = "tb0"
                    M.px(x, oy + y, c)
    for x in range(2, 46):
        if M.get(x, oy + 15) is None:
            M.px(x, oy + 15, "gd")
    return s


# --------------------------------------------------------------------------
# The yard
# --------------------------------------------------------------------------

def yard():
    names = {"hearth": (0, 0), "cauldron": (1, 0), "milking_post": (2, 0), "well": (3, 0),
             "target_top": (4, 0), "target": (4, 1), "standard_top": (5, 0), "standard": (5, 1),
             "rack_L": (0, 1), "rack_R": (1, 1), "post": (2, 1), "shields": (3, 1),
             "horse_TL": (6, 0), "horse_TR": (7, 0), "horse_BL": (6, 1), "horse_BR": (7, 1)}
    s = struct("yard", "Hearths, the practice ground, horses", 8, 2, SEC_Y,
               walk=["XXXXTTTT", "XXXXXXXX"], names=names,
               notes="On borrowed grass, impassable. `hearth`: a camp hearth in a ring of stones, its "
                     "fire flickering (`fire`); `cauldron`: a Thracian bronze cauldron on a tripod "
                     "over the fire (the cook fires of Themiskyra). `milking_post`: a post with a "
                     "leather pail and a rope for the mares (OIKOUMENE 4.4; the mare-milker's daily "
                     "milk). `well`: Themiskyra's well, a stone curb with a timber frame. The "
                     "practice ground: `target` (with `target_top`), a straw butt on a stand painted "
                     "in rings; `rack_L` `rack_R`, a rack of spears with crescent pelta shields; "
                     "`post`, a hacked training post; `shields`, a stand of bronze-faced shields; "
                     "`standard` (with `standard_top`), Ares's spear-standard with red streamers. A "
                     "tethered horse (2 x 2, `horse_TL` to `horse_BR`): a bay mare tied to her post, "
                     "standing; her top row is drawn over the player. Top rows marked `T` are the "
                     "tall pieces' heads.")
    ground(s, "grass")
    M, T = s.M, s.T
    # hearth ring and fire
    for (ox, caul) in ((0, False), (16, True)):
        for a in range(0, 360, 40):
            x = ox + 8 + int(round(5.5 * math.cos(math.radians(a))))
            y = 10 + int(round(3.5 * math.sin(math.radians(a))))
            put(M, x - 1, y - 1, ["22", "11"], {"2": "sn2", "1": "sn1"})
        for x in range(ox + 4, ox + 13):
            for y in range(9, 12):
                M.px(x, y, "as1")
        if caul:
            for y in range(2, 10):
                for x in range(ox + 3, ox + 13):
                    d = math.hypot((x - ox - 7.5) / 5, (y - 4) / 5)
                    if d < 1 and y >= 3:
                        M.px(x, y, "bz3" if x < ox + 6 else ("bz2" if x < ox + 10 else "bz1"))
                M.px(ox + 3, y, "bz0") if y > 3 else None
            for x in range(ox + 3, ox + 13):
                M.px(x, 3, "bz0")
    fr = anim_layer(s, "fire", 3)
    for f, L in enumerate([M] + fr):
        for (ox, base) in ((0, 10), (16, 12)):
            for j, (dx, ht) in enumerate(((-2, 4), (0, 6), (2, 4), (-1, 3), (1, 5))):
                ht2 = ht + ((f + j) % 3) - 1
                for k in range(ht2):
                    c = "fi3" if k == 0 else ("fi2" if k < ht2 - 2 else "fi1")
                    L.px(ox + 8 + dx + (1 if (k + f) % 4 == 0 else 0), base - k, c)
    # milking post
    for y in range(1, 15):
        M.px(32 + 7, y, "bz1" if y > 1 else "bz2")
        M.px(32 + 8, y, "bz0")
    for (x, y) in ((5, 7), (6, 7), (9, 7), (10, 7), (4, 8), (11, 8), (5, 9), (10, 9)):
        M.px(32 + x, y, "sn2")
    put(M, 32 + 9, 9, ["0000", "0110", "0110", ".00."], {"0": "bz0", "1": "bz1"})
    # well
    for y in range(5, 15):
        for x in range(2, 14):
            d = math.hypot((x - 7.5) / 5.5, (y - 10) / 4.5)
            if d < 1:
                M.px(48 + x, y, "b3" if d < 0.55 else ("sn3" if y < 10 else "sn2"))
            elif d < 1.2:
                M.px(48 + x, y, "sn1")
    for y in range(1, 10):
        M.px(48 + 2, y, "tb1")
        M.px(48 + 13, y, "tb1")
    for x in range(2, 14):
        M.px(48 + x, 1, "tb1")
    M.px(48 + 7, 2, "tb1")
    M.px(48 + 7, 3, "tb1")
    # target on its stand (felt)
    for y in range(4, 24):
        for x in range(2, 14):
            d = math.hypot(x - 7.5, (y - 10) * 1.0)
            if d < 6:
                c = "fc1" if d > 4.8 else ("fr2" if d > 3.4 else ("fc2" if d > 2 else "fr2"))
                if d < 0.9:
                    c = "ink"
                (T if y < 16 else M).px(64 + x, y, c)
    for y in range(16, 31):
        M.px(64 + 4, y, "tb1")
        M.px(64 + 11, y, "tb1")
    T.px(64 + 9, 9, "tb1")
    T.px(64 + 10, 8, "tb1")
    # standard: a spear with a crescent and streamers
    for y in range(2, 31):
        (T if y < 16 else M).px(80 + 7, y, "tb1")
        (T if y < 16 else M).px(80 + 8, y, "ink")
    put(T, 80 + 4, 1, ["..33..", ".3223.", "3....3"], {"3": "bz3", "2": "sg3"})
    for (x, y) in ((9, 6), (10, 7), (11, 8), (10, 9), (11, 10), (12, 11), (9, 8), (9, 9)):
        T.px(80 + x, y, "fr2" if (x + y) % 2 else "fr3")
    for x in range(84, 93):
        M.px(x, 31, "gd")
    # spear rack with pelta shields
    for y in range(18, 31):
        for x in range(0, 32):
            if y in (22, 29) and 1 <= x <= 30:
                M.px(x, y, "tb2")
        for x in (2, 29):
            M.px(x, y, "tb1")
    for sx in range(5, 29, 4):
        for y in range(16, 30):
            M.px(sx, y, "tb3" if y > 18 else "w0")
    for cx in (9, 22):
        for y in range(22, 30):
            for x in range(cx - 4, cx + 5):
                d = math.hypot(x - cx, (y - 26) * 1.1)
                if d < 4.2 and not (y < 24 and abs(x - cx) < 1.5):
                    M.px(x, y, "sg3" if d < 2 else ("sg2" if d < 3.2 else "tb0"))
    for x in range(1, 31):
        M.px(x, 31, "gd")
    # training post
    for y in range(18, 31):
        for x in range(5, 11):
            c = "tb3" if x < 7 else ("tb2" if x < 9 else "tb1")
            if (x * 3 + y) % 7 == 0:
                c = "tb0"
            M.px(32 + x, y, c)
    for x in range(36, 46):
        M.px(x, 31, "gd")
    # shields on a stand
    for (cx, cy) in ((52, 23), (58, 25), (54, 28)):
        for y in range(cy - 4, cy + 5):
            for x in range(cx - 4, cx + 5):
                d = math.hypot(x - cx, y - cy)
                if d < 4.4:
                    M.px(x, y, "bz3" if d < 1.2 else ("bz2" if x < cx else "bz1"))
                elif d < 5.0:
                    M.px(x, y, "bz0")
    # the tethered mare: a bay standing side-on, tied to a post
    horse = [
        "................................",
        "................................",
        ".....................00.........",
        "....................0110........",
        "...................01211000.....",
        "..................0122211110....",
        ".................01222211w10....",
        "................01222221.00.....",
        ".00000000000000122222210........",
        "0122222222222222222221110.......",
        "01222222222222222222211110......",
        "012222222222222222222111100.....",
        "0122222222222222222221110.......",
        ".0122222222222222222211110......",
        "..01111111111111111111110.......",
        "..011.0110.......0110.0110......",
        "..011..011.......011..011.......",
        "..011..011.......011..011.......",
        "..011..011.......011..011.......",
        "..022..022.......022..022.......",
        "..000..000.......000..000.......",
    ]
    for j, row in enumerate(horse):
        for i, ch in enumerate(row):
            if ch in "012w":
                c = {"0": "tb0", "1": "tb1", "2": "tb2", "w": "w0"}[ch]
                X, Y = 96 + i, 6 + j
                (T if Y < 16 else M).px(X, Y, c)
    for (x, y) in ((96 + 3, 15), (96 + 2, 16), (96 + 1, 17)):
        (T if y < 16 else M).px(x, y, "tb0")
    for y in range(16, 31):
        M.px(96 + 28, y, "tb1")
        M.px(96 + 29, y, "tb0")
    for x in range(96 + 23, 96 + 28):
        M.px(x, 16 + (x - 96 - 23) // 2, "sg3")
    for x in range(96, 96 + 30):
        if M.get(x, 27) is None:
            M.px(x, 27, "gd")
    F.settle(s, "fire", [(0, 0), (1, 0)])
    return s


def fence():
    from farlands_kits import FENCE_NOTES, fence_kit
    return fence_kit("fence", "Horse-field fence", SEC_Y, ("tb0", "tb1", "tb2", "tb3"), "gd",
                     notes=FENCE_NOTES + " Themiskyra's horse field, Diomedes's yard, the Wagon "
                     "Camp's horse lines.")


def troughs():
    names = {"trough_L": (0, 0), "trough_R": (1, 0), "hay": (2, 0)}
    s = struct("troughs", "A trough and hay", 3, 1, SEC_Y, walk=["XXX"], names=names,
               notes="On borrowed grass, impassable: `trough_L` `trough_R`, a hollowed-log water "
                     "trough two cells long; `hay`, a stack of hay on a pole, eaten at the bottom.")
    ground(s, "grass")
    M = s.M
    for y in range(5, 13):
        for x in range(2, 30):
            if y in (5, 12) or x in (2, 29):
                c = "tb0"
            elif y == 6:
                c = "tb3"
            elif y < 9:
                c = "b3" if (x + y) % 5 else "w0"
            else:
                c = "tb2" if y < 11 else "tb1"
            M.px(x, y, c)
    for x in range(3, 31):
        M.px(x, 13, "gd")
    for y in range(16):
        for x in range(16):
            d = math.hypot((x - 7.5) / 6.5, (y - 8) / 7.5)
            if d < 1 and y < 14:
                u = (x - 7.5) + (y - 8)
                c = "sg3" if u < 0 else ("sg2" if u < 5 else "sg1")
                if F.h(x, y, 5) % 5 == 0:
                    c = "sg0"
                M.px(32 + x, y, c)
    for y in range(0, 3):
        M.px(32 + 7, y, "sg0")
    for x in range(34, 47):
        M.px(x, 14, "gd")
    return s


def build():
    out = {}
    stp = St.build()
    for k in ("road", "road_join", "decor"):
        out[k] = stp[k]
    for s in (palisade(), gate(), hall(), stable(), tents(), wagons(), yard(), fence(), troughs()):
        out[s.key] = s
    return out


SPEC = {
    "symbol": "gTileset_SteppeCamp", "dir": "steppe_camp", "label": "SteppeCamp",
    "title": "the horse-peoples' camps: Themiskyra, Diomedes's yard, the Wagon Camp",
    "doc": "TILES_steppe_camp.md",
    "limit": 496,
    "sections": [
        ("ground", ["road", "road_join", "decor"]),
        ("walls", ["palisade", "gate"]),
        ("halls", ["hall", "stable"]),
        ("tents", ["tents", "wagons"]),
        ("yard", ["yard", "fence", "troughs"]),
    ],
    "rows": {"ground": 0, "walls": 10, "halls": 16, "tents": 24, "yard": 32},
    "why_split": "The steppe's land fills `steppe`'s 504 tiles, so the camps built on it are "
                 "their own set (and the Greek colonies another, `steppe_town`). Themiskyra borders the "
                 "Thermodon Road, Diomedes's yard the Bistonian Plain, the Wagon Camp the Steppe Road: "
                 "each meets the open steppe across a seam strip of aethos ground (MAP_DESIGN 5). The "
                 "road, its joins and the meadow's flowers are the steppe's own, redrawn here.",
}
