@ Test-only event scripts for act3_trainers.sh. Never linked into the ROM:
@ engine_build.sh assembles this file with the game's own macros and links it
@ into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME entry runs
@ once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
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

@ --- Two level-100 Metagross that obey (the eighth badge), each with Iron Head
	test_header Act3Trainers_GiveHeader, Act3Trainers_Give
Act3Trainers_Give:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_METAGROSS, 100, move1=MOVE_IRON_HEAD
	givemon SPECIES_METAGROSS, 100, move1=MOVE_IRON_HEAD
	setflag FLAG_BADGE08_GET
	releaseall
	end

@ --- A battle with one trainer, where the player stands ---------------------
	.macro test_battle name:req, trainer:req
	test_header \name\()Header, \name
\name:
	lockall
	setvar VAR_TEMP_F, 1
	special HealPlayerParty
	trainerbattle_no_intro \trainer, Act3Trainers_Text_Lose
	releaseall
	end
	.endm

	test_battle Act3Trainers_Eudoros, TRAINER_ICHOR_EUDOROS
	test_battle Act3Trainers_Galatea, TRAINER_ICHOR_GALATEA_1

@ --- Into Axylos's house on Skandeia, where the bad guests' scene plays ------
	test_header Act3Trainers_GuestsHeader, Act3Trainers_Guests
Act3Trainers_Guests:
	lockall
	setvar VAR_TEMP_F, 1
	special HealPlayerParty
	warpsilent MAP_KYTHERA_SKANDEIA_AXYLOS_HOUSE, 6, 8
	waitstate
	releaseall
	end

Act3Trainers_Text_Lose:
	.string "Beaten.$"
