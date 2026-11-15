// Ichor: scripts' small needs (design/ENGINE_API.md §7): counting a flag range,
// a forced omen, holding the day-and-night tint; and carried flames (§2).
#include "global.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "field_weather.h"
#include "ichor_calendar.h"
#include "ichor_herms.h"
#include "ichor_omen.h"
#include "ichor_relics.h"
#include "ichor_rites.h"
#include "ichor_save.h"
#include "rtc.h"
#include "pokemon.h"
#include "wild_encounter.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/ichor.h"
#include "constants/map_groups.h"
#include "constants/rtc.h"
#include "constants/weather.h"

u16 Ichor_CountFlagRange(void);
void Ichor_ForceOmen(void);
u16 Ichor_CheckOmen(void);
u16 Ichor_GetOmen(void);
void Ichor_HoldTimeOfDay(void);
void Ichor_ReleaseTimeOfDay(void);
u16 Ichor_GetHighestPartyLevel(void);
void Ichor_RestUntil(void);

TEST("Ichor: Ichor_CountFlagRange counts the set flags in a range")
{
    u32 i;
    for (i = 0; i < 8; i++)
        FlagClear(FLAG_ICHOR_PROPHECY_START + i);
    FlagSet(FLAG_ICHOR_PROPHECY_START + 0);
    FlagSet(FLAG_ICHOR_PROPHECY_START + 3);
    FlagSet(FLAG_ICHOR_PROPHECY_START + 7);
    FlagSet(FLAG_ICHOR_PROPHECY_START + 8);  // outside the range
    gSpecialVar_0x8004 = FLAG_ICHOR_PROPHECY_START;
    gSpecialVar_0x8005 = 8;
    EXPECT_EQ(Ichor_CountFlagRange(), 3);
    FlagClear(FLAG_ICHOR_PROPHECY_START + 8);
}

TEST("Ichor: a forced omen arrives the next day, then the day after draws its own")
{
    gIchorSave.omenKind = OMEN_NONE;
    gIchorSave.omenEntry = 0;
    gSpecialVar_0x8004 = OMEN_WEATHER;
    gSpecialVar_0x8005 = OMEN_WEATHER_LERNIP;
    Ichor_ForceOmen();
    EXPECT_EQ(Ichor_CheckOmen(), FALSE);  // not today

    Ichor_DoDailyEvents(1);
    gSpecialVar_0x8004 = OMEN_WEATHER;
    gSpecialVar_0x8005 = OMEN_WEATHER_LERNIP;
    EXPECT_EQ(Ichor_CheckOmen(), TRUE);
    gSpecialVar_0x8005 = OMEN_WEATHER_KRYOPUFF;
    EXPECT_EQ(Ichor_CheckOmen(), FALSE);
    EXPECT_EQ(Ichor_GetOmen(), OMEN_WEATHER);
    EXPECT_EQ(gSpecialVar_0x8004, OMEN_WEATHER_LERNIP);

    Ichor_DoDailyEvents(1);
    EXPECT_EQ(Ichor_GetOmen(), OMEN_GOOD_SIGN);  // drawn: no other kind has an open entry yet
}

TEST("Ichor: a held time of day overrides the clock until released")
{
    u32 time;
    for (time = 0; time < TIMES_OF_DAY_COUNT; time++)
    {
        gSpecialVar_0x8004 = time;
        Ichor_HoldTimeOfDay();
        EXPECT_EQ(GetTimeOfDay(), time);
    }
    Ichor_ReleaseTimeOfDay();
    EXPECT_EQ(gIchorSave.heldTimeOfDay, 0);
}

