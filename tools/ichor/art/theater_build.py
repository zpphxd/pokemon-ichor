#!/usr/bin/env python3
"""Draw, compile and catalog Thyrsa's theater tilesets.

  gTileset_Theater   the theater, on the aethos primary (MAP_THYRSA_THEATER)
  gTileset_Skene     the stage building's backstage and prop room, on oikos
                     (MAP_THYRSA_THEATER_SKENE)

For each tileset:
1. Paints every structure. For the theater that is the cavea, cell by cell
   from the shared geometry (theater_cavea.py), the seated crowd for the
   Dionysia (each crowd cell once per pair of blocks it sits in), the stage
   side (theater_stage.py) and the props. The skene's art is theater_skene.py.
   Checks every 8x8 tile draws from one palette group.
2. Packs them first-fit into the 8-wide sheet from 0x200, in build order, and
   writes data/tilesets/secondary/<dir>/porytiles_src.
3. Compiles with Porytiles in a scratch project against an empty stand-in
   primary, so the art uses only its own tiles and palettes 6-12.
4. Theater only: copies the crowd's palette into three spare slots, one per
   pair of blocks (low, mid, top), and points each pair's crowd cells at its
   slot, so a pair's trance pulse can stop on its own (src/ichor_act2_scene.c).
   Then borrows aethos's grass for the cells drawn on it.
5. Verifies every entry and the 504-tile limit, writes build/<dir>/catalog.json
   (structures, and for the theater the cavea's cells by signature, so the map
   builder places exactly the cells painted), the metatile labels scripts swap,
   the sheet and the catalog design/phase3/TILES_theater.md.

Usage: /usr/bin/python3 tools/ichor/art/theater_build.py [theater|skene|all] [--no-compile]
"""
from __future__ import annotations

import argparse
import hashlib
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
import theater_cavea as V  # noqa: E402
import theater_lib as T  # noqa: E402
import theater_stage as S  # noqa: E402

ROOT = T.ROOT
COLS = 8
TILE_LIMIT = 504
IMG = ROOT / "design/phase3/img"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
LABELS = ROOT / "include/constants/metatile_labels.h"


def sig(layers):
    return hashlib.sha1(V.key_of(layers)).hexdigest()[:16]


# --------------------------------------------------------------------------
# The theater's structures
# --------------------------------------------------------------------------

def cell_struct(key, title, section, layers):
    s = T.Struct(key, title, 1, 1, section, walk=["X"])
    for ln in ("bottom", "middle", "top"):
        s.layers[ln].a[:] = layers[ln]
    if not (layers["bottom"][..., 3] > 0).any() and (layers["middle"][..., 3] == 0).any():
        s.ground = {(0, 0): "grass"}     # the promenade's edge on the terrace's grass
    return s


def cavea_structs():
    """The cavea's cells: every distinct empty cell once, then every distinct
    crowd cell once per pair of blocks it sits in."""
    empty, crowd = {}, {p: {} for p in T.PAIRS}
    order_e, order_c = [], []
    for (cx, cy) in V.cavea_cells():
        le = V.paint_cell(cx, cy, False)
        se = sig(le)
        if se not in empty:
            empty[se] = cell_struct(f"cavea_{len(order_e):03d}", "A cell of the cavea", "cavea", le)
            order_e.append(empty[se])
        lf = V.paint_cell(cx, cy, True)
        sf = sig(lf)
        if sf == se:
            continue
        pair = T.pair_of_block(T.block_of_cell(cx, cy)) or "top"
        if sf not in crowd[pair]:
            s = cell_struct(f"crowd_{pair}_{len(crowd[pair]):03d}",
                            f"A cell of the crowd, {pair} blocks", "crowd", lf)
            s.pair = pair
            crowd[pair][sf] = s
            order_c.append(s)
    return order_e, order_c, empty, crowd


def theater_sections():
    e, c, empty, crowd = cavea_structs()
    return [("cavea", e), ("crowd", c), ("stage", S.build()), ("props", S.build_props())], \
        {"cavea": {k: s for k, s in empty.items()},
         "crowd": {p: {k: s for k, s in d.items()} for p, d in crowd.items()}}


def skene_sections():
    import theater_skene as K
    return K.sections(), {}


