#include "global.h"
#include "event_data.h"
#include "regions.h"
#include "constants/heal_locations.h"
#include "constants/vars.h"


static const u16 sKantoSubregionMapsecs[KANTO_SUBREGION_COUNT][30] = {
    [KANTO_SUBREGION_KANTO] =
    {
        MAPSEC_NONE
    },
    [KANTO_SUBREGION_SEVII123] =
    {
        MAPSEC_ONE_ISLAND,
        MAPSEC_TWO_ISLAND,
        MAPSEC_THREE_ISLAND,
        MAPSEC_KINDLE_ROAD,
        MAPSEC_TREASURE_BEACH,
        MAPSEC_CAPE_BRINK,
        MAPSEC_BOND_BRIDGE,
        MAPSEC_THREE_ISLE_PORT,
        MAPSEC_MT_EMBER,
        MAPSEC_BERRY_FOREST,
        MAPSEC_THREE_ISLE_PATH,
        MAPSEC_EMBER_SPA,
        MAPSEC_NONE
    },
    [KANTO_SUBREGION_SEVII45] =
    {
        MAPSEC_FOUR_ISLAND,
        MAPSEC_FIVE_ISLAND,
        MAPSEC_RESORT_GORGEOUS,
        MAPSEC_WATER_LABYRINTH,
        MAPSEC_FIVE_ISLE_MEADOW,
        MAPSEC_MEMORIAL_PILLAR,
        MAPSEC_NAVEL_ROCK_FRLG,
        MAPSEC_ICEFALL_CAVE,
        MAPSEC_ROCKET_WAREHOUSE,
        MAPSEC_LOST_CAVE,
        MAPSEC_NONE
    },
    [KANTO_SUBREGION_SEVII67] =
    {
        MAPSEC_SEVEN_ISLAND,
        MAPSEC_SIX_ISLAND,
        MAPSEC_OUTCAST_ISLAND,
        MAPSEC_GREEN_PATH,
        MAPSEC_WATER_PATH,
        MAPSEC_RUIN_VALLEY,
        MAPSEC_TRAINER_TOWER,
        MAPSEC_CANYON_ENTRANCE,
        MAPSEC_SEVAULT_CANYON,
        MAPSEC_TANOBY_RUINS,
        MAPSEC_SEVII_ISLE_22,
        MAPSEC_SEVII_ISLE_23,
        MAPSEC_SEVII_ISLE_24,
        MAPSEC_TRAINER_TOWER_2,
        MAPSEC_DOTTED_HOLE,
        MAPSEC_PATTERN_BUSH,
        MAPSEC_ALTERING_CAVE_FRLG,
        MAPSEC_TANOBY_CHAMBERS,
        MAPSEC_TANOBY_KEY,
        MAPSEC_BIRTH_ISLAND_FRLG,
        MAPSEC_MONEAN_CHAMBER,
        MAPSEC_LIPTOO_CHAMBER,
        MAPSEC_WEEPTH_CHAMBER,
        MAPSEC_DILFORD_CHAMBER,
        MAPSEC_SCUFIB_CHAMBER,
        MAPSEC_RIXY_CHAMBER,
        MAPSEC_VIAPOIS_CHAMBER,
        MAPSEC_NONE
    }
};

enum KantoSubRegion GetKantoSubregion(u32 mapSecId)
{
    // Ichor: outside an FRLG build the Sevii names above are aliases for the
    // Oikoumene's tail (constants/region_map_sections_oikoumene.h), and the
    // Oikoumene is one chart: never a Sevii sub-chart.
    if (!IS_FRLG)
        return KANTO_SUBREGION_KANTO;
    for (u32 i = KANTO_SUBREGION_KANTO; i <= KANTO_SUBREGION_SEVII67; i++)
    {
        for (u32 j = 0; sKantoSubregionMapsecs[i][j] != MAPSEC_NONE; j++)
        {
            if (mapSecId == sKantoSubregionMapsecs[i][j])
                return i;
        }
    }
    return KANTO_SUBREGION_KANTO;
}

