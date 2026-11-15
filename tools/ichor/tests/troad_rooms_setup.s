@ Test-only event scripts for tools/ichor/tests/troad_rooms.lua. Never linked
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

	@ A header that warps into a room through its door mat (warp 0).
	.macro room_header name:req, map:req
	test_header \name, \name\()_Script
\name\()_Script:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent \map, 0
	waitstate
	releaseall
	end
	.endm

@ --- The party and the bag the households want ------------------------------------
@ A Pelipper first (Kymon's trade takes the first slot), then a Mewtwo strong
@ enough for Odysseus, three dye berries for Theano. The Gate Emblem is set, as
@ Hektor's hall would, for Priam's gift; the chisel's find, as the Walls of
@ Laomedon will (batch 2), for the mason's.
	test_header TroadTest_SetupHeader, TroadTest_Setup
TroadTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PELIPPER, 60
	givemon SPECIES_MEWTWO, 100, move1=MOVE_PSYSTRIKE, move2=MOVE_AURA_SPHERE, move3=MOVE_ICE_BEAM, move4=MOVE_RECOVER
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_EMBLEM_GATE
	setflag FLAG_ICHOR_FOUND_MASONS_CHISEL
	additem ITEM_CHERI_BERRY
	additem ITEM_ORAN_BERRY
	additem ITEM_ASPEAR_BERRY
	setvar VAR_REPEL_STEP_COUNT, 999
	releaseall
	end

@ --- A Mudsdale for Idaios -------------------------------------------------------
	test_header TroadTest_GiveMudsdaleHeader, TroadTest_GiveMudsdale
TroadTest_GiveMudsdale:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_MUDSDALE, 60
	releaseall
	end

@ --- What time of day the game thinks it is, into VAR_0x8000 ---------------------
	test_header TroadTest_TimeHeader, TroadTest_Time
TroadTest_Time:
	lockall
	setvar VAR_TEMP_F, 1
	gettimeofday
	releaseall
	end

@ --- Into each room, through its door mat ----------------------------------------
	room_header TroadTest_SestosAsclepeionHeader, MAP_SESTOS_ASCLEPEION
	room_header TroadTest_SestosAgoraHeader, MAP_SESTOS_AGORA
	room_header TroadTest_SestosHerosTowerHeader, MAP_SESTOS_HEROS_TOWER
	room_header TroadTest_SestosFerryHouseHeader, MAP_SESTOS_FERRY_HOUSE
	room_header TroadTest_SestosNetLoftHeader, MAP_SESTOS_NET_LOFT
	room_header TroadTest_IlionAsclepeionHeader, MAP_ILION_ASCLEPEION
	room_header TroadTest_IlionAgoraHeader, MAP_ILION_AGORA
	room_header TroadTest_IlionPriamsPalaceHeader, MAP_ILION_PRIAMS_PALACE
	room_header TroadTest_IlionCassandrasRoomHeader, MAP_ILION_CASSANDRAS_ROOM
	room_header TroadTest_IlionGuestRoomHeader, MAP_ILION_GUEST_ROOM
	room_header TroadTest_IlionHorseStableHeader, MAP_ILION_HORSE_STABLE
	room_header TroadTest_IlionMasonsHouseHeader, MAP_ILION_MASONS_HOUSE
	room_header TroadTest_IlionWeaversHouseHeader, MAP_ILION_WEAVERS_HOUSE
	room_header TroadTest_IlionTempleOfAthenaHeader, MAP_ILION_TEMPLE_OF_ATHENA
