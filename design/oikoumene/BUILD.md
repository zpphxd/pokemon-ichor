# The Oikoumene: build plan

- **Owner:** the world-oikoumene session (branch `claude/world-oikoumene-950021`), build lead for the post-game's second chart. The creative director merges this branch into main after each batch; this session never merges into main itself.
- **What this is:** the working plan for building `design/OIKOUMENE.md` and `design/oikoumene/PERIODOS.md` as playable content at 1.0's core scope (decisions PG-1 to PG-41, all settled 2026-11-14). OIKOUMENE says what the world is; this file says who builds which file, with which ids, in which batch.
- **Read first,** in this order: `CLAUDE.md`, `design/MAP_DESIGN.md`, this file, your land's section of `OIKOUMENE.md` §4 (and `PERIODOS.md` §4 for a hall), `design/oikoumene/COVERAGE.md` (your land's areas), `design/BALANCE.md`, `design/TERMS.md`, `design/research/LAZARUS.md`, then the slice's or world-act1's model for your kind of work (below).

---

## 1. Scope: 1.0's core (PG-4)

All ten lands at core size, the ten halls, Herakles, the Nurseries, every species placed, and the chart. About 45 outdoor maps of OIKOUMENE's own, their towns' interiors, and the halls' 23 maps. Every house is enterable with someone in it and something that happens (MAP_DESIGN §2); every interior is a unique layout.

**Core maps per land.** "Folds in" means that area's COVERAGE species go into the named map's tables (OIKOUMENE §13: "all 79 encounter areas folded into those maps"). Stretch maps keep their section names, so they can be built later without renumbering.

