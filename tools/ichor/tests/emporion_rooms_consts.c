// Constants and struct offsets for tools/ichor/tests/emporion_rooms.lua.
// emporion_rooms.sh compiles this with the game's own headers (gcc -S) and turns each
// k_NAME into a Lua table entry, so the test never hardcodes an id or an offset.
#include "global.h"
#include "main.h"
#include "fieldmap.h"
#include "task.h"
#include "pokemon.h"
#include "ichor_save.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/map_event_ids.h"
#include "constants/map_scripts.h"
#include "constants/script_commands.h"
#include "constants/species.h"
#include "constants/opponents.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

// The rooms.
K(MAP_ASCLEPEION, MAP_EMPORION_CITY_ASCLEPEION)
K(MAP_DEIGMA, MAP_EMPORION_CITY_DEIGMA)
K(MAP_HEPHAISTEION, MAP_EMPORION_CITY_HEPHAISTEION)
K(MAP_TAVERN, MAP_EMPORION_CITY_TAVERN)
K(MAP_PHILOXENOS, MAP_EMPORION_CITY_PHILOXENOS_HOUSE)
K(MAP_WIDOW, MAP_EMPORION_CITY_WIDOWS_HOUSE)
K(MAP_RUNNERS, MAP_EMPORION_CITY_RUNNERS_HOUSE)
K(MAP_POTTER, MAP_EMPORION_CITY_POTTERS_WORKSHOP)
K(MAP_HIRING_HALL, MAP_EMPORION_CITY_HIRING_HALL)

// Flags the rooms set or read.
K(FLAG_SYS_POKEMON_GET, FLAG_SYS_POKEMON_GET)
K(FLAG_ARRIVED_EMPORION, FLAG_ICHOR_ARRIVED_EMPORION)
K(FLAG_ACT1_COMPLETE, FLAG_ICHOR_ACT1_COMPLETE)
K(FLAG_BADGE02_GET, FLAG_BADGE02_GET)
K(FLAG_DEIGMA_CLUE, FLAG_ICHOR_DEIGMA_CLUE)
K(FLAG_TRADED_NARKERAY, FLAG_ICHOR_TRADED_NARKERAY)
K(FLAG_FORGE_RELIT, FLAG_ICHOR_FORGE_RELIT)
K(FLAG_GOT_BRONZE_HAMMER, FLAG_ICHOR_GOT_BRONZE_HAMMER)
K(FLAG_HIRING_HALL, FLAG_ICHOR_HIRING_HALL)
K(FLAG_KNUCKLEBONES_EMPORION, FLAG_ICHOR_KNUCKLEBONES_EMPORION)
K(FLAG_KNUCKLEBONES_STREPSIADES, FLAG_ICHOR_KNUCKLEBONES_STREPSIADES)
K(FLAG_PHILOXENOS_LAUREL_2, FLAG_ICHOR_PHILOXENOS_LAUREL_2)
K(FLAG_GOT_QUICK_CLAW, FLAG_ICHOR_GOT_QUICK_CLAW)
K(FLAG_WROTE_TO_MOM, FLAG_ICHOR_WROTE_TO_MOM)
K(FLAG_GOT_WIDOWS_GIFT, FLAG_ICHOR_GOT_WIDOWS_GIFT)
K(FLAG_EUPHRONIOS_1, FLAG_ICHOR_EUPHRONIOS_1)
K(FLAG_EUPHRONIOS_2, FLAG_ICHOR_EUPHRONIOS_2)
K(FLAG_EUPHRONIOS_3, FLAG_ICHOR_EUPHRONIOS_3)
K(TRAINER_FLAGS_START, TRAINER_FLAGS_START)
K(TRAINER_CREW_BOSS, TRAINER_ICHOR_GRUNT_EMPORION_CREW_BOSS)
K(VAR_TEMP_0, VAR_TEMP_0)

