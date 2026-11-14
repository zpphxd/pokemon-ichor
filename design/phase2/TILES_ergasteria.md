# ergasteria: the working interiors

`gTileset_Ergasteria` ("workshops") is the secondary tileset for Phase 2's working rooms: the inns, the mint, the forge, the potter's, the tavern. Batch 1 draws Aegina's three homes (the inn, the mint and Aiakides's house, laid out in `ROOMS_ergasteria.md`). Batch 2 adds Emporion's workshops to the same set. It sits on the `oikos` primary, as oikia and civic do, and like them works on any primary.

![the gallery and courtyard pieces](img/ergasteria_gallery.png)

![every piece on terracotta](img/ergasteria_catalog.png)

## What's in it

**Shared with the slice.** The furniture a working room shares with a home is taken from oikia (`tools/ichor/art/oikia_art.py`) pixel for pixel, so these rooms match the slice's homes exactly:
- terracotta pavers and limestone flags, with their shadowed rows and columns;
- the whitewashed back wall with the red ochre dado and with the Aegean dado; the void;
- the red and the blue rug;
- the window, the niche, drying herbs, the jar shelf and the honey shelf;
- the kline, both klismos chairs, the stool, the long table and the round one;
- both amphorae, the pithos, the cooking pots, the kitchen hearth and its soot;
- the potted myrtle, the fish basket, knucklebones, the bronze lampstand, the Doric post and the reed door mat.

oikia's boards, loom, chest, altar, scrolls, stairs and the rest stay out until a room needs them: each piece costs tiles.

**New for the inn.**
- **The gallery wall.** The courtyard's back wall is three blocks tall: the eave and rafters, the whitewashed upper storey, then the shaded ground floor under the gallery with the inn's blue dado.
- **The gallery.** Timber bays drawn over that wall, one block wide each: a post with a guest-room door behind the balustrade, the balustrade over bare wall, a blue blanket airing over the rail, and a clay lamp hung under the gallery. Any order tiles cleanly.
- **The ladder** up to the gallery (the loft), 1x3: its top above the rail, its foot on the courtyard floor.
- **The cistern.** A fluted marble well-head over the rain cistern, with a dipper on its rope, 2x2.
- **The turtle mosaic.** A pebble mosaic of a sea turtle, Aegina's coin, in a frame of white beads, 4x3, walkable. Dark pebbles outline it, terracotta pebbles make its shell, and a row of white ones runs down its spine as on the island's staters.
- **The common room's hearth.** An open fire in a raised stone curb, free-standing, 2x2.
- **A long bench**, 2x1.

**New for the mint.**
- **The stone wall.** Ashlar for the strongroom: three courses of squared limestone with staggered joints on a dark plinth, under the same ceiling beam.
- **The anvil.** An iron block with the lower die in it, on an oak stump, a blank on the die.
- **The die rack.** Three upper dies, a hammer and tongs on a pegged board, hung on the wall, 2x2.
- **The brazier.** A small bronze brazier with silver blanks heating on its coals.
- **The balance.** A moneyer's balance, silver in one pan and a weight in the other, 1x2.
- **The strongbox.** Oak bound in bronze, with a sea turtle stamped on its lid, 2x2.
- **The vault door.** Oak bound in bronze, with a slot that lets coins out and nothing in, set in the back wall, 1x2.
- **The counting table.** Stacks of silver staters, a purse and blanks on a table, 2x1. Its top row of tiles is the iron palette and its bottom row the wood palette, which keeps every 8x8 tile in one palette.

**New for Aiakides's house.**
- **The shield and spear.** A bronze hoplite shield with an ant for its blazon and the spear behind it, hung on the wall, 2x2.
- **The ant shrine.** A little stone pillar with a terracotta ant on top and a lamp in its niche, against the back wall, 1x2.
- **The anthill pot.** A big pot full of earth with the anthill heaped in it, ants on the rim, 1x2.
- **The ant trail.** A line of ants marching across the floor, walkable, 1x1. Two in a row make a diagonal.

## How it is made

The art is in `tools/ichor/art/ergasteria_art.py`: hand-drawn character grids, one character per color, `.` for clear, with small generators for the round and symmetric pieces (the cistern, the mosaic, the shield, the gallery bays). `tools/ichor/art/ergasteria_build.py` does the rest, the way `oikia_build.py` does (`design/phase1/TILES_oikia.md`), and reuses its generic parts:

