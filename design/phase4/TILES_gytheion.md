# gytheion tileset catalog

`gTileset_Gytheion` is Gytheion and the strait off Malea (Act III, Lakonia; SCRIPT.md Part 10). It serves Gytheion and Route 24 (the strait off Malea). Pair it with the `aethos` primary, which supplies the open grass, paths, sand, sea, olives, cypresses and stone pines.

**This file is generated.** `tools/ichor/art/lakonia_build.py gytheion` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/lakonia_*.py` (the plane tree is Kythera's), the palette plan, the water and the soft-edge autotiles in `lakonia_lib.py`.

| Image | Shows |
|---|---|
| [`img/gytheion_quay.png`](img/gytheion_quay.png) | A 240 x 160 screen of Gytheion's quay: the purple steps, the stall, the dye-works and its heaps (3x; `gytheion_quay_1x.png` is 1x) |
| [`img/gytheion_town.png`](img/gytheion_town.png) | Gytheion: the quay, the theater and its stage-building, the dye-works, the causeway to Kranai; the strait off Malea |
| [`img/gytheion_pieces.png`](img/gytheion_pieces.png) | Every structure on its ground |
| [`img/gytheion_sheet.png`](img/gytheion_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

![A 240 x 160 screen of Gytheion's quay: the purple steps, the stall, the dye-works and its heaps (3x; `gytheion_quay_1x.png` is 1x)](img/gytheion_quay.png)

It is one of the Lakonia family of secondaries; see [`TILES_lakonia.md`](TILES_lakonia.md) for why the art is split and which seams then need aethos-only strips.

**What comes from aethos (or elsewhere), not from here.** The quay's top and the lanes are aethos's limestone path, Elaphonisos's white sand and the beach are aethos sand edged with Kythera's surf (drawn once, in Kythera's painter), the open strait is aethos sea, and the fishing boats are Skandeia's (`kythera_harbor.kaiki`).

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet (harbor at 0x200, town at 0x270, coast at 0x2C0). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/lakonia_tiles.py` holds every
Lakonia-family catalog as a Python dict (`mid('gytheion', 'house', 'door')`, and
`blob_key(mask, x, y)` for the soft-edged pieces), and `build/gytheion/catalog.json` is
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

**Animations.** Porytiles animations in this tileset, driven by `InitTilesetAnim_PorytilesManaged_Gytheion` (`include/porytiles_generated/tilesets/gytheion/generated_anim_code.h`): `current`: the Malea current's streaks running west (4 frames); `steam`: the dye vats steaming (3 frames); `surf`: Kythera's surf, washing up and back on the shingle (3 frames). Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet. Borrowed sea and shallows keep aethos's own animations.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of seven color
groups, one per secondary palette (`lakonia_lib.GROUPS`), passed to Porytiles as packing
hints:

| Group | Use |
|---|---|
| purple | Gytheion's murex purple: stains, shell heaps, lead vats, on the quay's limestone |
| stone | Plain stone, plaster and clay roofs: houses, the stoa, stelai, bridges, the causeway |
| foam | Kythera's foam group: the surf on Gytheion's shingle and Elaphonisos's sand |
| terra | Kythera's timber and terracotta: the fishing boats |
| mount | Taygetos and the Skiritis: dark rock, scree, black pine; Malea's foam |
| deep | The drowned town under Route 24's turquoise shallows |
| wood | Timber and thatch: boardwalks, the stilt hut, racks, the barracks' roof, posts |

