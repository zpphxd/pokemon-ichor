# steppe_camp tileset catalog

`gTileset_SteppeCamp` is the horse-peoples' camps: Themiskyra, Diomedes's yard, the Wagon Camp.  Pair it with the `aethos` primary, which supplies the open grass, the limestone path, sand, the sea, olives and cypresses. It is one of the steppe family (`steppe`, `steppe_town`, `steppe_camp`).

**This file is generated.** `tools/ichor/art/farlands_build.py steppe_camp` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/farlands_steppe_camp.py` (with `farlands_ground.py` and `farlands_kits.py`); the palette groups are in that file's `GROUPS`, the borrowed ground in `farlands_lib.py`.

| Image | Shows |
|---|---|
| [`img/farlands_steppe_camp_pieces.png`](img/farlands_steppe_camp_pieces.png) | Every structure on its ground (`*` marks the Oikoumene's pieces) |
| [`img/farlands_steppe_camp_sheet.png`](img/farlands_steppe_camp_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

**Why a sister set.** The steppe's land fills `steppe`'s 504 tiles, so the camps built on it are their own set (and the Greek colonies another, `steppe_town`). Themiskyra borders the Thermodon Road, Diomedes's yard the Bistonian Plain, the Wagon Camp the Steppe Road: each meets the open steppe across a seam strip of aethos ground (MAP_DESIGN 5). The road, its joins and the meadow's flowers are the steppe's own, redrawn here.

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row, with the walk codes beside them. Each section starts on a fixed row of the sheet (ground at 0x200, walls at 0x250, halls at 0x280, tents at 0x2C0, yard at 0x300). Structures are placed first-fit in build order, so appending one never moves another. Place pieces by key and name, never by raw id: `tools/ichor/maps/farlands_tiles.py` holds every far-lands catalog as a Python dict (`mid('steppe_camp', key, piece)`, and `soft('steppe_camp', key, region, x, y)` for soft ground); `build/steppe_camp/catalog.json` is the same as JSON.

**The Oikoumene's pieces** (drawn for world-oikoumene's lands, OIKOUMENE.md; `oikoumene_pieces('steppe_camp')` lists them): `wagons`. The rest serve LABORS's maps first; both sessions may use anything here.

**Walk codes:**

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `T` | Passable, drawn over the player, who walks behind it. |
| `D` | Door: `MB_NON_ANIMATED_DOOR`. Put the warp here. |

**Soft ground.** Grasses, roads, earth, mud and water come as 47 soft-edged shapes, keyed by a cell's neighbors (`farlands_lib.blob_key`, or `shape()` in `farlands_tiles.py`): `1|` then N NE E SE S SW W NW, 1 where the neighbor is in the region, a diagonal counting only when both its sides are. `1|11111111` is the full interior. Draw regions as irregular masks that follow the land (MAP_DESIGN 1: never plain rectangles); the shapes round every outer corner and wobble every edge.

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea*, *shallow* or *fall* draw no ground of their own: after Porytiles compiles, the build points their bottom-layer tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated sea (`0x170`), shallows (`0x0D1`) or waterfall (`0x0B3`). They meet aethos ground exactly and cost no tiles. A borrowed cell's art is in one layer: the middle (`COVERED`, under the player) or the top (`SPLIT`, over the player). Cells marked *drawn* paint their own ground, aethos's grass pixel for pixel where it shows.

**Seams.** MAP_DESIGN 5: the 6 rows (or 8 columns) nearest a connection to a map on a different secondary use only aethos metatiles. Everything here fades onto aethos ground, so a map can always end its soft regions before the strip: grass and earth shapes onto aethos grass, water onto aethos sea, roads through `road_join` onto aethos's limestone path patch (`1D0`-`1E2`).

**Animations.** Porytiles animations, driven by `InitTilesetAnim_PorytilesManaged_SteppeCamp` (`include/porytiles_generated/tilesets/steppe_camp/generated_anim_code.h`): `fire`: . Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player), `COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color groups, one per secondary palette (6-12), passed to Porytiles as packing hints.

