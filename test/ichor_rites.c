// Ichor: the rites' rules (design/SYSTEMS.md §3, src/ichor_rites.c). The altar's
// screens are checked in game by tools/ichor/tests/ichor_rites.sh; these check
// the numbers: Favor by taste, temples, Hestia's share, prayers, ranks, blessing
// lengths, Dionysus's Revel, the step countdown, the gifts, and every hook.
#include "global.h"
#include "event_data.h"
#include "ichor_relics.h"
#include "ichor_rites.h"
#include "ichor_save.h"
#include "item.h"
#include "pokemon.h"
#include "test/test.h"
#include "constants/ichor.h"
#include "constants/items.h"
#include "constants/moves.h"

void Ichor_MakeOffering(void);
void Ichor_Pray(void);
u16 Ichor_NextGiftDue(void);
u16 Ichor_GetBlessingGod(void);
void Ichor_TakeGift(void);

#define TASTE_ACCEPT 0
#define TASTE_LIKE   1
#define TASTE_LOVE   2
#define TASTE_REFUSE 3

static void ResetRites(void)
{
    u32 god;
    memset(gIchorSave.favor, 0, sizeof(gIchorSave.favor));
    memset(&gIchorSave.blessing, 0, sizeof(gIchorSave.blessing));
    memset(gIchorSave.dailyFlags, 0, sizeof(gIchorSave.dailyFlags));
    for (god = 0; god < ICHOR_GOD_COUNT; god++)
    {
        FlagClear(FLAG_ICHOR_GIFT(god, ICHOR_GIFT_I));
        FlagClear(FLAG_ICHOR_GIFT(god, ICHOR_GIFT_II));
        FlagClear(FLAG_ICHOR_GIFT(god, ICHOR_GIFT_III));
    }
    FlagClear(FLAG_ICHOR_EVER_EMBER);
    FlagClear(FLAG_ICHOR_HARVEST_BASKET);
    FlagClear(FLAG_ICHOR_THREE_FLAMED_TORCH);
    gSpecialVar_0x800B = FALSE;
}

static u32 Offer(u32 god, u32 item)
{
    gSpecialVar_0x800A = god;
    AddBagItem(item, 1);
    gSpecialVar_0x8006 = item;
    Ichor_MakeOffering();
    return gSpecialVar_Result;
}

TEST("Ichor: an offering's Favor follows the god's taste")
{
    ResetRites();
    EXPECT_EQ(Offer(ICHOR_GOD_DEMETER, ITEM_BARLEY_CAKE), TASTE_LOVE);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_DEMETER), 5);
    EXPECT_EQ(CountTotalItemQuantityInBag(ITEM_BARLEY_CAKE), 0);
    EXPECT_EQ(Offer(ICHOR_GOD_DEMETER, ITEM_ORAN_BERRY), TASTE_LIKE);       // first fruits
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_DEMETER), 8);
    EXPECT_EQ(Offer(ICHOR_GOD_DEMETER, ITEM_HONEY), TASTE_ACCEPT);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_DEMETER), 9);
    EXPECT_EQ(Offer(ICHOR_GOD_ARTEMIS, ITEM_SWIFT_FEATHER), TASTE_LOVE);    // any feather
    EXPECT_EQ(Offer(ICHOR_GOD_POSEIDON, ITEM_HEART_SCALE), TASTE_LOVE);     // a sea gift
    EXPECT_EQ(Offer(ICHOR_GOD_HERA, ITEM_POMEG_BERRY), TASTE_LOVE);         // her pomegranate
}

TEST("Ichor: Demeter refuses the pomegranate, and the player keeps it")
{
    ResetRites();
    RemoveBagItem(ITEM_POMEG_BERRY, CountTotalItemQuantityInBag(ITEM_POMEG_BERRY));
    EXPECT_EQ(Offer(ICHOR_GOD_DEMETER, ITEM_POMEG_BERRY), TASTE_REFUSE);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_DEMETER), 0);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_HESTIA), 0);
    EXPECT_EQ(CountTotalItemQuantityInBag(ITEM_POMEG_BERRY), 1);
    EXPECT_EQ(Ichor_GetBlessingGod(), ICHOR_GOD_NONE);
}

