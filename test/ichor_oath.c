#include "global.h"
#include "event_data.h"
#include "ichor_oath.h"
#include "ichor_save.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "string_util.h"
#include "test/test.h"
#include "constants/region_map_sections.h"

static void ResetOath(void)
{
    Ichor_InitSave();
    ResetPokemonStorageSystem();
    FlagClear(FLAG_ICHOR_GOT_STARTER);
}

TEST("Ichor: the Oath is an independent once-only pre-partner choice")
{
    ResetOath();
    EXPECT(!Ichor_IsOathActive());
    EXPECT(!Ichor_ChooseOath(2));
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_UNDECIDED);
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_IsOathActive());
    EXPECT(!Ichor_ChooseOath(FALSE));
    EXPECT(Ichor_IsOathActive());
    ResetOath();
    EXPECT(Ichor_ChooseOath(FALSE));
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_DECLINED);
    EXPECT(!Ichor_ChooseOath(TRUE));
    ResetOath();
    FlagSet(FLAG_ICHOR_GOT_STARTER);
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_IsOathActive());
}

TEST("Ichor: an Oath shares one chance across a named area's maps")
{
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_HECATES_HOLLOW));
    EXPECT_EQ(Ichor_CountOathEncounters(), 2);
    EXPECT(!Ichor_HasOathEncounter(MAPSEC_ELAIA_VILLAGE));
    Ichor_OnSaveLoaded();
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT_EQ(Ichor_CountOathEncounters(), 2);
}

TEST("Ichor: Oath encounter bits are bounded and cannot alias adjacent areas")
{
    u32 section;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_NONE));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_COUNT));
    EXPECT(!Ichor_ClaimOathEncounter(0xFFFFFFFF));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_DYNAMIC));
    EXPECT(!Ichor_ClaimOathEncounter(MAPSEC_SECRET_BASE));
    EXPECT_EQ(Ichor_CountOathEncounters(), 0);
    for (section = 0; section < MAPSEC_NONE; section++)
    {
        if (section == MAPSEC_DYNAMIC || section == MAPSEC_SECRET_BASE)
            continue;
        EXPECT(!Ichor_HasOathEncounter(section));
        EXPECT(Ichor_ClaimOathEncounter(section));
        EXPECT(Ichor_HasOathEncounter(section));
        EXPECT(!Ichor_ClaimOathEncounter(section));
    }
    EXPECT_EQ(Ichor_CountOathEncounters(), MAPSEC_NONE - 2);
}

TEST("Ichor: absent and released Oaths do not consume ordinary encounter chances")
{
    ResetOath();
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT_EQ(Ichor_CountOathEncounters(), 0);
    EXPECT(!Ichor_ReleaseOath());
    EXPECT(!Ichor_FailOath());
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_ReleaseOath());
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_RELEASED);
    EXPECT(!Ichor_ReleaseOath());
    EXPECT(!Ichor_FailOath());
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_HasOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_HECATES_HOLLOW));
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
}

TEST("Ichor: a failed Oath retains its receipts and cannot be sworn again")
{
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_AKTI_TOWN));
    gIchorSave.oath.fallenCount = 3;
    EXPECT(Ichor_FailOath());
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_FAILED);
    EXPECT(!Ichor_IsOathActive());
    EXPECT(!Ichor_FailOath());
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
    EXPECT_EQ(gIchorSave.oath.fallenCount, 3);
}

TEST("Ichor: version 4 migrates Oath bytes without changing existing progress")
{
    u32 i;
    gIchorSave.version = 4;
    gIchorSave.momWins = 27;
    gIchorSave.favor[1] = 83;
    gIchorSave.vars[0] = 2;
    gIchorSave.flags[0] = 0xA5;
    gIchorSave.flags2[0] = 0x5A;
    gIchorSave.thread.anchorCount = 4;
    memset(&gIchorSave.oath, 0xFF, sizeof(gIchorSave.oath));
    Ichor_OnSaveLoaded();
    EXPECT_EQ(gIchorSave.version, ICHOR_SAVE_VERSION);
    EXPECT_EQ(gIchorSave.oath.state, ICHOR_OATH_UNDECIDED);
    EXPECT_EQ(gIchorSave.oath.fallenCount, 0);
    for (i = 0; i < sizeof(gIchorSave.oath.encounters); i++)
        EXPECT_EQ(gIchorSave.oath.encounters[i], 0);
    EXPECT_EQ(gIchorSave.momWins, 27);
    EXPECT_EQ(gIchorSave.favor[1], 83);
    EXPECT_EQ(gIchorSave.vars[0], 2);
    EXPECT_EQ(gIchorSave.flags[0], 0xA5);
    EXPECT_EQ(gIchorSave.flags2[0], 0x5A);
    EXPECT_EQ(gIchorSave.thread.anchorCount, 4);
}

