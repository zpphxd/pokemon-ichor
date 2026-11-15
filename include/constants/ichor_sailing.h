#ifndef GUARD_CONSTANTS_ICHOR_SAILING_H
#define GUARD_CONSTANTS_ICHOR_SAILING_H

// Ichor postgame: the sailing layer (design/postgame/ENGINE.md, design/ODYSSEY.md
// §2 and §4). Shared by C and event scripts, so everything here is a #define.

// --- The ship's look and her deck --------------------------------------------------

// The Euploia at sea, 64x64, the standard 9-frame layout: sail full (downwind and
// crosswind) and slack (upwind and calm). The sprites agent's sheets (pg-b1-sprites)
// stand on the frame's bottom-middle 16x16 (design/postgame/SPRITES.md).
#define ICHOR_SHIP_GFX         OBJ_EVENT_GFX_ICHOR_EUPLOIA
#define ICHOR_SHIP_GFX_SLACK   OBJ_EVENT_GFX_ICHOR_EUPLOIA_SLACK

// Where boarding a moored ship, going below and every helm action arrive.
// ICHOR_STUB_EUPLOIA_DECK: a test room of the sail-engine's until the euploia
// agent's MAP_EUPLOIA_DECK merges; then point these three at it and delete the room.
#define ICHOR_SHIP_DECK_MAP    MAP_PG_TEST_DECK              // ICHOR_STUB_EUPLOIA_DECK
#define ICHOR_SHIP_DECK_X      4                             // ICHOR_STUB_EUPLOIA_DECK
#define ICHOR_SHIP_DECK_Y      4                             // ICHOR_STUB_EUPLOIA_DECK

// The Relic Ring's DECK entry's id (beside constants/ichor.h's ICHOR_RING_HEARTHFIRE).
#define ICHOR_RING_DECK        0xFFF1

// --- Wind -----------------------------------------------------------------------------

// The direction the wind blows FROM, as the Greeks named winds (Zephyros is the
// west wind, and it carries you east). Eight points, clockwise from north.
#define ICHOR_WIND_N            0
#define ICHOR_WIND_NE           1
#define ICHOR_WIND_E            2
#define ICHOR_WIND_SE           3
#define ICHOR_WIND_S            4
#define ICHOR_WIND_SW           5
#define ICHOR_WIND_W            6
#define ICHOR_WIND_NW           7
#define ICHOR_WIND_DIRECTIONS   8

// Strength. Ichor_SetWind also takes ICHOR_WIND_BECALMED: an event calm that the
// daily reset doesn't replace (any other strength lifts it).
#define ICHOR_WIND_CALM         0
#define ICHOR_WIND_FRESH        1
#define ICHOR_WIND_STRONG       2
#define ICHOR_WIND_BECALMED     3

// IchorEpics.wind's bits: direction 0-2, strength 3-4, Poseidon's grudge 5, becalmed 6.
#define ICHOR_WIND_DIR_MASK         0x07
#define ICHOR_WIND_STRENGTH_SHIFT   3
#define ICHOR_WIND_STRENGTH_MASK    0x18
#define ICHOR_WIND_GRUDGE_BIT       0x20
#define ICHOR_WIND_BECALMED_BIT     0x40

// The ship's heading against the wind (Ichor_GetSailing).
#define ICHOR_SAIL_CALM         0   // no wind, or becalmed: the oarsmen row
#define ICHOR_SAIL_DOWNWIND     1   // the wind within 45 degrees of behind you
#define ICHOR_SAIL_CROSSWIND    2
#define ICHOR_SAIL_UPWIND       3   // the wind within 45 degrees of ahead

// --- The helm ---------------------------------------------------------------------------

// Nausikles's menu (Ichor_BuildHelmMenu), as VAR_RESULT.
#define ICHOR_HELM_TAKE_HER_OUT 1
#define ICHOR_HELM_CAST_OFF     2
#define ICHOR_HELM_SET_COURSE   3
#define ICHOR_HELM_WIND         4
#define ICHOR_HELM_STAY         5

// --- The helm's voyages -----------------------------------------------------------------

// One id per port, each with one row in src/data/ichor_voyages.h. To add a port,
// append one line here and one row there; nothing else changes.
#define VOYAGE_NONE             0   // at sea, not moored anywhere
#define VOYAGE_AKTI             1
#define VOYAGE_ROUTE33          2   // the western sea (the westsea agent's row)
#define VOYAGE_CAPE_TAINARON    3
#define VOYAGE_KNOSSA           4
#define VOYAGE_LECHAION         5
#define VOYAGE_KALDERA          6
// The Labors' and the Oikoumene's ports follow here.

#endif // GUARD_CONSTANTS_ICHOR_SAILING_H
