# hesperides tileset catalog

`gTileset_Hesperides` is the Garden of the Hesperides and the Atlas range.  Pair it with the `aethos` primary, which supplies the open grass, the limestone path, sand, the sea, olives and cypresses. It is one of the far-west family (`far_west`, `hesperides`).

**This file is generated.** `tools/ichor/art/farlands_build.py hesperides` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/farlands_hesperides.py` (with `farlands_ground.py` and `farlands_kits.py`); the palette groups are in that file's `GROUPS`, the borrowed ground in `farlands_lib.py`.

| Image | Shows |
|---|---|
| [`img/farlands_hesperides_pieces.png`](img/farlands_hesperides_pieces.png) | Every structure on its ground (`*` marks the Oikoumene's pieces) |
| [`img/farlands_hesperides_sheet.png`](img/farlands_hesperides_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row, with the walk codes beside them. Each section starts on a fixed row of the sheet (garden at 0x200, tree at 0x250, stone at 0x290, atlas at 0x2D0). Structures are placed first-fit in build order, so appending one never moves another. Place pieces by key and name, never by raw id: `tools/ichor/maps/farlands_tiles.py` holds every far-lands catalog as a Python dict (`mid('hesperides', key, piece)`, and `soft('hesperides', key, region, x, y)` for soft ground); `build/hesperides/catalog.json` is the same as JSON.

**The Oikoumene's pieces** (drawn for world-oikoumene's lands, OIKOUMENE.md; `oikoumene_pieces('hesperides')` lists them): `snowline`, `cold`. The rest serve LABORS's maps first; both sessions may use anything here.

**Walk codes:**

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `T` | Passable, drawn over the player, who walks behind it. |
| `G` | Tall grass: `MB_TALL_GRASS`, wild encounters. Passable. |
| `D` | Door: `MB_NON_ANIMATED_DOOR`. Put the warp here. |
| `J` | Ledge: `MB_JUMP_SOUTH`. |
| `<` | Ledge: `MB_JUMP_WEST`. |
| `>` | Ledge: `MB_JUMP_EAST`. |

**Soft ground.** Grasses, roads, earth, mud and water come as 47 soft-edged shapes, keyed by a cell's neighbors (`farlands_lib.blob_key`, or `shape()` in `farlands_tiles.py`): `1|` then N NE E SE S SW W NW, 1 where the neighbor is in the region, a diagonal counting only when both its sides are. `1|11111111` is the full interior. Draw regions as irregular masks that follow the land (MAP_DESIGN 1: never plain rectangles); the shapes round every outer corner and wobble every edge.

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea*, *shallow* or *fall* draw no ground of their own: after Porytiles compiles, the build points their bottom-layer tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated sea (`0x170`), shallows (`0x0D1`) or waterfall (`0x0B3`). They meet aethos ground exactly and cost no tiles. A borrowed cell's art is in one layer: the middle (`COVERED`, under the player) or the top (`SPLIT`, over the player). Cells marked *drawn* paint their own ground, aethos's grass pixel for pixel where it shows.

**Seams.** MAP_DESIGN 5: the 6 rows (or 8 columns) nearest a connection to a map on a different secondary use only aethos metatiles. Everything here fades onto aethos ground, so a map can always end its soft regions before the strip: grass and earth shapes onto aethos grass, water onto aethos sea, roads through `road_join` onto aethos's limestone path patch (`1D0`-`1E2`).

**Animations.** Porytiles animations, driven by `InitTilesetAnim_PorytilesManaged_Hesperides` (`include/porytiles_generated/tilesets/hesperides/generated_anim_code.h`): `glint`: ; `splash`: ; `twinkle`: . Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player), `COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color groups, one per secondary palette (6-12), passed to Porytiles as packing hints.

