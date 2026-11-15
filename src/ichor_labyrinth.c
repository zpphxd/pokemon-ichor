// Ichor: the Labyrinth's engine (design/LABYRINTH.md §5, §12; ENGINE_API.md §6).
//
// - Ariadne's Thread: every step on a threaded map's floor lays thread, a step
//   back winds it up, and tying off at a bronze ring commits it. The thread is
//   saved in IchorSave.thread as segments of 2-bit steps, each starting at an
//   anchor; a segment never crosses maps.
// - Asterion: a field state machine on one object (patrol, listen, alert,
//   charge, stun, breakthrough, rest). He sees along his facing, as far as the
//   light on the player's tile allows, and hears steps.
// - The Helm of Darkness: trainers and Asterion can't see a helmed player in
//   the dark; the player's sprite turns translucent.
// - Daedalus's dials: one bit of a var turned with the Labrys.
// Each ring's ON_LOAD registers its floors, anchors and cracked walls; they are
// forgotten on the next map transition.
#include "global.h"
#include "difficulty.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_camera.h"
#include "field_effect.h"
#include "field_screen_effect.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "ichor_frozen.h"
#include "ichor_labyrinth.h"
#include "item.h"
#include "list_menu.h"
#include "malloc.h"
#include "overworld.h"
#include "region_map.h"
#include "script.h"
#include "script_menu.h"
#include "sprite.h"
#include "string_util.h"
#include "constants/event_object_movement.h"
#include "constants/field_effects.h"
#include "constants/ichor.h"
#include "constants/items.h"
#include "constants/metatile_behaviors.h"
#include "constants/rtc.h"
#include "constants/trainer_types.h"

#include "data/ichor_thread.h"

extern const u8 EventScript_IchorThreadLow[];
extern const u8 EventScript_IchorAsterionKnockdown[];
extern const u8 EventScript_IchorAsterionBrokeWall[];
extern const u8 EventScript_IchorRecruitBump[];

#define MAX_FLOORS        4
#define MAX_ANCHORS_HERE  8
#define MAX_WALLS         8
#define MAX_DRIFTS        8
#define DRIFT_STUCK_FRAMES 360  // LABORS Labor 4: stuck in the snow for 6 seconds
#define SPOOL_LOW         10
#define ANCHOR_TIED       0x100   // IchorThreadAnchor.reserved: a bronze ring, not just where a map began
#define ANCHOR_NAME(a)    ((a)->reserved & 0xFF)
#define NO_THREAD_ANCHOR         0xFF
#define MAX_COMMITTED     (ICHOR_THREAD_COMMITTED_BYTES * 4)
#define LIVE_CLOSED       0xFFFF  // IchorThread.liveMapId once the last segment is committed

// The ten twins of a threadable floor metatile, in this order in the tileset,
// starting at the twin id the ring's ON_LOAD gives.
enum
{
    SHAPE_H, SHAPE_V,
    SHAPE_NE, SHAPE_NW, SHAPE_SE, SHAPE_SW,              // corners, by the two sides they join
    SHAPE_CAP_N, SHAPE_CAP_S, SHAPE_CAP_W, SHAPE_CAP_E,  // ends, by the one side they join
    SHAPE_COUNT
};

// A step's 2-bit code is its direction - 1 (south, north, west, east).
enum { CONN_N = 1, CONN_S = 2, CONN_W = 4, CONN_E = 8 };
static const u8 sCodeConn[4] = { CONN_S, CONN_N, CONN_W, CONN_E };
static const u8 sOppositeCode[4] = { 1, 0, 3, 2 };
static const s8 sCodeDx[4] = { 0, 0, -1, 1 };
static const s8 sCodeDy[4] = { 1, -1, 0, 0 };

struct ThreadFloor { u16 floor; u16 firstTwin; };
struct AnchorHere { u8 x, y; u8 nameId; };
struct CrackedWall { u8 x, y; u16 flag; u16 broken; bool8 done; };
struct Drift { u8 x, y; u16 flag; };

enum
{
    AST_OFF,
    AST_PATROL,
    AST_LISTEN,
    AST_ALERT,
    AST_CHARGE,
    AST_STUNNED,
    AST_RETURN,   // walking back to where the charge began
    AST_REST,
    AST_DOWN,     // the player was knocked down: nothing more on this map
};

static EWRAM_DATA struct
{
    struct ThreadFloor floors[MAX_FLOORS];
    struct AnchorHere anchors[MAX_ANCHORS_HERE];
    struct CrackedWall walls[MAX_WALLS];
    struct Drift drifts[MAX_DRIFTS];
    u8 floorCount, anchorCount, wallCount, driftCount;
    bool8 segmentStarted;  // this map's segment has begun
    bool8 warnedLow;
    bool8 seenPlayer;      // lastX/lastY are valid
    bool8 helmBlend;       // the player's sprite was made translucent here
    s16 lastX, lastY;      // the player's tile last frame (grid coordinates)
    s16 entryX, entryY;    // where the player entered (a knockdown with no anchor)
    // Asterion
    u8 asterionLocalId;
    u8 aState;
    u16 aTimer;
    u8 aDir;               // the charge's direction
    u8 aCharged;           // tiles charged, to walk back
    u8 aRestSteps;
    u8 aOptions;           // ICHOR_CHARGER_* bits
    u16 aStunAfterStep;    // frames of stun once the step into a broken wall or a drift ends
    u8 aPatrolFacing;      // the way he faced when he left his patrol
    bool8 aPendingFace;
    u8 recruitBumped;      // the Titanborn object that last said "Watch it, recruit." + 1
} sLab = {0};

#define sThread (gIchorSave.thread)

// --- Difficulty -------------------------------------------------------------------------------

