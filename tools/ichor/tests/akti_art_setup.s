@ Test-only EWRAM fixture linked against the selected ROM's ELF.
#include "config/general.h"
#include "constants/map_scripts.h"
#include "constants/vars.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"
	.text
	.align 2

	.macro header name:req, native:req
	.global \name
\name:
	map_script MAP_SCRIPT_ON_FRAME_TABLE, \name\()_Table
	.byte 0
	.align 2
\name\()_Table:
	map_script_2 VAR_TEMP_F, 0, \name\()_Script
	.2byte 0
\name\()_Script:
	lockall
	setvar VAR_TEMP_F, 1
	callnative \native
	releaseall
	end
	.align 2
	.endm

	header AktiArt_MonHeader, AktiArt_Mon
	header AktiArt_FrameHeader, AktiArt_Frame
	header AktiArt_FreeMonHeader, AktiArt_FreeMon
	header AktiArt_TrainerHeader, AktiArt_Trainer
	header AktiArt_FreeTrainerHeader, AktiArt_FreeTrainer

	.thumb
	.align 2
	.thumb_func
AktiArt_Mon:
	push {r4, r5, lr}
	sub sp, #16
	mov r0, #66
	str r0, [sp]
	mov r0, #60
	str r0, [sp, #4]
	mov r0, #14
	str r0, [sp, #8]
	ldr r0, =0xFFFF
	str r0, [sp, #12]
	ldr r4, =gSpecialVar_0x8000
	ldrh r0, [r4]
	ldr r4, =gSpecialVar_0x8001
	ldrh r1, [r4]
	mov r2, #0
	mov r3, #1
	ldr r4, =CreateMonPicSprite
	bl AktiArt_CallR4
	ldr r4, =gSpecialVar_0x8005
	strh r0, [r4]
	mov r0, #162
	str r0, [sp]
	mov r0, #15
	str r0, [sp, #8]
	ldr r4, =gSpecialVar_0x8000
	ldrh r0, [r4]
	ldr r4, =gSpecialVar_0x8001
	ldrh r1, [r4]
	mov r2, #0
	mov r3, #0
	ldr r4, =CreateMonPicSprite
	bl AktiArt_CallR4
	ldr r4, =gSpecialVar_0x8006
	strh r0, [r4]
	add sp, #16
	pop {r4, r5}
	pop {r0}
	bx r0

	.thumb_func
AktiArt_Frame:
	push {r4, lr}
	ldr r4, =gSpecialVar_0x8005
	ldrh r0, [r4]
	ldr r4, =gSpecialVar_0x8002
	ldrh r1, [r4]
	mul r0, r1
	ldr r4, =gSprites
	add r0, r4
	mov r1, #1
	ldr r4, =StartSpriteAnim
	bl AktiArt_CallR4
	pop {r4}
	pop {r0}
	bx r0

	.thumb_func
AktiArt_FreeMon:
	push {r4, lr}
	ldr r4, =gSpecialVar_0x8005
	ldrh r0, [r4]
	ldr r4, =FreeAndDestroyMonPicSprite
	bl AktiArt_CallR4
	ldr r4, =gSpecialVar_0x8006
	ldrh r0, [r4]
	ldr r4, =FreeAndDestroyMonPicSprite
	bl AktiArt_CallR4
	pop {r4}
	pop {r0}
	bx r0

	.thumb_func
AktiArt_Trainer:
	push {r4, r5, lr}
	sub sp, #8
	ldr r4, =gSpecialVar_0x8000
	ldrh r5, [r4]
	mov r0, #14
	str r0, [sp]
	ldr r0, =0xFFFF
	str r0, [sp, #4]
	mov r0, r5
	mov r1, #1
	mov r2, #120
	mov r3, #60
	ldr r4, =CreateTrainerPicSprite
	bl AktiArt_CallR4
	ldr r4, =gSpecialVar_0x8005
	strh r0, [r4]
	add sp, #8
	pop {r4, r5}
	pop {r0}
	bx r0

	.thumb_func
AktiArt_FreeTrainer:
	push {r4, lr}
	ldr r4, =gSpecialVar_0x8005
	ldrh r0, [r4]
	ldr r4, =FreeAndDestroyTrainerPicSprite
	bl AktiArt_CallR4
	pop {r4}
	pop {r0}
	bx r0

	.thumb_func
AktiArt_CallR4:
	push {r5}
	mov r5, #1
	orr r4, r5
	pop {r5}
	bx r4
	.align 2
	.pool
