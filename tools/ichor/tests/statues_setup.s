#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
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

    test_header Act3Test_WarpHeader, Act3Test_Warp
Act3Test_Warp:
    lockall
    setvar VAR_TEMP_F, 1
    warpsilent MAP_AKTI_TOWN_AGORA, VAR_0x8008, VAR_0x8009
    waitstate
    releaseall
    end

    test_header Act3Test_RespawnHeader, Act3Test_Respawn
Act3Test_Respawn:
    lockall
    setvar VAR_TEMP_F, 1
    removeobject VAR_0x8000
    removeobject VAR_0x8001
    removeobject VAR_0x8002
    addobject VAR_0x8000
    addobject VAR_0x8001
    addobject VAR_0x8002
    releaseall
    end

    test_header Act3Test_RemoveHeader, Act3Test_Remove
Act3Test_Remove:
    lockall
    setvar VAR_TEMP_F, 1
    removeobject VAR_0x8000
    releaseall
    end

    test_header Act3Test_RedrawHeader, Act3Test_Redraw
Act3Test_Redraw:
    lockall
    setvar VAR_TEMP_F, 1
    special DrawWholeMapView
    releaseall
    end

    test_header Act3Test_TurnEastHeader, Act3Test_TurnEast
Act3Test_TurnEast:
    lockall
    setvar VAR_TEMP_F, 1
    turnobject VAR_0x8000, DIR_EAST
    releaseall
    end

    .global Act3Test_StatueTouch
Act3Test_StatueTouch:
    lockall
    addvar VAR_0x8003, 1
    copyvar VAR_0x8006, VAR_FACING
    copyvar VAR_0x8007, VAR_LAST_TALKED
    releaseall
    end
