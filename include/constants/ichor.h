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
#define HERM_EMPORION_CITY          25  // town anchor, outside the 23-route completion count
#define HERM_AETHOS_MAX             32  // FLAG_ICHOR_HERMS_START's range
// The Oikoumene's waystones (OIKOUMENE §4): herms, Thoth's ibis pillars, stone
// babas and cairns of Ammon. Ids 32-63, flagged in FLAG_ICHOR_WAYSTONES_START's
// range; they join the Wings' fly map but never count toward Aethos's herms.
#define HERM_OIKOUMENE_FIRST        32
#define HERM_MAX                    64

// --- Relics (SYSTEMS §1) ----------------------------------------------------
// IchorSave.options bits
#define ICHOR_OPTION_RELIC_AUTO  (1 << 0)  // "Relic prompts": clear = ASK (the default), set = AUTO
#define ICHOR_OPTION_TINT_OFF    (1 << 1)  // "Day/night tint": clear = ON (the default), set = OFF: daytime colors all day

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
#define OMEN_WEATHER_KERAMEIKOS_FOG  2  // world-act2: fog over Astyra's Kerameikos
#define OMEN_WEATHER_KITHAIRON_FOG   3  // world-act2: fog on Mt. Kithairon
#define OMEN_WEATHER_ELEUSA_SUN     4
// Swarm entries (add new ones at the end)
#define OMEN_SWARM_GLAUKOIN    0  // world-act2: Astyra
#define OMEN_SWARM_ROUTE_6     1  // world-act2: the Eleutherai road
#define OMEN_SWARM_ISTHMUS_KERAZAP  2
#define OMEN_SWARM_SKIRON_KERAZAP   3
#define OMEN_SWARM_ELEUSA_MELIBEE   4
#define OMEN_SWARM_ELEUSA_STACHYSS  5
// Visitor entries (add new ones at the end)
#define OMEN_VISITOR_HIEROLIVE 0  // world-act2: Astyra
#define OMEN_VISITOR_THYRSIVY  1  // world-act2: Thyrsa's old trellises, after the Dionysia
#define OMEN_VISITOR_ELEUSA_KORANTHA 2
#define OMEN_VISITOR_EMPORION_PITHOUND 3
#define OMEN_VISITOR_ISTHMUS_NEMECUB 4
// Good-sign entries: the augur's blessing, or today's lucky number (1-6)
#define OMEN_SIGN_BLESSING     0
#define OMEN_SIGN_LUCKY(n)     (n)   // "Today, threes are lucky." is OMEN_SIGN_LUCKY(3)

// The xenia rest (SYSTEMS §10): Ichor_RestUntil's VAR_0x8004, and the rest menu's choices
#define ICHOR_REST_DAWN   0   // 06:00
#define ICHOR_REST_NOON   1   // 12:00
#define ICHOR_REST_DUSK   2   // 19:00
#define ICHOR_REST_NIGHT  3   // 20:30
#define ICHOR_REST_COUNT  4

// --- The Labyrinth (LABYRINTH.md §5) --------------------------------------------
// Names for the Thread's RETURN TO… list: the name id a ring's ON_LOAD gives
// Ichor_AddThreadAnchor. The strings are in src/data/ichor_thread.h; add new
// ones at the end. 0 shows the map's own name.
// Ichor_StartAsterion's options (VAR_0x8005), for chargers that aren't
// Asterion: Labor 4's boar is deaf, wanders off after a stun, and runs its own
// script when it hits the player.
#define ICHOR_CHARGER_DEAF        (1 << 0)  // sight only
#define ICHOR_CHARGER_NO_RETURN   (1 << 1)  // after a stun, back to its movement where it stands
#define ICHOR_CHARGER_HIT_SCRIPT  (1 << 2)  // a hit runs the object's own script instead of the knockdown
#define ICHOR_CHARGE_HIT          1         // VAR_0x8005 when that script runs from a hit

