// Constants for tools/ichor/tests/ichor_labyrinth.lua (see engine_consts.h).
#include "engine_consts.h"
#include "sprite.h"
#include "constants/event_object_movement.h"
#include "constants/ichor.h"
#include "constants/items.h"
#include "constants/map_groups.h"

K(MAP_ROUTE1, MAP_KALLISTE_ROUTE1)
K(ITEM_LABRYS, ITEM_LABRYS)
K(FLAG_ICHOR_HELM_ON, FLAG_ICHOR_HELM_ON)
K(FLAG_TEMP_1, FLAG_TEMP_1)
K(VAR_TEMP_2, VAR_TEMP_2)
K(VAR_TEMP_3, VAR_TEMP_3)
K(MOVEMENT_TYPE_FACE_DOWN, MOVEMENT_TYPE_FACE_DOWN)
K(MOVEMENT_TYPE_FACE_LEFT, MOVEMENT_TYPE_FACE_LEFT)
K(DIR_SOUTH, DIR_SOUTH)
K(DIR_WEST, DIR_WEST)
// the thread in IchorSave
K(OFF_THR_ANCHORS, offsetof(struct IchorThread, anchors))
K(ANCHOR_SIZE, sizeof(struct IchorThreadAnchor))
K(OFF_ANCHOR_X, offsetof(struct IchorThreadAnchor, x))
K(OFF_ANCHOR_Y, offsetof(struct IchorThreadAnchor, y))
K(OFF_ANCHOR_STEPS, offsetof(struct IchorThreadAnchor, steps))
K(OFF_THR_ANCHOR_COUNT, offsetof(struct IchorThread, anchorCount))
K(OFF_THR_CURRENT, offsetof(struct IchorThread, currentAnchor))
K(OFF_THR_LIVE_X, offsetof(struct IchorThread, liveX))
K(OFF_THR_LIVE_Y, offsetof(struct IchorThread, liveY))
K(OFF_THR_LIVE_LEN, offsetof(struct IchorThread, liveLen))
K(OFF_THR_LIVE, offsetof(struct IchorThread, live))
// object templates, the map header, the player's sprite
K(OFF_SB1_TEMPLATES, offsetof(struct SaveBlock1, objectEventTemplates))
K(TEMPLATE_SIZE, sizeof(struct ObjectEventTemplate))
K(OFF_TPL_LOCAL_ID, offsetof(struct ObjectEventTemplate, localId))
K(OFF_TPL_X, offsetof(struct ObjectEventTemplate, x))
K(OFF_TPL_Y, offsetof(struct ObjectEventTemplate, y))
K(OFF_TPL_MOVEMENT, offsetof(struct ObjectEventTemplate, movementType))
K(OFF_TPL_TRAINER_TYPE, offsetof(struct ObjectEventTemplate, trainerType))
K(OFF_MAPHEADER_FLAGS_BYTE, 0x1A)
K(MAPHEADER_CAVE_BIT, 5)
K(OFF_SB1_FLASH_LEVEL, offsetof(struct SaveBlock1, flashLevel))
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_OBJ_SPRITE_ID, offsetof(struct ObjectEvent, spriteId))
K(OFF_OBJ_FACING, 0x18)
