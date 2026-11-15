# far_west tileset catalog

`gTileset_FarWest` is the far west: Erytheia, the Pillars, the Ocean Stream.  Pair it with the `aethos` primary, which supplies the open grass, the limestone path, sand, the sea, olives and cypresses. It is one of the far-west family (`far_west`, `hesperides`).

**This file is generated.** `tools/ichor/art/farlands_build.py far_west` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/farlands_far_west.py` (with `farlands_ground.py` and `farlands_kits.py`); the palette groups are in that file's `GROUPS`, the borrowed ground in `farlands_lib.py`.

| Image | Shows |
|---|---|
| [`img/farlands_far_west_pieces.png`](img/farlands_far_west_pieces.png) | Every structure on its ground (`*` marks the Oikoumene's pieces) |
| [`img/farlands_far_west_sheet.png`](img/farlands_far_west_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row, with the walk codes beside them. Each section starts on a fixed row of the sheet (ground at 0x200, coast at 0x300, rock at 0x328, pillars at 0x370, places at 0x3B0). Structures are placed first-fit in build order, so appending one never moves another. Place pieces by key and name, never by raw id: `tools/ichor/maps/farlands_tiles.py` holds every far-lands catalog as a Python dict (`mid('far_west', key, piece)`, and `soft('far_west', key, region, x, y)` for soft ground); `build/far_west/catalog.json` is the same as JSON.

**The Oikoumene's pieces** (drawn for world-oikoumene's lands, OIKOUMENE.md; `oikoumene_pieces('far_west')` lists them): `river`, `sea_marks`, `stacks`, `ledges`. The rest serve LABORS's maps first; both sessions may use anything here.

**Walk codes:**

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
| `<` | Ledge: `MB_JUMP_WEST`. |
| `>` | Ledge: `MB_JUMP_EAST`. |

**Soft ground.** Grasses, roads, earth, mud and water come as 47 soft-edged shapes, keyed by a cell's neighbors (`farlands_lib.blob_key`, or `shape()` in `farlands_tiles.py`): `1|` then N NE E SE S SW W NW, 1 where the neighbor is in the region, a diagonal counting only when both its sides are. `1|11111111` is the full interior. Draw regions as irregular masks that follow the land (MAP_DESIGN 1: never plain rectangles); the shapes round every outer corner and wobble every edge.

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea*, *shallow* or *fall* draw no ground of their own: after Porytiles compiles, the build points their bottom-layer tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated sea (`0x170`), shallows (`0x0D1`) or waterfall (`0x0B3`). They meet aethos ground exactly and cost no tiles. A borrowed cell's art is in one layer: the middle (`COVERED`, under the player) or the top (`SPLIT`, over the player). Cells marked *drawn* paint their own ground, aethos's grass pixel for pixel where it shows.

**Seams.** MAP_DESIGN 5: the 6 rows (or 8 columns) nearest a connection to a map on a different secondary use only aethos metatiles. Everything here fades onto aethos ground, so a map can always end its soft regions before the strip: grass and earth shapes onto aethos grass, water onto aethos sea, roads through `road_join` onto aethos's limestone path patch (`1D0`-`1E2`).

**Animations.** Porytiles animations, driven by `InitTilesetAnim_PorytilesManaged_FarWest` (`include/porytiles_generated/tilesets/far_west/generated_anim_code.h`): `breakers`: ; `glow`: ; `surf`: ; `twinkle`: . Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player), `COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color groups, one per secondary palette (6-12), passed to Porytiles as packing hints.

