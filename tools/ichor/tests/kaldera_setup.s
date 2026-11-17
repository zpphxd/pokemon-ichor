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

    test_header Kaldera_SetupHeader, Kaldera_SetupScript
Kaldera_SetupScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_PLOUTERAS, 5, move1=MOVE_SURF, move2=MOVE_LEER
    additem ITEM_GIRDLE_OF_HERAKLES, 1
    additem ITEM_HECATES_TORCH, 1
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_ICHOR_CROSSING_DONE
    setflag FLAG_ICHOR_SAVED_HALCYON_NEST
    setflag FLAG_ICHOR_ACT1_COMPLETE
    setflag FLAG_ICHOR_TALKED_TO_MOM
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_ASTYRA_HARBOR, 24, 13
    waitstate
    releaseall
    end

    test_header Kaldera_HomeHeader, Kaldera_HomeScript
Kaldera_HomeScript:
    setvar VAR_TEMP_F, 1
    warp MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_1F, 10, 4
    waitstate
    end

    test_header Kaldera_SaveHeader, Kaldera_SaveScript
Kaldera_SaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end
