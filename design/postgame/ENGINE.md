# Post-game engine API

What the post-game's engine gives map and script agents: the state you can read and write, and the specials and scripts you call. It sits beside `design/ENGINE_API.md` (the shared systems) and follows its conventions.

- **Owner:** the world-postgame session (`claude/world-postgame-9fad0c`). Map agents call these APIs and never change the code behind them. If an API is missing, ask for it.
- **Tests:** every system has a headless check, `tools/ichor/tests/pg_*.sh`, built on `tools/ichor/tests/pg_lib.lua` (§9). Run them after any engine change.
- **Upstream hooks** are marked `// Ichor postgame:`.

| § | System | Batch | State |
|---|---|---|---|
| 1 | `struct IchorEpics` | 1 | **Built** |
| 2 | The ship at sea; boarding, landing, below deck | 1 | **Built** (stand-in graphics and deck) |
| 3 | The helm and its voyages | 1 | **Built** (Akti open; five ports pending) |
| 4 | Wind | 1 | **Built** |
| 5 | The at-sea lock on the Wings | 1 | **Built** |
| 6 | The Great Bear | 1 | **Built** |
| 7 | Wild encounter overlays: shades on the roads | 1 | **Built** (Time Fractures: batch 8) |

---

## 1. IchorEpics (POSTGAME §6)

All of the post-game's per-epic state lives in **`gIchorSave.epics`**, a `struct IchorEpics` (`include/ichor_save.h`): 64 bytes at IchorSave offset `0x450`, carved from the front of `reserved` (which now starts at `0x490`, 112 bytes).

- **No version bump.** Every field's default is zero, and `reserved` was always zero-filled, so a save from before the epics existed loads with all of them at their defaults and needs no migration. Keep it that way: **a new field's zero must mean its default.** If one truly needs another default, it takes the next `ICHOR_SAVE_VERSION` and a step in `Ichor_OnSaveLoaded`.
- `STATIC_ASSERT`s in `src/ichor_save.c` pin its offset, its size and the ship's fields.
- Story state that isn't per-epic stays in flags and the three post-game vars (`VAR_ICHOR_POSTGAME`, `_ODYSSEY`, `_KATABASIS`).

| Offset | Field | Holds | Owner |
|---|---|---|---|
| `0x00` | `u16 laborsSet` | 12 bits: Labors given | LABORS §12 |
| `0x02` | `u16 laborsDone` | 12 bits | LABORS §12 |
| `0x04` | `u16 laborsDedicated` | 12 bits | LABORS §12 |
| `0x06` | `u8 laborStep[12]` | per-Labor state | LABORS §12 |
| `0x14` | `u32 lernaPools` | Labor 2's nine 2-bit pools, the moved-fire bit | LABORS §12 |
| `0x18` | `u8 titans` | 6 bits | UNDERWORLD §13 |
| `0x1A` | `u16 shades` | shades met, unburied paid for | UNDERWORLD §13 |
| `0x1C` | `u8 oathAtRest` | | UNDERWORLD §13 |
| `0x1E` | `u16 crew` | 10 bits (the crew flags are the source of truth today) | ODYSSEY §15 |
| `0x20` | `u8 oarsmenTaken` | Scylla's toll and the rescued bits | ODYSSEY §15 |
| `0x21` | `u8 wind` | **the wind (§4)** | sail-engine |
| `0x22` | `u16 storm` | Tornadus's position while loose | ODYSSEY §15 |
| `0x24` | `u16 voyage` | the voyage's choices | ODYSSEY §15 |
| `0x26` | `u8 shipPort` | **where she's moored (§2)**, a `VOYAGE_*`; was `shipUpgrades` | sail-engine |
| `0x28` | `u16 kleos` | the twelve laurels | POSTGAME §5 |
| `0x2A` | `u8 colossusLots` | 3 bits held, 3 bits used | POSTGAME §3.4 |
| `0x2B` | `u8 primordials` | Gaia, Oceanus, Ouranos, the Prime Mover | POSTGAME §3.3 |
| `0x2C` | `u8 atlantisBreath` | carried between dives on one visit | POSTGAME §3.2 |
| `0x2D` | `u8 version` | for the epics' own migrations | |
| `0x2E` | `u8 seaMapGroup`, `seaMapNum` | **the sea she lies on while you're below (§2)** | sail-engine |
| `0x30` | `u8 seaX`, `seaY`, `seaFacing` | her tile and heading (`DIR_*`) | sail-engine |
| `0x33` | `u8 pad[13]` | free | |

