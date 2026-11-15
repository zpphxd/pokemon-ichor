# lakonia tileset catalog

`gTileset_Lakonia` is Lakonia, the town with no walls (Act III, Lakonia; SCRIPT.md Part 10). It serves Lakonia. Pair it with the `aethos` primary, which supplies the open grass, paths, sand, sea, olives, cypresses and stone pines.

**This file is generated.** `tools/ichor/art/lakonia_build.py lakonia` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/lakonia_*.py` (the plane tree is Kythera's), the palette plan, the water and the soft-edge autotiles in `lakonia_lib.py`.

| Image | Shows |
|---|---|
| [`img/lakonia_agoge.png`](img/lakonia_agoge.png) | A 240 x 160 screen of the agoge's yard: the ring, the barracks, the Taygetos wall behind (3x; `lakonia_agoge_1x.png` is 1x) |
| [`img/lakonia_town.png`](img/lakonia_town.png) | The agora and the river: the Persian Stoa, the chained Enyalios, the Lesche, houses round their yards, the bridge, Orthia |
| [`img/lakonia_pieces.png`](img/lakonia_pieces.png) | Every structure on its ground |
| [`img/lakonia_sheet.png`](img/lakonia_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

![A 240 x 160 screen of the agoge's yard: the ring, the barracks, the Taygetos wall behind (3x; `lakonia_agoge_1x.png` is 1x)](img/lakonia_agoge.png)

## The Lakonia family

SCRIPT.md's front matter planned one `lakonia` secondary for all six maps.
Their pieces come to far more than one secondary's 504 tiles (the town alone,
with its ring, stoa, houses and the Taygetos wall, fills most of one), so the
art is split by map, as the Kythera family is. Every one pairs with the
`aethos` primary and is built by `tools/ichor/art/lakonia_build.py` from shared
painters, so a piece two of them carry (the Eurotas, the plane tree, the house
kit, the Taygetos rock) is drawn once and looks the same in both.

| Tileset | Symbol | Maps | Catalog |
|---|---|---|---|
| `gytheion` | `gTileset_Gytheion` | Gytheion; Route 24, the strait off Malea | [`TILES_gytheion.md`](TILES_gytheion.md) |
| `eurotas` | `gTileset_Eurotas` | Route 25, up the Eurotas | [`TILES_eurotas.md`](TILES_eurotas.md) |
| `lakonia` | `gTileset_Lakonia` | Lakonia | [`TILES_lakonia.md`](TILES_lakonia.md) |
| `stymphalia` | `gTileset_Stymphalia` | Route 26, Lake Stymphalia, Route 27 | [`TILES_stymphalia.md`](TILES_stymphalia.md) |

**Seams.** With the split, MAP_DESIGN §5's seam rule applies wherever neighbours
use different secondaries: the strip nearest the seam, on both maps, uses only
`aethos` metatiles (grass, path, olives, cypresses, pines, aethos sea).

| Seam | Tilesets | Rule |
|---|---|---|
| Route 24's west end ↔ Gytheion's harbor mouth | gytheion / gytheion | exempt |
| Route 24's east end ↔ Skandeia's north bay | gytheion / skandeia | 8 columns, both maps (open sea: aethos's anyway) |
| Gytheion's north gap ↔ Route 25's south end | gytheion / eurotas | 6 rows, both maps |
| Route 25's west end ↔ Lakonia's east edge | eurotas / lakonia | 8 columns, both maps: keep the Eurotas, its bridge and the plane trees 9 or more columns in from the seam |
| Lakonia's north gap ↔ Route 26's south end | lakonia / stymphalia | 6 rows, both maps |
| Route 26 ↔ Lake Stymphalia ↔ Route 27 | stymphalia / stymphalia | exempt |
| Route 27's west end ↔ Arkadia (Act II) | stymphalia / Act II's | 8 columns, both maps |

The strips cost little: the gaps and roads are aethos path and grass anyway,
and aethos olives, cypresses and stone pines plant the edges.

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet (town at 0x200, yard at 0x288, land at 0x350, water at 0x388). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/lakonia_tiles.py` holds every
Lakonia-family catalog as a Python dict (`mid('lakonia', 'house', 'door')`, and
`blob_key(mask, x, y)` for the soft-edged pieces), and `build/lakonia/catalog.json` is
the same as JSON.

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
| `C` | A sea current: `MB_WESTWARD_CURRENT`, surfable. |
| `J` | Ledge: `MB_JUMP_SOUTH`. |

