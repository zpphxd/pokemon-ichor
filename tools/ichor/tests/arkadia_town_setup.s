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

    @ Kleon's recruitment: arriving with four Laurels, before Kallisto.
    test_header ArkadiaTown_RecruitHeader, ArkadiaTown_RecruitScript
ArkadiaTown_RecruitScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KYNDER, 100, move1=MOVE_FLAMETHROWER, move2=MOVE_LEER
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_ARKADIA, 12, 36
    waitstate
    releaseall
    end

    test_header ArkadiaTown_SetupHeader, ArkadiaTown_SetupScript
ArkadiaTown_SetupScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KYNDER, 100, move1=MOVE_FLAMETHROWER, move2=MOVE_LEER
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_ICHOR_KLEON_JOINED_TITANS
    setflag FLAG_ICHOR_KALLISTO_TRIAL
    setflag FLAG_ICHOR_ACT1_COMPLETE
    @ This walks doors and seams. Damo stands on the walk to the Cave of Maia and
    @ Euandros inside it; their battles are RNG (2-13 turns, sometimes lost or
    @ drawn, which whites out to Arkadia), so any ROM change could fail the walk.
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_R12_DAMO
    setflag TRAINER_FLAGS_START + TRAINER_ICHOR_EUANDROS
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_ARKADIA, 20, 31
    waitstate
    releaseall
    end
