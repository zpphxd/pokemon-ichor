@ Test-only field-effect API and forced player-state evidence.
#include "config/general.h"
#include "constants/global.h"
#include "constants/pokemon.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/species.h"
#include "constants/vars.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"
	.text
	.align 2

	.macro header name:req
	.global \name\()Header
\name\()Header:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, \name\()Table
	.byte 0
	.align 2
\name\()Table:
	map_script_2 VAR_TEMP_F, 0, \name\()Script
	.2byte 0
\name\()Script:
	setvar VAR_TEMP_F, 1
	callnative \name
	end
	.align 2
	.endm

	header ElaiaEffects_Start
	header ElaiaEffects_Arrow
	header ElaiaEffects_Shadow
	header ElaiaEffects_Terrain
	header ElaiaEffects_Follower
	header ElaiaEffects_State
	header ElaiaEffects_Inspect
	header ElaiaEffects_Free

	.global ElaiaEffects_SetupHeader
ElaiaEffects_SetupHeader:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, ElaiaEffects_SetupTable
	.byte 0
	.align 2
ElaiaEffects_SetupTable:
	map_script_2 VAR_TEMP_F, 0, ElaiaEffects_SetupScript
	.2byte 0
ElaiaEffects_SetupScript:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_NEBREL, 30
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_KLEON_TOOK_STARTER
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_GOT_POKEBALLS
	setflag FLAG_ICHOR_RUINS_CLEARED
	setflag FLAG_ICHOR_HIDE_ROUTE1_FLOCK
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_KALLISTE_ROUTE1, 10, 39
	waitstate
	releaseall
	end

	.include "build/elaia_effects/consts.s"
