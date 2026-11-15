@ Test-only event scripts for tools/ichor/tests/egypt_rooms.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/daycare.h"
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

@ --- A party for the rooms: two Pidgey for the egg-ovens, a Smeargle for the
@ potter, a Machamp to keep; a Helix Fossil for Daphne. Then into Naukratis's
@ Asclepeion by its door mat. ---------------------------------------------------
	test_header EgyptTest_SetupHeader, EgyptTest_Setup
EgyptTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIDGEY, 30
	givemon SPECIES_PIDGEY, 30
	givemon SPECIES_SMEARGLE, 40
	givemon SPECIES_MACHAMP, 60
	giveitem ITEM_HELIX_FOSSIL
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	warp MAP_NAUKRATIS_ASCLEPEION, 0
	waitstate
	releaseall
	end

@ --- Into each room by its door mat (warp 0) ---------------------------------------
	.macro warp_header name:req, map:req
	test_header \name, \name\()_Script
\name\()_Script:
	lockall
	setvar VAR_TEMP_F, 1
	warp \map, 0
	waitstate
	releaseall
	end
	.endm

	warp_header EgyptTest_NAsclepeionHeader, MAP_NAUKRATIS_ASCLEPEION
	warp_header EgyptTest_NAgoraHeader, MAP_NAUKRATIS_AGORA
	warp_header EgyptTest_NFieldStationHeader, MAP_NAUKRATIS_FIELD_STATION
	warp_header EgyptTest_NEggOvensHeader, MAP_NAUKRATIS_EGG_OVENS
	warp_header EgyptTest_NIncenseShopHeader, MAP_NAUKRATIS_INCENSE_SHOP
	warp_header EgyptTest_NPottersHouseHeader, MAP_NAUKRATIS_POTTERS_HOUSE
	warp_header EgyptTest_NNetLoftHeader, MAP_NAUKRATIS_NET_LOFT
	warp_header EgyptTest_MAsclepeionHeader, MAP_MEMPHIS_ASCLEPEION
	warp_header EgyptTest_MAgoraHeader, MAP_MEMPHIS_AGORA
	warp_header EgyptTest_MApisStableHeader, MAP_MEMPHIS_APIS_STABLE
	warp_header EgyptTest_MScribesHouseHeader, MAP_MEMPHIS_SCRIBES_HOUSE
	warp_header EgyptTest_MEmbalmersHouseHeader, MAP_MEMPHIS_EMBALMERS_HOUSE

@ --- Read-backs: the day care's state into VAR_0x8000 and the party size into
@ VAR_0x8001; the species in party slots 0-5 into VAR_0x8008.. via a loop is
@ more than a test needs, so slots 0-3 go to VAR_0x8000-0x8003 in the second. --
	test_header EgyptTest_DaycareHeader, EgyptTest_Daycare
EgyptTest_Daycare:
	setvar VAR_TEMP_F, 1
	specialvar VAR_0x8000, GetDaycareState
	getpartysize
	copyvar VAR_0x8001, VAR_RESULT
	end

	test_header EgyptTest_PartyHeader, EgyptTest_Party
EgyptTest_Party:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, 0
	specialvar VAR_0x8000, ScriptGetPartyMonSpecies
	setvar VAR_0x8004, 1
	specialvar VAR_0x8001, ScriptGetPartyMonSpecies
	setvar VAR_0x8004, 2
	specialvar VAR_0x8002, ScriptGetPartyMonSpecies
	setvar VAR_0x8004, 3
	specialvar VAR_0x8003, ScriptGetPartyMonSpecies
	getpartysize
	copyvar VAR_0x8005, VAR_RESULT
	end