| Group | Use | Colors |
|---|---|---|
| red |  | `g1` `g2` `g3` `gd` `re0` `re1` `re2` `re3` `re4` `ks1` `ks2` `p3` `md0` `b2` `b4` |
| dusk |  | `dg0` `dg1` `dg2` `dg3` `dg4` `ev0` `ev1` `sl0` `sl1` `sl2` `ns0` `ns1` `ns2` `gl` `w0` |
| sea |  | `b1` `b2` `b3` `b4` `w0` `pk1` `pk2` `gl` `ks1` `ks2` `p3` `ev1` `ev2` `ev3` `ns1` |
| rock |  | `rr0` `rr1` `rr2` `rr3` `rr4` `ev0` `ev1` `gd` `g1` `w0` `b3` `b4` `gl` `ink` `mq1` |
| scrub |  | `mq0` `mq1` `mq2` `mq3` `tg` `pk1` `w0` `gd` `g1` `dg2` `dg3` `re1` `rb1` `ev1` |
| marble |  | `ml0` `ml1` `ml2` `ml3` `w0` `gl` `ev1` `ev2` `ink` `gd` `g1` `b3` `ap1` `ap2` `ap3` |
| works |  | `tb0` `tb1` `tb2` `tb3` `dg1` `dg2` `dg3` `rr1` `rr2` `rr3` `rr4` `ink` `gd` `g1` `ev1` |

**Tile budget.** 463 of 504 tiles (464 metatiles). The door animations copy their frames into tiles 504-511, so the build fails past 504. Static tiles within two pixels of one another are merged.

## Ground

### Red earth

`red_earth`, 8 wide by 6 tall. Erytheia's ground: iron-red earth, cracked and pebbled, 47 soft-edge shapes over borrowed aethos grass. Walkable. Use it for the island's open ground, cattle tracks (a region one cell wide) and the trodden ground round the hut and the den; aethos grass shows between. Its edge fades onto aethos grass, so a seam strip can be grass.

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

### Red earth on sand

`red_earth_sand`, 8 wide by 6 tall. The same 47 shapes over borrowed aethos sand (the same tiles: only the ground differs), for where red earth runs down to a beach.

Shape keys and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x230 |
| `1|00000010` | 0x231 |
| `1|00001000` | 0x232 |
| `1|00001010` | 0x233 |
| `1|00001110` | 0x234 |
| `1|00100000` | 0x235 |
| `1|00100010` | 0x236 |
| `1|00101000` | 0x237 |
| `1|00101010` | 0x238 |
| `1|00101110` | 0x239 |
| `1|00111000` | 0x23A |
| `1|00111010` | 0x23B |
| `1|00111110` | 0x23C |
| `1|10000000` | 0x23D |
| `1|10000010` | 0x23E |
| `1|10000011` | 0x23F |
| `1|10001000` | 0x240 |
| `1|10001010` | 0x241 |
| `1|10001011` | 0x242 |
| `1|10001110` | 0x243 |
| `1|10001111` | 0x244 |
| `1|10100000` | 0x245 |
| `1|10100010` | 0x246 |
| `1|10100011` | 0x247 |
| `1|10101000` | 0x248 |
| `1|10101010` | 0x249 |
| `1|10101011` | 0x24A |
| `1|10101110` | 0x24B |
| `1|10101111` | 0x24C |
| `1|10111000` | 0x24D |
| `1|10111010` | 0x24E |
| `1|10111011` | 0x24F |
| `1|10111110` | 0x250 |
| `1|10111111` | 0x251 |
| `1|11100000` | 0x252 |
| `1|11100010` | 0x253 |
| `1|11100011` | 0x254 |
| `1|11101000` | 0x255 |
| `1|11101010` | 0x256 |
| `1|11101011` | 0x257 |
| `1|11101110` | 0x258 |
| `1|11101111` | 0x259 |
| `1|11111000` | 0x25A |
| `1|11111010` | 0x25B |
| `1|11111011` | 0x25C |
| `1|11111110` | 0x25D |
| `1|11111111` | 0x25E |

### Sunset grass (encounters)

`dusk_grass`, 8 wide by 6 tall. Tall grass lit by a sun that never quite sets: gold blades, violet shadows between them, 47 soft-edge shapes over borrowed aethos grass. `MB_TALL_GRASS`. The forced bands and the optional fields of Erytheia and the pasture.

