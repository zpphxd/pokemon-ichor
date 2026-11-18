@ Test-only event scripts for the Act III engine checks (ichor_statues,
@ ichor_bull_leap, ichor_beam). Never linked into the ROM: engine_build.sh
@ assembles this file with the game's own macros and links it into spare EWRAM
@ against pokeemerald.elf. Each header's ON_FRAME entry runs once while
@ VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader). The Lua passes local ids and
@ coordinates in VAR_0x8000-VAR_0x8009.
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/flags.h"
#include "constants/ichor_act3.h"
#include "constants/items.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/moves.h"
#include "constants/pokemon.h"
#include "constants/species.h"
#include "constants/trainers.h"
#include "constants/opponents.h"
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

@ --- The test spot: the Akti Agora at (VAR_0x8008, VAR_0x8009) ----------------
	test_header Act3Test_WarpHeader, Act3Test_Warp
Act3Test_Warp:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_AKTI_TOWN_AGORA, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- Respawn the map's first three objects from their templates, or remove one
@ The Lua rewrites the templates in SaveBlock1 first (place, movement type,
@ script); removing and adding each object spawns it again from its template.
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

@ --- Redraw the map from the grid, after the Lua has written it ---------------
	test_header Act3Test_RedrawHeader, Act3Test_Redraw
Act3Test_Redraw:
	lockall
	setvar VAR_TEMP_F, 1
	special DrawWholeMapView
	releaseall
	end

@ --- Turn the object VAR_0x8000 (a mirror) ------------------------------------
	test_header Act3Test_TurnNorthHeader, Act3Test_TurnNorth
Act3Test_TurnNorth:
	lockall
	setvar VAR_TEMP_F, 1
	turnobject VAR_0x8000, DIR_NORTH
	releaseall
	end

	test_header Act3Test_TurnSouthHeader, Act3Test_TurnSouth
Act3Test_TurnSouth:
	lockall
	setvar VAR_TEMP_F, 1
	turnobject VAR_0x8000, DIR_SOUTH
	releaseall
	end

	test_header Act3Test_TurnEastHeader, Act3Test_TurnEast
Act3Test_TurnEast:
	lockall
	setvar VAR_TEMP_F, 1
	turnobject VAR_0x8000, DIR_EAST
	releaseall
	end

	test_header Act3Test_TurnWestHeader, Act3Test_TurnWest
Act3Test_TurnWest:
	lockall
	setvar VAR_TEMP_F, 1
	turnobject VAR_0x8000, DIR_WEST
	releaseall
	end

@ --- A statue's touch: the statue's own script. VAR_0x8003 counts touches; ----
@ VAR_0x8006 and VAR_0x8007 get VAR_FACING (DIR_NONE for a touch) and the
@ statue's local id.
	.global Act3Test_StatueTouch
Act3Test_StatueTouch:
	lockall
	addvar VAR_0x8003, 1
	copyvar VAR_0x8006, VAR_FACING
	copyvar VAR_0x8007, VAR_LAST_TALKED
	releaseall
	end

@ --- special Ichor_BullLeap with VAR_0x8004-VAR_0x8007 as the Lua set them ----
	test_header Act3Test_LeapHeader, Act3Test_Leap
Act3Test_Leap:
	lockall
	setvar VAR_TEMP_F, 1
	special Ichor_BullLeap
	releaseall
	end

@ (Ichor_TraceBeam's test header lives with the beam special, not ported to zach-main yet.)
