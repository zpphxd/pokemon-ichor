#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_TempleDemeter, the Temple of Demeter's
underground megaron (the Lesser Mysteries' rite, SYSTEMS.md §12).

1. Paints every structure (temple_demeter_art.build()) and checks each 8x8
   tile draws from one of its palette groups.
2. Packs them first-fit into the 8-wide sheet from 0x200, in build order,
   and writes data/tilesets/secondary/temple_demeter/porytiles_src.
3. Compiles with Porytiles in a scratch project against an empty stand-in
   primary, so the temple uses only its own tiles and palettes 6-12 and works
   on any interior primary (it is meant for oikos).
4. The glow-paint: in the compiled palettes, sets each latent color to the
   stone it imitates (so the seeds and chalk vanish by torchlight), then writes
   the doused set, porytiles_bin/glow/NN.pal: black everywhere except the
   latent colors, which glow, and the flames. The engine loads it over
   palettes 6-12 when the torch is doused (SYSTEMS.md §2, "Douse").
5. Verifies every entry and the 504-tile limit, writes the metatile labels
   scripts swap, build/temple_demeter/catalog.json, the sheet and the catalog
   design/phase2/TILES_temple_demeter.md.

Usage: /usr/bin/python3 tools/ichor/art/temple_demeter_build.py [--no-compile]
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
import temple_demeter_art as T  # noqa: E402

ROOT = E.ROOT
NAME = "gTileset_TempleDemeter"
DIR = ROOT / "data/tilesets/secondary/temple_demeter"
SRC = DIR / "porytiles_src"
BIN = DIR / "porytiles_bin"
GLOW = BIN / "glow"
CFG = ROOT / "porytiles/tilesets" / NAME
SCRATCH = ROOT / "build/temple_demeter_porytiles"
OUT = ROOT / "build/temple_demeter"
IMG = ROOT / "design/phase2/img"
SHEET = IMG / "temple_demeter_sheet.png"
PIECES = IMG / "temple_demeter_pieces.png"
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
    # cells no structure uses get plain floor, so every bottom stays opaque
    filler = T.Layer(16, 16)
    T.floor(filler, 0, 0)
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
        sys.exit(f"temple_demeter_build: failed: {' '.join(map(str, cmd))}")
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
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_TempleDemeterStub"])
    stub = SCRATCH / "data/tilesets/primary/temple_demeter_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_TempleDemeterStub"])
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    cfg.mkdir(parents=True)
    pairing = ("tileset:\n  primary_pairing:\n    mode: manual\n"
               "    partners: [gTileset_TempleDemeterStub]\n")
    (cfg / "config.yaml").write_text(pairing)
    sec = SCRATCH / "data/tilesets/secondary/temple_demeter"
    if (CFG / "tileset-manifest.json").exists() and BIN.exists():
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            shutil.copy2(CFG / f, cfg / f)
        shutil.copytree(BIN, sec / "porytiles_bin", ignore=shutil.ignore_patterns("glow"))
    else:
        # first build: the scratch C tables must not already declare the tileset
        for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                    "src/data/tilesets/metatiles.h"):
            p = SCRATCH / rel
            t = p.read_text()
            t = re.sub(r"const struct Tileset gTileset_TempleDemeter\s*=\s*\{.*?\};\n", "", t, flags=re.S)
            t = re.sub(r"const u16 gTilesetPalettes_PorytilesManaged_TempleDemeter(Glow)?\[\]\[16\]\s*=\s*\{.*?\};\n",
                       "", t, flags=re.S)
            t = "\n".join(line for line in t.split("\n")
                          if not re.search(r"PorytilesManaged_TempleDemeter(?!Stub)", line))
            p.write_text(t)
        run([pt, "create-tileset", "-C", str(SCRATCH), "--secondary", NAME])
        shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(SRC, sec / "porytiles_src")
    (cfg / "config.yaml").write_text(pairing + palette_hints())
    r = run([pt, "compile-tileset", "-C", str(SCRATCH), "--no-verify-checksums", NAME])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if BIN.exists():
        shutil.rmtree(BIN)     # glow/ is rewritten by glow_palettes()
    shutil.copytree(sec / "porytiles_bin", BIN)
    CFG.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        shutil.copy2(SCRATCH / "porytiles/tilesets" / NAME / f, CFG / f)
    (CFG / "config.yaml").write_text(
        "# Per-tileset Porytiles config for gTileset_TempleDemeter, the Temple of Demeter's\n"
        "# underground megaron. Written by tools/ichor/art/temple_demeter_build.py, which\n"
        "# compiles it against an empty stand-in primary: it uses only its own tiles and\n"
        "# palettes 6-12, so it works on any primary. Pair it with oikos directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Oikos]\n"
        + palette_hints())


# --------------------------------------------------------------------------
# The glow-paint palettes
# --------------------------------------------------------------------------

