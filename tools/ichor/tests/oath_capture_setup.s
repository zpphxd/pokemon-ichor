#include "constants/flags.h"
#include "constants/global.h"
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

	test_header Oath_SetupHeader, Oath_Setup
Oath_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_SNIVY, 80
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_ICHOR_GOT_STARTER
	setflag FLAG_ICHOR_TALKED_TO_MOM
	setflag FLAG_ICHOR_THREAD_READ
	setflag FLAG_ICHOR_KLEON_BATTLE_1_DONE
	setflag FLAG_ICHOR_ACT1_COMPLETE
	setvar VAR_REPEL_STEP_COUNT, 999
	giveitem ITEM_MASTER_BALL, 6
	callnative InitTimeBasedEvents
	warp MAP_ELAIA_VILLAGE_AKADEMIA, 13, 4
	waitstate
	releaseall
	end

	test_header Oath_BattleHeader, Oath_Battle
Oath_Battle:
	setvar VAR_TEMP_F, 1
	setwildbattle SPECIES_NEBREL, 3
	dowildbattle
	end

	test_header Oath_RouteHeader, Oath_Route
Oath_Route:
	setvar VAR_TEMP_F, 1
	warp MAP_KALLISTE_ROUTE1_KRONION_HILL, 13, 12
	waitstate
	end

	test_header Oath_SaveHeader, Oath_Save
Oath_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end

	test_header Oath_FaintHeader, Oath_Faint
Oath_Faint:
	setvar VAR_TEMP_F, 1
	callnative ZeroPlayerPartyMons
	givemon SPECIES_CLEFFA, 1
	createmon 0, 0, SPECIES_CLEFFA, 1, item=ITEM_POTION, move1=MOVE_SPLASH, move2=MOVE_LEER, move3=MOVE_NONE, move4=MOVE_NONE
	givemon SPECIES_SNIVY, 80
	setwildbattle SPECIES_ZIGZAGOON, 10
	dowildbattle
	end

	test_header Oath_HealHeader, Oath_Heal
Oath_Heal:
	setvar VAR_TEMP_F, 1
	special HealPlayerParty
	end

	test_header Oath_UrnHeader, Oath_Urn
Oath_Urn:
	setvar VAR_TEMP_F, 1
	callnative Oath_NameFixtureUrn
	end

	test_header Oath_PcHeader, Oath_Pc
Oath_Pc:
	setvar VAR_TEMP_F, 1
	special ShowPokemonStorageSystemPC
	end

	test_header Oath_ChoosePartnerHeader, Oath_ChoosePartner
Oath_ChoosePartner:
	setvar VAR_TEMP_F, 1
	special ChoosePartyMon
	end

	.thumb
	.align 2
	.thumb_func
Oath_NameFixtureUrn:
	push {lr}
	movs r0, #13
	bl GetBoxNamePtr
	ldr r1, =Oath_UrnName
	bl StringCopy
	pop {pc}

	.align 2
Oath_UrnName:
	.string "URN$"
	.pool
