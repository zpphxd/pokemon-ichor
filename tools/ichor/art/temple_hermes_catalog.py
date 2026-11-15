#!/usr/bin/env python3
"""Write design/phase2/TILES_temple_hermes.md from build/temple_hermes/catalog.json.

emporion_build.py temple_hermes runs this after a build.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from emporion_catalog import structure  # noqa: E402

INTRO = """\
# Temple of Hermes tileset: `temple_hermes`

The interior of Emporion's Temple of Hermes, home of the Herald's Run (SYSTEMS.md §12;
Laurel 2, Hierophant Kerykos the Herald, Flying). It is Ionic, cool and bright: white
marble under a frieze of golden wings on Aegean blue, a racetrack inlaid in red porphyry
and gold across the floor, bronze turnstiles and gates, relay torches, and the herald's
rostrum at the head of the stoa's steps. Hestia's hall is warm and lit by fire; this one
is the open air and the road.

![The Herald's Run, a mock room](img/emporion_scene_temple_interior.png)

| Image | Shows |
|---|---|
| `img/emporion_scene_temple_interior.png` | A mock of the Herald's Run (porch, switchback stoa, upper colonnade, rostrum) at 3x, rendered on `oikos` |
| `img/temple_hermes_pieces.png` | Every structure as drawn |
| `img/temple_hermes_sheet.png` | Every metatile with its id, from the compiled tileset, on `oikos` |

## How it is made

- `tools/ichor/art/temple_hermes.py` holds every pixel and the palette plan.
- `tools/ichor/art/emporion_build.py temple_hermes` draws it, compiles it with Porytiles in a
  scratch project against an empty stand-in primary, verifies it and rewrites this file.

**Works on any primary.** Like the Temple of Hestia, it uses only its own tiles and
palettes 6-12, and every bottom layer is opaque, so the primary's backdrop never shows.
The build checks both. It is drawn for `oikos` and renders the same on any primary.

**Layers.** Floors and walls fill the bottom layer; every object stands in the middle
layer over the floor. Nothing is drawn over sprites: a sprite north of an object never
overlaps it, and one south of it stands in front, which is right.

**Collision and behaviors.** The walk grids below give the collision to paint (`X`
blocks). `MB_COUNTER` is on the lectern and `MB_SOUTH_ARROW_WARP` on the doormat; every
other metatile is `MB_NORMAL`. The turnstiles' one-way rule and the herms' turning are
scripts (a step hook and `setmetatile`, SYSTEMS.md §12); the tiles carry no behavior.

**Palettes.** Every 8x8 tile draws from one of five groups (`temple_hermes.GROUPS`), all
colors multiples of 8:

| Group | For |
|---|---|
| floor | Marble slabs, the porphyry racetrack and its gold, the mosaic |
| marble | Columns, herms (with their oil and laurel), the balustrade, the rostrum, the statue |
| frieze | The walls and the painted frieze |
| bronze | Turnstiles, gates, torches and their fire, the step-glass |
| wood | Pigeonholes, scrolls and their seals, the table, the anointing oil, the doormat |

**Tile budget.** {tiles} of 504 tiles are used (the door animations own 504-511).

## The Herald's Run, piece by piece

| The trial needs (SYSTEMS.md §12) | Pieces |
|---|---|
| Sealed scrolls handed out by Kerykos | `scroll_table` (full and emptied), the scroll basket in `props` |
| Herald-herms to deliver them to | `herm`: heads facing four ways, plain or anointed; shafts plain or holding a delivered scroll |
| "One herm head swivels to point the way once you anoint it (a second use of oil)" | swap a head for its anointed version facing the next herm; the stand of oil in `props` |
| The step-glass | the bronze klepsydra in `props` (the counter itself is UI) |
| Hermes's one-way turnstiles; the upper colonnade's turnstiles reverse | `turnstile` (four directions): swap a turnstile for the opposite one to reverse it |
| A switchback stoa, a side colonnade with a shortcut | `balustrade` (sixteen joins), `column`, the lattice `gate`s |
| The entry porch, the main stoa, the upper colonnade | the floor, the lanes, the rostrum's platform, risers and steps for each level |
| Kerykos on the herald's rostrum at the head of the stoa's steps | `rostrum`: the platform, its roundel and its lectern (`MB_COUNTER`); `column` holds the statue of Hermes to flank him |
| Messenger props: pigeonholes, relay torches, the racetrack | `pigeonholes` (in the wall and as a cabinet), the torches in `props`, `lane` |
"""


def main(tiles_used=None, structs=None):
    cat = ROOT / "build/temple_hermes/catalog.json"
    doc = ROOT / "design/phase2/TILES_temple_hermes.md"
    data = json.loads(cat.read_text())
    if tiles_used is None:
        from emporion_catalog import tiles_used as count
        tiles_used = count("temple_hermes")
    out = [INTRO.format(tiles=tiles_used),
           "## Catalog\n",
           "Each grid lists metatile ids as Porymap shows them, with the collision beside it. "
           "Ids run from 0x200 in the order of `temple_hermes.build()`; add new pieces at the "
           "end so they keep their places. `build/temple_hermes/catalog.json` names every part "
           "(`names`), so a map builder can place them by name.\n"]
    for s in data:
        if not s["key"].startswith("_"):
            out += structure(s)
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("\n".join(out).rstrip() + "\n")
    print(doc)


if __name__ == "__main__":
    main()
