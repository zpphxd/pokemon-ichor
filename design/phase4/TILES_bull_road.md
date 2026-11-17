# bull_road tileset catalog

`gTileset_BullRoad` is the Bull Road, its vineyard terraces and the Bronze Heel (Act III, Knossa; LABYRINTH.md §2-§3, §11; SCRIPT.md Part 10). It serves the Bull Road (`MAP_KNOSSA_BULL_ROAD`), the vineyard terraces (`MAP_KNOSSA_BULL_ROAD_VINEYARD`) and the Bronze Heel (`MAP_KNOSSA_BRONZE_HEEL`). Pair it with the `aethos` primary, which supplies the open grass, paths, sand, sea, olives, cypresses, ledges and the Asclepeion and Agora fronts.

**This file is generated.** `tools/ichor/art/knossa_build.py bull_road` paints the tileset, compiles it, registers it and rewrites this catalog. The art is in `tools/ichor/art/knossa_*.py`, the palette plan in `knossa_lib.py`, what each tileset holds in `knossa_specs.py`; `knossa_scene.py` renders the mock scenes.

| Image | Shows |
|---|---|
| [`img/knossa_bull_road.png`](img/knossa_bull_road.png) | A 240 x 160 screen of the Bull Road: the terraces stepping down north, the vineyard, the herd crossing (3x; `_1x` is 1x) |
| [`img/knossa_bull_road_wide.png`](img/knossa_bull_road_wide.png) | A wider stretch: the fork and the great herm, the cutting, the labrys door, the beekeeper's hut, Ida's gate |
| [`img/knossa_bronze_heel.png`](img/knossa_bronze_heel.png) | The Bronze Heel: Talos's foot, the tide pools, the fossil ledge |
| [`img/bull_road_pieces.png`](img/bull_road_pieces.png) | Every structure on its ground |
| [`img/bull_road_sheet.png`](img/bull_road_sheet.png) | The numbered metatile sheet, rendered from the compiled tileset |

![A 240 x 160 screen of the Bull Road: the terraces stepping down north, the vineyard, the herd crossing (3x; `_1x` is 1x)](img/knossa_bull_road.png)

It is one of the Knossa family of secondaries; see [`TILES_amnisos.md`](TILES_amnisos.md) for why the art is split and which seams then need aethos-only strips.

## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet (road at 0x200, vineyard at 0x2B0, heel at 0x2D0). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/knossa_tiles.py` holds every Knossa
catalog as a Python dict (`mid('bull_road', 'cliff', 'back', ...)`, `place(...)`, `front(...)`),
and `build/bull_road/catalog.json` is the same as JSON.

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
| `^` | Ledge down to the north: `MB_JUMP_NORTH`. |
| `S` | Sand: `MB_SAND`. |

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea* or *shallow* draw no
ground of their own: after Porytiles compiles, the build points their bottom-layer tiles
at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated sea
(`0x170`) or animated turquoise shallows (`0x0D1`). They meet aethos ground exactly and
cost no tiles. Rebuild whenever aethos is repainted; the build checks every borrowed
entry. A borrowed cell's own art is in one layer: the middle (`COVERED`, under the
player) or the top (`SPLIT`, over the player).

**Animations.** Porytiles animations in this tileset, driven by `InitTilesetAnim_PorytilesManaged_BullRoad` (`include/porytiles_generated/tilesets/bull_road/generated_anim_code.h`): `bees`: bees flying at the hives' mouths (3 frames); `surf`: the foam on the shore and round rocks, washing up and back (3 frames, ping-pong; Kythera's). Every 8x8 tile that changes between frames is an animated tile; frame 0 is the key drawn in the sheet. The sea and shallows under them are aethos's own animations.

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color
groups, one per secondary palette (`knossa_lib.GROUPS`), passed to Porytiles as packing
hints:

