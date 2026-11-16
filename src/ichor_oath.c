#include "global.h"
#include "event_data.h"
#include "ichor_oath.h"
#include "ichor_save.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "string_util.h"
#include "constants/region_map_sections.h"

STATIC_ASSERT(MAPSEC_COUNT <= 256, IchorOathMapSectionsFit);
STATIC_ASSERT(TOTAL_BOXES_COUNT <= 16, IchorUrnBoxesFit);

#define URN_BOX (TOTAL_BOXES_COUNT - 1)

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
        || FlagGet(FLAG_ICHOR_GOT_STARTER)
        || (swear && CountMonsInBox(URN_BOX) != 0))
        return FALSE;
    gIchorSave.oath.state = swear ? ICHOR_OATH_ACTIVE : ICHOR_OATH_DECLINED;
    if (swear)
    {
        gIchorSave.oath.urnBoxes = 1 << URN_BOX;
        StringCopy(GetBoxNamePtr(URN_BOX), COMPOUND_STRING("URN"));
    }
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

bool32 Ichor_IsUrnBox(u32 box)
{
    return box < TOTAL_BOXES_COUNT
        && (gIchorSave.oath.state == ICHOR_OATH_ACTIVE
            || gIchorSave.oath.state == ICHOR_OATH_RELEASED
            || gIchorSave.oath.state == ICHOR_OATH_FAILED)
        && (gIchorSave.oath.urnBoxes & (1 << box));
}

bool32 Ichor_IsOathFallen(const struct BoxPokemon *mon)
{
    return Ichor_IsUrnBox(URN_BOX) && mon->oathFallen;
}

bool32 Ichor_RecordOathFallen(struct Pokemon *mon)
{
    if (!Ichor_IsOathActive() || mon->box.oathFallen
        || GetMonData(mon, MON_DATA_SPECIES) == SPECIES_NONE
        || GetMonData(mon, MON_DATA_IS_EGG)
        || GetMonData(mon, MON_DATA_HP) != 0)
        return FALSE;
    mon->box.oathFallen = TRUE;
    if (gIchorSave.oath.fallenCount < 0xFFFF)
        gIchorSave.oath.fallenCount++;
    return TRUE;
}

u32 Ichor_StoreOathFallen(struct Pokemon *mon)
{
    s32 box;
    s16 slot;
    u32 pages = 0;
    if (!Ichor_IsUrnBox(URN_BOX) || !mon->box.oathFallen
        || GetMonData(mon, MON_DATA_SPECIES) == SPECIES_NONE)
        return ICHOR_URN_NOT_FALLEN;
    for (box = URN_BOX; box >= 0; box--)
    {
        if (!Ichor_IsUrnBox(box))
            continue;
        pages++;
        slot = GetFirstFreeBoxSpot(box);
        if (slot >= 0)
        {
            SetBoxMonAt(box, slot, &mon->box);
            ZeroMonData(mon);
            return ICHOR_URN_STORED;
        }
    }
    for (box = URN_BOX - 1; box >= 0; box--)
    {
        u8 *name;
        if (Ichor_IsUrnBox(box) || CountMonsInBox(box) != 0)
            continue;
        gIchorSave.oath.urnBoxes |= 1 << box;
        name = StringCopy(GetBoxNamePtr(box), COMPOUND_STRING("URN "));
        ConvertIntToDecimalStringN(name, pages + 1, STR_CONV_MODE_LEFT_ALIGN, 2);
        SetBoxMonAt(box, 0, &mon->box);
        ZeroMonData(mon);
        return ICHOR_URN_STORED;
    }
    return ICHOR_URN_FULL;
}
