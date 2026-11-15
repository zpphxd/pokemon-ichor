#!/usr/bin/env python3
"""Draw, compile, register and catalog the far lands' secondaries.

  steppe       Thrace and the Pontic steppe: grasses, roads, rivers and marsh,
               kurgans and idols, the Arimaspian heights
  steppe_town  the Greek colonies on that coast: Abdera, and the Oikoumene's Olbia
  steppe_camp  Themiskyra, Diomedes's yard and the Scythian wagon camp
  far_west     Erytheia, Geryon's pasture, the Strait of the Pillars, the Ocean
               Stream; the Oikoumene's Atlantic shore and Tartessos
  hesperides   the Garden of the Hesperides, Atlas's ridge, the Atlas range

All pair with the aethos primary. The pipeline is world-act3's
kythera_build.py, ported:

1. Paints each set's structures (farlands_<set>.py), checks every 8x8 tile
   (over every animation frame) draws from one palette group, then redraws
   static tiles within 2 px of another as that tile.
2. Packs them into the 8-wide sheet, each section from a fixed row.
3. Writes data/tilesets/secondary/<dir>/porytiles_src (the three layers,
   attributes.csv, anim/).
4. Compiles with Porytiles in a scratch project (build/<dir>_porytiles)
   against an empty stand-in primary.
5. Borrows aethos ground: cells drawn on grass, path, sand, sea, shallows or
   falling water get aethos's ground metatile's bottom tiles.
6. Verifies every entry and the tile limit (504, or 496 for a set whose maps
   use wide doors: the door animations copy their frames over the last 8 or
   16 tiles), registers the set in src/data/tilesets/*.h (and its animation
   in src/tileset_anims.c), writes the scripted-swap labels, the catalog JSON,
   tools/ichor/maps/farlands_tiles.py, the sheet and piece images, and
   design/postgame/TILES_<set>.md.

Usage: /usr/bin/python3 tools/ichor/art/farlands_build.py [steppe|steppe_town|steppe_camp|
           far_west|hesperides|all] [--no-compile]
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
import farlands_lib as F  # noqa: E402

ROOT = F.ROOT
COLS = 8
NEAR_DUPLICATE_PX = 2
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
IMG = ROOT / "design/postgame/img"
DOCS = ROOT / "design/postgame"
TILES_PY = ROOT / "tools/ichor/maps/farlands_tiles.py"
NORMAL, COVERED, SPLIT = 0, 1, 2
ALL = ["steppe", "steppe_town", "steppe_camp", "far_west", "hesperides"]

# animation frame orders (Porytiles queues one step every 16 frames)
ANIM_ORDER = {
    "surf": ["0", "1", "2", "1"],
    "breakers": ["0", "1", "2", "3"],
    "fire": ["0", "1", "2", "1"],
    "glint": ["0", "0", "0", "1", "2", "0", "0", "0", "0", "0", "1", "0"],
    "glow": ["0", "1", "2", "1"],
    "twinkle": ["0", "0", "1", "0", "2", "0"],
}


def spec(name):
    mod = __import__(f"farlands_{name}")
    sp = mod.SPEC
    sp["module"] = mod
    sp.setdefault("labels", [])
    sp.setdefault("limit", 504)
    sp["name"] = name
    return sp


# --------------------------------------------------------------------------
# Packing and sources
# --------------------------------------------------------------------------

def pack(sp, sections):
    used = np.zeros((64, COLS), bool)
    total = 0
    starts = sorted(sp["rows"].values())
    for name, structs in sections:
        start = sp["rows"][name]
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
    return total, used


def write_sources(sp, structs, rows, used):
    src = ROOT / f"data/tilesets/secondary/{sp['dir']}/porytiles_src"
    if src.exists():
        shutil.rmtree(src)
    src.mkdir(parents=True)
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
    filler = F.C[sp.get("filler", "g2")]
    for r in range(rows):
        for c in range(COLS):
            if not used[r, c]:
                sheets["bottom"][r * 16:r * 16 + 16, c * 16:c * 16 + 16, :3] = filler
                sheets["bottom"][r * 16:r * 16 + 16, c * 16:c * 16 + 16, 3] = 255
    for ln, a in sheets.items():
        Image.fromarray(a, "RGBA").save(src / f"{ln}.png")
    lines = ["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh)]
    (src / "attributes.csv").write_text("\n".join(lines) + "\n")
    write_anims(src, structs)
    return src


def static_forms(structs):
    static = set()
    for s in structs:
        at = F.anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in s.ground:
                        continue
                    if (ln, tx, ty) in at:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    static |= {v.tobytes() for v in F._flips(t)}
    return static


def fix_keys(structs):
    """Make every animated tile's key frame non-empty and unique."""
    seen = {}
    nudged = 0
    static = static_forms(structs)
    for s in structs:
        at = F.anim_tiles(s)
        for (ln, tx, ty), name in sorted(at.items(), key=lambda kv: (kv[0][2], kv[0][1], kv[0][0])):
            an = s.anims[name]
            sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            base = s.layers[ln].a
            frames = [f.a[sl] for f in an["frames"]]
            for _ in range(64):
                key = base[sl].copy()
                key[key[..., 3] == 0] = 0
                fr = [key.tobytes()] + [np.where(f[..., 3:4] > 0, f, 0).tobytes() for f in frames]
                kb = key.tobytes()
                empty = not (key[..., 3] > 0).any()
                clash = (kb in seen and seen[kb] != fr) or \
                    any(v.tobytes() in static for v in F._flips(key))
                if not empty and not clash:
                    seen[kb] = fr
                    break
                done = False
                for f in frames:
                    diff = np.argwhere((f != base[sl]).any(-1) & (f[..., 3] > 0))
                    for (yy, xx) in diff:
                        if not done:
                            base[ty * 8 + yy, tx * 8 + xx] = f[yy, xx]
                            done = True
                            nudged += 1
                    if done:
                        break
                if not done:
                    raise SystemExit(f"farlands_build: can't make {s.key} tile ({tx},{ty})'s key unique")
    if nudged:
        print(f"  nudged {nudged} pixels to make animation key frames unique")


