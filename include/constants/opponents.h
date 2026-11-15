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
#define TRAINER_ICHOR_IKARIOS                 160
#define TRAINER_ICHOR_PYTHODOROS              161
#define TRAINER_ICHOR_BOTRYS                  162
#define TRAINER_ICHOR_ASTYLOS                 163
#define TRAINER_ICHOR_TIMOLAOS                164
#define TRAINER_ICHOR_LYKIDAS                 165
#define TRAINER_ICHOR_EUIA                    166
#define TRAINER_ICHOR_BROMIA                  167
#define TRAINER_ICHOR_ARIMNESTOS              168
#define TRAINER_ICHOR_GRUNT_ILYS              169
#define TRAINER_ICHOR_KOMOS                   170
#define TRAINER_ICHOR_HAGNON                  171
#define TRAINER_ICHOR_GRUNT_ARGILLOS          172
#define TRAINER_ICHOR_GRUNT_KERAMOS           173
#define TRAINER_ICHOR_GRUNT_PLINTHOS          174
#define TRAINER_ICHOR_GRUNT_GYPSOS            175
#define TRAINER_ICHOR_OINOPION                176
#define TRAINER_ICHOR_LENAIA                  177
#define TRAINER_ICHOR_HEGELOCHOS              178
#define TRAINER_ICHOR_MYNNISKOS               179
#define TRAINER_ICHOR_THETTALOS               180
#define TRAINER_ICHOR_THEODOROS               181
#define TRAINER_ICHOR_THESPIS_1               182
#define TRAINER_ICHOR_GRUNT_BORBOROS          183
#define TRAINER_ICHOR_KLEON_3_KYNDER          184
#define TRAINER_ICHOR_KLEON_3_HIPLING         185
#define TRAINER_ICHOR_KLEON_3_NEBREL          186
#define TRAINER_ICHOR_SILENOS                 187
#define TRAINERS_END_ACT2                     188

// world-act3, ids 320-499: Kythera, Knossa, Lakonia, Delphoi, the Frozen Hour, Olympus.
#define TRAINERS_END_ACT3                     0

// The post-game, ids 500-679: the Labors, Katabasis, the Olympiad, the Odyssey, Atlantis.
#define TRAINERS_END_POSTGAME                 0

// The Oikoumene, ids 680-819: the second map.
#define TRAINERS_END_OIKOUMENE                0

// Ids 820-863 are the director's reserve.

#define ICHOR_TRAINERS_MAX(a, b) ((a) > (b) ? (a) : (b))
#define TRAINERS_COUNT_EMERALD ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(TRAINERS_END_SLICE, TRAINERS_END_FRONTIER), \
                                                                     ICHOR_TRAINERS_MAX(TRAINERS_END_ACT1, TRAINERS_END_ACT2)), \
                                                  ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(TRAINERS_END_ACT3, TRAINERS_END_POSTGAME), \
                                                                     TRAINERS_END_OIKOUMENE))

// Ichor: one trainer flag per id, from TRAINER_FLAGS_START (0x500). 864 is upstream's
// value, so the flag and save layouts match upstream's again: ids 1-863 for about
// 700 trainers. Raising it shifts every system flag and grows SaveBlock1.
#define MAX_TRAINERS_COUNT_EMERALD 864

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
