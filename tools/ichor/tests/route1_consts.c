// Constants and struct offsets for tools/ichor/tests/route1.lua. route1.sh
// compiles this with the game's own headers (gcc -S) and turns each k_NAME into
// a Lua table entry, so the test never hardcodes an id or an offset.
#include "global.h"
#include "main.h"
#include "fieldmap.h"
#include "constants/battle.h"
#include "constants/flags.h"
#include "constants/map_groups.h"
#include "constants/opponents.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

K(MAP_ROUTE1, MAP_KALLISTE_ROUTE1)
K(MAP_KRONION, MAP_KALLISTE_ROUTE1_KRONION_HILL)
K(FLAG_RUINS_CLEARED, FLAG_ICHOR_RUINS_CLEARED)
K(FLAG_FOUND_TABLET, FLAG_ICHOR_FOUND_TITAN_TABLET)
K(FLAG_DEXNAV_GET, FLAG_ICHOR_DEXNAV_GET)
K(FLAG_HIDE_FLOCK, FLAG_ICHOR_HIDE_ROUTE1_FLOCK)
K(FLAG_HIDE_ALETHEA_RUINS, FLAG_ICHOR_HIDE_ALETHEA_RUINS)
K(FLAG_HIDE_RUINS_GRUNTS, FLAG_ICHOR_HIDE_RUINS_GRUNTS)
K(TRAINER_FLAGS_START, TRAINER_FLAGS_START)
K(TRAINER_TITYROS, TRAINER_ICHOR_TITYROS)
K(TRAINER_AGIS, TRAINER_ICHOR_AGIS)
K(TRAINER_PETROS, TRAINER_ICHOR_GRUNT_RUINS_PETROS)
K(TRAINER_AMATHOS, TRAINER_ICHOR_GRUNT_RUINS_AMATHOS)
K(B_OUTCOME_WON, B_OUTCOME_WON)

K(OFF_MAIN_CALLBACK2, offsetof(struct Main, callback2))
K(OFF_MAPHEADER_MAPSCRIPTS, offsetof(struct MapHeader, mapScripts))
K(OFF_SB1_LOCATION, offsetof(struct SaveBlock1, location))
K(OFF_SB1_FLAGS, offsetof(struct SaveBlock1, flags))
K(OFF_SB2_OPTIONS, offsetof(struct SaveBlock2, optionsButtonMode) + 1) // the options bitfield follows
K(OBJECT_EVENT_SIZE, sizeof(struct ObjectEvent))
K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))
K(OFF_AVATAR_OBJECT_EVENT_ID, offsetof(struct PlayerAvatar, objectEventId))
K(OFF_AVATAR_TILE_TRANSITION, offsetof(struct PlayerAvatar, tileTransitionState))
K(MAP_OFFSET, MAP_OFFSET)
