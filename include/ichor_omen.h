#ifndef GUARD_ICHOR_OMEN_H
#define GUARD_ICHOR_OMEN_H

// Ichor: omens (design/SYSTEMS.md §6). The day's omen lives in IchorSave
// (omenKind, omenEntry), drawn each new day from the entries in
// src/data/ichor_omens.h that story progress allows; a script can force
// tomorrow's. design/ENGINE_API.md §7 lists the calls.

// One row of src/data/ichor_omens.h
struct IchorOmenEntry
{
    u8 kind;          // OMEN_SWARM, OMEN_VISITOR, OMEN_WEATHER or OMEN_STRANGER
    u8 entry;         // its number within the kind (OMEN_WEATHER_LERNIP, ...)
    u16 unlockFlag;   // drawn only once this flag is set (0: from the start)
    u16 lockFlag;     // and never once this one is set (0: no end), e.g. a visitor met for good
    u16 hideFlag;     // a visitor's object: shown only on its day
    u16 species;      // a swarm's species, half the encounters on its map
    u16 map;          // a swarm's map (MAP_*)
    u8 level;         // a swarm's level
};

void Ichor_OmenNewDay(void);  // ichor_save.c, Ichor_DoDailyEvents
void Ichor_DrawOmen(u32 seed); // the draw itself, for the C tests
void Ichor_OmenFieldFrame(void);
void Ichor_SetOmenWeather(void);

#endif // GUARD_ICHOR_OMEN_H
