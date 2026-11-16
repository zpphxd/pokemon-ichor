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

    test_header Approach_SetupHeader, Approach_SetupScript
Approach_SetupScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KYNDER, 100, move1=MOVE_FLAMETHROWER, move2=MOVE_LEER
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE08_GET
    setflag FLAG_ICHOR_ACT1_COMPLETE
    setflag FLAG_ICHOR_DIONYSIA_BROKEN
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_THYRSA_CITY, 4, 19
    waitstate
    releaseall
    end

    test_header Approach_GirdleHeader, Approach_GirdleScript
Approach_GirdleScript:
    setvar VAR_TEMP_F, 1
    additem ITEM_GIRDLE_OF_HERAKLES
    end

    test_header Approach_SaveHeader, Approach_SaveScript
Approach_SaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end
