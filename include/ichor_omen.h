#ifndef GUARD_ICHOR_OMEN_H
#define GUARD_ICHOR_OMEN_H

// Ichor: omens (design/SYSTEMS.md §6). The day's omen lives in IchorSave
// (omenKind, omenEntry); a script can force tomorrow's. The daily draw from
// the entry table is not built yet. design/ENGINE_API.md §7 lists the calls.

void Ichor_OmenNewDay(void);  // ichor_save.c, Ichor_DoDailyEvents

#endif // GUARD_ICHOR_OMEN_H
