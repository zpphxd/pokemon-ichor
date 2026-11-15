#ifndef GUARD_CONSTANTS_VARS_H
#define GUARD_CONSTANTS_VARS_H

#include "constants/vars_frlg.h"

#define VARS_START 0x4000

// temporary vars
// The first 0x10 vars are temporary--they are cleared every time a map is loaded.
#define TEMP_VARS_START            0x4000
#define VAR_TEMP_0                 (TEMP_VARS_START + 0x0)
#define VAR_TEMP_1                 (TEMP_VARS_START + 0x1)
#define VAR_TEMP_2                 (TEMP_VARS_START + 0x2)
#define VAR_TEMP_3                 (TEMP_VARS_START + 0x3) // Note: Used when the player checks a TV
#define VAR_TEMP_4                 (TEMP_VARS_START + 0x4)
#define VAR_TEMP_5                 (TEMP_VARS_START + 0x5)
#define VAR_TEMP_6                 (TEMP_VARS_START + 0x6)
#define VAR_TEMP_7                 (TEMP_VARS_START + 0x7)
#define VAR_TEMP_8                 (TEMP_VARS_START + 0x8)
#define VAR_TEMP_9                 (TEMP_VARS_START + 0x9)
#define VAR_TEMP_A                 (TEMP_VARS_START + 0xA)
#define VAR_TEMP_B                 (TEMP_VARS_START + 0xB)
#define VAR_TEMP_C                 (TEMP_VARS_START + 0xC)
#define VAR_TEMP_D                 (TEMP_VARS_START + 0xD)
#define VAR_TEMP_E                 (TEMP_VARS_START + 0xE)
#define VAR_TEMP_F                 (TEMP_VARS_START + 0xF)
#define TEMP_VARS_END              VAR_TEMP_F
#define NUM_TEMP_VARS              (TEMP_VARS_END - TEMP_VARS_START + 1)

// object gfx id vars
// These 0x10 vars are used to dynamically control a map object's sprite.
// For example, the rival's sprite id is dynamically set based on the player's gender.
// See VarGetObjectEventGraphicsId().
#define VAR_OBJ_GFX_ID_0           0x4010
#define VAR_OBJ_GFX_ID_1           0x4011
#define VAR_OBJ_GFX_ID_2           0x4012
#define VAR_OBJ_GFX_ID_3           0x4013
#define VAR_OBJ_GFX_ID_4           0x4014
#define VAR_OBJ_GFX_ID_5           0x4015
#define VAR_OBJ_GFX_ID_6           0x4016
#define VAR_OBJ_GFX_ID_7           0x4017
#define VAR_OBJ_GFX_ID_8           0x4018
#define VAR_OBJ_GFX_ID_9           0x4019
#define VAR_OBJ_GFX_ID_A           0x401A
#define VAR_OBJ_GFX_ID_B           0x401B
#define VAR_OBJ_GFX_ID_C           0x401C
#define VAR_OBJ_GFX_ID_D           0x401D
#define VAR_OBJ_GFX_ID_E           0x401E
#define VAR_OBJ_GFX_ID_F           0x401F

// general purpose vars
#define VAR_UNUSED_0x4020                                0x4020 // Unused Var
#define VAR_REPEL_STEP_COUNT                             0x4021
#define VAR_ICE_STEP_COUNT                               0x4022
#define VAR_STARTER_MON                                  0x4023 // 0=Treecko, 1=Torchic, 2=Mudkip
#define VAR_MIRAGE_RND_H                                 0x4024 // Unused if OW_USE_DAILY_SEED_FOR_VANILLA_VARIABLES is TRUE
#define VAR_MIRAGE_RND_L                                 0x4025 // Unused if OW_USE_DAILY_SEED_FOR_VANILLA_VARIABLES is TRUE
#define VAR_SECRET_BASE_MAP                              0x4026
#define VAR_CYCLING_ROAD_RECORD_COLLISIONS               0x4027
#define VAR_CYCLING_ROAD_RECORD_TIME_L                   0x4028
#define VAR_CYCLING_ROAD_RECORD_TIME_H                   0x4029
#define VAR_FRIENDSHIP_STEP_COUNTER                      0x402A
#define VAR_POISON_STEP_COUNTER                          0x402B
#define VAR_RESET_RTC_ENABLE                             0x402C
#define VAR_ENIGMA_BERRY_AVAILABLE                       0x402D
#define VAR_WONDER_NEWS_STEP_COUNTER                     0x402E

