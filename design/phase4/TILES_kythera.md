# kythera tileset catalog

`gTileset_Kythera` is the Foam Road and the Spring of Kallirhoe (Act III, Kythera Isle; SCRIPT.md Part 10). Pair it with the `aethos` primary, which supplies the open grass, paths, sand, sea, olives and cypresses.

**This file is generated.** `tools/ichor/art/kythera_build.py kythera` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/kythera_*.py` (and `melos_art.py`), the palette plan and the borrowed ground in `kythera_lib.py`.

| Image | Shows |
|---|---|
| [`img/kythera_foam_beach.png`](img/kythera_foam_beach.png) | A 240 x 160 screen of the Foam Road at Aphrodite's rock (3x; `kythera_foam_beach_1x.png` is 1x) |
| [`img/kythera_foam_road.png`](img/kythera_foam_road.png) | A wider stretch of the Foam Road: the herm, the spring stair, the quarry and its drums, the cutting, the reef spit |
| [`img/kythera_spring.png`](img/kythera_spring.png) | The Spring of Kallirhoe |
| [`img/kythera_pieces.png`](img/kythera_pieces.png) | Every structure on its ground |
| [`img/kythera_sheet.png`](img/kythera_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

![A 240 x 160 screen of the Foam Road at Aphrodite's rock (3x; `kythera_foam_beach_1x.png` is 1x)](img/kythera_foam_beach.png)

## The Kythera family

Kythera Isle and Melos need far more distinct pieces than one secondary's 504
tiles hold (the coast and harbor alone came to over 600), so the art is split
by map, the way Emerald gives each town its own secondary. Every one pairs with
the `aethos` primary and is built by `tools/ichor/art/kythera_build.py` from
shared painters, so a piece two of them carry (the surf, myrtle, the house kit)
is drawn once and looks the same in both.

| Tileset | Symbol | Maps | Catalog |
|---|---|---|---|
| `kythera` | `gTileset_Kythera` | the Foam Road, the Spring of Kallirhoe | [`TILES_kythera.md`](TILES_kythera.md) |
| `skandeia` | `gTileset_Skandeia` | Skandeia | [`TILES_skandeia.md`](TILES_skandeia.md) |
| `paphia` | `gTileset_Paphia` | Paphia | [`TILES_paphia.md`](TILES_paphia.md) |
| `neraida` | `gTileset_Neraida` | the Neraida falls | [`TILES_neraida.md`](TILES_neraida.md) |
| `melos` | `gTileset_Melos` | Melos; Routes 22 and 23 and Antikythera; Echo's sea caves | [`TILES_melos.md`](TILES_melos.md) |
| `temple_aphrodite` | `gTileset_TempleAphrodite` | the Temple of Aphrodite (Galatea's Gallery), on the `oikos` interior primary | [`TILES_temple_aphrodite.md`](TILES_temple_aphrodite.md) |

**Seams between them.** SCRIPT.md Part 2 assumed one `kythera` for every Kythera
map, which would have made their shared seams exempt from MAP_DESIGN §5. With the
split, the seam rule applies where neighbours use different secondaries:

| Seam | Tilesets | Rule |
|---|---|---|
| Skandeia's west gate ↔ the Foam Road's east end | skandeia / kythera | the 8 columns nearest the seam, on both maps, use only `aethos` |
| the Foam Road's west end ↔ Paphia's east gate | kythera / paphia | 8 columns, both maps |
| Paphia's north edge ↔ the Neraida falls | paphia / neraida | 6 rows, both maps |
| the Foam Road's stair ↔ the spring | kythera / kythera | exempt |
| the sea maps of Routes 22 and 23 ↔ Melos, Skandeia, Kaldera | sea | aethos sea only, as before |

Gates, lanes and sea are aethos's anyway, so the strips cost little: plant aethos
olives, cypresses, grass and path there.

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet (coast at 0x200, land at 0x290, water at 0x320, town at 0x360). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/kythera_tiles.py` holds every
Kythera-family catalog as a Python dict (`mid('kythera', 'surf', 'S')`), and
`build/kythera/catalog.json` is the same as JSON.

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
| `C` | Cave floor: `MB_CAVE`, wild encounters. Passable. |

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea*, *shallow* or *fall*
draw no ground of their own: after Porytiles compiles, the build points their
bottom-layer tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand
(`0x124`), animated sea (`0x170`), animated turquoise shallows (`0x0D1`) or animated
waterfall (`0x0B3`). They meet aethos ground exactly and cost no tiles. Rebuild
whenever aethos is repainted; the build checks every borrowed entry. A borrowed cell's
own art is in one layer: the middle (`COVERED`, under the player) or the top (`SPLIT`,
over the player).

