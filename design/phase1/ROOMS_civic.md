# Civic rooms: the Akti Asclepeion, the Akti Agora and the Elaia Akademia

These are the three slice interiors, built from `gTileset_Civic` (see `TILES_civic.md`) and ready for the director to wire into the maps.

- **Source:** `tools/ichor/art/civic_rooms.py`. Each room is a short layout function there.
- **Rebuild:** `/usr/bin/python3 tools/ichor/art/civic_rooms.py` rewrites the blockdata and the renders. It also checks that each room renders identically over the `aethos` and `building` primaries.

| Room | Size | Blockdata | Render (3×) |
|---|---|---|---|
| Akti Asclepeion | 15×11 | `rooms/akti_asclepeion.bin` | `img/rooms_akti_asclepeion.png` |
| Akti Agora | 13×9 | `rooms/akti_agora.bin` | `img/rooms_akti_agora.png` |
| Elaia Akademia | 16×13 | `rooms/elaia_akademia.bin` | `img/rooms_elaia_akademia.png` |

## Wiring a room in

**The blockdata.** The `.bin` files are ready-made `map.bin` files: one u16 per block, row by row.
- Bits 0–9 hold the metatile id.
- Bits 10–11 hold collision. Solid cells are `0x04xx`.
- Bits 12–15 hold elevation. Walkable cells are `0x3xxx`, Emerald's interior convention.

**The layout entry.**
- `width` and `height`: as in the table above.
- `primary_tileset`: the interior primary. Use `gTileset_Building` now, and `oikos` when it lands. Civic draws nothing from the primary.
- `secondary_tileset`: `gTileset_Civic`.
- `border.bin`: four copies of `0x0200` (`void`), the near-black border metatile.

**Metatile ids** are listed in `TILES_civic.md`. They move only if `civic_tiles.py` inserts a metatile mid-list, so append new ones at the end once maps use them.

## How to read the grids

Each grid shows collision and the cells that matter for events. Coordinates are (x, y) from the top-left, as in Porymap.

| Mark | Meaning |
|---|---|
| `.` | Walkable |
| `#` | Solid |
| `D` | Exit mat |
| `S` | Stairs warp |
| `@` | Where the NPC behind a counter stands (walkable) |
| `=` | Counter front: `MB_COUNTER`, talk across it |
| `~` | The spring basin |
| `P` | The Pithos (`MB_PC`) |
| `K` | Krater cell |
| `A` | Statue plinth |
| `M` | Wall map |
| `$` | Pottery shelf (`MB_SHOP_SHELF`) |
| `B` | Scroll cabinet (`MB_BOOKSHELF`) |

Column capitals, laurel canopies, brazier flames and the armillary sphere are drawn over walkers. They show as `.`. Don't stand an NPC on one, because it would be drawn behind the art.

## Akti Asclepeion (15×11)

```text
    012345678901234
  0 ###############
  1 #####~~########
  2 SSA.#~~@####PP#
  3 ....=======....
  4 ##.............
  5 ##.............
  6 ..#.#.....#.#..
  7 ##.............
  8 ##.............
  9 ...............
 10 ..#....D....###
```

**Exit.** Mat at (7,10), `MB_SOUTH_ARROW_WARP`. Put one warp there to the Akti Town door at (6,16).

**Stairs.** Warps at (0,2) and (1,2), `MB_NON_ANIMATED_DOOR`.
- The player walks north onto them from (0,3) or (1,3).
- The slice has no upper floor. Point them at one, or paint them over: set (0..1, 0) to `asc_wall_top`, (0..1, 1) to `asc_wall` and (0..1, 2) to `asc_floor_a_sh` / `asc_floor_b_sh`.

**The healer and the counter.**
- The healer stands at (7,2), on `asc_counter_staff`. It is walkable, with the counter slab drawn on the top layer, so she is hidden from the waist down.
- The player talks from (7,4) across the counter front at (7,3).
- The whole front, (4..10, 3), is `MB_COUNTER`.
- These are the vanilla Pokémon Center positions: nurse at (7,2), player at (7,4).

**The sacred spring and the heal animation.**
- The basin is at (5..6, 1..2): the healer's x−2..x−1 and y−1..y, where the vanilla healing machine stood.
- `FLDEFF_POKECENTER_HEAL` places the party's balls in screen coordinates relative to the player at (7,4). In this room they land on the basin's water, at basin pixels x 9–23, y 8–24.
- The animation's "monitor" sprite (`graphics/field_effects/pics/pokecenter_monitor/`) still flashes a Hoenn screen. It covers map pixels x 112–136, y 8–24: the lower half of (7,0), the upper half of (7,1) and the left half of x=8. That is the rod-of-Asclepius relief. Repainting the sprite as a golden glow would make the relief light up during healing. That file is outside civic.

**The rod of Asclepius.**
- The relief is at (7, 0..1), above the healer.
- The serpent's head is in row 0 so it shows over her head.

**Votives.** Tablets on the wall at (8..9, 1); clay limbs on the counter at (8..9, 2).

**The Pithos.**
- The great jar is at (12..13, 0..2). (12,2) and (13,2) are `MB_PC`, used from (12,3) or (13,3) facing up.
- Lidded jars at (11, 1..2) and (14, 1..2) answer as vases.
- The script's "woman by the Pithos" fits at (11,3) or (14,3).

**The statue of Asclepius.**
- It stands at (2, 0..2). Put the script's BG event "Asclepius, with a snake coiled round his staff…" on (2,2); the player reads it from (2,3).
- The old man "by the statue" fits at (3,2) or (3,3).

