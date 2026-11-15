// Constants for tools/ichor/tests/oikoumene_chart.lua (see engine_consts.h).
#include "engine_consts.h"
#include "region_map.h"
#include "sprite.h"
#include "wild_encounter.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/region_map_sections.h"
#include "constants/songs.h"

K(MAP_SESTOS, MAP_SESTOS)
K(MAP_NAUKRATIS, MAP_NAUKRATIS)
K(MAP_AKTI, MAP_AKTI_TOWN)
K(MAPSEC_SESTOS, MAPSEC_SESTOS)
K(MAPSEC_NAUKRATIS, MAPSEC_NAUKRATIS)
K(MAPSEC_HELLESPONT, MAPSEC_HELLESPONT)
K(MAPSEC_AETHOS, MAPSEC_AETHOS)
K(MAPSEC_THE_OIKOUMENE, MAPSEC_THE_OIKOUMENE)
K(MAPSEC_AKTI_TOWN, MAPSEC_AKTI_TOWN)
K(MAPSEC_NONE, MAPSEC_NONE)
K(MAPSECTYPE_CITY_CANFLY, MAPSECTYPE_CITY_CANFLY)
K(ITEM_DAEDALUS_WINGS, ITEM_DAEDALUS_WINGS)
K(FLAG_ICHOR_OIKOUMENE_ARRIVED, FLAG_ICHOR_OIKOUMENE_ARRIVED)
K(VAR_ICHOR_OIK_CHART, VAR_ICHOR_OIK_CHART)
K(MUS_ICHOR_BATTLE_TRAINER, MUS_ICHOR_BATTLE_TRAINER)
K(MUS_ICHOR_BATTLE_WILD, MUS_ICHOR_BATTLE_WILD)
K(MUS_RG_VS_TRAINER, MUS_RG_VS_TRAINER)
K(MUS_RG_VS_WILD, MUS_RG_VS_WILD)
K(OFF_MAPHEADER_MAPSEC, offsetof(struct MapHeader, regionMapSectionId))
// region_map.c's sFlyMap: callback, state, mapSecId, then the RegionMap (4-aligned)
K(OFF_FLYMAP_REGIONMAP, 8)
K(OFF_RM_MAPSEC, offsetof(struct RegionMap, mapSecId))
K(OFF_RM_MAPSECTYPE, offsetof(struct RegionMap, mapSecType))
K(OFF_RM_NAME, offsetof(struct RegionMap, mapSecName))
K(OFF_RM_CURSOR_X, offsetof(struct RegionMap, cursorPosX))
K(OFF_RM_CURSOR_Y, offsetof(struct RegionMap, cursorPosY))
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_CALLBACK, offsetof(struct Sprite, callback))
K(OFF_SPRITE_TEMPLATE, offsetof(struct Sprite, template))
K(OFF_SPRITE_DATA0, offsetof(struct Sprite, data))
K(MAX_SPRITES, MAX_SPRITES)
