@ Test-only event scripts for tools/ichor/tests/act2_heights.lua. Never linked into
@ the ROM: engine_build.sh assembles this file with the game's own macros and links
@ it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME entry runs once
@ while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
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

@ --- The state beat 37 leaves the player in, at the top of Route 11 ---------------
@ A level-100 Prinplup that knows only Surf (mashing FIGHT wins every battle with no
@ level-up), the eighth badge (it obeys), the four laurels Act II has given by now, the
@ Girdle of Herakles (Thyrsa, beat 34), Fresh Water for the thirsty traveler, and a
@ Chelyra for the Cave of Maia's singer.
	test_header HeightsTest_SetupHeader, HeightsTest_Setup
HeightsTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PRINPLUP, 100, move1=MOVE_SURF, move2=MOVE_NONE, move3=MOVE_NONE, move4=MOVE_NONE
	givemon SPECIES_CHELYRA, 34
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_ICHOR_FOLLOWERS_DISABLED	@ the walker talks to whatever stands in front: not the follower
	setflag FLAG_BADGE01_GET
	setflag FLAG_BADGE02_GET
	setflag FLAG_BADGE03_GET
	setflag FLAG_BADGE04_GET
	setflag FLAG_BADGE08_GET
	additem ITEM_GIRDLE_OF_HERAKLES
	additem ITEM_FRESH_WATER
	additem ITEM_OLIVE_OIL, 2
	setvar VAR_REPEL_STEP_COUNT, 999
	warp MAP_ROUTE11_KRATHIS_GORGE, 19, 3
	waitstate
	releaseall
	end

@ --- Back to the drums from Arkadia: the road below them, to check they stay moved ---
	test_header HeightsTest_ReturnHeader, HeightsTest_Return
HeightsTest_Return:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_ROUTE11_KRATHIS_GORGE, 20, 20
	waitstate
	releaseall
	end
