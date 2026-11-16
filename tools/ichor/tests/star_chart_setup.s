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

	test_header ChartTest_HillHeader, ChartTest_Hill
ChartTest_Hill:
	setvar VAR_TEMP_F, 1
	setflag FLAG_ICHOR_RUINS_CLEARED
	setflag FLAG_ICHOR_HIDE_ALETHEA_RUINS
	setflag FLAG_ICHOR_HIDE_RUINS_GRUNTS
	warp MAP_KALLISTE_ROUTE1_KRONION_HILL, 15, 9
	waitstate
	end

	test_header ChartTest_HoldHeader, ChartTest_Hold
ChartTest_Hold:
	setvar VAR_TEMP_F, 1
	special Ichor_HoldTimeOfDay
	end

	test_header ChartTest_RemoveHeader, ChartTest_Remove
ChartTest_Remove:
	setvar VAR_TEMP_F, 1
	removeitem ITEM_STAR_CHART
	end

	test_header ChartTest_GiveHeader, ChartTest_Give
ChartTest_Give:
	setvar VAR_TEMP_F, 1
	additem ITEM_STAR_CHART
	end

	test_header ChartTest_IndoorHeader, ChartTest_Indoor
ChartTest_Indoor:
	setvar VAR_TEMP_F, 1
	warp MAP_ELAIA_VILLAGE_AKADEMIA, 13, 4
	waitstate
	end

	test_header ChartTest_TrySkyHeader, ChartTest_TrySky
ChartTest_TrySky:
	setvar VAR_TEMP_F, 1
	specialvar VAR_TEMP_E, Ichor_ShowNightSky
	end
