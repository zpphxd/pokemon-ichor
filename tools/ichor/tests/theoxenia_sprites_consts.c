// Constants for tools/ichor/tests/theoxenia_sprites.lua (see engine_consts.h).
#include "engine_consts.h"
#include "sprite.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"

K(GFX_SAM, OBJ_EVENT_GFX_ICHOR_SAM)
K(GFX_APOLLO, OBJ_EVENT_GFX_ICHOR_APOLLO)
K(GFX_CAMI, OBJ_EVENT_GFX_ICHOR_CAMI)
K(GFX_DEMETER, OBJ_EVENT_GFX_ICHOR_DEMETER)
K(ANIM_ICHOR_STRUM, ANIM_ICHOR_STRUM)
K(ANIM_ICHOR_RISE, ANIM_ICHOR_RISE)
K(DIR_SOUTH, DIR_SOUTH)
K(DIR_NORTH, DIR_NORTH)

K(OFF_OBJ_SPRITE_ID, offsetof(struct ObjectEvent, spriteId))
K(OFF_OBJ_GRAPHICS_ID, offsetof(struct ObjectEvent, graphicsId))
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_ANIMS, offsetof(struct Sprite, anims))
K(OFF_SPRITE_ANIM_NUM, offsetof(struct Sprite, animNum))
K(OFF_SPRITE_ANIM_CMD, offsetof(struct Sprite, animCmdIndex))