Shape keys and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x260 |
| `1|00000010` | 0x261 |
| `1|00001000` | 0x262 |
| `1|00001010` | 0x263 |
| `1|00001110` | 0x264 |
| `1|00100000` | 0x265 |
| `1|00100010` | 0x266 |
| `1|00101000` | 0x267 |
| `1|00101010` | 0x268 |
| `1|00101110` | 0x269 |
| `1|00111000` | 0x26A |
| `1|00111010` | 0x26B |
| `1|00111110` | 0x26C |
| `1|10000000` | 0x26D |
| `1|10000010` | 0x26E |
| `1|10000011` | 0x26F |
| `1|10001000` | 0x270 |
| `1|10001010` | 0x271 |
| `1|10001011` | 0x272 |
| `1|10001110` | 0x273 |
| `1|10001111` | 0x274 |
| `1|10100000` | 0x275 |
| `1|10100010` | 0x276 |
| `1|10100011` | 0x277 |
| `1|10101000` | 0x278 |
| `1|10101010` | 0x279 |
| `1|10101011` | 0x27A |
| `1|10101110` | 0x27B |
| `1|10101111` | 0x27C |
| `1|10111000` | 0x27D |
| `1|10111010` | 0x27E |
| `1|10111011` | 0x27F |
| `1|10111110` | 0x280 |
| `1|10111111` | 0x281 |
| `1|11100000` | 0x282 |
| `1|11100010` | 0x283 |
| `1|11100011` | 0x284 |
| `1|11101000` | 0x285 |
| `1|11101010` | 0x286 |
| `1|11101011` | 0x287 |
| `1|11101110` | 0x288 |
| `1|11101111` | 0x289 |
| `1|11111000` | 0x28A |
| `1|11111010` | 0x28B |
| `1|11111011` | 0x28C |
| `1|11111110` | 0x28D |
| `1|11111111` | 0x28E |

### Sunset grass on red earth (encounters)

`dusk_grass_red`, 8 wide by 6 tall. The same grass growing out of red earth: its edges fade onto `red_earth`'s full interior. Lay it inside a red-earth region (a cell of it next to plain grass would show red earth there, so keep a cell of red earth round it).

Shape keys and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x290 |
| `1|00000010` | 0x291 |
| `1|00001000` | 0x292 |
| `1|00001010` | 0x293 |
| `1|00001110` | 0x294 |
| `1|00100000` | 0x295 |
| `1|00100010` | 0x296 |
| `1|00101000` | 0x297 |
| `1|00101010` | 0x298 |
| `1|00101110` | 0x299 |
| `1|00111000` | 0x29A |
| `1|00111010` | 0x29B |
| `1|00111110` | 0x29C |
| `1|10000000` | 0x29D |
| `1|10000010` | 0x29E |
| `1|10000011` | 0x29F |
| `1|10001000` | 0x2A0 |
| `1|10001010` | 0x2A1 |
| `1|10001011` | 0x2A2 |
| `1|10001110` | 0x2A3 |
| `1|10001111` | 0x2A4 |
| `1|10100000` | 0x2A5 |
| `1|10100010` | 0x2A6 |
| `1|10100011` | 0x2A7 |
| `1|10101000` | 0x2A8 |
| `1|10101010` | 0x2A9 |
| `1|10101011` | 0x2AA |
| `1|10101110` | 0x2AB |
| `1|10101111` | 0x2AC |
| `1|10111000` | 0x2AD |
| `1|10111010` | 0x2AE |
| `1|10111011` | 0x2AF |
| `1|10111110` | 0x2B0 |
| `1|10111111` | 0x2B1 |
| `1|11100000` | 0x2B2 |
| `1|11100010` | 0x2B3 |
| `1|11100011` | 0x2B4 |
| `1|11101000` | 0x2B5 |
| `1|11101010` | 0x2B6 |
| `1|11101011` | 0x2B7 |
| `1|11101110` | 0x2B8 |
| `1|11101111` | 0x2B9 |
| `1|11111000` | 0x2BA |
| `1|11111010` | 0x2BB |
| `1|11111011` | 0x2BC |
| `1|11111110` | 0x2BD |
| `1|11111111` | 0x2BE |

