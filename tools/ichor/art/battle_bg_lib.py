"""Shared toolkit for Ichor's battle backgrounds (the "battle environments").

How the engine draws a battle background (pokeemerald-expansion 1.17.2):

* BG3 holds the scene: a 4bpp tileset in char block 2 (``tiles.png``, 128x128,
  at most 256 tiles), a 64x32-tile map (``map.bin``: two 32x32 screen blocks
  side by side) and 48 colors loaded to BG palettes 2-4 (``palette.pal``).
  Every map entry picks one of those three palettes, so each 8x8 tile may use
  the 15 colors of one sub-palette. Index 0 would show the backdrop, so the
  scene never uses it.
* Only the left 240x112 is normally on screen: the battle text box (BG0)
  covers y >= 112. During the intro slide the top half of BG3 scrolls in from
  x = 240 and the bottom half from x = -240, so the whole 512-pixel width is
  seen and it must wrap seamlessly. After a catch the game shows x = 256..495
  (the scene without platforms). So every scene here is painted as a
  256-pixel-wide strip that tiles horizontally; the left screen block gets the
  two platforms on top, the right block is the bare strip.
* BG1 holds the "entry" overlay that sweeps across during the intro (grass,
  sand, waves, light streaks): ``anim_tiles.png`` and a 32x32 ``anim_map.bin``,
  drawn with the same three palettes. There index 0 is transparent.

A scene is painted on a Canvas of color *names*; a Pal maps each name to a
GBA color and to one of the three sub-palettes. ``tileize`` cuts the canvas
into 8x8 tiles, picks a sub-palette for each, dedupes (with flips) and writes
the files. Palette variants reuse the same layout with other colors.

Colors must be multiples of 8 so they map exactly to GBA BGR555.
"""
from __future__ import annotations

import struct
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
ENV = ROOT / "graphics/battle_environment"

STRIP = 256          # scenery period: one screen block
MAP_W, MAP_H = 64, 32
VIEW_W, VIEW_H = 240, 160
TEXTBOX_Y = 112      # the battle text box covers BG3 from here down

# Where the engine puts the two battlers in a single battle
# (sBattlerCoords, src/battle_anim_mons.c): sprite centers.
OPPONENT_XY = (176, 40)
PLAYER_XY = (72, 80)
# Platform ellipse centers used by every Ichor scene, matched to those.
OPP_PLATFORM = (176, 69)
PLR_PLATFORM = (64, 109)


def check_rgb(c):
    assert len(c) == 3 and all(0 <= v <= 248 and v % 8 == 0 for v in c), c
    return tuple(c)


# --------------------------------------------------------------------------
# Palettes
# --------------------------------------------------------------------------

class Pal:
    """Three sub-palettes of up to 15 named colors each (slot 0 unused).

    colors: {name: (r, g, b)}
    subs:   three lists of names; a name may appear in more than one.
    """

    def __init__(self, colors, subs, zero=(0, 0, 0)):
        assert len(subs) == 3
        self.colors = {n: check_rgb(c) for n, c in colors.items()}
        self.subs = [list(s) for s in subs]
        for s in self.subs:
            assert len(s) <= 15, f"sub-palette has {len(s)} colors > 15: {s}"
            for n in s:
                assert n in self.colors, f"unknown color {n}"
        self.zero = check_rgb(zero)

    def variant(self, **overrides):
        c = dict(self.colors)
        for n, v in overrides.items():
            assert n in c, f"unknown color {n}"
            c[n] = v
        return Pal(c, self.subs, self.zero)

    def rgb48(self):
        out = []
        for s in self.subs:
            row = [self.zero] + [self.colors[n] for n in s]
            row += [(0, 0, 0)] * (16 - len(row))
            out += row
        return out

    def write_jasc(self, path):
        cols = self.rgb48()
        with open(path, "w", newline="\r\n") as f:
            f.write("JASC-PAL\n0100\n48\n")
            for c in cols:
                f.write("%d %d %d\n" % c)
        print(f"wrote {Path(path).relative_to(ROOT)}")

    def local(self, sub, name):
        return self.subs[sub].index(name) + 1


def read_jasc(path):
    v = Path(path).read_text().split()
    n = int(v[2])
    nums = list(map(int, v[3:3 + 3 * n]))
    return [tuple(nums[i * 3:i * 3 + 3]) for i in range(n)]


# --------------------------------------------------------------------------
# Canvas
# --------------------------------------------------------------------------

