# Temple of Dionysus tileset: `temple_dionysus`

<!-- catalog: written by tools/ichor/art/temple_dionysus_build.py; do not edit by hand -->

## Catalog

176 metatiles from 0x200; **439 of 504 tiles used** (the door animations own 504-511). Walk codes: `X` blocks, `.` walkable, `S` MB_SOUTH_ARROW_WARP (the doormat). Every other metatile is MB_NORMAL; the puzzle is all script.

### Floors: the wings, the stage, the roof, the orchestra

`floor`, 8 wide by 3 tall. `planks` are the wings' dark backstage boards (`_b`, `_knot` and `_worn` to break a run). `stage` is the stage's wide honey-coloured boards (`stage_gilt` has a gilt inlay, for Act III; `stage_mark` a chalk cross where an actor stands); `stage_lamp` is a footlight, a clay lamp burning at the stage's front edge (blocks; `_gilt` for Act III). `deck` is the skene roof's weathered planks, laid north-south; `deck_edge` is the roof's front row, its lip dropping to the audience; `deck_ivy` a pot of ivy and `deck_crate` Thespis's empty mask crate on the roof. `flag` paves the orchestra. `void` blocks: the border.

```text
ids                                                walk
0x200 0x201 0x202 0x203 0x204 0x205 0x206 0x207   . . . . . . . .
0x208 0x209 0x20A 0x20B 0x20C 0x20D 0x20E 0x20F   X . . . . . . .
0x210 0x211 0x212 0x213 0x214 0x215 0x216 0x217   X X X X X X X X
```

Pieces: `planks` 0x200, `planks_b` 0x201, `planks_knot` 0x202, `planks_worn` 0x203, `stage` 0x204, `stage_b` 0x205, `stage_gilt` 0x206, `stage_mark` 0x207, `void` 0x208, `flag` 0x209, `flag_b` 0x20A, `flag_c` 0x20B, `deck` 0x20C, `deck_b` 0x20D, `deck_edge` 0x20E, `deck_edge_b` 0x20F, `stage_lamp` 0x210, `deck_ivy` 0x211, `deck_crate` 0x212.

### The temple's walls: caps, corners, side walls

`wall`, 8 wide by 1 tall. `cap` is the top of a wall seen from above, with a gilt cornice on its south edge; every room's north wall starts with it. `side_l`/`side_r` run down the map's edges. `cap_end_l` is the cap ending with an opening to its left, `cap_end_r` an opening to its right (the parodos, a stair's top). `cap_gap` is the walkable floor of an opening through a cap row.

```text
ids                                                walk
0x218 0x219 0x21A 0x21B 0x21C 0x21D 0x21E 0x21F   X X X X X X X .
```

Pieces: `cap` 0x218, `cap_corner_l` 0x219, `cap_corner_r` 0x21A, `side_l` 0x21B, `side_r` 0x21C, `cap_end_l` 0x21D, `cap_end_r` 0x21E, `cap_gap` 0x21F.

### The frieze: the god's revel in black figure

`frieze`, 8 wide by 1 tall. The temple's wall face, a gold band painted in black figure like a wine cup: `ivy` and `grapes` between the revellers, `kantharos` (the god's cup), `panther`, `maenad` (with her thyrsus), `satyr`. Hang it under a `cap`. `jamb_l` ends the wall at an opening to its left, `jamb_r` to its right.

```text
ids                                                walk
0x220 0x221 0x222 0x223 0x224 0x225 0x226 0x227   X X X X X X X X
```

Pieces: `ivy` 0x220, `kantharos` 0x221, `panther` 0x222, `maenad` 0x223, `satyr` 0x224, `grapes` 0x225, `jamb_l` 0x226, `jamb_r` 0x227.

### Back walls behind the audience

