# Ichor engine API

What the engine gives map and script agents: the state you can read and write, and the specials and scripts you call. Each section names the system's spec in `design/SYSTEMS.md` and the code behind it.

- **Owner:** the engine-systems session. Map agents call these APIs and never change the code behind them. If an API is missing, ask for it.
- **Tests:** every system has a headless check in `tools/ichor/tests/ichor_*.sh`. Run them after any engine change.

## 1. Ichor's save state

All of Ichor's own persistent state lives in **`struct IchorSave`** (`include/ichor_save.h`, `src/ichor_save.c`). It is the first member of SaveBlock3.

| | |
|---|---|
| Size | 1,472 bytes. It was 1,280 until version 4 added the second flag bank at 0x500. SaveBlock3 is now 1,476 of its 1,624 bytes. |
| Version | `ICHOR_SAVE_VERSION` (6). Version 0 means a save from before IchorSave. |
| New game | `Ichor_InitSave()` (from `NewGameInitData`): everything zero, except `version` and `momLosses = 212`. |
| Loading a save | `Ichor_OnSaveLoaded()` (from `LoadGameSave`). A version-0 save gets the new-game defaults, so slice saves from before IchorSave still load. Each later version's step: 2 added `frozenHourStep` (§5); 3 added the forced omen and the held tint (§7), all from `headerReserved`; 4 added `flags2`, zeroed on load because an older save holds what used to sit past IchorSave's end there; 5 clears the new Oath allocation for older saves; 6 initializes its Urn-jar mask (§11). |
| New day | `Ichor_DoDailyEvents()` (from `DoDailyEvents`) clears the daily flag bank and draws the day's omen (§7). |
| Headroom | 136 bytes in `reserved` at 0x478 (64 remain reserved for the future `IchorEpics`), 20 in `headerReserved`, and 148 more in SaveBlock3. |

**Adding a field later.**
1. Take its bytes from the front of `reserved` and shrink `reserved` by the same amount. The struct keeps its size; `STATIC_ASSERT`s in `src/ichor_save.c` pin the size and the offsets. Growing the struct again is a last resort: it moves what follows IchorSave in SaveBlock3.
2. Bump `ICHOR_SAVE_VERSION`.
3. In `Ichor_OnSaveLoaded`, give the field its default when an older version loads.

This way the save never breaks again.

**What is in it.**

| Field | System | Notes |
|---|---|---|
| `options` | §1 relic prompt | Bit set means AUTO. Zero (ASK) is the default. |
| `relicRingCursor` | §1 Relic Ring | The ring opens on the last entry used. |
| `omenKind`, `omenEntry` | §6 omens | Today's omen. |
| `festivalsSeen` | §7 festivals | One bit per festival. |
| `blessing` | §3 rites | `god`, `flags` and `steps`. One blessing at a time. |
| `momWins`, `momLosses` | §9 knucklebones | Losses start at 212. |
| `favor[16]` | §3 rites | 0–100 per god. Favor never decreases. |
| `xenia[8]` | §10 xenia | Links done per token chain. |
| `vars[32]` | the var bank | See below. |
| `flags[256]` | the flag bank | 2,048 flags. See below. |
| `flags2[192]` (0x500) | the second flag bank | 1,536 flags (version 4). See below. |
| `dailyFlags[32]` | the daily bank | 256 flags, cleared each day. |
| `thread` | LABYRINTH.md §5.1 | Ariadne's Thread: 24 anchors (8 bytes each, not 6, because apcs-gnu rounds structs to 4 bytes), 1,792 committed steps, a 152-step live segment. |
| `oath` (0x450) | PITCH §5, UNDERWORLD §5 | Choice state, fallen count, 256 named-area encounter bits (version 5) and reserved Urn jars (version 6). Offered once at the bedroom clock on new games; see §11. |

### The flag and var banks

Only 26 vanilla vars and 322 vanilla flags were left, so IchorSave carries its own banks. Scripts use them with the ordinary commands, `setflag`, `checkflag`, `goto_if_set`, `setvar` and the rest, and with object-event hide flags. `GetFlagPointer` and `GetVarPointer` (`src/event_data.c`) route these ids into IchorSave.

| Bank | Ids | Count | Claim with |
|---|---|---|---|
| Flags | `0x2000`–`0x27FF` | 2,048 | `python3 tools/ichor/claim.py bankflag FLAG_ICHOR_<NAME> "comment"` |
| Flags, second bank | `0x2900`–`0x2EFF` | 1,536 | the same command; `--range` offsets 0x500–0xADF land here |
| Daily flags | `0x2800`–`0x28FF` | 256, cleared each day | `python3 tools/ichor/claim.py dailyflag FLAG_DAILY_ICHOR_<NAME> "comment"` |
| Vars | `0x4100`–`0x411F` | 32 | `python3 tools/ichor/claim.py bankvar VAR_ICHOR_<NAME> "comment"` |

**Use the banks for all new Ichor content,** including story flags, item balls, hidden items and hide flags. Hidden items take any flag in either general bank: `bg_hidden_item_event` packs it as `0x1000 + (flag - ICHOR_FLAGS_START)` in its 13-bit field, below which vanilla flags keep their old offsets, and `Ichor_GetHiddenItemFlag` (`include/ichor_save.h`) decodes it. Claim one with `claim.py hiddenitem FLAG_ICHOR_HIDDEN_ITEM_<NAME>`. Keep the remaining vanilla flags and vars for anything that has to sit in SaveBlock1. A claim adds a named line to `include/constants/flags.h` or `vars.h`, in the bank's "general" range.

**Parallel sessions** pass `--range LO-HI` first, as with vanilla flags (`tools/ichor/claim_ranges.md`). For a bank, LO and HI are offsets into its general range (`0x000`–`0xADF` for flags, where `0x500` and up is the second bank; `0x00`–`0x6F` for daily flags; `0x00`–`0x1F` for vars). Each claim takes the lowest free offset in the range, and lines stay sorted by offset, so separate ranges merge cleanly.

```bash
python3 tools/ichor/claim.py --range 0x000-0x0FF bankflag FLAG_ICHOR_MET_KERYKOS "met the Herald in Emporion"
```

**Reserved ranges.** Each system's bits form one contiguous run, so the engine can count them (`Ichor_CountFlags(first, count)`) and scripts can address them as `RANGE_START + n`:

