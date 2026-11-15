// Constants for tools/ichor/tests/ichor_herms.lua (see engine_consts.h).
#include "engine_consts.h"
#include "region_map.h"
#include "sprite.h"
#include "constants/ichor.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/region_map_sections.h"

K(MAP_ROUTE1, MAP_KALLISTE_ROUTE1)
K(MAP_AKTI, MAP_AKTI_TOWN)
K(MAPSEC_KALLISTE_ROUTE_1, MAPSEC_KALLISTE_ROUTE_1)
K(MAPSECTYPE_CITY_CANFLY, MAPSECTYPE_CITY_CANFLY)
K(HERM_KALLISTE_ROUTE_1, HERM_KALLISTE_ROUTE_1)
K(HERM_COUNT, HERM_COUNT)
K(ITEM_OLIVE_OIL, ITEM_OLIVE_OIL)
K(ITEM_DAEDALUS_WINGS, ITEM_DAEDALUS_WINGS)
K(ICHOR_GOD_HERMES, ICHOR_GOD_HERMES)
K(FLAG_ICHOR_ALL_HERMS_REWARD, FLAG_ICHOR_ALL_HERMS_REWARD)
// region_map.c's sFlyMap: callback, state, mapSecId, then the RegionMap (4-aligned)
K(OFF_FLYMAP_REGIONMAP, 8)
K(OFF_RM_MAPSEC, offsetof(struct RegionMap, mapSecId))
K(OFF_RM_MAPSECTYPE, offsetof(struct RegionMap, mapSecType))
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_CALLBACK, offsetof(struct Sprite, callback))
K(OFF_SPRITE_DATA0, offsetof(struct Sprite, data))
K(MAX_SPRITES, MAX_SPRITES)
