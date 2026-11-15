#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Trophonios, Trophonios's cave.

A self-contained secondary on the aethos primary (it borrows no ground), for
MAP_TROPHONIOS_CAVE_B1F and _B2F. Steps, as kithairon_build.py:
1. Paint every structure (trophonios_kit.py, trophonios_props.py), check each
   8x8 tile draws from one palette group (trophonios_lib.GROUPS), and merge
   tiles within 2 px of each other.
2. Pack the sections into the 8-wide sheet, first fit, in order.
3. Write data/tilesets/secondary/trophonios/porytiles_src and compile it with
   Porytiles in a scratch project against an empty stand-in primary.
4. Verify every entry, fail past 504 tiles (door animations own 504-511), and
   write build/trophonios/catalog.json, the metatile labels scripts swap, the
   glow copy (glow/00-15.pal), the sheet and the catalog part of
   design/phase3/TILES_trophonios.md.

Usage: /usr/bin/python3 tools/ichor/art/trophonios_build.py [--no-compile]
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
import trophonios_kit  # noqa: E402
import trophonios_lib as T  # noqa: E402
import trophonios_props  # noqa: E402

ROOT = T.ROOT
OUT = ROOT / "build/trophonios"
IMG = ROOT / "design/phase3/img"
DIR = "trophonios"
SYMBOL = "gTileset_Trophonios"
LABEL = "Trophonios"
COLS = 8
TILE_LIMIT = 504
NEAR_DUPLICATE_PX = 2

# Metatiles scripts swap: (structure, cell name, label)
LABELS = [
    ("brazier", "cold_top", "Brazier_ColdTop"),
    ("brazier", "cold", "Brazier_Cold"),
    ("brazier", "lit_top", "Brazier_LitTop"),
    ("brazier", "lit", "Brazier_Lit"),
    ("cleft", "coils", "Cleft_Coils"),
    ("cleft", "empty", "Cleft_Empty"),
]

SECTIONS = [
    ("kit", ["floor", "pave", "ledge", "ford", "cap", "face", "water"]),
    ("props", ["brazier", "throne", "grille", "ladder", "stairs", "spring", "outlet", "sink",
               "pool", "hole", "prints", "cleft", "offerings", "tablets", "lamp", "rocks", "lair",
               "dig"]),
]
SECTION_TITLES = {"kit": "The kit: floor, paving, walls, the stream",
                  "props": "The furniture"}


def painted():
    ss = {}
    for mod in (trophonios_kit, trophonios_props):
        for s in mod.build():
            assert s.key not in ss, s.key
            ss[s.key] = s
    return ss


def sections(ss):
    return [(sec, [ss[k] for k in keys]) for sec, keys in SECTIONS]


def pack(secs):
    used = np.zeros((64, COLS), bool)
    ids = {}
    rows = 0
    for _, structs in secs:
        for s in structs:
            grid = [[None] * s.w for _ in range(s.h)]
            for c0 in range(0, s.w, COLS):
                cw = min(COLS, s.w - c0)
                spot = None
                for row in range(0, 64 - s.h + 1):
                    for col in range(0, COLS - cw + 1):
                        if not used[row:row + s.h, col:col + cw].any():
                            spot = (row, col)
                            break
                    if spot:
                        break
                assert spot, f"no room for {s.key}"
                row, col = spot
                used[row:row + s.h, col:col + cw] = True
                for y in range(s.h):
                    for x in range(cw):
                        grid[y][c0 + x] = 0x200 + (row + y) * COLS + col + x
                rows = max(rows, row + s.h)
            ids[s.key] = grid
    return ids, rows


