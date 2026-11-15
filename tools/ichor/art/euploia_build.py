#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Euploia, the Euploia refitted.

1. Draws the scenes (euploia_deck.draw(), euploia_below.draw() and its
   variants: the hearth cold, each keepsake on the trophy shelf) and checks
   each 8x8 tile draws from one of the ship's seven palette groups
   (euploia_lib.GROUPS). Tiles within NEAR_DUPLICATE_PX pixels of another are
   redrawn as that one, so they're stored once.
2. Slices every scene into 16x16 cells and keeps one metatile per distinct
   cell (pixels, behavior and ground). Open sea with nothing on it is
   aethos's own 0x170 and costs nothing. Ids run from 0x200: the deck first,
   then below deck, then the cells only the variants use, then the void.
3. Writes data/tilesets/secondary/euploia/porytiles_src and compiles it with
   Porytiles in a scratch project (build/euploia_porytiles) against an empty
   stand-in primary, so the ship's art uses only its own tiles and palettes
   6-12; then copies porytiles_bin and the cache back.
4. Borrows aethos's sea: every deck cell on the water gets its bottom-layer
   tiles pointed at aethos's animated sea (0x170). Rebuild after repainting
   aethos.
5. Verifies every metatile entry, fails past TILE_LIMIT (504) tiles, and
   writes build/euploia/catalog.json (read by tools/ichor/maps/euploia.py),
   the sheet and preview images, and the generated part of
   design/postgame/TILES_euploia.md.

Ported from world-act1's trireme_build.py.

Usage: /usr/bin/python3 tools/ichor/art/euploia_build.py [--no-compile]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import euploia_lib as EL  # noqa: E402
from euploia_lib import CELL, ROOT, SEA, validate  # noqa: E402

NAME = "gTileset_Euploia"
SRC = ROOT / "data/tilesets/secondary/euploia/porytiles_src"
BIN = ROOT / "data/tilesets/secondary/euploia/porytiles_bin"
CFG = ROOT / "porytiles/tilesets" / NAME
SCRATCH = ROOT / "build/euploia_porytiles"
OUT = ROOT / "build/euploia"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
IMG = ROOT / "design/postgame/img"
TILE_LIMIT = 504
NEAR_DUPLICATE_PX = 7
COLS = 8


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"euploia_build: failed: {' '.join(map(str, cmd))}")
    return r


# --------------------------------------------------------------------------
# Near-duplicate tiles (as trireme_build)
# --------------------------------------------------------------------------

def _flips(t):
    return (t, t[:, ::-1], t[::-1, :], t[::-1, ::-1])


