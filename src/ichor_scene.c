// Ichor: small helpers for story scenes (design/phase2/SCRIPT.md).
// Scene support only; the Ichor systems (relics, rites, herms, save state)
// belong to the engine session and live in their own files.
#include "global.h"
#include "event_data.h"
#include "overworld.h"

// Force the day-night tint to an hour, for a scene that must play at night
// whatever the clock says (beat 10's night leg). VAR_0x8004 is the hour,
// 1-23; 0 hands the tint back to the real clock. The engine stores 0 as "no
// override", so midnight itself can't be forced: use 23 or 1.
void Ichor_SetHoursOverride(void)
{
    SetTimeOfDay(gSpecialVar_0x8004 % 24);
}
