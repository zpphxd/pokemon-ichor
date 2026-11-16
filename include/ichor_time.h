#ifndef GUARD_ICHOR_TIME_H
#define GUARD_ICHOR_TIME_H

// Ichor: a script can hold the day-and-night tint at one time of day, whatever
// the clock says, across warps and saves (design/ENGINE_API.md §7). The
// options menu's DAY/NIGHT TINT OFF draws daytime colors at every hour.

void Ichor_ApplyHeldTime(s32 *hours, s32 *minutes);  // overworld.c, UpdateTimeOfDay
bool32 Ichor_IsTintOff(void);                         // the DAY/NIGHT TINT option is OFF, and no tint is held
u16 Ichor_GetTimeOfDay(void);

#endif // GUARD_ICHOR_TIME_H
