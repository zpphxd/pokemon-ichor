"""Write design/phase3/TILES_kopais.md: gTileset_Kopais's tile catalog.

The catalog part is generated from the build (kopais_build.py calls main).
Everything from the heading "## Render-and-critique passes" on is written by
hand and kept as it is on every rebuild.
"""
from __future__ import annotations

import kopais_build as KB

DOC = KB.ROOT / "design/phase3/TILES_kopais.md"
KEEP = "## Render-and-critique passes"
SOFT = ("reeds", "marsh", "lake", "mud", "path", "barley", "crag")

HEAD = """# The Kopais shore's tileset

Route 8 runs west from Thyrsa along the south shore of Lake Kopais: open water, a
broad band of reed beds, the road, and the grey foot of Mount Phikion. One secondary on
the `aethos` primary, `gTileset_Kopais`.

**This catalog is generated** by `tools/ichor/art/kopais_build.py` (painters:
`kopais_marsh.py`, `kopais_stone.py`, `kopais_gear.py`; palettes, class keys and phases
in `kopais_lib.py`). The render-and-critique passes at the end are written by hand and
kept across rebuilds.

## How it fits together

**Place pieces by key and cell name** from `build/kopais/catalog.json`, never by raw id
(`tools/ichor/maps/kopais.py` does). Ids below are the current build's.

**Soft ground with class keys.** `reeds`, `marsh`, `lake`, `mud`, `path`, `barley` and
`crag` hold one piece per key the map uses: `1|` then the class of each neighbor N NE E
SE S SW W NW (`1` the same ground, `g` grass and anything dry, `w` marsh water, `m` mud,
`r` reeds, `L` the lake, `s` stonework standing in the water). The visible shape comes
from the binary key; every pixel outside it is painted as whatever the neighbor it lies
in is, so a reed bed fades into water on one side and stops at grass on another. Each
set decides which classes count as its own ground: the marsh counts reeds, the lake and
stonework as water (their own pieces draw the meeting); mud counts water and reeds as
mud. `tools/ichor/maps/kopais.py --shapes` lists the keys in
`tools/ichor/art/kopais_shapes.json`, and only those are drawn.

- `reeds` are the marsh's tall grass: **MB_LONG_GRASS**, so they hold encounters and the
  long-grass field effect (cut from aethos's reeds) parts round the player. They are
  taller than meadow grass: stems run the whole tile and their heads scatter.
- `marsh` is shallow, murky water, `lake` the open lake on aethos's animated water: both
  MB_POND_WATER (the Conch surfs them, rods fish them).
- `crag` is Phikion's grey limestone, Kithairon's painter, so the two mountains match.

**The tile animation.** Every animated piece (the reeds, the marsh water and the lake's
rim, and the gear standing in them, and the eel-smoker's fire) is painted for four
phases: the reeds lean east, rest, lean west; the water's ripples and glints drift. The
build finds the tiles each animated cell compiled to and writes their frames
(`data/tilesets/secondary/kopais/anim/`, indexed PNGs that `make` turns into `.4bpp`) and
`src/data/tilesets/kopais_anims.h`, which `src/tileset_anims.c` includes. The tileset's
callback is `InitTilesetAnim_Kopais`. A phase lasts 24 frames.

**Walk codes** in the grids: `X` blocks, `.` walkable, `T` walkable and drawn over the
player, `G` grass (MB_LONG_GRASS in `reeds`, MB_TALL_GRASS in `barley`).

**Borrowed ground.** Cells marked *grass*, *path* or *sea* draw no ground of their own:
the build points their bottom tiles at aethos's grass (`0x001`), road (`0x1D9`) or
animated sea (`0x170`). The dike's road, the Treasury's floor and the lake's interior
cost no tiles that way. Rebuild this set whenever aethos is repainted.

**Palettes.** Seven groups, one per secondary palette; every 8x8 tile draws from one.

| Group | Use |
|---|---|
| reed | reed beds on dry ground: reeds, cattails, grass, mud at their feet |
| reedw | reed beds standing in water |
| marsh | marsh water, mud banks, mudflats, lily pads, the lake's rim |
| field | the road, barley on the spur, turned earth |
| rock | Phikion's rock, scrub, the ledges, the Sphinx's ledge and its feathers |
| stone | the dike, the sluice, the Treasury, Gla's wall, the herm, the racing post |
| gear | the hide, nets, eel traps, the smoking rack and fire, the reed boat, the jetty |
"""


def grid_block(ids, s):
    lines = []
    for y in range(s.h):
        row = " ".join(f"0x{ids[y][x]:03X}" for x in range(s.w))
        lines.append(f"{row}   {' '.join(s.walk[y])}")
    return "```text\n" + "\n".join(lines) + "\n```"


def main(used, metas, secs, ids, moving, nruns):
    out = [HEAD]
    out.append("## Budget\n")
    out.append("| Tileset | Tiles | Metatiles | Animated tiles |")
    out.append("|---|---|---|---|")
    out.append(f"| `{KB.SYMBOL}` | {used} of {KB.TILE_LIMIT} | {metas} of 512 | {moving}, "
               f"in {nruns} runs |")
    out.append("")
    out.append(f"## `{KB.SYMBOL}`: {KB.TITLE}\n")
    out.append("![sheet](img/tiles_kopais_sheet.png)\n")
    for sec, structs in secs:
        out.append(f"### {KB.SECTION_TITLES[sec]}\n")
        for s in structs:
            g = ids[s.key]
            out.append(f"#### {s.title}\n")
            out.append(f"`{s.key}`, {s.w} wide by {s.h} tall. {s.notes}\n")
            if s.key in SOFT:
                out.append(f"{len(s.names)} shapes, from 0x{g[0][0]:03X}; the interior "
                           f"`1|11111111` is 0x{g[0][0]:03X}.\n")
                continue
            out.append(grid_block(g, s) + "\n")
            if s.names and not all("," in n for n in s.names):
                named = ", ".join(f"`{n}` 0x{g[c[1]][c[0]]:03X}" for n, c in s.names.items())
                out.append(f"Pieces: {named}.\n")
            gr = getattr(s, "ground", {})
            if gr:
                kinds = sorted(set(gr.values()))
                out.append("Borrowed ground: " + "; ".join(
                    f"{k} at " + ", ".join(f"{x},{y}" for (x, y), v in sorted(gr.items()) if v == k)
                    for k in kinds) + ".\n")
    text = "\n".join(out) + "\n"
    old = DOC.read_text() if DOC.exists() else ""
    if KEEP in old:
        text += old[old.index(KEEP):]
    else:
        text += KEEP + "\n\n(Written by hand; see the passes below.)\n"
    DOC.write_text(text)
    print(DOC.relative_to(KB.ROOT))
