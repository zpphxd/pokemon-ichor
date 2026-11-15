# stymphalia tileset catalog

`gTileset_Stymphalia` is Route 26, Lake Stymphalia and Route 27 (Act III, Lakonia; SCRIPT.md Part 10). It serves Route 26 (past the training grounds), Lake Stymphalia and Route 27 (over the hills into Arkadia). Pair it with the `aethos` primary, which supplies the open grass, paths, sand, sea, olives, cypresses and stone pines.

**This file is generated.** `tools/ichor/art/lakonia_build.py stymphalia` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/lakonia_*.py` (the plane tree is Kythera's), the palette plan, the water and the soft-edge autotiles in `lakonia_lib.py`.

| Image | Shows |
|---|---|
| [`img/stymphalia_boardwalk.png`](img/stymphalia_boardwalk.png) | A 240 x 160 screen of Lake Stymphalia: the boardwalk through the reeds, the causeway, Akanthis's stilt hut (3x; `stymphalia_boardwalk_1x.png` is 1x) |
| [`img/stymphalia_lake.png`](img/stymphalia_lake.png) | Lake Stymphalia: the causeway and boardwalks over the black water, the reed islets, the roosting reeds, the regrowing wall |
| [`img/stymphalia_platanistas.png`](img/stymphalia_platanistas.png) | Route 26's Platanistas: the plane-tree island in its moat, Herakles's and Lykourgos's bridges, the holm-oaks of the Skiritis |
| [`img/stymphalia_pieces.png`](img/stymphalia_pieces.png) | Every structure on its ground |
| [`img/stymphalia_sheet.png`](img/stymphalia_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

![A 240 x 160 screen of Lake Stymphalia: the boardwalk through the reeds, the causeway, Akanthis's stilt hut (3x; `stymphalia_boardwalk_1x.png` is 1x)](img/stymphalia_boardwalk.png)

It is one of the Lakonia family of secondaries; see [`TILES_lakonia.md`](TILES_lakonia.md) for why the art is split and which seams then need aethos-only strips.

**What comes from aethos (or elsewhere), not from here.** The running track and the goat paths are aethos path; the practice field's long grass is aethos's (`0x015`); Route 27's pines include aethos's stone pine beside the black pine here, and its oaks are the holm-oaks and walnuts; the Titans' lower road is aethos path under a `taygetos` lip and face; the great herms are aethos's.

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet (marsh at 0x200, water at 0x2D8, hills at 0x330). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/lakonia_tiles.py` holds every
Lakonia-family catalog as a Python dict (`mid('stymphalia', 'house', 'door')`, and
`blob_key(mask, x, y)` for the soft-edged pieces), and `build/stymphalia/catalog.json` is
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

**Animations.** Porytiles animations in this tileset, driven by `InitTilesetAnim_PorytilesManaged_Stymphalia` (`include/porytiles_generated/tilesets/stymphalia/generated_anim_code.h`): `eurotas`: the river's slow ripples drifting (3 frames); `glint`: bronze feathers catching the light in the roosting reeds (3 frames, mostly still); `marsh`: the black water, barely moving (3 frames, slow). Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet. Borrowed sea and shallows keep aethos's own animations.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of seven color
groups, one per secondary palette (`lakonia_lib.GROUPS`), passed to Porytiles as packing
hints:

| Group | Use |
|---|---|
| marsh | Stymphalia: black water, its reeds and mud, bronze feathers |
| river | The Eurotas: green water, its banks, reeds and pink oleander |
| veg | Plane, holm-oak, oak, walnut, willow; bark; the Sown Field |
| mount | Taygetos and the Skiritis: dark rock, scree, black pine; Malea's foam |
| wood | Timber and thatch: boardwalks, the stilt hut, racks, the barracks' roof, posts |
| stone | Plain stone, plaster and clay roofs: houses, the stoa, stelai, bridges, the causeway |

