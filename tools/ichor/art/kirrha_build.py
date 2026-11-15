#!/usr/bin/env python3
"""Draw, compile and catalog gTileset_Kirrha (Kirrha and Aigion, the harbor towns
of the Gulf crossing) and gTileset_GulfFerry (Panopeus's deck, Route 10).

The pipeline is thyrsa_build.py's (emporion_build.py's, function for function):
1. kirrha_art.build(name) draws every structure; each 8x8 tile must draw from one
   of kirrha_lib.GROUPS. Tiles within 2 px of another are redrawn as that one.
2. Packs them into the 8-wide sheet from 0x200, section by section.
3. Writes data/tilesets/secondary/<dir>/porytiles_src.
4. Compiles with Porytiles in a scratch project against an empty stand-in primary,
   so the art uses only its own tiles and palettes 6-12.
5. Borrows aethos's ground: every cell drawn on grass, path, sand or sea gets its
   bottom layer pointed at aethos's metatile (the sea animates). Rebuild whenever
   aethos is repainted.
6. Verifies every entry and fails past 504 tiles (the door animations own
   504-511). Writes build/<dir>/catalog.json, the sheet, the pieces preview and
   design/phase3/TILES_kirrha.md (keeping its hand-written passes section).

Usage: /usr/bin/python3 tools/ichor/art/kirrha_build.py [kirrha|gulf_ferry|all]
       [--no-compile] [--preview out.png]
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
import kirrha_art  # noqa: E402
import kirrha_lib as KL  # noqa: E402
from kalliste_lib import pack, write_sources  # noqa: E402

ROOT = KL.ROOT
IMG = ROOT / "design/phase3/img"
DOC = ROOT / "design/phase3/TILES_kirrha.md"
NEAR_DUPLICATE_PX = 3
PASSES_MARK = "<!-- passes: hand-written below this line; kirrha_build.py keeps it -->"
SYMBOLS = {"kirrha": "gTileset_Kirrha", "aigion": "gTileset_Aigion", "gulf_ferry": "gTileset_GulfFerry"}


def spec(name):
    return SimpleNamespace(
        name=name, dir=name, symbol=SYMBOLS[name], groups=KL.GROUPS, art=kirrha_art,
        temple=False,
        src=ROOT / f"data/tilesets/secondary/{name}/porytiles_src",
        bin=ROOT / f"data/tilesets/secondary/{name}/porytiles_bin",
        cfg=ROOT / f"porytiles/tilesets/{SYMBOLS[name]}",
        scratch=ROOT / f"build/{name}_porytiles",
        out=ROOT / f"build/{name}",
        sheet=IMG / f"{name}_sheet.png",
        pieces=IMG / f"{name}_pieces.png")


INTRO = """\
# Kirrha tileset catalog

Three secondaries on the `aethos` primary, for the Gulf crossing (SCRIPT.md beat 37), all
drawn by the same painters from one palette plan:

- **`gTileset_Kirrha`**: Kirrha, Delphoi's harbor at the head of the Krisaian gulf. The
  grey quay, moored boats, nets and the fish market under the fig, the Agora's shed, the
  houses (limewashed, from one kit), and the land around: the grey crags of Parnassos, the
  Phaidriades with Delphoi's roofs in their cleft, laurels, the pilgrims' gate, the fence
  of Apollo's plain, the rock in the bay.
- **`gTileset_Aigion`**: Aigion, the Achaean port across the gulf: the same quay, boats and
  crags, the houses in ochre, the ring of old planes round the altar of Zeus, the street's
  steps, Helike's drowned roofs. BUILD.md planned one `kirrha` set for both towns; one set
  came to some 610 tiles against the 504 the door animations leave, so Aigion has its own
  (the shared pieces cost ROM twice, a few KB, and nothing in looks).
- **`gTileset_GulfFerry`**: the deck of Panopeus's ferry (Route 10, `MAP_GULF_FERRY_DECK`).
  SCRIPT.md Part 10 says to reuse the `trireme` deck pieces; world-act1's Euploia isn't on
  this branch, so the deck is drawn here, small: one mast with a patched square sail, a low
  deckhouse and the steering oar at the stern, a goat pen amidships, rope and lashed
  amphorae at the bow. It is its own secondary so the towns keep their 504 tiles.

