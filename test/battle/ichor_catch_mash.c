// Ichor: the catch mash (src/ichor_catch.c, design/ENGINE_API.md §12).
// Tapping A as you throw multiplies the modified catch rate, up to a cap,
// and never turns a throw into a sure catch.
#include "global.h"
#include "ichor_catch.h"
#include "test/battle.h"

TEST("Catch mash: no presses leaves every catch rate unchanged")
{
    for (u32 odds = 0; odds <= 1000; odds++)
        EXPECT_EQ(Ichor_ApplyCatchMash(odds, 0), odds);
}

TEST("Catch mash: the bonus scales with presses up to the cap")
{
    static const u8 sCases[][2] = { {1, 103}, {5, 115}, {9, 127}, {10, 130}, {11, 130}, {50, 130} };

    ASSUME(ICHOR_CATCH_MASH_CAP == 10 && ICHOR_CATCH_MASH_MAX_BONUS == 30);
    for (u32 i = 0; i < ARRAY_COUNT(sCases); i++)
        EXPECT_EQ(Ichor_ApplyCatchMash(100, sCases[i][0]), sCases[i][1]);
}

TEST("Catch mash: the cap multiplies the catch rate by 1.3")
{
    ASSUME(ICHOR_CATCH_MASH_MAX_BONUS == 30);
    EXPECT_EQ(Ichor_ApplyCatchMash(10, ICHOR_CATCH_MASH_CAP), 13);
    EXPECT_EQ(Ichor_ApplyCatchMash(50, ICHOR_CATCH_MASH_CAP), 65);
    EXPECT_EQ(Ichor_ApplyCatchMash(150, ICHOR_CATCH_MASH_CAP), 195);
}

TEST("Catch mash: never reaches the auto-catch line, and leaves sure catches alone")
{
    // 255 and above skip the shake rolls; mashing must stop one short of them.
    for (u32 odds = 0; odds <= ICHOR_CATCH_MASH_ODDS_CEILING; odds++)
        EXPECT_LE(Ichor_ApplyCatchMash(odds, ICHOR_CATCH_MASH_CAP), ICHOR_CATCH_MASH_ODDS_CEILING);
    EXPECT_EQ(Ichor_ApplyCatchMash(250, ICHOR_CATCH_MASH_CAP), ICHOR_CATCH_MASH_ODDS_CEILING);
    EXPECT_EQ(Ichor_ApplyCatchMash(255, ICHOR_CATCH_MASH_CAP), 255);
    EXPECT_EQ(Ichor_ApplyCatchMash(0xFFFFFFFF, ICHOR_CATCH_MASH_CAP), 0xFFFFFFFF); // the Master Ball
}

TEST("Catch mash: a throw spends its presses, so the next throw starts from vanilla")
{
    gIchorCatchMash.presses = ICHOR_CATCH_MASH_CAP;
    EXPECT_EQ(Ichor_TakeCatchMash(100), Ichor_ApplyCatchMash(100, ICHOR_CATCH_MASH_CAP));
    EXPECT_EQ(gIchorCatchMash.baseOdds, 100);
    EXPECT_EQ(gIchorCatchMash.finalOdds, Ichor_ApplyCatchMash(100, ICHOR_CATCH_MASH_CAP));
    EXPECT_EQ(gIchorCatchMash.presses, 0);
    EXPECT_EQ(Ichor_TakeCatchMash(100), 100);
}

WILD_BATTLE_TEST("Catch mash: a throw with no presses keeps the vanilla catch chance")
{
    u32 recordedOdds;

    GIVEN {
        ASSUME(gSpeciesInfo[SPECIES_CLEFFA].catchRate == 150);
        WITH_CONFIG(B_MISSING_BADGE_CATCH_MALUS, GEN_7);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_CLEFFA) { Level(30); }
    } WHEN {
        TURN { USE_ITEM(player, ITEM_POKE_BALL); }
    } SCENE {
        CATCHING_CHANCE(&recordedOdds);
    } THEN {
        // Full HP: 150 / 3 = 50, as in capture.c's level-30 cases.
        EXPECT_EQ(recordedOdds, 50);
        EXPECT_EQ(gIchorCatchMash.presses, 0);
    }
}