static s32 DifficultyStep(void)
{
    switch (GetCurrentDifficultyLevel())
    {
    case DIFFICULTY_EASY: return -1;  // Mortal
    case DIFFICULTY_HARD: return 1;   // Spartan
    default:              return 0;   // Hero
    }
}

static u32 GetSpoolLength(void)
{
    return Ichor_GetStepGlassLimit();
}

// --- Light (§5.3) -------------------------------------------------------------------------

enum { LIGHT_DARK, LIGHT_MOON, LIGHT_SUN, LIGHT_FULL };

static void GetPlayerTile(s16 *x, s16 *y)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    *x = player->currentCoords.x;
    *y = player->currentCoords.y;
}

static u32 GetPlayerLight(void)
{
    s16 x, y;
    if (!gMapHeader.cave || gSaveBlock1Ptr->flashLevel == 0)  // a lit map, or a lit zone in a dark one
        return LIGHT_FULL;
    GetPlayerTile(&x, &y);
    if (MapGridGetMetatileBehaviorAt(x, y) == MB_ICHOR_LIGHT_POOL)
        return gTimeOfDay == TIME_NIGHT ? LIGHT_MOON : LIGHT_SUN;
    return LIGHT_DARK;
}

static bool32 IsHelmed(void)
{
    return FlagGet(FLAG_ICHOR_HELM_ON);
}

static bool32 IsTitanborn(struct ObjectEvent *obj)
{
    return obj->trainerType == TRAINER_TYPE_ICHOR_TITANBORN || obj->trainerType == TRAINER_TYPE_ICHOR_SENTRY;
}

static bool32 IsRunning(void)
{
    return (gPlayerAvatar.flags & PLAYER_AVATAR_FLAG_DASH) != 0;
}

// trainer_see.c: a trainer's sight. Frozen in the Frozen Hour, none. Titanborn
// take a disguised player for a recruit unless they run within 3 tiles
// (LABYRINTH §5.6). Against the Helm, none in the dark and 2 tiles in light.
u8 Ichor_GetTrainerSightRange(struct ObjectEvent *trainer)
{
    u32 range = trainer->trainerRange_berryTreeId;

    if (Ichor_IsHeldByFrozenHour(trainer))
        return 0;
    if (FlagGet(FLAG_ICHOR_DISGUISE_ON) && IsTitanborn(trainer))
        range = IsRunning() ? min(range, 3) : 0;
    if (range != 0 && IsHelmed())
        return GetPlayerLight() == LIGHT_DARK ? 0 : min(range, 2);
    return range;
}

// trainer_see.c: a sentry (TRAINER_TYPE_ICHOR_SENTRY) also sees the lines either
// side of its own, from 2 tiles out to its range, over open floor. Seen there,
// the player is called to from the sentry's post: the approach is 1, no steps.
u8 Ichor_GetSentrySideSight(struct ObjectEvent *sentry, u8 range, s16 px, s16 py)
{
    u32 code = sentry->facingDirection - 1;
    s32 dx = px - sentry->currentCoords.x, dy = py - sentry->currentCoords.y;
    s32 forward = dx * sCodeDx[code] + dy * sCodeDy[code];
    s32 side = sCodeDx[code] != 0 ? dy : dx;
    s32 d;

    if (abs(side) != 1 || forward < 2 || forward > range)
        return 0;
    for (d = 1; d < forward; d++)
    {
        s32 x = sentry->currentCoords.x + sCodeDx[code] * d + (sCodeDx[code] != 0 ? 0 : side);
        s32 y = sentry->currentCoords.y + sCodeDy[code] * d + (sCodeDy[code] != 0 ? 0 : side);
        if (MapGridGetCollisionAt(x, y))
            return 0;
    }
    return 1;
}

// field_player_avatar.c: a disguised player walking into a Titanborn gets
// "Watch it, recruit." Once per bump: the player has to step away first.
void Ichor_OnPlayerBump(u32 collision, u32 direction)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    s16 x = player->currentCoords.x, y = player->currentCoords.y;
    u8 id;

    if (collision != COLLISION_OBJECT_EVENT || !FlagGet(FLAG_ICHOR_DISGUISE_ON) || direction < DIR_SOUTH || direction > DIR_EAST)
        return;
    x += sCodeDx[direction - 1];
    y += sCodeDy[direction - 1];
    id = GetObjectEventIdByPosition(x, y, player->currentElevation);
    if (id >= OBJECT_EVENTS_COUNT || !IsTitanborn(&gObjectEvents[id]) || id + 1 == sLab.recruitBumped)
        return;
    sLab.recruitBumped = id + 1;
    ScriptContext_SetupScript(EventScript_IchorRecruitBump);
}

// --- Registration (each ring's ON_LOAD) ------------------------------------------------------

// special Ichor_AddThreadFloor: metatile VAR_0x8004 takes thread; its ten twins
// start at metatile VAR_0x8005, in the order of the SHAPE_* list above.
void Ichor_AddThreadFloor(void)
{
    if (sLab.floorCount < MAX_FLOORS)
    {
        sLab.floors[sLab.floorCount].floor = gSpecialVar_0x8004;
        sLab.floors[sLab.floorCount].firstTwin = gSpecialVar_0x8005;
        sLab.floorCount++;
    }
}

// special Ichor_AddThreadAnchor: a bronze ring at (VAR_0x8004, VAR_0x8005),
// named VAR_0x8006 (a THREAD_ANCHOR_* id) in the RETURN TO… list.
void Ichor_AddThreadAnchor(void)
{
    if (sLab.anchorCount < MAX_ANCHORS_HERE)
    {
        sLab.anchors[sLab.anchorCount].x = gSpecialVar_0x8004;
        sLab.anchors[sLab.anchorCount].y = gSpecialVar_0x8005;
        sLab.anchors[sLab.anchorCount].nameId = gSpecialVar_0x8006;
        sLab.anchorCount++;
    }
}

