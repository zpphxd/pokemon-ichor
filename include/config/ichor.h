#ifndef GUARD_CONFIG_ICHOR_H
#define GUARD_CONFIG_ICHOR_H

// Ichor: Hoenn-only systems cut from the ROM (hoenn-cut batch 3, design/art/INVENTORY.md
// section 10). Each switch guards that system's entry points with #if, so the linker's
// --gc-sections drops its code and data. Upstream files keep their contents, and merges
// stay small. Set a switch to 0 to bring the system back. The values are 1/0, not
// TRUE/FALSE, because the event scripts test them too and TRUE is a C-only macro.

#define ICHOR_CUT_MULTIBOOT     1    // The Colosseum, e-Reader and Berry Glitch Fix multiboot programs
#define ICHOR_CUT_MINIGAMES     1    // Slots, roulette, Pokémon Jump, Berry Crush, Dodrio Berry Picking, the lottery
#define ICHOR_CUT_CONTESTS      1    // Contests, the Berry Blender and Pokéblocks
#define ICHOR_CUT_SECRET_BASES  1    // Secret bases and decorations
#define ICHOR_CUT_POKENAV       1    // The PokéNav and Match Call
#define ICHOR_CUT_MYSTERY_GIFT  1    // Mystery Gift, Mystery Events and the e-Reader
#define ICHOR_CUT_LINK          1    // Union Room, Cable Club, link trades and battles, record mixing
#define ICHOR_CUT_TV            1    // TV shows, Battle TV and Pokémon News
#define ICHOR_CUT_MIRAGE_TOWER  1    // Mirage Island and Mirage Tower
#define ICHOR_CUT_MAUVILLE_MAN  1    // The Mauville Old Man: the bard's Easy Chat songs (165 KB of phonemes), the storyteller,
                                     // the hipster, the trader, Giddy. Not on INVENTORY's approved list, but its maps are gone.

#endif // GUARD_CONFIG_ICHOR_H
