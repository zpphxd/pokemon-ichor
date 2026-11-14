@ Test-only event scripts for tools/ichor/tests/trireme.lua. Never linked into
@ the ROM: tools/ichor/tests/trireme.sh assembles this file with the game's own
@ macros and links it at the blob address, in free EWRAM past the game's data,
@ resolving ROM symbols against pokeemerald.elf. The Lua test copies the blob
@ into RAM and points gMapHeader.mapScripts at one of the headers below, whose
@ ON_FRAME entry then runs on the next overworld frame.
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

@ --- 1. The state after beat 9B, then up the gangway onto the deck -----------
	.global TriremeTest_SetupHeader
TriremeTest_SetupHeader:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TriremeTest_SetupTable
	.byte 0
	.align 2
TriremeTest_SetupTable:
	map_script_2 VAR_TEMP_F, 0, TriremeTest_Setup
	.2byte 0
	.align 2
TriremeTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	@ A sturdy starter, so mashing A wins the snatcher battles without level-ups.
	@ The eighth badge keeps a level-30 starter obedient.
	givemon SPECIES_PIPLUP, 30
	setflag FLAG_BADGE08_GET
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_ICHOR_HALIA_SECOND_LOOK
	setflag FLAG_ICHOR_WINDS_TURNED
	setflag FLAG_ICHOR_MOM_HARBOR
	setflag FLAG_ICHOR_BOARDED_EUPLOIA
	@ No wild encounters on the walk (the deck has none; this is for safety).
	setvar VAR_REPEL_STEP_COUNT, 999
	@ The gangplank's warp, as Akti's quay and the ferry use it: the deck's warp 0.
	warp MAP_TRIREME_EUPLOIA_DECK, 0
	waitstate
	releaseall
	end

@ --- 2. Beat 10C: the morning after the night at Aigina's inn ----------------
	.global TriremeTest_LastLegHeader
TriremeTest_LastLegHeader:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TriremeTest_LastLegTable
	.byte 0
	.align 2
TriremeTest_LastLegTable:
	map_script_2 VAR_TEMP_F, 0, TriremeTest_LastLeg
	.2byte 0
	.align 2
TriremeTest_LastLeg:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_ICHOR_ARRIVED_AEGINA
	setflag FLAG_ICHOR_VISITED_AEGINA
	setflag FLAG_ICHOR_AEGINA_NIGHT
	warp MAP_TRIREME_EUPLOIA_DECK, 0
	waitstate
	releaseall
	end
