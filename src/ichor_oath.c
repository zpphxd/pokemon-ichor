#include "global.h"
#include "event_data.h"
#include "field_message_box.h"
#include "ichor_oath.h"
#include "ichor_save.h"
#include "main.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "string_util.h"
#include "constants/battle.h"
#include "constants/region_map_sections.h"

STATIC_ASSERT(MAPSEC_COUNT <= 256, IchorOathMapSectionsFit);
STATIC_ASSERT(TOTAL_BOXES_COUNT <= 16, IchorUrnBoxesFit);

#define URN_BOX (TOTAL_BOXES_COUNT - 1)

static EWRAM_DATA bool8 sOathCatchDenied = FALSE;
static EWRAM_DATA u8 sOathAftermathNotice = 0;

#define OATH_NOTICE_SHOWING (1 << 7)
#define OATH_NOTICE_RECOVERED 3
#define OATH_NOTICE_RECOVERED_FULL 4

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

void Ichor_BeginOathBattle(u32 battleType, u32 mapSection)
{
    sOathCatchDenied = FALSE;
    sOathAftermathNotice = 0;
    if (Ichor_IsOathBattle(battleType) && !(battleType & (BATTLE_TYPE_TRAINER | BATTLE_TYPE_GHOST)))
        sOathCatchDenied = !Ichor_ClaimOathEncounter(mapSection);
}

bool32 Ichor_IsOathBattle(u32 battleType)
{
    const u32 excluded = BATTLE_TYPE_LINK
        | BATTLE_TYPE_LINK_IN_BATTLE | BATTLE_TYPE_TOWER_LINK_MULTI
        | BATTLE_TYPE_RECORDED | BATTLE_TYPE_RECORDED_LINK
        | BATTLE_TYPE_FRONTIER | BATTLE_TYPE_TRAINER_HILL | BATTLE_TYPE_SECRET_BASE
        | BATTLE_TYPE_CATCH_TUTORIAL | BATTLE_TYPE_POKEDUDE;
    return Ichor_IsOathActive() && !(battleType & excluded);
}

bool32 Ichor_CanCatchOathBattle(void)
{
    return !Ichor_IsOathActive() || !sOathCatchDenied;
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

u32 Ichor_StoreOathPartyFallen(void)
{
    u32 slot, result = ICHOR_URN_NOT_FALLEN;
    if (!Ichor_IsUrnBox(URN_BOX))
        return result;
    for (slot = 0; slot < PARTY_SIZE; slot++)
    {
        u32 stored = Ichor_StoreOathFallen(&gParties[B_TRAINER_PLAYER][slot]);
        if (stored == ICHOR_URN_FULL)
            result = ICHOR_URN_FULL;
        else if (stored == ICHOR_URN_STORED && result != ICHOR_URN_FULL)
            result = ICHOR_URN_STORED;
    }
    if (result != ICHOR_URN_NOT_FALLEN)
    {
        CompactPartySlots();
        gPartiesCount[B_TRAINER_PLAYER] = CalculatePlayerPartyCount();
    }
    return result;
}

static bool32 HasUsablePartyPartner(void)
{
    u32 slot;
    for (slot = 0; slot < PARTY_SIZE; slot++)
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][slot];
        if (GetMonData(mon, MON_DATA_SPECIES) != SPECIES_NONE
            && !GetMonData(mon, MON_DATA_IS_EGG)
            && GetMonData(mon, MON_DATA_HP) != 0
            && !Ichor_IsOathFallen(&mon->box))
            return TRUE;
    }
    return FALSE;
}

bool32 Ichor_EndOathBattle(u32 battleType, u32 battleOutcome)
{
    if (!Ichor_IsOathBattle(battleType))
        return FALSE;
    if (!HasUsablePartyPartner())
        return TRUE;
    if (battleOutcome != B_OUTCOME_LOST && battleOutcome != B_OUTCOME_DREW)
        Ichor_RetryOathUrn();
    return FALSE;
}

void Ichor_RetryOathUrn(void)
{
    if (Ichor_IsUrnBox(URN_BOX) && HasUsablePartyPartner())
        sOathAftermathNotice = Ichor_StoreOathPartyFallen();
}

static bool32 HasUrnSpace(void)
{
    u32 box;
    for (box = 0; box < TOTAL_BOXES_COUNT; box++)
        if (Ichor_IsUrnBox(box) ? GetFirstFreeBoxSpot(box) >= 0 : CountMonsInBox(box) == 0)
            return TRUE;
    return FALSE;
}

