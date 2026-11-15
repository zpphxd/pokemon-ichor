"""Write design/phase3/TILES_kithairon.md: the Kithairon crossing's tile catalog.

The catalog part is generated from the build (kithairon_build.py calls main).
Everything from the heading "## Render-and-critique passes" on is written by
hand and kept as it is on every rebuild.
"""
from __future__ import annotations

from pathlib import Path

import kithairon_build as KB

DOC = KB.ROOT / "design/phase3/TILES_kithairon.md"
KEEP = "## Render-and-critique passes"

HEAD = """# The Kithairon crossing's tilesets

The road north from Eleusa over Mt. Kithairon to Thyrsa: vine terraces and dry stone,
black firs, grey rock, ivy, the border fort of Eleutherai with its Cyclopean walls,
the god's roofless temple, the maenads' mountain, and on the Asopos plain below, the
Kronia: red-and-cream awnings, bread, gold cloth. Three secondaries on the `aethos`
primary, drawn by one set of painters:

| Tileset | Maps |
|---|---|
| `gTileset_Kithairon` | Route 6, Eleutherai, Mt. Kithairon |
| `gTileset_Kronia` | Route 7 and the Kronia grounds |
| `gTileset_KithaironCave` | Antiope's cave |

**This catalog is generated** by `tools/ichor/art/kithairon_build.py` (painters:
`kithairon_ground.py`, `_trees.py`, `_stone.py`, `_vines.py`, `_houses.py`, `_camp.py`;
palettes and the soft-shape engine in `kithairon_lib.py`). The render-and-critique
passes at the end are written by hand and kept across rebuilds.

## How it fits together

**Why three sets, not one.** BUILD.md asked for one `kithairon` secondary for all four
outdoor maps, so their seams need no aethos-only strip. Everything the crossing needs
came to about 700 tiles against a secondary's 504, so the art is split, and the seam
still needs no aethos-only strip: Kithairon and Kronia both begin with the same **core**
section (soft ground, firs and the oak, crag detail, stones and markers), painted from
the same pixels and packed at the same metatile ids. The game draws a connected
neighbor with the tilesets of the map the player stands on, and a core metatile looks
the same in either set. The map builder keeps the six rows either side of the
Mt. Kithairon / Route 7 seam to core and aethos metatiles. The cave is its own small set.

**Place pieces by key and cell name** from `build/kithairon/<dir>/catalog.json`, never by
raw id (`tools/ichor/maps/kithairon.py` does). Ids below are the current build's.

**Soft ground.** `tall`, `path`, `crag`, `water` and `cave` hold one piece per blob
shape key: `1|` then the cell's neighbors N NE E SE S SW W NW, `1` in the region and `0`
not, a diagonal counting only when both its sides are in. `kithairon_lib.blob_key`
computes it. The map builder lists the keys its maps use in
`tools/ichor/art/kithairon_shapes.json` (`kithairon.py --shapes`), and only those are drawn.

- `crag` is Kithairon's grey limestone: a weathered top, and a 14 px face with strata
  along every south edge, so a crag reads as a rise with a cliff below it. Scatter
  `crag_detail`'s interior cells through a big crag; its south-face cells carry ivy,
  the marked ivy of the Thyrsus walls and a cave mouth.
- `water` is aethos's animated sea under a pebbly bank with reeds: MB_POND_WATER,
  surfable and fishable.

**Walk codes** in the grids: `X` blocks, `.` walkable, `T` walkable and drawn over the
player, `G` tall grass, `D` a door (MB_NON_ANIMATED_DOOR: put the warp there).

**Borrowed ground.** Cells marked *grass*, *path*, *sea* or *tall* draw no ground of
their own: the build points their bottom tiles at aethos's grass (`0x001`), road
(`0x1D9`), animated sea (`0x170`) or tall grass (`0x00D`). Rebuild these sets whenever
aethos is repainted.

**Palettes.** Seven groups, one per secondary palette; every 8x8 tile draws from one.

| Group | Use |
|---|---|
| field | tall grass, the road, its edges |
| rock | crags, the cave, boulders, ivy and the marked ivy, shrines, the herm |
| tree | firs, oaks |
| vine | trellises, the old vines, the wine-cart |
| house | Eleusa's house kit, verbatim |
| stone | Cyclopean walls, the temple, the wine press, troughs |
| camp | the Kronia's awnings, tables, tents, stage, banner, oven; the brazier |

**Scripted swaps** (`include/constants/metatile_labels.h`): `METATILE_Kithairon_OldVines`,
`_OldVines_B` and `_OldVines_Stumps` (the vines across Route 6, beat 26), and
`METATILE_KithaironCave_Brazier_ColdTop`, `_Cold`, `_LitTop`, `_Lit`.
"""


def grid_block(st):
    ids = st["ids"]
    lines = []
    for y in range(st["h"]):
        row = " ".join(f"0x{ids[y][x]:03X}" for x in range(st["w"]))
        walk = " ".join(st["walk"][y])
        lines.append(f"{row}   {walk}")
    return "```text\n" + "\n".join(lines) + "\n```"


def main(report, ss):
    out = [HEAD]
    out.append("## Budget\n")
    out.append("| Tileset | Tiles | Metatiles |")
    out.append("|---|---|---|")
    for name, (used, metas, _, _) in report.items():
        out.append(f"| `{KB.SETS[name]['symbol']}` | {used} of {KB.TILE_LIMIT} | {metas} of 512 |")
    out.append("")
    for name, (used, metas, secs, ids) in report.items():
        info = KB.SETS[name]
        out.append(f"## `{info['symbol']}`: {info['title']}\n")
        out.append(f"![sheet](img/tiles_{info['dir']}_sheet.png)\n")
        for sec, structs in secs:
            if name == "kronia" and sec == "core":
                out.append("### Core\n\nThe same structures at the same ids as in "
                           "`gTileset_Kithairon`'s core, above.\n")
                continue
            out.append(f"### {KB.SECTION_TITLES[sec]}\n")
            for s in structs:
                st = {"ids": ids[s.key], "walk": s.walk, "w": s.w, "h": s.h}
                out.append(f"#### {s.title}\n")
                out.append(f"`{s.key}`, {s.w} wide by {s.h} tall. {s.notes}\n")
                if s.key in ("tall", "path", "crag", "water", "cave"):
                    out.append(f"{len(s.names)} shapes, from 0x{ids[s.key][0][0]:03X}; the "
                               f"interior `1|11111111` is 0x{ids[s.key][0][0]:03X}.\n")
                    continue
                out.append(grid_block(st) + "\n")
                if s.names:
                    named = ", ".join(f"`{n}` 0x{ids[s.key][c[1]][c[0]]:03X}" for n, c in s.names.items())
                    out.append(f"Pieces: {named}.\n")
                gr = getattr(s, "ground", {})
                if gr:
                    kinds = sorted(set(gr.values()))
                    out.append("Borrowed ground: " + "; ".join(
                        f"{k} at " + ", ".join(f"{x},{y}" for (x, y), g in sorted(gr.items()) if g == k)
                        for k in kinds) + ".\n")
    text = "\n".join(out) + "\n"
    old = DOC.read_text() if DOC.exists() else ""
    if KEEP in old:
        text += old[old.index(KEEP):]
    else:
        text += KEEP + "\n\n(Written by hand; see each map's passes below.)\n"
    DOC.write_text(text)
    print(DOC.relative_to(KB.ROOT))
