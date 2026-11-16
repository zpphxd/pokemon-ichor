#include "global.h"
#include "event_data.h"
#include "ichor_oath.h"
#include "ichor_save.h"
#include "test/test.h"
#include "constants/region_map_sections.h"

static void ResetOath(void)
{
    Ichor_InitSave();
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
