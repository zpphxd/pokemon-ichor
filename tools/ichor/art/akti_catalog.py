#!/usr/bin/env python3
"""Write design/phase1/TILES_akti.md from build/akti/catalog.json.

akti_build.py runs this after a build; run it by hand only to refresh the
document. Every grid comes from the structures themselves, so the ids in the
catalog always match the compiled tileset.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/akti/catalog.json"
DOC = ROOT / "design/phase1/TILES_akti.md"

# (title, blurb, keys) in catalog order
SECTIONS = [
    ("Buildings and monuments", "The Temple of Hestia, Akti's houses, Poseidon's shrine, the "
     "altar and the krene.",
     ["temple_hestia", "house_small", "house_shuttered", "shrine_poseidon", "altar", "krene"]),
    ("The harbor", "The quay and its edges, the trireme Euploia and the kaikia, and the "
     "harbor's goods.",
     ["quay", "quay_steps", "quay_gangplank", "quay_edges", "trireme", "boat_kaiki",
      "boat_kaiki_left", "bollard_line", "rope_coil", "amphora_stack",
      "octopus_line", "fish_stall"]),
    ("The coast", "Limestone crags in the sea and on the shore, the west headland, and the "
     "beach.",
     ["sea_stack", "sea_rocks", "headland", "rocks_sand", "rock_grass", "beach_shells",
      "net_poles", "boat_beached"]),
    ("The town", "The plaza's paving, walls and terraces, and the gardens and yards of the "
     "lower town.",
     ["plaza", "terrace", "laundry", "boat_upturned", "fig_tree",
      "shrubs"]),
]

INTRO = """\
# Akti tileset catalog

The `akti` secondary tileset (`gTileset_Akti`) is Akti Town's harbor. Pair it with
the `aethos` primary, which supplies the open ground: grass, paths, sand, the sea and
the olive and cypress trees. `LAYOUT_AKTI_TOWN` uses aethos + akti; Elaia and Route 1
keep kalliste.

**This file is generated.** `tools/ichor/art/akti_build.py` draws the tileset, compiles
it and rewrites this catalog. The art is in `akti_art.py` (copies from kalliste, the
trireme, the plaza paving), `akti_harbor.py`, `akti_coast.py` and `akti_town.py`; the
palette plan and the borrowed-ground mechanism are in `akti_lib.py`.

![Every Akti structure on its ground](img/akti_pieces.png)

## How to use it

**IDs.** Each grid below lists metatile ids as Porymap shows them, row by row. Ids run
from 0x200 in the order of `akti_art.build()`, so append new structures at its end to
keep the existing ids. `tools/ichor/maps/akti.py` places structures by key from
`build/akti/catalog.json`, never by raw id.

**Collision and layers.** The walk grid beside each structure gives what to set on
each cell:

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `D` | Door: put the warp here. The behavior is `MB_NON_ANIMATED_DOOR`. |
| `T` | Passable, and drawn over the player, who walks beneath it. |
| `-` | Empty cell; don't place it. |

**Borrowed ground.** Cells marked *grass*, *sand* or *sea* below don't draw their own
ground. After Porytiles compiles, the build points their bottom-layer tiles at aethos's
own ground metatile: grass `0x001`, sand `0x124` or sea `0x170`. So:
- they meet the meadow, the beach or the sea around them seamlessly;
- every boat, rock and crag in the water sits on aethos's animated sea;
- they cost no Akti tiles.

These cells reference aethos's tiles by index. **Rebuild Akti whenever aethos is
repainted.** The build checks every borrowed entry against aethos's current
metatiles.

Objects that need a shadow on the grass (the fig, the upturned boat, the shrubs,
the rocks in the grass) draw aethos's grass themselves, copied pixel
for pixel, so they still match.

**Self-contained art.** Apart from the borrowed ground, Akti is compiled against an
empty stand-in primary in a scratch Porytiles project under `build/`. Its metatiles use
only Akti's own tiles (0x200 and up) and palettes 6-12. The build verifies this.

**Palettes.** Every 8x8 tile draws from one of seven color groups, one per secondary
palette (`akti_lib.GROUPS`):

| Group | Use |
|---|---|
| Cycladic | Whitewash, Aegean blue, terracotta pots, basil; the laundry |
| Marble | The temple, the altar and the krene, with bronze, fire and roof terracotta |
| Stone | The quay, walls and terraces, and every crag, with its foam and weed |
| Wood | The trireme, the kaikia, the upturned boat, nets and rope |
| Market | Amphorae, baskets, the catch, octopus and the stall's awning |
| Plaza | The plaza's warm limestone and marble, and the krene's water |
| Grove | Aethos's meadow greens and olives, the fig and the shrubs |

**Tile budget.** {tiles} of the 512 secondary tiles are used.
"""


def grid(ids):
    return [" ".join(f"0x{v:03X}" for v in r) for r in ids]


def main(tiles_used=None):
    data = {s["key"]: s for s in json.loads(CAT.read_text())}
    out = [INTRO.format(tiles=tiles_used if tiles_used is not None else "About 500")]
    listed = set()
    for title, blurb, keys in SECTIONS:
        out.append(f"## {title}\n\n{blurb}\n")
        for k in keys:
            s = data.get(k)
            if not s:
                continue
            listed.add(k)
            out.append(f"### {s['title']}\n")
            out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n")
            rows = grid(s["ids"])
            out.append("```text")
            out.append("ids".ljust(len(rows[0])) + "   walk")
            for r, w in zip(rows, s["walk"]):
                out.append(r + "   " + " ".join(w))
            out.append("```\n")
            ground = s.get("ground", {})
            if ground:
                kinds = sorted(set(ground.values()))
                if len(ground) == s["w"] * s["h"] and len(kinds) == 1:
                    out.append(f"Ground: all on aethos {kinds[0]}.\n")
                else:
                    parts = []
                    for kind in kinds:
                        cells = sorted(c for c, g in ground.items() if g == kind)
                        parts.append(f"{kind} at " + ", ".join(f"({c})" for c in cells))
                    out.append("Ground: " + "; ".join(parts) + ".\n")
            doors = [f"0x{s['ids'][int(c.split(',')[1])][int(c.split(',')[0])]:03X}"
                     for c, mb in s["behaviors"].items() if mb == "MB_NON_ANIMATED_DOOR"]
            if doors:
                out.append(f"Door metatile: {', '.join(doors)}.\n")
    missing = set(data) - listed
    assert not missing, f"akti_catalog: no section lists {sorted(missing)}"
    DOC.write_text("\n".join(out).rstrip() + "\n")
    print(DOC)


if __name__ == "__main__":
    main()
