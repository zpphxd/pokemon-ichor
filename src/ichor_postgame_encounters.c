// Ichor postgame: wild encounter overlays (design/postgame/ENGINE.md §6).
//
// wild_encounter.c's TryGenerateWildMon asks Ichor_OverlayWildSpecies for the
// species once a wild table has picked its slot and level. Each row below may
// replace it, one encounter in `oneIn`, when its conditions hold; the level is
// always the table's. No map's wild_encounters.json entry changes.
//
// To add an overlay (batch 8's Time Fractures), append a row. The first row
// whose conditions hold and whose roll succeeds wins.
#include "global.h"
#include "event_data.h"
#include "ichor_postgame_encounters.h"
#include "overworld.h"
#include "random.h"
#include "rtc.h"
#include "constants/map_types.h"
#include "constants/rtc.h"
#include "constants/species.h"

#define ANY_TIME  0xFF

// Map types an overlay may appear on, as a mask of (1 << MAP_TYPE_*).
#define ON_ROADS  ((1 << MAP_TYPE_ROUTE) | (1 << MAP_TYPE_OCEAN_ROUTE))

struct IchorEncounterOverlay
{
    u16 species;
    u8 oneIn;               // one encounter in this many
    u8 area;                // WILD_AREA_*
    u16 flag;               // only while this flag is set (0: always)
    u8 timeOfDay;           // TIME_* or ANY_TIME
    u8 notInDarkMaps:1;     // not on a map that needs a light (a cave)
    u8 padding:7;
    u16 mapTypes;           // a mask of (1 << MAP_TYPE_*)
    bool32 (*condition)(void); // any other rule (a Fracture's maps), or NULL
};

static const struct IchorEncounterOverlay sOverlays[] =
{
    // POSTGAME §1, shades on the roads: once the post-game is live, one land
    // encounter in eight at night is a gray Obolorn, outside caves and towns.
    {
        .species = SPECIES_OBOLORN,     // ICHOR_STUB_AETHOS_DEX until the dex lands
        .oneIn = 8,
        .area = WILD_AREA_LAND,
        .flag = FLAG_ICHOR_POSTGAME,
        .timeOfDay = TIME_NIGHT,
        .notInDarkMaps = TRUE,
        .mapTypes = ON_ROADS,
    },
};

static bool32 OverlayApplies(const struct IchorEncounterOverlay *overlay, enum WildPokemonArea area)
{
    if (overlay->area != area)
        return FALSE;
    if (overlay->flag != 0 && !FlagGet(overlay->flag))
        return FALSE;
    if (!(overlay->mapTypes & (1 << gMapHeader.mapType)))
        return FALSE;
    if (overlay->notInDarkMaps && gMapHeader.cave)
        return FALSE;
    if (overlay->timeOfDay != ANY_TIME && GetTimeOfDay() != overlay->timeOfDay)
        return FALSE;
    if (overlay->condition != NULL && !overlay->condition())
        return FALSE;
    return TRUE;
}

u16 Ichor_OverlayWildSpecies(u16 species, enum WildPokemonArea area)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sOverlays); i++)
    {
        const struct IchorEncounterOverlay *overlay = &sOverlays[i];
        if (OverlayApplies(overlay, area) && Random() % overlay->oneIn == 0)
            return overlay->species;
    }
    return species;
}
