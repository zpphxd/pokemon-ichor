"""aethos's Porymap assets: locked palettes and tiles pinned where Hoenn
secondaries expect them.

Hoenn secondaries reach into the primary by raw tile number and palette
slot. The slice maps still pair with Petalburg, so aethos keeps every tile
index and palette slot Petalburg uses (COMPAT), each holding the aethos
version of what General had there: grass stays grass, the tree's trunk
quarter is the olive's, the ledge lip is the terrace lip. The animations sit
at General's tile offsets too.

How the build gets that from Porytiles (porytiles/tilesets/gTileset_Aethos/
config.yaml sets tiles to patch and palettes to locked):
  1. PALETTES below are written as the six primary palettes. Porytiles never
     changes them; every tile of the art must fit one of them.
  2. tiles.png is seeded with the pinned tiles and the animation key frames.
  3. compile-tileset in patch mode keeps those slots and fills the empty ones
     with the rest of the art, reusing a pinned tile wherever the art matches.
  4. verify() checks the pins survived and that a compile with checksum
     verification on (what kalliste's pairing runs) changes nothing.
"""
import json
import re
import subprocess

import numpy as np
from PIL import Image

from aethos_lib import (PAL, ROOT, BASE, PORYTILES, flip, quad, split_tiles,
                        load_rgba)

BIN = ROOT / "data/tilesets/primary/aethos/porytiles_bin"
GENERAL = ROOT / "data/tilesets/primary/general"
CONFIG = ROOT / "porytiles/tilesets/gTileset_Aethos/config.yaml"
BACKDROP = (24, 40, 80)   # palette 0 color 0: the BG backdrop, a night-sea navy
COMPAT = ["gTileset_Petalburg"]
ANIM_OFFSETS = {"water": 432, "sand_water_edge": 464, "land_water_edge": 480,
                "waterfall": 496, "flower": 508}

# Six primary palettes. Slot 0 is transparent (palette 0's is the backdrop).
# Pinned for Petalburg's own tiles: palette 2 slots 2-4 and 14-15 (General's
# leaf and grass greens), palette 5 slots 11-13 (General's sand ramp).
# Palettes 0 and 1 share their marble slots, because General drew a few roof
# tiles in both and Petalburg reuses them that way.
PALETTES = [
    # 0 marble: buildings
    [None, "mb_d", "mb_m", "mb_l", "mb_h", "ink", "tc_d", "tc_m", "tc_l",
     "sg_d", "sg_l", "ae_m", "ae_l", "lp_d", "lp_l", "ae_d"],
    # 1 plaza: marble and clay on grass
    [None, "mb_d", "mb_m", "mb_l", "mb_h", "ink", "gr_d", "gr_m", "gr_l",
     "gm", "tc_m", "tc_l", "sg_l", "ae_m", "ae_l", "lp_l"],
    # 2 grove: olives, cypresses, pines, trunks, grass
    [None, "ol_s", "ol_l", "gm", "gd", "cy_d", "cy_m", "cy_l", "gr_m", "gr_l",
     "ink", "tr_d", "mb_d", "mb_m", "gr_d", "gk"],
    # 3 earth: limestone, ledges, cliffs, paths, soil, grass
    [None, "gr_d", "gr_m", "gr_l", "gm", "lp_k", "lp_d", "lp_m", "lp_l", "lp_h",
     "dt_d", "dt_m", "sd_d", "sd_m", "ink", "tr_d"],
    # 4 meadow: wild tall grass, anemones
    [None, "gk", "gd", "gm", "tg_l", "gr_d", "gr_m", "gr_l", "lp_l", "sg_d",
     "sg_l", "fl_d", "fl_m", "fl_l", "ink", "lp_h"],
    # 5 sea: the Aegean, surf, sea stacks, sand
    [None, "ae_d", "ae_m", "ae_n", "ae_l", "ae_h", "ae_t", "mb_h", "mb_d",
     "mb_m", "mb_l", "lp_h", "sd_m", "sd_d", "ink", "lp_d"],
]
PINNED_SLOTS = {(2, 2): (131, 197, 98), (2, 3): (57, 139, 49), (2, 4): (57, 82, 0),
                (2, 14): (65, 180, 131), (2, 15): (24, 164, 106),
                (5, 11): (238, 230, 164), (5, 12): (222, 205, 131), (5, 13): (213, 180, 106)}


def palette_rgb(p):
    return [BACKDROP] + [PAL[n] for n in PALETTES[p][1:]]


PAL_SETS = [set(palette_rgb(p)[1:]) for p in range(6)]


def colors(t):
    return {tuple(int(v) for v in c) for c in t[t[..., 3] > 0][:, :3]}


def fitting(t):
    c = colors(t)
    return [p for p in range(6) if c <= PAL_SETS[p]]


