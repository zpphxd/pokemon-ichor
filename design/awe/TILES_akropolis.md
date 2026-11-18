# akropolis tileset catalog

`gTileset_Akropolis` is the Akropolis of Astyra. It serves Astyra_Akropolis, paired with the `aethos` primary (open grass, paths, sand, sea, olives, cypresses, stelai, herms).

**Generated** by `tools/ichor/art/astyra_build.py akropolis`; the art is `tools/ichor/art/astyra_art.py` and `astyra_city_art.py`, every column from the shared kit `tools/ichor/art/columns.py` (STYLE.md, "Architecture: Gen 3 craft and Greek forms").

**Budget:** 501 of 504 tiles, 424 metatiles. Palettes (secondary slots 6-12): marble, bronze, ruin, rock, green.

Images: `design/phase4/img/akropolis_pieces.png` (every piece on its ground) and `design/phase4/img/akropolis_sheet.png` (the numbered sheet).

Walk codes: `X` solid, `.` walkable, `T` walkable and drawn over the player.


## akropolis

### `parthenon` (14 x 8): the Parthenon

The Parthenon (14 x 8) on borrowed path: an octastyle Doric front with painted capitals, a blue-and-red triglyph frieze, gold shields on the architrave, a sculpted pediment and gold akroteria, on a krepis of three steps. Solid; stand the player on the row below it (the shadow is drawn into row 7).

Top-left id 0x200; cells by `r<row>c<col>` or position.

### `promachos` (4 x 9): Athena Promachos

Athena Promachos, bronze, 4 x 9 on borrowed path, in contrapposto: the spear raised in her right fist, held clear of her body, its gold tip the gleam sailors saw from Sounion (animation `glint` on r0c0); the owl shield held out on her left arm; the Corinthian helmet pushed back on her crown with its red crest, showing her face; the aegis with the gorgoneion; the peplos in four big folds, the free knee lit. Rows 0-6 are drawn over the player (T); rows 7-8 are the hexagonal marble plinth in 3/4 with its cast shadow (X).

Top-left id 0x280; cells by `r<row>c<col>` or position.

### `erechtheion` (10 x 7): the Erechtheion

The Erechtheion (10 x 7) on borrowed path: the Ionic east porch with painted capitals and its dark-stone frieze of white figures, the bronze doors, and the Porch of the Maidens (cells 6-9) on its high podium. Solid.

Top-left id 0x2C8; cells by `r<row>c<col>` or position.

### `propylaia` (13 x 7): the Propylaia

The Propylaia (13 x 7): six Doric columns (painted) at a 32 px pitch, a doorway behind every gap, and the passage up column 6, walkable: its floor is drawn on the bottom layer and the lintel and pediment over the player. Rows 0-3 of column 6 sit on borrowed path. Everything else is solid.

Top-left id 0x300; cells by `r<row>c<col>` or position.

### `old_columns` (2 x 4): two standing columns of the Old Temple

Two moss-weathered Doric columns (2 x 4) with one architrave block still across them: the Old Temple, burned long ago. Rows 0-2 over the player, bases solid.

`TL` 0x27E, `TR` 0x27F, `UL` 0x286, `UR` 0x287, `ML` 0x28E, `MR` 0x28F, `BL` 0x296, `BR` 0x297

### `cliff` (5 x 3): the Akropolis cliff

The Akropolis rock's face, three cells tall: `lip` (`lip_b`) along the top of the drop, `face` (`face_b`, `face_bush`) below it, `foot` (`foot_b`) on the lower ground with the cast shadow; `_W` and `_E` ends; `lip_in_W` `lip_in_E` where the rim turns north; `rock` is solid bare rock. All solid.

`lip` 0x370, `lip_b` 0x371, `lip_W` 0x372, `lip_E` 0x373, `lip_in_W` 0x374, `lip_in_E` 0x378, `face` 0x379, `face_b` 0x37A, `face_W` 0x37B, `face_E` 0x37C, `rock` 0x380, `foot` 0x381, `foot_b` 0x382, `foot_W` 0x383, `foot_E` 0x384

