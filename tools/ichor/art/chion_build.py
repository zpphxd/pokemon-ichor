#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Chion, the secondary of Olympus's snows.

1. Builds the kit (cave_dark's kit recolored into ice and snow, with slick
   ice as MB_ICE), the glacier and cloud wall styles, and the props
   (tools/ichor/art/chion_props.py). Checks each 8x8 tile draws from one
   palette group (tools/ichor/art/chion_lib.py).
2. Packs them into the 8-wide metatile sheet; each section starts on a fixed
   row, so growing one section never renumbers another.
3. Writes data/tilesets/secondary/chion/porytiles_src.
4. Compiles with Porytiles in a scratch project (build/chion_porytiles)
   against an empty stand-in primary, so Chion uses only its own tiles and
   palettes 6-12, copies porytiles_bin and the Porytiles cache back, and
   verifies every metatile entry and the 504-tile budget.
5. Writes data/tilesets/secondary/chion/catalog.json (map builders read it),
   the metatile labels scripts swap in, and the numbered sheet.

Usage: /usr/bin/python3 tools/ichor/art/chion_build.py [--no-compile] [--preview out.png]
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
import chion_lib as lib  # noqa: E402
import chion_props as props  # noqa: E402
from chion_lib import ROOT, Struct, composite, pack, preview, validate, write_sources  # noqa: E402

NAME = "gTileset_Chion"
TS = ROOT / "data/tilesets/secondary/chion"
SRC = TS / "porytiles_src"
BIN = TS / "porytiles_bin"
CATALOG = TS / "catalog.json"
CFG = ROOT / "porytiles/tilesets" / NAME
SCRATCH = ROOT / "build/chion_porytiles"
SHEET = ROOT / "design/maps/img/chion_sheet.png"
TILE_LIMIT = 504          # CLAUDE.md: tiles 504-511 of a secondary are the door animations'

# First metatile row of each section (8 metatiles a row; id = 0x200 + row*8 + col).
SECTION_ROWS = {"kit": 0, "styles": 24, "props": 40}
SECTION_TITLES = {
    "kit": "The kit: ice walls, snow floor, slick ice (MB_ICE), the tarn",
    "styles": "The glacier's snow-topped walls; the cloud sea",
    "props": "Crystals, pines, the frozen giant, the seals, shrines, ladders, the propylaia",
}


def sections():
    return [("kit", props.kit_structs()), ("styles", props.style_structs()), ("props", props.props())]


def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"chion_build: failed: {' '.join(map(str, cmd))}")
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
    """A minimal Porytiles project: an empty primary and Chion paired with it."""
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    for rel in ("include/fieldmap.h", "include/global.fieldmap.h", "include/tileset_anims.h",
                "include/constants/metatile_behaviors.h", "src/fieldmap.c", "src/tileset_anims.c",
                "src/data/tilesets/headers.h", "src/data/tilesets/graphics.h",
                "src/data/tilesets/metatiles.h", "porytiles/config.yaml"):
        dst = SCRATCH / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    # the first compile creates Chion afresh: hide the real tree's declaration of it
    if not (CFG / "tileset-manifest.json").exists():
        for rel in ("src/data/tilesets/headers.h", "src/data/tilesets/graphics.h", "src/data/tilesets/metatiles.h"):
            f = SCRATCH / rel
            text = f.read_text()
            if rel.endswith("headers.h"):
                a = text.index("const struct Tileset gTileset_Chion =")
                b = text.index("};", a) + 2
                text = text[:a] + text[b:]
            else:
                a = text.index("// Ichor: chion")
                b = text.find("\n// Ichor:", a + 5)
                text = text[:a] + (text[b:] if b > 0 else "")
            f.write_text(text)
    (SCRATCH / "data/tilesets/primary").mkdir(parents=True)
    (SCRATCH / "data/tilesets/secondary").mkdir(parents=True)
    pt = porytiles()
    run([pt, "create-tileset", "-C", str(SCRATCH), "gTileset_ChionStub"])
    stub = SCRATCH / "data/tilesets/primary/chion_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(SCRATCH), "gTileset_ChionStub"])
    cfg = SCRATCH / "porytiles/tilesets" / NAME
    cfg.mkdir(parents=True)
    pairing = "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_ChionStub]\n"
    (cfg / "config.yaml").write_text(pairing)
    sec = SCRATCH / "data/tilesets/secondary/chion"
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
        "# Per-tileset Porytiles config for gTileset_Chion, the snows of Olympus.\n"
        "# Written by tools/ichor/art/chion_build.py, which compiles Chion against\n"
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
        sys.exit(f"chion_build: entries outside Chion's tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(BIN / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    if used > TILE_LIMIT or late:
        sys.exit(f"chion_build: {used} tiles used and tiles {late[:8]} referenced; a secondary "
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


LABEL_START = "// gTileset_Chion (Ichor: the snows of Olympus), written by tools/ichor/art/chion_build.py"
LABEL_END = "// end gTileset_Chion"
# The pieces scripts swap: (piece key, label stem).
SWAPS = [("plate", "Plate"), ("plate_down", "Plate_Down"), ("grate", "Grate"), ("grate_up", "Grate_Up")]


LABELS = ROOT / "include/constants/metatile_labels.h"


def write_labels(secs):
    """The metatiles scripts swap in, as METATILE_Chion_* in metatile_labels.h,
    rewritten in place on every build so the ids never go stale."""
    by_key = {s.key: s for _, ss in secs for s in ss}
    lines = [LABEL_START]
    for key, stem in SWAPS:
        s = by_key[key]
        lines.append(f"#define METATILE_Chion_{stem:<32} 0x{s.ids[0][0]:03X}")
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
        preview([s for s in allst if s.section == "props"]).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack([(SECTION_ROWS[n], ss) for n, ss in secs])
    write_sources(allst, rows, SRC)
    write_labels(secs)
    if not args.no_compile:
        compile_tileset()
        used = verify(rows)
        catalog(secs, used)
        sheet()


if __name__ == "__main__":
    main()
