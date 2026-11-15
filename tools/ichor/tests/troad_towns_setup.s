@ Test-only event scripts for tools/ichor/tests/troad_towns.lua. Never linked into
@ the ROM: tools/ichor/tests/troad_towns.sh assembles this file with the game's
@ own macros and links it in free EWRAM, resolving ROM symbols against
@ pokeemerald.elf. The Lua test copies the blob into RAM and points
@ gMapHeader.mapScripts at one of the headers below, whose ON_FRAME entry then
@ runs on the next overworld frame. Warping onto water starts the player surfing.
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

@ --- 1. A post-game player with one strong Pokémon, landing at Sestos ---------
	.global TroadTest_SetupHeader
TroadTest_SetupHeader:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TroadTest_SetupTable
	.byte 0
	.align 2
TroadTest_SetupTable:
	map_script_2 VAR_TEMP_F, 0, TroadTest_Setup
	.2byte 0
	.align 2
TroadTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	@ Every badge keeps a level-100 Pokémon obedient; it wins every battle with A.
	givemon SPECIES_MEWTWO, 100, move1=MOVE_PSYCHIC, move2=MOVE_ICE_BEAM, move3=MOVE_THUNDERBOLT, move4=MOVE_SURF
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_BADGE01_GET
	setflag FLAG_BADGE02_GET
	setflag FLAG_BADGE03_GET
	setflag FLAG_BADGE04_GET
	setflag FLAG_BADGE05_GET
	setflag FLAG_BADGE06_GET
	setflag FLAG_BADGE07_GET
	setflag FLAG_BADGE08_GET
	@ A long Repel: a level-100 lead keeps every wild Pokémon away.
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_SESTOS, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- 2. Warps to (VAR_0x8008, VAR_0x8009) on each map -------------------------
	.macro troad_warp name:req, map:req
	.global TroadTest_Warp\name\()Header
TroadTest_Warp\name\()Header:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TroadTest_Warp\name\()Table
	.byte 0
	.align 2
TroadTest_Warp\name\()Table:
	map_script_2 VAR_TEMP_F, 0, TroadTest_Warp\name
	.2byte 0
	.align 2
TroadTest_Warp\name:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent \map, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end
	.endm

	troad_warp Sestos, MAP_SESTOS
	troad_warp Hellespont, MAP_HELLESPONT
	troad_warp Ilion, MAP_ILION