The ship's upgrades are flags (`FLAG_ICHOR_SHIP_RAM`, `_SHIP_SAIL`, `_SHIP_KEEL`), so `shipUpgrades`'s byte holds the port instead, and the five bytes of the sea position come from the pad. Implicit alignment holes sit at `0x12`, `0x19`, `0x1D` and `0x27`.

**Tests** read and write the fields with `pg_lib.lua`'s `L.epic8("WIND")`, `L.setEpic16("CREW", n)` and `L.epicsBytes()`.

---

## 2. The ship at sea (ODYSSEY §2, §4)

Built in `src/ichor_sailing.c` and `data/scripts/ichor_postgame_sailing.pory`; constants in `include/constants/ichor_sailing.h`.

### The state

| | |
|---|---|
| `FLAG_ICHOR_ON_SHIP` | **She's under way.** Set from the moment she puts out until you go ashore, including while you're below deck from the sea. |
| `gIchorSave.epics.shipPort` | The `VOYAGE_*` port she's moored at. 0 means nobody has sailed her yet, and she waits at Akti. |
| `specialvar(VAR_RESULT, Ichor_GetShipPort)` | The port she's moored at, or `VOYAGE_NONE` while she's under way |
| `specialvar(VAR_RESULT, Ichor_IsMooredAt)` | `VAR_0x8004` = a port: TRUE if she's moored there |
| `specialvar(VAR_RESULT, Ichor_IsSailing)` | TRUE while you're in the ship on the water |

Nolan's recruitment ("if the Euploia is moored in Lechaion"):
```
setvar(VAR_0x8004, VOYAGE_LECHAION)
specialvar(VAR_RESULT, Ichor_IsMooredAt)
if (var(VAR_RESULT) == TRUE) { ... }
```

### The avatar

While `FLAG_ICHOR_ON_SHIP` is set and the player is in the surf state, the avatar is the *Euploia*:

- **Graphics** `ICHOR_SHIP_GFX` (sail full) and `ICHOR_SHIP_GFX_SLACK` (sail slack), 64×64 in the standard 9-frame layout. The sail fills downwind and crosswind and hangs slack upwind and in a calm (§4); it changes at a tile's center as the heading changes, and when the wind does.
- **No surf blob** (it's still there, hidden, so every surfing path keeps working; it shows again under a fishing or relic pose, which takes the ship's graphics off for a moment). The follower stays stowed, as it does for any surfing.
- **She doesn't run up a beach.** Land is a wall to the ship: you go ashore only at a landing (`EventScript_IchorLand`). Dive and fishing work as from the surf state.
- **Battles and saves** come back in the ship: the avatar's state is read back from her graphics.
- **Any water tile** you arrive on with the flag set puts you in her: a warp, a map connection, a dive coming up.
- **Collision is one tile,** as for any object. The sprite overhangs it (48 px above and 24 px to each side for 64×64), so give a sea map's channels a tile of water to spare where it matters.

**Stand-ins (`ICHOR_STUB_PG_SPRITES`).** Until the sprites agent's `OBJ_EVENT_GFX_ICHOR_EUPLOIA` and `_EUPLOIA_SLACK` merge, the full sail is the S.S. Tidal (96×40, the largest ship in an Emerald build) and the slack sail Rayquaza's still frames (64×64). The FRLG Seagallop is 64×64 but isn't in an Emerald build, and the cable car, the other 64×64 object, has one frame and crashes a walking avatar. The build lead points the two defines at the real graphics at merge.

### Boarding, landing, leaving