// special Ichor_AddCrackedWall: Asterion's charge breaks the wall at
// (VAR_0x8004, VAR_0x8005) into metatile VAR_0x8007 and sets flag VAR_0x8006
// (0 for none). The ring's ON_LOAD draws walls whose flag is set as broken.
void Ichor_AddCrackedWall(void)
{
    if (sLab.wallCount < MAX_WALLS)
    {
        struct CrackedWall *wall = &sLab.walls[sLab.wallCount++];
        wall->x = gSpecialVar_0x8004;
        wall->y = gSpecialVar_0x8005;
        wall->flag = gSpecialVar_0x8006;
        wall->broken = gSpecialVar_0x8007;
        wall->done = FALSE;
    }
}

// special Ichor_StartAsterion: object VAR_0x8004 (a local id on this map) is
// Asterion, or another charger with ICHOR_CHARGER_* options in VAR_0x8005.
void Ichor_StartAsterion(void)
{
    sLab.asterionLocalId = gSpecialVar_0x8004;
    sLab.aOptions = gSpecialVar_0x8005;
    sLab.aState = AST_PATROL;
    sLab.aPendingFace = FALSE;
}

// special Ichor_AddDrift: a snow drift at (VAR_0x8004, VAR_0x8005). A charge
// that runs into it stops there, stuck for 6 seconds, and sets flag VAR_0x8006
// (0 for none), so the map can count which drifts caught him.
void Ichor_AddDrift(void)
{
    if (sLab.driftCount < MAX_DRIFTS)
    {
        sLab.drifts[sLab.driftCount].x = gSpecialVar_0x8004;
        sLab.drifts[sLab.driftCount].y = gSpecialVar_0x8005;
        sLab.drifts[sLab.driftCount].flag = gSpecialVar_0x8006;
        sLab.driftCount++;
    }
}

bool32 Ichor_IsThreadedMap(void)
{
    return sLab.floorCount != 0;
}

void Ichor_LabyrinthOnMapTransition(void);

// --- The thread's data --------------------------------------------------------------------------

