#!/usr/bin/env python3
"""Draw, compile, register and catalog Act III's Knossa secondaries.

LABYRINTH.md §11 planned one `knossa` secondary for Amnisos, the Bull Road and
the palace. Its pieces come to well over one secondary's 504 tiles, so it is
split by map, as the Kythera family is:

  amnisos        Amnisos: the quay and the mole, the Titan triremes, the
                 Minoan houses with a hive on every roof, the harbor shrine,
                 the town wall, the cliff and the Cave of Eileithyia's mouth
  bull_road      the Bull Road and its vineyard, the Bronze Heel, the beekeeper's
                 hut, the labrys door and Ida's gate
  palace_minos   the Palace of Minos above ground: court, bull-leaping lane,
                 North Entrance, Theatral Area, light wells, Grand Staircase head
  palace_rooms   the palace's four rooms (Throne Room, West Magazines, Queen's
                 Megaron, Grand Staircase) and the Bull Road vault
  ida            the Ida path, the cradle shrine, the Idaean Cave and the
                 Cave of Eileithyia

All but palace_rooms pair with the aethos primary and borrow its ground;
palace_rooms uses only its own tiles and palettes 6-12, so it works on any
primary. The pipeline is kythera_build.py's (pack, sources, Porytiles in a
scratch project, borrowed ground, verify); this file adds Knossa's specs, its
registration, its catalogs and tools/ichor/maps/knossa_tiles.py.

Usage: /usr/bin/python3 tools/ichor/art/knossa_build.py [amnisos|bull_road|palace_minos|
           palace_rooms|ida|all] [--no-compile]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knossa_lib as N  # noqa: E402
import kythera_build as KB  # noqa: E402
import kythera_lib as K  # noqa: E402

ROOT = N.ROOT
IMG = ROOT / "design/phase4/img"
TILES_PY = ROOT / "tools/ichor/maps/knossa_tiles.py"
NAMES = ["amnisos", "bull_road", "palace_minos", "palace_rooms", "ida"]

KB.ANIM_ORDER.update({
    "bees": ["0", "1", "2", "1", "0", "2"],
})


def spec(name):
    import knossa_specs
    return knossa_specs.spec(name)


# --------------------------------------------------------------------------
# Registration (kythera_build's, with Knossa's comments)
# --------------------------------------------------------------------------

def register(sp, animated):
    d, name, sfx = sp["dir"], sp["symbol"], KB.suffix(sp)
    gfx = ROOT / "src/data/tilesets/graphics.h"
    t = gfx.read_text()
    if f"gTilesetTiles_PorytilesManaged_{sfx}[]" not in t:
        pals = ",\n".join(f'    INCBIN_U16("data/tilesets/secondary/{d}/porytiles_bin/palettes/{p:02d}.gbapal")'
                          for p in range(16))
        t = t.rstrip("\n") + (
            f"\n\n// Ichor: {d} ({sp['title']}), written by tools/ichor/art/knossa_build.py\n"
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
    if sp.get("primary", "aethos") == "aethos":
        why = ("// tools/ichor/art/knossa_build.py for the aethos primary: its ground cells\n"
               "// borrow aethos's grass, path, sand, sea and shallows, so rebuild it whenever\n"
               "// aethos changes.\n")
    else:
        why = ("// tools/ichor/art/knossa_build.py; it uses only its own tiles and palettes\n"
               "// 6-12, so it works on any primary.\n")
    block = (f"// Ichor: {d}, {sp['title']} (Act III, Knossa). Porytiles-managed, built by\n" + why +
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


def fix_config(sp):
    cfg = ROOT / "porytiles/tilesets" / sp["symbol"] / "config.yaml"
    t = cfg.read_text()
    t = t.replace("tools/ichor/art/kythera_build.py", "tools/ichor/art/knossa_build.py")
    if sp.get("primary", "aethos") != "aethos":
        t = t.replace("then points its ground cells at aethos's grass, path, sand,\n"
                      "# sea, shallows and waterfall. Pair it with aethos when compiling it directly.",
                      "it draws all its own ground.")
    cfg.write_text(t)


LABELS = ROOT / "include/constants/metatile_labels.h"


def write_labels(sp, structs):
    want = sp.get("labels", [])
    if not want:
        return
    start = f"// {sp['symbol']} (Ichor: {sp['title']}), written by tools/ichor/art/knossa_build.py"
    end = f"// end {sp['symbol']}"
    lines = [start]
    by = {s.key: s for s in structs}
    for key, items in want:
        s = by[key]
        for nm, label in items:
            cx, cy = s.names[nm]
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
# Catalog JSON, the Python catalog, images
# --------------------------------------------------------------------------

def catalog(sp, structs):
    data = []
    for sec_name, ss in sp["sections"]:
        for s in ss:
            data.append({
                "key": s.key, "title": s.title, "section": sec_name, "w": s.w, "h": s.h,
                "ids": s.ids, "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items()},
                "ground": {f"{x},{y}": g for (x, y), g in s.ground.items()},
                "anims": sorted(set(K.anim_tiles(s).values())),
            })
    by = {d["key"]: d for d in data}
    fronts = {}
    for k, f in sp.get("fronts", {}).items():
        kit = by[f["kit"]]
        ids = []
        for row in f["rows"]:
            r = []
            for ref in row:
                if ref is None:
                    r.append(None)
                    continue
                cx, cy = kit["names"][ref]
                r.append(kit["ids"][cy][cx])
            ids.append(r)
        fronts[k] = {**f, "ids": ids}
    out = ROOT / f"build/{sp['dir']}"
    out.mkdir(parents=True, exist_ok=True)
    cat = {"tileset": sp["symbol"], "structures": data, "fronts": fronts}
    (out / "catalog.json").write_text(json.dumps(cat, indent=1))
    return cat


def write_tiles_py(name, cat):
    cur = {}
    if TILES_PY.exists():
        ns = {}
        exec(compile(TILES_PY.read_text(), str(TILES_PY), "exec"), ns)
        cur = ns.get("TILESETS", {})
    slim = {"symbol": cat["tileset"], "structures": {}, "fronts": {}}
    for d in cat["structures"]:
        slim["structures"][d["key"]] = {
            "w": d["w"], "h": d["h"], "ids": d["ids"], "walk": d["walk"],
            "names": {k: tuple(v) for k, v in d["names"].items()},
            "ground": d["ground"], "section": d["section"],
        }
    for k, f in cat["fronts"].items():
        slim["fronts"][k] = {"rows": f["rows"], "ids": f["ids"]}
    cur[name] = slim
    body = json.dumps(cur, indent=1, sort_keys=True)
    body = body.replace("true", "True").replace("false", "False").replace("null", "None")
    TILES_PY.parent.mkdir(parents=True, exist_ok=True)
    TILES_PY.write_text(
        '"""Metatile ids of Act III\'s Knossa secondaries, for map builders.\n\n'
        "Generated by tools/ichor/art/knossa_build.py; do not edit. One entry per\n"
        "tileset (amnisos, bull_road, palace_minos, palace_rooms, ida), each\n"
        "{'symbol', 'structures':\n"
        "{key: {'w', 'h', 'ids' (rows of metatile ids), 'walk' (rows of walk codes),\n"
        "'names' {piece: (x, y)}, 'ground' {'x,y': aethos ground}, 'section'}},\n"
        "'fronts': {key: {'rows', 'ids'}}}. The catalogs, with what every piece is\n"
        "for, are design/phase4/TILES_<tileset>.md.\n\n"
        "    from knossa_tiles import mid, walk, place\n"
        "    door = mid('amnisos', 'house', 'door')\n"
        "    place(grid, 'palace_minos', 'column', x, y)   # a whole structure\n"
        '"""\n\n'
        f"TILESETS = {body}\n\n\n"
        "def mid(tileset, key, name=None, x=0, y=0):\n"
        '    """The metatile id of a named piece (or of cell (x, y) of a structure)."""\n'
        "    s = TILESETS[tileset]['structures'][key]\n"
        "    if name is not None:\n"
        "        x, y = s['names'][name]\n"
        "    return s['ids'][y][x]\n\n\n"
        "def walk(tileset, key, name=None, x=0, y=0):\n"
        '    """The walk code of a named piece: X . T G J D W P S (see the catalogs)."""\n'
        "    s = TILESETS[tileset]['structures'][key]\n"
        "    if name is not None:\n"
        "        x, y = s['names'][name]\n"
        "    return s['walk'][y][x]\n\n\n"
        "def front(tileset, key):\n"
        '    """A house front: rows of metatile ids (None where it leaves the ground)."""\n'
        "    return TILESETS[tileset]['fronts'][key]['ids']\n\n\n"
        "def place(grid, tileset, key, x, y):\n"
        '    """Write a whole structure into grid[y][x] (a list of rows of ids)."""\n'
        "    s = TILESETS[tileset]['structures'][key]\n"
        "    for j, row in enumerate(s['ids']):\n"
        "        for i, m in enumerate(row):\n"
        "            grid[y + j][x + i] = m\n")


