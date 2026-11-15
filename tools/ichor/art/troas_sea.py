"""The Hellespont and Sestos's harbor for gTileset_Troas.

  - The current: four pieces of fast water on aethos's animated sea, streaked
    with foam running east, each MB_EASTWARD_CURRENT (OIKOUMENE.md §4.1: "a strong
    current runs east; surf across it diagonally").
  - Helle's rock: the crag in mid-strait where Phrixos's sister fell from the
    golden ram, a little gilded ram set up on it by sailors.
  - A timber landing stage: the north shore's landing for Abdera, and the ferry's.
  - Akti's harbor, drawn by Akti's own painters (troas_lib.from_akti): the quay
    and its edges, the trireme Euploia with her gangplank's foot, a bollard.
"""
from __future__ import annotations

import random

import numpy as np

import akti_art
import akti_coast
import akti_harbor
from troas_lib import finish, from_akti, struct

GILD = {"s5": "w0", "s4": "m1", "s3": "m2", "s2": "m3", "s1": "m4", "s0": "m5", "sk": "ink",
        "wt0": "m5", "wt1": "m4", "alg": "m4", "ol1": "m4", "e1": "tc1", "e2": "tc2", "b3": "w0"}


def regroup(L, x0, y0, w, h, mapping):
    """Recolor every pixel in a box by name, so its tiles fall in another group."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            c = L.get(x, y)
            if c in mapping:
                L.px(x, y, mapping[c])


# --------------------------------------------------------------------------
# The current
# --------------------------------------------------------------------------

def current():
    """Fast water: foam streaks lean east, each a bright head trailing a pale
    tail to the west, broken into dashes so the sea shows through."""
    s = struct("current", "The Hellespont's current (eastward)", 4, 1, walk=["...."],
               notes="Surfable fast water: MB_EASTWARD_CURRENT carries a surfer east until "
                     "they leave it. Four variants; scatter them so the streaks never line "
                     "up. Elevation 1, like the sea. Not in a seam's aethos-only strip.",
               ground="sea")
    M = s.M
    rng = random.Random(41)
    for v in range(4):
        ox = v * 16
        rows = [(1 + v) % 4 + 1, 6 + (v * 3) % 3, 11 + (v + 1) % 3]
        for i, y in enumerate(rows):
            x0 = (v * 5 + i * 7) % 16
            length = 7 + (v + i) % 4
            for k in range(length):
                x = ox + (x0 + k) % 16
                if k == length - 1:
                    c = "w0"
                elif k >= length - 3:
                    c = "w0" if (k + i) % 2 == 0 else "b3"
                else:
                    c = "b3" if k % 3 != 2 else None
                if c:
                    M.px(x, y, c)
            # a chevron of spray at the head
            hx = ox + (x0 + length) % 16
            if rng.random() < 0.7:
                M.px(hx, y - 1, "b3")
                M.px(hx, y + 1, "b3")
        s.behaviors[(v, 0)] = "MB_EASTWARD_CURRENT"
    s.names = {f"v{v}": (v, 0) for v in range(4)}
    return finish(s)


# --------------------------------------------------------------------------
# Helle's rock
# --------------------------------------------------------------------------

RAM = [
    "..gg.....",
    ".gGGg....",
    "gGkGGggg.",
    ".gGGGGGGg",
    "..gGGGGGg",
    "..b..b.b.",
    "..b..b.b.",
]


def helle_rock():
    """A dark crag splitting the current, foam all round. On its top sailors have
    set a little gilded ram on a marble block, for Helle."""
    s = struct("helle_rock", "Helle's rock", 3, 2, walk=["XXX", "XXX"],
               notes="The Hellespont's set piece, mid-strait in the current. Read from a "
                     "neighbouring cell (a bg event on the rock).", ground="sea")
    M = s.M
    akti_coast.crag(M, [(4, 10), (12, 4), (22, 2), (33, 5), (43, 9), (44, 16), (36, 20),
                        (18, 21), (7, 18)], face=8, seed=21, shrub=1)
    akti_coast.crag(M, [(37, 21), (42, 20), (46, 23), (43, 26), (38, 26)], face=3, seed=22)
    akti_coast.crag(M, [(1, 22), (5, 21), (8, 24), (4, 26)], face=2, seed=23)
    # the votive: a gilded ram on a marble block, its tiles recoloured to marble
    regroup(M, 16, 0, 16, 16, GILD)
    M.rect(20, 9, 8, 4, "m1")
    M.hline(20, 27, 9, "w0")
    M.hline(20, 27, 12, "m4")
    M.vline(20, 9, 12, "ink")
    M.vline(27, 9, 12, "ink")
    M.blit(RAM, {"g": "g0", "G": "g1", "k": "ink", "b": "br"}, 19, 2)
    return finish(s)


# --------------------------------------------------------------------------
# The landing stage
# --------------------------------------------------------------------------

def planks(L, x0, y0, h):
    """A deck of boards running east-west, 12 px wide, over the water."""
    for y in range(y0, y0 + h):
        for x in range(x0 + 2, x0 + 14):
            Y = y % 4
            c = "wd2" if Y in (1, 2) else "wd3" if Y == 0 else "wd1"
            if x % 8 == 5 and Y == 2:
                c = "wd1"                       # a nail head in every board
            L.px(x, y, c)
        L.px(x0 + 2, y, "ink")
        L.px(x0 + 13, y, "ink")


def landing():
    """A timber landing stage running out north to south: its root on the shore,
    a run over the water, and the end with a mooring post, where boats tie up."""
    s = struct("landing", "Timber landing stage", 3, 1, walk=["...", ],
               notes="Cell 0: the root, on sand (place at the shore). Cell 1: the run, on "
                     "the sea, repeat it. Cell 2: the end on the sea, with a mooring post: "
                     "the landing tile, where a boat ties up. All walkable; a surfer can land "
                     "on any of them.", ground="sea")
    s.set_ground("sand", [(0, 0)])
    M = s.M
    for cx in range(3):
        planks(M, cx * 16, 0, 16 if cx < 2 else 13)
    # piles beside the run and the end, wet at the foot
    for cx in (1, 2):
        for px in (cx * 16, cx * 16 + 14):
            M.rect(px, 3, 2, 12, "wd1")
            M.vline(px, 3, 14, "ink")
            M.hline(px, px + 1, 14, "b2")
    M.hline(34, 45, 13, "ink")
    M.hline(34, 45, 14, "wd0")
    # the mooring post and a coil of line on the end
    M.rect(39, 3, 3, 6, "wd1")
    M.hline(39, 41, 3, "wd3")
    M.vline(38, 3, 8, "ink")
    M.vline(42, 3, 8, "ink")
    M.blit([".rr.", "r..r", ".rr."], {"r": "rp"}, 35, 9)
    # the root: the planks meet the sand on a log sill
    M.hline(2, 13, 0, "wd0")
    M.hline(2, 13, 1, "wd1")
    s.names = {"root": (0, 0), "run": (1, 0), "end": (2, 0)}
    return finish(s)


# --------------------------------------------------------------------------
# Akti's harbor pieces, drawn by Akti's painters
# --------------------------------------------------------------------------

def harbor():
    quay = from_akti(akti_art.quay())
    quay.names = {"NW": (0, 0), "N": (1, 0), "NE": (2, 0), "inNW": (3, 0), "inNE": (4, 0),
                  "W": (0, 1), "C": (1, 1), "E": (2, 1), "inSW": (3, 1), "inSE": (4, 1),
                  "SW": (0, 2), "S": (1, 2), "SE": (2, 2), "C2": (3, 2), "C3": (4, 2)}
    plank = from_akti(akti_art.quay_gangplank())
    ship = from_akti(akti_art.trireme(), title="The trireme Euploia (Akti's painter)")
    bollard = from_akti(akti_harbor.bollard_line())
    return [finish(quay), finish(plank), finish(ship), finish(bollard)]


def build_sea():
    return [current(), helle_rock(), landing()]


def build_harbor():
    return harbor()


if __name__ == "__main__":
    for s in build_sea() + build_harbor():
        print(s.key, s.w, s.h, np.count_nonzero(s.M.a[..., 3]))