class Canvas:
    """A grid of color names. x wraps around the width when wrap=True."""

    def __init__(self, w, h, fill=None, wrap=True):
        self.w, self.h, self.wrap = w, h, wrap
        self.px = [[fill] * w for _ in range(h)]

    def get(self, x, y):
        if self.wrap:
            x %= self.w
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.px[y][x]
        return None

    def set(self, x, y, name):
        if name is None:
            return
        if self.wrap:
            x %= self.w
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = name

    def rect(self, x0, y0, x1, y1, name):
        """Fill x0 <= x < x1, y0 <= y < y1."""
        for y in range(y0, y1):
            for x in range(x0, x1):
                self.set(x, y, name)

    def hline(self, x0, x1, y, name):
        for x in range(x0, x1):
            self.set(x, y, name)

    def stamp(self, grid, legend, x, y, hflip=False):
        """Draw an ASCII grid. legend maps a char to a color name; chars not in
        the legend (and ' ') are transparent."""
        for j, row in enumerate(grid):
            if hflip:
                row = row[::-1]
            for i, ch in enumerate(row):
                n = legend.get(ch)
                if n is not None:
                    self.set(x + i, y + j, n)

    def copy(self):
        c = Canvas(self.w, self.h, wrap=self.wrap)
        c.px = [r[:] for r in self.px]
        return c

    def paste(self, other, x, y):
        for j in range(other.h):
            for i in range(other.w):
                n = other.px[j][i]
                if n is not None:
                    self.set(x + i, y + j, n)

    def recolor(self, mapping, x0=0, y0=0, x1=None, y1=None):
        x1 = self.w if x1 is None else x1
        y1 = self.h if y1 is None else y1
        for y in range(y0, y1):
            for x in range(x0, x1):
                n = self.px[y][x]
                if n in mapping:
                    self.px[y][x] = mapping[n]


def hash2(x, y):
    """A stable pseudo-random int for a pixel (x wraps at the strip width), for
    scattering texture without visible repeats."""
    h = ((x % STRIP) * 374761393 + y * 668265263) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return h ^ (h >> 16)


def check_grid(grid, w=None):
    """Pad an ASCII grid's rows with spaces (transparent) to one width."""
    w = w or max(len(r) for r in grid)
    for r in grid:
        assert len(r) <= w, f"grid row {r!r} wider than {w}"
    return [r.ljust(w) for r in grid]


# --------------------------------------------------------------------------
# Shapes
# --------------------------------------------------------------------------

def in_ellipse(x, y, cx, cy, rx, ry):
    """Pixel-center test for an ellipse centered between pixels at (cx, cy):
    the pixel x covers [x, x+1), so its center is x + 0.5."""
    dx = (x + 0.5 - cx) / rx
    dy = (y + 0.5 - cy) / ry
    return dx * dx + dy * dy <= 1.0


def ellipse_rows(cx, cy, rx, ry):
    """{y: (x0, x1)} spans (x1 exclusive) of a filled ellipse."""
    rows = {}
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        xs = [x for x in range(int(cx - rx) - 1, int(cx + rx) + 2)
              if in_ellipse(x, y, cx, cy, rx, ry)]
        if xs:
            rows[y] = (xs[0], xs[-1] + 1)
    return rows


def gradient(c, y0, bands):
    """Horizontal bands from y0 down: bands = [(name, rows), ...]. Between two
    bands the first row of the lower band is a 1:1 checker of both, so the
    step softens without costing more than one tile per band edge."""
    y = y0
    prev = None
    for name, rows in bands:
        for r in range(rows):
            for x in range(c.w):
                if r == 0 and prev is not None:
                    c.set(x, y, name if (x + y) % 2 else prev)
                else:
                    c.set(x, y, name)
            y += 1
        prev = name
    return y


