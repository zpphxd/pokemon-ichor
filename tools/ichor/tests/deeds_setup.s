#include "constants/global.h"
#include "constants/flags.h"
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

	test_header DeedsTest_SetupHeader, DeedsTest_Setup
DeedsTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 5
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_BADGE01_GET
	setflag FLAG_BADGE02_GET
	setflag FLAG_BADGE03_GET
	setflag FLAG_ICHOR_ARRIVED_EMPORION
	setflag FLAG_ICHOR_MYSTERIES_NIGHT
	setflag FLAG_ICHOR_FRAGMENT_STOLEN
	setflag FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA
	setflag FLAG_ICHOR_ACT1_COMPLETE
	setflag FLAG_ICHOR_WROTE_TO_MOM
	setflag FLAG_ICHOR_GOT_TROWEL
	warp MAP_ELAIA_VILLAGE, 13, 12
	waitstate
	releaseall
	end

	test_header DeedsTest_SaveHeader, DeedsTest_Save
DeedsTest_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end