| Script | Put it on | Does |
|---|---|---|
| `EventScript_IchorBoardShip` | A port's gangplank (coord or bg event on the quay), `VAR_0x8004` = the port | "Board the Euploia?" YES: onto the port's sea map in the ship, at its row's entry (§3), if it has one; otherwise onto the deck, moored there. If she isn't moored at this port: "The Euploia isn't moored here." |
| `EventScript_IchorLand` | A bg event on a sea map's landing tile, `VAR_0x8004` = the port | In the ship only: "Go ashore at Akti?", then the port's quay, ship mode off, moored there |
| `EventScript_IchorLeaveShip` | The deck's gangplank | "Go ashore at Akti?" to the quay where she's moored; at sea, "She's at sea. The gangplank stays lashed down." |

```
// a quay's gangplank (bg event)
script Lechaion_EventScript_Gangplank {
    setvar(VAR_0x8004, VOYAGE_LECHAION)
    goto(EventScript_IchorBoardShip)
}

// a sea map's landing (bg event on the tile you face from the water)
script Route33_EventScript_LandTainaron {
    setvar(VAR_0x8004, VOYAGE_CAPE_TAINARON)
    goto(EventScript_IchorLand)
}
```

Show her and her gangplank only while she's moored there: in the quay map's `ON_TRANSITION`, set a `FLAG_TEMP_*` hide flag from `Ichor_IsMooredAt`.

