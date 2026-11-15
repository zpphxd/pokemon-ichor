// Constants and struct offsets for tools/ichor/tests/aigina_interior.lua.
// aigina_interior.sh compiles this with the game's own headers (gcc -S) and turns
// each k_NAME into a Lua table entry, so the test never hardcodes an id or an offset.
#include "global.h"
#include "main.h"
#include "fieldmap.h"
#include "event_object_movement.h"
#include "constants/flags.h"
#include "constants/map_groups.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

// Maps
K(MAP_TOWN, MAP_AEGINA_TOWN)
K(MAP_ROAD, MAP_AEGINA_APHAIA_ROAD)
K(MAP_OROS, MAP_AEGINA_MOUNT_OROS)
K(MAP_TEMPLE, MAP_AEGINA_TEMPLE_OF_APHAIA)

// The state after the voyage, with Act II's Aigina stop open (BUILD.md, batch 1)
K(FLAG_ARRIVED, FLAG_ICHOR_ARRIVED_AEGINA)
K(FLAG_VISITED, FLAG_ICHOR_VISITED_AEGINA)
K(FLAG_HIDE_CAST, FLAG_ICHOR_HIDE_AEGINA_CAST)
K(FLAG_NIGHT, FLAG_ICHOR_AEGINA_NIGHT)
K(FLAG_CROSSING_DONE, FLAG_ICHOR_CROSSING_DONE)
K(FLAG_AIGINA_STOP, FLAG_ICHOR_FERRY_TO_AEGINA)

// What the walk collects
K(FLAG_HERM, FLAG_ICHOR_HERM_AEGINA)
K(FLAG_SILVER_POWDER, FLAG_ICHOR_ITEM_APHAIA_SILVER_POWDER)
K(FLAG_SUPER_POTION, FLAG_ICHOR_ITEM_APHAIA_SUPER_POTION)
K(FLAG_FEATHERS, FLAG_ICHOR_ITEM_APHAIA_PRETTY_FEATHER)
K(FLAG_WINE, FLAG_ICHOR_ITEM_OROS_WINE)

// A Repel that won't run out, ahead of a lead raised to level 100: no wild
// Pokémon gets through on the walk
K(VAR_REPEL_STEP_COUNT, VAR_REPEL_STEP_COUNT)
K(VARS_START, VARS_START)
K(OFF_MON_LEVEL, offsetof(struct Pokemon, level))

// Struct offsets
K(OFF_MAIN_CALLBACK2, offsetof(struct Main, callback2))
K(OFF_SB1_POS, offsetof(struct SaveBlock1, pos))
K(OFF_SB1_LOCATION, offsetof(struct SaveBlock1, location))
K(OFF_SB1_FLAGS, offsetof(struct SaveBlock1, flags))
K(OFF_SB1_VARS, offsetof(struct SaveBlock1, vars))
K(OFF_SB2_OPTIONS, offsetof(struct SaveBlock2, optionsButtonMode) + 1) // the options bitfield follows
K(OBJECT_EVENT_SIZE, sizeof(struct ObjectEvent))
K(OBJECT_EVENTS_COUNT, OBJECT_EVENTS_COUNT)
K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))
K(OFF_OBJ_LOCAL_ID, offsetof(struct ObjectEvent, localId))
K(OFF_AVATAR_OBJECT_EVENT_ID, offsetof(struct PlayerAvatar, objectEventId))
K(OFF_AVATAR_TILE_TRANSITION, offsetof(struct PlayerAvatar, tileTransitionState))
K(OFF_BACKUP_MAP_WIDTH, offsetof(struct BackupMapLayout, width))
K(OFF_BACKUP_MAP_HEIGHT, offsetof(struct BackupMapLayout, height))
K(OFF_BACKUP_MAP_MAP, offsetof(struct BackupMapLayout, map))
K(MAP_OFFSET, MAP_OFFSET)
K(MAP_OFFSET_W, MAP_OFFSET_W)
K(MAP_OFFSET_H, MAP_OFFSET_H)