| Group | Use | Colors |
|---|---|---|
| meadow |  | `hg0` `hg1` `hg2` `hg3` `hg4` `ap1` `ap2` `ap3` `ev0` `ev1` `w0` `pk1` `pk2` `gd` `g1` |
| tree |  | `hg0` `hg1` `hg2` `hg3` `hg4` `ap0` `ap1` `ap2` `ap3` `w0` `tb0` `tb1` `tb2` `gd` `ev0` |
| ladon |  | `ld0` `ld1` `ld2` `ld3` `ap1` `ap2` `ap3` `ink` `w0` `gd` `g1` `ev0` `hg1` |
| marble |  | `ml0` `ml1` `ml2` `ml3` `w0` `ev1` `ev2` `b2` `b3` `b4` `ap2` `hg1` `hg2` `pk1` `gd` |
| bower |  | `tb0` `tb1` `tb2` `tb3` `hg1` `hg2` `hg3` `pk1` `pk2` `ap2` `ap3` `ink` `w0` `gd` `ev1` |
| mountain |  | `cr0` `cr1` `cr2` `cr3` `sw1` `sw2` `w0` `ev0` `ev1` `gd` `g1` `ink` `mq1` `mq2` `hg0` |
| sky |  | `ns0` `ns1` `ns2` `ev1` `ev2` `ev3` `w0` `gl` `sw2` `cr1` `cr2` |

**Tile budget.** 360 of 504 tiles (320 metatiles). The door animations copy their frames into tiles 504-511, so the build fails past 504. Static tiles within two pixels of one another are merged.

**Scripted swaps.** The build writes the ids scripts swap to the `gTileset_Hesperides` block at the end of `include/constants/metatile_labels.h`: `METATILE_Hesperides_Ladon_Head`, `METATILE_Hesperides_Ladon_Coil`, `METATILE_Hesperides_Ladon_W`, `METATILE_Hesperides_Ladon_E`.

## Garden

### Evening meadow grass (encounters)

`garden_grass`, 8 wide by 6 tall. The garden's long grass in the evening: deep green going blue in the shadows, its seed heads catching the gold light, 47 soft-edge shapes over borrowed aethos grass. `MB_TALL_GRASS`: the optional grass where Applin fall (LABORS 11's map), and the meadows of the Atlas foothills.

Shape keys and their ids:

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

### Flowers, windfalls and myrtle

`decor`, 8 wide by 1 tall. On borrowed grass. Walkable: `lilies` (white), `asphodel` (pale gold spikes), `petals` (rose petals on the grass), `windfalls` (fallen golden apples: one of them a hidden item). Impassable: `roses`, a rose bush in flower; `myrtle_L` `myrtle` `myrtle_R`, a clipped myrtle hedge, west-east, to border paths and the bowers' lawns.

```
230 231 232 233 234 235 236 237    ....XXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `lilies` | 0x230 | `.` | grass | — |
| `asphodel` | 0x231 | `.` | grass | — |
| `petals` | 0x232 | `.` | grass | — |
| `windfalls` | 0x233 | `.` | grass | — |
| `roses` | 0x234 | `X` | grass | — |
| `myrtle_L` | 0x235 | `X` | grass | — |
| `myrtle` | 0x236 | `X` | grass | — |
| `myrtle_R` | 0x237 | `X` | grass | — |

## Tree

### The golden-apple tree

`apple_tree`, 4 wide by 4 tall. The tree Gaia gave Hera at her wedding, 4 x 4 on borrowed grass (`c00` to `c33`, column then row): a broad crown going blue in the evening, hung with golden apples lit as if from inside, a few of them glinting (the `glint` animation), over a gnarled trunk and roots. The crown's two rows are drawn over the player; the trunk row and the trunk's foot are impassable (put the tree's bg event on `c12` or `c22`). Ladon (`ladon`) coils round its foot.

```
250 251 252 253    TTTT
258 259 25A 25B    TTTT
260 261 262 263    XXXX
268 269 26A 26B    .XX.
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `c00` | 0x250 | `T` | grass | — |
| `c10` | 0x251 | `T` | grass | — |
| `c20` | 0x252 | `T` | grass | — |
| `c30` | 0x253 | `T` | grass | — |
| `c01` | 0x258 | `T` | grass | — |
| `c11` | 0x259 | `T` | grass | — |
| `c21` | 0x25A | `T` | grass | — |
| `c31` | 0x25B | `T` | grass | — |
| `c02` | 0x260 | `X` | grass | — |
| `c12` | 0x261 | `X` | grass | — |
| `c22` | 0x262 | `X` | grass | — |
| `c32` | 0x263 | `X` | grass | — |
| `c03` | 0x268 | `.` | grass | — |
| `c13` | 0x269 | `X` | grass | — |
| `c23` | 0x26A | `X` | grass | — |
| `c33` | 0x26B | `.` | grass | — |

