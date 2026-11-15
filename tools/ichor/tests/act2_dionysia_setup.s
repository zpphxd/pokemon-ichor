@ Test-only event scripts for tools/ichor/tests/act2_dionysia.lua. Never linked
@ into the ROM: engine_build.sh assembles this file with the game's own macros
@ and links it into spare EWRAM against pokeemerald.elf. Each header's ON_FRAME
@ entry runs once while VAR_TEMP_F is 0 (engine_lib.lua's L.runHeader).
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

@ --- A save from just after the Three-Act Play: the Mask Laurel won ----------
@ Act I done and Act II up to the temple's trial; a Kynder starter (Kleon's
@ third team is then KLEON_3_KYNDER); a level-100 test Pokémon whose one move
@ (Flamethrower) no foe in these scenes is immune to. The eighth badge keeps it
@ obedient (the expansion's obedience goes by level met). Then in through the
@ theater's top gate, warp 0, as from Thyrsa.
	test_header Dionysia_SetupHeader, Dionysia_Setup
Dionysia_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	givemon SPECIES_MEWTWO, 100, move1=MOVE_FLAMETHROWER, move2=MOVE_NONE, move3=MOVE_NONE, move4=MOVE_NONE
	setvar VAR_STARTER_MON, 1
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
	setflag FLAG_SYS_B_DASH
	setflag FLAG_BADGE01_GET
	setflag FLAG_BADGE02_GET
	setflag FLAG_BADGE03_GET
	setflag FLAG_BADGE04_GET
	setflag FLAG_BADGE08_GET
	setflag FLAG_ICHOR_ACT2_BEGUN
	setflag FLAG_ICHOR_ARRIVED_THYRSA
	setflag FLAG_ICHOR_VISITED_THYRSA
	setflag FLAG_ICHOR_THREE_ACT_PLAY_DONE
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_THYRSA_THEATER, 0
	waitstate
	releaseall
	end