| Range | First flag | Count | What |
|---|---|---|---|
| `FLAG_ICHOR_RELICS_START` | `0x2000` | 64 | Relics, upgrades and relic state (batch 2 names them) |
| `FLAG_ICHOR_HERMS_START` | `0x2040` | 32 | Great herms anointed (§4) |
| `FLAG_ICHOR_CONSTELLATIONS_START` | `0x2060` | 32 | Constellations placed (§8) |
| `FLAG_ICHOR_SHERDS_START` | `0x2080` | 48 | Potsherds, 4 per amphora, amphora *n* at `+4n` (§5) |
| `FLAG_ICHOR_AMPHORAE_START` | `0x20B0` | 16 | Amphorae completed at the Akademia |
| `FLAG_ICHOR_OSTRAKA_START` | `0x20C0` | 32 | The 30 ostraka |
| `FLAG_ICHOR_PROPHECY_START` | `0x20E0` | 16 | The 8 prophecy tablets |
| `FLAG_ICHOR_PAGES_START` | `0x20F0` | 16 | Daedalus's 7 pages |
| `FLAG_ICHOR_BRAZIERS_START` | `0x2100` | 256 | Lit braziers and lit zones (§2) |
| `FLAG_ICHOR_GIFTS_START` | `0x2200` | 64 | Rite gifts: god *g* at `+4g` (I, II, III, the Hierophant's offering) |
| `FLAG_ICHOR_ALTARS_START` | `0x2240` | 32 | Cleansed desecrated altars |
| `FLAG_ICHOR_DIG_FIXED_START` | `0x2260` | 64 | One-time dig finds |
| `FLAG_ICHOR_THEOXENIA_START` | `0x22A0` | 64 | Theoxenia visits, hides and decoys |
| `FLAG_ICHOR_XENIA_START` | `0x22E0` | 32 | Xenia hosts and token-chain links |
| `FLAG_ICHOR_GENERAL_START` | `0x2300` | 1,280 | Claimed by name: `claim.py` bankflag offsets 0x000–0x4FF |
| `FLAG_ICHOR_GENERAL2_START` | `0x2900` | 1,504 | The second bank, claimed by name: `claim.py` bankflag offsets 0x500–0xADF |
| `FLAG_ICHOR_WAYSTONES_START` | `0x2EE0` | 32 | The Oikoumene's waystones (herms beyond Aethos, §4) |
| `FLAG_DAILY_ICHOR_PRAYED_START` | `0x2800` | 16 | Prayed to god *g* today |
| `FLAG_DAILY_ICHOR_DIG_START` | `0x2810` | 96 | Daily dig spots |
| `FLAG_DAILY_ICHOR_LAUREL_START` | `0x2870` | 32 | Laurel trees, one sprig a day |
| `FLAG_DAILY_ICHOR_GENERAL_START` | `0x2890` | 112 | Claimed by name |

**Index blocks given out** within the reserved ranges (ask the engine session for more):

| Range | Indices | Owner | Use |
|---|---|---|---|
| Braziers | +0x00–0x0F | engine | tests and the slice |
| Braziers | +0x10–0x1F | world-act1 | the Telesterion, the Mystery sanctum, Eleusa's procession torches (§2) |
| Braziers | +0x20–0x2F | world-act2 | Antiope's cave, Trophonios's cave B1F and the oracle's chamber; room for Arkadia and Kaldera |
| Desecrated altars | 0–7 | Act I (not yet claimed) | |
| Desecrated altars | 8–15 | world-act2 | the Kithairon shrine, Route 9's altar, and more |
| Theoxenia | +0x00–0x0F | engine | one visit flag per god (`+ICHOR_GOD_*`), when theoxenia is built |
| Theoxenia | +0x20–0x27 | world-act2 | decoys: Eleutherai, Thyrsa, Route 8, Kirrha, and more |
| Theoxenia | +0x28–0x2F | world-act2 | decoys, batch 4: Routes 13–16, Nemea, Daphni, Emporion and Eleusa in Act II |
| Xenia | +0x00–0x03 | chain 1 | The Potter's Knucklebone (§10): Diktys (Akti), the potter (Emporion), the actor (Thyrsa), the scribe (Astyra, world-act2's Eukleides) |
| Xenia | +0x04–0x07 | chain 2 | The Split Coin: Emporion, Eleusa, Arkadia, Kaldera |
| Xenia | +0x08–0x0B | chain 3 | The third chain (Phase 4's Broken Ring) |
| Xenia | +0x10–0x1F | hosts | One flag per host who has fed you, first come: ask the engine session |
| Fixed digs | +0x00–0x0F | world-act1 | Kalliste, Route 1, Kronion Hill, Emporion, Aigina |
| Fixed digs | +0x10–0x1B | world-act2 | the Treasury of Minyas, Gla, Trophonios's great boulder, Route 9's gully, and more |
| Fixed digs | +0x20–0x2F | world-act3 | Act III's finds, its prophecy tablets and Daedalus's pages |
| Fixed digs | +0x30–0x3F | post-game | |
| Daily dig spots | +0x00–0x1F | world-act1 | Act I: Kalliste, Emporion, Eleusa |
| Daily dig spots | +0x20–0x3F | world-act2 | Act II |
| Daily dig spots | +0x40–0x4F | world-act3 | Act III |
| Daily dig spots | +0x50–0x5F | post-game | |

**One assembler caveat.** The `compare` macro (and the `goto_if_eq`-style macros built on it) treats a second argument in `0x4000`–`0x40FF` as a var and anything else as a number. So comparing a var *against a bank var* needs `compare_var_to_var` explicitly. Comparing a bank var against a number works as usual.

**Tests read the banks from IchorSave,** not from SaveBlock1. `tools/ichor/tests/engine_lib.lua`'s `L.getFlag`, `L.setFlag`, `L.getVar` and `L.setVar` handle every range.

**Check:** `tools/ichor/tests/ichor_save.sh`.

---

## Status of the rest of this file

§1–§8 are built. What each section leaves for later is listed at its end.

| § | System | Batch | State |
|---|---|---|---|
| 1 | Save state and banks | 1 | **Built** |
| 2 | Relics, darkness and braziers | 2 | **Built** |
| 3 | Rites: altars, Favor, blessings, gifts | 3 | **Built** |
| 4 | Herm waystones and the Wings | 4 | **Built** |
| 5 | The Frozen Hour (SCRIPT.md Phase 4, E1–E6) | 5 | **Built** |
| 6 | The Labyrinth: the Thread, Asterion, the Helm, the dials, sentries, the disguise | 5 | **Built** |
| 7 | Scripts' small needs: flag counts, a held tint, omens, time-of-day tables | 5 | **Built** |
| 8 | Excavation: the Trowel, dig spots, fixed finds, amphora restoration | 6 | **Built** |

Until a batch lands, a script that calls one of its names won't link. Keep such calls behind a placeholder of your own until then, or ask for the batch's constants early.

### Difficulty selection and challenge rules (PITCH §5)

The bedroom clock calls the confirmed, save-fixed difficulty selector before
letting a new player downstairs. `VAR_ICHOR_DIFFICULTY` is bank var 0;
`FLAG_ICHOR_DIFFICULTY_CHOSEN` is general offset 0x01F. Without that flag,
`GetCurrentDifficultyLevel()` returns Hero even though the new bank var is zero.
Existing saves therefore do not become Mortal. No save-layout/version change
is needed.

`specialvar VAR_RESULT, Ichor_ChooseDifficulty` takes `VAR_0x8004` as the
expansion `DIFFICULTY_EASY`, `_NORMAL` or `_HARD` value. It returns false for an
invalid or already-confirmed selection; the caller must handle that result.
The low-level expansion setter remains available for engine/test setup, not a
player-facing mode-switch menu.

`Ichor_GetStepGlassLimit` returns 150/120/100 for Mortal/Hero/Spartan. Hermes's
trial and the Labyrinth's thread use the same helper. Kerykos's first and repeat
instructions buffer that actual limit. `Ichor_GetStepGlassHalf` derives its
halfway mark from the same limit; the run caches it in `VAR_TEMP_6` at startup,
so ordinary step ticks remain vars-only. The halfway warnings occur at
75/60/50 remaining steps, while the low warning stays at 30. Spartan's current cap
mapping is 14/20/26, then the next chapter's 32 after Laurel 3. EXP multipliers
and candies cannot exceed the cap. Its option menu and battles enforce SET;
the battle-item rejection gives an explicit message but still permits capture
balls. Trainer AI is upgraded even when a trainer has no separate Hard party.
The four Act I Hierophant party variants use the existing trainer ids.

`tools/ichor/tests/difficulty.sh` checks the actual menus, all boss variants,
confirmation rejection and real save/reset/CONTINUE for all modes. Its labeled
Hermes fixtures also exercise native initial/repeat dialogue, declining and
starting the rite, and the actual halfway warning at each difficulty's mark.
`make check -j$(sysctl -n hw.ncpu) TESTS='Ichor:'` also covers caps, EXP Candy and item rejection.
Oath rules and opening selection are documented in §11. Later chapter cap
milestones and natural-level approval remain open.

`SLICE_NATURAL=1 SLICE_DIFFICULTY=hero SLICE_STARTER=0 tools/ichor/tests/slice_playthrough.sh`
starts a genuine NEW GAME without the existing level-100 assist. The shared Lua
adapter rejects emulator memory writes, state loading, injected RAM scripts and
the assist; startup probes exercise those guards. Natural runs cannot use
`SLICE_FROM` or `SLICE_WORKAROUNDS`. `PARTY` records read actual species, levels,
EXP and HP around battles. Difficulty is chosen through the real clock menu;
the separate Oath stays declined. Kleon's opening loss is a valid story branch,
not a recorded victory; later losses stop the natural pilot explicitly.

`SLICE_STOP_AFTER=<beat>` requests partial coverage with a distinct `PARTIAL PASS`
marker. It does not satisfy the full-run endpoint checks or trainer checklist.
`tools/ichor/tests/slice_natural_opening.sh` exercises all nine starter/difficulty
prologues through Kleon, Alethea's heal/gifts and Mom's return.

The natural pilot in `slice_pilot.lua` uses real buttons for captures, living
replacements, medicine, healer visits, move learning and party ordering. It
tries up to three owned balls per eligible Route 1/Kronion encounter, keeping
at most four distinct partners; a fourth slot is reserved for an actually
encountered Eopeep or Pebblith as a Normal-type counter. It reads power/type/category from the native
move UI and scores available attacks using STAB, type effectiveness, current
offensive/defensive stats and stages, including Fur Coat's physical defense.
It accounts for Double Kick's two hits, actually held type boosters and common
Fire/Water/Grass/Ground/Electric ability immunities, respecting Mold Breaker,
Teravolt and Turboblaze. In particular, Pyrrha's Narthip has Flash Fire: the
pilot must not keep selecting Fire attacks merely because it is Grass-type.
Its move-learning heuristic declines unused Howl, and preserves Yawn and unique attacks ahead of observed
status moves or weaker redundant coverage. It attempts Yawn at most once per
opposing party member in trainer battles, skipping setup when a conservative
damage estimate favors a one- or two-hit finish. Scoring includes burn's
physical penalty (respecting the configured Facade exception), Guts and the
one-third-HP thresholds for Blaze, Overgrow and Torrent.
This is not a complete battle AI:
accuracy, other abilities, variable-power moves and most tactical status/switch
choices remain unmodeled. `slice_pilot_tactics.lua` checks these scoring rules,
bounded Yawn and the Spartan battle-item ban without emulator memory access.
Opponent party indices use the native `u16` array stride, not the high byte of
the player's index. Evolution learning remembers the actual evolving task's
party slot before the summary screen opens; the battle's last EXP recipient
can be a different partner. Both cases have isolated regressions.

Before Hestia, the pilot walks back to Kronion Hill and switch-trains the actual
party to at least level 10 (14 in Spartan), using Mom for HP/PP recovery. Training is bounded
to 6,000 grass steps; no EXP, party, item or progression writes are allowed.
Healing near Akti uses the actual Asclepeion; an NPC returning to the former
player tile on map reentry does not require the pilot to stand inside it.
Clinic recovery also supports Emporion's actual healer and checks every
partner's HP and remaining move PP, not just the lead's HP. A healthy lead must
not hide a fainted or PP-exhausted bench partner. The island-ending walk guard
is unchanged, and healthy teams do not loop through the healer.
An explicitly resumed fixture with a setup warp verifies the real Emporion
clinic round trip: genuine pre-Kerykos damage is healed, owned Potions are
preserved and the original city position and field control are restored.
That fixture is not continuous provenance. At Kerykos's dais, the pilot now
checks owned field recovery again after Philonides rather than entering the
Hierophant battle with unchecked new damage; it does not leave an active Run
for a clinic.
`PILOT` records describe inspections, item consumption, catches, move choices
and training alongside the existing `PARTY`/`BATTLE` evidence.
Before Ione, the starter is restored as the lead by its original personality
and given its actually collected type booster, or its reserved Sitrus Berry
in Spartan. GIVE checks both held ownership and exact Bag consumption.
It also gives the collected Hard Stone to Pebblith and an available Miracle
Seed to a Grass-type partner, without replacing an existing held item.
The scorer includes the actually held Hard Stone's Rock boost.
After Kalliste, the harness checks that Charcoal is actually in the Bag for
Kedalion's `checkitem`, not just held by a partner. Euboulos's existing recovery
conversation supplies a replacement when the first coal is held; the pilot
does not take the held copy or add another duplicate.
Mortal/Hero may use owned trainer-battle medicine at half HP or below, asserting
actual HP recovery and exact consumption. Spartan never requests battle medicine.
At Demeas's pre-Laurel stall it buys five ordinary balls through the quantity
and confirmation menus, asserting five added balls and the real 1,000 payment
before returning to the item list. A NEW GAME Hero/Kynder run through the
Agora verifies actual ownership changing from 2 to 7 and money from 4,440 to
3,440; that partial endpoint is not a chapter pass. Training keeps its battle
mode enabled across healing/menu walks as well as grass steps, and fails
explicitly if it runs out of owned balls before recruiting a counter.

At Emporion's actual general stall, the pilot now buys five Super Potions
for temple preparation rather than merely viewing the wares. The shared
purchase helper checks the native task's selected item and quantity, reads
the actual decimal price quote (including any blessing discount), and
verifies exact ownership and money changes before returning to the list.
A rejected quantity, malformed quote or mismatched receipt fails explicitly;
the pilot must not retry a completed transaction. Isolated models cover
ordinary/discounted prices and those refusals. An explicit matching-ROM
city fixture buys five real Super Potions: 2→7, with money 8,260→4,760 and
a quoted cost of 3,500. It is not continuous or temple-win evidence.
Pasion's separate 600 payment is checked against money immediately before
his conversation, so a legitimate earlier purchase does not invalidate it.

The earlier three-partner pilot reached `08_after` continuously from NEW GAME
with Hero/Nebrel: 418,310 frames,
117 battles. This strategy includes substantial wild training: the starter
enters Ione at level 16, alongside two level-10 partners. Mortal/Nebrel also
reaches `08_after` (333,477 frames, 78 battles). These older passes predate the
current four-partner strategy and do not certify its results.

With corrected evolution learning and native-width opposing party indices,
the pre-partner-gear Hero/Kynder pilot reached `08_after` from NEW GAME:
353,799 frames, 69 battles,
559 screenshots. Ione is entered with a level-16 Dikyon and three level-10
partners, including an actually caught Pebblith; Yawn is attempted separately
against all three of Ione's partners. Earlier Kynder attempts failed there.
The current partner-gear pilot has NEW GAME ending passes for Hero/Nebrel
(342,098 frames, 71 battles), Hero/Hipling (330,924 frames, 73 battles),
Mortal/Nebrel (336,571 frames, 66 battles) and Mortal/Hipling
(335,386 frames, 71 battles). Hero/Kynder instead loses to Ione, whose final
partner has 7 HP left; the earlier win does not certify the revised strategy.
Current Spartan/Nebrel also loses there, with Nemecub left at 46 HP, not the
older attempt's 2 HP. Spartan/Hipling's earlier four-level-14 loss and
Spartan/Kynder's possible Metis loss remain unclosed.

An earlier Mortal/Kynder run won both summit grunts but exhausted the
harness's shared 20,000-frame scene deadline: the battles alone took 12,705
and 6,525 frames. The native script context was normally WAITING after
`dotrainerbattle`, not an established engine lock. `L.settle` now excludes
nested battle time from its scene deadline; each battle retains its own
30,000-frame limit. A resumed summit fixture completes both battles, the
scene's flags and restored field control in 20,318 frames without raising
either deadline. A fresh NEW GAME Mortal/Kynder attempt instead loses its
first summit battle, so it does not certify continuous passage or an ending.
A separate resumed pre-Ione fixture verifies
native Hard Stone GIVE and Euboulos's actual coal replacement while the
starter still holds its booster; that is menu evidence, not chapter coverage.
With useful-Yawn and status/ability scoring, Mortal/Kynder reaches `08_after`
from NEW GAME: 275,043 frames, 48 battles, 520 screenshots. Hero/Kynder still
loses to Ione (last foe 31 HP), as does Spartan/Hipling (last foe 19 HP).
Those new attempts supersede neither older strategies' evidence nor the
remaining matrix, intended-curve and repeatability gates.
The next continuous Mortal/Kynder NEW GAME attempt reaches Kerykos in
460,136 frames, completing the Herald's Run with 73 of 150 steps left and
beating all three acolytes before losing to the Hierophant. Its companions
remain level 10–11 while the starter enters Kerykos at level 19 with 20/52 HP.
This is not a Laurel-2 or gate-opening pass. The harness now asserts the real
150/120/100 budget rather than a Hero-only 120; the previous mainland attempt
stopped at that incorrect assertion, not an actual rite failure.
Subsequent fresh attempts with pre-dais field recovery, then whole-team clinic
recovery, also lose to Kerykos (414,818 and 443,391 frames). In the latter the
starter reaches the boss at 17/52 HP after Philonides, with no usable medicine
left. Reaching a real healer earlier does not supply medicine for the temple;
the pilot still needs a legitimate preparation strategy. No balance change or
Laurel-2 natural pass is inferred from these losses.
With five actually purchased Super Potions, the next current-player-art
NEW GAME Mortal/Kynder run wins Kerykos, receives Laurel 2 and reaches the
Isthmus Gate (447,239 frames). It loses Kleon's second battle, an explicitly
supported no-whiteout branch in SCRIPT.md beat 16 and the native script;
the harness still stops at its win-only assertion. This is genuine Laurel-2
coverage, not a rival win or a verified final gate endpoint.
The gate check now accepts exactly the authored win/loss outcomes, reads the
actual starter-specific trainer ID from `gTrainerBattleParameter`, checks
rival music and the outcome-specific victory flag, and requires the shared
completion/hide flags, cleared no-whiteout flag, Kleon's removal, actual gate
traversal and returned field control. A loss must also leave every real party
member fully healed by the native scene. The final trainer checklist permits
this exception only with an actual recorded loss to the matching rival and
the completed scene; ordinary trainer/Hierophant victories remain mandatory.
Explicit current-ROM resumed fixtures pass the loss branch in 9,122 frames
and the strength-assisted win branch in 5,680 frames. Neither is continuous
natural evidence. One new continuous attempt was interrupted by host disk
exhaustion; it supplies no pass. After space recovered, a fresh NEW GAME
attempt buys the five real Super Potions but loses to Kerykos at 453,103 frames.
The earlier actual Laurel-2 victory therefore does not establish a reliable
strategy, and a continuous natural gate pass is still unverified.
These results do not establish the intended curve's balance. Other
starter/difficulty chapter runs, complete
natural-level Act I coverage and player approval remain separate gates.
The continuous route now continues beyond the opened Emporion gate: the actual
Isthmus slide and Hammer rewards, Hecate's Torch and western Hollow, cliff-road
trainers and healers, and Krokis's Eleusa arrival (`20_eleusa_arrival`). Its 17
additional trainers are tracked in the final victory checks. The city walker
stops avoiding the Isthmus gate only after the actual rival scene is complete.
A fresh NEW GAME Hero/Kynder **assisted** run passes in 378,413 frames with 63
battles and 1,263 complete screenshots. This is connected progression evidence,
not natural-level balance evidence. Earlier attempts affected by host disk
exhaustion are not complete persisted evidence. Demeter, the Mysteries and the
sanctum still have separate fixtures, not a continuous ending pass.

`python3 tools/ichor/tests/test_slice_policy.py` checks option/range preflight
without requiring a ROM or toolchain. Invalid requests must preserve existing
screenshots and save states; every declared beat remains selectable.

The headless runner fails with exit 1 if stdout cannot be written completely,
even if Lua reaches its completion marker. Partial logs are not valid run
evidence. `python3 tools/ichor/tests/test_headless_output.py` checks both complete
output and a real failed write under a small file-size limit; build the ROM
and runner first.

Screenshots are accepted only after checking the actual PNG signature and final
IEND chunk; mGBA's screenshot API itself returns nothing even on write failure.
An existing image is removed first so a failed replacement cannot reuse stale
evidence. Diagnostic state saves must also report success. Host disk exhaustion
must stop the run, not produce a successful log with missing artifacts.
After generating `build/slice/symbols.lua`, run
`mkdir -p build/slice-persistence/shots build/slice-persistence/states` and
`build/tools/ichor-mgba-headless --script tools/ichor/tests/slice_persistence.lua --frames 150 --until "SLICE PERSISTENCE done" pokeemerald.gba`
to check actual PNG/state writes and modeled stale-image, truncated-PNG and
state-save failures. This isolated check is not gameplay progression evidence.

`build/tools/ichor-mgba-headless --script tools/ichor/tests/slice_pilot_cursor.lua --frames 2 --until "PILOT CURSOR done" pokeemerald.gba`
checks all 30 cursor transitions across one-, two-, three- and four-move grids.
The isolated input model rejects moves into empty slots, including the
three-move case where bottom-left must reach top-right through the top row.

`build/tools/ichor-mgba-headless --script tools/ichor/tests/slice_scene_budget.lua --frames 2 --until "SCENE BUDGET done" pokeemerald.gba`
models two 11,000-frame battles inside one scene, plus genuine scene locks
with and without preceding battles. Battles must not consume the scene
budget, and non-battle timeouts must still fail within their requested limit.

## 2. Relics (SYSTEMS §1, §2)

Relics are key items. **No Pokémon ever needs a field move:** the party menu offers none, and every obstacle checks the bag.

### The items

| Item | Name in game | Field power | Used how |
|---|---|---|---|
| `ITEM_TALARIA` | Talaria | Run (hold B) | Always on once owned |
| `ITEM_BRONZE_HAMMER` | Bronze Hammer | Rock Smash: marble rubble | Face it, press A |
| `ITEM_HECATES_TORCH` | Hecate's Torch | Light in dark maps; light braziers; burn cobwebs | Automatic in the dark; A on a brazier or web; douse or light from the Relic Ring |
| `ITEM_DEMETERS_SICKLE` | Demeter's Sickle | Cut: thorn thickets | A |
| `ITEM_GIRDLE_OF_HERAKLES` | Girdle of Herakles | Strength: column drums | A, then push |
| `ITEM_POSEIDONS_CONCH` | Poseidon's Conch | Surf | A on water (always asks) |
| `ITEM_DAEDALUS_WINGS` | Daedalus's Wings | Fly | From the bag or the Relic Ring |
| `ITEM_HORN_OF_ACHELOUS` | Horn of Achelous | Waterfall | A at a waterfall while surfing (always asks) |
| `ITEM_ARIADNES_THREAD` | Ariadne's Thread | In the Labyrinth, laid on the floor as you walk, with TIE OFF, RETURN TO… and WIND IN (§6); elsewhere an escape to the dungeon's entrance | Relic Ring |
| `ITEM_LABRYS` | Labrys | Cleaves labrys seals and bronze chains | A |
| `ITEM_HELM_OF_DARKNESS` | Helm of Darkness | On or off; unseen in the dark, by trainers and Asterion (§6) | Relic Ring |
| `ITEM_NEREID_PEARL` | Nereid Pearl | Dive | A on deep water |
| `ITEM_AEOLUS_BAG` | Aeolus's Bag | Defog | From the bag |

**Giving a relic.** Use `giveitem(ITEM_BRONZE_HAMMER)`. The engine sets the relic's flag whenever the item enters the bag (`AddBagItem`), so scripts can check either. The icons are in `graphics/items/icons/`, drawn by `tools/ichor/art/items_relics.py`; Ariadne's Thread is the Escape Rope's coil in red.

**Check:** `tools/ichor/tests/ichor_relics.sh`.

**Relic flags** (bank, in `FLAG_ICHOR_RELICS_START`'s range):
- `FLAG_ICHOR_GOT_<RELIC>` for each relic above: `_BRONZE_HAMMER`, `_HECATES_TORCH`, `_DEMETERS_SICKLE`, `_GIRDLE_OF_HERAKLES`, `_POSEIDONS_CONCH`, `_DAEDALUS_WINGS`, `_HORN_OF_ACHELOUS`, `_ARIADNES_THREAD`, `_LABRYS`, `_HELM_OF_DARKNESS`, `_NEREID_PEARL`, `_AEOLUS_BAG`.
- **`FLAG_ICHOR_GOT_TALARIA` is an alias of `FLAG_SYS_B_DASH`,** so the slice's Talaria keeps working unchanged.
- Upgrades, which the rites' gift II sets: `FLAG_ICHOR_WINGED_TALARIA`, `FLAG_ICHOR_THREE_FLAMED_TORCH`, `FLAG_ICHOR_HEPHAESTUS_HAMMER`, `FLAG_ICHOR_TRITON_CONCH`, `FLAG_ICHOR_HELM_OF_HADES`.
- State: `FLAG_ICHOR_TORCH_DOUSED` and `FLAG_ICHOR_HELM_ON`.
- `FLAG_ICHOR_NO_RELICS`: set it in a map's ON_TRANSITION (a trial that forbids outside tools) and every relic refuses there. The engine clears it on every map change.

### Obstacles

Place an object event with the obstacle's graphics and script. The scripts keep their vanilla names, so the Hoenn maps still work until they are cut. Each asks first ("A thorn thicket. Cut it with Demeter's Sickle?"), or under the AUTO option just acts. Without the relic, each describes the obstacle and hints at a tool; none ever mentions a Pokémon.

| Obstacle | Graphics | Script | Needs |
|---|---|---|---|
| Thorn thicket | `OBJ_EVENT_GFX_CUTTABLE_TREE` | `EventScript_CutTree` | Demeter's Sickle |
| Marble rubble | `OBJ_EVENT_GFX_BREAKABLE_ROCK` | `EventScript_RockSmash` | Bronze Hammer |
| Column drum | `OBJ_EVENT_GFX_PUSHABLE_BOULDER` | `EventScript_StrengthBoulder` | Girdle of Herakles |
| Cobweb | any; a web sprite is coming | `EventScript_IchorCobweb` | Hecate's Torch |
| Thornweb | any | `EventScript_IchorThornweb` | the Three-Flamed Torch |
| Great boulder (2×2) | any | `EventScript_IchorGreatBoulder` | Hephaestus's Hammer |
| Labrys seal or bronze chain | any | `EventScript_IchorLabrysSeal` | Labrys |

- Any sprite works for the new obstacles, since the scripts never animate them; they remove the object with a sound. Only `EventScript_RockSmash` plays the rubble's breaking animation, so it needs the rubble sprite.
- **Art note:** `OBJ_EVENT_GFX_BREAKABLE_ROCK` draws nothing on Route 1 (found by `tools/ichor/tests/ichor_relics.sh`). The marble-rubble swap (INVENTORY §1) should fix it. The cut tree draws as a bush until the thorn-thicket art lands.
- Like vanilla, an obstacle comes back when the map reloads. To clear it for good, give the object a hide flag of your own; the script's `removeobject` sets it.
- **Water needs no events:** Surf, Waterfall and Dive come from the map's metatile behaviors, exactly as in Emerald, and check the Conch, the Horn and the Pearl.
- **The wording without the relic** follows SYSTEMS §1: "A thorn thicket. A good blade would clear it." and "The blocks won't shift by hand. A good hammer would break them."

### Darkness and braziers (SYSTEMS §2)

- **A dark map** is one whose header has `"cave": true` (Porymap: "Requires Flash"). The light radius comes from `Ichor_GetTorchFlashLevel` (`src/ichor_relics.c`):

  | | Flash level | Radius |
  |---|---|---|
  | No Torch | 7 | 1.5 tiles |
  | Hecate's Torch | 3 | 3.5 tiles |
  | The Three-Flamed Torch, or Hecate's blessing | 2 | 4 tiles |
  | Both | 1 | 4.5 tiles |
  | Torch doused (Relic Ring) | 8 | black: glow-paint only, once its palettes exist |

- **Braziers** are metatiles, so the map draws them. Each gets a flag in `FLAG_ICHOR_BRAZIERS_START`'s range; ask the engine session for a block of indices for your maps. Blocks given out so far:

  | Indices | Owner | Use |
  |---|---|---|
  | +0x00–0x0F | engine | tests and the slice |
  | +0x10–0x13 | world-act1 | the Telesterion's season braziers in Eleusa: autumn, winter, spring, summer |
  | +0x14–0x1F | world-act1 | kept: the Mystery sanctum's four, Eleusa's procession torches |
  | +0x20–0x2F | world-act2 | Antiope's cave, Trophonios's cave B1F and the oracle's chamber; room for Arkadia and Kaldera |
  ```
  // the brazier's bg event
  script Map_Brazier1 {
      setvar(VAR_0x8004, FLAG_ICHOR_BRAZIERS_START + 0)  // its flag
      setvar(VAR_0x8005, TRUE)              // TRUE: lighting it lights the zone the player stands in
      call(EventScript_IchorBrazier)        // asks, lights it, sets the flag
      if (var(VAR_RESULT) == TRUE) {        // TRUE only when it was lit just now
          setmetatile(...)                  // swap in your lit metatiles
          special(DrawWholeMapView)
      }
      releaseall
  }
  ```
  Without the Torch it says "A cold bronze brazier. It needs a flame." Once lit it says "The brazier burns steadily." In the map's ON_LOAD, swap the metatiles of every brazier whose flag is set.
- **Lit zones.** A coord event on each threshold of a brazier's zone:
  - going in: `setvar(VAR_0x8004, <brazier flag>)`, then `call(EventScript_IchorEnterLitZone)`. It brightens the map fully if that brazier is lit.
  - going out: `call(EventScript_IchorLeaveLitZone)`, which eases back to the torch's radius.
- **A map that loads with the player inside a lit zone** sets `setflashlevel(0)` in its ON_TRANSITION when the zone's flag is set.
- **The light eases both ways.** `animateflash` (and so the lit zones, braziers, dousing and relighting) darkens as well as brightens, even from a fully lit map. Asking for the level the map already has returns at once. These were fixed 2026-11-14, from world-act2's report: entering a lit zone that was already fully lit used to hang, and nothing could darken a map once it was fully lit. A map's own guard against either (Trophonios's cave's `VAR_TEMP_6`) can go.
- **The light moves 2 px a frame** and only inside the screen, so crossing a threshold takes under a second.
- **Glow-paint** (dousing to see it):
  - **The copies:** a secondary tileset's glow copies are `data/tilesets/secondary/<name>/glow/00.pal`–`15.pal`. They are the same slots as its `palettes/`, every color black except what glows.
  - **Registering:** declare them in `src/data/tilesets/graphics.h` as `gTilesetPalettes_<Name>Glow`, the same way as its palettes, and add one row to `src/data/ichor_glow.h`: `{ &gTileset_<Name>, gTilesetPalettes_<Name>Glow }`.
  - **What happens:** with the torch doused on a dark map of that tileset, slots 0–12 take the glow colors, and the map's layers show in the dark while its people stay hidden. Relighting brings back the map's own colors. A map loaded while doused gets the glow too.

### Carried flames (SYSTEMS §2)

- **A carried flame** is a named fire on Hecate's Torch for a set number of steps. Its kinds are `FLAME_HEARTH`, `FLAME_SANCTUM`, `FLAME_THRESHOLD`, `FLAME_PANATHENAIA` (the Panathenaia's race torch, §7), and the post-game's `FLAME_HESTIA_SHIP` (Hestia's fire) and `FLAME_LERNA` (Kleon's fire). Add new kinds at the end, with their names in `src/ichor_relics.c`.
- **The engine keeps it,** not the map's temp vars. Maps use `VAR_TEMP_*` for their own ends. Read it with `specialvar(VAR_RESULT, Ichor_GetFlameKind)` (`FLAME_NONE` without one) and `specialvar(VAR_RESULT, Ichor_GetFlameSteps)`. The first draft kept it in `VAR_TEMP_2` and `VAR_TEMP_3`; scripts that check those must switch to the specials.
- **It dies when you leave the map,** unless its kind **travels**. A travelling kind keeps its steps through doors, warps and map edges: so far `FLAME_HESTIA_SHIP`, Lampon's walk from Akti's temple to the quay, and `FLAME_PANATHENAIA`, the torch race from the Kerameikos's Dipylon through Astyra to the Akropolis. Mark a new kind in `sFlameTravels` (`src/ichor_relics.c`). A save and CONTINUE puts any flame out.
- **A brazier that gives its fire:** `setvar(VAR_0x8004, FLAME_HEARTH)`, `setvar(VAR_0x8005, 20)`, then `special(Ichor_TakeFlame)`. `VAR_RESULT` is `FALSE` without a lit Torch.
- **Relighting (the relay).** A brazier already lit with that fire gives a full budget the same way. Do it in the brazier's own script, after `call(EventScript_IchorBrazier)`: if its flag is set and `Ichor_GetFlameKind` is that kind (or any kind, if the brazier hands out its fire), call `Ichor_TakeFlame` again with the dry budget. Labor 2's burned pools work like this.
- **A brazier that wants a named fire** checks `Ichor_GetFlameKind` itself, then `special(Ichor_PutOutFlame)` if the fire is spent on it.
- **Each step burns one; in rain, two.** Rain means rain, downpour or a thunderstorm. Scripts always give the dry budget: SYSTEMS's 40 becomes 20 in rain. Passing 5 steps left: "The flame gutters." At 0: "The carried fire dies down to the torch's own flame."
- **Water puts it out:** "The water puts out the carried fire." Surfing, which covers falling into water and the waterfall, does it on the next step. Sailing doesn't: aboard the Euploia (world-postgame's `FLAG_ICHOR_ON_SHIP`) the torch stays lit. Dousing the Torch from the Ring puts it out silently.
- **Wind:** a draughty doorway's coord event runs `call(EventScript_IchorDraught)`. It does nothing without a flame; with one, "A draught snuffs out the carried fire."
- **The start menu's panel** shows "Hearth fire: 12 steps", under the blessing when there is one.
- **Order, Return and Reveal** (SYSTEMS's other verbs) are the map's own script.

### Calls for scripted relic moments

- `setvar(VAR_0x8004, ITEM_X)`, then `call(EventScript_IchorRelicPose)`: the player raises relic X, its icon shows over their head with a chime, and a follower hops. Use it when a story script uses a relic.
- `specialvar(VAR_RESULT, Ichor_CanUseRelic)` with `VAR_0x8004` = the relic and `VAR_0x8005` = an upgrade flag or 0. Returns `ICHOR_RELIC_OK`, `_MISSING`, `_FORBIDDEN` or `_TOO_WEAK` (`include/constants/ichor.h`).
- `specialvar(VAR_RESULT, Ichor_RelicPromptsAuto)`: TRUE when the player chose AUTO.
- `specialvar(VAR_RESULT, Ichor_IsInDarkMap)`.

### The player's side

- **The Relic Ring:** once the player owns a free relic, SELECT opens a menu in the top-right corner: the registered item first, then FLY, DOUSE TORCH or LIGHT TORCH, WEAR HELM or REMOVE HELM, and THREAD. Hestia's Hearthfire joins it with the rites (§3). It opens on the last entry used, so SELECT then A repeats the last action. Before the first free relic, SELECT runs the registered item as in Emerald.
- **From the bag,** each relic does what it does in the field. The contextual relics (Hammer, Sickle, Girdle, Labrys, Conch, Horn and Pearl) act on the obstacle or water in front of the player, or say there's nothing to use them on. The Wings open the fly map, and cancelling it returns to the bag. The Torch douses or relights on dark maps, and the Helm goes on or off. The Thread escapes a dungeon like the Escape Rope, and Aeolus's Bag clears fog from the map until the player leaves it.
- **The Town Map** flies with R once the Wings are owned (`OW_FLAG_POKE_RIDER` is `FLAG_ICHOR_GOT_DAEDALUS_WINGS`).
- **The option "Relic prompts":** the RELIC PROMPTS row of the options menu, ASK (the default) or AUTO. Water (Surf, Waterfall, Dive) always asks. The menu's eight rows are 14 px apart, so they still fit the vanilla box.
- **The pose:** the player raises the relic, its icon shows over their head, and a chime plays. No Pokémon cut-in appears, and a follower hops beside you as before.

### A change to the slice (for the map owner)

The Talaria is a flag today, not an item. For it to show in the bag, add one line to `data/maps/ElaiaVillage_PlayersHouse_1F/scripts.pory`, after `setflag(FLAG_RECEIVED_RUNNING_SHOES)`:
```diff
     setflag(FLAG_SYS_B_DASH)
     setflag(FLAG_RECEIVED_RUNNING_SHOES)
+    additem(ITEM_TALARIA)
```
Running already works without it.

## 3. Rites (SYSTEMS §3)

The code is `src/ichor_rites.c` and `data/scripts/ichor_rites.pory`. **God ids** are in `include/constants/ichor.h`: `ICHOR_GOD_HESTIA` (1), `_HERMES`, `_DEMETER`, `_DIONYSUS`, `_ARTEMIS`, `_HEPHAESTUS`, `_APHRODITE`, `_APOLLO`, `_ARES`, `_POSEIDON`, `_ATHENA`, `_HERA`, `_ZEUS`, `_HECATE`, `_HADES` (15). 0 is none.

### Altars

Use these directly as an altar's bg event or object script. Each runs the whole rite: the altar's line, then a menu of PRAY, MAKE AN OFFERING, FAVOR and LEAVE, then any gift that is due. LESSON joins the menu once the god has taught its move, and REST joins it at a hearth once Hestia's Ever-Ember is owned.

| Script | Where |
|---|---|
| `EventScript_IchorAltar_<God>` | A roadside or town altar, e.g. `EventScript_IchorAltar_Apollo` |
| `EventScript_IchorTempleAltar_<God>` | The god's great altar in their temple. Offerings count double. |
| `EventScript_IchorHearth` | A household hearth: Hestia's altar |
| `EventScript_IchorAltar_Ares` | Ares's trophy. The menu says OFFER A BATTLE instead of MAKE AN OFFERING. |
| `EventScript_IchorDesecratedAltar` | Set `VAR_0x8004` to the god and `VAR_0x8005` to the altar's index (0–31), then `goto` it. Beat the Titanborn guard in your own script first. Cleansing sets `FLAG_ICHOR_ALTARS_START + index` and gives the god +3 Favor; after that it's an ordinary altar. |

The altar scripts use `VAR_0x8004`–`0x8007` and `VAR_0x800A`–`0x800B`.

### The rules, as built

- **Prayer:** the god's minor blessing for 100 steps (150 once Known, Favor 10), and +1 Favor the first time each day (`FLAG_DAILY_ICHOR_PRAYED_START + god`).
- **Offerings:** the list shows every offering in the bag with its count and icon: the six new items, Honey, any berry (first fruits), the seven feathers, the sea gifts, and the Bronze Obol (Relic Copper, for Hades).
  - A loved offering gives +5 Favor and the major blessing for 500 steps. A liked one gives +3 and 300 steps, and any other offering is accepted for +1 and 150 steps.
  - Favor doubles at the god's temple altar. Hestia takes +1 of every offering made to another god.
  - Demeter refuses the pomegranate (Pomeg): no Favor, and the player keeps it.
- **Blessing length:** ×1.5 once Beloved (Favor 60), capped at 4,095 steps. A prayer or offering to another god asks first ("Apollo's blessing is still on you. Go on anyway?").
- **Dionysus:** passes on a random other god's blessing (never Zeus's or Hades's) at ×1.5 length. One major offering in eight gives Frenzy instead: encounters ×2, wild levels +3, EXP ×1.5.
- **The countdown:** one step at a time, like a Repel. When it ends, the god's line plays ("Apollo's light fades from you."). The start menu shows a BLESSING panel ("Apollo (412)").
- **The minor blessing** has the same effect as the major one, only shorter. The exception is Hestia: a prayer's Hearthfire heals HP only, while an offering's heals everything.

| God | Blessing, as built | Hook |
|---|---|---|
| Hestia | Hearthfire: HEARTHFIRE in the Relic Ring heals the party, then the blessing ends | `Ichor_UseHearthfire` |
| Hermes | Agora prices −20%, selling +20%, prize money +20% | `shop.c`, `item.c`, `Cmd_getmoneyreward` |
| Demeter | Wild held items as with Compound Eyes; berry trees +1 | `SetWildMonHeldItem`, `CalcBerryYield` |
| Dionysus | Revel or Frenzy, above | `Bless` |
| Artemis | Encounters −25%; at night the three rarest land slots ×3; Augur's Eye sneaking range +2 | `WildEncounterCheck`, `ChooseWildMonIndex_Land`, `dexnav.c` |
| Hephaestus | **Hook:** hidden-item glints and rock-smash drops wait for those systems | — |
| Aphrodite | Friendship gains ×2; 2 wild Pokémon in 3 are the lead's opposite gender | `AdjustFriendship`, `CreateWildMon` |
| Apollo | EXP +20% | `ApplyExperienceMultipliers` |
| Ares | Wild Pokémon 5+ levels below the lead don't appear; wild levels +2; EXP +10% | `TryGenerateWildMon` |
| Poseidon | Every cast bites at once; the rods' rare slots favored (as a Lure does); surfing encounters −50% | `fishing.c`, `ChooseWildMonIndex_Fishing` |
| Athena | Always escape wild battles; the Augur's Eye finds hidden Pokémon ×2 | `TryRunFromBattle`, `dexnav.c` |
| Hera | Eggs hatch ×2 faster; the day care finds eggs ×2 | `daycare.c` |
| Zeus | +1 shiny roll; Electric and Flying types about ×2 | `pokemon.c`, `TryGenerateWildMon` |
| Hecate | Torch radius one level larger (§2); at night Ghost, Dark and Psychic about ×2 | `Ichor_GetTorchFlashLevel`, `TryGenerateWildMon` |
| Hades | The coins sell for +50%. **Hook:** double dig and rock-smash finds wait for excavation | `item.c` |

### Gifts

- **Gift I (Favor 30)** is a lesson: the god's move, taught through the move-tutor party menu (`ChooseMonForMoveTutor`). Most of the gift moves aren't TMs in this build, and a lesson works for any move. If the player cancels, the lesson waits at the altar. Once taught, the altar's LESSON entry teaches it again as often as asked, like a TM.
  The 15 dynamically selected `sGods[].giftMove` moves are registered in
  `src/data/pokemon/special_movesets.json` under `extraTutors`: the script
  scanner cannot discover runtime-selected moves. Registration preserves each
  species' `all_learnables` eligibility; it does not make lessons universal.
- **Gift II (Favor 60)** is a tool or an upgrade:
  - Ever-Ember: Hearthfire never fades, and hearths offer REST.
  - The Winged Talaria: running into an `MB_ICHOR_GAP` tile leaps it like a ledge.
  - The Harvest Basket.
  - The thyrsus: climbs `MB_ROCK_CLIMB` ivy walls with the expansion's Rock Climb.
  - The Myrtle Wreath: a held item; its holder's friendship never drops.
  - The Lyre of Apollo (the Poké Flute, renamed).
  - The War Horn (the VS Seeker, renamed).
  - The Acorn of Dodona (the Shiny Charm, renamed).
  - Hephaestus's Hammer, the Three-Flamed Torch, Triton's Conch and the Helm of Hades: flags the relics read (§2).
  - The Hunter's Moon and the Eyes of Argus remain **flags-only hooks**.
    Athena's Stylus is read by the Scroll of Deeds to add open-quest hints.
- **Gift III (Favor 100)** sets its flag and shows the sacred animal. **Hook:** the static encounter waits for the dex's species.

### Calls for story scripts

| Call | In | Out |
|---|---|---|
| `special(Ichor_AddFavor)` | `VAR_0x8004` god, `VAR_0x8005` amount | Favor caps at 100 and never drops. Amounts: `ICHOR_FAVOR_LAUREL` (15), `_MYTH_QUEST` (10), `_FESTIVAL` (5), `_CLEANSE` (3). |
| `specialvar(VAR_RESULT, Ichor_GetFavorOf)` | `VAR_0x8004` god | 0–100 |
| `specialvar(VAR_RESULT, Ichor_GetBlessingGod)` | | The god whose blessing is on the player, or 0 |
| `special(Ichor_GrantBlessing)` | `VAR_0x8004` god, `VAR_0x8005` steps | A minor blessing, e.g. the augur's good omen |
| `call(EventScript_IchorHierophantGift)` | `VAR_0x8004` god | The Hierophant teaches gift I if it's due. `VAR_RESULT` is TRUE if they did. |
| `call(EventScript_IchorHierophantRite)` | `VAR_0x8004` god | First visit only: a line about the rite, and one loved offering |
| `goto(EventScript_IchorAresVictory)` | | After a won war-acolyte bout: Ares +5 Favor and War-lust. **The bout's trainer doesn't exist yet**: `EventScript_IchorAresBout` is the stub to replace. |

**Gift flags:** `FLAG_ICHOR_GIFT(god, n)` (`include/constants/flags.h`), where n is `ICHOR_GIFT_I`, `_II`, `_III` or `_HIEROPHANT`.

Hermes's and Demeter's map great altars call their temple wrappers. Kerykos
adds `ICHOR_FAVOR_LAUREL` before first setting Laurel 2, then offers the shared
Hermes lesson on return visits. His authored Honey rite retains the shared
Hierophant offering flag and full-Bag retry.

**The offerings** are `ITEM_OLIVE_OIL` (200), `ITEM_BARLEY_CAKE` (150), `ITEM_WINE` (300), `ITEM_FRANKINCENSE` (500), `ITEM_LAUREL_SPRIG` (100) and `ITEM_BRONZE_VOTIVE` (400). Honey now costs 300.
- **Their icons are stand-ins** borrowed from existing items (the oil flask, a cookie, juice, the incense cone, a seedling, the Metal Coat), as is the Myrtle Wreath's. Drawing the real ones is for the art team.

**Checks:** `tools/ichor/tests/ichor_rites.sh` (in game) and `test/ichor_rites.c` (the rules, in `make check`).
The in-game check includes both actual temple altars, prayer and doubled
offerings, actual tutor cancellation/retry, native confirmation of Harpeck's
learned U-turn, and no repeated claimed gift. `test/ichor_tms.c` checks eligible
and ineligible species; `tools/ichor/tests/temple_hermes.sh` checks the real
Laurel battle's one-time +15 Favor.

## 4. Herm waystones (SYSTEMS §4)

Built in `src/ichor_herms.c`, `src/data/ichor_herms.h` and `data/scripts/ichor_herms.pory`. Tested by `tools/ichor/tests/ichor_herms.sh`.

- **One great herm per route.** Its bg event runs `EventScript_IchorGreatHerm` directly. A herm that is already a sign with its own line calls `EventScript_IchorAnointHerm` after it, between `lockall` and `releaseall`. The engine knows which herm it is from the map; on a map with no herm row, both scripts do nothing.
- **Herm ids** (`include/constants/ichor.h`) follow AETHOS_MAP's land routes and their map sections: `HERM_KALLISTE_ROUTE_1`, `HERM_AETHOS_ROUTE_4` … `_18`, `HERM_BULL_ROAD`, `HERM_AETHOS_ROUTE_25` … `_30` and `HERM_THE_ASCENT`. That is 23 before the post-game (`HERM_COUNT`). The post-game's `HERM_AETHOS_ROUTE_31` and `_32` come after them and don't count toward the bonus. Sea routes have no herm. Room is left for 32.
- **Emporion's city anchor** uses `HERM_EMPORION_CITY` (25), outside the 23-route count.
  It anoints normally and flies to `HEAL_LOCATION_HERM_EMPORION_CITY` (26,32),
  south of its stone (26,31). City entry migrates the old
  `FLAG_ICHOR_HERM_EMPORION`; a new anointing mirrors that flag. Migration
  neither charges another Oil nor grants another Favor.
- **The Oikoumene's waystones** (herms, Thoth's ibis pillars, stone babas and cairns of Ammon; OIKOUMENE §4) take ids from `HERM_OIKOUMENE_FIRST` (32) to 63. They anoint the same way and join the Wings' fly map, but never count toward Aethos's herms or the bonus. Their flags are `FLAG_ICHOR_WAYSTONES_START + (id - 32)`; `Ichor_GetHermFlag(id)` gives any herm's flag. The Oikoumene session sends each waystone's map, map section and landing tile, and the engine session adds its row.
- **Each herm's flag** is `FLAG_ICHOR_HERMS_START + id`. A script that needs to know whether a herm is anointed (the Frozen Hour's turning heads) checks that flag. Nothing else sets it; the herm script does.
- **Each herm needs one engine table row and one heal location.** Tell the engine session the herm's map and its landing tile (the tile south of it, on the main path), or add both rows yourself:
  - `src/data/ichor_herms.h`: `[HERM_AETHOS_ROUTE_4] = { .map = MAP_..., .mapsec = MAPSEC_AETHOS_ROUTE_4, .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_4 },`
  - `src/data/heal_locations.json`: `HEAL_LOCATION_HERM_AETHOS_ROUTE_4`, with the landing tile's map, x and y.

  | Herm | Map | Herm tile | Landing tile |
  |---|---|---|---|
  | `HERM_KALLISTE_ROUTE_1` | `MAP_KALLISTE_ROUTE1` | (14,20), the fork's herm | (14,21) |

