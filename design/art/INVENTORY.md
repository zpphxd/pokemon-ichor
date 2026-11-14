# Ichor art inventory

The checklist that makes the total conversion true: every player-facing asset group and system in the ROM, with its status. It is the "inventory" that `design/ART_PLAN.md` §6 promises. Nothing should stay Hoenn by accident.

- **Measured against:** `main` at `c82f1634f7`, with a clean `make` (devkitARM 16.1, Emerald build).
- **Sizes** come from the linker map, `pokeemerald.map`, and `nm -S` on `pokeemerald.elf`. Unsized assembly labels are sized by the gap to the next symbol. KiB means 1024 bytes. Sizes are good to a few percent, and the groupings are by symbol name and source file.
- **Update rule:** when a batch merges, flip its rows from **In progress (batch)** to **Greek** and fix the counts in the summary.

## Legend

| Status | Meaning |
|---|---|
| **Greek** | Redrawn, rewritten or recomposed for Aethos, and in the repo. |
| **In progress (batch)** | A batch running in parallel owns it: the Kalliste maps and scripts, the 22 townsfolk walkers, music batch 2, the battle interface (healthboxes, battle text box, transitions), or the menus (bag, party, summary, shop, map popups). |
| **Hoenn** | Still Emerald's. It must be replaced or rewritten. |
| **Cut** | A Hoenn-only system or asset to remove, with no replacement. Systems on ART_PLAN's cut list are marked "per ART_PLAN"; the rest are flagged for the director. |
| **Keep** | Generic, and fine as it is (the battle animations, move SFX and so on). |
| **New** | Nothing exists in the ROM yet and nothing Hoenn is in its place. It has to be built (relics, the Scroll of Deeds, the Aethos cast). This sixth status is not in the brief; it stops "not started" from being counted as "Hoenn". |

**Phase** is the roadmap phase in `design/PITCH.md` §8: **1** is the Kalliste slice, **2** Act I (Emporion, Eleusa), **3** Act II (Thyrsa, Arkadia, Astyra, Kaldera), **4** Act III through the Pantheon (1.0), **5** post-game, and **6** the polish sweep. **Batch** means a running batch owns the row. **Dex** means it waits for `design/dex/`. **Director** means it needs a decision.

## Summary

**224 rows** across 11 areas. Counts by status (a row is an asset group or system, so these are not file counts):

| Status | Rows |
|---|---|
| Greek | 21 |
| In progress (batch) | 15 |
| Hoenn | 91 |
| Cut | 48 |
| Keep | 31 |
| New | 18 |

| Area | Greek | In progress | Hoenn | Cut | Keep | New | Rows |
|---|---|---|---|---|---|---|---|
| 1. Overworld | 5 | 1 | 11 | 4 | 3 | 3 | 27 |
| 2. People | 8 | 1 | 6 | 5 | 0 | 5 | 25 |
| 3. Pokémon | 0 | 0 | 1 | 0 | 5 | 3 | 9 |
| 4. Battles | 1 | 3 | 2 | 2 | 5 | 1 | 14 |
| 5. Screens | 3 | 5 | 23 | 3 | 2 | 3 | 39 |
| 6. Items | 0 | 0 | 8 | 5 | 1 | 3 | 17 |
| 7. Text | 0 | 3 | 15 | 1 | 1 | 0 | 20 |
| 8. Audio | 1 | 1 | 11 | 4 | 3 | 0 | 20 |
| 9. Data | 1 | 1 | 3 | 5 | 2 | 0 | 12 |
| 10. Cuts | 0 | 0 | 1 | 18 | 1 | 0 | 20 |
| 11. Overlooked | 2 | 0 | 10 | 1 | 8 | 0 | 21 |

Greek is mostly the tilesets, the title screen, the dialogue frames, Theo and Ianthe, the cast portraits and walkers, the grass, sand, water and temple battle backgrounds, and 10 songs. None of the Greek tilesets is attached to a map yet (0 of 790 layouts).

**ROM now:** 26,878,048 bytes of the 33,554,432-byte limit (80.10 %, from `make`). That leaves 6,676,384 bytes (6.37 MiB) free.

**ROM the cuts would free:**
- **ART_PLAN's list, with the Hoenn Frontier engine kept: 2.15 MiB (2,250,486 bytes).** That is contests, the Berry Blender, Pokéblocks, secret bases, Mirage Island, the PokéNav, e-Reader and Mystery Gift, the minigames, the link-only features, the Frontier maps and art, and FRLG data.
- **2.48 MiB (2,599,873 bytes) if the Frontier engine goes too.** The Olympiad needs it, so I recommend keeping it.
- **About 0.58 MiB more** if the director also approves the proposed cuts that are not on ART_PLAN's list (Mauville Old Man, TV, Easy Chat and mail, Safari Zone, transport, Apprentice, gym puzzles).
- **The cuts are small next to the dex.** Pokémon cries (9.4 MB) and species art and data (5.9 MB) are 57 % of the ROM. FRLG maps and tilesets are not built into the Emerald ROM at all, so cutting FRLG frees only 365 KiB.

**The ten highest-impact Hoenn items still visible in the slice**, ranked by how much a player would notice. The running batches (the Kalliste maps and their tilesets, the townsfolk, music batch 2, the battle interface and the menus) are left out; without them Hoenn tilesets would top the list. Existing species art is left out because it waits on the dex.

| # | What the player sees | Where | Rows |
|---|---|---|---|
| 1 | **The boot sequence.** The Nintendo, Creatures and Game Freak copyright, the "powered by" card, the Game Freak logo, Latios, Latias and Flygon, Brendan and May on bikes, the legendary trio, then Emerald's intro and title music under the Greek title screen. | `src/intro.c`, `graphics/intro/`, `MUS_INTRO`, `MUS_TITLE` | §5, §8, §11 |
| 2 | **The new-game speech.** Daphne's portrait says "My name is BIRCH" and "LITTLEROOT", a Lotad leaves a ball, the room is Hoenn's, and the Route 122 theme plays. | `data/text/birch_speech.inc`, `src/main_menu.c`, `graphics/birch_speech/` | §5, §7, §8 |
| 3 | **Field effects.** The tall-grass rustle on Route 1, footprints on Akti's beach, and ripples, splashes and ash. They are on screen constantly and are Hoenn's sprites. | `graphics/field_effects/pics/` | §1 |
| 4 | **Door animations.** Every house, the Asclepeion and the Agora play a recolored Hoenn door. | `graphics/door_anims/`, `src/field_door.c` | §1 |
| 5 | **Item icons, names and item balls.** Every bag and pickup icon is Emerald's, and Route 1's pickups are Poké Balls on the ground. | `graphics/items/icons/`, `graphics/object_events/pics/misc/ball_*.png` | §1, §6 |
| 6 | **The Pokédex and the map.** Daphne hands over a "HOENN DEX" on Hoenn's dex UI, and the Kalliste towns sit on the Hoenn region map. | `graphics/pokedex/`, `src/pokedex.c`, `src/data/region_map/` | §5, §7 |
| 7 | **The starter selection screen.** Birch's bag in the grass, with three Poké Balls. Ruling 11 keeps it for the slice. | `graphics/starter_choose/` | §5 |
| 8 | **The Asclepeion heal animation.** The Poké Ball tray and monitor play whenever the player heals. The nurse's text is in a batch; the animation is not. | `graphics/field_effects/pics/pokecenter_monitor.png`, `pokeball_glow.png` | §1 |
| 9 | **The water-clock scene.** The first task in the player's room opens Emerald's wall-clock screen. | `graphics/wallclock/`, `src/wallclock.c` | §5 |
| 10 | **Hoenn words in system text.** The whiteout line "scurried to a POKéMON CENTER", the "PROF. BIRCH" rescue lines, "BADGES" on the Continue panel, trainer-class names such as "LEADER", and the Hoenn-style trainer card. | `src/field_screen_effect.c`, `src/main_menu.c`, `src/trainer_card.c`, `src/battle_main.c` | §5, §7 |

---

