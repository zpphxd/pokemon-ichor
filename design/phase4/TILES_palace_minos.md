# palace_minos tileset catalog

`gTileset_PalaceMinos` is the Palace of Minos above ground (Act III, Knossa; LABYRINTH.md §2-§3, §11; SCRIPT.md Part 10). It serves the Palace of Minos (`MAP_KNOSSA_PALACE`). Pair it with the `aethos` primary, which supplies the open grass, paths, sand, sea, olives, cypresses, ledges and the Asclepeion and Agora fronts.

**This file is generated.** `tools/ichor/art/knossa_build.py palace_minos` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/knossa_*.py`, the palette plan in `knossa_lib.py`, what each tileset holds in `knossa_specs.py`; `knossa_scene.py` renders the mock scenes.

| Image | Shows |
|---|---|
| [`img/knossa_palace_court.png`](img/knossa_palace_court.png) | A 240 x 160 screen of the Central Court: the bull-leaping lane and its painted line, the Gentle Bull's pen, the porticoes, the bull-leapers on the east wall (3x; `_1x` is 1x) |
| [`img/knossa_palace_hill.png`](img/knossa_palace_hill.png) | The palace on its hill from the Bull Road's end: the stair up the limestone, the North Entrance and its charging bull, the West Court's kouloura, the Theatral Area |
| [`img/palace_minos_pieces.png`](img/palace_minos_pieces.png) | Every structure on its ground |
| [`img/palace_minos_sheet.png`](img/palace_minos_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

![A 240 x 160 screen of the Central Court: the bull-leaping lane and its painted line, the Gentle Bull's pen, the porticoes, the bull-leapers on the east wall (3x; `_1x` is 1x)](img/knossa_palace_court.png)

It is one of the Knossa family of secondaries; see [`TILES_amnisos.md`](TILES_amnisos.md) for why the art is split and which seams then need aethos-only strips.

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet (court at 0x200, walls at 0x250, fresco at 0x290, land at 0x2A8). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/knossa_tiles.py` holds every Knossa
catalog as a Python dict (`mid('palace_minos', 'paving', 'A', ...)`, `place(...)`, `front(...)`),
and `build/palace_minos/catalog.json` is the same as JSON.

**Walk codes** (the grid beside each structure, and the cell tables):

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `T` | Passable, drawn over the player, who walks behind it. |
| `G` | Tall grass: `MB_TALL_GRASS`, wild encounters. Passable. |
| `D` | Door: `MB_NON_ANIMATED_DOOR`. Put the warp here. |
| `W` | Sea: `MB_OCEAN_WATER`, surfable (collision 0). |
| `P` | Fresh water: `MB_POND_WATER`, surfable. |
| `J` | Ledge: `MB_JUMP_SOUTH`. |
| `^` | Ledge down to the north: `MB_JUMP_NORTH`. |
| `S` | Sand: `MB_SAND`. |

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea* or *shallow* draw no
ground of their own: after Porytiles compiles, the build points their bottom-layer tiles
at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated sea
(`0x170`) or animated turquoise shallows (`0x0D1`). They meet aethos ground exactly and
cost no tiles. Rebuild whenever aethos is repainted; the build checks every borrowed
entry. A borrowed cell's own art is in one layer: the middle (`COVERED`, under the
player) or the top (`SPLIT`, over the player).

**Animations.** None of its own; the borrowed sea and shallows animate.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color
groups, one per secondary palette (`knossa_lib.GROUPS`), passed to Porytiles as packing
hints:

