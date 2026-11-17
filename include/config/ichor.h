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

// Ichor: the catch mash (src/ichor_catch.c, design/ENGINE_API.md §12). When the player throws
// a ball, a short "Tap A!" beat opens before the odds are rolled, and each A press raises the
// modified catch rate a little. The odds are still rolled once, after the beat, so the shakes
// the player sees always match the result.
//   - Ten presses is about 6.7 a second over the 1.5 s window: steady mashing gets there,
//     and the window closes as soon as it does, so a good masher also throws sooner.
//   - x1.3 at the cap. Catch chance tracks the modified rate almost linearly below the
//     auto-catch line, so a 20% throw becomes 26%: well short of a Great Ball's x1.5.
//   - The boosted rate is capped at 254, one short of the auto-catch line, so the shake
//     rolls always happen and mashing never guarantees a catch. Master Balls, auto-catches,
//     trainer battles, the catch tutorial and Oath-refused battles get no window at all.
#define ICHOR_CATCH_MASH              1    // 0 turns the window and the bonus off
#define ICHOR_CATCH_MASH_FRAMES       90   // the longest the window stays open (1.5 s)
#define ICHOR_CATCH_MASH_CAP          10   // presses that count; more add nothing
#define ICHOR_CATCH_MASH_MAX_BONUS    30   // percent added to the catch rate at the cap
#define ICHOR_CATCH_MASH_ODDS_CEILING 254  // the highest rate mashing can reach (255 auto-catches)

#endif // GUARD_CONFIG_ICHOR_H
