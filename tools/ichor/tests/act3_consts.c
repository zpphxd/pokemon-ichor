// Constants for the Act III engine checks (see engine_consts.h and act3_lib.lua).
#include "engine_consts.h"
#include "task.h"
#include "constants/event_object_movement.h"
#include "constants/map_groups.h"

// the object templates SaveBlock1 keeps for the current map
K(OFF_SB1_TEMPLATES, offsetof(struct SaveBlock1, objectEventTemplates))
K(OFF_TEMPLATE_GRAPHICS, offsetof(struct ObjectEventTemplate, graphicsId))
K(OFF_TEMPLATE_ELEVATION, offsetof(struct ObjectEventTemplate, elevation))
K(OFF_TEMPLATE_MOVEMENT_TYPE, offsetof(struct ObjectEventTemplate, movementType))
K(OFF_TEMPLATE_MOVEMENT_RANGE, offsetof(struct ObjectEventTemplate, movementType) + 1)
K(OFF_TEMPLATE_TRAINER_TYPE, offsetof(struct ObjectEventTemplate, trainerType))
K(OFF_OBJ_MOVEMENT_TYPE, offsetof(struct ObjectEvent, movementType))
K(OFF_TASK_DATA, offsetof(struct Task, data))

// the test spot
K(MAP_AGORA, MAP_AKTI_TOWN_AGORA)

// movement types and directions
K(MOVEMENT_TYPE_FACE_DOWN, MOVEMENT_TYPE_FACE_DOWN)
K(MOVEMENT_TYPE_ICHOR_STATUE, MOVEMENT_TYPE_ICHOR_STATUE)
K(MOVEMENT_TYPE_ICHOR_STATUE_UP, MOVEMENT_TYPE_ICHOR_STATUE_UP)
K(MOVEMENT_TYPE_ICHOR_STATUE_RIGHT, MOVEMENT_TYPE_ICHOR_STATUE_RIGHT)
K(MOVEMENT_TYPE_ICHOR_STATUE_ROOTED_UP, MOVEMENT_TYPE_ICHOR_STATUE_ROOTED_UP)
K(MOVEMENT_TYPE_ICHOR_STATUE_ROOTED, MOVEMENT_TYPE_ICHOR_STATUE_ROOTED)
K(MOVEMENT_TYPE_ICHOR_MIRROR_UP, MOVEMENT_TYPE_ICHOR_MIRROR_UP)
K(MOVEMENT_TYPE_ICHOR_MIRROR_LEFT, MOVEMENT_TYPE_ICHOR_MIRROR_LEFT)
K(MOVEMENT_TYPE_ICHOR_MIRROR_RIGHT, MOVEMENT_TYPE_ICHOR_MIRROR_RIGHT)
K(DIR_NONE, DIR_NONE)
K(DIR_SOUTH, DIR_SOUTH)
K(DIR_NORTH, DIR_NORTH)
K(DIR_WEST, DIR_WEST)
K(DIR_EAST, DIR_EAST)
