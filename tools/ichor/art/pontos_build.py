#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Pontos, the Black Sea's outdoor secondary.

The pipeline is emporion_build.py's, with one addition: the Pontic sea.

1. Draws every structure (pontos_art.build()) and checks each 8x8 tile draws
   from one of the six palette groups; near-duplicate tiles are merged.
2. Packs them into the 8-wide sheet from 0x200, section by section.
3. Writes data/tilesets/secondary/pontos/porytiles_src.
4. Compiles with Porytiles in a scratch project under build/ against an empty
   stand-in primary, telling Porytiles the secondary has six palettes (6-11) so
   palette 12 stays free.
5. Writes palette 12, the Pontic sea: aethos's sea palette with its blues turned
   dark green (pontos_lib.PONTIC). Then points every cell on borrowed ground at
   aethos's metatile (grass 0x001, sand 0x124, path 0x1D9, tall grass 0x00D, and
   the sea 0x170 with palette 5 re-pointed at 12), and fills each derived piece
   with its aethos water metatile, re-pointed the same way. aethos's water
   animation runs in those tiles, so the Black Sea moves for no tiles at all.
   Rebuild whenever aethos is repainted.
6. Verifies every entry and fails past TILE_LIMIT (504) tiles. Writes
   build/pontos/catalog.json and coast_index.json (read by the map builders), the
   sheet and pieces images, and design/oikoumene/TILES_pontos.md.

Usage: /usr/bin/python3 tools/ichor/art/pontos_build.py [--no-compile] [--preview out.png]
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pontos_lib as P  # noqa: E402
from kalliste_lib import pack, write_sources  # noqa: E402

ROOT = P.ROOT
SYMBOL = "gTileset_Pontos"
DIR = "pontos"
SRC = ROOT / f"data/tilesets/secondary/{DIR}/porytiles_src"
BIN = ROOT / f"data/tilesets/secondary/{DIR}/porytiles_bin"
CFG = ROOT / f"porytiles/tilesets/{SYMBOL}"
SCRATCH = ROOT / f"build/{DIR}_porytiles"
OUT = ROOT / f"build/{DIR}"
IMG = ROOT / "design/oikoumene/img"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
TILE_LIMIT = 504
NEAR_DUPLICATE_PX = 2
NORMAL, COVERED, SPLIT = 0, 1, 2


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"pontos_build: failed: {' '.join(map(str, cmd))}")
    return r


def hints_yaml():
    y = "  palettes:\n    packing:\n      hints_enabled: true\n      hints:\n"
    for g, names in P.GROUPS.items():
        y += f"        - name: {g}\n          colors:\n"
        for n in names:
            r, gg, b = P.C[n]
            y += f"            - [{r}, {gg}, {b}]\n"
    return y


def scratch_project():
    S = SCRATCH
    if S.exists():
        shutil.rmtree(S)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml", "data/layouts/layouts.json"):
        dst = S / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    # six secondary palettes for Porytiles (6-11): palette 12 is the Pontic sea
    fm = S / "include/fieldmap.h"
    fm.write_text(re.sub(r"#define NUM_PALS_TOTAL \d+", "#define NUM_PALS_TOTAL 12", fm.read_text()))
    short = SYMBOL.replace("gTileset_", "")
    for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h"):
        p = S / rel
        t = p.read_text()
        t = re.sub(rf"const struct Tileset {SYMBOL} =\s*\{{.*?\}};", "", t, flags=re.S)
        t = re.sub(rf"const u16 gTilesetPalettes_PorytilesManaged_{short}\[\]\[16\] =\s*\{{.*?\}};",
                   "", t, flags=re.S)
        t = re.sub(rf"const u\d+ g\w+_PorytilesManaged_{short}\[\] = [^\n]*\n", "", t)
        p.write_text(t)
    (S / "data/tilesets/primary").mkdir(parents=True)
    (S / "data/tilesets/secondary").mkdir(parents=True)
    pt = porytiles()
    stub_name = f"{SYMBOL}Stub"
    run([pt, "create-tileset", "-C", S, stub_name])
    stubdir = next((S / "data/tilesets/primary").iterdir())
    stub = stubdir / "porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    from PIL import Image
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", S, stub_name])
    run([pt, "create-tileset", SYMBOL, "-C", S, "--secondary",
         "--primary-pairing-mode", "manual", "--primary-pairing-partners", stub_name])
    sec = S / f"data/tilesets/secondary/{DIR}"
    assert sec.exists(), f"porytiles made no {sec}"
    cfg = S / f"porytiles/tilesets/{SYMBOL}"
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [" + stub_name + "]\n" + hints_yaml())
    if (sec / "porytiles_src").exists():
        shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(SRC, sec / "porytiles_src")
    return sec


