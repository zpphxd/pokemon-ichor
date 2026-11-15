# Temple of Artemis tileset: `temple_artemis`

<!-- catalog: written by tools/ichor/art/temple_artemis_build.py; do not edit by hand -->

## Catalog

273 metatiles from 0x200; **438 of 504 tiles used** (the door animations own 504-511). Walk codes: `X` blocks, `.` walkable, `T` walkable and drawn over the player, `S` MB_SOUTH_ARROW_WARP (the doormat). Every other metatile is MB_NORMAL; the hunt is all objects and script.

### Floors: the night lawn, the porch's paving, the door

`floor`, 8 wide by 2 tall. `lawn` is the clipped night lawn (`_b` a second grain; `_tuft` a darker tussock; `_flowers` white asphodel). `lawn_shade` is the lawn under a hedge's face, in its shadow: put it on the row south of every hedge face. `pave` is the porch's marble paving (`_b`, `_c`, `_worn` to break a run; `_moon` a slab in a pool of moonlight; `_shade` under a hedge). The doormat (`mat_l`, `mat_r`) is MB_SOUTH_ARROW_WARP: a warp on each. `void` blocks: the border.

```text
ids                                                walk
0x200 0x201 0x202 0x203 0x204 0x205 0x206 0x207   . . . . . . X .
0x208 0x209 0x20A 0x20B 0x20C 0x20D 0x20E 0x20F   . . . . S S . .
```

Pieces: `lawn` 0x200, `lawn_b` 0x201, `lawn_flowers` 0x202, `lawn_flowers_b` 0x203, `lawn_shade` 0x204, `lawn_shade_b` 0x205, `void` 0x206, `lawn_tuft` 0x207, `pave` 0x208, `pave_b` 0x209, `pave_c` 0x20A, `pave_moon` 0x20B, `mat_l` 0x20C, `mat_r` 0x20D, `pave_shade` 0x20E, `pave_worn` 0x20F.

### Moonlight: pools of pale ground, every shape

`moon`, 8 wide by 6 tall. The lawn where the moon lies on it, clearly brighter: a hound that patrols it sees 6 tiles, not 3. Every one of the 47 blob shapes, named by shape key (`eleusa_lib.blob_key`); `1|11111111` is the middle of a pool. Walkable.

```text
ids                                                walk
0x210 0x211 0x212 0x213 0x214 0x215 0x216 0x217   . . . . . . . .
0x218 0x219 0x21A 0x21B 0x21C 0x21D 0x21E 0x21F   . . . . . . . .
0x220 0x221 0x222 0x223 0x224 0x225 0x226 0x227   . . . . . . . .
0x228 0x229 0x22A 0x22B 0x22C 0x22D 0x22E 0x22F   . . . . . . . .
0x230 0x231 0x232 0x233 0x234 0x235 0x236 0x237   . . . . . . . .
0x238 0x239 0x23A 0x23B 0x23C 0x23D 0x23E 0x23F   . . . . . . . .
```

Pieces: `1|00000000` 0x210, `1|00000010` 0x211, `1|00001000` 0x212, `1|00001010` 0x213, `1|00001110` 0x214, `1|00100000` 0x215, `1|00100010` 0x216, `1|00101000` 0x217, `1|00101010` 0x218, `1|00101110` 0x219, `1|00111000` 0x21A, `1|00111010` 0x21B, `1|00111110` 0x21C, `1|10000000` 0x21D, `1|10000010` 0x21E, `1|10000011` 0x21F, `1|10001000` 0x220, `1|10001010` 0x221, `1|10001011` 0x222, `1|10001110` 0x223, `1|10001111` 0x224, `1|10100000` 0x225, `1|10100010` 0x226, `1|10100011` 0x227, `1|10101000` 0x228, `1|10101010` 0x229, `1|10101011` 0x22A, `1|10101110` 0x22B, `1|10101111` 0x22C, `1|10111000` 0x22D, `1|10111010` 0x22E, `1|10111011` 0x22F, `1|10111110` 0x230, `1|10111111` 0x231, `1|11100000` 0x232, `1|11100010` 0x233, `1|11100011` 0x234, `1|11101000` 0x235, `1|11101010` 0x236, `1|11101011` 0x237, `1|11101110` 0x238, `1|11101111` 0x239, `1|11111000` 0x23A, `1|11111010` 0x23B, `1|11111011` 0x23C, `1|11111110` 0x23D, `1|11111111` 0x23E.

