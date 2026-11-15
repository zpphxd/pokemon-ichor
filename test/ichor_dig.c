// Ichor: excavation (design/SYSTEMS.md §5, design/ENGINE_API.md §8): the daily
// rolls, their rerolls and the blessings; fixed finds' fallbacks.
#include "global.h"
#include "event_data.h"
#include "item.h"
#include "ichor_dig.h"
#include "ichor_rites.h"
#include "ichor_save.h"
#include "test/test.h"
#include "constants/ichor.h"
#include "constants/items.h"

u16 Ichor_DigStart(void);
u16 Ichor_DigFindKind(void);
void Ichor_DigFinish(void);

#define ROLLS 2000

static void ResetDig(void)
{
    u32 i;
    for (i = 0; i < ICHOR_AMPHORA_COUNT * ICHOR_SHERDS_PER_AMPHORA; i++)
        FlagClear(FLAG_ICHOR_SHERDS_START + i);
    for (i = 0; i < ICHOR_OSTRAKA_COUNT; i++)
        FlagClear(FLAG_ICHOR_OSTRAKA_START + i);
    memset(&gIchorSave.blessing, 0, sizeof(gIchorSave.blessing));
    memset(gIchorSave.dailyFlags, 0, sizeof(gIchorSave.dailyFlags));
    gSaveBlock1Ptr->dailySeed = 0x5EED;
}

// Roll spot (i % 96) on day (i / 96), as the game would over many days.
static u16 Roll(u32 i, u32 table)
{
    gSaveBlock1Ptr->dailySeed = 0x5EED + (i / 96) * 7919;
    return Ichor_DigRollForTest(i % 96, table);
}

TEST("Ichor: a dig spot finds the same thing all day, and something new another day")
{
    u32 day, differs = 0;
    u16 first;
    ResetDig();
    first = Ichor_DigRollForTest(5, ICHOR_DIG_ACT_I | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_KRONOS));
    EXPECT_EQ(Ichor_DigRollForTest(5, ICHOR_DIG_ACT_I | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_KRONOS)), first);
    for (day = 1; day <= 20; day++)
    {
        gSaveBlock1Ptr->dailySeed = 0x5EED + day * 7919;
        if (Ichor_DigRollForTest(5, ICHOR_DIG_ACT_I | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_KRONOS)) != first)
            differs++;
    }
    EXPECT_GT(differs, 10);
}

TEST("Ichor: a spot gives only its own amphora's sherds, and none once the amphora is whole")
{
    u32 i, kronos = 0, other = 0, k;
    ResetDig();
    for (i = 0; i < ROLLS; i++)
    {
        u16 find = Roll(i, ICHOR_DIG_ACT_I);
        if ((find & 0xFF00) == ICHOR_FIND_SHERD(0))
            other++;
    }
    EXPECT_EQ(other, 0);  // no amphora: sherds reroll
    for (i = 0; i < ROLLS; i++)
    {
        u16 find = Roll(i, ICHOR_DIG_ACT_I | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_KRONOS));
        if (find == ICHOR_FIND_SHERD(ICHOR_AMPHORA_KRONOS))
            kronos++;
        else if ((find & 0xFF00) == ICHOR_FIND_SHERD(0))
            other++;
    }
    EXPECT_EQ(other, 0);
    EXPECT_GT(kronos, ROLLS * 16 / 100);  // the table's 22%
    EXPECT_LT(kronos, ROLLS * 28 / 100);
    for (k = 0; k < ICHOR_SHERDS_PER_AMPHORA; k++)
        FlagSet(FLAG_ICHOR_SHERDS_START + ICHOR_AMPHORA_KRONOS * ICHOR_SHERDS_PER_AMPHORA + k);
    kronos = 0;
    for (i = 0; i < ROLLS; i++)
    {
        if (Roll(i, ICHOR_DIG_ACT_I | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_KRONOS)) == ICHOR_FIND_SHERD(ICHOR_AMPHORA_KRONOS))
            kronos++;
    }
    EXPECT_EQ(kronos, 0);
}

TEST("Ichor: ostraka stop turning up once all 30 are found")
{
    u32 i, ostraka = 0;
    ResetDig();
    for (i = 0; i < ROLLS; i++)
    {
        if (Roll(i, ICHOR_DIG_ACT_II) == ICHOR_FIND_OSTRAKON)
            ostraka++;
    }
    EXPECT_GT(ostraka, ROLLS * 6 / 100);  // the table's 10%
    EXPECT_LT(ostraka, ROLLS * 14 / 100);
    for (i = 0; i < ICHOR_OSTRAKA_COUNT; i++)
        FlagSet(FLAG_ICHOR_OSTRAKA_START + i);
    for (i = 0; i < ROLLS; i++)
        EXPECT_NE(Roll(i, ICHOR_DIG_ACT_II), ICHOR_FIND_OSTRAKON);
}