| Land | Towns (core) | Routes, lanes and places (core) | Dungeons | Hall (PERIODOS) | Folds in | Stretch |
|---|---|---|---|---|---|---|
| **Troad** | Sestos (port), Ilion (city) | the Hellespont (lane), the Skamander Plain, the Ida Road (+ the Lambing Meadows nursery) | Gargaros Peak (2 floors + summit), the Walls of Laomedon (2) | the Skaian Gate (4) | T5 Hebros Shore → the Hellespont's north shore; T7 the Smintheion → the Skamander Plain's south corner | Chryse, the Hebros Shore |
| **Egypt** | Naukratis (port, the Oikoumene's hub), Memphis (city), Heliopolis and Elephantine (small) | the Delta Reeds (+ the Papyrus Shallows nursery), Pharos, the Pyramid Field, the Nile (lane) | the Great Pyramid (3 + flooded floor) | the precinct of Proteus (3) | Y5 Moeris → the Pyramid Field's oasis; Y6 Valley of Tombs → the Pyramid Field at night; Y8 → the Great Pyramid's lowest floors | Hekatompylos, Lake Moeris, the Valley of Tombs, Abydos, the Labyrinth of Moeris |
| **Black Sea** | Salmydessos (village), Aia (city); two households at LABORS's Themiskyra | the Bosporus (lane), the Pontic Coast (lane, with the Isle of Ares), the Phasis, the Field of Ares, Leuke (+ the Nesting Cliffs nursery) | the Grove of Ares (3), the Caucasus caves (3) | Aietes's palace (2) | E8 Chalybes' forges → the Phasis's iron reach | Chalybia, the Clashing Rocks' side channel |
| **Lydia** | Sardis (city), Miletos (port town), Gordion (small) | the Royal Road, the Pactolus Sands, Mount Tmolus, the Maeander (+ the Reed Beds nursery), Mount Latmos | the Chasm of Gyges (3) | the treasury (2) | L5 Sipylos → Tmolus's cliffs; L8 → the Chasm's flooded floor | Hypaipa, Mount Sipylos, Tantalus's palace |
| **Libya** | Ammonion (oasis), Kyrene (town) | the Great Sand Sea (maze), the Silphium Plateau, the Salt Ridge (with Antaeus's Ring), Tritonis (lake, + the Syrtis shore) | the Glass Crater (3), the Garamantes' Tunnels (2) | the hippodrome (2) | B4 Syrtis → Tritonis's shore; B8 → the Salt Ridge's ring | the Syrtis Shallows as its own map |
| **North** | Olbia (port), Abaris (village) | the Steppe Road (+ the Wagon Camp at one site, + the Calving Grounds nursery), the Feather Wastes, the Arimaspian Heights, the Rhipaean Pass, the Hyperborean Meadow | the Cave of Boreas (4) | the round temple (2) | S2 Maeotis → the Steppe Road's lake | the Wagon Camp moving, Lake Maeotis |
| **Aithiopia** | Meroë (city, + the Wading Pools nursery), the Gate of Dawn | the Cataracts (lane), the Table of the Sun, Mount Nysa, the Mountains of the Moon | — | the bath-court (2) | A3 Fountain → Meroë's spring; A6 Pygmy Marshes → the Mountains' marsh edge | the Pygmy Marshes as its own map |
| **Far West** | Gadeira (port, + the Tide Pools nursery), Tartessos | the Atlantic Shore, the Atlas foothills | the Atlas Range (4 + summit), the Silver Mines (2) | the royal gallery (2) | — | the Atarantes |
| **Western Sea** | Kroton (port), Cumae | the Phlegraean Fields, Ogygia (+ the Seal Caves nursery), Lake Avernus | — | the palaestra (2) | — | Elea |
| **Okeanos** | the Cimmerian Shore, the Isles of the Blessed (town + 2 isles) | Okeanos (lane, round the rim), the Land of Dreams, the Gates of the Sun, the Selvage | the Cave of Sleep (2), the Gorgons' Isle, the Cave of the Graiai | the tower of Kronos (2) | — | the Springs of Okeanos, the other two isles |

The epics' maps on this chart (LABORS's Thrace, Themiskyra, the Caucasus Crag and the far west; ODYSSEY's sea and islands) are **world-postgame's** to build. This session owns the chart, every section, and the connections between their maps and ours (§3).

---

## 2. Batches

Each batch runs as parallel worktree agents. This session merges them into its branch, keeps `make`, `tools/ichor/smoke_test.sh < /dev/null` and `tools/ichor/tests/slice_playthrough.sh < /dev/null` green after every merge, pushes the branch, and reports the batch with a render of every finished map to the director.

| # | Batch | Agents | Status |
|---|---|---|---|
| 0 | **Setup:** this file, the sections named (§3), the halls' 30 flags, id and flag sub-ranges (§4), batch 1's maps registered | this session | done |
| 1 | **The chart and the near ports.** The region map, Troad / Egypt / Black Sea towns and arrival lanes, their interiors, batch 1's trainer classes and sprites, batch 1's music | 9 (§5) | in progress |
| 2 | **The near lands' routes, dungeons and halls.** Troad II (Skamander, Ida, Gargaros, the Walls), the Skaian Gate; Egypt II (the Pyramid Field, the Great Pyramid, the Nile, Heliopolis, Elephantine), the precinct of Proteus and Helen; Black Sea II (the Phasis, the Field of Ares, Leuke, the Grove, the Caucasus caves), Aietes's palace and the Fleece; Themiskyra's two households; the near lands' legends; the Nurseries' first three | ~8 | |
| 3 | **Lydia and Libya** (63–72): each land's tileset, towns, routes, interiors and dungeons; the treasury and the hippodrome (the chariot); their legends, classes and music | ~8 | |
| 4 | **Aithiopia, the North, the Far West** (70–82): the same, with the round temple, the bath-court and the royal gallery; the cataracts, the Rhipaean ice and the far west's links to LABORS's maps | ~9 | |
| 5 | **The Western Sea and Okeanos** (74–85): Kroton, Cumae, Ogygia, the rim, the Isles, the palaestra and the tower of Kronos; Helios's cup round the rim; Aeolus's Bag on the rim fog; **Herakles at the Pillars** | ~8 | |
| 6 | **Finish:** every species placed (a coverage audit against `coverage.py`), the remaining legends, champion rematches and the War Horn upgrade, the trainer card's Oikoumene page, a full Oikoumene playthrough test, ROM review | ~5 | |

**Order inside a land.** A land's outdoor agent owns its tileset for the batch it draws it in; the interiors agent owns that land's interior set; a hall agent owns its hall's pieces (§6). Two agents never edit the same tileset in the same batch.

---

## 3. The chart: sections and connections

**Engine plan (PG-11).** The Oikoumene takes Kanto's chart slot: `REGION_OIKOUMENE` is `REGION_KANTO`, and `GetRegionForSectionId` reads two ranges as the Oikoumene, the Hoenn block (0–85) and part of the Kanto block's spare tail. The second range is new: OIKOUMENE §11 counted "about 75" sections, but distinct places, with the epics' maps on this chart, come to 107. PG-11 kept the Kanto tail "spare for either chart", and this uses 41 of its 53.

**Names.** `tools/ichor/oikoumene_sections.py` names every section (run it again after editing its tables; it's idempotent). The chart agent sets their positions and art. Interiors, dungeon floors and halls share their parent's section.

| Block | Ids | Sections |
|---|---|---|
| Hoenn, usable | 0–85, skipping 2, 8, 50–54, 57–59, 65, 66, 68, 69, 71, 79, 84, 85 (upstream code still treats those specially; the chart agent's audit may clear some) | `AETHOS` (the crossing target), then the Troad, Egypt, the Black Sea, Lydia, Libya and the North: 67 names |
| Kanto tail | after `MAPSEC_RHODOS` | `THE_OIKOUMENE` (on the **Aethos** chart, so outside both ranges), then Aithiopia, the Far West, the Western Sea and Okeanos: 40 names, `MAPSEC_OIKOUMENE2_FIRST` to `_LAST` |

`python3 tools/ichor/oikoumene_sections.py --list` prints them. The epics' sections, for world-postgame: `ABDERA`, `BISTONIAN_PLAIN`, `THEMISKYRA`, `THERMODON_ROAD`, `CAUCASUS` (shared: their crag, our caves), `PILLARS` (shared: their strait, our waters), `OCEAN_STREAM`, `ERYTHEIA`, `HESPERIDES`, `ATLAS_RIDGE`, `WINE_DARK_SEA` (both halves), `OUTER_SEA` (with Proteus's islet), `LOTUS_ISLE`, `CYCLOPS_ISLE`, `AIOLIA`, `AIAIA`, `SIRENS_ROCKS`, `SCYLLA_STRAIT`, `THRINAKIA`. Their Aethos-chart maps (the Western Cape, Maleia's waters, Scheria at Kerkyra, the Mist Beach) keep Aethos sections.

**How you get there** (OIKOUMENE §2). The *Euploia* is world-postgame's sailing layer (ODYSSEY §2, §14: the surf state with the ship sprite, the wind). Our sea lanes are ordinary sea maps that work with plain surfing until it lands.

| Lane | Seams | Status |
|---|---|---|
| The Hellespont | west edge ← Aethos's Route 20, the north Aegean (world-act2's); east end → Sestos's harbor; north shore has a landing for LABORS's Abdera (Labor 8) | to agree with world-act2 and world-postgame |
| The Bosporus, then the Pontic Coast | the Hellespont's east → the Bosporus (Salmydessos on its west shore) → the Pontic Coast, with landings at Themiskyra (LABORS's), Aia and Leuke | to agree with world-postgame |
| Pharos's waters | Aethos's Route 34, Kaldera's southeast sea (world-act3's) → Pharos → Naukratis's harbor | to agree with world-act3 |
| The Nile | Naukratis → Memphis → Heliopolis → Elephantine → the Cataracts (Horn of Achelous) | ours |
| The far west | LABORS's Strait of the Pillars ↔ Gadeira (sea), the Atlantic Shore; LABORS's Atlas's Ridge ↔ the Atlas foothills | to agree with world-postgame |
| The Western Sea's towns | quay warps from ODYSSEY's sea maps to Kroton, Cumae and Ogygia (after the voyage) | to agree with world-postgame |

Until the Aethos routes exist, our lanes' Aethos-side edges are left open and tested by warp. Seam strips use the primary tileset only (MAP_DESIGN §5); every land's maps share that land's secondary and are exempt inside the land.

**The crossing targets** (OIKOUMENE §2). On the Oikoumene chart, `MAPSEC_AETHOS` at the center flies you to Akti; on the Aethos chart, `MAPSEC_THE_OIKOUMENE` in the edge fog flies you to your last Oikoumene port. Both show once `FLAG_ICHOR_OIKOUMENE_ARRIVED` is set.

**Gating.** Nothing in the Oikoumene is reachable before the post-game: the lanes' Aethos ends are post-game routes, and the crossing target needs `FLAG_ICHOR_OIKOUMENE_ARRIVED`. Scripts that only make sense after the League check `FLAG_SYS_GAME_CLEAR`. Tests reach our maps by warp or save state.

---

## 4. Ids, flags and vars

**Trainer ids** (`tools/ichor/claim_ranges.md`: 680–819 and 864–1023). Define each in `include/constants/opponents.h` inside the Oikoumene block and keep `TRAINERS_END_OIKOUMENE` at the highest id + 1; parties go under `/* Ichor: the Oikoumene */` in `src/data/trainers.party`.

| Who | Ids |
|---|---|
| Troad routes, towns and heroes | 680–699 |
| Egypt | 700–719 |
| Black Sea | 720–739 |
| Lydia | 740–753 |
| Libya | 754–767 |
| North | 768–781 |
| Aithiopia | 782–793 |
| Far West | 794–805 |
| Western Sea | 806–812 |
| Okeanos | 813–819 |
| Halls: 4 trainers, the champion, the champion's rematch, in PERIODOS's order | Troad 864–869, Lydia 870–875, Black Sea 876–881, North 882–887, Egypt 888–894 (+ Helen), Aithiopia 895–900, Libya 901–906, Far West 907–912, Western Sea 913–918, Okeanos 919–924 |
| Herakles and his rematch | 925–926 |
| Spare, for any land that runs over | 927–1023 |

**Bank flags** (0x3C0–0x47F, 192). The halls' 30 and two shared flags are claimed (0x3C0–0x3DF):
- `FLAG_ICHOR_EMBLEM_GATE` … `_ROSE` (0x3C0–0x3C9, contiguous, in PERIODOS §1's order; `Ichor_CountFlags(FLAG_ICHOR_EMBLEM_GATE, 10)` counts them);
- `FLAG_ICHOR_PRIZE_*` (0x3CA–0x3D3) and `FLAG_ICHOR_SHORTCUT_*` (0x3D4–0x3DD), in the same order;
- `FLAG_ICHOR_OIKOUMENE_ARRIVED` and `FLAG_ICHOR_SUPER_ROD_GIVEN`.

| Who (batch 1) | bankflag offsets | vanilla, for hidden items |
|---|---|---|
| chart agent | 0x3E0–0x3E3 | — |
| Troad towns | 0x3E4–0x3F3 | 0x4C0–0x4C7 |
| Troad interiors | 0x3F4–0x403 | — |
| Egypt towns | 0x404–0x413 | 0x4C8–0x4CF |
| Egypt interiors | 0x414–0x423 | — |
| Black Sea towns | 0x424–0x433 | 0x4D0–0x4D7 |
| Black Sea interiors | 0x434–0x443 | — |
| unassigned | 0x444–0x47F (60) | 0x4D8–0x4FF |

**The range is short.** Each land at core wants about 28 flags (a reward per household, item balls, quest steps, hide flags), so about 280 for ten lands plus the halls' 30, against 192. This session has asked the director for a second bank range; until then, agents spend only their sub-range, reuse a quest's own flag as its NPC's hide flag, and put hidden items on the vanilla flags above. Claim with `python3 tools/ichor/claim.py --range LO-HI bankflag FLAG_ICHOR_<NAME> "comment"`.

**Bank vars** 24–27: unassigned. Puzzle state lives in `VAR_TEMP_*` for the length of a map (PERIODOS §7).

---

## 5. Batch 1: the chart and the near ports

All batch-1 maps are registered (`tools/ichor/new_map.py`, by `tools/ichor/oikoumene_register.py`) with placeholder layouts copied from Akti's; each owner rewrites its layout's size, tilesets and blockdata in `data/layouts/layouts.json` and `data/layouts/<Map>/`, and its `map.json` and `scripts.pory`. Agents don't run `new_map.py`: ask this session for a new map.

| Agent | Builds | Tilesets (new) | Files it owns |
|---|---|---|---|
| **chart** | `REGION_OIKOUMENE` and the two ranges; the chart art and grid (`tools/ichor/art/ui_oikoumene_map.py`, from `ui_world_map.py`'s method); every section's position; fly targets for batch 1's towns; the two crossing targets and their heal locations; the hidden-section audit (claim_ranges.md's list); map-name popup frames for the three near lands; the Oikoumene's trainer-battle music branch (`src/pokemon.c`); the Nurseries' monthly-table hook (OIKOUMENE §8, generalising the Altering Cave offset) | the chart's own art | `include/regions.h`, `src/regions.c`, `src/region_map.c`, the region-map art and layout headers, `region_map_sections.json` positions, `map_name_popup.c`, `src/wild_encounter.c`'s Nursery hook, `tools/ichor/art/ui_oikoumene_map.py`, `tools/ichor/tests/oikoumene_chart.*` |
| **troad-towns** | Sestos (port), the Hellespont (lane), Ilion (city): layouts, doors, people outdoors, items, signs, the herm, encounter tables T1 and T5 (the Hellespont), Alethea's quay scene at whichever first port you reach (`FLAG_ICHOR_OIKOUMENE_ARRIVED`) | `troas` | `tools/ichor/art/troas_*.py`, `data/tilesets/secondary/troas/`, `tools/ichor/maps/sestos.py`, `hellespont.py`, `ilion.py`, those maps' layouts and events |
| **troad-rooms** | Sestos's and Ilion's interiors (below) | `megaron` (Trojan interiors) | `tools/ichor/art/megaron_*.py`, its tileset, `tools/ichor/maps/troad_rooms.py`, those rooms |
| **egypt-towns** | Naukratis (port, hub), Pharos (island beach and its waters), the Delta Reeds (route, with the Papyrus Shallows nursery), Memphis (city): Y1, Y2's delta reach and Y7 | `kemet` | `tools/ichor/art/kemet_*.py`, its tileset, `tools/ichor/maps/naukratis.py`, `pharos.py`, `delta_reeds.py`, `memphis.py` |
| **egypt-rooms** | Naukratis's and Memphis's interiors, including the egg-ovens day care and Daphne's fossil revival | `per` (Egyptian mud-brick interiors) | `tools/ichor/art/per_*.py`, its tileset, `tools/ichor/maps/egypt_rooms.py`, those rooms |
| **pontos-towns** | the Bosporus (lane, with the Clashing Rocks standing open), Salmydessos (village), the Pontic Coast (lane, with the Isle of Ares), Aia (city): E1, E2 and E9's sea share | `pontos` | `tools/ichor/art/pontos_*.py`, its tileset, `tools/ichor/maps/bosporus.py`, `salmydessos.py`, `pontic_coast.py`, `aia.py` |
| **pontos-rooms** | Salmydessos's and Aia's interiors | `chalkeon` (Colchian bronze interiors) | `tools/ichor/art/chalkeon_*.py`, its tileset, `tools/ichor/maps/pontos_rooms.py`, those rooms |
| **sprites** | batch 1's trainer classes (§6 of OIKOUMENE: Trojan Hoplite, Charioteer, Shepherd of Ida, Argonaut, Colchian Sorceress, Chalybes Smith, Priest of the Sun, Scribe of Thoth, Embalmer, Nile Boatman, Phoenician Trader; titles PRINCE, PHARAOH, PRIESTESS, QUEEN, KING) with trainer pics; trainer pics for Hektor, Proteus, Medea, Helen; overworld sprites for batch 1's named people (Hero, Priam, Cassandra, Hektor, Phineus, Aietes, Medea, Proteus, Helen, the champions' guards) and the land families' townsfolk | — | `graphics/trainers/`, `graphics/object_events/pics/`, their tables, `include/constants/trainers.h` classes, `src/data/trainer_classes.h` (or wherever classes live), `tools/ichor/art/sprites_oikoumene*.py`, `design/oikoumene/SPRITES.md` |
| **music** | *The Wider World*, *The Plain of Troy*, *The Black Land*, *The Necropolis*, *The Black Sea*, *Battle! Oikoumene Trainer*, *Battle! Champion of the Periodos*, and *The Periodos* in its Troad, Egypt and Black Sea arrangements (`MUSIC.md`, PERIODOS §6) | — | `tools/ichor/music/songs_oikoumene.py`, the new song entries, `design/oikoumene/MUSIC_cues.md` |

**Batch 1's interiors** (OIKOUMENE §4's households). Every room is a unique layout; public buildings share their counter but not their plan.

| Town | Rooms |
|---|---|
| Sestos | Asclepeion (harbor, sea window), Agora, Hero's tower (the windy stair: a carried flame before dusk, Fire Stone; the Kubfu strait-lighting hook), the ferry house (Cramorant for your Pelipper), the net-loft (Super Rod or a Big Pearl) |
| Ilion | Asclepeion, Agora, Priam's palace (Soothe Bell after the Gate Emblem), Cassandra's room (three wrong predictions, three Pythian Laurels), the pilgrims' guest-room (Odysseus, the Xenion, his battle Lv 76–78), the horse-breeder's stable (Mudsdale for Rapidash), the mason's house (the lost chisel, Hard Stone), the peplos-weaver's (berries for a Silk Scarf), the temple of Athena (the Palladion; Deoxys's hook) |
| Naukratis | Asclepeion, Agora, Daphne's field station (fossils, the Oikoumene Dex rating), the egg-ovens (day care), the incense merchant (nine incenses, myrrh), the potter's house (Smeargle for Kecleon), the net-loft |
| Memphis | Asclepeion, Agora, the Apis keepers' (the true Apis, a Tauros), the scribe of Thoth (Unown riddles, Twisted Spoon), the embalmer's (linen, Reaper Cloth) |
| Salmydessos | Phineus's house (the dove), the bird-catcher's (Pidgeot for Unfezant) |
| Aia | Asclepeion, Agora, Phrixos's sons' house (Heat Rock), the linen-weaver's (Liepard for Persian), the palace workshop (Rotom's five forms). Aietes's audience hall and Medea's chamber are the palace hall's (batch 2) |

The precinct of Proteus, the Skaian Gate and Aietes's palace are batch 2's halls; batch 1 leaves their doors in place, locked with a line from a guard (`FLAG_ICHOR_*` none needed: the batch-2 build replaces the script).

**Door warps, fixed so the town and room agents agree without talking.** In each town, warp ids 0, 1, 2… are the doors of the rooms in the table above, in that order (Sestos: 0 Asclepeion, 1 Agora, 2 Hero's tower, 3 ferry house, 4 net-loft). The town's door warp sends to the room's warp 0, its door mat; the room's warp 0 sends back to the town's warp with the room's number. Extra warps in a town (a second door cell, a hall door, a landing, a cave) take ids after the rooms. A room with a second exit (Hero's tower's top) gives it warp 1 onwards.

**Seams between batch 1's agents.**
- **The Hellespont ↔ the Bosporus** (troad-towns and pontos-towns): the Hellespont's east edge meets the Bosporus's west edge, `right`/`left`, offset 0. On that edge, rows 8–21 are open sea on both maps and every other row is shore or cliff; both maps are at least 30 tall. The 8 columns nearest the seam use aethos metatiles only on both sides.
- **Inside one land** each agent chooses its own seams (one tileset, so exempt), and records every connection and its open rows or columns in `MAPS_<land>.md`.
- **To later batches and other sessions** (leave the edge open, aethos-only, and record it): the Hellespont's west edge (Route 20, world-act2), its south shore (the Skamander Plain, batch 2), Ilion's gates (the Skamander Plain and the Ida Road, batch 2); Pharos's north edge (Route 34, world-act3), Memphis's south edge (the Nile and the Pyramid Field, batch 2); the Pontic Coast's landings for Themiskyra (world-postgame) and Leuke (batch 2), and Aia's east gate (the Phasis, batch 2).

**Shared port scripts** (`data/scripts/ichor_oikoumene.pory`, this session's): `Oik_EventScript_AletheaQuay` (the first port you reach plays it, after placing Alethea; it sets `FLAG_ICHOR_OIKOUMENE_ARRIVED`), `Oik_EventScript_FisherGift` (the Super Rod at the first port's net-loft, a Big Pearl elsewhere; the caller keeps its own "given" flag) and `Oik_EventScript_SailHome` (`ICHOR_STUB_SHIP`). Sestos and Naukratis are first ports; Salmydessos and Aia are not (Themiskyra is the Black Sea's).

---

## 6. Conventions for every agent

- **Model your work on what's built.** The slice (`tools/ichor/maps/akti.py`, `elaia.py`, `route1.py`, `akti_homes.py`) and world-act1's branch (`claude/world-act1-6d11b7`: `tools/ichor/maps/emporion.py`, `eleusa.py`, `aegina_homes.py`, the `*_build.py` tileset scripts and `design/phase2/BUILD.md`) show how a tileset is drawn, compiled and mapped by code, and how a map's builder enforces seams, forced grass and sight lines.
- **Tilesets.** 4bpp, 16-colour palettes, colour 0 transparent; plan the 6 primary (aethos's, unchanged) and 7 secondary palettes first. At most 504 tiles in a secondary, and leave 496–511 free where a map uses wide doors. OIKOUMENE §7 sets each land's look; ART_PLAN §6 the method.
- **Plenty of wild encounters** (the user, 2026-11-14). Routes and lanes should feel alive, never thin:
  - **Rates above the slice's vanilla ones:** land 25 on routes (30 on long routes and in deep grass), surfing 10 on sea lanes, rivers and lakes (vanilla's 4 is too sparse for big lanes), fishing 30, rock smash 20, cave floors 15–20. Towns with water get surfing and fishing too.
  - **Lots of grass:** besides the forced bands, about a third of a route's walkable ground is grass, in shaped patches with reasons to go in (MAP_DESIGN §1). Sea lanes are water edge to edge, so every surfed tile can roll an encounter.
  - **Full tables:** fill all 12 land slots, all 5 surf slots and all 10 rod slots (Old, Good and Super), with day and night land sets on every route, Augur's Eye hidden slots, and rock smash wherever there are breakable rocks.
  - **Variety:** at least 8 distinct species per land table per time of day. Where an area's COVERAGE homes are fewer, fill the rest from its listed shares, then from same-land, same-type species, so no table repeats one species across most of its slots.
- **Wild tables.** From COVERAGE's areas, at their levels; the "no early evolved forms" and "evolved forms in late areas" rulings hold (BALANCE). Day and night sets where COVERAGE lists them (`OW_TIME_OF_DAY_ENCOUNTERS`); Augur's Eye slots as hidden mons. Lazarus's nine starter lines appear only wild (PG-5). Encounter entries go in `src/data/wild_encounters.json`, each map's block kept together.
- **Trainers.** Route trainers at the land's band (OIKOUMENE §9), from the land's classes; first trainer easy and in plain view; mandatory sight lines cut the only path (the builder proves it). Parties use National Dex species and legal moves at their levels.
- **Text.** Short lines that fit the Gen 3 box: measure every line with `tools/ichor/text_width.py`; speakers via `setspeaker`. People sound like people; myth is woven in, never lectured. TERMS's words (Asclepeion, Agora, Pithos, Emblem, Xenion).
- **Stubs**, each tagged in a comment so `grep -rn ICHOR_STUB_` finds it: `ICHOR_STUB_SHIP` (the *Euploia* at the quay until world-postgame's sailing lands: a Nausikles who offers SAIL HOME and warps to Akti), `ICHOR_STUB_HALL` (a hall door, batch 2), `ICHOR_STUB_SPRITE` (a stand-in graphics id until the sprites agent's lands), `ICHOR_STUB_MUSIC` (a stand-in song id), `ICHOR_STUB_HERM` (a waystone before the engine gives the Oikoumene herm ids), `ICHOR_STUB_LEGEND` (a legend's hook, for its batch), `ICHOR_STUB_AETHOS` (an Aethos-side seam).
- **Herms.** The engine's herm run has 32 ids, mostly Aethos's. This session has asked ichor-engine for an Oikoumene run; until then a waystone is a bg event tagged `ICHOR_STUB_HERM` that says what it is (a herm on Greek ground, Thoth's ibis pillar in Egypt) and sets nothing.
- **Tests.** Each agent adds a headless Lua check for its maps (`tools/ichor/tests/<area>.sh` + `.lua`, on `tools/ichor/mgba_headless.c`), reaching the map by warp: walk every door, read every sign, talk to every household, take every gift once, fight one trainer, prove the seams.
- **Done means** (per map): `make` green, `tools/ichor/smoke_test.sh < /dev/null` passing, the map meets MAP_DESIGN (forced grass on routes, trainer checkpoints, every dead end pays, every house a home, every interior unique, seam strips primary-only, signs at ends and forks), **at least three render-and-critique passes written down** in `design/oikoumene/MAPS_<land>.md`, and a 2x render in `design/oikoumene/img/<map>.png` for the user.
- **Commits.** `type(scope): description`, the why in the body, ending `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` (CLAUDE.md). Commit on your own worktree branch; this session merges.
- **Shared registration files** (`layouts.json`, the tileset tables in `src/data/tilesets/`, `event_objects.h` and the sprite tables, `wild_encounters.json`, `trainers.party`, `opponents.h`, `flags.h`) take small appended entries in your own block; this session resolves merge conflicts in them.
- **If the permission system denies an action,** stop and report it; don't find a way round it.

---

## 7. Engine asks

| Ask | For | To | Status |
|---|---|---|---|
| An Oikoumene herm run (about 30 ids) and their heal locations, so waystones join the Wings' fly map (OIKOUMENE §4) | every land | ichor-engine | asked |
| A second bank-flag range for the Oikoumene, about 256 flags (IchorSave's `reserved` has room) | every land | the director, then ichor-engine | asked |
| The chariot (PERIODOS §4.7; OIKOUMENE §13), Medium: a player state like the *Euploia*'s that always moves, two strides between turns | Kyrene's hall, batch 3 | ichor-engine | asked |
| A creature changing form on a step count (the Black Sea's brew, Egypt's shapes), Low–Medium | batch 2's halls | built on this branch by the hall agents, in ENGINE_API's conventions | — |
| The Song and the Wall: warp to the same tile on a twin map, and back unless it's a wall, Low | the Skaian Gate | built on this branch | — |
| The Nurseries' monthly tables, Low | every Nursery | built on this branch (chart agent) | batch 1 |
| The Oikoumene trainer-battle music, one line | every battle | built on this branch (chart agent) | batch 1 |

---

## 8. Results

Each batch's result goes here when it's merged: what was built, its renders, its tests, ROM after, and what's stubbed.
