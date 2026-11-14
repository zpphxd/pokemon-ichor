#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Akti, Akti Town's harbor secondary.

1. Draws every structure (akti_art.build(): kalliste copies, the harbor, the
   coast, the town) and checks each 8x8 tile draws from one of Akti's seven
   palette groups (akti_lib.GROUPS).
2. Packs them into the 8-wide metatile sheet from 0x200, in build order.
3. Writes data/tilesets/secondary/akti/porytiles_src (bottom/middle/top.png,
   attributes.csv).
4. Compiles with Porytiles in a scratch project (build/akti_porytiles) against
   an empty stand-in primary, so Akti's own art uses only its own tiles and
   palettes 6-12, then copies porytiles_bin and the cache back.
5. Borrows aethos's ground: every cell drawn on grass, sand or sea gets its
   bottom-layer tiles pointed at aethos's grass (0x001), sand (0x124) or animated
   sea (0x170). Rebuild Akti whenever aethos is repainted.
6. Verifies every metatile entry, writes build/akti/catalog.json (read by
   tools/ichor/maps/akti.py), the sheet and preview images, and
   design/phase1/TILES_akti.md.

Usage: /usr/bin/python3 tools/ichor/art/akti_build.py [--no-compile] [--preview out.png]
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
import akti_lib  # noqa: E402
from akti_lib import GROUND_METATILE, ROOT, validate  # noqa: E402
from kalliste_lib import pack, write_sources  # noqa: E402

SRC = ROOT / "data/tilesets/secondary/akti/porytiles_src"
BIN = ROOT / "data/tilesets/secondary/akti/porytiles_bin"
CFG = ROOT / "porytiles/tilesets/gTileset_Akti"
SCRATCH = ROOT / "build/akti_porytiles"
OUT = ROOT / "build/akti"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
SHEET = ROOT / "design/phase1/img/akti_sheet.png"
PIECES = ROOT / "design/phase1/img/akti_pieces.png"


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"akti_build: failed: {' '.join(map(str, cmd))}")
    return r


def scratch_project():
    """A minimal Porytiles project holding an empty primary and a copy of akti."""
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
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_AktiStub"])
    stub = SCRATCH / "data/tilesets/primary/akti_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    from PIL import Image
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_AktiStub"])
    cfg = SCRATCH / "porytiles/tilesets/gTileset_Akti"
    cfg.mkdir(parents=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        shutil.copy2(CFG / f, cfg / f)
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_AktiStub]\n")
    sec = SCRATCH / "data/tilesets/secondary/akti"
    shutil.copytree(SRC, sec / "porytiles_src")
    shutil.copytree(BIN, sec / "porytiles_bin")
    return sec


def compile_tileset():
    sec = scratch_project()
    r = run([porytiles(), "compile-tileset", "-C", str(SCRATCH), "--no-verify-checksums",
             "gTileset_Akti"])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    shutil.rmtree(BIN)
    shutil.copytree(sec / "porytiles_bin", BIN)
    shutil.copy2(SCRATCH / "porytiles/tilesets/gTileset_Akti/tileset.cache.json",
                 CFG / "tileset.cache.json")


NORMAL, COVERED, SPLIT = 0, 1, 2   # metatile layer types (attribute bits 12-15)


def borrow_ground(structs):
    """Give each ground cell aethos's ground tiles as its bottom layer.

    Those cells were compiled with an empty bottom, so Porytiles put their one
    drawn layer wherever its layer type says. Find it, then rebuild the cell as
    COVERED (ground under the middle layer) or SPLIT (ground under the top
    layer, drawn over the player)."""
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
            # where Porytiles put the drawn layer: the half that isn't all transparent
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
        sys.exit(f"akti_build: entries outside akti's tiles/palettes 6-12: {bad[:10]}")
    from PIL import Image
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    print(f"verified {len(raw)} metatiles; {used} of 512 tiles used; "
          f"{len(patched)} cells on aethos ground")
    return used


def catalog(structs):
    data = []
    for s in structs:
        data.append({
            "key": s.key, "title": s.title, "section": "akti", "w": s.w, "h": s.h,
            "ids": s.ids, "walk": s.walk, "notes": s.notes,
            "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
            "ground": {f"{x},{y}": g for (x, y), g in getattr(s, "ground", {}).items()},
        })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps(data, indent=1))


def images(structs):
    akti_lib.preview(structs, scale=2, cols=4).save(PIECES)
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", "akti",
         "--primary", "aethos", "--scale", "2", "-o", str(SHEET)])
    print(SHEET)
    print(PIECES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()

    import akti_art
    structs = akti_art.build()
    keys = [s.key for s in structs]
    assert len(keys) == len(set(keys)), "duplicate structure keys"
    probs = validate(structs)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        akti_lib.preview(structs, scale=2, cols=4).save(args.preview)
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
        used = verify(rows, patched)
        images(structs)
        import akti_catalog
        akti_catalog.main(used)


if __name__ == "__main__":
    main()
