#!/usr/bin/env python3
"""Write design/phase2/TILES_temple_demeter.md from build/temple_demeter/catalog.json.

temple_demeter_build.py runs this after a build, so the ids always match the
compiled tileset.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/temple_demeter/catalog.json"
DOC = ROOT / "design/phase2/TILES_temple_demeter.md"

INTRO = """\
# Temple of Demeter tileset: `temple_demeter`

`gTileset_TempleDemeter` is the Temple of Demeter's interior at Eleusa: an underground
megaron modelled on the Telesterion, where Hierophant Chloe the Mystagogue keeps the
Lesser Mysteries (SYSTEMS.md §12, Laurel 3). A forest of columns in near-darkness, lit by
torches; rock-cut tiers along the walls; the Descent of Persephone painted round the
frieze; tripod braziers and wall torches, cold and lit; the Anaktoron with the
Hierophant's throne by its door; kykeon and the baskets of the holy things; the
draughty doorway hung with ribbons; the crypt's stone sentinels; and the wreck the
Titans leave in it (STORY.md §6.2).

**This file is generated** by `tools/ichor/art/temple_demeter_build.py`. The art is in
`temple_demeter_art.py`; the sample rooms in `temple_demeter_scene.py`.

| Image | Shows |
|---|---|
| [`img/temple_demeter_lit.png`](img/temple_demeter_lit.png) | The sample rite, every brazier and torch lit |
| [`img/temple_demeter_dark.png`](img/temple_demeter_dark.png) | The same in the dark: the torch's radius round the player, the vestibule's lit zone |
| [`img/temple_demeter_doused.png`](img/temple_demeter_doused.png) | Doused: the `glow/` palettes, only the seeds, the chalk and the flames |
| [`img/temple_demeter_raid.png`](img/temple_demeter_raid.png) | The robbed Telesterion: overturned braziers, bootprints, one lamp on the steps |
| [`img/temple_demeter_sheet.png`](img/temple_demeter_sheet.png) | The numbered sheet, rendered from the compiled tileset on oikos |
| [`img/temple_demeter_pieces.png`](img/temple_demeter_pieces.png) | Every structure |

![The rite, lit](img/temple_demeter_lit.png)

## How it works

**Primary.** Pair it with `oikos`, the interior primary. Like the Temple of Hestia it uses
only its own tiles (0x200 and up) and palettes 6-12, so it renders the same on any
primary. Every metatile is COVERED: an opaque bottom layer and objects in the middle
layer. Nothing draws over the player.

