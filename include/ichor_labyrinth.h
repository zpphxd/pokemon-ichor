#ifndef GUARD_ICHOR_LABYRINTH_H
#define GUARD_ICHOR_LABYRINTH_H

// Ichor: the Labyrinth's engine (design/LABYRINTH.md §5, §12): Ariadne's Thread
// on the floor, Asterion, the Helm of Darkness and Daedalus's dials. Each ring's
// ON_LOAD registers its floors, anchors and cracked walls; design/ENGINE_API.md
// §6 lists the calls.

struct ObjectEvent;

bool32 Ichor_IsThreadedMap(void);                          // the Thread's field use
u8 Ichor_GetTrainerSightRange(struct ObjectEvent *trainer); // trainer_see.c
void Ichor_LabyrinthFrame(void);
void Ichor_LabyrinthOnMapTransition(void);

#endif // GUARD_ICHOR_LABYRINTH_H
