@ Test-only event scripts for tools/ichor/tests/emporion_runner.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/flags.h"
#include "constants/ichor.h"
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

@ --- Just won the Moon Laurel and came down Route 14: onto its east end -----------
@ (Eleusa visited but its herm never touched: the runner's YES must still get there)
    test_header Runner_MoonHeader, Runner_MoonScript
Runner_MoonScript:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KYNDER, 100, move1=MOVE_FLAMETHROWER, move2=MOVE_LEER
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_ICHOR_ACT1_COMPLETE
    setflag FLAG_ICHOR_KLEON_WON_HERALD
    setflag FLAG_ICHOR_KLEON_BATTLE_2_DONE
    setflag FLAG_ICHOR_ARKADIA_NORTH_OPEN
    setflag FLAG_ICHOR_VISITED_ELEUSA
    setflag FLAG_ICHOR_ARRIVED_ELEUSA
    setflag FLAG_ICHOR_SAFFRON_THREAD
    setflag FLAG_ICHOR_TOWN_HERM_EMPORION
    setflag FLAG_ICHOR_TOWN_HERM_NEMEA
    setvar VAR_REPEL_STEP_COUNT, 999
    warp MAP_ROUTE14_NEMEA_ROAD, 78, 13
    waitstate
    releaseall
    end

@ --- Back to the same moment, but by the Nemea herm: land at Emporion's ----------
    test_header Runner_LandHeader, Runner_LandScript
Runner_LandScript:
    lockall
    setvar VAR_TEMP_F, 1
    clearflag FLAG_ICHOR_TOLD_ELEUSA_ROAD
    warp MAP_EMPORION_CITY, 19, 41
    waitstate
    releaseall
    end
