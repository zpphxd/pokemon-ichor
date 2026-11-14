"""Shared pieces for Ichor's boot sequence art (intro_*.py).

Palettes, pixel helpers, two small pixel fonts, the V-cut shader for gilded
letters, and tile/tilemap writers. The palettes are the title screen's
(tools/ichor/art/title_screen.py), so the intro and the amphora read as one pot.
Every value is a multiple of 8 so it maps exactly to BGR555.
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]

# --------------------------------------------------------------------------
# Colors (title_screen.py PAINT / GOLD / THREAD)
# --------------------------------------------------------------------------
INK = (32, 24, 24)
SHEEN = (56, 48, 48)
CLAY_DEEP = (120, 48, 24)
CLAY_SHADE = (152, 64, 32)
CLAY = (184, 88, 48)
CLAY_LIGHT = (208, 112, 64)
CLAY_HI = (224, 136, 88)
WHITE = (232, 216, 176)        # added white
RED = (128, 40, 40)            # added red
GOLD_DEEP = (120, 72, 16)
GOLD_SHADOW = (168, 112, 32)
GOLD_MID = (200, 144, 40)
GOLD_LIT = (240, 192, 64)
GOLD_GLINT = (248, 232, 152)
THREAD_UNDER = (136, 80, 16)
THREAD_BODY = (232, 176, 48)
THREAD_BRIGHT = (248, 216, 104)
BLACK = (0, 0, 0)

CLAY_RAMP = [CLAY_DEEP, CLAY_SHADE, CLAY, CLAY_LIGHT, CLAY_HI]

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


def pad16(colors):
    colors = list(colors)
    assert len(colors) <= 16, len(colors)
    return colors + [BLACK] * (16 - len(colors))


# --------------------------------------------------------------------------
# Grids: lists of equal-length strings, one char per pixel
# --------------------------------------------------------------------------
def check(grid, name="grid"):
    widths = {len(r) for r in grid}
    assert len(widths) == 1, f"ragged {name}: {sorted(widths)}"
    return grid


def grid_size(grid):
    return len(grid[0]), len(grid)


def flip_grid(grid):
    return [r[::-1] for r in grid]


def paste(img, grid, x0, y0, key, skip=".", name="grid"):
    """Write grid chars through key (char -> index) into img at (x0, y0).
    Chars in skip are left alone; unknown chars raise."""
    check(grid, name)
    h, w = img.shape
    for dy, row in enumerate(grid):
        y = y0 + dy
        if not 0 <= y < h:
            continue
        for dx, ch in enumerate(row):
            x = x0 + dx
            if ch in skip or not 0 <= x < w:
                continue
            img[y, x] = key[ch]


def mask_to_grid(mask, on="#", off="."):
    return ["".join(on if v else off for v in row) for row in mask]


# --------------------------------------------------------------------------
# Drawing primitives on index arrays
# --------------------------------------------------------------------------
def disc(img, cx, cy, r, v):
    h, w = img.shape
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if 0 <= x < w and 0 <= y < h and (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                img[y, x] = v


def ellipse(img, cx, cy, rx, ry, v):
    h, w = img.shape
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if 0 <= x < w and 0 <= y < h and ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                img[y, x] = v


def line(img, x0, y0, x1, y1, v, width=1):
    """A line of the given width (round brush)."""
    n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
    for i in range(n + 1):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        if width <= 1:
            xi, yi = int(round(x)), int(round(y))
            if 0 <= yi < img.shape[0] and 0 <= xi < img.shape[1]:
                img[yi, xi] = v
        else:
            disc(img, x, y, width / 2 - 0.01, v)


def polyline(img, pts, v, width=1):
    for a, b in zip(pts, pts[1:]):
        line(img, a[0], a[1], b[0], b[1], v, width)


def polygon(img, pts, v):
    """Fill a polygon (even-odd, pixel centers)."""
    h, w = img.shape
    ys = [p[1] for p in pts]
    for y in range(max(0, int(min(ys))), min(h, int(max(ys)) + 1)):
        yc = y + 0.5
        xs = []
        for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]):
            if (ya <= yc < yb) or (yb <= yc < ya):
                xs.append(xa + (yc - ya) * (xb - xa) / (yb - ya))
        xs.sort()
        for xa, xb in zip(xs[::2], xs[1::2]):
            for x in range(max(0, int(math.ceil(xa - 0.5))), min(w, int(math.floor(xb - 0.5)) + 1)):
                img[y, x] = v


# --------------------------------------------------------------------------
# V-cut shading for gilded letters (as on the title's ICHOR)
# --------------------------------------------------------------------------
def vcut(mask):
    """Shade a letter mask as a V-groove lit from the top left: the groove's
    left/top wall is in shadow, its right/bottom wall catches the light.
    Returns rows of d (deep edge), s (shadow), m (turn), l (lit), g (glint)."""
    h, w = len(mask), len(mask[0])
    on = lambda x, y: 0 <= x < w and 0 <= y < h and mask[y][x] in "#X"

    def run(x, y, dx, dy):
        n = 0
        while on(x + dx * (n + 1), y + dy * (n + 1)):
            n += 1
        return n

    out = []
    for y in range(h):
        row = ""
        for x in range(w):
            if not on(x, y):
                row += "."
                continue
            # distance to the shadow side (left/up) and the lit side (right/down)
            a = min(run(x, y, -1, 0), run(x, y, 0, -1), run(x, y, -1, -1))
            b = min(run(x, y, 1, 0), run(x, y, 0, 1), run(x, y, 1, 1))
            if a == 0 and b == 0:
                row += "m"
            elif a < b:
                row += "d" if a == 0 else "s"
            elif b == 0:
                row += "g"
            elif a == b:
                row += "m"
            else:
                row += "l"
        out.append(row)
    return out


# --------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------
# A plain 7 px proportional capital font with 1 px strokes, for the legal
# lines. Two rows above the cap height hold accents (glyphs are 9 rows).
_F7 = {
    "A": [".##.", "#..#", "#..#", "####", "#..#", "#..#", "#..#"],
    "B": ["###.", "#..#", "#..#", "###.", "#..#", "#..#", "###."],
    "C": [".##.", "#..#", "#...", "#...", "#...", "#..#", ".##."],
    "D": ["###.", "#..#", "#..#", "#..#", "#..#", "#..#", "###."],
    "E": ["####", "#...", "#...", "###.", "#...", "#...", "####"],
    "F": ["####", "#...", "#...", "###.", "#...", "#...", "#..."],
    "G": [".##.", "#..#", "#...", "#.##", "#..#", "#..#", ".###"],
    "H": ["#..#", "#..#", "#..#", "####", "#..#", "#..#", "#..#"],
    "I": ["###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"],
    "K": ["#..#", "#..#", "#.#.", "##..", "#.#.", "#..#", "#..#"],
    "L": ["#...", "#...", "#...", "#...", "#...", "#...", "####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#..#", "##.#", "##.#", "#.##", "#.##", "#..#", "#..#"],
    "O": [".##.", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."],
    "P": ["###.", "#..#", "#..#", "###.", "#...", "#...", "#..."],
    "R": ["###.", "#..#", "#..#", "###.", "#.#.", "#..#", "#..#"],
    "S": [".###", "#...", "#...", ".##.", "...#", "...#", "###."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#..#", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."],
    "V": ["#...#", "#...#", "#...#", "#...#", ".#.#.", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "0": [".##.", "#..#", "#.##", "#..#", "##.#", "#..#", ".##."],
    "1": [".#.", "##.", ".#.", ".#.", ".#.", ".#.", "###"],
    "2": [".##.", "#..#", "...#", "..#.", ".#..", "#...", "####"],
    "6": [".##.", "#...", "#...", "###.", "#..#", "#..#", ".##."],
    "©": ["..###..", ".#...#.", "#..##.#", "#.#...#", "#..##.#", ".#...#.", "..###.."],
    "/": ["...#", "...#", "..#.", "..#.", ".#..", ".#..", "#..."],
    "·": [".", ".", ".", "#", ".", ".", "."],
    ",": ["..", "..", "..", "..", "..", ".#", "#."],
    ".": [".", ".", ".", ".", ".", ".", "#"],
    "-": ["...", "...", "...", "###", "...", "...", "..."],
    " ": ["..", "..", "..", "..", "..", "..", ".."],
}
ACUTE7 = ["..#.", ".#.."]  # sits on the two accent rows, over E


def font7(ch):
    if ch == "É":
        g = _F7["E"]
        return [a.ljust(len(g[0]), ".") for a in ACUTE7] + g
    g = _F7[ch]
    return ["." * len(g[0])] * 2 + g


def set_text7(text, gap=1):
    """Rows (9 high: 2 accent rows + 7 cap rows) of '#'/'.' for text."""
    rows = [""] * 9
    for i, ch in enumerate(text):
        g = font7(ch)
        check(g, ch)
        for y in range(9):
            rows[y] += g[y] + ("." * gap if i < len(text) - 1 else "")
    return rows


# A display font: 9 px capitals with 2 px stems, matching the title's POKEMON
# banner (title_lettering.POKEMON). V-cut with shade2.
F9 = {
    "P": ["######.", "##..###", "##...##", "##..###", "######.", "##.....", "##.....", "##.....", "##....."],
    "R": ["######.", "##..###", "##...##", "##..###", "######.", "##.###.", "##..###", "##...##", "##...##"],
    "E": ["######", "##....", "##....", "##....", "#####.", "##....", "##....", "##....", "######"],
    "T": ["########", "...##...", "...##...", "...##...", "...##...", "...##...", "...##...", "...##...", "...##..."],
    "H": ["##....##", "##....##", "##....##", "##....##", "########", "##....##", "##....##", "##....##", "##....##"],
    "×": ["......", "......", "##..##", ".####.", "..##..", ".####.", "##..##", "......", "......"],
    " ": ["...", "...", "...", "...", "...", "...", "...", "...", "..."],
}


def set_rows(glyphs, text, gap, h):
    rows = [""] * h
    for i, ch in enumerate(text):
        g = glyphs[ch]
        check(g, ch)
        for y in range(h):
            rows[y] += g[y] + ("." * gap if i < len(text) - 1 else "")
    return rows


def shade2(mask_rows):
    """The title's shade_thin: left/top pixels of a stroke in shadow, the rest lit."""
    h, w = len(mask_rows), len(mask_rows[0])
    on = lambda x, y: 0 <= x < w and 0 <= y < h and mask_rows[y][x] == "#"
    out = []
    for y in range(h):
        row = ""
        for x in range(w):
            if not on(x, y):
                row += "."
            elif not on(x - 1, y) or not on(x, y - 1):
                row += "s"
            else:
                row += "l"
        out.append(row)
    return out


