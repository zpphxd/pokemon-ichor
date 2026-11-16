#ifndef GUARD_ICHOR_CALENDAR_H
#define GUARD_ICHOR_CALENDAR_H

// Ichor: the festival calendar (design/SYSTEMS.md §7). A 36-day Aethos year on
// the day counter; design/ENGINE_API.md §7 lists the calls.

struct WildPokemon;

u32 Ichor_GetMonthOfDay(u32 day);
u32 Ichor_GetFestivalOfDay(u32 day);
u32 Ichor_GetTodaysFestival(void);
u16 Ichor_DaysToFestival(void);
u32 Ichor_FestivalWildSlot(const struct WildPokemon *wildPokemon, u32 index, u32 (*choose)(void)); // ichor_rites.c

#endif // GUARD_ICHOR_CALENDAR_H
