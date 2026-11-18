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

@ The player as they come down the Grand Staircase (LABYRINTH.md scene B): two
@ strong Pokémon, Hecate's Torch, Ariadne's Thread, the laurels so far.
    test_header Lab_SetupHeader, Lab_Setup
Lab_Setup:
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
    setflag FLAG_BADGE07_GET
    additem ITEM_HECATES_TORCH
    additem ITEM_ARIADNES_THREAD
    additem ITEM_POSEIDONS_CONCH
    additem ITEM_BRONZE_HAMMER
    additem ITEM_DEMETERS_SICKLE
    additem ITEM_GIRDLE_OF_HERAKLES
    setvar VAR_REPEL_STEP_COUNT, 999
    setflag FLAG_ICHOR_FIRST_LEAP
    setvar VAR_ICHOR_KNOSSA, 5
    warp MAP_LABYRINTH_RING1, 0
    waitstate
    releaseall
    end

    test_header Lab_TombHeader, Lab_Tomb
Lab_Tomb:
    lockall
    setvar VAR_TEMP_F, 1
    warp MAP_LABYRINTH_MINOS_TOMB, 7, 9
    waitstate
    releaseall
    end
