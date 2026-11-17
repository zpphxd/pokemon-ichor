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

    test_header Kythera_SetupHeader, Kythera_Setup
Kythera_Setup:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_METAGROSS, 5, move1=MOVE_IRON_HEAD
    givemon SPECIES_METAGROSS, 5, move1=MOVE_IRON_HEAD
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_BADGE06_GET
    setflag FLAG_ICHOR_CROSSING_DONE
    setflag FLAG_ICHOR_AKROPOLIS_RECOVERED
    setflag FLAG_ICHOR_KALDERA_FRAGMENT_LOST
    setflag FLAG_ICHOR_MOM_MISSING
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_KALDERA, 25, 30
    waitstate
    releaseall
    end

    test_header Kythera_SaveHeader, Kythera_Save
Kythera_Save:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end