TEST("Ichor: a carried flame counts down even on a quiet step, and water puts it out")
{
    Ichor_SetCarriedFlame(FLAME_HEARTH, 10);
    EXPECT_EQ(Ichor_CarriedFlameStep(FALSE), FALSE);
    EXPECT_EQ(Ichor_GetFlameSteps(), 9);
    EXPECT_EQ(Ichor_GetFlameKind(), FLAME_HEARTH);

    gPlayerAvatar.flags |= PLAYER_AVATAR_FLAG_SURFING;
    EXPECT_EQ(Ichor_CarriedFlameStep(FALSE), FALSE);
    EXPECT_EQ(Ichor_GetFlameKind(), FLAME_NONE);
    EXPECT_EQ(Ichor_IsCarryingFlame(), FALSE);
    gPlayerAvatar.flags &= ~PLAYER_AVATAR_FLAG_SURFING;
}

TEST("Ichor: Aethos's herms and the Oikoumene's waystones keep separate flags")
{
    EXPECT_EQ(Ichor_GetHermFlag(HERM_KALLISTE_ROUTE_1), FLAG_ICHOR_HERMS_START);
    EXPECT_EQ(Ichor_GetHermFlag(HERM_THE_ASCENT), FLAG_ICHOR_HERMS_START + HERM_THE_ASCENT);
    EXPECT_EQ(Ichor_GetHermFlag(HERM_OIKOUMENE_FIRST), FLAG_ICHOR_WAYSTONES_START);
    EXPECT_EQ(Ichor_GetHermFlag(HERM_MAX - 1), FLAG_ICHOR_WAYSTONES_START + 31);
}

TEST("Ichor: rain burns a carried flame down two steps at a time, and it still gutters")
{
    u8 weather = gWeatherPtr->currWeather;
    gWeatherPtr->currWeather = WEATHER_RAIN;
    Ichor_SetCarriedFlame(FLAME_LERNA, 8);
    Ichor_CarriedFlameStep(FALSE);
    EXPECT_EQ(Ichor_GetFlameSteps(), 6);
    Ichor_CarriedFlameStep(FALSE);  // 6 -> 4: past 5, so it guttered (silently here)
    EXPECT_EQ(Ichor_GetFlameSteps(), 4);
    Ichor_SetCarriedFlame(FLAME_LERNA, 1);
    Ichor_CarriedFlameStep(FALSE);  // never below 0
    EXPECT_EQ(Ichor_GetFlameSteps(), 0);
    EXPECT_EQ(Ichor_GetFlameKind(), FLAME_NONE);
    gWeatherPtr->currWeather = weather;
}

TEST("Ichor: a carried flame doesn't drown aboard the Euploia")
{
    Ichor_SetCarriedFlame(FLAME_HESTIA_SHIP, 10);
    gPlayerAvatar.flags |= PLAYER_AVATAR_FLAG_SURFING;
    FlagSet(FLAG_ICHOR_GENERAL_START + 0x302);  // world-postgame's FLAG_ICHOR_ON_SHIP
    Ichor_CarriedFlameStep(FALSE);
    EXPECT_EQ(Ichor_GetFlameKind(), FLAME_HESTIA_SHIP);
    EXPECT_EQ(Ichor_GetFlameSteps(), 9);
    FlagClear(FLAG_ICHOR_GENERAL_START + 0x302);
    gPlayerAvatar.flags &= ~PLAYER_AVATAR_FLAG_SURFING;
}

TEST("Ichor: a map's own temp vars are never read as a carried flame")
{
    Ichor_SetCarriedFlame(FLAME_NONE, 0);
    VarSet(VAR_TEMP_2, 1);  // Thyrsa's ON_TRANSITION does this
    VarSet(VAR_TEMP_3, 1);
    EXPECT_EQ(Ichor_IsCarryingFlame(), FALSE);
    Ichor_CarriedFlameStep(FALSE);
    EXPECT_EQ(VarGet(VAR_TEMP_2), 1);
    VarSet(VAR_TEMP_2, 0);
    VarSet(VAR_TEMP_3, 0);
}

