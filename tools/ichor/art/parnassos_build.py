#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Parnassos: Lebadeia and Route 9.

One secondary on the aethos primary for both maps, so the Lebadeia / Route 9
seam needs no aethos-only strip. It reuses kithairon_build's packing, Porytiles
compile and borrowed-ground steps (with Parnassos's own palette hints):

1. Paint every structure (parnassos_ground, _trees, _stone, _springs, _far,
   _houses), check each 8x8 tile draws from one palette group
   (parnassos_lib.GROUPS), and merge tiles within 2 px of each other.
2. Pack the sections into the 8-wide sheet, first fit, in order.
3. Write data/tilesets/secondary/parnassos/porytiles_src, compile with
   Porytiles in a scratch project against an empty stand-in primary, and point
   every borrowed-ground cell's bottom at aethos's grass, road, sea or tall grass.
4. Verify every entry, fail past 504 tiles (door animations own 504-511), and
   write build/parnassos/catalog.json, the metatile labels scripts swap, the
   sheet and the catalog part of design/phase3/TILES_parnassos.md.

Usage: /usr/bin/python3 tools/ichor/art/parnassos_build.py [--no-compile]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kithairon_build as KB  # noqa: E402
import parnassos_far  # noqa: E402
import parnassos_ground  # noqa: E402
import parnassos_houses  # noqa: E402
import parnassos_lib as P  # noqa: E402
import parnassos_springs  # noqa: E402
import parnassos_stone  # noqa: E402
import parnassos_trees  # noqa: E402

ROOT = P.ROOT
OUT = ROOT / "build/parnassos"
IMG = ROOT / "design/phase3/img"
DOC = ROOT / "design/phase3/TILES_parnassos.md"
KEEP = "## Render-and-critique passes"
INFO = {"symbol": "gTileset_Parnassos", "dir": "parnassos", "label": "Parnassos",
        "title": "Lebadeia and Route 9, the Split Road"}

SECTIONS = [
    ("ground", ["tall", "path", "crag", "water", "pave", "gully", "crag_detail"]),
    ("trees", ["laurel", "laurel_stack", "laurel_young", "wild_olive", "plane", "scrub", "meadow"]),
    ("stone", ["markers", "pmarkers", "ruin", "steps", "bridge", "timber"]),
    ("springs", ["face", "lethe", "mnemosyne"]),
    ("far", ["far", "ravine"]),
    ("houses", ["roof_tile", "wall", "windows", "doors"]),
]
SECTION_TITLES = {
    "ground": "Soft ground: grass, road, crags, the Herkyna, paving, gullies",
    "trees": "Laurels, wild olives, plane trees, scrub, flowers",
    "stone": "Worked stone: the herm, altars, the treasury's ruin, steps, bridges",
    "springs": "Lebadeia's precinct: the grille, the springs",
    "far": "The lookout's view: the Phaidriades and Delphoi, the ravine",
    "houses": "Lebadeia's houses (Eleusa's kit)",
}

# Metatiles scripts swap: (structure, cell name, label)
LABELS = [
    ("face", "grille", "Grille"),
    ("face", "grille_open", "GrilleOpen"),
    ("markers", "drum_gully", "DrumGully"),
    ("markers", "drum_gully_b", "DrumGully_B"),
    ("markers", "altar", "AltarApollo"),
    ("markers", "drum", "Drum"),
]


def crag_detail():
    """Kithairon's crag details (a crack, boulders, a tuft, a juniper), repainted
    on Parnassos's rock."""
    import kithairon_stone
    cd = kithairon_stone.crag_detail()
    s = P.crop(cd, "crag_detail", "Crag detail: cracks, boulders, tufts, juniper",
               ["crack", "boulders", "tuft", "juniper"],
               notes="Interior crag cells to scatter through a big crag (Kithairon's, "
                     "recolored): `crack`, `boulders`, `tuft`, `juniper`. Block.")
    return P.recolor_struct(s)


def painted():
    ss = {}
    for mod in (parnassos_ground, parnassos_trees, parnassos_stone, parnassos_springs, parnassos_far,
                parnassos_houses):
        for s in mod.build():
            assert s.key not in ss, s.key
            ss[s.key] = s
    ss["crag_detail"] = crag_detail()
    # the budget: keep only the cells the maps use (504 tiles)
    keep = {
        "markers": ["herm_top", "stone_top", "altar_top", "dig", "rubble", "feathers", "bench_L",
                    "bench_R", "herm", "boundary", "altar", "altar_bad", "cairn", "drum", "capital",
                    "boulder", "drum_gully", "drum_gully_b", "scree"],
        "far": ["top_a", "face_a", "face_b", "gorge_top", "gorge", "gorge_foot", "foot", "slope",
                "temple_L", "temple_R", "theater", "roofs", "slope_foot"],
        "crag_detail": ["crack", "juniper"],
        "ravine": ["lip"],
        "meadow": ["broom", "white"],
        "scrub": ["oak", "laurel"],
    }
    for key, names in keep.items():
        src = ss[key]
        s = P.crop(src, key, src.title, names, notes=src.notes)
        s.behaviors = {c: mb for c, mb in s.behaviors.items() if mb}
        ss[key] = s
    return ss


def palette_hints():
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in P.GROUPS.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = P.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


LABEL_FILE = ROOT / "include/constants/metatile_labels.h"
LABEL_START = "// gTileset_Parnassos (Ichor: Lebadeia and Route 9), written by tools/ichor/art/parnassos_build.py"
LABEL_END = "// end gTileset_Parnassos"


def write_labels(ids, ss):
    lines = [LABEL_START]
    for key, cell, label in LABELS:
        cx, cy = ss[key].names[cell]
        lines.append(f"#define METATILE_Parnassos_{label:<20} 0x{ids[key][cy][cx]:03X}")
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
            })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps({"symbol": INFO["symbol"], "structures": data},
                                                 indent=1))


