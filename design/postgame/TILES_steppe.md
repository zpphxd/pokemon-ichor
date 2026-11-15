# steppe tileset catalog

`gTileset_Steppe` is the steppe: Thrace, the Thermodon and Scythia.  Pair it with the `aethos` primary, which supplies the open grass, the limestone path, sand, the sea, olives and cypresses. It is one of the steppe family (`steppe`, `steppe_town`, `steppe_camp`).

**This file is generated.** `tools/ichor/art/farlands_build.py steppe` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/farlands_steppe.py` (with `farlands_ground.py` and `farlands_kits.py`); the palette groups are in that file's `GROUPS`, the borrowed ground in `farlands_lib.py`.

| Image | Shows |
|---|---|
| [`img/farlands_steppe_pieces.png`](img/farlands_steppe_pieces.png) | Every structure on its ground (`*` marks the Oikoumene's pieces) |
| [`img/farlands_steppe_sheet.png`](img/farlands_steppe_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row, with the walk codes beside them. Each section starts on a fixed row of the sheet (ground at 0x200, water at 0x288, mounds at 0x328, land at 0x378, heights at 0x390). Structures are placed first-fit in build order, so appending one never moves another. Place pieces by key and name, never by raw id: `tools/ichor/maps/farlands_tiles.py` holds every far-lands catalog as a Python dict (`mid('steppe', key, piece)`, and `soft('steppe', key, region, x, y)` for soft ground); `build/steppe/catalog.json` is the same as JSON.

**The Oikoumene's pieces** (drawn for world-oikoumene's lands, OIKOUMENE.md; `oikoumene_pieces('steppe')` lists them): `feather`, `reed_marsh`, `mudflat`, `kurgan`, `kurgan_large`, `idols`, `waystone`, `heights`, `fossils`. The rest serve LABORS's maps first; both sessions may use anything here.

**Walk codes:**

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `T` | Passable, drawn over the player, who walks behind it. |
| `G` | Tall grass: `MB_TALL_GRASS`, wild encounters. Passable. |
| `L` | Long grass or reeds: `MB_LONG_GRASS`, wild encounters. Passable. |
| `D` | Door: `MB_NON_ANIMATED_DOOR`. Put the warp here. |
| `P` | Fresh water: `MB_POND_WATER`, surfable. |
| `H` | Shallow water: `MB_SHALLOW_WATER`, walkable, splashes. |
| `M` | Mud or a puddle: `MB_PUDDLE`, walkable. |

**Soft ground.** Grasses, roads, earth, mud and water come as 47 soft-edged shapes, keyed by a cell's neighbors (`farlands_lib.blob_key`, or `shape()` in `farlands_tiles.py`): `1|` then N NE E SE S SW W NW, 1 where the neighbor is in the region, a diagonal counting only when both its sides are. `1|11111111` is the full interior. Draw regions as irregular masks that follow the land (MAP_DESIGN 1: never plain rectangles); the shapes round every outer corner and wobble every edge.

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea*, *shallow* or *fall* draw no ground of their own: after Porytiles compiles, the build points their bottom-layer tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated sea (`0x170`), shallows (`0x0D1`) or waterfall (`0x0B3`). They meet aethos ground exactly and cost no tiles. A borrowed cell's art is in one layer: the middle (`COVERED`, under the player) or the top (`SPLIT`, over the player). Cells marked *drawn* paint their own ground, aethos's grass pixel for pixel where it shows.

**Seams.** MAP_DESIGN 5: the 6 rows (or 8 columns) nearest a connection to a map on a different secondary use only aethos metatiles. Everything here fades onto aethos ground, so a map can always end its soft regions before the strip: grass and earth shapes onto aethos grass, water onto aethos sea, roads through `road_join` onto aethos's limestone path patch (`1D0`-`1E2`).

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player), `COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color groups, one per secondary palette (6-12), passed to Porytiles as packing hints.

