@ Test-only event scripts for tools/ichor/tests/pg_westsea.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/field_move.h"
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

@ --- A strong Pokémon, the post-game, quiet slice flags; Route 33 at (VAR_0x8008, VAR_0x8009)
	test_header WestseaTest_SetupHeader, WestseaTest_Setup
WestseaTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_MEWTWO, 70
	setmonmove 0, 0, MOVE_PSYSTRIKE
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
	setflag FLAG_ICHOR_HIDE_ROUTE1_FLOCK
	setflag FLAG_ICHOR_ARRIVED_AKTI
	setflag FLAG_ICHOR_VISITED_AKTI
	setflag FLAG_ICHOR_HIDE_ALETHEA_AKTI
	setflag FLAG_ICHOR_POSTGAME
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_ROUTE33_WESTERN_SEA, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- Route 33 at (VAR_0x8008, VAR_0x8009): onto water you arrive surfing ---------
	test_header WestseaTest_WarpHeader, WestseaTest_Warp
WestseaTest_Warp:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_ROUTE33_WESTERN_SEA, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header WestseaTest_GiveHeader, WestseaTest_Give
WestseaTest_Give:
	lockall
	setvar VAR_TEMP_F, 1
	additem VAR_0x8004, VAR_0x8005
	releaseall
	end

@ --- Heal the party between battles -----------------------------------------------
	test_header WestseaTest_HealHeader, WestseaTest_Heal
WestseaTest_Heal:
	lockall
	setvar VAR_TEMP_F, 1
	special HealPlayerParty
	releaseall
	end
