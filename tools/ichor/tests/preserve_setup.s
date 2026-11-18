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

@ Laurel 5's Arkadia: a Pokémon, some money, Kleon already gone to the Titans (his scene
@ on the west road done), and the player at the road's end by the keeper's hut.
    test_header Preserve_SetupHeader, Preserve_Setup
Preserve_Setup:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KAPRODON, 32
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_ICHOR_KLEON_JOINED_TITANS
    setflag FLAG_ICHOR_HIDE_IAPETOS_ARKADIA
    addmoney 3000
    warp MAP_ARKADIA, 5, 36
    waitstate
    releaseall
    end
