#ifndef GUARD_REGIONS_H
#define GUARD_REGIONS_H

#include "global.h"
#include "constants/regions.h"

enum KantoSubRegion GetKantoSubregion(u32 mapSecId);

// Ichor: the Oikoumene's sections are the Hoenn block (ids 0-85, less the
// Battle Frontier the kept Pyramid and Pike maps still use) and the Kanto
// block's spare tail (constants/region_map_sections_oikoumene.h). One range
// check each, unsigned, so the first range's 0 needs no compare.
static inline bool32 IsOikoumeneMapSec(u32 sectionId)
{
    if (IS_FRLG)
        return FALSE;
    if (sectionId - MAPSEC_OIKOUMENE_FIRST <= MAPSEC_OIKOUMENE_LAST - MAPSEC_OIKOUMENE_FIRST)
        return sectionId != MAPSEC_BATTLE_FRONTIER;
    return sectionId - MAPSEC_OIKOUMENE2_FIRST <= MAPSEC_OIKOUMENE2_LAST - MAPSEC_OIKOUMENE2_FIRST;
}

static inline enum Region GetRegionForSectionId(u32 sectionId)
{
    // Ichor: the Oikoumene reads as Kanto's chart slot (REGION_OIKOUMENE).
    if (IsOikoumeneMapSec(sectionId))
        return REGION_OIKOUMENE;
    // Ichor: outside an FRLG build the Kanto block's IDs hold Aethos's routes and
    // islands (design/AETHOS_MAP.md), so only an FRLG build reads them as Kanto.
    if (IS_FRLG && sectionId >= KANTO_MAPSEC_START && sectionId < MAPSEC_SPECIAL_AREA)
        return REGION_KANTO;
    return REGION_HOENN;
}

static inline enum Region GetCurrentRegion(void)
{
    return GetRegionForSectionId(gMapHeader.regionMapSectionId);
}

// Ichor: the Oikoumene chart's saved state (src/regions.c): the last port you
// were in and the towns you've been to, kept up on every map load.
void Ichor_TrackOikoumene(void);
bool32 Ichor_IsOikoumeneTown(u32 mapSecId);
bool32 Ichor_IsOikoumeneTownVisited(u32 mapSecId);
u32 Ichor_GetOikoumenePortHealLocation(void);

#endif // GUARD_REGIONS_H