def _tiles(scenes):
    occ = {}
    for s in scenes:
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and s.ground.get((tx // 2, ty // 2)) == "sea":
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    occ.setdefault(min(v.tobytes() for v in _flips(t)), []).append((layer, tx, ty))
    return occ


def merge_near_duplicates(scenes, limit=NEAR_DUPLICATE_PX, protect=()):
    """`protect` is a list of (layer, tx, ty): tiles that never merge with
    another, either way (the hearth's, whose tiles the fire animation owns)."""
    occ = _tiles(scenes)
    guarded = {k for k, places in occ.items()
               if any(any(layer is pl and (tx, ty) == (px, py) for (pl, px, py) in protect)
                      for (layer, tx, ty) in places)}
    occ = {k: v for k, v in occ.items() if k not in guarded}
    keys = list(occ)
    if not keys:
        return []
    arr = {k: np.frombuffer(k, np.uint8).reshape(8, 8, 4) for k in keys}
    flat = np.stack([arr[k].reshape(64, 4) for k in keys])
    pairs = []
    for i, k in enumerate(keys):
        best = None
        for v in _flips(arr[k]):
            d = (flat != v.reshape(1, 64, 4)).any(-1).sum(-1)
            best = d if best is None else np.minimum(best, d)
        for j in np.nonzero(best <= limit)[0]:
            if j > i:
                pairs.append((int(best[j]), i, int(j)))
    pairs.sort()
    dropped, kept, merges = set(), set(), []
    for d, i, j in pairs:
        a, b = keys[i], keys[j]
        if a in dropped or b in dropped:
            continue
        keep, drop = (a, b) if len(occ[a]) >= len(occ[b]) else (b, a)
        if drop in kept:
            keep, drop = drop, keep
            if drop in kept:
                continue
        for (layer, tx, ty) in occ[drop]:
            cur = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = min(
                _flips(arr[keep]), key=lambda v: int((cur != v).any(-1).sum()))
        dropped.add(drop)
        kept.add(keep)
        merges.append(d)
    return merges


# --------------------------------------------------------------------------
# Cells to metatiles
# --------------------------------------------------------------------------

def cell_key(s, x, y):
    parts = [s.cell(n, x, y).tobytes() for n in ("bottom", "middle", "top")]
    return (tuple(parts), s.beh.get((x, y), "MB_NORMAL"), s.ground.get((x, y)))


def is_open_sea(s, x, y):
    if s.ground.get((x, y)) != "sea" or (x, y) in s.beh:
        return False
    return not any((s.cell(n, x, y)[..., 3] > 0).any() for n in ("bottom", "middle", "top"))


class Packer:
    """Assigns one metatile per distinct cell, in first-seen order."""

    def __init__(self):
        self.ids = {}         # key -> metatile id
        self.cells = []       # (scene, x, y) of each metatile's first cell

    def id_for(self, s, x, y):
        if is_open_sea(s, x, y):
            return SEA
        k = cell_key(s, x, y)
        if k not in self.ids:
            self.ids[k] = 0x200 + len(self.cells)
            self.cells.append((s, x, y))
        return self.ids[k]

    def grid(self, s):
        return [[self.id_for(s, x, y) for x in range(s.w)] for y in range(s.h)]


def write_sources(packer, outdir):
    from PIL import Image
    outdir.mkdir(parents=True, exist_ok=True)
    n = len(packer.cells)
    rows = (n + COLS - 1) // COLS
    for ln in ("bottom", "middle", "top"):
        sheet = np.zeros((rows * CELL, COLS * CELL, 4), np.uint8)
        for i, (s, x, y) in enumerate(packer.cells):
            sx, sy = (i % COLS) * CELL, (i // COLS) * CELL
            sheet[sy:sy + CELL, sx:sx + CELL] = s.cell(ln, x, y)
        Image.fromarray(sheet, "RGBA").save(outdir / f"{ln}.png")
    lines = ["id,behavior"]
    for i, (s, x, y) in enumerate(packer.cells):
        b = s.beh.get((x, y))
        if b:
            lines.append(f"{i},{b}")
    (outdir / "attributes.csv").write_text("\n".join(lines) + "\n")
    return rows


# --------------------------------------------------------------------------
# Porytiles
# --------------------------------------------------------------------------

def scratch_project():
    from PIL import Image
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml"):
        dst = SCRATCH / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    (SCRATCH / "data/tilesets/primary").mkdir(parents=True)
    (SCRATCH / "data/tilesets/secondary").mkdir(parents=True)
    pt = porytiles()
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_EuploiaStub"])
    stub = SCRATCH / "data/tilesets/primary/euploia_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_EuploiaStub"])
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    cfg.mkdir(parents=True)
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_EuploiaStub]\n")
    sec = SCRATCH / "data/tilesets/secondary/euploia"
    if (CFG / "tileset-manifest.json").exists() and BIN.exists():
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            shutil.copy2(CFG / f, cfg / f)
        shutil.copytree(BIN, sec / "porytiles_bin")
    else:
        # first build: Porytiles creates the tileset (the real headers are kept by hand)
        run([pt, "create-tileset", "-C", str(SCRATCH), "--secondary", NAME])
        shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(SRC, sec / "porytiles_src")
    return sec


def compile_tileset():
    sec = scratch_project()
    r = run([porytiles(), "compile-tileset", "-C", str(SCRATCH), "--no-verify-checksums", NAME])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if BIN.exists():
        shutil.rmtree(BIN)
    shutil.copytree(sec / "porytiles_bin", BIN)
    CFG.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        shutil.copy2(SCRATCH / "porytiles/tilesets" / NAME / f, CFG / f)
    cfg = CFG / "config.yaml"
    if not cfg.exists():
        cfg.write_text(
            "# Per-tileset Porytiles config for gTileset_Euploia, the Euploia refitted (deck and\n"
            "# below deck). Sources are drawn by tools/ichor/art/euploia_build.py, which\n"
            "# compiles the ship against an empty stand-in primary, checks its metatiles use\n"
            "# only its own tiles and palettes 6-12, then points its sea cells at aethos's sea.\n"
            "# Pair it with aethos when compiling it directly.\n"
            "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n")


NORMAL, COVERED, SPLIT = 0, 1, 2


def borrow_sea(packer):
    """Point each sea cell's bottom layer at aethos's sea (0x170) under its art."""
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    meta = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(BIN / "metatile_attributes.bin", "<u2")
    patched = set()
    for i, (s, x, y) in enumerate(packer.cells):
        if s.ground.get((x, y)) != "sea":
            continue
        on_top = bool((s.cell("top", x, y)[..., 3] > 0).any())
        lt = int(attrs[i]) >> 12
        ent = [int(e) for e in meta[i]]
        art = ent[4:8] if any(ent[4:8]) else ent[0:4]
        if on_top and lt == NORMAL:
            art = ent[4:8]
        meta[i, 0:4] = aethos[SEA, 0:4]
        meta[i, 4:8] = art
        attrs[i] = (int(attrs[i]) & 0x0FFF) | ((SPLIT if on_top else COVERED) << 12)
        patched.add(i)
    meta.astype("<u2").tofile(BIN / "metatiles.bin")
    attrs.astype("<u2").tofile(BIN / "metatile_attributes.bin")
    return patched


