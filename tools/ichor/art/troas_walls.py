"""Ilion's great sloping walls, its gates and towers, and Hero's tower at Sestos,
for gTileset_Troas.

Troy's walls (Troy VI, the walls Poseidon and Apollo built for Laomedon) are
pale limestone ashlar, battered: the face leans back, each course catching the
sun on its lip, with shallow vertical offsets every few strides. Seen from the
south in Gen 3's three-quarter view, a wall is three rows: the walkway and its
crenellated parapet on top, then two rows of sloping face.

Every piece is in the stone group but the gates' timber and bronze (wood) and
Hero's lamp (marble), each kept to its own 8x8 tiles.
"""
from __future__ import annotations

import numpy as np

from troas_lib import ashlar, finish, mirror_x, struct

# --------------------------------------------------------------------------
# Painters
# --------------------------------------------------------------------------


def walkway(L, x0, y0, w, h):
    """The wall's top seen from above: packed earth and flags, lightly joined."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = x % 16, (y - y0) % 16
            c = "s3"
            if Y % 5 == 4 or (X + (Y // 5) * 6) % 11 == 10:
                c = "s2"
            elif (X * 3 + Y * 7) % 17 == 0:
                c = "s4"
            L.px(x, y, c)


def parapet(L, x0, y0, w, crenels=True):
    """A parapet 6 px tall along the south edge of a wall top: its lit top,
    its front, a notch every 8 px."""
    L.hline(x0, x0 + w - 1, y0, "sk")
    L.hline(x0, x0 + w - 1, y0 + 1, "s5")
    L.hline(x0, x0 + w - 1, y0 + 2, "s4")
    for y in range(y0 + 3, y0 + 6):
        L.hline(x0, x0 + w - 1, y, "s4" if y < y0 + 5 else "s3")
    if crenels:
        for x in range(x0, x0 + w):
            if x % 8 in (5, 6):
                L.px(x, y0, "s1")
                L.px(x, y0 + 1, "s2")
                L.px(x, y0 + 2, "s2")
            if x % 8 == 7:
                L.vline(x, y0 + 1, y0 + 2, "s1")


def face(L, x0, y0, w, h, foot=True):
    """The battered face: big courses, each lit along its top lip; the foot
    darkens and grows a little weed where it meets the ground."""
    ashlar(L, x0, y0, w, h, ox=0, oy=y0, course=8, light="s5", body="s4", joint="s2", shade="s3",
           batter=True)
    # the slope: a soft shade band low on every course
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if (y - y0) % 8 == 5 and L.get(x, y) == "s4":
                L.px(x, y, "s3")
    if foot:
        for x in range(x0, x0 + w):
            L.px(x, y0 + h - 1, "s1")
            L.px(x, y0 + h - 2, "s2" if x % 3 else "s1")
            if x % 16 in (3, 4, 11):
                L.px(x, y0 + h - 2, "alg")
                L.px(x, y0 + h - 3, "ol1" if x % 16 in (3, 11) else L.get(x, y0 + h - 3))


def side(L, x0, y0, h, left=True):
    """The wall's end seen edge-on: a shaded strip 4 px wide."""
    xs = range(x0, x0 + 4) if left else range(x0 - 3, x0 + 1)
    for i, x in enumerate(xs):
        for y in range(y0, y0 + h):
            c = "s2" if (i in (1, 2)) else "s1"
            if (y - y0) % 8 == 7:
                c = "s1"
            L.px(x, y, c)
    L.vline(x0 if left else x0, y0, y0 + h - 1, "sk")


# --------------------------------------------------------------------------
# The walls
# --------------------------------------------------------------------------

def wall():
    """The great wall running west-east, three rows: [end_W, run, run, offset,
    end_E]. Drop an offset every 3-5 cells of run."""
    s = struct("wall", "Ilion's great wall (west-east)", 5, 3, walk=["XXXXX"] * 3,
               notes="Three rows: the walkway and parapet, then two rows of the sloping face. "
                     "Columns: west end, run, run (the same), an offset (Troy's shallow setback), "
                     "east end. All impassable.")
    B = s.B
    for cx in range(5):
        x0 = cx * 16
        walkway(B, x0, 0, 16, 10)
        parapet(B, x0, 10, 16)
        face(B, x0, 16, 16, 32)
    # the offset: a vertical setback, lit on its west lip, shadow to its east
    for y in range(10, 48):
        B.px(53, y, "s5")
        B.px(54, y, "sk")
        B.px(55, y, "s1")
        B.px(56, y, "s2")
    B.px(54, 9, "s2")
    # ends
    side(B, 0, 0, 48, left=True)
    side(B, 79, 0, 48, left=False)
    s.names = {"end_W": (0, 0), "run": (1, 0), "offset": (3, 0), "end_E": (4, 0)}
    return finish(s)


