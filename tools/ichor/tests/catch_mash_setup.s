#include "constants/flags.h"
#include "constants/global.h"
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

	test_header Mash_SetupHeader, Mash_Setup
Mash_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 80
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_ACT1_COMPLETE
	setvar VAR_REPEL_STEP_COUNT, 999
	@ Poké Balls first, so they sit at the top of the ball pocket.
	giveitem ITEM_POKE_BALL, 20
	giveitem ITEM_MASTER_BALL, 1
	callnative InitTimeBasedEvents
	warp MAP_ELAIA_VILLAGE_AKADEMIA, 13, 4
	waitstate
	releaseall
	end

	@ Nebrel, catch rate 45, at level 3 (Gen 9's low-level bonus, x3): a modified
	@ catch rate of 45 at full HP, so about an 18% throw before the bonus.
	test_header Mash_BattleHeader, Mash_Battle
Mash_Battle:
	setvar VAR_TEMP_F, 1
	setwildbattle SPECIES_NEBREL, 3
	dowildbattle
	end
