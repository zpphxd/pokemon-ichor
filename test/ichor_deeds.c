#include "global.h"
#include "event_data.h"
#include "ichor_deeds.h"
#include "ichor_save.h"
#include "string_util.h"
#include "test/test.h"
#include "constants/ichor.h"
#include "constants/vars.h"

static bool32 Contains(const u8 *text)
{
    u32 i, size = StringLength(text), length = StringLength(gStringVar4);
    for (i = 0; i + size <= length; i++)
        if (StringCompareN(gStringVar4 + i, text, size) == 0)
            return TRUE;
    return FALSE;
}

static void ResetDeeds(void)
{
    static const u16 flags[] =
    {
        FLAG_SYS_POKEMON_GET, FLAG_ICHOR_GOT_STARTER, FLAG_BADGE01_GET, FLAG_BADGE02_GET, FLAG_BADGE03_GET,
        FLAG_ICHOR_ARRIVED_EMPORION, FLAG_ICHOR_MYSTERIES_NIGHT,
        FLAG_ICHOR_FRAGMENT_STOLEN, FLAG_ICHOR_ACT1_COMPLETE,
        FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA,
        FLAG_ICHOR_WROTE_TO_MOM, FLAG_ICHOR_GOT_MOMS_HONEY,
        FLAG_ICHOR_GOT_TROWEL, FLAG_ICHOR_ATHENAS_STYLUS,
        FLAG_ICHOR_KRONION_ALTAR_STONE, FLAG_ICHOR_ELEUSA_PERSENYX,
        FLAG_ICHOR_HOLLOW_RAKNIT,
    };
    u32 i;
    for (i = 0; i < ARRAY_COUNT(flags); i++)
        FlagClear(flags[i]);
    for (i = 0; i < ICHOR_AMPHORA_COUNT; i++)
        FlagClear(FLAG_ICHOR_AMPHORAE_START + i);
    for (i = 0; i < ICHOR_AMPHORA_COUNT * ICHOR_SHERDS_PER_AMPHORA; i++)
        FlagClear(FLAG_ICHOR_SHERDS_START + i);
    for (i = 0; i < 7; i++)
        FlagClear(FLAG_ICHOR_PAGES_START + i);
}

TEST("Ichor: Deeds unlock from story receipts and do not claim a pending gift")
{
    static const u16 prerequisites[] =
    {
        0, FLAG_ICHOR_GOT_STARTER, FLAG_BADGE01_GET, FLAG_ICHOR_ARRIVED_EMPORION,
        FLAG_BADGE02_GET, FLAG_BADGE03_GET, FLAG_ICHOR_MYSTERIES_NIGHT,
        FLAG_ICHOR_FRAGMENT_STOLEN, FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA,
        FLAG_ICHOR_ACT1_COMPLETE, FLAG_ICHOR_WROTE_TO_MOM,
    };
    static const u16 receipts[] =
    {
        FLAG_ICHOR_GOT_STARTER, FLAG_BADGE01_GET, FLAG_ICHOR_ARRIVED_EMPORION,
        FLAG_BADGE02_GET, FLAG_BADGE03_GET, FLAG_ICHOR_MYSTERIES_NIGHT,
        FLAG_ICHOR_FRAGMENT_STOLEN, FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA,
        FLAG_ICHOR_ACT1_COMPLETE, FLAG_ICHOR_WROTE_TO_MOM, FLAG_ICHOR_GOT_MOMS_HONEY,
    };
    u32 i;
    for (i = 0; i < ARRAY_COUNT(receipts); i++)
    {
        ResetDeeds();
        EXPECT_EQ(Ichor_DeedState(i), i == 0 ? ICHOR_DEED_OPEN : ICHOR_DEED_HIDDEN);
        if (prerequisites[i] != 0)
            FlagSet(prerequisites[i]);
        EXPECT_EQ(Ichor_DeedState(i), ICHOR_DEED_OPEN);
        gSpecialVar_0x8004 = i;
        EXPECT_EQ(Ichor_BufferDeed(), TRUE);
        EXPECT(!FlagGet(receipts[i]));
        FlagSet(FLAG_ICHOR_ATHENAS_STYLUS);
        EXPECT_EQ(Ichor_BufferDeed(), TRUE);
        EXPECT(Contains(COMPOUND_STRING("Athena's hint:")));
        FlagSet(receipts[i]);
        EXPECT_EQ(Ichor_DeedState(i), ICHOR_DEED_DONE);
    }
    EXPECT_EQ(Ichor_DeedState(0xFFFFFFFF), ICHOR_DEED_HIDDEN);
    gSpecialVar_0x8004 = 0xFFFF;
    EXPECT_EQ(Ichor_BufferDeed(), FALSE);
}