def platform(c, cx, cy, rx, ry, depth, top, side, rim=None, shadow=None, under=None):
    """A raised disc seen from the front.

    top(x, y, u, v) -> name for the top face, where (u, v) in [-1, 1] are the
    pixel's position in the ellipse (u left->right, v back->front).
    side(x, y, t, u) -> name for the front side band, t = 0..depth-1 rows
    below the top face's edge.
    rim:    name for a 1 px edge along the top face's back half (or None).
    shadow: name for a 1-2 px contact shadow under the side band (or None).
    under:  optional name painted where the shadow falls but only over
            pixels already of that name (lets shadows sit on grass only).
    """
    toprows = ellipse_rows(cx, cy, rx, ry)
    lowrows = ellipse_rows(cx, cy + depth, rx, ry)
    # side band: inside the lowered ellipse, below the top ellipse
    for y, (x0, x1) in lowrows.items():
        for x in range(x0, x1):
            if in_ellipse(x, y, cx, cy, rx, ry):
                continue
            # rows below the top edge at this x
            t = 0
            while t < depth + 2 and not in_ellipse(x, y - t - 1, cx, cy, rx, ry):
                t += 1
            u = (x + 0.5 - cx) / rx
            c.set(x, y, side(x, y, min(t, depth - 1), u))
    if shadow:
        sh = ellipse_rows(cx + 3, cy + depth + 1, rx - 1, ry)
        for y, (x0, x1) in sh.items():
            for x in range(x0, x1):
                if in_ellipse(x, y, cx, cy + depth, rx, ry) or in_ellipse(x, y, cx, cy, rx, ry):
                    continue
                if under is None or c.get(x, y) in under:
                    c.set(x, y, shadow)
    for y, (x0, x1) in toprows.items():
        for x in range(x0, x1):
            u = (x + 0.5 - cx) / rx
            v = (y + 0.5 - cy) / ry
            c.set(x, y, top(x, y, u, v))
    if rim:
        for y, (x0, x1) in toprows.items():
            for x in (x0, x1 - 1):
                c.set(x, y, rim)
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            ys = [y for y in toprows if toprows[y][0] <= x < toprows[y][1]]
            if ys:
                c.set(x, min(ys), rim)


# --------------------------------------------------------------------------
# Tiles
# --------------------------------------------------------------------------

def _flip(t, h, v):
    rows = [t[i * 8:(i + 1) * 8] for i in range(8)]
    if v:
        rows = rows[::-1]
    if h:
        rows = [r[::-1] for r in rows]
    return tuple(p for r in rows for p in r)


