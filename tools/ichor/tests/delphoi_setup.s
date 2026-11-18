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

@ The state Lakonia's chapter hands over (SCRIPT.md III-5J): seven Laurels, the
@ relics of Acts I-III, VAR_ICHOR_ACT3 = 10, standing on Kirrha's east road.
    test_header Delphoi_SetupHeader, Delphoi_Setup
Delphoi_Setup:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KYOGRE, 5, move1=MOVE_SURF
    givemon SPECIES_METAGROSS, 5, move1=MOVE_IRON_HEAD
    givemon SPECIES_METAGROSS, 5, move1=MOVE_IRON_HEAD
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_BADGE06_GET
    setflag FLAG_BADGE07_GET
    giveitem ITEM_POSEIDONS_CONCH
    giveitem ITEM_HORN_OF_ACHELOUS
    giveitem ITEM_HECATES_TORCH
    giveitem ITEM_BRONZE_HAMMER
    giveitem ITEM_OLIVE_OIL, 3
    setvar VAR_ICHOR_ACT3, 10
    setvar VAR_REPEL_STEP_COUNT, 9999
    warp MAP_KIRRHA, 25, 10
    waitstate
    releaseall
    end

    test_header Delphoi_SaveHeader, Delphoi_Save
Delphoi_Save:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end

@ The assist between stretches: a full heal (the route's rest points stand in).
    test_header Delphoi_HealHeader, Delphoi_Heal
Delphoi_Heal:
    lockall
    setvar VAR_TEMP_F, 1
    special HealPlayerParty
    releaseall
    end
