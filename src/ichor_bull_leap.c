// Ichor: the bull-leap timing special (engine need E7, LABYRINTH.md §3,
// design/phase4/ENGINE_ACT3.md). Generic: a moving object, a line and a
// window. Knossa's Gentle Bull and Asterion use it, and so does the Moment on
// the Stair of Hours.
//
//   setvar VAR_0x8004, LOCALID_BULL           @ the object that charges
//   setvar VAR_0x8005, ICHOR_TILE(10, 6)      @ the line's tile: x | (y << 8)
//   setvar VAR_0x8006, 10                     @ the window, in frames (0: 10)
//   setvar VAR_0x8007, 6                      @ frames per tile (0: 6)
//   special Ichor_BullLeap                    @ waits; VAR_RESULT: ICHOR_LEAP_*
//
// The object charges one tile at a time, by the longer way first, to the line's
// tile and stops there. The window opens on the frame its head starts across
// the line (its step onto the line's tile begins) and lasts VAR_0x8006 frames.
// A press of A before it opens is early, inside it clean; no press in it is
// late. Once the result is known the object finishes the tile it is crossing
// and the script goes on. Modeled on src/fishing.c's wait-for-A step.
#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "fieldmap.h"
#include "ichor_bull_leap.h"
#include "main.h"
#include "script.h"
#include "sprite.h"
#include "task.h"
#include "constants/ichor_act3.h"

#define tObjectEventId  data[0]
#define tLineX          data[1] // MAP_OFFSET coordinates
#define tLineY          data[2]
#define tWindow         data[3]
#define tFramesPerTile  data[4]
#define tDirection      data[5] // of the tile step under way, DIR_NONE between steps
#define tStepFrame      data[6] // frames into that step
#define tWindowFrame    data[7] // frames since the window opened, -1 before
#define tResult         data[8] // ICHOR_LEAP_*, or -1 while undecided
#define tFrame          data[9] // frames since the special started (for tests)
#define tWasFrozen      data[10]

#define RESULT_UNDECIDED -1

static void Ichor_BullLeapTask(u8 taskId);

void Ichor_BullLeap(void)
{
    u8 taskId = CreateTask(Ichor_BullLeapTask, 80);
    struct Task *task = &gTasks[taskId];
    u8 objectEventId = GetObjectEventIdByLocalIdAndMap(gSpecialVar_0x8004, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);

    task->tObjectEventId = objectEventId;
    task->tLineX = (gSpecialVar_0x8005 & 0xFF) + MAP_OFFSET;
    task->tLineY = (gSpecialVar_0x8005 >> 8) + MAP_OFFSET;
    task->tWindow = gSpecialVar_0x8006 ? gSpecialVar_0x8006 : ICHOR_LEAP_DEFAULT_WINDOW;
    task->tFramesPerTile = gSpecialVar_0x8007 ? gSpecialVar_0x8007 : ICHOR_LEAP_DEFAULT_FRAMES_PER_TILE;
    task->tDirection = DIR_NONE;
    task->tWindowFrame = -1;
    task->tResult = RESULT_UNDECIDED;
    if (objectEventId >= OBJECT_EVENTS_COUNT)
    {
        task->tResult = ICHOR_LEAP_LATE; // nothing to leap: ends on the first frame
        return;
    }
    // Held still as `lockall` leaves it, so its own movement type can't move
    // it, but with its walking animation playing.
    task->tWasFrozen = gObjectEvents[objectEventId].frozen;
    FreezeObjectEvent(&gObjectEvents[objectEventId]);
    gSprites[gObjectEvents[objectEventId].spriteId].animPaused = FALSE;
}

// The next tile toward the line, the longer way first; DIR_NONE on the line.
static enum Direction GetDirectionToLine(struct Task *task, struct ObjectEvent *obj)
{
    s16 dx = task->tLineX - obj->currentCoords.x;
    s16 dy = task->tLineY - obj->currentCoords.y;

    if (dx == 0 && dy == 0)
        return DIR_NONE;
    if (abs(dx) >= abs(dy))
        return dx > 0 ? DIR_EAST : DIR_WEST;
    return dy > 0 ? DIR_SOUTH : DIR_NORTH;
}

static void Ichor_BullLeapTask(u8 taskId)
{
    struct Task *task = &gTasks[taskId];
    struct ObjectEvent *obj;
    struct Sprite *sprite;
    s16 x, y, pixels;

    if (task->tObjectEventId >= OBJECT_EVENTS_COUNT)
    {
        gSpecialVar_Result = task->tResult;
        DestroyTask(taskId);
        ScriptContext_Enable();
        return;
    }
    obj = &gObjectEvents[task->tObjectEventId];
    sprite = &gSprites[obj->spriteId];

    // Between tiles: start the next step, unless the result is known or the
    // object stands on the line, where it waits for the window to close.
    if (task->tDirection == DIR_NONE && task->tResult == RESULT_UNDECIDED)
    {
        enum Direction dir = GetDirectionToLine(task, obj);
        if (dir == DIR_NONE)
        {
            if (task->tWindowFrame < 0)
                task->tWindowFrame = 0; // it started on the line
        }
        else
        {
            x = obj->currentCoords.x;
            y = obj->currentCoords.y;
            MoveCoords(dir, &x, &y);
            ShiftObjectEventCoords(obj, x, y);
            SetObjectEventDirection(obj, dir);
            StartSpriteAnimIfDifferent(sprite, GetMoveDirectionFastAnimNum(dir));
            task->tDirection = dir;
            task->tStepFrame = 0;
            if (x == task->tLineX && y == task->tLineY)
                task->tWindowFrame = 0; // its head starts across the line
        }
    }

    // The press, measured against the line.
    if (task->tResult == RESULT_UNDECIDED)
    {
        if (JOY_NEW(A_BUTTON))
            task->tResult = task->tWindowFrame < 0 ? ICHOR_LEAP_EARLY : ICHOR_LEAP_CLEAN;
        else if (task->tWindowFrame >= 0 && ++task->tWindowFrame > task->tWindow)
            task->tResult = ICHOR_LEAP_LATE;
    }

    // This frame's share of the step's 16 pixels.
    if (task->tDirection != DIR_NONE)
    {
        pixels = 16 * (task->tStepFrame + 1) / task->tFramesPerTile - 16 * task->tStepFrame / task->tFramesPerTile;
        switch (task->tDirection)
        {
        case DIR_EAST:  sprite->x += pixels; break;
        case DIR_WEST:  sprite->x -= pixels; break;
        case DIR_SOUTH: sprite->y += pixels; break;
        default:        sprite->y -= pixels; break;
        }
        if (++task->tStepFrame >= task->tFramesPerTile)
        {
            ShiftStillObjectEventCoords(obj);
            task->tDirection = DIR_NONE;
        }
    }

    task->tFrame++;
    if (task->tResult != RESULT_UNDECIDED && task->tDirection == DIR_NONE)
    {
        StartSpriteAnim(sprite, GetFaceDirectionAnimNum(obj->facingDirection));
        sprite->animPaused = TRUE;
        if (!task->tWasFrozen)
            UnfreezeObjectEvent(obj);
        gSpecialVar_Result = task->tResult;
        DestroyTask(taskId);
        ScriptContext_Enable();
    }
}
