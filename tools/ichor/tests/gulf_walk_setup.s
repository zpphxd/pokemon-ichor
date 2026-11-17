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

    test_header Gulf_SetupHeader, Gulf_SetupScript
Gulf_SetupScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KYNDER, 100, move1=MOVE_FLAMETHROWER, move2=MOVE_LEER
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_ICHOR_ACT1_COMPLETE
    setflag FLAG_ICHOR_DIONYSIA_BROKEN
    additem ITEM_HECATES_TORCH, 1
    @ the arkadia_route check fights these; this one walks the places
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_R9_POLYON
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_R9_MNASON
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_R9_AKESON
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_R9_ERYX
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_R9_PHILTA
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_R9_DEINON
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_R9_THEANO
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_KORYKIAN_TITYROS
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_KORYKIAN_KORYKIA
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_LEBADEIA, 11, 28
    waitstate
    releaseall
    end
