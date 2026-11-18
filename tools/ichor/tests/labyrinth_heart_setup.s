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
#include "constants/opponents.h"
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

@ The player as they come down from Ring IV (LABYRINTH.md, beat III-3J): strong
@ Pokémon, every relic the heart asks for, Enkelados's checkpoint behind them.
@ Asterion is set aside (FLAG_ICHOR_ASTERION_FREED hides him) so the walk through the
@ heart's puzzles is deterministic; tools/ichor/tests/ichor_labyrinth.sh tests his AI.
    test_header Heart_SetupHeader, Heart_Setup
Heart_Setup:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_MEWTWO, 60, move1=MOVE_SURF, move2=MOVE_ICE_BEAM, move3=MOVE_THUNDER, move4=MOVE_CALM_MIND
    givemon SPECIES_MEWTWO, 60, move1=MOVE_PSYSTRIKE, move2=MOVE_AURA_SPHERE, move3=MOVE_ICE_BEAM, move4=MOVE_RECOVER
    givemon SPECIES_METAGROSS, 60, move1=MOVE_IRON_HEAD, move2=MOVE_EARTHQUAKE, move3=MOVE_ZEN_HEADBUTT, move4=MOVE_BULLET_PUNCH
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_BADGE06_GET
    setflag FLAG_BADGE07_GET
    additem ITEM_HECATES_TORCH
    additem ITEM_ARIADNES_THREAD
    additem ITEM_POSEIDONS_CONCH
    additem ITEM_BRONZE_HAMMER
    additem ITEM_DEMETERS_SICKLE
    additem ITEM_GIRDLE_OF_HERAKLES
    additem ITEM_LABRYS
    additem ITEM_HELM_OF_DARKNESS
    setvar VAR_REPEL_STEP_COUNT, 999
    setflag FLAG_ICHOR_ASTERION_FREED
    setflag FLAG_ICHOR_HIDE_SENTRY_1
    setflag FLAG_ICHOR_HIDE_SENTRY_2
    setflag FLAG_ICHOR_HIDE_SENTRY_3
    settrainerflag TRAINER_ICHOR_SMYRIS
    setvar VAR_ICHOR_KNOSSA, 9
    warp MAP_LABYRINTH_RING5, 0
    waitstate
    releaseall
    end

@ A full heal between the heart's boss fights (the bot fights with one move and never switches).
    test_header Heart_HealHeader, Heart_Heal
Heart_Heal:
    lockall
    setvar VAR_TEMP_F, 1
    special HealPlayerParty
    releaseall
    end
