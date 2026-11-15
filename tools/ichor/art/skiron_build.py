#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Skiron, the secondary for Act I's
mainland road: Route 4 (the Isthmus road) and Route 5 (the Skironian cliffs).

1. Paints every structure (skiron_ground, _rock, _flora, _tombs, _props):
   the paved road and tall grass in the shapes listed in skiron_shapes.json,
   the diolkos, stone and the sea cliff, pines and scrub, the roadside tombs
   and the toppled tomb, the kilns, hives, the procession's camp and the ship.
   Checks each 8x8 tile draws from one of the seven palette groups
   (skiron_lib.GROUPS), then redraws tiles within 2 px of another as that one
   so they're stored once.
2. Packs them into the 8-wide metatile sheet; each section starts on a fixed
   row, so growing one section never renumbers another.
3. Writes data/tilesets/secondary/skiron/porytiles_src.
4. Compiles with Porytiles in a scratch project (build/skiron_porytiles)
   against an empty stand-in primary, so Skiron's own art uses only its own
   tiles and palettes 6-12, and copies porytiles_bin and the cache back.
5. Borrows aethos ground: every cell marked as sitting on grass, the path or
   the sea gets its bottom tiles pointed at aethos's 0x001, 0x1D9 or the
   animated 0x170. Rebuild Skiron whenever aethos's ground is repainted.
6. Verifies every metatile entry and the tile budget (504: the door
   animations own tiles 504-511), writes build/skiron/catalog.json (map
   builders and skiron_mockups.py read it), the numbered sheet, a pieces
   preview, the metatile labels scripts swap in, and the catalog section of
   design/phase2/TILES_skiron.md.

Usage: /usr/bin/python3 tools/ichor/art/skiron_build.py [--no-compile] [--preview out.png] [--plan]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skiron_flora  # noqa: E402
import skiron_ground  # noqa: E402
import skiron_props  # noqa: E402
import skiron_rock  # noqa: E402
import skiron_tombs  # noqa: E402
from agros_lib import pack, write_sources  # noqa: E402
from akti_build import _tiles, merge_near_duplicates  # noqa: E402
from skiron_lib import GROUND_METATILE, ROOT, preview, validate  # noqa: E402

NAME = "gTileset_Skiron"
SRC = ROOT / "data/tilesets/secondary/skiron/porytiles_src"
BIN = ROOT / "data/tilesets/secondary/skiron/porytiles_bin"
CFG = ROOT / "porytiles/tilesets" / NAME
SCRATCH = ROOT / "build/skiron_porytiles"
OUT = ROOT / "build/skiron"
SHAPES = Path(__file__).resolve().parent / "skiron_shapes.json"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
SHEET = ROOT / "design/phase2/img/skiron_sheet.png"
PIECES = ROOT / "design/phase2/img/skiron_pieces.png"

# First metatile row of each section (8 metatiles a row; id = 0x200 + row*8 + col).
SECTION_ROWS = {"ground": 0, "stone": 8, "flora": 32, "tombs": 40, "works": 50, "camp": 56}
SECTION_TITLES = {
    "ground": ("Ground", "The old paved road and tall grass, both with soft, shape-keyed edges."),
    "stone": ("Stone", "Rocks, ledges, the Skironian sea cliff and the road's cut bank, "
                       "Aphrodite's niches, the rock seat, the orchard's terrace wall and the "
                       "ruined watchtower."),
    "flora": ("Pines and scrub", "Aleppo pines in three shapes, kermes oak, thyme and dry grass."),
    "tombs": ("Tombs", "Grave stelai, a lekythos, a sarcophagus, the family plot's walls, a "
                       "burial mound, a milestone, and the toppled tomb (the rubble and the road "
                       "it leaves)."),
    "works": ("The potters' works and the hives", "Kilns, the drying rack, the wasters' heap, "
                                                  "firewood, amphorae and beehives."),
    "camp": ("The procession's camp", "Tents, bedrolls, myrtle, the sacred baskets, the "
                                      "cookfire and the cart."),
}
TILE_LIMIT = 504          # CLAUDE.md: tiles 504-511 of a secondary are the door animations'
NORMAL, COVERED, SPLIT = 0, 1, 2

LABELS = ROOT / "include/constants/metatile_labels.h"
LABEL_START = "// gTileset_Skiron (Ichor: Routes 4 and 5), written by tools/ichor/art/skiron_build.py"
LABEL_END = "// end gTileset_Skiron"
# The metatiles scripts swap in: the Bronze Hammer breaks the toppled tomb's rubble.
LABEL_PIECES = {
    "rubble": ["Rubble_TopLeft", "Rubble_TopRight", "Rubble_BottomLeft", "Rubble_BottomRight"],
    "rubble_cleared": ["RubbleCleared_TopLeft", "RubbleCleared_TopRight",
                       "RubbleCleared_BottomLeft", "RubbleCleared_BottomRight"],
    "rubble_small": ["RubbleSmall"],
    "rubble_small_cleared": ["RubbleSmallCleared"],
}


def sections():
    shapes = json.loads(SHAPES.read_text()) if SHAPES.exists() else {}
    return [("ground", skiron_ground.build(shapes)), ("stone", skiron_rock.build()),
            ("flora", skiron_flora.build()), ("tombs", skiron_tombs.build()),
            ("works", skiron_props.works()), ("camp", skiron_props.camp())]