**This file is generated** above the passes section. `tools/ichor/art/kirrha_build.py
[kirrha|gulf_ferry|all]` draws both, compiles them and rewrites the catalog. The art is in
`kirrha_harbor.py` (the waterfront), `kirrha_land.py` (crags, trees, the sacred places),
`kirrha_town.py` (the house kit and the households' recipes) and `kirrha_deck.py` (the
ferry); the palette plan and the painters are in `kirrha_lib.py`. The maps are built by
`tools/ichor/maps/harbors.py`, which places every piece by key and part name from
`build/kirrha/catalog.json` and `build/gulf_ferry/catalog.json`.

![Every Kirrha structure on its ground](img/kirrha_pieces.png)
![The ferry's pieces](img/gulf_ferry_pieces.png)

The numbered sheets are [img/kirrha_sheet.png](img/kirrha_sheet.png) and
[img/gulf_ferry_sheet.png](img/gulf_ferry_sheet.png). The map renders are
[img/Kirrha.png](img/Kirrha.png), [img/GulfFerry_Deck.png](img/GulfFerry_Deck.png) and
[img/Aigion.png](img/Aigion.png).

## How to use it

**IDs.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of its sheet, so adding to one section never renumbers another.

**Collision and layers.** `X` impassable (collision 1), `.` passable, `D` a door (put the
warp here; `MB_NON_ANIMATED_DOOR`), `T` passable and drawn over the player.

**Ground.** *aethos ground* (`grass`, `path`, `sand`, `sea`): the cell draws no ground of
its own; the build points its bottom layer at aethos's metatile (grass `0x001`, path
`0x1D9`, sand `0x124`, sea `0x170`), so a boat's water animates with the gulf around it.
Rebuild whenever aethos is repainted. *quay*: the grey quay paving, drawn here, repeating
every cell. *deck*: the ferry's planks. *none*: the art fills the cell.

**Seams.** Keep these tilesets out of the strips the engine copies across a connection
(MAP_DESIGN.md §5). Kirrha's north edge joins Route 9 (`parnassos`) with offset +18:
`fieldmap.c` copies only Kirrha's columns 11 and up across that seam, so rows 0-5 are
aethos-only from column 11 east, and the Phaidriades stand in columns 0-10, which Route 9
never draws. Aigion's south edge (Route 11, batch 3) keeps its six southern rows aethos-only.

**Palettes.** Every 8x8 tile draws from one of seven groups (`kirrha_lib.GROUPS`):

| Group | Use |
|---|---|
| crag | Parnassos's grey limestone (aethos's own warm greys in the middle of the ramp, with the Phaidriades' rust): crags, cliffs, the quay, piers, steps; laurel scrub and algae; aethos's grass on rims |
| clay | Kirrha's houses: terracotta, limewash, laurel-green shutters, door timber, grey quoins |
| clay2 | Aigion's houses, slot for slot: ochre stucco, blue shutters |
| wood | Timber, rope, linen and paint: boats, nets, racks, the shed, the gate's leaves, the fence, the deck |
| sea | Foam, the rock in the bay, the drowned roofs under the water |
| grove | Laurels, figs' and planes' leaves, bark, on aethos grass |
| market | Marble and bronze, fish and bread, amphorae, the fig's grey bark: the fish market, Delphoi's roofs, the altar of Zeus |

