#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_TempleArtemis, the Temple of Artemis at Arkadia, the
goddess's night garden (the Hunt for the Hind, SYSTEMS.md §12; design/phase3/SCRIPT.md
beat 44 and Part 5).

1. Paints every structure (temple_artemis_art.build()) and checks each 8x8 tile
   draws from one of its palette groups, that no cell uses three layers, and that
   nothing has holes under the sprite layer.
2. Packs them first-fit into the 8-wide sheet from 0x200, in build order, and writes
   data/tilesets/secondary/temple_artemis/porytiles_src.
3. Compiles with Porytiles in a scratch project against an empty stand-in primary,
   so the temple uses only its own tiles and palettes 6-12 and works on any interior
   primary (it is meant for oikos).
4. Verifies every entry and the 504-tile limit, writes the metatile labels the
   trial's scripts swap, build/temple_artemis/catalog.json, the sheet, the pieces
   image and the catalog part of design/phase3/TILES_temple_artemis.md.

Usage: /usr/bin/python3 tools/ichor/art/temple_artemis_build.py [--no-compile]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eleusa_lib as E  # noqa: E402
import temple_artemis_art as T  # noqa: E402

ROOT = E.ROOT
NAME = "gTileset_TempleArtemis"
STUB = "gTileset_TempleArtemisStub"
DIR = ROOT / "data/tilesets/secondary/temple_artemis"
SRC = DIR / "porytiles_src"
BIN = DIR / "porytiles_bin"
CFG = ROOT / "porytiles/tilesets" / NAME
SCRATCH = ROOT / "build/temple_artemis_porytiles"
OUT = ROOT / "build/temple_artemis"
IMG = ROOT / "design/phase3/img"
SHEET = IMG / "temple_artemis_sheet.png"
PIECES = IMG / "temple_artemis_pieces.png"
DOC = ROOT / "design/phase3/TILES_temple_artemis.md"
COLS = 8
TILE_LIMIT = 504


def pack(structs):
    used = np.zeros((64, COLS), bool)
    end = 0
    for s in structs:
        assert s.w <= COLS, s.key
        s.ids = [[None] * s.w for _ in range(s.h)]
        spot = None
        for row in range(0, 64 - s.h + 1):
            for col in range(0, COLS - s.w + 1):
                if not used[row:row + s.h, col:col + s.w].any():
                    spot = (row, col)
                    break
            if spot:
                break
        assert spot, f"no room for {s.key}"
        row, col = spot
        used[row:row + s.h, col:col + s.w] = True
        for y in range(s.h):
            for x in range(s.w):
                s.ids[y][x] = 0x200 + (row + y) * COLS + col + x
        end = max(end, row + s.h)
    return end, used


