// Constants for tools/ichor/tests/pg_sailing.lua (see engine_consts.h). The
// IchorEpics offsets and the player and sprite fields here are what pg_lib.lua
// expects every post-game check's consts to define.
#include "engine_consts.h"
#include "field_player_avatar.h"
#include "sprite.h"
#include "battle.h"
#include "window.h"
#include "ichor_sailing.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/ichor.h"
#include "constants/ichor_sailing.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/map_types.h"
#include "constants/rtc.h"
#include "constants/species.h"

// IchorSave.epics (pg_lib.lua's L.epic8 and friends)
K(OFF_ICHOR_EPICS, offsetof(struct IchorSave, epics))
K(ICHOR_EPICS_SIZE, sizeof(struct IchorEpics))
K(OFF_EPICS_WIND, offsetof(struct IchorEpics, wind))
K(OFF_EPICS_SHIP_PORT, offsetof(struct IchorEpics, shipPort))
K(OFF_EPICS_SEA_MAP_GROUP, offsetof(struct IchorEpics, seaMapGroup))
K(OFF_EPICS_SEA_MAP_NUM, offsetof(struct IchorEpics, seaMapNum))
K(OFF_EPICS_SEA_X, offsetof(struct IchorEpics, seaX))
K(OFF_EPICS_SEA_Y, offsetof(struct IchorEpics, seaY))
K(OFF_EPICS_SEA_FACING, offsetof(struct IchorEpics, seaFacing))
K(OFF_EPICS_CREW, offsetof(struct IchorEpics, crew))
K(OFF_EPICS_LABORS_DONE, offsetof(struct IchorEpics, laborsDone))
K(OFF_EPICS_KLEOS, offsetof(struct IchorEpics, kleos))

// the player, the avatar and sprites
K(OFF_OBJ_MOVEMENT_ACTION, offsetof(struct ObjectEvent, movementActionId))
K(OFF_OBJ_FIELD_EFFECT_SPRITE, offsetof(struct ObjectEvent, fieldEffectSpriteId))
K(OFF_OBJ_SPRITE_ID, offsetof(struct ObjectEvent, spriteId))
K(OFF_AVATAR_FLAGS, offsetof(struct PlayerAvatar, flags))
K(PLAYER_AVATAR_FLAG_SURFING, PLAYER_AVATAR_FLAG_SURFING)
K(SPRITE_SIZE, sizeof(struct Sprite))
K(OFF_SPRITE_CALLBACK, offsetof(struct Sprite, callback))
K(OFF_SPRITE_X, offsetof(struct Sprite, x))
K(OFF_SPRITE_Y, offsetof(struct Sprite, y))
K(OFF_SPRITE_FLAGS, offsetof(struct Sprite, data) + sizeof(((struct Sprite *)0)->data))  // inUse, coordOffsetEnabled, invisible...
K(SPRITE_FLAG_IN_USE, 1)
K(SPRITE_FLAG_INVISIBLE, 4)
K(MAX_SPRITES, MAX_SPRITES)
K(OBJ_EVENT_ID_FOLLOWER, OBJ_EVENT_ID_FOLLOWER)
K(OFF_BATTLEMON_SPECIES, 0)
K(BATTLEMON_SIZE, sizeof(struct BattlePokemon))

