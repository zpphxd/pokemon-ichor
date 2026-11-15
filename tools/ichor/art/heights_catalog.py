"""Write design/phase3/TILES_heights.md: the Arkadian climb's tile catalog.

The catalog part is generated from the build (heights_build.py calls main).
Everything from the heading "## Render-and-critique passes" on is written by
hand and kept as it is on every rebuild.
"""
from __future__ import annotations

import heights_build as HB

DOC = HB.ROOT / "design/phase3/TILES_heights.md"
KEEP = "## Render-and-critique passes"

HEAD = """# The Arkadian climb's tilesets

Aigion to Arkadia: the Krathis gorge, its white water and its fallen temple of
Artemis; the Styx's black cliff and still black pool, and Nonakris's slab-roofed
houses; Kyllene's wind-combed meadow, its tortoise boulders, the hawk's cliff, and
the first cypresses. Two secondaries on the `aethos` primary:

| Tileset | Maps |
|---|---|
| `gTileset_ArkadiaHeights` | Route 11 (the Krathis Gorge), Styx Falls, Route 12 (the Cypress Road) |
| `gTileset_MaiaCave` | the Cave of Maia |

**This catalog is generated** by `tools/ichor/art/heights_build.py` (painters:
`heights_ground.py`, `_trees.py`, `_props.py`, `_cave.py`; palettes in `heights_lib.py`,
which reuses kithairon_lib's soft-shape engine and Kithairon's fir painters). The
render-and-critique passes at the end are written by hand and kept across rebuilds.

## How it fits together

**One set for the climb.** Route 11, Styx Falls and Route 12 share
`gTileset_ArkadiaHeights`, so their seams need no aethos-only strip. Route 11's seam
with Aigion (the `kirrha` set) and Route 12's with Arkadia (`arkadia`) are drawn in
aethos pieces: `tools/ichor/maps/heights.py` keeps the six rows at each of those seams
to aethos metatiles and fails the build otherwise.

**Place pieces by key and cell name** from `build/heights/<dir>/catalog.json`, never by
raw id (`tools/ichor/maps/heights.py` does). Ids below are the current build's.

**Soft ground.** `tall`, `meadow_tall`, `path`, `rock`, `black`, `water`, `blackpool`,
`gravel` and the cave's `cwall` hold one piece per blob shape key: `1|` then the cell's
neighbors N NE E SE S SW W NW, `1` in the region and `0` not, a diagonal counting only
when both its sides are in. The map builder lists the keys its maps use in
`tools/ichor/art/heights_shapes.json` (`heights.py --shapes`), and only those are drawn.

**Cliffs with height.** Batch 1's crags showed a 14 px face on a one-row rise, and
Mt. Kithairon read flat. Here a cliff is two things: `rock` (or grass, or firs) on top,
and a band of `face` cells below it, one to four rows tall. A face cell's shape key is
`<lip><foot><west><east><variant>`: lip `g` (grass above), `r` (rock above) or `-` (more
face above), `f` on the band's bottom row (the dark foot and its fallen blocks), `w`/`e`
where a side is open to the ground, and one of three facet variants so a long band doesn't
repeat. A rock top with nothing of the rock south of it still shows its own short face, so
low crags work as before. `black`/`bface` are the same for the Styx's black rock.

**Climbing south.** Route 11 climbs south from Aigion, so its terraces' edges face north,
away from the camera. They are drawn as rims seen from above (`terraces`: a crevice,
then a lip of stones), and the ledges on them jump north (MB_JUMP_NORTH), so the way back
to Aigion is a quick hop. The faces the camera does see are on the side ravines, the
buttresses and the black cliff.

**Walk codes** in the grids: `X` blocks, `.` walkable, `T` walkable and drawn over the
player, `G` tall grass, `J` a ledge, `D` a door (MB_NON_ANIMATED_DOOR: put the warp there).

**Borrowed ground.** Cells marked *grass*, *path*, *sea*, *tall*, *shade* or *fall* draw
no ground of their own: the build points their bottom tiles at aethos's grass (`0x001`),
road (`0x1D9`), animated sea (`0x170`), tall grass (`0x00D`), deep shade (`0x01C`) or
animated waterfall (`0x0B3`). The white water's foam rides over the moving sea, and the
Styx's thread is aethos's waterfall seen through a slit in the black cliff. Rebuild these
sets whenever aethos is repainted.

**Palettes.** Seven groups, one per secondary palette; every 8x8 tile draws from one.

| Group | Use |
|---|---|
| field | tall barley grass, the road (agros's painters) |
| meadow | Kyllene's combed grass and its flowers |
| rock | the gorge's limestone, faces, rims, ledges, ravines, Nonakris's houses, boulders, the herm, the nest |
| black | the Styx's black rock and cliff, the black pool and its obols, the white thread |
| tree | firs, kermes oak, cypresses (Kithairon's group, so its painters work here) |
| water | white water, the pool's gravel bank, runnels, the spring, the side waterfall's foot |
| stone | the fallen temple's marble and drums, the kiln and its smoke, the shrine of Artemis |

The Cave of Maia has its own three: `cave` (warm brown rock, sand), `relic` (the lyre, the
cloth, the lamp), `altar` (marble and bronze).

**Scripted swaps** (`include/constants/metatile_labels.h`): `METATILE_ArkadiaHeights_DrumWedged`
(drum 2 in the gap, and the hawk spur's drum), `_DrumRest` (drum 3 against the cliff, and the
shepherd's cave drum), `_Gap`, and the shrine's `_Shrine_Top`, `_Shrine_TopR`, `_ShrineBad_Top`,
`_ShrineBad_TopR`.
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
        out.append(f"| `{HB.SETS[name]['symbol']}` | {used} of {HB.TILE_LIMIT} | {metas} of 512 |")
    out.append("")
    for name, (used, metas, secs, ids) in report.items():
        info = HB.SETS[name]
        out.append(f"## `{info['symbol']}`: {info['title']}\n")
        out.append(f"![sheet](img/tiles_{info['dir']}_sheet.png)\n")
        for sec, structs in secs:
            out.append(f"### {HB.SECTION_TITLES[sec]}\n")
            for s in structs:
                st = {"ids": ids[s.key], "walk": s.walk, "w": s.w, "h": s.h}
                out.append(f"#### {s.title}\n")
                out.append(f"`{s.key}`, {s.w} wide by {s.h} tall. {s.notes}\n")
                if s.key in HB.SHAPE_KEYS:
                    out.append(f"{len(s.names)} shapes, from 0x{ids[s.key][0][0]:03X}.\n")
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
    print(DOC.relative_to(HB.ROOT))
