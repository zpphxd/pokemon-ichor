@ Test-only scripts for ball_throw.lua: a fresh partner on Route 1's grass,
@ a ball of one kind in the Bag, and a wild battle to throw it in.
#include "constants/flags.h"
#include "constants/global.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/pokemon.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
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

	test_header Ball_SetupHeader, Ball_Setup
Ball_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 50
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_ACT1_COMPLETE
	setvar VAR_REPEL_STEP_COUNT, 999
	warp MAP_KALLISTE_ROUTE1, 10, 10
	waitstate
	releaseall
	end

	.macro give_header name:req, item:req
	test_header Ball_Give\name\()Header, Ball_Give\name
Ball_Give\name:
	setvar VAR_TEMP_F, 1
	giveitem \item, 5
	end
	.endm

	give_header Dive, ITEM_DIVE_BALL
	give_header Master, ITEM_MASTER_BALL
	give_header Great, ITEM_GREAT_BALL
	give_header Dusk, ITEM_DUSK_BALL
	give_header Poke, ITEM_POKE_BALL

	test_header Ball_BattleHeader, Ball_Battle
Ball_Battle:
	setvar VAR_TEMP_F, 1
	setwildbattle SPECIES_NEBREL, 3
	dowildbattle
	end
