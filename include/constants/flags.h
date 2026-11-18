#ifndef GUARD_CONSTANTS_FLAGS_H
#define GUARD_CONSTANTS_FLAGS_H

#include "constants/trainers.h"
#include "constants/opponents.h"
#include "constants/rematches.h"


// Temporary Flags
// These temporary flags are are cleared every time a map is loaded. They are used
// for things like shortening an NPCs introduction text if the player already spoke
// to them once.
#define TEMP_FLAGS_START 0x0
#define FLAG_TEMP_1      (TEMP_FLAGS_START + 0x1)
#define FLAG_TEMP_2      (TEMP_FLAGS_START + 0x2)
#define FLAG_TEMP_3      (TEMP_FLAGS_START + 0x3)
#define FLAG_TEMP_4      (TEMP_FLAGS_START + 0x4)
#define FLAG_TEMP_5      (TEMP_FLAGS_START + 0x5)  // Unused Flag
#define FLAG_TEMP_6      (TEMP_FLAGS_START + 0x6)  // Unused Flag
#define FLAG_TEMP_7      (TEMP_FLAGS_START + 0x7)  // Unused Flag
#define FLAG_TEMP_8      (TEMP_FLAGS_START + 0x8)  // Unused Flag
#define FLAG_TEMP_9      (TEMP_FLAGS_START + 0x9)  // Unused Flag
#define FLAG_TEMP_A      (TEMP_FLAGS_START + 0xA)  // Unused Flag
#define FLAG_TEMP_B      (TEMP_FLAGS_START + 0xB)  // Unused Flag
#define FLAG_TEMP_C      (TEMP_FLAGS_START + 0xC)  // Unused Flag
#define FLAG_TEMP_D      (TEMP_FLAGS_START + 0xD)  // Unused Flag
#define FLAG_TEMP_E      (TEMP_FLAGS_START + 0xE)  // When set, follower Pokémon won't be spawned
#define FLAG_TEMP_F      (TEMP_FLAGS_START + 0xF)  // Unused Flag
#define FLAG_TEMP_10     (TEMP_FLAGS_START + 0x10) // Unused Flag
#define FLAG_TEMP_11     (TEMP_FLAGS_START + 0x11)
#define FLAG_TEMP_12     (TEMP_FLAGS_START + 0x12)
#define FLAG_TEMP_13     (TEMP_FLAGS_START + 0x13)
#define FLAG_TEMP_14     (TEMP_FLAGS_START + 0x14)
#define FLAG_TEMP_15     (TEMP_FLAGS_START + 0x15)
#define FLAG_TEMP_16     (TEMP_FLAGS_START + 0x16)
#define FLAG_TEMP_17     (TEMP_FLAGS_START + 0x17)
#define FLAG_TEMP_18     (TEMP_FLAGS_START + 0x18)
#define FLAG_TEMP_19     (TEMP_FLAGS_START + 0x19)
#define FLAG_TEMP_1A     (TEMP_FLAGS_START + 0x1A)
#define FLAG_TEMP_1B     (TEMP_FLAGS_START + 0x1B)
#define FLAG_TEMP_1C     (TEMP_FLAGS_START + 0x1C)
#define FLAG_TEMP_1D     (TEMP_FLAGS_START + 0x1D)
#define FLAG_TEMP_1E     (TEMP_FLAGS_START + 0x1E)
#define FLAG_TEMP_1F     (TEMP_FLAGS_START + 0x1F)
#define TEMP_FLAGS_END   FLAG_TEMP_1F
#define NUM_TEMP_FLAGS   (TEMP_FLAGS_END - TEMP_FLAGS_START + 1)

#if IS_FRLG

#include "constants/flags_frlg.h"

#else

#define FLAG_ICHOR_DEXNAV_SEARCHING        0x20 // Ichor: DexNav (Augur's Eye) search active
#define FLAG_ICHOR_DEXNAV_GET              0x21 // Ichor: Augur's Eye obtained, shows in start menu
#define FLAG_ICHOR_DEXNAV_DETECTOR         0x22 // Ichor: Augur's Eye detector mode
#define FLAG_ICHOR_FOLLOWERS_DISABLED      0x23 // Ichor: set during cutscenes to hide the follower
#define FLAG_ICHOR_SET_WATER_CLOCK 0x24 // Ichor: set the water clock in your room
#define FLAG_ICHOR_TALKED_TO_MOM 0x25 // Ichor: Melitta sent you to the Klotheia
#define FLAG_ICHOR_THREAD_READ 0x26 // Ichor: Halia tried to read your thread
#define FLAG_ICHOR_GOT_STARTER 0x27 // Ichor: chose a starter at the Akademia
#define FLAG_ICHOR_KLEON_TOOK_STARTER 0x28 // Ichor: Kleon took his starter
#define FLAG_ICHOR_KLEON_BATTLE_1_DONE 0x29 // Ichor: first Kleon battle fought
#define FLAG_ICHOR_WON_KLEON_1 0x2A // Ichor: won the first Kleon battle
#define FLAG_ICHOR_GOT_POKEBALLS 0x2B // Ichor: Daphne gave the starting Poke Balls
#define FLAG_ICHOR_RUINS_CLEARED 0x2C // Ichor: drove the Titanborn off Kronion Hill
#define FLAG_ICHOR_FOUND_TITAN_TABLET 0x2D // Ichor: picked up the Titanborn tablet
#define FLAG_ICHOR_ARRIVED_AKTI 0x2E // Ichor: first arrival in Akti
#define FLAG_ICHOR_VISITED_AKTI 0x2F // Ichor: Akti visited (fly target)
#define FLAG_ICHOR_HEARTH_TRIAL_DONE 0x30 // Ichor: relit Hestia's hearth
#define FLAG_ICHOR_GOT_CHARCOAL 0x31 // Ichor: trial reward: Charcoal
#define FLAG_ICHOR_GOT_TM_FACADE 0x32 // Ichor: Ione gave TM42 Facade
#define FLAG_ICHOR_SLICE_COMPLETE 0x33 // Ichor: Phase 1 slice finished at the harbor
#define FLAG_ICHOR_GOT_KYDIPPE_ORAN 0x34 // Ichor: gift: Kydippe's Oran Berry
#define FLAG_ICHOR_GOT_ROUTE1_SITRUS 0x35 // Ichor: gift: Route 1 Sitrus Berry
#define FLAG_ICHOR_GOT_MOOMOO_MILK 0x36 // Ichor: gift: Moomoo Milk
#define FLAG_ICHOR_GOT_MYSTIC_WATER 0x37 // Ichor: gift: Mystic Water
#define FLAG_ICHOR_GOT_OLD_ROD 0x38 // Ichor: gift: Old Rod
#define FLAG_ICHOR_HIDE_KRATER_NEBREL 0x39 // Ichor: hide Nebrel's krater
#define FLAG_ICHOR_HIDE_KRATER_KYNDER 0x3A // Ichor: hide Kynder's krater
#define FLAG_ICHOR_HIDE_KRATER_HIPLING 0x3B // Ichor: hide Hipling's krater
#define FLAG_ICHOR_HIDE_KLEON_ELAIA 0x3C // Ichor: hide Kleon in Elaia
#define FLAG_ICHOR_HIDE_ALETHEA_AKADEMIA 0x3D // Ichor: hide Alethea in the Akademia
#define FLAG_ICHOR_HIDE_ALETHEA_ELAIA 0x3E // Ichor: hide Alethea in Elaia
#define FLAG_ICHOR_HIDE_ALETHEA_RUINS 0x3F // Ichor: hide Alethea on Kronion Hill
#define FLAG_ICHOR_HIDE_RUINS_GRUNTS 0x40 // Ichor: hide the Titanborn on Kronion Hill
#define FLAG_ICHOR_HIDE_TITAN_TABLET 0x41 // Ichor: hide the dropped tablet
#define FLAG_ICHOR_HIDE_ROUTE1_FLOCK 0x42 // Ichor: hide the goat flock on Route 1
#define FLAG_ICHOR_HIDE_KLEON_AKTI 0x43 // Ichor: hide Kleon in Akti
#define FLAG_ICHOR_HIDE_ALETHEA_AKTI 0x44 // Ichor: hide Alethea in Akti
#define FLAG_ICHOR_NO_WHITEOUT 0x45 // Ichor: set to make a battle loss continue the story
#define FLAG_ICHOR_ITEM_ROUTE1_POKE_BALL 0x46 // Ichor: item ball: Route 1 Poke Ball
#define FLAG_ICHOR_ITEM_ROUTE1_MIRACLE_SEED 0x47 // Ichor: item ball: Route 1 Miracle Seed
#define FLAG_ICHOR_ITEM_ROUTE1_POTION 0x48 // Ichor: item ball: Route 1 Potion
#define FLAG_ICHOR_ITEM_KRONION_ESCAPE_ROPE 0x49 // Ichor: item ball: Kronion Hill Escape Rope
#define FLAG_ICHOR_GOT_ELAIA_RELIC_COPPER 0x4A // Ichor: found the Relic Copper in Elaia's well
#define FLAG_ICHOR_ITEM_ELAIA_POTION 0x4B // Ichor: item ball: Potion by Elaia's olive press
#define FLAG_ICHOR_GOT_GLYKERA_CAKES 0x4C // Ichor: Glykera traded honey cakes for Melitta's honey
#define FLAG_ICHOR_DID_KIMON_TRADE 0x4D // Ichor: traded Kimon a Galekit for his Halcyling, Arion
#define FLAG_ICHOR_GOT_KIMON_PEARLS 0x4E // Ichor: Kimon's pearls, for the Hearth Laurel
#define FLAG_ICHOR_HIDE_SCRIBE 0x4F // Ichor: hide the traveling scribe in Elaia's square after beat 4

// Scripts
#define FLAG_ICHOR_ITEM_KRONION_BURN_HEAL        0x050 // Ichor: item ball: Kronion Hill Burn Heal, on the olive terraces
#define FLAG_SET_WALL_CLOCK                      0x51
#define FLAG_RESCUED_BIRCH                       0x52
#define FLAG_LEGENDARIES_IN_SOOTOPOLIS           0x53

#define FLAG_ICHOR_HIDE_AKTI_LOOSE_GOAT      0x54 // Ichor: Akti: object flag that hides Kapra, the loose goat
#define FLAG_ICHOR_GOT_SOOTHE_BELL           0x55 // Ichor: Akti: Aigon gave his goat's old bell (Soothe Bell)

#define FLAG_ICHOR_ITEM_KRONION_EVERSTONE    0x056 // Ichor: item ball: Kronion Hill Everstone, on the lookout shelf
#define FLAG_UNUSED_0x057                    0x057 // Unused Flag
#define FLAG_UNUSED_0x058                    0x058 // Unused Flag
#define FLAG_UNUSED_0x059                    0x059 // Unused Flag
#define FLAG_RECEIVED_BIKE                   0x5A
#define FLAG_WATTSON_REMATCH_AVAILABLE       0x5B
#define FLAG_COLLECTED_ALL_SILVER_SYMBOLS    0x5C
#define FLAG_UNUSED_0x05D                    0x05D // Unused Flag
#define FLAG_UNUSED_0x05E                    0x05E // Unused Flag
#define FLAG_RECEIVED_POKEBLOCK_CASE         0x5F
#define FLAG_RECEIVED_SECRET_POWER           0x60
#define FLAG_MET_TEAM_AQUA_HARBOR            0x61
#define FLAG_UNUSED_0x062                    0x062 // Unused Flag
#define FLAG_UNUSED_0x063                    0x063 // Unused Flag
#define FLAG_UNUSED_0x064                    0x064 // Unused Flag
#define FLAG_UNUSED_0x065                    0x065 // Unused Flag
#define FLAG_UNUSED_0x066                    0x066 // Unused Flag
#define FLAG_UNUSED_0x067                    0x067 // Unused Flag

#define FLAG_ICHOR_GOT_SHELL_BELL            0x68 // Ichor: Akti: Doris traded her shell bell for a Heart Scale

#define FLAG_OCEANIC_MUSEUM_MET_REPORTER     0x69
#define FLAG_RECEIVED_HM_STRENGTH            0x6A
#define FLAG_UNUSED_0x06B                    0x06B // Unused Flag
#define FLAG_WHITEOUT_TO_LAVARIDGE           0x6C // Set after defeating Flannery, so the player can't white out from poison before receiving Go Goggles
#define FLAG_UNUSED_0x06D                    0x06D // Unused Flag
#define FLAG_UNUSED_0x06E                    0x06E // Unused Flag
#define FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT  0x6F
#define FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE  0x70
#define FLAG_UNUSED_RS_LEGENDARY_BATTLE_DONE 0x71 // Unused Flag. Used in R/S to indicate whether player defeated or caught Groudon/Kyogre in Cave of Origin.
#define FLAG_SCOTT_CALL_BATTLE_FRONTIER      0x72 // Used in order to activate a phone call from Scott, inviting the player to the SS Tidal.
#define FLAG_UNUSED_0x073                    0x073 // Unused Flag
#define FLAG_ADVENTURE_STARTED               0x74 // RECEIVED Pokédex.
#define FLAG_DEFEATED_MAGMA_SPACE_CENTER     0x75 // Set when Team Magma is defeated at Mossdeep's Space Center.
#define FLAG_UNUSED_0x076                    0x076 // Unused Flag

#define FLAG_CANCEL_BATTLE_ROOM_CHALLENGE    0x77

#define FLAG_LANDMARK_MIRAGE_TOWER           0x78
#define FLAG_UNUSED_0x079                    0x079 // Unused Flag
#define FLAG_UNUSED_0x07A                    0x07A // Unused Flag
#define FLAG_UNUSED_0x07B                    0x07B // Unused Flag
#define FLAG_UNUSED_0x07C                    0x07C // Unused Flag
#define FLAG_UNUSED_0x07D                    0x07D // Unused Flag
#define FLAG_DEFEATED_WALLY_VICTORY_ROAD     0x7E
#define FLAG_UNUSED_0x07F                    0x07F // Unused Flag
#define FLAG_ENABLE_ROXANNE_FIRST_CALL       0x80 // Set after defeating Brawly. This will activate a call with Roxanne in order to register her.
#define FLAG_KYOGRE_ESCAPED_SEAFLOOR_CAVERN  0x81
#define FLAG_UNUSED_0x082                    0x082 // Unused Flag
#define FLAG_UNUSED_0x083                    0x083 // Unused Flag
#define FLAG_UNUSED_0x084                    0x084 // Unused Flag
#define FLAG_RECEIVED_AMULET_COIN            0x85
#define FLAG_PENDING_DAYCARE_EGG             0x86
#define FLAG_UNUSED_0x087                    0x087 // Unused Flag
#define FLAG_ENABLE_FIRST_WALLY_POKENAV_CALL 0x88 // Set after defeating Wally outside Mauville Gym. Will activate a call later to register Wally.
#define FLAG_UNUSED_0x089                    0x089 // Unused Flag
#define FLAG_SCOTT_CALL_FORTREE_GYM          0x8A // Triggers call from Scott after defeating Winona
#define FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY   0x8B
#define FLAG_UNUSED_0x08C                    0x08C // Unused Flag
#define FLAG_UNUSED_0x08D                    0x08D // Unused Flag
#define FLAG_UNUSED_0x08E                    0x08E // Unused Flag
#define FLAG_UNUSED_0x08F                    0x08F // Unused Flag
#define FLAG_UNUSED_0x090                    0x090 // Unused Flag
#define FLAG_CAUGHT_LUGIA                    0x91
#define FLAG_CAUGHT_HO_OH                    0x92
#define FLAG_UNUSED_0x093                    0x093 // Unused Flag
#define FLAG_UNUSED_0x094                    0x094 // Unused Flag
#define FLAG_DELIVERED_DEVON_GOODS           0x95
#define FLAG_UNUSED_0x096                    0x096 // Unused Flag
#define FLAG_RECEIVED_CASTFORM               0x97
#define FLAG_UNUSED_0x098                    0x098 // Unused Flag
#define FLAG_UNUSED_0x099                    0x099 // Unused Flag
#define FLAG_UNUSED_0x09A                    0x09A // Unused Flag
#define FLAG_UNUSED_0x09B                    0x09B // Unused Flag
#define FLAG_BATTLE_FRONTIER_TRADE_DONE      0x9C
#define FLAG_FORCE_MIRAGE_TOWER_VISIBLE      0x9D
#define FLAG_UNUSED_0x09E                    0x09E // Unused Flag
#define FLAG_UNUSED_0x09F                                0x09F // Unused Flag
#define FLAG_UNUSED_0x0A0                    0x0A0 // Unused Flag
#define FLAG_UNUSED_0x0A1                    0x0A1 // Unused Flag
#define FLAG_UNUSED_0x0A2                    0x0A2 // Unused Flag
#define FLAG_UNUSED_0x0A3                    0x0A3 // Unused Flag
#define FLAG_UNUSED_0x0A4                    0x0A4 // Unused Flag
#define FLAG_UNUSED_0x0A5                    0x0A5 // Unused Flag
#define FLAG_UNUSED_0x0A6                    0x0A6 // Unused Flag
#define FLAG_UNUSED_0x0A7                    0x0A7 // Unused Flag
#define FLAG_UNUSED_0x0A8                    0x0A8 // Unused Flag
#define FLAG_UNUSED_0x0A9                    0x0A9 // Unused Flag
#define FLAG_UNUSED_0x0AA                    0x0AA // Unused Flag
#define FLAG_UNUSED_0x0AB                    0x0AB // Unused Flag
#define FLAG_UNUSED_0x0AC                    0x0AC // Unused Flag
#define FLAG_HIDE_SECRET_BASE_TRAINER        0xAD
#define FLAG_DECORATION_1                    0xAE
#define FLAG_DECORATION_2                    0xAF
#define FLAG_DECORATION_3                    0xB0
#define FLAG_DECORATION_4                    0xB1
#define FLAG_DECORATION_5                    0xB2
#define FLAG_DECORATION_6                    0xB3
#define FLAG_DECORATION_7                    0xB4
#define FLAG_DECORATION_8                    0xB5
#define FLAG_DECORATION_9                    0xB6
#define FLAG_DECORATION_10                   0xB7
#define FLAG_DECORATION_11                   0xB8
#define FLAG_DECORATION_12                   0xB9
#define FLAG_DECORATION_13                   0xBA
#define FLAG_DECORATION_14                   0xBB
#define FLAG_RECEIVED_POKENAV                0xBC
#define FLAG_DELIVERED_STEVEN_LETTER         0xBD
#define FLAG_UNUSED_0x0BE                    0x0BE // Unused Flag
#define FLAG_UNUSED_0x0BF                    0x0BF // Unused Flag
#define FLAG_UNUSED_0x0C0                    0x0C0 // Unused Flag
#define FLAG_UNUSED_0x0C1                    0x0C1 // Unused Flag
#define FLAG_UNUSED_0x0C2                    0x0C2 // Unused Flag
#define FLAG_UNUSED_0x0C3                    0x0C3 // Unused Flag
#define FLAG_UNUSED_0x0C4                    0x0C4 // Unused Flag
#define FLAG_UNUSED_0x0C5                    0x0C5 // Unused Flag
#define FLAG_UNUSED_0x0C6                    0x0C6 // Unused Flag
#define FLAG_RUSTURF_TUNNEL_OPENED           0xC7
#define FLAG_UNUSED_0x0C8                    0x0C8 // Unused Flag
#define FLAG_UNUSED_0x0C9                    0x0C9 // Unused Flag
#define FLAG_UNUSED_0x0CA                    0x0CA // Unused Flag
#define FLAG_UNUSED_0x0CB                    0x0CB // Unused Flag
#define FLAG_UNUSED_0x0CC                    0x0CC // Unused Flag
#define FLAG_UNUSED_0x0CD                           0x0CD // Unused Flag
#define FLAG_UNUSED_0x0CE                    0x0CE // Unused Flag
#define FLAG_MET_ARCHIE_METEOR_FALLS         0xCF
#define FLAG_UNUSED_0x0D0                    0x0D0 // Unused Flag
#define FLAG_UNUSED_0x0D1                    0x0D1 // Unused Flag
#define FLAG_UNUSED_0x0D2                    0x0D2 // Unused Flag
#define FLAG_UNUSED_0x0D3                    0x0D3 // Unused Flag
#define FLAG_RECEIVED_RED_OR_BLUE_ORB        0xD4
#define FLAG_UNUSED_0x0D5                    0x0D5 // Unused Flag
#define FLAG_ENABLE_WALLY_MATCH_CALL         0xD6
#define FLAG_ENABLE_SCOTT_MATCH_CALL         0xD7
#define FLAG_ENABLE_MOM_MATCH_CALL           0xD8
#define FLAG_UNUSED_0x0D9                    0x0D9 // Unused Flag
#define FLAG_UNUSED_0x0DA                    0x0DA // Unused Flag
#define FLAG_UNUSED_0x0DB                    0x0DB // Unused Flag

#define FLAG_NEVER_SET_0x0DC                 0xDC // This flag is read, but never written to

#define FLAG_UNUSED_0x0DD                    0x0DD // Unused Flag
#define FLAG_UNUSED_0x0DE                    0x0DE // Unused Flag
#define FLAG_UNUSED_0x0DF                    0x0DF // Unused Flag
#define FLAG_UNUSED_0x0E0                    0x0E0 // Unused Flag
#define FLAG_UNUSED_0x0E1                    0x0E1 // Unused Flag
#define FLAG_UNUSED_0x0E2                    0x0E2 // Unused Flag
#define FLAG_UNUSED_0x0E3                    0x0E3 // Unused Flag
#define FLAG_UNUSED_0x0E4                    0x0E4 // Unused Flag
#define FLAG_UNUSED_0x0E5                    0x0E5 // Unused Flag
#define FLAG_UNUSED_0x0E6                    0x0E6 // Unused Flag
#define FLAG_UNUSED_0x0E7                    0x0E7 // Unused Flag
#define FLAG_UNUSED_0x0E8                    0x0E8 // Unused Flag

#define FLAG_ICHOR_AKTI_GOAT_HOME            0xE9 // Ichor: Akti: Kapra, Aigon's loose goat, was sent home

#define FLAG_UNUSED_0x0EA                    0x0EA // Unused Flag
#define FLAG_UNUSED_0x0EB                    0x0EB // Unused Flag
#define FLAG_UNUSED_0x0EC                    0x0EC // Unused Flag
#define FLAG_RECEIVED_SILVER_SHIELD          0xED
#define FLAG_RECEIVED_GOLD_SHIELD            0xEE
#define FLAG_UNUSED_0x0EF                    0x0EF // Unused Flag
#define FLAG_UNUSED_0x0F0                    0x0F0 // Unused Flag
#define FLAG_UNUSED_0x0F1                    0x0F1 // Unused Flag
#define FLAG_UNUSED_0x0F2                    0x0F2 // Unused Flag
#define FLAG_UNUSED_0x0F3                    0x0F3 // Unused Flag
#define FLAG_UNUSED_0x0F4                    0x0F4 // Unused Flag
#define FLAG_UNUSED_0x0F5                    0x0F5 // Unused Flag
#define FLAG_UNUSED_0x0F6                    0x0F6 // Unused Flag
#define FLAG_UNUSED_0x0F7                    0x0F7 // Unused Flag
#define FLAG_UNUSED_0x0F8                    0x0F8 // Unused Flag
#define FLAG_UNUSED_0x0F9                    0x0F9 // Unused Flag
#define FLAG_UNUSED_0x0FA                    0x0FA // Unused Flag
#define FLAG_UNUSED_0x0FB                    0x0FB // Unused Flag
#define FLAG_UNUSED_0x0FC                    0x0FC // Unused Flag
#define FLAG_ENABLE_RIVAL_MATCH_CALL         0xFD
#define FLAG_UNUSED_0x0FE                    0x0FE // Unused Flag
#define FLAG_LATIOS_OR_LATIAS_ROAMING        0xFF
#define FLAG_UNUSED_0x100                    0x100 // Unused Flag
#define FLAG_UNUSED_0x101                    0x101 // Unused Flag
#define FLAG_UNUSED_0x102                    0x102 // Unused Flag
#define FLAG_UNUSED_0x103                    0x103 // Unused Flag
#define FLAG_UNUSED_0x104                    0x104 // Unused Flag
#define FLAG_UNUSED_0x105                    0x105 // Unused Flag
#define FLAG_UNUSED_0x106                    0x106 // Unused Flag
#define FLAG_UNUSED_0x107                    0x107 // Unused Flag
#define FLAG_UNUSED_0x108                    0x108 // Unused Flag
#define FLAG_UNUSED_0x109                    0x109 // Unused Flag
#define FLAG_UNUSED_0x10A                    0x10A // Unused Flag
#define FLAG_UNUSED_0x10B                    0x10B // Unused Flag
#define FLAG_SECRET_BASE_REGISTRY_ENABLED    0x10C
#define FLAG_UNUSED_0x10D                    0x10D // Unused Flag
#define FLAG_CONTEST_SKETCH_CREATED          0x10E  // Set but never read
#define FLAG_UNUSED_0x10F                    0x10F // Unused Flag
#define FLAG_RECEIVED_EXP_SHARE              0x110
#define FLAG_POKERUS_EXPLAINED               0x111
#define FLAG_RECEIVED_RUNNING_SHOES          0x112
#define FLAG_UNUSED_0x113                    0x113 // Unused Flag
#define FLAG_UNUSED_0x114                    0x114 // Unused Flag
#define FLAG_UNUSED_0x115                    0x115 // Unused Flag
#define FLAG_UNUSED_0x116                    0x116 // Unused Flag
#define FLAG_UNUSED_0x117                    0x117 // Unused Flag
#define FLAG_UNUSED_0x118                    0x118 // Unused Flag
#define FLAG_ENABLE_PROF_BIRCH_MATCH_CALL    0x119
#define FLAG_UNUSED_0x11A                    0x11A // Unused Flag
#define FLAG_UNUSED_0x11B                    0x11B // Unused Flag
#define FLAG_UNUSED_0x11C                    0x11C // Unused Flag
#define FLAG_UNUSED_0x11D                    0x11D // Unused Flag
#define FLAG_UNUSED_0x11E                    0x11E // Unused Flag
#define FLAG_UNUSED_0x11F                    0x11F // Unused Flag
#define FLAG_UNUSED_0x120                    0x120 // Unused Flag
#define FLAG_UNUSED_0x121                    0x121 // Unused Flag
#define FLAG_UNUSED_0x122                    0x122 // Unused Flag
#define FLAG_RECEIVED_SS_TICKET              0x123
#define FLAG_UNUSED_0x124                    0x124 // Unused Flag
#define FLAG_UNUSED_0x125                      0x125 // Unused Flag
#define FLAG_UNUSED_0x126                    0x126 // Unused Flag
#define FLAG_UNUSED_0x127                    0x127 // Unused Flag
#define FLAG_PETALBURG_MART_EXPANDED_ITEMS   0x128
#define FLAG_UNUSED_0x129                    0x129 // Unused Flag
#define FLAG_UNUSED_0x12A                    0x12A // Unused Flag
#define FLAG_UNUSED_0x12B                    0x12B // Unused Flag
#define FLAG_UNUSED_0x12C                    0x12C // Unused Flag
#define FLAG_UNUSED_0x12D                    0x12D // Unused Flag
#define FLAG_UNUSED_0x12E                    0x12E // Unused Flag
#define FLAG_HAS_MATCH_CALL                  0x12F
#define FLAG_ADDED_MATCH_CALL_TO_POKENAV     0x130
#define FLAG_REGISTERED_STEVEN_POKENAV       0x131
#define FLAG_ENABLE_NORMAN_MATCH_CALL        0x132
#define FLAG_UNUSED_0x133                    0x133 // Unused Flag
#define FLAG_UNUSED_0x134                    0x134 // Unused Flag
#define FLAG_UNUSED_0x135                    0x135 // Unused Flag
#define FLAG_UNUSED_0x136                    0x136 // Unused Flag
#define FLAG_UNUSED_0x137                    0x137 // Unused Flag
#define FLAG_UNUSED_0x138                    0x138 // Unused Flag
#define FLAG_UNUSED_0x139                    0x139 // Unused Flag
#define FLAG_RECEIVED_AURORA_TICKET          0x13A
#define FLAG_RECEIVED_MYSTIC_TICKET          0x13B
#define FLAG_RECEIVED_OLD_SEA_MAP            0x13C
#define FLAG_WONDER_CARD_UNUSED_1            0x13D // These Wonder Card flags are referenced but never set
#define FLAG_WONDER_CARD_UNUSED_2            0x13E
#define FLAG_WONDER_CARD_UNUSED_3            0x13F
#define FLAG_WONDER_CARD_UNUSED_4            0x140
#define FLAG_WONDER_CARD_UNUSED_5            0x141
#define FLAG_WONDER_CARD_UNUSED_6            0x142
#define FLAG_WONDER_CARD_UNUSED_7            0x143
#define FLAG_WONDER_CARD_UNUSED_8            0x144
#define FLAG_WONDER_CARD_UNUSED_9            0x145
#define FLAG_WONDER_CARD_UNUSED_10           0x146
#define FLAG_WONDER_CARD_UNUSED_11           0x147
#define FLAG_WONDER_CARD_UNUSED_12           0x148
#define FLAG_WONDER_CARD_UNUSED_13           0x149
#define FLAG_WONDER_CARD_UNUSED_14           0x14A
#define FLAG_WONDER_CARD_UNUSED_15           0x14B
#define FLAG_WONDER_CARD_UNUSED_16           0x14C
#define FLAG_WONDER_CARD_UNUSED_17           0x14D
#define NUM_WONDER_CARD_FLAGS                (1 + FLAG_WONDER_CARD_UNUSED_17 - FLAG_RECEIVED_AURORA_TICKET)

#define FLAG_MIRAGE_TOWER_VISIBLE            0x14E
#define FLAG_UNUSED_0x14F                    0x14F // Unused Flag
#define FLAG_UNUSED_0x150                    0x150 // Unused Flag
#define FLAG_UNUSED_0x151                    0x151 // Unused Flag

#define FLAG_CHOSEN_MULTI_BATTLE_NPC_PARTNER 0x152

#define FLAG_MET_BATTLE_FRONTIER_BREEDER     0x153
#define FLAG_MET_BATTLE_FRONTIER_MANIAC      0x154
#define FLAG_UNUSED_0x155                    0x155 // Unused Flag
#define FLAG_UNUSED_0x156                    0x156 // Unused Flag
#define FLAG_MET_BATTLE_FRONTIER_GAMBLER     0x157
#define FLAG_ENABLE_MR_STONE_POKENAV         0x158
#define FLAG_NURSE_MENTIONS_GOLD_CARD        0x159
#define FLAG_MET_FRONTIER_BEAUTY_MOVE_TUTOR  0x15A
#define FLAG_MET_FRONTIER_SWIMMER_MOVE_TUTOR 0x15B

// Flags for whether a rematchable trainer has been registered in the player's Match Call.
// Most are used implicitly by adding their REMATCH_* id to TRAINER_REGISTERED_FLAGS_START.
// Some Match Call entries (like those for gym leaders, Wally, and all non-trainer NPCs like Prof. Birch)
// have their own separate flag that needs to be set to be enabled; see src/pokenav_match_call_data.c
#define TRAINER_REGISTERED_FLAGS_START       0x15C
#define FLAG_REGISTERED_ROSE                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_ROSE)
#define FLAG_REGISTERED_ANDRES               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ANDRES)
#define FLAG_REGISTERED_DUSTY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_DUSTY)
#define FLAG_REGISTERED_LOLA                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_LOLA)
#define FLAG_REGISTERED_RICKY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_RICKY)
#define FLAG_REGISTERED_LILA_AND_ROY         (TRAINER_REGISTERED_FLAGS_START + REMATCH_LILA_AND_ROY)
#define FLAG_REGISTERED_CRISTIN              (TRAINER_REGISTERED_FLAGS_START + REMATCH_CRISTIN)
#define FLAG_REGISTERED_BROOKE               (TRAINER_REGISTERED_FLAGS_START + REMATCH_BROOKE)
#define FLAG_REGISTERED_WILTON               (TRAINER_REGISTERED_FLAGS_START + REMATCH_WILTON)
#define FLAG_REGISTERED_VALERIE              (TRAINER_REGISTERED_FLAGS_START + REMATCH_VALERIE)
#define FLAG_REGISTERED_CINDY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_CINDY)
#define FLAG_REGISTERED_THALIA               (TRAINER_REGISTERED_FLAGS_START + REMATCH_THALIA)
#define FLAG_REGISTERED_JESSICA              (TRAINER_REGISTERED_FLAGS_START + REMATCH_JESSICA)
#define FLAG_REGISTERED_WINSTON              (TRAINER_REGISTERED_FLAGS_START + REMATCH_WINSTON)
#define FLAG_REGISTERED_STEVE                (TRAINER_REGISTERED_FLAGS_START + REMATCH_STEVE)
#define FLAG_REGISTERED_TONY                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_TONY)
#define FLAG_REGISTERED_NOB                  (TRAINER_REGISTERED_FLAGS_START + REMATCH_NOB)
#define FLAG_REGISTERED_KOJI                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_KOJI)
#define FLAG_REGISTERED_FERNANDO             (TRAINER_REGISTERED_FLAGS_START + REMATCH_FERNANDO)
#define FLAG_REGISTERED_DALTON               (TRAINER_REGISTERED_FLAGS_START + REMATCH_DALTON)
#define FLAG_REGISTERED_BERNIE               (TRAINER_REGISTERED_FLAGS_START + REMATCH_BERNIE)
#define FLAG_REGISTERED_ETHAN                (TRAINER_REGISTERED_FLAGS_START + REMATCH_ETHAN)
#define FLAG_REGISTERED_JOHN_AND_JAY         (TRAINER_REGISTERED_FLAGS_START + REMATCH_JOHN_AND_JAY)
#define FLAG_REGISTERED_JEFFREY              (TRAINER_REGISTERED_FLAGS_START + REMATCH_JEFFREY)
#define FLAG_REGISTERED_CAMERON              (TRAINER_REGISTERED_FLAGS_START + REMATCH_CAMERON)
#define FLAG_REGISTERED_JACKI                (TRAINER_REGISTERED_FLAGS_START + REMATCH_JACKI)
#define FLAG_REGISTERED_WALTER               (TRAINER_REGISTERED_FLAGS_START + REMATCH_WALTER)
#define FLAG_REGISTERED_KAREN                (TRAINER_REGISTERED_FLAGS_START + REMATCH_KAREN)
#define FLAG_REGISTERED_JERRY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_JERRY)
#define FLAG_REGISTERED_ANNA_AND_MEG         (TRAINER_REGISTERED_FLAGS_START + REMATCH_ANNA_AND_MEG)
#define FLAG_REGISTERED_ISABEL               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ISABEL)
#define FLAG_REGISTERED_MIGUEL               (TRAINER_REGISTERED_FLAGS_START + REMATCH_MIGUEL)
#define FLAG_REGISTERED_TIMOTHY              (TRAINER_REGISTERED_FLAGS_START + REMATCH_TIMOTHY)
#define FLAG_REGISTERED_SHELBY               (TRAINER_REGISTERED_FLAGS_START + REMATCH_SHELBY)
#define FLAG_REGISTERED_CALVIN               (TRAINER_REGISTERED_FLAGS_START + REMATCH_CALVIN)
#define FLAG_REGISTERED_ELLIOT               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ELLIOT)
#define FLAG_REGISTERED_ISAIAH               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ISAIAH)
#define FLAG_REGISTERED_MARIA                (TRAINER_REGISTERED_FLAGS_START + REMATCH_MARIA)
#define FLAG_REGISTERED_ABIGAIL              (TRAINER_REGISTERED_FLAGS_START + REMATCH_ABIGAIL)
#define FLAG_REGISTERED_DYLAN                (TRAINER_REGISTERED_FLAGS_START + REMATCH_DYLAN)
#define FLAG_REGISTERED_KATELYN              (TRAINER_REGISTERED_FLAGS_START + REMATCH_KATELYN)
#define FLAG_REGISTERED_BENJAMIN             (TRAINER_REGISTERED_FLAGS_START + REMATCH_BENJAMIN)
#define FLAG_REGISTERED_PABLO                (TRAINER_REGISTERED_FLAGS_START + REMATCH_PABLO)
#define FLAG_REGISTERED_NICOLAS              (TRAINER_REGISTERED_FLAGS_START + REMATCH_NICOLAS)
#define FLAG_REGISTERED_ROBERT               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ROBERT)
#define FLAG_REGISTERED_LAO                  (TRAINER_REGISTERED_FLAGS_START + REMATCH_LAO)
#define FLAG_REGISTERED_CYNDY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_CYNDY)
#define FLAG_REGISTERED_MADELINE             (TRAINER_REGISTERED_FLAGS_START + REMATCH_MADELINE)
#define FLAG_REGISTERED_JENNY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_JENNY)
#define FLAG_REGISTERED_DIANA                (TRAINER_REGISTERED_FLAGS_START + REMATCH_DIANA)
#define FLAG_REGISTERED_AMY_AND_LIV          (TRAINER_REGISTERED_FLAGS_START + REMATCH_AMY_AND_LIV)
#define FLAG_REGISTERED_ERNEST               (TRAINER_REGISTERED_FLAGS_START + REMATCH_ERNEST)
#define FLAG_REGISTERED_CORY                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_CORY)
#define FLAG_REGISTERED_EDWIN                (TRAINER_REGISTERED_FLAGS_START + REMATCH_EDWIN)
#define FLAG_REGISTERED_LYDIA                (TRAINER_REGISTERED_FLAGS_START + REMATCH_LYDIA)
#define FLAG_REGISTERED_ISAAC                (TRAINER_REGISTERED_FLAGS_START + REMATCH_ISAAC)
#define FLAG_REGISTERED_GABRIELLE            (TRAINER_REGISTERED_FLAGS_START + REMATCH_GABRIELLE)
#define FLAG_REGISTERED_CATHERINE            (TRAINER_REGISTERED_FLAGS_START + REMATCH_CATHERINE)
#define FLAG_REGISTERED_JACKSON              (TRAINER_REGISTERED_FLAGS_START + REMATCH_JACKSON)
#define FLAG_REGISTERED_HALEY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_HALEY)
#define FLAG_REGISTERED_JAMES                (TRAINER_REGISTERED_FLAGS_START + REMATCH_JAMES)
#define FLAG_REGISTERED_TRENT                (TRAINER_REGISTERED_FLAGS_START + REMATCH_TRENT)
#define FLAG_REGISTERED_SAWYER               (TRAINER_REGISTERED_FLAGS_START + REMATCH_SAWYER)
#define FLAG_REGISTERED_KIRA_AND_DAN         (TRAINER_REGISTERED_FLAGS_START + REMATCH_KIRA_AND_DAN)
#define FLAG_REGISTERED_WALLY                (TRAINER_REGISTERED_FLAGS_START + REMATCH_WALLY_VR)
#define FLAG_REGISTERED_ROXANNE              (TRAINER_REGISTERED_FLAGS_START + REMATCH_ROXANNE)
#define FLAG_REGISTERED_BRAWLY               (TRAINER_REGISTERED_FLAGS_START + REMATCH_BRAWLY)
#define FLAG_REGISTERED_WATTSON              (TRAINER_REGISTERED_FLAGS_START + REMATCH_WATTSON)
#define FLAG_REGISTERED_FLANNERY             (TRAINER_REGISTERED_FLAGS_START + REMATCH_FLANNERY)
#define FLAG_REGISTERED_NORMAN               (TRAINER_REGISTERED_FLAGS_START + REMATCH_NORMAN)
#define FLAG_REGISTERED_WINONA               (TRAINER_REGISTERED_FLAGS_START + REMATCH_WINONA)
#define FLAG_REGISTERED_TATE_AND_LIZA        (TRAINER_REGISTERED_FLAGS_START + REMATCH_TATE_AND_LIZA)
#define FLAG_REGISTERED_JUAN                 (TRAINER_REGISTERED_FLAGS_START + REMATCH_JUAN)
#define FLAG_REGISTERED_SIDNEY               (TRAINER_REGISTERED_FLAGS_START + REMATCH_SIDNEY)
#define FLAG_REGISTERED_PHOEBE               (TRAINER_REGISTERED_FLAGS_START + REMATCH_PHOEBE)
#define FLAG_REGISTERED_GLACIA               (TRAINER_REGISTERED_FLAGS_START + REMATCH_GLACIA)
#define FLAG_REGISTERED_DRAKE                (TRAINER_REGISTERED_FLAGS_START + REMATCH_DRAKE)
#define FLAG_REGISTERED_WALLACE              (TRAINER_REGISTERED_FLAGS_START + REMATCH_WALLACE)

#define FLAG_UNUSED_0x1AA                    0x1AA // Unused Flag
#define FLAG_UNUSED_0x1AB                    0x1AB // Unused Flag

#define FLAG_UNUSED_0x1AC                    0x1AC // Unused Flag
#define FLAG_BATTLED_DEOXYS                  0x1AD
#define FLAG_SHOWN_EON_TICKET                0x1AE
#define FLAG_SHOWN_AURORA_TICKET             0x1AF
#define FLAG_SHOWN_OLD_SEA_MAP               0x1B0
#define FLAG_MOVE_TUTOR_TAUGHT_SWAGGER       0x1B1
#define FLAG_MOVE_TUTOR_TAUGHT_ROLLOUT       0x1B2
#define FLAG_MOVE_TUTOR_TAUGHT_FURY_CUTTER   0x1B3
#define FLAG_MOVE_TUTOR_TAUGHT_MIMIC         0x1B4
#define FLAG_MOVE_TUTOR_TAUGHT_METRONOME     0x1B5
#define FLAG_MOVE_TUTOR_TAUGHT_SLEEP_TALK    0x1B6
#define FLAG_MOVE_TUTOR_TAUGHT_SUBSTITUTE    0x1B7
#define FLAG_MOVE_TUTOR_TAUGHT_DYNAMICPUNCH  0x1B8
#define FLAG_MOVE_TUTOR_TAUGHT_DOUBLE_EDGE   0x1B9
#define FLAG_MOVE_TUTOR_TAUGHT_EXPLOSION     0x1BA
#define FLAG_UNUSED_0x1BB                    0x1BB // Unused Flag
#define FLAG_UNUSED_0x1BC                    0x1BC // Unused Flag
#define FLAG_UNUSED_0x1BD                    0x1BD // Unused Flag
#define FLAG_DEFEATED_KYOGRE                 0x1BE
#define FLAG_DEFEATED_GROUDON                0x1BF
#define FLAG_UNUSED_0x1C0                    0x1C0 // Unused Flag
#define FLAG_UNUSED_0x1C1                    0x1C1 // Unused Flag
#define FLAG_UNUSED_0x1C2                    0x1C2 // Unused Flag
#define FLAG_UNUSED_0x1C3                    0x1C3 // Unused Flag
#define FLAG_UNUSED_0x1C4                      0x1C4 // Unused Flag
#define FLAG_UNUSED_0x1C5                      0x1C5 // Unused Flag
#define FLAG_DEFEATED_SUDOWOODO              0x1C6
#define FLAG_UNUSED_0x1C7                    0x1C7 // Unused Flag
#define FLAG_UNUSED_0x1C8                    0x1C8 // Unused Flag
#define FLAG_UNUSED_0x1C9                    0x1C9 // Unused Flag
#define FLAG_CAUGHT_MEW                      0x1CA
#define FLAG_UNUSED_0x1CB                          0x1CB // Unused Flag
#define FLAG_UNUSED_0x1CC                    0x1CC // Unused Flag
#define FLAG_UNUSED_0x1CD                    0x1CD // Unused Flag
#define FLAG_UNUSED_0x1CE                    0x1CE // Unused Flag
#define FLAG_UNUSED_0x1CF                    0x1CF // Unused Flag
#define FLAG_MET_SCOTT_ON_SS_TIDAL           0x1D0
#define FLAG_SCOTT_GIVES_BATTLE_POINTS       0x1D1
#define FLAG_COLLECTED_ALL_GOLD_SYMBOLS      0x1D2
#define FLAG_ENABLE_ROXANNE_MATCH_CALL       0x1D3
#define FLAG_ENABLE_BRAWLY_MATCH_CALL        0x1D4
#define FLAG_ENABLE_WATTSON_MATCH_CALL       0x1D5
#define FLAG_ENABLE_FLANNERY_MATCH_CALL      0x1D6
#define FLAG_ENABLE_WINONA_MATCH_CALL        0x1D7
#define FLAG_ENABLE_TATE_AND_LIZA_MATCH_CALL 0x1D8
#define FLAG_ENABLE_JUAN_MATCH_CALL          0x1D9

#define FLAG_UNUSED_0x1DA                    0x1DA // Unused Flag

#define FLAG_SHOWN_MYSTIC_TICKET             0x1DB
#define FLAG_UNUSED_0x1DC                    0x1DC // Unused Flag
#define FLAG_UNUSED_0x1DD                    0x1DD // Unused Flag

#define FLAG_UNUSED_0x1DE                    0x1DE // Unused Flag
#define FLAG_UNUSED_0x1DF                    0x1DF // Unused Flag
#define FLAG_UNUSED_0x1E0                    0x1E0 // Unused Flag
#define FLAG_UNUSED_0x1E1                    0x1E1 // Unused Flag
#define FLAG_UNUSED_0x1E2                    0x1E2 // Unused Flag
#define FLAG_UNUSED_0x1E3                    0x1E3 // Unused Flag

// Mystery Gift Flags (Unknown)
#define FLAG_MYSTERY_GIFT_DONE               0x1E4
#define FLAG_MYSTERY_GIFT_1                  0x1E5
#define FLAG_MYSTERY_GIFT_2                  0x1E6
#define FLAG_MYSTERY_GIFT_3                  0x1E7
#define FLAG_MYSTERY_GIFT_4                  0x1E8
#define FLAG_MYSTERY_GIFT_5                  0x1E9
#define FLAG_MYSTERY_GIFT_6                  0x1EA
#define FLAG_MYSTERY_GIFT_7                  0x1EB
#define FLAG_MYSTERY_GIFT_8                  0x1EC
#define FLAG_MYSTERY_GIFT_9                  0x1ED
#define FLAG_MYSTERY_GIFT_10                 0x1EE
#define FLAG_MYSTERY_GIFT_11                 0x1EF
#define FLAG_MYSTERY_GIFT_12                 0x1F0
#define FLAG_MYSTERY_GIFT_13                 0x1F1
#define FLAG_MYSTERY_GIFT_14                 0x1F2
#define FLAG_MYSTERY_GIFT_15                 0x1F3

// Hidden Items
#define FLAG_HIDDEN_ITEMS_START                                                         0x1F4
#define FLAG_ICHOR_HIDDEN_KRONION_PRETTY_FEATHER             0x1F4 // Ichor: hidden item: Kronion Hill Pretty Feather, on the tip of the point
#define FLAG_HIDDEN_ITEM_TRICK_HOUSE_NUGGET                  (FLAG_HIDDEN_ITEMS_START + 0x01)
#define FLAG_ICHOR_HIDDEN_ELAIA_X_SPEED                      0x1F6 // Ichor: hidden item: Elaia X Speed, in the corner past the race start
#define FLAG_UNUSED_0x1F7                                    0x1F7 // Unused Flag
#define FLAG_UNUSED_0x1F8                                    0x1F8 // Unused Flag
#define FLAG_UNUSED_0x1F9                                    0x1F9 // Unused Flag
#define FLAG_UNUSED_0x1FA                                    0x1FA // Unused Flag
#define FLAG_UNUSED_0x1FB                                    0x1FB // Unused Flag
#define FLAG_UNUSED_0x1FC                                    0x1FC // Unused Flag
#define FLAG_UNUSED_0x1FD                                    0x1FD // Unused Flag
#define FLAG_UNUSED_0x1FE                                    0x1FE // Unused Flag
#define FLAG_UNUSED_0x1FF                                    0x1FF // Unused Flag
#define FLAG_UNUSED_0x200                                    0x200 // Unused Flag
#define FLAG_UNUSED_0x201                                    0x201 // Unused Flag
#define FLAG_UNUSED_0x202                                    0x202 // Unused Flag
#define FLAG_UNUSED_0x203                                    0x203 // Unused Flag
#define FLAG_UNUSED_0x204                                    0x204 // Unused Flag
#define FLAG_UNUSED_0x205                                    0x205 // Unused Flag
#define FLAG_UNUSED_0x206                                    0x206 // Unused Flag
#define FLAG_UNUSED_0x207                                    0x207 // Unused Flag
#define FLAG_UNUSED_0x208                                    0x208 // Unused Flag
#define FLAG_UNUSED_0x209                                    0x209 // Unused Flag
#define FLAG_UNUSED_0x20A                                    0x20A // Unused Flag
#define FLAG_UNUSED_0x20B                                    0x20B // Unused Flag
#define FLAG_UNUSED_0x20C                                    0x20C // Unused Flag
#define FLAG_UNUSED_0x20D                                    0x20D // Unused Flag
#define FLAG_UNUSED_0x20E                                    0x20E // Unused Flag
#define FLAG_UNUSED_0x20F                                    0x20F // Unused Flag
#define FLAG_UNUSED_0x210                                    0x210 // Unused Flag
#define FLAG_UNUSED_0x211                                    0x211 // Unused Flag
#define FLAG_UNUSED_0x212                                    0x212 // Unused Flag
#define FLAG_HIDDEN_ITEM_ABANDONED_SHIP_RM_1_KEY             (FLAG_HIDDEN_ITEMS_START + 0x1F)
#define FLAG_HIDDEN_ITEM_ABANDONED_SHIP_RM_2_KEY             (FLAG_HIDDEN_ITEMS_START + 0x20)
#define FLAG_HIDDEN_ITEM_ABANDONED_SHIP_RM_4_KEY             (FLAG_HIDDEN_ITEMS_START + 0x21)
#define FLAG_HIDDEN_ITEM_ABANDONED_SHIP_RM_6_KEY             (FLAG_HIDDEN_ITEMS_START + 0x22)
#define FLAG_UNUSED_0x217                                    0x217 // Unused Flag
#define FLAG_UNUSED_0x218                                    0x218 // Unused Flag
#define FLAG_UNUSED_0x219                                    0x219 // Unused Flag
#define FLAG_UNUSED_0x21A                                    0x21A // Unused Flag
#define FLAG_UNUSED_0x21B                                    0x21B // Unused Flag
#define FLAG_UNUSED_0x21C                                    0x21C // Unused Flag
#define FLAG_UNUSED_0x21D                                    0x21D // Unused Flag
#define FLAG_UNUSED_0x21E                                    0x21E // Unused Flag
#define FLAG_UNUSED_0x21F                                    0x21F // Unused Flag
#define FLAG_UNUSED_0x220                                    0x220 // Unused Flag
#define FLAG_UNUSED_0x221                                    0x221 // Unused Flag
#define FLAG_UNUSED_0x222                                    0x222 // Unused Flag
#define FLAG_UNUSED_0x223                                    0x223 // Unused Flag
#define FLAG_UNUSED_0x224                                    0x224 // Unused Flag
#define FLAG_UNUSED_0x225                                    0x225 // Unused Flag
#define FLAG_UNUSED_0x226                                    0x226 // Unused Flag
#define FLAG_UNUSED_0x227                                    0x227 // Unused Flag
#define FLAG_UNUSED_0x228                                    0x228 // Unused Flag
#define FLAG_UNUSED_0x229                                    0x229 // Unused Flag
#define FLAG_UNUSED_0x22A                                    0x22A // Unused Flag
#define FLAG_UNUSED_0x22B                                    0x22B // Unused Flag
#define FLAG_UNUSED_0x22C                                    0x22C // Unused Flag
#define FLAG_UNUSED_0x22D                                    0x22D // Unused Flag
#define FLAG_UNUSED_0x22E                                    0x22E // Unused Flag
#define FLAG_UNUSED_0x22F                                    0x22F // Unused Flag
#define FLAG_UNUSED_0x230                                    0x230 // Unused Flag
#define FLAG_UNUSED_0x231                                    0x231 // Unused Flag
#define FLAG_UNUSED_0x232                                    0x232 // Unused Flag
#define FLAG_UNUSED_0x233                                    0x233 // Unused Flag
#define FLAG_UNUSED_0x234                                    0x234 // Unused Flag
#define FLAG_UNUSED_0x235                                    0x235 // Unused Flag
#define FLAG_UNUSED_0x236                                    0x236 // Unused Flag
#define FLAG_UNUSED_0x237                                    0x237 // Unused Flag
#define FLAG_UNUSED_0x238                                    0x238 // Unused Flag
#define FLAG_UNUSED_0x239                                    0x239 // Unused Flag
#define FLAG_UNUSED_0x23A                                    0x23A // Unused Flag
#define FLAG_UNUSED_0x23B                                    0x23B // Unused Flag
#define FLAG_UNUSED_0x23C                                    0x23C // Unused Flag
#define FLAG_UNUSED_0x23D                                    0x23D // Unused Flag
#define FLAG_UNUSED_0x23E                                    0x23E // Unused Flag
#define FLAG_UNUSED_0x23F                                    0x23F // Unused Flag
#define FLAG_UNUSED_0x240                                    0x240 // Unused Flag
#define FLAG_UNUSED_0x241                                    0x241 // Unused Flag
#define FLAG_UNUSED_0x242                                    0x242 // Unused Flag
#define FLAG_UNUSED_0x243                                    0x243 // Unused Flag
#define FLAG_UNUSED_0x244                                    0x244 // Unused Flag
#define FLAG_UNUSED_0x245                                    0x245 // Unused Flag
#define FLAG_UNUSED_0x246                                    0x246 // Unused Flag
#define FLAG_UNUSED_0x247                                    0x247 // Unused Flag
#define FLAG_UNUSED_0x248                                    0x248 // Unused Flag
#define FLAG_UNUSED_0x249                                    0x249 // Unused Flag
#define FLAG_UNUSED_0x24A                                    0x24A // Unused Flag
#define FLAG_UNUSED_0x24B                                    0x24B // Unused Flag
#define FLAG_UNUSED_0x24C                                    0x24C // Unused Flag
#define FLAG_UNUSED_0x24D                                    0x24D // Unused Flag
#define FLAG_UNUSED_0x24E                                    0x24E // Unused Flag
#define FLAG_UNUSED_0x24F                                    0x24F // Unused Flag
#define FLAG_UNUSED_0x250                                    0x250 // Unused Flag
#define FLAG_UNUSED_0x251                                    0x251 // Unused Flag
#define FLAG_UNUSED_0x252                                    0x252 // Unused Flag
#define FLAG_UNUSED_0x253                                    0x253 // Unused Flag
#define FLAG_HIDDEN_ITEM_ROUTE_116_BLACK_GLASSES             (FLAG_HIDDEN_ITEMS_START + 0x60)
#define FLAG_UNUSED_0x255                                    0x255 // Unused Flag
#define FLAG_UNUSED_0x256                                    0x256 // Unused Flag
#define FLAG_UNUSED_0x257                                    0x257 // Unused Flag
#define FLAG_UNUSED_0x258                                    0x258 // Unused Flag
#define FLAG_UNUSED_0x259                                    0x259 // Unused Flag
#define FLAG_UNUSED_0x25A                                    0x25A // Unused Flag
#define FLAG_UNUSED_0x25B                                    0x25B // Unused Flag
#define FLAG_UNUSED_0x25C                                    0x25C // Unused Flag
#define FLAG_UNUSED_0x25D                                    0x25D // Unused Flag
#define FLAG_UNUSED_0x25E                                    0x25E // Unused Flag
#define FLAG_UNUSED_0x25F                                    0x25F // Unused Flag
#define FLAG_UNUSED_0x260                                    0x260 // Unused Flag
#define FLAG_UNUSED_0x261                                    0x261 // Unused Flag
#define FLAG_UNUSED_0x262                                    0x262 // Unused Flag
#define FLAG_UNUSED_0x263                                    0x263 // Unused Flag

#define FLAG_ICHOR_HIDDEN_ROUTE1_ORAN_BERRY 0x264 // Ichor: hidden item: Route 1 Oran Berry
#define FLAG_ICHOR_HIDDEN_ROUTE1_REPEL 0x265 // Ichor: hidden item: Route 1 Repel
#define FLAG_ICHOR_HIDDEN_ROUTE1_ANTIDOTE 0x266 // Ichor: hidden item: Route 1 Antidote
#define FLAG_ICHOR_HIDDEN_KRONION_HARD_STONE 0x267 // Ichor: hidden item: Kronion Hill Hard Stone
#define FLAG_ICHOR_HIDDEN_KRONION_STARDUST 0x268 // Ichor: hidden item: Kronion Hill Stardust
#define FLAG_ICHOR_HALIA_SECOND_LOOK 0x269 // Ichor: Phase 2 beat 9A: Halia's second look under the canopy
#define FLAG_ICHOR_HIDE_MOM_HOME 0x26A // Ichor: hide Mom at home (she has gone down to Akti's quay)
#define FLAG_ICHOR_HIDE_MOM_AKTI 0x26B // Ichor: hide Mom on Akti's quay (set at new game; shown from beat 9A to the sailing)
#define FLAG_ICHOR_HIDE_KLEON_AKTI_DOOR 0x26C // Ichor: hide beat 9B's Kleon by the Temple of Hestia (set at new game)
#define FLAG_ICHOR_WINDS_TURNED 0x26D // Ichor: beat 9B: the halcyon days are over and the wind is back
#define FLAG_ICHOR_MOM_HARBOR 0x26E // Ichor: beat 9B: Mom gave the bread and honey on the quay
#define FLAG_ICHOR_BOARDED_EUPLOIA 0x26F // Ichor: beat 9B: boarded the Euploia for the crossing
#define FLAG_ICHOR_BATTLED_ALETHEA_DECK 0x270 // Ichor: beat 10: Alethea's practice battle on deck offered and fought
#define FLAG_ICHOR_SAVED_HALCYON_NEST 0x271 // Ichor: beat 10: kept the snatchers off the last halcyon nest
#define FLAG_ICHOR_GOT_HALCYLING 0x272 // Ichor: beat 10: took the halcyon chick (Halcyling)
#define FLAG_HIDDEN_ITEM_ICHOR_ELAIA_HONEY 0x273 // Ichor: hidden Honey at Melitta's beehives (hidden-item range)
#define FLAG_ICHOR_HIDE_HALCYON_NEST 0x274 // Ichor: hide the floating halcyon nest at the Euploia's bow
#define FLAG_ICHOR_HIDE_DECK_HARPECK 0x275 // Ichor: hide the snatchers diving at the halcyon nest
#define FLAG_ICHOR_ARRIVED_AEGINA 0x276 // Ichor: beat 10B: stepped onto Aegina's quay on the voyage night
#define FLAG_ICHOR_VISITED_AEGINA 0x277 // Ichor: Aegina Town visited (fly target)
#define FLAG_ICHOR_AEGINA_NIGHT 0x278 // Ichor: beat 10B: the night at Endeis's inn
#define FLAG_ICHOR_CROSSING_DONE 0x279 // Ichor: beat 10C: the Euploia made Emporion; the ferry runs
#define FLAG_ICHOR_FERRY_TO_AEGINA 0x27A // Ichor: the Euploia's Aigina stop is open, and so is Aigina Town's north gate (world-act2 sets it, Act II beat 46)
#define FLAG_ICHOR_FERRY_TO_EMPORION 0x27B // Ichor: the Euploia ferry is bound for Emporion (clear: Akti)
#define FLAG_ICHOR_TRADED_CHELONET 0x27C // Ichor: Aegina: traded Pheidon a Karkipool for his Chelonet, Stater
#define FLAG_ICHOR_GOT_BLACK_BELT 0x27D // Ichor: Aegina: Aiakides gave his Black Belt for a look at an Ergant
#define FLAG_ICHOR_ITEM_DECK_SUPER_POTION 0x27E // Ichor: item ball: Super Potion among the Euploia's bow cargo
#define FLAG_ICHOR_HIDDEN_DECK_HEART_SCALE 0x27F // Ichor: hidden item: Heart Scale in a coil of rope at the Euploia's stern
#define FLAG_ICHOR_ITEM_HOLD_POTION 0x280 // Ichor: item ball: Potion under the Euploia's bottom bench
#define FLAG_ICHOR_HIDDEN_AEGINA_BIG_PEARL 0x281 // Ichor: hidden item: Big Pearl at the end of Aegina's mole
#define FLAG_ICHOR_HIDDEN_AEGINA_STARDUST 0x282 // Ichor: hidden item: Stardust at the foot of Kolona's column
#define FLAG_ICHOR_HERM_AEGINA 0x283 // Ichor: anointed the great herm on the Aphaia Road (until the engine's herm range)
#define FLAG_ICHOR_ITEM_APHAIA_SILVER_POWDER 0x284 // Ichor: item ball: Silver Powder on the Aphaia Road's ant hills
#define FLAG_ICHOR_ITEM_APHAIA_SUPER_POTION 0x285 // Ichor: item ball: Super Potion at the Aphaia Road's Oros fork
#define FLAG_ICHOR_ITEM_APHAIA_PRETTY_FEATHER 0x286 // Ichor: item ball: two Pretty Feathers on the Temple of Aphaia's steps
#define FLAG_ICHOR_ITEM_OROS_WINE 0x287 // Ichor: item ball: Wine by Zeus's altar on Mount Oros
#define FLAG_ICHOR_HIDE_AEGINA_CAST 0x288 // Ichor: hide Kleon and Alethea on Aegina's quay once the voyage party has split up
#define FLAG_ICHOR_NO_RUNNING 0x289 // Ichor: set to make a scripted wild battle unescapable (WE_FLAG_NO_RUNNING)
#define FLAG_ICHOR_HIDDEN_EMPORION_BRONZE_OBOL 0x28A // Ichor: hidden item: Bronze Obol in a crack in the harbor wall
#define FLAG_ICHOR_HIDDEN_EMPORION_HEART_SCALE 0x28B // Ichor: hidden item: Heart Scale on the quay steps
#define FLAG_ICHOR_HIDDEN_EMPORION_HONEY 0x28C // Ichor: hidden item: Honey under Kydon's awning
#define FLAG_ICHOR_HIDDEN_EMPORION_STARDUST 0x28D // Ichor: hidden item: Stardust at the top of Acrocorinth's stair
#define FLAG_UNUSED_0x28E  0x28E // Unused Flag
#define FLAG_UNUSED_0x28F  0x28F // Unused Flag
#define FLAG_UNUSED_0x290  0x290 // Unused Flag
#define FLAG_UNUSED_0x291  0x291 // Unused Flag
#define FLAG_UNUSED_0x292  0x292 // Unused Flag
#define FLAG_UNUSED_0x293  0x293 // Unused Flag
#define FLAG_UNUSED_0x294  0x294 // Unused Flag
#define FLAG_UNUSED_0x295  0x295 // Unused Flag
#define FLAG_UNUSED_0x296  0x296 // Unused Flag
#define FLAG_UNUSED_0x297  0x297 // Unused Flag
#define FLAG_UNUSED_0x298  0x298 // Unused Flag
#define FLAG_UNUSED_0x299  0x299 // Unused Flag
#define FLAG_UNUSED_0x29A  0x29A // Unused Flag
#define FLAG_UNUSED_0x29B  0x29B // Unused Flag
#define FLAG_UNUSED_0x29C  0x29C // Unused Flag
#define FLAG_UNUSED_0x29D  0x29D // Unused Flag
#define FLAG_UNUSED_0x29E  0x29E // Unused Flag
#define FLAG_UNUSED_0x29F  0x29F // Unused Flag
#define FLAG_ICHOR_HIDDEN_ELEUSA_HONEY 0x2A0 // Ichor: Eleusa: hidden Honey by the beehives
#define FLAG_ICHOR_HIDDEN_ELEUSA_POMEG_BERRY 0x2A1 // Ichor: Eleusa: hidden Pomeg Berry under the well's tree
#define FLAG_ICHOR_HIDDEN_ELEUSA_BRONZE_OBOL 0x2A2 // Ichor: Eleusa: hidden Bronze Obol in the Maiden's Well
#define FLAG_ICHOR_HIDDEN_ROUTE4_ETHER 0x2A3 // Ichor: Route 4: hidden Ether in the kiln's ash
#define FLAG_ICHOR_HIDDEN_ROUTE4_ORAN_BERRY 0x2A4 // Ichor: Route 4: hidden Oran Berry by the terrace milestone
#define FLAG_ICHOR_HIDDEN_ROUTE4_STARDUST 0x2A5 // Ichor: Route 4: hidden Stardust by the procession's cookfire
#define FLAG_ICHOR_HIDDEN_ROUTE4_HARD_STONE 0x2A6 // Ichor: Route 4: hidden Hard Stone in the scree under the slide
#define FLAG_UNUSED_0x2A7  0x2A7 // Unused Flag
#define FLAG_UNUSED_0x2A8  0x2A8 // Unused Flag
#define FLAG_UNUSED_0x2A9  0x2A9 // Unused Flag
#define FLAG_UNUSED_0x2AA  0x2AA // Unused Flag
#define FLAG_UNUSED_0x2AB  0x2AB // Unused Flag
#define FLAG_UNUSED_0x2AC  0x2AC // Unused Flag
#define FLAG_UNUSED_0x2AD  0x2AD // Unused Flag
#define FLAG_UNUSED_0x2AE  0x2AE // Unused Flag
#define FLAG_UNUSED_0x2AF  0x2AF // Unused Flag
#define FLAG_ICHOR_HIDDEN_HOLLOW_ESCAPE_ROPE 0x2B0 // Ichor: Hecate's Hollow: hidden Escape Rope on fork 1's loop
#define FLAG_ICHOR_HIDDEN_HOLLOW_HONEY 0x2B1 // Ichor: Hecate's Hollow: hidden Honey in Hecate's supper niche
#define FLAG_ICHOR_HIDDEN_HOLLOW_STARDUST 0x2B2 // Ichor: Hecate's Hollow: hidden Stardust on fork 3's loop
#define FLAG_ICHOR_HIDDEN_HOLLOW_HARD_STONE 0x2B3 // Ichor: Hecate's Hollow: hidden Hard Stone in the shortcut tunnel
#define FLAG_UNUSED_0x2B4  0x2B4 // Unused Flag
#define FLAG_UNUSED_0x2B5  0x2B5 // Unused Flag
#define FLAG_UNUSED_0x2B6  0x2B6 // Unused Flag
#define FLAG_UNUSED_0x2B7  0x2B7 // Unused Flag
#define FLAG_ICHOR_HIDDEN_ROUTE5_HONEY 0x2B8 // Ichor: Route 5: Honey under a beehive in the thyme meadow
#define FLAG_ICHOR_HIDDEN_ROUTE5_PRETTY_FEATHER 0x2B9 // Ichor: Route 5: a Pretty Feather in a niche of Aphrodite's shrine
#define FLAG_ICHOR_HIDDEN_ROUTE5_HEART_SCALE 0x2BA // Ichor: Route 5: a Heart Scale at the tip of the shore point
#define FLAG_ICHOR_HIDDEN_ROUTE5_ORAN_BERRY 0x2BB // Ichor: Route 5: an Oran Berry in the inn's yard

// Event Flags
#define FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG                      0x2BC
#define FLAG_HIDE_APPRENTICE                                        0x2BD
#define FLAG_HIDE_POKEMON_CENTER_2F_MYSTERY_GIFT_MAN                0x2BE
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_1               0x2C7
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_2               0x2C8
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_3               0x2C9
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_4               0x2CA
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_5               0x2CB
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_6               0x2CC
#define FLAG_UNUSED_0x2CD                                           0x2CD // Unused Flag
#define FLAG_HIDE_MEW                                               0x2CE
#define FLAG_UNUSED_0x2CF                                           0x2CF // Unused Flag
#define FLAG_HIDE_ROUTE_101_BIRCH_ZIGZAGOON_BATTLE                  0x2D0
#define FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_BIRCH                  0x2D1
#define FLAG_ICHOR_HIDDEN_APHAIA_BIG_PEARL                          0x2D2 // Ichor: Aphaia Road: hidden Big Pearl at the west end of the bay's beach
#define FLAG_ICHOR_HIDDEN_APHAIA_REVIVE                             0x2D3 // Ichor: Aphaia Road: hidden Revive in the orchard's west corner
#define FLAG_ICHOR_HIDDEN_APHAIA_NUGGET                             0x2D4 // Ichor: Aphaia Road: hidden Nugget behind the umbrella pine on the meadow terrace
#define FLAG_ICHOR_HIDDEN_APHAIA_PRETTY_FEATHER                     0x2D5 // Ichor: Aphaia Road: hidden Pretty Feather past the horos, at the cliff edge
#define FLAG_ICHOR_HIDDEN_APHAIA_MOON_STONE                         0x2D6 // Ichor: Temple of Aphaia: hidden Moon Stone in the cypress nook west of the way
#define FLAG_ICHOR_HIDDEN_APHAIA_ETHER                              0x2D7 // Ichor: Temple of Aphaia: hidden Ether in the old foundations' far corner
#define FLAG_ICHOR_HIDDEN_OROS_STAR_PIECE                           0x2D8 // Ichor: Mount Oros: hidden Star Piece behind Zeus's altar

#define FLAG_ICHOR_HIDDEN_OROS_THUNDER_STONE                        0x2D9 // Ichor: Mount Oros: hidden Thunder Stone on the summit's east lip

#define FLAG_HIDE_LILYCOVE_FAN_CLUB_INTERVIEWER                     0x2DA
#define FLAG_ICHOR_HIDDEN_ELEUSA_GRANARY_REVIVE                     0x2DB // Ichor: Eleusa: the Revive under Sitokles's bed (hidden item)
#define FLAG_UNUSED_0x2DC                                           0x2DC // Unused Flag
#define FLAG_UNUSED_0x2DD                                           0x2DD // Unused Flag
#define FLAG_UNUSED_0x2DE                                           0x2DE // Unused Flag
#define FLAG_UNUSED_0x2DF                                           0x2DF // Unused Flag
#define FLAG_UNUSED_0x2E0                                           0x2E0 // Unused Flag
#define FLAG_UNUSED_0x2E1                                           0x2E1 // Unused Flag
#define FLAG_HIDE_ROUTE_104_MR_BRINEY                               0x2E2
#define FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY                           0x2E3
#define FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN                            0x2E4
#define FLAG_HIDE_ROUTE_109_MR_BRINEY                               0x2E5
#define FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT                          0x2E6
#define FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN                       0x2E7
#define FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT                          0x2E8
#define FLAG_UNUSED_0x2E9                                           0x2E9 // Unused Flag
#define FLAG_UNUSED_0x2EA                                           0x2EA // Unused Flag
#define FLAG_UNUSED_0x2EB                                           0x2EB // Unused Flag
#define FLAG_UNUSED_0x2EC                                           0x2EC // Unused Flag
#define FLAG_UNUSED_0x2ED                                           0x2ED // Unused Flag
#define FLAG_UNUSED_0x2EE                                           0x2EE // Unused Flag
#define FLAG_UNUSED_0x2EF                                           0x2EF // Unused Flag
#define FLAG_UNUSED_0x2F0                                           0x2F0 // Unused Flag
#define FLAG_UNUSED_0x2F1                                           0x2F1 // Unused Flag
#define FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_1          0x2F2
#define FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_2          0x2F3
#define FLAG_ICHOR_HIDDEN_SANCTUM_B1F_MIRACLE_SEED                  0x2F4 // Ichor: the sanctum, B1F: a Miracle Seed in the sealed granary's dust
#define FLAG_ICHOR_HIDDEN_SANCTUM_B2F_ETHER                         0x2F5 // Ichor: the sanctum, B2F: an Ether in the spring basin's overflow
#define FLAG_ICHOR_HIDDEN_SANCTUM_B3F_BRONZE_OBOL                   0x2F6 // Ichor: the sanctum, B3F: a Bronze Obol in the oldest granary's dust
#define FLAG_UNUSED_0x2F7                                           0x2F7 // Unused Flag
#define FLAG_UNUSED_0x2F8                                           0x2F8 // Unused Flag
#define FLAG_UNUSED_0x2F9                                           0x2F9 // Unused Flag
#define FLAG_UNUSED_0x2FA                                           0x2FA // Unused Flag
#define FLAG_HIDE_DEOXYS                                            0x2FB
#define FLAG_UNUSED_0x2FC                                           0x2FC // Unused Flag
#define FLAG_UNUSED_0x2FD                                           0x2FD // Unused Flag
#define FLAG_UNUSED_0x2FE                                           0x2FE // Unused Flag
#define FLAG_UNUSED_0x2FF                                           0x2FF // Unused Flag
#define FLAG_UNUSED_0x300                                           0x300 // Unused Flag
#define FLAG_UNUSED_0x301                                           0x301 // Unused Flag
#define FLAG_UNUSED_0x302                                           0x302 // Unused Flag
#define FLAG_UNUSED_0x303                                           0x303 // Unused Flag
#define FLAG_UNUSED_0x304                                           0x304 // Unused Flag
#define FLAG_UNUSED_0x305                                           0x305 // Unused Flag
#define FLAG_UNUSED_0x306                                           0x306 // Unused Flag
#define FLAG_UNUSED_0x307                                           0x307 // Unused Flag
#define FLAG_UNUSED_0x308                                           0x308 // Unused Flag
#define FLAG_UNUSED_0x309                                           0x309 // Unused Flag
#define FLAG_UNUSED_0x30A                                           0x30A // Unused Flag
#define FLAG_UNUSED_0x30B                                           0x30B // Unused Flag
#define FLAG_UNUSED_0x30C                                           0x30C // Unused Flag
#define FLAG_HIDE_PETALBURG_GYM_GREETER                             0x30D
#define FLAG_UNUSED_0x30E                                           0x30E // Unused Flag
#define FLAG_UNUSED_0x30F                                           0x30F // Unused Flag
#define FLAG_UNUSED_0x310                                           0x310 // Unused Flag
#define FLAG_UNUSED_0x311                                           0x311 // Unused Flag
#define FLAG_UNUSED_0x312                                           0x312 // Unused Flag
#define FLAG_UNUSED_0x313                                           0x313 // Unused Flag
#define FLAG_UNUSED_0x314                                           0x314 // Unused Flag
#define FLAG_HIDE_FANCLUB_OLD_LADY                                  0x315
#define FLAG_HIDE_FANCLUB_BOY                                       0x316
#define FLAG_HIDE_FANCLUB_LITTLE_BOY                                0x317
#define FLAG_HIDE_FANCLUB_LADY                                      0x318
#define FLAG_UNUSED_0x319                                           0x319 // Unused Flag
#define FLAG_UNUSED_0x31A                                           0x31A // Unused Flag
#define FLAG_UNUSED_0x31B                                           0x31B // Unused Flag
#define FLAG_UNUSED_0x31C                                           0x31C // Unused Flag
#define FLAG_UNUSED_0x31D                                           0x31D // Unused Flag
#define FLAG_UNUSED_0x31E                                           0x31E // Unused Flag
#define FLAG_UNUSED_0x31F                                           0x31F // Unused Flag
#define FLAG_UNUSED_0x320                                           0x320 // Unused Flag
#define FLAG_UNUSED_0x321                                           0x321 // Unused Flag
#define FLAG_HIDE_LILYCOVE_CONTEST_HALL_REPORTER                    0x322
#define FLAG_UNUSED_0x323                                           0x323 // Unused Flag
#define FLAG_HIDE_MAUVILLE_CITY_WALLY                               0x324
#define FLAG_UNUSED_0x325                                           0x325 // Unused Flag
#define FLAG_UNUSED_0x326                                           0x326 // Unused Flag
#define FLAG_UNUSED_0x327                                           0x327 // Unused Flag
#define FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDAS_BOYFRIEND     0x328
#define FLAG_UNUSED_0x329                                           0x329 // Unused Flag
#define FLAG_UNUSED_0x32A                                           0x32A // Unused Flag
#define FLAG_UNUSED_0x32B                                           0x32B // Unused Flag
#define FLAG_UNUSED_0x32C                                           0x32C // Unused Flag
#define FLAG_UNUSED_0x32D                                           0x32D // Unused Flag
#define FLAG_UNUSED_0x32E                                           0x32E // Unused Flag
#define FLAG_UNUSED_0x32F                                           0x32F // Unused Flag
#define FLAG_UNUSED_0x330                                           0x330 // Unused Flag
#define FLAG_UNUSED_0x331                                           0x331 // Unused Flag
#define FLAG_UNUSED_0x332                                           0x332 // Unused Flag
#define FLAG_UNUSED_0x333                                           0x333 // Unused Flag
#define FLAG_UNUSED_0x334                                           0x334 // Unused Flag
#define FLAG_UNUSED_0x335                                           0x335 // Unused Flag
#define FLAG_UNUSED_0x336                                           0x336 // Unused Flag
#define FLAG_UNUSED_0x337                                           0x337 // Unused Flag
#define FLAG_UNUSED_0x338                                           0x338 // Unused Flag
#define FLAG_UNUSED_0x339                                           0x339 // Unused Flag
#define FLAG_UNUSED_0x33A                                           0x33A // Unused Flag
#define FLAG_UNUSED_0x33B                                           0x33B // Unused Flag
#define FLAG_UNUSED_0x33C                                           0x33C // Unused Flag
#define FLAG_UNUSED_0x33D                                           0x33D // Unused Flag
#define FLAG_UNUSED_0x33E                                           0x33E // Unused Flag
#define FLAG_UNUSED_0x33F                                           0x33F // Unused Flag
#define FLAG_HIDE_LILYCOVE_CONTEST_HALL_BLEND_MASTER                0x340
#define FLAG_UNUSED_0x341                                           0x341 // Unused Flag
#define FLAG_UNUSED_0x342                                           0x342 // Unused Flag
#define FLAG_UNUSED_0x343                                           0x343 // Unused Flag
#define FLAG_HIDE_BATTLE_FRONTIER_RECEPTION_GATE_SCOTT              0x344
#define FLAG_UNUSED_0x345                                           0x345 // Unused Flag
#define FLAG_UNUSED_0x346                                           0x346 // Unused Flag
#define FLAG_UNUSED_0x347                                           0x347 // Unused Flag
#define FLAG_UNUSED_0x348                                           0x348 // Unused Flag
#define FLAG_UNUSED_0x349                                           0x349 // Unused Flag
#define FLAG_HIDE_BATTLE_FRONTIER_SUDOWOODO                         0x34A
#define FLAG_UNUSED_0x34B                                           0x34B // Unused Flag
#define FLAG_UNUSED_0x34C                                           0x34C // Unused Flag
#define FLAG_UNUSED_0x34D                                           0x34D // Unused Flag
#define FLAG_UNUSED_0x34E                                           0x34E // Unused Flag
#define FLAG_UNUSED_0x34F                                           0x34F // Unused Flag
#define FLAG_UNUSED_0x350                                           0x350 // Unused Flag
#define FLAG_UNUSED_0x351                                           0x351 // Unused Flag
#define FLAG_UNUSED_0x352                                           0x352 // Unused Flag
#define FLAG_UNUSED_0x353                                           0x353 // Unused Flag
#define FLAG_UNUSED_0x354                                           0x354 // Unused Flag
#define FLAG_UNUSED_0x355                                           0x355 // Unused Flag
#define FLAG_UNUSED_0x356                                           0x356 // Unused Flag
#define FLAG_UNUSED_0x357                                           0x357 // Unused Flag
#define FLAG_UNUSED_0x358                                           0x358 // Unused Flag
#define FLAG_UNUSED_0x359                                           0x359 // Unused Flag
#define FLAG_HIDE_VICTORY_ROAD_ENTRANCE_WALLY                       0x35A
#define FLAG_UNUSED_0x35B                                           0x35B // Unused Flag
#define FLAG_UNUSED_0x35C                                           0x35C // Unused Flag
#define FLAG_UNUSED_0x35D                                           0x35D // Unused Flag
#define FLAG_UNUSED_0x35E                                           0x35E // Unused Flag
#define FLAG_UNUSED_0x35F                                           0x35F // Unused Flag
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_ALT_1           0x360
#define FLAG_HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_ALT_2           0x361
#define FLAG_UNUSED_0x362                                           0x362 // Unused Flag
#define FLAG_UNKNOWN_0x363                                          0x363 // Set, however has no purpose.
#define FLAG_UNUSED_0x364                                           0x364 // Unused Flag
#define FLAG_UNUSED_0x365                                           0x365 // Unused Flag
#define FLAG_UNUSED_0x366                                           0x366 // Unused Flag
#define FLAG_UNUSED_0x367                                           0x367 // Unused Flag
#define FLAG_UNUSED_0x368                                           0x368 // Unused Flag
#define FLAG_UNUSED_0x369                                           0x369 // Unused Flag
#define FLAG_UNUSED_0x36A                                           0x36A // Unused Flag
#define FLAG_UNUSED_0x36B                                           0x36B // Unused Flag
#define FLAG_UNUSED_0x36C                                           0x36C // Unused Flag
#define FLAG_UNUSED_0x36D                                           0x36D // Unused Flag
#define FLAG_UNUSED_0x36E                                           0x36E // Unused Flag
#define FLAG_UNUSED_0x36F                                           0x36F // Unused Flag
#define FLAG_UNUSED_0x370                                           0x370 // Unused Flag
#define FLAG_HIDE_BRINEYS_HOUSE_PEEKO                               0x371
#define FLAG_UNUSED_0x372                                           0x372 // Unused Flag
#define FLAG_UNUSED_0x373                                           0x373 // Unused Flag
#define FLAG_UNUSED_0x374                                           0x374 // Unused Flag
#define FLAG_UNUSED_0x375                                           0x375 // Unused Flag
#define FLAG_UNUSED_0x376                                           0x376 // Unused Flag
#define FLAG_UNUSED_0x377                                           0x377 // Unused Flag
#define FLAG_HIDE_BATTLE_TOWER_OPPONENT                             0x378
#define FLAG_UNUSED_0x379                                           0x379 // Unused Flag
#define FLAG_UNUSED_0x37A                                           0x37A // Unused Flag
#define FLAG_HIDE_ROUTE_116_MR_BRINEY                               0x37B
#define FLAG_UNUSED_0x37C                                           0x37C // Unused Flag
#define FLAG_UNUSED_0x37D                                           0x37D // Unused Flag
#define FLAG_UNUSED_0x37E                                           0x37E // Unused Flag
#define FLAG_UNUSED_0x37F                                           0x37F // Unused Flag
#define FLAG_UNUSED_0x380                                           0x380 // Unused Flag
#define FLAG_UNUSED_0x381                                           0x381 // Unused Flag
#define FLAG_UNUSED_0x382                                           0x382 // Unused Flag
#define FLAG_UNUSED_0x383                                           0x383 // Unused Flag
#define FLAG_UNUSED_0x384                                           0x384 // Unused Flag
#define FLAG_UNUSED_0x385                                           0x385 // Unused Flag
#define FLAG_UNUSED_0x386                                           0x386 // Unused Flag
#define FLAG_UNUSED_0x387                                           0x387 // Unused Flag
#define FLAG_UNUSED_0x388                                           0x388 // Unused Flag
#define FLAG_UNUSED_0x389                                           0x389 // Unused Flag
#define FLAG_UNUSED_0x38A                                           0x38A // Unused Flag
#define FLAG_UNUSED_0x38B                                           0x38B // Unused Flag
#define FLAG_UNUSED_0x38C                                           0x38C // Unused Flag
#define FLAG_UNUSED_0x38D                                           0x38D // Unused Flag
#define FLAG_UNUSED_0x38E                                           0x38E // Unused Flag
#define FLAG_UNUSED_0x38F                                           0x38F // Unused Flag
#define FLAG_UNUSED_0x390                                           0x390 // Unused Flag
#define FLAG_UNUSED_0x391                                           0x391 // Unused Flag
#define FLAG_UNUSED_0x392                                           0x392 // Unused Flag
#define FLAG_UNKNOWN_0x393                                          0x393 // Set, however has no purpose.
#define FLAG_UNUSED_0x394                                           0x394 // Unused Flag
#define FLAG_UNUSED_0x395                                           0x395 // Unused Flag
#define FLAG_HIDE_BATTLE_TOWER_REPORTER                             0x396
#define FLAG_UNUSED_0x397                                           0x397 // Unused Flag
#define FLAG_UNUSED_0x398                                           0x398 // Unused Flag
#define FLAG_UNUSED_0x399                                           0x399 // Unused Flag
#define FLAG_UNUSED_0x39A                                           0x39A // Unused Flag
#define FLAG_UNUSED_0x39B                                           0x39B // Unused Flag
#define FLAG_UNUSED_0x39C                                           0x39C // Unused Flag
#define FLAG_UNUSED_0x39D                                           0x39D // Unused Flag
#define FLAG_UNUSED_0x39E                                           0x39E // Unused Flag
#define FLAG_UNUSED_0x39F                                           0x39F // Unused Flag
#define FLAG_UNUSED_0x3A0                                           0x3A0 // Unused Flag
#define FLAG_UNUSED_0x3A1                                           0x3A1 // Unused Flag
#define FLAG_UNUSED_0x3A2                                           0x3A2 // Unused Flag
#define FLAG_HIDE_RUSTURF_TUNNEL_ROCK_1                             0x3A3
#define FLAG_HIDE_RUSTURF_TUNNEL_ROCK_2                             0x3A4
#define FLAG_UNUSED_0x3A5                                           0x3A5 // Unused Flag
#define FLAG_UNUSED_0x3A6                                           0x3A6 // Unused Flag
#define FLAG_UNUSED_0x3A7                                           0x3A7 // Unused Flag
#define FLAG_UNUSED_0x3A8                                           0x3A8 // Unused Flag
#define FLAG_UNUSED_0x3A9                                           0x3A9 // Unused Flag
#define FLAG_UNUSED_0x3AA                                           0x3AA // Unused Flag
#define FLAG_UNUSED_0x3AB                                           0x3AB // Unused Flag
#define FLAG_UNUSED_0x3AC                                           0x3AC // Unused Flag
#define FLAG_UNUSED_0x3AD                                           0x3AD // Unused Flag
#define FLAG_UNUSED_0x3AE                                           0x3AE // Unused Flag
#define FLAG_UNUSED_0x3AF                                           0x3AF // Unused Flag
#define FLAG_UNUSED_0x3B0                                           0x3B0 // Unused Flag
#define FLAG_UNUSED_0x3B1                                           0x3B1 // Unused Flag
#define FLAG_UNUSED_0x3B2                                           0x3B2 // Unused Flag
#define FLAG_UNUSED_0x3B3                                           0x3B3 // Unused Flag
#define FLAG_HIDE_SLATEPORT_CITY_TM_SALESMAN                        0x3B4
#define FLAG_UNUSED_0x3B5                                           0x3B5 // Unused Flag
#define FLAG_UNUSED_0x3B6                                           0x3B6 // Unused Flag
#define FLAG_UNUSED_0x3B7                                           0x3B7 // Unused Flag
#define FLAG_UNUSED_0x3B8                                           0x3B8 // Unused Flag
#define FLAG_UNUSED_0x3B9                                           0x3B9 // Unused Flag
#define FLAG_UNUSED_0x3BA                                           0x3BA // Unused Flag
#define FLAG_UNUSED_0x3BB                                           0x3BB // Unused Flag
#define FLAG_UNUSED_0x3BC                                           0x3BC // Unused Flag
#define FLAG_UNUSED_0x3BD                                           0x3BD // Unused Flag
#define FLAG_UNUSED_0x3BE                                           0x3BE // Unused Flag
#define FLAG_UNUSED_0x3BF                                           0x3BF // Unused Flag
#define FLAG_UNUSED_0x3C0                                           0x3C0 // Unused Flag
#define FLAG_UNUSED_0x3C1                                           0x3C1 // Unused Flag
#define FLAG_UNUSED_0x3C2                                           0x3C2 // Unused Flag
#define FLAG_UNUSED_0x3C3                                           0x3C3 // Unused Flag
#define FLAG_UNUSED_0x3C4                                           0x3C4 // Unused Flag
#define FLAG_UNUSED_0x3C5                                           0x3C5 // Unused Flag
#define FLAG_UNUSED_0x3C6                                           0x3C6 // Unused Flag
#define FLAG_UNUSED_0x3C7                                           0x3C7 // Unused Flag
#define FLAG_UNUSED_0x3C8                                           0x3C8 // Unused Flag
#define FLAG_UNUSED_0x3C9                                           0x3C9 // Unused Flag
#define FLAG_UNUSED_0x3CA                                           0x3CA // Unused Flag
#define FLAG_UNUSED_0x3CB                                           0x3CB // Unused Flag
#define FLAG_UNUSED_0x3CC                                           0x3CC // Unused Flag
#define FLAG_UNUSED_0x3CD                                           0x3CD // Unused Flag
#define FLAG_UNUSED_0x3CE                                           0x3CE // Unused Flag
#define FLAG_UNUSED_0x3CF                                           0x3CF // Unused Flag
#define FLAG_UNUSED_0x3D0                                           0x3D0 // Unused Flag
#define FLAG_UNUSED_0x3D1                                           0x3D1 // Unused Flag
#define FLAG_UNUSED_0x3D2                                           0x3D2 // Unused Flag
#define FLAG_UNUSED_0x3D3                                           0x3D3 // Unused Flag
#define FLAG_UNUSED_0x3D4                                           0x3D4 // Unused Flag
#define FLAG_UNUSED_0x3D5                                           0x3D5 // Unused Flag
#define FLAG_UNUSED_0x3D6                                           0x3D6 // Unused Flag
#define FLAG_UNUSED_0x3D7                                           0x3D7 // Unused Flag
#define FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDA                0x3D8
#define FLAG_UNUSED_0x3D9                                           0x3D9 // Unused Flag
#define FLAG_UNUSED_0x3DA                                           0x3DA // Unused Flag
#define FLAG_UNUSED_0x3DB                                           0x3DB // Unused Flag
#define FLAG_UNUSED_0x3DC                                           0x3DC // Unused Flag
#define FLAG_UNUSED_0x3DD                                           0x3DD // Unused Flag
#define FLAG_UNUSED_0x3DE                                           0x3DE // Unused Flag
#define FLAG_UNUSED_0x3DF                                           0x3DF // Unused Flag
#define FLAG_UNUSED_0x3E0                                           0x3E0 // Unused Flag
#define FLAG_UNUSED_0x3E1                                           0x3E1 // Unused Flag
#define FLAG_UNUSED_0x3E2                                           0x3E2 // Unused Flag
#define FLAG_UNUSED_0x3E3                                           0x3E3 // Unused Flag
#define FLAG_HIDE_SOOTOPOLIS_CITY_RAYQUAZA                          0x3E4
#define FLAG_UNUSED_0x3E5                                           0x3E5 // Unused Flag
#define FLAG_UNUSED_0x3E6                                           0x3E6 // Unused Flag
#define FLAG_UNUSED_0x3E7                                           0x3E7 // Unused Flag

// Item Ball Flags
#define FLAG_UNUSED_0x3E8                                           0x3E8 // Unused Flag
#define FLAG_UNUSED_0x3E9                                           0x3E9 // Unused Flag
#define FLAG_UNUSED_0x3EA                                           0x3EA // Unused Flag
#define FLAG_UNUSED_0x3EB                                           0x3EB // Unused Flag
#define FLAG_UNUSED_0x3EC                                           0x3EC // Unused Flag
#define FLAG_UNUSED_0x3ED                                           0x3ED // Unused Flag
#define FLAG_UNUSED_0x3EE                                           0x3EE // Unused Flag
#define FLAG_UNUSED_0x3EF                                           0x3EF // Unused Flag
#define FLAG_UNUSED_0x3F0                                           0x3F0 // Unused Flag
#define FLAG_UNUSED_0x3F1                                           0x3F1 // Unused Flag
#define FLAG_UNUSED_0x3F2                                           0x3F2 // Unused Flag
#define FLAG_UNUSED_0x3F3                                           0x3F3 // Unused Flag
#define FLAG_UNUSED_0x3F4                                           0x3F4 // Unused Flag
#define FLAG_UNUSED_0x3F5                                           0x3F5 // Unused Flag
#define FLAG_UNUSED_0x3F6                                           0x3F6 // Unused Flag
#define FLAG_UNUSED_0x3F7                                           0x3F7 // Unused Flag
#define FLAG_UNUSED_0x3F8                                           0x3F8 // Unused Flag
#define FLAG_UNUSED_0x3F9                                           0x3F9 // Unused Flag
#define FLAG_UNUSED_0x3FA                                           0x3FA // Unused Flag
#define FLAG_UNUSED_0x3FB                                           0x3FB // Unused Flag
#define FLAG_UNUSED_0x3FC                                           0x3FC // Unused Flag
#define FLAG_UNUSED_0x3FD                                           0x3FD // Unused Flag
#define FLAG_UNUSED_0x3FE                                           0x3FE // Unused Flag
#define FLAG_UNUSED_0x3FF                                           0x3FF // Unused Flag
#define FLAG_UNUSED_0x400                                           0x400 // Unused Flag
#define FLAG_UNUSED_0x401                                           0x401 // Unused Flag
#define FLAG_UNUSED_0x402                                           0x402 // Unused Flag
#define FLAG_UNUSED_0x403                                           0x403 // Unused Flag
#define FLAG_UNUSED_0x404                                           0x404 // Unused Flag
#define FLAG_UNUSED_0x405                                           0x405 // Unused Flag
#define FLAG_UNUSED_0x406                                           0x406 // Unused Flag
#define FLAG_UNUSED_0x407                                           0x407 // Unused Flag
#define FLAG_UNUSED_0x408                                           0x408 // Unused Flag
#define FLAG_UNUSED_0x409                                           0x409 // Unused Flag
#define FLAG_UNUSED_0x40A                                           0x40A // Unused Flag
#define FLAG_UNUSED_0x40B                                           0x40B // Unused Flag
#define FLAG_UNUSED_0x40C                                           0x40C // Unused Flag
#define FLAG_UNUSED_0x40D                                           0x40D // Unused Flag
#define FLAG_UNUSED_0x40E                                           0x40E // Unused Flag
#define FLAG_UNUSED_0x40F                                           0x40F // Unused Flag
#define FLAG_UNUSED_0x410                                           0x410 // Unused Flag
#define FLAG_UNUSED_0x411                                           0x411 // Unused Flag
#define FLAG_UNUSED_0x412                                           0x412 // Unused Flag
#define FLAG_UNUSED_0x413                                           0x413 // Unused Flag
#define FLAG_UNUSED_0x414                                           0x414 // Unused Flag
#define FLAG_UNUSED_0x415                                           0x415 // Unused Flag
#define FLAG_UNUSED_0x416                                           0x416 // Unused Flag
#define FLAG_UNUSED_0x417                                           0x417 // Unused Flag
#define FLAG_UNUSED_0x418                                           0x418 // Unused Flag
#define FLAG_UNUSED_0x419                                           0x419 // Unused Flag
#define FLAG_UNUSED_0x41A                                           0x41A // Unused Flag
#define FLAG_UNUSED_0x41B                                           0x41B // Unused Flag
#define FLAG_UNUSED_0x41C                                           0x41C // Unused Flag
#define FLAG_UNUSED_0x41D                                           0x41D // Unused Flag
#define FLAG_UNUSED_0x41E                                           0x41E // Unused Flag
#define FLAG_UNUSED_0x41F                                           0x41F // Unused Flag
#define FLAG_UNUSED_0x420                                           0x420 // Unused Flag
#define FLAG_UNUSED_0x421                                           0x421 // Unused Flag
#define FLAG_UNUSED_0x422                                           0x422 // Unused Flag
#define FLAG_UNUSED_0x423                                           0x423 // Unused Flag
#define FLAG_UNUSED_0x424                                           0x424 // Unused Flag
#define FLAG_UNUSED_0x425                                           0x425 // Unused Flag
#define FLAG_UNUSED_0x426                                           0x426 // Unused Flag
#define FLAG_UNUSED_0x427                                           0x427 // Unused Flag
#define FLAG_UNUSED_0x428                                           0x428 // Unused Flag
#define FLAG_UNUSED_0x429                                           0x429 // Unused Flag
#define FLAG_UNUSED_0x42A                                           0x42A // Unused Flag
#define FLAG_UNUSED_0x42B                                           0x42B // Unused Flag
#define FLAG_UNUSED_0x42C                                           0x42C // Unused Flag
#define FLAG_UNUSED_0x42D                                           0x42D // Unused Flag
#define FLAG_UNUSED_0x42E                                           0x42E // Unused Flag
#define FLAG_UNUSED_0x42F                                           0x42F // Unused Flag
#define FLAG_UNUSED_0x430                                           0x430 // Unused Flag
#define FLAG_UNUSED_0x431                                           0x431 // Unused Flag
#define FLAG_UNUSED_0x432                                           0x432 // Unused Flag
#define FLAG_UNUSED_0x433                                           0x433 // Unused Flag
#define FLAG_UNUSED_0x434                                           0x434 // Unused Flag
#define FLAG_UNUSED_0x435                                           0x435 // Unused Flag
#define FLAG_UNUSED_0x436                                           0x436 // Unused Flag
#define FLAG_UNUSED_0x437                                           0x437 // Unused Flag
#define FLAG_UNUSED_0x438                                           0x438 // Unused Flag
#define FLAG_UNUSED_0x439                                           0x439 // Unused Flag
#define FLAG_UNUSED_0x43A                                           0x43A // Unused Flag
#define FLAG_UNUSED_0x43B                                           0x43B // Unused Flag
#define FLAG_UNUSED_0x43C                                           0x43C // Unused Flag
#define FLAG_UNUSED_0x43D                                           0x43D // Unused Flag
#define FLAG_UNUSED_0x43E                                           0x43E // Unused Flag
#define FLAG_UNUSED_0x43F                                           0x43F // Unused Flag
#define FLAG_UNUSED_0x440                                           0x440 // Unused Flag
#define FLAG_UNUSED_0x441                                           0x441 // Unused Flag
#define FLAG_UNUSED_0x442                                           0x442 // Unused Flag
#define FLAG_UNUSED_0x443                                           0x443 // Unused Flag
#define FLAG_UNUSED_0x444                                           0x444 // Unused Flag
#define FLAG_UNUSED_0x445                                           0x445 // Unused Flag
#define FLAG_UNUSED_0x446                                           0x446 // Unused Flag
#define FLAG_UNUSED_0x447                                           0x447 // Unused Flag
#define FLAG_UNUSED_0x448                                           0x448 // Unused Flag
#define FLAG_UNUSED_0x449                                           0x449 // Unused Flag
#define FLAG_UNUSED_0x44A                                           0x44A // Unused Flag
#define FLAG_UNUSED_0x44B                                           0x44B // Unused Flag
#define FLAG_UNUSED_0x44C                                           0x44C // Unused Flag
#define FLAG_UNUSED_0x44D                                           0x44D // Unused Flag
#define FLAG_UNUSED_0x44E                                           0x44E // Unused Flag
#define FLAG_UNUSED_0x44F                                           0x44F // Unused Flag
#define FLAG_UNUSED_0x450                                           0x450 // Unused Flag
#define FLAG_UNUSED_0x451                                           0x451 // Unused Flag
#define FLAG_UNUSED_0x452                                           0x452 // Unused Flag
#define FLAG_UNUSED_0x453                                           0x453 // Unused Flag
#define FLAG_UNUSED_0x454                                           0x454 // Unused Flag
#define FLAG_UNUSED_0x455                                           0x455 // Unused Flag
#define FLAG_UNUSED_0x456                                           0x456 // Unused Flag
#define FLAG_UNUSED_0x457                                           0x457 // Unused Flag
#define FLAG_UNUSED_0x458                                           0x458 // Unused Flag
#define FLAG_UNUSED_0x459                                           0x459 // Unused Flag
#define FLAG_UNUSED_0x45A                                           0x45A // Unused Flag
#define FLAG_UNUSED_0x45B                                           0x45B // Unused Flag
#define FLAG_UNUSED_0x45C                                           0x45C // Unused Flag
#define FLAG_UNUSED_0x45D                                           0x45D // Unused Flag
#define FLAG_UNUSED_0x45E                                           0x45E // Unused Flag
#define FLAG_UNUSED_0x45F                                           0x45F // Unused Flag
#define FLAG_UNUSED_0x460                                           0x460 // Unused Flag
#define FLAG_UNUSED_0x461                                           0x461 // Unused Flag
#define FLAG_UNUSED_0x462                                           0x462 // Unused Flag
#define FLAG_UNUSED_0x463                                           0x463 // Unused Flag
#define FLAG_UNUSED_0x464                                           0x464 // Unused Flag
#define FLAG_UNUSED_0x465                                           0x465 // Unused Flag
#define FLAG_UNUSED_0x466                                           0x466 // Unused Flag
#define FLAG_UNUSED_0x467                                           0x467 // Unused Flag
#define FLAG_UNUSED_0x468                                           0x468 // Unused Flag
#define FLAG_UNUSED_0x469                                           0x469 // Unused Flag
#define FLAG_UNUSED_0x46A                                           0x46A // Unused Flag
#define FLAG_UNUSED_0x46B                                           0x46B // Unused Flag
#define FLAG_UNUSED_0x46C                                           0x46C // Unused Flag
#define FLAG_UNUSED_0x46D                                           0x46D // Unused Flag
#define FLAG_UNUSED_0x46E                                           0x46E // Unused Flag
#define FLAG_UNUSED_0x46F                                           0x46F // Unused Flag
#define FLAG_UNUSED_0x470                                           0x470 // Unused Flag
#define FLAG_UNUSED_0x471                                           0x471 // Unused Flag
#define FLAG_UNUSED_0x472                                           0x472 // Unused Flag
#define FLAG_UNUSED_0x473                                           0x473 // Unused Flag
#define FLAG_UNUSED_0x474                                           0x474 // Unused Flag
#define FLAG_UNUSED_0x475                                           0x475 // Unused Flag
#define FLAG_UNUSED_0x476                                           0x476 // Unused Flag
#define FLAG_UNUSED_0x477                                           0x477 // Unused Flag
#define FLAG_UNUSED_0x478                                           0x478 // Unused Flag
#define FLAG_UNUSED_0x479                                           0x479 // Unused Flag
#define FLAG_UNUSED_0x47A                                           0x47A // Unused Flag
#define FLAG_UNUSED_0x47B                                           0x47B // Unused Flag
#define FLAG_UNUSED_0x47C                                           0x47C // Unused Flag
#define FLAG_UNUSED_0x47D                                           0x47D // Unused Flag
#define FLAG_UNUSED_0x47E                                           0x47E // Unused Flag
#define FLAG_UNUSED_0x47F                                           0x47F // Unused Flag
#define FLAG_UNUSED_0x480                                           0x480 // Unused Flag
#define FLAG_UNUSED_0x481                                           0x481 // Unused Flag
#define FLAG_UNUSED_0x482                                           0x482 // Unused Flag
#define FLAG_UNUSED_0x483                                           0x483 // Unused Flag
#define FLAG_UNUSED_0x484                                           0x484 // Unused Flag
#define FLAG_UNUSED_0x485                                           0x485 // Unused Flag
#define FLAG_UNUSED_0x486                                           0x486 // Unused Flag
#define FLAG_UNUSED_0x487                                           0x487 // Unused Flag
#define FLAG_UNUSED_0x488                                           0x488 // Unused Flag
#define FLAG_UNUSED_0x489                                           0x489 // Unused Flag
#define FLAG_UNUSED_0x48A                                           0x48A // Unused Flag
#define FLAG_UNUSED_0x48B                                           0x48B // Unused Flag
#define FLAG_UNUSED_0x48C                                           0x48C // Unused Flag
#define FLAG_UNUSED_0x48D                                           0x48D // Unused Flag
#define FLAG_UNUSED_0x48E                                           0x48E // Unused Flag
#define FLAG_UNUSED_0x48F                                           0x48F // Unused Flag
#define FLAG_UNUSED_0x490                                           0x490 // Unused Flag
#define FLAG_UNUSED_0x491                                           0x491 // Unused Flag
#define FLAG_UNUSED_0x492                                           0x492 // Unused Flag

#define FLAG_UNUSED_0x493                                           0x493 // Unused Flag
#define FLAG_UNUSED_0x494                                           0x494 // Unused Flag
#define FLAG_UNUSED_0x495                                           0x495 // Unused Flag
#define FLAG_UNUSED_0x496                                           0x496 // Unused Flag
#define FLAG_UNUSED_0x497                                           0x497 // Unused Flag
#define FLAG_UNUSED_0x498                                           0x498 // Unused Flag
#define FLAG_UNUSED_0x499                                           0x499 // Unused Flag
#define FLAG_UNUSED_0x49A                                           0x49A // Unused Flag
#define FLAG_UNUSED_0x49B                                           0x49B // Unused Flag
#define FLAG_UNUSED_0x49C                                           0x49C // Unused Flag
#define FLAG_UNUSED_0x49D                                           0x49D // Unused Flag
#define FLAG_UNUSED_0x49E                                           0x49E // Unused Flag
#define FLAG_UNUSED_0x49F                                           0x49F // Unused Flag
#define FLAG_UNUSED_0x4A0                                           0x4A0 // Unused Flag
#define FLAG_UNUSED_0x4A1                                           0x4A1 // Unused Flag
#define FLAG_UNUSED_0x4A2                                           0x4A2 // Unused Flag
#define FLAG_UNUSED_0x4A3                                           0x4A3 // Unused Flag
#define FLAG_UNUSED_0x4A4                                           0x4A4 // Unused Flag
#define FLAG_UNUSED_0x4A5                                           0x4A5 // Unused Flag
#define FLAG_UNUSED_0x4A6                                           0x4A6 // Unused Flag
#define FLAG_UNUSED_0x4A7                                           0x4A7 // Unused Flag
#define FLAG_UNUSED_0x4A8                                           0x4A8 // Unused Flag
#define FLAG_UNUSED_0x4A9                                           0x4A9 // Unused Flag
#define FLAG_UNUSED_0x4AA                                           0x4AA // Unused Flag
#define FLAG_UNUSED_0x4AB                                           0x4AB // Unused Flag
#define FLAG_UNUSED_0x4AC                                           0x4AC // Unused Flag
#define FLAG_UNUSED_0x4AD                                           0x4AD // Unused Flag
#define FLAG_UNUSED_0x4AE                                           0x4AE // Unused Flag
#define FLAG_UNUSED_0x4AF                                           0x4AF // Unused Flag
#define FLAG_UNUSED_0x4B0                                           0x4B0 // Unused Flag
#define FLAG_UNUSED_0x4B1                                           0x4B1 // Unused Flag
#define FLAG_UNUSED_0x4B2                                           0x4B2 // Unused Flag
#define FLAG_UNUSED_0x4B3                                           0x4B3 // Unused Flag
#define FLAG_UNUSED_0x4B4                                           0x4B4 // Unused Flag
#define FLAG_UNUSED_0x4B5                                           0x4B5 // Unused Flag
#define FLAG_UNUSED_0x4B6                                           0x4B6 // Unused Flag
#define FLAG_UNUSED_0x4B7                                           0x4B7 // Unused Flag
#define FLAG_UNUSED_0x4B8                                           0x4B8 // Unused Flag
#define FLAG_UNUSED_0x4B9                                           0x4B9 // Unused Flag
#define FLAG_UNUSED_0x4BA                                           0x4BA // Unused Flag
#define FLAG_UNUSED_0x4BB                                           0x4BB // Unused Flag
#define FLAG_UNUSED_0x4BC                                           0x4BC // Unused Flag
#define FLAG_UNUSED_0x4BD                                           0x4BD // Unused Flag
#define FLAG_UNUSED_0x4BE                                           0x4BE // Unused Flag
#define FLAG_UNUSED_0x4BF                                           0x4BF // Unused Flag
#define FLAG_UNUSED_0x4C0                                           0x4C0 // Unused Flag
#define FLAG_UNUSED_0x4C1                                           0x4C1 // Unused Flag
#define FLAG_UNUSED_0x4C2                                           0x4C2 // Unused Flag
#define FLAG_UNUSED_0x4C3                                           0x4C3 // Unused Flag
#define FLAG_UNUSED_0x4C4                                           0x4C4 // Unused Flag
#define FLAG_UNUSED_0x4C5                                           0x4C5 // Unused Flag
#define FLAG_UNUSED_0x4C6                                           0x4C6 // Unused Flag
#define FLAG_UNUSED_0x4C7                                           0x4C7 // Unused Flag
#define FLAG_UNUSED_0x4C8                                           0x4C8 // Unused Flag
#define FLAG_UNUSED_0x4C9                                           0x4C9 // Unused Flag
#define FLAG_UNUSED_0x4CA                                           0x4CA // Unused Flag
#define FLAG_UNUSED_0x4CB                                           0x4CB // Unused Flag
#define FLAG_UNUSED_0x4CC                                           0x4CC // Unused Flag
#define FLAG_UNUSED_0x4CD                                           0x4CD // Unused Flag
#define FLAG_UNUSED_0x4CE                                           0x4CE // Unused Flag
#define FLAG_UNUSED_0x4CF                                           0x4CF // Unused Flag
#define FLAG_UNUSED_0x4D0                                           0x4D0 // Unused Flag
#define FLAG_UNUSED_0x4D1                                           0x4D1 // Unused Flag
#define FLAG_UNUSED_0x4D2                                           0x4D2 // Unused Flag
#define FLAG_UNUSED_0x4D3                                           0x4D3 // Unused Flag
#define FLAG_UNUSED_0x4D4                                           0x4D4 // Unused Flag
#define FLAG_UNUSED_0x4D5                                           0x4D5 // Unused Flag
#define FLAG_UNUSED_0x4D6                                           0x4D6 // Unused Flag
#define FLAG_UNUSED_0x4D7                                           0x4D7 // Unused Flag
#define FLAG_UNUSED_0x4D8                                           0x4D8 // Unused Flag
#define FLAG_UNUSED_0x4D9                                           0x4D9 // Unused Flag
#define FLAG_UNUSED_0x4DA                                           0x4DA // Unused Flag
#define FLAG_UNUSED_0x4DB                                           0x4DB // Unused Flag
#define FLAG_UNUSED_0x4DC                                           0x4DC // Unused Flag
#define FLAG_UNUSED_0x4DD                                           0x4DD // Unused Flag
#define FLAG_UNUSED_0x4DE                                           0x4DE // Unused Flag
#define FLAG_UNUSED_0x4DF                                           0x4DF // Unused Flag
#define FLAG_ICHOR_ITEM_AKTI_POTION                                 0x4E0 // Ichor: Akti item ball: Potion among the quay crates
#define FLAG_ICHOR_ITEM_AKTI_PARALYZE_HEAL                          0x4E1 // Ichor: Akti item ball: Paralyze Heal by the fish stall
#define FLAG_ICHOR_HIDDEN_ITEM_AKTI_SUPER_POTION                    0x4E2 // Ichor: Akti hidden item: Super Potion behind Diktys's nets
#define FLAG_ICHOR_HIDDEN_ITEM_AKTI_PEARL                           0x4E3 // Ichor: Akti hidden item: Pearl on the tide rocks
#define FLAG_ICHOR_HIDDEN_ITEM_AKTI_HEART_SCALE                     0x4E4 // Ichor: Akti hidden item: Heart Scale on the beach
#define FLAG_UNUSED_0x4E5                                           0x4E5 // Unused Flag
#define FLAG_UNUSED_0x4E6                                           0x4E6 // Unused Flag
#define FLAG_UNUSED_0x4E7                                           0x4E7 // Unused Flag
#define FLAG_UNUSED_0x4E8                                           0x4E8 // Unused Flag
#define FLAG_UNUSED_0x4E9                                           0x4E9 // Unused Flag
#define FLAG_UNUSED_0x4EA                                           0x4EA // Unused Flag
#define FLAG_UNUSED_0x4EB                                           0x4EB // Unused Flag
#define FLAG_UNUSED_0x4EC                                           0x4EC // Unused Flag
#define FLAG_UNUSED_0x4ED                                           0x4ED // Unused Flag
#define FLAG_UNUSED_0x4EE                                           0x4EE // Unused Flag
#define FLAG_UNUSED_0x4EF                                           0x4EF // Unused Flag

#define FLAG_UNUSED_0x4F0                                           0x4F0 // Unused Flag
#define FLAG_DEFEATED_DEWFORD_GYM                                   0x4F1
#define FLAG_UNUSED_0x4F2                                           0x4F2 // Unused Flag
#define FLAG_DEFEATED_LAVARIDGE_GYM                                 0x4F3
#define FLAG_DEFEATED_PETALBURG_GYM                                 0x4F4
#define FLAG_UNUSED_0x4F5                                           0x4F5 // Unused Flag
#define FLAG_DEFEATED_MOSSDEEP_GYM                                  0x4F6
#define FLAG_DEFEATED_SOOTOPOLIS_GYM                                0x4F7
#define FLAG_DEFEATED_METEOR_FALLS_STEVEN                           0x4F8

#define FLAG_UNUSED_0x4F9                                           0x4F9 // Unused Flag
#define FLAG_UNUSED_0x4FA                                           0x4FA // Unused Flag

#define FLAG_DEFEATED_ELITE_4_SIDNEY                                0x4FB
#define FLAG_DEFEATED_ELITE_4_PHOEBE                                0x4FC
#define FLAG_DEFEATED_ELITE_4_GLACIA                                0x4FD
#define FLAG_DEFEATED_ELITE_4_DRAKE                                 0x4FE

#define FLAG_UNUSED_0x4FF                                           0x4FF // Unused Flag

// Trainer Flags
// Trainer flags occupy 0x500 - 0xAFF (Ichor: MAX_TRAINERS_COUNT_EMERALD is 1536)
// See constants/opponents.h. The values there + FLAG_TRAINER_FLAG_START are the flag IDs

#define TRAINER_FLAGS_START                                         0x500
#define TRAINER_FLAGS_END                                           (TRAINER_FLAGS_START + MAX_TRAINERS_COUNT - 1) // 0xAFF (Ichor: 1536 trainers)

// System Flags

#define SYSTEM_FLAGS                                   (TRAINER_FLAGS_END + 1) // 0xB00 (Ichor)

#define FLAG_SYS_POKEMON_GET                         (SYSTEM_FLAGS + 0x0) // FLAG_0x860
#define FLAG_SYS_POKEDEX_GET                         (SYSTEM_FLAGS + 0x1)
#define FLAG_SYS_POKENAV_GET                         (SYSTEM_FLAGS + 0x2)
#define FLAG_UNUSED_0x863                            (SYSTEM_FLAGS + 0x3) // Unused Flag
#define FLAG_SYS_GAME_CLEAR                          (SYSTEM_FLAGS + 0x4)
#define FLAG_SYS_CHAT_USED                           (SYSTEM_FLAGS + 0x5)
#define FLAG_UNLOCKED_TRENDY_SAYINGS                 (SYSTEM_FLAGS + 0x6)

// Badges
#define FLAG_BADGE01_GET                      (SYSTEM_FLAGS + 0x7)
#define FLAG_BADGE02_GET                      (SYSTEM_FLAGS + 0x8)
#define FLAG_BADGE03_GET                      (SYSTEM_FLAGS + 0x9)
#define FLAG_BADGE04_GET                      (SYSTEM_FLAGS + 0xA)
#define FLAG_BADGE05_GET                      (SYSTEM_FLAGS + 0xB)
#define FLAG_BADGE06_GET                      (SYSTEM_FLAGS + 0xC)
#define FLAG_BADGE07_GET                      (SYSTEM_FLAGS + 0xD)
#define FLAG_BADGE08_GET                      (SYSTEM_FLAGS + 0xE)
#define NUM_BADGES                            (1 + FLAG_BADGE08_GET - FLAG_BADGE01_GET)

// Towns and Cities
#define FLAG_VISITED_LITTLEROOT_TOWN                (SYSTEM_FLAGS + 0xF)
#define FLAG_VISITED_OLDALE_TOWN                    (SYSTEM_FLAGS + 0x10)
#define FLAG_VISITED_DEWFORD_TOWN                   (SYSTEM_FLAGS + 0x11)
#define FLAG_VISITED_LAVARIDGE_TOWN                 (SYSTEM_FLAGS + 0x12)
#define FLAG_VISITED_FALLARBOR_TOWN                 (SYSTEM_FLAGS + 0x13)
#define FLAG_VISITED_VERDANTURF_TOWN                (SYSTEM_FLAGS + 0x14)
#define FLAG_VISITED_PACIFIDLOG_TOWN                (SYSTEM_FLAGS + 0x15)
#define FLAG_VISITED_PETALBURG_CITY                 (SYSTEM_FLAGS + 0x16)
#define FLAG_VISITED_SLATEPORT_CITY                 (SYSTEM_FLAGS + 0x17)
#define FLAG_VISITED_MAUVILLE_CITY                  (SYSTEM_FLAGS + 0x18)
#define FLAG_VISITED_RUSTBORO_CITY                  (SYSTEM_FLAGS + 0x19)
#define FLAG_VISITED_FORTREE_CITY                   (SYSTEM_FLAGS + 0x1A)
#define FLAG_VISITED_LILYCOVE_CITY                  (SYSTEM_FLAGS + 0x1B)
#define FLAG_VISITED_MOSSDEEP_CITY                  (SYSTEM_FLAGS + 0x1C)
#define FLAG_VISITED_SOOTOPOLIS_CITY                (SYSTEM_FLAGS + 0x1D)
#define FLAG_VISITED_EVER_GRANDE_CITY               (SYSTEM_FLAGS + 0x1E)

#define FLAG_IS_CHAMPION                            (SYSTEM_FLAGS + 0x1F) // Seems to be related to linking.
#define FLAG_NURSE_UNION_ROOM_REMINDER              (SYSTEM_FLAGS + 0x20)

#define FLAG_UNUSED_0x881                           (SYSTEM_FLAGS + 0x21) // Unused Flag
#define FLAG_UNUSED_0x882                           (SYSTEM_FLAGS + 0x22) // Unused Flag
#define FLAG_UNUSED_0x883                           (SYSTEM_FLAGS + 0x23) // Unused Flag
#define FLAG_UNUSED_0x884                           (SYSTEM_FLAGS + 0x24) // Unused Flag
#define FLAG_UNUSED_0x885                           (SYSTEM_FLAGS + 0x25) // Unused Flag
#define FLAG_UNUSED_0x886                           (SYSTEM_FLAGS + 0x26) // Unused Flag
#define FLAG_UNUSED_0x887                           (SYSTEM_FLAGS + 0x27) // Unused Flag

#define FLAG_SYS_USE_FLASH                          (SYSTEM_FLAGS + 0x28)
#define FLAG_SYS_USE_STRENGTH                       (SYSTEM_FLAGS + 0x29)
// Sets abnormal weather on maps that check for it
#define FLAG_SYS_WEATHER_CTRL                       (SYSTEM_FLAGS + 0x2A)
#define FLAG_SYS_CYCLING_ROAD                       (SYSTEM_FLAGS + 0x2B)
#define FLAG_SYS_SAFARI_MODE                        (SYSTEM_FLAGS + 0x2C)
#define FLAG_SYS_CRUISE_MODE                        (SYSTEM_FLAGS + 0x2D)

#define FLAG_UNUSED_0x88E                           (SYSTEM_FLAGS + 0x2E) // Unused Flag
#define FLAG_UNUSED_0x88F                           (SYSTEM_FLAGS + 0x2F) // Unused Flag

#define FLAG_SYS_TV_HOME                            (SYSTEM_FLAGS + 0x30)
#define FLAG_SYS_TV_WATCH                           (SYSTEM_FLAGS + 0x31)
#define FLAG_SYS_TV_START                           (SYSTEM_FLAGS + 0x32)
#define FLAG_SYS_CHANGED_DEWFORD_TREND              (SYSTEM_FLAGS + 0x33)
#define FLAG_SYS_MIX_RECORD                         (SYSTEM_FLAGS + 0x34)
#define FLAG_SYS_CLOCK_SET                          (SYSTEM_FLAGS + 0x35)
#define FLAG_SYS_NATIONAL_DEX                       (SYSTEM_FLAGS + 0x36)
#define FLAG_SYS_CAVE_SHIP                          (SYSTEM_FLAGS + 0x37) // Unused Flag, leftover from R/S debug, presumably used by Emerald's debug too
#define FLAG_SYS_CAVE_WONDER                        (SYSTEM_FLAGS + 0x38) // Unused Flag, same as above
#define FLAG_SYS_CAVE_BATTLE                        (SYSTEM_FLAGS + 0x39) // Unused Flag, same as above
#define FLAG_SYS_SHOAL_TIDE                         (SYSTEM_FLAGS + 0x3A)
#define FLAG_SYS_RIBBON_GET                         (SYSTEM_FLAGS + 0x3B)

#define FLAG_LANDMARK_FLOWER_SHOP                   (SYSTEM_FLAGS + 0x3C)
#define FLAG_LANDMARK_MR_BRINEY_HOUSE               (SYSTEM_FLAGS + 0x3D)
#define FLAG_LANDMARK_ABANDONED_SHIP                (SYSTEM_FLAGS + 0x3E)
#define FLAG_LANDMARK_SEASHORE_HOUSE                (SYSTEM_FLAGS + 0x3F)
#define FLAG_LANDMARK_NEW_MAUVILLE                  (SYSTEM_FLAGS + 0x40)
#define FLAG_LANDMARK_OLD_LADY_REST_SHOP            (SYSTEM_FLAGS + 0x41)
#define FLAG_LANDMARK_TRICK_HOUSE                   (SYSTEM_FLAGS + 0x42)
#define FLAG_LANDMARK_WINSTRATE_FAMILY              (SYSTEM_FLAGS + 0x43)
#define FLAG_LANDMARK_GLASS_WORKSHOP                (SYSTEM_FLAGS + 0x44)
#define FLAG_LANDMARK_LANETTES_HOUSE                (SYSTEM_FLAGS + 0x45)
#define FLAG_LANDMARK_POKEMON_DAYCARE               (SYSTEM_FLAGS + 0x46)
#define FLAG_LANDMARK_SEAFLOOR_CAVERN               (SYSTEM_FLAGS + 0x47)
#define FLAG_LANDMARK_BATTLE_FRONTIER               (SYSTEM_FLAGS + 0x48)
#define FLAG_LANDMARK_SOUTHERN_ISLAND               (SYSTEM_FLAGS + 0x49)
#define FLAG_LANDMARK_FIERY_PATH                    (SYSTEM_FLAGS + 0x4A)

#define FLAG_SYS_PC_LANETTE                         (SYSTEM_FLAGS + 0x4B)
#define FLAG_SYS_MYSTERY_EVENT_ENABLE               (SYSTEM_FLAGS + 0x4C)
#define FLAG_SYS_ENC_UP_ITEM                        (SYSTEM_FLAGS + 0x4D)
#define FLAG_SYS_ENC_DOWN_ITEM                      (SYSTEM_FLAGS + 0x4E)
#define FLAG_SYS_BRAILLE_DIG                        (SYSTEM_FLAGS + 0x4F)
#define FLAG_SYS_REGIROCK_PUZZLE_COMPLETED          (SYSTEM_FLAGS + 0x50)
#define FLAG_SYS_BRAILLE_REGICE_COMPLETED           (SYSTEM_FLAGS + 0x51)
#define FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED         (SYSTEM_FLAGS + 0x52)
#define FLAG_ENABLE_SHIP_SOUTHERN_ISLAND            (SYSTEM_FLAGS + 0x53)

#define FLAG_LANDMARK_POKEMON_LEAGUE                (SYSTEM_FLAGS + 0x54)
#define FLAG_LANDMARK_ISLAND_CAVE                   (SYSTEM_FLAGS + 0x55)
#define FLAG_LANDMARK_DESERT_RUINS                  (SYSTEM_FLAGS + 0x56)
#define FLAG_LANDMARK_FOSSIL_MANIACS_HOUSE          (SYSTEM_FLAGS + 0x57)
#define FLAG_LANDMARK_SCORCHED_SLAB                 (SYSTEM_FLAGS + 0x58)
#define FLAG_LANDMARK_ANCIENT_TOMB                  (SYSTEM_FLAGS + 0x59)
#define FLAG_LANDMARK_TUNNELERS_REST_HOUSE          (SYSTEM_FLAGS + 0x5A)
#define FLAG_LANDMARK_HUNTERS_HOUSE                 (SYSTEM_FLAGS + 0x5B)
#define FLAG_LANDMARK_SEALED_CHAMBER                (SYSTEM_FLAGS + 0x5C)

#define FLAG_SYS_TV_LATIAS_LATIOS                   (SYSTEM_FLAGS + 0x5D)

#define FLAG_LANDMARK_SKY_PILLAR                    (SYSTEM_FLAGS + 0x5E)

#define FLAG_SYS_SHOAL_ITEM                         (SYSTEM_FLAGS + 0x5F)
#define FLAG_SYS_B_DASH                             (SYSTEM_FLAGS + 0x60) // RECEIVED Running Shoes
#define FLAG_SYS_CTRL_OBJ_DELETE                    (SYSTEM_FLAGS + 0x61)
#define FLAG_SYS_RESET_RTC_ENABLE                   (SYSTEM_FLAGS + 0x62)

#define FLAG_LANDMARK_BERRY_MASTERS_HOUSE           (SYSTEM_FLAGS + 0x63)

#define FLAG_SYS_TOWER_SILVER                       (SYSTEM_FLAGS + 0x64)
#define FLAG_SYS_TOWER_GOLD                         (SYSTEM_FLAGS + 0x65)
#define FLAG_SYS_DOME_SILVER                        (SYSTEM_FLAGS + 0x66)
#define FLAG_SYS_DOME_GOLD                          (SYSTEM_FLAGS + 0x67)
#define FLAG_SYS_PALACE_SILVER                      (SYSTEM_FLAGS + 0x68)
#define FLAG_SYS_PALACE_GOLD                        (SYSTEM_FLAGS + 0x69)
#define FLAG_SYS_ARENA_SILVER                       (SYSTEM_FLAGS + 0x6A)
#define FLAG_SYS_ARENA_GOLD                         (SYSTEM_FLAGS + 0x6B)
#define FLAG_SYS_FACTORY_SILVER                     (SYSTEM_FLAGS + 0x6C)
#define FLAG_SYS_FACTORY_GOLD                       (SYSTEM_FLAGS + 0x6D)
#define FLAG_SYS_PIKE_SILVER                        (SYSTEM_FLAGS + 0x6E)
#define FLAG_SYS_PIKE_GOLD                          (SYSTEM_FLAGS + 0x6F)
#define FLAG_SYS_PYRAMID_SILVER                     (SYSTEM_FLAGS + 0x70)
#define FLAG_SYS_PYRAMID_GOLD                       (SYSTEM_FLAGS + 0x71)
#define FLAG_SYS_FRONTIER_PASS                      (SYSTEM_FLAGS + 0x72)

#define FLAG_MAP_SCRIPT_CHECKED_DEOXYS              (SYSTEM_FLAGS + 0x73)
#define FLAG_DEOXYS_ROCK_COMPLETE                   (SYSTEM_FLAGS + 0x74)
#define FLAG_ENABLE_SHIP_BIRTH_ISLAND               (SYSTEM_FLAGS + 0x75)
#define FLAG_ENABLE_SHIP_FARAWAY_ISLAND             (SYSTEM_FLAGS + 0x76)

#define FLAG_SHOWN_BOX_WAS_FULL_MESSAGE             (SYSTEM_FLAGS + 0x77)

#define FLAG_ARRIVED_ON_FARAWAY_ISLAND              (SYSTEM_FLAGS + 0x78)
#define FLAG_ARRIVED_AT_MARINE_CAVE_EMERGE_SPOT     (SYSTEM_FLAGS + 0x79)
#define FLAG_ARRIVED_AT_TERRA_CAVE_ENTRANCE         (SYSTEM_FLAGS + 0x7A)

#define FLAG_SYS_MYSTERY_GIFT_ENABLE                (SYSTEM_FLAGS + 0x7B)

#define FLAG_ENTERED_MIRAGE_TOWER                   (SYSTEM_FLAGS + 0x7C)
#define FLAG_LANDMARK_ALTERING_CAVE                 (SYSTEM_FLAGS + 0x7D)
#define FLAG_LANDMARK_DESERT_UNDERPASS              (SYSTEM_FLAGS + 0x7E)
#define FLAG_LANDMARK_ARTISAN_CAVE                  (SYSTEM_FLAGS + 0x7F)
#define FLAG_ENABLE_SHIP_NAVEL_ROCK                 (SYSTEM_FLAGS + 0x80)
#define FLAG_ARRIVED_AT_NAVEL_ROCK                  (SYSTEM_FLAGS + 0x81)
#define FLAG_LANDMARK_TRAINER_HILL                  (SYSTEM_FLAGS + 0x82)

#define FLAG_UNUSED_0x8E3                           (SYSTEM_FLAGS + 0x83) // Unused Flag

#define FLAG_RECEIVED_POKEDEX_FROM_BIRCH            (SYSTEM_FLAGS + 0x84)

#define FLAG_UNUSED_0x8E5                           (SYSTEM_FLAGS + 0x85) // Unused Flag
#define FLAG_UNUSED_0x8E6                           (SYSTEM_FLAGS + 0x86) // Unused Flag
#define FLAG_UNUSED_0x8E7                           (SYSTEM_FLAGS + 0x87) // Unused Flag
#define FLAG_UNUSED_0x8E8                           (SYSTEM_FLAGS + 0x88) // Unused Flag
#define FLAG_UNUSED_0x8E9                           (SYSTEM_FLAGS + 0x89) // Unused Flag
#define FLAG_UNUSED_0x8EA                           (SYSTEM_FLAGS + 0x8A) // Unused Flag
#define FLAG_UNUSED_0x8EB                           (SYSTEM_FLAGS + 0x8B) // Unused Flag
#define FLAG_UNUSED_0x8EC                           (SYSTEM_FLAGS + 0x8C) // Unused Flag
#define FLAG_UNUSED_0x8ED                           (SYSTEM_FLAGS + 0x8D) // Unused Flag
#define FLAG_UNUSED_0x8EE                           (SYSTEM_FLAGS + 0x8E) // Unused Flag
#define FLAG_UNUSED_0x8EF                           (SYSTEM_FLAGS + 0x8F) // Unused Flag
#define FLAG_UNUSED_0x8F0                           (SYSTEM_FLAGS + 0x90) // Unused Flag
#define FLAG_UNUSED_0x8F1                           (SYSTEM_FLAGS + 0x91) // Unused Flag
#define FLAG_UNUSED_0x8F2                           (SYSTEM_FLAGS + 0x92) // Unused Flag
#define FLAG_UNUSED_0x8F3                           (SYSTEM_FLAGS + 0x93) // Unused Flag
#define FLAG_UNUSED_0x8F4                           (SYSTEM_FLAGS + 0x94) // Unused Flag
#define FLAG_UNUSED_0x8F5                           (SYSTEM_FLAGS + 0x95) // Unused Flag
#define FLAG_UNUSED_0x8F6                           (SYSTEM_FLAGS + 0x96) // Unused Flag
#define FLAG_UNUSED_0x8F7                           (SYSTEM_FLAGS + 0x97) // Unused Flag
#define FLAG_UNUSED_0x8F8                           (SYSTEM_FLAGS + 0x98) // Unused Flag
#define FLAG_UNUSED_0x8F9                           (SYSTEM_FLAGS + 0x99) // Unused Flag
#define FLAG_UNUSED_0x8FA                           (SYSTEM_FLAGS + 0x9A) // Unused Flag
#define FLAG_UNUSED_0x8FB                           (SYSTEM_FLAGS + 0x9B) // Unused Flag
#define FLAG_UNUSED_0x8FC                           (SYSTEM_FLAGS + 0x9C) // Unused Flag
#define FLAG_UNUSED_0x8FD                           (SYSTEM_FLAGS + 0x9D) // Unused Flag
#define FLAG_UNUSED_0x8FE                           (SYSTEM_FLAGS + 0x9E) // Unused Flag
#define FLAG_UNUSED_0x8FF                           (SYSTEM_FLAGS + 0x9F) // Unused Flag
#define FLAG_UNUSED_0x900                           (SYSTEM_FLAGS + 0xA0) // Unused Flag
#define FLAG_UNUSED_0x901                           (SYSTEM_FLAGS + 0xA1) // Unused Flag
#define FLAG_UNUSED_0x902                           (SYSTEM_FLAGS + 0xA2) // Unused Flag
#define FLAG_UNUSED_0x903                           (SYSTEM_FLAGS + 0xA3) // Unused Flag
#define FLAG_UNUSED_0x904                           (SYSTEM_FLAGS + 0xA4) // Unused Flag
#define FLAG_UNUSED_0x905                           (SYSTEM_FLAGS + 0xA5) // Unused Flag
#define FLAG_UNUSED_0x906                           (SYSTEM_FLAGS + 0xA6) // Unused Flag
#define FLAG_UNUSED_0x907                           (SYSTEM_FLAGS + 0xA7) // Unused Flag
#define FLAG_UNUSED_0x908                           (SYSTEM_FLAGS + 0xA8) // Unused Flag
#define FLAG_UNUSED_0x909                           (SYSTEM_FLAGS + 0xA9) // Unused Flag
#define FLAG_UNUSED_0x90A                           (SYSTEM_FLAGS + 0xAA) // Unused Flag
#define FLAG_UNUSED_0x90B                           (SYSTEM_FLAGS + 0xAB) // Unused Flag
#define FLAG_UNUSED_0x90C                           (SYSTEM_FLAGS + 0xAC) // Unused Flag
#define FLAG_UNUSED_0x90D                           (SYSTEM_FLAGS + 0xAD) // Unused Flag
#define FLAG_UNUSED_0x90E                           (SYSTEM_FLAGS + 0xAE) // Unused Flag
#define FLAG_UNUSED_0x90F                           (SYSTEM_FLAGS + 0xAF) // Unused Flag
#define FLAG_UNUSED_0x910                           (SYSTEM_FLAGS + 0xB0) // Unused Flag
#define FLAG_UNUSED_0x911                           (SYSTEM_FLAGS + 0xB1) // Unused Flag
#define FLAG_UNUSED_0x912                           (SYSTEM_FLAGS + 0xB2) // Unused Flag
#define FLAG_UNUSED_0x913                           (SYSTEM_FLAGS + 0xB3) // Unused Flag
#define FLAG_UNUSED_0x914                           (SYSTEM_FLAGS + 0xB4) // Unused Flag
#define FLAG_UNUSED_0x915                           (SYSTEM_FLAGS + 0xB5) // Unused Flag
#define FLAG_UNUSED_0x916                           (SYSTEM_FLAGS + 0xB6) // Unused Flag
#define FLAG_UNUSED_0x917                           (SYSTEM_FLAGS + 0xB7) // Unused Flag
#define FLAG_UNUSED_0x918                           (SYSTEM_FLAGS + 0xB8) // Unused Flag
#define FLAG_UNUSED_0x919                           (SYSTEM_FLAGS + 0xB9) // Unused Flag
#define FLAG_UNUSED_0x91A                           (SYSTEM_FLAGS + 0xBA) // Unused Flag
#define FLAG_UNUSED_0x91B                           (SYSTEM_FLAGS + 0xBB) // Unused Flag
#define FLAG_UNUSED_0x91C                           (SYSTEM_FLAGS + 0xBC) // Unused Flag
#define FLAG_UNUSED_0x91D                           (SYSTEM_FLAGS + 0xBD) // Unused Flag
#define FLAG_UNUSED_0x91E                           (SYSTEM_FLAGS + 0xBE) // Unused Flag
#define FLAG_UNUSED_0x91F                           (SYSTEM_FLAGS + 0xBF) // Unused Flag

// Daily Flags
// These flags are cleared once per day
// The start and end are byte-aligned because the flags are cleared in byte increments
#define DAILY_FLAGS_START                           (FLAG_UNUSED_0x91F + (8 - FLAG_UNUSED_0x91F % 8))
#define FLAG_UNUSED_0x920                           (DAILY_FLAGS_START + 0x0)  // Unused Flag
#define FLAG_DAILY_CONTEST_LOBBY_RECEIVED_BERRY     (DAILY_FLAGS_START + 0x1)
#define FLAG_DAILY_SECRET_BASE                      (DAILY_FLAGS_START + 0x2)
#define FLAG_UNUSED_0x923                           (DAILY_FLAGS_START + 0x3)  // Unused Flag
#define FLAG_UNUSED_0x924                           (DAILY_FLAGS_START + 0x4)  // Unused Flag
#define FLAG_UNUSED_0x925                           (DAILY_FLAGS_START + 0x5)  // Unused Flag
#define FLAG_UNUSED_0x926                           (DAILY_FLAGS_START + 0x6)  // Unused Flag
#define FLAG_UNUSED_0x927                           (DAILY_FLAGS_START + 0x7)  // Unused Flag
#define FLAG_UNUSED_0x928                           (DAILY_FLAGS_START + 0x8)  // Unused Flag
#define FLAG_UNUSED_0x929                           (DAILY_FLAGS_START + 0x9)  // Unused Flag
#define FLAG_DAILY_PICKED_LOTO_TICKET               (DAILY_FLAGS_START + 0xA)
#define FLAG_DAILY_ROUTE_114_RECEIVED_BERRY         (DAILY_FLAGS_START + 0xB)
#define FLAG_DAILY_ROUTE_111_RECEIVED_BERRY         (DAILY_FLAGS_START + 0xC)
#define FLAG_DAILY_BERRY_MASTER_RECEIVED_BERRY      (DAILY_FLAGS_START + 0xD)
#define FLAG_DAILY_ROUTE_120_RECEIVED_BERRY         (DAILY_FLAGS_START + 0xE)
#define FLAG_DAILY_LILYCOVE_RECEIVED_BERRY          (DAILY_FLAGS_START + 0xF)
#define FLAG_DAILY_FLOWER_SHOP_RECEIVED_BERRY       (DAILY_FLAGS_START + 0x10)
#define FLAG_DAILY_BERRY_MASTERS_WIFE               (DAILY_FLAGS_START + 0x11)
#define FLAG_DAILY_SOOTOPOLIS_RECEIVED_BERRY        (DAILY_FLAGS_START + 0x12)
#define FLAG_UNUSED_0x933                           (DAILY_FLAGS_START + 0x13) // Unused Flag
#define FLAG_DAILY_APPRENTICE_LEAVES                (DAILY_FLAGS_START + 0x14)

#define FLAG_UNUSED_0x935                           (DAILY_FLAGS_START + 0x15) // Unused Flag
#define FLAG_UNUSED_0x936                           (DAILY_FLAGS_START + 0x16) // Unused Flag
#define FLAG_UNUSED_0x937                           (DAILY_FLAGS_START + 0x17) // Unused Flag
#define FLAG_UNUSED_0x938                           (DAILY_FLAGS_START + 0x18) // Unused Flag
#define FLAG_UNUSED_0x939                           (DAILY_FLAGS_START + 0x19) // Unused Flag
#define FLAG_UNUSED_0x93A                           (DAILY_FLAGS_START + 0x1A) // Unused Flag
#define FLAG_UNUSED_0x93B                           (DAILY_FLAGS_START + 0x1B) // Unused Flag
#define FLAG_UNUSED_0x93C                           (DAILY_FLAGS_START + 0x1C) // Unused Flag
#define FLAG_UNUSED_0x93D                           (DAILY_FLAGS_START + 0x1D) // Unused Flag
#define FLAG_UNUSED_0x93E                           (DAILY_FLAGS_START + 0x1E) // Unused Flag
#define FLAG_UNUSED_0x93F                           (DAILY_FLAGS_START + 0x1F) // Unused Flag
#define FLAG_UNUSED_0x940                           (DAILY_FLAGS_START + 0x20) // Unused Flag
#define FLAG_UNUSED_0x941                           (DAILY_FLAGS_START + 0x21) // Unused Flag
#define FLAG_UNUSED_0x942                           (DAILY_FLAGS_START + 0x22) // Unused Flag
#define FLAG_UNUSED_0x943                           (DAILY_FLAGS_START + 0x23) // Unused Flag
#define FLAG_UNUSED_0x944                           (DAILY_FLAGS_START + 0x24) // Unused Flag
#define FLAG_UNUSED_0x945                           (DAILY_FLAGS_START + 0x25) // Unused Flag
#define FLAG_UNUSED_0x946                           (DAILY_FLAGS_START + 0x26) // Unused Flag
#define FLAG_UNUSED_0x947                           (DAILY_FLAGS_START + 0x27) // Unused Flag
#define FLAG_UNUSED_0x948                           (DAILY_FLAGS_START + 0x28) // Unused Flag
#define FLAG_UNUSED_0x949                           (DAILY_FLAGS_START + 0x29) // Unused Flag
#define FLAG_UNUSED_0x94A                           (DAILY_FLAGS_START + 0x2A) // Unused Flag
#define FLAG_UNUSED_0x94B                           (DAILY_FLAGS_START + 0x2B) // Unused Flag
#define FLAG_UNUSED_0x94C                           (DAILY_FLAGS_START + 0x2C) // Unused Flag
#define FLAG_UNUSED_0x94D                           (DAILY_FLAGS_START + 0x2D) // Unused Flag
#define FLAG_UNUSED_0x94E                           (DAILY_FLAGS_START + 0x2E) // Unused Flag
#define FLAG_UNUSED_0x94F                           (DAILY_FLAGS_START + 0x2F) // Unused Flag
#define FLAG_UNUSED_0x950                           (DAILY_FLAGS_START + 0x30) // Unused Flag
#define FLAG_UNUSED_0x951                           (DAILY_FLAGS_START + 0x31) // Unused Flag
#define FLAG_UNUSED_0x952                           (DAILY_FLAGS_START + 0x32) // Unused Flag
#define FLAG_UNUSED_0x953                           (DAILY_FLAGS_START + 0x33) // Unused Flag
#define FLAG_UNUSED_0x954                           (DAILY_FLAGS_START + 0x34) // Unused Flag
#define FLAG_UNUSED_0x955                           (DAILY_FLAGS_START + 0x35) // Unused Flag
#define FLAG_UNUSED_0x956                           (DAILY_FLAGS_START + 0x36) // Unused Flag
#define FLAG_UNUSED_0x957                           (DAILY_FLAGS_START + 0x37) // Unused Flag
#define FLAG_UNUSED_0x958                           (DAILY_FLAGS_START + 0x38) // Unused Flag
#define FLAG_UNUSED_0x959                           (DAILY_FLAGS_START + 0x39) // Unused Flag
#define FLAG_UNUSED_0x95A                           (DAILY_FLAGS_START + 0x3A) // Unused Flag
#define FLAG_UNUSED_0x95B                           (DAILY_FLAGS_START + 0x3B) // Unused Flag
#define FLAG_UNUSED_0x95C                           (DAILY_FLAGS_START + 0x3C) // Unused Flag
#define FLAG_UNUSED_0x95D                           (DAILY_FLAGS_START + 0x3D) // Unused Flag
#define FLAG_UNUSED_0x95E                           (DAILY_FLAGS_START + 0x3E) // Unused Flag
#define FLAG_UNUSED_0x95F                           (DAILY_FLAGS_START + 0x3F) // Unused Flag
#define DAILY_FLAGS_END                             (FLAG_UNUSED_0x95F + (7 - FLAG_UNUSED_0x95F % 8))
#define NUM_DAILY_FLAGS                             (DAILY_FLAGS_END - DAILY_FLAGS_START + 1)

#define FLAGS_COUNT (DAILY_FLAGS_END + 1)

// Special Flags (Stored in EWRAM (sSpecialFlags), not in the SaveBlock)
#define SPECIAL_FLAGS_START                     0x4000
#define FLAG_HIDE_MAP_NAME_POPUP                (SPECIAL_FLAGS_START + 0x0)
#define FLAG_DONT_TRANSITION_MUSIC              (SPECIAL_FLAGS_START + 0x1)
#define FLAG_ENABLE_MULTI_CORRIDOR_DOOR         (SPECIAL_FLAGS_START + 0x2)
#define FLAG_SPECIAL_FLAG_UNUSED_0x4003         (SPECIAL_FLAGS_START + 0x3) // Unused Flag
#define FLAG_STORING_ITEMS_IN_PYRAMID_BAG       (SPECIAL_FLAGS_START + 0x4)
#define FLAG_SAFE_FOLLOWER_MOVEMENT             (SPECIAL_FLAGS_START + 0x5) // When set, applymovement does not put the follower inside a pokeball
                                                                            // Also, scripted movements on the player will move follower(s), too
// FLAG_SPECIAL_FLAG_0x4005 - 0x407F also exist and are unused
#define SPECIAL_FLAGS_END                       (SPECIAL_FLAGS_START + 0x7F)
#define NUM_SPECIAL_FLAGS                       (SPECIAL_FLAGS_END - SPECIAL_FLAGS_START + 1)

// Ichor flag bank. These flags are saved in IchorSave (SaveBlock3), not in
// SaveBlock1: GetFlagPointer (src/event_data.c) sends ids 0x2000-0x28FF there.
// Scripts use them like any flag. Each range below is a run of bits the engine
// also counts (Ichor_CountFlags); the general ranges are claimed by name with
//   python3 tools/ichor/claim.py bankflag FLAG_ICHOR_<NAME> "comment"
//   python3 tools/ichor/claim.py dailyflag FLAG_DAILY_ICHOR_<NAME> "comment"
// See design/ENGINE_API.md. Both starts must stay multiples of 8.
#define ICHOR_FLAGS_START                       0x2000
#define ICHOR_FLAGS_COUNT                       2048
#define ICHOR_FLAGS_END                         (ICHOR_FLAGS_START + ICHOR_FLAGS_COUNT - 1)

#define FLAG_ICHOR_RELICS_START                 (ICHOR_FLAGS_START + 0x000) // 64: relics, upgrades, relic state (SYSTEMS §1)
#define FLAG_ICHOR_HERMS_START                  (ICHOR_FLAGS_START + 0x040) // 32 great herms (§4)
#define FLAG_ICHOR_CONSTELLATIONS_START         (ICHOR_FLAGS_START + 0x060) // 32: the 24 constellations (§8)
#define FLAG_ICHOR_SHERDS_START                 (ICHOR_FLAGS_START + 0x080) // 48 potsherds, 4 per amphora (§5)
#define FLAG_ICHOR_AMPHORAE_START               (ICHOR_FLAGS_START + 0x0B0) // 16: amphorae finished at the Akademia
#define FLAG_ICHOR_OSTRAKA_START                (ICHOR_FLAGS_START + 0x0C0) // 32: the 30 ostraka
#define FLAG_ICHOR_PROPHECY_START               (ICHOR_FLAGS_START + 0x0E0) // 16: the 8 prophecy tablets
#define FLAG_ICHOR_PAGES_START                  (ICHOR_FLAGS_START + 0x0F0) // 16: Daedalus's 7 pages (LABYRINTH.md)
#define FLAG_ICHOR_BRAZIERS_START               (ICHOR_FLAGS_START + 0x100) // 256 lit braziers and lit zones (§2)
#define FLAG_ICHOR_GIFTS_START                  (ICHOR_FLAGS_START + 0x200) // 64: 4 per god slot, gifts I, II, III and the Hierophant's offering (§3)
#define FLAG_ICHOR_ALTARS_START                 (ICHOR_FLAGS_START + 0x240) // 32 cleansed desecrated altars (§3)
#define FLAG_ICHOR_DIG_FIXED_START              (ICHOR_FLAGS_START + 0x260) // 64 one-time dig finds (§5)
#define FLAG_ICHOR_THEOXENIA_START              (ICHOR_FLAGS_START + 0x2A0) // 64: visits, hides and decoys (§10)
#define FLAG_ICHOR_XENIA_START                  (ICHOR_FLAGS_START + 0x2E0) // 32: hosts and token-chain links (§10)
#define FLAG_ICHOR_GENERAL_START                (ICHOR_FLAGS_START + 0x300) // 1,280 claimed by name, below
#define FLAG_ICHOR_GENERAL_COUNT                (ICHOR_FLAGS_COUNT - 0x300)
// The travel herms' 32 registration flags (§4), claimed by name below as
// FLAG_ICHOR_TOWN_HERM_<TOWN> in the engine's offsets 0x4A0-0x4BF, one per TOWN_HERM_* id.
#define FLAG_ICHOR_TOWN_HERMS_START             (FLAG_ICHOR_GENERAL_START + 0x4A0)

// The second bank (IchorSave.flags2, version 4), past the daily bank.
// claim.py bankflag's offsets 0x500-0xADF land in its general range.
#define ICHOR_FLAGS2_START                      0x2900
#define ICHOR_FLAGS2_COUNT                      1536
#define ICHOR_FLAGS2_END                        (ICHOR_FLAGS2_START + ICHOR_FLAGS2_COUNT - 1)
#define FLAG_ICHOR_GENERAL2_START               (ICHOR_FLAGS2_START + 0x000) // 1,504 claimed by name
#define FLAG_ICHOR_GENERAL2_COUNT               0x5E0
#define FLAG_ICHOR_WAYSTONES_START              (ICHOR_FLAGS2_START + 0x5E0) // 32: the Oikoumene's waystones (herms beyond Aethos)

// Hidden items with bank flags: their 13-bit flag field (asm/macros/map.inc)
// holds 0x1000 + (flag - ICHOR_FLAGS_START); below 0x1000 it is a vanilla flag's
// offset from FLAG_HIDDEN_ITEMS_START.
#define ICHOR_HIDDEN_ITEM_BANK_ID               0x1000

// The relics (SYSTEMS §1). Each FLAG_ICHOR_GOT_* is set whenever its item
// enters the bag. They sit at FLAG_ICHOR_RELICS_START + (item - ITEM_TALARIA);
// the Talaria's is the slice's FLAG_SYS_B_DASH instead.
#define FLAG_ICHOR_GOT_TALARIA                  FLAG_SYS_B_DASH
#define FLAG_ICHOR_GOT_BRONZE_HAMMER            (FLAG_ICHOR_RELICS_START + 0x01)
#define FLAG_ICHOR_GOT_HECATES_TORCH            (FLAG_ICHOR_RELICS_START + 0x02)
#define FLAG_ICHOR_GOT_DEMETERS_SICKLE          (FLAG_ICHOR_RELICS_START + 0x03)
#define FLAG_ICHOR_GOT_GIRDLE_OF_HERAKLES       (FLAG_ICHOR_RELICS_START + 0x04)
#define FLAG_ICHOR_GOT_POSEIDONS_CONCH          (FLAG_ICHOR_RELICS_START + 0x05)
#define FLAG_ICHOR_GOT_DAEDALUS_WINGS           (FLAG_ICHOR_RELICS_START + 0x06)
#define FLAG_ICHOR_GOT_HORN_OF_ACHELOUS         (FLAG_ICHOR_RELICS_START + 0x07)
#define FLAG_ICHOR_GOT_ARIADNES_THREAD          (FLAG_ICHOR_RELICS_START + 0x08)
#define FLAG_ICHOR_GOT_LABRYS                   (FLAG_ICHOR_RELICS_START + 0x09)
#define FLAG_ICHOR_GOT_HELM_OF_DARKNESS         (FLAG_ICHOR_RELICS_START + 0x0A)
#define FLAG_ICHOR_GOT_NEREID_PEARL             (FLAG_ICHOR_RELICS_START + 0x0B)
#define FLAG_ICHOR_GOT_AEOLUS_BAG               (FLAG_ICHOR_RELICS_START + 0x0C)
// upgrades, from the rites' gift II
#define FLAG_ICHOR_WINGED_TALARIA               (FLAG_ICHOR_RELICS_START + 0x20) // Hermes: leap one-tile gaps
#define FLAG_ICHOR_THREE_FLAMED_TORCH           (FLAG_ICHOR_RELICS_START + 0x21) // Hecate: wider light, burns thornwebs
#define FLAG_ICHOR_HEPHAESTUS_HAMMER            (FLAG_ICHOR_RELICS_START + 0x22) // Hephaestus: great boulders
#define FLAG_ICHOR_TRITON_CONCH                 (FLAG_ICHOR_RELICS_START + 0x23) // Poseidon: calms whirlpools (post-game)
#define FLAG_ICHOR_HELM_OF_HADES                (FLAG_ICHOR_RELICS_START + 0x24) // Hades: works in shadow by day (post-game)
// state
#define FLAG_ICHOR_TORCH_DOUSED                 (FLAG_ICHOR_RELICS_START + 0x30) // the torch is out (Relic Ring)
#define FLAG_ICHOR_HELM_ON                      (FLAG_ICHOR_RELICS_START + 0x31) // the Helm of Darkness is worn
#define FLAG_ICHOR_NO_RELICS                    (FLAG_ICHOR_RELICS_START + 0x32) // set in ON_TRANSITION: no relics here; cleared on every map change
// gift II upgrades that aren't relics (SYSTEMS §3)
#define FLAG_ICHOR_EVER_EMBER                   (FLAG_ICHOR_RELICS_START + 0x25) // Hestia: Hearthfire never counts down; hearths heal
#define FLAG_ICHOR_HARVEST_BASKET               (FLAG_ICHOR_RELICS_START + 0x26) // Demeter: berry trees always give one more
#define FLAG_ICHOR_THYRSUS                      (FLAG_ICHOR_RELICS_START + 0x27) // Dionysus: climb marked ivy walls (Rock Climb)
#define FLAG_ICHOR_HUNTERS_MOON                 (FLAG_ICHOR_RELICS_START + 0x28) // Artemis: the Augur's Eye lists rare slots (hook)
#define FLAG_ICHOR_ATHENAS_STYLUS               (FLAG_ICHOR_RELICS_START + 0x29) // Athena: Scroll of Deeds hints (hook)
#define FLAG_ICHOR_EYES_OF_ARGUS                (FLAG_ICHOR_RELICS_START + 0x2A) // Hera: the Augur's Eye detector always on (hook)

// The rites' gifts: god g's gift I, II, III and the Hierophant's offering
#define FLAG_ICHOR_GIFT(god, n)                 (FLAG_ICHOR_GIFTS_START + 4 * (god) + (n))
#define ICHOR_GIFT_I                            0
#define ICHOR_GIFT_II                           1
#define ICHOR_GIFT_III                          2
#define ICHOR_GIFT_HIEROPHANT                   3
#define FLAG_ICHOR_ALL_HERMS_REWARD             (FLAG_ICHOR_GIFTS_START + 4 * 0 + 0) // god slot 0 (none) is free: the all-herms bonus
// Ichor bank flags: claim.py bankflag adds lines here, in order.
#define FLAG_ICHOR_SAW_ROCKSLIDE                (FLAG_ICHOR_GENERAL_START + 0x000) // Ichor: Route 4: beat 17's first scene played (Alethea at the slide)
#define FLAG_ICHOR_ROCKSLIDE_CLEARED            (FLAG_ICHOR_GENERAL_START + 0x001) // Ichor: Route 4: beat 17, the three heaps broken, the slide cleared
#define FLAG_ICHOR_GOT_PROCESSION_BARLEY        (FLAG_ICHOR_GENERAL_START + 0x002) // Ichor: Route 4: beat 17, Eudemos's two Barley Cakes
#define FLAG_ICHOR_HIDE_ROCKSLIDE_1             (FLAG_ICHOR_GENERAL_START + 0x003) // Ichor: Route 4: the slide's first heap, broken (its object's hide flag)
#define FLAG_ICHOR_HIDE_ROCKSLIDE_2             (FLAG_ICHOR_GENERAL_START + 0x004) // Ichor: Route 4: the slide's second heap, broken
#define FLAG_ICHOR_HIDE_ROCKSLIDE_3             (FLAG_ICHOR_GENERAL_START + 0x005) // Ichor: Route 4: the slide's third heap, broken
#define FLAG_ICHOR_HIDE_PROCESSION_ROUTE4       (FLAG_ICHOR_GENERAL_START + 0x006) // Ichor: Route 4: the procession's camp struck after the slide clears (SCRIPT.md's _ROUTE2; Alethea goes with it)
#define FLAG_ICHOR_HIDE_GRUNT_LAAS              (FLAG_ICHOR_GENERAL_START + 0x007) // Ichor: Route 4: the herm's Titanborn guard ran off
#define FLAG_ICHOR_HIDE_THICKET_ROUTE4          (FLAG_ICHOR_GENERAL_START + 0x008) // Ichor: Route 4: the orchard's thorn thicket cut (Demeter's Sickle)
#define FLAG_ICHOR_ITEM_ROUTE4_POTION           (FLAG_ICHOR_GENERAL_START + 0x009) // Ichor: Route 4: Potion by the kilns
#define FLAG_ICHOR_ITEM_ROUTE4_REPEL            (FLAG_ICHOR_GENERAL_START + 0x00A) // Ichor: Route 4: Repel in the walled grave plot
#define FLAG_ICHOR_ITEM_ROUTE4_SUPER_POTION     (FLAG_ICHOR_GENERAL_START + 0x00B) // Ichor: Route 4: Super Potion up the hill spur
#define FLAG_ICHOR_ITEM_ROUTE4_TM_ROCK_TOMB     (FLAG_ICHOR_GENERAL_START + 0x00C) // Ichor: Route 4: TM39 Rock Tomb under the slide's last heap
#define FLAG_ICHOR_ITEM_ROUTE4_REVIVE           (FLAG_ICHOR_GENERAL_START + 0x00D) // Ichor: Route 4: Revive in the family tomb (the Girdle)
#define FLAG_ICHOR_ITEM_ROUTE4_SUN_STONE        (FLAG_ICHOR_GENERAL_START + 0x00E) // Ichor: Route 4: Sun Stone in the terrace orchard (the Sickle)
#define FLAG_ICHOR_ITEM_ROUTE4_GREAT_BALL       (FLAG_ICHOR_GENERAL_START + 0x00F) // Ichor: Route 4: Great Ball in the woods clearing (the Hammer)
#define FLAG_ICHOR_ITEM_ROUTE4_SPELL_TAG        (FLAG_ICHOR_GENERAL_START + 0x010) // Ichor: Route 4: Spell Tag at Hecate's crossroads shrine in the glade
#define FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA        (FLAG_ICHOR_GENERAL_START + 0x011) // Ichor: Kleon left Eleusa after the sanctum theft
#define FLAG_ICHOR_DAPHNE_REVELATION            (FLAG_ICHOR_GENERAL_START + 0x012) // Ichor: Daphne explained the Unwoven and gave the Star Chart
#define FLAG_ICHOR_GOT_STAR_CHART               (FLAG_ICHOR_GENERAL_START + 0x013) // Ichor: received the Star Chart at Eleusa
#define FLAG_ICHOR_ACT1_COMPLETE                (FLAG_ICHOR_GENERAL_START + 0x014) // Ichor: completed the Unwoven act
#define FLAG_ICHOR_HIDE_DAPHNE_ELEUSA           (FLAG_ICHOR_GENERAL_START + 0x015) // Ichor: Daphne absent from the Telesterion
#define FLAG_ICHOR_HIDE_ALETHEA_ELEUSA          (FLAG_ICHOR_GENERAL_START + 0x016) // Ichor: Alethea absent from Eleusa village
#define FLAG_ICHOR_HIDE_ALETHEA_REVELATION      (FLAG_ICHOR_GENERAL_START + 0x017) // Ichor: Alethea absent from the revelation scene
#define FLAG_ICHOR_ELEUSA_VINES_WEST_CUT        (FLAG_ICHOR_GENERAL_START + 0x018) // Ichor: cut the west vines on the Eleutherai road
#define FLAG_ICHOR_ELEUSA_VINES_MIDWEST_CUT     (FLAG_ICHOR_GENERAL_START + 0x019) // Ichor: cut the middle-west vines on the Eleutherai road
#define FLAG_ICHOR_ELEUSA_VINES_MIDEAST_CUT     (FLAG_ICHOR_GENERAL_START + 0x01A) // Ichor: cut the middle-east vines on the Eleutherai road
#define FLAG_ICHOR_ELEUSA_VINES_EAST_CUT        (FLAG_ICHOR_GENERAL_START + 0x01B) // Ichor: cut the east vines on the Eleutherai road
#define FLAG_ICHOR_LEFT_ELEUSA_WITH_ALETHEA     (FLAG_ICHOR_GENERAL_START + 0x01C) // Ichor: passed the Eleutherai vines with Alethea after Act I
#define FLAG_ICHOR_MYRTALE_PRIZE_PENDING        (FLAG_ICHOR_GENERAL_START + 0x01D) // Ichor: Myrtale owes the first-win Fling scroll until the Bag has room
#define FLAG_ICHOR_HIDE_OMEN_NEMECUB            (FLAG_ICHOR_GENERAL_START + 0x01E) // Ichor: Isthmus hill-spur visitor; hidden after capture or defeat
#define FLAG_ICHOR_DIFFICULTY_CHOSEN            (FLAG_ICHOR_GENERAL_START + 0x01F) // Ichor: Mortal, Hero or Spartan selected before leaving the bedroom
#define FLAG_ICHOR_HECATES_HOUND                (FLAG_ICHOR_GENERAL_START + 0x020) // Ichor: beat 18: Hecate's hound (Lykopup, static, night) at the Hekataion caught or beaten
#define FLAG_ICHOR_HOLLOW_RAKNIT                (FLAG_ICHOR_GENERAL_START + 0x021) // Ichor: Hecate's Hollow: the web chamber's Raknit (static, after the Arachne amphora) caught or beaten
#define FLAG_ICHOR_MET_HOLLOW_CRONE             (FLAG_ICHOR_GENERAL_START + 0x022) // Ichor: beat 18: heard the old woman out at Hecate's Hollow's east mouth
#define FLAG_ICHOR_GOT_HEKABE_SUPPER            (FLAG_ICHOR_GENERAL_START + 0x023) // Ichor: Hecate's Hollow: Hekabe's Barley Cake, after her battle
#define FLAG_ICHOR_HIDE_HOLLOW_WEB_WEST         (FLAG_ICHOR_GENERAL_START + 0x024) // Ichor: Hecate's Hollow: the cobweb on the road west, burnt (hides its two objects)
#define FLAG_ICHOR_HIDE_HOLLOW_WEB_CHAMBER      (FLAG_ICHOR_GENERAL_START + 0x025) // Ichor: Hecate's Hollow: the web chamber's cobweb, burnt
#define FLAG_ICHOR_HIDE_HOLLOW_WEB_SHORTCUT     (FLAG_ICHOR_GENERAL_START + 0x026) // Ichor: Hecate's Hollow: the shortcut's cobweb by the east mouth, burnt
#define FLAG_ICHOR_ITEM_HOLLOW_BRONZE_OBOL      (FLAG_ICHOR_GENERAL_START + 0x027) // Ichor: Hecate's Hollow: Bronze Obol (Relic Copper) at fork 2's dead end
#define FLAG_ICHOR_ITEM_HOLLOW_SILK_SCARF       (FLAG_ICHOR_GENERAL_START + 0x028) // Ichor: Hecate's Hollow: Silk Scarf in the web chamber
#define FLAG_ICHOR_ITEM_HOLLOW_ETHER            (FLAG_ICHOR_GENERAL_START + 0x029) // Ichor: Hecate's Hollow: Ether by the second brazier
#define FLAG_ICHOR_ITEM_HOLLOW_DUSK_BALL        (FLAG_ICHOR_GENERAL_START + 0x02A) // Ichor: Hecate's Hollow: Dusk Ball in the shortcut tunnel
#define FLAG_ICHOR_ITEM_HOLLOW_REVIVE           (FLAG_ICHOR_GENERAL_START + 0x02B) // Ichor: Hecate's Hollow: Revive in Kallias's side passage
#define FLAG_ICHOR_GOT_MOMS_HONEY               (FLAG_ICHOR_GENERAL_START + 0x02C) // Ichor: Elaia: received Mom's three Honey after writing home
#define FLAG_ICHOR_HIDE_DAPHNE_AKADEMIA         (FLAG_ICHOR_GENERAL_START + 0x02D) // Ichor: Elaia: Daphne left for the Mysteries on the mainland
#define FLAG_ICHOR_GOT_AMPHORA_PATCH            (FLAG_ICHOR_GENERAL_START + 0x02E) // Ichor: claimed Daphne's twelve-amphora Ability Patch
#define FLAG_ICHOR_KRONION_ALTAR_STONE          (FLAG_ICHOR_GENERAL_START + 0x02F) // Ichor: caught or defeated the Kronos amphora's altar Cairnolith
#define FLAG_ICHOR_ELEUSA_PERSENYX              (FLAG_ICHOR_GENERAL_START + 0x030) // Ichor: caught or defeated the Persephone amphora's field visitor
#define FLAG_ICHOR_HIDE_AMPHORA_PERSENYX        (FLAG_ICHOR_GENERAL_START + 0x031) // Ichor: derived visibility of the dusk-only restored-amphora visitor
#define FLAG_ICHOR_OATH_CHOICE_PENDING          (FLAG_ICHOR_GENERAL_START + 0x032) // Ichor: new game may choose its starting Oath; cleared by either answer
#define FLAG_ICHOR_BOUGHT_CHARIOT               (FLAG_ICHOR_GENERAL_START + 0x033) // Ichor: bought the chariot from Alfred at Waltz Chariots, Emporion
#define FLAG_ICHOR_ITEM_ROUTE5_SUPER_POTION     (FLAG_ICHOR_GENERAL_START + 0x040) // Ichor: Route 5: the Super Potion in the pine clearing
#define FLAG_ICHOR_ITEM_ROUTE5_GREAT_BALL       (FLAG_ICHOR_GENERAL_START + 0x041) // Ichor: Route 5: the Great Ball beside the rock seat
#define FLAG_ICHOR_ITEM_ROUTE5_PP_UP            (FLAG_ICHOR_GENERAL_START + 0x042) // Ichor: Route 5: the PP Up at the watchtower (the Girdle, Act II)
#define FLAG_ICHOR_ITEM_ROUTE5_CALCIUM          (FLAG_ICHOR_GENERAL_START + 0x043) // Ichor: Route 5: the Calcium in the pine hollow (Demeter's Sickle)
#define FLAG_ICHOR_ITEM_ROUTE5_SUPER_REPEL      (FLAG_ICHOR_GENERAL_START + 0x044) // Ichor: Route 5: the Super Repel at the end of the thyme meadow
#define FLAG_ICHOR_ITEM_ROUTE5_REVIVE           (FLAG_ICHOR_GENERAL_START + 0x045) // Ichor: Route 5: the Revive at the terrace's lookout, behind the rubble
#define FLAG_ICHOR_ROUTE5_THICKET_CUT           (FLAG_ICHOR_GENERAL_START + 0x046) // Ichor: Route 5: the pine hollow's thorn thicket is cut (its hide flag)
#define FLAG_ICHOR_ROUTE5_RUBBLE_BROKEN         (FLAG_ICHOR_GENERAL_START + 0x047) // Ichor: Route 5: the lookout's marble rubble is broken (its hide flag)
#define FLAG_ICHOR_GOT_GOOD_ROD                 (FLAG_ICHOR_GENERAL_START + 0x048) // Ichor: Route 5: Aigialeus gave the Good Rod
#define FLAG_ICHOR_TRADED_GELASABLE             (FLAG_ICHOR_GENERAL_START + 0x049) // Ichor: Route 5's inn: traded an Onotis for Xenokles's Gelasable GALANTHIS
#define FLAG_ICHOR_MET_XENOKLES                 (FLAG_ICHOR_GENERAL_START + 0x04A) // Ichor: Route 5's inn: Xenokles's welcome heard
#define FLAG_ICHOR_ITEM_ROUTE5_ETHER            (FLAG_ICHOR_GENERAL_START + 0x04B) // Ichor: Route 5: the Ether at the terrace's east end, past the shepherd
#define FLAG_ICHOR_ITEM_APHAIA_HYPER_POTION     (FLAG_ICHOR_GENERAL_START + 0x060) // Ichor: Aphaia Road: item ball, Hyper Potion at the west meadow's end
#define FLAG_ICHOR_ITEM_APHAIA_LEAF_STONE       (FLAG_ICHOR_GENERAL_START + 0x061) // Ichor: Aphaia Road: item ball, Leaf Stone in the pistachio terrace's far corner
#define FLAG_ICHOR_ITEM_APHAIA_GREAT_BALL       (FLAG_ICHOR_GENERAL_START + 0x062) // Ichor: Temple of Aphaia: item ball, Great Ball in the cypress nook east of the way
#define FLAG_ICHOR_SAFFRON_THREAD               (FLAG_ICHOR_GENERAL_START + 0x070) // Ichor: beat 19: Krokis tied the saffron thread at Eleusa's gate, three times, and it slipped off
#define FLAG_ICHOR_ARRIVED_ELEUSA               (FLAG_ICHOR_GENERAL_START + 0x071) // Ichor: beat 20: first step into Eleusa Village
#define FLAG_ICHOR_VISITED_ELEUSA               (FLAG_ICHOR_GENERAL_START + 0x072) // Ichor: Eleusa visited (fly target)
#define FLAG_ICHOR_HIDE_KLEON_ELEUSA            (FLAG_ICHOR_GENERAL_START + 0x073) // Ichor: hide Kleon in Eleusa's square (beats 20-22; set once the Mysteries begin)
#define FLAG_ICHOR_GOT_TM_GIGA_DRAIN            (FLAG_ICHOR_GENERAL_START + 0x074) // Ichor: beat 21: TM19 Giga Drain from Chloe
#define FLAG_ICHOR_PROCESSION_ARRIVED           (FLAG_ICHOR_GENERAL_START + 0x075) // Ichor: beat 22: the procession reached Eleusa (out of the Telesterion with the Harvest Laurel)
#define FLAG_ICHOR_HIDE_PROCESSION_ELEUSA       (FLAG_ICHOR_GENERAL_START + 0x076) // Ichor: hide the procession in Eleusa: Alethea, Kerykos, Eudemos, the initiates (shown from PROCESSION_ARRIVED until the Mysteries begin)
#define FLAG_ICHOR_MYSTERIES_BEGUN              (FLAG_ICHOR_GENERAL_START + 0x077) // Ichor: beat 22: told Kerykos YES, the doors closed; the night scene plays in the Telesterion
#define FLAG_ICHOR_HIDE_MYSTERIES_CROWD         (FLAG_ICHOR_GENERAL_START + 0x078) // Ichor: hide the Mysteries' congregation in the Telesterion: Kerykos, Alethea, the initiates (shown during beat 22)
#define FLAG_ICHOR_HIDE_TELESTERION_GRUNTS      (FLAG_ICHOR_GENERAL_START + 0x079) // Ichor: hide Psammis and Chersos in the Telesterion (shown only while they climb out, beat 22)
#define FLAG_ICHOR_HIDE_KLEON_TELESTERION       (FLAG_ICHOR_GENERAL_START + 0x07A) // Ichor: hide Kleon in the Telesterion (seated in beat 22, then at the Anaktoron's door until beat 24 sets it)
#define FLAG_ICHOR_MYSTERIES_NIGHT              (FLAG_ICHOR_GENERAL_START + 0x07B) // Ichor: beat 22: the night of the Mysteries played to the end (the raid, the multi battle, the stair)
#define FLAG_ICHOR_TELESTERION_MULTI            (FLAG_ICHOR_GENERAL_START + 0x07C) // Ichor: beat 22: fought the Telesterion's grunts beside Kleon (either outcome)
#define FLAG_ICHOR_TELESTERION_PIT_FALL         (FLAG_ICHOR_GENERAL_START + 0x07D) // Ichor: the Telesterion: fell into a grain pit at least once (Doso's chalk hint)
#define FLAG_ICHOR_ITEM_AEGINA_NET_BALL         (FLAG_ICHOR_GENERAL_START + 0x07E) // Ichor: Aigina Town: Net Ball on the north-west beach
#define FLAG_ICHOR_ITEM_ELEUSA_SUPER_POTION     (FLAG_ICHOR_GENERAL_START + 0x080) // Ichor: Eleusa: the Super Potion on the threshing floor
#define FLAG_ICHOR_ITEM_ELEUSA_AWAKENING        (FLAG_ICHOR_GENERAL_START + 0x081) // Ichor: Eleusa: the Awakening in the poppy meadow
#define FLAG_ICHOR_SANCTUM_OPEN                 (FLAG_ICHOR_GENERAL_START + 0x082) // Ichor: beat 22: the sanctum is open (the Ploutonion's gate and the Anaktoron's stair)
#define FLAG_ICHOR_LESSER_MYSTERIES_DONE        (FLAG_ICHOR_GENERAL_START + 0x083) // Ichor: the Telesterion: the fourth brazier lit, Chloe revealed
#define FLAG_ICHOR_MET_DOSO                     (FLAG_ICHOR_GENERAL_START + 0x084) // Ichor: the Telesterion: Doso's welcome heard
#define FLAG_ICHOR_HIDE_CHLOE_TELESTERION       (FLAG_ICHOR_GENERAL_START + 0x085) // Ichor: the Telesterion: Chloe unseen in the Anaktoron's doorway until the fourth brazier
#define FLAG_ICHOR_HIDE_OMEN_KORANTHA           (FLAG_ICHOR_GENERAL_START + 0x08E) // Ichor: Eleusa's daily flower-crowned visitor; hidden after capture or defeat
#define FLAG_ICHOR_HIDE_OMEN_PITHOUND           (FLAG_ICHOR_GENERAL_START + 0x08F) // Ichor: Emporion's marked-jar visitor; consumed after capture or defeat
#define FLAG_ICHOR_GOT_KYKEON                   (FLAG_ICHOR_GENERAL_START + 0x090) // Ichor: Eleusa: Metaneira gave the goddess's drink, Fresh Water and Barley Cakes, after Laurel 3
#define FLAG_ICHOR_GOT_TM_BULLET_SEED           (FLAG_ICHOR_GENERAL_START + 0x091) // Ichor: Eleusa: Theano gave TM09 Bullet Seed in Dysaules's farmhouse
#define FLAG_ICHOR_GOT_AMULET_COIN              (FLAG_ICHOR_GENERAL_START + 0x092) // Ichor: Eleusa: Sitokles gave the Amulet Coin his family kept by the cold iron, after the theft
#define FLAG_ICHOR_TRADED_PITHOUND              (FLAG_ICHOR_GENERAL_START + 0x093) // Ichor: Eleusa: traded Euphorion a Melibee for his Pithound, CRITIC
#define FLAG_ICHOR_FRAGMENT_STOLEN              (FLAG_ICHOR_GENERAL_START + 0x094) // Ichor: beat 23 (batch 5): the Titans have taken the cold iron from under Eleusa; set by the theft
#define FLAG_ICHOR_MET_METANEIRA                (FLAG_ICHOR_GENERAL_START + 0x095) // Ichor: Eleusa: Metaneira has told you why her family feeds strangers (she says it once)
#define FLAG_ICHOR_SANCTUM_ARRIVED              (FLAG_ICHOR_GENERAL_START + 0x086) // Ichor: beat 23A: the granaries' arrival scene played (Chloe holds the stair, Alethea takes a grunt)
#define FLAG_ICHOR_SANCTUM_VOICE                (FLAG_ICHOR_GENERAL_START + 0x087) // Ichor: beat 23B: Hyperion's voice heard up the Hall of the Kore
#define FLAG_ICHOR_HIDE_HYPERION_SANCTUM        (FLAG_ICHOR_GENERAL_START + 0x089) // Ichor: beat 23C: Hyperion beaten and gone up his tunnel; it caved in behind him
#define FLAG_ICHOR_ITEM_SANCTUM_B1F_HYPER_POTION (FLAG_ICHOR_GENERAL_START + 0x08A) // Ichor: the sanctum, B1F: the Hyper Potion in the side pit Bolos guards
#define FLAG_ICHOR_ITEM_SANCTUM_B2F_TM_DIG      (FLAG_ICHOR_GENERAL_START + 0x08B) // Ichor: the sanctum, B2F: TM28 Dig in Gaios's fresco alcove
#define FLAG_ICHOR_ITEM_SANCTUM_B2F_SUPER_POTION (FLAG_ICHOR_GENERAL_START + 0x08C) // Ichor: the sanctum, B2F: the Super Potion by the second fresco
#define FLAG_ICHOR_ITEM_SANCTUM_B3F_SOFT_SAND   (FLAG_ICHOR_GENERAL_START + 0x08D) // Ichor: the sanctum, B3F: the Soft Sand at the tunnel's mouth
#define FLAG_ICHOR_HERALDS_RUN_DONE             (FLAG_ICHOR_GENERAL_START + 0x0F0) // Ichor: the Herald's Run: the third scroll delivered (beat 15)
#define FLAG_ICHOR_HERMES_HERM_J1               (FLAG_ICHOR_GENERAL_START + 0x0F1) // Ichor: the Herald's Run: junction herm J1 oiled
#define FLAG_ICHOR_HERMES_HERM_J2               (FLAG_ICHOR_GENERAL_START + 0x0F2) // Ichor: the Herald's Run: junction herm J2 oiled
#define FLAG_ICHOR_HERMES_HERM_J3               (FLAG_ICHOR_GENERAL_START + 0x0F3) // Ichor: the Herald's Run: junction herm J3 oiled
#define FLAG_ICHOR_HERMES_HERM_J4               (FLAG_ICHOR_GENERAL_START + 0x0F4) // Ichor: the Herald's Run: junction herm J4 oiled
#define FLAG_ICHOR_GOT_TM_AERIAL_ACE            (FLAG_ICHOR_GENERAL_START + 0x0F5) // Ichor: TM40 Aerial Ace from Kerykos
#define FLAG_ICHOR_HERALDS_RUN_FAILED           (FLAG_ICHOR_GENERAL_START + 0x0F6) // Ichor: the step-glass ran dry once (Angelos's hint)
#define FLAG_ICHOR_HERALDS_RUN_TOLD             (FLAG_ICHOR_GENERAL_START + 0x0F7) // Ichor: Kerykos explained the Herald's Run
#define FLAG_ICHOR_DEIGMA_CLUE                  (FLAG_ICHOR_GENERAL_START + 0x0E0) // Ichor: Emporion: beat 12, Alethea learned of the forty lamps and saw the hook under the seal
#define FLAG_ICHOR_TRADED_NARKERAY              (FLAG_ICHOR_GENERAL_START + 0x0E1) // Ichor: Emporion: traded Thaletas an Onotis for his Narkeray, Socrates
#define FLAG_ICHOR_FORGE_RELIT                  (FLAG_ICHOR_GENERAL_START + 0x0E2) // Ichor: Emporion: beat 13, the Hephaisteion's forge relit from Hestia's coal
#define FLAG_ICHOR_HIRING_HALL                  (FLAG_ICHOR_GENERAL_START + 0x0E4) // Ichor: Emporion: beat the Titans' crew boss in the hiring hall and took his Rocky Helmet
#define FLAG_ICHOR_KNUCKLEBONES_EMPORION        (FLAG_ICHOR_GENERAL_START + 0x0E5) // Ichor: Emporion: Myrtale, the Dolphin's champion, lost her first game of knucklebones to you
#define FLAG_ICHOR_KNUCKLEBONES_STREPSIADES     (FLAG_ICHOR_GENERAL_START + 0x0E6) // Ichor: Emporion: beat Strepsiades at knucklebones (his prize paid)
#define FLAG_ICHOR_KNUCKLEBONES_STRATYLLIS      (FLAG_ICHOR_GENERAL_START + 0x0E7) // Ichor: Emporion: beat Stratyllis at knucklebones (her prize paid)
#define FLAG_ICHOR_PHILOXENOS_LAUREL_2          (FLAG_ICHOR_GENERAL_START + 0x0E8) // Ichor: Emporion: told Philoxenos the story of the Herald Laurel
#define FLAG_ICHOR_PHILOXENOS_LAUREL_3          (FLAG_ICHOR_GENERAL_START + 0x0E9) // Ichor: Emporion: told Philoxenos the story of the Harvest Laurel
#define FLAG_ICHOR_GOT_QUICK_CLAW               (FLAG_ICHOR_GENERAL_START + 0x0EA) // Ichor: Emporion: Dromokleia gave a runner's Quick Claw
#define FLAG_ICHOR_WROTE_TO_MOM                 (FLAG_ICHOR_GENERAL_START + 0x0EB) // Ichor: Emporion: after Act I, the runners took your letter home to Mom
#define FLAG_ICHOR_GOT_WIDOWS_GIFT              (FLAG_ICHOR_GENERAL_START + 0x0EC) // Ichor: Emporion: Penelopeia gave her husband's Sea Incense
#define FLAG_ICHOR_EUPHRONIOS_1                 (FLAG_ICHOR_GENERAL_START + 0x0ED) // Ichor: Emporion: Euphronios painted your Harpeck
#define FLAG_ICHOR_EUPHRONIOS_2                 (FLAG_ICHOR_GENERAL_START + 0x0EE) // Ichor: Emporion: Euphronios painted your Chelonet
#define FLAG_ICHOR_EUPHRONIOS_3                 (FLAG_ICHOR_GENERAL_START + 0x0EF) // Ichor: Emporion: Euphronios painted your Stachyss
#define FLAG_ICHOR_ARRIVED_EMPORION             (FLAG_ICHOR_GENERAL_START + 0x0C0) // Ichor: beat 11: stepped off the Euploia onto Emporion's quay (the herald's welcome played)
#define FLAG_ICHOR_VISITED_EMPORION             (FLAG_ICHOR_GENERAL_START + 0x0C1) // Ichor: Emporion visited (fly target)
#define FLAG_ICHOR_RITES_TUTORIAL               (FLAG_ICHOR_GENERAL_START + 0x0C2) // Ichor: beat 11: prayed at the quay herm with Kerykos; his three Olive Oil (ICHOR_STUB_OFFERINGS until the item exists)
#define FLAG_ICHOR_GOT_TROWEL                   (FLAG_ICHOR_GENERAL_START + 0x0C3) // Ichor: beat 11: Alethea gave the Trowel
#define FLAG_ICHOR_HIDE_KLEON_QUAY              (FLAG_ICHOR_GENERAL_START + 0x0C4) // Ichor: hide beat 11's Kleon on Emporion's quay
#define FLAG_ICHOR_HIDE_KERYKOS_QUAY            (FLAG_ICHOR_GENERAL_START + 0x0C5) // Ichor: hide beat 11's Kerykos on Emporion's quay
#define FLAG_ICHOR_HIDE_ALETHEA_QUAY            (FLAG_ICHOR_GENERAL_START + 0x0C6) // Ichor: hide beat 11's Alethea on Emporion's quay
#define FLAG_ICHOR_KLEON_WON_HERALD             (FLAG_ICHOR_GENERAL_START + 0x0C7) // Ichor: beat 14: Kleon came out of the Temple of Hermes with the Herald Laurel
#define FLAG_ICHOR_HIDE_KLEON_TEMPLE_STEPS      (FLAG_ICHOR_GENERAL_START + 0x0C8) // Ichor: hide beat 14's Kleon at the Temple of Hermes's door
#define FLAG_ICHOR_HIDE_KLEON_ISTHMUS_GATE      (FLAG_ICHOR_GENERAL_START + 0x0C9) // Ichor: hide Kleon at the Isthmus Gate (SCRIPT.md's _SACRED_GATE)
#define FLAG_ICHOR_KLEON_BATTLE_2_DONE          (FLAG_ICHOR_GENERAL_START + 0x0CA) // Ichor: beat 16: Kleon's second battle at the Isthmus Gate fought
#define FLAG_ICHOR_WON_KLEON_2                  (FLAG_ICHOR_GENERAL_START + 0x0CB) // Ichor: beat 16: won Kleon's second battle
#define FLAG_ICHOR_DAEDALUS_PAGE_1              (FLAG_ICHOR_GENERAL_START + 0x0CC) // Ichor: traded Glykera Olive Oil for page I; also sets FLAG_ICHOR_PAGES_START
#define FLAG_ICHOR_NUMBER_NINE_UNTIED           (FLAG_ICHOR_GENERAL_START + 0x0CD) // Ichor: untied Number Nine, who walked off his plinth (also hides him)
#define FLAG_ICHOR_HIDE_SYKEAS_HARPECK          (FLAG_ICHOR_GENERAL_START + 0x0CE) // Ichor: hide the snatcher on Sykeas's awning (beaten, caught or fled)
#define FLAG_ICHOR_GOT_SYKEAS_FIGS              (FLAG_ICHOR_GENERAL_START + 0x0CF) // Ichor: Sykeas gave his figs and the Pretty Feather
#define FLAG_ICHOR_MET_HALITHERSES              (FLAG_ICHOR_GENERAL_START + 0x0D0) // Ichor: talked to Halitherses the augur on Emporion's mole once
#define FLAG_ICHOR_DUG_EMPORION_QUAY            (FLAG_ICHOR_GENERAL_START + 0x0D1) // Ichor: beat 11: dug the Arachne sherd from the quay planter
#define FLAG_ICHOR_HERM_EMPORION                (FLAG_ICHOR_GENERAL_START + 0x0D2) // Ichor: anointed the great herm at Emporion's crossroads (ICHOR_STUB_HERM)
#define FLAG_ICHOR_ITEM_EMPORION_SUPER_POTION   (FLAG_ICHOR_GENERAL_START + 0x0D3) // Ichor: item ball: Super Potion on the ship sheds' slipway
#define FLAG_ICHOR_ITEM_EMPORION_X_SPEED        (FLAG_ICHOR_GENERAL_START + 0x0D4) // Ichor: item ball: X Speed at the end of the stoa
#define FLAG_ICHOR_ITEM_EMPORION_REPEL          (FLAG_ICHOR_GENERAL_START + 0x0D5) // Ichor: item ball: Repel behind the Deigma
#define FLAG_ICHOR_KRONIA_BREAD                 (FLAG_ICHOR_GENERAL_START + 0x100) // Ichor: accepted bread at the Kronia
#define FLAG_ICHOR_ARRIVED_THYRSA               (FLAG_ICHOR_GENERAL_START + 0x101) // Ichor: reached Thyrsa
#define FLAG_ICHOR_GOT_THESPIS_SCROLL           (FLAG_ICHOR_GENERAL_START + 0x102) // Ichor: received the Mask Laurel scroll
#define FLAG_ICHOR_DIONYSIA_WATCHED             (FLAG_ICHOR_GENERAL_START + 0x103) // Ichor: saw the forged Unwoven tragedy
#define FLAG_ICHOR_DIONYSIA_BROKEN              (FLAG_ICHOR_GENERAL_START + 0x104) // Ichor: broke the Dionysia trance with the satyr play
#define FLAG_ICHOR_SILENOS_BONES                (FLAG_ICHOR_GENERAL_START + 0x105) // Ichor: won Silenos knucklebones contest
#define FLAG_ICHOR_SILENOS_RIDDLE               (FLAG_ICHOR_GENERAL_START + 0x106) // Ichor: won Silenos riddle contest
#define FLAG_ICHOR_SILENOS_BATTLE               (FLAG_ICHOR_GENERAL_START + 0x107) // Ichor: won Silenos battle contest
#define FLAG_ICHOR_ITEM_R6_HEAL                 (FLAG_ICHOR_GENERAL_START + 0x108) // Ichor: Eleutherai road medicine
#define FLAG_ICHOR_ITEM_R6_BALL                 (FLAG_ICHOR_GENERAL_START + 0x109) // Ichor: Eleutherai road ball
#define FLAG_ICHOR_ITEM_R6_ETHER                (FLAG_ICHOR_GENERAL_START + 0x10A) // Ichor: Eleutherai road Ether
#define FLAG_ICHOR_ITEM_R7_HEAL                 (FLAG_ICHOR_GENERAL_START + 0x10B) // Ichor: Kronia road medicine
#define FLAG_ICHOR_ITEM_R7_BALL                 (FLAG_ICHOR_GENERAL_START + 0x10C) // Ichor: Kronia road ball
#define FLAG_ICHOR_ITEM_R7_ETHER                (FLAG_ICHOR_GENERAL_START + 0x10D) // Ichor: Kronia road Ether
#define FLAG_ICHOR_ITEM_KITHAIRON               (FLAG_ICHOR_GENERAL_START + 0x10E) // Ichor: Kithairon summit reward
#define FLAG_ICHOR_ITEM_KITHAIRON_BALL          (FLAG_ICHOR_GENERAL_START + 0x10F) // Ichor: Kithairon reward: Great Ball
#define FLAG_ICHOR_ITEM_KITHAIRON_ETHER         (FLAG_ICHOR_GENERAL_START + 0x110) // Ichor: Kithairon reward: Ether
#define FLAG_ICHOR_KLEON_JOINED_TITANS          (FLAG_ICHOR_GENERAL_START + 0x111) // Ichor: Arkadia: Kleon accepted Iapetos’s forged thread
#define FLAG_ICHOR_HIDE_IAPETOS_ARKADIA         (FLAG_ICHOR_GENERAL_START + 0x112) // Ichor: Arkadia: Iapetos is absent outside the recruitment scene
#define FLAG_ICHOR_KALLISTO_TRIAL               (FLAG_ICHOR_GENERAL_START + 0x113) // Ichor: Artemis: completed the Hunt for the Hind
#define FLAG_ICHOR_GOT_KALLISTO_SCROLL          (FLAG_ICHOR_GENERAL_START + 0x114) // Ichor: Kallisto awarded Night Slash
#define FLAG_ICHOR_ARKADIA_NORTH_OPEN           (FLAG_ICHOR_GENERAL_START + 0x115) // Ichor: Arkadia: left for the Nemean road
#define FLAG_ICHOR_ITEM_R8_HEAL                 (FLAG_ICHOR_GENERAL_START + 0x116) // Ichor: R8 medicine reward
#define FLAG_ICHOR_ITEM_R8_BALL                 (FLAG_ICHOR_GENERAL_START + 0x117) // Ichor: R8 capture reward
#define FLAG_ICHOR_ITEM_R8_ETHER                (FLAG_ICHOR_GENERAL_START + 0x118) // Ichor: R8 Ether reward
#define FLAG_ICHOR_ITEM_R9_HEAL                 (FLAG_ICHOR_GENERAL_START + 0x119) // Ichor: R9 medicine reward
#define FLAG_ICHOR_ITEM_R9_BALL                 (FLAG_ICHOR_GENERAL_START + 0x11A) // Ichor: R9 capture reward
#define FLAG_ICHOR_ITEM_R9_ETHER                (FLAG_ICHOR_GENERAL_START + 0x11B) // Ichor: R9 Ether reward
#define FLAG_ICHOR_ITEM_R11_HEAL                (FLAG_ICHOR_GENERAL_START + 0x11C) // Ichor: R11 medicine reward
#define FLAG_ICHOR_ITEM_R11_BALL                (FLAG_ICHOR_GENERAL_START + 0x11D) // Ichor: R11 capture reward
#define FLAG_ICHOR_ITEM_R11_ETHER               (FLAG_ICHOR_GENERAL_START + 0x11E) // Ichor: R11 Ether reward
#define FLAG_ICHOR_ITEM_R12_HEAL                (FLAG_ICHOR_GENERAL_START + 0x11F) // Ichor: R12 medicine reward
#define FLAG_ICHOR_ITEM_R12_BALL                (FLAG_ICHOR_GENERAL_START + 0x120) // Ichor: R12 capture reward
#define FLAG_ICHOR_ITEM_R12_ETHER               (FLAG_ICHOR_GENERAL_START + 0x121) // Ichor: R12 Ether reward
#define FLAG_ICHOR_ITEM_R13_HEAL                (FLAG_ICHOR_GENERAL_START + 0x122) // Ichor: Highland road visible healing jar
#define FLAG_ICHOR_ITEM_R13_BALL                (FLAG_ICHOR_GENERAL_START + 0x123) // Ichor: Highland road visible ball jar
#define FLAG_ICHOR_ITEM_R13_ETHER               (FLAG_ICHOR_GENERAL_START + 0x124) // Ichor: Highland road visible ether jar
#define FLAG_ICHOR_ITEM_R14_HEAL                (FLAG_ICHOR_GENERAL_START + 0x125) // Ichor: Nemea road visible healing jar
#define FLAG_ICHOR_ITEM_R14_BALL                (FLAG_ICHOR_GENERAL_START + 0x126) // Ichor: Nemea road visible ball jar
#define FLAG_ICHOR_ITEM_R14_ETHER               (FLAG_ICHOR_GENERAL_START + 0x127) // Ichor: Nemea road visible ether jar
#define FLAG_ICHOR_VISITED_ASTYRA               (FLAG_ICHOR_GENERAL_START + 0x128) // Ichor: Visited the capital
#define FLAG_ICHOR_MET_PHAEDON                  (FLAG_ICHOR_GENERAL_START + 0x129) // Ichor: Phaedon healed the player in Astyra
#define FLAG_ICHOR_MET_ELPIS                    (FLAG_ICHOR_GENERAL_START + 0x12A) // Ichor: Met Elpis and Starry
#define FLAG_ICHOR_DAPHNE_ASTYRA                (FLAG_ICHOR_GENERAL_START + 0x12B) // Ichor: Heard Daphne unwriting her book in the capital
#define FLAG_ICHOR_ITEM_R15_HEAL                (FLAG_ICHOR_GENERAL_START + 0x12C) // Ichor: Mystery road healing jar
#define FLAG_ICHOR_ITEM_R15_BALL                (FLAG_ICHOR_GENERAL_START + 0x12D) // Ichor: Mystery road ball jar
#define FLAG_ICHOR_ITEM_R15_ETHER               (FLAG_ICHOR_GENERAL_START + 0x12E) // Ichor: Mystery road ether jar
#define FLAG_ICHOR_ITEM_R16_HEAL                (FLAG_ICHOR_GENERAL_START + 0x12F) // Ichor: Capital pass healing jar
#define FLAG_ICHOR_ITEM_R16_BALL                (FLAG_ICHOR_GENERAL_START + 0x130) // Ichor: Capital pass ball jar
#define FLAG_ICHOR_ITEM_R16_ETHER               (FLAG_ICHOR_GENERAL_START + 0x131) // Ichor: Capital pass ether jar
#define FLAG_ICHOR_ELEUSA_CAPITAL_OPEN          (FLAG_ICHOR_GENERAL_START + 0x132) // Ichor: Eleusa eastern watch stood down after the Moon Laurel
#define FLAG_ICHOR_PHAEDON_DAPHNE_VISIT         (FLAG_ICHOR_GENERAL_START + 0x133) // Ichor: Witnessed Daphne and Phaedon at Elpis bedside
#define FLAG_ICHOR_HIDE_PHAEDON_HOUSE           (FLAG_ICHOR_GENERAL_START + 0x134) // Ichor: Phaedon left the bedside visit
#define FLAG_ICHOR_HIDE_DAPHNE_HOUSE            (FLAG_ICHOR_GENERAL_START + 0x135) // Ichor: Daphne left the bedside visit
#define FLAG_ICHOR_ASTYRA_OSTRACISM_DONE        (FLAG_ICHOR_GENERAL_START + 0x136) // Ichor: Witnessed the forged ostracism and Alethea exile
#define FLAG_ICHOR_HIDE_ALETHEA_ASTYRA          (FLAG_ICHOR_GENERAL_START + 0x137) // Ichor: Alethea is outside the city after exile
#define FLAG_ICHOR_HIDE_ALETHEA_R16             (FLAG_ICHOR_GENERAL_START + 0x138) // Ichor: Roadside Alethea is absent before exile or after confession
#define FLAG_ICHOR_ALETHEA_CONFESSED            (FLAG_ICHOR_GENERAL_START + 0x139) // Ichor: Alethea told the truth about her reading outside Astyra
#define FLAG_ICHOR_AKROPOLIS_GATE               (FLAG_ICHOR_GENERAL_START + 0x13A) // Ichor: Captain recognized the forged owl seal and stood aside
#define FLAG_ICHOR_AKROPOLIS_PAIR_ONE           (FLAG_ICHOR_GENERAL_START + 0x13B) // Ichor: Defeated Lithos and Koniortos beside Alethea
#define FLAG_ICHOR_AKROPOLIS_PAIR_TWO           (FLAG_ICHOR_GENERAL_START + 0x13C) // Ichor: Defeated Sideros and Chalkos beside Alethea
#define FLAG_ICHOR_KLEON_AKROPOLIS              (FLAG_ICHOR_GENERAL_START + 0x13D) // Ichor: Kleon revealed why the Titans want the Unwoven
#define FLAG_ICHOR_AKROPOLIS_OLIVE_FELL          (FLAG_ICHOR_GENERAL_START + 0x13E) // Ichor: Athena's olive was uprooted before the Rhea battle
#define FLAG_ICHOR_AKROPOLIS_RAID_DONE           (FLAG_ICHOR_GENERAL_START + 0x13F) // Ichor: Rhea escaped with the second fragment
#define FLAG_ICHOR_ITEM_AKROPOLIS_HEAL           (FLAG_ICHOR_GENERAL_START + 0x140) // Ichor: Sacred Way healing jar
#define FLAG_ICHOR_HIDE_ALETHEA_AKROPOLIS        (FLAG_ICHOR_GENERAL_START + 0x141) // Ichor: Independent actor hide state, not raid completion
#define FLAG_ICHOR_HIDE_RHEA_AKROPOLIS           (FLAG_ICHOR_GENERAL_START + 0x142) // Ichor: Rhea left through the spring stair
#define FLAG_ICHOR_AKROPOLIS_RECOVERED           (FLAG_ICHOR_GENERAL_START + 0x143) // Ichor: Phaedon tended the player after the raid
#define FLAG_ICHOR_HIDE_ALETHEA_ASTYRA_CLINIC    (FLAG_ICHOR_GENERAL_START + 0x144) // Ichor: Alethea is only at the clinic for the raid aftermath
#define FLAG_ICHOR_SALT_WELL_OPEN               (FLAG_ICHOR_GENERAL_START + 0x145) // Ichor: Caretaker opened Poseidon's stair
#define FLAG_ICHOR_SALT_WELL_TIDE_1             (FLAG_ICHOR_GENERAL_START + 0x146) // Ichor: Found the upper pool's safe backwash crossing
#define FLAG_ICHOR_SALT_WELL_TIDE_2             (FLAG_ICHOR_GENERAL_START + 0x147) // Ichor: Found the grotto's safe backwash crossing
#define FLAG_ICHOR_ALETHEA_LEFT_ASTYRA          (FLAG_ICHOR_GENERAL_START + 0x148) // Ichor: Alethea left after the Conch
#define FLAG_ICHOR_HIDE_ALETHEA_SALT_WELL       (FLAG_ICHOR_GENERAL_START + 0x149) // Ichor: Independent Salt Well actor state
#define FLAG_ICHOR_ITEM_SALT_WELL_HEAL          (FLAG_ICHOR_GENERAL_START + 0x14A) // Ichor: Supply by the teaching shallows
#define FLAG_ICHOR_ITEM_SALT_WELL_PEARL         (FLAG_ICHOR_GENERAL_START + 0x14B) // Ichor: Upper side grotto gift
#define FLAG_ICHOR_ITEM_SALT_WELL_ETHER         (FLAG_ICHOR_GENERAL_START + 0x14C) // Ichor: Lower side grotto supply
#define FLAG_ICHOR_ITEM_SALT_WELL_SHELL         (FLAG_ICHOR_GENERAL_START + 0x14D) // Ichor: Lower side grotto gift
#define FLAG_ICHOR_ITEM_ASTYRA_HARBOR           (FLAG_ICHOR_GENERAL_START + 0x14E) // Ichor: Harbor pier jar
#define FLAG_ICHOR_ARRIVED_KALDERA              (FLAG_ICHOR_GENERAL_START + 0x14F) // Ichor: reached Thera on the connected journey
#define FLAG_ICHOR_FORGE_TEACH                  (FLAG_ICHOR_GENERAL_START + 0x150) // Ichor: parked the first Bronze Servant
#define FLAG_ICHOR_FORGE_TEST                   (FLAG_ICHOR_GENERAL_START + 0x151) // Ichor: parked the paired Bronze Servants
#define FLAG_ICHOR_FORGE_MASTER                 (FLAG_ICHOR_GENERAL_START + 0x152) // Ichor: parked three servants with the column drum
#define FLAG_ICHOR_TALOS_RELIC_STORY            (FLAG_ICHOR_GENERAL_START + 0x153) // Ichor: Talos explained the wings and the Harpe
#define FLAG_ICHOR_KALDERA_FRAGMENT_LOST        (FLAG_ICHOR_GENERAL_START + 0x154) // Ichor: Hyperion escaped with the third Harpe fragment
#define FLAG_ICHOR_MOM_MISSING                  (FLAG_ICHOR_GENERAL_START + 0x155) // Ichor: read Kydippe's letter at Kaldera harbor
#define FLAG_ICHOR_HIDE_KALDERA_HYPERION        (FLAG_ICHOR_GENERAL_START + 0x156) // Ichor: Hyperion left the Telchines forge
#define FLAG_ICHOR_KALDERA_HOUSE_GIFT           (FLAG_ICHOR_GENERAL_START + 0x157) // Ichor: the smith gave the player a Metal Coat
#define FLAG_ICHOR_ITEM_KALDERA_BALL            (FLAG_ICHOR_GENERAL_START + 0x158) // Ichor: Kaldera's harbor supply
#define FLAG_ICHOR_ITEM_KALDERA_FORGE_ETHER     (FLAG_ICHOR_GENERAL_START + 0x159) // Ichor: Telchines forge supply
#define FLAG_ICHOR_ITEM_KALDERA_FORGE_REVIVE    (FLAG_ICHOR_GENERAL_START + 0x15A) // Ichor: Telchines forge side grotto gift
#define FLAG_ICHOR_HIDE_DAPHNE_LIBRARY          (FLAG_ICHOR_GENERAL_START + 0x15B) // Ichor: Daphne followed the player to Kaldera
#define FLAG_ICHOR_R6_VINES_CUT                 (FLAG_ICHOR_GENERAL_START + 0x15C) // Ichor: Route 6: Demeter's Sickle cut the vines on the terrace stair
#define FLAG_ICHOR_R6_PRESS_VINES_CUT           (FLAG_ICHOR_GENERAL_START + 0x15D) // Ichor: Route 6: the Sickle cut the vines over the old wine press
#define FLAG_ICHOR_R6_POSTERN_VINES_CUT         (FLAG_ICHOR_GENERAL_START + 0x15E) // Ichor: Route 6: the Sickle cut the vines in the fort's postern
#define FLAG_ICHOR_R6_VINEDRESSER_GIFT          (FLAG_ICHOR_GENERAL_START + 0x15F) // Ichor: Route 6: the vine-dresser gave the player a Miracle Seed
#define FLAG_ICHOR_KITHAIRON_WINE_GIFT          (FLAG_ICHOR_GENERAL_START + 0x160) // Ichor: Kithairon: the maenads gave the player Wine for the god
#define FLAG_ICHOR_FROZEN_HOUR                  (FLAG_ICHOR_GENERAL_START + 0x480) // Ichor: The Frozen Hour: the world is gray and still (engine, ENGINE_API §5)
#define FLAG_ICHOR_THREAD_NO_RETURN             (FLAG_ICHOR_GENERAL_START + 0x481) // Ichor: The Turning: the Thread's RETURN TO… is closed (engine, ENGINE_API §6)
#define FLAG_ICHOR_DISGUISE_ON                  (FLAG_ICHOR_GENERAL_START + 0x482) // Ichor: The Titan helmet is on: ordinary Titanborn and sentries take the player for a recruit (engine, ENGINE_API §6)
#define FLAG_ICHOR_MOM_CONFESSED                (FLAG_ICHOR_GENERAL_START + 0x483) // Ichor: Mom confessed the bee at the Kastalian spring: her knucklebones play fair (engine, ENGINE_API §7; set by world-act3 at III-7)
#define FLAG_ICHOR_PITHOS_EXPLAINED             (FLAG_ICHOR_GENERAL_START + 0x484) // Ichor: first lid lifted on a Pithos: what it is for was explained
#define FLAG_ICHOR_TOWN_HERM_ELAIA              (FLAG_ICHOR_GENERAL_START + 0x4A0) // Ichor: Elaia's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_ELAIA)
#define FLAG_ICHOR_TOWN_HERM_AKTI               (FLAG_ICHOR_GENERAL_START + 0x4A1) // Ichor: Akti's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_AKTI)
#define FLAG_ICHOR_TOWN_HERM_AIGINA             (FLAG_ICHOR_GENERAL_START + 0x4A2) // Ichor: Aigina's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_AIGINA)
#define FLAG_ICHOR_TOWN_HERM_EMPORION           (FLAG_ICHOR_GENERAL_START + 0x4A3) // Ichor: Emporion's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_EMPORION)
#define FLAG_ICHOR_TOWN_HERM_ELEUSA             (FLAG_ICHOR_GENERAL_START + 0x4A4) // Ichor: Eleusa's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_ELEUSA)
#define FLAG_ICHOR_TOWN_HERM_THYRSA             (FLAG_ICHOR_GENERAL_START + 0x4A5) // Ichor: Thyrsa's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_THYRSA)
#define FLAG_ICHOR_TOWN_HERM_LEBADEIA           (FLAG_ICHOR_GENERAL_START + 0x4A6) // Ichor: Lebadeia's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_LEBADEIA)
#define FLAG_ICHOR_TOWN_HERM_KIRRHA             (FLAG_ICHOR_GENERAL_START + 0x4A7) // Ichor: Kirrha's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_KIRRHA)
#define FLAG_ICHOR_TOWN_HERM_AIGION             (FLAG_ICHOR_GENERAL_START + 0x4A8) // Ichor: Aigion's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_AIGION)
#define FLAG_ICHOR_TOWN_HERM_STYX_FALLS         (FLAG_ICHOR_GENERAL_START + 0x4A9) // Ichor: Styx Falls's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_STYX_FALLS)
#define FLAG_ICHOR_TOWN_HERM_ARKADIA            (FLAG_ICHOR_GENERAL_START + 0x4AA) // Ichor: Arkadia's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_ARKADIA)
#define FLAG_ICHOR_TOWN_HERM_NEMEA              (FLAG_ICHOR_GENERAL_START + 0x4AB) // Ichor: Nemea's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_NEMEA)
#define FLAG_ICHOR_TOWN_HERM_DAPHNI             (FLAG_ICHOR_GENERAL_START + 0x4AC) // Ichor: Daphni's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_DAPHNI)
#define FLAG_ICHOR_TOWN_HERM_ASTYRA             (FLAG_ICHOR_GENERAL_START + 0x4AD) // Ichor: Astyra's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_ASTYRA)
#define FLAG_ICHOR_TOWN_HERM_KALDERA            (FLAG_ICHOR_GENERAL_START + 0x4AE) // Ichor: Kaldera's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_KALDERA)
#define FLAG_ICHOR_TOWN_HERM_SKANDEIA           (FLAG_ICHOR_GENERAL_START + 0x4AF) // Ichor: Skandeia's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_SKANDEIA)
#define FLAG_ICHOR_TOWN_HERM_PAPHIA             (FLAG_ICHOR_GENERAL_START + 0x4B0) // Ichor: Paphia's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_PAPHIA)
#define FLAG_ICHOR_TOWN_HERM_AMNISOS            (FLAG_ICHOR_GENERAL_START + 0x4B1) // Ichor: Amnisos's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_AMNISOS)
#define FLAG_ICHOR_TOWN_HERM_OLYMPUS            (FLAG_ICHOR_GENERAL_START + 0x4B2) // Ichor: Olympus (the Propylaia)'s travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_OLYMPUS)
#define FLAG_ICHOR_TOWN_HERM_GYTHEION           (FLAG_ICHOR_GENERAL_START + 0x4B3) // Ichor: Gytheion's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_GYTHEION)
#define FLAG_ICHOR_TOWN_HERM_LAKONIA            (FLAG_ICHOR_GENERAL_START + 0x4B4) // Ichor: Lakonia's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_LAKONIA)
#define FLAG_ICHOR_TOWN_HERM_SACRED_OLIVES      (FLAG_ICHOR_GENERAL_START + 0x4B5) // Ichor: the Sacred Olives (Route 28)'s travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_SACRED_OLIVES)
#define FLAG_ICHOR_TOWN_HERM_DELPHOI            (FLAG_ICHOR_GENERAL_START + 0x4B6) // Ichor: Delphoi's travel herm is registered (engine, SYSTEMS §4; FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_DELPHOI)
#define FLAG_ICHOR_TOWN_HERM_SPARE_23           (FLAG_ICHOR_GENERAL_START + 0x4B7) // Ichor: travel herm 23, kept for the next town: rename it (engine, SYSTEMS §4)
#define FLAG_ICHOR_TOWN_HERM_SPARE_24           (FLAG_ICHOR_GENERAL_START + 0x4B8) // Ichor: travel herm 24, kept for the next town: rename it (engine, SYSTEMS §4)
#define FLAG_ICHOR_TOWN_HERM_SPARE_25           (FLAG_ICHOR_GENERAL_START + 0x4B9) // Ichor: travel herm 25, kept for the next town: rename it (engine, SYSTEMS §4)
#define FLAG_ICHOR_TOWN_HERM_SPARE_26           (FLAG_ICHOR_GENERAL_START + 0x4BA) // Ichor: travel herm 26, kept for the next town: rename it (engine, SYSTEMS §4)
#define FLAG_ICHOR_TOWN_HERM_SPARE_27           (FLAG_ICHOR_GENERAL_START + 0x4BB) // Ichor: travel herm 27, kept for the next town: rename it (engine, SYSTEMS §4)
#define FLAG_ICHOR_TOWN_HERM_SPARE_28           (FLAG_ICHOR_GENERAL_START + 0x4BC) // Ichor: travel herm 28, kept for the next town: rename it (engine, SYSTEMS §4)
#define FLAG_ICHOR_TOWN_HERM_SPARE_29           (FLAG_ICHOR_GENERAL_START + 0x4BD) // Ichor: travel herm 29, kept for the next town: rename it (engine, SYSTEMS §4)
#define FLAG_ICHOR_TOWN_HERM_SPARE_30           (FLAG_ICHOR_GENERAL_START + 0x4BE) // Ichor: travel herm 30, kept for the next town: rename it (engine, SYSTEMS §4)
#define FLAG_ICHOR_TOWN_HERM_SPARE_31           (FLAG_ICHOR_GENERAL_START + 0x4BF) // Ichor: travel herm 31, kept for the next town: rename it (engine, SYSTEMS §4)
#define FLAG_ICHOR_HIDDEN_ITEM_R6_HONEY         (FLAG_ICHOR_GENERAL2_START + 0x000) // Ichor: Eleutherai shrine honey
#define FLAG_ICHOR_HIDDEN_ITEM_R6_REVIVE        (FLAG_ICHOR_GENERAL2_START + 0x001) // Ichor: Eleutherai terrace Revive
#define FLAG_ICHOR_HIDDEN_ITEM_R6_REPEL         (FLAG_ICHOR_GENERAL2_START + 0x002) // Ichor: Eleutherai verge Repel
#define FLAG_ICHOR_HIDDEN_ITEM_R7_HONEY         (FLAG_ICHOR_GENERAL2_START + 0x003) // Ichor: Kronia honey
#define FLAG_ICHOR_HIDDEN_ITEM_R7_REVIVE        (FLAG_ICHOR_GENERAL2_START + 0x004) // Ichor: Kronia Revive
#define FLAG_ICHOR_HIDDEN_ITEM_R7_REPEL         (FLAG_ICHOR_GENERAL2_START + 0x005) // Ichor: Kronia Repel
#define FLAG_ICHOR_HIDDEN_ITEM_KITHAIRON_HONEY  (FLAG_ICHOR_GENERAL2_START + 0x006) // Ichor: Kithairon hidden Honey
#define FLAG_ICHOR_HIDDEN_ITEM_KITHAIRON_REVIVE (FLAG_ICHOR_GENERAL2_START + 0x007) // Ichor: Kithairon hidden Revive
#define FLAG_ICHOR_HIDDEN_ITEM_KITHAIRON_REPEL  (FLAG_ICHOR_GENERAL2_START + 0x008) // Ichor: Kithairon hidden Super Repel
#define FLAG_ICHOR_HIDDEN_ITEM_R8_HONEY         (FLAG_ICHOR_GENERAL2_START + 0x009) // Ichor: R8 hidden Honey
#define FLAG_ICHOR_HIDDEN_ITEM_R8_REVIVE        (FLAG_ICHOR_GENERAL2_START + 0x00A) // Ichor: R8 hidden Revive
#define FLAG_ICHOR_HIDDEN_ITEM_R8_REPEL         (FLAG_ICHOR_GENERAL2_START + 0x00B) // Ichor: R8 hidden Super Repel
#define FLAG_ICHOR_HIDDEN_ITEM_R9_HONEY         (FLAG_ICHOR_GENERAL2_START + 0x00C) // Ichor: R9 hidden Honey
#define FLAG_ICHOR_HIDDEN_ITEM_R9_REVIVE        (FLAG_ICHOR_GENERAL2_START + 0x00D) // Ichor: R9 hidden Revive
#define FLAG_ICHOR_HIDDEN_ITEM_R9_REPEL         (FLAG_ICHOR_GENERAL2_START + 0x00E) // Ichor: R9 hidden Super Repel
#define FLAG_ICHOR_HIDDEN_ITEM_R11_HONEY        (FLAG_ICHOR_GENERAL2_START + 0x00F) // Ichor: R11 hidden Honey
#define FLAG_ICHOR_HIDDEN_ITEM_R11_REVIVE       (FLAG_ICHOR_GENERAL2_START + 0x010) // Ichor: R11 hidden Revive
#define FLAG_ICHOR_HIDDEN_ITEM_R11_REPEL        (FLAG_ICHOR_GENERAL2_START + 0x011) // Ichor: R11 hidden Super Repel
#define FLAG_ICHOR_HIDDEN_ITEM_R12_HONEY        (FLAG_ICHOR_GENERAL2_START + 0x012) // Ichor: R12 hidden Honey
#define FLAG_ICHOR_HIDDEN_ITEM_R12_REVIVE       (FLAG_ICHOR_GENERAL2_START + 0x013) // Ichor: R12 hidden Revive
#define FLAG_ICHOR_HIDDEN_ITEM_R12_REPEL        (FLAG_ICHOR_GENERAL2_START + 0x014) // Ichor: R12 hidden Super Repel
#define FLAG_ICHOR_HIDDEN_ITEM_R13_HONEY        (FLAG_ICHOR_GENERAL2_START + 0x015) // Ichor: Highland road grove honey
#define FLAG_ICHOR_HIDDEN_ITEM_R13_REVIVE       (FLAG_ICHOR_GENERAL2_START + 0x016) // Ichor: Highland road ridge revive
#define FLAG_ICHOR_HIDDEN_ITEM_R13_REPEL        (FLAG_ICHOR_GENERAL2_START + 0x017) // Ichor: Highland road wall repel
#define FLAG_ICHOR_HIDDEN_ITEM_R14_HONEY        (FLAG_ICHOR_GENERAL2_START + 0x018) // Ichor: Nemea road grove honey
#define FLAG_ICHOR_HIDDEN_ITEM_R14_REVIVE       (FLAG_ICHOR_GENERAL2_START + 0x019) // Ichor: Nemea road ridge revive
#define FLAG_ICHOR_HIDDEN_ITEM_R14_REPEL        (FLAG_ICHOR_GENERAL2_START + 0x01A) // Ichor: Nemea road wall repel
#define FLAG_ICHOR_HIDDEN_ITEM_R15_HONEY        (FLAG_ICHOR_GENERAL2_START + 0x01B) // Ichor: Salt lake honey
#define FLAG_ICHOR_HIDDEN_ITEM_R15_REVIVE       (FLAG_ICHOR_GENERAL2_START + 0x01C) // Ichor: Salt lake revive
#define FLAG_ICHOR_HIDDEN_ITEM_R15_REPEL        (FLAG_ICHOR_GENERAL2_START + 0x01D) // Ichor: Salt lake repel
#define FLAG_ICHOR_HIDDEN_ITEM_R16_HONEY        (FLAG_ICHOR_GENERAL2_START + 0x01E) // Ichor: Capital pass honey
#define FLAG_ICHOR_HIDDEN_ITEM_R16_REVIVE       (FLAG_ICHOR_GENERAL2_START + 0x01F) // Ichor: Capital pass revive
#define FLAG_ICHOR_HIDDEN_ITEM_R16_REPEL        (FLAG_ICHOR_GENERAL2_START + 0x020) // Ichor: Capital pass repel
#define FLAG_ICHOR_HIDDEN_AKROPOLIS_REVIVE       (FLAG_ICHOR_GENERAL2_START + 0x021) // Ichor: Lower terrace revive
#define FLAG_ICHOR_HIDDEN_AKROPOLIS_ETHER        (FLAG_ICHOR_GENERAL2_START + 0x022) // Ichor: Olive court ether
#define FLAG_ICHOR_KNUCKLEBONES_PHAIDIMOS       (FLAG_ICHOR_GENERAL2_START + 0x023) // Ichor: won Phaidimos's first knucklebones match (Thyrsa, the Kantharos)
#define FLAG_ICHOR_KNUCKLEBONES_GLAUKE          (FLAG_ICHOR_GENERAL2_START + 0x024) // Ichor: won Glauke's first knucklebones match (Thyrsa, the Kantharos)
#define FLAG_ICHOR_KNUCKLEBONES_THYRSA          (FLAG_ICHOR_GENERAL2_START + 0x025) // Ichor: beat Aristomache, Thyrsa's knucklebones champion
#define FLAG_ICHOR_TRADED_PROSOMIME             (FLAG_ICHOR_GENERAL2_START + 0x026) // Ichor: traded a Gelasable for Euthykles's Prosomime (Thyrsa)
#define FLAG_ICHOR_GOT_POLOS_MYSTIC_WATER       (FLAG_ICHOR_GENERAL2_START + 0x027) // Ichor: showed Polos a Prosomime and got his Mystic Water (Thyrsa)
#define FLAG_ICHOR_EUDORA_FIG_DUG               (FLAG_ICHOR_GENERAL2_START + 0x028) // Ichor: dug up the arm-ring under Eudora's fig (Thyrsa)
#define FLAG_ICHOR_GOT_POWER_BRACER             (FLAG_ICHOR_GENERAL2_START + 0x029) // Ichor: Eudora gave her husband's arm-ring, the Power Bracer (Thyrsa)
#define FLAG_ICHOR_MET_MANTO                    (FLAG_ICHOR_GENERAL2_START + 0x02A) // Ichor: met Manto on the Kadmeia wall (Thyrsa)
#define FLAG_ICHOR_MANTO_CROWS                  (FLAG_ICHOR_GENERAL2_START + 0x02B) // Ichor: Manto asked you to watch the crows over the Kronia (Thyrsa)
#define FLAG_ICHOR_SAW_CROWS                    (FLAG_ICHOR_GENERAL2_START + 0x02C) // Ichor: saw the crows fly south from the Elektran Gate (Thyrsa)
#define FLAG_ICHOR_GOT_TWISTED_SPOON            (FLAG_ICHOR_GENERAL2_START + 0x02D) // Ichor: Manto gave Teiresias's spoon, the Twisted Spoon (Thyrsa)
#define FLAG_ICHOR_GOT_DRAGON_FANG              (FLAG_ICHOR_GENERAL2_START + 0x02E) // Ichor: Chthonia gave the Dragon Fang (Thyrsa, the Sown house)
#define FLAG_ICHOR_GOT_STAPHYLOS_NUGGET         (FLAG_ICHOR_GENERAL2_START + 0x02F) // Ichor: Staphylos gave the press's Nugget (Thyrsa)
#define FLAG_ICHOR_THYRSA_BEGGAR_HELPED         (FLAG_ICHOR_GENERAL2_START + 0x030) // Ichor: led Thyrsa's blind beggar to the spring of Dirke
#define FLAG_ICHOR_ITEM_THYRSA_BLACK_SLUDGE     (FLAG_ICHOR_GENERAL2_START + 0x031) // Ichor: Thyrsa's Black Sludge item ball
#define FLAG_ICHOR_ITEM_THYRSA_SUPER_POTION     (FLAG_ICHOR_GENERAL2_START + 0x032) // Ichor: Thyrsa's Super Potion item ball
#define FLAG_ICHOR_ITEM_THYRSA_BIG_NUGGET       (FLAG_ICHOR_GENERAL2_START + 0x033) // Ichor: Thyrsa's Big Nugget item ball
#define FLAG_ICHOR_HIDDEN_ITEM_THYRSA_CELL_BATTERY (FLAG_ICHOR_GENERAL2_START + 0x034) // Ichor: Thyrsa: by Semele's chamber
#define FLAG_ICHOR_HIDDEN_ITEM_THYRSA_HEART_SCALE (FLAG_ICHOR_GENERAL2_START + 0x035) // Ichor: Thyrsa: at the spring of Dirke
#define FLAG_ICHOR_HIDDEN_ITEM_THYRSA_RARE_CANDY (FLAG_ICHOR_GENERAL2_START + 0x036) // Ichor: Thyrsa: at the north-west bricked gate
#define FLAG_ICHOR_HIDDEN_ITEM_THYRSA_PRETTY_FEATHER (FLAG_ICHOR_GENERAL2_START + 0x037) // Ichor: Thyrsa: under the Kadmeia's east wall
#define FLAG_ICHOR_HIDDEN_SALT_WELL_SALT        (FLAG_ICHOR_GENERAL2_START + 0x038) // Ichor: Upper tide-line salt
#define FLAG_ICHOR_HIDDEN_SALT_WELL_SCALE       (FLAG_ICHOR_GENERAL2_START + 0x039) // Ichor: Upper rock-pool scale
#define FLAG_ICHOR_HIDDEN_SALT_WELL_PEARL       (FLAG_ICHOR_GENERAL2_START + 0x03A) // Ichor: Lower sea gift
#define FLAG_ICHOR_HIDDEN_SALT_WELL_REVIVE      (FLAG_ICHOR_GENERAL2_START + 0x03B) // Ichor: Lower sheltered cache
#define FLAG_ICHOR_HIDDEN_ASTYRA_HARBOR_SALT    (FLAG_ICHOR_GENERAL2_START + 0x03C) // Ichor: Harbor salt
#define FLAG_ICHOR_HIDDEN_ASTYRA_HARBOR_SCALE   (FLAG_ICHOR_GENERAL2_START + 0x03D) // Ichor: Harbor scale
#define FLAG_ICHOR_TRADED_ARKOBY                (FLAG_ICHOR_GENERAL2_START + 0x03E) // Ichor: traded Hippothoos a Gelasable for Arkas (Arkadia, the charcoal hut)
#define FLAG_ICHOR_KROTOS_KID_1                 (FLAG_ICHOR_GENERAL2_START + 0x03F) // Ichor: Krotos's first lost kid sent home (Arkadia)
#define FLAG_ICHOR_KROTOS_KID_2                 (FLAG_ICHOR_GENERAL2_START + 0x040) // Ichor: Krotos's second lost kid sent home (Arkadia)
#define FLAG_ICHOR_KROTOS_KID_3                 (FLAG_ICHOR_GENERAL2_START + 0x041) // Ichor: Krotos's third lost kid sent home (Arkadia)
#define FLAG_ICHOR_GOT_LUCKY_EGG                (FLAG_ICHOR_GENERAL2_START + 0x042) // Ichor: Krotos's Lucky Egg (Arkadia, the goatherd's house)
#define FLAG_ICHOR_KLYMENE_STORY                (FLAG_ICHOR_GENERAL2_START + 0x043) // Ichor: heard Klymene's Atalanta story (Arkadia)
#define FLAG_ICHOR_KLYMENE_RACE                 (FLAG_ICHOR_GENERAL2_START + 0x044) // Ichor: racing Parthenopaios to the temple stair (Arkadia)
#define FLAG_ICHOR_KLYMENE_RACE_TURNED          (FLAG_ICHOR_GENERAL2_START + 0x045) // Ichor: touched the temple stair in the race (Arkadia)
#define FLAG_ICHOR_GOT_CHOICE_SCARF             (FLAG_ICHOR_GENERAL2_START + 0x046) // Ichor: Klymene's Choice Scarf (Arkadia)
#define FLAG_ICHOR_NYKTIMOS_STORY               (FLAG_ICHOR_GENERAL2_START + 0x047) // Ichor: heard Nyktimos's Lykaon story (Arkadia)
#define FLAG_ICHOR_GOT_BLACK_GLASSES            (FLAG_ICHOR_GENERAL2_START + 0x048) // Ichor: Nyktimos's Black Glasses after the Moon Laurel (Arkadia)
#define FLAG_ICHOR_ITEM_ARKADIA_MAX_REPEL       (FLAG_ICHOR_GENERAL2_START + 0x049) // Ichor: Arkadia's Max Repel item ball
#define FLAG_ICHOR_GOT_GRYLLOS                  (FLAG_ICHOR_GENERAL2_START + 0x04A) // Ichor: took Gryllos the Kaplet from Eubouleus (Styx Falls, the inn)
#define FLAG_ICHOR_GRYLLOS_SHOWN                (FLAG_ICHOR_GENERAL2_START + 0x04B) // Ichor: showed Eubouleus Gryllos grown (Styx Falls, the inn)
#define FLAG_ICHOR_GOT_CLEANSE_TAG              (FLAG_ICHOR_GENERAL2_START + 0x04C) // Ichor: Horkia's Cleanse Tag (Styx Falls, the oath house)
#define FLAG_ICHOR_GOT_TM_BULLDOZE              (FLAG_ICHOR_GENERAL2_START + 0x04D) // Ichor: Kepheus's TM Bulldoze (Styx Falls, the stone house)
#define FLAG_ICHOR_ITEM_STYX_FALLS_STARDUST     (FLAG_ICHOR_GENERAL2_START + 0x04E) // Ichor: Styx Falls's Stardust item ball
#define FLAG_ICHOR_MAIA_SINGER                  (FLAG_ICHOR_GENERAL2_START + 0x04F) // Ichor: the Cave of Maia's priestess heard a Chelyra (Route 12)
#define FLAG_ICHOR_ITEM_MAIA_MAX_REPEL          (FLAG_ICHOR_GENERAL2_START + 0x050) // Ichor: the Cave of Maia's Max Repel item ball
#define FLAG_ICHOR_ITEM_MAIA_LEPPA_BERRY        (FLAG_ICHOR_GENERAL2_START + 0x051) // Ichor: the Cave of Maia's Leppa Berry item ball
#define FLAG_ICHOR_ITEM_TEMPLE_ARTEMIS_PRETTY_FEATHER (FLAG_ICHOR_GENERAL2_START + 0x052) // Ichor: the Temple of Artemis's Pretty Feather item ball
#define FLAG_ICHOR_ITEM_CYPRESS_WOOD_DUSK_BALLS (FLAG_ICHOR_GENERAL2_START + 0x053) // Ichor: the Cypress Wood's Dusk Balls item ball
#define FLAG_ICHOR_ITEM_CYPRESS_WOOD_DUSK_STONE (FLAG_ICHOR_GENERAL2_START + 0x054) // Ichor: the Cypress Wood's Dusk Stone item ball
#define FLAG_ICHOR_ITEM_CYPRESS_WOOD_HYPER_POTION (FLAG_ICHOR_GENERAL2_START + 0x055) // Ichor: the Cypress Wood's Hyper Potion item ball
#define FLAG_ICHOR_HIDDEN_ITEM_ARKADIA_REVIVE   (FLAG_ICHOR_GENERAL2_START + 0x056) // Ichor: Arkadia: by the north gate's lamp
#define FLAG_ICHOR_HIDDEN_ITEM_ARKADIA_SILVER_POWDER (FLAG_ICHOR_GENERAL2_START + 0x057) // Ichor: Arkadia: behind the Agora
#define FLAG_ICHOR_HIDDEN_ITEM_STYX_FALLS_OBOL  (FLAG_ICHOR_GENERAL2_START + 0x058) // Ichor: Styx Falls: an obol by the Oath Stone
#define FLAG_ICHOR_HIDDEN_ITEM_STYX_FALLS_ETHER (FLAG_ICHOR_GENERAL2_START + 0x059) // Ichor: Styx Falls: in the gorge's gap
#define FLAG_ICHOR_HIDDEN_ITEM_STYX_KEPHEUS_EVERSTONE (FLAG_ICHOR_GENERAL2_START + 0x05A) // Ichor: Styx Falls: the rubble in Kepheus's lean-to
#define FLAG_ICHOR_HIDDEN_ITEM_MAIA_PP_UP       (FLAG_ICHOR_GENERAL2_START + 0x05B) // Ichor: the Cave of Maia: beside the cradle
#define FLAG_ICHOR_HIDDEN_ITEM_MAIA_FRESH_WATER (FLAG_ICHOR_GENERAL2_START + 0x05C) // Ichor: the Cave of Maia: by Hermes's altar
#define FLAG_ICHOR_HIDDEN_ITEM_TEMPLE_ARTEMIS_STARDUST (FLAG_ICHOR_GENERAL2_START + 0x05D) // Ichor: the Temple of Artemis: the first glade's corner
#define FLAG_ICHOR_HIDDEN_ITEM_TEMPLE_ARTEMIS_DUSK_BALL (FLAG_ICHOR_GENERAL2_START + 0x05E) // Ichor: the Temple of Artemis: by the Keryneia stele
#define FLAG_ICHOR_HIDDEN_ITEM_TEMPLE_ARTEMIS_STAR_PIECE (FLAG_ICHOR_GENERAL2_START + 0x05F) // Ichor: the Temple of Artemis: on Kallisto's rock
#define FLAG_ICHOR_HIDDEN_ITEM_CYPRESS_WOOD_CHARCOAL (FLAG_ICHOR_GENERAL2_START + 0x060) // Ichor: the Cypress Wood: by the burners' hedge
#define FLAG_ICHOR_HIDDEN_ITEM_CYPRESS_WOOD_BIG_MUSHROOM (FLAG_ICHOR_GENERAL2_START + 0x061) // Ichor: the Cypress Wood: in the east thicket
#define FLAG_ICHOR_HIDDEN_ITEM_CYPRESS_WOOD_STAR_PIECE (FLAG_ICHOR_GENERAL2_START + 0x062) // Ichor: the Cypress Wood: by Artemis's altar
#define FLAG_ICHOR_HIDDEN_ITEM_KALDERA_SALT     (FLAG_ICHOR_GENERAL2_START + 0x063) // Ichor: Kaldera harbor salt
#define FLAG_ICHOR_HIDDEN_ITEM_KALDERA_SCALE    (FLAG_ICHOR_GENERAL2_START + 0x064) // Ichor: Kaldera pier scale
#define FLAG_ICHOR_HIDDEN_ITEM_KALDERA_FORGE_SHARD (FLAG_ICHOR_GENERAL2_START + 0x065) // Ichor: Telchines forge red shard
#define FLAG_ICHOR_HIDDEN_ITEM_KALDERA_FORGE_NUGGET (FLAG_ICHOR_GENERAL2_START + 0x066) // Ichor: Telchines forge nugget
#define FLAG_ICHOR_HIDDEN_FOAM_ROAD_ETHER (FLAG_ICHOR_GENERAL2_START + 0x067) // Ichor: Foam Road hidden item: Ether behind the great herm
#define FLAG_ICHOR_HIDDEN_FOAM_ROAD_HEART_SCALE (FLAG_ICHOR_GENERAL2_START + 0x068) // Ichor: Foam Road hidden item: Heart Scale in the Horn's cliff-top meadow
#define FLAG_ICHOR_HIDDEN_FOAM_ROAD_NET_BALL (FLAG_ICHOR_GENERAL2_START + 0x069) // Ichor: Foam Road hidden item: Net Ball on the rock past Amphitos's jetty
#define FLAG_ICHOR_HIDDEN_FOAM_ROAD_STARDUST (FLAG_ICHOR_GENERAL2_START + 0x06A) // Ichor: Foam Road hidden item: Stardust in the cove under the east wood
#define FLAG_ICHOR_HIDDEN_ECHO_CAVES_HEART_SCALE (FLAG_ICHOR_GENERAL2_START + 0x06B) // Ichor: Echo's caves hidden item: Heart Scale at the dark gallery's end
#define FLAG_ICHOR_HIDDEN_PAPHIA_ULTRA_BALL (FLAG_ICHOR_GENERAL2_START + 0x06C) // Ichor: Paphia hidden item: Ultra Ball behind the dovecote
#define FLAG_ICHOR_HIDDEN_PAPHIA_PEARL (FLAG_ICHOR_GENERAL2_START + 0x06D) // Ichor: Paphia hidden item: Pearl under the mirror by the jetty
#define FLAG_ICHOR_HIDDEN_NERAIDA_MYSTIC_WATER (FLAG_ICHOR_GENERAL2_START + 0x06E) // Ichor: Neraida falls hidden item: Mystic Water in the mill-race
#define FLAG_ICHOR_HIDDEN_NERAIDA_PEARL (FLAG_ICHOR_GENERAL2_START + 0x06F) // Ichor: Neraida falls hidden item: Pearl behind the shrine's basin
#define FLAG_ICHOR_HIDDEN_KALLIRHOE_REVIVE (FLAG_ICHOR_GENERAL2_START + 0x070) // Ichor: Spring of Kallirhoe hidden item: Revive in the nook under the cave rock
#define FLAG_ICHOR_HIDDEN_KALLIRHOE_PP_UP (FLAG_ICHOR_GENERAL2_START + 0x071) // Ichor: Spring of Kallirhoe hidden item: PP Up at the fall's rock
#define FLAG_ICHOR_HIDDEN_ECHO_CAVES_SHELL_BELL (FLAG_ICHOR_GENERAL2_START + 0x072) // Ichor: Echo's caves hidden item: Shell Bell in the Speaking Hall's west nook
#define FLAG_ICHOR_HIDDEN_NERAIDA_HEART_SCALE (FLAG_ICHOR_GENERAL2_START + 0x073) // Ichor: Neraida falls hidden item: Heart Scale at the ledge path's foot
#define FLAG_ICHOR_HIDDEN_NERAIDA_HONEY (FLAG_ICHOR_GENERAL2_START + 0x074) // Ichor: Neraida falls hidden item: Honey in Kerinthos's bee wall
#define FLAG_ICHOR_HIDDEN_SKANDEIA_BIG_PEARL (FLAG_ICHOR_GENERAL2_START + 0x075) // Ichor: Skandeia hidden item: Big Pearl in the harbor shrine's niche, among the shells
#define FLAG_ICHOR_HIDDEN_SKANDEIA_HEART_SCALE (FLAG_ICHOR_GENERAL2_START + 0x076) // Ichor: Skandeia hidden item: Heart Scale at the north slip's end
#define FLAG_ICHOR_SAW_BAD_GUESTS               (FLAG_ICHOR_GENERAL_START + 0x200) // Ichor: Skandeia: saw the Titan guests at Axylos's table (beat III-1C2)
#define FLAG_ICHOR_BAD_GUESTS_GONE              (FLAG_ICHOR_GENERAL_START + 0x201) // Ichor: Skandeia: drove the bad guests from Axylos's table; also hides them and Alethea there
#define FLAG_ICHOR_TRADED_TELKANVIL             (FLAG_ICHOR_GENERAL_START + 0x202) // Ichor: Skandeia: traded Bathykleia a Glyphlet for Ankyra the Telkanvil
#define FLAG_ICHOR_GOT_SOOTHE_BELL_EUODIA       (FLAG_ICHOR_GENERAL_START + 0x203) // Ichor: Skandeia: Euodia the perfumer's Soothe Bell (SCRIPT.md's GOT_SOOTHE_BELL is Akti's)
#define FLAG_ICHOR_LITHOS_HOME                  (FLAG_ICHOR_GENERAL_START + 0x204) // Ichor: Skandeia: Lithos, home after the climax, gave the Ability Capsule
#define FLAG_ICHOR_KNUCKLEBONES_SKANDEIA        (FLAG_ICHOR_GENERAL_START + 0x205) // Ichor: Skandeia: first knucklebones win against Phereklos (Big Pearl)
#define FLAG_ICHOR_GOT_SHINY_STONE_PYGMALION    (FLAG_ICHOR_GENERAL_START + 0x206) // Ichor: Paphia: Pygmalion's Shiny Stone, after the climax
#define FLAG_ICHOR_GOT_EROSIE_EGG               (FLAG_ICHOR_GENERAL_START + 0x207) // Ichor: Paphia: Peristera's Egg (Erosie)
#define FLAG_ICHOR_GOT_MIRROR_HERB              (FLAG_ICHOR_GENERAL_START + 0x208) // Ichor: Paphia: Leukippe's Mirror Herb, after the Foam Laurel
#define FLAG_ICHOR_TRADED_HIMEROW               (FLAG_ICHOR_GENERAL_START + 0x209) // Ichor: Paphia: traded Lysis a Galenyon for Pothos the Himerow
#define FLAG_ICHOR_GOT_METRONOME                (FLAG_ICHOR_GENERAL_START + 0x20A) // Ichor: Neraida falls: Myles the miller's Metronome
#define FLAG_ICHOR_SAW_GEAR_BOX                 (FLAG_ICHOR_GENERAL_START + 0x20D) // Ichor: Route 23: saw Skyllias's box of gears off Antikythera (set there; read in the divers' house)
#define FLAG_ICHOR_CROSSED_ROUTE22              (FLAG_ICHOR_GENERAL_START + 0x213) // Ichor: Act III: III-1B3, rounded Malea and landed at Skandeia (hides Nausikles on Melos's jetty)
#define FLAG_ICHOR_VISITED_SKANDEIA             (FLAG_ICHOR_GENERAL_START + 0x214) // Ichor: Act III: Skandeia visited (fly target, MAPSEC_KYTHERA_ISLE)
#define FLAG_ICHOR_EUPLOIA_KEPT                 (FLAG_ICHOR_GENERAL_START + 0x215) // Ichor: Act III: III-1C, beat Molybdos; the Euploia isn't requisitioned
#define FLAG_ICHOR_ALETHEA_REJOINED             (FLAG_ICHOR_GENERAL_START + 0x216) // Ichor: Act III: III-1C2, Alethea met you on Skandeia's main street
#define FLAG_ICHOR_SAILED_FOR_KNOSSA            (FLAG_ICHOR_GENERAL_START + 0x217) // Ichor: Act III: III-1I, sailed from Skandeia for Amnisos
#define FLAG_ICHOR_SKANDEIA_CALL                (FLAG_ICHOR_GENERAL_START + 0x218) // Ichor: Act III: the Euploia's call at Skandeia between Amnisos and Gytheion (set by the Knossa writer's departure)
#define FLAG_ICHOR_SAILED_FOR_GYTHEION          (FLAG_ICHOR_GENERAL_START + 0x219) // Ichor: Act III: sailed on from Skandeia's call for Gytheion (Route 24 starts from it)
#define FLAG_ICHOR_HIDE_ALETHEA_CALL            (FLAG_ICHOR_GENERAL_START + 0x21A) // Ichor: Act III: Skandeia: hides Alethea at the gangplank (shown only during the call)
#define FLAG_ICHOR_HIDE_ALETHEA_SKANDEIA        (FLAG_ICHOR_GENERAL_START + 0x21B) // Ichor: Act III: Skandeia: hides Alethea at Axylos's door (shown from III-1C2 until the bad guests go)
#define FLAG_ICHOR_HIDE_MOLYBDOS                (FLAG_ICHOR_GENERAL_START + 0x21C) // Ichor: Act III: Skandeia: hides Molybdos once he is beaten
#define FLAG_ICHOR_HIDE_SKANDEIA_PORTERS        (FLAG_ICHOR_GENERAL_START + 0x21D) // Ichor: Act III: Skandeia: hides the Titanborn porters (from VAR_ICHOR_ACT3 6)
#define FLAG_ICHOR_HIDE_KRONIST_SKANDEIA        (FLAG_ICHOR_GENERAL_START + 0x21E) // Ichor: Act III: Skandeia: hides the Kronist (after the climax, VAR_ICHOR_ACT3 19)
#define FLAG_ICHOR_HEARD_KRONIST                (FLAG_ICHOR_GENERAL_START + 0x21F) // Ichor: Act III: Skandeia: the Kronist has preached at you once (his walk-past trigger)
#define FLAG_ICHOR_ITEM_SKANDEIA_SEA_INCENSE    (FLAG_ICHOR_GENERAL_START + 0x22F) // Ichor: Act III item ball: Skandeia's Sea Incense at the pocket beach's end
#define FLAG_ICHOR_HIDE_ALETHEA_FOAM_ROAD       (FLAG_ICHOR_GENERAL_START + 0x240) // Ichor: Foam Road: hides Alethea at Aphrodite's rock once her scene is done (beat III-1D)
#define FLAG_ICHOR_HIDE_KASSITEROS              (FLAG_ICHOR_GENERAL_START + 0x241) // Ichor: Foam Road: hides Kassiteros after Knossa (VAR_ICHOR_ACT3 >= 6)
#define FLAG_ICHOR_HIDE_MESSENGER_FOAM_ROAD     (FLAG_ICHOR_GENERAL_START + 0x242) // Ichor: Foam Road: hides Hermes the messenger at the great herm (theoxenia E1; move to the theoxenia range with ichor-engine)
#define FLAG_ICHOR_TALARIA_LENT                 (FLAG_ICHOR_GENERAL_START + 0x243) // Ichor: Foam Road: lent the Talaria to the messenger (theoxenia E1; move to the theoxenia range with ichor-engine)
#define FLAG_ICHOR_FOAM_ROAD_DRUMS_MOVED        (FLAG_ICHOR_GENERAL_START + 0x244) // Ichor: Foam Road: the Girdle of Herakles moved the quarry's column drums
#define FLAG_ICHOR_ITEM_FOAM_ROAD_HYPER_POTION  (FLAG_ICHOR_GENERAL_START + 0x245) // Ichor: Foam Road: the jar on the reef spit past Pontinos
#define FLAG_ICHOR_ITEM_FOAM_ROAD_RARE_CANDY    (FLAG_ICHOR_GENERAL_START + 0x246) // Ichor: Foam Road: the jar on the quarry's top step (the Girdle)
#define FLAG_ICHOR_ITEM_FOAM_ROAD_PRETTY_FEATHER (FLAG_ICHOR_GENERAL_START + 0x247) // Ichor: Foam Road: the Pretty Feathers in the cliff cove (the Horn)
#define FLAG_ICHOR_SAW_KALLIRHOE                (FLAG_ICHOR_GENERAL_START + 0x248) // Ichor: Spring of Kallirhoe: saw the youth at the pool with Alethea (beat III-1E)
#define FLAG_ICHOR_HIDE_ALETHEA_KALLIRHOE       (FLAG_ICHOR_GENERAL_START + 0x249) // Ichor: Spring of Kallirhoe: hides Alethea at the spring
#define FLAG_ICHOR_HIDE_KALLIRHOE_MOTHER        (FLAG_ICHOR_GENERAL_START + 0x24A) // Ichor: Spring of Kallirhoe: hides the youth's mother (shown evenings and nights after the scene)
#define FLAG_ICHOR_KALLIRHOE_MYRTLE_CUT         (FLAG_ICHOR_GENERAL_START + 0x24B) // Ichor: Spring of Kallirhoe: Demeter's Sickle cut the myrtle on the back path
#define FLAG_ICHOR_ITEM_KALLIRHOE_MIRACLE_SEED  (FLAG_ICHOR_GENERAL_START + 0x24C) // Ichor: Spring of Kallirhoe: the Miracle Seed on the ledge behind the myrtle
#define FLAG_ICHOR_ITEM_ECHO_CAVES_BIG_PEARL    (FLAG_ICHOR_GENERAL_START + 0x24D) // Ichor: Echo's caves: the Big Pearl on the Speaking Hall's ledge
#define FLAG_ICHOR_ITEM_ECHO_CAVES_ZINC         (FLAG_ICHOR_GENERAL_START + 0x24E) // Ichor: Echo's caves: the Zinc in the dark gallery's dead end
#define FLAG_ICHOR_ITEM_ECHO_CAVES_TM_HYPER_VOICE (FLAG_ICHOR_GENERAL_START + 0x24F) // Ichor: Echo's caves: TM Hyper Voice on the sea mouth's rock (once it is a TM)
#define FLAG_ICHOR_ALETHEA_SAILED_KNOSSA        (FLAG_ICHOR_GENERAL_START + 0x250) // Ichor: Paphia: Alethea sailed for Knossa on the honey boat (beat III-1F)
#define FLAG_ICHOR_HIDE_ALETHEA_PAPHIA          (FLAG_ICHOR_GENERAL_START + 0x251) // Ichor: Paphia: hides Alethea and the honey boat's skipper on the jetty
#define FLAG_ICHOR_HIDE_HERMES_PAPHIA           (FLAG_ICHOR_GENERAL_START + 0x252) // Ichor: Paphia: hides Hermes at the gate herm (theoxenia E1; move to the theoxenia range with ichor-engine)
#define FLAG_ICHOR_GALLERY_DONE                 (FLAG_ICHOR_GENERAL_START + 0x253) // Ichor: Temple of Aphrodite: first reached Galatea's dais
#define FLAG_ICHOR_GALATEA_FALLS_HINT           (FLAG_ICHOR_GENERAL_START + 0x254) // Ichor: Temple of Aphrodite: Galatea sent the player to the Neraida falls
#define FLAG_ICHOR_GOT_TM_DAZZLING_GLEAM        (FLAG_ICHOR_GENERAL_START + 0x255) // Ichor: Temple of Aphrodite: Galatea's TM Dazzling Gleam
#define FLAG_ICHOR_GALLERY_MIRROR_P2_BIT0       (FLAG_ICHOR_GENERAL_START + 0x256) // Ichor: Temple of Aphrodite: turnable mirror P2's facing, bit 0
#define FLAG_ICHOR_GALLERY_MIRROR_P2_BIT1       (FLAG_ICHOR_GENERAL_START + 0x257) // Ichor: Temple of Aphrodite: turnable mirror P2's facing, bit 1
#define FLAG_ICHOR_GALLERY_MIRROR_P3_BIT0       (FLAG_ICHOR_GENERAL_START + 0x258) // Ichor: Temple of Aphrodite: turnable mirror P3's facing, bit 0
#define FLAG_ICHOR_GALLERY_MIRROR_P3_BIT1       (FLAG_ICHOR_GENERAL_START + 0x259) // Ichor: Temple of Aphrodite: turnable mirror P3's facing, bit 1
#define FLAG_ICHOR_ITEM_TEMPLE_APHRODITE_MAX_REVIVE (FLAG_ICHOR_GENERAL_START + 0x25A) // Ichor: Temple of Aphrodite: the jar in Anthousa's alcove
#define FLAG_ICHOR_ITEM_NERAIDA_MAX_REPEL       (FLAG_ICHOR_GENERAL_START + 0x25C) // Ichor: Neraida falls: the jar on the top terrace
#define FLAG_ICHOR_ITEM_NERAIDA_PROTEIN         (FLAG_ICHOR_GENERAL_START + 0x25D) // Ichor: Neraida falls: the Protein on a rock in the upper pool
#define FLAG_ICHOR_KRENAIA_TOLD                 (FLAG_ICHOR_GENERAL_START + 0x25E) // Ichor: Neraida falls: Krenaia told the laureled player about the silent falls and the horn (beat III-1H)
#define FLAG_ICHOR_ITEM_FOAM_ROAD_PEARL_STRING  (FLAG_ICHOR_GENERAL_START + 0x260) // Ichor: Foam Road item ball: Pearl String on the islet
#define FLAG_ICHOR_ITEM_FOAM_ROAD_ULTRA_BALL    (FLAG_ICHOR_GENERAL_START + 0x261) // Ichor: Foam Road item ball: Ultra Ball in the barley by the bay
#define FLAG_ICHOR_ITEM_PAPHIA_LOVE_BALL        (FLAG_ICHOR_GENERAL_START + 0x262) // Ichor: Paphia item ball: Love Ball on the green by the Asclepeion
#define FLAG_ICHOR_ITEM_NERAIDA_BIG_ROOT        (FLAG_ICHOR_GENERAL_START + 0x263) // Ichor: Neraida falls item ball: Big Root in the east bank's meadow
#define FLAG_ICHOR_ITEM_NERAIDA_MAX_POTION      (FLAG_ICHOR_GENERAL_START + 0x264) // Ichor: Neraida falls item ball: Max Potion on the plunge pool's west bank
#define FLAG_ICHOR_ITEM_NERAIDA_ELIXIR          (FLAG_ICHOR_GENERAL_START + 0x265) // Ichor: Neraida falls item ball: Elixir on the upper shelf
#define FLAG_ICHOR_NERAIDA_BERRIES_PLANTED (FLAG_ICHOR_GENERAL_START + 0x25B) // Ichor: initialized the falls' first-fruits trees once
#define FLAG_ICHOR_ITEM_R7_SHRINE               (FLAG_ICHOR_GENERAL2_START + 0x100) // Ichor: Route 7: the jar at Kronos's stone, behind the Hammer rubble
#define FLAG_ICHOR_ITEM_R7_TERRACE              (FLAG_ICHOR_GENERAL2_START + 0x101) // Ichor: Route 7: the vine terrace behind the column drum (Girdle)
#define FLAG_ICHOR_R7_VINES_CUT                 (FLAG_ICHOR_GENERAL2_START + 0x102) // Ichor: Route 7: the old vineyard's vines cut (Sickle)
#define FLAG_ICHOR_R8_REEDS_CUT                 (FLAG_ICHOR_GENERAL2_START + 0x103) // Ichor: Route 8: the reed thicket on the south boardwalk cut (Sickle)
#define FLAG_ICHOR_ITEM_R8_GLA                  (FLAG_ICHOR_GENERAL2_START + 0x104) // Ichor: Route 8: the jar on Gla's island (Conch)
#define FLAG_ICHOR_ITEM_R8_ISLET                (FLAG_ICHOR_GENERAL2_START + 0x105) // Ichor: Route 8: the reed islet at the boardwalk's end
#define FLAG_ICHOR_R8_FISHER_GIFT               (FLAG_ICHOR_GENERAL2_START + 0x106) // Ichor: Route 8: the eel-fisher's gift
#define FLAG_ICHOR_ITEM_KATAVOTHRA_GALLERY      (FLAG_ICHOR_GENERAL2_START + 0x107) // Ichor: Kopais katavothres: the side gallery behind the rubble
#define FLAG_ICHOR_ITEM_KATAVOTHRA_ISLET        (FLAG_ICHOR_GENERAL2_START + 0x108) // Ichor: Kopais katavothres: the rock in the channel (Conch)
#define FLAG_ICHOR_ITEM_KATAVOTHRA_PASSAGE      (FLAG_ICHOR_GENERAL2_START + 0x109) // Ichor: Kopais katavothres: the main passage
#define FLAG_ICHOR_ITEM_LEBADEIA                (FLAG_ICHOR_GENERAL2_START + 0x10A) // Ichor: Lebadeia: the jar by the springs
#define FLAG_ICHOR_LEBADEIA_HONEY_TRADE         (FLAG_ICHOR_GENERAL2_START + 0x10B) // Ichor: Lebadeia: Euanthe's honey cakes, for Honey
#define FLAG_ICHOR_LEBADEIA_KEEPER_TALK         (FLAG_ICHOR_GENERAL2_START + 0x10C) // Ichor: Lebadeia: the Trophoneion's keeper told of the descent
#define FLAG_ICHOR_HIDDEN_ITEM_R7_SHRINE        (FLAG_ICHOR_GENERAL2_START + 0x10D) // Ichor: Route 7: under Kronos's stone
#define FLAG_ICHOR_HIDDEN_ITEM_KATAVOTHRA_SEEP  (FLAG_ICHOR_GENERAL2_START + 0x10E) // Ichor: Kopais katavothres: at the seep
#define FLAG_ICHOR_HIDDEN_ITEM_KATAVOTHRA_BONES (FLAG_ICHOR_GENERAL2_START + 0x10F) // Ichor: Kopais katavothres: among the old bones
#define FLAG_ICHOR_HIDDEN_ITEM_LEBADEIA_SPRING  (FLAG_ICHOR_GENERAL2_START + 0x110) // Ichor: Lebadeia: by the spring of Lethe
#define FLAG_ICHOR_HIDDEN_ITEM_LEBADEIA_TEMENOS (FLAG_ICHOR_GENERAL2_START + 0x111) // Ichor: Lebadeia: in the temenos wall's corner
// Gulf (gulf.py): moved from +0x100-0x122 to +0x0D0-0x0F2 on merge, clear of Kopais and Nemea
#define FLAG_ICHOR_AIGION_FISHER_GIFT           (FLAG_ICHOR_GENERAL2_START + 0x0D0) // Ichor: Gulf (gulf.py): AIGION_FISHER_GIFT
#define FLAG_ICHOR_AIGION_OATH_GIFT             (FLAG_ICHOR_GENERAL2_START + 0x0D1) // Ichor: Gulf (gulf.py): AIGION_OATH_GIFT
#define FLAG_ICHOR_AIGION_PRIEST_GIFT           (FLAG_ICHOR_GENERAL2_START + 0x0D2) // Ichor: Gulf (gulf.py): AIGION_PRIEST_GIFT
#define FLAG_ICHOR_ITEM_AIGION                  (FLAG_ICHOR_GENERAL2_START + 0x0D3) // Ichor: Gulf (gulf.py): ITEM_AIGION
#define FLAG_ICHOR_ITEM_AIGION_HELIKE           (FLAG_ICHOR_GENERAL2_START + 0x0D4) // Ichor: Gulf (gulf.py): ITEM_AIGION_HELIKE
#define FLAG_ICHOR_ITEM_KIRRHA                  (FLAG_ICHOR_GENERAL2_START + 0x0D5) // Ichor: Gulf (gulf.py): ITEM_KIRRHA
#define FLAG_ICHOR_ITEM_KIRRHA_ISLET            (FLAG_ICHOR_GENERAL2_START + 0x0D6) // Ichor: Gulf (gulf.py): ITEM_KIRRHA_ISLET
#define FLAG_ICHOR_ITEM_KORYKIAN_CHAMBER        (FLAG_ICHOR_GENERAL2_START + 0x0D7) // Ichor: Gulf (gulf.py): ITEM_KORYKIAN_CHAMBER
#define FLAG_ICHOR_ITEM_KORYKIAN_GROTTO         (FLAG_ICHOR_GENERAL2_START + 0x0D8) // Ichor: Gulf (gulf.py): ITEM_KORYKIAN_GROTTO
#define FLAG_ICHOR_ITEM_KORYKIAN_HALL           (FLAG_ICHOR_GENERAL2_START + 0x0D9) // Ichor: Gulf (gulf.py): ITEM_KORYKIAN_HALL
#define FLAG_ICHOR_ITEM_KORYKIAN_ISLET          (FLAG_ICHOR_GENERAL2_START + 0x0DA) // Ichor: Gulf (gulf.py): ITEM_KORYKIAN_ISLET
#define FLAG_ICHOR_ITEM_KORYKIAN_SANCTUM        (FLAG_ICHOR_GENERAL2_START + 0x0DB) // Ichor: Gulf (gulf.py): ITEM_KORYKIAN_SANCTUM
#define FLAG_ICHOR_ITEM_R11_FALLS               (FLAG_ICHOR_GENERAL2_START + 0x0DC) // Ichor: Gulf (gulf.py): ITEM_R11_FALLS
#define FLAG_ICHOR_ITEM_R11_ISLET               (FLAG_ICHOR_GENERAL2_START + 0x0DD) // Ichor: Gulf (gulf.py): ITEM_R11_ISLET
#define FLAG_ICHOR_ITEM_R9_DAULIS               (FLAG_ICHOR_GENERAL2_START + 0x0DE) // Ichor: Gulf (gulf.py): ITEM_R9_DAULIS
#define FLAG_ICHOR_ITEM_R9_RAVINE               (FLAG_ICHOR_GENERAL2_START + 0x0DF) // Ichor: Gulf (gulf.py): ITEM_R9_RAVINE
#define FLAG_ICHOR_KIRRHA_BEE_ASKED             (FLAG_ICHOR_GENERAL2_START + 0x0E0) // Ichor: Gulf (gulf.py): KIRRHA_BEE_ASKED
#define FLAG_ICHOR_KIRRHA_BEE_FOUND             (FLAG_ICHOR_GENERAL2_START + 0x0E1) // Ichor: Gulf (gulf.py): KIRRHA_BEE_FOUND
#define FLAG_ICHOR_KIRRHA_BELL_GIFT             (FLAG_ICHOR_GENERAL2_START + 0x0E2) // Ichor: Gulf (gulf.py): KIRRHA_BELL_GIFT
#define FLAG_ICHOR_KIRRHA_WATER_GIFT            (FLAG_ICHOR_GENERAL2_START + 0x0E3) // Ichor: Gulf (gulf.py): KIRRHA_WATER_GIFT
#define FLAG_ICHOR_KORYKIAN_THORNWEB_BURNT      (FLAG_ICHOR_GENERAL2_START + 0x0E4) // Ichor: Gulf (gulf.py): KORYKIAN_THORNWEB_BURNT
#define FLAG_ICHOR_KORYKIAN_WEB_BURNT           (FLAG_ICHOR_GENERAL2_START + 0x0E5) // Ichor: Gulf (gulf.py): KORYKIAN_WEB_BURNT
#define FLAG_ICHOR_R11_RUBBLE_BROKEN            (FLAG_ICHOR_GENERAL2_START + 0x0E6) // Ichor: Gulf (gulf.py): R11_RUBBLE_BROKEN
#define FLAG_ICHOR_R9_GREAT_BOULDER             (FLAG_ICHOR_GENERAL2_START + 0x0E7) // Ichor: Gulf (gulf.py): R9_GREAT_BOULDER
#define FLAG_ICHOR_R9_SCREE_BROKEN              (FLAG_ICHOR_GENERAL2_START + 0x0E8) // Ichor: Gulf (gulf.py): R9_SCREE_BROKEN
#define FLAG_ICHOR_R9_THICKET_CUT               (FLAG_ICHOR_GENERAL2_START + 0x0E9) // Ichor: Gulf (gulf.py): R9_THICKET_CUT
#define FLAG_ICHOR_HIDDEN_ITEM_AIGION_CAMP      (FLAG_ICHOR_GENERAL2_START + 0x0EA) // Ichor: Gulf (gulf.py): HIDDEN_ITEM_AIGION_CAMP
#define FLAG_ICHOR_HIDDEN_ITEM_AIGION_TERRACE   (FLAG_ICHOR_GENERAL2_START + 0x0EB) // Ichor: Gulf (gulf.py): HIDDEN_ITEM_AIGION_TERRACE
#define FLAG_ICHOR_HIDDEN_ITEM_KIRRHA_HEADLAND  (FLAG_ICHOR_GENERAL2_START + 0x0EC) // Ichor: Gulf (gulf.py): HIDDEN_ITEM_KIRRHA_HEADLAND
#define FLAG_ICHOR_HIDDEN_ITEM_KIRRHA_SHRINE    (FLAG_ICHOR_GENERAL2_START + 0x0ED) // Ichor: Gulf (gulf.py): HIDDEN_ITEM_KIRRHA_SHRINE
#define FLAG_ICHOR_HIDDEN_ITEM_KORYKIAN_ALTAR   (FLAG_ICHOR_GENERAL2_START + 0x0EE) // Ichor: Gulf (gulf.py): HIDDEN_ITEM_KORYKIAN_ALTAR
#define FLAG_ICHOR_HIDDEN_ITEM_KORYKIAN_BAY     (FLAG_ICHOR_GENERAL2_START + 0x0EF) // Ichor: Gulf (gulf.py): HIDDEN_ITEM_KORYKIAN_BAY
#define FLAG_ICHOR_HIDDEN_ITEM_R9_TOMB          (FLAG_ICHOR_GENERAL2_START + 0x0F0) // Ichor: Gulf (gulf.py): HIDDEN_ITEM_R9_TOMB
#define FLAG_ICHOR_R9_SPRING_GIFT               (FLAG_ICHOR_GENERAL2_START + 0x0F1) // Ichor: Gulf (gulf.py): R9 spring keeper's gift
#define FLAG_ICHOR_R11_SPRING_GIFT              (FLAG_ICHOR_GENERAL2_START + 0x0F2) // Ichor: Gulf (gulf.py): R11 nymph spring's gift
#define FLAG_ICHOR_ITEM_R13_GLADE               (FLAG_ICHOR_GENERAL2_START + 0x120) // Ichor: Route 13 glade jar behind the thicket
#define FLAG_ICHOR_ITEM_R13_CELL                (FLAG_ICHOR_GENERAL2_START + 0x121) // Ichor: Route 13 hermit's cell jar behind the rubble
#define FLAG_ICHOR_ITEM_R13_CRAG                (FLAG_ICHOR_GENERAL2_START + 0x122) // Ichor: Route 13 crag jar up the handholds (climbing relic)
#define FLAG_ICHOR_R13_BEEKEEPER_GIFT           (FLAG_ICHOR_GENERAL2_START + 0x123) // Ichor: Route 13 beekeeper's gift
#define FLAG_ICHOR_ITEM_NEMEA_TRACK             (FLAG_ICHOR_GENERAL2_START + 0x124) // Ichor: Nemea stadium jar
#define FLAG_ICHOR_ITEM_NEMEA_ISLET             (FLAG_ICHOR_GENERAL2_START + 0x125) // Ichor: Nemea river islet jar (Conch)
#define FLAG_ICHOR_NEMEA_HONEY_GIVEN            (FLAG_ICHOR_GENERAL2_START + 0x126) // Ichor: Molorchos got his honey
#define FLAG_ICHOR_NEMEA_PALAESTRA_GIFT         (FLAG_ICHOR_GENERAL2_START + 0x127) // Ichor: palaestra trainer's gift
#define FLAG_ICHOR_NEMEA_LION_BOULDER           (FLAG_ICHOR_GENERAL2_START + 0x128) // Ichor: lion's den boulder split (Hephaestus's Hammer)
#define FLAG_ICHOR_ITEM_R14_GULLY               (FLAG_ICHOR_GENERAL2_START + 0x129) // Ichor: Route 14 gully jar behind the rubble
#define FLAG_ICHOR_ITEM_R14_ISLET               (FLAG_ICHOR_GENERAL2_START + 0x12A) // Ichor: Route 14 gorge islet jar (Conch)
#define FLAG_ICHOR_R14_GREAT_BOULDER            (FLAG_ICHOR_GENERAL2_START + 0x12B) // Ichor: Route 14 great boulder split
#define FLAG_ICHOR_ITEM_TRETOS_HEAL             (FLAG_ICHOR_GENERAL2_START + 0x12C) // Ichor: Tretos jar
#define FLAG_ICHOR_ITEM_TRETOS_BALL             (FLAG_ICHOR_GENERAL2_START + 0x12D) // Ichor: Tretos jar behind the cobweb
#define FLAG_ICHOR_ITEM_TRETOS_POOL             (FLAG_ICHOR_GENERAL2_START + 0x12E) // Ichor: Tretos pool islet jar (Conch)
#define FLAG_ICHOR_ITEM_TRETOS_DEEP             (FLAG_ICHOR_GENERAL2_START + 0x12F) // Ichor: Tretos deep jar behind the thornweb
#define FLAG_ICHOR_HIDE_TRETOS_WEB              (FLAG_ICHOR_GENERAL2_START + 0x130) // Ichor: Tretos cobweb burnt
#define FLAG_ICHOR_HIDE_TRETOS_THORNWEB         (FLAG_ICHOR_GENERAL2_START + 0x131) // Ichor: Tretos thornweb burnt
#define FLAG_ICHOR_TRETOS_GREAT_BOULDER         (FLAG_ICHOR_GENERAL2_START + 0x132) // Ichor: Tretos great boulder split
#define FLAG_ICHOR_HIDDEN_ITEM_NEMEA_MOUND      (FLAG_ICHOR_GENERAL2_START + 0x133) // Ichor: Nemea, at Opheltes's mound
#define FLAG_ICHOR_HIDDEN_ITEM_NEMEA_SPRING     (FLAG_ICHOR_GENERAL2_START + 0x134) // Ichor: Nemea, by the Langia spring
#define FLAG_ICHOR_HIDDEN_ITEM_TRETOS_BONES     (FLAG_ICHOR_GENERAL2_START + 0x135) // Ichor: Tretos, in the bones
#define FLAG_ICHOR_HIDDEN_ITEM_TRETOS_SEEP      (FLAG_ICHOR_GENERAL2_START + 0x136) // Ichor: Tretos, at the seep
#define FLAG_ICHOR_R14_HERDSMAN_GIFT            (FLAG_ICHOR_GENERAL2_START + 0x137) // Ichor: Route 14 herdsman's gift
#define FLAG_ICHOR_TRETOS_RUBBLE                (FLAG_ICHOR_GENERAL2_START + 0x138) // Ichor: Tretos rubble broken (Hammer)
#define FLAG_ICHOR_R13_RUBBLE                   (FLAG_ICHOR_GENERAL2_START + 0x139) // Ichor: Route 13 hermit's cell rubble broken
#define FLAG_ICHOR_R14_RUBBLE                   (FLAG_ICHOR_GENERAL2_START + 0x13A) // Ichor: Route 14 gully rubble broken
#define FLAG_ICHOR_ACT3_COMPLETE                (FLAG_ICHOR_GENERAL2_START + 0x1C0) // Ichor: League: Act III done (Elpis's line, III-12); the Act III builder sets it. Gates L-1 to L-5
#define FLAG_ICHOR_LEAGUE_DECREE                (FLAG_ICHOR_GENERAL2_START + 0x1C1) // Ichor: League L-1: heard Kerykos read the Archon's decree in Astyra
#define FLAG_ICHOR_IAPETOS_TRIED                (FLAG_ICHOR_GENERAL2_START + 0x1C2) // Ichor: League L-2: the trial of Iapetos in the Stoa; Alethea's exile lifted
#define FLAG_ICHOR_SENTENCES_HEARD              (FLAG_ICHOR_GENERAL2_START + 0x1C3) // Ichor: League L-3: heard the sentences in Akti (Phaedon, Hyperion, Rhea)
#define FLAG_ICHOR_PANTHEON_ENTERED             (FLAG_ICHOR_GENERAL2_START + 0x1C4) // Ichor: League: the Propylaia's guard let you into the Pantheon (Emerald's FLAG_ENTERED_ELITE_FOUR)
#define FLAG_ICHOR_ARCHON_DEFEATED              (FLAG_ICHOR_GENERAL2_START + 0x1C5) // Ichor: League L-8: beat Aristeides on the summit the first time
#define FLAG_ICHOR_KNOT_UNTIED                  (FLAG_ICHOR_GENERAL2_START + 0x1C6) // Ichor: League L-8: untied Medon's Knot with Aristeides
#define FLAG_ICHOR_HIDE_ARCHON_SUMMIT           (FLAG_ICHOR_GENERAL2_START + 0x1C7) // Ichor: League: Aristeides gone home from the summit after the first Hall of Heroes
#define FLAG_ICHOR_EPILOGUE_DONE                (FLAG_ICHOR_GENERAL2_START + 0x1C8) // Ichor: League L-10: the Klotheia epilogue in Elaia played
#define FLAG_ICHOR_HIDE_DECREE_CROWD            (FLAG_ICHOR_GENERAL2_START + 0x1C9) // Ichor: League L-1: Kerykos's decree crowd in Astyra dispersed
#define FLAG_ICHOR_HIDE_TRIAL_STOA              (FLAG_ICHOR_GENERAL2_START + 0x1CA) // Ichor: League L-2: the trial's people gone from the Stoa
#define FLAG_ICHOR_ITEM_ASCENT1_FULL_RESTORE    (FLAG_ICHOR_GENERAL2_START + 0x1CB) // Ichor: Ascent 1F: Full Restore on the beacon knoll
#define FLAG_ICHOR_ITEM_ASCENT1_ULTRA_BALL      (FLAG_ICHOR_GENERAL2_START + 0x1CC) // Ichor: Ascent 1F: Ultra Ball behind the drum
#define FLAG_ICHOR_ITEM_ASCENT1_MAX_REPEL       (FLAG_ICHOR_GENERAL2_START + 0x1CD) // Ichor: Ascent 1F: Max Repel in the torrent bed
#define FLAG_ICHOR_ITEM_ASCENT2_MAX_REVIVE      (FLAG_ICHOR_GENERAL2_START + 0x1CE) // Ichor: Ascent 2F: Max Revive on the cloud ledge
#define FLAG_ICHOR_ITEM_ASCENT2_PP_MAX          (FLAG_ICHOR_GENERAL2_START + 0x1CF) // Ichor: Ascent 2F: PP Max under the overhang
#define FLAG_ICHOR_ITEM_ASCENT3_FULL_HEAL       (FLAG_ICHOR_GENERAL2_START + 0x1D0) // Ichor: Ascent 3F: Full Heal by the snow cairn
#define FLAG_ICHOR_ITEM_ASCENT3_RARE_CANDY      (FLAG_ICHOR_GENERAL2_START + 0x1D1) // Ichor: Ascent 3F: Rare Candy past the rubble
#define FLAG_ICHOR_GOT_ASCENT_LEFTOVERS         (FLAG_ICHOR_GENERAL2_START + 0x1D2) // Ichor: Ascent 2F: the camp's cook gave Leftovers
#define FLAG_ICHOR_HIDDEN_ITEM_ASCENT1_STARDUST (FLAG_ICHOR_GENERAL2_START + 0x1D3) // Ichor: Ascent 1F: in the fallen climbers' stelai
#define FLAG_ICHOR_HIDDEN_ITEM_ASCENT2_BIG_NUGGET (FLAG_ICHOR_GENERAL2_START + 0x1D4) // Ichor: Ascent 2F: at the ledge's end in the cloud
#define FLAG_ICHOR_HIDDEN_ITEM_ASCENT3_COMET_SHARD (FLAG_ICHOR_GENERAL2_START + 0x1D5) // Ichor: Ascent 3F: in the snow by the last cairn
#define FLAG_ICHOR_HIDDEN_ITEM_ASCENT2_ELIXIR   (FLAG_ICHOR_GENERAL2_START + 0x1D6) // Ichor: Ascent 2F: behind the camp's second tent
#define FLAG_ICHOR_HIDDEN_ITEM_ASCENT3_STAR_PIECE (FLAG_ICHOR_GENERAL2_START + 0x1D7) // Ichor: Ascent 3F: on the summit shoulder above the stair
#define FLAG_ICHOR_ARRIVED_GYTHEION             (FLAG_ICHOR_GENERAL2_START + 0x4F0) // Ichor: Lakonia: III-5A, landed at Gytheion
#define FLAG_ICHOR_VISITED_GYTHEION             (FLAG_ICHOR_GENERAL2_START + 0x4F1) // Ichor: Lakonia: Gytheion visited (fly target)
#define FLAG_ICHOR_GYTHEION_DUSK                (FLAG_ICHOR_GENERAL2_START + 0x4F2) // Ichor: Lakonia: III-5B, the fisherman and Kleon's helmet
#define FLAG_ICHOR_SAW_LAKONIA                  (FLAG_ICHOR_GENERAL2_START + 0x4F3) // Ichor: Lakonia: III-5C, the town in view from Route 25
#define FLAG_ICHOR_LAKONIA_ARRIVED              (FLAG_ICHOR_GENERAL2_START + 0x4F4) // Ichor: Lakonia: III-5D, Gylippos at the agora
#define FLAG_ICHOR_VISITED_LAKONIA              (FLAG_ICHOR_GENERAL2_START + 0x4F5) // Ichor: Lakonia: Lakonia visited (fly target)
#define FLAG_ICHOR_RHEA_UNMASKED                (FLAG_ICHOR_GENERAL2_START + 0x4F6) // Ichor: Lakonia: III-5E, the helmet comes off
#define FLAG_ICHOR_IAPETOS_LAKONIA_DONE         (FLAG_ICHOR_GENERAL2_START + 0x4F7) // Ichor: Lakonia: III-5F, Iapetos beaten in the lane
#define FLAG_ICHOR_ALETHEA_READ_TABLET          (FLAG_ICHOR_GENERAL2_START + 0x4F8) // Ichor: Lakonia: III-5G, Alethea read the sealed tablet
#define FLAG_ICHOR_KLEON_GOT_KOURODIN           (FLAG_ICHOR_GENERAL2_START + 0x4F9) // Ichor: Lakonia: III-5H, Rhea gave Kleon her Kourodin
#define FLAG_ICHOR_KLEON_LAKONIA_DONE           (FLAG_ICHOR_GENERAL2_START + 0x4FA) // Ichor: Lakonia: III-5I, the clean battle in the ring
#define FLAG_ICHOR_LAKONIA_PARTED               (FLAG_ICHOR_GENERAL2_START + 0x4FB) // Ichor: Lakonia: III-5J, the goat paths
#define FLAG_ICHOR_HIDE_RHEA_LAKONIA            (FLAG_ICHOR_GENERAL2_START + 0x4FC) // Ichor: Lakonia: hides Rhea after III-5J (shown again at VAR_ICHOR_ACT3 19)
#define FLAG_ICHOR_HIDE_KLEON_LAKONIA           (FLAG_ICHOR_GENERAL2_START + 0x4FD) // Ichor: Lakonia: hides Kleon after III-5J
#define FLAG_ICHOR_HIDE_ALETHEA_LAKONIA         (FLAG_ICHOR_GENERAL2_START + 0x4FE) // Ichor: Lakonia: hides Alethea after III-5J
#define FLAG_ICHOR_HIDE_BRASIDAS_LAKONIA        (FLAG_ICHOR_GENERAL2_START + 0x4FF) // Ichor: Lakonia: hides Brasidas after III-5I
#define FLAG_ICHOR_CARRYING_FIG_CAKE            (FLAG_ICHOR_GENERAL2_START + 0x500) // Ichor: Lakonia: carrying Timaia's fig cake to Teleklos
#define FLAG_ICHOR_DELIVERED_FIG_CAKE           (FLAG_ICHOR_GENERAL2_START + 0x501) // Ichor: Lakonia: Teleklos ate the fig cake
#define FLAG_ICHOR_GOT_HEAT_ROCK_AMYKLAI        (FLAG_ICHOR_GENERAL2_START + 0x502) // Ichor: Lakonia: Polyboia's Heat Rock
#define FLAG_ICHOR_READ_SCYTALE                 (FLAG_ICHOR_GENERAL2_START + 0x503) // Ichor: Lakonia: read Gylippos's strap on Othryades's staff (Route 27)
#define FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_SHELL_1 (FLAG_ICHOR_GENERAL2_START + 0x504) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDE_ALETHEA_GYTHEION        (FLAG_ICHOR_GENERAL2_START + 0x505) // Ichor: Lakonia: hides Alethea on Gytheion's quay after III-5B
#define FLAG_ICHOR_HIDE_ROUTE25_HESTIA          (FLAG_ICHOR_GENERAL2_START + 0x506) // Ichor: Lakonia: hides the woman at the roofless farmhouse (E2)
#define FLAG_ICHOR_ITEM_GYTHEION_NET_BALL       (FLAG_ICHOR_GENERAL2_START + 0x507) // Ichor: Lakonia: Gytheion beach item
#define FLAG_ICHOR_ITEM_ROUTE25_MEADOW          (FLAG_ICHOR_GENERAL2_START + 0x508) // Ichor: Lakonia: Route 25 item
#define FLAG_ICHOR_ITEM_ROUTE25_FARM            (FLAG_ICHOR_GENERAL2_START + 0x509) // Ichor: Lakonia: Route 25 item
#define FLAG_ICHOR_ITEM_ROUTE25_WEST            (FLAG_ICHOR_GENERAL2_START + 0x50A) // Ichor: Lakonia: Route 25 item
#define FLAG_ICHOR_ITEM_ROUTE25_FIELD           (FLAG_ICHOR_GENERAL2_START + 0x50B) // Ichor: Lakonia: Route 25 item
#define FLAG_ICHOR_ITEM_ROUTE25_AMYKLAI         (FLAG_ICHOR_GENERAL2_START + 0x50C) // Ichor: Lakonia: Route 25 item
#define FLAG_ICHOR_ITEM_LAKONIA_MENELAION       (FLAG_ICHOR_GENERAL2_START + 0x50D) // Ichor: Lakonia: the Menelaion item
#define FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_SHELL_2 (FLAG_ICHOR_GENERAL2_START + 0x50E) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_SHELL_3 (FLAG_ICHOR_GENERAL2_START + 0x50F) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_SHELL_4 (FLAG_ICHOR_GENERAL2_START + 0x510) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_THEATER (FLAG_ICHOR_GENERAL2_START + 0x511) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_KRANAI  (FLAG_ICHOR_GENERAL2_START + 0x512) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_THRONE   (FLAG_ICHOR_GENERAL2_START + 0x513) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_FORD     (FLAG_ICHOR_GENERAL2_START + 0x514) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_MEADOW   (FLAG_ICHOR_GENERAL2_START + 0x515) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_TERRACE  (FLAG_ICHOR_GENERAL2_START + 0x516) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_SCREE    (FLAG_ICHOR_GENERAL2_START + 0x517) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_LAKONIA_MENELAION (FLAG_ICHOR_GENERAL2_START + 0x518) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_LAKONIA_AGOGE    (FLAG_ICHOR_GENERAL2_START + 0x519) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_HIDDEN_ITEM_LAKONIA_BRIDGE   (FLAG_ICHOR_GENERAL2_START + 0x51A) // Ichor: Lakonia: hidden item
#define FLAG_ICHOR_GOT_KINGS_ROCK_GYTHEION      (FLAG_ICHOR_GENERAL2_START + 0x520) // Ichor: Lakonia: Porphyris's King's Rock for three Shoal Shells (Gytheion dye-works)
#define FLAG_ICHOR_TRADED_KYNOKETOS             (FLAG_ICHOR_GENERAL2_START + 0x521) // Ichor: Lakonia: traded a Karkitox for Lysandros's Kynoketos MALEA
#define FLAG_ICHOR_GOT_SHINY_STONE_KRANAI       (FLAG_ICHOR_GENERAL2_START + 0x522) // Ichor: Lakonia: Klymene's Shiny Stone, after the climax (Kranai)
#define FLAG_ICHOR_GOT_LEFTOVERS_GYTHEION       (FLAG_ICHOR_GENERAL2_START + 0x523) // Ichor: Lakonia: Timaia's Leftovers, after the fig cake
#define FLAG_ICHOR_GOT_SCYTALE_STRAP            (FLAG_ICHOR_GENERAL2_START + 0x524) // Ichor: Lakonia: Gylippos's leather strap (the scytale)
#define FLAG_ICHOR_GOT_TM_BULK_UP               (FLAG_ICHOR_GENERAL2_START + 0x525) // Ichor: Lakonia: Dexippos's TM Bulk Up for finishing the black broth
#define FLAG_ICHOR_GOT_FOCUS_SASH               (FLAG_ICHOR_GENERAL2_START + 0x526) // Ichor: Lakonia: Archidamos's Focus Sash, after Kleon's ring
#define FLAG_ICHOR_GOT_CHOICE_BAND              (FLAG_ICHOR_GENERAL2_START + 0x527) // Ichor: Lakonia: Hipposthenes's Choice Band, for showing him a Geogrip
#define FLAG_ICHOR_GOT_SCOPE_LENS               (FLAG_ICHOR_GENERAL2_START + 0x528) // Ichor: Lakonia: Kleta's Scope Lens, for the cheese game at Orthia
#define FLAG_ICHOR_GOT_WISE_GLASSES             (FLAG_ICHOR_GENERAL2_START + 0x529) // Ichor: Lakonia: Chilon's Wise Glasses, for answering in the fewest words
#define FLAG_ICHOR_XENIA_LAKONIA                (FLAG_ICHOR_GENERAL2_START + 0x52A) // Ichor: Lakonia: Lichas has fed you (xenia)
#define FLAG_ICHOR_RING1_GATE                   (FLAG_ICHOR_GENERAL2_START + 0x450) // Ichor: Labyrinth Ring I: the gate brazier caught, the stair down is open
#define FLAG_ICHOR_R1_TIE_TAUGHT                (FLAG_ICHOR_GENERAL2_START + 0x451) // Ichor: Labyrinth Ring I: Ariadne's TIE IT HERE shown
#define FLAG_ICHOR_ITEM_R1_HYPER_POTION         (FLAG_ICHOR_GENERAL2_START + 0x452) // Ichor: Labyrinth Ring I: the thread lesson's Hyper Potion
#define FLAG_ICHOR_ITEM_R1_TM_ROCK_SLIDE        (FLAG_ICHOR_GENERAL2_START + 0x453) // Ichor: Labyrinth Ring I: Xenodike's TM Rock Slide
#define FLAG_ICHOR_ITEM_R1_HYPER_POTION_2       (FLAG_ICHOR_GENERAL2_START + 0x454) // Ichor: Labyrinth Ring I: the hidden anchor's Hyper Potion
#define FLAG_ICHOR_ITEM_R1_ETHER                (FLAG_ICHOR_GENERAL2_START + 0x455) // Ichor: Labyrinth Ring I: an Ether in the cave pocket
#define FLAG_ICHOR_HIDDEN_ITEM_R1_BRONZE_OBOL   (FLAG_ICHOR_GENERAL2_START + 0x456) // Ichor: Labyrinth Ring I: a Bronze Obol in a dead end
#define FLAG_ICHOR_HIDDEN_ITEM_R1_REVIVE        (FLAG_ICHOR_GENERAL2_START + 0x457) // Ichor: Labyrinth Ring I: a Revive in the cleft
#define FLAG_ICHOR_HIDDEN_ITEM_AMNISOS_PEARL    (FLAG_ICHOR_GENERAL2_START + 0x400) // Ichor: Knossa hidden: Amnisos, Pearl at the jetty's end
#define FLAG_ICHOR_HIDDEN_ITEM_AMNISOS_OBOL     (FLAG_ICHOR_GENERAL2_START + 0x401) // Ichor: Knossa hidden: Amnisos, Bronze Obol behind the harbor shrine
#define FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_OLIVE_OIL (FLAG_ICHOR_GENERAL2_START + 0x402) // Ichor: Knossa hidden: the Bull Road, Olive Oil behind the great herm
#define FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_SILVER_OWL (FLAG_ICHOR_GENERAL2_START + 0x403) // Ichor: Knossa hidden: the Bull Road, Silver Owl in the cutting
#define FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_STAR_PIECE (FLAG_ICHOR_GENERAL2_START + 0x404) // Ichor: Knossa hidden: the Bull Road, Star Piece in the spring trough
#define FLAG_ICHOR_HIDDEN_ITEM_BULL_ROAD_MAX_ETHER (FLAG_ICHOR_GENERAL2_START + 0x405) // Ichor: Knossa hidden: the Bull Road, Max Ether under the oldest olive
#define FLAG_ICHOR_HIDDEN_ITEM_VINEYARD_WINE    (FLAG_ICHOR_GENERAL2_START + 0x406) // Ichor: Knossa hidden: the vineyard, Wine in the walled corner
#define FLAG_ICHOR_HIDDEN_ITEM_VINEYARD_ELIXIR  (FLAG_ICHOR_GENERAL2_START + 0x407) // Ichor: Knossa hidden: the vineyard, Elixir under the vintner's sign
#define FLAG_ICHOR_HIDDEN_ITEM_BRONZE_HEEL_METAL_COAT (FLAG_ICHOR_GENERAL2_START + 0x408) // Ichor: Knossa hidden: the Bronze Heel, Metal Coat at the point
#define FLAG_ICHOR_HIDDEN_ITEM_BRONZE_HEEL_STARDUST (FLAG_ICHOR_GENERAL2_START + 0x409) // Ichor: Knossa hidden: the Bronze Heel, Stardust in the ankle's hollow
#define FLAG_ICHOR_HIDDEN_ITEM_PALACE_SILVER_OWL (FLAG_ICHOR_GENERAL2_START + 0x40A) // Ichor: Knossa hidden: the palace, Silver Owl under the gypsum bench
#define FLAG_ICHOR_HIDDEN_ITEM_PALACE_STAR_PIECE (FLAG_ICHOR_GENERAL2_START + 0x40B) // Ichor: Knossa hidden: the palace, Star Piece in the light well
#define FLAG_ICHOR_HIDDEN_ITEM_PALACE_GOLD_STATER (FLAG_ICHOR_GENERAL2_START + 0x40C) // Ichor: Knossa hidden: the palace, Gold Stater by the horns
#define FLAG_ICHOR_ARRIVED_KNOSSA               (FLAG_ICHOR_GENERAL2_START + 0x40D) // Ichor: Knossa: III-3A, landed at Amnisos and met Alethea on the quay
#define FLAG_ICHOR_VISITED_AMNISOS              (FLAG_ICHOR_GENERAL2_START + 0x40E) // Ichor: Knossa: Amnisos visited (fly; heal location its Asclepeion)
#define FLAG_ICHOR_MET_ARIADNE                  (FLAG_ICHOR_GENERAL2_START + 0x40F) // Ichor: Knossa: III-3D, Scene A in the Throne Room
#define FLAG_ICHOR_FIRST_LEAP                   (FLAG_ICHOR_GENERAL2_START + 0x410) // Ichor: Knossa: III-3E, the first clean leap over the Gentle Bull
#define FLAG_ICHOR_MILON_PRACTICE               (FLAG_ICHOR_GENERAL2_START + 0x411) // Ichor: Knossa: the Bull Road, Milon's practice leap landed clean (his Lum Berry)
#define FLAG_ICHOR_SHOWED_KLEON_TABLET          (FLAG_ICHOR_GENERAL2_START + 0x412) // Ichor: Knossa: III-3O, Scene K, Kleon read Iapetos's hand and left
#define FLAG_ICHOR_ALETHEA_TOLD                 (FLAG_ICHOR_GENERAL2_START + 0x413) // Ichor: Knossa: III-3O, Alethea heard about Phaedon in the court
#define FLAG_ICHOR_DAPHNE_LETTER_KNOSSA         (FLAG_ICHOR_GENERAL2_START + 0x414) // Ichor: Knossa: III-4, Daphne's letter read on Amnisos's quay
#define FLAG_ICHOR_CAUGHT_ASTERION              (FLAG_ICHOR_GENERAL2_START + 0x415) // Ichor: Knossa: Asterion stepped into your ball in the court (LABYRINTH §10)
#define FLAG_ICHOR_LEAP_PRIZE_3                 (FLAG_ICHOR_GENERAL2_START + 0x416) // Ichor: Knossa: Sarpedon's prize for 3 leaps (Olive Oil x5)
#define FLAG_ICHOR_LEAP_PRIZE_5                 (FLAG_ICHOR_GENERAL2_START + 0x417) // Ichor: Knossa: Sarpedon's prize for 5 leaps (TM Body Slam)
#define FLAG_ICHOR_LEAP_PRIZE_10                (FLAG_ICHOR_GENERAL2_START + 0x418) // Ichor: Knossa: Sarpedon's prize for 10 leaps
#define FLAG_ICHOR_LEAP_PRIZE_20                (FLAG_ICHOR_GENERAL2_START + 0x419) // Ichor: Knossa: Sarpedon's prize for 20 leaps (a palace-herd Taurivet)
#define FLAG_ICHOR_GOT_KYDON_HONEY              (FLAG_ICHOR_GENERAL2_START + 0x41A) // Ichor: Knossa: Amnisos, Kydon's three jars of thyme honey
#define FLAG_ICHOR_GOT_KYDON_LEFTOVERS          (FLAG_ICHOR_GENERAL2_START + 0x41B) // Ichor: Knossa: Amnisos, Kydon's good jar (Leftovers) after the raid
#define FLAG_ICHOR_KNUCKLEBONES_AMNISOS         (FLAG_ICHOR_GENERAL2_START + 0x41C) // Ichor: Knossa: Amnisos, beat Lykastos, the Double Axe's champion (TM Taunt)
#define FLAG_ICHOR_BONES_KRESSA                 (FLAG_ICHOR_GENERAL2_START + 0x41D) // Ichor: Knossa: Amnisos, beat Kressa at knucklebones (Olive Oil)
#define FLAG_ICHOR_BONES_DORION                 (FLAG_ICHOR_GENERAL2_START + 0x41E) // Ichor: Knossa: Amnisos, beat Dorion at knucklebones (Wine)
#define FLAG_ICHOR_BROKEN_RING_2                (FLAG_ICHOR_GENERAL2_START + 0x41F) // Ichor: Knossa: Amnisos, Aithon's guest-gift (xenia chain link 2)
#define FLAG_ICHOR_GOT_FOCUS_BAND_KNOSSA        (FLAG_ICHOR_GENERAL2_START + 0x420) // Ichor: Knossa: Amnisos, Euanthe's Focus Band after the first leap
#define FLAG_ICHOR_TRADED_TELCHIS               (FLAG_ICHOR_GENERAL2_START + 0x421) // Ichor: Knossa: Amnisos, traded Polypos an Aphrell for Telchis
#define FLAG_ICHOR_GOT_BOMBYLIA_HONEY           (FLAG_ICHOR_GENERAL2_START + 0x422) // Ichor: Knossa: the Bull Road, Bombylia's two jars of honey
#define FLAG_ICHOR_FOSSIL_DUG                   (FLAG_ICHOR_GENERAL2_START + 0x423) // Ichor: Knossa: the Bronze Heel, dug one fossil from the tide ledge
#define FLAG_ICHOR_GOT_AKESTOR_SALVE            (FLAG_ICHOR_GENERAL2_START + 0x424) // Ichor: Knossa: Amnisos Asclepeion, Akestor's gift
#define FLAG_ICHOR_HIDE_ALETHEA_AMNISOS_QUAY    (FLAG_ICHOR_GENERAL2_START + 0x425) // Ichor: Knossa: hide Alethea on Amnisos's quay
#define FLAG_ICHOR_HIDE_ALETHEA_HEEL            (FLAG_ICHOR_GENERAL2_START + 0x426) // Ichor: Knossa: hide Alethea at the Bronze Heel
#define FLAG_ICHOR_HIDE_ALETHEA_MEGARON         (FLAG_ICHOR_GENERAL2_START + 0x427) // Ichor: Knossa: hide Alethea in the Queen's Megaron
#define FLAG_ICHOR_HIDE_ALETHEA_COURT           (FLAG_ICHOR_GENERAL2_START + 0x428) // Ichor: Knossa: hide Alethea in the Central Court
#define FLAG_ICHOR_HIDE_KLEON_KNOSSA            (FLAG_ICHOR_GENERAL2_START + 0x429) // Ichor: Knossa: hide Kleon in the palace court (Scene K)
#define FLAG_ICHOR_HIDE_PALACE_GRUNTS           (FLAG_ICHOR_GENERAL2_START + 0x42A) // Ichor: Knossa: hide the palace's Titanborn after the Turning
#define FLAG_ICHOR_HIDE_AMNISOS_VETERAN         (FLAG_ICHOR_GENERAL2_START + 0x42B) // Ichor: Knossa: hide the Titanborn veteran on Amnisos's mole after the Turning
#define FLAG_ICHOR_HIDE_BULL_ROAD_GRUNTS        (FLAG_ICHOR_GENERAL2_START + 0x42C) // Ichor: Knossa: hide the two Titanborn at the Bull Road's south end
#define FLAG_ICHOR_HIDE_ARIADNE_THRONE          (FLAG_ICHOR_GENERAL2_START + 0x42D) // Ichor: Knossa: hide Ariadne in the Throne Room
#define FLAG_ICHOR_HIDE_ARIADNE_STAIR           (FLAG_ICHOR_GENERAL2_START + 0x42E) // Ichor: Knossa: hide Ariadne at the Grand Staircase
#define FLAG_ICHOR_HIDE_ARIADNE_COURT           (FLAG_ICHOR_GENERAL2_START + 0x42F) // Ichor: Knossa: hide Ariadne in the Central Court
#define FLAG_ICHOR_HIDE_ASTERION_COURT          (FLAG_ICHOR_GENERAL2_START + 0x430) // Ichor: Knossa: hide Asterion in the Central Court
#define FLAG_ICHOR_HIDE_NAUSIKLES_AMNISOS       (FLAG_ICHOR_GENERAL2_START + 0x431) // Ichor: Knossa: hide Nausikles on Amnisos's quay
#define FLAG_ICHOR_ITEM_AMNISOS_MAX_REPEL       (FLAG_ICHOR_GENERAL2_START + 0x432) // Ichor: Knossa item ball: Amnisos, Max Repel up the cave path
#define FLAG_ICHOR_ITEM_AMNISOS_HYPER_POTION    (FLAG_ICHOR_GENERAL2_START + 0x433) // Ichor: Knossa item ball: Amnisos, Hyper Potion on the hive roof
#define FLAG_ICHOR_ITEM_BULL_ROAD_FULL_HEAL     (FLAG_ICHOR_GENERAL2_START + 0x434) // Ichor: Knossa item ball: the Bull Road, Full Heal
#define FLAG_ICHOR_ITEM_BULL_ROAD_ULTRA_BALL    (FLAG_ICHOR_GENERAL2_START + 0x435) // Ichor: Knossa item ball: the Bull Road, Ultra Ball
#define FLAG_ICHOR_ITEM_BULL_ROAD_MAX_POTION    (FLAG_ICHOR_GENERAL2_START + 0x436) // Ichor: Knossa item ball: the Bull Road, Max Potion
#define FLAG_ICHOR_ITEM_BULL_ROAD_HP_UP         (FLAG_ICHOR_GENERAL2_START + 0x437) // Ichor: Knossa item ball: the Bull Road, HP Up
#define FLAG_ICHOR_ITEM_BULL_ROAD_REVIVE        (FLAG_ICHOR_GENERAL2_START + 0x438) // Ichor: Knossa item ball: the Bull Road, Revive
#define FLAG_ICHOR_ITEM_VINEYARD_PP_UP          (FLAG_ICHOR_GENERAL2_START + 0x439) // Ichor: Knossa item ball: the vineyard's sealed jar, PP Up
#define FLAG_ICHOR_ITEM_VINEYARD_ULTRA_BALL     (FLAG_ICHOR_GENERAL2_START + 0x43A) // Ichor: Knossa item ball: the vineyard, Ultra Ball
#define FLAG_ICHOR_ITEM_BRONZE_HEEL_BIG_PEARL   (FLAG_ICHOR_GENERAL2_START + 0x43B) // Ichor: Knossa item ball: the Bronze Heel, Big Pearl on the giant's ankle
#define FLAG_ICHOR_ITEM_BRONZE_HEEL_RARE_CANDY  (FLAG_ICHOR_GENERAL2_START + 0x43C) // Ichor: Knossa item ball: the Bronze Heel, Rare Candy
#define FLAG_ICHOR_ITEM_PALACE_HYPER_POTION     (FLAG_ICHOR_GENERAL2_START + 0x43D) // Ichor: Knossa item ball: the West Magazines' open pithos, Hyper Potion
#define FLAG_ICHOR_ITEM_PALACE_ELIXIR           (FLAG_ICHOR_GENERAL2_START + 0x43E) // Ichor: Knossa item ball: the palace, Elixir in the Theatral Area
#define FLAG_ICHOR_ARIADNE_WOKE_YOU             (FLAG_ICHOR_GENERAL2_START + 0x43F) // Ichor: Knossa: III-3P, Ariadne at the Megaron's door before dawn (He wants you)
#define FLAG_ICHOR_ALETHEA_DAWN_DONE            (FLAG_ICHOR_GENERAL2_START + 0x440) // Ichor: Knossa: III-3P, Alethea sent the gull at dawn and went down to the quay
#define FLAG_ICHOR_R2_LONG_HALL                 (FLAG_ICHOR_GENERAL2_START + 0x458) // Ichor: Labyrinth Ring II: scene C played, Asterion broke the Long Hall's cracked wall
#define FLAG_ICHOR_ITEM_R2_TM                   (FLAG_ICHOR_GENERAL2_START + 0x459) // Ichor: Labyrinth Ring II: the sun room's TM
#define FLAG_ICHOR_ITEM_R2_MOON_STONE           (FLAG_ICHOR_GENERAL2_START + 0x45A) // Ichor: Labyrinth Ring II: the Moon Room's Moon Stone
#define FLAG_ICHOR_ITEM_R2_FULL_HEAL            (FLAG_ICHOR_GENERAL2_START + 0x45B) // Ichor: Labyrinth Ring II: the Full Heal behind the broken wall
#define FLAG_ICHOR_ITEM_R2_SILVER_OWL           (FLAG_ICHOR_GENERAL2_START + 0x45C) // Ichor: Labyrinth Ring II: Sinopos's gallery Silver Owl
#define FLAG_ICHOR_ITEM_R2_MAX_REPEL            (FLAG_ICHOR_GENERAL2_START + 0x45D) // Ichor: Labyrinth Ring II: a Max Repel in a dead end
#define FLAG_ICHOR_ITEM_R2_ULTRA_BALL           (FLAG_ICHOR_GENERAL2_START + 0x45E) // Ichor: Labyrinth Ring II: an Ultra Ball in the grotto
#define FLAG_ICHOR_HIDDEN_ITEM_R2_STARDUST      (FLAG_ICHOR_GENERAL2_START + 0x45F) // Ichor: Labyrinth Ring II: Stardust in the Moon Room
#define FLAG_ICHOR_HIDDEN_ITEM_R2_OBOL          (FLAG_ICHOR_GENERAL2_START + 0x460) // Ichor: Labyrinth Ring II: a Bronze Obol in a dead end
#define FLAG_ICHOR_HIDE_R3_WEB_1A               (FLAG_ICHOR_GENERAL2_START + 0x461) // Ichor: Labyrinth Ring III: web 1, west strand burned
#define FLAG_ICHOR_HIDE_R3_WEB_1B               (FLAG_ICHOR_GENERAL2_START + 0x462) // Ichor: Labyrinth Ring III: web 1, east strand burned
#define FLAG_ICHOR_HIDE_R3_WEB_2A               (FLAG_ICHOR_GENERAL2_START + 0x463) // Ichor: Labyrinth Ring III: web 2, a strand burned
#define FLAG_ICHOR_HIDE_R3_WEB_2B               (FLAG_ICHOR_GENERAL2_START + 0x464) // Ichor: Labyrinth Ring III: web 2, a strand burned
#define FLAG_ICHOR_HIDE_R3_WEB_3A               (FLAG_ICHOR_GENERAL2_START + 0x465) // Ichor: Labyrinth Ring III: web 3, a strand burned
#define FLAG_ICHOR_HIDE_R3_WEB_3B               (FLAG_ICHOR_GENERAL2_START + 0x466) // Ichor: Labyrinth Ring III: web 3, a strand burned
#define FLAG_ICHOR_HIDE_R3_WEB_4A               (FLAG_ICHOR_GENERAL2_START + 0x467) // Ichor: Labyrinth Ring III: the web pocket's web, a strand burned
#define FLAG_ICHOR_HIDE_R3_WEB_4B               (FLAG_ICHOR_GENERAL2_START + 0x468) // Ichor: Labyrinth Ring III: the web pocket's web, a strand burned
#define FLAG_ICHOR_ITEM_R3_MAX_ETHER            (FLAG_ICHOR_GENERAL2_START + 0x469) // Ichor: Labyrinth Ring III: the Max Ether behind the first web
#define FLAG_ICHOR_ITEM_R3_RARE_BONE            (FLAG_ICHOR_GENERAL2_START + 0x46A) // Ichor: Labyrinth Ring III: the Rare Bone in the web pocket
#define FLAG_ICHOR_ITEM_R3_TM                   (FLAG_ICHOR_GENERAL2_START + 0x46B) // Ichor: Labyrinth Ring III: Automaton No. 7's TM
#define FLAG_ICHOR_ITEM_R3_STAR_PIECE           (FLAG_ICHOR_GENERAL2_START + 0x46C) // Ichor: Labyrinth Ring III: the Star Piece by the glow trail's spur
#define FLAG_ICHOR_ITEM_R3_PEARL                (FLAG_ICHOR_GENERAL2_START + 0x46D) // Ichor: Labyrinth Ring III: a Big Pearl on the stream's islet
#define FLAG_ICHOR_HIDDEN_ITEM_R3_REVIVE        (FLAG_ICHOR_GENERAL2_START + 0x46E) // Ichor: Labyrinth Ring III: a Revive in a dead end
#define FLAG_ICHOR_MET_DAEDALUS                 (FLAG_ICHOR_GENERAL2_START + 0x46F) // Ichor: Labyrinth: scene D, Daedalus met in his workshop
#define FLAG_ICHOR_DAEDALUS_LIFT                (FLAG_ICHOR_GENERAL2_START + 0x470) // Ichor: Labyrinth: Daedalus's lift runs between the workshop and the Grand Staircase
#define FLAG_ICHOR_GOT_MASTER_BALL              (FLAG_ICHOR_GENERAL2_START + 0x471) // Ichor: Labyrinth: Daedalus gave the Master Ball (scene D)
#define FLAG_ICHOR_TITAN_DISGUISE               (FLAG_ICHOR_GENERAL2_START + 0x472) // Ichor: Labyrinth Ring IV: took a Titan helmet from the barracks locker (the disguise)
#define FLAG_ICHOR_ENKELADOS_PASSED             (FLAG_ICHOR_GENERAL2_START + 0x473) // Ichor: Labyrinth Ring IV: past Enkelados's checkpoint, by catechism or by battle
#define FLAG_ICHOR_ITEM_R4_MAX_REVIVE           (FLAG_ICHOR_GENERAL2_START + 0x474) // Ichor: Labyrinth Ring IV: the barracks' Max Revive
#define FLAG_ICHOR_ITEM_R4_HYPER_POTION         (FLAG_ICHOR_GENERAL2_START + 0x475) // Ichor: Labyrinth Ring IV: the armory's Hyper Potion
#define FLAG_ICHOR_ITEM_R4_IRON                 (FLAG_ICHOR_GENERAL2_START + 0x476) // Ichor: Labyrinth Ring IV: an Iron in the dig
#define FLAG_ICHOR_GOT_HELM_SCENE               (FLAG_ICHOR_GENERAL2_START + 0x477) // Ichor: Minos's tomb: scene F, the Helm taken from the bier
#define FLAG_ICHOR_ITEM_TOMB_GOLD_STATER        (FLAG_ICHOR_GENERAL2_START + 0x478) // Ichor: Minos's tomb: the Gold Stater among the grave goods
#define FLAG_ICHOR_HIDDEN_ITEM_R4_ULTRA_BALL    (FLAG_ICHOR_GENERAL2_START + 0x479) // Ichor: Labyrinth Ring IV: an Ultra Ball under a bunk
#define FLAG_ICHOR_HIDDEN_ITEM_R4_NUGGET        (FLAG_ICHOR_GENERAL2_START + 0x47A) // Ichor: Labyrinth Ring IV: a Nugget in the dig's spoil
#define FLAG_ICHOR_HIDE_R1_SEAL                 (FLAG_ICHOR_GENERAL2_START + 0x47B) // Ichor: Labyrinth Ring I: the labrys seal on the treasury door, cut (return gate)
#define FLAG_ICHOR_HIDE_R2_SEAL                 (FLAG_ICHOR_GENERAL2_START + 0x47C) // Ichor: Labyrinth Ring II: the labrys seal on the runners' shrine, cut (return gate)
#define FLAG_ICHOR_HIDE_R3_THORNWEB             (FLAG_ICHOR_GENERAL2_START + 0x47D) // Ichor: Labyrinth Ring III: the thornweb over the spiders' nest, burned (post-game gate)
#define FLAG_ICHOR_HIDE_R4_BOULDER              (FLAG_ICHOR_GENERAL2_START + 0x47E) // Ichor: Labyrinth Ring IV: the great boulder in the dig, broken (post-game gate)
#define FLAG_ICHOR_R1_STATIC                    (FLAG_ICHOR_GENERAL2_START + 0x47F) // Ichor: Labyrinth Ring I: the treasury's guardian battled
#define FLAG_ICHOR_R2_STATIC                    (FLAG_ICHOR_GENERAL2_START + 0x480) // Ichor: Labyrinth Ring II: the runners' shrine's Taurivet battled
#define FLAG_ICHOR_R3_STATIC                    (FLAG_ICHOR_GENERAL2_START + 0x481) // Ichor: Labyrinth Ring III: the nest's Hyphantis battled
#define FLAG_ICHOR_R4_STATIC                    (FLAG_ICHOR_GENERAL2_START + 0x482) // Ichor: Labyrinth Ring IV: the deep dig's Geogrip battled
#define FLAG_ICHOR_ITEM_R1_TREASURY             (FLAG_ICHOR_GENERAL2_START + 0x483) // Ichor: Labyrinth Ring I: the treasury's reward
#define FLAG_ICHOR_ITEM_R3_NEST                 (FLAG_ICHOR_GENERAL2_START + 0x484) // Ichor: Labyrinth Ring III: the nest's reward
#define FLAG_ICHOR_ITEM_R4_DEEP                 (FLAG_ICHOR_GENERAL2_START + 0x485) // Ichor: Labyrinth Ring IV: the deep dig's reward
#define FLAG_ICHOR_ITEM_R2_SHRINE               (FLAG_ICHOR_GENERAL2_START + 0x486) // Ichor: Labyrinth Ring II: the runners' shrine's reward (behind the labrys seal)
#define FLAG_ICHOR_HIDDEN_ITEM_R3_ETHER         (FLAG_ICHOR_GENERAL2_START + 0x487) // Ichor: Labyrinth Ring III: an Ether by the stream
#define FLAG_ICHOR_HIDDEN_ITEM_TOMB_PEARL       (FLAG_ICHOR_GENERAL2_START + 0x488) // Ichor: Minos's tomb: a Pearl in the dust by the bier
#define FLAG_ICHOR_HIDDEN_ITEM_TOMB_OBOL        (FLAG_ICHOR_GENERAL2_START + 0x489) // Ichor: Minos's tomb: the ferryman's Obol in a jar
#define FLAG_ICHOR_ITEM_CELLAR_1                (FLAG_ICHOR_GENERAL2_START + 0x48A) // Ichor: Labyrinth cellars: room 1's treasure
#define FLAG_ICHOR_ITEM_CELLAR_2                (FLAG_ICHOR_GENERAL2_START + 0x48B) // Ichor: Labyrinth cellars: room 2's treasure
#define FLAG_ICHOR_ITEM_CELLAR_3                (FLAG_ICHOR_GENERAL2_START + 0x48C) // Ichor: Labyrinth cellars: room 3's treasure
#define FLAG_ICHOR_ITEM_CELLAR_4                (FLAG_ICHOR_GENERAL2_START + 0x48D) // Ichor: Labyrinth cellars: room 4's treasure
#define FLAG_ICHOR_ITEM_CELLAR_5                (FLAG_ICHOR_GENERAL2_START + 0x48E) // Ichor: Labyrinth cellars: room 5's treasure
#define FLAG_ICHOR_ITEM_CELLAR_6                (FLAG_ICHOR_GENERAL2_START + 0x48F) // Ichor: Labyrinth cellars: room 6's treasure
#define FLAG_ICHOR_ITEM_CELLAR_7                (FLAG_ICHOR_GENERAL2_START + 0x490) // Ichor: Labyrinth cellars: room 7's treasure
#define FLAG_ICHOR_ITEM_CELLAR_8                (FLAG_ICHOR_GENERAL2_START + 0x491) // Ichor: Labyrinth cellars: room 8's treasure
#define FLAG_ICHOR_ITEM_CELLAR_9                (FLAG_ICHOR_GENERAL2_START + 0x492) // Ichor: Labyrinth cellars: room 9's treasure, two drops down
#define FLAG_ICHOR_RING5_WALL_TOMB              (FLAG_ICHOR_GENERAL2_START + 0x4A0) // Ichor: Ring V: %1, the tomb wall, broken by Asterion
#define FLAG_ICHOR_RING5_WALL_SOUTH             (FLAG_ICHOR_GENERAL2_START + 0x4A1) // Ichor: Ring V: %2, the south shortcut wall, broken
#define FLAG_ICHOR_RING5_WALL_TREASURE          (FLAG_ICHOR_GENERAL2_START + 0x4A2) // Ichor: Ring V: %3, the treasure wall, broken
#define FLAG_ICHOR_KLEON_HUMBLED                (FLAG_ICHOR_GENERAL2_START + 0x4A3) // Ichor: Ring V: Scene E, Kleon bowled over at pool 1
#define FLAG_ICHOR_HIDE_KLEON_RING5             (FLAG_ICHOR_GENERAL2_START + 0x4A4) // Ichor: Ring V: Kleon gone after Scene E (set at new game until the scene)
#define FLAG_ICHOR_RING5_DOOR_BACK              (FLAG_ICHOR_GENERAL2_START + 0x4A5) // Ichor: Ring V: the bronze grate back to the gallery, opened from the south
#define FLAG_ICHOR_RING5_BELL_RUNG              (FLAG_ICHOR_GENERAL2_START + 0x4A6) // Ichor: Ring V: the bell rung once (its first-time line)
#define FLAG_ICHOR_RING5_ITEM_1                 (FLAG_ICHOR_GENERAL2_START + 0x4A7) // Ichor: Ring V: item
#define FLAG_ICHOR_RING5_ITEM_2                 (FLAG_ICHOR_GENERAL2_START + 0x4A8) // Ichor: Ring V: item
#define FLAG_ICHOR_RING5_ITEM_3                 (FLAG_ICHOR_GENERAL2_START + 0x4A9) // Ichor: Ring V: item
#define FLAG_ICHOR_RING5_ITEM_4                 (FLAG_ICHOR_GENERAL2_START + 0x4AA) // Ichor: Ring V: item
#define FLAG_ICHOR_RING5_ITEM_5                 (FLAG_ICHOR_GENERAL2_START + 0x4AB) // Ichor: Ring V: item
#define FLAG_ICHOR_RING5_ITEM_6                 (FLAG_ICHOR_GENERAL2_START + 0x4AC) // Ichor: Ring V: item
#define FLAG_ICHOR_TOMB_ITEM                    (FLAG_ICHOR_GENERAL2_START + 0x4AD) // Ichor: Minos's tomb: the gold stater (Big Nugget)
#define FLAG_ICHOR_HIDE_HELM_BIER               (FLAG_ICHOR_GENERAL2_START + 0x4AE) // Ichor: Minos's tomb: the Helm taken from the bier
#define FLAG_ICHOR_HIDDEN_ITEM_RING5_ISLAND     (FLAG_ICHOR_GENERAL2_START + 0x4AF) // Ichor: Ring V: the lake island
#define FLAG_ICHOR_HIDDEN_ITEM_RING5_A          (FLAG_ICHOR_GENERAL2_START + 0x4B0) // Ichor: Ring V: hidden
#define FLAG_ICHOR_HIDDEN_ITEM_RING5_B          (FLAG_ICHOR_GENERAL2_START + 0x4B1) // Ichor: Ring V: hidden
#define FLAG_ICHOR_HIDDEN_ITEM_RING5_C          (FLAG_ICHOR_GENERAL2_START + 0x4B2) // Ichor: Ring V: hidden
#define FLAG_ICHOR_ASTERION_FREED               (FLAG_ICHOR_GENERAL2_START + 0x4B3) // Ichor: Starry Chamber: Scene J, the collar cut; Asterion is free (hides every chained or patrolling Asterion)
#define FLAG_ICHOR_PHAEDON_UNMASKED             (FLAG_ICHOR_GENERAL2_START + 0x4B4) // Ichor: Starry Chamber: Scene J, Kronos took off the gold mask
#define FLAG_ICHOR_RHEA_MERCY                   (FLAG_ICHOR_GENERAL2_START + 0x4B5) // Ichor: Starry Chamber: Scene J, Rhea left the threshold open; the Turning begins
#define FLAG_ICHOR_SHOWED_PHAEDON_TABLET        (FLAG_ICHOR_GENERAL2_START + 0x4B6) // Ichor: Starry Chamber: showed Phaedon the sealed tablet
#define FLAG_ICHOR_TURNING_DONE                 (FLAG_ICHOR_GENERAL2_START + 0x4B7) // Ichor: The Turning: out through the threshold
#define FLAG_ICHOR_ICARUS_FLIGHT                (FLAG_ICHOR_GENERAL2_START + 0x4B8) // Ichor: Scene L: flew up the Icarus Shaft
#define FLAG_ICHOR_HIDE_STARRY_CAST             (FLAG_ICHOR_GENERAL2_START + 0x4B9) // Ichor: Starry Chamber: Kronos, Rhea, Kleon and the chained Asterion gone after Scene J
#define FLAG_ICHOR_ARCHIVE_TABLET               (FLAG_ICHOR_GENERAL2_START + 0x4BA) // Ichor: Ring VI archive: took Kleon's draft (Scene H)
#define FLAG_ICHOR_GOT_ELPIS_TABLET             (FLAG_ICHOR_GENERAL2_START + 0x4BB) // Ichor: Ring VI archive: took Elpis's sealed tablet (Scene H)
#define FLAG_ICHOR_HIDE_HYPERION_KNOSSA         (FLAG_ICHOR_GENERAL2_START + 0x4BC) // Ichor: Ring VI: Hyperion gone after Scene G
#define FLAG_ICHOR_MISTRESS_HONEY               (FLAG_ICHOR_GENERAL2_START + 0x4BD) // Ichor: Ring VI shrine: offered Honey to the Mistress
#define FLAG_ICHOR_ARIADNE_JOINED               (FLAG_ICHOR_GENERAL2_START + 0x4BE) // Ichor: Ring VII: Scene I, Ariadne joined; the Gigas beaten
#define FLAG_ICHOR_DANCE_DONE                   (FLAG_ICHOR_GENERAL2_START + 0x4BF) // Ichor: Ring VII: the crane dance danced; the stair to the heart opens
#define FLAG_ICHOR_RING7_BEAM_DONE              (FLAG_ICHOR_GENERAL2_START + 0x4C0) // Ichor: Ring VII: the mirrors carry the beam to the crystal; the floor is lit
#define FLAG_ICHOR_HIDE_ARIADNE_RING7           (FLAG_ICHOR_GENERAL2_START + 0x4C1) // Ichor: Ring VII: Ariadne out of sight (before Scene I, and after the dance)
#define FLAG_ICHOR_HIDE_GIGAS_RING7             (FLAG_ICHOR_GENERAL2_START + 0x4C2) // Ichor: Ring VII: the Gigas gone after the double battle
#define FLAG_ICHOR_RING6_DIALS_SET              (FLAG_ICHOR_GENERAL2_START + 0x4C3) // Ichor: Ring VI: the dials stood at the clerks' setting (ABA) on first entry
#define FLAG_ICHOR_RING6_TEACH_OPEN             (FLAG_ICHOR_GENERAL2_START + 0x4C4) // Ichor: Ring VI: the teaching dial turned; the Hall of Dials is open
#define FLAG_ICHOR_HIDE_SENTRY_1                (FLAG_ICHOR_GENERAL2_START + 0x4C5) // Ichor: Ring VI: Bronzong sentry 1 rang its alarm and wound down
#define FLAG_ICHOR_HIDE_SENTRY_2                (FLAG_ICHOR_GENERAL2_START + 0x4C6) // Ichor: Ring VI: Bronzong sentry 2 rang its alarm and wound down
#define FLAG_ICHOR_HIDE_SENTRY_3                (FLAG_ICHOR_GENERAL2_START + 0x4C7) // Ichor: Ring VI: Bronzong sentry 3 rang its alarm and wound down
#define FLAG_ICHOR_RING6_LANDING_OPEN           (FLAG_ICHOR_GENERAL2_START + 0x4C8) // Ichor: Ring VI: the sealed landing door opened (Hyperion beaten)
#define FLAG_ICHOR_RING6_ARCHIVE_BACK           (FLAG_ICHOR_GENERAL2_START + 0x4C9) // Ichor: Ring VI: the archive's back grate opened from inside
#define FLAG_ICHOR_RING6_ITEM_1                 (FLAG_ICHOR_GENERAL2_START + 0x4CA) // Ichor: Ring VI: item
#define FLAG_ICHOR_RING6_ITEM_2                 (FLAG_ICHOR_GENERAL2_START + 0x4CB) // Ichor: Ring VI: item
#define FLAG_ICHOR_RING6_ITEM_3                 (FLAG_ICHOR_GENERAL2_START + 0x4CC) // Ichor: Ring VI: item
#define FLAG_ICHOR_RING6_ITEM_4                 (FLAG_ICHOR_GENERAL2_START + 0x4CD) // Ichor: Ring VI: item
#define FLAG_ICHOR_RING6_VAULT_1                (FLAG_ICHOR_GENERAL2_START + 0x4CE) // Ichor: Ring VI vault: chest
#define FLAG_ICHOR_RING6_VAULT_2                (FLAG_ICHOR_GENERAL2_START + 0x4CF) // Ichor: Ring VI vault: chest
#define FLAG_ICHOR_RING6_VAULT_3                (FLAG_ICHOR_GENERAL2_START + 0x4D0) // Ichor: Ring VI vault: chest
#define FLAG_ICHOR_RING6_VAULT_4                (FLAG_ICHOR_GENERAL2_START + 0x4D1) // Ichor: Ring VI vault: chest
#define FLAG_ICHOR_GOT_TM_FLARE                 (FLAG_ICHOR_GENERAL2_START + 0x4D2) // Ichor: Ring VI: Hyperion's TM after Scene G
#define FLAG_ICHOR_HIDDEN_ITEM_RING6_A          (FLAG_ICHOR_GENERAL2_START + 0x4D3) // Ichor: Ring VI: hidden
#define FLAG_ICHOR_HIDDEN_ITEM_RING6_B          (FLAG_ICHOR_GENERAL2_START + 0x4D4) // Ichor: Ring VI: hidden
#define FLAG_ICHOR_HIDDEN_ITEM_RING6_C          (FLAG_ICHOR_GENERAL2_START + 0x4D5) // Ichor: Ring VI: hidden
#define FLAG_ICHOR_HIDDEN_ITEM_RING6_FALLS      (FLAG_ICHOR_GENERAL2_START + 0x4D6) // Ichor: Ring VI: above the falls
#define FLAG_ICHOR_RING7_ITEM_1                 (FLAG_ICHOR_GENERAL2_START + 0x4D7) // Ichor: Ring VII: item
#define FLAG_ICHOR_RING7_ITEM_2                 (FLAG_ICHOR_GENERAL2_START + 0x4D8) // Ichor: Ring VII: item
#define FLAG_ICHOR_RING7_DISC                   (FLAG_ICHOR_GENERAL2_START + 0x4D9) // Ichor: Ring VII: the teaching mirror lit the disc
#define FLAG_ICHOR_HIDDEN_ITEM_RING7_A          (FLAG_ICHOR_GENERAL2_START + 0x4DA) // Ichor: Ring VII: hidden
#define FLAG_ICHOR_HIDDEN_ITEM_RING7_B          (FLAG_ICHOR_GENERAL2_START + 0x4DB) // Ichor: Ring VII: hidden
#define FLAG_ICHOR_THEOXENIA_HESTIA             (FLAG_ICHOR_GENERAL2_START + 0x52B) // Ichor: Lakonia: Hestia's visit at the roofless farmhouse (E2) done
#define FLAG_ICHOR_HIDE_LAKONIA_GEOGRIP         (FLAG_ICHOR_GENERAL2_START + 0x52C) // Ichor: Lakonia: the wrestling sands' Geogrip caught or beaten
#define FLAG_ICHOR_ITEM_ROUTE25_CLEFT           (FLAG_ICHOR_GENERAL2_START + 0x52D) // Ichor: Lakonia: the item in Taygetos's cleft on Route 25 (behind the Hammer's rubble)
#define FLAG_ICHOR_HIDE_ROUTE25_RUBBLE          (FLAG_ICHOR_GENERAL2_START + 0x52E) // Ichor: Lakonia: Route 25's cleft rubble broken
#define FLAG_ICHOR_HIDE_LAKONIA_RUBBLE          (FLAG_ICHOR_GENERAL2_START + 0x52F) // Ichor: Lakonia: the rubble in the Taygetos cleft behind the agoge broken
#define FLAG_ICHOR_ITEM_LAKONIA_CLEFT           (FLAG_ICHOR_GENERAL2_START + 0x530) // Ichor: Lakonia: the item in the cleft behind the agoge
#define FLAG_ICHOR_ITEM_GYTHEION_ISLET          (FLAG_ICHOR_GENERAL2_START + 0x531) // Ichor: Lakonia: the Proteus islet's item off Gytheion (Conch)
#define FLAG_ICHOR_HIDDEN_ITEM_ROUTE25_ISLET    (FLAG_ICHOR_GENERAL2_START + 0x532) // Ichor: Lakonia: Route 25's reed islet (Conch)
#define FLAG_ICHOR_HIDDEN_ITEM_GYTHEION_ISLET   (FLAG_ICHOR_GENERAL2_START + 0x533) // Ichor: Lakonia: the Proteus islet off Gytheion (Conch)
#define FLAG_ICHOR_SACRED_OLIVES_COLUMN         (FLAG_ICHOR_GENERAL2_START + 0x540) // Ichor: Delphoi: III-6A, the Titans' column has passed on the Sacred Olives
#define FLAG_ICHOR_HIDE_TITAN_COLUMN_OLIVES     (FLAG_ICHOR_GENERAL2_START + 0x541) // Ichor: Delphoi: hide the Titans' column on the Sacred Olives
#define FLAG_ICHOR_HIDE_HIERON_ROAD             (FLAG_ICHOR_GENERAL2_START + 0x542) // Ichor: Delphoi: hide Hieron at the roadside (he's in his hut)
#define FLAG_ICHOR_GOT_HIERON_OIL               (FLAG_ICHOR_GENERAL2_START + 0x543) // Ichor: Delphoi: Hieron gave 3 Olive Oil
#define FLAG_ICHOR_GOT_HIERON_BIG_ROOT          (FLAG_ICHOR_GENERAL2_START + 0x544) // Ichor: Delphoi: Hieron gave a Big Root after the climax
#define FLAG_ICHOR_GORGE_SENTRIES               (FLAG_ICHOR_GENERAL2_START + 0x545) // Ichor: Delphoi: III-6B, the gorge's sentries let you through
#define FLAG_ICHOR_GORGE_BOULDER                (FLAG_ICHOR_GENERAL2_START + 0x546) // Ichor: Delphoi: the gorge's cracked boulder (hide flag of the rock object)
#define FLAG_ICHOR_HIDE_OCHTHOS_GORGE           (FLAG_ICHOR_GENERAL2_START + 0x547) // Ichor: Delphoi: Ochthos has left the gorge (after the climax)
#define FLAG_ICHOR_VISITED_DELPHOI              (FLAG_ICHOR_GENERAL2_START + 0x548) // Ichor: Delphoi: visited (the fly flag)
#define FLAG_ICHOR_DELPHOI_ARRIVED              (FLAG_ICHOR_GENERAL2_START + 0x549) // Ichor: Delphoi: III-6C played (the Pythia passed, Alethea met)
#define FLAG_ICHOR_HIDE_PYTHIA_PROCESSION       (FLAG_ICHOR_GENERAL2_START + 0x54A) // Ichor: Delphoi: hide the Pythia's procession
#define FLAG_ICHOR_HIDE_ALETHEA_DELPHOI_STEPS   (FLAG_ICHOR_GENERAL2_START + 0x54B) // Ichor: Delphoi: hide Alethea on the Sacred Way
#define FLAG_ICHOR_DELPHOI_STADIUM_SCENE        (FLAG_ICHOR_GENERAL2_START + 0x54C) // Ichor: Delphoi: Kleon and Rhea at the stadium, seen
#define FLAG_ICHOR_HIDE_KLEON_DELPHOI_STADIUM   (FLAG_ICHOR_GENERAL2_START + 0x54D) // Ichor: Delphoi: hide Kleon at the stadium
#define FLAG_ICHOR_HIDE_RHEA_DELPHOI_STADIUM    (FLAG_ICHOR_GENERAL2_START + 0x54E) // Ichor: Delphoi: hide Rhea at the stadium
#define FLAG_ICHOR_APOLLO_DISC_0                (FLAG_ICHOR_GENERAL2_START + 0x54F) // Ichor: Temple of Apollo: the pronaos's disc lit
#define FLAG_ICHOR_APOLLO_DISC_1                (FLAG_ICHOR_GENERAL2_START + 0x550) // Ichor: Temple of Apollo: chamber 1's disc lit
#define FLAG_ICHOR_APOLLO_DISC_2                (FLAG_ICHOR_GENERAL2_START + 0x551) // Ichor: Temple of Apollo: chamber 2's disc lit
#define FLAG_ICHOR_APOLLO_DISC_3                (FLAG_ICHOR_GENERAL2_START + 0x552) // Ichor: Temple of Apollo: chamber 3's disc lit
#define FLAG_ICHOR_APOLLO_DISC_4                (FLAG_ICHOR_GENERAL2_START + 0x553) // Ichor: Temple of Apollo: chamber 4's disc lit
#define FLAG_ICHOR_APOLLO_BRAZIER               (FLAG_ICHOR_GENERAL2_START + 0x554) // Ichor: Temple of Apollo: the adyton's brazier lit from the beam
#define FLAG_ICHOR_PYTHIAN_LIGHT_DONE           (FLAG_ICHOR_GENERAL2_START + 0x555) // Ichor: Temple of Apollo: the tripod lit
#define FLAG_ICHOR_HIDE_PHEMONOE_TRIPOD         (FLAG_ICHOR_GENERAL2_START + 0x556) // Ichor: Temple of Apollo: hide the Pythia on the tripod until it's lit
#define FLAG_ICHOR_GOT_TM_MYSTICAL_FIRE         (FLAG_ICHOR_GENERAL2_START + 0x557) // Ichor: Temple of Apollo: the Pythia gave TM Mystical Fire
#define FLAG_ICHOR_PYTHIA_SPOKE                 (FLAG_ICHOR_GENERAL2_START + 0x558) // Ichor: Delphoi: the Pythia said Melitta (after the Sun Laurel)
#define FLAG_ICHOR_MOM_SPRING                   (FLAG_ICHOR_GENERAL2_START + 0x559) // Ichor: Delphoi: III-7, Mom at the Kastalian spring
#define FLAG_ICHOR_HIDE_MOM_DELPHOI_SPRING      (FLAG_ICHOR_GENERAL2_START + 0x55A) // Ichor: Delphoi: hide Mom at the spring
#define FLAG_ICHOR_OMPHALOS_NIGHT               (FLAG_ICHOR_GENERAL2_START + 0x55B) // Ichor: Delphoi: III-8 done, you went down the Omphalos stair
#define FLAG_ICHOR_OMPHALOS_OPEN                (FLAG_ICHOR_GENERAL2_START + 0x55C) // Ichor: Delphoi: the Omphalos is split open (III-8 on)
#define FLAG_ICHOR_HIDE_KLEON_DELPHOI_GATE      (FLAG_ICHOR_GENERAL2_START + 0x55D) // Ichor: Delphoi: hide Kleon at the Omphalos court's gate
#define FLAG_ICHOR_HIDE_RHEA_DELPHOI_GATE       (FLAG_ICHOR_GENERAL2_START + 0x55E) // Ichor: Delphoi: hide Rhea at the Omphalos court's gate
#define FLAG_ICHOR_HIDE_OMPHALOS_GIGAS          (FLAG_ICHOR_GENERAL2_START + 0x55F) // Ichor: Delphoi: hide Ephialtes and Thoas
#define FLAG_ICHOR_HIDE_OMPHALOS_HYPERION       (FLAG_ICHOR_GENERAL2_START + 0x560) // Ichor: Delphoi: hide Hyperion at the Omphalos
#define FLAG_ICHOR_HIDE_OMPHALOS_PHAEDON        (FLAG_ICHOR_GENERAL2_START + 0x561) // Ichor: Delphoi: hide Phaedon at the Omphalos
#define FLAG_ICHOR_HIDE_OMPHALOS_ARCHON         (FLAG_ICHOR_GENERAL2_START + 0x562) // Ichor: Delphoi: hide the Archon at the lower gate
#define FLAG_ICHOR_HIDE_MOM_STAIRHEAD           (FLAG_ICHOR_GENERAL2_START + 0x563) // Ichor: Delphoi: hide Mom and Alethea at the stairhead
#define FLAG_ICHOR_HIDE_OMPHALOS_MUSTER         (FLAG_ICHOR_GENERAL2_START + 0x564) // Ichor: Delphoi: hide the Titanborn on the Sacred Way
#define FLAG_ICHOR_GOT_THEOKLES_STYLUS          (FLAG_ICHOR_GENERAL2_START + 0x565) // Ichor: Delphoi: Theokles gave the bent stylus (Twisted Spoon)
#define FLAG_ICHOR_KITHARODE_QUIZ               (FLAG_ICHOR_GENERAL2_START + 0x566) // Ichor: Delphoi: Chrysothemis's nome quiz won (TM Hyper Voice)
#define FLAG_ICHOR_SIPHNIAN_TITHE               (FLAG_ICHOR_GENERAL2_START + 0x567) // Ichor: Delphoi: paid the Siphnians' tithe (Choice Specs)
#define FLAG_ICHOR_GOT_POLEMON_SPELL_TAG        (FLAG_ICHOR_GENERAL2_START + 0x568) // Ichor: Delphoi: Polemon gave a Spell Tag
#define FLAG_ICHOR_TRADED_KERAZAP_DELPHOI       (FLAG_ICHOR_GENERAL2_START + 0x569) // Ichor: Delphoi: traded a Melibee for Prophet the Kerazap
#define FLAG_ICHOR_GOT_PHILAGROS_BELL           (FLAG_ICHOR_GENERAL2_START + 0x56A) // Ichor: Delphoi: Philagros gave a Soothe Bell (after the climax)
#define FLAG_ICHOR_GOT_MELISSAI_HONEY           (FLAG_ICHOR_GENERAL2_START + 0x56B) // Ichor: Delphoi: Hagne gave honey (after the climax)
#define FLAG_ICHOR_GOT_DELPHOI_OSTRAKON         (FLAG_ICHOR_GENERAL2_START + 0x56C) // Ichor: Delphoi: Aristion gave his ostrakon
#define FLAG_ICHOR_HIDE_ALETHEA_TREASURY        (FLAG_ICHOR_GENERAL2_START + 0x56D) // Ichor: Delphoi: hide Alethea in Astyra's treasury
#define FLAG_ICHOR_HIDE_MOM_MELISSAI            (FLAG_ICHOR_GENERAL2_START + 0x56E) // Ichor: Delphoi: hide Mom in the melissai's inner room
#define FLAG_ICHOR_ITEM_OLIVES_MAX_REPEL        (FLAG_ICHOR_GENERAL2_START + 0x56F) // Ichor: Delphoi: the item ball (olives_max_repel)
#define FLAG_ICHOR_ITEM_OLIVES_ULTRA_BALL       (FLAG_ICHOR_GENERAL2_START + 0x570) // Ichor: Delphoi: the item ball (olives_ultra_ball)
#define FLAG_ICHOR_ITEM_OLIVES_HYPER_POTION     (FLAG_ICHOR_GENERAL2_START + 0x571) // Ichor: Delphoi: the item ball (olives_hyper_potion)
#define FLAG_ICHOR_ITEM_OLIVES_FULL_HEAL        (FLAG_ICHOR_GENERAL2_START + 0x572) // Ichor: Delphoi: the item ball (olives_full_heal)
#define FLAG_ICHOR_ITEM_OLIVES_PP_UP            (FLAG_ICHOR_GENERAL2_START + 0x573) // Ichor: Delphoi: the item ball (olives_pp_up)
#define FLAG_ICHOR_ITEM_GORGE_MAX_ETHER         (FLAG_ICHOR_GENERAL2_START + 0x574) // Ichor: Delphoi: the item ball (gorge_max_ether)
#define FLAG_ICHOR_ITEM_GORGE_ETHER             (FLAG_ICHOR_GENERAL2_START + 0x575) // Ichor: Delphoi: the item ball (gorge_ether)
#define FLAG_ICHOR_ITEM_GORGE_REVIVE            (FLAG_ICHOR_GENERAL2_START + 0x576) // Ichor: Delphoi: the item ball (gorge_revive)
#define FLAG_ICHOR_ITEM_GORGE_FULL_HEAL         (FLAG_ICHOR_GENERAL2_START + 0x577) // Ichor: Delphoi: the item ball (gorge_full_heal)
#define FLAG_ICHOR_ITEM_GORGE_ULTRA_BALL        (FLAG_ICHOR_GENERAL2_START + 0x578) // Ichor: Delphoi: the item ball (gorge_ultra_ball)
#define FLAG_ICHOR_ITEM_DELPHOI_ULTRA_BALL      (FLAG_ICHOR_GENERAL2_START + 0x579) // Ichor: Delphoi: the item ball (delphoi_ultra_ball)
#define FLAG_ICHOR_ITEM_APOLLO_FULL_RESTORE     (FLAG_ICHOR_GENERAL2_START + 0x57A) // Ichor: Delphoi: the item ball (apollo_full_restore)
#define FLAG_ICHOR_HIDDEN_ITEM_OLIVES_LEAF_STONE (FLAG_ICHOR_GENERAL2_START + 0x57B) // Ichor: Delphoi: hidden item (olives_leaf_stone)
#define FLAG_ICHOR_HIDDEN_ITEM_OLIVES_REVIVE    (FLAG_ICHOR_GENERAL2_START + 0x57C) // Ichor: Delphoi: hidden item (olives_revive)
#define FLAG_ICHOR_HIDDEN_ITEM_OLIVES_BIG_MUSHROOM (FLAG_ICHOR_GENERAL2_START + 0x57D) // Ichor: Delphoi: hidden item (olives_big_mushroom)
#define FLAG_ICHOR_HIDDEN_ITEM_OLIVES_STAR_PIECE (FLAG_ICHOR_GENERAL2_START + 0x57E) // Ichor: Delphoi: hidden item (olives_star_piece)
#define FLAG_ICHOR_HIDDEN_ITEM_GORGE_FULL_RESTORE (FLAG_ICHOR_GENERAL2_START + 0x57F) // Ichor: Delphoi: hidden item (gorge_full_restore)
#define FLAG_ICHOR_HIDDEN_ITEM_GORGE_MYSTIC_WATER (FLAG_ICHOR_GENERAL2_START + 0x580) // Ichor: Delphoi: hidden item (gorge_mystic_water)
#define FLAG_ICHOR_HIDDEN_ITEM_GORGE_PEARL      (FLAG_ICHOR_GENERAL2_START + 0x581) // Ichor: Delphoi: hidden item (gorge_pearl)
#define FLAG_ICHOR_HIDDEN_ITEM_GORGE_NUGGET     (FLAG_ICHOR_GENERAL2_START + 0x582) // Ichor: Delphoi: hidden item (gorge_nugget)
#define FLAG_ICHOR_HIDDEN_ITEM_DELPHOI_PEARL    (FLAG_ICHOR_GENERAL2_START + 0x583) // Ichor: Delphoi: hidden item (delphoi_pearl)
#define FLAG_ICHOR_HIDDEN_ITEM_DELPHOI_STARDUST (FLAG_ICHOR_GENERAL2_START + 0x584) // Ichor: Delphoi: hidden item (delphoi_stardust)
#define FLAG_ICHOR_HIDDEN_ITEM_DELPHOI_BRONZE_OBOL (FLAG_ICHOR_GENERAL2_START + 0x585) // Ichor: Delphoi: hidden item (delphoi_bronze_obol)
#define FLAG_ICHOR_HIDDEN_ITEM_APOLLO_HEAL_POWDER (FLAG_ICHOR_GENERAL2_START + 0x586) // Ichor: Delphoi: hidden item (apollo_heal_powder)
#define FLAG_ICHOR_HIDE_OCHTHOS_DELPHOI         (FLAG_ICHOR_GENERAL2_START + 0x587) // Ichor: Delphoi: hide Ochthos and his mother in the Asclepeion (until the climax)
#define FLAG_ICHOR_HIDDEN_ITEM_APOLLO_STARDUST  (FLAG_ICHOR_GENERAL2_START + 0x588) // Ichor: Temple of Apollo: hidden Stardust by the lyre
#define FLAG_ICHOR_HIDDEN_ITEM_OMPHALOS_STAIR_1 (FLAG_ICHOR_GENERAL2_START + 0x589) // Ichor: Omphalos stair: hidden item in the first niche
#define FLAG_ICHOR_HIDDEN_ITEM_OMPHALOS_STAIR_2 (FLAG_ICHOR_GENERAL2_START + 0x58A) // Ichor: Omphalos stair: hidden item on the lower landing
#define FLAG_ICHOR_ITEM_OMPHALOS_STAIR          (FLAG_ICHOR_GENERAL2_START + 0x58B) // Ichor: Omphalos stair: Hyperion's dropped pack
// Ichor bank flags: end

// Ichor: the Pantheon's four seats reuse Emerald's Elite Four defeat flags, so the
// whiteout and Hall of Heroes resets (EverGrandeCity_HallOfFame_EventScript_ResetEliteFour)
// keep working unchanged (design/LEAGUE.md).
#define FLAG_ICHOR_BEAT_BRASIDAS                FLAG_DEFEATED_ELITE_4_SIDNEY
#define FLAG_ICHOR_BEAT_THEMISTOKLES            FLAG_DEFEATED_ELITE_4_PHOEBE
#define FLAG_ICHOR_BEAT_HYPATIA                 FLAG_DEFEATED_ELITE_4_GLACIA
#define FLAG_ICHOR_BEAT_OLYMPIAS                FLAG_DEFEATED_ELITE_4_DRAKE

// Ichor daily flag bank, cleared every day by Ichor_DoDailyEvents.
#define ICHOR_DAILY_FLAGS_START                 0x2800
#define ICHOR_DAILY_FLAGS_COUNT                 256
#define ICHOR_DAILY_FLAGS_END                   (ICHOR_DAILY_FLAGS_START + ICHOR_DAILY_FLAGS_COUNT - 1)

#define FLAG_DAILY_ICHOR_PRAYED_START           (ICHOR_DAILY_FLAGS_START + 0x00) // 16: prayed to each god today (§3); slot 0 (no god) is Ares's bout
#define FLAG_DAILY_ICHOR_ARES_BOUT              (ICHOR_DAILY_FLAGS_START + 0x00) // fought Ares's war-acolyte today
#define FLAG_DAILY_ICHOR_DIG_START              (ICHOR_DAILY_FLAGS_START + 0x10) // 96 daily dig spots (§5)
#define FLAG_DAILY_ICHOR_LAUREL_START           (ICHOR_DAILY_FLAGS_START + 0x70) // 32 laurel trees, one sprig a day (§3)
#define FLAG_DAILY_ICHOR_GENERAL_START          (ICHOR_DAILY_FLAGS_START + 0x90) // 112 claimed by name, below
#define FLAG_DAILY_ICHOR_GENERAL_COUNT          (ICHOR_DAILY_FLAGS_COUNT - 0x90)
// Ichor daily bank flags: claim.py dailyflag adds lines here, in order.
#define FLAG_DAILY_ICHOR_FESTIVAL_JOINED        (FLAG_DAILY_ICHOR_GENERAL_START + 0x000) // Ichor: joined today's festival: its god's +5 Favor is given (engine, ENGINE_API §7)
#define FLAG_DAILY_ICHOR_AUGURY_READ            (FLAG_DAILY_ICHOR_GENERAL_START + 0x040) // Ichor: heard today's shared omen; prevents repeated augur blessings
#define FLAG_DAILY_ICHOR_TREADING               (FLAG_DAILY_ICHOR_GENERAL_START + 0x04C) // Ichor: trod Staphylos's grapes today (Thyrsa)
// Ichor daily bank flags: end

// Temp flag aliases
#define FLAG_TEMP_SKIP_GABBY_INTERVIEW          FLAG_TEMP_1
#define FLAG_TEMP_REGICE_PUZZLE_STARTED         FLAG_TEMP_2
#define FLAG_TEMP_REGICE_PUZZLE_FAILED          FLAG_TEMP_3
#define FLAG_TEMP_HIDE_FOLLOWER                 FLAG_TEMP_E
#define FLAG_TEMP_HIDE_MIRAGE_ISLAND_BERRY_TREE FLAG_TEMP_11

// FRLG flags

#define FLAG_HIDE_BULBASAUR_BALL                           0
#define FLAG_HIDE_SQUIRTLE_BALL                            0
#define FLAG_HIDE_CHARMANDER_BALL                          0
#define FLAG_HIDE_OAK_IN_HIS_LAB                           0
#define FLAG_HIDE_OAK_IN_PALLET_TOWN                       0
#define FLAG_HIDE_RIVAL_IN_LAB                             0
#define FLAG_HIDE_PEWTER_CITY_GYM_GUIDE                    0
#define FLAG_HIDE_DOME_FOSSIL                              0
#define FLAG_HIDE_HELIX_FOSSIL                             0
#define FLAG_HIDE_NUGGET_BRIDGE_ROCKET                     0
#define FLAG_HIDE_BILL_CLEFAIRY                            0
#define FLAG_HIDE_BILL_HUMAN_SEA_COTTAGE                   0
#define FLAG_HIDE_TOWER_FUJI                               0
#define FLAG_HIDE_POKEHOUSE_FUJI                           0
#define FLAG_HIDE_LIFT_KEY                                 0
#define FLAG_HIDE_SILPH_SCOPE                              0
#define FLAG_HIDE_HIDEOUT_GIOVANNI                         0
#define FLAG_HIDE_TOWN_MAP                                 0
#define FLAG_HIDE_POKEDEX                                  0
#define FLAG_HIDE_CERULEAN_ROCKET                          0
#define FLAG_HIDE_CERULEAN_RIVAL                           0
#define FLAG_HIDE_SS_ANNE_RIVAL                            0
#define FLAG_HIDE_SAFFRON_ROCKETS                          0
#define FLAG_HIDE_SAFFRON_CIVILIANS                        0
#define FLAG_HIDE_SEAFOAM_1F_BOULDER_1                     0
#define FLAG_HIDE_SEAFOAM_1F_BOULDER_2                     0
#define FLAG_HIDE_SEAFOAM_B1F_BOULDER_1                    0
#define FLAG_HIDE_SEAFOAM_B1F_BOULDER_2                    0
#define FLAG_HIDE_SEAFOAM_B2F_BOULDER_1                    0
#define FLAG_HIDE_SEAFOAM_B2F_BOULDER_2                    0
#define FLAG_HIDE_SEAFOAM_B3F_BOULDER_1                    0
#define FLAG_HIDE_SEAFOAM_B3F_BOULDER_2                    0
#define FLAG_HIDE_SEAFOAM_B3F_BOULDER_3                    0
#define FLAG_HIDE_SEAFOAM_B3F_BOULDER_4                    0
#define FLAG_HIDE_SEAFOAM_B3F_BOULDER_5                    0
#define FLAG_HIDE_SEAFOAM_B3F_BOULDER_6                    0
#define FLAG_HIDE_SEAFOAM_B4F_BOULDER_1                    0
#define FLAG_HIDE_SEAFOAM_B4F_BOULDER_2                    0
#define FLAG_HIDE_SILPH_RIVAL                              0
#define FLAG_HIDE_ROUTE_22_RIVAL                           0
#define FLAG_HIDE_PEWTER_MUSEUM_GUIDE                      0
#define FLAG_HIDE_TOWER_RIVAL                              0
#define FLAG_HIDE_MOLTRES                                  0
#define FLAG_HIDE_SILPH_ROCKETS                            0
#define FLAG_HIDE_ROUTE_12_SNORLAX                         0
#define FLAG_HIDE_VIRIDIAN_GIOVANNI                        0
#define FLAG_HIDE_OLD_AMBER                                0
#define FLAG_HIDE_EEVEE_BALL                               0
#define FLAG_HIDE_VICTORY_ROAD_2F_BOULDER                  0
#define FLAG_HIDE_VICTORY_ROAD_3F_BOULDER                  0
#define FLAG_HIDE_OAK_IN_CHAMP_ROOM                        0
#define FLAG_HIDE_GAME_CORNER_ROCKET                       0
#define FLAG_HIDE_CERULEAN_CAVE_GUARD                      0
#define FLAG_HIDE_ZAPDOS                                   0
#define FLAG_HIDE_TOWER_ROCKET_1                           0
#define FLAG_HIDE_CELADON_ROCKETS                          0
#define FLAG_HIDE_DOJO_HITMONLEE_BALL                      0
#define FLAG_HIDE_DOJO_HITMONCHAN_BALL                     0
#define FLAG_HIDE_CINNABAR_BILL                            0
#define FLAG_HIDE_UNION_ROOM_PLAYER_1                      0
#define FLAG_HIDE_UNION_ROOM_PLAYER_2                      0
#define FLAG_HIDE_UNION_ROOM_PLAYER_3                      0
#define FLAG_HIDE_UNION_ROOM_PLAYER_4                      0
#define FLAG_HIDE_UNION_ROOM_PLAYER_5                      0
#define FLAG_HIDE_UNION_ROOM_PLAYER_6                      0
#define FLAG_HIDE_UNION_ROOM_PLAYER_7                      0
#define FLAG_HIDE_UNION_ROOM_PLAYER_8                      0
#define FLAG_HIDE_CINNABAR_SEAGALLOP                       0
#define FLAG_HIDE_SAFFRON_FAN_CLUB_BLACKBELT               0
#define FLAG_HIDE_SAFFRON_FAN_CLUB_ROCKER                  0
#define FLAG_HIDE_SAFFRON_FAN_CLUB_WOMAN                   0
#define FLAG_HIDE_SAFFRON_FAN_CLUB_BEAUTY                  0
#define FLAG_HIDE_MG_DELIVERYMEN                           0
#define FLAG_HIDE_ONE_ISLAND_BILL                          0
#define FLAG_HIDE_ONE_ISLAND_POKECENTER_BILL               0
#define FLAG_HIDE_ONE_ISLAND_POKECENTER_CELIO              0
#define FLAG_HIDE_TWO_ISLAND_GAME_CORNER_BIKER             0
#define FLAG_HIDE_TWO_ISLAND_GAME_CORNER_LOSTELLE          0
#define FLAG_HIDE_LOSTELLE_IN_HER_HOME                     0
#define FLAG_0x077                                         0
#define FLAG_0x078                                         0
#define FLAG_HIDE_THREE_ISLAND_BIKERS                      0
#define FLAG_HIDE_LOSTELLE_IN_BERRY_FOREST                 0
#define FLAG_HIDE_TWO_ISLAND_WOMAN                         0
#define FLAG_HIDE_TWO_ISLAND_BEAUTY                        0
#define FLAG_HIDE_TWO_ISLAND_SUPER_NERD                    0
#define FLAG_HIDE_THREE_ISLAND_ANTIBIKERS                  0
#define FLAG_0x07F                                         0
#define FLAG_HIDE_ROUTE_16_SNORLAX                         0
#define FLAG_HIDE_MEWTWO                                   0
#define FLAG_HIDE_ARTICUNO                                 0
#define FLAG_HIDE_TOWER_ROCKET_2                           0
#define FLAG_HIDE_TOWER_ROCKET_3                           0
#define FLAG_HIDE_POWER_PLANT_ELECTRODE_1                  0
#define FLAG_HIDE_POWER_PLANT_ELECTRODE_2                  0
#define FLAG_HIDE_SS_ANNE                                  0
#define FLAG_HIDE_FIVE_ISLAND_ROCKETS                      0
#define FLAG_HIDE_MT_EMBER_EXTERIOR_ROCKETS                0
#define FLAG_HIDE_RUBY                                     0
#define FLAG_HIDE_ICEFALL_CAVE_LORELEI                     0
#define FLAG_HIDE_LORELEI_IN_HER_HOUSE                     0
#define FLAG_HIDE_ICEFALL_CAVE_ROCKETS                     0
#define FLAG_HIDE_RUIN_VALLEY_SCIENTIST                    0
#define FLAG_HIDE_SAPPHIRE                                 0
#define FLAG_HIDE_DOTTED_HOLE_SCIENTIST                    0
#define FLAG_HIDE_THREE_ISLAND_LONE_BIKER                  0
#define FLAG_HIDE_PEWTER_CITY_RUNNING_SHOES_GUY            0
#define FLAG_HIDE_LOST_CAVE_SELPHY                         0
#define FLAG_HIDE_RESORT_GORGEOUS_SELPHY                   0
#define FLAG_HIDE_RESORT_GORGEOUS_INSIDE_SELPHY            0
#define FLAG_HIDE_SELPHYS_BUTLER                           0
#define FLAG_HIDE_FOUR_ISLAND_RIVAL                        0
#define FLAG_HIDE_SIX_ISLAND_POKECENTER_RIVAL              0
#define FLAG_HIDE_BIRTH_ISLAND_METEORITE                   0
#define FLAG_HIDE_POSTGAME_GOSSIPERS                       0
#define FLAG_HIDE_FAME_CHECKER_ERIKA_JOURNALS              0
#define FLAG_HIDE_FAME_CHECKER_KOGA_JOURNAL                0
#define FLAG_HIDE_FAME_CHECKER_LT_SURGE_JOURNAL            0
#define FLAG_HIDE_VERMILION_CITY_OAKS_AIDE                 0
#define FLAG_HIDE_CINNABAR_POKECENTER_BILL                 0
#define FLAG_HIDE_CREDITS_RIVAL                            0
#define FLAG_HIDE_CREDITS_OAK                              0
#define FLAG_HIDE_LORELEI_HOUSE_MEOWTH_DOLL                0
#define FLAG_HIDE_LORELEI_HOUSE_CHANSEY_DOLL               0
#define FLAG_HIDE_LORELEIS_HOUSE_NIDORAN_F_DOLL            0
#define FLAG_HIDE_LORELEI_HOUSE_JIGGLYPUFF_DOLL            0
#define FLAG_HIDE_LORELEIS_HOUSE_NIDORAN_M_DOLL            0
#define FLAG_HIDE_LORELEIS_HOUSE_FEAROW_DOLL               0
#define FLAG_HIDE_LORELEIS_HOUSE_PIDGEOT_DOLL              0
#define FLAG_HIDE_LORELEIS_HOUSE_LAPRAS_DOLL               0
#define FLAG_HIDE_MISC_KANTO_ROCKETS                       0
#define FLAG_HIDE_SAFFRON_CITY_POKECENTER_SABRINA_JOURNALS 0

#define FLAG_HIDE_ROUTE2_ETHER                                  0
#define FLAG_HIDE_ROUTE2_PARALYZE_HEAL                          0
#define FLAG_HIDE_VIRIDIAN_FOREST_POKE_BALL                     0
#define FLAG_HIDE_VIRIDIAN_FOREST_ANTIDOTE                      0
#define FLAG_HIDE_VIRIDIAN_FOREST_POTION                        0
#define FLAG_HIDE_MT_MOON_1F_PARALYZE_HEAL                      0
#define FLAG_HIDE_MT_MOON_1F_TM09                               0
#define FLAG_HIDE_MT_MOON_1F_POTION                             0
#define FLAG_HIDE_MT_MOON_1F_RARE_CANDY                         0
#define FLAG_HIDE_MT_MOON_1F_ESCAPE_ROPE                        0
#define FLAG_HIDE_MT_MOON_1F_MOON_STONE                         0
#define FLAG_HIDE_MT_MOON_B2F_STAR_PIECE                        0
#define FLAG_HIDE_MT_MOON_B2F_TM46                              0
#define FLAG_HIDE_ROUTE4_TM05                                   0
#define FLAG_HIDE_ROUTE24_TM45                                  0
#define FLAG_HIDE_ROUTE25_TM43                                  0
#define FLAG_HIDE_SSANNE_1F_ROOM2_TM31                          0
#define FLAG_HIDE_SSANNE_2F_ROOM2_STARDUST                      0
#define FLAG_HIDE_SSANNE_2F_ROOM4_X_ATTACK                      0
#define FLAG_HIDE_SSANNE_B1F_ROOM2_TM44                         0
#define FLAG_HIDE_SSANNE_B1F_ROOM3_ETHER                        0
#define FLAG_HIDE_SSANNE_B1F_ROOM5_SUPER_POTION                 0
#define FLAG_HIDE_SSANNE_KITCHEN_GREAT_BALL                     0
#define FLAG_HIDE_ROUTE9_TM40                                   0
#define FLAG_HIDE_ROCKET_HIDEOUT_B1F_ESCAPE_ROPE                0
#define FLAG_HIDE_ROCKET_HIDEOUT_B1F_HYPER_POTION               0
#define FLAG_HIDE_ROCKET_HIDEOUT_B2F_X_SPEED                    0
#define FLAG_HIDE_ROCKET_HIDEOUT_B2F_MOON_STONE                 0
#define FLAG_HIDE_ROCKET_HIDEOUT_B2F_TM12                       0
#define FLAG_HIDE_ROCKET_HIDEOUT_B2F_SUPER_POTION               0
#define FLAG_HIDE_ROCKET_HIDEOUT_B3F_RARE_CANDY                 0
#define FLAG_HIDE_ROCKET_HIDEOUT_B3F_TM21                       0
#define FLAG_HIDE_ROCKET_HIDEOUT_B4F_TM49                       0
#define FLAG_HIDE_ROCKET_HIDEOUT_B4F_MAX_ETHER                  0
#define FLAG_HIDE_ROCKET_HIDEOUT_B4F_CALCIUM                    0
#define FLAG_HIDE_POKEMON_TOWER_3F_ESCAPE_ROPE                  0
#define FLAG_HIDE_POKEMON_TOWER_4F_ELIXIR                       0
#define FLAG_HIDE_POKEMON_TOWER_4F_AWAKENING                    0
#define FLAG_HIDE_POKEMON_TOWER_4F_GREAT_BALL                   0
#define FLAG_HIDE_POKEMON_TOWER_5F_NUGGET                       0
#define FLAG_HIDE_POKEMON_TOWER_6F_RARE_CANDY                   0
#define FLAG_HIDE_POKEMON_TOWER_6F_X_ACCURACY                   0
#define FLAG_HIDE_ROUTE12_TM48                                  0
#define FLAG_HIDE_ROUTE12_IRON                                  0
#define FLAG_HIDE_ROUTE15_TM18                                  0
#define FLAG_HIDE_SAFARI_ZONE_CENTER_NUGGET                     0
#define FLAG_HIDE_SAFARI_ZONE_EAST_MAX_POTION                   0
#define FLAG_HIDE_SAFARI_ZONE_EAST_FULL_RESTORE                 0
#define FLAG_HIDE_SAFARI_ZONE_EAST_TM11                         0
#define FLAG_HIDE_SAFARI_ZONE_EAST_LEAF_STONE                   0
#define FLAG_HIDE_SAFARI_ZONE_NORTH_PROTEIN                     0
#define FLAG_HIDE_SAFARI_ZONE_NORTH_TM47                        0
#define FLAG_HIDE_SAFARI_ZONE_WEST_TM32                         0
#define FLAG_HIDE_SAFARI_ZONE_WEST_GOLD_TEETH                   0
#define FLAG_HIDE_SAFARI_ZONE_WEST_MAX_POTION                   0
#define FLAG_HIDE_SAFARI_ZONE_WEST_MAX_REVIVE                   0
#define FLAG_HIDE_SILPH_CO_3F_HYPER_POTION                      0
#define FLAG_HIDE_SILPH_CO_4F_MAX_REVIVE                        0
#define FLAG_HIDE_SILPH_CO_4F_ESCAPE_ROPE                       0
#define FLAG_HIDE_SILPH_CO_4F_FULL_HEAL                         0
#define FLAG_HIDE_SILPH_CO_5F_PROTEIN                           0
#define FLAG_HIDE_SILPH_CO_5F_TM01                              0
#define FLAG_HIDE_SILPH_CO_5F_CARD_KEY                          0
#define FLAG_HIDE_SILPH_CO_6F_HP_UP                             0
#define FLAG_HIDE_SILPH_CO_6F_X_SPECIAL                         0
#define FLAG_HIDE_SILPH_CO_7F_CALCIUM                           0
#define FLAG_HIDE_SILPH_CO_7F_TM08                              0
#define FLAG_HIDE_SILPH_CO_10F_CARBOS                           0
#define FLAG_HIDE_SILPH_CO_10F_ULTRA_BALL                       0
#define FLAG_HIDE_SILPH_CO_10F_RARE_CANDY                       0
#define FLAG_HIDE_POWER_PLANT_MAX_POTION                        0
#define FLAG_HIDE_POWER_PLANT_TM17                              0
#define FLAG_HIDE_POWER_PLANT_TM25                              0
#define FLAG_HIDE_POWER_PLANT_THUNDER_STONE                     0
#define FLAG_HIDE_POWER_PLANT_ELIXIR                            0
#define FLAG_HIDE_POKEMON_MANSION_1F_CARBOS                     0
#define FLAG_HIDE_POKEMON_MANSION_1F_ESCAPE_ROPE                0
#define FLAG_HIDE_POKEMON_MANSION_2F_CALCIUM                    0
#define FLAG_HIDE_POKEMON_MANSION_3F_MAX_POTION                 0
#define FLAG_HIDE_POKEMON_MANSION_3F_IRON                       0
#define FLAG_HIDE_POKEMON_MANSION_B1F_TM14                      0
#define FLAG_HIDE_POKEMON_MANSION_B1F_FULL_RESTORE              0
#define FLAG_0x1A6                                              0
#define FLAG_HIDE_POKEMON_MANSION_B1F_TM22                      0
#define FLAG_HIDE_POKEMON_MANSION_B1F_SECRET_KEY                0
#define FLAG_HIDE_VICTORY_ROAD_1F_RARE_CANDY                    0
#define FLAG_HIDE_VICTORY_ROAD_1F_TM02                          0
#define FLAG_HIDE_VICTORY_ROAD_2F_GUARD_SPEC                    0
#define FLAG_HIDE_VICTORY_ROAD_2F_TM07                          0
#define FLAG_HIDE_VICTORY_ROAD_2F_FULL_HEAL                     0
#define FLAG_HIDE_VICTORY_ROAD_2F_TM37                          0
#define FLAG_HIDE_VICTORY_ROAD_3F_MAX_REVIVE                    0
#define FLAG_HIDE_VICTORY_ROAD_3F_TM50                          0
#define FLAG_HIDE_CERULEAN_CAVE_1F_MAX_ELIXIR                   0
#define FLAG_HIDE_CERULEAN_CAVE_1F_NUGGET                       0
#define FLAG_HIDE_CERULEAN_CAVE_1F_FULL_RESTORE                 0
#define FLAG_HIDE_CERULEAN_CAVE_2F_FULL_RESTORE                 0
#define FLAG_HIDE_CERULEAN_CAVE_2F_PP_UP                        0
#define FLAG_HIDE_CERULEAN_CAVE_2F_ULTRA_BALL                   0
#define FLAG_HIDE_CERULEAN_CAVE_B1F_MAX_REVIVE                  0
#define FLAG_HIDE_CERULEAN_CAVE_B1F_ULTRA_BALL                  0
#define FLAG_HIDE_FUCHSIA_CITY_WARDENS_HOUSE_RARE_CANDY         0
#define FLAG_HIDE_TWO_ISLAND_REVIVE                             0
#define FLAG_HIDE_THREE_ISLAND_ZINC                             0
#define FLAG_0x1BC                                              0
#define FLAG_0x1BD                                              0
#define FLAG_HIDE_VIRIDIAN_FOREST_POTION_2                      0
#define FLAG_HIDE_MT_MOON_B2F_REVIVE                            0
#define FLAG_HIDE_MT_MOON_B2F_ANTIDOTE                          0
#define FLAG_HIDE_ROUTE11_X_DEFEND                              0
#define FLAG_HIDE_ROUTE9_BURN_HEAL                              0
#define FLAG_HIDE_ROCK_TUNNEL_1F_REPEL                          0
#define FLAG_HIDE_ROCK_TUNNEL_1F_PEARL                          0
#define FLAG_HIDE_ROCK_TUNNEL_1F_ESCAPE_ROPE                    0
#define FLAG_HIDE_ROCK_TUNNEL_B1F_REVIVE                        0
#define FLAG_HIDE_ROCK_TUNNEL_B1F_MAX_ETHER                     0
#define FLAG_HIDE_SILPH_CO_8F_IRON                              0
#define FLAG_HIDE_SILPH_CO_11F_ZINC                             0
#define FLAG_HIDE_POKEMON_MANSION_1F_PROTEIN                    0
#define FLAG_HIDE_POKEMON_MANSION_2F_ZINC                       0
#define FLAG_HIDE_POKEMON_MANSION_2F_HP_UP                      0
#define FLAG_HIDE_VIRIDIAN_CITY_POTION                          0
#define FLAG_HIDE_ROUTE11_GREAT_BALL                            0
#define FLAG_HIDE_ROUTE11_AWAKENING                             0
#define FLAG_HIDE_POKEMON_TOWER_5F_CLEANSE_TAG                  0
#define FLAG_HIDE_CELADON_CITY_ETHER                            0
#define FLAG_HIDE_ROCKET_HIDEOUT_B3F_BLACK_GLASSES              0
#define FLAG_HIDE_SAFARI_ZONE_NORTH_QUICK_CLAW                  0
#define FLAG_HIDE_SEAFOAM_ISLANDS_1F_ICE_HEAL                   0
#define FLAG_HIDE_SEAFOAM_ISLANDS_B1F_WATER_STONE               0
#define FLAG_HIDE_SEAFOAM_ISLANDS_B1F_REVIVE                    0
#define FLAG_HIDE_SEAFOAM_ISLANDS_B2F_BIG_PEARL                 0
#define FLAG_HIDE_SEAFOAM_ISLANDS_B4F_ULTRA_BALL                0
#define FLAG_HIDE_FOUR_ISLAND_STAR_PIECE                        0
#define FLAG_HIDE_FOUR_ISLAND_STARDUST                          0
#define FLAG_HIDE_ONE_ISLAND_KINDLE_ROAD_ETHER                  0
#define FLAG_HIDE_ONE_ISLAND_KINDLE_ROAD_MAX_REPEL              0
#define FLAG_HIDE_ONE_ISLAND_KINDLE_ROAD_CARBOS                 0
#define FLAG_HIDE_FIVE_ISLAND_MEADOW_MAX_POTION                 0
#define FLAG_HIDE_FIVE_ISLAND_MEADOW_PP_UP                      0
#define FLAG_HIDE_FIVE_ISLAND_MEMORIAL_PILLAR_METAL_COAT        0
#define FLAG_HIDE_SIX_ISLAND_OUTCAST_ISLAND_PP_UP               0
#define FLAG_HIDE_SIX_ISLAND_WATER_PATH_ELIXIR                  0
#define FLAG_HIDE_SIX_ISLAND_WATER_PATH_DRAGON_SCALE            0
#define FLAG_HIDE_SIX_ISLAND_RUIN_VALLEY_FULL_RESTORE           0
#define FLAG_HIDE_SIX_ISLAND_RUIN_VALLEY_HP_UP                  0
#define FLAG_HIDE_SIX_ISLAND_RUIN_VALLEY_SUN_STONE              0
#define FLAG_HIDE_SEVEN_ISLAND_SEVAULT_CANYON_KINGS_ROCK        0
#define FLAG_HIDE_SEVEN_ISLAND_SEVAULT_CANYON_MAX_ELIXIR        0
#define FLAG_HIDE_SEVEN_ISLAND_SEVAULT_CANYON_NUGGET            0
#define FLAG_HIDE_THREE_ISLAND_BERRY_FOREST_MAX_ETHER           0
#define FLAG_HIDE_THREE_ISLAND_BERRY_FOREST_FULL_HEAL           0
#define FLAG_HIDE_THREE_ISLAND_BERRY_FOREST_MAX_ELIXIR          0
#define FLAG_HIDE_MT_EMBER_EXTERIOR_ULTRA_BALL                  0
#define FLAG_HIDE_MT_EMBER_EXTERIOR_FIRE_STONE                  0
#define FLAG_HIDE_MT_EMBER_EXTERIOR_DIRE_HIT                    0
#define FLAG_HIDE_FOUR_ISLAND_ICEFALL_CAVE_1F_ULTRA_BALL        0
#define FLAG_HIDE_FOUR_ISLAND_ICEFALL_CAVE_1F_HM07              0
#define FLAG_HIDE_FOUR_ISLAND_ICEFALL_CAVE_B1F_FULL_RESTORE     0
#define FLAG_HIDE_FOUR_ISLAND_ICEFALL_CAVE_B1F_NEVER_MELT_ICE   0
#define FLAG_HIDE_FIVE_ISLAND_ROCKET_WAREHOUSE_BIG_PEARL        0
#define FLAG_HIDE_FIVE_ISLAND_ROCKET_WAREHOUSE_TM36             0
#define FLAG_HIDE_FIVE_ISLAND_ROCKET_WAREHOUSE_PEARL            0
#define FLAG_HIDE_FIVE_ISLAND_ROCKET_WAREHOUSE_UP_GRADE         0
#define FLAG_HIDE_FIVE_ISLAND_LOST_CAVE_ROOM10_SILK_SCARF       0
#define FLAG_HIDE_FIVE_ISLAND_LOST_CAVE_ROOM11_LAX_INCENSE      0
#define FLAG_HIDE_FIVE_ISLAND_LOST_CAVE_ROOM12_SEA_INCENSE      0
#define FLAG_HIDE_FIVE_ISLAND_LOST_CAVE_ROOM13_MAX_REVIVE       0
#define FLAG_HIDE_FIVE_ISLAND_LOST_CAVE_ROOM14_RARE_CANDY       0
#define FLAG_HIDE_SEVEN_ISLAND_SEVAULT_CANYON_HOUSE_LUCKY_PUNCH 0
#define FLAG_HIDE_SILPH_CO_4F_TM41                              0

#define STORY_FLAGS_START                                0
#define FLAG_GOT_POTION_ON_ROUTE_1                       0
#define FLAG_GOT_TM34_FROM_SURGE                         0
#define FLAG_GOT_FOSSIL_FROM_MT_MOON                     0
#define FLAG_HELPED_BILL_IN_SEA_COTTAGE                  0
#define FLAG_GOT_SS_TICKET                               0
#define FLAG_GOT_SS_TICKET_DUP                           0
#define FLAG_GOT_TM42_AT_MEMORIAL_PILLAR                 0
#define FLAG_GOT_HM01                                    0
#define FLAG_GOT_HM02                                    0
#define FLAG_GOT_HM03                                    0
#define FLAG_GOT_HM04                                    0
#define FLAG_GOT_HM05                                    0
#define FLAG_RESCUED_MR_FUJI                             0
#define FLAG_GOT_POKE_FLUTE                              0
#define FLAG_0x23E                                       0
#define FLAG_GOT_TM28_FROM_ROCKET                        0
#define FLAG_GOT_OLD_ROD                                 0
#define FLAG_GOT_BIKE_VOUCHER                            0
#define FLAG_0x242                                       0
#define FLAG_GOT_COIN_CASE                               0
#define FLAG_GOT_GOOD_ROD                                0
#define FLAG_GOT_TM29_FROM_MR_PSYCHIC                    0
#define FLAG_GOT_LAPRAS_FROM_SILPH                       0
#define FLAG_GOT_POKEBALLS_FROM_OAK_AFTER_22_RIVAL       0
#define FLAG_DID_MIMIEN_TRADE                            0
#define FLAG_BOUGHT_MAGIKARP                             0
#define FLAG_DID_ZYNX_TRADE                              0
#define FLAG_DID_MS_NIDO_TRADE                           0
#define FLAG_0x24C                                       0
#define FLAG_DID_CH_DING_TRADE                           0
#define FLAG_GOT_TM38_FROM_BLAINE                        0
#define FLAG_OAK_SKIP_22_RIVAL_CHECK                     0
#define FLAG_GOT_MASTER_BALL_FROM_SILPH                  0
#define FLAG_DID_NINA_TRADE                              0
#define FLAG_GOT_ITEMFINDER                              0
#define FLAG_WOKE_UP_ROUTE_12_SNORLAX                    0
#define FLAG_GOT_TM39_FROM_BROCK                         0
#define FLAG_GOT_SUPER_ROD                               0
#define FLAG_GOT_EXP_SHARE_FROM_OAKS_AIDE                0
#define FLAG_DID_MARC_TRADE                              0
#define FLAG_BEAT_RIVAL_IN_OAKS_LAB                      0
#define FLAG_GOT_TM06_FROM_KOGA                          0
#define FLAG_0x25A                                       0
#define FLAG_GOT_TM27                                    0
#define FLAG_0x25C                                       0
#define FLAG_0x25D                                       0
#define FLAG_GOT_OLD_AMBER                               0
#define FLAG_0x25F                                       0
#define FLAG_0x260                                       0
#define FLAG_0x261                                       0
#define FLAG_0x262                                       0
#define FLAG_GOT_EEVEE                                   0
#define FLAG_FOUND_BOTH_VERMILION_GYM_SWITCHES           0
#define FLAG_CINNABAR_GYM_QUIZ_1                         0
#define FLAG_CINNABAR_GYM_QUIZ_2                         0
#define FLAG_CINNABAR_GYM_QUIZ_3                         0
#define FLAG_CINNABAR_GYM_QUIZ_4                         0
#define FLAG_CINNABAR_GYM_QUIZ_5                         0
#define FLAG_CINNABAR_GYM_QUIZ_6                         0
#define FLAG_POKEMON_MANSION_SWITCH_STATE                0
#define FLAG_OPENED_ROCKET_HIDEOUT                       0
#define FLAG_GOT_10_COINS_FROM_GAMBLER                   0
#define FLAG_GOT_20_COINS_FROM_GAMBLER                   0
#define FLAG_GOT_20_COINS_FROM_GAMBLER_2                 0
#define FLAG_GOT_BICYCLE                                 0
#define FLAG_GOT_DOME_FOSSIL                             0
#define FLAG_GOT_HELIX_FOSSIL                            0
#define FLAG_DID_ESPHERE_TRADE                           0
#define FLAG_DID_TANGENY_TRADE                           0
#define FLAG_DID_SEELOR_TRADE                            0
#define FLAG_0x277                                       0
#define FLAG_GOT_HITMON_FROM_DOJO                        0
#define FLAG_0x279                                       0
#define FLAG_SILPH_2F_DOOR_1                             0
#define FLAG_SILPH_2F_DOOR_2                             0
#define FLAG_SILPH_3F_DOOR_1                             0
#define FLAG_SILPH_3F_DOOR_2                             0
#define FLAG_SILPH_4F_DOOR_1                             0
#define FLAG_SILPH_4F_DOOR_2                             0
#define FLAG_SILPH_5F_DOOR_1                             0
#define FLAG_SILPH_5F_DOOR_2                             0
#define FLAG_SILPH_5F_DOOR_3                             0
#define FLAG_SILPH_6F_DOOR                               0
#define FLAG_SILPH_7F_DOOR_1                             0
#define FLAG_SILPH_7F_DOOR_2                             0
#define FLAG_SILPH_7F_DOOR_3                             0
#define FLAG_SILPH_8F_DOOR                               0
#define FLAG_SILPH_9F_DOOR_1                             0
#define FLAG_SILPH_9F_DOOR_2                             0
#define FLAG_SILPH_9F_DOOR_3                             0
#define FLAG_SILPH_9F_DOOR_4                             0
#define FLAG_SILPH_10F_DOOR                              0
#define FLAG_SILPH_11F_DOOR                              0
#define FLAG_0x28E                                       0
#define FLAG_0x28F                                       0
#define FLAG_MET_STICKER_MAN                             0
#define FLAG_PALLET_LADY_NOT_BLOCKING_SIGN               0
#define FLAG_GOT_VS_SEEKER                               0
#define FLAG_GOT_TM19_FROM_ERIKA                         0
#define FLAG_GOT_TM33_FROM_THIRSTY_GIRL                  0
#define FLAG_GOT_TM20_FROM_THIRSTY_GIRL                  0
#define FLAG_GOT_TM16_FROM_THIRSTY_GIRL                  0
#define FLAG_GOT_TM03_FROM_MISTY                         0
#define FLAG_GOT_TM26_FROM_GIOVANNI                      0
#define FLAG_0x299                                       0
#define FLAG_GOT_TM04_FROM_SABRINA                       0
#define FLAG_GOT_FAME_CHECKER                            0
#define FLAG_GOT_RECORD_SETTING_MAGIKARP                 0
#define FLAG_TWO_ISLAND_SHOP_INTRODUCED                  0
#define FLAG_TWO_ISLAND_SHOP_EXPANDED_1                  0
#define FLAG_TWO_ISLAND_SHOP_EXPANDED_2                  0
#define FLAG_TWO_ISLAND_SHOP_EXPANDED_3                  0
#define FLAG_SEVII_DETOUR_FINISHED                       0
#define FLAG_VISITED_TWO_ISLAND                          0
#define FLAG_RESCUED_LOSTELLE                            0
#define FLAG_0x2A4                                       0
#define FLAG_CAN_USE_ROCKET_HIDEOUT_LIFT                 0
#define FLAG_GOT_TEA                                     0
#define FLAG_GOT_POWDER_JAR                              0
#define FLAG_FOUGHT_MEWTWO                               0
#define FLAG_FOUGHT_MOLTRES                              0
#define FLAG_FOUGHT_ARTICUNO                             0
#define FLAG_FOUGHT_ZAPDOS                               0
#define FLAG_TUTOR_DOUBLE_EDGE                           0
#define FLAG_TUTOR_THUNDER_WAVE                          0
#define FLAG_TUTOR_ROCK_SLIDE                            0
#define FLAG_TUTOR_EXPLOSION                             0
#define FLAG_TUTOR_MEGA_PUNCH                            0
#define FLAG_TUTOR_MEGA_KICK                             0
#define FLAG_TUTOR_DREAM_EATER                           0
#define FLAG_TUTOR_SOFT_BOILED                           0
#define FLAG_TUTOR_SUBSTITUTE                            0
#define FLAG_TUTOR_SWORDS_DANCE                          0
#define FLAG_TUTOR_SEISMIC_TOSS                          0
#define FLAG_TUTOR_COUNTER                               0
#define FLAG_TUTOR_METRONOME                             0
#define FLAG_TUTOR_MIMIC                                 0
#define FLAG_TUTOR_BODY_SLAM                             0
#define FLAG_VISITED_OAKS_LAB                            0
#define FLAG_FOUGHT_POWER_PLANT_ELECTRODE_1              0
#define FLAG_FOUGHT_POWER_PLANT_ELECTRODE_2              0
#define FLAG_STOPPED_SEAFOAM_B3F_CURRENT                 0
#define FLAG_STOPPED_SEAFOAM_B4F_CURRENT                 0
#define FLAG_TALKED_TO_LORELEI_AFTER_WAREHOUSE           0
#define FLAG_DEFEATED_ROCKETS_IN_WAREHOUSE               0
#define FLAG_UNLOCKED_ROCKET_WAREHOUSE                   0
#define FLAG_NO_ROOM_FOR_TM42_AT_MEMORIAL_PILLAR         0
#define FLAG_LEARNED_YES_NAH_CHANSEY                     0
#define FLAG_GOT_NEST_BALL_FROM_WATER_PATH_HOUSE_1       0
#define FLAG_GOT_TOGEPI_EGG                              0
#define FLAG_NO_ROOM_FOR_TOGEPI_EGG                      0
#define FLAG_RECOVERED_SAPPHIRE                          0
#define FLAG_GOT_RUBY                                    0
#define FLAG_TUTOR_FRENZY_PLANT                          0
#define FLAG_TUTOR_BLAST_BURN                            0
#define FLAG_TUTOR_HYDRO_CANNON                          0
#define FLAG_LEARNED_ALL_MOVES_AT_CAPE_BRINK             0
#define FLAG_GOT_NUGGET_FROM_DUNSPARCE_TUNNEL            0
#define FLAG_USED_CUT_ON_RUIN_VALLEY_BRAILLE             0
#define FLAG_FOUGHT_DEOXYS                               0
#define FLAG_0x2E5                                       0
#define FLAG_0x2E6                                       0
#define FLAG_0x2E7                                       0
#define FLAG_0x2E8                                       0
#define FLAG_0x2E9                                       0
#define FLAG_0x2EA                                       0
#define FLAG_0x2EB                                       0
#define FLAG_REVIVED_DOME                                0
#define FLAG_REVIVED_HELIX                               0
#define FLAG_REVIVED_AMBER                               0
#define FLAG_GOT_HM06                                    0
#define FLAG_FOUGHT_LUGIA                                0
#define FLAG_FOUGHT_HO_OH                                0
#define FLAG_OAK_SAW_DEX_COMPLETION                      0
#define FLAG_LUGIA_FLEW_AWAY                             0
#define FLAG_HO_OH_FLEW_AWAY                             0
#define FLAG_DEOXYS_FLEW_AWAY                            0
#define FLAG_TALKED_TO_TEA_LADY_AFTER_HOF                0
#define FLAG_TALKED_TO_OAKS_AIDE_IN_VERMILION            0
#define FLAG_GOT_EVERSTONE_FROM_OAKS_AIDE                0
#define FLAG_GOT_MOON_STONE_FROM_JOYFUL_GAME_CORNER      0
#define FLAG_GOT_FULL_RESTORE_FROM_THREE_ISLAND_DEFENDER 0
#define FLAG_GOT_AMULET_COIN_FROM_OAKS_AIDE              0
#define FLAG_NO_ROOM_FOR_JOYFUL_GAME_CORNER_MOON_STONE   0
#define FLAG_OAKS_RATING_IS_VIA_PC                       0

#define FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_POTION                            0
#define FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE                          0
#define FLAG_HIDDEN_ITEM_MT_MOON_B2F_MOON_STONE                            0
#define FLAG_HIDDEN_ITEM_MT_MOON_B2F_ETHER                                 0
#define FLAG_HIDDEN_ITEM_ROUTE25_ELIXIR                                    0
#define FLAG_HIDDEN_ITEM_ROUTE25_ETHER                                     0
#define FLAG_HIDDEN_ITEM_ROUTE9_ETHER                                      0
#define FLAG_HIDDEN_ITEM_UNUSED_0x07                                       0
#define FLAG_HIDDEN_ITEM_SSANNE_B1F_CORRIDOR_HYPER_POTION                  0
#define FLAG_HIDDEN_ITEM_ROUTE10_SUPER_POTION                              0
#define FLAG_HIDDEN_ITEM_ROUTE10_MAX_ETHER                                 0
#define FLAG_HIDDEN_ITEM_ROCKET_HIDEOUT_B1F_PP_UP                          0
#define FLAG_HIDDEN_ITEM_ROCKET_HIDEOUT_B3F_NUGGET                         0
#define FLAG_HIDDEN_ITEM_ROCKET_HIDEOUT_B4F_NEST_BALL                      0
#define FLAG_HIDDEN_ITEM_POKEMON_TOWER_5F_BIG_MUSHROOM                     0
#define FLAG_HIDDEN_ITEM_ROUTE13_PP_UP                                     0
#define FLAG_HIDDEN_ITEM_UNUSED_0x10                                       0
#define FLAG_HIDDEN_ITEM_ROUTE17_RARE_CANDY                                0
#define FLAG_HIDDEN_ITEM_ROUTE17_FULL_RESTORE                              0
#define FLAG_HIDDEN_ITEM_ROUTE17_PP_UP                                     0
#define FLAG_HIDDEN_ITEM_ROUTE17_MAX_REVIVE                                0
#define FLAG_HIDDEN_ITEM_ROUTE17_MAX_ELIXIR                                0
#define FLAG_HIDDEN_ITEM_SAFARI_ZONE_CENTER_LEAF_STONE                     0
#define FLAG_HIDDEN_ITEM_SAFARI_ZONE_WEST_REVIVE                           0
#define FLAG_HIDDEN_ITEM_SILPH_CO_5F_ELIXIR                                0
#define FLAG_HIDDEN_ITEM_SILPH_CO_9F_MAX_POTION                            0
#define FLAG_HIDDEN_ITEM_SAFFRON_CITY_COPYCATS_HOUSE_2F_NUGGET             0
#define FLAG_HIDDEN_ITEM_POWER_PLANT_MAX_ELIXIR                            0
#define FLAG_HIDDEN_ITEM_POWER_PLANT_THUNDER_STONE                         0
#define FLAG_HIDDEN_ITEM_SEAFOAM_ISLANDS_B3F_NUGGET                        0
#define FLAG_HIDDEN_ITEM_SEAFOAM_ISLANDS_B4F_WATER_STONE                   0
#define FLAG_HIDDEN_ITEM_POKEMON_MANSION_1F_MOON_STONE                     0
#define FLAG_HIDDEN_ITEM_POKEMON_MANSION_3F_RARE_CANDY                     0
#define FLAG_HIDDEN_ITEM_POKEMON_MANSION_B1F_ELIXIR                        0
#define FLAG_HIDDEN_ITEM_ROUTE23_FULL_RESTORE                              0
#define FLAG_HIDDEN_ITEM_ROUTE23_ULTRA_BALL                                0
#define FLAG_HIDDEN_ITEM_ROUTE23_MAX_ETHER                                 0
#define FLAG_HIDDEN_ITEM_VICTORY_ROAD_1F_FULL_RESTORE                      0
#define FLAG_HIDDEN_ITEM_CERULEAN_CAVE_1F_ULTRA_BALL                       0
#define FLAG_HIDDEN_ITEM_UNUSED_0x28                                       0
#define FLAG_HIDDEN_ITEM_ROUTE11_ESCAPE_ROPE                               0
#define FLAG_HIDDEN_ITEM_ROUTE12_HYPER_POTION                              0
#define FLAG_HIDDEN_ITEM_UNUSED_0x2B                                       0
#define FLAG_HIDDEN_ITEM_UNUSED_0x2C                                       0
#define FLAG_HIDDEN_ITEM_UNUSED_0x2D                                       0
#define FLAG_HIDDEN_ITEM_UNUSED_0x2E                                       0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_PP_UP                                0
#define FLAG_HIDDEN_ITEM_VERMILION_CITY_MAX_ETHER                          0
#define FLAG_HIDDEN_ITEM_CERULEAN_CITY_RARE_CANDY                          0
#define FLAG_HIDDEN_ITEM_ROUTE4_GREAT_BALL                                 0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS                    0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_2                  0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_3                  0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_4                  0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_5                  0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_6                  0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_7                  0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_8                  0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_9                  0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_10                 0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_11                 0
#define FLAG_HIDDEN_ITEM_CELADON_CITY_GAME_CORNER_COINS_12                 0
#define FLAG_HIDDEN_ITEM_SEVEN_ISLAND_SEVAULT_CANYON_CHERI_BERRY           0
#define FLAG_HIDDEN_ITEM_SEVEN_ISLAND_TANOBY_RUINS_HEART_SCALE_4           0
#define FLAG_HIDDEN_ITEM_SEVEN_ISLAND_TANOBY_RUINS_HEART_SCALE             0
#define FLAG_HIDDEN_ITEM_SEVEN_ISLAND_TANOBY_RUINS_HEART_SCALE_2           0
#define FLAG_HIDDEN_ITEM_SEVEN_ISLAND_TANOBY_RUINS_HEART_SCALE_3           0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_ROCKET_WAREHOUSE_NEST_BALL            0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_ROCKET_WAREHOUSE_NET_BALL             0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL_POTION        0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL_ANTIDOTE      0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL_PARALYZE_HEAL 0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL_AWAKENING     0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL_BURN_HEAL     0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL_ICE_HEAL      0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL_ETHER         0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_EAST_WEST_TUNNEL_POTION          0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_EAST_WEST_TUNNEL_ANTIDOTE        0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_EAST_WEST_TUNNEL_PARALYZE_HEAL   0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_EAST_WEST_TUNNEL_AWAKENING       0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_EAST_WEST_TUNNEL_BURN_HEAL       0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_EAST_WEST_TUNNEL_ICE_HEAL        0
#define FLAG_HIDDEN_ITEM_UNDERGROUND_PATH_EAST_WEST_TUNNEL_ETHER           0
#define FLAG_HIDDEN_ITEM_MT_MOON_B1F_TINY_MUSHROOM                         0
#define FLAG_HIDDEN_ITEM_MT_MOON_B1F_TINY_MUSHROOM_2                       0
#define FLAG_HIDDEN_ITEM_MT_MOON_B1F_TINY_MUSHROOM_3                       0
#define FLAG_HIDDEN_ITEM_MT_MOON_B1F_BIG_MUSHROOM                          0
#define FLAG_HIDDEN_ITEM_MT_MOON_B1F_BIG_MUSHROOM_2                        0
#define FLAG_HIDDEN_ITEM_MT_MOON_B1F_BIG_MUSHROOM_3                        0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_RAZZ_BERRY              0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_BLUK_BERRY              0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_NANAB_BERRY             0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_WEPEAR_BERRY            0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_ORAN_BERRY              0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_CHERI_BERRY             0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_CHESTO_BERRY            0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_PECHA_BERRY             0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_RAWST_BERRY             0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_ASPEAR_BERRY            0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_PERSIM_BERRY            0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_PINAP_BERRY             0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BERRY_FOREST_LUM_BERRY               0
#define FLAG_HIDDEN_ITEM_ONE_ISLAND_TREASURE_BEACH_STARDUST                0
#define FLAG_HIDDEN_ITEM_ONE_ISLAND_TREASURE_BEACH_STARDUST_2              0
#define FLAG_HIDDEN_ITEM_ONE_ISLAND_TREASURE_BEACH_PEARL                   0
#define FLAG_HIDDEN_ITEM_ONE_ISLAND_TREASURE_BEACH_PEARL_2                 0
#define FLAG_HIDDEN_ITEM_ONE_ISLAND_TREASURE_BEACH_ULTRA_BALL              0
#define FLAG_HIDDEN_ITEM_ONE_ISLAND_TREASURE_BEACH_ULTRA_BALL_2            0
#define FLAG_HIDDEN_ITEM_ONE_ISLAND_TREASURE_BEACH_STAR_PIECE              0
#define FLAG_HIDDEN_ITEM_ONE_ISLAND_TREASURE_BEACH_BIG_PEARL               0
#define FLAG_HIDDEN_ITEM_TWO_ISLAND_CAPE_BRINK_RARE_CANDY                  0
#define FLAG_HIDDEN_ITEM_PEWTER_CITY_POKE_BALL                             0
#define FLAG_HIDDEN_ITEM_ROUTE3_ORAN_BERRY                                 0
#define FLAG_HIDDEN_ITEM_ROUTE4_PERSIM_BERRY                               0
#define FLAG_HIDDEN_ITEM_ROUTE24_PECHA_BERRY                               0
#define FLAG_HIDDEN_ITEM_ROUTE25_ORAN_BERRY                                0
#define FLAG_HIDDEN_ITEM_ROUTE25_BLUK_BERRY                                0
#define FLAG_HIDDEN_ITEM_ROUTE6_SITRUS_BERRY                               0
#define FLAG_HIDDEN_ITEM_ROUTE6_RARE_CANDY                                 0
#define FLAG_HIDDEN_ITEM_SSANNE_KITCHEN_PECHA_BERRY                        0
#define FLAG_HIDDEN_ITEM_SSANNE_KITCHEN_CHERI_BERRY                        0
#define FLAG_HIDDEN_ITEM_SSANNE_KITCHEN_CHESTO_BERRY                       0
#define FLAG_HIDDEN_ITEM_ROUTE9_RARE_CANDY                                 0
#define FLAG_HIDDEN_ITEM_UNUSED_0x7C                                       0
#define FLAG_HIDDEN_ITEM_ROUTE10_PERSIM_BERRY                              0
#define FLAG_HIDDEN_ITEM_ROUTE10_CHERI_BERRY                               0
#define FLAG_HIDDEN_ITEM_ROUTE8_RAWST_BERRY                                0
#define FLAG_HIDDEN_ITEM_ROUTE8_LUM_BERRY                                  0
#define FLAG_HIDDEN_ITEM_ROUTE8_LEPPA_BERRY                                0
#define FLAG_HIDDEN_ITEM_ROUTE12_RARE_CANDY                                0
#define FLAG_HIDDEN_ITEM_ROUTE12_LEFTOVERS                                 0
#define FLAG_HIDDEN_ITEM_ROUTE16_LEFTOVERS                                 0
#define FLAG_HIDDEN_ITEM_FUCHSIA_CITY_MAX_REVIVE                           0
#define FLAG_HIDDEN_ITEM_ROCKET_HIDEOUT_B4F_NET_BALL                       0
#define FLAG_HIDDEN_ITEM_SILPH_CO_2F_ULTRA_BALL                            0
#define FLAG_HIDDEN_ITEM_SILPH_CO_3F_PROTEIN                               0
#define FLAG_HIDDEN_ITEM_SILPH_CO_4F_IRON                                  0
#define FLAG_HIDDEN_ITEM_SILPH_CO_5F_PP_UP                                 0
#define FLAG_HIDDEN_ITEM_SILPH_CO_6F_CARBOS                                0
#define FLAG_HIDDEN_ITEM_SILPH_CO_7F_ZINC                                  0
#define FLAG_HIDDEN_ITEM_SILPH_CO_8F_NUGGET                                0
#define FLAG_HIDDEN_ITEM_SILPH_CO_9F_CALCIUM                               0
#define FLAG_HIDDEN_ITEM_SILPH_CO_10F_HP_UP                                0
#define FLAG_HIDDEN_ITEM_SILPH_CO_11F_REVIVE                               0
#define FLAG_HIDDEN_ITEM_ROUTE23_LUM_BERRY                                 0
#define FLAG_HIDDEN_ITEM_ROUTE23_SITRUS_BERRY                              0
#define FLAG_HIDDEN_ITEM_ROUTE23_ASPEAR_BERRY                              0
#define FLAG_HIDDEN_ITEM_ROUTE23_LEPPA_BERRY                               0
#define FLAG_HIDDEN_ITEM_ROUTE14_ZINC                                      0
#define FLAG_HIDDEN_ITEM_ROUTE9_CHESTO_BERRY                               0
#define FLAG_HIDDEN_ITEM_ROUTE10_NANAB_BERRY                               0
#define FLAG_HIDDEN_ITEM_ROUTE7_WEPEAR_BERRY                               0
#define FLAG_HIDDEN_ITEM_ROUTE20_STARDUST                                  0
#define FLAG_HIDDEN_ITEM_ROUTE21_NORTH_PEARL                               0
#define FLAG_HIDDEN_ITEM_ROUTE23_MAX_ELIXIR                                0
#define FLAG_HIDDEN_ITEM_ROUTE4_RAZZ_BERRY                                 0
#define FLAG_HIDDEN_ITEM_ROUTE14_PINAP_BERRY                               0
#define FLAG_HIDDEN_ITEM_MT_EMBER_EXTERIOR_FIRE_STONE                      0
#define FLAG_HIDDEN_ITEM_POKEMON_TOWER_7F_SOOTHE_BELL                      0
#define FLAG_HIDDEN_ITEM_NAVEL_ROCK_SUMMIT_SACRED_ASH                      0
#define FLAG_HIDDEN_ITEM_TWO_ISLAND_CAPE_BRINK_PP_MAX                      0
#define FLAG_HIDDEN_ITEM_MT_EMBER_EXTERIOR_ULTRA_BALL                      0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_DUNSPARCE_TUNNEL_NUGGET              0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_PP_UP                                0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BOND_BRIDGE_MAX_REPEL                0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BOND_BRIDGE_PEARL                    0
#define FLAG_HIDDEN_ITEM_THREE_ISLAND_BOND_BRIDGE_STARDUST                 0
#define FLAG_HIDDEN_ITEM_FOUR_ISLAND_PEARL                                 0
#define FLAG_HIDDEN_ITEM_FOUR_ISLAND_ULTRA_BALL                            0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_MEMORIAL_PILLAR_BIG_PEARL             0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_MEMORIAL_PILLAR_RAZZ_BERRY            0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_MEMORIAL_PILLAR_SITRUS_BERRY          0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_MEMORIAL_PILLAR_BLUK_BERRY            0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_RESORT_GORGEOUS_NEST_BALL             0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_RESORT_GORGEOUS_STARDUST              0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_RESORT_GORGEOUS_STAR_PIECE            0
#define FLAG_HIDDEN_ITEM_FIVE_ISLAND_RESORT_GORGEOUS_STARDUST_2            0
#define FLAG_HIDDEN_ITEM_SIX_ISLAND_OUTCAST_ISLAND_STAR_PIECE              0
#define FLAG_HIDDEN_ITEM_SIX_ISLAND_OUTCAST_ISLAND_NET_BALL                0
#define FLAG_HIDDEN_ITEM_SIX_ISLAND_GREEN_PATH_ULTRA_BALL                  0
#define FLAG_HIDDEN_ITEM_SIX_ISLAND_WATER_PATH_ASPEAR_BERRY                0
#define FLAG_HIDDEN_ITEM_SIX_ISLAND_WATER_PATH_ORAN_BERRY                  0
#define FLAG_HIDDEN_ITEM_SIX_ISLAND_WATER_PATH_PINAP_BERRY                 0
#define FLAG_HIDDEN_ITEM_SIX_ISLAND_LEPPA_BERRY                            0
#define FLAG_HIDDEN_ITEM_SEVEN_ISLAND_TRAINER_TOWER_BIG_PEARL              0
#define FLAG_HIDDEN_ITEM_SEVEN_ISLAND_TRAINER_TOWER_PEARL                  0
#define FLAG_HIDDEN_ITEM_SEVEN_ISLAND_TRAINER_TOWER_NANAB_BERRY            0
#define FLAG_HIDDEN_ITEM_SEVEN_ISLAND_SEVAULT_CANYON_ENTRANCE_RAWST_BERRY  0
#define FLAG_HIDDEN_ITEM_VIRIDIAN_CITY_GYM_MACHO_BRACE                     0
#define FLAG_HIDDEN_ITEM_SSANNE_EXTERIOR_LAVA_COOKIE                       0

#define FLAG_DEFEATED_BROCK           0
#define FLAG_DEFEATED_MISTY           0
#define FLAG_DEFEATED_LT_SURGE        0
#define FLAG_DEFEATED_ERIKA           0
#define FLAG_DEFEATED_KOGA            0
#define FLAG_DEFEATED_SABRINA         0
#define FLAG_DEFEATED_BLAINE          0
#define FLAG_DEFEATED_LEADER_GIOVANNI 0
#define FLAG_DEFEATED_LORELEI         0
#define FLAG_DEFEATED_BRUNO           0
#define FLAG_DEFEATED_AGATHA          0
#define FLAG_DEFEATED_LANCE           0
#define FLAG_DEFEATED_CHAMP           0

#define FLAG_0x82A                                                  0
#define FLAG_0x82B                                                  0
#define FLAG_SYS_SET_TRAINER_CARD_PROFILE                           0
#define FLAG_0x82E                                                  0
#define FLAG_SYS_ON_CYCLING_ROAD                                    0
#define FLAG_0x831                                                  0
#define FLAG_0x832                                                  0
#define FLAG_0x833                                                  0
#define FLAG_0x835                                                  0
#define FLAG_0x836                                                  0
#define FLAG_0x838                                                  0 // Set, never read
#define FLAG_0x83A                                                  0
#define FLAG_SYS_SAW_HELP_SYSTEM_INTRO                              0
#define FLAG_0x83D                                                  0
#define FLAG_OPENED_START_MENU                                      0
#define FLAG_SYS_PC_STORAGE_DISABLED                                0
#define FLAG_SYS_SEVII_MAP_123                                      0
#define FLAG_SYS_SEVII_MAP_4567                                     0
#define FLAG_SYS_GOT_BERRY_POUCH                                    0
#define FLAG_SYS_UNLOCKED_TANOBY_RUINS                              0

// World Map Flags
#define FLAG_WORLD_MAP_PALLET_TOWN                                  0
#define FLAG_WORLD_MAP_VIRIDIAN_CITY                                0
#define FLAG_WORLD_MAP_PEWTER_CITY                                  0
#define FLAG_WORLD_MAP_CERULEAN_CITY                                0
#define FLAG_WORLD_MAP_LAVENDER_TOWN                                0
#define FLAG_WORLD_MAP_VERMILION_CITY                               0
#define FLAG_WORLD_MAP_CELADON_CITY                                 0
#define FLAG_WORLD_MAP_FUCHSIA_CITY                                 0
#define FLAG_WORLD_MAP_CINNABAR_ISLAND                              0
#define FLAG_WORLD_MAP_INDIGO_PLATEAU_EXTERIOR                      0
#define FLAG_WORLD_MAP_SAFFRON_CITY                                 0
#define FLAG_WORLD_MAP_ONE_ISLAND                                   0
#define FLAG_WORLD_MAP_TWO_ISLAND                                   0
#define FLAG_WORLD_MAP_THREE_ISLAND                                 0
#define FLAG_WORLD_MAP_FOUR_ISLAND                                  0
#define FLAG_WORLD_MAP_FIVE_ISLAND                                  0
#define FLAG_WORLD_MAP_SEVEN_ISLAND                                 0
#define FLAG_WORLD_MAP_SIX_ISLAND                                   0
#define FLAG_WORLD_MAP_ROUTE4_POKEMON_CENTER_1F                     0
#define FLAG_WORLD_MAP_ROUTE10_POKEMON_CENTER_1F                    0
#define FLAG_WORLD_MAP_VIRIDIAN_FOREST                              0
#define FLAG_WORLD_MAP_MT_MOON_1F                                   0
#define FLAG_WORLD_MAP_SSANNE_EXTERIOR                              0
#define FLAG_WORLD_MAP_UNDERGROUND_PATH_NORTH_SOUTH_TUNNEL          0
#define FLAG_WORLD_MAP_UNDERGROUND_PATH_EAST_WEST_TUNNEL            0
#define FLAG_WORLD_MAP_DIGLETTS_CAVE_B1F                            0
#define FLAG_WORLD_MAP_VICTORY_ROAD_1F                              0
#define FLAG_WORLD_MAP_ROCKET_HIDEOUT_B1F                           0
#define FLAG_WORLD_MAP_SILPH_CO_1F                                  0
#define FLAG_WORLD_MAP_POKEMON_MANSION_1F                           0
#define FLAG_WORLD_MAP_SAFARI_ZONE_CENTER                           0
#define FLAG_WORLD_MAP_POKEMON_LEAGUE_LORELEIS_ROOM                 0
#define FLAG_WORLD_MAP_ROCK_TUNNEL_1F                               0
#define FLAG_WORLD_MAP_SEAFOAM_ISLANDS_1F                           0
#define FLAG_WORLD_MAP_POKEMON_TOWER_1F                             0
#define FLAG_WORLD_MAP_CERULEAN_CAVE_1F                             0
#define FLAG_WORLD_MAP_POWER_PLANT                                  0
#define FLAG_WORLD_MAP_NAVEL_ROCK_EXTERIOR                          0
#define FLAG_WORLD_MAP_MT_EMBER_EXTERIOR                            0
#define FLAG_WORLD_MAP_THREE_ISLAND_BERRY_FOREST                    0
#define FLAG_WORLD_MAP_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE            0
#define FLAG_WORLD_MAP_FIVE_ISLAND_ROCKET_WAREHOUSE                 0
#define FLAG_WORLD_MAP_TRAINER_TOWER_LOBBY                          0
#define FLAG_WORLD_MAP_SIX_ISLAND_DOTTED_HOLE_1F                    0
#define FLAG_WORLD_MAP_FIVE_ISLAND_LOST_CAVE_ENTRANCE               0
#define FLAG_WORLD_MAP_SIX_ISLAND_PATTERN_BUSH                      0
#define FLAG_WORLD_MAP_SIX_ISLAND_ALTERING_CAVE                     0
#define FLAG_WORLD_MAP_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER     0
#define FLAG_WORLD_MAP_THREE_ISLAND_DUNSPARCE_TUNNEL                0
#define FLAG_WORLD_MAP_SEVEN_ISLAND_SEVAULT_CANYON_TANOBY_KEY       0
#define FLAG_WORLD_MAP_BIRTH_ISLAND_EXTERIOR                        0

#endif

#if TESTING
#define TESTING_FLAGS_START                     0x5000
#define TESTING_FLAG_SLEEP_CLAUSE               (TESTING_FLAGS_START + 0x0)
#define TESTING_FLAG_INVERSE_BATTLE             (TESTING_FLAGS_START + 0x1)
#define TESTING_FLAG_TRAINER_SLIDES             (TESTING_FLAGS_START + 0x2)
#define TESTING_FLAG_UNUSED_3                   (TESTING_FLAGS_START + 0x3)
#define TESTING_FLAG_UNUSED_4                   (TESTING_FLAGS_START + 0x4)
#define TESTING_FLAG_UNUSED_5                   (TESTING_FLAGS_START + 0x5)
#define TESTING_FLAG_UNUSED_6                   (TESTING_FLAGS_START + 0x6)
#define TESTING_FLAG_UNUSED_7                   (TESTING_FLAGS_START + 0x7)
#endif // TESTING

// Ichor: story flags read before their owners claim them (ICHOR_STUB_STORY_FLAGS).
#include "constants/ichor_flag_stubs.h"

#endif // GUARD_CONSTANTS_FLAGS_H
