"""Route 33's art for gTileset_Westsea: the post-game's western sea.

Everything here stands in aethos's animated sea, or on its sand and grass, the
way Akti's coast does (akti_lib.ground): a cell's bottom layer is left empty and
westsea_build.py gives it aethos's own ground, so the water under every rock,
reef, wreck and current moves with the sea around it.

Pieces:
  - the rocky coast: an autotile of limestone crags in thirteen shapes (edges,
    corners, inner corners), its top cut from one 32x32 texture on a torus so the
    mainland and the islets run seamlessly;
  - shoals: lighter water over sand, a dithered overlay on the live sea, in the
    same thirteen shapes, and reefs awash in them;
  - currents in four directions (MB_*_CURRENT), a whirlpool, the loose reef the
    bronze ram breaks, and the fog bank toward the Pillars;
  - the wreck, the stone ship (the Phaeacians' ship that Poseidon turned to stone
    off Kerkyra, Odyssey 13.159-164), the birds' rock and Poseidon's sea-stack
    altar;
  - Halia's islet: her reed-thatched hut, the jetty, Kymon's raft, and Akti's
    nets, beached boat, shells and kaiki (drawn by akti's own painters).

Every 8x8 tile takes its colors from one of GROUPS (secondary palettes 6-12);
validate() checks it. See westsea_build.py for packing and compiling.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import akti_lib  # noqa: E402,F401  (registers akti's color names)
import kalliste_lib as K  # noqa: E402
from akti_lib import ground  # noqa: E402
from kalliste_lib import Struct, tile_colors  # noqa: E402
from kalliste_parts import voronoi_labels  # noqa: E402

SEC = "westsea"

# --------------------------------------------------------------------------
# Colors and palette groups
# --------------------------------------------------------------------------

NEW = {
    # shoals: the sea over pale sand, aethos's turquoise (ae_t) and lighter
    "sh0": (64, 144, 200), "sh1": (88, 176, 200), "sh2": (120, 192, 208),
    "sh3": (160, 208, 216), "sh4": (200, 224, 208),
    # the fog bank
    "fg0": (192, 200, 216), "fg1": (224, 232, 232),
    # reed thatch
    "th0": (96, 72, 40), "th1": (144, 112, 56), "th2": (192, 160, 88), "th3": (224, 200, 128),
    "th4": (240, 224, 168),
}
for _n, _c in NEW.items():
    assert all(v % 8 == 0 for v in _c), _n
    K.C[_n] = _c
    K.RGB2NAME.setdefault(_c, _n)
C = K.C

GROUPS = {
    # limestone crags, their foam and weed, gulls (akti's "stone" group)
    "stone": ["sk", "s0", "s1", "s2", "s3", "s4", "s5", "e1", "e2", "wt0", "wt1", "alg",
              "w0", "b3", "ol1"],
    # overlays on the live sea: shoals, currents, the whirlpool, fog
    "sea": ["b0", "wa1", "b1", "wr", "wa3", "b2", "b3", "w0", "ink", "sh0", "sh1", "sh2", "sh3",
            "sh4", "fg0"],
    # timber, rope and pitch: the wreck, the jetty, the raft, boats, nets (akti's)
    "wood": ["ink", "wd0", "wd1", "wd2", "wd3", "rp", "w0", "b0", "b1", "b2", "rd", "g1",
             "br", "g0", "tc1"],
    # Halia's hut: reed thatch over rough whitewashed stone
    "hut": ["ink", "th0", "th1", "th2", "th3", "th4", "w0", "w1", "w2", "w3", "s1", "s2", "s3",
            "wd0", "wd1"],
    # Poseidon's altar on its stack: marble and Aegean paint, with the stack's stone
    "shrine": ["ink", "w0", "m1", "m2", "m3", "m4", "b0", "b1", "b2", "g1", "sk", "s1", "s2",
               "s3", "s4"],
    # the meadow and olive greens (akti's), for anything on the islets' grass
    "grove": ["ink", "gr0", "gr1", "gr2", "ov0", "ov1", "ov2", "ov3", "ov4", "tk0", "tk1",
              "tk2", "pu0", "pu1", "wd2"],
    # the fog bank: pearl-grey mist over the sea's blues
    "fog": ["w0", "fg0", "fg1", "b3", "b2", "wr", "b1", "b0"],
}
for g, names in GROUPS.items():
    assert len(names) <= 15, (g, len(names))
    assert len(set(C[n] for n in names)) == len(names), g
    for n in names:
        assert n in C, n
GROUP_RGB = {g: {C[n] for n in names} for g, names in GROUPS.items()}


def validate(structs):
    """akti_lib.validate with westsea's groups: one group per tile per layer, at
    most two layers per metatile, and borrowed-ground cells draw one upper layer."""
    problems = []
    for s in structs:
        gr = getattr(s, "ground", {})
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    cols = tile_colors(layer, tx, ty)
                    if cols and not any(cols <= g for g in GROUP_RGB.values()):
                        names = sorted(K.RGB2NAME.get(c, str(c)) for c in cols)
                        problems.append(f"{s.key} {ln} tile ({tx},{ty}) mixes groups: {names}")
        for cy in range(s.h):
            for cx in range(s.w):
                sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                n = sum(1 for layer in s.layers.values() if (layer.a[sl][..., 3] > 0).any())
                if n == 3:
                    problems.append(f"{s.key} metatile ({cx},{cy}) has three layers")
                if (cx, cy) in gr:
                    if (s.B.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground draws a bottom")
                    if (s.T.a[sl][..., 3] > 0).any() and (s.M.a[sl][..., 3] > 0).any():
                        problems.append(f"{s.key} ({cx},{cy}) on borrowed ground uses both upper layers")
                    continue
                lower = np.maximum(s.B.a[sl][..., 3], s.M.a[sl][..., 3])
                if n and not (lower > 0).all():
                    problems.append(f"{s.key} ({cx},{cy}) has holes below the sprites layer")
    return problems


def paint(L, ox, oy, grid):
    """Paint a 2-D array of color names (None = leave) at (ox, oy)."""
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c is not None:
                L.px(ox + x, oy + y, c)


# --------------------------------------------------------------------------
# Neighborhood autotiles: thirteen shapes
# --------------------------------------------------------------------------
# A region cell's shape comes from which of its neighbours lie outside the region
# (the map builders use the same names; see tools/ichor/maps/westsea.py):
#   tl t tr / l c r / bl b br, and in_nw in_ne in_sw in_se for a cell whose only
#   outside neighbour is that diagonal.

SHAPES = ["tl", "t", "tr", "l", "c", "r", "bl", "b", "br", "in_nw", "in_ne", "in_sw", "in_se"]


def shape_grid(shape):
    """3x3 booleans (row-major, True = inside the region) for a canonical shape."""
    g = [[True] * 3 for _ in range(3)]
    if shape.startswith("in_"):
        d = shape[3:]
        g[0 if "n" in d else 2][0 if "w" in d else 2] = False
        return g
    if "t" in shape:
        g[0] = [False] * 3
    if "b" in shape:
        g[2] = [False] * 3
    if "l" in shape:
        for r in g:
            r[0] = False
    if "r" in shape:
        for r in g:
            r[2] = False
    return g


def cell_mask(grid):
    """48x48 booleans: the 3x3 cells of `grid` in pixels."""
    m = np.zeros((48, 48), bool)
    for j in range(3):
        for i in range(3):
            if grid[j][i]:
                m[j * 16:j * 16 + 16, i * 16:i * 16 + 16] = True
    return m


def erode(mask, up, down, side):
    """The region shrunk away from its outside: `up` px below an outside cell
    above, `down` px above one below, `side` px from one beside, with rounded
    corners (an elliptical kernel, each half its own height)."""
    h, w = mask.shape
    out = mask.copy()
    for dy in range(-up, down + 1):
        for dx in range(-side, side + 1):
            ry = up if dy < 0 else max(down, 1)
            if (dx / (side + 0.5)) ** 2 + (dy / (ry + 0.5)) ** 2 > 1.0:
                continue
            sh = np.zeros_like(mask)
            ys0, ys1 = max(0, -dy), min(h, h - dy)
            xs0, xs1 = max(0, -dx), min(w, w - dx)
            sh[ys0:ys1, xs0:xs1] = mask[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx]
            # outside the canvas counts as inside (the region runs on)
            if dy > 0:
                sh[h - dy:, :] = True
            if dy < 0:
                sh[:-dy, :] = True
            if dx > 0:
                sh[:, w - dx:] = True
            if dx < 0:
                sh[:, :-dx] = True
            out &= sh
    return out


def dilate(mask, r=1):
    out = mask.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if abs(dx) + abs(dy) > r:
                continue
            out |= np.roll(np.roll(mask, dy, 0), dx, 1)
    return out


# --------------------------------------------------------------------------
# The rocky coast
# --------------------------------------------------------------------------

FACE = 7          # the south face's height, px
_TEX = {}


def rock_texture(seed=5):
    """A 32x32 limestone top on a torus: facets lit on their upper-left edges,
    joined by dark cracks, a few pocks. Sampled at map parity, so it runs on."""
    if seed in _TEX:
        return _TEX[seed]
    rng = random.Random(seed)
    seeds = [(rng.randrange(32), rng.randrange(32)) for _ in range(10)]
    lab = voronoi_labels(32, 32, seeds, wrap=True, stretch=(1.0, 1.25))
    tilt = [rng.choice(("s3", "s3", "s4", "s3", "s2", "s3")) for _ in seeds]
    hi = {"s2": "s3", "s3": "s4", "s4": "s4"}
    lo = {"s4": "s3", "s3": "s2", "s2": "s2"}
    noise = np.random.default_rng(seed).random((32, 32))
    tex = np.empty((32, 32), object)
    for y in range(32):
        for x in range(32):
            k = lab[y, x]
            c = tilt[k]
            r = lab[y, (x + 1) % 32] != k
            d = lab[(y + 1) % 32, x] != k
            l_ = lab[y, (x - 1) % 32] != k
            u = lab[(y - 1) % 32, x] != k
            if r or d:
                c = "s1" if (r and d) else "s2" if c != "s2" else "s1"
            elif l_ or u:
                c = hi[c]
            elif noise[y, x] < 0.10:
                c = lo[c]                          # pocks and weathering
            elif noise[y, x] > 0.95:
                c = hi[c]
            tex[y, x] = c
    _TEX[seed] = tex
    return tex


def scrub_dots(rng, n, region):
    """Lentisk and thyme clumps: a list of (x, y, color) inside `region`."""
    out = []
    ys, xs = np.nonzero(region)
    if not len(xs):
        return out
    for _ in range(n):
        i = rng.randrange(len(xs))
        x, y = int(xs[i]), int(ys[i])
        for (dx, dy, c) in ((0, 0, "ol1"), (1, 0, "ol1"), (-1, 1, "ol1"), (0, 1, "alg"),
                            (1, 1, "alg"), (2, 1, "ol1"), (0, -1, "ol1"), (1, 2, "s1"),
                            (0, 2, "s1")):
            out.append((x + dx, y + dy, c))
    return out


def rock_cell(grid, parity=(0, 0), seed=5, scrub=0, cave=False):
    """The middle cell of a 3x3 neighbourhood of rock (True) and sea, as a 16x16
    grid of color names (None = the sea shows through)."""
    rock = cell_mask(grid)
    top = erode(rock, up=4, down=FACE + 3, side=3)
    face = np.zeros_like(top)
    for d in range(1, FACE + 1):
        face[d:] |= top[:-d]
    face &= ~top
    body = top | face
    foam1 = dilate(body, 1) & ~body
    foam2 = dilate(body, 2) & ~body & ~foam1
    tex = rock_texture(seed)
    px, py = parity
    rng = random.Random(seed * 131 + px * 7 + py * 3 + sum(map(sum, grid)))
    out = np.empty((48, 48), object)
    for y in range(48):
        for x in range(48):
            ax, ay = x - 16 + px * 16, y - 16 + py * 16
            if top[y, x]:
                c = tex[ay % 32, ax % 32]
                # the rim: lit along the upper-left, dark along the lower-right
                if not top[y - 1, x] if y else False:
                    c = "s5"
                elif x and not top[y, x - 1]:
                    c = "s5" if c != "s1" else "s4"
                elif x + 1 < 48 and not top[y, x + 1]:
                    c = "s2"
                out[y, x] = c
            elif face[y, x]:
                depth = 0
                while depth < FACE and y - depth - 1 >= 0 and face[y - depth - 1, x]:
                    depth += 1
                below = y + 1 >= 48 or not body[y + 1, x]
                c = "s2" if (ax * 3 + 1) % 7 else "s1"
                if depth == 0:
                    c = "s3"
                elif (ax + depth) % 5 == 0:
                    c = "s1"
                if below:
                    c = "wt0"
                elif y + 2 < 48 and not body[y + 2, x]:
                    c = "alg" if ax % 3 else "wt1"
                if x and not body[y, x - 1] and c not in ("wt0", "alg", "wt1"):
                    c = "s3"
                out[y, x] = c
            elif foam1[y, x] and (y + 1 >= 48 or not top[min(47, y + 1), x] or face[y - 1, x]):
                # foam: thick along the foot, broken on the sides and above
                below_face = y and face[y - 1, x]
                if below_face or (ax * 5 + ay) % 3:
                    out[y, x] = "w0" if (ax + ay) % 4 else "b3"
                else:
                    out[y, x] = None
            elif foam2[y, x] and (ax * 3 + ay * 5) % 4 == 0 and y > 0 and face[max(0, y - 2), x]:
                out[y, x] = "b3"
            else:
                out[y, x] = None
    # outline the silhouette
    edge = body & ~(np.roll(body, 1, 0) & np.roll(body, -1, 0) & np.roll(body, 1, 1) & np.roll(body, -1, 1))
    for y, x in zip(*np.nonzero(edge)):
        if 0 < y < 47 and 0 < x < 47 and out[y, x] not in ("s5", "wt0") and body[y, x]:
            nb_out = (not body[y - 1, x]) or (not body[y + 1, x]) or (not body[y, x - 1]) or (not body[y, x + 1])
            if nb_out:
                out[y, x] = "sk" if out[y, x] != "alg" else "alg"
    # scrub on the top, away from the rims
    inner = erode(top, 2, 2, 2) & cell_mask([[False] * 3, [False, True, False], [False] * 3])
    for (x, y, c) in scrub_dots(rng, scrub, inner):
        if 0 <= x < 48 and 0 <= y < 48 and top[y, x]:
            out[y, x] = c
    cell = out[16:32, 16:32].copy()
    if cave:
        # a sea cave in the south face: a dark arch with water running in
        arch = ["  kkkk  ", " kkkkkk ", "kkkkkkkk", "kkkkkkkk", "kkwkkwkk"]
        fy = max((y for y in range(16) if cell[y, 8] in ("wt0", "alg", "wt1", "s1", "s2", "s3")),
                 default=12)
        for j, row in enumerate(arch):
            for i, ch in enumerate(row):
                if ch == " ":
                    continue
                y, x = fy - 4 + j, 4 + i
                if 0 <= y < 16:
                    cell[y, x] = "sk" if ch == "k" else "w0"
    return cell


def rock_piece(shape, parity=(0, 0), scrub=0, seed=5, key=None, cave=False):
    key = key or f"rock_{shape}" + (f"_{parity[0]}{parity[1]}" if parity != (0, 0) else "")
    s = Struct(key, f"Rocky coast: {shape}", 1, 1, SEC, walk=["X"],
               notes="Limestone coast autotile on aethos's animated sea.")
    ground(s, "sea")
    paint(s.M, 0, 0, rock_cell(shape_grid(shape), parity, seed=seed, scrub=scrub, cave=cave))
    s.shape = shape
    return s


def rock_pieces():
    """The coast: thirteen shapes. The top runs on a 2x2-cell texture, so the
    middle comes in four parities, the north and south edges in two (by x) and
    the west and east edges in two (by y); corners take parity (0,0). Two more
    middles carry scrub."""
    out = []
    for shape in SHAPES:
        if shape == "c":
            for p in ((0, 0), (1, 0), (0, 1), (1, 1)):
                out.append(rock_piece("c", p))
        elif shape in ("t", "b"):
            for p in ((0, 0), (1, 0)):
                out.append(rock_piece(shape, p))
        elif shape in ("l", "r"):
            for p in ((0, 0), (0, 1)):
                out.append(rock_piece(shape, p))
        else:
            out.append(rock_piece(shape))
    out.append(rock_piece("b", (0, 0), key="rock_b_cave", cave=True))
    return out


def rock_cypress():
    """A cypress rooted in a cleft of the rock top: 1x2, on the coast's middle."""
    s = Struct("rock_cypress", "Cypress in the rock", 1, 2, SEC, walk=["X", "X"],
               notes="Stands on rock_c: its lower cell is the rock top, parity (0,0).")
    ground(s, "sea")
    base = rock_cell(shape_grid("c"), (0, 1))
    top = rock_cell(shape_grid("c"), (0, 0))
    paint(s.M, 0, 0, top)
    paint(s.M, 0, 16, base)
    # the spire: dark alg and ol1, outlined sk
    for y in range(1, 26):
        half = max(1, min(5, int((y + 2) / 3.2)))
        if y > 20:
            half = max(1, 5 - (y - 20))
        for x in range(8 - half, 8 + half):
            c = "alg" if (x + y) % 3 else "ol1"
            if x == 8 - half:
                c = "sk"
            elif x == 8 + half - 1:
                c = "sk" if y % 2 else "alg"
            s.M.px(x, y, c)
    s.M.vline(8, 26, 28, "s0")
    s.M.vline(7, 27, 28, "s1")
    return s


