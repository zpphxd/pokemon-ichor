"""Aegina's harbor for gTileset_Aegina.

Two kinds of structure:
  - copies of Akti's harbor pieces, drawn by Akti's own painters so they match
    pixel for pixel: the quay and its edges, the gangplank's foot, the trireme
    Euploia, the kaikia, bollards, rope, amphorae, rocks awash;
  - the round harbor: four rounded corners for the basin and the round mole
    heads that flank its mouth, each with a harbor beacon.

The rounded corners are drawn as a real curved wall seen from the south. The
quay's top edge (its rim) is a quarter circle; the waterline is the same circle
8 px lower, because the wall stands 8 px tall. Where the rim lies above the
waterline (the basin's north side) the wet wall face shows between them; on the
south side the quay's top hides the waterline, as on Akti's straight edges.
Each corner meets Akti's straight quay edges exactly at its sides.
"""
from __future__ import annotations

import math

import akti_art
import akti_coast
import akti_harbor
import kalliste_akti as KA
from aegina_lib import Struct, ground, retitle

SEC = "aegina"


def copies():
    """Akti's harbor pieces, unchanged."""
    out = []
    for s in (akti_art.quay(), akti_art.quay_gangplank(), akti_art.kaiki(),
              akti_art.kaiki(left=True), akti_art.trireme(), akti_harbor.bollard_line(),
              akti_harbor.rope_coil(), akti_harbor.amphora_stack(), akti_coast.sea_rocks()):
        out.append(retitle(s, s.key, s.title))
    return out


# --------------------------------------------------------------------------
# The round basin
# --------------------------------------------------------------------------

R = 32          # the corners' radius: two cells
WALL = 8        # the quay wall's height, as Akti's south edge draws it

# Lip colors by distance from the rim, for each side the water lies on
LIP = {
    "S": ["s4", "s5"],                          # water to the south: the face below
    "N": ["s1", "s5", "s4", "s4", "s2"],        # water to the north: coping
    "E": ["s1", "s4", "s4", "s3", "s2"],        # water to the east: the shaded lip
    "W": ["s1", "s5", "s4", "s4", "s2"],        # water to the west: the lit lip
}


def face_px(L, x, y, j, k):
    """A pixel of the wet wall face: j px below the rim, k px above the waterline."""
    row = j // 4
    off = 8 if row % 2 else 0
    bx, by = (x + off) % 16, j % 4
    wet = k <= 4
    if bx == 15 or by == 3:
        c = "wt0"
    elif by == 0:
        c = "wt1" if wet else "s2"
    else:
        c = "wt1" if wet else "s1"
    if k <= 1 or (k == 2 and x % 3 == 0):
        c = "alg"
    L.px(x, y, c)


def paint_round(s, rim_c, north):
    """Paint a rounded basin corner into a 3 x 3 structure.

    rim_c: the rim circle's center in px. north: True for the basin's north
    corners, where the wall face shows; the waterline circle is then the rim
    circle 8 px lower. Cells that hold any water sit on borrowed sea and draw
    in the middle layer; the rest draw their own bottom. Cells that are all
    water are left out (place aethos sea there)."""
    W, H = s.w * 16, s.h * 16
    cx, cy = rim_c
    wx, wy = cx, cy + WALL

    def kind(x, y):
        dr = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
        if dr >= R:
            return "quay"
        if not north:
            return "water"
        dw = math.hypot(x + 0.5 - wx, y + 0.5 - wy)
        return "water" if dw < R else "face"

    kinds = [[kind(x, y) for x in range(W)] for y in range(H)]
    wet_cells, dry_cells, skip = [], [], set()
    for celly in range(s.h):
        for cellx in range(s.w):
            ks = [kinds[y][x] for y in range(celly * 16, celly * 16 + 16)
                  for x in range(cellx * 16, cellx * 16 + 16)]
            if all(k == "water" for k in ks):
                skip.add((cellx, celly))
            elif any(k == "water" for k in ks):
                wet_cells.append((cellx, celly))
            else:
                dry_cells.append((cellx, celly))
    ground(s, "sea", wet_cells)
    s.skip = skip
    s.walk = ["".join("-" if (x, y) in skip else ("X" if (x, y) in wet_cells else ".")
                      for x in range(s.w)) for y in range(s.h)]

    # the ashlar paving, phase-locked like Akti's quay
    from kalliste_lib import Layer
    pave = Layer(W, H)
    KA.quay(pave, 0, 0, W, H)
    for y in range(H):
        for x in range(W):
            k = kinds[y][x]
            if k == "water":
                continue
            L = s.M if (x // 16, y // 16) in wet_cells else s.B
            if k == "face":
                # j: px below the rim at this column; k: px above the waterline
                top = cy - math.sqrt(max(0.0, R * R - (x + 0.5 - cx) ** 2))
                wl = wy - math.sqrt(max(0.0, R * R - (x + 0.5 - wx) ** 2))
                face_px(L, x, y, int(y - top), int(wl - y))
                continue
            L.px(x, y, pave.get(x, y))
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy) - R
            ux, uy = x + 0.5 - cx, y + 0.5 - cy
            if abs(uy) >= abs(ux):
                side = "S" if uy < 0 else "N"
            else:
                side = "E" if ux < 0 else "W"
            lip = LIP[side]
            if d < len(lip):
                L.px(x, y, lip[int(d)])


