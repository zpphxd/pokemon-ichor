#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/ichor.h"
#include "constants/items.h"
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

	test_header RolloverTest_SetupHeader, RolloverTest_Setup
RolloverTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 50
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_ARRIVED_ELEUSA
	setflag FLAG_ICHOR_ACT1_COMPLETE
	setflag FLAG_ICHOR_GOT_DEMETERS_SICKLE
	setflag FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA
	setflag FLAG_ICHOR_MYSTERIES_NIGHT
	setflag FLAG_ICHOR_ROCKSLIDE_CLEARED
	setvar VAR_REPEL_STEP_COUNT, 999
	callnative InitTimeBasedEvents
	warp MAP_ELEUSA_VILLAGE, 31, 35
	waitstate
	releaseall
	end

	test_header RolloverTest_AdvanceHeader, RolloverTest_Advance
RolloverTest_Advance:
	lockall
	setvar VAR_TEMP_F, 1
	special Ichor_ForceOmen
	callnative RolloverTest_NextDay
	releaseall
	end

	test_header RolloverTest_ConsumeHeader, RolloverTest_Consume
RolloverTest_Consume:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_ICHOR_HIDE_OMEN_KORANTHA
	removeobject LOCALID_ELEUSA_OMEN_KORANTHA
	releaseall
	end

	test_header RolloverTest_HeldHeader, RolloverTest_Held
RolloverTest_Held:
	lockall
	setvar VAR_TEMP_F, 1
	special Ichor_ForceOmen
	callnative Ichor_OmenNewDay
	delay 180
	releaseall
	end

	test_header RolloverTest_SpotHeader, RolloverTest_Spot
RolloverTest_Spot:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_ELEUSA_VILLAGE, 32, 35
	waitstate
	releaseall
	end

	test_header RolloverTest_IsthmusHeader, RolloverTest_Isthmus
RolloverTest_Isthmus:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_ROUTE4_ISTHMUS, 28, 4
	waitstate
	releaseall
	end

	.align 2
	.syntax unified
	.thumb
	.thumb_func
RolloverTest_NextDay:
	push {r4, lr}
	bl RtcCalcLocalTime
	ldr r0, =gLocalTime
	movs r1, #0
	ldrsh r0, [r0, r1]
	adds r0, #1
	movs r1, #0
	movs r2, #0
	movs r3, #0
	bl RtcCalcLocalTimeOffset
	pop {r4, pc}
