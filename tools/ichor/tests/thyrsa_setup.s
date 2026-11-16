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

    test_header Thyrsa_SetupHeader, Thyrsa_SetupScript
Thyrsa_SetupScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KYNDER, 100, move1=MOVE_FLAMETHROWER, move2=MOVE_LEER
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE08_GET
    setflag FLAG_ICHOR_ACT1_COMPLETE
    setflag FLAG_ICHOR_ARRIVED_ELEUSA
    setflag FLAG_ICHOR_SAFFRON_THREAD
    setflag FLAG_ICHOR_GOT_DEMETERS_SICKLE
    setflag FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA
    setflag FLAG_ICHOR_HIDE_KLEON_ELEUSA
    additem ITEM_DEMETERS_SICKLE
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_ELEUSA_VILLAGE, 45, 7
    waitstate
    releaseall
    end

    test_header Thyrsa_SaveHeader, Thyrsa_SaveScript
Thyrsa_SaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end
