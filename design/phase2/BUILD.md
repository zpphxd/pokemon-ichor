# Phase 2 build plan: Act I on the mainland

Owner: the world-act1 session (branch `claude/world-act1-6d11b7`). This is the working plan for building `design/phase2/SCRIPT.md` as playable content. SCRIPT.md says what happens; this file says who builds which file, with which ids, and what is stubbed until another session lands.

Read first, in this order: `CLAUDE.md`, `design/MAP_DESIGN.md`, this file, the SCRIPT.md beats and Part 2 rosters for your maps, `design/TERMS.md`, then the slice's model for your kind of work (below).

## Batches

| # | Batch | Status |
|---|---|---|
| 1 | The voyage and Aegina: beats 9A–10C, the *Euploia*, Aegina Town and its three homes, the Aegina detour | in progress |
| 2 | Emporion and the Temple of Hermes: beats 11–16 | waits for gTileset_Emporion (director) |
| 3 | The Sacred Way and Hecate's Hollow: beats 17–19, Routes 2–4, Thria | |
| 4 | Eleusa and the Temple of Demeter: beats 20–22 | waits for gTileset_Eleusa (director) |
| 5 | The revelation: beats 23–25, the sanctum, Return to Kalliste | |

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
| `MAP_AEGINA_APHAIA_ROAD` | 40×24 | aethos + **aegina** | route | detour agent (after the Aegina tileset) |
| `MAP_AEGINA_TEMPLE_OF_APHAIA` | 24×20 | aethos + **aegina** | route | detour agent |
| `MAP_AEGINA_MOUNT_OROS` | 16×16 | aethos + **aegina** | route | detour agent |

