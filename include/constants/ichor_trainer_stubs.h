#ifndef GUARD_CONSTANTS_ICHOR_TRAINER_STUBS_H
#define GUARD_CONSTANTS_ICHOR_TRAINER_STUBS_H

// ICHOR_STUB_TRAINER_IDS: Phase 2 trainer names, until this session's trainer
// id range lands with the Hoenn cut (tools/ichor/claim_ranges.md).
//
// Scripts use the final names. Until each is registered in opponents.h with
// its party in src/data/trainers.party (the parties are written in
// design/phase2/trainers_batch1.party), it is TRAINER_NONE here: the build
// works, but don't start these battles in tests. Registering one removes its
// line below.

#ifndef TRAINER_ICHOR_ALETHEA_DECK
#define TRAINER_ICHOR_ALETHEA_DECK TRAINER_NONE
#endif
#ifndef TRAINER_ICHOR_PHORMION
#define TRAINER_ICHOR_PHORMION     TRAINER_NONE
#endif
#ifndef TRAINER_ICHOR_LYKON
#define TRAINER_ICHOR_LYKON        TRAINER_NONE
#endif
#ifndef TRAINER_ICHOR_MYRMEX
#define TRAINER_ICHOR_MYRMEX       TRAINER_NONE
#endif
#ifndef TRAINER_ICHOR_SOSTRATOS
#define TRAINER_ICHOR_SOSTRATOS    TRAINER_NONE
#endif
#ifndef TRAINER_ICHOR_EUTHYMIA
#define TRAINER_ICHOR_EUTHYMIA     TRAINER_NONE
#endif

#endif // GUARD_CONSTANTS_ICHOR_TRAINER_STUBS_H
