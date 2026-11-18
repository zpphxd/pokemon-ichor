#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Oros, the outdoor snows of Olympus
(tools/ichor/art/oros_art.py).

Unlike Chion's sheet, Oros packs by content: every 16x16 cell of every piece is
compared with every other (all three layers, its behavior and whether it
blocks), and identical cells share one metatile. The full-width facade repeats
its columns, frieze and steps, so its 600 cells come to a fraction of that; a
secondary may hold only 512 metatiles and 504 tiles, and this build checks both.

Writes data/tilesets/secondary/<oros|propylon>/{porytiles_src,porytiles_bin,catalog.json}
(each piece's ids grid: tools/ichor/maps/oros_lib.py reads it) and the
numbered sheet design/maps/img/<set>_sheet.png.

Two tilesets come out of the one drawing: gTileset_Oros (the Snowfield, the
Glacier, Boreas's ridge) and gTileset_Propylon (3F's terraces and the
Propylaia's full-width facade), since the facade alone fills half a secondary.

Usage: /usr/bin/python3 tools/ichor/art/oros_build.py [--set oros,propylon] [--no-compile] [--preview out.png]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pantheon_lib as P  # noqa: E402
import oros_art as art  # noqa: E402
from chion_lib import preview, validate  # noqa: E402

ROOT = P.ROOT
SETS = {"oros": ("gTileset_Oros", "oros"), "propylon": ("gTileset_Propylon", "propylon")}
METATILE_LIMIT = 512


def cell_key(s, cx, cy):
    parts = []
    for n in ("bottom", "middle", "top"):
        parts.append(s.layers[n].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16].tobytes())
    parts.append(s.walk[cy][cx].encode())
    parts.append(str(s.behaviors.get((cx, cy), "")).encode())
    return b"|".join(parts)


def pack_unique(structs):
    """Give every distinct cell one metatile id (0x200 up), in first-seen order."""
    seen, cells = {}, []
    for s in structs:
        s.ids = [[0] * s.w for _ in range(s.h)]
        for cy in range(s.h):
            for cx in range(s.w):
                k = cell_key(s, cx, cy)
                if k not in seen:
                    seen[k] = len(cells)
                    cells.append((s, cx, cy))
                s.ids[cy][cx] = 0x200 + seen[k]
    return cells


def write_sources(cells, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    rows = (len(cells) + 7) // 8
    for n in ("bottom", "middle", "top"):
        sheet = np.zeros((rows * 16, 128, 4), np.uint8)
        for i, (s, cx, cy) in enumerate(cells):
            y, x = divmod(i, 8)
            sheet[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = s.layers[n].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        Image.fromarray(sheet, "RGBA").save(outdir / f"{n}.png")
    lines = ["id,behavior"]
    for i, (s, cx, cy) in enumerate(cells):
        mb = s.behaviors.get((cx, cy))
        if mb:
            lines.append(f"{i},{mb}")
    (outdir / "attributes.csv").write_text("\n".join(lines) + "\n")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview")
    ap.add_argument("--only", help="sections to build (a test of the tile count)")
    ap.add_argument("--set", default="oros,propylon", help="oros (the snow floors), propylon (3F and the facade)")
    args = ap.parse_args()
    for which in args.set.split(","):
        build(which, args)


def build(which, args):
    NAME, FOLDER = SETS[which]
    SHEET = ROOT / f"design/maps/img/{FOLDER}_sheet.png"
    P.use(art.C, art.GROUPS)
    secs = art.sections(which)
    if args.only:
        secs = [(n, ss) for n, ss in secs if n in args.only.split(",")]
    allst = [s for _, ss in secs for s in ss]
    probs = validate(allst)
    for p in probs[:40]:
        print("PROBLEM:", p)
    if args.preview:
        preview(allst, scale=2).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    cells = pack_unique(allst)
    print(f"{NAME}: {sum(s.w * s.h for s in allst)} cells in {len(allst)} pieces -> {len(cells)} metatiles")
    if len(cells) > METATILE_LIMIT:
        sys.exit(f"{NAME}: {len(cells)} metatiles; a secondary holds {METATILE_LIMIT}")
    seat = P.Seat(NAME, FOLDER, art.C, art.GROUPS, lambda: secs, {})
    rows = write_sources(cells, seat.src)
    if args.no_compile:
        return
    seat.compile()
    used = seat.verify(rows)
    data = {"tileset": NAME, "primary": "gTileset_Aethos", "tiles_used": used, "metatiles": len(cells),
            "pieces": []}
    for name, structs in secs:
        for s in structs:
            data["pieces"].append({"key": s.key, "title": s.title, "section": name, "w": s.w, "h": s.h,
                                   "ids": s.ids, "walk": s.walk,
                                   "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()}})
    seat.catalog_path.write_text(json.dumps(data, indent=1) + "\n")
    cfg = seat.cfg / "config.yaml"
    cfg.write_text(cfg.read_text().replace("a seat of the Pantheon", "the outdoor snows of Olympus")
                   .replace("pantheon_build.py", "oros_build.py").replace("gTileset_Oikos", "gTileset_Aethos")
                   .replace("Pair it with oikos", "Pair it with aethos"))
    seat.sheet(SHEET)
    print(SHEET)


if __name__ == "__main__":
    main()
