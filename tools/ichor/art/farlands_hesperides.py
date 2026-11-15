"""gTileset_Hesperides: the Garden of the Hesperides and the Atlas range.

The far west's sister set. LABORS's Labor 11 (the Garden, Atlas's Ridge) and,
for the Oikoumene, the Atlas foothills and the Atlas range's slopes, which
continue from Atlas's Ridge, so those maps share this set and need no seam
strip between them. It is always evening here: deep greens going blue, gold
light, the sky low overhead.

  garden   evening meadow grass (encounters), flowers, myrtle hedges
  tree     the golden-apple tree (4 x 4, its apples glinting) and Ladon's coils
  stone    the Hesperides' garden walls, a fountain, Arethousa's spring,
           the nymphs' bowers
  atlas    a cold-rock crag kit with snow on its brows, a snowline, cold high
           scrub, ledges, a cave mouth, and the summit edge where the sky hangs
           low enough to touch
"""
from __future__ import annotations

import math

import numpy as np

import farlands_lib as F
import farlands_ground as G
import farlands_kits as K
from farlands_lib import anim_layer, ground, put, struct

GROUPS = {
    # the evening meadow and its flowers
    "meadow": ["hg0", "hg1", "hg2", "hg3", "hg4", "ap1", "ap2", "ap3", "ev0", "ev1", "w0", "pk1",
               "pk2", "gd", "g1"],
    # the golden-apple tree and the hedges
    "tree": ["hg0", "hg1", "hg2", "hg3", "hg4", "ap0", "ap1", "ap2", "ap3", "w0", "tb0", "tb1",
             "tb2", "gd", "ev0"],
    # Ladon
    "ladon": ["ld0", "ld1", "ld2", "ld3", "ap1", "ap2", "ap3", "ink", "w0", "gd", "g1", "ev0",
              "hg1"],
    # marble walls, the fountain, the spring
    "marble": ["ml0", "ml1", "ml2", "ml3", "w0", "ev1", "ev2", "b2", "b3", "b4", "ap2", "hg1",
               "hg2", "pk1", "gd"],
    # the bowers: trellis, vines, roses, lamps
    "bower": ["tb0", "tb1", "tb2", "tb3", "hg1", "hg2", "hg3", "pk1", "pk2", "ap2", "ap3", "ink",
              "w0", "gd", "ev1"],
    # Atlas's cold rock and snow, cold scrub
    "mountain": ["cr0", "cr1", "cr2", "cr3", "sw1", "sw2", "w0", "ev0", "ev1", "gd", "g1", "ink",
                 "mq1", "mq2", "hg0"],
    # the low sky
    "sky": ["ns0", "ns1", "ns2", "ev1", "ev2", "ev3", "w0", "gl", "sw2", "cr1", "cr2"],
}

SEC_G, SEC_T, SEC_S, SEC_A = "garden", "tree", "stone", "atlas"
CR = ("cr0", "cr1", "cr2", "cr3", "sw1")
LEAF = ("hg0", "hg1", "hg2", "hg3")


# --------------------------------------------------------------------------
# The garden
# --------------------------------------------------------------------------

def _meadow_tex():
    return G.recolor_tex(0x00D, {"t0": "hg0", "t1": "hg1", "gd": "hg2", "t3": "hg3", "tg": "ap2"})


def garden_grass():
    return G.blob_set(
        "garden_grass", "Evening meadow grass (encounters)", SEC_G,
        G.grass_overlay(_meadow_tex(), "hg0", "hg3", "ap2", seed=8.8), on="grass", walk="G",
        notes="The garden's long grass in the evening: deep green going blue in the shadows, its "
              "seed heads catching the gold light, 47 soft-edge shapes over borrowed aethos grass. "
              "`MB_TALL_GRASS`: the optional grass where Applin fall (LABORS 11's map), and the "
              "meadows of the Atlas foothills.")


