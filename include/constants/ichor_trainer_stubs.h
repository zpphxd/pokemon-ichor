#ifndef GUARD_CONSTANTS_ICHOR_TRAINER_STUBS_H
#define GUARD_CONSTANTS_ICHOR_TRAINER_STUBS_H

// ICHOR_STUB_TRAINER_IDS: Phase 2 trainer names, until this session's trainer
// id range lands with the Hoenn cut (tools/ichor/claim_ranges.md).
//
// Scripts use the final names. Until each is registered in opponents.h with
// its party in src/data/trainers.party (the parties are written in
// design/phase2/trainers_batch1.party), it is TRAINER_NONE here: the build
// works, but don't start these battles in tests. Registering one removes its
// line below. Batch 1's trainers are all registered; later batches add
// their stubs here while their classes or ids are pending.


#endif // GUARD_CONSTANTS_ICHOR_TRAINER_STUBS_H
