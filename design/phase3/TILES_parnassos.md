# Parnassos's tileset: Lebadeia and Route 9

The road west under Parnassos: Lebadeia in its gorge, where the Herkyna comes out of
the rock beside the springs of Lethe and Mnemosyne and the oracle's bronze grille; then
the Split Road, climbing through pale limestone, bay laurel and wild olive to the
crossroads where three roads meet, the lookout under Delphoi's cliffs, and the fallen
Phokian treasury above the cutting. One secondary on the `aethos` primary:

| Tileset | Maps |
|---|---|
| `gTileset_Parnassos` | `MAP_LEBADEIA`, `MAP_ROUTE9_SCHISTE` |

Both maps share it, so their seam (Lebadeia's west edge, Route 9's east edge) needs no
aethos-only strip. Kirrha and Aigion are on the harbors agent's own `kirrha` set
(BUILD.md), so this set carries only these two maps.

**This catalog is generated** by `tools/ichor/art/parnassos_build.py` (painters:
`parnassos_ground.py`, `_trees.py`, `_stone.py`, `_springs.py`, `_far.py`, `_houses.py`;
palettes in `parnassos_lib.py`, the soft-shape engine and crag painter borrowed from
Kithairon's). The render-and-critique passes at the end are written by hand and kept
across rebuilds.

**Place pieces by key and cell name** from `build/parnassos/catalog.json`, never by raw
id (`tools/ichor/maps/parnassos.py` does). Ids below are the current build's.

**Soft ground.** `tall`, `path`, `crag`, `water`, `pave` and `gully` hold one piece per
blob shape key: `1|` then the cell's neighbors N NE E SE S SW W NW. The map builder lists
the keys its maps use in `tools/ichor/art/parnassos_shapes.json`
(`parnassos.py --shapes`), and only those are drawn.

**Walk codes** in the grids: `X` blocks, `.` walkable, `T` walkable and drawn over the
player, `G` tall grass, `D` a door (MB_NON_ANIMATED_DOOR: put the warp there).

**Borrowed ground.** Cells on *grass*, *path*, *sea* or *tall* draw no ground of their own:
the build points their bottom tiles at aethos's grass (`0x001`), road (`0x1D9`), animated
water (`0x170`) or tall grass (`0x00D`). Rebuild the set whenever aethos is repainted.

**Palettes.** Seven groups, one per secondary palette; every 8x8 tile draws from one.

| Group | Use |
|---|---|
| field | tall grass, the road, the broken bridge's timber |
| rock | crags and their details, the Herkyna's banks, gullies, the grille, the spout, the ravine |
| tree | laurels, wild olives, planes, scrub |
| stone | paving, the herm, the boundary stone, altars, the ruin, drums, steps, bridges, the bench, the chair |
| water | the springs of Lethe and Mnemosyne |
| house | Eleusa's house kit, verbatim |
| far | the Phaidriades, Delphoi's roofs, the Kastalian falls |

**Scripted swaps** (`include/constants/metatile_labels.h`): `METATILE_Parnassos_Grille` and
`_GrilleOpen` (the oracle's grille, beat 35B), `_DrumGully`, `_DrumGully_B` and `_Drum` (the
treasury's drums at rest, beat 36C), and `_AltarApollo` (the shrine once cleansed).

## Budget

| Tileset | Tiles | Metatiles |
|---|---|---|
| `gTileset_Parnassos` | 498 of 504 | 272 of 512 |

![sheet](img/tiles_parnassos_sheet.png)

## Soft ground: grass, road, crags, the Herkyna, paving, gullies

### Tall grass with soft edges

`tall`, 8 wide by 2 tall. Barley tall grass on aethos grass, cut from one field so any outline works (agros's painter, as on every route). MB_TALL_GRASS throughout. Names are blob shape keys (`1|NNEESESSWWNW`).

15 shapes, from 0x200; the interior `1|11111111` is 0x200.

### The road with soft edges

`path`, 8 wide by 3 tall. The limestone road and its goat tracks, scalloped where they meet the grass (agros's painter). Names are blob shape keys.

23 shapes, from 0x210; the interior `1|11111111` is 0x210.

### Crags: pale limestone with a south face

`crag`, 8 wide by 4 tall. Parnassos's limestone seen from above, its south face showing, on aethos grass. Fill any region: the face appears along every south edge, with a shadow on the grass below. Impassable. Kithairon's painter, recolored. Names are blob shape keys.

28 shapes, from 0x228; the interior `1|11111111` is 0x228.

### The Herkyna: water with a pebbly bank

`water`, 8 wide by 2 tall. Aethos's animated water under a bank of pale pebbles and reeds. MB_POND_WATER: surf it with the Conch and fish it. Names are blob shape keys; the interior is `1|11111111`.

13 shapes, from 0x248; the interior `1|11111111` is 0x248.

### Paving: polygonal limestone flags

`pave`, 8 wide by 4 tall. Old polygonal flags, worn into the grass at their edges: the crossroads' triangle, Lebadeia's precinct, the treasury's floor. Walkable. Where paving meets the road, count the road as paving (and the paving as road) so they join without a grass seam. Names are blob shape keys.

25 shapes, from 0x258; the interior `1|11111111` is 0x258.

### Gullies: a dry ravine from above

`gully`, 8 wide by 2 tall. A dry gully: its far wall's face falls into a dark floor, the near lips catch the light. Impassable. The treasury's drums roll into one; the broken bridge spans another. Names are blob shape keys.

16 shapes, from 0x278; the interior `1|11111111` is 0x278.

### Crag detail: cracks, boulders, tufts, juniper

`crag_detail`, 2 wide by 1 tall. Interior crag cells to scatter through a big crag (Kithairon's, recolored): `crack`, `boulders`, `tuft`, `juniper`. Block.

```text
0x288 0x289   X X
```

Pieces: `crack` 0x288, `juniper` 0x289.

## Laurels, wild olives, plane trees, scrub, flowers

### Bay laurel (2 x 3)

`laurel`, 2 wide by 3 tall. Apollo's tree: a dense dark egg of glossy leaves on a slim grey trunk. The top row is drawn over the player.

```text
0x28A 0x28B   T T
0x292 0x293   X X
0x29A 0x29B   X X
```

### A laurel's base with the next laurel's crown over it

`laurel_stack`, 2 wide by 1 tall. Between two laurels in a column: the upper laurel's base row, the lower laurel's crown top over it. Blocks.

```text
0x28C 0x28D   X X
```

### Young laurel (1 x 2)

`laurel_young`, 1 wide by 2 tall. A sapling laurel for gaps in the scrub. Its top half is drawn over the player.

```text
0x28E   T
0x296   X
```

### Wild olive (2 x 2)

`wild_olive`, 2 wide by 2 tall. The oleaster of Parnassos's terraces: a gnarled two-stemmed trunk under thin silver-green leaves. The top row is drawn over the player.

```text
0x290 0x291   T T
0x298 0x299   X X
```

### Plane tree (3 x 3)

`plane`, 3 wide by 3 tall. The oriental plane of Lebadeia's grove: a great spreading crown over a pale mottled trunk. The top row and the bottom corners are drawn over the player; the trunk and the crown's middle row block.

```text
0x29C 0x29D 0x29E   T T T
0x2A4 0x2A5 0x2A6   X X X
0x2AC 0x2AD 0x2AE   T X T
```

### Scrub: kermes oak and laurel bushes

`scrub`, 2 wide by 1 tall. Low bushes for the laurel scrub along the road: `oak` a round kermes oak, `laurel` a young bay, `pair` two small bushes. Block.

```text
0x294 0x295   X X
```

Pieces: `oak` 0x294, `laurel` 0x295.

### Mountain flowers and a tussock

`meadow`, 2 wide by 1 tall. Walkable. Scatter through open grass with aethos's red anemones (0x004): `broom` yellow Spanish broom, `white` asphodel, `tuft` a tussock.

```text
0x2A0 0x2A1   . .
```

Pieces: `broom` 0x2A0, `white` 0x2A1.

## Worked stone: the herm, altars, the treasury's ruin, steps, bridges

### Stones and shrines of the Split Road

`markers`, 8 wide by 3 tall. On borrowed grass except the gully drums. `herm_top` over `herm`: the great herm. `stone_top` over `boundary`: the old boundary stone of the crossroads. `altar_top` over `altar` (or `altar_bad`, the god's face scratched with a sickle): Apollo's little marble altar. `cairn` the pilgrims' cairn; `bench_L`, `bench_R` the lookout's bench; `chair` the stone chair of Mnemosyne (walkable: the reading's seat); `drum` a column drum at rest; `drum_gully*` drums fallen into a gully (on the gully's floor, for the treasury's push puzzle); `capital`, `stump` Doric pieces; `rubble`, `feathers`, `dig`, `scree`, `scree_b` walkable; `boulder` a grey rock; `drum_b` a drum lying on its side.

```text
0x2B0 0x2B1 0x2B2 0x2B3 0x2B4 0x2B5 0x2B6 0x2B7   T T T . . . X X
0x2B8 0x2B9 0x2BA 0x2BB 0x2BC 0x2BD 0x2BE 0x2BF   X X X X X X X X
0x2C0 0x2C1 0x2C2 0x2C3 0x2C4 0x2C5 0x2C6 0x2C7   X X . . . . . .
```

Pieces: `herm_top` 0x2B0, `stone_top` 0x2B1, `altar_top` 0x2B2, `dig` 0x2B3, `rubble` 0x2B4, `feathers` 0x2B5, `bench_L` 0x2B6, `bench_R` 0x2B7, `herm` 0x2B8, `boundary` 0x2B9, `altar` 0x2BA, `altar_bad` 0x2BB, `cairn` 0x2BC, `drum` 0x2BD, `capital` 0x2BE, `boulder` 0x2BF, `drum_gully` 0x2C0, `drum_gully_b` 0x2C1, `scree` 0x2C2.

### The herm, the boundary stone and the chair, on paving

`pmarkers`, 5 wide by 1 tall. `markers`' `herm_top` over `herm`, `stone_top` over `boundary`, and `chair`, on the paving's flags instead of grass.

```text
0x2C8 0x2C9 0x2CA 0x2CB 0x2CC   T X T X .
```

Pieces: `herm_top` 0x2C8, `herm` 0x2C9, `stone_top` 0x2CA, `boundary` 0x2CB, `chair` 0x2CC.

### The treasury's broken walls

`ruin`, 8 wide by 1 tall. The Phokian treasury's ashlar, on borrowed grass. `W_L`, `W_M`, `W_R`: a west-east wall with its coping and south face; `W_low` the same broken low; `W_stub` a fallen end; `NS` a north-south wall seen from above, `NS_end` its south end with a bit of face; `door_L` a door jamb.

```text
0x2D0 0x2D1 0x2D2 0x2D3 0x2D4 0x2D5 0x2D6 0x2D7   X X X X X X X X
```

Pieces: `W_L` 0x2D0, `W_M` 0x2D1, `W_low` 0x2D2, `W_R` 0x2D3, `NS` 0x2D4, `NS_end` 0x2D5, `W_stub` 0x2D6, `door_L` 0x2D7.

### The pilgrims' steps

`steps`, 3 wide by 1 tall. Three pale limestone risers going down to the south: the steps of Lebadeia's precinct, where the pilgrims sit. West-east; walkable.

```text
0x2A8 0x2A9 0x2AA   . . .
```

Pieces: `L` 0x2A8, `M` 0x2A9, `R` 0x2AA.

### Stone bridges over the Herkyna

`bridge`, 4 wide by 2 tall. Over a river two cells wide. The road bridge is two rows: `N_L` `N_R` (its north parapet) over `S_L` `S_R` (its south parapet). The footbridge is one row, `F_L` `F_R`, parapets both sides. Walkable; count these cells as river when tiling the banks, so the water runs under.

```text
0x2D8 0x2D9 0x2DA 0x2DB   . . . .
0x2E0 0x2E1 0x2E2 0x2E3   . . . .
```

Pieces: `N_L` 0x2D8, `N_R` 0x2D9, `S_L` 0x2E0, `S_R` 0x2E1, `F_L` 0x2DA, `F_R` 0x2DB, `F_L2` 0x2E2, `F_R2` 0x2E3.

### The broken timber bridge

`timber`, 3 wide by 1 tall. A plank bridge over a gully three cells wide: `W`, `gap` (the middle planks fell: MB_ICHOR_GAP, so the Winged Talaria leap it at a run), `E`. Walkable but the gap. Count these cells as gully when tiling it.

```text
0x2CD 0x2CE 0x2CF   . X .
```

Pieces: `W` 0x2CD, `gap` 0x2CE, `E` 0x2CF.

## Lebadeia's precinct: the grille, the springs

### The oracle's rock: grille, spout, tablets

`face`, 5 wide by 1 tall. South-face cells of the crag (blob key `1|11100011`) over the precinct's paving, a shadowed foot at their base (`plain` the bare face). `grille` the bronze grille shut across Trophonios's cave mouth (blocks); `grille_open` swung back, MB_NON_ANIMATED_DOOR, the cave's warp (the map swaps it in when `FLAG_ICHOR_TROPHONIOS_GRILLE_OPEN` is set); `spout` the spring of Mnemosyne running out of the rock; `tablets` pilgrims' tablets hung on pegs.

```text
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC   X D X X X
```

Pieces: `grille` 0x2E8, `grille_open` 0x2E9, `spout` 0x2EA, `tablets` 0x2EB, `plain` 0x2EC.

### The spring of Lethe (2 x 2)

`lethe`, 2 wide by 2 tall. A square stone basin of black, still water: forgetting. Blocks. A hidden item can sit in it (the Bronze Obol someone threw in to forget something).

```text
0x2DC 0x2DD   X X
0x2E4 0x2E5   X X
```

Pieces: `NW` 0x2DC, `NE` 0x2DD, `SW` 0x2E4, `SE` 0x2E5.

### The spring of Mnemosyne (2 x 2)

`mnemosyne`, 2 wide by 2 tall. Bright running water in a stone rim, fed from the spout above (put `face`'s `spout` over its west column) and spilling east through a notch into the Herkyna: put the river's water cells against its east side and count these cells as water when tiling the river. Blocks.

```text
0x2DE 0x2DF   X X
0x2E6 0x2E7   X X
```

Pieces: `NW` 0x2DE, `NE` 0x2DF, `SW` 0x2E6, `SE` 0x2E7.

## The lookout's view: the Phaidriades and Delphoi, the ravine

### The far side: the Phaidriades and Delphoi

`far`, 8 wide by 2 tall. A backdrop across the lookout's ravine, from the top: cliff tops (`top_a`, `top_b`), faces (`face_a`, `face_b`) with the Kastalian gorge and its falls between them (`gorge_top`, `gorge`, `gorge_foot`), the cliffs' foot (`foot`, `foot_b`), the slope with the sanctuary (`slope`, `slope_b`, `temple_L` `temple_R`, `theater`, `roofs`), and `slope_foot` falling into the ravine. All block.

```text
0x2F0 0x2F1 0x2F2 0x2F3 0x2F4 0x2F5 0x2F6 0x2F7   X X X X X X X X
0x2F8 0x2F9 0x2FA 0x2FB 0x2FC 0x2FD 0x2FE 0x2FF   X X X X X X X X
```

Pieces: `top_a` 0x2F0, `face_a` 0x2F1, `face_b` 0x2F2, `gorge_top` 0x2F3, `gorge` 0x2F4, `gorge_foot` 0x2F5, `foot` 0x2F6, `slope` 0x2F7, `temple_L` 0x2F8, `temple_R` 0x2F9, `theater` 0x2FA, `roofs` 0x2FB, `slope_foot` 0x2FC.

### The ravine, and the lookout's lip

`ravine`, 1 wide by 1 tall. `dark` the ravine's depth; `mist` the same with a thread of mist; `lip` the lookout's near edge (grass to the south, the drop to the north; walkable, the player stops at it).

```text
0x28F   .
```

Pieces: `lip` 0x28F.

## Lebadeia's houses (Eleusa's kit)

### Tiled roof: ridge row and eave row

`roof_tile`, 3 wide by 2 tall. Red Laconian tiles. Repeat the middle column for a wider house.

```text
0x300 0x301 0x302   X X X
0x308 0x309 0x30A   X X X
```

Pieces: `R0_L` 0x300, `R0_M` 0x301, `R0_R` 0x302, `R1_L` 0x308, `R1_M` 0x309, `R1_R` 0x30A.

### Wall rows: upper and lower (on the socle)

`wall`, 3 wide by 2 tall. Plain plaster. Every window, door and extra below is a W0 or W1 M cell, so it can stand anywhere between the corners.

```text
0x303 0x304 0x305   X X X
0x30B 0x30C 0x30D   X X X
```

Pieces: `W0_L` 0x303, `W0_M` 0x304, `W0_R` 0x305, `W1_L` 0x30B, `W1_M` 0x30C, `W1_R` 0x30D.

### Upper-wall cells: windows and garlic

`windows`, 2 wide by 1 tall. W0 cells. `shutters` is an open window with ox-blood shutters, `lattice` a small timber grille, `closed` shutters shut, `garlic` strings of garlic and onions on a peg.

```text
0x2A2 0x2A3   X X
```

Pieces: `shutters` 0x2A2, `lattice` 0x2A3.

### Doors (lower-wall cells)

`doors`, 2 wide by 1 tall. W1 cells; every one is a door (MB_NON_ANIMATED_DOOR): put the warp there. `plank` a dark plank door in ox-blood jambs, `dutch` its top leaf open, `curtain` an arched doorway with a striped wool curtain, `barn_l` + `barn_r` a wide double door (warp on both).

```text
0x2ED 0x2EE   D D
```

Pieces: `plank` 0x2ED, `curtain` 0x2EE.

## Render-and-critique passes

(Written by hand.)
