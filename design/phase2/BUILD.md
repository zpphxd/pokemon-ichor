# Phase 2 build plan: Act I on the mainland

Owner: the world-act1 session (branch `claude/world-act1-6d11b7`). This is the working plan for building `design/phase2/SCRIPT.md` as playable content. SCRIPT.md says what happens; this file says who builds which file, with which ids, and what is stubbed until another session lands.

Read first, in this order: `CLAUDE.md`, `design/MAP_DESIGN.md`, this file, the SCRIPT.md beats and Part 2 rosters for your maps, `design/TERMS.md`, then the slice's model for your kind of work (below).

## Batches

The route chain follows the revised `design/AETHOS_MAP.md`; SCRIPT.md's route plan has the reconciliation note.

| # | Batch | Status |
|---|---|---|
| 1 | The voyage (Routes 2–3) and Aigina: beats 9A–10C, the *Euploia*, Aigina Town and its three homes; Aigina's three interior maps built for world-act2 (Act II) | in progress |
| 2 | Emporion and the Temple of Hermes: beats 11–16 | in progress (tilesets on main) |
| 3 | Route 4 (the Isthmus), Hecate's Hollow, Route 5 (the Skironian cliffs): beats 17–19 | tilesets started: `isthmos`, `cave_dark` |
| 4 | Eleusa and the Temple of Demeter: beats 20–22 | the maps, ambient events and the rite's layout built (below); the story scenes next |
| 5 | The revelation: beats 23–25, the sanctum, Return to Kalliste | |

**Moved out of Act I** (to world-act2): Thria, the Rheitoi and the jesters' bridge (Route 15); the Halai Shore's homes and trainers (Route 18); the scripting of Aigina's interior.

## Batch 1 maps

All are registered (`tools/ichor/new_map.py`) with placeholder layouts copied from Akti; each owner rewrites its layout's size, tilesets and blockdata in `data/layouts/layouts.json` and `data/layouts/<Map>/`.

| Map | Size | Tilesets | Type | Owner |
|---|---|---|---|---|
| `MAP_TRIREME_EUPLOIA_DECK` | 24×16 | aethos + **trireme** (new) | ocean route, no name popup | trireme agent |
| `MAP_TRIREME_EUPLOIA_HOLD` | about 18×9 | oikos or aethos + **trireme** | indoor | trireme agent |
| `MAP_AEGINA_TOWN` | 30×24 | aethos + **aegina** (new) | town | Aegina agent |
| `MAP_AEGINA_TOWN_INN` | room | oikos + **ergasteria** (new) | indoor | interiors agent |
| `MAP_AEGINA_TOWN_MINT` | room | oikos + **ergasteria** | indoor | interiors agent |
| `MAP_AEGINA_TOWN_AIAKIDES_HOUSE` | room | oikos + **ergasteria** (or oikia if it fits) | indoor | interiors agent |
| `MAP_AEGINA_APHAIA_ROAD` | 40×24 | aethos + **aegina** | route | detour agent (after the Aegina tileset); Act II, scripted by world-act2 |
| `MAP_AEGINA_TEMPLE_OF_APHAIA` | 24×20 | aethos + **aegina** | route | detour agent |
| `MAP_AEGINA_MOUNT_OROS` | 16×16 | aethos + **aegina** | route | detour agent |