TEST("Ichor: hidden items decode vanilla flags and bank flags from the same field")
{
    EXPECT_EQ(Ichor_GetHiddenItemFlag(0), FLAG_HIDDEN_ITEMS_START);
    EXPECT_EQ(Ichor_GetHiddenItemFlag(FLAG_HIDDEN_ITEM_ICHOR_ELAIA_HONEY - FLAG_HIDDEN_ITEMS_START), FLAG_HIDDEN_ITEM_ICHOR_ELAIA_HONEY);
    EXPECT_EQ(Ichor_GetHiddenItemFlag(ICHOR_HIDDEN_ITEM_BANK_ID), ICHOR_FLAGS_START);
    EXPECT_EQ(Ichor_GetHiddenItemFlag(ICHOR_HIDDEN_ITEM_BANK_ID + (FLAG_ICHOR_GENERAL_START - ICHOR_FLAGS_START)), FLAG_ICHOR_GENERAL_START);
    EXPECT_EQ(Ichor_GetHiddenItemFlag(ICHOR_HIDDEN_ITEM_BANK_ID + (ICHOR_FLAGS2_END - ICHOR_FLAGS_START)), ICHOR_FLAGS2_END);
    EXPECT_LT(ICHOR_HIDDEN_ITEM_BANK_ID + (ICHOR_FLAGS2_END - ICHOR_FLAGS_START), 1 << 13);  // fits the 13-bit field
}

TEST("Ichor: Ichor_GetHighestPartyLevel reads the strongest Pokémon, not an Egg")
{
    ZeroPlayerPartyMons();
    RUN_OVERWORLD_SCRIPT(
        givemon SPECIES_WOBBUFFET, 12;
        givemon SPECIES_WOBBUFFET, 31;
        givemon SPECIES_WOBBUFFET, 25;
    );
    EXPECT_EQ(Ichor_GetHighestPartyLevel(), 31);
    ZeroPlayerPartyMons();
}

static u32 LocalMinutes(void)
{
    RtcCalcLocalTime();
    return gLocalTime.hours * 60 + gLocalTime.minutes;
}

TEST("Ichor: a xenia rest moves the clock forward to the hour chosen, never back")
{
    RtcCalcLocalTimeOffset(3, 8, 0, 0);    // day 3, 08:00
    gSpecialVar_0x8004 = ICHOR_REST_DUSK;
    Ichor_RestUntil();
    EXPECT_EQ(LocalMinutes() / 60, 19);
    EXPECT_EQ(gLocalTime.days, 3);
    gSpecialVar_0x8004 = ICHOR_REST_NOON;  // behind: nothing happens
    Ichor_RestUntil();
    EXPECT_EQ(LocalMinutes() / 60, 19);
    gSpecialVar_0x8004 = ICHOR_REST_NIGHT;
    Ichor_RestUntil();
    EXPECT_GE(LocalMinutes(), 20 * 60 + 30);
    EXPECT_LT(LocalMinutes(), 20 * 60 + 32);
    gSpecialVar_0x8004 = ICHOR_REST_DAWN;  // never past midnight
    Ichor_RestUntil();
    EXPECT_GE(LocalMinutes(), 20 * 60 + 30);
    EXPECT_EQ(gLocalTime.days, 3);
}

