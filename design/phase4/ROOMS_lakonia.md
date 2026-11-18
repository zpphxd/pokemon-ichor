# Lakonia's rooms: Gytheion and Lakonia

Fifteen interiors for Act III's Lakonia chapter (`design/phase4/SCRIPT.md`, Part 2,
Gytheion and Lakonia). Every house is a home and every interior is unique
(`design/MAP_DESIGN.md` §2): each room is drawn for who lives or works in it.

```bash
/usr/bin/python3 tools/ichor/maps/lakonia_rooms.py                 # compose, compile the three sets, write the rooms
/usr/bin/python3 tools/ichor/maps/lakonia_rooms.py --no-compile --preview DIR   # compose and look
```

## How they're built

- **Machinery:** `tools/ichor/art/ergasteria_build.py`'s RoomSet, as Emporion's and
  Eleusa's rooms are: compose every cell from stamps, deduplicate, compile with
  Porytiles against aethos, check every room renders identically on oikos, aethos
  and building, write the layouts. Rooms are data in `tools/ichor/maps/lakonia_rooms.py`;
  never hand-edit their `map.bin`, since metatile ids move whenever a room changes.
- **Art:** `tools/ichor/art/lakonia_rooms_art.py`, in oikia's seven palettes (limen's
  copy, with Tyrian purple in cloth). It carries oikia's, ergasteria's and limen's
  furniture as it is and draws what these rooms needed (below).
- **Three secondaries,** so each stays well inside 504 tiles and carries only the
  floors and walls its rooms use:

  | Tileset | Rooms | Floors | Walls |
  |---|---|---|---|
  | `gTileset_OikiaGytheion` | Gytheion's five | flags, boards, terracotta, sea | stone, blue, red, white |
  | `gTileset_OikiaLakonia` | Lampito, Gylippos, Chilon, Lichas, the syssition | beaten earth | Lakonian plaster, smoke, sayings |
  | `gTileset_CivicLakonia` | the Asclepeion, the Agora, the agoge, the palaestra, Orthia | flags, earth, sand, court | stone, Lakonian plaster |

- **Doors:** each room's warps 0 and 1 are its door mat, back to its town's warp:
  Gytheion 0 Asclepeion, 1 dye-works, 2 Lysandros, 3 Timaia, 4 Kranai; Lakonia 0
  Asclepeion, 1 Agora, 2 Lampito, 3 Gylippos, 4 syssition, 5 agoge, 6 palaestra,
  7 Orthia, 8 Chilon, 9 Lichas.
- **Script swaps:** `include/constants/metatile_labels.h` gets the hearth's
  (`METATILE_OikiaLakonia_Hearth_{Cold,Lit}_{TL,TR,BL,BR}`) and Orthia's altar
  (`METATILE_CivicLakonia_Altar_{West,Middle,East}` and `_Cheese_*`), written by the
  builder. The room variants write `LakoniaLampito_EventScript_SetHearthLit` and
  `LakoniaOrthia_EventScript_AltarBare` into their maps' scripts.pory.

## Pieces drawn for these rooms

Lakonian plaster over mudbrick (no dado, no paint), the syssition's soot-black
wall, Chilon's wall of scratched sayings, Kranai's whitewash with a pink foot;
beaten earth, raked sand in a dark kerb, Orthia's flags with marsh grass in the
joints. Two grave-stelai painted on the plaster (AGIS; a swallow), the loom with a
small red cloak, the hearth cold and lit, a wall patch where the plaster has
fallen off the brick; the elders' twelve scytale staffs, a reed sleeping mat,
Gylippos's stool with the strap on it; the IF shard; cushions, the Olympic tripod,
figs; the mess table's plank, cups on pegs, the black cauldron, the barley barrel;
thirty reed mats (two weaves), the spear rack, red cloaks on pegs, the herd's
names struck through; oil flasks and strigils, six dried olive crowns, a bench of
folded cloaks; a willow, the long altar with and without its cheeses, the
goddess's bound wooden image, marsh reeds; the plank-on-two-stones counter, a
marble spring trough with its spout, the great scales, iron bars stacked like
firewood, a plank stall; scenery flats (a palace, the sea), theater masks on pegs,
the window over the front rows, the old ticket counter; a lead dye vat, the murex
heap, hanging skeins, the hank under its cloth; the gulf scratched in plaster,
model triremes, a bronze ram; the bread oven, a child's wooden spear, the fig
cake under its cloth, folded nets; the dove niche and the votive sandals.