# --------------------------------------------------------------------------
# Shoals: lighter water over sand
# --------------------------------------------------------------------------

_SHOAL_NOISE = None


def shoal_noise():
    """A 32x32 value noise on a torus: where the sand under a shoal is paler."""
    global _SHOAL_NOISE
    if _SHOAL_NOISE is None:
        rng = np.random.default_rng(33)
        base = rng.random((8, 8))
        up = np.kron(base, np.ones((4, 4)))
        # blur on the torus
        out = np.zeros_like(up)
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                out += np.roll(np.roll(up, dy, 0), dx, 1)
        out /= 49.0
        _SHOAL_NOISE = (out - out.min()) / (out.max() - out.min())
    return _SHOAL_NOISE


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def shoal_cell(grid, parity=(0, 0)):
    """A dithered turquoise overlay whose density rises from the region's edge
    to its middle; the live sea shows through the gaps."""
    m = cell_mask(grid)
    # round the region's corners, outer and inner, so the shoal's edge curves
    r = 5
    m = ~erode(~erode(m, r, r, r), r, r, r)       # opening: convex corners rounded
    m = erode(~erode(~m, r, r, r), r, r, r)       # closing: concave corners filled round
    # distance (in px, capped) from the outside of the region
    dist = np.zeros((48, 48), int)
    cur = m.copy()
    for d in range(1, 9):
        cur = erode(cur, 1, 1, 1)
        dist += cur
    noise = shoal_noise()
    px, py = parity
    out = np.empty((16, 16), object)
    for y in range(16):
        for x in range(16):
            X, Y = x + 16, y + 16
            ax, ay = x + px * 16, y + py * 16
            d = dist[Y, X]
            if not m[Y, X] or d == 0:
                out[y, x] = None
                continue
            level = 1 + d * 2
            if BAYER[ay % 4][ax % 4] >= level:
                out[y, x] = None
                continue
            n = noise[ay % 32, ax % 32]
            c = "sh1" if n < 0.4 else "sh2" if n < 0.82 else "sh3"
            if (ax * 7 + ay * 13) % 29 == 0:
                c = "sh3" if c != "sh3" else "sh4"
            if d < 3:
                c = "sh0" if (ax + ay) % 2 else "sh1"
            out[y, x] = c
    return out


