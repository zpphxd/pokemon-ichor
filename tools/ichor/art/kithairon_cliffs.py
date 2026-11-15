"""Kithairon's mountain: cliffs with height, and what grows and falls on them.

The polish pass (design/phase3/TILES_kithairon.md, "Polish pass") replaced the
old `crag`, a flat grey slab with a 14 px face that read as paving, with a
tiered landscape: the map builder gives every cell a height (a tier), and every
raised tier is outlined by these pieces.

  cliff        one piece per boundary shape of a raised tier, on borrowed grass:
               a rocky rim along its north, west and east edges, and along its
               south edge a lit lip over a 24 px limestone face with strata and
               cracks, darkening to a cast shadow at the foot. The face takes the
               tier's two southmost rows, so a cliff reads as a wall you could
               not climb. The tier's inside is left to the map: grass, firs, the
               road. Keys are blob shape keys plus one bit, `|1` or `|0`: is the
               tier still there two rows down (`|0` marks the face's upper row).
  cliff_face   face variants the builder scatters along a cliff, upper (`_u`) and
               lower (`_l`) row: ivy, a crack with a fern, a tuft on a ledgelet,
               a seep; and the cave mouth (lower row, a door).
  cliff_stair  rock steps cut through a two-row face for the road, 2 wide
               (`TL`, `TR` over `BL`, `BR`) and 1 wide (`T`, `B`), on borrowed
               road.
  ledge        one-way rock ledges: `S_*` drop south (MB_JUMP_SOUTH, the way
               home on Mt. Kithairon), `N_*` drop north (MB_JUMP_NORTH, the way
               down Route 7's north face). L, M, R.
  rocks        impassable rocky ground for a tier's top: a boulder pile, a split
               crag with a juniper, a scree heap.
  deadfall     a fallen fir across the ground (2 wide), a stump, a snag.

Light from the top left, as the rest of the crossing.
"""
from __future__ import annotations

import math

import numpy as np

import kithairon_ground as G
import kithairon_lib as K

SEC = "cliff"
LIP, FACE, FOOT = 2, 24, 2          # the south edge, from the tier's top down
RIM = 3                             # the rim along the other edges

_GRASS = None


def grass_px(x, y):
    """The name of aethos grass's color at (x, y), phase-locked to 16 px."""
    global _GRASS
    if _GRASS is None:
        _GRASS = K.aethos(K.GRASS)
    return G.A_name(_GRASS[y % 16, x % 16])


def shade(name, steps=1):
    ramp = {"g3": "g2", "g2": "g1", "g1": "gd", "gd": "gd"}
    for _ in range(steps):
        name = ramp.get(name, name)
    return name


# --------------------------------------------------------------------------
# The cliff's boundary shapes
# --------------------------------------------------------------------------

DIRS = K.DIRS


def tall_region(key):
    """64 x 48 bool canvas round a cell (rows y-1 .. y+2): the tier."""
    parts = key.split("|")
    neigh, s2 = parts[1], (parts[2] if len(parts) > 2 else "1")
    s2 = s2[:1]
    R = np.zeros((64, 48), bool)
    R[16:32, 16:32] = True
    for st, (dx, dy) in zip(neigh, DIRS):
        if st == "1":
            R[16 + dy * 16:32 + dy * 16, 16 + dx * 16:32 + dx * 16] = True
    if neigh[4] == "1" and s2 == "1":
        R[48:64, 16:32] = True
        # the row two down continues the columns either side when they go on
        if neigh[5] == "1":
            R[48:64, 0:16] = True
        if neigh[3] == "1":
            R[48:64, 32:48] = True
    return R


def _wobble(seed, amp, h=64, w=48):
    y, x = np.mgrid[0:h, 0:w].astype(float)
    t = 2 * math.pi / 16
    f = (np.sin(t * 2 * x + seed) + np.sin(t * 2 * y + 1.7 * seed)
         + np.sin(t * (x + y) + 2.3 * seed) + 0.6 * np.sin(t * 3 * (x - y) + seed)) / 3.6
    return amp * f