def collect_anims(structs):
    out = {}
    seen = {}
    for s in structs:
        at = F.anim_tiles(s)
        for (ln, tx, ty), name in sorted(at.items(), key=lambda kv: (kv[0][2], kv[0][1], kv[0][0])):
            an = s.anims[name]
            sl = np.s_[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            key = s.layers[ln].a[sl].copy()
            key[key[..., 3] == 0] = 0
            frames = [key] + [f.a[sl].copy() for f in an["frames"]]
            for f in frames:
                f[f[..., 3] == 0] = 0
            kb = key.tobytes()
            if kb in seen:
                prev = seen[kb]
                if prev[0] != name or any(not np.array_equal(a, b) for a, b in zip(prev[1], frames)):
                    raise SystemExit(f"farlands_build: {s.key} tile ({tx},{ty}) shares its key frame "
                                     f"with another animated tile but animates differently")
                continue
            seen[kb] = (name, frames)
            out.setdefault(name, []).append((key, frames))
    return out


def write_anims(src, structs):
    anims = collect_anims(structs)
    if not anims:
        return {}
    d = src / "anim"
    d.mkdir(parents=True, exist_ok=True)
    meta = {}
    for name, tiles in anims.items():
        n = len(tiles[0][1])
        ad = d / name
        ad.mkdir()
        key = np.concatenate([t[0] for t in tiles], axis=0)
        Image.fromarray(key, "RGBA").save(ad / "key.png")
        for fi in range(n):
            fr = np.concatenate([t[1][fi] for t in tiles], axis=0)
            Image.fromarray(fr, "RGBA").save(ad / f"{fi}.png")
        order = ANIM_ORDER.get(name, [str(i) for i in range(n)])
        order = [o for o in order if int(o) < n]
        meta[name] = {"frames": [str(i) for i in range(n)], "frame_order": order}
        print(f"  anim {name}: {len(tiles)} tiles x {n} frames")
    (d / "anim.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def check_anim_keys(structs):
    static, keys = set(), set()
    for s in structs:
        at = F.anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if ln == "bottom" and (tx // 2, ty // 2) in s.ground:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    forms = {v.tobytes() for v in F._flips(t)}
                    if (ln, tx, ty) in at:
                        keys |= forms
                    else:
                        static |= forms
    clash = keys & static
    if clash:
        raise SystemExit(f"farlands_build: {len(clash)} animated key tiles also appear as static tiles")


# --------------------------------------------------------------------------
# Porytiles, in a scratch project
# --------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-4000:], r.stderr[-4000:])
        sys.exit(f"farlands_build: failed: {' '.join(map(str, cmd))}")
    return r


def palette_hints(groups):
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in groups.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = F.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


def suffix(sp):
    return sp["symbol"].replace("gTileset_", "")


def scratch_project(sp, groups):
    name, d = sp["symbol"], sp["dir"]
    sfx = suffix(sp)
    scratch = ROOT / f"build/{d}_porytiles"
    cfg_real = ROOT / "porytiles/tilesets" / name
    bin_real = ROOT / f"data/tilesets/secondary/{d}/porytiles_bin"
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
    for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "src/tileset_anims.c", "include/tileset_anims.h"):
        p = scratch / rel
        t = p.read_text()
        t = re.sub(rf"(// [^\n]*\n)*const struct Tileset {name}\s*=\s*\{{.*?\}};\n", "", t, flags=re.S)
        t = re.sub(rf"const u16 gTilesetPalettes_PorytilesManaged_{sfx}\[\]\[16\]\s*=\s*\{{.*?\}};\n",
                   "", t, flags=re.S)
        t = "\n".join(line for line in t.split("\n")
                      if not re.search(rf"PorytilesManaged_{sfx}\b|tilesets/{d}/generated_anim_code",
                                       line))
        p.write_text(t)
    pt = porytiles()
    run([pt, "create-tileset", "-C", str(scratch), f"gTileset_{sfx}Stub"])
    stub = next((scratch / "data/tilesets/primary").iterdir()) / "porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(scratch), f"gTileset_{sfx}Stub"])
    cfg = scratch / "porytiles/tilesets" / name
    cfg.mkdir(parents=True)
    pairing = (f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_{sfx}Stub]\n")
    (cfg / "config.yaml").write_text(pairing)
    run([pt, "create-tileset", "-C", str(scratch), "--secondary", name])
    sec = scratch / f"data/tilesets/secondary/{d}"
    shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(ROOT / f"data/tilesets/secondary/{d}/porytiles_src", sec / "porytiles_src")
    (cfg / "config.yaml").write_text(pairing + palette_hints(groups))
    return scratch, sec, cfg_real, bin_real


def compile_tileset(sp, groups):
    scratch, sec, cfg_real, bin_real = scratch_project(sp, groups)
    name = sp["symbol"]
    r = run([porytiles(), "compile-tileset", "-C", str(scratch), "--no-verify-checksums", name])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-2000:])
    if bin_real.exists():
        shutil.rmtree(bin_real)
    shutil.copytree(sec / "porytiles_bin", bin_real)
    cfg_real.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        shutil.copy2(scratch / "porytiles/tilesets" / name / f, cfg_real / f)
    (cfg_real / "config.yaml").write_text(
        f"# Per-tileset Porytiles config for {name} ({sp['title']}).\n"
        "# Written by tools/ichor/art/farlands_build.py, which compiles it against an empty\n"
        "# stand-in primary, then points its ground cells at aethos's grass, path, sand,\n"
        "# sea, shallows and waterfall. Pair it with aethos when compiling it directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + palette_hints(groups))
    gen = scratch / f"include/porytiles_generated/tilesets/{sp['dir']}/generated_anim_code.h"
    dst = ROOT / f"include/porytiles_generated/tilesets/{sp['dir']}/generated_anim_code.h"
    if gen.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(gen, dst)
        return True
    if dst.exists():
        dst.unlink()
    return False


def borrow_ground(sp, structs):
    bin_ = ROOT / f"data/tilesets/secondary/{sp['dir']}/porytiles_bin"
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    meta = np.fromfile(bin_ / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(bin_ / "metatile_attributes.bin", "<u2")
    patched = {}
    for s in structs:
        for (cx, cy), kind in s.ground.items():
            i = s.ids[cy][cx] - 0x200
            sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            on_top = bool((s.T.a[sl][..., 3] > 0).any())
            lt = int(attrs[i]) >> 12
            ent = [int(e) for e in meta[i]]
            art = ent[4:8] if any(ent[4:8]) else ent[0:4]
            if on_top and lt == NORMAL:
                art = ent[4:8]
            meta[i, 0:4] = aethos[F.GROUND_METATILE[kind], 0:4]
            meta[i, 4:8] = art
            attrs[i] = (int(attrs[i]) & 0x0FFF) | ((SPLIT if on_top else COVERED) << 12)
            patched[i] = kind
    meta.astype("<u2").tofile(bin_ / "metatiles.bin")
    attrs.astype("<u2").tofile(bin_ / "metatile_attributes.bin")
    return patched


def verify(sp, rows, patched):
    bin_ = ROOT / f"data/tilesets/secondary/{sp['dir']}/porytiles_bin"
    raw = np.fromfile(bin_ / "metatiles.bin", "<u2").reshape(-1, 8)
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = []
    for i, entries in enumerate(raw):
        for j, e in enumerate(entries):
            e = int(e)
            if i in patched and j < 4:
                if e != int(aethos[F.GROUND_METATILE[patched[i]], j]):
                    bad.append((0x200 + i, j, "ground"))
                continue
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                continue
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"farlands_build: entries outside the secondary's tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(bin_ / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    limit = sp["limit"]
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= limit})
    print(f"verified {len(raw)} metatiles; {used} of {limit} tiles used; "
          f"{len(patched)} cells on aethos ground")
    if used > limit or late:
        sys.exit(f"farlands_build: {used} tiles and tiles {late[:8]} referenced; the door "
                 f"animations overwrite tiles {limit}-511")
    return used, len(raw)


