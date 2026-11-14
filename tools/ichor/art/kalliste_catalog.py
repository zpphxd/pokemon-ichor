#!/usr/bin/env python3
"""Write design/phase1/TILES_kalliste.md from build/kalliste/catalog.json.

kalliste_build.py runs this after a build; run it by hand only to refresh the
document. Every grid comes from the structures themselves, so ids in the
catalog always match the compiled tileset.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/kalliste/catalog.json"
DOC = ROOT / "design/phase1/TILES_kalliste.md"

SECTIONS = [
    ("elaia", "Elaia Village", "Cycladic houses, the blue-domed shrine, the Klotheia square, walls, "
                               "terraces and the olive press."),
    ("akti", "Akti Town", "The Temple of Hestia, the harbor kit and the shrine to Poseidon."),
    ("kronion", "Kronion Hill", "The archaic shrine's ruins and the Titanborn's dig."),
]

INTRO = """\
# Kalliste tileset catalog

The `kalliste` secondary tileset (`gTileset_Kalliste`) holds every Greek structure on
Kalliste Isle. Pair it with the `aethos` primary, which supplies the ground (grass,
paths, sand, the sea and trees).

**This file is generated.** `tools/ichor/art/kalliste_build.py` draws the tileset,
compiles it and rewrites this catalog. The scene render comes from
`tools/ichor/art/kalliste_scene.py`.

![Mock scene: Elaia, Kronion Hill and Akti on aethos ground](img/kalliste_scene.png)

## How to use it

**IDs.**
- Each grid below lists metatile ids as Porymap shows them, row by row.
- Each section starts on a fixed row of the sheet: Elaia at 0x200, Akti at 0x2C0 and
  Kronion at 0x380. Adding to one section never renumbers another, so new pieces
  should be appended to their section.

**Collision and layers.** The walk grid beside each structure gives what to set on
each cell when placing it:

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `D` | Door: put the warp here. The behavior is `MB_NON_ANIMATED_DOOR`, so the warp triggers without a door animation. |
| `T` | Passable, and drawn over the player, who walks behind it. |
| `J` | Ledge: `MB_JUMP_SOUTH`. |
| `-` | Empty cell; don't place it. |

**Ground.**
- Buildings fill their whole footprint, so they sit on any aethos ground.
- Small objects carry their own ground in the bottom layer, because kalliste cannot
  borrow aethos tiles:
  - garland posts and the altar sit on festival paving;
  - nets, amphorae and crates sit on quay paving;
  - columns, drums and the dig sit on stylobate slabs;
  - boats sit on sea.
- Put these on matching ground.
- The sea under the boats copies aethos's deep water (0x170) colors but does not
  animate.

**Self-contained build.**
- kalliste is compiled against an empty stand-in primary, in a scratch Porytiles
  project under `build/`.
- Its metatiles use only kalliste's own tiles (0x200 and up) and palettes 6–12, so
  they keep working whatever aethos becomes. The build verifies this.
- To compile against aethos instead, run `porytiles compile-tileset gTileset_Kalliste`.
  `porytiles/tilesets/gTileset_Kalliste/config.yaml` pairs it with aethos. Porytiles
  may then reuse aethos tiles and palettes, so recompile kalliste whenever aethos
  changes.

**Palettes.** Every 8×8 tile draws from one of seven color groups, one per secondary
palette:

| Group | Use |
|---|---|
| Cycladic | Whitewash, Aegean blue, terracotta pots, basil |
| Marble | Hestia's temple and the festival altar, with hearth bronze, fire and roof terracotta |
| Stone | Limestone walls, terraces, the quay and Kronion's weathered poros |
| Wood | Boats, crates, nets and rope |
| Clay | Amphorae, the Klotheia garlands and the distaff posts |
| Paving | Slate flagstones in white lime |
| Sea | The water under the boats |

**Tile budget.** {tiles} of the 512 secondary tiles are used. The set is nearly full,
so more Kalliste art will need trimming or a second secondary. The harbor kit is the
easiest part to split out.
"""


def grid(ids):
    w = max(len(r) for r in ids)
    lines = []
    for r in ids:
        lines.append(" ".join(f"0x{v:03X}" for v in r))
    return "\n".join(lines)


def main(tiles_used=None):
    data = json.loads(CAT.read_text())
    out = [INTRO.format(tiles=tiles_used if tiles_used is not None else "About 490")]
    for key, title, blurb in SECTIONS:
        out.append(f"## {title}\n\n{blurb}\n")
        for s in data:
            if s["section"] != key:
                continue
            out.append(f"### {s['title']}\n")
            out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n")
            out.append("```text")
            walk = s["walk"]
            idw = len(grid(s["ids"]).split("\n")[0])
            out.append("ids".ljust(idw) + "   walk")
            for row_ids, row_walk in zip(grid(s["ids"]).split("\n"), walk):
                out.append(row_ids + "   " + " ".join(row_walk))
            out.append("```\n")
            doors = [f"0x{s['ids'][int(k.split(',')[1])][int(k.split(',')[0])]:03X}"
                     for k, mb in s["behaviors"].items() if mb == "MB_NON_ANIMATED_DOOR"]
            if doors:
                out.append(f"Door metatile: {', '.join(doors)}.\n")
    DOC.write_text("\n".join(out).rstrip() + "\n")
    print(DOC)


if __name__ == "__main__":
    main()
