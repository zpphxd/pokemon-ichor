#ifndef GUARD_CONSTANTS_OPPONENTS_H
#define GUARD_CONSTANTS_OPPONENTS_H

#include "constants/battle_partner.h"
#include "constants/opponents_frlg.h"

#define TRAINER_NONE                          0

// Ichor: Emerald's 855 Hoenn trainers are cut (hoenn-cut, batch 1), and Ichor's own
// start at 1. Each owner adds trainers only inside its id range, listed in
// tools/ichor/claim_ranges.md, and only in its own block below. Every block ends
// with its TRAINERS_END_* line: keep it at your highest id + 1 (0 while the block
// is empty). TRAINERS_COUNT_EMERALD is the largest of them, so gTrainers grows
// only as far as the trainers that exist, and no two owners edit the same line.

// The slice: Kalliste Isle, ids 1-14 (full). See design/phase1/SCRIPT.md Part 3.
#define TRAINER_ICHOR_KLEON_ELAIA_SNIVY       1
#define TRAINER_ICHOR_KLEON_ELAIA_CYNDAQUIL   2
#define TRAINER_ICHOR_KLEON_ELAIA_PIPLUP      3
#define TRAINER_ICHOR_TITYROS                 4
#define TRAINER_ICHOR_PHYLLIS                 5
#define TRAINER_ICHOR_KOMATAS                 6
#define TRAINER_ICHOR_AGIS                    7
#define TRAINER_ICHOR_POLYEIDOS               8
#define TRAINER_ICHOR_GRUNT_RUINS_PETROS      9
#define TRAINER_ICHOR_GRUNT_RUINS_AMATHOS     10
#define TRAINER_ICHOR_LAMPON                  11
#define TRAINER_ICHOR_PYRRHA                  12
#define TRAINER_ICHOR_AITHRA                  13
#define TRAINER_ICHOR_IONE_1                  14
#define TRAINERS_END_SLICE                    15

// The Frontier engine, ids 15-21: the seven Hoenn Frontier Brains, kept because
// gFrontierBrainInfo (src/frontier_util.c) takes each Brain's pic, class and name
// from gTrainers. The post-game re-themes them as the Olympiad's Brains.
#define TRAINER_ANABEL                        15
#define TRAINER_TUCKER                        16
#define TRAINER_SPENSER                       17
#define TRAINER_GRETA                         18
#define TRAINER_NOLAND                        19
#define TRAINER_LUCY                          20
#define TRAINER_BRANDON                       21
#define TRAINERS_END_FRONTIER                 22

// Ids 22-39 are the director's reserve.

// world-act1, ids 40-159: the crossing, Aegina, Emporion, the Sacred Way, Eleusa.
#define TRAINERS_END_ACT1                     0

// world-act2, ids 160-319: Thyrsa, Arkadia, Astyra, Kaldera.
#define TRAINERS_END_ACT2                     0

// world-act3, ids 320-499: Kythera, Knossa, Lakonia, Delphoi, the Frozen Hour, Olympus.
// Each region takes the next ids, in design/phase4/SCRIPT.md Part 3's order.

