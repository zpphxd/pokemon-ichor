@ Test-only event scripts for tools/ichor/tests/oikoumene_trainer_pics.lua. Never
@ linked into the ROM: engine_build.sh assembles this file with the game's own
@ macros and links it into spare EWRAM against pokeemerald.elf. Each header's
@ ON_FRAME entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/map_scripts.h"
#include "constants/opponents.h"
#include "constants/pokemon.h"
#include "constants/species.h"
#include "constants/trainers.h"
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

@ --- 1. A Pokémon of your own, so a trainer can challenge you ------------------
	test_header OikTr_GiveHeader, OikTr_Give_Script
OikTr_Give_Script:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIPLUP, 70
	releaseall
	end

@ --- 2. The battle: the test trainer, whatever the Lua side has made of it ---
	test_header OikTr_BattleHeader, OikTr_Battle_Script
OikTr_Battle_Script:
	lockall
	setvar VAR_TEMP_F, 1
	trainerbattle_no_intro TRAINER_ICHOR_TITYROS, OikTr_Text_Defeat
	releaseall
	end

OikTr_Text_Defeat:
	.string "Well fought.$"
