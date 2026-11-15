// Ichor postgame: the helm's voyages (design/postgame/ENGINE.md §3).
//
// One row per VOYAGE_* port (include/constants/ichor_sailing.h). To add a port,
// append one #define there and one row here; the helm's list, the landing and
// the crossing all read this table.
//
//   .name      the port in prose ("Go ashore at Akti?"); the helm's list shows it
//              in capitals
//   .crossing  Nausikles's line as SET A COURSE leaves for it (two short lines)
//   .gateFlag  on the helm's list once this flag is set; 0 keeps the port closed
//   .quay*     where you step ashore. VOYAGE_NO_QUAY for a port of open sea: a
//              course set for it puts you straight out on its sea map.
//   .sea*      her sea map off this port, where CAST OFF and boarding put you, in
//              the ship, heading .seaDir. VOYAGE_NO_SEA: she moors, and boarding
//              takes you onto the deck.

#define VOYAGE_QUAY(map, x, y)         .quayMap = (map), .quayX = (x), .quayY = (y)
#define VOYAGE_NO_QUAY                 .quayMap = MAP_UNDEFINED
#define VOYAGE_SEA(map, x, y, dir)     .seaMap = (map), .seaX = (x), .seaY = (y), .seaDir = (dir)
#define VOYAGE_NO_SEA                  .seaMap = MAP_UNDEFINED

static const struct IchorVoyage sIchorVoyages[] =
{
    [VOYAGE_NONE] = {
        .name = COMPOUND_STRING("the open sea"),
        .crossing = COMPOUND_STRING(""),
        .gateFlag = 0,
        VOYAGE_NO_QUAY,
        VOYAGE_NO_SEA,
    },

    // Akti's quay, just south of the slice's gangplank at (7,9) where the trireme
    // lies along the mole. Her home port: a new ship is moored here.
    [VOYAGE_AKTI] = {
        .name = COMPOUND_STRING("Akti"),
        .crossing = COMPOUND_STRING("NAUSIKLES: Home to Akti, then.\nThe gulls will be glad of us."),
        .gateFlag = FLAG_ICHOR_GOT_EUPLOIA,
        VOYAGE_QUAY(MAP_AKTI_TOWN, 7, 10),
        VOYAGE_NO_SEA,
    },

    // The westsea agent's row: Route 33, the western sea, a port of open sea.
    // [VOYAGE_ROUTE33] = {
    //     .name = COMPOUND_STRING("the western sea"),
    //     .crossing = COMPOUND_STRING("NAUSIKLES: West, then, past Maleia.\nOpen water all the way."),
    //     .gateFlag = FLAG_ICHOR_GOT_EUPLOIA,
    //     VOYAGE_NO_QUAY,
    //     VOYAGE_SEA(MAP_ROUTE33_WESTERN_SEA, <x>, <y>, DIR_WEST),
    // },
    [VOYAGE_ROUTE33] = {  // ICHOR_PG_PORT_PENDING: the westsea agent's row replaces this
        .name = COMPOUND_STRING("the western sea"),
        .crossing = COMPOUND_STRING(""),
        .gateFlag = 0,
        VOYAGE_NO_QUAY,
        VOYAGE_NO_SEA,
    },

    // ICHOR_PG_PORT_PENDING: Cape Tainaron (batch 3), its quay and Route 33 off it.
    [VOYAGE_CAPE_TAINARON] = {
        .name = COMPOUND_STRING("Cape Tainaron"),
        .crossing = COMPOUND_STRING("NAUSIKLES: Round the Mani to Tainaron.\nWhere the road goes down. I'll wait."),
        .gateFlag = 0,
        VOYAGE_NO_QUAY,  // MAP_CAPE_TAINARON's quay
        VOYAGE_NO_SEA,   // MAP_ROUTE33_WESTERN_SEA, off the cape
    },

    // ICHOR_PG_PORT_PENDING: Knossa's harbor at Amnisos (world-act2's map).
    [VOYAGE_KNOSSA] = {
        .name = COMPOUND_STRING("Knossa"),
        .crossing = COMPOUND_STRING("NAUSIKLES: South to Knossa.\nThey still paint bulls on everything."),
        .gateFlag = 0,
        VOYAGE_NO_QUAY,
        VOYAGE_NO_SEA,
    },

    // ICHOR_PG_PORT_PENDING: Lechaion, Emporion's harbor by the Diolkos (Nolan's quay).
    [VOYAGE_LECHAION] = {
        .name = COMPOUND_STRING("Lechaion"),
        .crossing = COMPOUND_STRING("NAUSIKLES: Up the gulf to Lechaion.\nThey haul ships over land there. Madness."),
        .gateFlag = 0,
        VOYAGE_NO_QUAY,
        VOYAGE_NO_SEA,
    },

    // ICHOR_PG_PORT_PENDING: Kaldera's harbor, under Talos's forge.
    [VOYAGE_KALDERA] = {
        .name = COMPOUND_STRING("Kaldera"),
        .crossing = COMPOUND_STRING("NAUSIKLES: Out to Kaldera. You'll smell\nthe forge before you see the island."),
        .gateFlag = 0,
        VOYAGE_NO_QUAY,
        VOYAGE_NO_SEA,
    },
};

#undef VOYAGE_QUAY
#undef VOYAGE_NO_QUAY
#undef VOYAGE_SEA
#undef VOYAGE_NO_SEA