TEST("Ichor: each act's table has only its own finds")
{
    u32 i;
    ResetDig();
    for (i = 0; i < ROLLS; i++)
    {
        u16 a1 = Roll(i, ICHOR_DIG_ACT_I), a3 = Roll(i, ICHOR_DIG_ACT_III);
        EXPECT_NE(a1, ITEM_RELIC_SILVER);
        EXPECT_NE(a1, ITEM_RELIC_GOLD);
        EXPECT_NE(a1, ITEM_RARE_BONE);
        EXPECT_NE(a1, ITEM_COMET_SHARD);
        EXPECT_NE(a1, ITEM_BOTTLE_CAP);
        EXPECT_NE(a3, ITEM_RELIC_COPPER);
        EXPECT_NE(a3, ITEM_PEARL);
        EXPECT_NE(a3, ITEM_HARD_STONE);
    }
}

TEST("Ichor: Demeter's blessing digs up rarer finds, and Hades's doubles an item")
{
    u32 i, plainSherds = 0, demeterSherds = 0, plainPearls = 0, demeterPearls = 0;
    ResetDig();
    for (i = 0; i < ROLLS; i++)
    {
        u16 find = Roll(i, ICHOR_DIG_ACT_I | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_KRONOS));
        plainSherds += (find == ICHOR_FIND_SHERD(ICHOR_AMPHORA_KRONOS));
        plainPearls += (find == ITEM_PEARL);
    }
    Ichor_SetBlessingTo(ICHOR_GOD_DEMETER, 1000, 0);
    for (i = 0; i < ROLLS; i++)
    {
        u16 find = Roll(i, ICHOR_DIG_ACT_I | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_KRONOS));
        demeterSherds += (find == ICHOR_FIND_SHERD(ICHOR_AMPHORA_KRONOS));
        demeterPearls += (find == ITEM_PEARL);
    }
    EXPECT_LT(demeterSherds, plainSherds * 3 / 4);  // the commonest find, rarer
    EXPECT_GT(demeterPearls, plainPearls * 3 / 2);  // the rarest, commoner

    // Hades: an item find comes up twice; a sherd is still one sherd
    ResetDig();
    Ichor_SetBlessingTo(ICHOR_GOD_HADES, 1000, 0);
    AddBagItem(ITEM_ALETHEAS_TROWEL, 1);
    for (i = 0; i < 96; i++)
    {
        gSpecialVar_0x8004 = i;
        gSpecialVar_0x8005 = ICHOR_DIG_ACT_I;
        gSpecialVar_0x8006 = ICHOR_DIG_MODE_SPOT;
        EXPECT_EQ(Ichor_DigStart(), ICHOR_DIG_READY);
        if (Ichor_DigFindKind() == ICHOR_FIND_KIND_ITEM)
        {
            EXPECT_EQ(gSpecialVar_0x8007, 2);
            break;
        }
    }
    EXPECT_LT(i, 96);
    RemoveBagItem(ITEM_ALETHEAS_TROWEL, 1);
    memset(&gIchorSave.blessing, 0, sizeof(gIchorSave.blessing));
}

TEST("Ichor: a fixed dig needs the Trowel, digs once, and pays Stardust for a whole amphora")
{
    u32 k;
    ResetDig();
    FlagClear(FLAG_ICHOR_DIG_FIXED_START + 63);
    gSpecialVar_0x8004 = 63;
    gSpecialVar_0x8005 = ICHOR_FIND_SHERD(ICHOR_AMPHORA_ICARUS);
    gSpecialVar_0x8006 = ICHOR_DIG_MODE_FIXED;
    EXPECT_EQ(Ichor_DigStart(), ICHOR_DIG_NO_TROWEL);

    AddBagItem(ITEM_ALETHEAS_TROWEL, 1);
    for (k = 0; k < ICHOR_SHERDS_PER_AMPHORA; k++)
        FlagSet(FLAG_ICHOR_SHERDS_START + ICHOR_AMPHORA_ICARUS * ICHOR_SHERDS_PER_AMPHORA + k);
    EXPECT_EQ(Ichor_DigStart(), ICHOR_DIG_READY);
    EXPECT_EQ(Ichor_DigFindKind(), ICHOR_FIND_KIND_ITEM);
    EXPECT_EQ(gSpecialVar_0x8006, ITEM_STARDUST);
    Ichor_DigFinish();
    EXPECT(FlagGet(FLAG_ICHOR_DIG_FIXED_START + 63));
    gSpecialVar_0x8006 = ICHOR_DIG_MODE_FIXED;  // Ichor_DigFindKind put the item there
    EXPECT_EQ(Ichor_DigStart(), ICHOR_DIG_BARE);

    FlagClear(FLAG_ICHOR_DIG_FIXED_START + 63);
    RemoveBagItem(ITEM_ALETHEAS_TROWEL, 1);
    ResetDig();
}
