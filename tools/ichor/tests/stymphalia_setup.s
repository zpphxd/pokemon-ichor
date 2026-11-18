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

@ The state III-5J leaves (design/phase4/SCRIPT.md): seven Laurels, the relics so far,
@ Rhea, Kleon and Alethea gone over Taygetos, and the player on Lakonia's north road.
    test_header Stymphalia_SetupHeader, Stymphalia_Setup
Stymphalia_Setup:
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
    setflag FLAG_BADGE06_GET
    setflag FLAG_BADGE07_GET
    setflag FLAG_ICHOR_VISITED_LAKONIA
    setflag FLAG_ICHOR_LAKONIA_ARRIVED
    setflag FLAG_ICHOR_RHEA_UNMASKED
    setflag FLAG_ICHOR_IAPETOS_LAKONIA_DONE
    setflag FLAG_ICHOR_KLEON_LAKONIA_DONE
    setflag FLAG_ICHOR_LAKONIA_PARTED
    setflag FLAG_ICHOR_HIDE_RHEA_LAKONIA
    setflag FLAG_ICHOR_HIDE_KLEON_LAKONIA
    setflag FLAG_ICHOR_HIDE_ALETHEA_LAKONIA
    setvar VAR_ICHOR_ACT3, 10
    giveitem ITEM_HECATES_TORCH
    giveitem ITEM_DEMETERS_SICKLE
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_LAKONIA, 25, 6
    waitstate
    releaseall
    end

    test_header Stymphalia_SaveHeader, Stymphalia_SaveScript
Stymphalia_SaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end

@ The test party's PP, topped up between long fights (the road's own rests heal too)
    test_header Stymphalia_HealHeader, Stymphalia_HealScript
Stymphalia_HealScript:
    lockall
    setvar VAR_TEMP_F, 1
    special HealPlayerParty
    releaseall
    end
