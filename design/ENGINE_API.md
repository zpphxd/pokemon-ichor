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

---

## Status of the rest of this file

§1 is built. **§2–§5 are the planned API, published early so the world sessions can write their scripts against it now.** The names in them are fixed: build against them, and stub what isn't there yet. The behavior lands batch by batch:

| § | System | Batch | State |
|---|---|---|---|
| 1 | Save state and banks | 1 | **Built** |
| 2 | Relics, darkness and braziers | 2 | Planned, names fixed |
| 3 | Rites: altars, Favor, blessings, gifts | 3 | Planned, names fixed |
| 4 | Herm waystones and the Wings | 4 | Planned, names fixed |
| 5 | Labyrinth mechanics, then the Frozen Hour | 5 | Hooks only |

Until a batch lands, a script that calls one of its names won't link. Keep such calls behind a placeholder of your own until then, or ask for the batch's constants early.

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
| `ITEM_ARIADNES_THREAD` | Ariadne's Thread | Outside the Labyrinth, an escape to the dungeon's entrance | Relic Ring |
| `ITEM_LABRYS` | Labrys | Cleaves labrys seals and bronze chains | A |
| `ITEM_HELM_OF_DARKNESS` | Helm of Darkness | On or off; hook for unseen-in-the-dark (§5) | Relic Ring |
| `ITEM_NEREID_PEARL` | Nereid Pearl | Dive | A on deep water |
| `ITEM_AEOLUS_BAG` | Aeolus's Bag | Defog | From the bag |

**Giving a relic.** Use `giveitem(ITEM_BRONZE_HAMMER)`. The engine sets the relic's flag whenever the item enters the bag, so scripts can check either.

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

- Like vanilla, an obstacle comes back when the map reloads. To clear it for good, give the object a hide flag of your own; the script's `removeobject` sets it.
- **Water needs no events:** Surf, Waterfall and Dive come from the map's metatile behaviors, exactly as in Emerald, and check the Conch, the Horn and the Pearl.
- **The wording without the relic** follows SYSTEMS §1: "A thorn thicket. A good blade would clear it." and "The blocks won't shift by hand. A good hammer would break them."

### Darkness and braziers (SYSTEMS §2)

- **A dark map** is one whose header has `"cave": true` (Porymap: "Requires Flash"). Without the Torch the light radius is 1.5 tiles. With it, 3.5. The Three-Flamed Torch or Hecate's blessing gives 4, and both give 4.5.
- **Braziers** are metatiles, so the map draws them. Each gets a flag in `FLAG_ICHOR_BRAZIERS_START`'s range; ask for a block of indices for your maps.
  ```
  // the brazier's bg event
  script Map_Brazier1 {
      setvar(VAR_0x8004, FLAG_ICHOR_BRAZIERS_START + 0)
      call(EventScript_IchorBrazier)        // asks, lights it, sets the flag
      if (var(VAR_RESULT) == TRUE) {        // TRUE only when it was lit just now
          setmetatile(...)                  // swap to your lit metatiles
          special(DrawWholeMapView)
      }
      releaseall
  }
  ```
  In the map's ON_LOAD, swap the metatiles of every brazier whose flag is set.
- **Lit zones.** A coord event on each threshold of a brazier's zone:
  - going in: `setvar(VAR_0x8004, <brazier flag>)` and then `call(EventScript_IchorEnterLitZone)`, which brightens the map if that brazier is lit;
  - going out: `call(EventScript_IchorLeaveLitZone)`, which goes back to the torch's radius.

### The player's side