def fit_tile(t):
    """Snap a tile's colors onto the palette that fits it best (nearest
    color). The terrain pass uses this as a safety net for General's mixed
    material tiles; hand-drawn art is checked, never snapped."""
    if fitting(t):
        return t
    cs = colors(t)
    best = None
    for p in range(6):
        rgb = palette_rgb(p)[1:]
        mapping, cost = {}, 0
        for c in cs:
            n = min(rgb, key=lambda r: sum((a - b) ** 2 for a, b in zip(r, c)))
            mapping[c] = n
            cost += sum((a - b) ** 2 for a, b in zip(n, c))
        if best is None or cost < best[0]:
            best = (cost, mapping)
    out = t.copy()
    for y in range(t.shape[0]):
        for x in range(t.shape[1]):
            if t[y, x, 3]:
                out[y, x, :3] = best[1][tuple(int(v) for v in t[y, x, :3])]
    return out


def encode(t, p):
    rgb = palette_rgb(p)
    out = np.zeros((8, 8), np.uint8)
    for y in range(8):
        for x in range(8):
            if t[y, x, 3]:
                out[y, x] = rgb.index(tuple(int(v) for v in t[y, x, :3]), 1)
    return out


def check_fit(sheet, frames):
    """Every art tile (and every anim tile over all frames) must fit a palette."""
    bad = []
    for m in range(512):
        for l in sheet.used(m):
            for q in range(4):
                t = quad(sheet.view(m, l), q)
                if t[..., 3].any() and not fitting(t):
                    bad.append(f"{m:03X} layer {l} q{q}: {sorted(name_of(c) for c in colors(t))}")
    for name, fr in frames.items():
        for i, c in enumerate(anim_colorsets(fr)):
            if not [p for p in range(6) if c <= PAL_SETS[p]]:
                bad.append(f"anim {name} tile {i}: {sorted(name_of(x) for x in c)}")
    return bad


def name_of(c):
    from aethos_lib import ALIASES
    for k, v in PAL.items():
        if v == c and k not in ALIASES:
            return k
    return str(c)


def anim_colorsets(frames):
    tiles = [split_tiles(f) for f in frames]
    out = []
    for i in range(len(tiles[0])):
        c = set()
        for f in tiles:
            c |= colors(f[i])
        out.append(c)
    return out


# --------------------------------------------------------------------------
# Pins
# --------------------------------------------------------------------------

def _tileset_bins():
    headers = (ROOT / "src/data/tilesets/headers.h").read_text()
    metas = dict(re.findall(r'(gMetatiles_\w+)\[\]\s*=\s*INCBIN_U16\("([^"]+)"',
                            (ROOT / "src/data/tilesets/metatiles.h").read_text()))
    out = {}
    for name, body in re.findall(r'const struct Tileset (gTileset_\w+)\s*=\s*\{(.*?)\};', headers, re.S):
        f = dict(re.findall(r'\.(\w+)\s*=\s*(\w+)', body))
        if f.get("metatiles") in metas:
            out[name] = ROOT / metas[f["metatiles"]]
    return out


def compat_refs():
    """{primary tile: Counter of palettes} over the COMPAT secondaries."""
    from collections import Counter, defaultdict
    bins = _tileset_bins()
    refs = defaultdict(Counter)
    for s in COMPAT:
        for e in np.fromfile(bins[s], "<u2").tolist():
            t = e & 0x3FF
            if 0 < t < 512:
                refs[t][e >> 12] += 1
    return refs


def _general_layer_of(base, m, k):
    """Which of our three layers General's metatile entry k drew on."""
    used = set(base.layers(m))
    if 0 in used and 2 in used:          # split
        return 0 if k < 4 else 2
    if 0 in used:                        # covered
        return 0 if k < 4 else 1
    return 1 if k < 4 else 2             # normal


