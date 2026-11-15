#ifndef GUARD_ICHOR_FROZEN_H
#define GUARD_ICHOR_FROZEN_H

// Ichor: the Frozen Hour (design/phase4/SCRIPT.md Part 11, E1-E6). While
// FLAG_ICHOR_FROZEN_HOUR is set the field is gray, everyone but the player and
// the unfrozen stands still, there are no wild encounters and the music box
// plays. design/ENGINE_API.md §5 lists what map scripts call.

struct ObjectEvent;

bool32 Ichor_IsFrozenHour(void);
bool32 Ichor_SuspendsDayNight(void);                     // overworld.c, MapHasNaturalLight
void Ichor_TintBgPalettes(u32 offset, u32 count, bool32 alsoFaded); // fieldmap.c, tileset palettes
void Ichor_OnSpritePaletteLoaded(u32 slot);              // sprite.c
bool32 Ichor_IsHeldByFrozenHour(struct ObjectEvent *objectEvent); // trainer_see.c
bool32 Ichor_KeepsObjectFrozen(struct ObjectEvent *objectEvent);  // event_object_movement.c
void Ichor_FrozenHourFrame(void);                        // overworld.c, every field frame
void Ichor_FrozenHourOnMapTransition(void);

#endif // GUARD_ICHOR_FROZEN_H
