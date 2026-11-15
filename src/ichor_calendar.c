// Ichor: the festival calendar (design/SYSTEMS.md §7, design/ENGINE_API.md §7).
//
// Aethos keeps the old Attic year, 36 real days long: 12 months of 3 days on
// the day counter (VAR_DAYS, which the clock keeps), each month's festival on
// its middle day. Towns dress for a festival in their own ON_TRANSITION; the
// engine answers what day it is, gives the god's Favor for joining, and runs
// the Anthesteria's night of Ghost-types.

#include "global.h"
#include "event_data.h"
#include "rtc.h"
#include "ichor_calendar.h"
#include "ichor_rites.h"
#include "pokemon.h"
#include "wild_encounter.h"
#include "constants/flags.h"
#include "constants/ichor.h"
#include "constants/pokemon.h"
#include "constants/rtc.h"
#include "constants/vars.h"

#define FESTIVAL_DAY   1    // the middle day of a month
#define JOIN_FAVOR     5
#define GHOST_DRAWS    2    // the Anthesteria: up to two more draws for a Ghost-type, so about three times as many

// The god whose Favor a festival gives; ICHOR_GOD_NONE gives none
static const u8 sFestivalGods[ICHOR_MONTH_COUNT + 1] =
{
    [ICHOR_FESTIVAL_PANATHENAIA] = ICHOR_GOD_ATHENA,
    [ICHOR_FESTIVAL_KARNEIA]     = ICHOR_GOD_APOLLO,
    [ICHOR_FESTIVAL_MYSTERIES]   = ICHOR_GOD_DEMETER,
    [ICHOR_FESTIVAL_PYANOPSIA]   = ICHOR_GOD_APOLLO,
    [ICHOR_FESTIVAL_POSEIDEA]    = ICHOR_GOD_POSEIDON,
    [ICHOR_FESTIVAL_THEOGAMIA]   = ICHOR_GOD_HERA,
    [ICHOR_FESTIVAL_ANTHESTERIA] = ICHOR_GOD_DIONYSUS,
    [ICHOR_FESTIVAL_DIONYSIA]    = ICHOR_GOD_DIONYSUS,
    [ICHOR_FESTIVAL_MOUNICHIA]   = ICHOR_GOD_ARTEMIS,
    [ICHOR_FESTIVAL_THARGELIA]   = ICHOR_GOD_APOLLO,
    [ICHOR_FESTIVAL_KRONIA]      = ICHOR_GOD_NONE,  // Kronos isn't a god you pray to
};

static u32 Today(void)
{
    return VarGet(VAR_DAYS);
}

u32 Ichor_GetMonthOfDay(u32 day)
{
    return (day / ICHOR_DAYS_PER_MONTH) % ICHOR_MONTH_COUNT;
}

u32 Ichor_GetFestivalOfDay(u32 day)
{
    u32 month = Ichor_GetMonthOfDay(day);
    if (day % ICHOR_DAYS_PER_MONTH != FESTIVAL_DAY || month == ICHOR_MONTH_MAIMAKTERION)
        return ICHOR_FESTIVAL_NONE;
    return month + 1;
}

u32 Ichor_GetTodaysFestival(void)
{
    return Ichor_GetFestivalOfDay(Today());
}

// specialvar Ichor_GetMonth: this month (ICHOR_MONTH_*), with the day of the
// month (0-2) in VAR_0x8004.
u16 Ichor_GetMonth(void)
{
    gSpecialVar_0x8004 = Today() % ICHOR_DAYS_PER_MONTH;
    return Ichor_GetMonthOfDay(Today());
}

// specialvar Ichor_GetFestival: today's festival (ICHOR_FESTIVAL_*), or
// ICHOR_FESTIVAL_NONE.
u16 Ichor_GetFestival(void)
{
    return Ichor_GetTodaysFestival();
}

// specialvar Ichor_DaysToFestival: days until festival VAR_0x8004 next comes,
// 0 if it is today ("The Panathenaia is in 4 days.").
u16 Ichor_DaysToFestival(void)
{
    u32 days;
    for (days = 0; days < ICHOR_MONTH_COUNT * ICHOR_DAYS_PER_MONTH; days++)
    {
        if (Ichor_GetFestivalOfDay(Today() + days) == gSpecialVar_0x8004)
            return days;
    }
    return 0xFFFF;  // not a festival
}

// specialvar Ichor_JoinFestival: the player joins today's festival. The first
// time today, its god gives +5 Favor: TRUE. FALSE if there's no festival, it
// has no god, or the player already joined today.
u16 Ichor_JoinFestival(void)
{
    u32 festival = Ichor_GetTodaysFestival();
    if (festival == ICHOR_FESTIVAL_NONE || FlagGet(FLAG_DAILY_ICHOR_FESTIVAL_JOINED))
        return FALSE;
    FlagSet(FLAG_DAILY_ICHOR_FESTIVAL_JOINED);
    if (sFestivalGods[festival] == ICHOR_GOD_NONE)
        return FALSE;
    Ichor_AddFavorTo(sFestivalGods[festival], JOIN_FAVOR);
    return TRUE;
}

static bool32 IsGhost(u32 species)
{
    return gSpeciesInfo[species].types[0] == TYPE_GHOST || gSpeciesInfo[species].types[1] == TYPE_GHOST;
}

// The Anthesteria: the jars are opened and the dead walk. At night, a land
// encounter that isn't a Ghost-type draws again, up to twice, keeping a Ghost.
u32 Ichor_FestivalWildSlot(const struct WildPokemon *wildPokemon, u32 index, u32 (*choose)(void))
{
    u32 i, other;
    if (Ichor_GetTodaysFestival() != ICHOR_FESTIVAL_ANTHESTERIA || GetTimeOfDay() != TIME_NIGHT)
        return index;
    for (i = 0; i < GHOST_DRAWS && !IsGhost(wildPokemon[index].species); i++)
    {
        other = choose();
        if (IsGhost(wildPokemon[other].species))
            index = other;
    }
    return index;
}
