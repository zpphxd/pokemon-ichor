#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Thyrsa, Thyrsa City's secondary tileset.

The pipeline is emporion_build.py's, reused function for function:
1. thyrsa_art.build() draws every structure; each 8x8 tile must draw from one of
   thyrsa_lib.GROUPS. Tiles within 2 px of another are redrawn as that one.
2. Packs them into the 8-wide sheet from 0x200, section by section.
3. Writes data/tilesets/secondary/thyrsa/porytiles_src.
4. Compiles with Porytiles in a scratch project against an empty stand-in primary,
   so the art uses only its own tiles and palettes 6-12.
5. Borrows aethos's ground: every cell drawn on grass or path gets its bottom
   layer pointed at aethos's metatile. Rebuild whenever aethos is repainted.
6. Verifies every entry and fails past 504 tiles (the door animations own
   504-511). Writes build/thyrsa/catalog.json, the sheet, the pieces preview and
   design/phase3/TILES_thyrsa.md (keeping its hand-written passes section).

Usage: /usr/bin/python3 tools/ichor/art/thyrsa_build.py [--no-compile] [--preview out.png]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emporion_build as EB  # noqa: E402
import emporion_lib as E  # noqa: E402
import thyrsa_art  # noqa: E402
import thyrsa_lib as T  # noqa: E402
from kalliste_lib import pack, write_sources  # noqa: E402

ROOT = T.ROOT
IMG = ROOT / "design/phase3/img"
DOC = ROOT / "design/phase3/TILES_thyrsa.md"
# Thyrsa merges tiles within 3 px (Emporion's 2): the masonry's speckle is noise anyway
NEAR_DUPLICATE_PX = 3
PASSES_MARK = "<!-- passes: hand-written below this line; thyrsa_build.py keeps it -->"


def spec():
    name = "thyrsa"
    return SimpleNamespace(
        name=name, dir=name, symbol="gTileset_Thyrsa", groups=T.GROUPS, art=thyrsa_art,
        temple=False,
        src=ROOT / f"data/tilesets/secondary/{name}/porytiles_src",
        bin=ROOT / f"data/tilesets/secondary/{name}/porytiles_bin",
        cfg=ROOT / "porytiles/tilesets/gTileset_Thyrsa",
        scratch=ROOT / f"build/{name}_porytiles",
        out=ROOT / f"build/{name}",
        sheet=IMG / f"{name}_sheet.png",
        pieces=IMG / f"{name}_pieces.png")


# --------------------------------------------------------------------------
# The catalog
# --------------------------------------------------------------------------

INTRO = """\
# Thyrsa tileset catalog

`gTileset_Thyrsa` is Thyrsa City, the god's own city: Thebes renamed, walled on a long
hill, older and greyer than Corinth. Pair it with the `aethos` primary, which supplies
grass, paths, olives, cypresses, pines and the hillside outside the walls. Thyrsa's
interiors are `gTileset_ThyrsaRooms` (the rooms agent), the temple's is
`gTileset_TempleDionysus` and the theater's is `gTileset_Theater`.

**This file is generated** above the passes section. `tools/ichor/art/thyrsa_build.py`
draws the tileset, compiles it and rewrites the catalog. The art is in `thyrsa_walls.py`
(streets, walls and gates), `thyrsa_town.py` (the house kit, the Agora, the market and
the garlands), `thyrsa_civic.py` (the temple, the Asclepeion, Dirke, Semele's chamber) and
`thyrsa_vines.py`; the palette plan, the masonry and the painters are in `thyrsa_lib.py`.
The map is built by `tools/ichor/maps/thyrsa.py`, which places every piece by key and
part name from `build/thyrsa/catalog.json`.

![Every Thyrsa structure on its ground](img/thyrsa_pieces.png)

The numbered sheet is [img/thyrsa_sheet.png](img/thyrsa_sheet.png). The city's render is
[img/ThyrsaCity.png](img/ThyrsaCity.png).

## How to use it

**IDs.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet ({starts}), so adding to one section never renumbers
another. `build/thyrsa/catalog.json` carries every structure's ids, walk codes, ground and
named parts.

**Collision and layers.** `X` impassable (collision 1), `.` passable, `D` a door (put the
warp here; `MB_NON_ANIMATED_DOOR`), `T` passable and drawn over the player. The vine rows
are `MB_TALL_GRASS`.

**Ground.** *aethos ground* (`grass`, `path`): the cell draws no ground of its own; the
build points its bottom layer at aethos's metatile (grass `0x001`, path `0x1D9`), so
rebuild whenever aethos is repainted. *flags* (`pave`): the street flags, drawn into the
bottom layer; the texture repeats every cell, so a prop on the flags meets the street
around it. *earth*: the vineyards' furrows. *none*: the art fills the cell.

**The masonry.** The city wall, the towers and the terrace walls share one Cyclopean
texture that repeats every 32 px. Pieces that continue a wall come as an even/odd pair:
put the even one on even map columns, or the blocks break at the joint. Wall pieces are
drawn for a wall whose battlement row is an even map row.

**Seams.** Keep this tileset out of the six rows nearest an up/down seam and the eight
columns nearest a left/right seam (MAP_DESIGN.md §5). Thyrsa's walls stand inside those
strips; the hillside outside them is aethos.

**Palettes.** Every 8x8 tile draws from one of seven groups (`thyrsa_lib.GROUPS`):

| Group | Use |
|---|---|
| stone | Theban stone: the Cyclopean walls, gates and towers, the street flags, kerbs, steps, terrace walls, Semele's chamber, Chthonia's house; ivy and smoke |
| clay | Terracotta roofs, ochre stucco, wine-purple doors and shutters, masks over doors |
| clay2 | The same, slot for slot, with limewash and vine-green paint |
| marble | The temple and the Asclepeion: marble, gold, painted blue and red; Dirke's water |
| fest | The festival: masks, garlands, ribbons, the awnings, the temple's painted doors |
| vine | The vineyards: vines, grapes, trellises, tilled earth; the fig |
| wood | The press, jars, barrels and stalls: timber, warm limestone, terracotta |

**Tile budget.** {tiles} of 504 tiles are used. The door animations copy their frames into
tiles 504-511, so the build fails past 504. Symmetric fronts are mirrored about a tile
edge, the walls and flags repeat on the 16 or 32 px grid, ivy is an overlay on the wall's
own tiles, the limewashed houses are free recolors, and tiles within two pixels of
another are redrawn as that tile.
"""