static u16 CurrentMapId(void)
{
    return (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
}

static u32 GetStep(const u8 *bits, u32 i)
{
    return (bits[i >> 2] >> ((i & 3) * 2)) & 3;
}

static void SetStep(u8 *bits, u32 i, u32 code)
{
    u32 shift = (i & 3) * 2;
    bits[i >> 2] = (bits[i >> 2] & ~(3 << shift)) | (code << shift);
}

// The last anchor's segment is the live one until it is committed.
static bool32 HasLiveSegment(void)
{
    return sThread.anchorCount != 0 && sThread.liveMapId != LIVE_CLOSED;
}

// Steps committed by every segment before anchor `n`.
static u32 CommittedBefore(u32 n)
{
    u32 i, total = 0;
    for (i = 0; i < n; i++)
        total += sThread.anchors[i].steps;
    return total;
}

static u32 CommittedTotal(void)
{
    return CommittedBefore(HasLiveSegment() ? sThread.anchorCount - 1 : sThread.anchorCount);
}

static void DropOldestAnchor(void)
{
    u32 i, drop = sThread.anchors[0].steps;
    u32 total = CommittedTotal();

    for (i = 0; i + drop < total; i++)
        SetStep(sThread.committed, i, GetStep(sThread.committed, i + drop));
    for (i = 1; i < sThread.anchorCount; i++)
        sThread.anchors[i - 1] = sThread.anchors[i];
    sThread.anchorCount--;
    if (sThread.currentAnchor != NO_THREAD_ANCHOR)
        sThread.currentAnchor = sThread.currentAnchor == 0 ? NO_THREAD_ANCHOR : sThread.currentAnchor - 1;
}

// The live segment becomes committed thread.
static void CommitLive(void)
{
    u32 i, offset;

    if (!HasLiveSegment())
        return;
    while (sThread.anchorCount > 1 && CommittedBefore(sThread.anchorCount - 1) + sThread.liveLen > MAX_COMMITTED)
        DropOldestAnchor();  // the outer rings' marks go first (LABYRINTH §5.1)
    offset = CommittedBefore(sThread.anchorCount - 1);
    for (i = 0; i < sThread.liveLen && offset + i < MAX_COMMITTED; i++)
        SetStep(sThread.committed, offset + i, GetStep(sThread.live, i));
    sThread.anchors[sThread.anchorCount - 1].steps = i;
    sThread.liveLen = 0;
    sThread.liveMapId = LIVE_CLOSED;
}

// A new live segment starting at map coordinates (x, y) on this map.
static void StartSegment(u32 x, u32 y, bool32 tied, u32 nameId)
{
    struct IchorThreadAnchor *anchor;

    CommitLive();
    if (sThread.anchorCount == ICHOR_THREAD_ANCHORS)
        DropOldestAnchor();
    anchor = &sThread.anchors[sThread.anchorCount++];
    anchor->mapId = CurrentMapId();
    anchor->x = x;
    anchor->y = y;
    anchor->steps = 0;
    anchor->reserved = nameId | (tied ? ANCHOR_TIED : 0);
    sThread.liveMapId = anchor->mapId;
    sThread.liveX = x;
    sThread.liveY = y;
    sThread.liveLen = 0;
    if (tied)
        sThread.currentAnchor = sThread.anchorCount - 1;
    sLab.warnedLow = FALSE;
}

// --- Drawing ---------------------------------------------------------------------------------

static s32 FindFloor(u32 metatileId)
{
    u32 i;
    for (i = 0; i < sLab.floorCount; i++)
    {
        if (metatileId == sLab.floors[i].floor
         || (metatileId >= sLab.floors[i].firstTwin && metatileId < sLab.floors[i].firstTwin + SHAPE_COUNT))
            return i;
    }
    return -1;
}

static s32 ShapeOf(u32 conn)
{
    switch (conn)
    {
    case CONN_W | CONN_E: return SHAPE_H;
    case CONN_N | CONN_S: return SHAPE_V;
    case CONN_N | CONN_E: return SHAPE_NE;
    case CONN_N | CONN_W: return SHAPE_NW;
    case CONN_S | CONN_E: return SHAPE_SE;
    case CONN_S | CONN_W: return SHAPE_SW;
    case CONN_N:          return SHAPE_CAP_N;
    case CONN_S:          return SHAPE_CAP_S;
    case CONN_W:          return SHAPE_CAP_W;
    case CONN_E:          return SHAPE_CAP_E;
    default:              return -1;  // a lone tile: plain floor
    }
}

static const struct AnchorHere *FindAnchorAt(s32 mapX, s32 mapY);

// Draws thread joining sides `conn` on grid tile (x, y). Thread is only ever
// laid on floor and bronze rings, so anything else on its path now is a wall
// the Turning or a dial put there: the thread keeps it open as the first floor
// (LABYRINTH §5.1, "committed thread tiles never become walls").
static void DrawThreadTile(s32 x, s32 y, u32 conn, bool32 toScreen)
{
    s32 floor = FindFloor(MapGridGetMetatileIdAt(x, y));
    s32 shape = ShapeOf(conn);

    if (floor < 0)
    {
        if (conn == 0 || FindAnchorAt(x - MAP_OFFSET, y - MAP_OFFSET))
            return;  // bare, or a bronze ring: it stays in view
        floor = 0;
    }
    MapGridSetMetatileIdAt(x, y, shape < 0 ? sLab.floors[floor].floor : sLab.floors[floor].firstTwin + shape);
    if (toScreen)
        CurrentMapDrawMetatileAt(x, y);
}

// Walks one segment from its start, calling `visit` on each tile with the sides it joins.
typedef void (*ThreadVisit)(s32 x, s32 y, u32 conn, void *arg);
static void WalkSegment(const u8 *bits, u32 offset, u32 len, s32 x, s32 y, ThreadVisit visit, void *arg)
{
    u32 i, prevConn = 0;
    if (len == 0)
        return;  // no thread yet: the start tile keeps whatever is drawn there
    for (i = 0; i <= len; i++)
    {
        u32 conn = prevConn;
        u32 code = 0;
        if (i < len)
        {
            code = GetStep(bits, offset + i);
            conn |= sCodeConn[code];
        }
        visit(x, y, conn, arg);
        if (i < len)
        {
            x += sCodeDx[code];
            y += sCodeDy[code];
            prevConn = sCodeConn[sOppositeCode[code]];
        }
    }
}

// Every segment on this map, oldest first, then the live one.
static void WalkThreadHere(ThreadVisit visit, void *arg)
{
    u32 i, offset = 0;
    u16 mapId = CurrentMapId();

    for (i = 0; i < sThread.anchorCount; i++)
    {
        struct IchorThreadAnchor *anchor = &sThread.anchors[i];
        bool32 live = HasLiveSegment() && (i == sThread.anchorCount - 1);
        if (anchor->mapId == mapId)
        {
            if (live)
                WalkSegment(sThread.live, 0, sThread.liveLen, anchor->x + MAP_OFFSET, anchor->y + MAP_OFFSET, visit, arg);
            else
                WalkSegment(sThread.committed, offset, anchor->steps, anchor->x + MAP_OFFSET, anchor->y + MAP_OFFSET, visit, arg);
        }
        if (!live)
            offset += anchor->steps;
    }
}

static void VisitDraw(s32 x, s32 y, u32 conn, void *arg)
{
    DrawThreadTile(x, y, conn, *(bool8 *)arg);
}

struct TileQuery { s32 x, y; u32 conn; bool8 found; };
static void VisitFind(s32 x, s32 y, u32 conn, void *arg)
{
    struct TileQuery *q = arg;
    if (x == q->x && y == q->y)
    {
        q->conn = conn;  // the newest visit wins
        q->found = TRUE;
    }
}

// Redraws one tile from the thread now saved: the newest thread over it, or bare floor.
static void RedrawTile(s32 x, s32 y)
{
    struct TileQuery q = { .x = x, .y = y, .conn = 0, .found = FALSE };
    WalkThreadHere(VisitFind, &q);
    DrawThreadTile(x, y, q.found ? q.conn : 0, TRUE);
}

// special Ichor_DrawThread: draws this map's thread, at the end of the ring's ON_LOAD.
void Ichor_DrawThread(void)
{
    bool8 toScreen = FALSE;
    WalkThreadHere(VisitDraw, &toScreen);
}

// --- Laying and winding ----------------------------------------------------------------------

static const struct AnchorHere *FindAnchorAt(s32 mapX, s32 mapY)
{
    u32 i;
    for (i = 0; i < sLab.anchorCount; i++)
    {
        if (sLab.anchors[i].x == mapX && sLab.anchors[i].y == mapY)
            return &sLab.anchors[i];
    }
    return NULL;
}

static bool32 HasThread(void)
{
    return CheckBagHasItem(ITEM_ARIADNES_THREAD, 1);
}

static bool32 IsLiveHere(void)
{
    return HasLiveSegment() && sThread.liveMapId == CurrentMapId();
}

// The live segment's last tile and the one before it (grid coordinates).
static void GetLiveHead(s32 *x, s32 *y, s32 *prevX, s32 *prevY)
{
    u32 i;
    *x = sThread.liveX + MAP_OFFSET;
    *y = sThread.liveY + MAP_OFFSET;
    *prevX = *prevY = -1;
    for (i = 0; i < sThread.liveLen; i++)
    {
        u32 code = GetStep(sThread.live, i);
        *prevX = *x;
        *prevY = *y;
        *x += sCodeDx[code];
        *y += sCodeDy[code];
    }
}

static void OnThreadStep(s32 fromX, s32 fromY, s32 toX, s32 toY)
{
    s32 headX, headY, prevX, prevY;
    u32 code;

    if (!IsLiveHere())
        return;
    GetLiveHead(&headX, &headY, &prevX, &prevY);
    if (fromX != headX || fromY != headY)
        return;  // the player wasn't at the thread's end

    if (toX == prevX && toY == prevY)
    {
        // Back along the thread: it winds up (one tile of spool back)
        sThread.liveLen--;
        RedrawTile(headX, headY);
        RedrawTile(prevX, prevY);
        return;
    }

    if (abs(toX - fromX) + abs(toY - fromY) != 1 || sThread.liveLen >= GetSpoolLength())
        return;
    if (FindFloor(MapGridGetMetatileIdAt(toX, toY)) < 0 && !FindAnchorAt(toX - MAP_OFFSET, toY - MAP_OFFSET))
        return;  // stairs and doorways take no thread

    if (toY > fromY)      code = DIR_SOUTH - 1;
    else if (toY < fromY) code = DIR_NORTH - 1;
    else if (toX < fromX) code = DIR_WEST - 1;
    else                  code = DIR_EAST - 1;
    SetStep(sThread.live, sThread.liveLen++, code);
    RedrawTile(fromX, fromY);
    RedrawTile(toX, toY);

    if (!sLab.warnedLow && GetSpoolLength() - sThread.liveLen == SPOOL_LOW)
    {
        sLab.warnedLow = TRUE;
        ScriptContext_SetupScript(EventScript_IchorThreadLow);
    }
}

// The first frame on a threaded map: this map's segment starts where the
// player stands, tied if that's a bronze ring (each ring's entrance ties itself).
static void StartMapSegment(s16 x, s16 y)
{
    const struct AnchorHere *anchor = FindAnchorAt(x - MAP_OFFSET, y - MAP_OFFSET);
    sLab.segmentStarted = TRUE;
    StartSegment(x - MAP_OFFSET, y - MAP_OFFSET, anchor != NULL, anchor ? anchor->nameId : THREAD_ANCHOR_UNNAMED);
}

// Restores the live segment's tiles and empties it.
static void WindIn(void)
{
    s32 x, y;
    u32 i, len = sThread.liveLen;

    if (!IsLiveHere())
    {
        sThread.liveLen = 0;
        return;
    }
    x = sThread.liveX + MAP_OFFSET;
    y = sThread.liveY + MAP_OFFSET;
    sThread.liveLen = 0;
    RedrawTile(x, y);
    for (i = 0; i < len; i++)
    {
        u32 code = GetStep(sThread.live, i);
        x += sCodeDx[code];
        y += sCodeDy[code];
        RedrawTile(x, y);
    }
}

// --- The Thread's menu (Relic Ring → THREAD) ------------------------------------------------------

enum { THREAD_MENU_TIE_OFF, THREAD_MENU_RETURN, THREAD_MENU_WIND_IN, THREAD_MENU_LEAVE };

static void PushChoice(const u8 *text, u16 id)
{
    struct ListMenuItem item;
    u8 *name = Alloc(32);  // freed by the menu
    StringCopy(name, text);
    item.name = name;
    item.id = id;
    MultichoiceDynamic_PushElement(item);
}

static bool32 CanTieOffHere(void)
{
    s16 x, y;
    GetPlayerTile(&x, &y);
    return Ichor_IsThreadedMap() && FindAnchorAt(x - MAP_OFFSET, y - MAP_OFFSET) != NULL;
}

// special Ichor_BuildThreadMenu: TIE OFF (on a bronze ring), RETURN TO…, WIND IN, LEAVE.
void Ichor_BuildThreadMenu(void)
{
    if (CanTieOffHere())
        PushChoice(COMPOUND_STRING("TIE OFF"), THREAD_MENU_TIE_OFF);
    PushChoice(COMPOUND_STRING("RETURN TO…"), THREAD_MENU_RETURN);
    PushChoice(COMPOUND_STRING("WIND IN"), THREAD_MENU_WIND_IN);
    PushChoice(COMPOUND_STRING("LEAVE"), THREAD_MENU_LEAVE);
}

// special Ichor_ThreadTieOff: commits the thread at this bronze ring, refills
// the spool and makes the ring the one a knockdown returns to.
void Ichor_ThreadTieOff(void)
{
    s16 x, y;
    const struct AnchorHere *anchor;

    GetPlayerTile(&x, &y);
    anchor = FindAnchorAt(x - MAP_OFFSET, y - MAP_OFFSET);
    gSpecialVar_Result = FALSE;
    if (anchor == NULL)
        return;
    StartSegment(anchor->x, anchor->y, TRUE, anchor->nameId);
    gSpecialVar_Result = TRUE;
}

// special Ichor_ThreadWindIn: the live segment winds up at once.
void Ichor_ThreadWindIn(void)
{
    WindIn();
}

static bool32 IsListedBefore(u32 n)
{
    u32 i;
    for (i = sThread.anchorCount - 1; i > n; i--)
    {
        if ((sThread.anchors[i].reserved & ANCHOR_TIED)
         && sThread.anchors[i].mapId == sThread.anchors[n].mapId
         && sThread.anchors[i].x == sThread.anchors[n].x
         && sThread.anchors[i].y == sThread.anchors[n].y)
            return TRUE;
    }
    return FALSE;
}

// special Ichor_BuildThreadReturnMenu: every bronze ring tied off, newest first.
// VAR_RESULT is how many.
void Ichor_BuildThreadReturnMenu(void)
{
    s32 i;
    u32 count = 0;

    for (i = sThread.anchorCount - 1; i >= 0; i--)
    {
        struct IchorThreadAnchor *anchor = &sThread.anchors[i];
        u8 name[32];
        if (!(anchor->reserved & ANCHOR_TIED) || IsListedBefore(i))
            continue;
        if (ANCHOR_NAME(anchor) < ARRAY_COUNT(sThreadAnchorNames) && sThreadAnchorNames[ANCHOR_NAME(anchor)] != NULL)
            StringCopy(name, sThreadAnchorNames[ANCHOR_NAME(anchor)]);
        else
            GetMapName(name, Overworld_GetMapHeaderByGroupAndId(anchor->mapId >> 8, anchor->mapId & 0xFF)->regionMapSectionId, 0);
        PushChoice(name, i);
        count++;
    }
    gSpecialVar_Result = count;
}

static void WarpToAnchorPos(u16 mapId, u32 x, u32 y)
{
    SetWarpDestination(mapId >> 8, mapId & 0xFF, WARP_ID_NONE, x, y);
    DoWarp();
    ResetInitialPlayerAvatarState();
}

// special Ichor_ThreadReturnTo: the live thread winds in and the player follows
// the thread back to anchor VAR_0x8004 (from the list). VAR_RESULT is TRUE when
// the warp has begun: then the script must waitstate.
void Ichor_ThreadReturnTo(void)
{
    struct IchorThreadAnchor anchor;

    gSpecialVar_Result = FALSE;
    if (gSpecialVar_0x8004 >= sThread.anchorCount || FlagGet(FLAG_ICHOR_THREAD_NO_RETURN))
        return;
    anchor = sThread.anchors[gSpecialVar_0x8004];
    WindIn();
    WarpToAnchorPos(anchor.mapId, anchor.x, anchor.y);
    gSpecialVar_Result = TRUE;
}

// --- Asterion (§5.3) ----------------------------------------------------------------------------

static struct ObjectEvent *GetAsterion(void)
{
    u8 id;
    if (sLab.aState == AST_OFF)
        return NULL;
    id = GetObjectEventIdByLocalIdAndMap(sLab.asterionLocalId, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);
    return id < OBJECT_EVENTS_COUNT ? &gObjectEvents[id] : NULL;
}

static s32 Clamp0(s32 n) { return n < 0 ? 0 : n; }

static u32 GetAsterionSight(void)
{
    static const u8 sSight[] = { [LIGHT_DARK] = 3, [LIGHT_MOON] = 5, [LIGHT_SUN] = 7, [LIGHT_FULL] = 7 };
    u32 light = GetPlayerLight();

    if (IsHelmed())
        return light == LIGHT_DARK ? 0 : Clamp0(2 + DifficultyStep());
    return Clamp0(sSight[light] + DifficultyStep());
}

static u32 GetAsterionHearing(void)
{
    bool32 running = (gPlayerAvatar.flags & PLAYER_AVATAR_FLAG_DASH) != 0;
    if (IsHelmed())
        return running ? Clamp0(3 + DifficultyStep()) : 0;
    return Clamp0((running ? 5 : 2) + DifficultyStep());
}

static bool32 IsBetweenTiles(struct ObjectEvent *obj)
{
    return !obj->singleMovementActive && (!obj->heldMovementActive || obj->heldMovementFinished);
}

// Takes Asterion off his movement type to do `action`; FALSE while he is mid-step.
static bool32 Steer(struct ObjectEvent *obj, u8 action)
{
    if (!IsBetweenTiles(obj))
        return FALSE;
    ObjectEventClearHeldMovement(obj);
    ObjectEventSetHeldMovement(obj, action);
    return TRUE;
}

static void LeavePatrol(struct ObjectEvent *obj, u32 state)
{
    sLab.aPatrolFacing = obj->facingDirection;
    sLab.aState = state;
    sLab.aPendingFace = TRUE;
}

static void ResumePatrol(struct ObjectEvent *obj)
{
    ObjectEventClearHeldMovement(obj);
    if (sLab.aPatrolFacing != DIR_NONE)
        SetObjectEventDirection(obj, sLab.aPatrolFacing);  // back to his watch
    gSprites[obj->spriteId].data[1] = 0;  // sTypeFuncId: the movement type starts over
    sLab.aState = AST_PATROL;
}

static void ShowIcon(struct ObjectEvent *obj, u32 fieldEffect)
{
    ObjectEventGetLocalIdAndMap(obj, &gFieldEffectArguments[0], &gFieldEffectArguments[1], &gFieldEffectArguments[2]);
    FieldEffectStart(fieldEffect);
}

static bool32 CanSee(struct ObjectEvent *obj, s16 px, s16 py)
{
    u32 d, range = GetAsterionSight();
    u32 code = obj->facingDirection - 1;
    s32 x = obj->currentCoords.x, y = obj->currentCoords.y;

    if (obj->facingDirection < DIR_SOUTH || obj->facingDirection > DIR_EAST)
        return FALSE;
    for (d = 1; d <= range; d++)
    {
        x += sCodeDx[code];
        y += sCodeDy[code];
        if (x == px && y == py)
            return TRUE;
        if (MapGridGetCollisionAt(x, y))  // a wall stops his eye
            return FALSE;
    }
    return FALSE;
}

static u32 DirectionToward(struct ObjectEvent *obj, s16 px, s16 py)
{
    s32 dx = px - obj->currentCoords.x, dy = py - obj->currentCoords.y;
    if (abs(dx) > abs(dy))
        return dx < 0 ? DIR_WEST : DIR_EAST;
    return dy < 0 ? DIR_NORTH : DIR_SOUTH;
}

static u32 GetAlertFrames(void)
{
    static const u8 sFrames[] = { 60, 40, 30 };  // Mortal, Hero, Spartan
    return sFrames[DifficultyStep() + 1];
}

static void Knockdown(struct ObjectEvent *obj)
{
    if (sLab.aOptions & ICHOR_CHARGER_HIT_SCRIPT)
    {
        // The object's own script handles the hit (a knockback, a battle); then it patrols again
        gSpecialVar_0x8004 = sLab.asterionLocalId;
        gSpecialVar_0x8005 = ICHOR_CHARGE_HIT;
        ResumePatrol(obj);
        ScriptContext_SetupScript(GetObjectEventScriptPointerByObjectEventId(obj - gObjectEvents));
        return;
    }
    sLab.aState = AST_DOWN;
    ScriptContext_SetupScript(EventScript_IchorAsterionKnockdown);
}

static const struct Drift *FindDrift(s32 x, s32 y)
{
    u32 i;
    for (i = 0; i < sLab.driftCount; i++)
    {
        if (sLab.drifts[i].x + MAP_OFFSET == x && sLab.drifts[i].y + MAP_OFFSET == y)
            return &sLab.drifts[i];
    }
    return NULL;
}

static struct CrackedWall *FindWall(s32 x, s32 y)
{
    u32 i;
    for (i = 0; i < sLab.wallCount; i++)
    {
        if (!sLab.walls[i].done && sLab.walls[i].x + MAP_OFFSET == x && sLab.walls[i].y + MAP_OFFSET == y)
            return &sLab.walls[i];
    }
    return NULL;
}

static void Stun(struct ObjectEvent *obj, u32 frames)
{
    sLab.aState = AST_STUNNED;
    sLab.aTimer = frames;
    ShowIcon(obj, FLDEFF_QUESTION_MARK_ICON);  // dazed (stand-in for LABYRINTH's stars)
}

static bool32 IsPlayerAt(s32 x, s32 y)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    return (player->currentCoords.x == x && player->currentCoords.y == y)
        || (player->previousCoords.x == x && player->previousCoords.y == y);
}

