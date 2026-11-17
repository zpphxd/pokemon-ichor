// Constants and struct offsets for tools/ichor/tests/fishing.lua.
// fishing.sh compiles this with the game's own headers (gcc -S) and turns each
// k_NAME into a Lua table entry, so the test hardcodes no id or offset.
#include "global.h"
#include "task.h"
#include "constants/items.h"
#include "constants/map_groups.h"

#define K(name, value) const int k_##name = (value);

K(OFF_SB1_BAG, offsetof(struct SaveBlock1, bag))
K(OFF_BAG_KEY, offsetof(struct Bag, keyItems))
K(SLOT_SIZE, sizeof(struct ItemSlot))
K(BAG_KEYITEMS_COUNT, BAG_KEYITEMS_COUNT)
K(OFF_SB2_KEY, offsetof(struct SaveBlock2, encryptionKey))
K(OFF_SB1_REGISTERED, offsetof(struct SaveBlock1, registeredItem))
K(ITEM_OLD_ROD, ITEM_OLD_ROD)
K(TASK_SIZE, sizeof(struct Task))
K(OFF_TASK_DATA, offsetof(struct Task, data))

// the maps the audit opened
K(MAP_ROUTE8_KOPAIS_ROAD, MAP_ROUTE8_KOPAIS_ROAD)
K(MAP_KIRRHA, MAP_KIRRHA)
K(MAP_KYTHERA_NERAIDA_FALLS, MAP_KYTHERA_NERAIDA_FALLS)
K(MAP_ROUTE12_CYPRESS_ROAD, MAP_ROUTE12_CYPRESS_ROAD)
