// Constants and struct offsets for tools/ichor/tests/elaia_opening.lua (and the
// smoke test). elaia_opening.sh compiles this with the game's own headers (gcc -S)
// and turns each k_NAME into a Lua table entry, so the tests never hardcode an
// id or an offset.
#include "global.h"
#include "main.h"
#include "fieldmap.h"
#include "task.h"
#include "pokemon.h"
#include "constants/battle.h"
#include "constants/flags.h"
#include "constants/map_groups.h"
#include "constants/map_scripts.h"
#include "constants/script_commands.h"
#include "constants/songs.h"
#include "constants/species.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

// Maps
K(MAP_ELAIA, MAP_ELAIA_VILLAGE)
K(MAP_HOUSE_1F, MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_1F)
K(MAP_HOUSE_2F, MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_2F)
K(MAP_KYDIPPE, MAP_ELAIA_VILLAGE_NEIGHBORS_HOUSE)
K(MAP_AKADEMIA, MAP_ELAIA_VILLAGE_AKADEMIA)
K(MAP_ROUTE1, MAP_KALLISTE_ROUTE1)
K(MAP_BAKERS_HOUSE, MAP_ELAIA_VILLAGE_BAKERS_HOUSE)

// Story flags and vars (SCRIPT.md Part 8)
K(FLAG_SET_WATER_CLOCK, FLAG_ICHOR_SET_WATER_CLOCK)
K(FLAG_TALKED_TO_MOM, FLAG_ICHOR_TALKED_TO_MOM)
K(FLAG_THREAD_READ, FLAG_ICHOR_THREAD_READ)
K(FLAG_GOT_STARTER, FLAG_ICHOR_GOT_STARTER)
K(FLAG_KLEON_TOOK_STARTER, FLAG_ICHOR_KLEON_TOOK_STARTER)
K(FLAG_KLEON_BATTLE_1_DONE, FLAG_ICHOR_KLEON_BATTLE_1_DONE)
K(FLAG_WON_KLEON_1, FLAG_ICHOR_WON_KLEON_1)
K(FLAG_GOT_POKEBALLS, FLAG_ICHOR_GOT_POKEBALLS)
K(FLAG_GOT_KYDIPPE_ORAN, FLAG_ICHOR_GOT_KYDIPPE_ORAN)
K(FLAG_GOT_GLYKERA_CAKES, FLAG_ICHOR_GOT_GLYKERA_CAKES)
K(FLAG_DID_KIMON_TRADE, FLAG_ICHOR_DID_KIMON_TRADE)
K(FLAG_GOT_KIMON_PEARLS, FLAG_ICHOR_GOT_KIMON_PEARLS)
K(FLAG_HIDDEN_HONEY, FLAG_HIDDEN_ITEM_ICHOR_ELAIA_HONEY)
K(FLAG_BADGE01_GET, FLAG_BADGE01_GET)
K(FLAG_HIDE_KRATER_NEBREL, FLAG_ICHOR_HIDE_KRATER_NEBREL)
K(FLAG_HIDE_KRATER_KYNDER, FLAG_ICHOR_HIDE_KRATER_KYNDER)
K(FLAG_HIDE_KRATER_HIPLING, FLAG_ICHOR_HIDE_KRATER_HIPLING)
K(FLAG_HIDE_KLEON_ELAIA, FLAG_ICHOR_HIDE_KLEON_ELAIA)
K(FLAG_HIDE_ALETHEA_ELAIA, FLAG_ICHOR_HIDE_ALETHEA_ELAIA)
K(FLAG_HIDE_SCRIBE, FLAG_ICHOR_HIDE_SCRIBE)
K(FLAG_NO_WHITEOUT, FLAG_ICHOR_NO_WHITEOUT)
K(FLAG_SYS_B_DASH, FLAG_SYS_B_DASH)
K(FLAG_SYS_POKEMON_GET, FLAG_SYS_POKEMON_GET)
K(FLAG_SYS_POKEDEX_GET, FLAG_SYS_POKEDEX_GET)
K(VAR_STARTER_MON, VAR_STARTER_MON)
K(VARS_START, VARS_START)

// Music
K(MUS_ELAIA, MUS_ICHOR_ELAIA)
K(MUS_AKADEMIA, MUS_ICHOR_AKADEMIA)

K(B_OUTCOME_WON, B_OUTCOME_WON)
K(VAR_TEMP_0, VAR_TEMP_0)
K(PARTY_SIZE, PARTY_SIZE)
K(SPECIES_GALEKIT, SPECIES_GALEKIT)

// Script bytecode for the setup script the test writes into spare EWRAM.
K(SCR_OP_END, SCR_OP_END)
K(SCR_OP_SETVAR, SCR_OP_SETVAR)
K(SCR_OP_CALLNATIVE, SCR_OP_CALLNATIVE)
K(SCR_OP_WAITSTATE, SCR_OP_WAITSTATE)
K(SCR_OP_WARP, SCR_OP_WARP)
K(MAP_SCRIPT_ON_FRAME_TABLE, MAP_SCRIPT_ON_FRAME_TABLE)
K(OFF_MAPHEADER_MAPSCRIPTS, offsetof(struct MapHeader, mapScripts))
K(B_OUTCOME_LOST, B_OUTCOME_LOST)

// Struct offsets
K(OFF_MAIN_CALLBACK2, offsetof(struct Main, callback2))
K(OFF_SB1_POS, offsetof(struct SaveBlock1, pos))
K(OFF_SB1_LOCATION, offsetof(struct SaveBlock1, location))
K(OFF_SB1_FLAGS, offsetof(struct SaveBlock1, flags))
K(OFF_SB1_VARS, offsetof(struct SaveBlock1, vars))
K(OFF_SB2_OPTIONS, offsetof(struct SaveBlock2, optionsButtonMode) + 1) // the options bitfield follows
K(OFF_SB2_NAME, offsetof(struct SaveBlock2, playerName))
K(OFF_SB2_GENDER, offsetof(struct SaveBlock2, playerGender))
K(OBJECT_EVENT_SIZE, sizeof(struct ObjectEvent))
K(OBJECT_EVENTS_COUNT, OBJECT_EVENTS_COUNT)
K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))
K(OFF_OBJ_LOCAL_ID, offsetof(struct ObjectEvent, localId))
K(OFF_AVATAR_OBJECT_EVENT_ID, offsetof(struct PlayerAvatar, objectEventId))
K(OFF_AVATAR_TILE_TRANSITION, offsetof(struct PlayerAvatar, tileTransitionState))
K(OFF_BACKUP_MAP_WIDTH, offsetof(struct BackupMapLayout, width))
K(OFF_BACKUP_MAP_MAP, offsetof(struct BackupMapLayout, map))
K(MAP_OFFSET, MAP_OFFSET)
K(MAPGRID_COLLISION_MASK, MAPGRID_COLLISION_MASK)
K(POKEMON_SIZE, sizeof(struct Pokemon))
K(OFF_MON_HP, offsetof(struct Pokemon, hp))
K(OFF_MON_MAXHP, offsetof(struct Pokemon, maxHP))
K(BATTLE_MON_SIZE, sizeof(struct BattlePokemon))
K(OFF_BATTLE_MON_HP, offsetof(struct BattlePokemon, hp))
K(TASK_SIZE, sizeof(struct Task))
K(OFF_TASK_FUNC, offsetof(struct Task, func))
K(OFF_TASK_ACTIVE, offsetof(struct Task, isActive))
K(NUM_TASKS, NUM_TASKS)
