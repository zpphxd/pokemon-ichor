// Ichor: the Nursery of Nysa's yard on Route 7 (tools/ichor/maps/kopais.py).
//
// The nursery is the expansion's day care (src/daycare.c, Hera's blessing
// hooks included); this only shows its two Pokémon roaming the yard, as in
// Emerald's Route 117. Route 7's ON_TRANSITION calls Ichor_SetNurseryYardMons:
// it puts each deposited Pokémon's overworld sprite (shiny and female forms
// kept) in VAR_OBJ_GFX_ID_0 and _1, which the yard's two objects use, and
// sets VAR_0x8004 and _5 to whether each slot holds a Pokémon, so the script
// hides an empty slot's object.
#include "global.h"
#include "daycare.h"
#include "event_data.h"
#include "pokemon.h"
#include "constants/event_objects.h"
#include "constants/vars.h"

void Ichor_SetNurseryYardMons(void)
{
    u32 i;

    for (i = 0; i < DAYCARE_MON_COUNT; i++)
    {
        struct BoxPokemon *mon = &gSaveBlock1Ptr->daycare.mons[i].mon;
        u16 gfx = OBJ_EVENT_GFX_SPECIES(NONE);

        if (GetBoxMonData(mon, MON_DATA_SANITY_HAS_SPECIES))
        {
            gfx = GetBoxMonData(mon, MON_DATA_SPECIES) + OBJ_EVENT_MON;
            if (GetBoxMonData(mon, MON_DATA_IS_SHINY))
                gfx += OBJ_EVENT_MON_SHINY;
            if (GetBoxMonGender(mon) == MON_FEMALE)
                gfx += OBJ_EVENT_MON_FEMALE;
        }
        VarSet(VAR_OBJ_GFX_ID_0 + i, gfx);
        VarSet(VAR_0x8004 + i, GetBoxMonData(mon, MON_DATA_SANITY_HAS_SPECIES) ? TRUE : FALSE);
    }
}