**Tile budget.** 462 of 504 tiles (416 metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.

**Scripted swaps.** The build writes the ids scripts swap to the `gTileset_Stymphalia` block at the end of `include/constants/metatile_labels.h`: `METATILE_Stymphalia_ReedWall`, `METATILE_Stymphalia_ReedWall_Cut`, `METATILE_Stymphalia_Drum_L`, `METATILE_Stymphalia_Drum_Moved`, `METATILE_Stymphalia_HammerRock`, `METATILE_Stymphalia_HammerRock_Broken`.

## Lake Stymphalia

### Lake Stymphalia: black water, muddy shores

`marsh`, 8 wide by 7 tall. Lake Stymphalia's still black water (animated, barely) between muddy grass shores, as all 47 soft-edge shapes; `1|11111111` is open water. Fresh water (`MB_POND_WATER`, surfable). Extra open-water cells: `rock`, a low rock in the water (the islets' rocks; the far rock with the item), `stump`, a drowned stump. Both impassable.

Shape keys (`blob_key`) and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x200 |
| `1|00000010` | 0x201 |
| `1|00001000` | 0x202 |
| `1|00001010` | 0x203 |
| `1|00001110` | 0x204 |
| `1|00100000` | 0x205 |
| `1|00100010` | 0x206 |
| `1|00101000` | 0x207 |
| `1|00101010` | 0x208 |
| `1|00101110` | 0x209 |
| `1|00111000` | 0x20A |
| `1|00111010` | 0x20B |
| `1|00111110` | 0x20C |
| `1|10000000` | 0x20D |
| `1|10000010` | 0x20E |
| `1|10000011` | 0x20F |
| `1|10001000` | 0x210 |
| `1|10001010` | 0x211 |
| `1|10001011` | 0x212 |
| `1|10001110` | 0x213 |
| `1|10001111` | 0x214 |
| `1|10100000` | 0x215 |
| `1|10100010` | 0x216 |
| `1|10100011` | 0x217 |
| `1|10101000` | 0x218 |
| `1|10101010` | 0x219 |
| `1|10101011` | 0x21A |
| `1|10101110` | 0x21B |
| `1|10101111` | 0x21C |
| `1|10111000` | 0x21D |
| `1|10111010` | 0x21E |
| `1|10111011` | 0x21F |
| `1|10111110` | 0x220 |
| `1|10111111` | 0x221 |
| `1|11100000` | 0x222 |
| `1|11100010` | 0x223 |
| `1|11100011` | 0x224 |
| `1|11101000` | 0x225 |
| `1|11101010` | 0x226 |
| `1|11101011` | 0x227 |
| `1|11101110` | 0x228 |
| `1|11101111` | 0x229 |
| `1|11111000` | 0x22A |
| `1|11111010` | 0x22B |
| `1|11111011` | 0x22C |
| `1|11111110` | 0x22D |
| `1|11111111` | 0x22E |

Every shape cell: walk `P`, `MB_POND_WATER`.

Extra cells:

| Id | Piece | Walk | Behavior | Layer |
|---|---|---|---|---|
| 0x22F | `rock` | `X` | `MB_NORMAL` | COVERED |
| 0x230 | `stump` | `X` | `MB_NORMAL` | COVERED |

### Stymphalia's reed grass in the shallows (tall grass)

`marsh_reeds`, 8 wide by 6 tall. Reed grass standing in the black water, on the islets and across the causeway (the forced band), as all 47 soft-edge shapes. `MB_TALL_GRASS`.

