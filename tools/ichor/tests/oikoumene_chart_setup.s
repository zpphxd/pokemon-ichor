@ Test-only event scripts for tools/ichor/tests/oikoumene_chart.lua. Never linked
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

@ --- A strong Pokémon, quiet slice flags, Sestos at (VAR_0x8008, VAR_0x8009) -----
	test_header ChartTest_SetupHeader, ChartTest_Setup
ChartTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIPLUP, 60
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
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_SESTOS, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

	test_header ChartTest_GiveHeader, ChartTest_Give
ChartTest_Give:
	lockall
	setvar VAR_TEMP_F, 1
	additem VAR_0x8004, VAR_0x8005
	releaseall
	end

@ --- Warps between the charts -------------------------------------------------------
	test_header ChartTest_AktiHeader, ChartTest_Akti
ChartTest_Akti:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_AKTI_TOWN, 14, 20
	waitstate
	releaseall
	end

	test_header ChartTest_NaukratisHeader, ChartTest_Naukratis
ChartTest_Naukratis:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_NAUKRATIS, 14, 20
	waitstate
	releaseall
	end

@ --- Battles on Oikoumene ground, for the music --------------------------------------
	test_header ChartTest_WildHeader, ChartTest_Wild
ChartTest_Wild:
	lockall
	setvar VAR_TEMP_F, 1
	setwildbattle SPECIES_WOOLOO, 5
	dowildbattle
	releaseall
	end

	test_header ChartTest_TrainerHeader, ChartTest_Trainer
ChartTest_Trainer:
	setvar VAR_TEMP_F, 1
	trainerbattle_no_intro TRAINER_ICHOR_TITYROS, ChartTest_Text_Lose
	end

ChartTest_Text_Lose:
	.string "Well fought.$"