### Ladon's coils

`ladon`, 6 wide by 2 tall. The serpent who never sleeps, asleep, coiled round the tree, as scenery on borrowed grass (impassable). Wrap the tree: `W_top` over `W` stand against the trunk row's west side, `E_top` over `E` its east; along the front, from west to east, `head` (resting on a coil, eye shut), then any run of `coil`, `coil_b`, `loop`, `loop_b`, ending in `tail` or `tail_b`. `coil_V` is a run going north-south. He is fought here (Melodrakon, LABORS 11); when he's caught or gone, swap every Ladon cell for aethos grass (`0x001`). Gold belly scales, green-teal back.

```
270 271 272 273 274 275    XXXXXX
278 279 27A 27B 27C 27D    XXXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `W_top` | 0x270 | `X` | grass | — |
| `W` | 0x278 | `X` | grass | — |
| `E_top` | 0x271 | `X` | grass | — |
| `E` | 0x279 | `X` | grass | — |
| `head` | 0x272 | `X` | grass | — |
| `coil` | 0x273 | `X` | grass | — |
| `coil_b` | 0x274 | `X` | grass | — |
| `tail` | 0x275 | `X` | grass | — |
| `loop` | 0x27A | `X` | grass | — |
| `loop_b` | 0x27B | `X` | grass | — |
| `tail_b` | 0x27C | `X` | grass | — |
| `coil_V` | 0x27D | `X` | grass | — |

## Stone

### The Hesperides' garden walls

`walls`, 6 wide by 2 tall. Low marble walls on borrowed grass, a gilded coping, climbing roses, impassable. `H_L` `H` `H_R` a west-east run (`H_roses` breaks it with roses); `gate_L` `gate_R` the posts either side of a two-cell gateway (leave the cells between them open); `V_T` `V` `V_B` a north-south run (`V_ivy` with ivy); `NW` and `NE` the corners where a west-east run turns south.

```
290 291 292 293 294 295    XXXXXX
298 299 29A 29B 29C 29D    XXXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `H_L` | 0x290 | `X` | grass | — |
| `H` | 0x291 | `X` | grass | — |
| `H_roses` | 0x292 | `X` | grass | — |
| `H_R` | 0x293 | `X` | grass | — |
| `gate_L` | 0x294 | `X` | grass | — |
| `gate_R` | 0x295 | `X` | grass | — |
| `V_T` | 0x298 | `X` | grass | — |
| `V` | 0x299 | `X` | grass | — |
| `V_B` | 0x29A | `X` | grass | — |
| `NW` | 0x29B | `X` | grass | — |
| `NE` | 0x29C | `X` | grass | — |
| `V_ivy` | 0x29D | `X` | grass | — |

### A fountain, and Arethousa's spring

`fountain`, 4 wide by 2 tall. On borrowed grass, impassable. The fountain (2 x 2, `TL` `TR` / `BL` `BR`): a marble basin with a jet that plays (`splash`). Arethousa's spring (2 x 2, `spring_*`): water welling up among mossy marble blocks into a round pool; the hidden Lansat Berry is by it (LABORS 11's map).