| Group | Use | Colors |
|---|---|---|
| gold |  | `sg0` `sg1` `sg2` `sg3` `sg4` `t1` `w1` `w0` `dt1` `dt2` `dt3` `pp` `th2` `cf` `gd` |
| earth |  | `g1` `g2` `g3` `gd` `l0` `l1` `rd0` `rd3` `p1` `p2` `p3` `md0` `md1` `md2` `sg2` |
| river |  | `b2` `b3` `b4` `w0` `g1` `g2` `g3` `gd` `md0` `md1` `md2` `t0` `t1` `t3` `rb1` |
| stone |  | `g1` `g2` `g3` `gd` `sn0` `sn1` `sn2` `sn3` `w1` `w0` `lc` `ink` `t0` `sg2` `fr2` |
| mound |  | `g1` `g2` `g3` `gd` `t0` `t1` `sg1` `sg2` `sg3` `l0` `l1` `sn1` `sn2` `sn3` `md0` |
| heights |  | `hr0` `hr1` `hr2` `hr3` `hr4` `au1` `au2` `bn1` `bn2` `ink` `g1` `g2` `gd` `tb1` `tb2` |
| grove |  | `wl1` `wl2` `wl3` `wl4` `k1` `k2` `k3` `t0` `g1` `gd` `tb1` `tb2` `tb3` `b3` `sg3` |

**Tile budget.** 462 of 504 tiles (448 metatiles). The door animations copy their frames into tiles 504-511, so the build fails past 504. Static tiles within two pixels of one another are merged.

**Scripted swaps.** The build writes the ids scripts swap to the `gTileset_Steppe` block at the end of `include/constants/metatile_labels.h`: `METATILE_Steppe_DigMound`, `METATILE_Steppe_DigMound_Dug`, `METATILE_Steppe_Kurgan_Door_Shut`, `METATILE_Steppe_Kurgan_Door`, `METATILE_Steppe_Kurgan_Crown`, `METATILE_Steppe_Kurgan_Crown_Idol`.

## Ground

### Long golden steppe grass (encounters)

`steppe_grass`, 8 wide by 6 tall. Thrace's long grass: knee-high golden tufts with dark green feet, all 47 soft-edge shapes over borrowed aethos grass (`farlands_lib.blob_key` gives a cell's key from a region mask). Every cell is `MB_TALL_GRASS`. Blade tips lean out over the meadow along the top edge. Use it for the forced bands and the optional fields of the Bistonian Plain and the Thermodon Road.

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

### Silver feather-grass (encounters) *(Oikoumene)*

`feather`, 2 wide by 1 tall. The Pontic steppe's feather-grass (Stipa): straw tufts bleached silver, long awns catching the wind. Two full-interior cells, `MB_TALL_GRASS`, to use in place of `steppe_grass` `1|11111111` anywhere inside a grass region (its soft edges stay golden). For the Oikoumene's Scythia, fill whole fields with them; on a Thracian map, set a streak of them for the wind.

```
230 231    GG
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `feather` | 0x230 | `G` | grass | MB_TALL_GRASS |
| `feather_b` | 0x231 | `G` | grass | MB_TALL_GRASS |

### Dirt road (and worn track)

`road`, 8 wide by 6 tall. Thrace's roads are beaten earth: hoof-prints, pebbles, a darker lip where the grass gives way. 47 soft-edge shapes over borrowed aethos grass; a region one cell wide reads as a worn track, two or three wide as a cart road. Lay roads as regions that bend diagonally in steps, and the soft corners make the curve. Walkable. Where a road crosses into a seam strip it must become aethos's limestone path: use `road_join`.

Shape keys and their ids:

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

### The road meets aethos's limestone path

`road_join`, 6 wide by 2 tall. Where the dirt road becomes aethos's limestone path, so a road can run into a seam strip (MAP_DESIGN 5) or into a town's paving. Named `<side>_<cell>`, side being where the aethos path lies: `S_L` `S_C` `S_R` are the left, middle and right cells of a north-south road with the path to the south (below them put aethos `1D8` `1D9` `1DA`); `N_*` the same with the path to the north; `E_T` `E_C` `E_B` the top, middle and bottom cells of an east-west road with the path to the east (beside them put aethos `1D1` (top) `1D9` `1E1` (bottom)); `W_*` the same to the west. A two-wide road uses only `_L` `_R` (or `_T` `_B`). Walkable.

```
268 269 26A 26B 26C 26D    ......
270 271 272 273 274 275    ......
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `S_L` | 0x268 | `.` | drawn | — |
| `S_C` | 0x269 | `.` | drawn | — |
| `S_R` | 0x26A | `.` | drawn | — |
| `N_L` | 0x26B | `.` | drawn | — |
| `N_C` | 0x26C | `.` | drawn | — |
| `N_R` | 0x26D | `.` | drawn | — |
| `E_T` | 0x270 | `.` | drawn | — |
| `E_C` | 0x271 | `.` | drawn | — |
| `E_B` | 0x272 | `.` | drawn | — |
| `W_T` | 0x273 | `.` | drawn | — |
| `W_C` | 0x274 | `.` | drawn | — |
| `W_B` | 0x275 | `.` | drawn | — |

