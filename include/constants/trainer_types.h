#ifndef GUARD_CONSTANTS_TRAINER_TYPES_H
#define GUARD_CONSTANTS_TRAINER_TYPES_H

#define TRAINER_TYPE_NONE               0
#define TRAINER_TYPE_NORMAL             1
#define TRAINER_TYPE_SEE_ALL_DIRECTIONS 2
#define TRAINER_TYPE_BURIED             3
// Ichor: Titanborn in the Labyrinth (LABYRINTH §5.6). Both see in a line, as
// NORMAL does, and both take a disguised player for a recruit; a sentry also
// sees the lines either side of its own, from 2 tiles out.
#define TRAINER_TYPE_ICHOR_TITANBORN    4
#define TRAINER_TYPE_ICHOR_SENTRY       5
#define TRAINER_TYPE_OW_WILD_ENCOUNTER  0xFF

#endif  // GUARD_CONSTANTS_TRAINER_TYPES_H
