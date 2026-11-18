# Lakonia's room tilesets

`gTileset_OikiaGytheion`, `gTileset_OikiaLakonia` and `gTileset_CivicLakonia`, the
secondaries for Gytheion's and Lakonia's fifteen rooms, pair with `gTileset_Oikos`.
Each uses only its own tiles and palettes 6-12. They are written by
`tools/ichor/maps/lakonia_rooms.py` from `tools/ichor/art/lakonia_rooms_art.py`;
the rooms themselves are in `ROOMS_lakonia.md`. Metatile ids move whenever a room
changes, so scripts use the labels in `include/constants/metatile_labels.h`, never
raw ids. The tables below are generated.

Sheets: `design/phase4/img/rooms_lakonia/oikia_gytheion_sheet.png`, `oikia_lakonia_sheet.png`,
`civic_lakonia_sheet.png`.

## gTileset_OikiaGytheion

<!-- oikia_gytheion_build: begin generated -->

Built: **149** metatiles (`0x200`-`0x294`) of 512, **375** tiles of 504, palettes 6-12.

| Piece | Metatile |
|---|---|
| floor flags, plain | `200` |
| floor flags, top | `201` |
| floor flags, left | `202` |
| floor flags, corner | `203` |
| floor boards, plain | `204` |
| floor boards, top | `205` |
| floor boards, left | `206` |
| floor boards, corner | `207` |
| floor terracotta, plain | `208` |
| floor terracotta, alt | `209` |
| floor terracotta, top | `20A` |
| floor terracotta, left | `20B` |
| floor terracotta, corner | `20C` |
| floor sea, plain | `20D` |
| floor sea, left | `20E` |
| wall stone, row 0 | `20F` |
| wall stone, row 1 | `210` |
| wall blue, row 0 | `211` |
| wall blue, row 1 | `212` |
| wall red, row 0 | `211` |
| wall red, row 1 | `213` |
| wall white, row 0 | `214` |
| wall white, row 1 | `215` |
| void (outside the room) | `216` |
| rug red, top-left | `217` |
| rug red, top | `218` |
| rug red, top-right | `219` |
| rug red, left | `21A` |
| rug red, middle | `21B` |
| rug red, right | `21C` |
| rug red, bottom-left | `21D` |
| rug red, bottom | `21E` |
| rug red, bottom-right | `21F` |

