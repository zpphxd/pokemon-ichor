#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/flags.h"
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

	test_header HomeTest_SetupHeader, HomeTest_Setup
HomeTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 5, move1=MOVE_TACKLE
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	clearflag FLAG_ICHOR_HIDE_MOM_HOME
	warp MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_1F, 3, 4
	waitstate
	releaseall
	end

	test_header HomeTest_RunnersHeader, HomeTest_Runners
HomeTest_Runners:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_EMPORION_CITY_RUNNERS_HOUSE, 5, 7
	waitstate
	releaseall
	end

	test_header HomeTest_ReturnHeader, HomeTest_Return
HomeTest_Return:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_1F, 3, 4
	waitstate
	releaseall
	end

	test_header HomeTest_EleusaHeader, HomeTest_Eleusa
HomeTest_Eleusa:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_ELEUSA_VILLAGE, 46, 6
	waitstate
	releaseall
	end

	test_header HomeTest_SaveHeader, HomeTest_Save
HomeTest_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end
