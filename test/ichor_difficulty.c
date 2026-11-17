#include "global.h"
#include "caps.h"
#include "data.h"
#include "difficulty.h"
#include "event_data.h"
#include "ichor_save.h"
#include "item_use.h"
#include "party_menu.h"
#include "pokemon.h"
#include "test/test.h"
#include "constants/items.h"
#include "constants/species.h"

static void ResetDifficulty(void)
{
    Ichor_InitSave();
    VarSet(B_VAR_DIFFICULTY, DIFFICULTY_EASY);
}

TEST("Ichor: unchosen and legacy saves remain Hero despite the zeroed difficulty var")
{
    ResetDifficulty();
    EXPECT_EQ(GetCurrentDifficultyLevel(), DIFFICULTY_NORMAL);
    EXPECT_EQ(GetCurrentLevelCap(), MAX_LEVEL);
    EXPECT_EQ(Ichor_GetStepGlassLimit(), 120);
    Ichor_OnSaveLoaded();
    EXPECT_EQ(GetCurrentDifficultyLevel(), DIFFICULTY_NORMAL);
}

TEST("Ichor: the confirmed difficulty is save-fixed and survives loading")
{
    u32 difficulty;
    for (difficulty = DIFFICULTY_EASY; difficulty <= DIFFICULTY_HARD; difficulty++)
    {
        ResetDifficulty();
        gSpecialVar_0x8004 = difficulty;
        EXPECT_EQ(Ichor_ChooseDifficulty(), TRUE);
        EXPECT(FlagGet(FLAG_ICHOR_DIFFICULTY_CHOSEN));
        EXPECT_EQ(GetCurrentDifficultyLevel(), difficulty);
        if (difficulty == DIFFICULTY_HARD)
            EXPECT(gSaveBlock2Ptr->optionsBattleStyle == OPTIONS_BATTLE_STYLE_SET);
        Ichor_OnSaveLoaded();
        EXPECT_EQ(GetCurrentDifficultyLevel(), difficulty);
        gSpecialVar_0x8004 = (difficulty + 1) % 3;
        EXPECT_EQ(Ichor_ChooseDifficulty(), FALSE);
        EXPECT_EQ(GetCurrentDifficultyLevel(), difficulty);
    }
    ResetDifficulty();
}

TEST("Ichor: an invalid difficulty selection cannot lock the save")
{
    ResetDifficulty();
    gSpecialVar_0x8004 = 99;
    EXPECT_EQ(Ichor_ChooseDifficulty(), FALSE);
    EXPECT(!FlagGet(FLAG_ICHOR_DIFFICULTY_CHOSEN));
    EXPECT_EQ(GetCurrentDifficultyLevel(), DIFFICULTY_NORMAL);
}

TEST("Ichor: Spartan caps follow the Act I boss aces and the next chapter")
{
    FlagClear(FLAG_BADGE01_GET);
    FlagClear(FLAG_BADGE02_GET);
    FlagClear(FLAG_BADGE03_GET);
    SetCurrentDifficultyLevel(DIFFICULTY_HARD);
    EXPECT(IsHardLevelCapEnabled());
    EXPECT_EQ(GetCurrentLevelCap(), 14);
    FlagSet(FLAG_BADGE01_GET);
    EXPECT_EQ(GetCurrentLevelCap(), 20);
    FlagSet(FLAG_BADGE02_GET);
    EXPECT_EQ(GetCurrentLevelCap(), 26);
    FlagSet(FLAG_BADGE03_GET);
    EXPECT_EQ(GetCurrentLevelCap(), 32);
    SetCurrentDifficultyLevel(DIFFICULTY_EASY);
    EXPECT_EQ(GetCurrentLevelCap(), MAX_LEVEL);
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    EXPECT_EQ(GetCurrentLevelCap(), MAX_LEVEL);
    FlagClear(FLAG_BADGE01_GET);
    FlagClear(FLAG_BADGE02_GET);
    FlagClear(FLAG_BADGE03_GET);
    ResetDifficulty();
}

TEST("Ichor: Spartan stops cap-level EXP while Hero and Mortal retain ordinary EXP")
{
    FlagClear(FLAG_BADGE01_GET);
    SetCurrentDifficultyLevel(DIFFICULTY_HARD);
    EXPECT_EQ(GetSoftLevelCapExpValue(13, 500), 500);
    EXPECT_EQ(GetSoftLevelCapExpValue(14, 500), 0);
    EXPECT_EQ(GetSoftLevelCapExpValue(15, 500), 0);
    SetCurrentDifficultyLevel(DIFFICULTY_EASY);
    EXPECT_EQ(GetSoftLevelCapExpValue(14, 500), 500);
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    EXPECT_EQ(GetSoftLevelCapExpValue(14, 500), 500);
    ResetDifficulty();
}

