#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Kopais, Route 8's secondary (the Kopais shore).

Steps (as kithairon_build.py, for one set):
1. Paint every structure (kopais_marsh, kopais_stone, kopais_gear), check each
   8x8 tile draws from one palette group (kopais_lib.GROUPS), and merge tiles
   within 2 px of each other, except in animated pieces (their frames must
   match their key frame pixel for pixel).
2. Pack into the 8-wide sheet, first fit, in order.
3. Write data/tilesets/secondary/kopais/porytiles_src, compile with Porytiles in a
   scratch project against an empty stand-in primary, and point every
   borrowed-ground cell's bottom at aethos's grass, road or water.
4. Animate: paint the animated pieces again for phases 1-3, find the tiles each
   one's cells compiled to, and write their frames as indexed PNGs under
   data/tilesets/secondary/kopais/anim/ (make turns them into .4bpp) and the C
   that copies them into VRAM, src/data/tilesets/kopais_anims.h (included at the
   end of src/tileset_anims.c; gTileset_Kopais's callback is InitTilesetAnim_Kopais).
5. Verify, fail past 504 tiles, write build/kopais/catalog.json, the sheet and
   design/phase3/TILES_kopais.md.

Usage: /usr/bin/python3 tools/ichor/art/kopais_build.py [--no-compile]
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
import kopais_gear  # noqa: E402
import kopais_lib as K  # noqa: E402
import kopais_marsh  # noqa: E402
import kopais_stone  # noqa: E402

ROOT = K.ROOT
OUT = ROOT / "build/kopais"
IMG = ROOT / "design/phase3/img"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
COLS = 8
TILE_LIMIT = 504
NEAR_DUPLICATE_PX = 2
SYMBOL, DIR, LABEL = "gTileset_Kopais", "kopais", "Kopais"
TITLE = "Route 8, the Kopais shore"
SRC = ROOT / f"data/tilesets/secondary/{DIR}/porytiles_src"
BIN = ROOT / f"data/tilesets/secondary/{DIR}/porytiles_bin"
ANIM = ROOT / f"data/tilesets/secondary/{DIR}/anim"
ANIM_H = ROOT / "src/data/tilesets/kopais_anims.h"
ANIM_PERIOD = 24          # frames per phase: four phases, about 1.6 s a cycle

SECTIONS = [
    ("ground", ["reeds", "marsh", "lake", "mud", "path", "barley", "crag"]),
    ("stone", ["rock_bits", "sphinx", "markers", "dike", "tholos", "gla"]),
    ("gear", ["hide", "nets", "traps", "rack", "boat", "nest", "jetty", "water_bits"]),
]
SECTION_TITLES = {
    "ground": "Soft ground: reeds, marsh water, the lake, mudflats, the road, barley, rock",
    "stone": "Phikion's rock and the Minyans' stonework",
    "gear": "The marsh people's gear, and things in the water",
}


def painted(phase=0):
    ss = {}
    for mod in (kopais_marsh, kopais_stone, kopais_gear):
        for s in mod.build(phase):
            assert s.key not in ss, s.key
            ss[s.key] = s
    return ss


def ordered(ss):
    return [(sec, [ss[k] for k in keys]) for sec, keys in SECTIONS]


# --------------------------------------------------------------------------
# Packing and sources (as kithairon_build)
# --------------------------------------------------------------------------

def pack(secs):
    used = np.zeros((64, COLS), bool)
    ids, rows = {}, 0
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


def write_sources(secs, ids, rows):
    if SRC.exists():
        shutil.rmtree(SRC)
    SRC.mkdir(parents=True)
    sheets = {ln: np.zeros((rows * 16, COLS * 16, 4), np.uint8) for ln in ("bottom", "middle", "top")}
    beh = {}
    for _, structs in secs:
        for s in structs:
            g = ids[s.key]
            for cy in range(s.h):
                for cx in range(s.w):
                    r, c = divmod(g[cy][cx] - 0x200, COLS)
                    for ln in sheets:
                        sheets[ln][r * 16:r * 16 + 16, c * 16:c * 16 + 16] = \
                            s.layers[ln].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            for (x, y), mb in s.behaviors.items():
                if mb:
                    beh[g[y][x] - 0x200] = mb
    for ln, a in sheets.items():
        Image.fromarray(a, "RGBA").save(SRC / f"{ln}.png")
    (SRC / "attributes.csv").write_text(
        "\n".join(["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh)]) + "\n")


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"kopais_build: failed: {' '.join(map(str, cmd))}")
    return r


def palette_hints():
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in K.GROUPS.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = K.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


def compile_set():
    name = SYMBOL
    scratch = ROOT / f"build/{DIR}_porytiles"
    cfg = ROOT / "porytiles/tilesets" / name
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
    stub_name = "gTileset_KopaisStub"
    run([pt, "create-tileset", "-C", str(scratch), stub_name])
    stub = scratch / "data/tilesets/primary/kopais_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(scratch), stub_name])
    scfg = scratch / "porytiles/tilesets" / name
    scfg.mkdir(parents=True)
    pairing = f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [{stub_name}]\n"
    (scfg / "config.yaml").write_text(pairing)
    sec = scratch / f"data/tilesets/secondary/{DIR}"
    short = name.replace("gTileset_", "")
    for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h"):
        p = scratch / rel
        t = p.read_text()
        t = re.sub(rf"const struct Tileset {name}\s*=\s*\{{.*?\}};\n", "", t, flags=re.S)
        t = re.sub(rf"const u16 gTilesetPalettes_PorytilesManaged_{short}\[\]\[16\]\s*=\s*\{{.*?\}};\n",
                   "", t, flags=re.S)
        t = "\n".join(line for line in t.split("\n")
                      if not re.search(rf"PorytilesManaged_{short}\b", line))
        p.write_text(t)
    run([pt, "create-tileset", "-C", str(scratch), "--secondary", name])
    shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(SRC, sec / "porytiles_src")
    (scfg / "config.yaml").write_text(pairing + palette_hints())
    r = run([pt, "compile-tileset", "-C", str(scratch), "--no-verify-checksums", name])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-1500:])
    if BIN.exists():
        shutil.rmtree(BIN)
    shutil.copytree(sec / "porytiles_bin", BIN)
    cfg.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        if (scfg / f).exists():
            shutil.copy2(scfg / f, cfg / f)
    (cfg / "config.yaml").write_text(
        f"# Per-tileset Porytiles config for {name} ({TITLE}).\n"
        "# Written by tools/ichor/art/kopais_build.py, which compiles it against an empty\n"
        "# stand-in primary, then points its ground cells at aethos's grass, road and\n"
        "# water, and writes its tile animation. Pair it with aethos when compiling it directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + palette_hints())


NORMAL, COVERED, SPLIT = 0, 1, 2


def borrow_ground(secs, ids):
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    meta = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(BIN / "metatile_attributes.bin", "<u2")
    patched = {}
    for _, structs in secs:
        for s in structs:
            for (cx, cy), kind in getattr(s, "ground", {}).items():
                i = ids[s.key][cy][cx] - 0x200
                sl = np.s_[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                on_top = bool((s.T.a[sl][..., 3] > 0).any())
                lt = int(attrs[i]) >> 12
                ent = [int(e) for e in meta[i]]
                art = ent[4:8] if any(ent[4:8]) else ent[0:4]
                if on_top and lt == NORMAL:
                    art = ent[4:8]
                meta[i, 0:4] = aethos[K.GROUND_METATILE[kind], 0:4]
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
                if e != int(aethos[K.GROUND_METATILE[patched[i]], j]):
                    bad.append((0x200 + i, j, "ground"))
                continue
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                continue
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"kopais_build: entries outside its tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    print(f"{SYMBOL}: {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{len(patched)} cells on aethos ground")
    if used > TILE_LIMIT or late:
        sys.exit(f"kopais_build: {used} tiles; door animations overwrite {TILE_LIMIT}-511")
    return used


# --------------------------------------------------------------------------
# The tile animation
# --------------------------------------------------------------------------

def read_pal(path):
    lines = Path(path).read_text().split()
    n = int(lines[2])
    vals = list(map(int, lines[3:3 + 3 * n]))
    return [tuple(vals[i:i + 3]) for i in range(0, 3 * n, 3)]


def animated_entries(ss, ids, patched, meta, attrs):
    """(tile, palette, hflip, vflip, struct key, layer, x0, y0) for every tile
    entry of every animated cell."""
    out = []
    for key, s in ss.items():
        if not getattr(s, "anim", None):
            continue
        g = ids[key]
        for cy in range(s.h):
            for cx in range(s.w):
                i = g[cy][cx] - 0x200
                lt = int(attrs[i]) >> 12
                lower, upper = {NORMAL: ("middle", "top"), COVERED: ("bottom", "middle"),
                                SPLIT: ("bottom", "top")}[lt]
                for j in range(8):
                    if j < 4 and i in patched:
                        continue
                    e = int(meta[i, j])
                    t, hf, vf, pal = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
                    if t < 512 or (t == 0 and pal == 0):
                        continue
                    k = j % 4
                    out.append((t - 512, pal, hf, vf, key, lower if j < 4 else upper,
                                cx * 16 + (k % 2) * 8, cy * 16 + (k // 2) * 8))
    return out


def repalette(ss, frames_ss, ids, patched):
    """Porytiles picks a tile's palette from its key frame's colors; a frame may
    bring in a color that palette lacks (a glint, a cattail swaying in). Move
    each such tile to a palette that holds every color of every frame."""
    meta = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(BIN / "metatile_attributes.bin", "<u2")
    img = Image.open(BIN / "tiles.png")
    raw = np.array(img)
    tw = raw.shape[1] // 8
    pals = {p: read_pal(BIN / "palettes" / f"{p:02d}.pal") for p in range(6, 13)}
    need = {}
    cur = {}
    for (t, pal, hf, vf, key, ln, x0, y0) in animated_entries(ss, ids, patched, meta, attrs):
        cur.setdefault(t, set()).add(pal)
        for p in range(K.PHASES):
            a = frames_ss[p][key].layers[ln].a[y0:y0 + 8, x0:x0 + 8]
            need.setdefault(t, set()).update(tuple(int(v) for v in px[:3]) for px in a.reshape(-1, 4)
                                             if px[3] > 0)
    moved = 0
    for t, cols in need.items():
        (pal,) = cur[t] if len(cur[t]) == 1 else (sorted(cur[t])[0],)
        if cols <= set(pals[pal]):
            continue
        better = [p for p in range(6, 13) if cols <= set(pals[p])]
        if not better:
            sys.exit(f"kopais_build: animated tile {t} needs {[K.A.RGB2NAME.get(c, c) for c in cols]}, "
                     "which no palette holds")
        users = [(i, j) for i in range(len(meta)) for j in range(8)
                 if not (j < 4 and i in patched) and (int(meta[i, j]) & 0x3FF) == t + 512]
        if len({int(meta[i, j]) >> 12 for (i, j) in users}) > 1:
            sys.exit(f"kopais_build: tile {t} is shared across palettes; can't move it")
        p2 = better[0]
        ty, tx = divmod(t, tw)
        blk = raw[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
        for yy in range(8):
            for xx in range(8):
                v = int(blk[yy, xx])
                if v % 16 == 0:
                    continue
                rgb = pals[pal][v % 16]
                blk[yy, xx] = p2 * 16 + pals[p2].index(rgb)
        for (i, j) in users:
            meta[i, j] = (int(meta[i, j]) & 0x0FFF) | (p2 << 12)
        moved += 1
    if moved:
        out = Image.fromarray(raw, "P")
        out.putpalette(img.getpalette())
        out.save(BIN / "tiles.png")
        meta.astype("<u2").tofile(BIN / "metatiles.bin")
    print(f"animation: {moved} tiles moved to a palette that holds their frames' colors")


def animate(ss, ids, patched):
    """Find the compiled tiles of every animated piece and write their frames.
    Returns (tile count, run count)."""
    frames_ss = [ss] + [painted(p) for p in range(1, K.PHASES)]
    repalette(ss, frames_ss, ids, patched)
    meta = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(BIN / "metatile_attributes.bin", "<u2")
    tiles_img = Image.open(BIN / "tiles.png")
    assert tiles_img.mode == "P", tiles_img.mode
    tiles = np.array(tiles_img) & 0x0F       # porytiles writes palette * 16 + index
    tw = tiles.shape[1] // 8
    pals = {p: read_pal(BIN / "palettes" / f"{p:02d}.pal") for p in range(6, 13)}
    found = {}           # tile index -> [frame arrays]
    conflicts = 0
    for key, s in ss.items():
        if not getattr(s, "anim", None):
            continue
        g = ids[key]
        for cy in range(s.h):
            for cx in range(s.w):
                i = g[cy][cx] - 0x200
                lt = int(attrs[i]) >> 12
                lower, upper = {NORMAL: ("middle", "top"), COVERED: ("bottom", "middle"),
                                SPLIT: ("bottom", "top")}[lt]
                for j in range(8):
                    if j < 4 and i in patched:
                        continue
                    e = int(meta[i, j])
                    t, hf, vf, pal = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
                    if t < 512 or (t == 0 and pal == 0):
                        continue
                    t -= 512
                    ln = lower if j < 4 else upper
                    k = j % 4
                    x0, y0 = cx * 16 + (k % 2) * 8, cy * 16 + (k // 2) * 8
                    fr = []
                    for p in range(K.PHASES):
                        a = frames_ss[p][key].layers[ln].a[y0:y0 + 8, x0:x0 + 8]
                        if hf:
                            a = a[:, ::-1]
                        if vf:
                            a = a[::-1, :]
                        idx = np.zeros((8, 8), np.uint8)
                        for yy in range(8):
                            for xx in range(8):
                                if a[yy, xx, 3] == 0:
                                    continue
                                rgb = tuple(int(v) for v in a[yy, xx, :3])
                                if rgb not in pals[pal]:
                                    sys.exit(f"kopais_build: {key} ({cx},{cy}) phase {p}: color "
                                             f"{K.A.RGB2NAME.get(rgb, rgb)} not in palette {pal}")
                                idx[yy, xx] = pals[pal].index(rgb)
                        fr.append(idx)
                    ty, tx = divmod(t, tw)
                    key0 = tiles[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                    if not (fr[0] == key0).all():
                        sys.exit(f"kopais_build: {key} ({cx},{cy}) entry {j}: the key frame "
                                 f"doesn't match tile {t}")
                    if t in found:
                        if any(not (a == b).all() for a, b in zip(found[t], fr)):
                            conflicts += 1
                        continue
                    found[t] = fr
    moving = sorted(t for t, fr in found.items() if any(not (f == fr[0]).all() for f in fr[1:]))
    # copy runs of consecutive tiles, bridging gaps of up to two static tiles
    runs = []
    for t in moving:
        if runs and t - runs[-1][-1] <= 3:
            runs[-1].extend(range(runs[-1][-1] + 1, t + 1))
        else:
            runs.append([t])
    if ANIM.exists():
        shutil.rmtree(ANIM)
    ANIM.mkdir(parents=True)
    pal_img = [v for i in range(16) for v in (i * 16, i * 16, i * 16)]
    for r, run_ in enumerate(runs):
        for p in range(K.PHASES):
            img = np.zeros((8, 8 * len(run_)), np.uint8)
            for n, t in enumerate(run_):
                if t in found:
                    img[:, n * 8:n * 8 + 8] = found[t][p]
                else:
                    ty, tx = divmod(t, tw)
                    img[:, n * 8:n * 8 + 8] = tiles[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            im = Image.fromarray(img, "P")
            im.putpalette(pal_img)
            im.save(ANIM / f"run{r:02d}_{p}.png")
    write_anim_c(runs)
    print(f"animation: {len(moving)} moving tiles in {len(runs)} runs; {conflicts} shared-tile "
          f"conflicts (first painter wins)")
    return len(moving), len(runs)


def write_anim_c(runs):
    rel = f"data/tilesets/secondary/{DIR}/anim"
    out = ["// Ichor: gTileset_Kopais's tile animation (Route 8): the reeds sway, the marsh",
           "// water glints, the eel-smoker's fire flickers. Written by",
           "// tools/ichor/art/kopais_build.py, which finds the compiled tiles of every",
           "// animated piece; included at the end of src/tileset_anims.c. Do not edit.",
           "#ifndef GUARD_KOPAIS_ANIMS_H", "#define GUARD_KOPAIS_ANIMS_H", ""]
    for r, run_ in enumerate(runs):
        for p in range(K.PHASES):
            out.append(f"static const u16 sKopaisAnim_Run{r}_{p}[] = INCBIN_U16(\"{rel}/run{r:02d}_{p}.4bpp\");")
        out.append(f"static const u16 *const sKopaisAnim_Run{r}[] = {{"
                   + ", ".join(f"sKopaisAnim_Run{r}_{p}" for p in range(K.PHASES)) + "};")
    out.append("")
    out.append("struct KopaisAnimRun { const u16 *const *frames; u16 tile; u16 count; };")
    out.append("static const struct KopaisAnimRun sKopaisAnimRuns[] = {")
    for r, run_ in enumerate(runs):
        out.append(f"    {{sKopaisAnim_Run{r}, {run_[0]}, {len(run_)}}},")
    out.append("};")
    out.append("")
    out.append(f"#define KOPAIS_ANIM_PERIOD {ANIM_PERIOD}")
    out.append("#define KOPAIS_ANIM_BATCH 6")
    out.append("")
    out.append("// Each phase change copies the runs a few at a time over consecutive frames,")
    out.append("// so the transfer buffer (20 slots) never fills.")
    out.append("static void TilesetAnim_Kopais(u16 timer)")
    out.append("{")
    out.append("    u16 step = timer % KOPAIS_ANIM_PERIOD;")
    out.append(f"    u16 phase = (timer / KOPAIS_ANIM_PERIOD) % {K.PHASES};")
    out.append("    u16 i;")
    out.append("    for (i = step * KOPAIS_ANIM_BATCH; i < (step + 1) * KOPAIS_ANIM_BATCH && i < ARRAY_COUNT(sKopaisAnimRuns); i++)")
    out.append("        AppendTilesetAnimToBuffer(sKopaisAnimRuns[i].frames[phase],")
    out.append("                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + sKopaisAnimRuns[i].tile)),")
    out.append("                                  sKopaisAnimRuns[i].count * TILE_SIZE_4BPP);")
    out.append("}")
    out.append("")
    out.append("void InitTilesetAnim_Kopais(void)")
    out.append("{")
    out.append("    sSecondaryTilesetAnimCounter = 0;")
    out.append(f"    sSecondaryTilesetAnimCounterMax = KOPAIS_ANIM_PERIOD * {K.PHASES} * 2;")
    out.append("    sSecondaryTilesetAnimCallback = TilesetAnim_Kopais;")
    out.append("}")
    out.append("")
    out.append("#endif // GUARD_KOPAIS_ANIMS_H")
    ANIM_H.write_text("\n".join(out) + "\n")
    assert (len(runs) + 5) // 6 <= ANIM_PERIOD, "too many runs to copy in one phase"


# --------------------------------------------------------------------------
# Catalog, labels, images
# --------------------------------------------------------------------------

def catalog(secs, ids):
    data = []
    for sec, structs in secs:
        for s in structs:
            data.append({
                "key": s.key, "title": s.title, "section": sec, "w": s.w, "h": s.h,
                "ids": ids[s.key], "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items() if mb},
                "ground": {f"{x},{y}": g for (x, y), g in getattr(s, "ground", {}).items()},
                "anim": getattr(s, "anim", None),
            })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps({"symbol": SYMBOL, "structures": data}, indent=1))


def images():
    IMG.mkdir(parents=True, exist_ok=True)
    out = IMG / "tiles_kopais_sheet.png"
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", SYMBOL,
         "--primary", "aethos", "--scale", "2", "-o", str(out)])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    ss = painted()
    probs = K.validate(list(ss.values()))
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    still = [s for s in ss.values() if not getattr(s, "anim", None)]
    n0 = len(K.tiles_of(list(ss.values())))
    K.merge_near_duplicates(still, NEAR_DUPLICATE_PX)
    print(f"tiles: {n0} -> {len(K.tiles_of(list(ss.values())))} after merging (animated pieces untouched)")
    probs = K.validate(list(ss.values()))
    if probs:
        for p in probs:
            print("PROBLEM:", p)
        sys.exit(1)
    secs = ordered(ss)
    ids, rows = pack(secs)
    print(f"{rows} sheet rows, {rows * 8} metatiles")
    write_sources(secs, ids, rows)
    catalog(secs, ids)
    if args.no_compile:
        return
    compile_set()
    patched = borrow_ground(secs, ids)
    used = verify(rows, patched)
    moving, nruns = animate(ss, ids, patched)
    print(images().relative_to(ROOT))
    import kopais_catalog
    kopais_catalog.main(used, rows * 8, secs, ids, moving, nruns)


if __name__ == "__main__":
    main()