def shoal_piece(shape, parity=(0, 0)):
    key = f"shoal_{shape}" + (f"_{parity[0]}{parity[1]}" if parity != (0, 0) else "")
    s = Struct(key, f"Shoal: {shape}", 1, 1, SEC, walk=["."],
               notes="Lighter water over sand, surfable (MB_OCEAN_WATER), on the live sea.")
    ground(s, "sea")
    paint(s.M, 0, 0, shoal_cell(shape_grid(shape), parity))
    s.behaviors[(0, 0)] = "MB_OCEAN_WATER"
    s.shape = shape
    return s


def shoal_pieces():
    out = []
    for shape in SHAPES:
        if shape == "c":
            for p in ((0, 0), (1, 0), (0, 1), (1, 1)):
                out.append(shoal_piece("c", p))
        else:
            out.append(shoal_piece(shape))
    return out


def reef(key, seed, cluster):
    """A reef awash in a shoal: a few low crags, weed and foam. Its water is drawn
    (a shoal's middle, opaque) rather than borrowed, so the crags can sit on the
    middle layer over it. Solid."""
    from akti_coast import crag
    s = Struct(key, "Reef awash", 1, 1, SEC, walk=["X"],
               notes="Low rocks just breaking the surface, in a shoal. Solid.")
    halo = shoal_cell(shape_grid("c"), (seed % 2, 0))
    for y in range(16):
        for x in range(16):
            c = halo[y, x]
            if c is None:
                c = "wr" if (x * 3 + y * 5 + seed) % 7 == 0 else "b1"
            s.B.px(x, y, c)
    for pts, face in cluster:
        crag(s.M, pts, face=face, seed=seed, shrub=0)
    return s