**Tilesets.**
- `trireme`: SCRIPT.md Part 10. Deck planks, the mast and sail (furled, full, sagging), the bronze ram and the painted eye, steering oars, the stern's curl, rope coils, lashed amphorae, the hatch, the rail with gaps where the player can fish over the side; the hold's three banks of benches with oars. The sea round the deck is aethos's animated sea.
- `aegina`: one secondary for all four Aegina outdoor maps, so their seams need no aethos-only strip. Akti's harbor pieces (copy them from `tools/ichor/art/akti_*.py`) plus the round mole, Kolona's column on its headland, the inn and mint fronts, Aiakides's house, ant hills, pistachio trees, dry grass and scrub, the gate, the Temple of Aphaia's Doric front on its pine hill, Zeus's summit altar, a herm (aethos has one at 0x01B).
- `ergasteria` ("workshops"): Phase 2's working interiors. `oikia` is full and `civic` has 48 tiles left, so this new secondary on the `oikos` primary carries the furniture those rooms share (copied from oikia/civic as needed) plus the new pieces. Batch 1 draws Aegina's inn (courtyard cistern, wooden guest gallery, turtle mosaic, hearth), the mint (two anvils, coin dies on a rack, a blank-heating brazier, scales, a turtle-stamped chest) and Aiakides's house (shield and spear trophy, clay-ant shrine, an anthill in a pot). Leave room: Emporion's workshops (the forge, the potter's wheel and kiln) are planned for this set in batch 2. Keep under 440 tiles in batch 1.

Every secondary stays at or under 504 tiles; leave 496–511 free where a map uses wide doors (CLAUDE.md).

## Batch 2 maps

Registered with placeholder layouts; each owner rewrites its layout.

| Map | Tilesets | Owner |
|---|---|---|
| `MAP_EMPORION_CITY` | aethos + **emporion** | Emporion city agent |
| `MAP_EMPORION_HARBOR` (the harbor district, where the *Euploia* moors) | aethos + **isthmos** | Emporion city agent |
| `MAP_EMPORION_CITY_ASCLEPEION`, `_DEIGMA`, `_HEPHAISTEION`, `_TAVERN`, `_PHILOXENOS_HOUSE`, `_WIDOWS_HOUSE`, `_RUNNERS_HOUSE`, `_POTTERS_WORKSHOP`, `_HIRING_HALL` | oikos + ergasteria (or civic, oikia) | Emporion interiors agent |
| `MAP_EMPORION_CITY_TEMPLE_OF_HERMES` | oikos + **temple_hermes** | Temple of Hermes agent |

The city's west gate is the **Isthmus Gate** to Route 4 (batch 3); its seam columns go in the connections table. The Long Walls Gate of SCRIPT.md has no road in the revised map: Astyra is reached through Eleusa in Act II, so it isn't drawn.

## Warps, connections and seams (batch 1)

| From | To | How |
|---|---|---|
| Akti quay, the gangplank | the deck | scripted warp (beat 9B, and the ferry) |
| the deck, the hatch | the hold | warp both ways: the deck's warp **1** is the hatch (14,7), the hold's warp **0** the ladder's foot (11,5); each sends to the other (both `MB_LADDER`) |
| the deck | Aegina's quay | scripted warp (end of beat 10, and the ferry) |
| Aegina's inn, after the night | the deck | scripted warp (beat 10C) |
| Aegina Town doors | inn, mint, Aiakides's house | warps both ways. Aegina Town's warps: **0** the quay landing (12,12), not a door: `warp(MAP_AEGINA_TOWN, 0)` lands the ferry and the end of beat 10 there; **1** the inn door (15,16); **2** the mint door (21,16); **3** Aiakides's door (27,8). Each door's `dest_warp_id` is 0, so each room's warp 0 is its door mat; the rooms send the player back to town warps 1, 2 and 3. |
| Aegina Town, north gate | the Aphaia Road | map connection, up. The gate's passage is **columns 24-25** of Aegina Town; row 0 is walkable there and nowhere else (pines and scrub close the rest). Aegina's row 0 is sea west of column 21, so the Aphaia Road's bottom rows over Aegina's columns 0-20 should be sea or shore. With the road at the Aphaia Road's columns c and c+1, the connection's offset is 24 − c. |
| the Aphaia Road | the Temple of Aphaia, Mount Oros | the detour agent's choice (connections or warps), recorded here |

Record the warp ids and the arrival tiles you choose in this table, so the scripted warps in other maps can use them.

| Map | Arrival tile (x, y) | For |
|---|---|---|
| `MAP_TRIREME_EUPLOIA_DECK` | (13,4), the starboard entry port where the gangplank comes aboard; warp **0** is there (not a door): `warp(MAP_TRIREME_EUPLOIA_DECK, 0)` | boarding from a quay, the ferry, and the inn's warp for beat 10C. Casting off plays on arrival there while `FLAG_ICHOR_BOARDED_EUPLOIA` is set and `FLAG_ICHOR_SAVED_HALCYON_NEST` clear; beat 10C plays on any arrival while `FLAG_ICHOR_AEGINA_NIGHT` is set and `FLAG_ICHOR_CROSSING_DONE` clear |
| `MAP_AEGINA_TOWN` | (12,12), the quay below the gangplank; warp 0 is there | stepping off the *Euploia* (beat 10B plays on arrival while `FLAG_ICHOR_ARRIVED_AEGINA` is clear) |
| `MAP_AKTI_TOWN` | (9, 10), the quay by the gangplank | stepping off the ferry |
| `MAP_ELEUSA_VILLAGE` | (25, 12), the Telesterion's steps | beats 22 and 24, outside the hall |
| `MAP_ELEUSA_VILLAGE_TEMPLE_OF_DEMETER` | (13, 26), the stair; (13, 14), the Anaktoron's doorway | entering; beat 22's scene and beat 25 |

## Batch 4: Eleusa and the Temple of Demeter

Built by the Eleusa agent: `tools/ichor/maps/eleusa.py` (the village, 50×40, aethos + eleusa) and `tools/ichor/maps/temple_demeter.py` (the Telesterion, 27×27, oikos + temple_demeter, dark). Passes and renders: `design/phase2/MAPS_eleusa.md`.

**Connections and seams.** None of Eleusa's neighbours exists yet, so `map.json` has no connections; the openings are built and `eleusa.py` checks them. Eleusa's 8 columns nearest the west and east edges and its 6 rows nearest the north edge use aethos metatiles only.

| Edge | Neighbour | Open on Eleusa's side | Notes |
|---|---|---|---|
| west (left) | Route 5, the Skironian cliffs | rows y 24–27 at x = 0 | The Sacred Way in from Hecate's Hollow; Krokis's gate is just inside, at x 7–8. |
| north (up) | Route 6, `MAP_ROUTE6_ELEUTHERAI_ROAD` (world-act2) | columns x 44–47 at y = 0 | A two-column road (x 45–46) between grass verges (x 44, 47). The vines are on Route 6's map, past the seam; Eleusa's side is open. |
| east (right) | Route 15, the road of the Mysteries | rows y 24–27 at x = 49 | Shut in Act I: a dry-stone wall across the road at x = 48 (rows 24, 26–27) with a hoplite standing in its gap at (48, 25). Act II hides him (a hide flag of the story's choosing). |

**Doors.** Every door's warp, by Eleusa's warp id. The placeholder rooms (registered with `new_map.py`, group `gMapGroup_IndoorEleusa`, Akti's Fisher's house copied) warp back from their mat to the first id of their door.

| Warp id | Where (x, y) | To |
|---|---|---|
| 0 | (10, 23) | `MAP_ELEUSA_VILLAGE_ASCLEPEION` |
| 1 | (17, 23) | `MAP_ELEUSA_VILLAGE_AGORA` |
| 2 | (38, 23) | `MAP_ELEUSA_VILLAGE_HOUSE_OF_KELEOS` |
| 3, 4 | (15, 17), (16, 17), barn doors | `MAP_ELEUSA_VILLAGE_GRANARY_HOUSE` |
| 5 | (24, 30) | `MAP_ELEUSA_VILLAGE_POETS_HOUSE` (Euphorion) |
| 6, 7 | (31, 30), (32, 30), barn doors | `MAP_ELEUSA_VILLAGE_FARMHOUSE` (Dysaules) |
| 8 | (25, 11) | `MAP_ELEUSA_VILLAGE_TEMPLE_OF_DEMETER` (its warp 0, the stair) |
| 9, 10 | (31, 8), (32, 8), the Ploutonion's bronze gate | `MAP_ELEUSA_SANCTUM_B1F` (shut until `FLAG_ICHOR_SANCTUM_OPEN`) |

The Telesterion's warps: 0–2 the stair (13, 12, 14 on row 26) to Eleusa's warp 8; 3 the Anaktoron's door (13, 13) to `MAP_ELEUSA_SANCTUM_B1F`, shut until `FLAG_ICHOR_SANCTUM_OPEN`. `MAP_ELEUSA_SANCTUM_B1F`, `B2F` and `B3F` are registered as placeholders (SCRIPT.md calls them `MAP_ELEUSA_MYSTERY_SANCTUM_*`; the brief named them `MAP_ELEUSA_SANCTUM_*`, so these are the ids).

**Flags claimed** (bank 0x080–0x085, vanilla 0x2A0–0x2A2): `FLAG_ICHOR_ITEM_ELEUSA_SUPER_POTION`, `FLAG_ICHOR_ITEM_ELEUSA_AWAKENING`, `FLAG_ICHOR_SANCTUM_OPEN`, `FLAG_ICHOR_LESSER_MYSTERIES_DONE`, `FLAG_ICHOR_MET_DOSO`, `FLAG_ICHOR_HIDE_CHLOE_TELESTERION`; `FLAG_ICHOR_HIDDEN_ELEUSA_HONEY`, `FLAG_ICHOR_HIDDEN_ELEUSA_POMEG_BERRY`, `FLAG_ICHOR_HIDDEN_ELEUSA_BRONZE_OBOL`.

**Braziers.** The Telesterion's four season braziers use `FLAG_ICHOR_BRAZIERS_START + 0x10` (Autumn), `+ 0x11` (Winter), `+ 0x12` (Spring), `+ 0x13` (Summer). The block `+ 0x14`–`+ 0x1F` is left for the sanctum's four and Eleusa's procession torches. Ask before using it for anything else.

## Flags claimed for batch 1

Claimed from this session's range (0x200–0x2FF) in `include/constants/flags.h`. Agents don't claim flags: ask the session if you need another one.

| Flag | Use |
|---|---|
| `FLAG_ICHOR_HALIA_SECOND_LOOK`, `FLAG_ICHOR_HIDE_MOM_HOME`, `FLAG_ICHOR_HIDE_MOM_AKTI`, `FLAG_ICHOR_HIDE_KLEON_AKTI_DOOR`, `FLAG_ICHOR_WINDS_TURNED`, `FLAG_ICHOR_MOM_HARBOR`, `FLAG_ICHOR_BOARDED_EUPLOIA` | beats 9A–9B (Elaia, Akti) |
| `FLAG_ICHOR_BATTLED_ALETHEA_DECK`, `FLAG_ICHOR_SAVED_HALCYON_NEST`, `FLAG_ICHOR_GOT_HALCYLING`, `FLAG_ICHOR_HIDE_HALCYON_NEST`, `FLAG_ICHOR_HIDE_DECK_HARPECK`, `FLAG_ICHOR_NO_RUNNING` | beat 10 |
| `FLAG_ICHOR_ARRIVED_AEGINA`, `FLAG_ICHOR_VISITED_AEGINA`, `FLAG_ICHOR_HIDE_AEGINA_CAST`, `FLAG_ICHOR_AEGINA_NIGHT` | beat 10B |
| `FLAG_ICHOR_CROSSING_DONE` | beat 10C; also hides the voyage cast on deck afterwards |
| `FLAG_ICHOR_FERRY_TO_EMPORION` | the ferry's destination (clear: Akti) |
| `FLAG_ICHOR_FERRY_TO_AEGINA` | Aigina's ferry stop and north gate are open: world-act2 sets it at its Act II beat 46. Aigina Town's gatekeeper reads it. |
| `FLAG_ICHOR_TRADED_CHELONET`, `FLAG_ICHOR_GOT_BLACK_BELT` | Aegina's homes |
| `FLAG_ICHOR_ITEM_DECK_SUPER_POTION`, `FLAG_ICHOR_HIDDEN_DECK_HEART_SCALE`, `FLAG_ICHOR_ITEM_HOLD_POTION` | the trireme's items |
| `FLAG_ICHOR_HIDDEN_AEGINA_BIG_PEARL`, `FLAG_ICHOR_HIDDEN_AEGINA_STARDUST` | Aegina Town's hidden items |
| `FLAG_ICHOR_HERM_AEGINA`, `FLAG_ICHOR_ITEM_APHAIA_SILVER_POWDER`, `FLAG_ICHOR_ITEM_APHAIA_SUPER_POTION`, `FLAG_ICHOR_ITEM_APHAIA_PRETTY_FEATHER`, `FLAG_ICHOR_ITEM_OROS_WINE` | the detour |

IchorSave's flag bank is on main. From batch 2 on, new flags are bank flags in this session's offsets (`tools/ichor/claim_ranges.md`: bankflag 0x000–0x0FF, dailyflag 0x40–0x4B, bankvar 0–5), claimed with `python3 tools/ichor/claim.py --range LO-HI bankflag FLAG_ICHOR_... "comment"`. Hidden items still need vanilla flags at or above `FLAG_HIDDEN_ITEMS_START`, from 0x200–0x2FF. Sub-ranges handed to agents:

| Who | bankflag | vanilla (hidden items) |
|---|---|---|
| this session | 0x000–0x07F | 0x298–0x29F |
| Eleusa agent | 0x080–0x0BF | 0x2A0–0x2BB |
| Emporion city agent | 0x0C0–0x0DF | 0x28A–0x293 |
| Emporion interiors agent | 0x0E0–0x0EF | 0x294–0x297 |
| Temple of Hermes agent | 0x0F0–0x0FF | — |

## Stubs until other sessions land

Each stub is marked in the code with its tag, so it can be found and replaced with `grep -rn ICHOR_STUB_`.

- **`ICHOR_STUB_AETHOS_DEX`: species.** `include/constants/ichor_species_stubs.h` maps every Aethos name SCRIPT.md uses (`SPECIES_HARPECK`, `SPECIES_HALCYLING`, …) to a vanilla stand-in of the same type. Write the Aethos names everywhere: scripts, parties, encounter tables, `OBJ_EVENT_GFX_SPECIES(HARPECK)`. Don't write `Ability:` lines in parties while the stand-ins are in place; they are noted in comments for the dex.
- **`ICHOR_STUB_TRAINER_IDS`: trainer ids.** Only 11 ids are free until the Hoenn cut. Parties are written now in `design/phase2/trainers_batch1.party` and registered when this session's range appears in `tools/ichor/claim_ranges.md`. Scripts use the final names (`TRAINER_ICHOR_PHORMION`); `include/constants/ichor_trainer_stubs.h` defines them until then.
- **`ICHOR_STUB_HERM`, `ICHOR_STUB_RITES`, `ICHOR_STUB_DIG`: herms, altars, dig spots.** The engine session is building them (SYSTEMS.md §3–§5). Until its API is on main, a herm is a bg event that offers to anoint it ("Somewhere, Hermes makes a note.") and sets its flag; an altar shows its SCRIPT.md text and says nothing about prayer mechanics; a fixed dig spot is a bg event with the turned-earth text and no reward. Write each as its own small script with the tag in a comment.
- **`ICHOR_STUB_DARKNESS`: the Torch, braziers and lit zones** (ENGINE_API.md §2). The Telesterion is a dark map (`requires_flash`). Until the engine's darkness lands, its ON_TRANSITION sets flash level 3 (the Torch's radius, SCRIPT.md Part 5); its braziers call a local `StubBrazier` (ask, light, set the flag) in place of `EventScript_IchorBrazier`, and its lit-zone triggers call `StubEnterLitZone` and `LeaveLitZone` (flash 0 inside a lit quarter, 3 outside) in place of `EventScript_IchorEnterLitZone` / `_LeaveLitZone`. Dousing, and so the glowing seeds and chalk, waits for the engine.
- **`ICHOR_STUB_OFFERINGS`: Olive Oil, Wine, Barley Cake, Frankincense.** New items from the engine session. Until then, Wine on Mount Oros is an item ball of `ITEM_BERRY_JUICE` with the tag.
- **Music** (Act I's songs are on main; `design/MUSIC.md` has the rules): the deck and hold `MUS_ICHOR_TRIREME`; Aigina Town `MUS_ICHOR_AKTI` (island harbors share it); mainland routes `MUS_ICHOR_ROAD` (its night form switches in by itself); Emporion `MUS_ICHOR_EMPORION`; the Temple of Hermes `MUS_ICHOR_TEMPLE_HERMES`; Eleusa `MUS_ICHOR_ELEUSA`; the Telesterion and the Mysteries `MUS_ICHOR_TEMPLE_DEMETER`; Hecate's Hollow and any cave `MUS_ICHOR_HOLLOW`; Hyperion `MUS_ICHOR_BATTLE_ADMIN`; Daphne's revelation `MUS_ICHOR_REVELATION`; Aigina's interior (Act II) `MUS_ICHOR_ROAD`. Still stubbed (`ICHOR_STUB_MUSIC`): the inn's night by the hearth plays `MUS_ICHOR_ASCLEPEION`, and the Kleon's-stroke march variant of the trireme song doesn't exist. **Never** use Elpis's lullaby (627, 628) in Act I.
- **`ICHOR_STUB_EMPORION`: the end of batch 1.** Beat 10C calls `Ichor_EventScript_EuploiaMakesEmporion` (in `data/scripts/ichor_act1.pory`). Until Emporion exists it plays a short card and leaves the player on deck with the ferry running, so Akti and Aegina stay reachable.

## Rulings that change SCRIPT.md's tables

- **No random early-evolved wild encounters** (director, 2026-11-14, `design/BALANCE.md`; the dex team's c0c5aeb27f). Dropped: Hoplomex at 1% on the Aegina detour (its slots are Ergant 16 instead), and Korantha, Stachypter and Plouteras at 22 around Eleusa (batch 4). Kept as story rewards: the augury statics (Harpelle 17, Korantha or Persenyx 22) and the Hoplomex on Aiakides's team.
- **Placements the dex adopted, built as scripted:** Lykopup (static, Lv 20) at Hecate's Hollow; Raknit (static, Lv 20) in the web chamber; Obolorn at 1% at night on Route 2's tombs (Lv 15–20); Pebblith on the Halai cliffs (Lv 10–16); Ergant on Aegina's ant hills (Lv 12–16); Spalunk is Alethea's partner only, never wild on Kalliste.
- **Every other Phase 2 area** takes its species and levels from each species' `habitat` field in `design/dex/species/*.yaml` (branch `claude/aethos-dex-a7c73a`).

## Scene helpers this session provides

- `special(Ichor_SetHoursOverride)` with `VAR_0x8004` = an hour (1–23) forces the day-night tint; 0 hands it back to the clock. The voyage night: 22 from the night leg until the inn's fade, re-applied in Aegina Town's and the inn's `MAP_SCRIPT_ON_TRANSITION` while `FLAG_ICHOR_ARRIVED_AEGINA` is set and `FLAG_ICHOR_AEGINA_NIGHT` is clear (the override isn't saved).
- `FLAG_ICHOR_NO_RUNNING` makes a wild battle unescapable (`WE_FLAG_NO_RUNNING`). `FLAG_ICHOR_NO_WHITEOUT` now also covers scripted wild battles (`src/battle_setup.c`), so a lost snatcher fight carries the scene on. Heal the party quietly after a lost fight.
- The ferry (`Ichor_EventScript_FerryQuay`, `Ichor_EventScript_FerryDeck` in `data/scripts/ichor_act1.pory`): call them from Nausikles's object on each quay and on deck once `FLAG_ICHOR_CROSSING_DONE` is set.

## Ownership

Each agent touches only its own files. Shared registration files (`layouts.json`, the tileset tables in `src/data/tilesets/`, `include/constants/event_objects.h` and the sprite tables) take small appended entries; this session resolves merge conflicts in them.

| Owner | Files |
|---|---|
| this session | `design/phase2/BUILD.md`, flags, `data/scripts/ichor_act1.pory`, `src/ichor_scene.c`, the stub headers, `src/data/trainers.party`, `src/data/wild_encounters.json`, `src/data/trade.h`, Elaia's and Akti's scripts and objects (beats 9A–9B), the playthrough test |
| trireme agent | `tools/ichor/art/trireme_*.py`, `data/tilesets/secondary/trireme/`, `tools/ichor/maps/trireme.py`, the deck and hold layouts, `map.json` and `scripts.pory`, `design/phase2/TILES_trireme.md` |
| Aegina agent | `tools/ichor/art/aegina_*.py`, `data/tilesets/secondary/aegina/`, `tools/ichor/maps/aegina.py`, Aegina Town's layout, `map.json` and `scripts.pory`, `design/phase2/TILES_aegina.md` |
| interiors agent | `tools/ichor/art/ergasteria_*.py`, `data/tilesets/secondary/ergasteria/`, `tools/ichor/maps/aegina_homes.py`, the three homes' layouts, `map.json` and `scripts.pory`, `design/phase2/ROOMS_ergasteria.md` |
| detour agent | `tools/ichor/maps/aegina_detour.py`, the three detour maps' layouts, `map.json` and `scripts.pory` |
| sprites agent | new files under `graphics/trainers/`, `graphics/object_events/pics/`, their tables, `tools/ichor/art/sprites_phase2*.py`, `design/phase2/SPRITES.md` |

## Done means (per map)

- `make` is green and `tools/ichor/smoke_test.sh` passes.
- The map follows MAP_DESIGN.md: forced grass on routes, trainer checkpoints, every dead end pays, every house a home, every interior unique, seam strips from the primary only, signs at ends and forks.
- **At least three render-and-critique passes**, each written down (what was wrong, what changed), and in-game screenshots of every scene, looked at.
- Every line of text measured with `tools/ichor/text_width.py`; the speaker's name goes in the name box (`setspeaker`), as in the slice.
- A render at 2x in `design/phase2/img/<map>.png` for the director to forward to the user.
