#!/usr/bin/env python3
"""Draw, compile and catalog the Arkadian climb's secondary tilesets.

  gTileset_ArkadiaHeights  Route 11 (the Krathis gorge), Styx Falls, Route 12
                           (the cypress road over Kyllene)
  gTileset_MaiaCave        the Cave of Maia on Route 12

Steps (as kithairon_build.py):
1. Paint every structure, check each 8x8 tile draws from one palette group
   (heights_lib.GROUPS, CAVE_GROUPS), and merge tiles within 2 px of each other.
2. Pack each set's sections into the 8-wide sheet, first fit, in order.
3. Write data/tilesets/secondary/<dir>/porytiles_src, compile with Porytiles in
   a scratch project against an empty stand-in primary, and point every
   borrowed-ground cell's bottom at aethos's grass, road, sea, tall grass,
   deep shade or waterfall.
4. Verify every entry, fail past 504 tiles (door animations own 504-511), and
   write build/heights/<dir>/catalog.json, the metatile labels scripts swap,
   the sheets and design/phase3/TILES_heights.md.

Usage: /usr/bin/python3 tools/ichor/art/heights_build.py [--no-compile] [--only heights,maia]
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
import heights_cave  # noqa: E402
import heights_ground  # noqa: E402
import heights_lib as H  # noqa: E402
import heights_props  # noqa: E402
import heights_trees  # noqa: E402

ROOT = H.ROOT
OUT = ROOT / "build/heights"
IMG = ROOT / "design/phase3/img"
AETHOS_META = ROOT / "data/tilesets/primary/aethos/porytiles_bin/metatiles.bin"
COLS = 8
TILE_LIMIT = 504
NEAR_DUPLICATE_PX = 2

SETS = {
    "heights": {"symbol": "gTileset_ArkadiaHeights", "dir": "arkadia_heights",
                "label": "ArkadiaHeights", "title": "Route 11, the Krathis gorge"},
    "styx": {"symbol": "gTileset_StyxFalls", "dir": "styx_falls", "label": "StyxFalls",
             "title": "Styx Falls and Nonakris"},
    "kyllene": {"symbol": "gTileset_Kyllene", "dir": "kyllene", "label": "Kyllene",
                "title": "Route 12, the cypress road over Kyllene"},
    "maia": {"symbol": "gTileset_MaiaCave", "dir": "maia_cave", "label": "MaiaCave",
             "title": "the Cave of Maia"},
}

# Metatiles scripts swap: (set, structure, cell name, label)
LABELS = [
    ("heights", "ruins", "drum_wedged", "DrumWedged"),
    ("heights", "ruins", "drum_rest", "DrumRest"),
    ("heights", "ruins", "gap", "Gap"),
    ("kyllene", "hawk", "drum_wedged", "DrumWedged"),
    ("kyllene", "shrine", "top", "Shrine_Top"),
    ("kyllene", "shrine", "top_R", "Shrine_TopR"),
    ("kyllene", "shrine", "bad_top", "ShrineBad_Top"),
    ("kyllene", "shrine", "bad_top_R", "ShrineBad_TopR"),
]

# The core: painted once, packed first at the same ids in all three outdoor
# sets, so the seams between Route 11, Styx Falls and Route 12 can use it.
CORE = ["path", "rock", "face", "fir", "fir_stack", "fir_young", "oak", "cypress", "cypress_stack",
        "fir_shade", "fir_stack_shade", "fir_young_shade", "oak_shade", "cypress_shade",
        "cypress_stack_shade", "terraces", "marks", "rock_detail"]
EXTRAS = {
    "heights": [("gorge", ["tall", "water", "rapids", "ruins", "kiln", "chasm", "falls", "spring"])],
    "styx": [("styx", ["bface", "blackpool", "blackpool_deep", "thread", "houses", "stones"])],
    "kyllene": [("kyllene", ["meadow_tall", "tall", "decor", "tortoises", "shrine", "kiln", "split",
                             "hawk"])],
}
CAVE = [("cave", ["cwall", "cface", "cfloor", "maia"])]
SECTION_TITLES = {
    "core": "Core: shared by all three outdoor sets at the same ids",
    "gorge": "The Krathis gorge: white water, the fallen temple, the kiln, the ravine, the side "
             "waterfall, the spring",
    "styx": "Styx Falls: the black cliff, the black pool, the thread, Nonakris",
    "kyllene": "Kyllene: the combed meadow, tortoise boulders, the shrine of Artemis, the hawk's "
               "cliff",
    "cave": "The Cave of Maia",
}
SHAPE_KEYS = ("tall", "meadow_tall", "path", "rock", "face", "bface", "water", "blackpool",
              "cwall", "cface")


def sections_for(name, ss):
    if name == "maia":
        return [(sec, [ss[k] for k in keys]) for sec, keys in CAVE]
    return [("core", [ss[k] for k in CORE])] + [(sec, [ss[k] for k in keys])
                                                for sec, keys in EXTRAS[name]]


def painted():
    ss = {}
    for mod in (heights_ground, heights_trees, heights_props, heights_cave):
        for s in mod.build():
            assert s.key not in ss, s.key
            ss[s.key] = s
    hs = ss.pop("houses")
    ss["houses"] = H.crop(hs, "houses", hs.title, list(hs.names), notes=hs.notes)
    mk = ss.pop("markers")
    ss["marks"] = H.crop(mk, "marks", "Herms, turned earth, scree, a boulder",
                         ["herm_top", "herm", "dig", "scree", "scree_b", "boulder"],
                         notes="On borrowed grass. `herm_top` over `herm`: a great herm, Hermes's "
                               "bearded head on a square pillar, hung with a garland. `dig` turned "
                               "earth (walkable). `scree`/`scree_b` loose stones (walkable). "
                               "`boulder` a grey rock.")
    ss["spring"] = H.crop(mk, "spring", "Pelasgos's spring, snowmelt runnels",
                          ["spring_W", "spring_E", "runnel", "runnel_g"],
                          notes="`spring_W` + `_E`: Pelasgos's spring, a stone trough fed by a "
                                "spout, on aethos's animated water (blocks). `runnel` snowmelt across "
                                "the road, `runnel_g` across grass (walkable).")
    ss["tortoises"] = H.crop(mk, "tortoises", "Kyllene's tortoise boulders, the hawk's nest",
                             ["tort", "tort_b", "tort_big_L", "tort_big_R", "nest"],
                             notes="On borrowed grass: `tort`, `tort_b`, `tort_big_L` + `_R`, gray "
                                   "boulders shaped like tortoise shells (some of them are "
                                   "Chelonet). `nest` the hawk's stick nest on its pinnacle (rock "
                                   "all round).")
    ru = ss.pop("ruins")
    keep = [n for n in ru.names if n not in ("hoofcups",)]
    ss["ruins"] = H.crop(ru, "ruins", ru.title, keep, notes=ru.notes)
    ss["hawk"] = H.crop(ru, "hawk", "The hawk spur's drum and its gap", ["gap", "drum_wedged"],
                        notes="`gap` the break in the hawk spur's goat path (walkable only at "
                              "elevation 1: the drum's button), `drum_wedged` the boundary drum "
                              "dropped into it, a step (walkable).")
    ss["stones"] = H.crop(ru, "stones", "The Oath Stone and the hoof-cups", ["hoofcups"],
                          notes="`oath` the Oath Stone, a flat-topped boulder worn smooth by "
                                "hands; `hoofcups` a row of hoof-cups on a flat stone, each tied "
                                "with a linen scrap. On borrowed grass; both block.")
    oath = H.crop(mk, "x", "", ["oath"])
    st = ss["stones"]
    for ln in ("bottom", "middle", "top"):
        a = st.layers[ln].a.copy()
        st.layers[ln] = H.Layer(32, 16)
        st.layers[ln].a[:, 0:16] = oath.layers[ln].a
        st.layers[ln].a[:, 16:32] = a
    st.w, st.walk = 2, ["XX"]
    st.names = {"oath": (0, 0), "hoofcups": (1, 0)}
    st.ground = {(0, 0): "grass", (1, 0): "grass"}
    ch = ss.pop("chasm")
    ss["chasm"] = H.crop(ch, "chasm", ch.title, ["void", "plank", "plank_gap", "mouth_L", "mouth_R",
                                                 "in_L", "in_R"], notes=ch.notes)
    ss["split"] = H.crop(ch, "split", "A split in the cliff path", ["split"],
                         notes="A split across the goat path above the Cave of Maia, too wide to "
                               "step (MB_ICHOR_GAP: the Winged Talaria leap it).")
    fa = ss.pop("falls")
    ss["falls"] = H.crop(fa, "falls", "The side waterfall",
                         ["fall_top", "fall", "fall_ledge", "fall_foot"],
                         notes="Cliff faces with a slit where aethos's animated waterfall shows "
                               "through: `fall_top`, `fall`, `fall_ledge` (a ledge halfway up, "
                               "something glinting on it), `fall_foot`. MB_WATERFALL (the Horn "
                               "of Achelous, Act III).")
    ss["thread"] = H.crop(fa, "thread", "The Styx",
                          ["thread_top", "thread", "thread_b", "thread_foot"],
                          notes="The Styx: one long thread of white water down the black cliff, "
                                "aethos's animated waterfall seen through a slit. `thread_top` in "
                                "mist, `thread`, `thread_b`, `thread_foot` meeting the black pool.")
    return ss


# --------------------------------------------------------------------------
# Packing and sources
# --------------------------------------------------------------------------

def pack(secs):
    used = np.zeros((64, COLS), bool)
    ids = {}
    rows = 0
    for name, structs in secs:
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


def write_sources(src, secs, ids, rows):
    if src.exists():
        shutil.rmtree(src)
    src.mkdir(parents=True)
    sheets = {ln: np.zeros((rows * 16, COLS * 16, 4), np.uint8) for ln in ("bottom", "middle", "top")}
    beh = {}
    for _, structs in secs:
        for s in structs:
            g = ids[s.key]
            for cy in range(s.h):
                for cx in range(s.w):
                    i = g[cy][cx] - 0x200
                    r, c = divmod(i, COLS)
                    for ln in sheets:
                        sheets[ln][r * 16:r * 16 + 16, c * 16:c * 16 + 16] = \
                            s.layers[ln].a[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
            for (x, y), mb in s.behaviors.items():
                if mb:
                    beh[g[y][x] - 0x200] = mb
    for ln, a in sheets.items():
        Image.fromarray(a, "RGBA").save(src / f"{ln}.png")
    (src / "attributes.csv").write_text(
        "\n".join(["id,behavior"] + [f"{k},{beh[k]}" for k in sorted(beh)]) + "\n")


# --------------------------------------------------------------------------
# Porytiles
# --------------------------------------------------------------------------

def porytiles():
    return shutil.which("porytiles") or str(Path.home() / ".local/bin/porytiles")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(f"heights_build: failed: {' '.join(map(str, cmd))}")
    return r


def palette_hints(groups):
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in groups.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = H.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


def compile_set(info, groups):
    name, d = info["symbol"], info["dir"]
    scratch = ROOT / f"build/{d}_porytiles"
    src = ROOT / f"data/tilesets/secondary/{d}/porytiles_src"
    binp = ROOT / f"data/tilesets/secondary/{d}/porytiles_bin"
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
    stub_name = "gTileset_HeightsStub"
    run([pt, "create-tileset", "-C", str(scratch), stub_name])
    stub = scratch / "data/tilesets/primary/heights_stub/porytiles_src"
    shutil.rmtree(stub / "anim", ignore_errors=True)
    (stub / "attributes.csv").write_text("id,behavior\n")
    for n in ("bottom", "middle", "top"):
        Image.new("RGBA", (128, 16), (255, 0, 255, 255)).save(stub / f"{n}.png")
    run([pt, "compile-tileset", "-C", str(scratch), stub_name])
    scfg = scratch / "porytiles/tilesets" / name
    scfg.mkdir(parents=True)
    pairing = f"tileset:\n  primary_pairing:\n    mode: manual\n    partners: [{stub_name}]\n"
    (scfg / "config.yaml").write_text(pairing)
    sec = scratch / f"data/tilesets/secondary/{d}"
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
    shutil.copytree(src, sec / "porytiles_src")
    (scfg / "config.yaml").write_text(pairing + palette_hints(groups))
    r = run([pt, "compile-tileset", "-C", str(scratch), "--no-verify-checksums", name])
    if r.stdout.strip() or r.stderr.strip():
        print((r.stdout + r.stderr)[-1500:])
    if binp.exists():
        shutil.rmtree(binp)
    shutil.copytree(sec / "porytiles_bin", binp)
    cfg.mkdir(parents=True, exist_ok=True)
    for f in ("tileset-manifest.json", "tileset.cache.json"):
        if (scfg / f).exists():
            shutil.copy2(scfg / f, cfg / f)
    (cfg / "config.yaml").write_text(
        f"# Per-tileset Porytiles config for {name} ({info['title']}).\n"
        "# Written by tools/ichor/art/heights_build.py, which compiles it against an empty\n"
        "# stand-in primary, then points its ground cells at aethos's grass, road, sea, tall\n"
        "# grass, deep shade and waterfall. Pair it with aethos when compiling it directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + palette_hints(groups))
    return binp


NORMAL, COVERED, SPLIT = 0, 1, 2


def borrow_ground(binp, secs, ids):
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    meta = np.fromfile(binp / "metatiles.bin", "<u2").reshape(-1, 8)
    attrs = np.fromfile(binp / "metatile_attributes.bin", "<u2")
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
                meta[i, 0:4] = aethos[H.GROUND_METATILE[kind], 0:4]
                meta[i, 4:8] = art
                attrs[i] = (int(attrs[i]) & 0x0FFF) | ((SPLIT if on_top else COVERED) << 12)
                patched[i] = kind
    meta.astype("<u2").tofile(binp / "metatiles.bin")
    attrs.astype("<u2").tofile(binp / "metatile_attributes.bin")
    return patched


def verify(binp, rows, patched, label):
    raw = np.fromfile(binp / "metatiles.bin", "<u2").reshape(-1, 8)
    aethos = np.fromfile(AETHOS_META, "<u2").reshape(-1, 8)
    assert len(raw) >= rows * 8, (len(raw), rows)
    bad = []
    for i, entries in enumerate(raw):
        for j, e in enumerate(entries):
            e = int(e)
            if i in patched and j < 4:
                if e != int(aethos[H.GROUND_METATILE[patched[i]], j]):
                    bad.append((0x200 + i, j, "ground"))
                continue
            tile, pal = e & 0x3FF, e >> 12
            if tile == 0 and pal == 0:
                continue
            if tile < 512 or not (6 <= pal <= 12):
                bad.append((0x200 + i, hex(e)))
    if bad:
        sys.exit(f"heights_build: {label}: entries outside its tiles/palettes 6-12: {bad[:10]}")
    a = np.array(Image.open(binp / "tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    used = max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    late = sorted({(int(e) & 0x3FF) - 512 for entries in raw for e in entries
                   if (int(e) & 0x3FF) - 512 >= TILE_LIMIT})
    print(f"{label}: {len(raw)} metatiles; {used} of {TILE_LIMIT} tiles used; "
          f"{len(patched)} cells on aethos ground")
    if used > TILE_LIMIT or late:
        sys.exit(f"heights_build: {label}: {used} tiles; door animations overwrite {TILE_LIMIT}-511")
    return used


# --------------------------------------------------------------------------
# Catalog, labels, images
# --------------------------------------------------------------------------

LABEL_FILE = ROOT / "include/constants/metatile_labels.h"
LABEL_START = "// gTileset_ArkadiaHeights, gTileset_MaiaCave (Ichor: the Arkadian climb), written by tools/ichor/art/heights_build.py"
LABEL_END = "// end gTileset_ArkadiaHeights"


def write_labels(all_ids):
    lines = [LABEL_START]
    for setname, key, cell, label in LABELS:
        if setname not in all_ids:
            continue
        ids, ss = all_ids[setname]
        cx, cy = ss[key].names[cell]
        lines.append(f"#define METATILE_{SETS[setname]['label']}_{label:<20} 0x{ids[key][cy][cx]:03X}")
    lines.append(LABEL_END)
    block = "\n".join(lines) + "\n"
    text = LABEL_FILE.read_text()
    if LABEL_START in text:
        a = text.index(LABEL_START)
        b = text.index(LABEL_END, a) + len(LABEL_END) + 1
        text = text[:a] + block + text[b:]
    else:
        end = text.rindex("#endif")
        text = text[:end] + block + "\n" + text[end:]
    LABEL_FILE.write_text(text)


def catalog(setname, secs, ids):
    data = []
    for sec, structs in secs:
        for s in structs:
            data.append({
                "key": s.key, "title": s.title, "section": sec, "w": s.w, "h": s.h,
                "ids": ids[s.key], "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items() if mb},
                "ground": {f"{x},{y}": g for (x, y), g in getattr(s, "ground", {}).items()},
            })
    d = OUT / SETS[setname]["dir"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "catalog.json").write_text(json.dumps({"symbol": SETS[setname]["symbol"],
                                                "structures": data}, indent=1))
    return data


def images(setname):
    IMG.mkdir(parents=True, exist_ok=True)
    out = IMG / f"tiles_{SETS[setname]['dir']}_sheet.png"
    run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", SETS[setname]["symbol"],
         "--primary", "aethos", "--scale", "2", "-o", str(out)])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--only", help="comma-separated: heights,styx,kyllene,maia")
    args = ap.parse_args()
    ss = painted()
    outdoor = CORE + [k for ex in EXTRAS.values() for _, ks in ex for k in ks]
    cavekeys = [k for _, ks in CAVE for k in ks]

    def check():
        probs = H.validate([ss[k] for k in dict.fromkeys(outdoor)])
        probs += H.validate([ss[k] for k in cavekeys], cave=True)
        for p in probs:
            print("PROBLEM:", p)
        if probs:
            sys.exit(1)
    check()
    # merge the core once, then each set's own pieces (never touching the core,
    # so it stays identical in all three)
    core = [ss[k] for k in CORE]
    n0 = len(H.tiles_of(core))
    H.merge_near_duplicates(core, NEAR_DUPLICATE_PX)
    print(f"core: {n0} -> {len(H.tiles_of(core))} tiles")
    for name, extras in list(EXTRAS.items()) + [("maia", CAVE)]:
        mine = [ss[k] for _, keys in extras for k in keys if k not in CORE]
        n0 = len(H.tiles_of(mine))
        H.merge_near_duplicates(mine, NEAR_DUPLICATE_PX)
        print(f"{name} extras: {n0} -> {len(H.tiles_of(mine))} tiles")
    check()
    wanted = args.only.split(",") if args.only else list(SETS)
    report = {}
    all_ids = {}
    for name in wanted:
        cave = name == "maia"
        secs = sections_for(name, ss)
        ids, rows = pack(secs)
        print(f"{name}: {rows} sheet rows, {rows * 8} metatiles, "
              f"{len(H.tiles_of([s for _, st in secs for s in st]))} tiles before compiling")
        all_ids[name] = (ids, ss)
        info = SETS[name]
        write_sources(ROOT / f"data/tilesets/secondary/{info['dir']}/porytiles_src", secs, ids, rows)
        catalog(name, secs, ids)
        if not args.no_compile:
            binp = compile_set(info, H.CAVE_GROUPS if cave else H.GROUPS)
            patched = borrow_ground(binp, secs, ids)
            used = verify(binp, rows, patched, name)
            report[name] = (used, rows * 8, secs, ids)
    out = [n for n in all_ids if n != "maia"]
    for a in out:
        for b in out:
            for k in CORE:
                assert all_ids[a][0][k] == all_ids[b][0][k], f"core {k} moved between {a} and {b}"
    write_labels(all_ids)
    if not args.no_compile:
        for name in wanted:
            try:
                print(images(name).relative_to(ROOT))
            except SystemExit as e:
                print("sheet image skipped:", e)
        import heights_catalog
        heights_catalog.main(report, ss)


if __name__ == "__main__":
    main()
