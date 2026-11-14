# Ichor engine API

What the engine gives map and script agents: the state you can read and write, and the specials and scripts you call. Each section names the system's spec in `design/SYSTEMS.md` and the code behind it.

- **Owner:** the engine-systems session. Map agents call these APIs and never change the code behind them. If an API is missing, ask for it.
- **Tests:** every system has a headless check in `tools/ichor/tests/ichor_*.sh`. Run them after any engine change.

## 1. Ichor's save state

All of Ichor's own persistent state lives in **`struct IchorSave`** (`include/ichor_save.h`, `src/ichor_save.c`). It is the first member of SaveBlock3.

| | |
|---|---|
| Size | 1,280 bytes, fixed. SaveBlock3 is now 1,284 of its 1,624 bytes. |
| Version | `ICHOR_SAVE_VERSION` (1). Version 0 means a save from before IchorSave. |
| New game | `Ichor_InitSave()` (from `NewGameInitData`): everything zero, except `version = 1` and `momLosses = 212`. |
| Loading a save | `Ichor_OnSaveLoaded()` (from `LoadGameSave`). A version-0 save gets the new-game defaults, so slice saves from before IchorSave still load. |
| New day | `Ichor_DoDailyEvents()` (from `DoDailyEvents`) clears the daily flag bank. |
| Headroom | 176 bytes in `reserved`, plus 24 in `headerReserved`. |

**Adding a field later.**
1. Take its bytes from the front of `reserved` and shrink `reserved` by the same amount. The struct must stay 1,280 bytes; `STATIC_ASSERT`s in `src/ichor_save.c` pin the size and the offsets.
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
| `dailyFlags[32]` | the daily bank | 256 flags, cleared each day. |
| `thread` | LABYRINTH.md §5.1 | Ariadne's Thread: 24 anchors (8 bytes each, not 6, because apcs-gnu rounds structs to 4 bytes), 1,792 committed steps, a 152-step live segment. |

### The flag and var banks

Only 26 vanilla vars and 322 vanilla flags were left, so IchorSave carries its own banks. Scripts use them with the ordinary commands, `setflag`, `checkflag`, `goto_if_set`, `setvar` and the rest, and with object-event hide flags. `GetFlagPointer` and `GetVarPointer` (`src/event_data.c`) route these ids into IchorSave.

| Bank | Ids | Count | Claim with |
|---|---|---|---|
| Flags | `0x2000`–`0x27FF` | 2,048 | `python3 tools/ichor/claim.py bankflag FLAG_ICHOR_<NAME> "comment"` |
| Daily flags | `0x2800`–`0x28FF` | 256, cleared each day | `python3 tools/ichor/claim.py dailyflag FLAG_DAILY_ICHOR_<NAME> "comment"` |
| Vars | `0x4100`–`0x411F` | 32 | `python3 tools/ichor/claim.py bankvar VAR_ICHOR_<NAME> "comment"` |

**Use the banks for all new Ichor content,** including story flags, item balls, hidden items and hide flags. Keep the remaining vanilla flags and vars for anything that has to sit in SaveBlock1. A claim adds a named line to `include/constants/flags.h` or `vars.h`, in the bank's "general" range.

**Parallel sessions** pass `--range LO-HI` first, as with vanilla flags (`tools/ichor/claim_ranges.md`). For a bank, LO and HI are offsets into its general range (`0x000`–`0x4FF` for flags, `0x00`–`0x6F` for daily flags, `0x00`–`0x1F` for vars). Each claim takes the lowest free offset in the range, and lines stay sorted by offset, so separate ranges merge cleanly.

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
| `FLAG_ICHOR_GENERAL_START` | `0x2300` | 1,280 | Claimed by name |
| `FLAG_DAILY_ICHOR_PRAYED_START` | `0x2800` | 16 | Prayed to god *g* today |
| `FLAG_DAILY_ICHOR_DIG_START` | `0x2810` | 96 | Daily dig spots |
| `FLAG_DAILY_ICHOR_LAUREL_START` | `0x2870` | 32 | Laurel trees, one sprig a day |
| `FLAG_DAILY_ICHOR_GENERAL_START` | `0x2890` | 112 | Claimed by name |

**Tests read the banks from IchorSave,** not from SaveBlock1. `tools/ichor/tests/engine_lib.lua`'s `L.getFlag`, `L.setFlag`, `L.getVar` and `L.setVar` handle every range.

**Check:** `tools/ichor/tests/ichor_save.sh`.
