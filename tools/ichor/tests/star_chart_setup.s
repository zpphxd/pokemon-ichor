#include "constants/global.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
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
	test_header ChartTest_SetupHeader, ChartTest_Setup
ChartTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 5
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	giveitem ITEM_STAR_CHART
	warp MAP_ELAIA_VILLAGE, 13, 12
	waitstate
	releaseall
	end
	test_header ChartTest_SaveHeader, ChartTest_Save
ChartTest_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end
