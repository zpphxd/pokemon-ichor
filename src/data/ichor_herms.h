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
    [HERM_AETHOS_ROUTE_4] = {
        .map = MAP_ROUTE4_ISTHMUS,
        .mapsec = MAPSEC_AETHOS_ROUTE_4,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_4,    // the desecrated herm off the spur, (23,7); land at (23,8)
    },
    [HERM_AETHOS_ROUTE_5] = {
        .map = MAP_ROUTE5_SKIRONIAN_CLIFFS,
        .mapsec = MAPSEC_AETHOS_ROUTE_5,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_5,    // by the inn, (58,20); land at (58,21)
    },
    [HERM_EMPORION_CITY] = {
        .map = MAP_EMPORION_CITY,
        .mapsec = MAPSEC_EMPORION_CITY,
        .healLocation = HEAL_LOCATION_HERM_EMPORION_CITY,
    },
    [HERM_AETHOS_ROUTE_13] = {
        .map = MAP_ROUTE13_HIGHLAND_ROAD,
        .mapsec = MAPSEC_AETHOS_ROUTE_13,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_13,
    },
    [HERM_AETHOS_ROUTE_14] = {
        .map = MAP_ROUTE14_NEMEA_ROAD,
        .mapsec = MAPSEC_AETHOS_ROUTE_14,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_14,
    },
    [HERM_AETHOS_ROUTE_15] = {
        .map = MAP_ROUTE15_MYSTERY_ROAD,
        .mapsec = MAPSEC_AETHOS_ROUTE_15,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_15,
    },
    [HERM_AETHOS_ROUTE_16] = {
        .map = MAP_ROUTE16_CAPITAL_PASS,
        .mapsec = MAPSEC_AETHOS_ROUTE_16,
        .healLocation = HEAL_LOCATION_HERM_AETHOS_ROUTE_16,
    },
};
