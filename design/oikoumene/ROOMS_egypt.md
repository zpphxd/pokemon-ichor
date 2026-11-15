# Egypt's rooms: Naukratis and Memphis, on per

Twelve interiors for the Oikoumene's Egyptian towns (design/oikoumene/BUILD.md §5), laid out in `tools/ichor/maps/egypt_rooms.py` from a new secondary tileset, `gTileset_Per` (Egyptian *pr*, "house"), on the oikos primary. Who lives in each room comes from `design/OIKOUMENE.md` §4.5 and §8.

Build everything (the tileset, the layouts, the map.json events) with:

```
/usr/bin/python3 tools/ichor/maps/egypt_rooms.py
```

The play check is `tools/ichor/tests/egypt_rooms.sh`.

<!-- egypt: begin overview -->
<!-- egypt: end overview -->

## Render-and-critique passes

<!-- egypt: begin passes -->
<!-- egypt: end passes -->

## Generated tables

The builder rewrites everything below this line.

<!-- per_build: begin generated -->

### The Asclepeion, Naukratis

- Map: `MAP_NAUKRATIS_ASCLEPEION`. Layout: `data/layouts/Naukratis_Asclepeion/map.bin`, **13x9** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: flags. Wall: plaster. Render: `design/oikoumene/img/egypt_naukratis_asclepeion.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789012
  0 #############
  1 #9##########8
  2 ...###2##.67.
  3 ...######....
  4 ##...........
  5 .........###.
  6 ##3.......5.4
  7 ..#.#....#...
  8 ..#.#.11.#..#
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (6,8), (7,8) |  | door mat back to MAP_NAUKRATIS (warp 0) |
| 2 | npc | (6,2) | (6,4) facing north, across the counter | the healer |
| 3 | npc | (2,6) | faces west | a Samian sailor by the beds, his hand bound up |
| 4 | npc | (12,6) | faces west | an Egyptian woman, waiting with her Espurr |
| 5 | npc | (10,6) | faces east | her Espurr, Miu |
| 6 | bg | (10,2) | (10,3) facing north | the Pithos |
| 7 | bg | (11,2) | (11,3) facing north | the Pithos |
| 8 | bg | (12,1) | (12,2) facing north | the ear stele |
| 9 | bg | (1,1) | (1,2) facing north | the window on the harbor |

### The Agora, Naukratis

- Map: `MAP_NAUKRATIS_AGORA`. Layout: `data/layouts/Naukratis_Agora/map.bin`, **12x8** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: earth. Wall: plaster. Render: `design/oikoumene/img/egypt_naukratis_agora.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678901
  0 ############
  1 ############
  2 #5####2#..##
  3 ....####....
  4 #.........##
  5 ##3......4.#
  6 ##..........
  7 .....11....#
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,7), (6,7) |  | door mat back to MAP_NAUKRATIS (warp 1) |
| 2 | npc | (6,2) | (6,4) facing north, across the counter | Charaxos, the stallkeeper |
| 3 | npc | (2,5) | faces west | a Chian wine trader, by the amphorae |
| 4 | npc | (9,5) | faces east | a porter by the grain sacks |
| 5 | bg | (1,2) | (1,3) facing north | the amphora rack |

### Daphne's field station, Naukratis

- Map: `MAP_NAUKRATIS_FIELD_STATION`. Layout: `data/layouts/Naukratis_FieldStation/map.bin`, **11x8** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: earth. Wall: plaster. Render: `design/oikoumene/img/egypt_naukratis_field_station.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    01234567890
  0 ###########
  1 ###########
  2 #4#.#...#5#
  3 ..#.......#
  4 ....3#2....
  5 #......##.#
  6 #..........
  7 .....11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,7), (6,7) |  | door mat back to MAP_NAUKRATIS (warp 2) |
| 2 | npc | (6,4) | faces south | Daphne, by her silt trough |
| 3 | bg | (4,4) | (4,5) facing north | the silt trough |
| 4 | bg | (1,2) | (1,3) facing north | her notes, and the chart over them |
| 5 | bg | (9,2) | (9,3) facing north | the fossil crates |

### The egg-ovens, Naukratis

- Map: `MAP_NAUKRATIS_EGG_OVENS`. Layout: `data/layouts/Naukratis_EggOvens/map.bin`, **13x9** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: earth. Wall: brick. Render: `design/oikoumene/img/egypt_naukratis_egg_ovens.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789012
  0 #############
  1 #############
  2 ####4#####5##
  3 .............
  4 ..2....#....#
  5 .#..#.#...3.#
  6 .............
  7 #..........#.
  8 ......11.....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (6,8), (7,8) |  | door mat back to MAP_NAUKRATIS (warp 3) |
