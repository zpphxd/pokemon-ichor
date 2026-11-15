// Constants for tools/ichor/tests/ichor_world.lua (see engine_consts.h).
#include "engine_consts.h"
#include "constants/event_object_movement.h"
#include "constants/ichor.h"
#include "constants/rtc.h"
#include "constants/trainer_types.h"
#include "sprite.h"
#include "constants/map_groups.h"
#include "constants/items.h"

K(MAP_ROUTE1, MAP_KALLISTE_ROUTE1)
K(MAP_PHILOXENOS, MAP_EMPORION_CITY_PHILOXENOS_HOUSE)
K(MAP_KELEOS, MAP_ELEUSA_VILLAGE_HOUSE_OF_KELEOS)
K(FLAG_BADGE02, FLAG_BADGE02_GET)
K(FLAG_PHILOXENOS_STORY, FLAG_ICHOR_PHILOXENOS_LAUREL_2)
K(ITEM_WINE, ITEM_WINE)
K(OFF_TIME_HOURS, offsetof(struct Time, hours))
K(OFF_TIME_MINUTES, offsetof(struct Time, minutes))
K(ICHOR_BONES_CAUTIOUS, ICHOR_BONES_CAUTIOUS)
K(ICHOR_BONES_MOM, ICHOR_BONES_MOM)
K(TRAINER_TYPE_ICHOR_GOD, TRAINER_TYPE_ICHOR_GOD)
K(MOVEMENT_TYPE_FACE_DOWN, MOVEMENT_TYPE_FACE_DOWN)
K(TEMPLATE_SIZE, sizeof(struct ObjectEventTemplate))
K(OFF_SB1_TEMPLATES, offsetof(struct SaveBlock1, objectEventTemplates))
K(OFF_TPL_LOCAL_ID, offsetof(struct ObjectEventTemplate, localId))
K(OFF_TPL_X, offsetof(struct ObjectEventTemplate, x))
K(OFF_TPL_Y, offsetof(struct ObjectEventTemplate, y))
K(OFF_TPL_MOVEMENT, offsetof(struct ObjectEventTemplate, movementType))
K(OFF_TPL_TRAINER_TYPE, offsetof(struct ObjectEventTemplate, trainerType))
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_CALLBACK, offsetof(struct Sprite, callback))
K(OFF_SPRITE_DATA0, offsetof(struct Sprite, data))
K(MAX_SPRITES, MAX_SPRITES)
K(ICHOR_OPTION_TINT_OFF, ICHOR_OPTION_TINT_OFF)
K(OFF_ICHOR_OPTIONS_W, offsetof(struct IchorSave, options))
K(TIME_NIGHT, TIME_NIGHT)