def compile_tileset():
    sec = scratch_project()
    r = run([porytiles(), "compile-tileset", "-C", SCRATCH, "--no-verify-checksums", SYMBOL])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if BIN.exists():
        shutil.rmtree(BIN)
    shutil.copytree(sec / "porytiles_bin", BIN)
    CFG.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        p = SCRATCH / f"porytiles/tilesets/{SYMBOL}/{f}"
        if p.exists():
            shutil.copy2(p, CFG / f)
    (CFG / "config.yaml").write_text(
        "# Written by tools/ichor/art/pontos_build.py; edit it there. The build compiles in a\n"
        "# scratch project with six secondary palettes: palette 12 is the Pontic sea, written\n"
        "# by the build, never packed.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n" + hints_yaml())


def write_sea_palette():
    """Palette 12 = the Pontic sea; every other unused slot stays as Porytiles left it."""
    pal = P.pontic_palette()
    lines = ["JASC-PAL", "0100", "16"] + [f"{r} {g} {b}" for (r, g, b) in pal]
    pdir = BIN / "palettes"
    (pdir / f"{P.SEA_SLOT:02d}.pal").write_text("\n".join(lines) + "\n")
    for n in range(16):
        f = pdir / f"{n:02d}.pal"
        if not f.exists():
            f.write_text("JASC-PAL\n0100\n16\n" + "0 0 0\n" * 16)


# --------------------------------------------------------------------------
# Near-duplicate merging (as emporion_build.py)
# --------------------------------------------------------------------------

def _flips(t):
    return (t, t[:, ::-1], t[::-1, :], t[::-1, ::-1])


def _tiles(structs):
    occ = {}
    for s in structs:
        if s.derived is not None:
            continue
        gr = s.borrowed
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in gr:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    occ.setdefault(min(v.tobytes() for v in _flips(t)), []).append((layer, tx, ty))
    return occ


def merge_near_duplicates(structs, limit=NEAR_DUPLICATE_PX):
    occ = _tiles(structs)
    keys = list(occ)
    if not keys:
        return []
    arr = {k: np.frombuffer(k, np.uint8).reshape(8, 8, 4) for k in keys}
    flat = np.stack([arr[k].reshape(64, 4) for k in keys])
    pairs = []
    for i, k in enumerate(keys):
        best = None
        for v in _flips(arr[k]):
            d = (flat != v.reshape(1, 64, 4)).any(-1).sum(-1)
            best = d if best is None else np.minimum(best, d)
        for j in np.nonzero(best <= limit)[0]:
            if j > i:
                pairs.append((int(best[j]), i, int(j)))
    pairs.sort()
    dropped, kept, merges = set(), set(), []
    for d, i, j in pairs:
        a, b = keys[i], keys[j]
        if a in dropped or b in dropped:
            continue
        keep, drop = (a, b) if len(occ[a]) >= len(occ[b]) else (b, a)
        if drop in kept:
            keep, drop = drop, keep
            if drop in kept:
                continue
        for (layer, tx, ty) in occ[drop]:
            cur = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = min(
                _flips(arr[keep]), key=lambda v: int((cur != v).any(-1).sum()))
        dropped.add(drop)
        kept.add(keep)
        merges.append(d)
    return merges


# --------------------------------------------------------------------------
# After the compile: the borrowed ground and the derived sea
# --------------------------------------------------------------------------

def patch(structs):
    meta = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(BIN / "metatile_attributes.bin", "<u2")
    patched = {}
    for s in structs:
        if s.derived is not None:
            for cy, row in enumerate(s.derived):
                for cx, mid in enumerate(row):
                    i = s.ids[cy][cx] - 0x200
                    meta[i] = P.aethos_entries(mid, pontic=True)
                    attrs[i] = P.aethos_attr(mid)
                    patched[i] = ("derived", mid)
            continue
        for (cx, cy), kind in s.borrowed.items():
            i = s.ids[cy][cx] - 0x200
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            on_top = bool((s.T.a[sl][..., 3] > 0).any())
            lt = int(attrs[i]) >> 12
            ent = [int(e) for e in meta[i]]
            art = ent[4:8] if any(ent[4:8]) else ent[0:4]
            if on_top and lt == NORMAL:
                art = ent[4:8]
            ground = P.aethos_entries(P.GROUND_METATILE[kind], pontic=(kind == "psea"))
            meta[i, 0:4] = ground[0:4]
            meta[i, 4:8] = art
            beh = int(attrs[i]) & 0x0FFF
            attrs[i] = beh | ((SPLIT if on_top else COVERED) << 12)
            patched[i] = ("ground", kind)
    meta.astype("<u2").tofile(BIN / "metatiles.bin")
    attrs.astype("<u2").tofile(BIN / "metatile_attributes.bin")
    return patched