### A river *(Oikoumene)*

`river`, 8 wide by 6 tall. Fresh water (`MB_POND_WATER`) over borrowed aethos sea, its banks cut in red earth: 47 soft-edge shapes of the water, the land side of an edge cell drawn as aethos grass pixel for pixel. The Baetis below Tartessos's silver mines, and the brooks of Erytheia.

Shape keys and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x2C0 |
| `1|00000010` | 0x2C1 |
| `1|00001000` | 0x2C2 |
| `1|00001010` | 0x2C3 |
| `1|00001110` | 0x2C4 |
| `1|00100000` | 0x2C5 |
| `1|00100010` | 0x2C6 |
| `1|00101000` | 0x2C7 |
| `1|00101010` | 0x2C8 |
| `1|00101110` | 0x2C9 |
| `1|00111000` | 0x2CA |
| `1|00111010` | 0x2CB |
| `1|00111110` | 0x2CC |
| `1|10000000` | 0x2CD |
| `1|10000010` | 0x2CE |
| `1|10000011` | 0x2CF |
| `1|10001000` | 0x2D0 |
| `1|10001010` | 0x2D1 |
| `1|10001011` | 0x2D2 |
| `1|10001110` | 0x2D3 |
| `1|10001111` | 0x2D4 |
| `1|10100000` | 0x2D5 |
| `1|10100010` | 0x2D6 |
| `1|10100011` | 0x2D7 |
| `1|10101000` | 0x2D8 |
| `1|10101010` | 0x2D9 |
| `1|10101011` | 0x2DA |
| `1|10101110` | 0x2DB |
| `1|10101111` | 0x2DC |
| `1|10111000` | 0x2DD |
| `1|10111010` | 0x2DE |
| `1|10111011` | 0x2DF |
| `1|10111110` | 0x2E0 |
| `1|10111111` | 0x2E1 |
| `1|11100000` | 0x2E2 |
| `1|11100010` | 0x2E3 |
| `1|11100011` | 0x2E4 |
| `1|11101000` | 0x2E5 |
| `1|11101010` | 0x2E6 |
| `1|11101011` | 0x2E7 |
| `1|11101110` | 0x2E8 |
| `1|11101111` | 0x2E9 |
| `1|11111000` | 0x2EA |
| `1|11111010` | 0x2EB |
| `1|11111011` | 0x2EC |
| `1|11111110` | 0x2ED |
| `1|11111111` | 0x2EE |

### Maquis: lentisk, dwarf palm, broom, cistus

`scrub`, 6 wide by 1 tall. Low scrub on borrowed grass, lit from the west. Impassable: `lentisk` and `lentisk_b`, dark glossy mastic bushes; `palm`, a dwarf fan-palm; `broom`, in yellow flower. Walkable: `cistus`, a low rock-rose with pink flowers; `thistle`, a few purple-headed thistles. Scatter them on grass and red earth's edges; line a cattle track with them.

```
2F0 2F1 2F2 2F3 2F4 2F5    XXXX..
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `lentisk` | 0x2F0 | `X` | grass | — |
| `lentisk_b` | 0x2F1 | `X` | grass | — |
| `palm` | 0x2F2 | `X` | grass | — |
| `broom` | 0x2F3 | `X` | grass | — |
| `cistus` | 0x2F4 | `.` | grass | — |
| `thistle` | 0x2F5 | `.` | grass | — |

### Red boulders and slag heaps

`rocks`, 4 wide by 1 tall. On borrowed grass, impassable: `boulder` and `boulders`, red rock lit gold on its western face, violet in shadow. `slag` and `slag_b`: heaps of glassy black slag from the silver smelters round Tartessos (the Oikoumene's).

```
2F8 2F9 2FA 2FB    XXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `boulder` | 0x2F8 | `X` | grass | — |
| `boulders` | 0x2F9 | `X` | grass | — |
| `slag` | 0x2FA | `X` | grass | — |
| `slag_b` | 0x2FB | `X` | grass | — |

