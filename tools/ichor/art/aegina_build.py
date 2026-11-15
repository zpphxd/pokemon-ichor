#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Aegina, the island secondary for Aegina
Town and the Aegina detour. It follows akti_build.py step for step:

1. Draws every structure (aegina_art.build()) and checks each 8x8 tile draws from
   one of Aegina's seven palette groups (aegina_lib.GROUPS). Tiles within
   NEAR_DUPLICATE_PX pixels of another are redrawn as that one, so they're
   stored once.
2. Packs them into the 8-wide metatile sheet from 0x200, in build order.
3. Writes data/tilesets/secondary/aegina/porytiles_src (bottom/middle/top.png,
   attributes.csv).
4. Compiles with Porytiles in a scratch project (build/aegina_porytiles) against
   an empty stand-in primary, so Aegina's own art uses only its own tiles and
   palettes 6-12, then copies porytiles_bin and the cache back. The first run
   creates porytiles/tilesets/gTileset_Aegina.
5. Borrows aethos's ground: every cell drawn on grass, sand, sea or path gets its
   bottom-layer tiles pointed at aethos's grass (0x001), sand (0x124), animated
   sea (0x170) or limestone path (0x1D9). Rebuild Aegina whenever aethos is
   repainted.
6. Verifies every metatile entry and fails past TILE_LIMIT (504) tiles: the door
   animations own tiles 504-511. Writes build/aegina/catalog.json (read by
   tools/ichor/maps/aegina.py), the sheet and pieces images, and the catalog
   section of design/phase2/TILES_aegina.md.

Usage: /usr/bin/python3 tools/ichor/art/aegina_build.py [--no-compile] [--preview out.png]
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
import aegina_lib  # noqa: E402
from aegina_lib import GROUND_METATILE, ROOT, validate  # noqa: E402
from akti_build import NEAR_DUPLICATE_PX, TILE_LIMIT, _tiles, merge_near_duplicates  # noqa: E402
from kalliste_lib import pack, write_sources  # noqa: E402

NAME = "gTileset_Aegina"
SRC = ROOT / "data/tilesets/secondary/aegina/porytiles_src"
BIN = ROOT / "data/tilesets/secondary/aegina/porytiles_bin"
CFG = ROOT / "porytiles/tilesets" / NAME
SCRATCH = ROOT / "build/aegina_porytiles"
OUT = ROOT / "build/aegina"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
IMG = ROOT / "design/phase2/img"
SHEET = IMG / "aegina_sheet.png"
PIECES = IMG / "aegina_pieces.png"


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"aegina_build: failed: {' '.join(map(str, cmd))}")
    return r


def scratch_project():
    """A minimal Porytiles project holding an empty primary and Aegina."""
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
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_AeginaStub"])
    stub = SCRATCH / "data/tilesets/primary/aegina_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    from PIL import Image
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_AeginaStub"])
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    sec = SCRATCH / "data/tilesets/secondary/aegina"
    if (CFG / "tileset-manifest.json").exists():
        cfg.mkdir(parents=True)
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            if (CFG / f).exists():
                shutil.copy2(CFG / f, cfg / f)
        shutil.copytree(SRC, sec / "porytiles_src")
        if BIN.exists():
            shutil.copytree(BIN, sec / "porytiles_bin")
    else:
        run([pt, "create-tileset", NAME, "--secondary", "-C", str(SCRATCH),
             "--primary-pairing-mode", "manual", "--primary-pairing-partners",
             "gTileset_AeginaStub"])
        shutil.rmtree(sec / "porytiles_src")
        shutil.copytree(SRC, sec / "porytiles_src")
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_AeginaStub]\n")
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
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        shutil.copy2(cfg / f, CFG / f)
    (CFG / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n")


NORMAL, COVERED, SPLIT = 0, 1, 2   # metatile layer types (attribute bits 12-15)


def borrow_ground(structs):
    """Give each ground cell aethos's ground tiles as its bottom layer (see
    akti_build.borrow_ground): COVERED when its art is in the middle layer,
    SPLIT when it is in the top layer, drawn over the player."""
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    meta = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(BIN / "metatile_attributes.bin", "<u2")
    patched = {}
    for s in structs:
        for (cx, cy), kind in getattr(s, "ground", {}).items():
            i = s.ids[cy][cx] - 0x200
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            on_top = bool((s.T.a[sl][..., 3] > 0).any())
            lt = int(attrs[i]) >> 12
            ent = [int(e) for e in meta[i]]
            art = ent[4:8] if any(ent[4:8]) else ent[0:4]
            if on_top and lt == NORMAL:
                art = ent[4:8]
            meta[i, 0:4] = aethos[GROUND_METATILE[kind], 0:4]
            meta[i, 4:8] = art
            attrs[i] = (int(attrs[i]) & 0x0FFF) | ((SPLIT if on_top else COVERED) << 12)
            patched[i] = kind
    meta.astype("<u2").tofile(BIN / "metatiles.bin")
    attrs.astype("<u2").tofile(BIN / "metatile_attributes.bin")
    return patched


def verify(rows, patched):
    raw = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = []
    for i, entries in enumerate(raw):
        for j, e in enumerate(entries):
            e = int(e)
            if i in patched and j < 4:
                if e != int(aethos[GROUND_METATILE[patched[i]], j]):
                    bad.append((0x200 + i, j, "ground"))
                continue
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                continue
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"aegina_build: entries outside aegina's tiles/palettes 6-12: {bad[:10]}")
    from PIL import Image
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{len(patched)} cells on aethos ground")
    if used > TILE_LIMIT:
        sys.exit(f"aegina_build: {used} tiles; the door animations overwrite tiles "
                 f"{TILE_LIMIT}-511, so Aegina may use at most {TILE_LIMIT}")
    return used