def wall_ns():
    """The wall running north-south, one cell a row: its walkway, the parapet on
    the outer side, and a sliver of sloping face beyond. ns_W: outer face to the
    west. ns_E: to the east. corner_W and corner_E are 3-row columns where a
    north-south wall meets the great wall's south face."""
    s = struct("wall_ns", "Ilion's wall (north-south) and its corners", 4, 3, walk=["XXXX"] * 3,
               notes="Row 0, cells 0-1: ns_W and ns_E, to repeat down a north-south run (outer "
                     "face west, or east). Cells 2-3 (three rows): the corner where a west or "
                     "east wall turns into the great wall's south face; put it at the face's "
                     "end in place of end_W or end_E.")
    B = s.B
    for cy in range(3):
        # ns_W: face sliver 0-5, parapet 6-9, walkway 10-15
        y0 = cy * 16
        for y in range(y0, y0 + 16):
            for x in range(0, 6):
                c = "s3" if (y + x) % 8 else "s2"
                if (y % 8) == 7:
                    c = "s2"
                if x == 0:
                    c = "s1"
                B.px(x, y, c)
            B.px(6, y, "sk")
            B.px(7, y, "s5")
            B.px(8, y, "s4")
            B.px(9, y, "s1" if y % 8 in (5, 6) else "s4")
        walkway(B, 10, y0, 6, 16)
    # copy ns_W mirrored into ns_E
    B.a[:, 16:32] = B.a[:, 0:16][:, ::-1]
    # corner W: the north-south run comes down and turns into the south face
    walkway(B, 32, 0, 16, 10)
    for y in range(0, 10):
        B.px(32, y, "s1")
        for x in range(33, 38):
            B.px(x, y, "s3" if (y + x) % 8 else "s2")
        B.px(38, y, "sk")
        B.px(39, y, "s5")
        B.px(40, y, "s4")
    parapet(B, 32, 10, 16)
    face(B, 32, 16, 16, 32)
    side(B, 32, 10, 38, left=True)
    B.a[:, 48:64] = B.a[:, 32:48][:, ::-1]
    s.names = {"ns_W": (0, 0), "ns_E": (1, 0), "corner_W": (2, 0), "corner_E": (3, 0)}
    return finish(s)


def tower():
    """A bastion tower standing out of the wall: its crenellated platform, then
    three rows of face, one more than the wall's, so it projects south. An arrow
    slit in the middle. Symmetric."""
    s = struct("tower", "A tower on Ilion's wall", 3, 4, walk=["XXX"] * 4,
               notes="Place its top row in line with the wall's top row; it stands one row "
                     "proud of the wall's face.")
    B = s.B
    walkway(B, 0, 0, 48, 9)
    parapet(B, 0, 9, 48)
    for x in range(0, 48):
        B.px(x, 15, "s2")
    face(B, 0, 16, 48, 48)
    side(B, 0, 0, 64, left=True)
    # the slit window
    B.rect(22, 26, 4, 14, "sk")
    B.rect(23, 27, 2, 12, "s0")
    B.hline(21, 26, 25, "s5")
    B.hline(21, 26, 40, "s2")
    # a band course under the parapet
    B.hline(0, 47, 17, "s5")
    mirror_x(B, 0, 48, 0, 64)
    return finish(s)


