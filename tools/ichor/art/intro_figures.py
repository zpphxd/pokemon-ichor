"""Black-figure figures for the intro's frieze and the loom, pixel by pixel.

Hand-drawn grids for the small creatures and the Fates' tools; procedural
painters (seeded, so every run is identical) for the long shapes: olive trees,
the trireme, the ketos, the temple and Olympus. intro_screen.py places them.

Grid legend (black-figure conventions, as in title_fates.py):
  .  clay field (transparent: the pot shows through)
  #  black gloss
  i  incision: a line scratched through the black (also transparent)
  w  added white
  r  added red
Painters draw straight into index arrays with the same meaning:
  0 clay/incision, 1 ink, 2 white, 3 red.
"""
import math
import random

import numpy as np

import intro_lib as L
import title_fates as FATES

T, K, Wt, R = 0, 1, 2, 3          # transparent, ink, white, red
KEY = {"#": K, "i": T, "w": Wt, "r": R}


def to_array(grid):
    L.check(grid)
    a = np.zeros((len(grid), len(grid[0])), int)
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch != ".":
                a[y, x] = KEY[ch]
    return a


def stamp(img, arr, x0, y0):
    """Paste a painted array (0 = leave) into img; incisions need 'i' grids,
    so painted arrays mark incisions with -1."""
    h, w = arr.shape
    H, W = img.shape
    for y in range(h):
        for x in range(w):
            v = arr[y, x]
            if v == 0:
                continue
            yy, xx = y0 + y, x0 + x
            if 0 <= yy < H and 0 <= xx < W:
                img[yy, xx] = 0 if v < 0 else v


def grid_arr(grid):
    """Grid -> array where incisions are -1 (so stamp() cuts them)."""
    L.check(grid)
    a = np.zeros((len(grid), len(grid[0])), int)
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "i":
                a[y, x] = -1
            elif ch != ".":
                a[y, x] = KEY[ch]
    return a


def rim(arr):
    """Black-figure added white sits on the black: give white areas a 1 px ink
    rim wherever they would touch the clay."""
    out = arr.copy()
    h, w = arr.shape
    for y in range(h):
        for x in range(w):
            if arr[y, x] != 0:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h and arr[yy, xx] == Wt:
                    out[y, x] = K
                    break
    return out


def raster(draw, w, h, ss=4):
    """Rasterize vector drawing at ss x and reduce: a pixel takes the most
    common painted value of its block when at least half the block is
    painted. draw(canvas, s) paints with coordinates multiplied by s."""
    big = np.zeros((h * ss, w * ss), int)
    draw(big, ss)
    out = np.zeros((h, w), int)
    for y in range(h):
        for x in range(w):
            blk = big[y * ss:(y + 1) * ss, x * ss:(x + 1) * ss].ravel()
            nz = blk[blk != 0]
            if len(nz) * 2 >= ss * ss:
                vals, counts = np.unique(nz, return_counts=True)
                out[y, x] = vals[np.argmax(counts)]
    return out


def pad(arr, l=1, r=1, t=1, b=1):
    h, w = arr.shape
    out = np.zeros((h + t + b, w + l + r), int)
    out[t:t + h, l:l + w] = arr
    return out


# ==========================================================================
# Clotho (from the title), with her spindle lifted out to be a sprite
# ==========================================================================
SPINDLE_ROWS = range(42, 55)
SPINDLE_COLS = range(26, 34)


def clotho_static():
    g = [list(r) for r in FATES.CLOTHO]
    for y in SPINDLE_ROWS:
        for x in SPINDLE_COLS:
            g[y][x] = "."
    return grid_arr(["".join(r) for r in g])


CLOTHO_HAND = FATES.CLOTHO_HAND          # (31, 32): the thread leaves here
SPINDLE_ORIGIN = (26, 42)                # grid point of the sprite's (0, 0)


def spindle_frames():
    """8x16 sprite frames of the drop spindle turning: the shaft hangs from the
    thread, the whorl is a disc seen edge-on, and an added-white mark on its
    rim travels round as it turns (and hides behind it for a frame)."""
    frames = []
    for m in (0, 1, 2, 3, 4, 5, None):
        f = np.zeros((16, 8), int)
        f[0, 3] = Wt                     # the thread knotted at the hook
        for y in range(1, 14):
            f[y, 3] = K                  # shaft (title grid col 29 -> col 3)
        for y, (x0, x1) in ((8, (2, 4)), (9, (0, 6)), (10, (0, 6)), (11, (1, 5))):
            for x in range(x0, x1 + 1):
                f[y, x] = K
        if m is not None:
            f[10 if m < 5 else 9, (0, 1, 3, 5, 6, 4)[m]] = Wt
        frames.append(f)
    return frames


