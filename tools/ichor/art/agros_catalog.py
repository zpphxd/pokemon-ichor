#!/usr/bin/env python3
"""Write design/phase1/TILES_agros.md from build/agros/catalog.json.

agros_build.py runs this after a build. Every grid comes from the structures
themselves, so the ids in the document always match the compiled tileset.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/agros/catalog.json"
DOC = ROOT / "design/phase1/TILES_agros.md"

SECTIONS = [
    ("ground", "Soft ground", "Tall grass, the road and goat tracks, with edges that follow the land "
               "instead of the grid. These are painted per shape (see below), so the grids list "
               "shape keys rather than a fixed layout."),
    ("flora", "Trees, shrubs and herbs", "The ancient olive, a fig, broom, oleander, thyme, field herbs "
              "and soft shade."),
    ("stone", "Stone", "Rocks, field walls that join any way, the terrace lip, Kronion's rock bands, the "
              "rocky shore and the threshing floor."),
    ("props", "Farm and roadside props", "The cart, the bee wall, the spring and a roadside shrine."),
    ("ruins", "Kronion's ruins (copied from kalliste)", "Pixel-for-pixel copies of the kalliste pieces "
              "Route 1 and Kronion Hill use, so those maps need only aethos + agros. See TILES_kalliste.md "
              "for how they fit together."),
]

INTRO = """\
# Agros tileset catalog

`gTileset_Agros` is Ichor's countryside secondary tileset: the rural art for Route 1,
Kronion Hill and the routes to come. Pair it with the `aethos` primary, which supplies
the grass, plain tall grass, the road's middle, olives, pines, cypresses and the sea.
The name is Greek for field, the land outside the town walls.

**This file is generated.** `tools/ichor/art/agros_build.py` paints the tileset,
compiles it and rewrites this catalog. The numbered sheet is
[`img/agros_sheet.png`](img/agros_sheet.png).

![Agros sheet](img/agros_sheet.png)

## How to use it

**IDs.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet ({starts}); adding to one section never renumbers
another, so append new pieces to their section.

**Collision and layers.** The walk grid beside each structure gives what to set on each
cell when placing it:

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `T` | Passable, drawn over the player, who walks behind it. |
| `G` | Passable tall grass: the behavior is `MB_TALL_GRASS`, so wild encounters happen here. |
| `J` | Ledge: `MB_JUMP_SOUTH`. Set collision 1, as vanilla does for ledges. |

**Named pieces.** Sets that are picked by context (wall joins, shore sides, rock-band
ends, ground shapes) give each piece a name. `build/agros/catalog.json` carries a
`names` map from name to cell, and `tools/ichor/maps/route1.py` shows how a map
builder chooses them.

**Soft ground and shape keys.** Tall grass, the road and goat tracks are painted per
cell from the cell's 3×3 neighborhood:

- The region is the union of its cells at pixel level, opened with a rounded brush:
  shrunk by a margin, grown back by a corner radius, its edge wobbled by a noise that
  repeats every 16 px. So every piece meets its neighbors seamlessly, and pieces that
  share a corner share 8×8 tiles.
- A shape key is the cell's state then its neighbors' in the order N NE E SE S SW W NW:
  `1` in the region, `0` not, and for road and meadow cells the letters `a b c d` for a
  *half cell*, a grass cell in a stair-step corner whose region is the triangle toward
  its NE, SE, SW or NW corner. Half cells turn one-cell steps into diagonals, so the
  road meanders instead of stair-stepping.
- A diagonal counts only when both of its sides are filled.
- A fully surrounded cell is plain aethos: `0x00D` tall grass, `0x1D9` road.
- Only the shapes the maps use are built. They are listed in
  `tools/ichor/art/agros_shapes.json`; `route1.py --shapes` updates the list, and
  Agros must then be rebuilt.

