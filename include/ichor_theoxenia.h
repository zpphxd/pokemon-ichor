#ifndef GUARD_ICHOR_THEOXENIA_H
#define GUARD_ICHOR_THEOXENIA_H

// Ichor: theoxenia's tells (design/SYSTEMS.md §10). An object whose trainer
// type is TRAINER_TYPE_ICHOR_GOD is a god in disguise: it casts no shadow, the
// follower bows when within 3 tiles of it, and the Augur's Eye says something
// is watching. design/ENGINE_API.md §7 has the details.

struct ObjectEvent;

bool32 Ichor_IsDisguisedGod(const struct ObjectEvent *objectEvent); // field_effect_helpers.c, shadows
bool32 Ichor_IsGodOnMap(void);                                     // dexnav.c
void Ichor_TheoxeniaFrame(void);                                   // every field frame

#endif // GUARD_ICHOR_THEOXENIA_H
