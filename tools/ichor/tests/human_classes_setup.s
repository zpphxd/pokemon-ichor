@ Test-only real graphics-ID movement and trainer-loader gallery in spare EWRAM.
#include "config/general.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/map_scripts.h"
#include "constants/vars.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"
	.text
	.align 2
	.macro header name:req, script:req
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

	header Humans_StageHeader, Humans_StageScript
Humans_StageScript:
	setvar VAR_TEMP_F, 1
	callnative Humans_Stage
	end

	header Humans_SpawnHeader, Humans_SpawnScript
Humans_SpawnScript:
	setvar VAR_TEMP_F, 1
	getplayerxy VAR_0x8007, VAR_0x8008
	subvar VAR_0x8007, 4
	addvar VAR_0x8008, 1
	callnative Humans_Spawn
	end

	header Humans_RemoveHeader, Humans_RemoveScript
Humans_RemoveScript:
	setvar VAR_TEMP_F, 1
	removeobject 0x50
	end

	.macro walk name:req, direction:req
	header Humans_\name\()Header, Humans_\name\()Script
Humans_\name\()Script:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8000, 0
	applymovement 0x50, Humans_\name\()Movement
	waitmovement 0
	setvar VAR_0x8000, 1
	releaseall
	end
Humans_\name\()Movement:
	face_\direction
	walk_in_place_slow_\direction
	walk_in_place_slow_\direction
	walk_in_place_slow_\direction
	walk_in_place_slow_\direction
	step_end
	.endm
	walk Down, down
	walk Up, up
	walk Left, left
	walk Right, right

	header Humans_BowHeader, Humans_BowScript
Humans_BowScript:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8000, 0
	applymovement 0x50, Humans_BowMovement
	waitmovement 0
	setvar VAR_0x8000, 1
	releaseall
	end
Humans_BowMovement:
	face_down
	nurse_joy_bow
	delay_4
	step_end

	header Humans_FrontHeader, Humans_FrontScript
Humans_FrontScript:
	setvar VAR_TEMP_F, 1
	callnative Humans_Front
	end
	header Humans_FreeFrontHeader, Humans_FreeFrontScript
Humans_FreeFrontScript:
	setvar VAR_TEMP_F, 1
	callnative Humans_FreeFront
	end

	.thumb
	.align 2
	.thumb_func
Humans_Stage:
	push {r4, r5, lr}
	mov r0, #0
	ldr r1, =0x1040
	ldr r4, =SetGpuReg
	bl Humans_CallR4
	pop {r4, r5}
	pop {r0}
	bx r0
	.align 2
	.pool

	.thumb_func
Humans_Spawn:
	push {r4, r5, lr}
	sub sp, #8
	ldr r4, =gSpecialVar_0x8008
	ldrh r1, [r4]
	add r1, #7
	str r1, [sp]
	mov r1, #3
	str r1, [sp, #4]
	ldr r4, =gSpecialVar_0x8007
	ldrh r3, [r4]
	add r3, #7
	ldr r4, =gSpecialVar_0x8004
	ldrh r0, [r4]
	mov r1, #MOVEMENT_TYPE_FACE_DOWN
	mov r2, #0x50
	ldr r4, =SpawnSpecialObjectEventParameterized
	bl Humans_CallR4
	add sp, #8
	pop {r4, r5}
	pop {r0}
	bx r0
	.align 2
	.pool

	.thumb_func
Humans_Front:
	push {r4, r5, lr}
	sub sp, #8
	mov r0, #15
	str r0, [sp]
	ldr r0, =0xFFFF
	str r0, [sp, #4]
	ldr r4, =gSpecialVar_0x8004
	ldrh r0, [r4]
	mov r1, #1
	mov r2, #200
	mov r3, #80
	ldr r4, =CreateTrainerPicSprite
	bl Humans_CallR4
	ldr r4, =gSpecialVar_0x8005
	strh r0, [r4]
	add sp, #8
	pop {r4, r5}
	pop {r0}
	bx r0
	.align 2
	.pool

	.thumb_func
Humans_FreeFront:
	push {r4, r5, lr}
	ldr r4, =gSpecialVar_0x8005
	ldrh r0, [r4]
	ldr r4, =FreeAndDestroyTrainerPicSprite
	bl Humans_CallR4
	ldr r4, =gSpecialVar_0x8006
	strh r0, [r4]
	pop {r4, r5}
	pop {r0}
	bx r0
	.thumb_func
Humans_CallR4:
	mov r5, #1
	orr r4, r5
	bx r4
	.align 2
	.pool
