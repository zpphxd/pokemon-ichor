# Civic: the Greek public halls tileset

`gTileset_Civic` is the secondary tileset for Aethos's public interiors: the **Asclepeion** (the healing hall that replaces the Pokémon Center), the **Agora** (the shop) and the **Akademia** (Professor Daphne's grove hall). The slice rooms built from it are described in `ROOMS_civic.md`.

- **Art source:** `tools/ichor/art/civic_art.py`. Every piece is a hand-drawn character grid, one character per pixel, with a legend at the top of the file.
- **Builder:** `tools/ichor/art/civic_tiles.py` cuts the art into metatiles, writes the Porytiles sources, compiles them and checks the result.
- **Rooms:** `tools/ichor/art/civic_rooms.py` lays out the three slice rooms and renders them.
- **Rebuild everything:**
  ```bash
  /usr/bin/python3 tools/ichor/art/civic_tiles.py    # sources, compile, verify, sheet
  /usr/bin/python3 tools/ichor/art/civic_rooms.py    # room .bin files and renders
  ```
- **Metatile table:** `civic_tiles.py --catalog` prints the table at the end of this file.
- **Sheet:** `img/civic_sheet.png` shows every metatile over aethos at 2×, numbered.

## It works on any primary

Civic is drawn for the interior primary, `oikos`, which is still being drawn. Today it renders the same over `building` or `aethos`. Porytiles can only compile a secondary against a primary it manages, so civic is paired with aethos in `porytiles/tilesets/gTileset_Civic/config.yaml`. Civic never borrows from that primary:

- **Its own tiles.** Every metatile uses civic's tiles, or tile 0, which is transparent in every primary.
- **Its own palettes.** Every metatile uses palettes 6–12 only.
- **No shared colors.** No civic color equals an aethos color. Porytiles will put a secondary tile in a primary palette whenever its colors fit there, and it will reuse a flat primary tile for a flat civic one. That is why the void tile carries a few flecks.
- **Opaque floors.** Bottom layers are fully opaque, so the primary's backdrop color never shows.

`civic_tiles.py` checks all four on every build and fails if any is broken. `civic_rooms.py` renders each room over `aethos` and over `building` and fails unless the two renders are identical.

`--no-verify-checksums` is passed to Porytiles because aethos's checksum cache predates its last repaint. Recompiling aethos to refresh the cache is aethos's owner's call, not civic's.

## Palettes

Every 8×8 tile takes all its colors from one of seven planned palettes, listed in `PALETTES` in `civic_tiles.py`. The plan goes to Porytiles as palette hints, and the compile takes under a second. Without the plan, Porytiles' packer ran for minutes.

| Palette | Colors used for |
|---|---|
| marble | The Asclepeion's walls, counter, columns, statue, relief, stairs and mosaic. The Akademia's stylobate and long table. |
| spring | The spring basin, the stone couches, the specimen jars, the map of Aethos, and the blue cloth |
| clay | The pithoi, jars, amphorae, kraters, votives and mats |
| wood | The Agora's timber, plaster and stall. The Akademia's walls, floor, scrolls and desks. |
| bronze | The braziers, the balance scale, the coins and the armillary sphere |
| grove | Grass, the laurel, the cypress hedge, the herbs and the serpent |
| dyes | The purple and saffron cloth, and the baskets of goods |

All colors are multiples of 8, in the families of the master palette in `PLAN.md`.

**Shifted values.** Many values sit one step off the master palette, for example white marble `248 248 248` against `248 248 240`. This keeps them distinct from aethos, as explained above. The difference doesn't show.

## Budget

| Resource | Used | Limit |
|---|---|---|
| Tiles | 504 | 512 |
| Metatiles | 206 | 512 |
| Palettes | 7 | 7, slots 6–12 |

**Tiles are the tight resource.** To spend them carefully:
- Reuse a piece over a different floor. A column on the clay floor costs no new tiles.
- Use repeated rows and flipped cells.
- Add new pieces only after checking the count printed by the build.

## Conventions