- **The Relic Ring:** SELECT opens a menu of the registered item plus every owned free relic (the Wings, the Torch, the Helm, the Thread, and Hestia's Hearthfire while you hold her blessing). It opens on the last entry used.
- **The option "Relic prompts":** ASK (the default) or AUTO. Surf and Waterfall always ask.
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

**God ids** (`include/constants/ichor.h`): `ICHOR_GOD_HESTIA` (1), `_HERMES`, `_DEMETER`, `_DIONYSUS`, `_ARTEMIS`, `_HEPHAESTUS`, `_APHRODITE`, `_APOLLO`, `_ARES`, `_POSEIDON`, `_ATHENA`, `_HERA`, `_ZEUS`, `_HECATE`, `_HADES` (15). 0 is none.

### Altars

Use these directly as an altar's bg event or object script. Each runs the whole rite: PRAY, MAKE AN OFFERING, FAVOR or LEAVE, then any gift that is due.

| Script | Where |
|---|---|
| `EventScript_IchorAltar_<God>` | A roadside or town altar, e.g. `EventScript_IchorAltar_Apollo` |
| `EventScript_IchorTempleAltar_<God>` | The god's great altar in their temple: offerings count double |
| `EventScript_IchorHearth` | A household hearth (Hestia) |
| `EventScript_IchorAresTrophy` | Ares's trophy: "Offer a battle", once a day |
| `EventScript_IchorDesecratedAltar` | Set `VAR_0x8004` to the god and `VAR_0x8005` to the altar's index (0–31), then `goto` it. Beat the Titanborn guard in your own script first. Its flag is `FLAG_ICHOR_ALTARS_START + index`. |

### Calls for story scripts

| Call | In | Out |
|---|---|---|
| `special(Ichor_AddFavor)` | `VAR_0x8004` god, `VAR_0x8005` amount | Favor never drops and caps at 100. |
| `specialvar(VAR_RESULT, Ichor_GetFavor)` | `VAR_0x8004` god | 0–100 |
| `specialvar(VAR_RESULT, Ichor_GetBlessingGod)` | | The god whose blessing is on you, or 0 |
| `special(Ichor_GrantBlessing)` | `VAR_0x8004` god, `VAR_0x8005` steps | For the augur's free minor blessing and the like |
| `EventScript_IchorHierophantGift` | `VAR_0x8004` god | The Hierophant hands over gift I if it is due. `VAR_RESULT` is TRUE if they did. |
| `EventScript_IchorHierophantRite` | `VAR_0x8004` god | On your first visit, the Hierophant teaches the rite and gives one loved offering |

**Favor amounts,** as constants: `ICHOR_FAVOR_LAUREL` (15), `ICHOR_FAVOR_MYTH_QUEST` (10), `ICHOR_FAVOR_FESTIVAL` (5) and `ICHOR_FAVOR_CLEANSE` (3).

**Gift flags:** `FLAG_ICHOR_GIFTS_START + 4 * god + n`, where n is 0 for gift I, 1 for gift II, 2 for gift III and 3 for the Hierophant's offering.

**The offerings** are Agora items: `ITEM_OLIVE_OIL`, `ITEM_BARLEY_CAKE`, `ITEM_WINE`, `ITEM_FRANKINCENSE`, `ITEM_LAUREL_SPRIG` and `ITEM_BRONZE_VOTIVE` (new); Honey, any berry (first fruits), the seven feathers and the sea gifts (existing). Prices are in SYSTEMS §3.

## 4. Herm waystones (SYSTEMS §4)

- **One great herm per route.** Its bg event script is `EventScript_IchorGreatHerm`, used directly. The engine knows which herm it is from the map.
- **Herm ids** (`include/constants/ichor.h`): `HERM_KALLISTE_ROUTE_1` and `HERM_ROUTE_2` to `HERM_ROUTE_15`. Room is left for 32. Each herm's flag is `FLAG_ICHOR_HERMS_START + id`.
- **Each herm needs one engine table row and one heal location.** Tell the engine session the herm's map and its landing tile (the tile south of it, on the main path), or add both rows yourself:
  - `src/data/ichor_herms.h`: `[HERM_ROUTE_2] = { MAP_..., HEAL_LOCATION_HERM_ROUTE_2 },`
  - `src/data/heal_locations.json`: `HEAL_LOCATION_HERM_ROUTE_2`, with the landing tile's map, x and y.
- **Anointing** costs 1 Olive Oil and gives Hermes +1 Favor, once per herm. Anointing every herm gives Hermes +10 more.
- **With the Wings,** every anointed herm's route is a fly target on the region map, landing on the tile south of the herm.
- **Count:** `specialvar(VAR_RESULT, Ichor_CountHerms)`, for the Scroll of Deeds ("Herms anointed: 7 of 22").

## 5. Later: the Labyrinth and the Frozen Hour

These come after herms, unless the director reorders them. IchorSave already holds Ariadne's Thread (§1). Each needs its maps first, so world-act3 and the engine session agree the details before it is built:
- **Ariadne's Thread on the floor:** the per-step callback, the drawing and winding, tying off, and RETURN TO… (LABYRINTH.md §5.1).
- **Asterion:** patrol, sight and charge AI (§5.3).
- **The Helm of Darkness:** stealth in the dark, through `OW_FLAG_NO_TRAINER_SEE` and Asterion's sight.
- **Daedalus's wall dials,** turned with the Labrys.
- **The Frozen Hour:** the gray palette drain and frozen NPCs (STORY.md).