TILESETS = {
    "theater": {
        "name": "gTileset_Theater", "dir": "theater", "primary": "aethos",
        "groups": T.GROUPS, "sections": theater_sections,
        "section_rows": {"cavea": 0, "crowd": 23, "stage": 44, "props": 54},
        "doc": "TILES_theater.md",
    },
    "skene": {
        "name": "gTileset_Skene", "dir": "skene", "primary": "oikos",
        "groups": None, "sections": skene_sections,
        "section_rows": None,
        "doc": "TILES_theater.md",
    },
}


# --------------------------------------------------------------------------
# Packing and sources
# --------------------------------------------------------------------------

def pack(secs, section_rows):
    used = np.zeros((64, COLS), bool)
    total = 0
    for name, structs in secs:
        start = (section_rows or {}).get(name, 0)
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
                total = max(total, row + s.h)
        print(f"  {name}: {len(structs)} structures")
    return total, used


def write_sources(cfg, structs, rows, used):
    src = ROOT / "data/tilesets/secondary" / cfg["dir"] / "porytiles_src"
    src.mkdir(parents=True, exist_ok=True)
    W, H = COLS * 16, rows * 16
    sheets = {ln: np.zeros((H, W, 4), np.uint8) for ln in ("bottom", "middle", "top")}
    # unused cells are opaque, so every metatile has a bottom (Porytiles needs no holes there)
    filler = T.Layer(16, 16)
    filler.rect(0, 0, 16, 16, "ink")
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
        Image.fromarray(a, "RGBA").save(src / f"{ln}.png")
    lines = ["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh)]
    (src / "attributes.csv").write_text("\n".join(lines) + "\n")


# --------------------------------------------------------------------------
# Porytiles
# --------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"theater_build: failed: {' '.join(map(str, cmd))}")
    return r


def palette_hints(groups):
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in groups.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = T.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


def compile_tileset(cfg, groups):
    name, d = cfg["name"], cfg["dir"]
    scratch = ROOT / "build" / f"{d}_porytiles"
    src = ROOT / "data/tilesets/secondary" / d / "porytiles_src"
    binp = ROOT / "data/tilesets/secondary" / d / "porytiles_bin"
    conf = ROOT / "porytiles/tilesets" / name
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
    stubname = name + "Stub"
    run([pt, "create-tileset", "-C", str(scratch), stubname])
    stubdir = next((scratch / "data/tilesets/primary").iterdir()) / "porytiles_src"
    shutil.rmtree(stubdir / "anim", ignore_errors=True)
    (stubdir / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stubdir / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(scratch), stubname])
    sconf = scratch / "porytiles/tilesets" / name
    sconf.mkdir(parents=True)
    pairing = f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [{stubname}]\n"
    (sconf / "config.yaml").write_text(pairing)
    sec = scratch / "data/tilesets/secondary" / d
    short = name.removeprefix("gTileset_")
    for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h"):
        p = scratch / rel
        t = p.read_text()
        t = re.sub(rf"const struct Tileset {name}\s*=\s*\{{.*?\}};\n", "", t, flags=re.S)
        t = re.sub(rf"const u16 gTilesetPalettes_PorytilesManaged_{short}\[\]\[16\]\s*=\s*\{{.*?\}};\n",
                   "", t, flags=re.S)
        t = "\n".join(line for line in t.split("\n")
                      if not re.search(rf"PorytilesManaged_{short}(?!Stub)\b", line))
        p.write_text(t)
    run([pt, "create-tileset", "-C", str(scratch), "--secondary", name])
    shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(src, sec / "porytiles_src")
    (sconf / "config.yaml").write_text(pairing + palette_hints(groups))
    r = run([pt, "compile-tileset", "-C", str(scratch), "--no-verify-checksums", name])
    out = (r.stdout + r.stderr).strip()
    if out:
        print(out[-1500:])
    if binp.exists():
        shutil.rmtree(binp)
    shutil.copytree(sec / "porytiles_bin", binp)
    conf.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        if (sconf / f).exists():
            shutil.copy2(sconf / f, conf / f)
    (conf / "config.yaml").write_text(
        f"# Per-tileset Porytiles config for {name}, Thyrsa's theater.\n"
        "# Written by tools/ichor/art/theater_build.py, which compiles it against an empty\n"
        "# stand-in primary (and for the theater copies the crowd's palette and borrows\n"
        "# aethos's grass afterwards). Rebuild it with that script, not porytiles.\n"
        f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_{cfg['primary'].capitalize()}]\n"
        + palette_hints(groups))


# --------------------------------------------------------------------------
# After the compile: the crowd's palettes, borrowed grass, checks
# --------------------------------------------------------------------------

