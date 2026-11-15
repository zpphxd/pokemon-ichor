# Ichor art inventory

The checklist that makes the total conversion true: every player-facing asset group and system in the ROM, with its status. It is the "inventory" that `design/ART_PLAN.md` §6 promises. Nothing should stay Hoenn by accident.

- **Audited against:** the remnants branch, which is `main` at `25526ae5dc` plus that pass's fixes (`design/phase1/UI_remnants.md`), with a clean `make` (devkitARM 16.1, Emerald build). Each row was checked by looking: in game for the screens (the slice playthrough, its side checks and gallery, and a screen harness), and in the repo for the rest.
- **Sizes** were measured at `c82f1634f7` from the linker map, `pokeemerald.map`, and `nm -S` on `pokeemerald.elf`, and have not been re-measured; only the ROM total below is current. Unsized assembly labels are sized by the gap to the next symbol. KiB means 1024 bytes. Sizes are good to a few percent, and the groupings are by symbol name and source file.
- **Update rule:** when a batch merges, flip its rows from **In progress (batch)** to **Greek** and fix the counts in the summary.
- **What a row means.** A row is an asset group or system. When the slice's part of a group is Greek and the rest waits on later maps (the item icons, the songs), the row says so in its notes and its phase.

## Legend

| Status | Meaning |
|---|---|
| **Greek** | Redrawn, rewritten or recomposed for Aethos, and in the repo. |
| **In progress (batch)** | A batch running in parallel owns it. Today that is only the main menu's backdrop (QA P6). |
| **Hoenn** | Still Emerald's. It must be replaced or rewritten. |
| **Cut** | A Hoenn-only system or asset to remove, with no replacement. Systems on ART_PLAN's cut list are marked "per ART_PLAN"; the rest are flagged for the director. |
| **Keep** | Generic, and fine as it is (the battle animations, move SFX and so on). |
| **New** | Nothing exists in the ROM yet and nothing Hoenn is in its place. It has to be built (relics, the Scroll of Deeds, the Aethos cast). This sixth status is not in the brief; it stops "not started" from being counted as "Hoenn". |

**Phase** is the roadmap phase in `design/PITCH.md` §8: **1** is the Kalliste slice, **2** Act I (Emporion, Eleusa), **3** Act II (Thyrsa, Arkadia, Astyra, Kaldera), **4** Act III through the Pantheon (1.0), **5** post-game, and **6** the polish sweep. **Batch** means a running batch owns the row. **Dex** means it waits for `design/dex/`. **Director** means it needs a decision.

## Summary

**226 rows** across 11 areas. Counts by status (a row is an asset group or system, so these are not file counts):

| Status | Rows |
|---|---|
| Greek | 87 |
| In progress (batch) | 1 |
| Hoenn | 42 |
| Cut | 47 |
| Keep | 32 |
| New | 17 |

| Area | Greek | In progress | Hoenn | Cut | Keep | New | Rows |
|---|---|---|---|---|---|---|---|
| 1. Overworld | 13 | 0 | 7 | 4 | 2 | 3 | 29 |
| 2. People | 11 | 0 | 4 | 5 | 0 | 5 | 25 |
| 3. Pokémon | 0 | 0 | 1 | 0 | 5 | 3 | 9 |
| 4. Battles | 5 | 0 | 2 | 2 | 5 | 0 | 14 |
| 5. Screens | 26 | 1 | 5 | 3 | 1 | 3 | 39 |
| 6. Items | 3 | 0 | 4 | 5 | 2 | 3 | 17 |
| 7. Text | 11 | 0 | 7 | 1 | 1 | 0 | 20 |
| 8. Audio | 7 | 0 | 6 | 4 | 3 | 0 | 20 |
| 9. Data | 3 | 0 | 2 | 5 | 2 | 0 | 12 |
| 10. Cuts | 0 | 0 | 1 | 17 | 2 | 0 | 20 |
| 11. Overlooked | 8 | 0 | 3 | 1 | 9 | 0 | 21 |

Two rows are new since the first count: the `agros` and `akti` tilesets, and the follower's balls.

