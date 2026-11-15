@ Test-only event scripts for tools/ichor/tests/pontos_rooms.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
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

	@ warp into a room by its door mat (warp 0), as the town's door would
	.macro room_header name:req, map:req
	test_header \name, \name\()_Script
\name\()_Script:
	lockall
	setvar VAR_TEMP_F, 1
	warp \map, 0
	waitstate
	releaseall
	end
	.endm

@ --- The party the rooms need: a Pidgeot and a Liepard to trade, a Rotom that
@ knows only Thunder Shock (so each form's move has room) ----------------------
	test_header PontosTest_SetupHeader, PontosTest_Setup
PontosTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIDGEOT, 40
	givemon SPECIES_LIEPARD, 40
	givemon SPECIES_ROTOM, 40, move1=MOVE_THUNDER_SHOCK, move2=MOVE_NONE, move3=MOVE_NONE, move4=MOVE_NONE
	setflag FLAG_SYS_POKEMON_GET
	setvar VAR_REPEL_STEP_COUNT, 999
	releaseall
	end

@ --- The species in party slot VAR_0x8005, into VAR_0x8000 -----------------------
	test_header PontosTest_SpeciesHeader, PontosTest_Species
PontosTest_Species:
	lockall
	setvar VAR_TEMP_F, 1
	copyvar VAR_0x8004, VAR_0x8005
	specialvar VAR_0x8000, ScriptGetPartyMonSpecies
	releaseall
	end

	room_header PontosTest_PhineusHeader, MAP_SALMYDESSOS_PHINEUSS_HOUSE
	room_header PontosTest_BirdCatcherHeader, MAP_SALMYDESSOS_BIRD_CATCHERS_HOUSE
	room_header PontosTest_AsclepeionHeader, MAP_AIA_ASCLEPEION
	room_header PontosTest_AgoraHeader, MAP_AIA_AGORA
	room_header PontosTest_PhrixosHeader, MAP_AIA_PHRIXOS_SONS_HOUSE
	room_header PontosTest_LinenHeader, MAP_AIA_LINEN_WEAVERS_HOUSE
	room_header PontosTest_WorkshopHeader, MAP_AIA_PALACE_WORKSHOP