// Ichor: the Oikoumene chart's saved state, the bank var VAR_ICHOR_OIK_CHART
// (design/oikoumene/BUILD.md §5, "The chart"):
//   bits 0-1   the last Oikoumene port you were in, an index into sOikoumenePorts.
//              THE OIKOUMENE, the Aethos chart's crossing target, flies you there.
//   bits 2-15  the towns you've been to, one bit each in sOikoumeneTowns's order.
//              A town's fly target opens once its bit is set, so the towns' own
//              scripts needn't set a visited flag.
// Both are kept up on every map load (Ichor_TrackOikoumene, from overworld.c).
#define OIK_PORT_BITS   2
#define OIK_PORT_MASK   ((1 << OIK_PORT_BITS) - 1)
#define OIK_TOWN_SHIFT  OIK_PORT_BITS

static const struct { u8 mapSec; u8 healLocation; } sOikoumenePorts[1 << OIK_PORT_BITS] =
{
    {MAPSEC_SESTOS,     HEAL_LOCATION_SESTOS},     // the default
    {MAPSEC_NAUKRATIS,  HEAL_LOCATION_NAUKRATIS},
    {MAPSEC_KROTON,     HEAL_LOCATION_NONE},       // batch 5's; Sestos until Kroton has a heal location
    {MAPSEC_THEMISKYRA, HEAL_LOCATION_NONE},       // LABORS's; Sestos until Themiskyra has one
};

// The towns with fly targets on the Oikoumene chart (region_map.c's sFlyLocations).
// Later batches add theirs at the end: never reorder, saves keep the bits.
static const u8 sOikoumeneTowns[] =
{
    MAPSEC_SESTOS,
    MAPSEC_ILION,
    MAPSEC_NAUKRATIS,
    MAPSEC_MEMPHIS,
    MAPSEC_SALMYDESSOS,
    MAPSEC_AIA,
};
STATIC_ASSERT(ARRAY_COUNT(sOikoumeneTowns) <= 16 - OIK_TOWN_SHIFT, OikoumeneTownsFitTheChartVar);

static s32 GetOikoumeneTownIndex(u32 mapSecId)
{
    for (u32 i = 0; i < ARRAY_COUNT(sOikoumeneTowns); i++)
    {
        if (sOikoumeneTowns[i] == mapSecId)
            return i;
    }
    return -1;
}

bool32 Ichor_IsOikoumeneTown(u32 mapSecId)
{
    return GetOikoumeneTownIndex(mapSecId) >= 0;
}

bool32 Ichor_IsOikoumeneTownVisited(u32 mapSecId)
{
    s32 i = GetOikoumeneTownIndex(mapSecId);
    return i >= 0 && ((VarGet(VAR_ICHOR_OIK_CHART) >> (OIK_TOWN_SHIFT + i)) & 1);
}

void Ichor_TrackOikoumene(void)
{
    u32 mapSecId = gMapHeader.regionMapSectionId;
    u32 state;
    s32 town;

    if (!IsOikoumeneMapSec(mapSecId))
        return;
    state = VarGet(VAR_ICHOR_OIK_CHART);
    for (u32 i = 0; i < ARRAY_COUNT(sOikoumenePorts); i++)
    {
        if (sOikoumenePorts[i].mapSec == mapSecId)
            state = (state & ~OIK_PORT_MASK) | i;
    }
    town = GetOikoumeneTownIndex(mapSecId);
    if (town >= 0)
        state |= 1 << (OIK_TOWN_SHIFT + town);
    VarSet(VAR_ICHOR_OIK_CHART, state);
}

u32 Ichor_GetOikoumenePortHealLocation(void)
{
    u32 port = VarGet(VAR_ICHOR_OIK_CHART) & OIK_PORT_MASK;
    if (sOikoumenePorts[port].healLocation == HEAL_LOCATION_NONE)
        port = 0;
    return sOikoumenePorts[port].healLocation;
}
