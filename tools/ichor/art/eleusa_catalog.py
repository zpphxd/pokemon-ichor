#!/usr/bin/env python3
"""Write design/phase2/TILES_eleusa.md from build/eleusa/catalog.json.

eleusa_build.py runs this after a build. Every grid comes from the structures
themselves, so the ids in the document always match the compiled tileset.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/eleusa/catalog.json"
DOC = ROOT / "design/phase2/TILES_eleusa.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))

SECTIONS = [
    ("fields", "Fields", "Standing wheat (Eleusa's tall grass), harvested stubble, sheaves and "
               "Demeter's poppies. The wheat and the stubble are soft-edged: each comes as all 47 "
               "blob shapes, named by shape key."),
    ("farm", "Farmyards", "The threshing floor (agros's own alonia) and its harvest-time middle, "
             "the winnowing, pithoi standing and sunk, and the bread oven."),
    ("houses", "The house kit", "Parts that snap together into farmhouse fronts (see *House "
               "fronts* below for eight ready arrangements), and the courtyard walls that close a "
               "farm compound."),
    ("sanctuary", "The sanctuary of the Mysteries", "The Temple of Demeter, the Greater "
                  "Propylaea, the Telesterion, the Kallichoron well, the Plutonion, the Sacred "
                  "Way, the Rheitoi, the procession's torches, a field shrine and Persephone's "
                  "pomegranate. The three temples share one kit: their columns, frieze and steps "
                  "are the same tiles."),
    ("civic", "Eleusa's Asclepeion and Agora", "The village's own healing house and grain market, "
              "in its plaster and tile."),
]

INTRO = """\
# Eleusa tileset catalog

`gTileset_Eleusa` is Eleusa Village: Eleusis on its wheat plain, the third Laurel's
town. It is gold and earth, where Kalliste is whitewash and Aegean blue: ochre
plaster farmhouses under red Laconian tiles or reed thatch, ox-blood doors, golden
wheat and stubble, poppies, threshing floors and pithoi. At its heart is the sanctuary
of the Mysteries in honey marble and Eleusis's dark grey stone. Pair it with the
`aethos` primary, which supplies the grass, the limestone path, trees and the sea.

**This file is generated.** `tools/ichor/art/eleusa_build.py` paints the tileset,
compiles it and rewrites this catalog. The art lives in `eleusa_fields.py`,
`eleusa_farm.py`, `eleusa_house.py` and `eleusa_sacred.py`; the palette plan and the
borrowed-ground mechanism in `eleusa_lib.py`.