def tile_counts(structs):
    """How many distinct tiles each structure adds, in build order, and which
    structures' tiles only the detour uses."""
    seen, out = set(), []
    for s in structs:
        mine = set()
        gr = getattr(s, "ground", {})
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    from akti_build import _flips
                    mine.add(min(v.tobytes() for v in _flips(t)))
        out.append((s.key, len(mine), len(mine - seen), mine))
        seen |= mine
    return out


def catalog(structs):
    data = []
    for s in structs:
        data.append({
            "key": s.key, "title": s.title, "section": "aegina", "w": s.w, "h": s.h,
            "ids": s.ids, "walk": s.walk, "notes": s.notes,
            "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
            "ground": {f"{x},{y}": g for (x, y), g in getattr(s, "ground", {}).items()},
            "skip": [f"{x},{y}" for (x, y) in sorted(getattr(s, "skip", set()))],
        })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps(data, indent=1))


def images(structs):
    IMG.mkdir(parents=True, exist_ok=True)
    aegina_lib.preview(structs, scale=2, cols=4).save(PIECES)
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", "aegina",
         "--primary", "aethos", "--scale", "2", "-o", str(SHEET)])
    print(SHEET)
    print(PIECES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()

    import aegina_art
    structs = aegina_art.build()
    keys = [s.key for s in structs]
    assert len(keys) == len(set(keys)), "duplicate structure keys"
    probs = validate(structs)
    counts = None
    if not probs:
        before = len(_tiles(structs))
        merges = merge_near_duplicates(structs, NEAR_DUPLICATE_PX)
        print(f"merged {len(merges)} near-duplicate tiles "
              f"({merges.count(1)} differed by 1 px, {merges.count(2)} by 2): "
              f"{before} -> {len(_tiles(structs))} tiles")
        probs = validate(structs)
        counts = tile_counts(structs)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        aegina_lib.preview(structs, scale=2, cols=4).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack([(0, structs)])
    assert rows <= 64, f"{rows} sheet rows: more than 512 metatiles"
    write_sources(structs, rows, SRC)
    catalog(structs)
    detour, town, only = set(), set(), set()
    for key, _, _, mine in counts:
        if key in aegina_art.DETOUR:
            detour |= mine
            if key not in aegina_art.DETOUR_SHARED:
                only |= mine
        if key not in aegina_art.DETOUR or key in aegina_art.DETOUR_SHARED:
            town |= mine
    only -= town
    print(f"{len(_tiles(structs))} tiles drawn; the detour's pieces use {len(detour)}, "
          f"{len(only)} of them the detour's alone")
    if not args.no_compile:
        compile_tileset()
        patched = borrow_ground(structs)
        used = verify(rows, patched)
        images(structs)
        import aegina_catalog
        aegina_catalog.main(used, [(k, n, new) for (k, n, new, _) in counts], len(detour), len(only))


if __name__ == "__main__":
    main()