## The rooms, and the critique passes

Each room was rendered, critiqued and fixed three times
(`design/phase4/img/rooms_lakonia/pass1`, `pass2`, `pass3`; the final renders sit
beside them).

**Pass 1 to 2.**
- The Lakonian wall repeated its fallen-plaster patch on every tile, so every
  Lakonian room read as polka-dot wallpaper. The patch became its own piece
  (`wall_worn`), placed once or twice a room where a wall gets knocked.
- The spring basin read as a dark box on the wall (a stove, or a television). It
  became marble with water in it.
- The syssition's soot only darkened the top band, and its cups were dots: the
  whole wall is smoke now, and the cups are cups.
- The palaestra's sand pit was nearly the flags' color; it is now pale and raked,
  in a dark stone kerb.
- Lichas's cushions sat beside his rug instead of on it. Gytheion's Asclepeion
  had nothing over the counter: the actors' old masks hang there now. The agoge's
  mats were one tile repeated thirty times; they alternate two weaves. Orthia
  got marsh reeds through the flags at its edges.

**Pass 2 to 3.**
- The marble basin still read as a screen on a stand, framed and upright. It is a
  low trough at the foot of the wall now, fed by a spout in the plaster, so the
  heal animation's balls land in the water.
- Spots checked against reach: the agoge's master moved a tile so his corner
  (the herd's names) can be read; signs nobody could face were dropped.

**Notes per room.**
- *Gytheion's Asclepeion:* a long, narrow hall (16x7), the flats and masks to the
  west, the counter in the middle, two windows on the front rows and the benches
  under them to the east, the Pithos at the end. The healer's trough is at her
  right hand, as Akti's is, so the heal animation lands in it.
- *The dye-works:* the east end is open to the sea (two blocked columns of
  harbor). Three vats steam in two rows; the shell heap and the hank are by the
  open end, where the light is.
- *Lysandros:* the gulf map covers the west wall, the window is mostly sea, the
  triremes are over his couch, and the ram holds the door.
- *Timaia:* small and warm: the oven in the corner, the cake on the table, the
  spear behind the door.
- *Kranai:* one white room, the doves in the niche between two windows, the
  sandals hanging in both corners, the bench under the window toward Kythera.
- *Lampito:* the loom and the chest under it in the west corner, the hearth (cold
  until III-5E) against the back wall under its soot, the two stelai to the east,
  the table and two stools in the middle where Kleon sits.
- *Gylippos:* almost empty, as SCRIPT says. The staffs are the only thing on the
  walls.
- *Chilon:* the sayings are the wall itself; the IF shard on its shelf.
- *Lichas:* cushions on a red rug (the only rug in Lakonia), the hearth lit, the
  tripod, the curtained guest bed.
- *The syssition:* no windows, one long plank, fifteen places, the cauldron at the
  far end.
- *Lakonia's Asclepeion:* bare stone, a plank on two stones, one bench.
- *The Agora:* the scales on the wall behind the stall, the iron bars by the door.
- *The agoge:* thirty mats in three rows, cloaks along the whole back wall, the
  master's corner (stool, names, spears) in the east.
- *The palaestra:* the pit in the west half, the porch (two columns, a louterion,
  the bench of cloaks) in the east, the crowns over the middle.
- *Orthia:* willows in both back corners, the image between them, the long altar
  across the court, benches for watchers by the gate. The cheese game's two
  watchers stand west and east; the safe ways are behind their backs.

### Lampito's house: coordinates for the story scripts

| What | Where |
|---|---|
| Door mat | (5,8) and (6,8): warps 0 and 1, to `MAP_LAKONIA` warp 2 |
| Table | (6,5) and (7,5) (solid) |
| Stools | (5,5) and (8,5), walkable: whoever stands on one sits |
| Hearth | (4..5, 2..3), solid; read from (4,4) facing north. Cold: `METATILE_OikiaLakonia_Hearth_Cold_TL/TR/BL/BR` at (4,2) (5,2) (4,3) (5,3); lit: `METATILE_OikiaLakonia_Hearth_Lit_*`. `LakoniaLampito_EventScript_SetHearthLit` (generated) sets all four; `ON_LOAD` calls it once `FLAG_ICHOR_RHEA_UNMASKED` is set |
| Soot over the hearth | (4..5, 0..1), wall |
| Loom (red cloak) | (0..1, 0..2); read from (2,2) facing west |
| Chest under the loom | (0..1, 3..4); read from (2,4) facing west |
| Stelai | AGIS (7,0..1), swallow (9,0..1); read from (7,2) and (9,2) facing north |
| `LOCALID_LAMPITO_KLEON` | (5,5), on the west stool, facing east; gfx `OBJ_EVENT_GFX_ICHOR_KLEON` |
| `LOCALID_LAMPITO_RHEA` | (5,7), just inside the door, facing north; gfx `OBJ_EVENT_GFX_VAR_1` |
| `LOCALID_LAMPITO_ALETHEA` | (8,7), facing north; gfx `OBJ_EVENT_GFX_ICHOR_ALETHEA` |
| `LOCALID_LAMPITO_HELMET` | (6,5), on the table; placeholder gfx `OBJ_EVENT_GFX_ICHOR_TABLET` |
| `LOCALID_LAMPITO_TABLET` | (7,5), on the table; placeholder gfx `OBJ_EVENT_GFX_ICHOR_TABLET` |
| Open floor | rows 2..7 east of the chest, round the hearth and table; the player reaches the table from (6,4) or (6,6) |

All five objects have flag `0`; the chapter builder gives them hide flags.

## Generated tables

<!-- oikia_gytheion_build: begin generated -->

### The Asclepeion, Gytheion (the stage-building)

- Map: `MAP_GYTHEION_ASCLEPEION`. Layout: `data/layouts/Gytheion_Asclepeion/map.bin`, **16x7** blocks, `gTileset_Oikos` + `gTileset_OikiaGytheion`.
- Floor: flags. Wall: stone. Render: `design/phase2/img/Gytheion_Asclepeion.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789012345
  0 ################
  1 #4#5#######6####
  2 ....###2.......7
  3 ......###.......
  4 #.........####.#
  5 #..........3...#
  6 .......11.......
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (7,6), (8,6) |  | the door to the quay (south-arrow mat) |
| 2 | npc | (7,2) | faces south | the healer, at the old ticket counter |
| 3 | npc | (11,5) | faces north | a fisherman with his arm in a sling, on the front bench |
| 4 | bg | (1,1) | (1,2) facing north | the scenery flat: a palace |
| 5 | bg | (3,1) | (3,2) facing north | the scenery flat: the sea |
| 6 | bg | (11,1) | (11,2) facing north | the window over the front rows |
| 7 | bg | (15,2) | (15,3) facing north | the Pithos |

### The dye-works, Gytheion

- Map: `MAP_GYTHEION_DYEWORKS`. Layout: `data/layouts/Gytheion_Dyeworks/map.bin`, **13x8** blocks, `gTileset_Oikos` + `gTileset_OikiaGytheion`.
- Floor: flags, sea. Wall: stone. Render: `design/phase2/img/Gytheion_Dyeworks.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789012
  0 #############
  1 #############
  2 .##..##..####
  3 .##..3#..4###
  4 ...........##
  5 .##.2.....###
  6 .##......5###
  7 .....11....##
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,7), (6,7) |  | the door to the beach (south-arrow mat) |
| 2 | npc | (4,5) | faces east | Porphyris, purple to the elbows |
| 3 | bg | (5,3) | (5,4) facing north | a lead vat |
| 4 | bg | (9,3) | (8,3) facing east | the shell heap |
| 5 | bg | (9,6) | (8,6) facing east | the hank under a cloth |

