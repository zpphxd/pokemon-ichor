@ Test-only event scripts for tools/ichor/tests/pg_opening.lua. Never linked into
@ the ROM: engine_build.sh assembles this file with the game's own macros and links
@ it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME entry runs once
@ while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
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

@ --- A save as the slice and the acts leave it: a Pokémon, every slice beat done,
@ --- the Hearth Laurel, the temple's acolytes beaten. The post-game flag stays clear.
	test_header PgTest_SetupHeader, PgTest_Setup
PgTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIPLUP, 70
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_ICHOR_SET_WATER_CLOCK
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_KLEON_TOOK_STARTER
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_GOT_POKEBALLS
	setflag FLAG_ICHOR_HIDE_KLEON_ELAIA
	setflag FLAG_ICHOR_HIDE_ALETHEA_ELAIA
	setflag FLAG_ICHOR_HIDE_ALETHEA_AKADEMIA
	setflag FLAG_ICHOR_HIDE_SCRIBE
	setflag FLAG_ICHOR_RUINS_CLEARED
	setflag FLAG_ICHOR_HIDE_ROUTE1_FLOCK
	setflag FLAG_ICHOR_ARRIVED_AKTI
	setflag FLAG_ICHOR_VISITED_AKTI
	setflag FLAG_ICHOR_AKTI_GOAT_HOME
	setflag FLAG_ICHOR_HIDE_AKTI_LOOSE_GOAT
	setflag FLAG_ICHOR_GOT_MYSTIC_WATER
	setflag FLAG_ICHOR_GOT_ROUTE1_SITRUS
	setflag FLAG_BADGE01_GET
	setflag FLAG_ICHOR_GOT_TM_FACADE
	setflag FLAG_ICHOR_HEARTH_TRIAL_DONE
	setflag FLAG_ICHOR_GOT_CHARCOAL
	setvar VAR_ICHOR_HEARTH_TRIAL, 6
	settrainerflag TRAINER_ICHOR_LAMPON
	settrainerflag TRAINER_ICHOR_PYRRHA
	settrainerflag TRAINER_ICHOR_AITHRA
	settrainerflag TRAINER_ICHOR_IONE_1
	setflag FLAG_ICHOR_SLICE_COMPLETE
	setflag FLAG_ICHOR_HIDE_KLEON_AKTI
	setflag FLAG_ICHOR_HIDE_ALETHEA_AKTI
	setvar VAR_REPEL_STEP_COUNT, 999
	releaseall
	end

@ --- Warps: (VAR_0x8008, VAR_0x8009) on each map ---------------------------------
	test_header PgTest_ElaiaHeader, PgTest_Elaia
PgTest_Elaia:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_ELAIA_VILLAGE, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header PgTest_AktiHeader, PgTest_Akti
PgTest_Akti:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_AKTI_TOWN, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header PgTest_TempleHeader, PgTest_Temple
PgTest_Temple:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_AKTI_TOWN_TEMPLE_OF_HESTIA, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header PgTest_AsclepeionHeader, PgTest_Asclepeion
PgTest_Asclepeion:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_AKTI_TOWN_ASCLEPEION, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header PgTest_FishersHeader, PgTest_Fishers
PgTest_Fishers:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_AKTI_TOWN_FISHERS_HOUSE, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header PgTest_AgoraHeader, PgTest_Agora
PgTest_Agora:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_AKTI_TOWN_AGORA, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header PgTest_Route1Header, PgTest_Route1
PgTest_Route1:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end