Shape keys (`blob_key`) and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x238 |
| `1|00000010` | 0x239 |
| `1|00001000` | 0x23A |
| `1|00001010` | 0x23B |
| `1|00001110` | 0x23C |
| `1|00100000` | 0x23D |
| `1|00100010` | 0x23E |
| `1|00101000` | 0x23F |
| `1|00101010` | 0x240 |
| `1|00101110` | 0x241 |
| `1|00111000` | 0x242 |
| `1|00111010` | 0x243 |
| `1|00111110` | 0x244 |
| `1|10000000` | 0x245 |
| `1|10000010` | 0x246 |
| `1|10000011` | 0x247 |
| `1|10001000` | 0x248 |
| `1|10001010` | 0x249 |
| `1|10001011` | 0x24A |
| `1|10001110` | 0x24B |
| `1|10001111` | 0x24C |
| `1|10100000` | 0x24D |
| `1|10100010` | 0x24E |
| `1|10100011` | 0x24F |
| `1|10101000` | 0x250 |
| `1|10101010` | 0x251 |
| `1|10101011` | 0x252 |
| `1|10101110` | 0x253 |
| `1|10101111` | 0x254 |
| `1|10111000` | 0x255 |
| `1|10111010` | 0x256 |
| `1|10111011` | 0x257 |
| `1|10111110` | 0x258 |
| `1|10111111` | 0x259 |
| `1|11100000` | 0x25A |
| `1|11100010` | 0x25B |
| `1|11100011` | 0x25C |
| `1|11101000` | 0x25D |
| `1|11101010` | 0x25E |
| `1|11101011` | 0x25F |
| `1|11101110` | 0x260 |
| `1|11101111` | 0x261 |
| `1|11111000` | 0x262 |
| `1|11111010` | 0x263 |
| `1|11111011` | 0x264 |
| `1|11111110` | 0x265 |
| `1|11111111` | 0x266 |

Every shape cell: walk `G`, `MB_TALL_GRASS`.

### Dense reed curtains

`curtain`, 8 wide by 6 tall. Reeds too thick to walk through, standing in black water: the curtain round the reed-bed nests (its gap is the way in) and the lake's walls, as all 47 soft-edge shapes. Impassable.

Shape keys (`blob_key`) and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x268 |
| `1|00000010` | 0x269 |
| `1|00001000` | 0x26A |
| `1|00001010` | 0x26B |
| `1|00001110` | 0x26C |
| `1|00100000` | 0x26D |
| `1|00100010` | 0x26E |
| `1|00101000` | 0x26F |
| `1|00101010` | 0x270 |
| `1|00101110` | 0x271 |
| `1|00111000` | 0x272 |
| `1|00111010` | 0x273 |
| `1|00111110` | 0x274 |
| `1|10000000` | 0x275 |
| `1|10000010` | 0x276 |
| `1|10000011` | 0x277 |
| `1|10001000` | 0x278 |
| `1|10001010` | 0x279 |
| `1|10001011` | 0x27A |
| `1|10001110` | 0x27B |
| `1|10001111` | 0x27C |
| `1|10100000` | 0x27D |
| `1|10100010` | 0x27E |
| `1|10100011` | 0x27F |
| `1|10101000` | 0x280 |
| `1|10101010` | 0x281 |
| `1|10101011` | 0x282 |
| `1|10101110` | 0x283 |
| `1|10101111` | 0x284 |
| `1|10111000` | 0x285 |
| `1|10111010` | 0x286 |
| `1|10111011` | 0x287 |
| `1|10111110` | 0x288 |
| `1|10111111` | 0x289 |
| `1|11100000` | 0x28A |
| `1|11100010` | 0x28B |
| `1|11100011` | 0x28C |
| `1|11101000` | 0x28D |
| `1|11101010` | 0x28E |
| `1|11101011` | 0x28F |
| `1|11101110` | 0x290 |
| `1|11101111` | 0x291 |
| `1|11111000` | 0x292 |
| `1|11111010` | 0x293 |
| `1|11111011` | 0x294 |
| `1|11111110` | 0x295 |
| `1|11111111` | 0x296 |

Every shape cell: walk `X`, `MB_NORMAL`.

### The bronze birds' roost (the north bed)

`roost`, 4 wide by 1 tall. The north shore's reed bed where the Stymphalian birds roost so thick nobody can walk in (LABORS's Stymphalian Reeds, Labor 6): a curtain of reeds with bronze feathers glinting in it (`glint`, animated). Run `L` `M` (`M_b`) `R` along the curtain's front. Impassable.

```text
ids                          walk
0x298 0x299 0x29A 0x29B   X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x298 | `L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x299 | `M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29A | `R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29B | `M_b` | `X` | `MB_NORMAL` | COVERED |  |

### The reed wall that grows back (the south-east bed)