def write_sources(structs, rows, used):
    SRC.mkdir(parents=True, exist_ok=True)
    W, H = COLS * 16, rows * 16
    sheets = {ln: np.zeros((H, W, 4), np.uint8) for ln in ("bottom", "middle", "top")}
    # cells no structure uses get plain boards, so every bottom stays opaque
    filler = T.Layer(16, 16)
    T.lawn(filler, 0, 0)
    for r in range(rows):
        for c in range(COLS):
            if not used[r, c]:
                sheets["bottom"][r * 16:r * 16 + 16, c * 16:c * 16 + 16] = filler.a
    beh = {}
    for s in structs:
        for cy in range(s.h):
            for cx in range(s.w):
                i = s.ids[cy][cx] - 0x200
                r, c = divmod(i, COLS)
                for ln in sheets:
                    sheets[ln][r * 16:r * 16 + 16, c * 16:c * 16 + 16] = \
                        s.layers[ln].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
        for (x, y), mb in s.behaviors.items():
            beh[s.ids[y][x] - 0x200] = mb
    for ln, a in sheets.items():
        Image.fromarray(a, "RGBA").save(SRC / f"{ln}.png")
    lines = ["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh)]
    (SRC / "attributes.csv").write_text("\n".join(lines) + "\n")


# --------------------------------------------------------------------------
# Porytiles
# --------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"temple_artemis_build: failed: {' '.join(map(str, cmd))}")
    return r


def palette_hints():
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in T.GROUPS.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = T.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


def compile_tileset():
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
    run([pt, "create-tileset", "-C", str(SCRATCH), STUB])
    stub = SCRATCH / "data/tilesets/primary/temple_artemis_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), STUB])
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    cfg.mkdir(parents=True)
    pairing = ("tileset:\n  primary_pairing:\n    mode: manual\n"
               f"    partners: [{STUB}]\n")
    (cfg / "config.yaml").write_text(pairing)
    sec = SCRATCH / "data/tilesets/secondary/temple_artemis"
    if (CFG / "tileset-manifest.json").exists() and BIN.exists():
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            shutil.copy2(CFG / f, cfg / f)
        shutil.copytree(BIN, sec / "porytiles_bin")
    else:
        # first build: the scratch C tables must not already declare the tileset
        for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                    "src/data/tilesets/metatiles.h"):
            p = SCRATCH / rel
            t = p.read_text()
            t = re.sub(r"const struct Tileset gTileset_TempleArtemis\s*=\s*\{.*?\};\n", "", t, flags=re.S)
            t = re.sub(r"const u16 gTilesetPalettes_PorytilesManaged_TempleArtemis\[\]\[16\]\s*=\s*\{.*?\};\n",
                       "", t, flags=re.S)
            t = "\n".join(line for line in t.split("\n")
                          if not re.search(r"PorytilesManaged_TempleArtemis(?!Stub)", line))
            p.write_text(t)
        run([pt, "create-tileset", "-C", str(SCRATCH), "--secondary", NAME])
        shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(SRC, sec / "porytiles_src")
    (cfg / "config.yaml").write_text(pairing + palette_hints())
    r = run([pt, "compile-tileset", "-C", str(SCRATCH), "--no-verify-checksums", NAME])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if BIN.exists():
        shutil.rmtree(BIN)
    shutil.copytree(sec / "porytiles_bin", BIN)
    CFG.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        shutil.copy2(SCRATCH / "porytiles/tilesets" / NAME / f, CFG / f)
    (CFG / "config.yaml").write_text(
        "# Per-tileset Porytiles config for gTileset_TempleArtemis, the Temple of Artemis at\n"
        "# Arkadia. Written by tools/ichor/art/temple_artemis_build.py, which compiles it\n"
        "# against an empty stand-in primary: it uses only its own tiles and palettes 6-12,\n"
        "# so it works on any primary. Pair it with oikos directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Oikos]\n"
        + palette_hints())


# --------------------------------------------------------------------------
# Verify, labels, catalog
# --------------------------------------------------------------------------

def verify(rows):
    raw = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8
    bad = [(0x200 + i, hex(int(e))) for i, entries in enumerate(raw) for e in entries
           if not (int(e) & 0x3FF == 0 and int(e) >> 12 == 0)
           and (int(e) & 0x3FF < 512 or not (6 <= int(e) >> 12 <= 12))]
    if bad:
        sys.exit(f"temple_artemis_build: entries outside its tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used")
    if used > TILE_LIMIT or late:
        sys.exit(f"temple_artemis_build: {used} tiles; tiles {TILE_LIMIT}-511 belong to the doors")
    return used


LABELS = ROOT / "include/constants/metatile_labels.h"
LABEL_START = ("// gTileset_TempleArtemis (Ichor: the Hunt for the Hind), written by "
               "tools/ichor/art/temple_artemis_build.py")
LABEL_END = "// end gTileset_TempleArtemis"
WANT = [
    ("gates", [("hedge_l", "StairHedge_L"), ("hedge_lowered_l", "StairHedge_Lowered_L"),
               ("hedge_r", "StairHedge_R"), ("hedge_lowered_r", "StairHedge_Lowered_R"),
               ("gate_top", "GateTop"), ("gate_top_open", "GateTop_Open"),
               ("gate", "Gate"), ("gate_open", "Gate_Open")]),
]