KALATHOS = [
    "...w.ww.w.ww...",
    "..wwwwwwwwwwww.",
    "#.wwwwwwwwwww.#",
    "###############",
    ".#i#i#i#i#i#i#.",
    ".#############.",
    "..#i#i#i#i#i#..",
    "..###########..",
    "..#i#i#i#i#i#..",
    "...#########...",
    "...#rrrrrrr#...",
    "...#########...",
]


# ==========================================================================
# The olive grove of Elaia
# ==========================================================================
def olive_tree(seed, w=64, h=78, lean=0.0, with_boughs=False):
    """A gnarled olive: a twisting trunk forking into boughs, each bough
    carrying a leafy mass with incised leaves, and a few white olives."""
    rnd = random.Random(seed)
    a = np.zeros((h, w), int)
    base_x = w // 2 + int(lean * 6)
    # trunk: two twisting strands that meet, wide at the root
    pts = []
    x = base_x
    for i, y in enumerate(range(h - 1, h - 34, -1)):
        x += lean * 0.25 + math.sin(i * 0.35 + seed) * 0.35
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        wid = 7.5 - i * 0.12
        L.line(a, x - wid / 2, y, x + wid / 2, y, K, 1)
    # roots
    L.line(a, base_x - 4, h - 1, base_x - 9, h - 1, K, 2)
    L.line(a, base_x + 4, h - 1, base_x + 8, h - 1, K, 2)
    # bark: incised twists in the trunk
    for i in range(3, len(pts) - 4, 4):
        x, y = pts[i]
        L.line(a, x - 2, y, x + 1, y - 3, T, 1)
    top_x, top_y = pts[-1]
    # boughs
    boughs = []
    for ang, ln in ((-2.3, 20), (-1.55, 22), (-0.85, 20), (-2.75, 14), (-0.35, 15)):
        ang += rnd.uniform(-0.15, 0.15)
        ex = top_x + math.cos(ang) * ln
        ey = top_y + math.sin(ang) * ln
        mx = (top_x + ex) / 2 + rnd.uniform(-3, 3)
        my = (top_y + ey) / 2 + rnd.uniform(-2, 2)
        L.polyline(a, [(top_x, top_y), (mx, my), (ex, ey)], K, 3)
        boughs.append((ex, ey))
    # leafy masses
    for ex, ey in boughs:
        rx, ry = rnd.uniform(9, 12), rnd.uniform(6, 8)
        L.ellipse(a, ex, ey, rx, ry, K)
        # leafy edge: lanceolate leaves sticking out of the mass
        for k in range(14):
            t = rnd.uniform(0, 2 * math.pi)
            px, py = ex + math.cos(t) * rx, ey + math.sin(t) * ry
            if py > ey + ry * 0.6:
                continue
            L.line(a, px, py, px + math.cos(t) * 3, py + math.sin(t) * 2.2 - 0.6, K, 1)
    # incised leaves inside the masses
    for ex, ey in boughs:
        for k in range(10):
            px = ex + rnd.uniform(-8, 7)
            py = ey + rnd.uniform(-5, 4)
            if 0 < px < w - 3 and 0 < py < h - 3 and a[int(py), int(px)] == K:
                d = rnd.choice((1, -1))
                if all(a[int(py) + j, int(px) + k2] == K for j in (-1, 0, 1) for k2 in (-1, 0, 1, 2)):
                    a[int(py), int(px)] = -1
                    a[int(py) - d * 0 + 1, int(px) + 1] = -1
    # olives
    for ex, ey in boughs:
        for k in range(3):
            px = int(ex + rnd.uniform(-7, 7))
            py = int(ey + rnd.uniform(-3, 5))
            if 1 <= px < w - 1 and 1 <= py < h - 1 and a[py, px] == K:
                a[py, px] = Wt
    return (a, boughs) if with_boughs else a


NOCTOWL = [
    "#...........#",
    ".#.........#.",
    ".##.......##.",
    "..#########..",
    ".###########.",
    "##www###www##",
    "#ww#w###w#ww#",
    "##www#i#www##",
    ".#####i#####.",
    "..#########..",
    ".##i#i#i#i##.",
    ".#i#i#i#i#i#.",
    ".##i#i#i#i##.",
    ".###########.",
    "..#########..",
    "...#######...",
    "....#...#....",
    "...##...##...",
]

MAREEP = [  # grazing, head down to the left; the fleece is added white
    "..........................",
    ".......ww.wwww.www........",
    ".....wwwwwwwwwwwwwwww.....",
    "....wwwwwwwwwwwwwwwwww....",
    "..#wwwwwwwwwwwwwwwwwwww..#",
    ".#.wwwwwwwwwwwwwwwwwwww.#.",
    "#.##wwwwwwwwwwwwwwwwwww#..",
    "#####wwwwwwwwwwwwwwwww.#..",
    "######wwwwwwwwwwwwwwww.ww.",
    "#i####.##..##..##..##wwww.",
    "######.##..##..##..##wwww.",
    ".####..##..##..##..##..ww.",
    "..##...##..##..##..##.....",
    ".......#...#...#...#......",
]