| Group | Use |
|---|---|
| minoan | Minoan red, ochre, gypsum, black and terracotta (labyrinth_art's): red columns, black capitals, horns of consecration, labrys marks, pithoi, the houses, the hives |
| fresco | Fresco blue, white, saffron and skin (labyrinth_art's): dolphins, lilies, bull-leapers, the lily prince, saffron gatherers, blue monkeys, griffins |
| stone | Cretan limestone on aethos grass: cliffs, terrace and town walls, the goat path |
| green | Vines and grapes, holm oak, phrygana and thyme, on aethos grass |
| terra | Kythera's timber and terracotta: boats, the triremes, nets, trellis posts |

**Tile budget.** 330 of 504 tiles (184 metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.

**Scripted swaps.** The build writes the ids scripts swap to the `gTileset_PalaceMinos` block at the end of `include/constants/metatile_labels.h`: `METATILE_PalaceMinos_PenGate`.

## The court

### Court paving and the bull-leaping lane

`paving`, 6 wide by 4 tall. The Central Court's gypsum paving, big slabs set in red plaster (LABYRINTH §3). Lay `A` `B` `C` `D` in a mix, `cracked` and `weeds` (grass in the joints, the palace is a ruin above ground) here and there. Where the paving meets grass it breaks up: `edge_N` (grass to the north) `edge_S` `edge_W` `edge_E` and the outer corners `edge_NW` `edge_NE` `edge_SW` `edge_SE` (on borrowed grass). **The bull-leaping lane** (LABYRINTH §3): nine cells of smoother gypsum edged in painted red, north-south `lane_N`, `lane` x7, `lane_S` (the bull paws at `lane_N`, you stand at `lane_S`), or west-east `lane_W` `lane_h` `lane_E`; `lane_line` / `lane_h_line` is the painted line across it, on the cell in front of you, where you press A as his head crosses. **The Theatral Area**: `dance` and `dance_b`, its worn paving, rings scuffed into the slabs by dancers, the dancing floor's twin. All walkable.

```text
ids                                      walk
0x200 0x201 0x202 0x203 0x204 0x205   . . . . . .
0x208 0x209 0x20A 0x20B 0x20C 0x20D   . . . . . .
0x210 0x211 0x212 0x213 0x214 0x215   . . . . . .
0x218 0x219 0x21A 0x21B 0x21C 0x21D   . . . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x200 | `A` | `.` | `MB_NORMAL` | COVERED |  |
| 0x201 | `B` | `.` | `MB_NORMAL` | COVERED |  |
| 0x202 | `C` | `.` | `MB_NORMAL` | COVERED |  |
| 0x203 | `D` | `.` | `MB_NORMAL` | COVERED |  |
| 0x204 | `cracked` | `.` | `MB_NORMAL` | COVERED |  |
| 0x205 | `weeds` | `.` | `MB_NORMAL` | COVERED |  |
| 0x208 | `edge_N` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x209 | `edge_S` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x20A | `edge_W` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x20B | `edge_E` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x20C | `edge_NW` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x20D | `edge_NE` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x210 | `edge_SW` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x211 | `edge_SE` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x212 | `lane` | `.` | `MB_NORMAL` | COVERED |  |
| 0x213 | `lane_line` | `.` | `MB_NORMAL` | COVERED |  |
| 0x214 | `lane_N` | `.` | `MB_NORMAL` | COVERED |  |
| 0x215 | `lane_S` | `.` | `MB_NORMAL` | COVERED |  |
| 0x218 | `lane_h` | `.` | `MB_NORMAL` | COVERED |  |
| 0x219 | `lane_h_line` | `.` | `MB_NORMAL` | COVERED |  |
| 0x21A | `lane_W` | `.` | `MB_NORMAL` | COVERED |  |
| 0x21B | `lane_E` | `.` | `MB_NORMAL` | COVERED |  |
| 0x21C | `dance` | `.` | `MB_NORMAL` | COVERED |  |
| 0x21D | `dance_b` | `.` | `MB_NORMAL` | COVERED |  |

### The Theatral Area, the pen, a light well, the hill's stair

`court_works`, 7 wide by 4 tall. On court paving. **The Theatral Area** (LABYRINTH §3): broad shallow steps where the court watched the dances, seen from the front: `steps_L` `steps` `steps_R` (walkable, you climb them), `steps_V` a flight running north (walkable), `steps_corner` where two flights meet (impassable). Lay its floor with `paving.dance`. **The Gentle Bull's pen** in the Central Court: a timber rail fence, `fence_L` `fence` `fence_R` west to east, `fence_V` north to south, `fence_gate` (Sarpedon opens it; impassable until scripted), `trough` and `hay` inside (impassable). **A light well** (`well_*`, 2 x 2): a square shaft open to the sky, a parapet round it and a red column going down into the dark (impassable). **A kouloura** (`pit_*`, 2 x 2): the West Court's round stone-lined pit, grass in it (impassable). **The stair up the palace's hill**: `stair_L` `stair_R` over `stair_foot_L` `stair_foot_R`, a broad gypsum stair (walkable), set in the hill's limestone face (`cliff`) where the Bull Road arrives. `drain`: a stone channel in the paving (walkable); `plinth`: an empty statue base (impassable).

```text
ids                                            walk
0x220 0x221 0x222 0x223 0x224 0x225 0x226   . . . . X X X
0x228 0x229 0x22A 0x22B 0x22C 0x22D 0x22E   X X X X X X X
0x230 0x231 0x232 0x233 0x234 0x235 0x236   X X . . X . X
0x238 0x239 0x23A 0x23B 0x23C 0x23D 0x23E   X X . . X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x220 | `steps_L` | `.` | `MB_NORMAL` | COVERED |  |
| 0x221 | `steps` | `.` | `MB_NORMAL` | COVERED |  |
| 0x222 | `steps_R` | `.` | `MB_NORMAL` | COVERED |  |
| 0x223 | `steps_V` | `.` | `MB_NORMAL` | COVERED |  |
| 0x224 | `steps_corner` | `X` | `MB_NORMAL` | COVERED |  |
| 0x225 | `well_TL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x226 | `well_TR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x228 | `fence_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x229 | `fence` | `X` | `MB_NORMAL` | COVERED |  |
| 0x22A | `fence_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x22B | `fence_V` | `X` | `MB_NORMAL` | COVERED |  |
| 0x22C | `fence_gate` | `X` | `MB_NORMAL` | COVERED |  |
| 0x22D | `well_BL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x22E | `well_BR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x230 | `pit_TL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x231 | `pit_TR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x232 | `stair_L` | `.` | `MB_NORMAL` | COVERED |  |
| 0x233 | `stair_R` | `.` | `MB_NORMAL` | COVERED |  |
| 0x234 | `trough` | `X` | `MB_NORMAL` | COVERED |  |
| 0x235 | `drain` | `.` | `MB_NORMAL` | COVERED |  |
| 0x236 | `plinth` | `X` | `MB_NORMAL` | COVERED |  |
| 0x238 | `pit_BL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x239 | `pit_BR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x23A | `stair_foot_L` | `.` | `MB_NORMAL` | COVERED |  |
| 0x23B | `stair_foot_R` | `.` | `MB_NORMAL` | COVERED |  |
| 0x23C | `hay` | `X` | `MB_NORMAL` | COVERED |  |
| 0x23D | (5, 3) | `X` | `MB_NORMAL` | COVERED |  |
| 0x23E | (6, 3) | `X` | `MB_NORMAL` | COVERED |  |

## Walls and columns

### Gypsum ashlar walls, doorways and horns

`walls`, 8 wide by 3 tall. The palace's walls, standing one storey above the ruin, in gypsum ashlar (on court paving). A wall running west to east is a `top_*` row (its top seen from above, drawn over the player) over a `face_*` row: `_L` `_R` end it; `top_broken` is a gap in the top course, `top_horns` a top course crowned with horns of consecration. Faces: `face_labrys` (a block cut with the masons' double axe), `face_frieze` (a red and ochre painted band, for the court's west façade), `face_window` (a small high window), `face_shadow` (the face in the shadow of a portico). **Doorways** (`MB_NON_ANIMATED_DOOR`, warps to the rooms): `door` (gypsum jambs, a red lintel; the Throne Room, the West Magazines, the Queen's Megaron) and `door_stair` (steps going down into the dark: the Grand Staircase). A wall running north to south is `side` (its top, a strip), ending `side_N` / `side_S`, `side_T` where it meets a west-east wall; turn corners with `corner_NW` `corner_NE` `corner_SW` (the top's corner). Loose: `horns` (great horns of consecration on a plinth, impassable), `rubble` (fallen blocks, impassable), `block` (one fallen block). The paving under each piece is `paving.A`, so lay `A` around walls, or let the mix fall where it may.

```text
ids                                                  walk
0x250 0x251 0x252 0x253 0x254 0x255 0x256 0x257   X X X X X X X X
0x258 0x259 0x25A 0x25B 0x25C 0x25D 0x25E 0x25F   X X X X X X X X
0x260 0x261 0x262 0x263 0x264 0x265 0x266 0x267   D D X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x250 | `top_L` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x251 | `top` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x252 | `top_R` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x253 | `top_broken` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x254 | `top_horns` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x255 | `side` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x256 | `side_N` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x257 | `side_S` | `X` | `MB_NORMAL` | COVERED |  |
| 0x258 | `face_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x259 | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25A | `face_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25B | `face_labrys` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25C | `face_frieze` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25D | `corner_NW` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x25E | `corner_NE` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x25F | `side_T` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x260 | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x261 | `door_stair` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x262 | `face_window` | `X` | `MB_NORMAL` | COVERED |  |
| 0x263 | `face_shadow` | `X` | `MB_NORMAL` | COVERED |  |
| 0x264 | `horns` | `X` | `MB_NORMAL` | COVERED |  |
| 0x265 | `rubble` | `X` | `MB_NORMAL` | COVERED |  |
| 0x266 | `block` | `X` | `MB_NORMAL` | COVERED |  |
| 0x267 | `corner_SW` | `X` | `MB_NORMAL` | SPLIT |  |

### Red columns, porticoes and a pithos

`columns`, 7 wide by 2 tall. LABYRINTH §3's columns: red shafts that **taper downward**, wider at the top, under black cushion capitals, on gypsum bases (on court paving). A column is `col_top` (the capital, drawn over the player) over `col` (impassable); `stump_top` over `stump` is one broken off; `col_grass_top` over `col_grass` stands in the grass (borrowed). **A portico**: a beam row over a row of columns and the shaded floor between them: `beam_L` `beam` (`beam_horns`, horns of consecration on the roof line) `beam_R` above, `beam_col` where a column's capital meets the beam; under the beam, `under_col` (a column in the portico's shade) alternating with `under` (shaded paving, walkable). `pithos_top` over `pithos`: a giant storage jar taller than you, its rope bands in relief (impassable).

```text
ids                                            walk
0x268 0x269 0x26A 0x26B 0x26C 0x26D 0x26E   T T T T T T T
0x270 0x271 0x272 0x273 0x274 0x275 0x276   X X X . X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x268 | `col_top` | `T` | `MB_NORMAL` | SPLIT |  |
| 0x269 | `beam_col` | `T` | `MB_NORMAL` | SPLIT |  |
| 0x26A | `beam_L` | `T` | `MB_NORMAL` | SPLIT |  |
| 0x26B | `beam` | `T` | `MB_NORMAL` | SPLIT |  |
| 0x26C | `beam_R` | `T` | `MB_NORMAL` | SPLIT |  |
| 0x26D | `beam_horns` | `T` | `MB_NORMAL` | SPLIT |  |
| 0x26E | `col_grass_top` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x270 | `col` | `X` | `MB_NORMAL` | COVERED |  |
| 0x271 | `stump` | `X` | `MB_NORMAL` | COVERED |  |
| 0x272 | `under_col` | `X` | `MB_NORMAL` | COVERED |  |
| 0x273 | `under` | `.` | `MB_NORMAL` | COVERED |  |
| 0x274 | `pithos_top` | `X` | `MB_NORMAL` | COVERED |  |
| 0x275 | `col_grass` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x276 | `pithos` | `X` | `MB_NORMAL` | COVERED |  |

## Frescoes and reliefs

### The charging bull, the bull-leapers, the lily prince

`frescoes`, 8 wide by 2 tall. Panels for a wall two face rows tall (stack `walls.face` over `walls.face`; the panels' ground is that ashlar). **The charging bull** (`bull_*`, 3 x 2), the North Entrance's painted relief: a red bull head-down at the charge under an olive, on a pale sky. **The bull-leapers** (`leap_*`, 3 x 2), for the Central Court's east wall: on a blue ground a white bull at the gallop, one leaper vaulting his back, one gripping his horns, one waiting at his tail to catch, in a border of painted checks. **The lily prince** (`prince_*`, 2 x 2), the relief in the corridor south of the court: a red-skinned youth in a crown of lilies and plumes, walking among lilies. All impassable; each is a bg event.

```text
ids                                                  walk
0x290 0x291 0x292 0x293 0x294 0x295 0x296 0x297   X X X X X X X X
0x298 0x299 0x29A 0x29B 0x29C 0x29D 0x29E 0x29F   X X X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x290 | `bull_TL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x291 | `bull_T` | `X` | `MB_NORMAL` | COVERED |  |
| 0x292 | `bull_TR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x293 | `leap_TL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x294 | `leap_T` | `X` | `MB_NORMAL` | COVERED |  |
| 0x295 | `leap_TR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x296 | `prince_TL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x297 | `prince_TR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x298 | `bull_BL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x299 | `bull_B` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29A | `bull_BR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29B | `leap_BL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29C | `leap_B` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29D | `leap_BR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29E | `prince_BL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29F | `prince_BR` | `X` | `MB_NORMAL` | COVERED |  |

## The land

### Low limestone cliffs

`cliff`, 8 wide by 2 tall. Crete's grey-gold limestone, Kythera's cliff kit in Knossa's stone. A cliff whose face looks south is `lip` (the plateau's edge, on borrowed grass) over `face` over a foot: `foot_sea` (borrowed sea, foam breaking at the base, animated), `foot_sand` or `foot_grass` (walkable ground with fallen stones). `_L` / `_R` end a run. Stack `face` rows for a taller cliff. The plateau's other edges: `side_E` (plateau to the west, the drop to the east), `side_W`, `back` (plateau to the south, the drop to the north, the face hidden), `back_NW` / `back_NE`; `corner_in_E` / `_W` turn a south face into a side going north. `seep` is the face where a spring runs out. Lip and face cells are impassable. Here it is the palace's hill (Kephala): stack two or three `face` rows along its south and west, the palace's paving on the plateau above, and cut `court_works.stair_*` into it where the Bull Road arrives.

```text
ids                                                  walk
0x2A8 0x2A9 0x2AA 0x2AB 0x2AC 0x2AD 0x2AE 0x2AF   X X X X X X X X
0x2B0 0x2B1 0x2B2 0x2B3 0x2B4 0x2B5 0x2B6 0x2B7   X X X X X X X .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2A8 | `lip_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2A9 | `lip` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2AA | `lip_b` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2AB | `lip_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2AC | `face_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2AD | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AE | `face_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AF | `face_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B0 | `side_E` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B1 | `side_W` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B2 | `back` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B3 | `back_NW` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B4 | `back_NE` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B5 | `corner_in_E` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B6 | `corner_in_W` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B7 | `foot_grass` | `.` | `MB_NORMAL` | COVERED | grass |
