// Constants for tools/ichor/tests/ichor_save.lua (see engine_consts.h).
#include "engine_consts.h"
#include "ichor_oath.h"
#include "constants/region_map_sections.h"
K(OFF_ICHOR_OATH, offsetof(struct IchorSave, oath))
K(ICHOR_OATH_SIZE, sizeof(struct IchorOath))
K(OFF_OATH_STATE, offsetof(struct IchorOath, state))
K(OFF_OATH_FALLEN_COUNT, offsetof(struct IchorOath, fallenCount))
K(OFF_OATH_ENCOUNTERS, offsetof(struct IchorOath, encounters))
K(ICHOR_OATH_ACTIVE, ICHOR_OATH_ACTIVE)
K(MAPSEC_KALLISTE_ROUTE_1, MAPSEC_KALLISTE_ROUTE_1)
// a hidden item planted in RAM (map events copied out of ROM)
K(MAP_EVENTS_SIZE, sizeof(struct MapEvents))
K(OFF_BG_X, offsetof(struct BgEvent, x))
K(OFF_BG_Y, offsetof(struct BgEvent, y))
K(OFF_BG_ELEVATION, offsetof(struct BgEvent, elevation))
K(ICHOR_HIDDEN_ITEM_BANK_ID, ICHOR_HIDDEN_ITEM_BANK_ID)
