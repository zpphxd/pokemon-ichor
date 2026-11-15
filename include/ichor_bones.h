#ifndef GUARD_ICHOR_BONES_H
#define GUARD_ICHOR_BONES_H

// Ichor: knucklebones (design/SYSTEMS.md §9). Map scripts call
// EventScript_IchorKnucklebones (data/scripts/ichor_bones.pory);
// design/ENGINE_API.md §7 lists the calls.

// For the C tests: bones are face indices 0-3 (1, 3, 4, 6)
u32 Ichor_BonesTestCompare(const u8 *you, const u8 *them);
u32 Ichor_BonesTestMarks(u32 opponent, const u8 *bones);

#endif // GUARD_ICHOR_BONES_H