### Gravel walks, every shape

`walk`, 8 wide by 6 tall. Raked gravel walks through the lawn, named by shape key like the moonlight. Walkable.

```text
ids                                                walk
0x240 0x241 0x242 0x243 0x244 0x245 0x246 0x247   . . . . . . . .
0x248 0x249 0x24A 0x24B 0x24C 0x24D 0x24E 0x24F   . . . . . . . .
0x250 0x251 0x252 0x253 0x254 0x255 0x256 0x257   . . . . . . . .
0x258 0x259 0x25A 0x25B 0x25C 0x25D 0x25E 0x25F   . . . . . . . .
0x260 0x261 0x262 0x263 0x264 0x265 0x266 0x267   . . . . . . . .
0x268 0x269 0x26A 0x26B 0x26C 0x26D 0x26E 0x26F   . . . . . . . .
```

Pieces: `1|00000000` 0x240, `1|00000010` 0x241, `1|00001000` 0x242, `1|00001010` 0x243, `1|00001110` 0x244, `1|00100000` 0x245, `1|00100010` 0x246, `1|00101000` 0x247, `1|00101010` 0x248, `1|00101110` 0x249, `1|00111000` 0x24A, `1|00111010` 0x24B, `1|00111110` 0x24C, `1|10000000` 0x24D, `1|10000010` 0x24E, `1|10000011` 0x24F, `1|10001000` 0x250, `1|10001010` 0x251, `1|10001011` 0x252, `1|10001110` 0x253, `1|10001111` 0x254, `1|10100000` 0x255, `1|10100010` 0x256, `1|10100011` 0x257, `1|10101000` 0x258, `1|10101010` 0x259, `1|10101011` 0x25A, `1|10101110` 0x25B, `1|10101111` 0x25C, `1|10111000` 0x25D, `1|10111010` 0x25E, `1|10111011` 0x25F, `1|10111110` 0x260, `1|10111111` 0x261, `1|11100000` 0x262, `1|11100010` 0x263, `1|11100011` 0x264, `1|11101000` 0x265, `1|11101010` 0x266, `1|11101011` 0x267, `1|11101110` 0x268, `1|11101111` 0x269, `1|11111000` 0x26A, `1|11111010` 0x26B, `1|11111011` 0x26C, `1|11111110` 0x26D, `1|11111111` 0x26E.

### Clipped laurel hedges, every shape

`hedge`, 8 wide by 6 tall. The garden's walls: clipped laurel, a flat moonlit top and a dark south face. Named by shape key of the hedge mass (`eleusa_lib.blob_key`). A cell whose south neighbor isn't hedge draws the face; give hedge walls two rows (top, face) so the face sits under a top. Blocks.

```text
ids                                                walk
0x270 0x271 0x272 0x273 0x274 0x275 0x276 0x277   X X X X X X X X
0x278 0x279 0x27A 0x27B 0x27C 0x27D 0x27E 0x27F   X X X X X X X X
0x280 0x281 0x282 0x283 0x284 0x285 0x286 0x287   X X X X X X X X
0x288 0x289 0x28A 0x28B 0x28C 0x28D 0x28E 0x28F   X X X X X X X X
0x290 0x291 0x292 0x293 0x294 0x295 0x296 0x297   X X X X X X X X
0x298 0x299 0x29A 0x29B 0x29C 0x29D 0x29E 0x29F   X X X X X X X X
```