def read_pal(p):
    vals = [int(v) for v in p.read_text().split()[3:]]
    return [tuple(vals[i:i + 3]) for i in range(0, 48, 3)]


def write_pal(p, colors):
    lines = ["JASC-PAL", "0100", "16"] + [f"{r} {g} {b}" for r, g, b in colors]
    p.write_text("\n".join(lines) + "\n")


NORMAL, COVERED, SPLIT = 0, 1, 2


def crowd_palettes(binp, crowd_structs):
    """Find the crowd's palette, copy it into three spare slots and point each
    pair's crowd cells at its own copy. Returns {pair: slot, 'base': slot}."""
    pals = {i: read_pal(binp / "palettes" / f"{i:02d}.pal") for i in range(16)}
    marker = T.C["qcp"]
    base = next(i for i in range(6, 13) if marker in pals[i])
    used = set()
    meta = np.fromfile(binp / "metatiles.bin", "<u2").reshape(-1, 8)
    for e in meta.ravel():
        if int(e) & 0x3FF or int(e) >> 12:
            used.add(int(e) >> 12)
    free = [i for i in range(6, 13) if i not in used]
    assert len(free) >= 3, f"need three spare palettes for the crowd, have {free}"
    slots = {"base": base}
    for pair, slot in zip(T.PAIRS, free[-3:]):
        slots[pair] = slot
        write_pal(binp / "palettes" / f"{slot:02d}.pal", pals[base])
    for s in crowd_structs:
        slot = slots[s.pair]
        i = s.ids[0][0] - 0x200
        for j in range(8):
            e = int(meta[i, j])
            if (e >> 12) == base:
                meta[i, j] = (e & 0x0FFF) | (slot << 12)
    meta.astype("<u2").tofile(binp / "metatiles.bin")
    return slots


def borrow_ground(binp, structs):
    """Cells drawn on grass get aethos's grass as their bottom layer."""
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    meta = np.fromfile(binp / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(binp / "metatile_attributes.bin", "<u2")
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
    meta.astype("<u2").tofile(binp / "metatiles.bin")
    attrs.astype("<u2").tofile(binp / "metatile_attributes.bin")
    return patched


def verify(binp, rows, patched, tag):
    raw = np.fromfile(binp / "metatiles.bin", "<u2").reshape(-1, 8)
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
        sys.exit(f"theater_build ({tag}): entries outside its own tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(binp / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    print(f"{tag}: verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{len(patched)} cells on aethos grass")
    if used > TILE_LIMIT or late:
        sys.exit(f"theater_build ({tag}): {used} tiles, tiles {late[:8]} referenced; the door "
                 f"animations overwrite tiles {TILE_LIMIT}-511")
    return used, len(raw)


# --------------------------------------------------------------------------
# Catalog, labels, images
# --------------------------------------------------------------------------

def write_labels(tag, secs, want):
    start = f"// {tag}: written by tools/ichor/art/theater_build.py"
    end = f"// end {tag}"
    lines = [start]
    for _, structs in secs:
        for s in structs:
            for piece, label in want.get(s.key, ()):
                cx, cy = s.names[piece]
                lines.append(f"#define METATILE_{label:<32} 0x{s.ids[cy][cx]:03X}")
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


THEATER_LABELS = {
    "door_ivy": [("closed_00", "Theater_DoorIvy_Top"), ("closed_10", "Theater_DoorIvy_Bottom"),
                 ("open_00", "Theater_DoorIvyOpen_Top"), ("open_10", "Theater_DoorIvyOpen_Bottom")],
    "door_crown": [("closed_00", "Theater_DoorCrown_TopL"), ("closed_01", "Theater_DoorCrown_TopR"),
                   ("closed_10", "Theater_DoorCrown_BottomL"), ("closed_11", "Theater_DoorCrown_BottomR"),
                   ("open_00", "Theater_DoorCrownOpen_TopL"), ("open_01", "Theater_DoorCrownOpen_TopR"),
                   ("open_10", "Theater_DoorCrownOpen_BottomL"), ("open_11", "Theater_DoorCrownOpen_BottomR")],
    "door_goat": [("closed_00", "Theater_DoorGoat_Top"), ("closed_10", "Theater_DoorGoat_Bottom"),
                  ("open_00", "Theater_DoorGoatOpen_Top"), ("open_10", "Theater_DoorGoatOpen_Bottom")],
    "torch_lit_pave": [("head", "Theater_TorchLit_Head"), ("foot", "Theater_TorchLit_Foot")],
    "torch_cold_pave": [("head", "Theater_TorchCold_Head"), ("foot", "Theater_TorchCold_Foot")],
    "thymele": [("tl", "Theater_Thymele_TL"), ("tr", "Theater_Thymele_TR"),
                ("bl", "Theater_Thymele_BL"), ("br", "Theater_Thymele_BR")],
    "thymele_ink": [("tl", "Theater_ThymeleInk_TL"), ("tr", "Theater_ThymeleInk_TR"),
                    ("bl", "Theater_ThymeleInk_BL"), ("br", "Theater_ThymeleInk_BR")],
    "loom": [("top", "Theater_Loom_Top"), ("bottom", "Theater_Loom_Bottom")],
    "loom_fallen": [("top", "Theater_LoomFallen_Top"), ("bottom", "Theater_LoomFallen_Bottom")],
    "vine": [("top", "Theater_Vine_Top"), ("bottom", "Theater_Vine_Bottom")],
    "vine_cut": [("top", "Theater_VineCut_Top"), ("bottom", "Theater_VineCut_Bottom")],
    "stage": [("back_a", "Theater_Stage_BackA"), ("back_b", "Theater_Stage_BackB"),
              ("front_a", "Theater_Stage_FrontA"), ("front_b", "Theater_Stage_FrontB")],
}


def catalog(cfg, secs, extra, slots):
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
    out = {"structures": data}
    if extra:
        out["cavea"] = {k: s.ids[0][0] for k, s in extra["cavea"].items()}
        out["crowd"] = {p: {k: s.ids[0][0] for k, s in d.items()} for p, d in extra["crowd"].items()}
    if slots:
        out["palettes"] = slots
    d = ROOT / "build" / cfg["dir"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "catalog.json").write_text(json.dumps(out, indent=1))
    return out


def images(cfg, secs):
    IMG.mkdir(parents=True, exist_ok=True)
    allst = [s for n, ss in secs for s in ss if n not in ("cavea", "crowd")]
    if allst:
        E.preview(allst, scale=2, cols=4).save(IMG / f"{cfg['dir']}_pieces.png")
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", cfg["name"],
         "--primary", cfg["primary"], "--scale", "2", "-o", str(IMG / f"{cfg['dir']}_sheet.png")])


