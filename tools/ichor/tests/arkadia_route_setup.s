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
    warp MAP_THYRSA_CITY, 3, 24
    waitstate
    releaseall
    end

    test_header Approach_GirdleHeader, Approach_GirdleScript
Approach_GirdleScript:
    setvar VAR_TEMP_F, 1
    additem ITEM_GIRDLE_OF_HERAKLES
    end

    @ the one Kynder runs out of Flamethrower on the long Kopais road: top it up
    test_header Approach_HealHeader, Approach_HealScript
Approach_HealScript:
    setvar VAR_TEMP_F, 1
    special HealPlayerParty
    end

    test_header Approach_SaveHeader, Approach_SaveScript
Approach_SaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end

    test_header Hunt_SetupHeader, Hunt_SetupScript
Hunt_SetupScript:
    setvar VAR_TEMP_F, 1
    setflag FLAG_ICHOR_DIFFICULTY_CHOSEN
    setvar VAR_ICHOR_DIFFICULTY, 1
    setflag FLAG_ICHOR_KLEON_JOINED_TITANS
    additem ITEM_PRETTY_FEATHER
    warp MAP_ARKADIA, 20, 31
    waitstate
    end

    test_header Hunt_CapHeader, Hunt_CapScript
Hunt_CapScript:
    setvar VAR_TEMP_F, 1
    callnative Hunt_ReadCap
    end
    .align 2
    .thumb
    .thumb_func
Hunt_ReadCap:
    push {lr}
    bl GetCurrentLevelCap
    ldr r1, =gSpecialVar_Result
    strh r0, [r1]
    pop {pc}
    .pool