`regrow`, 4 wide by 1 tall. The south-east shore's reed wall that grows back as fast as Demeter's Sickle cuts it (LABORS's Springs of Lerna, Labor 2): `wall` `wall_b` (impassable, a tangle of green new shoots among the old reeds) and `cut` `cut_b`, the same cells cut to stubble, which a script swaps in and out. Behind it, draw the eight pools with `marsh`.

```text
ids                          walk
0x29C 0x29D 0x29E 0x29F   X X . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x29C | `wall` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29D | `wall_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x29E | `cut` | `.` | `MB_NORMAL` | COVERED |  |
| 0x29F | `cut_b` | `.` | `MB_NORMAL` | COVERED |  |

### The old stone causeway on piles

`causeway`, 4 wide by 3 tall. The causeway from Stymphalia's south shore: old paving on stone piles over the black water, green with slime at the waterline. Two cells of it: north-south `V` (`V_b` a variant; `V_N` `V_S` end it on a bank), and east-west `H` (`H_W` `H_E` end it on a bank) with its south face `face` (`face_W` `face_E`) in the row below: piers and dark water between. `turn` joins a north-south run onto an east-west one (put `face_turn` under it). Deck walkable; face impassable.

```text
ids                          walk
0x2A0 0x2A1 0x2A2 0x2A3   . . . .
0x2A8 0x2A9 0x2AA 0x2AB   . . . .
0x2B0 0x2B1 0x2B2 0x2B3   X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2A0 | `V` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A1 | `V_b` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A2 | `V_N` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A3 | `V_S` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A8 | `H` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2A9 | `H_W` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2AA | `H_E` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2AB | `turn` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2B0 | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B1 | `face_W` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B2 | `face_E` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B3 | `face_turn` | `X` | `MB_NORMAL` | COVERED |  |

### Wooden boardwalks over the mud and water

`boardwalk`, 8 wide by 2 tall. Boardwalks of gray old planks on posts, one cell wide, threading the reed islets: `V` north-south, `H` east-west, `cross`, T-junctions (`T_E` has a branch east, and so on), corners (`NE` joins north and east, and so on) and ends (`end_N` is the north end of a run: its last plank, the open water beyond). `V_sit` is a run with a gap at its edge where Borboros sits with his legs over the side. Walkable; the water round them shows through.

```text
ids                                                  walk
0x2B8 0x2B9 0x2BA 0x2BB 0x2BC 0x2BD 0x2BE 0x2BF   . . . . . . . .
0x2C0 0x2C1 0x2C2 0x2C3 0x2C4 0x2C5 0x2C6 0x2C7   . . . . . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2B8 | `V` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2B9 | `H` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2BA | `cross` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2BB | `end_N` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2BC | `end_S` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2BD | `end_W` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2BE | `end_E` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2BF | `V_sit` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C0 | `T_E` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C1 | `T_W` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C2 | `T_N` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C3 | `T_S` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C4 | `NE` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C5 | `NW` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C6 | `SE` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C7 | `SW` | `.` | `MB_NORMAL` | COVERED |  |

### Akanthis's stilt hut

`stilt_hut`, 3 wide by 3 tall. The old fowler's hut on stilts beside the causeway (the rest point): a reed-thatched roof, walls of woven reed on a timber frame, nets drying, and a plank porch over the water where it meets the causeway. `door` (`MB_NON_ANIMATED_DOOR`) opens off the porch; the porch is walkable. The hidden item is under the hut.

```text
ids                    walk
0x2A4 0x2A5 0x2A6   X X X
0x2AC 0x2AD 0x2AE   X D X
0x2B4 0x2B5 0x2B6   . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2A4 | `roof_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A5 | `roof` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2A6 | `roof_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AC | `wall_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AD | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x2AE | `wall_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B4 | `porch_L` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2B5 | `porch` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2B6 | `porch_R` | `.` | `MB_NORMAL` | COVERED |  |

## Fresh water

### The Eurotas: green water, soft banks

`river`, 8 wide by 7 tall. The Eurotas, the Platanistas's moat and every stream: slow green water (animated) between soft grass banks with a fringe of reeds, as all 47 soft-edge shapes; kythera_lib.blob_key gives a cell's key from a water mask, and `1|11111111` is open water. Every cell is fresh water (`MB_POND_WATER`, surfable; fish from the bank). Extra open-water cells: `rock`, a flat rock the fisher stands on (impassable); `ford`, stepping stones across a side stream (walkable: lay a line of them); `tuft`, a clump of reeds in midstream (impassable).

Shape keys (`blob_key`) and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x2D8 |
| `1|00000010` | 0x2D9 |
| `1|00001000` | 0x2DA |
| `1|00001010` | 0x2DB |
| `1|00001110` | 0x2DC |
| `1|00100000` | 0x2DD |
| `1|00100010` | 0x2DE |
| `1|00101000` | 0x2DF |
| `1|00101010` | 0x2E0 |
| `1|00101110` | 0x2E1 |
| `1|00111000` | 0x2E2 |
| `1|00111010` | 0x2E3 |
| `1|00111110` | 0x2E4 |
| `1|10000000` | 0x2E5 |
| `1|10000010` | 0x2E6 |
| `1|10000011` | 0x2E7 |
| `1|10001000` | 0x2E8 |
| `1|10001010` | 0x2E9 |
| `1|10001011` | 0x2EA |
| `1|10001110` | 0x2EB |
| `1|10001111` | 0x2EC |
| `1|10100000` | 0x2ED |
| `1|10100010` | 0x2EE |
| `1|10100011` | 0x2EF |
| `1|10101000` | 0x2F0 |
| `1|10101010` | 0x2F1 |
| `1|10101011` | 0x2F2 |
| `1|10101110` | 0x2F3 |
| `1|10101111` | 0x2F4 |
| `1|10111000` | 0x2F5 |
| `1|10111010` | 0x2F6 |
| `1|10111011` | 0x2F7 |
| `1|10111110` | 0x2F8 |
| `1|10111111` | 0x2F9 |
| `1|11100000` | 0x2FA |
| `1|11100010` | 0x2FB |
| `1|11100011` | 0x2FC |
| `1|11101000` | 0x2FD |
| `1|11101010` | 0x2FE |
| `1|11101011` | 0x2FF |
| `1|11101110` | 0x300 |
| `1|11101111` | 0x301 |
| `1|11111000` | 0x302 |
| `1|11111010` | 0x303 |
| `1|11111011` | 0x304 |
| `1|11111110` | 0x305 |
| `1|11111111` | 0x306 |

Every shape cell: walk `P`, `MB_POND_WATER`.

Extra cells:

| Id | Piece | Walk | Behavior | Layer |
|---|---|---|---|---|
| 0x307 | `rock` | `X` | `MB_NORMAL` | COVERED |
| 0x308 | `ford` | `.` | `MB_NORMAL` | COVERED |
| 0x309 | `tuft` | `X` | `MB_NORMAL` | COVERED |

### The plain stone bridge, and footbridges

`bridge`, 4 wide by 1 tall. The Platanistas's two bridges and the hill streams': plank footbridges one cell wide, `foot_V` north-south (ended on the banks by `foot_V_N` `foot_V_S`), `foot_H` east-west. Walkable.

```text
ids                          walk
0x310 0x311 0x312 0x313   . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x310 | `foot_V` | `.` | `MB_NORMAL` | COVERED |  |
| 0x311 | `foot_H` | `.` | `MB_NORMAL` | COVERED |  |
| 0x312 | `foot_V_N` | `.` | `MB_NORMAL` | COVERED |  |
| 0x313 | `foot_V_S` | `.` | `MB_NORMAL` | COVERED |  |

### Herakles and Lykourgos at the Platanistas's bridges

`statues`, 2 wide by 2 tall. The Platanistas's two bridgeheads: Herakles in his lion skin with his club, and Lykourgos the lawgiver, bearded, with his staff, in old weathered marble (objects). Each is a head (drawn over the player) over a base (impassable). On borrowed grass.

```text
ids              walk
0x314 0x315   T T
0x31C 0x31D   X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x314 | `herakles` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x315 | `lykourgos` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x31C | `herakles_base` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x31D | `lykourgos_base` | `X` | `MB_NORMAL` | COVERED | grass |

## The hills

### Holm-oak, black pine and walnut

`trees`, 7 wide by 3 tall. The hill country's trees, on borrowed grass. The holm-oak (`holm_*`, 2 x 2): a dense dark evergreen crown, top row over the player. The black pine (`pine_*`, 2 x 3): tiers of dark needles high on Taygetos and the Skiritis, its top row over the player. The walnut (`walnut_XY`, 3 x 3): a broad pale-green crown on a gray trunk, the Karyai spring's trees. `holm_small` is a young holm-oak and `shrub` a kermes-oak bush, 1 x 1, impassable. Plant trunk rows impassable.

```text
ids                                            walk
0x330 0x331 0x332 0x333 0x334 0x335 0x336   T T T T T T T
0x338 0x339 0x33A 0x33B 0x33C 0x33D 0x33E   X X X X X X X
0x340 0x341 0x342 0x343 0x344 0x345 0x346   X X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x330 | `holm_TL` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x331 | `holm_TR` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x332 | `pine_TL` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x333 | `pine_TR` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x334 | `walnut_00` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x335 | `walnut_10` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x336 | `walnut_20` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x338 | `holm_BL` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x339 | `holm_BR` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x33A | `pine_ML` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x33B | `pine_MR` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x33C | `walnut_01` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x33D | `walnut_11` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x33E | `walnut_21` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x340 | `holm_small` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x341 | `shrub` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x342 | `pine_BL` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x343 | `pine_BR` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x344 | `walnut_02` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x345 | `walnut_12` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x346 | `walnut_22` | `X` | `MB_NORMAL` | COVERED | grass |

### Plane tree and apple trees

`plane`, 3 wide by 3 tall. The oriental plane (3 x 3), Lakonia's tree: a broad crown of maple-like leaves over a mottled pale trunk, on borrowed grass. Its top row is drawn over the player (`T`); the rest is impassable. (Kythera's painter: `kythera_land.trees`.)