def verify(rows, patched):
    raw = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = []
    for i, entries in enumerate(raw):
        if not any(int(e) for e in entries):
            continue
        what = patched.get(i)
        for j, e in enumerate(entries):
            e = int(e)
            tile, pal = e & 0x3FF, e >> 12
            if what and (what[0] == "derived" or j < 4):
                if tile >= 512:
                    bad.append((hex(0x200 + i), j, "aethos entry points past the primary"))
                continue
            if tile == 0 and pal == 0:
                continue
            if tile < 512 or not (6 <= pal <= 11):
                bad.append((hex(0x200 + i), hex(e)))
    if bad:
        sys.exit(f"pontos_build: entries outside pontos's tiles/palettes 6-11: {bad[:10]}")
    from PIL import Image
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{sum(1 for v in patched.values() if v[0] == 'ground')} cells on aethos ground, "
          f"{sum(1 for v in patched.values() if v[0] == 'derived')} derived sea pieces")
    if used > TILE_LIMIT:
        sys.exit(f"pontos_build: {used} tiles; the door animations overwrite tiles {TILE_LIMIT}-511")
    return used


def behavior_names():
    txt = (ROOT / "include/constants/metatile_behaviors.h").read_text()
    out, v = {}, 0
    for name, val in re.findall(r"^\s*(MB_\w+)\s*(?:=\s*(\w+))?\s*,", txt, re.M):
        if val:
            v = int(val, 0)
        out[v] = name
        v += 1
    return out


def catalog_json(structs, index):
    mb = behavior_names()
    data = []
    for s in structs:
        beh = {f"{x},{y}": b for (x, y), b in s.behaviors.items()}
        if s.derived is not None:
            for cy, row in enumerate(s.derived):
                for cx, mid in enumerate(row):
                    beh[f"{cx},{cy}"] = mb.get(P.aethos_attr(mid) & 0xFF, "?")
        data.append({
            "key": s.key, "title": s.title, "section": s.section, "w": s.w, "h": s.h,
            "ids": s.ids, "walk": s.walk, "notes": s.notes, "behaviors": beh,
            "ground": {f"{x},{y}": g for (x, y), g in sorted(s.ground.items())},
            "names": {n: list(c) for n, c in s.names.items()},
            "derived": s.derived,
        })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps(data, indent=1))
    (OUT / "coast_index.json").write_text(json.dumps(index, indent=1, sort_keys=True))


def images(structs):
    IMG.mkdir(parents=True, exist_ok=True)
    P.preview([s for s in structs if s.section != "coast"], scale=2, cols=5).save(IMG / "pontos_pieces.png")
    run([sys.executable, ROOT / "tools/ichor/render_map.py", "--sheet", f"data/tilesets/secondary/{DIR}",
         "--primary", "aethos", "--scale", "2", "-o", IMG / "pontos_sheet.png"])


def palette_report():
    pals = []
    for i in range(6, 13):
        p = BIN / "palettes" / f"{i:02d}.pal"
        v = [int(t) for t in p.read_text().split()[3:]]
        cols = {tuple(v[k * 3:k * 3 + 3]) for k in range(1, 16)}
        cols.discard((0, 0, 0))
        pals.append(len(cols))
    return pals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()

    import pontos_art
    sections = pontos_art.build()
    index = pontos_art.build.index
    structs = [s for _, ss in sections for s in ss]
    keys = [s.key for s in structs]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, f"duplicate structure keys {dup}"
    probs = P.validate(structs)
    if not probs:
        before = len(_tiles(structs))
        merges = merge_near_duplicates(structs)
        print(f"merged {len(merges)} near-duplicate tiles: {before} -> {len(_tiles(structs))} "
              f"distinct tiles before palette sharing")
        probs = P.validate(structs)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        P.preview(structs, scale=2, cols=5).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack(sections)
    assert rows <= pontos_art.BATCH2_ROW, f"{rows} sheet rows: batch 1 runs into batch 2's rows"
    write_sources(structs, rows, SRC)
    catalog_json(structs, index)
    if args.no_compile:
        return
    compile_tileset()
    write_sea_palette()
    patched = patch(structs)
    used = verify(rows, patched)
    print("colors per palette 6-12:", palette_report())
    images(structs)
    import pontos_catalog
    pontos_catalog.main(used, structs, sections)


if __name__ == "__main__":
    main()
