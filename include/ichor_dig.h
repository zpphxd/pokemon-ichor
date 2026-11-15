#ifndef GUARD_ICHOR_DIG_H
#define GUARD_ICHOR_DIG_H

// Ichor: excavation with Alethea's Trowel (design/SYSTEMS.md §5). Map scripts
// goto EventScript_IchorDigSpot or EventScript_IchorDigFixed
// (data/scripts/ichor_dig.pory); design/ENGINE_API.md §8 lists the calls.

u16 Ichor_DigRollForTest(u32 spot, u32 tableArg); // the daily roll, without side effects

#endif // GUARD_ICHOR_DIG_H