u32 Ichor_PrepareOathRecovery(void)
{
    u32 box, slot, partySlot, stored;
    bool32 hasUrnSpace;
    if (gIchorSave.oath.state == ICHOR_OATH_FAILED)
        return ICHOR_OATH_EXHAUSTED;
    if (!Ichor_IsOathActive())
        return ICHOR_OATH_RECOVERY_NONE;
    if (HasUsablePartyPartner())
    {
        Ichor_RetryOathUrn();
        return ICHOR_OATH_RECOVERY_NONE;
    }

    for (box = 0; box < TOTAL_BOXES_COUNT; box++)
    {
        if (Ichor_IsUrnBox(box))
            continue;
        for (slot = 0; slot < IN_BOX_COUNT; slot++)
        {
            struct BoxPokemon *mon = GetBoxedMonPtr(box, slot);
            if (GetBoxMonData(mon, MON_DATA_SPECIES) != SPECIES_NONE
                && !GetBoxMonData(mon, MON_DATA_IS_EGG)
                && !Ichor_IsOathFallen(mon))
                goto found;
        }
    }
    Ichor_FailOath();
    return ICHOR_OATH_EXHAUSTED;

found:
    hasUrnSpace = HasUrnSpace();
    for (partySlot = 0; partySlot < PARTY_SIZE; partySlot++)
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][partySlot];
        if (GetMonData(mon, MON_DATA_SPECIES) == SPECIES_NONE
            || (hasUrnSpace && Ichor_IsOathFallen(&mon->box)))
            break;
    }
    // Refuse before any mutation if burial cannot free a recovery slot.
    if (partySlot == PARTY_SIZE)
        return ICHOR_OATH_RECOVERY_BLOCKED;

    stored = Ichor_StoreOathPartyFallen();
    for (partySlot = 0; partySlot < PARTY_SIZE; partySlot++)
        if (GetMonData(&gParties[B_TRAINER_PLAYER][partySlot], MON_DATA_SPECIES) == SPECIES_NONE)
            break;
    BoxMonToMon(GetBoxedMonPtr(box, slot), &gParties[B_TRAINER_PLAYER][partySlot]);
    HealPokemon(&gParties[B_TRAINER_PLAYER][partySlot]);
    ZeroBoxMonAt(box, slot);
    if (stored == ICHOR_URN_FULL)
        stored = Ichor_StoreOathPartyFallen();
    CompactPartySlots();
    gPartiesCount[B_TRAINER_PLAYER] = CalculatePlayerPartyCount();
    sOathAftermathNotice = stored == ICHOR_URN_FULL ? OATH_NOTICE_RECOVERED_FULL : OATH_NOTICE_RECOVERED;
    return ICHOR_OATH_RECOVERED;
}

bool32 Ichor_ShowOathAftermathNotice(void)
{
    if (sOathAftermathNotice == ICHOR_URN_NOT_FALLEN)
        return FALSE;
    if (!(sOathAftermathNotice & OATH_NOTICE_SHOWING))
    {
        const u8 *text;
        switch (sOathAftermathNotice)
        {
        case ICHOR_URN_FULL:
            text = COMPOUND_STRING("The Urn has no room.\nFallen partners remain with you.\pEmpty a Pithos jar to give them\nrest. They cannot return to battle.");
            break;
        case OATH_NOTICE_RECOVERED:
            text = COMPOUND_STRING("A living partner from storage\nhas joined your party.\pYour fallen partners now rest\nin the Urn.");
            break;
        case OATH_NOTICE_RECOVERED_FULL:
            text = COMPOUND_STRING("A living partner from storage\nhas joined your party.\pThe Urn has no room.\nFallen partners remain with you.\pEmpty a Pithos jar to give them\nrest. They cannot return to battle.");
            break;
        default:
            text = COMPOUND_STRING("Your fallen partners now rest\nin the Urn.");
            break;
        }
        if (ShowFieldMessage(text))
            sOathAftermathNotice |= OATH_NOTICE_SHOWING;
        return TRUE;
    }
    if (!IsFieldMessageBoxHidden() || !JOY_NEW(A_BUTTON | B_BUTTON))
        return TRUE;
    HideFieldMessageBox();
    sOathAftermathNotice = ICHOR_URN_NOT_FALLEN;
    return FALSE;
}
