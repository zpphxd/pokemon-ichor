@ Test-only event scripts for tools/ichor/tests/act2_artemis.lua. Never linked into
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

@ --- 1. The state beat 43 leaves the player in, then the temple's door -----------
@ A level-100 Prinplup that knows only Surf, so mashing FIGHT wins every battle with
@ no level-up or evolution. The eighth badge keeps it obedient. The first four laurels
@ are Act I's and Thespis's; the fifth is the Moon Laurel, which Kallisto gives. Kleon
@ has gone to the Titans (beat 42), so the temple's door is open. Followers are off, so
@ the hounds' patrols run exactly as the test's model of them says.
	test_header ArtemisTest_SetupHeader, ArtemisTest_Setup
ArtemisTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PRINPLUP, 100, move1=MOVE_SURF, move2=MOVE_NONE, move3=MOVE_NONE, move4=MOVE_NONE
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_BADGE01_GET
	setflag FLAG_BADGE02_GET
	setflag FLAG_BADGE03_GET
	setflag FLAG_BADGE04_GET
	setflag FLAG_BADGE08_GET
	setflag FLAG_ICHOR_KLEON_JOINED_TITANS
	setflag FLAG_ICHOR_FOLLOWERS_DISABLED
	warp MAP_ARKADIA_TEMPLE_OF_ARTEMIS, 0
	waitstate
	releaseall
	end

@ --- 2. Back in through the door (the garden should stay solved) ----------------
	test_header ArtemisTest_ReenterHeader, ArtemisTest_Reenter
ArtemisTest_Reenter:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_ARKADIA_TEMPLE_OF_ARTEMIS, 0
	waitstate
	releaseall
	end
