# steppe_town tileset catalog

`gTileset_SteppeTown` is the Greek colonies of the steppe coast: Abdera and Olbia.  Pair it with the `aethos` primary, which supplies the open grass, the limestone path, sand, the sea, olives and cypresses. It is one of the steppe family (`steppe`, `steppe_town`, `steppe_camp`).

**This file is generated.** `tools/ichor/art/farlands_build.py steppe_town` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/farlands_steppe_town.py` (with `farlands_ground.py` and `farlands_kits.py`); the palette groups are in that file's `GROUPS`, the borrowed ground in `farlands_lib.py`.

| Image | Shows |
|---|---|
| [`img/farlands_steppe_town_pieces.png`](img/farlands_steppe_town_pieces.png) | Every structure on its ground (`*` marks the Oikoumene's pieces) |
| [`img/farlands_steppe_town_sheet.png`](img/farlands_steppe_town_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

**Why a sister set.** The steppe's land (grasses, rivers, kurgans, the heights) fills `steppe`'s 504 tiles, so the towns built on it are their own sets: this one for the Greek colonies, `steppe_camp` for the horse-peoples' camps. A colony that borders the open steppe meets it across a seam strip of aethos ground (MAP_DESIGN 5). The road and its joins are the steppe's own, redrawn here.

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row, with the walk codes beside them. Each section starts on a fixed row of the sheet (ground at 0x200, houses at 0x250, civic at 0x290, harbor at 0x2C0, market at 0x2E0). Structures are placed first-fit in build order, so appending one never moves another. Place pieces by key and name, never by raw id: `tools/ichor/maps/farlands_tiles.py` holds every far-lands catalog as a Python dict (`mid('steppe_town', key, piece)`, and `soft('steppe_town', key, region, x, y)` for soft ground); `build/steppe_town/catalog.json` is the same as JSON.

**The Oikoumene's pieces** (drawn for world-oikoumene's lands, OIKOUMENE.md; `oikoumene_pieces('steppe_town')` lists them): `house`, `civic`, `temple`, `quay`, `market`, `pen`. The rest serve LABORS's maps first; both sessions may use anything here.

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

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player), `COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color groups, one per secondary palette (6-12), passed to Porytiles as packing hints.

| Group | Use | Colors |
|---|---|---|
| earth |  | `g1` `g2` `g3` `gd` `l0` `l1` `rd0` `rd3` `p1` `p2` `p3` `md0` `md1` `md2` `sg2` |
| roof |  | `tc0` `tc1` `tc2` `sg0` `sg1` `sg2` `sg3` `tb0` `tb1` `ink` `gd` `g1` `w1` `w0` `bz3` |
| wall |  | `mb1` `mb2` `mb3` `tb0` `tb1` `tb2` `tb3` `tb4` `w0` `w1` `ink` `gd` `k1` `fb` `g1` |
| quay |  | `b2` `b3` `b4` `w0` `tb0` `tb1` `tb2` `tb3` `tb4` `sn1` `sn2` `sn3` `ink` `sg3` `fr2` |
| market |  | `fr1` `fr2` `fr3` `fc1` `fc2` `tc1` `tc2` `tb1` `tb2` `tb3` `sn2` `sn3` `ink` `gd` `sg2` |
| temple |  | `w0` `w1` `k2` `k3` `p1` `p2` `p3` `bz1` `bz2` `bz3` `ink` `tc1` `b1` `gd` `g1` |

**Tile budget.** 286 of 496 tiles (264 metatiles). Its maps use wide doors, whose animation frames copy over tiles 496-511 (`DOOR_TILE_START_SIZE2`, `src/field_door.c`), so the build fails past 496. Static tiles within two pixels of one another are merged.

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

## Houses

### The colony house kit *(Oikoumene)*