def soft_tall(R, radius=5.5, amp=1.5, seed=3.7):
    """The tier rounded at its corners: open R with a round brush."""
    from scipy.ndimage import distance_transform_edt as edt
    h, w = R.shape
    if R.all():
        return R.copy()
    # distance from each pixel's center to the nearest outside pixel's center
    d_in = edt(R)
    core = d_in > radius + 0.5
    if not core.any():
        return np.zeros_like(R)
    d_core = edt(~core)
    return (d_core <= radius + _wobble(seed, amp, h, w)) & R


# The face is built of rounded blocks of limestone, three courses deep, each
# course's joints offset from the last so no seam runs straight down. Seeds are
# (x, depth, half-width, half-height); x repeats every 16 px.
_BLOCKS = [
    (3, 5, 4.4, 7.5), (10.5, 3.5, 3.4, 6.0), (18.5, 6, 4.8, 8.0), (26.5, 4, 3.6, 6.5),
    (15, 1, 1.8, 1.8), (31, 1.5, 2.0, 2.2),
    (7, 17, 4.6, 6.5), (14.5, 19, 3.0, 5.5), (22, 17.5, 4.4, 7.0), (29.5, 19, 3.4, 6.0),
    (14.5, 12, 2.2, 2.0), (1, 22, 2.4, 2.0), (25.5, 12.5, 1.8, 1.6),
]
_RAMP = ["rk5", "rk4", "rk3", "rk2", "rk1", "rk0"]


def _block_field(w, h, blocks, wrap=16):
    near = np.zeros((h, w), int)
    gap = np.zeros((h, w), float)
    uu = np.zeros((h, w), float)
    for y in range(h):
        for x in range(w):
            ds = []
            for i, (bx, by, rx, ry) in enumerate(blocks):
                dx = (x - bx) % wrap
                dx = dx - wrap if dx > wrap / 2 else dx
                dy = y - by
                ds.append((((dx / rx) ** 2 + (dy / ry) ** 2) ** 0.5, i, dx / rx + dy / ry))
            ds.sort()
            near[y, x] = ds[0][1]
            gap[y, x] = ds[1][0] - ds[0][0]
            uu[y, x] = ds[0][2]
    return near, gap, uu


_FN, _FG, _FU = _block_field(32, FACE, _BLOCKS, wrap=32)


def face_px(x, d):
    """The limestone face at column x (period 32: a face cell's phase picks
    which half), depth d below the lip (0 .. FACE-1): tall slabs lit on their
    upper left, dark joints, the whole face darkening toward its foot; a
    shadow under the lip's overhang."""
    xx = x % 32
    if d == 0:
        return "rk1" if (xx * 3) % 5 else "rk2"
    if d >= FACE - 1:
        return "rk0"
    g, u = _FG[d, xx], _FU[d, xx]
    if g < 0.28:
        return "rk0" if d > 8 else "rk1"
    k = 0 if u < -1.15 else (1 if u < -0.35 else (2 if u < 0.35 else (3 if u < 0.95 else 4)))
    if g < 0.5 and k < 3:
        k += 1                          # each block's rim, a shade down
    k += (d >= 14) + (d >= FACE - 4)    # deeper, darker
    return _RAMP[min(k, 5)]


_RIM_BLOCKS = [(3, 3, 3.0, 2.5), (9, 2, 2.5, 2.2), (14, 5, 2.6, 2.6), (6, 8, 2.8, 2.4),
               (12, 11, 3.0, 2.6), (2, 12, 2.4, 2.4), (8, 14, 2.5, 2.0)]
_RIM_ALL = [(bx, by + dy, rx, ry) for (bx, by, rx, ry) in _RIM_BLOCKS for dy in (-16, 0, 16)]
_RN, _RG, _RU = _block_field(16, 16, _RIM_ALL)


