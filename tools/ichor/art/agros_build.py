#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Agros, the countryside secondary tileset.

1. Paints every structure: soft-edged ground (tall grass, path, goat tracks)
   in the shapes listed in agros_shapes.json, flora, stone, props, and copies
   of the kalliste ruins Route 1 and Kronion Hill use. Checks each 8x8 tile
   draws from one palette group.
2. Packs them into the 8-wide metatile sheet; each section starts on a fixed
   row, so growing one section never renumbers another.
3. Writes data/tilesets/secondary/agros/porytiles_src.
4. Compiles with Porytiles in a scratch project (build/agros_porytiles)
   against an empty stand-in primary, so Agros uses only its own tiles and
   palettes 6-12, copies porytiles_bin and the Porytiles cache back, and
   verifies every metatile entry.
5. Writes build/agros/catalog.json (map builders read it), the sheet image
   design/phase1/img/agros_sheet.png, and design/phase1/TILES_agros.md.

Usage: /usr/bin/python3 tools/ichor/art/agros_build.py [--no-compile] [--preview out.png]

Ground shapes: a map builder lists the tall-grass, path and track shapes its
maps need in tools/ichor/art/agros_shapes.json (tools/ichor/maps/route1.py
--shapes does it for Route 1 and Kronion Hill). Rebuild Agros after it changes,
and after aethos's grass, tall grass or path art changes.
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
import agros_flora  # noqa: E402
import agros_ground  # noqa: E402
import agros_props  # noqa: E402
import agros_rock  # noqa: E402
from agros_lib import ROOT, Struct, adopt, composite, pack, preview, validate, write_sources  # noqa: E402

NAME = "gTileset_Agros"
SRC = ROOT / "data/tilesets/secondary/agros/porytiles_src"
BIN = ROOT / "data/tilesets/secondary/agros/porytiles_bin"
CFG = ROOT / "porytiles/tilesets" / NAME
SCRATCH = ROOT / "build/agros_porytiles"
OUT = ROOT / "build/agros"
SHAPES = Path(__file__).resolve().parent / "agros_shapes.json"
DOC = ROOT / "design/phase1/TILES_agros.md"
SHEET = ROOT / "design/phase1/img/agros_sheet.png"

# First metatile row of each section (8 metatiles a row; id = 0x200 + row*8 + col).
SECTION_ROWS = {"ground": 0, "flora": 20, "stone": 26, "props": 38, "ruins": 42}
SECTION_TITLES = {
    "ground": "Soft ground: tall grass, the road, goat tracks",
    "flora": "Trees, shrubs and herbs",
    "stone": "Stone: rocks, walls, ledges, the hill, the shore, the threshing floor",
    "props": "Farm and roadside props",
    "ruins": "Kronion's ruins and terraces (copied from kalliste)",
}
KALLISTE_PARTS = ["stylobate", "ruin_columns", "ruin_drums", "dig_site", "altar_broken", "terrace"]


def ground():
    shapes = json.loads(SHAPES.read_text()) if SHAPES.exists() else {}
    out = []
    specs = [
        ("tall", "Tall grass with soft edges", agros_ground.paint_tall, "G",
         "Barley meadow edges. Each piece is named by its shape key (see agros_ground.py) and "
         "keeps MB_TALL_GRASS, so encounters follow the cells while the outline stays soft."),
        ("path", "The limestone road, curving", agros_ground.paint_path, ".",
         "Road pieces by shape key, including half cells that cut stair-steps on the diagonal. "
         "The road's middle is aethos 0x1D9."),
        ("track", "Goat track", agros_ground.paint_track, ".",
         "A narrow worn track of bare earth through grass, by shape key."),
    ]
    for kind, title, painter, code, notes in specs:
        keys = shapes.get(kind) or []
        if keys:
            out.append(agros_ground.shape_set(kind, title, keys, painter, code, "ground", notes))
    return out


def kalliste_parts():
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import kalliste_elaia
    import kalliste_kronion
    found = {s.key: s for s in kalliste_kronion.build() + kalliste_elaia.build()}
    parts = [adopt(found[k], "ruins") for k in KALLISTE_PARTS]
    dig = next(s for s in parts if s.key == "dig_site")
    return parts + [pit_stair(dig)]


def pit_stair(dig):
    """The dig pit's lower half after the slice: the Titanborn dug deeper and
    struck cut stone steps going down into the dark (design/SYSTEMS.md, relic
    gates: Hecate's Torch's second gate, down to the Kronion crypt). Kronion
    Hill's script swaps it in for the pit's lower row once the ruins are clear."""
    s = Struct("pit_stair", "Kronion Hill: the dark stair in the pit", 2, 1, "ruins", walk=["XX"],
               names={"left": (0, 0), "right": (1, 0)},
               notes="The pit's lower row once the steps are uncovered: three worn treads "
                     "dropping into black. Set over the pit's (0,1)-(1,1) cells in game "
                     "(METATILE_Agros_PitStair_Left/Right).")
    L = s.B
    L.a[:] = dig.B.a[16:32, 0:32]
    L.vline(6, 0, 12, "s0")                       # the cut walls of the stairwell
    L.vline(25, 0, 12, "s1")
    L.hline(6, 25, 0, "s1")                       # the lip where the floor gives way
    L.hline(7, 24, 1, "s4")                       # first tread, lit
    L.hline(7, 24, 2, "s3")
    L.hline(7, 24, 3, "s0")                       # its riser
    L.rect(7, 4, 18, 2, "s2")                     # second tread
    L.hline(8, 23, 6, "sk")
    L.hline(8, 23, 7, "s1")                       # third, barely lit
    L.rect(7, 8, 18, 5, "ink")                    # then nothing
    L.vline(7, 4, 12, "sk")
    L.vline(24, 4, 12, "s0")
    for x, y in ((10, 2), (19, 1), (14, 5), (21, 4)):
        L.px(x, y, "s2" if y < 3 else "s1")       # wear on the treads
    return s


