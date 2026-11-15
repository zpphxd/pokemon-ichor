"""Write design/oikoumene/TILES_pontos.md from the built structures.

pontos_build.py runs this after a build, so every id in the catalog matches the
compiled tileset.
"""
from __future__ import annotations

from pathlib import Path

import pontos_art
import pontos_lib as P

ROOT = P.ROOT
DOC = ROOT / "design/oikoumene/TILES_pontos.md"

INTRO = """\
# Pontos tileset catalog

`gTileset_Pontos` is the Black Sea's outdoor secondary (OIKOUMENE.md §4.3 and §7): a dark
green sea under low cloud, white chalk cliffs, the blue-black Clashing Rocks, Thracian
Salmydessos in wattle and thatch, Colchian Aia in log towers, and Aietes's bronze palace
with Hephaestus's four fountains. Pair it with the `aethos` primary, which supplies grass,
tall grass, paths, sand, olives, pines, steles, herms, the Asclepeion and the Agora.

**This file is generated.** `/usr/bin/python3 tools/ichor/art/pontos_build.py` draws the
tileset, compiles it and rewrites this catalog. The art is in `pontos_coast.py` (the coast
autotiles), `pontos_props.py` (sea, rocks, landmarks, the Isle of Ares, flora) and
`pontos_town.py` (houses, the palace, the fountains, harbors); the palette plan and the
ground mechanism are in `pontos_lib.py`.

![Every Pontos structure on its ground](img/pontos_pieces.png)

The numbered sheet is [img/pontos_sheet.png](img/pontos_sheet.png).

## The palettes

| Slot | Group | Holds |
|---|---|---|
| 6-11 | chalk, kyanean, bronze, timber, flora, accent | Packed by Porytiles from `pontos_lib.GROUPS`; every 8x8 tile draws from one group |
| 12 | the Pontic sea | Not packed. aethos's sea palette (slot 5) with every blue turned dark sea green (`pontos_lib.PONTIC`). Pontos metatiles that point at aethos's water tiles with palette 12 show aethos's animated water in Black Sea colors, for no tiles |

**Borrowed ground.** A cell on `grass`, `sand`, `path`, `tall` or `psea` ground has its
bottom layer pointed at aethos's metatile (0x001, 0x124, 0x1D9, 0x00D, and 0x170 in
palette 12). Rebuild Pontos whenever aethos is repainted.

**The coast autotiles.** Each coast piece is the center of a 3x3 neighbourhood of land (1)
and sea (0), drawn so that neighbours meet exactly. Map builders list the neighbourhoods
they need in `tools/ichor/art/pontos_shapes.json` (`--shapes`), the build draws one piece
per distinct drawing, and `build/pontos/coast_index.json` maps every neighbourhood to its
piece. Plain chalk land is aethos's grass; plain sea is `psea`.

## Budget

{budget}

## Structures
"""


def grid(s):
    rows = []
    for y in range(s.h):
        rows.append(" ".join(f"{s.ids[y][x]:03X}" for x in range(s.w)))
    return "<br>".join(rows)


def main(used, structs, sections):
    budget = (f"{used} of 504 tiles (the door animations own 504-511). Batch 1 fills sheet rows "
              f"0-{max(max(r for r in (s.origin[1] + s.h for s in ss)) for _, ss in sections if ss) - 1}; "
              f"rows {pontos_art.BATCH2_ROW}-63 are batch 2's (the Phasis, the Field of Ares, the "
              f"Grove of Ares, Leuke, the Caucasus caves).")
    out = [INTRO.replace("{budget}", budget)]
    for row, key, title, blurb in pontos_art.SECTIONS:
        out.append(f"\n### {title} (from row {row}, 0x{0x200 + row * 8:03X})\n\n{blurb}\n")
        ss = [s for s in structs if s.section == key]
        if key == "coast":
            counts = {}
            for s in ss:
                counts[s.coast[0]] = counts.get(s.coast[0], 0) + 1
            out.append("Pieces: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) +
                       f"; ids 0x{ss[0].ids[0][0]:03X}-0x{ss[-1].ids[0][0]:03X}.\n" if ss else "None yet.\n")
            continue
        out.append("| Key | What | Size | Ids | Walk |\n|---|---|---|---|---|")
        for s in ss:
            walk = "<br>".join(f"`{r}`" for r in s.walk)
            out.append(f"| `{s.key}` | {s.title} | {s.w}x{s.h} | {grid(s)} | {walk} |")
        out.append("")
    DOC.write_text("\n".join(out) + "\n")
    print(DOC)
