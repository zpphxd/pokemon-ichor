// Ichor: the great herms (design/SYSTEMS.md §4; design/ENGINE_API.md §4).
//
// One row per route's great herm: the map it stands on (the herm's bg event runs
// EventScript_IchorGreatHerm), the region map section that becomes a fly target
// once it's anointed, and the heal location on the tile south of the herm, where
// Daedalus's Wings land. Add a row, and that heal location in
// src/data/heal_locations.json, when a route's herm is placed. The Oikoumene's
// waystones take ids from HERM_OIKOUMENE_FIRST (include/constants/ichor.h).
const struct IchorHerm gIchorHerms[HERM_MAX] =
{
    [HERM_KALLISTE_ROUTE_1] = {
        .map = MAP_KALLISTE_ROUTE1,
        .mapsec = MAPSEC_KALLISTE_ROUTE_1,
        .healLocation = HEAL_LOCATION_HERM_KALLISTE_ROUTE_1,  // the spur fork, (14,20); land at (14,21)
    },
    [HERM_AETHOS_ROUTE_11] = {
        .map = MAP_ROUTE11_KRATHIS_GORGE,
        .mapsec = MAPSEC_AETHOS_ROUTE_11,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_11,  // the river-spur fork, (27,35); land on the road at (26,36)
    },
    [HERM_AETHOS_ROUTE_12] = {
        .map = MAP_ROUTE12_CYPRESS_ROAD,
        .mapsec = MAPSEC_AETHOS_ROUTE_12,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_12,  // by the Cave of Maia, (23,11); land at (23,12)
    },
    [HERM_AETHOS_ROUTE_6] = {
        .map = MAP_ROUTE6_ELEUTHERAI_ROAD,
        .mapsec = MAPSEC_AETHOS_ROUTE_6,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_6,  // the spur fork, (34,7); land at (34,8)
    },
    [HERM_AETHOS_ROUTE_7] = {
        .map = MAP_ROUTE7_KRONIA_GROUNDS,
        .mapsec = MAPSEC_AETHOS_ROUTE_7,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_7,  // the mountain's foot, (24,15); land at (24,16)
    },
    [HERM_AETHOS_ROUTE_8] = {
        .map = MAP_ROUTE8_KOPAIS,
        .mapsec = MAPSEC_AETHOS_ROUTE_8,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_8,    // the spur fork, (24,14); land at (24,15)
    },
    [HERM_AETHOS_ROUTE_9] = {
        .map = MAP_ROUTE9_SCHISTE,
        .mapsec = MAPSEC_AETHOS_ROUTE_9,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_9,  // the Split Road's crossroads, (30,14); land at (30,15)
    },
};