```text
ids                    walk
0x348 0x349 0x34A   T T T
0x350 0x351 0x352   X X X
0x358 0x359 0x35A   X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x348 | `plane_00` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x349 | `plane_10` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x34A | `plane_20` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x350 | `plane_01` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x351 | `plane_11` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x352 | `plane_21` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x358 | `plane_02` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x359 | `plane_12` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x35A | `plane_22` | `X` | `MB_NORMAL` | COVERED | grass |

### Altars: Amyklai's fire, the Phoibaion

`phoibaion`, 2 wide by 1 tall. The Phoibaion on Route 26: the little old altar where the two teams made their offering before the fight, 2 x 1 on borrowed grass; the visible item sits on its step. Impassable.

```text
ids              walk
0x34B 0x34C   X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x34B | `cold_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x34C | `cold_R` | `X` | `MB_NORMAL` | COVERED | grass |

### A spring in a stone basin

`spring`, 2 wide by 2 tall. A spring welling into a stone basin under a carved spout, 2 x 2: Amyklai's spring beside the throne and the Karyai spring under the walnuts (both heal: put the bg event on the basin). The water is the Eurotas's, animated. Impassable; on borrowed grass outside the kerb.

```text
ids              walk
0x34D 0x34E   X X
0x355 0x356   X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x34D | `TL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x34E | `TR` | `X` | `MB_NORMAL` | COVERED |  |
| 0x355 | `BL` | `X` | `MB_NORMAL` | COVERED |  |
| 0x356 | `BR` | `X` | `MB_NORMAL` | COVERED |  |

### Track posts, the column drum, the Hammer rock

`odds`, 8 wide by 1 tall. On borrowed grass. `post`: the running track's turning post, a stone pillar (impassable); `start`: its starting sill, a grooved stone set in the ground (walkable). `drum_L` `drum_R`: a fallen column drum lying across a goat path, 2 x 1, that the Girdle of Herakles rolls aside; `drag` is the path after, scraped where it went. `hammer`: a cracked boulder the Bronze Hammer breaks; `rubble` what's left (walkable). `stele`: a weathered boundary stone (Lakonia | Arkadia, at Karyai).

```text
ids                                                  walk
0x360 0x361 0x362 0x363 0x364 0x365 0x366 0x367   X . X X . X . X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x360 | `post` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x361 | `start` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x362 | `drum_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x363 | `drum_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x364 | `drag` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x365 | `hammer` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x366 | `rubble` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x367 | `stele` | `X` | `MB_NORMAL` | COVERED | grass |

