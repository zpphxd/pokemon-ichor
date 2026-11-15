#ifndef GUARD_ICHOR_TIME_H
#define GUARD_ICHOR_TIME_H

// Ichor: a script can hold the day-and-night tint at one time of day, whatever
// the clock says, across warps and saves (design/ENGINE_API.md §7).

void Ichor_ApplyHeldTime(s32 *hours, s32 *minutes);  // overworld.c, UpdateTimeOfDay

#endif // GUARD_ICHOR_TIME_H