- **What the player sees.**
  - With no Olive Oil: "A great herm, hung with old garlands. Hermes's face, worn smooth. Travelers anoint these with olive oil."
  - With oil: the same, then "Anoint it with olive oil? (You have 2.)" YES takes one Olive Oil, gives Hermes +1 Favor, chimes, and says "The oil runs down the old stone face. Somewhere, Hermes makes a note."
  - Anointed: "The great herm's face still shines with your oil. Hermes remembers you passed."
  - The last herm adds "Every great herm in Aethos shines with your oil now. Hermes is delighted!" It gives Hermes +10 more and sets `FLAG_ICHOR_ALL_HERMS_REWARD` (the Scroll of Deeds' stamp).
- **With Daedalus's Wings,** every anointed herm's route shows a lit dot on the fly map and is a fly target. The player lands on the herm's landing tile.
- **Count:** `specialvar(VAR_RESULT, Ichor_CountHerms)` returns the herms anointed and puts `HERM_COUNT` in `VAR_0x8004`, for the Scroll of Deeds ("Herms anointed: 7 of 23").

### A change to Route 1 (for the map owner)

Route 1's fork herm becomes its great herm. In `data/maps/KallisteRoute1/scripts.pory`:

```diff
 script KallisteRoute1_EventScript_HermFork {
     msgbox(format("East: Kronion Hill. North: Akti Town."), MSGBOX_SIGN)
+    lockall
+    call(EventScript_IchorAnointHerm)
+    releaseall
 }
```

## 5. The Frozen Hour (Phase 4 SCRIPT.md, Part 11, E1–E6)

Built in `src/ichor_frozen.c`. Tested by `tools/ichor/tests/ichor_frozen.sh` (21 checks on Route 1). The names are world-act3's.

### The mode (E1)

While `FLAG_ICHOR_FROZEN_HOUR` is set:
- **Every tileset and sprite palette is gray.** The exceptions are the player, the follower and any unfrozen object (E3). The tint lives in the unfaded palette buffer, so fades, warps, weather and battles all keep it. The day-and-night tint is off.
- **Everyone else is frozen,** including people who spawn later. A script's `lockall`/`releaseall` doesn't thaw them, and frozen trainers don't see you.
- **Talking to a frozen person** gives Phase 4's generic line (`EventScript_IchorFrozenGeneric`), never their own script, so frozen trainers don't battle:
  - "They don't move. They don't blink.", "Frozen mid-step, one foot off the ground." or "Caught halfway through a word.", by local id modulo 3;
  - "It's frozen with its ears up, listening for something." for a Pokémon object.
  - Inanimate objects (item balls, rocks) keep their own scripts.
  - **A map with frozen scripts of its own** calls `special(Ichor_FrozenScriptsHere)` in `ON_TRANSITION`. Then every object's own script runs. Those scripts check `FLAG_ICHOR_FROZEN_HOUR` themselves, and can `goto(EventScript_IchorFrozenGeneric)` for anyone without a line. Don't `faceplayer` a frozen person.
- **There are no wild encounters** on foot or surfing.
- **The map's music is `MUS_ICHOR_ELPIS_LULLABY_BOX`,** on every map.
- **Not built:** muting the field's own sound effects. Scripts' `playse` is unaffected anyway.

Setting the flag takes effect on the next map load. To freeze the map the player is on, use E2.

**Palettes are shared.** A sprite palette is gray or in color as a whole, so an unfrozen object that shares a palette with frozen ones colors them too. Give Phaedon, Hyperion, Kleon and the Fates palettes of their own.

### Calls

| Call | What it does |
|---|---|
| `setvar(VAR_0x8004, <x>)`, `setvar(VAR_0x8005, <y>)`, `special(Ichor_FrozenHourBegin)` | **E2, the gray spreading.** It starts at the Loom's tile (map coordinates). One palette goes gray every 6 frames: tileset palettes by the nearest on-screen tile drawn with them, sprite palettes by the nearest person wearing them. People freeze as it reaches them. Then the flag is set and the music box starts. The special waits until it's done; don't add `waitstate`. |
| `setvar(VAR_0x8004, LOCALID_...)`, `special(Ichor_UnfreezeObject)` | **E3, unfrozen objects.** Call it in the map's `ON_TRANSITION` for objects that should load in color (Phaedon, Hyperion, Elpis's music box, the pool's ripple). Called on someone standing frozen (Kleon waking), their color runs back in over 16 frames and they can move. The list resets on every map load. |
| `MOVEMENT_TYPE_ICHOR_FROZEN_STEP_DOWN`, `_UP`, `_LEFT`, `_RIGHT` | **E4, frozen poses.** The object holds its walk animation's stride frame in that direction. It's a normal movement type: set it in Porymap. |
| `special(Ichor_SepiaMemoryBegin)`, `special(Ichor_SepiaMemoryEnd)` | **E5, sepia memory.** The gray turns sepia for the memory, then back. It also works outside the hour, tinting everything but the player and follower. |
| `setvar(VAR_0x8004, <1–12>)`, `special(Ichor_ColorReturnStep)` | **E6, the color returns.** Each step brings back a twelfth of the color and is saved (`IchorSave.frozenHourStep`), so a map load mid-Stair keeps it. Step 12 clears the flag and brings back the day-and-night tint and the map's music. Frozen people thaw when the script ends: end it with `releaseall`, or they thaw once no script is running. |

### Still to build for Phase 4 (from Part 11)

E7–E18 are not in this batch: the bull-leap timing, statues, beams, large objects, herm heads, the reversed frieze, Melitta's cloak and the shadowless figure. E11, E13 and E15 are script-only. E12, the herm heads, needs only `FLAG_ICHOR_HERMS_START + HERM_<id>` (§4) and `setmetatile`.

## 6. The Labyrinth (LABYRINTH.md §5, §12)

Built in `src/ichor_labyrinth.c` and `data/scripts/ichor_labyrinth.pory`. Tested by `tools/ichor/tests/ichor_labyrinth.sh` (30 checks). The test uses Route 1 as a stand-in ring and borrows ordinary metatiles as the thread's twins.

### A ring's map scripts

```
// ON_LOAD
setvar(VAR_0x8004, <floor metatile>)          // a floor that takes thread (up to 4)
setvar(VAR_0x8005, <its first twin>)          // ten twins in a row, in the order below
special(Ichor_AddThreadFloor)

setvar(VAR_0x8004, <x>)                       // a bronze ring (up to 8)
setvar(VAR_0x8005, <y>)
setvar(VAR_0x8006, THREAD_ANCHOR_...)         // its name in RETURN TO…
special(Ichor_AddThreadAnchor)

setvar(VAR_0x8004, <x>)                       // a cracked wall Asterion can break (up to 8)
setvar(VAR_0x8005, <y>)
setvar(VAR_0x8006, FLAG_ICHOR_...)            // set when it breaks; 0 for none
setvar(VAR_0x8007, <broken metatile>)
special(Ichor_AddCrackedWall)

// ...draw broken walls (by their flags), dials, the Turning's layout...
special(Ichor_DrawThread)                     // last

// ON_TRANSITION (or ON_LOAD)
setvar(VAR_0x8004, LOCALID_...)
special(Ichor_StartAsterion)
```

- **The twins of each floor** are ten metatiles in a row: the straights H and V; the corners NE, NW, SE, SW (named for the two sides they join); and the end caps N, S, W, E (named for the one side they join). With two floors that is 20 twins, the art list's count.
- **Anchor names** are `THREAD_ANCHOR_*` in `include/constants/ichor.h`, with their strings in `src/data/ichor_thread.h`. Add Ring I–VII's names there. `THREAD_ANCHOR_UNNAMED` shows the map's name.
- **`MB_ICHOR_LIGHT_POOL`** is the metatile behavior for skylight pools (Ring V).

### Ariadne's Thread, as built

- **Laying is automatic** on a map that registered floors, while the Thread is in the bag. Floors and bronze rings take thread. On anything else (stairs, doorways) the thread waits at its end.
- **Stepping back onto the thread's last tile winds it up.**
- **The spool** is 150, 120 or 100 tiles: Mortal, Hero and Spartan are `DIFFICULTY_EASY`, `_NORMAL` and `_HARD`. "The spool is nearly empty." shows at 10 left.
- **Segments.**
  - Each map's segment starts where the player enters. On a bronze ring it starts tied, so each ring's entrance ties itself.
  - Leaving the map commits the segment.
  - Thread is redrawn over whatever is there, except bronze rings, so a wall from the Turning or a dial on a committed tile is drawn open again. That's why `Ichor_DrawThread` goes last.
- **The Relic Ring's THREAD** (or the bag), on a threaded map:
  - TIE OFF, on a bronze ring: commits the thread, refills the spool, and makes this the ring a knockdown returns to.
  - RETURN TO…: tied rings, newest first. It fades and warps there, and the live thread winds in. The Grand Staircase is listed once it's registered as a ring named `THREAD_ANCHOR_GRAND_STAIRCASE`.
  - WIND IN and LEAVE.
  - Off the Labyrinth, the Thread is the Escape Rope.
- **The Turning:** set `FLAG_ICHOR_THREAD_NO_RETURN`. RETURN TO… then says "The thread shakes in your hand. Walk it."
- **Saved** in `IchorSave.thread`: 24 anchors and 1,792 committed steps. The oldest segments are dropped when it fills.

### Asterion, as built

His own movement type is his patrol: `FACE_*` or `WALK_SEQUENCE_*`, set in Porymap. He does nothing while any script runs.

| | |
|---|---|
| **Sight** | Along his facing, stopped by walls. Its range comes from the player's tile: 3 on a dark tile; 7 in a skylight pool by day, 5 at night; 7 on a lit map or in a lit zone. With the Helm: 0 in the dark, 2 elsewhere. |
| **Hearing** | The player's steps, counted in tiles: walking 2, running 5. With the Helm: walking 0, running 3. |
| **Difficulty** | Mortal is 1 shorter and Spartan 1 longer, except the Helm's zeros. |
| **Listen** | He turns toward a step for 60 frames, then goes back to his patrol, facing as before. |
| **Alert** | "!" and a scrape. The player keeps control for 60, 40 or 30 frames, then he charges along that line at 4 frames per tile. |
| **Hitting the player** | Even half a step out of the way: "Asterion's charge sends you sprawling!" They wake at their current ring (or where they entered the map) with the live thread wound in. |
| **Hitting a wall** | Stunned for 120 frames (a "?" stands in for the stars), then he walks back to where the charge began. |
| **Hitting a registered cracked wall** | It becomes its broken metatile (passable), its flag is set, and the camera shakes. He stumbles into the gap, stunned for 60 frames. |
| **The bronze bell** | `setvar(VAR_0x8004, 30)`, then `special(Ichor_AsterionRest)`. He lies still (facing south) for that many of the player's steps, and wakes early if the player comes next to him. |

**Other chargers.** Labor 4's boar uses the same AI. Pass `ICHOR_CHARGER_*` bits in `VAR_0x8005` to `Ichor_StartAsterion`:

| Option | What it changes |
|---|---|
| `ICHOR_CHARGER_DEAF` | Sight only, no hearing. Outdoors his sight is the full 7 tiles. |
| `ICHOR_CHARGER_NO_RETURN` | After a stun he goes back to his movement type where he stands, instead of walking back up the charge line. |
| `ICHOR_CHARGER_HIT_SCRIPT` | A hit runs the object's own script, with `VAR_0x8004` = its local id and `VAR_0x8005` = `ICHOR_CHARGE_HIT`, instead of the knockdown warp; then he patrols again. The script does the knockback and the battle, and sets `VAR_0x8005` back to 0 so a later talk isn't read as a hit. |

**Snow drifts:** `setvar(VAR_0x8004, x)`, `setvar(VAR_0x8005, y)`, `setvar(VAR_0x8006, FLAG_...)`, then `special(Ichor_AddDrift)` in `ON_LOAD`, up to 8. A charge that runs into a drift ploughs in and sticks for 6 seconds, then goes on as after any stun, and the drift's flag is set so the map can count which drift caught him.

### The Helm of Darkness, as built

- **Wearing it** (`FLAG_ICHOR_HELM_ON`, the Ring's WEAR HELM) makes the player's sprite translucent.
- **Trainers can't see the player** on a dark tile: a dark map, outside lit zones and light pools. Elsewhere they see 2 tiles at most. Talking to them still starts the battle.
- **Asterion** follows the table above.

### Sentries and the disguise (§5.6)

- **Trainer types** (`include/constants/trainer_types.h`), set in Porymap:
  - `TRAINER_TYPE_ICHOR_TITANBORN`: sees in a line, as `TRAINER_TYPE_NORMAL` does.
  - `TRAINER_TYPE_ICHOR_SENTRY`: sees its own line, plus the lines either side of it from 2 tiles out, to its sight range (give sentries 5). Seen in a side lane, the sentry calls out from its post instead of walking over.
- **The disguise.** While `FLAG_ICHOR_DISGUISE_ON` is set, both types take the player for a recruit. They see nothing, unless the player runs within 3 tiles; then they see as usual.
  - Walking into one shows "Watch it, recruit." (`EventScript_IchorRecruitBump`), once until the player steps away.
  - Talking to one runs its own script, as always. Gigas elites, who question you instead, are script.
  - `FLAG_ICHOR_DISGUISE_ON` is the engine's: set it when the helmet goes on and clear it when it comes off. Having the helmet (`TITAN_DISGUISE` in LABYRINTH §13) is world-act3's flag.
  - **The sprite is not swapped yet.** The two helmeted walking sheets (decision L9) don't exist; this is LABYRINTH's "keep the mechanic, skip the sprite". When they land, the swap goes in `GetPlayerAvatarGraphicsIdByStateIdAndGender`, and the sheets need the player's animation table, running frames included.
- **The Helm** stacks with the disguise.

### Dials

```
copyvar(VAR_0x8004, VAR_ICHOR_LABYRINTH)   // the dials' positions
setvar(VAR_0x8005, <this dial's bit>)
call(EventScript_IchorDial)                // needs the Labrys; asks, or AUTO
copyvar(VAR_ICHOR_LABYRINTH, VAR_0x8004)   // saved back, turned or not
// VAR_RESULT: the wall's new position, 0 (A) or 1 (B); 0xFF if nothing turned.
// Swap the wall's metatiles, special(DrawWholeMapView), releaseall.
```

### Not built yet

- **Art:** the thread's twins, the skylight pools, Asterion's stars and lying-down frame, and the dust puff on his scrape.
- **Engine:**
  - the waypoint patrol for wall %2 (`MOVEMENT_TYPE_ICHOR_PATROL`);
  - the disguise's sprite (above);
  - the bull-leap (E7);
  - the mirrors and beam (E9);
  - the Endless Labyrinth.
- **Script-only, for world-act3:** the sun and moon gates, the dancing floor, the lift, the sunken floor and the alarms.

## 7. Scripts' small needs

Built in `src/ichor_save.c`, `src/ichor_time.c`, `src/ichor_omen.c` and `src/ichor_scene.c`. Tested by `make check TESTS="Ichor:"`, `tools/ichor/tests/ichor_world.sh` and the scene checks below.

### Story picture windows and the Act I title

`Ichor_ShowScenePicture(tiles, palette)` is the shared C renderer for a 64x64,
4bpp picture with sixteen colors. The restored-amphora wrapper and
`specialvar(VAR_RESULT, Ichor_ShowTabletPicture)` both use it. It borrows BG
palette 13, preserves both its unfaded and displayed colors, and returns
`FALSE` if a scene window is already open or allocation fails.
`special(Ichor_HideScenePicture)` clears and releases the window and restores
both palettes; repeated closes are safe. Close pictures before rewards,
another menu or a map transition. The existing amphora show/hide specials
retain their interfaces and restoration guard.

The revelation opens the tablet between Daphne introducing its back and
explaining the raking light, and closes it after her reading and its pause.
Regenerate the original indexed asset with
`python3 tools/ichor/art/tablet_back.py`; `make` converts the PNG.

After closing dialogue and its speaker plaque, fading the field to black and
calling `specialvar(VAR_RESULT, Ichor_ShowActOneCard)` opens the centered title.
It uses the original pottery frame, independent of the player's menu-frame
choice, and temporarily borrows BG palettes 14 and 15. Check for `TRUE`,
`delay(60)`, `waitbuttonpress`, then `special(Ichor_HideActOneCard)` before
showing the thank-you message or warping. It cannot coexist with a picture;
its close is idempotent and restores both unfaded and displayed palettes.
The revelation reports either allocation failure explicitly without losing
its already-earned reward or trapping the player.

`tools/ichor/tests/sanctum.sh` exercises both actual revelation branches,
compiled tablet pixels, palette restoration, speaker continuity, A and B
title acknowledgment, window cleanup, full-Bag retry and saved/repeated
completion. `tools/ichor/tests/amphorae.sh` checks all twelve paintings through
the shared renderer.

### The revelation's one-lamp lighting

The Demeter hall's generated `DrawRevelation` overlay applies between Kleon's
departure and Daphne's completed revelation. It keeps the raid's overturned
front braziers, extinguishes other flames and places one clay lamp beside
Daphne at `(13, 23)`, without changing saved brazier flags. Map transition sets
`ICHOR_FLASH_TORCH`; the revelation also uses `animateflash` and `setflashlevel`
after positioning the cast, so a full-Bag retry cannot inherit full brightness.
The lamp flickers through the authored sixty-frame pause. Regenerate its
overlay and flicker script with `python3 tools/ichor/maps/temple_demeter.py`.

This is map-local staging, not a change to Torch ownership, dousing, upgrades
or the tint preference. Normal map entry restores the room and personal Torch
radius after completion; entering outdoors clears native Flash as usual.
The sanctum regression counts all flames, samples the real flicker script,
retries from full brightness, exercises doused and upgraded Torches with native
Flash, and checks normal reentry and saved brazier progress.

The temple hymn continues through the scene's opening. At “She didn't see one
at all”, `playbgm(MUS_ICHOR_REVELATION, FALSE)` starts the existing original
score with its sustained aulos D4. Do not save this as a map-music override:
the Chart fanfare resumes it automatically, while the exit and normal reentry
must restore Eleusa's theme and the temple hymn respectively. Both dialogue
branches check those transitions and the intro's single active D4 voice;
full-Bag refusals leave the temple hymn playing.

### Counting flags

`setvar(VAR_0x8004, FLAG_ICHOR_PROPHECY_START)`, `setvar(VAR_0x8005, 8)`, `specialvar(VAR_RESULT, Ichor_CountFlagRange)`: how many of those flags are set. It works on any flag range: a bank, a vanilla range or the daily flags.

### A party Pokémon's level

`specialvar(VAR_RESULT, Ichor_GetHighestPartyLevel)` gives the level of the strongest Pokémon in the party, not counting Eggs. "Level thirty strong?" is `if (var(VAR_RESULT) >= 30)`.

### The DAY/NIGHT TINT option

**The setting.** The options menu has a DAY/NIGHT TINT row, ON or OFF. It's saved in `IchorSave.options` (`ICHOR_OPTION_TINT_OFF`, clear by default), so a new game is ON.

**ON** is the expansion's day-and-night tint (`OW_ENABLE_DNS`), as before.

**OFF** draws the overworld in daytime colors at every hour. Only the colors change:
- `gTimeOfDay` and `GetTimeOfDay()` still follow the clock. So do the time-of-day encounter tables, night music, night-only events, Hecate's night test, the xenia rest and the omens.
- Night lamps don't glow.

**Not affected by the setting:**
- A script's held tint (`Ichor_HoldTimeOfDay`, such as Delphoi's night) shows whatever the setting.
- The Frozen Hour's gray and its color return are their own system.

**For C code:** `Ichor_IsTintOff()` is TRUE when OFF is chosen and no tint is held.

### The xenia rest (SYSTEMS §10)

A host's bed moves the clock forward to dawn (06:00), noon (12:00), dusk (19:00) or night (20:30), never back and never past midnight. The menu offers only the hours still ahead today, then NOT NOW:

```
msgbox(format("Stay, if you like. Rest till you want to wake."))
call(EventScript_IchorXeniaRest)
if (var(VAR_RESULT) == TRUE) {
    special(HealPlayerParty)
    msgbox(format("{PLAYER} slept behind the striped curtain and woke well rested."))
}
```

- **What it does:** it asks "Rest until when?", fades to black, moves the clock, waits a second and fades back. The tint follows at once.
- **`VAR_RESULT`** is `FALSE` for NOT NOW, or when no hour is left (after 20:30). The healing and the host's words are the map's.
- **From C,** `special(Ichor_RestUntil)` with an `ICHOR_REST_*` in `VAR_0x8004` moves the clock without the menu.

### Holding the day-and-night tint

- **`setvar(VAR_0x8004, TIME_EVENING)`, then `special(Ichor_HoldTimeOfDay)`.** The tint holds at that time of day, whatever the clock says. The hold lasts through warps and saves until `special(Ichor_ReleaseTimeOfDay)`. It takes `TIME_MORNING`, `TIME_DAY`, `TIME_EVENING` or `TIME_NIGHT`, each at full strength.
- **`specialvar(VAR_RESULT, Ichor_GetTimeOfDay)`.** Returns the current
  `TIME_*` value, including a script's held time. DAY/NIGHT TINT OFF is visual
  only and does not turn nighttime gameplay into daytime. The underlying C
  `GetTimeOfDay` is not itself a script special.
- **It's the game's time of day while held,** not just the colors. Encounter tables and time-based evolutions follow it, so night falls at Delphoi for the Pokémon too.
- The tint only shows on maps with natural light (towns, routes and the sea), so interiors look the same either way.
- The expansion's own `SetTimeOfDay` hour override still works, but it resets on every warp. Use the hold for anything that spans maps.

### Knucklebones (SYSTEMS §9)

A best-of-five match, played in the message box with a menu. The map gives the opponent's personality in `VAR_0x8004` and their name, as prose, in `STR_VAR_3`:

```
bufferstring(STR_VAR_3, ThyrsaCity_Tavern_Text_Glauke)   // text … { "Glauke" }
setvar(VAR_0x8004, ICHOR_BONES_BOLD)
call(EventScript_IchorKnucklebones)
if (var(VAR_RESULT) == TRUE) { ... you won ... }
```

**Each throw:**
1. You see your four bones: "3  1  4  4  (12)".
2. A menu lists each bone as KEEP or ROLL (A switches it), then ROLL THEM (once one is marked) and STAND. B also stands.
3. The opponent throws and rethrows as they play.
4. The higher sum takes the throw, and a tie is thrown again. Aphrodite (1, 3, 4, 6) beats everything; the Dog (four 1s) loses to everything.
5. The score shows ("2-1"). The first to three wins.

**The opponents** (`ICHOR_BONES_*`):

| Value | Plays |
|---|---|
| `_CAUTIOUS` | Rethrows only its 1s |
| `_BOLD` | Holding three different sides, rethrows the spare to chase Aphrodite. Otherwise, its 1s. |
| `_SILENOS` | Loaded bones: a 6 comes up 30% of the time. After two throws in a row with two 6s or more, LOADED! appears in your menu; calling it wins the match at once ("“Loaded!” Silenos goes very still."). |
| `_MOM` | Until `FLAG_ICHOR_MOM_CONFESSED`, the bee: two rethrows and faces 5/30/30/35. You win about 1 match in 18, as SYSTEMS §9 says. After the confession she plays fair, so it's about even. Every match goes on her record. |

Nobody breaks up an Aphrodite.

**Mom:**
- `specialvar(VAR_RESULT, Ichor_GetMomRecord)` gives your wins against her, with her wins in `VAR_0x8004`, for the 2F text. The record starts at 0–212.
- **Her first loss:** the map shows her lines and gives `ITEM_APHRODITE_BONE`, a key item that adds one rethrow a match.
- **`FLAG_ICHOR_MOM_CONFESSED`** (engine-owned, bank offset 0x483) is set by world-act3 at the Kastalian spring (STORY III-7).

**Left to the map:** prizes, the champions' flags and the lines around the match. There are no wagers.

### The festival calendar (SYSTEMS §7)

**The year.** An Aethos year is 36 days on the day counter (`VAR_DAYS`): 12 months of 3 days, and each month's festival on its middle day. So a festival comes every three days, and Maimakterion, the month of storms, has none.

**The calls:**
- `specialvar(VAR_RESULT, Ichor_GetFestival)` gives today's `ICHOR_FESTIVAL_*`, or `ICHOR_FESTIVAL_NONE`. A town dresses for its festival in `ON_TRANSITION`: decoration hide flags, music and an alternate market list.
- `specialvar(VAR_RESULT, Ichor_GetMonth)` gives the `ICHOR_MONTH_*`, with the day of the month (0–2) in `VAR_0x8004`.
- `setvar(VAR_0x8004, ICHOR_FESTIVAL_PANATHENAIA)`, then `specialvar(VAR_RESULT, Ichor_DaysToFestival)`, gives the days until that festival comes (0 means today): "The Panathenaia is in 4 days."
- `specialvar(VAR_RESULT, Ichor_JoinFestival)`: the player takes part. The first time on a festival day, its god gives +5 Favor and `VAR_RESULT` is `TRUE`. The daily flag is `FLAG_DAILY_ICHOR_FESTIVAL_JOINED`. The Kronia has no god to give Favor.

**By itself, the engine runs only the Anthesteria:** at night, Ghost-types come about three times as often on land. Everything else on a festival day is the town's script, and the main path never needs a festival (the Act II Dionysia is story time).

The Scroll of Deeds' calendar page reads this schedule and the current
`VAR_DAYS`. **Not built:** `IchorSave.festivalsSeen` and the remaining festival
world events.

### Theoxenia's tells (SYSTEMS §10)

A god in disguise is an object event whose trainer type is **`TRAINER_TYPE_ICHOR_GOD`** (Porymap's trainer type field; give it no sight range). The engine then gives three of §10's tells:

1. **No shadow.** Every other object has one (`OW_OBJECT_VANILLA_SHADOWS` is off).
2. **The follower bows** once it is within 3 tiles of the god and the player stands still: it turns to the god and dips. It bows again only after leaving that range.
3. **The Augur's Eye** shows "Something here is watching you." in place of its top line, on any map where a disguised god stands.

**Left to the map:**
- The detail that doesn't fit (the third tell) is the god's art.
- The tests and the reveal are scripts.
- A Stranger omen (§6) is a row in `src/data/ichor_omens.h`.

**Other uses:**
- **The reveal:** when the god drops the disguise, swap the object's graphics. If you swap it for an ordinary object, the shadow comes back.
- **Decoys** are ordinary objects: shadows, and no bow.
- **Phase 4's E18, the shadowless figure,** is a `TRAINER_TYPE_ICHOR_GOD` object as well.
- **The visit flags** are `FLAG_ICHOR_THEOXENIA_START + ICHOR_GOD_*`, as §1's table gives them.

### Omens (SYSTEMS §6)

- **Today's omen** is `IchorSave.omenKind` (`OMEN_SWARM`, `_VISITOR`, `_WEATHER`, `_GOOD_SIGN`, `_STRANGER`, or `OMEN_NONE`) and `omenEntry`, an entry within that kind. The entries are numbered in `include/constants/ichor.h`; append new ids without renumbering existing saved entries.
- **Forcing tomorrow's omen,** as when Akanthis first tells the Lernip rumor: `setvar(VAR_0x8004, OMEN_WEATHER)`, `setvar(VAR_0x8005, OMEN_WEATHER_LERNIP)`, `special(Ichor_ForceOmen)`.
- **A map that owns an omen's weather** checks it in `ON_TRANSITION`:
  ```
  setvar(VAR_0x8004, OMEN_WEATHER)
  setvar(VAR_0x8005, OMEN_WEATHER_LERNIP)
  specialvar(VAR_RESULT, Ichor_CheckOmen)
  if (var(VAR_RESULT) == TRUE) { setweather(WEATHER_RAIN) }
  ```
- `specialvar(VAR_RESULT, Ichor_GetOmen)` gives the kind, with the entry in `VAR_0x8004`. The augurs use it: Halitherses and Manto switch on the kind and entry for their line.
- **The daily draw.** Each new day without a forced omen draws one:
  - **The kind** comes by SYSTEMS §6's weights: swarm 35 (45 before any stranger can walk), visitor 25, weather 20, good sign 10, stranger 10. A kind with no open entry isn't drawn.
  - **The entry** is then one of that kind's rows in `src/data/ichor_omens.h` whose `unlockFlag` is set and whose `lockFlag` isn't. So augurs only name places the player can reach.
  - **A good sign** needs no rows. Half the time it is `OMEN_SIGN_BLESSING` (the augur grants a minor blessing with `Ichor_GrantBlessing`, §3). Otherwise it is `OMEN_SIGN_LUCKY(1)`–`(6)`, today's lucky number.
- **What an omen does by itself:**
  - **A swarm** starts the expansion's mass outbreak for the day: half the row's `map`'s land encounters are its `species` at its `level`, with the species' own moves.
  - **A visitor's object** shows only on its day. Each new day the engine sets every visitor's `hideFlag`, then clears today's. A map's script sets it again once the visitor is caught or beaten.
  - **Live rollover** queues a field refresh after the daily draw. Once the
    player is stationary and no script, fade or Frozen Hour is active, expired
    visitor objects are removed and visible new arrivals are spawned. A new
    arrival waits if the player occupies its tile. This does not respawn a
    same-day consumed visitor or remove Emporion's permanent marked jar.
  - **Weather** is generally the map's `ON_TRANSITION`, as above. Eleusa uses
    `special(Ichor_SetOmenWeather)` to select sun or normal weather from the same
    policy as live rollover; the field refresh updates both saved and live weather.
- **Adding an omen.** Number it in `include/constants/ichor.h` (`OMEN_SWARM_*`, `OMEN_VISITOR_*`, `OMEN_WEATHER_*`), then add a row:
  ```
  { .kind = OMEN_SWARM, .entry = OMEN_SWARM_ROUTE6, .unlockFlag = FLAG_ICHOR_ARRIVED_ELEUSA,
    .species = SPECIES_..., .map = MAP_ROUTE6_ELEUTHERAI_ROAD, .level = 18 },
  { .kind = OMEN_VISITOR, .entry = OMEN_VISITOR_THYRSIVY, .unlockFlag = FLAG_ICHOR_DIONYSIA_DONE,
    .hideFlag = FLAG_ICHOR_HIDE_OMEN_THYRSIVY },
  ```
  Reachable Act I rows now include Kerazap on the cleared Isthmus (level 18)
  and Skiron road (19), Melibee (20) and Stachyss (21) in Eleusa, and Eleusa sun
  weather. The latter four unlock on arrival in Eleusa. Swarm ids 2-5 preserve
  the reserved Act II entries 0/1. Eleusa's transition clears the previous
  weather before applying today's sun. Later rows remain progress-gated;
  Eleusa's `OMEN_VISITOR_ELEUSA_KORANTHA` (2) is registered at (17,35), level 22,
  with `FLAG_ICHOR_HIDE_OMEN_KORANTHA`. Capture/defeat hides it until another
  matching omen; escape/loss does not. Map entry hides off-day visitors even
  on legacy saves with an unset new flag. Interaction also rejects an expired
  visitor if the day changes while the player stays in the wheat. The daily
  draw now queues the live refresh described above.
  Emporion's `OMEN_VISITOR_EMPORION_PITHOUND` (3) unlocks on the first city
  visit. Only the westernmost stoa jar at (10,24), whose description identifies
  a scratched paw-print, starts this level-16 visitor. Its BG script checks the
  current omen on every interaction and uses `FLAG_ICHOR_HIDE_OMEN_PITHOUND`
  as today's consumed state, not as a flag to hide the jar. Capture/defeat
  consumes the visit; loss/escape keeps it available. The other five jars retain
  their ordinary one-in-four level-14-16 encounters.
  `OMEN_VISITOR_ISTHMUS_NEMECUB` (4) unlocks when the Isthmus rockslide is
  cleared. The level-18 golden cub stands in the hill-spur scrub at (28,3).
  `FLAG_ICHOR_HIDE_OMEN_NEMECUB` records capture/defeat for that visit; loss and
  escape preserve it. Entry and interaction reject off-day visitors, including
  legacy saves and an on-map day change.
  `tools/ichor/tests/omen_rollover.sh` checks actual midnight field-clock
  rollover without map reentry: Korantha and Nemecub arrival/expiry, same-day
  consumption, script/Frozen Hour deferral, occupied-tile arrival, and
  Eleusa's saved/live sun onset and expiry.
- **Halitherses's reading** uses the actual saved kind/entry and
  `FLAG_DAILY_ICHOR_AUGURY_READ`. A good-sign blessing asks before replacing
  the current blessing, grants Hermes 100 steps without Favor, and cannot be
  refreshed by another conversation or map reentry. Declining keeps the old
  blessing; an absent omen does not consume the day's reading.

### Four time-of-day encounter tables on one map

These need no engine change. `OW_TIME_OF_DAY_ENCOUNTERS` is on, and `tools/wild_encounters/wild_encounters_to_header.py` builds one table per time of day.
- **In `src/data/wild_encounters.json`,** give the map up to four entries with the same `map` and `base_label`s ending `_Morning`, `_Day`, `_Evening` and `_Night`. Route 1 already has `gKallisteRoute1_Morning` and `_Night`.
- **The hours** (`OW_TIMES_OF_DAY`, latest generation): morning 6–10, day 10–19, evening 19–20, night 20–6.
- **A time with no table of its own falls back to `_Morning`** (`OW_TIME_OF_DAY_FALLBACK`). With all four defined, Lakonia's Chalkip can sit in `_Morning` and `_Evening` only.

## 8. Excavation (SYSTEMS §5)

Alethea gives the Trowel with `giveitem(ITEM_ALETHEAS_TROWEL)` (a key item). Every dig spot is a bg event, or an object, whose script sets two vars and goes to one of two scripts:

Act I's integrated daily indices are 0 (Emporion shipsheds), 1 (Hephaisteion
garden), 2/3 (Eleusa west/east fields), and 4/5 (Isthmus kilns/hill spur).
The Isthmus pair use the Arachne amphora and independent daily flags. Fixed
index 0 is Emporion's quay planter; index 1 is the Isthmus family tomb's
Arachne sherd, behind the existing Act II Girdle gate. Do not reuse these indices.
Fixed index 2 is the sanctum B1F Persephone sherd behind bay B's great jar;
it requires the Trowel and stays consumed across reentry and saved games.
Fixed index 3 is Daedalus's page II in sanctum B3F's exposed foundations.
The cave-in must have happened before excavation; ownership uses the canonical
page flag `FLAG_ICHOR_PAGES_START + 1`, with no extra general-bank flag.

```
// A daily spot: dug once a day; its find is rolled from the day's seed and the spot
setvar(VAR_0x8004, <spot index>)       // FLAG_DAILY_ICHOR_DIG_START + index: dug today
setvar(VAR_0x8005, ICHOR_DIG_ACT_I | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_ARACHNE))
goto(EventScript_IchorDigSpot)

// A fixed find: dug once, ever
setvar(VAR_0x8004, <find index>)       // FLAG_ICHOR_DIG_FIXED_START + index: dug
setvar(VAR_0x8005, ITEM_RARE_BONE)     // an item, or ICHOR_FIND_SHERD(ICHOR_AMPHORA_*),
                                       // ICHOR_FIND_PROPHECY(1-8), ICHOR_FIND_PAGE(1-7), ICHOR_FIND_OSTRAKON
goto(EventScript_IchorDigFixed)
```

**A daily spot's `VAR_0x8005`:**
- The table: `ICHOR_DIG_ACT_I`, `_ACT_II` or `_ACT_III` (Act III and the post-game). These are SYSTEMS §5's tables.
- The amphora, if the spot holds sherds: `| ICHOR_DIG_SHERDS(ICHOR_AMPHORA_*)`. The twelve `ICHOR_AMPHORA_*` names follow §5's table (`_KRONOS` is Kalliste, `_PERSEPHONE` Eleusa, `_ARACHNE` Emporion, and so on).

**Registered Act I daily spots:** harbor ship sheds 0, Hephaisteion garden 1
(Arachne), Eleusa west field 2 and east meadow 3 (Persephone). The village's
two BG events use separate index-setting wrappers and a shared loot caller;
never share a daily index between sites. See `tools/ichor/claim_ranges.md`.
Kalliste's three daily spots use indices 6 (Kronion Hill's pried-up slabs),
7 (Route 1's bee terraces) and 8 (Akti's beach shells), all with the Kronos
amphora and Act I loot. They are BG interactions on visible map details, not
objects removed by a dig; their consumed flags clear at midnight without
requiring reentry. The existing map generator owns both Route 1 and Kronion
events and the terrace's turned-earth tile.
- A spot with no amphora never gives a sherd: the roll goes again. So does a sherd roll once all four of its amphora's sherds are collected, and an ostrakon roll once all 30 are found. Collection does not set the restored-amphora flag.