| Group | Use | Colors |
|---|---|---|
| earth |  | `g1` `g2` `g3` `gd` `l0` `l1` `rd0` `rd3` `p1` `p2` `p3` `md0` `md1` `md2` `sg2` |
| gold |  | `sg0` `sg1` `sg2` `sg3` `sg4` `t1` `w1` `w0` `dt1` `dt2` `dt3` `pp` `th2` `cf` `gd` |
| timber |  | `tb0` `tb1` `tb2` `tb3` `tb4` `sg1` `sg2` `sg3` `ink` `gd` `g1` `w0` `k2` `k3` `b3` |
| felt |  | `fr0` `fr1` `fr2` `fr3` `fc0` `fc1` `fc2` `fb` `ink` `gd` `g1` `sg3` `tb1` `w0` `bz3` |
| bronze |  | `bz0` `bz1` `bz2` `bz3` `vg1` `fi1` `fi2` `fi3` `as1` `sn1` `sn2` `ink` `gd` `g1` `w0` |
| stone |  | `sn0` `sn1` `sn2` `sn3` `w1` `w0` `g1` `g2` `g3` `gd` `md1` `lc` `ink` `b3` `tb1` |
| roof |  | `g1` `g2` `gd` `t1` `sg0` `sg1` `sg2` `sg3` `tb0` `tb1` `tb2` `tb3` `ink` `fr2` `w0` |

**Tile budget.** 444 of 496 tiles (296 metatiles). Its maps use wide doors, whose animation frames copy over tiles 496-511 (`DOOR_TILE_START_SIZE2`, `src/field_door.c`), so the build fails past 496. Static tiles within two pixels of one another are merged.

## Ground

### Dirt road (and worn track)

`road`, 8 wide by 6 tall. Thrace's roads are beaten earth: hoof-prints, pebbles, a darker lip where the grass gives way. 47 soft-edge shapes over borrowed aethos grass; a region one cell wide reads as a worn track, two or three wide as a cart road. Lay roads as regions that bend diagonally in steps, and the soft corners make the curve. Walkable. Where a road crosses into a seam strip it must become aethos's limestone path: use `road_join`.

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

### The road meets aethos's limestone path

`road_join`, 6 wide by 2 tall. Where the dirt road becomes aethos's limestone path, so a road can run into a seam strip (MAP_DESIGN 5) or into a town's paving. Named `<side>_<cell>`, side being where the aethos path lies: `S_L` `S_C` `S_R` are the left, middle and right cells of a north-south road with the path to the south (below them put aethos `1D8` `1D9` `1DA`); `N_*` the same with the path to the north; `E_T` `E_C` `E_B` the top, middle and bottom cells of an east-west road with the path to the east (beside them put aethos `1D1` (top) `1D9` `1E1` (bottom)); `W_*` the same to the west. A two-wide road uses only `_L` `_R` (or `_T` `_B`). Walkable.

```
230 231 232 233 234 235    ......
238 239 23A 23B 23C 23D    ......
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `S_L` | 0x230 | `.` | drawn | — |
| `S_C` | 0x231 | `.` | drawn | — |
| `S_R` | 0x232 | `.` | drawn | — |
| `N_L` | 0x233 | `.` | drawn | — |
| `N_C` | 0x234 | `.` | drawn | — |
| `N_R` | 0x235 | `.` | drawn | — |
| `E_T` | 0x238 | `.` | drawn | — |
| `E_C` | 0x239 | `.` | drawn | — |
| `E_B` | 0x23A | `.` | drawn | — |
| `W_T` | 0x23B | `.` | drawn | — |
| `W_C` | 0x23C | `.` | drawn | — |
| `W_B` | 0x23D | `.` | drawn | — |

### Dry turf, tussocks and steppe flowers

`decor`, 6 wide by 1 tall. On borrowed aethos grass, walkable, to scatter through the meadow so it isn't one flat green: `turf`, a patch of grazed dry turf (the steppe's short grass); `tussock` and `tussocks`, clumps of last year's straw; `poppies` and `salvia` (violet sage), the steppe's flowers in early summer; `plumes`, a few feather-grass awns standing out of the meadow. None has encounters.

```
240 241 242 243 244 245    ......
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `turf` | 0x240 | `.` | grass | — |
| `tussock` | 0x241 | `.` | grass | — |
| `tussocks` | 0x242 | `.` | grass | — |
| `poppies` | 0x243 | `.` | grass | — |
| `salvia` | 0x244 | `.` | grass | — |
| `plumes` | 0x245 | `.` | grass | — |

## Walls

### The palisade

`palisade`, 5 wide by 2 tall. Themiskyra's wall: sharpened stakes on a footing of field stone, on borrowed grass, impassable. A west-east run is two rows, `top` over `base` (the stakes' points, drawn over the player, over the stakes and the stone), with `top_L` / `base_L` and `top_R` / `base_R` ending it. A north-south run is `V` (the stakes seen end-on), ending in `V_B` on its footing. `tower_top` over `tower`: a square watch-post where runs meet. Diomedes's yard uses the same wall.