// Kythera and Melos, ids 320-347 (Part 3, "Kythera's trainers"): the Euploia's
// voyage, Melos, Route 22, Skandeia, the Foam Road, the spring and Echo's caves,
// the Temple of Aphrodite, the Neraida falls, Route 23 and Antikythera.
// The sea routes' extra swimmers, divers and sailors (MAP_DESIGN.md §8.2's
// sea-route minimum) follow at 348-358. Knossa continues at 359.
#define TRAINER_ICHOR_EUDOROS                 320
#define TRAINER_ICHOR_KERDON                  321
#define TRAINER_ICHOR_KIMOLOS                 322
#define TRAINER_ICHOR_THEION                  323
#define TRAINER_ICHOR_KYMAIOS                 324
#define TRAINER_ICHOR_ANTALKIDAS              325
#define TRAINER_ICHOR_NIKANDROS               326
#define TRAINER_ICHOR_HAGNE                   327
#define TRAINER_ICHOR_MOLYBDOS                328
#define TRAINER_ICHOR_OCHROS                  329
#define TRAINER_ICHOR_PSEPHOS                 330
#define TRAINER_ICHOR_AMPHITOS                331
#define TRAINER_ICHOR_SKOPAS                  332
#define TRAINER_ICHOR_PONTINOS                333
#define TRAINER_ICHOR_KASSITEROS              334
#define TRAINER_ICHOR_PHILOTES                335
#define TRAINER_ICHOR_KALAMIS                 336
#define TRAINER_ICHOR_KOLYMBOS                337
#define TRAINER_ICHOR_ANTHOUSA                338
#define TRAINER_ICHOR_RHODANTHE               339
#define TRAINER_ICHOR_GALATEA_1               340
#define TRAINER_ICHOR_LYKIDAS                 341
#define TRAINER_ICHOR_KERINTHOS               342
#define TRAINER_ICHOR_MOPSOS                  343
#define TRAINER_ICHOR_THESTYLIS               344
#define TRAINER_ICHOR_BATHYLLOS               345
#define TRAINER_ICHOR_EUTHYKLES               346
#define TRAINER_ICHOR_MYRSINE                 347
#define TRAINER_ICHOR_AKTAIOS                 348
#define TRAINER_ICHOR_NERINE                  349
#define TRAINER_ICHOR_PHORBAS                 350
#define TRAINER_ICHOR_LAMPROS                 351
#define TRAINER_ICHOR_PSAMATHE                352
#define TRAINER_ICHOR_PELAGON                 353
#define TRAINER_ICHOR_KLEITOS                 354
#define TRAINER_ICHOR_DOROS                   355
#define TRAINER_ICHOR_AKAMAS                  356
#define TRAINER_ICHOR_EIONE                   357
#define TRAINER_ICHOR_NAUPLIOS                358

// Kythera, ids 490-498 (MAP_DESIGN §8's route standard): the Foam Road's and the
// Neraida falls' second wave, from the top of act3's range so Knossa's 348 on stay free.
#define TRAINER_ICHOR_LYKON_KYTHERA                  490
#define TRAINER_ICHOR_THEANO                 491
#define TRAINER_ICHOR_KYMODOKE               492
#define TRAINER_ICHOR_MENALKAS               493
#define TRAINER_ICHOR_AMARYLLIS              494
#define TRAINER_ICHOR_DAPHNIS                495
#define TRAINER_ICHOR_OPORA                  496
#define TRAINER_ICHOR_PEGAIOS                497
#define TRAINER_ICHOR_DEXITHEA               498

#define TRAINERS_END_ACT3                     499

// The post-game, ids 500-679: the Labors, Katabasis, the Olympiad, the Odyssey, Atlantis.
#define TRAINERS_END_POSTGAME                 0

// The Oikoumene, ids 680-819 and 864-1023: the second map.
#define TRAINERS_END_OIKOUMENE                0

// Ids 820-863 are the director's reserve. 864-1023 are the Oikoumene's (above).

#define ICHOR_TRAINERS_MAX(a, b) ((a) > (b) ? (a) : (b))
#define TRAINERS_COUNT_EMERALD ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(TRAINERS_END_SLICE, TRAINERS_END_FRONTIER), \
                                                                     ICHOR_TRAINERS_MAX(TRAINERS_END_ACT1, TRAINERS_END_ACT2)), \
                                                  ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(TRAINERS_END_ACT3, TRAINERS_END_POSTGAME), \
                                                                     TRAINERS_END_OIKOUMENE))

// Ichor: one trainer flag per id, from TRAINER_FLAGS_START (0x500): ids 1-1023. Raised
// from upstream's 864 for the Oikoumene's champion halls (design/OIKOUMENE.md PG-38).
// Raising it shifts every system flag and grows SaveBlock1.
#define MAX_TRAINERS_COUNT_EMERALD 1024

// Ichor: temporary. Maps the removed Hoenn names to TRAINER_NONE until batch 2
// deletes the Hoenn scripts that still use them. Never use these names.
#include "constants/opponents_hoenn_stub.h"

#if IS_FRLG
#define TRAINERS_COUNT                      TRAINERS_COUNT_FRLG
#define MAX_TRAINERS_COUNT                  MAX_TRAINERS_COUNT_FRLG
#else
#define TRAINERS_COUNT                      TRAINERS_COUNT_EMERALD
#define MAX_TRAINERS_COUNT                  MAX_TRAINERS_COUNT_EMERALD
#endif
#define TRAINER_PARTNER(partner)           (MAX_TRAINERS_COUNT + partner)

#endif  // GUARD_CONSTANTS_OPPONENTS_H
