@ Test-only event scripts for act3_kythera_road.sh. Never linked into the ROM:
@ engine_build.sh assembles this file with the game's own macros and links it
@ into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME entry runs
@ once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
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

@ --- The state Skandeia leaves behind: landed (VAR_ICHOR_ACT3 2), Alethea met on
@ the main street; a strong team (badge 8 so it obeys), the Talaria, one berry.
	test_header Road_SetupHeader, Road_Setup
Road_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_METAGROSS, 100, move1=MOVE_IRON_HEAD
	givemon SPECIES_METAGROSS, 100, move1=MOVE_IRON_HEAD
	setflag FLAG_BADGE08_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_ICHOR_ALETHEA_REJOINED
	setvar VAR_ICHOR_ACT3, 2
	additem ITEM_ORAN_BERRY, 1
	releaseall
	end

@ --- Into the Foam Road at Skandeia's gate (VAR_0x8008, VAR_0x8009) ------------------
	test_header Road_WarpFoamRoadHeader, Road_WarpFoamRoad
Road_WarpFoamRoad:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_KYTHERA_FOAM_ROAD, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- The Foam Laurel, as Galatea gives it (act3_galatea_gallery.sh plays her) --------
	test_header Road_LaurelHeader, Road_Laurel
Road_Laurel:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_BADGE07_GET
	setflag FLAG_ICHOR_GALATEA_FALLS_HINT
	setvar VAR_ICHOR_ACT3, 3
	special HealPlayerParty
	releaseall
	end

@ --- Two more berries for Krenaia's first fruits (three in all) ---------------------
	test_header Road_BerriesHeader, Road_Berries
Road_Berries:
	lockall
	setvar VAR_TEMP_F, 1
	additem ITEM_ORAN_BERRY, 2
	releaseall
	end