def rim_width(x, y):
    """How far the rocks reach in from an open edge: 3-5 px, ragged."""
    return 4 + K.hsh(x // 3, y // 3, 17) % 3


def rim_shade(x, y):
    """A shade index (0 lit .. 4 dark) for a rim pixel: small rounded stones."""
    xx, yy = x % 16, y % 16
    if _RG[yy, xx] < 0.3:
        return 3
    u = _RU[yy, xx]
    return 0 if u < -0.9 else (1 if u < -0.1 else (2 if u < 0.7 else 3))


def paint_cliff(s, ox, oy, key):
    """One boundary cell of a tier, on borrowed grass (the middle layer)."""
    R = tall_region(key)
    V = soft_tall(R)
    M = s.M
    phase = 16 if key.endswith("|b") else 0
    cy0, cx0 = 16, 16
    # run of tier below each pixel, per column: how far to the south edge
    below = np.zeros(V.shape, int)
    for x in range(V.shape[1]):
        run = 0
        for y in range(V.shape[0] - 1, -1, -1):
            if V[y, x]:
                below[y, x] = run
                run += 1
            else:
                run = 0
    # extends past the canvas: the tier goes on south of it
    deep = R[63, :]
    for x in range(V.shape[1]):
        if deep[x]:
            for y in range(V.shape[0] - 1, -1, -1):
                if not V[y, x]:
                    break
                below[y, x] += 99
    # distance to outside, westward / eastward / northward, within the tier's top
    def dist(dx, dy, lim):
        d = np.full(V.shape, lim, int)
        for y in range(V.shape[0]):
            for x in range(V.shape[1]):
                if not V[y, x]:
                    continue
                for k in range(lim):
                    xx, yy = x + dx * (k + 1), y + dy * (k + 1)
                    if not (0 <= xx < V.shape[1] and 0 <= yy < V.shape[0]):
                        break
                    if not V[yy, xx]:
                        d[y, x] = k
                        break
        return d
    dw, de, dn = dist(-1, 0, 8), dist(1, 0, 8), dist(0, -1, 8)
    for y in range(16):
        for x in range(16):
            gy, gx = cy0 + y, cx0 + x
            if not V[gy, gx]:
                # outside the tier inside this cell: its foot, or a corner. East
                # of the tier, a sliver of shadow.
                if V[gy, max(0, gx - 1)] or V[gy, max(0, gx - 2)]:
                    M.px(ox + x, oy + y, shade(grass_px(x, y)))
                continue
            b = below[gy, gx]
            if b < FOOT:
                M.px(ox + x, oy + y, shade(grass_px(x, y), 2 if b == FOOT - 1 else 1))
                continue
            if b < FOOT + FACE:
                d = FOOT + FACE - 1 - b
                c = face_px(x + phase, d)
                # the face's ends: lit on the west, dark on the east
                if dw[gy, gx] == 0:
                    c = "ink" if d > 2 else "rk1"
                elif dw[gy, gx] == 1:
                    c = "rk4" if d < FACE - 3 else "rk2"
                elif de[gy, gx] == 0:
                    c = "ink"
                elif de[gy, gx] == 1:
                    c = "rk1"
                M.px(ox + x, oy + y, c)
                continue
            if b < FOOT + FACE + LIP:
                d = b - FOOT - FACE        # 0 just over the face, 1 the top edge
                c = "rk5" if d == 1 else ("rk4" if (x + y) % 5 else "rk5")
                if dw[gy, gx] == 0 or de[gy, gx] == 0:
                    c = "ink"
                if dn[gy, gx] == 0:
                    c = "ink"
                M.px(ox + x, oy + y, c)
                continue
            # the tier's top: a bevelled rock lip along any open edge (north,
            # west, east), lit north and west, shaded east; grass inside
            w_, e_, n_ = dw[gy, gx], de[gy, gx], dn[gy, gx]
            m_ = min(w_, e_, n_)
            h = K.hsh(x + phase, y, 41) % 9
            if m_ == 0:
                M.px(ox + x, oy + y, "ink")
            elif m_ < 4:
                if n_ == m_:
                    c = ("rk5", "rk4", "rk3")[m_ - 1]
                elif w_ == m_:
                    c = ("rk4", "rk3", "rk3")[m_ - 1]
                else:
                    c = ("rk1", "rk2", "rk3")[m_ - 1]
                if h == 0 and m_ > 1:
                    c = "rk2"
                M.px(ox + x, oy + y, c)
            elif m_ == 4 and (n_ == m_ or w_ == m_ or e_ == m_):
                # the lip's own shadow on the grass just inside it
                M.px(ox + x, oy + y, shade(grass_px(x, y)))


def cliff_keys(wanted):
    keys = [k for k in wanted if k.count("|") >= 2]
    return keys or ["1|11111111|0", "1|11100011|0"]


def cliff():
    import kithairon_ground as GG
    keys = cliff_keys(GG.wanted("cliff"))
    s = K.shape_set("cliff", "Cliffs: the edges of a raised tier", SEC, keys, paint_cliff, "X",
                    "The boundary of a raised tier, on borrowed grass: a rocky rim on its "
                    "north, west and east edges, and on its south edge a lit lip over a "
                    "24 px limestone face that takes the tier's two southmost rows and "
                    "darkens to a shadow at its foot. The tier's inside is ordinary ground. "
                    "Names are blob shape keys plus `|1` (the tier goes on two rows down) or "
                    "`|0` (this is the face's upper row). Blocks.", on="grass")
    return s


# --------------------------------------------------------------------------
# Face variants, stairs, ledges
# --------------------------------------------------------------------------

UPPER, LOWER = "1|11100011|0", "1|11100011"   # a mid-face cell, upper and lower row


def _face_cell(L, ox, oy, row):
    """A plain mid-face cell (row 0 upper, 1 lower), painted as the cliff set
    paints it, so variants match their neighbors."""
    tmp = K.struct("_tmp", "", 1, 1, SEC, on="grass")
    paint_cliff(tmp, 0, 0, UPPER if row == 0 else LOWER)
    L.a[oy:oy + 16, ox:ox + 16] = tmp.M.a[0:16, 0:16]
    return tmp


def _ivy(L, ox, oy, y0, y1, density, seed, marked=False):
    for y in range(y0, y1):
        for x in range(16):
            h = K.hsh(x, y, seed) % 100
            hang = (x * 7 + seed) % 5 < 3 and y < y0 + 3 + (x * 13 + seed) % 14
            if (h < density * 100 * (0.6 if not hang else 1.0)) and (hang or h < 25):
                u = (x + y) % 4
                L.px(ox + x, oy + y, "iv2" if u == 0 else ("iv1" if u < 3 else "iv0"))
    if marked:
        for (x, y) in ((3, 4), (9, 6), (12, 11), (5, 12), (7, 2), (13, 3)):
            if y0 <= y < y1:
                L.px(ox + x, oy + y, "mk")
                L.px(ox + x + 1, oy + y, "mk")
                L.px(ox + x, oy + y + 1, "iv0")


def cliff_face():
    names = {"ivy_u": (0, 0), "crack_u": (1, 0), "tuft_u": (2, 0), "marked_u": (3, 0),
             "ivy_l": (0, 1), "seep_l": (1, 1), "fern_l": (2, 1), "marked_l": (3, 1),
             "mouth": (4, 1), "plain_u": (4, 0)}
    s = K.struct("cliff_face", "Cliff faces: ivy, cracks, the marked ivy, a cave mouth", 5, 2, SEC,
                 walk=["XXXXX", "XXXXD"], names=names, on="grass",
                 notes="Mid-face cells to scatter along a cliff's south face: `_u` for its "
                       "upper row (blob key `1|11100011|0`), `_l` for its lower row (`1|11100011`). "
                       "`ivy` hangs from the lip, `crack_u` splits the face with a fern, "
                       "`tuft_u` a grass tuft on a ledgelet, `seep_l` a dark wet streak, "
                       "`fern_l` a fern at the foot. `marked_u` over `marked_l` is the marked "
                       "ivy of the Thyrsus walls (gift II). `mouth` is a cave mouth in the lower "
                       "row (MB_NON_ANIMATED_DOOR: put the warp there).")
    M = s.M
    for (cx, cy) in names.values():
        _face_cell(M, cx * 16, cy * 16, cy)
    # upper row: the lip is at y 2-3, the face below it
    _ivy(M, 0, 0, 3, 16, 0.55, seed=5)
    _ivy(M, 0, 16, 0, 10, 0.45, seed=6)
    # a crack with a fern growing from it
    for i, (x, y) in enumerate(((6, 4), (7, 5), (7, 6), (8, 7), (8, 8), (9, 9), (9, 10), (10, 11),
                                (10, 12), (11, 13), (11, 14), (12, 15))):
        M.px(16 + x, y, "rk0")
        M.px(16 + x + 1, y, "rk4" if i % 2 else "rk3")
    K.put(M, 16 + 2, 9, [".i.i", "iiii", ".jj.", "..j."], {"i": "iv1", "j": "iv0"})
    # a grass tuft on a ledgelet
    K.put(M, 32 + 3, 8, ["2.2.2...", "12121.2.", "11111121", "KKKKKKKK"],
          {"1": "g1", "2": "g2", "K": "rk1"})
    # the marked ivy: thick, gold-berried, from lip to foot
    _ivy(M, 48, 0, 3, 16, 0.8, seed=7, marked=True)
    _ivy(M, 48, 16, 0, 14, 0.8, seed=9, marked=True)
    # a seep: a dark wet streak down the lower face, moss at its foot
    for y in range(0, 14):
        for x in range(6, 9 + (y > 8)):
            if (x + y) % 3:
                M.px(16 + x, 16 + y, "rk1" if y < 10 else "rk0")
    K.put(M, 16 + 4, 16 + 11, ["iiiiii", "jiijii"], {"i": "iv1", "j": "iv0"})
    # a fern at the foot
    K.put(M, 32 + 3, 16 + 6, [
        "..j...j..",
        ".jij.jij.",
        "jiiijiiij",
        ".jiiiiij.",
        "..jjijj..",
        "....j....",
    ], {"i": "iv2", "j": "iv1"})
    # the cave mouth: a dark arch in the lower face, its lip lit
    K.put(M, 64 + 2, 16 + 0, [
        "...KKKKKK...",
        "..K000000K..",
        ".K00000000K.",
        "K0000000000K",
        "K0000000000K",
        "K0000000000K",
        "K0000000000K",
        "K0000000000K",
        "K0000000000K",
        "K0000000000K",
        "K0000000000K",
        "K0000000000K",
        "K0000000000K",
        "K0000000000K",
    ], {"K": "rk1", "0": "ink"})
    for y in range(1, 14):
        M.px(64 + 1, 16 + y, "rk4")
    for x in range(64 + 3, 64 + 13):
        M.px(x, 16 + 14, "rk1")
    s.behaviors[(4, 1)] = "MB_NON_ANIMATED_DOOR"
    return s


def _steps(L, ox, oy, w, cheeks):
    """Rock steps over 32 px: treads lit, risers shaded, a cut cheek each side."""
    # the plateau's surface at the top (borrowed road shows through: leave it)
    treads = [4, 10, 16, 22, 28]
    for y in range(4, 32):
        for x in range(w):
            k = max(t for t in treads if t <= y) if y >= 4 else None
            r = y - k
            c = "rk5" if r == 0 else ("rk4" if r == 1 else ("rk3" if r < 4 else "rk2"))
            if r == 5:
                c = "rk1"
            if K.hsh(ox + x, y, 77) % 13 == 0 and r > 1:
                c = "rk2"
            L.px(ox + x, oy + y, c)
    for y in range(0, 32):
        if "L" in cheeks:
            L.px(ox + 0, oy + y, "ink" if y > 2 else "rk1")
            L.px(ox + 1, oy + y, "rk1" if y > 3 else "rk3")
            L.px(ox + 2, oy + y, "rk2" if y > 3 else "rk4")
        if "R" in cheeks:
            L.px(ox + w - 1, oy + y, "ink" if y > 2 else "rk1")
            L.px(ox + w - 2, oy + y, "rk0" if y > 3 else "rk2")
    # the bottom step meets the lower ground
    for x in range(w):
        L.px(ox + x, oy + 31, "rk1" if x % 2 else "rk2")


def cliff_stair():
    names = {"TL": (0, 0), "TR": (1, 0), "BL": (0, 1), "BR": (1, 1), "T": (2, 0), "B": (2, 1)}
    s = K.struct("cliff_stair", "Rock steps cut through a cliff", 3, 2, SEC,
                 walk=["...", "..."], names=names, on="path",
                 notes="The road's way up a cliff: a two-row flight of rock steps cut through "
                       "the face, on borrowed road. 2 wide: `TL`, `TR` over `BL`, `BR`; 1 wide: "
                       "`T` over `B`. Put them in the face's two rows; the face's own cells "
                       "either side stay as they are. Walkable.")
    tmp = K.Layer(48, 32)
    _steps(tmp, 0, 0, 32, "LR")
    _steps(tmp, 32, 0, 16, "LR")
    s.M.a[:] = tmp.a
    return s


def ledges():
    names = {"S_L": (0, 0), "S_M": (1, 0), "S_R": (2, 0), "N_L": (0, 1), "N_M": (1, 1), "N_R": (2, 1)}
    s = K.struct("ledge", "Rock ledges: one way down", 3, 2, SEC, walk=["JJJ", "XXX"], names=names,
                 on="grass",
                 notes="`S_*` drop south (MB_JUMP_SOUTH): a knee-high step of grey rock with "
                       "grass above and its shadow below; the road home on Mt. Kithairon. "
                       "`N_*` drop north (MB_JUMP_NORTH): the same seen from above, the land "
                       "falling away beyond a rocky lip; the way down Route 7's north face. "
                       "L, M, R: the ends taper into the grass.")
    for i in range(3):
        s.behaviors[(i, 1)] = "MB_JUMP_NORTH"
    M = s.M
    # south: lip at y 6, face 6..11, shadow 12..13
    for cx, end in ((0, "L"), (1, "M"), (2, "R")):
        ox = cx * 16
        for x in range(16):
            gx = ox + x
            taper = (end == "L" and x < 3) or (end == "R" and x > 12)
            t = (3 - x if end == "L" else (x - 12 if end == "R" else 0)) if taper else 0
            top = 4 + t + (K.hsh(gx, 0, 3) % 2)
            bot = 12 - t // 2
            if bot <= top:
                continue
            M.px(gx, top - 1, "ink")
            M.px(gx, top, "rk5" if x % 4 else "rk4")
            for y in range(top + 1, bot):
                d = y - top
                c = face_px(x + 3, min(FACE - 2, d * 3))
                M.px(gx, y, c)
            M.px(gx, bot, "rk0")
            M.px(gx, bot + 1, shade(grass_px(x, bot + 1), 2))
            M.px(gx, bot + 2, shade(grass_px(x, bot + 2)) if x % 2 else grass_px(x, bot + 2))
    # north: the drop falls away at the cell's top
    for cx, end in ((0, "L"), (1, "M"), (2, "R")):
        ox = cx * 16
        for x in range(16):
            gx = ox + x
            taper = (end == "L" and x < 3) or (end == "R" and x > 12)
            t = (3 - x if end == "L" else (x - 12 if end == "R" else 0)) if taper else 0
            if t >= 3:
                continue
            lip = 5 + (K.hsh(gx, 1, 5) % 2)
            for y in range(0 + t, lip - 1):
                M.px(gx, 16 + y, shade(grass_px(x, y), 2 if y < lip - 2 else 1))
            M.px(gx, 16 + lip - 1, "ink")
            for y in range(lip, lip + 4 - t // 2):
                d = y - lip
                c = ("rk2", "rk4", "rk5", "rk3")[d] if (x // 3) % 2 else ("rk1", "rk3", "rk5", "rk4")[d]
                M.px(gx, 16 + y, c)
            M.px(gx, 16 + lip + 4 - t // 2, "rk1")
    return s


def rocks():
    names = {"pile": (0, 0), "split": (1, 0), "scree": (2, 0)}
    s = K.struct("rocks", "Rocky ground: boulders, a split crag, a scree heap", 3, 1, SEC,
                 walk=["XXX"], names=names, on="grass",
                 notes="Impassable rock for a tier's top or a wood's floor: `pile` a heap of "
                       "boulders, `split` a crag split by a juniper, `scree` a heap of broken "
                       "stone. On borrowed grass.")
    M = s.M

    def boulder(ox, oy, cx, cy, rx, ry):
        m = K.ellipse_mask(48, 16, cx, cy, rx, ry)
        for y, x in np.argwhere(m):
            u = (x - cx) / rx + (y - cy) / ry
            M.px(ox + x, oy + y, "rk5" if u < -1.0 else ("rk4" if u < -0.2 else ("rk3" if u < 0.6 else "rk2")))
        for y, x in np.argwhere(K.halo(m)):
            if M.a[oy + y, ox + x, 3] == 0 or y >= cy:
                M.px(ox + x, oy + y, "ink" if y >= cy else "rk1")
        for y, x in np.argwhere(K.halo(K.halo(m) | m)):
            if y > cy + ry - 2 and M.a[oy + y, ox + x, 3] == 0:
                M.px(ox + x, oy + y, shade(grass_px(x, y), 2))
    boulder(0, 0, 10.0, 9.5, 5.0, 4.5)
    boulder(0, 0, 4.5, 5.5, 3.5, 3.0)
    boulder(0, 0, 12.0, 3.5, 2.5, 2.2)
    # split crag: two halves with a juniper between
    boulder(0, 0, 21.0, 8.0, 4.5, 6.0)
    boulder(0, 0, 28.5, 9.0, 3.8, 5.5)
    m = K.ellipse_mask(48, 16, 25.0, 6.0, 3.5, 4.0)
    for y, x in np.argwhere(m):
        u = (x - 25) / 3.5 + (y - 6) / 4
        M.px(x, y, "iv2" if u < -0.5 else ("iv1" if u < 0.6 else "iv0"))
    for (x, y) in ((24, 12), (25, 13)):
        M.px(x, y, "rk0")
    # scree heap
    for (x, y, r) in ((36, 10, 3), (41, 9, 3), (39, 5, 2), (44, 12, 2), (34, 4, 2), (43, 4, 2), (38, 13, 2)):
        boulder(0, 0, float(x), float(y), r + 0.3, r * 0.8)
    return s


def deadfall():
    names = {"log_W": (0, 0), "log_E": (1, 0), "stump": (2, 0), "snag_top": (3, 0), "snag": (3, 1),
             "log_W_s": (0, 1), "log_E_s": (1, 1), "stump_s": (2, 1)}
    s = K.struct("deadfall", "Deadfall: a fallen fir, a stump, a dead snag", 4, 2, SEC,
                 walk=["XXXT", "XXXX"], names=names, on="grass",
                 notes="`log_W` + `log_E`: a fallen fir lying east-west, its broken top to "
                       "the west and its root plate to the east, moss along its back. `stump` "
                       "a fir stump, `snag_top` over `snag` a dead fir standing grey (its top "
                       "drawn over the player). `_s` copies stand on the woods' deep shade.")
    M = s.M
    # the log: a long cylinder, lit along its top
    for x in range(2, 28):
        for y in range(5, 12):
            d = y - 5
            c = ("k2", "k2", "k1", "k1", "k1", "fr0", "ink")[d]
            if d == 1 and (x * 7) % 5 == 0:
                c = "fr2"
            if d == 0 and x % 4 == 1:
                c = "fr3"
            if d in (2, 3) and (x * 3) % 7 == 0:
                c = "fr0"
            M.px(x, y, c)
        M.px(x, 4, "ink")
        if x % 3:
            M.px(x, 12, "gd")
            M.px(x, 13, shade(grass_px(x, 13)))
    # moss on its back
    for x in (6, 7, 8, 14, 15, 21, 22, 23):
        M.px(x, 5, "fr2")
        M.px(x, 4, "fr3")
    # broken top to the west: splinters
    K.put(M, 0, 5, ["Kk", "Kgk", "kK.", "Kg.", "K.."], {"K": "ink", "k": "k2", "g": "g3"})
    # root plate to the east: a disc of roots and earth standing on edge
    m = K.ellipse_mask(32, 16, 28.5, 7.0, 3.5, 6.5)
    for y, x in np.argwhere(m):
        c = "k1" if (x + y) % 3 else "fr0"
        if x < 27:
            c = "k2"
        M.px(x, y, c)
    for y, x in np.argwhere(K.halo(m)):
        M.px(x, y, "ink")
    for (x, y) in ((30, 2), (31, 5), (31, 9), (29, 13)):
        M.px(x, y, "k1")
    # the stump: cut rings
    m = K.ellipse_mask(16, 16, 7.5, 6.0, 5.5, 3.2)
    for y in range(6, 13):
        for x in range(2, 14):
            M.px(32 + x, y, "k1" if x < 6 else ("k2" if x < 10 else "k1"))
        M.px(32 + 2, y, "ink")
        M.px(32 + 13, y, "ink")
    for y, x in np.argwhere(m):
        r = ((x - 7.5) / 5.5) ** 2 + ((y - 6) / 3.2) ** 2
        M.px(32 + x, y, "g3" if r < 0.25 else ("k2" if r < 0.6 else ("g3" if r < 0.8 else "k1")))
    for y, x in np.argwhere(K.halo(m)):
        if y < 7:
            M.px(32 + x, y, "ink")
    for x in range(2, 14):
        M.px(32 + x, 13, "ink")
        M.px(32 + x, 14, shade(grass_px(x, 14), 2) if x % 2 else shade(grass_px(x, 14)))
    K.put(M, 32 + 1, 10, ["f..", "ff."], {"f": "fr2"})
    # the snag: a dead fir, grey and bare
    T = s.T
    for y in range(0, 16):
        w = 1 if y < 5 else 2
        for x in range(8 - w // 2, 8 + w):
            T.px(48 + x, y, "k2" if x < 8 else "k1")
    for (x0, y0, x1, y1) in ((8, 6, 3, 3), (9, 8, 13, 4), (8, 11, 2, 9), (9, 13, 14, 10)):
        T.line(48 + x0, y0, 48 + x1, y1, "k2")
    for y in range(16, 30):
        for x in range(6, 11):
            M.px(48 + x, y, "k2" if x < 8 else ("k1" if x < 10 else "ink"))
        M.px(48 + 5, y, "ink")
    for (x0, y0, x1, y1) in ((8, 19, 4, 16), (9, 21, 13, 17)):
        M.line(48 + x0, y0, 48 + x1, y1, "k2")
    for x in range(3, 14):
        M.px(48 + x, 30, "k1" if 5 < x < 11 else "gd")
        if x % 2:
            M.px(48 + x, 31, "gd")
    # the woods' shade copies: same pixels; the shade ground is borrowed below
    for cx in range(3):
        M.a[16:32, cx * 16:cx * 16 + 16] = M.a[0:16, cx * 16:cx * 16 + 16]
    s.ground = {}
    K.ground(s, "grass", [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)])
    K.ground(s, "shade", [(0, 1), (1, 1), (2, 1)])
    return s


def build():
    return [cliff(), cliff_face(), cliff_stair(), ledges(), rocks(), deadfall()]
