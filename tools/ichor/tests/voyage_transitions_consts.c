// Constants and struct offsets for tools/ichor/tests/voyage_transitions.lua.
// voyage_transitions.sh compiles this with the game's own headers (gcc -S) and
// turns each k_NAME into a Lua table entry, so the test hardcodes no id or offset.
#include "global.h"
#include "main.h"
#include "fieldmap.h"
#include "task.h"
#include "pokemon.h"
#include "constants/flags.h"
#include "constants/map_groups.h"
#include "constants/map_event_ids.h"
#include "constants/map_scripts.h"
#include "constants/script_commands.h"
#include "constants/species.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

K(MAP_AEGINA, MAP_AEGINA_TOWN)
K(MAP_INN, MAP_AEGINA_TOWN_INN)
K(MAP_DECK, MAP_TRIREME_EUPLOIA_DECK)
K(MAP_EMPORION_HARBOR, MAP_EMPORION_HARBOR)
K(FLAG_ARRIVED_AEGINA, FLAG_ICHOR_ARRIVED_AEGINA)
K(FLAG_VISITED_AEGINA, FLAG_ICHOR_VISITED_AEGINA)
K(FLAG_AEGINA_NIGHT, FLAG_ICHOR_AEGINA_NIGHT)
K(FLAG_CROSSING_DONE, FLAG_ICHOR_CROSSING_DONE)
K(FLAG_SYS_POKEMON_GET, FLAG_SYS_POKEMON_GET)
K(VAR_TEMP_0, VAR_TEMP_0)
K(LOCALID_INN_KLEON, LOCALID_AEGINA_INN_KLEON)
K(VAR_REPEL_STEP_COUNT, VAR_REPEL_STEP_COUNT)
K(SPECIES_KARKIPOOL, SPECIES_KARKIPOOL)
K(PARTY_SIZE, PARTY_SIZE)

K(SCR_OP_END, SCR_OP_END)
K(SCR_OP_SETVAR, SCR_OP_SETVAR)
K(SCR_OP_SETFLAG, SCR_OP_SETFLAG)
K(SCR_OP_CALLNATIVE, SCR_OP_CALLNATIVE)
K(SCR_OP_WARP, SCR_OP_WARP)
K(SCR_OP_WAITSTATE, SCR_OP_WAITSTATE)
K(MAP_SCRIPT_ON_FRAME_TABLE, MAP_SCRIPT_ON_FRAME_TABLE)

K(OFF_MAIN_CALLBACK2, offsetof(struct Main, callback2))
K(OFF_MAPHEADER_MAPSCRIPTS, offsetof(struct MapHeader, mapScripts))
K(OFF_SB1_LOCATION, offsetof(struct SaveBlock1, location))
K(OFF_SB1_FLAGS, offsetof(struct SaveBlock1, flags))
K(OFF_SB2_OPTIONS, offsetof(struct SaveBlock2, optionsButtonMode) + 1)
K(OBJECT_EVENT_SIZE, sizeof(struct ObjectEvent))
K(NUM_OBJECT_EVENTS, OBJECT_EVENTS_COUNT)
K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))
K(OFF_OBJ_LOCAL_ID, offsetof(struct ObjectEvent, localId))
K(OFF_AVATAR_OBJECT_EVENT_ID, offsetof(struct PlayerAvatar, objectEventId))
K(OFF_AVATAR_TILE_TRANSITION, offsetof(struct PlayerAvatar, tileTransitionState))
K(MAP_OFFSET, MAP_OFFSET)
K(TASK_SIZE, sizeof(struct Task))
K(OFF_TASK_FUNC, offsetof(struct Task, func))
K(OFF_TASK_ACTIVE, offsetof(struct Task, isActive))
K(NUM_TASKS, NUM_TASKS)