**What a dig does:**
- **Without the Trowel,** it says the earth has been turned and something glints in it.
- **With it,** the player raises the Trowel (the relic pose), dust puffs on the tile and the find comes up.
  - Items go in the Bag. If it's full, nothing is dug, and the spot stays.
  - A sherd sets the amphora's next flag (`FLAG_ICHOR_SHERDS_START + 4 × amphora + n`) and says "*n* of its 4 pieces".
  - An ostrakon sets the next of `FLAG_ICHOR_OSTRAKA_START + 0–29`, in order, and shows its words. The 30 are in `src/ichor_dig.c` (`sOstraka`). Nine name Aristeides, for Lysimachos, and the last is the player's. Writers may rewrite any of them.
  - Tablet *n* sets `FLAG_ICHOR_PROPHECY_START + n − 1`, and page *n* sets `FLAG_ICHOR_PAGES_START + n − 1`. Alethea's reading, or the page's text, is the map's own script (see below).
- **Afterwards,** a daily spot says "dug today" until tomorrow, and a fixed find says "nothing else is buried here".
- **A fixed find with nothing left to give** (a sherd whose four-piece collection is already complete) gives Stardust instead.
- **Rolls are seeded by the day's seed and the spot,** so reloading a save digs up the same thing.
- **Blessings:** Demeter's rolls twice and keeps the rarer find. Hades's doubles an item from a daily spot.
- **Loot that waits on other work:** the fossils are Kanto's and Hoenn's until the dex adds the Aethos fossils. The 1% Ichor Stone is one of ten Mega Stones; Balance may change the list in `sIchorStones`.

