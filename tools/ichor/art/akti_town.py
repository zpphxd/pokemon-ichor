"""Akti's town pieces for gTileset_Akti: the krene in the plaza, the gardens
(a fig and shrubs) and the edges where the quay's
paving runs out onto grass and sand.
"""
from __future__ import annotations

import math
import random

from akti_lib import Struct, ground
from kalliste_parts import doric_column

SEC = "akti"


# --------------------------------------------------------------------------
# The krene
# --------------------------------------------------------------------------

def krene():
    """A fountain house: a small Doric porch whose back wall holds a bronze lion's
    head, water pouring from its mouth into a marble basin. Townsfolk gather in
    front of it."""
    from akti_art import paint_paving
    s = Struct("krene", "Krene: the fountain house", 3, 3, SEC,
               walk=["XXX", "XXX", "XXX"],
               notes="A fountain house on the plaza's paving: a terracotta roof and pediment "
                     "(row 0), two Doric columns framing a bronze lion's-head spout (row 1), "
                     "and the marble basin it fills (row 2). Stand townsfolk in front of it.")
    B, M = s.B, s.M
    paint_paving(B, 0, 0, 48, 48, marble=False)
    W = 48
    # --- roof seen from above, falling to either side of a lit ridge
    for x in range(2, W - 2):
        for y in range(0, 8):
            col = x % 4 if x < 24 else 3 - x % 4
            if x < 24:
                c = "tc2" if col != 3 else "tc1"
            else:
                c = "tc1" if col != 3 else "tc0"
            if y % 4 == 3:
                c = "tc0"
            M.px(x, y, c)
    M.hline(2, W - 3, 0, "ink")
    M.vline(1, 0, 8, "ink")
    M.vline(W - 2, 0, 8, "ink")
    # --- pediment: raking cornice and a marble tympanum with a shell relief
    def ytop(x):
        return int(round(15 - 7 * (1 - abs(x - 23.5) / 22.5)))
    for x in range(1, W - 1):
        t = ytop(x)
        M.px(x, t, "ink")
        M.px(x, t + 1, "w0")
        for y in range(t + 2, 16):
            M.px(x, y, "m2")
    # entablature
    M.hline(0, W - 1, 16, "w0")
    M.hline(0, W - 1, 17, "m1")
    M.hline(0, W - 1, 18, "m3")
    M.hline(0, W - 1, 19, "m4")
    M.vline(0, 8, 19, "ink")
    M.vline(W - 1, 8, 19, "ink")
    # --- the porch: back wall in shade, the lion's head in bronze, its water
    M.rect(1, 20, W - 2, 14, "m4")
    M.rect(1, 20, W - 2, 2, "m5")
    lion = [
        "  kkkkkk  ",
        " kGggggGk ",
        "kGgkggkgGk",
        "kggggggggk",
        "kgbGggGbgk",
        " kgbkkbgk ",
        "  kbbbbk  ",
        "   kkkk   ",
    ]
    M.blit(lion, {"k": "ink", "G": "g1", "g": "g0", "b": "br"}, 19, 21)
    for y in range(28, 34):                     # the stream from its mouth
        M.px(23, y, "w0")
        M.px(24, y, "m1" if y % 2 else "w0")
    for x in (2, 39):                           # columns at the porch's corners
        doric_column(M, x, 16, 7, 18, ["m5", "m4", "m2", "m1", "w0"], "ink", fluted=False)
    # --- the basin: a marble trough brimming with water
    M.rect(8, 33, 32, 2, "m2")
    M.hline(8, 39, 33, "w0")
    M.rect(8, 35, 32, 9, "b1")
    M.hline(9, 38, 35, "b0")
    for y in range(36, 43):
        for x in range(9, 39):
            if (x + y * 3) % 8 == 0:
                M.px(x, y, "b2")
    M.ellipse(20, 35, 27, 39, "b2")          # where the stream strikes
    M.ellipse(22, 36, 25, 38, "w0")
    M.px(19, 37, "b3")
    M.px(28, 37, "b3")
    M.rect(8, 44, 32, 3, "m3")
    M.hline(8, 39, 44, "m2")
    M.hline(8, 39, 47, "m4")
    M.vline(8, 33, 47, "ink")
    M.vline(39, 33, 47, "ink")
    # The krene is symmetric: mirror its left half so the right half's tiles are
    # the left's, flipped (Porytiles stores them once).
    M.a[:, 24:48] = M.a[:, 0:24][:, ::-1]
    # column bases below the porch, on the paving
    for x in (2, 39):
        M.rect(x - 1, 34, 9, 13, "m2")
        M.vline(x - 1, 34, 46, "ink")
        M.vline(x + 7, 34, 46, "ink")
        M.vline(x, 34, 46, "w0")
        M.vline(x + 6, 34, 46, "m4")
        M.hline(x - 1, x + 7, 34, "m3")
        M.hline(x - 1, x + 7, 47, "m4")
    return s


# --------------------------------------------------------------------------
# Gardens
# --------------------------------------------------------------------------