### The Skiritai watchtower

`tower`, 2 wide by 3 tall. The lookout spur's watchtower: a round tower of rough stone with a crenellated top, 2 x 3; its top is drawn over the player, its body impassable. `door` is a dark low doorway (`MB_NON_ANIMATED_DOOR`, or leave it closed). On borrowed grass.

```text
ids              walk
0x368 0x369   T T
0x370 0x371   X X
0x378 0x379   X D
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x368 | `top_L` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x369 | `top_R` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x370 | `mid_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x371 | `mid_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x378 | `base_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x379 | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED | grass |

### A ravine and its plank bridge

`ravine`, 3 wide by 3 tall. Route 27's ravine, running east-west across the path: `lip` (grass dropping away) over `chasm` (dark depths) over `foot` (the far wall's top, grass beyond); `_b` cells vary a run. The only way over is the plank bridge, one cell wide, north to south: `bridge_N` `bridge` `bridge_S` (Scout Othryades stands on it). Ravine impassable; the bridge walkable.

```text
ids                    walk
0x36A 0x36B 0x36C   X X .
0x372 0x373 0x374   X X .
0x37A 0x37B 0x37C   X X .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x36A | `lip` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x36B | `lip_b` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x36C | `bridge_N` | `.` | `MB_NORMAL` | COVERED |  |
| 0x372 | `chasm` | `X` | `MB_NORMAL` | COVERED |  |
| 0x373 | `chasm_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x374 | `bridge` | `.` | `MB_NORMAL` | COVERED |  |
| 0x37A | `foot` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x37B | `foot_b` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x37C | `bridge_S` | `.` | `MB_NORMAL` | COVERED |  |