TEST("Ichor: the daily omen is drawn only from entries the story has opened")
{
    u32 seed, kinds[OMEN_STRANGER + 1] = {0};
    FlagClear(FLAG_BADGE07_GET);
    FlagClear(FLAG_BADGE08_GET);
    for (seed = 0; seed < 300; seed++)
    {
        Ichor_DrawOmen(seed * 2654435761u);
        kinds[gIchorSave.omenKind]++;
    }
    EXPECT_EQ(kinds[OMEN_GOOD_SIGN], 300);  // nothing else is open yet

    FlagSet(FLAG_BADGE07_GET);  // the two weather rows open
    memset(kinds, 0, sizeof(kinds));
    for (seed = 0; seed < 600; seed++)
    {
        Ichor_DrawOmen(seed * 2654435761u);
        kinds[gIchorSave.omenKind]++;
        if (gIchorSave.omenKind == OMEN_WEATHER)
            EXPECT(gIchorSave.omenEntry == OMEN_WEATHER_KRYOPUFF || gIchorSave.omenEntry == OMEN_WEATHER_LERNIP);
        if (gIchorSave.omenKind == OMEN_GOOD_SIGN)
            EXPECT_LE(gIchorSave.omenEntry, OMEN_SIGN_LUCKY(6));
    }
    EXPECT_EQ(kinds[OMEN_SWARM] + kinds[OMEN_VISITOR] + kinds[OMEN_STRANGER], 0);
    EXPECT_GT(kinds[OMEN_WEATHER], 600 * 55 / 100);  // 20 against the good sign's 10
    EXPECT_LT(kinds[OMEN_WEATHER], 600 * 78 / 100);

    FlagSet(FLAG_BADGE08_GET);  // the test rows: a swarm and two visitors
    memset(kinds, 0, sizeof(kinds));
    for (seed = 0; seed < 1000; seed++)
    {
        Ichor_DrawOmen(seed * 2654435761u);
        kinds[gIchorSave.omenKind]++;
    }
    EXPECT_GT(kinds[OMEN_SWARM], 1000 * 37 / 100);  // 45 of 100 before strangers walk
    EXPECT_LT(kinds[OMEN_SWARM], 1000 * 53 / 100);
    EXPECT_GT(kinds[OMEN_VISITOR], 1000 * 18 / 100);
    EXPECT_EQ(kinds[OMEN_STRANGER], 0);
    FlagClear(FLAG_BADGE07_GET);
    FlagClear(FLAG_BADGE08_GET);
}

TEST("Ichor: an omen's swarm starts today's outbreak, and only today's visitor shows")
{
    FlagSet(FLAG_BADGE08_GET);
    gIchorSave.forcedOmenKind = OMEN_SWARM;
    gIchorSave.forcedOmenEntry = 0;
    Ichor_DoDailyEvents(1);
    EXPECT_EQ(gSaveBlock1Ptr->outbreakPokemonSpecies, SPECIES_WOBBUFFET);
    EXPECT_EQ(gSaveBlock1Ptr->outbreakPokemonLevel, 7);
    EXPECT_EQ(gSaveBlock1Ptr->outbreakLocationMapNum, MAP_NUM(MAP_KALLISTE_ROUTE1));
    EXPECT_EQ(gSaveBlock1Ptr->outbreakDaysLeft, 1);
    EXPECT(FlagGet(FLAG_TEMP_1) && FlagGet(FLAG_TEMP_2));  // no visitor today

    gIchorSave.forcedOmenKind = OMEN_VISITOR;
    gIchorSave.forcedOmenEntry = 1;
    Ichor_DoDailyEvents(1);
    EXPECT(FlagGet(FLAG_TEMP_1));
    EXPECT(!FlagGet(FLAG_TEMP_2));
    FlagClear(FLAG_BADGE08_GET);
}

u16 Ichor_GetMonth(void);
u16 Ichor_GetFestival(void);
u16 Ichor_DaysToFestival(void);
u16 Ichor_JoinFestival(void);