static void CreateOathMon(struct Pokemon *mon)
{
    CreateRandomMon(mon, SPECIES_NEBREL, 5);
}

TEST("Ichor: swearing reserves an empty Urn without overwriting stored Pokemon")
{
    struct Pokemon mon;
    u8 oldName[BOX_NAME_LENGTH + 1];
    ResetOath();
    StringCopy(oldName, GetBoxNamePtr(TOTAL_BOXES_COUNT - 1));
    CreateOathMon(&mon);
    SetBoxMonAt(TOTAL_BOXES_COUNT - 1, 0, &mon.box);
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 1));
    EXPECT_EQ(GetBoxMonDataAt(TOTAL_BOXES_COUNT - 1, 0, MON_DATA_SPECIES), SPECIES_NEBREL);
    EXPECT_EQ(StringCompare(oldName, GetBoxNamePtr(TOTAL_BOXES_COUNT - 1)), 0);
    EXPECT(Ichor_ChooseOath(FALSE));
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT_EQ(StringCompare(GetBoxNamePtr(TOTAL_BOXES_COUNT - 1), COMPOUND_STRING("URN")), 0);
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 1));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 2));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT));
}

TEST("Ichor: only actual non-Egg fainting under the Oath records a fall")
{
    struct Pokemon mon;
    u32 zero = 0, egg = TRUE;
    ResetOath();
    CreateOathMon(&mon);
    EXPECT(!Ichor_RecordOathFallen(&mon));
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_RecordOathFallen(&mon));
    SetMonData(&mon, MON_DATA_IS_EGG, &egg);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(!Ichor_RecordOathFallen(&mon));
    SetMonData(&mon, MON_DATA_IS_EGG, &zero);
    EXPECT(Ichor_RecordOathFallen(&mon));
    EXPECT(Ichor_IsOathFallen(&mon.box));
    EXPECT_EQ(gIchorSave.oath.fallenCount, 1);
    EXPECT(!Ichor_RecordOathFallen(&mon));
    EXPECT_EQ(gIchorSave.oath.fallenCount, 1);
    ZeroMonData(&mon);
    EXPECT(!Ichor_RecordOathFallen(&mon));
}

TEST("Ichor: legacy Pokemon's formerly unused bit is ignored outside an Oath")
{
    struct Pokemon mon;
    ResetOath();
    CreateOathMon(&mon);
    mon.box.oathFallen = TRUE;
    EXPECT(!Ichor_IsOathFallen(&mon.box));
    FlagSet(FLAG_ICHOR_GOT_STARTER);
    EXPECT(!Ichor_ChooseOath(TRUE));
    EXPECT(!Ichor_IsOathFallen(&mon.box));
}

TEST("Ichor: the Urn retains the entire fallen Pokemon before clearing its source")
{
    struct Pokemon mon;
    struct BoxPokemon snapshot;
    const u8 nickname[POKEMON_NAME_LENGTH + 1] = _("CLOUD");
    u32 zero = 0, location = MAPSEC_KALLISTE_ROUTE_1;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    CreateOathMon(&mon);
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_NOT_FALLEN);
    SetMonData(&mon, MON_DATA_NICKNAME, nickname);
    SetMonData(&mon, MON_DATA_MET_LOCATION, &location);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(Ichor_RecordOathFallen(&mon));
    snapshot = mon.box;
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_STORED);
    EXPECT_EQ(memcmp(GetBoxedMonPtr(TOTAL_BOXES_COUNT - 1, 0), &snapshot, sizeof(snapshot)), 0);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SPECIES), SPECIES_NONE);
    EXPECT_EQ(gIchorSave.oath.fallenCount, 1);
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_NOT_FALLEN);
}