static void ChargeStep(struct ObjectEvent *obj, s16 px, s16 py)
{
    u32 dir = sLab.aDir;
    s32 nx = obj->currentCoords.x + sCodeDx[dir - 1];
    s32 ny = obj->currentCoords.y + sCodeDy[dir - 1];
    struct CrackedWall *wall;

    const struct Drift *drift;

    if (sLab.aStunAfterStep)
    {
        u32 frames = sLab.aStunAfterStep;
        sLab.aStunAfterStep = 0;
        Stun(obj, frames);
        return;
    }
    if (IsPlayerAt(nx, ny))
    {
        Knockdown(obj);  // he hits you, even half a step out of the way
        return;
    }
    switch (GetCollisionAtCoords(obj, nx, ny, dir))
    {
    case COLLISION_NONE:
        Steer(obj, GetWalkFasterMovementAction(dir));
        sLab.aCharged++;
        if ((drift = FindDrift(nx, ny)) != NULL)
        {
            // A snow drift: he ploughs in and sticks
            if (drift->flag != 0)
                FlagSet(drift->flag);
            sLab.aStunAfterStep = DRIFT_STUCK_FRAMES;
        }
        break;
    default:
        wall = FindWall(nx, ny);
        if (wall == NULL)
        {
            Stun(obj, 120);
            break;
        }
        // Breakthrough: the wall bursts and stays broken; he stumbles into the gap
        wall->done = TRUE;
        MapGridSetMetatileIdAt(nx, ny, wall->broken);
        CurrentMapDrawMetatileAt(nx, ny);
        if (wall->flag != 0)
            FlagSet(wall->flag);
        Steer(obj, GetWalkFastMovementAction(dir));
        sLab.aCharged++;
        sLab.aStunAfterStep = 60;
        ScriptContext_SetupScript(EventScript_IchorAsterionBrokeWall);
        break;
    }
}