## Coast

### The sunset surf

`surf`, 6 wide by 2 tall. Where sand meets the evening sea: each cell borrows aethos's animated sea and draws the sand down to the waterline (aethos sand pixel for pixel, so it meets plain aethos sand `0x124`), wet sand gone gold, and foam lit pink by the low sun, washing up and back (the `surf` animation). Named by where the sea is: `S` (sand north, sea south), `N`, `E`, `W`; `out_NW` is a sand spit's south-east tip (sand to the north-west), and so on; `in_SE` is a cove's corner, sea only to the south-east. Every cell is `MB_OCEAN_WATER`, as aethos's beach edges are. Where a far-west beach meets a seam, end it with aethos's own sand and sea.

```
300 301 302 303 304 305    WWWWWW
308 309 30A 30B 30C 30D    WWWWWW
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `S` | 0x300 | `W` | sea | MB_OCEAN_WATER |
| `N` | 0x301 | `W` | sea | MB_OCEAN_WATER |
| `E` | 0x302 | `W` | sea | MB_OCEAN_WATER |
| `W` | 0x303 | `W` | sea | MB_OCEAN_WATER |
| `out_NW` | 0x304 | `W` | sea | MB_OCEAN_WATER |
| `out_NE` | 0x305 | `W` | sea | MB_OCEAN_WATER |
| `out_SW` | 0x308 | `W` | sea | MB_OCEAN_WATER |
| `out_SE` | 0x309 | `W` | sea | MB_OCEAN_WATER |
| `in_SE` | 0x30A | `W` | sea | MB_OCEAN_WATER |
| `in_SW` | 0x30B | `W` | sea | MB_OCEAN_WATER |
| `in_NE` | 0x30C | `W` | sea | MB_OCEAN_WATER |
| `in_NW` | 0x30D | `W` | sea | MB_OCEAN_WATER |

### Atlantic breakers and the sun's road *(Oikoumene)*

`sea_marks`, 4 wide by 1 tall. Over borrowed aethos sea, surfable. `breaker` and `breaker_b`: a big Atlantic roller, a long crest of white water curling and spilling as it comes in (the `breakers` animation); lay them in staggered rows two to four cells off a beach for the Atlantic shore. `sun_road` and `sun_road_b`: the setting sun's glitter on the water, pink and gold, twinkling (`twinkle`); lay a band of them due west of a headland, toward the sunset.

```
310 311 312 313    WWWW
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `breaker` | 0x310 | `W` | sea | MB_OCEAN_WATER |
| `breaker_b` | 0x311 | `W` | sea | MB_OCEAN_WATER |
| `sun_road` | 0x312 | `W` | sea | MB_OCEAN_WATER |
| `sun_road_b` | 0x313 | `W` | sea | MB_OCEAN_WATER |

### Sea stacks and tide pools *(Oikoumene)*

`stacks`, 4 wide by 2 tall. `stack` (2 x 2): a red sea stack standing out of the water, lit gold on its western face, foam round its foot; its top row is drawn over the player. `stack_small` (1 x 2, with `stack_small_top`): a lone pinnacle. Both stand on borrowed sea, impassable. `pool` and `pool_b`: rock shelves with tide pools and weed (on borrowed sand), impassable, for the Atlantic shore at low tide.