def write_sources(src, secs, ids, rows):
    if src.exists():
        shutil.rmtree(src)
    src.mkdir(parents=True)
    sheets = {ln: np.zeros((rows * 16, COLS * 16, 4), np.uint8) for ln in ("bottom", "middle", "top")}
    beh = {}
    for _, structs in secs:
        for s in structs:
            g = ids[s.key]
            for cy in range(s.h):
                for cx in range(s.w):
                    i = g[cy][cx] - 0x200
                    r, c = divmod(i, COLS)
                    for ln in sheets:
                        sheets[ln][r * 16:r * 16 + 16, c * 16:c * 16 + 16] = \
                            s.layers[ln].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            for (x, y), mb in s.behaviors.items():
                if mb:
                    beh[g[y][x] - 0x200] = mb
    for ln, a in sheets.items():
        Image.fromarray(a, "RGBA").save(src / f"{ln}.png")
    (src / "attributes.csv").write_text(
        "\n".join(["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh)]) + "\n")


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"trophonios_build: failed: {' '.join(map(str, cmd))}")
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


def compile_set():
    scratch = ROOT / "build/trophonios_porytiles"
    src = ROOT / f"data/tilesets/secondary/{DIR}/porytiles_src"
    binp = ROOT / f"data/tilesets/secondary/{DIR}/porytiles_bin"
    cfg = ROOT / "porytiles/tilesets" / SYMBOL
    if scratch.exists():
        shutil.rmtree(scratch)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml"):
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    (scratch / "data/tilesets/primary").mkdir(parents=True)
    (scratch / "data/tilesets/secondary").mkdir(parents=True)
    pt = porytiles()
    stub_name = "gTileset_TrophStub"
    run([pt, "create-tileset", "-C", str(scratch), stub_name])
    stub = scratch / "data/tilesets/primary/troph_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(scratch), stub_name])
    scfg = scratch / "porytiles/tilesets" / SYMBOL
    scfg.mkdir(parents=True)
    pairing = f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [{stub_name}]\n"
    (scfg / "config.yaml").write_text(pairing)
    sec = scratch / f"data/tilesets/secondary/{DIR}"
    short = SYMBOL.replace("gTileset_", "")
    for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h"):
        p = scratch / rel
        t = p.read_text()
        t = re.sub(rf"const struct Tileset {SYMBOL}\s*=\s*\{{.*?\}};\n", "", t, flags=re.S)
        t = re.sub(rf"const u16 gTilesetPalettes_PorytilesManaged_{short}\[\]\[16\]\s*=\s*\{{.*?\}};\n",
                   "", t, flags=re.S)
        t = "\n".join(line for line in t.split("\n")
                      if not re.search(rf"PorytilesManaged_{short}\b", line))
        p.write_text(t)
    run([pt, "create-tileset", "-C", str(scratch), "--secondary", SYMBOL])
    shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(src, sec / "porytiles_src")
    (scfg / "config.yaml").write_text(pairing + palette_hints())
    r = run([pt, "compile-tileset", "-C", str(scratch), "--no-verify-checksums", SYMBOL])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-1500:])
    if binp.exists():
        shutil.rmtree(binp)
    shutil.copytree(sec / "porytiles_bin", binp)
    cfg.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        if (scfg / f).exists():
            shutil.copy2(scfg / f, cfg / f)
    (cfg / "config.yaml").write_text(
        f"# Per-tileset Porytiles config for {SYMBOL} (Trophonios's cave).\n"
        "# Written by tools/ichor/art/trophonios_build.py, which compiles it against an empty\n"
        "# stand-in primary: the set draws nothing from its primary. Pair it with aethos when\n"
        "# compiling it directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + palette_hints())
    return binp


def verify(binp, rows):
    raw = np.fromfile(binp / "metatiles.bin", "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = []
    for i, entries in enumerate(raw):
        for e in entries:
            e = int(e)
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                continue
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"trophonios_build: entries outside its tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(binp / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    print(f"{SYMBOL}: {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used")
    if used > TILE_LIMIT or late:
        sys.exit(f"trophonios_build: {used} tiles; door animations overwrite {TILE_LIMIT}-511")
    return used


def write_glow(binp):
    """The glow copy (SYSTEMS.md section 2): every color black but the chalk.
    For the engine's douse; not registered until the engine loads it."""
    glow = ROOT / f"data/tilesets/secondary/{DIR}/glow"
    if glow.exists():
        shutil.rmtree(glow)
    glow.mkdir(parents=True)
    bright = {T.C["ch1"]: (152, 248, 208), T.C["ch2"]: (216, 248, 232)}
    found = []
    for i in range(16):
        p = binp / "palettes" / f"{i:02d}.pal"
        lines = p.read_text().split("\n")
        cols = [tuple(int(v) for v in ln.split()) for ln in lines[3:19] if ln.strip()]
        out = []
        for j, c in enumerate(cols):
            if j and c in bright:
                out.append(bright[c])
                found.append((i, j))
            else:
                out.append((0, 0, 0))
        (glow / f"{i:02d}.pal").write_text(
            "JASC-PAL\n0100\n16\n" + "\n".join(f"{r} {g} {b}" for r, g, b in out) + "\n")
    return found


LABEL_FILE = ROOT / "include/constants/metatile_labels.h"
LABEL_START = "// gTileset_Trophonios (Ichor: Trophonios's cave), written by tools/ichor/art/trophonios_build.py"
LABEL_END = "// end gTileset_Trophonios"


def write_labels(ids, ss):
    lines = [LABEL_START]
    for key, cell, label in LABELS:
        cx, cy = ss[key].names[cell]
        lines.append(f"#define METATILE_{LABEL}_{label:<20} 0x{ids[key][cy][cx]:03X}")
    lines.append(LABEL_END)
    block = "\n".join(lines) + "\n"
    text = LABEL_FILE.read_text()
    if LABEL_START in text:
        a = text.index(LABEL_START)
        b = text.index(LABEL_END, a) + len(LABEL_END) + 1
        text = text[:a] + block + text[b:]
    else:
        end = text.rindex("#endif")
        text = text[:end] + block + "\n" + text[end:]
    LABEL_FILE.write_text(text)


def catalog(secs, ids):
    data = []
    for sec, structs in secs:
        for s in structs:
            data.append({
                "key": s.key, "title": s.title, "section": sec, "w": s.w, "h": s.h,
                "ids": ids[s.key], "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items() if mb},
            })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps({"symbol": SYMBOL, "structures": data}, indent=1))
    return data


def sheet():
    IMG.mkdir(parents=True, exist_ok=True)
    out = IMG / "tiles_trophonios_sheet.png"
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", SYMBOL,
         "--primary", "aethos", "--scale", "2", "-o", str(out)])
    return out