def reef_pieces():
    return [
        reef("reef_a", 61, [([(2, 6), (7, 4), (11, 6), (9, 10), (3, 10)], 3),
                            ([(10, 11), (13, 10), (15, 12), (12, 14)], 2)]),
        reef("reef_b", 62, [([(3, 3), (8, 2), (10, 5), (6, 7), (2, 6)], 2),
                            ([(7, 9), (12, 8), (14, 11), (11, 13), (6, 12)], 3)]),
        reef("reef_c", 63, [([(1, 8), (5, 6), (8, 8), (6, 11), (2, 11)], 2),
                            ([(9, 3), (13, 2), (15, 5), (12, 7)], 2),
                            ([(10, 10), (14, 9), (15, 12), (11, 13)], 2)]),
    ]


# --------------------------------------------------------------------------
# Currents, the whirlpool, the ram's reef, the fog
# --------------------------------------------------------------------------

def current_piece(direction, variant):
    """A current: flow lines on the live sea, with an arrowhead, running
    `direction`. The lines wrap at the cell's edges, so a lane of current cells
    reads as one stream; the two variants differ only in where the arrowhead is.
    MB_*_CURRENT carries the surfer along it."""
    beh = {"e": "MB_EASTWARD_CURRENT", "w": "MB_WESTWARD_CURRENT",
           "n": "MB_NORTHWARD_CURRENT", "s": "MB_SOUTHWARD_CURRENT"}[direction]
    s = Struct(f"current_{direction}{variant}", f"Current flowing {direction}", 1, 1, SEC,
               walk=["."], notes=f"{beh}: a fast lane with it, a wall against it.")
    ground(s, "sea")
    g = [[None] * 16 for _ in range(16)]
    # flow lines, drawn flowing east: (row, start, length); each bends a little
    for (row, x0, ln) in ((2, 3, 11), (7, 10, 13), (12, 6, 9)):
        for i in range(ln):
            x = (x0 + i) % 16
            y = row
            g[y][x] = "w0" if i >= ln - 2 else ("b3" if i >= 2 else "b2")
    # the arrowhead at the end of one line
    (ty, tx) = (7, (10 + 13 - 1) % 16) if variant == "a" else (12, (6 + 9 - 1) % 16)
    for k in (1, 2):
        for dy in (-k, k):
            y, x = ty + dy, (tx - k) % 16
            if 0 <= y < 16:
                g[y][x] = "w0" if k == 1 else "b3"
    arr = np.array(g, object)
    if direction == "w":
        arr = arr[:, ::-1]
    elif direction == "s":
        arr = arr.T
    elif direction == "n":
        arr = arr.T[::-1, :]
    paint(s.M, 0, 0, arr)
    s.behaviors[(0, 0)] = beh
    return s


def current_pieces():
    return [current_piece(d, v) for d in "ewns" for v in "ab"]


def whirlpool():
    """A 2x2 ring of turning water: Triton's Conch calms it (data/scripts/
    ichor_postgame_sea.pory). The cells are passable; invisible objects block it
    until it's calmed, then the map swaps in plain sea."""
    s = Struct("whirlpool", "Whirlpool", 2, 2, SEC, walk=["..", ".."],
               notes="Four cells; the map's objects block them until the Conch calms it.")
    ground(s, "sea")
    cx, cy = 15.5, 15.5
    for y in range(32):
        for x in range(32):
            dx, dy = x - cx, y - cy
            r = math.hypot(dx, dy)
            if r > 15.2:
                continue
            a = math.atan2(dy, dx)
            # a four-armed spiral: the phase turns with the radius
            ph = (a * 4 / (2 * math.pi) + r / 4.2) % 1.0
            if r < 2.2:
                c = "ink"
            elif r < 4.5:
                c = "b0" if ph < 0.6 else "wa1"
            elif ph < 0.16:
                c = "w0" if r > 6 else "b3"
            elif ph < 0.34:
                c = "b3" if r > 9 else "b2"
            elif ph < 0.55:
                c = "b2" if r < 11 else "wr"
            elif ph < 0.8:
                c = "b1" if r < 9 else ("wa1" if r < 13 else None)
            else:
                c = "b0" if r < 8 else ("wa1" if r < 12 else None)
            if r > 13.5 and c not in ("w0", "b3"):
                c = None
            if c:
                s.M.px(x, y, c)
    return s


def ram_rock(key, seed, pts_list):
    """Loose reef rock, cracked and barnacled: what the bronze ram breaks."""
    from akti_coast import crag
    s = Struct(key, "Loose reef rock (the ram breaks it)", 1, 1, SEC, walk=["."],
               notes="Passable cell: the map's invisible object blocks it until the ram "
                     "breaks it (EventScript_IchorSeaRock), then the map swaps in sea.")
    ground(s, "sea")
    for pts, face in pts_list:
        crag(s.M, pts, face=face, seed=seed, shrub=0)
    rng = random.Random(seed)
    # cracks through the rock and barnacles at the waterline
    for _ in range(3):
        x, y = rng.randrange(4, 12), rng.randrange(3, 9)
        for k in range(rng.randrange(3, 6)):
            if s.M.get(x, y) in ("s2", "s3", "s4", "s5", "s1"):
                s.M.px(x, y, "sk")
            x += rng.choice((-1, 0, 1))
            y += 1
    for _ in range(7):
        x, y = rng.randrange(1, 15), rng.randrange(6, 14)
        if s.M.get(x, y) in ("wt0", "wt1", "alg", "s1", "s2"):
            s.M.px(x, y, "w0")
    return s