class Tileset:
    """Accumulates unique 4bpp tiles (dedupe with h/v flips)."""

    def __init__(self, pal, palbase=2, max_tiles=256, blank_first=True):
        self.pal, self.palbase, self.max = pal, palbase, max_tiles
        self.tiles, self.first_sub, self.index = [], [], {}
        if blank_first:
            self._add((0,) * 64, 0)

    def _add(self, t, sub):
        self.index[t] = (len(self.tiles), 0, 0)
        self.tiles.append(t)
        self.first_sub.append(sub)
        return len(self.tiles) - 1

    def entry(self, names):
        """names: 64 color names (None = transparent) -> u16 map entry."""
        used = {n for n in names if n is not None}
        if not used:
            return 0  # blank tile, palette 0
        sub = None
        for s, lst in enumerate(self.pal.subs):
            if used <= set(lst):
                sub = s
                break
        if sub is None:
            raise ValueError(f"no sub-palette holds all of {sorted(used)}")
        t = tuple(0 if n is None else self.pal.local(sub, n) for n in names)
        for h in (0, 1):
            for v in (0, 1):
                k = _flip(t, h, v)
                if k in self.index:
                    tid = self.index[k][0]
                    return tid | (h << 10) | (v << 11) | ((self.palbase + sub) << 12)
        tid = self._add(t, sub)
        return tid | ((self.palbase + sub) << 12)

    def write_png(self, path):
        n = len(self.tiles)
        assert n <= self.max, f"{path}: {n} tiles > {self.max}"
        im = Image.new("P", (128, 128))
        px = im.load()
        for i, t in enumerate(self.tiles):
            ox, oy = (i % 16) * 8, (i // 16) * 8
            for j, c in enumerate(t):
                # 8-bit index = sub-palette * 16 + color so the PNG previews in
                # the right colors; the build keeps the low 4 bits.
                px[ox + j % 8, oy + j // 8] = self.first_sub[i] * 16 + c if c else 0
        flat = [v for c in self.pal.rgb48() for v in c]
        im.putpalette(flat)
        im.save(path)
        print(f"wrote {Path(path).relative_to(ROOT)} ({n} tiles)")


def canvas_tiles(c, tx, ty):
    return [c.px[ty * 8 + j][tx * 8 + i] for j in range(8) for i in range(8)]


def write_map(path, entries):
    Path(path).write_bytes(struct.pack("<%dH" % len(entries), *entries))
    print(f"wrote {Path(path).relative_to(ROOT)}")


def preview_canvas(canvas, pal, path, scale=2):
    """Render a canvas of names straight to RGB (before any tile limits)."""
    im = Image.new("RGB", (canvas.w, canvas.h), (255, 0, 255))
    px = im.load()
    for y in range(canvas.h):
        for x in range(canvas.w):
            n = canvas.px[y][x]
            if n is not None:
                px[x, y] = pal.colors[n]
    im = im.resize((canvas.w * scale, canvas.h * scale), Image.NEAREST)
    im.save(path)
    return im


def _tile_entries(canvas, pal, palbase, blocks, need_full):
    ts = Tileset(pal, palbase)
    entries, errors = [], []
    for block in blocks:
        for ty in range(32):
            for tx in range(32):
                names = canvas_tiles(canvas, block * 32 + tx, ty)
                if need_full:
                    assert None not in names, f"hole in BG3 tile ({block * 32 + tx},{ty})"
                try:
                    entries.append(ts.entry(names))
                except ValueError as e:
                    errors.append(((block * 32 + tx) * 8, ty * 8, str(e)))
                    entries.append(0)
    if errors:
        for x, y, e in errors[:40]:
            print(f"  tile at x={x} y={y}: {e}")
        raise SystemExit(f"{len(errors)} tiles mix sub-palettes")
    return ts, entries


def build_bg(canvas, pal, outdir, palbase=2):
    """canvas: 512x256. Writes tiles.png and map.bin (two 32x32 blocks)."""
    assert canvas.w == MAP_W * 8 and canvas.h == MAP_H * 8
    ts, entries = _tile_entries(canvas, pal, palbase, (0, 1), True)
    ts.write_png(outdir / "tiles.png")
    write_map(outdir / "map.bin", entries)
    return ts, entries


def build_anim(canvas, pal, outdir, palbase=2):
    """canvas: 256x256, None = transparent. Writes anim_tiles.png/anim_map.bin."""
    assert canvas.w == 256 and canvas.h == 256
    ts, entries = _tile_entries(canvas, pal, palbase, (0,), False)
    ts.write_png(outdir / "anim_tiles.png")
    write_map(outdir / "anim_map.bin", entries)
    return ts, entries


def compose(strip, platforms):
    """strip: 256x256 wrapped scenery. platforms: a 256x256 overlay canvas
    (None = see-through) for the left block. Returns the 512x256 BG canvas."""
    full = Canvas(512, 256, wrap=False)
    for y in range(256):
        for x in range(256):
            p = platforms.px[y][x]
            full.px[y][x] = p if p is not None else strip.px[y][x]
            full.px[y][x + 256] = strip.px[y][x]
    return full


# --------------------------------------------------------------------------
# Rendering built files (for mock-ups)
# --------------------------------------------------------------------------

def render_map(tiles_png, map_bin, pal48, w, h, palbase=2, transparent=None):
    """Render a GBA text-BG map exactly as the hardware would. For a 64-wide
    map the entries are two 32x32 screen blocks. Index 0 pixels get
    `transparent` (None -> RGBA alpha 0)."""
    im = Image.open(tiles_png)
    src = im.load()
    tw = im.size[0] // 8
    data = Path(map_bin).read_bytes()
    ent = struct.unpack("<%dH" % (len(data) // 2), data)
    out = Image.new("RGBA", (w * 8, h * 8), (0, 0, 0, 0))
    o = out.load()
    for ty in range(h):
        for tx in range(w):
            idx = (tx // 32) * 1024 + ty * 32 + (tx % 32) if w > 32 else ty * 32 + tx
            e = ent[idx]
            t, hf, vf, pn = e & 0x3FF, e >> 10 & 1, e >> 11 & 1, e >> 12
            sx, sy = (t % tw) * 8, (t // tw) * 8
            for y in range(8):
                for x in range(8):
                    xx = 7 - x if hf else x
                    yy = 7 - y if vf else y
                    ci = src[sx + xx, sy + yy] % 16 if sy + yy < im.size[1] else 0
                    if ci == 0:
                        if transparent is not None:
                            o[tx * 8 + x, ty * 8 + y] = transparent + (255,)
                        continue
                    pi = (pn - palbase) * 16 + ci
                    c = pal48[pi] if 0 <= pi < len(pal48) else (255, 0, 255)
                    o[tx * 8 + x, ty * 8 + y] = tuple(v - v % 8 for v in c) + (255,)
    return out
