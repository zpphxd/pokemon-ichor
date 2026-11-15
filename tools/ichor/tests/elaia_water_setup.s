@ Forced mount/underwater fixtures, never linked into the production ROM.
#include "config/general.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/flags.h"
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
	header ElaiaWater_State
	header ElaiaWater_Free

	.global ElaiaWater_SetupHeader
ElaiaWater_SetupHeader:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, ElaiaWater_SetupTable
	.byte 0
	.align 2
ElaiaWater_SetupTable:
	map_script_2 VAR_TEMP_F, 0, ElaiaWater_SetupScript
	.2byte 0
ElaiaWater_SetupScript:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_ICHOR_HIDE_ROUTE1_FLOCK
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_KALLISTE_ROUTE1, 13, 41
	waitstate
	releaseall
	end
	.include "build/elaia_water/consts.s"
