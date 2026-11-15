// Constants and struct offsets for tools/ichor/tests/trireme.lua. trireme.sh
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

K(MAP_DECK, MAP_TRIREME_EUPLOIA_DECK)
K(MAP_HOLD, MAP_TRIREME_EUPLOIA_HOLD)
K(MAP_AEGINA, MAP_AEGINA_TOWN)
K(MAP_EMPORION_HARBOR, MAP_EMPORION_HARBOR)
K(FLAG_BOARDED, FLAG_ICHOR_BOARDED_EUPLOIA)
K(FLAG_SAVED_NEST, FLAG_ICHOR_SAVED_HALCYON_NEST)
K(FLAG_GOT_HALCYLING, FLAG_ICHOR_GOT_HALCYLING)
K(FLAG_BATTLED_ALETHEA, FLAG_ICHOR_BATTLED_ALETHEA_DECK)
K(FLAG_CROSSING_DONE, FLAG_ICHOR_CROSSING_DONE)
K(FLAG_AEGINA_NIGHT, FLAG_ICHOR_AEGINA_NIGHT)
K(FLAG_NO_WHITEOUT, FLAG_ICHOR_NO_WHITEOUT)
K(FLAG_NO_RUNNING, FLAG_ICHOR_NO_RUNNING)
K(FLAG_ITEM_SUPER_POTION, FLAG_ICHOR_ITEM_DECK_SUPER_POTION)
K(FLAG_HIDDEN_HEART_SCALE, FLAG_ICHOR_HIDDEN_DECK_HEART_SCALE)
K(FLAG_ITEM_HOLD_POTION, FLAG_ICHOR_ITEM_HOLD_POTION)
K(VAR_TEMP_1_INDEX, VAR_TEMP_1 - VARS_START)
K(B_OUTCOME_WON, B_OUTCOME_WON)
K(TRAINER_FLAGS_START, TRAINER_FLAGS_START)
K(TRAINER_PHORMION, TRAINER_ICHOR_PHORMION)
K(TRAINER_LYKON, TRAINER_ICHOR_LYKON)
K(TRAINER_ALETHEA, TRAINER_ICHOR_ALETHEA_DECK)
K(B_OUTCOME_CAUGHT, B_OUTCOME_CAUGHT)

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
K(MAP_OFFSET, MAP_OFFSET)
