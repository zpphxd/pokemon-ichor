// Ichor: herm waystones (design/SYSTEMS.md §4).
//
// Every route has one great herm. Anointing it with olive oil costs one Olive
// Oil, gives Hermes +1 Favor once, and registers it; anointing every herm gives
// Hermes +10 more. With Daedalus's Wings, every anointed herm's route is a fly
// target on the region map, landing on the tile south of the herm. The rows
// are in src/data/ichor_herms.h; data/scripts/ichor_herms.pory has the script.
#include "global.h"
#include "event_data.h"
#include "ichor_herms.h"
#include "ichor_relics.h"
#include "ichor_rites.h"
#include "item.h"
#include "string_util.h"
#include "constants/heal_locations.h"
#include "constants/items.h"
#include "constants/maps.h"
#include "constants/region_map_sections.h"

#include "data/ichor_herms.h"

#define HERM_FLAG(herm) (FLAG_ICHOR_HERMS_START + (herm))
#define HERM_NONE 0xFF

static bool32 IsPlaced(u32 herm)
{
    return herm < HERM_MAX && gIchorHerms[herm].map != 0;
}

static u32 GetHermOnThisMap(void)
{
    u32 herm;
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    for (herm = 0; herm < HERM_MAX; herm++)
    {
        if (IsPlaced(herm) && gIchorHerms[herm].map == map)
            return herm;
    }
    return HERM_NONE;
}

static bool32 IsAnointed(u32 herm)
{
    return FlagGet(HERM_FLAG(herm));
}

u32 Ichor_CountAnointedHerms(void)
{
    return Ichor_CountFlags(FLAG_ICHOR_HERMS_START, HERM_COUNT);
}

// specialvar Ichor_CountHerms: anointed herms, for the Scroll of Deeds. VAR_0x8004 gets HERM_COUNT.
u16 Ichor_CountHerms(void)
{
    gSpecialVar_0x8004 = HERM_COUNT;
    return Ichor_CountAnointedHerms();
}

enum { HERM_STATE_NONE, HERM_STATE_ANOINTED, HERM_STATE_DRY };

// specialvar Ichor_GetHermState: this map's great herm: HERM_STATE_NONE (no
// herm row for this map), _ANOINTED or _DRY. STR_VAR_1 is the Olive Oil carried.
u16 Ichor_GetHermState(void)
{
    u32 herm = GetHermOnThisMap();
    ConvertIntToDecimalStringN(gStringVar1, CountTotalItemQuantityInBag(ITEM_OLIVE_OIL), STR_CONV_MODE_LEFT_ALIGN, 3);
    if (herm == HERM_NONE)
        return HERM_STATE_NONE;
    return IsAnointed(herm) ? HERM_STATE_ANOINTED : HERM_STATE_DRY;
}

// special Ichor_AnointHerm: takes one Olive Oil and registers this map's herm.
// VAR_RESULT is TRUE when it was the last of them (Hermes's +10).
void Ichor_AnointHerm(void)
{
    u32 herm = GetHermOnThisMap();

    gSpecialVar_Result = FALSE;
    if (herm == HERM_NONE || IsAnointed(herm) || !RemoveBagItem(ITEM_OLIVE_OIL, 1))
        return;
    FlagSet(HERM_FLAG(herm));
    Ichor_AddFavorTo(ICHOR_GOD_HERMES, 1);
    if (Ichor_CountAnointedHerms() == HERM_COUNT && !FlagGet(FLAG_ICHOR_ALL_HERMS_REWARD))
    {
        FlagSet(FLAG_ICHOR_ALL_HERMS_REWARD);
        Ichor_AddFavorTo(ICHOR_GOD_HERMES, 10);
        gSpecialVar_Result = TRUE;
    }
}

static u32 GetHermForMapsec(u32 mapsec)
{
    u32 herm;
    for (herm = 0; herm < HERM_MAX; herm++)
    {
        if (IsPlaced(herm) && gIchorHerms[herm].mapsec == mapsec)
            return herm;
    }
    return HERM_NONE;
}

// A route is a fly target once its herm is anointed (the fly map itself needs the Wings).
bool32 Ichor_IsHermFlyTarget(u32 mapsec)
{
    u32 herm = GetHermForMapsec(mapsec);
    return herm != HERM_NONE && IsAnointed(herm) && gIchorHerms[herm].healLocation != HEAL_LOCATION_NONE;
}

u32 Ichor_GetHermHealLocation(u32 mapsec)
{
    if (!Ichor_IsHermFlyTarget(mapsec))
        return HEAL_LOCATION_NONE;
    return gIchorHerms[GetHermForMapsec(mapsec)].healLocation;
}

// The map section of herm `herm` if it's anointed (its fly map icon), else MAPSEC_NONE.
u32 Ichor_GetAnointedHermMapsec(u32 herm)
{
    if (!IsPlaced(herm) || !IsAnointed(herm))
        return MAPSEC_NONE;
    return gIchorHerms[herm].mapsec;
}