**Soft-edged pieces** (`yard`, `sands`, `river`, `reeds`, `marsh`, `marsh_reeds`,
`curtain`, `scree`...) are drawn as all 47 blob shapes and named by shape key: `1|`
then the cell's N NE E SE S SW W NW neighbours (1 = in the region; a diagonal counts
only when both its sides do). `blob_key(mask, x, y)` in `lakonia_tiles.py` computes it.
Each 8x8 quadrant depends only on its own two sides and corner, so a whole set costs
about a dozen tiles.

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea* or *shallow* draw
no ground of their own: after Porytiles compiles, the build points their bottom-layer
tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated
sea (`0x170`) or animated turquoise shallows (`0x0D1`). They meet aethos ground exactly
and cost no tiles. Rebuild whenever aethos is repainted. A borrowed cell's own art is
in one layer: the middle (`COVERED`, under the player) or the top (`SPLIT`, over him).

**Fresh water** is Lakonia's own: the Eurotas's slow green water and Stymphalia's black
water are animated textures in the bottom layer of every water cell (the same few
tiles under all of them), with banks, reeds, planks and stone on the middle layer.

**Animations.** Porytiles animations in this tileset, driven by `InitTilesetAnim_PorytilesManaged_Lakonia` (`include/porytiles_generated/tilesets/lakonia/generated_anim_code.h`): `eurotas`: the river's slow ripples drifting (3 frames). Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet. Borrowed sea and shallows keep aethos's own animations.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of seven color
groups, one per secondary palette (`lakonia_lib.GROUPS`), passed to Porytiles as packing
hints:

| Group | Use |
|---|---|
| red | Lakonian red and bronze: cloaks, shields, doors, awnings, the bronze gods |
| stone | Plain stone, plaster and clay roofs: houses, the stoa, stelai, bridges, the causeway |
| veg | Plane, holm-oak, oak, walnut, willow; bark; the Sown Field |
| river | The Eurotas: green water, its banks, reeds and pink oleander |
| mount | Taygetos and the Skiritis: dark rock, scree, black pine; Malea's foam |
| wood | Timber and thatch: boardwalks, the stilt hut, racks, the barracks' roof, posts |
| yard | Beaten sand: the agoge's yard, the ring, the wrestling sands, their stone |

