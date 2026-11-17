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

@ Kaldera's quay after the Forge Laurel and Kydippe's letter: the state the
@ southern voyage starts from (STORY II-13, II-14). Two level-100 partners,
@ since the bad guests are a double battle.
    test_header KytheraTown_SetupHeader, KytheraTown_SetupScript
KytheraTown_SetupScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_OLYMPANAX, 100, move1=MOVE_SCALD, move2=MOVE_LEER
    givemon SPECIES_PYLAKYON, 100, move1=MOVE_FLARE_BLITZ, move2=MOVE_LEER
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_BADGE06_GET
    setflag FLAG_ICHOR_ACT1_COMPLETE
    setflag FLAG_ICHOR_KLEON_JOINED_TITANS
    setflag FLAG_ICHOR_AKROPOLIS_RECOVERED
    setflag FLAG_ICHOR_ALETHEA_LEFT_ASTYRA
    setflag FLAG_ICHOR_ARRIVED_KALDERA
    setflag FLAG_ICHOR_KALDERA_FRAGMENT_LOST
    setflag FLAG_ICHOR_MOM_MISSING
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_KALDERA, 19, 34
    waitstate
    releaseall
    end

@ The Gallery's statues stand still for the walk to Galatea, as after the
@ Laurel: the statue engine itself is tools/ichor/tests/ichor_statues.sh's.
@ VAR_TEMP_1 = 3 keeps the rooms' triggers from waking them again.
    test_header KytheraTown_FreezeHeader, KytheraTown_FreezeScript
KytheraTown_FreezeScript:
    lockall
    setvar VAR_TEMP_F, 1
    call KytheraTempleOfAphrodite_EventScript_StillAll
    call KytheraTempleOfAphrodite_EventScript_RespawnStatues
    setvar VAR_TEMP_1, 3
    releaseall
    end

@ The assisted team rests between stretches of road (a dozen trainers line
@ the Foam Road; the check is about the maps, not attrition).
    test_header KytheraTown_HealHeader, KytheraTown_HealScript
KytheraTown_HealScript:
    lockall
    setvar VAR_TEMP_F, 1
    special HealPlayerParty
    releaseall
    end
