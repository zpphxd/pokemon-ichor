@ Test-only event scripts for tools/ichor/tests/ichor_frozen.lua. Never linked
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

@ --- A Pokémon, quiet slice flags, Route 1 at (VAR_0x8008, VAR_0x8009), no repel ----
	test_header FrozenTest_SetupHeader, FrozenTest_Setup
FrozenTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIPLUP, 20
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
	setvar VAR_REPEL_STEP_COUNT, 0
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- The Frozen Hour, entered by loading the map with its flag set ------------------
	test_header FrozenTest_EnterHeader, FrozenTest_Enter
FrozenTest_Enter:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_ICHOR_FROZEN_HOUR
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- A script that locks and releases everyone ----------------------------------
	test_header FrozenTest_LockReleaseHeader, FrozenTest_LockRelease
FrozenTest_LockRelease:
	lockall
	setvar VAR_TEMP_F, 1
	delay 30
	releaseall
	end

@ --- Respawn object VAR_0x8008 from its (rewritten) template ----------------------
	test_header FrozenTest_RespawnHeader, FrozenTest_Respawn
FrozenTest_Respawn:
	lockall
	setvar VAR_TEMP_F, 1
	removeobject VAR_0x8008
	addobject VAR_0x8008
	releaseall
	end

@ --- The specials, as map scripts call them (VAR_0x8004/5 set by the Lua) ---------
	test_header FrozenTest_UnfreezeHeader, FrozenTest_Unfreeze
FrozenTest_Unfreeze:
	setvar VAR_TEMP_F, 1
	special Ichor_UnfreezeObject
	end

	test_header FrozenTest_SepiaBeginHeader, FrozenTest_SepiaBegin
FrozenTest_SepiaBegin:
	setvar VAR_TEMP_F, 1
	special Ichor_SepiaMemoryBegin
	end

	test_header FrozenTest_SepiaEndHeader, FrozenTest_SepiaEnd
FrozenTest_SepiaEnd:
	setvar VAR_TEMP_F, 1
	special Ichor_SepiaMemoryEnd
	end

	test_header FrozenTest_ColorStepHeader, FrozenTest_ColorStep
FrozenTest_ColorStep:
	setvar VAR_TEMP_F, 1
	special Ichor_ColorReturnStep
	end

	test_header FrozenTest_BeginHeader, FrozenTest_Begin
FrozenTest_Begin:
	lockall
	setvar VAR_TEMP_F, 1
	special Ichor_FrozenHourBegin
	releaseall
	end
