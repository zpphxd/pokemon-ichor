#!/usr/bin/env python3
"""Write design/phase2/TILES_emporion.md or TILES_isthmos.md from build/<name>/catalog.json.

emporion_build.py runs this after a build. Every grid comes from the structures
themselves, so the ids always match the compiled tileset.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))

INTRO = {
    "emporion": """\
# Emporion tileset catalog

`gTileset_Emporion` is Emporion City: Corinth in its prime, the great trading port of
the Isthmus, in marble and painted stone. Pair it with the `aethos` primary, which
supplies grass, paths, the sea, olives, cypresses and stone pines. Its sister,
`gTileset_Isthmos` ([TILES_isthmos.md](TILES_isthmos.md)), holds the harbor of Lechaion,
the Diolkos, the shipwright's yard and the Isthmian sanctuary; the Temple of Hermes's
interior is `gTileset_TempleHermes` ([TILES_temple_hermes.md](TILES_temple_hermes.md)).

**Why two city tilesets.** The brief's whole Isthmus (city, Agora, temple, monuments,
workshops, Acrocorinth, port, ship sheds, the Diolkos with its ship, Isthmia) came to
about 870 tiles drawn plainly and about 650 after every economy below. A secondary holds
504. The split follows the real map: Lechaion was Corinth's harbor town 3 km north, the
Diolkos crossed the Isthmus west of it, and Isthmia lay 10 km east. If the map team
builds Emporion as one map with its harbor inside it, move `emporion_port.build_port()`
into `emporion_art.py` and cut the same number of tiles elsewhere.

**This file is generated.** `tools/ichor/art/emporion_build.py emporion` draws the tileset,
compiles it and rewrites this catalog. The art is in `emporion_city.py` (streets and the
house kit), `emporion_agora.py`, `emporion_monuments.py` and `emporion_land.py`; the palette
plan, the ground mechanism and the painters are in `emporion_lib.py`.

![Every Emporion structure on its ground](img/emporion_pieces.png)

The numbered sheet is [img/emporion_sheet.png](img/emporion_sheet.png). Mock scenes of a
street, the Agora and the temple are in `img/emporion_scene_*.png` (see the end of this
file).
""",
    "isthmos": """\
# Isthmos tileset catalog

`gTileset_Isthmos` is Emporion's harbor and the Isthmus, the maps outside the city walls:
the port of Lechaion, the Diolkos (the stone track on which ships were hauled across the
Isthmus) with a merchant ship on its cradle, the shipwright's yard, and the Isthmian
sanctuary of Poseidon. Pair it with the `aethos` primary, which supplies grass, paths,
sand, the animated sea and the stone pines of Isthmia.

It is the sister of `gTileset_Emporion` ([TILES_emporion.md](TILES_emporion.md)): the city
didn't fit one secondary (see there). It carries the city's paving, kerbs, steps and the
whole house kit, drawn by the same code, so a harbor district has streets and homes that
match the city's pixel for pixel. The house recipes in TILES_emporion.md work here with
this file's ids.

**This file is generated.** `tools/ichor/art/emporion_build.py isthmos` draws the tileset,
compiles it and rewrites this catalog. The art is in `emporion_port.py`, `emporion_land.py`
and the shared `emporion_city.py`.

![Every Isthmos structure on its ground](img/isthmos_pieces.png)

The numbered sheet is [img/isthmos_sheet.png](img/isthmos_sheet.png). The port mock scene is
`img/emporion_scene_port.png`.
""",
}

USAGE = """\
## How to use it

**IDs.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet ({starts}), so adding to one section never renumbers
another; append new pieces at the end of their section. `build/{name}/catalog.json`
carries every structure's ids, walk codes, ground and named parts (`names`) for map
builders, who should place pieces by key and name, never by raw id.

**Collision and layers.** The walk grid beside each structure gives what to set on each
cell:

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `D` | Door: put the warp here. The behavior is `MB_NON_ANIMATED_DOOR`. |
| `T` | Passable, and drawn over the player, who walks behind it. |

Counters (`MB_COUNTER`) are noted where they are.

**Ground.** Each cell is on one of these:
- *aethos ground* (`grass`, `sand`, `sea`, `path`): the cell draws no ground of its own.
  After Porytiles compiles, the build points its bottom layer at aethos's own metatile
  (grass `0x001`, sand `0x124`, sea `0x170`, path `0x1D9`), so it meets the meadow, beach
  or road around it seamlessly, the sea under every ship animates, and it costs no tiles.
  These cells reference aethos's tiles by index: **rebuild whenever aethos is repainted**.
  The build checks every borrowed entry.