**Tile budget.** 500 of 504 tiles (464 metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.

**Scripted swaps.** The build writes the ids scripts swap to the `gTileset_Lakonia` block at the end of `include/constants/metatile_labels.h`: `METATILE_Lakonia_SownField_Teeth`, `METATILE_Lakonia_SownField`.

## Town

### Plain flat-roofed houses

`house`, 8 wide by 5 tall. Lakonian houses: tan lime plaster over mudbrick on a rubble footing, flat roofs of beaten clay, timber doors stained red, no ornament. Build a front from rows: a roof (`R_L` `R_M` `R_R` one row deep; or `RB_*` over `RF_*` for a deeper house), an optional upper wall (`U_*`), and the ground floor (`G_*` with the `door`). A house with no upper wall is low, one room. `R_jar` `RF_jar` `R_brush` put a jar or a heap of brushwood on a roof; `R_vent` is the syssition's smoke hole. `T_L` `T_M` `T_R` are reed thatch, for the barracks. `U_window`, `U_worn` (plaster fallen off the brick), `U_shield` (a bronze shield with the lambda hung over Lampito's door), `U_cloak` (a red cloak on a peg), `U_list` (the herd's names painted by the barracks door). `G_window`, `G_open` (an open doorway, dark), `G_bench` (a stone bench), `G_jar` (a pithos), `G_spears` (a rack of practice spears), `G_wood` (stacked firewood), `G_worn`. The Lesche's porch: `P_L` `P_col` `P_gap` `P_R` with `door_porch` at its back. Every cell is impassable but the doors (`MB_NON_ANIMATED_DOOR`). The fronts below arrange them.

```text
ids                                                  walk
0x200 0x201 0x202 0x203 0x204 0x205 0x206 0x207   X X X X X X X X
0x208 0x209 0x20A 0x20B 0x20C 0x20D 0x20E 0x20F   X X X X X X X X
0x210 0x211 0x212 0x213 0x214 0x215 0x216 0x217   X X X X X X X X
0x218 0x219 0x21A 0x21B 0x21C 0x21D 0x21E 0x21F   X X X D X X X X
0x220 0x221 0x222 0x223 0x224 0x225 0x226 0x227   X X D X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x200 | `RB_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x201 | `RB_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x202 | `RB_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x203 | `R_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x204 | `R_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x205 | `R_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x206 | `R_brush` | `X` | `MB_NORMAL` | COVERED |  |
| 0x207 | `R_vent` | `X` | `MB_NORMAL` | COVERED |  |
| 0x208 | `RF_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x209 | `RF_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x20A | `RF_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x20B | `RF_jar` | `X` | `MB_NORMAL` | COVERED |  |
| 0x20C | `T_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x20D | `T_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x20E | `T_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x20F | `U_window` | `X` | `MB_NORMAL` | COVERED |  |
| 0x210 | `U_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x211 | `U_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x212 | `U_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x213 | `U_shield` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x214 | `U_worn` | `X` | `MB_NORMAL` | COVERED |  |
| 0x215 | `U_cloak` | `X` | `MB_NORMAL` | COVERED |  |
| 0x216 | `U_list` | `X` | `MB_NORMAL` | COVERED |  |
| 0x217 | `G_jar` | `X` | `MB_NORMAL` | COVERED |  |
| 0x218 | `G_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x219 | `G_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x21A | `G_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x21B | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x21C | `G_open` | `X` | `MB_NORMAL` | COVERED |  |
| 0x21D | `G_bench` | `X` | `MB_NORMAL` | COVERED |  |
| 0x21E | `G_spears` | `X` | `MB_NORMAL` | COVERED |  |
| 0x21F | `G_wood` | `X` | `MB_NORMAL` | COVERED |  |
| 0x220 | `P_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x221 | `P_col` | `X` | `MB_NORMAL` | COVERED |  |
| 0x222 | `door_porch` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x223 | `P_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x224 | (4, 4) | `X` | `MB_NORMAL` | COVERED |  |
| 0x225 | (5, 4) | `X` | `MB_NORMAL` | COVERED |  |
| 0x226 | (6, 4) | `X` | `MB_NORMAL` | COVERED |  |
| 0x227 | (7, 4) | `X` | `MB_NORMAL` | COVERED |  |

### The Persian Stoa

`stoa`, 7 wide by 6 tall. The Persian Stoa along the agora's east side (an object, Part 2): its roof held up by carved men in trousers and tall hats, captives from the war, a trace of red paint left on their clothes. Drawn 7 wide; widen it by repeating the middle columns (`col_*` and `gap_*`, 3 tall, alternating) and the middle `roof`, `beam` and `step` cells. The step row is walkable; put the object's bg event on a column's base.

```text
ids                                            walk
0x228 0x229 0x22A 0x22B 0x22C 0x22D 0x22E   X X X X X X X
0x230 0x231 0x232 0x233 0x234 0x235 0x236   X X X X X X X
0x238 0x239 0x23A 0x23B 0x23C 0x23D 0x23E   X X X X X X X
0x240 0x241 0x242 0x243 0x244 0x245 0x246   X X X X X X X
0x248 0x249 0x24A 0x24B 0x24C 0x24D 0x24E   X X X X X X X
0x250 0x251 0x252 0x253 0x254 0x255 0x256   . . . . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x228 | `roof_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x229 | `roof` | `X` | `MB_NORMAL` | COVERED |  |
| 0x22A | (2, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x22B | (3, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x22C | (4, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x22D | (5, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x22E | `roof_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x230 | `beam_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x231 | `beam` | `X` | `MB_NORMAL` | COVERED |  |
| 0x232 | (2, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x233 | (3, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x234 | (4, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x235 | (5, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x236 | `beam_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x238 | (0, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x239 | `col_top` | `X` | `MB_NORMAL` | COVERED |  |
| 0x23A | `gap_top` | `X` | `MB_NORMAL` | COVERED |  |
| 0x23B | (3, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x23C | (4, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x23D | (5, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x23E | (6, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x240 | (0, 3) | `X` | `MB_NORMAL` | COVERED |  |
| 0x241 | `col_mid` | `X` | `MB_NORMAL` | COVERED |  |
| 0x242 | `gap_mid` | `X` | `MB_NORMAL` | COVERED |  |
| 0x243 | (3, 3) | `X` | `MB_NORMAL` | COVERED |  |
| 0x244 | (4, 3) | `X` | `MB_NORMAL` | COVERED |  |
| 0x245 | (5, 3) | `X` | `MB_NORMAL` | COVERED |  |
| 0x246 | (6, 3) | `X` | `MB_NORMAL` | COVERED |  |
| 0x248 | (0, 4) | `X` | `MB_NORMAL` | COVERED |  |
| 0x249 | `col_base` | `X` | `MB_NORMAL` | COVERED |  |
| 0x24A | `gap_base` | `X` | `MB_NORMAL` | COVERED |  |
| 0x24B | (3, 4) | `X` | `MB_NORMAL` | COVERED |  |
| 0x24C | (4, 4) | `X` | `MB_NORMAL` | COVERED |  |
| 0x24D | (5, 4) | `X` | `MB_NORMAL` | COVERED |  |
| 0x24E | (6, 4) | `X` | `MB_NORMAL` | COVERED |  |
| 0x250 | `step_L` | `.` | `MB_NORMAL` | COVERED |  |
| 0x251 | `step` | `.` | `MB_NORMAL` | COVERED |  |
| 0x252 | (2, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x253 | (3, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x254 | (4, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x255 | (5, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x256 | `step_R` | `.` | `MB_NORMAL` | COVERED |  |

### A Doric colonnade (the palaestra's porch)

`colonnade`, 5 wide by 3 tall. The palaestra's porch on the wrestling sands: a tiled roof over plain Doric columns (2 cells tall) and the court's shade behind them. Repeat `col`/`gap` (and the roof and base under them) to lengthen it. `door` (base row) is the palaestra's door (`MB_NON_ANIMATED_DOOR`), at the back of the porch.

```text
ids                                walk
0x258 0x259 0x25A 0x25B 0x25C   X X X X X
0x260 0x261 0x262 0x263 0x264   X X X X X
0x268 0x269 0x26A 0x26B 0x26C   X X X D X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x258 | `roof_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x259 | `roof` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25A | (2, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x25B | (3, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x25C | `roof_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x260 | `col_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x261 | `col` | `X` | `MB_NORMAL` | COVERED |  |
| 0x262 | `gap` | `X` | `MB_NORMAL` | COVERED |  |
| 0x263 | (3, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x264 | `col_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x268 | `base_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x269 | `base_col` | `X` | `MB_NORMAL` | COVERED |  |
| 0x26A | `base_gap` | `X` | `MB_NORMAL` | COVERED |  |
| 0x26B | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x26C | `base_R` | `X` | `MB_NORMAL` | COVERED |  |

### The sanctuary of Artemis Orthia

`orthia`, 3 wide by 4 tall. Orthia's little temple on the Eurotas's marshy bank, among willows: an old gabled front of plain limestone, two columns before a dark doorway, an altar on the steps where the cheese game is played (Kleta, the priestess). `door` is `MB_NON_ANIMATED_DOOR`; `altar` (impassable) takes the bg event. Stands on grass (the bottom row borrows it).

```text
ids                    walk
0x25D 0x25E 0x25F   X X X
0x265 0x266 0x267   X X X
0x26D 0x26E 0x26F   X D X
0x275 0x276 0x277   X X .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x25D | `pediment_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x25E | `pediment` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x25F | `pediment_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x265 | `cella_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x266 | `cella` | `X` | `MB_NORMAL` | COVERED |  |
| 0x267 | `cella_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x26D | `front_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x26E | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x26F | `front_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x275 | `step_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x276 | `altar` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x277 | `step_R` | `.` | `MB_NORMAL` | COVERED | grass |

### The chained Enyalios

`enyalios`, 1 wide by 2 tall. The bronze war god in the agora, his ankles bound in bronze fetters so War will never leave Lakonia, a fresh garland hung on his chain (an object). `top` (his helmet and spear, drawn over the player) over `base` (his fettered legs on a plinth; impassable, the bg event). On borrowed path.

```text
ids        walk
0x22F   T
0x237   X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x22F | `top` | `T` | `MB_NORMAL` | SPLIT | path |
| 0x237 | `base` | `X` | `MB_NORMAL` | COVERED | path |

### A small burial plot

`burial`, 3 wide by 2 tall. A low kerb of stones round a patch of grass, two small rounded stelai and a row of field stones: beside Lampito's house (her two children; fragment 8's widow keeps another). Impassable. On borrowed grass; the middle `T` and `B` repeat to widen it.

```text
ids                    walk
0x270 0x271 0x272   X X X
0x278 0x279 0x27A   X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x270 | `TL` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x271 | `T` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x272 | `TR` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x278 | `BL` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x279 | `B` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x27A | `BR` | `X` | `MB_NORMAL` | COVERED | grass |

### The rope across the Mani road

`rope`, 3 wide by 1 tall. Route 31's closed road south: a rope slung between two posts with a strip of red cloth tied in the middle (`post_L` `rope` `post_R`, on borrowed path; repeat `rope` for a wider road). Put an aethos stele (`0x003`) beside it as the sign. Impassable until the post-game.

```text
ids                    walk
0x27B 0x27C 0x27D   X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x27B | `post_L` | `X` | `MB_NORMAL` | COVERED | path |
| 0x27C | `rope` | `X` | `MB_NORMAL` | COVERED | path |
| 0x27D | `post_R` | `X` | `MB_NORMAL` | COVERED | path |

### House fronts

Every house is a home (MAP_DESIGN.md §2), so each front has a door. These are arrangements of the `house` kit's parts and cost no metatiles of their own; mix the parts for more (`front(tileset, key)` in `lakonia_tiles.py` returns the ids). Walk: every house cell is `X` except its door (`D`).

**A plain house** (`house`): most Lakonian households.

```text
ids                    walk
0x203 0x204 0x205   X X X
0x210 0x20F 0x212   X X X
0x218 0x21B 0x21A   X D X
```

**A wider house round its yard** (`house_wide`): Chilon's, Lichas's.

```text
ids                          walk
0x200 0x201 0x201 0x202   X X X X
0x208 0x20B 0x209 0x20A   X X X X
0x210 0x20F 0x211 0x212   X X X X
0x217 0x219 0x21B 0x21A   X X D X
```

**Lampito's house: a shield over the door** (`lampito`): Rhea (Lampito) and Kleon; the burial plot stands beside it.

```text
ids                          walk
0x203 0x206 0x204 0x205   X X X X
0x210 0x213 0x214 0x212   X X X X
0x218 0x21B 0x21D 0x21A   X D X X
```

**A low house, one room** (`low_house`): Gylippos's, the poorest.

```text
ids                    walk
0x203 0x204 0x205   X X X
0x21F 0x21B 0x21A   X D X
```

**The syssition, the mess hall: long, low, no windows** (`syssition`): Dexippos the cook; the smoke hole over the cauldron.

```text
ids                                      walk
0x203 0x204 0x207 0x204 0x204 0x205   X X X X X X
0x218 0x219 0x21F 0x21B 0x219 0x21A   X X X D X X
```

**The agoge's barracks, under reed thatch** (`barracks`): Archidamos and his herd of boys.

```text
ids                                      walk
0x20C 0x20D 0x20D 0x20D 0x20D 0x20E   X X X X X X
0x210 0x215 0x216 0x211 0x215 0x212   X X X X X X
0x21E 0x21C 0x219 0x21B 0x21C 0x21A   X X X D X X
```

**The Lesche, the elders' hall, with its porch** (`lesche`): the elders; the Augur on its roof.

```text
ids                                walk
0x200 0x201 0x201 0x201 0x202   X X X X X
0x208 0x209 0x209 0x209 0x20A   X X X X X
0x220 0x221 0x222 0x221 0x223   X X D X X
```

## Yards and the ring

### Beaten sand (the yards, the agoge's yard), soft-edged

`yard`, 8 wide by 6 tall. The beaten sand of house yards and the agoge's great yard, on borrowed grass, as all 47 soft-edge shapes (kythera_lib.blob_key gives a cell's key from a mask). Walkable. The full interior is `1|11111111`; the battle-school ring stands on it.

Shape keys (`blob_key`) and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x288 |
| `1|00000010` | 0x289 |
| `1|00001000` | 0x28A |
| `1|00001010` | 0x28B |
| `1|00001110` | 0x28C |
| `1|00100000` | 0x28D |
| `1|00100010` | 0x28E |
| `1|00101000` | 0x28F |
| `1|00101010` | 0x290 |
| `1|00101110` | 0x291 |
| `1|00111000` | 0x292 |
| `1|00111010` | 0x293 |
| `1|00111110` | 0x294 |
| `1|10000000` | 0x295 |
| `1|10000010` | 0x296 |
| `1|10000011` | 0x297 |
| `1|10001000` | 0x298 |
| `1|10001010` | 0x299 |
| `1|10001011` | 0x29A |
| `1|10001110` | 0x29B |
| `1|10001111` | 0x29C |
| `1|10100000` | 0x29D |
| `1|10100010` | 0x29E |
| `1|10100011` | 0x29F |
| `1|10101000` | 0x2A0 |
| `1|10101010` | 0x2A1 |
| `1|10101011` | 0x2A2 |
| `1|10101110` | 0x2A3 |
| `1|10101111` | 0x2A4 |
| `1|10111000` | 0x2A5 |
| `1|10111010` | 0x2A6 |
| `1|10111011` | 0x2A7 |
| `1|10111110` | 0x2A8 |
| `1|10111111` | 0x2A9 |
| `1|11100000` | 0x2AA |
| `1|11100010` | 0x2AB |
| `1|11100011` | 0x2AC |
| `1|11101000` | 0x2AD |
| `1|11101010` | 0x2AE |
| `1|11101011` | 0x2AF |
| `1|11101110` | 0x2B0 |
| `1|11101111` | 0x2B1 |
| `1|11111000` | 0x2B2 |
| `1|11111010` | 0x2B3 |
| `1|11111011` | 0x2B4 |
| `1|11111110` | 0x2B5 |
| `1|11111111` | 0x2B6 |

Every shape cell: walk `.`, `MB_NORMAL`.

### The battle-school ring

`ring`, 9 wide by 9 tall. The agoge's ring (beat III-5I): a round floor of raked sand 7 cells across in a low stone wall the cadets sit on, 9 x 9 cells in all, standing on the yard's beaten sand (its corners meet `yard`'s interior exactly). Its gap is the south middle cell (`gap`, the coord trigger); `center` is the middle of the floor. Wall cells are impassable; seat the cadets on them.

```text
ids                                                        walk
0x2B8 0x2B9 0x2BA 0x2BB 0x2BC 0x2BD 0x2BE 0x2BF 0x300   . . X X X X X . .
0x2C0 0x2C1 0x2C2 0x2C3 0x2C4 0x2C5 0x2C6 0x2C7 0x308   . X . . . . . X .
0x2C8 0x2C9 0x2CA 0x2CB 0x2CC 0x2CD 0x2CE 0x2CF 0x310   X . . . . . . . X
0x2D0 0x2D1 0x2D2 0x2D3 0x2D4 0x2D5 0x2D6 0x2D7 0x318   X . . . . . . . X
0x2D8 0x2D9 0x2DA 0x2DB 0x2DC 0x2DD 0x2DE 0x2DF 0x320   X . . . . . . . X
0x2E0 0x2E1 0x2E2 0x2E3 0x2E4 0x2E5 0x2E6 0x2E7 0x328   X . . . . . . . X
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC 0x2ED 0x2EE 0x2EF 0x330   X . . . . . . . X
0x2F0 0x2F1 0x2F2 0x2F3 0x2F4 0x2F5 0x2F6 0x2F7 0x338   . X . . . . . X .
0x2F8 0x2F9 0x2FA 0x2FB 0x2FC 0x2FD 0x2FE 0x2FF 0x340   . X X X . X X X .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2B8 | `NW` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2B9 | (1, 0) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2BA | (2, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2BB | (3, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2BC | `N` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2BD | (5, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2BE | (6, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2BF | (7, 0) | `.` | `MB_NORMAL` | COVERED |  |
| 0x300 | (8, 0) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C0 | (0, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C1 | (1, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C2 | (2, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C3 | (3, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C4 | (4, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C5 | (5, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C6 | (6, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C7 | (7, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x308 | (8, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C8 | (0, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C9 | (1, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2CA | (2, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2CB | (3, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2CC | (4, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2CD | (5, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2CE | (6, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2CF | (7, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x310 | (8, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2D0 | (0, 3) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2D1 | (1, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2D2 | (2, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2D3 | (3, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2D4 | (4, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2D5 | (5, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2D6 | (6, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2D7 | (7, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x318 | (8, 3) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2D8 | `W` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2D9 | (1, 4) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2DA | (2, 4) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2DB | (3, 4) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2DC | `center` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2DD | (5, 4) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2DE | (6, 4) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2DF | (7, 4) | `.` | `MB_NORMAL` | COVERED |  |
| 0x320 | (8, 4) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2E0 | (0, 5) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2E1 | (1, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2E2 | (2, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2E3 | (3, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2E4 | (4, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2E5 | (5, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2E6 | (6, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2E7 | (7, 5) | `.` | `MB_NORMAL` | COVERED |  |
| 0x328 | (8, 5) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2E8 | (0, 6) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2E9 | (1, 6) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2EA | (2, 6) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2EB | (3, 6) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2EC | (4, 6) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2ED | (5, 6) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2EE | (6, 6) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2EF | (7, 6) | `.` | `MB_NORMAL` | COVERED |  |
| 0x330 | (8, 6) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2F0 | (0, 7) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2F1 | (1, 7) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2F2 | (2, 7) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2F3 | (3, 7) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2F4 | (4, 7) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2F5 | (5, 7) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2F6 | (6, 7) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2F7 | (7, 7) | `X` | `MB_NORMAL` | COVERED |  |
| 0x338 | (8, 7) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2F8 | (0, 8) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2F9 | (1, 8) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2FA | (2, 8) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2FB | (3, 8) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2FC | `gap` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2FD | (5, 8) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2FE | (6, 8) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2FF | (7, 8) | `X` | `MB_NORMAL` | COVERED |  |
| 0x340 | (8, 8) | `.` | `MB_NORMAL` | COVERED |  |

### The wrestling sands, a dug pit in a stone kerb

`sands`, 4 wide by 3 tall. The palaestra's wrestling sands: soft, dug, raked pale sand sunk in a low stone kerb, a 3 x 3 kit on borrowed grass (`TL` `T` `TR` / `L` `C` `R` / `BL` `B` `BR`; repeat the middles). `C_b` is the sand scuffed where two have wrestled; `T_gap` `B_gap` are the kerb's north and south runs with a step down into the pit. Walkable throughout (a Geogrip lives here by day).

```text
ids                          walk
0x301 0x302 0x303 0x304   . . . .
0x309 0x30A 0x30B 0x30C   . . . .
0x311 0x312 0x313 0x314   . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x301 | `TL` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x302 | `T` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x303 | `TR` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x304 | `T_gap` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x309 | `L` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x30A | `C` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x30B | `R` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x30C | `C_b` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x311 | `BL` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x312 | `B` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x313 | `BR` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x314 | `B_gap` | `.` | `MB_NORMAL` | COVERED | grass |

### The Sown Field: plough furrows (tall grass)

`sown`, 4 wide by 3 tall. The battle school's practice strip in the training fields: ploughed furrows running east-west with green shoots in them. `MB_TALL_GRASS` (cadets practice in it; on Sporadon days things come up in it). A 3 x 3 kit on borrowed grass: `TL` `T` `TR` / `L` `C` `R` / `BL` `B` `BR`; `C_b` is a variant interior, `C_teeth` a furrow with something white in it.

```text
ids                          walk
0x319 0x31A 0x31B 0x31C   G G G G
0x321 0x322 0x323 0x324   G G G G
0x329 0x32A 0x32B 0x32C   G G G .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x319 | `TL` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x31A | `T` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x31B | `TR` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x31C | `C_b` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x321 | `L` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x322 | `C` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x323 | `R` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x324 | `C_teeth` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x329 | `BL` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x32A | `B` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x32B | `BR` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x32C | (3, 2) | `.` | `MB_NORMAL` | COVERED | grass |

## The land

### Taygetos: the dark wall

`taygetos`, 8 wide by 3 tall. The mountain wall behind Lakonia, and the rock walls of the hill routes. Fill the mountain's body with `mass_00` `mass_10` / `mass_01` `mass_11`, a 2 x 2 block that tiles (put `mass_XY` at x % 2, y % 2; `mass_pine` breaks it up). A south-facing wall is `lip` over `face` over `foot`, the foot standing on grass (`_b` are variants to break a long run; `_L` `_R` end one); `pine_face` is a face with a black pine on a ledge. `side_E` / `side_W` run north-south down the mountain's east or west flank (with `side_E_foot` / `side_W_foot` where a flank meets a south face's foot row); `back` and `back_NW` `back_NE` finish a free-standing rock's north edge onto grass. `in_E` `in_W` turn a south face's lip into a flank. `gully` and `gully_foot` are a dry watercourse down the face. Loose pieces on grass: `boulder`, `boulders` (impassable), `scree` (walkable). All impassable except `scree`.

```text
ids                                                  walk
0x350 0x351 0x352 0x353 0x354 0x355 0x356 0x357   X X X X X X X X
0x358 0x359 0x35A 0x35B 0x35C 0x35D 0x35E 0x35F   X X X X X X X X
0x360 0x361 0x362 0x363 0x364 0x365 0x366 0x367   . . . . . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x350 | `mass_00` | `X` | `MB_NORMAL` | COVERED |  |
| 0x351 | `mass_10` | `X` | `MB_NORMAL` | COVERED |  |
| 0x352 | `mass_01` | `X` | `MB_NORMAL` | COVERED |  |
| 0x353 | `mass_11` | `X` | `MB_NORMAL` | COVERED |  |
| 0x354 | `mass_pine` | `X` | `MB_NORMAL` | COVERED |  |
| 0x355 | `lip` | `X` | `MB_NORMAL` | COVERED |  |
| 0x356 | `lip_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x357 | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x358 | `face_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x359 | `foot` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x35A | `foot_b` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x35B | `pine_face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x35C | `side_E` | `X` | `MB_NORMAL` | COVERED |  |
| 0x35D | `side_E_foot` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x35E | `in_E` | `X` | `MB_NORMAL` | COVERED |  |
| 0x35F | `boulder` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x360 | `scree` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x361 | (1, 2) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x362 | (2, 2) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x363 | (3, 2) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x364 | (4, 2) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x365 | (5, 2) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x366 | (6, 2) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x367 | (7, 2) | `.` | `MB_NORMAL` | COVERED | grass |

### Plane tree and apple trees

`plane`, 3 wide by 3 tall. The oriental plane (3 x 3), Lakonia's tree: a broad crown of maple-like leaves over a mottled pale trunk, on borrowed grass. Its top row is drawn over the player (`T`); the rest is impassable. (Kythera's painter: `kythera_land.trees`.)

```text
ids                    walk
0x368 0x369 0x36A   T T T
0x370 0x371 0x372   X X X
0x378 0x379 0x37A   X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x368 | `plane_00` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x369 | `plane_10` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x36A | `plane_20` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x370 | `plane_01` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x371 | `plane_11` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x372 | `plane_21` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x378 | `plane_02` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x379 | `plane_12` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x37A | `plane_22` | `X` | `MB_NORMAL` | COVERED | grass |

### A weeping willow

`willow`, 2 wide by 3 tall. Orthia's willows by the river: a weeping crown of long silvery fronds over a dark trunk, 2 x 3; the top row is drawn over the player, the rest is impassable. On borrowed grass.

```text
ids              walk
0x36B 0x36C   T T
0x373 0x374   X X
0x37B 0x37C   X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x36B | `TL` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x36C | `TR` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x373 | `ML` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x374 | `MR` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x37B | `BL` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x37C | `BR` | `X` | `MB_NORMAL` | COVERED | grass |

### Oleander

`oleander`, 3 wide by 1 tall. Pink oleander, the riverbank shrub: `bush`, and a two-cell thicket `thicket_L` `thicket_R`. Impassable, on borrowed grass. Poisonous; the goats know.

```text
ids                    walk
0x36D 0x36E 0x36F   X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x36D | `bush` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x36E | `thicket_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x36F | `thicket_R` | `X` | `MB_NORMAL` | COVERED | grass |

## Fresh water

### The Eurotas: green water, soft banks

`river`, 8 wide by 7 tall. The Eurotas, the Platanistas's moat and every stream: slow green water (animated) between soft grass banks with a fringe of reeds, as all 47 soft-edge shapes; kythera_lib.blob_key gives a cell's key from a water mask, and `1|11111111` is open water. Every cell is fresh water (`MB_POND_WATER`, surfable; fish from the bank). Extra open-water cells: `rock`, a flat rock the fisher stands on (impassable); `ford`, stepping stones across a side stream (walkable: lay a line of them); `tuft`, a clump of reeds in midstream (impassable).

Shape keys (`blob_key`) and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x388 |
| `1|00000010` | 0x389 |
| `1|00001000` | 0x38A |
| `1|00001010` | 0x38B |
| `1|00001110` | 0x38C |
| `1|00100000` | 0x38D |
| `1|00100010` | 0x38E |
| `1|00101000` | 0x38F |
| `1|00101010` | 0x390 |
| `1|00101110` | 0x391 |
| `1|00111000` | 0x392 |
| `1|00111010` | 0x393 |
| `1|00111110` | 0x394 |
| `1|10000000` | 0x395 |
| `1|10000010` | 0x396 |
| `1|10000011` | 0x397 |
| `1|10001000` | 0x398 |
| `1|10001010` | 0x399 |
| `1|10001011` | 0x39A |
| `1|10001110` | 0x39B |
| `1|10001111` | 0x39C |
| `1|10100000` | 0x39D |
| `1|10100010` | 0x39E |
| `1|10100011` | 0x39F |
| `1|10101000` | 0x3A0 |
| `1|10101010` | 0x3A1 |
| `1|10101011` | 0x3A2 |
| `1|10101110` | 0x3A3 |
| `1|10101111` | 0x3A4 |
| `1|10111000` | 0x3A5 |
| `1|10111010` | 0x3A6 |
| `1|10111011` | 0x3A7 |
| `1|10111110` | 0x3A8 |
| `1|10111111` | 0x3A9 |
| `1|11100000` | 0x3AA |
| `1|11100010` | 0x3AB |
| `1|11100011` | 0x3AC |
| `1|11101000` | 0x3AD |
| `1|11101010` | 0x3AE |
| `1|11101011` | 0x3AF |
| `1|11101110` | 0x3B0 |
| `1|11101111` | 0x3B1 |
| `1|11111000` | 0x3B2 |
| `1|11111010` | 0x3B3 |
| `1|11111011` | 0x3B4 |
| `1|11111110` | 0x3B5 |
| `1|11111111` | 0x3B6 |

Every shape cell: walk `P`, `MB_POND_WATER`.

Extra cells:

| Id | Piece | Walk | Behavior | Layer |
|---|---|---|---|---|
| 0x3B7 | `rock` | `X` | `MB_NORMAL` | COVERED |
| 0x3B8 | `ford` | `.` | `MB_NORMAL` | COVERED |
| 0x3B9 | `tuft` | `X` | `MB_NORMAL` | COVERED |

### The plain stone bridge, and footbridges

`bridge`, 3 wide by 2 tall. Lakonia's plain stone bridge over the Eurotas, east-west: `deck_W` `deck` `deck_E` (repeat `deck`) over its south face `face_W` `arch` `face_E` in the water. Deck walkable, face impassable.

```text
ids                    walk
0x3C0 0x3C1 0x3C2   . . .
0x3C8 0x3C9 0x3CA   X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x3C0 | `deck_W` | `.` | `MB_NORMAL` | COVERED |  |
| 0x3C1 | `deck` | `.` | `MB_NORMAL` | COVERED |  |
| 0x3C2 | `deck_E` | `.` | `MB_NORMAL` | COVERED |  |
| 0x3C8 | `face_W` | `X` | `MB_NORMAL` | COVERED |  |
| 0x3C9 | `arch` | `X` | `MB_NORMAL` | COVERED |  |
| 0x3CA | `face_E` | `X` | `MB_NORMAL` | COVERED |  |