## 1. Overworld

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Outdoor primary tileset `aethos` | `data/tilesets/primary/aethos/`, `porytiles/tilesets/gTileset_Aethos/`, `tools/ichor/art/aethos_*.py`, `design/phase1/TILES_aethos.md` | Greek | 1 | Replaces `general`: olives, cypress, limestone, Aegean, Asclepeion and Agora exteriors. Checked in renders only. No layout uses it yet (0 of 790). 18 free tile slots. |
| Interior primary tileset `oikos` | `data/tilesets/primary/oikos/`, `design/phase1/TILES_oikos.md` | Greek | 1 | Replaces `building`: terracotta floors, klinai, amphorae. The TV becomes Mom's loom and the PC becomes the Pithos. Not attached to any map yet. |
| Secondary tilesets `kalliste`, `temple_hestia` | `data/tilesets/secondary/kalliste/`, `.../temple_hestia/`, `design/phase1/TILES_kalliste.md`, `TILES_temple.md` | Greek | 1 | Cycladic village, harbor, Kronion ruins and the Hestia temple interior. |
| Secondary tilesets `oikia`, `civic` | `data/tilesets/secondary/oikia/`, `.../civic/`, `design/phase1/TILES_oikia.md`, `TILES_civic.md` | Greek | 1 | Houses, the Asclepeion, the Agora and the Akademia. 48 civic tile slots are left. |
| Wiring the Greek tilesets into the slice maps | `data/layouts/layouts.json`, `data/maps/ElaiaVillage*`, `KallisteRoute1*`, `AktiTown*` | In progress (batch) | 1 | All 12 Kalliste maps still point at `General`, `Petalburg`, `Building`, `BrendansMaysHouse`, `Lab`, `PokemonCenter`, `Shop`, `GenericBuilding` and `RustboroGym`. |
| Biome secondary tilesets to come | New `data/tilesets/secondary/*` | New | 2–5 | About 15: Astyra, Thyrsa vineyards and theater, Eleusa wheat and Mystery sanctum, Arkadia cypress forest, Kaldera caldera, Kythera coves, Knossa Labyrinth, Lakonia, Delphoi, Olympus, Underworld and Elysium, Atlantis (ART_PLAN §1). |
| Temple interiors for Hermes through Zeus, trireme decks, the Pithos room | New secondaries | New | 2–5 | The Hestia interior is the pattern. Table of orders and materials: ART_PLAN §1. |
| Hoenn secondary tilesets | `data/tilesets/secondary/*` (67 Hoenn folders, plus 62 FRLG folders that are not built) | Hoenn | 2–5 | Retired biome by biome as the Aethos maps replace Hoenn's. The Hoenn tilesets total about 428 KiB in the ROM. Frontier, Secret Base, Mirage Tower, Contest and Cable Club tilesets go with their systems (§10). |
| Hoenn primaries `general`, `building`, `secret_base` | `data/tilesets/primary/` | Hoenn | 2–5 | `aethos` and `oikos` replace the first two once every layout moves. `secret_base` is cut. `building_frlg` and `general_frlg` are not built. |
| Aethos tile animations | `include/porytiles_generated/tilesets/aethos/`, `src/tileset_anims.c` | Greek | 1 | Water, surf, waterfalls and anemones, at General's slots. |
| Hoenn tile animations | `src/tileset_anims.c` (25 `InitTilesetAnim_*` for Hoenn tilesets), `data/tilesets/secondary/*/anim/` | Hoenn | 2–5 | Dewford, Slateport, Mauville, Lavaridge steam, Pacifidlog bridges, Sootopolis, Underwater, Cave and the rest. About 116 KiB. |
| Door animations | `graphics/door_anims/` (85 sheets), `src/field_door.c` (25 KiB) | Hoenn | 1 | `general`, `poke_center` and `poke_mart` still play over the aethos doors at `021`, `061` and `041`. They show a recolored Hoenn door. Redraw for the farmhouse, Asclepeion and Agora, then the temples. Kalliste's and civic's own doors are non-animated. |
| Terrain contact effects | `graphics/field_effects/pics/`: `short_grass`, `tall_grass`, `long_grass`, `jump_*`, `cut_grass`, `sand_footprints`, `deep_sand_footprints`, `ripple`, `splash`, `water_surfacing`, `bubbles`, `ash*`, `bike_tire_tracks` and others | Hoenn | 1 | Route 1 has tall grass and Akti has sand and water. The aethos tall-grass tile is barley, but the rustle sprite that plays over it is still Hoenn's grass. Greek: barley stalks, sand and olive-leaf puffs. `bike_tire_tracks` is cut with bikes. Colors are palette-driven, so a recolor is a first pass. |
| Shadows, emotes and sparkles | `graphics/field_effects/pics/shadow_*`, `emotion_*`, `emote_x`, `sparkle`, `shiny_sparkle`, `small_sparkle` | Keep | 6 | Generic shapes. The "!" and "?" emotes share the player palette (`may.pal` indices 14–15), so they are already recolored. |
| Weather | `graphics/weather/` (9 files plus `drought*`), `src/field_weather*.c` | Keep | 6 | Rain, snow, fog, ash, sandstorm, drought, bubbles and clouds are generic. The Frozen Hour palette drain is an engine job. `sDroughtWeatherColors` is 49 KiB. |
| Asclepeion healing machine and monitor | `graphics/field_effects/pics/pokecenter_monitor.png`, `pokeball_glow.png`, `src/field_effect.c` | Hoenn | 1 | The heal animation shows a Poké Ball tray and a monitor. Greek: a snake-staff altar and a flame bowl, or a spring basin. Nurse text is a separate row (§7). |
| Mart and Asclepeion light sprites | `graphics/object_events/pics/misc/poke_center_light.png`, `mart_light.png`, `light.png` | Hoenn | 1 | Window lights outside the doors. Greek: oil lamps. |
| Berry trees | `graphics/object_events/pics/berry_trees/` (47 sheets), `graphics/berries/` (67 pics), `src/berry.c` | Hoenn | 2 | The bible says nothing about berries, and the slice already gifts an Oran Berry and a Sitrus Berry. Proposal: keep the system and restyle the trees and fruit as Greek fruit and herbs. Needs a director decision. |
| Cut, Rock Smash and Strength objects | `graphics/object_events/pics/misc/cuttable_tree.png`, `breakable_rock.png`, `pushable_boulder.png` | Hoenn | 2 | Field powers become relics (Labrys, Bronze Hammer, Girdle of Herakles). Greek: a thorn thicket or olive sapling, a marble rubble pile, a column drum. |
| Signs, statues and props | `graphics/object_events/pics/misc/sign.png`, `wooden_sign.png`, `gym_sign.png`, `statue.png`, `clipboard.png`, `birchs_bag.png`, `moving_box.png`, `town_map.png`, `pokedex.png`, `fossil*.png`, `old_amber.png`, `truck.png` | Hoenn | 1 | The slice needs signs and the gym sign (a temple stele) first. `birchs_bag` and `truck` belong to Hoenn's opening and can go. The `sign` text frame is already Greek (`graphics/text_window/signpost.png`). |
| Item-ball pickups on the ground | `graphics/object_events/pics/misc/ball_*.png` (28) | Hoenn | 1 | Route 1 has item pickups and they show as Poké Balls. Greek: a votive bundle, a clay lamp or a small amphora. One sheet per type, or one shared sheet. |
| Event Pokémon sprites | `graphics/object_events/pics/pokemon_old/` (63) | Keep | Dex | Static overworld Pokémon (Azumarill, Kyogre and so on). Followers make most of them redundant. |
| Trireme and sailing sequence | `graphics/object_events/pics/misc/ss_tidal.png`, `graphics/ss_anne/` (wake, smoke), `src/ss_anne.c`, `src/seagallop.c` | New | 1–2 | The slice ends at the trireme in Akti's harbor. The bible replaces ferries with triremes. The kalliste harbor kit already has the quay and moored boats. The moving trireme sprite and the crossing scene need art. |
| Cable car | `graphics/cable_car/` (4), `src/cable_car.c` | Cut | 6 | Mt. Chimney only. Proposed in §10. |
| SS Tidal and ferries | `graphics/seagallop/`, `graphics/ss_anne/`, `mr_briney_boat.png`, `ss_tidal.png` | Cut | 6 | Replaced by triremes. Proposed in §10. |
| Secret-base decorations | `graphics/object_events/pics/dolls/` (41), `cushions/` (10), `graphics/decorations/` (43) | Cut | 6 | Per ART_PLAN (§10). |
| Hoenn gym puzzle mechanics | `src/rotating_gate.c` (16 KiB), Fortree and Mossdeep gym tiles and scripts | Cut | 6 | Used by Fortree Gym and Trick House 6 only. The Hearth trial is Ichor's own puzzle. Proposed in §10. |