| Stamp | Cells | Palette | From | Metatiles (where) | What it is |
|---|---|---|---|---|---|
| `window` | 1x2 | wall | oikia | 26F / 274 (Gytheion_TimaiaHouse) | shuttered window, Aegean-blue shutters open |
| `kline` | 2x2 | wood | oikia | 264 265 / 267 268 (Gytheion_LysandrosHouse) | kline (couch-bed): a scrolled headrest with a bronze boss, linen pillow, woven blue coverlet |
| `stool` | 1x1 | wood | oikia | 27B (Gytheion_TimaiaHouse) | diphros: a folding stool with crossed legs and a fleece seat |
| `table` | 2x1 | wood | oikia | 262 263 (Gytheion_LysandrosHouse) | trapeza: a low table with bread, a red jug, olives and a cup |
| `amphora` | 1x2 | clay | oikia | 23C / 23E (Gytheion_Asclepeion) | amphora with a black-figure band |
| `amphora_plain` | 1x2 | clay | oikia | 24F / 251 (Gytheion_Dyeworks) | a plain oil amphora |
| `pithos` | 1x2 | clay | oikia | 231 / 235 (Gytheion_Asclepeion) | pithos: a big storage jar with rope-pattern bands and a stone lid |
| `myrtle` | 1x2 | nature | oikia | 239 / 23D (Gytheion_Asclepeion) | potted myrtle, Aphrodite's shrub, in flower |
| `lampstand` | 1x2 | bronze | oikia | 22A / 232 (Gytheion_Asclepeion) | lychnouchos: a bronze lampstand on lion-paw feet, lamp lit |
| `mat` | 2x1 | nature | oikia | 23F 240 (Gytheion_Asclepeion) | woven reed mat at the door; both cells are south-arrow warps |
| `jar_shelf` | 2x2 | wood | oikia | 270 271 / 275 276 (Gytheion_TimaiaHouse) | wall shelf of remedy jars and flasks |
| `klismos_r` | 1x1 | wood | oikia | 261 (Gytheion_LysandrosHouse) | klismos chair, facing right |
| `oars` | 1x3 | wood | oikia | 260 / 266 / 269 (Gytheion_LysandrosHouse) | a pair of oars with blue-painted blades, leaning on the wall |
| `bench` | 2x1 | wood | ergasteria | 23A 23B (Gytheion_Asclepeion) | a long wooden bench |
| `sea_window` | 2x2 | wall | limen | 255 256 / 25C 25D (Gytheion_LysandrosHouse) | a wide window on the harbor: the shutters open, the sea under the sill, a sail out on it |
| `water_jar` | 1x2 | clay | limen | 26A / 26B (Gytheion_LysandrosHouse) | a big water jar, a bronze ladle hooked over its rim |
| `basin_stone` | 2x2 | bronze | lakonia_rooms | 22B 22C / 233 234 (Gytheion_Asclepeion) | a stone basin of cold spring water. Nothing else |
| `flat_palace` | 2x2 | wall | lakonia_rooms | 220 221 / 226 227 (Gytheion_Asclepeion) | a painted scenery flat: a palace |
| `flat_sea` | 2x2 | wall | lakonia_rooms | 222 223 / 228 229 (Gytheion_Asclepeion) | a painted scenery flat: the sea, and a ship on it |
| `theater_window` | 2x2 | wall | lakonia_rooms | 224 225 / 22F 230 (Gytheion_Asclepeion) | a window over the theater's front rows, where patients sit in the sun |
| `tickets_L` | 1x1 | wood | lakonia_rooms | 236 (Gytheion_Asclepeion) | the old ticket counter; the healer's counter now |
| `tickets_M` | 1x1 | wood | lakonia_rooms | 237 (Gytheion_Asclepeion) | the old ticket counter; the healer's counter now |
| `tickets_R` | 1x1 | wood | lakonia_rooms | 238 (Gytheion_Asclepeion) | the old ticket counter; the healer's counter now |
| `vat` | 2x2 | cloth | lakonia_rooms | 245 246 / 249 24A (Gytheion_Dyeworks) | a lead dye vat steaming over a low fire, purple to the brim |
| `shell_heap` | 2x2 | cloth | lakonia_rooms | 247 248 / 24B 24C (Gytheion_Dyeworks) | a heap of crushed murex shells: ten thousand snails for one cloak |
| `skeins` | 2x2 | cloth | lakonia_rooms | 241 242 / 243 244 (Gytheion_Dyeworks) | skeins of wool hanging from the rafters, pink to nearly black |
| `hank_stool` | 1x1 | wood | lakonia_rooms | 250 (Gytheion_Dyeworks) | a stool with one finished hank of true purple on it, under a cloth |
| `gulf_map` | 3x2 | wall | lakonia_rooms | 252 253 254 / 259 25A 25B (Gytheion_LysandrosHouse) | a map of the gulf scratched into the plaster, every rock and current marked |
| `trireme_shelf` | 2x2 | wood | lakonia_rooms | 257 258 / 25E 25F (Gytheion_LysandrosHouse) | three model triremes on a shelf |
| `ram` | 1x1 | bronze | lakonia_rooms | 26E (Gytheion_LysandrosHouse) | a bronze ship's ram, used as a doorstop |
| `bread_oven` | 2x2 | clay | lakonia_rooms | 272 273 / 277 278 (Gytheion_TimaiaHouse) | a bread oven built into the corner, warm |
| `toy_spear` | 1x2 | wood | lakonia_rooms | 27F / 283 (Gytheion_TimaiaHouse) | a child's wooden spear propped behind the door |
| `cake_table` | 2x1 | wood | lakonia_rooms | 27C 27D (Gytheion_TimaiaHouse) | the table, and on it a cloth over something fig-shaped |
| `bench_nets` | 2x1 | wood | lakonia_rooms | 279 27A (Gytheion_TimaiaHouse) | nets mended and folded on a bench |
| `dove_niche` | 1x2 | wall | lakonia_rooms | 287 / 28D (Gytheion_KranaiShrine) | a niche with two clay doves in it |
| `sandals_a` | 2x2 | wall | lakonia_rooms | 284 285 / 28A 28B (Gytheion_KranaiShrine) | a hundred tiny votive sandals on strings |
| `sandals_b` | 2x2 | wall | lakonia_rooms | 288 289 / 28E 28F (Gytheion_KranaiShrine) | votive sandals on strings, left by runaways |
| `mask_pegs` | 2x1 | wall | lakonia_rooms | 22D 22E (Gytheion_Asclepeion) | old theater masks on pegs: comic, tragic, a king's |

<!-- oikia_gytheion_build: end generated -->

## gTileset_OikiaLakonia

<!-- oikia_lakonia_build: begin generated -->

Built: **101** metatiles (`0x200`-`0x264`) of 512, **279** tiles of 504, palettes 6-12.

