@ Existing retired bike tables exercised only in spare EWRAM.
#include "constants/map_scripts.h"
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

	header ElaiaEffects_State
	header ElaiaEffects_Free
	header PlayerBikes_Setup

	.include "build/player_bikes/consts.s"
