# Ichor engine API

What the engine gives map and script agents: the state you can read and write, and the specials and scripts you call. Each section names the system's spec in `design/SYSTEMS.md` and the code behind it.

- **Owner:** the engine-systems session. Map agents call these APIs and never change the code behind them. If an API is missing, ask for it.
- **Tests:** every system has a headless check in `tools/ichor/tests/ichor_*.sh`. Run them after any engine change.

## 1. Ichor's save state

All of Ichor's own persistent state lives in **`struct IchorSave`** (`include/ichor_save.h`, `src/ichor_save.c`). It is the first member of SaveBlock3.

| | |
|---|---|
| Size | 1,472 bytes. It was 1,280 until version 4 added the second flag bank at 0x500. SaveBlock3 is now 1,476 of its 1,624 bytes. |
| Version | `ICHOR_SAVE_VERSION` (4). Version 0 means a save from before IchorSave. |
| New game | `Ichor_InitSave()` (from `NewGameInitData`): everything zero, except `version` and `momLosses = 212`. |
| Loading a save | `Ichor_OnSaveLoaded()` (from `LoadGameSave`). A version-0 save gets the new-game defaults, so slice saves from before IchorSave still load. Each later version's step: 2 added `frozenHourStep` (§5); 3 added the forced omen and the held tint (§7), all from `headerReserved`; 4 added `flags2`, zeroed on load because an older save holds what used to sit past IchorSave's end there. |
| New day | `Ichor_DoDailyEvents()` (from `DoDailyEvents`) clears the daily flag bank and draws the day's omen (§7). |
| Headroom | 176 bytes in `reserved` at 0x450 (world-postgame takes 64 of them for `IchorEpics`), 20 in `headerReserved`, and 148 more in SaveBlock3. |

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
| 8 | Excavation: the Trowel, dig spots, fixed finds | 6 | **Built** |

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

### Carried flames (SYSTEMS §2)

- **A carried flame** is a named fire on Hecate's Torch for a set number of steps. Its kinds are `FLAME_HEARTH`, `FLAME_SANCTUM`, `FLAME_THRESHOLD`, and the post-game's `FLAME_HESTIA_SHIP` (Hestia's fire) and `FLAME_LERNA` (Kleon's fire). Add new kinds at the end, with their names in `src/ichor_relics.c`.
- **The engine keeps it,** not the map's temp vars. Maps use `VAR_TEMP_*` for their own ends. Read it with `specialvar(VAR_RESULT, Ichor_GetFlameKind)` (`FLAME_NONE` without one) and `specialvar(VAR_RESULT, Ichor_GetFlameSteps)`. The first draft kept it in `VAR_TEMP_2` and `VAR_TEMP_3`; scripts that check those must switch to the specials.
- **It dies when you leave the map,** unless its kind **travels**. A travelling kind keeps its steps through doors, warps and map edges: so far only `FLAME_HESTIA_SHIP`, Lampon's walk from Akti's temple to the quay. Mark a new kind in `sFlameTravels` (`src/ichor_relics.c`). A save and CONTINUE puts any flame out.
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
  - The Hunter's Moon, Athena's Stylus and the Eyes of Argus are **flags only, hooks** for the Augur's Eye and the Scroll of Deeds.
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

**The offerings** are `ITEM_OLIVE_OIL` (200), `ITEM_BARLEY_CAKE` (150), `ITEM_WINE` (300), `ITEM_FRANKINCENSE` (500), `ITEM_LAUREL_SPRIG` (100) and `ITEM_BRONZE_VOTIVE` (400). Honey now costs 300.
- **Their icons are stand-ins** borrowed from existing items (the oil flask, a cookie, juice, the incense cone, a seedling, the Metal Coat), as is the Myrtle Wreath's. Drawing the real ones is for the art team.

**Checks:** `tools/ichor/tests/ichor_rites.sh` (in game) and `test/ichor_rites.c` (the rules, in `make check`).

## 4. Herm waystones (SYSTEMS §4)

Built in `src/ichor_herms.c`, `src/data/ichor_herms.h` and `data/scripts/ichor_herms.pory`. Tested by `tools/ichor/tests/ichor_herms.sh`.

- **One great herm per route.** Its bg event runs `EventScript_IchorGreatHerm` directly. A herm that is already a sign with its own line calls `EventScript_IchorAnointHerm` after it, between `lockall` and `releaseall`. The engine knows which herm it is from the map; on a map with no herm row, both scripts do nothing.
- **Herm ids** (`include/constants/ichor.h`) follow AETHOS_MAP's land routes and their map sections: `HERM_KALLISTE_ROUTE_1`, `HERM_AETHOS_ROUTE_4` … `_18`, `HERM_BULL_ROAD`, `HERM_AETHOS_ROUTE_25` … `_30` and `HERM_THE_ASCENT`. That is 23 before the post-game (`HERM_COUNT`). The post-game's `HERM_AETHOS_ROUTE_31` and `_32` come after them and don't count toward the bonus. Sea routes have no herm. Room is left for 32.
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

Built in `src/ichor_save.c`, `src/ichor_time.c` and `src/ichor_omen.c`. Tested by `make check TESTS="Ichor:"`.

### Counting flags

`setvar(VAR_0x8004, FLAG_ICHOR_PROPHECY_START)`, `setvar(VAR_0x8005, 8)`, `specialvar(VAR_RESULT, Ichor_CountFlagRange)`: how many of those flags are set. It works on any flag range: a bank, a vanilla range or the daily flags.

