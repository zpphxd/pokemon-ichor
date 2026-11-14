"""Akti Town's harbor art for gTileset_Akti.

Two kinds of structure live here:
  - copies of the kalliste pieces Akti uses (the temple facade, Glaukos's house,
    Poseidon's shrine, the altar, the quay, walls and terraces, the kaiki),
    redrawn by kalliste's own painters so they match Elaia pixel for pixel, with
    a few Akti changes (the temple's roof, the boats on live sea);
  - new harbor art: the trireme Euploia, the fish stall, a limestone coast,
    the beach, the krene, the plaza paving, harbor life and the gardens.

Every structure is a kalliste_lib Struct; akti_lib.ground() puts cells on aethos
grass, sand or sea. See akti_build.py for packing and TILES_akti.md for the catalog.
"""
from __future__ import annotations

import math

from akti_lib import Struct, ground
import kalliste_akti as KA
import kalliste_elaia as KE

SEC = "akti"


def retitle(s, key, title, notes=None, walk=None):
    s.key, s.title, s.section = key, title, SEC
    if notes is not None:
        s.notes = notes
    if walk is not None:
        s.walk = walk
    return s


def aethos_ground_pixels(L, cx, cy, mid=0x001):
    """Copy an aethos ground metatile's pixels into a layer cell, by color name,
    so a drawn bottom (with shadows) meets aethos's own ground seamlessly."""
    from akti_lib import aethos_metatile
    import kalliste_lib as K
    t = aethos_metatile(mid)
    for y in range(16):
        for x in range(16):
            L.px(cx * 16 + x, cy * 16 + y, K.RGB2NAME[tuple(int(v) for v in t[y, x])])


def shade(L, pts, c):
    for (x, y) in pts:
        L.px(x, y, c)


# ==========================================================================
# Copies from kalliste
# ==========================================================================

def temple():
    """Kalliste's temple facade with the roof redrawn: the slopes either side of
    the pediment now read as two planes of tiles falling away from a lit ridge,
    instead of a flat red slab."""
    s = retitle(KA.temple_hestia(), "temple_hestia", "Temple of Hestia, exterior")
    L = s.B
    W = 112
    cx = 55.5

    def ytop(x):
        return int(round(31 - 21 * (1 - abs(x - cx) / cx)))
    # Each slope is drawn in zones a tile (8 px) wide: lit near the ridge, darker
    # toward the eaves, and the left (sunward) slope brighter than the right.
    # Inside a zone the pattern repeats every 4 px, so whole tiles repeat.
    ZONES = {True: [("tc2", "tc2", "tc1"), ("tc2", "tc1", "tc1")],     # the sunward slope
             False: [("tc2", "tc1", "tc0"), ("tc1", "tc1", "tc0")]}    # the shaded slope
    for x in range(1, W - 1):
        t = ytop(x)
        lit = x < 56
        zone = (55 - x) // 8 if lit else (x - 56) // 8      # 0 at the ridge
        hi, body, lo = ZONES[lit][0 if zone < 2 else 1]
        col = x % 4 if lit else (3 - x % 4)
        for y in range(1, t):
            c = hi if col == 0 else (lo if col == 3 else body)
            if y % 4 == 3:
                c = lo
            L.px(x, y, c)
    # the ridge: a row of pale ridge tiles with antefix bumps, catching the sun
    for y in range(1, 11):
        L.px(54, y, "tc2")
        L.px(55, y, "tc2" if y % 3 else "fc")
        L.px(56, y, "tc1")
        L.px(57, y, "tc0")
    # the back edge of the roof and its eaves: a dark line with antefix dots
    L.hline(1, W - 2, 0, "ink")
    for x in range(3, W - 3, 8):
        L.px(x, 1, "tc0")
    L.vline(0, 0, 31, "ink")
    L.vline(W - 1, 0, 31, "ink")
    # the apex tripod and flame again, over the new tiles
    L.blit(KA.TRIPOD, KA.TRIPOD_KEY, 50, 6)
    L.blit(KA.FLAME, KA.FLAME_KEY, 51, 0)
    s.notes = ("A tetrastyle Doric front in marble: a terracotta roof falling away either side "
               "of a lit ridge, a pediment with a relief hearth and a bronze fire-tripod on the "
               "apex, a triglyph frieze, bronze doors between two lit braziers, and three steps. "
               "Door: row 4, middle column (MB_NON_ANIMATED_DOOR). The step row is walkable.")
    return s