TEST("Ichor: Deeds distinguish amphora pieces, restoration and real encounter completion")
{
    u32 i, piece;
    ResetDeeds();
    for (i = 0; i < ICHOR_AMPHORA_COUNT; i++)
    {
        gSpecialVar_0x8004 = ICHOR_DEED_AMPHORA_START + i;
        EXPECT_EQ(Ichor_DeedState(gSpecialVar_0x8004), ICHOR_DEED_HIDDEN);
        EXPECT_EQ(Ichor_BufferDeed(), FALSE);
        for (piece = 0; piece < ICHOR_SHERDS_PER_AMPHORA; piece++)
            FlagSet(FLAG_ICHOR_SHERDS_START + i * ICHOR_SHERDS_PER_AMPHORA + piece);
        EXPECT_EQ(Ichor_DeedState(gSpecialVar_0x8004), ICHOR_DEED_OPEN);
        EXPECT_EQ(Ichor_BufferDeed(), TRUE);
        EXPECT(Contains(COMPOUND_STRING("Ready for Daphne's shelf.")));
        EXPECT(!FlagGet(FLAG_ICHOR_AMPHORAE_START + i));
        FlagSet(FLAG_ICHOR_AMPHORAE_START + i);
        EXPECT_EQ(Ichor_DeedState(gSpecialVar_0x8004), i < 3 ? ICHOR_DEED_OPEN : ICHOR_DEED_RECORDED);
        EXPECT_EQ(Ichor_BufferDeed(), TRUE);
        EXPECT(Contains(COMPOUND_STRING("Restored.")));
        EXPECT_EQ(gSpecialVar_0x8004, ICHOR_DEED_AMPHORA_START + i);
        EXPECT(StringLength(gStringVar4) < sizeof(gStringVar4));
    }
    FlagSet(FLAG_ICHOR_KRONION_ALTAR_STONE);
    FlagSet(FLAG_ICHOR_ELEUSA_PERSENYX);
    FlagSet(FLAG_ICHOR_HOLLOW_RAKNIT);
    for (i = 0; i < 3; i++)
        EXPECT_EQ(Ichor_DeedState(ICHOR_DEED_AMPHORA_START + i), ICHOR_DEED_DONE);
}

TEST("Ichor: Athena's Stylus adds hints only to open Deeds")
{
    u32 i;
    ResetDeeds();
    FlagSet(FLAG_ICHOR_GOT_TROWEL);
    for (i = 0; i < 7; i++)
        FlagSet(FLAG_ICHOR_PAGES_START + i);
    EXPECT_EQ(Ichor_DeedState(11), ICHOR_DEED_DONE);
    FlagClear(FLAG_ICHOR_PAGES_START + 6);
    for (i = 0; i < 12; i++)
    {
        FlagSet(FLAG_ICHOR_ATHENAS_STYLUS);
        gSpecialVar_0x8004 = i;
        if (Ichor_DeedState(i) == ICHOR_DEED_OPEN)
        {
            EXPECT_EQ(Ichor_BufferDeed(), TRUE);
            EXPECT(Contains(COMPOUND_STRING("Athena's hint:")));
            FlagClear(FLAG_ICHOR_ATHENAS_STYLUS);
            EXPECT_EQ(Ichor_BufferDeed(), TRUE);
            EXPECT(!Contains(COMPOUND_STRING("Athena's hint:")));
        }
    }
    FlagSet(FLAG_ICHOR_ATHENAS_STYLUS);
    FlagSet(FLAG_ICHOR_GOT_STARTER);
    gSpecialVar_0x8004 = 0;
    EXPECT_EQ(Ichor_BufferDeed(), TRUE);
    EXPECT(!Contains(COMPOUND_STRING("Athena's hint:")));
    for (i = 0; i < 7; i++)
        FlagClear(FLAG_ICHOR_PAGES_START + i);
    gSpecialVar_0x8004 = 11;
    EXPECT_EQ(Ichor_BufferDeed(), TRUE);
    EXPECT(Contains(COMPOUND_STRING("Glykera")));
    FlagSet(FLAG_ICHOR_PAGES_START);
    EXPECT_EQ(Ichor_BufferDeed(), TRUE);
    EXPECT(Contains(COMPOUND_STRING("lowest hall")));
    FlagSet(FLAG_ICHOR_PAGES_START + 1);
    EXPECT_EQ(Ichor_BufferDeed(), TRUE);
    EXPECT(Contains(COMPOUND_STRING("beyond Eleusa")));
}

TEST("Ichor: Deeds calendar covers all 36 days and preserves its page id")
{
    u32 day;
    for (day = 0; day < 72; day++)
    {
        VarSet(VAR_DAYS, day);
        gSpecialVar_0x8004 = ICHOR_DEED_CALENDAR;
        EXPECT_EQ(Ichor_BufferDeed(), TRUE);
        EXPECT_EQ(gSpecialVar_0x8004, ICHOR_DEED_CALENDAR);
        if ((day / 3) % 12 == ICHOR_MONTH_MAIMAKTERION)
            EXPECT(Contains(COMPOUND_STRING("No festival this month.")));
        else if (day % 3 == 1)
            EXPECT(Contains(COMPOUND_STRING("today.")));
        else
            EXPECT(Contains(day % 3 == 0 ? COMPOUND_STRING("1 day.") : COMPOUND_STRING("35 days.")));
    }
}
