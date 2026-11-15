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
#define TRAINER_ICHOR_KLEON_ELAIA_NEBREL       1
#define TRAINER_ICHOR_KLEON_ELAIA_KYNDER   2
#define TRAINER_ICHOR_KLEON_ELAIA_HIPLING      3
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

// The slice again, ids 22-25, from the director's reserve: Route 1's sixth
// trainer and the herders of Kronion Hill's high pastures (MAP_DESIGN.md §8).
#define TRAINER_ICHOR_THESTYLIS               22
#define TRAINER_ICHOR_MENALKAS                23
#define TRAINER_ICHOR_THYRSIS                 24
#define TRAINER_ICHOR_LYKIDAS                 25
#define TRAINERS_END_SLICE2                   26

// Ids 26-39 are the director's reserve.

// world-act1, ids 40-159: the crossing, Aegina, Emporion, the Sacred Way, Eleusa.
#define TRAINER_ICHOR_ALETHEA_DECK            40
#define TRAINER_ICHOR_PHORMION                41
#define TRAINER_ICHOR_LYKON                   42
// Emporion city agent, ids 43-59: Kleon at the Isthmus Gate, one team per starter
#define TRAINER_ICHOR_KLEON_2_KYNDER          43
#define TRAINER_ICHOR_KLEON_2_HIPLING         44
#define TRAINER_ICHOR_KLEON_2_NEBREL          45
// Emporion's interiors, ids 60-64 (the hiring hall)
#define TRAINER_ICHOR_GRUNT_EMPORION_CREW_BOSS 60
// The Temple of Hermes (ids 65-79; tools/ichor/maps/temple_hermes.py)
#define TRAINER_ICHOR_PODARGE                 65
#define TRAINER_ICHOR_EUCHIDAS                66
#define TRAINER_ICHOR_PHILONIDES              67
#define TRAINER_ICHOR_KERYKOS_1               68
// Route 4, the Isthmus road (batch 3, ids 80-99)
#define TRAINER_ICHOR_EXEKIAS                 80
#define TRAINER_ICHOR_MYRRHINE                81
#define TRAINER_ICHOR_GRUNT_ROUTE4_LAAS       82
#define TRAINER_ICHOR_MENALKAS_ISTHMUS             83
#define TRAINER_ICHOR_PHEIDIPPOS              84
#define TRAINER_ICHOR_KAPELOS                 85
// Hecate's Hollow, ids 100-109 (tools/ichor/maps/hecates_hollow.py)
#define TRAINER_ICHOR_HEKABE                  100
#define TRAINER_ICHOR_KALLIAS                 101
#define TRAINER_ICHOR_PHAINO                  102
#define TRAINER_ICHOR_BATTOS                  103
// Route 5, the Skironian cliffs, ids 110-129 (tools/ichor/maps/route5.py)
#define TRAINER_ICHOR_KYNEGEIROS              110
#define TRAINER_ICHOR_MELANTHIOS              111
#define TRAINER_ICHOR_MYRTO                   112
#define TRAINER_ICHOR_ARISTAIOS               113
#define TRAINER_ICHOR_MOPSOS                  114
#define TRAINER_ICHOR_DAPHNIS                 115
#define TRAINER_ICHOR_KERDON                  116
// Eleusa's story (ids 140-149): the Temple of Demeter, Eubouleus, the Mysteries' grunts
#define TRAINER_ICHOR_KALLIDIKE               140
#define TRAINER_ICHOR_EUMOLPOS                141
#define TRAINER_ICHOR_MELISSA                 142
#define TRAINER_ICHOR_CHLOE_1_DAY             143
#define TRAINER_ICHOR_CHLOE_1_NIGHT           144
#define TRAINER_ICHOR_GRUNT_TELESTERION_PSAMMIS 145
#define TRAINER_ICHOR_GRUNT_TELESTERION_CHERSOS 146
#define TRAINER_ICHOR_EUBOULEUS               147
// The Mystery sanctum under Eleusa (ids 150-159; tools/ichor/maps/sanctum.py, beat 23)
#define TRAINER_ICHOR_GRUNT_SANCTUM_KROKALOS  150
#define TRAINER_ICHOR_GRUNT_SANCTUM_BOLOS     151
#define TRAINER_ICHOR_GRUNT_SANCTUM_KONIS     152
#define TRAINER_ICHOR_GRUNT_SANCTUM_GAIOS     153
#define TRAINER_ICHOR_HYPERION_1              154
#define TRAINERS_END_ACT1                     155

// world-act2, ids 160-319, 820-849 and 1344-1403: Thyrsa, Arkadia, Astyra, Kaldera.
#define TRAINERS_END_ACT2                     0

// world-act3, ids 320-499 and 1404-1503: Kythera, Knossa, Lakonia, Delphoi, the Frozen Hour, Olympus.
#define TRAINERS_END_ACT3                     0

// The post-game, ids 500-679 and 1024-1223: the Labors, Katabasis, the Olympiad, the Odyssey, Atlantis.
#define TRAINERS_END_POSTGAME                 0

// The Oikoumene, ids 680-819, 864-1023 and 1224-1343: the second map.
#define TRAINERS_END_OIKOUMENE                0

// Ids 850-863 and 1504-1535 are the director's reserve.

#define ICHOR_TRAINERS_MAX(a, b) ((a) > (b) ? (a) : (b))
#define TRAINERS_COUNT_EMERALD ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(TRAINERS_END_SLICE, TRAINERS_END_FRONTIER), \
                                                                                        TRAINERS_END_SLICE2), \
                                                                     ICHOR_TRAINERS_MAX(TRAINERS_END_ACT1, TRAINERS_END_ACT2)), \
                                                  ICHOR_TRAINERS_MAX(ICHOR_TRAINERS_MAX(TRAINERS_END_ACT3, TRAINERS_END_POSTGAME), \
                                                                     TRAINERS_END_OIKOUMENE))

// Ichor: one trainer flag per id, from TRAINER_FLAGS_START (0x500): ids 1-1535. Raised
// from upstream's 864, to 1,024 for the Oikoumene's champion halls (design/OIKOUMENE.md
// PG-38) and then to 1,536 for Emerald's trainer density (design/MAP_DESIGN.md section 8).
// Raising it shifts every system flag and grows SaveBlock1.
#define MAX_TRAINERS_COUNT_EMERALD 1536

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

// Ichor: Phase 2 trainer names until their ids are registered (see the header).
#include "constants/ichor_trainer_stubs.h"

#endif  // GUARD_CONSTANTS_OPPONENTS_H