**Animations.** Porytiles animations in this tileset, driven by `InitTilesetAnim_PorytilesManaged_Kythera` (`include/porytiles_generated/tilesets/kythera/generated_anim_code.h`): `surf`: the foam on the shore, round rocks, at a fall's foot and over a weir, washing up and back (3 frames, ping-pong). Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet. The sea, shallows and waterfall under them are aethos's own animations.

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

**Tile budget.** 457 of 504 tiles (368 metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.

**Scripted swaps.** The build writes the ids scripts swap to the `gTileset_Kythera` block at the end of `include/constants/metatile_labels.h`: `METATILE_Kythera_GirdleGate_TL`, `METATILE_Kythera_GirdleGate_TR`, `METATILE_Kythera_GirdleGate_BL`, `METATILE_Kythera_GirdleGate_BR`, `METATILE_Kythera_GirdleGate_Moved`.

## The coast

### Foam-edged surf

`surf`, 8 wide by 2 tall. Where Kythera's sand meets the sea. Each cell borrows aethos's animated sea and draws the sand to the waterline, a rim of turquoise shallows and the foam, which washes up and back (the `surf` animation, 3 frames). Pieces are named by where the sea is: `S` (sand north, sea south; `S2` is the same with a deeper bite, to break up a long beach), `N`, `E`, `W`; `out_NW` is the south-east tip of a sand spit (sand to the north-west, sea round it), and so on; `in_SE` is a cove's corner, sea only to the south-east. The sand above meets aethos sand (0x124) exactly; the sea below meets aethos sea (0x170). Every cell is `MB_OCEAN_WATER`, like aethos's own beach edges: surf onto it, walk on the sand beside it.

```text
ids                                                  walk
0x200 0x201 0x202 0x203 0x204 0x205 0x206 0x207   W W W W W W W W
0x208 0x209 0x20A 0x20B 0x20C 0x20D 0x20E 0x20F   W W W W W W W W
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x200 | `S` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x201 | `S2` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x202 | `N` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x203 | `E` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x204 | `W` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x205 | `out_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x206 | `out_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x207 | `out_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x208 | `out_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x209 | `in_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x20A | `in_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x20B | `in_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x20C | `in_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x20D | (5, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x20E | (6, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x20F | (7, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |

### White sand: foam lace, shells and wrack

`sand_decor`, 6 wide by 1 tall. Decorations on borrowed aethos sand, all walkable: `lace`, a line of dried foam the tide left (lay it a cell or two above the surf); `shells`, scattered cockles; `scallop`, one great scallop shell, Aphrodite's sign; `wrack`, a line of dried sea-grass; `footprints`, someone walked here; `sherd_dig`, turned earth above the tide line (Alethea's dig spot).

```text
ids                                      walk
0x210 0x211 0x212 0x213 0x214 0x215   . . . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x210 | `lace` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x211 | `shells` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x212 | `scallop` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x213 | `wrack` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x214 | `footprints` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x215 | `sherd_dig` | `.` | `MB_NORMAL` | COVERED | sand |

### Shingle beach, soft-edged

`shingle`, 8 wide by 6 tall. Pebble beach over borrowed aethos sand, as all 47 soft-edge shapes (kythera_lib.blob_key gives a cell's key from a mask). Walkable. The full interior is `1|11111111`. Keep a cell or two of plain sand between shingle and the surf.

Shape keys (kythera_lib.blob_key) and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x218 |
| `1|00000010` | 0x219 |
| `1|00001000` | 0x21A |
| `1|00001010` | 0x21B |
| `1|00001110` | 0x21C |
| `1|00100000` | 0x21D |
| `1|00100010` | 0x21E |
| `1|00101000` | 0x21F |
| `1|00101010` | 0x220 |
| `1|00101110` | 0x221 |
| `1|00111000` | 0x222 |
| `1|00111010` | 0x223 |
| `1|00111110` | 0x224 |
| `1|10000000` | 0x225 |
| `1|10000010` | 0x226 |
| `1|10000011` | 0x227 |
| `1|10001000` | 0x228 |
| `1|10001010` | 0x229 |
| `1|10001011` | 0x22A |
| `1|10001110` | 0x22B |
| `1|10001111` | 0x22C |
| `1|10100000` | 0x22D |
| `1|10100010` | 0x22E |
| `1|10100011` | 0x22F |
| `1|10101000` | 0x230 |
| `1|10101010` | 0x231 |
| `1|10101011` | 0x232 |
| `1|10101110` | 0x233 |
| `1|10101111` | 0x234 |
| `1|10111000` | 0x235 |
| `1|10111010` | 0x236 |
| `1|10111011` | 0x237 |
| `1|10111110` | 0x238 |
| `1|10111111` | 0x239 |
| `1|11100000` | 0x23A |
| `1|11100010` | 0x23B |
| `1|11100011` | 0x23C |
| `1|11101000` | 0x23D |
| `1|11101010` | 0x23E |
| `1|11101011` | 0x23F |
| `1|11101110` | 0x240 |
| `1|11101111` | 0x241 |
| `1|11111000` | 0x242 |
| `1|11111010` | 0x243 |
| `1|11111011` | 0x244 |
| `1|11111110` | 0x245 |
| `1|11111111` | 0x246 |

Every cell: walk `.`, `MB_NORMAL`.

### Tide rocks, a reef spit, white rocks, sea marks

`rocks`, 8 wide by 1 tall. White rock in the sea and on land. `tide_rock` and `tide_rocks` stand in the surf with breathing foam (animated). The reef spit is a walkable path of flat, wet rock out into the sea at low tide (the diver's spit on the Foam Road): `spit_M` runs east-west, `spit_V` north-south, and `spit_head`, a broad flat rock, ends it or turns it. Its foam breathes too. `rock_sand` and `rocks_sand` sit on sand, `rock_grass` on grass.

```text
ids                                                  walk
0x248 0x249 0x24A 0x24B 0x24C 0x24D 0x24E 0x24F   X X . . . X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x248 | `tide_rock` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x249 | `tide_rocks` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x24A | `spit_M` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x24B | `spit_V` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x24C | `spit_head` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x24D | `rock_sand` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x24E | `rocks_sand` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x24F | `rock_grass` | `X` | `MB_NORMAL` | COVERED | grass |

### Aphrodite's rock

`aphrodite_rock`, 3 wide by 3 tall. The great white rock in the shallows where the goddess came ashore on the foam (the Foam Road's set piece, beat III-1D). It borrows aethos's sea; its collar of foam never quite goes away (the `surf` animation). Impassable. Put sea round it on every side; the beach and Alethea's dig spot sit north of it.

```text
ids                    walk
0x250 0x251 0x252   X X X
0x258 0x259 0x25A   X X X
0x260 0x261 0x262   X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x250 | (0, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x251 | `peak` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x252 | (2, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x258 | (0, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x259 | (1, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x25A | (2, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x260 | (0, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x261 | `foot` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x262 | (2, 2) | `X` | `MB_NORMAL` | COVERED | sea |

### Low pink sea-cliffs

`cliff`, 8 wide by 3 tall. Kythera's pink stone, in a kit for low cliffs along the shore and the cutting. A south-facing cliff is `lip` over `face` over a foot: `foot_sea` (borrowed sea, foam breaking at the base, animated), `foot_sand` or `foot_grass` (walkable ground with fallen stones). `_L` / `_R` end a run; `_b` breaks up a long one. The plateau's other edges: `side_E` (plateau to the west, drop to the east), `side_W`, `back` (plateau to the south, drop to the north, the face hidden), `back_NW` / `back_NE` its corners; `corner_in_E` / `_W` turn a south face into a side going north. `spring_lip` is the face with a rock lip a thin fall pours from (pair with `falls.thin_fall` below it); `seep` is the face where the freshwater spring runs out into its basin. Lip and face cells are impassable.

```text
ids                                                  walk
0x268 0x269 0x26A 0x26B 0x26C 0x26D 0x26E 0x26F   X X X X X X X X
0x270 0x271 0x272 0x273 0x274 0x275 0x276 0x277   X X X X X . . .
0x278 0x279 0x27A 0x27B 0x27C 0x27D 0x27E 0x27F   W W W X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x268 | `lip_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x269 | `lip` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x26A | `lip_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x26B | `side_E` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x26C | `side_W` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x26D | `back` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x26E | `back_NW` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x26F | `back_NE` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x270 | `face_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x271 | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x272 | `face_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x273 | `corner_in_E` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x274 | `corner_in_W` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x275 | `foot_sand` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x276 | `foot_grass` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x277 | `foot_sand_rocks` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x278 | `foot_sea_L` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x279 | `foot_sea` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x27A | `foot_sea_R` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x27B | `spring_lip` | `X` | `MB_NORMAL` | COVERED |  |
| 0x27C | `seep` | `X` | `MB_NORMAL` | COVERED |  |
| 0x27D | (5, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x27E | (6, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x27F | (7, 2) | `X` | `MB_NORMAL` | COVERED |  |

### The harbor's gear

`jetty`, 1 wide by 1 tall. Amphitos's fishing jetty off the Foam Road's shingle cove: `gangplank`, a run of timber planks over borrowed sea, laid north-south one cell after another out from the waterline (walkable; Skandeia's gangplank).

```text
ids        walk
0x216   .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x216 | `gangplank` | `.` | `MB_NORMAL` | COVERED | sea |

### A fishing boat, afloat and beached

`kaiki`, 6 wide by 2 tall. A kaiki, the island's fishing boat, bow to the east, 3 x 2 each: `afloat` on borrowed sea, `beached` drawn up on the sand (borrowed sand). Impassable.

```text
ids                                      walk
0x280 0x281 0x282 0x283 0x284 0x285   X X X X X X
0x288 0x289 0x28A 0x28B 0x28C 0x28D   X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x280 | `afloat` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x281 | (1, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x282 | (2, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x283 | `beached` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x284 | (4, 0) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x285 | (5, 0) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x288 | (0, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x289 | (1, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x28A | (2, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x28B | (3, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x28C | (4, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x28D | (5, 1) | `X` | `MB_NORMAL` | COVERED | sand |

## The land

### Myrtle hedges

`myrtle`, 7 wide by 2 tall. Dense, glossy myrtle starred with white flowers, Aphrodite's shrub: the ridge along the Foam Road and the glade round the spring. Runs east-west: `L` `M` (`M2` breaks up a long run) `R`; north-south: `T` `V` `B`; turns: `NW` `NE` `SW` `SE` (named by the corner of the hedge they make). `single` stands alone, `bush` is a smaller round one. `gap_stair` is the run broken by rough steps (the stair up to the spring: walkable). All on borrowed grass; impassable except the stair.

```text
ids                                            walk
0x290 0x291 0x292 0x293 0x294 0x295 0x296   X X X X X X .
0x298 0x299 0x29A 0x29B 0x29C 0x29D 0x29E   X X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x290 | `L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x291 | `M` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x292 | `M2` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x293 | `R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x294 | `single` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x295 | `bush` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x296 | `gap_stair` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x298 | `T` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x299 | `V` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29A | `B` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29B | `NW` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29C | `NE` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29D | `SW` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29E | `SE` | `X` | `MB_NORMAL` | COVERED | grass |

### Rose briar, oleander and meadow flowers

`flowers`, 7 wide by 1 tall. On borrowed grass. `briar` is a wild rose bush; `briar_L` `briar_R` a two-cell thicket. Walkable: `thrift`, sea-pink cushions; `narcissus` and `narcissus_b`, the white flower of the spring (ring Kallirhoe's pool with them); `petals`, rose petals blown on the grass.

```text
ids                                            walk
0x2A0 0x2A1 0x2A2 0x2A3 0x2A4 0x2A5 0x2A6   X X X . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2A0 | `briar` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2A1 | `briar_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2A2 | `briar_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2A3 | `thrift` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2A4 | `narcissus` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2A5 | `narcissus_b` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2A6 | `petals` | `.` | `MB_NORMAL` | COVERED | grass |

### Sea-grass and thrift (tall grass), soft-edged

`seagrass`, 8 wide by 6 tall. Kythera's tall grass: blue-green sea-grass with sea-pink thrift, as all 47 soft-edge shapes on aethos grass (kythera_lib.blob_key gives a cell's key from a mask). `MB_TALL_GRASS` throughout: wild encounters follow the cells while the outline stays soft. The full interior is `1|11111111`.

Shape keys (kythera_lib.blob_key) and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x2A8 |
| `1|00000010` | 0x2A9 |
| `1|00001000` | 0x2AA |
| `1|00001010` | 0x2AB |
| `1|00001110` | 0x2AC |
| `1|00100000` | 0x2AD |
| `1|00100010` | 0x2AE |
| `1|00101000` | 0x2AF |
| `1|00101010` | 0x2B0 |
| `1|00101110` | 0x2B1 |
| `1|00111000` | 0x2B2 |
| `1|00111010` | 0x2B3 |
| `1|00111110` | 0x2B4 |
| `1|10000000` | 0x2B5 |
| `1|10000010` | 0x2B6 |
| `1|10000011` | 0x2B7 |
| `1|10001000` | 0x2B8 |
| `1|10001010` | 0x2B9 |
| `1|10001011` | 0x2BA |
| `1|10001110` | 0x2BB |
| `1|10001111` | 0x2BC |
| `1|10100000` | 0x2BD |
| `1|10100010` | 0x2BE |
| `1|10100011` | 0x2BF |
| `1|10101000` | 0x2C0 |
| `1|10101010` | 0x2C1 |
| `1|10101011` | 0x2C2 |
| `1|10101110` | 0x2C3 |
| `1|10101111` | 0x2C4 |
| `1|10111000` | 0x2C5 |
| `1|10111010` | 0x2C6 |
| `1|10111011` | 0x2C7 |
| `1|10111110` | 0x2C8 |
| `1|10111111` | 0x2C9 |
| `1|11100000` | 0x2CA |
| `1|11100010` | 0x2CB |
| `1|11100011` | 0x2CC |
| `1|11101000` | 0x2CD |
| `1|11101010` | 0x2CE |
| `1|11101011` | 0x2CF |
| `1|11101110` | 0x2D0 |
| `1|11101111` | 0x2D1 |
| `1|11111000` | 0x2D2 |
| `1|11111010` | 0x2D3 |
| `1|11111011` | 0x2D4 |
| `1|11111110` | 0x2D5 |
| `1|11111111` | 0x2D6 |

Every cell: walk `G`, `MB_TALL_GRASS`.

### The rose-marble quarry and the column drums

`quarry`, 8 wide by 3 tall. The quarry spur off the Foam Road. Its cut walls: `cut_*`, the sawn top edge (on borrowed grass), over `face_*`, benches of rose marble squared by the masons, with a row of wedge holes; `face_carved` shows a column drum half cut from the rock. `step` is a cut terrace to stand on (the top step's jar), `step_edge` its lip below. The floor: `chips` (marble chips on borrowed path) and `chips_grass`. Cut stone: `block`, `blocks`. Column drums: `drum_up`, and `drum_fallen` + `drum_fallen_R` lying east-west. The Girdle gate is `gate_TL` `gate_TR` over `gate_BL` `gate_BR`: drums fallen across the quarry's mouth; when the Girdle of Herakles moves them, swap all four cells to `drag`, the path scored with drag marks.

```text
ids                                                  walk
0x2D8 0x2D9 0x2DA 0x2DB 0x2DC 0x2DD 0x2DE 0x2DF   X X X . . X X X
0x2E0 0x2E1 0x2E2 0x2E3 0x2E4 0x2E5 0x2E6 0x2E7   X X X X . X X X
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC 0x2ED 0x2EE 0x2EF   . X X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2D8 | `cut_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2D9 | `cut` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2DA | `cut_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2DB | `step` | `.` | `MB_NORMAL` | COVERED | path |
| 0x2DC | `chips` | `.` | `MB_NORMAL` | COVERED | path |
| 0x2DD | `block` | `X` | `MB_NORMAL` | COVERED | path |
| 0x2DE | `gate_TL` | `X` | `MB_NORMAL` | COVERED | path |
| 0x2DF | `gate_TR` | `X` | `MB_NORMAL` | COVERED | path |
| 0x2E0 | `face_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2E1 | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2E2 | `face_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2E3 | `step_edge` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2E4 | `chips_grass` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2E5 | `blocks` | `X` | `MB_NORMAL` | COVERED | path |
| 0x2E6 | `gate_BL` | `X` | `MB_NORMAL` | COVERED | path |
| 0x2E7 | `gate_BR` | `X` | `MB_NORMAL` | COVERED | path |
| 0x2E8 | `drum_up` | `.` | `MB_NORMAL` | COVERED | path |
| 0x2E9 | `drum_fallen` | `X` | `MB_NORMAL` | COVERED | path |
| 0x2EA | `drum_fallen_R` | `X` | `MB_NORMAL` | COVERED | path |
| 0x2EB | `drag` | `X` | `MB_NORMAL` | COVERED | path |
| 0x2EC | `face_carved` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2ED | (5, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2EE | (6, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2EF | (7, 2) | `X` | `MB_NORMAL` | COVERED |  |

## Fresh water

### The Spring of Kallirhoe's round pool

`spring_pool`, 4 wide by 4 tall. Kallirhoe's pool: a ring of worn, mossy stones round clear turquoise water (borrowed shallows, animated), 4 x 4. The youth kneels on the grass just south of it; put `falls.thin_fall` against its north side for the thin fall from the rock lip, and ring it with `flowers.narcissus`. The water cells are `MB_POND_WATER`; the rim is impassable.

```text
ids                          walk
0x320 0x321 0x322 0x323   X X X X
0x328 0x329 0x32A 0x32B   X P P X
0x330 0x331 0x332 0x333   X P P X
0x338 0x339 0x33A 0x33B   X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x320 | (0, 0) | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x321 | `north` | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x322 | (2, 0) | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x323 | (3, 0) | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x328 | (0, 1) | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x329 | (1, 1) | `P` | `MB_POND_WATER` | COVERED | shallow |
| 0x32A | (2, 1) | `P` | `MB_POND_WATER` | COVERED | shallow |
| 0x32B | (3, 1) | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x330 | (0, 2) | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x331 | (1, 2) | `P` | `MB_POND_WATER` | COVERED | shallow |
| 0x332 | (2, 2) | `P` | `MB_POND_WATER` | COVERED | shallow |
| 0x333 | (3, 2) | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x338 | (0, 3) | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x339 | `south` | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x33A | (2, 3) | `X` | `MB_NORMAL` | COVERED | shallow |
| 0x33B | (3, 3) | `X` | `MB_NORMAL` | COVERED | shallow |

### Waterfalls, and the Foam Road's spring basin

`falls`, 4 wide by 1 tall. Freshwater. `thin_fall`: a thin cascade one cell wide, rock either side of the stream (borrowed waterfall, `MB_WATERFALL`): the spring's fall from its rock lip (put `cliff.spring_lip` above it) and the Foam Road's Horn gate off the cliff west of Aphrodite's rock. `thin_foot` is its foot in a pool, `thin_sea` its foot in the sea (both animated foam). `basin`: the Foam Road's rest point, the stone basin under the cliff's `seep` where pilgrims drink (borrowed shallows; impassable, read it).

```text
ids                          walk
0x324 0x325 0x326 0x327   F P W X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x324 | `thin_fall` | `F` | `MB_WATERFALL` | COVERED | fall |
| 0x325 | `thin_foot` | `P` | `MB_POND_WATER` | COVERED | shallow |
| 0x326 | `thin_sea` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x327 | `basin` | `X` | `MB_NORMAL` | COVERED | shallow |

### The Minoan vault door, the cave stair

`cave_stair`, 1 wide by 2 tall. Set into a pink cliff face: `cave_top` over `cave_stair`, a rough arch and a rock stair going down into the dark, the spring's way down to Echo's caves. The stair is the door (`MB_NON_ANIMATED_DOOR`).

```text
ids        walk
0x32C   X
0x334   D
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x32C | `cave_top` | `X` | `MB_NORMAL` | COVERED |  |
| 0x334 | `cave_stair` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |

## Town

### The great herm and the harbor shrine

`herm`, 1 wide by 2 tall. Kythera's great herm at the Foam Road's fork: a tall marble pillar with Hermes's bearded head, the oil on his face long dried to a dark stain, on a plinth carved with the roads (on borrowed grass). `herm` (top, drawn over the player) over `herm_base` (impassable; bg event here).

```text
ids        walk
0x360   T
0x368   X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x360 | `herm` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x368 | `herm_base` | `X` | `MB_NORMAL` | COVERED | grass |

### The boat on log rollers

`rollers`, 3 wide by 2 tall. The boat KASSITEROS hauled up the Foam Road toward Paphia on log rollers (borrowed path), a sickle chalked on her bow; after Knossa she is still there, abandoned. 3 x 2, impassable; the bg event goes on her bow.

```text
ids                    walk
0x361 0x362 0x363   X X X
0x369 0x36A 0x36B   X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x361 | `boat` | `X` | `MB_NORMAL` | COVERED | path |
| 0x362 | (1, 0) | `X` | `MB_NORMAL` | COVERED | path |
| 0x363 | (2, 0) | `X` | `MB_NORMAL` | COVERED | path |
| 0x369 | (0, 1) | `X` | `MB_NORMAL` | COVERED | path |
| 0x36A | (1, 1) | `X` | `MB_NORMAL` | COVERED | path |
| 0x36B | (2, 1) | `X` | `MB_NORMAL` | COVERED | path |