def ram_rocks():
    return [
        ram_rock("ram_rock_a", 71, [([(1, 5), (6, 2), (11, 3), (14, 7), (12, 10), (5, 11), (1, 9)], 3)]),
        ram_rock("ram_rock_b", 72, [([(2, 3), (7, 1), (10, 4), (8, 8), (3, 7)], 3),
                                    ([(7, 7), (12, 5), (15, 9), (13, 12), (8, 12)], 3)]),
    ]


_FOG_NOISE = None


def fog_noise():
    """32x32 soft noise on a torus, stretched east-west: the fog's banks."""
    global _FOG_NOISE
    if _FOG_NOISE is None:
        rng = np.random.default_rng(77)
        base = rng.random((4, 8))
        up = np.kron(base, np.ones((8, 4)))
        out = np.zeros_like(up)
        for dy in range(-4, 5):
            for dx in range(-3, 4):
                out += np.roll(np.roll(up, dy, 0), dx, 1)
        _FOG_NOISE = (out - out.min()) / (out.max() - out.min())
    return _FOG_NOISE


def fog_cell(kind, parity=(0, 0)):
    """The fog bank toward the Pillars. 'core': a wall of pearl mist with slow
    banks in it; 'edge': the bank's eastern face, thinning to the live sea;
    'lane': the thinner mist of the one way through. Seamless across cells."""
    noise = fog_noise()
    px, py = parity
    out = np.empty((16, 16), object)
    for y in range(16):
        for x in range(16):
            ax, ay = x + px * 16, y + py * 16
            n = noise[ay % 32, ax % 32]
            if kind == "core":
                density = 1.0
            elif kind == "edge":
                density = 1.0 - (x + 0.5) / 16.0 + 0.25 * (n - 0.5)
            else:
                density = 0.38 + 0.3 * (n - 0.5)
            if BAYER[ay % 4][ax % 4] >= density * 16:
                out[y, x] = None
                continue
            out[y, x] = "w0" if n > 0.86 else "fg1" if n > 0.5 else "fg0"
            if kind != "core" and BAYER[ay % 4][ax % 4] >= density * 16 - 3:
                out[y, x] = "b3"                    # the mist's thin edge catches the blue
    return out


def fog_piece(key, kind, parity=(0, 0)):
    s = Struct(key, f"Fog bank ({kind})", 1, 1, SEC, walk=["X" if kind == "core" else "."],
               notes="Mist over the sea toward the Pillars. The core is a wall; the way "
                     "through is held by the map's invisible objects.")
    ground(s, "sea")
    paint(s.M, 0, 0, fog_cell(kind, parity))
    return s


def fog_pieces():
    out = [fog_piece(f"fog_core_{px}{py}", "core", (px, py)) for py in (0, 1) for px in (0, 1)]
    out += [fog_piece(f"fog_edge_{py}", "edge", (0, py)) for py in (0, 1)]
    out += [fog_piece(f"fog_lane_{px}", "lane", (px, 0)) for px in (0, 1)]
    return out


# --------------------------------------------------------------------------
# More rock: scrub, pines, islets, reefs on open sea, mooring posts
# --------------------------------------------------------------------------