| Image | Shows |
|---|---|
| [`img/eleusa_scene.png`](img/eleusa_scene.png) | The mock scene: village, fields, sanctuary (`eleusa_scene.py`) |
| [`img/eleusa_fronts.png`](img/eleusa_fronts.png) | The eight house fronts, composed from the kit |
| [`img/eleusa_pieces.png`](img/eleusa_pieces.png) | Every structure on its ground |
| [`img/eleusa_sheet.png`](img/eleusa_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

![Mock scene](img/eleusa_scene.png)

## How to use it

**IDs.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet ({starts}). Structures are placed first-fit in build
order, so appending a new one never moves an old one. The Telesterion is 9 wide, so the
sheet stores it in two chunks; its grid below is whole. Map builders should place
pieces by key and name from `build/eleusa/catalog.json`, never by raw id.

**Collision and layers.** The walk grid beside each structure gives what to set on each
cell:

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `T` | Passable, drawn over the player, who walks behind or beneath it. |
| `G` | Tall grass: `MB_TALL_GRASS`, so wild encounters happen here. Passable. |
| `D` | Door: `MB_NON_ANIMATED_DOOR`. Put the warp here. |

**Borrowed ground.** Cells marked *grass*, *path* or *sea* below draw no ground of their
own. After Porytiles compiles, the build points their bottom-layer tiles at aethos's own
grass (`0x001`), limestone path (`0x1D9`) or animated sea (`0x170`). They meet the
meadow, the lane or the pool around them exactly, cost no Eleusa tiles, and the
Rheitoi's water animates. **Rebuild Eleusa whenever aethos is repainted**; the build
checks every borrowed entry against aethos's current metatiles. A borrowed cell keeps
only one layer of its own, so its art is either under the player (middle) or over it
(top).

**Soft ground.** The wheat and the stubble are agros's soft-ground engine
(`agros_ground.py`): a cell's piece is chosen by its shape key, the cell then its
neighbors N NE E SE S SW W NW, `1` in the field and `0` not, a diagonal counting only
when both its sides are in. `eleusa_lib.blob_key(region, x, y)` computes it from a field
mask; `eleusa_scene.py` shows the use. All 47 shapes exist, so any outline works. The
full interior is `1|11111111`. Where wheat meets stubble, give each cell the shape it
has in its own field: a strip of grass shows between, like a balk between two plots.

**Seams.** The engine draws a connected map with the tilesets of the map the player
stands on, so keep Eleusa pieces out of the six rows nearest an up/down seam and the
eight columns nearest a left/right one (MAP_DESIGN.md §5). Use aethos's own grass, path
and trees there.

**Self-contained art.** Apart from the borrowed ground, Eleusa is compiled against an
empty stand-in primary in a scratch Porytiles project under `build/`, so its art uses
only its own tiles (0x200 and up) and palettes 6-12. The build verifies every entry.

**Palettes.** Every 8x8 tile draws from one of seven color groups, one per secondary
palette (`eleusa_lib.GROUPS`). They reach Porytiles as packing hints.

| Group | Use |
|---|---|
| field | Wheat, stubble, poppies and reed thatch, on aethos grass |
| grove | The pomegranate's leaves, fruit and trunk |
| earth | The threshing floor, the Sacred Way's slabs, grain heaps, the sledge |
| clay | Pithoi, the oven, sacks and the liknon |
| house | Lime plaster, roof tiles, dark timber, ox-blood paint, the stone socle |
| marble | Honey marble, Eleusis's grey stone, gilding, torch fire |
| rock | The Plutonion's crag, the Kallichoron's curb, the Rheitoi's kerbs |

**Tile budget.** {used} of 504 tiles are used ({meta} metatiles). A secondary owns 512
tiles, but the door animations copy their frames into tiles 504-511
(`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build fails past 504. It merges
tiles within two pixels of each other, and the sacred buildings, the house kit and the
roofs are drawn on a 16 px grid so repeats share tiles. That leaves little room: new
pieces should reuse the kits' parts, or something must go.

**Scripted swaps.** The build writes the ids scripts swap to the `gTileset_Eleusa`
block at the end of `include/constants/metatile_labels.h`: `METATILE_Eleusa_TorchPost_Lit`
and `_Cold` light or put out a procession torch (setmetatile on the torch's top cell).
"""


def grid(ids, walk):
    w = max(len(f"0x{i:03X}") if i is not None else 5 for row in ids for i in row)
    lines = []
    for row, wr in zip(ids, walk):
        cells = " ".join(f"0x{i:03X}" if i is not None else "  -  " for i in row)
        lines.append(f"{cells}   {' '.join(wr)}")
    head = "ids".ljust(len(lines[0]) - len(walk[0]) * 2 + 1) + "   walk"
    return "```text\n" + head + "\n" + "\n".join(lines) + "\n```"


def main(secs=None, used=None):
    data = json.loads(CAT.read_text())
    structs, fronts = data["structures"], data["fronts"]
    from eleusa_build import SECTION_ROWS
    starts = ", ".join(f"{n} at 0x{0x200 + r * 8:03X}" for n, r in SECTION_ROWS.items())
    meta = sum(s["w"] * s["h"] for s in structs)
    out = [INTRO.format(starts=starts, used=used if used is not None else "?", meta=meta)]
    for key, title, blurb in SECTIONS:
        out.append(f"## {title}\n\n{blurb}\n")
        for s in structs:
            if s["section"] != key:
                continue
            out.append(f"### {s['title']}\n")
            out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n")
            if s["key"] in ("wheat", "stubble"):
                rows = ["| Shape key | Id | Walk |", "|---|---|---|"]
                for name, (cx, cy) in sorted(s["names"].items()):
                    rows.append(f"| `{name}` | 0x{s['ids'][cy][cx]:03X} | {s['walk'][cy][cx]} |")
                out.append("\n".join(rows) + "\n")
                continue
            out.append(grid(s["ids"], s["walk"]) + "\n")
            if s["names"]:
                parts = ", ".join(f"`{n}` 0x{s['ids'][cy][cx]:03X}"
                                  for n, (cx, cy) in s["names"].items())
                out.append(f"Pieces: {parts}.\n")
            if s["ground"]:
                kinds = sorted(set(s["ground"].values()))
                cells = ", ".join(sorted(s["ground"]))
                out.append(f"Borrowed ground ({', '.join(kinds)}): cells {cells}.\n")
            doors = [f"0x{s['ids'][int(k.split(',')[1])][int(k.split(',')[0])]:03X}"
                     for k, mb in s["behaviors"].items() if mb == "MB_NON_ANIMATED_DOOR"]
            if doors and s["section"] != "houses":
                out.append(f"Door metatile{'s' if len(doors) > 1 else ''}: {', '.join(doors)}.\n")
        if key == "houses":
            out.append("### House fronts\n")
            out.append("Every house in Eleusa is a home (MAP_DESIGN.md §2), so each front has a "
                       "door. These eight are arrangements of the parts above and cost no "
                       "metatiles of their own; mix the parts for more. A `-` cell is not part "
                       "of the house: leave the map's own ground there. Walk: every house cell "
                       "is `X` except its door cells (`D`).\n\n"
                       "![House fronts](img/eleusa_fronts.png)\n")
            for k, f in fronts.items():
                walk = []
                for row in f["rows"]:
                    walk.append("".join("-" if r == "." else ("D" if r.startswith("doors.") or
                                                               r == "porch.W1_door" else "X")
                                        for r in row))
                out.append(f"**{f['title']}** (`{k}`): {f['who']}.\n")
                out.append(grid(f["ids"], walk) + "\n")
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text("\n".join(out))
    print(DOC.relative_to(ROOT))


if __name__ == "__main__":
    main()