TEST("Ichor: temple altars double Favor, and Hestia takes +1 of every offering")
{
    ResetRites();
    gSpecialVar_0x800B = TRUE;
    Offer(ICHOR_GOD_APOLLO, ITEM_LAUREL_SPRIG);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_APOLLO), 10);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_HESTIA), 1);
    gSpecialVar_0x800B = FALSE;
    Offer(ICHOR_GOD_HESTIA, ITEM_OLIVE_OIL);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_HESTIA), 6);  // her own offering: no extra share
}

TEST("Ichor: the first prayer each day gives +1 Favor, and a minor blessing")
{
    ResetRites();
    gSpecialVar_0x800A = ICHOR_GOD_ATHENA;
    Ichor_Pray();
    Ichor_Pray();
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_ATHENA), 1);
    EXPECT_EQ(gIchorSave.blessing.god, ICHOR_GOD_ATHENA);
    EXPECT_EQ(gIchorSave.blessing.steps, 100);
    EXPECT_EQ(gIchorSave.blessing.flags & ICHOR_BLESSING_MAJOR, 0);
    Ichor_DoDailyEvents(1);
    Ichor_AddFavorTo(ICHOR_GOD_ATHENA, 9);
    Ichor_Pray();
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_ATHENA), 11);
    EXPECT_EQ(gIchorSave.blessing.steps, 150);  // Known: a longer prayer blessing
}

TEST("Ichor: Favor caps at 100 and never drops")
{
    ResetRites();
    Ichor_AddFavorTo(ICHOR_GOD_ZEUS, 250);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_ZEUS), 100);
    Ichor_AddFavorTo(ICHOR_GOD_ZEUS, 0);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_ZEUS), 100);
}

TEST("Ichor: a blessing's length follows the offering, and the Beloved's lasts longer")
{
    ResetRites();
    Offer(ICHOR_GOD_APOLLO, ITEM_LAUREL_SPRIG);
    EXPECT_EQ(gIchorSave.blessing.steps, 500);
    Offer(ICHOR_GOD_APOLLO, ITEM_HONEY);
    EXPECT_EQ(gIchorSave.blessing.steps, 300);
    Offer(ICHOR_GOD_APOLLO, ITEM_WINE);
    EXPECT_EQ(gIchorSave.blessing.steps, 150);
    Ichor_AddFavorTo(ICHOR_GOD_APOLLO, 60);
    Offer(ICHOR_GOD_APOLLO, ITEM_LAUREL_SPRIG);
    EXPECT_EQ(gIchorSave.blessing.steps, 750);
    EXPECT(gIchorSave.blessing.flags & ICHOR_BLESSING_MAJOR);
}

TEST("Ichor: Dionysus passes on another god's blessing, or Frenzy one time in eight")
{
    u32 i, frenzies = 0, revels = 0;
    for (i = 0; i < 400; i++)
    {
        ResetRites();
        Offer(ICHOR_GOD_DIONYSUS, ITEM_WINE);
        if (gIchorSave.blessing.flags & ICHOR_BLESSING_FRENZY)
        {
            frenzies++;
            EXPECT_EQ(gIchorSave.blessing.god, ICHOR_GOD_DIONYSUS);
            EXPECT_EQ(gIchorSave.blessing.steps, 500);
        }
        else
        {
            revels++;
            EXPECT(gIchorSave.blessing.flags & ICHOR_BLESSING_REVEL);
            EXPECT_NE(gIchorSave.blessing.god, ICHOR_GOD_DIONYSUS);
            EXPECT_NE(gIchorSave.blessing.god, ICHOR_GOD_ZEUS);
            EXPECT_NE(gIchorSave.blessing.god, ICHOR_GOD_HADES);
            EXPECT_EQ(gIchorSave.blessing.steps, 750);
        }
    }
    EXPECT_GT(frenzies, 20);   // about 50 in 400
    EXPECT_LT(frenzies, 90);
    EXPECT_GT(revels, 300);
}

