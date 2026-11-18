@ Test-only event scripts for tools/ichor/tests/bag_overflow.lua and
@ bag_save.lua. Never linked into the ROM: engine_build.sh assembles this file
@ with the game's own macros and links it into spare EWRAM against the ELF.
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

	test_header BagOverflow_FindHeader, BagOverflow_Find
	test_header BagOverflow_GiftHeader, BagOverflow_Gift
	test_header BagOverflow_HiddenHeader, BagOverflow_Hidden
	test_header BagOverflow_MartHeader, BagOverflow_MartScript
	test_header BagOverflow_SaveHeader, BagOverflow_Save
	test_header BagOverflow_OldItemsHeader, BagOverflow_OldItems

@ An item ball: finditem, as every map's ground items use. No object of local
@ id 250 exists, so the removeobject in Std_FindItem does nothing.
BagOverflow_Find:
	setvar VAR_TEMP_F, 1
	setvar VAR_LAST_TALKED, 250
	finditem ITEM_POTION
	copyvar VAR_0x8000, VAR_RESULT
	end

@ A gift: giveitem, as every Ichor gift script does.
BagOverflow_Gift:
	setvar VAR_TEMP_F, 1
	lock
	giveitem ITEM_SUPER_POTION
	copyvar VAR_0x8000, VAR_RESULT
	release
	end

@ A hidden item, through the same script a bg_hidden_item_event runs.
BagOverflow_Hidden:
	setvar VAR_TEMP_F, 1
	setvar VAR_0x8004, FLAG_TEMP_1
	setvar VAR_0x8005, ITEM_ETHER
	setvar VAR_0x8009, 1
	goto EventScript_HiddenItemScript

BagOverflow_MartScript:
	setvar VAR_TEMP_F, 1
	lock
	pokemart BagOverflow_Mart
	release
	end

	.align 2
BagOverflow_Mart:
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_NONE

BagOverflow_Save:
	setvar VAR_TEMP_F, 1
	lockall
	special SaveGame
	releaseall
	end

@ bag_save.lua on the old ROM: something in every pocket, then a real save.
BagOverflow_OldItems:
	setvar VAR_TEMP_F, 1
	lockall
	additem ITEM_POTION, 7
	additem ITEM_REPEL, 3
	additem ITEM_POKE_BALL, 12
	additem ITEM_GREAT_BALL, 2
	additem ITEM_TM01, 1
	additem ITEM_ORAN_BERRY, 5
	additem ITEM_OLD_ROD, 1
	additem ITEM_ESCAPE_ROPE, 1
	special SaveGame
	releaseall
	end
