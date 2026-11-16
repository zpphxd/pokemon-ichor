#include "global.h"
#include "event_data.h"
#include "ichor_oath.h"
#include "ichor_save.h"
#include "constants/region_map_sections.h"

STATIC_ASSERT(MAPSEC_COUNT <= 256, IchorOathMapSectionsFit);

static bool32 IsNamedArea(u32 mapSection)
{
    return mapSection < MAPSEC_NONE
        && mapSection != MAPSEC_DYNAMIC
        && mapSection != MAPSEC_SECRET_BASE;
}

bool32 Ichor_IsOathActive(void)
{
    return gIchorSave.oath.state == ICHOR_OATH_ACTIVE;
}

bool32 Ichor_ChooseOath(bool32 swear)
{
    if (swear > TRUE || gIchorSave.oath.state != ICHOR_OATH_UNDECIDED
        || FlagGet(FLAG_ICHOR_GOT_STARTER))
        return FALSE;
    gIchorSave.oath.state = swear ? ICHOR_OATH_ACTIVE : ICHOR_OATH_DECLINED;
    return TRUE;
}

bool32 Ichor_ReleaseOath(void)
{
    if (!Ichor_IsOathActive())
        return FALSE;
    gIchorSave.oath.state = ICHOR_OATH_RELEASED;
    return TRUE;
}

bool32 Ichor_FailOath(void)
{
    if (!Ichor_IsOathActive())
        return FALSE;
    gIchorSave.oath.state = ICHOR_OATH_FAILED;
    return TRUE;
}

bool32 Ichor_HasOathEncounter(u32 mapSection)
{
    if (!IsNamedArea(mapSection))
        return FALSE;
    return (gIchorSave.oath.encounters[mapSection / 8] & (1 << (mapSection % 8))) != 0;
}

bool32 Ichor_ClaimOathEncounter(u32 mapSection)
{
    if (!Ichor_IsOathActive())
        return TRUE;
    if (!IsNamedArea(mapSection) || Ichor_HasOathEncounter(mapSection))
        return FALSE;
    gIchorSave.oath.encounters[mapSection / 8] |= 1 << (mapSection % 8);
    return TRUE;
}

u32 Ichor_CountOathEncounters(void)
{
    u32 mapSection, count = 0;
    for (mapSection = 0; mapSection < MAPSEC_NONE; mapSection++)
        if (Ichor_HasOathEncounter(mapSection))
            count++;
    return count;
}
