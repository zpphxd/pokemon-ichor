@ Test-only event scripts for tools/ichor/tests/ichor_world.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
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

@ --- A Pokémon, quiet slice flags, Route 1 at (VAR_0x8008, VAR_0x8009) ------
	test_header WorldTest_SetupHeader, WorldTest_Setup
WorldTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIPLUP, 20
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
	setflag FLAG_ICHOR_ARRIVED_AKTI
	setflag FLAG_ICHOR_VISITED_AKTI
	setflag FLAG_ICHOR_HIDE_ALETHEA_AKTI
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- The clock: VAR_0x8004 hours, VAR_0x8005 minutes, today ----------------------
	test_header WorldTest_ClockHeader, WorldTest_Clock
WorldTest_Clock:
	lockall
	setvar VAR_TEMP_F, 1
	callnative WorldTest_SetClock
	releaseall
	end

@ --- A host's bed: the rest, with its answer in VAR_0x8009 -------------------------
	test_header WorldTest_RestHeader, WorldTest_Rest
WorldTest_Rest:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8009, 0xFF
	call EventScript_IchorXeniaRest
	copyvar VAR_0x8009, VAR_RESULT
	releaseall
	end

@ --- The party's highest level, in VAR_0x8009 -------------------------------------
	test_header WorldTest_LevelHeader, WorldTest_Level
WorldTest_Level:
	lockall
	setvar VAR_TEMP_F, 1
	specialvar VAR_0x8009, Ichor_GetHighestPartyLevel
	releaseall
	end

@ --- A knucklebones match against VAR_0x8004, its answer in VAR_0x8009 ----------
	test_header WorldTest_BonesHeader, WorldTest_Bones
WorldTest_Bones:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8009, 0xFF
	bufferstring STR_VAR_3, WorldTest_Text_Glauke
	call EventScript_IchorKnucklebones
	copyvar VAR_0x8009, VAR_RESULT
	releaseall
	end

WorldTest_Text_Glauke:
	.string "Glauke$"

@ --- Route 1 at (VAR_0x8008, VAR_0x8009); an object respawned from its template ---
	test_header WorldTest_WarpHeader, WorldTest_Warp
WorldTest_Warp:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header WorldTest_RespawnHeader, WorldTest_Respawn
WorldTest_Respawn:
	lockall
	setvar VAR_TEMP_F, 1
	removeobject VAR_0x8008
	addobject VAR_0x8008
	releaseall
	end

@ --- Save the game (the Lua answers the prompts) -----------------------------------
	test_header WorldTest_SaveHeader, WorldTest_Save
WorldTest_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end

@ RtcCalcLocalTimeOffset(gLocalTime.days, VAR_0x8004, VAR_0x8005, 0)
	.thumb
	.align 2
	.thumb_func
	.global WorldTest_SetClock
WorldTest_SetClock:
	push {r4, lr}
	ldr r4, =RtcCalcLocalTime
	bl WorldTest_CallR4
	ldr r0, =gLocalTime
	mov r1, #0
	ldrsh r0, [r0, r1]            @ today
	ldr r1, =gSpecialVar_0x8004
	ldrh r1, [r1]                 @ hours
	ldr r2, =gSpecialVar_0x8005
	ldrh r2, [r2]                 @ minutes
	mov r3, #0                    @ seconds
	ldr r4, =RtcCalcLocalTimeOffset
	bl WorldTest_CallR4
	pop {r4}
	pop {r0}
	bx r0
WorldTest_CallR4:
	bx r4
	.pool
