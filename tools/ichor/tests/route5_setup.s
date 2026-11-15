@ Test-only event scripts for tools/ichor/tests/route5.lua. Never linked into
@ the ROM: engine_build.sh assembles this file with the game's own macros and
@ links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/ichor.h"
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

@ --- The bag and the party for the walk, then out of the Hollow's west mouth --
@ The road's player has come from Emporion and through the Hollow: the Bronze
@ Hammer (beat 13), oil for the herms (Kerykos, beat 11), the Old Rod from Akti,
@ and an Onotis to trade at the inn. The warp lands on the mouth's door tile,
@ and the game walks the player out of it, as a warp from the Hollow does.
	test_header Route5Test_SetupHeader, Route5Test_Setup
Route5Test_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_ONOTIS, 18
	giveitem ITEM_BRONZE_HAMMER, 1
	giveitem ITEM_OLIVE_OIL, 3
	giveitem ITEM_OLD_ROD, 1
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_BADGE01_GET
	setflag FLAG_BADGE02_GET
	warp MAP_ROUTE5_SKIRONIAN_CLIFFS, 9, 8
	waitstate
	releaseall
	end
