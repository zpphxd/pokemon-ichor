// Ichor: Galatea's marble statues (engine need E8, design/phase4/ENGINE_ACT3.md).
//
// A statue is an object with a MOVEMENT_TYPE_ICHOR_STATUE* movement type; a
// mirror is one with MOVEMENT_TYPE_ICHOR_MIRROR*, and its facing is its angle.
// Both hold still like FACE_* objects. On each step the player takes under
// their own control, every statue on screen that the player can't see steps
// one tile toward them (a rooted one only turns to face them), and a walking
// statue that ends up next to the player touches them: its own script runs.
#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "fieldmap.h"
#include "follower_npc.h"
#include "ichor_statue.h"
#include "script.h"
#include "sound.h"
#include "constants/event_object_movement.h"
#include "constants/event_objects.h"
#include "constants/songs.h"

extern const u8 gInitialMovementTypeFacingDirections[];

// A line of sight runs at most this many tiles and turns at this many mirrors.
#define SIGHT_MAX_TILES   32
#define SIGHT_MAX_MIRRORS 4

// The stone-grinding sound of a statue moving, once per step however many move.
#define SE_STATUE_STEP SE_M_STRENGTH

enum StatueKind
{
    STATUE_NONE,
    STATUE_WALKS,
    STATUE_ROOTED,
};

static enum StatueKind GetStatueKind(u32 movementType)
{
    if (movementType >= MOVEMENT_TYPE_ICHOR_STATUE && movementType <= MOVEMENT_TYPE_ICHOR_STATUE_RIGHT)
        return STATUE_WALKS;
    if (movementType >= MOVEMENT_TYPE_ICHOR_STATUE_ROOTED && movementType <= MOVEMENT_TYPE_ICHOR_STATUE_ROOTED_RIGHT)
        return STATUE_ROOTED;
    return STATUE_NONE;
}

bool32 Ichor_IsMirror(u32 movementType)
{
    return movementType >= MOVEMENT_TYPE_ICHOR_MIRROR && movementType <= MOVEMENT_TYPE_ICHOR_MIRROR_RIGHT;
}

// A mirror's face sends a line the way the mirror faces: back the way it came
// when the mirror faces it head-on (a wall mirror shows what's behind you), or
// round a corner when the line comes from the side. Its bronze back stops it.
enum Direction Ichor_MirrorTurn(enum Direction travel, enum Direction mirrorFacing)
{
    if (travel == mirrorFacing)
        return DIR_NONE;
    return mirrorFacing;
}

static bool32 IsPlayerOrFollower(u32 objectEventId)
{
    if (gObjectEvents[objectEventId].isPlayer || gObjectEvents[objectEventId].localId == OBJ_EVENT_ID_FOLLOWER)
        return TRUE;
    return PlayerHasFollowerNPC() && objectEventId == GetFollowerNPCObjectId();
}

bool32 Ichor_FieldObjectAt(s16 x, s16 y, struct IchorFieldObject *out)
{
    u32 i;
    u8 mapNum = gSaveBlock1Ptr->location.mapNum, mapGroup = gSaveBlock1Ptr->location.mapGroup;

    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *obj = &gObjectEvents[i];
        if (obj->active && obj->currentCoords.x == x && obj->currentCoords.y == y && !IsPlayerOrFollower(i))
        {
            out->objectEventId = i;
            out->localId = obj->localId;
            out->movementType = obj->movementType;
            out->facing = obj->facingDirection;
            return TRUE;
        }
    }

    // Off screen, an object stands where its template puts it. A beam or a
    // line of sight can reach further than the objects that have spawned.
    for (i = 0; i < gMapHeader.events->objectEventCount; i++)
    {
        const struct ObjectEventTemplate *template = &gSaveBlock1Ptr->objectEventTemplates[i];
        if (template->x + MAP_OFFSET != x || template->y + MAP_OFFSET != y || template->kind != OBJ_KIND_NORMAL)
            continue;
        if (FlagGet(template->flagId) || GetObjectEventIdByLocalIdAndMap(template->localId, mapNum, mapGroup) != OBJECT_EVENTS_COUNT)
            continue;
        out->objectEventId = OBJECT_EVENTS_COUNT;
        out->localId = template->localId;
        out->movementType = template->movementType;
        out->facing = gInitialMovementTypeFacingDirections[template->movementType];
        return TRUE;
    }
    return FALSE;
}