# --------------------------------------------------------------------------
# Tiles and files
# --------------------------------------------------------------------------
class TileSet:
    """Deduplicated 4bpp tiles (8x8 index arrays), flips allowed."""

    def __init__(self, first=None, allow_flip=True):
        self.tiles, self.index = [], {}
        self.allow_flip = allow_flip
        if first is not None:
            self.add(first)

    def add(self, t):
        key = t.tobytes()
        if key in self.index:
            return self.index[key]
        if self.allow_flip:
            for flip, ft in ((1, t[:, ::-1]), (2, t[::-1, :]), (3, t[::-1, ::-1])):
                k = ft.tobytes()
                if k in self.index:
                    return self.index[k][0], flip
        self.index[key] = (len(self.tiles), 0)
        self.tiles.append(t.copy())
        return self.index[key]

    def __len__(self):
        return len(self.tiles)


def tilemap(img, ts, pal_row, base=0):
    """Map an image (h, w multiples of 8) onto TileSet ts. Returns u16 (rows, cols)."""
    h, w = img.shape
    assert h % 8 == 0 and w % 8 == 0, img.shape
    out = np.zeros((h // 8, w // 8), np.uint16)
    for ty in range(h // 8):
        for tx in range(w // 8):
            n, flip = ts.add(img[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8])
            out[ty, tx] = (n + base) | ((flip & 1) << 10) | ((flip >> 1) << 11) | (pal_row << 12)
    return out


def map_to_screen(m, cols=32, rows=32, fill=0):
    """Place a (r, c) map at the top left of a cols x rows screen map."""
    out = np.full((rows, cols), fill, np.uint16)
    out[:m.shape[0], :m.shape[1]] = m[:rows, :cols]
    return out


def save_indexed(arr, palette, path):
    """An indexed PNG whose palette has exactly len(palette) entries, so the
    build's .gbapal from it is that many colors."""
    im = Image.fromarray(np.asarray(arr, np.uint8), "P")
    flat = []
    for c in palette:
        flat.extend(c)
    im.putpalette(flat)
    im.save(path, optimize=False)


def save_tiles(tiles, palette, path, per_row=16):
    rows = max(1, (len(tiles) + per_row - 1) // per_row)
    sheet = np.zeros((rows * 8, per_row * 8), int)
    for i, t in enumerate(tiles):
        sheet[(i // per_row) * 8:(i // per_row) * 8 + 8, (i % per_row) * 8:(i % per_row) * 8 + 8] = t
    save_indexed(sheet, palette, path)


def write_jasc(path, colors):
    with open(path, "w", newline="\r\n") as f:
        f.write(f"JASC-PAL\n0100\n{len(colors)}\n")
        for c in colors:
            f.write("%d %d %d\n" % c)


def write_map(path, m):
    Path(path).write_bytes(np.asarray(m, "<u2").tobytes())


def sprite_sheet(frames, w, h):
    """Stack sprite frames (h x w index arrays) vertically: with the image w px
    wide, gbagfx's tile order is the OBJ 1D layout, frame after frame."""
    out = np.zeros((h * len(frames), w), int)
    for i, f in enumerate(frames):
        assert f.shape == (h, w), (f.shape, (h, w))
        out[i * h:(i + 1) * h] = f
    return out


# --------------------------------------------------------------------------
# Preview helpers
# --------------------------------------------------------------------------
def rgb(img, palette, transparent=None):
    """Index array -> RGB array. Index 0 maps to transparent (None) or color."""
    pal = np.array([palette[i] if i < len(palette) else BLACK for i in range(256)], np.uint8)
    return pal[np.asarray(img, int)]


def over(dst, img, palette, x0=0, y0=0):
    """Composite index img (0 = transparent) over RGB dst at (x0, y0)."""
    h, w = img.shape
    H, W = dst.shape[:2]
    for y in range(h):
        yy = y0 + y
        if not 0 <= yy < H:
            continue
        for x in range(w):
            xx = x0 + x
            v = img[y, x]
            if v and 0 <= xx < W:
                dst[yy, xx] = palette[v]
    return dst


def upscale(arr, k=3):
    return Image.fromarray(np.asarray(arr, np.uint8)).resize((arr.shape[1] * k, arr.shape[0] * k), Image.NEAREST)
