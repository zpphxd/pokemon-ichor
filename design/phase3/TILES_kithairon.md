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
| `gTileset_Kithairon` | 468 of 504 | 280 of 512 |
| `gTileset_Kronia` | 415 of 504 | 248 of 512 |
| `gTileset_KithaironCave` | 63 of 504 | 48 of 512 |

## `gTileset_Kithairon`: Route 6, Eleutherai and Mt. Kithairon

![sheet](img/tiles_kithairon_sheet.png)

### Core: shared by Kithairon and Kronia at the same ids

#### Tall grass with soft edges

`tall`, 8 wide by 3 tall. Barley tall grass on aethos grass, cut from one field so any outline works (agros's painter, as on Route 1). MB_TALL_GRASS throughout. Names are blob shape keys (`1|NNEESESSWWNW`).

20 shapes, from 0x200; the interior `1|11111111` is 0x200.

#### The road with soft edges

`path`, 8 wide by 3 tall. The limestone road and its goat-track branches, scalloped where they meet the grass (agros's painter). Names are blob shape keys.

23 shapes, from 0x218; the interior `1|11111111` is 0x218.

#### Crags: grey rock with a south face

`crag`, 8 wide by 5 tall. Kithairon's grey limestone, seen from above with its south face showing, on aethos grass. Fill any region with it: the face appears along every south edge and the rock casts a shadow on the grass. Impassable. Names are blob shape keys.

34 shapes, from 0x230; the interior `1|11111111` is 0x230.

#### Water with a pebbly bank (pools, the Asopos)

`water`, 8 wide by 2 tall. Aethos's animated sea under a bank of grey pebbles and reeds. MB_POND_WATER: surf it with the Conch and fish it. Names are blob shape keys; the interior is `1|11111111`.

13 shapes, from 0x258; the interior `1|11111111` is 0x258.

#### Black fir (2 x 3 with its spire)

`fir`, 2 wide by 3 tall. A black fir. The top row is its spire over the grass of the row above: walkable, drawn over the player. Rows 1-2 block.

```text
0x268 0x269   T T
0x270 0x271   X X
0x278 0x279   X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### Slim fir (2 x 3 with its spire)

`fir_b`, 2 wide by 3 tall. A black fir. The top row is its spire over the grass of the row above: walkable, drawn over the player. Rows 1-2 block.

```text
0x26A 0x26B   T T
0x272 0x273   X X
0x27A 0x27B   X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### A fir's base with the next fir's spire over it

`fir_stack`, 2 wide by 1 tall. Between two firs in a column: the upper fir's base row, the lower fir's spire over it. Blocks.

```text
0x26C 0x26D   X X
```

Borrowed ground: grass at 0,0, 1,0.

#### A fir's base with the next fir's spire over it

`fir_stack_b`, 2 wide by 1 tall. Between two firs in a column: the upper fir's base row, the lower fir's spire over it. Blocks.

```text
0x26E 0x26F   X X
```

Borrowed ground: grass at 0,0, 1,0.

#### Young fir (1 x 2)

`fir_young`, 1 wide by 2 tall. A sapling fir for gaps at the woods' edge. Its top half is drawn over the player.

```text
0x274   T
0x27C   X
```

Borrowed ground: grass at 0,0, 0,1.

#### Scrub oak (2 x 2)

`oak`, 2 wide by 2 tall. A low, wide kermes oak of the mountain's lower slopes.

```text
0x275 0x276   X X
0x27D 0x27E   X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1.

#### Crag detail: cracks, boulders, ivy, mouths

`crag_detail`, 8 wide by 1 tall. Interior crag cells (`crack`, `boulders`, `tuft`, `juniper`, `ivy_top`) to scatter through a big crag. South-face cells (blob key `1|11100011`): `ivy_face` ivy over the face, `marked_face` the marked ivy of the Thyrsus walls (gift II), `mouth` a cave mouth (MB_NON_ANIMATED_DOOR: put the warp there).

```text
0x280 0x281 0x282 0x283 0x284 0x285 0x286 0x287   X X X X X X X D
```

Pieces: `crack` 0x280, `boulders` 0x281, `tuft` 0x282, `juniper` 0x283, `ivy_top` 0x284, `ivy_face` 0x285, `marked_face` 0x286, `mouth` 0x287.

#### Stones and shrines of the mountain

`markers`, 8 wide by 2 tall. On borrowed grass. `herm_top` over `herm`: the great herm, hung with ivy. `shrine_top` over `shrine`: the little rock shrine of Dionysus with its stone cup; `shrine_bad_*` the same with a sickle scratched across the cup (desecrated). `boundary` a worn boundary stone, `seat` Aktaion's rock seat, `boulder` a grey rock, `scree`/`scree_b` loose stones (walkable), `drum`/`drum_b` the maenads' frame drums, `dig` turned earth on grass and `dig_cave` on the cave floor (walkable).

```text
0x288 0x289 0x28A 0x28B 0x28C 0x28D 0x28E 0x28F   T T T . . X X X
0x290 0x291 0x292 0x293 0x294 0x295 0x296 0x297   X X X X . X X X
```

Pieces: `herm_top` 0x288, `shrine_top` 0x289, `shrine_bad_top` 0x28A, `dig` 0x28B, `scree_b` 0x28C, `drum_b` 0x28D, `boulder` 0x28E, `herm` 0x28F, `shrine` 0x290, `shrine_bad` 0x291, `boundary` 0x292, `seat` 0x293, `scree` 0x294, `drum` 0x295.

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1, 3,0, 3,1, 4,0, 4,1, 5,0, 5,1, 6,0, 6,1, 7,0, 7,1.

#### Black fir (2 x 3 with its spire), in the woods' shade

`fir_shade`, 2 wide by 3 tall. The same as `fir`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir`'s top row there.

```text
0x298 0x299   T T
0x2A0 0x2A1   X X
0x2A8 0x2A9   X X
```

Borrowed ground: shade at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### Slim fir (2 x 3 with its spire), in the woods' shade

`fir_b_shade`, 2 wide by 3 tall. The same as `fir_b`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_b`'s top row there.

```text
0x29A 0x29B   T T
0x2A2 0x2A3   X X
0x2AA 0x2AB   X X
```

Borrowed ground: shade at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2.

#### A fir's base with the next fir's spire over it, in the woods' shade

`fir_stack_shade`, 2 wide by 1 tall. The same as `fir_stack`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_stack`'s top row there.

```text
0x29C 0x29D   X X
```

Borrowed ground: shade at 0,0, 1,0.

#### A fir's base with the next fir's spire over it, in the woods' shade

`fir_stack_b_shade`, 2 wide by 1 tall. The same as `fir_stack_b`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_stack_b`'s top row there.

```text
0x29E 0x29F   X X
```

Borrowed ground: shade at 0,0, 1,0.

#### Young fir (1 x 2), in the woods' shade

`fir_young_shade`, 1 wide by 2 tall. The same as `fir_young`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `fir_young`'s top row there.

```text
0x277   T
0x27F   X
```

Borrowed ground: shade at 0,0, 0,1.

#### Scrub oak (2 x 2), in the woods' shade

`oak_shade`, 2 wide by 2 tall. The same as `oak`, on aethos's deep-shade grass, for inside a wood. The spire row stays on plain grass: use `oak`'s top row there.

```text
0x2A4 0x2A5   X X
0x2AC 0x2AD   X X
```

Borrowed ground: shade at 0,0, 0,1, 1,0, 1,1.

### The god's vines: trellises, the old vines, the press, the cart

#### Vine row on a trellis (east-west)

`trellis`, 4 wide by 1 tall. A row of the god's vines. `W` and `E` end the row with a post; `M` and `grapes` repeat between (mix them). Rows block: leave a lane between rows, or plant tall grass there.

```text
0x2B0 0x2B1 0x2B2 0x2B3   X X X X
```

Pieces: `W` 0x2B0, `M` 0x2B1, `grapes` 0x2B2, `E` 0x2B3.

Borrowed ground: grass at 0,0, 1,0, 2,0, 3,0.

#### The old vines across the road, and their cut stumps

`old_vines`, 3 wide by 1 tall. On borrowed road. `vines` and `vines_b` alternate across the road and block; when Demeter's Sickle cuts them, swap each for `stumps` (walkable): METATILE_Kithairon_OldVines_* and _Stumps.

```text
0x2B4 0x2B5 0x2B6   X X .
```

Pieces: `vines` 0x2B4, `vines_b` 0x2B5, `stumps` 0x2B6.

Borrowed ground: path at 0,0, 1,0, 2,0.

#### Stone wine press and treading floor

`press`, 3 wide by 2 tall. A treading floor of dressed stone, purple with years of must, draining through a spout into a sunken vat. Its sign is the press ("Tread barefoot...").

```text
0x2B8 0x2B9 0x2BA   X X X
0x2C0 0x2C1 0x2C2   X X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### The wine-cart with the broken wheel

`cart`, 3 wide by 2 tall. Tipped onto its axle on the third terrace: a cart of amphorae for the Dionysia, its east wheel off and lying flat. The driver stands beside it.

```text
0x2BB 0x2BC 0x2BD   X X X
0x2C3 0x2C4 0x2C5   X X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### The herald's barrier pole across the road

`barrier`, 2 wide by 1 tall. On borrowed road, across a two-wide road: `W` then `E`. Blocks. When the herald lifts it, swap both cells back to road (METATILE_Kithairon_Barrier_W/_E, aethos's road 0x1D9).

```text
0x2A6 0x2A7   X X
```

Pieces: `W` 0x2A6, `E` 0x2A7.

Borrowed ground: path at 0,0, 1,0.

### Eleutherai's fort, the god's temple, troughs, Pentheus's fir

#### Eleutherai's Cyclopean walls, towers and gate

`fort`, 7 wide by 4 tall. A wall run is W0 over W1: L, then M repeated, then R. A tower (T0 over T1 over T2, 2 wide) stands in a run's place with its T0 row above the coping. The gate is gate_* over gateF_* (3 wide): the passage is the middle column, its lintel drawn over the player. `side` is a wall seen from above, running north; `side_foot` ends it. `door` (a W1 cell) is the watch-house's door; `slit` an arrow slit for W0. `court` is the parade ground's beaten earth (walkable).

```text
0x2C8 0x2C9 0x2CA 0x2CB 0x2CC 0x2CD 0x2CE   X X X X X X X
0x2D0 0x2D1 0x2D2 0x2D3 0x2D4 0x2D5 0x2D6   X X X D X X X
0x2D8 0x2D9 0x2DA 0x2DB 0x2DC 0x2DD 0x2DE   X T X . X X X
0x2E0 0x2E1 0x2E2 0x2E3 0x2E4 0x2E5 0x2E6   X . X X X X X
```

Pieces: `W0_L` 0x2C8, `W0_M` 0x2C9, `W0_R` 0x2CA, `slit` 0x2CB, `W1_L` 0x2D0, `W1_M` 0x2D1, `W1_R` 0x2D2, `door` 0x2D3, `side` 0x2CC, `side_foot` 0x2D4, `T0_L` 0x2CD, `T0_R` 0x2CE, `T1_L` 0x2D5, `T1_R` 0x2D6, `T2_L` 0x2DD, `T2_R` 0x2DE, `gate_L` 0x2D8, `gate_M` 0x2D9, `gate_R` 0x2DA, `gateF_L` 0x2E0, `gateF_M` 0x2E1, `gateF_R` 0x2E2, `court` 0x2DB.

#### The god's roofless temple: columns and the empty plinth

`temple`, 8 wide by 2 tall. On borrowed road paving (the floor is aethos's limestone patch), with `_g` copies on grass for the columns that stand outside it. A standing column is `col_top` over `col` (its capital drawn over the player). `plinth` is the empty plinth (beat 27): put its sign there. `broom` is Oinoe's swept step with her broom leaning on it.

```text
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC 0x2ED 0x2EE 0x2EF   T . . . T . . .
0x2F0 0x2F1 0x2F2 0x2F3 0x2F4 0x2F5 0x2F6 0x2F7   X X X X X X X .
```

Pieces: `col_top` 0x2E8, `col` 0x2F0, `stump` 0x2F1, `drum` 0x2F2, `plinth` 0x2F3, `col_top_g` 0x2EC, `col_g` 0x2F4, `stump_g` 0x2F5, `drum_g` 0x2F6, `broom` 0x2F7.

Borrowed ground: grass at 4,0, 4,1, 5,0, 5,1, 6,0, 6,1, 7,0; path at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1, 3,0, 3,1, 7,1.

#### Stone trough with spring water

`trough`, 2 wide by 1 tall. A long stone trough on borrowed (animated) water, fed by a spout at its west end: Eleutherai's spring, Phorbas's fold. Blocks.

```text
0x2AE 0x2AF   X X
```

Pieces: `W` 0x2AE, `E` 0x2AF.

Borrowed ground: sea at 0,0, 1,0.

#### Pentheus's fir: the enormous one

`pentheus_fir`, 3 wide by 4 tall. An enormous old fir, one great branch torn away high up (beat 28). The top row is its spire, drawn over the player. Put the landmark's sign on its bottom middle cell.

```text
0x2F8 0x2F9 0x2FA   T T T
0x300 0x301 0x302   X X X
0x308 0x309 0x30A   X X X
0x310 0x311 0x312   X X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 0,3, 1,0, 1,1, 1,2, 1,3, 2,0, 2,1, 2,2, 2,3.

### Eleutherai's houses (Eleusa's kit)

#### Tiled roof: ridge row and eave row

`roof_tile`, 3 wide by 2 tall. Red Laconian tiles. Repeat the middle column for a wider house.

```text
0x2FB 0x2FC 0x2FD   X X X
0x303 0x304 0x305   X X X
```

Pieces: `R0_L` 0x2FB, `R0_M` 0x2FC, `R0_R` 0x2FD, `R1_L` 0x303, `R1_M` 0x304, `R1_R` 0x305.

#### Wall rows: upper and lower (on the socle)

`wall`, 3 wide by 2 tall. Plain plaster. Every window, door and extra below is a W0 or W1 M cell, so it can stand anywhere between the corners.

```text
0x30B 0x30C 0x30D   X X X
0x313 0x314 0x315   X X X
```

Pieces: `W0_L` 0x30B, `W0_M` 0x30C, `W0_R` 0x30D, `W1_L` 0x313, `W1_M` 0x314, `W1_R` 0x315.

#### Upper-wall cells: windows and garlic

`windows`, 2 wide by 1 tall. W0 cells. `shutters` is an open window with ox-blood shutters, `lattice` a small timber grille, `closed` shutters shut, `garlic` strings of garlic and onions on a peg.

```text
0x2BE 0x2BF   X X
```

Pieces: `shutters` 0x2BE, `lattice` 0x2BF.

#### Doors (lower-wall cells)

`doors`, 2 wide by 1 tall. W1 cells; every one is a door (MB_NON_ANIMATED_DOOR): put the warp there. `plank` a dark plank door in ox-blood jambs, `dutch` its top leaf open, `curtain` an arched doorway with a striped wool curtain, `barn_l` + `barn_r` a wide double door (warp on both).

```text
0x2C6 0x2C7   D D
```

Pieces: `plank` 0x2C6, `curtain` 0x2C7.

## `gTileset_Kronia`: Route 7 and the Kronia grounds

![sheet](img/tiles_kronia_sheet.png)

### Core

The same structures at the same ids as in `gTileset_Kithairon`'s core, above.

### The Kronia grounds

#### A long table under a striped awning, and benches

`feast_table`, 5 wide by 3 tall. Row 0, the awning: C_L, C_M (repeat, mixing C_M2 and C_M3 for the poles' sag), C_R. Row 1, the table under its hem: T_L, then any mix of T_bread, T_figs and T_jars, then T_R. Row 2 holds benches for the row below a table: B_L, B_M..., B_R, or B_one alone. Everything blocks; people sit on the benches (put the objects there).

```text
0x2B0 0x2B1 0x2B2 0x2B3 0x2B4   X X X X X
0x2B8 0x2B9 0x2BA 0x2BB 0x2BC   X X X X X
0x2C0 0x2C1 0x2C2 0x2C3 0x2C4   X X X X .
```

Pieces: `C_L` 0x2B0, `C_M` 0x2B1, `C_M2` 0x2B2, `C_M3` 0x2B3, `C_R` 0x2B4, `T_L` 0x2B8, `T_bread` 0x2B9, `T_figs` 0x2BA, `T_jars` 0x2BB, `T_R` 0x2BC, `B_L` 0x2C0, `B_M` 0x2C1, `B_R` 0x2C2, `B_one` 0x2C3.

Borrowed ground: grass at 0,0, 0,2, 1,0, 1,2, 2,0, 2,2, 3,0, 3,2, 4,0, 4,2.

#### The great domed bread oven

`oven`, 3 wide by 3 tall. A beehive oven of whitewashed daub on a stone ring, its mouth glowing, loaves on a board beside it. The baker stands by it. Its ash holds a hidden Charcoal ("still warm").

```text
0x2B5 0x2B6 0x2B7   X X X
0x2BD 0x2BE 0x2BF   X X X
0x2C5 0x2C6 0x2C7   X X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 2,0, 2,1, 2,2.

#### A Kronist tent

`tent`, 2 wide by 2 tall. A round canvas tent with a striped crown and a pennant, its flap tied shut. Ring them round the stage.

```text
0x2A6 0x2A7   X X
0x2AE 0x2AF   X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1.

#### The stewards' big tent

`big_tent`, 4 wide by 3 tall. The stewards' tent behind the stage: wide cream canvas trimmed in gold, a gold sickle painted over the flap, which is shut. "Nobody goes in." The flap (bottom row, middle) is never a door.

```text
0x2C8 0x2C9 0x2CA 0x2CB   X X X X
0x2D0 0x2D1 0x2D2 0x2D3   X X X X
0x2D8 0x2D9 0x2DA 0x2DB   X X X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 2,0, 2,1, 2,2, 3,0, 3,1, 3,2.

#### The Kronist stage hung with gold cloth

`stage`, 5 wide by 3 tall. A raised wooden stage: a backdrop of gold cloth on posts with a golden sun-and-sickle, the planked floor where the Kronist speaks (put him on the middle row), steps down the middle of its front.

```text
0x2E0 0x2E1 0x2E2 0x2E3 0x2E4   X X X X X
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC   X X X X X
0x2F0 0x2F1 0x2F2 0x2F3 0x2F4   X X X X X
```

Borrowed ground: grass at 0,0, 0,1, 0,2, 1,0, 1,1, 1,2, 2,0, 2,1, 2,2, 3,0, 3,1, 3,2, 4,0, 4,1, 4,2.

#### The painted banner: NO MORE HOURS

`banner`, 3 wide by 2 tall. A big banner on two poles: a golden field, people dancing, no one old, a smashed water clock in the corner and gold letters along the foot (beat 29). Its sign is on the bottom middle cell.

```text
0x2CC 0x2CD 0x2CE   X X X
0x2D4 0x2D5 0x2D6   X X X
```

Borrowed ground: grass at 0,0, 0,1, 1,0, 1,1, 2,0, 2,1.

#### Hoops, the gold sign and the reader's table

`camp_small`, 4 wide by 1 tall. `hoop` a child's hoop and stick lying in the grass (it blocks; put them out of the road), `board` the gold-painted sign on its post, `reader_L` + `reader_R` the reader's little table with wax tablets and his painted sign (TRUE READINGS. FREE.).

```text
0x2DC 0x2DD 0x2DE 0x2DF   X X X X
```

Pieces: `hoop` 0x2DC, `board` 0x2DD, `reader_L` 0x2DE, `reader_R` 0x2DF.

Borrowed ground: grass at 0,0, 1,0, 2,0, 3,0.

#### Stone trough with spring water

`trough`, 2 wide by 1 tall. A long stone trough on borrowed (animated) water, fed by a spout at its west end: Eleutherai's spring, Phorbas's fold. Blocks.

```text
0x2E5 0x2E6   X X
```

Pieces: `W` 0x2E5, `E` 0x2E6.

Borrowed ground: sea at 0,0, 1,0.

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

(Written by hand; see each map's passes below.)
