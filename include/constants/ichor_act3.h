#ifndef GUARD_CONSTANTS_ICHOR_ACT3_H
#define GUARD_CONSTANTS_ICHOR_ACT3_H

// Ichor: constants for Act III's engine specials (design/phase4/ENGINE_ACT3.md).

// special Ichor_BullLeap (src/ichor_bull_leap.c): VAR_RESULT
#define ICHOR_LEAP_EARLY 0 // A before the object reached the line
#define ICHOR_LEAP_CLEAN 1 // A inside the window
#define ICHOR_LEAP_LATE  2 // no A before the window closed

// special Ichor_BullLeap: the defaults for VAR_0x8006 and VAR_0x8007 when 0
// (LABYRINTH.md §3, Hero)
#define ICHOR_LEAP_DEFAULT_WINDOW         10 // frames
#define ICHOR_LEAP_DEFAULT_FRAMES_PER_TILE 6

// Packs a map tile into one var, for Ichor_BullLeap's line (VAR_0x8005).
#define ICHOR_TILE(x, y) ((x) | ((y) << 8))

#endif // GUARD_CONSTANTS_ICHOR_ACT3_H