#define VAR_FRONTIER_MANIAC_FACILITY                     0x402F
#define VAR_FRONTIER_GAMBLER_CHALLENGE                   0x4030
#define VAR_FRONTIER_GAMBLER_SET_CHALLENGE               0x4031
#define VAR_FRONTIER_GAMBLER_AMOUNT_BET                  0x4032
#define VAR_FRONTIER_GAMBLER_STATE                       0x4033

#define VAR_DEOXYS_ROCK_STEP_COUNT                       0x4034
#define VAR_DEOXYS_ROCK_LEVEL                            0x4035
#define VAR_PC_BOX_TO_SEND_MON                           0x4036
#define VAR_ABNORMAL_WEATHER_LOCATION                    0x4037
#define VAR_ABNORMAL_WEATHER_STEP_COUNTER                0x4038
#define VAR_SHOULD_END_ABNORMAL_WEATHER                  0x4039
#define VAR_FARAWAY_ISLAND_STEP_COUNTER                  0x403A
#define VAR_REGICE_STEPS_1                               0x403B
#define VAR_REGICE_STEPS_2                               0x403C
#define VAR_REGICE_STEPS_3                               0x403D
#define VAR_ALTERING_CAVE_WILD_SET                       0x403E
#define VAR_DISTRIBUTE_EON_TICKET                        0x403F // This var is read and written, but is always zero. The only way to obtain the Eon Ticket in Emerald is via Record Mixing
#define VAR_DAYS                                         0x4040
#define VAR_FANCLUB_FAN_COUNTER                          0x4041
#define VAR_FANCLUB_LOSE_FAN_TIMER                       0x4042
#define VAR_DEPT_STORE_FLOOR                             0x4043
#define VAR_UNUSED_0x4044                                0x4044 // Unused Var
#define VAR_POKELOT_PRIZE_ITEM                           0x4045
#define VAR_NATIONAL_DEX                                 0x4046
#define VAR_SEEDOT_SIZE_RECORD                           0x4047
#define VAR_ASH_GATHER_COUNT                             0x4048
#define VAR_BIRCH_STATE                                  0x4049
#define VAR_CRUISE_STEP_COUNT                            0x404A
#define VAR_POKELOT_RND1                                 0x404B // Unused if OW_USE_DAILY_SEED_FOR_VANILLA_VARIABLES is TRUE
#define VAR_POKELOT_RND2                                 0x404C // Unused if OW_USE_DAILY_SEED_FOR_VANILLA_VARIABLES is TRUE
#define VAR_UNUSED_0x404D                                0x404D // Unused Var
#define VAR_ICHOR_DEXNAV_SPECIES                         0x404E // Ichor: registered Augur's Eye species
#define VAR_LOTAD_SIZE_RECORD                            0x404F
#define VAR_LITTLEROOT_TOWN_STATE                        0x4050
#define VAR_UNUSED_0x4051                                0x4051 // Unused Var
#define VAR_UNUSED_0x4052                                0x4052 // Unused Var
#define VAR_UNUSED_0x4053                                0x4053 // Unused Var
#define VAR_CURRENT_SECRET_BASE                          0x4054 // was probably allocated for VAR_FALLARBOR_TOWN_STATE at one point
#define VAR_UNUSED_0x4055                                0x4055 // Unused Var
#define VAR_UNUSED_0x4056                                0x4056 // Unused Var
#define VAR_UNUSED_0x4057                                0x4057 // Unused Var
#define VAR_UNUSED_0x4058                                0x4058 // Unused Var
#define VAR_UNUSED_0x4059                                0x4059 // Unused Var
#define VAR_UNUSED_0x405A                                0x405A // Unused Var
#define VAR_UNUSED_0x405B                                0x405B // Unused Var
#define VAR_UNUSED_0x405C                                0x405C // Unused Var
#define VAR_MOSSDEEP_CITY_STATE                          0x405D
#define VAR_SOOTOPOLIS_CITY_STATE                        0x405E
#define VAR_UNUSED_0x405F                                0x405F // Unused Var
#define VAR_ROUTE101_STATE                               0x4060
#define VAR_UNUSED_0x4061                                0x4061 // Unused Var
#define VAR_UNUSED_0x4062                                0x4062 // Unused Var
#define VAR_UNUSED_0x4063                                0x4063 // Unused Var
#define VAR_UNUSED_0x4064                                0x4064 // Unused Var
#define VAR_UNUSED_0x4065                                0x4065 // Unused Var
#define VAR_UNUSED_0x4066                                0x4066 // Unused Var
#define VAR_UNUSED_0x4067                                0x4067 // Unused Var
#define VAR_UNUSED_0x4068                                0x4068 // Unused Var
#define VAR_UNUSED_0x4069                                0x4069 // Unused Var
#define VAR_UNUSED_0x406A                                0x406A // Unused Var
#define VAR_UNUSED_0x406B                                0x406B // Unused Var
#define VAR_UNUSED_0x406C                                0x406C // Unused Var
#define VAR_UNUSED_0x406D                                0x406D // Unused Var
#define VAR_UNUSED_0x406E                                0x406E // Unused Var
#define VAR_ROUTE116_STATE                               0x406F
#define VAR_UNUSED_0x4070                                0x4070 // Unused Var
#define VAR_UNUSED_0x4071                                0x4071 // Unused Var
#define VAR_UNUSED_0x4072                                0x4072 // Unused Var
#define VAR_UNUSED_0x4073                                0x4073 // Unused Var
#define VAR_UNUSED_0x4074                                0x4074 // Unused Var
#define VAR_UNUSED_0x4075                                0x4075 // Unused Var
#define VAR_UNUSED_0x4076                                0x4076 // Unused Var
#define VAR_UNUSED_0x4077                                0x4077 // Unused Var
#define VAR_UNUSED_0x4078                                0x4078 // Unused Var
#define VAR_UNUSED_0x4079                                0x4079 // Unused Var
#define VAR_UNUSED_0x407A                                0x407A // Unused Var
#define VAR_UNUSED_0x407B                                0x407B // Unused Var
#define VAR_UNUSED_0x407C                                0x407C // Unused Var
#define VAR_UNUSED_0x407D                                0x407D // Unused Var
#define VAR_UNUSED_0x407E                                0x407E // Unused Var
#define VAR_UNUSED_0x407F                                0x407F // Unused Var
#define VAR_UNUSED_0x4080                                0x4080 // Unused Var
#define VAR_UNUSED_0x4081                                0x4081 // Unused Var
#define VAR_LITTLEROOT_HOUSES_STATE_MAY                  0x4082
#define VAR_ICHOR_DEXNAV_STEP_COUNTER                    0x4083 // Ichor: Augur's Eye step counter
#define VAR_BIRCH_LAB_STATE                              0x4084
#define VAR_UNUSED_0x4085                                0x4085 // Unused Var
#define VAR_CONTEST_HALL_STATE                           0x4086
#define VAR_CABLE_CLUB_STATE                             0x4087
#define VAR_CONTEST_TYPE                                 0x4088
#define VAR_SECRET_BASE_INITIALIZED                      0x4089
#define VAR_CONTEST_PRIZE_PICKUP                         0x408A
#define VAR_ICHOR_HEARTH_TRIAL                           0x408B // Ichor: Hearth Trial progress (braziers lit)
#define VAR_LITTLEROOT_HOUSES_STATE_BRENDAN              0x408C
#define VAR_LITTLEROOT_RIVAL_STATE                       0x408D
#define VAR_UNUSED_0x408E                                0x408E // Unused Var
#define VAR_UNUSED_0x408F                                0x408F // Unused Var
#define VAR_BRINEY_HOUSE_STATE                           0x4090
#define VAR_UNUSED_0x4091                                0x4091 // Unused Var
#define VAR_LITTLEROOT_INTRO_STATE                       0x4092
#define VAR_UNUSED_0x4093                                0x4093 // Unused Var
#define VAR_UNUSED_0x4094                                0x4094 // Unused Var
#define VAR_LILYCOVE_FAN_CLUB_STATE                      0x4095
#define VAR_BRINEY_LOCATION                              0x4096
#define VAR_INIT_SECRET_BASE                             0x4097
#define VAR_UNUSED_0x4098                                0x4098 // Unused Var
#define VAR_LILYCOVE_CONTEST_LOBBY_STATE                 0x4099
#define VAR_RUSTURF_TUNNEL_STATE                         0x409A
#define VAR_UNUSED_0x409B                                0x409B // Unused Var
#define VAR_ELITE_4_STATE                                0x409C
#define VAR_UNUSED_0x409D                                0x409D // Unused Var
#define VAR_UNUSED_0x409E                                0x409E // Unused Var
#define VAR_UNUSED_0x409F                                0x409F // Unused Var
#define VAR_UNUSED_0x40A0                                0x40A0 // Unused Var
#define VAR_UNUSED_0x40A1                                0x40A1 // Unused var
#define VAR_UNUSED_0x40A2                                0x40A2 // Unused Var
#define VAR_UNUSED_0x40A3                                0x40A3 // Unused Var
#define VAR_SAFARI_ZONE_STATE                            0x40A4  // 0: In or out of SZ, 1: Player exiting SZ, 2: Player entering SZ
#define VAR_UNUSED_0x40A5                                0x40A5 // Unused Var
#define VAR_UNUSED_0x40A6                                0x40A6 // Unused Var
#define VAR_UNUSED_0x40A7                                0x40A7 // Unused Var
#define VAR_UNUSED_0x40A8                                0x40A8 // Unused Var
#define VAR_CYCLING_CHALLENGE_STATE                      0x40A9
#define VAR_UNUSED_0x40AA                                0x40AA // Unused Var
#define VAR_UNUSED_0x40AB                                0x40AB // Unused Var
#define VAR_UNUSED_0x40AC                                0x40AC // Unused Var
#define VAR_UNUSED_0x40AD                                0x40AD // Unused Var
#define VAR_UNUSED_0x40AE                                0x40AE // Unused Var
#define VAR_UNUSED_0x40AF                                0x40AF // Unused Var
#define VAR_UNUSED_0x40B0                                0x40B0 // Unused Var
#define VAR_UNUSED_0x40B1                                0x40B1 // Unused Var
#define VAR_UNUSED_0x40B2                                0x40B2 // Unused Var
#define VAR_WEATHER_INSTITUTE_STATE                      0x40B3
#define VAR_SS_TIDAL_STATE                               0x40B4
#define VAR_UNUSED_0x40B5                                0x40B5 // Unused Var
#define VAR_UNUSED_0x40B6                                0x40B6 // Unused Var
#define VAR_UNUSED_0x40B7                                0x40B7 // Unused Var
#define VAR_UNUSED_0x40B8                                0x40B8 // Unused Var
#define VAR_UNUSED_0x40B9                                0x40B9 // Unused Var
#define VAR_UNUSED_0x40BA                                0x40BA // Unused Var
#define VAR_UNUSED_0x40BB                                0x40BB // Unused Var
#define VAR_BRAVO_TRAINER_BATTLE_TOWER_ON                0x40BC
#define VAR_UNUSED_0x40BD                                0x40BD // Unused Var
#define VAR_UNUSED_0x40BE                                0x40BE // Unused Var
#define VAR_UNUSED_0x40BF                                0x40BF // Unused Var
#define VAR_UNUSED_0x40C0                                0x40C0 // Unused Var
#define VAR_UNUSED_0x40C1                                0x40C1 // Unused Var
#define VAR_PACIFIDLOG_TM_RECEIVED_DAY                   0x40C2
#define VAR_UNUSED_0x40C3                                0x40C3 // Unused Var
#define VAR_UNUSED_0x40C4                                0x40C4 // Unused Var
#define VAR_UNUSED_0x40C5                                0x40C5 // Unused Var
#define VAR_UNUSED_0x40C6                                0x40C6 // Unused Var
#define VAR_UNUSED_0x40C7                                0x40C7 // Unused Var
#define VAR_UNUSED_0x40C8                                0x40C8 // Unused Var
#define VAR_UNUSED_0x40C9                                0x40C9 // Unused Var
#define VAR_SKY_PILLAR_STATE                             0x40CA
#define VAR_MIRAGE_TOWER_STATE                           0x40CB
#define VAR_UNUSED_0x40CC                                0x40CC // Unused Var
#define VAR_CABLE_CLUB_TUTORIAL_STATE                    0x40CD
#define VAR_FRONTIER_BATTLE_MODE                         0x40CE
#define VAR_FRONTIER_FACILITY                            0x40CF
#define VAR_HAS_ENTERED_BATTLE_FRONTIER                  0x40D0 // Var is used like a flag.
#define VAR_SCOTT_STATE                                  0x40D1
#define VAR_UNUSED_0x40D2                                0x40D2 // Unused Var
#define VAR_UNUSED_0x40D3                                0x40D3 // Unused Var
#define VAR_UNUSED_0x40D4                                0x40D4 // Unused Var
#define VAR_ROAMER_POKEMON                               0x40D5 // 0 = Latias, 1 = Latios
#define VAR_TRAINER_HILL_IS_ACTIVE                       0x40D6
#define VAR_UNUSED_0x40D7                                0x40D7 // Unused Var
#define VAR_UNUSED_0x40D8                                0x40D8 // Unused Var
#define VAR_UNUSED_0x40D9                                0x40D9 // Unused Var
#define VAR_UNUSED_0x40DA                                0x40DA // Unused Var
#define VAR_UNUSED_0x40DB                                0x40DB // Unused Var
#define VAR_UNUSED_0x40DC                                0x40DC // Unused Var
#define VAR_GIFT_PICHU_SLOT                              0x40DD
#define VAR_GIFT_UNUSED_1                                0x40DE // Var is written to, but never read
#define VAR_GIFT_UNUSED_2                                0x40DF // Var is written to, but never read
#define VAR_GIFT_UNUSED_3                                0x40E0 // Var is written to, but never read
#define VAR_GIFT_UNUSED_4                                0x40E1 // Var is written to, but never read
#define VAR_GIFT_UNUSED_5                                0x40E2 // Var is written to, but never read
#define VAR_GIFT_UNUSED_6                                0x40E3 // Var is written to, but never read
#define VAR_GIFT_UNUSED_7                                0x40E4 // var is written to, but never read
#define VAR_UNUSED_0x40E5                                0x40E5 // Unused Var
#define VAR_DAILY_SLOTS                                  0x40E6
#define VAR_DAILY_WILDS                                  0x40E7
#define VAR_DAILY_BLENDER                                0x40E8
#define VAR_DAILY_PLANTED_BERRIES                        0x40E9
#define VAR_DAILY_PICKED_BERRIES                         0x40EA
#define VAR_DAILY_ROULETTE                               0x40EB
#define VAR_SECRET_BASE_STEP_COUNTER                     0x40EC // Used by Secret Base TV programs
#define VAR_SECRET_BASE_LAST_ITEM_USED                   0x40ED // Used by Secret Base TV programs
#define VAR_SECRET_BASE_LOW_TV_FLAGS                     0x40EE // Used by Secret Base TV programs
#define VAR_SECRET_BASE_HIGH_TV_FLAGS                    0x40EF // Used by Secret Base TV programs
#define VAR_SECRET_BASE_IS_NOT_LOCAL                     0x40F0 // Set to TRUE while in another player's secret base.
#define VAR_DAILY_BP                                     0x40F1
#define VAR_WALLY_CALL_STEP_COUNTER                      0x40F2
#define VAR_SCOTT_FORTREE_CALL_STEP_COUNTER              0x40F3
#define VAR_ROXANNE_CALL_STEP_COUNTER                    0x40F4
#define VAR_SCOTT_BF_CALL_STEP_COUNTER                   0x40F5
#define VAR_RIVAL_RAYQUAZA_CALL_STEP_COUNTER             0x40F6
#define VAR_UNUSED_0x40F7                                0x40F7 // Unused Var
#define VAR_UNUSED_0x40F8                                0x40F8 // Unused Var
#define VAR_UNUSED_0x40F9                                0x40F9 // Unused Var
#define VAR_UNUSED_0x40FA                                0x40FA // Unused Var
#define VAR_UNUSED_0x40FB                                0x40FB // Unused Var
#define VAR_UNUSED_0x40FC                                0x40FC // Unused Var
#define VAR_UNUSED_0x40FD                                0x40FD // Unused Var
#define VAR_UNUSED_0x40FE                                0x40FE // Unused Var
#define VAR_UNUSED_0x40FF                                0x40FF // Unused Var