def verify(n, patched):
    from PIL import Image
    raw = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    assert len(raw) >= n, (len(raw), n)
    bad = []
    for i, entries in enumerate(raw[:n]):
        for j, e in enumerate(entries):
            e = int(e)
            if i in patched and j < 4:
                if e != int(aethos[SEA, j]):
                    bad.append((0x200 + i, j, "sea"))
                continue
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                continue
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"euploia_build: entries outside the ship's tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    print(f"verified {n} metatiles; {used} of {TILE_LIMIT} tiles used; {len(patched)} on aethos sea")
    if used > TILE_LIMIT:
        sys.exit(f"euploia_build: {used} tiles; the door animations own tiles {TILE_LIMIT}-511")
    return used


# --------------------------------------------------------------------------
# Catalog
# --------------------------------------------------------------------------

def catalog(packer, deck, below, variants, void):
    base_d, base_b = packer.grid(deck), packer.grid(below)
    data = {
        "scenes": {
            "deck": {"w": deck.w, "h": deck.h, "ids": base_d, "walk": ["".join(r) for r in deck.walk]},
            "below": {"w": below.w, "h": below.h, "ids": base_b, "walk": ["".join(r) for r in below.walk]},
        },
        "variants": {},
        "pieces": [],
        "metatiles": len(packer.cells),
    }
    for name, s in variants.items():
        g = packer.grid(s)
        data["variants"][name] = [[x, y, g[y][x]] for y in range(below.h) for x in range(below.w)
                                  if g[y][x] != base_b[y][x]]
    data["void"] = packer.grid(void)[0][0]
    for scene_key, s, grid in (("deck", deck, base_d), ("below", below, base_b),
                               ("void", void, packer.grid(void))):
        for p in s.pieces:
            ids = [[grid[p["y"] + j][p["x"] + i] for i in range(p["w"])] for j in range(p["h"])]
            walk = ["".join(s.walk[p["y"] + j][p["x"] + i] for i in range(p["w"])) for j in range(p["h"])]
            data["pieces"].append(dict(p, scene=scene_key, ids=ids, walk=walk))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps(data, indent=1))
    return data


# --------------------------------------------------------------------------
# Hestia's fire: the hearth's flames as tile-animation frames
# --------------------------------------------------------------------------

FIRE_FRAMES = 4
ANIM_H = ROOT / "src/data/tilesets/euploia_anim.h"


def read_pal(i):
    lines = (BIN / "palettes" / f"{i:02d}.pal").read_text().split("\n")[3:19]
    return [tuple(int(v) for v in ln.split()) for ln in lines]


def encode_tile(px, pal):
    """An 8x8 RGBA tile as 16 little-endian u16 words of 4bpp, by `pal`."""
    out = bytearray()
    for row in px:
        nib = []
        for p in row:
            if p[3] == 0:
                nib.append(0)
            else:
                rgb = tuple(int(v) for v in p[:3])
                if rgb not in pal[1:]:
                    sys.exit(f"euploia_build: fire color {rgb} isn't in its tile's palette")
                nib.append(pal.index(rgb, 1))
        for k in range(0, 8, 2):
            out.append(nib[k] | (nib[k + 1] << 4))
    return [out[k] | (out[k + 1] << 8) for k in range(0, 32, 2)]


