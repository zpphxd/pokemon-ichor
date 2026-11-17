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

    test_header Nemea_EarlyHeader, Nemea_EarlyScript
Nemea_EarlyScript:
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
    setflag FLAG_ICHOR_KLEON_WON_HERALD
    setflag FLAG_ICHOR_KLEON_BATTLE_2_DONE
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_EMPORION_CITY, 4, 41
    waitstate
    releaseall
    end

    test_header Nemea_ArkadiaHeader, Nemea_ArkadiaScript
Nemea_ArkadiaScript:
    setvar VAR_TEMP_F, 1
    warp MAP_ARKADIA, 20, 31
    waitstate
    end

    test_header Nemea_MoonHeader, Nemea_MoonScript
Nemea_MoonScript:
    setvar VAR_TEMP_F, 1
    setflag FLAG_BADGE05_GET
    additem ITEM_OLIVE_OIL, 2
    additem ITEM_BRONZE_HAMMER, 1
    additem ITEM_HECATES_TORCH, 1
    end

    test_header Nemea_SaveHeader, Nemea_SaveScript
Nemea_SaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end
