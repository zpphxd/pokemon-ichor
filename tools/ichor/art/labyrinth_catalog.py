#!/usr/bin/env python3
"""Write design/phase4/TILES_labyrinth.md from build/labyrinth/catalog.json.

labyrinth_build.py runs this after a build, so every id in the catalog matches
the compiled tileset.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from emporion_catalog import structure  # noqa: E402

# The rest of the Labyrinth, by section, with the tiles held back for it. The
# workshop is the first part drawn; these are the allowances the later batches
# are budgeted to, so the whole Labyrinth fits one secondary under 504 tiles.
BUDGET = [
    ("house", "The rings' dark corridor kit: wall tops and faces seen from every side, "
              "inner and outer corners, rim-lit edges. Rings reuse the arcade, the slab floor "
              "and the side walls as drawn; a niche is an arcade bay", 24),
    ("house", "The thread twins (§5.1): straights, corners and end caps on the slab's two "
              "halves, 20 metatiles. Run the thread through each cell's upper tile row so a "
              "straight changes two tiles", 30),
    ("rings", "Braziers 2x2 lit and unlit, anchor rings, cracked walls whole and broken, "
              "labrys seals, dial walls A and B, web anchors", 38),
    ("rings", "Skylight pools by day and night, glow-marks (the latent `lg`), sun and moon "
              "gates", 22),
    ("rings", "Mirror bases (four facings) and the 5x5 dancing floor, five symbols lit and "
              "unlit", 22),
    ("rooms", "Ring IV's Titan barracks and mess hall (bunks are the kline, tables the "
              "bench), sickle banners, bronze grates", 14),
    ("rooms", "Ring VI's forge, the archive (its shelves are the workshop's rack with "
              "scrolls) and the vault", 32),
    ("rooms", "Minos's tomb (painted pillars, the bier) and the frescoes that carry clues", 26),
    ("heart", "The Starry Chamber: the lustral pool (its twinkles are tile animations "
              "swapped over base tiles) and the star-clock's ring", 24),
]

PALETTES = [
    ("stone", "Dark stone with thread red", "The masonry of every map (a cool grey limestone "
     "that warms toward the light), the floor's red plaster, Ariadne's thread (three reds), "
     "lamp-warm and dawn-cool light on stone, and the latent glow paint"),
    ("minoan", "Minoan red", "Red columns, ochre, gypsum, black capitals, terracotta (the "
     "Pithos), horns of consecration, labrys seals, Minos's tomb"),
    ("fresco", "Fresco blue", "Blue grounds, dolphins, lilies, saffron, bull-leapers, blue "
     "monkeys, griffins (not drawn yet)"),
    ("bronze", "Bronze and Titan", "The automata, grates, dials, the bell, mirrors, anchor "
     "rings, tools, the collar, the music box; the Titans' slate and gold"),
    ("fire", "Forge fire", "Flames, embers, molten bronze, iron, clay lamps. Its three "
     "bronze shades are bronze's own, so a hand or a lamp's dish can share a tile with its "
     "flame"),
    ("night", "Starry night", "The Starry Chamber, its black lustral pool, moonlit marble "
     "(not drawn yet)"),
    ("timber", "Timber and papyrus", "Benches, drafting tables, plans and their sinopia and "
     "charcoal lines, shelves, the bed and its blue blanket, the lift's deck, scrolls"),
]

INTRO = """\
# Labyrinth tileset: `labyrinth`

`gTileset_Labyrinth` is Daedalus's Labyrinth under Knossa (LABYRINTH.md §11). This first
batch draws **Daedalus's workshop**, the hub at the end of Ring III, for scenes D and L:
"A long vaulted room. Rows of bronze automata stand still. On the bench sits a
half-polished bronze collar. A grate seals a shaft of grey light. A music box ticks."
The rings, the forge, the archive, the tomb and the Starry Chamber come later into the
same tileset; its palettes and sections are planned for all of it now.

