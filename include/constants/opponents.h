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
#define TRAINER_ICHOR_DAMON                 160
#define TRAINER_ICHOR_PHANO                 161
#define TRAINER_ICHOR_LYSIS                 162
#define TRAINER_ICHOR_MELANIPPE             163
#define TRAINER_ICHOR_SOSTRATOS             164
#define TRAINER_ICHOR_THEOGNIS              165
#define TRAINER_ICHOR_AKTAIOS               166
#define TRAINER_ICHOR_NYSA                  167
#define TRAINER_ICHOR_BROMIOS               168
#define TRAINER_ICHOR_CHARINOS              169
#define TRAINER_ICHOR_KLEITO                170
#define TRAINER_ICHOR_EUPHRON               171
#define TRAINER_ICHOR_HAGES                 172
#define TRAINER_ICHOR_MYRTON                173
#define TRAINER_ICHOR_DORIS                 174
#define TRAINER_ICHOR_PHILISKOS             175
#define TRAINER_ICHOR_EUXENOS               176
#define TRAINER_ICHOR_MANTO                 177
#define TRAINER_ICHOR_THYRSA_COMIC          178
#define TRAINER_ICHOR_THYRSA_TRAGIC         179
#define TRAINER_ICHOR_THYRSA_SATYR          180
#define TRAINER_ICHOR_THESPIS               181
#define TRAINER_ICHOR_SILENOS               182
#define TRAINER_ICHOR_R8_PANOS              183
#define TRAINER_ICHOR_R8_AMPELIS            184
#define TRAINER_ICHOR_R8_KEPHALOS           185
#define TRAINER_ICHOR_R8_MEDA               186
#define TRAINER_ICHOR_R8_MELAS              187
#define TRAINER_ICHOR_R8_THYONE             188
#define TRAINER_ICHOR_R9_POLYON             189
#define TRAINER_ICHOR_R9_MNASON             190
#define TRAINER_ICHOR_R9_AKESON             191
#define TRAINER_ICHOR_R9_ERYX               192
#define TRAINER_ICHOR_R9_PHILTA             193
#define TRAINER_ICHOR_R9_DEINON             194
#define TRAINER_ICHOR_R11_DORYS             195
#define TRAINER_ICHOR_R11_LACHON            196
#define TRAINER_ICHOR_R11_THRASEAS          197
#define TRAINER_ICHOR_R11_MYRINE            198
#define TRAINER_ICHOR_R11_PHERON            199
#define TRAINER_ICHOR_R11_XANTHE            200
#define TRAINER_ICHOR_R12_STHENON           201
#define TRAINER_ICHOR_R12_BRISEIS           202
#define TRAINER_ICHOR_R12_OPHION            203
#define TRAINER_ICHOR_R12_DAMO              204
#define TRAINER_ICHOR_R12_PHANES            205
#define TRAINER_ICHOR_R12_KALLIN            206
#define TRAINER_ICHOR_ARTEMIS_TEACH          207
#define TRAINER_ICHOR_ARTEMIS_TEST           208
#define TRAINER_ICHOR_ARTEMIS_MASTER         209
#define TRAINER_ICHOR_KALLISTO               210
#define TRAINER_ICHOR_R13_POLYDOROS         211
#define TRAINER_ICHOR_R13_ANTHE             212
#define TRAINER_ICHOR_R13_LYKON             213
#define TRAINER_ICHOR_R13_THEANO            214
#define TRAINER_ICHOR_R13_KALLIAS           215
#define TRAINER_ICHOR_R13_AGLAON            216
#define TRAINER_ICHOR_R14_ISON              217
#define TRAINER_ICHOR_R14_PHILOMELE         218
#define TRAINER_ICHOR_R14_NEOKLES           219
#define TRAINER_ICHOR_R14_ERATO             220
#define TRAINER_ICHOR_R14_DEMADES           221
#define TRAINER_ICHOR_R14_KLEARCHOS         222
#define TRAINER_ICHOR_R15_TIMON             223
#define TRAINER_ICHOR_R15_HEGESO            224
#define TRAINER_ICHOR_R15_POLEMON           225
#define TRAINER_ICHOR_R15_PHILA             226
#define TRAINER_ICHOR_R15_AGIS              227
#define TRAINER_ICHOR_R15_PRAXON            228
#define TRAINER_ICHOR_R16_NIKIAS            229
#define TRAINER_ICHOR_R16_TIMARETE          230
#define TRAINER_ICHOR_R16_KLEOBIS           231
#define TRAINER_ICHOR_R16_DIOTIMA           232
#define TRAINER_ICHOR_R16_ARISTON           233
#define TRAINER_ICHOR_R16_EUBIOS            234
#define TRAINER_ICHOR_AKROPOLIS_LITHOS       235
#define TRAINER_ICHOR_AKROPOLIS_KONIORTOS   236
#define TRAINER_ICHOR_AKROPOLIS_SIDEROS      237
#define TRAINER_ICHOR_AKROPOLIS_CHALKOS      238
#define TRAINER_ICHOR_KLEON_AKROPOLIS_KYNDER 239
#define TRAINER_ICHOR_KLEON_AKROPOLIS_HIPLING 240
#define TRAINER_ICHOR_KLEON_AKROPOLIS_NEBREL 241
#define TRAINER_ICHOR_RHEA_AKROPOLIS         242
#define TRAINER_ICHOR_SALT_WELL_GLAUKOS      243
#define TRAINER_ICHOR_SALT_WELL_KYMOTHOE     244
#define TRAINER_ICHOR_SALT_WELL_HALIA        245
#define TRAINER_ICHOR_PHEGEUS                 246
#define TRAINER_ICHOR_KORYTHOS                247
#define TRAINER_ICHOR_EUANDROS                248
#define TRAINER_ICHOR_AGAPENOR                249
#define TRAINER_ICHOR_EUADNE                  250
#define TRAINER_ICHOR_HEKAERGE                251
#define TRAINER_ICHOR_LYSIPPE                 252
#define TRAINER_ICHOR_MAINALOS                253
#define TRAINER_ICHOR_WOOD_MELANIPPE          254
#define TRAINER_ICHOR_KALDERA_SMITH_ONE      255
#define TRAINER_ICHOR_KALDERA_SMITH_TWO      256
#define TRAINER_ICHOR_KALDERA_SMITH_THREE    257
#define TRAINER_ICHOR_KALDERA_PETROS         258
#define TRAINER_ICHOR_KALDERA_AMATHOS        259
#define TRAINER_ICHOR_KALDERA_PHLOGIOS       260
#define TRAINER_ICHOR_KALDERA_TALOS          261
#define TRAINER_ICHOR_KALDERA_HYPERION       262
#define TRAINERS_END_ACT2                   263

