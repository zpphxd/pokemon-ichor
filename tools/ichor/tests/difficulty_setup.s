#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/map_scripts.h"
    .include "asm/macros.inc"
    .include "asm/macros/event.inc"
    .include "constants/constants.inc"
    .text
    .align 2
    .global DifficultyMenuHeader
DifficultyMenuHeader:
    map_script MAP_SCRIPT_ON_FRAME_TABLE, DifficultyMenuTable
    .byte 0
    .align 2
DifficultyMenuTable:
    map_script_2 VAR_TEMP_F, 0, DifficultyMenuScript
    .2byte 0
    .align 2
    .global DifficultyMenuScript
DifficultyMenuScript:
    lockall
    setvar VAR_TEMP_F, 1
    call ElaiaVillage_PlayersHouse_2F_EventScript_ChooseDifficulty
    copyvar VAR_0x8000, VAR_ICHOR_DIFFICULTY
    specialvar VAR_0x8001, Ichor_GetStepGlassLimit
    releaseall
    end

    .align 2
    .global DifficultySaveHeader
DifficultySaveHeader:
    map_script MAP_SCRIPT_ON_FRAME_TABLE, DifficultySaveTable
    .byte 0
    .align 2
DifficultySaveTable:
    map_script_2 VAR_TEMP_F, 0, DifficultySaveScript
    .2byte 0
    .align 2
    .global DifficultySaveScript
DifficultySaveScript:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end