HEAD = """# Parnassos's tileset: Lebadeia and Route 9

The road west under Parnassos: Lebadeia in its gorge, where the Herkyna comes out of
the rock beside the springs of Lethe and Mnemosyne and the oracle's bronze grille; then
the Split Road, climbing through pale limestone, bay laurel and wild olive to the
crossroads where three roads meet, the lookout under Delphoi's cliffs, and the fallen
Phokian treasury above the cutting. One secondary on the `aethos` primary:

| Tileset | Maps |
|---|---|
| `gTileset_Parnassos` | `MAP_LEBADEIA`, `MAP_ROUTE9_SCHISTE` |

Both maps share it, so their seam (Lebadeia's west edge, Route 9's east edge) needs no
aethos-only strip. Kirrha and Aigion are on the harbors agent's own `kirrha` set
(BUILD.md), so this set carries only these two maps.

**This catalog is generated** by `tools/ichor/art/parnassos_build.py` (painters:
`parnassos_ground.py`, `_trees.py`, `_stone.py`, `_springs.py`, `_far.py`, `_houses.py`;
palettes in `parnassos_lib.py`, the soft-shape engine and crag painter borrowed from
Kithairon's). The render-and-critique passes at the end are written by hand and kept
across rebuilds.

**Place pieces by key and cell name** from `build/parnassos/catalog.json`, never by raw
id (`tools/ichor/maps/parnassos.py` does). Ids below are the current build's.

**Soft ground.** `tall`, `path`, `crag`, `water`, `pave` and `gully` hold one piece per
blob shape key: `1|` then the cell's neighbors N NE E SE S SW W NW. The map builder lists
the keys its maps use in `tools/ichor/art/parnassos_shapes.json`
(`parnassos.py --shapes`), and only those are drawn.

**Walk codes** in the grids: `X` blocks, `.` walkable, `T` walkable and drawn over the
player, `G` tall grass, `D` a door (MB_NON_ANIMATED_DOOR: put the warp there).

**Borrowed ground.** Cells on *grass*, *path*, *sea* or *tall* draw no ground of their own:
the build points their bottom tiles at aethos's grass (`0x001`), road (`0x1D9`), animated
water (`0x170`) or tall grass (`0x00D`). Rebuild the set whenever aethos is repainted.

**Palettes.** Seven groups, one per secondary palette; every 8x8 tile draws from one.

| Group | Use |
|---|---|
| field | tall grass, the road, the broken bridge's timber |
| rock | crags and their details, the Herkyna's banks, gullies, the grille, the spout, the ravine |
| tree | laurels, wild olives, planes, scrub |
| stone | paving, the herm, the boundary stone, altars, the ruin, drums, steps, bridges, the bench, the chair |
| water | the springs of Lethe and Mnemosyne |
| house | Eleusa's house kit, verbatim |
| far | the Phaidriades, Delphoi's roofs, the Kastalian falls |

**Scripted swaps** (`include/constants/metatile_labels.h`): `METATILE_Parnassos_Grille` and
`_GrilleOpen` (the oracle's grille, beat 35B), `_DrumGully`, `_DrumGully_B` and `_Drum` (the
treasury's drums at rest, beat 36C), and `_AltarApollo` (the shrine once cleansed).
"""


