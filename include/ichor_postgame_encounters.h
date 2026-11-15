#ifndef GUARD_ICHOR_POSTGAME_ENCOUNTERS_H
#define GUARD_ICHOR_POSTGAME_ENCOUNTERS_H

#include "wild_encounter.h"

// Ichor postgame: wild encounter overlays (src/ichor_postgame_encounters.c). A row
// of the overlay table can replace the species a wild table just picked, at the
// table's level: the shades on the roads at night (POSTGAME §1), and in batch 8
// the Time Fractures.
u16 Ichor_OverlayWildSpecies(u16 species, enum WildPokemonArea area);

#endif // GUARD_ICHOR_POSTGAME_ENCOUNTERS_H
