#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Eleusa, Eleusa Village's secondary.

1. Paints every structure: the fields (eleusa_fields), the farmyards
   (eleusa_farm), the house kit (eleusa_house), the sanctuary and the civic
   buildings (eleusa_sacred). Checks each 8x8 tile draws from one of the seven
   palette groups (eleusa_lib.GROUPS), then redraws tiles within 2 px of
   another as that tile, so near-duplicates are stored once.
2. Packs them into the 8-wide metatile sheet. Each section starts on a fixed
   row, so growing one never renumbers another. A structure wider than 8 is
   stored in 8-wide column chunks; its catalog grid is still whole.
3. Writes data/tilesets/secondary/eleusa/porytiles_src.
4. Compiles with Porytiles in a scratch project (build/eleusa_porytiles)
   against an empty stand-in primary, so Eleusa's own art uses only its own
   tiles and palettes 6-12.
5. Borrows aethos's ground: every cell drawn on grass, path or sea gets its
   bottom-layer tiles pointed at aethos's grass (0x001), path (0x1D9) or
   animated sea (0x170). Rebuild Eleusa whenever aethos is repainted.
6. Verifies every metatile entry and fails past TILE_LIMIT (504) tiles: the
   door animations own tiles 504-511. Writes build/eleusa/catalog.json, the
   metatile labels scripts swap, the sheet and piece images, and the catalog
   design/phase2/TILES_eleusa.md (eleusa_catalog.py).

Usage: /usr/bin/python3 tools/ichor/art/eleusa_build.py [--no-compile] [--preview out.png]
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
import eleusa_farm  # noqa: E402
import eleusa_fields  # noqa: E402
import eleusa_house  # noqa: E402
import eleusa_lib as E  # noqa: E402
import eleusa_sacred  # noqa: E402

ROOT = E.ROOT
NAME = "gTileset_Eleusa"
SRC = ROOT / "data/tilesets/secondary/eleusa/porytiles_src"
BIN = ROOT / "data/tilesets/secondary/eleusa/porytiles_bin"
CFG = ROOT / "porytiles/tilesets" / NAME
SCRATCH = ROOT / "build/eleusa_porytiles"
OUT = ROOT / "build/eleusa"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
IMG = ROOT / "design/phase2/img"
SHEET = IMG / "eleusa_sheet.png"
PIECES = IMG / "eleusa_pieces.png"
FRONTS = IMG / "eleusa_fronts.png"

COLS = 8
TILE_LIMIT = 504     # door animations copy their frames into tiles 504-511
NEAR_DUPLICATE_PX = 2

# First sheet row of each section (id = 0x200 + row * 8 + col).
SECTION_ROWS = {"fields": 0, "farm": 13, "houses": 18, "sanctuary": 26, "civic": 54}
SECTION_TITLES = {
    "fields": "Fields: wheat, stubble, sheaves and poppies",
    "farm": "Farmyards: threshing, winnowing, pithoi and the oven",
    "houses": "The house kit and courtyard walls",
    "sanctuary": "The sanctuary of the Mysteries",
    "civic": "Eleusa's Asclepeion and Agora",
}


def sections():
    return [("fields", eleusa_fields.build()), ("farm", eleusa_farm.build()),
            ("houses", eleusa_house.build()), ("sanctuary", eleusa_sacred.build()),
            ("civic", eleusa_sacred.build_civic())]


# --------------------------------------------------------------------------
# Packing: shelf-pack each section from its fixed row; wide structures are
# stored in 8-wide column chunks
# --------------------------------------------------------------------------