def bush(L, x, y, w, rng):
    """A lentisk or thyme bush on rock: a dome of two greens, a dark foot, a
    shadow to the lower right."""
    h = max(3, w * 2 // 3)
    for j in range(h + 1):
        for i in range(w + 1):
            if ((i - w / 2) / (w / 2 + 0.3)) ** 2 + ((j - h / 2) / (h / 2 + 0.3)) ** 2 <= 1.0:
                c = "ol1" if (i + j) % 3 and j < h * 0.6 else "alg"
                if j == 0 or i == 0:
                    c = "ol1"
                L.px(x + i, y + j, c)
    for i in range(1, w + 1):
        L.px(x + i, y + h + 1, "s1")
    L.px(x + w + 1, y + h, "s1")
    L.px(x + w // 2, y + h, "sk")


def rock_scrub_piece(parity):
    key = f"rock_c_scrub_{parity[0]}{parity[1]}"
    s = Struct(key, "Rock top under scrub", 1, 1, SEC, walk=["X"],
               notes="The mainland's middle, thick with lentisk and thyme.")
    ground(s, "sea")
    cell = rock_cell(shape_grid("c"), parity)
    paint(s.M, 0, 0, cell)
    rng = random.Random(97 + parity[0] * 3 + parity[1] * 5)
    spots = [(1, 1, 5), (8, 2, 4), (3, 8, 4), (9, 9, 5)]
    rng.shuffle(spots)
    for (x, y, w) in spots[:3 + (parity[0] ^ parity[1])]:
        bush(s.M, x + rng.randrange(0, 2), y + rng.randrange(0, 2), w, rng)
    return s


def rock_pine():
    """A stone pine on the rock: an umbrella of dark needles on a leaning trunk,
    its shadow on the limestone. 2x2; place it at even x and y."""
    s = Struct("rock_pine", "Stone pine on the rock", 2, 2, SEC, walk=["XX", "XX"],
               notes="Over rock_c's four parities: place at an even (x, y).")
    ground(s, "sea")
    for cy in (0, 1):
        for cx in (0, 1):
            paint(s.M, cx * 16, cy * 16, rock_cell(shape_grid("c"), (cx, cy)))
    M = s.M
    for y in range(22, 29):
        for x in range(12, 28):
            if ((x - 20) / 8.5) ** 2 + ((y - 25) / 3.5) ** 2 <= 1.0:
                M.px(x, y, "s1" if (x + y) % 2 else "s2")
    for k in range(10):
        M.px(15 + k // 4, 26 - k, "s0")
        M.px(16 + k // 4, 26 - k, "e1")
    for y in range(2, 18):
        for x in range(2, 30):
            d = ((x - 16) / 13.5) ** 2 + ((y - 10) / 7.5) ** 2
            if d > 1.0:
                continue
            c = "alg"
            if y < 8 and (x + y) % 3:
                c = "ol1"
            if d > 0.8:
                c = "sk" if y > 10 else "alg"
            if (x * 5 + y * 3) % 11 == 0 and y < 12:
                c = "ol1"
            M.px(x, y, c)
    return s


def crag_islet(key, w, h, crags, notes):
    from akti_coast import crag
    s = Struct(key, "Rock islet", w, h, SEC, walk=["X" * w] * h, notes=notes)
    ground(s, "sea")
    for (pts, face, seed, shrub) in crags:
        crag(s.M, pts, face=face, seed=seed, shrub=shrub)
    return s


def crag_islets():
    return [
        crag_islet("islet_a", 3, 2, [
            ([(3, 6), (12, 2), (24, 3), (36, 1), (44, 7), (42, 14), (30, 17), (14, 18), (4, 14)], 9, 101, 3),
            ([(36, 18), (41, 16), (46, 19), (44, 24), (37, 23)], 4, 102, 0)],
            "A long rock islet, scrub on its back, a smaller rock at its foot."),
        crag_islet("islet_b", 2, 2, [
            ([(6, 4), (14, 1), (22, 3), (26, 10), (21, 17), (9, 18), (4, 12)], 10, 103, 1),
            ([(20, 20), (25, 18), (29, 21), (26, 25), (21, 25)], 3, 104, 0)],
            "A tall stack and its fallen piece."),
        crag_islet("islet_c", 3, 3, [
            ([(4, 10), (14, 3), (28, 2), (40, 8), (44, 20), (36, 30), (20, 32), (6, 26)], 11, 105, 5),
            ([(2, 34), (8, 32), (12, 35), (10, 40), (3, 39)], 3, 106, 0)],
            "A broad islet: a crown of scrub and thyme over a cliff on its south side."),
        crag_islet("islet_d", 2, 1, [
            ([(2, 5), (9, 2), (15, 4), (14, 9), (6, 10)], 3, 107, 0),
            ([(16, 3), (24, 1), (30, 5), (27, 10), (18, 10)], 4, 108, 1)],
            "Two low rocks side by side."),
    ]


def reef_sea(key, seed, cluster):
    from akti_coast import crag
    s = Struct(key, "Reef awash, open sea", 1, 1, SEC, walk=["X"],
               notes="Low rocks just breaking the surface, on the live sea. Solid.")
    ground(s, "sea")
    for pts, face in cluster:
        crag(s.M, pts, face=face, seed=seed, shrub=0)
    return s


def reefs_sea():
    return [
        reef_sea("reefs_a", 111, [([(2, 6), (7, 4), (11, 6), (9, 10), (3, 10)], 3),
                                  ([(10, 11), (13, 10), (15, 12), (12, 14)], 2)]),
        reef_sea("reefs_b", 112, [([(3, 3), (8, 2), (10, 5), (6, 7), (2, 6)], 2),
                                  ([(7, 9), (12, 8), (14, 11), (11, 13), (6, 12)], 3)]),
        reef_sea("reefs_c", 113, [([(1, 8), (5, 6), (8, 8), (6, 11), (2, 11)], 2),
                                  ([(9, 3), (13, 2), (15, 5), (12, 7)], 2),
                                  ([(10, 10), (14, 9), (15, 12), (11, 13)], 2)]),
    ]


def mooring_post():
    """A landing's mooring post: a tarred pole in the water, a rope's eye on it
    and a ring of foam. Solid."""
    s = Struct("mooring_post", "Mooring post", 1, 1, SEC, walk=["X"],
               notes="Marks a landing: the bg event is on the water next to it.")
    ground(s, "sea")
    M = s.M
    for y in range(2, 13):
        M.px(7, y, "wd0")
        M.px(8, y, "wd1")
    M.blit(["kkkk", "k22k"], {"k": "ink", "2": "wd2"}, 6, 1)
    M.blit(["rrrr", "r  r", "rrrr"], {"r": "rp"}, 6, 6)
    for x in (5, 6, 9, 10):
        M.px(x, 13, "w0")
    M.px(7, 13, "b2")
    M.px(8, 13, "w0")
    return s


# --------------------------------------------------------------------------
# Set pieces in the sea
# --------------------------------------------------------------------------

def wreck():
    """A merchant ship aground on a reef, broken-backed, bow up and to the left:
    her ribs open on the near side, the mast snapped, amphorae spilling."""
    s = Struct("wreck", "Wreck aground", 4, 3, SEC,
               walk=["XXXX", "XXXX", "XXX."],
               notes="Solid but the last cell. Hidden item on her deck (a bg event).")
    ground(s, "sea")
    M = s.M
    # hull: a long tilted shape; deck planks above, the side below
    hull_top = lambda x: int(14 - 7 * math.exp(-((x - 6) / 9.0) ** 2) + 0.06 * x)
    for x in range(3, 58):
        t = hull_top(x)
        side = 14 if x < 44 else 14 - (x - 44) // 3
        for y in range(t, t + 6):                  # the deck, sloping
            c = "wd3" if (y - t) % 3 else "wd2"
            if (x + (y - t) * 5) % 13 == 0:
                c = "wd1"
            M.px(x, y, c)
        for y in range(t + 6, t + 6 + side):       # the side, planked
            k = y - (t + 6)
            c = "wd1" if k % 3 else "wd0"
            if k == 0:
                c = "rd"
            if x > 26 and x < 40 and 3 < k < side - 2:
                # the breach: the ribs show
                c = "ink" if x % 4 else "wd2"
            M.px(x, y, c)
        M.px(x, t, "ink")
        M.px(x, t + 6 + side, "wd0" if x % 3 else "ink")
    # the bow post and the stern's broken end
    for k in range(8):
        M.px(3 - k // 3, hull_top(3) - k, "wd0")
        M.px(4 - k // 3, hull_top(3) - k, "wd1")
    for y in range(hull_top(57), hull_top(57) + 14):
        M.px(57 + (y % 3) - 1, y, "wd0")
    # the snapped mast and a rag of sail
    mx = 24
    for y in range(hull_top(mx) - 12, hull_top(mx) + 2):
        M.px(mx, y, "wd0")
        M.px(mx + 1, y, "wd2")
    M.blit(["rrrw ", " rrww", "  rw "], {"r": "rp", "w": "w0"}, mx + 2, hull_top(mx) - 11)
    M.px(mx, hull_top(mx) - 13, "ink")
    # amphorae spilled across the deck and into the shallows
    amph = [" kk ", "kttk", "kTtk", " kk "]
    for (x, y) in ((12, 10), (17, 8), (33, 11), (50, 33), (56, 40)):
        M.blit(amph, {"k": "ink", "t": "tc1", "T": "g0"}, x, y)
    # foam where the sea breaks on her
    for x in range(2, 60):
        y = hull_top(x) + 6 + (14 if x < 44 else 14 - (x - 44) // 3) + 1
        if (x * 7) % 5 < 3:
            M.px(x, y, "w0")
    return s


def debris(key, seed):
    """Floating timbers from the wreck: passable."""
    s = Struct(key, "Floating timbers", 1, 1, SEC, walk=["."],
               notes="Planks adrift; passable sea.")
    ground(s, "sea")
    rng = random.Random(seed)
    for _ in range(2):
        x, y = rng.randrange(1, 8), rng.randrange(2, 13)
        ln = rng.randrange(6, 10)
        for i in range(ln):
            s.M.px(x + i, y, "wd2" if i % 4 else "wd1")
            s.M.px(x + i, y + 1, "wd0")
        s.M.px(x - 1, y, "w0")
        s.M.px(x + ln, y + 1, "w0")
    return s


def stone_ship():
    """The Phaeacians' ship that carried Odysseus home, which Poseidon struck to
    stone with the flat of his hand as she came back into harbor (Odyssey 13.159-
    164): a ship in every line, oars out, all of it limestone."""
    s = Struct("stone_ship", "The stone ship", 5, 2, SEC,
               walk=["XXXXX", "XXXXX"],
               notes="The set piece off Kerkyra. Solid; read it from the water.")
    ground(s, "sea")
    M = s.M
    W, H = 80, 32
    keel = lambda x: 22 - int(5 * math.exp(-((x - 74) / 6.0) ** 2))         # stern rises at the right
    deck = lambda x: 9 + int(3 * math.exp(-((x - 40) / 30.0) ** 2)) - int(6 * math.exp(-((x - 74) / 5.0) ** 2))
    body = np.zeros((H, W), bool)
    for x in range(6, 78):
        top = deck(x)
        bot = keel(x)
        if x < 12:                                 # the ram and the bow's rise
            top = 10 - (12 - x) // 2
            bot = 20 + (12 - x) // 3
        body[max(0, top):min(H, bot), x] = True
    # the stern's curl
    for k in range(10):
        x, y = 76 - k // 3, 4 + k
        body[y, x] = body[y, x - 1] = True
    face_rows = 7
    for y in range(H):
        for x in range(W):
            if not body[y, x]:
                continue
            top = not body[y - 1, x] if y else True
            t = deck(x) if x >= 12 else 10 - (12 - x) // 2
            if y < t + 4:
                c = "s5" if top else ("s4" if (x + y) % 7 else "s3")       # the deck, sunlit
            elif y < t + 4 + face_rows + 4:
                k = y - (t + 4)
                c = "s3" if k == 0 else ("s2" if k % 3 else "s1")         # the hull's strakes
            else:
                c = "s2"
            M.px(x, y, c)
    # oars: stone ridges down the side, each ending in a blade awash
    for i, x in enumerate(range(16, 70, 6)):
        t = deck(x) + 5
        for k in range(10):
            M.px(x - k // 3, t + k, "s4" if k < 8 else "s5")
            M.px(x - k // 3 + 1, t + k, "s1")
        M.px(x - 3, t + 10, "w0")
        M.px(x - 2, t + 10, "w0")
    # the waterline: wet stone, weed, foam
    for x in range(4, 79):
        ys = [y for y in range(H) if body[y, x]]
        if not ys:
            continue
        b = max(ys)
        M.px(x, b, "wt0")
        M.px(x, b - 1, "alg" if x % 3 else "wt1")
        if b + 1 < H:
            M.px(x, b + 1, "w0" if x % 4 else "b3")
        if b + 2 < H and x % 3 == 0:
            M.px(x, b + 2, "b3")
    # outline
    pad = np.pad(body, 1)
    edge = body & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    for y, x in zip(*np.nonzero(edge)):
        if M.get(x, y) not in ("s5", "wt0"):
            M.px(x, y, "sk")
    # the painted eye at the bow, worn into the stone, and a gull on the stern post
    M.blit([" kk ", "k55k", " kk "], {"k": "sk", "5": "s5"}, 9, 12)
    M.blit([" ww  ", "wwwws", " ss  ", " k k "], {"w": "w0", "s": "wt1", "k": "sk"}, 70, 0)
    return s


def birds_rock():
    """A stack white with the gulls' droppings, their nests in its ledges."""
    from akti_coast import crag
    s = Struct("birds_rock", "The birds' rock", 2, 2, SEC, walk=["XX", "XX"],
               notes="Gulls on a guano-streaked stack; a hidden item in its foot.")
    ground(s, "sea")
    M = s.M
    crag(M, [(5, 6), (12, 2), (21, 1), (27, 6), (28, 14), (22, 19), (10, 20), (4, 14)],
         face=8, seed=91, shrub=0)
    rng = random.Random(9)
    # droppings: white runs down the face from the ledges
    for _ in range(14):
        x, y = rng.randrange(6, 26), rng.randrange(4, 18)
        if M.get(x, y) not in ("s1", "s2", "s3", "s4", "s5"):
            continue
        for k in range(rng.randrange(2, 6)):
            if M.get(x, y + k) in ("s1", "s2", "s3", "s4", "s5", "wt1"):
                M.px(x, y + k, "w0" if k < 3 else "s5")
    gull = [" ww  ", "wwwwk", "  s  "]
    for (x, y) in ((9, 3), (18, 2), (22, 9), (12, 12)):
        M.blit(gull, {"w": "w0", "k": "sk", "s": "wt1"}, x, y)
    # a nest of twigs on the summit
    M.blit(["e1e1e", "1e1e1"], {"e": "e1", "1": "s1"}, 13, 6)
    return s


def altar_stack():
    """Poseidon's altar on a sea stack: a small marble altar with a trident
    relief, under a little blue-roofed canopy, on a crag the sea has undercut.
    The altar runs EventScript_IchorAltar_Poseidon (a bg event on its cell)."""
    from akti_coast import crag
    s = Struct("altar_stack", "Poseidon's altar on its stack", 2, 3, SEC,
               walk=["XX", "XX", "XX"],
               notes="Rows 1-2 are the stack; row 0 the altar and canopy. Read from the sea "
                     "at row 2.")
    ground(s, "sea")
    M = s.M
    # the stack: a tall crag drawn in the shrine group's stone (s1-s4, sk)
    crag(M, [(3, 16), (10, 12), (22, 12), (29, 16), (27, 30), (24, 36), (8, 36), (4, 28)],
         face=10, seed=95, shrub=0)
    for y in range(48):
        for x in range(32):
            c = M.get(x, y)
            if y < 32 and c in ("s5",):
                M.px(x, y, "s4")
            if y < 32 and c in ("s0", "e1", "e2", "wt0", "wt1", "alg", "ol1"):
                M.px(x, y, "s1")
            if y < 32 and c in ("w0", "b3"):
                M.px(x, y, None)
    # the canopy: two posts, a blue roof, a gold finial
    M.blit(["     g      ",
            "    bbbb    ",
            "   bBBBBb   ",
            "  bBBBBBBb  ",
            " kkkkkkkkkk ",
            "  m      m  ",
            "  m      m  ",
            "  m      m  ",
            "  m      m  ",
            "  m      m  "], {"g": "g1", "b": "b0", "B": "b1", "k": "ink", "m": "m2"}, 10, 0)
    # the altar block with its trident
    M.blit(["kkkkkkkk",
            "kw1111wk",
            "k1m2b2mk",
            "k1mbbbmk",
            "k1m2b2mk",
            "k3333333",
            "kkkkkkkk"], {"k": "ink", "w": "w0", "1": "m1", "m": "m2", "2": "m3", "b": "b1",
                          "3": "m4"}, 12, 7)
    return s


# --------------------------------------------------------------------------
# Halia's islet
# --------------------------------------------------------------------------

def hut():
    """Halia's hut: a low reed-thatched cottage of rough whitewashed stone, its
    roof weighed down with stones on ropes against the west wind, a smoke hole
    over the hearth, a small window and a plank door."""
    s = Struct("hut", "Halia's reed-thatched hut", 3, 3, SEC,
               walk=["XXX", "XXX", "XDX"],
               notes="On aethos grass. The door (row 2, middle) warps into the hut.")
    ground(s, "grass")
    M = s.M
    # walls: rows 20-47
    for y in range(22, 46):
        for x in range(3, 45):
            c = "w1"
            if (x * 3 + y * 7) % 23 == 0:
                c = "w2"
            if (y - 22) % 6 == 5 and (x + (y // 6) * 3) % 9 < 4:
                c = "w2"                                    # the rough coursing shows through
            if y > 41:
                c = "s3" if (x + y) % 5 else "s2"           # a stone footing
            M.px(x, y, c)
    for y in range(22, 46):
        M.px(3, y, "w3")
        M.px(44, y, "w3")
        M.px(4, y, "w2")
    M.hline(3, 44, 46, "s1")
    # the door, centred in the middle cell
    for y in range(31, 47):
        for x in range(19, 29):
            c = "wd1" if (x - 19) % 3 else "wd0"
            if y == 31 or x in (19, 28):
                c = "ink"
            M.px(x, y, c)
    M.px(26, 39, "th4")
    # a window with a shutter, and a pot by the door
    M.blit(["kkkkk", "kwkwk", "kkkkk", "kwkwk", "kkkkk"], {"k": "ink", "w": "wd1"}, 8, 29)
    M.blit([" kk ", "k33k", "k22k", " kk "], {"k": "ink", "3": "s3", "2": "s2"}, 33, 41)
    # the roof: a fat thatch, ridged, rounded at the eaves, overhanging the walls
    for y in range(0, 28):
        for x in range(0, 48):
            eave = 26 if 2 <= x <= 45 else 25
            inset = max(0, 6 - y) if y < 6 else 0
            if x < inset or x > 47 - inset or y > eave:
                continue
            # straw bundles: diagonal strokes, darker in the courses' shadows
            k = (x + (y // 4) * 2) % 4
            c = "th3" if k == 0 else "th2" if k < 3 else "th1"
            if y % 4 == 3:
                c = "th1" if x % 2 else "th2"
            if y < 3:
                c = "th4" if x % 3 else "th3"
            if y >= eave - 1:
                c = "th0" if x % 2 else "th1"
            M.px(x, y, c)
    # the ridge and the weighting ropes with their stones
    M.hline(6, 41, 1, "th0")
    for rx in (10, 24, 38):
        for y in range(2, 24):
            M.px(rx, y, "th0" if y % 2 else "s1")
        M.blit(["k22k", "k33k", " kk "], {"k": "ink", "2": "s2", "3": "s3"}, rx - 2, 22)
    # the smoke hole and a wisp
    M.blit(["kkkk", "k  k", "kkkk"], {"k": "ink"}, 28, 4)
    M.blit([" w", "w ", " w"], {"w": "w2"}, 29, 0)
    return s


def jetty(key, kind):
    """The islet's plank jetty on posts, over the live sea. Walkable."""
    s = Struct(key, f"Jetty ({kind})", 1, 1, SEC, walk=["."],
               notes="Planks on posts over aethos's sea; walk on it, land from it.")
    ground(s, "sea")
    M = s.M
    if kind in ("h", "end_e", "end_w"):
        x0 = 0 if kind != "end_w" else 3
        x1 = 15 if kind != "end_e" else 12
        for y in range(3, 13):
            for x in range(x0, x1 + 1):
                c = "wd3" if (x // 4 + y) % 2 else "wd2"
                if x % 4 == 3:
                    c = "wd1"
                if y in (3, 12):
                    c = "wd0"
                M.px(x, y, c)
        for x in range(x0, x1 + 1):
            M.px(x, 13, "ink" if x % 4 == 0 else None)
        for px in ((1, 13) if kind == "h" else (x0 + 1, x1 - 1)):
            M.vline(px, 13, 15, "wd0")
        if kind != "h":
            bx = x1 - 3 if kind == "end_e" else x0 + 1
            M.blit([" kk ", "k12k", "k12k", "k12k", " kk "], {"k": "ink", "1": "wd1", "2": "wd2"}, bx, 1)
            M.blit(["rrr"], {"r": "rp"}, bx, 6)
    else:  # "v": planks running north-south
        for y in range(0, 16):
            for x in range(3, 13):
                c = "wd3" if (y // 4 + x) % 2 else "wd2"
                if y % 4 == 3:
                    c = "wd1"
                if x in (3, 12):
                    c = "wd0"
                M.px(x, y, c)
        M.vline(13, 0, 15, "ink")
    return s


def raft():
    """Kymon's raft: six logs lashed with rope, a stub mast and a basket."""
    s = Struct("raft", "Kymon's raft", 2, 1, SEC, walk=["XX"],
               notes="On the live sea. Kymon stands on the left cell.")
    ground(s, "sea")
    M = s.M
    for i in range(6):
        y = 3 + i * 2
        for x in range(2, 30):
            M.px(x, y, "wd2" if x % 5 else "wd1")
            M.px(x, y + 1, "wd1")
        M.px(1, y, "wd0")
        M.px(30, y + 1, "wd0")
    for x in (7, 22):
        M.vline(x, 3, 14, "rp")
    for x in range(1, 31):
        M.px(x, 15, "w0" if x % 3 else None)
    M.blit(["kkkk", "k12k", "k21k", "kkkk"], {"k": "ink", "1": "wd3", "2": "rp"}, 22, 5)
    return s


def build():
    import akti_coast
    pieces = (rock_pieces() + [rock_cypress()] + shoal_pieces() + reef_pieces()
              + current_pieces() + [whirlpool()] + ram_rocks() + fog_pieces()
              + [wreck(), debris("debris_a", 3), debris("debris_b", 8), stone_ship(),
                 birds_rock(), altar_stack(), hut(),
                 jetty("jetty_h", "h"), jetty("jetty_end_e", "end_e"), raft()]
              + [akti_coast.net_poles(), akti_coast.boat_beached(),
                 akti_coast.sea_stack(), akti_coast.sea_rocks()]
              + [rock_scrub_piece(p) for p in ((0, 0), (1, 0), (0, 1), (1, 1))]
              + [rock_pine()] + crag_islets() + reefs_sea() + [mooring_post()])
    for s in pieces:
        s.section = SEC
    return pieces