### Dry turf, tussocks and steppe flowers

`decor`, 6 wide by 1 tall. On borrowed aethos grass, walkable, to scatter through the meadow so it isn't one flat green: `turf`, a patch of grazed dry turf (the steppe's short grass); `tussock` and `tussocks`, clumps of last year's straw; `poppies` and `salvia` (violet sage), the steppe's flowers in early summer; `plumes`, a few feather-grass awns standing out of the meadow. None has encounters.

```
232 233 234 235 236 237    ......
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `turf` | 0x232 | `.` | grass | — |
| `tussock` | 0x233 | `.` | grass | — |
| `tussocks` | 0x234 | `.` | grass | — |
| `poppies` | 0x235 | `.` | grass | — |
| `salvia` | 0x236 | `.` | grass | — |
| `plumes` | 0x237 | `.` | grass | — |

## Water

### Rivers and lakes, with soft banks

`river`, 8 wide by 6 tall. Fresh water (`MB_POND_WATER`, surfable; fish here) over borrowed aethos sea, so it moves. The 47 soft-edge shapes are of the water: an edge cell draws the grassy bank over the land side, aethos grass pixel for pixel, with a muddy lip, a pale fringe of shallows and a ripple line, and now and then a few reeds. The Thermodon, the Nestos, the Borysthenes, Lake Maeotis. One cell wide is a brook.

Shape keys and their ids:

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

### Reed marsh (encounters) *(Oikoumene)*

`reed_marsh`, 8 wide by 6 tall. A bed of reeds and cattails taller than you, 47 soft-edge shapes over borrowed grass. `MB_LONG_GRASS`: wild encounters, and the reeds part round you. For Lake Maeotis's marsh and the Thermodon's backwaters.

Shape keys and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x2B8 |
| `1|00000010` | 0x2B9 |
| `1|00001000` | 0x2BA |
| `1|00001010` | 0x2BB |
| `1|00001110` | 0x2BC |
| `1|00100000` | 0x2BD |
| `1|00100010` | 0x2BE |
| `1|00101000` | 0x2BF |
| `1|00101010` | 0x2C0 |
| `1|00101110` | 0x2C1 |
| `1|00111000` | 0x2C2 |
| `1|00111010` | 0x2C3 |
| `1|00111110` | 0x2C4 |
| `1|10000000` | 0x2C5 |
| `1|10000010` | 0x2C6 |
| `1|10000011` | 0x2C7 |
| `1|10001000` | 0x2C8 |
| `1|10001010` | 0x2C9 |
| `1|10001011` | 0x2CA |
| `1|10001110` | 0x2CB |
| `1|10001111` | 0x2CC |
| `1|10100000` | 0x2CD |
| `1|10100010` | 0x2CE |
| `1|10100011` | 0x2CF |
| `1|10101000` | 0x2D0 |
| `1|10101010` | 0x2D1 |
| `1|10101011` | 0x2D2 |
| `1|10101110` | 0x2D3 |
| `1|10101111` | 0x2D4 |
| `1|10111000` | 0x2D5 |
| `1|10111010` | 0x2D6 |
| `1|10111011` | 0x2D7 |
| `1|10111110` | 0x2D8 |
| `1|10111111` | 0x2D9 |
| `1|11100000` | 0x2DA |
| `1|11100010` | 0x2DB |
| `1|11100011` | 0x2DC |
| `1|11101000` | 0x2DD |
| `1|11101010` | 0x2DE |
| `1|11101011` | 0x2DF |
| `1|11101110` | 0x2E0 |
| `1|11101111` | 0x2E1 |
| `1|11111000` | 0x2E2 |
| `1|11111010` | 0x2E3 |
| `1|11111011` | 0x2E4 |
| `1|11111110` | 0x2E5 |
| `1|11111111` | 0x2E6 |

### Mudflats *(Oikoumene)*

`mudflat`, 8 wide by 6 tall. Lake Maeotis's shore: cracked grey-brown mud with standing water in the hoof-holes, 47 soft-edge shapes over borrowed grass, walkable (`MB_PUDDLE`, so feet splash). Lay it between the meadow and the water's edge (`river` banks are muddy too).

Shape keys and their ids:

| Shape key | Id |
|---|---|
| `1|00000000` | 0x2E8 |
| `1|00000010` | 0x2E9 |
| `1|00001000` | 0x2EA |
| `1|00001010` | 0x2EB |
| `1|00001110` | 0x2EC |
| `1|00100000` | 0x2ED |
| `1|00100010` | 0x2EE |
| `1|00101000` | 0x2EF |
| `1|00101010` | 0x2F0 |
| `1|00101110` | 0x2F1 |
| `1|00111000` | 0x2F2 |
| `1|00111010` | 0x2F3 |
| `1|00111110` | 0x2F4 |
| `1|10000000` | 0x2F5 |
| `1|10000010` | 0x2F6 |
| `1|10000011` | 0x2F7 |
| `1|10001000` | 0x2F8 |
| `1|10001010` | 0x2F9 |
| `1|10001011` | 0x2FA |
| `1|10001110` | 0x2FB |
| `1|10001111` | 0x2FC |
| `1|10100000` | 0x2FD |
| `1|10100010` | 0x2FE |
| `1|10100011` | 0x2FF |
| `1|10101000` | 0x300 |
| `1|10101010` | 0x301 |
| `1|10101011` | 0x302 |
| `1|10101110` | 0x303 |
| `1|10101111` | 0x304 |
| `1|10111000` | 0x305 |
| `1|10111010` | 0x306 |
| `1|10111011` | 0x307 |
| `1|10111110` | 0x308 |
| `1|10111111` | 0x309 |
| `1|11100000` | 0x30A |
| `1|11100010` | 0x30B |
| `1|11100011` | 0x30C |
| `1|11101000` | 0x30D |
| `1|11101010` | 0x30E |
| `1|11101011` | 0x30F |
| `1|11101110` | 0x310 |
| `1|11101111` | 0x311 |
| `1|11111000` | 0x312 |
| `1|11111010` | 0x313 |
| `1|11111011` | 0x314 |
| `1|11111110` | 0x315 |
| `1|11111111` | 0x316 |

### Reeds in the water, fords and stepping stones

`reeds_ford`, 6 wide by 1 tall. `reeds_water` and `reeds_water_b`: a clump of reeds standing in the river (borrowed sea; impassable, surf round it). `reeds_bank`: reeds on dry ground (borrowed grass; impassable). `ford`: a gravel bar under a skin of water, walkable (`MB_SHALLOW_WATER`): lay a line of them across a river, inside the water region, to make a ford; `ford_stones` is the same with stepping stones. `stones`: three flat stones in the grass by a ford (walkable).

```
318 319 31A 31B 31C 31D    XX.HH.
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `reeds_water` | 0x318 | `X` | sea | — |
| `reeds_water_b` | 0x319 | `X` | sea | — |
| `reeds_bank` | 0x31A | `.` | grass | — |
| `ford` | 0x31B | `H` | drawn | MB_SHALLOW_WATER |
| `ford_stones` | 0x31C | `H` | drawn | MB_SHALLOW_WATER |
| `stones` | 0x31D | `.` | grass | — |