def house():
    return retitle(KE.house_small(), "house_small", "Small Cycladic house")


def house_shuttered():
    """The small house with no door on its front: a blue-shuttered window and a
    whitewashed bench take the door's place, so it can stand anywhere."""
    s = KE.house_small()
    s = retitle(s, "house_shuttered", "Small Cycladic house, shuttered front",
                walk=["XXXX", "XXXX", "XXXX"],
                notes="The small house with its door bricked up as a shuttered window over a "
                      "whitewashed bench, so a scenery house needs no barred door. All solid.")
    s.behaviors = {}
    L = s.B
    # whitewash over the door and its step
    L.rect(16, 25, 15, 23, "w1")
    L.hline(1, 62, 45, "w2")
    L.hline(1, 62, 46, "w3")
    L.hline(0, 63, 47, "w4")
    # shuttered window, closed: two blue leaves with louvres
    win = [
        "kkkkkkkkkk",
        "kHMMMkHMMk",
        "kMDDDkMDDk",
        "kHMMMkHMMk",
        "kMDDDkMDDk",
        "kHMMMkHMMk",
        "kMDDDkMDDk",
        "kkkkkkkkkk",
        "w33333333w",
    ]
    L.blit(win, {"k": "ink", "H": "b2", "M": "b1", "D": "b0", "w": "w0", "3": "w3"}, 18, 23)
    # a whitewashed bench below it, with its shadow
    L.rect(15, 38, 18, 3, "w0")
    L.hline(15, 32, 41, "w2")
    L.vline(16, 41, 43, "w3")
    L.vline(31, 41, 43, "w3")
    L.hline(15, 32, 37, "dk")
    return s


def shrine():
    return retitle(KA.poseidon_shrine(), "shrine_poseidon", "Harbor shrine to Poseidon")


def quay():
    return retitle(KA.harbor_quay(), "quay", "Harbor quay: ashlar paving, edges and corners")


def kaiki(left=False):
    s = KA.kaiki_mirrored() if left else KA.kaiki()
    s = retitle(s, "boat_kaiki_left" if left else "boat_kaiki",
                "Moored kaiki, bow to the left" if left else "Moored kaiki with painted eyes",
                notes="A fishing kaiki on live sea: the water under it is aethos's animated "
                      "sea. Bow to the " + ("left." if left else "right."))
    ground(s, "sea")
    return s


def altar():
    """Elaia's marble altar with its fire lit, standing on Akti's warm paving."""
    s = KE.altar()
    s = retitle(s, "altar", "Altar of Hestia before the temple",
                notes="Elaia's marble altar and fire-bowl, on the plaza's warm paving. "
                      "The temple's sign is cut on it.")
    paint_paving(s.B, 0, 0, 32, 32, marble=False)
    return s


def terraces():
    return _row(KE.terraces(), "terrace", "Terrace retaining wall and steps", 0,
                "A retaining wall for terraced ground, lower ground to the south: west end, "
                "two middles to alternate, steps up through the wall, east end.", ["XXX.X"])


def _row(src, key, title, cy, notes, walk):
    """One row of a kalliste structure as its own structure."""
    s = Struct(key, title, src.w, 1, SEC, walk=walk, notes=notes)
    for ln in ("bottom", "middle", "top"):
        s.layers[ln].a[:] = src.layers[ln].a[cy * 16:cy * 16 + 16]
    return s


def quay_steps():
    """Kalliste's steps cut down into the water, on the quay's north edge."""
    s = Struct("quay_steps", "Harbor steps down to the water", 1, 1, SEC, walk=["."],
               notes="Steps cut down into the water from the quay's north edge (water to the "
                     "north). Put the surf start beside them.")
    s.B.a[:] = KA.harbor_steps().B.a[:, 0:16]
    return s


# ==========================================================================
# The plaza's warm paving
# ==========================================================================

MARBLE_SLABS = {(0, 0)}   # (slab column % 2, slab row % 2) laid in marble
PALE_SLABS = {(1, 1)}     # and in a paler limestone


