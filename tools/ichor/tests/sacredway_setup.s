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

@ After the Moon Laurel (Laurel 5): Eleusa's east watch has stood aside, and the
@ player holds the Hammer, the Torch, the Sickle, the Girdle and Pan's Crook.
    test_header SacredWay_SetupHeader, SacredWay_Setup
SacredWay_Setup:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_METAGROSS, 5, move1=MOVE_IRON_HEAD, move2=MOVE_ZEN_HEADBUTT, move3=MOVE_EARTHQUAKE, move4=MOVE_BULLET_PUNCH
    givemon SPECIES_METAGROSS, 5, move1=MOVE_IRON_HEAD, move2=MOVE_ZEN_HEADBUTT, move3=MOVE_EARTHQUAKE, move4=MOVE_BULLET_PUNCH
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_ICHOR_SAFFRON_THREAD
    setflag FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA
    setflag FLAG_ICHOR_ACT1_COMPLETE
    setflag FLAG_ICHOR_LEFT_ELEUSA_WITH_ALETHEA
    setflag FLAG_ICHOR_KLEON_WON_HERALD
    setflag FLAG_ICHOR_KLEON_BATTLE_2_DONE
    additem ITEM_BRONZE_HAMMER, 1
    additem ITEM_HECATES_TORCH, 1
    additem ITEM_DEMETERS_SICKLE, 1
    additem ITEM_GIRDLE_OF_HERAKLES, 1
    additem ITEM_PANS_CROOK, 1
    setflag FLAG_ICHOR_GOT_BRONZE_HAMMER
    setflag FLAG_ICHOR_GOT_HECATES_TORCH
    setflag FLAG_ICHOR_GOT_DEMETERS_SICKLE
    setflag FLAG_ICHOR_GOT_GIRDLE_OF_HERAKLES
    setflag FLAG_ICHOR_GOT_PANS_CROOK
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_ELEUSA_VILLAGE, 46, 26
    waitstate
    releaseall
    end

    test_header SacredWay_SaveHeader, SacredWay_SaveScript
SacredWay_SaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end

    test_header SacredWay_HealHeader, SacredWay_HealScript
SacredWay_HealScript:
    lockall
    setvar VAR_TEMP_F, 1
    special HealPlayerParty
    setvar VAR_REPEL_STEP_COUNT, 999
    releaseall
    end