def mareep():
    return rim(pad(grid_arr(MAREEP), 1, 1, 1, 0))


# ==========================================================================
# The sea: waves, the trireme, the ketos (Gyarados) and dolphins (Finizen)
# ==========================================================================
# A running-wave (Vitruvian scroll) crest, period 16, sitting on solid ink.
WAVE = [
    "........###.....",
    "......##...#....",
    ".....#..##..#...",
    "....#..#..#.#...",
    "...#...#.##.#...",
    "..#.....#..#....",
    ".#.......##.....",
    "################",
]


def sea_band(w, depth=12, seed=7):
    """The sea: the running-wave crest over ink water with incised swell
    lines and a few added-white flecks of foam."""
    rnd = random.Random(seed)
    crest = grid_arr(WAVE)
    h = len(WAVE) + depth
    a = np.zeros((h, w), int)
    for x in range(w):
        for y in range(len(WAVE)):
            v = crest[y, x % 16]
            if v:
                a[y, x] = v
        for y in range(len(WAVE), h):
            a[y, x] = K
    for y in range(len(WAVE) + 2, h - 1, 3):
        ph = rnd.uniform(0, 10)
        for x in range(w):
            if math.sin(x / 5.0 + ph + y) > 0.55:
                a[y, x] = T
    for k in range(w // 24):
        x = rnd.randrange(2, w - 2)
        a[len(WAVE) + 1, x] = Wt
    return a


def trireme():
    """A war galley, black-figure: low hull with a bronze ram, the painted eye
    on the prow, a curling stern, a row of oars and a white square sail."""
    w, h = 132, 70
    a = np.zeros((h, w), int)
    wl = 60                       # waterline row
    # hull: from the ram (left, at the waterline) to the stern (right)
    hull = [(4, wl), (14, wl - 3), (20, wl - 9), (110, wl - 9), (118, wl - 7),
            (122, wl - 3), (112, wl + 1), (24, wl + 1), (12, wl + 2)]
    L.polygon(a, hull, K)
    # the ram's beak and the prow post curling up
    L.polygon(a, [(0, wl + 1), (6, wl - 2), (14, wl - 1), (12, wl + 2)], K)
    L.polyline(a, [(20, wl - 9), (18, wl - 15), (20, wl - 20), (24, wl - 21)], K, 2)
    # the stern ornament (aphlaston) curving forward over the deck
    L.polyline(a, [(118, wl - 7), (124, wl - 14), (126, wl - 22), (122, wl - 28), (117, wl - 28),
                   (115, wl - 25)], K, 3)
    # deck rail and incised wales
    L.line(a, 20, wl - 12, 110, wl - 12, K, 1)
    for x in range(24, 108, 7):
        L.line(a, x, wl - 12, x, wl - 9, K, 1)
    L.line(a, 16, wl - 4, 116, wl - 4, T, 1)
    L.line(a, 22, wl - 7, 112, wl - 7, T, 1)
    # oar ports (white dots) and oars raking down into the sea
    for i, x in enumerate(range(30, 106, 7)):
        a[wl - 6, x] = Wt
        L.line(a, x, wl - 5, x - 9, wl + 8, K, 1)
    # the eye on the prow
    L.disc(a, 17.5, wl - 5.5, 2.2, Wt)
    a[wl - 6, 17] = K
    a[wl - 5, 17] = K
    # red band along the hull
    for x in range(26, 108):
        if a[wl - 2, x] == K:
            a[wl - 2, x] = R
    # mast, yard and sail
    mx = 66
    L.line(a, mx, wl - 12, mx, 6, K, 2)
    L.line(a, mx - 30, 9, mx + 30, 9, K, 2)
    sail = [(mx - 28, 10), (mx + 28, 10), (mx + 26, wl - 22), (mx - 26, wl - 22)]
    L.polygon(a, sail, Wt)
    # sail seams and brails as ink lines, the black rim of added white
    for k in range(1, 6):
        x = mx - 28 + k * 56 // 6
        L.line(a, x, 11, x - 1, wl - 23, K, 1)
    L.line(a, mx - 27, 22, mx + 27, 22, K, 1)
    a = rim(a)
    # forestay and backstay
    L.line(a, mx, 7, 22, wl - 20, K, 1)
    L.line(a, mx, 7, 118, wl - 27, K, 1)
    # masthead
    L.disc(a, mx, 5, 2, K)
    return a


def ketos():
    """Gyarados as the ketos, the sea serpent of Greek vases: two coils
    arching out of the waves, the neck rearing up to a great head with the
    three-pointed crest, jaws open on added-white teeth, a trailing whisker,
    a finned back and incised scales. The sea is painted over its foot."""
    w, h = 100, 66
    a = np.zeros((h, w), int)
    water = h - 8

    def arch(x0, x1, top, wid):
        pts = []
        for i in range(41):
            t = i / 40
            x = x0 + (x1 - x0) * t
            y = water + 6 - (water + 6 - top) * math.sin(t * math.pi)
            pts.append((x, y))
        for (x, y) in pts:
            L.disc(a, x, y, wid / 2, K)
        return pts

    tail = arch(2, 30, water - 18, 7)
    coil = arch(36, 72, water - 32, 11)
    # tail fin
    L.polygon(a, [(4, water - 2), (0, water - 12), (6, water - 6), (12, water - 13), (9, water - 1)], K)
    # neck: rising out of the water to the head
    neck = [(78, water + 4), (80, water - 14), (82, water - 30), (80, water - 42)]
    for i in range(len(neck) - 1):
        (x0, y0), (x1, y1) = neck[i], neck[i + 1]
        L.line(a, x0, y0, x1, y1, K, 12 - i)
    # head: long upper jaw and snout to the right, lower jaw dropped open
    hy = water - 46
    L.polygon(a, [(72, hy + 2), (80, hy - 5), (92, hy - 3), (99, hy + 2), (98, hy + 5), (86, hy + 6),
                  (80, hy + 9), (74, hy + 8)], K)
    L.polygon(a, [(78, hy + 11), (88, hy + 10), (97, hy + 15), (96, hy + 17), (84, hy + 17), (79, hy + 15)], K)
    for x in range(86, 98, 2):        # teeth
        a[hy + 6, x] = Wt
        a[hy + 11, x - 1] = Wt
    L.disc(a, 85, hy, 1.5, Wt)        # eye
    a[hy, 86] = K
    # the crest: three points swept back
    for b0, b1, tip in (((78, hy - 4), (83, hy - 5), (78, hy - 15)),
                        ((75, hy - 2), (80, hy - 4), (70, hy - 11)),
                        ((73, hy + 1), (77, hy - 1), (65, hy - 4))):
        spike(a, b0, b1, tip)
    # whisker trailing back from the jaw
    L.polyline(a, [(80, hy + 10), (74, hy + 14), (70, hy + 13), (66, hy + 17), (62, hy + 16)], K, 1)
    # fins along the backs of the coils
    for pts, step, wid in ((tail, 8, 7), (coil, 6, 11)):
        for i in range(6, 36, step):
            x, y = pts[i]
            spike(a, (x - 3, y - wid / 2 + 1), (x + 2, y - wid / 2 + 1), (x - 3, y - wid / 2 - 5))
    # incised scales: small arcs in rows along the big coil and the neck
    for pts, wid in ((coil, 11), (tail, 7)):
        for i in range(4, 38, 3):
            x, y = pts[i]
            for dy in ((-1, 2) if wid > 8 else (0,)):
                for dx in (-1, 0, 1):
                    xx, yy = int(round(x + dx)), int(round(y + dy + abs(dx)))
                    if 0 <= yy < h and a[yy, xx] == K:
                        a[yy, xx] = -1
    for y in range(water - 36, water - 2, 4):
        for dx in (-1, 0, 1):
            xx = int(round(80 + (water - y) * 0.03)) + dx
            if a[y + abs(dx), xx] == K:
                a[y + abs(dx), xx] = -1
    # red belly line up the front of the neck
    for y in range(water - 40, water):
        x = int(round(83.5 - (y - (water - 40)) * 0.05))
        if a[y, x] == K and a[y, x + 1] == 0:
            a[y, x] = R
    return a


def finizen_frames():
    """32x16 frames of a leaping dolphin (Finizen), nose to the right:
    rising, level, diving. Ink body, white belly stripe and eye."""
    frames = []
    for ang in (-0.5, 0.0, 0.55):
        def draw(c, s, ang=ang):
            ca, sa = math.cos(ang), math.sin(ang)

            def P(x, y):  # dolphin space (center 0,0) -> frame pixels
                return (16 + (x * ca - y * sa)) * s, (8 + (x * sa + y * ca)) * s

            def poly(pts, v):
                L.polygon(c, [P(x, y) for x, y in pts], v)

            body = [(-11, 0), (-7, -2.6), (-1, -3.6), (5, -3.4), (9, -2.2), (11.5, -0.6), (13.5, 0),
                    (11.5, 1), (8, 2.4), (2, 3.2), (-5, 2.6), (-9, 1.2)]
            poly(body, K)
            poly([(-2, -3.2), (1, -7.2), (3, -3.2)], K)              # dorsal fin
            poly([(-10, 0), (-15, -4.5), (-13, 0), (-15, 4.5)], K)   # flukes
            poly([(1, 2.4), (-2, 6), (4, 2.6)], K)                   # flipper
            poly([(-6, 1.6), (2, 2.2), (9, 1.2), (2, 1.0)], Wt)      # belly stripe
            poly([(7.6, -1.6), (8.8, -1.6), (8.8, -0.6), (7.6, -0.6)], Wt)  # eye
        frames.append(raster(draw, 32, 16))
    return frames


# ==========================================================================
# The temple of the Twelve
# ==========================================================================
def temple():
    """A Doric temple in side view with twelve columns, on three steps,
    under a triglyph frieze and a tiled roof with palmette acroteria."""
    ncol, step = 12, 15
    w = 18 + ncol * step
    h = 76
    a = np.zeros((h, w), int)
    g = h - 1
    # three steps
    for k in range(3):
        y0 = g - 2 * k - 1
        L.polygon(a, [(k * 3, y0 - 1), (w - k * 3, y0 - 1), (w - k * 3, y0 + 1), (k * 3, y0 + 1)], K)
        L.line(a, k * 3 + 1, y0 + 1, w - k * 3 - 2, y0 + 1, T, 1)
    top_step = g - 6
    col_top = top_step - 44
    for c in range(ncol):
        x = 11 + c * step
        # shaft with entasis, incised flutes
        for y in range(col_top + 3, top_step + 1):
            t = (y - col_top) / 44
            half = 2.6 + 0.4 * math.sin(t * math.pi) - 0.3 * (1 - t)
            for xx in range(int(round(x - half)), int(round(x + half)) + 1):
                a[y, xx] = K
        for y in range(col_top + 5, top_step - 1, 1):
            a[y, x] = T
        # capital: echinus and abacus
        L.line(a, x - 4, col_top + 2, x + 4, col_top + 2, K, 1)
        L.line(a, x - 5, col_top + 1, x + 5, col_top + 1, K, 1)
        L.line(a, x - 5, col_top, x + 5, col_top, K, 1)
    # architrave
    arch_y = col_top - 6
    for y in range(arch_y, col_top):
        L.line(a, 3, y, w - 4, y, K, 1)
    L.line(a, 4, arch_y + 3, w - 5, arch_y + 3, R, 1)
    # frieze of triglyphs (ink, incised) and metopes (clay with a white disc)
    fr_y = arch_y - 8
    L.line(a, 3, fr_y, w - 4, fr_y, K, 1)
    for x in range(3, w - 4):
        k = (x - 3) % (step // 2 + 1 if False else 8)
        for y in range(fr_y, arch_y):
            if k < 4:
                a[y, x] = K
        if k in (1, 2) and fr_y + 1 < arch_y - 1:
            for y in range(fr_y + 2, arch_y - 1):
                if k == 1:
                    a[y, x] = T
    for x in range(9, w - 6, 8):
        a[fr_y + 4, x] = Wt
    # cornice and roof with antefixes
    cor_y = fr_y - 3
    for y in range(cor_y, fr_y):
        L.line(a, 1, y, w - 2, y, K, 1)
    L.line(a, 2, cor_y + 1, w - 3, cor_y + 1, T, 1)
    roof_y = cor_y - 6
    L.polygon(a, [(4, cor_y), (w - 5, cor_y), (w - 9, roof_y), (8, roof_y)], K)
    for x in range(10, w - 10, 4):
        a[roof_y + 2, x] = -1
        a[roof_y + 3, x + 1] = -1
    for x in range(6, w - 5, 10):
        L.polygon(a, [(x, cor_y), (x + 2, cor_y - 4), (x + 4, cor_y)], K)
    # palmette acroteria at the corners
    for x in (8, w - 9):
        L.polygon(a, [(x - 3, roof_y), (x, roof_y - 7), (x + 3, roof_y)], K)
        a[roof_y - 3, x] = R
    return a


XATU = [  # standing like a totem, wings wrapped as a cloak, facing left
    ".....##......",
    "....####.....",
    "...######....",
    "..##w#####...",
    "####.#####...",
    "...#######...",
    "....#####....",
    "..#########..",
    ".##wwwwwww##.",
    ".#wwwwwwwww#.",
    ".#w#ww#ww#w#.",
    ".##rrrrrrr##.",
    ".###########.",
    ".##i##i##i##.",
    ".#i##i##i##i#",
    ".##i##i##i##.",
    ".#i##i##i##i#",
    ".###########.",
    ".#rrrrrrrrr#.",
    ".###########.",
    "..#########..",
    "..####.####..",
    "...##...##...",
    "..###...###..",
]

TRIPOD_FIRE = [  # the altar under the flame sprite
    "...wwwwwww...",
    ".###########.",
    "..#i#####i#..",
    "..#########..",
    "..#rrrrrrr#..",
    "..#########..",
    "..##i###i##..",
    "..#########..",
    ".###########.",
    "#############",
]


def flame_frames():
    """16x16 fire on the altar, 3 frames: added red and white tongues."""
    shapes = [
        ["......r.........", ".....rr..r......", "....rwr.rr......", "...rrwrrwr......",
         "...rwwwrwrr.....", "..rrwwwwwrr.....", "..rwwwwwwwr.....", "...rrwwwwr......"],
        [".........r......", "....r...rr......", "....rr.rwr......", "...rwrrrwrr.....",
         "...rwwrwwwr.....", "..rrwwwwwwrr....", "..rwwwwwwwr.....", "...rrwwwwr......"],
        ["......r.........", "......rr..r.....", "...r.rwr.rr.....", "...rrrwrrwr.....",
         "..rrwwwwwwr.....", "..rwwwwwwwrr....", "..rwwwwwwwr.....", "...rrwwwwr......"],
    ]
    frames = []
    for s in shapes:
        f = np.zeros((16, 16), int)
        g = grid_arr(s)
        f[8:16, :] = g
        frames.append(f)
    return frames


# ==========================================================================
# Olympus: peaks in the clouds, and Zapdos, Zeus's thunder-eagle
# ==========================================================================
def cypress(h=54, seed=3):
    """A cypress spire: a tall flame of ink with incised chevrons."""
    rnd = random.Random(seed)
    w = 13
    a = np.zeros((h, w), int)
    for y in range(h - 4):
        t = y / (h - 4)
        half = 5.6 * math.sin(min(1.0, t * 1.15) * math.pi * 0.5) ** 0.8 * (1 - 0.25 * t)
        if y < 3:
            half = 0.5
        for x in range(w):
            if abs(x - w // 2) <= half + rnd.uniform(-0.4, 0.4):
                a[y, x] = K
    L.line(a, w // 2, h - 5, w // 2, h - 1, K, 2)
    for y in range(8, h - 8, 5):
        for d in range(1, 4):
            for sx in (-1, 1):
                x, yy = w // 2 + sx * d, y - d
                if a[yy, x] == K and a[yy, x + sx] == K:
                    a[yy, x] = -1
    return a


def olympus(seed=12, h=78):
    """Mount Olympus: three peaks with added-white snow and incised ridges,
    a white cloud bank around its waist, and the Twelve's seat at the top."""
    rnd = random.Random(seed)
    w = 220
    a = np.zeros((h, w), int)
    g = h - 1
    k = (h - 8) / 84
    peaks = [(0, g), (28, g - 30 * k), (44, g - 26 * k), (70, g - 62 * k), (84, g - 58 * k),
             (104, g - 84 * k), (122, g - 66 * k), (140, g - 70 * k), (166, g - 40 * k), (188, g - 46 * k),
             (219, g)]
    peaks = [(x, int(round(y))) for x, y in peaks]
    L.polygon(a, peaks + [(219, g), (0, g)], K)
    tops = [peaks[5], peaks[3], peaks[7]]
    # snow on the three high peaks
    for (px, py) in tops:
        snow = [(px, py), (px + 9, py + 9), (px + 5, py + 7), (px + 2, py + 11), (px - 3, py + 8),
                (px - 7, py + 10), (px - 9, py + 8)]
        L.polygon(a, snow, Wt)
    # incised ridges running down from the peaks
    for (px, py), dx in ((tops[0], -1), (tops[0], 1), (tops[2], -1), (tops[1], 1)):
        x, y = px + dx * 2, py + 12
        for _ in range(22):
            y += 1
            x += dx * rnd.choice((0, 1, 1))
            if 0 <= x < w and 0 <= y < h and a[y, x] == K:
                a[y, x] = -1
    # the seat of the Twelve: a tiny temple on the summit
    sx, sy = tops[0][0], tops[0][1] - 1
    L.line(a, sx - 7, sy - 1, sx + 7, sy - 1, K, 1)
    for x in range(sx - 6, sx + 7, 3):
        L.line(a, x, sy - 6, x, sy - 2, K, 1)
    L.polygon(a, [(sx - 8, sy - 6), (sx, sy - 10), (sx + 8, sy - 6)], K)
    # the cloud bank: white puffs with ink rims and incised curls
    clouds = np.zeros((h, w), int)
    cloud_y = g - int(30 * k + 4)
    for n in range(16):
        cx = 10 + n * 13 + rnd.uniform(-3, 3)
        cy = cloud_y + 5 * math.sin(n * 1.3) + rnd.uniform(-2, 2)
        r = rnd.uniform(6, 9)
        L.ellipse(clouds, cx, cy, r * 1.25, r * 0.8, Wt)
    clouds = rim(clouds)
    # curls on the clouds' lower edges
    for n in range(16):
        cx = int(14 + n * 13)
        cy = int(cloud_y + 4 + 5 * math.sin(n * 1.3))
        if 0 <= cx < w - 3 and 0 <= cy < h:
            for dx, dy in ((0, 0), (1, -1), (2, -1), (3, 0)):
                if clouds[cy + dy, cx + dx] == Wt:
                    clouds[cy + dy, cx + dx] = K
    for y in range(h):
        for x in range(w):
            if clouds[y, x]:
                a[y, x] = clouds[y, x]
    return a


def spike(a, base0, base1, tip, v=K):
    L.polygon(a, [base0, tip, base1], v)


def zapdos():
    """Zapdos in flight, facing right, wings raised like a heraldic eagle:
    five jagged feathers on the near wing, two of the far wing showing past
    it, the spiked crest, the long beak, a spiked tail and chest. Ink with
    incised feather shafts, a white eye and a red wing-bar."""
    w, h = 60, 40
    a = np.zeros((h, w), int)
    # far wing, behind: its two outer feathers show past the near wing
    L.polygon(a, [(37, 20), (46, 4), (44, 12), (52, 9), (42, 22)], K)
    # near wing: one broad shape with a jagged, lightning-cut edge
    wing = [(39, 22), (37, 11), (41, 1), (34, 6), (31, 0), (27, 7), (21, 3), (21, 11), (12, 9), (18, 16),
            (9, 18), (19, 21), (22, 25)]
    L.polygon(a, wing, K)
    feathers = [((32, 20), (40, 3)), ((29, 20), (31, 2)), ((26, 21), (22, 5)), ((24, 22), (14, 10)),
                ((23, 23), (11, 17))]
    # body and chest
    L.ellipse(a, 30, 25.5, 11, 5, K)
    for x in (25, 30, 35):
        spike(a, (x - 2, 29), (x + 2, 29), (x - 1, 34))
    # tail: three spikes
    for tip in ((5, 20), (3, 25), (7, 30)):
        spike(a, (21, 22), (21, 28), tip)
    # neck, head, crest and beak
    L.polygon(a, [(37, 22), (42, 17), (47, 15), (48, 21), (41, 27)], K)
    L.ellipse(a, 46.5, 17.5, 4, 3.5, K)
    for b0, b1, tip in (((43, 15), (46, 14), (41, 6)), ((41, 17), (44, 15), (35, 11)),
                        ((45, 14), (48, 14), (48, 7))):
        spike(a, b0, b1, tip)
    L.polygon(a, [(49, 15), (59, 18), (49, 20)], K)
    L.line(a, 50, 18, 57, 18, -1, 1)
    a[16, 47] = Wt
    a[16, 48] = Wt
    a[17, 47] = Wt
    # legs and talons
    L.line(a, 27, 30, 26, 37, K, 2)
    L.line(a, 33, 30, 34, 37, K, 2)
    for x in (26, 34):
        L.line(a, x - 2, 38, x + 2, 38, K, 1)
    # incised feather lines: from the wing's root toward each point
    for (bx, by), (tx, ty) in feathers:
        L.line(a, bx, by - 2, bx + (tx - bx) * 0.62, by - 2 + (ty - by + 2) * 0.62, -1, 1)
    # the red bar where the wing meets the body, and a line under the wing
    for x in range(24, 39):
        if a[21, x] == K:
            a[21, x] = R
    L.line(a, 22, 24, 38, 23, -1, 1)
    return a


def bolt_frames():
    """16x32 lightning: two jagged bolts, white with a red core."""
    shapes = [
        ["...ww...", "..ww....", ".www....", "wwwwww..", "...ww...", "..ww....", ".wwwww..", "...www..",
         "...ww...", "..ww....", "..w.....", ".w......"],
        ["....ww..", "...ww...", "..www...", ".wwwwww.", "....ww..", "...ww...", "..wwwww.", "....ww..",
         "...ww...", "...w....", "..w.....", "..w....."],
    ]
    frames = []
    for s in shapes:
        f = np.zeros((32, 16), int)
        g = grid_arr(s)
        g2 = np.kron(g, np.ones((2, 2), int))[:, :16]
        f[4:4 + g2.shape[0], :g2.shape[1]] = g2
        # red core
        for y in range(32):
            xs = np.nonzero(f[y] == Wt)[0]
            if len(xs) >= 3:
                f[y, xs[len(xs) // 2]] = R
        frames.append(f)
    return frames


# ==========================================================================
# Painted name labels (title_lettering.GREEK, plus the letters we need)
# ==========================================================================
import title_lettering as LET

GREEK5 = dict(LET.GREEK)
GREEK5.update({
    "Υ": ["#.#", "#.#", ".#.", ".#.", ".#."],
    "Μ": ["#...#", "##.##", "#.#.#", "#...#", "#...#"],
    "Ν": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "Δ": ["..#..", ".#.#.", ".#.#.", "#...#", "#####"],
})


def label(text):
    rows = L.set_rows(GREEK5, text, 1, 5)
    return grid_arr(rows)


# ==========================================================================
# The loom: warp threads, loom weights, Lachesis's rod, Atropos's shears
# ==========================================================================
LOOM_WEIGHT = [
    "...#...",
    "..#w#..",
    "..###..",
    ".#####.",
    ".##i##.",
    "#######",
    "##i#i##",
    "#######",
    "#rrrrr#",
    "#######",
]

# Lachesis's measuring rod, held upright: black with added-white marks.
ROD = (["..#..", ".###.", ".#w#.", ".###.", ".###."] +
       [".###." if k % 4 else ".#w#." for k in range(40)] +
       [".###.", ".#w#.", ".###.", "..#.."])

SHEARS_CUT = (14, 16)   # in the 64x32 shears frame: where the blades close on a thread
SHEARS_WRIST = (50, 16)  # where the forearm sprites join


def shears_frames():
    """64x32 frames of Atropos's spring shears, blades to the left, gripped by
    her hand (added white) at the handles: open wide, half open, closed.
    The two halves pivot on the U-shaped spring bow at the right."""
    frames = []
    bow = (46.0, 16.0)
    for ang in (0.30, 0.15, 0.02):
        def draw(c, s, ang=ang):
            def P(x, y, sg):  # half-shears space (bow at 0, blade to -x) -> frame
                a = -sg * ang
                return ((bow[0] + x * math.cos(a) - y * math.sin(a)) * s,
                        (bow[1] + x * math.sin(a) + y * math.cos(a)) * s)

            for sg in (1, -1):        # upper half, then lower
                arm = [(1, -1.8 * sg), (-14, -2.8 * sg), (-14, 0.8 * sg), (1, 1.6 * sg)]
                L.polygon(c, [P(x, y, sg) for x, y in arm], K)
                blade = [(-13, -4.4 * sg), (-36, -1.6 * sg), (-44, 0.4 * sg), (-13, 1.2 * sg)]
                L.polygon(c, [P(x, y, sg) for x, y in blade], K)
            # the spring bow
            for t in np.linspace(-1.7, 1.7, 50):
                L.disc(c, (bow[0] + 2.0 + 4.2 * math.cos(t)) * s, (bow[1] + 4.6 * math.sin(t)) * s, 1.0 * s, K)
            # her fingers round the handles, the wrist toward the bow
            L.ellipse(c, 40 * s, 16 * s, 5.0 * s, 4.6 * s, Wt)
            L.polygon(c, [(40 * s, 12 * s), (51 * s, 13.5 * s), (51 * s, 18.5 * s), (40 * s, 20 * s)], Wt)
        f = raster(draw, 64, 32)
        f = rim(f)
        # the bevel along each blade's back: an incised line one pixel in
        for sg in (1, -1):
            a_ = -sg * ang
            for t in np.linspace(0, 1, 60):
                x, y = -15 + (-34 + 15) * t, (-2.6 + 1.8 * t) * sg
                px = bow[0] + x * math.cos(a_) - y * math.sin(a_)
                py = bow[1] + x * math.sin(a_) + y * math.cos(a_)
                xi, yi = int(px), int(py)
                if f[yi, xi] == K and f[yi - sg, xi] == K and f[yi + sg, xi] == K:
                    f[yi, xi] = 0
        # finger lines
        for x in (37, 40, 43):
            for y in range(13, 20):
                if f[y, x] == Wt and f[y - 1, x] == Wt and y % 2 == 1:
                    f[y, x] = K
        frames.append(f)
    return frames


def arm_frames():
    """64x32 frames (the piece in rows 8-23) of the forearm reaching in from the right: [0] the bare white
    wrist and forearm into a black sleeve with a red cuff, [1] more sleeve,
    with incised folds. Lachesis's arm is the same, flipped."""
    a = np.zeros((16, 64), int)
    cy = 8
    for x in range(64):
        if x < 18:
            half = 2.6 + x * 0.06
            for y in range(int(round(cy - half)), int(round(cy + half)) + 1):
                a[y, x] = Wt
        else:
            half = 4.5 + min(1.5, (x - 18) * 0.08)
            for y in range(int(round(cy - half)), int(round(cy + half)) + 1):
                a[y, x] = K
    a = rim(a)
    for y in range(16):
        for x in (18, 19):
            if a[y, x] == K:
                a[y, x] = R
    for x0 in range(26, 64, 7):
        L.line(a, x0, cy - 4, x0 + 4, cy + 4, -1, 1)
    b = np.zeros((16, 64), int)
    for x in range(64):
        for y in range(cy - 6, cy + 7):
            b[y, x] = K
    for x0 in range(2, 64, 7):
        L.line(b, x0, cy - 5, x0 + 4, cy + 5, -1, 1)
    # GBA sprites have no 64x16 shape: centre each piece in a 64x32 frame
    out = []
    for piece in (a, b):
        f = np.zeros((32, 64), int)
        f[8:24] = np.where(piece < 0, 0, piece)
        out.append(f)
    return out


def rod_hand():
    """16x16: Lachesis's fist round the rod (the rod passes behind at x 7-9)."""
    f = np.zeros((16, 16), int)
    L.ellipse(f, 6.0, 8.0, 4.6, 4.2, Wt)
    L.ellipse(f, 3.0, 8.5, 3.5, 3.0, Wt)
    f = rim(f)
    for y in (6, 8, 10):
        for x in (7, 8, 9):
            if f[y, x] == Wt:
                f[y, x] = K
    return f


def knot():
    """8x8: the red knot Lachesis ties where a thread will be cut."""
    f = np.zeros((8, 8), int)
    g = grid_arr(["..r..", ".rrr.", ".rwr.", "..r.."])
    f[2:6, 1:6] = g
    return f