Greek now covers everything the slice shows except the few items below: all 15 slice maps and their tilesets, the cast, townsfolk and classes, the boot sequence, title and speech, every everyday screen (bag, party, summary, Agora, popups, codex, Pithos, naming, options, trainer card, region map, klepsydra, starter table, evolution, berry tag, the Augur's Eye), the battle interface, backgrounds and transitions, the field effects, doors and ground jars, the slice's item icons, 36 songs, and the system text. The 42 Hoenn rows are almost all Hoenn's own maps, people, music and text, which go as Aethos's maps replace them in Phases 2-5.

**ROM now:** 25,648,568 bytes of the 33,554,432-byte limit (76.44 %, from `make`). That leaves 7,905,864 bytes (7.54 MiB) free.

**ROM the cuts would free** (measured at `c82f1634f7`):
- **ART_PLAN's list, with the Hoenn Frontier engine kept: 2.15 MiB (2,250,486 bytes).** That is contests, the Berry Blender, Pokéblocks, secret bases, Mirage Island, the PokéNav, e-Reader and Mystery Gift, the minigames, the link-only features, the Frontier maps and art, and FRLG data.
- **2.48 MiB (2,599,873 bytes) if the Frontier engine goes too.** The Olympiad needs it, so I recommend keeping it.
- **About 0.58 MiB more** if the director also approves the proposed cuts that are not on ART_PLAN's list (Mauville Old Man, TV, Easy Chat and mail, Safari Zone, transport, Apprentice, gym puzzles).
- **The cuts are small next to the dex.** Pokémon cries (9.4 MB) and species art and data (5.9 MB) were 57 % of the ROM. FRLG maps and tilesets are not built into the Emerald ROM at all, so cutting FRLG frees only 365 KiB.

**What a slice player can still see that is Hoenn**, ranked by how much a player would notice. Existing species art is left out, because the dex team owns it.

| # | What the player sees | Where | Owner | Rows |
|---|---|---|---|---|
| 1 | **The trade scene.** Kimon's Finizen trade in Glykera's bakery plays Emerald's trade art. | `graphics/trade/`, `src/trade.c` | UI | §5 |
| 2 | **The main menu's lavender backdrop** behind NEW GAME and CONTINUE (QA P6). | `src/main_menu.c`, `graphics/interface/main_menu_*.pal` | UI, in progress | §5 |
| 3 | **The codex's AETHOS counts** still count Hoenn's regional dex: SEEN AETHOS 3 for Geodude, Nosepass and Machop (QA m7). | `src/pokedex.c` | Dex team | §3 |
| 4 | **Emerald's item icons on held items.** Wild Pokémon in the slice may hold a Pretty Feather, Everstone, Light Clay, Metal Coat, Moon Stone, Luminous Moss, Dragon Scale or Poison Barb. | `graphics/items/icons/` | Items | §6 |
| 5 | **The berry pictures** on Bag > Berries > CHECK TAG: Emerald's Oran and Sitrus, on the new clay label. | `graphics/berries/` | Items, with the berry decision | §1, §5 |
| 6 | **The summary's RIBBON box** on the skills page, for a system Aethos hasn't decided on. | `src/pokemon_summary_screen.c` | Director | §11 |
| 7 | **Small expansion leftovers on the Augur's Eye:** the "R TO REGISTER!" line and the no-data "X". | `src/dexnav.c`, `graphics/dexnav/no_data.png` | Text, UI | §5 |
| 8 | **The save-failed screen's clock icon**, if a save ever fails. | `graphics/misc/clock_small.png` | UI | §5 |

---

## 1. Overworld

### Route 1 / Akti native redraw coverage

The second town-scoped polish pass covers **KallisteRoute1,
KallisteRoute1_KronionHill, AktiTown**, and all six implemented Akti interiors:
**TempleOfHestia, Asclepeion, Agora, FishersHouse, DiversHouse and
GoatherdsHouse**. The older **Greek** labels below record conversion, not approval
of this new native-art pass.

Map objects, all encounter periods and the referenced trainer parties establish
20 directly used species. Their complete evolution families contain 43 species.
Elaia owns the polished **Eripip** and **Galekit**, not their later stages.

| Coverage | Native redraw status |
|---|---|
| Halcyling, Galenyon | New matched native battle fronts, backs, six follower frames and two menu-icon frames implemented from `tools/dex/sprites/lines/halcyon.py` and its six hand-finished art grids. Existing normal/shiny color identities, palette files and bird footprints retained deliberately. Creative and matched in-game review still pending. |
| Ione, Titan Grunt | Native three-quarter portraits and all nine walker states redrawn in `sprites_trainers.py` and `sprites_npc.py`. Their existing portrait and shared cast palettes retained unchanged. Creative and matched in-game review still pending. |
| Eopeep, Alekrow, Hoplektor; Kerazap, Kerastorm; Harpeck, Harpelle; Epopoi, Lophops, Basilops; Karkipool, Karkitox; Ketofry, Kynoketos; Melibee, Melisseer; Onotis, Midonos; Ergant, Hoplomex; Narthip, Promethex; Nemecub, Nemeleon; Elaleaf, Elapling, Hierolive; Spalunk, Plouteras; Kampillar, Nymveil, Psychora; Pebblith, Cairnolith, Laolith; Narkeray; Chelonet, Chelyra; Gelasable | Still awaiting this batch's native polish; existing sprites retained, not claimed redrawn. This includes species used only by the local trainers. |
| Theo, Ianthe, Kleon, Alethea, Melitta; shared folk already polished in Elaia; pickups and starter kraters; Elaia's five contact effects | Elaia's human/opening-object checkpoint `dfb7974fbc` is integrated. Preserve these sources and sprites; the separate twelve-species checkpoint is still pending. |
| Kronion tablet; two upturned-boat halves | Tablet markings and lighting refined at native 16x16 resolution. The boat is now drawn directly at 32x16, then split into matched halves, instead of extracting and remapping tileset art. Existing cast palette and object wiring retained. Nine-map ROM gallery and same-camera prop before/after evidence captured; actor animation phases can differ. The tablet is captured during the Route 1 review's real cutscene drop, not an ordinary summit visit. Creative approval pending. |
| Other local folk and class portraits; local healing effects and emotes | Existing assets retained for now; local polish/review still outstanding. |
| Tiles, animated metatiles, battle backgrounds, UI, weather and move animations | Retained explicitly; not part of a native creature/character/object sprite redraw claim. Temple braziers and hearth-trial changes are metatiles, not object sprites. |

The town batch is **not complete**. Full shared regeneration and final ROM
evidence must follow integration of Elaia's landed polish so its assets are not
reverted. Greek god ball art has separate ownership and is excluded here.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Outdoor primary tileset `aethos` | `data/tilesets/primary/aethos/`, `porytiles/tilesets/gTileset_Aethos/`, `tools/ichor/art/aethos_*.py`, `design/phase1/TILES_aethos.md` | Greek | 1 | Replaces `general`: olives, cypress, limestone, Aegean, Asclepeion and Agora exteriors. Elaia, Route 1, Kronion Hill and Akti use it. 18 free tile slots. |
| Interior primary tileset `oikos` | `data/tilesets/primary/oikos/`, `design/phase1/TILES_oikos.md` | Greek | 1 | Replaces `building`: terracotta floors, klinai, amphorae. The TV becomes Mom's loom and the PC becomes the Pithos. Every slice interior uses it. |
| Secondary tilesets `kalliste`, `temple_hestia` | `data/tilesets/secondary/kalliste/`, `.../temple_hestia/`, `design/phase1/TILES_kalliste.md`, `TILES_temple.md` | Greek | 1 | Cycladic village, harbor, Kronion ruins and the Hestia temple interior. |
| Secondary tilesets `oikia`, `civic` | `data/tilesets/secondary/oikia/`, `.../civic/`, `design/phase1/TILES_oikia.md`, `TILES_civic.md` | Greek | 1 | Houses, the Asclepeion, the Agora and the Akademia. 48 civic tile slots are left. |
| Secondary tilesets `agros`, `akti` | `data/tilesets/secondary/agros/`, `.../akti/`, `tools/ichor/art/agros_*.py`, `akti_*.py`, `design/phase1/TILES_agros.md`, `TILES_akti.md` | Greek | 1 | Route 1's and Kronion Hill's countryside, and Akti's harbor. |
| Wiring the Greek tilesets into the slice maps | `data/layouts/layouts.json`, `data/maps/ElaiaVillage*`, `KallisteRoute1*`, `AktiTown*` | Greek | 1 | All 15 slice layouts are on Greek tilesets: aethos with kalliste, agros or akti outdoors, and oikos with oikia, civic or temple_hestia indoors. |
| Biome secondary tilesets to come | New `data/tilesets/secondary/*` | New | 2–5 | About 15: Astyra, Thyrsa vineyards and theater, Eleusa wheat and Mystery sanctum, Arkadia cypress forest, Kaldera caldera, Kythera coves, Knossa Labyrinth, Lakonia, Delphoi, Olympus, Underworld and Elysium, Atlantis (ART_PLAN §1). |
| Temple interiors for Hermes through Zeus, trireme decks, the Pithos room | New secondaries | New | 2–5 | The Hestia interior is the pattern. Table of orders and materials: ART_PLAN §1. |
| Hoenn secondary tilesets | `data/tilesets/secondary/*` (67 Hoenn folders, plus 62 FRLG folders that are not built) | Hoenn | 2–5 | Retired biome by biome as the Aethos maps replace Hoenn's. The Hoenn tilesets total about 428 KiB in the ROM. Frontier, Secret Base, Mirage Tower, Contest and Cable Club tilesets go with their systems (§10). |
| Hoenn primaries `general`, `building`, `secret_base` | `data/tilesets/primary/` | Hoenn | 2–5 | `aethos` and `oikos` replace the first two once every layout moves. `secret_base` is cut. `building_frlg` and `general_frlg` are not built. |
| Aethos tile animations | `include/porytiles_generated/tilesets/aethos/`, `src/tileset_anims.c` | Greek | 1 | Water, surf, waterfalls and anemones, at General's slots. |
| Hoenn tile animations | `src/tileset_anims.c` (25 `InitTilesetAnim_*` for Hoenn tilesets), `data/tilesets/secondary/*/anim/` | Hoenn | 2–5 | Dewford, Slateport, Mauville, Lavaridge steam, Pacifidlog bridges, Sootopolis, Underwater, Cave and the rest. About 116 KiB. |
| Door animations | `graphics/door_anims/` (85 sheets), `src/field_door.c` (25 KiB) | Greek | 1 | The five aethos doors open with Greek sheets (`graphics/door_anims/ichor_*.png`, `tools/ichor/art/doors.py`, `design/phase1/ITEMS.md`), and on an Ichor map no Hoenn door can play (`src/field_door.c`). The 85 Hoenn sheets stay for Hoenn maps and go with them. Kalliste's, akti's and civic's doors are non-animated by design. |
| Terrain contact effects | `graphics/field_effects/pics/`: `short_grass`, `tall_grass`, `long_grass`, `jump_*`, `cut_grass`, `sand_footprints`, `deep_sand_footprints`, `ripple`, `splash`, `water_surfacing`, `bubbles`, `ash*`, `bike_tire_tracks` and others | Greek | 1 | Tall grass (barley), long grass (reeds), sandal footprints, ripples, splashes and ledge dust are redrawn over the aethos tiles (`field_effects.py`, `design/phase1/FIELD_EFFECTS.md`). Ash, bubbles, deep sand and bike tracks are out of the slice's reach and take the new palettes. `bike_tire_tracks` is cut with bikes. |
| Shadows, emotes and sparkles | `graphics/field_effects/pics/shadow_*`, `emotion_*`, `emote_x`, `sparkle`, `shiny_sparkle`, `small_sparkle`, `graphics/misc/emotes.png` | Greek | 1 | The "!", "?", "!!", "X" and heart emotes are pottery shards (`FIELD_EFFECTS.md`), and so are the follower's eleven emotions (`graphics/misc/emotes.png`, `follower_icons.py`, `design/phase1/UI_remnants.md`). Shadows and sparkles are generic shapes. |
| Weather | `graphics/weather/` (9 files plus `drought*`), `src/field_weather*.c` | Keep | 6 | Rain, snow, fog, ash, sandstorm, drought, bubbles and clouds are generic. The Frozen Hour palette drain is an engine job. `sDroughtWeatherColors` is 49 KiB. |
| Asclepeion healing machine and monitor | `graphics/field_effects/pics/pokecenter_monitor.png`, `pokeball_glow.png`, `src/field_effect.c` | Greek | 1 | The rod-of-Asclepius relief lights gold and the healed balls float in the spring (`FIELD_EFFECTS.md`). Nurse text is §7. |
| Mart and Asclepeion light sprites | `graphics/object_events/pics/misc/poke_center_light.png`, `mart_light.png`, `light.png` | Hoenn | 2–5 | Window lights outside the doors. No slice map places one. Greek: oil lamps. |
| Berry trees | `graphics/object_events/pics/berry_trees/` (47 sheets), `graphics/berries/` (67 pics), `src/berry.c` | Hoenn | 2 | The bible says nothing about berries, and the slice already gifts an Oran Berry and a Sitrus Berry. Proposal: keep the system and restyle the trees and fruit as Greek fruit and herbs. Needs a director decision. |
| Cut, Rock Smash and Strength objects | `graphics/object_events/pics/misc/cuttable_tree.png`, `breakable_rock.png`, `pushable_boulder.png` | Hoenn | 2 | Field powers become relics (Labrys, Bronze Hammer, Girdle of Herakles). Greek: a thorn thicket or olive sapling, a marble rubble pile, a column drum. |
| Signs, statues and props | `graphics/object_events/pics/misc/sign.png`, `wooden_sign.png`, `gym_sign.png`, `statue.png`, `clipboard.png`, `birchs_bag.png`, `moving_box.png`, `town_map.png`, `pokedex.png`, `fossil*.png`, `old_amber.png`, `truck.png` | Hoenn | 2–5 | No slice map places any of them: the slice's signs are tiles, and its field objects are Ichor's (the Titanborn's tablet, the upturned boats). A temple stele for the gym sign comes first when a map needs one. `birchs_bag` and `truck` belong to Hoenn's opening and can go. |
| Item-ball pickups on the ground | `graphics/object_events/pics/misc/ichor_item_jar.png`, `tools/ichor/art/items.py` (Emerald's `ball_*.png` served it before) | Greek | 1 | A sealed clay jar: `OBJ_EVENT_GFX_ITEM_BALL` draws `ichor_item_jar.png` (`design/phase1/ITEMS.md`). Hoenn maps' item balls are jars too. |
| The follower's balls | `graphics/object_events/pics/misc/ball_*.png` (28), `tools/ichor/art/follower_icons.py` | Greek | 1 | At doors the follower goes into the party menu's black-figure ball. The other 27 balls keep their colors as painted caps (`design/phase1/UI_remnants.md`). The Poké Ball loads the townsfolk palette. |
| Event Pokémon sprites | `graphics/object_events/pics/pokemon_old/` (63) | Keep | Dex | Static overworld Pokémon (Azumarill, Kyogre and so on). Followers make most of them redundant. |
| Trireme and sailing sequence | `graphics/object_events/pics/misc/ss_tidal.png`, `graphics/ss_anne/` (wake, smoke), `src/ss_anne.c`, `src/seagallop.c` | New | 1–2 | The slice ends at the trireme in Akti's harbor, which the akti tiles paint at the quay. The bible replaces ferries with triremes. The moving trireme sprite and the crossing scene still need art. |
| Cable car | `graphics/cable_car/` (4), `src/cable_car.c` | Cut | 6 | Mt. Chimney only. Proposed in §10. |
| SS Tidal and ferries | `graphics/seagallop/`, `graphics/ss_anne/`, `mr_briney_boat.png`, `ss_tidal.png` | Cut | 6 | Replaced by triremes. Proposed in §10. |
| Secret-base decorations | `graphics/object_events/pics/dolls/` (41), `cushions/` (10), `graphics/decorations/` (43) | Cut | 6 | Per ART_PLAN (§10). |
| Hoenn gym puzzle mechanics | `src/rotating_gate.c` (16 KiB), Fortree and Mossdeep gym tiles and scripts | Cut | 6 | Used by Fortree Gym and Trick House 6 only. The Hearth trial is Ichor's own puzzle. Proposed in §10. |

## 2. People

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Theo and Ianthe: walking, running (Talaria wings), fishing (Old Rod), field-move (relic raise) | `graphics/object_events/pics/people/brendan/`, `.../may/`, `tools/ichor/art/sprites_player_ow.py`, `design/phase1/SPRITES_player_ow.md` | Greek | 1 | 4 of the 10 sheets each, and the surfing sheet below. The folders keep Brendan's and May's names and palettes (`brendan.pal`, `may.pal`), which also color the rival and link-player sprites. |
| Theo and Ianthe: surfing | `.../brendan/surfing.png`, `.../may/surfing.png` | Greek | 1 | Theo and Ianthe ride a Minoan dolphin (`surf_poses.py`, `surf_blob.png`, `FIELD_EFFECTS.md`). Poseidon's Conch, the relic that grants it, does not exist yet (§6). |
| Theo and Ianthe: underwater (Dive) | `.../underwater.png` | Hoenn | 5 | Atlantis and the Nereid Pearl. |
| Mach Bike and Acro Bike | `.../mach_bike.png`, `.../acro_bike.png`, `graphics/field_effects/pics/bike_tire_tracks.png`, `bike_shop` tileset | Cut | 6 | `SPRITES_player_ow.md` says Aethos has no bikes. The bible does not list a bike. Needs a director decision, including the three bike key items and the `bike_shop` maps. |
| Watering and decorating poses | `.../watering.png`, `.../decorating.png` | Cut | 6 | `SPRITES_player_ow.md`: no watering cans or secret bases. Tied to the berry decision (§1) for watering. |
| Ruby/Sapphire and FRLG player sheets | `.../people/ruby_sapphire_brendan/`, `ruby_sapphire_may/`, `rs_brendan.png`, `rs_may.png`, `leaf/`, `red/` | Cut | 6 | Never used by Aethos. |
| Player battle back pics | `graphics/trainers/back_pics/brendan.png`, `may.png`, `graphics/trainers/palettes/brendan.pal`, `may.pal`, `design/phase1/SPRITES_player.md` | Greek | 1 | Theo and Ianthe with throw animation. |
| Player front pics | `graphics/trainers/front_pics/brendan.png`, `may.png` | Greek | 1 | The boy-or-girl choice, the trainer card and the Birch speech use them. Ianthe's side of the choice was not captured in-game. |
| Other back pics | `graphics/trainers/back_pics/`: `brendan_rs`, `may_rs`, `red`, `leaf`, `steven`, `wally`, `old_man`, `pokedude`, `none` | Hoenn | 6 | 9 of 11 files are Hoenn, Kanto or tutorial characters. About 70 KiB of the 86 KiB of back pics. Alethea's new back pic (`alethea.png`) leads the catch tutorial in Wally's place, so `wally` and `old_man` are unused by Aethos. |
| Daphne, Alethea, Kleon, Ione, Titan grunt overworld sprites | `graphics/object_events/pics/people/ichor/`, `design/phase1/SPRITES_npc.md` | Greek | 1 | Shared palette `ichor_cast.pal`. |
| Kleon, Ione, Titan grunt, Daphne portraits | `graphics/trainers/front_pics/kleon.png`, `hierophant_ione.png`, `titan_grunt.png`, `professor_daphne.png`, `design/phase1/SPRITES.md` | Greek | 1 | Polish pass 1 done. Still open: 3/4 turns, more folds, Kleon's swagger pose, Ione unchanged. |
| Daphne in the new-game speech | `graphics/birch_speech/birch.png` | Greek | 1 | Same file as Birch's, so no code change. The text, Smoliv, the laurel-grove stage and the music are Ichor's too (§5, §7, §8). |
| Alethea portrait and back pic | none | New | 3 | Her back pic is drawn (`sprites_alethea_back.py`) and leads the catch tutorial. Her front portrait is not; she fights beside you in Act II's double battle. |
| The Twelve's Hierophants (2–8), the four Pantheon seats and the Archon | New `front_pics/`, `people/` | New | 2–5 | Ione is done. Names are in PITCH §3. |
| Team Titan admins (Hyperion, Iapetos, Rhea), Kronos and Phaedon, Elpis, Kallisto's hunt, the Fates | New | New | 3–4 | Phaedon is the healer behind the mask: his walker and portrait must read as the same man. |
| Townsfolk walkers (22) | `include/constants/event_objects.h:444-465` (aliases `OBJ_EVENT_GFX_ICHOR_*`), `graphics/object_events/pics/people/` | Greek | 1 | Drawn (`sprites_folk.py`, `design/phase1/SPRITES_folk.md`). Every person on the slice's maps is an Ichor sprite. |
| More civilians to reach about 40 types | New `people/` | New | 2–5 | Potters, philosophers, olive farmers, oracles, athletes and so on (ART_PLAN §2). |
| Hoenn and FRLG NPC walker sheets | `graphics/object_events/pics/people/*.png` (about 230 sheets including subfolders), 393 `OBJ_EVENT_GFX_*` ids | Hoenn | 2–5 | Retired as the Hoenn maps go. Keep the sheets of generic types (the shared poses) as palette bases only if useful. |
| Hoenn story characters and teams | `.../people/team_aqua/`, `team_magma/`, `gym_leaders/`, `elite_four/`, `frontier_brains/`, `steven.png`, `wally.png`, `wallace.png`, `prof_birch.png`, `scott.png` and similar | Cut | 6 | No counterpart in Aethos. Team Titan, the Hierophants and the Pantheon replace them. |
| Aethos trainer classes | `include/constants/trainers.h` (Lakonian, Shepherd, Harvester, Goatherd, Hoplite, Augur, Titanborn, Acolyte, Hierophant), `src/battle_main.c` `gTrainerClasses` | Greek | 1 | 9 classes. The bible wants about 25. |
| Aethos trainer-class portraits | `graphics/trainers/front_pics/shepherd.png`, `harvester.png`, `goatherd.png`, `hoplite.png`, `augur.png`, `acolyte_m.png`, `acolyte_f.png`, `design/phase1/SPRITES_classes.md` | Greek | 1 | 7 class portraits, plus the 4 cast portraits above, make 11 new pic ids. Front pics only. |
| Remaining Aethos classes and portraits (about 16) | New | New | 2–5 | Fisher, sailor, potter, hunter, philosopher, athlete, oracle, bronzesmith and the rest, as each biome needs them. |
| Hoenn trainer classes and pics | `include/constants/trainers.h` (66 Hoenn classes, 2 unused), `graphics/trainers/front_pics/`, `src/data/graphics/trainers.h` | Hoenn | 2–5 | 66 classes and 85 pic ids (83 untouched; Brendan and May were redrawn as Theo and Ianthe). All 158 front pics together are about 105 KiB. Aqua, Magma, Frontier, Contest and Battle Girl classes go with their systems. Suggested replacements from the nine class designs (the bible does not assign them): Hierophant for Leader, Titanborn for Aqua and Magma, Lakonian for Rival, Hoplite for Black Belt and Battle Girl, Augur for Psychic, Hex Maniac and Expert, Shepherd for Camper, Bug Catcher and Youngster, Harvester for Picnicker, Lass and Aroma Lady, Goatherd for Hiker and Ruin Maniac, Acolyte for the temple-room trainers. |
| FRLG trainer classes and pics | `include/constants/trainers.h` (50 `_FRLG` classes), `graphics/trainers/front_pics/*_frlg.png` (62), `back_pics/` | Cut | 6 | FRLG data is not otherwise built, but 62 pics are about 43 KiB of ROM. Per ART_PLAN. |
| Trainer-sighting music table | `src/data/trainer_approach_music.h` | Greek | 1 | Every jingle the slice's classes reach is Ichor's: the male, female, intense, suspicious, hiker, rival and Titan slots play `mus_ichor_encounter_*` (§8). Hoenn classes keep their Hoenn slots. |

## 3. Pokémon

The Aethos regional dex of about 150 species is designed separately in `design/dex/` (not in this worktree). How it mixes with the existing nine generations is still open (`PITCH.md` §4). So these rows say what each group costs and what depends on the decision. The existing species are generation 1 to 9 art, not Hoenn's alone.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Existing species front, back, icon, footprint and palettes | `graphics/pokemon/` (1,029 folders), `src/data/pokemon/`, `src/pokemon.o` | Keep | Dex | 1,571 species and form entries. About 5.9 MB of ROM (22 %), about 3.7 KiB per form. The slice's starters and Route 1 mons use this art. Not Hoenn-specific. |
| New Aethos species (about 150): sprites, icons, footprints, palettes, shiny palettes, follower sprites | `graphics/pokemon/<species>/` | New | 2–5 | Gen 3 pic format. Done by biome as the story reaches them. |
| Cries | `sound/direct_sound_samples/cries/`, `sound/cry_tables.inc` | Keep | Dex | About 1,160 sampled cries: 9.4 MB, 35 % of the ROM, about 8 KiB each. The biggest single block in the ROM. Cries for removed species are the largest ROM lever (§10). |
| New Aethos cries | `sound/direct_sound_samples/cries/` | New | 2–5 | One per new species. |
| Follower and overworld Pokémon sprites | `graphics/pokemon/*/overworld*.png` | Keep | Dex | Followers are on (`e3dd2df4c2`). New species need theirs. |
| Pokédex entry text | `src/data/pokemon/species_info/` (descriptions) | Keep | Dex | New species need entries in Daphne's voice ("every myth is a memory of a Pokémon"). |
| Hoenn dex mode and Hoenn dex ordering | `src/pokedex.c` (`DEX_MODE_HOENN`, "HOENN DEX"), `src/data/` order tables | Hoenn | 1 | The codex lists by national number and the mode is named AETHOS DEX, but its AETHOS counts still walk Hoenn's regional order (QA m7). The dex team is building the Aethos order. |
| Fusion, Dynamax and Tera forms and art | species info, `graphics/battle_interface/*_indicator.png` | Keep | Dex | The bible turns Z-Moves, Dynamax and Tera off. Their art costs ROM but is harmless. |
| Apotheosis (Mega Evolution) trigger and Ichor Stones | `graphics/battle_interface/mega_trigger.png`, `mega_indicator.png`, 92 Mega Stone items | New | 4 | The trigger is painted as the Omphalos (§4). The 92 stones and the Apotheosis wording wait for Phase 4 (`design/TERMS.md`). All classic and Z-A Megas are in the species data. |

## 4. Battles

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Greek battle backgrounds: grass, sand, water, building (also gym, leader, plain, frontier) | `graphics/battle_environment/{tall_grass,sand,water,building,plain}/`, `src/data/battle_environment.h`, `design/phase1/BATTLE_BG.md` | Greek | 1 | 8 environments: the olive grove, Akti's shore, the open Aegean and the Doric temple hall with its leader, gym and plain variants. `KYOGRE` uses the water tiles in a storm palette. |
| Other Greek backgrounds still needed | `graphics/battle_environment/{cave,rock,long_grass,pond_water,underwater}/` | Hoenn | 2–5 | Cave, mountain, long grass, pond and underwater are still Emerald's. Needs: cypress forest, caldera, Labyrinth, Underworld, Atlantis, Olympus. |
| Elite Four, Champion and Pantheon halls | `graphics/battle_environment/stadium/`, `sky/`, `src/data/battle_environment.h` (Sidney, Phoebe, Glacia, Drake, Champion) | Hoenn | 4 | The Pantheon needs five Olympus halls. |
| Team Aqua, Team Magma, Groudon, Kyogre and Rayquaza backgrounds | same | Cut | 6 | No Aethos equivalent. The Primordials may need one scene each in Phase 5. |
| Expansion extra backgrounds (puddle, marsh, swamp, snow, ice, volcano, space and so on) | `src/data/battle_environment.h` | Keep | 6 | They reuse base tiles. |
| Healthboxes, HP and EXP bars, status and ball indicators | `graphics/battle_interface/` (71 files), `src/battle_interface.c` | Greek | 1 | Terracotta plaques, ink-drawn tubes and little kraters for the party balls (`design/phase1/UI_battle.md`). The type indicators beside the healthbox are generic (Keep). |
| Battle text box and action and move menus | `graphics/battle_interface/textbox*`, `move_info_window_*`, `src/battle_message.c` | Greek | 1 | The dialogue box itself, with ink-pointer menus on parchment (`UI_battle.md`). Wording is §7. |
| Battle transitions | `graphics/battle_transitions/` (23 files), `src/battle_transition.c`, `src/battle_transition_frontier.c` | Greek | 1 | Bands of a turning pot for wild battles and a black-figure face-off for trainers (`UI_battle.md`). The Aqua, Magma, Regi, legendary, Elite Four mugshot and Frontier set pieces are Hoenn's art, and no slice battle plays them. |
| Poké Ball sprites and capture sequence | `graphics/balls/` (29), `src/pokeball.c` | Keep | — | The director ruled that Poké Balls keep their name and look (`design/phase1/ITEMS.md`). The party menu, the battle tokens and the follower's balls paint them black-figure. |
| Throw, shake, open and move animations | `graphics/battle_anims/` (476 files), `data/battle_anim_scripts.s` | Keep | — | ART_PLAN keeps these. About 306 KiB of art plus 243 KiB of scripts. |
| Type and status icons | `graphics/types/` (28), `graphics/interface/status_icons.png`, `src/data/types_info.h` | Keep | 6 | Generic. Contest category icons in `graphics/types/` go with contests. |
| Mid-battle trainer slide tables | `src/trainer_slide.c` (`sTrainerSlides` 275 KiB, `sFrontierTrainerSlides` 94 KiB) | Keep | 6 | A feature to keep, but both tables are empty arrays sized by trainer count × 3 difficulties. About 369 KiB of ROM is zeros. 94 KiB is counted in the Frontier row (§10); the other 275 KiB is in no cut total. It shrinks when the Hoenn trainer ids go. |
| Frontier battle UI (Dome tourney tree, Factory, Arena, Palace and so on) | `src/battle_dome.c`, `battle_factory_screen.c`, `battle_arena.c`, `battle_palace.c`, `graphics/battle_frontier/` | Cut | 5 | Per ART_PLAN, except the engine that the Olympiad reuses (§10). |
| Apotheosis trigger button and flash | `graphics/battle_interface/mega_trigger.png` | Greek | 4 | The Omphalos, Delphi's netted stone: dim marble until pressed, then lit with golden ichor (`UI_battle.md`). The gimmick's wording waits for Phase 4. |

## 5. Screens

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Boot copyright screen | `graphics/intro/copyright.png`, `copyright.bin`, `src/intro.c` | Greek | 1 | Black gloss between meander rules: it credits Pokémon's makers and calls Ichor a fan-made game (`design/phase1/INTRO.md`). |
| Expansion "powered by" credit | `graphics/expansion_intro/`, `src/expansion_intro.c`, `EXPANSION_INTRO` in `include/config/general.h` | Greek | 1 | Restyled: "POWERED BY" over a gilded PRET × RHH, between meander rules (`INTRO.md`). It keeps the upstream attribution. |
| Game Freak logo and drops | `graphics/intro/scene_1/` (`drops_logo.png`, `logo.pal`, `sparkle.png`), `src/intro.c` | Greek | 1 | Replaced by the studio mark: a drop of ichor that blooms into ΙΧΩΡ (`INTRO.md`). |
| Latios, Latias, Flygon, Brendan and May intro | `graphics/intro/scene_2/` (bicycle, houses, `latias.png`, `latios.png`, `flygon.png`, `manectric.png`, `volbeat.png`) | Greek | 1 | Replaced by the black-figure frieze of Aethos that Clotho's thread runs along (`INTRO.md`). The bible maps Latias and Latios to the Dioskouroi (PITCH §4), so their art can return in a Greek scene later. |
| Legendary trio sequence | `graphics/intro/scene_3/`, `src/intro.c` | Greek | 1 | Replaced by the Fates' loom, where Atropos stops at the golden thread (`INTRO.md`). |
| Title screen: the Fates amphora | `graphics/title_screen/`, `src/title_screen.c`, `tools/ichor/art/title_screen.py`, `design/phase1/TITLE.md` | Greek | 1 | The music is Ichor's (§8), and the expansion's Quickstart badge is hidden (`QUICKSTART_HUD`). |
| Main menu (New Game, Continue, Options) and Continue panel | `src/main_menu.c`, `graphics/interface/main_menu_*.pal` | In progress (batch) | 1 | The Continue panel says LAURELS and the windows use the Greek frames. Another agent is repainting the lavender backdrop (QA P6). |
| Birch speech scene | `graphics/birch_speech/`, `src/main_menu.c` (about lines 1270–1830), `data/text/birch_speech.inc` | Greek | 1 | Daphne in the Akademia's laurel grove at dawn, with Smoliv, her own words and `MUS_ICHOR_NEW_GAME` (`design/phase1/UI_world.md`). The labels keep Birch's names so `main_menu.c` needs no logic changes. |
| Start menu | `src/start_menu.c`, `src/strings.c:427-433,874-884` | Greek | 1 | POKéDEX, AUGURY, POKéMON, BAG, the player's name, SAVE, OPTION and EXIT on the pottery frame. POKéNAV is defined but never shown. |
| Starter selection | `graphics/starter_choose/` (5), `src/starter_choose.c` | Greek | 1 | Three kraters on Daphne's table (`UI_world.md`). The flow is Emerald's, per ruling 11. |
| Naming screen | `graphics/naming_screen/` (16), `src/naming_screen.c` | Greek | 1 | A writing tablet and a wax keyboard (`design/phase1/UI_codex.md`). Defaults are THEO and IANTHE. |
| Options menu | `src/option_menu.c`, `graphics/text_window/1–20.png` | Greek | 1 | Twenty pottery frame choices (`text_window`). |
| Dialogue box, name box, signpost, menu frames | `graphics/text_window/` (24 files), `tools/ichor/art/ui_frames.py` | Greek | 1 | Terracotta, black-figure, with a meander border. |
| Bag screen | `graphics/bag/`, `src/item_menu.c` | Greek | 1 | The traveler's satchel (`design/phase1/UI_menus.md`). The Pyramid bag goes with the Frontier. |
| Party menu | `graphics/party_menu/`, `src/party_menu.c` | Greek | 1 | Clay plaques on terracotta (`UI_menus.md`). Its prompts are in sentence case (QA P3). |
| Summary screen | `graphics/summary_screen/`, `src/pokemon_summary_screen.c` | Greek | 1 | Papyrus unrolled from a scroll rod (`UI_menus.md`). The contest page is hidden. The skills page's RIBBON box is §11. |
| Shop | `graphics/shop/`, `src/shop.c` | Greek | 1 | The Agora's market stall (`UI_menus.md`). |
| Map-name popups | `graphics/map_popup/` (14), `src/map_name_popup.c` | Greek | 1 | Steles and plaques (`UI_menus.md`). |
| Pokédex | `graphics/pokedex/` (28), `src/pokedex.c`, `src/pokedex_area_screen.c` | Greek | 1 | A bronze-cornered codex (`UI_codex.md`). The area glow is gold hatching and the unknown Pokémon a clay roundel (`UI_remnants.md`). The HGSS dex is off. |
| Region map and Fly map | `graphics/pokedex/region_map*.png` (Hoenn, Kanto and Sevii maps), `src/region_map.c`, `src/field_region_map.c`, `src/data/region_map/` | Greek | 1 | A black-figure map of Aethos on all three screens (`UI_world.md`, `design/AETHOS_MAP.md`). The Kanto and Sevii maps are FRLG leftovers and never show. |
| Pithos storage screen | `graphics/pokemon_storage/` (92 files, 30 box wallpapers), `src/pokemon_storage_system.c` | Greek | 1 | Sixteen painted jars, named in the wallpaper menu (`UI_codex.md`). |
| Trainer card | `graphics/trainer_card/` (`badges.png`, bronze, copper, silver, gold, `bg.bin`), `src/trainer_card.c` | Greek | 1 | A kylix with a wreath of Laurels (`UI_world.md`). |
| Evolution scene | `graphics/evolution_scene/`, `src/evolution_scene.c` | Greek | 1 | A black-figure radiance (`UI_world.md`) with gold sparks (`UI_remnants.md`). |
| Trade scene | `graphics/trade/` (11), `src/trade.c` | Hoenn | 1 | Kimon's Finizen trade in Glykera's bakery plays it, so the slice shows Emerald's trade art. The GBA and cable art is link-only. |
| Hall of Fame | `src/hall_of_fame.c`, `graphics/misc/hall_of_fame.png`, `graphics/field_effects/pics/hof_monitor*` | Hoenn | 4 | The Pantheon's laurel hall. Its strings already say HALL OF HEROES (§7); the art is Emerald's. |
| Credits | `src/credits.c`, `src/data/credits.h` (57 staff pages), `graphics/credits/`, `graphics/intro/scene_2/*_credits.png` | Hoenn | 4 | Emerald's Game Freak staff roll and the bike scenery. See §11. |
| Dex diploma | `graphics/diploma/` (Hoenn and National palettes), `src/diploma.c` | Hoenn | 4 | Signed PROF. DAPHNE now (§7). The art is Emerald's. |
| Wall clock | `graphics/wallclock/`, `src/wallclock.c` | Greek | 1 | The klepsydra (`UI_world.md`). |
| DexNav (the Augur's Eye) | `graphics/dexnav/` (9), `src/dexnav.c`, `include/config/dexnav.h` | Greek | 1 | An augur's tablet (`design/phase1/UI_remnants.md`, QA P5). The register line still reads the expansion's "R TO REGISTER!". |
| Scroll of Deeds (quest log) | not in the ROM | New | 3 | PITCH §5 promises it. No quest-log code exists. |
| Difficulty select and the Oath of the Styx | not in the ROM as screens | New | 1 | The bible's four difficulties and the Nuzlocke oath need a new-game screen. `include/constants/difficulty.h` exists. |
| Laurel case | not in the ROM | New | 1 | ART_PLAN §5. Could share the trainer card's laurel art. |
| Save prompt and save info panel | `src/start_menu.c`, `src/strings.c:957` (`gText_SavingBadges`), `data/text/save.inc` | Greek | 1 | PLAYER, LAURELS and TIME on the pottery frame, with the place in the dialogue red. |
| Reset-clock and save-error screens | `graphics/reset_rtc_screen/`, `src/reset_rtc_screen.c`, `src/main_menu.c:259-262` | Keep | 6 | Generic text on the pottery frames. The save-failed screen stands on the Akademia art of the starter table; its small clock icon (`graphics/misc/clock_small.png`) is Emerald's. See §11. |
| Easy Chat and Mail | `graphics/easy_chat/` (9), `graphics/mail/` (12 mail designs), `src/easy_chat.c` | Hoenn | Keep | Kept for now ("where safe"): mail items and the Frontier still use them. 45 KiB. |
| Berry tag and berry check | `graphics/bag/berry_tag*`, `check_berry*`, `src/berry_tag_screen.c` | Greek | 1 | A clay label tied with twine (`ui_berry_tag.py`, `UI_remnants.md`). The berry pictures (`graphics/berries/`) are still Emerald's fruit, with the berry decision (§1). |
| Pokémon Jump, Berry Crush, Dodrio picking, slot machine and roulette screens | `graphics/pokemon_jump/`, `berry_crush/`, `dodrio_berry_picking/`, `slot_machine/`, `roulette/` | Cut | 6 | Per ART_PLAN, as minigames (§10). |
| Contest, Berry Blender, Pokéblock, PokéNav, Union Room, Mystery Gift, Wonder Card and secret-base screens | `graphics/contest/`, `berry_blender/`, `pokeblock/`, `pokenav/`, `union_room_chat/`, `wonder_card/`, `wonder_news/`, `link/`, `wireless_status_screen/` | Cut | 6 | Per ART_PLAN (§10). |
| Link and Frontier screens: Frontier Pass, Trainer Hill, picture frames | `graphics/frontier_pass/`, `graphics/picture_frame/` | Cut | 5 | See §10. |

## 6. Items

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Item icons, 874 items | `graphics/items/icons/` (619 PNGs), `graphics/items/icon_palettes/`, `src/data/items.h` | Hoenn | 2–5 | All Emerald and expansion icons except the slice's 34, which are Greek (row below; `items.py`, `design/phase1/ITEMS.md`). About 115 KiB. Restyle phase by phase. Items wild Pokémon may hold in the slice (Pretty Feather, Everstone and others) keep Emerald's. |
| Medicines and battle items | `graphics/items/icons/` | Greek | 1 | The slice's: clay flasks, herb bundles tied with colored wool, amphoriskoi of nectar and incense cones (`ITEMS.md`). The rest go with the row above. |
| Poké Balls and their cases | 28 ball items, `graphics/items/icons/*_ball.png`, `graphics/balls/` | Keep | — | Director's ruling: the name and look stay (`ITEMS.md`). See §4. |
| Berries | 68 berry items, `graphics/berries/` | Hoenn | 2 | Oran and Sitrus are a fig and a quince (`ITEMS.md`); the other 66 are Emerald's. See §1. 15 berry descriptions end with "{POKEBLOCK} ingredient". |
| TMs and HMs | 108 items (100 TMs, 8 HMs), `graphics/items/icons/tm.png`, `hm.png`, `tm_case.png` | Greek | 1 | Every TM is a sealed papyrus scroll and every HM a wax tablet, in the type's color (`ITEMS.md`). The eight HMs become relics (next row). |
| Field-power relics | none (`ITEM_TALARIA`, `ITEM_LABRYS` and the rest do not exist) | New | 1–3 | Talaria (run), Daedalus's Wings (Fly), Poseidon's Conch (Surf), Bronze Hammer (Rock Smash), Labrys (Cut), Girdle of Herakles (Strength), Hecate's Torch (Flash), Nereid Pearl (Dive): 0 of 8 exist. The player's field-move pose already raises a relic. Waterfall has no relic in PITCH §5. The slice needs only the Talaria, which Mom gives you in beat 1. |
| Omphalos (Mega key stone) | `ITEM_MEGA_RING` (key item "Mega Ring") | New | 4 | Rename and redraw. |
| Ichor Stones (Mega Stones) | 92 Mega Stone items | Hoenn | 4 | Redraw as one shared icon family with per-stone glints. |
| Laurels (badges) | `graphics/trainer_card/badges.png`, item/flag `FLAG_BADGE01_GET…08` | Greek | 1 | The trainer card's wreath gilds a leaf with its god's emblem for each Laurel (`UI_world.md`). The Hearth Laurel is the slice's reward. |
| Augur's Eye, Scroll of Deeds, Laurel case | key items | New | 1–3 | Icons for the Talaria, the Augur's Eye, the codex and the Hearth Laurel are drawn but not wired, because the slice keeps them as flags (`ITEMS.md`). The Scroll of Deeds and the Laurel case have no item yet. |
| Hoenn and Kanto key items | `src/data/items.h` (about 37: S.S. Ticket, Devon Parts, Go-Goggles, Devon Scope, Basement Key, Scanner, Storage Key, four Room Keys, Meteorite, Magma Emblem, Contest Pass, Letter, Eon, Mystic and Aurora Tickets, Old Sea Map, Parcel, Secret Key, Bike Voucher, Gold Teeth, Card Key, Lift Key, Silph Scope, Tri-Pass, Rainbow Pass, Tea, Ruby, Sapphire, Wailmer Pail, Poké Flute, Soot Sack, Teachy TV, Fame Checker) | Cut | 6 | No place in Aethos. |
| Bikes | Bike, Mach Bike, Acro Bike, Bike Voucher | Cut | 6 | See §2. |
| Contest items | 5 Contest Scarves, {POKEBLOCK} Case, Contest Pass | Cut | 6 | Per ART_PLAN (§10). |
| Items for gimmicks the bible turns off | 35 Z-Crystals, Z-Power Ring, Dynamax Band, Dynamax Candy, Max Mushrooms, Max Honey, Tera Orb, 19 Tera Shards | Cut | 6 | PITCH §5: only Apotheosis stays. Proposed. |
| Names that say Hoenn or Kanto | "Poké Ball", "Poké Doll", "Poké Toy", "Poké Radar", "Poké Flute", "Pokéshi Doll", "Devon", "S.S." | Hoenn | 6 | The bible's "Pokémon" is kept, so "Poké Ball" may stay. Decide the ball family name once (§4). |
| Mail items (12 designs) | `graphics/mail/` | Cut | 6 | With Easy Chat. |
| Fossils, Apricorns, shards, other generic items | `graphics/items/icons/` | Keep | 6 | Names and icons are generic. Restyle opportunistically. |

## 7. Text

Counts are matching lines or strings from `grep`, so they are not exhaustive.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| New-game speech | `data/text/birch_speech.inc` (3 Birch blocks), `src/strings.c:46`, `src/main_menu.c` | Greek | 1 | Daphne's speech ("every myth is a memory of a Pokémon"). The labels keep Birch's names. |
| Starter-choice strings | `src/strings.c:63-64` | Greek | 1 | "Three Pokémon. Three kraters." and "Will this Pokémon be your partner?" |
| Whiteout and rescue messages | `src/field_screen_effect.c:64,66,1471` | Greek | 1 | "hurried to the Asclepeion" and "hurried back home". No PROF. BIRCH remains. |
| Asclepeion nurse text | `data/text/pkmn_center_nurse.inc` (10 strings), `data/scripts/pkmn_center_nurse*.inc` | Greek | 1 | The healer speaks Ichor's lines (ruling 6); the Hoenn copies stay for Hoenn's centers. |
| Pithos (PC) strings | `data/text/pc.inc`, `data/scripts/pc.inc` ("SOMEONE'S PC", "LANETTE'S PC") | Greek | 1 | The Pithos and its jars (ruling 6). |
| Start and main menu labels | `src/strings.c:427-433,874-884`, `src/main_menu.c:277` | Greek | 1 | AUGURY, LAURELS, POKéDEX. POKéNAV is defined but never shown. |
| Pokédex dex-mode titles | `src/pokedex.c:1184`, `src/strings.c:904,909` | Greek | 1 | AETHOS DEX and NATIONAL DEX. The counts behind AETHOS are §3. |
| Pokédex rating | `data/text/pokedex_rating.inc` (about 25 rating blocks), `src/strings.c:53` | Greek | 4 | Daphne gives the rating; no HOENN or BIRCH remains. |
| Hall of Fame and diploma text | `src/strings.c:57,63,906`, `src/hall_of_fame.c` | Greek | 4 | "ARCHON OF AETHOS!", HALL OF HEROES, and the diploma signed PROF. DAPHNE. |
| Battle messages that name Hoenn people | `src/battle_message.c` (`STRINGID_DONTLEAVEBIRCH`, `gText_WhatWillWallyDo`, `gText_BattleWallyName`, the Wally catch tutorial, the champion lines at `:1524-1527`) | Greek | 1 | Daphne and Alethea stand in for Birch and Wally. No other battle line names a Hoenn person; the Battle Arena referee's lines go with the Frontier (§11). |
| Trainer class names | `src/battle_main.c` `gTrainerClasses` | Hoenn | 2–5 | 9 Aethos names are in. 116 Hoenn and FRLG names remain, including "ELITE FOUR", "CHAMPION" and "LEADER". |
| Place names and landmarks | `src/data/region_map/region_map_sections.json` (241 map sections; 32 are Aethos's), `src/landmark.c` (27), `src/data/heal_locations.json` (44) | Hoenn | 2–5 | Kalliste's three sections and 29 more Aethos sections are in (`UI_world.md`), so the popups, the Fly map and the summary's "Met at" name ELAIA VILLAGE, ROUTE 1 and AKTI TOWN. Hoenn's 209 sections and 27 landmarks stay with Hoenn's maps. |
| Hoenn words in strings: HOENN, BIRCH, POKéNAV, POKéMON CENTER, MART, GYM, LEAGUE | the files in the rows above, plus `data/text/*.inc` and `src/data/*.h` | Hoenn | 1–5 | The count below is matching string lines (FRLG left out). System text and shared scripts: HOENN 14, BIRCH 4, POKéNAV 41, POKéMON CENTER 14, GYM 105, LEAGUE 24, down from 20, 10, 41, 19, 105 and 27; what is left serves Hoenn's systems and cut ones, and the slice's 269 messages show none. Hoenn map scripts: HOENN 42, BIRCH 45, POKéNAV 53, POKéMON CENTER 8, MART 13, GYM 169, LEAGUE 43. The map scripts go with the maps. "POKé MART" never appears as a string. |
| Trainer dialogue | `data/text/trainers.inc` (2,507 string lines, about 855 Hoenn trainers) | Hoenn | 2–5 | Mentions GYM BADGES, LEAGUE and CHAMPION. The 14 Ichor trainers' text is in `SCRIPT.md`. |
| Hoenn map-script dialogue | `data/maps/*/scripts.inc` (about 520 non-FRLG folders, 15,700 string lines) | Hoenn | 2–5 | Hoenn counts: 42 "HOENN", 45 "BIRCH", 53 "POKéNAV", 169 "GYM", 43 "LEAGUE", 63 "TEAM AQUA", 65 "TEAM MAGMA", 53 "CONTEST", 8 "POKéMON CENTER". Goes away with the maps. |
| Slice dialogue | `design/phase1/SCRIPT.md`, `data/maps/{ElaiaVillage*,KallisteRoute1*,AktiTown*}/scripts.pory` | Greek | 1 | The maps and scripts batch, in Poryscript. The slice's 269 messages show no Hoenn word (QA). |
| Story, tutor and lottery text | `data/text/move_tutors.inc` (Mossdeep, Sootopolis gyms), `apprentice.inc`, `mauville_man.inc`, `lottery_corner.inc`, `tv.inc`, `match_call.inc` (69 lines), `fame_checker_frlg.inc` | Cut | 6 | Most go with their systems (§10). Move-tutor text needs a rewrite if tutors stay. |
| Berry descriptions that mention Pokéblocks | `src/data/items.h` (15 berries, "{POKEBLOCK} ingredient") | Hoenn | 2 | Goes with the Pokéblock cut. |
| Item descriptions | `src/data/items.h` | Hoenn | 2 | Mostly generic. A few mention Contests, Devon Corp and Poké Flute. |
| Shared strings that say Pokémon | `src/strings.c`, `src/battle_message.c` and the party and summary screens | Keep | 6 | The title is "Pokémon Ichor", so "POKéMON" and the `{PKMN}` glyph stay. Decide once and record it (§11). |

## 8. Audio

Songs by use. Counts are from `include/constants/songs.h` and sizes are from the map (KiB of ROM). The ROM holds about 220 songs.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Ichor songs: Elaia, Route 1, Akti, Hestia temple, Asclepeion, Titan, trainer, wild and rival battle themes, trainer victory | `sound/songs/midi/mus_ichor_*.mid` (10, 16 KiB), `sound/voicegroups/` Ichor voicegroup, `tools/ichor/music/` | Greek | 1 | 36 songs, among them every slice town, route, building and battle theme, the encounter jingles, the fanfares, the title and the intro. Registered at the end of `song_table.inc`, with 27 Emerald slots repointed. |
| Slice fanfares and the rest of the slice's songs | `include/constants/songs.h` | Greek | 1 | Every song and fanfare the slice plays is Ichor's: caught, victories, level up, heal, badge, item, evolved, TM and evolution, the title, the intro and the speech. |
| Title theme | `MUS_TITLE` in `src/title_screen.c:671` | Greek | 1 | `MUS_TITLE` plays `mus_ichor_title`. |
| Intro tracks | `MUS_INTRO`, `MUS_INTRO_BATTLE` in `src/intro.c:1208,1731` | Greek | 1 | `MUS_INTRO` plays `mus_ichor_intro`. `MUS_INTRO_BATTLE` belonged to the legendary scene, which is gone. |
| New-game speech music | `src/main_menu.c:1291` (`PlayBGM`) | Greek | 1 | `MUS_ICHOR_NEW_GAME`. |
| Towns and cities | 13 songs, 49 KiB: Littleroot, Oldale, Petalburg, Rustboro, Dewford, Slateport, Verdanturf, Fallarbor, Fortree, Lilycove, Sootopolis, Ever Grande (plus a test track) | Hoenn | 2–5 | One theme per Aethos town as it arrives. |
| Routes, woods and travel | 17 songs, 56 KiB: Routes 101, 104, 110, 113, 118, 119, 120, 122, Petalburg Woods, cycling, surf, sailing, underwater, desert, two GSC leftovers, Follow Me | Hoenn | 2–5 | Cycling is cut with bikes. |
| Dungeons and set pieces | 12 songs, 39 KiB: Mt. Chimney, Mt. Pyre (and exterior), Cave of Origin, Abandoned Ship, Sealed Chamber, Aqua/Magma hideout, Victory Road, abnormal weather, Groudon weather, Awaken Legend, Rayquaza appears | Hoenn | 3–5 | Keep the shape of a few (cave, victory road) as Aethos dungeons. |
| Buildings and indoor | 8 songs, 20 KiB: Pokémon Center, Mart, Gym, Birch Lab, Pokémon School, two museums, Help | Hoenn | 2–5 | The slice plays Ichor's Asclepeion, temple, Agora and Akademia themes; its houses play their town's. These Hoenn songs serve Hoenn's maps. |
| Battle themes | 14 songs, 45 KiB: wild, trainer, gym leader, rival, Aqua/Magma, champion, Elite Four, Kyogre/Groudon, Rayquaza, Regi, Mew, Frontier Brain, legend beast, intro battle | Hoenn | 2–4 | The Ichor wild, trainer and rival themes exist. Still needed: Hierophant, Titan admins, Pantheon, Archon, Kronos and Dialga. |
| Trainer-sighting jingles | 17 songs, 39 KiB (`MUS_ENCOUNTER_*`) | Greek | 1 | The slots the slice's classes reach play `mus_ichor_encounter_*` (§2). The Hoenn jingles stay for Hoenn's classes. |
| Fanfares and jingles | 18 songs, 24 KiB: caught, victory (wild, trainer, leader, league, Aqua/Magma, road), level up, heal, badge, item, evolved, TM, evolution (and intro), move deleted, berry, "too bad" | Greek | 1 | Every fanfare the slice plays is Ichor's. The berry, move-deleted, "too bad" and league jingles are Emerald's, and the slice never plays them. |
| Title, credits, Hall of Fame | 6 songs, 32 KiB: title, intro, credits, end, Hall of Fame, HoF room | Hoenn | 4 | The title and intro are Ichor's (rows above). The credits, end and Hall of Fame songs come with Act III. |
| FRLG songs | 75 songs, 239 KiB (`mus_rg_*`) | Cut | 6 | Per ART_PLAN. Built into the ROM. |
| Songs of cut systems | 31 songs, 94 KiB: contests, link contests, Frontier, Game Corner, slots, roulette, Trick House, Safari Zone, Cable Car, match call | Cut | 6 | Counted in §10. |
| Sound effects (269) | `sound/songs/midi/se_*.mid` (31 KiB total), `include/constants/songs.h` | Keep | — | 227 are generic: 130 move effects and about 97 UI, battle and field sounds (menu, door, ball, level up, faint, ledge, dex and so on). |
| Hoenn-specific sound effects | `SE_POKENAV_*` (4), `SE_CONTEST_*` (8), `SE_BERRY_BLENDER` (1), `SE_ROULETTE_*` (2), `SE_PIKE_*` (2), `SE_ARENA_*` (2), `SE_TRUCK_*` (4), `SE_BALLOON_*` (3), `SE_RG_*` (15), `SE_SUDOWOODO_SHAKE` (1) | Cut | 6 | 42 effects that go with their systems. Under 5 KiB. |
| Instruments, voicegroups and mixing | `sound/direct_sound_samples/` (107 samples, 754 KiB), `sound/voicegroups/` (183 files, 249 KiB) | Keep | 1 | The shared engine. The Ichor voicegroup (`ichor.inc`) maps Greek roles (lyre, kithara, aulos, frame drum) onto existing Emerald samples, so there are no new sampled instruments yet. |
| Cries | `sound/direct_sound_samples/cries/` | Keep | Dex | See §3. |
| Mauville Old Man phonemes | `sound/songs/midi/ph_*.mid` (51), `sound/direct_sound_samples/phonemes/`, `src/bard_music.c` | Cut | 6 | 162 KiB. Proposed (§10). |

## 9. Data

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Hoenn maps | `data/maps/`, `data/layouts/` | Cut | 2–5 | Removed by hoenn-cut batch 2 with their layouts, scripts, encounter tables, heal locations and the tilesets only they used. What's left is the Ichor maps and, until batch 3, the Battle Frontier and Trainer Hill maps. `include/constants/maps_removed_stub.h` keeps the removed names compiling for upstream code. |
| Ichor maps | `data/maps/{ElaiaVillage*,KallisteRoute1*,AktiTown*}`, `data/ichor_maps.inc` | Greek | 1 | 15 maps: Elaia and its four interiors, Route 1, Kronion Hill, Akti and its six interiors, all on Greek tilesets, with Poryscript scripts. |
| FRLG maps, tilesets and scripts | `*_Frlg` maps, `*_frlg` tilesets and scripts | Cut | 6 | Removed by hoenn-cut batch 2. They were never in the Emerald ROM. A few FRLG tileset animation frames stay, because `src/tileset_anims.c` names them. On upstream merges, resolve modify/delete conflicts on these paths with `git rm`. |
| Hoenn trainers | `src/data/trainers.party`, `include/constants/opponents.h`, `src/data/battle_partners.party` (2) | Cut | 2–5 | Removed by hoenn-cut batch 1: 847 Hoenn trainers gone, Ichor's 14 renumbered 1–14, and the seven Frontier Brains kept at 15–21 for the Frontier engine. `gTrainers` fell from 132 KiB to 3.4 KiB and now grows only with real trainers. Id ranges per session are in `tools/ichor/claim_ranges.md`. `PARTNER_STEVEN` is still there. FRLG's 624 trainers in `trainers_frlg.party` are not built. |
| Trainer-slide tables | `src/trainer_slide.c` | Keep | 6 | 187 KiB of mostly empty pointers: `sTrainerSlides` (156 KiB, (`MAX_TRAINERS_COUNT` 1,536 + partners) × 26 slides) and `sFrontierTrainerSlides` (30 KiB). Ichor keeps one difficulty's slides for every difficulty, a third of upstream's size. A sparse table would free most of the rest. |
| Hoenn wild encounter tables | `src/data/wild_encounters.json` | Cut | 2–5 | Removed by hoenn-cut batch 2: 388 Hoenn and FRLG headers. |
| Heal locations | `src/data/heal_locations.json` | Greek | 1 | Elaia and Akti, plus the Battle Frontier's until batch 3. |
| Fly destinations and region sections | `src/data/region_map/` (241 sections) | Greek | 1 | The Aethos map's sections, with Elaia and Akti as fly targets (`UI_world.md`). Hoenn's sections stay until their maps go. Hoenn's sections 0–85 are now free `MAPSEC_OIKOUMENE_*` slots (hoenn-cut batch 2; see `tools/ichor/claim_ranges.md`). |
| Flags and vars | `include/constants/flags.h`, `vars.h` | Keep | — | Hoenn-cut batch 2 freed 700 flags and 95 vars. The per-session ranges are in `tools/ichor/claim_ranges.md`. |
| Mart stock, tutors, in-game trades, apprentices, lottery | `data/scripts/`, map scripts | Hoenn | 2–5 | Rebuilt per Aethos location. |
| Move tutors and Frontier rewards | `data/text/move_tutors.inc`, `data/scripts/move_tutors.inc` | Hoenn | 3 | Needs Aethos tutors and, in Phase 5, Olympiad prizes. |
| Hoenn contest and Frontier data tables | `src/data/contest_*.h`, `src/data/battle_frontier/`, `data/contest_ai_scripts.s` | Cut | 5 | Counted in §10. The Frontier engine is kept; its tables are replaced by Olympiad data. |

## 10. Hoenn-only systems to cut

The first block is ART_PLAN's cut list, plus FRLG data, the PokéNav, Mirage Island, the minigames and the link and e-Reader pieces named in the brief. Each is sized as its code, text, graphics, music, SFX, maps and tilesets, from the map. The totals count only things that are in the ROM now.

| System | Where | ROM (KiB) | Status | Phase | Notes |
|---|---|---|---|---|---|
| Contests | `src/contest*.c`, `contest_ai.c`, `picture_frame`, `graphics/contest/`, `graphics/picture_frame/`, `data/contest_ai_scripts.s`, `include/config/contest.h`, `ContestHall*` maps, `gTileset_Contest`, 8 contest songs | 201.3 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_CONTESTS` in `include/config/ichor.h`). About 21 KiB stays: the summary screen still reads the contest move data and the category icons; guarding that waits for the menus restyle. |
| Berry Blender | `src/berry_blender.c`, `graphics/berry_blender/`, `data/text/blend_master.inc`, `SE_BERRY_BLENDER` | 38.5 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_CONTESTS`). |
| Pokéblocks | `src/pokeblock*.c`, `use_pokeblock.c`, `graphics/pokeblock/` | 31.3 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_CONTESTS`). The Safari Zone's feeder now places nothing. |
| Secret bases and decorations | `src/secret_base.c`, `decoration*.c`, `graphics/decorations/`, `data/tilesets/*/secret_base*`, `SecretBase_*` maps, `data/text/secret_base_trainers.inc` | 123.4 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_SECRET_BASES`). The bedroom PC's DECORATION option closes the PC. About 11 KiB stays, because the Frontier exchange corner names decorations. |
| Mirage Island and Mirage Tower | `src/mirage_tower.c`, `MirageTower_*` maps, `gTileset_MirageTower`, `Route111_NoMirageTower`, `Route130_MirageIsland` layouts, `graphics/misc/mirage_tower*` | 43.6 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_MIRAGE_TOWER`). |
| PokéNav and Match Call | `src/pokenav*.c` (14 files), `src/match_call.c`, `graphics/pokenav/` (64), `data/text/match_call.inc`, `SE_POKENAV_*` | 137.3 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_POKENAV`). |
| e-Reader and Mystery Gift | `src/mystery_gift*.c`, `mevent*.c`, `ereader*.c`, `data/multiboot_ereader.s`, `graphics/wonder_card/`, `wonder_news/`, `MysteryEventsHouse` | 61.0 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_MYSTERY_GIFT`, `ICHOR_CUT_MULTIBOOT`). The main menu's Mystery Gift entries go back to the menu. |
| Minigames: slots, roulette, Pokémon Jump, Berry Crush, Dodrio picking, lottery corner, Game Corners, Trick House | `src/slot_machine.c`, `roulette.c`, `pokemon_jump.c`, `berry_crush.c`, `dodrio_berry_picking.c`, `lottery_corner.c`, `minigame_countdown.c`, matching `graphics/` and maps | 235.3 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_MINIGAMES`). |
| Link-only features: Union Room, link trade and battle, Cable Club, record mixing, Colosseum multiboot, rfu library, Berry-fix multiboot | `src/union_room*.c`, `link*.c`, `librfu*.c`, `AgbRfu_LinkManager.c`, `cable_club.c`, `record_mixing.c`, `data/multiboot_pokemon_colosseum.s` (164 KiB), `data/multiboot_berry_glitch_fix.s` (15 KiB), `BattleColosseum_*`, `UnionRoom`, `TradeCenter`, `CableClub` maps and tilesets | 419.9 | Cut | 6 | Union Room, Cable Club, record mixing and the Colosseum and Berry-fix multiboot programs are cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_LINK`, `ICHOR_CUT_MULTIBOOT`). The RFU library and link-battle core stay, because main.c, battles and the overworld call into them. `trade.c` stays for in-game trades. |
| Hoenn Battle Frontier: maps, art, trainers, text | `BattleFrontier_*` maps (Tower, Dome, Palace, Pike, Pyramid, Arena, Factory, lounge), `BattlePyramidSquare*`, three Battle Tents, `TrainerHill_*`, twelve Frontier and Trainer Hill tilesets, `graphics/battle_frontier/`, `frontier_pass/`, `door_anims/battle_*`, `sFrontierTrainerSlides`, `data/text/battle_tent.inc` | 540.6 | Cut | 5 | Maps cut by hoenn-cut batch 3. Kept: the Battle Pyramid floor, top and squares (the Labyrinth's engine builds floors from them), the Pike rooms and the Trainer Hill floors, whose layouts the engine loads. The art the engine no longer reaches drops out of the ROM by itself (the build now uses -ffunction-sections). |
| FRLG data in the ROM | 75 FRLG songs (239 KiB), two FRLG Japanese fonts (64 KiB), 62 FRLG trainer pics (43 KiB), Kanto and Sevii region-map art, `hall_of_fame_frlg.c`, `voicegroup_frlg_*` | 365.4 | Cut | 6 | Per ART_PLAN, but FRLG maps are not in the ROM, so this is the whole ROM saving. The repo cleanup is in §9. |
| **Total, ART_PLAN's list (Frontier engine kept)** | | **2,197.7** | | | **2.15 MiB (2.25 MB)** |
| Hoenn Battle Frontier engine and data tables | `src/battle_tower.c` (`gBattleFrontierMons` 32 KiB, `gBattleFrontierTrainers` 16 KiB), `battle_dome.c`, `battle_pike.c`, `battle_pyramid.c`, `battle_arena.c`, `battle_factory*.c`, `battle_palace.c`, `battle_tent.c`, `trainer_hill.c`, `trainer_tower*.c`, `frontier_util.c`, Frontier songs | 341.2 | Keep | 5 | Keep: the Olympiad needs the facilities' rules. Replace the Hoenn trainer and Pokémon tables. Removing the engine too adds 341 KiB. |
| **Total if the Frontier engine also goes** | | **2,538.9** | | | **2.48 MiB (2.60 MB)** |

Additional Hoenn-only systems. They are **not** on ART_PLAN's list, so they are not in the totals above. I propose cutting them, and the director decides.

| System | Where | ROM (KiB) | Status | Phase | Notes |
|---|---|---|---|---|---|
| Mauville Old Man: bard, storyteller, hipster, Giddy, trader | `src/mauville_old_man.c`, `bard_music.c` (162 KiB of phoneme data), `sound/direct_sound_samples/phonemes/`, `ph_*.mid` | 283.8 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_MAUVILLE_MAN`). Not approved in the brief, but its maps were gone and the bard is an Easy Chat feature. Set the switch to 0 to restore it. |
| TV shows, Battle TV and Pokémon News | `src/tv.c`, `battle_tv.c`, `data/text/tv.inc` (2,193 string lines), `pokemon_news.inc` | 76.6 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_TV`). |
| Easy Chat and Mail | `src/easy_chat.c`, `data/text/`, `graphics/easy_chat/`, `graphics/mail/`, 12 mail items | 59.1 | Keep | 6 | Kept for now ("where safe"): mail items and the Frontier still use them. 45 KiB. |
| Safari Zone | `src/safari_zone.c`, `battle_controller_safari.c`, `healthbox_safari.png`, Safari maps | 40.9 | Cut | 6 | |
| Cable car and SS Tidal and ferries | `src/cable_car.c`, `ss_anne.c`, `seagallop.c`, graphics | 44.9 | Cut | 6 | Triremes replace ferries. |
| Apprentice, Lilycove Lady, wall-clock set screen, mass outbreaks | `src/apprentice.c`, `lilycove_lady.c`, `wallclock.c`, `mass_outbreak.c` | 68.2 | Cut | 6 | The Lilycove Lady is counted under Contests, not here. The wall clock stays: `wallclock.c` now runs the klepsydra (§5). |
| Hoenn gym puzzle mechanics | `src/rotating_gate.c` | 16.0 | Cut | 6 | Fortree Gym and Trick House 6 only. |
| **Subtotal of the proposals** | | **about 590** | | | **0.58 MiB** |
| Hoenn legendary set pieces | `src/rayquaza_scene.c`, `graphics/rayquaza_scene/` (25), Regi puzzle and Braille, Deoxys rock, weather-trio songs, Cave of Origin and Sealed Chamber songs | 335.6 | Hoenn | 5 | Not a cut. PITCH §6.6 reuses Groudon, Kyogre and Rayquaza as the Primordials (Gaia, Oceanus, Ouranos), so re-theme their scenes. |

**Where the ROM goes** (26,878,048 bytes used; the rest of the 33,554,432-byte limit is 6,676,384 bytes, or 6.37 MiB, free):

| Block | ROM | Share | What it means |
|---|---|---|---|
| Pokémon cries | 9.37 MB | 34.9 % | About 1,160 samples, 8 KiB each. Cuts depend on the dex. |
| Pokémon species data and art | 5.87 MB | 21.8 % | 1,571 entries, about 3.7 KiB each. |
| Hoenn map scripts, layouts and text | 1.07 MB | 4.0 % | Frees as Aethos maps replace Hoenn. The cut systems' maps are in their own rows. |
| Instruments, voicegroups, tables | 0.85 MB | 3.2 % | Shared engine. |
| Battle animations (art and scripts) | 0.80 MB | 3.0 % | Kept. |
| Overworld object graphics | 0.63 MB | 2.4 % | People, objects and field sprites. Mostly Hoenn and FRLG sheets, retired with the maps. |
| Tilesets (Hoenn 428 KiB, Greek 73 KiB) and animations (118 KiB) | 0.63 MB | 2.3 % | |
| Fonts | 0.37 MB | 1.4 % | Plus 64 KiB of FRLG fonts in the FRLG cut. Includes about 75 KiB of Japanese glyph tables (§11). |
| Hoenn music not on a cut list | 0.30 MB | 1.1 % | Replace as Ichor songs arrive. |
| Everything on ART_PLAN's cut list | 2.25 MB | 8.4 % | The first total above. |
| Engine code, other UI, text, the Frontier engine, the proposed cuts and the rest | about 4.7 MB | 17.5 % | |

The cuts matter less than the dex. The Hoenn-only systems on ART_PLAN's list free about 2.2 MB. The cries and species art together are 15 MB, so how many existing species stay decides the ROM budget far more than any system cut does.

## 11. Possibly overlooked

A total conversion tends to miss these. Each is checked in the repo.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Game Freak copyright and logo | `graphics/intro/copyright.png`, `graphics/intro/scene_1/`, `graphics/credits/the_end_copyright.png`, `src/strings.c:906` (diploma "GAME FREAK"), `graphics/intro/` | Greek | 1 | The copyright card credits Pokémon's makers and calls Ichor a fan-made game; the Game Freak logo is gone (`INTRO.md`). The diploma is signed PROF. DAPHNE. The credits' "the end" copyright waits with the credits. |
| Credits roll | `src/data/credits.h` (57 pages of Game Freak staff), `src/credits.c`, `graphics/credits/` | Hoenn | 4 | Needs Ichor's own credits plus upstream attribution (pokeemerald, expansion, tools, fonts, music sources). |
| ROM header title and game code | `Makefile` (`TITLE ?= POKEMONICHOR`, `GAME_CODE ?= BPEE`, `MAKER_CODE := 01`), `src/rom_header_gf.c:102` (`"pokemon emerald version"`), `src/rom_header_rhh.c` | Greek | 1 | The cartridge title is POKEMONICHOR (`Makefile`). The game code stays `BPEE`, because emulators pick the save type from it. The GF header's internal name in `src/rom_header_gf.c` still reads "pokemon emerald version"; only link and save tools read it. |
| Default player and rival names | `src/main_menu.c:481,485` ("THEO", "IANTHE") | Greek | 1 | Done. The rival is Kleon by script, and there is no rival-naming step (`sText_RivalsName` is used only by the FRLG Oak speech). Check the in-game-trade nicknames, egg OT strings and the debug menu's Brendan and May follower entries. |
| Save-error and corruption screens | `src/main_menu.c:259-262`, `src/strings.c:568` | Keep | 6 | Plain text. Only the "POKéMON" word and the menu frame show. Worth a proofread. |
| Clock reset screen | `src/reset_rtc_screen.c`, `graphics/reset_rtc_screen/` | Keep | 6 | Generic. "The internal battery has run dry". |
| Battle-message wording | `src/battle_message.c` | Greek | 1 | Swept: no line the game can reach says FOE, ELITE FOUR, CHAMPION, LEADER, Birch or Wally. The Battle Arena referee's three lines go with the Frontier. Trainer-class openers are generic. |
| `{PKMN}` glyph and the "POKé" glyphs | `charmap.txt:55` (`PKMN`), `graphics/fonts/latin_*.png` | Keep | Director | The font draws "PK" and "MN" as small caps in 2 tiles. The party menu no longer prints them (QA P3); Frontier and link text still does. Fine if the game keeps "Pokémon". Record the decision (§7). |
| The font | `graphics/fonts/` (23 files), `src/fonts.c` (422 KiB) | Keep | Director | Gen 3's six Latin variants plus 5 Japanese ones. Greek letters appear on the title as paint, not as glyphs. A Greek-style font is optional. |
| Japanese font tables | `src/fonts.c` (`gFont*Japanese*`), `src/text.c` (`sFontBoldJapaneseGlyphs`), `graphics/fonts/japanese_*.png` | Cut | 6 | About 75 KiB beyond FRLG's 64 KiB (counted in §10). An English-only build can drop them, but it needs careful engine work. Not in any total. |
| Ribbons | `src/pokemon_summary_screen.c` (ribbon count on the skills page), `graphics/pokenav/ribbons/`, `src/data/` ribbon names | Hoenn | 4 | The summary's skills page shows a RIBBON box. Champion, Cool, Beauty, Winning, Effort, Marine and so on. Re-theme as Laurels or cut with contests. |
| Summary "Trainer memo" and "Met at" lines | `src/pokemon_summary_screen.c`, `src/strings.c` | Greek | 1 | "Calm nature, met at Lv5, ELAIA VILLAGE." Hoenn places only show for Hoenn's maps. |
| Move-tutor, PC and trade-scene text | `data/text/move_tutors.inc`, `data/text/pc.inc`, `data/text/ingame_trade_frlg.inc` | Hoenn | 2 | The Pithos strings are Ichor's (§7). Tutor and trade text are not. |
| Pocket names | `src/strings.c:145` ("POKé BALLS" and others) | Keep | — | ITEMS, POKé BALLS, TMs & HMs, BERRIES and KEY ITEMS, on the satchel's parchment label. TERMS.md keeps Poké Ball and TM. |
| Pokémon type names and move names | `src/data/types_info.h`, `src/data/moves_info.h` | Keep | — | Generic. |
| Pokémon Center and Mart words in the follower messages | `src/follower_helper.c:26,132-140` | Greek | 1 | The follower's lines say "Your Pokémon", look up at Mount Olympus, and notice the Agora's shelves (`UI_remnants.md`). |
| Dev tools | `src/debug.c` (28 KiB), `graphics/quickstart/`, `include/config/quickstart.h`, `include/config/debug.h` | Keep | 6 | Disable for the release patch. Quickstart is off in release builds, and its title badge is hidden (`QUICKSTART_HUD`). |
| Hoenn flags and vars in names | `include/constants/flags.h`, `vars.h` | Keep | — | Internal names only. |
| Unused graphics | `graphics/unused/` (11 PNGs: old battle UI, a Bulbasaur and a Charizard) | Keep | 6 | Not built into the ROM. Delete when tidying. |
| Pokémon Center jingle at the heal tray, the Pokémon Center fainting sequence | `graphics/field_effects/`, `MUS_HEAL` | Greek | 1 | `MUS_HEAL` plays `mus_ichor_heal` over the Asclepeion's spring (§1, §8). |
| The brand "Pokémon Ichor" on the title | `graphics/title_screen/` | Greek | 1 | Done. |