```
250 251 252 253 254    TTTXT
258 259 25A 25B 25C    XXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `top_L` | 0x250 | `T` | grass | — |
| `top` | 0x251 | `T` | grass | — |
| `top_R` | 0x252 | `T` | grass | — |
| `base_L` | 0x258 | `X` | grass | — |
| `base` | 0x259 | `X` | grass | — |
| `base_R` | 0x25A | `X` | grass | — |
| `V` | 0x253 | `X` | grass | — |
| `V_B` | 0x25B | `X` | grass | — |
| `tower_top` | 0x254 | `T` | grass | — |
| `tower` | 0x25C | `X` | grass | — |

### The gate of Themiskyra

`gate`, 4 wide by 3 tall. The camp's gate, 4 x 3 on borrowed grass: two timber gate-towers hung with pelta shields, a lintel beam carved with horses across the top, the two middle cells of the bottom rows open (walk through them). Join `palisade` runs to its sides at the bottom two rows. The towers' tops and the lintel are drawn over the player.

```
260 261 262 263    TTTT
268 269 26A 26B    XTTX
270 271 272 273    X..X
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `c00` | 0x260 | `T` | grass | — |
| `c10` | 0x261 | `T` | grass | — |
| `c20` | 0x262 | `T` | grass | — |
| `c30` | 0x263 | `T` | grass | — |
| `c01` | 0x268 | `X` | grass | — |
| `c11` | 0x269 | `T` | grass | — |
| `c21` | 0x26A | `T` | grass | — |
| `c31` | 0x26B | `X` | grass | — |
| `c02` | 0x270 | `X` | grass | — |
| `c12` | 0x271 | `.` | grass | — |
| `c22` | 0x272 | `.` | grass | — |
| `c32` | 0x273 | `X` | grass | — |

## Halls

### Hippolyta's hall

`hall`, 6 wide by 4 tall. The queen's hall, 6 x 4 on borrowed grass: a long timber hall under a high turf roof, its gable ends crowned with carved horse heads painted red, round bronze-rimmed shields hung along the wall, Ares's spear-standard by the door. The wide double door is `c22` and `c32` (`MB_NON_ANIMATED_DOOR`, two cells: a wide door, which is why this set stops at 496 tiles). The roof's top row is drawn over the player.

```
280 281 282 283 284 285    TTTTTT
288 289 28A 28B 28C 28D    XXXXXX
290 291 292 293 294 295    XXXXXX
298 299 29A 29B 29C 29D    XXDDXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `c00` | 0x280 | `T` | grass | — |
| `c10` | 0x281 | `T` | grass | — |
| `c20` | 0x282 | `T` | grass | — |
| `c30` | 0x283 | `T` | grass | — |
| `c40` | 0x284 | `T` | grass | — |
| `c50` | 0x285 | `T` | grass | — |
| `c01` | 0x288 | `X` | grass | — |
| `c11` | 0x289 | `X` | grass | — |
| `c21` | 0x28A | `X` | grass | — |
| `c31` | 0x28B | `X` | grass | — |
| `c41` | 0x28C | `X` | grass | — |
| `c51` | 0x28D | `X` | grass | — |
| `c02` | 0x290 | `X` | grass | — |
| `c12` | 0x291 | `X` | grass | — |
| `c22` | 0x292 | `X` | grass | — |
| `c32` | 0x293 | `X` | grass | — |
| `c42` | 0x294 | `X` | grass | — |
| `c52` | 0x295 | `X` | grass | — |
| `c03` | 0x298 | `X` | grass | — |
| `c13` | 0x299 | `X` | grass | — |
| `c23` | 0x29A | `D` | grass | MB_NON_ANIMATED_DOOR |
| `c33` | 0x29B | `D` | grass | MB_NON_ANIMATED_DOOR |
| `c43` | 0x29C | `X` | grass | — |
| `c53` | 0x29D | `X` | grass | — |

### Diomedes's stable

`stable`, 6 wide by 3 tall. The man-eating mares' stable (LABORS 8), 6 x 3 on borrowed grass: a long low barn of black timber under a sagging thatch, stall hatches barred shut along its front, horse skulls nailed over the wide double door (`c22` `c32`, `MB_NON_ANIMATED_DOOR`). The roof's top row is drawn over the player. For the Oikoumene, any steppe stable.

```
2A0 2A1 2A2 2A3 2A4 2A5    TTTTTT
2A8 2A9 2AA 2AB 2AC 2AD    XXXXXX
2B0 2B1 2B2 2B3 2B4 2B5    XXDDXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `c00` | 0x2A0 | `T` | grass | — |
| `c10` | 0x2A1 | `T` | grass | — |
| `c20` | 0x2A2 | `T` | grass | — |
| `c30` | 0x2A3 | `T` | grass | — |
| `c40` | 0x2A4 | `T` | grass | — |
| `c50` | 0x2A5 | `T` | grass | — |
| `c01` | 0x2A8 | `X` | grass | — |
| `c11` | 0x2A9 | `X` | grass | — |
| `c21` | 0x2AA | `X` | grass | — |
| `c31` | 0x2AB | `X` | grass | — |
| `c41` | 0x2AC | `X` | grass | — |
| `c51` | 0x2AD | `X` | grass | — |
| `c02` | 0x2B0 | `X` | grass | — |
| `c12` | 0x2B1 | `X` | grass | — |
| `c22` | 0x2B2 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `c32` | 0x2B3 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `c42` | 0x2B4 | `X` | grass | — |
| `c52` | 0x2B5 | `X` | grass | — |

