# limen and domos: Emporion's interiors

`gTileset_Limen` ("harbor") and `gTileset_Domos` ("house") are twin secondary tilesets for Emporion's rooms, on the `oikos` primary like oikia, civic and ergasteria, and like them they work on any primary. limen has the harbor's rooms (the Deigma, the Dolphin, the widow's room over the rope-walk, the Titans' hiring hall); domos has the town's (Philoxenos's andron, the runners' barracks, Euphronios's workshop). The rooms are laid out in `ROOMS_emporion.md`.

They are two sets because seven rooms' pieces didn't fit one secondary's 504 tiles (a first single set ran past the limit at about 550). Both are drawn by one art module and share its palettes, so any piece can go in either set: a set compiles only the pieces its rooms use.

## What's in it

**Shared with the slice.** limen's palettes are oikia's seven, so oikia's furniture comes over pixel for pixel: the window, niche, jar shelf, kline, klismos and stool, the tables and the desk, the scrolls cabinet, chest, loom, trident, nets, klepsydra, wool basket, amphorae, pithos, pots, hearth and soot, fish basket, lampstand, column and the reed mat. ergasteria's long bench and the mint's balance come too. Floors: oikia's terracotta, boards and limestone flags. Walls: oikia's red and Aegean dados, and ergasteria's ashlar.

