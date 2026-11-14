# Phase 3 build plan: Act II

Owner: the world-act2 session (branch `claude/world-act2-0a92e7`). This is the working plan for building `design/phase3/SCRIPT.md` as playable content. SCRIPT.md says what happens; this file says who builds which file, with which ids, and what is stubbed until another session lands.

Read first, in this order: `CLAUDE.md`, `design/MAP_DESIGN.md`, this file, the SCRIPT.md beats and Part 2 rosters for your maps, `design/TERMS.md`, `design/MUSIC.md`, then the model for your kind of work (below). world-act1's `design/phase2/BUILD.md` (on `claude/world-act1-6d11b7`) is the sister plan for Act I; where this file is silent, follow it.

## Batches

| # | Batch | Beats | Status |
|---|---|---|---|
| 1 | **The Kithairon crossing and Thyrsa:** Route 6, Mt. Kithairon (Eleutherai and the pass), Route 7 and the Kronia grounds, Thyrsa City and its interiors, the theater and skene, the Temple of Dionysus | 26–34 | in progress |
| 2 | The road west: Route 8, Lebadeia and Trophonios's cave, Route 9, Kirrha, the Gulf ferry, Aigion | 35–37 | |
| 3 | Arkadia: Route 11, Styx Falls, Route 12, Arkadia and its interiors, the Cypress Wood, the Pool, the Temple of Artemis | 38–44 | |
| 4 | Back to the Isthmus and the road of the Mysteries: Route 13, Nemea, Route 14, the Act II changes to Emporion, Eleusa and Akti, Route 15 with Thria, Daphni, Route 16; Aigina's interior scripted onto world-act1's maps | 45–47 | |
| 5 | Astyra: the city and its interiors, the Kerameikos and the paupers' graves, the Akropolis, Phaleron, the salt well | 48–57 | |
| 6 | The voyage and Kaldera: the *Paralos*, Delos, Route 19, Paros, the caldera road, Kaldera and its interiors, the Temple of Hephaestus, the Telchines' forge, Nea Kameni; the empty house in Elaia | 58–67 | |
| 7 | The optional lands: Euboia; Routes 17–18 with Marathon, Halai and Sounion; the open Aegean | — | |

Each batch ends with a report to the director: the branch and commit, what's playable, the map renders, the test results and the ROM delta.

## Batch 1

### Who builds what

Every agent touches only its own files. Shared registration files (`data/layouts/layouts.json`, `data/maps/map_groups.json`, `src/data/tilesets/*`, `include/constants/event_objects.h` and the sprite tables) take small appended entries; this session resolves conflicts in them.