# --------------------------------------------------------------------------

def build_one(tag, no_compile=False):
    cfg = TILESETS[tag]
    secs, extra = cfg["sections"]()
    if tag == "skene":
        import theater_skene as K
        cfg["groups"] = K.GROUPS
        cfg["section_rows"] = K.SECTION_ROWS
    groups = cfg["groups"]
    group_rgb = {g: {T.C[n] for n in names} for g, names in groups.items()}
    allst = [s for _, ss in secs for s in ss]
    keys = [s.key for s in allst]
    assert len(keys) == len(set(keys)), "duplicate structure keys"
    probs = E.validate(allst, group_rgb)
    for p in probs[:30]:
        print("PROBLEM:", p)
    if probs:
        sys.exit(f"theater_build ({tag}): {len(probs)} palette or layer problems")
    print(f"{tag}: {len(E.tiles_of(allst))} distinct tiles before Porytiles")
    rows, used = pack(secs, cfg["section_rows"])
    write_sources(cfg, allst, rows, used)
    if no_compile:
        return
    compile_tileset(cfg, groups)
    binp = ROOT / "data/tilesets/secondary" / cfg["dir"] / "porytiles_bin"
    slots = None
    if tag == "theater":
        crowd = [s for n, ss in secs if n == "crowd" for s in ss]
        slots = crowd_palettes(binp, crowd)
        print(f"theater: crowd palettes {slots}")
    patched = borrow_ground(binp, allst) if cfg["primary"] == "aethos" else {}
    used_tiles, nmeta = verify(binp, rows, patched, tag)
    catalog(cfg, secs, extra, slots)
    if tag == "theater":
        write_labels("gTileset_Theater (Ichor: Thyrsa's theater)", secs, THEATER_LABELS)
    else:
        import theater_skene as K
        write_labels("gTileset_Skene (Ichor: the theater's skene)", secs, K.LABELS)
    images(cfg, secs)
    return used_tiles, nmeta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("which", nargs="?", default="all", choices=("theater", "skene", "all"))
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    for tag in (("theater", "skene") if args.which == "all" else (args.which,)):
        build_one(tag, args.no_compile)


if __name__ == "__main__":
    main()
