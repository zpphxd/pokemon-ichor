@ Test-only event scripts for tools/ichor/tests/temple_demeter.lua. Never linked into
@ the ROM: engine_build.sh assembles this file with the game's own macros and links
@ it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME entry runs once
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

@ --- The road behind: the player has just come down Route 5 from Hecate's Hollow ----
@ A level-100 Kynder that knows Flamethrower first (and Leer second, for the lost
@ battle), the Herald Laurel and the Torch, as at the end of beat 18; the eighth badge
@ only so a level-100 Pokémon obeys. VAR_STARTER_MON 1 (Kynder): Kleon has Hipling.
@ Then onto Eleusa's west edge, where Route 5's road comes in.
	test_header DemeterTest_SetupHeader, DemeterTest_Setup
DemeterTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_KYNDER, 100, move1=MOVE_FLAMETHROWER, move2=MOVE_LEER, move3=MOVE_EMBER, move4=MOVE_SMOKESCREEN
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_BADGE01_GET
	setflag FLAG_BADGE02_GET
	setflag FLAG_BADGE08_GET
	setvar VAR_STARTER_MON, 1
	additem ITEM_HECATES_TORCH
	additem ITEM_BRONZE_HAMMER
	setflag FLAG_ICHOR_CROSSING_DONE
	setflag FLAG_ICHOR_ARRIVED_EMPORION
	setflag FLAG_ICHOR_VISITED_EMPORION
	setflag FLAG_ICHOR_GOT_TROWEL
	setflag FLAG_ICHOR_KLEON_BATTLE_2_DONE
	setflag FLAG_ICHOR_WON_KLEON_2
	setvar VAR_REPEL_STEP_COUNT, 999
	warp MAP_ELEUSA_VILLAGE, 0, 25
	waitstate
	releaseall
	end

@ --- The clock: night (22:00) or day (12:00) for Chloe's ace ------------------------
	test_header DemeterTest_NightHeader, DemeterTest_Night
DemeterTest_Night:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, 22
	callnative Ichor_SetHoursOverride
	end

	test_header DemeterTest_DayHeader, DemeterTest_Day
DemeterTest_Day:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, 12
	callnative Ichor_SetHoursOverride
	end
