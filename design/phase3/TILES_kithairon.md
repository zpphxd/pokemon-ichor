# The Kithairon crossing's tilesets

The road north from Eleusa over Mt. Kithairon to Thyrsa: vine terraces and dry stone,
black firs, grey rock, ivy, the border fort of Eleutherai with its Cyclopean walls,
the god's roofless temple, the maenads' mountain, and on the Asopos plain below, the
Kronia: red-and-cream awnings, bread, gold cloth. Three secondaries on the `aethos`
primary, drawn by one set of painters:

| Tileset | Maps |
|---|---|
| `gTileset_Kithairon` | Route 6, Eleutherai, Mt. Kithairon |
| `gTileset_Kronia` | Route 7 and the Kronia grounds |
| `gTileset_KithaironCave` | Antiope's cave |

**This catalog is generated** by `tools/ichor/art/kithairon_build.py` (painters:
`kithairon_ground.py`, `_trees.py`, `_stone.py`, `_vines.py`, `_houses.py`, `_camp.py`;
palettes and the soft-shape engine in `kithairon_lib.py`). The render-and-critique
passes at the end are written by hand and kept across rebuilds.

## How it fits together

**Why three sets, not one.** BUILD.md asked for one `kithairon` secondary for all four
outdoor maps, so their seams need no aethos-only strip. Everything the crossing needs
came to about 700 tiles against a secondary's 504, so the art is split, and the seam
still needs no aethos-only strip: Kithairon and Kronia both begin with the same **core**
section (soft ground, firs and the oak, crag detail, stones and markers), painted from
the same pixels and packed at the same metatile ids. The game draws a connected
neighbor with the tilesets of the map the player stands on, and a core metatile looks
the same in either set. The map builder keeps the six rows either side of the
Mt. Kithairon / Route 7 seam to core and aethos metatiles. The cave is its own small set.

**Place pieces by key and cell name** from `build/kithairon/<dir>/catalog.json`, never by
raw id (`tools/ichor/maps/kithairon.py` does). Ids below are the current build's.

**Soft ground.** `tall`, `path`, `crag`, `water` and `cave` hold one piece per blob
shape key: `1|` then the cell's neighbors N NE E SE S SW W NW, `1` in the region and `0`
not, a diagonal counting only when both its sides are in. `kithairon_lib.blob_key`
computes it. The map builder lists the keys its maps use in
`tools/ichor/art/kithairon_shapes.json` (`kithairon.py --shapes`), and only those are drawn.

- `crag` is Kithairon's grey limestone: a weathered top, and a 14 px face with strata
  along every south edge, so a crag reads as a rise with a cliff below it. Scatter
  `crag_detail`'s interior cells through a big crag; its south-face cells carry ivy,
  the marked ivy of the Thyrsus walls and a cave mouth.
- `water` is aethos's animated sea under a pebbly bank with reeds: MB_POND_WATER,
  surfable and fishable.

**Walk codes** in the grids: `X` blocks, `.` walkable, `T` walkable and drawn over the
player, `G` tall grass, `D` a door (MB_NON_ANIMATED_DOOR: put the warp there).

**Borrowed ground.** Cells marked *grass*, *path*, *sea* or *tall* draw no ground of
their own: the build points their bottom tiles at aethos's grass (`0x001`), road
(`0x1D9`), animated sea (`0x170`) or tall grass (`0x00D`). Rebuild these sets whenever
aethos is repainted.

**Palettes.** Seven groups, one per secondary palette; every 8x8 tile draws from one.

| Group | Use |
|---|---|
| field | tall grass, the road, its edges |
| rock | crags, the cave, boulders, ivy and the marked ivy, shrines, the herm |
| tree | firs, oaks |
| vine | trellises, the old vines, the wine-cart |
| house | Eleusa's house kit, verbatim |
| stone | Cyclopean walls, the temple, the wine press, troughs |
| camp | the Kronia's awnings, tables, tents, stage, banner, oven; the brazier |

**Scripted swaps** (`include/constants/metatile_labels.h`): `METATILE_Kithairon_OldVines`,
`_OldVines_B` and `_OldVines_Stumps` (the vines across Route 6, beat 26), and
`METATILE_KithaironCave_Brazier_ColdTop`, `_Cold`, `_LitTop`, `_Lit`.

## Budget

| Tileset | Tiles | Metatiles |
|---|---|---|
| `gTileset_Kithairon` | 480 of 504 | 248 of 512 |
| `gTileset_Kronia` | 480 of 504 | 256 of 512 |
| `gTileset_KithaironPass` | 405 of 504 | 240 of 512 |
| `gTileset_KithaironCave` | 62 of 504 | 48 of 512 |

## `gTileset_Kithairon`: Route 6, Eleutherai and Mt. Kithairon

![sheet](img/tiles_kithairon_sheet.png)

### Core: shared by Kithairon and Kronia at the same ids

#### Tall grass with soft edges