| Piece | Metatile |
|---|---|
| floor earth, plain | `200` |
| floor earth, alt | `201` |
| floor earth, top | `202` |
| floor earth, left | `203` |
| floor earth, corner | `204` |
| wall lakon, row 0 | `205` |
| wall lakon, row 1 | `206` |
| wall smoke, row 0 | `207` |
| wall smoke, row 1 | `208` |
| wall sayings, row 0 | `209` |
| wall sayings, row 1 | `20A` |
| void (outside the room) | `20B` |
| rug red, top-left | `20C` |
| rug red, top | `20D` |
| rug red, top-right | `20E` |
| rug red, left | `20F` |
| rug red, middle | `210` |
| rug red, right | `211` |
| rug red, bottom-left | `212` |
| rug red, bottom | `213` |
| rug red, bottom-right | `214` |

| Stamp | Cells | Palette | From | Metatiles (where) | What it is |
|---|---|---|---|---|---|
| `stool` | 1x1 | wood | oikia | 230 (Lakonia_ChilonHouse) | diphros: a folding stool with crossed legs and a fleece seat |
| `table` | 2x1 | wood | oikia | 231 232 (Lakonia_LampitosHouse) | trapeza: a low table with bread, a red jug, olives and a cup |
| `chest` | 2x2 | wood | oikia | 229 22A / 22E 22F (Lakonia_LampitosHouse) | kibotos: a wooden chest with bronze straps and painted panels |
| `amphora` | 1x2 | clay | oikia | 253 / 257 (Lakonia_LichasHouse) | amphora with a black-figure band |
| `amphora_plain` | 1x2 | clay | oikia | 228 / 22D (Lakonia_LampitosHouse) | a plain oil amphora |
| `pots` | 1x1 | clay | oikia | 227 (Lakonia_LampitosHouse) | cooking pots: a sooty chytra, a jug and a stack of bowls |
| `soot` | 2x2 | clay | oikia | 217 218 / 21F 220 (Lakonia_LampitosHouse) | smoke-blackened plaster above the hearth |
| `kalathos` | 1x1 | nature | oikia | 247 (Lakonia_ChilonHouse) | kalathos: the wool basket, heaped with carded fleece |
| `lampstand` | 1x2 | bronze | oikia | 243 / 246 (Lakonia_ChilonHouse) | lychnouchos: a bronze lampstand on lion-paw feet, lamp lit |
| `mat` | 2x1 | nature | oikia | 235 236 (Lakonia_LampitosHouse) | woven reed mat at the door; both cells are south-arrow warps |
| `table_round` | 1x1 | wood | oikia | 245 (Lakonia_ChilonHouse) | a small three-legged table with a jug and bread |
| `water_jar` | 1x2 | clay | limen | 233 / 234 (Lakonia_LampitosHouse) | a big water jar, a bronze ladle hooked over its rim |
| `curtain_bed` | 2x2 | cloth | limen | 24A 24B / 24E 24F (Lakonia_LichasHouse) | the guest bed behind a striped curtain, the near half drawn back |
| `pallet` | 1x2 | nature | limen | 242 / 244 (Lakonia_ChilonHouse) | a runner's straw pallet, a gray blanket rolled at its head |
| `stele_agis` | 1x2 | wall | lakonia_rooms | 219 / 221 (Lakonia_LampitosHouse) | a grave-stele painted on the plaster: AGIS, IN WAR (only the war dead get names) |
| `stele_swallow` | 1x2 | wall | lakonia_rooms | 21A / 222 (Lakonia_LampitosHouse) | a grave-stele painted on the plaster, with no name: a small swallow |
| `loom_cloak` | 2x3 | wood | lakonia_rooms | 215 216 / 21C 21D / 223 224 (Lakonia_LampitosHouse) | a loom with a small red cloak on it. Too small for anyone in this house |
| `hearth_cold` | 2x2 | clay | lakonia_rooms | 225 226 / 22B 22C (Lakonia_LampitosHouse) | a hearth of stones, cold: ash, and nobody's lit it in a long time |
| `hearth_lit` | 2x2 | clay | lakonia_rooms | 24C 24D / 250 251 (Lakonia_LichasHouse) | the same hearth, lit: someone's home |
| `staff_rack` | 3x2 | wood | lakonia_rooms | 237 238 239 / 23A 23B 23C (Lakonia_GylipposHouse) | the elders' scytale staffs on pegs: a dozen, all exactly as thick, a name burned into each |
| `sleeping_mat` | 1x2 | nature | lakonia_rooms | 23D / 23F (Lakonia_GylipposHouse) | a sleeping mat of cut reeds on the bare floor |
| `stool_strap` | 1x1 | wood | lakonia_rooms | 23E (Lakonia_GylipposHouse) | Gylippos's stool, a leather strap coiled on it |
| `if_shelf` | 1x2 | clay | lakonia_rooms | 240 / 241 (Lakonia_ChilonHouse) | a pottery shard on a shelf with one word on it: IF |
| `cushions` | 2x1 | cloth | lakonia_rooms | 254 255 (Lakonia_LichasHouse) | a heap of cushions. The only cushions in Lakonia; the neighbors find them suspicious |
| `tripod` | 1x2 | bronze | lakonia_rooms | 248 / 249 (Lakonia_LichasHouse) | a bronze tripod from Olympia, with someone else's name on it |
| `figs` | 1x1 | nature | lakonia_rooms | 252 (Lakonia_LichasHouse) | a basket of figs |
| `plank_L` | 1x1 | wood | lakonia_rooms | 260 (Lakonia_Syssition) | the mess table: one long plank on trestles |
| `plank_M` | 1x1 | wood | lakonia_rooms | 261 (Lakonia_Syssition) | the mess table: one long plank on trestles |
| `plank_R` | 1x1 | wood | lakonia_rooms | 262 (Lakonia_Syssition) | the mess table: one long plank on trestles |
| `cup_pegs` | 2x1 | clay | lakonia_rooms | 259 25A (Lakonia_Syssition) | clay cups on pegs, one for every man's place |
| `cauldron` | 2x2 | clay | lakonia_rooms | 25C 25D / 25E 25F (Lakonia_Syssition) | the black cauldron over the fire: black broth, the worst soup in the world |
| `barley` | 1x2 | wood | lakonia_rooms | 258 / 25B (Lakonia_Syssition) | a barrel of barley |
| `stool_seat` | 1x1 | wood | lakonia_rooms | 230 (Lakonia_LampitosHouse) | a stool (walkable: whoever stands on it sits) |
| `wall_worn` | 1x1 | wall | lakonia_rooms | 21E (Lakonia_LampitosHouse) | plaster fallen off the brick |

