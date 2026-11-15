#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_CaveDark, the secondary of Ichor's dark places.

1. Paints every structure: the kit (rock with depth, floor, lit floor,
   still water: cave_dark_kit.py), the cave's furniture (cave_dark_props.py)
   and the pieces of the four places (cave_dark_places.py). Checks each 8x8
   tile draws from one palette group.
2. Packs them into the 8-wide metatile sheet; each section starts on a fixed
   row, so growing one section never renumbers another.
3. Writes data/tilesets/secondary/cave_dark/porytiles_src.
4. Compiles with Porytiles in a scratch project (build/cave_dark_porytiles)
   against an empty stand-in primary, so CaveDark uses only its own tiles
   and palettes 6-12, copies porytiles_bin and the Porytiles cache back, and
   verifies every metatile entry and the 504-tile budget.
5. Writes the glow palettes (SYSTEMS.md §2, dousing) next to the compiled
   ones, data/tilesets/secondary/cave_dark/catalog.json (map builders read
   it), the metatile labels scripts swap in, and the numbered sheet.

Usage: /usr/bin/python3 tools/ichor/art/cave_dark_build.py [--no-compile] [--preview out.png]
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
import cave_dark_kit as kit  # noqa: E402
import cave_dark_lib as lib  # noqa: E402
from cave_dark_lib import ROOT, Struct, composite, pack, preview, validate, write_sources  # noqa: E402

NAME = "gTileset_CaveDark"
TS = ROOT / "data/tilesets/secondary/cave_dark"
SRC = TS / "porytiles_src"
BIN = TS / "porytiles_bin"
GLOW = TS / "glow"
CATALOG = TS / "catalog.json"
CFG = ROOT / "porytiles/tilesets" / NAME
SCRATCH = ROOT / "build/cave_dark_porytiles"
SHEET = ROOT / "design/phase2/img/cave_dark_sheet.png"
TILE_LIMIT = 504          # CLAUDE.md: tiles 504-511 of a secondary are the door animations'

# First metatile row of each section (8 metatiles a row; id = 0x200 + row*8 + col).
SECTION_ROWS = {"kit": 0, "cave": 24, "places": 42}
SECTION_TITLES = {
    "kit": "The kit: rock with depth, floor, lit floor, still water",
    "cave": "The cave's furniture: stone, light, fire, webs, Hecate",
    "places": "The four places: the crypt and the sea grottos",
}


def kit_structs():
    """Every kit cell as a 1x1 Struct, named by its autotile key."""
    out = []
    order = {"T": 0, "ft": 1, "fb": 2, "floor": 3, "lit": 4, "water": 5}
    cells = kit.kit_cells()
    for key in sorted(cells, key=lambda k: (order[k.split("|")[0]], k)):
        layers, walk, mb = cells[key]
        s = lib.one(key, key, "kit", layers, walk=walk, floor_mb=mb if walk == "." else None)
        out.append(s)
    return out


def sections():
    secs = [("kit", kit_structs())]
    try:
        import cave_dark_props
        secs.append(("cave", cave_dark_props.build()))
    except ImportError:
        pass
    try:
        import cave_dark_places
        secs.append(("places", cave_dark_places.build()))
    except ImportError:
        pass
    return secs


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"cave_dark_build: failed: {' '.join(map(str, cmd))}")
    return r


