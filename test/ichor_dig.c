// Ichor: excavation (design/SYSTEMS.md §5, design/ENGINE_API.md §8): the daily
// rolls, their rerolls and the blessings; fixed finds' fallbacks.
#include "global.h"
#include "event_data.h"
#include "item.h"
#include "money.h"
#include "string_util.h"
#include "ichor_dig.h"
#include "ichor_rites.h"
#include "ichor_save.h"
#include "test/test.h"
#include "constants/ichor.h"
#include "constants/items.h"

u16 Ichor_DigStart(void);
u16 Ichor_DigFindKind(void);
void Ichor_DigFinish(void);
u16 Ichor_SellToMoneychanger(void);
u16 Ichor_QuoteToMoneychanger(void);

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

static void ResetAmphorae(void)
{
    u32 i;
    ResetDig();
    for (i = 0; i < ICHOR_AMPHORA_COUNT; i++)
        FlagClear(FLAG_ICHOR_AMPHORAE_START + i);
    memset(gIchorSave.favor, 0, sizeof(gIchorSave.favor));
}

TEST("Ichor: all twelve amphorae need four sherds and explicit restoration")
{
    u32 amphora, piece;
    ResetAmphorae();
    for (amphora = 0; amphora < ICHOR_AMPHORA_COUNT; amphora++)
    {
        gSpecialVar_0x8004 = amphora;
        EXPECT_EQ(Ichor_AmphoraStatus(amphora), ICHOR_AMPHORA_INCOMPLETE);
        for (piece = 0; piece < ICHOR_SHERDS_PER_AMPHORA - 1; piece++)
        {
            FlagSet(FLAG_ICHOR_SHERDS_START + amphora * ICHOR_SHERDS_PER_AMPHORA + piece);
            EXPECT_EQ(Ichor_RestoreAmphora(), ICHOR_AMPHORA_INCOMPLETE);
            EXPECT(!FlagGet(FLAG_ICHOR_AMPHORAE_START + amphora));
        }
        EXPECT_EQ(Ichor_BufferAmphoraNotes(), FALSE);
        FlagSet(FLAG_ICHOR_SHERDS_START + amphora * ICHOR_SHERDS_PER_AMPHORA + piece);
        EXPECT_EQ(Ichor_BufferAmphora(), ICHOR_AMPHORA_READY);
        EXPECT(!FlagGet(FLAG_ICHOR_AMPHORAE_START + amphora));
        EXPECT_EQ(Ichor_RestoreAmphora(), ICHOR_AMPHORA_RESTORED);
        EXPECT_EQ(Ichor_CountFlags(FLAG_ICHOR_AMPHORAE_START, ICHOR_AMPHORA_COUNT), amphora + 1);
        EXPECT_EQ(Ichor_CountFlags(FLAG_ICHOR_SHERDS_START + amphora * ICHOR_SHERDS_PER_AMPHORA,
                                  ICHOR_SHERDS_PER_AMPHORA), ICHOR_SHERDS_PER_AMPHORA);
        EXPECT_EQ(Ichor_BufferAmphoraNotes(), TRUE);
        EXPECT(StringLength(gStringVar4) > 80 && StringLength(gStringVar4) < sizeof(gStringVar4));
    }
}

TEST("Ichor: invalid amphora ids cannot read notes or alter collection state")
{
    ResetAmphorae();
    gSpecialVar_0x8004 = ICHOR_AMPHORA_COUNT;
    EXPECT_EQ(Ichor_BufferAmphora(), ICHOR_AMPHORA_INVALID);
    EXPECT_EQ(Ichor_RestoreAmphora(), ICHOR_AMPHORA_INVALID);
    EXPECT_EQ(Ichor_BufferAmphoraNotes(), FALSE);
    gSpecialVar_0x8004 = 0xFFFF;
    EXPECT_EQ(Ichor_RestoreAmphora(), ICHOR_AMPHORA_INVALID);
    EXPECT_EQ(Ichor_AmphoraStatus(0xFFFFFFFF), ICHOR_AMPHORA_INVALID);
    EXPECT_EQ(Ichor_CountFlags(FLAG_ICHOR_AMPHORAE_START, ICHOR_AMPHORA_COUNT), 0);
    EXPECT_EQ(Ichor_CountFlags(FLAG_ICHOR_SHERDS_START, ICHOR_AMPHORA_COUNT * ICHOR_SHERDS_PER_AMPHORA), 0);
}