```
314 315 316 317    TTTX
31C 31D 31E 31F    XXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `stack_TL` | 0x314 | `T` | sea | — |
| `stack_TR` | 0x315 | `T` | sea | — |
| `stack_BL` | 0x31C | `X` | sea | — |
| `stack_BR` | 0x31D | `X` | sea | — |
| `stack_small` | 0x31E | `X` | sea | — |
| `pool` | 0x31F | `X` | sand | — |
| `pool_b` | 0x317 | `X` | sand | — |
| `stack_small_top` | 0x316 | `T` | sea | — |

## Rock

### Red crags

`crag`, 4 wide by 7 tall. How to build a crag: a plateau of high ground, its cells plain aethos grass. Its south edge is three rows: `lip` (the crest, grass above the rock's brow), `face` (bare rock; stack two for a taller cliff) and `foot` (the face's base, rubble and shadow on the ground, walkable). `_L` and `_R` end a run where the plateau's west and east edges turn north; `face_b` breaks up a long run. The west and east edges are `side_W` and `side_E` (a strip of rock falling away), the north edge `back` (a thin rim) with its corners `back_NW` and `back_NE`; `in_NW` and `in_NE` are inner corners where a south face meets a side running north. Everything but `foot` is impassable, on borrowed aethos grass. Use aethos's ledges (`087` and kin) for one-way drops. Red rock lit from the west, its shadows violet. Extra pieces: `face_lit`, a face the sunset strikes full on; `foot_sea_L` `foot_sea` `foot_sea_R`, a face whose foot stands in the sea (borrowed sea, foam at the base; surfable), for Erytheia's and the Atlantic's sea cliffs and the Strait's headlands; `cave`, a cave mouth (Orthros's den, the Atlas range's caves); `mine`, a timber-framed mine head (Tartessos's silver mines, the Oikoumene's). `cave` and `mine` are `MB_NON_ANIMATED_DOOR`.

```
328 329 32A 32B    XXXX
330 331 332 333    XXXX
338 339 33A 33B    XXXX
340 341 342 343    XXXX
348 349 34A 34B    ....
350 351 352 353    XWWW
358 359 35A 35B    DDXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `back_NW` | 0x328 | `X` | grass | — |
| `back` | 0x329 | `X` | grass | — |
| `back_NE` | 0x32B | `X` | grass | — |
| `side_W` | 0x330 | `X` | grass | — |
| `side_E` | 0x333 | `X` | grass | — |
| `in_NW` | 0x331 | `X` | grass | — |
| `in_NE` | 0x332 | `X` | grass | — |
| `lip_L` | 0x338 | `X` | grass | — |
| `lip` | 0x339 | `X` | grass | — |
| `lip_R` | 0x33B | `X` | grass | — |
| `face_L` | 0x340 | `X` | grass | — |
| `face` | 0x341 | `X` | grass | — |
| `face_b` | 0x342 | `X` | grass | — |
| `face_R` | 0x343 | `X` | grass | — |
| `foot_L` | 0x348 | `.` | grass | — |
| `foot` | 0x349 | `.` | grass | — |
| `foot_R` | 0x34B | `.` | grass | — |
| `face_lit` | 0x350 | `X` | grass | — |
| `foot_sea_L` | 0x351 | `W` | sea | MB_OCEAN_WATER |
| `foot_sea` | 0x352 | `W` | sea | MB_OCEAN_WATER |
| `foot_sea_R` | 0x353 | `W` | sea | MB_OCEAN_WATER |
| `cave` | 0x358 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `mine` | 0x359 | `D` | grass | MB_NON_ANIMATED_DOOR |

### Red-rock ledges *(Oikoumene)*

`ledges`, 5 wide by 1 tall. One-way drops in red rock on borrowed grass: `S_L` `S` `S_R` jump south (a run and its ends), `W` jumps west, `E` east. For Erytheia's gully, the Atlas foothills' steep slopes and the Oikoumene's red uplands.

