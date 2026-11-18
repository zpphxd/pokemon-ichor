#!/usr/bin/env python3
"""Draw, compile, register and catalog the Labyrinth's two secondaries.

  labyrinth  gTileset_Labyrinth: the house, Daedalus's workshop, the outer rings
             (I, II, III, V), Minos's tomb and the Icarus Shaft
  mychos     gTileset_Mychos ("the innermost part of a house"): the house again,
             the Titan wing (Rings IV and VI, the archive, the vault, the
             Mistress's shrine), Ring VII and the Starry Chamber

LABYRINTH.md §11 planned one tileset; the rings, rooms and heart outgrew its 504
tiles, so it is split by map as Emporion was with Isthmos. Both draw the house
and the rings' floor (labyrinth_kit) at the same metatile ids.

The pipeline is emporion_build.py's, for a self-contained interior tileset, plus
tile animations (kythera_build.py's way) and the Labyrinth's palette variant sets:

1. Draws every structure (labyrinth_art.build(tileset)) and checks each 8x8 tile
   (over every animation frame) draws from one palette group, every bottom layer
   is opaque and no metatile uses three layers. Static tiles within
   NEAR_DUPLICATE_PX pixels of another are redrawn as that one.
2. Packs them into the 8-wide metatile sheet from 0x200, section by section,
   each section on a fixed row (labyrinth_art.SECTIONS), and writes
   data/tilesets/secondary/<dir>/porytiles_src with its anim/ (the braziers'
   and the forge's flames, the Starry Chamber's twinkling pool).
3. Compiles with Porytiles in a scratch project under build/ against an empty
   stand-in primary, so the tileset uses only its own tiles and palettes 6-12
   and works on any interior primary (it is drawn for oikos).
4. Registers it in src/data/tilesets/*.h and its animation in
   src/tileset_anims.c, and writes the variant palette sets beside the
   compiled palettes:
   - glow/NN.pal, the doused torch (SYSTEMS.md §2): black but for the glow
     paint, the flames and a faint thread. The latent glow color is normalized
     in the base palettes to the stone it imitates.
   - dawn/NN.pal (labyrinth), scene L: every color dimmed and cooled but the dawn
     light.
5. Verifies every entry, fails past TILE_LIMIT (504) tiles (door animations own
   504-511), and writes build/<dir>/catalog.json, the sheet and pieces previews
   in design/phase4/img/, design/phase4/TILES_<dir>.md and, for map builders,
   tools/ichor/maps/labyrinth_tiles.py.

Usage: /usr/bin/python3 tools/ichor/art/labyrinth_build.py [labyrinth|mychos|all] [--no-compile]
Then /usr/bin/python3 tools/ichor/art/labyrinth_scene.py renders the mock scenes.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion_build as EB  # noqa: E402
import emporion_lib as E  # noqa: E402
import labyrinth_art as A  # noqa: E402
from kalliste_lib import write_sources  # noqa: E402

ROOT = A.K.ROOT
IMG = ROOT / "design/phase4/img"
TILE_LIMIT = EB.TILE_LIMIT
TILES_PY = ROOT / "tools/ichor/maps/labyrinth_tiles.py"
SYMBOLS = {"labyrinth": "gTileset_Labyrinth", "mychos": "gTileset_Mychos",
           "daidaleion": "gTileset_Daidaleion"}
TITLES = {"labyrinth": "Daedalus's Labyrinth: the house, the cave, Rings I-IV, Minos's tomb",
          "daidaleion": "Daedalus's workshop and the Icarus Shaft",
          "mychos": "Daedalus's Labyrinth: the Titan wing, the Choros, the Starry Chamber"}

# animation frame orders (Porytiles steps one entry every 16 frames; lengths
# that divide 16 loop cleanly)
ANIM_ORDER = {
    "flame": ["0", "1", "2", "1"],
    "forge": ["0", "1", "2", "1"],
    "stars": ["0", "0", "1", "2", "1", "0", "0", "3", "0", "1", "0", "0", "2", "3", "2", "0"],
}


class Spec:
    """The fields emporion_build's helpers read."""
    art = A
    temple = True   # self-contained: no borrowed ground, opaque bottoms

    def __init__(self, name="labyrinth"):
        self.name = self.dir = name
        self.symbol = SYMBOLS[name]
        self.groups = A.groups_for(name)
        self.sfx = self.symbol.replace("gTileset_", "")
        self.src = ROOT / f"data/tilesets/secondary/{self.dir}/porytiles_src"
        self.bin = ROOT / f"data/tilesets/secondary/{self.dir}/porytiles_bin"
        self.cfg = ROOT / f"porytiles/tilesets/{self.symbol}"
        self.scratch = ROOT / f"build/{self.dir}_porytiles"
        self.out = ROOT / f"build/{self.dir}"
        self.sheet = IMG / f"{self.dir}_sheet.png"
        self.pieces = IMG / f"{self.dir}_pieces.png"


