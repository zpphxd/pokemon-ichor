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
    [HERM_KYTHERA_FOAM_ROAD] = {
        .map = MAP_KYTHERA_FOAM_ROAD,
        .mapsec = MAPSEC_NONE,                                 // Skandeia is Kythera's fly target
        .healLocation = HEAL_LOCATION_HERM_KYTHERA_FOAM_ROAD,  // the fork, (43,6); land at (43,7)
    },
};
