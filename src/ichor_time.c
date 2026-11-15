// Ichor: holding the day-and-night tint (design/ENGINE_API.md §7). A held time
// of day replaces the clock's hour for the tint, and for everything else that
// asks the time of day (encounter tables, evolutions), until it is released.
// Delphoi stays at evening, then night, from Phase 4's III-7 to III-8.
// Also the xenia rest (SYSTEMS §10), which moves the clock itself forward.
#include "global.h"
#include "event_data.h"
#include "ichor_time.h"
#include "list_menu.h"
#include "malloc.h"
#include "overworld.h"
#include "rtc.h"
#include "script_menu.h"
#include "string_util.h"
#include "constants/ichor.h"
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

// The options menu's DAY/NIGHT TINT OFF: the overworld draws in daytime colors
// at every hour (overworld.c), unless a script holds a time of day.
bool32 Ichor_IsTintOff(void)
{
    return (gIchorSave.options & ICHOR_OPTION_TINT_OFF) && gIchorSave.heldTimeOfDay == 0;
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

// --- The xenia rest (SYSTEMS §10) --------------------------------------------------
// A host's bed moves the clock forward to dawn, noon, dusk or night, and never
// past midnight: each choice is offered only while that hour is still ahead.

static const u8 sRestHour[ICHOR_REST_COUNT][2] =
{
    [ICHOR_REST_DAWN]  = { 6, 0 },
    [ICHOR_REST_NOON]  = { 12, 0 },
    [ICHOR_REST_DUSK]  = { 19, 0 },
    [ICHOR_REST_NIGHT] = { 20, 30 },
};

static const u8 *const sRestNames[ICHOR_REST_COUNT] =
{
    [ICHOR_REST_DAWN]  = COMPOUND_STRING("DAWN"),
    [ICHOR_REST_NOON]  = COMPOUND_STRING("NOON"),
    [ICHOR_REST_DUSK]  = COMPOUND_STRING("DUSK"),
    [ICHOR_REST_NIGHT] = COMPOUND_STRING("NIGHT"),
};

static bool32 IsRestAhead(u32 rest)
{
    return sRestHour[rest][0] * 60 + sRestHour[rest][1] > gLocalTime.hours * 60 + gLocalTime.minutes;
}

static void PushRestChoice(const u8 *text, u16 id)
{
    struct ListMenuItem item;
    u8 *name = Alloc(16);  // freed by the menu
    StringCopy(name, text);
    item.name = name;
    item.id = id;
    MultichoiceDynamic_PushElement(item);
}

// specialvar Ichor_BuildRestMenu: pushes the hours still ahead today, then
// NOT NOW, for dynmultistack. Answers how many hours it offered; with none
// it pushes nothing.
u16 Ichor_BuildRestMenu(void)
{
    u32 rest, count = 0;

    RtcCalcLocalTime();
    for (rest = 0; rest < ICHOR_REST_COUNT; rest++)
    {
        if (!IsRestAhead(rest))
            continue;
        PushRestChoice(sRestNames[rest], rest);
        count++;
    }
    if (count != 0)
        PushRestChoice(COMPOUND_STRING("NOT NOW"), ICHOR_REST_COUNT);
    return count;
}

// special Ichor_RestUntil: the clock moves forward to the ICHOR_REST_* hour in
// VAR_0x8004, if it is still ahead today; otherwise it stays.
void Ichor_RestUntil(void)
{
    u32 rest = gSpecialVar_0x8004;

    RtcCalcLocalTime();
    if (rest >= ICHOR_REST_COUNT || !IsRestAhead(rest))
        return;
    RtcCalcLocalTimeOffset(gLocalTime.days, sRestHour[rest][0], sRestHour[rest][1], 0);
    RetintNow();
}