# --------------------------------------------------------------------------
# Registration in the C tables
# --------------------------------------------------------------------------

def register(sp, animated):
    d, name, sfx = sp["dir"], sp["symbol"], suffix(sp)
    gfx = ROOT / "src/data/tilesets/graphics.h"
    t = gfx.read_text()
    if f"gTilesetTiles_PorytilesManaged_{sfx}[]" not in t:
        pals = ",\n".join(f'    INCBIN_U16("data/tilesets/secondary/{d}/porytiles_bin/palettes/{p:02d}.gbapal")'
                          for p in range(16))
        t = t.rstrip("\n") + (
            f"\n\n// Ichor: {d} ({sp['title']}), written by tools/ichor/art/farlands_build.py\n"
            f"const u32 gTilesetTiles_PorytilesManaged_{sfx}[] = "
            f"INCBIN_U32(\"data/tilesets/secondary/{d}/porytiles_bin/tiles.4bpp.lz\");\n\n"
            f"const u16 gTilesetPalettes_PorytilesManaged_{sfx}[][16] =\n{{\n{pals}\n}};\n")
        gfx.write_text(t)
    met = ROOT / "src/data/tilesets/metatiles.h"
    t = met.read_text()
    if f"gMetatiles_PorytilesManaged_{sfx}[]" not in t:
        t = t.rstrip("\n") + (
            f"\n\n// Ichor: {d}\n"
            f"const u16 gMetatiles_PorytilesManaged_{sfx}[] = "
            f"INCBIN_U16(\"data/tilesets/secondary/{d}/porytiles_bin/metatiles.bin\");\n"
            f"const u16 gMetatileAttributes_PorytilesManaged_{sfx}[] = "
            f"INCBIN_U16(\"data/tilesets/secondary/{d}/porytiles_bin/metatile_attributes.bin\");\n")
        met.write_text(t)
    hdr = ROOT / "src/data/tilesets/headers.h"
    t = hdr.read_text()
    cb = f"InitTilesetAnim_PorytilesManaged_{sfx}" if animated else "NULL"
    block = (f"// Ichor: {d}, {sp['title']} (post-game). Porytiles-managed, built by\n"
             f"// tools/ichor/art/farlands_build.py for the aethos primary: its ground cells\n"
             f"// borrow aethos's grass, path, sand, sea, shallows and waterfall, so rebuild\n"
             f"// it whenever aethos changes.\n"
             f"const struct Tileset {name} =\n{{\n"
             f"    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n"
             f"    .tiles = gTilesetTiles_PorytilesManaged_{sfx},\n"
             f"    .palettes = gTilesetPalettes_PorytilesManaged_{sfx},\n"
             f"    .metatiles = gMetatiles_PorytilesManaged_{sfx},\n"
             f"    .metatileAttributes = gMetatileAttributes_PorytilesManaged_{sfx},\n"
             f"    .callback = {cb},\n}};\n")
    if f"const struct Tileset {name} =" in t:
        t = re.sub(rf"// Ichor: {d}, .*?const struct Tileset {name}\s*=\s*\{{.*?\}};\n", block, t,
                   flags=re.S)
    else:
        t = t.rstrip("\n") + "\n\n" + block
    hdr.write_text(t)
    anc = ROOT / "src/tileset_anims.c"
    anh = ROOT / "include/tileset_anims.h"
    inc = f'#include "porytiles_generated/tilesets/{d}/generated_anim_code.h"'
    dec = f"void InitTilesetAnim_PorytilesManaged_{sfx}(void);"
    t = anc.read_text()
    if animated and inc not in t:
        t = t.rstrip("\n") + f"\n// [Porytiles] Auto-generated include. Do not remove.\n{inc}\n"
    if not animated and inc in t:
        t = t.replace(f"// [Porytiles] Auto-generated include. Do not remove.\n{inc}\n", "")
    anc.write_text(t)
    t = anh.read_text()
    if animated and dec not in t:
        t = t.replace("\n#endif // GUARD_TILESET_ANIMS_H",
                      f"\n// [Porytiles] Auto-generated declaration. Do not remove.\n{dec}\n"
                      "\n#endif // GUARD_TILESET_ANIMS_H")
    if not animated and dec in t:
        t = t.replace(f"// [Porytiles] Auto-generated declaration. Do not remove.\n{dec}\n", "")
    anh.write_text(t)


