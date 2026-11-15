// Constants and struct offsets for tools/ichor/tests/temple_hermes.lua.
// temple_hermes.sh compiles this with the game's own headers (gcc -S) and turns each
// k_NAME into a Lua table entry, so the test never hardcodes an id or an offset.
#include "global.h"
#include "main.h"
#include "fieldmap.h"
#include "ichor_save.h"
#include "gba/m4a_internal.h"
#include "constants/battle.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/map_scripts.h"
#include "constants/metatile_labels.h"
#include "constants/moves.h"
#include "constants/opponents.h"
#include "constants/script_commands.h"
#include "constants/songs.h"
#include "constants/species.h"
#include "constants/vars.h"

#define K(name, value) const int k_##name = (value);

// Where the test goes and what it reads.
K(MAP_TEMPLE, MAP_EMPORION_CITY_TEMPLE_OF_HERMES)
K(VAR_TEMP_0, VAR_TEMP_0)
K(VAR_DELIVERED, VAR_TEMP_1)
K(VAR_GLASS, VAR_TEMP_2)
K(VAR_RUNNING, VAR_TEMP_3)
K(VAR_OIL, VAR_TEMP_5)
K(VARS_START, VARS_START)
K(FLAG_RUN_DONE, FLAG_ICHOR_HERALDS_RUN_DONE)
K(FLAG_RUN_FAILED, FLAG_ICHOR_HERALDS_RUN_FAILED)
K(FLAG_RUN_TOLD, FLAG_ICHOR_HERALDS_RUN_TOLD)
K(FLAG_HERM_J1, FLAG_ICHOR_HERMES_HERM_J1)
K(FLAG_HERM_J2, FLAG_ICHOR_HERMES_HERM_J2)
K(FLAG_HERM_J3, FLAG_ICHOR_HERMES_HERM_J3)
K(FLAG_HERM_J4, FLAG_ICHOR_HERMES_HERM_J4)
K(FLAG_GOT_TM_AERIAL_ACE, FLAG_ICHOR_GOT_TM_AERIAL_ACE)
K(FLAG_HERMES_OFFERING, FLAG_ICHOR_GIFTS_START + 11)   // the Hierophant's offering, Hermes (god 2)
K(FLAG_BADGE01_GET, FLAG_BADGE01_GET)
K(FLAG_BADGE02_GET, FLAG_BADGE02_GET)
K(FLAG_BADGE08_GET, FLAG_BADGE08_GET)
K(FLAG_SYS_POKEMON_GET, FLAG_SYS_POKEMON_GET)
K(TRAINER_FLAGS_START, TRAINER_FLAGS_START)
K(TRAINER_PODARGE, TRAINER_ICHOR_PODARGE)
K(TRAINER_EUCHIDAS, TRAINER_ICHOR_EUCHIDAS)
K(TRAINER_PHILONIDES, TRAINER_ICHOR_PHILONIDES)
K(TRAINER_KERYKOS, TRAINER_ICHOR_KERYKOS_1)
K(B_OUTCOME_WON, B_OUTCOME_WON)
K(ITEM_TM40, ITEM_TM40)
K(ITEM_HONEY, ITEM_HONEY)
K(MUS_TEMPLE_HERMES, MUS_ICHOR_TEMPLE_HERMES)
K(MUS_BATTLE_HIEROPHANT, MUS_ICHOR_BATTLE_RIVAL)

// The room's scripted metatiles (tools/ichor/maps/temple_hermes.py writes the labels).
K(MT_HEAD_S, METATILE_TempleHermes_Herm_HeadS)
K(MT_HEAD_N, METATILE_TempleHermes_Herm_HeadN)
K(MT_HEAD_OILED_N, METATILE_TempleHermes_Herm_HeadOiledN)
K(MT_HEAD_OILED_E, METATILE_TempleHermes_Herm_HeadOiledE)
K(MT_HEAD_OILED_S, METATILE_TempleHermes_Herm_HeadOiledS)
K(MT_HEAD_OILED_W, METATILE_TempleHermes_Herm_HeadOiledW)
K(MT_SHAFT, METATILE_TempleHermes_Herm_Shaft)
K(MT_SHAFT_SCROLL, METATILE_TempleHermes_Herm_ShaftScroll)
K(MT_TURN_E, METATILE_TempleHermes_Turnstile_TurnE)
K(MT_TURN_W, METATILE_TempleHermes_Turnstile_TurnW)
K(MT_GATE_SHUT, METATILE_TempleHermes_Turnstile_GateHShut)
K(MT_GATE_OPEN, METATILE_TempleHermes_Turnstile_GateHOpen)
K(MT_TORCH_LIT, METATILE_TempleHermes_Props_TorchLit)
K(MT_TORCH_COLD, METATILE_TempleHermes_Props_TorchCold)
K(MT_GLASS, METATILE_TempleHermes_Props_GlassTop)
K(MT_GLASS_GONE, METATILE_TempleHermes_Props_Floor)
K(MT_TABLE_FULL, METATILE_TempleHermes_ScrollTable_FullL)
K(MT_TABLE_EMPTY, METATILE_TempleHermes_ScrollTable_EmptyL)