### Lysandros's house, Gytheion

- Map: `MAP_GYTHEION_LYSANDROS_HOUSE`. Layout: `data/layouts/Gytheion_LysandrosHouse/map.bin`, **10x8** blocks, `gTileset_Oikos` + `gTileset_OikiaGytheion`.
- Floor: boards. Wall: blue. Render: `design/phase2/img/Gytheion_LysandrosHouse.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789
  0 ##########
  1 #3##4##5##
  2 ..........
  3 #..###2.##
  4 #.......##
  5 #........#
  6 .........#
  7 ....116...
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (4,7), (5,7) |  | the door to the quay (south-arrow mat) |
| 2 | npc | (6,3) | faces west | Lysandros, the old harbor-master |
| 3 | bg | (1,1) | (1,2) facing north | the gulf scratched into the plaster |
| 4 | bg | (4,1) | (4,2) facing north | the window that's mostly sea |
| 5 | bg | (7,1) | (7,2) facing north | the model triremes |
| 6 | bg | (6,7) | (6,6) facing south | the bronze ram doorstop |

### Timaia's house, Gytheion

- Map: `MAP_GYTHEION_TIMAIA_HOUSE`. Layout: `data/layouts/Gytheion_TimaiaHouse/map.bin`, **9x7** blocks, `gTileset_Oikos` + `gTileset_OikiaGytheion`.
- Floor: terracotta. Wall: red. Render: `design/phase2/img/Gytheion_TimaiaHouse.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678
  0 #########
  1 #########
  2 #3...#6..
  3 .........
  4 ..##42..#
  5 ......5.#
  6 ....11#..
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (4,6), (5,6) |  | the door to the lane (south-arrow mat) |
| 2 | npc | (5,4) | faces west | Timaia, by her table |
| 3 | bg | (1,2) | (1,3) facing north | the bread oven |
| 4 | bg | (4,4) | (4,5) facing north | the fig cake under its cloth |
| 5 | bg | (6,5) | (7,5) facing west | the child's wooden spear |
| 6 | bg | (6,2) | (6,3) facing north | the folded nets |