- *paving* (`pave`, Emporion's marble flags) or *yard* (`quay`, warm poros blocks): drawn
  into the cell's bottom layer. Both repeat every 16 px, so every paved cell shares the
  same few tiles, and a prop on paving meets the street around it exactly.
- *none*: the art fills the cell.

A cell keeps at most two layers. On aethos ground that means one drawn layer: a part
drawn over the player there can't also have a part under the player.

**Seams.** The engine draws a connected map with the tilesets of the map the player
stands on (MAP_DESIGN.md §5). Keep this tileset's pieces out of the six rows nearest an
up/down seam and the eight columns nearest a left/right seam, unless both maps share it.

**Self-contained.** Apart from the borrowed ground, the tileset is compiled against an
empty stand-in primary, so its metatiles use only its own tiles (0x200 and up) and
palettes 6-12. The build verifies this.

**Palettes.** Every 8x8 tile draws from one of seven color groups, one per secondary
palette (`emporion_lib.GROUPS`). All colors are multiples of 8, in the master palette's
families (PLAN.md):

| Group | Use |
|---|---|
| marble | Marble, gold and painted blue and red: temples, colonnades, the Peirene, the street paving and kerbs, statues, the notice board, fountain water |
| clay | Terracotta roofs, ochre stucco, Aegean-blue doors and shutters, timber; striped awnings |
| clay2 | The same colors slot for slot, with rose stucco and sea-green paint |
| stone | Poros limestone: yards, quays, warehouses, the Diolkos, Acrocorinth's crag and walls |
| wood | Timber, rope, ships, cranes, bronze and fire |
| market | The goods: pots and vases, cloth, spices, fish, wine; the kilns |
| grove | Aethos's grass, pines and laurels |

**Free recolors.** `clay` and `clay2` list their colors in the same order, so a part drawn
in ochre and recolored to rose is the same 4bpp tile in another palette: Porytiles aligns
the slots and stores it once. Every rose house part, and the rose and green awnings, cost
no tiles.

**Tile budget.** {tiles} of 504 tiles are used. A secondary has 512, but the door
animations copy their frames into tiles 504-511 (`DOOR_TILE_START_SIZE1` in
`src/field_door.c`), so the build fails past 504. To fit, the art is drawn for reuse:
symmetric fronts are mirrored about a tile edge (Porytiles stores a flipped tile once);
walls, roofs, paving, friezes and rock repeat on the 8 or 16 px grid; the Temple of
Hermes, the Asclepeion and the Hephaisteion share one porch kit, row for row; and any
tile within two pixels of another is redrawn as that tile.
"""


def tiles_used(name):
    """How many tiles the compiled tileset uses (the last non-empty tile, plus one)."""
    import numpy as np
    from PIL import Image
    a = np.array(Image.open(ROOT / f"data/tilesets/secondary/{name}/porytiles_bin/tiles.png"))
    tiles = [a[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]
    return max(i for i, t in enumerate(tiles) if t.any()) + 1


def grid(ids):
    return [" ".join(f"0x{v:03X}" for v in r) for r in ids]


def structure(s):
    out = [f"### {s['title']}\n", f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n"]
    rows = grid(s["ids"])
    out.append("```text")
    out.append("ids".ljust(len(rows[0])) + "   walk")
    for r, w in zip(rows, s["walk"]):
        out.append(r + "   " + " ".join(w))
    out.append("```\n")
    ground = s.get("ground", {})
    kinds = {}
    for c, g in ground.items():
        kinds.setdefault(g, []).append(c)
    named = {"grass": "aethos grass", "sand": "aethos sand", "sea": "aethos sea",
             "path": "aethos path", "pave": "marble paving", "quay": "poros yard paving"}
    shown = {k: v for k, v in kinds.items() if k != "none"}
    if shown:
        if len(kinds) == 1:
            out.append(f"Ground: all on {named[next(iter(shown))]}.\n")
        else:
            parts = []
            for kind, cells in sorted(shown.items()):
                cells = sorted(cells, key=lambda c: (int(c.split(',')[1]), int(c.split(',')[0])))
                parts.append(f"{named[kind]} at " + ", ".join(f"({c})" for c in cells))
            out.append("Ground: " + "; ".join(parts) + "; the rest draws its own.\n")
    doors = [f"0x{s['ids'][int(c.split(',')[1])][int(c.split(',')[0])]:03X}"
             for c, mb in s["behaviors"].items() if mb == "MB_NON_ANIMATED_DOOR"]
    if doors:
        out.append(f"Door metatiles: {', '.join(doors)}.\n")
    counters = [f"0x{s['ids'][int(c.split(',')[1])][int(c.split(',')[0])]:03X}"
                for c, mb in s["behaviors"].items() if mb == "MB_COUNTER"]
    if counters:
        out.append(f"Counter metatiles (`MB_COUNTER`): {', '.join(counters)}.\n")
    names = s.get("names") or {}
    if names:
        out.append("Parts: " + ", ".join(f"`{n}` 0x{s['ids'][y][x]:03X}"
                                         for n, (x, y) in names.items()) + ".\n")
    return out


def recipes(data):
    import emporion_city as C
    out = ["## House recipes\n",
           "Eight different houses from the kit, as id grids (top row first). Lay them in a "
           "terrace along a street, vary their widths, and give each its own door warp and "
           "household. Stack a second upper storey for a three-storey house (recipe 8). A "
           "house's door is the cell marked `D` in its ground storey.\n"]
    for i, r in enumerate(C.RECIPES, 1):
        cells = C.recipe_cells(r)
        rows = [" ".join(f"0x{data[k]['ids'][data[k]['names'][n][1]][data[k]['names'][n][0]]:03X}"
                         for k, n in row) for row in cells]
        out.append(f"**{i}. {r[0]}** ({len(cells[0])} wide, {len(cells)} tall"
                   f"{', rose' if r[1] else ', ochre'})\n")
        out.append("```text")
        out += rows
        out.append("```\n")
    return out


def main(name="emporion", tiles_used=None, sections=None):
    if sections is None:
        import importlib
        sections = importlib.import_module(f"{name}_art").SECTIONS
    cat = ROOT / f"build/{name}/catalog.json"
    doc = ROOT / f"design/phase2/TILES_{name}.md"
    data = {s["key"]: s for s in json.loads(cat.read_text())}
    starts = ", ".join(f"{t.lower()} at 0x{0x200 + row * 8:03X}" for row, _, t, _ in sections)
    if tiles_used is None:
        tiles_used = globals()["tiles_used"](name)
    out = [INTRO[name], USAGE.format(tiles=tiles_used,
                                    name=name, starts=starts)]
    listed = set()
    for row, key, title, blurb in sections:
        out.append(f"## {title}\n\n{blurb}\n")
        for s in data.values():
            if s["section"] == key and not s["key"].startswith("_"):
                listed.add(s["key"])
                out += structure(s)
        if key == "houses" and name == "emporion":
            out += recipes(data)
    missing = set(data) - listed
    assert not missing, f"emporion_catalog: no section lists {sorted(missing)}"
    if name == "emporion":
        out.append(MAP_NOTES)
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("\n".join(out).rstrip() + "\n")
    print(doc)


MAP_NOTES = """\
## Mock scenes

`tools/ichor/art/emporion_scene.py` composes four throwaway scenes from these catalogs by
structure key and renders them with `tools/ichor/render_map.py` on the compiled tilesets:
a street of merchant houses, the Agora, the port of Lechaion with the Diolkos (Isthmos),
and the Temple of Hermes on its height. They are block data, not maps.

| Image | Shows |
|---|---|
| `img/emporion_scene_street.png` | A street of the eight house recipes |
| `img/emporion_scene_agora.png` | The stoa, the Agora shop, the stalls, Pegasus, the notice board |
| `img/emporion_scene_temple.png` | The Temple of Hermes on its terrace, the Asclepeion, the Peirene, Acrocorinth behind |
| `img/emporion_scene_port.png` | Lechaion: quays, sheds, warehouses, the crane, the ship and the Diolkos |
| `img/emporion_scene_*_pass1.png`, `_pass2`, `_pass3` | The three render-and-critique passes; the unsuffixed image is the final one |
| `img/emporion_scene_temple_interior.png` | The Herald's Run, a mock of the temple's interior (TILES_temple_hermes.md) |
"""


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["emporion"]))
