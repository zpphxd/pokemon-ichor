// Ichor: omens (design/SYSTEMS.md §6; design/ENGINE_API.md §7).
//
// Today's omen is IchorSave.omenKind (an OMEN_* kind) and omenEntry (an entry
// within that kind, e.g. OMEN_WEATHER_LERNIP). A script can force tomorrow's
// omen, as when Akanthis first tells the Lernip rumor. The daily draw from
// SYSTEMS §6's entry table comes with the augurs; until then a day with no
// forced omen has none.
#include "global.h"
#include "event_data.h"
#include "ichor_omen.h"
#include "constants/ichor.h"

void Ichor_OmenNewDay(void)
{
    if (gIchorSave.forcedOmenKind != OMEN_NONE)
    {
        gIchorSave.omenKind = gIchorSave.forcedOmenKind;
        gIchorSave.omenEntry = gIchorSave.forcedOmenEntry;
        gIchorSave.forcedOmenKind = OMEN_NONE;
        gIchorSave.forcedOmenEntry = 0;
        return;
    }
    // Ichor: SYSTEMS §6's daily draw goes here (src/ichor_omen.c), from dailySeed ^ ICHOR_OMEN_SALT.
    gIchorSave.omenKind = OMEN_NONE;
    gIchorSave.omenEntry = 0;
}

// special Ichor_ForceOmen: tomorrow's omen is kind VAR_0x8004, entry VAR_0x8005.
void Ichor_ForceOmen(void)
{
    gIchorSave.forcedOmenKind = gSpecialVar_0x8004;
    gIchorSave.forcedOmenEntry = gSpecialVar_0x8005;
}

// specialvar Ichor_CheckOmen: TRUE if today's omen is kind VAR_0x8004, entry
// VAR_0x8005. A map's ON_TRANSITION uses it to set the omen's weather.
u16 Ichor_CheckOmen(void)
{
    return gIchorSave.omenKind != OMEN_NONE
        && gIchorSave.omenKind == gSpecialVar_0x8004
        && gIchorSave.omenEntry == gSpecialVar_0x8005;
}

// specialvar Ichor_GetOmen: today's omen kind (OMEN_NONE if none); its entry in VAR_0x8004.
u16 Ichor_GetOmen(void)
{
    gSpecialVar_0x8004 = gIchorSave.omenEntry;
    return gIchorSave.omenKind;
}
