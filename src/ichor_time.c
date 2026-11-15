// Ichor: holding the day-and-night tint (design/ENGINE_API.md §7). A held time
// of day replaces the clock's hour for the tint, and for everything else that
// asks the time of day (encounter tables, evolutions), until it is released.
// Delphoi stays at evening, then night, from Phase 4's III-7 to III-8.
#include "global.h"
#include "event_data.h"
#include "ichor_time.h"
#include "overworld.h"
#include "rtc.h"
#include "constants/rtc.h"

// A moment inside each time of day where its tint is at full strength.
static const u8 sHeldHour[TIMES_OF_DAY_COUNT][2] =
{
    [TIME_MORNING] = { MORNING_HOUR_BEGIN + (MORNING_HOUR_END - MORNING_HOUR_BEGIN) / 2, 0 },
    [TIME_DAY]     = { DAY_HOUR_BEGIN + 2, 0 },
    [TIME_EVENING] = { EVENING_HOUR_END - 1, 59 },
    [TIME_NIGHT]   = { NIGHT_HOUR_BEGIN + 1, 0 },
};

void Ichor_ApplyHeldTime(s32 *hours, s32 *minutes)
{
    u32 held = gIchorSave.heldTimeOfDay;
    if (held == 0 || held > TIMES_OF_DAY_COUNT)
        return;
    *hours = sHeldHour[held - 1][0] % HOURS_PER_DAY;
    *minutes = sHeldHour[held - 1][1];
}

static void RetintNow(void)
{
    gTimeUpdateCounter = 0;  // OverworldBasic re-reads the time and re-tints next frame
}

// special Ichor_HoldTimeOfDay: the tint holds at TIME_* VAR_0x8004 until released.
void Ichor_HoldTimeOfDay(void)
{
    if (gSpecialVar_0x8004 >= TIMES_OF_DAY_COUNT)
        return;
    gIchorSave.heldTimeOfDay = gSpecialVar_0x8004 + 1;
    RetintNow();
}

// special Ichor_ReleaseTimeOfDay: the clock's own time of day returns.
void Ichor_ReleaseTimeOfDay(void)
{
    gIchorSave.heldTimeOfDay = 0;
    RetintNow();
}