Pieces: `1|00000000` 0x270, `1|00000010` 0x271, `1|00001000` 0x272, `1|00001010` 0x273, `1|00001110` 0x274, `1|00100000` 0x275, `1|00100010` 0x276, `1|00101000` 0x277, `1|00101010` 0x278, `1|00101110` 0x279, `1|00111000` 0x27A, `1|00111010` 0x27B, `1|00111110` 0x27C, `1|10000000` 0x27D, `1|10000010` 0x27E, `1|10000011` 0x27F, `1|10001000` 0x280, `1|10001010` 0x281, `1|10001011` 0x282, `1|10001110` 0x283, `1|10001111` 0x284, `1|10100000` 0x285, `1|10100010` 0x286, `1|10100011` 0x287, `1|10101000` 0x288, `1|10101010` 0x289, `1|10101011` 0x28A, `1|10101110` 0x28B, `1|10101111` 0x28C, `1|10111000` 0x28D, `1|10111010` 0x28E, `1|10111011` 0x28F, `1|10111110` 0x290, `1|10111111` 0x291, `1|11100000` 0x292, `1|11100010` 0x293, `1|11100011` 0x294, `1|11101000` 0x295, `1|11101010` 0x296, `1|11101011` 0x297, `1|11101110` 0x298, `1|11101111` 0x299, `1|11111000` 0x29A, `1|11111010` 0x29B, `1|11111011` 0x29C, `1|11111110` 0x29D, `1|11111111` 0x29E.

### The first hunters' arch: antlers

`arch_antlers`, 4 wide by 3 tall. Set it into a two-row hedge wall: row 0 over the lawn north of the wall (the crown, drawn over the player), row 1 in the wall's top row (the capitals and the lintel, walked under), row 2 in its face row (the posts and the opening). The lawn under the crown is plain `lawn`.

```text
ids                        walk
0x2A0 0x2A1 0x2A2 0x2A3   T T T T
0x2A8 0x2A9 0x2AA 0x2AB   X T T X
0x2B0 0x2B1 0x2B2 0x2B3   X . . X
```

Pieces: `crown_l` 0x2A0, `crown_ml` 0x2A1, `crown_mr` 0x2A2, `crown_r` 0x2A3, `cap_l` 0x2A8, `lintel_l` 0x2A9, `lintel_r` 0x2AA, `cap_r` 0x2AB, `post_l` 0x2B0, `open_l` 0x2B1, `open_r` 0x2B2, `post_r` 0x2B3.

### The second hunters' arch: the bow

`arch_bow`, 4 wide by 3 tall. Set it into a two-row hedge wall: row 0 over the lawn north of the wall (the crown, drawn over the player), row 1 in the wall's top row (the capitals and the lintel, walked under), row 2 in its face row (the posts and the opening). The lawn under the crown is plain `lawn`.

```text
ids                        walk
0x2A4 0x2A5 0x2A6 0x2A7   T T T T
0x2AC 0x2AD 0x2AE 0x2AF   X T T X
0x2B4 0x2B5 0x2B6 0x2B7   X . . X
```

Pieces: `crown_l` 0x2A4, `crown_ml` 0x2A5, `crown_mr` 0x2A6, `crown_r` 0x2A7, `cap_l` 0x2AC, `lintel_l` 0x2AD, `lintel_r` 0x2AE, `cap_r` 0x2AF, `post_l` 0x2B4, `open_l` 0x2B5, `open_r` 0x2B6, `post_r` 0x2B7.

### The third hunters' arch: the crescent moon

`arch_moon`, 4 wide by 3 tall. Set it into a two-row hedge wall: row 0 over the lawn north of the wall (the crown, drawn over the player), row 1 in the wall's top row (the capitals and the lintel, walked under), row 2 in its face row (the posts and the opening). The lawn under the crown is plain `lawn`.

