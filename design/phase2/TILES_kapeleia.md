# gTileset_Kapeleia and gTileset_Nysa

Two secondaries built by `tools/ichor/art/kapeleia_build.py` (via `tools/ichor/maps/kapeleia_rooms.py`) from `tools/ichor/art/kapeleia_art.py`: limen's palettes and pieces, plus the market stall kit (five awning colorways, nine goods rows, the shared plank counter), the trapeza, the fountain, banners, floor baskets, bales, rolled carpets, and the nursery's liknon, Egg baskets, ivy, fawn skin and thyrsoi. kapeleia holds the Great Deigma alone (the stalls fill most of a set); nysa holds the Nursery of Nysa. Both are on palettes 6-12 and render the same on oikos, aethos and building.

A stall is four stamps: `awning_<colorway>` (3x2), `goods_<stall>` (3x1, the seller stands in the middle cell, which is drawn in the top layer so the goods stand in front of their legs) and `stall_counter` (3x1, MB_COUNTER, talked across from the row below).

<!-- kapeleia_build: begin generated -->

Built: **196** metatiles (`0x200`-`0x2c3`) of 512, **423** tiles of 504, palettes 6-12.

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
| `window` | 1x2 | wall | limen | 230 / 236 (great_deigma) | shuttered window, Aegean-blue shutters open |
| `column` | 1x3 | bronze | limen | 27A / 280 / 289 (great_deigma) | a Doric post of whitewashed stone, holding up the beam |
| `amphora` | 1x2 | clay | limen | 260 / 276 (great_deigma) | amphora with a black-figure band |
| `amphora_plain` | 1x2 | clay | limen | 264 / 277 (great_deigma) | a plain oil amphora |
| `pithos` | 1x2 | clay | limen | 271 / 279 (great_deigma) | pithos: a big storage jar with rope-pattern bands and a stone lid |
| `sack` | 1x1 | nature | limen | 278 (great_deigma) | a sack of grain tied at the neck |
| `crate_stack` | 1x2 | wood | limen | 25C / 272 (great_deigma) | two crates stacked |
| `scales` | 1x2 | bronze | limen | 243 / 255 (great_deigma) | a moneyer's balance: silver in one pan, a bronze weight in the other |
| `notice_board` | 1x2 | wall | limen | 233 / 242 (great_deigma) | the public notice board by the door: a whitened board, a sheet sealed with the Archon's owl |
| `mat` | 2x1 | nature | limen | 2C0 2C1 (great_deigma) | woven reed mat at the door; both cells are south-arrow warps |
| `lampstand` | 1x2 | bronze | limen | 27F / 288 (great_deigma) | lychnouchos: a bronze lampstand on lion-paw feet, lamp lit |
| `trestle_oil` | 2x2 | clay | limen | 2AB 2AC / 2B6 2B7 (great_deigma) | a trestle of oil samples: three transport amphorae and a stoppered flask |
| `trestle_grain` | 2x2 | clay | limen | 2BE 2BF / 2C2 2C3 (great_deigma) | the grain merchant's trestle: open sacks of barley and wheat, a bowl of first fruits |
| `amphora_rack` | 2x2 | clay | limen | 291 292 / 29B 29C (great_deigma) | a timber rack of wine amphorae laid two high, mouths out |
| `dolphin_mosaic` | 4x2 | bronze | limen | 296 297 298 299 / 29D 29E 29E 29F (great_deigma) | a pebble mosaic of a leaping dolphin over the waves: the tavern's sign, on its floor |
| `awning_red` | 3x2 | cloth | kapeleia | 23F 240 241 / 252 253 254 (great_deigma) | a stall's awning, red and white stripes on two posts |
| `awning_blue` | 3x2 | cloth | kapeleia | 23B 23C 23D / 24F 250 251 (great_deigma) | a stall's awning, blue and white stripes on two posts |
| `awning_purple` | 3x2 | cloth | kapeleia | 237 238 239 / 24C 24D 24E (great_deigma) | a stall's awning, purple and white stripes on two posts |
| `awning_saffron` | 3x2 | cloth | kapeleia | 248 249 24A / 259 25A 25B (great_deigma) | a stall's awning, saffron and white stripes on two posts |
| `awning_green` | 3x2 | cloth | kapeleia | 244 245 246 / 256 257 258 (great_deigma) | a stall's awning, green and white stripes on two posts |
| `stall_counter` | 3x1 | wood | kapeleia | 273 274 275 (great_deigma) | a stall's plank counter, talked across to the seller behind it |
| `goods_phoenician` | 3x1 | wood | kapeleia | 25D --- 25F (great_deigma) | Tyrian purple, murex shells, Sidonian glass, cedar |
| `goods_egyptian` | 3x1 | wood | kapeleia | 261 --- 263 (great_deigma) | papyrus, a faience scarab and beads, alabaster jars |
| `goods_scythian` | 3x1 | wood | kapeleia | 265 --- 267 (great_deigma) | furs, a gold stag plaque, a red bow case |
| `goods_stones` | 3x1 | wood | kapeleia | 268 --- 26A (great_deigma) | evolution stones laid out: Fire, Sun, Water, Thunder, Leaf, Moon |
| `goods_tablets` | 3x1 | wood | kapeleia | 26B --- 26D (great_deigma) | wax tablets, a stylus, a scroll case, a bronze star sphere |
| `goods_berries` | 3x1 | wood | kapeleia | 26E --- 270 (great_deigma) | baskets of Oran, Pecha, Cheri and Sitrus berries |
| `goods_curios` | 3x1 | wood | kapeleia | 293 --- 295 (great_deigma) | an open chest of gold, a glass egg, a peacock feather, a jar |
| `goods_spices` | 3x1 | wood | kapeleia | 2B3 --- 2B5 (great_deigma) | saffron, sumac, cumin and salt heaped in bowls |
| `goods_pottery` | 3x1 | wood | kapeleia | 2B8 --- 2BA (great_deigma) | Athenian pots: a black-figure amphora, a cup, a lekythos, plates |
| `trapeza` | 3x2 | wood | kapeleia | 28E --- 290 / 273 274 275 (great_deigma) | the money-changer's trapeza: coin stacks of bronze, silver and gold, a touchstone |
| `fountain` | 3x2 | bronze | kapeleia | 281 282 283 / 28A 28B 28C (great_deigma) | the market's fountain: a marble basin under a lion's head spout |
| `banner_red` | 1x2 | cloth | kapeleia | 235 / 24B (great_deigma) | a red banner hung on the wall |
| `banner_blue` | 1x2 | cloth | kapeleia | 232 / 23E (great_deigma) | a blue banner hung on the wall |
| `banner_purple` | 1x2 | cloth | kapeleia | 231 / 23A (great_deigma) | a purple banner hung on the wall |
| `banner_green` | 1x2 | cloth | kapeleia | 234 / 247 (great_deigma) | a green banner hung on the wall |
| `baskets_floor` | 2x1 | nature | kapeleia | 2BC 2BD (great_deigma) | baskets of figs and onions on the floor |
| `bales` | 2x2 | cloth | kapeleia | 2A6 2A7 / 2B1 2B2 (great_deigma) | bales of raw wool, roped |
| `carpets_rolled` | 1x2 | cloth | kapeleia | 27B / 284 (great_deigma) | rolled carpets stood on end |

