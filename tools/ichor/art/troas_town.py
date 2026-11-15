"""Ilion's and Sestos's buildings for gTileset_Troas: the Trojan house kit, Priam's
megaron, the temple of Athena, and the things in yards and lanes.

The house kit is Troy's own: flat roofs of packed clay behind a low parapet, a
row of round beam ends under the roof, lime plaster over mudbrick, timber doors
and small windows, a darker socle. Every part comes in ochre plaster and, slot
for slot, in whitewash (troas_lib's plaster and plaster2 groups), so a white
house costs no tiles. Houses are assembled by the map builder from parts.

Priam's megaron and the temple are symmetric, so each costs about half its
tiles; both are in the marble group (marble, bronze, gold, terracotta).
"""
from __future__ import annotations

import numpy as np

import emporion_lib as E
from troas_lib import WHITEWASH, ashlar, finish, mirror_x, plaster, recolor, struct

# --------------------------------------------------------------------------
# The house kit
# --------------------------------------------------------------------------

KIT_NAMES = {
    "roof_W": (0, 0), "roof": (1, 0), "roof_E": (2, 0), "roof_jars": (3, 0),
    "up_W": (0, 1), "up": (1, 1), "up_E": (2, 1), "up_window": (3, 1), "up_shutters": (4, 1),
    "lo_W": (0, 2), "lo": (1, 2), "lo_E": (2, 2), "lo_window": (3, 2), "door": (4, 2),
    "stable_door": (5, 2),
}


def roof_cell(L, x0, west=False, east=False):
    """A flat clay roof from above, its parapet lip along the front."""
    for y in range(0, 16):
        for x in range(x0, x0 + 16):
            X = x - x0
            c = "rf1"
            if (X * 5 + y * 3) % 13 == 0:
                c = "rf2"
            elif (X * 7 + y * 11) % 17 == 0:
                c = "rf0"
            L.px(x, y, c)
    L.hline(x0, x0 + 15, 0, "ink")
    L.hline(x0, x0 + 15, 1, "rf2")
    # the parapet lip at the front
    L.hline(x0, x0 + 15, 11, "rf0")
    L.hline(x0, x0 + 15, 12, "pl3")
    L.hline(x0, x0 + 15, 13, "pl2")
    L.hline(x0, x0 + 15, 14, "pl2")
    L.hline(x0, x0 + 15, 15, "pl1")
    if west:
        L.vline(x0, 0, 15, "ink")
        L.vline(x0 + 1, 1, 10, "rf2")
    if east:
        L.vline(x0 + 15, 0, 15, "ink")
        L.vline(x0 + 14, 1, 10, "rf0")