```text
ids                        walk
0x2B8 0x2B9 0x2BA 0x2BB   T T T T
0x2C0 0x2C1 0x2C2 0x2C3   X T T X
0x2C8 0x2C9 0x2CA 0x2CB   X . . X
```

Pieces: `crown_l` 0x2B8, `crown_ml` 0x2B9, `crown_mr` 0x2BA, `crown_r` 0x2BB, `cap_l` 0x2C0, `lintel_l` 0x2C1, `lintel_r` 0x2C2, `cap_r` 0x2C3, `post_l` 0x2C8, `open_l` 0x2C9, `open_r` 0x2CA, `post_r` 0x2CB.

### Myrtle: small bushes and the big one

`bush`, 8 wide by 1 tall. Myrtle bushes on the lawn, dense enough to stop a hound's eye. `myrtle`, `_b`, `_flowers` (in white flower) are one cell. `big_*` is the great myrtle, 2 x 2: place `big_tl` `big_tr` over `big_bl` `big_br`. `stump` is an old cut laurel trunk. All block.

```text
ids                                                walk
0x2D0 0x2D1 0x2D2 0x2D3 0x2D4 0x2D5 0x2D6 0x2D7   X X X X X X X X
```

Pieces: `myrtle` 0x2D0, `myrtle_b` 0x2D1, `myrtle_flowers` 0x2D2, `big_tl` 0x2D3, `big_tr` 0x2D4, `big_bl` 0x2D5, `big_br` 0x2D6, `stump` 0x2D7.

### Stelae, cypresses, lamps: tall things on the lawn