LABELS = ROOT / "include/constants/metatile_labels.h"


def write_labels(sp, structs):
    want = dict(sp.get("labels", []))
    if not want:
        return
    start = f"// {sp['symbol']} (Ichor: {sp['title']}), written by tools/ichor/art/farlands_build.py"
    end = f"// end {sp['symbol']}"
    lines = [start]
    by = {s.key: s for s in structs}
    for key, items in want.items():
        s = by[key]
        for name, label in items:
            cx, cy = s.names[name]
            lines.append(f"#define METATILE_{sp['label']}_{label:<24} 0x{s.ids[cy][cx]:03X}")
    lines.append(end)
    block = "\n".join(lines) + "\n"
    text = LABELS.read_text()
    if start in text:
        a = text.index(start)
        b = text.index(end, a) + len(end) + 1
        text = text[:a] + block + text[b:]
    else:
        e = text.rindex("#endif")
        text = text[:e] + block + "\n" + text[e:]
    LABELS.write_text(text)


# --------------------------------------------------------------------------
# Catalog
# --------------------------------------------------------------------------

def catalog(sp, sections):
    data = []
    for sec_name, ss in sections:
        for s in ss:
            data.append({
                "key": s.key, "title": s.title, "section": sec_name, "w": s.w, "h": s.h,
                "ids": s.ids, "walk": s.walk, "notes": s.notes, "oikoumene": bool(s.oik),
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
                "ground": {f"{x},{y}": g for (x, y), g in s.ground.items()},
                "anims": sorted(set(F.anim_tiles(s).values())),
            })
    out = ROOT / f"build/{sp['dir']}"
    out.mkdir(parents=True, exist_ok=True)
    cat = {"tileset": sp["symbol"], "structures": data}
    (out / "catalog.json").write_text(json.dumps(cat, indent=1))
    return cat