def grid(ids):
    return [" ".join(f"0x{v:03X}" for v in r) for r in ids]


NAMED_GROUND = {"grass": "aethos grass", "path": "aethos path", "pave": "the street flags",
                "earth": "tilled earth", "sand": "aethos sand", "sea": "aethos sea"}


def structure_md(s):
    out = [f"### {s['title']}\n", f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n"]
    rows = grid(s["ids"])
    out.append("```text")
    out.append("ids".ljust(len(rows[0])) + "   walk")
    for r, w in zip(rows, s["walk"]):
        out.append(r + "   " + " ".join(w))
    out.append("```\n")
    kinds = {}
    for c, g in s.get("ground", {}).items():
        kinds.setdefault(g, []).append(c)
    shown = {k: v for k, v in kinds.items() if k != "none"}
    if shown:
        if len(kinds) == 1:
            out.append(f"Ground: all on {NAMED_GROUND[next(iter(shown))]}.\n")
        else:
            parts = []
            for kind, cells in sorted(shown.items()):
                cells = sorted(cells, key=lambda c: (int(c.split(',')[1]), int(c.split(',')[0])))
                parts.append(f"{NAMED_GROUND[kind]} at " + ", ".join(f"({c})" for c in cells))
            out.append("Ground: " + "; ".join(parts) + "; the rest draws its own.\n")
    for mb, label in (("MB_NON_ANIMATED_DOOR", "Door metatiles"),
                      ("MB_TALL_GRASS", "Tall grass (`MB_TALL_GRASS`)")):
        ids = [f"0x{s['ids'][int(c.split(',')[1])][int(c.split(',')[0])]:03X}"
               for c, b in s["behaviors"].items() if b == mb]
        if ids:
            out.append(f"{label}: {', '.join(ids)}.\n")
    names = s.get("names") or {}
    if names:
        out.append("Parts: " + ", ".join(f"`{n}` 0x{s['ids'][y][x]:03X}"
                                         for n, (x, y) in names.items()) + ".\n")
    return out


def recipes_md(data):
    import thyrsa_town as TT
    out = ["## House recipes\n",
           "Houses from the kit, as id grids (top row first). The city map builds each of its "
           "households from these parts, every one different.\n"]
    for i, r in enumerate(TT.RECIPES, 1):
        cells = TT.recipe_cells(r)
        rows = [" ".join(f"0x{data[k]['ids'][data[k]['names'][n][1]][data[k]['names'][n][0]]:03X}"
                         for k, n in row) for row in cells]
        out.append(f"**{i}. {r[0]}** ({len(cells[0])} wide, {len(cells)} tall)\n")
        out.append("```text")
        out += rows
        out.append("```\n")
    return out


def write_catalog(used):
    data = {s["key"]: s for s in json.loads((ROOT / "build/thyrsa/catalog.json").read_text())}
    starts = ", ".join(f"{t.lower()} at 0x{0x200 + row * 8:03X}" for row, _, t, _ in thyrsa_art.SECTIONS)
    out = [INTRO.format(starts=starts, tiles=used)]
    for row, key, title, blurb in thyrsa_art.SECTIONS:
        out.append(f"## {title}\n\n{blurb}\n")
        for s in data.values():
            if s["section"] == key:
                out += structure_md(s)
        if key == "houses":
            out += recipes_md(data)
    passes = ""
    if DOC.exists() and PASSES_MARK in DOC.read_text():
        passes = DOC.read_text().split(PASSES_MARK, 1)[1]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text("\n".join(out).rstrip() + "\n\n" + PASSES_MARK + (passes or "\n"))
    print(DOC)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()
    sp = spec()
    sections = thyrsa_art.build()
    structs = [s for _, ss in sections for s in ss]
    keys = [s.key for s in structs]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, f"duplicate structure keys {dup}"
    probs = T.validate(structs)
    if not probs:
        before = len(EB._tiles(structs))
        merges = EB.merge_near_duplicates(structs, limit=NEAR_DUPLICATE_PX)
        print(f"merged {len(merges)} near-duplicate tiles: {before} -> "
              f"{len(EB._tiles(structs))} distinct tiles before palette sharing")
        probs = T.validate(structs)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        E.preview(structs, scale=2, cols=5).save(args.preview)
        print(args.preview)
    if probs:
        sys.exit(1)
    rows = pack(sections)
    assert rows <= 64, f"{rows} sheet rows: more than 512 metatiles"
    write_sources(structs, rows, sp.src)
    EB.catalog_json(sp, structs)
    if args.no_compile:
        return
    EB.compile_tileset(sp)
    patched = EB.borrow_ground(sp, structs)
    used = EB.verify(sp, rows, patched)
    print("colors per palette 6-12:", EB.palette_report(sp))
    IMG.mkdir(parents=True, exist_ok=True)
    EB.images(sp, structs)
    write_catalog(used)


if __name__ == "__main__":
    main()
