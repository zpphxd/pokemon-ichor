@ Test-only event scripts for tools/ichor/tests/ichor_labyrinth.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/field_move.h"
#include "constants/flags.h"
#include "constants/ichor.h"
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

@ --- A Pokémon (no follower), the relics, Route 1 at (VAR_0x8008, VAR_0x8009) ------
	test_header LabTest_SetupHeader, LabTest_Setup
LabTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIPLUP, 30
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_KLEON_TOOK_STARTER
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_GOT_POKEBALLS
	setflag FLAG_ICHOR_HIDE_KLEON_ELAIA
	setflag FLAG_ICHOR_HIDE_ALETHEA_ELAIA
	setflag FLAG_ICHOR_RUINS_CLEARED
	setflag FLAG_ICHOR_HIDE_ROUTE1_FLOCK
	setflag FLAG_ICHOR_ARRIVED_AKTI
	setflag FLAG_ICHOR_VISITED_AKTI
	setflag FLAG_ICHOR_HIDE_ALETHEA_AKTI
	setflag FLAG_ICHOR_FOLLOWERS_DISABLED
	additem ITEM_ARIADNES_THREAD
	additem ITEM_HELM_OF_DARKNESS
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header LabTest_WarpHeader, LabTest_Warp
LabTest_Warp:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- Route 1 as a threaded ring: floor metatile 1, twins 2-11, two bronze rings ------
	test_header LabTest_ThreadMapHeader, LabTest_ThreadMap
LabTest_ThreadMap:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 2
	special Ichor_AddThreadFloor
	setvar VAR_0x8004, 15
	setvar VAR_0x8005, 49
	setvar VAR_0x8006, THREAD_ANCHOR_GRAND_STAIRCASE
	special Ichor_AddThreadAnchor
	setvar VAR_0x8004, 19
	setvar VAR_0x8005, 49
	setvar VAR_0x8006, THREAD_ANCHOR_UNNAMED
	special Ichor_AddThreadAnchor
	special Ichor_DrawThread
	special DrawWholeMapView
	end

	test_header LabTest_ThreadMenuHeader, LabTest_ThreadMenu
LabTest_ThreadMenu:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorThreadMenu

@ --- Asterion: object VAR_0x8008, and a cracked wall at (13,50) -----------------
	test_header LabTest_RespawnHeader, LabTest_Respawn
LabTest_Respawn:
	lockall
	setvar VAR_TEMP_F, 1
	removeobject VAR_0x8008
	addobject VAR_0x8008
	releaseall
	end

	test_header LabTest_AsterionHeader, LabTest_Asterion
LabTest_Asterion:
	setvar VAR_TEMP_F, 1
	copyvar VAR_0x8004, VAR_0x8008
	special Ichor_StartAsterion
	setvar VAR_0x8004, 13
	setvar VAR_0x8005, 50
	setvar VAR_0x8006, FLAG_TEMP_1
	setvar VAR_0x8007, 1
	special Ichor_AddCrackedWall
	end

	test_header LabTest_RestHeader, LabTest_Rest
LabTest_Rest:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, 3
	special Ichor_AsterionRest
	end

@ --- A dial: bit 3 of VAR_TEMP_2; the result in VAR_TEMP_3 ---------------------
	test_header LabTest_DialHeader, LabTest_Dial
LabTest_Dial:
	setvar VAR_TEMP_F, 1
	copyvar VAR_0x8004, VAR_TEMP_2
	setvar VAR_0x8005, 3
	call EventScript_IchorDial
	copyvar VAR_TEMP_2, VAR_0x8004
	copyvar VAR_TEMP_3, VAR_RESULT
	releaseall
	end

	test_header LabTest_GiveHeader, LabTest_Give
LabTest_Give:
	lockall
	setvar VAR_TEMP_F, 1
	additem VAR_0x8004, VAR_0x8005
	releaseall
	end
