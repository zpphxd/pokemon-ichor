"""Write the generated part of design/phase3/TILES_trophonios.md.

trophonios_build.py calls main(). Everything from the heading
"## The maps" on is written by hand and kept as it is on every rebuild.
"""
from __future__ import annotations

import trophonios_build as TB

DOC = TB.ROOT / "design/phase3/TILES_trophonios.md"
KEEP = "## The maps"

HEAD = """# Trophonios's cave: the tileset and the maps

The oracle's cave under Lebadeia's precinct (SCRIPT.md Part 5, beats 35B-35C): the
priests' paved chamber inside the bronze grille with the throne of Mnemosyne, a rope
ladder into the dark, the underground Herkyna, the pilgrims' chalk handprints, the
snake's cleft, the black pool that reflects nothing, and the bread-oven hole in the
oracle's floor. One secondary, `gTileset_Trophonios`, on the `aethos` primary, for
`MAP_TROPHONIOS_CAVE_B1F` and `_B2F`.

**Generated.** The catalog below is written by `tools/ichor/art/trophonios_build.py`
(painters: `trophonios_kit.py`, `trophonios_props.py`; palettes and helpers in
`trophonios_lib.py`). The maps' part, from "The maps" on, is written by hand and kept
across rebuilds.

```bash
/usr/bin/python3 tools/ichor/maps/trophonios.py --shapes   # list the wall and water shapes the maps use
/usr/bin/python3 tools/ichor/art/trophonios_build.py       # paint, compile, verify, catalog
/usr/bin/python3 tools/ichor/maps/trophonios.py            # build both floors, render them
```

## How it fits together

**Where it started.** Batch 1's `gTileset_KithaironCave` (Antiope's cave) was the
model: the crag rock turned into cave walls on a floor, and the bronze brazier. Its
walls read flat (one grey for rock and floor, a 14 px face), so this set redraws them:
a near-black umber **cap** for the rock seen from above, and a warm ochre limestone
**face**, two or three cells tall, along every south edge, so each wall reads as a wall
with height. The floor is a cooler grey-brown clay, darker than the face and lighter
than the cap, so walkable and blocked never blur.

**Self-contained.** Like `gTileset_KithaironCave`, the set is compiled against an empty
stand-in primary and draws only its own tiles and palettes 6-12, so it works on any
primary. Outside the torch's circle the GBA shows black whatever the primary.

**Layers.** Walls' ends, props and furniture stand in the middle layer over the plain
floor's bottom tiles, so the floor is stored once and every 8x8 tile keeps to one palette
group. Full-width faces and the cap's interior are bottom-layer only.

**Walls are auto-tiled** by `tools/ichor/maps/trophonios.py` from a grid of rock and
floor: every rock cell above a floor cell is the face's base, the cells above it are the
face's upper rows (two tall under the cap; three where the upper chamber's cliff drops to
the cave), and the rest is the cap, picked by blob shape key. Place other pieces by key
and cell name from `build/trophonios/catalog.json`, never by raw id.

**Palettes.** Six groups, one per secondary palette; every 8x8 tile draws from one.

| Group | Use |
|---|---|
| rock | the cap, the face, chalk prints and seeps on the face, stalagmites |
| floor | the clay floor, damp, contact shadows, chalk on the floor, the priests' paving, the stairs down, the oracle's hole |
| water | the underground Herkyna and its banks and ford, the spring, the outlet and sink, the black pool |
| fire | bronze braziers and their flames, the lamps, the bread offerings and honey cakes |
| stone | the throne of Mnemosyne, the grille and its daylight, the rope ladder, the votive tablets |
| life | the snake's coils, cobwebs, old bones |

**The glow copy** (SYSTEMS.md section 2). The chalk is two colors, `ch1` and `ch2`, in
the rock and floor palettes: faint grey-white on the rock in torchlight. The build writes
`data/tilesets/secondary/trophonios/glow/00.pal`-`15.pal`, a copy of the set's palettes
with every color black except the chalk, which glows green (as Phase 2's Hecate's chalk).
The engine doesn't load a glow copy on douse yet (ENGINE_API section 2: doused is "black:
glow-paint only, once its palettes exist"), so it isn't registered in
`src/data/tilesets/graphics.h`; until it is, the chalk is read by torchlight and by its
signs (below).

**Scripted swaps** (`include/constants/metatile_labels.h`): `METATILE_Trophonios_Brazier_ColdTop`,
`_Cold`, `_LitTop`, `_Lit`; `METATILE_Trophonios_Cleft_Coils`, `_Cleft_Empty`.
"""


def grid_block(st, ids):
    lines = []
    for y in range(st.h):
        row = " ".join(f"0x{ids[y][x]:03X}" for x in range(st.w))
        lines.append(f"{row}   {' '.join(st.walk[y])}")
    return "```text\n" + "\n".join(lines) + "\n```"


def main(used, metas, secs, ids, glow):
    out = [HEAD]
    out.append("## Budget\n")
    out.append(f"`{TB.SYMBOL}`: **{used} of {TB.TILE_LIMIT} tiles**, {metas} of 512 metatiles. "
               f"The chalk sits at palette slots {sorted(set(glow))} (palette, index).\n")
    out.append("![sheet](img/tiles_trophonios_sheet.png)\n")
    for sec, structs in secs:
        out.append(f"## {TB.SECTION_TITLES[sec]}\n")
        for s in structs:
            out.append(f"### {s.title}\n")
            out.append(f"`{s.key}`, {s.w} wide by {s.h} tall. {s.notes}\n")
            if s.key in ("cap", "face", "water"):
                out.append(f"{len(s.names)} shapes, from 0x{ids[s.key][0][0]:03X}.\n")
                continue
            out.append(grid_block(s, ids[s.key]) + "\n")
            if s.names:
                named = ", ".join(f"`{n}` 0x{ids[s.key][c[1]][c[0]]:03X}" for n, c in s.names.items())
                out.append(f"Pieces: {named}.\n")
    text = "\n".join(out) + "\n"
    old = DOC.read_text() if DOC.exists() else ""
    if KEEP in old:
        text += old[old.index(KEEP):]
    else:
        text += KEEP + "\n\n(Written by hand: see each floor below.)\n"
    DOC.write_text(text)
    print(DOC.relative_to(TB.ROOT))
