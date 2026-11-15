#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Labyrinth, Daedalus's Labyrinth under Knossa.

The pipeline is emporion_build.py's, for a self-contained interior tileset (as
the Temple of Hermes is), plus the two palette variant sets the Labyrinth needs:

1. Draws every structure (labyrinth_art.build()) and checks each 8x8 tile draws
   from one palette group, every bottom layer is opaque and no metatile uses
   three layers. Tiles within NEAR_DUPLICATE_PX pixels of another are redrawn as
   that one, so they are stored once.
2. Packs them into the 8-wide metatile sheet from 0x200, section by section,
   each section on a fixed row (labyrinth_art.SECTIONS) so adding to one never
   renumbers another, and writes data/tilesets/secondary/labyrinth/porytiles_src.
3. Compiles with Porytiles in a scratch project under build/ against an empty
   stand-in primary, so the tileset uses only its own tiles and palettes 6-12
   and works on any interior primary (it is drawn for oikos).
4. Writes the variant palette sets beside the compiled palettes:
   - glow/NN.pal, the doused torch (SYSTEMS.md §2): black but for the glow
     paint, the flames and a faint thread. The latent glow color is normalized
     in the base palettes to the stone it imitates.
   - dawn/NN.pal, scene L: every color dimmed and cooled but the dawn light.
   The map (world-act3) loads either over palettes 6-12.
5. Verifies every entry, fails past TILE_LIMIT (504) tiles (door animations own
   504-511), and writes build/labyrinth/catalog.json, the sheet and pieces
   previews in design/phase4/img/, and design/phase4/TILES_labyrinth.md.

Usage: /usr/bin/python3 tools/ichor/art/labyrinth_build.py [--no-compile]
Then /usr/bin/python3 tools/ichor/art/labyrinth_scene.py renders the mock scenes.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion_build as EB  # noqa: E402
import emporion_lib as E  # noqa: E402
import labyrinth_art as A  # noqa: E402
from kalliste_lib import write_sources  # noqa: E402

ROOT = A.K.ROOT
IMG = ROOT / "design/phase4/img"
TILE_LIMIT = EB.TILE_LIMIT


class Spec:
    """The fields emporion_build's helpers read."""
    name = dir = "labyrinth"
    symbol = "gTileset_Labyrinth"
    groups = A.GROUPS
    art = A
    temple = True   # self-contained: no borrowed ground, opaque bottoms

    def __init__(self):
        self.src = ROOT / f"data/tilesets/secondary/{self.dir}/porytiles_src"
        self.bin = ROOT / f"data/tilesets/secondary/{self.dir}/porytiles_bin"
        self.cfg = ROOT / f"porytiles/tilesets/{self.symbol}"
        self.scratch = ROOT / f"build/{self.dir}_porytiles"
        self.out = ROOT / f"build/{self.dir}"
        self.sheet = IMG / f"{self.dir}_sheet.png"
        self.pieces = IMG / f"{self.dir}_pieces.png"


def compile_tileset(spec):
    # Until the tileset is registered in src/data/tilesets/headers.h, Porytiles
    # can't reopen it from its manifest, so create it afresh each time.
    if spec.symbol not in (ROOT / "src/data/tilesets/headers.h").read_text():
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            (spec.cfg / f).unlink(missing_ok=True)
    sec = EB.scratch_project(spec)
    r = EB.run([EB.porytiles(), "compile-tileset", "-C", spec.scratch, "--no-verify-checksums",
                spec.symbol])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if spec.bin.exists():
        shutil.rmtree(spec.bin)
    shutil.copytree(sec / "porytiles_bin", spec.bin)
    spec.cfg.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        p = spec.scratch / f"porytiles/tilesets/{spec.symbol}/{f}"
        if p.exists():
            shutil.copy2(p, spec.cfg / f)
    (spec.cfg / "config.yaml").write_text(
        "# Written by tools/ichor/art/labyrinth_build.py; edit it there.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Oikos]\n"
        + EB.hints_yaml(spec.groups, E.C))


