// Constants for tools/ichor/tests/ichor_relics.lua (see engine_consts.h).
#include "engine_consts.h"
#include "scanline_effect.h"
#include "field_player_avatar.h"
#include "field_weather.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/ichor.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/metatile_behaviors.h"
#include "constants/weather.h"

// the relics, their flags and options
K(ITEM_TALARIA, ITEM_TALARIA)
K(ITEM_BRONZE_HAMMER, ITEM_BRONZE_HAMMER)
K(ITEM_HECATES_TORCH, ITEM_HECATES_TORCH)
K(ITEM_DEMETERS_SICKLE, ITEM_DEMETERS_SICKLE)
K(ITEM_GIRDLE_OF_HERAKLES, ITEM_GIRDLE_OF_HERAKLES)
K(ITEM_POSEIDONS_CONCH, ITEM_POSEIDONS_CONCH)
K(ITEM_DAEDALUS_WINGS, ITEM_DAEDALUS_WINGS)
K(ITEM_HORN_OF_ACHELOUS, ITEM_HORN_OF_ACHELOUS)
K(ITEM_ARIADNES_THREAD, ITEM_ARIADNES_THREAD)
K(ITEM_LABRYS, ITEM_LABRYS)
K(ITEM_HELM_OF_DARKNESS, ITEM_HELM_OF_DARKNESS)
K(ITEM_NEREID_PEARL, ITEM_NEREID_PEARL)
K(ITEM_AEOLUS_BAG, ITEM_AEOLUS_BAG)
K(ICHOR_RELIC_FIRST, ICHOR_RELIC_FIRST)
K(ICHOR_RELIC_LAST, ICHOR_RELIC_LAST)
K(FLAG_ICHOR_RELICS_START, FLAG_ICHOR_RELICS_START)
K(FLAG_SYS_B_DASH, FLAG_SYS_B_DASH)
K(FLAG_SYS_USE_STRENGTH, FLAG_SYS_USE_STRENGTH)
K(FLAG_ICHOR_THREE_FLAMED_TORCH, FLAG_ICHOR_THREE_FLAMED_TORCH)
K(FLAG_ICHOR_HEPHAESTUS_HAMMER, FLAG_ICHOR_HEPHAESTUS_HAMMER)
K(FLAG_ICHOR_TORCH_DOUSED, FLAG_ICHOR_TORCH_DOUSED)
K(FLAG_ICHOR_HELM_ON, FLAG_ICHOR_HELM_ON)
K(FLAG_ICHOR_NO_RELICS, FLAG_ICHOR_NO_RELICS)
K(ICHOR_OPTION_RELIC_AUTO, ICHOR_OPTION_RELIC_AUTO)
K(ICHOR_GOD_HECATE, ICHOR_GOD_HECATE)
K(ICHOR_FLASH_NO_TORCH, ICHOR_FLASH_NO_TORCH)
K(ICHOR_FLASH_TORCH, ICHOR_FLASH_TORCH)
K(ICHOR_FLASH_TORCH_STRONG, ICHOR_FLASH_TORCH_STRONG)
K(ICHOR_FLASH_TORCH_BOTH, ICHOR_FLASH_TORCH_BOTH)
K(ICHOR_FLASH_DOUSED, ICHOR_FLASH_DOUSED)

// obstacles, spawned from a rewritten object template
K(GFX_CUTTABLE_TREE, OBJ_EVENT_GFX_CUTTABLE_TREE)
K(GFX_BREAKABLE_ROCK, OBJ_EVENT_GFX_BREAKABLE_ROCK)
K(GFX_PUSHABLE_BOULDER, OBJ_EVENT_GFX_PUSHABLE_BOULDER)
K(OFF_SB1_TEMPLATES, offsetof(struct SaveBlock1, objectEventTemplates))
K(TEMPLATE_SIZE, sizeof(struct ObjectEventTemplate))
K(OFF_TPL_LOCAL_ID, offsetof(struct ObjectEventTemplate, localId))
K(OFF_TPL_GFX, offsetof(struct ObjectEventTemplate, graphicsId))
K(OFF_TPL_X, offsetof(struct ObjectEventTemplate, x))
K(OFF_TPL_Y, offsetof(struct ObjectEventTemplate, y))
K(OFF_TPL_ELEVATION, offsetof(struct ObjectEventTemplate, elevation))
K(OFF_TPL_MOVEMENT, offsetof(struct ObjectEventTemplate, movementType))
K(OFF_TPL_TRAINER_TYPE, offsetof(struct ObjectEventTemplate, trainerType))
K(OFF_TPL_SCRIPT, offsetof(struct ObjectEventTemplate, script))
K(OFF_TPL_FLAG, offsetof(struct ObjectEventTemplate, flagId))
K(MOVEMENT_TYPE_FACE_DOWN, MOVEMENT_TYPE_FACE_DOWN)

// the map, its header and the player
K(MAP_ROUTE1, MAP_KALLISTE_ROUTE1)
K(OFF_MAPHEADER_CONNECTIONS, offsetof(struct MapHeader, connections))
K(OFF_MAPHEADER_FLAGS_BYTE, 0x1A) // allowCycling.. cave bitfield byte
K(MAPHEADER_CAVE_BIT, 5)
K(CONNECTION_DIVE, CONNECTION_DIVE)
K(CONNECTION_SIZE, sizeof(struct MapConnection))
K(OFF_CONN_DIRECTION, offsetof(struct MapConnection, direction))
K(OFF_CONN_OFFSET, offsetof(struct MapConnection, offset))
K(OFF_CONN_GROUP, offsetof(struct MapConnection, mapGroup))
K(OFF_CONN_NUM, offsetof(struct MapConnection, mapNum))
K(OFF_SB1_FLASH_LEVEL, offsetof(struct SaveBlock1, flashLevel))
K(OFF_SB1_REGISTERED_ITEM, offsetof(struct SaveBlock1, registeredItem))
K(OFF_AVATAR_FLAGS, offsetof(struct PlayerAvatar, flags))
K(PLAYER_AVATAR_FLAG_SURFING, PLAYER_AVATAR_FLAG_SURFING)
K(OFF_WEATHER_CURR, offsetof(struct Weather, currWeather))
K(WEATHER_FOG_HORIZONTAL, WEATHER_FOG_HORIZONTAL)
K(WEATHER_NONE, WEATHER_NONE)
K(OFF_ICHOR_BLESSING_GOD, offsetof(struct IchorSave, blessing.god))
K(OFF_ICHOR_BLESSING_STEPS, offsetof(struct IchorSave, blessing.steps))
K(FLAME_HEARTH, FLAME_HEARTH)
K(FLAME_NONE, FLAME_NONE)
K(VAR_TEMP_2, VAR_TEMP_2)
K(VAR_TEMP_3, VAR_TEMP_3)
K(FLAME_HESTIA_SHIP, FLAME_HESTIA_SHIP)
K(FLAG_ICHOR_BRAZIERS_START_R, FLAG_ICHOR_BRAZIERS_START)
K(OFF_SCANLINE_STATE, offsetof(struct ScanlineEffect, state))