## 2. People

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Theo and Ianthe: walking, running (Talaria wings), fishing (Old Rod), field-move (relic raise) | `graphics/object_events/pics/people/brendan/`, `.../may/`, `tools/ichor/art/sprites_player_ow.py`, `design/phase1/SPRITES_player_ow.md` | Greek | 1 | 4 of the 10 sheets each. The folders keep Brendan's and May's names and palettes (`brendan.pal`, `may.pal`), which also color the rival and link-player sprites. |
| Theo and Ianthe: surfing | `.../brendan/surfing.png`, `.../may/surfing.png` | Hoenn | 2 | A dolphin-back or a small boat (ART_PLAN §2). Needs Poseidon's Conch. The surf blob field effect goes with it. |
| Theo and Ianthe: underwater (Dive) | `.../underwater.png` | Hoenn | 5 | Atlantis and the Nereid Pearl. |
| Mach Bike and Acro Bike | `.../mach_bike.png`, `.../acro_bike.png`, `graphics/field_effects/pics/bike_tire_tracks.png`, `bike_shop` tileset | Cut | 6 | `SPRITES_player_ow.md` says Aethos has no bikes. The bible does not list a bike. Needs a director decision, including the three bike key items and the `bike_shop` maps. |
| Watering and decorating poses | `.../watering.png`, `.../decorating.png` | Cut | 6 | `SPRITES_player_ow.md`: no watering cans or secret bases. Tied to the berry decision (§1) for watering. |
| Ruby/Sapphire and FRLG player sheets | `.../people/ruby_sapphire_brendan/`, `ruby_sapphire_may/`, `rs_brendan.png`, `rs_may.png`, `leaf/`, `red/` | Cut | 6 | Never used by Aethos. |
| Player battle back pics | `graphics/trainers/back_pics/brendan.png`, `may.png`, `graphics/trainers/palettes/brendan.pal`, `may.pal`, `design/phase1/SPRITES_player.md` | Greek | 1 | Theo and Ianthe with throw animation. |
| Player front pics | `graphics/trainers/front_pics/brendan.png`, `may.png` | Greek | 1 | The boy-or-girl choice, the trainer card and the Birch speech use them. Ianthe's side of the choice was not captured in-game. |
| Other back pics | `graphics/trainers/back_pics/`: `brendan_rs`, `may_rs`, `red`, `leaf`, `steven`, `wally`, `old_man`, `pokedude`, `none` | Hoenn | 6 | 9 of 11 files are Hoenn, Kanto or tutorial characters. About 70 KiB of the 86 KiB of back pics. `wally` and `old_man` serve the catch tutorials. |
| Daphne, Alethea, Kleon, Ione, Titan grunt overworld sprites | `graphics/object_events/pics/people/ichor/`, `design/phase1/SPRITES_npc.md` | Greek | 1 | Shared palette `ichor_cast.pal`. |
| Kleon, Ione, Titan grunt, Daphne portraits | `graphics/trainers/front_pics/kleon.png`, `hierophant_ione.png`, `titan_grunt.png`, `professor_daphne.png`, `design/phase1/SPRITES.md` | Greek | 1 | Polish pass 1 done. Still open: 3/4 turns, more folds, Kleon's swagger pose, Ione unchanged. |
| Daphne in the new-game speech | `graphics/birch_speech/birch.png` | Greek | 1 | Same file as Birch's, so no code change. The speech text, the Lotad and the background are not (§5, §7). |
| Alethea portrait and back pic | none | New | 3 | She fights beside you in Act II's double battle. |
| The Twelve's Hierophants (2–8), the four Pantheon seats and the Archon | New `front_pics/`, `people/` | New | 2–5 | Ione is done. Names are in PITCH §3. |
| Team Titan admins (Hyperion, Iapetos, Rhea), Kronos and Phaedon, Elpis, Kallisto's hunt, the Fates | New | New | 3–4 | Phaedon is the healer behind the mask: his walker and portrait must read as the same man. |
| Townsfolk walkers (22) | `include/constants/event_objects.h:444-465` (aliases `OBJ_EVENT_GFX_ICHOR_*`), `graphics/object_events/pics/people/` | In progress (batch) | 1 | Mom, priestess, two youths, man, woman, two elders, two kids, fisher, sailor, diver, healer, merchant, shepherd, harvester, goatherd, hoplite, augur and two acolytes. Aliases of Hoenn sheets until the batch lands. |
| More civilians to reach about 40 types | New `people/` | New | 2–5 | Potters, philosophers, olive farmers, oracles, athletes and so on (ART_PLAN §2). |
| Hoenn and FRLG NPC walker sheets | `graphics/object_events/pics/people/*.png` (about 230 sheets including subfolders), 393 `OBJ_EVENT_GFX_*` ids | Hoenn | 2–5 | Retired as the Hoenn maps go. Keep the sheets of generic types (the shared poses) as palette bases only if useful. |
| Hoenn story characters and teams | `.../people/team_aqua/`, `team_magma/`, `gym_leaders/`, `elite_four/`, `frontier_brains/`, `steven.png`, `wally.png`, `wallace.png`, `prof_birch.png`, `scott.png` and similar | Cut | 6 | No counterpart in Aethos. Team Titan, the Hierophants and the Pantheon replace them. |
| Aethos trainer classes | `include/constants/trainers.h` (Lakonian, Shepherd, Harvester, Goatherd, Hoplite, Augur, Titanborn, Acolyte, Hierophant), `src/battle_main.c` `gTrainerClasses` | Greek | 1 | 9 classes. The bible wants about 25. |
| Aethos trainer-class portraits | `graphics/trainers/front_pics/shepherd.png`, `harvester.png`, `goatherd.png`, `hoplite.png`, `augur.png`, `acolyte_m.png`, `acolyte_f.png`, `design/phase1/SPRITES_classes.md` | Greek | 1 | 7 class portraits, plus the 4 cast portraits above, make 11 new pic ids. Front pics only. |
| Remaining Aethos classes and portraits (about 16) | New | New | 2–5 | Fisher, sailor, potter, hunter, philosopher, athlete, oracle, bronzesmith and the rest, as each biome needs them. |
| Hoenn trainer classes and pics | `include/constants/trainers.h` (66 Hoenn classes, 2 unused), `graphics/trainers/front_pics/`, `src/data/graphics/trainers.h` | Hoenn | 2–5 | 66 classes and 85 pic ids (83 untouched; Brendan and May were redrawn as Theo and Ianthe). All 158 front pics together are about 105 KiB. Aqua, Magma, Frontier, Contest and Battle Girl classes go with their systems. Suggested replacements from the nine class designs (the bible does not assign them): Hierophant for Leader, Titanborn for Aqua and Magma, Lakonian for Rival, Hoplite for Black Belt and Battle Girl, Augur for Psychic, Hex Maniac and Expert, Shepherd for Camper, Bug Catcher and Youngster, Harvester for Picnicker, Lass and Aroma Lady, Goatherd for Hiker and Ruin Maniac, Acolyte for the temple-room trainers. |
| FRLG trainer classes and pics | `include/constants/trainers.h` (50 `_FRLG` classes), `graphics/trainers/front_pics/*_frlg.png` (62), `back_pics/` | Cut | 6 | FRLG data is not otherwise built, but 62 pics are about 43 KiB of ROM. Per ART_PLAN. |
| Trainer-sighting music table | `src/data/trainer_approach_music.h` | Hoenn | 1 | Maps trainer classes to the 17 Hoenn "I see you" jingles (§8). The Ichor classes need Greek-mode jingles and entries here. |

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
| Hoenn dex mode and Hoenn dex ordering | `src/pokedex.c` (`DEX_MODE_HOENN`, "HOENN DEX"), `src/data/` order tables | Hoenn | 1 | Replace with the Aethos regional dex. See §5. |
| Fusion, Dynamax and Tera forms and art | species info, `graphics/battle_interface/*_indicator.png` | Keep | Dex | The bible turns Z-Moves, Dynamax and Tera off. Their art costs ROM but is harmless. |
| Apotheosis (Mega Evolution) trigger and Ichor Stones | `graphics/battle_interface/mega_trigger.png`, `mega_indicator.png`, 92 Mega Stone items | New | 4 | See §4 and §6. All classic and Z-A Megas are in the species data. |

