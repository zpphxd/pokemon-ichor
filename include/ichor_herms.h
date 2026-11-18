#ifndef GUARD_ICHOR_HERMS_H
#define GUARD_ICHOR_HERMS_H

// Ichor: herm waystones (design/SYSTEMS.md §4). Anointing a route's great herm
// with olive oil registers it; once the player has Daedalus's Wings, every
// anointed herm's route is a fly target, landing south of the herm.

#include "constants/ichor.h"

struct IchorHerm
{
    u16 map;           // MAP_* the herm stands on; 0 = not placed yet
    u16 mapsec;        // MAPSEC_* that becomes a fly target
    u16 healLocation;  // HEAL_LOCATION_* south of the herm
};

extern const struct IchorHerm gIchorHerms[HERM_MAX];

// A town's travel herm (SYSTEMS §4): registered by the town's healer or a
// touch; any herm then carries the player to its landing tile.
struct IchorTownHerm
{
    u16 map;           // MAP_* the herm stands on; 0 = no town here yet
    u8 x, y;           // the landing tile, beside the herm on the main path
    u16 healLocation;  // the town's healer's HEAL_LOCATION_* (registers it), or HEAL_LOCATION_NONE
    const u8 *name;
};

extern const struct IchorTownHerm gIchorTownHerms[TOWN_HERM_MAX];

bool32 Ichor_IsTownHermRegistered(u32 townHerm);

u16 Ichor_GetHermFlag(u32 herm);

u32 Ichor_CountAnointedHerms(void);
bool32 Ichor_IsHermFlyTarget(u32 mapsec);                 // region_map.c, GetMapsecType
u32 Ichor_GetHermHealLocation(u32 mapsec);                // region_map.c, FilterFlyDestination
u32 Ichor_GetAnointedHermMapsec(u32 herm);                // region_map.c, CreateFlyDestIcons

#endif // GUARD_ICHOR_HERMS_H
