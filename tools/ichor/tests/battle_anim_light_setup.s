@ Test-only scripts: a wild battle where both sides know ordinary moves.
#include "constants/flags.h"
#include "constants/global.h"
#include "constants/pokemon.h"
#include "constants/items.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/moves.h"
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

	test_header Anim_SetupHeader, Anim_Setup
Anim_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_BLISSEY, 50
	createmon 0, 0, SPECIES_BLISSEY, 50, move1=MOVE_TACKLE, move2=MOVE_BRICK_BREAK, move3=MOVE_MEGA_DRAIN, move4=MOVE_SCARY_FACE
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_BADGE08_GET
	setvar VAR_REPEL_STEP_COUNT, 999
	warp MAP_KALLISTE_ROUTE1_KRONION_HILL, 13, 12
	waitstate
	releaseall
	end

	test_header Anim_BattleHeader, Anim_Battle
Anim_Battle:
	setvar VAR_TEMP_F, 1
	special HealPlayerParty
	createmon 1, 0, SPECIES_BLISSEY, 50, move1=MOVE_TACKLE, move2=MOVE_BRICK_BREAK, move3=MOVE_MEGA_DRAIN, move4=MOVE_SCARY_FACE
	dowildbattle
	end