## Tents

### Felt tents

`tents`, 7 wide by 3 tall. Round felt tents, 3 x 3 on borrowed grass: `red` (`red00` to `red22`, column then row) is the Amazons' red felt banded with cream; `cream` is undyed felt banded red, the guest tent you're lodged in. The domes' top rows are drawn over the player; the door flap is the bottom middle cell (`MB_NON_ANIMATED_DOOR`). Swaps for the bottom middle cell: `ascl_door` (on the cream tent: the rod of Asclepius painted on its flap, Themiskyra's Asclepeion tent), `agora_door` (on the red tent: an awning and goods, the Agora of Pontic goods). `flap_open` is a flap tied back (`MB_NON_ANIMATED_DOOR`), for a household that's expecting you. For the Oikoumene's Wagon Camp too.

```
2C0 2C1 2C2 2C3 2C4 2C5 2C6    TTTTTTX
2C8 2C9 2CA 2CB 2CC 2CD 2CE    XXXXXXD
2D0 2D1 2D2 2D3 2D4 2D5 2D6    XDXXDXD
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `red00` | 0x2C0 | `T` | grass | — |
| `red10` | 0x2C1 | `T` | grass | — |
| `red20` | 0x2C2 | `T` | grass | — |
| `red01` | 0x2C8 | `X` | grass | — |
| `red11` | 0x2C9 | `X` | grass | — |
| `red21` | 0x2CA | `X` | grass | — |
| `red02` | 0x2D0 | `X` | grass | — |
| `red12` | 0x2D1 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `red22` | 0x2D2 | `X` | grass | — |
| `cream00` | 0x2C3 | `T` | grass | — |
| `cream10` | 0x2C4 | `T` | grass | — |
| `cream20` | 0x2C5 | `T` | grass | — |
| `cream01` | 0x2CB | `X` | grass | — |
| `cream11` | 0x2CC | `X` | grass | — |
| `cream21` | 0x2CD | `X` | grass | — |
| `cream02` | 0x2D3 | `X` | grass | — |
| `cream12` | 0x2D4 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `cream22` | 0x2D5 | `X` | grass | — |
| `ascl_door` | 0x2D6 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `agora_door` | 0x2CE | `D` | grass | MB_NON_ANIMATED_DOOR |
| `flap_open` | 0x2C6 | `X` | grass | — |

### Felt-roofed wagon-houses *(Oikoumene)*

`wagons`, 3 wide by 4 tall. The Scythians' houses on wheels (Herodotus 4.46): a wagon-house is 3 x 2, a felt roof over a timber body on four solid wheels. Pick a roof row, `red_roof0` `red_roof1` `red_roof2` (red felt), `cream_roof*` (undyed felt) or `black_roof*` (black felt stitched with blue), drawn over the player, and put `body0` `body1` `body2` below it; `body1` is the door (`MB_NON_ANIMATED_DOOR`), the rest impassable. Three households, three roofs: the archer chief's, the barrow-keeper's, the racer's (OIKOUMENE 4.4's Wagon Camp).

```
2D8 2D9 2DA    TTT
2E0 2E1 2E2    TTT
2E8 2E9 2EA    TTT
2F0 2F1 2F2    XDX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `red_roof0` | 0x2D8 | `T` | grass | — |
| `red_roof1` | 0x2D9 | `T` | grass | — |
| `red_roof2` | 0x2DA | `T` | grass | — |
| `cream_roof0` | 0x2E0 | `T` | grass | — |
| `cream_roof1` | 0x2E1 | `T` | grass | — |
| `cream_roof2` | 0x2E2 | `T` | grass | — |
| `black_roof0` | 0x2E8 | `T` | grass | — |
| `black_roof1` | 0x2E9 | `T` | grass | — |
| `black_roof2` | 0x2EA | `T` | grass | — |
| `body0` | 0x2F0 | `X` | grass | — |
| `body1` | 0x2F1 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `body2` | 0x2F2 | `X` | grass | — |

