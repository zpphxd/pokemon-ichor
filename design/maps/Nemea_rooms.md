# Nemea rooms

Written by tools/ichor/maps/nemea_rooms.py (via ergasteria_build.py).

<!-- domos_build: begin generated -->

### The palaestra, Nemea

- Map: `MAP_NEMEA_PALAESTRA`. Layout: `data/layouts/Nemea_Palaestra/map.bin`, **16x11** blocks, `gTileset_Oikos` + `gTileset_Domos`.
- Floor: terracotta, claydust. Wall: red. Render: `design/phase2/img/nemea_palaestra.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    0123456789012345
  0 ################
  1 ##5#######6#####
  2 #.....##.#....#.
  3 #..#..##2#..#.#.
  4 ...#........#...
  5 ...#..3.....#...
  6 .##..........##.
  7 ...#........#...
  8 .#.#.....##.#...
  9 .7.#.....##4##..
 10 .......11.......
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (7,10), (8,10) |  | door to Nemea (south-arrow mat) |
| 2 | npc | (8,3) | faces south | Kleitos the trainer, by the hearth |
| 3 | npc | (6,5) | faces east | Tisandros the wrestler, in the sand pit |
| 4 | npc | (11,9) | faces west | Chionis the runner, by the benches |
| 5 | bg | (2,1) | (2,2) facing north | the course scratched on the plaster |
| 6 | bg | (10,1) | (10,2) facing north | the oil jars |
| 7 | bg | (1,9) | (2,9) facing west | the washbasin |

### Molorchos's cottage, Nemea

- Map: `MAP_NEMEA_MOLORCHOS_HOUSE`. Layout: `data/layouts/Nemea_MolorchosHouse/map.bin`, **11x8** blocks, `gTileset_Oikos` + `gTileset_Domos`.
- Floor: terracotta. Wall: tavern. Render: `design/phase2/img/nemea_molorchos.png` (2x).

Walk map: `#` blocked, `.` open. Digits and letters mark the spots in the table; a bg event is marked on its furniture tile.

```
    01234567890
  0 ###########
  1 ###########
  2 ###......#3
  3 #4...2.....
  4 ...###.....
  5 ##.....#.#.
  6 ##.........
  7 .....11....
```

| # | Kind | Tile | Read from | What |
|---|---|---|---|---|
| 1 | warp | (5,7), (6,7) |  | door to Nemea (south-arrow mat) |
| 2 | npc | (5,3) | faces south | Molorchos, at his table |
| 3 | bg | (10,2) | (10,3) facing north | the honey jar |
| 4 | bg | (1,3) | (1,4) facing north | the hearth |

<!-- domos_build: end generated -->