```
360 361 362 363 364    JJJ<>
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `S_L` | 0x360 | `J` | grass | MB_JUMP_SOUTH |
| `S` | 0x361 | `J` | grass | MB_JUMP_SOUTH |
| `S_R` | 0x362 | `J` | grass | MB_JUMP_SOUTH |
| `W` | 0x363 | `<` | grass | MB_JUMP_WEST |
| `E` | 0x364 | `>` | grass | MB_JUMP_EAST |

## Pillars

### The Pillars of Herakles

`pillars`, 6 wide by 6 tall. The two Pillars, 2 x 6 each, on borrowed grass: `W00` to `W15` (column then row) carries NE PLUS carved and gilded on its shaft, `E00` to `E15` ULTRA. Their top two rows (the capital and the shaft's top) are drawn over the player; the rest is impassable. The set piece (LABORS 10, step 3): each headland starts with a fallen column, `fallen00` to `fallen31` (4 x 2, lying west-east, the capital at its east end; impassable), beside an empty `socket_L` `socket_R` (2 x 1, the plinth's cut). When the Girdle pushes it upright, swap the fallen cells to grass and the socket and the 2 x 5 above it to the standing pillar (the socket becomes the pillar's base row, `W05` `W15`). The labels below name each swap.

```
370 371 372 373 374 375    TTTTTT
378 379 37A 37B 37C 37D    TTTTXX
380 381 382 383 384 385    XXXXXX
388 389 38A 38B 38C 38D    XXXXXX
390 391 392 393 394 395    XXXXXX
398 399 39A 39B 39C 39D    XXXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `W00` | 0x370 | `T` | grass | — |
| `W10` | 0x371 | `T` | grass | — |
| `W01` | 0x378 | `T` | grass | — |
| `W11` | 0x379 | `T` | grass | — |
| `W02` | 0x380 | `X` | grass | — |
| `W12` | 0x381 | `X` | grass | — |
| `W03` | 0x388 | `X` | grass | — |
| `W13` | 0x389 | `X` | grass | — |
| `W04` | 0x390 | `X` | grass | — |
| `W14` | 0x391 | `X` | grass | — |
| `W05` | 0x398 | `X` | grass | — |
| `W15` | 0x399 | `X` | grass | — |
| `E00` | 0x372 | `T` | grass | — |
| `E10` | 0x373 | `T` | grass | — |
| `E01` | 0x37A | `T` | grass | — |
| `E11` | 0x37B | `T` | grass | — |
| `E02` | 0x382 | `X` | grass | — |
| `E12` | 0x383 | `X` | grass | — |
| `E03` | 0x38A | `X` | grass | — |
| `E13` | 0x38B | `X` | grass | — |
| `E04` | 0x392 | `X` | grass | — |
| `E14` | 0x393 | `X` | grass | — |
| `E05` | 0x39A | `X` | grass | — |
| `E15` | 0x39B | `X` | grass | — |
| `socket_L` | 0x39C | `X` | grass | — |
| `socket_R` | 0x39D | `X` | grass | — |
| `fallen00` | 0x37C | `X` | grass | — |
| `fallen01` | 0x384 | `X` | grass | — |
| `fallen10` | 0x37D | `X` | grass | — |
| `fallen11` | 0x385 | `X` | grass | — |
| `fallen20` | 0x38C | `X` | grass | — |
| `fallen21` | 0x394 | `X` | grass | — |
| `fallen30` | 0x38D | `X` | grass | — |
| `fallen31` | 0x395 | `X` | grass | — |

### The glow between the Pillars, the fog bank beyond

`strait`, 6 wide by 1 tall. Over borrowed sea, surfable. `glow` and `glow_b`: the sea between the Pillars once both stand, lit from below, pulsing gold (`glow`); swap them in across the strait in the set piece. The fog bank west of the strait: `fog_E` its eastern edge (fog to the west), `fog` its body, and `fog_shape` `fog_shape_b` a dark shape on the horizon in the fog, a seed for Atlantis (POSTGAME 3). Aeolus's Bag parts the fog (the Oikoumene's waters of the Strait).

