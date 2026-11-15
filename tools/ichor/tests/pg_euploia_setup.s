@ Test-only event scripts for tools/ichor/tests/pg_euploia.lua. Never linked
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

@ --- A Pokémon, quiet slice flags, the post-game, the ship; then the deck ---------
	test_header EuploiaTest_SetupHeader, EuploiaTest_Setup
EuploiaTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIPLUP, 70
	givemon SPECIES_SNIVY, 70
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
	setflag FLAG_ICHOR_GOT_EUPLOIA
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_EUPLOIA_DECK, 6, 5
	waitstate
	releaseall
	end

@ --- Reload a map, so ON_LOAD and ON_TRANSITION run again with the flags as set
	test_header EuploiaTest_DeckHeader, EuploiaTest_Deck
EuploiaTest_Deck:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_EUPLOIA_DECK, 6, 5
	waitstate
	releaseall
	end

	test_header EuploiaTest_BelowHeader, EuploiaTest_Below
EuploiaTest_Below:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_EUPLOIA_BELOW, 8, 5
	waitstate
	releaseall
	end

@ --- Every keepsake on the trophy shelf, as batch 6's ON_LOAD will put them ------
	test_header EuploiaTest_ShelfHeader, EuploiaTest_Shelf
EuploiaTest_Shelf:
	lockall
	setvar VAR_TEMP_F, 1
	call EuploiaBelow_EventScript_KeepsakeFleece
	call EuploiaBelow_EventScript_KeepsakeLotus
	call EuploiaBelow_EventScript_KeepsakeCord
	call EuploiaBelow_EventScript_KeepsakeFeather
	call EuploiaBelow_EventScript_KeepsakeTooth
	call EuploiaBelow_EventScript_KeepsakeCup
	call EuploiaBelow_EventScript_KeepsakeOar
	special DrawWholeMapView
	releaseall
	end