- **Layers.**
  - Floors and walls fill the bottom layer.
  - Furniture goes on the middle layer, under sprites.
  - Things a walker passes behind go on the top layer: column capitals and shafts, the laurel's canopy, the flames of braziers and the armillary's sphere. The counter slab over a staff cell is also on the top layer.
  - Porytiles sets the layer type from the layers used.
- **Collision lives in the layout, not the tileset.** The `Solid` column below is the default `civic_rooms.py` applies:
  - collision 1 for solid cells
  - elevation 3 for walkable ones, as in Emerald's interiors.
- **Ids follow the order in `define()`.** The rooms refer to metatiles by name, so regenerate them after any change.
  - Once maps use these ids, add new metatiles at the end of `define()` so existing ids don't move.
- **Naming.**
  - `_sh` variants sit in the shadow under a back wall.
  - `_l` and `_r` are wall ends.
  - `prefix_X_Y` is the cell at column X, row Y of a multi-cell piece.
  - `_b` variants are the same object over the Asclepeion's cream slab.

## Behaviors

| Behavior | Metatiles | Effect |
|---|---|---|
| `MB_COUNTER` | `*_counter_front_*` | Talk across the counter to the NPC behind it |
| `MB_PC` | `asc_pithos_0_2`, `asc_pithos_1_2` | Opens storage, like the Pokémon Center PC |
| `MB_NON_ANIMATED_DOOR` | `asc_stairs_0_2`, `asc_stairs_1_2` | Warps when walked onto, as house stairs do |
| `MB_SOUTH_ARROW_WARP` | `asc_mat`, `asc_mat_b`, `ago_mat`, `aka_mat` | The exit mat |
| `MB_SHOP_SHELF` | `ago_shelf_0_2` | "The shelves brim with all sorts of POKéMON merchandise." |
| `MB_BOOKSHELF` | `aka_scrolls_*_2` | "It's filled with all sorts of books." Override with a BG event for the script's line. |
| `MB_VASE` | the bottom cell of every jar and amphora | "This vase looks expensive… But, it was empty." |

A BG event always takes priority over a metatile behavior, so scripted lines (the statue, the wall map, the bookshelf) can sit on any of these.

## Pieces

**Shared**
- **Doric column.** Capital, fluted shaft and plinth, 1×3.
- **Threshold mat.** Terracotta mosaic with a black key.
- **Marble bench.** Lion-paw feet, 2×1.
- **Bronze tripod brazier.** Lit, 1×2.
- **Void.** A near-black metatile for layout borders.

**Asclepeion**
- **Floor and walls.**
  - White and cream marble slabs, laid as a checker.
  - Ashlar walls with a blue running-wave frieze between gold fillets, over a blue dado.
- **The healer's counter.** An altar with a triglyph frieze: blue metopes and gold rosettes.
- **The sacred spring.** A bronze serpent spouts into a marble basin set where the healing machine stood (2×2).
- **The rod of Asclepius.** A painted relief above the healer.
- **Votive offerings.**
  - Clay tablets hung on the wall: a patient on a couch, an eye, a serpent.
  - Clay limbs on the counter: a leg, an arm, an eye plaque.
- **The Pithos corner.** A great storage jar with rope bands and a wax seal that glows, 2×3. Lidded jars stand beside it.
- **Asclepius.** The god in a blue-painted wall niche on an inscribed plinth.
- **Healing couches (klinai).** Stone, with linen and a blue blanket.
- **Floor mosaic.** A serpent rod in a terracotta ring, framed in blue (3×3).
- **One of the god's snakes,** loose on the floor.
- **Marble stairs.** They climb into a doorway in the back wall.

**Agora**
- **Floor and walls.**
  - Large pale fired-clay floor tiles.
  - A timber beam over limewashed plaster, with a red dado.
- **Dyed cloth.** Purple, Aegean blue and saffron, hung from rods under the beam.
- **Drying herbs and a garlic braid.**
- **Pottery shelves.** Oil flasks, an amphora and stamnoi.
- **Demeas's stall.**
  - A striped madder-and-cream awning on poles.
  - A wooden counter with a bronze balance scale, a loaf and an oil flask.
  - A striped cloth over the counter's front.