TEST("Ichor: a full Urn preserves its contents and leaves the fallen source intact")
{
    struct Pokemon mon, living;
    struct BoxPokemon snapshot;
    u32 i, box, zero = 0;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    for (i = 0; i < IN_BOX_COUNT; i++)
    {
        CreateOathMon(&mon);
        SetMonData(&mon, MON_DATA_HP, &zero);
        EXPECT(Ichor_RecordOathFallen(&mon));
        EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_STORED);
    }
    CreateOathMon(&living);
    for (box = 0; box < TOTAL_BOXES_COUNT - 1; box++)
        for (i = 0; i < IN_BOX_COUNT; i++)
            SetBoxMonAt(box, i, &living.box);
    CreateOathMon(&mon);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(Ichor_RecordOathFallen(&mon));
    snapshot = mon.box;
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_FULL);
    EXPECT_EQ(memcmp(&mon.box, &snapshot, sizeof(snapshot)), 0);
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 1), IN_BOX_COUNT);
    EXPECT_EQ(gIchorSave.oath.fallenCount, IN_BOX_COUNT + 1);
    for (i = 0; i < IN_BOX_COUNT; i++)
        EXPECT(Ichor_IsOathFallen(GetBoxedMonPtr(TOTAL_BOXES_COUNT - 1, i)));
}

TEST("Ichor: a growing Urn reserves only empty jars and preserves living Pokemon")
{
    struct Pokemon mon, living;
    u32 i, zero = 0;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    CreateOathMon(&living);
    SetBoxMonAt(TOTAL_BOXES_COUNT - 2, 0, &living.box);
    for (i = 0; i < IN_BOX_COUNT + 1; i++)
    {
        CreateOathMon(&mon);
        SetMonData(&mon, MON_DATA_HP, &zero);
        EXPECT(Ichor_RecordOathFallen(&mon));
        EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_STORED);
    }
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 1), IN_BOX_COUNT);
    EXPECT_EQ(CountMonsInBox(TOTAL_BOXES_COUNT - 3), 1);
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 3));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 2));
    EXPECT_EQ(StringCompare(GetBoxNamePtr(TOTAL_BOXES_COUNT - 3), COMPOUND_STRING("URN 2")), 0);
    EXPECT_EQ(memcmp(GetBoxedMonPtr(TOTAL_BOXES_COUNT - 2, 0), &living.box, sizeof(living.box)), 0);
    EXPECT(Ichor_ReleaseOath());
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 3));
}

TEST("Ichor: releasing the Oath keeps its Urn and already fallen records")
{
    struct Pokemon mon;
    u32 zero = 0;
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    CreateOathMon(&mon);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(Ichor_RecordOathFallen(&mon));
    EXPECT(Ichor_ReleaseOath());
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 1));
    EXPECT_EQ(Ichor_StoreOathFallen(&mon), ICHOR_URN_STORED);
    CreateOathMon(&mon);
    SetMonData(&mon, MON_DATA_HP, &zero);
    EXPECT(!Ichor_RecordOathFallen(&mon));
    EXPECT_EQ(gIchorSave.oath.fallenCount, 1);
}

TEST("Ichor: version 5 preserves Oath progress while initializing only its Urn mask")
{
    ResetOath();
    EXPECT(Ichor_ChooseOath(TRUE));
    EXPECT(Ichor_ClaimOathEncounter(MAPSEC_KALLISTE_ROUTE_1));
    gIchorSave.oath.fallenCount = 7;
    gIchorSave.version = 5;
    gIchorSave.oath.urnBoxes = 0xFFFF;
    Ichor_OnSaveLoaded();
    EXPECT_EQ(gIchorSave.version, ICHOR_SAVE_VERSION);
    EXPECT(Ichor_IsOathActive());
    EXPECT_EQ(gIchorSave.oath.fallenCount, 7);
    EXPECT_EQ(Ichor_CountOathEncounters(), 1);
    EXPECT_EQ(gIchorSave.oath.urnBoxes, 1 << (TOTAL_BOXES_COUNT - 1));
    EXPECT(Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 1));
    EXPECT(!Ichor_IsUrnBox(TOTAL_BOXES_COUNT - 2));
}
