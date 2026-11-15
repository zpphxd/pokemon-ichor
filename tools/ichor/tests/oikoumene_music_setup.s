@ Test-only event scripts for tools/ichor/tests/oikoumene_music.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
#include "constants/global.h"
#include "constants/map_scripts.h"
#include "constants/songs.h"
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

@ One header per song: play it as a map script would, with playbgm.
	.macro play_song song:req
	test_header MusicTest_\song\()Header, MusicTest_\song
MusicTest_\song:
	setvar VAR_TEMP_F, 1
	playbgm \song, FALSE
	end
	.endm

	play_song MUS_ICHOR_WIDER_WORLD
	play_song MUS_ICHOR_PLAIN_OF_TROY
	play_song MUS_ICHOR_BLACK_LAND
	play_song MUS_ICHOR_NECROPOLIS
	play_song MUS_ICHOR_BLACK_SEA
	play_song MUS_ICHOR_BATTLE_OIKOUMENE
	play_song MUS_ICHOR_BATTLE_PERIODOS
	play_song MUS_ICHOR_PERIODOS_TROAD
	play_song MUS_ICHOR_PERIODOS_EGYPT
	play_song MUS_ICHOR_PERIODOS_PONTOS