### The shrine on Kranai, Gytheion

- Map: `MAP_GYTHEION_KRANAI_SHRINE`. Layout: `data/layouts/Gytheion_KranaiShrine/map.bin`, **9x7** blocks, `gTileset_Oikos` + `gTileset_OikiaGytheion`.
- Floor: flags. Wall: white. Render: `design/phase2/img/Gytheion_KranaiShrine.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678
  0 #########
  1 #4##3####
  2 #.....5#.
  3 #.2......
  4 ........#
  5 ........#
  6 ...11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (3,6), (4,6) |  | the door to the islet (south-arrow mat) |
| 2 | npc | (2,3) | faces south | Klymene, the shrine-keeper |
| 3 | bg | (4,1) | (4,2) facing north | the doves in the niche |
| 4 | bg | (1,1) | (1,2) facing north | the votive sandals |
| 5 | bg | (6,2) | (5,2) facing east | the bench under the window, toward Kythera |

<!-- oikia_gytheion_build: end generated -->

<!-- oikia_lakonia_build: begin generated -->

### Lampito's house, Lakonia

- Map: `MAP_LAKONIA_LAMPITOS_HOUSE`. Layout: `data/layouts/Lakonia_LampitosHouse/map.bin`, **11x9** blocks, `gTileset_Oikos` + `gTileset_OikiaLakonia`.
- Floor: earth. Wall: lakon. Render: `design/phase2/img/Lakonia_LampitosHouse.png` (2x).
- Variant `lit`: `LakoniaLampito_EventScript_SetHearthLit` in the map's scripts.pory swaps its cells.

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    01234567890
  0 ###########
  1 #######8#9#
  2 #5..###...#
  3 ##..7#....#
  4 #6.........
  5 .....2##...
  6 ..........#
  7 .....3..4.#
  8 .....11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,8), (6,8) |  | the door to the yard (south-arrow mat) |
| 2 | npc | (5,5) | faces east | Kleon, at the table |
| 3 | npc | (5,7) | faces north | Rhea, just inside the door |
| 4 | npc | (8,7) | faces north | Alethea, by the door |
| 5 | bg | (1,2) | (2,2) facing west | the loom |
| 6 | bg | (1,4) | (2,4) facing west | the chest under the loom |
| 7 | bg | (4,3) | (4,4) facing north | the hearth |
| 8 | bg | (7,1) | (7,2) facing north | the stele: AGIS |
| 9 | bg | (9,1) | (9,2) facing north | the stele: a swallow |

### Gylippos's house, Lakonia

- Map: `MAP_LAKONIA_GYLIPPOS_HOUSE`. Layout: `data/layouts/Lakonia_GylipposHouse/map.bin`, **7x7** blocks, `gTileset_Oikos` + `gTileset_OikiaLakonia`.
- Floor: earth. Wall: lakon. Render: `design/phase2/img/Lakonia_GylipposHouse.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456
  0 #######
  1 ###3###
  2 .......
  3 #...24.
  4 #.....#
  5 ......#
  6 ...11..
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (3,6), (4,6) |  | the door to the lane (south-arrow mat) |
| 2 | npc | (4,3) | faces south | Gylippos, standing (the stool is his) |
| 3 | bg | (3,1) | (3,2) facing north | the elders' staffs |
| 4 | bg | (5,3) | (5,4) facing north | the stool and the strap |

