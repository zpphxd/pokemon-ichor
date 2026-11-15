@ Test-only event scripts for tools/ichor/tests/route1.lua. Never linked into
@ the ROM: tools/ichor/tests/route1.sh assembles this file with the game's own
@ macros and links it at TEST_BLOB_ADDR, in free EWRAM past the game's data,
@ resolving ROM symbols against pokeemerald.elf. The Lua test copies the blob
@ into RAM and points gMapHeader.mapScripts at one of the headers below, whose
@ ON_FRAME entry then runs on the next overworld frame.
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
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

@ --- 1. The state Elaia leaves the player in after beat 4, then Route 1 -------
	.global Route1Test_SetupHeader
Route1Test_SetupHeader:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route1Test_SetupTable
	.byte 0
	.align 2
Route1Test_SetupTable:
	map_script_2 VAR_TEMP_F, 0, Route1Test_Setup
	.2byte 0
	.align 2
Route1Test_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	@ A sturdy starter, so mashing A wins every battle without level-ups. The
	@ expansion's obedience goes by level met, so the eighth badge keeps a
	@ level-30 starter obedient; nothing on Route 1 reads badges.
	givemon SPECIES_PIPLUP, 30
	setflag FLAG_BADGE08_GET
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_KLEON_TOOK_STARTER
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_GOT_POKEBALLS
	setflag FLAG_ICHOR_HIDE_KLEON_ELAIA
	setflag FLAG_ICHOR_HIDE_ALETHEA_ELAIA
	additem ITEM_POKE_BALL, 5
	@ A long Repel, so wild encounters don't interrupt the scripted walks.
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- 2. Warps to (VAR_0x8008, VAR_0x8009) on either map -----------------------
	.global Route1Test_WarpRoute1Header
Route1Test_WarpRoute1Header:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route1Test_WarpRoute1Table
	.byte 0
	.align 2
Route1Test_WarpRoute1Table:
	map_script_2 VAR_TEMP_F, 0, Route1Test_WarpRoute1
	.2byte 0
	.align 2
Route1Test_WarpRoute1:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	.global Route1Test_WarpKronionHeader
Route1Test_WarpKronionHeader:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route1Test_WarpKronionTable
	.byte 0
	.align 2
Route1Test_WarpKronionTable:
	map_script_2 VAR_TEMP_F, 0, Route1Test_WarpKronion
	.2byte 0
	.align 2
Route1Test_WarpKronion:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_KALLISTE_ROUTE1_KRONION_HILL, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end
