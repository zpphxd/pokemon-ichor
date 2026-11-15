@ Test-only event scripts for tools/ichor/tests/ichor_relics.lua. Never linked
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

@ --- A Pokémon that knows Cut and Surf, quiet slice flags, then Route 1's
@ open patch at (VAR_0x8008, VAR_0x8009) ---------------------------------------
	test_header RelicTest_SetupHeader, RelicTest_Setup
RelicTest_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_PIPLUP, 30, move1=MOVE_CUT, move2=MOVE_SURF, move3=MOVE_STRENGTH, move4=MOVE_ROCK_SMASH
	setflag FLAG_BADGE08_GET
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

@ --- Party check: the unlocked-field-move check for Cut and Surf fails even
@ though the Pokémon knows both. VAR_0x8000 = 1 per check that held. ---------
	test_header RelicTest_FieldMovesHeader, RelicTest_FieldMoves
RelicTest_FieldMoves:
	lockall
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8000, 0
	checkfieldmove FIELD_MOVE_CUT, TRUE
	goto_if_ne VAR_RESULT, PARTY_SIZE, RelicTest_FieldMoves_1
	addvar VAR_0x8000, 1
RelicTest_FieldMoves_1:
	checkfieldmove FIELD_MOVE_SURF, TRUE
	goto_if_ne VAR_RESULT, PARTY_SIZE, RelicTest_FieldMoves_2
	addvar VAR_0x8000, 1
RelicTest_FieldMoves_2:
	checkfieldmove FIELD_MOVE_CUT, FALSE
	goto_if_eq VAR_RESULT, PARTY_SIZE, RelicTest_FieldMoves_3
	addvar VAR_0x8000, 1
RelicTest_FieldMoves_3:
	releaseall
	end

@ --- Give the item in VAR_0x8004 (the engine sets its relic flag) ----------------
	test_header RelicTest_GiveHeader, RelicTest_Give
RelicTest_Give:
	lockall
	setvar VAR_TEMP_F, 1
	additem VAR_0x8004, 1
	releaseall
	end

@ --- Respawn the template with local id VAR_0x8008 (the Lua rewrote it) ---------
	test_header RelicTest_SpawnHeader, RelicTest_Spawn
RelicTest_Spawn:
	lockall
	setvar VAR_TEMP_F, 1
	removeobject VAR_0x8008
	addobject VAR_0x8008
	releaseall
	end

@ --- Recompute the light for this map (after the Lua sets the cave bit) ---------
	test_header RelicTest_FlashHeader, RelicTest_Flash
RelicTest_Flash:
	lockall
	setvar VAR_TEMP_F, 1
	callnative RelicTest_DefaultFlashLevel
	releaseall
	end

@ --- Fog on this map --------------------------------------------------------------
	test_header RelicTest_FogHeader, RelicTest_Fog
RelicTest_Fog:
	lockall
	setvar VAR_TEMP_F, 1
	setweather WEATHER_FOG_HORIZONTAL
	doweather
	releaseall
	end

@ --- Warp back to (VAR_0x8008, VAR_0x8009) on Route 1, on foot ------------------
	test_header RelicTest_WarpHeader, RelicTest_Warp
RelicTest_Warp:
	lockall
	setvar VAR_TEMP_F, 1
	warpsilent MAP_KALLISTE_ROUTE1, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

@ --- SetDefaultFlashLevel, rebuilt here: LTO inlines the game's own copy away ----
@ The light on a map load: none on a lit map, else the Torch's radius.
	.thumb
	.align 2
	.thumb_func
	.global RelicTest_DefaultFlashLevel
RelicTest_DefaultFlashLevel:
	push {lr}
	ldr r0, =gMapHeader
	ldrb r0, [r0, #0x1A]          @ the cave bit is bit 5 of this byte
	lsl r0, r0, #26
	bpl RelicTest_DefaultFlashLevel_Lit
	ldr r3, =Ichor_GetTorchFlashLevel
	bl RelicTest_CallR3
	b RelicTest_DefaultFlashLevel_Set
RelicTest_DefaultFlashLevel_Lit:
	mov r0, #0
RelicTest_DefaultFlashLevel_Set:
	ldr r3, =SetFlashLevel
	bl RelicTest_CallR3
	pop {r0}
	bx r0
RelicTest_CallR3:
	bx r3
	.pool


@ --- Carried flames: take one (VAR_0x8004 kind, VAR_0x8005 steps), a draught, a douse
	.arm
	.align 2
@ --- A lit zone's threshold, going in (VAR_0x8004 = the zone's brazier flag) and out
	test_header RelicTest_EnterLitHeader, RelicTest_EnterLit
RelicTest_EnterLit:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorEnterLitZone

	test_header RelicTest_LeaveLitHeader, RelicTest_LeaveLit
RelicTest_LeaveLit:
	setvar VAR_TEMP_F, 1
	goto EventScript_IchorLeaveLitZone

	test_header RelicTest_TakeFlameHeader, RelicTest_TakeFlame
RelicTest_TakeFlame:
	setvar VAR_TEMP_F, 1
	special Ichor_TakeFlame
	end

	test_header RelicTest_DraughtHeader, RelicTest_Draught
RelicTest_Draught:
	setvar VAR_TEMP_F, 1
	call EventScript_IchorDraught
	end

	test_header RelicTest_DouseHeader, RelicTest_Douse
RelicTest_Douse:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, 1
	special Ichor_SetTorchDoused
	setvar VAR_0x8004, 0
	special Ichor_SetTorchDoused
	end