// the ship
K(FLAG_ICHOR_POSTGAME, FLAG_ICHOR_POSTGAME)
K(FLAG_ICHOR_GOT_EUPLOIA, FLAG_ICHOR_GOT_EUPLOIA)
K(FLAG_ICHOR_ON_SHIP, FLAG_ICHOR_ON_SHIP)
K(FLAG_ICHOR_AT_SEA, FLAG_ICHOR_AT_SEA)
K(FLAG_ICHOR_SHIP_SAIL, FLAG_ICHOR_SHIP_SAIL)
K(ICHOR_SHIP_GFX, ICHOR_SHIP_GFX)
K(ICHOR_SHIP_GFX_SLACK, ICHOR_SHIP_GFX_SLACK)
K(MAP_PG_TEST_DECK, MAP_PG_TEST_DECK)
K(ICHOR_SHIP_DECK_MAP, ICHOR_SHIP_DECK_MAP)
K(ICHOR_SHIP_DECK_X, ICHOR_SHIP_DECK_X)
K(ICHOR_SHIP_DECK_Y, ICHOR_SHIP_DECK_Y)
K(MAP_AKTI_TOWN, MAP_AKTI_TOWN)
K(MAP_KALLISTE_ROUTE1, MAP_KALLISTE_ROUTE1)
K(VOYAGE_NONE, VOYAGE_NONE)
K(VOYAGE_AKTI, VOYAGE_AKTI)
K(ICHOR_WIND_N, ICHOR_WIND_N)
K(ICHOR_WIND_E, ICHOR_WIND_E)
K(ICHOR_WIND_S, ICHOR_WIND_S)
K(ICHOR_WIND_W, ICHOR_WIND_W)
K(ICHOR_WIND_CALM, ICHOR_WIND_CALM)
K(ICHOR_WIND_FRESH, ICHOR_WIND_FRESH)
K(ICHOR_WIND_STRONG, ICHOR_WIND_STRONG)
K(ICHOR_WIND_BECALMED, ICHOR_WIND_BECALMED)
K(ICHOR_WIND_STRENGTH_SHIFT, ICHOR_WIND_STRENGTH_SHIFT)
K(ICHOR_WIND_GRUDGE_BIT, ICHOR_WIND_GRUDGE_BIT)
K(ICHOR_WIND_BECALMED_BIT, ICHOR_WIND_BECALMED_BIT)

// directions and walks
K(DIR_SOUTH, DIR_SOUTH)
K(DIR_NORTH, DIR_NORTH)
K(DIR_WEST, DIR_WEST)
K(DIR_EAST, DIR_EAST)
K(MOVEMENT_ACTION_WALK_FAST_LEFT, MOVEMENT_ACTION_WALK_FAST_LEFT)
K(MOVEMENT_ACTION_WALK_FAST_UP, MOVEMENT_ACTION_WALK_FAST_UP)
K(MOVEMENT_ACTION_WALK_FAST_RIGHT, MOVEMENT_ACTION_WALK_FAST_RIGHT)
K(MOVEMENT_ACTION_RIDE_WATER_CURRENT_LEFT, MOVEMENT_ACTION_RIDE_WATER_CURRENT_LEFT)
K(MOVEMENT_ACTION_WALK_FASTER_LEFT, MOVEMENT_ACTION_WALK_FASTER_LEFT)

// the map header and the hour
K(OFF_MAPHEADER_MAPTYPE, offsetof(struct MapHeader, mapType))
K(MAP_TYPE_OCEAN_ROUTE, MAP_TYPE_OCEAN_ROUTE)
K(MAP_TYPE_TOWN, MAP_TYPE_TOWN)
K(TIME_NIGHT, TIME_NIGHT)
K(TIME_DAY, TIME_DAY)
K(VAR_REPEL_STEP_COUNT, VAR_REPEL_STEP_COUNT)
K(SPECIES_OBOLORN, SPECIES_OBOLORN)
K(OFF_SB1_DAILY_SEED, offsetof(struct SaveBlock1, dailySeed))
K(VAR_0x8003, VAR_0x8003)
K(WINDOW_SIZE, sizeof(struct Window))
K(OFF_WINDOW_WIDTH, offsetof(struct WindowTemplate, width))
K(OFF_WINDOW_HEIGHT, offsetof(struct WindowTemplate, height))
K(ICHOR_WIND_PANEL_WIDTH, ICHOR_WIND_PANEL_WIDTH)
K(ITEM_DAEDALUS_WINGS, ITEM_DAEDALUS_WINGS)
K(ICHOR_RELIC_FIRST, ICHOR_RELIC_FIRST)
K(RING_DECK_CURSOR, 0xFE)  // src/ichor_relics.c's RING_DECK
