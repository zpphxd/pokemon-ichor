# astyra tileset catalog

`gTileset_Astyra` is Astyra, the capital. It serves Astyra, Astyra_Harbor, paired with the `aethos` primary (open grass, paths, sand, sea, olives, cypresses, stelai, herms).

**Generated** by `tools/ichor/art/astyra_build.py astyra`; the art is `tools/ichor/art/astyra_art.py` and `astyra_city_art.py`, every column from the shared kit `tools/ichor/art/columns.py` (STYLE.md, "Architecture: Gen 3 craft and Greek forms").

**Budget:** 497 of 504 tiles, 344 metatiles. Palettes (secondary slots 6-12): marble, bronze, ruin, rock, roof, green, water.

Images: `design/phase4/img/astyra_pieces.png` (every piece on its ground) and `design/phase4/img/astyra_sheet.png` (the numbered sheet).

Walk codes: `X` solid, `.` walkable, `T` walkable and drawn over the player.


## rock

### `skyline_parthenon` (14 x 4): the Parthenon over the wall

The Parthenon's pediment, frieze and capitals over the Akropolis wall (14 x 4; the same art as gTileset_Akropolis). Solid.

Top-left id 0x200; cells by `r<row>c<col>` or position.

### `skyline_promachos` (4 x 5): Athena Promachos over the wall

Promachos from the city (4 x 5): crest, helmet, aegis, the owl shield and the spear with its gleaming tip (animation `glint`), standing behind the Akropolis wall. Solid scenery.

Top-left id 0x240; cells by `r<row>c<col>` or position.

### `cliff` (4 x 3): the Akropolis cliff

The rock's face from the city, under the Akropolis wall: `face` `face_b` (repeat them), `foot` `foot_b` on the grass with the cast shadow, `_W` and `_E` ends, `rock` solid. All solid.

`face` 0x244, `face_b` 0x245, `face_W` 0x246, `face_E` 0x247, `foot` 0x24C, `foot_b` 0x24D, `foot_W` 0x24E, `foot_E` 0x24F, `rock` 0x254

### `akro_wall` (7 x 1): the Akropolis wall

The Akropolis wall along the rock's top (`L` `M` `M_b` `R`, `M_b` with a re-used block), and `gate`, the door up to the Propylaia between `gate_L` and `gate_R`.

`L` 0x268, `M` 0x269, `M_b` 0x26A, `R` 0x26B, `gate_L` 0x26C, `gate` 0x26D, `gate_R` 0x26E

### `rock_stair` (2 x 1): the rock-cut stair

`face` 0x226, `foot` 0x227


## town

### `stoa` (6 x 5): the Stoa of the Archon

Top-left id 0x278; cells by `r<row>c<col>` or position.

### `library` (7 x 5): the Library of Astyra

The Library (7 x 5): Astyra's one Corinthian building, bronze capitals, a pediment with a gold scroll-case relief. Door at r3c3; r4c3 is its walkable step.

Top-left id 0x2A0; cells by `r<row>c<col>` or position.

### `asclepeion` (5 x 4): the Asclepeion

The Asclepeion (5 x 4) on borrowed grass: terracotta roof, an Ionic porch in antis, the snake-staff over the door (r3c2).

`r0c0` 0x2C8, `r0c1` 0x2C9, `r0c2` 0x2CA, `r0c3` 0x2CB, `r0c4` 0x2CC, `r1c0` 0x2D0, `r1c1` 0x2D1, `r1c2` 0x2D2, `r1c3` 0x2D3, `r1c4` 0x2D4, `r2c0` 0x2D8, `r2c1` 0x2D9, `r2c2` 0x2DA, `r2c3` 0x2DB, `r2c4` 0x2DC, `r3c0` 0x2E0, `r3c1` 0x2E1, `r3c2` 0x2E2, `r3c3` 0x2E3, `r3c4` 0x2E4

### `house` (6 x 3): courtyard houses

`RT_L` 0x2E8, `RT_M` 0x2E9, `RT_R` 0x2EA, `F_L` 0x2EB, `F_M` 0x2EC, `F_R` 0x2ED, `RB_L` 0x2F0, `RB_M` 0x2F1, `RB_R` 0x2F2, `U_L` 0x2F3, `U_M` 0x2F4, `U_R` 0x2F5, `W_L` 0x2F8, `W_M` 0x2F9, `W_R` 0x2FA, `W_win` 0x2FB, `door` 0x2FC, `W_jar` 0x2FD

