@ Test-only event scripts for tools/ichor/tests/oikoumene_ow_sprites.lua. Never
@ linked into the ROM: engine_build.sh assembles this file with the game's own
@ macros and links it into spare EWRAM against pokeemerald.elf. Each header's
@ ON_FRAME entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/pokemon.h"
#include "constants/species.h"
#include "constants/vars.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"

	.set MAP_OFFSET, 7      @ include/fieldmap.h
	.set FIRST_ID,   0x40   @ the walkers' local ids, FIRST_ID upwards
	.set LAST_ID,    0x4C

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

@ --- A lead Pokémon, so a follower walks with the player ------------------------
	test_header OikOw_PartyHeader, OikOw_Party
OikOw_Party:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIKACHU, 10
	releaseall
	end

@ --- Akti, by the Agora: VAR_0x8007, VAR_0x8008 are the player's tile -----------
	test_header OikOw_AktiHeader, OikOw_Akti
OikOw_Akti:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_AKTI_TOWN, VAR_0x8007, VAR_0x8008
	waitstate
	releaseall
	end

@ --- Clear Akti's own people and props (local ids 1-20) ------------------------
	test_header OikOw_ClearHeader, OikOw_Clear
OikOw_Clear:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8006, 1
OikOw_Clear_Loop:
	removeobject VAR_0x8006
	addvar VAR_0x8006, 1
	goto_if_le VAR_0x8006, 20, OikOw_Clear_Loop
	releaseall
	end

@ --- Spawn one walker: graphics VAR_0x8004, local id VAR_0x8006, map tile -----
@ (VAR_0x8007, VAR_0x8008), facing down. -----------------------------------------
	test_header OikOw_SpawnHeader, OikOw_SpawnOne
OikOw_SpawnOne:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8005, MOVEMENT_TYPE_FACE_DOWN
	callnative OikOw_Spawn
	releaseall
	end

@ --- Remove the walker with local id VAR_0x8006 --------------------------------
	test_header OikOw_RemoveHeader, OikOw_Remove
OikOw_Remove:
	lockall
	setvar VAR_TEMP_F, 1
	removeobject VAR_0x8006
	releaseall
	end

@ --- One step for every walker present; VAR_0x8000 is 1 once all have landed --
	.macro step_all name:req, movement:req
	test_header \name\()Header, \name
\name:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8000, 0
	setvar VAR_0x8006, FIRST_ID
\name\()_Apply:
	applymovement VAR_0x8006, \movement
	addvar VAR_0x8006, 1
	goto_if_le VAR_0x8006, LAST_ID, \name\()_Apply
	setvar VAR_0x8006, FIRST_ID
\name\()_Wait:
	waitmovement VAR_0x8006
	addvar VAR_0x8006, 1
	goto_if_le VAR_0x8006, LAST_ID, \name\()_Wait
	setvar VAR_0x8000, 1
	releaseall
	end
	.endm

	step_all OikOw_WalkLeft, OikOw_Movement_Left
	step_all OikOw_WalkDown, OikOw_Movement_Down
	step_all OikOw_WalkRight, OikOw_Movement_Right
	step_all OikOw_WalkUp, OikOw_Movement_Up
	step_all OikOw_FaceDown, OikOw_Movement_FaceDown

@ Two tiles each way: one step shows one walk frame, the next the other.
OikOw_Movement_Left:
	walk_left
	walk_left
	step_end
OikOw_Movement_Down:
	walk_down
	walk_down
	step_end
OikOw_Movement_Right:
	walk_right
	walk_right
	step_end
OikOw_Movement_Up:
	walk_up
	walk_up
	step_end
OikOw_Movement_FaceDown:
	face_down
	step_end

@ --- Native: spawn an object event on the current map ---------------------------
@ void OikOw_Spawn(struct ScriptContext *ctx): graphics from VAR_0x8004,
@ movement type VAR_0x8005, local id VAR_0x8006, map x and y from VAR_0x8007
@ and VAR_0x8008, elevation 3, through SpawnSpecialObjectEventParameterized
@ (which takes coordinates with MAP_OFFSET added). As theoxenia_sprites_setup.s.
	.thumb
	.align 2
	.thumb_func
	.global OikOw_Spawn
OikOw_Spawn:
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
	bl OikOw_CallR4
	add sp, #8
	pop {r4, r5}
	pop {r0}
	bx r0

	.thumb_func
OikOw_CallR4:
	bx r4

	.align 2
	.pool
