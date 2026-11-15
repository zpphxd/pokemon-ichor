// Constants for tools/ichor/tests/ichor_save.lua (see engine_consts.h).
#include "engine_consts.h"
// a hidden item planted in RAM (map events copied out of ROM)
K(MAP_EVENTS_SIZE, sizeof(struct MapEvents))
K(OFF_BG_X, offsetof(struct BgEvent, x))
K(OFF_BG_Y, offsetof(struct BgEvent, y))
K(OFF_BG_ELEVATION, offsetof(struct BgEvent, elevation))
K(ICHOR_HIDDEN_ITEM_BANK_ID, ICHOR_HIDDEN_ITEM_BANK_ID)
