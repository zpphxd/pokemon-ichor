#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Westsea, Route 33's sea secondary.

The same pipeline as akti_build.py (read it first), with westsea's art:
1. westsea_art.build() draws every piece; validate() checks each 8x8 tile draws
   from one palette group; near-duplicate tiles are merged (akti_build's merge).
2. The pieces are packed into the 8-wide sheet from 0x200, in build order, and
   written to data/tilesets/secondary/westsea/porytiles_src.
3. Porytiles compiles them in a scratch project against an empty stand-in
   primary, so westsea's art uses only its own tiles and palettes 6-12.
4. Every cell on borrowed ground gets aethos's grass (0x001), sand (0x124) or
   animated sea (0x170) as its bottom layer.
5. verify() checks every entry and the 504-tile limit (door animations own
   504-511); catalog.json goes to build/westsea/ for tools/ichor/maps/westsea.py,
   and the sheet and piece previews to design/postgame/img/.

Usage: /usr/bin/python3 tools/ichor/art/westsea_build.py [--no-compile] [--preview out.png]
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
import akti_build as AB  # noqa: E402  (merge_near_duplicates, _tiles)
import akti_lib  # noqa: E402
from akti_lib import GROUND_METATILE, ROOT  # noqa: E402
from kalliste_lib import pack, write_sources  # noqa: E402

SRC = ROOT / "data/tilesets/secondary/westsea/porytiles_src"
BIN = ROOT / "data/tilesets/secondary/westsea/porytiles_bin"
CFG = ROOT / "porytiles/tilesets/gTileset_Westsea"
SCRATCH = ROOT / "build/westsea_porytiles"
OUT = ROOT / "build/westsea"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
IMG = ROOT / "design/postgame/img"
SHEET = IMG / "westsea_sheet.png"
PIECES = IMG / "westsea_pieces.png"
TILE_LIMIT = AB.TILE_LIMIT
NORMAL, COVERED, SPLIT = AB.NORMAL, AB.COVERED, AB.SPLIT


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"westsea_build: failed: {' '.join(map(str, cmd))}")
    return r


def scratch_project():
    """A minimal Porytiles project holding an empty primary and westsea's sources."""
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml"):
        dst = SCRATCH / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
        if not BIN.exists() and rel.startswith("src/data/tilesets/"):
            # the first build: Porytiles creates westsea in the scratch project, from
            # headers that don't declare it yet
            dst.write_text(dst.read_text().split("// Ichor (world-postgame): westsea")[0])
    (SCRATCH / "data/tilesets/primary").mkdir(parents=True)
    (SCRATCH / "data/tilesets/secondary").mkdir(parents=True)
    pt = AB.porytiles()
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_WestseaStub"])
    stub = SCRATCH / "data/tilesets/primary/westsea_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    from PIL import Image
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_WestseaStub"])
    sec = SCRATCH / "data/tilesets/secondary/westsea"
    if BIN.exists():
        cfg = SCRATCH / "porytiles/tilesets/gTileset_Westsea"
        cfg.mkdir(parents=True)
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            if (CFG / f).exists():
                shutil.copy2(CFG / f, cfg / f)
        shutil.copytree(BIN, sec / "porytiles_bin")
    else:
        cfg = SCRATCH / "porytiles/tilesets/gTileset_Westsea"
        cfg.mkdir(parents=True)
        (cfg / "config.yaml").write_text(
            "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_WestseaStub]\n")
        (SCRATCH / "data/layouts").mkdir(parents=True, exist_ok=True)
        (SCRATCH / "data/layouts/layouts.json").write_text(
            '{"layouts_table_label": "gMapLayouts", "layouts": []}\n')
        run([pt, "create-tileset", "--secondary", "-C", str(SCRATCH), "gTileset_Westsea"])
        shutil.rmtree(sec / "porytiles_src")
        cfg = SCRATCH / "porytiles/tilesets/gTileset_Westsea"
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_WestseaStub]\n")
    shutil.copytree(SRC, sec / "porytiles_src")
    return sec


def compile_tileset():
    sec = scratch_project()
    r = run([AB.porytiles(), "compile-tileset", "-C", str(SCRATCH), "--no-verify-checksums",
             "gTileset_Westsea"])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if BIN.exists():
        shutil.rmtree(BIN)
    shutil.copytree(sec / "porytiles_bin", BIN)
    CFG.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        src = SCRATCH / "porytiles/tilesets/gTileset_Westsea" / f
        if src.exists():
            shutil.copy2(src, CFG / f)
    (CFG / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n")


def borrow_ground(structs):
    """akti_build.borrow_ground, on westsea's binaries."""
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
        sys.exit(f"westsea_build: entries outside westsea's tiles/palettes 6-12: {bad[:10]}")
    from PIL import Image
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{len(patched)} cells on aethos ground")
    if used > TILE_LIMIT:
        sys.exit(f"westsea_build: {used} tiles; the door animations overwrite tiles {TILE_LIMIT}-511")
    return used


def catalog(structs):
    data = []
    for s in structs:
        data.append({
            "key": s.key, "title": s.title, "section": "westsea", "w": s.w, "h": s.h,
            "ids": s.ids, "walk": s.walk, "notes": s.notes,
            "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
            "ground": {f"{x},{y}": g for (x, y), g in getattr(s, "ground", {}).items()},
        })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps(data, indent=1))


def images(structs):
    IMG.mkdir(parents=True, exist_ok=True)
    akti_lib.preview(structs, scale=2, cols=6).save(PIECES)
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", "westsea",
         "--primary", "aethos", "--scale", "2", "-o", str(SHEET)])
    print(SHEET)
    print(PIECES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every piece here")
    args = ap.parse_args()

    import westsea_art
    structs = westsea_art.build()
    keys = [s.key for s in structs]
    assert len(keys) == len(set(keys)), "duplicate piece keys"
    probs = westsea_art.validate(structs)
    if not probs:
        before = len(AB._tiles(structs))
        merges = AB.merge_near_duplicates(structs)
        print(f"merged {len(merges)} near-duplicate tiles: {before} -> {len(AB._tiles(structs))} tiles")
        probs = westsea_art.validate(structs)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        akti_lib.preview(structs, scale=2, cols=6).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack([(0, structs)])
    assert rows <= 64, f"{rows} sheet rows: more than 512 metatiles"
    write_sources(structs, rows, SRC)
    catalog(structs)
    if not args.no_compile:
        compile_tileset()
        patched = borrow_ground(structs)
        verify(rows, patched)
        images(structs)


if __name__ == "__main__":
    main()