### Chilon's house, Lakonia

- Map: `MAP_LAKONIA_CHILON_HOUSE`. Layout: `data/layouts/Lakonia_ChilonHouse/map.bin`, **8x7** blocks, `gTileset_Oikos` + `gTileset_OikiaLakonia`.
- Floor: earth. Wall: sayings. Render: `design/phase2/img/Lakonia_ChilonHouse.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    01234567
  0 ########
  1 ##4##3##
  2 #......#
  3 #.2##..#
  4 .......#
  5 ........
  6 ...11...
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (3,6), (4,6) |  | the door to the lane (south-arrow mat) |
| 2 | npc | (2,3) | faces south | Chilon, a very old man |
| 3 | bg | (5,1) | (5,2) facing north | the shard that says IF |
| 4 | bg | (2,1) | (2,2) facing north | the sayings on the wall |

### Lichas's house, Lakonia

- Map: `MAP_LAKONIA_LICHAS_HOUSE`. Layout: `data/layouts/Lakonia_LichasHouse/map.bin`, **10x8** blocks, `gTileset_Oikos` + `gTileset_OikiaLakonia`.
- Floor: earth. Wall: lakon. Render: `design/phase2/img/Lakonia_LichasHouse.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789
  0 ##########
  1 ###3######
  2 ##..2...4#
  3 ##...#5...
  4 .........#
  5 ....####.#
  6 ..........
  7 ....11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (4,7), (5,7) |  | the door to the lane (south-arrow mat) |
| 2 | npc | (4,2) | faces south | Lichas, the host |
| 3 | bg | (3,1) | (3,2) facing north | the tripod with someone else's name on it |
| 4 | bg | (8,2) | (7,2) facing east | the guest bed behind its curtain |
| 5 | bg | (6,3) | (6,2) facing south | the figs |

### The syssition, Lakonia

- Map: `MAP_LAKONIA_SYSSITION`. Layout: `data/layouts/Lakonia_Syssition/map.bin`, **15x7** blocks, `gTileset_Oikos` + `gTileset_OikiaLakonia`.
- Floor: earth. Wall: smoke. Render: `design/phase2/img/Lakonia_Syssition.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678901234
  0 ###############
  1 ####4##########
  2 #...........###
  3 ..#.#.#.#..23##
  4 .#########.....
  5 ...#.#.#.......
  6 ......11.......
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (6,6), (7,6) |  | the door to the agora (south-arrow mat) |
| 2 | npc | (11,3) | faces south | Dexippos, the cook |
| 3 | bg | (12,3) | (12,4) facing north | the black cauldron |
| 4 | bg | (4,1) | (4,2) facing north | the cups on their pegs |

<!-- oikia_lakonia_build: end generated -->

<!-- civic_lakonia_build: begin generated -->

### The Asclepeion, Lakonia

- Map: `MAP_LAKONIA_ASCLEPEION`. Layout: `data/layouts/Lakonia_Asclepeion/map.bin`, **9x7** blocks, `gTileset_Oikos` + `gTileset_CivicLakonia`.
- Floor: flags. Wall: stone. Render: `design/phase2/img/Lakonia_Asclepeion.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678
  0 #########
  1 #########
  2 ..4#2...3
  3 ...###...
  4 .........
  5 ......##.
  6 ...11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (3,6), (4,6) |  | the door to the road (south-arrow mat) |
| 2 | npc | (4,2) | faces south | the healer, a Lakonian woman of very few words |
| 3 | bg | (8,2) | (8,3) facing north | the Pithos |
| 4 | bg | (2,2) | (1,2) facing east | the spring basin |

### The Agora, Lakonia