**New for the Deigma.**
- **The harbor.** A floor of blue water with wavelets that repeat every 8 pixels, and its left-edge variant with the quay's stone lip. It can't be walked on (the room's `blocked` grid character).
- **Trestle tables.** One trestle, a plank on crossed legs, drawn in the lowest 8 pixel rows of a 2x2 piece, with each sample's goods above it in their own palette: Lampis's stepped stand of clay lamps; three oil amphorae and a flask; bolts of Tyrian purple, saffron, madder and blue, with a length of purple hanging over the edge; open sacks of barley and wheat and a bowl of first fruits; and one bronze helmet with a red crest, on a stand. The trestle's tiles are shared, so a table costs only its goods.
- **A stuffed tunny** mounted on a board, for the wall.
- **The notice board.** A whitened board on a post, a sheet sealed with the Archon's owl.
- **A grain sack.**

**New for the Dolphin.**
- **The tavern wall.** A low, heavy beam and yellowed plaster with old smoke at the top, over oikia's red dado.
- **The sea window**, 2x2: shutters open, a gull, the sea under the sill with a sail out on it. The widow's room has one too.
- **The amphora rack**, 2x2: a dark-stained timber rack with amphorae laid two high, mouths out.
- **The dolphin mosaic**, 4x2 and walkable: a blue dolphin leaping over waves in a frame of dark and white beads.
- **The knucklebones table**, 2x1: heavy and square, its top worn pale in a hollow, four bones in it and the cup.
- **The krater**, 1x2: a black-figure mixing bowl on a stone stand, the ladle hooked on the rim (Philoxenos has one too).

**New for Philoxenos's andron.**
- **The side couch**, 1x2, and its mirror: a dining couch along a side wall, its scrolled headrest at the top. With oikia's kline along the back wall they make seven.
- **The host mosaic**, 4x2 and walkable: a host stepping out of his doorway, hand held out to a traveler in a broad hat with a staff, a dog at his heels, in a bead border.
- **The curtained bed**, 2x2: the guest bed behind a striped madder-and-wool curtain, the near half drawn back.
- **The washbasin**, 1x2: a marble basin on a pillar, a bronze jug beside it.

**New for the widow's room.**
- **The shroud on the loom**: oikia's loom with its weaving recolored to plain linen.
- **The oar**, 2x1: a single oar hung on two pegs under the beam, its blade painted blue.
- **The starfish altar**, 1x1: a small marble altar of Poseidon with a dried starfish and a shell.

**New for the runners' house.**
- **The straw pallet**, 1x2, a gray blanket rolled at its head.
- **Sandals on pegs**, 2x1: three pairs hung by their laces.
- **The road map**, 2x2: a scratched plaster panel, roads and towns, tallies in red, the coast in blue and Kalliste off it.
- **The water jar**, 1x2, a bronze ladle hooked on the rim.
- **The back door**, 1x2, with the red finishing ribbon nailed over it.

**New for Euphronios's workshop.**
- **The clay-dust floor**: trodden gray dust (drawn in the clay palette, so it needs no floor colors).
- **The kiln**, 2x3: a brick dome with a fire in its mouth and a spyhole, its chimney up through the roof over the wall.
- **The wheel**, 1x1, caked in clay, a half-painted cup on it.
- **The drying shelves**, 2x2: two long shelves of unpainted cups and jars.
- **The signature**, 2x1: ΕΥΦΡΟΝΙΟΣ in black slip across the plaster under the beam.
- **The paint table**: a trestle with a black amphora half figured in red, two cups, brushes and slip.
- **Slip pots** and **a clay bin**, 1x1 each.

**New for the hiring hall.**
- **The timber wall**: upright planks nailed to rails under the roof beam, on a stone plinth.
- **Crates**, 1x1: plain, of shovels (bronze blades up), of bronze helmets, one with a sickle chalked small on it; and a stack of two, 1x2.
- **The hoist**, 1x3: the sheave at the beam, the rope, the hook over a coil on the floor.
- **The shipshed doors**, 2x2, barred.
- **The pay table**, 2x1: an open ledger of wax tablets, a stylus and a fat purse of silver on the trestle. Its cells are `MB_COUNTER`, so the crew boss is talked to across it.

## How it is made

`tools/ichor/art/limen_art.py` draws the pieces, as `ergasteria_art.py` does: character grids, one character per color, with `tools/ichor/art/char_canvas.py` for the bigger pieces built from shapes. `tools/ichor/art/limen_build.py` defines the two sets and builds them with `ergasteria_build.py`'s machinery, so everything in `TILES_ergasteria.md` ("How it is made") holds here: the rooms are data in Python, ids move freely between builds, and each set must render identically on oikos, aethos and building.

```bash
/usr/bin/python3 tools/ichor/maps/emporion_rooms.py                # all of Emporion's sets and rooms
/usr/bin/python3 tools/ichor/art/limen_build.py --no-compile        # compose and check limen and domos only
```

**A piece in two palettes.** A trestle's goods and its plank are drawn in different palettes: `trestle()` keeps every 8x8 tile in one of them by putting the boundary on a tile row (the goods stop at row 24, the trestle starts there).

## Palettes

oikia's seven, with three purples added to cloth for the Deigma's wool. Every value is a multiple of 8 and none is an aethos color (the builder asserts both).

| Palette | Use | Colors |
|---|---|---|
| wall | oikia's: beams, whitewash, dados, shutters, sky. Also the sea (through windows and under the quay), the ashlar, the warehouse planks, the road map, the notice board | 15 |
| floor | oikia's: terracotta, boards, limestone | 15 |
| wood | oikia's: furniture, bronze fittings, linen, cloth. Also the trestles, crates, the ledger, the sandals, the side couches | 15 |
| clay | oikia's: pottery, hearth, fire, soot, slip. Also the kiln, the wheel, the clay-dust floor, the rack, the lamps, oil and grain | 15 |
| cloth | oikia's rug colors, plus Tyrian purple (3): the wool, the striped curtain | 15 |
| nature | oikia's: plants, wicker, fish, rope. Also the pallets, the tunny, the sacks, the hoist | 15 |
| bronze | oikia's: bronze, flame, water, marble. Also the helmet, both mosaics, the washbasin, the starfish altar | 15 |

## Budget

| Set | Tiles | Metatiles |
|---|---|---|
| limen | 436 of 504 | 192 of 512 |
| domos | 374 of 504 | 152 of 512 |

Tiles 504-511 stay free in both, for door animations.

## Generated tables

The builder rewrites everything between each pair of markers below.

### limen

<!-- limen_build: begin generated -->

Built: **185** metatiles (`0x200`-`0x2b8`) of 512, **436** tiles of 504, palettes 6-12.

| Piece | Metatile |
|---|---|
| floor terracotta, plain | `200` |
| floor terracotta, alt | `201` |
| floor terracotta, top | `202` |
| floor terracotta, left | `203` |
| floor terracotta, corner | `204` |
| floor boards, plain | `205` |
| floor boards, top | `206` |
| floor boards, left | `207` |
| floor boards, corner | `208` |
| floor flags, plain | `209` |
| floor flags, top | `20A` |
| floor flags, left | `20B` |
| floor flags, corner | `20C` |
| floor claydust, plain | `20D` |
| floor claydust, alt | `20E` |
| floor claydust, top | `20F` |
| floor claydust, left | `210` |
| floor claydust, corner | `211` |
| floor sea, plain | `212` |
| floor sea, left | `213` |
| wall red, row 0 | `214` |
| wall red, row 1 | `215` |
| wall blue, row 0 | `214` |
| wall blue, row 1 | `216` |
| wall stone, row 0 | `217` |
| wall stone, row 1 | `218` |
| wall timber, row 0 | `219` |
| wall timber, row 1 | `21A` |
| wall tavern, row 0 | `21B` |
| wall tavern, row 1 | `21C` |
| void (outside the room) | `21D` |
| rug red, top-left | `21E` |
| rug red, top | `21F` |
| rug red, top-right | `220` |
| rug red, left | `221` |
| rug red, middle | `222` |
| rug red, right | `223` |
| rug red, bottom-left | `224` |
| rug red, bottom | `225` |
| rug red, bottom-right | `226` |
| rug blue, top-left | `227` |
| rug blue, top | `228` |
| rug blue, top-right | `229` |
| rug blue, left | `22A` |
| rug blue, middle | `22B` |
| rug blue, right | `22C` |
| rug blue, bottom-left | `22D` |
| rug blue, bottom | `22E` |
| rug blue, bottom-right | `22F` |

| Stamp | Cells | Palette | From | Metatiles (where) | What it is |
|---|---|---|---|---|---|
| `kline` | 2x2 | wood | oikia | 294 295 / 298 299 (widow) | kline (couch-bed): a scrolled headrest with a bronze boss, linen pillow, woven blue coverlet |
| `stool` | 1x1 | wood | oikia | 25D (deigma) | diphros: a folding stool with crossed legs and a fleece seat |
| `table` | 2x1 | wood | oikia | 272 273 (tavern) | trapeza: a low table with bread, a red jug, olives and a cup |
| `desk` | 2x1 | wood | oikia | 25B 25C (deigma) | writing table: a wax tablet with its stylus, a rolled scroll |
| `scrolls` | 2x2 | wood | oikia | 230 231 / 234 235 (deigma) | a cabinet of scrolls in pigeonholes, parchment tags hanging |
| `chest` | 2x2 | wood | oikia | 296 297 / 29A 29B (widow) | kibotos: a wooden chest with bronze straps and painted panels |
| `trident` | 1x2 | bronze | oikia | 289 / 28E (widow) | a trident hung on two pegs |
| `nets` | 2x2 | nature | oikia | 263 264 / 269 26A (tavern) | a fishing net drying on two pegs: cork floats, lead sinkers, a starfish caught in it |
| `kalathos` | 1x1 | nature | oikia | 291 (widow) | kalathos: the wool basket, heaped with carded fleece |
| `amphora` | 1x2 | clay | oikia | 233 / 23B (deigma) | amphora with a black-figure band |
| `amphora_plain` | 1x2 | clay | oikia | 232 / 23A (deigma) | a plain oil amphora |
| `pithos` | 1x2 | clay | oikia | 239 / 23E (deigma) | pithos: a big storage jar with rope-pattern bands and a stone lid |
| `fish_basket` | 1x1 | nature | oikia | 282 (tavern) | a wicker basket of the morning's catch |
| `lampstand` | 1x2 | bronze | oikia | 27C / 27F (tavern) | lychnouchos: a bronze lampstand on lion-paw feet, lamp lit |
| `column` | 1x3 | bronze | oikia | 23F / 246 / 24D (deigma) | a Doric post of whitewashed stone, holding up the beam |
| `mat` | 2x1 | nature | oikia | 25F 260 (deigma) | woven reed mat at the door; both cells are south-arrow warps |
| `bench` | 2x1 | wood | ergasteria | 26E 26F (tavern) | a long wooden bench |
| `scales` | 1x2 | bronze | ergasteria | 238 / 23D (deigma) | a moneyer's balance: silver in one pan, a bronze weight in the other |
| `trestle_lamps` | 2x2 | clay | limen | 242 243 / 249 24A (deigma) | Lampis's trestle: a stepped stand of clay oil lamps |
| `trestle_oil` | 2x2 | clay | limen | 244 245 / 24B 24C (deigma) | a trestle of oil samples: three transport amphorae and a stoppered flask |
| `trestle_wool` | 2x2 | cloth | limen | 240 241 / 247 248 (deigma) | the wool merchant's trestle: bolts of Tyrian purple, saffron, madder and blue |
| `trestle_helmet` | 2x2 | bronze | limen | 250 251 / 257 258 (deigma) | a trestle with a single bronze helmet on a stand, a red crest on it |
| `trestle_grain` | 2x2 | clay | limen | 24E 24F / 255 256 (deigma) | the grain merchant's trestle: open sacks of barley and wheat, a bowl of first fruits |
| `trestle_ledger` | 2x1 | wood | limen | 2B0 2B1 (hiring_hall) | the crew boss's pay table: an open ledger of wax tablets and a fat purse of silver; a counter, so he's talked to across it |
| `fish_mounted` | 2x1 | nature | limen | 236 237 (deigma) | a stuffed tunny mounted on a board, glass-eyed, as big as a boy |
| `notice_board` | 1x2 | wall | limen | 254 / 25A (deigma) | the public notice board by the door: a whitened board, a sheet sealed with the Archon's owl |
| `sea_window` | 2x2 | wall | limen | 265 266 / 26B 26C (tavern) | a wide window on the harbor: the shutters open, the sea under the sill, a sail out on it |
| `amphora_rack` | 2x2 | clay | limen | 261 262 / 267 268 (tavern) | a timber rack of wine amphorae laid two high, mouths out |
| `dolphin_mosaic` | 4x2 | bronze | limen | 275 276 277 278 / 279 27A 27A 27B (tavern) | a pebble mosaic of a leaping dolphin over the waves: the tavern's sign, on its floor |
| `bones_table` | 2x1 | wood | limen | 27D 27E (tavern) | the knucklebones table: its top worn pale in a hollow where the bones land, four bones in it |
| `sack` | 1x1 | nature | limen | 252 (deigma) | a sack of grain tied at the neck |
| `krater` | 1x2 | clay | limen | 26D / 270 (tavern) | a big black-figure krater on a stone stand, for mixing the wine with water |
| `oar_hung` | 2x1 | wood | limen | 287 288 (widow) | a single oar hung on two pegs under the beam, its blade painted blue: her husband's |
| `starfish_altar` | 1x1 | bronze | limen | 293 (widow) | a little marble altar of Poseidon: a dried starfish and a shell on it |
| `loom_shroud` | 2x3 | wood | limen | 283 284 / 28A 28B / 28F 290 (widow) | the upright loom with a half-finished shroud of plain linen on it |
| `crate` | 1x1 | wood | limen | 2B4 (hiring_hall) | a plank crate, nailed shut |
| `crate_shovels` | 1x1 | wood | limen | 2A8 (hiring_hall) | a crate of new shovels, their bronze blades up |
| `crate_helmets` | 1x1 | wood | limen | 2AB (hiring_hall) | a crate heaped with bronze helmets |
| `crate_sickle` | 1x1 | wood | limen | 2AD (hiring_hall) | a crate with a sickle chalked small on it, almost hidden |
| `crate_stack` | 1x2 | wood | limen | 2A3 / 2A7 (hiring_hall) | two crates stacked |
| `hoist` | 1x3 | nature | limen | 2A0 / 2A4 / 2A9 (hiring_hall) | a rope-and-pulley hoist: the sheave at the beam, the rope, a hook over a coil on the floor |
| `shed_doors` | 2x2 | wood | limen | 2A1 2A2 / 2A5 2A6 (hiring_hall) | the great double doors out to the shipsheds, barred from inside |

<!-- limen_build: end generated -->

### domos

<!-- domos_build: begin generated -->

Built: **166** metatiles (`0x200`-`0x2a5`) of 512, **412** tiles of 504, palettes 6-12.

| Piece | Metatile |
|---|---|
| floor terracotta, plain | `200` |
| floor terracotta, alt | `201` |
| floor terracotta, top | `202` |
| floor terracotta, left | `203` |
| floor terracotta, corner | `204` |
| floor boards, plain | `205` |
| floor boards, top | `206` |
| floor boards, left | `207` |
| floor boards, corner | `208` |
| floor flags, plain | `209` |
| floor flags, top | `20A` |
| floor flags, left | `20B` |
| floor flags, corner | `20C` |
| floor claydust, plain | `20D` |
| floor claydust, alt | `20E` |
| floor claydust, top | `20F` |
| floor claydust, left | `210` |
| floor claydust, corner | `211` |
| floor sea, plain | `212` |
| floor sea, left | `213` |
| wall red, row 0 | `214` |
| wall red, row 1 | `215` |
| wall blue, row 0 | `214` |
| wall blue, row 1 | `216` |
| wall stone, row 0 | `217` |
| wall stone, row 1 | `218` |
| wall timber, row 0 | `219` |
| wall timber, row 1 | `21A` |
| wall tavern, row 0 | `21B` |
| wall tavern, row 1 | `21C` |
| void (outside the room) | `21D` |
| rug red, top-left | `21E` |
| rug red, top | `21F` |
| rug red, top-right | `220` |
| rug red, left | `221` |
| rug red, middle | `222` |
| rug red, right | `223` |
| rug red, bottom-left | `224` |
| rug red, bottom | `225` |
| rug red, bottom-right | `226` |
| rug blue, top-left | `227` |
| rug blue, top | `228` |
| rug blue, top-right | `229` |
| rug blue, left | `22A` |
| rug blue, middle | `22B` |
| rug blue, right | `22C` |
| rug blue, bottom-left | `22D` |
| rug blue, bottom | `22E` |
| rug blue, bottom-right | `22F` |

| Stamp | Cells | Palette | From | Metatiles (where) | What it is |
|---|---|---|---|---|---|
| `window` | 1x2 | wall | oikia | 230 / 234 (philoxenos) | shuttered window, Aegean-blue shutters open |
| `niche` | 1x2 | wall | oikia | 231 / 235 (philoxenos) | wall niche with a terracotta goddess and an aryballos |
| `kline` | 2x2 | wood | oikia | 238 239 / 23E 23F (philoxenos) | kline (couch-bed): a scrolled headrest with a bronze boss, linen pillow, woven blue coverlet |
| `stool` | 1x1 | wood | oikia | 272 (runners) | diphros: a folding stool with crossed legs and a fleece seat |
| `table` | 2x1 | wood | oikia | 273 274 (runners) | trapeza: a low table with bread, a red jug, olives and a cup |
| `table_round` | 1x1 | wood | oikia | 246 (philoxenos) | a small three-legged table with a jug and bread |
| `klepsydra` | 1x2 | bronze | oikia | 263 / 269 (runners) | klepsydra: a bronze bowl drips into a basin past a marble hour scale |
| `amphora` | 1x2 | clay | oikia | 23D / 244 (philoxenos) | amphora with a black-figure band |
| `amphora_plain` | 1x2 | clay | oikia | 275 / 278 (runners) | a plain oil amphora |
| `pithos` | 1x2 | clay | oikia | 28F / 291 (potter) | pithos: a big storage jar with rope-pattern bands and a stone lid |
| `pots` | 1x1 | clay | oikia | 241 (philoxenos) | cooking pots: a sooty chytra, a jug and a stack of bowls |
| `hearth` | 2x2 | clay | oikia | 23B 23C / 242 243 (philoxenos) | kitchen hearth: Hestia's fire in a stone curb, a bronze cauldron on its tripod |
| `soot` | 2x2 | clay | oikia | 232 233 / 236 237 (philoxenos) | smoke-blackened plaster above the hearth |
| `lampstand` | 1x2 | bronze | oikia | 258 / 25C (philoxenos) | lychnouchos: a bronze lampstand on lion-paw feet, lamp lit |
| `column` | 1x3 | bronze | oikia | 23A / 240 / 248 (philoxenos) | a Doric post of whitewashed stone, holding up the beam |
| `mat` | 2x1 | nature | oikia | 25E 25F (philoxenos) | woven reed mat at the door; both cells are south-arrow warps |
| `bench` | 2x1 | wood | ergasteria | 276 277 (runners) | a long wooden bench |
| `trestle_cups` | 2x2 | clay | limen | 287 288 / 28B 28C (potter) | Euphronios's paint table: a black amphora with a red figure half done, cups, brushes |
| `amphora_rack` | 2x2 | clay | limen | 295 296 / 299 29A (rest_house) | a timber rack of wine amphorae laid two high, mouths out |
| `sack` | 1x1 | nature | limen | 29F (rest_house) | a sack of grain tied at the neck |
| `louterion` | 1x2 | bronze | limen | 259 / 25D (philoxenos) | a marble washbasin on its pillar by the door, a bronze jug beside it |
| `krater` | 1x2 | clay | limen | 24B / 251 (philoxenos) | a big black-figure krater on a stone stand, for mixing the wine with water |
| `kline_side` | 1x2 | wood | limen | 245 / 249 (philoxenos) | a dining couch along the side wall: scrolled headrest, linen bolster, blue coverlet |
| `kline_side_r` | 1x2 | wood | limen | 247 / 24A (philoxenos) | the same couch along the other wall |
| `host_mosaic` | 4x2 | bronze | limen | 24C 24D 24E 24F / 252 253 254 255 (philoxenos) | a pebble mosaic of a host stepping out of his door to greet a traveler: xenia, in the floor |
| `curtain_bed` | 2x2 | cloth | limen | 256 257 / 25A 25B (philoxenos) | the guest bed behind a striped curtain, the near half drawn back |
| `pallet` | 1x2 | nature | limen | 26B / 26E (runners) | a runner's straw pallet, a gray blanket rolled at its head |
| `sandals_pegs` | 2x1 | wood | limen | 264 265 (runners) | sandals hung in pairs by their laces from the pegs, ready for the road |
| `road_map` | 2x2 | wall | limen | 260 261 / 266 267 (runners) | every road in Aethos scratched into the plaster, the distances in stades tallied beside them |
| `water_jar` | 1x2 | clay | limen | 26A / 26D (runners) | a big water jar, a bronze ladle hooked over its rim |
| `ribbon_door` | 1x2 | wall | limen | 262 / 268 (runners) | the back door to the yard, the red finishing ribbon nailed across its lintel |
| `kiln` | 2x3 | clay | limen | 27D 27E / 281 282 / 283 284 (potter) | the domed kiln, its chimney up through the roof and a fire in its mouth |
| `wheel` | 1x1 | clay | limen | 292 (potter) | the potter's wheel, caked in clay, a half-painted cup turning on it |
| `slip_pots` | 1x1 | clay | limen | 290 (potter) | pots of black slip, the brushes left standing in them |
| `drying_shelf` | 2x2 | clay | limen | 279 27A / 27F 280 (potter) | long shelves of new cups and jars drying, not yet painted |
| `scrawl` | 2x1 | wall | limen | 27B 27C (potter) | EUPHRONIOS PAINTED ME, scrawled in black slip on the plaster (here, the first word) |
| `clay_bin` | 1x1 | clay | limen | 28D (potter) | a stone basin of wet clay, kneaded and waiting |
| `crate` | 1x1 | wood | limen | 2A5 (rest_house) | a plank crate, nailed shut |
| `shed_doors` | 2x2 | wood | limen | 297 298 / 29B 29C (rest_house) | the great double doors out to the shipsheds, barred from inside |

<!-- domos_build: end generated -->
