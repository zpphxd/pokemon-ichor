@ Test-only event scripts for tools/ichor/tests/pg_sprites.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/flags.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/vars.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"

	.set MAP_OFFSET, 7      @ include/fieldmap.h

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

	@ spawn one object at map (x, y): graphics, movement type, local id
	.macro spawn_at gfx:req, type:req, id:req, x:req, y:req
	setvar VAR_0x8007, \x
	setvar VAR_0x8008, \y
	setvar VAR_0x8004, \gfx
	setvar VAR_0x8005, \type
	setvar VAR_0x8006, \id
	callnative PgSpr_Spawn
	.endm

@ --- 1. Quiet slice flags, then Akti's harbor quay, by the open water --------
	test_header PgSpr_SetupHeader, PgSpr_Setup
PgSpr_Setup:
	lockall
	setvar VAR_TEMP_F, 1
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
	warpsilent MAP_AKTI_TOWN, 15, 9
	waitstate
	releaseall
	end

@ --- 2. Remove one object event: its address in VAR_0x8004 (low) and 0x8005 ---
	test_header PgSpr_RemoveHeader, PgSpr_Remove_Script
PgSpr_Remove_Script:
	lockall
	setvar VAR_TEMP_F, 1
	callnative PgSpr_Remove
	releaseall
	end

@ --- 3. The Euploia, sail full in the west basin and slack in the east water,
@ rowing in place to one heading --------------------------------------------
	.macro ships_header name:req, type:req
	test_header \name, \name\()_Script
\name\()_Script:
	lockall
	setvar VAR_TEMP_F, 1
	spawn_at OBJ_EVENT_GFX_ICHOR_EUPLOIA, \type, 0x50, 11, 8
	spawn_at OBJ_EVENT_GFX_ICHOR_EUPLOIA_SLACK, \type, 0x51, 19, 8
	releaseall
	end
	.endm

	ships_header PgSpr_ShipsDownHeader, MOVEMENT_TYPE_WALK_IN_PLACE_DOWN
	ships_header PgSpr_ShipsUpHeader, MOVEMENT_TYPE_WALK_IN_PLACE_UP
	ships_header PgSpr_ShipsLeftHeader, MOVEMENT_TYPE_WALK_IN_PLACE_LEFT
	ships_header PgSpr_ShipsRightHeader, MOVEMENT_TYPE_WALK_IN_PLACE_RIGHT

@ --- 4. The walkers in two rows of the quay, walking in place ----------------
	.macro crew_header name:req, type:req
	test_header \name, \name\()_Script
\name\()_Script:
	lockall
	setvar VAR_TEMP_F, 1
	spawn_at OBJ_EVENT_GFX_ICHOR_NOLAN, \type, 0x60, 8, 10
	spawn_at OBJ_EVENT_GFX_ICHOR_PHEMIOS, \type, 0x61, 10, 10
	spawn_at OBJ_EVENT_GFX_ICHOR_LYNKEUS, \type, 0x62, 12, 10
	spawn_at OBJ_EVENT_GFX_ICHOR_TRUCE_HERALD, \type, 0x63, 14, 10
	spawn_at OBJ_EVENT_GFX_ICHOR_ACHILLES, \type, 0x64, 20, 10
	spawn_at OBJ_EVENT_GFX_ICHOR_ODYSSEUS, \type, 0x65, 22, 10
	releaseall
	end
	.endm

	.macro olympia_header name:req, type:req
	test_header \name, \name\()_Script
\name\()_Script:
	lockall
	setvar VAR_TEMP_F, 1
	spawn_at OBJ_EVENT_GFX_ICHOR_HIPPOLYTA, \type, 0x66, 8, 10
	spawn_at OBJ_EVENT_GFX_ICHOR_ATALANTA, \type, 0x67, 10, 10
	spawn_at OBJ_EVENT_GFX_ICHOR_ARIADNE, \type, 0x68, 12, 10
	spawn_at OBJ_EVENT_GFX_ICHOR_OLYMPIAS, \type, 0x69, 14, 10
	spawn_at OBJ_EVENT_GFX_ICHOR_PAIONIOS, \type, 0x6A, 20, 10
	releaseall
	end
	.endm

	crew_header PgSpr_CrewDownHeader, MOVEMENT_TYPE_WALK_IN_PLACE_DOWN
	crew_header PgSpr_CrewUpHeader, MOVEMENT_TYPE_WALK_IN_PLACE_UP
	crew_header PgSpr_CrewLeftHeader, MOVEMENT_TYPE_WALK_IN_PLACE_LEFT
	crew_header PgSpr_CrewRightHeader, MOVEMENT_TYPE_WALK_IN_PLACE_RIGHT
	olympia_header PgSpr_OlympiaDownHeader, MOVEMENT_TYPE_WALK_IN_PLACE_DOWN
	olympia_header PgSpr_OlympiaUpHeader, MOVEMENT_TYPE_WALK_IN_PLACE_UP
	olympia_header PgSpr_OlympiaLeftHeader, MOVEMENT_TYPE_WALK_IN_PLACE_LEFT
	olympia_header PgSpr_OlympiaRightHeader, MOVEMENT_TYPE_WALK_IN_PLACE_RIGHT

@ --- Natives ------------------------------------------------------------------
@ void PgSpr_Spawn(struct ScriptContext *ctx): graphics from VAR_0x8004,
@ movement type VAR_0x8005, local id VAR_0x8006, map x and y from VAR_0x8007
@ and VAR_0x8008, elevation 3, through SpawnSpecialObjectEventParameterized
@ (which takes coordinates with MAP_OFFSET added).
	.thumb
	.align 2
	.thumb_func
	.global PgSpr_Spawn
PgSpr_Spawn:
	push {r4, r5, lr}
	sub sp, #8
	ldr r4, =gSpecialVar_0x8008
	ldrh r1, [r4]
	add r1, #MAP_OFFSET
	str r1, [sp]
	mov r1, #3
	str r1, [sp, #4]
	ldr r4, =gSpecialVar_0x8007
	ldrh r3, [r4]
	add r3, #MAP_OFFSET
	ldr r4, =gSpecialVar_0x8004
	ldrh r0, [r4]
	ldr r4, =gSpecialVar_0x8005
	ldrh r1, [r4]
	ldr r4, =gSpecialVar_0x8006
	ldrh r2, [r4]
	ldr r4, =SpawnSpecialObjectEventParameterized
	mov r5, #1
	orr r4, r5
	bl PgSpr_CallR4
	add sp, #8
	pop {r4, r5}
	pop {r0}
	bx r0

@ void PgSpr_Remove(struct ScriptContext *ctx): RemoveObjectEvent on the object
@ event whose address is VAR_0x8005:VAR_0x8004 (the Lua side finds it). This
@ skips removeobject's hide-flag lookup, which reads a template a spawned
@ object doesn't have.
	.thumb_func
	.global PgSpr_Remove
PgSpr_Remove:
	push {r4, r5, lr}
	ldr r4, =gSpecialVar_0x8004
	ldrh r0, [r4]
	ldr r4, =gSpecialVar_0x8005
	ldrh r1, [r4]
	lsl r1, r1, #16
	orr r0, r1
	ldr r4, =RemoveObjectEvent
	mov r5, #1
	orr r4, r5
	bl PgSpr_CallR4
	pop {r4, r5}
	pop {r0}
	bx r0

	.thumb_func
PgSpr_CallR4:
	bx r4

	.align 2
	.pool