def hints_yaml():
    """Palette hints (one palette per group) and tile sharing: the crypt's and the
    grottos' recolored rock reuses the cave's tiles under its own palette."""
    lines = ["  tiles:", "    sharing:", "      packing: biased", "      alignment: greedy",
             "  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in lib.GROUPS.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = lib.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


def scratch_project():
    """A minimal Porytiles project: an empty primary and CaveDark paired with it."""
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
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_CaveDarkStub"])
    stub = SCRATCH / "data/tilesets/primary/cave_dark_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_CaveDarkStub"])
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    cfg.mkdir(parents=True)
    pairing = "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_CaveDarkStub]\n"
    (cfg / "config.yaml").write_text(pairing)
    sec = SCRATCH / "data/tilesets/secondary/cave_dark"
    if (CFG / "tileset-manifest.json").exists() and BIN.exists():
        for f in ("tileset-manifest.json", "tileset.cache.json"):
            shutil.copy2(CFG / f, cfg / f)
        shutil.copytree(BIN, sec / "porytiles_bin")
    else:
        run([porytiles(), "create-tileset", "-C", str(SCRATCH), "--secondary", NAME])
        shutil.rmtree(sec / "porytiles_src")
    shutil.copytree(SRC, sec / "porytiles_src")
    (cfg / "config.yaml").write_text(pairing + hints_yaml())
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
        "# Per-tileset Porytiles config for gTileset_CaveDark, the dark places' secondary.\n"
        "# Written by tools/ichor/art/cave_dark_build.py, which compiles CaveDark against\n"
        "# an empty stand-in primary and checks its metatiles use only its own tiles and\n"
        "# palettes 6-12. Pair it with aethos when compiling it directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + hints_yaml())


