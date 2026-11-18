#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/moves.h"
#include "constants/pokemon.h"
#include "constants/species.h"
#include "constants/vars.h"
#include "constants/rtc.h"
    .include "asm/macros.inc"
    .include "asm/macros/event.inc"
    .include "constants/constants.inc"
    .text
    .align 2
    .macro test_header name:req, script:req
    .global \name
\name:
    map_script MAP_SCRIPT_ON_FRAME_TABLE, \name\()_Table
    .byte 0
    .align 2
\name\()_Table:
    map_script_2 VAR_TEMP_F, 0, \script
    .2byte 0
    .align 2
    .endm

@ The assisted team: three level-100 sweepers (the climb forces many battles
@ between heals, and a sweeper with one move runs dry), whose first move hits every type
@ (Ice has no immunities; Regice, because a form-changing Kyurem has its stats
@ recalculated after every battle, which undoes the assist), and a status move second.
    test_header Ascent_SetupHeader, Ascent_SetupScript
Ascent_SetupScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_REGICE, 100, ITEM_CHOICE_SPECS, move1=MOVE_FLASH_CANNON, move2=MOVE_ICE_BEAM
    givemon SPECIES_REGICE, 100, ITEM_CHOICE_SPECS, move1=MOVE_FLASH_CANNON, move2=MOVE_ICE_BEAM
    givemon SPECIES_REGICE, 100, ITEM_CHOICE_SPECS, move1=MOVE_FLASH_CANNON, move2=MOVE_ICE_BEAM
    additem ITEM_GIRDLE_OF_HERAKLES, 1
    additem ITEM_BRONZE_HAMMER, 1
    additem ITEM_HECATES_TORCH, 1
    additem ITEM_LABRYS, 1
    additem ITEM_DAEDALUS_WINGS, 1
    additem ITEM_ARIADNES_THREAD, 1
    additem ITEM_HELM_OF_DARKNESS, 1
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_BADGE06_GET
    setflag FLAG_BADGE07_GET
    setflag FLAG_BADGE08_GET
    setflag FLAG_ICHOR_ACT1_COMPLETE
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_ASTYRA, 42, 33
    waitstate
    releaseall
    end

@ Daylight for the review screenshots (Astyra releases any held hour on arrival).
    test_header Ascent_DayHeader, Ascent_DayScript
Ascent_DayScript:
    lockall
    setvar VAR_TEMP_F, 1
    setvar VAR_0x8004, TIME_DAY
    special Ichor_HoldTimeOfDay
    releaseall
    end

    test_header Ascent_SaveHeader, Ascent_SaveScript
Ascent_SaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end