```
2A0 2A1 2A2 2A3    XXXX
2A8 2A9 2AA 2AB    XXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `TL` | 0x2A0 | `X` | grass | — |
| `TR` | 0x2A1 | `X` | grass | — |
| `BL` | 0x2A8 | `X` | grass | — |
| `BR` | 0x2A9 | `X` | grass | — |
| `spring_TL` | 0x2A2 | `X` | grass | — |
| `spring_TR` | 0x2A3 | `X` | grass | — |
| `spring_BL` | 0x2AA | `X` | grass | — |
| `spring_BR` | 0x2AB | `X` | grass | — |

### A nymph's bower

`bower`, 3 wide by 3 tall. Where a Hesperid lives (Aigle, Arethousa, Hespere: LABORS 11's three bowers), 3 x 3 on borrowed grass: a timber arbor roofed with vines and climbing roses, gold lamps hung under the eaves, a curtain of leaves over the door (`door`, `MB_NON_ANIMATED_DOOR`). Its top row is drawn over the player. Set each nymph's bower apart with what grows round it (`decor`'s lilies, asphodel, roses).

```
2A4 2A5 2A6    TTT
2AC 2AD 2AE    XXX
2B4 2B5 2B6    XDX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `c00` | 0x2A4 | `T` | grass | — |
| `c10` | 0x2A5 | `T` | grass | — |
| `c20` | 0x2A6 | `T` | grass | — |
| `c01` | 0x2AC | `X` | grass | — |
| `c11` | 0x2AD | `X` | grass | — |
| `c21` | 0x2AE | `X` | grass | — |
| `c02` | 0x2B4 | `X` | grass | — |
| `c12` | 0x2B5 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `c22` | 0x2B6 | `X` | grass | — |
| `door` | 0x2B5 | `D` | grass | MB_NON_ANIMATED_DOOR |

## Atlas

### Atlas's crags, snow on their brows

`crag`, 4 wide by 6 tall. How to build a crag: a plateau of high ground, its cells plain aethos grass. Its south edge is three rows: `lip` (the crest, grass above the rock's brow), `face` (bare rock; stack two for a taller cliff) and `foot` (the face's base, rubble and shadow on the ground, walkable). `_L` and `_R` end a run where the plateau's west and east edges turn north; `face_b` breaks up a long run. The west and east edges are `side_W` and `side_E` (a strip of rock falling away), the north edge `back` (a thin rim) with its corners `back_NW` and `back_NE`; `in_NW` and `in_NE` are inner corners where a south face meets a side running north. Everything but `foot` is impassable, on borrowed aethos grass. Use aethos's ledges (`087` and kin) for one-way drops. Cold blue-grey rock, its crests dusted with snow. Extra faces: `face_ice`, a face glazed with ice; `cave`, a cave mouth (`MB_NON_ANIMATED_DOOR`): the Atlas range's caves, Jirachi's and Moltres's climbs (the Oikoumene's). For Atlas's Ridge and the Oikoumene's Atlas foothills and range.

