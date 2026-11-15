#ifndef GUARD_CONSTANTS_REGIONS_H
#define GUARD_CONSTANTS_REGIONS_H

// Core-series regions
enum Region
{
    REGION_NONE,
    REGION_KANTO,
    REGION_JOHTO,
    REGION_HOENN,
    REGION_SINNOH,
    REGION_UNOVA,
    REGION_KALOS,
    REGION_ALOLA,
    REGION_GALAR,
    REGION_HISUI,
    REGION_PALDEA,
    REGIONS_COUNT,
};

// Ichor: the Oikoumene, the post-game's second chart, takes Kanto's chart slot
// (gRegionMapInfos[REGION_MAP_KANTO], the Kanto grid, Kanto's fly targets).
// Only an FRLG build has a Kanto of its own (design/oikoumene/BUILD.md §3).
#define REGION_OIKOUMENE REGION_KANTO

enum KantoSubRegion
{
    KANTO_SUBREGION_KANTO,
    KANTO_SUBREGION_SEVII123,
    KANTO_SUBREGION_SEVII45,
    KANTO_SUBREGION_SEVII67,
    KANTO_SUBREGION_COUNT
};

#endif  // GUARD_CONSTANTS_REGIONS_H
