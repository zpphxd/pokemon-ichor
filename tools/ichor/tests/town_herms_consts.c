// Constants for tools/ichor/tests/town_herms.lua (see engine_consts.h).
#include "engine_consts.h"
#include "ichor_herms.h"
#include "region_map.h"
#include "sprite.h"
#include "constants/flags.h"
#include "constants/ichor.h"
#include "constants/map_groups.h"

K(MAP_AKTI, MAP_AKTI_TOWN)
K(MAP_AKTI_ASCLEPEION, MAP_AKTI_TOWN_ASCLEPEION)
K(MAP_EMPORION, MAP_EMPORION_CITY)
K(FLAG_ICHOR_TOWN_HERMS_START, FLAG_ICHOR_TOWN_HERMS_START)
K(TOWN_HERM_COUNT, TOWN_HERM_COUNT)
K(TOWN_HERM_ELAIA, TOWN_HERM_ELAIA)
K(TOWN_HERM_AKTI, TOWN_HERM_AKTI)
K(TOWN_HERM_EMPORION, TOWN_HERM_EMPORION)
K(TOWN_HERM_ELEUSA, TOWN_HERM_ELEUSA)
K(TOWN_HERM_THYRSA, TOWN_HERM_THYRSA)
// region_map.c's sFlyMap: callback, state, mapSecId, the RegionMap (4-aligned),
// tileBuffer[0x1c0], nameBuffer[0x26], choseFlyLocation, then hermDest
K(OFF_FLYMAP_REGIONMAP, 8)
K(OFF_FLYMAP_HERMDEST, 8 + sizeof(struct RegionMap) + 0x1c0 + 0x26 + 1)
K(OFF_RM_CURSOR_X, offsetof(struct RegionMap, cursorPosX))
K(OFF_RM_CURSOR_Y, offsetof(struct RegionMap, cursorPosY))
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_CALLBACK, offsetof(struct Sprite, callback))
K(OFF_SPRITE_DATA0, offsetof(struct Sprite, data))
K(MAX_SPRITES, MAX_SPRITES)
// src/data/ichor_town_herms.h's rows: each herm's own cell on the region map
K(TOWN_HERM_ROW_SIZE, sizeof(struct IchorTownHerm))
K(OFF_TH_MAPX, offsetof(struct IchorTownHerm, mapX))
K(OFF_TH_MAPY, offsetof(struct IchorTownHerm, mapY))
K(TOWN_HERM_SKANDEIA, TOWN_HERM_SKANDEIA)
K(TOWN_HERM_PAPHIA, TOWN_HERM_PAPHIA)
K(TOWN_HERM_OLYMPUS, TOWN_HERM_OLYMPUS)
