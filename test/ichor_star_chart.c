#include "global.h"
#include "event_data.h"
#include "ichor_rites.h"
#include "ichor_save.h"
#include "ichor_star_chart.h"
#include "test/test.h"
#include "constants/ichor.h"

static void ResetStars(void)
{
    static const u16 receipts[] =
    {
        FLAG_ICHOR_GOT_POSEIDONS_CONCH, FLAG_BADGE04_GET, FLAG_BADGE05_GET,
        FLAG_BADGE07_GET, FLAG_BADGE08_GET,
    };
    u32 i;
    for (i = 0; i < ARRAY_COUNT(receipts); i++)
        FlagClear(receipts[i]);
    for (i = 0; i < 7; i++)
        FlagClear(FLAG_ICHOR_PAGES_START + i);
    for (i = 0; i < 32; i++)
        FlagClear(FLAG_ICHOR_CONSTELLATIONS_START + i);
    memset(gIchorSave.favor, 0, sizeof(gIchorSave.favor));
}

TEST("Ichor: myth receipts place the correct stars permanently and once")
{
    static const u16 receipts[] =
    {
        FLAG_ICHOR_GOT_POSEIDONS_CONCH, FLAG_BADGE04_GET, FLAG_BADGE05_GET,
        FLAG_BADGE07_GET, FLAG_BADGE08_GET,
    };
    static const u8 stars[] =
    {
        ICHOR_STAR_DELPHINUS, ICHOR_STAR_CRATER, ICHOR_STAR_URSA_MAJOR,
        ICHOR_STAR_CYGNUS, ICHOR_STAR_CORVUS,
    };
    u32 i;
    ResetStars();
    for (i = 0; i < ARRAY_COUNT(receipts); i++)
    {
        FlagSet(receipts[i]);
        EXPECT(FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + stars[i]));
        EXPECT_EQ(Ichor_CountStars(), i + 1);
        FlagSet(receipts[i]);
        FlagClear(receipts[i]);
        EXPECT_EQ(Ichor_CountStars(), i + 1);
    }
    EXPECT(!FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + ICHOR_STAR_UNWOVEN));
}

TEST("Ichor: Favor 30 and seven distinct pages place only their own stars")
{
    u32 i;
    ResetStars();
    Ichor_AddFavorTo(ICHOR_GOD_ARTEMIS, 29);
    Ichor_AddFavorTo(ICHOR_GOD_HERA, 29);
    EXPECT_EQ(Ichor_CountStars(), 0);
    Ichor_AddFavorTo(ICHOR_GOD_ARTEMIS, 1);
    EXPECT(FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + ICHOR_STAR_ORION));
    Ichor_AddFavorTo(ICHOR_GOD_HERA, 1);
    EXPECT(FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + ICHOR_STAR_CANCER));
    Ichor_AddFavorTo(ICHOR_GOD_HESTIA, 100);
    EXPECT_EQ(Ichor_CountStars(), 2);
    for (i = 0; i < 6; i++)
        FlagSet(FLAG_ICHOR_PAGES_START + i);
    EXPECT_EQ(Ichor_CountStars(), 2);
    FlagSet(FLAG_ICHOR_PAGES_START + 6);
    EXPECT(FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + ICHOR_STAR_PLEIADES));
    EXPECT_EQ(Ichor_CountStars(), 3);
}

TEST("Ichor: the chart recovers legacy receipts without inventing later myths")
{
    ResetStars();
    FlagSet(FLAG_BADGE04_GET);
    FlagClear(FLAG_ICHOR_CONSTELLATIONS_START + ICHOR_STAR_CRATER);
    gIchorSave.favor[ICHOR_GOD_ARTEMIS] = 30;
    Ichor_RefreshStars();
    EXPECT_EQ(Ichor_CountStars(), 2);
    Ichor_RefreshStars();
    EXPECT_EQ(Ichor_CountStars(), 2);
    EXPECT(!FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + ICHOR_STAR_UNWOVEN));
    EXPECT(!FlagGet(FLAG_ICHOR_CONSTELLATIONS_START + ICHOR_STAR_TAURUS));
}

TEST("Ichor: all 24 chart placements are bounded and ignore reserved extra bits")
{
    u32 i;
    ResetStars();
    FlagSet(FLAG_ICHOR_CONSTELLATIONS_START + 31);
    EXPECT_EQ(Ichor_CountStars(), 0);
    gSpecialVar_0x8004 = ICHOR_STAR_COUNT;
    EXPECT_EQ(Ichor_PlaceConstellation(), FALSE);
    EXPECT_EQ(Ichor_PlaceStar(0xFFFFFFFF), FALSE);
    for (i = 0; i < ICHOR_STAR_COUNT; i++)
    {
        gSpecialVar_0x8004 = i;
        EXPECT_EQ(Ichor_PlaceConstellation(), TRUE);
        EXPECT_EQ(Ichor_PlaceConstellation(), FALSE);
        EXPECT_EQ(Ichor_CountConstellations(), i + 1);
    }
}