// The statues the player can see: every statue on the line of tiles straight
// ahead, which turns at each mirror's face and stops at a mirror's back, a wall
// (an impassable tile), anyone else, or the edge of the map. Statues don't
// block the line. One bit per object event.
static u32 GetWatchedStatues(void)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    s16 x = player->currentCoords.x;
    s16 y = player->currentCoords.y;
    enum Direction dir = player->facingDirection;
    u32 tiles, mirrors = 0, watched = 0;
    struct IchorFieldObject seen;

    for (tiles = 0; tiles < SIGHT_MAX_TILES; tiles++)
    {
        MoveCoords(dir, &x, &y);
        if (Ichor_FieldObjectAt(x, y, &seen))
        {
            if (GetStatueKind(seen.movementType) != STATUE_NONE)
            {
                if (seen.objectEventId < OBJECT_EVENTS_COUNT)
                    watched |= 1u << seen.objectEventId;
                continue;
            }
            if (!Ichor_IsMirror(seen.movementType) || ++mirrors > SIGHT_MAX_MIRRORS)
                break;
            dir = Ichor_MirrorTurn(dir, seen.facing);
            if (dir == DIR_NONE)
                break;
            continue;
        }
        if (MapGridGetCollisionAt(x, y))
            break;
    }
    return watched;
}

// The way from the statue toward the player along the longer axis (east or
// west on a tie), or along the other axis if `other`. DIR_NONE if it's level.
static enum Direction GetDirectionTowardPlayer(struct ObjectEvent *statue, bool32 other)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    s16 dx = player->currentCoords.x - statue->currentCoords.x;
    s16 dy = player->currentCoords.y - statue->currentCoords.y;
    bool32 across = (abs(dx) >= abs(dy)) != other;

    if (across)
        return dx > 0 ? DIR_EAST : (dx < 0 ? DIR_WEST : DIR_NONE);
    return dy > 0 ? DIR_SOUTH : (dy < 0 ? DIR_NORTH : DIR_NONE);
}

static bool32 IsNextToPlayer(struct ObjectEvent *statue)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    return abs(player->currentCoords.x - statue->currentCoords.x) + abs(player->currentCoords.y - statue->currentCoords.y) == 1;
}

// One tile toward the player, along the longer axis or else the shorter one.
// The usual collision rules apply, the template's movement range included,
// except that the tile someone has just stepped off doesn't block. The statue
// doesn't walk: it is simply one tile nearer.
static bool32 TryStepTowardPlayer(struct ObjectEvent *statue)
{
    u32 attempt;

    for (attempt = 0; attempt < 2; attempt++)
    {
        enum Direction dir = GetDirectionTowardPlayer(statue, attempt);
        s16 x = statue->currentCoords.x;
        s16 y = statue->currentCoords.y;
        enum Collision collision;

        if (dir == DIR_NONE)
            continue;
        MoveCoords(dir, &x, &y);
        collision = GetCollisionAtCoords(statue, x, y, dir);
        if (collision == COLLISION_NONE
         || (collision == COLLISION_OBJECT_EVENT && GetObjectEventIdByXY(x, y) == OBJECT_EVENTS_COUNT))
        {
            MoveObjectEventToMapCoords(statue, x, y);
            return TRUE;
        }
    }
    return FALSE;
}

static bool32 TryStartTouch(u32 objectEventId)
{
    const u8 *script = GetObjectEventScriptPointerByObjectEventId(objectEventId);

    if (script == NULL)
        return FALSE;
    gSpecialVar_LastTalked = gObjectEvents[objectEventId].localId;
    gSpecialVar_Facing = DIR_NONE; // a touch, not a talk
    gSelectedObjectEvent = objectEventId;
    ScriptContext_SetupScript(script);
    return TRUE;
}

bool32 Ichor_StatuesOnPlayerStep(void)
{
    u32 i, watched = 0;
    bool32 haveStatues = FALSE, moved = FALSE, touched = FALSE;

    for (i = 0; i < OBJECT_EVENTS_COUNT && !haveStatues; i++)
        haveStatues = gObjectEvents[i].active && GetStatueKind(gObjectEvents[i].movementType) != STATUE_NONE;
    if (!haveStatues)
        return FALSE;

    watched = GetWatchedStatues();
    for (i = 0; i < OBJECT_EVENTS_COUNT && !touched; i++)
    {
        struct ObjectEvent *statue = &gObjectEvents[i];
        enum StatueKind kind = GetStatueKind(statue->movementType);
        enum Direction toward;

        if (!statue->active || kind == STATUE_NONE || (watched & (1u << i)) || statue->heldMovementActive)
            continue;
        if (kind == STATUE_WALKS && !IsNextToPlayer(statue) && TryStepTowardPlayer(statue))
            moved = TRUE;
        toward = GetDirectionTowardPlayer(statue, FALSE);
        if (toward != DIR_NONE && toward != statue->facingDirection)
            ObjectEventTurn(statue, toward);
        if (kind == STATUE_WALKS && IsNextToPlayer(statue))
            touched = TryStartTouch(i);
    }
    if (moved)
        PlaySE(SE_STATUE_STEP);
    return touched;
}