def gateway():
    """An open gate through the wall (the citadel's ramp gate): two jambs and a
    passage two cells wide. The wall top and the lintel are drawn over the
    player, who walks under them; the passage floor is shaded paving."""
    s = struct("gateway", "Ilion's open gate (the ramp gate)", 4, 3,
               walk=["X..X", "X..X", "X..X"],
               notes="Set in the great wall's three rows. The middle two columns are passable: "
                     "the player walks under the wall top and the lintel.")
    B, T = s.B, s.T
    # jambs
    for cx in (0, 3):
        walkway(B, cx * 16, 0, 16, 10)
        parapet(B, cx * 16, 10, 16)
        face(B, cx * 16, 16, 16, 32)
    side(B, 15, 10, 38, left=False)
    # the passage floor: worn flags, darker deep under the wall
    for y in range(0, 48):
        for x in range(16, 48):
            X, Y = x % 16, y % 12
            c = "s2" if y < 30 else "s3"
            if Y == 11 or X == 15:
                c = "s1"
            elif Y == 0 and y >= 30:
                c = "s4"
            if y < 14:
                c = "s1" if (X + Y) % 5 else "s0"
            B.px(x, y, c)
    # the wall top over the passage, and the lintel: on the top layer
    walkway(T, 16, 0, 32, 10)
    parapet(T, 16, 10, 32)
    ashlar(T, 16, 16, 32, 8, ox=0, oy=16, course=8, light="s5", body="s4", joint="s2", shade="s3")
    T.hline(16, 47, 23, "sk")
    T.hline(16, 47, 24, "s1")
    mirror_x(B, 0, 64, 0, 48)
    mirror_x(T, 0, 64, 0, 48)
    return finish(s)


# --------------------------------------------------------------------------
# The Skaian Gate
# --------------------------------------------------------------------------

SHIELD = [
    "..kkkk..",
    ".kgGGgk.",
    "kgGbbGgk",
    "kGbGGbGk",
    "kGbGGbGk",
    "kgGbbGgk",
    ".kgGGgk.",
    "..kkkk..",
]


def skaian_gate():
    """The Skaian Gate's outer face: the great tower over a deep gateway, bronze
    shields hung along it, and its two timber leaves shut and barred. The doors
    are a hall (batch 2): their bottom cells are door metatiles, left impassable
    until the Skaian Gate's hall opens."""
    s = struct("skaian_gate", "The Skaian Gate (outer face)", 4, 4,
               walk=["XXXX", "XXXX", "XXXX", "XXXX"],
               notes="Set in the great wall with its top row one row above the wall's top "
                     "(the gate tower stands taller). The bottom cells of the two leaves, "
                     "(1,3) and (2,3), are MB_NON_ANIMATED_DOOR: impassable now; the hall's "
                     "build opens one and puts its warp there.")
    B = s.B
    # the tower top: a deep crenellated platform the full width
    walkway(B, 0, 0, 64, 8)
    parapet(B, 0, 8, 64)
    # the tower's face, rows 0-1, with the shields
    face(B, 0, 14, 64, 18, foot=False)
    B.hline(0, 63, 14, "s5")
    B.hline(0, 63, 31, "s2")
    for x in (2, 18, 38, 54):
        B.blit(SHIELD, {"k": "sk", "g": "s2", "G": "s4", "b": "s1"}, x, 17)
    # the jambs, rows 2-3
    for cx in (0, 3):
        face(B, cx * 16, 32, 16, 32)
    side(B, 0, 0, 64, left=True)
    # the lintel: one long block over the doors
    for x in range(16, 48):
        for y in range(32, 40):
            B.px(x, y, "s5" if y == 32 else "s4" if y < 37 else "s3")
    B.hline(16, 47, 39, "sk")
    for y in range(32, 64):
        B.px(15, y, "sk")
        B.px(14, y, "s2")
    # the doors (wood group): cols 1-2, rows 2-3 below the lintel, timber leaves
    # banded in bronze and studded, barred across
    for y in range(40, 64):
        for x in range(16, 32):
            X = x - 16
            c = "wd1" if X % 5 else "wd0"
            if X in (1, 2):
                c = "wd2"
            if y in (44, 45, 56, 57):
                c = "br" if y in (44, 56) else "g0"
            if c in ("wd1",) and (x + y) % 9 == 0:
                c = "wd2"
            B.px(x, y, c)
        B.px(16, y, "ink")
    for y in (47, 53, 59):
        for x in range(19, 31, 4):
            B.px(x, y, "g1")
    # the bar: a heavy beam across both leaves
    for x in range(16, 32):
        B.px(x, 49, "ink")
        B.px(x, 50, "wd3")
        B.px(x, 51, "wd2")
        B.px(x, 52, "ink")
    B.hline(16, 31, 63, "ink")
    mirror_x(B, 0, 64, 0, 64)
    # the leaves meet: a dark seam down the middle, the bar crossing it
    B.vline(31, 40, 63, "ink")
    B.vline(32, 40, 63, "wd0")
    s.behaviors[(1, 3)] = "MB_NON_ANIMATED_DOOR"
    s.behaviors[(2, 3)] = "MB_NON_ANIMATED_DOOR"
    return finish(s)


