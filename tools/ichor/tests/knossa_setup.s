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

@ The state Kythera leaves: the Horn won (VAR_ICHOR_ACT3 4), the Euploia kept and
@ its scenes done, so Nausikles offers the crossing to Knossa.
    test_header Knossa_SetupHeader, Knossa_Setup
Knossa_Setup:
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
    setflag FLAG_ICHOR_CROSSING_DONE
    setflag FLAG_ICHOR_AKROPOLIS_RECOVERED
    setflag FLAG_ICHOR_KALDERA_FRAGMENT_LOST
    setflag FLAG_ICHOR_MOM_MISSING
    setflag FLAG_ICHOR_CROSSED_ROUTE22
    setflag FLAG_ICHOR_EUPLOIA_KEPT
    setflag FLAG_ICHOR_ALETHEA_REJOINED
    setflag FLAG_ICHOR_BAD_GUESTS_GONE
    setflag FLAG_ICHOR_HEARD_KRONIST
    setflag FLAG_ICHOR_ALETHEA_SAILED_KNOSSA
    setvar VAR_ICHOR_ACT3, 4
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_KYTHERA_SKANDEIA, 26, 12
    waitstate
    releaseall
    end

@ The Labyrinth chapters' hand-offs, stood in for: out through the threshold at
@ night (VAR_ICHOR_KNOSSA 18) and down the Icarus Shaft at dawn (19).
    test_header Knossa_TurningHeader, Knossa_Turning
Knossa_Turning:
    lockall
    setvar VAR_TEMP_F, 1
    setvar VAR_ICHOR_KNOSSA, 18
    warp MAP_KNOSSA_PALACE, 29, 16
    waitstate
    releaseall
    end

    test_header Knossa_IcarusHeader, Knossa_Icarus
Knossa_Icarus:
    lockall
    setvar VAR_TEMP_F, 1
    setvar VAR_ICHOR_KNOSSA, 19
    warp MAP_KNOSSA_PALACE, 30, 23
    waitstate
    releaseall
    end

@ Evening on Amnisos's quay (beat III-4).
    test_header Knossa_EveningHeader, Knossa_Evening
Knossa_Evening:
    lockall
    setvar VAR_TEMP_F, 1
    setvar VAR_0x8004, TIME_EVENING
    special Ichor_HoldTimeOfDay
    warp MAP_KNOSSA_AMNISOS, 19, 9
    waitstate
    releaseall
    end
