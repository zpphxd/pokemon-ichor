"""Thyrsa's polish pass (Act II batch 2): the pieces that make the square read as the
heart of the god's city, and Eudora's yard as a household's.

  - fountain: the god's fountain at the square's heart. The bronze god (the statue's
    top cell, reused) stands on a plinth in a marble basin, water from two lion spouts.
  - stall_masks: the mask-seller's stall for the Dionysia, beside the wine stall.
  - litter: the festival's traces on the flags (ivy and a dropped ribbon; petals and a
    grape; a spilled cup), each confined to one or two of its cell's tiles so a scatter
    of them costs little.
  - laundry: Eudora's washing line, the soldier's red cloak and a white chiton.

They are appended at the end of the civic section, so the ids batch 1 laid down stay
where they were. thyrsa_build.py draws, compiles and catalogs them with the rest.
"""
from __future__ import annotations

import math
import random

import emporion_lib as E
import thyrsa_lib as T
from thyrsa_lib import finish, struct

INK = "ink"


def fountain():
    s = struct("fountain", "The god's fountain", 3, 2, walk=["XXX", "XXX"], ground="pave",
               section="civic",
               notes="The fountain at the heart of the square: a marble basin, its water fed by "
                     "two bronze lion heads on the plinth in the middle, where the god in bronze "
                     "stands. Lay the statue's top cell (statue, row 0) in the row above the "
                     "fountain's middle cell: his legs continue on the plinth. Give the basin a "
                     "bg event.")
    L = s.M
    W, H = 48, 32
    # the basin: a rounded rectangle, rim 3 px, water inside
    x0, x1, y0, y1 = 1, W - 2, 6, H - 2

    def inside(x, y, inset):
        xa, xb, ya, yb = x0 + inset, x1 - inset, y0 + inset, y1 - inset
        if not (xa <= x <= xb and ya <= y <= yb):
            return False
        r = 5 - inset if inset < 5 else 0
        for cx, cy in ((xa + r, ya + r), (xb - r, ya + r), (xa + r, yb - r), (xb - r, yb - r)):
            if (x < xa + r or x > xb - r) and (y < ya + r or y > yb - r):
                if (x - cx) ** 2 + (y - cy) ** 2 > r * r + r * 0.6:
                    if abs(x - cx) <= r and abs(y - cy) <= r:
                        return False
        return True

    for y in range(H):
        for x in range(W // 2):
            if not inside(x, y, 0):
                continue
            if not inside(x, y, 1):
                L.px(x, y, INK)
            elif not inside(x, y, 2):
                L.px(x, y, "w0" if y < y1 - 3 else "m2")
            elif not inside(x, y, 3):
                L.px(x, y, "m1" if y < y1 - 4 else "m3")
            elif not inside(x, y, 4):
                L.px(x, y, "m3" if y < 16 else "m4")      # the rim's inner lip, shaded
            else:
                # water: dark under the back rim, ripples further out
                if y < y0 + 6:
                    c = "b0"
                elif (x * 5 + y * 3) % 23 == 0:
                    c = "w0"
                elif (x * 3 + y * 7) % 11 == 0:
                    c = "b2"
                else:
                    c = "b1"
                L.px(x, y, c)
    # the front rim's lit top and its shadow on the flags
    for x in range(x0 + 4, W // 2):
        L.px(x, y1 - 3, "w0")
    E.mirror_half(L, 0, W, 0, H)
    # the plinth in the middle, rising from the water: marble, with two lion spouts
    px0, px1 = 17, 30
    for y in range(3, 17):
        for x in range(px0, px1 + 1):
            c = "m1" if x < px0 + 3 else "m3" if x > px1 - 3 else "m2"
            L.px(x, y, c)
    L.hline(px0, px1, 3, INK)
    L.hline(px0 + 1, px1 - 1, 4, "w0")
    L.hline(px0, px1, 6, "m4")
    L.vline(px0, 3, 16, INK)
    L.vline(px1, 3, 16, INK)
    L.hline(px0 - 1, px1 + 1, 17, INK)
    # its foot in the water: a ring of foam
    for x in range(px0 - 2, px1 + 3):
        L.px(x, 18, "w0" if x % 3 else "b2")
    lion = [" kkk ", "kGgGk", "kgkgk", " kGk ", "  k  "]
    for lx in (px0 + 2, px1 - 6):
        L.blit(lion, {"k": INK, "G": "g1", "g": "g0"}, lx, 8)
        for y in range(13, 22):
            L.px(lx + 2, y, "b2" if y % 2 else "w0")
        L.px(lx + 1, 21, "w0")
        L.px(lx + 3, 21, "w0")
    # the god's legs, continuing the statue's top cell (thyrsa_town.statue)
    leg_rows = [
        "      kbgbk     ",
        "      kb kbk    ",
        "      kb  kbk   ",
        "     kbk  kbk   ",
        "     kkk  kkk   ",
    ]
    # the statue is drawn for a 16 px cell at the god's column (the fountain's middle)
    L.blit([r for r in leg_rows], {"k": INK, "b": "br", "g": "g0"}, 16, 0)
    # a red ribbon round his ankle for the festival (thyrsa's statue sign says so)
    L.px(22, 2, "rd")
    L.px(23, 2, "rd")
    L.px(24, 3, "rd0")
    s.names = {"W": (0, 0), "god": (1, 0), "E": (2, 0), "basin": (1, 1)}
    return finish(s)


def mask_stall():
    s = struct("stall_masks", "Market stall: festival masks", 2, 2, walk=["XX", "XX"],
               ground="pave", section="civic",
               notes="The mask-seller's stall for the Dionysia, under an ivy-green and white "
                     "awning: comic, tragic and satyr masks on pegs and on the counter. "
                     "Free-standing on the flags; the seller stands beside it.")
    import thyrsa_town as TT
    M = s.M
    TT._stall_awning(M, "iv2", "iv1")
    TT._stall_frame(M)
    # masks hung on the awning's posts, and three on the counter
    T.mask(M, 4, 16, "comic", hair=True)
    T.mask(M, 12, 15, "satyr")
    T.mask(M, 20, 16, "tragic", hair=True)
    # ribbons trailing off the counter's front
    for x, c in ((6, "rd"), (14, "vp1"), (24, "rd")):
        M.vline(x, 30, 31, c)
    return finish(s)


def litter():
    s = struct("litter", "The festival's traces on the flags", 3, 1, walk=["..."],
               ground="pave", section="civic",
               notes="What the god's festival leaves on the street, one cell each, all walkable: "
                     "(0) a trampled ivy wreath with its red ribbon, (1) a comic mask somebody "
                     "dropped, (2) a spilled cup in a puddle of wine. Scatter them thinly along "
                     "the procession's way and round the stalls; each fills one or two of its "
                     "cell's tiles, the rest is plain flags.")
    M = s.M
    key = {"1": "iv1", "2": "iv2", "3": "iv3", "r": "rd", "d": "rd0", "k": INK}
    # (0) an ivy wreath, trampled flat, its ribbon trailing: the cell's lower half
    M.blit([
        "   1221      ",
        "  23   12    ",
        " 12     32   ",
        " 21      1   ",
        "  12   rr2   ",
        "   r1221 rd  ",
        "  rd      rr ",
        " rd        d ",
    ], key, 1, 8)
    # (1) a comic mask, face up, a little askew: the lower right tile
    T.mask(M, 24, 8, "comic")
    M.px(31, 9, "rd")
    M.px(31, 10, "rd0")
    # (2) a spilled cup in its wine: the upper half
    stain = [(x, y) for y in range(1, 8) for x in range(33, 47)
             if ((x - 40) / 6.2) ** 2 + ((y - 4.5) / 3.2) ** 2 < 1]
    for (x, y) in stain:
        M.px(x, y, "vp1" if (x * 3 + y) % 5 else "vp2")
    for (x, y) in stain:
        if ((x - 40) / 6.2) ** 2 + ((y - 4.5) / 3.2) ** 2 > 0.6:
            M.px(x, y, "vp0")
    M.blit(["kkkkk  ", "kwwwwkk", " kwwwk ", "  kkk  "], {"k": INK, "w": "wd2"}, 34, 2)
    s.names = {"ivy": (0, 0), "mask": (1, 0), "cup": (2, 0)}
    return finish(s)


def laundry():
    s = struct("laundry", "A washing line", 2, 1, walk=["XX"], ground="pave", section="civic",
               notes="Eudora's washing line across her yard: two posts, a soldier's red cloak, "
                     "half-mended, and a white chiton. On the flags of a courtyard. Drawn low "
                     "in the cell, so most of it is the line's posts over the flags.")
    M = s.M
    # the posts, mirror images, and the line sagging between them at y 7-9
    for x in (2, 28):
        M.vline(x, 1, 15, "wd0")
        M.vline(x + 1, 1, 15, "wd1")
        M.hline(x, x + 1, 0, INK)
    for x in range(4, 28):
        sag = int(round(1.5 * math.sin(math.pi * (x - 4) / 24)))
        M.px(x, 8 + sag, "wd2")
    # the cloak: red wool, darned, its hem dark (the lower tiles)
    for y in range(9, 16):
        for x in range(5, 14):
            M.px(x, y, "rd" if (x + 2 * y) % 9 else "rd0")
    M.hline(5, 13, 9, INK)
    M.vline(5, 9, 15, INK)
    M.vline(13, 9, 15, INK)
    M.hline(6, 12, 15, "rd0")
    for (x, y) in ((8, 12), (9, 13), (10, 12)):     # a darn
        M.px(x, y, "wd2")
    # the chiton: white linen
    for y in range(10, 16):
        for x in range(18, 26):
            M.px(x, y, "w0")
    M.hline(18, 25, 10, INK)
    M.vline(18, 10, 15, INK)
    M.vline(25, 10, 15, INK)
    M.vline(21, 11, 15, "wd2")
    return finish(s)


def bench():
    s = struct("bench", "A stone bench", 2, 1, walk=["XX"], ground="pave", section="civic",
               notes="A long bench of the city's grey stone on two blocky feet, worn smooth: "
                     "(0) west half, (1) east half. Under the square's trees.")
    M = s.M
    W = 32
    M.rect(1, 6, W - 2, 4, "cg4")
    M.hline(1, W - 2, 6, "cg5")
    M.hline(0, W - 1, 5, INK)
    M.hline(0, W - 1, 10, INK)
    M.vline(0, 5, 10, INK)
    M.vline(W - 1, 5, 10, INK)
    for fx in (3, W - 8):
        M.rect(fx, 11, 5, 4, "cg2")
        M.vline(fx, 11, 14, INK)
        M.vline(fx + 4, 11, 14, INK)
        M.hline(fx, fx + 4, 15, INK)
    M.hline(2, W - 3, 9, "cg3")
    s.names = {"W": (0, 0), "E": (1, 0)}
    return finish(s)


def court_extras():
    """Eudora's yard wall, made a household's: a barred gate in its front, and the fig's
    ivy over its coping. The wall's own stucco and tiles (thyrsa_town.court_wall), so only
    the gate and the ivy cost tiles."""
    import thyrsa_town as TT
    s = struct("court_extras", "A courtyard wall: gate and ivy", 2, 1, walk=["XX"], ground="none",
               section="civic",
               notes="Drop-ins for court_wall's run: (0) the yard's gate, a plank door under a "
                     "little tiled lintel, barred from inside; (1) the wall with ivy spilling over "
                     "its coping from the yard.")
    base = TT.court_wall()
    L = s.B
    # both cells start as the wall's run cell
    for i in range(2):
        L.a[0:16, i * 16:i * 16 + 16] = base.B.a[0:16, 16:32]
    # (0) the gate: planks in wine-purple paint, iron straps, a lintel of tiles
    L.rect(3, 4, 10, 11, "wn1")
    for x in (5, 8, 11):
        L.vline(x, 5, 14, "wn0")
    L.hline(3, 12, 7, "ink")
    L.hline(3, 12, 12, "ink")
    L.vline(2, 3, 15, "ink")
    L.vline(13, 3, 15, "ink")
    L.hline(1, 14, 2, "tc3")
    L.hline(1, 14, 3, "tc1")
    L.px(9, 10, "oc3")          # the latch
    # (1) ivy over the coping
    M = s.M
    for x in range(17, 31):
        h = 3 + (x * 5) % 4 + (2 if x in (20, 21, 26) else 0)
        for y in range(0, h):
            M.px(x, y, "iv2" if (x + y) % 3 else "iv1")
    for (x, y) in ((19, 6), (22, 5), (27, 7), (24, 4)):
        M.px(x, y, "iv1")
    s.names = {"gate": (0, 0), "ivy": (1, 0)}
    return finish(s)


def build():
    return [fountain(), mask_stall(), litter(), laundry(), court_extras()]