#define VARS_END                                         0x40FF
#define VARS_COUNT                                       (VARS_END - VARS_START + 1)

// Ichor var bank. These vars are saved in IchorSave (SaveBlock3): GetVarPointer
// (src/event_data.c) sends ids 0x4100-0x411F there. Scripts use them like any
// var. Claim one by name with
//   python3 tools/ichor/claim.py bankvar VAR_ICHOR_<NAME> "comment"
// See design/ENGINE_API.md.
#define ICHOR_VARS_START                                 0x4100
#define ICHOR_VARS_COUNT                                 32
#define ICHOR_VARS_END                                   (ICHOR_VARS_START + ICHOR_VARS_COUNT - 1)
// Ichor bank vars: claim.py bankvar adds lines here, in order.
#define VAR_ICHOR_OIK_CHART                     (ICHOR_VARS_START + 0x018) // Ichor: Oikoumene chart: bits 0-1 the last port you were in (src/regions.c), bits 2-15 the towns you have been to, for their fly targets
// Ichor bank vars: end

#define SPECIAL_VARS_START            0x8000
// special vars
// They are commonly used as parameters to commands, or return values from commands.
#define VAR_0x8000                    0x8000
#define VAR_0x8001                    0x8001
#define VAR_0x8002                    0x8002
#define VAR_0x8003                    0x8003
#define VAR_0x8004                    0x8004
#define VAR_0x8005                    0x8005
#define VAR_0x8006                    0x8006
#define VAR_0x8007                    0x8007
#define VAR_0x8008                    0x8008
#define VAR_0x8009                    0x8009
#define VAR_0x800A                    0x800A
#define VAR_0x800B                    0x800B
#define VAR_FACING                    0x800C
#define VAR_RESULT                    0x800D
#define VAR_ITEM_ID                   0x800E
#define VAR_LAST_TALKED               0x800F
#define VAR_CONTEST_RANK              0x8010
#define VAR_CONTEST_CATEGORY          0x8011
#define VAR_MON_BOX_ID                0x8012
#define VAR_MON_BOX_POS               0x8013
#define VAR_UNUSED_0x8014             0x8014
#define VAR_TRAINER_BATTLE_OPPONENT_A 0x8015 // Alias of TRAINER_BATTLE_PARAM.opponentA

