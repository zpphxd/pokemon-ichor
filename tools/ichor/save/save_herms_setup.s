#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/flags.h"
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

	test_header SaveHerms_SaveHeader, SaveHerms_Save
SaveHerms_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end

@ Adds the HM for every relic in the Bag (Ichor_EventScript_GiveRelicMoves, without its text), then saves.
	test_header SaveHerms_RelicMovesHeader, SaveHerms_RelicMoves
SaveHerms_RelicMoves:
	lockall
	setvar VAR_TEMP_F, 1
	checkitem ITEM_BRONZE_HAMMER, 1
	goto_if_eq VAR_RESULT, FALSE, SaveHerms_RelicMoves_0
	checkitem ITEM_HM_ROCK_SMASH, 1
	goto_if_eq VAR_RESULT, TRUE, SaveHerms_RelicMoves_0
	additem ITEM_HM_ROCK_SMASH, 1
SaveHerms_RelicMoves_0:
	checkitem ITEM_HECATES_TORCH, 1
	goto_if_eq VAR_RESULT, FALSE, SaveHerms_RelicMoves_1
	checkitem ITEM_HM_FLASH, 1
	goto_if_eq VAR_RESULT, TRUE, SaveHerms_RelicMoves_1
	additem ITEM_HM_FLASH, 1
SaveHerms_RelicMoves_1:
	checkitem ITEM_DEMETERS_SICKLE, 1
	goto_if_eq VAR_RESULT, FALSE, SaveHerms_RelicMoves_2
	checkitem ITEM_HM_CUT, 1
	goto_if_eq VAR_RESULT, TRUE, SaveHerms_RelicMoves_2
	additem ITEM_HM_CUT, 1
SaveHerms_RelicMoves_2:
	checkitem ITEM_GIRDLE_OF_HERAKLES, 1
	goto_if_eq VAR_RESULT, FALSE, SaveHerms_RelicMoves_3
	checkitem ITEM_HM_STRENGTH, 1
	goto_if_eq VAR_RESULT, TRUE, SaveHerms_RelicMoves_3
	additem ITEM_HM_STRENGTH, 1
SaveHerms_RelicMoves_3:
	checkitem ITEM_POSEIDONS_CONCH, 1
	goto_if_eq VAR_RESULT, FALSE, SaveHerms_RelicMoves_4
	checkitem ITEM_HM_SURF, 1
	goto_if_eq VAR_RESULT, TRUE, SaveHerms_RelicMoves_4
	additem ITEM_HM_SURF, 1
SaveHerms_RelicMoves_4:
	checkitem ITEM_DAEDALUS_WINGS, 1
	goto_if_eq VAR_RESULT, FALSE, SaveHerms_RelicMoves_5
	checkitem ITEM_HM_FLY, 1
	goto_if_eq VAR_RESULT, TRUE, SaveHerms_RelicMoves_5
	additem ITEM_HM_FLY, 1
SaveHerms_RelicMoves_5:
	checkitem ITEM_HORN_OF_ACHELOUS, 1
	goto_if_eq VAR_RESULT, FALSE, SaveHerms_RelicMoves_6
	checkitem ITEM_HM_WATERFALL, 1
	goto_if_eq VAR_RESULT, TRUE, SaveHerms_RelicMoves_6
	additem ITEM_HM_WATERFALL, 1
SaveHerms_RelicMoves_6:
	checkitem ITEM_NEREID_PEARL, 1
	goto_if_eq VAR_RESULT, FALSE, SaveHerms_RelicMoves_7
	checkitem ITEM_HM_DIVE, 1
	goto_if_eq VAR_RESULT, TRUE, SaveHerms_RelicMoves_7
	additem ITEM_HM_DIVE, 1
SaveHerms_RelicMoves_7:
	special SaveGame
	releaseall
	end