TILE_LIMIT = 504          # CLAUDE.md: tiles 504-511 of a secondary are the door animations'

LABELS = ROOT / "include/constants/metatile_labels.h"
LABEL_START = "// gTileset_Agros (Ichor: Route 1 and Kronion Hill), written by tools/ichor/art/agros_build.py"
LABEL_END = "// end gTileset_Agros"


def write_labels(secs):
    """The metatiles scripts swap in, as METATILE_Agros_* in metatile_labels.h,
    rewritten in place on every build so the ids never go stale."""
    want = {"pit_stair": ("PitStair_Left", "PitStair_Right")}
    lines = [LABEL_START]
    for _, structs in secs:
        for s in structs:
            for i, label in enumerate(want.get(s.key, ())):
                lines.append(f"#define METATILE_Agros_{label:<26} 0x{s.ids[0][i]:03X}")
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


def sections():
    return [("ground", ground()), ("flora", agros_flora.build()), ("stone", agros_rock.build()),
            ("props", agros_props.build()), ("ruins", kalliste_parts())]


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"agros_build: failed: {' '.join(map(str, cmd))}")
    return r


def scratch_project():
    """A minimal Porytiles project: an empty primary and Agros paired with it."""
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
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_AgrosStub"])
    stub = SCRATCH / "data/tilesets/primary/agros_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_AgrosStub"])
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    cfg.mkdir(parents=True)
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_AgrosStub]\n")
    sec = SCRATCH / "data/tilesets/secondary/agros"
    if (CFG / "tileset-manifest.json").exists() and BIN.exists():
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            shutil.copy2(CFG / f, cfg / f)
        shutil.copytree(BIN, sec / "porytiles_bin")
    else:
        # first build: Porytiles creates the tileset and appends its C
        # declarations to the scratch headers (the real ones are kept by hand)
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
            "# Per-tileset Porytiles config for gTileset_Agros, the countryside secondary.\n"
            "# Sources are drawn by tools/ichor/art/agros_build.py, which compiles Agros against\n"
            "# an empty stand-in primary and checks its metatiles use only its own tiles and\n"
            "# palettes 6-12. Pair it with aethos when compiling it directly.\n"
            "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n")


def verify(rows):
    raw = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = [(0x200 + i, hex(int(e))) for i, entries in enumerate(raw) for e in entries
           if not (int(e) & 0x3FF == 0 and int(e) >> 12 == 0)
           and (int(e) & 0x3FF < 512 or not (6 <= int(e) >> 12 <= 12))]
    if bad:
        sys.exit(f"agros_build: entries outside Agros's tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    # A door animation copies its frames into a secondary's tiles 504-511
    # (DOOR_TILE_START_SIZE1, src/field_door.c), so Agros keeps out of them:
    # it will serve rural maps with doors.
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    if used > TILE_LIMIT or late:
        sys.exit(f"agros_build: {used} tiles used and tiles {late[:8]} referenced; a secondary "
                 f"may use at most {TILE_LIMIT} (504-511 belong to door animations)")
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used")
    return used


def catalog(secs):
    data = []
    for name, structs in secs:
        for s in structs:
            data.append({
                "key": s.key, "title": s.title, "section": name, "w": s.w, "h": s.h,
                "ids": s.ids, "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
            })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps(data, indent=1))


def sheet(secs, rows, scale=2):
    """The numbered sheet: every metatile composited, its id above it."""
    from PIL import ImageDraw, ImageFont
    cell, lab, pad = 16 * scale, 10, 2
    img = Image.new("RGB", (8 * (cell + pad) + pad, rows * (cell + lab + pad) + pad), (40, 40, 48))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=9)
    for _, structs in secs:
        for s in structs:
            comp = composite(s)
            for j in range(s.h):
                for i in range(s.w):
                    mid = s.ids[j][i]
                    r, c = divmod(mid - 0x200, 8)
                    x, y = pad + c * (cell + pad), pad + r * (cell + lab + pad)
                    tile = Image.fromarray(comp[j * 16:j * 16 + 16, i * 16:i * 16 + 16])
                    img.paste(tile.resize((cell, cell), Image.NEAREST), (x, y + lab))
                    d.text((x + 1, y), f"{mid:03X}", fill=(230, 230, 200), font=font)
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    img.save(SHEET)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()
    secs = sections()
    allst = [s for _, ss in secs for s in ss]
    probs = validate(allst)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        preview(allst).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack([(SECTION_ROWS[n], ss) for n, ss in secs])
    write_sources(allst, rows, SRC)
    catalog(secs)
    sheet(secs, rows)
    write_labels(secs)
    if not args.no_compile:
        compile_tileset()
        used = verify(rows)
        import agros_catalog
        agros_catalog.main(secs, used)


if __name__ == "__main__":
    main()