static void UpdateAsterion(bool32 stepped, s16 px, s16 py)
{
    struct ObjectEvent *obj = GetAsterion();

    if (obj == NULL || sLab.aState == AST_DOWN || ArePlayerFieldControlsLocked())
        return;

    switch (sLab.aState)
    {
    case AST_PATROL:
        if (CanSee(obj, px, py))
            LeavePatrol(obj, AST_ALERT);
        else if (stepped && !(sLab.aOptions & ICHOR_CHARGER_DEAF)
              && abs(px - obj->currentCoords.x) + abs(py - obj->currentCoords.y) <= GetAsterionHearing())
            LeavePatrol(obj, AST_LISTEN);
        break;
    case AST_LISTEN:
        if (sLab.aPendingFace)
        {
            if (!Steer(obj, GetFaceDirectionMovementAction(DirectionToward(obj, px, py))))
                break;
            sLab.aPendingFace = FALSE;
            sLab.aTimer = 60;
            break;
        }
        if (IsBetweenTiles(obj) && CanSee(obj, px, py))
        {
            sLab.aState = AST_ALERT;
            sLab.aPendingFace = TRUE;
        }
        else if (--sLab.aTimer == 0)
        {
            ResumePatrol(obj);
        }
        break;
    case AST_ALERT:
        if (sLab.aPendingFace)
        {
            // "!", the horns lowered, a scrape of the floor; the player keeps control
            if (!Steer(obj, GetWalkInPlaceFastMovementAction(obj->facingDirection)))
                break;
            ShowIcon(obj, FLDEFF_EXCLAMATION_MARK_ICON);
            sLab.aPendingFace = FALSE;
            sLab.aTimer = GetAlertFrames();
            sLab.aDir = obj->facingDirection;
            break;
        }
        if (--sLab.aTimer == 0)
        {
            sLab.aState = AST_CHARGE;
            sLab.aCharged = 0;
        }
        break;
    case AST_CHARGE:
        if ((obj->currentCoords.x == px && obj->currentCoords.y == py))
        {
            Knockdown(obj);  // the player stepped into him
            break;
        }
        if (IsBetweenTiles(obj))
            ChargeStep(obj, px, py);
        break;
    case AST_STUNNED:
        if (--sLab.aTimer != 0)
            break;
        if (sLab.aOptions & ICHOR_CHARGER_NO_RETURN)
            ResumePatrol(obj);  // turns and goes back to wandering where it stands
        else
            sLab.aState = AST_RETURN;
        break;
    case AST_RETURN:
        if (!IsBetweenTiles(obj))
            break;
        if (sLab.aCharged != 0)
        {
            u32 back = sOppositeCode[sLab.aDir - 1] + 1;
            s32 nx = obj->currentCoords.x + sCodeDx[back - 1];
            s32 ny = obj->currentCoords.y + sCodeDy[back - 1];
            if (GetCollisionAtCoords(obj, nx, ny, back) == COLLISION_NONE)
            {
                Steer(obj, GetWalkNormalMovementAction(back));
                sLab.aCharged--;
                break;
            }
        }
        ResumePatrol(obj);
        break;
    case AST_REST:
        if (!stepped)
            break;
        if (abs(px - obj->currentCoords.x) + abs(py - obj->currentCoords.y) <= 1)
        {
            sLab.aState = AST_LISTEN;  // bumped awake
            sLab.aPendingFace = TRUE;
        }
        else if (--sLab.aRestSteps == 0)
        {
            ResumePatrol(obj);
        }
        break;
    }
}