def read_pal(p):
    vals = [int(v) for v in p.read_text().split()[3:]]
    return [tuple(vals[i * 3:i * 3 + 3]) for i in range(len(vals) // 3)]


def write_pal(p, cols):
    # .pal files are CRLF in this repo (.gitattributes), as Porytiles writes them
    p.write_bytes(("JASC-PAL\r\n0100\r\n16\r\n" + "".join(f"{r} {g} {b}\r\n" for r, g, b in cols)).encode())


def glow_palettes():
    """Normalize the latent colors to their stone, and write the doused set."""
    GLOW.mkdir(parents=True, exist_ok=True)
    latent = {T.C[n]: n for n in T.LATENT}
    flames = {T.C[n] for n in T.FLAMES}
    found = {}
    for i in range(16):
        p = BIN / "palettes" / f"{i:02d}.pal"
        cols = read_pal(p)
        glow = [(0, 0, 0)] * 16
        if 6 <= i <= 12:
            for k, c in enumerate(cols):
                if k == 0:
                    continue
                if c in latent:
                    n = latent[c]
                    glow[k] = T.LATENT[n]
                    cols[k] = T.C[T.LATENT_BASE[n]]
                    found.setdefault(n, []).append((i, k))
                elif c in flames:
                    glow[k] = c
            write_pal(p, cols)
        glow[0] = cols[0]
        write_pal(GLOW / f"{i:02d}.pal", glow)
    for n in T.LATENT:
        assert n in found, f"latent color {n} not in any palette"
    print("glow-paint at (palette, index):", found)
    return found


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
        sys.exit(f"temple_demeter_build: entries outside its tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used")
    if used > TILE_LIMIT or late:
        sys.exit(f"temple_demeter_build: {used} tiles; tiles {TILE_LIMIT}-511 belong to the doors")
    return used


LABELS = ROOT / "include/constants/metatile_labels.h"
LABEL_START = ("// gTileset_TempleDemeter (Ichor: the Lesser Mysteries), written by "
               "tools/ichor/art/temple_demeter_build.py")
LABEL_END = "// end gTileset_TempleDemeter"
WANT = [
    ("braziers", [("top_cold", "BrazierTop_Cold"), ("top_lit", "BrazierTop_Lit"),
                  ("vestibule_cold", "BrazierVestibule_Cold"), ("vestibule_lit", "BrazierVestibule_Lit"),
                  ("spring_cold", "BrazierSpring_Cold"), ("spring_lit", "BrazierSpring_Lit"),
                  ("summer_cold", "BrazierSummer_Cold"), ("summer_lit", "BrazierSummer_Lit"),
                  ("autumn_cold", "BrazierAutumn_Cold"), ("autumn_lit", "BrazierAutumn_Lit"),
                  ("winter_cold", "BrazierWinter_Cold"), ("winter_lit", "BrazierWinter_Lit")]),
    ("glow", [("l0", "Glow_L0"), ("r0", "Glow_R0"), ("l1", "Glow_L1"), ("r1", "Glow_R1"),
              ("bl", "Glow_BL"), ("b", "Glow_B"), ("br", "Glow_BR"), ("pool", "Glow_Pool")]),
    ("floor", [("floor", "Floor"), ("seed", "Floor_Seed"), ("seeds", "Floor_Seeds")]),
    ("wall_lights", [("sconce_cold", "Sconce_Cold"), ("sconce_lit", "Sconce_Lit"),
                     ("niche_cold", "Niche_Cold"), ("niche_lit", "Niche_Lit"),
                     ("floor_sconce", "Floor_UnderSconce"), ("lower_lit", "WallLower_Lit"),
                     ("frieze_lit", "Frieze_Lit"),
                     ("door_top_painted", "PaintedDoorTop"), ("door_top_open", "PaintedDoorTop_Open"),
                     ("door_bottom_painted", "PaintedDoorBottom"),
                     ("door_bottom_open", "PaintedDoorBottom_Open")]),
    ("wall", [("lower", "WallLower")]),
    ("frieze", [("key", "Frieze_Key")]),
    ("columns", [("torch_cold", "ColumnTorch_Cold"), ("torch_lit", "ColumnTorch_Lit"),
                 ("bottom", "ColumnBottom"), ("bottom_lit", "ColumnBottom_Lit")]),
    ("vessels", [("lamp_cold", "Lamp_Cold"), ("lamp_lit", "Lamp_Lit"), ("altar_ear", "Altar_Ear")]),
    ("dais", [("altar_empty", "Altar_Empty")]),
    ("partition", [("door_draught", "DraughtDoor_A"), ("door_draught_b", "DraughtDoor_B")]),
]


def write_labels(structs):
    by = {s.key: s for s in structs}
    lines = [LABEL_START]
    for key, items in WANT:
        s = by[key]
        for name, label in items:
            cx, cy = s.names[name]
            lines.append(f"#define METATILE_TempleDemeter_{label:<24} 0x{s.ids[cy][cx]:03X}")
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
    } for s in structs]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps({"structures": data}, indent=1))


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
    write_labels(structs)
    if args.no_compile:
        return
    compile_tileset()
    glow_palettes()
    n = verify(rows)
    IMG.mkdir(parents=True, exist_ok=True)
    E.preview(structs, scale=2, cols=3).save(PIECES)
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", NAME,
         "--primary", "oikos", "--scale", "2", "-o", str(SHEET)])
    import temple_demeter_catalog
    temple_demeter_catalog.main(n)


if __name__ == "__main__":
    main()
