// Constants and struct offsets for tools/ichor/tests/aegina_town.lua.
// aegina_town.sh compiles this with the game's own headers (gcc -S) and turns each
// k_NAME into a Lua table entry, so the test never hardcodes an id or an offset.
#include "global.h"
#include "main.h"
#include "fieldmap.h"
#include "event_object_movement.h"
#include "constants/flags.h"
#include "constants/map_groups.h"
#include "constants/rtc.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

// Maps
K(MAP_AEGINA, MAP_AEGINA_TOWN)
K(MAP_INN, MAP_AEGINA_TOWN_INN)
K(MAP_MINT, MAP_AEGINA_TOWN_MINT)
K(MAP_AIAKIDES, MAP_AEGINA_TOWN_AIAKIDES_HOUSE)

// Story flags (BUILD.md, batch 1)
K(FLAG_ARRIVED, FLAG_ICHOR_ARRIVED_AEGINA)
K(FLAG_VISITED, FLAG_ICHOR_VISITED_AEGINA)
K(FLAG_HIDE_CAST, FLAG_ICHOR_HIDE_AEGINA_CAST)
K(FLAG_NIGHT, FLAG_ICHOR_AEGINA_NIGHT)
K(FLAG_CROSSING_DONE, FLAG_ICHOR_CROSSING_DONE)
K(FLAG_AIGINA_STOP, FLAG_ICHOR_FERRY_TO_AEGINA)
K(FLAG_BIG_PEARL, FLAG_ICHOR_HIDDEN_AEGINA_BIG_PEARL)
K(FLAG_STARDUST, FLAG_ICHOR_HIDDEN_AEGINA_STARDUST)
K(TIME_NIGHT, TIME_NIGHT)

// Struct offsets
K(OFF_SB1_LOCATION, offsetof(struct SaveBlock1, location))
K(OFF_SB1_FLAGS, offsetof(struct SaveBlock1, flags))
K(OBJECT_EVENT_SIZE, sizeof(struct ObjectEvent))
K(OBJECT_EVENTS_COUNT, OBJECT_EVENTS_COUNT)
K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))
K(OFF_OBJ_LOCAL_ID, offsetof(struct ObjectEvent, localId))
K(OFF_AVATAR_OBJECT_EVENT_ID, offsetof(struct PlayerAvatar, objectEventId))
K(OFF_BACKUP_MAP_WIDTH, offsetof(struct BackupMapLayout, width))
K(OFF_BACKUP_MAP_MAP, offsetof(struct BackupMapLayout, map))
K(MAP_OFFSET, MAP_OFFSET)