#define SPECIAL_VARS_END              0x8015

// If an overworld trigger uses this pseudo-variable as the trigger check,
// then the script will be run using RunScriptImmediately instead of in the
// global script context. This means it will run faster, but cannot do any
// cutscenes nor call a wait command. Used for weather effects in vanilla.
#define TRIGGER_RUN_IMMEDIATELY   0

// Temp var aliases
#define VAR_TEMP_CHALLENGE_STATUS  VAR_TEMP_0

#define VAR_TEMP_MIXED_RECORDS         VAR_TEMP_0
#define VAR_TEMP_RECORD_MIX_GIFT_ITEM  VAR_TEMP_1

#define VAR_TEMP_PLAYING_PYRAMID_MUSIC  VAR_TEMP_E

#define VAR_TEMP_FRONTIER_TUTOR_SELECTION  VAR_TEMP_D
#define VAR_TEMP_FRONTIER_TUTOR_ID         VAR_TEMP_E

#define VAR_TEMP_TRANSFERRED_SPECIES  VAR_TEMP_1

#if TESTING
#define TESTING_VARS_START                  0x9000
#define TESTING_VAR_DIFFICULTY              (TESTING_VARS_START + 0x0)
#define TESTING_VAR_TRAINER_SLIDES          (TESTING_VARS_START + 0x1)
#define TESTING_VAR_UNUSED_2                (TESTING_VARS_START + 0x2)
#define TESTING_VAR_UNUSED_3                (TESTING_VARS_START + 0x3)
#define TESTING_VAR_UNUSED_4                (TESTING_VARS_START + 0x4)
#define TESTING_VAR_UNUSED_5                (TESTING_VARS_START + 0x5)
#define TESTING_VAR_UNUSED_6                (TESTING_VARS_START + 0x6)
#define TESTING_VAR_UNUSED_7                (TESTING_VARS_START + 0x7)
#endif // TESTING

#endif // GUARD_CONSTANTS_VARS_H