```
2D0 2D1 2D2 2D3    XXXX
2D8 2D9 2DA 2DB    XXXX
2E0 2E1 2E2 2E3    XXXX
2E8 2E9 2EA 2EB    XXXX
2F0 2F1 2F2 2F3    ....
2F8 2F9 2FA 2FB    XDXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `back_NW` | 0x2D0 | `X` | grass | — |
| `back` | 0x2D1 | `X` | grass | — |
| `back_NE` | 0x2D3 | `X` | grass | — |
| `side_W` | 0x2D8 | `X` | grass | — |
| `side_E` | 0x2DB | `X` | grass | — |
| `in_NW` | 0x2D9 | `X` | grass | — |
| `in_NE` | 0x2DA | `X` | grass | — |
| `lip_L` | 0x2E0 | `X` | grass | — |
| `lip` | 0x2E1 | `X` | grass | — |
| `lip_R` | 0x2E3 | `X` | grass | — |
| `face_L` | 0x2E8 | `X` | grass | — |
| `face` | 0x2E9 | `X` | grass | — |
| `face_b` | 0x2EA | `X` | grass | — |
| `face_R` | 0x2EB | `X` | grass | — |
| `foot_L` | 0x2F0 | `.` | grass | — |
| `foot` | 0x2F1 | `.` | grass | — |
| `foot_R` | 0x2F3 | `.` | grass | — |
| `face_ice` | 0x2F8 | `X` | grass | — |
| `cave` | 0x2F9 | `D` | grass | MB_NON_ANIMATED_DOOR |

### The snowline *(Oikoumene)*

`snowline`, 8 wide by 6 tall. Old snow lying in the hollows above the treeline, 47 soft-edge shapes over borrowed grass, walkable: the snowline transition the Atlas foothills climb through. Above it, whole fields of it; below, a patch or two in the shadow of a crag.

Shape keys and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x300 |
| `1|00000010` | 0x301 |
| `1|00001000` | 0x302 |
| `1|00001010` | 0x303 |
| `1|00001110` | 0x304 |
| `1|00100000` | 0x305 |
| `1|00100010` | 0x306 |
| `1|00101000` | 0x307 |
| `1|00101010` | 0x308 |
| `1|00101110` | 0x309 |
| `1|00111000` | 0x30A |
| `1|00111010` | 0x30B |
| `1|00111110` | 0x30C |
| `1|10000000` | 0x30D |
| `1|10000010` | 0x30E |
| `1|10000011` | 0x30F |
| `1|10001000` | 0x310 |
| `1|10001010` | 0x311 |
| `1|10001011` | 0x312 |
| `1|10001110` | 0x313 |
| `1|10001111` | 0x314 |
| `1|10100000` | 0x315 |
| `1|10100010` | 0x316 |
| `1|10100011` | 0x317 |
| `1|10101000` | 0x318 |
| `1|10101010` | 0x319 |
| `1|10101011` | 0x31A |
| `1|10101110` | 0x31B |
| `1|10101111` | 0x31C |
| `1|10111000` | 0x31D |
| `1|10111010` | 0x31E |
| `1|10111011` | 0x31F |
| `1|10111110` | 0x320 |
| `1|10111111` | 0x321 |
| `1|11100000` | 0x322 |
| `1|11100010` | 0x323 |
| `1|11100011` | 0x324 |
| `1|11101000` | 0x325 |
| `1|11101010` | 0x326 |
| `1|11101011` | 0x327 |
| `1|11101110` | 0x328 |
| `1|11101111` | 0x329 |
| `1|11111000` | 0x32A |
| `1|11111010` | 0x32B |
| `1|11111011` | 0x32C |
| `1|11111110` | 0x32D |
| `1|11111111` | 0x32E |

### Cold scrub, frost, scree and ledges *(Oikoumene)*

`cold`, 7 wide by 1 tall. On borrowed grass, for the high slopes. `cold_scrub` and `cold_scrub_b`: wind-cut juniper, rimed with frost (impassable). `frost_grass`: grass stiff with hoar-frost; `scree`: loose stones (both walkable). Ledges in the cold rock: `ledge_S` jumps south, `ledge_W` west, `ledge_E` east.

```
330 331 332 333 334 335 336    XX..J<>
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `cold_scrub` | 0x330 | `X` | grass | — |
| `cold_scrub_b` | 0x331 | `X` | grass | — |
| `frost_grass` | 0x332 | `.` | grass | — |
| `scree` | 0x333 | `.` | grass | — |
| `ledge_S` | 0x334 | `J` | grass | MB_JUMP_SOUTH |
| `ledge_W` | 0x335 | `<` | grass | MB_JUMP_WEST |
| `ledge_E` | 0x336 | `>` | grass | MB_JUMP_EAST |

### The summit edge, where the sky hangs low

`low_sky`, 6 wide by 1 tall. The sky's underside, sagging down onto the summit (LABORS 11's Atlas's Ridge, and the Oikoumene's Atlas range, where Jirachi waits): a dark blue weight full of stars, its lower edge glowing. Impassable, drawn whole. `sky` and `sky_b` fill the top of the map; `rim` and `rim_b` are its lower edge over the summit's snow (the sky above, a glowing seam, then snow), `rim_L` and `rim_R` the ends where it lifts away. Its stars twinkle (`twinkle`).

```
338 339 33A 33B 33C 33D    XXXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `sky` | 0x338 | `X` | drawn | — |
| `sky_b` | 0x339 | `X` | drawn | — |
| `rim_L` | 0x33A | `X` | drawn | — |
| `rim` | 0x33B | `X` | drawn | — |
| `rim_b` | 0x33C | `X` | drawn | — |
| `rim_R` | 0x33D | `X` | drawn | — |
