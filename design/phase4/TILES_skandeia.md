# skandeia tileset catalog

`gTileset_Skandeia` is Skandeia, Kythera's harbor town (Act III, Kythera Isle; SCRIPT.md Part 10). Pair it with the `aethos` primary, which supplies the open grass, paths, sand, sea, olives and cypresses.

**This file is generated.** `tools/ichor/art/kythera_build.py skandeia` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/kythera_*.py` (and `melos_art.py`), the palette plan and the borrowed ground in `kythera_lib.py`.

| Image | Shows |
|---|---|
| [`img/skandeia_pieces.png`](img/skandeia_pieces.png) | Every structure on its ground |
| [`img/skandeia_sheet.png`](img/skandeia_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

It is one of the Kythera family of secondaries; see [`TILES_kythera.md`](TILES_kythera.md) for why the art is split and which seams then need aethos-only strips.

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet (harbor at 0x200, town at 0x2A0, coast at 0x310). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/kythera_tiles.py` holds every
Kythera-family catalog as a Python dict (`mid('skandeia', 'surf', 'S')`), and
`build/skandeia/catalog.json` is the same as JSON.

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
| `F` | Waterfall: `MB_WATERFALL` (the Horn of Achelous climbs it). |
| `J` | Ledge: `MB_JUMP_SOUTH`. |

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea*, *shallow* or *fall*
draw no ground of their own: after Porytiles compiles, the build points their
bottom-layer tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand
(`0x124`), animated sea (`0x170`), animated turquoise shallows (`0x0D1`) or animated
waterfall (`0x0B3`). They meet aethos ground exactly and cost no tiles. Rebuild
whenever aethos is repainted; the build checks every borrowed entry. A borrowed cell's
own art is in one layer: the middle (`COVERED`, under the player) or the top (`SPLIT`,
over the player).

**Animations.** Porytiles animations in this tileset, driven by `InitTilesetAnim_PorytilesManaged_Skandeia` (`include/porytiles_generated/tilesets/skandeia/generated_anim_code.h`): `surf`: the foam on the shore, round rocks, at a fall's foot and over a weir, washing up and back (3 frames, ping-pong). Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet. The sea, shallows and waterfall under them are aethos's own animations.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of seven color
groups, one per secondary palette (`kythera_lib.GROUPS`), passed to Porytiles as packing
hints.

| Group | Use |
|---|---|
| foam | The surf, foam lace, shingle, white rock, Aphrodite's rock, reefs, quays, pumice |
| rose | Pink stone and rose marble: sea-cliffs, the quarry, temple and stair, kerbs, moss |
| green | Myrtle, sea-grass and thrift, roses, narcissus, plane, oleander, apple |
| cyc | Whitewashed houses, Aegean doors, rose-pink frames, pots, dovecotes, sea doors |
| terra | Timber and terracotta: boats, the trireme, slips, mill wheels, bridges, gear |
| bronze | Bronze mirrors, the harbor shrine's dove, the great herm, the Minoan vault door |
| melos | Melos's obsidian slope on its earth and grass |