**Tile budget.** gTileset_Kirrha uses {kirrha} of 504 tiles, gTileset_Aigion {aigion} and gTileset_GulfFerry
{gulf_ferry}. Faces and pavings repeat on the 16 or 32 px grid, Aigion's houses are the
recolors of Kirrha's, and tiles within two pixels of another are redrawn as that tile.
"""


def grid(ids):
    return [" ".join(f"0x{v:03X}" for v in r) for r in ids]


NAMED_GROUND = {"grass": "aethos grass", "path": "aethos path", "sand": "aethos sand",
                "sea": "aethos sea", "quay": "the quay paving", "deck": "the deck's planks"}


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
    for mb, label in (("MB_NON_ANIMATED_DOOR", "Door metatiles"),):
        ids = [f"0x{s['ids'][int(c.split(',')[1])][int(c.split(',')[0])]:03X}"
               for c, b in s["behaviors"].items() if b == mb]
        if ids:
            out.append(f"{label}: {', '.join(ids)}.\n")
    names = s.get("names") or {}
    if names:
        out.append("Parts: " + ", ".join(f"`{n}` 0x{s['ids'][y][x]:03X}"
                                         for n, (x, y) in names.items()) + ".\n")
    return out


def recipes_md(data, tileset):
    import kirrha_town as KT
    out = ["#### House recipes\n",
           "Households from the kit, as id grids (top row first).\n"]
    for name, rows in KT.RECIPES.items():
        aig = name in ("achaean", "goatherd")
        if aig != (tileset == "aigion"):
            continue
        kit, sg = ("house_aigion", "house_signs_aigion") if aig else ("house", "house_signs")
        lines = []
        for row in rows:
            ids = []
            for part in row:
                key = kit if part in data[kit]["names"] else sg
                x, y = data[key]["names"][part]
                ids.append(f"0x{data[key]['ids'][y][x]:03X}")
            lines.append(" ".join(ids))
        out.append(f"**{name}** ({len(rows[0])} wide, {len(rows)} tall)\n")
        out += ["```text"] + lines + ["```\n"]
    return out


def write_catalog(used):
    out = []
    for name in ("kirrha", "aigion", "gulf_ferry"):
        cat = ROOT / f"build/{name}/catalog.json"
        if not cat.exists():
            continue
        data = {s["key"]: s for s in json.loads(cat.read_text())}
        out.append(f"## `{SYMBOLS[name]}`\n")
        for row, key, title, blurb in kirrha_art.SECTIONS[name]:
            out.append(f"### Section: {title} (from 0x{0x200 + row * 8:03X})\n\n{blurb}\n")
            for s in data.values():
                if s["section"] == key:
                    out += ["#" + ln if ln.startswith("### ") else ln for ln in structure_md(s)]
            if key == "town":
                out += recipes_md(data, name)
    passes = ""
    if DOC.exists() and PASSES_MARK in DOC.read_text():
        passes = DOC.read_text().split(PASSES_MARK, 1)[1]
    intro = INTRO.format(kirrha=used.get("kirrha", "?"), aigion=used.get("aigion", "?"),
                         gulf_ferry=used.get("gulf_ferry", "?"))
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(intro + "\n" + "\n".join(out).rstrip() + "\n\n" + PASSES_MARK + (passes or "\n"))
    print(DOC)


def used_tiles(sp):
    try:
        from PIL import Image
        import numpy as np
        a = np.array(Image.open(sp.bin / "tiles.png"))
        tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
        return max(i for i, tl in enumerate(tiles) if tl.any()) + 1
    except Exception:
        return "?"


def build_one(name, args):
    sp = spec(name)
    sections = kirrha_art.build(name)
    structs = [s for _, ss in sections for s in ss]
    keys = [s.key for s in structs]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, f"duplicate structure keys {dup}"
    probs = KL.validate(structs)
    if not probs:
        before = len(EB._tiles(structs))
        merges = EB.merge_near_duplicates(structs, limit=NEAR_DUPLICATE_PX)
        print(f"{name}: merged {len(merges)} near-duplicate tiles: {before} -> "
              f"{len(EB._tiles(structs))} distinct tiles before palette sharing")
        probs = KL.validate(structs)
    for p in probs:
        print("PROBLEM:", p)
    if args.preview:
        out = Path(args.preview)
        out = out.with_name(f"{out.stem}_{name}{out.suffix}")
        E.preview(structs, scale=2, cols=5).save(out)
        print(out)
    if probs:
        sys.exit(1)
    rows = pack(sections)
    assert rows <= 64, f"{rows} sheet rows: more than 512 metatiles"
    write_sources(structs, rows, sp.src)
    EB.catalog_json(sp, structs)
    if args.no_compile:
        return None
    EB.compile_tileset(sp)
    patched = EB.borrow_ground(sp, structs)
    used = EB.verify(sp, rows, patched)
    print(f"{name}: colors per palette 6-12:", EB.palette_report(sp))
    IMG.mkdir(parents=True, exist_ok=True)
    EB.images(sp, structs)
    return used


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tileset", nargs="?", default="all", choices=["kirrha", "aigion", "gulf_ferry", "all"])
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--preview", help="write a composited preview of every structure here")
    args = ap.parse_args()
    names = ["kirrha", "aigion", "gulf_ferry"] if args.tileset == "all" else [args.tileset]
    used = {}
    for n in names:
        u = build_one(n, args)
        if u is not None:
            used[n] = u
    if args.no_compile:
        return
    for n in ("kirrha", "aigion", "gulf_ferry"):
        if n not in used and (ROOT / f"data/tilesets/secondary/{n}/porytiles_bin/tiles.png").exists():
            used[n] = used_tiles(spec(n))
    write_catalog(used)


if __name__ == "__main__":
    main()
