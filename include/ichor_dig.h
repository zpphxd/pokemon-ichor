#ifndef GUARD_ICHOR_DIG_H
#define GUARD_ICHOR_DIG_H

// Ichor: excavation with Alethea's Trowel (design/SYSTEMS.md §5). Map scripts
// goto EventScript_IchorDigSpot or EventScript_IchorDigFixed
// (data/scripts/ichor_dig.pory); design/ENGINE_API.md §8 lists the calls.

u16 Ichor_DigRollForTest(u32 spot, u32 tableArg); // the daily roll, without side effects
u16 Ichor_AmphoraStatus(u32 amphora);
u16 Ichor_BufferAmphora(void);
u16 Ichor_RestoreAmphora(void);
u16 Ichor_BufferAmphoraNotes(void);
void Ichor_BuildAmphoraMenu(void);
u16 Ichor_ShowAmphoraPicture(void);
void Ichor_HideAmphoraPicture(void);

#endif // GUARD_ICHOR_DIG_H
