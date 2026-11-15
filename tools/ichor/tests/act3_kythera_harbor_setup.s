@ Test-only event scripts for act3_kythera_harbor.sh. Never linked into the ROM:
@ engine_build.sh assembles this file with the game's own macros and links it
@ into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME entry runs
@ once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
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

@ --- Act II's end state: Kydippe's letter read, VAR_ICHOR_ACT3 still 0. Two
@ level-100 Metagross that obey (the eighth badge), a long Repel so the walks
@ through the barley aren't interrupted, then the southern deck, where Act II's
@ Kaldera will warp the player (12,6). The boarding scene plays on arrival.
	test_header Act3Harbor_StartHeader, Act3Harbor_Start
Act3Harbor_Start:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_METAGROSS, 100, move1=MOVE_IRON_HEAD
	givemon SPECIES_METAGROSS, 100, move1=MOVE_IRON_HEAD
	setflag FLAG_BADGE08_GET
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_B_DASH
	setvar VAR_ICHOR_ACT3, 0
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_TRIREME_EUPLOIA_DECK_SOUTH, 12, 6
	waitstate
	releaseall
	end