// world-act3, ids 320-499 and 1404-1503: Kythera, Knossa, Lakonia, Delphoi, the Frozen Hour, Olympus.
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
#define TRAINER_ICHOR_LYKIDAS_KYTHERA         341
#define TRAINER_ICHOR_KERINTHOS               342
#define TRAINER_ICHOR_MOPSOS_KYTHERA                  343
#define TRAINER_ICHOR_THESTYLIS_KYTHERA       344
// Knossa above ground, ids 345-364 (claim_ranges.md): the Bull Road's nine (SCRIPT's
// Kerinthe, Euphemos and Phaistia, and six more for MAP_DESIGN.md §8's late-route
// density), the vineyard's two, the Bronze Heel's one and the North Entrance's two.
#define TRAINER_ICHOR_KERINTHE              345
#define TRAINER_ICHOR_BOUKOLION             346
#define TRAINER_ICHOR_EUPHEMOS              347
#define TRAINER_ICHOR_KYBISTE               348
#define TRAINER_ICHOR_KROKALE               349
#define TRAINER_ICHOR_TELEMOS               350
#define TRAINER_ICHOR_ELAIS                 351
#define TRAINER_ICHOR_THEORIS               352
#define TRAINER_ICHOR_PHAISTIA              353
#define TRAINER_ICHOR_IPHITOS               354
#define TRAINER_ICHOR_PROPOLIS              355
#define TRAINER_ICHOR_GLAUKE_KNOSSA         356
#define TRAINER_ICHOR_KERAMOS               357
#define TRAINER_ICHOR_GYPSOS                358
#define TRAINER_ICHOR_LYKON_KYTHERA                  490
#define TRAINER_ICHOR_THEANO                 491
#define TRAINER_ICHOR_KYMODOKE               492
#define TRAINER_ICHOR_MENALKAS_KYTHERA        493
#define TRAINER_ICHOR_AMARYLLIS              494
#define TRAINER_ICHOR_DAPHNIS_KYTHERA                495
#define TRAINER_ICHOR_OPORA                  496
#define TRAINER_ICHOR_PEGAIOS                497
#define TRAINER_ICHOR_DEXITHEA               498
// Labyrinth I (ids 365-389; tools/ichor/claim_ranges.md): Rings I-IV.
#define TRAINER_ICHOR_AKAKALLIS               365
#define TRAINER_ICHOR_XENODIKE                366
#define TRAINER_ICHOR_TEPHRA                  367
#define TRAINER_ICHOR_SINOPOS                 368
#define TRAINER_ICHOR_AUTOMATON_3             369
#define TRAINER_ICHOR_AUTOMATON_7             370
#define TRAINER_ICHOR_LITHOS                  371
#define TRAINER_ICHOR_KONIORTOS               372
#define TRAINER_ICHOR_SIDEROS                 373
#define TRAINER_ICHOR_CHALKOS                 374
#define TRAINER_ICHOR_PELOS                   375
#define TRAINER_ICHOR_ENKELADOS               376
#define TRAINERS_END_ACT3 499

// The League (world-act3's Olympus), ids 460-499, below Kythera's and Knossa's
// claims from 320 up (tools/ichor/claim_ranges.md): the Ascent, the Pantheon, the Archon.
#define TRAINER_ICHOR_ASCENT_PHILON          460
#define TRAINER_ICHOR_ASCENT_LAMPON          461
#define TRAINER_ICHOR_ASCENT_THEANO          462
#define TRAINER_ICHOR_ASCENT_KALLIAS         463
#define TRAINER_ICHOR_ASCENT_AGATHE          464
#define TRAINER_ICHOR_ASCENT_NIKIAS          465
#define TRAINER_ICHOR_ASCENT_EIRENE          466
#define TRAINER_ICHOR_ASCENT_DEXIOS          467
#define TRAINER_ICHOR_ASCENT_STHENELOS       468
#define TRAINER_ICHOR_ASCENT_GORGO           469
#define TRAINER_ICHOR_ASCENT_MELITE          470
#define TRAINER_ICHOR_BRASIDAS               471
#define TRAINER_ICHOR_THEMISTOKLES           472
#define TRAINER_ICHOR_HYPATIA                473
#define TRAINER_ICHOR_OLYMPIAS               474
#define TRAINER_ICHOR_ARISTEIDES             475
#define TRAINERS_END_LEAGUE                  476

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
                                                                     ICHOR_TRAINERS_MAX(TRAINERS_END_OIKOUMENE, TRAINERS_END_LEAGUE)))

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
