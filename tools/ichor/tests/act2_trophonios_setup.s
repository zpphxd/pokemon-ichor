@ Test-only event scripts for tools/ichor/tests/act2_trophonios.lua. Never linked into
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

@ --- 1. The state beat 35B leaves the player in, at the grille's foot --------------
@ A level-100 Prinplup that knows only Surf, so mashing FIGHT wins every battle with
@ no level-up or evolution; the eighth badge keeps it obedient. Act I's Torch and
@ Hammer, one Honey (Saon's), and the grille open (Saon sets it in Lebadeia).
	test_header TrophTest_SetupHeader, TrophTest_Setup
TrophTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PRINPLUP, 100, move1=MOVE_SURF, move2=MOVE_NONE, move3=MOVE_NONE, move4=MOVE_NONE
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_BADGE01_GET
	setflag FLAG_BADGE02_GET
	setflag FLAG_BADGE03_GET
	setflag FLAG_BADGE08_GET
	additem ITEM_HECATES_TORCH, 1
	additem ITEM_BRONZE_HAMMER, 1
	additem ITEM_HONEY, 1
	setflag FLAG_ICHOR_TROPHONIOS_GRILLE_OPEN
	setvar VAR_REPEL_STEP_COUNT, 999
	warp MAP_TROPHONIOS_CAVE_B1F, 0
	waitstate
	releaseall
	end

@ --- The torch, doused and relit as the Relic Ring does -------------------------------
	test_header TrophTest_DouseHeader, TrophTest_Douse
TrophTest_Douse:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorTorchDoused

	test_header TrophTest_RelightHeader, TrophTest_Relight
TrophTest_Relight:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorTorchRelit

@ --- Hephaestus's Hammer: the Bronze Hammer's upgrade (Hephaestus's gift II) ----------
	test_header TrophTest_HephaestusHeader, TrophTest_Hephaestus
TrophTest_Hephaestus:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_ICHOR_HEPHAESTUS_HAMMER
	releaseall
	end

@ --- A long Repel again (the walk back down) --------------------------------------------
	test_header TrophTest_RepelHeader, TrophTest_Repel
TrophTest_Repel:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_REPEL_STEP_COUNT, 999
	releaseall
	end