`back`, 5 wide by 2 tall. The wall each act's audience sits against, under a `cap`. Act I's is plain wine plaster (`act1_garland` hung with an ivy garland); Act II's is hung with painted masks (`act2_masks` the comic, `_b` the tragic). Act III's is the front of the skene roof, carved and gilt (`deck_face`, with gilt masks); `deck_face_arm` is the cell under the god-machine, and `deck_face_arm_lowered` (+1) the same with the boom swung down over it, its pulley and rope.

```text
ids                              walk
0x228 0x229 0x22A 0x22B 0x22C   X X X X X
0x230 0x231 0x232 0x233 0x234   X X X X X
```

Pieces: `act1` 0x228, `act1_garland` 0x229, `act2` 0x22A, `act2_masks` 0x22B, `act2_masks_b` 0x22C, `deck_face` 0x230, `deck_face_masks` 0x231, `deck_face_garland` 0x232, `deck_face_arm` 0x233, `deck_face_arm_lowered` 0x234.

### Act I's set seen from the wings

`skene1`, 6 wide by 1 tall. Rough timber and canvas, the back of a travelling set. Three rows: `cap` (the top beam, seen from the stage), `upper`, `lower` (`_b` braced, or with ivy painted through the canvas). `cap_gap` is the way through the cap over a real door: walkable.

```text
ids                                    walk
0x238 0x239 0x23A 0x23B 0x23C 0x23D   X . X X X X
```

Pieces: `cap` 0x238, `cap_gap` 0x239, `upper` 0x23A, `upper_b` 0x23B, `lower` 0x23C, `lower_b` 0x23D.

### Act II's set seen from the wings

`skene2`, 8 wide by 1 tall. A painted palace front: red panels in ochre frames between blue bands (`_b` with a rosette or painted ivy). `upper_end` and `lower_end` finish the set's east end, by the satyrs' corner.

```text
ids                                                walk
0x240 0x241 0x242 0x243 0x244 0x245 0x246 0x247   X . X X X X X X
```

Pieces: `cap` 0x240, `cap_gap` 0x241, `upper` 0x242, `upper_b` 0x243, `lower` 0x244, `lower_b` 0x245, `upper_end` 0x246, `lower_end` 0x247.

### Act III's set seen from the wings

`skene3`, 6 wide by 1 tall. The marble skene, the grandest: ashlar under a gilt band, ivy carved low (`_b` is a fluted pilaster, upper and lower).

```text
ids                                    walk
0x248 0x249 0x24A 0x24B 0x24C 0x24D   X . X X X X
```

Pieces: `cap` 0x248, `cap_gap` 0x249, `upper` 0x24A, `upper_b` 0x24B, `lower` 0x24C, `lower_b` 0x24D.

### The three doors, and Act I's painted two

`doors`, 5 wide by 2 tall. A real door is `<kind>_upper` (its sign on the lintel: an ivy garland with grapes, a gilt crown, goat horns) over the doorway `<kind>`, both walkable: put the entrance's coord event on the doorway, and the act's `cap_gap` above the upper cell. The doorway is dark under a wine-red valance, its curtain tied back, and the stage's light lies on the boards beyond. Act I's crown and goat doors are only painted on its canvas (`*_painted_upper` over `*_painted`): both block.

```text
ids                              walk
0x250 0x251 0x252 0x253 0x254   . . . . .
0x258 0x259 0x25A 0x25B 0x25C   . X X X X
```

Pieces: `ivy_upper` 0x250, `crown_upper` 0x251, `goat_upper` 0x252, `ivy` 0x253, `crown` 0x254, `goat` 0x258, `crown_painted_upper` 0x259, `goat_painted_upper` 0x25A, `crown_painted` 0x25B, `goat_painted` 0x25C.

### The mask rack: pegs, full or empty

`rack`, 6 wide by 1 tall. Hang the rack on a skene's `lower` row, one cell per mask, faced from the wings. Each peg is a little oak board; `<mask>_empty` (= the full peg + 1) is the same peg with its mask gone, for the mask the player is wearing. Act I's rack is the comic peg alone.

```text
ids                                    walk
0x260 0x261 0x262 0x263 0x264 0x265   X X X X X X
```