def decor():
    names = {"lilies": (0, 0), "asphodel": (1, 0), "petals": (2, 0), "windfalls": (3, 0),
             "roses": (4, 0), "myrtle_L": (5, 0), "myrtle": (6, 0), "myrtle_R": (7, 0)}
    s = struct("decor", "Flowers, windfalls and myrtle", 8, 1, SEC_G, walk=["....XXXX"],
               names=names,
               notes="On borrowed grass. Walkable: `lilies` (white), `asphodel` (pale gold spikes), "
                     "`petals` (rose petals on the grass), `windfalls` (fallen golden apples: one of "
                     "them a hidden item). Impassable: `roses`, a rose bush in flower; `myrtle_L` "
                     "`myrtle` `myrtle_R`, a clipped myrtle hedge, west-east, to border paths and the "
                     "bowers' lawns.")
    ground(s, "grass")
    M = s.M
    for (x, y) in ((3, 4), (10, 3), (6, 10), (13, 11), (2, 13)):
        put(M, x - 1, y - 1, [".w.", "wpw", ".g."], {"w": "w0", "p": "ap3", "g": "hg2"})
        M.px(x, y + 2, "hg1")
    for (x, y) in ((4, 5), (11, 4), (7, 11), (14, 12)):
        for j in range(5):
            M.px(16 + x, y + j, "ap3" if j < 3 else "hg2")
        M.px(16 + x - 1, y + 1, "ap2")
        M.px(16 + x + 1, y + 2, "ap2")
    for (x, y) in ((2, 3), (9, 2), (13, 7), (5, 9), (11, 12), (3, 14), (8, 6)):
        M.px(32 + x, y, "pk2")
        M.px(32 + x + 1, y, "pk1")
    for (x, y) in ((4, 5), (11, 9), (6, 12)):
        put(M, 48 + x - 1, y - 1, [".a.", "a3b", ".b."], {"a": "ap2", "3": "ap3", "b": "ap1"})
        M.px(48 + x + 1, y + 1, "gd")
    # rose bush
    m = F.blob(7.5, 8.5, 6.5, 5.5, 16, 16, wobble=0.1, k=6, seed=2)
    tmp = F.Layer(16, 16)
    F.foliage(tmp, m, LEAF, seed=5, outline="hg0", clump=3.0, flowers=["pk1", "pk2", "w0"], fl_rate=2)
    for y, x in np.argwhere(m):
        M.px(64 + x, y, tmp.get(x, y))
    for x in range(16):
        for y in range(1, 16):
            if not m[y, x] and m[y - 1, x]:
                M.px(64 + x, y, "gd")
    # myrtle hedge
    for i, (l, r) in ((5, (True, False)), (6, (False, False)), (7, (False, True))):
        m = F.mask_from(lambda x, y: 3 <= y <= 13 and (x >= (4 if l else 0)) and (x <= (11 if r else 15))
                        and not (l and (x - 4) ** 2 + (y - 8) ** 2 > 30 and x < 9)
                        and not (r and (x - 11) ** 2 + (y - 8) ** 2 > 30 and x > 6), 16, 16)
        tmp = F.Layer(16, 16)
        F.foliage(tmp, m, LEAF, seed=9, outline="hg0", clump=3.0)
        for y, x in np.argwhere(m):
            M.px(i * 16 + x, y, tmp.get(x, y))
        for x in range(16):
            if m[13, x]:
                M.px(i * 16 + x, 14, "gd")
    return s


# --------------------------------------------------------------------------
# The golden-apple tree and Ladon
# --------------------------------------------------------------------------

APPLES = [(9, 9), (17, 6), (27, 8), (37, 5), (46, 9), (54, 12), (12, 18), (22, 15), (31, 17),
          (41, 14), (50, 20), (6, 25), (18, 26), (28, 24), (38, 27), (47, 28), (57, 25), (24, 33),
          (34, 35), (14, 34), (44, 36)]