#define THREAD_ANCHOR_UNNAMED          0
#define THREAD_ANCHOR_GRAND_STAIRCASE  1
// Labyrinth I's anchors (10-29); Labyrinth II uses 30 and up (design/maps/Labyrinth_System.md)
#define THREAD_ANCHOR_R1_THRESHOLD           10
#define THREAD_ANCHOR_R1_FRESCO              11
#define THREAD_ANCHOR_R1_GATE                12
#define THREAD_ANCHOR_R1_CLEFT               13
#define THREAD_ANCHOR_R2_ENTRANCE            14
#define THREAD_ANCHOR_R2_LONG_HALL           15
#define THREAD_ANCHOR_R2_HERALDS             16
#define THREAD_ANCHOR_R2_GROTTO              17
#define THREAD_ANCHOR_R3_ENTRANCE            18
#define THREAD_ANCHOR_R3_STREAM              19
#define THREAD_ANCHOR_R3_WEBS                20
#define THREAD_ANCHOR_R3_WORKSHOP_DOOR       21
#define THREAD_ANCHOR_WORKSHOP               22
#define THREAD_ANCHOR_R4_ENTRANCE            23
#define THREAD_ANCHOR_R4_BARRACKS            24
#define THREAD_ANCHOR_R4_DIG                 25
#define THREAD_ANCHOR_R4_CHECKPOINT          26
// The Labyrinth's heart (the Labyrinth II build), from 40 up
#define THREAD_ANCHOR_RING5_GALLERY    40
#define THREAD_ANCHOR_RING5_WEST       41
#define THREAD_ANCHOR_RING5_EAST       42
#define THREAD_ANCHOR_RING5_TOMB       43
#define THREAD_ANCHOR_RING5_SOUTH      44
#define THREAD_ANCHOR_RING5_TREASURE   45
#define THREAD_ANCHOR_RING5_DEEP       46
#define THREAD_ANCHOR_RING6_LANDING    47
#define THREAD_ANCHOR_RING6_DIALS      48
#define THREAD_ANCHOR_RING6_FORGE      49
#define THREAD_ANCHOR_RING6_SHRINE     50
#define THREAD_ANCHOR_RING6_WEST       51
#define THREAD_ANCHOR_RING6_EAST       52
#define THREAD_ANCHOR_RING6_DEEP       53
#define THREAD_ANCHOR_RING7_STAIR      54
#define THREAD_ANCHOR_RING7_DOME       55
#define THREAD_ANCHOR_RING7_MIRRORS    56
#define THREAD_ANCHOR_RING7_DEEP       57

// Carried flames (SYSTEMS §2): VAR_TEMP_3 holds the kind, VAR_TEMP_2 the steps
// left. Names for the start menu are in src/ichor_relics.c; add new kinds at the end.
#define FLAME_NONE       0
#define FLAME_HEARTH     1
#define FLAME_SANCTUM    2
#define FLAME_THRESHOLD  3
#define FLAME_HESTIA_SHIP 4  // Lampon: Hestia's great hearth at Akti to the Euploia's (post-game)
#define FLAME_LERNA      5   // Kleon's fire at Lerna (Labor 2)
#define FLAME_PANATHENAIA 6  // the Panathenaia's torch race: the Dipylon to the Akropolis (SYSTEMS §7)
#define FLAME_COUNT      7
#define ICHOR_FLAME_GUTTER_STEPS  5  // "The flame gutters."

// Light radius levels for dark maps (SYSTEMS §2; sFlashLevelToRadius)
#define ICHOR_FLASH_NO_TORCH      7  // 24 px
#define ICHOR_FLASH_TORCH         3  // 56 px
#define ICHOR_FLASH_TORCH_STRONG  2  // 64 px: the Three-Flamed Torch, or Hecate's blessing
#define ICHOR_FLASH_TORCH_BOTH    1  // 72 px: both
#define ICHOR_FLASH_DOUSED        8  // dark: glow-paint only

// --- The festival calendar (SYSTEMS §7; ENGINE_API §7) ---------------------------
// An Aethos year is 36 days: 12 months of 3, the festival on each month's middle day.
#define ICHOR_MONTH_HEKATOMBAION   0
#define ICHOR_MONTH_METAGEITNION   1
#define ICHOR_MONTH_BOEDROMION     2
#define ICHOR_MONTH_PYANEPSION     3
#define ICHOR_MONTH_MAIMAKTERION   4   // the month of storms: no festival
#define ICHOR_MONTH_POSEIDEON      5
#define ICHOR_MONTH_GAMELION       6
#define ICHOR_MONTH_ANTHESTERION   7
#define ICHOR_MONTH_ELAPHEBOLION   8
#define ICHOR_MONTH_MOUNICHION     9
#define ICHOR_MONTH_THARGELION    10
#define ICHOR_MONTH_SKIROPHORION  11
#define ICHOR_MONTH_COUNT         12
#define ICHOR_DAYS_PER_MONTH       3
// Festivals: each is its month + 1, so a month's festival is ICHOR_FESTIVAL(month)
#define ICHOR_FESTIVAL_NONE        0
#define ICHOR_FESTIVAL_PANATHENAIA (ICHOR_MONTH_HEKATOMBAION + 1)   // Athena, Astyra: the torch race
#define ICHOR_FESTIVAL_KARNEIA     (ICHOR_MONTH_METAGEITNION + 1)   // Apollo, Lakonia
#define ICHOR_FESTIVAL_MYSTERIES   (ICHOR_MONTH_BOEDROMION + 1)     // Demeter, Eleusa
#define ICHOR_FESTIVAL_PYANOPSIA   (ICHOR_MONTH_PYANEPSION + 1)     // Apollo, every port
#define ICHOR_FESTIVAL_POSEIDEA    (ICHOR_MONTH_POSEIDEON + 1)      // Poseidon, every harbor
#define ICHOR_FESTIVAL_THEOGAMIA   (ICHOR_MONTH_GAMELION + 1)       // Hera and Zeus, Astyra
#define ICHOR_FESTIVAL_ANTHESTERIA (ICHOR_MONTH_ANTHESTERION + 1)   // Dionysus, everywhere: Ghost-types at night
#define ICHOR_FESTIVAL_DIONYSIA    (ICHOR_MONTH_ELAPHEBOLION + 1)   // Dionysus, Thyrsa
#define ICHOR_FESTIVAL_MOUNICHIA   (ICHOR_MONTH_MOUNICHION + 1)     // Artemis, Arkadia
#define ICHOR_FESTIVAL_THARGELIA   (ICHOR_MONTH_THARGELION + 1)     // Apollo and Artemis, Delphoi and Arkadia
#define ICHOR_FESTIVAL_KRONIA      (ICHOR_MONTH_SKIROPHORION + 1)   // Kronos, Kronion Hill and Titan sites