<!-- oikia_lakonia_build: end generated -->

## gTileset_CivicLakonia

<!-- civic_lakonia_build: begin generated -->

Built: **108** metatiles (`0x200`-`0x26b`) of 512, **254** tiles of 504, palettes 6-12.

| Piece | Metatile |
|---|---|
| floor flags, plain | `200` |
| floor flags, top | `201` |
| floor flags, left | `202` |
| floor flags, corner | `203` |
| floor earth, plain | `204` |
| floor earth, alt | `205` |
| floor earth, top | `206` |
| floor earth, left | `207` |
| floor earth, corner | `208` |
| floor sand, plain | `209` |
| floor sand, top | `20A` |
| floor sand, left | `20B` |
| floor sand, corner | `20C` |
| floor court, plain | `20D` |
| floor court, top | `20E` |
| floor court, left | `20F` |
| floor court, corner | `210` |
| wall stone, row 0 | `211` |
| wall stone, row 1 | `212` |
| wall lakon, row 0 | `213` |
| wall lakon, row 1 | `214` |
| void (outside the room) | `215` |
| rug red, top-left | `216` |
| rug red, top | `217` |
| rug red, top-right | `218` |
| rug red, left | `219` |
| rug red, middle | `21A` |
| rug red, right | `21B` |
| rug red, bottom-left | `21C` |
| rug red, bottom | `21D` |
| rug red, bottom-right | `21E` |

