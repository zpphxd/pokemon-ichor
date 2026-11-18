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
#include "constants/opponents.h"
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

@ The assisted team: one level-100 sweeper whose first move hits every type
@ (Ice has no immunities), and a status move second for the deliberate loss.
    test_header League_SetupHeader, League_SetupScript
League_SetupScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KYUREM, 100, ITEM_CHOICE_SPECS, move1=MOVE_ICE_BEAM, move2=MOVE_GROWL
    additem ITEM_GIRDLE_OF_HERAKLES, 1
    additem ITEM_BRONZE_HAMMER, 1
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_BADGE06_GET
    setflag FLAG_BADGE07_GET
    setflag FLAG_BADGE08_GET
    setflag FLAG_ICHOR_ACT1_COMPLETE
    setvar VAR_REPEL_STEP_COUNT, 999
    @ the climb's trainers are tools/ichor/tests/ascent.sh's to fight; here the road is clear
    settrainerflag TRAINER_ICHOR_ASCENT_PHILON
    settrainerflag TRAINER_ICHOR_ASCENT_KLYTOS
    settrainerflag TRAINER_ICHOR_ASCENT_LAMPON
    settrainerflag TRAINER_ICHOR_ASCENT_THEANO
    settrainerflag TRAINER_ICHOR_ASCENT_KALLIAS
    settrainerflag TRAINER_ICHOR_ASCENT_AGATHE
    settrainerflag TRAINER_ICHOR_ASCENT_LYSANDRA
    settrainerflag TRAINER_ICHOR_ASCENT_NIKIAS
    settrainerflag TRAINER_ICHOR_ASCENT_EIRENE
    settrainerflag TRAINER_ICHOR_ASCENT_DEXIOS
    warp MAP_ASTYRA, 42, 33
    waitstate
    releaseall
    end

@ Daylight for the review screenshots (Astyra releases any held hour on arrival).
    test_header League_DayHeader, League_DayScript
League_DayScript:
    lockall
    setvar VAR_TEMP_F, 1
    setvar VAR_0x8004, TIME_DAY
    special Ichor_HoldTimeOfDay
    releaseall
    end

    test_header League_SaveHeader, League_SaveScript
League_SaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end

@ Above the cloud: the climb between the camp and 3F is ascent.sh's. The
@ gatekeeper is beaten and the awe scenes seen, so the walk to the doors is free.
    test_header League_AboveCloudHeader, League_AboveCloudScript
League_AboveCloudScript:
    lockall
    setvar VAR_TEMP_F, 1
    settrainerflag TRAINER_ICHOR_ASCENT_POLYDAMAS
    setflag FLAG_ICHOR_SEEN_CLOUD_BREAK
    setflag FLAG_ICHOR_SEEN_PANTHEON
    warp MAP_ASCENT_3F, 21, 9
    waitstate
    releaseall
    end
