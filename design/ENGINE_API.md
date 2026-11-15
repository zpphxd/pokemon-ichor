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

**One assembler caveat.** The `compare` macro (and the `goto_if_eq`-style macros built on it) treats a second argument in `0x4000`–`0x40FF` as a var and anything else as a number. So comparing a var *against a bank var* needs `compare_var_to_var` explicitly. Comparing a bank var against a number works as usual.

**Tests read the banks from IchorSave,** not from SaveBlock1. `tools/ichor/tests/engine_lib.lua`'s `L.getFlag`, `L.setFlag`, `L.getVar` and `L.setVar` handle every range.

**Check:** `tools/ichor/tests/ichor_save.sh`.

---

## Status of the rest of this file

§1–§3 are built. **§4–§5 are the planned API, published early so the world sessions can write their scripts against it now.** The names in them are fixed: build against them, and stub what isn't there yet. The behavior lands batch by batch:

| § | System | Batch | State |
|---|---|---|---|
| 1 | Save state and banks | 1 | **Built** |
| 2 | Relics, darkness and braziers | 2 | **Built** |
| 3 | Rites: altars, Favor, blessings, gifts | 3 | **Built** |
| 4 | Herm waystones and the Wings | 4 | **Built** |
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

## 5. Later: the Labyrinth and the Frozen Hour

These come after herms, unless the director reorders them. IchorSave already holds Ariadne's Thread (§1). Each needs its maps first, so world-act3 and the engine session agree the details before it is built:
- **Ariadne's Thread on the floor:** the per-step callback, the drawing and winding, tying off, and RETURN TO… (LABYRINTH.md §5.1).
- **Asterion:** patrol, sight and charge AI (§5.3).
- **The Helm of Darkness:** stealth in the dark, through `OW_FLAG_NO_TRAINER_SEE` and Asterion's sight.
- **Daedalus's wall dials,** turned with the Labrys.
- **The Frozen Hour:** the gray palette drain and frozen NPCs (STORY.md).
