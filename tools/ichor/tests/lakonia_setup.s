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

@ The state Knossa leaves: seven Laurels, the relics, the sealed tablet, and the
@ Euploia boarded at Amnisos for Gytheion (VAR_ICHOR_ACT3 6, VAR_ICHOR_KNOSSA 20).
    test_header Lakonia_SetupHeader, Lakonia_Setup
Lakonia_Setup:
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
    setflag FLAG_ICHOR_CROSSING_DONE
    setflag FLAG_ICHOR_SAVED_HALCYON_NEST
    setflag FLAG_ICHOR_SAILED_FOR_KNOSSA
    setflag FLAG_ICHOR_DAPHNE_LETTER_KNOSSA
    setflag FLAG_ICHOR_SAILED_FOR_GYTHEION
    setvar VAR_ICHOR_ACT3, 6
    setvar VAR_ICHOR_KNOSSA, 20
    giveitem ITEM_SEALED_TABLET
    giveitem ITEM_HECATES_TORCH
    giveitem ITEM_DEMETERS_SICKLE
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_TRIREME_EUPLOIA_DECK, 13, 5
    waitstate
    releaseall
    end
