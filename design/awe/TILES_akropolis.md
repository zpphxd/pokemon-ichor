# akropolis tileset catalog

`gTileset_Akropolis` is the Akropolis of Astyra. It serves Astyra_Akropolis, paired with the `aethos` primary (open grass, paths, sand, sea, olives, cypresses, stelai, herms).

**Generated** by `tools/ichor/art/astyra_build.py akropolis`; the art is `tools/ichor/art/astyra_art.py` and `astyra_city_art.py`, every column from the shared kit `tools/ichor/art/columns.py` (STYLE.md, "Architecture: Gen 3 craft and Greek forms").

**Budget:** 494 of 504 tiles, 480 metatiles. Palettes (secondary slots 6-12): marble, bronze, ruin, rock, green.

Images: `design/phase4/img/akropolis_pieces.png` (every piece on its ground) and `design/phase4/img/akropolis_sheet.png` (the numbered sheet).

Walk codes: `X` solid, `.` walkable, `T` walkable and drawn over the player.


## rock

### `cliff` (5 x 3): the Akropolis cliff

The Akropolis rock's face, three cells tall: `lip` (`lip_b`) along the top of the drop, `face` (`face_b`, `face_bush`) below it, `foot` (`foot_b`) on the lower ground with the cast shadow; `_W` and `_E` ends; `lip_in_W` `lip_in_E` where the rim turns north; `rock` is solid bare rock. All solid.

`lip` 0x200, `lip_b` 0x201, `lip_W` 0x202, `lip_E` 0x203, `lip_in_W` 0x204, `lip_in_E` 0x208, `face` 0x209, `face_b` 0x20A, `face_W` 0x20B, `face_E` 0x20C, `rock` 0x210, `foot` 0x211, `foot_b` 0x212, `foot_W` 0x213, `foot_E` 0x214

### `edge` (6 x 1): the plateau's rims and the north wall

The plateau's rims: `edge_W` and `edge_E` (the drop off-map), and the north wall, top `wall_N` (`wall_N_drums`) over face `wall_N_face` (`wall_N_face_d`, with old column drums built in). All solid.

`edge_W` 0x218, `edge_E` 0x219, `wall_N` 0x21A, `wall_N_drums` 0x21B, `wall_N_face` 0x21C, `wall_N_face_d` 0x21D

### `ramp` (7 x 2): the ramp's retaining walls and stairs

`cap_L` 0x220, `cap` 0x221, `cap_R` 0x222, `stair_top_L` 0x223, `stair_top` 0x224, `stair_top_R` 0x225, `post` 0x226, `wall_L` 0x228, `wall` 0x229, `wall_R` 0x22A, `stair_L` 0x22B, `stair` 0x22C, `stair_R` 0x22D


## monuments

### `parthenon` (14 x 8): the Parthenon

The Parthenon (14 x 8) on borrowed path: an octastyle Doric front with painted capitals, a blue-and-red triglyph frieze, gold shields on the architrave, a sculpted pediment and gold akroteria, on a krepis of three steps. Solid; stand the player on the row below it (the shadow is drawn into row 7).

Top-left id 0x238; cells by `r<row>c<col>` or position.

### `promachos` (4 x 9): Athena Promachos

Athena Promachos, bronze, 4 x 9 on borrowed path: the Attic helmet and its red crest, a face that reads at 1x (brows, inlaid eyes, nose, mouth), the aegis with the gorgoneion, the owl shield on her left arm, the spear in her right hand with its gold tip (the gleam sailors saw from Sounion; animation `glint` on r0c0), the peplos in folds of five value steps. Rows 0-6 are drawn over the player (T); rows 7-8 are the marble plinth in 3/4 with its cast shadow (X).

Top-left id 0x2B8; cells by `r<row>c<col>` or position.

### `erechtheion` (10 x 7): the Erechtheion

The Erechtheion (10 x 7) on borrowed path: the Ionic east porch with painted capitals and its dark-stone frieze of white figures, the bronze doors, and the Porch of the Maidens (cells 6-9) on its high podium. Solid.

Top-left id 0x300; cells by `r<row>c<col>` or position.

### `propylaia` (13 x 7): the Propylaia

The Propylaia (13 x 7): six Doric columns (painted) at a 32 px pitch, a doorway behind every gap, and the passage up column 6, walkable: its floor is drawn on the bottom layer and the lintel and pediment over the player. Rows 0-3 of column 6 sit on borrowed path. Everything else is solid.

Top-left id 0x338; cells by `r<row>c<col>` or position.

### `altar` (3 x 2): an altar

An altar (3 x 2): a marble block with corner horns, a garland and the fire's soot, its shadow on the floor; solid. It stands outside, in front of the temple.

`L` 0x2BC, `M` 0x2BD, `R` 0x2BE, `BL` 0x2C4, `B` 0x2C5, `BR` 0x2C6

### `spring` (5 x 1): Poseidon's marks and the salt spring

Poseidon's marks: `trident` (read it), `well_shut` and `well_open` (the salt spring's stone, shut and opened: a door down to the Salt Well), `cleft` (the spring stair's crack) and `rubble` (the cleft after the raid). Scripts swap them: METATILE_Akropolis_WellOpen, METATILE_Akropolis_Rubble.

`trident` 0x3A8, `well_shut` 0x3A9, `well_open` 0x3AA, `cleft` 0x3AB, `rubble` 0x3AC


## ruins

### `foundations` (4 x 3): the Old Temple's foundations

`TL` 0x3B8, `T` 0x3B9, `TR` 0x3BA, `L` 0x3C0, `C` 0x3C1, `R` 0x3C2, `BL` 0x3C8, `B` 0x3C9, `BR` 0x3CA, `crack` 0x3BB, `crack_b` 0x3C3, `step` 0x3CB

### `old_columns` (2 x 4): two standing columns of the Old Temple

Two moss-weathered Doric columns (2 x 4) with one architrave block still across them: the Old Temple, burned long ago. Rows 0-2 over the player, bases solid.

`TL` 0x3BC, `TR` 0x3BD, `UL` 0x3C4, `UR` 0x3C5, `ML` 0x3CC, `MR` 0x3CD, `BL` 0x3D4, `BR` 0x3D5

### `ruins` (5 x 1): fallen column pieces (moss)

`stub` 0x3D8, `drum` 0x3D9, `cap_doric` 0x3DA, `plinth_feet` 0x3DB, `poppies` 0x3DC

### `col_moss3` (1 x 3): doric column (moss, 3 tall)

`cap` 0x3BE, `shaft` 0x3C6, `base` 0x3CE