def write_labels(structs):
    by = {s.key: s for s in structs}
    lines = [LABEL_START]
    for key, items in WANT:
        s = by[key]
        for name, label in items:
            cx, cy = s.names[name]
            lines.append(f"#define METATILE_TempleArtemis_{label:<22} 0x{s.ids[cy][cx]:03X}")
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


def catalog(structs):
    data = [{
        "key": s.key, "title": s.title, "w": s.w, "h": s.h, "ids": s.ids, "walk": s.walk,
        "notes": s.notes, "names": {k: list(v) for k, v in s.names.items()},
        "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
        "top": [[bool((s.T.a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16][..., 3] > 0).any())
                 for cx in range(s.w)] for cy in range(s.h)],
    } for s in structs]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps({"structures": data}, indent=1))


CAT_START = "<!-- catalog: written by tools/ichor/art/temple_artemis_build.py; do not edit by hand -->"
CAT_END = "<!-- end of catalog -->"


def write_doc(structs, used_tiles):
    out = [CAT_START, "", "## Catalog", "",
           f"{sum(s.w * s.h for s in structs)} metatiles from 0x200; **{used_tiles} of "
           f"{TILE_LIMIT} tiles used** (the door animations own 504-511). Walk codes: `X` "
           "blocks, `.` walkable, `T` walkable and drawn over the player, `S` "
           "MB_SOUTH_ARROW_WARP (the doormat). Every other metatile is MB_NORMAL; the "
           "hunt is all objects and script.", ""]
    for s in structs:
        out.append(f"### {s.title}")
        out.append("")
        out.append(f"`{s.key}`, {s.w} wide by {s.h} tall. {s.notes}")
        out.append("")
        out.append("```text")
        out.append("ids" + " " * (6 * s.w - 3) + "   walk")
        for y in range(s.h):
            ids = " ".join(f"0x{v:03X}" for v in s.ids[y])
            out.append(f"{ids}   {' '.join(s.walk[y])}")
        out.append("```")
        out.append("")
        if s.names:
            parts = []
            for n, (cx, cy) in sorted(s.names.items(), key=lambda kv: s.ids[kv[1][1]][kv[1][0]]):
                parts.append(f"`{n}` 0x{s.ids[cy][cx]:03X}")
            out.append("Pieces: " + ", ".join(parts) + ".")
            out.append("")
    out.append(CAT_END)
    block = "\n".join(out)
    if DOC.exists():
        text = DOC.read_text()
        if CAT_START in text and CAT_END in text:
            a = text.index(CAT_START)
            b = text.index(CAT_END) + len(CAT_END)
            text = text[:a] + block + text[b:]
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
    else:
        text = "# Temple of Artemis tileset: `temple_artemis`\n\n" + block + "\n"
    DOC.write_text(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    structs = T.build()
    probs = E.validate(structs, T.GROUP_RGB)
    if not probs:
        before = len(E.tiles_of(structs))
        merges = E.merge_near_duplicates(structs, 2)
        print(f"merged {len(merges)} near-duplicate tiles: {before} -> {len(E.tiles_of(structs))}")
        probs = E.validate(structs, T.GROUP_RGB)
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    rows, used = pack(structs)
    write_sources(structs, rows, used)
    catalog(structs)
    IMG.mkdir(parents=True, exist_ok=True)
    E.preview(structs, scale=2, cols=3).save(PIECES)
    if args.no_compile:
        print(f"{len(E.tiles_of(structs))} distinct tiles (before Porytiles); {rows} sheet rows")
        return
    write_labels(structs)
    compile_tileset()
    n = verify(rows)
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", NAME,
         "--primary", "oikos", "--scale", "2", "-o", str(SHEET)])
    write_doc(structs, n)


if __name__ == "__main__":
    main()