| 2 | npc | (2,4) | faces east | Neferu, the oven-keeper, turning eggs |
| 3 | npc | (10,5) | faces west | Tiy, who takes in the Pokémon |
| 4 | bg | (4,2) | (4,3) facing north | an oven |
| 5 | bg | (10,2) | (10,3) facing north | an oven |

### The incense merchant's, Naukratis

- Map: `MAP_NAUKRATIS_INCENSE_SHOP`. Layout: `data/layouts/Naukratis_IncenseShop/map.bin`, **10x8** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: earth. Wall: plaster. Render: `design/oikoumene/img/egypt_naukratis_incense_shop.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789
  0 ##########
  1 ##########
  2 #4##.2##5#
  3 ....##....
  4 .3.......#
  5 #........#
  6 ..........
  7 ....11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (4,7), (5,7) |  | door mat back to MAP_NAUKRATIS (warp 4) |
| 2 | npc | (5,2) | (5,4) facing north, across the counter | Yada'il, the incense merchant from Saba |
| 3 | npc | (1,4) | faces east | a Greek widow buying for a funeral |
| 4 | bg | (1,2) | (1,3) facing north | the frankincense |
| 5 | bg | (8,2) | (8,3) facing north | the myrrh |

### The potter's house, Naukratis

- Map: `MAP_NAUKRATIS_POTTERS_HOUSE`. Layout: `data/layouts/Naukratis_PottersHouse/map.bin`, **11x8** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: earth. Wall: brick. Render: `design/oikoumene/img/egypt_naukratis_potters_house.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    01234567890
  0 ###########
  1 ###########
  2 #5###...#6#
  3 ...3...#...
  4 #....#2....
  5 #...#....##
  6 ...........
  7 .....11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,7), (6,7) |  | door mat back to MAP_NAUKRATIS (warp 5) |
| 2 | npc | (6,4) | faces west | Lykos the potter, at his wheel |
| 3 | npc | (3,3) | faces south | Lykos's Kecleon, among the drying pots |
| 4 | npc | (3,3) | faces north | the Smeargle, painting, after the trade |
| 5 | bg | (1,2) | (1,3) facing north | the pot shelf |
| 6 | bg | (9,2) | (9,3) facing north | the kiln |

### The net-loft, Naukratis

- Map: `MAP_NAUKRATIS_NET_LOFT`. Layout: `data/layouts/Naukratis_NetLoft/map.bin`, **12x8** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: mat. Wall: brick. Render: `design/oikoumene/img/egypt_naukratis_net_loft.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678901
  0 ############
  1 ############
  2 ##.###...##.
  3 ...........#
  4 ...#4.....2#
  5 #..##3......
  6 .#......5#..
  7 .....11.....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,7), (6,7) |  | door mat back to MAP_NAUKRATIS (warp 6) |
| 2 | npc | (10,4) | faces west | Ipy the fisher, mending a net |
| 3 | npc | (5,5) | faces west | Merit, at her loom |
| 4 | bg | (4,4) | (4,3) facing south | the ground loom |
| 5 | bg | (8,6) | (8,5) facing south | the papyrus skiff |

### The Asclepeion, Memphis

- Map: `MAP_MEMPHIS_ASCLEPEION`. Layout: `data/layouts/Memphis_Asclepeion/map.bin`, **15x10** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: flags. Wall: temple. Render: `design/oikoumene/img/egypt_memphis_asclepeion.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678901234
  0 ###############
  1 ##############9
  2 .#8####2###.67.
  3 ..4.######.....
  4 ...............
  5 ##.#.......#.##
  6 ...#..3....#...
  7 #..#.......#..#
  8 ##..........5##
  9 .......11......
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (7,9), (8,9) |  | door mat back to MAP_MEMPHIS (warp 0) |
| 2 | npc | (7,2) | (7,4) facing north, across the counter | the healer |
| 3 | npc | (6,6) | faces south | a lector-priestess of Imhotep, on the mat |
| 4 | npc | (2,3) | faces north | a scribe, praying to his patron |
| 5 | npc | (12,8) | faces west | a boy with a scorpion sting, by his bed |
| 6 | bg | (12,2) | (12,3) facing north | the Pithos |
| 7 | bg | (13,2) | (13,3) facing north | the Pithos |
| 8 | bg | (2,2) | (2,3) facing north | the statue of Imhotep |
| 9 | bg | (14,1) | (14,2) facing north | the ear stele |

