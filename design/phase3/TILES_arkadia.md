# Arkadia tileset catalog

Arkadia is a town in a forest, on a long slope among cypresses so tall the houses look like
toys between their trunks (SCRIPT.md Part 2). Two secondaries, both on the `aethos` primary:

- `gTileset_Arkadia` (488 of 504 tiles): the town's cypresses in four shapes, the
  lamp-trees unlit and lit, the canopy at the town's edges, the grey rock (Kithairon's, so
  the climb from Route 12 matches) with its tall faces, terrace walls, the timber-and-stone
  house kit under weathered shingles, the Asclepeion against its outcrop, the Agora's stall
  round the great cypress, Hippothoos's hut and kiln, Krotos's byre and fence, the old
  racecourse, Iamos's wall, Pan's grotto, the temple stair, the Temple of Artemis and its
  precinct gate, and the Cypress Wood's gate.
- `gTileset_ArkadiaWood` (247 of 504 tiles): the Wood's floor in deep shade, its
  ferns (the tall grass), the canopy, the great trunks, the starlit clearing and its stump,
  the Tomb of Kallisto, Agapenor's kiln, and the Pool's glade: the canopy over grass, the
  black pool and its fixed stars, white poplars, asphodel (the glade's tall grass), the seat.

**This file is generated** above the passes section by `tools/ichor/art/arkadia_build.py`.
The art is in `arkadia_lib.py` (colors, groups, the cypress and canopy painters),
`arkadia_trees.py`, `arkadia_town.py` and `arkadia_wood.py`. The maps are built by
`tools/ichor/maps/arkadia.py` from the plans in `tools/ichor/maps/arkadia_plan.py`; the
soft sets hold only the outlines those plans use, so rebuild the tiles after changing one.

The sheets are [img/tiles_arkadia_sheet.png](img/tiles_arkadia_sheet.png) and
[img/tiles_arkadia_wood_sheet.png](img/tiles_arkadia_wood_sheet.png); every piece on its ground
is [img/arkadia_pieces.png](img/arkadia_pieces.png) and
[img/arkadia_wood_pieces.png](img/arkadia_wood_pieces.png).

**Why two sets.** One set's 504 tiles can't hold a town, a dark forest and a sacred pool. The
Wood is entered by a gate warp, so no seam joins the two; the Wood and the Pool share theirs, so
their seam needs no aethos-only strip.

**Collision.** `X` blocks, `.` walks, `T` walks and draws over the player, `G` tall grass
(`MB_TALL_GRASS`), `J` a ledge (`MB_JUMP_SOUTH`), `D` a door (`MB_NON_ANIMATED_DOOR`).

**Ground.** Pieces marked on grass leave their bottom layer to aethos's grass (`0x001`); the build
points it there, so rebuild after aethos is repainted.

**Palettes.** Every 8x8 tile draws from one group of its set:

| Set | Group | Use |
|---|---|---|
| Arkadia | tree | the cypresses, the canopy, the lamps and their glow, on grass |
| Arkadia | house | stone footings, dark timber, weathered shingles, daub, a lit window, a red door |
| Arkadia | rock | Kithairon's grey rock, moss, a cave's dark, a glint, the spring |
| Arkadia | sacred | the temple: marble, silver, the roof's terracotta, the night-blue frieze |
| Arkadia | town | the racecourse's earth, the awning, nets, fences, the kiln and its smoke |
| ArkadiaWood | forest | the floor in deep shade, the canopy, ferns, bark, starlight, embers |
| ArkadiaWood | tomb | the mound's earth and stones, the little shrine |
| ArkadiaWood | canopy | the canopy over grass, round the Pool |
| ArkadiaWood | glade | white poplars, asphodel, the seat |
| ArkadiaWood | pool | the black water, its stars, the kerb |

## gTileset_Arkadia

### — Cypresses, the lamp-trees and the canopy —

### Cypress: the tall spire

`cypress_spire`, 2 wide by 4 tall. A tall, slim cypress, 2x4: the town's commonest. Rows 0-1 draw over the player (walk behind it); rows 2-3 block.

```text
ids           walk
0x200 0x201   T T
0x208 0x209   T T
0x210 0x211   X X
0x218 0x219   X X
```

Parts: `tl` 0x200, `tr` 0x201, `ul` 0x208, `ur` 0x209, `ml` 0x210, `mr` 0x211, `bl` 0x218, `br` 0x219.

### Cypress: the broad flame

`cypress_broad`, 2 wide by 4 tall. A fuller cypress, its crown rounded into a flame.

```text
ids           walk
0x202 0x203   T T
0x20A 0x20B   T T
0x212 0x213   X X
0x21A 0x21B   X X
```

Parts: `tl` 0x202, `tr` 0x203, `ul` 0x20A, `ur` 0x20B, `ml` 0x212, `mr` 0x213, `bl` 0x21A, `br` 0x21B.

### Cypress: the twins

`cypress_twin`, 2 wide by 4 tall. Two slim cypresses grown together, one a head taller.

```text
ids           walk
0x204 0x205   T T
0x20C 0x20D   T T
0x214 0x215   X X
0x21C 0x21D   X X
```

Parts: `tl` 0x204, `tr` 0x205, `ul` 0x20C, `ur` 0x20D, `ml` 0x214, `mr` 0x215, `bl` 0x21C, `br` 0x21D.

### Cypress: the old one

`cypress_old`, 2 wide by 4 tall. A gnarled old cypress, leaning, its crown split by a lightning stroke long ago, its trunk showing.

```text
ids           walk
0x206 0x207   T T
0x20E 0x20F   T T
0x216 0x217   X X
0x21E 0x21F   X X
```

Parts: `tl` 0x206, `tr` 0x207, `ul` 0x20E, `ur` 0x20F, `ml` 0x216, `mr` 0x217, `bl` 0x21E, `br` 0x21F.

### The lamp-tree (unlit)

`lamptree`, 2 wide by 4 tall. The broad cypress hung with two clay lamps on chains: every cypress on the main path. The lamps are on row 2 (`ml`, `mr`); `lamps_lit` holds the same two cells with the lamps alight, which the dusk scene and the night swap in (metatile labels `Arkadia_LampUnlit_L/_R`, `Arkadia_LampLit_L/_R`).

```text
ids           walk
0x220 0x221   T T
0x228 0x229   T T
0x230 0x231   X X
0x238 0x239   X X
```

Parts: `tl` 0x220, `tr` 0x221, `ul` 0x228, `ur` 0x229, `ml` 0x230, `mr` 0x231, `bl` 0x238, `br` 0x239.

### The lamp-tree's lamps, alight

`lamps_lit`, 2 wide by 1 tall. Row 2 of `lamptree` with its lamps lit: swap these over `ml` and `mr`.

```text
ids           walk
0x222 0x223   X X
```

Parts: `L` 0x222, `R` 0x223.

### The canopy: a mass of cypress crowns

`canopy`, 8 wide by 3 tall. Cypress crowns so close they knit, over aethos grass: the forest the town stands in. Spires along the north edge, trunks and shade along the south. Impassable. Names are blob shape keys.

```text
ids                                               walk
0x240 0x241 0x242 0x243 0x244 0x245 0x246 0x247   X X X X X X X X
0x248 0x249 0x24A 0x24B 0x24C 0x24D 0x24E 0x24F   X X X X X X X X
0x250 0x251 0x252 0x253 0x254 0x255 0x256 0x257   X X X X X X X X
```

### — Rock, terraces, houses and the town's buildings —

### Rock with a south face

`rock`, 8 wide by 2 tall. The grey rock of the Arkadian hills seen from above, its south face showing, on aethos grass: the Asclepeion's outcrop and the temple hill. Where `face` cells continue below, the rock above them is drawn as region (no face). Impassable. Names are blob keys.

```text
ids                                               walk
0x258 0x259 0x25A 0x25B 0x25C 0x25D 0x25E 0x25F   X X X X X X X X
0x260 0x261 0x262 0x263 0x264 0x265 0x266 0x267   X X X X X X X X
```

### Tall rock faces

`face`, 3 wide by 3 tall. A rock face more than one row tall, below `rock`: `top` (the lip), `mid`, `foot` (the dark foot); `W` and `E` are the face's ends with grass beside them. The waterfall cliff is six rows of it, the temple hill's front two.

```text
ids                 walk
0x224 0x225 0x226   X X X
0x22C 0x22D 0x22E   X X X
0x234 0x235 0x236   X X X
```

Parts: `top` 0x224, `topW` 0x225, `topE` 0x226, `mid` 0x22C, `midW` 0x22D, `midE` 0x22E, `foot` 0x234, `footW` 0x235, `footE` 0x236.

### Pan's grotto

`grotto`, 2 wide by 1 tall. A shallow cave mouth in the outcrop's south face, a syrinx carved over it: lay it where the outcrop's face row is. Too shallow to enter: a sign event in front.

```text
ids           walk
0x22A 0x22B   X X
```

Parts: `L` 0x22A, `R` 0x22B.

### The spring and its basin

`spring`, 1 wide by 2 tall. `spout`: the outcrop's face with the spring pouring from a crack (lay it in the face row beside the Asclepeion); `basin`: a stone basin on grass below it.

```text
ids     walk
0x227   X
0x22F   X
```

Parts: `spout` 0x227, `basin` 0x22F.

### The cave mouth beside the falls

`cliff_cave`, 1 wide by 1 tall. A face cell (`face`'s `mid`) with a dark cave mouth and a glint inside: the Horn of Achelous's cave (Act III). Lay it beside the waterfall.

```text
ids     walk
0x232   X
```

### Terrace wall

`terrace`, 4 wide by 1 tall. A dry-stone terrace wall, the upper level north of it: `W` end, `run`, `E` end, `stair` (walkable steps up through it).

```text
ids                       walk
0x23A 0x23B 0x23C 0x23D   X X X .
```

Parts: `W` 0x23A, `run` 0x23B, `E` 0x23C, `stair` 0x23D.

### Iamos's old wall

`oldwall`, 2 wide by 1 tall. A stub of the old wall, Cyclopean, on grass: `W` and `E`, broken at both ends. Iamos sits on it.

```text
ids           walk
0x23E 0x23F   X X
```

Parts: `W` 0x23E, `E` 0x23F.

### The temple stair

`stair`, 3 wide by 3 tall. A broad stone stair through the temple hill's lip (row 0) and its two-row face (rows 1-2): west cheek, run, east cheek. Walkable. The first step is the race's turning point.

```text
ids                 walk
0x268 0x269 0x26A   . . .
0x270 0x271 0x272   . . .
0x278 0x279 0x27A   . . .
```

Parts: `W0` 0x268, `run0` 0x269, `E0` 0x26A, `W1` 0x270, `run1` 0x271, `E1` 0x272, `W2` 0x278, `run2` 0x279, `E2` 0x27A.

### The house kit: timber and stone under shingles

`house`, 8 wide by 3 tall. Arkadia's houses, built from parts. Roofs: `ridgeW` `ridge`… `ridgeE` over `eaveW` `eave`… `eaveE` (weathered wooden shingles). An upper storey of timber and daub: `upW` `up` `upWin` `upE`, and `upRibbon` (Klymene's window, a victor's ribbon on the sill). The ground storey, daub over a stone footing: `wallW` `wall` `wallWin` `wallE`, doors `door`, `doorWolf` (Nyktimos's hall: the grey wolf pelt over the lintel), `doorPan` (Krotos's: the horned mask), `doorWide` (the hall's double door), `wallSacks` (charcoal sacks against the wall), and `louvre` (a roof cell with a smoke louvre). Doors are MB_NON_ANIMATED_DOOR.

```text
ids                                               walk
0x280 0x281 0x282 0x283 0x284 0x285 0x286 0x287   X X X X X X X X
0x288 0x289 0x28A 0x28B 0x28C 0x28D 0x28E 0x28F   X X X X X X X D
0x290 0x291 0x292 0x293 0x294 0x295 0x296 0x297   D D X X D . . .
```

Parts: `ridgeW` 0x280, `ridge` 0x281, `ridgeE` 0x282, `eaveW` 0x288, `eave` 0x289, `eaveE` 0x28A, `upW` 0x283, `up` 0x284, `upWin` 0x285, `upE` 0x286, `upRibbon` 0x287, `wallW` 0x28B, `wall` 0x28C, `wallWin` 0x28D, `wallE` 0x28E, `door` 0x28F, `doorWolf` 0x290, `doorPan` 0x291, `wallSacks` 0x292, `louvre` 0x293, `doorWide` 0x294.

### The Asclepeion

`asclepeion`, 5 wide by 4 tall. The Asclepeion, 5x4: shingles over stone, the rod of Asclepius on a white plaque, a porch on two posts, the door at (2,3) (MB_NON_ANIMATED_DOOR). Build it against the outcrop's south face, the spring's `spout` and `basin` beside its west wall.

```text
ids                             walk
0x298 0x299 0x29A 0x29B 0x29C   X X X X X
0x2A0 0x2A1 0x2A2 0x2A3 0x2A4   X X X X X
0x2A8 0x2A9 0x2AA 0x2AB 0x2AC   X X X X X
0x2B0 0x2B1 0x2B2 0x2B3 0x2B4   X X D X X
```

Parts: `door` 0x2B2.

### The Agora's stall round the great cypress

`agora`, 4 wide by 6 tall. The town's biggest cypress (rows 0-2, on grass) with the Agora's stall built round its trunk (rows 3-5): a striped awning, nets and jars, the counter, the door at (1,5) (MB_NON_ANIMATED_DOOR).

```text
ids                       walk
0x2B8 0x2B9 0x2BA 0x2BB   X X X X
0x2C0 0x2C1 0x2C2 0x2C3   X X X X
0x2C8 0x2C9 0x2CA 0x2CB   X X X X
0x2D0 0x2D1 0x2D2 0x2D3   X X X X
0x2D8 0x2D9 0x2DA 0x2DB   X X X X
0x2E0 0x2E1 0x2E2 0x2E3   X D X X
```

Parts: `door` 0x2E1.

### Hippothoos's charcoal hut

`hut`, 4 wide by 3 tall. A hut dug half into the hillside: turf on the roof, a front of split logs, charcoal sacks stacked by the door at (2,2) (MB_NON_ANIMATED_DOOR).

```text
ids                       walk
0x26B 0x26C 0x26D 0x26E   X X X X
0x273 0x274 0x275 0x276   X X X X
0x27B 0x27C 0x27D 0x27E   X X D X
```

Parts: `door` 0x27D.

### A charcoal kiln

`kiln`, 2 wide by 2 tall. A smoking charcoal kiln on grass: an earth mound with its vents.

```text
ids           walk
0x29D 0x29E   X X
0x2A5 0x2A6   X X
```

### Krotos's byre

`byre`, 2 wide by 3 tall. A wattle lean-to for the kids, with a straw roof, against the goatherd's house.

```text
ids           walk
0x2AD 0x2AE   X X
0x2B5 0x2B6   X X
0x2BD 0x2BE   X X
```

### Post-and-rail fence

`fence`, 7 wide by 1 tall. The goat pasture's fence on grass: `h` and `v` runs, corners `nw` `ne` `sw` `se`, and an open `gate` (walkable).

```text
ids                                         walk
0x2E8 0x2E9 0x2EA 0x2EB 0x2EC 0x2ED 0x2EE   X X X X X X .
```

Parts: `h` 0x2E8, `v` 0x2E9, `nw` 0x2EA, `ne` 0x2EB, `sw` 0x2EC, `se` 0x2ED, `gate` 0x2EE.

### The old racecourse

`track`, 3 wide by 1 tall. The old racecourse, two cells wide, running north-south: `W` and `E` its two halves (stone kerbs outside), `post` the carved finishing post on grass beside the track (blocks).

```text
ids                 walk
0x2C4 0x2C5 0x2C6   . . X
```

Parts: `W` 0x2C4, `E` 0x2C5, `post` 0x2C6.

### The Temple of Artemis

`temple`, 5 wide by 4 tall. The small Doric temple on the hill, 5x4, on the hill's rock top: terracotta roof, the pediment with its silver moon disc, the frieze, four columns. The way in is the precinct's gate below it.

```text
ids                             walk
0x2F0 0x2F1 0x2F2 0x2F3 0x2F4   X X X X X
0x2F8 0x2F9 0x2FA 0x2FB 0x2FC   X X X X X
0x300 0x301 0x302 0x303 0x304   X X X X X
0x308 0x309 0x30A 0x30B 0x30C   X X X X X
```

### The precinct wall and gate

`precinct`, 4 wide by 2 tall. The low marble wall round the temple's precinct, seen from the stair: `topW` and `top` (its coping, rock behind), `faceW` and `face` (its face); the gate: `propW` `prop` `propW` mirrored (the propylon's little roof) over `col` `gate` `col` mirrored. Mirror the west pieces for the east (they're symmetric about the gate). The gate is MB_NON_ANIMATED_DOOR: the warp into the night garden.

```text
ids                       walk
0x2CC 0x2CD 0x2CE 0x2CF   X X X X
0x2D4 0x2D5 0x2D6 0x2D7   X X X D
```

Parts: `topW` 0x2CC, `top` 0x2CD, `propW` 0x2CE, `prop` 0x2CF, `faceW` 0x2D4, `face` 0x2D5, `col` 0x2D6, `gate` 0x2D7.

### The Cypress Wood's gate

`woodgate`, 3 wide by 4 tall. Cut into the canopy on the square's west: the crowns over a timber lintel with Artemis's crescent, two great trunks, the dark of the Wood between them. The opening's floor (1,3) is MB_NON_ANIMATED_DOOR: the warp into the Wood.

```text
ids                 walk
0x2F5 0x2F6 0x2F7   X X X
0x2FD 0x2FE 0x2FF   X X X
0x305 0x306 0x307   X X X
0x30D 0x30E 0x30F   X . X
```

Parts: `door` 0x30E.

### The precinct wall and gate, east half

`precinct_e`, 4 wide by 2 tall. `precinct` mirrored: lay its columns 1-3 east of the gate.

```text
ids                       walk
0x2DC 0x2DD 0x2DE 0x2DF   X X X X
0x2E4 0x2E5 0x2E6 0x2E7   D X X X
```

Parts: `topW` 0x2DF, `top` 0x2DE, `propW` 0x2DD, `prop` 0x2DC, `faceW` 0x2E7, `face` 0x2E6, `col` 0x2E5, `gate` 0x2E4.

## gTileset_ArkadiaWood

### — The Cypress Wood —

### The Wood's floor

`floor`, 7 wide by 1 tall. The floor in deep shade (`plain`, `roots` where a tree's roots cross, `needles` a drift of them); the stump clearing's starlit floor (`lit`, `lit2`); `mats`, the floor brightening toward the gate (MB_SOUTH_ARROW_WARP: the way back to Arkadia, on the bottom row); `dig`, turned earth (a dig spot).

```text
ids                                         walk
0x200 0x201 0x202 0x203 0x204 0x205 0x206   . . . . . . .
```

Parts: `plain` 0x200, `roots` 0x201, `needles` 0x202, `lit` 0x203, `lit2` 0x204, `mats` 0x205, `dig` 0x206.

### Ferns (the Wood's tall grass)

`ferns`, 2 wide by 1 tall. Clumps of bracken on the dark floor, each self-contained so any outline works: `a` and `b`, alternate them. MB_TALL_GRASS.

```text
ids           walk
0x208 0x209   G G
```

Parts: `a` 0x208, `b` 0x209.

### The stump

`stump`, 1 wide by 1 tall. An old cypress stump cut flat, on the clearing's starlit floor: where Kleon sits (beat 42).

```text
ids     walk
0x207   X
```

### The Tomb of Kallisto

`tomb`, 5 wide by 4 tall. The mound, 5x4: its top is walkable from the east (column 4, rows 1-2); the shrine at (2,1) (an altar: Artemis's rites); the turned earth at (2,2) (prophecy tablet #5's fixed dig); the fallen trunk across the south face at (2,3)-(3,3) is a ledge down to the path (MB_JUMP_SOUTH).

```text
ids                             walk
0x20A 0x20B 0x20C 0x20D 0x20E   X X X X X
0x212 0x213 0x214 0x215 0x216   X . X . .
0x21A 0x21B 0x21C 0x21D 0x21E   X . . . .
0x222 0x223 0x224 0x225 0x226   X X J J X
```

Parts: `shrine` 0x214, `earth` 0x21C, `ledge` 0x224.

### Agapenor's kiln

`kiln_wood`, 2 wide by 2 tall. A charcoal kiln on the Wood's floor: an earth mound, its vents glowing, smoke going up into the canopy. Its ash hides the Charcoal.

```text
ids           walk
0x210 0x211   X X
0x218 0x219   X X
```

### A stone stele in the Wood

`stele`, 1 wide by 1 tall. A small stele on the Wood's floor, for its signs.

```text
ids     walk
0x20F   X
```

### A great trunk

`great_trunk`, 1 wide by 1 tall. The foot of a huge cypress, roots spread on the floor; put it on the canopy's south edge where a trunk should show (the narrow's pillars).

```text
ids     walk
0x217   X
```

### The Wood's canopy over its floor

`canopy`, 8 wide by 3 tall. The Wood's close-knit cypresses on its floor in deep shade. Impassable. Names are blob shape keys.

```text
ids                                               walk
0x228 0x229 0x22A 0x22B 0x22C 0x22D 0x22E 0x22F   X X X X X X X X
0x230 0x231 0x232 0x233 0x234 0x235 0x236 0x237   X X X X X X X X
0x238 0x239 0x23A 0x23B 0x23C 0x23D 0x23E 0x23F   X X X X X X X X
```

### — The Pool of Mnemosyne's glade —

### The Wood's canopy round the Pool's glade

`canopy_grass`, 8 wide by 2 tall. The Wood's dark cypresses standing round the glade, over aethos grass. Impassable. Names are blob shape keys.

```text
ids                                               walk
0x240 0x241 0x242 0x243 0x244 0x245 0x246 0x247   X X X X X X X X
0x248 0x249 0x24A 0x24B 0x24C 0x24D 0x24E 0x24F   X X X X X X X X
```

### The Pool of Mnemosyne

`pool`, 4 wide by 3 tall. The round pool, 4x3 on grass: still black water reflecting stars that never move, ringed by pale stones. Impassable; nothing lives in it.

```text
ids                       walk
0x250 0x251 0x252 0x253   X X X X
0x258 0x259 0x25A 0x25B   X X X X
0x260 0x261 0x262 0x263   X X X X
```

Parts: `edge_w` 0x258, `edge_s` 0x261.

### Asphodel (the glade's tall grass)

`asphodel`, 2 wide by 1 tall. Pale asphodel spikes in grey-green leaves, on aethos grass: the glade's tall grass, Arkoby country. Self-contained clumps: `a` and `b`, alternate them. MB_TALL_GRASS.

```text
ids           walk
0x220 0x221   G G
```

Parts: `a` 0x220, `b` 0x221.

### The stone seat

`seat`, 2 wide by 1 tall. `seat`: the stone seat facing the water, where Mnaseas sits; `dig`: turned earth in the grass (a dig spot; walkable).

```text
ids           walk
0x254 0x255   X .
```

Parts: `seat` 0x254, `dig` 0x255.

### A white poplar

`poplar`, 2 wide by 3 tall. A white poplar, Mnemosyne's tree, 2x3 on grass: its top row draws over the player.

```text
ids           walk
0x256 0x257   T T
0x25E 0x25F   X X
0x266 0x267   X X
```

Parts: `tl` 0x256, `tr` 0x257, `ml` 0x25E, `mr` 0x25F, `bl` 0x266, `br` 0x267.

### A white poplar

`poplar_b`, 2 wide by 3 tall. A white poplar, Mnemosyne's tree, 2x3 on grass: its top row draws over the player.

```text
ids           walk
0x25C 0x25D   T T
0x264 0x265   X X
0x26C 0x26D   X X
```

Parts: `tl` 0x25C, `tr` 0x25D, `ml` 0x264, `mr` 0x265, `bl` 0x26C, `br` 0x26D.

<!-- passes: hand-written below this line; arkadia_build.py keeps it -->