![The workshop, scene D](img/labyrinth_scene_workshop.png)

![The workshop at dawn, scene L](img/labyrinth_scene_workshop_dawn.png)

| Image | Shows |
|---|---|
| `img/labyrinth_scene_workshop.png` | The 24 x 18 workshop as scene D stages it, lit and quiet, rendered on `oikos` at 3x |
| `img/labyrinth_scene_workshop_dawn.png` | The same room for scene L: the grate open, grey dawn light down the shaft, the lamps out, the collar gone, with the dawn palette set |
| `img/labyrinth_scene_*_pass1.png`, `_pass2` | The first two render-and-critique passes; the unsuffixed images are the third and final |
| `img/labyrinth_pieces.png` | Every structure as drawn |
| `img/labyrinth_sheet.png` | Every metatile with its id, from the compiled tileset, on `oikos` |

## How it is made

- `tools/ichor/art/labyrinth_art.py` holds the palette plan, the house's masonry (floor,
  arcade, edges) and the sheet's sections; `labyrinth_workshop.py` holds the workshop.
- `tools/ichor/art/labyrinth_build.py` draws it, compiles it with Porytiles in a scratch
  project against an empty stand-in primary, writes the variant palette sets, verifies it
  and rewrites this file. `labyrinth_scene.py` renders the mock scenes.
- Run both with `/usr/bin/python3`.

**Works on any primary.** It uses only its own tiles and palettes 6-12, and every bottom
layer is opaque. It is drawn for `oikos`.