TEST("Ichor: restoration grants Hephaestus and Aphrodite Favor once, capped at 100")
{
    static const u8 amphorae[] = { ICHOR_AMPHORA_HEPHAESTUS, ICHOR_AMPHORA_PARIS };
    static const u8 gods[] = { ICHOR_GOD_HEPHAESTUS, ICHOR_GOD_APHRODITE };
    u32 i, piece, capped;

    for (capped = 0; capped < 2; capped++)
    {
        ResetAmphorae();
        for (i = 0; i < ARRAY_COUNT(amphorae); i++)
        {
            gIchorSave.favor[gods[i]] = capped ? 98 : 10;
            for (piece = 0; piece < ICHOR_SHERDS_PER_AMPHORA; piece++)
                FlagSet(FLAG_ICHOR_SHERDS_START + amphorae[i] * ICHOR_SHERDS_PER_AMPHORA + piece);
            gSpecialVar_0x8004 = amphorae[i];
            EXPECT_EQ(Ichor_RestoreAmphora(), ICHOR_AMPHORA_RESTORED);
            EXPECT_EQ(Ichor_GetFavor(gods[i]), capped ? 100 : 15);
            EXPECT_EQ(Ichor_RestoreAmphora(), ICHOR_AMPHORA_RESTORED);
            EXPECT_EQ(Ichor_GetFavor(gods[i]), capped ? 100 : 15);
        }
    }
}

TEST("Ichor: legacy restored amphorae remain readable without duplicate Favor")
{
    ResetAmphorae();
    FlagSet(FLAG_ICHOR_AMPHORAE_START + ICHOR_AMPHORA_HEPHAESTUS);
    gSpecialVar_0x8004 = ICHOR_AMPHORA_HEPHAESTUS;
    EXPECT_EQ(Ichor_BufferAmphora(), ICHOR_AMPHORA_RESTORED);
    EXPECT_EQ(Ichor_BufferAmphoraNotes(), TRUE);
    EXPECT_EQ(Ichor_RestoreAmphora(), ICHOR_AMPHORA_RESTORED);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_HEPHAESTUS), 0);
    EXPECT_EQ(Ichor_CountFlags(FLAG_ICHOR_SHERDS_START, ICHOR_AMPHORA_COUNT * ICHOR_SHERDS_PER_AMPHORA), 0);
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

TEST("Ichor: a moneychanger buys a coin at the market's price plus his percent")
{
    u32 money;
    memset(&gIchorSave.blessing, 0, sizeof(gIchorSave.blessing));
    SetMoney(&gSaveBlock1Ptr->money, 0);
    AddBagItem(ITEM_RELIC_SILVER, 1);
    gSpecialVar_0x8004 = ITEM_RELIC_SILVER;
    gSpecialVar_0x8005 = 20;
    EXPECT_EQ(Ichor_SellToMoneychanger(), TRUE);
    money = GetMoney(&gSaveBlock1Ptr->money);
    EXPECT_EQ(money, 2400);                     // the Silver Owl sells for 2,000; +20%
    EXPECT(!CheckBagHasItem(ITEM_RELIC_SILVER, 1));
    EXPECT_EQ(Ichor_SellToMoneychanger(), FALSE); // none left
    EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), money);

    Ichor_SetBlessingTo(ICHOR_GOD_HADES, 100, 0);  // Hades: +50% on the coins, then his +20%
    AddBagItem(ITEM_RELIC_COPPER, 1);
    gSpecialVar_0x8004 = ITEM_RELIC_COPPER;
    EXPECT_EQ(Ichor_SellToMoneychanger(), TRUE);
    EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), money + 900);
    memset(&gIchorSave.blessing, 0, sizeof(gIchorSave.blessing));
    SetMoney(&gSaveBlock1Ptr->money, 0);
}

TEST("Ichor: moneychanger quotes preserve all three coins and reject incomplete payments")
{
    static const u16 coins[] = {ITEM_RELIC_COPPER, ITEM_RELIC_SILVER, ITEM_RELIC_GOLD};
    static const u32 prices[] = {600, 2400, 6000};
    u32 i;

    memset(&gIchorSave.blessing, 0, sizeof(gIchorSave.blessing));
    gSpecialVar_0x8005 = 20;
    for (i = 0; i < ARRAY_COUNT(coins); i++)
    {
        EXPECT(AddBagItem(coins[i], 1));
        gSpecialVar_0x8004 = coins[i];
        SetMoney(&gSaveBlock1Ptr->money, MAX_MONEY - prices[i] + 1);
        EXPECT_EQ(Ichor_QuoteToMoneychanger(), FALSE);
        EXPECT_EQ(Ichor_SellToMoneychanger(), FALSE);
        EXPECT(CheckBagHasItem(coins[i], 1));
        EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), MAX_MONEY - prices[i] + 1);

        SetMoney(&gSaveBlock1Ptr->money, MAX_MONEY - prices[i]);
        EXPECT_EQ(Ichor_QuoteToMoneychanger(), TRUE);
        EXPECT(CheckBagHasItem(coins[i], 1));
        EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), MAX_MONEY - prices[i]);
        EXPECT_EQ(Ichor_SellToMoneychanger(), TRUE);
        EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), MAX_MONEY);
        EXPECT(!CheckBagHasItem(coins[i], 1));
        EXPECT_EQ(Ichor_QuoteToMoneychanger(), FALSE);
    }
    SetMoney(&gSaveBlock1Ptr->money, 0);
}