def pack(secs):
    """First-fit: each structure (or 8-wide chunk of one) takes the first free
    rectangle of the sheet, scanning rows from its section's start. Structures
    are placed in build order, so appending a new one never moves an old one."""
    used = np.zeros((64, COLS), bool)
    total = 0
    starts = sorted(SECTION_ROWS[n] for n, _ in secs)
    for name, structs in secs:
        start = SECTION_ROWS[name]
        end = start
        for s in structs:
            s.ids = [[None] * s.w for _ in range(s.h)]
            for c0 in range(0, s.w, COLS):
                cw = min(COLS, s.w - c0)
                spot = None
                for row in range(start, 64 - s.h + 1):
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
                        s.ids[y][c0 + x] = 0x200 + (row + y) * COLS + col + x
                end = max(end, row + s.h)
        later = [st for st in starts if st > start]
        if later:
            assert end <= min(later), f"section {name} overflows into row {min(later)} (ends {end})"
        print(f"  {name}: rows {start}-{end - 1}")
        total = max(total, end)
    return total


def write_sources(structs, rows):
    SRC.mkdir(parents=True, exist_ok=True)
    W, H = COLS * 16, rows * 16
    sheets = {ln: np.zeros((H, W, 4), np.uint8) for ln in ("bottom", "middle", "top")}
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
# Porytiles, in a scratch project with an empty stand-in primary
# --------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"eleusa_build: failed: {' '.join(map(str, cmd))}")
    return r


def palette_hints():
    """Our seven groups as Porytiles packing hints, so its palette search
    starts from the plan instead of searching from nothing."""
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in E.GROUPS.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = E.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


def scratch_project():
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
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_EleusaStub"])
    stub = SCRATCH / "data/tilesets/primary/eleusa_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_EleusaStub"])
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    cfg.mkdir(parents=True)
    pairing = "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_EleusaStub]\n"
    (cfg / "config.yaml").write_text(pairing)
    sec = SCRATCH / "data/tilesets/secondary/eleusa"
    if (CFG / "tileset-manifest.json").exists() and BIN.exists():
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            shutil.copy2(CFG / f, cfg / f)
        shutil.copytree(BIN, sec / "porytiles_bin")
    else:
        # first build: Porytiles creates the tileset, so the scratch copies of the
        # C tables must not already declare it (the real ones are kept by hand)
        import re
        for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                    "src/data/tilesets/metatiles.h"):
            p = SCRATCH / rel
            t = p.read_text()
            t = re.sub(r"const struct Tileset gTileset_Eleusa\s*=\s*\{.*?\};\n", "", t, flags=re.S)
            t = re.sub(r"const u16 gTilesetPalettes_PorytilesManaged_Eleusa\[\]\[16\]\s*=\s*\{.*?\};\n",
                       "", t, flags=re.S)
            t = "\n".join(line for line in t.split("\n")
                          if not re.search(r"PorytilesManaged_Eleusa(?!Stub)\b", line))
            p.write_text(t)
        run([pt, "create-tileset", "-C", str(SCRATCH), "--secondary", NAME])
        shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(SRC, sec / "porytiles_src")
    (cfg / "config.yaml").write_text(pairing + palette_hints())
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
        "# Per-tileset Porytiles config for gTileset_Eleusa, Eleusa Village's secondary.\n"
        "# Written by tools/ichor/art/eleusa_build.py, which compiles Eleusa against an\n"
        "# empty stand-in primary, then points its ground cells at aethos's grass, path\n"
        "# and sea. Pair it with aethos when compiling it directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + palette_hints())


NORMAL, COVERED, SPLIT = 0, 1, 2   # metatile layer types (attribute bits 12-15)


def borrow_ground(structs):
    """Give each ground cell aethos's ground tiles as its bottom layer (as
    akti_build.py does): the cell was compiled with an empty bottom, so find
    the layer Porytiles put its art in, and rebuild the cell as COVERED
    (ground under the middle layer) or SPLIT (ground under the top layer)."""
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
            meta[i, 0:4] = aethos[E.GROUND_METATILE[kind], 0:4]
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
                if e != int(aethos[E.GROUND_METATILE[patched[i]], j]):
                    bad.append((0x200 + i, j, "ground"))
                continue
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                continue
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"eleusa_build: entries outside Eleusa's tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{len(patched)} cells on aethos ground")
    if used > TILE_LIMIT or late:
        sys.exit(f"eleusa_build: {used} tiles and tiles {late[:8]} referenced; the door "
                 f"animations overwrite tiles {TILE_LIMIT}-511")
    return used