TEST("Ichor: a blessing counts down one step at a time, and ends")
{
    ResetRites();
    Ichor_SetBlessingTo(ICHOR_GOD_APOLLO, 2, ICHOR_BLESSING_MAJOR);
    EXPECT_EQ(Ichor_OnStep(), FALSE);
    EXPECT_EQ(gIchorSave.blessing.steps, 1);
    EXPECT(Ichor_IsBlessed(ICHOR_GOD_APOLLO));
    EXPECT_EQ(Ichor_OnStep(), TRUE);   // the fading line plays
    EXPECT_EQ(Ichor_GetBlessingGod(), ICHOR_GOD_NONE);
    EXPECT_EQ(Ichor_OnStep(), FALSE);
}

TEST("Ichor: with Ever-Ember, Hestia's Hearthfire doesn't count down")
{
    ResetRites();
    FlagSet(FLAG_ICHOR_EVER_EMBER);
    Ichor_SetBlessingTo(ICHOR_GOD_HESTIA, 1, ICHOR_BLESSING_MAJOR);
    EXPECT_EQ(Ichor_OnStep(), FALSE);
    EXPECT(Ichor_IsBlessed(ICHOR_GOD_HESTIA));
}

TEST("Ichor: gifts come at Favor 30, 60 and 100, in order")
{
    ResetRites();
    gSpecialVar_0x800A = ICHOR_GOD_HECATE;
    EXPECT_EQ(Ichor_NextGiftDue(), 0xFF);
    Ichor_AddFavorTo(ICHOR_GOD_HECATE, 30);
    EXPECT_EQ(Ichor_NextGiftDue(), ICHOR_GIFT_I);
    EXPECT_EQ(gSpecialVar_0x8005, MOVE_HEX);
    gSpecialVar_0x8005 = ICHOR_GIFT_I;
    Ichor_TakeGift();
    EXPECT_EQ(Ichor_NextGiftDue(), 0xFF);
    Ichor_AddFavorTo(ICHOR_GOD_HECATE, 70);
    EXPECT_EQ(Ichor_NextGiftDue(), ICHOR_GIFT_II);
    gSpecialVar_0x8005 = ICHOR_GIFT_II;
    Ichor_TakeGift();
    EXPECT(FlagGet(FLAG_ICHOR_THREE_FLAMED_TORCH));   // her gift II is the torch's upgrade
    EXPECT_EQ(Ichor_NextGiftDue(), ICHOR_GIFT_III);
    gSpecialVar_0x8005 = ICHOR_GIFT_III;
    Ichor_TakeGift();
    EXPECT_EQ(Ichor_NextGiftDue(), 0xFF);
    gSpecialVar_0x800A = ICHOR_GOD_APOLLO;
    Ichor_AddFavorTo(ICHOR_GOD_APOLLO, 60);
    FlagSet(FLAG_ICHOR_GIFT(ICHOR_GOD_APOLLO, ICHOR_GIFT_I));
    EXPECT_EQ(Ichor_NextGiftDue(), ICHOR_GIFT_II);
    EXPECT_EQ(gSpecialVar_0x8006, ITEM_POKE_FLUTE);   // the Lyre of Apollo
}

TEST("Ichor: Hermes, Hades and the coins in the market")
{
    ResetRites();
    EXPECT_EQ(Ichor_ModifyBuyPrice(1000), 1000);
    Ichor_SetBlessingTo(ICHOR_GOD_HERMES, 10, 0);
    EXPECT_EQ(Ichor_ModifyBuyPrice(1000), 800);
    EXPECT_EQ(Ichor_ModifySellPrice(ITEM_POTION, 100), 120);
    EXPECT_EQ(Ichor_ModifyPrizeMoney(1000), 1200);
    Ichor_SetBlessingTo(ICHOR_GOD_HADES, 10, 0);
    EXPECT_EQ(Ichor_ModifySellPrice(ITEM_RELIC_COPPER, 100), 150);
    EXPECT_EQ(Ichor_ModifySellPrice(ITEM_POTION, 100), 100);
}

