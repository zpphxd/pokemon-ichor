@ Test-only event scripts for act3_galatea_gallery.sh. Never linked into the ROM:
@ engine_build.sh assembles this file with the game's own macros and links it into
@ spare EWRAM against pokeemerald.elf. Each header's ON_FRAME entry runs once while
@ VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/flags.h"
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

@ Native low-met-level creation; Lua applies the existing level assist.
	test_header Gallery_GiveHeader, Gallery_Give
Gallery_Give:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_METAGROSS, 5, move1=MOVE_IRON_HEAD
	givemon SPECIES_METAGROSS, 5, move1=MOVE_IRON_HEAD
	setvar VAR_ICHOR_ACT3, 2
	releaseall
	end

@ Into the temple at (VAR_0x8008, VAR_0x8009), healed.
	test_header Gallery_WarpHeader, Gallery_Warp
Gallery_Warp:
	lockall
	setvar VAR_TEMP_F, 1
	special HealPlayerParty
	warpsilent MAP_KYTHERA_TEMPLE_OF_APHRODITE, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end