def basin_corner(corner):
    """One rounded corner of the round basin, 3 x 3 cells."""
    north = corner in ("nw", "ne")
    rim = {"nw": (48, 48 - WALL), "ne": (0, 48 - WALL), "sw": (48, 0), "se": (0, 0)}[corner]
    names = {"nw": "north-west", "ne": "north-east", "sw": "south-west", "se": "south-east"}
    place = {
        "nw": "its cell (1,1) on the basin's top-left water cell: row 0 continues the north "
              "rim (Akti's quay south edge, the face showing), column 0 the west rim (the "
              "quay's east edge)",
        "ne": "its cell (1,1) on the basin's top-right water cell: row 0 continues the north "
              "rim, column 2 the east rim (the quay's west edge)",
        "sw": "its cell (1,1) on the basin's bottom-left water cell: column 0 continues the "
              "west rim, row 2 the south rim (the quay's north edge, coping only)",
        "se": "its cell (1,1) on the basin's bottom-right water cell: column 2 continues the "
              "east rim, row 2 the south rim",
    }[corner]
    s = Struct(f"basin_{corner}", f"Round basin, {names[corner]} corner", 3, 3, SEC,
               notes=f"The round harbor's {names[corner]} corner: the quay curves round on a "
                     f"two-cell radius, its wet wall face {'showing' if north else 'hidden'} "
                     f"as on Akti's straight {'south' if north else 'north'} edges. Place "
                     f"{place}. Cells with water are solid and sit on aethos's animated sea; "
                     "'-' cells are open water: put aethos sea (0x170) there.")
    paint_round(s, rim, north)
    return s


# --------------------------------------------------------------------------
# The mole heads and their beacons
# --------------------------------------------------------------------------

def beacon(M, x, y):
    """A harbor light: a marble pillar carrying a bronze fire basket, lit."""
    # flame
    M.blit(["   f   ", "  ffc f", " fcyc f", "fcyyycf", " cyyyc ", "  ccc  "],
           {"f": "fl", "c": "g1", "y": "fc"}, x - 3, y)
    # the fire basket: bronze bands
    M.blit(["kGggggbk", " kgggbk ", "  kbbk  "], {"k": "ink", "G": "g1", "g": "g0", "b": "br"},
           x - 4, y + 6)
    # the pillar, lit on the left
    for yy in range(y + 9, y + 23):
        M.px(x - 2, yy, "ink")
        M.px(x - 1, yy, "w0")
        M.px(x, yy, "m2")
        M.px(x + 1, yy, "m4")
        M.px(x + 2, yy, "ink")
    M.blit(["kkkkkkk", "kw1223k", "k12234k", "kkkkkkk"],
           {"k": "ink", "w": "w0", "1": "m1", "2": "m2", "3": "m3", "4": "m4"}, x - 3, y + 21)