TEST("Ichor: EXP, encounter rates and the sea")
{
    s32 exp = 100;
    ResetRites();
    Ichor_SetBlessingTo(ICHOR_GOD_APOLLO, 10, 0);
    Ichor_ModifyExp(&exp);
    EXPECT_EQ(exp, 120);
    Ichor_SetBlessingTo(ICHOR_GOD_ARTEMIS, 10, 0);
    EXPECT_EQ(Ichor_ModifyEncounterRate(400), 300);
    Ichor_SetBlessingTo(ICHOR_GOD_DIONYSUS, 10, ICHOR_BLESSING_MAJOR | ICHOR_BLESSING_FRENZY);
    EXPECT_EQ(Ichor_ModifyEncounterRate(400), 800);
    EXPECT_EQ(Ichor_ModifyWildLevel(10), 13);
    exp = 100;
    Ichor_ModifyExp(&exp);
    EXPECT_EQ(exp, 150);
    Ichor_SetBlessingTo(ICHOR_GOD_POSEIDON, 10, 0);
    EXPECT(Ichor_FishBitesAtOnce());
    Ichor_SetBlessingTo(ICHOR_GOD_ZEUS, 10, 0);
    EXPECT_EQ(Ichor_ExtraShinyRolls(), 1);
    Ichor_SetBlessingTo(ICHOR_GOD_HERA, 10, 0);
    EXPECT_EQ(Ichor_ExtraEggCycles(), 1);
    EXPECT_EQ(Ichor_ModifyEggChance(40), 80);
    Ichor_SetBlessingTo(ICHOR_GOD_DEMETER, 10, 0);
    EXPECT(Ichor_BoostsWildHeldItems());
    EXPECT_EQ(Ichor_ExtraBerryYield(), 1);
    Ichor_SetBlessingTo(ICHOR_GOD_ARTEMIS, 10, 0);
    EXPECT_EQ(Ichor_DexNavSneakBonus(), 2);
    Ichor_SetBlessingTo(ICHOR_GOD_ATHENA, 10, 0);
    EXPECT_EQ(Ichor_DexNavHiddenRate(25), 50);
    ResetRites();
    FlagSet(FLAG_ICHOR_HARVEST_BASKET);
    EXPECT_EQ(Ichor_ExtraBerryYield(), 1);
}

TEST("Ichor: Ares turns weak wild Pokémon away and raises the rest")
{
    ResetRites();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_WOBBUFFET, 30, 0, OTID_STRUCT_PLAYER_ID);
    EXPECT(Ichor_IsWildLevelAllowed(10));
    Ichor_SetBlessingTo(ICHOR_GOD_ARES, 10, 0);
    EXPECT(!Ichor_IsWildLevelAllowed(25));
    EXPECT(Ichor_IsWildLevelAllowed(26));
    EXPECT_EQ(Ichor_ModifyWildLevel(26), 28);
}

TEST("Ichor: Aphrodite doubles friendship, and the Myrtle Wreath stops it falling")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];
    u16 wreath = ITEM_MYRTLE_WREATH, none = ITEM_NONE;
    ResetRites();
    CreateMon(mon, SPECIES_WOBBUFFET, 30, 0, OTID_STRUCT_PLAYER_ID);
    EXPECT_EQ(Ichor_ModifyFriendshipDelta(mon, 3), 3);
    Ichor_SetBlessingTo(ICHOR_GOD_APHRODITE, 10, 0);
    EXPECT_EQ(Ichor_ModifyFriendshipDelta(mon, 3), 6);
    EXPECT_EQ(Ichor_ModifyFriendshipDelta(mon, -5), -5);
    SetMonData(mon, MON_DATA_HELD_ITEM, &wreath);
    EXPECT_EQ(Ichor_ModifyFriendshipDelta(mon, -5), 0);
    SetMonData(mon, MON_DATA_HELD_ITEM, &none);
}