// Objects the test looks for.
K(LOCALID_ALETHEA, LOCALID_EMPORION_DEIGMA_ALETHEA)
K(LOCALID_NARKERAY, LOCALID_EMPORION_DEIGMA_NARKERAY)
K(LOCALID_ONOTIS, LOCALID_EMPORION_DEIGMA_ONOTIS)
K(LOCALID_CREW_BOSS, LOCALID_EMPORION_HIRING_HALL_CREW_BOSS)

// The test party and items.
K(SPECIES_ONOTIS, SPECIES_ONOTIS)
K(SPECIES_HARPECK, SPECIES_HARPECK)
K(SPECIES_CHELONET, SPECIES_CHELONET)
K(SPECIES_STACHYSS, SPECIES_STACHYSS)
K(SPECIES_SWAMPERT, SPECIES_SWAMPERT)
K(ITEM_CHARCOAL, ITEM_CHARCOAL)
K(PARTY_SIZE, PARTY_SIZE)

// Script bytecode for the setup scripts the test writes into spare EWRAM.
K(SCR_OP_END, SCR_OP_END)
K(SCR_OP_SETVAR, SCR_OP_SETVAR)
K(SCR_OP_SETFLAG, SCR_OP_SETFLAG)
K(SCR_OP_CLEARFLAG, SCR_OP_CLEARFLAG)
K(SCR_OP_ADDITEM, SCR_OP_ADDITEM)
K(SCR_OP_CALLNATIVE, SCR_OP_CALLNATIVE)
K(SCR_OP_WARP, SCR_OP_WARP)
K(SCR_OP_WAITSTATE, SCR_OP_WAITSTATE)
K(MAP_SCRIPT_ON_FRAME_TABLE, MAP_SCRIPT_ON_FRAME_TABLE)

// Struct offsets.
K(OFF_MAIN_CALLBACK2, offsetof(struct Main, callback2))
K(OFF_MAPHEADER_MAPSCRIPTS, offsetof(struct MapHeader, mapScripts))
K(OFF_SB1_LOCATION, offsetof(struct SaveBlock1, location))
K(OFF_SB1_FLAGS, offsetof(struct SaveBlock1, flags))
K(OFF_SB2_OPTIONS, offsetof(struct SaveBlock2, optionsButtonMode) + 1) // the options bitfield follows
K(OFF_SB3_ICHOR, offsetof(struct SaveBlock3, ichor))
K(OFF_ICHOR_FLAGS, offsetof(struct IchorSave, flags))
K(ICHOR_FLAGS_START, ICHOR_FLAGS_START)
K(ICHOR_FLAGS_END, ICHOR_FLAGS_END)
K(OBJECT_EVENT_SIZE, sizeof(struct ObjectEvent))
K(NUM_OBJECT_EVENTS, OBJECT_EVENTS_COUNT)
K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))
K(OFF_OBJ_LOCAL_ID, offsetof(struct ObjectEvent, localId))
K(OFF_AVATAR_OBJECT_EVENT_ID, offsetof(struct PlayerAvatar, objectEventId))
K(OFF_AVATAR_TILE_TRANSITION, offsetof(struct PlayerAvatar, tileTransitionState))
K(MAP_OFFSET, MAP_OFFSET)
K(POKEMON_SIZE, sizeof(struct Pokemon))
K(OFF_MON_NICKNAME, offsetof(struct Pokemon, box) + offsetof(struct BoxPokemon, nickname))
K(OFF_MON_HP, offsetof(struct Pokemon, hp))
K(OFF_MON_MAXHP, offsetof(struct Pokemon, maxHP))
K(TASK_SIZE, sizeof(struct Task))
K(OFF_TASK_FUNC, offsetof(struct Task, func))
K(OFF_TASK_ACTIVE, offsetof(struct Task, isActive))
K(NUM_TASKS, NUM_TASKS)
K(OFF_MAPGRID_MAP, offsetof(struct BackupMapLayout, map))
K(OFF_MAPGRID_WIDTH, offsetof(struct BackupMapLayout, width))