## 4. Battles

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Greek battle backgrounds: grass, sand, water, building (also gym, leader, plain, frontier) | `graphics/battle_environment/{tall_grass,sand,water,building,plain}/`, `src/data/battle_environment.h`, `design/phase1/BATTLE_BG.md` | Greek | 1 | 8 environments: the olive grove, Akti's shore, the open Aegean and the Doric temple hall with its leader, gym and plain variants. `KYOGRE` uses the water tiles in a storm palette. |
| Other Greek backgrounds still needed | `graphics/battle_environment/{cave,rock,long_grass,pond_water,underwater}/` | Hoenn | 2–5 | Cave, mountain, long grass, pond and underwater are still Emerald's. Needs: cypress forest, caldera, Labyrinth, Underworld, Atlantis, Olympus. |
| Elite Four, Champion and Pantheon halls | `graphics/battle_environment/stadium/`, `sky/`, `src/data/battle_environment.h` (Sidney, Phoebe, Glacia, Drake, Champion) | Hoenn | 4 | The Pantheon needs five Olympus halls. |
| Team Aqua, Team Magma, Groudon, Kyogre and Rayquaza backgrounds | same | Cut | 6 | No Aethos equivalent. The Primordials may need one scene each in Phase 5. |
| Expansion extra backgrounds (puddle, marsh, swamp, snow, ice, volcano, space and so on) | `src/data/battle_environment.h` | Keep | 6 | They reuse base tiles. |
| Healthboxes, HP and EXP bars, status and ball indicators | `graphics/battle_interface/` (71 files), `src/battle_interface.c` | In progress (batch) | Batch | The pottery interface. The type indicators beside the healthbox are generic (Keep). |
| Battle text box and action and move menus | `graphics/battle_interface/textbox*`, `move_info_window_*`, `src/battle_message.c` | In progress (batch) | Batch | Wording is a separate row (§7). |
| Battle transitions | `graphics/battle_transitions/` (23 files), `src/battle_transition.c`, `src/battle_transition_frontier.c` | In progress (batch) | Batch | Black-figure silhouettes. Aqua, Magma, Regi, Kyogre, Groudon, Rayquaza, the Elite Four mugshots and the Frontier logo are Hoenn art and should be dropped. |
| Poké Ball sprites and capture sequence | `graphics/balls/` (29), `src/pokeball.c` | Keep | Director | 28 balls in the bag. The bible is silent on balls. ART_PLAN says "ball cases and so on". Decide whether to rename and restyle them (a clay sphaira) or keep the Poké Ball look. |
| Throw, shake, open and move animations | `graphics/battle_anims/` (476 files), `data/battle_anim_scripts.s` | Keep | — | ART_PLAN keeps these. About 306 KiB of art plus 243 KiB of scripts. |
| Type and status icons | `graphics/types/` (28), `graphics/interface/status_icons.png`, `src/data/types_info.h` | Keep | 6 | Generic. Contest category icons in `graphics/types/` go with contests. |
| Mid-battle trainer slide tables | `src/trainer_slide.c` (`sTrainerSlides` 275 KiB, `sFrontierTrainerSlides` 94 KiB) | Keep | 6 | A feature to keep, but both tables are empty arrays sized by trainer count × 3 difficulties. About 369 KiB of ROM is zeros. 94 KiB is counted in the Frontier row (§10); the other 275 KiB is in no cut total. It shrinks when the Hoenn trainer ids go. |
| Frontier battle UI (Dome tourney tree, Factory, Arena, Palace and so on) | `src/battle_dome.c`, `battle_factory_screen.c`, `battle_arena.c`, `battle_palace.c`, `graphics/battle_frontier/` | Cut | 5 | Per ART_PLAN, except the engine that the Olympiad reuses (§10). |
| Apotheosis trigger button and flash | `graphics/battle_interface/mega_trigger.png` | New | 4 | The one battle gimmick (PITCH §5). |

