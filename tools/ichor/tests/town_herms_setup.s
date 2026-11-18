@ Test-only event scripts for tools/ichor/tests/town_herms.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/ichor.h"
#include "constants/items.h"
#include "constants/map_event_ids.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
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

@ --- A Pokémon, quiet slice flags, into Akti's Asclepeion ------------------------
@ (warpsilent runs the Asclepeion's own transition script: setrespawn to Akti)
	test_header TownHermTest_SetupHeader, TownHermTest_Setup
TownHermTest_Setup:
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
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_AKTI_TOWN_ASCLEPEION, 7, 5
	waitstate
	releaseall
	end

@ --- Akti's healer, run as the counter would run it ------------------------------
	test_header TownHermTest_HealHeader, TownHermTest_Heal
TownHermTest_Heal:
	setvar VAR_TEMP_F, 1
	lock
	setvar VAR_0x800B, LOCALID_AKTI_HEALER
	call Ichor_EventScript_AsclepeionHealer
	waitmessage
	waitbuttonpress
	release
	end

@ --- To Emporion at (VAR_0x8008, VAR_0x8009) ------------------------------------
	test_header TownHermTest_EmporionHeader, TownHermTest_Emporion
TownHermTest_Emporion:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_EMPORION_CITY, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- Ask the engine directly: the travel count here, and a warp to an
@ unregistered town (VAR_0x8004), which must refuse ------------------------------
	test_header TownHermTest_ProbeHeader, TownHermTest_Probe
TownHermTest_Probe:
	setvar VAR_TEMP_F, 1
	specialvar VAR_0x8005, Ichor_CountTravelHerms
	specialvar VAR_0x8006, Ichor_TravelToTownHerm
	end
