"""Kythera's coast: the foam-edged surf, white sand's foam lace and shells,
shingle, tide rocks and reef spits, Aphrodite's rock, the low pink sea-cliffs,
Melos's pumice cliffs, and the sea marks of Routes 22 and 23.

The surf is an overlay on aethos's animated sea: each surf cell borrows the
sea for its bottom layer and draws, in its middle layer, the sand down to the
waterline, a rim of turquoise shallows, and the foam, which washes up and back
over three frames (the "surf" animation). The sand is aethos's own sand, pixel
for pixel, so a surf cell meets plain aethos sand (0x124) without a seam.

Waterlines are signed distance fields in cell-local pixels (positive = sand),
wobbled by a 16 px periodic swell, so any edge meets any corner.
"""
from __future__ import annotations

import math

import numpy as np

import kythera_lib as K
from kythera_lib import anim_layer, ground, put, struct

SEC = "coast"
SAND = 0x124

# --------------------------------------------------------------------------
# Waterlines
# --------------------------------------------------------------------------


def wob(t, k=0):
    t = t % 16
    w = 1.0 * math.sin(2 * math.pi * t / 16 + 0.4) + 0.5 * math.sin(4 * math.pi * t / 16 + 1.3)
    if k:
        w += k * math.sin(math.pi * t / 16)
    return w


def inter(a, b, r=4.0):
    if a < r and b < r:
        return r - math.hypot(max(r - a, 0), max(r - b, 0))
    return min(a, b)


def union(a, b, r=4.0):
    return -inter(-a, -b, r)


def sd_S(x, y, k=0):
    return 7 + wob(x, k) - y


def sd_N(x, y, k=0):
    return y - (8 - wob(x + 5, k))


def sd_E(x, y, k=0):
    return 7 + wob(y + 3, k) - x


def sd_W(x, y, k=0):
    return x - (8 - wob(y + 9, k))


SHORES = {
    # name: (signed distance, where the sea is)
    "S": (lambda x, y: sd_S(x, y), "sea to the south"),
    "S2": (lambda x, y: sd_S(x, y, 2.0), "sea to the south, a deeper bite"),
    "N": (lambda x, y: sd_N(x, y), "sea to the north"),
    "E": (lambda x, y: sd_E(x, y), "sea to the east"),
    "W": (lambda x, y: sd_W(x, y), "sea to the west"),
    "out_NW": (lambda x, y: inter(sd_S(x, y), sd_E(x, y)), "sand's south-east tip: sand to the north-west"),
    "out_NE": (lambda x, y: inter(sd_S(x, y), sd_W(x, y)), "sand's south-west tip: sand to the north-east"),
    "out_SW": (lambda x, y: inter(sd_N(x, y), sd_E(x, y)), "sand's north-east tip: sand to the south-west"),
    "out_SE": (lambda x, y: inter(sd_N(x, y), sd_W(x, y)), "sand's north-west tip: sand to the south-east"),
    "in_SE": (lambda x, y: union(sd_S(x, y), sd_E(x, y)), "a cove's corner: sea only to the south-east"),
    "in_SW": (lambda x, y: union(sd_S(x, y), sd_W(x, y)), "a cove's corner: sea only to the south-west"),
    "in_NE": (lambda x, y: union(sd_N(x, y), sd_E(x, y)), "a cove's corner: sea only to the north-east"),
    "in_NW": (lambda x, y: union(sd_N(x, y), sd_W(x, y)), "a cove's corner: sea only to the north-west"),
}

FRONT = (0.6, -1.4, 1.8)    # the wave's leading edge per frame, in sd units


def sand_px(X, Y):
    """aethos sand at absolute pixel (X, Y), as a color name."""
    rgb = tuple(int(v) for v in K.aethos(SAND)[Y % 16, X % 16])
    return K.A.RGB2NAME[rgb]