def mole_head(facing):
    """The round head of a mole two cells thick, with its beacon.

    facing "w": the mole runs off to the east and its head points west into the
    harbor mouth. "e" is its mirror image (Porytiles stores the flipped tiles
    once). Row 0 is the mole's seaward side (coping), row 1 its basin side, the
    wall face showing above the basin's water."""
    s = Struct(f"mole_head_{facing}", "Mole head with a harbor beacon, pointing "
               + ("west" if facing == "w" else "east"), 2, 2, SEC, walk=["XX", "XX"],
               notes="The rounded end of a mole two cells thick (row 0: open sea to the north, "
                     "the coping; row 1: the basin to the south, its wall face showing), with "
                     "a lit harbor beacon on a marble pillar. Points "
                     + ("west: the mole runs on to the east in Akti's quay pieces (row 0 its "
                        "north edge, row 1 its south edge)." if facing == "w" else
                        "east: the mirror image, the mole running on to the west.")
                     + " All four cells are solid; the walk ends on the mole beside it.")
    W, H = 32, 32
    hx, hy, hr = 16, 12, 12            # the head's round end: rim circle

    def rim(x, y):
        return (x >= 16 and y < 24) or math.hypot(x + 0.5 - hx, y + 0.5 - hy) < hr

    def wl(x, y):
        return (x >= 16 and 8 <= y < 32) or math.hypot(x + 0.5 - hx, y + 0.5 - hy - WALL) < hr

    from kalliste_lib import Layer
    pave = Layer(W, H)
    KA.quay(pave, 0, 0, W, H)
    ground(s, "sea", [(0, 0), (0, 1)])
    for y in range(H):
        for x in range(W):
            L = s.M if x < 16 else s.B
            if rim(x, y):
                L.px(x, y, pave.get(x, y))
                # distance to the rim's edge, and which side the water is on
                if x >= 16 or math.hypot(x + 0.5 - hx, y + 0.5 - hy) < 0.01:
                    d_top, d_bot = y, 23 - y
                    d_round = 99
                else:
                    d_top = d_bot = 99
                    d_round = hr - math.hypot(x + 0.5 - hx, y + 0.5 - hy)
                if x < 16:
                    ux, uy = x + 0.5 - hx, y + 0.5 - hy
                    if abs(uy) > abs(ux) * 1.2:
                        lip = LIP["N"] if uy < 0 else LIP["S"]
                    else:
                        lip = LIP["W"]
                    if d_round < len(lip):
                        L.px(x, y, lip[int(d_round)])
                else:
                    if d_top < 5:
                        L.px(x, y, LIP["N"][d_top])
                    elif d_bot < 2:
                        L.px(x, y, LIP["S"][d_bot])
                    if x % 16 == 7 and 1 <= y <= 4:
                        L.px(x, y, "s1")        # the coping's joints, as Akti's
            elif wl(x, y):
                # the wall face: rows below the rim, down to the waterline
                if x >= 16:
                    j, k = y - 24, 31 - y
                else:
                    half = math.sqrt(max(0.0, hr * hr - (x + 0.5 - hx) ** 2))
                    j, k = int(y - (hy + half)), int(hy + WALL + half - y)
                face_px(L, x, y, max(0, j), max(0, k))
    # the beacon on the head, its shadow on the paving
    for yy in range(17, 24):
        s.B.px(27 + (yy - 17) // 3, yy, "s2")
        s.B.px(28 + (yy - 17) // 3, yy, "s3")
    beacon(s.M, 24, 0)
    if facing == "e":
        for layer in s.layers.values():
            layer.a[:] = layer.a[:, ::-1].copy()
        s.ground = {(1 - x, y): g for (x, y), g in s.ground.items()}
    return s


def later():
    """Pieces added after the first build, appended so earlier ids stay put: Akti's
    kaiki hauled up on the sand, for the beach below the town."""
    s = akti_coast.boat_beached()
    return [retitle(s, s.key, s.title)]


def build():
    return (copies()
            + [basin_corner(c) for c in ("nw", "ne", "sw", "se")]
            + [mole_head("w"), mole_head("e")])
