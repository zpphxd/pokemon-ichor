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
#define HERM_AETHOS_MAX             32  // FLAG_ICHOR_HERMS_START's range
// The Oikoumene's waystones (OIKOUMENE §4): herms, Thoth's ibis pillars, stone
// babas and cairns of Ammon. Ids 32-63, flagged in FLAG_ICHOR_WAYSTONES_START's
// range; they join the Wings' fly map but never count toward Aethos's herms.
#define HERM_OIKOUMENE_FIRST        32
#define HERM_MAX                    64

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

// --- Omens (SYSTEMS §6) ------------------------------------------------------
// IchorSave.omenKind: today's omen. omenEntry numbers the entries within a kind.
#define OMEN_NONE       0
#define OMEN_SWARM      1
#define OMEN_VISITOR    2
#define OMEN_WEATHER    3
#define OMEN_GOOD_SIGN  4
#define OMEN_STRANGER   5
// Weather entries (SYSTEMS §6; add new ones at the end)
#define OMEN_WEATHER_KRYOPUFF  0  // snow on the Ascent's lowest slopes
#define OMEN_WEATHER_LERNIP    1  // rain over Lake Stymphalia (Phase 4 SCRIPT.md, the Lernip hunt)

// --- The Labyrinth (LABYRINTH.md §5) --------------------------------------------
// Names for the Thread's RETURN TO… list: the name id a ring's ON_LOAD gives
// Ichor_AddThreadAnchor. The strings are in src/data/ichor_thread.h; add new
// ones at the end. 0 shows the map's own name.
#define THREAD_ANCHOR_UNNAMED          0
#define THREAD_ANCHOR_GRAND_STAIRCASE  1

// Carried flames (SYSTEMS §2): VAR_TEMP_3 holds the kind, VAR_TEMP_2 the steps
// left. Names for the start menu are in src/ichor_relics.c; add new kinds at the end.
#define FLAME_NONE       0
#define FLAME_HEARTH     1
#define FLAME_SANCTUM    2
#define FLAME_THRESHOLD  3
#define FLAME_COUNT      4
#define ICHOR_FLAME_GUTTER_STEPS  5  // "The flame gutters."

// Light radius levels for dark maps (SYSTEMS §2; sFlashLevelToRadius)
#define ICHOR_FLASH_NO_TORCH      7  // 24 px
#define ICHOR_FLASH_TORCH         3  // 56 px
#define ICHOR_FLASH_TORCH_STRONG  2  // 64 px: the Three-Flamed Torch, or Hecate's blessing
#define ICHOR_FLASH_TORCH_BOTH    1  // 72 px: both
#define ICHOR_FLASH_DOUSED        8  // dark: glow-paint only

#endif // GUARD_CONSTANTS_ICHOR_H
