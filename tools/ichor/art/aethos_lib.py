"""Shared toolkit for drawing the aethos primary tileset.

aethos keeps General's 512 metatile ids, behaviors and layer usage, so every
layout still means the same thing. Its art is redrawn from scratch: the
painters (aethos_*.py) draw each metatile's layers into three 128x1024 RGBA
canvases, which Porytiles compiles into porytiles_bin/.

General's decompiled sources (tools/ichor/art/base/aethos) are used only as a
map: which layers a metatile uses, where a material sits (water, sand, rock),
and which 8x8 tiles are animation key frames. No General pixel is copied out.

Conventions:
  * Colors are RGB multiples of 8 (exact GBA BGR555). Transparent pixels are
    written as magenta, Porytiles' extrinsic transparency.
  * Hand-drawn art is ASCII: one char per pixel, looked up in a legend of
    named colors from PAL. '.' and ' ' are transparent.
  * Layers are 0 bottom, 1 middle, 2 top. A metatile may use two at most.
"""
from __future__ import annotations

import shutil
import textwrap
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "tools/ichor/art/base/aethos"
OUT = ROOT / "data/tilesets/primary/aethos/porytiles_src"
PORYTILES = Path.home() / ".local/bin/porytiles"
MAGENTA = (255, 0, 255)
B, M, T = 0, 1, 2

# --------------------------------------------------------------------------
# Master palette: design/phase1/PLAN.md families plus in-family steps.
# --------------------------------------------------------------------------
PAL = {
    "ink": (32, 24, 24),
    # sun-bleached grass
    "gr_s": (120, 136, 56),     # deep shade (under trees)
    "gr_d": (144, 152, 72),     # tuft
    "gr_m": (184, 184, 104),    # field
    "gr_l": (208, 200, 128),    # light
    "gr_h": (232, 224, 160),    # straw fleck
    # tall grass / reeds
    "tg_k": (40, 56, 24),
    "tg_d": (72, 96, 40),
    "tg_m": (112, 136, 56),
    "tg_l": (160, 176, 80),
    # olive tree
    "ol_k": (40, 56, 32),       # outline
    "ol_d": (72, 88, 48),
    "ol_m": (112, 128, 80),
    "ol_l": (152, 168, 120),
    "ol_s": (200, 208, 176),    # silver leaf
    # gnarled trunk, gray-brown
    "tr_k": (48, 40, 32),
    "tr_d": (88, 72, 56),
    "tr_m": (128, 112, 88),
    "tr_l": (168, 152, 128),
    # cypress
    "cy_k": (16, 40, 32),
    "cy_d": (24, 56, 40),
    "cy_m": (40, 88, 56),
    "cy_l": (72, 120, 72),
    # stone pine
    "pn_d": (40, 72, 40),
    "pn_m": (64, 104, 56),
    "pn_l": (104, 144, 80),
    # limestone path
    "lp_d": (176, 144, 96),
    "lp_m": (208, 184, 136),
    "lp_l": (232, 216, 176),
    "lp_h": (248, 240, 216),
    # earth / tilled soil
    "dt_k": (88, 56, 40),
    "dt_d": (128, 88, 56),
    "dt_m": (168, 128, 88),
    # limestone rock (cliffs, boulders, walls)
    "rk_k": (64, 56, 56),
    "rk_d": (112, 104, 96),
    "rk_m": (160, 152, 136),
    "rk_l": (200, 192, 168),
    "rk_h": (232, 224, 200),
    # marble
    "mb_d": (128, 120, 112),
    "mb_m": (168, 160, 152),
    "mb_l": (216, 208, 192),
    "mb_h": (248, 248, 240),
    # terracotta
    "tc_d": (120, 48, 24),
    "tc_m": (184, 88, 48),
    "tc_l": (224, 136, 88),
    # sun-gold
    "sg_d": (200, 144, 40),
    "sg_l": (240, 192, 64),
    # red anemone / poppy
    "fl_d": (152, 24, 32),
    "fl_m": (216, 56, 40),
    "fl_l": (248, 120, 88),
    # sand
    "sd_d": (200, 168, 104),
    "sd_m": (232, 208, 144),
    "sd_l": (248, 232, 184),
    # Aegean
    "ae_k": (16, 40, 96),
    "ae_d": (24, 56, 120),
    "ae_m": (48, 104, 176),
    "ae_n": (80, 136, 200),
    "ae_l": (112, 168, 224),
    "ae_h": (176, 216, 240),
    "ae_t": (88, 176, 200),     # turquoise shallows
    "foam": (248, 248, 240),
    # wood
    "wd_d": (96, 64, 40),
    "wd_m": (144, 104, 64),
    "wd_l": (184, 144, 96),
}
# The primary has 6 palettes of 15 colors, and Porytiles must fit every tile
# into one of them. So the families above share ramps, planned as:
#   grove   gk gd gm ol_l ol_s cy_d cy_m cy_l gr_d gr_m gr_l ink tr_d mb_d mb_m
#   meadow  gk gd gm tg_l gr_d gr_m gr_l lp_l sg_d sg_l fl_d fl_m fl_l ink
#   earth   gr_d gr_m gr_l gm lp_k lp_d lp_m lp_l lp_h dt_d dt_m sd_d sd_m ink
#   sea     ae_d ae_m ae_n ae_l ae_h ae_t mb_h sd_d sd_m lp_k lp_d lp_m lp_l lp_h ink
#   marble  mb_d mb_m mb_l mb_h tc_d tc_m tc_l sg_d sg_l ae_m ae_l lp_d lp_l ink
#   plaza   gr_d gr_m gr_l gm mb_d mb_m mb_l mb_h tc_m tc_l sg_l ae_m ae_l lp_l ink
# Names below are aliases onto those shared ramps: natural rock is warm
# limestone (the path ramp), bark is ink, umber and marble grays, and every
# green outline is one dark olive.
PAL.update({
    "gk": (40, 56, 32), "gd": (72, 88, 48), "gm": (112, 128, 64),
    "lp_k": (120, 96, 64),
})
ALIASES = {
    "ol_k": "gk", "tg_k": "gk", "cy_k": "gk",
    "ol_d": "gd", "tg_d": "gd",
    "ol_m": "gm", "tg_m": "gm", "gr_s": "gm",
    "gr_h": "lp_l", "sd_l": "lp_h", "ae_k": "ae_d", "foam": "mb_h",
    "tr_k": "ink", "tr_m": "mb_d", "tr_l": "mb_m", "dt_k": "tr_d",
    "rk_k": "lp_k", "rk_d": "lp_d", "rk_m": "lp_m", "rk_l": "lp_l", "rk_h": "lp_h",
    "pn_d": "cy_d", "pn_m": "cy_m", "pn_l": "cy_l",
    "wd_d": "tr_d", "wd_m": "dt_d", "wd_l": "dt_m",
}
for _a, _b in ALIASES.items():
    PAL[_a] = PAL[_b]