```bash
/usr/bin/python3 tools/ichor/art/ergasteria_build.py                # compose, compile, check, write the rooms and images
/usr/bin/python3 tools/ichor/art/ergasteria_build.py --no-compile   # compose and check only
/usr/bin/python3 tools/ichor/maps/aegina_homes.py                   # the same build, from the rooms' end
```

1. It composes every cell of every room (each module in `room_modules()`; batch 1 has `tools/ichor/maps/aegina_homes.py`) and of three catalog layouts.
2. It deduplicates the cells into metatiles, the bare floors, walls and rugs first, and writes `data/tilesets/secondary/ergasteria/porytiles_src/`.
3. It compiles with Porytiles, paired with `gTileset_Aethos`, and copies back any solid tile Porytiles borrowed from aethos.
4. It checks every metatile uses only ergasteria's tiles and palettes 6-12, renders every room on `oikos`, `aethos` and `building`, and fails unless all three match the composed source.
5. It writes each room's `map.bin` and `border.bin`, edits its `layouts.json` entry (size and tilesets only), and writes the renders and the generated tables here and in `ROOMS_ergasteria.md`.

**The rooms are data in Python.** The builder rewrites their blockdata on every run, so metatile ids may move freely between builds. Re-dress a room in `aegina_homes.py`, not in Porymap.

**Rooms can mix floors and walls.** Beyond oikia's format, a room's `floors` maps more grid characters to other floors (the inn's flagged courtyard is `,`), and `walls` maps more characters to other wall styles of any height (the inn's three-block gallery wall is `G`).

**Layers, collision and behavior** follow oikia: floors and walls on the bottom layer, furniture on the middle layer; floor passable at elevation 3, walls and furniture blocked at elevation 0, warp tiles passable at elevation 0. Only the door mat carries a behavior (`MB_SOUTH_ARROW_WARP`). A walkable piece (the mosaic, the ant trail) keeps the floor passable; laid over a blocked cell it keeps it blocked.

## Palettes

Seven palettes of at most 15 colors, all multiples of 8, none equal to an aethos color (the builder asserts both). Five are oikia's, so the shared furniture fits them as it is.

| Palette | Use | Colors |
|---|---|---|
| wall | oikia's: beams, whitewash, red ochre and Aegean dados, ochre key, shutters, sky; also the ashlar and the gallery wall | 15 |
| floor | terracotta (6) and limestone (5), oikia's; a dark pebble; three earth tones | 15 |
| wood | oikia's: furniture woods, bronze fittings, linen, red and blue cloth, olive | 15 |
| clay | oikia's: pottery, hearth stone, fire, soot, white slip, bronze, honey | 15 |
| iron | oikia's rug colors (madder, ochre, saffron, wool, indigo, blues, brown), with iron (3), silver and a lit wood | 15 |
| nature | oikia's: myrtle and herbs, wicker, fish, rope, a plant pot | 14 |
| bronze | oikia's: bronze, flame, water, marble, painted red | 15 |

**Planned for batch 2.** The palettes were chosen so Emporion's workshops need no new ones:
- **The forge** (the Hephaisteion): the hearth's stone, fire and soot are in clay; the smith's horned anvil, tongs and bars in iron, where the madder, ochre and saffron double as red, orange and yellow heat; the bellows' leather is iron's browns.
- **The potter's wheel and kiln** (Euphronios): clay has the whole terracotta ramp, the white slip, stone and fire; the wheel and shelves are wood.
- **The tavern** (the Dolphin): the dolphin mosaic uses the floor palette's pebbles as the turtle does; amphora racks are wood and clay; knucklebones and the long bench are already in.
- **Beaten-earth floors** for the workshops: the floor palette's three earth tones (unused in batch 1).
- One nature slot is free.

## Budget

Batch 1 uses **399 of 504 tiles** (the ceiling batch 1 was given was about 440): 105 are left for batch 2. Tiles 504-511 stay free, because door animations copy their frames over them (`DOOR_TILE_START_SIZE1` in `src/field_door.c`). Metatiles are not tight: 270 of 512.