**Couches, columns and braziers.**
- The couches (klinai) are in the alcove at (0..1, 4..5) and (0..1, 7..8).
- Columns stand at x=2 and x=12, rows 4–6 and 8–10. Their bases at (2,6), (2,10), (12,6) and (12,10) are solid.
- Braziers are at (4, 5..6) and (10, 5..6), with solid bases in row 6.
- The god's snake lies at (1,9).

**Floor and bench.**
- The floor mosaic at (6..8, 5..7) is walkable.
- The bench is at (13..14, 10). The bandaged fisher fits at (13,9) or (14,9).

## Akti Agora (13×9)

```text
    0123456789012
  0 #############
  1 #############
  2 ..#@#....$$$.
  3 #.===.....###
  4 #.....##....#
  5 ......##.....
  6 .............
  7 ##..#...#..##
  8 #.....D.....#
```

**Exit.** Mat at (6,8). Warp to the Akti Town Agora door at (14,6).

**Demeas's stall.**
- Demeas stands at (3,2), on `ago_counter_staff`, under the striped awning at (2..4, 0..1).
- The player talks from (3,4) across (3,3). The front, (2..4, 3), is `MB_COUNTER`.
- The bronze balance scale is on the counter at (2,2), and a loaf and an oil flask at (4,2).

**Shelves and wall.**
- Pottery shelves stand at (9..11, 0..2). Row 2 is `MB_SHOP_SHELF`.
- Dyed cloth hangs at x=1 (purple), x=5 (blue) and x=8 (saffron), and herbs at x=6..7, all in rows 0–1.

**Goods.**
- Baskets: grain (0,3), olives (0,4), figs (10,3), pomegranates (11,3).
- The amphora is at (12, 3..4).
- Jars are at (0, 7..8) and (12, 7..8). The bottom cells answer as vases.
- The money-changer's table (trapeza) is at (6..7, 4..5).

**The stoa colonnade.**
- Columns stand at x=1, 4, 8 and 11, rows 5–7, with solid bases in row 7.
- The way from the door to the stall runs between them.
- The two customers fit at (9,3) by the shelves and at (5,6) by the colonnade.

## Elaia Akademia (16×13)

```text
    0123456789012345
  0 ################
  1 ######MM########
  2 .....#......BBBB
  3 ........#KKK#...
  4 ....#.#.=====...
  5 .##.............
  6 ................
  7 .##...##...##...
  8 ....#.##...##...
  9 ......#....#...#
 10 .............###
 11 ##..........####
 12 ....#.....D....#
```

**Exit.** Mat at (10,12). Warp to the Elaia Village Akademia door at (7,16).
- From the mat, the aisle x=8..10 runs clear to the table.

**Daphne's table and the three kraters.**
- Daphne stands at (10,2), behind the long table.
- The table top is (8..12, 3) and its front is (8..12, 4), both solid.
- The kraters each have their own cell:

  | Krater | Cell | Metatile |
  |---|---|---|
  | Snivy | (9,3) | `aka_krater_snivy` `0x2AC` |
  | Cyndaquil | (10,3) | `aka_krater_cyndaquil` `0x2AD` |
  | Piplup | (11,3) | `aka_krater_piplup` `0x2AE` |

- **To hide a krater,** set its cell to the bare table, `aka_table_m` (`0x2AA`):
  - On map load, in an `ON_LOAD` script that checks the `FLAG_ICHOR_HIDE_KRATER_*` flags: `setmetatile 9, 3, 0x2AA, TRUE`.
  - During the scene, follow it with `special DrawWholeMapView`.
- **Option B.** If the starters are chosen FRLG-style, the player faces the table front from row 5. The krater BG events go on (9,4), (10,4) and (11,4), the cells in front of each krater.
- **Talking to Daphne.** The table is two rows deep, so `MB_COUNTER` can't reach her across it.
  - For her later lines, move her to a table end such as (7,3) or (13,3), or have the player approach from the side.
  - In the cutscenes the player walks up to row 5 or 6. Beat 3's "two tiles below the table" is row 6.

**Alethea and the scrolls.**
- She catalogs at the scroll cabinets, (12..15, 0..2). Stand her at (13,3) or (14,3) facing up.
- Row 2 is `MB_BOOKSHELF`. Put the script's bookshelf BG event ("Every myth is a memory of a Pokémon") on any of (12..15, 2).

**The wall map.**
- The map is at (6..7, 0..1). Its BG events go on (6,1) and (7,1), read from (6,2) or (7,2).
- Kalliste is the gold speck by the arrow, bottom left. The script says "green dot"; see the note in `TILES_civic.md`.

**Around the hall.**
- Specimen jars at (5, 1..2).
- The armillary sphere at (6, 3..4), with its sphere drawn over walkers and a solid base at (6,4).
- Writing desks at (6..7, 7..8) and (11..12, 7..8), with stools at (6,9) and (11,9).

**Alethea's corner of dig finds.**
- Worktable (13..14, 10..11), crate (15,9), amphora (15, 10..11), marble head (12,11) and pick (15,12).

**The grove.**
- x=0..3, behind the cypress hedge.
- Two laurels: canopies at (1..2, 3..4) and (0..1, 9..10), trunks solid at (1..2, 5) and (0..1, 11).
- A marble bench at (1..2, 7).

**The colonnade.**
- Columns stand on the stylobate at x=4, rows 2–4, 6–8 and 10–12, with solid bases at (4,4), (4,8) and (4,12).
- The way into the grove is through (4,5), (4,9), or any column's shaft row.
