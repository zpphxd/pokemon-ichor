#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
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

	test_header AmphoraLeads_SetupHeader, AmphoraLeads_Setup
AmphoraLeads_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 5
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_MYSTERIES_NIGHT
	setflag FLAG_ICHOR_RUINS_CLEARED
	setflag FLAG_ICHOR_HIDE_RUINS_GRUNTS
	setflag FLAG_ICHOR_HIDE_ALETHEA_RUINS
	setflag FLAG_ICHOR_ACT1_COMPLETE
	setflag FLAG_ICHOR_GOT_DEMETERS_SICKLE
	setflag FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA
	setflag FLAG_ICHOR_ROCKSLIDE_CLEARED
	setvar VAR_REPEL_STEP_COUNT, 999
	giveitem ITEM_MASTER_BALL, 3
	callnative InitTimeBasedEvents
	warp MAP_ELAIA_VILLAGE_AKADEMIA, 13, 4
	waitstate
	releaseall
	end

	test_header AmphoraLeads_KronionHeader, AmphoraLeads_Kronion
AmphoraLeads_Kronion:
	setvar VAR_TEMP_F, 1
	warp MAP_KALLISTE_ROUTE1_KRONION_HILL, 13, 12
	waitstate
	end

	test_header AmphoraLeads_EleusaHeader, AmphoraLeads_Eleusa
AmphoraLeads_Eleusa:
	setvar VAR_TEMP_F, 1
	warp MAP_ELEUSA_VILLAGE, 27, 35
	waitstate
	end

	test_header AmphoraLeads_SpotHeader, AmphoraLeads_Spot
AmphoraLeads_Spot:
	setvar VAR_TEMP_F, 1
	warp MAP_ELEUSA_VILLAGE, 37, 33
	waitstate
	end

	test_header AmphoraLeads_HollowHeader, AmphoraLeads_Hollow
AmphoraLeads_Hollow:
	setvar VAR_TEMP_F, 1
	warp MAP_HECATES_HOLLOW, 7, 6
	waitstate
	end

	test_header AmphoraLeads_AkademiaHeader, AmphoraLeads_Akademia
AmphoraLeads_Akademia:
	setvar VAR_TEMP_F, 1
	warp MAP_ELAIA_VILLAGE_AKADEMIA, 13, 4
	waitstate
	end

	test_header AmphoraLeads_HoldHeader, AmphoraLeads_Hold
AmphoraLeads_Hold:
	setvar VAR_TEMP_F, 1
	special Ichor_HoldTimeOfDay
	end

	test_header AmphoraLeads_ClockHeader, AmphoraLeads_Clock
AmphoraLeads_Clock:
	setvar VAR_TEMP_F, 1
	special Ichor_ReleaseTimeOfDay
	callnative AmphoraLeads_SetClock
	end

	test_header AmphoraLeads_HeldClockHeader, AmphoraLeads_HeldClock
AmphoraLeads_HeldClock:
	lockall
	setvar VAR_TEMP_F, 1
	special Ichor_ReleaseTimeOfDay
	callnative AmphoraLeads_SetClock
	delay 180
	releaseall
	end

	test_header AmphoraLeads_StrongHeader, AmphoraLeads_Strong
AmphoraLeads_Strong:
	setvar VAR_TEMP_F, 1
	createmon 0, 0, SPECIES_SNIVY, 5, move1=MOVE_SHADOW_BALL, move2=MOVE_LEER, move3=MOVE_NONE, move4=MOVE_NONE
	end

	test_header AmphoraLeads_WeakHeader, AmphoraLeads_Weak
AmphoraLeads_Weak:
	setvar VAR_TEMP_F, 1
	callnative ZeroPlayerPartyMons
	givemon SPECIES_CLEFFA, 1
	createmon 0, 0, SPECIES_CLEFFA, 1, move1=MOVE_SPLASH, move2=MOVE_LEER, move3=MOVE_NONE, move4=MOVE_NONE
	end

	test_header AmphoraLeads_SaveHeader, AmphoraLeads_Save
AmphoraLeads_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end

	.thumb
	.align 2
	.thumb_func
AmphoraLeads_SetClock:
	push {r4, lr}
	ldr r0, =gLocalTime
	movs r1, #0
	ldrsh r0, [r0, r1]
	ldr r1, =gSpecialVar_0x8004
	ldrh r1, [r1]
	ldr r2, =gSpecialVar_0x8005
	ldrh r2, [r2]
	ldr r3, =gSpecialVar_0x8006
	ldrh r3, [r3]
	bl RtcCalcLocalTimeOffset
	ldr r0, =gTimeUpdateCounter
	movs r1, #0
	strh r1, [r0]
	pop {r4, pc}
