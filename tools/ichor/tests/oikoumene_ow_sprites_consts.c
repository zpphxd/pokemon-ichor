// Constants for tools/ichor/tests/oikoumene_ow_sprites.lua (see engine_consts.h).
#include "engine_consts.h"
#include "sprite.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"

// The batch's ids run contiguously, the Troad's ten, Egypt's nine, then the
// Black Sea's eight, in the order oikoumene_ow_sprites.lua lists them.
K(GFX_FIRST, OBJ_EVENT_GFX_ICHOR_HERO_LAMPKEEPER)
K(GFX_LAST, OBJ_EVENT_GFX_ICHOR_CHALYBES_SMITH)
K(GFX_FIRST_KEMET, OBJ_EVENT_GFX_ICHOR_PROTEUS)
K(GFX_FIRST_PONTOS, OBJ_EVENT_GFX_ICHOR_AIETES)
K(PAL_TAG_TROAD, OBJ_EVENT_PAL_TAG_ICHOR_TROAD)
K(PAL_TAG_KEMET, OBJ_EVENT_PAL_TAG_ICHOR_KEMET)
K(PAL_TAG_PONTOS, OBJ_EVENT_PAL_TAG_ICHOR_PONTOS)
K(MOVEMENT_TYPE_FACE_DOWN, MOVEMENT_TYPE_FACE_DOWN)
K(DIR_SOUTH, DIR_SOUTH)
K(DIR_NORTH, DIR_NORTH)
K(DIR_WEST, DIR_WEST)
K(DIR_EAST, DIR_EAST)

K(OFF_OBJ_SPRITE_ID, offsetof(struct ObjectEvent, spriteId))
K(OFF_OBJ_GRAPHICS_ID, offsetof(struct ObjectEvent, graphicsId))
K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_ANIMS, offsetof(struct Sprite, anims))
K(OFF_SPRITE_ANIM_NUM, offsetof(struct Sprite, animNum))
K(OFF_SPRITE_ANIM_CMD, offsetof(struct Sprite, animCmdIndex))