# --------------------------------------------------------------------------
# The variant palette sets
# --------------------------------------------------------------------------

def read_pal(p):
    vals = [int(v) for v in p.read_text().split()[3:]]
    return [tuple(vals[i * 3:i * 3 + 3]) for i in range(len(vals) // 3)]


def write_pal(p, cols):
    # .pal files are CRLF in this repo (.gitattributes), as Porytiles writes them
    p.write_bytes(("JASC-PAL\r\n0100\r\n16\r\n"
                   + "".join(f"{r} {g} {b}\r\n" for r, g, b in cols)).encode())


def variant_palettes(spec):
    """Normalize the latent glow color, then write glow/ and dawn/ beside palettes/."""
    pals = spec.bin / "palettes"
    glow_dir, dawn_dir = spec.bin / "glow", spec.bin / "dawn"
    glow_dir.mkdir(exist_ok=True)
    dawn_dir.mkdir(exist_ok=True)
    latent = {A.C[n]: n for n in A.LATENT}
    keep = {A.C[n] for n in A.GLOW_KEEP}
    dim = {A.C[n]: v for n, v in A.GLOW_DIM.items()}
    dawn_keep = {A.C[n] for n in A.DAWN_KEEP}
    found = {}
    for i in range(16):
        p = pals / f"{i:02d}.pal"
        cols = read_pal(p)
        glow = [(0, 0, 0)] * 16
        dawn = list(cols)
        if 6 <= i <= 12:
            for k, c in enumerate(cols):
                if k == 0:
                    continue
                if c in latent:
                    n = latent[c]
                    glow[k] = A.LATENT[n]
                    cols[k] = A.C[A.LATENT_BASE[n]]
                    found.setdefault(n, []).append((i, k))
                elif c in keep:
                    glow[k] = c
                elif c in dim:
                    glow[k] = dim[c]
                dawn[k] = cols[k] if cols[k] in dawn_keep else A.dawn_color(cols[k])
            write_pal(p, cols)
        glow[0] = cols[0]
        write_pal(glow_dir / f"{i:02d}.pal", glow)
        write_pal(dawn_dir / f"{i:02d}.pal", dawn)
    for n in A.LATENT:
        if n not in found:
            print(f"glow paint {n}: not drawn yet (no glow-marks in this batch)")
    return found


def catalog_json(spec, structs):
    """emporion_build's catalog, plus each odd twin's twin: the structure and first
    row it stands in for."""
    import json
    EB.catalog_json(spec, structs)
    p = spec.out / "catalog.json"
    data = json.loads(p.read_text())
    by_key = {s.key: s for s in structs}
    for d in data:
        s = by_key[d["key"]]
        if getattr(s, "twin_of", None):
            d["twin_of"] = list(s.twin_of)
        d["parity"] = getattr(s, "parity", None)
    p.write_text(json.dumps(data, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    spec = Spec()

    sections = A.build()
    structs = [s for _, ss in sections for s in ss]
    keys = [s.key for s in structs]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, f"duplicate structure keys {dup}"
    probs = A.validate(structs)
    if not probs:
        before = len(EB._tiles(structs))
        merges = EB.merge_near_duplicates(structs)
        print(f"merged {len(merges)} near-duplicate tiles "
              f"({merges.count(1)} differed by 1 px, {merges.count(2)} by 2): "
              f"{before} -> {len(EB._tiles(structs))} distinct tiles before palette sharing")
        probs = A.validate(structs)
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    rows = A.pack(sections)
    print(f"{sum(s.w * s.h for s in structs)} metatiles drawn, in {rows} sheet rows")
    write_sources(structs, rows, spec.src)
    catalog_json(spec, structs)
    if args.no_compile:
        return
    compile_tileset(spec)
    used = EB.verify(spec, rows, {})
    variant_palettes(spec)
    print("colors per palette 6-12:", EB.palette_report(spec))
    IMG.mkdir(parents=True, exist_ok=True)
    EB.images(spec, [s for s in structs if not s.key.endswith("_odd")])
    A.write_catalog(used, structs)


if __name__ == "__main__":
    main()
