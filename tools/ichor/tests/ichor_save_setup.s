@ Test-only event scripts for tools/ichor/tests/ichor_save.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
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

@ --- 1. Write and read back every kind of bank slot ---------------------------
@ VAR_0x8000 gets one bit per check that read back right; the Lua checks the
@ raw bytes in IchorSave as well.
	test_header SaveTest_BanksHeader, SaveTest_Banks
SaveTest_Banks:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8000, 0
	setflag FLAG_ICHOR_GENERAL_START
	setflag ICHOR_FLAGS_END
	setflag FLAG_ICHOR_HERMS_START + 3
	setflag FLAG_DAILY_ICHOR_PRAYED_START + 2
	setflag ICHOR_DAILY_FLAGS_END
	setvar ICHOR_VARS_START, 1234
	setvar ICHOR_VARS_END, 0xBEEF
	goto_if_unset FLAG_ICHOR_GENERAL_START, SaveTest_Banks_1
	addvar VAR_0x8000, 1
SaveTest_Banks_1:
	goto_if_unset ICHOR_FLAGS_END, SaveTest_Banks_2
	addvar VAR_0x8000, 2
SaveTest_Banks_2:
	goto_if_unset FLAG_DAILY_ICHOR_PRAYED_START + 2, SaveTest_Banks_3
	addvar VAR_0x8000, 4
SaveTest_Banks_3:
	goto_if_set FLAG_ICHOR_GENERAL_START + 1, SaveTest_Banks_4
	addvar VAR_0x8000, 8
SaveTest_Banks_4:
	goto_if_ne ICHOR_VARS_START, 1234, SaveTest_Banks_5
	addvar VAR_0x8000, 16
SaveTest_Banks_5:
	goto_if_ne ICHOR_VARS_END, 0xBEEF, SaveTest_Banks_6
	addvar VAR_0x8000, 32
SaveTest_Banks_6:
	@ a bank flag cleared again
	setflag FLAG_ICHOR_GENERAL_START + 7
	clearflag FLAG_ICHOR_GENERAL_START + 7
	goto_if_set FLAG_ICHOR_GENERAL_START + 7, SaveTest_Banks_7
	addvar VAR_0x8000, 64
SaveTest_Banks_7:
	releaseall
	end

@ --- 2. Run the day's events: once to start the clock (Quickstart leaves the
@ water clock unset), then again after the Lua moves the clock a day on --------
	test_header SaveTest_ClockHeader, SaveTest_Clock
SaveTest_Clock:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_SYS_CLOCK_SET
	dotimebasedevents
	releaseall
	end

	test_header SaveTest_NewDayHeader, SaveTest_NewDay
SaveTest_NewDay:
	lockall
	setvar VAR_TEMP_F, 1
	dotimebasedevents
	releaseall
	end

@ --- 3. Save the game (the Lua answers the prompts) ---------------------------
	test_header SaveTest_SaveHeader, SaveTest_Save
SaveTest_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end