// --- Knucklebones (SYSTEMS §9; ENGINE_API §7) ----------------------------------
// EventScript_IchorKnucklebones's VAR_0x8004: who you play
#define ICHOR_BONES_CAUTIOUS  0   // rethrows only 1s
#define ICHOR_BONES_BOLD      1   // chases Aphrodite whenever it holds three different sides
#define ICHOR_BONES_SILENOS   2   // loaded bones: a 6 three times in ten
#define ICHOR_BONES_MOM       3   // two rethrows and a humming bee, until FLAG_ICHOR_MOM_CONFESSED
#define ICHOR_BONES_COUNT     4
// Internal to data/scripts/ichor_bones.pory
#define ICHOR_BONES_MENU_ROLL    4
#define ICHOR_BONES_MENU_STAND   5
#define ICHOR_BONES_MENU_LOADED  6
#define ICHOR_BONES_TIE     0
#define ICHOR_BONES_YOURS   1
#define ICHOR_BONES_THEIRS  2

// --- Excavation (SYSTEMS §5; ENGINE_API §8) -----------------------------------
// A daily dig spot's VAR_0x8005: the act's loot table, and the amphora whose
// sherds the spot holds, if any:
//   setvar(VAR_0x8005, ICHOR_DIG_ACT_I | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_ARACHNE))
#define ICHOR_DIG_ACT_I    1
#define ICHOR_DIG_ACT_II   2
#define ICHOR_DIG_ACT_III  3   // Act III and the post-game
#define ICHOR_DIG_SHERDS(amphora)  (((amphora) + 1) << 4)

// The 12 amphorae: sherds at FLAG_ICHOR_SHERDS_START + 4 * amphora (§5's table)
#define ICHOR_AMPHORA_KRONOS      0   // Kalliste
#define ICHOR_AMPHORA_PERSEPHONE  1   // Eleusa
#define ICHOR_AMPHORA_ARACHNE     2   // Emporion
#define ICHOR_AMPHORA_HERMES      3   // Emporion's coast
#define ICHOR_AMPHORA_HEPHAESTUS  4   // Kaldera
#define ICHOR_AMPHORA_ICARUS      5   // the Ikarian coasts
#define ICHOR_AMPHORA_PANDORA     6   // Astyra
#define ICHOR_AMPHORA_ORPHEUS     7   // Arkadia
#define ICHOR_AMPHORA_ATALANTA    8   // Arkadia
#define ICHOR_AMPHORA_PHAETHON    9   // Kaldera
#define ICHOR_AMPHORA_PARIS      10   // Kythera
#define ICHOR_AMPHORA_THESEUS    11   // Knossa
#define ICHOR_AMPHORA_COUNT      12
#define ICHOR_SHERDS_PER_AMPHORA  4
#define ICHOR_OSTRAKA_COUNT      30

#define ICHOR_AMPHORA_INCOMPLETE 0
#define ICHOR_AMPHORA_READY      1
#define ICHOR_AMPHORA_RESTORED   2
#define ICHOR_AMPHORA_INVALID    3
#define ICHOR_AMPHORA_MENU_ERROR 0xFFFF

// A fixed find's VAR_0x8005 is an item, or one of these
#define ICHOR_FIND_SHERD(amphora)  (0xF000 + (amphora))  // the amphora's next sherd
#define ICHOR_FIND_PROPHECY(n)     (0xF100 + (n))        // tablet n (1-8): FLAG_ICHOR_PROPHECY_START + n - 1
#define ICHOR_FIND_PAGE(n)         (0xF200 + (n))        // Daedalus's page n (1-7): FLAG_ICHOR_PAGES_START + n - 1
#define ICHOR_FIND_OSTRAKON        0xF300                // the next ostrakon

// Ichor_DigStart's answer (internal to data/scripts/ichor_dig.pory)
#define ICHOR_DIG_READY      0
#define ICHOR_DIG_NO_TROWEL  1
#define ICHOR_DIG_DUG_TODAY  2   // a daily spot, already dug today
#define ICHOR_DIG_BARE       3   // a fixed find, already dug
#define ICHOR_DIG_MODE_SPOT   0
#define ICHOR_DIG_MODE_FIXED  1
// Ichor_DigFindKind's answer
#define ICHOR_FIND_KIND_ITEM      0
#define ICHOR_FIND_KIND_SHERD     1
#define ICHOR_FIND_KIND_OSTRAKON  2
#define ICHOR_FIND_KIND_PROPHECY  3
#define ICHOR_FIND_KIND_PAGE      4

#endif // GUARD_CONSTANTS_ICHOR_H