**For a story beat** (a storm throws you onto another sea, the Phaeacians' night crossing): `special(Ichor_PutShipAtSea)` with `VAR_0x8004` = the map (`MAP_*`), `VAR_0x8005`/`6` = x, y and `VAR_0x8007` = the heading (`DIR_*`). It waits for the warp.

### Below deck and back

- **DECK.** At sea in the ship, the Relic Ring gets a DECK entry (it opens even with no relic). It runs `EventScript_IchorGoBelowDeck`: `special(Ichor_GoBelowDeck)` saves the sea map, x, y and heading (`epics.sea*`) and warps to the deck. She stays under way.
- **The deck map** is reached only through `ICHOR_SHIP_DECK_MAP`, `ICHOR_SHIP_DECK_X` and `_Y`, where every boarding and every DECK arrives, facing the bow (north). **`ICHOR_STUB_EUPLOIA_DECK`:** they point at `MAP_PG_TEST_DECK`, the sail-engine's test room on the Diver's house layout, until the euploia agent's `MAP_EUPLOIA_DECK` merges; then the build lead points them at it (and its arrival tile) and deletes `data/maps/PgTestDeck/`.
- **TAKE HER OUT** at the helm (`special(Ichor_ReturnToSea)`) puts you back on the same tile, heading the same way, in the ship.

---

## 3. The helm and its voyages

`EventScript_IchorHelm` is Nausikles at the steering oars: the deck's object (or bg event) runs it directly. "NAUSIKLES: Where to, Archon?", then a menu (`special(Ichor_BuildHelmMenu)`, ids `ICHOR_HELM_*`):

| Entry | When | Does |
|---|---|---|
| TAKE HER OUT | You came below from the sea | Back to the sea (§2) |
| CAST OFF | Moored at a port with a sea map | Out onto it in the ship (`special(Ichor_CastOff)`) |
| SET A COURSE | Not past Maleia (`FLAG_ICHOR_AT_SEA` clear) | The open ports but the one she's moored at, in capitals; then Nausikles's line for the port, a fade, the sea, and the port's quay. A port of open sea puts you out on its sea instead. With nowhere to go: "Nowhere else to go yet. The chart's blank past here." |
| THE WIND? | Always | "A fresh wind out of the west. Keep it behind you and she flies." A calm and Poseidon's grudge have their own lines. |
| STAY | Always | "Suit yourself. She'll keep." |

### The ports: `src/data/ichor_voyages.h`

One row per `VOYAGE_*` id (`include/constants/ichor_sailing.h`). **Adding a port is one `#define` and one row**; the menu, the landing and the crossing all read the table.

```c
[VOYAGE_LECHAION] = {
    .name = COMPOUND_STRING("Lechaion"),          // "Go ashore at Lechaion?"; the menu shows LECHAION
    .crossing = COMPOUND_STRING("NAUSIKLES: Up the gulf to Lechaion.\nThey haul ships over land there. Madness."),
    .gateFlag = FLAG_ICHOR_...,                   // on the helm's list once set; 0 keeps it closed
    VOYAGE_QUAY(MAP_LECHAION, 12, 8),             // or VOYAGE_NO_QUAY: a port of open sea
    VOYAGE_NO_SEA,                                // or VOYAGE_SEA(map, x, y, DIR_*): CAST OFF and boarding go there
},
```

The crossing line is two short lines with an explicit `\n` (check them with `tools/ichor/text_width.py`; 216 px is the box).

| Id | Port | Row |
|---|---|---|
| `VOYAGE_NONE` (0) | at sea | — |
| `VOYAGE_AKTI` | Akti's quay, (7,10), just south of the slice's gangplank at (7,9). No sea map yet: boarding goes on deck. Gate `FLAG_ICHOR_GOT_EUPLOIA`. Keep the arrival tile clear of people. | **Open** |
| `VOYAGE_ROUTE33` | The western sea: the westsea agent's row (a commented template sits above it) | Pending |
| `VOYAGE_CAPE_TAINARON`, `_KNOSSA`, `_LECHAION`, `_KALDERA` | Their maps are on other branches: names and lines written, gate 0, no quay, no sea (`ICHOR_PG_PORT_PENDING`) | Pending |

The Labors' and the Oikoumene's ports append after `VOYAGE_KALDERA`.

---

## 4. Wind (ODYSSEY §4)

`gIchorSave.epics.wind`: direction in bits 0–2, strength in bits 3–4, Poseidon's grudge bit 5, becalmed bit 6.

| Constant | Values |
|---|---|
| Direction, **where the wind blows from** (Zephyros, the west wind, carries you east) | `ICHOR_WIND_N`, `_NE`, `_E`, `_SE`, `_S`, `_SW`, `_W`, `_NW` (0–7, clockwise) |
| Strength | `ICHOR_WIND_CALM`, `_FRESH`, `_STRONG`; and `ICHOR_WIND_BECALMED` for `Ichor_SetWind` |
| Heading against it (`Ichor_GetSailing`, C) | `ICHOR_SAIL_CALM`, `_DOWNWIND` (from within 45° of behind you), `_CROSSWIND`, `_UPWIND` (from within 45° of ahead) |

**Each day** the daily reset (`Ichor_DoDailyEvents`, right after the daily seed turns) rolls a direction and a strength from the seed: calm 20%, fresh 55%, strong 25%. The grudge and an event calm survive it.

| Call | In | Out |
|---|---|---|
| `special(Ichor_SetWind)` | `VAR_0x8004` direction, `VAR_0x8005` strength | `ICHOR_WIND_BECALMED` is a calm the daily reset leaves alone (Thrinakia); any other strength lifts it |
| `specialvar(VAR_RESULT, Ichor_GetWind)` | | The direction; also `VAR_0x8004` direction, `VAR_0x8005` the strength that counts (calm when becalmed), `VAR_0x8006` TRUE under the grudge |
| `special(Ichor_BufferWind)` | | `STR_VAR_1` = "west, fresh" ("calm"; "ahead, strong" under the grudge), `STR_VAR_2` = "west", `STR_VAR_3` = "fresh" |
| `special(Ichor_SetGrudge)` / `special(Ichor_LiftGrudge)` | | Poseidon's grudge on (the Cyclops's boast) and off (a loved offering at a sea altar) |
| `specialvar(VAR_RESULT, Ichor_GetSailingEncounterRate)` | | The encounter rate for the ship's heading, in percent (50, 100, 150) |

**In the ship:**

| Heading | Speed (frames per tile) | Sail | Encounters |
|---|---|---|---|
| Downwind | 6, the current's speed; **4 with the new sail** (`FLAG_ICHOR_SHIP_SAIL`) | full | ×0.5 |
| Crosswind | 8, the surf speed | full | ×1 |
| Upwind | 8, rowing | slack | ×1.5 |
| Calm or becalmed | 8, rowing | slack | ×1 |