### The Agora, Memphis

- Map: `MAP_MEMPHIS_AGORA`. Layout: `data/layouts/Memphis_Agora/map.bin`, **12x8** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: mat. Wall: plaster. Render: `design/oikoumene/img/egypt_memphis_agora.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678901
  0 ############
  1 ############
  2 ##..##2#..##
  3 ....####....
  4 #...........
  5 #4........##
  6 ..........35
  7 #....11.....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,7), (6,7) |  | door mat back to MAP_MEMPHIS (warp 1) |
| 2 | npc | (6,2) | (6,4) facing north, across the counter | Senbi, the stallkeeper |
| 3 | npc | (10,6) | faces west | the linen-seller |
| 4 | npc | (1,5) | faces west | a girl eyeing the dates |
| 5 | bg | (11,6) | (11,7) facing north | the amulet tray |

### The Apis keepers', Memphis

- Map: `MAP_MEMPHIS_APIS_STABLE`. Layout: `data/layouts/Memphis_ApisStable/map.bin`, **16x10** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: earth. Wall: temple. Render: `design/oikoumene/img/egypt_memphis_apis_stable.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789012345
  0 ################
  1 #######bc#######
  2 #.#.###..###.#.#
  3 .4#5.#....#6.#7.
  4 .......##.......
  5 ............##..
  6 ........2.......
  7 .#.3.......8.9..
  8 #.............a#
  9 .......11.......
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (7,9), (8,9) |  | door mat back to MAP_MEMPHIS (warp 2) |
| 2 | npc | (8,6) | faces south | Pakhom, the chief keeper |
| 3 | npc | (3,7) | faces east | a herdsman with a broom |
| 4 | npc | (1,3) | faces south | a black bull: a star on the brow |
| 5 | npc | (3,3) | faces south | a black bull: single tail hairs |
| 6 | npc | (11,3) | faces south | the true Apis |
| 7 | npc | (14,3) | faces south | a brown bull with every other mark |
| 8 | npc | (11,7) | faces west | a black bull: a plain back |
| 9 | npc | (13,7) | faces west | a black bull: a crescent on the brow |
| a | npc | (14,8) | faces west | Hesat, mother of the last Apis |
| b | bg | (7,1) | (7,2) facing north | the window of appearances |
| c | bg | (8,1) | (8,2) facing north | the window of appearances |

### The scribe of Thoth's house, Memphis

- Map: `MAP_MEMPHIS_SCRIBES_HOUSE`. Layout: `data/layouts/Memphis_ScribesHouse/map.bin`, **11x8** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: mat. Wall: plaster. Render: `design/oikoumene/img/egypt_memphis_scribes_house.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    01234567890
  0 ###########
  1 #####45####
  2 #7##....6##
  3 .....2.#...
  4 ...3##.#...
  5 #.........#
  6 .#.........
  7 .....11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,7), (6,7) |  | door mat back to MAP_MEMPHIS (warp 3) |
| 2 | npc | (5,3) | faces south | Amenemope, scribe of Thoth |
| 3 | npc | (3,4) | faces east | his apprentice, copying |
| 4 | bg | (5,1) | (5,2) facing north | the hieroglyph panel |
| 5 | bg | (6,1) | (6,2) facing north | the hieroglyph panel |
| 6 | bg | (8,2) | (8,3) facing north | the ibis of Thoth |
| 7 | bg | (1,2) | (1,3) facing north | the papyrus niches |

### The embalmer's house, Memphis

- Map: `MAP_MEMPHIS_EMBALMERS_HOUSE`. Layout: `data/layouts/Memphis_EmbalmersHouse/map.bin`, **11x8** blocks, `gTileset_Oikos` + `gTileset_Per`.
- Floor: flags. Wall: brick. Render: `design/oikoumene/img/egypt_memphis_embalmers_house.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    01234567890
  0 ###########
  1 ###########
  2 ###.4#.5#.#
  3 ...........
  4 .#3...##...
  5 ....2.....#
  6 6.........#
  7 .....11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,7), (6,7) |  | door mat back to MAP_MEMPHIS (warp 4) |
| 2 | npc | (4,5) | faces south | Khay the embalmer |
| 3 | bg | (2,4) | (2,5) facing north | the wrapped bundle |
| 4 | bg | (4,2) | (4,3) facing north | the canopic jars |
| 5 | bg | (7,2) | (7,3) facing north | the jackal mask |
| 6 | bg | (0,6) | (1,6) facing west | the linen basket |

### The pieces