// special Ichor_AsterionRest: the bronze bell. He lies down for VAR_0x8004
// steps of the player's (30 if 0) and hears and sees nothing, unless bumped.
void Ichor_AsterionRest(void)
{
    struct ObjectEvent *obj = GetAsterion();
    if (obj == NULL)
        return;
    sLab.aPatrolFacing = obj->facingDirection;
    ObjectEventClearHeldMovement(obj);
    ObjectEventSetHeldMovement(obj, GetFaceDirectionMovementAction(DIR_SOUTH));
    sLab.aState = AST_REST;
    sLab.aRestSteps = gSpecialVar_0x8004 ? gSpecialVar_0x8004 : 30;
}

// special Ichor_AsterionKnockdown (then waitstate): the live thread winds in
// and the player wakes at their current anchor, or where they entered this map.
void Ichor_AsterionKnockdown(void)
{
    WindIn();
    if (sThread.currentAnchor < sThread.anchorCount && (sThread.anchors[sThread.currentAnchor].reserved & ANCHOR_TIED))
    {
        struct IchorThreadAnchor *anchor = &sThread.anchors[sThread.currentAnchor];
        WarpToAnchorPos(anchor->mapId, anchor->x, anchor->y);
    }
    else
    {
        WarpToAnchorPos(CurrentMapId(), sLab.entryX - MAP_OFFSET, sLab.entryY - MAP_OFFSET);
    }
}