def bubbles(X, Y, f):
    """Foam lace: a 16 px periodic froth of bubbles, drifting per frame."""
    x, y = (X + 3 * f) % 16, (Y + (f * 5) // 2) % 16
    v = (x * 5 + y * 7 + (x * y) % 5) % 13
    return v in (0, 3, 4, 8) or ((x + 2 * y) % 7 == 0)


def water_px(d, X, Y, f):
    """The overlay's color at signed distance d (sand > 0) in frame f, or None
    for open sea (the borrowed water shows)."""
    F = FRONT[f]
    if d > F:
        if d > 2.6:
            return sand_px(X, Y)
        if d > 0.0:
            # wet sand darkens toward the water, flecked with drying foam
            if d > 1.9 and K.hp(X, Y, 3) % 2:
                return "ks2"
            return "w0" if K.hp(X, Y, 7) % 23 == 0 else "ks1"
        return "kq1" if d > -3.2 else ("b3" if (X + Y) % 2 else "kq1")
    if d > F - 1.1:
        return "w0"
    if d > F - 4.2:
        if bubbles(X, Y, f):
            return "w0" if d > F - 2.6 else "kq2"
        if d > -3.6:
            return "kq2" if (X + Y + f) % 3 == 0 else "kq1"
        return "kq2" if (X * 3 + Y) % 5 == 0 else None
    if d > -3.6:
        return "kq1"
    if d > -4.6:
        return "b3" if (X + 2 * Y) % 3 == 0 else None
    return None


def paint_shore(s, frames, cx, cy, sd):
    for f, L in enumerate([s.M] + frames):
        for y in range(16):
            for x in range(16):
                X, Y = cx * 16 + x, cy * 16 + y
                c = water_px(sd(x, y), X, Y, f)
                if c:
                    L.px(X, Y, c)


def surf():
    names = list(SHORES)
    w = 8
    hh = (len(names) + w - 1) // w
    cells = {n: (i % w, i // w) for i, n in enumerate(names)}
    walk = []
    for j in range(hh):
        walk.append("".join("W" for _ in range(w)))
    s = struct("surf", "Foam-edged surf", w, hh, SEC, walk=walk, names=cells,
               notes="Where Kythera's sand meets the sea. Each cell borrows aethos's animated sea and "
                     "draws the sand to the waterline, a rim of turquoise shallows and the foam, which "
                     "washes up and back (the `surf` animation, 3 frames). Pieces are named by where the "
                     "sea is: `S` (sand north, sea south; `S2` is the same with a deeper bite, to break "
                     "up a long beach), `N`, `E`, `W`; `out_NW` is the south-east tip of a sand spit "
                     "(sand to the north-west, sea round it), and so on; `in_SE` is a cove's corner, sea "
                     "only to the south-east. The sand above meets aethos sand (0x124) exactly; the sea "
                     "below meets aethos sea (0x170). Every cell is `MB_OCEAN_WATER`, like aethos's own "
                     "beach edges: surf onto it, walk on the sand beside it.")
    ground(s, "sea")
    frames = anim_layer(s, "surf", 3)
    for n, (cx, cy) in cells.items():
        paint_shore(s, frames, cx, cy, SHORES[n][0])
    # unused tail cells repeat S
    for i in range(len(names), w * hh):
        paint_shore(s, frames, i % w, i // w, SHORES["S"][0])
    return s


# --------------------------------------------------------------------------
# White sand: foam lace, shells, wrack, a big scallop, shingle
# --------------------------------------------------------------------------

def sand_decor():
    names = {"lace": (0, 0), "lace_b": (1, 0), "shells": (2, 0), "scallop": (3, 0),
             "wrack": (4, 0), "pebbles": (5, 0), "footprints": (6, 0), "sherd_dig": (7, 0)}
    s = struct("sand_decor", "White sand: foam lace, shells and wrack", 8, 1, SEC,
               walk=["........"], names=names,
               notes="Decorations on borrowed aethos sand, all walkable: `lace` and `lace_b`, lines of "
                     "dried foam the tide left (lay them in a row a cell or two above the surf); `shells`, "
                     "scattered cockles; `scallop`, one great scallop shell, Aphrodite's sign; `wrack`, a "
                     "line of dried sea-grass; `pebbles`; `footprints`, someone walked here; `sherd_dig`, "
                     "turned earth above the tide line (Alethea's dig spot).")
    ground(s, "sand")
    M = s.M
    # foam lace: a wavy line of white froth, 16 px periodic
    for k, (cx, cy) in enumerate([(0, 0), (1, 0)]):
        for x in range(16):
            X = cx * 16 + x
            yc = 8 + wob(x + 7 * k, 1.0 + k) * 1.4
            for y in range(16):
                d = abs(y - yc)
                Y = cy * 16 + y
                if d < 0.8:
                    M.px(X, Y, "w0")
                elif d < 2.2 and bubbles(X, Y, k):
                    M.px(X, Y, "w0" if y < yc else "kq2")
                elif 2.2 <= d < 3.0 and (x + y + k) % 5 == 0:
                    M.px(X, Y, "p3")
    # shells: cockles and a few tiny scallops
    for (x, y, kind) in ((2, 3, 0), (10, 2, 1), (6, 8, 0), (12, 10, 2), (3, 12, 1), (9, 13, 0)):
        X, Y = 2 * 16 + x, y
        if kind == 0:
            put(M, X, Y, [".wh.", "wpph", ".hh."], {"w": "w0", "p": "kr3", "h": "ks1"})
        elif kind == 1:
            put(M, X, Y, ["w.w", "wpw", ".h."], {"w": "w0", "p": "kq2", "h": "ks1"})
        else:
            put(M, X, Y, [".hh", "hww"], {"h": "kr2", "w": "kr3"})
    # the great scallop: ribbed fan, its hinge to the south
    put(M, 3 * 16 + 1, 1, [
        "....kkkkkk....",
        "..kkwpwpwpkk..",
        ".kwpwpwpwpwpk.",
        ".kpwpwpwpwpwk.",
        "kwpwpwpwpwpwpk",
        "kpwpwpwpwpwpwk",
        "kwpwpwpwpwpwpk",
        ".kpwpwpwpwpwk.",
        ".kkpwpwpwpwkk.",
        "...kkpwpwkk...",
        ".....kwwk.....",
        "....kkqqkk....",
        "....hkkkkh....",
    ], {"k": "kr1", "w": "w0", "p": "kr3", "q": "kq2", "h": "ks1"})
    for X in range(3 * 16 + 1, 3 * 16 + 15):
        for Y in range(13, 15):
            if M.get(X, Y - 1) in ("kr1", "kr3", "w0") and M.get(X, Y) is None and (X + Y) % 2:
                M.px(X, Y, "ks1")
    # wrack: a tangled line of dried sea-grass and a stick
    for x in range(16):
        X = 4 * 16 + x
        yc = 9 + wob(x + 3, 1.2)
        for y in range(16):
            if abs(y - yc) < 0.7:
                M.px(X, y, "l1" if (x * 3 + y) % 4 else "kr1")
            elif abs(y - yc) < 1.6 and (x + y) % 3 == 0:
                M.px(X, y, "ks1")
    M.line(4 * 16 + 3, 6, 4 * 16 + 9, 5, "l1")
    # pebbles
    for (x, y, c) in ((2, 2, "kr2"), (7, 4, "kr1"), (11, 3, "kr3"), (4, 9, "kr3"), (9, 10, "kr2"),
                      (13, 12, "kr1"), (1, 13, "kr2"), (6, 13, "kr3")):
        X = 5 * 16 + x
        put(M, X, y, ["ab", "bc"], {"a": "w0" if c == "kr3" else "kr3", "b": c, "c": "kr0"})
        M.px(X + 2, y + 1, "ks1")
    # footprints, walking north
    for (x, y) in ((4, 12), (9, 8), (4, 4), (9, 0)):
        put(M, 6 * 16 + x, y, [".k.", "kkk", "kkk", ".k."], {"k": "ks1"})
    # dig spot: turned earth, a trowel scrape
    put(M, 7 * 16 + 2, 3, [
        "...hhhhh...",
        ".hhlllllhh.",
        "hllwlllwllh",
        "hlllkllllll",
        "hllllkllwlh",
        ".hlllllllh.",
        "...hhhhh...",
    ], {"h": "ks1", "l": "l1", "w": "ks2", "k": "kr0"})
    return s


def shingle():
    """Shingle: rounded grey and white pebbles over the sand, soft-edged."""
    from agros_ground import blob_keys, halo, visible
    keys = blob_keys()
    w = 8
    hh = (len(keys) + w - 1) // w
    names = {k: (i % w, i // w) for i, k in enumerate(keys)}
    s = struct("shingle", "Shingle beach, soft-edged", w, hh, SEC, walk=["." * w] * hh, names=names,
               notes="Pebble beach over borrowed aethos sand, as all 47 soft-edge shapes "
                     "(kythera_lib.blob_key gives a cell's key from a mask). Walkable. The full "
                     "interior is `1|11111111`. Keep a cell or two of plain sand between shingle and "
                     "the surf.")
    ground(s, "sand")
    M = s.M
    # a 16 px periodic field of pebbles, each lit top-left with a shadow on the sand
    field = {}
    peb = [  # (x, y, rows)
        (1, 0, [".w33.", "w3332", "33221", ".110."]),
        (8, 1, [".32.", "3221", ".11."]),
        (12, 4, [".21.", "2110", "1100", ".00."]),
        (3, 6, [".ww3.", "ww332", "w3322", ".221."]),
        (9, 7, ["w3.", "332", ".21"]),
        (0, 11, [".32.", "3321", "2211", ".10."]),
        (6, 12, [".w33.", "w3332", "32221", ".111."]),
        (13, 11, [".2.", "221", ".1."]),
    ]
    tone = {"w": "w0", "3": "kr3", "2": "kr2", "1": "kr1", "0": "kr0"}
    for n, (px_, py_, rows) in enumerate(peb):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in tone:
                    field[((px_ + i) % 16, (py_ + j) % 16)] = (tone[ch], n, i, j)
        # contact shadow below-right
        for i in range(1, len(rows[0]) + 1):
            q = ((px_ + i) % 16, (py_ + len(rows)) % 16)
            if q not in field:
                field[q] = ("ks1", n, i, len(rows))
    centers = [(px_ + len(rows[0]) / 2, py_ + len(rows) / 2) for (px_, py_, rows) in peb]

    def pebble_at(x, y, vis):
        """The pebble color at cell pixel (x, y), drawn only if its whole
        pebble's center (in this cell's frame) falls in the visible mask."""
        e = field.get((x % 16, y % 16))
        if not e:
            return None
        c, n, i, j = e
        px_, py_, rows = peb[n]
        # the pebble's origin in this cell's frame: the copy that contains (x, y)
        ox_ = x - i
        oy_ = y - j
        cx_ = min(15, max(0, int(ox_ + len(rows[0]) / 2)))
        cy_ = min(15, max(0, int(oy_ + len(rows) / 2)))
        return c if vis[cy_, cx_] else None

    def paint(ox, oy, key):
        vis, _ = visible(key, margin=1.0, radius=3.0, amp=1.6, seed=4.1, jag=0.8)
        for y in range(16):
            for x in range(16):
                c = pebble_at(x, y, vis)
                if c:
                    M.px(ox + x, oy + y, c)
    for k, (cx, cy) in names.items():
        paint(cx * 16, cy * 16, k)
    for i in range(len(keys), w * hh):
        paint((i % w) * 16, (i // w) * 16, keys[-1])
    return s


# --------------------------------------------------------------------------
# White rocks: tide rocks, a reef spit, rocks on the sand
# --------------------------------------------------------------------------

def rock_blob(L, ox, oy, pts, outline="kr0", shade=(("kr3", "kr2"), "kr1"), seed=0):
    """Fill a polygon with lit white rock: top-left facets lit, fissures."""
    sub = K.Layer(L.w, L.h)
    sub.poly([(ox + x, oy + y) for x, y in pts], "kr2")
    ys, xs = np.nonzero(sub.a[..., 3] > 0)
    if not len(xs):
        return
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    for y, x in zip(ys, xs):
        u = (x - x0) / max(1, x1 - x0)
        v = (y - y0) / max(1, y1 - y0)
        k = K.h(x, y, seed)
        if u + v < 0.55:
            c = "w0" if k % 5 else "kr3"
        elif u + v < 1.05:
            c = "kr3" if k % 4 else "kr2"
        elif u + v < 1.45:
            c = "kr2" if k % 5 else "kr1"
        else:
            c = "kr1"
        L.px(int(x), int(y), c)
    # a fissure or two
    for (fx, fy, fl) in ((0.45, 0.25, 4), (0.7, 0.55, 3)):
        x = int(x0 + fx * (x1 - x0))
        y = int(y0 + fy * (y1 - y0))
        for i in range(fl):
            if sub.a[y + i, x + (i // 2), 3]:
                L.px(x + (i // 2), y + i, "kr1")
    sub.outline("kr2")
    ys, xs = np.nonzero(sub.a[..., 3] > 0)
    edge = {(int(x), int(y)) for y, x in zip(ys, xs) if sub.get(int(x), int(y)) == "kr2"
            and L.get(int(x), int(y)) is not None}
    full = K.Layer(L.w, L.h)
    full.poly([(ox + x, oy + y) for x, y in pts], "kr2")
    full.outline(outline)
    for y, x in zip(*np.nonzero(full.a[..., 3] > 0)):
        if full.get(int(x), int(y)) == outline:
            L.px(int(x), int(y), outline)
    return edge


def foam_ring(frames_all, X0, Y0, w, h_, mask, width=(2, 3, 2), lace=True, pale="kq2"):
    """Animated foam round a shape: frames_all = [layer frame0, frame1, frame2];
    mask(x, y) -> True inside the shape (absolute px). The ring breathes.
    `pale` is the foam's shadow color (kq2 in the foam group, mw2 on pink
    stone)."""
    for f, L in enumerate(frames_all):
        wd = width[f % len(width)]
        for Y in range(Y0, Y0 + h_):
            for X in range(X0, X0 + w):
                if mask(X, Y) or L.get(X, Y) not in (None, "kq1", "kq2", "w0", "b3", "mw2"):
                    continue
                # distance to the shape (cheap: search a small box)
                dmin = 99
                for dy in range(-wd - 1, wd + 2):
                    for dx in range(-wd - 1, wd + 2):
                        if mask(X + dx, Y + dy):
                            dmin = min(dmin, math.hypot(dx, dy))
                if dmin <= 1.0:
                    L.px(X, Y, "w0")
                elif dmin <= wd + 0.5:
                    L.px(X, Y, "w0" if bubbles(X, Y, f) else pale)
                elif dmin <= wd + 1.6 and lace and (X * 3 + Y * 5 + f) % 4 == 0:
                    L.px(X, Y, pale)


def tide_rocks():
    names = {"tide_rock": (0, 0), "tide_rocks": (1, 0), "spit_W": (2, 0), "spit_M": (3, 0),
             "spit_E": (4, 0), "spit_head": (5, 0), "spit_N": (6, 0), "spit_S": (7, 0),
             "spit_V": (6, 1), "rock_sand": (0, 1), "rocks_sand": (1, 1), "rock_grass": (2, 1),
             "stake": (3, 1), "stakes": (4, 1), "sunken_column": (5, 1), "sunken_drum": (7, 1)}
    walk = ["XX......", "XXXXXX.W"]
    s = struct("rocks", "Tide rocks, a reef spit, white rocks, sea marks", 8, 2, SEC, walk=walk,
               names=names,
               notes="White rock in the sea and on land. `tide_rock` and `tide_rocks` stand in the "
                     "surf with breathing foam (animated). The reef spit is a walkable path of flat, "
                     "wet rock out into the sea at low tide (the diver's spit on the Foam Road): "
                     "`spit_W` `spit_M` `spit_E` run east-west, `spit_N` `spit_V` `spit_S` north-"
                     "south, `spit_head` is a broad flat rock to stand on at the end. `rock_sand` "
                     "and `rocks_sand` sit on sand, `rock_grass` on grass. `stake` and `stakes` mark "
                     "the trireme lane (Routes 22 and 23); `sunken_column` is a fallen column's "
                     "capital awash (Route 23), `sunken_drum` a drum under the turquoise shallows "
                     "(surfable).")
    sea_cells = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (6, 1), (3, 1),
                 (4, 1), (5, 1)]
    ground(s, "sea", sea_cells)
    ground(s, "sand", [(0, 1), (1, 1)])
    ground(s, "grass", [(2, 1)])
    ground(s, "shallow", [(7, 1)])
    M = s.M
    frames = anim_layer(s, "surf", 3)
    allf = [M] + frames
    # tide rocks
    shapes = {
        (0, 0): [[(4, 5), (7, 2), (11, 3), (13, 7), (12, 11), (8, 12), (4, 11), (3, 8)]],
        (1, 0): [[(1, 4), (4, 2), (7, 4), (7, 8), (4, 9), (1, 8)],
                 [(8, 8), (11, 6), (14, 8), (14, 12), (11, 13), (8, 12)]],
    }
    for (cx, cy), polys in shapes.items():
        sub = K.Layer(M.w, M.h)
        for p in polys:
            for L in allf:
                rock_blob(L, cx * 16, cy * 16, p, seed=cx)
            sub.poly([(cx * 16 + x, cy * 16 + y) for x, y in p], "kr2")
        foam_ring(allf, cx * 16, cy * 16, 16, 16, lambda X, Y, sub=sub: sub.get(X, Y) is not None)
    # the reef spit: flat wet rock, a few pools, foam along its flanks
    spit = K.Layer(M.w, M.h)

    def spit_cell(cx, cy, kind):
        ox, oy = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                if kind == "h":
                    inside = 3 + wob(x, 0.6) * 0.6 <= y <= 12 + wob(x + 6) * 0.6
                elif kind == "v":
                    inside = 3 + wob(y + 2) * 0.6 <= x <= 12 + wob(y + 9) * 0.6
                elif kind == "W":
                    inside = (3 + wob(x) * 0.6 <= y <= 12 + wob(x + 6) * 0.6) and \
                        math.hypot(max(0, 7 - x), max(0, abs(y - 7.5) - 2)) < 5.5
                elif kind == "E":
                    inside = (3 + wob(x) * 0.6 <= y <= 12 + wob(x + 6) * 0.6) and \
                        math.hypot(max(0, x - 8), max(0, abs(y - 7.5) - 2)) < 5.5
                elif kind == "N":
                    inside = (3 + wob(y + 2) * 0.6 <= x <= 12 + wob(y + 9) * 0.6) and \
                        math.hypot(max(0, 7 - y), max(0, abs(x - 7.5) - 2)) < 5.5
                elif kind == "S":
                    inside = (3 + wob(y + 2) * 0.6 <= x <= 12 + wob(y + 9) * 0.6) and \
                        math.hypot(max(0, y - 8), max(0, abs(x - 7.5) - 2)) < 5.5
                else:  # head: a broad round slab
                    inside = math.hypot(x - 7.5, y - 7.5) < 7.2 + wob(x + y) * 0.5
                if inside:
                    spit.px(ox + x, oy + y, "kr2")
    for (cx, cy), kind in (((2, 0), "W"), ((3, 0), "h"), ((4, 0), "E"), ((5, 0), "head"),
                           ((6, 0), "N"), ((6, 1), "v"), ((7, 0), "S")):
        spit_cell(cx, cy, kind)
    ys, xs = np.nonzero(spit.a[..., 3] > 0)
    for y, x in zip(ys, xs):
        k = K.h(int(x), int(y), 5)
        up = spit.get(int(x), int(y) - 1) is None
        left = spit.get(int(x) - 1, int(y)) is None
        down = spit.get(int(x), int(y) + 1) is None
        right = spit.get(int(x) + 1, int(y)) is None
        if up or left:
            c = "kr3"
        elif down or right:
            c = "kr0" if down else "kr1"
        else:
            c = "kr2" if k % 7 else "kr3"
            if k % 29 == 0:
                c = "kq1"
        for L in allf:
            L.px(int(x), int(y), c)
    # rock pools on the head and a weed fringe
    for L in allf:
        put(L, 5 * 16 + 4, 5, [".kk.", "kqqk", "kqbk", ".kk."], {"k": "kr1", "q": "kq1", "b": "b3"})
        put(L, 5 * 16 + 10, 9, ["kk", "qk"], {"k": "kr1", "q": "kq1"})
    foam_ring(allf, 2 * 16, 0, 6 * 16, 32, lambda X, Y: spit.get(X, Y) is not None,
              width=(1, 2, 1))
    # rocks on sand and grass: white boulders with a contact shadow
    for (cx, cy, polys, gshade) in (
            (0, 1, [[(3, 6), (6, 3), (10, 3), (13, 6), (13, 11), (9, 13), (4, 12), (3, 9)]], "ks1"),
            (1, 1, [[(1, 7), (3, 4), (7, 5), (8, 9), (5, 12), (2, 11)],
                    [(8, 9), (11, 6), (14, 8), (15, 12), (12, 14), (9, 13)]], "ks1"),
            (2, 1, [[(3, 6), (6, 3), (11, 4), (13, 8), (12, 12), (7, 13), (3, 11)]], None)):
        for p in polys:
            sh = [(x + 1, y + 2) for x, y in p]
            if gshade:
                M.poly([(cx * 16 + x, cy * 16 + y) for x, y in sh], gshade)
            rock_blob(M, cx * 16, cy * 16, p, seed=cy)
    # rock on grass: green-group-free shadow using the rock's own dark tone
    # stakes: weathered posts in the sea with a little foam
    for (cx, posts) in ((3, [(7, 2)]), (4, [(3, 3), (10, 6)])):
        sub = K.Layer(M.w, M.h)
        for (px_, py_) in posts:
            X, Y = cx * 16 + px_, 16 + py_
            for L in allf:
                put(L, X, Y, ["kwk", "kwk", "kwk", "kwk", "kwk", "kwk", "kwk", ".k."],
                    {"k": "kr0", "w": "kr2"})
                L.px(X + 1, Y, "kr3")
            sub.rect(X, Y + 5, 3, 3, "kr0")
        foam_ring(allf, cx * 16, 16, 16, 16, lambda X, Y, sub=sub: sub.get(X, Y) is not None,
                  width=(1, 1, 2), lace=False)
    # a sunken Ionic capital awash: marble scrolls in the surf
    sub = K.Layer(M.w, M.h)
    for L in allf:
        put(L, 5 * 16 + 1, 16 + 4, [
            ".kkkkkkkkkkkk.",
            "kwwwwwwwwwwwwk",
            "kwkkw3333wkkwk",
            "k3wk3333333wk3",
            "kk3k22222223kk",
            ".kk.k22222k.kk",
            "....k22222k...",
            "....k21212k...",
        ], {"k": "kr0", "w": "w0", "3": "kr3", "2": "kr2", "1": "kr1"})
    sub.rect(5 * 16 + 1, 16 + 4, 14, 6, "kr0")
    sub.rect(5 * 16 + 5, 16 + 10, 7, 2, "kr0")
    foam_ring(allf, 5 * 16, 16, 16, 16, lambda X, Y: sub.get(X, Y) is not None, width=(1, 2, 1))
    # a column drum seen through the shallows: pale shape, no foam
    put(M, 7 * 16 + 3, 16 + 3, [
        "..kkkkkk..",
        ".k222222k.",
        "k22222222k",
        "k22222222k",
        "k22222222k",
        "k22222222k",
        ".k222222k.",
        "..kkkkkk..",
    ], {"k": "kq1", "2": "kq2"})
    put(M, 7 * 16 + 5, 16 + 5, ["2.2.2", ".2.2.", "2.2.2"], {"2": "b4"})
    K.settle(s, "surf", [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (6, 1),
                         (3, 1), (4, 1), (5, 1)])
    return s


# --------------------------------------------------------------------------
# Aphrodite's rock: a great white stack in the shallows, its foam collar
# --------------------------------------------------------------------------

def _stack_rows():
    """Left and right edges per row of the great stack and its companion."""
    main = {}
    prof = [(2, 17, 27), (4, 13, 31), (7, 10, 33), (11, 8, 35), (16, 6, 36), (22, 5, 37),
            (28, 4, 38), (34, 3, 38), (40, 2, 39), (46, 3, 38)]
    for y in range(2, 47):
        for (y0, l0, r0), (y1, l1, r1) in zip(prof, prof[1:]):
            if y0 <= y <= y1:
                f = (y - y0) / (y1 - y0)
                l = l0 + (l1 - l0) * f + 0.8 * math.sin(y * 0.9)
                r = r0 + (r1 - r0) * f + 0.8 * math.sin(y * 0.7 + 2)
                main[y] = (int(round(l)), int(round(r)))
                break
    # the shoulder notch on the right, where a slab fell away
    for y in range(13, 18):
        l, r = main[y]
        main[y] = (l, r - (3 - abs(y - 15)))
    comp = {}
    for y in range(30, 47):
        f = (y - 30) / 16
        comp[y] = (int(round(36 - 3 * f)), int(round(44 + 2 * min(1, f * 2))))
    return main, comp


def aphrodite_rock():
    s = struct("aphrodite_rock", "Aphrodite's rock", 3, 3, SEC, walk=["XXX", "XXX", "XXX"],
               names={"peak": (1, 0), "foot": (1, 2)},
               notes="The great white rock in the shallows where the goddess came ashore on the foam "
                     "(the Foam Road's set piece, beat III-1D). It borrows aethos's sea; its collar "
                     "of foam never quite goes away (the `surf` animation). Impassable. Put sea round "
                     "it on every side; the beach and Alethea's dig spot sit north of it.")
    ground(s, "sea")
    M = s.M
    frames = anim_layer(s, "surf", 3)
    allf = [M] + frames
    main, comp = _stack_rows()
    shape = K.Layer(48, 48)

    def paint_mass(rows, top_fn, seed):
        for y, (l, r) in rows.items():
            for x in range(l, r + 1):
                shape.px(x, y, "kr2")
                u = (x - l) / max(1, r - l)
                k = K.h(x, y, seed)
                if y < top_fn(x):
                    # the stack's weathered top, catching the sun
                    c = "w0" if (u < 0.7 and k % 5) else "kr3"
                    if y == top_fn(x) - 1:
                        c = "kr3" if u < 0.6 else "kr2"
                elif u < 0.12:
                    c = "w0" if k % 3 else "kr3"
                elif u < 0.45:
                    c = "kr3" if (x % 4 or k % 3 == 0) else "kr2"
                elif u < 0.78:
                    c = "kr2" if (x % 4 != 1) else "kr1"
                else:
                    c = "kr1" if k % 4 else "kr2"
                if y > 41:
                    c = "kr1" if c in ("w0", "kr3", "kr2") and k % 3 else "kr0"
                for L in allf:
                    L.px(x, y, c)
    paint_mass(main, lambda x: 12 + int(round(2.2 * math.sin((x - 4) / 34 * math.pi))), 9)
    paint_mass(comp, lambda x: 34, 13)
    for L in allf:
        # ledges, a fissure, the separation of the two rocks
        for x in range(7, 34):
            y = 25 + int(round(math.sin(x / 5)))
            if shape.get(x, y) and L.get(x, y) in ("kr3", "kr2", "w0"):
                L.px(x, y, "kr1")
                L.px(x, y - 1, "w0" if x < 20 else "kr3")
        L.line(24, 13, 22, 23, "kr1")
        L.line(22, 23, 25, 33, "kr1")
        L.line(25, 33, 24, 41, "kr0")
        L.line(36, 32, 35, 45, "kr0")
        # a gull on the top
        put(L, 15, 5, [".w.", "wwk", ".k."], {"w": "w0", "k": "kr0"})
    for L in allf:
        tmp = K.Layer(48, 48)
        tmp.a[:] = shape.a
        tmp.outline("kr0")
        for y, x in zip(*np.nonzero(tmp.a[..., 3] > 0)):
            if tmp.get(int(x), int(y)) == "kr0":
                L.px(int(x), int(y), "kr0")
    foam_ring(allf, 0, 0, 48, 48, lambda X, Y: shape.get(X, Y) is not None and Y > 26,
              width=(3, 4, 3))
    for f, L in enumerate(allf):
        for (x, y) in ((1, 44), (46, 27), (2, 30), (44, 22), (12, 47), (30, 47)):
            if L.get(x, y) is None:
                L.px(x + (f % 2), y, "kq2")
    return s


# --------------------------------------------------------------------------
# The pink sea-cliffs
# --------------------------------------------------------------------------

# Pink stone strata: (top row at x=0, joints, wave phase, tone). The bands
# wave a little; few joints, so they read as rock, not masonry; a fracture
# runs down across them; each band is a shade darker than the one above.
BANDS = [(0, (11,), 0.0, 0), (5, (), 1.7, 1), (10, (5,), 3.1, 0), (13, (), 4.0, 1)]
FRACTURE = {y: 7 + (1 if y > 8 else 0) for y in range(3, 13)}


def _band_at(x, y):
    """(band index, row within the band, thickness, stone start, stone end, tone)."""
    n = len(BANDS)
    tops = []
    for (y0, joints, ph, tone) in BANDS:
        tops.append(y0 + round(0.8 * math.sin(2 * math.pi * x / 16 + ph)))
    for bi in range(n):
        top = tops[bi]
        bot = tops[bi + 1] if bi + 1 < n else tops[0] + 16
        if top <= y < bot or (bi == n - 1 and y < tops[0] and y + 16 < bot):
            if bi == n - 1 and y < tops[0]:
                top -= 16
                bot -= 16
            js = sorted(BANDS[bi][1])
            if js:
                xs = max([j for j in js if j <= x], default=js[-1] - 16)
                xe = min([j for j in js if j > x], default=js[0] + 16)
            else:
                xs, xe = -100, 100
            return bi, y - top, bot - top, xs, xe, BANDS[bi][3]
    return 0, 0, 5, -100, 100, 0


def stone_px(X, Y, dark=0):
    """Pink stone face, 16 px periodic: wavy strata, each lit along its top,
    shadowed beneath, a rare joint and a fracture; dark=1 is the shaded
    variant (caves, a face turned from the sun)."""
    ramp = ["rm5", "rm4", "rm3", "rm2", "rm1", "rm0", "cv0"]
    x, y = X % 16, Y % 16
    bi, tt, th, xs, xe, tone = _band_at(x, y)
    if FRACTURE.get(y) == x and tt > 0:
        i = 5
    elif FRACTURE.get(y) == x + 1 and tt > 0:
        i = 2
    elif x == xs:
        i = 5 if tt >= th - 1 else 4
    elif tt == 0:
        i = 1 if x - xs > 1 and xe - x > 1 else 2
    elif tt >= th - 1:
        i = 4
    elif x == xs + 1:
        i = 2
    elif x == xe - 1:
        i = 4
    elif tt == 1:
        i = 2 + tone
    else:
        k = K.hp(X, Y, 21 + bi)
        i = (3 if k % 3 else 2) + (tone if k % 4 else 0)
        if k % 37 == 0:
            i = 4
    return ramp[min(i + dark, len(ramp) - 1)]


def cliff():
    """The low pink sea-cliff kit. A cliff whose face looks south is three
    rows: `lip` (the plateau's edge, on borrowed grass), `face`, then the
    ground or sea at its foot (`foot_*`)."""
    names = {
        "lip_L": (0, 0), "lip": (1, 0), "lip_b": (2, 0), "lip_R": (3, 0),
        "face_L": (0, 1), "face": (1, 1), "face_b": (2, 1), "face_R": (3, 1),
        "foot_sea_L": (0, 2), "foot_sea": (1, 2), "foot_sea_b": (2, 2), "foot_sea_R": (3, 2),
        "side_E": (4, 0), "side_W": (5, 0), "back": (6, 0), "back_NW": (7, 0),
        "back_NE": (6, 1), "corner_in_E": (4, 1), "corner_in_W": (5, 1), "foot_sand": (7, 1),
        "foot_grass": (4, 2), "foot_sand_rocks": (5, 2), "spring_lip": (6, 2), "seep": (7, 2),
    }
    walk = ["XXXXXXXX", "XXXXXXX.", "WWWW..XX"]
    s = struct("cliff", "Low pink sea-cliffs", 8, 3, SEC, walk=walk, names=names,
               notes="Kythera's pink stone, in a kit for low cliffs along the shore and the cutting. A "
                     "south-facing cliff is `lip` over `face` over a foot: `foot_sea` (borrowed sea, "
                     "foam breaking at the base, animated), `foot_sand` or `foot_grass` (walkable "
                     "ground with fallen stones). `_L` / `_R` end a run; `_b` breaks up a long one. The "
                     "plateau's other edges: `side_E` (plateau to the west, drop to the east), "
                     "`side_W`, `back` (plateau to the south, drop to the north, the face hidden), "
                     "`back_NW` / `back_NE` its corners; `corner_in_E` / `_W` turn a south face into a "
                     "side going north. `spring_lip` is the face with a rock lip a thin fall pours "
                     "from (pair with `falls.thin_fall` below it); `seep` is the face where the "
                     "freshwater spring runs out into its basin. Lip and face cells are impassable.")
    ground(s, "grass", [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (6, 1)])
    ground(s, "sea", [(0, 2), (1, 2), (2, 2), (3, 2)])
    ground(s, "sand", [(7, 1), (5, 2)])
    ground(s, "grass", [(4, 2)])
    M, B = s.M, s.B
    frames = anim_layer(s, "surf", 3)
    allf = [M] + frames

    def lip(L, ox, oy, end=None, b=0, edge_y=10):
        """The plateau's crest: grass to edge_y, then the stone's rounded brow."""
        for x in range(16):
            X = ox + x
            top = edge_y + int(round(wob(x + 4 * b, 0.8) * 0.8))
            if end == "L":
                top += max(0, 6 - x) // 2
            if end == "R":
                top += max(0, x - 9) // 2
            for y in range(top, 16):
                Y = oy + y
                if end == "L" and x < 6 - (y - top) and y - top < 6:
                    continue
                if end == "R" and x > 9 + (y - top) and y - top < 6:
                    continue
                if y == top:
                    c = "rm5" if (x + b) % 5 else "rm4"
                elif y == top + 1:
                    c = "rm4"
                else:
                    c = stone_px(X, Y)
                L.px(X, Y, c)
            # grass tufts lipping over the brow
            if (x * 7 + b) % 5 == 0:
                L.px(X, oy + top, "my3")
                L.px(X, oy + top - 1, "my2")

    def face(L, ox, oy, end=None, b=0):
        for y in range(16):
            for x in range(16):
                X, Y = ox + x, oy + y
                if end == "L" and x < 6 - y // 3:
                    continue
                if end == "R" and x > 9 + y // 3:
                    continue
                c = stone_px(X + 5 * b, Y)
                # darker toward the foot, where the spray keeps it wet
                if y > 11 and c in ("rm3", "rm4"):
                    c = "rm2"
                L.px(X, Y, c)
        if end == "L":
            for y in range(16):
                x = max(0, 6 - y // 3)
                L.px(ox + x, oy + y, "rm4")
        if end == "R":
            for y in range(16):
                x = min(15, 9 + y // 3)
                L.px(ox + x, oy + y, "rm1")

    # row 0: lips; row 1: faces (bottom layer: no ground under a face)
    lip(M, 0, 0, "L")
    lip(M, 16, 0)
    lip(M, 32, 0, b=1)
    lip(M, 48, 0, "R")
    # the face cells under an end show grass beside the slope
    for cx, end, b in ((0, "L", 0), (1, None, 0), (2, None, 1), (3, "R", 0)):
        if end:
            ground(s, "grass", [(cx, 1)])
        face(M if end else B, cx * 16, 16, end, b)
    # row 2: the foot in the sea, foam breaking on it (animated)
    for cx, end in ((0, "L"), (1, None), (2, None), (3, "R")):
        ox, oy = cx * 16, 32
        sub = K.Layer(M.w, M.h)
        for x in range(16):
            # the cliff's base: wet dark stone at the top of the cell
            depth = 3 + int(round(wob(x + 3 * cx, 0.5)))
            if end == "L":
                depth = depth if x >= 6 else max(0, depth - (6 - x))
            if end == "R":
                depth = depth if x <= 9 else max(0, depth - (x - 9))
            for y in range(depth):
                c = "rm1" if y < depth - 1 else "rm0"
                for L in allf:
                    L.px(ox + x, oy + y, c)
                sub.px(ox + x, oy + y, "rm0")
            # fallen blocks at the waterline
        for (bx, by) in (((3, 4), (11, 3)) if cx % 2 else ((7, 4),)):
            for L in allf:
                put(L, ox + bx, oy + by - 1, [".ab.", "abbc", "bbcc"], {"a": "rm3", "b": "rm2", "c": "rm0"})
            sub.rect(ox + bx, oy + by - 1, 4, 3, "rm0")
        foam_ring(allf, ox, oy, 16, 16, lambda X, Y, sub=sub: sub.get(X, Y) is not None or Y < oy,
                  width=(2, 3, 2), pale="mw2")
    # side_E: plateau west, the drop east (a sliver of face catching shadow)
    for (cx, side) in ((4, "E"), (5, "W")):
        ox = cx * 16
        for y in range(16):
            edge = 12 + int(round(wob(y + 2 * cx, 0.6) * 0.5))
            for x in range(16):
                X, Y = ox + x, y
                xx = x if side == "E" else 15 - x
                if xx == edge:
                    M.px(X, Y, "rm5" if side == "W" else "rm4")
                elif edge < xx <= edge + 3:
                    M.px(X, Y, stone_px(X, Y, 1 if side == "E" else 0))
                elif xx > edge + 3:
                    M.px(X, Y, "rm1" if side == "E" else "rm2")
            if (y * 5 + cx) % 6 == 0:
                M.px(ox + (edge if side == "E" else 15 - edge), y, "my3")
    # back: plateau south, the drop north. Only the brow shows: a thin shadowed
    # strip of the far face, then the lit edge, grass tufts on it.
    ox = 6 * 16
    for x in range(16):
        e = 3 + int(round(wob(x + 1, 0.7) * 0.6))
        for y in range(0, e):
            M.px(ox + x, y, "rm1" if y < e - 1 else "rm2")
        M.px(ox + x, e, "rm4")
        if (x * 3) % 7 == 0:
            M.px(ox + x, e + 1, "my3")
    # back corners: the brow turns down a side (NW: plateau to the south-east)
    for (cx, cy, mirror) in ((7, 0, False), (6, 1, True)):
        ox, oy = cx * 16, cy * 16
        for y in range(16):
            for x in range(16):
                xx = 15 - x if mirror else x
                # distance from the corner's arc center (12, 12) in the oriented frame
                r = math.hypot(max(0, 12 - xx), max(0, 12 - y))
                inside = r <= 8.5 if (xx < 12 and y < 12) else (xx >= 12 or y >= 12)
                edge_x = xx < 12 and y >= 12 and xx <= 3
                edge_y = y < 12 and xx >= 12 and y <= 3
                if xx < 12 and y < 12:
                    if r > 11.5:
                        pass
                    elif r > 9.5:
                        M.px(ox + x, oy + y, "rm1")
                    elif r > 8.5:
                        M.px(ox + x, oy + y, "rm2")
                    elif r > 7.6:
                        M.px(ox + x, oy + y, "rm4")
                elif y >= 12 and xx <= 3:
                    M.px(ox + x, oy + y, stone_px(ox + x, oy + y, 1) if xx < 3 else "rm4")
                elif xx >= 12 and y <= 3:
                    M.px(ox + x, oy + y, ("rm1", "rm1", "rm2", "rm4")[y])
    # inner corners: a south face turning into a side running north
    for (cx, side) in ((4, "E"), (5, "W")):
        ox, oy = cx * 16, 16
        ground(s, "grass", [(cx, 1)])
        for y in range(16):
            for x in range(16):
                xx = x if side == "W" else 15 - x
                if xx >= 6 + y // 4:
                    M.px(ox + x, oy + y, stone_px(ox + x, oy + y))
            e = 6 + y // 4
            M.px(ox + (e if side == "W" else 15 - e), oy + y, "rm4" if side == "W" else "rm1")
    # feet on land: fallen stones and a shadow
    for (cx, cy, kind) in ((7, 1, "sand"), (4, 2, "grass"), (5, 2, "sandrocks")):
        ox, oy = cx * 16, cy * 16
        for x in range(16):
            for y in range(0, 2 + (x % 3 == 0)):
                M.px(ox + x, oy + y, "rm0" if y == 0 else "rm1")
        stones = ((2, 4), (9, 3)) if kind != "sandrocks" else ((1, 4), (6, 6), (10, 3), (12, 9))
        for (bx, by) in stones:
            put(M, ox + bx, oy + by, [".ab.", "abbc", ".cc."], {"a": "rm4", "b": "rm3", "c": "rm1"})
        if kind == "grass":
            for (tx, ty) in ((5, 9), (12, 11), (3, 12)):
                put(M, ox + tx, oy + ty, ["a.a", ".b."], {"a": "my3", "b": "my2"})
    # spring_lip: a jutting rock lip at the face's foot, wet streak beneath
    ox, oy = 6 * 16, 32
    for y in range(16):
        for x in range(16):
            B.px(ox + x, oy + y, stone_px(ox + x, oy + y))
    put(B, ox + 2, oy + 9, [
        "..aaaaaaaaaa..",
        ".abbbbbbbbbbc.",
        "abbbbbbbbbbbbc",
        ".ccccddddcccc.",
    ], {"a": "rm5", "b": "rm3", "c": "rm1", "d": "rm0"})
    for y in range(13, 16):
        for x in (6, 7, 8, 9):
            B.px(ox + x, oy + y, "rm0" if x in (6, 9) else "cv0")
    put(B, ox + 1, oy + 3, ["mm.", "mmm", ".m."], {"m": "my2"})
    put(B, ox + 12, oy + 5, [".m", "mm"], {"m": "my1"})
    # seep: water darkening the stone where the spring runs out, moss round it
    ox, oy = 7 * 16, 32
    for y in range(16):
        for x in range(16):
            B.px(ox + x, oy + y, stone_px(ox + x, oy + y))
    for y in range(4, 16):
        for x in range(6, 10):
            if abs(x - 7.5) < 1.5 + y / 12:
                B.px(ox + x, oy + y, "rm1" if (x + y) % 3 else "rm0")
    put(B, ox + 6, oy + 2, [".aa.", "abba", "abba", ".cc."], {"a": "rm4", "b": "cv0", "c": "rm0"})
    for (mx, my_) in ((3, 6), (10, 8), (2, 11), (11, 13), (4, 14)):
        put(B, ox + mx, oy + my_, ["mm", "nm"], {"m": "my3", "n": "my2"})
    K.settle(s, "surf", [(0, 2), (1, 2), (2, 2), (3, 2)])
    return s


# --------------------------------------------------------------------------
# Melos's pumice cliffs, worn into waves
# --------------------------------------------------------------------------

def pumice():
    names = {"top_L": (0, 0), "top": (1, 0), "top_R": (2, 0), "mass": (3, 0),
             "foot_L": (0, 1), "foot": (1, 1), "foot_R": (2, 1), "hollow": (3, 1)}
    s = struct("pumice", "Melos's white pumice cliffs", 4, 2, SEC,
               walk=["XXXX", "WWWX"], names=names,
               notes="Melos's bay ends in white pumice worn by the sea into frozen waves. `top_*` is "
                     "the cliff's crest (on borrowed grass), `mass` its body to fill a wider headland, "
                     "`foot_*` where it meets the sea (borrowed sea, animated foam), `hollow` a "
                     "sea-worn hollow in the mass where something might be tucked (the dead end's "
                     "reward). Impassable.")
    ground(s, "grass", [(0, 0), (1, 0), (2, 0)])
    ground(s, "sea", [(0, 1), (1, 1), (2, 1)])
    M, B = s.M, s.B
    frames = anim_layer(s, "surf", 3)
    allf = [M] + frames

    def wave_px(X, Y):
        """White rock carved into smooth undulating ridges."""
        x, y = X % 32, Y % 16
        ridge = (y + 3 * math.sin(2 * math.pi * x / 32) + 1.5 * math.sin(2 * math.pi * x / 16 + 1)) % 6
        if ridge < 1.0:
            return "w0"
        if ridge < 2.5:
            return "kr3"
        if ridge < 4.2:
            return "kr3" if (X + Y) % 4 else "kr2"
        if ridge < 5.2:
            return "kr2"
        return "kr1"
    # crest: rounded white lumps over grass
    for cx, end in ((0, "L"), (1, None), (2, "R")):
        ox = cx * 16
        for x in range(16):
            top = 6 + int(round(2 * math.sin(2 * math.pi * (ox + x) / 22) + wob(x) * 0.6))
            if end == "L":
                top += max(0, 6 - x)
            if end == "R":
                top += max(0, x - 9)
            for y in range(max(0, top), 16):
                M.px(ox + x, y, "w0" if y == top else wave_px(ox + x, y))
    # mass
    for y in range(16):
        for x in range(16):
            B.px(48 + x, y, wave_px(48 + x, y))
    # foot: the waves of rock end in a dark wet line, and foam breaks
    for cx, end in ((0, "L"), (1, None), (2, "R")):
        ox, oy = cx * 16, 16
        sub = K.Layer(M.w, M.h)
        for x in range(16):
            d = 5 + int(round(2 * math.sin(2 * math.pi * (ox + x) / 22 + 2) + wob(x + 5) * 0.5))
            if end == "L":
                d = d if x >= 5 else max(0, d - (5 - x) * 2)
            if end == "R":
                d = d if x <= 10 else max(0, d - (x - 10) * 2)
            for y in range(d):
                c = wave_px(ox + x, oy + y) if y < d - 2 else ("kr1" if y == d - 2 else "kr0")
                for L in allf:
                    L.px(ox + x, oy + y, c)
                sub.px(ox + x, oy + y, "kr0")
        foam_ring(allf, ox, oy, 16, 16, lambda X, Y, sub=sub: sub.get(X, Y) is not None or Y < oy,
                  width=(2, 3, 2))
    # hollow: a smooth sea-worn hole in the mass
    for y in range(16):
        for x in range(16):
            B.px(48 + x, 16 + y, wave_px(48 + x, 16 + y))
    put(B, 48 + 3, 16 + 4, [
        "..kkkkkkk..",
        ".k1000001k.",
        "k100000001k",
        "k100000001k",
        "k110000011k",
        ".k1100011k.",
        "..k33333k..",
    ], {"k": "kr2", "1": "kr1", "0": "kr0", "3": "kr3"})
    K.settle(s, "surf", [(0, 1), (1, 1), (2, 1)])
    return s


def build():
    """Kythera's coast pieces (Melos's take theirs from the same painters)."""
    rocks = tide_rocks()
    cl = cliff()
    return [
        surf(),
        K.pick(sand_decor(), ["lace", "shells", "scallop", "wrack", "footprints", "sherd_dig"],
               notes="Decorations on borrowed aethos sand, all walkable: `lace`, a line of dried foam "
                     "the tide left (lay it a cell or two above the surf); `shells`, scattered "
                     "cockles; `scallop`, one great scallop shell, Aphrodite's sign; `wrack`, a line "
                     "of dried sea-grass; `footprints`, someone walked here; `sherd_dig`, turned earth "
                     "above the tide line (Alethea's dig spot)."),
        shingle(),
        K.pick(rocks, ["tide_rock", "tide_rocks", "spit_M", "spit_V", "spit_head", "rock_sand",
                       "rocks_sand", "rock_grass"],
               notes="White rock in the sea and on land. `tide_rock` and `tide_rocks` stand in the "
                     "surf with breathing foam (animated). The reef spit is a walkable path of flat, "
                     "wet rock out into the sea at low tide (the diver's spit on the Foam Road): "
                     "`spit_M` runs east-west, `spit_V` north-south, and `spit_head`, a broad flat "
                     "rock, ends it or turns it. Its foam breathes too. `rock_sand` and `rocks_sand` "
                     "sit on sand, `rock_grass` on grass."),
        aphrodite_rock(),
        K.pick(cl, ["lip_L", "lip", "lip_R", "side_E", "side_W", "back", "back_NW", "back_NE",
                    "face_L", "face", "face_R", "corner_in_E", "corner_in_W", "foot_sand",
                    "foot_grass", "foot_sand_rocks", "foot_sea_L", "foot_sea", "foot_sea_R",
                    "spring_lip", "seep"], w=8),
    ]
