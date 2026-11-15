@ Test-only event scripts for tools/ichor/tests/theoxenia_sprites.lua. Never
@ linked into the ROM: engine_build.sh assembles this file with the game's own
@ macros and links it into spare EWRAM against pokeemerald.elf. Each header's
@ ON_FRAME entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/map_scripts.h"
#include "constants/vars.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"

	.set MAP_OFFSET,      7      @ include/fieldmap.h
	.set LOCALID_SAM,     0x50
	.set LOCALID_APOLLO,  0x51
	.set LOCALID_CAMI,    0x52
	.set LOCALID_DEMETER, 0x53

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

	@ spawn one object: graphics, movement type, local id, offset from the player
	.macro spawn gfx:req, type:req, id:req, dx:req, dy:req
	getplayerxy VAR_0x8007, VAR_0x8008
	addvar VAR_0x8007, \dx
	addvar VAR_0x8008, \dy
	setvar VAR_0x8004, \gfx
	setvar VAR_0x8005, \type
	setvar VAR_0x8006, \id
	callnative Theox_Spawn
	.endm

@ --- 1. Place the four: Sam and Apollo facing down, Cami facing up (seated on
@ her bench), Demeter facing down, in a row above the player. ----------------
	test_header Theox_SpawnHeader, Theox_Spawn_Script
Theox_Spawn_Script:
	lockall
	setvar VAR_TEMP_F, 1
	spawn OBJ_EVENT_GFX_ICHOR_SAM, MOVEMENT_TYPE_FACE_DOWN, LOCALID_SAM, -2, -2
	spawn OBJ_EVENT_GFX_ICHOR_APOLLO, MOVEMENT_TYPE_FACE_DOWN, LOCALID_APOLLO, -1, -2
	spawn OBJ_EVENT_GFX_ICHOR_CAMI, MOVEMENT_TYPE_FACE_UP, LOCALID_CAMI, 1, -2
	spawn OBJ_EVENT_GFX_ICHOR_DEMETER, MOVEMENT_TYPE_FACE_DOWN, LOCALID_DEMETER, 2, -2
	releaseall
	end

@ --- 2. Sam strums: nurse_joy_bow plays ANIM_ICHOR_STRUM and waits for its end
	test_header Theox_StrumHeader, Theox_Strum_Script
Theox_Strum_Script:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8000, 0
	applymovement LOCALID_SAM, Theox_Movement_Bow
	waitmovement LOCALID_SAM
	setvar VAR_0x8000, 1
	releaseall
	end

@ --- 3. Apollo strums the gold lyre the same way --------------------------------
	test_header Theox_ApolloHeader, Theox_Apollo_Script
Theox_Apollo_Script:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8000, 0
	applymovement LOCALID_APOLLO, Theox_Movement_Bow
	waitmovement LOCALID_APOLLO
	setvar VAR_0x8000, 1
	releaseall
	end

@ --- 4. Cami rises from the bench: ANIM_ICHOR_RISE, left facing down ----------
	test_header Theox_RiseHeader, Theox_Rise_Script
Theox_Rise_Script:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8001, 0
	applymovement LOCALID_CAMI, Theox_Movement_Bow
	waitmovement LOCALID_CAMI
	setvar VAR_0x8001, 1
	releaseall
	end

@ --- 5. face_up sits her down again -------------------------------------------
	test_header Theox_SitHeader, Theox_Sit_Script
Theox_Sit_Script:
	lockall
	setvar VAR_TEMP_F, 1
	applymovement LOCALID_CAMI, Theox_Movement_FaceUp
	waitmovement LOCALID_CAMI
	releaseall
	end

Theox_Movement_Bow:
	nurse_joy_bow
	step_end

Theox_Movement_FaceUp:
	face_up
	step_end

@ --- Native: spawn an object event on the current map ---------------------------
@ void Theox_Spawn(struct ScriptContext *ctx): graphics from VAR_0x8004,
@ movement type VAR_0x8005, local id VAR_0x8006, map x and y from VAR_0x8007
@ and VAR_0x8008, elevation 3, through SpawnSpecialObjectEventParameterized
@ (which takes coordinates with MAP_OFFSET added).
	.thumb
	.align 2
	.thumb_func
	.global Theox_Spawn
Theox_Spawn:
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
	bl Theox_CallR4
	add sp, #8
	pop {r4, r5}
	pop {r0}
	bx r0

	.thumb_func
Theox_CallR4:
	bx r4

	.align 2
	.pool