| Agent | Builds | Files it owns |
|---|---|---|
| **kithairon** | The `kithairon` secondary (one set for all four maps of the crossing, so their shared seams need no aethos-only strip); Route 6, Eleutherai, Mt. Kithairon, Route 7 with the Kronia grounds: layouts, events, `scripts.pory` (beats 26–29 and the rosters) | `tools/ichor/art/kithairon_*.py`, `data/tilesets/secondary/kithairon/`, `tools/ichor/maps/kithairon.py`, the four maps' layouts and `data/maps/<Map>/`, `design/phase3/TILES_kithairon.md` |
| **thyrsa** | The `thyrsa` secondary (the city, its gates, its vineyards and the Kadmeia, and the theater's outer gate in the city wall); Thyrsa City (beat 30 and the roster), with a door warp into the theater | `tools/ichor/art/thyrsa_*.py`, `data/tilesets/secondary/thyrsa/`, `tools/ichor/maps/thyrsa.py`, `MAP_THYRSA_CITY`'s layout and `data/maps/ThyrsaCity/`, `design/phase3/TILES_thyrsa.md` |
| **rooms** | The `thyrsa_rooms` secondary on the `oikos` primary; every Thyrsa and Eleutherai interior except the temple and the theater: the Asclepeion, the Agora, the Kantharos, the xenia host, the seven households, Eleutherai's watch-house and homes | `tools/ichor/art/thyrsa_rooms_*.py`, `data/tilesets/secondary/thyrsa_rooms/`, `tools/ichor/maps/thyrsa_rooms.py`, those maps' layouts and `data/maps/<Map>/`, `design/phase3/ROOMS_thyrsa.md` |
| **temple** | The `temple_dionysus` secondary on the `oikos` primary; the Temple of Dionysus and the Three-Act Play (SCRIPT.md Part 5, beat 31); Thespis | `tools/ichor/art/temple_dionysus*.py`, `data/tilesets/secondary/temple_dionysus/`, `tools/ichor/maps/temple_dionysus.py`, `MAP_THYRSA_CITY_TEMPLE_OF_DIONYSUS`, `design/phase3/TILES_temple_dionysus.md` |
| **scenes** | The `theater` secondary (the cavea and its seated crowd, the orchestra, the skene's front and doors, the god-machine; backstage, the mask racks and the prop room for the skene, on `oikos`); the theater and the skene maps; the Dionysia (beat 32) with the trance effect, Kleon's third battle (beat 33), Silenos's contest (beat 34) | `tools/ichor/art/theater_*.py`, `data/tilesets/secondary/theater/` (and a `skene` secondary if the backstage rooms need their own), `tools/ichor/maps/theater.py`, `MAP_THYRSA_THEATER` and `MAP_THYRSA_THEATER_SKENE` whole, `src/ichor_act2_scene.c` and its header (the trance palette pulse and anything else these scenes need), `data/scripts/ichor_act2.pory` (shared Act II scene scripts), `design/phase3/TILES_theater.md` |
| **sprites** | Trainer portraits and overworld walkers for batch 1's new people and classes | new files under `graphics/trainers/` and `graphics/object_events/pics/`, their tables, `tools/ichor/art/sprites_act2*.py`, `design/phase3/SPRITES.md` |
| **this session** | This file, flag claims, the stub headers, trainer ids and parties, the wild encounter tables, the batch tests, integration | `design/phase3/BUILD.md`, `include/constants/flags.h` claims, `include/constants/ichor_species_stubs_act2.h`, `include/constants/opponents.h` (the world-act2 block), `src/data/trainers.party` (the world-act2 section), `src/data/wild_encounters.json`, `tools/ichor/tests/act2_*` |

**Parties and encounters are staged, then merged by this session**, so no two agents edit the same file: each agent writes its trainers' parties in `design/phase3/parties/<agent>.party` (the `.party` syntax, SCRIPT.md Part 3's blocks with the id names) and its encounter tables in `design/phase3/encounters/<agent>.json` (the `wild_encounters.json` entry for each map). This session folds them in and builds.

### Models

| Kind of work | Model to follow |
|---|---|
| An outdoor secondary tileset | `tools/ichor/art/eleusa_*.py` and `design/phase2/TILES_eleusa.md` (soft ground, borrowed ground, the catalog), and `emporion_*.py` for a city |
| A route or town builder | `tools/ichor/maps/route1.py` (ASCII grids, auto-tiling, review renders), `akti.py` |
| Interiors | `tools/ichor/art/oikia_*.py`, `civic_*.py`, `design/phase1/ROOMS_oikia.md`, `ROOMS_civic.md`; `tools/ichor/maps/akti_homes.py` |
| A temple trial | `tools/ichor/art/temple_demeter_*.py`, `temple_hermes*.py`; the slice's Hearth Trial (`data/maps/AktiTown_TempleOfHestia/scripts.pory`) |
| Sprites | `tools/ichor/art/sprites_*.py`, `design/phase1/SPRITES_classes.md`, `SPRITES_npc.md` |
| A headless test | `tools/ichor/tests/route1.sh`, `temple_trial.sh`, `slice_lib.lua` |

### Maps

This session has registered every batch 1 map with `tools/ichor/new_map.py`, so warps between agents' maps compile from the start. Each has a placeholder layout (a copy of an Act I layout, on stand-in tilesets) and stand-in music. Replace the layout, its tilesets and its size with your builder's output, and set the music when MUSIC.md's cue exists (`ICHOR_STUB_MUSIC` until then). Keep the map names, ids and groups.

| Map (directory) | `MAPSEC` | Tilesets | Type | Size (SCRIPT.md) | Group | Owner |
|---|---|---|---|---|---|---|
| `MAP_ROUTE6_ELEUTHERAI_ROAD` (`Route6_EleutheraiRoad`) | `MAPSEC_AETHOS_ROUTE_6` | aethos + kithairon | route | 56×28 | TownsAndRoutes | kithairon |
| `MAP_ROUTE6_ANTIOPES_CAVE` (`Route6_AntiopesCave`) | `MAPSEC_AETHOS_ROUTE_6` | the agent's choice (a cave set on aethos, or kithairon) | underground | SCRIPT.md's | IndoorKithairon | kithairon |
| `MAP_ELEUTHERAI` (`Eleutherai`) | `MAPSEC_MT_KITHAIRON` | aethos + kithairon | town-like waypoint | 32×26 | TownsAndRoutes | kithairon |
| `MAP_MT_KITHAIRON` (`MtKithairon`) | `MAPSEC_MT_KITHAIRON` | aethos + kithairon | route | 40×56 | TownsAndRoutes | kithairon |
| `MAP_ROUTE7_KRONIA_GROUNDS` (`Route7_KroniaGrounds`) | `MAPSEC_AETHOS_ROUTE_7` | aethos + kithairon | route | 44×40 | TownsAndRoutes | kithairon |
| `MAP_THYRSA_CITY` (`ThyrsaCity`) | `MAPSEC_THYRSA_CITY` | aethos + thyrsa | city | 56×48 | TownsAndRoutes | thyrsa |
| `MAP_THYRSA_THEATER` (`ThyrsaTheater`) | `MAPSEC_THYRSA_CITY` | aethos + theater | outdoor set piece | 40×34 | TownsAndRoutes | scenes |
| `MAP_THYRSA_THEATER_SKENE` (`ThyrsaTheater_Skene`) | `MAPSEC_THYRSA_CITY` | oikos + theater (or skene) | indoor | backstage and the prop room | IndoorThyrsa | scenes |
| `MAP_ELEUTHERAI_WATCH_HOUSE`, `_LYSIDIKE_HOUSE`, `_OINOE_HOUSE` | `MAPSEC_MT_KITHAIRON` | oikos + thyrsa_rooms | indoor | each room's own | IndoorKithairon | rooms |
| `MAP_THYRSA_CITY_ASCLEPEION`, `_AGORA`, `_TAVERN`, `_MASK_WORKSHOP`, `_ACTOR_HOUSE`, `_EUDORA_HOUSE`, `_MANTO_HOUSE`, `_PINDAROS_HOUSE`, `_SOWN_HOUSE`, `_VINTNER_HOUSE` | `MAPSEC_THYRSA_CITY` | oikos + thyrsa_rooms | indoor | each room's own | IndoorThyrsa | rooms |
| `MAP_THYRSA_CITY_TEMPLE_OF_DIONYSUS` (`ThyrsaCity_TempleOfDionysus`) | `MAPSEC_THYRSA_CITY` | oikos + temple_dionysus | indoor | the trial's | IndoorThyrsa | temple |

### Seams and warps

| Seam | Columns or rows | Agreed with |
|---|---|---|
| Eleusa's north edge → Route 6's south edge | `MAP_ELEUSA_VILLAGE` (50×40, aethos + eleusa, world-act1's commit 0284b88d32) is open at y = 0 in columns 44–47: the road is 45–46, grass verges at 44 and 47. Eleusa's six rows nearest the seam are aethos-only and have no vines; the vines are on Route 6, just past the seam. Route 6's road meets its south edge in the kithairon agent's choice of four columns *r*…*r*+3 (verge, road, road, verge), with Route 6's own seam rows aethos-only. Offsets follow from *r*: Eleusa `up` to Route 6 with offset 44 − *r*; Route 6 `down` to Eleusa with offset *r* − 44. This session adds both connections at integration, once Eleusa and Route 6 are on one branch. | world-act1 (columns), kithairon (*r*) |
| Route 6 ↔ Eleutherai ↔ Mt. Kithairon ↔ Route 7 | the kithairon agent's choice, recorded here | — |
| Route 7's north edge → Thyrsa's Elektran Gate | Route 7's road leaves its north edge at columns 20–23; Thyrsa's Elektran Gate opens on its south edge at columns 26–29. The connection is `up` from Route 7 with offset −6 (Thyrsa's `down` with offset +6). Both rows at the seam are aethos-only. The kithairon and thyrsa agents may move it together, and record the change here. | kithairon, thyrsa |
| Thyrsa's west edge (the Neistan Gate) → Route 8 | batch 2. Draw the gate and the road's first columns; record them here | — |
| Eleusa's east edge → Route 15 | batch 4. Eleusa is open at x = 49 in rows 24–27; a wall runs down x = 48 with its gap at (48,25), where a hoplite stands in Act I. This session claimed his hide flag, `FLAG_ICHOR_HIDE_ELEUSA_EAST_HOPLITE` (bank 0x10C), and puts it on his object in batch 4, once Eleusa is on main | world-act1 |
| Thyrsa's east edge (the Proitid Gate) → Euboia | batch 7. Draw the gate shut, with its guard | — |

Record arrival tiles for scripted warps here as you choose them.

**Door warp ids are fixed now**, so the outdoor and interior agents can wire both ends without waiting for each other. On an outdoor map, warp *N* is the door in this table. In every interior, warp 0 (and 1, for a two-tile doorway) is the way out, to the outdoor map's warp *N*. Add any further warps after these.

| Outdoor map | Warp | Leads to (its warp 0) |
|---|---|---|
| `MAP_ROUTE6_ELEUTHERAI_ROAD` | 0 | `MAP_ROUTE6_ANTIOPES_CAVE` |
| `MAP_ELEUTHERAI` | 0, 1, 2 | `MAP_ELEUTHERAI_WATCH_HOUSE`, `_OINOE_HOUSE`, `_LYSIDIKE_HOUSE` |
| `MAP_THYRSA_CITY` | 0, 1, 2, 3 | `MAP_THYRSA_CITY_ASCLEPEION`, `_AGORA`, `_TAVERN`, `_TEMPLE_OF_DIONYSUS` |
| `MAP_THYRSA_CITY` | 4, 5, 6, 7 | `_MASK_WORKSHOP`, `_ACTOR_HOUSE`, `_EUDORA_HOUSE`, `_MANTO_HOUSE` |
| `MAP_THYRSA_CITY` | 8, 9, 10 | `_PINDAROS_HOUSE`, `_SOWN_HOUSE`, `_VINTNER_HOUSE` |
| `MAP_THYRSA_CITY` | 11 | `MAP_THYRSA_THEATER` (the theater's outer gate in the city wall) |
| `MAP_THYRSA_THEATER` | 1 | `MAP_THYRSA_THEATER_SKENE` (the skene's back door) |

The theater's warp 0 is its gate back to the city's warp 11.

### New classes, pics and walkers

**Trainer names** fit `TRAINER_NAME_LENGTH`, 10 characters. Batch 1's three long ones are now Astylos (Route 6's runner, was Thersandros), Mynniskos and Thettalos (the temple's actors, were Kallippides and Nikostratos); SCRIPT.md is updated. Eight later trainers' names are too long too and get renamed in their batches.

The sprites agent makes these, under these names, so everyone else can use them now:

- **Classes** (`Class:` in a party): `Maenad`, `Satyr`, `Actor`, `Vintner`. Until they exist, `tools/ichor/act2/fold_parties.py` folds them in as Harvester, Goatherd, Acolyte and Harvester.
- **Pics** (`Pic:`): `Maenad`, `Satyr`, `Actor`, `Vintner`, `Hierophant Thespis`, `Silenos`. Until they exist, the fold uses Hierophant Ione's pic for Thespis and the Shepherd's for the rest.
- **Walkers and objects** (`graphics_id` in `map.json`, `setobjectgraphics` in scripts): `include/constants/ichor_gfx_stubs_act2.h` names each one and points it at a stand-in walker. Use the names there. When the sprites agent adds a real one to `event_objects.h`, it deletes that name's line from the stub header in the same commit.
- Named townsfolk (Pindaros, Staphylos, Oinoe and the rest) use the existing folk walkers in batch 1. The sprites agent may add palette variants and list them in its report; this session swaps them in.

### Ids

**Trainer ids** (`include/constants/opponents.h`, the world-act2 block, 160–319). This session defines them; agents write parties under these names.

| Ids | Agent | Trainers |
|---|---|---|
| 160–175 | kithairon | Route 6: Ikarios, Pythodoros, Botrys, Astylos. Eleutherai: Timolaos. Kithairon: Lykidas, Euia, Bromia, Arimnestos, grunt Ilys. Route 7: Komos, Hagnon; the Kronia: grunts Argillos, Keramos, Plinthos, Gypsos |
| 176–178 | thyrsa | Thyrsa City: Oinopion, Lenaia, Hegelochos |
| 179–182 | temple | Mynniskos, Thettalos, Theodoros; Thespis |
| 183–187 | scenes | Borboros (the actor); Kleon's three (`_3_KYNDER`, `_3_HIPLING`, `_3_NEBREL`); Silenos |

**Flags.** Claim only inside your sub-range, with `python3 tools/ichor/claim.py --range LO-HI bankflag FLAG_ICHOR_<NAME> "comment"`. Systems whose flags the engine reserves (herms, cleansed altars, prophecy tablets, Daedalus's pages, constellations, digs, rite gifts, theoxenia, xenia, relics) don't come from these ranges: use the engine's names (`design/ENGINE_API.md`) behind the stubs below.

| Agent | bankflag offsets | Count |
|---|---|---|
| this session (story, cross-map) | 0x100–0x10F | 16 |
| kithairon | 0x110–0x12F | 32 |
| thyrsa | 0x130–0x13F | 16 |
| rooms | 0x140–0x14F | 16 |
| temple | 0x150–0x153 | 4 |
| scenes | 0x154–0x15F | 12 |

**Bank vars** (`claim.py --range LO-HI bankvar VAR_ICHOR_<NAME> "comment"`): temple 6–7 (the Three-Act Play's state), scenes 8–9 (the Dionysia and the contest), this session 10–11.

Story flags this session has already claimed, for everyone to use: `FLAG_ICHOR_ACT2_BEGUN`, `_VISITED_ELEUTHERAI`, `_KRONIA_SEEN`, `_ARRIVED_THYRSA`, `_VISITED_THYRSA`, `_THREE_ACT_PLAY_DONE`, `_DIONYSIA_BEGUN`, `_DIONYSIA_DONE`, `_SAW_PROGRAM_HOOK`, `_KLEON_BATTLE_3_DONE` (all `FLAG_ICHOR_…`).

Daily flags (this session claims them): `FLAG_DAILY_ICHOR_KRONIST_BREAD`, `_SKENE_MASK`, `_TREADING`, from 0x4C. **Hidden items** need vanilla flags (0x1F4 or above). Act II's range is vanilla flags 0x300–0x37F, 110 of them free, from the Hoenn cut's batch 2 (commit aae327b35e on `claude/hoenn-cut-db6209`, not yet on main). Until it is on main, list each hidden item in your map's section of this file and don't place it; this session claims the flags (`claim.py --range 300-37F flag …`) and places them once the cut lands. Story state stays in the Ichor bank flags. Vars beyond the bank vars above need the director's OK. The cut removes every Hoenn and FRLG map: never use a Hoenn or FRLG `MAP_`, `LAYOUT_` or `HEAL_LOCATION_` name (warps, heal points, copied layouts), since after the cut they compile only as stubs.

Batch 1 alone wants about 80 bank flags, and Act II about 430 before item balls; the 256 in 0x100–0x1FF won't hold the act. The director has the ask.

### Stubs until other sessions land

Each stub is tagged in a comment, so it can be found with `grep -rn ICHOR_STUB_`. world-act1 uses the same tags for Act I.

- **`ICHOR_STUB_AETHOS_DEX`: species.** The Aethos dex isn't in the ROM. Write the Aethos names everywhere (`SPECIES_THYRSIVY`, `OBJ_EVENT_GFX_SPECIES(BOTRYKIT)`). `include/constants/ichor_species_stubs_act2.h` maps each Act II name to a vanilla stand-in of the same type, every one behind `#ifndef`, so world-act1's header (`ichor_species_stubs.h`, which covers Act I's species and is included first) defines the shared ones. Both headers sit inside `#ifndef ICHOR_AETHOS_DEX`, so the dex lands by defining that one macro. Write no `Ability:` lines in parties while the stand-ins are in place; note the ability in a comment for the dex.
- **`ICHOR_STUB_RELICS`: the Girdle and the obstacles.** The relics are engine batch 2. Use the engine's names: the item `ITEM_GIRDLE_OF_HERAKLES` and the flag `FLAG_ICHOR_GOT_GIRDLE_OF_HERAKLES`, behind `ICHOR_STUB_RELICS`. Until they exist, the Girdle is a story flag of this session's (`FLAG_ICHOR_ACT2_STUB_GIRDLE`, aliased), a column drum is an object whose script checks it and moves the drum by script, and the vines are a thicket object whose script checks `FLAG_ICHOR_GOT_DEMETERS_SICKLE` (world-act1's beat 23 sets it; `flags.h` aliases it to this session's `FLAG_ICHOR_ACT2_STUB_SICKLE` until the engine defines it), with the hide flag `FLAG_ICHOR_HIDE_ELEUTHERAI_VINES`, which the kithairon agent claims. Scripts check `FLAG_ICHOR_GOT_GIRDLE_OF_HERAKLES` the same way.
- **`ICHOR_STUB_RITES`, `ICHOR_STUB_HERM`, `ICHOR_STUB_DIG`.** Engine batches 3–4. An altar shows its SCRIPT.md text and says nothing about prayer mechanics; a desecrated altar's guard battles you and the cleansing line plays; a great herm offers to anoint and sets nothing; a fixed dig spot shows the turned-earth text. Each is its own small script with the tag in a comment, so it can be swapped for `EventScript_IchorAltar_<God>`, `EventScript_IchorGreatHerm` and the dig API when they land.
- **`ICHOR_STUB_OFFERINGS`.** Olive Oil, Wine, Barley Cake and the Bronze Votive are engine items. Until then, an offering given in a scene is skipped with the tag, and an offering item ball uses `ITEM_BERRY_JUICE`.
- **`ICHOR_STUB_MUSIC`.** Act II's new cues (SCRIPT.md Part 9) aren't composed yet. Use the nearest built cue and tag it: `MUS_ICHOR_ROAD` for Route 6, Kithairon and Route 7; `MUS_ICHOR_EMPORION` for Thyrsa; `MUS_ICHOR_TEMPLE_HERMES` for the Temple of Dionysus; the Titan theme for the tragedy; the rival battle for Kleon; the slice's gym battle for Thespis. Never use Elpis's lullaby (627, 628) in batch 1.
- **`ICHOR_STUB_KNUCKLEBONES`.** If the knucklebones script isn't on main when the scenes and rooms agents reach Silenos and the Kantharos, play each match as a scripted win or loss with the SCRIPT.md lines, behind the tag.
- **`ICHOR_STUB_SCENE_HOURS`.** world-act1's `Ichor_SetHoursOverride` isn't on main yet. The Dionysia holds dusk on its own map (the scenes agent draws the sky layer at dusk, SCRIPT.md beat 32), so batch 1 doesn't need it.

### Done means (per map)

- `make` is green and `tools/ichor/smoke_test.sh` passes.
- The map follows MAP_DESIGN.md: forced grass on routes, trainer checkpoints, every dead end pays, every house a home, every interior unique, seam strips from the primary only, signs at ends and forks.
- **At least three render-and-critique passes,** each written down in your TILES or ROOMS doc (what was wrong, what changed), and in-game screenshots of every scene, looked at.
- Every line of text measured with `tools/ichor/text_width.py`; the speaker's name in the name box, as in the slice.
- A 2x render in `design/phase3/img/<map>.png` for the director to forward to the user.

### Tests

This session writes `tools/ichor/tests/act2_batch1.sh` on `slice_lib.lua`: it starts a save with Act I's end flags set (`FLAG_ICHOR_ACT1_COMPLETE`, the three laurels, the Sickle), warps to Route 6's south edge and plays beats 26–34 headlessly: the vines, the Kronia, the trial, the Dionysia, Kleon and the Girdle, ending at Thyrsa's open west gate. The full-playthrough test (world-act1's) is extended through Act II once Act I's maps are on main.