# --------------------------------------------------------------------------
# Catalog, labels, images
# --------------------------------------------------------------------------

LABELS = ROOT / "include/constants/metatile_labels.h"
LABEL_START = "// gTileset_Eleusa (Ichor: Eleusa Village), written by tools/ichor/art/eleusa_build.py"
LABEL_END = "// end gTileset_Eleusa"


def write_labels(secs):
    """The metatiles scripts swap in, as METATILE_Eleusa_* in metatile_labels.h,
    rewritten on every build so the ids never go stale."""
    want = {"torch_post": [("top_lit", "TorchPost_Lit"), ("top_cold", "TorchPost_Cold"),
                           ("foot", "TorchPost_Foot")]}
    lines = [LABEL_START]
    for _, structs in secs:
        for s in structs:
            for name, label in want.get(s.key, ()):
                cx, cy = s.names[name]
                lines.append(f"#define METATILE_Eleusa_{label:<24} 0x{s.ids[cy][cx]:03X}")
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
    fronts = {k: {**v, "ids": [[None if ref == "." else _ref_id(secs, ref) for ref in row]
                               for row in v["rows"]]}
              for k, v in eleusa_house.FRONTS.items()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps({"structures": data, "fronts": fronts}, indent=1))
    return data, fronts


def _ref_id(secs, ref):
    key, name = ref.split(".")
    for _, structs in secs:
        for s in structs:
            if s.key == key:
                cx, cy = s.names[name]
                return s.ids[cy][cx]
    raise KeyError(ref)


def images(secs):
    IMG.mkdir(parents=True, exist_ok=True)
    allst = [s for _, ss in secs for s in ss]
    E.preview(allst, scale=2, cols=4).save(PIECES)
    # the house fronts, composed from their parts
    houses = [s for n, ss in secs if n == "houses" for s in ss]
    from PIL import ImageDraw
    imgs = [(k, Image.fromarray(eleusa_house.front_image(houses, f["rows"])))
            for k, f in eleusa_house.FRONTS.items()]
    sc, pad = 3, 10
    row1, row2 = imgs[:4], imgs[4:]
    W = max(sum(i.width * sc + pad for _, i in r) for r in (row1, row2)) + pad
    H = sum(max(i.height for _, i in r) * sc + 22 for r in (row1, row2)) + pad
    out = Image.new("RGB", (W, H), (40, 40, 48))
    d = ImageDraw.Draw(out)
    y = pad
    for r in (row1, row2):
        x = pad
        for k, i in r:
            d.text((x, y), k, fill=(230, 230, 200))
            out.paste(i.resize((i.width * sc, i.height * sc), Image.NEAREST), (x, y + 12))
            x += i.width * sc + pad
        y += max(i.height for _, i in r) * sc + 22
    out.save(FRONTS)
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", "gTileset_Eleusa",
         "--primary", "aethos", "--scale", "2", "-o", str(SHEET)])
    for p in (SHEET, PIECES, FRONTS):
        print(p.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()
    secs = sections()
    allst = [s for _, ss in secs for s in ss]
    keys = [s.key for s in allst]
    assert len(keys) == len(set(keys)), "duplicate structure keys"
    probs = E.validate(allst)
    if not probs:
        before = len(E.tiles_of(allst))
        merges = E.merge_near_duplicates(allst, NEAR_DUPLICATE_PX)
        print(f"merged {len(merges)} near-duplicate tiles: {before} -> {len(E.tiles_of(allst))} tiles")
        probs = E.validate(allst)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        E.preview(allst, scale=2, cols=4).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack(secs)
    write_sources(allst, rows)
    catalog(secs)
    write_labels(secs)
    if not args.no_compile:
        compile_tileset()
        patched = borrow_ground(allst)
        used = verify(rows, patched)
        images(secs)
        import eleusa_catalog
        eleusa_catalog.main(used)


if __name__ == "__main__":
    main()