### `foundations` (4 x 3): the Old Temple's foundations

`TL` 0x29C, `T` 0x29D, `TR` 0x29E, `L` 0x2A4, `C` 0x2A5, `R` 0x2A6, `BL` 0x2AC, `B` 0x2AD, `BR` 0x2AE, `crack` 0x29F, `crack_b` 0x2A7, `step` 0x2AF

### `pave` (4 x 3): the paved way

`TL` 0x2B4, `T` 0x2B5, `TR` 0x2B6, `L` 0x2B7, `C` 0x2BC, `R` 0x2BD, `BL` 0x2BE, `B` 0x2BF, `BR` 0x2C4, `C2` 0x2C5

### `col_moss3` (1 x 3): doric column (moss, 3 tall)

`cap` 0x284, `shaft` 0x28C, `base` 0x294

### `ramp` (8 x 2): the ramp's retaining walls and stairs

`cap_L` 0x388, `cap` 0x389, `cap_R` 0x38A, `stair_top_L` 0x38B, `stair_top` 0x38C, `stair_top_R` 0x38D, `cap_pier` 0x38E, `wall_L` 0x38F, `wall` 0x390, `wall_R` 0x391, `stair_L` 0x392, `stair` 0x393, `stair_R` 0x394, `wall_pier` 0x395, `foot_pier` 0x396

### `altar` (3 x 2): an altar

An altar (3 x 2): a marble block with corner horns, a garland and the fire's soot, its shadow on the floor; solid. It stands outside, in front of the temple.

`L` 0x33D, `M` 0x33E, `R` 0x33F, `BL` 0x345, `B` 0x346, `BR` 0x347

### `outcrop` (3 x 2): the bare rock

The bedrock breaking through the plateau (3 x 2): two weathered tiers, each lit on top with a riser below, a cracked south face, scrub in a crevice, its shadow down and right. Solid.

`TL` 0x34D, `T` 0x34E, `TR` 0x34F, `BL` 0x355, `B` 0x356, `BR` 0x357

### `votive` (2 x 2): votive statues

Votives for the processional way (2 x 2): a bronze kouros and a painted marble kore holding out her offering, each on a 3/4 plinth with its shadow. The figure row is drawn over the player; the plinth row is solid.

`kouros_top` 0x35D, `kore_top` 0x35E, `kouros` 0x365, `kore` 0x366

### `brazier` (1 x 2): a lit brazier

A lit bronze brazier (1 x 2): the fire over the player, flickering (animation `flame`), the bowl on three legs and a base plate below, solid.

`fire` 0x285, `stand` 0x28D

### `edge` (6 x 1): the plateau's rims and the north wall

The plateau's rims: `edge_W` and `edge_E` (the drop off-map), and the north wall, top `wall_N` (`wall_N_drums`) over face `wall_N_face` (`wall_N_face_d`, with old column drums built in). All solid.

`edge_W` 0x398, `edge_E` 0x399, `wall_N` 0x39A, `wall_N_drums` 0x39B, `wall_N_face` 0x39C, `wall_N_face_d` 0x39D

### `spring` (5 x 1): Poseidon's marks and the salt spring

Poseidon's marks: `trident` (read it), `well_shut` and `well_open` (the salt spring's stone, shut and opened: a door down to the Salt Well), `cleft` (the spring stair's crack) and `rubble` (the cleft after the raid). Scripts swap them: METATILE_Akropolis_WellOpen, METATILE_Akropolis_Rubble.

`trident` 0x3A0, `well_shut` 0x3A1, `well_open` 0x3A2, `cleft` 0x3A3, `rubble` 0x3A4

### `ruins` (3 x 1): fallen column pieces (moss)

`stub` 0x36D, `drum` 0x36E, `poppies` 0x36F
