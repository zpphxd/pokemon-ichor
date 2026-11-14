// Constants and struct offsets for tools/ichor/tests/temple_trial.lua.
// temple_trial.sh compiles this with the game's own headers (gcc -S) and turns each
// k_NAME into a Lua table entry, so the test never hardcodes an id or an offset.
#include "global.h"
#include "main.h"
#include "fieldmap.h"
#include "constants/battle.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/map_scripts.h"
#include "constants/moves.h"
#include "constants/opponents.h"
#include "constants/script_commands.h"
#include "constants/species.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

// Where the test goes and what it reads.
K(MAP_TEMPLE, MAP_AKTI_TOWN_TEMPLE_OF_HESTIA)
K(MAP_AKTI, MAP_AKTI_TOWN)
K(VAR_HEARTH_TRIAL, VAR_ICHOR_HEARTH_TRIAL)
K(VAR_TEMP_0, VAR_TEMP_0)
K(VARS_START, VARS_START)
K(FLAG_TRIAL_DONE, FLAG_ICHOR_HEARTH_TRIAL_DONE)
K(FLAG_GOT_CHARCOAL, FLAG_ICHOR_GOT_CHARCOAL)
K(FLAG_GOT_TM_FACADE, FLAG_ICHOR_GOT_TM_FACADE)
K(FLAG_BADGE01_GET, FLAG_BADGE01_GET)
K(FLAG_BADGE08_GET, FLAG_BADGE08_GET)
K(FLAG_SYS_POKEMON_GET, FLAG_SYS_POKEMON_GET)
K(TRAINER_FLAGS_START, TRAINER_FLAGS_START)
K(TRAINER_LAMPON, TRAINER_ICHOR_LAMPON)
K(TRAINER_PYRRHA, TRAINER_ICHOR_PYRRHA)
K(TRAINER_AITHRA, TRAINER_ICHOR_AITHRA)
K(TRAINER_IONE, TRAINER_ICHOR_IONE_1)
K(B_OUTCOME_WON, B_OUTCOME_WON)

// The test team: one Prinplup at level 100 (no experience, so no level-up or
// evolution prompts) that knows only Surf.
K(SPECIES_TEST, SPECIES_PRINPLUP)
K(MOVE_TEST, MOVE_SURF)
K(MOVE_NONE, MOVE_NONE)
K(PARTY_SIZE, PARTY_SIZE)

// Script bytecode for the setup script the test writes into spare EWRAM.
K(SCR_OP_END, SCR_OP_END)
K(SCR_OP_SETVAR, SCR_OP_SETVAR)
K(SCR_OP_SETFLAG, SCR_OP_SETFLAG)
K(SCR_OP_CALLNATIVE, SCR_OP_CALLNATIVE)
K(SCR_OP_WARP, SCR_OP_WARP)
K(SCR_OP_WAITSTATE, SCR_OP_WAITSTATE)
K(MAP_SCRIPT_ON_FRAME_TABLE, MAP_SCRIPT_ON_FRAME_TABLE)

// Struct offsets.
K(OFF_MAIN_CALLBACK2, offsetof(struct Main, callback2))
K(OFF_MAPHEADER_MAPSCRIPTS, offsetof(struct MapHeader, mapScripts))
K(OFF_SB1_LOCATION, offsetof(struct SaveBlock1, location))
K(OFF_SB1_FLAGS, offsetof(struct SaveBlock1, flags))
K(OFF_SB1_VARS, offsetof(struct SaveBlock1, vars))
K(OFF_SB2_OPTIONS, offsetof(struct SaveBlock2, optionsButtonMode) + 1) // the options bitfield follows
K(OBJECT_EVENT_SIZE, sizeof(struct ObjectEvent))
K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))
K(OFF_AVATAR_OBJECT_EVENT_ID, offsetof(struct PlayerAvatar, objectEventId))
K(OFF_AVATAR_TILE_TRANSITION, offsetof(struct PlayerAvatar, tileTransitionState))
K(OFF_BACKUP_MAP_WIDTH, offsetof(struct BackupMapLayout, width))
K(OFF_BACKUP_MAP_MAP, offsetof(struct BackupMapLayout, map))
K(MAP_OFFSET, MAP_OFFSET)