### Holding the day-and-night tint

- **`setvar(VAR_0x8004, TIME_EVENING)`, then `special(Ichor_HoldTimeOfDay)`.** The tint holds at that time of day, whatever the clock says. The hold lasts through warps and saves until `special(Ichor_ReleaseTimeOfDay)`. It takes `TIME_MORNING`, `TIME_DAY`, `TIME_EVENING` or `TIME_NIGHT`, each at full strength.
- **It's the game's time of day while held,** not just the colors. Encounter tables and time-based evolutions follow it, so night falls at Delphoi for the Pokémon too.
- The tint only shows on maps with natural light (towns, routes and the sea), so interiors look the same either way.
- The expansion's own `SetTimeOfDay` hour override still works, but it resets on every warp. Use the hold for anything that spans maps.

### Omens (SYSTEMS §6)

- **Today's omen** is `IchorSave.omenKind` (`OMEN_SWARM`, `_VISITOR`, `_WEATHER`, `_GOOD_SIGN`, `_STRANGER`, or `OMEN_NONE`) and `omenEntry`, an entry within that kind. The entries are numbered in `include/constants/ichor.h`: `OMEN_WEATHER_KRYOPUFF` and `OMEN_WEATHER_LERNIP` so far. Add new ones at the end.
- **Forcing tomorrow's omen,** as when Akanthis first tells the Lernip rumor: `setvar(VAR_0x8004, OMEN_WEATHER)`, `setvar(VAR_0x8005, OMEN_WEATHER_LERNIP)`, `special(Ichor_ForceOmen)`.
- **A map that owns an omen's weather** checks it in `ON_TRANSITION`:
  ```
  setvar(VAR_0x8004, OMEN_WEATHER)
  setvar(VAR_0x8005, OMEN_WEATHER_LERNIP)
  specialvar(VAR_RESULT, Ichor_CheckOmen)
  if (var(VAR_RESULT) == TRUE) { setweather(WEATHER_RAIN) }
  ```
- `specialvar(VAR_RESULT, Ichor_GetOmen)` gives the kind, with the entry in `VAR_0x8004`. The augurs use it.
- **Not built yet:** SYSTEMS §6's daily draw from the entry table (swarms through `StartMassOutbreak`, visitors' hide flags, the story filter). Until it lands, a day without a forced omen has none.

### Four time-of-day encounter tables on one map

These need no engine change. `OW_TIME_OF_DAY_ENCOUNTERS` is on, and `tools/wild_encounters/wild_encounters_to_header.py` builds one table per time of day.
- **In `src/data/wild_encounters.json`,** give the map up to four entries with the same `map` and `base_label`s ending `_Morning`, `_Day`, `_Evening` and `_Night`. Route 1 already has `gKallisteRoute1_Morning` and `_Night`.
- **The hours** (`OW_TIMES_OF_DAY`, latest generation): morning 6–10, day 10–19, evening 19–20, night 20–6.
- **A time with no table of its own falls back to `_Morning`** (`OW_TIME_OF_DAY_FALLBACK`). With all four defined, Lakonia's Chalkip can sit in `_Morning` and `_Evening` only.

## 8. Excavation (SYSTEMS §5)

Alethea gives the Trowel with `giveitem(ITEM_ALETHEAS_TROWEL)` (a key item). Every dig spot is a bg event, or an object, whose script sets two vars and goes to one of two scripts:

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
- A spot with no amphora never gives a sherd: the roll goes again. So does a sherd roll once its amphora is whole, and an ostrakon roll once all 30 are found.

**What a dig does:**
- **Without the Trowel,** it says the earth has been turned and something glints in it.
- **With it,** the player raises the Trowel (the relic pose), dust puffs on the tile and the find comes up.
  - Items go in the Bag. If it's full, nothing is dug, and the spot stays.
  - A sherd sets the amphora's next flag (`FLAG_ICHOR_SHERDS_START + 4 × amphora + n`) and says "*n* of its 4 pieces".
  - An ostrakon sets the next of `FLAG_ICHOR_OSTRAKA_START + 0–29`, in order, and shows its words. The 30 are in `src/ichor_dig.c` (`sOstraka`). Nine name Aristeides, for Lysimachos, and the last is the player's. Writers may rewrite any of them.
  - Tablet *n* sets `FLAG_ICHOR_PROPHECY_START + n − 1`, and page *n* sets `FLAG_ICHOR_PAGES_START + n − 1`. Alethea's reading, or the page's text, is the map's own script (see below).
- **Afterwards,** a daily spot says "dug today" until tomorrow, and a fixed find says "nothing else is buried here".
- **A fixed find with nothing left to give** (a sherd of a whole amphora) gives Stardust instead.
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

**The coins** are renamed, and sell for half their price at any market (Hades's blessing +50%):

| Item | Name | Sells for |
|---|---|---|
| `ITEM_RELIC_COPPER` | Bronze Obol | ¥500 |
| `ITEM_RELIC_SILVER` | Silver Owl | ¥2,000 |
| `ITEM_RELIC_GOLD` | Gold Stater | ¥5,000 |

Pasion's "+20%" in Emporion is then ¥600, ¥2,400 and ¥6,000, which his script can write as numbers.

**Index blocks** for dig spots are in §1's table. Ask the engine session for more.

**Checks:** `tools/ichor/tests/ichor_dig.sh` (15 checks on Route 1) and `make check TESTS="Ichor:"` (`test/ichor_dig.c`: the rolls, rerolls, act tables and blessings).

