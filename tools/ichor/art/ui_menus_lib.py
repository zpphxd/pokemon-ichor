#!/usr/bin/env python3
"""Shared toolkit for Ichor's everyday menu screens (bag, party, summary, shop,
map popups). The screens are painted as whole indexed images, then cut into
GBA tiles and tilemaps here, so the art stays editable as pictures while the
output matches what the engine loads.

Conventions, matching tools/ichor/art/ui_frames.py:
  - colors are RGB triples that are multiples of 8 (exact in BGR555)
  - index 0 of every 16-color palette is transparent
  - light comes from the top left
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]

# --- Master palette (design/phase1/PLAN.md) --------------------------------
INK = (32, 24, 24)              # black-figure ink
INK_TEXT = (56, 40, 32)         # ink for printed text, as the dialogue box
CLAY_DARK = (120, 48, 24)       # terracotta, dark
CLAY = (184, 88, 48)            # terracotta
CLAY_LIGHT = (224, 136, 88)     # terracotta, light
CLAY_PALE = (240, 176, 128)     # terracotta slip, palest (highlight only)
PARCHMENT = (232, 216, 176)     # limestone light: text fields
PARCH_SHADE = (208, 184, 136)   # limestone mid: text shadow
PARCH_DARK = (176, 144, 96)     # limestone dark: panel shading
MARBLE_DARK = (168, 160, 152)
MARBLE = (216, 208, 192)
MARBLE_LIGHT = (248, 248, 240)
AEGEAN_DARK = (24, 56, 120)
AEGEAN = (48, 104, 176)
AEGEAN_LIGHT = (112, 168, 224)
AEGEAN_PALE = (176, 216, 240)
OLIVE_DARK = (56, 72, 32)
OLIVE = (96, 112, 48)
OLIVE_LIGHT = (144, 160, 72)
SILVER_LEAF = (168, 184, 136)
GOLD_DARK = (200, 144, 40)
GOLD = (240, 192, 64)
GOLD_PALE = (248, 224, 136)
BRONZE = (152, 96, 40)

# HP bar colors, the same meaning as the battle HP box: healthy, caution, danger.
HP_GREEN = (88, 208, 96)
HP_GREEN_DARK = (48, 152, 64)
HP_YELLOW = (248, 208, 56)
HP_YELLOW_DARK = (200, 144, 24)
HP_RED = (240, 88, 56)
HP_RED_DARK = (168, 40, 32)

# One period of the running meander, 5 px tall, repeating every 8 px. It is
# the same motif as the dialogue box (ui_frames.py), so every screen carries
# the identical key.
MEANDER = [
    "#####.##",
    "....#.#.",
    ".####.#.",
    ".#....#.",
    ".######.",
]

TRANSPARENT = (112, 200, 160)   # placeholder for index 0 in previews


def gba(c):
    """Snap an RGB triple to the GBA's 5-bit channels."""
    return tuple(v - v % 8 for v in c)


def pal16(colors, fill=(0, 0, 0)):
    """Pad a color list to 16 entries and check it is GBA-exact."""
    colors = list(colors) + [fill] * (16 - len(colors))
    assert len(colors) == 16, len(colors)
    for c in colors:
        assert all(v % 8 == 0 for v in c), c
    return colors


