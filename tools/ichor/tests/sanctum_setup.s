@ Test-only event scripts for tools/ichor/tests/sanctum.lua. Never linked into the
@ ROM: engine_build.sh assembles this file with the game's own macros and links it
@ into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME entry runs once
@ while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/ichor.h"
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

@ --- What the earlier beats leave behind, and down the Anaktoron's stair ----------
@ A party at Eleusa's levels (BALANCE.md: Chloe 24-26, Kleon about 23), each with
@ one move so a level-up never asks to forget one; three Laurels, so they obey;
@ Hecate's Torch; the Lesser Mysteries done and the sanctum open (beat 22). Then
@ to B1F's warp 0, the foot of the stair, where beat 22 lands the player.
	test_header SanctumTest_SetupHeader, SanctumTest_Setup
SanctumTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_THALAMARE, 26, hpIv=31, atkIv=31, defIv=31, speedIv=31, spAtkIv=31, spDefIv=31, move1=MOVE_SURF
	givemon SPECIES_KERAZAP, 25, hpIv=31, atkIv=31, defIv=31, speedIv=31, spAtkIv=31, spDefIv=31, move1=MOVE_THUNDERBOLT
	givemon SPECIES_HALCYLING, 24, hpIv=31, atkIv=31, defIv=31, speedIv=31, spAtkIv=31, spDefIv=31, move1=MOVE_WATER_PULSE
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_BADGE01_GET
	setflag FLAG_BADGE02_GET
	setflag FLAG_BADGE03_GET
	additem ITEM_HECATES_TORCH
	additem ITEM_ALETHEAS_TROWEL
	setflag FLAG_ICHOR_LESSER_MYSTERIES_DONE
	setflag FLAG_ICHOR_BRAZIERS_START + 0x10
	setflag FLAG_ICHOR_BRAZIERS_START + 0x11
	setflag FLAG_ICHOR_BRAZIERS_START + 0x12
	setflag FLAG_ICHOR_BRAZIERS_START + 0x13
	setflag FLAG_ICHOR_SANCTUM_OPEN
	setvar VAR_REPEL_STEP_COUNT, 999
	warp MAP_ELEUSA_SANCTUM_B1F, 0
	waitstate
	releaseall
	end

@ --- Back down to the deepest granary, after the theft (the climb back) -----------
	test_header SanctumTest_BackDownHeader, SanctumTest_BackDown
SanctumTest_BackDown:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_ELEUSA_SANCTUM_B3F, 0
	waitstate
	releaseall
	end

	test_header SanctumTest_SaveHeader, SanctumTest_Save
SanctumTest_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end