TEST("Ichor: the Aethos year is 36 days, a festival on each month's middle day")
{
    EXPECT_EQ(Ichor_GetMonthOfDay(0), ICHOR_MONTH_HEKATOMBAION);
    EXPECT_EQ(Ichor_GetMonthOfDay(3), ICHOR_MONTH_METAGEITNION);
    EXPECT_EQ(Ichor_GetMonthOfDay(35), ICHOR_MONTH_SKIROPHORION);
    EXPECT_EQ(Ichor_GetMonthOfDay(36), ICHOR_MONTH_HEKATOMBAION);
    EXPECT_EQ(Ichor_GetFestivalOfDay(0), ICHOR_FESTIVAL_NONE);
    EXPECT_EQ(Ichor_GetFestivalOfDay(1), ICHOR_FESTIVAL_PANATHENAIA);
    EXPECT_EQ(Ichor_GetFestivalOfDay(2), ICHOR_FESTIVAL_NONE);
    EXPECT_EQ(Ichor_GetFestivalOfDay(13), ICHOR_FESTIVAL_NONE);  // Maimakterion, the month of storms
    EXPECT_EQ(Ichor_GetFestivalOfDay(22), ICHOR_FESTIVAL_ANTHESTERIA);
    EXPECT_EQ(Ichor_GetFestivalOfDay(34 + 36 * 5), ICHOR_FESTIVAL_KRONIA);

    VarSet(VAR_DAYS, 37);  // the Panathenaia, a year on
    EXPECT_EQ(Ichor_GetMonth(), ICHOR_MONTH_HEKATOMBAION);
    EXPECT_EQ(gSpecialVar_0x8004, 1);
    EXPECT_EQ(Ichor_GetFestival(), ICHOR_FESTIVAL_PANATHENAIA);
    gSpecialVar_0x8004 = ICHOR_FESTIVAL_PANATHENAIA;
    EXPECT_EQ(Ichor_DaysToFestival(), 0);
    gSpecialVar_0x8004 = ICHOR_FESTIVAL_KARNEIA;
    EXPECT_EQ(Ichor_DaysToFestival(), 3);
    VarSet(VAR_DAYS, 38);
    gSpecialVar_0x8004 = ICHOR_FESTIVAL_PANATHENAIA;
    EXPECT_EQ(Ichor_DaysToFestival(), 35);
}

TEST("Ichor: joining a festival gives its god +5 Favor once a day")
{
    u32 athena = Ichor_GetFavor(ICHOR_GOD_ATHENA);
    FlagClear(FLAG_DAILY_ICHOR_FESTIVAL_JOINED);
    VarSet(VAR_DAYS, 2);       // no festival
    EXPECT_EQ(Ichor_JoinFestival(), FALSE);
    VarSet(VAR_DAYS, 1);       // the Panathenaia
    EXPECT_EQ(Ichor_JoinFestival(), TRUE);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_ATHENA), athena + 5);
    EXPECT_EQ(Ichor_JoinFestival(), FALSE);
    EXPECT_EQ(Ichor_GetFavor(ICHOR_GOD_ATHENA), athena + 5);
    FlagClear(FLAG_DAILY_ICHOR_FESTIVAL_JOINED);
    VarSet(VAR_DAYS, 34);      // the Kronia: no god's Favor
    EXPECT_EQ(Ichor_JoinFestival(), FALSE);
    FlagClear(FLAG_DAILY_ICHOR_FESTIVAL_JOINED);
}

static u32 ChooseGhost(void) { return 1; }

TEST("Ichor: on the Anthesteria's night a land encounter draws again for a Ghost-type")
{
    static const struct WildPokemon slots[] = {
        {5, 5, SPECIES_WOBBUFFET},
        {5, 5, SPECIES_GASTLY},
    };
    VarSet(VAR_DAYS, 22);              // the Anthesteria
    gSpecialVar_0x8004 = TIME_NIGHT;
    Ichor_HoldTimeOfDay();
    EXPECT_EQ(Ichor_FestivalWildSlot(slots, 0, ChooseGhost), 1);
    gSpecialVar_0x8004 = TIME_DAY;     // by day, nothing changes
    Ichor_HoldTimeOfDay();
    EXPECT_EQ(Ichor_FestivalWildSlot(slots, 0, ChooseGhost), 0);
    VarSet(VAR_DAYS, 23);              // the day after, at night
    gSpecialVar_0x8004 = TIME_NIGHT;
    Ichor_HoldTimeOfDay();
    EXPECT_EQ(Ichor_FestivalWildSlot(slots, 0, ChooseGhost), 0);
    Ichor_ReleaseTimeOfDay();
}