def write_tiles_py(name, cat):
    """tools/ichor/maps/farlands_tiles.py: every far-lands set's catalog as a
    Python dict, so map builders (ours and the Oikoumene's) place pieces by name."""
    cur = {}
    if TILES_PY.exists():
        ns = {}
        exec(compile(TILES_PY.read_text(), str(TILES_PY), "exec"), ns)
        cur = ns.get("TILESETS", {})
    slim = {"symbol": cat["tileset"], "structures": {}}
    for d in cat["structures"]:
        slim["structures"][d["key"]] = {
            "w": d["w"], "h": d["h"], "ids": d["ids"], "walk": d["walk"],
            "names": {k: tuple(v) for k, v in d["names"].items()},
            "ground": d["ground"], "section": d["section"], "oikoumene": d["oikoumene"],
        }
    cur[name] = slim
    body = json.dumps(cur, indent=1, sort_keys=True)
    body = body.replace("true", "True").replace("false", "False").replace("null", "None")
    TILES_PY.parent.mkdir(parents=True, exist_ok=True)
    TILES_PY.write_text(
        '"""Metatile ids of the far lands\' secondaries, for map builders.\n\n'
        "Generated by tools/ichor/art/farlands_build.py; do not edit. One entry per\n"
        "tileset (steppe, steppe_town, steppe_camp, far_west, hesperides), each\n"
        "{'symbol', 'structures': {key: {'w', 'h', 'ids' (rows of metatile ids),\n"
        "'walk' (rows of walk codes), 'names' {piece: (x, y)}, 'ground' {'x,y':\n"
        "aethos ground}, 'section', 'oikoumene' (True: drawn for the Oikoumene's\n"
        "lands)}}}. The catalogs, with what every piece is for, are\n"
        "design/postgame/TILES_*.md.\n\n"
        "Soft ground (grasses, roads, red earth, mud, water) comes in 47 shapes keyed\n"
        "by a cell's neighbors: shape(region, x, y) gives the key, and\n"
        "soft(tileset, key, region, x, y) the metatile.\n\n"
        "    from farlands_tiles import mid, soft\n"
        "    idol = mid('steppe', 'idols', 'horn')\n"
        "    grass = soft('steppe', 'steppe_grass', region, x, y)\n"
        '"""\n\n'
        f"TILESETS = {body}\n\n"
        "NEIGHBORS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]\n\n\n"
        "def mid(tileset, key, name=None, x=0, y=0):\n"
        '    """The metatile id of a named piece (or of cell (x, y) of a structure)."""\n'
        "    s = TILESETS[tileset]['structures'][key]\n"
        "    if name is not None:\n"
        "        x, y = s['names'][name]\n"
        "    return s['ids'][y][x]\n\n\n"
        "def walk(tileset, key, name=None, x=0, y=0):\n"
        '    """The walk code of a named piece: X . T G L D W P H M F J (see the catalogs)."""\n'
        "    s = TILESETS[tileset]['structures'][key]\n"
        "    if name is not None:\n"
        "        x, y = s['names'][name]\n"
        "    return s['walk'][y][x]\n\n\n"
        "def shape(region, x, y):\n"
        '    """The soft-ground shape key of cell (x, y) in a boolean grid region[y][x]:\n'
        "    '1|' then N NE E SE S SW W NW, a diagonal counting only when both of its\n"
        '    sides are in. Cells off the grid count as in the region."""\n'
        "    hh, ww = len(region), len(region[0])\n\n"
        "    def at(i, j):\n"
        "        if not (0 <= i < ww and 0 <= j < hh):\n"
        "            return 1\n"
        "        return 1 if region[j][i] else 0\n"
        "    b = [at(x + dx, y + dy) for dx, dy in NEIGHBORS]\n"
        "    for d, (a, c) in ((1, (0, 2)), (3, (2, 4)), (5, (4, 6)), (7, (6, 0))):\n"
        "        if not (b[a] and b[c]):\n"
        "            b[d] = 0\n"
        "    return '1|' + ''.join(str(v) for v in b)\n\n\n"
        "def soft(tileset, key, region, x, y):\n"
        '    """The metatile for cell (x, y) of a soft-ground region (it must be in it)."""\n'
        "    return mid(tileset, key, shape(region, x, y))\n\n\n"
        "def oikoumene_pieces(tileset):\n"
        '    """The keys of the pieces drawn for the Oikoumene\'s lands."""\n'
        "    return sorted(k for k, s in TILESETS[tileset]['structures'].items() if s['oikoumene'])\n")