def grid_block(ids, s):
    lines = []
    for y in range(s.h):
        row = " ".join(f"0x{ids[y][x]:03X}" for x in range(s.w))
        lines.append(f"{row}   {' '.join(s.walk[y])}")
    return "```text\n" + "\n".join(lines) + "\n```"


def write_doc(used, metas, secs, ids):
    out = [HEAD, "## Budget\n", "| Tileset | Tiles | Metatiles |", "|---|---|---|",
           f"| `{INFO['symbol']}` | {used} of {KB.TILE_LIMIT} | {metas} of 512 |", "",
           f"![sheet](img/tiles_parnassos_sheet.png)\n"]
    for sec, structs in secs:
        out.append(f"## {SECTION_TITLES[sec]}\n")
        for s in structs:
            out.append(f"### {s.title}\n")
            out.append(f"`{s.key}`, {s.w} wide by {s.h} tall. {s.notes}\n")
            if s.key in ("tall", "path", "crag", "water", "pave", "gully"):
                out.append(f"{len(s.names)} shapes, from 0x{ids[s.key][0][0]:03X}; the interior "
                           f"`1|11111111` is 0x{ids[s.key][0][0]:03X}.\n")
                continue
            out.append(grid_block(ids[s.key], s) + "\n")
            if s.names:
                named = ", ".join(f"`{n}` 0x{ids[s.key][c[1]][c[0]]:03X}" for n, c in s.names.items())
                out.append(f"Pieces: {named}.\n")
    text = "\n".join(out) + "\n"
    old = DOC.read_text() if DOC.exists() else ""
    text += old[old.index(KEEP):] if KEEP in old else KEEP + "\n\n(Written by hand.)\n"
    DOC.write_text(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    ss = painted()
    probs = P.validate(list(ss.values()))
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    allstructs = [ss[k] for _, keys in SECTIONS for k in keys]
    assert set(ss) == {s.key for s in allstructs}, set(ss) ^ {s.key for s in allstructs}
    n0 = len(P.tiles_of(allstructs))
    P.merge_near_duplicates(allstructs, KB.NEAR_DUPLICATE_PX)
    print(f"parnassos: {n0} -> {len(P.tiles_of(allstructs))} tiles before compiling")
    probs = P.validate(allstructs)
    if probs:
        sys.exit("\n".join(probs[:10]))
    secs = [(sec, [ss[k] for k in keys]) for sec, keys in SECTIONS]
    ids, rows = KB.pack(secs)
    print(f"parnassos: {rows} sheet rows, {rows * 8} metatiles")
    KB.write_sources(ROOT / "data/tilesets/secondary/parnassos/porytiles_src", secs, ids, rows)
    catalog(secs, ids)
    write_labels(ids, ss)
    if args.no_compile:
        return
    KB.palette_hints = palette_hints          # compile with Parnassos's palette plan
    binp = KB.compile_set(INFO)
    cfg = ROOT / "porytiles/tilesets" / INFO["symbol"] / "config.yaml"
    cfg.write_text(
        f"# Per-tileset Porytiles config for {INFO['symbol']} ({INFO['title']}).\n"
        "# Written by tools/ichor/art/parnassos_build.py, which compiles it against an empty\n"
        "# stand-in primary, then points its ground cells at aethos's grass, road, sea and\n"
        "# tall grass. Pair it with aethos when compiling it directly.\n"
        "tileset:\n  primary_pairing:\n    mode: manual\n    partners: [gTileset_Aethos]\n"
        + palette_hints())
    patched = KB.borrow_ground(binp, secs, ids)
    used = KB.verify(binp, rows, patched, "parnassos")
    IMG.mkdir(parents=True, exist_ok=True)
    out = IMG / "tiles_parnassos_sheet.png"
    KB.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", INFO["symbol"],
            "--primary", "aethos", "--scale", "2", "-o", str(out)])
    write_doc(used, rows * 8, secs, ids)
    print(out.relative_to(ROOT), DOC.relative_to(ROOT))


if __name__ == "__main__":
    main()