for _n, _c in PAL.items():
    assert all(v % 8 == 0 and 0 <= v <= 248 for v in _c), (_n, _c)


def rgba(name):
    if name is None:
        return (0, 0, 0, 0)
    return PAL[name] + (255,)


# --------------------------------------------------------------------------
# ASCII art
# --------------------------------------------------------------------------

def art(text, legend):
    """ASCII art -> (h, w, 4) uint8. legend maps chars to PAL names."""
    rows = [r for r in textwrap.dedent(text).split("\n") if r.strip()]
    w = max(len(r) for r in rows)
    out = np.zeros((len(rows), w, 4), np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in ". ":
                continue
            out[y, x] = rgba(legend[ch])
    return out


def flip_h(img):
    return img[:, ::-1].copy()


def flip_v(img):
    return img[::-1].copy()


def tile16(img, x0=0, y0=0):
    """A 16x16 window of a pattern that repeats every img.shape pixels."""
    h, w = img.shape[:2]
    ys = (np.arange(16) + y0) % h
    xs = (np.arange(16) + x0) % w
    return img[ys][:, xs].copy()


def over(dst, src):
    """Alpha-over (binary alpha), in place. Shapes must match."""
    m = src[..., 3] > 0
    dst[m] = src[m]
    return dst


def solid(name, h=16, w=16):
    out = np.zeros((h, w, 4), np.uint8)
    out[:] = rgba(name)
    return out


def recolor(img, mapping):
    """Swap named colors: mapping {from_name: to_name}."""
    out = img.copy()
    for a, b in mapping.items():
        m = (img[..., :3] == PAL[a]).all(-1) & (img[..., 3] > 0)
        out[m] = rgba(b)
    return out


# --------------------------------------------------------------------------
# The three layer canvases
# --------------------------------------------------------------------------

def mt_xy(m):
    return (m % 8) * 16, (m // 8) * 16


def load_rgba(path):
    a = np.array(Image.open(path).convert("RGBA"))
    t = (a[..., 3] == 0) | (a[..., :3] == MAGENTA).all(-1)
    a[t] = 0
    return a


class Base:
    """General's decompiled layers, used as a geometry/material map."""

    def __init__(self):
        self.L = np.stack([load_rgba(BASE / f"{n}.png") for n in ("bottom", "middle", "top")])

    def get(self, m, layer):
        x, y = mt_xy(m)
        return self.L[layer, y:y + 16, x:x + 16]

    def layers(self, m):
        return [l for l in range(3) if self.get(m, l)[..., 3].any()]

    def comp(self, m):
        out = np.zeros((16, 16, 4), np.uint8)
        for l in range(3):
            over(out, self.get(m, l))
        return out

    def mask(self, m, colors, layers=(0, 1, 2)):
        """Pixels of metatile m whose General color is in `colors`."""
        out = np.zeros((16, 16), bool)
        for l in layers:
            a = self.get(m, l)
            for c in colors:
                out |= (a[..., :3] == c).all(-1) & (a[..., 3] > 0)
        return out


class Sheet:
    def __init__(self):
        self.L = np.zeros((3, 1024, 128, 4), np.uint8)
        self.owner = {}  # metatile -> painter name, to catch double painting

    def view(self, m, layer):
        x, y = mt_xy(m)
        return self.L[layer, y:y + 16, x:x + 16]

    def clear(self, m, layers=(0, 1, 2)):
        for l in layers:
            self.view(m, l)[:] = 0

    def set(self, m, layer, img):
        assert img.shape == (16, 16, 4), img.shape
        self.view(m, layer)[:] = img

    def put(self, m, layer, img, x=0, y=0):
        """Alpha-paste img with its top-left at (x, y) inside metatile m,
        clipped to the metatile."""
        v = self.view(m, layer)
        h, w = img.shape[:2]
        sx0, sy0 = max(0, -x), max(0, -y)
        dx0, dy0 = max(0, x), max(0, y)
        sx1, sy1 = min(w, 16 - x), min(h, 16 - y)
        if sx1 <= sx0 or sy1 <= sy0:
            return
        over(v[dy0:dy0 + sy1 - sy0, dx0:dx0 + sx1 - sx0], img[sy0:sy1, sx0:sx1])

    def put_grid(self, grid, layer, img, x=0, y=0):
        """Paste a big image across a grid of metatiles.

        grid: rows of metatile ids (None to skip); img lands at pixel (x, y)
        of the grid's top-left corner. `layer` may be an int or a dict
        {metatile: layer} or a callable(row, col) -> layer.
        """
        for r, row in enumerate(grid):
            for c, m in enumerate(row):
                if m is None:
                    continue
                l = layer
                if isinstance(layer, dict):
                    l = layer.get(m, None)
                elif callable(layer):
                    l = layer(r, c)
                if l is None:
                    continue
                self.put(m, l, img, x - c * 16, y - r * 16)

    def used(self, m):
        return [l for l in range(3) if self.view(m, l)[..., 3].any()]


# --------------------------------------------------------------------------
# Animation key frames
# --------------------------------------------------------------------------

ANIMS = ("flower", "water", "sand_water_edge", "land_water_edge", "waterfall")


def split_tiles(a):
    h, w = a.shape[:2]
    return [a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
            for ty in range(h // 8) for tx in range(w // 8)]


def join_tiles(tiles, w_tiles):
    rows = (len(tiles) + w_tiles - 1) // w_tiles
    out = np.zeros((rows * 8, w_tiles * 8, 4), np.uint8)
    for i, t in enumerate(tiles):
        y, x = divmod(i, w_tiles)
        out[y * 8:y * 8 + 8, x * 8:x * 8 + 8] = t
    return out


def anim_shape(name):
    a = load_rgba(BASE / "anim" / name / "key.png")
    return a.shape[1] // 8, len(split_tiles(a))


def anim_frame_names(name):
    d = BASE / "anim" / name
    return sorted([p.stem for p in d.glob("*.png") if p.stem != "key"], key=int)


def scan_anim_uses(base):
    """{(m, layer, quadrant): (anim, tile, hflip, vflip)} for General."""
    keys = {}
    for name in ANIMS:
        for i, t in enumerate(split_tiles(load_rgba(BASE / "anim" / name / "key.png"))):
            for hf in (0, 1):
                for vf in (0, 1):
                    tt = t[:, ::-1] if hf else t
                    tt = tt[::-1] if vf else tt
                    keys.setdefault(tt.tobytes(), (name, i, hf, vf))
    uses = {}
    for l in range(3):
        for m in range(512):
            a = base.get(m, l)
            for q in range(4):
                qx, qy = (q % 2) * 8, (q // 2) * 8
                k = keys.get(np.ascontiguousarray(a[qy:qy + 8, qx:qx + 8]).tobytes())
                if k:
                    uses[(m, l, q)] = k
    return uses


def place_anim_keys(sheet, uses, keys):
    """Stamp new key tiles where General used animated tiles.

    keys: {anim: [8x8 RGBA tiles]}. Anims missing from `keys` are skipped."""
    for (m, l, q), (name, i, hf, vf) in uses.items():
        if name not in keys:
            continue
        t = keys[name][i]
        if hf:
            t = t[:, ::-1]
        if vf:
            t = t[::-1]
        qx, qy = (q % 2) * 8, (q // 2) * 8
        sheet.view(m, l)[qy:qy + 8, qx:qx + 8] = t


# --------------------------------------------------------------------------
# Tile dictionary: the primary holds 512 tiles, 60 of them animation slots,
# so art is budgeted per 8x8 tile, with flips counting as the same tile.
# --------------------------------------------------------------------------

FLIPS = ((0, 0), (1, 0), (0, 1), (1, 1))


def flip(t, hf, vf):
    if hf:
        t = t[:, ::-1]
    if vf:
        t = t[::-1]
    return np.ascontiguousarray(t)


def canon(t):
    """(canonical bytes, hf, vf) such that flip(canonical, hf, vf) == t."""
    best = None
    for hf, vf in FLIPS:
        b = flip(t, hf, vf).tobytes()
        if best is None or b < best[0]:
            best = (b, hf, vf)
    return best


def quad(view, q):
    qx, qy = (q % 2) * 8, (q // 2) * 8
    return view[qy:qy + 8, qx:qx + 8]


def tile_index(layers_get, skip=()):
    """Group every non-empty 8x8 tile by flip-canonical form.

    layers_get(m, l) -> 16x16x4. Returns (canon_tiles, uses) where uses is a
    list of (m, l, q, ci, hf, vf) and flip(canon_tiles[ci], hf, vf) is the
    tile at that spot."""
    index, tiles, uses = {}, [], []
    for m in range(512):
        for l in range(3):
            v = layers_get(m, l)
            for q in range(4):
                if (m, l, q) in skip:
                    continue
                t = np.ascontiguousarray(quad(v, q))
                if not t[..., 3].any():
                    continue
                b, hf, vf = canon(t)
                if b not in index:
                    index[b] = len(tiles)
                    tiles.append(flip(t, hf, vf))  # canonical orientation
                uses.append((m, l, q, index[b], hf, vf))
    return tiles, uses


def count_tiles(sheet, skip=()):
    tiles, _ = tile_index(sheet.view, skip)
    return len(tiles)


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def to_png(a, path):
    out = a.copy()
    t = out[..., 3] == 0
    out[t] = MAGENTA + (255,)
    out[..., 3] = 255
    Image.fromarray(out, "RGBA").save(path)


def validate(sheet):
    problems = []
    for m in range(512):
        u = sheet.used(m)
        if len(u) > 2:
            problems.append(f"{m:03X}: content on three layers")
        for l in u:
            v = sheet.view(m, l)
            for q in range(4):
                qx, qy = (q % 2) * 8, (q // 2) * 8
                t = v[qy:qy + 8, qx:qx + 8]
                cols = {tuple(p) for p in t[t[..., 3] > 0][:, :3].tolist()}
                if len(cols) > 15:
                    problems.append(f"{m:03X} layer {l} tile {q}: {len(cols)} colors")
                bad = [c for c in cols if any(v % 8 for v in c)]
                if bad:
                    problems.append(f"{m:03X} layer {l}: off-grid colors {bad[:3]}")
    return problems


def write(sheet, frames):
    """Write porytiles_src. frames: {anim: [frame arrays]} (key first)."""
    problems = validate(sheet)
    if problems:
        raise SystemExit("aethos: invalid sheet:\n  " + "\n  ".join(problems[:40]))
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "anim").mkdir(parents=True)
    for l, n in enumerate(("bottom", "middle", "top")):
        to_png(sheet.L[l], OUT / f"{n}.png")
    shutil.copy(BASE / "attributes.csv", OUT / "attributes.csv")
    shutil.copy(BASE / "anim/anim.json", OUT / "anim/anim.json")
    for name in ANIMS:
        d = OUT / "anim" / name
        d.mkdir()
        key, *rest = frames[name]
        to_png(key, d / "key.png")
        for fn, f in zip(anim_frame_names(name), rest):
            to_png(f, d / f"{fn}.png")