def paint_paving(L, x0, y0, w, h, seed=0, marble=True, ox=0, oy=0):
    """Warm limestone flags in a 16 px running bond, in cream lime joints, with
    pale marble flags laid among them on a 32 px repeat. (ox, oy) is where this
    box sits on the plaza, so the four interior variants join into one floor;
    marble=False lays limestone only, the same in every cell (for the edges)."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            X, Y = x + ox, y + oy
            row = Y // 8
            off = 8 if row % 2 else 0
            bx, by = (X + off) % 16, Y % 8
            sx = ((X + off) // 16) % 2
            is_marble = marble and (sx, row % 2) in MARBLE_SLABS
            is_pale = marble and (sx, row % 2) in PALE_SLABS
            if bx == 15 or by == 7:
                c = "pv0"
            elif by == 0 or bx == 0:
                c = "w0" if is_marble else "pv2"
            else:
                c = "pv2" if (is_marble or (is_pale and (bx + by) % 2)) else "pv1"
                if is_marble and (bx + by) % 7 == 3:
                    c = "m2"
                elif not is_marble and (bx * 3 + by * 5 + sx) % 11 == 0:
                    c = "pv0"
            L.px(x, y, c)


PLAZA_VARIANTS = {(0, 0): (3, 0), (1, 0): (4, 0), (0, 1): (3, 1), (1, 1): (4, 1)}


def paving():
    s = Struct("plaza", "Plaza paving: warm limestone and marble flags", 5, 3, SEC,
               walk=[".....", ".....", "....."],
               notes="Warm limestone flags in a running bond, with pale marble ones laid "
                     "among them on a two-cell repeat. Columns 0-2 are the kerbed border: "
                     "NW, N, NE / W, plain, E / SW, S, SE, the kerb terracotta, showing its "
                     "face on the south edge. Columns 3-4, rows 0-1, are the four interior "
                     "cells: lay the one at (3 + x % 2, y % 2) for map cell (x, y) and the "
                     "marble flags fall into place. (3, 2) and (4, 2) are plain limestone.")
    L = s.B
    paint_paving(L, 0, 0, 48, 48, marble=False)
    for (cx, cy) in PLAZA_VARIANTS.values():
        paint_paving(L, cx * 16, cy * 16, 16, 16, ox=-cx * 16 + (cx - 3) * 16,
                     oy=-cy * 16 + cy * 16)
    paint_paving(L, 48, 32, 32, 16, marble=False)
    # kerbs: terracotta coping with a lit top and a shaded face
    def kerb_top(x0, x1, y):
        L.hline(x0, x1, y, "tc2")
        L.hline(x0, x1, y + 1, "tc1")
        L.hline(x0, x1, y + 2, "pv0")
    def kerb_left(x, y0, y1):
        L.vline(x, y0, y1, "tc2")
        L.vline(x + 1, y0, y1, "tc1")
        L.vline(x + 2, y0, y1, "pv0")
    def kerb_right(x, y0, y1):
        L.vline(x, y0, y1, "tc1")
        L.vline(x - 1, y0, y1, "tc2")
        L.vline(x - 2, y0, y1, "pv0")
    def kerb_bottom(x0, x1, y):
        L.hline(x0, x1, y - 3, "pv0")
        L.hline(x0, x1, y - 2, "tc2")
        L.hline(x0, x1, y - 1, "tc1")
        L.hline(x0, x1, y, "m4")
    # row 0
    kerb_top(0, 47, 0)
    kerb_left(0, 0, 15)
    kerb_right(47, 0, 15)
    # row 1
    kerb_left(0, 16, 31)
    kerb_right(47, 16, 31)
    # row 2
    kerb_bottom(0, 47, 47)
    kerb_left(0, 32, 46)
    kerb_right(47, 32, 46)
    for (x, y) in ((0, 0), (47, 0), (0, 47), (47, 47)):
        L.px(x, y, "m4")
    return s


# ==========================================================================
# The trireme Euploia
# ==========================================================================

def trireme():
    """A trireme moored bow to the right, 8 x 3 cells on live sea.

    Long black hull with a red wale; the oarbox along her side with a bank of
    oars at rest, blades in the water; the bronze ram and the painted eye at the
    bow; a curling aphlaston at the stern with a steering oar; one mast amidships
    with its square sail furled on the yard, stays to bow and stern, and a row of
    bronze shields along the rail. A gangplank runs from her side down to the
    quay below (the quay_gangplank piece meets it)."""
    s = Struct("trireme", "The trireme Euploia", 8, 3, SEC,
               walk=["XXXXXXXX", "XXXXXXXX", "XXXXXXXX"],
               notes="The Euploia moored bow to the right on aethos's animated sea. Place her "
                     "with her bottom row on the water row just north of the quay, so the "
                     "gangplank (bottom row, column 3) lands on quay_gangplank below it.")
    ground(s, "sea")
    M = s.M
    WL = 38          # waterline

    # --- hull silhouette: keel at the waterline, sheer curving up at both ends
    def sheer(x):
        """Top of the hull side (the gunwale) at x."""
        if x < 14:
            return 22 - int((14 - x) * 0.9)
        if x > 104:
            return 22 - int((x - 104) * 0.5)
        return 22
    def keel(x):
        if x < 10:
            return WL - 2 + (10 - x) // 4
        return WL
    stern, bow = 6, 112
    # water shadow under the hull and foam where the hull meets the sea
    for x in range(stern + 2, bow + 4):
        M.px(x, WL + 1, "b0")
        M.px(x, WL + 2, "b0" if x % 2 else "b1")
        if x % 8 == 3:
            M.px(x, WL + 3, "b0")
    for x in range(stern, bow + 2):
        if x % 4:
            M.px(x, WL, "w0" if x % 8 != 5 else "b2")
    # hull side
    for x in range(stern, bow + 1):
        top, bot = sheer(x), keel(x) - 1
        for y in range(top, bot + 1):
            c = "wd0"
            if y >= bot - 1:
                c = "ink"
            elif y == top + 9:
                c = "rd"                          # the red wale
            elif y == top + 10:
                c = "tc1"
            elif y == top:
                c = "wd1"
            M.px(x, y, c)
        M.px(x, top - 1, "ink")
    M.vline(stern - 1, sheer(stern), keel(stern), "ink")
    # planks: faint seams along the hull
    for x in range(stern + 4, bow - 6):
        if (x // 8) % 2 == 0:
            M.px(x, 34, "wd1")
    # --- the oarbox (parexeiresia) overhanging the side, with oar ports
    for x in range(18, 100):
        M.px(x, 25, "wd2")
        M.px(x, 26, "wd3")
        M.px(x, 27, "wd1")
        M.px(x, 28, "ink")
        if x % 8 == 4:
            M.px(x, 27, "ink")
    M.vline(17, 25, 28, "ink")
    M.vline(100, 25, 28, "ink")
    # oars at rest: shafts from the ports angled down aft, blades in the water
    for i, x0 in enumerate(range(20, 100, 8)):
        x, y = x0, 28
        while y < WL + 3:
            M.px(x, y, "wd3" if y < 33 else "wd2")
            y += 1
            if y % 2 == 0:
                x -= 1
        # the blade, and the ripple it makes
        M.px(x, WL + 2, "wd3")
        M.px(x - 1, WL + 2, "wd2")
        M.px(x - 1, WL + 3, "wd2")
        M.px(x - 2, WL + 4, "w0")
        M.px(x + 1, WL + 4, "b2")
        M.px(x - 3, WL + 4, "b2")
    # --- deck seen from above, the rail and its shields
    for x in range(14, 106):
        for y in range(17, 22):
            M.px(x, y, "wd3" if y % 3 else "wd2")
        M.px(x, 16, "ink")
        M.px(x, 22, "wd1")
    for x in range(16, 104, 16):        # deck seams across the planking
        M.vline(x, 17, 21, "wd2")
    for x0 in range(22, 100, 16):        # bronze shields hung along the rail
        M.blit([" kk ", "kGgk", "kgbk", " kk "], {"k": "ink", "G": "g1", "g": "g0", "b": "br"},
               x0, 20)
    # --- the bow: the stem post, the eye and the bronze ram
    for y in range(12, 24):
        x = 104 + (24 - y) // 2
        M.px(x, y, "wd1")
        M.px(x + 1, y, "ink")
    M.blit([" kkk ", "kwwbk", "kwbbw", " kkkk"], {"k": "ink", "w": "w0", "b": "b0"}, 99, 29)
    M.px(98, 30, "rd")
    M.px(104, 31, "rd")
    ram = [
        "k            ",
        "kGGGGGGgk    ",
        "kgggggggGGk  ",
        "kbbbbbbbggGGk",
        "kgggggggGGk  ",
        "kbbbbbbbbk   ",
        "kkkkkkkkk    ",
    ]
    M.blit(ram, {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 112, WL - 5)
    # the proembolion: a small bronze boar's head above the ram
    M.blit(["kGk", "kgb", " kk"], {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 109, 27)
    # --- the stern: the aphlaston, a fan of timbers rising from the stern and
    # curling forward over the steersman, each tip gilded
    for k in range(6):
        for t in range(0, 48):
            u = t / 47
            # each timber leaves the stern post and sweeps up, then forward
            x = 4 + k * 1.6 + 7 * u + 3 * math.sin(u * math.pi)
            y = 24 - 20 * math.sin(u * math.pi * 0.62) - k * 0.7
            xi, yi = int(round(x)), int(round(y))
            if yi >= 1:
                M.px(xi, yi, ["wd2", "wd1", "wd2", "wd1", "wd2", "wd0"][k])
        tip_x = int(round(4 + k * 1.6 + 7 + 3 * math.sin(math.pi)))
        tip_y = int(round(24 - 20 * math.sin(math.pi * 0.62) - k * 0.7))
        M.px(tip_x + 1, tip_y, "g1")
        M.px(tip_x + 1, tip_y + 1, "g0")
    M.vline(3, 8, 24, "ink")
    M.vline(15, 12, 22, "ink")
    # steering oar angled down past the stern quarter
    for k in range(18):
        x, y = 16 - k // 3, 24 + k
        M.px(x, y, "wd2")
        M.px(x + 1, y, "wd1")
    M.rect(9, WL + 1, 3, 4, "wd3")
    M.px(8, WL + 4, "w0")
    # --- the mast, the yard and the furled sail, with stays fore and aft
    MX = 62
    M.line(MX + 2, 2, 104, 12, "rp")          # forestay to the bow
    M.vline(MX - 1, 0, 21, "ink")
    M.vline(MX, 0, 21, "wd2")
    M.vline(MX + 1, 0, 21, "wd1")
    M.vline(MX + 2, 0, 21, "ink")
    M.rect(MX - 1, 0, 4, 2, "wd0")            # the masthead block
    for x in range(34, 92):                   # the yard
        M.px(x, 4, "ink")
        M.px(x, 5, "wd2")
        M.px(x, 6, "wd1")
    for x in range(35, 91):                   # the square sail, furled in a fat roll
        sag = 0
        M.px(x, 7, "rp")
        M.px(x, 8 + sag // 2, "w0")
        M.px(x, 9 + sag // 2, "w0" if (x // 4) % 2 else "rp")
        M.px(x, 10 + sag, "rp")
        M.px(x, 11 + sag, "wd3")
        M.px(x, 12 + sag, "ink")
        if x % 8 == 0:                        # gaskets lashing it to the yard
            M.vline(x, 7, 11 + sag, "wd1")
    M.px(34, 7, "ink")
    M.px(91, 7, "ink")
    for x in range(40, 90, 16):               # brails hanging from the furled sail
        M.vline(x, 13, 16, "rp")
    # a pennant on the masthead: a red ribbon, hanging perfectly still
    M.vline(MX + 3, 0, 4, "rd")
    M.px(MX + 3, 5, "rd")
    # --- the gangplank, from her side down to the quay (column 3, bottom row)
    for y in range(29, 48):
        M.px(52, y, "ink")
        M.px(53, y, "wd3")
        M.px(54, y, "wd2")
        M.px(55, y, "wd3")
        M.px(56, y, "ink")
        if y % 4 == 1:
            M.hline(53, 55, y, "wd1")         # cleats
    return s


def quay_gangplank():
    """Quay coping (water to the north) with the foot of the trireme's gangplank."""
    s = Struct("quay_gangplank", "Quay edge with the gangplank's foot", 1, 1, SEC,
               walk=["."],
               notes="The quay's north edge with the trireme's gangplank resting on it. "
                     "Place it directly below the trireme's bottom row, column 3.")
    B, M = s.B, s.M
    KA.quay(B, 0, 0, 16, 16)
    KA.coping_n(B, 0, 0, 16)
    for y in range(0, 11):
        M.px(4, y, "ink")
        M.px(5, y, "wd3")
        M.px(6, y, "wd2")
        M.px(7, y, "wd3")
        M.px(8, y, "ink")
        if y % 4 == 1:
            M.hline(5, 7, y, "wd1")
    M.hline(4, 8, 11, "ink")
    M.hline(4, 8, 12, "wd0")
    return s


def build():
    import akti_coast
    import akti_harbor
    import akti_town
    return ([temple(), house(), house_shuttered(), shrine(), altar(), paving(), quay(),
             quay_steps(), quay_gangplank(), kaiki(), kaiki(left=True), trireme(),
             terraces()]
            + akti_harbor.build() + akti_coast.build() + akti_town.build())