Built: **363** metatiles (`0x200`-`0x36a`) of 512, **482** tiles of 504, palettes 6-12.

| Stamp | Cells | Palette | Metatiles | What it is |
|---|---|---|---|---|
| `mat` | 2x1 | nature | 256 257 | papyrus door mat; both cells are south-arrow warps |
| `counter_heal_l` | 1x2 | stone | 21D / 225 | the Asclepeion's counter (left end): civic's, shared |
| `counter_heal_m` | 1x2 | stone | 221 / 226 | the Asclepeion's counter (middle): civic's, shared |
| `counter_heal_r` | 1x2 | stone | 222 / 227 | the Asclepeion's counter (right end): civic's, shared |
| `counter_heal_staff` | 1x2 | stone | --- / 313 | the healer's place at the counter: the slab is on the top layer, over her |
| `counter_stall_m` | 1x2 | wood | 246 / 24C | the Agora's stall counter (middle): civic's, shared |
| `counter_stall_staff` | 1x2 | wood | --- / 24C | the stallkeeper's place: the slab is on the top layer, over them |
| `counter_stall_l_scale` | 1x2 | wood | 30B / 24B | the stall counter's left end, with a balance |
| `counter_stall_r_bread` | 1x2 | wood | 30C / 24D | the stall counter's right end, with loaves and a beer jug |
| `pithos` | 2x2 | wood | 30D 30E / 314 315 | the Pithos: a great silt-ware jar sealed with a stamped mud stopper |
| `window_river` | 1x2 | nature | 213 / 216 | a high window with a palm-wood grille: the Nile, a far bank and a sail |
| `ear_stele` | 1x2 | stone | 215 / 21C | an ear stele: a votive carved with ears, so the god will hear |
| `bed` | 2x1 | wood | 30F 310 | an Egyptian bed on lion's legs, with a footboard and a wooden headrest |
| `stool` | 1x1 | wood | 264 | a folding stool with crossed legs and a leather seat |
| `chair` | 1x1 | wood | 311 | a chair with a slanted back and lion's feet |
| `table` | 1x1 | wood | 2A4 | a low table with a bowl of figs |
| `jar` | 1x1 | wood | 312 | a silt-ware jar with a white band, on its ring stand |
| `jars` | 1x1 | wood | 296 | beer jars, stoppered with mud |
| `chest` | 1x1 | wood | 316 | a chest with painted panels and a gabled lid |
| `basket_dates` | 1x1 | nature | 317 | a basket of dates |
| `basket_eggs` | 1x1 | nature | 318 | a wicker basket of eggs |
| `basket_fish` | 1x1 | nature | 319 | a basket of Nile perch |
| `sacks_frank` | 1x1 | wood | 31A | sacks of frankincense: pale gold tears |
| `sacks_myrrh` | 1x1 | wood | 294 | sacks of myrrh: red-brown lumps |
| `sacks_grain` | 1x1 | wood | 24F | sacks of emmer wheat |
| `papyrus_column` | 1x3 | stone | 31B / 320 / 325 | a closed-bud papyrus column, ribbed, its neck bound in gold and red |
| `papyrus_pot` | 1x2 | nature | 31C / 321 | papyrus growing in a pot of river water |
| `lamp` | 1x2 | fire | 31D / 322 | a clay oil lamp, lit, on a bronze stand |
| `basin_naukratis` | 2x2 | stone | 31E 31F / 323 324 | the healing basin, Naukratis: river water from a gold lotus spout |
| `basin_memphis` | 2x2 | stone | 326 327 / 323 324 | the healing basin, Memphis: an offering table with a pool |
| `imhotep` | 1x2 | stone | 328 / 331 | Imhotep, the Greeks' Asclepius, seated with a papyrus on his knees |
| `counter_heal_front` | 1x1 | stone | 226 | the Asclepeion counter's front, under the basin |
| `relief_rod` | 1x2 | stone | 214 / 219 | the rod of Asclepius painted over the counter (civic's relief) |
| `amphora_rack` | 2x2 | wood | 329 251 / 332 255 | Greek transport amphorae in a rack: wine from Chios, oil from Samos |
| `crate_fossils` | 1x1 | wood | 32A | an open crate of fossils bedded in straw: a coiled shell, a dome, amber |
| `crate_shut` | 1x1 | wood | 258 | a shut packing crate |
| `crate_stack` | 1x2 | wood | 32B / 333 | two packing crates, roped, marked with a delta |
| `silt_trough` | 2x1 | wood | 265 266 | Daphne's revival trough: black Nile silt, kept warm, a fossil half out of it |
| `desk_notes` | 2x1 | wood | 32C 32D | a work table: field notes on papyrus, reed brushes, a bone being drawn |
| `cot` | 2x1 | wood | 32E 32F | Daphne's camp cot, a striped blanket and her satchel |
| `chart` | 2x2 | wood | 259 25A / 25C 25D | Daphne's chart of the Oikoumene, her route inked in red |
| `dig_tools` | 1x1 | wood | 330 | a pick and a brush, laid down for the day (civic's) |
| `egg_oven` | 2x2 | fire | 334 335 / 33F 340 | an egg-oven of mud brick: eggs on straw below, the fire-trough's slot above |
| `fire_trough` | 1x1 | fire | 281 | a fire-trough sunk in the floor, smouldering |
| `fuel` | 1x1 | fire | 278 | dung cakes stacked for the ovens' fires |
| `censer` | 1x2 | fire | --- / 341 | a bronze censer on its tripod, smoke rising |
| `incense_table` | 2x1 | wood | 337 338 | the incense merchant's low table: a balance and heaps of resin |
| `jar_shelf` | 2x2 | wood | 339 33A / 342 343 | shelves of stoppered jars and alabaster flasks of oil |
| `wheel` | 1x1 | wood | 2A2 | the potter's turntable, a wet pot on it |
| `kiln` | 2x2 | fire | 33B 33C / 344 345 | the potter's kiln, its fire-mouth glowing |
| `pot_shelf` | 2x2 | wood | 33D 33E / 346 347 | shelves of Naukratite pottery: white-slipped chalices with painted bands |
| `clay_tub` | 1x1 | wood | 2A3 | a trough of wet Nile clay |
| `greenware` | 1x1 | wood | 2A1 | unfired pots drying on a plank |
| `net_rack` | 2x2 | nature | 348 349 / 355 356 | nets drying over two poles, cork floats on the head-rope |
| `ground_loom` | 2x2 | wood | 34A 34B / 357 358 | a ground loom pegged to the floor, a length of linen half woven |
| `flax` | 1x1 | nature | 34C | sheaves of flax for linen |
| `spindles` | 1x1 | nature | 34D | a basket of spindles and linen thread |
| `skiff` | 2x1 | nature | 34E 34F | a papyrus skiff, bound in five places, ends curled up |
| `basket_bread` | 1x1 | wood | 350 | a basket of conical loaves and a jug of beer |
| `onions` | 1x2 | nature | 2CD / 2CE | strings of onions and garlic, hung up to dry |
| `linen_bolts` | 1x1 | wood | 351 | bolts of linen, the finest on top |
| `amulets` | 1x1 | paint | 352 | a tray of faience amulets: scarabs and eyes of Horus |
| `stall_wall` | 1x2 | mud | 353 / 2E5 | a stall's low partition of whitewashed mud brick |
| `manger` | 1x1 | stone | 354 | a limestone manger heaped with fodder |
| `water_trough` | 2x1 | stone | 2E6 2E7 | a long limestone water trough |
| `hay` | 1x1 | nature | 359 | a heap of hay |
| `window_apis` | 2x2 | stone | 305 306 / 307 308 | the window of appearances, under a cornice of gilded cobras |
| `niches` | 2x2 | wood | 35A 35B / 366 367 | the scribe's niches: papyrus rolls stacked end-on |
| `scribe_desk` | 2x1 | wood | 35C 35D | a low writing table: a papyrus, the palette's red and black inks, a water pot |
| `ibis` | 1x2 | stone | 35E / 368 | Thoth as an ibis on a gilt-edged pedestal |
| `baboon` | 1x1 | stone | 35F | Thoth's baboon, seated, the moon's disc on its head |
| `glyphs` | 2x2 | paint | 2E9 2EA / 2ED 2EE | a painted panel of hieroglyphs: the scribe's riddles |
| `natron_table` | 2x1 | stone | 360 361 | an embalming bed of stone, lion-headed, a linen-wrapped bundle on it |
| `natron` | 1x1 | stone | 362 | a heap of natron, the drying salt, on a reed tray |
| `canopic` | 1x1 | stone | 363 | four canopic jars, lidded with the four sons of Horus |
| `anubis` | 1x2 | stone | 364 / 369 | the jackal mask of Anubis on its stand |
| `resin_pot` | 1x1 | fire | 365 | a pot of resin warming over coals |
| `linen_rolls` | 1x1 | nature | 36A | a basket of linen bandage rolls |

<!-- per_build: end generated -->
