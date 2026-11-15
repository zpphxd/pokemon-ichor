#ifndef GUARD_CONSTANTS_ICHOR_POSTGAME_H
#define GUARD_CONSTANTS_ICHOR_POSTGAME_H

// The post-game's opening (design/POSTGAME.md §1; design/postgame/BUILD.md, batch 1).
// Scripts in data/scripts/ichor_postgame_opening.pory and ichor_postgame_crew.pory;
// placements on other branches' maps in design/postgame/PLACEMENTS.md.

// Heralds of the Olympic truce (spondophoroi): VAR_0x8004 for EventScript_IchorHerald.
// One per town in AETHOS_MAP.md's list. Atlantis has none: it is under the sea.
#define ICHOR_HERALD_ELAIA       0
#define ICHOR_HERALD_AKTI        1
#define ICHOR_HERALD_EMPORION    2
#define ICHOR_HERALD_ELEUSA      3
#define ICHOR_HERALD_THYRSA      4
#define ICHOR_HERALD_ARKADIA     5
#define ICHOR_HERALD_ASTYRA      6
#define ICHOR_HERALD_KALDERA     7
#define ICHOR_HERALD_KYTHERA     8
#define ICHOR_HERALD_AMNISOS     9
#define ICHOR_HERALD_LAKONIA    10
#define ICHOR_HERALD_DELPHOI    11
#define ICHOR_HERALD_OLYMPUS    12
#define ICHOR_HERALD_TAINARON   13
#define ICHOR_HERALD_OLYMPIA    14
#define ICHOR_HERALD_COUNT      15

// ICHOR_STUB_PG_FLAGS: the Katabasis is done once VAR_ICHOR_KATABASIS reaches "the
// Ascent done" (UNDERWORLD.md §13 lists the states in order; this is the 18th).
// Batch 3 owns the var's values and replaces this with its own constant.
#define ICHOR_PG_KATABASIS_DONE 18

// ICHOR_STUB_CARRIED_FLAME: Hestia's fire for the Euploia (Lampon's recruitment). The
// engine's FLAME_HESTIA_SHIP is on ichor-engine's branch; this stands in until it
// merges, and only the stubs in data/scripts/ichor_postgame_crew.pory compare with it.
#ifndef FLAME_HESTIA_SHIP
#define FLAME_HESTIA_SHIP 0x7F
#endif

#endif // GUARD_CONSTANTS_ICHOR_POSTGAME_H