| Group | Use |
|---|---|
| minoan | Minoan red, ochre, gypsum, black and terracotta (labyrinth_art's): red columns, black capitals, horns of consecration, labrys marks, pithoi, the houses, the hives |
| stone | Cretan limestone on aethos grass: cliffs, terrace and town walls, the goat path |
| foam | Kythera's surf, foam lace, wet rock and quay edges |
| green | Vines and grapes, holm oak, phrygana and thyme, on aethos grass |
| bronze | Bronze and verdigris (Talos's foot, the Kouretes' shields, door fittings), and the marble herm |
| terra | Kythera's timber and terracotta: boats, the triremes, nets, trellis posts |

**Tile budget.** 421 of 504 tiles (280 metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.

**Scripted swaps.** The build writes the ids scripts swap to the `gTileset_BullRoad` block at the end of `include/constants/metatile_labels.h`: `METATILE_BullRoad_VaultDoor_TL`, `METATILE_BullRoad_VaultDoor_T`, `METATILE_BullRoad_VaultDoor_TR`, `METATILE_BullRoad_VaultDoor_BL`, `METATILE_BullRoad_VaultDoor_B`, `METATILE_BullRoad_VaultDoor_BR`, `METATILE_BullRoad_VaultOpen_TL`, `METATILE_BullRoad_VaultOpen_T`, `METATILE_BullRoad_VaultOpen_TR`, `METATILE_BullRoad_VaultOpen_BL`, `METATILE_BullRoad_VaultOpen_B`, `METATILE_BullRoad_VaultOpen_BR`, `METATILE_BullRoad_IdaGate_Top`, `METATILE_BullRoad_IdaGate`, `METATILE_BullRoad_IdaGate_OpenTop`, `METATILE_BullRoad_IdaGate_Open`, `METATILE_BullRoad_FossilLedge_L`, `METATILE_BullRoad_FossilLedge_R`, `METATILE_BullRoad_FossilLedge_Gone_L`, `METATILE_BullRoad_FossilLedge_Gone_R`.

## The Bull Road

### Low limestone cliffs

`cliff`, 8 wide by 3 tall. Crete's grey-gold limestone, Kythera's cliff kit in Knossa's stone. A cliff whose face looks south is `lip` (the plateau's edge, on borrowed grass) over `face` over a foot: `foot_sea` (borrowed sea, foam breaking at the base, animated), `foot_sand` or `foot_grass` (walkable ground with fallen stones). `_L` / `_R` end a run. Stack `face` rows for a taller cliff. The plateau's other edges: `side_E` (plateau to the west, the drop to the east), `side_W`, `back` (plateau to the south, the drop to the north, the face hidden), `back_NW` / `back_NE`; `corner_in_E` / `_W` turn a south face into a side going north. `seep` is the face where a spring runs out. Lip and face cells are impassable.

```text
ids                                                  walk
0x200 0x201 0x202 0x203 0x204 0x205 0x206 0x207   X X X X X X X X
0x208 0x209 0x20A 0x20B 0x20C 0x20D 0x20E 0x20F   X X X X X X X .
0x210 0x211 0x212 0x213 0x214 0x215 0x216 0x217   X X X X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x200 | `lip_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x201 | `lip` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x202 | `lip_b` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x203 | `lip_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x204 | `face_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x205 | `face` | `X` | `MB_NORMAL` | COVERED |  |
| 0x206 | `face_b` | `X` | `MB_NORMAL` | COVERED |  |
| 0x207 | `face_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x208 | `side_E` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x209 | `side_W` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x20A | `back` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x20B | `back_NW` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x20C | `back_NE` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x20D | `corner_in_E` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x20E | `corner_in_W` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x20F | `foot_grass` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x210 | `seep` | `X` | `MB_NORMAL` | COVERED |  |
| 0x211 | (1, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x212 | (2, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x213 | (3, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x214 | (4, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x215 | (5, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x216 | (6, 2) | `X` | `MB_NORMAL` | COVERED |  |
| 0x217 | (7, 2) | `X` | `MB_NORMAL` | COVERED |  |

### Limestone terrace walls

`terrace`, 7 wide by 2 tall. A dry-stone retaining wall one cell high, Kythera's terrace kit in Cretan limestone. Lay a `top_*` row (the upper terrace's edge, walkable, on borrowed grass) above a wall row: `L` `M` (`M2`) `R`. `steps` cuts a stair through the wall (walkable) under `top_steps`. `niche` is an arched niche with a low plinth (a votive's); `spout` is a spring spout dribbling into a trough. Wall cells are impassable.

```text
ids                                            walk
0x218 0x219 0x21A 0x21B 0x21C 0x21D 0x21E   X X X X . X X
0x220 0x221 0x222 0x223 0x224 0x225 0x226   . . . . T . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x218 | `L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x219 | `M` | `X` | `MB_NORMAL` | COVERED |  |
| 0x21A | `M2` | `X` | `MB_NORMAL` | COVERED |  |
| 0x21B | `R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x21C | `steps` | `.` | `MB_NORMAL` | COVERED |  |
| 0x21D | `niche` | `X` | `MB_NORMAL` | COVERED |  |
| 0x21E | `spout` | `X` | `MB_NORMAL` | COVERED |  |
| 0x220 | `top_L` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x221 | `top` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x222 | `top_M2` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x223 | `top_R` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x224 | `top_steps` | `T` | `MB_NORMAL` | COVERED | grass |
| 0x225 | `top_niche` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x226 | `top_spout` | `.` | `MB_NORMAL` | COVERED | grass |

### Terrace brows: ledges down to the north

`brow`, 5 wide by 1 tall. The Bull Road's terraces step down northward, so the trip back to Amnisos is quick (LABYRINTH §2; MAP_DESIGN §1): from the road you see only each terrace's coping, the drop beyond it to the north. `L` `M` (`M2`) `R` are ledges you hop down northward (`MB_JUMP_NORTH`, walk code `^`); `stair` is a flight of rough steps through the brow, the way back up (walkable). On borrowed grass.

```text
ids                                walk
0x228 0x229 0x22A 0x22B 0x22C   ^ ^ ^ ^ .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x228 | `L` | `^` | `MB_JUMP_NORTH` | COVERED | grass |
| 0x229 | `M` | `^` | `MB_JUMP_NORTH` | COVERED | grass |
| 0x22A | `M2` | `^` | `MB_JUMP_NORTH` | COVERED | grass |
| 0x22B | `R` | `^` | `MB_JUMP_NORTH` | COVERED | grass |
| 0x22C | `stair` | `.` | `MB_NORMAL` | COVERED | grass |

### The labrys door in the east cliff

`labrys_door`, 6 wide by 2 tall. The Bull Road vault's door (LABYRINTH §2's relic gate), set in a two-row stretch of the east cliff's face (stack two `cliff.face` rows either side, a `cliff.lip` row above): a gypsum doorway under horns of consecration, red-painted jambs, and a door with no handle, only a hollow the shape of a double axe. Closed: `top_L` `top` `top_R` over `foot_L` `door` `foot_R` (impassable; the bg event is on `door`). **Opened with the Labrys** after Ring III: swap all six cells to `open_*`, the slab gone and a stair going down into the dark; `open_door` is `MB_NON_ANIMATED_DOOR`, the warp to `MAP_KNOSSA_BULL_ROAD_VAULT`.

```text
ids                                      walk
0x230 0x231 0x232 0x233 0x234 0x235   X X X X X X
0x238 0x239 0x23A 0x23B 0x23C 0x23D   X X X X D X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x230 | `top_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x231 | `top` | `X` | `MB_NORMAL` | COVERED |  |
| 0x232 | `top_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x233 | `open_top_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x234 | `open_top` | `X` | `MB_NORMAL` | COVERED |  |
| 0x235 | `open_top_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x238 | `foot_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x239 | `door` | `X` | `MB_NORMAL` | COVERED |  |
| 0x23A | `foot_R` | `X` | `MB_NORMAL` | COVERED |  |
| 0x23B | `open_foot_L` | `X` | `MB_NORMAL` | COVERED |  |
| 0x23C | `open_door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x23D | `open_foot_R` | `X` | `MB_NORMAL` | COVERED |  |

### Mount Ida's labrys-sealed gate

`ida_gate`, 4 wide by 2 tall. The gate to the Ida path on the Bull Road's south-west (SCRIPT.md Part 2): two square limestone pillars, each cut with a double axe, and between them a timber gate bound shut, a fat clay seal stamped with a labrys over the lock. Set it in a terrace or field wall: `pillar_L_top` `gate_top` `pillar_R_top` (drawn over the player) over `pillar_L` `gate` `pillar_R` (impassable; bg event on `gate`: the seal). **Opened with the Labrys** after Ring III (`FLAG_ICHOR_IDA_GATE`): swap `gate_top` and `gate` to `open_top` and `open`, the path running through (walkable). All on borrowed grass.

```text
ids                          walk
0x240 0x241 0x242 0x243   T T T T
0x248 0x249 0x24A 0x24B   X X X .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x240 | `pillar_L_top` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x241 | `gate_top` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x242 | `pillar_R_top` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x243 | `open_top` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x248 | `pillar_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x249 | `gate` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x24A | `pillar_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x24B | `open` | `.` | `MB_NORMAL` | COVERED | grass |

### The beekeeper's hut, over its spring

`mitato`, 4 wide by 3 tall. Bombylia's hut, the Bull Road's rest point (SCRIPT.md Part 2): a Cretan mitato, a round hut of dry stone corbelled into a dome, built over a spring. 3 x 3: the dome's crown (`top_*`, drawn over the player, who walks behind it) over its walls over `foot_L` `door` `foot_R`. `door` is `MB_NON_ANIMATED_DOOR` (the warp to `MAP_KNOSSA_BULL_ROAD_HUT`); the spring's overflow runs out under it: lay `runnel` (walkable, a stone channel of water) south of the door, as many cells as you like. `hives` (clay tubes on a slab) and `skeps` stand in the yard, bees about them (impassable). All on borrowed grass but the door.

```text
ids                          walk
0x244 0x245 0x246 0x247   T T T X
0x24C 0x24D 0x24E 0x24F   X X X X
0x254 0x255 0x256 0x257   X D X .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x244 | `top_L` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x245 | `top` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x246 | `top_R` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x247 | `hives` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x24C | `wall_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x24D | `lintel` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x24E | `wall_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x24F | `skeps` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x254 | `foot_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x255 | `door` | `D` | `MB_NON_ANIMATED_DOOR` | COVERED |  |
| 0x256 | `foot_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x257 | `runnel` | `.` | `MB_NORMAL` | COVERED | grass |

### The great herm and the harbor shrine

`herm`, 1 wide by 2 tall. The great herm at the Bull Road's fork (SYSTEMS §4), which doubles as the sign, "East: the Bronze Heel. South: the palace.": a tall marble pillar with Hermes's bearded head on a plinth carved with the roads, Kythera's great herm (on borrowed grass). `herm` (drawn over the player) over `herm_base` (impassable; bg event here). A hidden item waits behind it.

```text
ids        walk
0x21F   T
0x227   X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x21F | `herm` | `T` | `MB_NORMAL` | SPLIT | grass |
| 0x227 | `herm_base` | `X` | `MB_NORMAL` | COVERED | grass |

### Phrygana: thyme, sage, spiny burnet, asphodel

`phrygana`, 5 wide by 1 tall. Crete's low scrub on borrowed grass, between the terraces and on the Bronze Heel's slope, where the bees work. Walkable: `thyme` and `thyme_b` (flowering cushions), `asphodel` (white spikes). Impassable: `sage` (Jerusalem sage, grey leaves), `burnet` (a spiny cushion).

```text
ids                                walk
0x258 0x259 0x25A 0x25B 0x25C   . X X . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x258 | `thyme` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x259 | `sage` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x25A | `burnet` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x25B | `asphodel` | `.` | `MB_NORMAL` | COVERED | grass |
| 0x25C | `thyme_b` | `.` | `MB_NORMAL` | COVERED | grass |

## The vineyard

### The vineyard: trellised rows and low vines

`vines`, 6 wide by 3 tall. The vines of the house of Minos (SCRIPT.md Part 2, the vineyard terraces), all on borrowed grass. **Trellised rows**, impassable, running west to east: `row_L` `row` (`row_grapes`, `row_post` to vary it) `row_R`. **Low vines**, the vineyard's tall grass (`MB_TALL_GRASS`; its own encounter table, so it must look unlike the road's barley): a soft-edged patch, `NW` `N` `NE` / `W` `C` `E` / `SW` `S` `SE`, with `C_b` and `C_grapes` to break up the middle and `C_dig` for the vineyard's lowest-terrace sherd (turned earth among the vines). Lay rows and low vines in alternating bands across a terrace. `sign` is the old vintner's sign (impassable; bg event): "Vines of the house of Minos."