## Yard

### Hearths, the practice ground, horses

`yard`, 8 wide by 2 tall. On borrowed grass, impassable. `hearth`: a camp hearth in a ring of stones, its fire flickering (`fire`); `cauldron`: a Thracian bronze cauldron on a tripod over the fire (the cook fires of Themiskyra). `milking_post`: a post with a leather pail and a rope for the mares (OIKOUMENE 4.4; the mare-milker's daily milk). `well`: Themiskyra's well, a stone curb with a timber frame. The practice ground: `target` (with `target_top`), a straw butt on a stand painted in rings; `rack_L` `rack_R`, a rack of spears with crescent pelta shields; `post`, a hacked training post; `shields`, a stand of bronze-faced shields; `standard` (with `standard_top`), Ares's spear-standard with red streamers. A tethered horse (2 x 2, `horse_TL` to `horse_BR`): a bay mare tied to her post, standing; her top row is drawn over the player. Top rows marked `T` are the tall pieces' heads.

```
300 301 302 303 304 305 306 307    XXXXTTTT
308 309 30A 30B 30C 30D 30E 30F    XXXXXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `hearth` | 0x300 | `X` | grass | — |
| `cauldron` | 0x301 | `X` | grass | — |
| `milking_post` | 0x302 | `X` | grass | — |
| `well` | 0x303 | `X` | grass | — |
| `target_top` | 0x304 | `T` | grass | — |
| `target` | 0x30C | `X` | grass | — |
| `standard_top` | 0x305 | `T` | grass | — |
| `standard` | 0x30D | `X` | grass | — |
| `rack_L` | 0x308 | `X` | grass | — |
| `rack_R` | 0x309 | `X` | grass | — |
| `post` | 0x30A | `X` | grass | — |
| `shields` | 0x30B | `X` | grass | — |
| `horse_TL` | 0x306 | `T` | grass | — |
| `horse_TR` | 0x307 | `T` | grass | — |
| `horse_BL` | 0x30E | `X` | grass | — |
| `horse_BR` | 0x30F | `X` | grass | — |

### Horse-field fence

`fence`, 4 wide by 3 tall. A two-rail timber fence on borrowed grass, impassable. `H_L` `H` `H_R`: a west-east run and its ends; `V_T` `V` `V_B`: a north-south run; `NW` `NE` `SW` `SE`: the corners of a paddock (`NW` is its top-left); `gate` and `gate_V`: an open gateway in a run (walkable). Themiskyra's horse field, Diomedes's yard, the Wagon Camp's horse lines.

```
310 311 312 313    XXX.
318 319 31A 31B    XXX.
320 321 322 323    XXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `H_L` | 0x310 | `X` | grass | — |
| `H` | 0x311 | `X` | grass | — |
| `H_R` | 0x312 | `X` | grass | — |
| `gate` | 0x313 | `.` | grass | — |
| `V_T` | 0x318 | `X` | grass | — |
| `V` | 0x319 | `X` | grass | — |
| `V_B` | 0x31A | `X` | grass | — |
| `gate_V` | 0x31B | `.` | grass | — |
| `NW` | 0x320 | `X` | grass | — |
| `NE` | 0x321 | `X` | grass | — |
| `SW` | 0x322 | `X` | grass | — |
| `SE` | 0x323 | `X` | grass | — |

### A trough and hay

`troughs`, 3 wide by 1 tall. On borrowed grass, impassable: `trough_L` `trough_R`, a hollowed-log water trough two cells long; `hay`, a stack of hay on a pole, eaten at the bottom.

```
314 315 316    XXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `trough_L` | 0x314 | `X` | grass | — |
| `trough_R` | 0x315 | `X` | grass | — |
| `hay` | 0x316 | `X` | grass | — |
