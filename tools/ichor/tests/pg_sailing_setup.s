@ Test-only event scripts for tools/ichor/tests/pg_sailing.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. The shared post-game
@ headers (PgLib_*) and the test_header macro come from pg_setup.inc.
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/field_move.h"
#include "constants/flags.h"
#include "constants/ichor.h"
#include "constants/ichor_sailing.h"
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

#include "tools/ichor/tests/pg_setup.inc"

@ --- Akti's gangplank, as the akti agent's event will run it -------------------
	test_header PgSail_BoardHeader, PgSail_Board
PgSail_Board:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, VOYAGE_AKTI
	goto EventScript_IchorBoardShip

@ --- The deck's helm and gangplank ------------------------------------------------
	test_header PgSail_HelmHeader, PgSail_Helm
PgSail_Helm:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorHelm

	test_header PgSail_LeaveHeader, PgSail_Leave
PgSail_Leave:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorLeaveShip

@ --- A landing on a sea map, for Akti -----------------------------------------------
	test_header PgSail_LandHeader, PgSail_Land
PgSail_Land:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, VOYAGE_AKTI
	goto EventScript_IchorLand

@ --- In the ship at sea: VAR_0x8004 map, 0x8005/6 x, y, 0x8007 facing (set by the Lua)
	test_header PgSail_ToSeaHeader, PgSail_ToSea
PgSail_ToSea:
	lockall
	setvar VAR_TEMP_F, 1
	special Ichor_PutShipAtSea
	releaseall
	end

@ --- The wind: VAR_0x8004 direction, VAR_0x8005 strength (set by the Lua) -----------
	test_header PgSail_WindHeader, PgSail_Wind
PgSail_Wind:
	lockall
	setvar VAR_TEMP_F, 1
	special Ichor_SetWind
	releaseall
	end

	test_header PgSail_GrudgeHeader, PgSail_Grudge
PgSail_Grudge:
	lockall
	setvar VAR_TEMP_F, 1
	special Ichor_SetGrudge
	releaseall
	end

	test_header PgSail_LiftGrudgeHeader, PgSail_LiftGrudge
PgSail_LiftGrudge:
	lockall
	setvar VAR_TEMP_F, 1
	special Ichor_LiftGrudge
	releaseall
	end

@ --- What the scripts see: VAR_0x8000 port, 0x8001 stars, 0x8002 encounter %,
@ 0x8003 moored at Akti; Ichor_GetWind's 0x8004-0x8006; Ichor_BufferWind's strings
	test_header PgSail_QueryHeader, PgSail_Query
PgSail_Query:
	lockall
	setvar VAR_TEMP_F, 1
	specialvar VAR_0x8000, Ichor_GetShipPort
	specialvar VAR_0x8001, Ichor_IsStarsOut
	specialvar VAR_0x8002, Ichor_GetSailingEncounterRate
	setvar VAR_0x8004, VOYAGE_AKTI
	specialvar VAR_0x8003, Ichor_IsMooredAt
	specialvar VAR_RESULT, Ichor_GetWind
	special Ichor_BufferWind
	releaseall
	end