Pieces: `comic` 0x260, `comic_empty` 0x261, `tragic` 0x262, `tragic_empty` 0x263, `satyr` 0x264, `satyr_empty` 0x265.

### The audience: clay votive figures on stone tiers

`audience`, 7 wide by 2 tall. Two tiers along each act's back wall: a `back_*` row against the wall and a `front_*` row before it, each in three arrangements. The audience is clay votives, two to a seat, with painted hair, white faces, ivy wreaths, red robes, and their mouths open. `*_end_l`/`*_end_r` finish a run beside a stair. Under the god-machine: `back_arm`/`front_arm`, and `*_lowered` (+1) with its rope hanging down over the figures.

```text
ids                                          walk
0x268 0x269 0x26A 0x26B 0x26C 0x26D 0x26E   X X X X X X X
0x270 0x271 0x272 0x273 0x274 0x275 0x276   X X X X X X X
```

Pieces: `back_a` 0x268, `back_b` 0x269, `back_c` 0x26A, `front_a` 0x26B, `front_b` 0x26C, `front_c` 0x26D, `back_end_l` 0x26E, `front_end_l` 0x270, `back_end_r` 0x271, `front_end_r` 0x272, `back_arm` 0x273, `back_arm_lowered` 0x274, `front_arm` 0x275, `front_arm_lowered` 0x276.

### The curtained stair: up from a stage to the next act's wings

`stair`, 2 wide by 5 tall. Two cells wide, five rows from the next act's wall `cap` (`top`) down through its back wall (`through`) and past the audience (`steps`) to the stage (`foot`). The curtain hangs at the foot: `foot_closed_*` blocks; `foot_open_*` is the same stair with the curtain drawn back and tied, walkable.

```text
ids            walk
0x278 0x279   . .
0x280 0x281   . .
0x288 0x289   . .
0x290 0x291   X X
0x298 0x299   . .
```

Pieces: `top_l` 0x278, `top_r` 0x279, `through_l` 0x280, `through_r` 0x281, `steps_l` 0x288, `steps_r` 0x289, `foot_closed_l` 0x290, `foot_closed_r` 0x291, `foot_open_l` 0x298, `foot_open_r` 0x299.

### The skene roof and the god-machine

`machine`, 8 wide by 2 tall. On the roof (`deck` boards): the crane's `mast_top` over `mast`, its `winch` beside it, and in front, on the roof's edge, `arm`. Each has a `_lowered` twin (+1): raised, the boom stands up against the mast; lowered, it swings forward over the audience, over the player's head on the edge (drawn in the top layer), past `deck_face_arm`, and lets its rope down the tiers' `*_arm` cells to `hook_lowered` on the stage (`hook` is plain stage boards; lowered, it blocks: face it to hold on). Props: the thunder machine (`bronteion_top` over `bronteion`), a `rope_coil`, `amphorae`, an `edge_post`, a `lamp_post`, and the Hierophant's `throne`.

```text
ids                                                walk
0x2A0 0x2A1 0x2A2 0x2A3 0x2A4 0x2A5 0x2A6 0x2A7   X X X X . . . X
0x2A8 0x2A9 0x2AA 0x2AB 0x2AC 0x2AD 0x2AE 0x2AF   X X X X X X X X
```

Pieces: `mast_top` 0x2A0, `mast_top_lowered` 0x2A1, `mast` 0x2A2, `mast_lowered` 0x2A3, `arm` 0x2A4, `arm_lowered` 0x2A5, `hook` 0x2A6, `hook_lowered` 0x2A7, `winch` 0x2A8, `bronteion_top` 0x2A9, `bronteion` 0x2AA, `rope_coil` 0x2AB, `amphorae` 0x2AC, `edge_post` 0x2AD, `lamp_post` 0x2AE, `throne` 0x2AF.

### The god's orchestra: the dancing floor round the great altar