<!-- kapeleia_build: end generated -->

<!-- nysa_build: begin generated -->

Built: **103** metatiles (`0x200`-`0x266`) of 512, **268** tiles of 504, palettes 6-12.

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
| `window` | 1x2 | wall | limen | 232 / 23C (nursery) | shuttered window, Aegean-blue shutters open |
| `mat` | 2x1 | nature | limen | 265 266 (nursery) | woven reed mat at the door; both cells are south-arrow warps |
| `stool` | 1x1 | wood | limen | 25C (nursery) | diphros: a folding stool with crossed legs and a fleece seat |
| `table` | 2x1 | wood | limen | 25A 25B (nursery) | trapeza: a low table with bread, a red jug, olives and a cup |
| `kline` | 2x2 | wood | limen | 256 257 / 25F 260 (nursery) | kline (couch-bed): a scrolled headrest with a bronze boss, linen pillow, woven blue coverlet |
| `loom` | 2x3 | wood | limen | 230 231 / 23A 23B / 242 243 (nursery) | warp-weighted loom: a half-woven cloth, the warp, clay loom weights |
| `hearth` | 2x2 | clay | limen | 246 247 / 24E 24F (nursery) | kitchen hearth: Hestia's fire in a stone curb, a bronze cauldron on its tripod |
| `soot` | 2x2 | clay | limen | 238 239 / 240 241 (nursery) | smoke-blackened plaster above the hearth |
| `jar_shelf` | 2x2 | wood | limen | 234 235 / 23E 23F (nursery) | wall shelf of remedy jars and flasks |
| `herbs` | 1x2 | nature | limen | 233 / 23D (nursery) | bundles of drying herbs hung from pegs in the beam |
| `myrtle` | 1x2 | nature | limen | 244 / 24C (nursery) | potted myrtle, Aphrodite's shrub, in flower |
| `kalathos` | 1x1 | nature | limen | 263 (nursery) | kalathos: the wool basket, heaped with carded fleece |
| `krater` | 1x2 | clay | limen | 245 / 24D (nursery) | a big black-figure krater on a stone stand, for mixing the wine with water |
| `water_jar` | 1x2 | clay | limen | 25D / 264 (nursery) | a big water jar, a bronze ladle hooked over its rim |
| `pots` | 1x1 | clay | limen | 254 (nursery) | cooking pots: a sooty chytra, a jug and a stack of bowls |
| `stall_counter` | 3x1 | wood | kapeleia | 249 24A 24B (nursery) | a stall's plank counter, talked across to the seller behind it |
| `liknon` | 2x1 | nature | kapeleia | 250 251 (nursery) | the liknon: a winnowing-basket cradle with an Egg in it |
| `nest_basket` | 1x1 | nature | kapeleia | 248 (nursery) | a straw basket of Eggs |
| `ivy` | 2x1 | nature | kapeleia | 236 237 (nursery) | a swag of ivy along the wall, a bunch of grapes |
| `nebris` | 2x2 | cloth | kapeleia | 258 259 / 261 262 (nursery) | a dappled fawn skin on the floor |
| `thyrsoi` | 1x2 | nature | kapeleia | 255 / 25E (nursery) | thyrsoi, ivy-wound staffs tipped with pine cones |

<!-- nysa_build: end generated -->
