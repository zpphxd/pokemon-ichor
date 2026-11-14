"""Kythera's land: myrtle hedges, rose briar, sea-grass and thrift (the tall
grass), meadow flowers and narcissus, plane trees, oleander and apple trees,
the rose-marble quarry with its column drums (the Girdle gate), and pink-stone
terrace walls.

Everything stands on borrowed aethos grass or path, so it meets the meadow
exactly; the sea-grass is the exception, drawn whole as soft-edged tall grass
on aethos's grass texture.
"""
from __future__ import annotations

import math

import numpy as np

import kythera_lib as K
from kythera_lib import ground, put, struct
from kythera_coast import stone_px, wob

SEC = "land"
GRASS = 0x001

# --------------------------------------------------------------------------
# Foliage
# --------------------------------------------------------------------------

MYRTLE = ("my1", "my1", "my2", "my3")         # dark glossy myrtle
LEAF = ("my1", "my2", "my3", "my4")           # plane, apple, briar
OLEANDER = ("t0", "my1", "my2", "my3")


def foliage(L, mask, ramp, seed=0, outline="t0", clump=4.0, flowers=None, fl_rate=0,
            periodic=True):
    """Shade a foliage mass (mask: 2D bool array the size of L) as clumps of
    leaves lit from the top left, with a dark outline. ramp is dark -> light
    (4 colors). Clumps sit on a 16 px periodic jittered grid, so a hedge run
    repeats cleanly. flowers: colors dotted over the lit side."""
    hgt, wid = mask.shape
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return
    n = int(round(16 / clump))
    cl = 16 / n
    for y, x in zip(ys, xs):
        x, y = int(x), int(y)
        px_, py_ = (x % 16, y % 16) if periodic else (x, y)
        best, bd = None, 1e9
        gx, gy = int(px_ // cl), int(py_ // cl)
        for j in (gy - 1, gy, gy + 1):
            for i in (gx - 1, gx, gx + 1):
                hh = K.h(i % n if periodic else i, j % n if periodic else j, seed + 3)
                cx_ = (i + 0.25 + (hh % 6) / 10) * cl
                cy_ = (j + 0.25 + ((hh // 6) % 6) / 10) * cl
                d = (px_ - cx_) ** 2 + (py_ - cy_) ** 2
                if d < bd:
                    bd, best = d, (cx_, cy_)
        dx, dy = px_ - best[0], py_ - best[1]
        t = dx + dy
        lvl = 2 if t < -1.0 else (1 if t < 1.5 else 0)
        # the whole mass is lit from the top left, shadowed underneath
        up = sum(1 for k in range(1, 4) if y - k < 0 or not mask[y - k, x])
        left = sum(1 for k in range(1, 3) if x - k < 0 or not mask[y, x - k])
        down = sum(1 for k in range(1, 4) if y + k >= hgt or not mask[y + k, x])
        if up >= 2 or (left >= 2 and up >= 1):
            lvl += 1
        if down >= 2:
            lvl -= 1
        lvl = max(0, min(3, lvl + 1 if lvl < 3 else 3))
        L.px(x, y, ramp[lvl])
        if flowers and lvl >= 2 and K.hp(x, y, seed + 9) % fl_rate == 0:
            L.px(x, y, flowers[K.hp(x, y, seed + 1) % len(flowers)])
    if outline:
        sub = K.Layer(wid, hgt)
        sub.mask_fill(mask, ramp[0])
        sub.outline(outline)
        for y, x in zip(*np.nonzero(sub.a[..., 3] > 0)):
            if sub.get(int(x), int(y)) == outline:
                L.px(int(x), int(y), outline)


def blob_mask(w, h_, pts_fn):
    m = np.zeros((h_, w), bool)
    for y in range(h_):
        for x in range(w):
            m[y, x] = pts_fn(x, y)
    return m


def grass_shadow(L, mask_fn, x0, y0, w, h_):
    """Darken borrowed grass under something: paint gd on the shadow area."""
    for y in range(y0, y0 + h_):
        for x in range(x0, x0 + w):
            if L.get(x, y) is None and mask_fn(x, y):
                L.px(x, y, "gd" if (x + y) % 2 == 0 or mask_fn(x, y - 1) else "g1")


# --------------------------------------------------------------------------
# Myrtle hedge
# --------------------------------------------------------------------------

def hedge():
    names = {"L": (0, 0), "M": (1, 0), "M2": (2, 0), "R": (3, 0), "single": (4, 0),
             "T": (5, 0), "V": (5, 1), "B": (5, 2),
             "NW": (0, 1), "NE": (1, 1), "SW": (0, 2), "SE": (1, 2),
             "end_bloom": (2, 1), "gap_stair": (3, 1), "thin": (4, 1),
             "low_L": (2, 2), "low_R": (3, 2), "bush": (4, 2)}
    walk = ["XXXXXX", "XXX.XX", "XXXXXX"]
    s = struct("myrtle", "Myrtle hedges", 6, 3, SEC, walk=walk, names=names,
               notes="Dense, glossy myrtle starred with white flowers, Aphrodite's shrub: the ridge "
                     "along the Foam Road and the glade round the spring. Runs east-west: `L` `M` "
                     "(`M2` breaks up a long run) `R`; north-south: `T` `V` `B`; turns: `NW` `NE` "
                     "`SW` `SE` (named by the corner of the hedge they make). `single` stands alone, "
                     "`bush` is a smaller round one. `gap_stair` is the run broken by rough stone steps "
                     "(the stair up to the spring: walkable). `end_bloom` is a run end in heavy flower; "
                     "`thin` is a gappy stretch; `low_L` `low_R` a low clipped run's ends. All on "
                     "borrowed grass; impassable except the stair.")
    ground(s, "grass")
    M = s.M
    W, H = 6 * 16, 3 * 16
    mask = np.zeros((H, W), bool)

    def top_edge(X, k=0):
        return 2 + 1.6 * math.sin(2 * math.pi * X / 16 + k) + 0.8 * math.sin(2 * math.pi * X / 8 + 1 + k)

    def run(cx, cy, l=False, r=False, k=0.0, lo=0):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, cy * 16 + y
                te = top_edge(X, k) + lo
                if y < te or y > 13:
                    continue
                if l and math.hypot(max(0, 7 - x), max(0, 8 - y)) > 7.5:
                    continue
                if r and math.hypot(max(0, x - 8), max(0, 8 - y)) > 7.5:
                    continue
                mask[Y, X] = True

    def col(cx, cy, t=False, b=False):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, cy * 16 + y
                half = 6.5 + 0.8 * math.sin(2 * math.pi * Y / 16)
                if abs(x - 7.5) > half:
                    continue
                if t and math.hypot(x - 7.5, max(0, 7 - y)) > 7.2:
                    continue
                if b and y > 13:
                    continue
                mask[Y, X] = True

    run(0, 0, l=True)
    run(1, 0)
    run(2, 0, k=1.3)
    run(3, 0, r=True)
    for y in range(16):          # single: a round clump
        for x in range(16):
            if math.hypot((x - 7.5) / 7.2, (y - 7.5) / 6.6) < 1 and y < 14:
                mask[y, 64 + x] = True
    col(5, 0, t=True)
    col(5, 1)
    col(5, 2, b=True)
    # corners: NW = hedge going east and south (corner at top-left)
    for (cx, cy, ex, sy) in ((0, 1, 1, 1), (1, 1, -1, 1), (0, 2, 1, -1), (1, 2, -1, -1)):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, cy * 16 + y
                hx = (x >= 1) if ex > 0 else (x <= 14)          # horizontal arm
                in_h = 2 + top_edge(X) * 0.5 <= y <= 13 and (x >= 5 if ex > 0 else x <= 10)
                in_v = abs(x - 7.5) <= 6.5 and ((y >= 6) if sy > 0 else (y <= 10))
                corner = math.hypot(x - 7.5, y - 7.5) < 7.2
                if (in_h or in_v or corner) and hx and y <= (13 if sy < 0 or True else 15):
                    if sy < 0 and y > 13:
                        continue
                    mask[Y, X] = True
    run(2, 1, r=True)            # end_bloom
    run(4, 1, k=2.1)             # thin
    run(2, 2, l=True, lo=3)      # low ends
    run(3, 2, r=True, lo=3)
    for y in range(16):          # bush
        for x in range(16):
            if math.hypot((x - 7.5) / 5.6, (y - 8.5) / 5.0) < 1:
                mask[32 + y, 64 + x] = True
    # the stair cell: hedge either side of rough steps
    for y in range(16):
        for x in range(16):
            X, Y = 48 + x, 16 + y
            te = top_edge(X)
            if te <= y <= 13 and (x < 3 or x > 12):
                mask[Y, X] = True
    # thin: punch gaps
    for (gx, gy, r) in ((4 * 16 + 4, 16 + 9, 2.5), (4 * 16 + 11, 16 + 6, 2.0)):
        for y in range(H):
            for x in range(W):
                if math.hypot(x - gx, y - gy) < r:
                    mask[y, x] = False
    # shadows on the grass below each mass, then the foliage
    sh = np.zeros_like(mask)
    sh[2:, 1:] = mask[:-2, :-1]
    for y, x in zip(*np.nonzero(sh & ~mask)):
        if y % 16 >= 10:
            M.px(int(x), int(y), "gd" if (x + y) % 2 == 0 or y % 16 > 13 else "g1")
    foliage(M, mask, MYRTLE, seed=2, flowers=["w0", "w0", "my4"], fl_rate=9)
    for (bx, by) in ((2 * 16 + 4, 16 + 5), (2 * 16 + 8, 16 + 8), (2 * 16 + 3, 16 + 10),
                     (2 * 16 + 7, 16 + 4)):
        put(M, bx, by, [".w.", "wyw", ".w."], {"w": "w0", "y": "kt2"})
    # the stair: rough pink-free steps of trodden earth and stone (green group)
    for i, y in enumerate((3, 7, 11)):
        for x in range(3, 13):
            M.px(48 + x, 16 + y, "kt2")
            M.px(48 + x, 16 + y + 1, "kt2" if x % 5 else "kt1")
            M.px(48 + x, 16 + y + 2, "kt1")
            M.px(48 + x, 16 + y + 3, "g1" if (x + i) % 3 else "gd")
    return s


# --------------------------------------------------------------------------
# Rose briar, oleander, flowers
# --------------------------------------------------------------------------

def flowers():
    names = {"briar": (0, 0), "briar_L": (1, 0), "briar_R": (2, 0), "oleander": (3, 0),
             "thrift": (4, 0), "narcissus": (5, 0), "narcissus_b": (6, 0), "petals": (7, 0),
             "basil_pot": (7, 1)}
    s = struct("flowers", "Rose briar, oleander and meadow flowers", 8, 2, SEC,
               walk=["XXXX....", "XXXXXXX."], names=names,
               notes="On borrowed grass. `briar` is a wild rose bush; `briar_L` `briar_R` a two-cell "
                     "thicket. `oleander` is the ravine's pink-flowered shrub. Walkable decorations: "
                     "`thrift`, sea-pink cushions; `narcissus` and `narcissus_b`, the white flower of "
                     "the spring (ring Kallirhoe's pool with them); `petals`, rose petals blown on the "
                     "grass; `basil_pot`, a pot of basil set out on the grass.")
    ground(s, "grass", [(x, 0) for x in range(8)] + [(7, 1)])
    M = s.M
    W, H = 8 * 16, 2 * 16
    m = np.zeros((H, W), bool)
    for y in range(16):
        for x in range(16):
            if math.hypot((x - 7.5) / 7.0, (y - 8.0) / 6.4) < 1 and y < 14:
                m[y, x] = True
            # two-cell thicket
            X = 16 + x
            if math.hypot((X - 31.5) / 14.5, (y - 8.0) / 6.4) < 1 and y < 14:
                m[y, X] = True
            X2 = 32 + x
            if math.hypot((X2 - 31.5) / 14.5, (y - 8.0) / 6.4) < 1 and y < 14:
                m[y, X2] = True
            # oleander: taller, looser
            if math.hypot((x - 7.5) / 6.6, (y - 7.0) / 7.0) < 1 and y < 14:
                m[y, 48 + x] = True
    sh = np.zeros_like(m)
    sh[2:, 1:] = m[:-2, :-1]
    for y, x in zip(*np.nonzero(sh & ~m)):
        if y % 16 >= 9:
            M.px(int(x), int(y), "gd" if (x + y) % 2 == 0 else "g1")
    mb = m.copy()
    mb[:, 48:64] = False
    foliage(M, mb, MYRTLE, seed=5, flowers=["rs1", "rs2", "rs1", "rs3"], fl_rate=5)
    mo = np.zeros_like(m)
    mo[:, 48:64] = m[:, 48:64]
    foliage(M, mo, LEAF, seed=8, clump=3.0, flowers=["rs2", "rs3", "rs2"], fl_rate=3)
    # roses: a few big open blooms on the briar
    for (bx, by) in ((3, 4), (9, 7), (5, 9), (18, 5), (25, 8), (37, 4), (42, 9), (30, 3)):
        put(M, bx, by, [".a.", "aba", ".a."], {"a": "rs2", "b": "rs1"})
    # thrift: pink cushions on wiry stems
    for (tx, ty) in ((2, 4), (9, 2), (6, 9), (12, 10), (3, 12)):
        X = 64 + tx
        put(M, X, ty, [".qp.", "qppp", ".pp.", "..1."], {"q": "rs3", "p": "rs2", "1": "my1"})
    # narcissus: white stars with a red-rimmed cup, strappy leaves
    for k, cx in enumerate((5, 6)):
        pts = ((3, 3), (10, 5), (6, 10), (12, 12)) if k == 0 else ((2, 8), (8, 2), (11, 9), (5, 13))
        for (nx, ny) in pts:
            X = cx * 16 + nx
            put(M, X, ny, [".w.", "wrw", ".w.", ".2.", "23."], {"w": "w0", "r": "rs1", "2": "my2",
                                                                "3": "my3"})
    # petals
    for (px_, py_, c) in ((2, 3, "rs2"), (7, 5, "rs3"), (11, 2, "rs1"), (4, 10, "rs2"),
                          (13, 9, "rs3"), (9, 13, "rs2"), (1, 13, "rs1")):
        M.px(112 + px_, py_, c)
        M.px(112 + px_ + 1, py_, c if c != "rs1" else "rs2")
    # basil in a clay pot (pot colors aren't green-group: the pot is drawn in kt*)
    put(M, 112 + 4, 16 + 2, [
        "..3434..",
        ".342343.",
        "34322433",
        ".223322.",
        "..2222..",
        ".kkkkkk.",
        "k222222k",
        ".k2222k.",
        ".kk22kk.",
        "..kkkk..",
        "..gggg..",
    ], {"3": "my3", "4": "my4", "2": "my2", "k": "kt1", "g": "gd"})
    for y in range(16 + 7, 16 + 12):
        for x in range(112 + 5, 112 + 11):
            if M.get(x, y) == "my2":
                M.px(x, y, "kt2")
    return s


# --------------------------------------------------------------------------
# Sea-grass and thrift: Kythera's tall grass, soft-edged
# --------------------------------------------------------------------------

def _seagrass_tex():
    """A 16x16 periodic tuft texture: blades leaning, lit at the tips, dark
    between, with thrift heads."""
    t = {}
    for y in range(16):
        for x in range(16):
            t[(x, y)] = "my2" if (x + 2 * y) % 3 else "my1"
    blades = []
    for i in range(11):
        hh = K.h(i, 3, 17)
        bx = (i * 16) // 11 + hh % 2
        top = hh % 7
        lean = (hh // 7) % 3 - 1
        ln = 7 + (hh // 3) % 5
        tone = ("my3", "my4", "my3", "my3", "my4")[hh % 5]
        blades.append((bx, top, lean, ln, tone))
    for (bx, top, lean, ln, tone) in blades:
        for k in range(ln):
            y = (top + k) % 16
            x = (bx + (lean * (ln - k)) // 4) % 16
            c = tone
            if k == 0:
                c = "my4"
            elif k > ln - 3:
                c = "my2" if k == ln - 1 else ("my3" if tone == "my4" else "my2")
            t[(x, y)] = c
    for (hx, hy) in ((4, 2), (12, 9)):
        for (dx, dy, c) in ((0, 0, "rs3"), (1, 0, "rs2"), (0, 1, "rs2"), (1, 1, "rs1"),
                            (-1, 1, "rs2"), (0, 2, "my2")):
            t[((hx + dx) % 16, (hy + dy) % 16)] = c
    return t


def seagrass():
    from agros_ground import blob_keys, halo, ring, visible
    keys = blob_keys()
    w = 8
    hh = (len(keys) + w - 1) // w
    names = {k: (i % w, i // w) for i, k in enumerate(keys)}
    s = struct("seagrass", "Sea-grass and thrift (tall grass), soft-edged", w, hh, SEC,
               walk=["G" * w] * hh, names=names,
               notes="Kythera's tall grass: blue-green sea-grass with sea-pink thrift, as all 47 soft-"
                     "edge shapes on aethos grass (kythera_lib.blob_key gives a cell's key from a "
                     "mask). `MB_TALL_GRASS` throughout: wild encounters follow the cells while the "
                     "outline stays soft. The full interior is `1|11111111`.")
    B = s.B
    tex_ = _seagrass_tex()

    def paint(ox, oy, key):
        vis, _ = visible(key, margin=1.0, radius=3.0, amp=1.4, seed=5.3, jag=1.2)
        K.tex(B, GRASS, ox, oy, 16, 16)
        for y in range(16):
            for x in range(16):
                if vis[y, x]:
                    B.px(ox + x, oy + y, tex_[((ox + x) % 16, (oy + y) % 16)])
        for y, x in np.argwhere(ring(vis)):
            if B.get(ox + x, oy + y) in ("my3", "my4"):
                continue
            B.px(ox + x, oy + y, "my1")
        for y, x in np.argwhere(halo(vis)):
            if y + 1 < 16 and vis[y + 1, x] and (x * 5 + y * 3) % 4 == 0:
                B.px(ox + x, oy + y, "my3")
                if y - 1 >= 0 and not vis[y - 1, x] and (x + y) % 3 == 0:
                    B.px(ox + x, oy + y - 1, "my4")
    for k, (cx, cy) in names.items():
        paint(cx * 16, cy * 16, k)
    for i in range(len(keys), w * hh):
        paint((i % w) * 16, (i // w) * 16, keys[-1])
    return s


# --------------------------------------------------------------------------
# Trees: the plane, the apple
# --------------------------------------------------------------------------

def trees():
    s = struct("trees", "Plane tree and apple trees", 5, 3, SEC,
               walk=["TTTTT", "XXXXX", "XX.XX"],
               names={"plane": (0, 0), "apple": (3, 0), "apple_gold": (3, 2),
                      "plane_00": (0, 0), "plane_10": (1, 0), "plane_20": (2, 0),
                      "plane_01": (0, 1), "plane_11": (1, 1), "plane_21": (2, 1),
                      "plane_02": (0, 2), "plane_12": (1, 2), "plane_22": (2, 2),
                      "apple_TL": (3, 0), "apple_TR": (4, 0), "apple_BL": (3, 1),
                      "apple_BR": (4, 1), "gold_L": (3, 2), "gold_R": (4, 2)},
               notes="On borrowed grass. The oriental plane (`plane`, 3 wide by 3 tall at its "
                     "top-left): a broad crown of maple-like leaves over a mottled pale trunk, for the "
                     "Neraida ravine and Paphia's square; its crown's top row is drawn over the player. "
                     "The apple (`apple`, 2 by 2): a round crown hung with red apples, for the orchard "
                     "on Paphia's north edge; its top row is over the player too. Plant them with the "
                     "trunk row impassable. `apple_gold` (bottom right, 2 wide by 1) is an apple's "
                     "crown in golden blossom, to swap over an apple's top row.")
    ground(s, "grass")
    s.walk = ["TTTTT", "XXXXX", "XXXXX"]
    s.behaviors = {}
    M, T = s.M, s.T
    # --- the plane: crown 48 x 34, trunk below
    crown = np.zeros((48, 80), bool)
    for y in range(48):
        for x in range(48):
            r = math.hypot((x - 24) / 23.0, (y - 17) / 16.5)
            bump = 0.07 * math.sin(math.atan2(y - 17, x - 24) * 7)
            if r < 1 + bump and y < 36:
                crown[y, x] = True
    # trunk and shadow first (middle layer), crown over them
    for y in range(26, 47):
        for x in range(19, 29):
            half = 3.5 + max(0, y - 40) * 0.6
            if abs(x - 23.5) <= half:
                k = K.h(x, y, 4)
                c = "kt2" if x < 22 else ("kt1" if x > 25 else ("w0" if k % 5 == 0 else "my4"))
                if k % 7 == 0:
                    c = "kt1"
                M.px(x, y, c)
    for y in range(42, 48):
        for x in range(10, 40):
            if math.hypot((x - 25) / 14, (y - 44) / 3.0) < 1 and M.get(x, y) is None:
                M.px(x, y, "gd" if (x + y) % 2 == 0 else "g1")
    tmp = K.Layer(80, 48)
    foliage(tmp, crown, LEAF, seed=11, clump=4.5)
    for y in range(48):
        for x in range(48):
            if tmp.a[y, x, 3]:
                (T if y < 16 else M).px(x, y, tmp.get(x, y))
    # --- the apple: 32 x 26 crown, short trunk
    def apple(ox, oy, gold=False, only_top=False):
        cr = np.zeros((48, 80), bool)
        for y in range(32):
            for x in range(32):
                if math.hypot((x - 16) / 14.5, (y - 12) / 11.5) < 1 + 0.06 * math.sin(math.atan2(y - 12, x - 16) * 6):
                    cr[oy + y, ox + x] = True
        if not only_top:
            for y in range(20, 30):
                for x in range(13, 19):
                    if abs(x - 15.5) <= 1.5 + max(0, y - 26) * 0.7:
                        M.px(ox + x, oy + y, "kt1" if x > 15 else "kt2")
            for y in range(27, 32):
                for x in range(4, 28):
                    if math.hypot((x - 17) / 11, (y - 29) / 2.5) < 1 and M.get(ox + x, oy + y) is None:
                        M.px(ox + x, oy + y, "gd" if (x + y) % 2 == 0 else "g1")
        tmp = K.Layer(80, 48)
        foliage(tmp, cr, LEAF, seed=13 + gold, clump=4.0,
                flowers=["w0", "rs3", "w0"] if gold else None, fl_rate=3)
        if not gold:
            for (ax, ay) in ((6, 6), (13, 4), (22, 7), (9, 13), (18, 12), (25, 15), (13, 18), (6, 17)):
                put(tmp, ox + ax, oy + ay, ["ab", "bc"], {"a": "rs2", "b": "rs1", "c": "kt1"})
        for y in range(48):
            for x in range(80):
                if tmp.a[y, x, 3] and (not only_top or y < oy + 16):
                    (T if y < oy + 16 else M).px(x, y, tmp.get(x, y))
    apple(48, 0)
    # golden blossom crown top, at (3, 2)-(4, 2): drawn as the apple's top row
    gold = K.Layer(80, 48)
    cr = np.zeros((48, 80), bool)
    for y in range(16):
        for x in range(32):
            if math.hypot((x - 16) / 14.5, (y - 12) / 11.5) < 1 + 0.06 * math.sin(math.atan2(y - 12, x - 16) * 6):
                cr[32 + y, 48 + x] = True
    foliage(gold, cr, LEAF, seed=14, clump=4.0, flowers=["w0", "kt2", "w0", "rs3"], fl_rate=2)
    for y in range(32, 48):
        for x in range(48, 80):
            if gold.a[y, x, 3]:
                T.px(x, y, gold.get(x, y))
    s.walk = ["TTTTT", "XXXXX", "XXXTT"]
    for cy, row in enumerate(s.walk):
        for cx, ch in enumerate(row):
            pass
    return s


# --------------------------------------------------------------------------
# The rose-marble quarry and its column drums (the Girdle gate)
# --------------------------------------------------------------------------

def quarry():
    names = {"cut_L": (0, 0), "cut": (1, 0), "cut_R": (2, 0), "face_L": (0, 1), "face": (1, 1),
             "face_R": (2, 1), "step": (3, 0), "step_edge": (3, 1),
             "chips": (4, 0), "chips_grass": (4, 1), "block": (5, 0), "blocks": (5, 1),
             "drum_up": (6, 0), "drum_fallen": (6, 1), "drum_fallen_R": (7, 1), "drag": (7, 0),
             "gate_TL": (0, 2), "gate_TR": (1, 2), "gate_BL": (0, 3), "gate_BR": (1, 3),
             "block_big_TL": (2, 2), "block_big_TR": (3, 2), "block_big_BL": (2, 3),
             "block_big_BR": (3, 3), "face_carved": (4, 2), "cut_carved": (4, 3)}
    walk = ["XXX..X.X", "XXXX.XXX", "XXXXX...", "XXXXX..."]
    s = struct("quarry", "The rose-marble quarry and the column drums", 8, 4, SEC, walk=walk,
               names=names,
               notes="The quarry spur off the Foam Road. Its cut walls: `cut_*` the sawn top edge (on "
                     "borrowed grass) over `face_*`, a face of rose marble squared by the masons, with "
                     "wedge holes; `face_carved` / `cut_carved` show a column half cut from the rock. "
                     "`step` is a cut terrace to stand on (the top step's jar), `step_edge` its lip. "
                     "The floor: `chips` (marble chips on borrowed path) and `chips_grass`. Cut stone: "
                     "`block`, `blocks`, and `block_big_*` (2x2). Column drums: `drum_up`, "
                     "`drum_fallen` + `drum_fallen_R`. The Girdle gate is `gate_*` (2x2): drums fallen "
                     "across the quarry's mouth; when the Girdle of Herakles moves them, swap all four "
                     "cells to `drag` (the floor with the drag marks).")
    M, B = s.M, s.B
    ground(s, "grass", [(0, 0), (1, 0), (2, 0), (4, 1), (4, 3)])
    ground(s, "path", [(4, 0), (5, 0), (6, 0), (7, 0), (5, 1), (6, 1), (7, 1), (3, 0),
                       (0, 2), (1, 2), (0, 3), (1, 3), (2, 2), (3, 2), (2, 3), (3, 3)])
    ground(s, "grass", [(0, 1), (2, 1)])

    def marble_px(X, Y, k=0):
        """Sawn rose marble: smooth white-pink, a few drifting veins (16 px
        periodic; k is ignored, so every face shares its tiles)."""
        x, y = X % 16, Y % 16
        if (x + 2 * y) % 16 in (3,) and y % 8 < 6:
            return "rm3"
        if (2 * x + y) % 23 == 0:
            return "rm4"
        return "rm5"

    # cut edge on grass: a crisp sawn lip
    for cx, end in ((0, "L"), (1, None), (2, "R")):
        ox = cx * 16
        for x in range(16):
            if end == "L" and x < 4:
                continue
            if end == "R" and x > 11:
                continue
            for y in range(11, 16):
                M.px(ox + x, y, "w0" if y == 11 else ("rm4" if y == 12 else marble_px(ox + x, y)))
    # face: two cut benches, each lit along its top, a saw line between blocks,
    # a row of wedge holes where the next block will be split off
    for cx, end in ((0, "L"), (1, None), (2, "R"), (4, "C")):
        ox, oy = cx * 16, 16 if cx != 4 else 32
        tgt = M if end in ("L", "R") else B
        for y in range(16):
            for x in range(16):
                if end == "L" and x < 4:
                    continue
                if end == "R" and x > 11:
                    continue
                X, Y = ox + x, oy + y
                yy = y % 8
                c = marble_px(X, Y)
                if yy == 0:
                    c = "w0"
                elif yy == 7:
                    c = "rm2"
                elif yy == 6:
                    c = "rm4"
                elif (x + 6 * (y // 8)) % 16 == 11:
                    c = "rm3"
                elif (x + 6 * (y // 8)) % 16 == 12:
                    c = "rm4"
                tgt.px(X, Y, c)
        if end == "L":
            for y in range(16):
                tgt.px(ox + 4, oy + y, "rm5")
                tgt.px(ox + 3, oy + y, "rm2")
        if end == "R":
            for y in range(16):
                tgt.px(ox + 11, oy + y, "rm3")
                tgt.px(ox + 12, oy + y, "rm1")
        for wx in (2, 6, 10, 14):
            if (end == "L" and wx < 5) or (end == "R" and wx > 10):
                continue
            tgt.px(ox + wx, oy + 3, "rm1")
    # carved: a column drum half freed from the face
    for (ox, oy, tgt) in ((64, 32, B), (64, 48, M)):
        if tgt is M:
            for x in range(16):
                for y in range(4, 16):
                    M.px(ox + x, oy + y, "w0" if y == 4 else ("rm4" if y == 5 else marble_px(ox + x, oy + y)))
        put(tgt, ox + 3, oy + (1 if tgt is B else 7), [
            "kkkkkkkkkk",
            "k54434453k",
            "k54434453k",
            "k54434453k",
            "k54434453k",
            "k54434453k",
            "kkkkkkkkkk",
        ][: (16 - (1 if tgt is B else 7))], {"k": "rm1", "5": "w0", "4": "rm5", "3": "rm3"})
    # step: a cut terrace (walkable) and its lip
    for y in range(16):
        for x in range(16):
            M.px(48 + x, y, marble_px(48 + x, y, 2) if (x + y) % 11 else "rm4")
    for x in range(16):
        M.px(48 + x, 15, "rm2")
        M.px(48 + x, 14, "rm4")
    for y in range(16):
        for x in range(16):
            B.px(48 + x, 16 + y, marble_px(48 + x, 16 + y, 1))
    for x in range(16):
        B.px(48 + x, 16, "w0")
        B.px(48 + x, 17, "rm4")
        B.px(48 + x, 31, "rm1")
    # chips: marble chips and dust on path and grass
    for (ox, oy) in ((64, 0), (64, 16)):
        for (px_, py_) in ((2, 3), (7, 2), (12, 5), (4, 9), (10, 10), (1, 13), (13, 13), (7, 7)):
            put(M, ox + px_, oy + py_, ["wr", "rk"], {"w": "w0", "r": "rm4", "k": "rm2"})
        for (px_, py_) in ((5, 5), (11, 1), (3, 11), (14, 8), (8, 14)):
            M.px(ox + px_, oy + py_, "rm5")

    def block(ox, oy, w=12, h_=11, lit="w0", top="rm5", side="rm3", dark="rm1"):
        """A squared block: lit top face, front face, shaded right side."""
        tp = 4
        for y in range(h_):
            for x in range(w):
                if y < tp:
                    c = top if x < w - 2 else side
                    if y == 0 or x == 0:
                        c = lit
                elif x >= w - 2:
                    c = dark
                else:
                    c = "rm4" if y == tp else ("rm3" if (x + y) % 7 else "rm2")
                M.px(ox + x, oy + y, c)
        for x in range(w):
            M.px(ox + x, oy + h_ - 1, dark)
        for x in range(1, w + 1):
            if M.get(ox + x, oy + h_) is None:
                M.px(ox + x, oy + h_, "g1" if False else "rm1")
    block(80 + 2, 2)
    block(80 + 1, 16 + 5, w=8, h_=8)
    block(80 + 8, 16 + 2, w=7, h_=7)
    # the big block 2x2
    for y in range(29):
        for x in range(28):
            X, Y = 32 + 2 + x, 32 + 1 + y
            if y < 8:
                c = "w0" if (y == 0 or x == 0) else ("rm5" if x < 26 else "rm3")
            elif x >= 26:
                c = "rm1"
            else:
                c = marble_px(X, Y, 3)
                if y == 8:
                    c = "rm4"
            if y == 28:
                c = "rm1"
            M.px(X, Y, c)
    for (wx, wy) in ((8, 14), (16, 14)):
        put(M, 34 + wx, 33 + wy, ["k", "1"], {"k": "rm0", "1": "rm1"})

    def drum_up(ox, oy):
        """An upright fluted drum: elliptical top, fluted body."""
        for y in range(14):
            for x in range(12):
                X, Y = ox + x, oy + y
                if y < 4:
                    if math.hypot((x - 5.5) / 6, (y - 2) / 2.2) <= 1:
                        M.px(X, Y, "w0" if x < 6 else "rm5")
                else:
                    if y >= 12 and math.hypot((x - 5.5) / 6, (y - 12) / 2.2) > 1:
                        continue
                    c = ("rm4", "rm5", "rm3")[x % 3] if x < 8 else ("rm2" if x % 3 else "rm1")
                    M.px(X, Y, c)
        for x in range(12):
            if M.get(ox + x, oy + 4):
                M.px(ox + x, oy + 4, "rm3")
    drum_up(96 + 2, 1)

    def drum_fallen(ox, oy, length=28):
        """A drum lying east-west: round end facing west (lit), fluted body."""
        for y in range(12):
            for x in range(length):
                X, Y = ox + x, oy + y
                endc = math.hypot((x - 4) / 4.0, (y - 6) / 6.0)
                if x < 4 and endc > 1:
                    continue
                if x >= length - 3 and math.hypot((x - (length - 3)) / 3.0, (y - 6) / 6.0) > 1:
                    continue
                if x < 8 and endc <= 1:
                    c = "rm5" if endc < 0.6 else "rm4"
                    if endc > 0.85:
                        c = "rm2"
                else:
                    c = ("rm5", "rm4", "rm3")[y % 3] if y < 6 else ("rm3", "rm2", "rm1")[y % 3]
                    if y == 0:
                        c = "w0"
                    if y == 11:
                        c = "rm1"
                M.px(X, Y, c)
        put(M, ox + 3, oy + 5, [".1.", "1k1", ".1."], {"1": "rm3", "k": "rm2"})
    drum_fallen(96 + 2, 16 + 2)
    # the gate: two fallen drums and an upright across the quarry mouth
    drum_fallen(0 + 1, 32 + 3, 30)
    drum_fallen(0 + 3, 32 + 17, 27)
    drum_up(16 + 3, 32 + 13)
    for (gx, gy) in ((2, 15), (12, 30), (25, 29)):
        put(M, gx, 32 + gy, ["wr", "rk"], {"w": "w0", "r": "rm4", "k": "rm2"})
    # drag: the path scored with two long ruts and a few chips
    for x in range(16):
        for y in (5, 6, 10, 11):
            if (x + y) % 5:
                M.px(112 + x, y, "rm2" if y in (6, 11) else "rm3")
    put(M, 112 + 3, 13, ["wr", "rk"], {"w": "w0", "r": "rm4", "k": "rm2"})
    s.walk = ["XXX..X.X", "XXXX.XXX", "XXXXX...", "XXXXX..."]
    return s


# --------------------------------------------------------------------------
# Pink-stone terrace walls
# --------------------------------------------------------------------------

def terrace():
    names = {"L": (0, 0), "M": (1, 0), "M2": (2, 0), "R": (3, 0), "steps": (4, 0),
             "niche": (5, 0), "spout": (6, 0), "top_L": (0, 1), "top": (1, 1), "top_R": (3, 1),
             "top_steps": (4, 1), "top_niche": (5, 1), "top_spout": (6, 1), "top_M2": (2, 1)}
    s = struct("terrace", "Pink-stone terrace walls", 7, 2, SEC,
               walk=["XXXX.XX", "....T.."], names=names,
               notes="A retaining wall one cell high between two terraces, in pink rubble with a lit "
                     "coping. Lay a `top_*` row (the upper terrace's edge, walkable, on borrowed grass) "
                     "above a wall row: `L` `M` (`M2`) `R`. `steps` cuts a stair through the wall "
                     "(walkable) under `top_steps`. `niche` is an arched niche with a low plinth, for "
                     "a statue or a votive (Melos's armless goddess stands in one); `spout` is a lion-"
                     "less spring spout dribbling into a trough.")
    M, B = s.M, s.B
    ground(s, "grass", [(x, 1) for x in range(7)] + [(0, 0), (3, 0)])
    for cx, end in ((0, "L"), (1, None), (2, None), (3, "R"), (4, "S"), (5, "N"), (6, "P")):
        ox = cx * 16
        tgt = M if end in ("L", "R") else B
        for y in range(16):
            for x in range(16):
                X = ox + x
                if end == "L" and x < 3:
                    continue
                if end == "R" and x > 12:
                    continue
                c = stone_px(X + 7 * (cx == 2), y)
                if y < 2:
                    c = "rm5" if y == 0 else "rm3"
                tgt.px(X, y, c)
        if end == "L":
            for y in range(16):
                tgt.px(ox + 3, y, "rm4")
        if end == "R":
            for y in range(16):
                tgt.px(ox + 12, y, "rm1")
    # steps through the wall
    for i, y in enumerate(range(0, 16, 4)):
        for x in range(2, 14):
            B.px(64 + x, y, "rm5")
            B.px(64 + x, y + 1, "rm4")
            B.px(64 + x, y + 2, "rm3")
            B.px(64 + x, y + 3, "rm1")
        for yy in range(y, y + 4):
            B.px(64 + 1, yy, "rm1")
            B.px(64 + 14, yy, "rm1")
    # niche with plinth
    put(B, 80 + 3, 2, [
        "...1111...",
        "..122221..",
        ".12000021.",
        "1200000021",
        "1200000021",
        "1200000021",
        "1200000021",
        "1201111021",
        "1214444121",
        "1213333121",
        "1213333121",
        "1211111121",
        "1111111111",
    ], {"1": "rm1", "2": "rm2", "0": "rm0", "4": "w0", "3": "rm5"})
    # spout and trough
    put(B, 96 + 6, 3, ["1111", "1001", ".11."], {"1": "rm1", "0": "cv0"})
    for y in range(6, 10):
        B.px(96 + 7 + (y % 2), y, "w0")
    put(B, 96 + 2, 9, [
        "111111111111",
        "155555555551",
        "152222222251",
        "111111111111",
    ], {"1": "rm1", "5": "rm5", "2": "my2"})
    # the upper terrace's edge: a coping line at the bottom of each top cell
    for cx in range(7):
        ox = cx * 16
        for x in range(16):
            if cx == 0 and x < 3:
                continue
            if cx == 3 and x > 12:
                continue
            if cx == 4 and 2 <= x <= 13:
                continue
            M.px(ox + x, 14, "rm4")
            M.px(ox + x, 15, "rm5")
            if (x * 3 + cx) % 7 == 0:
                M.px(ox + x, 13, "my3")
        if cx == 4:
            for x in range(2, 14):
                M.px(ox + x, 15, "rm5")
                M.px(ox + x, 14, "rm4")
                M.px(ox + x, 13, "rm3" if x in (2, 13) else "rm4")
    return s


def build():
    h = hedge()
    q = quarry()
    f = flowers()
    return [
        K.pick(h, ["L", "M", "M2", "R", "single", "bush", "gap_stair", "T", "V", "B", "NW", "NE",
                   "SW", "SE"], w=7,
               notes="Dense, glossy myrtle starred with white flowers, Aphrodite's shrub: the ridge "
                     "along the Foam Road and the glade round the spring. Runs east-west: `L` `M` "
                     "(`M2` breaks up a long run) `R`; north-south: `T` `V` `B`; turns: `NW` `NE` "
                     "`SW` `SE` (named by the corner of the hedge they make). `single` stands alone, "
                     "`bush` is a smaller round one. `gap_stair` is the run broken by rough steps (the "
                     "stair up to the spring: walkable). All on borrowed grass; impassable except the "
                     "stair."),
        K.pick(f, ["briar", "briar_L", "briar_R", "oleander", "thrift", "narcissus", "narcissus_b",
                   "petals"],
               notes="On borrowed grass. `briar` is a wild rose bush; `briar_L` `briar_R` a two-cell "
                     "thicket. `oleander` is the ravine's pink-flowered shrub. Walkable decorations: "
                     "`thrift`, sea-pink cushions; `narcissus` and `narcissus_b`, the white flower of "
                     "the spring (ring Kallirhoe's pool with them); `petals`, rose petals blown on the "
                     "grass."),
        seagrass(),
        trees(),
        K.pick(q, ["cut_L", "cut", "cut_R", "step", "chips", "block", "gate_TL", "gate_TR",
                   "face_L", "face", "face_R", "step_edge", "chips_grass", "blocks", "gate_BL",
                   "gate_BR", "drum_up", "drum_fallen", "drum_fallen_R", "drag", "face_carved"], w=8,
               notes="The quarry spur off the Foam Road. Its cut walls: `cut_*`, the sawn top edge (on "
                     "borrowed grass), over `face_*`, benches of rose marble squared by the masons, "
                     "with a row of wedge holes; `face_carved` shows a column drum half cut from the "
                     "rock. `step` is a cut terrace to stand on (the top step's jar), `step_edge` its "
                     "lip below. The floor: `chips` (marble chips on borrowed path) and `chips_grass`. "
                     "Cut stone: `block`, `blocks`. Column drums: `drum_up`, and `drum_fallen` + "
                     "`drum_fallen_R` lying east-west. The Girdle gate is `gate_TL` `gate_TR` over "
                     "`gate_BL` `gate_BR`: drums fallen across the quarry's mouth; when the Girdle of "
                     "Herakles moves them, swap all four cells to `drag`, the path scored with drag "
                     "marks."),
        terrace(),
    ]