def fig_tree():
    """A fig: broad lobed leaves, purple figs, a smooth grey trunk, and its shadow."""
    s = Struct("fig_tree", "Fig tree", 2, 2, SEC, walk=["XX", "XX"],
               notes="A fig tree on aethos grass, its shadow under it. All four cells solid.")
    ground(s, "grass")
    M = s.M
    M.ellipse(3, 24, 30, 31, "gr1")          # its shadow, drawn with the tree
    for x in range(4, 30, 2):
        M.px(x, 23, "gr1")
    rng = random.Random(4)
    # trunk and low branches
    M.rect(14, 18, 4, 12, "tk1")
    M.vline(14, 18, 29, "tk2")
    M.vline(17, 18, 29, "tk0")
    M.line(15, 19, 9, 13, "tk1")
    M.line(16, 19, 23, 12, "tk1")
    M.hline(12, 19, 29, "ink")
    # canopy: overlapping lobed leaves, lit from the upper left
    blobs = [(9, 9, 7), (21, 8, 7), (15, 5, 7), (6, 15, 5), (25, 15, 5), (16, 13, 6)]
    for (cx, cy, r) in blobs:
        M.ellipse(cx - r, cy - r, cx + r, cy + r, "ov1")
    for (cx, cy, r) in blobs:
        M.ellipse(cx - r + 1, cy - r + 1, cx + r - 2, cy + r - 2, "ov2")
        M.ellipse(cx - r + 2, cy - r + 1, cx - 1, cy - 1, "ov3")
    for _ in range(40):                        # leaf lobes and veins
        x, y = rng.randrange(3, 29), rng.randrange(1, 20)
        if M.get(x, y) == "ov2":
            M.px(x, y, rng.choice(("ov1", "ov3", "ov1")))
    for (x, y) in ((8, 12), (20, 11), (13, 7), (24, 16), (10, 17), (18, 15), (5, 14)):
        M.blit(["pP", "pp"], {"p": "pu0", "P": "pu1"}, x, y)
    # outline the canopy's silhouette in the darkest green
    import numpy as np
    a = M.a[..., 3] > 0
    pad = np.pad(a, 1)
    edge = a & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if M.get(x, y) in ("ov1", "ov2", "ov3"):
            M.px(x, y, "ov0")
    return s


def shrubs():
    s = Struct("shrubs", "Lentisk and rosemary", 2, 1, SEC, walk=["XX"],
               notes="Two low Mediterranean shrubs on aethos grass with their shadows, to break "
                     "up tree lines and soften corners.")
    ground(s, "grass")
    M = s.M
    rng = random.Random(17)
    for (cx, r) in ((8, 6), (24, 5)):
        M.ellipse(cx - r, 10, cx + r, 15, "gr1")
        M.ellipse(cx - r, 3, cx + r, 13, "ov1")
        M.ellipse(cx - r + 1, 4, cx + r - 2, 11, "ov2")
        M.ellipse(cx - r + 2, 4, cx, 8, "ov3")
        for _ in range(14):
            x, y = cx + rng.randint(-r + 1, r - 1), rng.randint(4, 12)
            if M.get(x, y):
                M.px(x, y, rng.choice(("ov1", "ov0", "ov3")))
        M.px(cx, 12, "ov0")
    for (x, y) in ((5, 6), (7, 4), (10, 7)):        # rosemary flowers
        M.px(x, y, "ov4")
    return s


# --------------------------------------------------------------------------
# Where the quay's paving runs out
# --------------------------------------------------------------------------

def _paving_strip(M, cells, edge, seed):
    """Quay flags spilling off a paved edge: a ragged lip and a few loose stones."""
    rng = random.Random(seed)
    for (cx, side) in cells:
        x0 = cx * 16
        for i in range(16):
            depth = 4 + int(2.5 * math.sin((i + seed) * 0.7)) + rng.randint(0, 1)
            for d in range(depth):
                if side == "n":
                    x, y = x0 + i, d
                else:
                    x, y = x0 + d, i
                c = "s4" if (x // 8 + y // 4) % 2 else "s5"
                if d == depth - 1:
                    c = "s2"
                elif d == depth - 2:
                    c = "s3"
                M.px(x, y, c)
        for _ in range(3):                           # loose stones beyond the lip
            a, b = rng.randrange(1, 14), rng.randrange(7, 12)
            x, y = (x0 + a, b) if side == "n" else (x0 + b, a)
            M.blit(["55", "32"], {"5": "s4", "3": "s3", "2": "s2"}, x, y)


def quay_edges():
    s = Struct("quay_edges", "Quay paving running out onto grass and sand", 2, 1, SEC,
               walk=[".."],
               notes="Lay these on the first row or column past the quay: on grass, flags "
                     "spilling from the quay to the north; on sand, flags spilling from the "
                     "quay to the west. Both walkable.")
    ground(s, "grass", [(0, 0)])
    ground(s, "sand", [(1, 0)])
    _paving_strip(s.M, [(0, "n")], None, 3)
    _paving_strip(s.M, [(1, "w")], None, 5)
    return s


def build():
    return [krene(), fig_tree(), shrubs(), quay_edges()]