```
3A0 3A1 3A2 3A3 3A4 3A5    WWWWWW
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `glow` | 0x3A0 | `W` | sea | MB_OCEAN_WATER |
| `glow_b` | 0x3A1 | `W` | sea | MB_OCEAN_WATER |
| `fog_E` | 0x3A2 | `W` | sea | MB_OCEAN_WATER |
| `fog` | 0x3A3 | `W` | sea | MB_OCEAN_WATER |
| `fog_shape` | 0x3A4 | `W` | sea | MB_OCEAN_WATER |
| `fog_shape_b` | 0x3A5 | `W` | sea | MB_OCEAN_WATER |

## Places

### Where Helios's cup moors

`dock`, 5 wide by 3 tall. The cup's landing: a marble quay whose face drops into the sea (`quay_L` `quay` `quay_R`, the quay's south edge over borrowed sea; walk on the paving above them, which is aethos limestone path), `steps` going down into the water, a gilded `bollard` to moor to (impassable), and a sun-disc set in the paving (`sundisc`, walkable; `sundisc_b` impassable as a plinth). The cup itself, `cup_TL` to `cup_BR` (3 x 2 on borrowed sea): a great golden bowl the size of a house rocking in the shallows, full of light. It is there at sunset only: put it in with a script (the labels below) and take it out after. For the Western Cape (pair the cape's map with this set) and Erytheia's landing.

```
3B0 3B1 3B2 3B3 3B4    XXX.X
3B8 3B9 3BA 3BB 3BC    WWW..
3C0 3C1 3C2 3C3 3C4    WWWXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `quay_L` | 0x3B0 | `X` | sea | — |
| `quay` | 0x3B1 | `X` | sea | — |
| `quay_R` | 0x3B2 | `X` | sea | — |
| `steps` | 0x3B3 | `.` | sea | — |
| `bollard` | 0x3B4 | `X` | path | — |
| `cup_TL` | 0x3B8 | `W` | sea | MB_OCEAN_WATER |
| `cup_T` | 0x3B9 | `W` | sea | MB_OCEAN_WATER |
| `cup_TR` | 0x3BA | `W` | sea | MB_OCEAN_WATER |
| `cup_BL` | 0x3C0 | `W` | sea | MB_OCEAN_WATER |
| `cup_B` | 0x3C1 | `W` | sea | MB_OCEAN_WATER |
| `cup_BR` | 0x3C2 | `W` | sea | MB_OCEAN_WATER |
| `sundisc` | 0x3BB | `.` | path | — |
| `sundisc_b` | 0x3BC | `.` | path | — |

### Eurytion's hut

`hut`, 3 wide by 3 tall. The herdsman's hut on Erytheia, 3 x 3 on borrowed grass: walls of red field stone, a steep thatched roof gone gold in the sunset, a smoke-hole, a crooked door (`door`, `MB_NON_ANIMATED_DOOR`). The roof's top row is drawn over the player. For any herders' or fishers' huts in the far west.

```
3B5 3B6 3B7    TTT
3BD 3BE 3BF    XXX
3C5 3C6 3C7    XDX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `c00` | 0x3B5 | `T` | grass | — |
| `c10` | 0x3B6 | `T` | grass | — |
| `c20` | 0x3B7 | `T` | grass | — |
| `c01` | 0x3BD | `X` | grass | — |
| `c11` | 0x3BE | `X` | grass | — |
| `c21` | 0x3BF | `X` | grass | — |
| `c02` | 0x3C5 | `X` | grass | — |
| `c12` | 0x3C6 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `c22` | 0x3C7 | `X` | grass | — |
| `door` | 0x3C6 | `D` | grass | MB_NON_ANIMATED_DOOR |

### The Ocean Stream: rocks of light, the edge of the world

`stream`, 6 wide by 1 tall. For the Ocean Stream (LABORS 10): the cup sails west round the edge of the world at night. `light_rock` and `light_rocks`: floating rocks of light, the obstacles you steer round, glowing (`glow`; borrowed sea). `rim_W`: the world's western edge, the sea spilling over a lip of foam into the void (sea to the east); `rim_E` the same with the void to the east. `void` and `void_b`: the starry dark beyond, impassable. Use the void for the map's border, too.

```
3C8 3C9 3CA 3CB 3CC 3CD    XXXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `light_rock` | 0x3C8 | `X` | sea | — |
| `light_rocks` | 0x3C9 | `X` | sea | — |
| `rim_W` | 0x3CA | `X` | sea | — |
| `rim_E` | 0x3CB | `X` | sea | — |
| `void` | 0x3CC | `X` | drawn | — |
| `void_b` | 0x3CD | `X` | drawn | — |