def verify(rows):
    raw = np.fromfile(BIN / "metatiles.bin", "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = [(0x200 + i, hex(int(e))) for i, entries in enumerate(raw) for e in entries
           if not (int(e) & 0x3FF == 0 and int(e) >> 12 == 0)
           and (int(e) & 0x3FF < 512 or not (6 <= int(e) >> 12 <= 12))]
    if bad:
        sys.exit(f"cave_dark_build: entries outside CaveDark's tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    if used > TILE_LIMIT or late:
        sys.exit(f"cave_dark_build: {used} tiles used and tiles {late[:8]} referenced; a secondary "
                 f"may use at most {TILE_LIMIT} (504-511 belong to door animations)")
    print(f"verified {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used")
    return used


def estimate_tiles(structs):
    """Distinct 8x8 tiles, counting flips as one: what Porytiles will store."""
    seen = set()
    for s in structs:
        for L in s.layers.values():
            for ty in range(s.h * 2):
                for tx in range(s.w * 2):
                    t = L.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                    if not t[..., 3].any():
                        continue
                    forms = [t, t[:, ::-1], t[::-1], t[::-1, ::-1]]
                    keys = [f.tobytes() for f in forms]
                    if not any(k in seen for k in keys):
                        seen.add(keys[0])
    return len(seen)


FRAMES = 3


def anim_sources():
    """The flames, animated: the lit brazier's and the Hekataion's torches.
    Each animation's key is a strip of the 8x8 tiles that change between
    frames (frame 0 is the key, as drawn in the layers); Porytiles copies the
    frames over those tiles in VRAM, so frames cost ROM but no tile slots."""
    import cave_dark_props as P
    specs = [("brazier_flame", [P.brazier(True, frame=k)[0:16] for k in range(FRAMES)]),
             ("torch_flame", [P.hekataion("lit", "lit", "lit", frame=k)[0:16] for k in range(FRAMES)])]
    root = SRC / "anim"
    if root.exists():
        shutil.rmtree(root)
    manifest = {}
    for i, (name, frames) in enumerate(specs):
        names = [f"{k:02d}" for k in range(FRAMES)]
        manifest[name] = {"frames": names, "frame_order": names + [names[1]], "frame_offset": i}
    for name, frames in specs:
        tiles = []
        H, W = frames[0].shape[:2]
        for ty in range(H // 8):
            for tx in range(W // 8):
                sl = [f[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] for f in frames]
                if any((s != sl[0]).any() for s in sl[1:]):
                    tiles.append(sl)
        d = root / name
        d.mkdir(parents=True)
        for k in range(FRAMES):
            strip = np.concatenate([t[k] for t in tiles], axis=1)
            Image.fromarray(strip, "RGBA").save(d / f"{k:02d}.png")
            if k == 0:
                Image.fromarray(strip, "RGBA").save(d / "key.png")
        print(f"anim {name}: {len(tiles)} tiles x {FRAMES} frames")
    (root / "anim.json").write_text(json.dumps(manifest, indent=2) + "\n")


GEN = "porytiles_generated/tilesets/cave_dark/generated_anim_code.h"
INIT = "InitTilesetAnim_PorytilesManaged_CaveDark"


def wire_anims():
    """Bring Porytiles' animation wiring from the scratch project into the
    real tree, the way aethos's is: the generated header, one include in
    src/tileset_anims.c, one declaration in include/tileset_anims.h, and the
    tileset's callback in src/data/tilesets/headers.h. Idempotent."""
    src = SCRATCH / "include" / GEN
    if not src.exists():
        sys.exit("cave_dark_build: Porytiles wrote no animation code")
    dst = ROOT / "include" / GEN
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    c = ROOT / "src/tileset_anims.c"
    text = c.read_text()
    line = f'#include "{GEN}"'
    if line not in text:
        c.write_text(text.rstrip("\n") + "\n\n// [Porytiles] Auto-generated include. Do not remove.\n" + line + "\n")
    hdr = ROOT / "include/tileset_anims.h"
    text = hdr.read_text()
    decl = f"void {INIT}(void);"
    if decl not in text:
        anchor = "void InitTilesetAnim_PorytilesManaged_Aethos(void);\n"
        assert anchor in text
        text = text.replace(anchor, anchor + "// [Porytiles] Auto-generated declaration. Do not remove.\n" + decl + "\n")
        hdr.write_text(text)
    hs = ROOT / "src/data/tilesets/headers.h"
    text = hs.read_text()
    a = text.index("const struct Tileset gTileset_CaveDark =")
    b = text.index("};", a)
    block = text[a:b].replace(".callback = NULL,", f".callback = {INIT},")
    hs.write_text(text[:a] + block + text[b:])


def read_pal(path):
    vals = [int(v) for v in path.read_text().split()[3:3 + 48]]
    return [tuple(vals[i * 3:i * 3 + 3]) for i in range(16)]


def write_pal(path, colors):
    path.write_bytes(("JASC-PAL\r\n0100\r\n16\r\n" + "".join(f"{r} {g} {b}\r\n" for r, g, b in colors)).encode())


def glow_palettes():
    """The glow copy (SYSTEMS.md §2, dousing): palettes 0-15 with every color
    black except Hecate's chalk, which glows. The engine loads it over the
    map's palettes when the torch is doused, and restores them on relighting."""
    GLOW.mkdir(parents=True, exist_ok=True)
    found = []
    for i in range(16):
        out = [(0, 0, 0)] * 16
        if 6 <= i <= 12:
            pal = read_pal(BIN / "palettes" / f"{i:02d}.pal")
            for j, c in enumerate(pal):
                for name, g in lib.GLOW.items():
                    if c == lib.C[name]:
                        out[j] = g
                        found.append((i, j, name))
        write_pal(GLOW / f"{i:02d}.pal", out)
    groups = {i: n for i in range(6, 13) for n in lib.GROUPS
              if set(read_pal(BIN / "palettes" / f"{i:02d}.pal")[1:]) >= {lib.C[c] for c in lib.GROUPS[n]}}
    return found, groups


def catalog(secs, used):
    data = {"tileset": NAME, "primary": "gTileset_Aethos", "tiles_used": used, "pieces": [], "kit": {},
            "styles": {}}
    for name, structs in secs:
        for s in structs:
            if name == "kit":
                data["kit"][s.key] = s.ids[0][0]
                continue
            if ":" in s.key:
                style, key = s.key.split(":", 1)
                data["styles"].setdefault(style, {})[key] = s.ids[0][0]
                continue
            data["pieces"].append({
                "key": s.key, "title": s.title, "section": name, "w": s.w, "h": s.h,
                "ids": s.ids, "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
            })
    CATALOG.write_text(json.dumps(data, indent=1) + "\n")


LABELS = ROOT / "include/constants/metatile_labels.h"
LABEL_START = "// gTileset_CaveDark (Ichor: the dark places), written by tools/ichor/art/cave_dark_build.py"
LABEL_END = "// end gTileset_CaveDark"
# The pieces scripts swap: (piece key, label stem). Each cell gets its own label.
SWAPS = [
    ("brazier_cold", "Brazier_Cold"), ("brazier_lit", "Brazier_Lit"),
    ("hekataion_torch_w_lit", "Hekataion_TorchW_Lit"), ("hekataion_torch_s_lit", "Hekataion_TorchS_Lit"),
    ("hekataion_torch_e_lit", "Hekataion_TorchE_Lit"), ("hekataion_torch_s_gone", "Hekataion_TorchS_Gone"),
    ("hekataion_no_cake", "Hekataion_NoCake"),
    ("web_1", "Web1"), ("torn_1", "Web1_Torn"), ("web_2", "Web2"), ("torn_2", "Web2_Torn"),
    ("web_3", "Web3"), ("torn_3", "Web3_Torn"),
    ("niche_supper", "Niche_Supper"), ("niche_empty", "Niche_Empty"),
]


def write_labels(secs):
    """The metatiles scripts swap in, as METATILE_CaveDark_* in metatile_labels.h,
    rewritten in place on every build so the ids never go stale."""
    by_key = {s.key: s for _, ss in secs for s in ss}
    lines = [LABEL_START]
    for key, stem in SWAPS:
        s = by_key.get(key)
        if not s:
            continue
        for y in range(s.h):
            for x in range(s.w):
                suffix = "" if s.w * s.h == 1 else f"_{x}{y}" if s.w > 1 else f"_{y}"
                lines.append(f"#define METATILE_CaveDark_{stem + suffix:<32} 0x{s.ids[y][x]:03X}")
    hk = by_key.get("hekataion")
    if hk:
        for i, d in enumerate("WSE"):
            lines.append(f"#define METATILE_CaveDark_{'Hekataion_Torch' + d + '_Cold':<32} 0x{hk.ids[0][i]:03X}")
        lines.append(f"#define METATILE_CaveDark_{'Hekataion_Cake':<32} 0x{hk.ids[3][1]:03X}")
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


def sheet(scale=2):
    """The numbered sheet, rendered from the compiled tileset on aethos."""
    sys.path.insert(0, str(ROOT / "tools/ichor"))
    import render_map as rm
    rm.read_fieldmap_constants()
    syms = rm.scan_tileset_symbols()
    r = rm.Renderer(rm.Tileset(rm.resolve_tileset("gTileset_Aethos", syms)),
                    rm.Tileset(rm.tileset_from_dir(TS)))
    count = len(r.s.metatiles)
    img = rm.render_sheet(r, 0x200, count, scale)
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    img.save(SHEET)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()
    secs = sections()
    allst = [s for _, ss in secs for s in ss]
    probs = validate(allst)
    for p in probs[:40]:
        print("PROBLEM:", p)
    print(f"{len(allst)} structures, about {estimate_tiles(allst)} distinct tiles")
    if args.preview:
        preview([s for s in allst if s.section != "kit"]).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack([(SECTION_ROWS[n], ss) for n, ss in secs])
    write_sources(allst, rows, SRC)
    anim_sources()
    write_labels(secs)
    if not args.no_compile:
        compile_tileset()
        used = verify(rows)
        wire_anims()
        found, groups = glow_palettes()
        print("palette slots:", ", ".join(f"{i}={n}" for i, n in sorted(groups.items())))
        print("glow indices:", found)
        catalog(secs, used)
        sheet()


if __name__ == "__main__":
    main()