# --------------------------------------------------------------------------
# Porytiles
# --------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"skiron_build: failed: {' '.join(map(str, cmd))}")
    return r


def scratch_project():
    """A minimal Porytiles project: an empty primary and Skiron paired with it."""
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
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_SkironStub"])
    stub = SCRATCH / "data/tilesets/primary/skiron_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_SkironStub"])
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    sec = SCRATCH / "data/tilesets/secondary/skiron"
    cfg.mkdir(parents=True)
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_SkironStub]\n")
    if (CFG / "tileset-manifest.json").exists() and BIN.exists():
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            shutil.copy2(CFG / f, cfg / f)
        shutil.copytree(BIN, sec / "porytiles_bin")
    else:
        # first build: Porytiles creates the tileset (and appends its C
        # declarations to the scratch headers; the real ones are kept by hand)
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
    (CFG / "config.yaml").write_text(
        "# Per-tileset Porytiles config for gTileset_Skiron, the secondary for Routes 4 and 5.\n"
        "# Sources are drawn by tools/ichor/art/skiron_build.py, which compiles Skiron against\n"
        "# an empty stand-in primary, checks its own art uses only its tiles and palettes 6-12,\n"
        "# then points its ground cells at aethos's grass, path and sea. Pair it with aethos\n"
        "# when compiling it directly (the build's borrowed ground is then lost: rerun the script).\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n")


def borrow_ground(structs):
    """Give each borrowed-ground cell aethos's ground tiles as its bottom layer.

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
        sys.exit(f"skiron_build: entries outside Skiron's tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for i, entries in enumerate(raw) for j, e in enumerate(entries)
                   if not (i in patched and j < 4) and (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{len(patched)} cells on aethos ground")
    if used > TILE_LIMIT or late:
        sys.exit(f"skiron_build: {used} tiles used and tiles {late[:8]} referenced; a secondary "
                 f"may use at most {TILE_LIMIT} (504-511 belong to door animations)")
    return used


# --------------------------------------------------------------------------
# Outputs
# --------------------------------------------------------------------------

def catalog(secs):
    data = []
    for name, structs in secs:
        for s in structs:
            data.append({
                "key": s.key, "title": s.title, "section": name, "w": s.w, "h": s.h,
                "ids": s.ids, "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
                "ground": {f"{x},{y}": g for (x, y), g in getattr(s, "ground", {}).items()},
            })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps(data, indent=1))


def write_labels(secs):
    """The metatiles scripts swap in, as METATILE_Skiron_* in metatile_labels.h,
    rewritten in place on every build so the ids never go stale."""
    lines = [LABEL_START]
    for _, structs in secs:
        for s in structs:
            labels = LABEL_PIECES.get(s.key, ())
            cells = [c for row in s.ids for c in row]
            for label, mid in zip(labels, cells):
                lines.append(f"#define METATILE_Skiron_{label:<26} 0x{mid:03X}")
    lines.append(LABEL_END)
    block = "\n".join(lines) + "\n"
    text = LABELS.read_text()
    if LABEL_START in text:
        a = text.index(LABEL_START)
        b = text.index(LABEL_END, a) + len(LABEL_END) + 1
        text = text[:a] + block + text[b:]
    else:
        end = text.rindex("#endif")
        text = text[:end] + block + "\n" + text[end:]
    LABELS.write_text(text)


def images(secs):
    allst = [s for _, ss in secs for s in ss]
    PIECES.parent.mkdir(parents=True, exist_ok=True)
    preview(allst, scale=2, width=1200).save(PIECES)
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet",
         str(ROOT / "data/tilesets/secondary/skiron"), "--primary", "gTileset_Aethos",
         "--scale", "2", "-o", str(SHEET)])
    print(SHEET)
    print(PIECES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    ap.add_argument("--plan", action="store_true", help="print each section's rows and stop")
    args = ap.parse_args()
    secs = sections()
    allst = [s for _, ss in secs for s in ss]
    keys = [s.key for s in allst]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, f"duplicate structure keys: {dup}"
    probs = validate(allst)
    if not probs:
        before = len(_tiles(allst))
        merges = merge_near_duplicates(allst)
        print(f"merged {len(merges)} near-duplicate tiles: {before} -> {len(_tiles(allst))} tiles")
        probs = validate(allst)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        preview(allst, scale=2, width=1200).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    if args.plan:
        from agros_lib import COLS
        for name, ss in secs:
            row, col, shelf = SECTION_ROWS[name], 0, 0
            for s in ss:
                if col + s.w > COLS:
                    row += shelf
                    col, shelf = 0, 0
                col += s.w
                shelf = max(shelf, s.h)
            print(f"{name:8s} rows {SECTION_ROWS[name]:2d}..{row + shelf - 1:2d}")
    rows = pack([(SECTION_ROWS[n], ss) for n, ss in secs])
    assert rows <= 64, f"{rows} sheet rows: more than 512 metatiles"
    if args.plan:
        return
    write_sources(allst, rows, SRC)
    catalog(secs)
    write_labels(secs)
    if not args.no_compile:
        compile_tileset()
        patched = borrow_ground(allst)
        used = verify(rows, patched)
        images(secs)
        import skiron_catalog
        skiron_catalog.main(used)


if __name__ == "__main__":
    main()