# --------------------------------------------------------------------------
# Hero's tower
# --------------------------------------------------------------------------

def heros_tower():
    """Hero's round tower on Sestos's point: courses of pale stone shaded as a
    drum, a slit window up the stair, a crenellated top, and on it the lamp she
    lights every night for a swimmer, in a bronze brazier. Door at the foot."""
    s = struct("heros_tower", "Hero's tower", 2, 5, walk=["..", "XX", "XX", "XX", "DX"],
               notes="Sestos's landmark, 2 x 5, on the harbor's point. Door at (0,4). Row 0 is "
                     "the lamp, above the tower's top, on grass: drawn over the player, who "
                     "can walk behind it.")
    B = s.B
    # the drum: horizontal courses, lit at left, dark at right
    for y in range(20, 80):
        for x in range(2, 30):
            t = (x - 2) / 27
            c = "s5" if t < 0.18 else "s4" if t < 0.5 else "s3" if t < 0.78 else "s2"
            # courses 8 px tall, tile-aligned, the joints staggered course to
            # course: the drum repeats every 16 px, so its rows share tiles
            if (y % 8) == 7:
                c = {"s5": "s3", "s4": "s2", "s3": "s2", "s2": "s1"}[c]
            elif (x + (y // 8) % 2 * 6) % 12 == 11 and t > 0.1:
                c = "s2" if t < 0.6 else "s1"
            B.px(x, y, c)
        B.px(1, y, "sk")
        B.px(30, y, "sk")
    # the crenellated top, a band wider than the drum
    for y in range(16, 22):
        for x in range(0, 32):
            c = "s5" if y == 17 else "s4" if y < 20 else "s3"
            B.px(x, y, c)
    B.hline(0, 31, 16, "sk")
    B.hline(0, 31, 22, "s1")
    # merlons: notches in the band, the lit tops between
    for x in range(0, 32, 8):
        B.rect(x + 5, 16, 2, 3, "s1")
        B.px(x + 5, 16, "sk")
    # stair slits climbing round the drum
    for (x, y) in ((8, 30), (14, 44), (20, 58)):
        B.rect(x, y, 2, 6, "sk")
    # the door: a dark arched doorway under a lit voussoir, a worn step
    for y in range(66, 79):
        for x in range(5, 13):
            B.px(x, y, "sk" if y < 69 or x in (5, 12) else "s0")
    for x in range(6, 12):
        B.px(x, 65, "sk")
    B.hline(5, 12, 64, "s5")
    B.vline(4, 65, 78, "s5")
    B.vline(13, 65, 78, "s1")
    B.hline(4, 13, 78, "s3")
    # the foot: stones on the rock, a step
    B.hline(0, 31, 79, "sk")
    # the lamp on top (marble group): a bronze brazier on a tripod, the flame
    L = B
    L.rect(10, 9, 12, 3, "br")
    L.hline(10, 21, 9, "g1")
    L.hline(11, 20, 11, "ink")
    for x in (11, 16, 20):
        L.vline(x, 12, 15, "br")
    for (x, y, c) in ((15, 1, "fl"), (16, 0, "fl"), (14, 3, "fl"), (17, 2, "fl"), (13, 5, "fl"),
                      (18, 4, "fl"), (15, 3, "fc"), (16, 2, "fc"), (15, 5, "fc"), (16, 4, "fc"),
                      (14, 6, "fc"), (17, 6, "fc"), (15, 7, "w0"), (16, 6, "w0"), (12, 7, "fl"),
                      (19, 7, "fl"), (13, 8, "fc"), (18, 8, "fc"), (14, 8, "fl"), (17, 8, "fl"),
                      (15, 8, "fc"), (16, 8, "fc"), (16, 7, "fc"), (15, 6, "fc")):
        L.px(x, y, c)
    # row 0 is open sky over grass: the lamp goes on the top layer (the player
    # walks behind it); the drum stands on grass, on the middle layer
    s.T.a[0:16] = B.a[0:16]
    s.M.a[16:] = B.a[16:]
    B.a[:] = 0
    s.set_ground("grass")
    return finish(s)


def build():
    return [wall(), wall_ns(), tower(), gateway(), skaian_gate(), heros_tower()]