def images(sp, structs):
    IMG.mkdir(parents=True, exist_ok=True)
    d = sp["dir"]
    F.shelf_preview(structs, scale=2, width=1400).save(IMG / f"farlands_{d}_pieces.png")
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", sp["symbol"],
         "--primary", "aethos", "--scale", "2", "-o", str(IMG / f"farlands_{d}_sheet.png")])
    print(f"design/postgame/img/farlands_{d}_pieces.png, farlands_{d}_sheet.png")


# --------------------------------------------------------------------------

def build_one(name, compile_=True, quiet=False):
    sp = spec(name)
    mod = sp["module"]
    groups = mod.GROUPS
    F.check_groups(groups, name)
    grgb = F.group_rgb(groups)
    by = mod.build()
    sections = [(sec, [by[k] for k in keys]) for sec, keys in sp["sections"]]
    structs = [s for _, ss in sections for s in ss]
    keys = [s.key for s in structs]
    assert len(keys) == len(set(keys)), f"duplicate structure keys in {name}"
    missing = set(by) - set(keys)
    assert not missing, f"{name}: built but not placed: {sorted(missing)}"
    probs = F.validate(structs, grgb)
    if not probs:
        before = len(F.tiles_of(structs))
        merges = F.merge_near_duplicates(structs, NEAR_DUPLICATE_PX, grgb)
        print(f"{name}: merged {len(merges)} near-duplicate tiles: {before} -> "
              f"{len(F.tiles_of(structs))} tiles")
        probs = F.validate(structs, grgb)
    for p in F.tile_report(structs, grgb)[:40]:
        print("PROBLEM:", p)
    for p in probs[:40]:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    fix_keys(structs)
    check_anim_keys(structs)
    rows, used = pack(sp, sections)
    write_sources(sp, structs, rows, used)
    cat = catalog(sp, sections)
    write_tiles_py(name, cat)
    write_labels(sp, structs)
    if not compile_:
        cost = F.tile_cost(structs)
        print(f"{name}: {len(F.tiles_of(structs))} tiles (before Porytiles), {rows * 8} metatile slots")
        for k, v in sorted(cost.items(), key=lambda kv: -kv[1]):
            print(f"  {k:24} {v}")
        return
    animated = compile_tileset(sp, groups)
    patched = borrow_ground(sp, structs)
    register(sp, animated)
    n_tiles, n_meta = verify(sp, rows, patched)
    images(sp, structs)
    import farlands_catalog
    farlands_catalog.main(name, sp, sections, n_tiles, n_meta, groups)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tileset", nargs="?", default="steppe")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    names = ALL if args.tileset == "all" else [args.tileset]
    for n in names:
        build_one(n, not args.no_compile)


if __name__ == "__main__":
    main()