**Self-contained build.** Agros is compiled against an empty stand-in primary in a
scratch Porytiles project under `build/`. Its metatiles use only its own tiles (0x200
and up) and palettes 6–12, so they keep working whatever aethos becomes; the build
verifies this. Its ground pieces are painted from aethos's own pixels (grass, tall
grass, road), read from the compiled aethos tileset at build time, so they meet aethos
ground exactly. **Rebuild Agros whenever aethos's grass, tall grass or road change.**
`porytiles/tilesets/gTileset_Agros/config.yaml` pairs Agros with aethos for a direct
Porytiles compile.

**The sea.** Agros draws no water except the spring's basin. The rocky shore paints
rocks and foam on the sea side of a grass cell, and the sea itself is the neighboring
aethos `0x170`, so it animates.

**Palettes.** Every 8×8 tile draws from one of seven color groups, one per secondary
palette:

| Group | Use |
|---|---|
| Field | Grass, barley, the road and bare earth, herbs |
| Grove | Olive, fig and cypress foliage, bark, shade |
| Rock | Limestone on grass: rocks, walls, the lip, the hill's rock bands, the threshing floor |
| Clay | The cart and its load, the bee wall's hives |
| Bloom | Broom, oleander and thyme in flower |
| Water | The spring, the rocky shore's greys and foam, the shrine's whitewash and blue |
| Kalliste stone | The copied ruins and terraces, in kalliste's own stone palette |

**Tile budget.** {tiles} of 504 tiles are used. A secondary owns 512, but door animations copy their frames into tiles 504–511, so `agros_build.py` fails the build past 504.

**Scripted swaps.** `agros_build.py` writes the ids scripts swap in to the `gTileset_Agros` block at the end of `include/constants/metatile_labels.h` (today `METATILE_Agros_PitStair_Left` and `_Right`, Kronion Hill's dark stair), so they never go stale.

**Seams.** A map connected to another is drawn with the tilesets of the map the player stands on. So the rows of Route 1 a player in Akti or Elaia can see (0–4 and 59–63) use aethos pieces only; `route1.py` swaps in aethos's own and fails the build on any Agros piece there. A future map on Agros should do the same at its seams.
"""


def grid(ids):
    return "\n".join(" ".join(f"0x{v:03X}" for v in r) for r in ids)


def main(secs=None, tiles_used=None):
    data = json.loads(CAT.read_text())
    starts = []
    for key, title, _ in SECTIONS:
        ids = [s["ids"][0][0] for s in data if s["section"] == key]
        if ids:
            starts.append(f"{title.split(' (')[0].lower()} at 0x{min(ids):03X}")
    out = [INTRO.format(tiles=tiles_used if tiles_used is not None else "About 480",
                        starts=", ".join(starts))]
    for key, title, blurb in SECTIONS:
        items = [s for s in data if s["section"] == key]
        if not items:
            continue
        out.append(f"## {title}\n\n{blurb}\n")
        for s in items:
            out.append(f"### {s['title']}\n")
            out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n")
            if key == "ground":
                out.append("| Shape key | Id | Walk |\n|---|---|---|")
                for name, (cx, cy) in s["names"].items():
                    out.append(f"| `{name}` | 0x{s['ids'][cy][cx]:03X} | {s['walk'][cy][cx]} |")
                out.append("")
                continue
            out.append("```text")
            g = grid(s["ids"]).split("\n")
            out.append("ids".ljust(len(g[0])) + "   walk")
            for row_ids, row_walk in zip(g, s["walk"]):
                out.append(row_ids + "   " + " ".join(row_walk))
            out.append("```\n")
            if s["names"]:
                named = ", ".join(f"`{n}` 0x{s['ids'][c[1]][c[0]]:03X}" for n, c in s["names"].items())
                out.append(f"Pieces: {named}.\n")
    DOC.write_text("\n".join(out).rstrip() + "\n")
    print(DOC)


if __name__ == "__main__":
    main()