# --- Painting --------------------------------------------------------------
class Canvas:
    """An indexed image. Each pixel holds palette * 16 + color, so one canvas
    can carry several palettes and still preview correctly."""

    def __init__(self, w, h, fill=0):
        self.a = np.full((h, w), fill, dtype=np.uint8)

    @property
    def w(self):
        return self.a.shape[1]

    @property
    def h(self):
        return self.a.shape[0]

    def rect(self, x, y, w, h, c):
        self.a[max(y, 0):max(y + h, 0), max(x, 0):max(x + w, 0)] = c

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = c

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def frame(self, x, y, w, h, c):
        self.hline(x, y, w, c)
        self.hline(x, y + h - 1, w, c)
        self.vline(x, y, h, c)
        self.vline(x + w - 1, y, h, c)

    def grid(self, x, y, rows, key, transparent=" "):
        """Stamp a character grid. key maps characters to indices."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == transparent:
                    continue
                self.px(x + i, y + j, key[ch])

    def meander(self, x, y, w, ink, ground=None, flip=False):
        """A running meander band, 5 px tall, starting at x and clipped to w."""
        rows = MEANDER[::-1] if flip else MEANDER
        for j, row in enumerate(rows):
            for i in range(w):
                ch = row[i % 8]
                if ch == "#":
                    self.px(x + i, y + j, ink)
                elif ground is not None:
                    self.px(x + i, y + j, ground)

    def remap(self, mapping, x=0, y=0, w=None, h=None):
        w = self.w if w is None else w
        h = self.h if h is None else h
        sub = self.a[y:y + h, x:x + w]
        out = sub.copy()
        for k, v in mapping.items():
            out[sub == k] = v
        self.a[y:y + h, x:x + w] = out

    def paste(self, other, x, y, skip=None):
        a = other.a if isinstance(other, Canvas) else other
        h, w = a.shape
        region = self.a[y:y + h, x:x + w]
        if skip is None:
            region[:] = a
        else:
            m = a != skip
            region[m] = a[m]


def from_grid(rows, key, transparent=" "):
    c = Canvas(len(rows[0]), len(rows), 0)
    c.grid(0, 0, rows, key, transparent)
    return c


# --- Tiles and tilemaps ----------------------------------------------------
def tiles_of(a):
    """Split an (H, W) array into a row-major list of 8x8 arrays."""
    h, w = a.shape
    return [a[y:y + 8, x:x + 8] for y in range(0, h, 8) for x in range(0, w, 8)]


class TileSet:
    """Collects unique 4bpp tiles (deduplicated with flips) for a tilemap."""

    def __init__(self, reserved=0, flips=True):
        self.tiles = [np.zeros((8, 8), np.uint8)] * reserved
        self.lookup = {}
        self.flips = flips
        for i, t in enumerate(self.tiles):
            self._index(t, i)

    def _index(self, t, i):
        variants = [(t, 0)]
        if self.flips:
            variants += [(t[:, ::-1], 0x400), (t[::-1, :], 0x800), (t[::-1, ::-1], 0xC00)]
        for v, f in variants:
            self.lookup.setdefault(v.tobytes(), (i, f))

    def place(self, index, t):
        """Put a tile at a fixed index (the code draws it by number)."""
        t = np.asarray(t, np.uint8) & 15
        while len(self.tiles) <= index:
            self.tiles.append(np.zeros((8, 8), np.uint8))
        self.tiles[index] = t
        self.lookup = {}
        for i, tt in enumerate(self.tiles):
            self._index(tt, i)
        return index

    def add(self, t):
        """Return (index, flip bits) for a tile, adding it if new."""
        t = np.asarray(t, np.uint8) & 15
        hit = self.lookup.get(t.tobytes())
        if hit is not None:
            return hit
        i = len(self.tiles)
        self.tiles.append(t.copy())
        self._index(t, i)
        return i, 0

    def __len__(self):
        return len(self.tiles)


def compile_map(canvas, tileset, map_w=32, map_h=32, origin=(0, 0), region=None, palette_of=None):
    """Cut a canvas into a map_w x map_h tilemap of u16 entries.

    The canvas pixel values carry their palette in the high nibble; a tile must
    use a single palette. region (x, y, w, h in tiles) limits which cells are
    filled; the rest stay 0. palette_of(tx, ty) can force a palette number.
    """
    entries = np.zeros((map_h, map_w), np.uint16)
    ox, oy = origin
    cw, ch = canvas.w // 8, canvas.h // 8
    rx, ry, rw, rh = region or (0, 0, cw, ch)
    for ty in range(ry, ry + rh):
        for tx in range(rx, rx + rw):
            cell = canvas.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            pals = set((cell[cell & 15 != 0] >> 4).tolist())
            if palette_of is not None:
                pal = palette_of(tx, ty)
            else:
                assert len(pals) <= 1, f"tile ({tx},{ty}) mixes palettes {pals}"
                pal = pals.pop() if pals else 0
            idx, flip = tileset.add(cell & 15)
            entries[oy + ty, ox + tx] = idx | flip | (pal << 12)
    return entries


def write_tilemap(path, entries):
    Path(path).write_bytes(entries.astype("<u2").tobytes())
    print(f"wrote {Path(path).relative_to(ROOT)}")


def read_tilemap(path, w=32):
    a = np.frombuffer(Path(path).read_bytes(), dtype="<u2")
    return a.reshape(-1, w)


def write_tiles_png(path, tiles, palettes, tiles_wide=16, min_tiles=0, pal_of_tile=None):
    """Write tiles as an indexed PNG. palettes is a list of 16-color lists; an
    8-bit PNG is written when there is more than one, with each tile's pixels
    offset into its palette so the sheet previews in its real colors."""
    n = max(len(tiles), min_tiles)
    rows = (n + tiles_wide - 1) // tiles_wide
    a = np.zeros((rows * 8, tiles_wide * 8), np.uint8)
    for i, t in enumerate(tiles):
        p = pal_of_tile(i) if pal_of_tile else 0
        y, x = (i // tiles_wide) * 8, (i % tiles_wide) * 8
        a[y:y + 8, x:x + 8] = (np.asarray(t, np.uint8) & 15) + p * 16
    write_indexed_png(path, a, palettes)


def write_indexed_png(path, a, palettes, transparency=None):
    flat = [v for pal in palettes for c in pal16(pal) for v in c]
    im = Image.fromarray(np.asarray(a, np.uint8), "P")
    im.putpalette(flat)
    options = {} if transparency is None else {"transparency": transparency}
    if len(palettes) == 1:
        assert int(np.asarray(a).max()) < 16
        im.save(path, bits=4, **options)
    else:
        im.save(path, **options)
    print(f"wrote {Path(path).relative_to(ROOT)}")


def write_jasc(path, colors):
    lines = ["JASC-PAL", "0100", str(len(colors))] + ["%d %d %d" % tuple(c) for c in colors]
    Path(path).write_text("\r\n".join(lines) + "\r\n")
    print(f"wrote {Path(path).relative_to(ROOT)}")


def read_jasc(path):
    lines = Path(path).read_text().split()
    n = int(lines[2])
    v = list(map(int, lines[3:3 + 3 * n]))
    return [tuple(v[i:i + 3]) for i in range(0, 3 * n, 3)]


def png_palette(path):
    im = Image.open(path)
    p = im.getpalette()
    return [tuple(p[i:i + 3]) for i in range(0, len(p), 3)]


# --- Previews --------------------------------------------------------------
def render_map(entries, tiles, palettes, w=30, h=20, transparent=None):
    """Render a tilemap to RGB. tiles: list of 8x8 index arrays (low nibble);
    palettes: list of 16-color lists indexed by the entries' palette number."""
    out = np.zeros((h * 8, w * 8, 3), np.uint8)
    if transparent is not None:
        out[:] = transparent
    for ty in range(h):
        for tx in range(w):
            e = int(entries[ty, tx])
            idx, hf, vf, pal = e & 0x3FF, e & 0x400, e & 0x800, e >> 12
            if idx >= len(tiles):
                continue
            t = np.asarray(tiles[idx]) & 15
            if hf:
                t = t[:, ::-1]
            if vf:
                t = t[::-1, :]
            p = np.array(pal16(palettes[pal]) if pal < len(palettes) else [(255, 0, 255)] * 16, np.uint8)
            block = p[t]
            if transparent is not None:
                m = t == 0
                block[m] = out[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8][m]
            out[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = block
    return out


def load_tiles(path):
    a = np.array(Image.open(path))
    return [t & 15 for t in tiles_of(a)]


def save_rgb(path, rgb, scale=1):
    im = Image.fromarray(np.asarray(rgb, np.uint8), "RGB")
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(path)
    try:
        shown = Path(path).relative_to(ROOT)
    except ValueError:
        shown = path
    print(f"wrote {shown}")


def canvas_rgb(canvas, palettes):
    """Preview a multi-palette canvas (pixel = pal * 16 + color)."""
    flat = np.array([c for pal in palettes for c in pal16(pal)], np.uint8)
    return flat[canvas.a]