`house`, 6 wide by 6 tall. Greek houses built from the north coast's materials, as a kit: a front is three rows, the roof's upper half (`*_A_*`, drawn over the player), its lower half (`*_B_*`, ending in the eave) and the wall. Roofs: `tile` (terracotta pantiles, the colonists' pride) or `thatch` (reed, as the Thracians roof). Walls: `brick` (plastered mud-brick) or `timber` (weathered planks), each with `L` `M` `R`, a `door` (`MB_NON_ANIMATED_DOOR`), a `window` and a shuttered `shutter`. Repeat `_M` for a longer house. Ready-made fronts are listed below (`fronts`), five of them, for Abdera and for the Oikoumene's Olbia. On borrowed grass: put a path or the road in front of the door.

```
250 251 252 253 254 255    TTTTTT
258 259 25A 25B 25C 25D    XXXXXX
260 261 262 263 264 265    TTTTTT
268 269 26A 26B 26C 26D    XXXXXX
270 271 272 273 274 275    XXXDXX
278 279 27A 27B 27C 27D    XXXDXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `tile_A_L` | 0x250 | `T` | grass | — |
| `tile_B_L` | 0x258 | `X` | grass | — |
| `tile_A_M` | 0x251 | `T` | grass | — |
| `tile_B_M` | 0x259 | `X` | grass | — |
| `tile_A_R` | 0x252 | `T` | grass | — |
| `tile_B_R` | 0x25A | `X` | grass | — |
| `thatch_A_L` | 0x260 | `T` | grass | — |
| `thatch_B_L` | 0x268 | `X` | grass | — |
| `thatch_A_M` | 0x261 | `T` | grass | — |
| `thatch_B_M` | 0x269 | `X` | grass | — |
| `thatch_A_R` | 0x262 | `T` | grass | — |
| `thatch_B_R` | 0x26A | `X` | grass | — |
| `brick_L` | 0x270 | `X` | grass | — |
| `brick_M` | 0x271 | `X` | grass | — |
| `brick_R` | 0x272 | `X` | grass | — |
| `brick_door` | 0x273 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `brick_window` | 0x274 | `X` | grass | — |
| `brick_shutter` | 0x275 | `X` | grass | — |
| `timber_L` | 0x278 | `X` | grass | — |
| `timber_M` | 0x279 | `X` | grass | — |
| `timber_R` | 0x27A | `X` | grass | — |
| `timber_door` | 0x27B | `D` | grass | MB_NON_ANIMATED_DOOR |
| `timber_window` | 0x27C | `X` | grass | — |
| `timber_shutter` | 0x27D | `X` | grass | — |

## Civic

### Asclepeion and Agora pieces *(Oikoumene)*

`civic`, 6 wide by 1 tall. The colony's Asclepeion and Agora, built from the house kit plus these. Asclepeion (5 wide): roof `tile_A_L tile_A_M ascl_ped tile_A_M tile_A_R` (the pediment carries the bronze rod of Asclepius), `tile_B_*` below, wall `brick_L ascl_col ascl_door ascl_col brick_R` (whitewashed porch posts, the door with its snake plaque). Agora (5 wide): roof `thatch_A_L thatch_A_M agora_ped thatch_A_M thatch_A_R` (a painted pinax of an amphora), `thatch_B_*`, wall `timber_L agora_awning agora_door agora_awning timber_R` (a striped awning over goods). Doors are `MB_NON_ANIMATED_DOOR`; the pediments are drawn over the player.

```
290 291 292 293 294 295    TDXTDX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `ascl_ped` | 0x290 | `T` | grass | — |
| `ascl_door` | 0x291 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `ascl_col` | 0x292 | `X` | grass | — |
| `agora_ped` | 0x293 | `T` | grass | — |
| `agora_door` | 0x294 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `agora_awning` | 0x295 | `X` | grass | — |

### A small temple of Apollo *(Oikoumene)*

`temple`, 4 wide by 3 tall. The colonists' temple of Apollo the Healer, 4 x 3 on borrowed grass: a limestone porch of four Ionic columns on three steps, a pediment with the sun's bronze disc and a painted cornice, the doorway between the middle columns (`door_L` and `door_R`, a two-cell doorway, `MB_NON_ANIMATED_DOOR`). Its top row is drawn over the player. For Olbia (the Oikoumene's) and any colony that has room for it.

```
298 299 29A 29B    TTTT
2A0 2A1 2A2 2A3    XXXX
2A8 2A9 2AA 2AB    XDDX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `c00` | 0x298 | `T` | grass | — |
| `c10` | 0x299 | `T` | grass | — |
| `c20` | 0x29A | `T` | grass | — |
| `c30` | 0x29B | `T` | grass | — |
| `c01` | 0x2A0 | `X` | grass | — |
| `c11` | 0x2A1 | `X` | grass | — |
| `c21` | 0x2A2 | `X` | grass | — |
| `c31` | 0x2A3 | `X` | grass | — |
| `c02` | 0x2A8 | `X` | grass | — |
| `c12` | 0x2A9 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `c22` | 0x2AA | `D` | grass | MB_NON_ANIMATED_DOOR |
| `c32` | 0x2AB | `X` | grass | — |
| `door_L` | 0x2A9 | `D` | grass | MB_NON_ANIMATED_DOOR |
| `door_R` | 0x2AA | `D` | grass | MB_NON_ANIMATED_DOOR |

## Harbor

### The river-mouth quay *(Oikoumene)*

`quay`, 8 wide by 2 tall. A timber quay on piles where the river meets the sea. `deck`: plain planking (walkable, drawn whole). Its edges over borrowed sea, walkable: `edge_S` (the deck's south edge, the water below), `edge_E` `edge_W`, `corner_SE` `corner_SW`. `gangplank`: the edge with a plank run out over the water to the ship (put `EventScript_IchorBoardShip` here, and the voyage row in `ichor_voyages.h`). `post`: a mooring post on the deck (impassable). `boat_L` `boat_R`: a Thracian fishing boat drawn up on borrowed sea; `nets`: nets drying on a rack (on the deck, impassable). For Abdera's harbor and Olbia's (the Oikoumene's).

```
2C0 2C1 2C2 2C3 2C4 2C5 2C6 2C7    ......XX
2C8 2C9 2CA 2CB 2CC 2CD 2CE 2CF    XXX.....
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `deck` | 0x2C0 | `.` | drawn | — |
| `edge_S` | 0x2C1 | `.` | sea | — |
| `edge_E` | 0x2C2 | `.` | sea | — |
| `edge_W` | 0x2C3 | `.` | sea | — |
| `corner_SE` | 0x2C4 | `.` | sea | — |
| `corner_SW` | 0x2C5 | `.` | sea | — |
| `gangplank` | 0x2C6 | `X` | sea | — |
| `post` | 0x2C7 | `X` | drawn | — |
| `boat_L` | 0x2C8 | `X` | sea | — |
| `boat_R` | 0x2C9 | `X` | sea | — |
| `nets` | 0x2CA | `X` | drawn | — |

## Market

### Stalls, a cart, goods *(Oikoumene)*

`market`, 6 wide by 2 tall. On borrowed grass (or set them on aethos path). `stall` (2 x 2): a striped felt awning on poles over a counter of Thracian goods; `fur` (2 x 2): a trader's stall hung with furs from the north; their top rows are drawn over the player, the counters impassable (put the clerk behind). `cart_L` `cart_R`: a two-wheeled ox-cart loaded with grain sacks. `amphorae`: a stack of wine jars; `salt_fish`: fish drying on a rack (the Pontic trade). All impassable.

```
2E0 2E1 2E2 2E3 2E4 2E5    TTTTXX
2E8 2E9 2EA 2EB 2EC 2ED    XXXXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `stall_TL` | 0x2E0 | `T` | grass | — |
| `stall_TR` | 0x2E1 | `T` | grass | — |
| `stall_BL` | 0x2E8 | `X` | grass | — |
| `stall_BR` | 0x2E9 | `X` | grass | — |
| `fur_TL` | 0x2E2 | `T` | grass | — |
| `fur_TR` | 0x2E3 | `T` | grass | — |
| `fur_BL` | 0x2EA | `X` | grass | — |
| `fur_BR` | 0x2EB | `X` | grass | — |
| `cart_L` | 0x2EC | `X` | grass | — |
| `cart_R` | 0x2ED | `X` | grass | — |
| `amphorae` | 0x2E4 | `X` | grass | — |
| `salt_fish` | 0x2E5 | `X` | grass | — |

### The horse-market pen *(Oikoumene)*

`pen`, 4 wide by 3 tall. A two-rail timber fence on borrowed grass, impassable. `H_L` `H` `H_R`: a west-east run and its ends; `V_T` `V` `V_B`: a north-south run; `NW` `NE` `SW` `SE`: the corners of a paddock (`NW` is its top-left); `gate` and `gate_V`: an open gateway in a run (walkable). For the horse market (put horses in it as Pokémon objects) and any paddock in town.

```
2F0 2F1 2F2 2F3    XXX.
2F8 2F9 2FA 2FB    XXX.
300 301 302 303    XXXX
```

| Piece | Id | Walk | Ground | Behavior |
|---|---|---|---|---|
| `H_L` | 0x2F0 | `X` | grass | — |
| `H` | 0x2F1 | `X` | grass | — |
| `H_R` | 0x2F2 | `X` | grass | — |
| `gate` | 0x2F3 | `.` | grass | — |
| `V_T` | 0x2F8 | `X` | grass | — |
| `V` | 0x2F9 | `X` | grass | — |
| `V_B` | 0x2FA | `X` | grass | — |
| `gate_V` | 0x2FB | `.` | grass | — |
| `NW` | 0x300 | `X` | grass | — |
| `NE` | 0x301 | `X` | grass | — |
| `SW` | 0x302 | `X` | grass | — |
| `SE` | 0x303 | `X` | grass | — |
