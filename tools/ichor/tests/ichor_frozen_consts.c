// Constants for tools/ichor/tests/ichor_frozen.lua (see engine_consts.h).
#include "engine_consts.h"
#include "sprite.h"
#include "constants/event_object_movement.h"
#include "constants/map_groups.h"
#include "constants/songs.h"
#include "constants/opponents.h"

K(MAP_ROUTE1, MAP_KALLISTE_ROUTE1)
K(FLAG_ICHOR_FROZEN_HOUR, FLAG_ICHOR_FROZEN_HOUR)
K(MUS_ICHOR_ELPIS_LULLABY_BOX, MUS_ICHOR_ELPIS_LULLABY_BOX)
K(MOVEMENT_TYPE_ICHOR_FROZEN_STEP_LEFT, MOVEMENT_TYPE_ICHOR_FROZEN_STEP_LEFT)
K(ANIM_STD_GO_WEST, ANIM_STD_GO_WEST)
K(OFF_SB3_FROZEN_STEP, offsetof(struct IchorSave, frozenHourStep))
K(OFF_SB1_TEMPLATES, offsetof(struct SaveBlock1, objectEventTemplates))
K(TEMPLATE_SIZE, sizeof(struct ObjectEventTemplate))
K(OFF_TPL_LOCAL_ID, offsetof(struct ObjectEventTemplate, localId))
K(OFF_TPL_MOVEMENT, offsetof(struct ObjectEventTemplate, movementType))
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_OAM_ATTR2, offsetof(struct Sprite, oam) + 4)
K(OFF_SPRITE_ANIM_NUM, offsetof(struct Sprite, animNum))
K(OFF_SPRITE_ANIM_CMD, offsetof(struct Sprite, animCmdIndex))
K(OFF_OBJ_SPRITE_ID, offsetof(struct ObjectEvent, spriteId))
K(OFF_OBJ_FLAGS0, 0)
K(OFF_TPL_X, offsetof(struct ObjectEventTemplate, x))
K(OFF_TPL_Y, offsetof(struct ObjectEventTemplate, y))
K(TRAINER_ICHOR_TITYROS, TRAINER_ICHOR_TITYROS)