**Layers.** Floors and walls fill the bottom layer; objects stand in the middle layer over
them. Surfaces that carry objects (the bench tops, the shelving, the lift's deck) fill the
bottom layer so the objects on them can be in another palette. Nothing is drawn over
sprites.

**Floor parity.** The floor's gypsum slabs are two cells long, laid in a running bond:
`floor` `slab_l` goes where x + y is even and `slab_r` where it is odd. So every piece that
stands on the floor comes as **twins**: `<key>` for a top-left cell where x + y is even, and
`<key>_odd` where it is odd. The twins share every object tile and differ only in the floor
under them; pick by parity, or the slabs under the piece won't line up. Where only some rows
of a piece show floor (a bench's front, not its top), `<key>_odd` holds just those rows and
`<key>`'s other rows serve both parities; the catalog says which rows. The runner covers
the floor whole and needs no twin; the dawn light under the Icarus Shaft comes in one
parity, the shaft's own.

**Collision and behaviors.** The walk grids below give the collision to paint (`X` blocks,
`.` passes, `D` is a door). `MB_NON_ANIMATED_DOOR` is on the back door, `MB_SOUTH_ARROW_WARP`
on the threshold, `MB_PC` on the Pithos's bottom row; every other metatile is `MB_NORMAL`.
The heal bed, the music box, the lift and the grate are scripts.

## Palettes

LABYRINTH.md §11 plans seven palettes. Six are slots. The seventh, **glow**, is a palette
*variant*: SYSTEMS.md §2 says each dark tileset needs "one extra palette set" for the doused
torch, loaded over 6-12, as the Temple of Demeter's is. That frees the seventh slot, which
this plan gives to **timber and papyrus**: the workshop's furniture, and later the archive's
shelves and the Titans' tables and bunks, which none of the six covers. Every 8x8 tile draws
from one group (`labyrinth_art.GROUPS`), all colors multiples of 8.

| Group | §11 name | For |
|---|---|---|
{palette_rows}

**Variant sets** (in `porytiles_bin/`, written by the build; load over palettes 6-12):

| Set | When | What it does |
|---|---|---|
| `glow/` | The torch doused (SYSTEMS.md §2) | Black but for the glow paint (a latent color that by torchlight is the dark stone it is painted on), the flames, and Ariadne's thread, faint: Ring III's "your own thread shows faintly when doused". No glow-marks are drawn yet; the color is reserved in `stone`. |
| `dawn/` | Scene L, the workshop's dawn | Every color dimmed and cooled toward a grey morning but the dawn light (`ld0`, `ld1`) and the first light at the top of the shaft (`lw1`), which stay as drawn: the room goes dim and blue and the open shaft blazes. The map's scene-L state loads it in `ON_LOAD` (one `LoadPalette` over 6-12, as for the glow set); nothing is wired yet. |

## Tile budget

**{tiles} of 504 tiles are used** by this batch (the door animations own 504-511, and the
build fails past 504). **{left} are left** for the rest of the Labyrinth. The later batches
are budgeted to these allowances, which sum to {planned}, leaving {spare} spare:

| Section | For | Tiles |
|---|---|---|
{budget_rows}
| | **Total for the rest** | **{planned}** |

How the workshop keeps to its share:
- The floor is one slab two cells long: a handful of tiles for the whole floor, and every
  floor piece's twin costs no tiles at all.
- Patterns that repeat (the grate's bars, the shaft's light, the shelving, the runner's
  border, the bench planks) repeat on the 8 px tile grid, so each row is one tile, and the
  Icarus Shaft, the Pithos and the runner are mirror-symmetric about a tile edge.
- The arcade's arches are symmetric about the middle of the bay, so the right half is the
  left half flipped and stored once; every bay shares one arch.
- Benches are a top and a front that repeat; the items on them are overlays.
- Any tile within two pixels of another is redrawn as that tile.

**Metatiles.** A secondary holds 512. This batch draws {metatiles}, packed first-fit into the
sheet's house rows (0-12) and workshop rows (13-35); the rings are held rows 36-49, the
rooms 50-58 and the heart 59-63.

If the rest of the Labyrinth outgrows its allowance, split it as Emporion and Isthmos
were split: keep the rings and the workshop here and move the Titan rooms and the Starry
Chamber to a sister tileset sharing `labyrinth_art`'s house kit.

## Weak spots and open questions

- **No Daedalus sprite yet**, so both scenes stage around his absence: in scene D he would
  stand behind his bench, in scene L by the shaft.
- **The dawn depends on the `dawn/` set.** Without it the open shaft is pale light on a
  lit room and much less of an event. world-act3 has to load it for scene L.
- **The floor's running bond** still reads a little like brickwork where the floor is bare;
  the runner and the furniture carry the room.
- **The open shaft's light** falls in even streaks; a true falloff down the shaft would cost
  another eight or so tiles.
- **Small things at 1x**: the music box and the plans' drawings are only a few pixels at the
  game's real size, so their object text carries them. The Labyrinth plan reads more as
  rings than as a maze.
- **No pools of lamplight** on the floor: warm halos round the lamp-bearers cost about
  twenty tiles a parity, which the budget can't spare.
- **The budget is tight.** The rest of the Labyrinth's allowance leaves only a few tiles
  spare; the sister-tileset fallback above is the release valve.
- **The seventh slot.** This plan reads §11's "glow, a palette variant" as a variant set and
  spends the seventh slot on timber and papyrus. If the creative director wanted glow as a
  slot, timber has to fold into bronze, which costs the furniture its own browns.

## Scenes D and L, piece by piece

| The scene needs | Pieces |
|---|---|
| A long vaulted room | `arcade` (piers, three-cell bays, the back door's pier, the side walls), `arch4`, `floor`, `edge` |
| Rows of bronze automata, standing still | `auto_kore`, `auto_kouros`, `auto_open`, and the empty plinths `plinth_three`, `plinth_seven`, `plinth_nine`; every automaton tied to its plinth at the ankles |
| "Don't touch Number Four. She bites." | `auto_hound`, IIII on her plinth (Attic numerals) |
| A half-polished bronze collar on the bench | `bench` (`collar_l`, `collar_r`), with Perdix's saw and a mallet; `bench_parts` for the cloth left where the collar lay (scene L), a vise holding a bronze hand, plain tops and fronts for benches of any length |
| A grate seals a shaft of grey light | `shaft`, shut |
| Scene L: the grate open, grey dawn light down the shaft | `shaft`, open, and `light_spill` on the floor below; `auto_lamp_cold` and `pier_cold` for the burned-out lamps; the `dawn/` palette set |
| A music box ticks | `music_box`: the prototype of Elpis's box, on a bronze tripod |
| The heal bed, the Pithos | `kline`; `pithos` (`MB_PC` on its bottom row) |
| The lift that opens after scene D | `lift` (the platform's cell is walkable), and `lift_deck`, the empty shaft, to swap into its platform cell while it is away |
| Drafting tables; plans pinned up: the Wings, the Labyrinth's rings | `drafting` (the collar's design, a fresh sheet), `bay_wings`, `bay_plan` |
| The way in from the front, Ring III's web maze | `edge`'s threshold, and `runner` from it to the bench |
| Shelves of parts, lamps, the back door | `bay_shelves` (with Perdix's bronze partridge), `auto_lamp` and the sconces, the door in `arcade`'s `door_pier` |
"""


def main(tiles_used=None, structs=None):
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import labyrinth_art as A
    cat = ROOT / "build/labyrinth/catalog.json"
    doc = ROOT / "design/phase4/TILES_labyrinth.md"
    data = json.loads(cat.read_text())
    if tiles_used is None:
        from emporion_catalog import tiles_used as count
        tiles_used = count("labyrinth")
    planned = sum(n for _, _, n in BUDGET)
    left = 504 - tiles_used
    group_name = {g: (name, use) for g, name, use in PALETTES}
    palette_rows = "\n".join(f"| {g} | {group_name[g][0]} | {group_name[g][1]} |"
                             for g in A.GROUPS)
    budget_rows = "\n".join(f"| {sec} | {what} | {n} |" for sec, what, n in BUDGET)
    metatiles = sum(len(s["ids"]) * len(s["ids"][0]) for s in data)
    out = [INTRO.format(tiles=tiles_used, left=left, planned=planned, spare=left - planned,
                        metatiles=metatiles,
                        palette_rows=palette_rows, budget_rows=budget_rows)]
    out.append("## Catalog\n")
    out.append("Each grid lists metatile ids as Porymap shows them, with the collision beside "
               "it. Each section starts on a fixed row of the sheet, so adding to one never "
               "renumbers another: " + ", ".join(
                   f"{key} at 0x{0x200 + row * 8:03X}" for row, key, *_ in A.SECTIONS) + "; "
               "reserved: " + ", ".join(f"{key} at 0x{0x200 + row * 8:03X}"
                                        for row, key, _ in A.RESERVED) + ". "
               "`build/labyrinth/catalog.json` names every part (`names`), so a map builder "
               "can place pieces by key and name, never by raw id. Odd twins are listed with "
               "their even twin.\n")
    by_key = {s["key"]: s for s in data}
    by_sec = {}
    for s in data:
        by_sec.setdefault(s["section"], []).append(s)
    for row, key, title, blurb in A.SECTIONS:
        out.append(f"### {title}\n\n{blurb}\n")
        for s in by_sec.get(key, []):
            if s["key"].endswith("_odd"):
                twin, r0 = s.get("twin_of") or [s["key"][:-4], 0]
                rows = ("" if s["h"] == len(by_key[twin]["ids"]) else
                        f" of row{'s' if s['h'] > 1 else ''} "
                        + "-".join(str(r) for r in sorted({r0, r0 + s["h"] - 1})))
                out.append(f"`{s['key']}`: the odd twin{rows}, ids "
                           + "; ".join(" ".join(f"0x{v:03X}" for v in r) for r in s["ids"])
                           + ".\n")
                continue
            block = structure(s)
            block[0] = block[0].replace("### ", "#### ")
            out += block
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("\n".join(out).rstrip() + "\n")
    print(doc)


if __name__ == "__main__":
    main()
