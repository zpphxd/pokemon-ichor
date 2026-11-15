#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Kemet, Egypt's outdoor secondary.

Runs emporion_build.py's pipeline (draw, merge near-duplicate tiles, pack the
sheet by section, compile with Porytiles against a stand-in primary so the art
uses only its own tiles and palettes 6-12, point cells on grass, sand, sea and path
at aethos's own ground metatiles, verify, and fail past 504 tiles), with Kemet's
art (kemet_art.py), palette groups (kemet_lib.py) and catalog (kemet_catalog.py).

Writes data/tilesets/secondary/kemet/, porytiles/tilesets/gTileset_Kemet/,
build/kemet/catalog.json (the map builders read it), design/oikoumene/TILES_kemet.md
and the sheet and pieces images in design/oikoumene/img/.

Usage: /usr/bin/python3 tools/ichor/art/kemet_build.py [--no-compile] [--preview out.png]
Rebuild whenever aethos is repainted (the borrowed ground comes from it).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kemet_lib  # noqa: E402,F401  (registers Kemet's colors before the pipeline reads them)
import emporion_build as EB  # noqa: E402
import emporion_lib as E  # noqa: E402
from kalliste_lib import pack, write_sources  # noqa: E402

EB.TILESETS["kemet"] = ("kemet_art", "gTileset_Kemet")
IMG = EB.ROOT / "design/oikoumene/img"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()
    spec = EB.Spec("kemet")
    spec.groups = kemet_lib.GROUPS
    spec.sheet = IMG / "kemet_sheet.png"
    spec.pieces = IMG / "kemet_pieces.png"
    IMG.mkdir(parents=True, exist_ok=True)

    sections = spec.art.build()
    structs = [s for _, ss in sections for s in ss]
    keys = [s.key for s in structs]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, f"duplicate structure keys {dup}"
    probs = kemet_lib.validate(structs)
    if not probs:
        before = len(EB._tiles(structs))
        merges = EB.merge_near_duplicates(structs)
        print(f"merged {len(merges)} near-duplicate tiles: {before} -> "
              f"{len(EB._tiles(structs))} distinct tiles before palette sharing")
        probs = kemet_lib.validate(structs)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        E.preview(structs, scale=2, cols=5).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack(sections)
    assert rows <= 64, f"{rows} sheet rows: more than 512 metatiles"
    write_sources(structs, rows, spec.src)
    EB.catalog_json(spec, structs)
    if args.no_compile:
        return
    EB.compile_tileset(spec)
    patched = EB.borrow_ground(spec, structs)
    used = EB.verify(spec, rows, patched)
    print("colors per palette 6-12:", EB.palette_report(spec))
    # The config the scratch compile left in the repo names the Emporion script;
    # say who writes this one.
    cfg = spec.cfg / "config.yaml"
    cfg.write_text(cfg.read_text().replace("emporion_build.py", "kemet_build.py"))
    EB.images(spec, structs)
    spec.art.write_catalog(used, structs)


if __name__ == "__main__":
    main()