- **The surf state already moves at the running speed** (8 frames per tile), so rowing keeps it and the wind goes one step up the engine's ladder: 6 downwind, 4 with the new sail. The three numbers are `SAIL_FRAMES_*` in `src/ichor_sailing.c`.
- **A strong wind behind her** carries her one tile further on the first step from rest: tap once, sail two. Holding the pad, or steering another way, makes no difference.
- **Poseidon's grudge** turns the wind against whatever heading you take: always upwind, sail slack, ×1.5, and never calmer than fresh. While it holds, every new day blows strong.
- **The start menu's info panel** (the rites' BLESSING panel) shows "Wind: west, fresh" while you're at sea in the ship, under the blessing if there is one. It grows to 17 tiles wide for "Wind: south-east, strong".

---

## 5. The at-sea lock (ODYSSEY §4, O1)

While **`FLAG_ICHOR_AT_SEA`** is set, Daedalus's Wings refuse, from the bag and from the Relic Ring: "No herm out here. The sea has no roads." Herm flight goes through the Wings' fly map, so it's refused with them. The Town Map shows no "R FLY" and R does nothing. The helm offers no SET A COURSE.

Set the flag when you round Maleia and clear it at home; the Odyssey's scripts own it.

---

## 6. The Great Bear (ODYSSEY §4)

At night (the game's own time of day), on a `MAP_TYPE_OCEAN_ROUTE` map, while you're in the ship, the Great Bear's seven stars hang at the top of the screen, fixed to north: a 32×16 sprite, pale gold and blend-immune, so the night tint never dims it. The art is `graphics/field_effects/pics/ichor_great_bear.png`, drawn by `tools/ichor/art/great_bear.py`. Map loads and battles put it back as needed.

`specialvar(VAR_RESULT, Ichor_IsStarsOut)` is TRUE under the same three conditions: for the Outer Sea's night exit (batch 6) and Alethea's star reading.

---

## 7. Wild encounter overlays (POSTGAME §1, §3.4)

`src/ichor_postgame_encounters.c` keeps a table of overlays. Once a wild table has picked its slot and level, `wild_encounter.c` asks `Ichor_OverlayWildSpecies`, and the first row whose conditions hold and whose roll succeeds replaces the species, **at the table's level**. No map's `wild_encounters.json` entry changes.

| Row | Species | Odds | Where and when |
|---|---|---|---|
| **Shades on the roads** | `SPECIES_OBOLORN` (a stand-in until the dex lands: `ICHOR_STUB_AETHOS_DEX`) | 1 in 8 | Land encounters, `FLAG_ICHOR_POSTGAME` set, at night, on `MAP_TYPE_ROUTE` and `_OCEAN_ROUTE` maps that aren't dark (caves and towns never) |

**Batch 8's Time Fractures** append a row: species, odds, area, flag, time of day, map types, and an optional `condition` function for anything else (a Fracture's own maps).

---

## 8. What map agents put on their maps

| Map | Put | How |
|---|---|---|
| A port's quay | The ship (objects or metatiles) and a **gangplank** | Gangplank: coord or bg event, `VAR_0x8004` = the port, `goto(EventScript_IchorBoardShip)`. Hide both with a `FLAG_TEMP_*` unless `Ichor_IsMooredAt` is TRUE. Keep the row's quay tile clear. |
| A sea map | `MAP_TYPE_OCEAN_ROUTE`; a **landing** bg event per port | `VAR_0x8004` = the port, `goto(EventScript_IchorLand)`, on the tile you face from the water |
| `src/data/ichor_voyages.h` | **A row per port** | Name, crossing line, gate flag, quay, sea entry and heading (§3); one `#define` in `include/constants/ichor_sailing.h` |
| The deck | The helm and the deck's gangplank | Nausikles (or the steering oars) runs `EventScript_IchorHelm`; the gangplank runs `EventScript_IchorLeaveShip`. Arrivals land at `ICHOR_SHIP_DECK_X`/`_Y`, facing north. |

---

## 9. Tests: `pg_lib.lua` and `pg_sailing.sh`