**Tilesets.**
- `trireme`: SCRIPT.md Part 10. Deck planks, the mast and sail (furled, full, sagging), the bronze ram and the painted eye, steering oars, the stern's curl, rope coils, lashed amphorae, the hatch, the rail with gaps where the player can fish over the side; the hold's three banks of benches with oars. The sea round the deck is aethos's animated sea.
- `aegina`: one secondary for all four Aegina outdoor maps, so their seams need no aethos-only strip. Akti's harbor pieces (copy them from `tools/ichor/art/akti_*.py`) plus the round mole, Kolona's column on its headland, the inn and mint fronts, Aiakides's house, ant hills, pistachio trees, dry grass and scrub, the gate, the Temple of Aphaia's Doric front on its pine hill, Zeus's summit altar, a herm (aethos has one at 0x01B).
- `ergasteria` ("workshops"): Phase 2's working interiors. `oikia` is full and `civic` has 48 tiles left, so this new secondary on the `oikos` primary carries the furniture those rooms share (copied from oikia/civic as needed) plus the new pieces. Batch 1 draws Aegina's inn (courtyard cistern, wooden guest gallery, turtle mosaic, hearth), the mint (two anvils, coin dies on a rack, a blank-heating brazier, scales, a turtle-stamped chest) and Aiakides's house (shield and spear trophy, clay-ant shrine, an anthill in a pot). Leave room: Emporion's workshops (the forge, the potter's wheel and kiln) are planned for this set in batch 2. Keep under 440 tiles in batch 1.

Every secondary stays at or under 504 tiles; leave 496–511 free where a map uses wide doors (CLAUDE.md).

## Warps, connections and seams (batch 1)

| From | To | How |
|---|---|---|
| Akti quay, the gangplank | the deck | scripted warp (beat 9B, and the ferry) |
| the deck, the hatch | the hold | warp both ways |
| the deck | Aegina's quay | scripted warp (end of beat 10, and the ferry) |
| Aegina's inn, after the night | the deck | scripted warp (beat 10C) |
| Aegina Town doors | inn, mint, Aiakides's house | warps both ways |
| Aegina Town, north gate | the Aphaia Road | map connection, up. The Aegina agent picks the gate columns and records them here; the detour agent matches them. |
| the Aphaia Road | the Temple of Aphaia, Mount Oros | the detour agent's choice (connections or warps), recorded here |

Record the warp ids and the arrival tiles you choose in this table, so the scripted warps in other maps can use them.

| Map | Arrival tile (x, y) | For |
|---|---|---|
| `MAP_TRIREME_EUPLOIA_DECK` | *(trireme agent fills in)* | boarding from a quay |
| `MAP_AEGINA_TOWN` | *(Aegina agent fills in)* | stepping off the *Euploia* |
| `MAP_AKTI_TOWN` | (9, 10), the quay by the gangplank | stepping off the ferry |

## Flags claimed for batch 1

Claimed from this session's range (0x200–0x2FF) in `include/constants/flags.h`. Agents don't claim flags: ask the session if you need another one.

| Flag | Use |
|---|---|
| `FLAG_ICHOR_HALIA_SECOND_LOOK`, `FLAG_ICHOR_HIDE_MOM_HOME`, `FLAG_ICHOR_HIDE_MOM_AKTI`, `FLAG_ICHOR_HIDE_KLEON_AKTI_DOOR`, `FLAG_ICHOR_WINDS_TURNED`, `FLAG_ICHOR_MOM_HARBOR`, `FLAG_ICHOR_BOARDED_EUPLOIA` | beats 9A–9B (Elaia, Akti) |
| `FLAG_ICHOR_BATTLED_ALETHEA_DECK`, `FLAG_ICHOR_SAVED_HALCYON_NEST`, `FLAG_ICHOR_GOT_HALCYLING`, `FLAG_ICHOR_HIDE_HALCYON_NEST`, `FLAG_ICHOR_HIDE_DECK_HARPECK`, `FLAG_ICHOR_NO_RUNNING` | beat 10 |
| `FLAG_ICHOR_ARRIVED_AEGINA`, `FLAG_ICHOR_VISITED_AEGINA`, `FLAG_ICHOR_HIDE_AEGINA_CAST`, `FLAG_ICHOR_AEGINA_NIGHT` | beat 10B |
| `FLAG_ICHOR_CROSSING_DONE` | beat 10C; also hides the voyage cast on deck afterwards |
| `FLAG_ICHOR_FERRY_TO_AEGINA`, `FLAG_ICHOR_FERRY_TO_EMPORION` | the ferry's destination (both clear: Akti) |
| `FLAG_ICHOR_TRADED_CHELONET`, `FLAG_ICHOR_GOT_BLACK_BELT` | Aegina's homes |
| `FLAG_ICHOR_ITEM_DECK_SUPER_POTION`, `FLAG_ICHOR_HIDDEN_DECK_HEART_SCALE`, `FLAG_ICHOR_ITEM_HOLD_POTION` | the trireme's items |
| `FLAG_ICHOR_HIDDEN_AEGINA_BIG_PEARL`, `FLAG_ICHOR_HIDDEN_AEGINA_STARDUST` | Aegina Town's hidden items |
| `FLAG_ICHOR_HERM_AEGINA`, `FLAG_ICHOR_ITEM_APHAIA_SILVER_POWDER`, `FLAG_ICHOR_ITEM_APHAIA_SUPER_POTION`, `FLAG_ICHOR_ITEM_APHAIA_PRETTY_FEATHER`, `FLAG_ICHOR_ITEM_OROS_WINE` | the detour |

The engine session is adding a 2,048-flag bank in IchorSave (`design/ENGINE_API.md` on its branch). Later batches will claim there; batch 1's vanilla flags can move once it lands.

## Stubs until other sessions land

Each stub is marked in the code with its tag, so it can be found and replaced with `grep -rn ICHOR_STUB_`.

- **`ICHOR_STUB_AETHOS_DEX`: species.** `include/constants/ichor_species_stubs.h` maps every Aethos name SCRIPT.md uses (`SPECIES_HARPECK`, `SPECIES_HALCYLING`, …) to a vanilla stand-in of the same type. Write the Aethos names everywhere: scripts, parties, encounter tables, `OBJ_EVENT_GFX_SPECIES(HARPECK)`. Don't write `Ability:` lines in parties while the stand-ins are in place; they are noted in comments for the dex.
- **`ICHOR_STUB_TRAINER_IDS`: trainer ids.** Only 11 ids are free until the Hoenn cut. Parties are written now in `design/phase2/trainers_batch1.party` and registered when this session's range appears in `tools/ichor/claim_ranges.md`. Scripts use the final names (`TRAINER_ICHOR_PHORMION`); `include/constants/ichor_trainer_stubs.h` defines them until then.
- **`ICHOR_STUB_HERM`, `ICHOR_STUB_RITES`, `ICHOR_STUB_DIG`: herms, altars, dig spots.** The engine session is building them (SYSTEMS.md §3–§5). Until its API is on main, a herm is a bg event that offers to anoint it ("Somewhere, Hermes makes a note.") and sets its flag; an altar shows its SCRIPT.md text and says nothing about prayer mechanics; a fixed dig spot is a bg event with the turned-earth text and no reward. Write each as its own small script with the tag in a comment.
- **`ICHOR_STUB_OFFERINGS`: Olive Oil, Wine, Barley Cake, Frankincense.** New items from the engine session. Until then, Wine on Mount Oros is an item ball of `ITEM_BERRY_JUICE` with the tag.
- **`ICHOR_STUB_MUSIC`: songs.** Use these until the Phase 2 songs exist: the deck `MUS_ICHOR_AKTI` (for `MUS_ICHOR_TRIREME`), Aegina Town `MUS_ICHOR_AKTI` (final), the inn's night `MUS_ICHOR_ASCLEPEION` (for `MUS_ICHOR_HEARTH_NIGHT`), the detour `MUS_ICHOR_ROUTE1` (for `MUS_ICHOR_HALAI`).
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