## 5. Screens

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Boot copyright screen | `graphics/intro/copyright.png`, `copyright.bin`, `src/intro.c` | Hoenn | 1 | Shows the Nintendo, Creatures and Game Freak lines. See §11. |
| Expansion "powered by" credit | `graphics/expansion_intro/`, `src/expansion_intro.c`, `EXPANSION_INTRO` in `include/config/general.h` | Keep | Director | Plays after the copyright screen. Keep as upstream attribution or move it to the credits. |
| Game Freak logo and drops | `graphics/intro/scene_1/` (`drops_logo.png`, `logo.pal`, `sparkle.png`), `src/intro.c` | Hoenn | 1 | ART_PLAN §5 replaces the intro with Daphne. |
| Latios, Latias, Flygon, Brendan and May intro | `graphics/intro/scene_2/` (bicycle, houses, `latias.png`, `latios.png`, `flygon.png`, `manectric.png`, `volbeat.png`) | Hoenn | 1 | Hoenn scenery and bikes. The bible maps Latias and Latios to the Dioskouroi twins (PITCH §4), so their art can return in a Greek scene later. |
| Legendary trio sequence | `graphics/intro/scene_3/`, `src/intro.c` | Hoenn | 1 | Groudon, Kyogre and Rayquaza. |
| Title screen: the Fates amphora | `graphics/title_screen/`, `src/title_screen.c`, `tools/ichor/art/title_screen.py`, `design/phase1/TITLE.md` | Greek | 1 | The music is still Emerald's `MUS_TITLE` (§8). |
| Main menu (New Game, Continue, Options) and Continue panel | `src/main_menu.c`, `graphics/interface/main_menu_*.pal` | Hoenn | 1 | The Continue panel says "BADGES" (`main_menu.c:277`) and counts the Pokédex. The windows use the Greek frames. |
| Birch speech scene | `graphics/birch_speech/`, `src/main_menu.c` (about lines 1270–1830), `data/text/birch_speech.inc` | Hoenn | 1 | The portrait is Daphne's, but the text says "BIRCH" and "LITTLEROOT", a Lotad leaves a ball (`SPECIES_LOTAD`), the background and shadow are Hoenn's, and the music is `MUS_ROUTE122`. Text is in §7. |
| Start menu | `src/start_menu.c`, `src/strings.c:427-433,874-884` | Hoenn | 1 | Labels are POKéDEX, POKéMON, BAG, POKéNAV, SAVE, OPTION, EXIT and DEXNAV. Frames are Greek. DexNav shows as "DEXNAV", not the Augur's Eye. |
| Starter selection | `graphics/starter_choose/` (5), `src/starter_choose.c` | Hoenn | 1 | Birch's bag in the grass with three Poké Balls. Ruling 11 keeps the vanilla screen for the slice. Three kraters later. |
| Naming screen | `graphics/naming_screen/` (16), `src/naming_screen.c` | Hoenn | 1 | Emerald's keyboard frame, buttons, cursor and PC icon. Defaults are THEO and IANTHE. |
| Options menu | `src/option_menu.c`, `graphics/text_window/1–20.png` | Greek | 1 | Twenty pottery frame choices (`text_window`). |
| Dialogue box, name box, signpost, menu frames | `graphics/text_window/` (24 files), `tools/ichor/art/ui_frames.py` | Greek | 1 | Terracotta, black-figure, with a meander border. |
| Bag screen | `graphics/bag/`, `src/item_menu.c` | In progress (batch) | Batch | The traveler's satchel. The Brendan and May bag pics, the Pyramid bag and the berry-check art go with it or are cut. |
| Party menu | `graphics/party_menu/`, `src/party_menu.c` | In progress (batch) | Batch | |
| Summary screen | `graphics/summary_screen/`, `src/pokemon_summary_screen.c` | In progress (batch) | Batch | A scroll. The contest-moves page and the ribbon count on the skills page are Hoenn (§11). |
| Shop | `graphics/shop/`, `src/shop.c` | In progress (batch) | Batch | The Agora. |
| Map-name popups | `graphics/map_popup/` (14), `src/map_name_popup.c` | In progress (batch) | Batch | Carved steles. |
| Pokédex | `graphics/pokedex/` (28), `src/pokedex.c`, `src/pokedex_area_screen.c` | Hoenn | 1 | A codex. Daphne gives it in beat 3. The HGSS dex (`POKEDEX_PLUS_HGSS`, `graphics/pokedex/hgss/`) is off, so its art is not in the ROM. |
| Region map and Fly map | `graphics/pokedex/region_map*.png` (Hoenn, Kanto and Sevii maps), `src/region_map.c`, `src/field_region_map.c`, `src/data/region_map/` | Hoenn | 1 | The three Kalliste towns sit on Hoenn's grid at (4,9) to (4,11). Needs the Aethos map. The Kanto and Sevii maps are FRLG leftovers. |
| Pithos storage screen | `graphics/pokemon_storage/` (92 files, 30 box wallpapers), `src/pokemon_storage_system.c` | Hoenn | 1 | Jars. Wallpapers include Azumarill, Dusclops, Pokémon Center and Zigzagoon themes. |
| Trainer card | `graphics/trainer_card/` (`badges.png`, bronze, copper, silver, gold, `bg.bin`), `src/trainer_card.c` | Hoenn | 1 | A kylix. Eight Hoenn gym badges become laurels. |
| Evolution scene | `graphics/evolution_scene/`, `src/evolution_scene.c` | Hoenn | 2 | ART_PLAN §5 lists it. Generic swirl, low priority. |
| Trade scene | `graphics/trade/` (11), `src/trade.c` | Hoenn | 6 | Used for in-game NPC trades as well as link trades. The GBA and cable art is link-only. |
| Hall of Fame | `src/hall_of_fame.c`, `graphics/misc/hall_of_fame.png`, `graphics/field_effects/pics/hof_monitor*` | Hoenn | 4 | The Pantheon's laurel hall. Strings in §7. |
| Credits | `src/credits.c`, `src/data/credits.h` (57 staff pages), `graphics/credits/`, `graphics/intro/scene_2/*_credits.png` | Hoenn | 4 | Emerald's Game Freak staff roll and the bike scenery. See §11. |
| Dex diploma | `graphics/diploma/` (Hoenn and National palettes), `src/diploma.c` | Hoenn | 4 | Signed "GAME FREAK" in `strings.c:906`. |
| Wall clock | `graphics/wallclock/`, `src/wallclock.c` | Hoenn | 1 | The slice script runs `special StartWallClock` as the "water clock" in the player's room. The clock face and its text prompt are Hoenn's. |
| DexNav (the Augur's Eye) | `graphics/dexnav/` (9), `src/dexnav.c`, `include/config/dexnav.h` | Hoenn | 1 | Stock look and the name "DEXNAV". The slice has Alethea give it at the ruins. |
| Scroll of Deeds (quest log) | not in the ROM | New | 3 | PITCH §5 promises it. No quest-log code exists. |
| Difficulty select and the Oath of the Styx | not in the ROM as screens | New | 1 | The bible's four difficulties and the Nuzlocke oath need a new-game screen. `include/constants/difficulty.h` exists. |
| Laurel case | not in the ROM | New | 1 | ART_PLAN §5. Could share the trainer card's laurel art. |
| Save prompt and save info panel | `src/start_menu.c`, `src/strings.c:957` (`gText_SavingBadges`), `data/text/save.inc` | Hoenn | 1 | The info box lists PLAYER, BADGES, POKéDEX and PLAYTIME on the Greek frame. Rename BADGES to LAURELS. |
| Reset-clock and save-error screens | `graphics/reset_rtc_screen/`, `src/reset_rtc_screen.c`, `src/main_menu.c:259-262` | Keep | 6 | Generic text. See §11. |
| Easy Chat and Mail | `graphics/easy_chat/` (9), `graphics/mail/` (12 mail designs), `src/easy_chat.c` | Hoenn | 6 | Proposed cut, §10. |
| Berry tag and berry check | `graphics/bag/berry_tag*`, `check_berry*`, `src/berry_tag_screen.c` | Hoenn | 2 | Follows the berry decision (§1). |
| Pokémon Jump, Berry Crush, Dodrio picking, slot machine and roulette screens | `graphics/pokemon_jump/`, `berry_crush/`, `dodrio_berry_picking/`, `slot_machine/`, `roulette/` | Cut | 6 | Per ART_PLAN, as minigames (§10). |
| Contest, Berry Blender, Pokéblock, PokéNav, Union Room, Mystery Gift, Wonder Card and secret-base screens | `graphics/contest/`, `berry_blender/`, `pokeblock/`, `pokenav/`, `union_room_chat/`, `wonder_card/`, `wonder_news/`, `link/`, `wireless_status_screen/` | Cut | 6 | Per ART_PLAN (§10). |
| Link and Frontier screens: Frontier Pass, Trainer Hill, picture frames | `graphics/frontier_pass/`, `graphics/picture_frame/` | Cut | 5 | See §10. |

## 6. Items

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Item icons, 874 items | `graphics/items/icons/` (619 PNGs), `graphics/items/icon_palettes/`, `src/data/items.h` | Hoenn | 1 | All Emerald and expansion icons. About 115 KiB. Restyle phase by phase as each is needed, starting with the slice's list (`SCRIPT.md` Part 6): Potion, Super Potion, Antidote, Paralyze Heal, Awakening, Repel, Escape Rope, Poké Ball, Oran and Sitrus Berry, Honey, Moomoo Milk, Miracle Seed, Hard Stone, Stardust, Pearl, Heart Scale, Relic Copper, Charcoal, Old Rod, Mystic Water and TM42. |
| Medicines and battle items | `graphics/items/icons/` | Hoenn | 1 | Clay flasks and herb bundles (ART_PLAN §5). |
| Poké Balls and their cases | 28 ball items, `graphics/items/icons/*_ball.png`, `graphics/balls/` | Hoenn | Director | See §4. |
| Berries | 68 berry items, `graphics/berries/` | Hoenn | 2 | See §1. 15 berry descriptions end with "{POKEBLOCK} ingredient". |
| TMs and HMs | 108 items (100 TMs, 8 HMs), `graphics/items/icons/tm.png`, `hm.png`, `tm_case.png` | Hoenn | 2 | Clay tablets (TM) are an easy restyle. The eight HMs (Cut, Fly, Surf, Strength, Flash, Rock Smash, Waterfall, Dive) are replaced by relics (next row). |
| Field-power relics | none (`ITEM_TALARIA`, `ITEM_LABRYS` and the rest do not exist) | New | 1–3 | Talaria (run), Daedalus's Wings (Fly), Poseidon's Conch (Surf), Bronze Hammer (Rock Smash), Labrys (Cut), Girdle of Herakles (Strength), Hecate's Torch (Flash), Nereid Pearl (Dive): 0 of 8 exist. The player's field-move pose already raises a relic. Waterfall has no relic in PITCH §5. The slice needs only the Talaria, which Mom gives you in beat 1. |
| Omphalos (Mega key stone) | `ITEM_MEGA_RING` (key item "Mega Ring") | New | 4 | Rename and redraw. |
| Ichor Stones (Mega Stones) | 92 Mega Stone items | Hoenn | 4 | Redraw as one shared icon family with per-stone glints. |
| Laurels (badges) | `graphics/trainer_card/badges.png`, item/flag `FLAG_BADGE01_GET…08` | Hoenn | 1 | The Hearth Laurel is the slice's reward. |
| Augur's Eye, Scroll of Deeds, Laurel case | key items | New | 1–3 | The Augur's Eye is already flagged (`FLAG_ICHOR_DEXNAV_GET`). |
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
| New-game speech | `data/text/birch_speech.inc` (3 Birch blocks), `src/strings.c:46`, `src/main_menu.c` | Hoenn | 1 | "My name is BIRCH", "LITTLEROOT", "POKéMON LAB". Rewrite as Daphne's speech ("every myth is a memory of a Pokémon"). `gText_ThisIsAPokemon` keeps its slot. |
| Starter-choice strings | `src/strings.c:63-64` | Hoenn | 1 | `gText_BirchInTrouble`, "Do you choose this POKéMON?". The rescue premise is gone. |
| Whiteout and rescue messages | `src/field_screen_effect.c:64,66,1471` | Hoenn | 1 | "scurried to a POKéMON CENTER" (twice) and `StringCopy` of "PROF. BIRCH". |
| Asclepeion nurse text | `data/text/pkmn_center_nurse.inc` (10 strings), `data/scripts/pkmn_center_nurse*.inc` | In progress (batch) | 1 | Ruling 6: Ichor-only copies, so Hoenn's text stays until Hoenn goes. The shared version says "POKéMON CENTER" and mentions the GOLD CARD. |
| Pithos (PC) strings | `data/text/pc.inc`, `data/scripts/pc.inc` ("SOMEONE'S PC", "LANETTE'S PC") | In progress (batch) | 1 | Ichor-only copies per ruling 6. |
| Start and main menu labels | `src/strings.c:427-433,874-884`, `src/main_menu.c:277` | Hoenn | 1 | POKéNAV, DEXNAV, BADGES, POKéDEX. |
| Pokédex dex-mode titles | `src/pokedex.c:1184` ("HOENN region's POKéDEX", "HOENN DEX"), `src/strings.c:904,909` ("HOENN") | Hoenn | 1 | Replace with the Aethos dex. |
| Pokédex rating | `data/text/pokedex_rating.inc` (about 25 rating blocks, each spoken by "PROF. BIRCH"; two mention the HOENN region), `src/strings.c:53` | Hoenn | 4 | |
| Hall of Fame and diploma text | `src/strings.c:57,63,906`, `src/hall_of_fame.c` | Hoenn | 4 | "LEAGUE CHAMPION!", "PROF. BIRCH's POKéDEX rating", "GAME FREAK". |
| Battle messages that name Hoenn people | `src/battle_message.c` (`STRINGID_DONTLEAVEBIRCH`, `gText_WhatWillWallyDo`, `gText_BattleWallyName`, the Wally catch tutorial, the champion lines at `:1524-1527`) | Hoenn | 1 | The generic wording ("Wild X appeared!", damage and status text) stays. See §11. |
| Trainer class names | `src/battle_main.c` `gTrainerClasses` | Hoenn | 2–5 | 9 Aethos names are in. 116 Hoenn and FRLG names remain, including "ELITE FOUR", "CHAMPION" and "LEADER". |
| Place names and landmarks | `src/data/region_map/region_map_sections.json` (212 map sections; 3 are Ichor), `src/landmark.c` (27), `src/data/heal_locations.json` (42; no Akti yet) | Hoenn | 1 | Names appear in the map popup, Fly map, Pokédex areas and summary "Met at" lines. |
| Hoenn words in strings: HOENN, BIRCH, POKéNAV, POKéMON CENTER, MART, GYM, LEAGUE | the files in the rows above, plus `data/text/*.inc` and `src/data/*.h` | Hoenn | 1–5 | The count below is matching string lines. System text and shared scripts: HOENN 20, BIRCH 10, POKéNAV 41, POKéMON CENTER 19, GYM 105, LEAGUE 27. Hoenn map scripts: HOENN 42, BIRCH 45, POKéNAV 53, POKéMON CENTER 8, MART 13, GYM 169, LEAGUE 43. Fix the system text first; the map scripts go with the maps. "POKé MART" never appears as a string. |
| Trainer dialogue | `data/text/trainers.inc` (2,507 string lines, about 855 Hoenn trainers) | Hoenn | 2–5 | Mentions GYM BADGES, LEAGUE and CHAMPION. The 14 Ichor trainers' text is in `SCRIPT.md`. |
| Hoenn map-script dialogue | `data/maps/*/scripts.inc` (about 520 non-FRLG folders, 15,700 string lines) | Hoenn | 2–5 | Hoenn counts: 42 "HOENN", 45 "BIRCH", 53 "POKéNAV", 169 "GYM", 43 "LEAGUE", 63 "TEAM AQUA", 65 "TEAM MAGMA", 53 "CONTEST", 8 "POKéMON CENTER". Goes away with the maps. |
| Slice dialogue | `design/phase1/SCRIPT.md`, `data/maps/{ElaiaVillage*,KallisteRoute1*,AktiTown*}/scripts.pory` | In progress (batch) | Batch | The maps and scripts batch. |
| Story, tutor and lottery text | `data/text/move_tutors.inc` (Mossdeep, Sootopolis gyms), `apprentice.inc`, `mauville_man.inc`, `lottery_corner.inc`, `tv.inc`, `match_call.inc` (69 lines), `fame_checker_frlg.inc` | Cut | 6 | Most go with their systems (§10). Move-tutor text needs a rewrite if tutors stay. |
| Berry descriptions that mention Pokéblocks | `src/data/items.h` (15 berries, "{POKEBLOCK} ingredient") | Hoenn | 2 | Goes with the Pokéblock cut. |
| Item descriptions | `src/data/items.h` | Hoenn | 2 | Mostly generic. A few mention Contests, Devon Corp and Poké Flute. |
| Shared strings that say Pokémon | `src/strings.c`, `src/battle_message.c` and the party and summary screens | Keep | 6 | The title is "Pokémon Ichor", so "POKéMON" and the `{PKMN}` glyph stay. Decide once and record it (§11). |

## 8. Audio

Songs by use. Counts are from `include/constants/songs.h` and sizes are from the map (KiB of ROM). The ROM holds about 220 songs.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Ichor songs: Elaia, Route 1, Akti, Hestia temple, Asclepeion, Titan, trainer, wild and rival battle themes, trainer victory | `sound/songs/midi/mus_ichor_*.mid` (10, 16 KiB), `sound/voicegroups/` Ichor voicegroup, `tools/ichor/music/` | Greek | 1 | Registered at the end of `song_table.inc`. |
| Slice fanfares and the rest of the slice's songs | `include/constants/songs.h` | In progress (batch) | Batch | Music batch 2. Heal, level-up, item, caught, evolution and badge fanfares are still Hoenn's. Check that the batch also covers the title, intro and new-game speech tracks. |
| Title theme | `MUS_TITLE` in `src/title_screen.c:671` | Hoenn | 1 | The screen is Greek but boots with Emerald's tune. |
| Intro tracks | `MUS_INTRO`, `MUS_INTRO_BATTLE` in `src/intro.c:1208,1731` | Hoenn | 1 | Go with the intro (§5). |
| New-game speech music | `MUS_ROUTE122` in `src/main_menu.c:1287` | Hoenn | 1 | The Hoenn route theme plays under the speech. |
| Towns and cities | 13 songs, 49 KiB: Littleroot, Oldale, Petalburg, Rustboro, Dewford, Slateport, Verdanturf, Fallarbor, Fortree, Lilycove, Sootopolis, Ever Grande (plus a test track) | Hoenn | 2–5 | One theme per Aethos town as it arrives. |
| Routes, woods and travel | 17 songs, 56 KiB: Routes 101, 104, 110, 113, 118, 119, 120, 122, Petalburg Woods, cycling, surf, sailing, underwater, desert, two GSC leftovers, Follow Me | Hoenn | 2–5 | Cycling is cut with bikes. |
| Dungeons and set pieces | 12 songs, 39 KiB: Mt. Chimney, Mt. Pyre (and exterior), Cave of Origin, Abandoned Ship, Sealed Chamber, Aqua/Magma hideout, Victory Road, abnormal weather, Groudon weather, Awaken Legend, Rayquaza appears | Hoenn | 3–5 | Keep the shape of a few (cave, victory road) as Aethos dungeons. |
| Buildings and indoor | 8 songs, 20 KiB: Pokémon Center, Mart, Gym, Birch Lab, Pokémon School, two museums, Help | Hoenn | 1 | `mus_ichor_asclepeion` and `mus_ichor_temple` cover two. Agora, Akademia and houses need theirs. |
| Battle themes | 14 songs, 45 KiB: wild, trainer, gym leader, rival, Aqua/Magma, champion, Elite Four, Kyogre/Groudon, Rayquaza, Regi, Mew, Frontier Brain, legend beast, intro battle | Hoenn | 2–4 | The Ichor wild, trainer and rival themes exist. Still needed: Hierophant, Titan admins, Pantheon, Archon, Kronos and Dialga. |
| Trainer-sighting jingles | 17 songs, 39 KiB (`MUS_ENCOUNTER_*`) | Hoenn | 1 | `src/data/trainer_approach_music.h` maps classes to them. Ichor classes need Greek-mode jingles. |
| Fanfares and jingles | 18 songs, 24 KiB: caught, victory (wild, trainer, leader, league, Aqua/Magma, road), level up, heal, badge, item, evolved, TM, evolution (and intro), move deleted, berry, "too bad" | Hoenn | 1 | Music batch 2 owns the slice's fanfares (row above). |
| Title, credits, Hall of Fame | 6 songs, 32 KiB: title, intro, credits, end, Hall of Fame, HoF room | Hoenn | 4 | Credits and HoF come with Act III. |
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
| Ichor maps | `data/maps/{ElaiaVillage*,KallisteRoute1*,AktiTown*}`, `data/ichor_maps.inc` | In progress (batch) | Batch | 12 maps: Elaia, Route 1, Kronion Hill, Akti, and eight interiors. The layouts and scripts are stubs on Hoenn tilesets. |
| FRLG maps, tilesets and scripts | `*_Frlg` maps, `*_frlg` tilesets and scripts | Cut | 6 | Removed by hoenn-cut batch 2. They were never in the Emerald ROM. A few FRLG tileset animation frames stay, because `src/tileset_anims.c` names them. On upstream merges, resolve modify/delete conflicts on these paths with `git rm`. |
| Hoenn trainers | `src/data/trainers.party`, `include/constants/opponents.h`, `src/data/battle_partners.party` (2) | Cut | 2–5 | Removed by hoenn-cut batch 1: 847 Hoenn trainers gone, Ichor's 14 renumbered 1–14, and the seven Frontier Brains kept at 15–21 for the Frontier engine. `gTrainers` fell from 132 KiB to 3.4 KiB and now grows only with real trainers. Id ranges per session are in `tools/ichor/claim_ranges.md`. `PARTNER_STEVEN` is still there. FRLG's 624 trainers in `trainers_frlg.party` are not built. |
| Trainer-slide tables | `src/trainer_slide.c` | Keep | 6 | 355 KiB of mostly empty pointers: `sTrainerSlides` (264 KiB, three difficulties × (`MAX_TRAINERS_COUNT` + partners) × 26 slides) and `sFrontierTrainerSlides` (91 KiB). They are sized by the id limits, not by how many trainers exist, so the trainer cut barely shrank them. Keeping only the Normal difficulty's slides would free about 237 KiB, an engine edit for the director. |
| Hoenn wild encounter tables | `src/data/wild_encounters.json` | Cut | 2–5 | Removed by hoenn-cut batch 2: 388 Hoenn and FRLG headers. |
| Heal locations | `src/data/heal_locations.json` | Greek | 1 | Elaia and Akti, plus the Battle Frontier's until batch 3. |
| Fly destinations and region sections | `src/data/region_map/` | Hoenn | 1 | Hoenn's sections 0–85 are now free `MAPSEC_OIKOUMENE_*` slots (hoenn-cut batch 2; see `tools/ichor/claim_ranges.md`). See §5 and §7. |
| Flags and vars | `include/constants/flags.h`, `vars.h` | Keep | — | Hoenn-cut batch 2 freed 700 flags and 95 vars. The per-session ranges are in `tools/ichor/claim_ranges.md`. |
| Mart stock, tutors, in-game trades, apprentices, lottery | `data/scripts/`, map scripts | Hoenn | 2–5 | Rebuilt per Aethos location. |
| Move tutors and Frontier rewards | `data/text/move_tutors.inc`, `data/scripts/move_tutors.inc` | Hoenn | 3 | Needs Aethos tutors and, in Phase 5, Olympiad prizes. |
| Hoenn contest and Frontier data tables | `src/data/contest_*.h`, `src/data/battle_frontier/`, `data/contest_ai_scripts.s` | Cut | 5 | Counted in §10. The Frontier engine is kept; its tables are replaced by Olympiad data. |

## 10. Hoenn-only systems to cut

The first block is ART_PLAN's cut list, plus FRLG data, the PokéNav, Mirage Island, the minigames and the link and e-Reader pieces named in the brief. Each is sized as its code, text, graphics, music, SFX, maps and tilesets, from the map. The totals count only things that are in the ROM now.

| System | Where | ROM (KiB) | Status | Phase | Notes |
|---|---|---|---|---|---|
| Contests | `src/contest*.c`, `contest_ai.c`, `picture_frame`, `graphics/contest/`, `graphics/picture_frame/`, `data/contest_ai_scripts.s`, `include/config/contest.h`, `ContestHall*` maps, `gTileset_Contest`, 8 contest songs | 201.3 | Cut | 6 | Includes the Lilycove Lady, the contest SFX and the contest-category icons in `graphics/types/`. Contest scarves and the summary screen's contest-moves page need to go with it. |
| Berry Blender | `src/berry_blender.c`, `graphics/berry_blender/`, `data/text/blend_master.inc`, `SE_BERRY_BLENDER` | 38.5 | Cut | 6 | |
| Pokéblocks | `src/pokeblock*.c`, `use_pokeblock.c`, `graphics/pokeblock/` | 31.3 | Cut | 6 | Tied to the Blender, contests and the Pokénav's conditions. |
| Secret bases and decorations | `src/secret_base.c`, `decoration*.c`, `graphics/decorations/`, `data/tilesets/*/secret_base*`, `SecretBase_*` maps, `data/text/secret_base_trainers.inc` | 123.4 | Cut | 6 | Includes the player's decorating pose, the doll and cushion object sprites and `record_mixing` hooks. |
| Mirage Island and Mirage Tower | `src/mirage_tower.c`, `MirageTower_*` maps, `gTileset_MirageTower`, `Route111_NoMirageTower`, `Route130_MirageIsland` layouts, `graphics/misc/mirage_tower*` | 43.6 | Cut | 6 | |
| PokéNav and Match Call | `src/pokenav*.c` (14 files), `src/match_call.c`, `graphics/pokenav/` (64), `data/text/match_call.inc`, `SE_POKENAV_*` | 137.3 | Cut | 6 | Region map and ribbons are also reachable through the Pokénav. Keep the region map code if the Fly map needs it. |
| e-Reader and Mystery Gift | `src/mystery_gift*.c`, `mevent*.c`, `ereader*.c`, `data/multiboot_ereader.s`, `graphics/wonder_card/`, `wonder_news/`, `MysteryEventsHouse` | 61.0 | Cut | 6 | Includes the 12.5 KiB e-Reader multiboot program and the Mystery Events House tileset. |
| Minigames: slots, roulette, Pokémon Jump, Berry Crush, Dodrio picking, lottery corner, Game Corners, Trick House | `src/slot_machine.c`, `roulette.c`, `pokemon_jump.c`, `berry_crush.c`, `dodrio_berry_picking.c`, `lottery_corner.c`, `minigame_countdown.c`, matching `graphics/` and maps | 235.3 | Cut | 6 | Trick House has its own tileset, maps and music. |
| Link-only features: Union Room, link trade and battle, Cable Club, record mixing, Colosseum multiboot, rfu library, Berry-fix multiboot | `src/union_room*.c`, `link*.c`, `librfu*.c`, `AgbRfu_LinkManager.c`, `cable_club.c`, `record_mixing.c`, `data/multiboot_pokemon_colosseum.s` (164 KiB), `data/multiboot_berry_glitch_fix.s` (15 KiB), `BattleColosseum_*`, `UnionRoom`, `TradeCenter`, `CableClub` maps and tilesets | 419.9 | Cut | 6 | Includes `src/trade.c` (69 KiB) and the trade art. In-game NPC trades share that scene, so the saving is about 70 KiB smaller if they stay. |
| Hoenn Battle Frontier: maps, art, trainers, text | `BattleFrontier_*` maps (Tower, Dome, Palace, Pike, Pyramid, Arena, Factory, lounge), `BattlePyramidSquare*`, three Battle Tents, `TrainerHill_*`, twelve Frontier and Trainer Hill tilesets, `graphics/battle_frontier/`, `frontier_pass/`, `door_anims/battle_*`, `sFrontierTrainerSlides`, `data/text/battle_tent.inc` | 540.6 | Cut | 5 | Per ART_PLAN: the Hoenn facilities go. The Olympiad (PITCH §6.3) is built fresh at Olympia, with Achilles, Atalanta, Odysseus and Hippolyta as Brains. |
| FRLG data in the ROM | 75 FRLG songs (239 KiB), two FRLG Japanese fonts (64 KiB), 62 FRLG trainer pics (43 KiB), Kanto and Sevii region-map art, `hall_of_fame_frlg.c`, `voicegroup_frlg_*` | 365.4 | Cut | 6 | Per ART_PLAN, but FRLG maps are not in the ROM, so this is the whole ROM saving. The repo cleanup is in §9. |
| **Total, ART_PLAN's list (Frontier engine kept)** | | **2,197.7** | | | **2.15 MiB (2.25 MB)** |
| Hoenn Battle Frontier engine and data tables | `src/battle_tower.c` (`gBattleFrontierMons` 32 KiB, `gBattleFrontierTrainers` 16 KiB), `battle_dome.c`, `battle_pike.c`, `battle_pyramid.c`, `battle_arena.c`, `battle_factory*.c`, `battle_palace.c`, `battle_tent.c`, `trainer_hill.c`, `trainer_tower*.c`, `frontier_util.c`, Frontier songs | 341.2 | Keep | 5 | Keep: the Olympiad needs the facilities' rules. Replace the Hoenn trainer and Pokémon tables. Removing the engine too adds 341 KiB. |
| **Total if the Frontier engine also goes** | | **2,538.9** | | | **2.48 MiB (2.60 MB)** |

Additional Hoenn-only systems. They are **not** on ART_PLAN's list, so they are not in the totals above. I propose cutting them, and the director decides.

| System | Where | ROM (KiB) | Status | Phase | Notes |
|---|---|---|---|---|---|
| Mauville Old Man: bard, storyteller, hipster, Giddy, trader | `src/mauville_old_man.c`, `bard_music.c` (162 KiB of phoneme data), `sound/direct_sound_samples/phonemes/`, `ph_*.mid` | 283.8 | Cut | 6 | The biggest candidate. Easy Chat words and phonemes. |
| TV shows, Battle TV and Pokémon News | `src/tv.c`, `battle_tv.c`, `data/text/tv.inc` (2,193 string lines), `pokemon_news.inc` | 76.6 | Cut | 6 | The Aethos world has no TV. The oikos tileset already turns the TV into a loom. |
| Easy Chat and Mail | `src/easy_chat.c`, `data/text/`, `graphics/easy_chat/`, `graphics/mail/`, 12 mail items | 59.1 | Cut | 6 | Mail has no setting. Easy Chat words also feed trainer greetings. |
| Safari Zone | `src/safari_zone.c`, `battle_controller_safari.c`, `healthbox_safari.png`, Safari maps | 40.9 | Cut | 6 | |
| Cable car and SS Tidal and ferries | `src/cable_car.c`, `ss_anne.c`, `seagallop.c`, graphics | 44.9 | Cut | 6 | Triremes replace ferries. |
| Apprentice, Lilycove Lady, wall-clock set screen, mass outbreaks | `src/apprentice.c`, `lilycove_lady.c`, `wallclock.c`, `mass_outbreak.c` | 68.2 | Cut | 6 | The Lilycove Lady is counted under Contests, not here. Keep the wall clock until the water-clock scene has its own art (§5). |
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
| Game Freak copyright and logo | `graphics/intro/copyright.png`, `graphics/intro/scene_1/`, `graphics/credits/the_end_copyright.png`, `src/strings.c:906` (diploma "GAME FREAK"), `graphics/intro/` | Hoenn | 1 | The screen credits Nintendo, Creatures and Game Freak as the game's makers. Replace it with an Ichor fan-work notice that credits the original games, in the voice the title already uses ("A FAN WORK · 2026"). |
| Credits roll | `src/data/credits.h` (57 pages of Game Freak staff), `src/credits.c`, `graphics/credits/` | Hoenn | 4 | Needs Ichor's own credits plus upstream attribution (pokeemerald, expansion, tools, fonts, music sources). |
| ROM header title and game code | `Makefile` (`TITLE ?= POKEMON EMER`, `GAME_CODE ?= BPEE`, `MAKER_CODE := 01`), `src/rom_header_gf.c:102` (`"pokemon emerald version"`), `src/rom_header_rhh.c` | Hoenn | 6 | The ROM header still reads "POKEMON EMER". Change the 12-byte title. Keep `BPEE`, because emulators pick the save type from the game code. |
| Default player and rival names | `src/main_menu.c:481,485` ("THEO", "IANTHE") | Greek | 1 | Done. The rival is Kleon by script, and there is no rival-naming step (`sText_RivalsName` is used only by the FRLG Oak speech). Check the in-game-trade nicknames, egg OT strings and the debug menu's Brendan and May follower entries. |
| Save-error and corruption screens | `src/main_menu.c:259-262`, `src/strings.c:568` | Keep | 6 | Plain text. Only the "POKéMON" word and the menu frame show. Worth a proofread. |
| Clock reset screen | `src/reset_rtc_screen.c`, `graphics/reset_rtc_screen/` | Keep | 6 | Generic. "The internal battery has run dry". |
| Battle-message wording | `src/battle_message.c` | Hoenn | 1 | Sweep for "FOE", "Wild", "ELITE FOUR", "CHAMPION", "LEADER", "PROF. BIRCH", Wally and the Frontier lines. Trainer-class openers like "{CLASS} {NAME} would like to battle!" are generic. |
| `{PKMN}` glyph and the "POKé" glyphs | `charmap.txt:55` (`PKMN`), `graphics/fonts/latin_*.png` | Keep | Director | The font draws "PK" and "MN" as small caps in 2 tiles. Fine if the game keeps "Pokémon". Record the decision (§7). |
| The font | `graphics/fonts/` (23 files), `src/fonts.c` (422 KiB) | Keep | Director | Gen 3's six Latin variants plus 5 Japanese ones. Greek letters appear on the title as paint, not as glyphs. A Greek-style font is optional. |
| Japanese font tables | `src/fonts.c` (`gFont*Japanese*`), `src/text.c` (`sFontBoldJapaneseGlyphs`), `graphics/fonts/japanese_*.png` | Cut | 6 | About 75 KiB beyond FRLG's 64 KiB (counted in §10). An English-only build can drop them, but it needs careful engine work. Not in any total. |
| Ribbons | `src/pokemon_summary_screen.c` (ribbon count on the skills page), `graphics/pokenav/ribbons/`, `src/data/` ribbon names | Hoenn | 4 | Champion, Cool, Beauty, Winning, Effort, Marine and so on. Re-theme as Laurels or cut with contests. |
| Summary "Trainer memo" and "Met at" lines | `src/pokemon_summary_screen.c`, `src/strings.c` | Hoenn | 1 | Use the Hoenn place names (§7). |
| Move-tutor, PC and trade-scene text | `data/text/move_tutors.inc`, `data/text/pc.inc`, `data/text/ingame_trade_frlg.inc` | Hoenn | 2 | |
| Pocket names | `src/strings.c:145` ("POKé BALLS" and others) | Hoenn | Batch | Part of the bag restyle. |
| Pokémon type names and move names | `src/data/types_info.h`, `src/data/moves_info.h` | Keep | — | Generic. |
| Pokémon Center and Mart words in the follower messages | `src/follower_helper.c:26,132-140` | Hoenn | 1 | "staring straight at the POKéMON LEAGUE", the Mart music cue. |
| Dev tools | `src/debug.c` (28 KiB), `graphics/quickstart/`, `include/config/quickstart.h`, `include/config/debug.h` | Keep | 6 | Disable for the release patch. Quickstart is flagged as off in release builds. |
| Hoenn flags and vars in names | `include/constants/flags.h`, `vars.h` | Keep | — | Internal names only. |
| Unused graphics | `graphics/unused/` (11 PNGs: old battle UI, a Bulbasaur and a Charizard) | Keep | 6 | Not built into the ROM. Delete when tidying. |
| Pokémon Center jingle at the heal tray, the Pokémon Center fainting sequence | `graphics/field_effects/`, `MUS_HEAL` | Hoenn | 1 | See §1 and §8. |
| The brand "Pokémon Ichor" on the title | `graphics/title_screen/` | Greek | 1 | Done. |