To spend tiles carefully:
- Draw symmetric pieces symmetric to the pixel. Porytiles stores a mirrored 8x8 tile once, so the mosaic costs 18 tiles, not 36.
- Make plain fill repeat every 8 pixels (the mosaic's pebble field does), so it costs one tile.
- Leave pieces out of the set until a room uses them, as above.

## Generated tables

The builder rewrites everything below this line.

<!-- ergasteria_build: begin generated -->

Built: **270** metatiles (`0x200`-`0x30d`) of 512, **399** tiles of 504 (batch 1's budget: 440), palettes 6-12.

| Piece | Metatile |
|---|---|
| floor terracotta, plain | `200` |
| floor terracotta, alt | `201` |
| floor terracotta, top | `202` |
| floor terracotta, left | `203` |
| floor terracotta, corner | `204` |
| floor flags, plain | `205` |
| floor flags, top | `206` |
| floor flags, left | `207` |
| floor flags, corner | `208` |
| wall red, row 0 | `209` |
| wall red, row 1 | `20A` |
| wall blue, row 0 | `209` |
| wall blue, row 1 | `20B` |
| wall stone, row 0 | `20C` |
| wall stone, row 1 | `20D` |
| wall gallery, row 0 | `20E` |
| wall gallery, row 1 | `20F` |
| wall gallery, row 2 | `210` |
| void (outside the room) | `211` |
| rug red, top-left | `212` |
| rug red, top | `213` |
| rug red, top-right | `214` |
| rug red, left | `215` |
| rug red, middle | `216` |
| rug red, right | `217` |
| rug red, bottom-left | `218` |
| rug red, bottom | `219` |
| rug red, bottom-right | `21A` |
| rug blue, top-left | `21B` |
| rug blue, top | `21C` |
| rug blue, top-right | `21D` |
| rug blue, left | `21E` |
| rug blue, middle | `21F` |
| rug blue, right | `220` |
| rug blue, bottom-left | `221` |
| rug blue, bottom | `222` |
| rug blue, bottom-right | `223` |

| Stamp | Cells | Palette | From | Metatiles (catalog) | What it is |
|---|---|---|---|---|---|
| `window` | 1x2 | wall | oikia | 225 / 22D (terracotta) | shuttered window, Aegean-blue shutters open |
| `niche` | 1x2 | wall | oikia | 228 / 230 (terracotta) | wall niche with a terracotta goddess and an aryballos |
| `herbs` | 1x2 | nature | oikia | 224 / 22C (terracotta) | bundles of drying herbs hung from pegs in the beam |
| `jar_shelf` | 2x2 | wood | oikia | 226 227 / 22E 22F (terracotta) | wall shelf of remedy jars and flasks |
| `honey_shelf` | 2x2 | wood | oikia | 229 22A / 231 232 (terracotta) | wall shelf of honey jars sealed with wax |
| `kline` | 2x2 | wood | oikia | 2AD 2AE / 295 296 (terracotta) | kline (couch-bed): a scrolled headrest with a bronze boss, linen pillow, woven blue coverlet |
| `klismos_r` | 1x1 | wood | oikia | 2AF (terracotta) | klismos chair, facing right |
| `klismos_l` | 1x1 | wood | oikia | 2B0 (terracotta) | klismos chair, facing left |
| `stool` | 1x1 | wood | oikia | 2B1 (terracotta) | diphros: a folding stool with crossed legs and a fleece seat |
| `table` | 2x1 | wood | oikia | 2B3 2B4 (terracotta) | trapeza: a low table with bread, a red jug, olives and a cup |
| `table_round` | 1x1 | wood | oikia | 251 (terracotta) | a small three-legged table with a jug and bread |
| `amphora` | 1x2 | clay | oikia | 2B5 / 2B7 (terracotta) | amphora with a black-figure band |
| `amphora_plain` | 1x2 | clay | oikia | 2B6 / 2B8 (terracotta) | a plain oil amphora |
| `pithos` | 1x2 | clay | oikia | 29C / 29D (terracotta) | pithos: a big storage jar with rope-pattern bands and a stone lid |
| `pots` | 1x1 | clay | oikia | 255 (terracotta) | cooking pots: a sooty chytra, a jug and a stack of bowls |
| `hearth` | 2x2 | clay | oikia | 2AB 28E / 2AC 294 (terracotta) | kitchen hearth: Hestia's fire in a stone curb, a bronze cauldron on its tripod |
| `soot` | 2x2 | clay | oikia | 282 283 / 2A8 2A9 (terracotta) | smoke-blackened plaster above the hearth |
| `myrtle` | 1x2 | nature | oikia | 2B9 / 2C3 (terracotta) | potted myrtle, Aphrodite's shrub, in flower |
| `fish_basket` | 1x1 | nature | oikia | 2BA (terracotta) | a wicker basket of the morning's catch |
| `knucklebones` | 1x1 | nature | oikia | 2BB (terracotta) | astragaloi: five knucklebones on a leather gaming cloth |
| `lampstand` | 1x2 | bronze | oikia | 246 / 24B (terracotta) | lychnouchos: a bronze lampstand on lion-paw feet, lamp lit |
| `column` | 1x3 | bronze | oikia | 247 / 24C / 252 (terracotta) | a Doric post of whitewashed stone, holding up the beam |
| `mat` | 2x1 | nature | oikia | 29E 29F (terracotta) | woven reed mat at the door; both cells are south-arrow warps |
| `cistern` | 2x2 | bronze | ergasteria | 2C8 2C9 / 2CB 2CC (terracotta) | the courtyard's rain cistern: a fluted marble well-head over dark water, a dipper on its rope |
| `mosaic_turtle` | 4x3 | floor | ergasteria | 256 257 258 259 / 25A 25B 25C 25D / 262 263 264 265 (gallery) | pebble mosaic of a sea turtle, Aegina's coin: terracotta shell, white beads down the spine |
| `gallery_door` | 1x3 | wood | ergasteria | 22B / 234 / 23A (gallery) | the inn's timber gallery: a post, a guest-room door behind the balustrade |
| `gallery_rail` | 1x3 | wood | ergasteria | --- / 235 / 23B (gallery) | the gallery's balustrade over bare wall |
| `gallery_blanket` | 1x3 | wood | ergasteria | --- / 236 / 23B (gallery) | a blue blanket airing over the gallery rail |
| `gallery_lamp` | 1x3 | wood | ergasteria | --- / 235 / 23C (gallery) | the balustrade, with a clay lamp hung under the gallery |
| `ladder` | 1x3 | wood | ergasteria | 30C / 30D / 240 (gallery) | a timber ladder up to the guest gallery (the loft); its foot stands in the courtyard |
| `hearth_floor` | 2x2 | clay | ergasteria | 23E 23F / 244 245 (terracotta) | the common room's hearth: an open fire in a raised stone curb, where the inn eats |
| `bench` | 2x1 | wood | ergasteria | 2B2 243 (terracotta) | a long wooden bench |
| `anvil` | 1x1 | iron | ergasteria | 2BC (terracotta) | a coin anvil: an iron block with the lower die in it, on an oak stump; a blank on the die |
| `coin_table` | 2x1 | wood | ergasteria | 2C1 2C2 (terracotta) | a counting table: stacks of silver staters, a purse, blanks waiting their turn |
| `die_rack` | 2x2 | iron | ergasteria | 2A0 2A1 / 2A3 2A4 (terracotta) | the moneyer's rack: three upper dies, a hammer and tongs on pegs |
| `brazier_small` | 1x1 | bronze | ergasteria | 2BD (terracotta) | a small bronze brazier, silver blanks heating on its coals |
| `scales` | 1x2 | bronze | ergasteria | 2BE / 2C4 (terracotta) | a moneyer's balance: silver in one pan, a bronze weight in the other |
| `turtle_chest` | 2x2 | wood | ergasteria | 2BF 2C0 / 2C5 2C6 (terracotta) | the mint's strongbox: oak bound in bronze, a sea turtle stamped on its lid |
| `vault_door` | 1x2 | wood | ergasteria | 2A2 / 2A5 (terracotta) | the strongroom's inner door: oak bound in bronze, with a slot that lets coins out and nothing in |
| `shield_spear` | 2x2 | bronze | ergasteria | 284 285 / 2A6 2A7 (terracotta) | Aiakides's bronze shield, an ant for its blazon, and his spear, hung on the wall |
| `ant_shrine` | 1x2 | clay | ergasteria | 2AA / 28F (terracotta) | a little stone shrine with a clay ant on it and a lamp in its niche: Aiakides's ancestors |
| `anthill_pot` | 1x2 | clay | ergasteria | 2C7 / 2CA (terracotta) | a big pot full of earth, a living anthill heaped in it; ants on the rim |
| `ant_trail` | 1x1 | clay | ergasteria | 297 (terracotta) | a line of ants across the floor, marching for the crumbs |

<!-- ergasteria_build: end generated -->
