#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
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

	test_header KallisteDigs_SetupHeader, KallisteDigs_Setup
KallisteDigs_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 50
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_RUINS_CLEARED
	setflag FLAG_ICHOR_HIDE_ALETHEA_RUINS
	setflag FLAG_ICHOR_HIDE_RUINS_GRUNTS
	setflag FLAG_ICHOR_HIDE_TITAN_TABLET
	setflag FLAG_ICHOR_CROSSING_DONE
	setflag FLAG_ICHOR_ACT1_COMPLETE
	setvar VAR_REPEL_STEP_COUNT, 9999
	callnative InitTimeBasedEvents
	warp MAP_KALLISTE_ROUTE1_KRONION_HILL, 12, 9
	waitstate
	releaseall
	end

	test_header KallisteDigs_KronionHeader, KallisteDigs_Kronion
KallisteDigs_Kronion:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_KALLISTE_ROUTE1_KRONION_HILL, 12, 9
	waitstate
	releaseall
	end

	test_header KallisteDigs_TerracesHeader, KallisteDigs_Terraces
KallisteDigs_Terraces:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_KALLISTE_ROUTE1, 23, 27
	waitstate
	releaseall
	end

	test_header KallisteDigs_AktiHeader, KallisteDigs_Akti
KallisteDigs_Akti:
	lockall
	setvar VAR_TEMP_F, 1
	warp MAP_AKTI_TOWN, 24, 8
	waitstate
	releaseall
	end

	test_header KallisteDigs_AkademiaHeader, KallisteDigs_Akademia
KallisteDigs_Akademia:
	lockall
	setvar VAR_TEMP_F, 1
	setflag FLAG_ICHOR_MYSTERIES_NIGHT
	warp MAP_ELAIA_VILLAGE_AKADEMIA, 13, 4
	waitstate
	releaseall
	end

	test_header KallisteDigs_TrowelHeader, KallisteDigs_Trowel
KallisteDigs_Trowel:
	setvar VAR_TEMP_F, 1
	additem ITEM_ALETHEAS_TROWEL
	end

// Probe the real roller without finishing a dig or changing collection flags.
	test_header KallisteDigs_ProbeHeader, KallisteDigs_Probe
KallisteDigs_Probe:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8006, ICHOR_DIG_MODE_SPOT
	specialvar VAR_TEMP_E, Ichor_DigStart
	specialvar VAR_RESULT, Ichor_DigFindKind
	end

	test_header KallisteDigs_SaveHeader, KallisteDigs_Save
KallisteDigs_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end

	test_header KallisteDigs_AdvanceHeader, KallisteDigs_Advance
KallisteDigs_Advance:
	lockall
	setvar VAR_TEMP_F, 1
	callnative KallisteDigs_NextDay
	releaseall
	end

	.align 2
	.syntax unified
	.thumb
	.thumb_func
KallisteDigs_NextDay:
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