**Tile budget.** 358 of 504 tiles (304 metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.

**Scripted swaps.** The build writes the ids scripts swap to the `gTileset_Skandeia` block at the end of `include/constants/metatile_labels.h`: `METATILE_Skandeia_Slip_Empty_TL`, `METATILE_Skandeia_Slip_Boat_TL`.

## The harbor

### The curved stone quay

`quay`, 8 wide by 3 tall. Skandeia's quay (and Paphia's jetty). Its top is aethos's limestone path (0x1D9): pave the quay with it, and these edges finish it where its wall drops into the sea (each borrows aethos's sea). Named by where the sea is: `S` (sea south; `S_b` adds a drain, `ring_S` a bronze mooring ring), `N`, `E`, `W`; `out_SE` is the quay's rounded south-east corner (the sea round it), `in_SE` the inside of a bend (sea only to the south-east): the rounded corners make the quay curve. `steps_E` and `steps_S` go down into the water for boats (walkable). `N_plank` is the north edge with a ship's gangplank landing on it (a ship moored to the north, as the Euploia's plank comes down to it), `S_plank` the south edge with a plank going down to a boat (both walkable). Edge cells are otherwise impassable: the quay's walkable top ends on the path cell behind them.

```text
ids                                                  walk
0x200 0x201 0x202 0x203 0x204 0x205 0x206 0x207   X X X X X X X X
0x208 0x209 0x20A 0x20B 0x20C 0x20D 0x20E 0x20F   X X X X X . . X
0x210 0x211 0x212 0x213 0x214 0x215 0x216 0x217   . . . . . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x200 | `S` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x201 | `S_b` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x202 | `N` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x203 | `E` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x204 | `W` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x205 | `out_SE` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x206 | `out_SW` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x207 | `out_NE` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x208 | `out_NW` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x209 | `in_SE` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x20A | `in_SW` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x20B | `in_NE` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x20C | `in_NW` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x20D | `steps_E` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x20E | `steps_S` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x20F | `ring_S` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x210 | `N_plank` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x211 | `S_plank` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x212 | (2, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x213 | (3, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x214 | (4, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x215 | (5, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x216 | (6, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x217 | (7, 2) | `.` | `MB_NORMAL` | COVERED | sea |

### Slipways, and the boat the Titans left

`slips`, 4 wide by 3 tall. The slipways at the quay's north end, every one empty and chalked with a sickle. `slip` (2 wide x 3 tall at its top-left): a stone ramp with timber runners down into the sea, its foot on borrowed sea. `slip_boat` (2 x 3): the one boat the Titans left, hauled up the same slip, a sickle chalked on her bow and, smaller, somebody else's note. After the climax the boats come back: swap `slip_boat`'s six cells over a `slip`'s. Impassable; the feet are water.

```text
ids                          walk
0x218 0x219 0x21A 0x21B   X X X X
0x220 0x221 0x222 0x223   X X X X
0x228 0x229 0x22A 0x22B   W W W W
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x218 | `slip` | `X` | `MB_NORMAL` | COVERED |  |
| 0x219 | (1, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x21A | `slip_boat` | `X` | `MB_NORMAL` | COVERED |  |
| 0x21B | (3, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x220 | (0, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x221 | (1, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x222 | (2, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x223 | (3, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x228 | (0, 2) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x229 | (1, 2) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x22A | (2, 2) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x22B | (3, 2) | `W` | `MB_OCEAN_WATER` | COVERED | sea |

### A fishing boat, afloat and beached

`kaiki`, 6 wide by 2 tall. A kaiki, the island's fishing boat, bow to the east, 3 x 2 each: `afloat` on borrowed sea, `beached` drawn up on the sand (borrowed sand). Impassable.

```text
ids                                      walk
0x230 0x231 0x232 0x233 0x234 0x235   X X X X X X
0x238 0x239 0x23A 0x23B 0x23C 0x23D   X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x230 | `afloat` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x231 | (1, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x232 | (2, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x233 | `beached` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x234 | (4, 0) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x235 | (5, 0) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x238 | (0, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x239 | (1, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x23A | (2, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x23B | (3, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x23C | (4, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x23D | (5, 1) | `X` | `MB_NORMAL` | COVERED | sand |

### The trireme Euploia

`trireme`, 8 wide by 3 tall. The Euploia moored bow to the east, as at Akti, on borrowed sea; place her with her bottom row on the water just north of the quay, so her gangplank (bottom row, column 3) lands on the quay's south edge below. Impassable. At Skandeia she is requisitioned: Molybdos stands at the plank.

```text
ids                                                  walk
0x240 0x241 0x242 0x243 0x244 0x245 0x246 0x247   X X X X X X X X
0x248 0x249 0x24A 0x24B 0x24C 0x24D 0x24E 0x24F   X X X X X X X X
0x250 0x251 0x252 0x253 0x254 0x255 0x256 0x257   X X X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x240 | (0, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x241 | (1, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x242 | (2, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x243 | (3, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x244 | (4, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x245 | (5, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x246 | (6, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x247 | (7, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x248 | (0, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x249 | (1, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x24A | (2, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x24B | (3, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x24C | (4, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x24D | (5, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x24E | (6, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x24F | (7, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x250 | (0, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x251 | (1, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x252 | (2, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x253 | `gangplank` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x254 | (4, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x255 | (5, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x256 | (6, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x257 | (7, 2) | `X` | `MB_NORMAL` | COVERED | sea |

### The harbor's gear

`gear`, 7 wide by 1 tall. On borrowed path (the quay's top). `oars`, a stack of oars the Titanborn carry to the slips; `nets`, a heap of nets with floats (the old sailor mends them); `rope`, a coil (walkable); `amphorae`, a rack of jars; `crate`, a fish crate; `bollard`, a stone bollard. `gangplank` is a plank over borrowed sea (walkable) from the quay's edge to a ship's side.

```text
ids                                            walk
0x258 0x259 0x25A 0x25B 0x25C 0x25D 0x25E   X X . X X X .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x258 | `oars` | `X` | `MB_NORMAL` | COVERED | path |
| 0x259 | `nets` | `X` | `MB_NORMAL` | COVERED | path |
| 0x25A | `rope` | `.` | `MB_NORMAL` | COVERED | path |
| 0x25B | `amphorae` | `X` | `MB_NORMAL` | COVERED | path |
| 0x25C | `crate` | `X` | `MB_NORMAL` | COVERED | path |
| 0x25D | `bollard` | `X` | `MB_NORMAL` | COVERED | path |
| 0x25E | `gangplank` | `.` | `MB_NORMAL` | COVERED | sea |

## Town

### The Cycladic house kit

`house`, 5 wide by 4 tall. Parts that snap together into whitewashed cube houses (see *House fronts* below). Rows: `R_*` the flat roof and its parapet, seen from above; `U_*` the upper wall; `G_*` and the doors, the ground-floor wall on its grey-washed foot. Columns `_L` (the lit west corner), `_M` (repeat it), `_R` (the shaded east corner). Roof extras: `R_chimney`, `R_dove` / `R_doves` (Paphia's roofs), `R_jar` (a water jar on the roof). Upper-wall extras: `U_window` (blue shutters), `U_window_pink`, `U_niche` (a little lamp niche), `U_vine` (a vine trained over the wall). Doors (`MB_NON_ANIMATED_DOOR`, put the warp here): `door` (Aegean blue in a rose-pink frame), `door_white` (the same in a white frame, for Skandeia's plainer houses), `door_arch` (an arched doorway). Ground-wall extras: `G_window`, `pot_rose`, `pot_basil` (a pot on the step), `mirror` (a polished bronze mirror by the door, Paphia's custom) and `mirror_dim` (the same, a dim figure in it), `G_bench` (a whitewashed bench), `G_shell` (a scallop shell set in the wall), `G_steps` (an outside stair up to the roof). Every cell is impassable except the doors.

```text
ids                                walk
0x2A0 0x2A1 0x2A2 0x2A3 0x2A4   X X X X X
0x2A8 0x2A9 0x2AA 0x2AB 0x2AC   X X X X X
0x2B0 0x2B1 0x2B2 0x2B3 0x2B4   X X X D D
0x2B8 0x2B9 0x2BA 0x2BB 0x2BC   X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2A0 | `R_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A1 | `R_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A2 | `R_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A3 | `R_chimney` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A4 | `R_jar` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A8 | `U_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A9 | `U_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AA | `U_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AB | `U_window` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AC | `U_vine` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B0 | `G_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B1 | `G_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B2 | `G_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B3 | `door_white` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x2B4 | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x2B8 | `pot_rose` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B9 | `pot_basil` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2BA | `G_window` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2BB | `G_bench` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2BC | `G_steps` | `X` | `MB_NORMAL` | COVERED |  |

### The great herm and the harbor shrine

`shrine`, 1 wide by 2 tall. Aphrodite of the Harbor, at the quay's south end: a marble niche with a bronze dove, its sill heaped with old shells (on borrowed path). `shrine` (top, drawn over the player) over `shrine_base` (impassable; the bg event).

```text
ids        walk
0x2A5   T
0x2AD   X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2A5 | `shrine` | `T` | `MB_NORMAL` | SPLIT | path |
| 0x2AD | `shrine_base` | `X` | `MB_NORMAL` | COVERED | path |

### Pink-stone terrace walls

`terrace`, 7 wide by 2 tall. A retaining wall one cell high between two terraces, in pink rubble with a lit coping. Lay a `top_*` row (the upper terrace's edge, walkable, on borrowed grass) above a wall row: `L` `M` (`M2`) `R`. `steps` cuts a stair through the wall (walkable) under `top_steps`. `niche` is an arched niche with a low plinth, for a statue or a votive (Melos's armless goddess stands in one); `spout` is a lion-less spring spout dribbling into a trough.

```text
ids                                            walk
0x2C0 0x2C1 0x2C2 0x2C3 0x2C4 0x2C5 0x2C6   X X X X . X X
0x2C8 0x2C9 0x2CA 0x2CB 0x2CC 0x2CD 0x2CE   . . . . T . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2C0 | `L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2C1 | `M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C2 | `M2` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C3 | `R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2C4 | `steps` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C5 | `niche` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C6 | `spout` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C8 | `top_L` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2C9 | `top` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2CA | `top_M2` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2CB | `top_R` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2CC | `top_steps` | `T` | `MB_NORMAL` | COVERED | grass |
| 0x2CD | `top_niche` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2CE | `top_spout` | `.` | `MB_NORMAL` | COVERED | grass |

### House fronts

Every house is a home (MAP_DESIGN.md §2), so each front has a door. These are arrangements of the `house` kit's parts and cost no metatiles of their own; mix the parts for more. Walk: every house cell is `X` except its door (`D`).

**A cube house** (`cube`): the commonest Kythera house: one room, a blue door.

```text
ids                    walk
0x2A0 0x2A1 0x2A2   X X X
0x2A8 0x2AB 0x2AA   X X X
0x2B0 0x2B3 0x2B2   X D X
```

**A cube house with roses** (`cube_pot`): Skandeia: a pot of roses on the step.

```text
ids                          walk
0x2A0 0x2A3 0x2A1 0x2A2   X X X X
0x2A8 0x2AB 0x2A9 0x2AA   X X X X
0x2B0 0x2B3 0x2B8 0x2B2   X D X X
```

**A long house** (`long_house`): a family house, basil by the door, a bench.

```text
ids                                walk
0x2A0 0x2A1 0x2A4 0x2A1 0x2A2   X X X X X
0x2A8 0x2AB 0x2A9 0x2AB 0x2AA   X X X X X
0x2B0 0x2B9 0x2B3 0x2BB 0x2B2   X X D X X
```

**A house with an outside stair** (`stair_house`): a stair up to the roof terrace.

```text
ids                    walk
0x2A0 0x2A1 0x2A2   X X X
0x2A8 0x2AB 0x2AA   X X X
0x2BC 0x2B3 0x2B2   X D X
```

## The coast

### Foam-edged surf

`surf`, 8 wide by 2 tall. Where Kythera's sand meets the sea. Each cell borrows aethos's animated sea and draws the sand to the waterline, a rim of turquoise shallows and the foam, which washes up and back (the `surf` animation, 3 frames). Pieces are named by where the sea is: `S` (sand north, sea south; `S2` is the same with a deeper bite, to break up a long beach), `N`, `E`, `W`; `out_NW` is the south-east tip of a sand spit (sand to the north-west, sea round it), and so on; `in_SE` is a cove's corner, sea only to the south-east. The sand above meets aethos sand (0x124) exactly; the sea below meets aethos sea (0x170). Every cell is `MB_OCEAN_WATER`, like aethos's own beach edges: surf onto it, walk on the sand beside it.

```text
ids                                                  walk
0x310 0x311 0x312 0x313 0x314 0x315 0x316 0x317   W W W W W W W W
0x318 0x319 0x31A 0x31B 0x31C 0x31D 0x31E 0x31F   W W W W W W W W
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x310 | `S` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x311 | `S2` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x312 | `N` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x313 | `E` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x314 | `W` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x315 | `out_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x316 | `out_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x317 | `out_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x318 | `out_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x319 | `in_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x31A | `in_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x31B | `in_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x31C | `in_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x31D | (5, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x31E | (6, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x31F | (7, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |

### White sand: foam lace, shells and wrack

`sand_decor`, 4 wide by 1 tall. On borrowed sand, walkable: `lace` (a line of dried foam), `shells`, `scallop`, `wrack`.

```text
ids                          walk
0x320 0x321 0x322 0x323   . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x320 | `lace` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x321 | `shells` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x322 | `scallop` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x323 | `wrack` | `.` | `MB_NORMAL` | COVERED | sand |

### Myrtle hedges

`myrtle`, 5 wide by 1 tall. Myrtle on borrowed grass: a run `L` `M` `R`, a `single` clump and a smaller round `bush`. Impassable.

```text
ids                                walk
0x328 0x329 0x32A 0x32B 0x32C   X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x328 | `L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x329 | `M` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x32A | `R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x32B | `single` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x32C | `bush` | `X` | `MB_NORMAL` | COVERED | grass |

### Rose briar, oleander and meadow flowers

`flowers`, 3 wide by 1 tall. On borrowed grass: `briar`, a wild rose bush (impassable); `thrift` and `petals` (walkable).

```text
ids                    walk
0x324 0x325 0x326   X . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x324 | `briar` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x325 | `thrift` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x326 | `petals` | `.` | `MB_NORMAL` | COVERED | grass |