**Collision.** Walk codes below: `X` blocks (collision 1), `.` walkable, `D`
`MB_NON_ANIMATED_DOOR` (put a warp there), `S` `MB_SOUTH_ARROW_WARP` (the stair out,
like a door mat: the map's bottom row, a warp event on each cell).

**The rite's four verbs, in tiles.**

- **Light.** Every light has a cold and a lit metatile, **the lit one = the cold one + 1**:
  the brazier bowls and legs, the wall sconces, the niche lamps, the column torches, the
  lamp on the steps. Swap both cells of a brazier together and keep them impassable. A lit
  light stands in a pool of warmed floor: swap the `glow` ring in round it (on cells that
  hold plain `floor`) and `floor` back when it goes out, as the Hearth Trial does. A
  season brazier lights a quarter of the hall for good: that is a lit zone (flash level 0,
  SYSTEMS.md §2), and swapping its quarter's sconces to lit makes the change visible.
- **Douse.** Persephone's pomegranate seeds (`floor` `seed`, `seeds`) and Hecate's chalk
  (`chalk_fork`, `chalk_trail_*`, `wall` `lower_chalk`) are painted in two latent colors.
  The build sets those palette entries to the stone they sit on, so by torchlight they are
  invisible. `porytiles_bin/glow/06.pal`-`12.pal` is the doused set: black everywhere,
  except the seeds (pomegranate red), the chalk (a pale violet) and the flames, so lit
  braziers stay landmarks. The engine loads it over palettes 6-12, with flash level 0,
  when the torch is doused, and restores the normal set on relighting.
  `gTilesetPalettes_TempleDemeterGlow` in `src/data/tilesets/graphics.h` is that set,
  ready for the engine (unused until it is wired). The primary's palettes 0-5 should go
  black too.
- **Wind.** `partition` `door_draught` / `door_draught_b`: a doorway in a low wall with
  ribbons streaming through it, both walkable. Alternate the two to make them flutter.
  `floor` `draught` shows dust running toward it.
- **Reveal.** `wall_lights` `door_top_painted` over `door_bottom_painted` is a doorway in
  the fresco; `_open` (+1 each) is the same wall opened, its bottom a door.

**Darkness rules** (SYSTEMS.md §2): the wall top's lip and the side walls carry a rim
light, so the wall line reads inside a 3.5-tile torch radius; give every mandatory
acolyte a lamp or brazier.

**Palettes.** Six color groups (`temple_demeter_art.GROUPS`), one per secondary palette:
`floor` (stone, warmed stone, the seed latent, gilt), `wall` (stone, the fresco, the
chalk latent), `fire` (bronze, flame, ash), `marble` (the dais, throne and altar), `clay`
(vessels, baskets, ribbons) and `warm` (the fresco and stone under firelight). Slot 12 is
free.

**Tile budget.** {used} of 504 tiles are used ({meta} metatiles). The door animations own
tiles 504-511.

**Labels.** The build writes `METATILE_TempleDemeter_*` for everything a script swaps to
the end of `include/constants/metatile_labels.h`: the braziers, the glow ring, the
sconces, niches, column torches, the lamp, the painted door, the altar and the draught
doorway.
"""


def grid(ids, walk):
    lines = []
    for row, wr in zip(ids, walk):
        lines.append(" ".join(f"0x{i:03X}" for i in row) + "   " + " ".join(wr))
    head = "ids".ljust(len(ids[0]) * 6 - 1) + "   walk"
    return "```text\n" + head + "\n" + "\n".join(lines) + "\n```"


def main(used=None):
    data = json.loads(CAT.read_text())["structures"]
    meta = sum(s["w"] * s["h"] for s in data)
    out = [INTRO.format(used=used if used is not None else "?", meta=meta), "## Catalog\n"]
    for s in data:
        out.append(f"### {s['title']}\n")
        out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n")
        out.append(grid(s["ids"], s["walk"]) + "\n")
        if s["names"]:
            parts = ", ".join(f"`{n}` 0x{s['ids'][cy][cx]:03X}" for n, (cx, cy) in s["names"].items())
            out.append(f"Pieces: {parts}.\n")
    out.append(SAMPLE)
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text("\n".join(out))
    print(DOC.relative_to(ROOT))


SAMPLE = """\
## The sample rite (`temple_demeter_scene.py`)

The renders come from one sample layout, 21 x 30, built from the pieces above to show the
kit doing the rite, not to fix the map (the Phase 2 script and geography are still being
written):

- **Teach (the vestibule, south).** The stair down from the temple, one brazier already
  lit (`vestibule`), one seed by the player's feet that only shows doused.
- **Test (the hall).** A forest of columns, tiers along the side walls, four season
  braziers, one in each quarter, each beside a seed; column torches and wall sconces to
  light with each quarter. Two acolytes' spots are marked by lit column torches.
- **Master (the Anaktoron, north).** A partition wall across the hall with the draughty
  doorway, chalk marks that show only doused, and the Anaktoron with the throne beside
  its door; the frieze tells the Descent of Persephone round the walls.

The raid render swaps braziers for `overturned`, scatters `bootprints`, `rubble` and a
`kiste_smashed`, and leaves one `lamp_lit` on the tiers: the robbed Telesterion of
STORY.md §6.2.
"""


if __name__ == "__main__":
    main()