### `city_wall` (7 x 2): the city wall

The city wall: `v` runs north-south (seen from above), `h_top` over `h_face` east-west; towers 2 x 2; `gate_top` is a lintel drawn over the player above a walkable gap; `gate_face` is a wall face with the gap open.

`v` 0x300, `v_end_N` 0x301, `v_end_S` 0x302, `tower_TL` 0x303, `tower_TR` 0x304, `h_top` 0x305, `h_L` 0x306, `h_R` 0x308, `tower_BL` 0x309, `tower_BR` 0x30A, `h_face` 0x30B, `h_face_b` 0x30C, `gate_top` 0x30D, `gate_face` 0x30E

### `fountain` (3 x 3): the fountain house

The fountain house (3 x 3): a Doric porch and a pediment, the bronze lion's head pouring into the marble basin (animation `spout`). Solid; read it from the front.

`r0c0` 0x2CD, `r0c1` 0x2CE, `r0c2` 0x2CF, `r1c0` 0x2D5, `r1c1` 0x2D6, `r1c2` 0x2D7, `r2c0` 0x2DD, `r2c1` 0x2DE, `r2c2` 0x2DF

### `kodros` (2 x 3): Kodros, the last king

Kodros, the last king (2 x 3): bronze on a hexagonal 3/4 marble plinth, its cast shadow on the floor. Rows 0-1 over the player, the plinth solid; the bg event is on the plinth.

`TL` 0x27E, `TR` 0x27F, `ML` 0x286, `MR` 0x287, `BL` 0x28E, `BR` 0x28F

### `kairos` (2 x 3): Kairos, the Moment

Kairos, the Moment (2 x 3): bronze on a hexagonal 3/4 marble plinth, its cast shadow on the floor. Rows 0-1 over the player, the plinth solid; the bg event is on the plinth.

`TL` 0x2E6, `TR` 0x2E7, `ML` 0x2EE, `MR` 0x2EF, `BL` 0x2F6, `BR` 0x2F7

### `altar` (3 x 2): an altar

An altar (3 x 2): a marble block with corner horns, a garland and the fire's soot, its shadow on the floor; solid. It stands outside, in front of the temple.

`L` 0x310, `M` 0x311, `R` 0x312, `BL` 0x318, `B` 0x319, `BR` 0x31A

### `stall` (2 x 2): a market stall

`TL` 0x296, `TR` 0x297, `BL` 0x29E, `BR` 0x29F

### `bema` (3 x 2): the speaker's platform

The bema on the Pnyx (3 x 2), cut from the rock; solid. A sign on its front (the vista).

`L` 0x313, `M` 0x314, `R` 0x315, `BL` 0x31B, `B` 0x31C, `BR` 0x31D

### `kerameikos` (3 x 1): fallen column pieces (marble)

The Kerameikos's broken grave monuments, on borrowed grass: `stub`, `plinth_feet`, `drum` (solid), `poppies` (walkable).

`stub` 0x320, `plinth_feet` 0x321, `poppies` 0x322


## harbor

### `quay` (8 x 2): the harbor quay

The quay over borrowed sea: `N` (the quay to the north, its lit edge, the wet foot), corners, `W` `E` `S` edges; on the quay: `bollard`, `ring`; `steps` go down into the water (walkable).

`N` 0x330, `NW` 0x331, `NE` 0x332, `W` 0x333, `E` 0x334, `S` 0x335, `SW` 0x336, `SE` 0x337, `bollard` 0x338, `steps` 0x339, `ring` 0x33A

### `ship_shed` (3 x 3): a ship shed

A ship shed (3 x 3) at the water: a tiled roof on stone piers, the slip's timber ways running down into the dark, a ram's bronze. Solid; set its bottom row at the waterline.

`r0c0` 0x340, `r0c1` 0x341, `r0c2` 0x342, `r1c0` 0x348, `r1c1` 0x349, `r1c2` 0x34A, `r2c0` 0x350, `r2c1` 0x351, `r2c2` 0x352

### `sea_door` (1 x 2): the sea-door

The salt spring's sealed sea-door in the harbor rock (1 x 2). Solid; the bg event sits on `door`.

`top` 0x343, `door` 0x34B