def fire_frames(packer, below):
    """Find the hearth's flame tiles in the compiled tileset (the tiles that
    change between the flames' phases) and write each phase as a frame for
    src/tileset_anims.c (src/data/tilesets/euploia_anim.h)."""
    import euploia_below as EBm
    meta = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(BIN / "metatile_attributes.bin", "<u2")
    grid = packer.grid(below)
    phases = [below] + [EBm.draw("base", phase=p) for p in range(1, FIRE_FRAMES)]
    fresh = EBm.draw("base", phase=0)          # unmerged, to compare the phases like for like
    hx, hy = EBm.HEARTH
    tiles = {}                                  # tile -> (pal, hflip, vflip, layer, x, y)
    for cy in (hy - 1, hy):
        for cx in (hx, hx + 1):
            i = grid[cy][cx] - 0x200
            for li, ln in enumerate(("bottom", "middle")):
                for q in range(4):
                    x0, y0 = cx * CELL + (q % 2) * 8, cy * CELL + (q // 2) * 8
                    ref = fresh.layers[ln].a[y0:y0 + 8, x0:x0 + 8]
                    if all((p.layers[ln].a[y0:y0 + 8, x0:x0 + 8] == ref).all() for p in phases[1:]):
                        continue
                    if li == 1:
                        assert int(attrs[i]) >> 12 == COVERED, "the hearth's flames should be on its middle layer"
                    e = int(meta[i][li * 4 + q])
                    tiles.setdefault(e & 0x3FF, (e >> 12, e & 0x400, e & 0x800, ln, x0, y0))
    # the flame tiles must be the lit hearth's alone, or the fire would flicker elsewhere
    hearth = {grid[cy][cx] - 0x200 for cy in (hy - 1, hy) for cx in (hx, hx + 1)}
    for i, entries in enumerate(meta[:len(packer.cells)]):
        if i not in hearth and any(int(e) & 0x3FF in tiles for e in entries):
            sys.exit(f"euploia_build: metatile 0x{0x200 + i:03X} shares a flame tile with the hearth")
    frames = []
    for p in phases:
        words = []
        for t, (pal, hf, vf, ln, x0, y0) in tiles.items():
            px = p.layers[ln].a[y0:y0 + 8, x0:x0 + 8]
            if hf:
                px = px[:, ::-1]
            if vf:
                px = px[::-1]
            words += encode_tile(px, read_pal(pal))
        frames.append(words)
    lines = [
        "// Generated by tools/ichor/art/euploia_build.py: Hestia's fire on the Euploia's",
        "// hearth, below deck (euploia_below.py's FLAMES). src/tileset_anims.c copies each",
        "// frame over the flame tiles below. Rebuild the tileset and this file together.",
        f"#define EUPLOIA_FIRE_FRAMES {FIRE_FRAMES}",
        f"#define EUPLOIA_FIRE_TILES {len(tiles)}",
        "",
        "// the flame tiles, as BG tile numbers (the secondary's start at 512)",
        "static const u16 sEuploiaFireTiles[EUPLOIA_FIRE_TILES] = {"
        + ", ".join(str(t) for t in tiles) + "};",
        "",
        "static const u16 sEuploiaFireFrames[EUPLOIA_FIRE_FRAMES][EUPLOIA_FIRE_TILES * 16] = {",
    ]
    for words in frames:
        lines.append("    {")
        for k in range(0, len(words), 8):
            lines.append("        " + ", ".join(f"0x{w:04X}" for w in words[k:k + 8]) + ",")
        lines.append("    },")
    lines.append("};")
    ANIM_H.write_text("\n".join(lines) + "\n")
    print(f"hearth fire: {len(tiles)} tiles animated, {FIRE_FRAMES} frames")


def images():
    IMG.mkdir(parents=True, exist_ok=True)
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", "euploia",
         "--primary", "aethos", "--scale", "2", "-o", str(IMG / "euploia_sheet.png")])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    import euploia_below
    import euploia_deck
    deck = euploia_deck.draw()
    below = euploia_below.draw()
    variants = {v: euploia_below.draw(v) for v in euploia_below.VARIANTS}
    void = euploia_below.void()
    scenes = [deck, below] + list(variants.values()) + [void]
    probs = [p for s in scenes for p in validate(s)]
    if not probs:
        before = len(_tiles(scenes))
        hx, hy = euploia_below.HEARTH
        flames = [(below.M, tx, ty) for tx in range(hx * 2, hx * 2 + 4) for ty in range(hy * 2 - 2, hy * 2 + 2)]
        merges = merge_near_duplicates(scenes, protect=flames)
        print(f"merged {len(merges)} near-duplicate tiles: {before} -> {len(_tiles(scenes))} tiles")
        probs = [p for s in scenes for p in validate(s)]
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    packer = Packer()
    packer.grid(deck)
    packer.grid(below)
    for s in variants.values():
        packer.grid(s)
    packer.grid(void)
    n = len(packer.cells)
    print(f"{n} metatiles ({n * 100 // 512}% of the secondary's 512)")
    assert n <= 512
    write_sources(packer, SRC)
    OUT.mkdir(parents=True, exist_ok=True)
    for s in (deck, below):
        EL.save_preview(s, OUT / f"{s.key}_preview.png", scale=2)
    if args.no_compile:
        catalog(packer, deck, below, variants, void)
        return
    compile_tileset()
    patched = borrow_sea(packer)
    used = verify(n, patched)
    fire_frames(packer, below)
    data = catalog(packer, deck, below, variants, void)
    images()
    import euploia_catalog
    euploia_catalog.write(data, used)


if __name__ == "__main__":
    main()