TEST("Ichor: Kaldera caps follow Talos, Hyperion and the next Laurel")
{
    u32 i;
    for (i = FLAG_BADGE01_GET; i <= FLAG_BADGE05_GET; i++)
        FlagSet(i);
    FlagSet(FLAG_ICHOR_AKROPOLIS_RAID_DONE);
    FlagClear(FLAG_BADGE06_GET);
    FlagClear(FLAG_ICHOR_KALDERA_FRAGMENT_LOST);
    SetCurrentDifficultyLevel(DIFFICULTY_HARD);
    EXPECT_EQ(GetCurrentLevelCap(), 43);
    FlagSet(FLAG_BADGE06_GET);
    EXPECT_EQ(GetCurrentLevelCap(), 44);
    FlagSet(FLAG_ICHOR_KALDERA_FRAGMENT_LOST);
    EXPECT_EQ(GetCurrentLevelCap(), 48);
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    EXPECT_EQ(GetCurrentLevelCap(), MAX_LEVEL);
    for (i = FLAG_BADGE01_GET; i <= FLAG_BADGE06_GET; i++)
        FlagClear(i);
    FlagClear(FLAG_ICHOR_AKROPOLIS_RAID_DONE);
    FlagClear(FLAG_ICHOR_KALDERA_FRAGMENT_LOST);
    ResetDifficulty();
}

TEST("Ichor: Hermes and the Thread share the 150, 120 and 100 step difficulty limits")
{
    SetCurrentDifficultyLevel(DIFFICULTY_EASY);
    EXPECT_EQ(Ichor_GetStepGlassLimit(), 150);
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    EXPECT_EQ(Ichor_GetStepGlassLimit(), 120);
    SetCurrentDifficultyLevel(DIFFICULTY_HARD);
    EXPECT_EQ(Ichor_GetStepGlassLimit(), 100);
    EXPECT_EQ(GetTrainerAIFlagsFromId(1) & AI_FLAG_SMART_TRAINER, AI_FLAG_SMART_TRAINER);
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    EXPECT_EQ(GetTrainerAIFlagsFromId(1), GetTrainerStructFromId(1)->aiFlags);
    ResetDifficulty();
}

TEST("Ichor: EXP Candy cannot bank experience above the Spartan cap")
{
    struct Pokemon mon;
    enum GrowthRate growthRate = gSpeciesInfo[SPECIES_NEBREL].growthRate;
    FlagClear(FLAG_BADGE01_GET);
    SetCurrentDifficultyLevel(DIFFICULTY_HARD);
    CreateMon(&mon, SPECIES_NEBREL, 13, 0, OTID_STRUCT_PLAYER_ID);
    EXPECT(!ExecuteTableBasedItemEffect(&mon, ITEM_EXP_CANDY_XL, 0, 0));
    EXPECT_EQ(GetMonData(&mon, MON_DATA_LEVEL), 14);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_EXP), gExperienceTables[growthRate][14]);
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    CreateMon(&mon, SPECIES_NEBREL, 13, 0, OTID_STRUCT_PLAYER_ID);
    EXPECT(!ExecuteTableBasedItemEffect(&mon, ITEM_EXP_CANDY_XL, 0, 0));
    EXPECT_GT(GetMonData(&mon, MON_DATA_LEVEL), 14);
    ResetDifficulty();
}

TEST("Ichor: Spartan refuses healing and escape items without changing Hero healing")
{
    struct Pokemon mon;
    u32 hp = 1;
    CreateMon(&mon, SPECIES_NEBREL, 5, 0, OTID_STRUCT_PLAYER_ID);
    SetMonData(&mon, MON_DATA_HP, &hp);
    gPartyMenu.slotId = PARTY_SIZE - 1;
    SetCurrentDifficultyLevel(DIFFICULTY_HARD);
    EXPECT(CannotUseItemsInBattle(ITEM_POTION, &mon));
    EXPECT(CannotUseItemsInBattle(ITEM_POKE_DOLL, &mon));
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), 1);
    SetCurrentDifficultyLevel(DIFFICULTY_NORMAL);
    EXPECT(!CannotUseItemsInBattle(ITEM_POTION, &mon));
    ResetDifficulty();
}
