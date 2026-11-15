#ifndef GUARD_CONSTANTS_ICHOR_FLAG_STUBS_H
#define GUARD_CONSTANTS_ICHOR_FLAG_STUBS_H

// ICHOR_STUB_STORY_FLAGS: story flags that other sessions own, read by maps
// built before those sessions claim them (design/phase2/BUILD.md, "Stubs").
//
// Each is guarded, so it steps aside on its own once the owner claims the real
// flag in flags.h (this file is included at the end of flags.h). Delete a
// line when its flag is claimed; delete the file when it's empty.

// Beat 11 (the Emporion city agent): the herald's welcome on the quay. Beat 11
// plays the moment the Euploia ties up, so "the crossing is over" means it has
// played. Read by the Deigma, where Alethea waits for beat 12.
#ifndef FLAG_ICHOR_ARRIVED_EMPORION
#define FLAG_ICHOR_ARRIVED_EMPORION FLAG_ICHOR_CROSSING_DONE
#endif

#endif // GUARD_CONSTANTS_ICHOR_FLAG_STUBS_H