`tall`, 6 wide by 2 tall. Each is a base (blocks) under a top drawn over the player in the cell above, which must be plain `lawn` (the lamp's, plain `pave`). Stelae carry a deer, a bow or a laurel wreath, and stop a hound's eye. `cypress` and `cypress_b` are a cypress two cells tall. `lamp` is a bronze lampstand, burning (the porch's).

```text
ids                                    walk
0x2D8 0x2D9 0x2DA 0x2DB 0x2DC 0x2DD   T T T T T T
0x2E0 0x2E1 0x2E2 0x2E3 0x2E4 0x2E5   X X X X X X
```

Pieces: `stele_deer_top` 0x2D8, `stele_bow_top` 0x2D9, `stele_wreath_top` 0x2DA, `cypress_top` 0x2DB, `cypress_b_top` 0x2DC, `lamp_top` 0x2DD, `stele_deer` 0x2E0, `stele_bow` 0x2E1, `stele_wreath` 0x2E2, `cypress` 0x2E3, `cypress_b` 0x2E4, `lamp` 0x2E5.

### A tall cypress

`tallcypress`, 1 wide by 3 tall. A cypress three cells tall: `top` over `mid` (both drawn over the player) over `base`, on plain `lawn`.

```text
ids      walk
0x2BC   T
0x2C4   T
0x2CC   X
```

Pieces: `top` 0x2BC, `mid` 0x2C4, `base` 0x2CC.

### The hounds' kennels, a bowl, Anthia's bench

`kennel`, 8 wide by 1 tall. By the porch: the temple hounds' kennels (2 x 2: `kennel_tl` `kennel_tr` over `kennel_bl` `kennel_br`), a bronze water `bowl`, a `leash` coiled on a post, all on the porch's paving. `bench_l` `bench_r`: a marble bench with a fleece thrown over it, on the lawn (Anthia's grove). All block.

```text
ids                                                walk
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC 0x2ED 0x2EE 0x2EF   X X X X X X X X
```

Pieces: `kennel_tl` 0x2E8, `kennel_tr` 0x2E9, `kennel_bl` 0x2EA, `kennel_br` 0x2EB, `bowl` 0x2EC, `leash` 0x2ED, `bench_l` 0x2EE, `bench_r` 0x2EF.

### The great altar of Artemis

`altar`, 3 wide by 2 tall. The great altar (3 x 2) on the porch's paving: a marble table under a silver crescent, a bow and a quiver carved on its front, the first feathers of the hunt laid on top.

```text
ids                  walk
0x2BD 0x2BE 0x2BF   X X X
0x2C5 0x2C6 0x2C7   X X X
```

Pieces: `altar_tl` 0x2BD, `altar_tm` 0x2BE, `altar_tr` 0x2BF, `altar_bl` 0x2C5, `altar_bm` 0x2C6, `altar_br` 0x2C7.

### Artemis

`statue`, 2 wide by 3 tall. The goddess on her plinth, drawing an arrow from her quiver, on the porch's paving: `tl` `tr` (drawn over the player) over `ml` `mr` over `bl` `br`.

```text
ids            walk
0x2F0 0x2F1   T T
0x2F8 0x2F9   X X
0x300 0x301   X X
```

Pieces: `tl` 0x2F0, `tr` 0x2F1, `ml` 0x2F8, `mr` 0x2F9, `bl` 0x300, `br` 0x301.

### The moonlit rock

`rock`, 8 wide by 3 tall. Kallisto's rock, built from cell types. Row by row of the rock: the `flat` on top (`_b`; `_shade` under the hedge; `_w`/`_e` its sides, the lawn beyond; `corner_w`/`_e` lawn with the rock's rounded corner, blocking), the `lip` where it drops (`_w`, `_e`; `stair_top` where the stair begins), the `cliff` (`_b`, `_w`, `_e`; `stair`), the cliff's `foot` (`_w`, `_e`; `stair_foot`), and in front of it `rubble`, a `boulder` and a `landing` of flat rock. `seat` is the flat stone Kallisto sits on (walkable: she stands on it).

```text
ids                                                walk
0x308 0x309 0x30A 0x30B 0x30C 0x30D 0x30E 0x30F   . . . . . . X X
0x310 0x311 0x312 0x313 0x314 0x315 0x316 0x317   . . . . X X X .
0x318 0x319 0x31A 0x31B 0x31C 0x31D 0x31E 0x31F   X X X . X X . X
```

Pieces: `flat` 0x308, `flat_b` 0x309, `flat_shade` 0x30A, `flat_w` 0x30B, `flat_e` 0x30C, `seat` 0x30D, `corner_w` 0x30E, `corner_e` 0x30F, `lip` 0x310, `lip_w` 0x311, `lip_e` 0x312, `stair_top` 0x313, `cliff` 0x314, `cliff_w` 0x315, `cliff_e` 0x316, `stair` 0x317, `foot` 0x318, `foot_w` 0x319, `foot_e` 0x31A, `stair_foot` 0x31B, `rubble` 0x31C, `boulder` 0x31D, `landing` 0x31E, `cliff_b` 0x31F.

### The hedge across the stair, and Anthia's gate

`gates`, 8 wide by 1 tall. `hedge_l` `hedge_r`: the low laurel hedge across the foot of the rock's stair, on the rock's stair rock; `hedge_lowered_*` (= the hedge + 1) is the same hedge clipped to its roots, walkable. `gate_top` over `gate`: Anthia's woven laurel gate in a hedge wall's top and face rows; `gate_top_open` and `gate_open` (= the closed piece + 1) stand open.

```text
ids                                                walk
0x320 0x321 0x322 0x323 0x324 0x325 0x326 0x327   X . X . X . X .
```

Pieces: `hedge_l` 0x320, `hedge_lowered_l` 0x321, `hedge_r` 0x322, `hedge_lowered_r` 0x323, `gate_top` 0x324, `gate_top_open` 0x325, `gate` 0x326, `gate_open` 0x327.

### The moon pool on the rock

`pool`, 2 wide by 1 tall. A basin cut in the rock's flat, holding still black water and the moon's reflection. Blocks; place on the rock's flat.

```text
ids            walk
0x2CD 0x2CE   X X
```

Pieces: `pool_l` 0x2CD, `pool_r` 0x2CE.

<!-- end of catalog -->