def preview(ss, path):
    """Every structure composited, for a quick look while painting."""
    pad = 4
    imgs = []
    for sec, keys in SECTIONS:
        for k in keys:
            s = ss[k]
            imgs.append(Image.fromarray(T.composite(s)).resize((s.w * 48, s.h * 48), Image.NEAREST))
    W = 8 * 48 + 2 * pad
    rows, x, y, rh = [], pad, pad, 0
    placed = []
    for im in imgs:
        if x + im.width > W - pad:
            x, y, rh = pad, y + rh + pad, 0
        placed.append((im, x, y))
        x += im.width + pad
        rh = max(rh, im.height)
    out = Image.new("RGB", (W, y + rh + pad), (255, 0, 255))
    for im, x, y in placed:
        out.paste(im, (x, y))
    out.save(path)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composite of every structure here")
    args = ap.parse_args()
    ss = painted()
    probs = T.validate(list(ss.values()))
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    if args.preview:
        print(preview(ss, args.preview))
    allst = list(ss.values())
    n0 = len(T.tiles_of(allst))
    T.merge_near_duplicates(allst, NEAR_DUPLICATE_PX)
    print(f"tiles: {n0} -> {len(T.tiles_of(allst))} after merging near duplicates")
    probs = T.validate(allst)
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    secs = sections(ss)
    ids, rows = pack(secs)
    print(f"{rows} sheet rows, {rows * 8} metatiles")
    write_sources(ROOT / f"data/tilesets/secondary/{DIR}/porytiles_src", secs, ids, rows)
    catalog(secs, ids)
    write_labels(ids, ss)
    if args.no_compile:
        return
    binp = compile_set()
    used = verify(binp, rows)
    glow = write_glow(binp)
    print(f"glow copy: chalk at {glow}")
    print(sheet().relative_to(ROOT))
    import trophonios_catalog
    trophonios_catalog.main(used, rows * 8, secs, ids, glow)


if __name__ == "__main__":
    main()