def images(sp, structs):
    IMG.mkdir(parents=True, exist_ok=True)
    d = sp["dir"]
    K.shelf_preview(structs, scale=2, width=1400).save(IMG / f"{d}_pieces.png")
    KB.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", sp["symbol"],
            "--primary", sp.get("primary", "aethos"), "--scale", "2", "-o",
            str(IMG / f"{d}_sheet.png")])
    print(f"design/phase4/img/{d}_pieces.png, design/phase4/img/{d}_sheet.png")


# --------------------------------------------------------------------------

def build_one(name, compile_=True):
    sp = spec(name)
    groups = sp["groups"]
    group_rgb = N.group_rgb(groups)
    structs = [s for _, ss in sp["sections"] for s in ss]
    keys = [s.key for s in structs]
    assert len(keys) == len(set(keys)), f"duplicate structure keys in {name}"
    probs = K.validate(structs, group_rgb)
    if not probs:
        before = len(K.tiles_of(structs))
        merges = K.merge_near_duplicates(structs, KB.NEAR_DUPLICATE_PX, group_rgb)
        print(f"{name}: merged {len(merges)} near-duplicate tiles: {before} -> "
              f"{len(K.tiles_of(structs))} tiles")
        probs = K.validate(structs, group_rgb)
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    KB.fix_keys(structs)
    KB.check_anim_keys(structs)
    rows, used = KB.pack(sp)
    KB.write_sources(sp, structs, rows, used)
    cat = catalog(sp, structs)
    write_tiles_py(name, cat)
    write_labels(sp, structs)
    if not compile_:
        return
    animated = KB.compile_tileset(sp, groups)
    fix_config(sp)
    patched = KB.borrow_ground(sp, structs)
    register(sp, animated)
    n_tiles, n_meta = KB.verify(sp, rows, patched)
    images(sp, structs)
    import knossa_catalog
    knossa_catalog.main(name, sp, n_tiles, n_meta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tileset", nargs="?", default="amnisos")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    names = NAMES if args.tileset == "all" else [args.tileset]
    for n in names:
        build_one(n, not args.no_compile)


if __name__ == "__main__":
    main()