**Tile budget.** 497 of 504 tiles (248 metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.

## The harbor

### The curved stone quay

`quay`, 8 wide by 2 tall. Gytheion's quay (Skandeia's kit, drawn once). Its top is aethos's limestone path (0x1D9): pave the quay with it, and these edges finish it where its wall drops into the sea (each borrows aethos's sea). Named by where the sea is: `S` (sea south; `S_b` adds a drain, `ring_S` a bronze mooring ring), `N`, `E`, `W`; `out_SE` is the quay's rounded south-east corner (the sea round it), `in_SE` the inside of a bend (sea only to the south-east): the rounded corners make the quay curve. `steps_E` and `steps_S` go down into the water for boats (walkable). `N_plank` is the north edge with a ship's gangplank landing on it (a ship moored to the north, as the Euploia's plank comes down to it), `S_plank` the south edge with a plank going down to a boat (both walkable). Edge cells are otherwise impassable: the quay's walkable top ends on the path cell behind them.

```text
ids                                                  walk
0x200 0x201 0x202 0x203 0x204 0x205 0x206 0x207   X X X X X X X X
0x208 0x209 0x20A 0x20B 0x20C 0x20D 0x20E 0x20F   X X X X X X . .
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
| 0x20D | `ring_S` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x20E | `S_plank` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x20F | (7, 1) | `.` | `MB_NORMAL` | COVERED | sea |

### The purple quay: steps, stains, murex heaps

`quayside`, 7 wide by 3 tall. Gytheion's quay is aethos's limestone path with Skandeia's quay edges (the `quay` kit); these finish it in purple. `steps_S` `steps_E` `steps_W`: steps down into the sea (borrowed), stained purple where the dyers rinse their arms (walkable); `steps_SL` `steps_SR` are a stair two cells wide. `amphorae`: jars of brine for the shells (impassable). On borrowed path: `stain` `stain_b` (walkable), `drain` (a gutter running purple to the sea, impassable), `mooring` (a bollard, impassable), `bucket` (the fisherman's bronze helmet, bailing water; impassable), `basket` (a basket of live murex). Murex shell heaps behind the dye-works, gray like snow: `heap_*` (2 x 2) and `heap_small` (impassable); `shells` on path and `shells_sand` on sand (walkable, crushed shell). On the shingle beach (borrowed sand): `pebbles` `pebbles_b`, stained purple (walkable).

```text
ids                                            walk
0x210 0x211 0x212 0x213 0x214 0x215 0x216   . . . X . . .
0x218 0x219 0x21A 0x21B 0x21C 0x21D 0x21E   X X . X X X .
0x220 0x221 0x222 0x223 0x224 0x225 0x226   X X . . X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x210 | `steps_S` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x211 | `steps_E` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x212 | `steps_W` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x213 | `stain` | `X` | `MB_NORMAL` | COVERED | path |
| 0x214 | `stain_b` | `.` | `MB_NORMAL` | COVERED | path |
| 0x215 | `drain` | `.` | `MB_NORMAL` | COVERED | path |
| 0x216 | `steps_SL` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x218 | `heap_TL` | `X` | `MB_NORMAL` | COVERED | path |
| 0x219 | `heap_TR` | `X` | `MB_NORMAL` | COVERED | path |
| 0x21A | `shells` | `.` | `MB_NORMAL` | COVERED | path |
| 0x21B | `shells_sand` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x21C | `heap_small` | `X` | `MB_NORMAL` | COVERED | path |
| 0x21D | `mooring` | `X` | `MB_NORMAL` | COVERED | path |
| 0x21E | `steps_SR` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x220 | `heap_BL` | `X` | `MB_NORMAL` | COVERED | path |
| 0x221 | `heap_BR` | `X` | `MB_NORMAL` | COVERED | path |
| 0x222 | `pebbles` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x223 | `pebbles_b` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x224 | `bucket` | `X` | `MB_NORMAL` | SPLIT | path |
| 0x225 | `basket` | `X` | `MB_NORMAL` | COVERED | path |
| 0x226 | `amphorae` | `X` | `MB_NORMAL` | COVERED | path |

### The dye-works

`dyeworks`, 5 wide by 2 tall. Porphyris's dye-works on the shore: a long rough-stone shed under a clay-tile roof, its walls stained purple to the eaves, skeins of wool drying on a pole by the door, and its east end open to the sea, the lead vats glowing purple in the dark (`open`, `open_R`). `door` is `MB_NON_ANIMATED_DOOR`. Impassable otherwise. The heaps of shell go behind it.

```text
ids                                walk
0x228 0x229 0x22A 0x22B 0x22C   X X X X X
0x230 0x231 0x232 0x233 0x234   X X D X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x228 | `roof_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x229 | `roof` | `X` | `MB_NORMAL` | COVERED |  |
| 0x22A | `roof_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x22B | `roof_open` | `X` | `MB_NORMAL` | COVERED |  |
| 0x22C | `roof_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x230 | `wall_L` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x231 | `skeins` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x232 | `door` | `D` | `MB_NON_ANIMATED_DOOR` | SPLIT |  |
| 0x233 | `open` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x234 | `open_R` | `X` | `MB_NORMAL` | SPLIT |  |

### Lead vats, a skein rack, nets drying

`vats`, 5 wide by 1 tall. On borrowed path. `vat` `vat_b`: a great lead vat of purple steaming over its fire (animated steam), outside the dye-works. `skein_rack`: dyed wool drying on a frame. `nets_L` `nets_R`: nets hung to dry on poles, the stall's racks and the fishers'. All impassable.

```text
ids                                walk
0x238 0x239 0x23A 0x23B 0x23C   X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x238 | `vat` | `X` | `MB_NORMAL` | COVERED | path |
| 0x239 | `vat_b` | `X` | `MB_NORMAL` | COVERED | path |
| 0x23A | `skein_rack` | `X` | `MB_NORMAL` | COVERED | path |
| 0x23B | `nets_L` | `X` | `MB_NORMAL` | COVERED | path |
| 0x23C | `nets_R` | `X` | `MB_NORMAL` | COVERED | path |

### The stall under the purple awning

`stall`, 3 wide by 2 tall. Gytheion's one shop (the hamlet's Agora): a stall on the quay under a striped purple awning (drawn over the player), its counter of planks with stock on racks of drying nets. Talk to the stallkeeper across the counter. On borrowed path.

```text
ids                    walk
0x22D 0x22E 0x22F   T T T
0x235 0x236 0x237   X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x22D | `awning_L` | `T` | `MB_NORMAL` | SPLIT | path |
| 0x22E | `awning` | `T` | `MB_NORMAL` | SPLIT | path |
| 0x22F | `awning_R` | `T` | `MB_NORMAL` | SPLIT | path |
| 0x235 | `counter_L` | `X` | `MB_NORMAL` | COVERED | path |
| 0x236 | `counter` | `X` | `MB_NORMAL` | COVERED | path |
| 0x237 | `counter_R` | `X` | `MB_NORMAL` | COVERED | path |

### The causeway to Kranai

`kranai_way`, 4 wide by 2 tall. The low stone causeway from Gytheion's beach out to the islet of Kranai, a cell wide, over the borrowed sea, rough blocks with the sea foaming against them: east-west `H` (`H_b`; `H_W` `H_E` meet sand), north-south `V` (`V_b`; `V_N` `V_S` meet sand). Walkable.

```text
ids                          walk
0x240 0x241 0x242 0x243   . . . .
0x248 0x249 0x24A 0x24B   . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x240 | `H` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x241 | `H_b` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x242 | `H_W` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x243 | `H_E` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x248 | `V` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x249 | `V_b` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x24A | `V_N` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x24B | `V_S` | `.` | `MB_NORMAL` | COVERED | sea |

### The shrine on Kranai

`kranai_shrine`, 3 wide by 2 tall. Klymene's little whitewashed shrine on Kranai, where Paris and Helen spent their first night: a gabled roof of gray slabs, whitewash gone pink at the foot with old purple, a dark doorway (`door`, `MB_NON_ANIMATED_DOOR`). The roof row stands on borrowed sand.

```text
ids                    walk
0x23D 0x23E 0x23F   X X X
0x245 0x246 0x247   X D X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x23D | `roof_L` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x23E | `roof` | `X` | `MB_NORMAL` | COVERED |  |
| 0x23F | `roof_R` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x245 | `wall_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x246 | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x247 | `wall_R` | `X` | `MB_NORMAL` | COVERED |  |

### A fishing boat, afloat and beached

`kaiki`, 6 wide by 2 tall. A kaiki, the island's fishing boat, bow to the east, 3 x 2 each: `afloat` on borrowed sea, `beached` drawn up on the sand (borrowed sand). Impassable.

```text
ids                                      walk
0x250 0x251 0x252 0x253 0x254 0x255   X X X X X X
0x258 0x259 0x25A 0x25B 0x25C 0x25D   X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x250 | `afloat` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x251 | (1, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x252 | (2, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x253 | `beached` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x254 | (4, 0) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x255 | (5, 0) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x258 | (0, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x259 | (1, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x25A | (2, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x25B | (3, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x25C | (4, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x25D | (5, 1) | `X` | `MB_NORMAL` | COVERED | sand |

## Town

### Plain flat-roofed houses

`house`, 8 wide by 2 tall. Lakonian houses: tan lime plaster over mudbrick on a rubble footing, flat roofs of beaten clay, timber doors stained red, no ornament. Build a front from rows: a roof (`R_L` `R_M` `R_R` one row deep; or `RB_*` over `RF_*` for a deeper house), an optional upper wall (`U_*`), and the ground floor (`G_*` with the `door`). A house with no upper wall is low, one room. `R_jar` `RF_jar` `R_brush` put a jar or a heap of brushwood on a roof; `R_vent` is the syssition's smoke hole. `T_L` `T_M` `T_R` are reed thatch, for the barracks. `U_window`, `U_worn` (plaster fallen off the brick), `U_shield` (a bronze shield with the lambda hung over Lampito's door), `U_cloak` (a red cloak on a peg), `U_list` (the herd's names painted by the barracks door). `G_window`, `G_open` (an open doorway, dark), `G_bench` (a stone bench), `G_jar` (a pithos), `G_spears` (a rack of practice spears), `G_wood` (stacked firewood), `G_worn`. The Lesche's porch: `P_L` `P_col` `P_gap` `P_R` with `door_porch` at its back. Every cell is impassable but the doors (`MB_NON_ANIMATED_DOOR`). The fronts below arrange them.

```text
ids                                                  walk
0x270 0x271 0x272 0x273 0x274 0x275 0x276 0x277   X X X X X X X X
0x278 0x279 0x27A 0x27B 0x27C 0x27D 0x27E 0x27F   X X X D X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x270 | `R_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x271 | `R_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x272 | `R_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x273 | `R_brush` | `X` | `MB_NORMAL` | COVERED |  |
| 0x274 | `U_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x275 | `U_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x276 | `U_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x277 | `U_window` | `X` | `MB_NORMAL` | COVERED |  |
| 0x278 | `G_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x279 | `G_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x27A | `G_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x27B | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x27C | `G_jar` | `X` | `MB_NORMAL` | COVERED |  |
| 0x27D | `G_wood` | `X` | `MB_NORMAL` | COVERED |  |
| 0x27E | (6, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x27F | (7, 1) | `X` | `MB_NORMAL` | COVERED |  |

### The stage-building: Gytheion's Asclepeion

`skene`, 6 wide by 2 tall. The theater's stage-building, its back to the town, which is Gytheion's Asclepeion: a long low building of plastered stone under a flat roof, a painted panel (`pinax`) and the rod of Asclepius (`rod`) beside the door (`door`, `MB_NON_ANIMATED_DOOR`; Fly lands outside it). Place it across the theater's open side. Impassable but the door.

```text
ids                                      walk
0x280 0x281 0x282 0x283 0x284 0x285   X X X X X X
0x288 0x289 0x28A 0x28B 0x28C 0x28D   X X X D X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x280 | `roof_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x281 | `roof` | `X` | `MB_NORMAL` | COVERED |  |
| 0x282 | (2, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x283 | (3, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x284 | (4, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x285 | `roof_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x288 | `wall_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x289 | `pinax` | `X` | `MB_NORMAL` | COVERED |  |
| 0x28A | `wall` | `X` | `MB_NORMAL` | COVERED |  |
| 0x28B | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x28C | `rod` | `X` | `MB_NORMAL` | SPLIT |  |
| 0x28D | `wall_R` | `X` | `MB_NORMAL` | COVERED |  |

### The little theater on the hill

`theater`, 7 wide by 4 tall. Gytheion's theater, cut into the hill behind the hamlet: curved rows of stone seats climbing the slope round the half-moon of the orchestra, 7 x 4, the hill's grass above (mirror-symmetric, so it costs half). Walk the rows (the patients sit in the sun in the front ones); the outer cells and the top are impassable. The stage-building, the Asclepeion, stands across its open south side: `skene`.

```text
ids                                            walk
0x290 0x291 0x292 0x293 0x294 0x295 0x296   X X X X X X X
0x298 0x299 0x29A 0x29B 0x29C 0x29D 0x29E   X . . . . . X
0x2A0 0x2A1 0x2A2 0x2A3 0x2A4 0x2A5 0x2A6   X . . . . . X
0x2A8 0x2A9 0x2AA 0x2AB 0x2AC 0x2AD 0x2AE   X . . . . . X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x290 | (0, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x291 | (1, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x292 | (2, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x293 | `top` | `X` | `MB_NORMAL` | COVERED |  |
| 0x294 | (4, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x295 | (5, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x296 | (6, 0) | `X` | `MB_NORMAL` | COVERED |  |
| 0x298 | (0, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x299 | (1, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x29A | (2, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x29B | (3, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x29C | (4, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x29D | (5, 1) | `.` | `MB_NORMAL` | COVERED |  |
| 0x29E | (6, 1) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A0 | (0, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A1 | (1, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A2 | (2, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A3 | `seat` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A4 | (4, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A5 | (5, 2) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A6 | (6, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A8 | `west` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A9 | (1, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2AA | (2, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2AB | `orchestra` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2AC | (4, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2AD | (5, 3) | `.` | `MB_NORMAL` | COVERED |  |
| 0x2AE | `east` | `X` | `MB_NORMAL` | COVERED |  |

### House fronts

Every house is a home (MAP_DESIGN.md §2), so each front has a door. These are arrangements of the `house` kit's parts and cost no metatiles of their own; mix the parts for more (`front(tileset, key)` in `lakonia_tiles.py` returns the ids). Walk: every house cell is `X` except its door (`D`).

**A plain house** (`house`): most Lakonian households.

```text
ids                    walk
0x270 0x271 0x272   X X X
0x274 0x277 0x276   X X X
0x278 0x27B 0x27A   X D X
```

**A low house, one room** (`low_house`): Gylippos's, the poorest.

```text
ids                    walk
0x270 0x271 0x272   X X X
0x27D 0x27B 0x27A   X D X
```

## The coast

### Foam-edged surf

`surf`, 8 wide by 2 tall. Where Kythera's sand meets the sea. Each cell borrows aethos's animated sea and draws the sand to the waterline, a rim of turquoise shallows and the foam, which washes up and back (the `surf` animation, 3 frames). Pieces are named by where the sea is: `S` (sand north, sea south; `S2` is the same with a deeper bite, to break up a long beach), `N`, `E`, `W`; `out_NW` is the south-east tip of a sand spit (sand to the north-west, sea round it), and so on; `in_SE` is a cove's corner, sea only to the south-east. The sand above meets aethos sand (0x124) exactly; the sea below meets aethos sea (0x170). Every cell is `MB_OCEAN_WATER`, like aethos's own beach edges: surf onto it, walk on the sand beside it.

```text
ids                                                  walk
0x2C0 0x2C1 0x2C2 0x2C3 0x2C4 0x2C5 0x2C6 0x2C7   W W W W W W W W
0x2C8 0x2C9 0x2CA 0x2CB 0x2CC 0x2CD 0x2CE 0x2CF   W W W W W W W W
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2C0 | `S` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2C1 | `S2` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2C2 | `N` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2C3 | `E` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2C4 | `W` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2C5 | `out_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2C6 | `out_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2C7 | `out_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2C8 | `out_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2C9 | `in_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2CA | `in_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2CB | `in_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2CC | `in_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2CD | (5, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2CE | (6, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2CF | (7, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |

### The Malea current

`current`, 2 wide by 1 tall. The fast current under Cape Malea's cliffs that carries surfers west (`MB_WESTWARD_CURRENT`): streaks of foam on the borrowed sea, racing west (animated). Lay a band of `current` `current_b` along the cliffs.

```text
ids              walk
0x2D0 0x2D1   W W
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2D0 | `current` | `W` | `MB_WESTWARD_CURRENT` | COVERED | sea |
| 0x2D1 | `current_b` | `W` | `MB_WESTWARD_CURRENT` | COVERED | sea |

### The drowned town off Elaphonisos

`drowned`, 4 wide by 3 tall. Under the clear turquoise shallows off Elaphonisos's north shore: streets, house walls and a square with a well in it, seen through the water (the post-game's Nereid Pearl dives here). Lay them over borrowed shallows like a plan of a town: `wall_H`, `wall_V`, corners `NW` `NE` `SW` `SE` (named for the corner of the house they make), `door_H` (a wall with a doorway), `well`, `street` and `square` (paving), `column` (a stump), `rubble`. Every cell is surfable sea (`MB_OCEAN_WATER`).

```text
ids                          walk
0x2D2 0x2D3 0x2D4 0x2D5   W W W W
0x2DA 0x2DB 0x2DC 0x2DD   W W W W
0x2E2 0x2E3 0x2E4 0x2E5   W W W W
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2D2 | `wall_H` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2D3 | `wall_V` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2D4 | `NW` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2D5 | `NE` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2DA | `SW` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2DB | `SE` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2DC | `door_H` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2DD | `well` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2E2 | `street` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2E3 | `square` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2E4 | `column` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |
| 0x2E5 | `rubble` | `W` | `MB_OCEAN_WATER` | COVERED | shallow |

### Taygetos: the dark wall

`taygetos`, 8 wide by 2 tall. Cape Malea's cliffs on Route 24's north side, Taygetos's dark rock (see `TILES_lakonia.md`): fill the cape with `mass_*` (2 x 2, at x % 2, y % 2), edge it with `lip` over `face` over `foot_sea`, the face dropping into the sea with foam at its foot (`_b` vary a run); `side_E` runs down the cape's east flank; `stack` is a dark rock in the sea. Impassable.

```text
ids                                                  walk
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC 0x2ED 0x2EE 0x2EF   X X X X X X X X
0x2F0 0x2F1 0x2F2 0x2F3 0x2F4 0x2F5 0x2F6 0x2F7   X X X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2E8 | `mass_00` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2E9 | `mass_10` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2EA | `mass_01` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2EB | `mass_11` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2EC | `lip` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2ED | `lip_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2EE | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2EF | `face_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2F0 | `foot_sea` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x2F1 | `foot_sea_b` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x2F2 | `side_E` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2F3 | `stack` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x2F4 | (4, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x2F5 | (5, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x2F6 | (6, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x2F7 | (7, 1) | `X` | `MB_NORMAL` | COVERED | sea |