- **The money-changer's trapeza.** Coin stacks, loose coins and a purse.
- **Baskets.** Grain, green olives, figs and pomegranates.
- **Black-figure amphora** in a ring stand, plus the lidded jars.
- **Inner colonnade.** The Asclepeion's column on the clay floor.

**Akademia**
- **Floor and walls.**
  - Limestone flags.
  - Ashlar walls with a cream meander on a terracotta frieze.
- **The grove.**
  - A clipped cypress hedge.
  - Sun-bleached grass, with wildflowers.
  - A marble stylobate carrying the colonnade.
  - A laurel (Daphne's tree), its canopy drawn over walkers.
- **Daphne's long marble table.** Lion-paw legs, and three kraters on their own cells:
  - Snivy: a cream serpent on black (it grows into Delphoi's python).
  - Cyndaquil: flames.
  - Piplup: a white-ground krater with blue water and waves.
- **Wall pieces.**
  - A painted map of Aethos. Kalliste is the gold speck by the arrow.
  - A marble shelf of specimen jars: a shell, a starfish, a beetle.
  - Cabinets of scrolls in cubbyholes with red tags.
- **An armillary sphere** on a bronze tripod.
- **Writing desks.** Each has an unrolled scroll, ink, a reed pen and a wax tablet, with stools.
- **Alethea's dig finds.**
  - A worktable of potsherds, a brush and a trowel.
  - A crate of sherds.
  - A fallen marble head.
  - A pick.

**Emporion's Asclepeion** (Phase 2, laid out in `tools/ichor/maps/emporion_rooms.py`; see `design/phase2/ROOMS_emporion.md`). Added after every slice metatile, so the slice rooms' ids didn't move.
- **The sea window.** 4x2 in the back wall, behind the healer: the cornice runs on over it, three lights between marble mullions, the harbor beyond with a trireme under sail, a broad sill.
- **The bell-pull.** Ship's rope hung from a ring, knotted at its end, 1x2.
- **Votive anchors.** Two small bronze anchors on nails, hung by sailors who came home.

**Two colors moved one step** when the Emporion pieces were added: limestone `L` from `208 184 136` to `208 184 128`, and red `r` from `216 56 40` to `216 56 48`. aethos's repaint had taken both values, and `precheck()` won't compile civic while a legend color is an aethos color. The slice rooms' renders differ only by those two steps.

## Not done

- **Kalliste's green dot.** The script calls Kalliste "a tiny green dot" on the wall map. The map lives in the spring palette, which has no green, so the dot is gold. Moving the map to its own palette would cost a palette slot.
- **Room for growth.** Civic is full: 504 of 512 tiles after Emporion's Asclepeion. New public halls can reuse its pieces; new pieces need a second civic tileset.

## Metatile table

Generated by `civic_tiles.py --catalog`. `Layers` lists the Porytiles layers each metatile uses.

| Id | Name | Layers | Behavior | Solid |
|---|---|---|---|---|
| `0x200` | `void` | bottom |  | yes |
| `0x201` | `asc_floor_a` | bottom |  |  |
| `0x202` | `asc_floor_b` | bottom |  |  |
| `0x203` | `asc_floor_a_sh` | bottom |  |  |
| `0x204` | `asc_floor_b_sh` | bottom |  |  |
| `0x205` | `asc_wall_top` | bottom |  | yes |
| `0x206` | `asc_wall_top_l` | bottom |  | yes |
| `0x207` | `asc_wall_top_r` | bottom |  | yes |
| `0x208` | `asc_wall` | bottom |  | yes |
| `0x209` | `asc_wall_l` | bottom |  | yes |
| `0x20A` | `asc_wall_r` | bottom |  | yes |
| `0x20B` | `asc_column_0_0` | bottom+top |  |  |
| `0x20C` | `asc_column_0_1` | bottom+top |  |  |
| `0x20D` | `asc_column_0_2` | bottom+middle |  | yes |
| `0x20E` | `asc_counter_l` | bottom+middle |  | yes |
| `0x20F` | `asc_counter_m` | bottom+middle |  | yes |
| `0x210` | `asc_counter_r` | bottom+middle |  | yes |
| `0x211` | `asc_counter_staff` | bottom+top |  |  |
| `0x212` | `asc_counter_front_l` | bottom | `MB_COUNTER` | yes |
| `0x213` | `asc_counter_front_m` | bottom | `MB_COUNTER` | yes |
| `0x214` | `asc_counter_front_r` | bottom | `MB_COUNTER` | yes |
| `0x215` | `asc_basin_0_0` | bottom+middle |  | yes |
| `0x216` | `asc_basin_1_0` | bottom+middle |  | yes |
| `0x217` | `asc_basin_0_1` | bottom+middle |  | yes |
| `0x218` | `asc_basin_1_1` | bottom+middle |  | yes |
| `0x219` | `asc_relief_0_0` | bottom+middle |  | yes |
| `0x21A` | `asc_relief_0_1` | bottom+middle |  | yes |
| `0x21B` | `asc_votive_wall_0_0` | bottom+middle |  | yes |
| `0x21C` | `asc_votive_wall_1_0` | bottom+middle |  | yes |
| `0x21D` | `asc_votive_counter_0_0` | bottom+middle |  | yes |
| `0x21E` | `asc_votive_counter_1_0` | bottom+middle |  | yes |
| `0x21F` | `asc_pithos_0_0` | bottom+middle |  | yes |
| `0x220` | `asc_pithos_1_0` | bottom+middle |  | yes |
| `0x221` | `asc_pithos_0_1` | bottom+middle |  | yes |
| `0x222` | `asc_pithos_1_1` | bottom+middle |  | yes |
| `0x223` | `asc_pithos_0_2` | bottom+middle | `MB_PC` | yes |
| `0x224` | `asc_pithos_1_2` | bottom+middle | `MB_PC` | yes |
| `0x225` | `asc_jar_0_0` | bottom+middle |  | yes |
| `0x226` | `asc_jar_0_1` | bottom+middle | `MB_VASE` | yes |
| `0x227` | `asc_statue_0_0` | bottom+middle |  | yes |
| `0x228` | `asc_statue_0_1` | bottom+middle |  | yes |
| `0x229` | `asc_statue_0_2` | bottom+middle |  | yes |
| `0x22A` | `asc_stairs_0_0` | bottom |  | yes |
| `0x22B` | `asc_stairs_1_0` | bottom |  | yes |
| `0x22C` | `asc_stairs_0_1` | bottom |  | yes |
| `0x22D` | `asc_stairs_1_1` | bottom |  | yes |
| `0x22E` | `asc_stairs_0_2` | bottom+middle | `MB_NON_ANIMATED_DOOR` |  |
| `0x22F` | `asc_stairs_1_2` | bottom+middle | `MB_NON_ANIMATED_DOOR` |  |
| `0x230` | `asc_mosaic_0_0` | bottom |  |  |
| `0x231` | `asc_mosaic_1_0` | bottom |  |  |
| `0x232` | `asc_mosaic_2_0` | bottom |  |  |
| `0x233` | `asc_mosaic_0_1` | bottom |  |  |
| `0x234` | `asc_mosaic_1_1` | bottom |  |  |
| `0x235` | `asc_mosaic_2_1` | bottom |  |  |
| `0x236` | `asc_mosaic_0_2` | bottom |  |  |
| `0x237` | `asc_mosaic_1_2` | bottom |  |  |
| `0x238` | `asc_mosaic_2_2` | bottom |  |  |
| `0x239` | `asc_kline_0_0` | bottom+middle |  | yes |
| `0x23A` | `asc_kline_1_0` | bottom+middle |  | yes |
| `0x23B` | `asc_kline_0_1` | bottom+middle |  | yes |
| `0x23C` | `asc_kline_1_1` | bottom+middle |  | yes |
| `0x23D` | `asc_snake_0_0` | bottom+middle |  |  |
| `0x23E` | `asc_brazier_0_0` | bottom+top |  |  |
| `0x23F` | `asc_brazier_0_1` | bottom+middle |  | yes |
| `0x240` | `asc_bench_0_0` | bottom+middle |  | yes |
| `0x241` | `asc_bench_1_0` | bottom+middle |  | yes |
| `0x242` | `asc_mat` | bottom+middle | `MB_SOUTH_ARROW_WARP` |  |
| `0x243` | `asc_kline_b_0_0` | bottom+middle |  | yes |
| `0x244` | `asc_kline_b_1_0` | bottom+middle |  | yes |
| `0x245` | `asc_kline_b_0_1` | bottom+middle |  | yes |
| `0x246` | `asc_kline_b_1_1` | bottom+middle |  | yes |
| `0x247` | `asc_snake_b_0_0` | bottom+middle |  |  |
| `0x248` | `asc_brazier_b_0_0` | bottom+top |  |  |
| `0x249` | `asc_brazier_b_0_1` | bottom+middle |  | yes |
| `0x24A` | `asc_bench_b_0_0` | bottom+middle |  | yes |
| `0x24B` | `asc_bench_b_1_0` | bottom+middle |  | yes |
| `0x24C` | `asc_mat_b` | bottom+middle | `MB_SOUTH_ARROW_WARP` |  |
| `0x24D` | `asc_column_b_0_0` | bottom+top |  |  |
| `0x24E` | `asc_column_b_0_1` | bottom+top |  |  |
| `0x24F` | `asc_column_b_0_2` | bottom+middle |  | yes |
| `0x250` | `ago_floor` | bottom |  |  |
| `0x251` | `ago_floor_sh` | bottom |  |  |
| `0x252` | `ago_wall_top` | bottom |  | yes |
| `0x253` | `ago_wall_top_l` | bottom |  | yes |
| `0x254` | `ago_wall_top_r` | bottom |  | yes |
| `0x255` | `ago_wall` | bottom |  | yes |
| `0x256` | `ago_wall_l` | bottom |  | yes |
| `0x257` | `ago_wall_r` | bottom |  | yes |
| `0x258` | `ago_cloth_purple_0_0` | bottom+middle |  | yes |
| `0x259` | `ago_cloth_purple_0_1` | bottom+middle |  | yes |
| `0x25A` | `ago_cloth_blue_0_0` | bottom+middle |  | yes |
| `0x25B` | `ago_cloth_blue_0_1` | bottom+middle |  | yes |
| `0x25C` | `ago_cloth_saffron_0_0` | bottom+middle |  | yes |
| `0x25D` | `ago_cloth_saffron_0_1` | bottom+middle |  | yes |
| `0x25E` | `ago_herbs_0_0` | bottom+middle |  | yes |
| `0x25F` | `ago_herbs_0_1` | bottom+middle |  | yes |
| `0x260` | `ago_shelf_0_0` | bottom+middle |  | yes |
| `0x261` | `ago_shelf_0_1` | bottom |  | yes |
| `0x262` | `ago_shelf_0_2` | bottom | `MB_SHOP_SHELF` | yes |
| `0x263` | `ago_awning_0_0` | bottom+middle |  | yes |
| `0x264` | `ago_awning_1_0` | bottom+middle |  | yes |
| `0x265` | `ago_awning_2_0` | bottom+middle |  | yes |
| `0x266` | `ago_awning_0_1` | bottom+middle |  | yes |
| `0x267` | `ago_awning_1_1` | bottom+middle |  | yes |
| `0x268` | `ago_awning_2_1` | bottom+middle |  | yes |
| `0x269` | `ago_counter_l` | bottom+middle |  | yes |
| `0x26A` | `ago_counter_m` | bottom+middle |  | yes |
| `0x26B` | `ago_counter_staff` | bottom+top |  |  |
| `0x26C` | `ago_counter_r` | bottom+middle |  | yes |
| `0x26D` | `ago_counter_front_l` | bottom | `MB_COUNTER` | yes |
| `0x26E` | `ago_counter_front_m` | bottom | `MB_COUNTER` | yes |
| `0x26F` | `ago_counter_front_r` | bottom | `MB_COUNTER` | yes |
| `0x270` | `ago_column_0_0` | bottom+top |  |  |
| `0x271` | `ago_column_0_1` | bottom+top |  |  |
| `0x272` | `ago_column_0_2` | bottom+middle |  | yes |
| `0x273` | `ago_basket_grain` | bottom+middle |  | yes |
| `0x274` | `ago_basket_olives` | bottom+middle |  | yes |
| `0x275` | `ago_basket_figs` | bottom+middle |  | yes |
| `0x276` | `ago_basket_pomegranates` | bottom+middle |  | yes |
| `0x277` | `ago_trapeza_0_0` | bottom+middle |  | yes |
| `0x278` | `ago_trapeza_1_0` | bottom+middle |  | yes |
| `0x279` | `ago_trapeza_0_1` | bottom+middle |  | yes |
| `0x27A` | `ago_trapeza_1_1` | bottom+middle |  | yes |
| `0x27B` | `ago_amphora_0_0` | bottom+middle |  | yes |
| `0x27C` | `ago_amphora_0_1` | bottom+middle | `MB_VASE` | yes |
| `0x27D` | `ago_jar_0_0` | bottom+middle |  | yes |
| `0x27E` | `ago_jar_0_1` | bottom+middle | `MB_VASE` | yes |
| `0x27F` | `ago_mat` | bottom+middle | `MB_SOUTH_ARROW_WARP` |  |
| `0x280` | `aka_floor` | bottom |  |  |
| `0x281` | `aka_floor_b` | bottom |  |  |
| `0x282` | `aka_floor_sh` | bottom |  |  |
| `0x283` | `aka_floor_b_sh` | bottom |  |  |
| `0x284` | `aka_wall_top` | bottom |  | yes |
| `0x285` | `aka_wall_top_l` | bottom |  | yes |
| `0x286` | `aka_wall_top_r` | bottom |  | yes |
| `0x287` | `aka_wall` | bottom |  | yes |
| `0x288` | `aka_wall_l` | bottom |  | yes |
| `0x289` | `aka_wall_r` | bottom |  | yes |
| `0x28A` | `aka_hedge_top` | bottom |  | yes |
| `0x28B` | `aka_hedge` | bottom |  | yes |
| `0x28C` | `aka_grass` | bottom |  |  |
| `0x28D` | `aka_grass_flowers` | bottom |  |  |
| `0x28E` | `aka_grass_sh` | bottom |  |  |
| `0x28F` | `aka_stylobate` | bottom |  |  |
| `0x290` | `aka_stylobate_sh` | bottom |  |  |
| `0x291` | `aka_column_0_0` | bottom+top |  |  |
| `0x292` | `aka_column_0_1` | bottom+top |  |  |
| `0x293` | `aka_column_0_2` | bottom+middle |  | yes |
| `0x294` | `aka_column_cap_sh` | bottom+top |  |  |
| `0x295` | `aka_laurel_0_0` | bottom+top |  |  |
| `0x296` | `aka_laurel_1_0` | bottom+top |  |  |
| `0x297` | `aka_laurel_0_1` | bottom+top |  |  |
| `0x298` | `aka_laurel_1_1` | bottom+top |  |  |
| `0x299` | `aka_laurel_0_2` | bottom+middle |  | yes |
| `0x29A` | `aka_laurel_1_2` | bottom+middle |  | yes |
| `0x29B` | `aka_bench_0_0` | bottom+middle |  | yes |
| `0x29C` | `aka_bench_1_0` | bottom+middle |  | yes |
| `0x29D` | `aka_map_0_0` | bottom+middle |  | yes |
| `0x29E` | `aka_map_1_0` | bottom+middle |  | yes |
| `0x29F` | `aka_map_0_1` | bottom+middle |  | yes |
| `0x2A0` | `aka_map_1_1` | bottom+middle |  | yes |
| `0x2A1` | `aka_specimens_0_0` | bottom+middle |  | yes |
| `0x2A2` | `aka_specimens_0_1` | bottom+middle |  | yes |
| `0x2A3` | `aka_scrolls_0_0` | bottom+middle |  | yes |
| `0x2A4` | `aka_scrolls_1_0` | bottom+middle |  | yes |
| `0x2A5` | `aka_scrolls_0_1` | bottom |  | yes |
| `0x2A6` | `aka_scrolls_1_1` | bottom |  | yes |
| `0x2A7` | `aka_scrolls_0_2` | bottom+middle | `MB_BOOKSHELF` | yes |
| `0x2A8` | `aka_scrolls_1_2` | bottom+middle | `MB_BOOKSHELF` | yes |
| `0x2A9` | `aka_table_l` | bottom+middle |  | yes |
| `0x2AA` | `aka_table_m` | bottom+middle |  | yes |
| `0x2AB` | `aka_table_r` | bottom+middle |  | yes |
| `0x2AC` | `aka_krater_snivy` | bottom+middle |  | yes |
| `0x2AD` | `aka_krater_cyndaquil` | bottom+middle |  | yes |
| `0x2AE` | `aka_krater_piplup` | bottom+middle |  | yes |
| `0x2AF` | `aka_table_front_0_0` | bottom+middle |  | yes |
| `0x2B0` | `aka_table_front_1_0` | bottom+middle |  | yes |
| `0x2B1` | `aka_table_front_2_0` | bottom+middle |  | yes |
| `0x2B2` | `aka_armillary_0_0` | bottom+top |  |  |
| `0x2B3` | `aka_armillary_0_1` | bottom+middle |  | yes |
| `0x2B4` | `aka_desk_0_0` | bottom+middle |  | yes |
| `0x2B5` | `aka_desk_1_0` | bottom+middle |  | yes |
| `0x2B6` | `aka_desk_0_1` | bottom+middle |  | yes |
| `0x2B7` | `aka_desk_1_1` | bottom+middle |  | yes |
| `0x2B8` | `aka_stool` | bottom+middle |  | yes |
| `0x2B9` | `aka_worktable_0_0` | bottom+middle |  | yes |
| `0x2BA` | `aka_worktable_1_0` | bottom+middle |  | yes |
| `0x2BB` | `aka_worktable_0_1` | bottom+middle |  | yes |
| `0x2BC` | `aka_worktable_1_1` | bottom+middle |  | yes |
| `0x2BD` | `aka_crate` | bottom+middle |  | yes |
| `0x2BE` | `aka_head` | bottom+middle |  | yes |
| `0x2BF` | `aka_tools` | bottom+middle |  | yes |
| `0x2C0` | `aka_amphora_0_0` | bottom+middle |  | yes |
| `0x2C1` | `aka_amphora_0_1` | bottom+middle | `MB_VASE` | yes |
| `0x2C2` | `aka_mat` | bottom+middle | `MB_SOUTH_ARROW_WARP` |  |
| `0x2C3` | `asc_sea_window_0_0` | bottom |  | yes |
| `0x2C4` | `asc_sea_window_1_0` | bottom |  | yes |
| `0x2C5` | `asc_sea_window_2_0` | bottom |  | yes |
| `0x2C6` | `asc_sea_window_3_0` | bottom |  | yes |
| `0x2C7` | `asc_sea_window_0_1` | bottom |  | yes |
| `0x2C8` | `asc_sea_window_1_1` | bottom |  | yes |
| `0x2C9` | `asc_sea_window_2_1` | bottom |  | yes |
| `0x2CA` | `asc_sea_window_3_1` | bottom |  | yes |
| `0x2CB` | `asc_bell_rope_0_0` | bottom+middle |  | yes |
| `0x2CC` | `asc_bell_rope_0_1` | bottom+middle |  | yes |
| `0x2CD` | `asc_anchors_0_0` | bottom+middle |  | yes |