# --------------------------------------------------------------------------
# Tiles: near-duplicates and animations
# --------------------------------------------------------------------------

def _flips(t):
    return (t, t[:, ::-1], t[::-1, :], t[::-1, ::-1])


def static_tiles(structs):
    """{normalized tile bytes: [(layer, tx, ty)]} for every static tile."""
    occ = {}
    for s in structs:
        at = A.anim_tiles(s)
        for ln, layer in s.layers.items():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    if (ln, tx, ty) in at:
                        continue
                    t = layer.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy()
                    if not (t[..., 3] > 0).any():
                        continue
                    t[t[..., 3] == 0] = 0
                    occ.setdefault(min(v.tobytes() for v in _flips(t)), []).append((layer, tx, ty))
    return occ


def merge_near_duplicates(structs, limit=EB.NEAR_DUPLICATE_PX):
    """emporion_build's merge, leaving animated tiles alone."""
    occ = static_tiles(structs)
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


def fix_keys(structs):
    """Make every animated tile's key frame (frame 0) non-empty and unique among
    the animated tiles and the static ones (Porytiles finds animated tiles by
    their key frame): one that isn't takes a pixel from its own later frames."""
    seen = {}
    static = set()
    for k in static_tiles(structs):
        t = np.frombuffer(k, np.uint8).reshape(8, 8, 4)
        static |= {v.tobytes() for v in _flips(t)}
    nudged = 0
    for s in structs:
        at = A.anim_tiles(s)
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
                    any(v.tobytes() in static for v in _flips(key))
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
                    sys.exit(f"labyrinth_build: can't make {s.key} tile ({tx},{ty})'s key unique")
    if nudged:
        print(f"  nudged {nudged} pixels to make animation key frames unique")


def collect_anims(structs):
    """{anim name: [(key tile, [frame tiles])]} in a stable order."""
    out, seen = {}, {}
    for s in structs:
        at = A.anim_tiles(s)
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
                    sys.exit(f"labyrinth_build: {s.key} tile ({tx},{ty}) shares its key frame "
                             f"with another animated tile but animates differently")
                continue
            seen[kb] = (name, frames)
            out.setdefault(name, []).append((key, frames))
    return out


