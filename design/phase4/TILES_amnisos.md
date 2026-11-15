# amnisos tileset catalog

`gTileset_Amnisos` is Amnisos, the harbor of Knossa (Act III, Knossa; LABYRINTH.md §2-§3, §11; SCRIPT.md Part 10). It serves Amnisos (`MAP_KNOSSA_AMNISOS`). Pair it with the `aethos` primary, which supplies the open grass, paths, sand, sea, olives, cypresses, ledges and the Asclepeion and Agora fronts.

**This file is generated.** `tools/ichor/art/knossa_build.py amnisos` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/knossa_*.py`, the palette plan in `knossa_lib.py`, what each tileset holds in `knossa_specs.py`; `knossa_scene.py` renders the mock scenes.

| Image | Shows |
|---|---|
| [`img/knossa_amnisos_quay.png`](img/knossa_amnisos_quay.png) | A 240 x 160 screen of Amnisos's quay at dawn: the Titan ships at the mole, the Asclepeion and the Agora, hives on every roof (3x; `_1x` is 1x) |
| [`img/knossa_amnisos_town.png`](img/knossa_amnisos_town.png) | Amnisos: the quay and the mole, the five houses, the cliff and the Cave of Eileithyia's mouth, the south gap |
| [`img/amnisos_pieces.png`](img/amnisos_pieces.png) | Every structure on its ground |
| [`img/amnisos_sheet.png`](img/amnisos_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

![A 240 x 160 screen of Amnisos's quay at dawn: the Titan ships at the mole, the Asclepeion and the Agora, hives on every roof (3x; `_1x` is 1x)](img/knossa_amnisos_quay.png)

## The Knossa family

LABYRINTH.md §11 planned one `knossa` secondary for Amnisos, the Bull Road and the
palace. Their pieces come to far more than one secondary's 504 tiles (the palace's
frescoes alone would fill half of one), so the art is split by map, as the Kythera
family is. All are built by `tools/ichor/art/knossa_build.py` from shared painters, so a
piece two of them carry (the limestone cliff, the surf, the hives) is drawn once and
looks the same in both. The labyrinth tileset (`TILES_labyrinth.md`) is the Labyrinth's
own and is not part of this family, but the palace's Minoan red, ochre, gypsum and fresco
blue are its colors exactly, so the Grand Staircase meets Ring I in one palette.

| Tileset | Symbol | Primary | Maps | Catalog |
|---|---|---|---|---|
| `amnisos` | `gTileset_Amnisos` | aethos | Amnisos | [`TILES_amnisos.md`](TILES_amnisos.md) |
| `bull_road` | `gTileset_BullRoad` | aethos | the Bull Road, the vineyard terraces, the Bronze Heel | [`TILES_bull_road.md`](TILES_bull_road.md) |
| `palace_minos` | `gTileset_PalaceMinos` | aethos | the Palace of Minos above ground | [`TILES_palace_minos.md`](TILES_palace_minos.md) |
| `palace_rooms` | `gTileset_PalaceRooms` | oikos (any) | the Throne Room, the West Magazines, the Queen's Megaron, the Grand Staircase | [`TILES_palace_rooms.md`](TILES_palace_rooms.md) |
| `ida` | `gTileset_Ida` | aethos | the Ida path, the cradle shrine, the Idaean Cave, the Cave of Eileithyia | [`TILES_ida.md`](TILES_ida.md) |

**Seams between them** (MAP_DESIGN §5). With the split, the seam rule applies wherever
neighbours use different secondaries:

| Seam | Tilesets | Rule |
|---|---|---|
| Amnisos's south gap ↔ the Bull Road's north end | amnisos / bull_road | the 6 rows nearest the seam, on both maps, use only `aethos` |
| the Bull Road's south end ↔ the Palace of Minos's north edge | bull_road / palace_minos | 6 rows, both maps |
| the Bull Road's fork ↔ the Bronze Heel | bull_road / bull_road | exempt (one tileset) |
| the Bull Road ↔ the vineyard terraces | bull_road / bull_road | exempt, if it is a connection; a warp through the terrace gap needs nothing |
| the Bull Road's Ida gate ↔ the Ida path | bull_road / ida | a warp through the gate needs nothing; as a connection, 6 rows (or 8 columns), both maps |
| the Ida path ↔ the cradle shrine | ida / ida | exempt |
| Amnisos ↔ the Cave of Eileithyia, the palace ↔ its rooms, the cradle shrine ↔ the Idaean Cave | — | warps, no seam |

Gates, lanes and the sea are aethos's anyway, so the strips cost little: plant aethos
olives, cypresses, grass, path and ledges there.

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet (harbor at 0x200, town at 0x250, coast at 0x270, land at 0x290). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/knossa_tiles.py` holds every Knossa
catalog as a Python dict (`mid('amnisos', 'quay', 'E', ...)`, `place(...)`, `front(...)`),
and `build/amnisos/catalog.json` is the same as JSON.

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
| `J` | Ledge: `MB_JUMP_SOUTH`. |
| `S` | Sand: `MB_SAND`. |

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea* or *shallow* draw no
ground of their own: after Porytiles compiles, the build points their bottom-layer tiles
at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated sea
(`0x170`) or animated turquoise shallows (`0x0D1`). They meet aethos ground exactly and
cost no tiles. Rebuild whenever aethos is repainted; the build checks every borrowed
entry. A borrowed cell's own art is in one layer: the middle (`COVERED`, under the
player) or the top (`SPLIT`, over the player).

