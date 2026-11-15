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
black firs, grey rock and its cliffs, ivy, the border fort of Eleutherai with its
Cyclopean walls, the god's roofless temple, the maenads' mountain, and on the Asopos
plain below, the Kronia: red-and-cream awnings, bread, gold cloth. Four secondaries on
the `aethos` primary, drawn by one set of painters:

| Tileset | Maps |
|---|---|
| `gTileset_Kithairon` | Route 6, Eleutherai |
| `gTileset_KithaironPass` | Mt. Kithairon (the polish pass gave the climb its own set) |
| `gTileset_Kronia` | Route 7 and the Kronia grounds |
| `gTileset_KithaironCave` | Antiope's cave |

**This catalog is generated** by `tools/ichor/art/kithairon_build.py` (painters:
`kithairon_ground.py`, `_trees.py`, `_stone.py`, `_vines.py`, `_houses.py`, `_camp.py`,
`_cliffs.py`; palettes and the soft-shape engine in `kithairon_lib.py`). The
render-and-critique passes at the end are written by hand and kept across rebuilds.

## How it fits together

**Why four sets, not one.** BUILD.md asked for one `kithairon` secondary for all four
outdoor maps, so their seams need no aethos-only strip. Everything the crossing needs
is far more than a secondary's 504 tiles, so the art is split, and the seams still need
no aethos-only strip: Kithairon, KithaironPass and Kronia all begin with the same
**core** section (soft ground, firs and the oak, the cliffs and their faces, stairs,
ledges, rocks, deadfall, stones and markers), painted from the same pixels and packed at
the same metatile ids. The game draws a connected neighbor with the tilesets of the map
the player stands on, and a core metatile looks the same in any of the three. The map
builder keeps the six rows either side of the Eleutherai / Mt. Kithairon and
Mt. Kithairon / Route 7 seams to core and aethos metatiles. The cave is its own small set.

**Place pieces by key and cell name** from `build/kithairon/<dir>/catalog.json`, never by
raw id (`tools/ichor/maps/kithairon.py` does). Ids below are the current build's.

**Soft ground.** `tall`, `path`, `water`, `trampled` and `cave` hold one piece per blob
shape key: `1|` then the cell's neighbors N NE E SE S SW W NW, `1` in the region and `0`
not, a diagonal counting only when both its sides are in. `kithairon_lib.blob_key`
computes it. The map builder lists the keys its maps use in
`tools/ichor/art/kithairon_shapes.json` (`kithairon.py --shapes`), and only those are drawn.

**Tiers and cliffs** (the polish pass). The map builder gives every cell a height. A
raised tier is outlined by `cliff`: a rocky rim along its north, west and east edges,
and along its south edge a lit lip over a 24 px limestone face of tall slabs that takes
the tier's two southmost rows and darkens to a shadow at its foot. Its keys are blob keys
plus `|1` (the tier goes on two rows down) or `|0` (the face's upper row), and `|b` for
the face's second phase, so the slabs repeat every 32 px, not 16. Firs standing on a
boundary hide the cliff; elsewhere it shows. `cliff_face` dresses a face (ivy, a crack,
a tuft, a seep, a fern), `cliff_stair` cuts steps through it, `ledge` gives one-way rock
drops (south on Mt. Kithairon, north down Route 7's north face).

- `water` is aethos's animated sea under a pebbly bank with reeds: MB_POND_WATER,
  surfable and fishable. It is in the pass and Kronia sets, not the core.

**Walk codes** in the grids: `X` blocks, `.` walkable, `T` walkable and drawn over the
player, `G` tall grass, `J` a ledge (MB_JUMP_SOUTH), `D` a door (MB_NON_ANIMATED_DOOR: put
the warp there). The north ledges are `X` cells with MB_JUMP_NORTH.

**Borrowed ground.** Cells marked *grass*, *path*, *sea*, *shade* or *tall* draw no ground
of their own: the build points their bottom tiles at aethos's grass (`0x001`), road
(`0x1D9`), animated sea (`0x170`), deep shade (`0x01C`) or tall grass (`0x00D`). Rebuild
these sets whenever aethos is repainted.

**Palettes.** Seven groups, one per secondary palette; every 8x8 tile draws from one.

| Group | Use |
|---|---|
| field | tall grass, the road, its edges; the maenads' drums |
| rock | cliffs, ledges, rocks, the cave, ivy and the marked ivy, shrines, the herm |
| tree | firs, oaks, deadfall |
| vine | trellises, the wine-cart |
| house | Eleusa's house kit, verbatim |
| stone | Cyclopean walls, the temple, the wine press, troughs |
| camp | the Kronia's awnings, tables, tents, stage, banner, oven; the brazier |

**Scripted swaps** (`include/constants/metatile_labels.h`): `METATILE_Kithairon_Barrier_W`
and `_E` (the herald's pole, beat 26), `METATILE_KithaironPass_Shrine_Top`, `_Shrine`,
`_ShrineBad_Top`, `_ShrineBad` (the shrine once cleansed), and
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
            if name in ("kronia", "pass") and sec == "core":
                out.append("### Core\n\nThe same structures at the same ids as in "
                           "`gTileset_Kithairon`'s core, above.\n")
                continue
            out.append(f"### {KB.SECTION_TITLES[sec]}\n")
            for s in structs:
                st = {"ids": ids[s.key], "walk": s.walk, "w": s.w, "h": s.h}
                out.append(f"#### {s.title}\n")
                out.append(f"`{s.key}`, {s.w} wide by {s.h} tall. {s.notes}\n")
                if s.key in ("tall", "path", "water", "cave", "cliff", "trampled"):
                    first = next(iter(s.names))
                    out.append(f"{len(s.names)} shapes, from 0x{ids[s.key][0][0]:03X}; the first, "
                               f"`{first}`, is 0x{ids[s.key][0][0]:03X}.\n")
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
