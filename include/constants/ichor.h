#ifndef GUARD_CONSTANTS_ICHOR_H
#define GUARD_CONSTANTS_ICHOR_H

// Ichor: constants shared by the engine and map scripts. See design/ENGINE_API.md.

// --- The gods (SYSTEMS §3) ------------------------------------------------
#define ICHOR_GOD_NONE        0
#define ICHOR_GOD_HESTIA      1
#define ICHOR_GOD_HERMES      2
#define ICHOR_GOD_DEMETER     3
#define ICHOR_GOD_DIONYSUS    4
#define ICHOR_GOD_ARTEMIS     5
#define ICHOR_GOD_HEPHAESTUS  6
#define ICHOR_GOD_APHRODITE   7
#define ICHOR_GOD_APOLLO      8
#define ICHOR_GOD_ARES        9
#define ICHOR_GOD_POSEIDON    10
#define ICHOR_GOD_ATHENA      11
#define ICHOR_GOD_HERA        12
#define ICHOR_GOD_ZEUS        13
#define ICHOR_GOD_HECATE      14
#define ICHOR_GOD_HADES       15
#define ICHOR_GOD_COUNT       16  // including NONE

// Favor for story deeds (SYSTEMS §3): special Ichor_AddFavor with VAR_0x8005 = one of these
#define ICHOR_FAVOR_LAUREL      15  // win that god's laurel or Pantheon seat
#define ICHOR_FAVOR_MYTH_QUEST  10  // finish that god's myth-quest
#define ICHOR_FAVOR_FESTIVAL    5   // take part in that god's festival
#define ICHOR_FAVOR_CLEANSE     3   // cleanse a desecrated altar

// The Relic Ring's entry for Hestia's Hearthfire (not an item)
#define ICHOR_RING_HEARTHFIRE   0xFFF0

// --- Herm waystones (SYSTEMS §4) ---------------------------------------------
// One great herm per land route, named for its map section in design/AETHOS_MAP.md
// (sea routes have none). HERM_COUNT counts the routes before the post-game: the
// Scroll of Deeds and the all-herms bonus count those.
#define HERM_KALLISTE_ROUTE_1       0
#define HERM_AETHOS_ROUTE_4         1
#define HERM_AETHOS_ROUTE_5         2
#define HERM_AETHOS_ROUTE_6         3
#define HERM_AETHOS_ROUTE_7         4
#define HERM_AETHOS_ROUTE_8         5
#define HERM_AETHOS_ROUTE_9         6
#define HERM_AETHOS_ROUTE_11        7
#define HERM_AETHOS_ROUTE_12        8
#define HERM_AETHOS_ROUTE_13        9
#define HERM_AETHOS_ROUTE_14        10
#define HERM_AETHOS_ROUTE_15        11
#define HERM_AETHOS_ROUTE_16        12
#define HERM_AETHOS_ROUTE_17        13
#define HERM_AETHOS_ROUTE_18        14
#define HERM_BULL_ROAD              15
#define HERM_AETHOS_ROUTE_25        16
#define HERM_AETHOS_ROUTE_26        17
#define HERM_AETHOS_ROUTE_27        18
#define HERM_AETHOS_ROUTE_28        19
#define HERM_AETHOS_ROUTE_29        20
#define HERM_AETHOS_ROUTE_30        21
#define HERM_THE_ASCENT             22
#define HERM_COUNT                  23
// the post-game's land routes, after HERM_COUNT
#define HERM_AETHOS_ROUTE_31        23
#define HERM_AETHOS_ROUTE_32        24
// Ichor: world-act3: Kythera's great herm at the Foam Road's fork (SCRIPT.md
// III-1D, FLAG_ICHOR_HERM_KYTHERA). Kythera isn't an AETHOS_MAP route, so it sits
// outside HERM_COUNT, and its row has no map section: Skandeia stays the
// island's one fly target.
#define HERM_KYTHERA_FOAM_ROAD      25
#define HERM_MAX                   32  // the flag range's size

// --- Relics (SYSTEMS §1) ----------------------------------------------------
// IchorSave.options bits
#define ICHOR_OPTION_RELIC_AUTO  (1 << 0)  // "Relic prompts": clear = ASK (the default), set = AUTO

// gFieldEffectArguments[0] for a field effect a relic performs: the player
// raises the relic and its icon shows, instead of a Pokémon's cut-in. The low
// bits are the item. It stays below VARS_START, so setfieldeffectargument
// passes it as a value.
#define ICHOR_FIELD_EFFECT_RELIC  0x2000

// Ichor_CanUseRelic results (VAR_RESULT)
#define ICHOR_RELIC_OK         0
#define ICHOR_RELIC_MISSING    1  // the player doesn't have it
#define ICHOR_RELIC_FORBIDDEN  2  // FLAG_ICHOR_NO_RELICS: this place forbids outside tools
#define ICHOR_RELIC_TOO_WEAK   3  // it needs the relic's upgrade

// --- The Labyrinth (LABYRINTH.md §5) --------------------------------------------
// Names for the Thread's RETURN TO… list: the name id a ring's ON_LOAD gives
// Ichor_AddThreadAnchor. The strings are in src/data/ichor_thread.h; add new
// ones at the end. 0 shows the map's own name.
#define THREAD_ANCHOR_UNNAMED          0
#define THREAD_ANCHOR_GRAND_STAIRCASE  1

// Light radius levels for dark maps (SYSTEMS §2; sFlashLevelToRadius)
#define ICHOR_FLASH_NO_TORCH      7  // 24 px
#define ICHOR_FLASH_TORCH         3  // 56 px
#define ICHOR_FLASH_TORCH_STRONG  2  // 64 px: the Three-Flamed Torch, or Hecate's blessing
#define ICHOR_FLASH_TORCH_BOTH    1  // 72 px: both
#define ICHOR_FLASH_DOUSED        8  // dark: glow-paint only

#endif // GUARD_CONSTANTS_ICHOR_H
