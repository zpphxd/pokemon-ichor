@ Test-only event scripts for tools/ichor/tests/ichor_rites.lua. Never linked
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

@ --- Snivy (who can learn Solar Beam), quiet slice flags, Route 1 at
@ (VAR_0x8008, VAR_0x8009) ------------------------------------------------------
	test_header RitesTest_SetupHeader, RitesTest_Setup
RitesTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 20, move1=MOVE_TACKLE, move2=MOVE_LEER
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
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- Give VAR_0x8005 of item VAR_0x8004 -------------------------------------------
	test_header RitesTest_GiveHeader, RitesTest_Give
RitesTest_Give:
	lockall
	setvar VAR_TEMP_F, 1
	additem VAR_0x8004, VAR_0x8005
	releaseall
	end

@ --- The altars, as a map's bg event would run them -----------------------------
	test_header RitesTest_ApolloHeader, RitesTest_Apollo
RitesTest_Apollo:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorAltar_Apollo

	test_header RitesTest_ApolloTempleHeader, RitesTest_ApolloTemple
RitesTest_ApolloTemple:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorTempleAltar_Apollo

	test_header RitesTest_AthenaHeader, RitesTest_Athena
RitesTest_Athena:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorAltar_Athena

	test_header RitesTest_HearthHeader, RitesTest_Hearth
RitesTest_Hearth:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorHearth

	test_header RitesTest_DemeterHeader, RitesTest_Demeter
RitesTest_Demeter:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorAltar_Demeter

	test_header RitesTest_DesecratedHeader, RitesTest_Desecrated
RitesTest_Desecrated:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, ICHOR_GOD_APOLLO
	setvar VAR_0x8005, 0
	goto EventScript_IchorDesecratedAltar

	test_header RitesTest_HermesMapHeader, RitesTest_HermesMap
RitesTest_HermesMap:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_BADGE02_GET
	setflag FLAG_ICHOR_HERALDS_RUN_DONE
	setflag FLAG_ICHOR_GOT_TM_AERIAL_ACE
	setflag FLAG_ICHOR_GIFT(ICHOR_GOD_HERMES, ICHOR_GIFT_HIEROPHANT)
	givemon SPECIES_HARPECK, 5, move1=MOVE_PECK, move2=MOVE_NONE, move3=MOVE_NONE, move4=MOVE_NONE
	warp MAP_EMPORION_CITY_TEMPLE_OF_HERMES, 9, 5
	waitstate
	releaseall
	end

	test_header RitesTest_DemeterMapHeader, RitesTest_DemeterMap
RitesTest_DemeterMap:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_BADGE03_GET
	warp MAP_ELEUSA_VILLAGE_TEMPLE_OF_DEMETER, 14, 6
	waitstate
	releaseall
	end

	test_header RitesTest_CheckUturnHeader, RitesTest_CheckUturn
RitesTest_CheckUturn:
	setvar VAR_TEMP_F, 1
	callnative RitesTest_ReadMove
	end

	.align 2
	.syntax unified
	.thumb
	.thumb_func
RitesTest_ReadMove:
	push {r4, lr}
	ldr r0, =gParties
	ldr r1, =gSpecialVar_0x8004
	ldrh r1, [r1]
	adds r0, r0, r1
	ldr r1, =gSpecialVar_0x8005
	ldrh r1, [r1]
	bl GetMonData2
	ldr r1, =gSpecialVar_0x8007
	strh r0, [r1]
	pop {r4, pc}
