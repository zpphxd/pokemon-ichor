#ifndef GUARD_CONSTANTS_ICHOR_POSTGAME_SEA_H
#define GUARD_CONSTANTS_ICHOR_POSTGAME_SEA_H

// Ichor (world-postgame): the post-game's seas. Route 33 (batch 1) first; the
// Odyssey's sea maps (batch 6) reuse data/scripts/ichor_postgame_sea.pory.

// ICHOR_STUB_PG_FLAGS: Labor 10's Pillars of Herakles are set (design/LABORS.md),
// which opens the way through the fog bank toward Atlantis. Batches 4-5 claim
// the real flag; until then this is flag 0, which is never set, so the fog stays
// shut. The build lead swaps this #define for the claimed one.
#define FLAG_ICHOR_L10_PILLARS 0

// Route 33's cells and metatiles: written by tools/ichor/maps/westsea.py. Don't edit by hand.
#define METATILE_R33_SEA           0x170  // aethos's open sea
#define METATILE_R33_CURRENT_W     0x233  // westsea's westward current
#define METATILE_R33_RAFT_L        0x290  // Kymon's raft, left cell
#define METATILE_R33_RAFT_R        0x291  // Kymon's raft, right cell
#define R33_WHIRL_ECHINADES_X      14  // the Echinades' whirlpool, top-left (2x2)
#define R33_WHIRL_ECHINADES_Y      38
#define R33_WHIRL_LAGOON_X         33  // the lagoon's whirlpool, top-left (2x2)
#define R33_WHIRL_LAGOON_Y         11
#define R33_ROCKS_COVE_X           42  // the cove's loose rock: two cells east-west
#define R33_ROCKS_COVE_Y           51
#define R33_ROCKS_CURRENT_X        40  // the current's loose rock: two cells north-south
#define R33_ROCKS_CURRENT_Y        66
#define R33_RAFT_SEA_X             47  // Kymon's raft, becalmed (2x1)
#define R33_RAFT_SEA_Y             57
#define R33_RAFT_HOME_X            21  // Kymon's raft, moored at Halia's jetty (2x1)
#define R33_RAFT_HOME_Y            48
#define R33_TOW_X                  23  // where the tow leaves you: the jetty's landing
#define R33_TOW_Y                  47
#define R33_FOG_ON_X               13  // the fog's approach: weather on west of here
#define R33_FOG_TOP_Y              52  // and south of here
// End of Route 33's cells and metatiles.

#endif // GUARD_CONSTANTS_ICHOR_POSTGAME_SEA_H
