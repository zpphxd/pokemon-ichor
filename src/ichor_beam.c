// Ichor: the beam trace (engine need E9, design/phase4/ENGINE_ACT3.md), shared
// by Apollo's Pythian Light at Delphoi and Ring VII's mirrors in the Labyrinth.
//
//   setvar VAR_0x8004, LOCALID_M1        @ the source: the object the light comes from
//   setvar VAR_0x8005, METATILE_BEAM_H   @ the first of the six beam metatiles
//   special Ichor_TraceBeam              @ VAR_RESULT: the local id it ended on, or 0
//
// The beam leaves the source's tile the way the source faces (a mirror under a
// shaft of light, or an invisible lamp object) and runs tile by tile. At a
// mirror (MOVEMENT_TYPE_ICHOR_MIRROR*) it turns the way the mirror faces; a
// mirror facing it head-on or showing it its back ends it. Any other object
// ends it on that object; so does a wall (an impassable tile) or the map's
// edge, with VAR_RESULT 0. The floor it crosses becomes beam metatiles, and the
// corner pieces go under the mirrors it turns at. Tracing a source again first
// puts back the floor its last beam covered.
#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_camera.h"
#include "fieldmap.h"
#include "ichor_beam.h"
#include "ichor_statue.h"

extern const u8 gInitialMovementTypeFacingDirections[];

// Beams remembered at once (each map has at most this many sources), the
// longest beam in tiles, and the most mirrors one can turn at.
#define BEAM_SLOTS      2
#define BEAM_MAX_TILES  128
#define BEAM_MAX_MIRRORS 16

// VAR_0x8005 + these: the six beam metatiles, consecutive in the tileset.
enum BeamPiece
{
    BEAM_EAST_WEST,
    BEAM_NORTH_SOUTH,
    BEAM_NORTH_EAST, // a corner joining the tile's north and east sides
    BEAM_NORTH_WEST,
    BEAM_SOUTH_EAST,
    BEAM_SOUTH_WEST,
    BEAM_PIECE_COUNT,
};

struct BeamTile
{
    u8 x, y;   // MAP_OFFSET coordinates
    u16 block; // the map grid's entry before the beam covered it
};

struct BeamPath
{
    u8 mapGroup;
    u8 mapNum;
    u8 sourceLocalId; // 0: a free slot
    u8 count;
    u16 firstMetatile;
    struct BeamTile tiles[BEAM_MAX_TILES];
};

static EWRAM_DATA struct BeamPath sBeamPaths[BEAM_SLOTS] = {0};

static struct BeamPath *GetBeamPath(u8 sourceLocalId)
{
    u32 i;
    u8 mapGroup = gSaveBlock1Ptr->location.mapGroup, mapNum = gSaveBlock1Ptr->location.mapNum;
    struct BeamPath *path, *spare = NULL;

    for (i = 0; i < BEAM_SLOTS; i++)
    {
        path = &sBeamPaths[i];
        if (path->sourceLocalId == sourceLocalId && path->mapGroup == mapGroup && path->mapNum == mapNum)
            return path;
        if (spare == NULL && (path->sourceLocalId == 0 || path->mapGroup != mapGroup || path->mapNum != mapNum))
            spare = path;
    }
    if (spare == NULL)
        spare = &sBeamPaths[0];
    spare->mapGroup = mapGroup;
    spare->mapNum = mapNum;
    spare->sourceLocalId = sourceLocalId;
    spare->count = 0;
    return spare;
}

static bool32 IsInGrid(s32 x, s32 y)
{
    return x >= 0 && y >= 0 && x < gBackupMapLayout.width && y < gBackupMapLayout.height;
}

// The floor the last beam covered, wherever it still shows the beam (a map
// that has been left and entered again has its own floor back already).
static void RestoreBeamPath(struct BeamPath *path)
{
    u32 i;

    for (i = 0; i < path->count; i++)
    {
        struct BeamTile *tile = &path->tiles[i];
        u32 metatile = MapGridGetMetatileIdAt(tile->x, tile->y);
        if (metatile >= path->firstMetatile && metatile < path->firstMetatile + BEAM_PIECE_COUNT)
            MapGridSetMetatileEntryAt(tile->x, tile->y, tile->block);
    }
    path->count = 0;
}

