@ Test-only event scripts for tools/ichor/tests/ichor_dig.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
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

@ --- A Pokémon, quiet slice flags, Route 1 at (VAR_0x8008, VAR_0x8009) ------
	test_header DigTest_SetupHeader, DigTest_Setup
DigTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIPLUP, 20
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_KLEON_TOOK_STARTER
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_GOT_POKEBALLS
	setflag FLAG_ICHOR_HIDE_KLEON_ELAIA
	setflag FLAG_ICHOR_HIDE_ALETHEA_ELAIA
	setflag FLAG_ICHOR_RUINS_CLEARED
	setflag FLAG_ICHOR_ARRIVED_AKTI
	setflag FLAG_ICHOR_VISITED_AKTI
	setflag FLAG_ICHOR_HIDE_ALETHEA_AKTI
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header DigTest_GiveHeader, DigTest_Give
DigTest_Give:
	lockall
	setvar VAR_TEMP_F, 1
	additem VAR_0x8004, VAR_0x8005
	releaseall
	end

	test_header DigTest_TakeHeader, DigTest_Take
DigTest_Take:
	lockall
	setvar VAR_TEMP_F, 1
	removeitem VAR_0x8004, VAR_0x8005
	releaseall
	end

@ --- The dig spots, run as a map's bg event would run them -----------------------
	test_header DigTest_SpotHeader, DigTest_Spot
DigTest_Spot:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorDigSpot

	test_header DigTest_FixedHeader, DigTest_Fixed
DigTest_Fixed:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorDigFixed

@ --- A dig called from a map's own script, which goes on afterwards -------------
	test_header DigTest_CallHeader, DigTest_Call
DigTest_Call:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8009, 0xFF
	call EventScript_IchorDigFixed
	copyvar VAR_0x8009, VAR_RESULT
	lockall
	msgbox DigTest_Text_After, MSGBOX_DEFAULT
	releaseall
	end

DigTest_Text_After:
	.string "And the script goes on.$"