`orchestra`, 5 wide by 4 tall. Five by four. A round dancing floor of pale marble, ringed in grey, on the orchestra's flags; the great altar of Dionysus stands in the middle (the inner 3 x 2, blocking): a marble table with scrolled ends, hung with ivy, its top stained with wine, a black kantharos and a bunch of grapes on it, a panther carved on its front. Place it whole; `r<row><col>` names each cell. The block is drawn symmetric, so its right half costs no tiles.

```text
ids                              walk
0x27A 0x27B 0x27C 0x27D 0x27E   . . . . .
0x282 0x283 0x284 0x285 0x286   . X X X .
0x28A 0x28B 0x28C 0x28D 0x28E   . X X X .
0x292 0x293 0x294 0x295 0x296   . . . . .
```

Pieces: `r00` 0x27A, `r01` 0x27B, `r02` 0x27C, `r03` 0x27D, `r04` 0x27E, `r10` 0x282, `r11` 0x283, `r12` 0x284, `r13` 0x285, `r14` 0x286, `r20` 0x28A, `r21` 0x28B, `r22` 0x28C, `r23` 0x28D, `r24` 0x28E, `r30` 0x292, `r31` 0x293, `r32` 0x294, `r33` 0x295, `r34` 0x296.

### The entry: the god's image's base, torches, the doormat

`entry`, 7 wide by 2 tall. `base` is the low stone base inside the door where the god's old wooden image stands (an object on top of it). `torch_top` over `torch`: a tall bronze torch, burning. `krater`: a wine krater painted in black figure. `ivy_pot`. `thyrsoi_top` over `thyrsoi`: a stand of ivy-tipped staves. `bench_l`/`bench_r` a marble bench. `jars` two wine jars. The doormat (`mat_l`, `mat`, `mat_r`) is MB_SOUTH_ARROW_WARP: a warp on each.

```text
ids                                          walk
0x2B0 0x2B1 0x2B2 0x2B3 0x2B4 0x2B5 0x2B6   X X X X X X X
0x2B8 0x2B9 0x2BA 0x2BB 0x2BC 0x2BD 0x2BE   S S S X X X .
```

Pieces: `base` 0x2B0, `torch_top` 0x2B1, `torch` 0x2B2, `krater` 0x2B3, `ivy_pot` 0x2B4, `thyrsoi_top` 0x2B5, `thyrsoi` 0x2B6, `mat_l` 0x2B8, `mat` 0x2B9, `mat_r` 0x2BA, `bench_l` 0x2BB, `bench_r` 0x2BC, `jars` 0x2BD.

### The wings: the program, trunks, rails and the satyrs' corner

`wings`, 8 wide by 2 tall. `program` is the act's program on a reading stand (`program_torn`: Act III's, the scroll torn off below). A costume `trunk_l`/`_r`, a costume `rail_l`/`_r` hung with robes, a `basket` of props, stacked scenery `flats`, an oil `lamp` on a stand, a `stool`, a `wigs` stand. The satyrs' corner (Act II's alcove): its back wall hung with goatskins (`goatskins_l`, `goatskins`, `goatskins_r`) under a `cap`, a `hay` bale, and `corner_planks` to walk on.

```text
ids                                                walk
0x2C0 0x2C1 0x2C2 0x2C3 0x2C4 0x2C5 0x2C6 0x2C7   X X X X X X X X
0x2C8 0x2C9 0x2CA 0x2CB 0x2CC 0x2CD 0x2CE 0x2CF   X X X X X X . X
```

Pieces: `program` 0x2C0, `program_torn` 0x2C1, `trunk_l` 0x2C2, `trunk_r` 0x2C3, `rail_l` 0x2C4, `rail_r` 0x2C5, `basket` 0x2C6, `flats` 0x2C7, `lamp` 0x2C8, `stool` 0x2C9, `goatskins_l` 0x2CA, `goatskins` 0x2CB, `goatskins_r` 0x2CC, `hay` 0x2CD, `corner_planks` 0x2CE, `wigs` 0x2CF.

<!-- end of catalog -->
