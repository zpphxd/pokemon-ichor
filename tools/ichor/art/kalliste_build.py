#!/usr/bin/env python3
"""Draw, compile and catalog the kalliste secondary tileset.

1. Draws every structure (kalliste_elaia, kalliste_akti, kalliste_kronion) and
   checks each 8x8 tile draws from one palette group.
2. Packs them into the 8-wide metatile sheet. Each section starts on a fixed
   row, so adding to one section never renumbers another.
3. Writes data/tilesets/secondary/kalliste/porytiles_src (bottom/middle/top.png,
   attributes.csv).
4. Compiles with Porytiles in a scratch project (build/kalliste_porytiles)
   against an empty stand-in primary, so the output uses only kalliste's own
   tiles and palettes 6-12 and keeps working whatever aethos becomes. Copies
   porytiles_bin and the cache back, then verifies every metatile entry.
5. Writes build/kalliste/catalog.json, used by kalliste_scene.py and the
   TILES_kalliste.md generator.

Usage: /usr/bin/python3 tools/ichor/art/kalliste_build.py [--no-compile] [--preview out.png]

To compile against aethos instead (Porytiles may then share aethos tiles and
palettes): porytiles compile-tileset gTileset_Kalliste, with the manual pairing
in porytiles/tilesets/gTileset_Kalliste/config.yaml.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kalliste_lib import ROOT, pack, preview, validate, write_sources  # noqa: E402

SRC = ROOT / "data/tilesets/secondary/kalliste/porytiles_src"
BIN = ROOT / "data/tilesets/secondary/kalliste/porytiles_bin"
CFG = ROOT / "porytiles/tilesets/gTileset_Kalliste"
SCRATCH = ROOT / "build/kalliste_porytiles"
OUT = ROOT / "build/kalliste"

# First metatile row of each section (8 metatiles per row; id = 0x200 + row*8 + col).
SECTION_ROWS = {"elaia": 0, "akti": 24, "kronion": 48}


def sections():
    import kalliste_elaia
    out = [("elaia", kalliste_elaia.build())]
    try:
        import kalliste_akti
        out.append(("akti", kalliste_akti.build()))
    except ImportError:
        pass
    try:
        import kalliste_kronion
        out.append(("kronion", kalliste_kronion.build()))
    except ImportError:
        pass
    return out


def porytiles():
    exe = shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")
    return exe


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"kalliste_build: failed: {' '.join(map(str, cmd))}")
    return r


def scratch_project():
    """A minimal Porytiles project holding an empty primary and a copy of kalliste."""
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
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_KallisteStub"])
    stub = SCRATCH / "data/tilesets/primary/kalliste_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    from PIL import Image
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_KallisteStub"])
    cfg = SCRATCH / "porytiles/tilesets/gTileset_Kalliste"
    cfg.mkdir(parents=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        shutil.copy2(CFG / f, cfg / f)
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_KallisteStub]\n")
    sec = SCRATCH / "data/tilesets/secondary/kalliste"
    shutil.copytree(SRC, sec / "porytiles_src")
    shutil.copytree(BIN, sec / "porytiles_bin")
    return sec


def compile_tileset():
    sec = scratch_project()
    r = run([porytiles(), "compile-tileset", "-C", str(SCRATCH), "--no-verify-checksums",
             "gTileset_Kalliste"])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    shutil.rmtree(BIN)
    shutil.copytree(sec / "porytiles_bin", BIN)
    shutil.copy2(SCRATCH / "porytiles/tilesets/gTileset_Kalliste/tileset.cache.json",
                 CFG / "tileset.cache.json")


def verify(rows):
    raw = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = []
    for i, entries in enumerate(raw):
        for e in entries:
            e = int(e)
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                continue  # the universal transparent tile
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"kalliste_build: entries outside kalliste's tiles/palettes 6-12: {bad[:10]}")
    from PIL import Image
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1   # the rest is padding
    print(f"verified {len(raw)} metatiles; {used} of 512 tiles used")
    return used


def catalog(secs):
    data = []
    for name, structs in secs:
        for s in structs:
            data.append({
                "key": s.key, "title": s.title, "section": name, "w": s.w, "h": s.h,
                "ids": s.ids, "walk": s.walk, "notes": s.notes,
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
            })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps(data, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    ap.add_argument("--only", help="preview only these structure keys (comma list)")
    args = ap.parse_args()

    secs = sections()
    allst = [s for _, ss in secs for s in ss]
    probs = validate(allst)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        sel = allst
        if args.only:
            keys = set(args.only.split(","))
            sel = [s for s in allst if s.key in keys]
        preview(sel).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack([(SECTION_ROWS[n], ss) for n, ss in secs])
    write_sources(allst, rows, SRC)
    catalog(secs)
    if not args.no_compile:
        compile_tileset()
        used = verify(rows)
        import kalliste_catalog
        kalliste_catalog.main(used)


if __name__ == "__main__":
    main()