def _general_tile_rgba(t, p):
    idx = np.array(Image.open(GENERAL / "tiles.png")) % 16
    tile = idx[(t // 16) * 8:(t // 16) * 8 + 8, (t % 16) * 8:(t % 16) * 8 + 8]
    vals = [int(v) for v in (GENERAL / f"palettes/{p:02d}.pal").read_text().split()[3:51]]
    pal = [tuple(vals[i:i + 3]) for i in range(0, 48, 3)]
    out = np.zeros((8, 8, 4), np.uint8)
    for y in range(8):
        for x in range(8):
            if tile[y, x]:
                out[y, x] = pal[tile[y, x]] + (255,)
    return out


def _quantize(t, p):
    rgb = palette_rgb(p)[1:]
    out = t.copy()
    for y in range(8):
        for x in range(8):
            if t[y, x, 3]:
                c = np.array(t[y, x, :3], int)
                out[y, x, :3] = min(rgb, key=lambda r: ((np.array(r) - c) ** 2).sum())
    return out


def pins(sheet, base):
    """{tile index: (8x8 RGBA in aethos art, palette)} for every tile a COMPAT
    secondary references."""
    from aethos_terrain import render_tile
    gen = np.fromfile(GENERAL / "metatiles.bin", "<u2").reshape(-1, 8)
    out = {}
    for t, pals in compat_refs().items():
        p = pals.most_common(1)[0][0]
        if p > 5:
            p = 2
        best = None
        for m in range(512):
            for k in range(8):
                e = int(gen[m, k])
                if e & 0x3FF != t:
                    continue
                l = _general_layer_of(base, m, k)
                c = quad(sheet.view(m, l), k % 4)
                c = flip(c, e >> 10 & 1, e >> 11 & 1)
                if c[..., 3].any() and p in fitting(c):
                    best = c
                    break
            if best is not None:
                break
        if best is None:  # no fitting art: General's tile, in aethos colors
            g = _general_tile_rgba(t, p)
            best = _quantize(render_tile(g), p)
        out[t] = (best, p)
    return out


# --------------------------------------------------------------------------
# Writing, compiling, verifying
# --------------------------------------------------------------------------

def write_pal(path, rgb):
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in rgb]
    path.write_bytes(("\r\n".join(lines) + "\r\n").encode())


def write_config():
    CONFIG.write_text(
        "# aethos is regenerated by tools/ichor/art/paint_aethos.py. Hoenn\n"
        "# secondaries point at its tiles by index and its palettes by slot, so\n"
        "# tiles are only ever patched into empty slots and palettes are locked\n"
        "# (see tools/ichor/art/aethos_bin.py and design/phase1/TILES_aethos.md).\n"
        "tileset:\n"
        "  palettes:\n"
        "    edit_mode: locked\n"
        "  tiles:\n"
        "    edit_mode: patch\n")


def seed(pinned, frames):
    """Write locked palettes and a tiles.png holding only the pinned tiles and
    the animation key frames."""
    (BIN / "palettes").mkdir(parents=True, exist_ok=True)
    for p in range(16):
        rgb = palette_rgb(p) if p < 6 else [BACKDROP] + [(0, 0, 0)] * 15
        write_pal(BIN / f"palettes/{p:02d}.pal", rgb)
    idx = np.zeros((512, 8, 8), np.uint8)
    for t, (c, p) in pinned.items():
        idx[t] = encode(c, p) + 16 * p   # Porytiles tags even color 0
    anim_pal = {}
    for name, fr in frames.items():
        sets = anim_colorsets(fr)
        keys = split_tiles(fr[0])
        for i, (k, c) in enumerate(zip(keys, sets)):
            p = next(p for p in range(6) if c <= PAL_SETS[p])
            idx[ANIM_OFFSETS[name] + i] = encode(k, p) + 16 * p
            anim_pal[(name, i)] = p
    img = idx.reshape(32, 16, 8, 8).swapaxes(1, 2).reshape(256, 128)
    im = Image.fromarray(img, "P")
    flat = []
    for p in range(6):
        for c in palette_rgb(p):
            flat.extend(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.save(BIN / "tiles.png")
    return anim_pal


def porytiles(*args):
    r = subprocess.run([str(PORYTILES), *args], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-6000:], r.stderr[-3000:])
        raise SystemExit(f"aethos: porytiles {' '.join(args)} failed")
    return r


def snapshot():
    snap = {"tiles": np.array(Image.open(BIN / "tiles.png")).tobytes()}
    for name in ("metatiles.bin", "metatile_attributes.bin"):
        snap[name] = (BIN / name).read_bytes()
    for p in range(16):
        snap[f"pal{p}"] = (BIN / f"palettes/{p:02d}.pal").read_bytes()
    for f in sorted((BIN / "anim").rglob("*.png")):
        snap[str(f)] = np.array(Image.open(f)).tobytes()
    return snap


def bin_tile(t):
    a = np.array(Image.open(BIN / "tiles.png"))
    y, x = divmod(t, 16)
    return a[y * 8:y * 8 + 8, x * 8:x * 8 + 8]


def build(sheet, base, frames):
    write_config()
    pinned = pins(sheet, base)
    seed(pinned, frames)
    porytiles("compile-tileset", "--no-verify-checksums", "gTileset_Aethos")
    # the pins must survive
    moved = []
    for t, (c, p) in pinned.items():
        got = bin_tile(t)
        e = encode(c, p)
        # the game reads value % 16; opaque pixels must also keep the palette
        if not ((got % 16 == e).all() and (got[e > 0] // 16 == p).all()):
            moved.append(t)
    if moved:
        raise SystemExit(f"aethos: Porytiles moved pinned tiles {moved}")
    # a verified recompile (as kalliste's pairing runs it) must change nothing
    before = snapshot()
    porytiles("compile-tileset", "gTileset_Aethos")
    after = snapshot()
    changed = [k for k in before if before[k] != after.get(k)]
    if changed:
        raise SystemExit(f"aethos: a verified recompile changed {changed[:5]}")
    return pinned