| Stamp | Cells | Palette | From | Metatiles (where) | What it is |
|---|---|---|---|---|---|
| `stool` | 1x1 | wood | oikia | 243 (Lakonia_Agoge) | diphros: a folding stool with crossed legs and a fleece seat |
| `amphora_plain` | 1x2 | clay | oikia | 22E / 232 (Lakonia_Agora) | a plain oil amphora |
| `pithos` | 1x2 | clay | oikia | 221 / 224 (Lakonia_Asclepeion) | pithos: a big storage jar with rope-pattern bands and a stone lid |
| `myrtle` | 1x2 | nature | oikia | 262 / 264 (Lakonia_Orthia) | potted myrtle, Aphrodite's shrub, in flower |
| `column` | 1x3 | bronze | oikia | 24C / 24E / 250 (Lakonia_Palaestra) | a Doric post of whitewashed stone, holding up the beam |
| `mat` | 2x1 | nature | oikia | 22A 22B (Lakonia_Asclepeion) | woven reed mat at the door; both cells are south-arrow warps |
| `bench` | 2x1 | wood | ergasteria | 228 229 (Lakonia_Asclepeion) | a long wooden bench |
| `sack` | 1x1 | nature | limen | 233 (Lakonia_Agora) | a sack of grain tied at the neck |
| `louterion` | 1x2 | bronze | limen | 24D / 24F (Lakonia_Palaestra) | a marble washbasin on its pillar by the door, a bronze jug beside it |
| `reed_mat` | 1x1 | nature | lakonia_rooms | 244 (Lakonia_Agoge) | a sleeping mat of reeds cut barehanded from the Eurotas. No knives |
| `spear_rack` | 2x2 | wood | lakonia_rooms | 246 247 / 248 249 (Lakonia_Agoge) | a rack of wooden practice spears, blunted |
| `cloak_pegs` | 2x2 | wood | lakonia_rooms | 23B 23C / 23F 240 (Lakonia_Agoge) | red cloaks on pegs. One cloak a year; you make it last |
| `names_list` | 2x2 | wall | lakonia_rooms | 23D 23E / 241 242 (Lakonia_Agoge) | the herd's names painted on the plaster; some are struck through |
| `oil_hooks` | 2x1 | bronze | lakonia_rooms | 24B 24B (Lakonia_Palaestra) | oil flasks and bronze scrapers on hooks |
| `crowns` | 3x1 | nature | lakonia_rooms | 24A 24A 24A (Lakonia_Palaestra) | six olive crowns, dried brown, nailed above the door. Olympia, six times |
| `cloak_bench` | 2x1 | wood | lakonia_rooms | 251 252 (Lakonia_Palaestra) | a bench of folded cloaks |
| `willow` | 2x3 | nature | lakonia_rooms | 253 254 / 256 257 / 259 25A (Lakonia_Orthia) | a willow. The goddess's image was found in a willow thicket, bound upright |
| `altar_M` | 1x1 | clay | lakonia_rooms | 25E (Lakonia_Orthia) | the long stone altar of Artemis Orthia |
| `xoanon` | 1x2 | wood | lakonia_rooms | 255 / 258 (Lakonia_Orthia) | Orthia: the goddess's wooden image, small and heavy, bound upright in willow withies |
| `stone_counter_L` | 1x1 | wood | lakonia_rooms | 225 (Lakonia_Asclepeion) | Lakonia's counter: a plank on two stones, a bowl of cold water on it |
| `stone_counter_M` | 1x1 | wood | lakonia_rooms | 226 (Lakonia_Asclepeion) | Lakonia's counter: a plank on two stones, a bowl of cold water on it |
| `stone_counter_R` | 1x1 | wood | lakonia_rooms | 227 (Lakonia_Asclepeion) | Lakonia's counter: a plank on two stones, a bowl of cold water on it |
| `basin_stone` | 2x2 | bronze | lakonia_rooms | 21F 220 / 222 223 (Lakonia_Asclepeion) | a stone basin of cold spring water. Nothing else |
| `iron_bars` | 2x1 | clay | lakonia_rooms | 237 238 (Lakonia_Agora) | iron bars stacked like firewood. You can't hide one up your sleeve |
| `great_scales` | 2x2 | bronze | lakonia_rooms | 22C 22D / 22F 230 (Lakonia_Agora) | a great set of scales: everything in Lakonia is weighed |
| `stall_L` | 1x1 | wood | lakonia_rooms | 234 (Lakonia_Agora) | a plank stall counter |
| `stall_M` | 1x1 | wood | lakonia_rooms | 235 (Lakonia_Agora) | a plank stall counter |
| `stall_R` | 1x1 | wood | lakonia_rooms | 236 (Lakonia_Agora) | a plank stall counter |
| `altar_cheese_L` | 1x1 | clay | lakonia_rooms | 25D (Lakonia_Orthia) | the long altar with a round cheese on it |
| `altar_cheese_M` | 1x1 | clay | lakonia_rooms | 25F (Lakonia_Orthia) | the long altar with a round cheese on it |
| `altar_cheese_R` | 1x1 | clay | lakonia_rooms | 260 (Lakonia_Orthia) | the long altar with a round cheese on it |
| `wall_worn` | 1x1 | wall | lakonia_rooms | 231 (Lakonia_Agora) | plaster fallen off the brick |
| `reeds` | 1x1 | nature | lakonia_rooms | 25C (Lakonia_Orthia) | marsh reeds growing up through the court's flags |
| `reed_mat_b` | 1x1 | nature | lakonia_rooms | 245 (Lakonia_Agoge) | a sleeping mat of reeds |

<!-- civic_lakonia_build: end generated -->