def wall_cell(L, x0, y0, west=False, east=False, beams=False, socle=False):
    plaster(L, x0, y0, 16, 16, ox=x0, oy=y0)
    if beams:
        # the roof beams' round ends in a row under the parapet
        L.hline(x0, x0 + 15, y0, "pl1")
        for x in range(x0, x0 + 16):
            L.px(x, y0 + 1, "wd0")
            L.px(x, y0 + 4, "wd0")
        for bx in (x0 + 1, x0 + 9):
            L.blit([".kk.", "kwWk", "kWWk", ".kk."], {"k": "wd0", "w": "wd2", "W": "wd1"}, bx, y0 + 1)
        L.hline(x0, x0 + 15, y0 + 5, "pl1")
    if socle:
        for x in range(x0, x0 + 16):
            L.px(x, y0 + 12, "pl1")
            L.px(x, y0 + 13, "pl0")
            L.px(x, y0 + 14, "pl0" if (x // 4) % 2 else "pl1")
            L.px(x, y0 + 15, "sk")
    if west:
        L.vline(x0, y0, y0 + 15, "ink")
        L.vline(x0 + 1, y0, y0 + 15, "pl3")
    if east:
        L.vline(x0 + 15, y0, y0 + 15, "ink")
        L.vline(x0 + 14, y0, y0 + 15, "pl1")
        L.vline(x0 + 13, y0, y0 + 15, "pl1" if not socle else L.get(x0 + 13, y0) or "pl1")


def window(L, x, y, w=6, h=6, shutters=False):
    L.rect(x - 1, y - 1, w + 2, h + 2, "wd0")
    L.rect(x, y, w, h, "ink")
    L.hline(x, x + w - 1, y + h - 1, "wd1")
    L.hline(x - 1, x + w, y + h + 1, "pl3")     # the sill, lit
    if shutters:
        for sx in (x - 3, x + w + 1):
            L.rect(sx, y - 1, 2, h + 2, "b1")
            L.vline(sx, y - 1, y + h, "ink")


def kit():
    s = struct("house_kit", "Trojan house kit (ochre plaster)", 6, 3,
               walk=["XXXXXX", "XXXXXX", "XXXXDD"],
               notes="Assemble a house of width n from three rows: roof_W roof... roof_E; up_W "
                     "... up_E; lo_W ... lo_E, with windows, a door or the stable's double "
                     "door in the middles. roof_jars varies a roof. door and stable_door are "
                     "MB_NON_ANIMATED_DOOR: put the warp there.",
               names=KIT_NAMES)
    B = s.B
    for cx in range(6):
        roof_cell(B, cx * 16, west=cx == 0, east=cx == 2)
        wall_cell(B, cx * 16, 16, west=cx == 0, east=cx == 2, beams=True)
        wall_cell(B, cx * 16, 32, west=cx == 0, east=cx == 2, socle=True)
    # roof variants: storage jars by the parapet; a smoke hatch; a second texture
    for (x, y) in ((51, 5), (57, 6)):
        B.blit([".kk.", "kttk", "kTtk", "kttk", ".kk."], {"k": "ink", "t": "rf2", "T": "pl3"}, x, y)
    # upper wall: window, shuttered window, a painted band
    window(B, 53, 23)
    window(B, 69, 23, shutters=True)
    # lower wall: window, door, stable door
    window(B, 53, 36, h=5)
    # the door: timber planks in a dark frame, a bronze ring
    for y in range(34, 48):
        for x in range(67, 77):
            B.px(x, y, "wd1" if (x - 67) % 3 else "wd0")
    B.rect(66, 33, 12, 1, "ink")
    B.vline(66, 33, 47, "ink")
    B.vline(77, 33, 47, "ink")
    B.hline(66, 77, 32, "wd0")
    B.px(74, 41, "w0")
    # the stable's double door, braced
    for y in range(33, 48):
        for x in range(81, 95):
            B.px(x, y, "wd1" if (x - 81) % 4 else "wd0")
    for k in range(12):
        B.px(82 + k, 46 - k, "wd2")
    B.vline(88, 33, 47, "ink")
    B.rect(80, 32, 16, 1, "ink")
    B.vline(80, 32, 47, "ink")
    B.vline(95, 32, 47, "ink")
    for cx, cy in ((4, 2), (5, 2)):
        s.behaviors[(cx, cy)] = "MB_NON_ANIMATED_DOOR"
    return finish(s)


def kit_white(k):
    return recolor(k, WHITEWASH, "house_kit_white", "Trojan house kit (whitewash)",
                   notes="The house kit in whitewash, part for part: same names as house_kit.")


# --------------------------------------------------------------------------
# Priam's megaron
# --------------------------------------------------------------------------

HORSE = [
    "....kk......",
    "...kkkk.....",
    "..kk.kkkkkk.",
    ".k...kkkkkkk",
    ".....kk..k.k",
    ".....k...k.k",
]


def palace():
    """Priam's palace on the citadel: a broad megaron with a painted frieze of
    horses (Troy "of the fine horses"), a deep porch with two great columns in
    antis, the door at the back of the porch, three broad steps. Symmetric."""
    s = struct("priams_palace", "Priam's palace", 5, 4, walk=["XXXXX", "XXXXX", "XXXXX", "XXDXX"],
               notes="5 x 4. Door at (2,3). The crown of the citadel after the temple.")
    B = s.B
    W = 80
    # row 0: terracotta roof edge and a cornice with gilded disks
    for y in range(0, 10):
        for x in range(W):
            X = x % 8
            c = "tc1"
            if X == 6:
                c = "tc2"
            elif X == 7:
                c = "tc0"
            elif y % 4 == 0:
                c = "tc2"
            B.px(x, y, c)
    B.hline(0, W - 1, 0, "ink")
    B.hline(0, W - 1, 10, "ink")
    for y in (11, 12):
        B.hline(0, W - 1, y, "m1")
    B.hline(0, W - 1, 13, "m3")
    for x in range(4, W, 8):
        B.rect(x, 11, 2, 2, "g1")
    B.hline(0, W - 1, 14, "ink")
    B.hline(0, W - 1, 15, "m2")
    # row 1: the frieze of horses on a cream ground, framed
    for y in range(16, 30):
        B.hline(0, W - 1, y, "m1")
    B.hline(0, W - 1, 16, "tc0")
    B.hline(0, W - 1, 29, "tc0")
    for x in (2, 18, 34):
        B.blit(HORSE, {"k": "tc0"}, x, 19)
        B.px(x + 3, 25, "tc1")
    B.hline(0, W - 1, 30, "m3")
    B.hline(0, W - 1, 31, "ink")
    # rows 2-3: the antae, the porch, two columns
    for y in range(32, 64):
        for x in range(W):
            B.px(x, y, "m5" if y < 36 else "m4" if x % 16 else "m5")
    # the antae: the side walls' ends, in ashlar-like marble courses
    for y in range(32, 64):
        for x in range(0, 10):
            c = "m1" if x < 3 else "m2" if x < 8 else "m3"
            if (y - 32) % 8 == 7:
                c = "m3"
            B.px(x, y, c)
        B.px(0, y, "ink")
        B.px(10, y, "ink")
    # the back wall of the porch with the door
    for y in range(40, 62):
        for x in range(10, W - 10):
            B.px(x, y, "m3" if (y - 40) % 6 else "m4")
    # the columns at x 18..27 and their mirror: tapering Minoan-Mycenaean shafts,
    # dark red with a gold ring under the capital
    for y in range(34, 60):
        t = (y - 34) / 26
        hw = int(round(4 + 1.5 * t))
        for x in range(23 - hw, 23 + hw):
            c = "tc1" if x < 23 - hw + 2 else "tc0" if x >= 23 + hw - 2 else "tc2" if x < 23 else "tc1"
            B.px(x, y, c)
        B.px(23 - hw - 1, y, "ink")
        B.px(23 + hw, y, "ink")
    B.rect(16, 32, 14, 4, "m1")
    B.hline(16, 29, 32, "ink")
    B.hline(16, 29, 35, "m4")
    B.hline(18, 27, 36, "g1")
    B.rect(17, 59, 12, 3, "m2")
    B.hline(17, 28, 59, "m1")
    # the door: tall double leaves of dark wood banded in bronze (marble group's
    # bronze and gold, its own tiles)
    for y in range(44, 62):
        for x in range(32, 40):
            B.px(x, y, "br" if (x - 32) % 4 else "m5")
    for y in (48, 56):
        B.hline(32, 39, y, "g0")
    B.hline(32, 39, 43, "ink")
    B.vline(32, 43, 61, "ink")
    # the steps
    for y in range(62, 64):
        B.hline(0, W - 1, y, "m1" if y == 62 else "m3")
    mirror_x(B, 0, W, 0, 64)
    B.vline(39, 44, 61, "ink")
    B.vline(40, 44, 61, "m5")
    B.px(37, 52, "g1")
    B.px(42, 52, "g1")
    return finish(s)


# --------------------------------------------------------------------------
# The temple of Athena
# --------------------------------------------------------------------------

def temple_athena():
    """Athena Ilias on the summit: a marble Doric temple, the gilded owl on the
    gable, triglyphs and painted metopes, four columns before a dark porch and
    the door. The Palladion is inside. Symmetric."""
    s = struct("temple_athena", "The temple of Athena", 5, 5,
               walk=["XXXXX", "XXXXX", "XXXXX", "XXXXX", "XXDXX"],
               notes="5 x 5, the city's crown on the citadel's summit. Door at (2,4).")
    G, B = s.M, s.B
    W = 80
    # rows 0-1 stand on the summit's grass: the gable is drawn on the middle layer
    # over borrowed ground, rows 2-4 are the temple's body
    s.set_ground("grass", [(x, y) for y in range(2) for x in range(5)])
    # the gable: raking cornice and tympanum
    for y in range(4, 32):
        half = min(40, int((y - 4) / 26 * 40) + 1)
        for x in range(40 - half, 40):
            c = "tc1" if y < 7 or x < 40 - half + 3 else "tc2"
            G.px(x, y, c)
        G.px(40 - half - 1, y, "ink")
    for y in range(8, 30):
        half = int((y - 8) / 22 * 33)
        for x in range(40 - half, 40):
            G.px(x, y, "m1" if y > 11 else "m2")
    # the tympanum's relief: Athena's shield and spear, in gold
    G.blit(["..kk..", ".kggk.", "kgGGgk", "kgGGgk", ".kggk.", "..kk.."],
           {"k": "ink", "g": "g0", "G": "g1"}, 34, 18)
    G.vline(30, 14, 28, "br")
    # the gilded owl on the apex (acroterion)
    G.blit(["..k..k..", "..kkkk..", ".kgggg..", ".kgwgw..", ".kgggg..", "..kggk..", "...kk..."],
           {"k": "ink", "g": "g0", "w": "fc"}, 36, 0)
    G.hline(0, W - 1, 30, "m4")
    G.hline(0, W - 1, 31, "ink")
    mirror_x(G, 0, W, 0, 32)
    # row 2: the entablature: architrave, triglyphs and painted metopes
    for y in range(32, 48):
        B.hline(0, W - 1, y, "m1")
    B.hline(0, W - 1, 32, "tc1")
    B.hline(0, W - 1, 33, "tc0")
    for x in range(0, W, 8):
        B.rect(x, 35, 4, 7, "m3")
        B.vline(x + 1, 35, 41, "m5")
        B.vline(x + 2, 35, 41, "m4")
        B.rect(x + 4, 36, 3, 5, "tc2")
        B.px(x + 5, 37, "tc0")
        B.px(x + 5, 39, "tc0")
    B.hline(0, W - 1, 42, "m4")
    B.hline(0, W - 1, 43, "m2")
    for y in range(44, 48):
        B.hline(0, W - 1, y, "w0" if y == 44 else "m2")
    B.hline(0, W - 1, 47, "m4")
    # rows 3-4: the dark porch and four Doric columns, the door between
    for y in range(48, 80):
        for x in range(W):
            B.px(x, y, "m5" if y < 54 or (x % 8 == 7 or y % 8 == 7) else "m4")
    for cxs in (6, 22):
        E.doric_capital(B, cxs, 48, 6)
        E.shaft(B, cxs, 53, 6, 21)
    # the door at the back of the porch: bronze leaves
    for y in range(58, 76):
        for x in range(33, 40):
            B.px(x, y, "br" if (x - 33) % 3 else "g0")
    B.hline(33, 39, 57, "ink")
    B.vline(33, 57, 75, "ink")
    # the stylobate's steps
    for y in range(74, 80):
        B.hline(0, W - 1, y, "w0" if y in (74, 77) else "m2" if y in (75, 78) else "m3")
    mirror_x(B, 0, W, 0, 80)
    B.vline(40, 58, 73, "ink")
    return finish(s)


# --------------------------------------------------------------------------
# Yards, lanes and springs
# --------------------------------------------------------------------------

def herm():
    """A great herm: a tall marble pillar with Hermes's bearded head, garlanded."""
    s = struct("great_herm", "A great herm", 1, 2, walk=["X", "X"],
               notes="The waystone (ICHOR_STUB_HERM until the Oikoumene's herm run exists). "
                     "Read it from below.", ground="grass")
    M = s.M
    M.rect(4, 8, 8, 22, "m1")
    M.vline(4, 8, 29, "w0")
    M.vline(10, 8, 29, "m3")
    M.vline(11, 8, 29, "m4")
    M.rect(3, 28, 10, 4, "m3")
    M.hline(3, 12, 28, "m1")
    M.blit(["..kkkk..", ".kmmmmk.", "kmkmmkmk", "kmmmmmmk", ".kbbbbk.", ".kbbbbk.", "..kbbk..",
            "...kk..."], {"k": "ink", "m": "m1", "b": "m4"}, 4, 1)
    for x in range(3, 13):
        M.px(x, 12 + (1 if x in (3, 12) else 0), "g0" if x % 2 else "g1")
    E.silhouette_outline(M, (0, 0, 16, 32))
    return finish(s)


def yard():
    """Things for yards and lanes, all on grass: a hay rick, a stone trough, the
    mason's stacked blocks, column drums, dye vats, and a two-cell chariot."""
    s = struct("yard", "Yard things", 7, 1, walk=["XXXXXXX"], ground="grass",
               names={"hay": (0, 0), "trough": (1, 0), "blocks": (2, 0), "drums": (3, 0),
                      "dye_vats": (4, 0), "chariot_W": (5, 0), "chariot_E": (6, 0)},
               notes="hay, trough (horses drink here), blocks and drums (the mason's yard), "
                     "dye_vats (the peplos-weaver's), a chariot (two cells). All impassable.")
    M = s.M
    # hay rick (wood group)
    E.fill_mask(M, E.ellipse_mask(14, 12), 1, 3, "wd3")
    for y in range(3, 15):
        for x in range(1, 15):
            if M.get(x, y) == "wd3" and (x + 2 * y) % 5 == 0:
                M.px(x, y, "rp")
            if M.get(x, y) == "wd3" and (x * 3 + y) % 7 == 0:
                M.px(x, y, "wd2")
    E.silhouette_outline(M, (0, 0, 16, 16), "wd1")
    M.hline(3, 12, 15, "wd1")
    # trough (stone group)
    M.rect(17, 6, 14, 8, "s3")
    M.rect(19, 7, 10, 4, "b3")
    M.hline(19, 28, 7, "w0")
    M.hline(17, 30, 6, "s5")
    M.hline(17, 30, 13, "s1")
    M.vline(17, 6, 13, "sk")
    M.vline(30, 6, 13, "sk")
    M.hline(18, 29, 14, "s1")
    # blocks (stone group)
    for (x, y, w) in ((33, 9, 7), (40, 9, 7), (36, 3, 7)):
        M.rect(x, y, w, 6, "s4")
        M.hline(x, x + w - 1, y, "s5")
        M.vline(x + w - 1, y, y + 5, "s2")
        M.hline(x, x + w - 1, y + 5, "s1")
        M.vline(x, y, y + 5, "sk")
    # column drums (stone group, fluted)
    for (x, y) in ((49, 8), (56, 9)):
        E.fill_mask(M, E.ellipse_mask(7, 6), x, y, "s4")
        M.px(x + 3, y + 2, "s5")
        M.px(x + 2, y + 3, "s3")
        E.silhouette_outline(M, (x - 1, y - 1, 9, 8), "s1")
    M.rect(51, 3, 8, 5, "s3")
    M.hline(51, 58, 3, "s5")
    M.vline(51, 3, 7, "sk")
    M.vline(58, 3, 7, "s1")
    # dye vats (wood group: tubs of red and blue)
    for (x, c) in ((65, "rd"), (72, "b1")):
        M.rect(x, 6, 7, 8, "wd1")
        M.hline(x, x + 6, 6, "wd0")
        M.hline(x + 1, x + 5, 7, c)
        M.hline(x + 1, x + 5, 8, c)
        M.hline(x, x + 6, 10, "wd0")
        M.vline(x, 6, 13, "ink")
        M.vline(x + 6, 6, 13, "ink")
        M.hline(x, x + 6, 14, "ink")
    M.vline(70, 2, 7, "wd2")
    # the chariot (wood group): a light car on two four-spoked wheels, pole up
    for (cx, cy) in ((86, 9), (100, 9)):
        E.fill_mask(M, E.ellipse_mask(10, 10), cx - 5, cy - 4, "ink")
        E.fill_mask(M, E.ellipse_mask(8, 8), cx - 4, cy - 3, "wd2")
        E.fill_mask(M, E.ellipse_mask(4, 4), cx - 2, cy - 1, "ink")
        M.px(cx - 1, cy + 1, "br")
        M.px(cx, cy + 1, "g0")
        M.hline(cx - 4, cx + 3, cy + 1, "wd0")
        M.vline(cx - 1, cy - 3, cy + 5, "wd0")
    M.rect(88, 2, 12, 7, "rd")
    M.hline(88, 99, 2, "g1")
    M.vline(88, 2, 8, "ink")
    M.vline(99, 2, 8, "ink")
    M.hline(88, 99, 8, "ink")
    M.line(100, 4, 109, 0, "wd1")
    M.line(100, 5, 109, 1, "ink")
    return finish(s)


def springs():
    """The two springs of the Skamander under the walls, one warm and one cold,
    with the stone washing-troughs where Trojan women washed their clothes in
    peacetime (Iliad 22.147-156)."""
    s = struct("springs", "The twin springs and washing troughs", 2, 1, walk=["XX"],
               notes="Two cells: the warm spring (a wisp of steam) and the cold, each running "
                     "into a long stone trough.", ground="grass")
    M = s.M
    for x0 in (0, 16):
        M.rect(x0 + 1, 4, 14, 10, "s3")
        M.rect(x0 + 3, 6, 10, 5, "b3")
        M.hline(x0 + 3, x0 + 12, 6, "w0")
        M.hline(x0 + 1, x0 + 14, 4, "s5")
        M.hline(x0 + 1, x0 + 14, 13, "s1")
        M.vline(x0 + 1, 4, 13, "sk")
        M.vline(x0 + 14, 4, 13, "sk")
        M.hline(x0 + 2, x0 + 13, 14, "s2")
        M.rect(x0 + 6, 1, 4, 3, "s2")
        M.hline(x0 + 6, x0 + 9, 1, "s4")
        M.px(x0 + 7, 4, "w0")
        M.px(x0 + 8, 5, "b3")
    for (x, y) in ((6, 0), (7, 1), (5, 2), (9, 0)):
        M.px(x, y, "w0")
    return finish(s)


def build():
    k = kit()
    return [k, kit_white(k), palace(), temple_athena(), herm(), yard(), springs()]


__all__ = ["build", "ashlar", "np"]