**`tools/ichor/tests/pg_lib.lua`** extends `engine_lib.lua` for every post-game check:

| Helper | Does |
|---|---|
| `L.pgStart(x, y)` | A new game, then `pg_setup.inc`'s `PgLib_SetupHeader`: `FLAG_ICHOR_POSTGAME`, a Lv 70 party of six (Lapras leads), every relic in the bag, `FLAG_ICHOR_GOT_EUPLOIA`, the clock started, the slice's scenes done, a Repel; then Akti at (x, y), by default the quay |
| `L.setPostgame(on)`, `L.encounters(on)` | The post-game flag; wild encounters on (Repel off) or off |
| `L.warp(map, x, y)` | Load any map at any tile, as a door warp's load does (a water tile with `FLAG_ICHOR_ON_SHIP` set puts you in the ship) |
| `L.setHour(h)`, `L.night()`, `L.day()`, `L.timeOfDay()` | The local hour, keeping the day |
| `L.newDay()` | The clock a day on, and the daily events |
| `L.saveAndReload()` | Save, reset, CONTINUE |
| `L.epic8(name)`, `L.setEpic8`, `L.epic16`, `L.setEpic16`, `L.epicsBytes()` | IchorEpics fields by their `OFF_EPICS_*` names |
| `L.press`, `L.hold(key, n)`, `L.step(key)`, `L.pickMenu(n)` | Keys, steps, a scrolling menu's nth entry |
| `L.graphicsId()`, `L.movementAction()`, `L.surfing()`, `L.findSprite(cb)`, `L.spriteVisible(id)` | The player and sprites |
| `L.encode(s)`, `L.textAt(addr, s)`, `L.textContains(addr, s)` | Text in the game's charset |

A check's `pg_<area>_setup.s` writes `#include "tools/ichor/tests/pg_setup.inc"` after its `.include` lines (no apostrophes in that file's comments: cpp reads them), and its `pg_<area>_consts.c` defines the `OFF_ICHOR_EPICS`/`OFF_EPICS_*` offsets as `pg_sailing_consts.c` does.

**`tools/ichor/tests/pg_sailing.sh`** (45 checks): boards at Akti's quay onto the moored deck; THE WIND? and an empty SET A COURSE; the deck's gangplank; the ship in Akti's harbor (graphics, no blob, the follower stowed); downwind, upwind, crosswind and calm speeds and sails, the new sail, the strong wind's extra tile, Poseidon's grudge, the encounter rate; no beaching; the start menu's wind line; DECK and TAKE HER OUT to the same tile and heading; SET A COURSE and the crossing to Akti; a landing; the Wings refused at sea; the Great Bear by night (Akti is marked an ocean route in RAM for it) and gone by day; the daily wind, the grudge and an event calm across days; save and reload at sea; and Route 1's shades: none by day, one by night, none before the post-game. Screenshots in `build/pg_sailing/shots/`.

---

## 10. Stubbed, and left

| Tag | What | Until |
|---|---|---|
| `ICHOR_STUB_PG_SPRITES` | `ICHOR_SHIP_GFX`/`_SLACK` are the S.S. Tidal and Rayquaza's still frames | The sprites agent's `OBJ_EVENT_GFX_ICHOR_EUPLOIA`/`_SLACK` |
| `ICHOR_STUB_EUPLOIA_DECK` | `ICHOR_SHIP_DECK_MAP` is `MAP_PG_TEST_DECK` at (4,4) | The euploia agent's `MAP_EUPLOIA_DECK` |
| `ICHOR_PG_PORT_PENDING` | Five closed ports | Their maps; Route 33's row from the westsea agent |
| `ICHOR_STUB_AETHOS_DEX` | `SPECIES_OBOLORN` is a stand-in | The dex |

**Left for later batches:** currents and fog banks are map work with vanilla behaviors and Aeolus's Bag (ODYSSEY §4); the Outer Sea's night exit (batch 6) reads `Ichor_IsStarsOut`; the bronze ram's sea rocks (an obstacle script); Time Fractures (batch 8, a row in §7). The Great Bear doesn't check that Ursa Major is placed (it always is by the post-game).