```text
ids                                      walk
0x2B0 0x2B1 0x2B2 0x2B3 0x2B4 0x2B5   X X X X X X
0x2B8 0x2B9 0x2BA 0x2BB 0x2BC 0x2BD   G G G G G G
0x2C0 0x2C1 0x2C2 0x2C3 0x2C4 0x2C5   G G G G G G
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2B0 | `row_L` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B1 | `row` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B2 | `row_grapes` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B3 | `row_post` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B4 | `row_R` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B5 | `sign` | `X` | `MB_NORMAL` | COVERED | grass |
| 0x2B8 | `NW` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2B9 | `N` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2BA | `NE` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2BB | `C_b` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2BC | `W` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2BD | `C` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2C0 | `E` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2C1 | `C_grapes` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2C2 | `SW` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2C3 | `S` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2C4 | `SE` | `G` | `MB_TALL_GRASS` | COVERED | grass |
| 0x2C5 | `C_dig` | `G` | `MB_TALL_GRASS` | COVERED | grass |

## The Bronze Heel

### Talos's bronze foot

`talos_foot`, 5 wide by 4 tall. A bronze foot taller than a house, on the Bronze Heel's beach (SCRIPT.md Part 2): broken at the ankle, the hollow inside dark; verdigris over everything but the toes, rubbed bright; a great bronze nail hammered into the vein at the heel (`nail`). Place it whole, on borrowed sand. The top row is drawn over the player, who can walk behind the ankle; the rest is impassable. The foot is the bg event (`heel` or `nail`); the Big Pearl's sealed jar stands on the ankle's break, and Glauke does handstands by the `toes`.

```text
ids                                walk
0x2D0 0x2D1 0x2D2 0x2D3 0x2D4   T T T T T
0x2D8 0x2D9 0x2DA 0x2DB 0x2DC   X X X X X
0x2E0 0x2E1 0x2E2 0x2E3 0x2E4   X X X X X
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC   X X X X X
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2D0 | (0, 0) | `T` | `MB_NORMAL` | SPLIT | sand |
| 0x2D1 | `ankle` | `T` | `MB_NORMAL` | SPLIT | sand |
| 0x2D2 | (2, 0) | `T` | `MB_NORMAL` | SPLIT | sand |
| 0x2D3 | (3, 0) | `T` | `MB_NORMAL` | COVERED | sand |
| 0x2D4 | (4, 0) | `T` | `MB_NORMAL` | COVERED | sand |
| 0x2D8 | (0, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2D9 | (1, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2DA | (2, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2DB | (3, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2DC | (4, 1) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2E0 | `nail` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2E1 | (1, 2) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2E2 | (2, 2) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2E3 | (3, 2) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2E4 | `toe` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2E8 | `heel` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2E9 | (1, 3) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2EA | (2, 3) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2EB | (3, 3) | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2EC | `toes` | `X` | `MB_NORMAL` | COVERED | sand |

### Tide pools, and the fossil ledge

`tide_pools`, 4 wide by 2 tall. On borrowed sand by the water. Tide pools in wet rock: `pool` and `pool_b` (an anemone, a crab; impassable), `urchins` (black urchins in a shallow pool; impassable), `pool_dig` (a pool's sandy edge stirred up: the daily dig spot, walkable). **The fossil ledge** by the tide line (SCRIPT.md Part 6, the fixed dig): `ledge_skull` `ledge_dart`, a low shelf of soft rock with a great one-eyed skull and a stone dart showing in it (impassable; the dig's bg events). When the player chooses one, it crumbles into the sea: swap both cells to `ledge_gone_L` `ledge_gone_R` (rubble and wet sand, walkable). `FLAG_ICHOR_FOSSIL_DUG`.

```text
ids                          walk
0x2F0 0x2F1 0x2F2 0x2F3   X X . X
0x2F8 0x2F9 0x2FA 0x2FB   X X . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2F0 | `pool` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2F1 | `pool_b` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2F2 | `pool_dig` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x2F3 | `urchins` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2F8 | `ledge_skull` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2F9 | `ledge_dart` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x2FA | `ledge_gone_L` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x2FB | `ledge_gone_R` | `.` | `MB_NORMAL` | COVERED | sand |

### Foam-edged surf

`surf`, 8 wide by 2 tall. Where the Bronze Heel's sand meets the sea. Each cell borrows aethos's animated sea and draws the sand to the waterline, a rim of turquoise shallows and the foam, which washes up and back (the `surf` animation, 3 frames). Pieces are named by where the sea is: `S` (sand north, sea south; `S2` is the same with a deeper bite, to break up a long beach), `N`, `E`, `W`; `out_NW` is the south-east tip of a sand spit (sand to the north-west, sea round it), and so on; `in_SE` is a cove's corner, sea only to the south-east. The sand above meets aethos sand (0x124) exactly; the sea below meets aethos sea (0x170). Every cell is `MB_OCEAN_WATER`, like aethos's own beach edges: surf onto it, walk on the sand beside it.

```text
ids                                                  walk
0x300 0x301 0x302 0x303 0x304 0x305 0x306 0x307   W W W W W W W W
0x308 0x309 0x30A 0x30B 0x30C 0x30D 0x30E 0x30F   W W W W W W W W
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x300 | `S` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x301 | `S2` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x302 | `N` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x303 | `E` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x304 | `W` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x305 | `out_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x306 | `out_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x307 | `out_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x308 | `out_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x309 | `in_SE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x30A | `in_SW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x30B | `in_NE` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x30C | `in_NW` | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x30D | (5, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x30E | (6, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |
| 0x30F | (7, 1) | `W` | `MB_OCEAN_WATER` | COVERED | sea |

### White sand: foam lace, shells and wrack

`sand_decor`, 4 wide by 1 tall. On borrowed sand, walkable: `lace` (dried foam), `shells`, `wrack`, `footprints`.

```text
ids                          walk
0x2F4 0x2F5 0x2F6 0x2F7   . . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x2F4 | `lace` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x2F5 | `shells` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x2F6 | `wrack` | `.` | `MB_NORMAL` | COVERED | sand |
| 0x2F7 | `footprints` | `.` | `MB_NORMAL` | COVERED | sand |

### Tide rocks, a reef spit, white rocks, sea marks

`rocks`, 7 wide by 1 tall. Kythera's tide rocks: `tide_rock` and `tide_rocks` in the sea (foam round them, animated), `rock_sand` and `rocks_sand` on the beach, and the reef spit, `spit_head` `spit_M` `spit_V`: the Bronze Heel's rocky peninsula out to its tip (walkable; the Metal Coat hides at the tip).

```text
ids                                            walk
0x310 0x311 0x312 0x313 0x314 0x315 0x316   X X X X . . .
```

| Id | Piece | Walk | Behavior | Layer | Ground |
|---|---|---|---|---|---|
| 0x310 | `tide_rock` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x311 | `tide_rocks` | `X` | `MB_NORMAL` | COVERED | sea |
| 0x312 | `rock_sand` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x313 | `rocks_sand` | `X` | `MB_NORMAL` | COVERED | sand |
| 0x314 | `spit_head` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x315 | `spit_M` | `.` | `MB_NORMAL` | COVERED | sea |
| 0x316 | `spit_V` | `.` | `MB_NORMAL` | COVERED | sea |