def write_anims(src, structs):
    shutil.rmtree(src / "anim", ignore_errors=True)
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
        Image.fromarray(np.concatenate([t[0] for t in tiles], axis=0), "RGBA").save(ad / "key.png")
        for fi in range(n):
            Image.fromarray(np.concatenate([t[1][fi] for t in tiles], axis=0), "RGBA").save(
                ad / f"{fi}.png")
        order = ANIM_ORDER.get(name, [str(i) for i in range(n)])
        meta[name] = {"frames": [str(i) for i in range(n)], "frame_order": order}
        print(f"  anim {name}: {len(tiles)} tiles x {n} frames")
    (d / "anim.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


# --------------------------------------------------------------------------
# Compiling and registering
# --------------------------------------------------------------------------

def compile_tileset(spec):
    """Compile in the scratch project; returns True if it has animations."""
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
    gen = spec.scratch / f"include/porytiles_generated/tilesets/{spec.dir}/generated_anim_code.h"
    dst = ROOT / f"include/porytiles_generated/tilesets/{spec.dir}/generated_anim_code.h"
    if gen.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(gen, dst)
        return True
    if dst.exists():
        dst.unlink()
    return False


VARIANTS = {"labyrinth": ("glow",), "daidaleion": ("dawn",), "mychos": ("glow",)}
VARIANT_NOTE = {
    "glow": "// The doused set (SYSTEMS.md §2, \"Douse\"): black but for the glow paint, the flames\n"
            "// and a faint thread. Load it over palettes 6-12 while the torch is doused. Written\n"
            "// by tools/ichor/art/labyrinth_build.py; not yet wired into the engine.\n",
    "dawn": "// The dawn set (LABYRINTH.md §8, scene L): the workshop dimmed and cooled but for the\n"
            "// grey light down the Icarus Shaft. Load it over palettes 6-12 for the scene, and on\n"
            "// the Icarus Shaft. Written by tools/ichor/art/labyrinth_build.py; not yet wired\n"
            "// into the engine.\n",
}


def register(spec, animated):
    """Declare the tileset in src/data/tilesets/*.h and its animation in
    src/tileset_anims.c (idempotent)."""
    d, sfx, name = spec.dir, spec.sfx, spec.symbol
    gfx = ROOT / "src/data/tilesets/graphics.h"
    t = gfx.read_text()
    if f"gTilesetTiles_PorytilesManaged_{sfx}[]" not in t:
        pals = ",\n".join(f'    INCBIN_U16("data/tilesets/secondary/{d}/porytiles_bin/palettes/{p:02d}.gbapal")'
                          for p in range(16))
        t = t.rstrip("\n") + (
            f"\n\n// Ichor: {d}\n"
            f"const u32 gTilesetTiles_PorytilesManaged_{sfx}[] = "
            f"INCBIN_U32(\"data/tilesets/secondary/{d}/porytiles_bin/tiles.4bpp.lz\");\n\n"
            f"const u16 gTilesetPalettes_PorytilesManaged_{sfx}[][16] =\n{{\n{pals}\n}};\n")
    for v in VARIANTS[spec.name]:
        arr = f"gTilesetPalettes_{sfx}{v.capitalize()}"
        if f"{arr}[][16]" not in t:
            pals = ",\n".join(f'    INCBIN_U16("data/tilesets/secondary/{d}/porytiles_bin/{v}/{p:02d}.gbapal")'
                              for p in range(6, 13))
            t = t.rstrip("\n") + f"\n\n{VARIANT_NOTE[v]}const u16 {arr}[][16] =\n{{\n{pals}\n}};\n"
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
    variants = " and ".join(f"gTilesetPalettes_{sfx}{v.capitalize()}" for v in VARIANTS[spec.name])
    what = {"labyrinth": "the house's masonry, the karst cave it\n// was cut into, Rings I-IV "
                         "and Minos's tomb (LABYRINTH_MAZE.md)",
            "daidaleion": "the house's masonry, Daedalus's workshop\n// and the Icarus Shaft",
            "mychos": "the house's masonry, the Titan wing (Rings IV and\n// VI), Ring VII and "
                      "the Starry Chamber"}[spec.name]
    block = (f"// Ichor: {d}, Daedalus's Labyrinth under Knossa (LABYRINTH.md §11). Porytiles-managed,\n"
             f"// built by tools/ichor/art/labyrinth_build.py: {what}. It uses only\n"
             f"// its own tiles and palettes 6-12, with opaque floors, so it works on any interior\n"
             f"// primary (drawn for oikos). Its variant palette sets ({variants})\n"
             f"// are in graphics.h. No layout uses it yet.\n"
             f"const struct Tileset {name} =\n{{\n"
             f"    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n"
             f"    .tiles = gTilesetTiles_PorytilesManaged_{sfx},\n"
             f"    .palettes = gTilesetPalettes_PorytilesManaged_{sfx},\n"
             f"    .metatiles = gMetatiles_PorytilesManaged_{sfx},\n"
             f"    .metatileAttributes = gMetatileAttributes_PorytilesManaged_{sfx},\n"
             f"    .callback = {cb},\n}};\n")
    pat = rf"(// Ichor: {d},[^\n]*\n(//[^\n]*\n)*)?const struct Tileset {name}\s*=\s*\{{.*?\}};\n"
    if re.search(pat, t, flags=re.S):
        t = re.sub(pat, lambda m: block, t, count=1, flags=re.S)
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
    """Normalize the latent glow color, then write glow/ (and dawn/) beside palettes/."""
    pals = spec.bin / "palettes"
    out = {v: spec.bin / v for v in VARIANTS[spec.name]}
    for d in out.values():
        d.mkdir(exist_ok=True)
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
        if "glow" in out:
            write_pal(out["glow"] / f"{i:02d}.pal", glow)
        if "dawn" in out:
            write_pal(out["dawn"] / f"{i:02d}.pal", dawn)
    for n in A.LATENT:
        if n not in found:
            print(f"glow paint {n}: not drawn in {spec.name}")
    return found


# --------------------------------------------------------------------------
# Catalogs
# --------------------------------------------------------------------------

def catalog_json(spec, structs):
    """emporion_build's catalog, plus each odd twin's twin, the parity, thread
    floors' runs and the animated parts."""
    EB.catalog_json(spec, structs)
    p = spec.out / "catalog.json"
    data = json.loads(p.read_text())
    by_key = {s.key: s for s in structs}
    for d in data:
        s = by_key[d["key"]]
        if getattr(s, "twin_of", None):
            d["twin_of"] = list(s.twin_of)
        d["parity"] = getattr(s, "parity", None)
        if getattr(s, "runs", None):
            d["runs"] = {n: s.ids[i // 8][i % 8] for n, i in s.runs.items()}
        if getattr(s, "anims", None):
            d["anims"] = sorted(s.anims)
    p.write_text(json.dumps(data, indent=1))
    return data


def write_tiles_py(name, data):
    """tools/ichor/maps/labyrinth_tiles.py: both tilesets' catalogs as a Python
    dict, with the autotile, so map builders place pieces by key and name."""
    import inspect
    import labyrinth_kit as KIT
    cur = {}
    if TILES_PY.exists():
        ns = {}
        exec(compile(TILES_PY.read_text(), str(TILES_PY), "exec"), ns)
        cur = ns.get("TILESETS", {})
    slim = {"symbol": SYMBOLS[name], "structures": {}}
    for d in data:
        e = {"w": d["w"], "h": d["h"], "ids": d["ids"], "walk": d["walk"],
             "names": {k: tuple(v) for k, v in d["names"].items()}, "section": d["section"]}
        if d.get("behaviors"):
            e["behaviors"] = d["behaviors"]
        if d.get("twin_of"):
            e["twin_of"] = tuple(d["twin_of"])
        if d.get("runs"):
            e["runs"] = d["runs"]
        slim["structures"][d["key"]] = e
    cur[name] = slim
    src = "\n\n".join(inspect.getsource(f) for f in (KIT.top_name, KIT.face_name, KIT.classify))
    head = '''"""Metatile ids of the Labyrinth's two secondaries, for map builders.

Generated by tools/ichor/art/labyrinth_build.py; do not edit. TILESETS has one
entry per tileset ('labyrinth', 'mychos'), each {'symbol', 'structures': {key:
{'w', 'h', 'ids' (rows of metatile ids), 'walk' (rows of walk codes: X blocks,
. passes, D door), 'names' {part: (x, y)}, 'section', and where they apply
'behaviors' {'x,y': MB_*}, 'twin_of' (even twin, first row), 'runs' {floor:
id}}}}. The catalogs, with what every piece is for, are
design/phase4/TILES_labyrinth.md and TILES_mychos.md.

    import labyrinth_tiles as LT
    LT.mid('labyrinth', 'brazier', 'lit_tl')     # one named part
    LT.piece('labyrinth', 'brazier', x, y)       # a floor piece, by parity: key or key_odd
    LT.floor(x, y)                               # the ring floor for cell (x, y)
    LT.thread_floors()                           # [(floor, first twin)] for Ichor_AddThreadFloor
    LT.autotile(grid)                            # wall/floor grid -> metatile ids

The house (rows 0-12) and the thread section (rows 36-38) are the same ids in
both tilesets.
"""


'''
    funcs = '''

def mid(tileset, key, name):
    """The metatile id of a named part."""
    s = TILESETS[tileset]["structures"][key]
    x, y = s["names"][name]
    return s["ids"][y][x]


def piece(tileset, key, x, y):
    """The key to lay a floor-standing piece with its top-left cell at map (x, y):
    `key` where x + y is even, `key_odd` (its floor rows) where odd."""
    st = TILESETS[tileset]["structures"]
    return key + "_odd" if (x + y) % 2 and key + "_odd" in st else key


def floor(x, y, tileset="labyrinth", kind="dark"):
    """The ring floor for map cell (x, y): the slab's left half where x + y is
    even, its right half where odd (kind 'dark', or 'sun' / 'moon' for Ring V's
    pools in labyrinth)."""
    key = "thread" if kind == "dark" else "pools"
    return mid(tileset, key, f"{kind}_{'l' if (x + y) % 2 == 0 else 'r'}")


def thread_floors(tileset="labyrinth", kinds=("dark",)):
    """[(floor id, first twin id)] for each floor of kinds, for a ring's ON_LOAD
    (Ichor_AddThreadFloor: VAR_0x8004 = floor, VAR_0x8005 = first twin)."""
    out = []
    for kind in kinds:
        key = "thread" if kind == "dark" else "pools"
        for half in "lr":
            f = mid(tileset, key, f"{kind}_{half}")
            out.append((f, f + 1))
    return out


def autotile(grid, tileset="labyrinth"):
    """Metatile ids for a grid of booleans (True = wall): each wall cell gets
    its kit piece from `walls`; floor cells get None (lay floor())."""
    out = []
    for y, row in enumerate(grid):
        r = []
        for x, w in enumerate(row):
            r.append(mid(tileset, "walls", classify(grid, x, y)) if w else None)
        out.append(r)
    return out
'''
    body = "TILESETS = " + json.dumps(cur, indent=1, sort_keys=True).replace("null", "None") \
        .replace("true", "True").replace("false", "False")
    TILES_PY.parent.mkdir(parents=True, exist_ok=True)
    TILES_PY.write_text(head + src + "\n\n\n" + body + "\n" + funcs)
    print(TILES_PY)


# --------------------------------------------------------------------------

def build_one(name, compile_=True):
    spec = Spec(name)
    sections = A.build(name)
    structs = [s for _, ss in sections for s in ss]
    keys = [s.key for s in structs]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, f"duplicate structure keys {dup}"
    probs = A.validate(structs, spec.groups)
    if not probs:
        before = len(static_tiles(structs))
        merges = merge_near_duplicates(structs)
        print(f"{name}: merged {len(merges)} near-duplicate tiles "
              f"({merges.count(1)} differed by 1 px, {merges.count(2)} by 2): "
              f"{before} -> {len(static_tiles(structs))} distinct static tiles before palette "
              f"sharing")
        fix_keys(structs)
        probs = A.validate(structs, spec.groups)
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    rows = A.pack(sections)
    print(f"{name}: {sum(s.w * s.h for s in structs)} metatiles drawn, in {rows} sheet rows")
    write_sources(structs, rows, spec.src)
    write_anims(spec.src, structs)
    data = catalog_json(spec, structs)
    if not compile_:
        return
    animated = compile_tileset(spec)
    register(spec, animated)
    used = EB.verify(spec, rows, {})
    variant_palettes(spec)
    print("colors per palette 6-12:", EB.palette_report(spec))
    IMG.mkdir(parents=True, exist_ok=True)
    EB.images(spec, [s for s in structs if not s.key.endswith("_odd")])
    write_tiles_py(name, data)
    A.write_catalog(name, used, structs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tileset", nargs="?", default="all", choices=["labyrinth", "daidaleion", "mychos", "all"])
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    for name in (["labyrinth", "daidaleion"] if args.tileset == "all" else [args.tileset]):
        build_one(name, not args.no_compile)


if __name__ == "__main__":
    main()
