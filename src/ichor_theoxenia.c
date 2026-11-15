// Ichor: theoxenia's tells (design/SYSTEMS.md §10, design/ENGINE_API.md §7).
// Players learn to know a god in disguise: no shadow, the follower's bow, and
// the Augur's Eye's warning. A map marks the god's object with
// TRAINER_TYPE_ICHOR_GOD; the tests and the reveal are the map's scripts.

#include "global.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "ichor_theoxenia.h"
#include "constants/event_objects.h"
#include "constants/trainer_types.h"

#define BOW_RANGE   3   // tiles, from the follower
#define BOW_PERIOD  8   // frames between looks

// The god the follower last bowed to (its local id), until it's out of range
static EWRAM_DATA u8 sBowedAt = 0;
static EWRAM_DATA u8 sBowTimer = 0;

bool32 Ichor_IsDisguisedGod(const struct ObjectEvent *objectEvent)
{
    return objectEvent->active && objectEvent->trainerType == TRAINER_TYPE_ICHOR_GOD;
}

bool32 Ichor_IsGodOnMap(void)
{
    u32 i;
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        if (Ichor_IsDisguisedGod(&gObjectEvents[i]))
            return TRUE;
    }
    return FALSE;
}

static struct ObjectEvent *GodNear(s16 x, s16 y)
{
    u32 i;
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *god = &gObjectEvents[i];
        if (Ichor_IsDisguisedGod(god)
         && abs(god->currentCoords.x - x) + abs(god->currentCoords.y - y) <= BOW_RANGE)
            return god;
    }
    return NULL;
}

// The follower bows once to a god within 3 tiles of it: it turns to face them
// and dips, while the player stands still. It bows again only after leaving
// the god's range.
void Ichor_TheoxeniaFrame(void)
{
    struct ObjectEvent *follower, *god;
    u32 direction;

    if (++sBowTimer < BOW_PERIOD)
        return;
    sBowTimer = 0;
    follower = GetFollowerObject();
    if (follower == NULL || follower->invisible)
        return;
    god = GodNear(follower->currentCoords.x, follower->currentCoords.y);
    if (god == NULL)
    {
        sBowedAt = 0;
        return;
    }
    if (sBowedAt == god->localId || gPlayerAvatar.tileTransitionState != T_NOT_MOVING
     || (follower->heldMovementActive && !follower->heldMovementFinished))
        return;
    direction = GetDirectionToFace(follower->currentCoords.x, follower->currentCoords.y,
                                   god->currentCoords.x, god->currentCoords.y);
    ObjectEventClearHeldMovementIfFinished(follower);
    ObjectEventSetHeldMovement(follower, GetWalkInPlaceSlowMovementAction(direction));
    sBowedAt = god->localId;
}
