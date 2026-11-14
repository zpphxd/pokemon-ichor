# Phase 1 QA: the Kalliste slice

The first pass was on 2026-11-14 against main at `4108e52c12`. The second pass, below, re-checked every issue on main at `726eb794d6`, which adds:
- Route 1 and Kronion Hill rebuilt on gTileset_Agros.
- The world screens and the codex Pokédex.
- The QA fixes.
- Elaia's new seam with Route 1, which moves everything in the village four rows south.
- Glykera's bakery, the new house west of the square.

Everything here was found by playing the slice with key presses in the headless runner, or by the static map audit. Every issue has a screenshot in `img/qa/` and a way to reproduce it with the tools below.

## Status on main at `726eb794d6`

| Severity | Open | Fixed since the first pass |
|---|---|---|
| Blocker | 0 | B1, B2 |
| Major | 1: M2 | M1; M3 mostly (what's left is m7) |
| Minor | 3: m1, m7 (new), m8 (new) | m2, m3, m4, m5, m6 |
| Polish | 11: P1, P2, P3, P5, P6, P7, P8, P9, P11 (new), P12 (new), P13 (new) | P4, P10 |

**The full playthrough plays the whole slice on current main.** It runs from the title to "Thank you for playing" with no workarounds: about 107k frames and 17 battles.
- **It exits non-zero on one open bug, M2.** M2's check is the only one that fails. Its fix is a one-liner (see M2). It isn't applied here, because game content belongs to the Akti owner.
- **m1 is logged as a FINDING,** a design-level item that doesn't fail the run.
- **Side checks:** every one is clean except the M2 check.

**The tests no longer name a coordinate.**
- People, trainers, items, signs, hidden items, story triggers and warps are found on the live map by the script they run, or the flag they set. The tests read them from the ROM's event tables.
- Routes are pathfound on the live grid. People off screen block the path at their map positions.
- Route 1's things are visited nearest-first. What the flock walls off waits for the second pass, after the hill.
- So a moved NPC, item or trainer never breaks the run. One that is removed or renamed fails with its script or flag name.
- Elaia's new seam moved every person, sign and door in the village four rows. The tests passed on it unchanged.

**What is clean on current main.** These all work:
- Every beat plays in order, and every story flag and var lands where SCRIPT.md says.
- Each map plays its own music, including the Agora's own theme. The battle music is right for Kleon, Ione, the Titanborn, the route trainers, the acolytes and wild Pokémon.
- All 12 trainers are beaten once, and none battles twice.
- Every gift and item gives its item once, and asking again gives nothing.
- The game saves in the Asclepeion, resets and continues with the party and flags intact.
- Nothing replays after leaving and re-entering the Akademia, Kronion Hill or Akti's south gate.
- Whiteouts:
  - Whiting out before the first Asclepeion heal (including in Akti) wakes you at home with Mom.
  - Whiting out after the first heal wakes you in the Asclepeion, with no softlock.
- Losing to Petros mid-scene, or to Ione, and coming back replays the battle correctly.
- The torch goes out after a whiteout.
- 255 distinct messages were shown, battle text included. None is wider than the box, none runs to three lines, and none has a Hoenn word or a dictionary typo.
- No warp lands on a solid tile, and no item is out of reach in the static audit.
- **The rebuilt Route 1 and Kronion Hill:**
  - Every trainer, item, gift and sign is reachable. Agis, the Route 1 Potion and the north herm sit behind the flock and are reached after the hill.
  - The summit scene, both grunt battles, the tablet's new line, the Augur's Eye and the dark stair's line ("Stone steps go down into the dark...") all play.
  - The olive-tip cells that the audit lists as mixed collision are open everywhere except along a hedgerow, which is a deliberate barrier.
- **Glykera's bakery:**
  - The comb from Mom's hives buys two honey cakes, once (`FLAG_ICHOR_GOT_GLYKERA_CAKES`). Glykera takes the Honey, and asking again gives nothing.
  - Kimon's trade offer can be turned down.
  - Every sign reads except the honey shelf (P13).
  - Kimon's Finizen trade and his pearls after the badge are played by Elaia's own `elaia_opening.lua`, not here.

## How to rerun

```bash
make -j$(sysctl -n hw.ncpu)
tools/ichor/tests/slice_playthrough.sh            # the gate: exits non-zero on any failure
SLICE_WORKAROUNDS=1 tools/ichor/tests/slice_playthrough.sh   # play past a known softlock
tools/ichor/tests/slice_sidechecks.sh             # whiteouts, re-entry, losses, menus (needs a full run's save states;
                                                  #   if a blocker ever returns, run the playthrough with SLICE_WORKAROUNDS=1 first)
tools/ichor/tests/slice_gallery.sh                # the look-review gallery, img/gallery/
python3 tools/ichor/tests/slice_map_audit.py      # static: reachability, warps, edges, mixed collision
python3 tools/ichor/tests/slice_grid.py AktiTown  # one map's walk grid (collision, elevation, events)
```

- **Resuming.** `SLICE_FROM=<beat>`, for example `07_temple`, resumes from that beat's save state in `build/slice/states/` for quick iteration.
- **Logs.** `build/slice/run.log` has every check. Its `TEXT` lines are decoded into `build/slice/text.txt`.
- **The one assist.** After the starter screen, the starter's experience is set to level 100's. Its moves, met level and species are untouched, and every battle is fought with button presses.

**The look-review gallery** is in `img/gallery/`, one 2x contact sheet per section. Each frame is captioned with its beat:

| Sheets | Contents |
|---|---|
| `01_opening` to `10_ending` | the beats in order. Long sections are split into `_01` and `_02` sheets. |
| `11_battles_*` | every battle |
| `12_menus_*` | the start menu and its screens, after the slice |
| `13_maps` | each of the 13 maps as the player first sees it |

Frames are picked by the names the playthrough gives them, so a rerun after an art pass gives comparable sheets. `GALLERY_ALL=<dir>` also writes every screenshot of the run, in order.

---

## Blockers

### B1. The Asclepeion healer softlocks the game after every heal (FIXED)
- **Status:** fixed on `726eb794d6`. Verified: the heal returns control, and the save, reset and continue that follow it work.
- **Area:** sprites (cause). Akti owns the interim script fix.
- **Repro:**
  1. In Akti, enter the Asclepeion.
  2. Talk to the healer across the counter and answer YES.
  3. After "There. Whole and well, by Asclepius's grace." the arrow stays up. No button does anything, ever.
- **Screenshot:** `img/qa/B1_healer_softlock.png`
- **Cause:**
  - The script ends with `applymovement(VAR_0x800B, Movement_PkmnCenterNurse_Bow)` at `data/maps/AktiTown_Asclepeion/scripts.pory:53`.
  - `OBJ_EVENT_GFX_ICHOR_HEALER` uses `sAnimTable_Standard`, which has no `ANIM_NURSE_BOW`. The bow's `MovementAction_WaitSpriteAnim` never ends, so `waitmovement` never returns. The runner shows the script stuck in `WaitForMovementFinish`.
- **Suggested fix:**
  - **Proper fix (sprites):** give `gObjectEventGraphicsInfo_IchorHealer` `.anims = sAnimTable_Nurse`, and add a tenth "bow" frame to `sPicTable_IchorHealer`. `sAnim_NurseBow` shows frame 9. This also fixes B2.
  - **Interim one-liner (Akti):**
    ```diff
    -    applymovement(VAR_0x800B, Movement_PkmnCenterNurse_Bow)
    +    applymovement(VAR_0x800B, Common_Movement_FaceDown)
    ```
- **Test note:** `tools/ichor/tests/akti_town.lua` passes with this bug. It never checks that the player gets control back, and its own `13_healer_done_02.png` shows the stuck box.

### B2. Whiting out anywhere after reaching Akti softlocks in the Asclepeion (FIXED)
- **Status:** fixed on `726eb794d6`. Verified by the side checks: whiting out in Akti, in the Temple and after the end, and losing to Ione, all wake you in the Asclepeion with control.
- **Area:** sprites (same cause as B1). The engine owns the interim fix.
- **Repro:** after arriving in Akti, lose any battle, or faint to a wild Pokémon. Losing to Ione does it.
  1. You wake in the Asclepeion: "Easy, now. Let's tend your Pokémon first."
  2. The heal plays, then "...Go in health."
  3. The game hangs.
- **Screenshots:** `img/qa/B2_whiteout_softlock.png` and `img/qa/B2_lose_to_ione_softlock.png`
- **Cause:** `EventScript_AfterWhiteOutHeal` (`data/event_scripts.s:1075`) bows the respawn NPC with `Movement_PkmnCenterNurse_Bow`. For Akti that NPC is the Ichor healer, so it hangs exactly as in B1.
- **Suggested fix:** the sprite fix in B1 covers this. The interim alternative is the same one-line swap at `data/event_scripts.s:1075`, but that line is shared with Hoenn's centers.

## Major

### M1. The Relic Copper in Elaia's well can be taken again and again (FIXED)
- **Status:** fixed on `726eb794d6`. Verified: one Relic Copper, a second look gives nothing, and the kid stays put.
- **Area:** Elaia
- **Repro:** read the well at (23,18) from (23,17): "found one Relic Copper!" Read it again: another one. It repeats forever, and each one sells for money.
- **Screenshot:** `img/qa/M1_relic_copper_again.png`, the second pickup
- **Cause:**
  - `finditem` leaves `VAR_RESULT` as `pyramid_getlocation`'s answer, not TRUE, so `FLAG_ICHOR_GOT_ELAIA_RELIC_COPPER` is never set (`data/maps/ElaiaVillage/scripts.pory:565`).
  - `finditem` also runs `removeobject VAR_LAST_TALKED`, which is meant for item balls, not signs.
- **Suggested fix:** `giveitem` sets `VAR_RESULT` and removes no one.
  ```diff
  -        finditem(ITEM_RELIC_COPPER)
  +        giveitem(ITEM_RELIC_COPPER)
  ```

### M2. A trip indoors in the middle of the ending breaks it, and part 1 replays (OPEN)
- **Status:** still open on `726eb794d6`. The playthrough logs it right after part 1 (the flag is still set), and the `ending_after_leaving_akti` side check reproduces it.
- **Area:** Akti
- **Repro:**
  1. Win the Hearth Laurel and step out of the Temple. Part 1 plays: Alethea runs in and heads for the quay.
  2. Before reaching the quay, enter any building (the Asclepeion, say) and come back out.
  3. Alethea is gone from the quay, and walking onto it starts nothing.
  4. Stepping in front of the Temple door plays part 1 again from "THEO! You did it!"
- **Screenshots:** `img/qa/M2_quay_after_trip_indoors.png` and `img/qa/M2_part1_replays.png`
- **Cause:**
  - In `AktiTown_EventScript_HarborPart1`, `removeobject(LOCALID_AKTI_ALETHEA)` sets `FLAG_ICHOR_HIDE_ALETHEA_AKTI`, and `addobject` doesn't clear it.
  - So on the next map load, ON_TRANSITION sees the flag and re-arms part 1 instead of part 2. The playthrough flags it right after part 1, with the flag still set.
- **Suggested fix:** in `data/maps/AktiTown/scripts.pory`, around line 155:
  ```diff
       removeobject(LOCALID_AKTI_ALETHEA)
       setobjectxyperm(LOCALID_AKTI_ALETHEA, 7, 10)
  +    clearflag(FLAG_ICHOR_HIDE_ALETHEA_AKTI)
       addobject(LOCALID_AKTI_ALETHEA)
  ```
  This hasn't been applied or tested here, because game content is out of QA's scope. After the fix, `tools/ichor/tests/slice_playthrough.sh` and the `ending_after_leaving_akti` side check should both pass.

### M3. The Pokédex is Hoenn's regional dex, and the slice's Pokémon never appear in it (MOSTLY FIXED)
- **Status:** mostly fixed on `726eb794d6`. The codex lists by national number, Snivy is No0495, and POKéDEX shows 1 on the CONTINUE panel and the card. The regional counts are still wrong: see m7.
- **Area:** engine and UI
- **Repro:** after the starter, open START, then POKéDEX.
  - The list shows No001–No005 blank, with SEEN 3 and OWN 0 while you hold a Snivy. The 3 seen are Geodude, Nosepass and Machop, which are Hoenn-dex species.
  - The CONTINUE panel and the Trainer Card also show POKéDEX 0.
  - Snivy's summary screen numbers it "No000".
- **Screenshot:** `img/qa/M3_pokedex_hoenn.png`
- **Cause:** a new game starts in the Hoenn regional dex mode. Snivy, Smoliv, Wooloo and nearly every slice species are not in the Hoenn dex.
- **Suggested fix (engine):** either build the Aethos regional order, or as an interim enable the National Dex in `NewGameInitData`. The Pokédex screen is also still Hoenn's green art (see P10).

## Minor

### m1. Kleon blocks the only way to the quay's west end, and its Potion, until the ending (OPEN)
- **Status:** still open on `726eb794d6`. The playthrough now logs it as a FINDING, a design call that doesn't fail the run, and collects the Potion after the ending.
- **Area:** Akti
- **Repro:**
  - Before the badge, Kleon stands at (5,10), the one tile between the town and the quay's west pocket: the crates, the item ball at (2,10) and the pier at rows 4–6.
  - The Potion is visible but out of reach until Kleon leaves in the ending. `tools/ichor/tests/slice_grid.py AktiTown` shows the pocket: (4,9) is solid, and (4,10) leads only to (5,10).
- **Screenshot:** `img/qa/m1_kleon_blocks_quay.png`. The ball is just left of Kleon.
- **Suggested fix:** open (4,9) on the map, or move the ball out of the pocket. Moving Kleon would change the part 2 staging.

### m2. Akti becomes the respawn point on arrival, not at the first heal (FIXED)
- **Status:** fixed on `726eb794d6`. Whiting out in Akti before the first heal wakes you at home.
- **Area:** Akti
- **Repro:** arrive in Akti (Diktys's welcome) and white out before entering the Asclepeion. You wake in the Asclepeion, not at home. SCRIPT.md beat 6 says "Run `setrespawn HEAL_LOCATION_AKTI_TOWN` at the Asclepeion's first heal, not here." Until B2 is fixed, this also makes an early loss a softlock.
- **Screenshot:** `img/qa/m2_respawn_before_heal.png`
- **Suggested fix:** delete `setrespawn(HEAL_LOCATION_AKTI_TOWN)` from `AktiTown_EventScript_Arrival` (`data/maps/AktiTown/scripts.pory:75`). The Asclepeion's ON_TRANSITION already sets it when you walk in.

### m3. The Agora plays Akti's theme; its own theme is never heard (FIXED)
- **Status:** fixed on `726eb794d6`. The Agora plays `mus_ichor_agora`, and the playthrough checks it.
- **Area:** Akti (music)
- **Repro:** enter the Agora. The BGM is `mus_ichor_akti`. `MUS_ICHOR_AGORA` is composed and registered, but no map uses it.
- **Screenshot:** `img/qa/m3_agora_music.png`
- **Suggested fix:** in `data/maps/AktiTown_Agora/map.json`:
  ```diff
  -  "music": "MUS_ICHOR_AKTI",
  +  "music": "MUS_ICHOR_AGORA",
  ```

### m4. The starter screen is still Professor Birch's bag (FIXED)
- **Status:** fixed on `726eb794d6`. The starters sit in three kraters on Daphne's table. See `img/gallery/04_akademia.png`.
- **Area:** UI and sprites
- **Repro:** at the Akademia, after Daphne's question, the starter screen shows Birch's satchel on grass, with "Fire Mouse POKéMON" in caps. The box beside it says "Three kraters, three Pokémon." The user sees this in the look review.
- **Screenshot:** `img/qa/m4_starter_bag.png`
- **Suggested fix:** the planned repaint of the bag as three kraters (SCRIPT.md beat 3).

### m5. The Trainer Card says BADGES and shows Hoenn's Stone Badge (FIXED)
- **Status:** fixed on `726eb794d6`. The card is the kylix, with no BADGES label. See `img/gallery/12_menus_02.png`.
- **Area:** UI
- **Repro:** START, then THEO. The card front reads "BADGES" (TERMS.md: LAURELS). After Ione, slot 1 shows the Stone Badge icon, and the card is the stock green Hoenn design.
- **Screenshot:** `img/qa/m5_trainer_card_badges.png`
- **Suggested fix:** the planned kylix card (ART_PLAN §5), relabelled LAURELS, with laurel icons. The word is drawn in the card's tiles, not in a string.

### m6. The summary screen shows a CONTEST MOVES page (contests are cut) (FIXED)
- **Status:** fixed on `726eb794d6`. The summary screen stops at BATTLE MOVES.
- **Area:** UI
- **Repro:** POKéMON, then Snivy, then SUMMARY, then page right to CONTEST MOVES. It shows TOUGH and COOL condition tags.
- **Screenshot:** `img/qa/m6_contest_moves.png`
- **Suggested fix:** a one-line config change in `include/config/contest.h`:
  ```diff
  -#define C_HIDE_CONTEST_DATA         FALSE
  +#define C_HIDE_CONTEST_DATA         TRUE
  ```

### m7. The codex's AETHOS counts are still Hoenn's regional dex (NEW, OPEN)
- **Status:** new on `726eb794d6`.
- **Area:** engine and UI
- **Repro:** after the slice, open START, then POKéDEX.
  - The panel reads SEEN AETHOS 3 / ALL 23 and OWN AETHOS 0 / ALL 1, with Snivy in the party.
  - The 3 "Aethos" species seen are the ones in Hoenn's dex (Geodude, Nosepass, Machop).
- **Screenshot:** `img/qa/m7_aethos_counts.png`
- **Cause:** `GetHoennPokedexCount` (`src/pokedex.c:4546`) walks `HOENN_DEX_COUNT` through `HoennToNationalOrder`. The label became AETHOS (`DEX_MODE_HOENN` = "AETHOS DEX"), but the list behind it is still Hoenn's.
- **Suggested fix:** an Aethos regional order, as M3 suggested. Until then, hide the AETHOS row so the panel doesn't contradict the party.

### m8. By day, the codex's AREA map says AREA UNKNOWN for every slice Pokémon (NEW, OPEN)
- **Area:** engine (Pokédex area screen)
- **Repro:**
  - In daytime, open POKéDEX, then Ekans (seen on Route 1), then AREA. The new Aethos map reads "AREA UNKNOWN DAY".
  - Route 1, Kronion Hill and Akti define only `_Morning` and `_Night` tables. The game falls back to `_Morning` for day and evening (`OW_TIME_OF_DAY_FALLBACK`), and the playthrough meets Ekans in the daytime grass.
  - Paging the AREA screen to MORNING shows the route.
- **Screenshot:** `img/qa/m8_area_unknown_by_day.png`
- **Cause:** `FindMapsWithMon` (`src/pokedex_area_screen.c:343`) reads `encounterTypes[gAreaTimeOfDay]` with no fallback, while the field uses the fallback.
- **Suggested fix (engine):** when that time's table is empty and `OW_TIME_OF_DAY_DISABLE_FALLBACK` is FALSE, search `encounterTypes[OW_TIME_OF_DAY_FALLBACK]`, as the wild encounter code does.

## Polish

### P1. Daphne's name box stays up over system lines in the Akademia (OPEN)
- **Status:** still open on `726eb794d6`.
- **Area:** Elaia
- **Repro:** the nickname prompt ("Do you want to give a nickname to this Snivy?"), "{PLAYER} received Snivy!" and "{PLAYER} received the Pokédex!" all show the DAPHNE box.
- **Screenshot:** `img/qa/p1_daphne_box_on_prompt.png`
- **Suggested fix:** call `setspeaker(SP_NAME_NONE)` before them, as Kronion Hill does before "received the Augur's Eye!".

### P2. Unnamed NPCs speak without a name box (OPEN)
- **Status:** still open on `726eb794d6`.
- **Area:** text
- **Repro:** these have no name box, though SCRIPT.md gives each a speaker label and named characters get one:
  - the old shepherd at the gate
  - the fishwife and the Lakonian rower
  - the pilgrim and the old woman on the temple steps
  - the carter, the youth on the wall, both olive farmers, and the kids in Elaia and on Akti's pier
- **Screenshot:** `img/qa/p2_no_name_box.png`
- **Suggested fix:** a `setspeaker` with the role (OLD SHEPHERD, FISHWIFE, ...). This is a director call.

### P3. The party menu's prompts still use the old capitals (OPEN)
- **Status:** still open on `726eb794d6`.
- **Area:** text and UI
- **Repro:** POKéMON shows "Choose POKéMON or CANCEL.", and Snivy's menu shows "Do what with this PKMN?" TERMS.md says prose is sentence case.
- **Screenshot:** `img/qa/p3_party_caps.png`

### P4. The naming screen is the stock blue Hoenn screen (FIXED)
- **Status:** fixed on `726eb794d6`. The naming screen is the writing tablet.
- **Area:** UI
- **Repro:** Daphne's speech, then the name.
- **Screenshot:** `img/qa/p4_naming_screen.png`

### P5. The Augur's Eye opens the stock DexNav screen (OPEN)
- **Status:** still open on `726eb794d6`.
- **Area:** UI
- **Repro:** START, then AUGURY. The screen is red and blue, with "R TO REGISTER!".
- **Screenshot:** `img/qa/p5_augury_ui.png`

### P6. The main menu's backdrop is the stock lavender (OPEN)
- **Status:** still open on `726eb794d6`.
- **Area:** UI
- **Repro:** at the title, press A. This applies to the NEW GAME and CONTINUE panels.
- **Screenshot:** `img/qa/p6_main_menu.png`

### P7. Kronion Hill uses Route 1's map section (OPEN)
- **Status:** still open on `726eb794d6`.
- **Area:** Route 1
- **Repro:** the summit's map is `MAPSEC_KALLISTE_ROUTE_1`, so it never gets its own "KRONION HILL" popup or region-map name, though its stele names it.
- **Screenshot:** `img/qa/p7_kronion_hill.png`

### P8. The Titanborn's encounter theme is never heard (OPEN)
- **Status:** still open on `726eb794d6`.
- **Area:** Route 1 (music)
- **Repro:** the summit scene plays the route theme until the battles. `MUS_ICHOR_ENCOUNTER_TITAN` is unused, because the grunts are `trainerbattle_no_intro` and the scene never calls `playbgm`.
- **Suggested fix:** `playbgm(MUS_ICHOR_ENCOUNTER_TITAN, FALSE)` when the grunts turn around.

### P9. Invisible walls around the sacred olive's garden in Elaia (OPEN)
- **Status:** still open on `726eb794d6`.
- **Area:** Elaia
- **Repro:** these cells are drawn as open grass and flowers but are solid (coordinates on the new map, four rows lower than before):
  - (13–16,15–17), around the olive
  - (12,18) and (17,18)
  - (4,24–26), (7,27) and (27,6) at the edges. (4,26) and (7,27) are new with the seam.
- **Screenshot:** `img/qa/p9_elaia_invisible_walls.png` (solid cells boxed in red)
- **Suggested fix:** if the garden is meant to be closed, give it a visible edge.

### P10. The Pokédex screens are Hoenn's green art (FIXED)
- **Status:** fixed on `726eb794d6`. The Pokédex is the codex.
- **Area:** UI
- **Repro:** START, then POKéDEX. The list and the entry screens are stock. See M3 for the dex contents.
- **Screenshot:** `img/qa/M3_pokedex_hoenn.png`

### P11. Akti's goats have lines no one can hear (NEW, OPEN)
- **Area:** Akti
- **Repro:**
  - The two Skiddo at (23,24) and (25,25) run `AktiTown_EventScript_Goat`, but they stand in a pen walled on every side, and its fence isn't a counter.
  - Nothing can be faced to talk to them. Both the static audit and the playthrough ("can't reach goat") show this.
- **Screenshot:** `img/qa/p11_goat_pen.png`
- **Suggested fix:** make one fence cell a counter-type tile so they can be talked to over it, or drop the script.

### P12. The codex entry weighs Pokémon in pounds (NEW, OPEN)
- **Area:** UI and text
- **Repro:** POKéDEX, then any entry. It reads "WT ????.? lbs", the stock imperial unit.
- **Screenshot:** `img/qa/p12_lbs.png`
- **Suggested fix:** a director call: the expansion's metric units, or an in-world measure.

### P13. The honey shelf in Glykera's bakery can't be reached (NEW, OPEN)
- **Area:** Elaia
- **Repro:**
  - `ElaiaVillage_BakersHouse_EventScript_HoneyShelf` is a sign at (0,1), read from (0,2).
  - (0,2) is in a small pocket, (0–1,3–4), and the only way in is (2,4), where Glykera stands facing down.
  - So the shelf, and its line that changes after the cakes, can never be read. The playthrough logs "can't reach honey_shelf", and the static audit agrees.
- **Screenshot:** `img/qa/p13_honey_shelf.png`. The shelf is boxed red, the cut-off pocket yellow and Glykera's tile blue.
- **Suggested fix:** stand Glykera at (0,4) or (1,3), so (2,4) is a way in, or move the shelf's sign to a jar on the open wall.

---

## Notes

**Checked but not filed:**
- Battle backgrounds: each environment matches `BATTLE_BG.md`.
- Item pockets: the Escape Rope sits in KEY ITEMS because it is reusable under the expansion's Gen 8+ rule.
- The expansion's name box carries across `msgbox` calls until `closemessage`, so a missing `setspeaker` between two lines by the same speaker is fine.
- Petros and Amathos walk through the pit's rim (10,9) as they climb out. It's scripted movement and reads as climbing.
- The side checks' `text.txt` marks the two whiteout lines ("THEO hurried back home..." and "THEO hurried to the Asclepeion...") as TALL. That is a false positive: they appear in the full-screen whiteout window, which holds more lines than the text box.

**The static audit's remaining REACH lines are expected:**
- the olive press tile behind the farmer
- a Halia trigger under the festival-goer
- the scroll shelf tile behind Daphne
- Ione and the hearth before the trial opens the dais
- Kronion Hill's pit signs and the grunts, who are inside the pit, which only the scene uses
- Akti's goats (P11) and the two decorative Wingull on the breakwater
- the honey shelf in Glykera's bakery (P13)
- Akti's quay edge (row 3) is solid, while the same tile at the north pier's end is open. It reads as the pier's last step, so it isn't filed.

**For the test suite:** `akti_town.lua` and `akti_harbor_ending.lua` take their screenshots on fixed timings, so they pass through softlocks (B1). `slice_lib.lua`'s `settle()` fails on any script that waits on the same thing for 2400 frames, and the slice tests could share it.
