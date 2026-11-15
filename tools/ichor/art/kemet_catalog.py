#!/usr/bin/env python3
"""Write design/oikoumene/TILES_kemet.md from the built structures.

kemet_build.py runs this after a build, so the ids always match the compiled
tileset. Map builders read build/kemet/catalog.json and place pieces by key and
part name, never by raw id.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "design/oikoumene/TILES_kemet.md"

INTRO = """\
# Kemet tileset catalog

`gTileset_Kemet` is Egypt's outdoor secondary: the Nile's delta and valley as the Greeks
of Naukratis saw them (OIKOUMENE.md §4.5 and §7). Pair it with the `aethos` primary, which
supplies the meadow, sand, the animated sea, limestone paths, ledges, rocks, the
Asclepeion and the Agora. Batch 1 builds Naukratis, Pharos, the Delta Reeds and Memphis
with it; batch 2's Pyramid Field, the Great Pyramid's exterior, the Nile, Heliopolis and
Elephantine share it.

**This file is generated.** `tools/ichor/art/kemet_build.py` draws the tileset, compiles it
and rewrites this catalog. The art is in `kemet_ground.py`, `kemet_flora.py`,
`kemet_town.py` and `kemet_monuments.py`; the palette plan, the ground mechanism and the
painters are in `kemet_lib.py`.

![Every Kemet structure on its ground](img/kemet_pieces.png)

The numbered sheet is [img/kemet_sheet.png](img/kemet_sheet.png).

## The palette plan

Seven groups fill the secondary's palettes 6-12. Every 8x8 tile takes all its colors
from one group (`kemet_lib.validate()` enforces it), so Porytiles can always pack them.

| Group | Holds |
|---|---|
| nile | Black mud (wet, dry, cracked), the bank's foam line, aethos's meadow greens for tufts |
| reed | Papyrus stems and umbels, palm fronds and trunks, dates, mud at their feet |
| stone | Tura limestone (walls, quays, obelisks, pyramids), sand, electrum caps |
| paint | Ochre red and yellow, malachite, lapis, skin, on limestone: reliefs, steles, Thoth's pillar, the sphinx's nemes |
| brick | Whitewash over mud brick, bare brick, palm-log beams, dark doorways |
| hellas | Marble, terracotta, Greek blue and red, gilt: the Hellenion |
| goods | Boats, rope, reed bundles, linen, nets, Naukratis pottery |

## Ground

Each cell sits on one of:
- **borrowed aethos ground** (`grass`, `sand`, `sea`, `path`): the build points the cell's
  bottom layer at aethos's own ground metatile, so the sea under a mud bank or a papyrus
  clump keeps aethos's animation and costs no tiles;
- **drawn ground**: `mud` (Kemet's black mud, the same 16 px repeat everywhere) or `quay`
  (limestone ashlar), painted into the bottom layer;
- **none**: the art fills the cell.

Walk codes: `X` solid, `.` walkable, `T` walkable and drawn over the player, `D` a door
(`MB_NON_ANIMATED_DOOR`). Encounter cells (`reeds`, `dune_grass`) are `MB_TALL_GRASS`;
`lotus` is `MB_OCEAN_WATER`.

## How to use it

- **Edges** (`mud_grass`, `bank`, `quay`) are named by `edge_key()` (the slice's map
  builders): `tl` is a region cell with its north and west neighbours outside, `in_nw` a
  cell whose only outside neighbour is the north-west diagonal.
- **Thickets** are regions at least 2x2: `nw n ne / w c e / sw s se` by which sides face
  out (`c2`, `n2`, `s2` for variety), and above every north-edge cell a `fringe_mud`,
  `fringe_mud2` or `fringe_grass`, whose umbels are drawn over the player.
- **Walls**: a top is `top_NSWE` with a 1 for each side the wall continues; south of a top
  with no wall below goes a face, `face_WE`.
- Doors are part `door` of each house; the build sets their behavior.
"""


def grid(s):
    rows = []
    for r in s["ids"]:
        rows.append(" ".join(f"{i:03X}" for i in r))
    return "```\n" + "\n".join(rows) + "\n```\n"


def main(used, structs, sections):
    lines = [INTRO]
    starts = ", ".join(f"{title} at row {row} (0x{0x200 + row * 8:03X})" for row, _, title, _ in sections)
    lines.append(f"\n**Budget.** {used} of 504 tiles. Sections start on fixed rows: {starts}.\n")
    for row, key, title, blurb in sections:
        lines.append(f"\n## {title}\n\n{blurb}\n")
        for s in structs:
            if s.section != key:
                continue
            lines.append(f"\n### `{s.key}`: {s.title} ({s.w}x{s.h})\n")
            if s.notes:
                lines.append(s.notes + "\n")
            names = getattr(s, "names", {})
            if names:
                parts = ", ".join(f"`{n}` {s.ids[y][x]:03X}" for n, (x, y) in names.items())
                lines.append(f"\nParts: {parts}.\n")
            lines.append("\nWalk: `" + " / ".join(s.walk) + "`\n\n")
            lines.append(grid({"ids": s.ids}))
    OUT.write_text("".join(lines))
    print(OUT)