static void DrawBeamPiece(struct BeamPath *path, s16 x, s16 y, enum BeamPiece piece)
{
    u16 *block;

    if (!IsInGrid(x, y) || path->count >= BEAM_MAX_TILES)
        return;
    block = &gBackupMapLayout.map[x + gBackupMapLayout.width * y];
    path->tiles[path->count].x = x;
    path->tiles[path->count].y = y;
    path->tiles[path->count].block = *block;
    path->count++;
    *block = (*block & ~MAPGRID_METATILE_ID_MASK) | ((path->firstMetatile + piece) & MAPGRID_METATILE_ID_MASK);
}

// The corner under a mirror: the side the beam came in by, and the side it
// leaves by.
static enum BeamPiece GetCornerPiece(enum Direction in, enum Direction out)
{
    bool32 north = (in == DIR_SOUTH || out == DIR_NORTH);
    bool32 east = (in == DIR_WEST || out == DIR_EAST);

    if (north)
        return east ? BEAM_NORTH_EAST : BEAM_NORTH_WEST;
    return east ? BEAM_SOUTH_EAST : BEAM_SOUTH_WEST;
}

// Where the source stands and the way it faces: live, or its template's if it
// is off screen. FALSE if this map has no such object showing.
static bool32 GetSource(u8 localId, s16 *x, s16 *y, enum Direction *facing)
{
    u32 i;
    u8 objectEventId = GetObjectEventIdByLocalIdAndMap(localId, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);

    if (objectEventId < OBJECT_EVENTS_COUNT)
    {
        *x = gObjectEvents[objectEventId].currentCoords.x;
        *y = gObjectEvents[objectEventId].currentCoords.y;
        *facing = gObjectEvents[objectEventId].facingDirection;
        return TRUE;
    }
    for (i = 0; i < gMapHeader.events->objectEventCount; i++)
    {
        const struct ObjectEventTemplate *template = &gSaveBlock1Ptr->objectEventTemplates[i];
        if (template->localId == localId && !FlagGet(template->flagId))
        {
            *x = template->x + MAP_OFFSET;
            *y = template->y + MAP_OFFSET;
            *facing = gInitialMovementTypeFacingDirections[template->movementType];
            return TRUE;
        }
    }
    return FALSE;
}

void Ichor_TraceBeam(void)
{
    struct BeamPath *path = GetBeamPath(gSpecialVar_0x8004);
    struct IchorFieldObject hit;
    enum Direction dir;
    s16 x = MAP_OFFSET, y = MAP_OFFSET;
    u32 tiles, mirrors = 0;

    RestoreBeamPath(path);
    path->firstMetatile = gSpecialVar_0x8005;
    gSpecialVar_Result = 0;

    if (GetSource(gSpecialVar_0x8004, &x, &y, &dir))
    {
        for (tiles = 0; tiles < BEAM_MAX_TILES; tiles++)
        {
            MoveCoords(dir, &x, &y);
            if (Ichor_FieldObjectAt(x, y, &hit))
            {
                enum Direction out;

                if (!Ichor_IsMirror(hit.movementType) || ++mirrors > BEAM_MAX_MIRRORS)
                {
                    gSpecialVar_Result = hit.localId;
                    break;
                }
                out = Ichor_MirrorTurn(dir, hit.facing);
                if (out == DIR_NONE || out == GetOppositeDirection(dir))
                {
                    gSpecialVar_Result = hit.localId; // its back, or head-on
                    break;
                }
                DrawBeamPiece(path, x, y, GetCornerPiece(dir, out));
                dir = out;
                continue;
            }
            if (MapGridGetCollisionAt(x, y))
                break;
            DrawBeamPiece(path, x, y, (dir == DIR_EAST || dir == DIR_WEST) ? BEAM_EAST_WEST : BEAM_NORTH_SOUTH);
        }
    }
    gSpecialVar_0x8006 = x - MAP_OFFSET;
    gSpecialVar_0x8007 = y - MAP_OFFSET;
    DrawWholeMapView();
}