// --- Dials (§5.5) ----------------------------------------------------------------------------

// special Ichor_TurnDial: flips bit VAR_0x8005 of VAR_0x8004 (a copy of the
// ring's dial var, which the script copies back). VAR_RESULT is the dial's new
// position: 0 (A) or 1 (B).
void Ichor_TurnDial(void)
{
    u16 bit = 1 << (gSpecialVar_0x8005 & 15);
    gSpecialVar_0x8004 ^= bit;
    gSpecialVar_Result = (gSpecialVar_0x8004 & bit) != 0;
}

// --- Every field frame --------------------------------------------------------------------------

// The Helm of Darkness: the player's sprite turns translucent while it's worn.
static void UpdateHelmLook(void)
{
    struct Sprite *sprite = &gSprites[gObjectEvents[gPlayerAvatar.objectEventId].spriteId];
    bool32 helmed = IsHelmed();

    if (helmed && sprite->oam.objMode != ST_OAM_OBJ_BLEND)
    {
        sprite->oam.objMode = ST_OAM_OBJ_BLEND;
        sLab.helmBlend = TRUE;
    }
    else if (!helmed && sLab.helmBlend)
    {
        sprite->oam.objMode = ST_OAM_OBJ_NORMAL;
        sLab.helmBlend = FALSE;
    }
}

void Ichor_LabyrinthFrame(void)
{
    s16 x, y;
    bool32 stepped;

    if (gPlayerAvatar.objectEventId >= OBJECT_EVENTS_COUNT || !gObjectEvents[gPlayerAvatar.objectEventId].active)
        return;
    UpdateHelmLook();

    GetPlayerTile(&x, &y);
    if (!sLab.seenPlayer)
    {
        sLab.seenPlayer = TRUE;
        sLab.lastX = sLab.entryX = x;
        sLab.lastY = sLab.entryY = y;
    }
    stepped = (x != sLab.lastX || y != sLab.lastY);
    if (stepped)
        sLab.recruitBumped = 0;
    if (sLab.floorCount == 0 && sLab.aState == AST_OFF)
    {
        sLab.lastX = x;
        sLab.lastY = y;
        return;
    }

    if (sLab.floorCount != 0 && HasThread())
    {
        if (!sLab.segmentStarted)
            StartMapSegment(x, y);
        else if (stepped)
            OnThreadStep(sLab.lastX, sLab.lastY, x, y);
    }
    UpdateAsterion(stepped, x, y);
    sLab.lastX = x;
    sLab.lastY = y;
}

// A new map: the thread laid on the last one is committed there (segments
// never cross maps), and the last map's registrations are forgotten.
void Ichor_LabyrinthOnMapTransition(void)
{
    bool8 helmBlend = sLab.helmBlend;

    if (sLab.segmentStarted)
        CommitLive();
    memset(&sLab, 0, sizeof(sLab));
    sLab.helmBlend = helmBlend;
}
