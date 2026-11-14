#!/usr/bin/env python3
"""Draw, compile and catalog Phase 2's tilesets: gTileset_Emporion (the city),
gTileset_Isthmos (its harbor and the Isthmus) and gTileset_TempleHermes.

The pipeline is akti_build.py's, generalized so all three share it:

1. Draws every structure (emporion_art, isthmos_art or temple_hermes .build()) and
   checks each 8x8 tile draws from one palette group. Tiles within
   NEAR_DUPLICATE_PX pixels of another are redrawn as that one, so they are
   stored once.
2. Packs them into the 8-wide metatile sheet from 0x200, section by section,
   each section on a fixed row so adding to one never renumbers another.
3. Writes data/tilesets/secondary/<dir>/porytiles_src.
4. Compiles with Porytiles in a scratch project under build/ against an empty
   stand-in primary, so the art uses only its own tiles and palettes 6-12, with
   the palette groups as packing hints. The parallel "clay" and "clay2" groups
   let Porytiles store a recolored house part once.
5. Emporion only: borrows aethos's ground. Every cell drawn on grass, sand, sea
   or path gets its bottom layer pointed at aethos's metatile (0x001, 0x124,
   0x170, 0x1D9). Rebuild whenever aethos is repainted.
6. Verifies every entry and fails past TILE_LIMIT (504) tiles: door animations
   own tiles 504-511. Writes build/<dir>/catalog.json, the sheet and the pieces
   preview, and the catalog (design/phase2/TILES_<dir>.md).

Usage: /usr/bin/python3 tools/ichor/art/emporion_build.py [emporion|isthmos|temple_hermes]
       [--no-compile] [--preview out.png]
Then /usr/bin/python3 tools/ichor/art/emporion_scene.py renders the mock scenes.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion_lib as E  # noqa: E402
from kalliste_lib import pack, write_sources  # noqa: E402

ROOT = E.ROOT
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
IMG = ROOT / "design/phase2/img"

# Door animations copy their frames into the last 8 tiles of VRAM, which are a
# secondary tileset's tiles 504-511 (DOOR_TILE_START_SIZE1 in src/field_door.c).
TILE_LIMIT = 504
NEAR_DUPLICATE_PX = 2
NORMAL, COVERED, SPLIT = 0, 1, 2   # metatile layer types (attribute bits 12-15)


TILESETS = {
    # name: (module, symbol)
    "emporion": ("emporion_art", "gTileset_Emporion"),
    "isthmos": ("isthmos_art", "gTileset_Isthmos"),
    "temple_hermes": ("temple_hermes", "gTileset_TempleHermes"),
}


class Spec:
    def __init__(self, name="emporion"):
        import importlib
        mod, self.symbol = TILESETS[name]
        art = importlib.import_module(mod)
        self.name = self.dir = name
        self.groups = getattr(art, "GROUPS", E.GROUPS)
        self.art = art
        self.temple = name == "temple_hermes"
        self.src = ROOT / f"data/tilesets/secondary/{self.dir}/porytiles_src"
        self.bin = ROOT / f"data/tilesets/secondary/{self.dir}/porytiles_bin"
        self.cfg = ROOT / f"porytiles/tilesets/{self.symbol}"
        self.scratch = ROOT / f"build/{self.dir}_porytiles"
        self.out = ROOT / f"build/{self.dir}"
        self.sheet = IMG / f"{self.dir}_sheet.png"
        self.pieces = IMG / f"{self.dir}_pieces.png"


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"emporion_build: failed: {' '.join(map(str, cmd))}")
    return r


def hints_yaml(groups, colors):
    y = "  palettes:\n    packing:\n      hints_enabled: true\n      hints:\n"
    for g, names in groups.items():
        y += f"        - name: {g}\n          colors:\n"
        for n in names:
            r, gg, b = colors[n]
            y += f"            - [{r}, {gg}, {b}]\n"
    return y


def scratch_project(spec):
    S = spec.scratch
    if S.exists():
        shutil.rmtree(S)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml",
                "data/layouts/layouts.json"):
        dst = S / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    (S / "data/tilesets/primary").mkdir(parents=True)
    (S / "data/tilesets/secondary").mkdir(parents=True)
    pt = porytiles()
    stub_name = f"{spec.symbol}Stub"
    run([pt, "create-tileset", "-C", S, stub_name])
    stubdir = next((S / "data/tilesets/primary").iterdir())
    stub = stubdir / "porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    from PIL import Image
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", S, stub_name])
    cfg = S / f"porytiles/tilesets/{spec.symbol}"
    if (spec.cfg / "tileset-manifest.json").exists():
        cfg.mkdir(parents=True)
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            if (spec.cfg / f).exists():
                shutil.copy2(spec.cfg / f, cfg / f)
        sec = S / f"data/tilesets/secondary/{spec.dir}"
        sec.mkdir(parents=True)
        if spec.bin.exists():
            shutil.copytree(spec.bin, sec / "porytiles_bin")
    else:
        # The tables already declare the tileset (it is registered in the repo), so
        # hide those declarations from Porytiles while it creates the tileset.
        import re
        short = spec.symbol.replace("gTileset_", "")
        for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                    "src/data/tilesets/metatiles.h"):
            p = S / rel
            t = p.read_text()
            t = re.sub(rf"const struct Tileset {spec.symbol} =\s*\{{.*?\}};", "", t, flags=re.S)
            t = re.sub(rf"const u16 gTilesetPalettes_PorytilesManaged_{short}\[\]\[16\] =\s*\{{.*?\}};",
                       "", t, flags=re.S)
            t = re.sub(rf"const u\d+ g\w+_PorytilesManaged_{short}\[\] = [^\n]*\n", "", t)
            p.write_text(t)
        run([pt, "create-tileset", spec.symbol, "-C", S, "--secondary",
             "--primary-pairing-mode", "manual", "--primary-pairing-partners", stub_name])
        sec = S / f"data/tilesets/secondary/{spec.dir}"
        assert sec.exists(), f"porytiles made no {sec}"
    (cfg / "config.yaml").write_text(
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [" + stub_name + "]\n"
        + hints_yaml(spec.groups, E.C))
    if (sec / "porytiles_src").exists():
        shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(spec.src, sec / "porytiles_src")
    return sec


def compile_tileset(spec):
    sec = scratch_project(spec)
    r = run([porytiles(), "compile-tileset", "-C", spec.scratch, "--no-verify-checksums",
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
    # The project's own config pairs with aethos, so a direct Porytiles compile
    # (as for akti) works; the build itself always uses the scratch project.
    (spec.cfg / "config.yaml").write_text(
        f"# Written by tools/ichor/art/emporion_build.py; edit it there.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + hints_yaml(spec.groups, E.C))


def _flips(t):
    return (t, t[:, ::-1], t[::-1, :], t[::-1, ::-1])


def _tiles(structs):
    occ = {}
    for s in structs:
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
    """Redraw each tile within `limit` pixels of another as that other tile (as
    akti_build.py does). Returns the merges."""
    occ = _tiles(structs)
    keys = list(occ)
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


def borrow_ground(spec, structs):
    """Point each borrowed cell's bottom layer at aethos's ground metatile."""
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    meta = np.fromfile(spec.bin / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(spec.bin / "metatile_attributes.bin", "<u2")
    patched = {}
    for s in structs:
        for (cx, cy), kind in s.borrowed.items():
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
    meta.astype("<u2").tofile(spec.bin / "metatiles.bin")
    attrs.astype("<u2").tofile(spec.bin / "metatile_attributes.bin")
    return patched


def verify(spec, rows, patched):
    raw = np.fromfile(spec.bin / "metatiles.bin", "<u2").reshape(-1, 8)
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = []
    for i, entries in enumerate(raw):
        if not any(int(e) for e in entries):
            continue   # an unused slot in the sheet
        for j, e in enumerate(entries):
            e = int(e)
            if i in patched and j < 4:
                if e != int(aethos[E.GROUND_METATILE[patched[i]], j]):
                    bad.append((0x200 + i, j, "ground"))
                continue
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                if spec.temple and j < 4:
                    bad.append((0x200 + i, j, "transparent first layer"))
                continue
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"emporion_build: entries outside {spec.dir}'s tiles/palettes 6-12: {bad[:10]}")
    from PIL import Image
    a = np.array(Image.open(spec.bin / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{len(patched)} cells on aethos ground")
    if used > TILE_LIMIT:
        sys.exit(f"emporion_build: {used} tiles; the door animations overwrite tiles "
                 f"{TILE_LIMIT}-511, so {spec.dir} may use at most {TILE_LIMIT}")
    return used


def catalog_json(spec, structs):
    data = []
    for s in structs:
        data.append({
            "key": s.key, "title": s.title, "section": s.section, "w": s.w, "h": s.h,
            "ids": s.ids, "walk": s.walk, "notes": s.notes,
            "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
            "ground": {f"{x},{y}": g for (x, y), g in sorted(s.ground.items())},
            "names": {n: list(c) for n, c in getattr(s, "names", {}).items()},
        })
    spec.out.mkdir(parents=True, exist_ok=True)
    (spec.out / "catalog.json").write_text(json.dumps(data, indent=1))


def images(spec, structs):
    IMG.mkdir(parents=True, exist_ok=True)
    E.preview(structs, scale=2, cols=5).save(spec.pieces)
    run([sys.executable, ROOT / "tools/ichor/render_map.py", "--sheet",
         f"data/tilesets/secondary/{spec.dir}",
         "--primary", "oikos" if spec.temple else "aethos", "--scale", "2", "-o", spec.sheet])
    print(spec.sheet)
    print(spec.pieces)


def palette_report(spec):
    pals = []
    for i in range(6, 13):
        p = spec.bin / "palettes" / f"{i:02d}.pal"
        v = [int(t) for t in p.read_text().split()[3:]]
        cols = {tuple(v[k * 3:k * 3 + 3]) for k in range(1, 16)}
        cols.discard((0, 0, 0))
        pals.append(len(cols))
    return pals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tileset", nargs="?", default="emporion", choices=sorted(TILESETS))
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()
    spec = Spec(args.tileset)

    sections = spec.art.build()
    structs = [s for _, ss in sections for s in ss]
    keys = [s.key for s in structs]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, f"duplicate structure keys {dup}"
    validate = getattr(spec.art, "validate", E.validate)
    probs = validate(structs)
    if not probs:
        before = len(_tiles(structs))
        merges = merge_near_duplicates(structs)
        print(f"merged {len(merges)} near-duplicate tiles "
              f"({merges.count(1)} differed by 1 px, {merges.count(2)} by 2): "
              f"{before} -> {len(_tiles(structs))} distinct tiles before palette sharing")
        probs = validate(structs)
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
    catalog_json(spec, structs)
    if args.no_compile:
        return
    compile_tileset(spec)
    patched = borrow_ground(spec, structs) if not spec.temple else {}
    used = verify(spec, rows, patched)
    print("colors per palette 6-12:", palette_report(spec))
    images(spec, structs)
    spec.art.write_catalog(used, structs)


if __name__ == "__main__":
    main()
