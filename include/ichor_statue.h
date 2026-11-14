#ifndef GUARD_ICHOR_STATUE_H
#define GUARD_ICHOR_STATUE_H

// Ichor: Galatea's marble statues and the bronze mirrors that watch them
// (engine need E8; design/phase4/ENGINE_ACT3.md). The beam trace (E9,
// src/ichor_beam.c) turns at the same mirrors.

// What stands on a tile, for a line of sight or a beam.
struct IchorFieldObject
{
    u8 objectEventId; // OBJECT_EVENTS_COUNT if it hasn't spawned (off screen)
    u8 localId;
    u8 movementType;
    u8 facing;
};

// Called on each step the player takes under their own control
// (ProcessPlayerFieldInput). TRUE if a statue's touch script has started.
bool32 Ichor_StatuesOnPlayerStep(void);

bool32 Ichor_IsMirror(u32 movementType);
// The way a line travelling `travel` leaves a mirror facing `mirrorFacing`:
// the way the mirror faces, or DIR_NONE when the line comes at its back.
enum Direction Ichor_MirrorTurn(enum Direction travel, enum Direction mirrorFacing);
// The object on map tile (x, y) (MAP_OFFSET coordinates) other than the player
// and followers: a live object, or else an object of the current map that is
// off screen, at its template's place and facing, unless its flag hides it.
bool32 Ichor_FieldObjectAt(s16 x, s16 y, struct IchorFieldObject *out);

#endif // GUARD_ICHOR_STATUE_H