**Animations.** Porytiles animations in this tileset, driven by `InitTilesetAnim_PorytilesManaged_Amnisos` (`include/porytiles_generated/tilesets/amnisos/generated_anim_code.h`): `bees`: bees flying at the hives' mouths (3 frames); `surf`: the foam on the shore and round rocks, washing up and back (3 frames, ping-pong; Kythera's). Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet. The sea and shallows under them are aethos's own animations.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color
groups, one per secondary palette (`knossa_lib.GROUPS`), passed to Porytiles as packing
hints:

| Group | Use |
|---|---|
| minoan | Minoan red, ochre, gypsum, black and terracotta (labyrinth_art's): red columns, black capitals, horns of consecration, labrys marks, pithoi, the houses, the hives |
| fresco | Fresco blue, white, saffron and skin (labyrinth_art's): dolphins, lilies, bull-leapers, the lily prince, saffron gatherers, blue monkeys, griffins |
| stone | Cretan limestone on aethos grass: cliffs, terrace and town walls, the goat path |
| foam | Kythera's surf, foam lace, wet rock and quay edges |
| green | Vines and grapes, holm oak, phrygana and thyme, on aethos grass |
| bronze | Bronze and verdigris (Talos's foot, the Kouretes' shields, door fittings), and the marble herm |
| terra | Kythera's timber and terracotta: boats, the triremes, nets, trellis posts |

**Tile budget.** 426 of 504 tiles (208 metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.

## The harbor

### The curved stone quay

`quay`, 8 wide by 3 tall. Amnisos's quay and the mole that curves out east from it (Kythera's quay kit). Its top is aethos's limestone path (`0x1D9`); these edges finish it where the wall drops into the sea (each borrows aethos's sea). Named by where the sea is: `S` (`S_b` adds a drain, `ring_S` a mooring ring), `N`, `E`, `W`; `out_*` are rounded outer corners, `in_*` the inside of a bend, so the mole can curve. A mole two cells wide is an `N` row over an `S` row. `steps_E` / `steps_S` go down to the water (walkable); `N_plank` takes a gangplank from a ship moored north of the quay, `S_plank` one going down to a boat (walkable). Other edge cells are impassable.

```text
ids                                                  walk
0x200 0x201 0x202 0x203 0x204 0x205 0x206 0x207   X X X X X X X X
0x208 0x209 0x20A 0x20B 0x20C 0x20D 0x20E 0x20F   X X X X X . . X
0x210 0x211 0x212 0x213 0x214 0x215 0x216 0x217   . . . . . . . .
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
| 0x20D | `steps_E` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x20E | `steps_S` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x20F | `ring_S` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x210 | `N_plank` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x211 | `S_plank` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x212 | (2, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x213 | (3, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x214 | (4, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x215 | (5, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x216 | (6, 2) | `.` | `MB_NORMAL` | COVERED | sea |
| 0x217 | (7, 2) | `.` | `MB_NORMAL` | COVERED | sea |

### A Titan trireme, furled

`titan_trireme`, 8 wide by 3 tall. One of the four Titan triremes moored at Amnisos's mole (SCRIPT.md III-3A): black-tarred, her slate sail furled on the yard with a sickle chalked on it, no crew on deck. 8 x 3 on borrowed sea, bow to the east; moor four along the mole's north side, each wholly on sea cells. Impassable. **Sailed:** when `FLAG_ICHOR_HIDE_TITAN_SHIPS` is set (after the Turning), swap each ship's 24 cells to aethos sea (`0x170`): nothing is left at the mole.

```text
ids                                                  walk
0x218 0x219 0x21A 0x21B 0x21C 0x21D 0x21E 0x21F   X X X X X X X X
0x220 0x221 0x222 0x223 0x224 0x225 0x226 0x227   X X X X X X X X
0x228 0x229 0x22A 0x22B 0x22C 0x22D 0x22E 0x22F   X X X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x218 | (0, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x219 | (1, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x21A | (2, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x21B | (3, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x21C | (4, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x21D | (5, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x21E | (6, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x21F | (7, 0) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x220 | `stern` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x221 | (1, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x222 | (2, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x223 | (3, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x224 | (4, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x225 | (5, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x226 | (6, 1) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x227 | `bow` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x228 | (0, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x229 | (1, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x22A | (2, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x22B | (3, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x22C | (4, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x22D | (5, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x22E | (6, 2) | `X` | `MB_NORMAL` | COVERED | sea |
| 0x22F | (7, 2) | `X` | `MB_NORMAL` | COVERED | sea |

### A fishing boat, afloat and beached

`kaiki`, 2 wide by 1 tall. A kaiki, the island's fishing boat, bow to the east, 3 x 2 each: `afloat` on borrowed sea, `beached` drawn up on the sand (borrowed sand). Impassable.

```text
ids              walk
0x230 0x231   X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x230 | `afloat` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x231 | `beached` | `X` | `MB_NORMAL` | COVERED | sand |

### The harbor's gear

`gear`, 6 wide by 1 tall. Harbor gear on borrowed path (Kythera's): `oars`, `nets` (walkable), `rope`, `amphorae`, `crate`, `bollard`. Impassable but `nets`.

```text
ids                                      walk
0x232 0x233 0x234 0x235 0x236 0x237   X X . X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x232 | `oars` | `X` | `MB_NORMAL` | COVERED | path |
| 0x233 | `nets` | `X` | `MB_NORMAL` | COVERED | path |
| 0x234 | `rope` | `.` | `MB_NORMAL` | COVERED | path |
| 0x235 | `amphorae` | `X` | `MB_NORMAL` | COVERED | path |
| 0x236 | `crate` | `X` | `MB_NORMAL` | COVERED | path |
| 0x237 | `bollard` | `X` | `MB_NORMAL` | COVERED | path |

### The harbor shrine

`shrine`, 1 wide by 2 tall. Amnisos's harbor shrine at the quay's end: a gypsum pillar under horns of consecration, a red double axe painted on its face, a honey jar at its foot (on borrowed path). `top` is drawn over the player; `base` is impassable and takes the bg event. The Bronze Obol is hidden behind it.

```text
ids        walk
0x238   T
0x240   X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x238 | `top` | `T` | `MB_NORMAL` | SPLIT | path |
| 0x240 | `base` | `X` | `MB_NORMAL` | COVERED | path |

### Quay flagstones

`flags`, 6 wide by 1 tall. The quay's paving: lay `A`, `B` and `C` in a staggered mix (no two of a kind side by side reads best), with a `drain` grate, an iron mooring `ring` let into a slab, and a `worn` cracked slab here and there. Walkable.

```text
ids                                      walk
0x239 0x23A 0x23B 0x23C 0x23D 0x23E   . . . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x239 | `A` | `.` | `MB_NORMAL` | COVERED |  |
| 0x23A | `B` | `.` | `MB_NORMAL` | COVERED |  |
| 0x23B | `C` | `.` | `MB_NORMAL` | COVERED |  |
| 0x23C | `drain` | `.` | `MB_NORMAL` | COVERED |  |
| 0x23D | `ring` | `.` | `MB_NORMAL` | COVERED |  |
| 0x23E | `worn` | `.` | `MB_NORMAL` | COVERED |  |

## Town

### The Minoan house kit

`house`, 8 wide by 4 tall. Parts that snap together into Amnisos's houses (see *House fronts* below): plastered walls banded with timber, the joists' round ends in a row, windows of four red-painted panes, flat roofs of beaten earth. Rows: `R_*` the flat roof and its parapet, seen from above; `U_*` the upper wall; `G_*` and the doors, the ground-floor wall over its ochre dado and gypsum socle. Columns `_L` (the lit west corner), `_M` (repeat it), `_R` (the shaded east corner). **A hive on every roof** (LABYRINTH §2): `R_hive` (three clay hive-tubes, the Minoan kind), `R_skep` (two straw skeps), and `R_hive_L` / `R_hive_R`, the tubes at a roof's corners; bees fly at their mouths (the `bees` animation). Roof extras: `R_horns` (horns of consecration on the parapet, for the grander houses), `R_ladder` (a ladder's top over the parapet), `R_jar` (a water jar). Upper wall: `U_window` (four red panes), `U_window_R` (the same at the shaded corner), `U_windows` (two small ones), `U_frieze` (a painted band of running spirals), `U_ladder`. Ground floor: `door` and `door_axe` (`MB_NON_ANIMATED_DOOR`; `door_axe` hangs the tavern's board with its red double axe), `G_window`, `G_window_R`, `G_ladder`, `G_steps` (an outside stair climbing the wall west to east, arriving at `R_steps` on the roof), `G_pithos` (a storage jar against the wall), `G_octopus` (octopus traps stacked by the wall, one drying on a line: the fisher's hut), `G_bench` (a gypsum bench), `G_hives` (hive-tubes built into the wall, Kydon's honey house). **The ladder** (`G_ladder`, `U_ladder`, `R_ladder` in one column) climbs to a roof: its cells are walkable. To make a roof a terrace to stand on, set its plain roof cells passable at a higher elevation than the street and the ladder elevation 0, as for stairs, so the player can only get up by the ladder (the kid by the hives waits up there). Every other cell is impassable.

```text
ids                                                  walk
0x250 0x251 0x252 0x253 0x254 0x255 0x256 0x257   X X X X X X . X
0x258 0x259 0x25A 0x25B 0x25C 0x25D 0x25E 0x25F   X X X X X X . X
0x260 0x261 0x262 0x263 0x264 0x265 0x266 0x267   X X X D D X . X
0x268 0x269 0x26A 0x26B 0x26C 0x26D 0x26E 0x26F   X X X X X X . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x250 | `R_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x251 | `R_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x252 | `R_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x253 | `R_hive` | `X` | `MB_NORMAL` | COVERED |  |
| 0x254 | `R_skep` | `X` | `MB_NORMAL` | COVERED |  |
| 0x255 | `R_horns` | `X` | `MB_NORMAL` | COVERED |  |
| 0x256 | `R_ladder` | `.` | `MB_NORMAL` | COVERED |  |
| 0x257 | `R_jar` | `X` | `MB_NORMAL` | COVERED |  |
| 0x258 | `U_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x259 | `U_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25A | `U_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25B | `U_window` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25C | `U_windows` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25D | `U_frieze` | `X` | `MB_NORMAL` | COVERED |  |
| 0x25E | `U_ladder` | `.` | `MB_NORMAL` | COVERED |  |
| 0x25F | `U_window_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x260 | `G_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x261 | `G_M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x262 | `G_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x263 | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x264 | `door_axe` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x265 | `G_window` | `X` | `MB_NORMAL` | COVERED |  |
| 0x266 | `G_ladder` | `.` | `MB_NORMAL` | COVERED |  |
| 0x267 | `G_pithos` | `X` | `MB_NORMAL` | COVERED |  |
| 0x268 | `G_octopus` | `X` | `MB_NORMAL` | COVERED |  |
| 0x269 | `G_bench` | `X` | `MB_NORMAL` | COVERED |  |
| 0x26A | `R_hive_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x26B | `R_hive_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x26C | `G_window_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x26D | `G_hives` | `X` | `MB_NORMAL` | COVERED |  |
| 0x26E | `G_steps` | `.` | `MB_NORMAL` | COVERED |  |
| 0x26F | `R_steps` | `.` | `MB_NORMAL` | COVERED |  |

### House fronts

Every house is a home (MAP_DESIGN.md §2), so each front has a door. These are arrangements of the kit's parts and cost no metatiles of their own; mix the parts for more (`knossa_tiles.front()`). Walk: every house cell is `X` except its door (`D`) and a ladder or stair.

**Kydon's honey house** (`honey_house`): Kydon's: hive-tubes in the wall, skeps and tubes on the roof (the Honey gift).

```text
ids                          walk
0x250 0x253 0x254 0x26B   X X X X
0x258 0x25B 0x259 0x25F   X X X X
0x260 0x26D 0x263 0x262   X X D X
```

**The Double Axe** (`tavern`): the tavern, its board hung by the door (the knucklebones champion).

```text
ids                                walk
0x26A 0x251 0x257 0x254 0x252   X X X X X
0x258 0x25C 0x25D 0x25B 0x25A   X X X X X
0x260 0x267 0x264 0x265 0x262   X X D X X
```

**Aithon's house** (`xenia_house`): the xenia host's, horns on the parapet (rest until a chosen hour).

```text
ids                                walk
0x250 0x253 0x255 0x254 0x252   X X X X X
0x258 0x25B 0x25D 0x25B 0x25A   X X X X X
0x260 0x265 0x263 0x269 0x262   X X D X X
```

**The old leaper's house** (`leaper_house`): Euanthe's, Sarpedon's wife: a ladder to the roof, where the kid by the hives waits.

```text
ids                          walk
0x250 0x251 0x256 0x26B   X X . X
0x258 0x25C 0x25E 0x25F   X X . X
0x260 0x263 0x266 0x262   X D . X
```

**Polypos's hut** (`fisher_hut`): the fisher's: octopus traps and a catch drying (a trade, and the bean story).

```text
ids                    walk
0x26A 0x254 0x252   X X X
0x268 0x263 0x26C   X D X
```

## The coast

### Foam-edged surf

`surf`, 8 wide by 2 tall. Where Amnisos's sand meets the sea. Each cell borrows aethos's animated sea and draws the sand to the waterline, a rim of turquoise shallows and the foam, which washes up and back (the `surf` animation, 3 frames). Pieces are named by where the sea is: `S` (sand north, sea south; `S2` is the same with a deeper bite, to break up a long beach), `N`, `E`, `W`; `out_NW` is the south-east tip of a sand spit (sand to the north-west, sea round it), and so on; `in_SE` is a cove's corner, sea only to the south-east. The sand above meets aethos sand (0x124) exactly; the sea below meets aethos sea (0x170). Every cell is `MB_OCEAN_WATER`, like aethos's own beach edges: surf onto it, walk on the sand beside it.

```text
ids                                                  walk
0x270 0x271 0x272 0x273 0x274 0x275 0x276 0x277   W W W W W W W W
0x278 0x279 0x27A 0x27B 0x27C 0x27D 0x27E 0x27F   W W W W W W W W
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x270 | `S` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x271 | `S2` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x272 | `N` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x273 | `E` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x274 | `W` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x275 | `out_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x276 | `out_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x277 | `out_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x278 | `out_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x279 | `in_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x27A | `in_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x27B | `in_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x27C | `in_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x27D | (5, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x27E | (6, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x27F | (7, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |

### White sand: foam lace, shells and wrack

`sand_decor`, 5 wide by 1 tall. On borrowed sand, walkable: `lace` (dried foam), `shells`, `wrack`, `footprints`, `sherd_dig` (turned earth: Amnisos's beach sherd of amphora #12, and its daily dig spot).

```text
ids                                walk
0x280 0x281 0x282 0x283 0x284   . . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x280 | `lace` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x281 | `shells` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x282 | `wrack` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x283 | `footprints` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x284 | `sherd_dig` | `.` | `MB_NORMAL` | COVERED | sand |

## The land

### Low limestone cliffs

`cliff`, 8 wide by 3 tall. Crete's grey-gold limestone, Kythera's cliff kit in Knossa's stone. A cliff whose face looks south is `lip` (the plateau's edge, on borrowed grass) over `face` over a foot: `foot_sea` (borrowed sea, foam breaking at the base, animated), `foot_sand` or `foot_grass` (walkable ground with fallen stones). `_L` / `_R` end a run. Stack `face` rows for a taller cliff. The plateau's other edges: `side_E` (plateau to the west, the drop to the east), `side_W`, `back` (plateau to the south, the drop to the north, the face hidden), `back_NW` / `back_NE`; `corner_in_E` / `_W` turn a south face into a side going north. `seep` is the face where a spring runs out. Lip and face cells are impassable.

```text
ids                                                  walk
0x290 0x291 0x292 0x293 0x294 0x295 0x296 0x297   X X X X X X X X
0x298 0x299 0x29A 0x29B 0x29C 0x29D 0x29E 0x29F   X X X X X X X .
0x2A0 0x2A1 0x2A2 0x2A3 0x2A4 0x2A5 0x2A6 0x2A7   . . W W W W W W
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x290 | `lip_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x291 | `lip` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x292 | `lip_b` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x293 | `lip_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x294 | `face_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x295 | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x296 | `face_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x297 | `face_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x298 | `side_E` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x299 | `side_W` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29A | `back` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29B | `back_NW` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29C | `back_NE` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29D | `corner_in_E` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29E | `corner_in_W` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x29F | `foot_grass` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2A0 | `foot_sand` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x2A1 | `foot_sand_rocks` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x2A2 | `foot_sea_L` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2A3 | `foot_sea` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2A4 | `foot_sea_R` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2A5 | (5, 2) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2A6 | (6, 2) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x2A7 | (7, 2) | `W` | `MB_OCEAN_WATER` | COVERED | sea |

### The town wall and its terraces

`wall`, 7 wide by 2 tall. Amnisos's town wall and the terraces the houses climb, in dry-stone Cretan limestone (Kythera's terrace kit). A `top_*` row (walkable, on borrowed grass) over a wall row `L` `M` (`M2`) `R`. **The south gap** to the Bull Road: end the wall `R`, leave the gap (two or three cells of aethos path), start again `L`, a sign beside it. `steps` cuts a stair through a terrace wall (walkable); `niche` holds a votive; `spout` is the town's fountain into a trough.

```text
ids                                            walk
0x2A8 0x2A9 0x2AA 0x2AB 0x2AC 0x2AD 0x2AE   X X X X . X X
0x2B0 0x2B1 0x2B2 0x2B3 0x2B4 0x2B5 0x2B6   . . . . T . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2A8 | `L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2A9 | `M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AA | `M2` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AB | `R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2AC | `steps` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2AD | `niche` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2AE | `spout` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2B0 | `top_L` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2B1 | `top` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2B2 | `top_M2` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2B3 | `top_R` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2B4 | `top_steps` | `T` | `MB_NORMAL` | COVERED | grass |
| 0x2B5 | `top_niche` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2B6 | `top_spout` | `.` | `MB_NORMAL` | COVERED | grass |

### The Cave of Eileithyia's mouth, and the goat path

`cave_mouth`, 4 wide by 3 tall. Set into a two-row stretch of the limestone cliff above Amnisos's west end (SCRIPT.md Part 2; stack two `cliff.face` rows either side): the brow (`lip_L` `lip` `lip_R`, on borrowed grass) over `arch_*` over `sill_L` `door` `sill_R`. A low cave mouth, its jambs squared by old hands and cut with double axes; clay figurines, a honey cake and a lamp left on the sill. `door` is `MB_NON_ANIMATED_DOOR`, the warp into the cave. The goat path climbs beside it: `stair_lip` over `stair` over `stair_foot`, rough steps cut up the face (walkable; give them elevation 0, as for stairs).

```text
ids                          walk
0x2B8 0x2B9 0x2BA 0x2BB   X X X .
0x2C0 0x2C1 0x2C2 0x2C3   X X X .
0x2C8 0x2C9 0x2CA 0x2CB   X D X .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2B8 | `lip_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B9 | `lip` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2BA | `lip_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2BB | `stair_lip` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x2C0 | `arch_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C1 | `arch` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C2 | `arch_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C3 | `stair` | `.` | `MB_NORMAL` | COVERED |  |
| 0x2C8 | `sill_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2C9 | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x2CA | `sill_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x2CB | `stair_foot` | `.` | `MB_NORMAL` | COVERED |  |