// The test team: one Prinplup at level 100 (no experience, so no level-up or
// evolution prompts) that knows only Surf.
K(SPECIES_TEST, SPECIES_PRINPLUP)
K(MOVE_TEST, MOVE_SURF)
K(MOVE_NONE, MOVE_NONE)
K(PARTY_SIZE, PARTY_SIZE)

// Script bytecode for the setup script the test writes into spare EWRAM.
K(SCR_OP_END, SCR_OP_END)
K(SCR_OP_SETVAR, SCR_OP_SETVAR)
K(SCR_OP_SETFLAG, SCR_OP_SETFLAG)
K(SCR_OP_CALLNATIVE, SCR_OP_CALLNATIVE)
K(SCR_OP_WARP, SCR_OP_WARP)
K(SCR_OP_WAITSTATE, SCR_OP_WAITSTATE)
K(MAP_SCRIPT_ON_FRAME_TABLE, MAP_SCRIPT_ON_FRAME_TABLE)

// Struct offsets.
K(OFF_MAIN_CALLBACK2, offsetof(struct Main, callback2))
K(OFF_MAPHEADER_MAPSCRIPTS, offsetof(struct MapHeader, mapScripts))
K(OFF_SB1_LOCATION, offsetof(struct SaveBlock1, location))
K(OFF_SB1_FLAGS, offsetof(struct SaveBlock1, flags))
K(OFF_SB1_VARS, offsetof(struct SaveBlock1, vars))
K(OFF_SB1_BAG, offsetof(struct SaveBlock1, bag))
K(BAG_SLOTS, BAG_ITEMS_COUNT + BAG_KEYITEMS_COUNT + BAG_POKEBALLS_COUNT + BAG_TMHM_COUNT + BAG_BERRIES_COUNT)
K(ITEM_SLOT_SIZE, sizeof(struct ItemSlot))
K(OFF_ITEM_SLOT_QUANTITY, offsetof(struct ItemSlot, quantity))
K(OFF_SB2_ENCRYPTION_KEY, offsetof(struct SaveBlock2, encryptionKey))
K(OFF_SB2_OPTIONS, offsetof(struct SaveBlock2, optionsButtonMode) + 1) // the options bitfield follows
K(OFF_SB3_ICHOR, offsetof(struct SaveBlock3, ichor))
K(OFF_ICHOR_FLAGS, offsetof(struct IchorSave, flags))
K(ICHOR_FLAGS_START, ICHOR_FLAGS_START)
K(ICHOR_FLAGS_END, ICHOR_FLAGS_END)
K(OBJECT_EVENT_SIZE, sizeof(struct ObjectEvent))
K(OBJECT_EVENTS_COUNT, OBJECT_EVENTS_COUNT)
K(OFF_OBJ_CURRENT_COORDS, offsetof(struct ObjectEvent, currentCoords))
K(OFF_OBJ_LOCAL_ID, offsetof(struct ObjectEvent, localId))
K(OFF_SB1_OBJ_TEMPLATES, offsetof(struct SaveBlock1, objectEventTemplates))
K(OBJ_TEMPLATES_COUNT, OBJECT_EVENT_TEMPLATES_COUNT)
K(OBJ_TEMPLATE_SIZE, sizeof(struct ObjectEventTemplate))
K(OFF_TEMPLATE_LOCAL_ID, offsetof(struct ObjectEventTemplate, localId))
K(OFF_TEMPLATE_X, offsetof(struct ObjectEventTemplate, x))
K(OFF_TEMPLATE_Y, offsetof(struct ObjectEventTemplate, y))
K(OFF_AVATAR_OBJECT_EVENT_ID, offsetof(struct PlayerAvatar, objectEventId))
K(OFF_AVATAR_TILE_TRANSITION, offsetof(struct PlayerAvatar, tileTransitionState))
K(OFF_BACKUP_MAP_WIDTH, offsetof(struct BackupMapLayout, width))
K(OFF_BACKUP_MAP_MAP, offsetof(struct BackupMapLayout, map))
K(MAP_OFFSET, MAP_OFFSET)
K(SONG_SIZE, sizeof(struct Song))
K(OFF_SONG_HEADER, offsetof(struct Song, header))
K(OFF_MPLAY_SONGHEADER, offsetof(struct MusicPlayerInfo, songHeader))