**A dig-spot object** (turned earth drawn as an object) takes the dig's flag as its own (`FLAG_DAILY_ICHOR_DIG_START + spot` or `FLAG_ICHOR_DIG_FIXED_START + index`). The dig removes it. A daily spot's object comes back the next day.

**After the dig.** Both scripts work as a `goto` or a `call`. After a `call`, `VAR_RESULT` is `TRUE` if something was dug up just now, so a map can follow a tablet with Alethea's reading:

```
setvar(VAR_0x8004, 0x12)
setvar(VAR_0x8005, ICHOR_FIND_PROPHECY(3))
call(EventScript_IchorDigFixed)
if (var(VAR_RESULT) == TRUE) {
    // Alethea reads tablet 3
}
```

**The coins** are renamed, and sell at any market for these (a quarter of their price, the expansion's Gen 9 rule; Hades's blessing +50%):

| Item | Name | Sells for |
|---|---|---|
| `ITEM_RELIC_COPPER` | Bronze Obol | ¥500 |
| `ITEM_RELIC_SILVER` | Silver Owl | ¥2,000 |
| `ITEM_RELIC_GOLD` | Gold Stater | ¥5,000 |

A moneychanger (Pasion in Emporion, Astyra's) pays the market's price plus his own percent, with any blessing counted:

```
setvar(VAR_0x8004, ITEM_RELIC_SILVER)
setvar(VAR_0x8005, 20)                       // +20%
specialvar(VAR_RESULT, Ichor_SellToMoneychanger)
if (var(VAR_RESULT) == TRUE) {
    playse(SE_SHOP)
    msgbox(format("He pays you ¥{STR_VAR_1}."))
}
```

Call `specialvar(VAR_RESULT, Ichor_QuoteToMoneychanger)` with the same inputs
before confirmation to buffer the payment in `STR_VAR_1` without removing the
coin. Both calls return `FALSE` if the item is missing, cannot be sold, or its
full payment would exceed the money cap. A refused sale leaves the item and
money unchanged; the sale rechecks capacity. With no blessing, +20% is ¥600,
¥2,400 and ¥6,000.

**Index blocks** for dig spots are in §1's table. Ask the engine session for more.

### Amphora restoration

The Akademia's three shelf BG events enter `EventScript_IchorAmphoraShelf`.
This is a self-service shelf with Daphne's written notes, available after she
leaves for the Mysteries; it does not change her location or require an invented
attendant. Its scrolling menu shows only collected or restored myths, in
canonical `ICHOR_AMPHORA_*` order, with a piece count or `whole` label.

The player must explicitly confirm assembling four sherds. Partial collections,
menu cancellation and declined confirmation leave the restoration flag unset.
Restoration sets `FLAG_ICHOR_AMPHORAE_START + amphora`, retains all four collected
flags, and grants Hephaestus or Aphrodite five capped Favor once for their
respective myths. A legacy restored flag remains readable even without sherds
and does not grant Favor again.

With an amphora id in `VAR_0x8004`:
- `Ichor_BufferAmphora` returns `ICHOR_AMPHORA_INCOMPLETE`, `_READY`,
  `_RESTORED` or `_INVALID`, buffering the name/count in `STR_VAR_1/2` when valid.
- `Ichor_RestoreAmphora` rechecks eligibility and returns the resulting status.
- `Ichor_BufferAmphoraNotes` returns `TRUE` and copies the notes to `gStringVar4`
  only for a restored amphora.
- `Ichor_ShowAmphoraPicture` returns `TRUE` only after opening the 64x64 window.
  `Ichor_HideAmphoraPicture` releases it and restores the borrowed BG palette.
  Close it before another menu, map transition or reward.

`Ichor_BuildAmphoraMenu` puts its count in `VAR_RESULT`; zero means no entries,
and `ICHOR_AMPHORA_MENU_ERROR` is an explicit allocation failure. The menu owns
and frees its labels. Finish its dynamic selection before showing a painting.

The twelve panels use one 16-color palette, no secondary-tileset capacity,
and 24,576 bytes of uncompressed 4bpp graphics. Regenerate their indexed PNG with
`python3 tools/ichor/art/amphorae.py`; `make` supplies the `.4bpp` and `.gbapal`.

All twelve **restored** flags unlock the last page and one Ability Patch.
`FLAG_ICHOR_GOT_AMPHORA_PATCH` is set only after `giveitem` succeeds; pending
and claimed rewards persist across CONTINUE. Forty-eight collected sherds alone
do not qualify. Later-region world callers remain to
integrate; the shelf and Scroll of Deeds record their canonical restored-amphora gates and clues,
not an automatically finished encounter.

**Checks:** `tools/ichor/tests/ichor_dig.sh` (15 checks on Route 1) and `make check TESTS="Ichor:"` (`test/ichor_dig.c`: the rolls, rerolls, act tables and blessings).
`tools/ichor/tests/amphorae.sh` exercises all twelve real shelf choices and
paintings, cancellation, explicit restoration, Favor, saved/full-Bag collection
rewards and repeated reading. `tools/ichor/tests/kalliste_digs.sh` also follows
four actually excavated Kronos sherds through shelf restoration and CONTINUE.

### The Act I amphora encounters

Checking Kronion's existing broken altar after restoring Kronos offers
Cairnolith Lv20 at `TIME_NIGHT`, with Sand Force and a held Hard Stone.
`FLAG_ICHOR_KRONION_ALTAR_STONE` records capture or victory, not an approach,
escape or whiteout. Both existing altar BG events share this state.

The Hollow's web chamber similarly uses the canonical Arachne restoration
flag to reveal Raknit Lv20 with Defiant. `FLAG_ICHOR_HOLLOW_RAKNIT` records
its outcome. Claimed Raknit is hidden/removed immediately and its interaction
rechecks eligibility, closing same-map repeats.

`Ichor_SetPersephoneVisitor` derives `FLAG_ICHOR_HIDE_AMPHORA_PERSENYX` only
on Eleusa's map: show the object at (37,33) if Persephone is restored,
`FLAG_ICHOR_ELEUSA_PERSENYX` is unset and the time is `TIME_EVENING`. The
map transition calls it before object placement; the safe field refresh
also handles clock boundaries without leaving the map. Scripts, palette
fades, the Frozen Hour, player movement and an occupied arrival tile defer
that refresh. Its Lv22 battle is optional, and only capture/victory claim it.
These are independent of daily omen draws and do not reset on another day.

`tools/ichor/tests/amphora_leads.sh` restores the three myths through the real
shelf and exercises exact enemy levels/abilities/items, declined approaches,
escape, whiteout, victory, actual ball captures, save/CONTINUE and live dusk
boundaries. The battle-strength assist is not natural-level balance approval.

## 9. Scroll of Deeds

`src/ichor_deeds.c` reads existing saved receipts; opening the journal never
sets a quest flag, restores an amphora, consumes an item or claims a reward.
The ordinary and debug start menus use the cut PokéNav's slot for **DEEDS**
when `ICHOR_CUT_POKENAV` is enabled, preserving the nine-entry action buffer.
The trainer card and special-mode menu builders are unchanged. The script
uses standard pottery-framed scrolling choices and field messages, with
B returning to the contents and then releasing field controls.

- `Ichor_DeedState(deed)` returns `ICHOR_DEED_HIDDEN`, `OPEN`, `DONE` or
  `RECORDED`. Story ids 0–11 follow the first partner, Hearth Laurel, crossing,
  Herald Laurel, Harvest Laurel, Mysteries night, stolen fragment, Kleon's
  departure, revelation, letter, Mom's parcel and Daedalus's seven pages.
  An existing completion receipt remains readable even if an older save
  lacks the prerequisite receipt.
- Amphora ids are `ICHOR_DEED_AMPHORA_START + myth` (16–27). No sherds means
  hidden; four sherds remain an open restoration. Only a restored myth
  reveals its lead. The three Act I capture/victory receipts mark their
  leads done; later leads are **recorded**, not fictitiously completed.
- `Ichor_BuildDeedsMenu` takes category 0 (contents), 1 (Act I) or 2
  (amphorae) in `VAR_0x8004`, and the previous selection id in `VAR_0x800A`.
  It queues separately allocated labels for `dynmultistack`, returns the
  count in `VAR_RESULT`, and supplies the resumable **item id**, not row
  number, in `VAR_0x8000`. Allocation failure cleans queued labels and
  returns `ICHOR_DEEDS_MENU_ERROR`; the script displays an explicit error.
- `Ichor_BufferDeed` takes a page id in `VAR_0x8004`, writes the message to
  `gStringVar4`, preserves the id and returns TRUE. Hidden/invalid ids return
  FALSE with an explanatory message. Athena's Stylus adds hints only to
  open pages; Daedalus hints follow which of the first two pages is missing.
- `ICHOR_DEED_HERMS` (40) reads `Ichor_CountAnointedHerms` and `HERM_COUNT`,
  without counting post-game waystones as Aethos herms.
- `ICHOR_DEED_CALENDAR` (41) shows the current month, day of three and
  time until that month's next festival, using `Ichor_DaysToFestival`.
  Maimakterion explicitly has no festival. This is a schedule, not festival
  attendance or a claim that all twelve world events have been built.

`test/ichor_deeds.c` covers story gates, pending gifts, all twelve myths,
Stylus hints and two complete calendar years.
`bash tools/ichor/tests/deeds.sh` exercises the real start-menu callback,
empty pages, scrolling, read/back navigation, the retained trainer card,
field-control release and save/reset/CONTINUE.

## 10. Star Chart

`ITEM_STAR_CHART` opens `src/ichor_star_chart.c` through the real Bag's USE
action. BG2 holds the parchment sky, BG1 holds 24 original star-and-line
patterns and the selected patch, and BG0 holds the count, name and controls.
Only placed patterns appear. Unplaced names remain hidden, including the
Unwoven until its eventual credits caller. D-pad movement wraps through
six columns and four rows; B frees the chart's windows and tilemaps and
returns to the same Bag pocket. Placed stars cycle between two gold shades.
Allocation failures display an explicit retry message rather than claiming
the screen opened.

The Bag uses an original 24x24 rolled-sky icon and its own sixteen-color
palette, not the Town Map's graphics. Regenerate just this asset with
`python3 tools/ichor/art/items.py --write --only star_chart`; the focused
option retains the generator's shared-palette checks without rewriting
other icon PNGs or the ground jar.

### Outdoor seats

Kronion Hill's eastern shrine steps at `(15, 8)`, approached from `(15, 9)`,
run `EventScript_IchorSkySeat`. The summit stele explains the seat; the route
builder preserves the event and checks reachability without changing terrain.
The shared script requires the real Chart, night and an affirmative answer,
then fades to black and calls `specialvar(VAR_RESULT, Ichor_ShowNightSky)`.
On `TRUE`, `waitstate` waits for the screen; on immediate `FALSE`, fade back in.
Screen-initialization failure resumes with `FALSE` and the script reports an
explicit retry message. The native entry also rejects indoor, daytime,
missing-item and already-open callers.

The sky shares the portable view's patterns, selection and saved flags, but
uses its own midnight-blue palette, pale twinkling stars and field-exit label.
B releases its resources and uses `CB2_ReturnToFieldContinueScript`, retaining
the seat's position and music. It does not consume the Chart or change the
held time, tint option or weather. The portable view still returns to its
original Bag pocket. No new save field or milestone reward is introduced.

### Saved placements

The existing `FLAG_ICHOR_CONSTELLATIONS_START` range stores one saved bit
per constellation, in SYSTEMS §8 order (indices 0–23). This uses the already
reserved flag bank instead of introducing a new `IchorSave.constellations`
field or changing save layout/version. Extra reserved bits 24–31 do not count.

- `Ichor_PlaceStar(index)` returns TRUE only for a first valid placement.
  Invalid indices and repeated placements return FALSE without changing
  other bits. `specialvar(VAR_RESULT, Ichor_PlaceConstellation)` exposes
  this with the index in `VAR_0x8004`.
- `Ichor_CountStars()` and
  `specialvar(VAR_RESULT, Ichor_CountConstellations)` count only the 24 myths.
- `FlagSet` calls `Ichor_StarFlagSet` for the Conch and Laurel 4/5/7/8
  receipts, placing Delphinus, Crater, Ursa Major, Cygnus and Corvus.
  The seventh distinct Daedalus page places the Pleiades.
- `Ichor_AddFavorTo` places Orion or Cancer when Artemis or Hera first
  reaches Favor 30. Other gods do not place those stars.
- `Ichor_RefreshStars` recovers these existing receipts and Favor thresholds
  on opening older saves. Placements are permanent; removing a debug
  receipt does not erase a star.

The other myth callers, additional outdoor seats, moon-dance encounter and
6/12/18/24 milestone rewards remain future integrations. Manually seeded
all-star fixtures demonstrate rendering, not current story obtainability.

`test/ichor_star_chart.c` covers bounded/idempotent placement, exact receipt
mapping, thresholds, distinct pages, legacy recovery and reserved bits.
`tools/ichor/tests/star_chart.sh` opens the real Bag item, checks all 24
distinct rendered pixel patterns, the empty final patch, palette twinkling,
navigation, screen cleanup and save/reset/CONTINUE. It compares all 288
compiled icon bytes and all sixteen colors against the live Bag sprite's
OBJ VRAM and palette, both before opening the Chart and after returning.
The same run interacts with the actual hill seat: daytime and missing-item
refusals, declining, dawn during its prompt, empty and two-myth skies, distinct
live colors, twinkle, navigation, repeated cleanup, retained music/position,
save/CONTINUE and the portable parchment afterward. Native guard checks also
exercise indoor, daytime and missing-Chart callers.

## 11. Oath of the Styx

The autonomous continuation uses **one wild-encounter chance per named area**,
not one per map or dungeon floor. This is an implementation decision, not a
claim of human approval. New games can now select the core Oath at the
bedroom clock after choosing difficulty. NO is the default, swearing requires
a second confirmation, and either completed answer is saved once. The
explanation covers area chances, permanent falls, empty-jar capacity,
stored-survivor recovery and the unchanged last-manual-save ending policy.
Later Charon/Riverside scenes are separate, unfinished Underworld work.

`src/ichor_oath.c` provides the saved-state core:

- `Ichor_ChooseOath(TRUE/FALSE)` accepts a single choice before the starter
  receipt, independently of difficulty. It refuses repeats, invalid booleans
  and choices after the starter. Swearing requires an empty final
  Pithos jar, names it URN and reserves it without moving existing Pokemon.
- The playable `Ichor_ChooseStartingOath` special additionally requires
  `FLAG_ICHOR_OATH_CHOICE_PENDING`, set only by `NewGameInitData`, not by
  IchorSave initialization or old-save migration. Either successful answer
  clears it. The bedroom script also skips players with the starter receipt,
  so existing saves and late arrivals cannot be retroactively enrolled.
  `gSpecialVar_0x8004` supplies TRUE/FALSE; a failed write leaves eligibility
  intact and reports the error in the original choice loop.
- `Ichor_IsOathActive()` recognizes only ACTIVE. The other saved states are
  UNDECIDED, DECLINED, RELEASED and FAILED.
- `Ichor_ClaimOathEncounter(mapSection)` admits the first encounter and saves
  its bit. Under an active Oath it refuses another chance in that named area,
  out-of-range IDs, dynamic sections and secret bases. Without an active Oath
  it admits ordinary encounters without recording a bit.
- `Ichor_BeginOathBattle` runs once from `CB2_InitBattle`, after save pointers
  have been relocated. Real wild encounters claim the named area's chance
  immediately: escape or defeat still spends it, while failed ball throws in
  that first battle can be retried. Trainer, link, recorded, Frontier,
  Trainer Hill, secret-base, tutorial and uncatchable ghost battles do not
  spend a chance. Dungeon floors sharing a named map section share a chance.
- `Ichor_CanCatchOathBattle` supplies the Bag, last-ball shortcut, Safari throw,
  native throw command and victory-catch guards. Repeat-area Bag attempts
  explain the refusal without spending an item or turn. Native quick/Safari
  action guards also preserve their ball counts. Inactive/released runs keep
  their normal capture behavior. This is not a gift/trade restriction.
- `Ichor_HasOathEncounter` and `Ichor_CountOathEncounters` read valid receipts.
- `Ichor_ReleaseOath` and `Ichor_FailOath` each transition an active Oath once,
  retaining its receipts and fallen count. Neither permits re-enrollment.
- `Ichor_RecordOathFallen(mon)` marks an actual zero-HP, non-Egg Pokemon
  once under an active Oath and increments its fallen count. The marker uses
  a previously unused BoxPokemon bit, leaving the Pokemon/storage sizes
  unchanged; `Ichor_IsOathFallen` ignores it outside sworn runs. Native
  `SetValuesOnFaint` records only the player's own Pokemon in real battles,
  not opponents, NPC partners or simulated/tutorial battles.
  Field poison also records actual zero-HP falls outside battle facilities;
  modern poison survival at one HP does not count as a fall.
- Fallen HP remains zero through `SetMonData`'s HP/HP-lost setters, stat
  recalculation, party healing and boxed-to-party conversion, including
  after release. `HealPokemon` and `HealBoxPokemon` leave the whole fallen
  record unchanged, including PP and status; modern party healing otherwise
  heals every stored jar too. Item effects refuse fallen targets; battle
  revival items explain why, and Revival Blessing's native search excludes them. Ordinary
  saves, including legacy Pokemon with the formerly unused bit set, retain
  ordinary healing and revival.
- `Ichor_IsUrnBox(box)` identifies saved reserved jars even after release or
  failure. Ordinary capture storage, full-storage checks and script free-space
  checks skip those jars. Direct party deposits refuse reserved destinations
  before changing their source.
- Reserved jars offer only SUMMARY/CANCEL for their occupants and JUMP/CANCEL
  for the jar itself. Normal/shortcut/group movement, A/B quick placement and
  Move items cannot remove or add partners or belongings. Refusals explain
  that the Urn is sealed; group refusal temporarily switches out of the
  eight-bit icon layer so the message remains legible, then restores the
  held group without changing its data.
- Fallen partners, including any retained in the party for capacity handling,
  cannot use ordinary PC deposit or service-selection APIs. Their summaries
  remain viewable but cannot rename, relearn or reorder moves. They do not
  count as living stored partners or usable stored field-move holders.
  The party menu offers only SUMMARY/CANCEL; direct-choice services explicitly
  refuse them without closing the chooser or changing the partner.
- `Ichor_StoreOathFallen(mon)` stores the entire marked BoxPokemon before
  clearing its source. A full Urn grows only into an entirely empty Pithos
  jar, named URN 2 and onward. Living Pokemon are never displaced. If no
  reserved space or empty jar exists, the explicit `ICHOR_URN_FULL` result
  leaves both the source and storage intact. Call this after battle, then
  compact/recount the party; the caller must report capacity refusal and
  prevent use or revival of a retained fallen partner.
- `Ichor_StoreOathPartyFallen()` transfers all marked party partners before
  compacting and recounting the party. Its aggregate result is NOT_FALLEN
  when no fallen partners were present, STORED when all pending partners fit,
  or FULL when any remain. FULL can include partial success: retained sources stay intact,
  and retrying after an ordinary jar becomes empty cannot duplicate records.
- `Ichor_EndOathBattle(type, outcome)` applies that transfer to real,
  non-defeat battles only when a living, non-Egg player partner remains.
  Wild, scripted wild, ghost, trainer and rematch return paths call it after
  any existing follower/variant party restoration. A TRUE result forces
  whiteout recovery before ordinary callback branches, including scripted
  no-whiteout battles and NPC victories with no usable player survivor.
  Lost/drawn battles with a usable restored party keep their native outcome
  handling; an Egg does not count as a survivor.
- `Ichor_ShowOathAftermathNotice()` runs after the field fades back in,
  before the normal return tasks unlock movement or resume the paused
  script. Transfer and full-capacity notices require acknowledgment without
  replacing the original event script. A full Urn retains the pending fallen
  partner and explains the need for an empty jar.
- `Ichor_RetryOathUrn()` repeats survivor-safe burial when opening the Pithos
  menu or returning from storage. Freeing an ordinary jar therefore resolves
  retained fallen partners without another battle, including after release.
  The same acknowledged notice is shown before the menu accepts input, and
  its ordinary description is restored afterward. No usable party survivor
  still means no transfer; total-party-loss recovery remains separate.
- `Ichor_PrepareOathRecovery()` runs before ordinary whiteout healing.
  An active Oath without a usable party partner searches non-Urn storage for
  a non-Egg, non-fallen partner. It buries fallen party members, restores one
  stored partner to the party, clears that source only after conversion,
  and retries burial if withdrawing it emptied a jar. Whole memorial records
  remain unchanged; partial capacity retains all overflow partners.
  The usual whiteout destination/healing remains in use, and an acknowledged
  recovery notice precedes the destination's normal healing script.
  RECOVERY_NONE leaves ordinary/released runs to native handling; RECOVERED
  means the party is usable again. EXHAUSTED marks only the in-memory Oath
  FAILED when no living stored partner exists. RECOVERY_BLOCKED instead
  leaves the Oath active and all party/storage records unchanged when no
  party slot can be freed without displacing a partner.
- `Ichor_ShowOathEndScreen(capacityBlocked)` explains exhaustion or blocked
  capacity and returns to the native title on A/B. It never writes a save.
  CONTINUE also routes saved FAILED states to this terminal screen before
  loading a map. Normal defeat therefore preserves the last manual save.
- The field-poison task finishes every original party index/message before
  survivor-safe burial and compaction. It waits for the Urn notice to be
  acknowledged before enabling the original script. Total-party field loss
  retains the native whiteout script and therefore uses the same stored-partner
  recovery and terminal safeguards. Facility losses keep their own routing;
  modern poison survival at one HP does not mark a permanent fall.

Version 5 takes 40 bytes from the old reserved region at 0x450. Total
IchorSave/SaveBlock3 sizes and every existing field offset stay unchanged,
including the second flag bank at 0x500. Older saves get zero Oath bytes,
not whatever previously occupied that reserve. Version 6 takes its two-byte
Urn mask from padding within those same 40 bytes; version-5 migration
preserves existing Oath progress and reserves only the original final jar.
Opening selection does not change the IchorSave version, save layout or
chosen difficulty. Existing saves have no new-game eligibility flag and
therefore remain unprompted and unenrolled.

The continuation's conservative run-ending policy is to return to the title
without overwriting the last manual save, not to auto-save a failed run or
permanently retire the save. This was selected autonomously while the user
was unavailable, not explicitly approved by the user. Defeat/load enforcement
is now implemented, including explicit capacity refusal without falsely
declaring stored living partners exhausted.

Native tests cover the entire map-section range, byte boundaries, invalid
indices, once-only choice/transitions and migration. The actual-ROM save
fixture seeds Oath state, saves and CONTINUEs, then writes version-4 and
version-5 saves with stale reserve bytes and verifies migration preserves
the old progress. Urn tests verify whole-Pokemon preservation, no duplicate
fall counting, safe growth, occupied-jar refusal and full-capacity retention.
`tools/ichor/tests/oath_capture.sh` enrolls only a fixture save and plays real
first-area capture, repeat-area Bag refusal, an escaped second area's chance,
save/reset/CONTINUE and capture after release. Native checks cover excluded
battle categories and quick/Safari no-consumption guards.
The same real-ROM fixture now plays an actual weak-lead fall, selects a living
replacement and checks native party healing before and after save/reload.
Native tests cover HP/item/boxed-heal bypasses, Revival Blessing's target
search and actual recorded-link fainting without permanent loss.
Native storage checks also fill every ordinary jar while leaving two reserved
jars empty, prove that capture and script capacity checks report full, and
verify that unsworn saves keep their final jar available. The actual-ROM
fixture uses the actual battle's automatically transferred fallen BoxPokemon and plays
view-only menus, summaries, shortcut/group refusal, A/B placement refusal,
safe return of held ordinary partners, Move items and the party-deposit
chooser. The complete fixture passes 68 checks with 25 screenshots, including
byte-for-byte Urn preservation through a second save/reset/CONTINUE after
release. It also fills the Urn, occupies every ordinary jar, plays another real
fall and verifies the explicit capacity notice, retained source, continued
non-revival and preservation through save/reset/CONTINUE. A direct-choice
party service refuses the retained partner; moving a living stored partner
to empty a jar triggers automatic burial on storage exit, with the original
Urn unchanged and the expansion preserved by save/reset/CONTINUE. Native tests cover
multiple fallen partners, survivor/Egg compaction, partial-capacity retry,
simulation and defeat exclusions, and the no-survivor routing guard.
`tools/ichor/tests/oath_recovery.sh` adds 18 real-ROM checks and eight
screenshots: an actual scripted no-whiteout defeat, boxed-survivor recovery,
memorial preservation, exhausted-run title return, transactional capacity
refusal, last-manual-save preservation and saved-FAILED load interception.
It also runs the native poison-message task with two one-HP survivors and an
already marked pending partner, checks that indices stay intact until every
message finishes, and proves acknowledged burial resumes the original
script with exact memorial records. The native all-party field-loss script
also reaches stored-survivor recovery. This is not a claim that the current
modern configuration inflicts lethal overworld poison damage.
Native tests also cover six-partner recovery, Eggs/memorials not counting
as survivors, partial-capacity retention, newly emptied source-jar reuse,
and ordinary/released whiteout preservation.
`tools/ichor/tests/oath_choice.sh` adds 21 real-ROM checks and six screenshots:
default decline, rejected binding confirmation, accepted enrollment on all
three difficulties, old-save and post-starter refusal, once-only persistence
of either answer, and the complete native water-clock-to-Oath handoff through
save/reset/CONTINUE. These demonstrate the core rules, not human balance
approval or completed later-chapter memorial scenes.