### Taygetos: the dark wall

`taygetos`, 8 wide by 4 tall. The Skiritis's rock walls and the ridge above the Titans' road, Taygetos's rock (see `TILES_lakonia.md` for the kit): `lip` over `face` over `foot` for a south-facing wall, `side_E`/`side_W` and their feet for flanks, `back*` for a free-standing outcrop's north rim, `mass_*` (2 x 2) to fill. Loose `boulder`, `boulders`, and walkable `scree`.

```text
ids                                                  walk
0x380 0x381 0x382 0x383 0x384 0x385 0x386 0x387   X X X X X X X X
0x388 0x389 0x38A 0x38B 0x38C 0x38D 0x38E 0x38F   X X X X X X X X
0x390 0x391 0x392 0x393 0x394 0x395 0x396 0x397   X X X X X X X X
0x398 0x399 0x39A 0x39B 0x39C 0x39D 0x39E 0x39F   X . . . . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x380 | `mass_00` | `X` | `MB_NORMAL` | COVERED |  |
| 0x381 | `mass_10` | `X` | `MB_NORMAL` | COVERED |  |
| 0x382 | `mass_01` | `X` | `MB_NORMAL` | COVERED |  |
| 0x383 | `mass_11` | `X` | `MB_NORMAL` | COVERED |  |
| 0x384 | `lip` | `X` | `MB_NORMAL` | COVERED |  |
| 0x385 | `lip_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x386 | `lip_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x387 | `lip_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x388 | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x389 | `face_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x38A | `face_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x38B | `face_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x38C | `foot` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x38D | `foot_b` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x38E | `foot_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x38F | `foot_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x390 | `side_E` | `X` | `MB_NORMAL` | COVERED |  |
| 0x391 | `side_W` | `X` | `MB_NORMAL` | COVERED |  |
| 0x392 | `side_E_foot` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x393 | `side_W_foot` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x394 | `back` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x395 | `back_NW` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x396 | `back_NE` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x397 | `boulder` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x398 | `boulders` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x399 | `scree` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x39A | (2, 3) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x39B | (3, 3) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x39C | (4, 3) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x39D | (5, 3) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x39E | (6, 3) | `.` | `MB_NORMAL` | COVERED | grass |
| 0x39F | (7, 3) | `.` | `MB_NORMAL` | COVERED | grass |