`tall`, 8 wide by 3 tall. Barley tall grass on aethos grass, cut from one field so any outline works (agros's painter, as on Route 1). MB_TALL_GRASS throughout. Names are blob shape keys (`1|NNEESESSWWNW`).

23 shapes, from 0x200; the interior `1|11111111` is 0x200.

#### The road with soft edges

`path`, 8 wide by 3 tall. The limestone road and its goat-track branches, scalloped where they meet the grass (agros's painter). Names are blob shape keys.

24 shapes, from 0x218; the interior `1|11111111` is 0x218.

#### Black fir (2 x 3 with its spire)

`fir`, 2 wide by 3 tall. A black fir. The top row is its spire over the grass of the row above: walkable, drawn over the player. Rows 1-2 block.

```text
0x230 0x231   T T
0x238 0x239   X X
0x240 0x241   X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### Slim fir (2 x 3 with its spire)

`fir_b`, 2 wide by 3 tall. A black fir. The top row is its spire over the grass of the row above: walkable, drawn over the player. Rows 1-2 block.

```text
0x232 0x233   T T
0x23A 0x23B   X X
0x242 0x243   X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### A fir's base with the next fir's spire over it

`fir_stack`, 2 wide by 1 tall. Between two firs in a column: the upper fir's base row, the lower fir's spire over it. Blocks.

```text
0x234 0x235   X X
```

Borrowed ground: grass at 0,0, 1,0.

#### A fir's base with the next fir's spire over it

`fir_stack_b`, 2 wide by 1 tall. Between two firs in a column: the upper fir's base row, the lower fir's spire over it. Blocks.

```text
0x236 0x237   X X
```

Borrowed ground: grass at 0,0, 1,0.

#### Young fir (1 x 2)

`fir_young`, 1 wide by 2 tall. A sapling fir for gaps at the woods' edge. Its top half is drawn over the player.

```text
0x23C   T
0x244   X
```

Borrowed ground: grass at 0,0, 0,1.

#### Scrub oak (2 x 2)

`oak`, 2 wide by 2 tall. A low, wide kermes oak of the mountain's lower slopes.

```text
0x23D 0x23E   X X
0x245 0x246   X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1.

#### Stones of the road: the herm, boundary stones, scree

`markers`, 4 wide by 2 tall. On borrowed grass. `herm_top` over `herm`: the great herm, hung with ivy. `boundary` a worn boundary stone, `boulder` a grey rock, `scree`/`scree_b` loose stones (walkable), `dig` turned earth on grass (walkable).

```text
0x248 0x249 0x24A 0x24B   T . . X
0x250 0x251 0x252 0x253   X X . .
```

Pieces: `herm_top` 0x248, `dig` 0x249, `scree_b` 0x24A, `boulder` 0x24B, `herm` 0x250, `boundary` 0x251, `scree` 0x252.

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1, 3,0, 3,1.

#### Black fir (2 x 3 with its spire), in the woods' shade

`fir_shade`, 2 wide by 3 tall. The same as `fir`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir`'s top row there.

```text
0x24C 0x24D   T T
0x254 0x255   X X
0x25C 0x25D   X X
```

Borrowed ground: shade at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### Slim fir (2 x 3 with its spire), in the woods' shade

`fir_b_shade`, 2 wide by 3 tall. The same as `fir_b`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_b`'s top row there.

```text
0x24E 0x24F   T T
0x256 0x257   X X
0x25E 0x25F   X X
```

Borrowed ground: shade at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### A fir's base with the next fir's spire over it, in the woods' shade

`fir_stack_shade`, 2 wide by 1 tall. The same as `fir_stack`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_stack`'s top row there.

```text
0x258 0x259   X X
```

Borrowed ground: shade at 0,0, 1,0.

#### A fir's base with the next fir's spire over it, in the woods' shade

`fir_stack_b_shade`, 2 wide by 1 tall. The same as `fir_stack_b`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_stack_b`'s top row there.

```text
0x25A 0x25B   X X
```

Borrowed ground: shade at 0,0, 1,0.

#### Young fir (1 x 2), in the woods' shade

`fir_young_shade`, 1 wide by 2 tall. The same as `fir_young`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_young`'s top row there.

```text
0x23F   T
0x247   X
```

Borrowed ground: shade at 0,0, 0,1.

#### Scrub oak (2 x 2), in the woods' shade

`oak_shade`, 2 wide by 2 tall. The same as `oak`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `oak`'s top row there.

```text
0x260 0x261   X X
0x268 0x269   X X
```

Borrowed ground: shade at 0,0, 0,1, 1,0, 1,1.

#### Meadow flowers and a tussock

`meadow`, 3 wide by 1 tall. Walkable. Scatter through open grass with aethos's red anemones (0x004): `white` narcissus, `yellow` mountain crocus, `tuft` a tussock.

```text
0x262 0x263 0x264   . . .
```

Pieces: `white` 0x262, `yellow` 0x263, `tuft` 0x264.

Borrowed ground: grass at 0,0, 1,0, 2,0.

#### Cliffs: the edges of a raised tier

`cliff`, 8 wide by 3 tall. The boundary of a raised tier, on borrowed grass: a rocky rim on its north, west and east edges, and on its south edge a lit lip over a 24 px limestone face that takes the tier's two southmost rows and darkens to a shadow at its foot. The tier's inside is ordinary ground. Names are blob shape keys plus `|1` (the tier goes on two rows down) or `|0` (this is the face's upper row). Blocks.

```text
0x270 0x271 0x272 0x273 0x274 0x275 0x276 0x277   X X X X X X X X
0x278 0x279 0x27A 0x27B 0x27C 0x27D 0x27E 0x27F   X X X X X X X X
0x280 0x281 0x282 0x283 0x284 0x285 0x286 0x287   X X X X X X X X
```

Pieces: `1|00001110|1` 0x270, `1|00111000|1` 0x271, `1|00111110|1` 0x272, `1|10000011|0` 0x273, `1|10000011|0|b` 0x274, `1|10001111|0` 0x275, `1|10001111|0|b` 0x276, `1|10001111|1` 0x277, `1|11100000|0` 0x278, `1|11100000|0|b` 0x279, `1|11100011|0` 0x27A, `1|11100011|0|b` 0x27B, `1|11111000|0` 0x27C, `1|11111000|0|b` 0x27D, `1|11111000|1` 0x27E, `1|11111111|0` 0x27F, `1|11111111|0|b` 0x280.

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 2,0, 2,1, 2,2, 3,0, 3,1, 3,2, 4,0, 4,1, 4,2, 5,0, 5,1, 5,2, 6,0, 6,1, 6,2, 7,0, 7,1, 7,2.

#### Cliff faces: ivy, a crack, a tuft, a seep, a fern

`cliff_face`, 3 wide by 2 tall. Mid-face cells to scatter along a cliff's south face: `_u` for its upper row, `_l` for its lower row. `ivy` hangs from the lip, `crack_u` splits the face with a fern, `tuft_u` a grass tuft on a ledgelet, `seep_l` a dark wet streak, `fern_l` a fern at the foot.

```text
0x265 0x266 0x267   X X X
0x26D 0x26E 0x26F   X X X
```

Pieces: `ivy_u` 0x265, `crack_u` 0x266, `tuft_u` 0x267, `ivy_l` 0x26D, `seep_l` 0x26E, `fern_l` 0x26F.

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### Rock steps cut through a cliff

`cliff_stair`, 3 wide by 2 tall. The road's way up a cliff: a two-row flight of rock steps cut through the face, on borrowed road. 2 wide: `TL`, `TR` over `BL`, `BR`; 1 wide: `T` over `B`. Put them in the face's two rows; the face's own cells either side stay as they are. Walkable.

```text
0x288 0x289 0x28A   . . .
0x290 0x291 0x292   . . .
```

Pieces: `TL` 0x288, `TR` 0x289, `BL` 0x290, `BR` 0x291, `T` 0x28A, `B` 0x292.

Borrowed ground: path at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### Rock ledges: one way down

`ledge`, 3 wide by 2 tall. `S_*` drop south (MB_JUMP_SOUTH): a knee-high step of grey rock with grass above and its shadow below; the road home on Mt. Kithairon. `N_*` drop north (MB_JUMP_NORTH): the same seen from above, the land falling away beyond a rocky lip; the way down Route 7's north face. L, M, R: the ends taper into the grass.

```text
0x28B 0x28C 0x28D   J J J
0x293 0x294 0x295   X X X
```

Pieces: `S_L` 0x28B, `S_M` 0x28C, `S_R` 0x28D, `N_L` 0x293, `N_M` 0x294, `N_R` 0x295.

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### Rocky ground: boulders, a split crag, a scree heap

`rocks`, 3 wide by 1 tall. Impassable rock for a tier's top or a wood's floor: `pile` a heap of boulders, `split` a crag split by a juniper, `scree` a heap of broken stone. On borrowed grass.

```text
0x26A 0x26B 0x26C   X X X
```

Pieces: `pile` 0x26A, `split` 0x26B, `scree` 0x26C.

Borrowed ground: grass at 0,0, 1,0, 2,0.

#### Deadfall: a fallen fir, a stump, a dead snag

`deadfall`, 4 wide by 2 tall. `log_W` + `log_E`: a fallen fir lying east-west, its broken top to the west and its root plate to the east, moss along its back. `stump` a fir stump, `snag_top` over `snag` a dead fir standing grey (its top drawn over the player). `_s` copies stand on the woods' deep shade.

```text
0x298 0x299 0x29A 0x29B   X X X T
0x2A0 0x2A1 0x2A2 0x2A3   X X X X
```

Pieces: `log_W` 0x298, `log_E` 0x299, `stump` 0x29A, `snag_top` 0x29B, `snag` 0x2A3, `log_W_s` 0x2A0, `log_E_s` 0x2A1, `stump_s` 0x2A2.

Borrowed ground: grass at 0,0, 1,0, 2,0, 3,0, 3,1; shade at 0,1, 1,1, 2,1.

### The god's vines: trellises, the old vines, the press, the cart

#### Vine row on a trellis (east-west)

`trellis`, 4 wide by 1 tall. A row of the god's vines. `W` and `E` end the row with a post; `M` and `grapes` repeat between (mix them). Rows block: leave a lane between rows, or plant tall grass there.

```text
0x29C 0x29D 0x29E 0x29F   X X X X
```

Pieces: `W` 0x29C, `M` 0x29D, `grapes` 0x29E, `E` 0x29F.

Borrowed ground: grass at 0,0, 1,0, 2,0, 3,0.

#### Stone wine press and treading floor

`press`, 3 wide by 2 tall. A treading floor of dressed stone, purple with years of must, draining through a spout into a sunken vat. Its sign is the press ("Tread barefoot...").

```text
0x2A4 0x2A5 0x2A6   X X X
0x2AC 0x2AD 0x2AE   X X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### The wine-cart with the broken wheel

`cart`, 3 wide by 2 tall. Tipped onto its axle on the third terrace: a cart of amphorae for the Dionysia, its east wheel off and lying flat. The driver stands beside it.

```text
0x2A8 0x2A9 0x2AA   X X X
0x2B0 0x2B1 0x2B2   X X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### The herald's barrier pole across the road

`barrier`, 2 wide by 1 tall. On borrowed road, across a two-wide road: `W` then `E`. Blocks. When the herald lifts it, swap both cells back to road (METATILE_Kithairon_Barrier_W/_E, aethos's road 0x1D9).

```text
0x28E 0x28F   X X
```

Pieces: `W` 0x28E, `E` 0x28F.

Borrowed ground: path at 0,0, 1,0.

### Eleutherai's fort, the god's temple, troughs, Pentheus's fir

#### Eleutherai's Cyclopean walls, towers and gate

`fort`, 7 wide by 4 tall. A wall run is W0 over W1: L, then M repeated, then R. A tower (T0 over T1 over T2, 2 wide) stands in a run's place with its T0 row above the coping. The gate is gate_* over gateF_* (3 wide): the passage is the middle column, its lintel drawn over the player. `side` is a wall seen from above, running north; `side_foot` ends it. `door` (a W1 cell) is the watch-house's door; `slit` an arrow slit for W0. `court` is the parade ground's beaten earth (walkable).

```text
0x2B8 0x2B9 0x2BA 0x2BB 0x2BC 0x2BD 0x2BE   X X X X X X X
0x2C0 0x2C1 0x2C2 0x2C3 0x2C4 0x2C5 0x2C6   X X X D X X X
0x2C8 0x2C9 0x2CA 0x2CB 0x2CC 0x2CD 0x2CE   X T X . X X X
0x2D0 0x2D1 0x2D2 0x2D3 0x2D4 0x2D5 0x2D6   X . X X X X X
```

Pieces: `W0_L` 0x2B8, `W0_M` 0x2B9, `W0_R` 0x2BA, `slit` 0x2BB, `W1_L` 0x2C0, `W1_M` 0x2C1, `W1_R` 0x2C2, `door` 0x2C3, `side` 0x2BC, `side_foot` 0x2C4, `T0_L` 0x2BD, `T0_R` 0x2BE, `T1_L` 0x2C5, `T1_R` 0x2C6, `T2_L` 0x2CD, `T2_R` 0x2CE, `gate_L` 0x2C8, `gate_M` 0x2C9, `gate_R` 0x2CA, `gateF_L` 0x2D0, `gateF_M` 0x2D1, `gateF_R` 0x2D2, `court` 0x2CB.

#### The god's roofless temple: columns and the empty plinth

`temple`, 8 wide by 2 tall. On borrowed road paving (the floor is aethos's limestone patch), with `_g` copies on grass for the columns that stand outside it. A standing column is `col_top` over `col` (its capital drawn over the player). `plinth` is the empty plinth (beat 27): put its sign there. `broom` is Oinoe's swept step with her broom leaning on it.

```text
0x2D8 0x2D9 0x2DA 0x2DB 0x2DC 0x2DD 0x2DE 0x2DF   T . . . T . . .
0x2E0 0x2E1 0x2E2 0x2E3 0x2E4 0x2E5 0x2E6 0x2E7   X X X X X X X .
```

Pieces: `col_top` 0x2D8, `col` 0x2E0, `stump` 0x2E1, `drum` 0x2E2, `plinth` 0x2E3, `col_top_g` 0x2DC, `col_g` 0x2E4, `stump_g` 0x2E5, `drum_g` 0x2E6, `broom` 0x2E7.

Borrowed ground: grass at 4,0, 4,1, 5,0, 5,1, 6,0, 6,1, 7,0; path at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1, 3,0, 3,1, 7,1.

#### Stone trough with spring water

`trough`, 2 wide by 1 tall. A long stone trough on borrowed (animated) water, fed by a spout at its west end: Eleutherai's spring, Phorbas's fold. Blocks.

```text
0x296 0x297   X X
```

Pieces: `W` 0x296, `E` 0x297.

Borrowed ground: sea at 0,0, 1,0.

#### A cave mouth in a cliff's lower row

`cliff_mouth`, 1 wide by 1 tall. A dark arch in a cliff's lower face row (MB_NON_ANIMATED_DOOR: put the warp there).

```text
0x2A7   D
```

Pieces: `mouth` 0x2A7.

Borrowed ground: grass at 0,0.

### Eleutherai's houses (Eleusa's kit)

#### Tiled roof: ridge row and eave row

`roof_tile`, 3 wide by 2 tall. Red Laconian tiles. Repeat the middle column for a wider house.

```text
0x2E8 0x2E9 0x2EA   X X X
0x2F0 0x2F1 0x2F2   X X X
```

Pieces: `R0_L` 0x2E8, `R0_M` 0x2E9, `R0_R` 0x2EA, `R1_L` 0x2F0, `R1_M` 0x2F1, `R1_R` 0x2F2.

#### Wall rows: upper and lower (on the socle)

`wall`, 3 wide by 2 tall. Plain plaster. Every window, door and extra below is a W0 or W1 M cell, so it can stand anywhere between the corners.

```text
0x2EB 0x2EC 0x2ED   X X X
0x2F3 0x2F4 0x2F5   X X X
```

Pieces: `W0_L` 0x2EB, `W0_M` 0x2EC, `W0_R` 0x2ED, `W1_L` 0x2F3, `W1_M` 0x2F4, `W1_R` 0x2F5.

#### Upper-wall cells: windows and garlic

`windows`, 2 wide by 1 tall. W0 cells. `shutters` is an open window with ox-blood shutters, `lattice` a small timber grille, `closed` shutters shut, `garlic` strings of garlic and onions on a peg.

```text
0x2B3 0x2B4   X X
```

Pieces: `shutters` 0x2B3, `lattice` 0x2B4.

#### Doors (lower-wall cells)

`doors`, 2 wide by 1 tall. W1 cells; every one is a door (MB_NON_ANIMATED_DOOR): put the warp there. `plank` a dark plank door in ox-blood jambs, `dutch` its top leaf open, `curtain` an arched doorway with a striped wool curtain, `barn_l` + `barn_r` a wide double door (warp on both).

```text
0x2B5 0x2B6   D D
```

Pieces: `plank` 0x2B5, `curtain` 0x2B6.

## `gTileset_Kronia`: Route 7 and the Kronia grounds

![sheet](img/tiles_kronia_sheet.png)

### Core

The same structures at the same ids as in `gTileset_Kithairon`'s core, above.

### The Kronia grounds

#### A long table under a striped awning, and benches

`feast_table`, 5 wide by 3 tall. Row 0, the awning: C_L, C_M (repeat, mixing C_M2 and C_M3 for the poles' sag), C_R. Row 1, the table under its hem: T_L, then any mix of T_bread, T_figs and T_jars, then T_R. Row 2 holds benches for the row below a table: B_L, B_M..., B_R, or B_one alone. Everything blocks; people sit on the benches (put the objects there).

```text
0x2A8 0x2A9 0x2AA 0x2AB 0x2AC   X X X X X
0x2B0 0x2B1 0x2B2 0x2B3 0x2B4   X X X X X
0x2B8 0x2B9 0x2BA 0x2BB 0x2BC   X X X X .
```

Pieces: `C_L` 0x2A8, `C_M` 0x2A9, `C_M2` 0x2AA, `C_M3` 0x2AB, `C_R` 0x2AC, `T_L` 0x2B0, `T_bread` 0x2B1, `T_figs` 0x2B2, `T_jars` 0x2B3, `T_R` 0x2B4, `B_L` 0x2B8, `B_M` 0x2B9, `B_R` 0x2BA, `B_one` 0x2BB.

Borrowed ground: grass at 0,0, 0,2, 1,0, 1,2, 2,0, 2,2, 3,0, 3,2, 4,0, 4,2.

#### The great domed bread oven

`oven`, 3 wide by 3 tall. A beehive oven of whitewashed daub on a stone ring, its mouth glowing, loaves on a board beside it. The baker stands by it. Its ash holds a hidden Charcoal ("still warm").

```text
0x29D 0x29E 0x29F   X X X
0x2A5 0x2A6 0x2A7   X X X
0x2AD 0x2AE 0x2AF   X X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 2,0, 2,1, 2,2.

#### A Kronist tent

`tent`, 2 wide by 2 tall. A round canvas tent with a striped crown and a pennant, its flap tied shut. Ring them round the stage.

```text
0x28E 0x28F   X X
0x296 0x297   X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1.

#### The stewards' big tent

`big_tent`, 4 wide by 3 tall. The stewards' tent behind the stage: wide cream canvas trimmed in gold, a gold sickle painted over the flap, which is shut. "Nobody goes in." The flap (bottom row, middle) is never a door.

```text
0x2C0 0x2C1 0x2C2 0x2C3   X X X X
0x2C8 0x2C9 0x2CA 0x2CB   X X X X
0x2D0 0x2D1 0x2D2 0x2D3   X X X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 2,0, 2,1, 2,2, 3,0, 3,1, 3,2.

#### The Kronist stage hung with gold cloth

`stage`, 5 wide by 3 tall. A raised wooden stage: a backdrop of gold cloth on posts with a golden sun-and-sickle, the planked floor where the Kronist speaks (put him on the middle row), steps down the middle of its front.

```text
0x2D8 0x2D9 0x2DA 0x2DB 0x2DC   X X X X X
0x2E0 0x2E1 0x2E2 0x2E3 0x2E4   X X X X X
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC   X X X X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 2,0, 2,1, 2,2, 3,0, 3,1, 3,2, 4,0, 4,1, 4,2.

#### The painted banner: NO MORE HOURS

`banner`, 3 wide by 2 tall. A big banner on two poles: a golden field, people dancing, no one old, a smashed water clock in the corner and gold letters along the foot (beat 29). Its sign is on the bottom middle cell.

```text
0x2B5 0x2B6 0x2B7   X X X
0x2BD 0x2BE 0x2BF   X X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### Hoops, the gold sign and the reader's table

`camp_small`, 4 wide by 1 tall. `hoop` a child's hoop and stick lying in the grass (it blocks; put them out of the road), `board` the gold-painted sign on its post, `reader_L` + `reader_R` the reader's little table with wax tablets and his painted sign (TRUE READINGS. FREE.).

```text
0x2C4 0x2C5 0x2C6 0x2C7   X X X X
```

Pieces: `hoop` 0x2C4, `board` 0x2C5, `reader_L` 0x2C6, `reader_R` 0x2C7.

Borrowed ground: grass at 0,0, 1,0, 2,0, 3,0.

#### Stone trough with spring water

`trough`, 2 wide by 1 tall. A long stone trough on borrowed (animated) water, fed by a spout at its west end: Eleutherai's spring, Phorbas's fold. Blocks.

```text
0x2CC 0x2CD   X X
```

Pieces: `W` 0x2CC, `E` 0x2CD.

Borrowed ground: sea at 0,0, 1,0.

#### Water with a pebbly bank (pools, the Asopos)

`water`, 8 wide by 2 tall. Aethos's animated sea under a bank of grey pebbles and reeds. MB_POND_WATER: surf it with the Conch and fish it. Names are blob shape keys; the interior is `1|11111111`.

13 shapes, from 0x2F0; the interior `1|11111111` is 0x2F0.

## `gTileset_KithaironPass`: Mt. Kithairon, the maenads' pass

![sheet](img/tiles_kithairon_pass_sheet.png)

### Core: shared by Kithairon and Kronia at the same ids

#### Tall grass with soft edges

`tall`, 8 wide by 3 tall. Barley tall grass on aethos grass, cut from one field so any outline works (agros's painter, as on Route 1). MB_TALL_GRASS throughout. Names are blob shape keys (`1|NNEESESSWWNW`).

23 shapes, from 0x200; the interior `1|11111111` is 0x200.

#### The road with soft edges

`path`, 8 wide by 3 tall. The limestone road and its goat-track branches, scalloped where they meet the grass (agros's painter). Names are blob shape keys.

24 shapes, from 0x218; the interior `1|11111111` is 0x218.

#### Black fir (2 x 3 with its spire)

`fir`, 2 wide by 3 tall. A black fir. The top row is its spire over the grass of the row above: walkable, drawn over the player. Rows 1-2 block.

```text
0x230 0x231   T T
0x238 0x239   X X
0x240 0x241   X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### Slim fir (2 x 3 with its spire)

`fir_b`, 2 wide by 3 tall. A black fir. The top row is its spire over the grass of the row above: walkable, drawn over the player. Rows 1-2 block.

```text
0x232 0x233   T T
0x23A 0x23B   X X
0x242 0x243   X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### A fir's base with the next fir's spire over it

`fir_stack`, 2 wide by 1 tall. Between two firs in a column: the upper fir's base row, the lower fir's spire over it. Blocks.

```text
0x234 0x235   X X
```

Borrowed ground: grass at 0,0, 1,0.

#### A fir's base with the next fir's spire over it

`fir_stack_b`, 2 wide by 1 tall. Between two firs in a column: the upper fir's base row, the lower fir's spire over it. Blocks.

```text
0x236 0x237   X X
```

Borrowed ground: grass at 0,0, 1,0.

#### Young fir (1 x 2)

`fir_young`, 1 wide by 2 tall. A sapling fir for gaps at the woods' edge. Its top half is drawn over the player.

```text
0x23C   T
0x244   X
```

Borrowed ground: grass at 0,0, 0,1.

#### Scrub oak (2 x 2)

`oak`, 2 wide by 2 tall. A low, wide kermes oak of the mountain's lower slopes.

```text
0x23D 0x23E   X X
0x245 0x246   X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1.

#### Stones of the road: the herm, boundary stones, scree

`markers`, 4 wide by 2 tall. On borrowed grass. `herm_top` over `herm`: the great herm, hung with ivy. `boundary` a worn boundary stone, `boulder` a grey rock, `scree`/`scree_b` loose stones (walkable), `dig` turned earth on grass (walkable).

```text
0x248 0x249 0x24A 0x24B   T . . X
0x250 0x251 0x252 0x253   X X . .
```

Pieces: `herm_top` 0x248, `dig` 0x249, `scree_b` 0x24A, `boulder` 0x24B, `herm` 0x250, `boundary` 0x251, `scree` 0x252.

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1, 3,0, 3,1.

#### Black fir (2 x 3 with its spire), in the woods' shade

`fir_shade`, 2 wide by 3 tall. The same as `fir`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir`'s top row there.

```text
0x24C 0x24D   T T
0x254 0x255   X X
0x25C 0x25D   X X
```

Borrowed ground: shade at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### Slim fir (2 x 3 with its spire), in the woods' shade

`fir_b_shade`, 2 wide by 3 tall. The same as `fir_b`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_b`'s top row there.

```text
0x24E 0x24F   T T
0x256 0x257   X X
0x25E 0x25F   X X
```

Borrowed ground: shade at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### A fir's base with the next fir's spire over it, in the woods' shade

`fir_stack_shade`, 2 wide by 1 tall. The same as `fir_stack`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_stack`'s top row there.

```text
0x258 0x259   X X
```

Borrowed ground: shade at 0,0, 1,0.

#### A fir's base with the next fir's spire over it, in the woods' shade

`fir_stack_b_shade`, 2 wide by 1 tall. The same as `fir_stack_b`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_stack_b`'s top row there.

```text
0x25A 0x25B   X X
```

Borrowed ground: shade at 0,0, 1,0.

#### Young fir (1 x 2), in the woods' shade

`fir_young_shade`, 1 wide by 2 tall. The same as `fir_young`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_young`'s top row there.

```text
0x23F   T
0x247   X
```

Borrowed ground: shade at 0,0, 0,1.

#### Scrub oak (2 x 2), in the woods' shade

`oak_shade`, 2 wide by 2 tall. The same as `oak`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `oak`'s top row there.

```text
0x260 0x261   X X
0x268 0x269   X X
```

Borrowed ground: shade at 0,0, 0,1, 1,0, 1,1.

#### Meadow flowers and a tussock

`meadow`, 3 wide by 1 tall. Walkable. Scatter through open grass with aethos's red anemones (0x004): `white` narcissus, `yellow` mountain crocus, `tuft` a tussock.

```text
0x262 0x263 0x264   . . .
```

Pieces: `white` 0x262, `yellow` 0x263, `tuft` 0x264.

Borrowed ground: grass at 0,0, 1,0, 2,0.

#### Cliffs: the edges of a raised tier

`cliff`, 8 wide by 3 tall. The boundary of a raised tier, on borrowed grass: a rocky rim on its north, west and east edges, and on its south edge a lit lip over a 24 px limestone face that takes the tier's two southmost rows and darkens to a shadow at its foot. The tier's inside is ordinary ground. Names are blob shape keys plus `|1` (the tier goes on two rows down) or `|0` (this is the face's upper row). Blocks.

```text
0x270 0x271 0x272 0x273 0x274 0x275 0x276 0x277   X X X X X X X X
0x278 0x279 0x27A 0x27B 0x27C 0x27D 0x27E 0x27F   X X X X X X X X
0x280 0x281 0x282 0x283 0x284 0x285 0x286 0x287   X X X X X X X X
```

Pieces: `1|00001110|1` 0x270, `1|00111000|1` 0x271, `1|00111110|1` 0x272, `1|10000011|0` 0x273, `1|10000011|0|b` 0x274, `1|10001111|0` 0x275, `1|10001111|0|b` 0x276, `1|10001111|1` 0x277, `1|11100000|0` 0x278, `1|11100000|0|b` 0x279, `1|11100011|0` 0x27A, `1|11100011|0|b` 0x27B, `1|11111000|0` 0x27C, `1|11111000|0|b` 0x27D, `1|11111000|1` 0x27E, `1|11111111|0` 0x27F, `1|11111111|0|b` 0x280.

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 2,0, 2,1, 2,2, 3,0, 3,1, 3,2, 4,0, 4,1, 4,2, 5,0, 5,1, 5,2, 6,0, 6,1, 6,2, 7,0, 7,1, 7,2.

#### Cliff faces: ivy, a crack, a tuft, a seep, a fern

`cliff_face`, 3 wide by 2 tall. Mid-face cells to scatter along a cliff's south face: `_u` for its upper row, `_l` for its lower row. `ivy` hangs from the lip, `crack_u` splits the face with a fern, `tuft_u` a grass tuft on a ledgelet, `seep_l` a dark wet streak, `fern_l` a fern at the foot.

```text
0x265 0x266 0x267   X X X
0x26D 0x26E 0x26F   X X X
```

Pieces: `ivy_u` 0x265, `crack_u` 0x266, `tuft_u` 0x267, `ivy_l` 0x26D, `seep_l` 0x26E, `fern_l` 0x26F.

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### Rock steps cut through a cliff

`cliff_stair`, 3 wide by 2 tall. The road's way up a cliff: a two-row flight of rock steps cut through the face, on borrowed road. 2 wide: `TL`, `TR` over `BL`, `BR`; 1 wide: `T` over `B`. Put them in the face's two rows; the face's own cells either side stay as they are. Walkable.

```text
0x288 0x289 0x28A   . . .
0x290 0x291 0x292   . . .
```

Pieces: `TL` 0x288, `TR` 0x289, `BL` 0x290, `BR` 0x291, `T` 0x28A, `B` 0x292.

Borrowed ground: path at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### Rock ledges: one way down

`ledge`, 3 wide by 2 tall. `S_*` drop south (MB_JUMP_SOUTH): a knee-high step of grey rock with grass above and its shadow below; the road home on Mt. Kithairon. `N_*` drop north (MB_JUMP_NORTH): the same seen from above, the land falling away beyond a rocky lip; the way down Route 7's north face. L, M, R: the ends taper into the grass.

```text
0x28B 0x28C 0x28D   J J J
0x293 0x294 0x295   X X X
```

Pieces: `S_L` 0x28B, `S_M` 0x28C, `S_R` 0x28D, `N_L` 0x293, `N_M` 0x294, `N_R` 0x295.

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### Rocky ground: boulders, a split crag, a scree heap

`rocks`, 3 wide by 1 tall. Impassable rock for a tier's top or a wood's floor: `pile` a heap of boulders, `split` a crag split by a juniper, `scree` a heap of broken stone. On borrowed grass.

```text
0x26A 0x26B 0x26C   X X X
```

Pieces: `pile` 0x26A, `split` 0x26B, `scree` 0x26C.

Borrowed ground: grass at 0,0, 1,0, 2,0.

#### Deadfall: a fallen fir, a stump, a dead snag

`deadfall`, 4 wide by 2 tall. `log_W` + `log_E`: a fallen fir lying east-west, its broken top to the west and its root plate to the east, moss along its back. `stump` a fir stump, `snag_top` over `snag` a dead fir standing grey (its top drawn over the player). `_s` copies stand on the woods' deep shade.

```text
0x298 0x299 0x29A 0x29B   X X X T
0x2A0 0x2A1 0x2A2 0x2A3   X X X X
```

Pieces: `log_W` 0x298, `log_E` 0x299, `stump` 0x29A, `snag_top` 0x29B, `snag` 0x2A3, `log_W_s` 0x2A0, `log_E_s` 0x2A1, `stump_s` 0x2A2.

Borrowed ground: grass at 0,0, 1,0, 2,0, 3,0, 3,1; shade at 0,1, 1,1, 2,1.

### The maenads' pass: Pentheus's fir, the shrine, the dancing floor

#### Pentheus's fir: the enormous one

`pentheus_fir`, 3 wide by 4 tall. An enormous old fir, one great branch torn away high up (beat 28). The top row is its spire, drawn over the player. Put the landmark's sign on its bottom middle cell.

```text
0x29C 0x29D 0x29E   T T T
0x2A4 0x2A5 0x2A6   X X X
0x2AC 0x2AD 0x2AE   X X X
0x2B4 0x2B5 0x2B6   X X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 0,3, 1,0, 1,1, 1,2, 1,3, 2,0, 2,1, 2,2, 2,3.

#### The mountain's shrine, Aktaion's seat, the maenads' drums

`shrine`, 3 wide by 3 tall. On borrowed grass. `shrine_top` over `shrine`: the little rock shrine of Dionysus with its stone cup; `shrine_bad_*` the same with a sickle scratched across the cup (desecrated). `seat` Aktaion's rock seat. `drum` a maenad's frame drum lying on its back, `drum_b` one stood on its rim with a beater: a skin over a deep wooden hoop, an ochre ring, bronze jingles.

```text
0x2A8 0x2A9 0x2AA   T T X
0x2B0 0x2B1 0x2B2   X X X
0x2B8 0x2B9 0x2BA   X X X
```

Pieces: `shrine_top` 0x2A8, `shrine_bad_top` 0x2A9, `drum_b` 0x2AA, `shrine` 0x2B0, `shrine_bad` 0x2B1, `seat` 0x2B2, `drum` 0x2B8.

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 2,0, 2,1, 2,2.

#### The marked ivy of the Thyrsus walls

`cliff_marked`, 1 wide by 2 tall. Thick ivy with gold-marked leaves from lip to foot, `marked_u` over `marked_l`: Dionysus's Thyrsus (gift II) climbs it. Put the wall's sign on the lower cell.

```text
0x28E   X
0x296   X
```

Pieces: `marked_u` 0x28E, `marked_l` 0x296.

Borrowed ground: grass at 0,0, 0,1.

#### Stone trough with spring water

`trough`, 2 wide by 1 tall. A long stone trough on borrowed (animated) water, fed by a spout at its west end: Eleutherai's spring, Phorbas's fold. Blocks.

```text
0x2BB 0x2BC   X X
```

Pieces: `W` 0x2BB, `E` 0x2BC.

Borrowed ground: sea at 0,0, 1,0.

#### Water with a pebbly bank (pools, the Asopos)

`water`, 8 wide by 2 tall. Aethos's animated sea under a bank of grey pebbles and reeds. MB_POND_WATER: surf it with the Conch and fish it. Names are blob shape keys; the interior is `1|11111111`.

13 shapes, from 0x2C0; the interior `1|11111111` is 0x2C0.

#### The dancing floor: trampled earth with soft edges

`trampled`, 8 wide by 2 tall. Grass beaten to bare earth by dancing feet. Walkable; names are blob shape keys.

```text
0x2D0 0x2D1 0x2D2 0x2D3 0x2D4 0x2D5 0x2D6 0x2D7   . . . . . . . .
0x2D8 0x2D9 0x2DA 0x2DB 0x2DC 0x2DD 0x2DE 0x2DF   . . . . . . . .
```

Pieces: `1|11111111` 0x2D0, `1|00000010` 0x2D1, `1|00001000` 0x2D2, `1|00101110` 0x2D3, `1|00111000` 0x2D4, `1|00111110` 0x2D5, `1|10000010` 0x2D6, `1|10000011` 0x2D7, `1|10001111` 0x2D8, `1|10111111` 0x2D9, `1|11100000` 0x2DA, `1|11100011` 0x2DB, `1|11111011` 0x2DC, `1|11111110` 0x2DD.

#### Wild pear in flower (2 x 2)

`pear`, 2 wide by 2 tall. A wild pear, white with blossom: the mountain's spring.

```text
0x2E0 0x2E1   X X
0x2E8 0x2E9   X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1.

#### The shepherds' lean-to

`leanto`, 2 wide by 2 tall. Brush thatch on four poles over straw and a sheepskin, against the fold wall. Phorbas sits on the wall beside it.

```text
0x2E2 0x2E3   X X
0x2EA 0x2EB   X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1.

## `gTileset_KithaironCave`: Antiope's cave

![sheet](img/tiles_kithairon_cave_sheet.png)

### Antiope's cave

#### Antiope's cave: walls on the cave floor

`cave`, 8 wide by 3 tall. The crag's rock as cave walls, on the cave floor. Impassable. Names are blob shape keys; `cave_floor` below is the open floor.

17 shapes, from 0x200; the interior `1|11111111` is 0x200.

#### Antiope's cave: the floor

`cave_floor`, 3 wide by 1 tall. `plain` the packed floor, `pebbles` a scatter of stones, `exit` the floor brightening toward daylight: MB_SOUTH_ARROW_WARP, put the warp out there on the cave's bottom row.

```text
0x218 0x219 0x21A   . . .
```

Pieces: `plain` 0x218, `pebbles` 0x219, `exit` 0x21A.

#### The cave's walls: carving, shelf, marked ivy

`cave_detail`, 5 wide by 1 tall. South-face cells of the cave walls (blob key `1|11100011`): the twins' carving, 2 wide (`cave_carving_L`, `_R`), a rock shelf for the PP Up, the marked ivy to the Star Piece's ledge, a crack.

```text
0x21B 0x21C 0x21D 0x21E 0x21F   X X X X X
```

Pieces: `cave_carving_L` 0x21B, `cave_carving_R` 0x21C, `cave_shelf` 0x21D, `cave_marked` 0x21E, `cave_crack` 0x21F.

#### The bronze brazier, cold and lit

`brazier`, 2 wide by 2 tall. A bronze bowl on a tripod, on the cave floor: `cold_top` over `cold`, and lit (`lit_top` over `lit`). Swap both cells to light it: METATILE_Kithairon_Brazier_*.

```text
0x220 0x221   X X
0x228 0x229   X X
```

Pieces: `cold_top` 0x220, `cold` 0x228, `lit_top` 0x221, `lit` 0x229.

#### Turned earth on the cave floor

`dig_cave`, 1 wide by 1 tall. A fixed dig spot on the cave floor (walkable).

```text
0x222   .
```

Pieces: `dig_cave` 0x222.

## Render-and-critique passes

Written by hand, kept across rebuilds. Each map was rendered with
`tools/ichor/maps/kithairon.py` (plain 2x, a review copy with collision and events, and
15 x 10 GBA screens along the road, in `build/render/kithairon/`), compared with
MAP_DESIGN.md and Act I's best maps (Route 1's final pass, Eleusa's scene), and fixed. The
final 2x renders are in `img/<Map>.png`; in-game screenshots of every scene are from
`tools/ichor/tests/kithairon.sh` (`build/test_kithairon/shots/`).

| Render | Map |
|---|---|
| [`img/kithairon_crossing.png`](img/kithairon_crossing.png) | The whole crossing, 1x, stitched as the maps connect: Route 7 at the top, Route 6 at the bottom |
| [`img/Route6_EleutheraiRoad.png`](img/Route6_EleutheraiRoad.png) | Route 6, the Eleutherai Road (56 x 28) |
| [`img/Route6_AntiopesCave.png`](img/Route6_AntiopesCave.png) | Antiope's cave (16 x 12) |
| [`img/Eleutherai.png`](img/Eleutherai.png) | Eleutherai (32 x 26) |
| [`img/MtKithairon.png`](img/MtKithairon.png) | Mt. Kithairon, the maenads' pass (40 x 56) |
| [`img/Route7_KroniaGrounds.png`](img/Route7_KroniaGrounds.png) | Route 7, the Kronia grounds (44 x 40) |

The builder also checks each map: every person, sign and trigger can be reached from the
entry (relic-gated items excepted), and which grass bands are forced. Today: Route 6's
two (3 and 4 deep), Mt. Kithairon's one (4 deep), Route 7's two (4 and 3 deep).

### The art (all maps)

1. **First paint.** The crag top was a 16 px Voronoi of small plates: it read as cobbled
   paving, not a mountain, and its 7 px face was too short to read as a cliff. Firs were
   right; Pentheus's torn branch was a black box. The whole kit came to about 700 tiles
   against 504.
2. **Second.** The crag top is now a plain weathered grey with sparse pits, and the detail
   moved into `crag_detail` cells (a crack, boulders, a tuft, a juniper, ivy) that the
   builder scatters through any crag; the face is 14 px of columns darkening to the foot,
   so a one-row crag reads as a retaining wall and a deep one as a cliff. The torn branch is
   a bitten-out gap with a pale stump. The Cyclopean masonry went from a 32 px to a 16 px
   repeat (64 tiles instead of 87). Three sets with a shared core replaced one set.
3. **Third.** Fir woods read as a plantation: identical firs in ranks on bright grass. The
   woods now stand on aethos's deep-shade grass (new metatiles, no new tiles), every other
   column pair is a row lower, and two-row runs are young firs, not oaks. Open grass was
   bare: `meadow` (narcissus, crocus, a tussock) and aethos's red anemones are scattered
   through it. The wine press was a purple slab; it is now dressed stone with the must's
   stain in its middle. The cave's walls were lighter than its floor (wrong for a cave):
   they are dark now, the floor paler, and the twins' carving is cut in light lines.

### Route 6, the Eleutherai Road

1. **Draft** (road at Eleusa's placeholder 26–29). Correct beats but flat: the terraces
   didn't read as terraces, and a huge flat crag filled the east side.
2. **Pass 1** (road moved to Eleusa's real 44–47). Redrawn as an exact grid. The terrace
   risers are one-row crags, so the hillside steps up in three visible terraces: the olive
   band (aethos only, the Eleusa seam), the vine terrace, terrace 2. The zigzag is mirrored
   (west along the vine terrace, the stair at the west end, east along terrace 2), because
   the road now arrives on the east side; the rhythm is SCRIPT.md's.
3. **Pass 2.** Woods on top of the east crag instead of bare rock, the spur's grass given an
   irregular edge, the first riser (row 21) made rock so the vines are the only way up.
4. **Pass 3.** Meadow flowers through the terraces; the press redrawn. Left as is: the
   aethos dry-stone walls are thin lines next to the crag risers; they mark terrace edges
   where the risers would be too heavy.

### Antiope's cave

1. **Draft.** Light grey wall tops over a dark floor: the cave looked inverted, and the
   carving was invisible.
2. **Pass 1.** Walls darkened, the floor lightened; the carving, the shelf (PP Up) and the
   marked ivy (Star Piece) each sit on a south face where they can be seen.
3. **Pass 2.** The exit mat is the floor brightening toward daylight, on the bottom row.

### Eleutherai

1. **Draft.** The road was drawn over by the town's ground and vanished; the temple paving
   had holes where the columns stood.
2. **Pass 1.** Exact grid: the road runs straight past the crag's foot, the fort is stamped
   whole (south wall with towers and the gate, side walls, the north wall with the
   watch-house door), the temple's paving counts its column cells as paving.
3. **Pass 2.** The empty plinth and Oinoe's broom were painted a row too high in the
   temple piece and didn't show; fixed. A row of oaks crowned the fort; the fort now stands
   on its rock (crag behind and beside it), firs on the rock's flanks. An olive and
   cypresses break up the open ground; the south side's path round the pens was opened.
4. **Pass 3.** Flowers through the grass. Left as is: the court is plain beaten earth.

### Mt. Kithairon

1. **Draft.** Mostly open grass with a straight road; the rows of firs looked planted.
2. **Pass 1.** Exact grid with the switchbacks, the fir clearing's band, the glade, the fork,
   the fold, the shrine ledge.
3. **Pass 2.** Woods closed in round the fold and below the shrine ledge; the dancing floor
   became a ring of trampled earth in the glade instead of a square; scree on the slopes.
4. **Pass 3.** Woods staggered and on shade; young firs where the woods are two rows
   deep.
5. **Pass 4.** The north half's road ran straight for thirty rows: it now bends west round
   the fold's wall, between the fold and a clump of firs. In game the maenads' ring stood
   above the camera when the dance began; the ring moved two rows south and the trigger to
   the glade's first row (37), so the whole dance is on screen. Left as is: the drums read
   as pale stones, not drums.

### Route 7, the Kronia grounds

1. **Draft.** The camp read as a camp, but sparse; the Asopos was a wide blue block; the
   defile's two crags were large flat slabs; band 2's walls (aethos's north-south wall)
   looked like ladders.
2. **Pass 1.** Exact grid: the north face's defile, switchbacks and pasture; the camp's
   tables, oven, stage, stewards' tent, banner and tents; the herm at the mountain's foot.
3. **Pass 2.** The Asopos narrowed, its west bank wandering, the reed islet midstream;
   band 2 fenced by scrub (firs) instead of walls.
4. **Pass 3.** The defile's rock narrowed with firs on its shoulders; three more tents in
   the ring; an olive in the west meadow. Known weakness: the west meadow is still open.

### Deviations

- **Three secondaries, not one** (above, *How it fits together*). The Route 7 seam is
  covered by the shared core.
- **Route 6's zigzag is mirrored** (Eleusa's road arrives at x 44-47, on the east side).
- **Route 7 has no ledges.** aethos's ledges only jump south (uphill here); SCRIPT.md's
  open question 1 wanted north-dropping ledges, which would need new ledge art. The
  descent's shortcut is the road itself.
- **Komos faces across the defile**, not up the road: one trainer facing up a two-wide road
  covers one column. His sight (4) covers both road columns.
- **Arimnestos guards the drum's path** at the fork rather than standing west of the fold:
  SCRIPT.md puts the boundary stone at the fork and the drum west of the fold, and he
  stands by both.