def tree():
    names = {f"c{x}{y}": (x, y) for y in range(4) for x in range(4)}
    s = struct("apple_tree", "The golden-apple tree", 4, 4, SEC_T,
               walk=["TTTT", "TTTT", "XXXX", ".XX."], names=names,
               notes="The tree Gaia gave Hera at her wedding, 4 x 4 on borrowed grass (`c00` to "
                     "`c33`, column then row): a broad crown going blue in the evening, hung with "
                     "golden apples lit as if from inside, a few of them glinting (the `glint` "
                     "animation), over a gnarled trunk and roots. The crown's two rows are drawn over "
                     "the player; the trunk row and the trunk's foot are impassable (put the tree's bg "
                     "event on `c12` or `c22`). Ladon (`ladon`) coils round its foot.")
    ground(s, "grass")
    M, T = s.M, s.T
    W, H = 64, 64
    # trunk and roots
    for y in range(32, 60):
        half = 5 + max(0, y - 50) * 0.9 + 1.2 * math.sin(y * 0.5)
        for x in range(32 - 12, 32 + 12):
            if abs(x - 31.5) <= half:
                u = (x - 31.5) / max(1, half)
                c = "tb2" if u < -0.3 else ("tb1" if u < 0.5 else "tb0")
                if F.h(x, y, 3) % 7 == 0:
                    c = "tb0"
                M.px(x, y, c)
    for (x0, dx) in ((27, -1), (36, 1)):
        for j in range(10):
            x = x0 + dx * j
            y = 56 + j // 3
            if 0 <= x < 64 and y < 64:
                M.px(x, y, "tb1")
                M.px(x, y + 1, "tb0")
    for x in range(14, 52):
        for y in range(58, 64):
            if M.get(x, y) is None and math.hypot((x - 33) / 18, (y - 60) / 3) < 1:
                M.px(x, y, "gd")
    # crown
    crown = F.mask_from(lambda x, y: math.hypot((x - 31.5) / 31.0, (y - 21) / 21.0) < 1
                        + 0.06 * math.sin(math.atan2(y - 21, x - 31.5) * 9), W, H)
    crown[44:, :] = False
    tmp = F.Layer(W, H)
    F.foliage(tmp, crown, LEAF, seed=21, outline="hg0", clump=4.5)
    # the evening light: gold on the western rim
    for y, x in np.argwhere(crown):
        if tmp.get(x, y) == "hg3" and x < 24 and F.h(x, y, 5) % 3 == 0:
            tmp.px(x, y, "hg4")
    # apples
    for (ax, ay) in APPLES:
        if crown[min(H - 1, ay), min(W - 1, ax)]:
            put(tmp, ax - 1, ay - 1, [".12.", "1232", "1220", ".00."],
                {"1": "ap2", "2": "ap2", "3": "ap3", "0": "ap1"})
            tmp.px(ax, ay - 1, "ap3")
    for y in range(H):
        for x in range(W):
            c = tmp.get(x, y)
            if c:
                (T if y < 32 else M).px(x, y, c)
    # glints: a white star on a few apples now and then
    frT = anim_layer(s, "glint", 3, layer="top")
    for f, pts in ((0, [(17, 6), (41, 14)]), (1, [(27, 8), (22, 15), (50, 20)])):
        for (ax, ay) in pts:
            put(frT[f], ax - 2, ay - 2, ["..w..", ".wbw.", "wbwbw", ".wbw.", "..w.."] if f == 1 else
                ["....", ".w..", "wbw.", ".w.."], {"w": "w0", "b": "ap3"})
    F.settle(s, "glint", [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (3, 1)])
    return s