- Map: `MAP_LAKONIA_AGORA`. Layout: `data/layouts/Lakonia_Agora/map.bin`, **9x7** blocks, `gTileset_Oikos` + `gTileset_CivicLakonia`.
- Floor: earth. Wall: lakon. Render: `design/phase2/img/Lakonia_Agora.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678
  0 #########
  1 #####3###
  2 ##.2.....
  3 ..###....
  4 .........
  5 ......4#.
  6 ...11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (3,6), (4,6) |  | the door to the road (south-arrow mat) |
| 2 | npc | (3,2) | faces south | the stallkeeper, who weighs everything |
| 3 | bg | (5,1) | (5,2) facing north | the great scales |
| 4 | bg | (6,5) | (6,4) facing south | the iron bars |

### The agoge, Lakonia

- Map: `MAP_LAKONIA_AGOGE`. Layout: `data/layouts/Lakonia_Agoge/map.bin`, **16x10** blocks, `gTileset_Oikos` + `gTileset_CivicLakonia`.
- Floor: earth. Wall: lakon. Render: `design/phase2/img/Lakonia_Agoge.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789012345
  0 ################
  1 ###6##########4#
  2 ................
  3 ............2#..
  4 ..............##
  5 ..............5#
  6 .....3..........
  7 ................
  8 ................
  9 .......11.......
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (7,9), (8,9) |  | the door to the yard (south-arrow mat) |
| 2 | npc | (12,3) | faces south | Archidamos, the boys' master, by his stool |
| 3 | npc | (5,6) | faces south | a cadet, sitting on his mat |
| 4 | bg | (14,1) | (14,2) facing north | the herd's names |
| 5 | bg | (14,5) | (13,5) facing east | the practice spears |
| 6 | bg | (3,1) | (3,2) facing north | the red cloaks |

### The palaestra, Lakonia

- Map: `MAP_LAKONIA_PALAESTRA`. Layout: `data/layouts/Lakonia_Palaestra/map.bin`, **13x9** blocks, `gTileset_Oikos` + `gTileset_CivicLakonia`.
- Floor: flags, sand. Wall: stone. Render: `design/phase2/img/Lakonia_Palaestra.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789012
  0 #############
  1 #4###3#######
  2 .........##.#
  3 .........##.#
  4 ....2....#..#
  5 ..........5#.
  6 .............
  7 .............
  8 .....11......
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,8), (6,8) |  | the door to the sands (south-arrow mat) |
| 2 | npc | (4,4) | faces south | Hipposthenes, six times crowned |
| 3 | bg | (5,1) | (5,2) facing north | the six olive crowns |
| 4 | bg | (1,1) | (1,2) facing north | the oil flasks and scrapers |
| 5 | bg | (10,5) | (10,6) facing north | the bench of folded cloaks |

### The sanctuary of Artemis Orthia, Lakonia

- Map: `MAP_LAKONIA_ORTHIA`. Layout: `data/layouts/Lakonia_Orthia/map.bin`, **15x11** blocks, `gTileset_Oikos` + `gTileset_CivicLakonia`.
- Floor: court. Wall: stone. Render: `design/phase2/img/Lakonia_Orthia.png` (2x).
- Variant `bare`: `LakoniaOrthia_EventScript_AltarBare` in the map's scripts.pory swaps its cells.

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    012345678901234
  0 ###############
  1 #######5#######
  2 ##...........##
  3 #....6#7#8.....
  4 #.3...........#
  5 ...............
  6 #...........4.#
  7 #.............#
  8 .##......2..##.
  9 #.............#
 10 .......11......
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (7,10), (8,10) |  | the gate to the river bank (south-arrow mat) |
| 2 | npc | (9,8) | faces west | Kleta, the priestess |
| 3 | npc | (2,4) | faces east | a watching cadet (west) |
| 4 | npc | (12,6) | faces west | a watching cadet (east) |
| 5 | bg | (7,1) | (7,2) facing north | the goddess's wooden image |
| 6 | bg | (5,3) | (5,2) facing south | the cheese, west end |
| 7 | bg | (7,3) | (7,2) facing south | the cheese, middle |
| 8 | bg | (9,3) | (9,2) facing south | the cheese, east end |

<!-- civic_lakonia_build: end generated -->