## Mounds

### Kurgans: a small mound, a dig-spot mound *(Oikoumene)*

`kurgan`, 4 wide by 2 tall. Burial mounds of the horse-lords, grassy domes ringed with half-buried kerb stones. `small` is 2 x 2 (its cells `small_TL` `small_TR` / `small_BL` `small_BR`), impassable. `low` and `low_b` are low barrows one cell across, for a line of them along a ridge. `dig` is a low mound with fresh cracks in its turf: a dig spot (`EventScript_IchorDigSpot` on it); swap it for `dug`, the opened pit, once dug. All drawn whole (grass round them is aethos's own pixels).

```
328 329 32A 32B    XXXX
330 331 332 333    XXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `small_TL` | 0x328 | `X` | drawn | — |
| `small_TR` | 0x329 | `X` | drawn | — |
| `small_BL` | 0x330 | `X` | drawn | — |
| `small_BR` | 0x331 | `X` | drawn | — |
| `dig` | 0x32A | `X` | drawn | — |
| `dug` | 0x32B | `X` | drawn | — |
| `low` | 0x332 | `X` | drawn | — |
| `low_b` | 0x333 | `X` | drawn | — |

### The great kurgan, with a grave door and a summit idol *(Oikoumene)*

`kurgan_large`, 4 wide by 4 tall. A royal barrow, 4 x 3 (`c00` to `c32`, column then row), impassable: a broad dome lit from the west, dry tufts on its flanks, kerb stones round its foot. Two swaps: `door` replaces `c12` (the bottom row's second cell) with the grave entrance, a passage lined with upright slabs (`MB_NON_ANIMATED_DOOR`: warp to the barrow's chamber; the Oikoumene's barrow-keeper, Spiritomb's lair); `summit_idol` replaces `c10` (the top row's second cell) with a stone baba standing on the crown. The extra row's last two cells are fillers.

```
32C 32D 32E 32F    XXXX
334 335 336 337    XXXX
33C 33D 33E 33F    XXXX
344 345 346 347    XDXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `c00` | 0x32C | `X` | drawn | — |
| `c10` | 0x32D | `X` | drawn | — |
| `c20` | 0x32E | `X` | drawn | — |
| `c30` | 0x32F | `X` | drawn | — |
| `c01` | 0x334 | `X` | drawn | — |
| `c11` | 0x335 | `X` | drawn | — |
| `c21` | 0x336 | `X` | drawn | — |
| `c31` | 0x337 | `X` | drawn | — |
| `c02` | 0x33C | `X` | drawn | — |
| `c12` | 0x33D | `X` | drawn | — |
| `c22` | 0x33E | `X` | drawn | — |
| `c32` | 0x33F | `X` | drawn | — |
| `door` | 0x345 | `D` | drawn | MB_NON_ANIMATED_DOOR |
| `summit_idol` | 0x346 | `X` | drawn | — |

### Stone babas, race markers, a cairn *(Oikoumene)*

`idols`, 5 wide by 2 tall. Stone idols (`baba`) on borrowed grass, each 1 x 2: the top cell (`*_top`) is drawn over the player, the bottom one impassable (put a bg event here: they stand on kurgans and at fords, and travellers leave them a cup of milk). `horn`: a man holding a drinking horn at his belly; `woman`: hands folded, a tall headdress; `worn`: weathered faceless and leaning, crusted with lichen. `marker` (with `marker_top`): a race marker, a stone post banded in red ochre, for the Wagon Camp's races and the steppe's boundary lines. `cairn`: a heap of stones with a red rag tied to a stick, the turning post of a race course (`cairn_top` is plain grass to go above it).

```
348 349 34A 34B 34C    TTTT.
350 351 352 353 354    XXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `horn_top` | 0x348 | `T` | grass | — |
| `horn` | 0x350 | `X` | grass | — |
| `woman_top` | 0x349 | `T` | grass | — |
| `woman` | 0x351 | `X` | grass | — |
| `worn_top` | 0x34A | `T` | grass | — |
| `worn` | 0x352 | `X` | grass | — |
| `marker_top` | 0x34B | `T` | grass | — |
| `marker` | 0x353 | `X` | grass | — |
| `cairn` | 0x354 | `X` | grass | — |
| `cairn_top` | 0x34C | `.` | grass | — |

### The great idol: a route's waystone *(Oikoumene)*

`waystone`, 2 wide by 3 tall. A great stone idol twice a man's height, four-square, with a pointed cap, a drinking horn and a short sword at its belt, on a plinth cut with the roads it watches; red ribbons and a heap of offering-stones at its foot. 2 x 3 on borrowed grass: the top row is drawn over the player, the rest impassable. Put the route sign's bg event on its plinth (`c01` or `c11`, bottom row is `c02` `c12`).

```
34D 34E    TT
355 356    XX
35D 35E    XX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `c00` | 0x34D | `T` | grass | — |
| `c10` | 0x34E | `T` | grass | — |
| `c01` | 0x355 | `X` | grass | — |
| `c11` | 0x356 | `X` | grass | — |
| `c02` | 0x35D | `X` | grass | — |
| `c12` | 0x35E | `X` | grass | — |

## Land

### Willow, poplar and a lone oak

`trees`, 5 wide by 2 tall. On borrowed grass; each tree's top row is drawn over the player, its bottom row impassable. `willow` (2 x 2): a white willow on a river bank, its fronds hanging to the grass. `poplar` (1 x 2, with `poplar_top`): a black poplar, tall and narrow; plant them in lines along a river. `oak` (2 x 2): a lone wind-bent oak, the only shade for a day's ride; set a rest point under it.

```
378 379 37A 37B 37C    TTTTT
380 381 382 383 384    XXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `willow_TL` | 0x378 | `T` | grass | — |
| `willow_TR` | 0x379 | `T` | grass | — |
| `willow_BL` | 0x380 | `X` | grass | — |
| `willow_BR` | 0x381 | `X` | grass | — |
| `poplar_top` | 0x37A | `T` | grass | — |
| `poplar` | 0x382 | `X` | grass | — |
| `oak_TL` | 0x37B | `T` | grass | — |
| `oak_TR` | 0x37C | `T` | grass | — |
| `oak_BL` | 0x383 | `X` | grass | — |
| `oak_BR` | 0x384 | `X` | grass | — |

## Heights

### The Arimaspian heights: rock faces *(Oikoumene)*

`heights`, 4 wide by 6 tall. How to build a crag: a plateau of high ground, its cells plain aethos grass. Its south edge is three rows: `lip` (the crest, grass above the rock's brow), `face` (bare rock; stack two for a taller cliff) and `foot` (the face's base, rubble and shadow on the ground, walkable). `_L` and `_R` end a run where the plateau's west and east edges turn north; `face_b` breaks up a long run. The west and east edges are `side_W` and `side_E` (a strip of rock falling away), the north edge `back` (a thin rim) with its corners `back_NW` and `back_NE`; `in_NW` and `in_NE` are inner corners where a south face meets a side running north. Everything but `foot` is impassable, on borrowed aethos grass. Use aethos's ledges (`087` and kin) for one-way drops. Extra faces: `face_gold` and `face_gold_b`, the face threaded with veins of gold the one-eyed Arimaspians dig (Herodotus 3.116); `mine`, a timber-framed mine head; `cave`, a natural cave mouth. Both are `MB_NON_ANIMATED_DOOR` (put the warp there).

```
390 391 392 393    XXXX
398 399 39A 39B    XXXX
3A0 3A1 3A2 3A3    XXXX
3A8 3A9 3AA 3AB    XXXX
3B0 3B1 3B2 3B3    ....
3B8 3B9 3BA 3BB    XXDD
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `back_NW` | 0x390 | `X` | grass | — |
| `back` | 0x391 | `X` | grass | — |
| `back_NE` | 0x393 | `X` | grass | — |
| `side_W` | 0x398 | `X` | grass | — |
| `side_E` | 0x39B | `X` | grass | — |
| `in_NW` | 0x399 | `X` | grass | — |
| `in_NE` | 0x39A | `X` | grass | — |
| `lip_L` | 0x3A0 | `X` | grass | — |
| `lip` | 0x3A1 | `X` | grass | — |
| `lip_R` | 0x3A3 | `X` | grass | — |
| `face_L` | 0x3A8 | `X` | grass | — |
| `face` | 0x3A9 | `X` | grass | — |
| `face_b` | 0x3AA | `X` | grass | — |
| `face_R` | 0x3AB | `X` | grass | — |
| `foot_L` | 0x3B0 | `.` | grass | — |
| `foot` | 0x3B1 | `.` | grass | — |
| `foot_R` | 0x3B3 | `.` | grass | — |
| `face_gold` | 0x3B8 | `X` | grass | — |
| `face_gold_b` | 0x3B9 | `X` | grass | — |
| `mine` | 0x3BA | `D` | grass | MB_NON_ANIMATED_DOOR |
| `cave` | 0x3BB | `D` | grass | MB_NON_ANIMATED_DOOR |

### Fossil beds of mismatched bones *(Oikoumene)*

`fossils`, 4 wide by 1 tall. On borrowed grass, impassable: shelves of pale rock weathering out of the turf, where the 'gold-guardians' lie (Adrienne Mayor: griffin tales from fossils). `bed`, bare rock; `skull`, a beaked skull too big for any bird; `jaw`, a toothed jaw beside a wing-bone; `ribs`, ribs and a clawed foot that don't belong together. Dig spots: the Oikoumene's mismatched fossils (Dracozolt and kin) come out of these.

```
394 395 396 397    XXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `bed` | 0x394 | `X` | grass | — |
| `skull` | 0x395 | `X` | grass | — |
| `jaw` | 0x396 | `X` | grass | — |
| `ribs` | 0x397 | `X` | grass | — |
