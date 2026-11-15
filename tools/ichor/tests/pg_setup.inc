@ Shared test-only event scripts for the post-game headless checks
@ (tools/ichor/tests/pg_lib.lua). Never linked into the ROM. Each post-game check
@ (its pg_<area>_setup.s) pulls this in with
@     #include "tools/ichor/tests/pg_setup.inc"
@ after its .include lines (cpp expands the constants here), then adds its own
@ headers with the test_header macro defined below. Each header ON_FRAME entry
@ runs once while VAR_TEMP_F is 0 (L.runHeader in engine_lib.lua).

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

@ --- The post-game, ready: a Lv 70 party of six, every relic, the ship, the
@ clock started, the slice scenes quiet, then Akti at (VAR_0x8008, VAR_0x8009) --
	test_header PgLib_SetupHeader, PgLib_Setup
PgLib_Setup:
	lockall
	setvar VAR_TEMP_F, 1
	call PgLib_Party
	call PgLib_Relics
	setflag FLAG_ICHOR_POSTGAME
	setflag FLAG_ICHOR_GOT_EUPLOIA
	setflag FLAG_SYS_POKEMON_GET
	setflag FLAG_SYS_POKEDEX_GET
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
	setflag FLAG_ICHOR_ARRIVED_AKTI
	setflag FLAG_ICHOR_VISITED_AKTI
	setflag FLAG_ICHOR_HEARTH_TRIAL_DONE
	setflag FLAG_ICHOR_SLICE_COMPLETE
	setflag FLAG_ICHOR_HIDE_KLEON_AKTI
	setflag FLAG_ICHOR_HIDE_ALETHEA_AKTI
	setflag FLAG_BADGE01_GET
	setflag FLAG_SYS_CLOCK_SET
	dotimebasedevents
	setvar VAR_REPEL_STEP_COUNT, 999
	warpsilent MAP_AKTI_TOWN, VAR_0x8008, VAR_0x8009
	waitstate
	releaseall
	end

PgLib_Party:
	givemon SPECIES_LAPRAS, 70
	givemon SPECIES_ARCANINE, 70
	givemon SPECIES_VENUSAUR, 70
	givemon SPECIES_ALAKAZAM, 70
	givemon SPECIES_MACHAMP, 70
	givemon SPECIES_STARMIE, 70
	return

PgLib_Relics:
	additem ITEM_TALARIA
	additem ITEM_BRONZE_HAMMER
	additem ITEM_HECATES_TORCH
	additem ITEM_DEMETERS_SICKLE
	additem ITEM_GIRDLE_OF_HERAKLES
	additem ITEM_POSEIDONS_CONCH
	additem ITEM_DAEDALUS_WINGS
	additem ITEM_HORN_OF_ACHELOUS
	additem ITEM_ARIADNES_THREAD
	additem ITEM_LABRYS
	additem ITEM_HELM_OF_DARKNESS
	additem ITEM_NEREID_PEARL
	additem ITEM_AEOLUS_BAG
	setflag FLAG_SYS_B_DASH
	return

@ --- A new day: the time-based events, after the Lua has turned the clock ----
	test_header PgLib_DayHeader, PgLib_Day
PgLib_Day:
	lockall
	setvar VAR_TEMP_F, 1
	dotimebasedevents
	releaseall
	end

@ --- Save the game (the Lua answers the prompts) -------------------------------
	test_header PgLib_SaveHeader, PgLib_Save
PgLib_Save:
	lockall
	setvar VAR_TEMP_F, 1
	special SaveGame
	releaseall
	end