def ladon():
    names = {"W_top": (0, 0), "W": (0, 1), "E_top": (1, 0), "E": (1, 1),
             "head": (2, 0), "coil": (3, 0), "coil_b": (4, 0), "tail": (5, 0),
             "loop": (2, 1), "loop_b": (3, 1), "tail_b": (4, 1), "coil_V": (5, 1)}
    s = struct("ladon", "Ladon's coils", 6, 2, SEC_T, walk=["XXXXXX", "XXXXXX"], names=names,
               notes="The serpent who never sleeps, asleep, coiled round the tree, as scenery on "
                     "borrowed grass (impassable). Wrap the tree: `W_top` over `W` stand against "
                     "the trunk row's west side, `E_top` over `E` its east; along the front, from "
                     "west to east, `head` (resting on a coil, eye shut), then any run of `coil`, "
                     "`coil_b`, `loop`, `loop_b`, ending in `tail` or `tail_b`. `coil_V` is a run "
                     "going north-south. He is fought here (Melodrakon, LABORS 11); when he's caught "
                     "or gone, swap every Ladon cell for aethos grass (`0x001`). Gold belly scales, "
                     "green-teal back.")
    ground(s, "grass")
    M = s.M

    def body(L, pts, width=6.0):
        """A thick coil along a polyline of (x, y), back lit, belly gold."""
        mask = np.zeros((32, 96), bool)
        side = np.zeros((32, 96), float)
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
            for i in range(n + 1):
                u = i / n
                cx, cy = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
                for y in range(int(cy - width), int(cy + width) + 1):
                    for x in range(int(cx - width), int(cx + width) + 1):
                        if 0 <= y < 32 and 0 <= x < 96:
                            d = math.hypot(x - cx, y - cy)
                            if d <= width / 2:
                                mask[y, x] = True
                                side[y, x] = (y - cy) / (width / 2)
        for y, x in np.argwhere(mask):
            v = side[y, x]
            if v > 0.45:
                c = "ap2" if (x + y) % 3 else "ap1"
            elif v < -0.4:
                c = "ld3"
            else:
                c = "ld2" if (x // 2 + y) % 3 else "ld1"
                if (x + 2 * y) % 5 == 0:
                    c = "ld1"
            L.px(int(x), int(y), c)
        for y, x in np.argwhere(F.edge_of(mask)):
            L.px(int(x), int(y), "ld0")
        for x in range(96):
            for y in range(1, 32):
                if not mask[y, x] and mask[y - 1, x] and L.get(x, y) is None:
                    L.px(x, y, "gd")
        return mask

    tmp = F.Layer(96, 32)
    # the trunk-side columns: coils rising, looped round the trunk
    body(tmp, [(8, 30), (6, 22), (10, 14), (7, 6), (11, 1)], 7)
    body(tmp, [(24, 30), (26, 22), (22, 14), (25, 6), (21, 1)], 7)
    # the front: head, coils, tail
    body(tmp, [(46, 12), (40, 10), (36, 12), (34, 13)], 6)
    body(tmp, [(48, 4), (56, 13), (64, 4)], 7)
    body(tmp, [(64, 12), (72, 4), (80, 12)], 7)
    body(tmp, [(80, 4), (86, 10), (92, 12), (95, 11)], 5)
    body(tmp, [(32, 22), (40, 28), (48, 20)], 7)
    body(tmp, [(48, 28), (56, 20), (64, 28)], 7)
    body(tmp, [(64, 20), (72, 26), (76, 28), (79, 27)], 5)
    body(tmp, [(88, 16), (86, 24), (90, 31)], 7)
    # the head: a broad dragon's head, eye shut, a gold crest
    put(tmp, 33, 4, [
        "....000000....",
        "..002222220...",
        ".0222222222000",
        "0223322222ap00",
        "02233332022220",
        "0222222222220.",
        ".000000000000.",
    ], {"0": "ld0", "2": "ld2", "3": "ld3", "a": "ap2", "p": "ap3"})
    for x in range(41, 45):
        tmp.px(x, 8, "ink")
    for (x, y) in ((35, 3), (37, 2), (39, 2)):
        tmp.px(x, y, "ap2")
    for y in range(32):
        for x in range(96):
            c = tmp.get(x, y)
            if c:
                M.px(x, y, c)
    return s


# --------------------------------------------------------------------------
# Stone: walls, fountain, spring, bowers
# --------------------------------------------------------------------------

def walls():
    names = {"H_L": (0, 0), "H": (1, 0), "H_roses": (2, 0), "H_R": (3, 0), "gate_L": (4, 0),
             "gate_R": (5, 0), "V_T": (0, 1), "V": (1, 1), "V_B": (2, 1), "NW": (3, 1), "NE": (4, 1),
             "V_ivy": (5, 1)}
    s = struct("walls", "The Hesperides' garden walls", 6, 2, SEC_S,
               walk=["XXXXXX", "XXXXXX"], names=names,
               notes="Low marble walls on borrowed grass, a gilded coping, climbing roses, impassable. "
                     "`H_L` `H` `H_R` a west-east run (`H_roses` breaks it with roses); `gate_L` "
                     "`gate_R` the posts either side of a two-cell gateway (leave the cells between "
                     "them open); `V_T` `V` `V_B` a north-south run (`V_ivy` with ivy); `NW` and `NE` "
                     "the corners where a west-east run turns south.")
    ground(s, "grass")
    M = s.M

    def hwall(ox, oy, left=True, right=True, roses=False):
        x0 = ox + (4 if not left else 0)
        x1 = ox + (11 if not right else 15)
        for y in range(5, 15):
            for x in range(x0, x1 + 1):
                if y < 7:
                    c = "ap2" if y == 5 else "ml3"
                elif y < 13:
                    c = "ml2" if (x + (y // 3) * 4) % 8 else "ml1"
                    if y % 3 == 0:
                        c = "ml1"
                else:
                    c = "ml0"
                M.px(x, oy + y, c)
            M.px(x0, oy + y, "ml0") if not left else None
            M.px(x1, oy + y, "ml0") if not right else None
        for x in range(x0, x1 + 1):
            M.px(x, oy + 15, "gd")
        if roses:
            for (rx, ry) in ((ox + 3, 8), (ox + 9, 10), (ox + 13, 7), (ox + 6, 12)):
                put(M, rx - 1, oy + ry - 1, [".h.", "hph", ".h."], {"h": "hg2", "p": "pk1"})
            for x in range(ox + 1, ox + 15, 3):
                M.px(x, oy + 9, "hg1")

    def post(ox, oy):
        for y in range(1, 15):
            for x in range(ox + 3, ox + 13):
                c = "ml3" if x < ox + 6 else ("ml2" if x < ox + 10 else "ml1")
                if y < 3:
                    c = "ap2" if y == 1 else "ml3"
                M.px(x, oy + y, c)
        put(M, ox + 5, oy - 0, ["....", ".aa.", "aaaa"], {"a": "ap2"})
        for x in range(ox + 3, ox + 15):
            M.px(x, oy + 15, "gd")

    def vwall(ox, oy, top=True, bottom=True, ivy=False):
        y0 = oy + (0 if top else 5)
        y1 = oy + (15 if bottom else 12)
        for y in range(y0, y1 + 1):
            for x in range(ox + 5, ox + 11):
                c = "ap2" if x == ox + 5 else ("ml3" if x < ox + 8 else "ml2")
                M.px(x, y, c)
            M.px(ox + 11, y, "ml0")
            M.px(ox + 12, y, "gd")
        if ivy:
            for y in range(y0, y1 + 1, 2):
                M.px(ox + 7 + (y % 3), y, "hg2")
                M.px(ox + 8, y + 1, "hg1")

    hwall(0, 0, left=False)
    hwall(16, 0)
    hwall(32, 0, roses=True)
    hwall(48, 0, right=False)
    post(64, 0)
    post(80, 0)
    vwall(0, 16, top=False)
    vwall(16, 16)
    vwall(32, 16, bottom=False)
    hwall(48, 16, left=False)
    vwall(48 - 3, 16, top=False)
    hwall(64, 16, right=False)
    vwall(64 + 3, 16, top=False)
    vwall(80, 16, ivy=True)
    return s


def fountain():
    names = {"TL": (0, 0), "TR": (1, 0), "BL": (0, 1), "BR": (1, 1),
             "spring_TL": (2, 0), "spring_TR": (3, 0), "spring_BL": (2, 1), "spring_BR": (3, 1)}
    s = struct("fountain", "A fountain, and Arethousa's spring", 4, 2, SEC_S,
               walk=["XXXX", "XXXX"], names=names,
               notes="On borrowed grass, impassable. The fountain (2 x 2, `TL` `TR` / `BL` `BR`): a "
                     "marble basin with a jet that plays (`splash`). Arethousa's spring (2 x 2, "
                     "`spring_*`): water welling up among mossy marble blocks into a round pool; the "
                     "hidden Lansat Berry is by it (LABORS 11's map).")
    ground(s, "grass")
    M = s.M
    for y in range(32):
        for x in range(32):
            d = math.hypot((x - 15.5) / 14.5, (y - 19) / 10.5)
            if d < 1:
                if d > 0.82:
                    c = "ml3" if y < 19 else ("ml2" if x < 16 else "ml1")
                else:
                    c = "b3" if (x + y) % 4 else "b4"
                    if y < 16 and d > 0.6:
                        c = "b2"
                M.px(x, y, c)
            elif d < 1.12 and y > 19:
                M.px(x, y, "ml0")
            elif d < 1.2 and y > 22:
                M.px(x, y, "gd")
    # the jet: a pedestal and spray, animated
    for y in range(8, 20):
        M.px(15, y, "ml2")
        M.px(16, y, "ml1")
    fr = anim_layer(s, "splash", 3)
    for f, L in enumerate([M] + fr):
        for j in range(9):
            y = 9 - j
            for side in (-1, 1):
                x = 15.5 + side * (j * 0.6 + f * 0.4)
                yy = int(y + (j * j) * 0.12 + f * 0.5)
                if 0 <= yy < 32:
                    L.px(int(x), yy, "w0" if j % 2 == f % 2 else "b4")
        for (x, y) in ((8 + f, 15), (22 - f, 15), (12, 17 - f % 2), (19, 17 - (f + 1) % 2)):
            L.px(x, y, "w0")
    F.settle(s, "splash", [(0, 0), (1, 0), (0, 1), (1, 1)])
    # the spring: mossy blocks round a well-up pool
    for y in range(32):
        for x in range(32):
            d = math.hypot((x - 16) / 11.0, (y - 18) / 9.0)
            if d < 1:
                c = "b3" if d > 0.4 else ("w0" if (x + y) % 3 == 0 else "b4")
                M.px(32 + x, y, c)
    for (bx, by, w, h_) in ((3, 9, 8, 6), (11, 5, 9, 5), (21, 8, 8, 6), (2, 20, 7, 6), (24, 21, 7, 6),
                            (10, 26, 12, 5)):
        for y in range(by, by + h_):
            for x in range(bx, bx + w):
                if 0 <= y < 32:
                    c = "ml2" if y < by + 2 else ("ml1" if x < bx + w - 2 else "ml0")
                    if (x + y) % 5 == 0 and y < by + 3:
                        c = "hg2"
                    M.px(32 + x, y, c)
        for x in range(bx, bx + w):
            if by + h_ < 32:
                M.px(32 + x, by + h_, "gd")
    return s


def bower():
    names = {f"c{x}{y}": (x, y) for y in range(3) for x in range(3)}
    names["door"] = (1, 2)
    s = struct("bower", "A nymph's bower", 3, 3, SEC_S, walk=["TTT", "XXX", "XDX"], names=names,
               notes="Where a Hesperid lives (Aigle, Arethousa, Hespere: LABORS 11's three bowers), 3 "
                     "x 3 on borrowed grass: a timber arbor roofed with vines and climbing roses, gold "
                     "lamps hung under the eaves, a curtain of leaves over the door (`door`, "
                     "`MB_NON_ANIMATED_DOOR`). Its top row is drawn over the player. Set each nymph's "
                     "bower apart with what grows round it (`decor`'s lilies, asphodel, roses).")
    ground(s, "grass")
    M, T = s.M, s.T
    W = 48
    # posts and the trellis wall
    for y in range(20, 46):
        for x in range(4, 44):
            c = None
            if x in (4, 5, 42, 43) or x in (23, 24):
                c = "tb2" if x % 2 == 0 else "tb1"
            elif (x - 4) % 6 == 0 or (y - 20) % 6 == 0:
                c = "tb2"
            elif (x + y) % 3 == 0:
                c = "hg2"
            else:
                c = "hg1" if (x * 3 + y) % 5 else "tb0"
            M.px(x, y, c)
    for x in range(4, 44):
        M.px(x, 46, "tb0")
        M.px(x + 1, 47, "gd")
    # the door: a curtain of leaves
    for y in range(32, 46):
        for x in range(18, 30):
            c = "hg3" if (x + y // 2) % 3 == 0 else ("hg2" if (x + y) % 2 else "hg1")
            if y == 32:
                c = "tb1"
            M.px(x, y, c)
    # the vine roof: a rounded mass, roses, lamps
    roof = F.mask_from(lambda x, y: math.hypot((x - 23.5) / 24, (y - 14) / 12) < 1
                       + 0.05 * math.sin(math.atan2(y - 14, x - 23.5) * 10) and y < 26, W, 48)
    tmp = F.Layer(W, 48)
    F.foliage(tmp, roof, ("hg1", "hg1", "hg2", "hg3"), seed=31, outline="tb0", clump=3.2,
              flowers=["pk1", "pk2", "w0"], fl_rate=4)
    for y, x in np.argwhere(roof):
        (T if y < 16 else M).px(int(x), int(y), tmp.get(int(x), int(y)))
    for (lx, ly) in ((8, 24), (39, 24), (23, 25)):
        put(M, lx - 1, ly, [".k.", "a3a", ".a."], {"k": "tb0", "a": "ap2", "3": "ap3"})
    return s


# --------------------------------------------------------------------------
# Atlas
# --------------------------------------------------------------------------

def crag():
    def cave(s, M, ox, oy):
        K.cave_mouth(M, ox, oy, ("ev0", "ink"), "cr1")

    def icy(s, M, ox, oy):
        for y in range(16):
            for x in range(16):
                c = K.rock_px(ox + x + 5, oy + y + 3, CR, 0, 2)
                if (x + 2 * y) % 11 == 0 or (y < 4 and F.hp(x, y, 1) % 3 == 0):
                    c = "sw2"
                M.px(ox + x, oy + y, c)

    s = K.cliff_kit("crag", "Atlas's crags, snow on their brows", SEC_A, CR, "cr0", "ev0",
                    notes=K.CLIFF_NOTES + " Cold blue-grey rock, its crests dusted with snow. "
                    "Extra faces: `face_ice`, a face glazed with ice; `cave`, a cave mouth "
                    "(`MB_NON_ANIMATED_DOOR`): the Atlas range's caves, Jirachi's and Moltres's "
                    "climbs (the Oikoumene's). For Atlas's Ridge and the Oikoumene's Atlas foothills "
                    "and range.",
                    oik=False, seed=2, snow=("sw1", "sw2"),
                    extra_faces=[("face_ice", icy), ("cave", cave)])
    F.set_walk(s, ["XXXX", "XXXX", "XXXX", "XXXX", "....", "XDXX"])
    return s


def _snow_px(X, Y):
    k = F.hp(X, Y, 81)
    c = "sw2" if k % 4 else "w0"
    if k % 11 == 0:
        c = "sw1"
    return c


def snowline():
    return G.blob_set(
        "snowline", "The snowline", SEC_A,
        G.earth_overlay(_snow_px, "sw1", None, margin=2.0, radius=4.5, amp=2.4, seed=9.1),
        on="grass", walk=".", oik=True,
        notes="Old snow lying in the hollows above the treeline, 47 soft-edge shapes over borrowed "
              "grass, walkable: the snowline transition the Atlas foothills climb through. Above "
              "it, whole fields of it; below, a patch or two in the shadow of a crag.")


def cold():
    names = {"cold_scrub": (0, 0), "cold_scrub_b": (1, 0), "frost_grass": (2, 0), "scree": (3, 0),
             "ledge_S": (4, 0), "ledge_W": (5, 0), "ledge_E": (6, 0)}
    s = struct("cold", "Cold scrub, frost, scree and ledges", 7, 1, SEC_A, walk=["XX..J<>"],
               names=names, oik=True,
               notes="On borrowed grass, for the high slopes. `cold_scrub` and `cold_scrub_b`: "
                     "wind-cut juniper, rimed with frost (impassable). `frost_grass`: grass stiff "
                     "with hoar-frost; `scree`: loose stones (both walkable). Ledges in the cold "
                     "rock: `ledge_S` jumps south, `ledge_W` west, `ledge_E` east.")
    ground(s, "grass")
    M = s.M
    for i, seed in ((0, 1.0), (1, 3.0)):
        m = F.blob(7.5, 9.5, 7.0, 4.8, 16, 16, wobble=0.18, k=8, seed=seed)
        tmp = F.Layer(16, 16)
        F.foliage(tmp, m, ("hg0", "mq1", "mq1", "mq2"), seed=4 + i, outline="hg0", clump=2.5,
                  flowers=["sw2", "w0"], fl_rate=4)
        for y, x in np.argwhere(m):
            M.px(i * 16 + x, y, tmp.get(x, y))
        for x in range(16):
            for y in range(1, 16):
                if not m[y, x] and m[y - 1, x]:
                    M.px(i * 16 + x, y, "ev0")
    for (x, y) in ((2, 3), (7, 2), (12, 5), (4, 9), (10, 10), (14, 13), (6, 13), (1, 7)):
        M.px(32 + x, y, "sw2")
        M.px(32 + x + 1, y, "w0")
        M.px(32 + x, y + 1, "sw1")
    for (x, y, r) in ((4, 4, 2.0), (10, 3, 1.6), (12, 9, 2.2), (5, 11, 1.8), (9, 13, 1.4), (2, 8, 1.2)):
        for yy in range(16):
            for xx in range(16):
                d = math.hypot(xx - x, (yy - y) * 1.2)
                if d < r:
                    M.px(48 + xx, yy, "cr3" if yy < y else "cr2")
                elif d < r + 0.9 and yy >= y:
                    M.px(48 + xx, yy, "cr1")
    for x in range(16):
        top = 8 + int(round(math.sin(x * 0.5) * 0.8))
        for y in range(top, top + 5):
            c = "sw2" if y == top else ("cr3" if y == top + 1 else ("cr2" if y < top + 4 else "cr1"))
            M.px(64 + x, y, c)
        M.px(64 + x, top + 5, "ev0")
    for i, side in ((5, "W"), (6, "E")):
        for y in range(16):
            for k in range(5):
                x = 6 + k if side == "W" else 9 - k
                c = "sw2" if k == 0 else ("cr3" if k == 1 else ("cr2" if k < 4 else "cr1"))
                M.px(i * 16 + x, y, c)
            M.px(i * 16 + (5 if side == "W" else 10), y, "ev0")
    return s


def low_sky():
    names = {"sky": (0, 0), "sky_b": (1, 0), "rim_L": (2, 0), "rim": (3, 0), "rim_b": (4, 0),
             "rim_R": (5, 0)}
    s = struct("low_sky", "The summit edge, where the sky hangs low", 6, 1, SEC_A,
               walk=["XXXXXX"], names=names, oik=False,
               notes="The sky's underside, sagging down onto the summit (LABORS 11's Atlas's Ridge, "
                     "and the Oikoumene's Atlas range, where Jirachi waits): a dark blue weight full "
                     "of stars, its lower edge glowing. Impassable, drawn whole. `sky` and `sky_b` "
                     "fill the top of the map; `rim` and `rim_b` are its lower edge over the summit's "
                     "snow (the sky above, a glowing seam, then snow), `rim_L` and `rim_R` the ends "
                     "where it lifts away. Its stars twinkle (`twinkle`).")
    B = s.B
    for i in range(6):
        for y in range(16):
            for x in range(16):
                X = i * 16 + x
                if i < 2:
                    edge = 99
                else:
                    sag = 10 + int(round(math.sin(2 * math.pi * (x + 3 * i) / 16) * 0.8))
                    if i == 2:
                        sag = min(sag, 2 + x // 2 + 2)
                    if i == 5:
                        sag = min(sag, 2 + (15 - x) // 2 + 2)
                    edge = sag
                if y < edge:
                    k = F.hp(x + 7 * i, y, 13)
                    c = "ns0" if y < edge - 6 or i < 2 else ("ns1" if y < edge - 2 else "ns2")
                    if i < 2:
                        c = "ns0" if (y + x // 4) % 7 else "ns1"
                    if k % 29 == 0:
                        c = "w0"
                    elif k % 19 == 0:
                        c = "ev2"
                    if y == edge - 1:
                        c = "gl" if (x + i) % 3 else "ev3"
                    elif y == edge - 2:
                        c = "ev2"
                else:
                    c = "sw2" if (x + y) % 5 else "w0"
                    if y == edge:
                        c = "ev3"
                    if F.hp(x, y, 2) % 13 == 0:
                        c = "cr2"
                B.px(X, y, c)
    fr = anim_layer(s, "twinkle", 3, layer="bottom")
    for f, L in enumerate(fr):
        for i in range(6):
            for (x, y) in ((3, 2), (11, 5), (7, 8), (14, 1)):
                if i >= 2 and y > 6:
                    continue
                X = i * 16 + x
                if (x + y + i + f) % 2 == 0:
                    L.px(X, y, "w0")
                    L.px(X + 1, y, "ev3")
                    L.px(X, y + 1, "ev3")
                else:
                    L.px(X, y, "gl")
    return s


def build():
    out = {}
    for s in (garden_grass(), decor(), tree(), ladon(), walls(), fountain(), bower(), crag(),
              snowline(), cold(), low_sky()):
        out[s.key] = s
    return out


SPEC = {
    "symbol": "gTileset_Hesperides", "dir": "hesperides", "label": "Hesperides",
    "title": "the Garden of the Hesperides and the Atlas range",
    "doc": "TILES_hesperides.md",
    "limit": 504,
    "sections": [
        ("garden", ["garden_grass", "decor"]),
        ("tree", ["apple_tree", "ladon"]),
        ("stone", ["walls", "fountain", "bower"]),
        ("atlas", ["crag", "snowline", "cold", "low_sky"]),
    ],
    "rows": {"garden": 0, "tree": 10, "stone": 18, "atlas": 26},
    "labels": [("ladon", [("head", "Ladon_Head"), ("coil", "Ladon_Coil"), ("W", "Ladon_W"),
                          ("E", "Ladon_E")])],
}
