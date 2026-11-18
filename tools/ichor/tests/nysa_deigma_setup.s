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

@ A party of four: a lead, the two Onotis to leave at the nursery (a male and
@ a female, same Trainer: "medium" compatibility, 50%), and a fourth so two
@ can be left. Money for the stalls, old coins for the trapeza.
	test_header NysaTest_SetupHeader, NysaTest_Setup
NysaTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SWAMPERT, 50
	givemon SPECIES_ONOTIS, 20, , , , , MON_MALE
	givemon SPECIES_ONOTIS, 20, , , , , MON_FEMALE
	givemon SPECIES_HARPECK, 18
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_ARRIVED_EMPORION
	setflag FLAG_ICHOR_DEIGMA_CLUE
	setvar VAR_REPEL_STEP_COUNT, 999
	addmoney 200000
	giveitem ITEM_RELIC_COPPER, 2
	giveitem ITEM_RELIC_GOLD, 1
	callnative InitTimeBasedEvents
	warp MAP_ROUTE7_KRONIA_GROUNDS, 35, 5
	waitstate
	releaseall
	end

	test_header NysaTest_Route7Header, NysaTest_Route7
NysaTest_Route7:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_ROUTE7_KRONIA_GROUNDS, 38, 5
	waitstate
	releaseall
	end

	test_header NysaTest_CityHeader, NysaTest_City
NysaTest_City:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_EMPORION_CITY, 36, 38
	waitstate
	releaseall
	end

	test_header NysaTest_NextDayHeader, NysaTest_NextDay
NysaTest_NextDay:
	lockall
	setvar VAR_TEMP_F, 1
	callnative NysaTest_AdvanceDay
	releaseall
	end

	.align 2
	.syntax unified
	.thumb
	.thumb_func
NysaTest_AdvanceDay:
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
